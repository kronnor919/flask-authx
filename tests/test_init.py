from flask import Flask
from flask_authx import AuthX
from flask_authx import config


USERNAME = "kronnor"
PW = "73336463"


def test_init(builded_app: Flask):
    authx: AuthX = builded_app.extensions["authx"]

    rules = [r.rule for r in builded_app.url_map.iter_rules()]

    with builded_app.app_context():
        admin_res = authx.users_repository.get_by_name(USERNAME)  # pyright: ignore[reportOptionalMemberAccess]

    assert authx == builded_app.extensions["authx"]
    assert "/users" in rules
    assert "/auth/login" in rules
    assert "/auth/logout" in rules
    assert admin_res.value is not None


def test_config():
    assert config.FIRST_USER_NAME == USERNAME
    assert config.FIRST_USER_PASSWORD == PW


def test_first_user_exists(builded_app: Flask):
    authx: AuthX = builded_app.extensions["authx"]

    with builded_app.app_context():
        user_res = authx.users_repository.get_by_name(USERNAME)  # pyright: ignore[reportOptionalMemberAccess]

    assert user_res.success is True

    admin = user_res.value

    assert admin.username == USERNAME
    assert authx.password_hashing.verify(PW, admin.password)  # pyright: ignore[reportOptionalMemberAccess]
