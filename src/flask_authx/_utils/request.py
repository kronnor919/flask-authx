from functools import wraps
from flask import request

from flask_authx._utils.responses import (
    MissingJsonFieldsResponse,
    JSONRequiredResponse,
    MissingQueryParamsResponse,
)


def json_fields(*, required: list[str] = [], optional: list[str] = []):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not request.is_json:
                return JSONRequiredResponse.create()

            json: dict = request.json  # type: ignore
            missing: list[str] = []

            for fld in required + optional:
                if fld in required and fld not in json:
                    missing.append(fld)
                    continue
                kwargs[fld] = json[fld]

            if len(missing) != 0:
                return MissingJsonFieldsResponse.create(*missing)

            return f(*args, **kwargs)

        return wrapper

    return decorator


def query_fields(*, required: list[str] = [], optional: list[str] = []):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            args = request.args
            missing: list[str] = []

            for arg in required + optional:
                if arg in required and arg not in args:
                    missing.append(arg)
                    continue
                kwargs[arg] = args[arg]

            if len(missing) != 0:
                return MissingQueryParamsResponse.create(*missing)

            return f(*args, **kwargs)

        return wrapper

    return decorator
