from pytest import fixture
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


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
