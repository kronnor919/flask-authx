from abc import ABC, abstractmethod

from flask_authx._entities import Session, User
from flask_authx._role import Role
from flask_authx._forms import UserForm
from flask_authx._errors import (
    ConflictError,
    InvalidCredentialsError,
    NotAuthenticatedError,
    DatabaseError,
    NotFoundError,
    ValidationError,
)
from flask_authx._utils.result import Result


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


class IUsersService(ABC):
    @abstractmethod
    def all(self) -> Result[list[User], DatabaseError]:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Result[User, NotFoundError | DatabaseError]:
        pass

    @abstractmethod
    def get_by_name(self, username: str) -> Result[User, NotFoundError | DatabaseError]:
        pass

    @abstractmethod
    def add(
        self, form: UserForm
    ) -> Result[User, ConflictError | ValidationError | DatabaseError]:
        pass

    @abstractmethod
    def remove(self, id: int) -> Result[None, NotFoundError | DatabaseError]:
        pass

    @abstractmethod
    def update_name(
        self, id: int, new_username: str
    ) -> Result[User, ValidationError | NotFoundError | ConflictError | DatabaseError]:
        pass

    @abstractmethod
    def update_role(
        self, id: int, role: Role
    ) -> Result[User, NotFoundError | DatabaseError]:
        pass

    @abstractmethod
    def mark_authenticated(
        self, id: int
    ) -> Result[User, NotFoundError | DatabaseError]:
        pass

    @abstractmethod
    def mark_unauthenticated(
        self, id: int
    ) -> Result[User, NotFoundError | DatabaseError]:
        pass

    @abstractmethod
    def is_authenticated(self, id: int) -> Result[bool, NotFoundError | DatabaseError]:
        pass
