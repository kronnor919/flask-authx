from flask_authx.forms import SessionForm
from flask_authx.entities import Session
from flask_authx.errors import (
    ConflictError,
    DatabaseError,
    NotFoundError,
    ValidationError,
)
from flask_authx.database.sqlalchemy.shared.instance import get_instance
from flask_authx.database.sqlalchemy.models import get_session_model
from flask_authx.database.sqlalchemy.shared.errors import (
    handle_database_error,
    handle_integrity_error,
)
from flask_authx.interfaces.repository import ISessionsRepository
from flask_authx.utils.result import Result


class SQLAlchemySessionsRepository(ISessionsRepository):
    def __init__(self) -> None:
        super().__init__()
        self.SessionModel = get_session_model()

    @handle_database_error
    def all(self) -> Result[list[Session], DatabaseError]:
        sessions = get_instance().session.query(self.SessionModel).all()
        return Result.ok([s.to_entity() for s in sessions])

    @handle_database_error
    def get_by_token(
        self, token: str
    ) -> Result[Session, NotFoundError | DatabaseError]:
        sess = get_instance().session.get(self.SessionModel, token)
        if not sess:
            return Result.fail(
                NotFoundError(f"Session with token: {token} doesn't exist.")
            )
        return Result.ok(sess.to_entity())

    @handle_database_error
    def get_by_user(
        self, user_id: int
    ) -> Result[Session, NotFoundError | DatabaseError]:
        sess = (
            get_instance()
            .session.query(self.SessionModel)
            .filter(self.SessionModel.user_id == user_id)
            .first()
        )

        if not sess:
            return Result.fail(
                NotFoundError(f"Session for user with id: {user_id} doesn't exist.")
            )

        return Result.ok(sess.to_entity())

    @handle_database_error
    @handle_integrity_error
    def add(
        self, new: SessionForm
    ) -> Result[Session, ConflictError | ValidationError | DatabaseError]:
        model = self.SessionModel.create(new)
        get_instance().session.add(model)
        get_instance().session.commit()
        return Result.ok(model.to_entity())

    @handle_database_error
    def remove(self, token: str) -> Result[None, NotFoundError | DatabaseError]:
        model = get_instance().session.get(self.SessionModel, token)
        if not model:
            return Result.fail(
                NotFoundError(f"Session with token: {token} doesn't exist.")
            )
        get_instance().session.delete(model)
        get_instance().session.commit()
        return Result.ok(None)

    @handle_database_error
    def remove_by_user(
        self, user_id: int
    ) -> Result[None, NotFoundError | DatabaseError]:
        model = (
            get_instance()
            .session.query(self.SessionModel)
            .filter(self.SessionModel.user_id == user_id)
            .first()
        )

        if not model:
            return Result.fail(
                NotFoundError(f"Session for user with id: {user_id} doesn't exist.")
            )

        get_instance().session.delete(model)
        get_instance().session.commit()
        return Result.ok(None)
