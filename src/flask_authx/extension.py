import os
from typing import Optional, cast

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_authx.database.sqlalchemy.shared import ensure_sqlalchemy
from flask_authx.domain.errors import ConfigurationError, ProgrammingError
from flask_authx.interfaces.database import IDatabaseSetup
from flask_authx.interfaces.repository import ISessionsRepository, IUsersRepository
from flask_authx.interfaces.security import IPasswordHashing
from flask_authx.interfaces.service import IAuthService
from flask_authx.routes.users import UsersRoutes
from flask_authx.routes.auth import AuthRoutes
from flask_authx.security.passwords import BcryptPasswordHashing
from flask_authx.services.auth import AuthService
from flask_authx.container import container


class AuthX:
    def __init__(
        self,
        builder: "AuthXBuilder",
    ) -> None:
        self.app = builder.app
        self.users_repository = builder.users_repository
        self.sessions_repository = builder.sessions_repository
        self.auth_service = builder.auth_service
        self.database_setup = builder.database_setup
        self.auth_routes_prefix = builder.auth_routes_prefix
        self.users_routes_prefix = builder.users_routes_prefix
        self.password_hashing = builder.password_hashing

        if self.app:
            self.init_app(self.app)

    def init_app(self, app: Flask):
        authx: Optional[AuthX] = app.extensions.get("authx")
        sqlalchemy_ext = app.extensions.get("sqlalchemy")

        if authx:
            raise RuntimeError(
                "A 'AuthX' instance has been detected in this app, use that instead (with app['authx'])."
            )

        if not os.path.exists(os.path.join(".", ".env")):
            raise ConfigurationError("Environment file required in root directory.")

        app.extensions["authx"] = self

        if not all([
            self.users_repository,
            self.database_setup,
            self.sessions_repository,
        ]):
            ensure_sqlalchemy(app)

            container.fk_sqlalchemy = cast(SQLAlchemy, sqlalchemy_ext)

            from flask_authx.database.sqlalchemy.repositories.session import (
                SQLAlchemySessionsRepository,
            )
            from flask_authx.database.sqlalchemy.repositories.users import (
                SQLAlchemyUsersRepository,
            )
            from flask_authx.database.sqlalchemy.setup import SQLAlchemyDatabaseSetup

            container.users_repository = SQLAlchemyUsersRepository()
            container.database_setup = SQLAlchemyDatabaseSetup(app)
            container.sessions_repository = SQLAlchemySessionsRepository()

        container.database_setup = self.database_setup or container.database_setup
        container.users_repository = self.users_repository or container.users_repository
        container.sessions_repository = (
            self.sessions_repository or container.sessions_repository
        )
        container.auth_service = self.auth_service or AuthService()
        container.password_hashing = self.password_hashing or BcryptPasswordHashing()

        container.database_setup.init()

        UsersRoutes(
            self.users_routes_prefix,
            app=app,
        )
        AuthRoutes(
            prefix=self.auth_routes_prefix,
            app=app,
        )


class AuthXBuilder:
    def __init__(self, app: Flask):
        self.app = app
        self.auth_routes_prefix: str = "/auth"
        self.users_routes_prefix: str = "/users"

        self.users_repository: Optional[IUsersRepository] = None
        self.sessions_repository: Optional[ISessionsRepository] = None
        self.database_setup: Optional[IDatabaseSetup] = None
        self.auth_service: Optional[IAuthService] = None
        self.password_hashing: Optional[IPasswordHashing] = None

    def set_users_repository(self, repository: IUsersRepository):
        self.users_repository = repository
        return self

    def set_sessions_repository(self, repository: ISessionsRepository):
        self.sessions_repository = repository
        return self

    def set_auth_service(self, service: IAuthService):
        self.auth_service = service
        return self

    def set_database_setup(self, setup: IDatabaseSetup):
        self.database_setup = setup
        return self

    def set_auth_prefix(self, prefix: str):
        if not prefix.startswith("/"):
            raise ProgrammingError("Routes prefixes must start with slash ('/')")
        self.auth_routes_prefix = prefix
        return self

    def set_users_prefix(self, prefix: str):
        if not prefix.startswith("/"):
            raise ProgrammingError("Routes prefixes must start with slash ('/')")
        self.users_routes_prefix = prefix
        return self

    def set_password_hashing(self, component: IPasswordHashing):
        self.password_hashing = component
        return self

    def build(self) -> AuthX:
        return AuthX(self)
