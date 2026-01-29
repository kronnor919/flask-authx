import pytest
from flask import Flask
from flask_authx import AuthXBuilder


USERNAME = "kronnor"
PW = "73336463"


@pytest.fixture(scope="module")
def builded_app(app: Flask):
    app_copy = app

    app_copy.config.from_mapping(
        {"FIRST_USER_NAME": USERNAME, "FIRST_USER_PASSWORD": PW}
    )

    AuthXBuilder(app_copy).build()

    yield app_copy


def test_init(builded_app: Flask):
    authx = builded_app.extensions["authx"]

    rules = [r.rule for r in builded_app.url_map.iter_rules()]

    with builded_app.app_context():
        admin_res = authx.users_repository.get_by_name(USERNAME)  # pyright: ignore[reportOptionalMemberAccess]

    assert authx == builded_app.extensions["authx"]
    assert "/users" in rules
    assert "/auth/login" in rules
    assert "/auth/logout" in rules
    assert admin_res.value is not None
