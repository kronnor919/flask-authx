from dataclasses import dataclass

from flask_authx.domain.entities import User
from flask_authx.domain.errors import ValidationError
from flask_authx.domain.value_objects import Role
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
