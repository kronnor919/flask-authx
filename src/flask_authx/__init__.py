"""
Flask-AuthX provides a complete user session management system, with authentication, password hashing,
a pre-configured database, and automatically creates ready-to-use endpoints for any client.

## Basic usage

```py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_authx import AuthXBuilder

def create_app() -> Flask:
    app = Flask(__name__)

    app.config.from_mapping({
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "FIRST_USER_NAME": "kronnor",
        "FIRST_USER_PASSWORD": "73336463"
    })
    # You could also load configuration from an environment file (.env)

    SQLAlchemy(app) # Required by flask-authx by default

    AuthXBuilder(app).build()

    return app
```
"""

from flask_authx._extension import AuthX as AuthX
from flask_authx._extension import AuthXBuilder as AuthXBuilder
from flask_authx._interfaces.database import IDatabaseSetup as IDatabaseSetup
from flask_authx._interfaces.repository import (
    ISessionsRepository as ISessionsRepository,
)
from flask_authx._interfaces.repository import IUsersRepository as IUsersRepository
from flask_authx._interfaces.security import IPasswordHashing as IPasswordHashing
from flask_authx._interfaces.service import IAuthService as IAuthService
from flask_authx._interfaces.service import IUsersService as IUsersService
from flask_authx._entities import User as User
from flask_authx._entities import Session as Session
from flask_authx._forms import UserForm as UserForm
from flask_authx._forms import UserUpdateData as UserUpdateData
from flask_authx._forms import SessionForm as SessionForm
from flask_authx._role import Role as Role
from flask_authx._utils import responses as responses
from flask_authx._errors import ProgrammingError as ProgrammingError
from flask_authx._errors import AppError as AppError
from flask_authx._errors import ConfigurationError as ConfigurationError
from flask_authx._errors import NotFoundError as NotFoundError
from flask_authx._errors import ValidationError as ValidationError
from flask_authx._errors import DatabaseError as DatabaseError
from flask_authx._errors import ConflictError as ConflictError
from flask_authx._errors import DependentResourceError as DependentResourceError
from flask_authx._errors import NotAuthenticatedError as NotAuthenticatedError
from flask_authx._errors import InvalidCredentialsError as InvalidCredentialsError
from flask_authx import config as config


__all__ = [
    "AuthX",
    "AuthXBuilder",
    "IDatabaseSetup",
    "ISessionsRepository",
    "IUsersRepository",
    "IAuthService",
    "IPasswordHashing",
    "IUsersService",
    "User",
    "Session",
    "UserForm",
    "UserUpdateData",
    "SessionForm",
    "Role",
    "responses",
    "ProgrammingError",
    "AppError",
    "ConfigurationError",
    "NotFoundError",
    "ValidationError",
    "DatabaseError",
    "ConflictError",
    "DependentResourceError",
    "NotAuthenticatedError",
    "InvalidCredentialsError",
    "config",
]
