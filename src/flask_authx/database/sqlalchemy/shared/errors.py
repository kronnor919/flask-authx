import sqlalchemy.exc as sae

from flask_authx.errors import (
    ProgrammingError,
    DatabaseError,
    ConflictError,
    ValidationError,
)
from flask_authx.utils.result import Result
from .instance import instance


def handle_database_error(f):
    def wrapper(*args, **kwargs):
        db_session = instance.session
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
        db_session = instance.session
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
