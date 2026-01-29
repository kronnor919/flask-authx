from enum import Enum

from flask_authx.errors import ProgrammingError


class Role(Enum):
    user = "user"
    """
    Authenticated user
    """

    admin = "admin"
    """
    Admin account
    """

    dev = "dev"
    """
    Developer account
    """

    unauth = "unauth"
    """
    Unauthenticated user
    """

    @staticmethod
    def parse(s: str) -> "Role":
        if not Role.is_parseable(s):
            raise ProgrammingError(f"Option '{s}' is not a member of the role enum.")

        val = getattr(Role, s)

        return val

    @staticmethod
    def is_parseable(s: str) -> bool:
        return hasattr(Role, s)

    def dump(self) -> str:
        return self.value
