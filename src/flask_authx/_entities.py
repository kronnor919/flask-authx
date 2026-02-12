from dataclasses import dataclass
from datetime import datetime

from flask_authx._errors import ValidationError
from flask_authx._role import Role
from flask_authx._utils.result import Result


@dataclass
class User:
    id: int
    username: str
    password: str
    """
    Plain or hashed password.
    """

    role: Role
    is_authenticated: bool
    created_at: datetime

    @classmethod
    def validate_username(cls, username: str) -> Result[None, ValidationError]:
        if len(username) < 3:
            return Result.fail(
                ValidationError("Username must contains at least 3 characters.")
            )
        return Result.ok(None)

    @classmethod
    def validate_password(cls, password: str) -> Result[None, ValidationError]:
        if len(password) < 8:
            return Result.fail(
                ValidationError("Password must contains at least 8 characters.")
            )
        return Result.ok(None)


@dataclass
class Session:
    token: str
    user: User
    created_at: datetime
