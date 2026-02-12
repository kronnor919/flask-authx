from flask import Config
from flask_authx._errors import ConfigurationError


FIRST_USER_NAME: str
FIRST_USER_PASSWORD: str


def load_config(app_config: Config):
    global FIRST_USER_NAME, FIRST_USER_PASSWORD

    try:
        FIRST_USER_NAME = app_config["FIRST_USER_NAME"]
        FIRST_USER_PASSWORD = app_config["FIRST_USER_PASSWORD"]

    except KeyError as field:
        raise ConfigurationError(f"Missing field in app config: {field}")
