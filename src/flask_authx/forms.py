from dataclasses import dataclass
from typing import TypedDict

from flask_authx.entities import User
from flask_authx.errors import ValidationError
from flask_authx.role import Role
from flask_authx.utils.result import Result


@dataclass(frozen=True)
class UserForm:
    username: str
    password: str
    role: Role

    def is_valid(self) -> Result[None, ValidationError]:
        rules = [
            User.validate_username(self.username),
            User.validate_password(self.password),
        ]

        for r in rules:
            if not r.success:
                return r

        return Result.ok(None)


@dataclass
class SessionForm:
    token: str
    user: User


class UserUpdateData(TypedDict, total=False):
    username: str
    role: Role
    is_authenticated: bool
