import os
from pytest import fixture
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


@fixture
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


@fixture(autouse=True)
def env_config():
    env_path = ".env"

    with open(env_path, "w") as f:
        f.writelines(['SUPERUSER_NAME="admin"\n', 'SUPERUSER_PASSWORD="14/10/10"'])

    yield

    os.remove(env_path)
