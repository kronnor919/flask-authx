from abc import ABC, abstractmethod

from flask_authx.entities import Session, User
from flask_authx.forms import UserForm
from flask_authx.errors import (
    ConflictError,
    InvalidCredentialsError,
    NotAuthenticatedError,
    DatabaseError,
)
from flask_authx.utils.result import Result


class IAuthService(ABC):
    @abstractmethod
    def login(
        self, u: UserForm
    ) -> Result[
        Session,
        InvalidCredentialsError | ConflictError | DatabaseError,
    ]:
        pass

    @abstractmethod
    def logout(self, user: User) -> Result[None, NotAuthenticatedError | DatabaseError]:
        pass
