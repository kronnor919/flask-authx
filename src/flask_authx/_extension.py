from typing import Optional
from flask import Flask

from flask_authx._database.sqlalchemy.shared.instance import (
    set_sqlalchemy,
)
from flask_authx._errors import ProgrammingError
from flask_authx._interfaces.database import IDatabaseSetup
from flask_authx._interfaces.repository import ISessionsRepository, IUsersRepository
from flask_authx._interfaces.security import IPasswordHashing
from flask_authx._interfaces.service import IAuthService
from flask_authx._routes.users import UsersRoutes
from flask_authx._routes.auth import AuthRoutes
from flask_authx._services.password_hashing import BcryptPasswordHashing
from flask_authx._services.auth import AuthService
from flask_authx.config import load_config
from flask_authx._services.users import IUsersService, UsersService


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
        self.users_service = builder.users_service

        if self.app:
            self.init_app(self.app)

    def init_app(self, app: Flask):
        authx: Optional[AuthX] = app.extensions.get("authx")

        if authx:
            raise RuntimeError(
                "A 'AuthX' instance has been detected in this app, use that instead (with app['authx'])."
            )

        app.extensions["authx"] = self

        load_config(app.config)

        self.password_hashing = self.password_hashing or BcryptPasswordHashing()

        if (
            not self.database_setup
            or not self.users_repository
            or not self.sessions_repository
        ):
            set_sqlalchemy(app)

            from flask_authx._database.sqlalchemy.repositories.session import (
                SQLAlchemySessionsRepository,
            )
            from flask_authx._database.sqlalchemy.repositories.users import (
                SQLAlchemyUsersRepository,
            )
            from flask_authx._database.sqlalchemy.setup import SQLAlchemyDatabaseSetup

            self.users_repository = SQLAlchemyUsersRepository()
            self.users_service = self.users_service or UsersService(
                self.users_repository, self.password_hashing
            )
            self.database_setup = SQLAlchemyDatabaseSetup(app, self.users_service)
            self.sessions_repository = SQLAlchemySessionsRepository()

        self.users_service = self.users_service or UsersService(
            self.users_repository, self.password_hashing
        )

        self.auth_service = self.auth_service or AuthService(
            self.sessions_repository, self.users_service, self.password_hashing
        )

        self.database_setup.init()

        UsersRoutes(
            self.users_service,
            self.sessions_repository,
            prefix=self.users_routes_prefix,
            app=app,
        )

        AuthRoutes(
            self.auth_service,
            self.sessions_repository,
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
        self.users_service: Optional[IUsersService] = None

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

    def set_users_service(self, component: IUsersService):
        self.users_service = component
        return self

    def build(self) -> AuthX:
        return AuthX(self)
