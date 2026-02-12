import pytest
from unittest.mock import Mock
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_authx import (
    AuthX,
    AuthXBuilder,
    IAuthService,
    IUsersRepository,
    ISessionsRepository,
    IDatabaseSetup,
    IPasswordHashing,
)
from flask_authx._interfaces.service import IUsersService
from flask_authx._errors import ProgrammingError, ConfigurationError
from flask_authx import config
from flask_authx._database.sqlalchemy.shared.instance import (
    ensure_sqlalchemy,
    set_sqlalchemy,
    get_instance,
)


class TestBuilder:
    def test_builder_creation(self, builder):
        assert builder.auth_routes_prefix == "/auth"
        assert builder.users_routes_prefix == "/users"

    def test_set_valid_prefixes(self, builder):
        builder.set_auth_prefix("/api/auth")

        assert builder.auth_routes_prefix == "/api/auth"

    def test_set_prefix_without_slash(self, builder):
        with pytest.raises(ProgrammingError):
            builder.set_auth_prefix("api/auth")

    def test_set_empty_prefix(self, builder):
        with pytest.raises(ProgrammingError):
            builder.set_auth_prefix("")

    def test_method_chaining(self, builder):
        auth_service = Mock(spec=IAuthService)

        result = builder.set_auth_service(auth_service).set_users_prefix("/accounts")

        assert builder.auth_service is auth_service
        assert builder is result

    def test_build_returns_authx(self, builder):
        user_repo = Mock(IUsersRepository)
        sess_repo = Mock(ISessionsRepository)
        db_setup = Mock(IDatabaseSetup)

        authx = (
            builder.set_users_repository(user_repo)
            .set_database_setup(db_setup)
            .set_sessions_repository(sess_repo)
            .build()
        )

        assert isinstance(authx, AuthX)


class TestAuthX:
    def test_init_app_registers_extension(self, builder):
        # Use mocks to avoid triggering full database initialization
        from unittest.mock import Mock

        user_repo = Mock(spec=IUsersRepository)
        sess_repo = Mock(spec=ISessionsRepository)
        db_setup = Mock(spec=IDatabaseSetup)

        authx = (
            builder.set_users_repository(user_repo)
            .set_database_setup(db_setup)
            .set_sessions_repository(sess_repo)
            .build()
        )
        app = authx.app

        assert "authx" in app.extensions
        assert app.extensions.get("authx")

    def test_init_app_prevents_duplicate_registration(self, app_with_sqlalchemy):
        b1 = AuthXBuilder(app_with_sqlalchemy)
        b2 = AuthXBuilder(app_with_sqlalchemy)

        b1.build()

        with pytest.raises(RuntimeError):
            b2.build()

    def test_default_services_creation(self, builder: AuthXBuilder):
        authx = builder.build()

        assert isinstance(authx.auth_service, IAuthService)
        assert isinstance(authx.users_service, IUsersService)
        assert isinstance(authx.password_hashing, IPasswordHashing)
        assert isinstance(authx.database_setup, IDatabaseSetup)
        assert isinstance(authx.sessions_repository, ISessionsRepository)
        assert isinstance(authx.users_repository, IUsersRepository)

    def test_load_valid_config(self, app):
        USERNAME = "kronnor"
        PASSWORD = "securepassword123"

        app.config["FIRST_USER_NAME"] = USERNAME
        app.config["FIRST_USER_PASSWORD"] = PASSWORD

        config.load_config(app.config)

        assert config.FIRST_USER_NAME == USERNAME
        assert config.FIRST_USER_PASSWORD == PASSWORD

    def test_load_config_without_username(self, app):
        app.config["FIRST_USER_PASSWORD"] = "subliminal message"

        with pytest.raises(ConfigurationError) as exc_info:
            config.load_config(app.config)

        assert "FIRST_USER_NAME" in str(exc_info)

    def test_load_config_without_password(self, app):
        app.config["FIRST_USER_NAME"] = "kcid"

        with pytest.raises(ConfigurationError) as exc_info:
            config.load_config(app.config)

        assert "FIRST_USER_PASSWORD" in str(exc_info)

    def test_load_empty_config(self, app):
        with pytest.raises(ConfigurationError):
            config.load_config(app.config)


class TestSQLAlchemy:
    def test_ensure_sqlalchemy_with_extension(self):
        app = Flask(__name__)

        sa = Mock(spec=SQLAlchemy)
        app.extensions["sqlalchemy"] = sa

        db = ensure_sqlalchemy(app)

        assert db is not None
        assert sa is db

    def test_ensure_sqlalchemy_without_extension(self):
        app = Flask(__name__)

        with pytest.raises(RuntimeError):
            ensure_sqlalchemy(app)

    def test_set_sqlalchemy_updates_global(self):
        app = Flask(__name__)

        mock_sa = Mock()
        app.extensions["sqlalchemy"] = mock_sa

        set_sqlalchemy(app)

        assert get_instance() is mock_sa
