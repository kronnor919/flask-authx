from typing import Optional
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from flask_authx.interfaces.database import IDatabaseSetup
from flask_authx.interfaces.repository import ISessionsRepository, IUsersRepository
from flask_authx.interfaces.security import IPasswordHashing
from flask_authx.interfaces.service import IAuthService


class Container:
    _fk_sqlalchemy: Optional[SQLAlchemy] = None
    _fk_migrate: Optional[Migrate] = None
    _auth_service: IAuthService
    _users_repository: IUsersRepository
    _sessions_repository: ISessionsRepository
    _database_setup: IDatabaseSetup
    _password_hashing: IPasswordHashing

    @property
    def auth_service(self):
        return self._auth_service

    @auth_service.setter
    def auth_service(self, service: IAuthService):
        self._auth_service = service

    @property
    def users_repository(self):
        return self._users_repository

    @users_repository.setter
    def users_repository(self, repo: IUsersRepository):
        self._users_repository = repo

    @property
    def sessions_repository(self):
        return self._sessions_repository

    @sessions_repository.setter
    def sessions_repository(self, repo: ISessionsRepository):
        self._sessions_repository = repo

    @property
    def database_setup(self):
        return self._database_setup

    @database_setup.setter
    def database_setup(self, setup: IDatabaseSetup):
        self._database_setup = setup

    @property
    def fk_sqlalchemy(self):
        return self._fk_sqlalchemy

    @fk_sqlalchemy.setter
    def fk_sqlalchemy(self, sqlalchemy: SQLAlchemy):
        self._fk_sqlalchemy = sqlalchemy

    @property
    def fk_migrate(self):
        return self._fk_migrate

    @fk_migrate.setter
    def fk_migrate(self, migrate: Migrate):
        self._fk_migrate = migrate

    @property
    def password_hashing(self):
        return self._password_hashing

    @password_hashing.setter
    def password_hashing(self, component: IPasswordHashing):
        self._password_hashing = component


container = Container()
