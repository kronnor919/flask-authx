from typing import cast
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy.exc as sae

from flask_authx.domain.errors import (
    ProgrammingError,
    DatabaseError,
    ConflictError,
    ValidationError,
)
from flask_authx.utils.result import Result
from flask_authx.container import container


def get_sqlalchemy():
    return cast(SQLAlchemy, container.fk_sqlalchemy)


def ensure_sqlalchemy(app: Flask):
    if not app.extensions.get("sqlalchemy"):
        raise RuntimeError(
            "App must have initialized 'SQLAlchemy' instance, from `Flask-SQLAlchemy` extension. Or define your own database configuration via `AuthXBuilder`."
        )


def handle_database_error(f):
    def wrapper(*args, **kwargs):
        db_session = get_sqlalchemy().session
        try:
            return f(*args, **kwargs)

        except sae.ProgrammingError as ex:
            db_session.rollback()
            raise ProgrammingError(str(ex))

        except sae.SQLAlchemyError as ex:
            db_session.rollback()
            return Result.fail(DatabaseError(str(ex)))

    return wrapper


def handle_integrity_error(f):
    def wrapper(*args, **kwargs):
        db_session = get_sqlalchemy().session
        try:
            return f(*args, **kwargs)

        except sae.IntegrityError as ex:
            if "unique" in str(ex).lower():
                return Result.fail(
                    ConflictError("Two rows cannot have the same identificator.")
                )
            db_session.rollback()
            return Result.fail(ValidationError(str(ex)))

    return wrapper
