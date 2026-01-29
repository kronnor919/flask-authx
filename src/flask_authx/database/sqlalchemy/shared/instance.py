from flask import Flask
from flask_sqlalchemy import SQLAlchemy


instance: SQLAlchemy = None  # pyright: ignore[reportAssignmentType]


def set_sqlalchemy(app: Flask):
    sa = ensure_sqlalchemy(app)
    global instance
    instance = sa


def ensure_sqlalchemy(app: Flask) -> SQLAlchemy:
    if not app.extensions.get("sqlalchemy"):
        raise RuntimeError(
            "App must have initialized 'SQLAlchemy' instance, from `Flask-SQLAlchemy` extension. Or define your own database configuration via `AuthXBuilder`."
        )
    return app.extensions["sqlalchemy"]
