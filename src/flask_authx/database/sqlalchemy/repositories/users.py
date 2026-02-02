from flask_authx.entities import User
from flask_authx.forms import UserForm, UserUpdateData
from flask_authx.errors import (
    DatabaseError,
    NotFoundError,
    ConflictError,
    ValidationError,
)
from flask_authx.database.sqlalchemy.models import UserModel
from flask_authx.database.sqlalchemy.shared.instance import instance
from flask_authx.database.sqlalchemy.shared.errors import (
    handle_database_error,
    handle_integrity_error,
)
from flask_authx.interfaces.repository import IUsersRepository
from flask_authx.utils.result import Result


class SQLAlchemyUsersRepository(IUsersRepository):
    COLUMN_MAPPER = {
        "username": "username",
        "is_authenticated": "is_authenticated",
        "role": "role",
    }

    def __init__(self) -> None:
        super().__init__()

    @handle_database_error
    def all(self) -> Result[list[User], DatabaseError]:
        models = instance.session.query(UserModel).all()

        return Result.ok([m.to_entity() for m in models])

    @handle_database_error
    def get_by_id(self, id: int) -> Result[User, NotFoundError | DatabaseError]:
        model = instance.session.get(UserModel, id)

        if not model:
            return Result.fail(NotFoundError(f"User with id: {id} doesn't exist."))

        return Result.ok(model.to_entity())

    @handle_database_error
    def get_by_name(self, username: str) -> Result[User, NotFoundError | DatabaseError]:
        model = (
            instance.session.query(UserModel)
            .filter(UserModel.username == username)
            .first()
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

        instance.session.add(model)
        instance.session.commit()

        return Result.ok(model.to_entity())

    @handle_database_error
    def remove(self, id: int) -> Result[None, NotFoundError | DatabaseError]:
        model = instance.session.get(UserModel, id)

        if not model:
            return Result.fail(NotFoundError(f"User with id: {id} not found."))

        instance.session.delete(model)
        instance.session.commit()

        return Result.ok(None)

    @handle_database_error
    @handle_integrity_error
    def update(
        self, id: int, values: UserUpdateData
    ) -> Result[User, ConflictError | ValidationError | NotFoundError | DatabaseError]:
        model = instance.session.get(UserModel, id)

        if not model:
            return Result.fail(NotFoundError(f"User with id: {id} not found."))

        for k, v in values.items():
            if k in self.COLUMN_MAPPER:
                setattr(model, self.COLUMN_MAPPER[k], v)

        instance.session.commit()

        return Result.ok(model.to_entity())
