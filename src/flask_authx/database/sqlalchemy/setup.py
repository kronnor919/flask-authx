from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_authx.errors import (
    AppError,
    DatabaseError,
    NotFoundError,
    ConfigurationError,
)
from flask_authx.forms import UserForm
from flask_authx.role import Role
from flask_authx.interfaces.database import IDatabaseSetup
from flask_authx.interfaces.service import IUsersService
from flask_authx.database.sqlalchemy.models import UserModel, SessionModel  # noqa
from flask_authx.config import FIRST_USER_NAME, FIRST_USER_PASSWORD


class SQLAlchemyDatabaseSetup(IDatabaseSetup):
    def __init__(self, app: Flask, users_service: IUsersService) -> None:
        self.app = app
        self.sqlalchemy: SQLAlchemy = app.extensions["sqlalchemy"]
        self.users_service = users_service

    def init(self) -> None:
        with self.app.app_context():
            if not self.app.extensions.get("migrate"):
                self.sqlalchemy.create_all()

            res = self.users_service.get_by_name(FIRST_USER_NAME)

            if not res.success:
                if res.error_is(NotFoundError):
                    first_user = UserForm(
                        username=FIRST_USER_NAME,
                        password=FIRST_USER_PASSWORD,
                        role=Role.admin,
                    )

                    add_res = self.users_service.add(first_user)

                    if not add_res.success:
                        raise DatabaseError(
                            (
                                "It was not possible to create the first "
                                f"administrator user. Error: {add_res.error.message}"
                            )
                        )

                elif res.error_is(DatabaseError):
                    raise DatabaseError(res.error.message)

                else:
                    raise AppError(f"Unexpected error: {res.error}")
