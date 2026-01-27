from datetime import datetime
from sqlalchemy import (
    Boolean,
    Column,
    Enum,
    ForeignKey,
    Integer,
    String,
    DateTime,
)
from sqlalchemy.orm import relationship

from flask_authx.database.sqlalchemy.shared.instance import instance
from flask_authx.domain.entities import Session, User
from flask_authx.domain.forms import SessionForm, UserForm
from flask_authx.domain.value_objects import Role
from flask_authx.container import container


class UserModel(instance.Model):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(150), nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    is_authenticated = Column(Boolean, nullable=False)
    role = Column(Enum(Role), nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    session = relationship("SessionModel", uselist=False, back_populates="user")

    def to_entity(self) -> User:
        return User(
            self.id,  # type: ignore
            self.username,  # type: ignore
            self.password_hash,  # type: ignore
            self.role,  # type: ignore
            self.is_authenticated,  # type: ignore
            self.created_at,  # type: ignore
        )

    @staticmethod
    def create(u: UserForm) -> "UserModel":
        return UserModel(
            username=u.username,  # type: ignore
            password_hash=container.password_hashing.hash(u.password),  # type: ignore
            role=u.role,  # type: ignore
            is_authenticated=False,  # type: ignore
        )


class SessionModel(instance.Model):
    __tablename__ = "Sessions"

    token = Column(String, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("Users.id"), unique=True)
    created_at = Column(DateTime, default=datetime.now)

    user = relationship(UserModel, uselist=False, back_populates="session")

    def to_entity(self) -> Session:
        return Session(self.token, self.user, self.created_at)  # type: ignore

    @staticmethod
    def create(s: SessionForm) -> "SessionModel":
        return SessionModel(token=s.token, user_id=s.user.id)  # type: ignore
