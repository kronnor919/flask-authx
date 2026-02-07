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

from flask_authx.entities import Session, User
from flask_authx.forms import SessionForm, UserForm
from flask_authx.role import Role


def create_models(db):
    """Create models dynamically using the provided SQLAlchemy instance."""

    class UserModel(db.Model):
        __tablename__ = "Users"

        id = Column(Integer, primary_key=True, autoincrement=True)
        username = Column(String(150), nullable=False, unique=True)
        password_hash = Column(String, nullable=False)
        is_authenticated = Column(Boolean, nullable=False)
        role = Column(Enum(Role), nullable=False)
        created_at = Column(DateTime, default=datetime.now)

        session = relationship(
            "SessionModel",
            uselist=False,
            back_populates="user",
            cascade="all, delete-orphan",
        )

        def to_entity(self) -> User:
            return User(
                self.id,
                self.username,
                self.password_hash,
                self.role,
                self.is_authenticated,
                self.created_at,
            )

        @staticmethod
        def create(u: UserForm):
            return UserModel(
                username=u.username,
                password_hash=u.password,
                role=u.role,
                is_authenticated=False,
            )

    class SessionModel(db.Model):
        __tablename__ = "Sessions"

        token = Column(String, primary_key=True, nullable=False)
        user_id = Column(Integer, ForeignKey("Users.id"), unique=True)
        created_at = Column(DateTime, default=datetime.now)

        user = relationship(UserModel, uselist=False, back_populates="session")

        def to_entity(self) -> Session:
            return Session(self.token, self.user, self.created_at)

        @staticmethod
        def create(s: SessionForm):
            return SessionModel(token=s.token, user_id=s.user.id)

    return UserModel, SessionModel


# Cache for dynamically created models
_cached = {}


def get_user_model():
    from flask_authx.database.sqlalchemy.shared.instance import get_instance

    db = get_instance()
    if id(db) not in _cached:
        _cached[id(db)] = create_models(db)
    return _cached[id(db)][0]


def get_session_model():
    from flask_authx.database.sqlalchemy.shared.instance import get_instance

    db = get_instance()
    if id(db) not in _cached:
        _cached[id(db)] = create_models(db)
    return _cached[id(db)][1]


# For backward compatibility - will be replaced at runtime
UserModel = None
SessionModel = None
