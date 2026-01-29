from typing import Optional
from flask import Blueprint, Flask

from flask_authx.domain.entities import User
from flask_authx.domain.forms import UserForm
from flask_authx.domain.value_objects import Role
from flask_authx.domain.errors import (
    ConflictError,
    InvalidCredentialsError,
    NotAuthenticatedError,
)
from flask_authx.interfaces.repository import ISessionsRepository
from flask_authx.interfaces.service import IAuthService
from flask_authx.security.auth import require_authentication
from flask_authx.utils.request import json_fields
from flask_authx.utils.responses import (
    InternalErrorResponse,
    InvalidCredentialsResponse,
    RequireAuthenticationResponse,
    SessionAlreadyOpenResponse,
    SuccessfulEmptyResponse,
    SuccessfulLoginResponse,
)


class AuthRoutes:
    def __init__(
        self,
        auth_service: IAuthService,
        sessions_repository: ISessionsRepository,
        *,
        prefix: str,
        app: Optional[Flask] = None,
    ) -> None:
        self.auth_svc = auth_service
        self.sessions_repository = sessions_repository

        self._auth_bp = Blueprint("auth", __name__, url_prefix=prefix)
        self._require_authentication = require_authentication(self.sessions_repository)
        self._setup_routes()

        if app:
            self.init_routes(app)

    def init_routes(self, app: Flask):
        app.register_blueprint(self._auth_bp)

    def _setup_routes(self):
        @self._auth_bp.route("/login", methods=["POST"])
        @json_fields(required=["username", "password"])
        def login(username: str, password: str):
            # Tested
            form = UserForm(username, password, Role.unauth)
            login_res = self.auth_svc.login(form)

            if not login_res.success:
                if login_res.error_is(InvalidCredentialsError):
                    return InvalidCredentialsResponse.create()

                elif login_res.error_is(ConflictError):
                    return SessionAlreadyOpenResponse.create()

                else:
                    return InternalErrorResponse.create(login_res.error.message)

            sess = login_res.value

            return SuccessfulLoginResponse.create(sess)

        @self._auth_bp.route("/logout", methods=["DELETE"])
        @self._require_authentication
        def logout(user: User):
            # Tested
            logout_res = self.auth_svc.logout(user)

            if not logout_res.success:
                if logout_res.error_is(NotAuthenticatedError):
                    return RequireAuthenticationResponse.create()

                else:
                    return InternalErrorResponse.create(logout_res.error.message)

            return SuccessfulEmptyResponse.create()
