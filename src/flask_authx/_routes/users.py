from typing import Optional
from flask import Blueprint, Flask, url_for

from flask_authx._entities import User
from flask_authx._forms import UserForm
from flask_authx._role import Role
from flask_authx._errors import (
    ConflictError,
    DatabaseError,
    NotFoundError,
    ValidationError,
)
from flask_authx._interfaces.repository import ISessionsRepository
from flask_authx._interfaces.service import IUsersService
from flask_authx._security.auth import require_authentication
from flask_authx._utils.request import json_fields
from flask_authx._utils.responses import (
    BadRequestFormatResponse,
    CreatedUserResponse,
    InternalErrorResponse,
    UserFormValidationErrorResponse,
    SuccessfulEmptyResponse,
    PermissionErrorResponse,
    UserInfoResponse,
    UserNotFoundResponse,
    UsernameConflictResponse,
    UsersListResponse,
)


class UsersRoutes:
    def __init__(
        self,
        users_service: IUsersService,
        sessions_repository: ISessionsRepository,
        *,
        prefix: str,
        app: Optional[Flask] = None,
    ) -> None:
        self.users_service = users_service
        self.sessions_repository = sessions_repository

        self._users_bp = Blueprint("users", __name__, url_prefix=prefix)
        self._require_authentication = require_authentication(self.sessions_repository)
        self._setup_routes()

        if app:
            self.init_routes(app)

    def init_routes(self, app: Flask):
        app.register_blueprint(self._users_bp)

    def _setup_routes(self):
        @self._users_bp.route("", methods=["GET"])
        def get_all():
            # Tested
            res = self.users_service.all()

            if not res.success:
                if res.error_is(DatabaseError):
                    return InternalErrorResponse.create(res.error.message)

            return UsersListResponse.create(res.value)

        @self._users_bp.route("/<int:id>", methods=["GET"])
        def get_by_id(id: int):
            # Tested
            res = self.users_service.get_by_id(id)

            if not res.success:
                if res.error_is(NotFoundError):
                    return UserNotFoundResponse.create(id=id)

                elif res.error_is(DatabaseError):
                    return InternalErrorResponse.create(res.error.message)

            return UserInfoResponse.create(res.value)

        @self._users_bp.route("/<string:username>", methods=["GET"])
        def get_by_username(username: str):
            # Tested
            res = self.users_service.get_by_name(username)

            if not res.success:
                if res.error_is(NotFoundError):
                    return UserNotFoundResponse.create(username=username)

                elif res.error_is(DatabaseError):
                    return InternalErrorResponse.create(res.error.message)

            return UserInfoResponse.create(res.value)

        @self._users_bp.route("/<int:id>", methods=["DELETE"])
        @self._require_authentication
        def delete(id: int, user: User):
            # Tested
            if user.id != id and user.role != Role.admin:
                return PermissionErrorResponse.create()

            session_res = self.sessions_repository.remove_by_user(id)

            if not session_res.success:
                if session_res.error_is(DatabaseError):
                    return InternalErrorResponse.create(session_res.error.message)

            res = self.users_service.remove(id)

            if not res.success:
                if res.error_is(NotFoundError):
                    return UserNotFoundResponse.create(id=id)

                elif res.error_is(DatabaseError):
                    return InternalErrorResponse.create(res.error.message)

            return SuccessfulEmptyResponse.create()

        @self._users_bp.route("", methods=["POST"])
        @json_fields(required=["username", "password", "role"])
        def post(username: str, password: str, role: str):
            # Tested
            if not Role.is_parseable(role):
                return BadRequestFormatResponse.create(
                    "The value of the field 'role' isn't valid."
                )

            form = UserForm(username, password, Role.parse(role))
            valid_res = form.is_valid()

            if not valid_res.success:
                return UserFormValidationErrorResponse.create(valid_res.error.message)

            res = self.users_service.add(form)
            user = res.value

            if not res.success:
                if res.error_is(ConflictError):
                    return UsernameConflictResponse.create()

                elif res.error_is(ValidationError):
                    return InternalErrorResponse.create(
                        f"Unhandled validation error: {res.error.message}"
                    )

                elif res.error_is(DatabaseError):
                    return InternalErrorResponse.create(res.error.message)

            url = url_for("users.get_by_id", _method="GET", _external=True, id=user.id)

            return CreatedUserResponse.create(res.value, url)
