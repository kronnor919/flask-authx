import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_authx import AuthXBuilder


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["TESTING"] = True

    return app


@pytest.fixture
def app_with_sqlalchemy():
    app = Flask(__name__)

    app.config["TESTING"] = True
    app.config["FIRST_USER_NAME"] = "admin"
    app.config["FIRST_USER_PASSWORD"] = "subliminal message"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    SQLAlchemy(app)

    return app


@pytest.fixture
def builder():
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.config["FIRST_USER_NAME"] = "admin"
    app.config["FIRST_USER_PASSWORD"] = "subliminal message"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    db = SQLAlchemy(app)

    with app.app_context():
        import flask_authx.database.sqlalchemy.shared.instance as instance_module
        from flask_authx.database.sqlalchemy.shared.instance import set_sqlalchemy

        instance_module.instance = None
        set_sqlalchemy(app)

    authx_builder = AuthXBuilder(app)
    return authx_builder
