from abc import ABC, abstractmethod
from typing import Any

from flask_authx.entities import Session, User
from flask_authx.forms import SessionForm, UserForm
from flask_authx.errors import (
    ConflictError,
    DatabaseError,
    NotFoundError,
    ValidationError,
)
from flask_authx.utils.result import Result


class IUsersRepository(ABC):
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
        self, new: UserForm
    ) -> Result[User, ConflictError | ValidationError | DatabaseError]:
        pass

    @abstractmethod
    def remove(self, id: int) -> Result[None, NotFoundError | DatabaseError]:
        pass

    @abstractmethod
    def update(
        self, id: int, values: dict[str, Any]
    ) -> Result[User, ConflictError | ValidationError | NotFoundError | DatabaseError]:
        pass


class ISessionsRepository(ABC):
    @abstractmethod
    def all(self) -> Result[list[Session], DatabaseError]:
        pass

    @abstractmethod
    def get_by_token(
        self, token: str
    ) -> Result[Session, NotFoundError | DatabaseError]:
        pass

    @abstractmethod
    def get_by_user(
        self, user_id: int
    ) -> Result[Session, NotFoundError | DatabaseError]:
        pass

    @abstractmethod
    def add(
        self, new: SessionForm
    ) -> Result[Session, ConflictError | ValidationError | DatabaseError]:
        pass

    @abstractmethod
    def remove(self, token: str) -> Result[None, NotFoundError | DatabaseError]:
        pass

    @abstractmethod
    def remove_by_user(
        self, user_id: int
    ) -> Result[None, NotFoundError | DatabaseError]:
        pass
