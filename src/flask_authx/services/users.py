from flask_authx.entities import User
from flask_authx.errors import (
    ConflictError,
    DatabaseError,
    NotFoundError,
    ValidationError,
)
from flask_authx.forms import UserForm, UserUpdateData
from flask_authx.interfaces.service import IUsersService
from flask_authx.interfaces.repository import IUsersRepository
from flask_authx.interfaces.security import IPasswordHashing
from flask_authx.role import Role
from flask_authx.utils.result import Result


class UsersService(IUsersService):
    def __init__(
        self, users_repository: IUsersRepository, password_hashing: IPasswordHashing
    ) -> None:
        self.users_repository = users_repository
        self.password_hashing = password_hashing

    def all(self) -> Result[list[User], DatabaseError]:
        res = self.users_repository.all()

        if not res.success:
            return Result.fail(DatabaseError(res.error.message))

        return Result.ok(res.value)

    def get_by_id(self, id: int) -> Result[User, NotFoundError | DatabaseError]:
        res = self.users_repository.get_by_id(id)

        if not res.success:
            if res.error_is(NotFoundError):
                return Result.fail(NotFoundError(f"User with id {id} not found"))

            return Result.fail(DatabaseError(res.error.message))

        return Result.ok(res.value)

    def get_by_name(self, username: str) -> Result[User, NotFoundError | DatabaseError]:
        res = self.users_repository.get_by_name(username)

        if not res.success:
            if res.error_is(NotFoundError):
                return Result.fail(
                    NotFoundError(f"User with name {username} not found")
                )

            return Result.fail(DatabaseError(res.error.message))

        return Result.ok(res.value)

    def add(
        self, form: UserForm
    ) -> Result[User, ConflictError | ValidationError | DatabaseError]:
        if not form.is_valid().success:
            return Result.fail(ValidationError("Invalid user form data"))

        existing_user_res = self.users_repository.get_by_name(form.username)

        if existing_user_res.success:
            return Result.fail(
                ConflictError(f"User with name {form.username} already exists")
            )

        hashed_password = self.password_hashing.hash(form.password)
        new_form = UserForm(
            username=form.username, password=hashed_password, role=form.role
        )

        add_res = self.users_repository.add(new_form)

        if not add_res.success:
            return Result.fail(DatabaseError(add_res.error.message))

        return Result.ok(add_res.value)

    def remove(self, id: int) -> Result[None, NotFoundError | DatabaseError]:
        res = self.users_repository.remove(id)

        if not res.success:
            if res.error_is(NotFoundError):
                return Result.fail(NotFoundError(f"User with id {id} not found"))
            return Result.fail(DatabaseError(res.error.message))

        return Result.ok(None)

    def update_name(
        self, id: int, new_username: str
    ) -> Result[User, ValidationError | NotFoundError | ConflictError | DatabaseError]:
        valid_name_res = User.validate_username(new_username)

        if not valid_name_res.success:
            return Result.fail(
                ValidationError(
                    f"Invalid username. INFO: {valid_name_res.error.message}"
                )
            )

        existing_user_res = self.users_repository.get_by_name(new_username)

        if existing_user_res.success:
            return Result.fail(
                ConflictError(f"User with name {new_username} already exists")
            )

        else:
            if existing_user_res.error_is(DatabaseError):
                return Result.fail(DatabaseError(existing_user_res.error.message))

        update_data: UserUpdateData = {"username": new_username}
        update_res = self.users_repository.update(id, update_data)

        if not update_res.success:
            if update_res.error_is(NotFoundError):
                return Result.fail(NotFoundError(f"User with id {id} not found"))

            return Result.fail(DatabaseError(update_res.error.message))

        return Result.ok(update_res.value)

    def update_role(
        self, id: int, role: Role
    ) -> Result[User, NotFoundError | DatabaseError]:
        update_data: UserUpdateData = {"role": role}
        update_res = self.users_repository.update(id, update_data)

        if not update_res.success:
            if update_res.error_is(NotFoundError):
                return Result.fail(NotFoundError(f"User with id {id} not found"))

            return Result.fail(DatabaseError("Cannot update user role"))

        return Result.ok(update_res.value)

    def mark_authenticated(
        self, id: int
    ) -> Result[User, NotFoundError | DatabaseError]:
        update_data: UserUpdateData = {"is_authenticated": True}
        update_res = self.users_repository.update(id, update_data)

        if not update_res.success:
            if update_res.error_is(NotFoundError):
                return Result.fail(NotFoundError(f"User with id {id} not found"))

            return Result.fail(DatabaseError("Cannot mark user as authenticated"))

        return Result.ok(update_res.value)

    def mark_unauthenticated(
        self, id: int
    ) -> Result[User, NotFoundError | DatabaseError]:
        update_data: UserUpdateData = {"is_authenticated": False}
        update_res = self.users_repository.update(id, update_data)

        if not update_res.success:
            if update_res.error_is(NotFoundError):
                return Result.fail(NotFoundError(f"User with id {id} not found"))

            return Result.fail(DatabaseError("Cannot mark user as unauthenticated"))

        return Result.ok(update_res.value)

    def is_authenticated(self, id: int) -> Result[bool, NotFoundError | DatabaseError]:
        res = self.users_repository.get_by_id(id)

        if not res.success:
            if res.error_is(NotFoundError):
                return Result.fail(NotFoundError(f"User with id {id} not found"))

            return Result.fail(DatabaseError(res.error.message))

        return Result.ok(res.value.is_authenticated)
