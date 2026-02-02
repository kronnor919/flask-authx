import json
from http import HTTPStatus
from typing import Any
from flask import Flask
from flask.testing import FlaskClient
from flask_authx.errors import NotFoundError
from flask_authx.forms import UserForm
from flask_authx.role import Role


def test_get_users(app_client: FlaskClient):
    res = app_client.get("/users")
    json: dict[str, Any] = res.get_json()

    users: list[dict] | None = json.get("users")

    assert res.status_code == HTTPStatus.OK
    assert json.get("success") is True
    assert isinstance(users, list)
    assert len(users) >= 1


def test_get_user_by_id(app_client: FlaskClient):
    res = app_client.get("/users/1")
    json: dict[str, Any] = res.get_json()
    user = json.get("user")

    assert res.status_code == HTTPStatus.OK
    assert user is not None
    assert user != {}
    assert user.get("username") == "kronnor"
    assert user.get("role") == "admin"


def test_user_by_name(app_client: FlaskClient):
    res = app_client.get("/users/kronnor")
    user = res.get_json().get("user")

    assert res.status_code == HTTPStatus.OK
    assert user is not None
    assert user != {}
    assert user.get("username") == "kronnor"
    assert user.get("role") == "admin"


def test_post_user(app_client: FlaskClient, builded_app: Flask):
    res = app_client.post(
        "/users",
        data=json.dumps({"username": "user1", "password": "894728374", "role": "user"}),
        content_type="application/json",
    )

    data: dict = res.get_json()
    user_data = data["user"]

    assert res.status_code == HTTPStatus.CREATED
    assert user_data is not None
    assert user_data["username"] == "user1"
    assert user_data["role"] == "user"

    with builded_app.app_context():
        rem_res = builded_app.extensions["authx"].users_service.remove(user_data["id"])

    assert rem_res.success is True


def test_delete_user(app_client: FlaskClient, builded_app: Flask):
    user = UserForm("Steve", "14/11/10", Role.unauth)

    with builded_app.app_context():
        add_res = builded_app.extensions["authx"].users_service.add(user)

        assert add_res.success

        login_res = builded_app.extensions["authx"].auth_service.login(user)

        assert login_res.success

        del_res = app_client.delete(
            f"/users/{add_res.value.id}",
            headers={"Authorization": f"Bearer {login_res.value.token}"},
        )

        assert del_res.status_code == HTTPStatus.OK

        with builded_app.app_context():
            exists_res = builded_app.extensions["authx"].users_service.get_by_name(
                "Steve"
            )

        assert not exists_res.success
        assert exists_res.error_is(NotFoundError)
