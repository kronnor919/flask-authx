from pytest import fixture
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_authx import AuthXBuilder


@fixture(scope="session")
def app():
    app = Flask(__name__)

    app.config.from_mapping(
        {
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "TESTING": True,
        }
    )

    SQLAlchemy(app)

    return app


@fixture(scope="session")
def builded_app(app: Flask):
    app.config.from_mapping(
        {
            "FIRST_USER_NAME": "kronnor",
            "FIRST_USER_PASSWORD": "73336463",
        }  # This values MUST BE NOT CHANGED (break the tests)
    )

    AuthXBuilder(app).build()

    return app


@fixture(scope="session")
def app_client(builded_app: Flask):
    with builded_app.test_client() as c:
        return c
