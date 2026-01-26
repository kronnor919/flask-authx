from flask_authx.domain.forms import SessionForm
from flask_authx.domain.entities import Session
from flask_authx.domain.errors import (
    ConflictError,
    DatabaseError,
    NotFoundError,
    ValidationError,
)
from flask_authx.database.sqlalchemy.models import SessionModel
from flask_authx.database.sqlalchemy.shared import (
    get_sqlalchemy,
    handle_database_error,
    handle_integrity_error,
)
from flask_authx.interfaces.repository import ISessionsRepository
from flask_authx.utils.result import Result


db_session = get_sqlalchemy().session


class SQLAlchemySessionsRepository(ISessionsRepository):
    @handle_database_error
    def all(self) -> Result[list[Session], DatabaseError]:
        sessions = db_session.query(SessionModel).all()

        return Result.ok([s.to_entity() for s in sessions])

    @handle_database_error
    def get_by_token(
        self, token: str
    ) -> Result[Session, NotFoundError | DatabaseError]:
        sess = db_session.get(SessionModel, token)

        if not sess:
            return Result.fail(NotFoundError("Invalid access token"))

        return Result.ok(sess.to_entity())

    @handle_database_error
    def get_by_user(
        self, user_id: int
    ) -> Result[Session, NotFoundError | DatabaseError]:
        sess = (
            db_session.query(SessionModel)
            .filter(SessionModel.user_id == user_id)
            .one_or_none()
        )

        if not sess:
            return Result.fail(
                NotFoundError(f"No session linked to user with id: {user_id}")
            )

        return Result.ok(sess.to_entity())

    @handle_database_error
    @handle_integrity_error
    def add(
        self, new: SessionForm
    ) -> Result[Session, ConflictError | ValidationError | DatabaseError]:
        model = SessionModel.create(new)

        db_session.add(model)
        db_session.commit()

        return Result.ok(model.to_entity())

    @handle_database_error
    def remove(self, token: str) -> Result[None, NotFoundError | DatabaseError]:
        model = db_session.get(SessionModel, token)

        if not model:
            return Result.fail(NotFoundError("Invalid session token."))

        db_session.delete(model)
        db_session.commit()

        return Result.ok(None)

    @handle_database_error
    def remove_by_user(
        self, user_id: int
    ) -> Result[None, NotFoundError | DatabaseError]:
        model = (
            db_session.query(SessionModel)
            .filter(SessionModel.user_id == user_id)
            .one_or_none()
        )

        if not model:
            return Result.fail(NotFoundError("User doesn't have an active session."))

        db_session.delete(model)
        db_session.commit()

        return Result.ok(None)
