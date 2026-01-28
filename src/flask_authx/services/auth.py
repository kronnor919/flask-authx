from flask_authx.domain.entities import Session, User
from flask_authx.domain.forms import SessionForm, UserForm
from flask_authx.domain.errors import (
    ConflictError,
    DatabaseError,
    InvalidCredentialsError,
    NotAuthenticatedError,
    NotFoundError,
)
from flask_authx.interfaces.repository import ISessionsRepository, IUsersRepository
from flask_authx.interfaces.service import IAuthService
from flask_authx.interfaces.security import IPasswordHashing
from flask_authx.security.tokens import generate_access_token
from flask_authx.utils.result import Result


class AuthService(IAuthService):
    def __init__(
        self,
        sessions_repository: ISessionsRepository,
        users_repository: IUsersRepository,
        password_hashing: IPasswordHashing,
    ) -> None:
        self.sessions_db = sessions_repository
        self.users_db = users_repository
        self.password_hashing = password_hashing

    def login(
        self, u: UserForm
    ) -> Result[
        Session,
        InvalidCredentialsError | ConflictError | DatabaseError,
    ]:
        user_res = self.users_db.get_by_name(u.username)

        if not user_res.success:
            return Result.fail(InvalidCredentialsError("Invalid credentials"))

        user = user_res.value  # Contains hashed password

        if not self.password_hashing.verify(u.password, user.password):
            return Result.fail(InvalidCredentialsError("Invalid credentials"))

        upd_auth_res = self.users_db.update(user.id, {"is_authenticated": True})

        if not upd_auth_res.success:
            return Result.fail(DatabaseError("Cannot update the state of the user"))

        new_session = SessionForm(token=generate_access_token(), user=user)
        new_sess_res = self.sessions_db.add(new_session)

        if not new_sess_res.success:
            if new_sess_res.error_is(ConflictError):
                return Result.fail(ConflictError("User is already logged in"))

            else:
                return Result.fail(DatabaseError("Cannot create the new session"))

        return Result.ok(new_sess_res.value)

    def logout(self, user: User) -> Result[None, NotAuthenticatedError | DatabaseError]:
        sess_res = self.sessions_db.get_by_user(user.id)

        if not sess_res.success:
            if sess_res.error_is(NotFoundError):
                return Result.fail(
                    NotAuthenticatedError(f"No session linked to user {user.id}")
                )

            else:
                return Result.fail(DatabaseError("Cannot find the session"))

        sess = sess_res.value

        rem_sess_res = self.sessions_db.remove(sess.token)

        if not rem_sess_res.success:
            return Result.fail(DatabaseError(rem_sess_res.error.message))

        upd_usr_res = self.users_db.update(user.id, {"is_authenticated": True})

        if not upd_usr_res.success:
            return Result.fail(DatabaseError(upd_usr_res.error.message))

        return Result.ok(None)
