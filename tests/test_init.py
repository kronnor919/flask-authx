from flask import Flask
from flask_authx import AuthXBuilder


def test_init(app: Flask):
    authx = AuthXBuilder(app).build()

    rules = [r.rule for r in app.url_map.iter_rules()]

    with app.app_context():
        admin_res = authx.users_repository.get_by_name("admin")  # pyright: ignore[reportOptionalMemberAccess]

    assert authx == app.extensions["authx"]
    assert "/users" in rules
    assert "/auth/login" in rules
    assert "/auth/logout" in rules
    assert admin_res.value is not None
