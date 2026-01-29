from functools import wraps
from flask import request

from flask_authx.errors import DatabaseError, NotFoundError
from flask_authx.interfaces.repository import ISessionsRepository
from flask_authx.utils.responses import (
    InternalErrorResponse,
    RequireAuthenticationResponse,
)


def require_authentication(session_repository: ISessionsRepository):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            header = request.headers.get("Authorization")

            if not header or not header.startswith("Bearer "):
                return RequireAuthenticationResponse.create()

            parts = header.split(" ")
            if len(parts) != 2:
                return RequireAuthenticationResponse.create()

            token = parts[1]

            # This means that the client is not authenticated
            if not token:
                return RequireAuthenticationResponse.create()

            res = session_repository.get_by_token(token)

            if not res.success:
                if res.error_is(NotFoundError):
                    return RequireAuthenticationResponse.create()

                elif res.error_is(DatabaseError):
                    return InternalErrorResponse.create(res.error.message)

            return f(*args, **kwargs, user=res.value.user)

        return wrapper

    return decorator
