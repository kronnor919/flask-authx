from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_authx.domain.errors import (
    AppError,
    DatabaseError,
    NotFoundError,
    ConfigurationError,
)
from flask_authx.domain.forms import UserForm
from flask_authx.domain.value_objects import Role
from flask_authx.interfaces.database import IDatabaseSetup
from flask_authx.interfaces.repository import IUsersRepository
from flask_authx.database.sqlalchemy.models import UserModel, SessionModel  # noqa
from flask_authx.config import FIRST_USER_NAME, FIRST_USER_PASSWORD


class SQLAlchemyDatabaseSetup(IDatabaseSetup):
    def __init__(self, app: Flask, users_repository: IUsersRepository) -> None:
        self.app = app
        self.sqlalchemy: SQLAlchemy = app.extensions["sqlalchemy"]
        self.users_repository = users_repository

    def init(self) -> None:
        with self.app.app_context():
            if not self.app.extensions.get("migrate"):
                self.sqlalchemy.create_all()

            res = self.users_repository.get_by_name(FIRST_USER_NAME)

            if not res.success:
                if res.error_is(NotFoundError):
                    first_user = UserForm(
                        username=FIRST_USER_NAME,
                        password=FIRST_USER_PASSWORD,
                        role=Role.admin,
                    )
                    valid_res = first_user.is_valid()

                    if not valid_res.success:
                        raise ConfigurationError(
                            "The entered credentials for the first admin are not valid."
                        )

                    self.users_repository.add(first_user)

                elif res.error_is(DatabaseError):
                    raise DatabaseError(res.error.message)

                else:
                    raise AppError(f"Unexpected error: {res.error}")
