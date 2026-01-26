from typing import cast

from flask_authx.domain.entities import User
from flask_authx.domain.forms import UserForm
from flask_authx.domain.errors import (
    DatabaseError,
    NotFoundError,
    ConflictError,
    ValidationError,
)
from flask_authx.database.sqlalchemy.models import UserModel
from flask_authx.database.sqlalchemy.shared import (
    get_sqlalchemy,
    handle_database_error,
    handle_integrity_error,
)
from flask_authx.interfaces.repository import IUsersRepository
from flask_authx.utils.result import Result
from flask_authx.container import container


db_session = get_sqlalchemy().session


class SQLAlchemyUsersRepository(IUsersRepository):
    @handle_database_error
    def all(self) -> Result[list[User], DatabaseError]:
        models = db_session.query(UserModel).all()

        return Result.ok([m.to_entity() for m in models])

    @handle_database_error
    def get_by_id(self, id: int) -> Result[User, NotFoundError | DatabaseError]:
        model = db_session.get(UserModel, id)

        if not model:
            return Result.fail(NotFoundError(f"User with id: {id} doesn't exist."))

        return Result.ok(model.to_entity())

    @handle_database_error
    def get_by_name(self, username: str) -> Result[User, NotFoundError | DatabaseError]:
        model = (
            db_session.query(UserModel).filter(UserModel.username == username).first()
        )

        if not model:
            return Result.fail(
                NotFoundError(f"User with username: {username} not found.")
            )

        return Result.ok(model.to_entity())

    @handle_database_error
    @handle_integrity_error
    def add(
        self, new: UserForm
    ) -> Result[User, ConflictError | ValidationError | DatabaseError]:
        model = UserModel.create(new)

        db_session.add(model)
        db_session.commit()

        return Result.ok(model.to_entity())

    @handle_database_error
    def remove(self, id: int) -> Result[None, NotFoundError | DatabaseError]:
        model = db_session.get(UserModel, id)

        if not model:
            return Result.fail(NotFoundError(f"User with id: {id} not found."))

        db_session.delete(model)
        db_session.commit()

        return Result.ok(None)

    @handle_database_error
    @handle_integrity_error
    def update(
        self, id: int, values: dict
    ) -> Result[User, ConflictError | ValidationError | NotFoundError | DatabaseError]:
        rows = db_session.query(UserModel).filter(UserModel.id == id).update(values)
        db_session.commit()

        if rows == 0:
            return Result.fail(NotFoundError(f"User with id: {id} doesn't exist."))

        model = db_session.get(UserModel, id)

        return Result.ok(cast(UserModel, model).to_entity())
