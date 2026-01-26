from http import HTTPStatus
from typing import Optional

from flask import make_response

from flask_authx.domain.entities import Session, User


class UserNotFoundResponse:
    @staticmethod
    def create(*, id: Optional[int] = None, username: Optional[str] = None):
        if id is not None:
            message = f"User with id {id} not found."
        elif username is not None:
            message = f"User with username: {username} not found."
        else:
            message = "User not found."

        res = make_response({"success": False, "error": message})
        res.status_code = HTTPStatus.NOT_FOUND
        return res


class InternalErrorResponse:
    @staticmethod
    def create(message: str):
        res = make_response({"success": False, "error": message})
        res.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        return res


class UserInfoResponse:
    @staticmethod
    def create(user: User):
        res = make_response({
            "success": True,
            "user": {
                "id": user.id,
                "username": user.username,
                "role": user.role.dump(),
                "is_authenticated": user.is_authenticated,
                "created_at": user.created_at.isoformat(),
            },
        })
        res.status_code = HTTPStatus.OK
        return res


class UsersListResponse:
    @staticmethod
    def create(users: list[User]):
        res = make_response({
            "success": True,
            "users": [
                {"id": u.id, "username": u.username, "role": u.role.dump()}
                for u in users
            ],
        })
        res.status_code = HTTPStatus.OK
        return res


class SuccessfulEmptyResponse:
    @staticmethod
    def create():
        res = make_response({"success": True})
        res.status_code = HTTPStatus.OK
        return res


class JSONRequiredResponse:
    @staticmethod
    def create():
        res = make_response({
            "success": False,
            "error": "MimeType must be 'application/json'",
        })
        res.status_code = HTTPStatus.UNSUPPORTED_MEDIA_TYPE
        return res


class MissingJsonFieldsResponse:
    @staticmethod
    def create(*fields: str):
        res = make_response({
            "success": False,
            "error": f"Missing fields in JSON body: {', '.join([f"'{f}'" for f in fields])}",
        })
        res.status_code = HTTPStatus.BAD_REQUEST
        return res


class CreatedUserResponse:
    @staticmethod
    def create(user: User, location: str):
        res = make_response(UserInfoResponse.create(user))
        res.status_code = HTTPStatus.CREATED
        res.headers.set("Location", location)
        return res


class BadRequestFormatResponse:
    @staticmethod
    def create(message: str):
        res = make_response({"success": False, "error": message})
        res.status_code = HTTPStatus.BAD_REQUEST
        return res


class UsernameConflictResponse:
    @staticmethod
    def create():
        res = make_response({
            "success": False,
            "error": "That username is already taken.",
        })
        res.status_code = HTTPStatus.CONFLICT
        return res


class UserFormValidationErrorResponse:
    @staticmethod
    def create(message: Optional[str] = None):
        res = make_response({
            "success": False,
            "error": message or "Invalid credentials.",
        })
        res.status_code = HTTPStatus.BAD_REQUEST
        return res


class RequireAuthenticationResponse:
    @staticmethod
    def create():
        res = make_response({
            "success": False,
            "error": "The requested action requires authentication.",
        })
        res.status_code = HTTPStatus.UNAUTHORIZED
        return res


class MissingQueryParamsResponse:
    @staticmethod
    def create(*fields: str):
        res = make_response({
            "success": False,
            "error": f"Missing params in query string: {', '.join([f"'{f}'" for f in fields])}",
        })
        res.status_code = HTTPStatus.BAD_REQUEST
        return res


class PermissionErrorResponse:
    @staticmethod
    def create():
        res = make_response({
            "success": False,
            "error": "Your account doesn't have the required permission to proceed with the requested action.",
        })
        res.status_code = HTTPStatus.FORBIDDEN
        return res


class InvalidCredentialsResponse:
    @staticmethod
    def create():
        res = make_response({
            "success": False,
            "error": "Invalid username or password.",
        })
        res.status_code = HTTPStatus.UNAUTHORIZED
        return res


class SessionAlreadyOpenResponse:
    @staticmethod
    def create():
        res = make_response({
            "success": False,
            "error": "Session already open on another device. Please log out from there first.",
        })
        res.status_code = HTTPStatus.UNAUTHORIZED
        return res


class SuccessfulLoginResponse:
    @staticmethod
    def create(session: Session):
        res = make_response({"success": True, "access_token": session.token})
        res.status_code = HTTPStatus.OK
        return res
