from __future__ import annotations

import base64
from typing import TYPE_CHECKING, Any

from webob.exc import HTTPForbidden, HTTPProxyAuthenticationRequired
from webtest import TestApp as Client

import morepath
from more.basicauth import BasicAuthIdentityPolicy
from morepath import NO_IDENTITY, Identity, Response

if TYPE_CHECKING:
    from morepath import Request
    from morepath.authentication import NoIdentity


def test_basic_auth_identity_policy() -> None:
    class App(morepath.App):
        pass

    class Model:
        def __init__(self, id: str) -> None:
            self.id = id

    class Permission:
        pass

    @App.path(model=Model, path="{id}", variables=lambda model: {"id": model.id})
    def get_model(id: str) -> Model:
        return Model(id)

    @App.permission_rule(model=Model, permission=Permission)
    def get_permission(
        identity: Identity, model: Model, permission: Permission
    ) -> bool:
        return bool(identity.userid == "user" and identity.password == "secret")

    @App.view(model=Model, permission=Permission)
    def default(self: Model, request: Request[App]) -> str:
        return f"Model: {self.id}"

    @App.identity_policy()
    def policy() -> BasicAuthIdentityPolicy:
        return BasicAuthIdentityPolicy()

    @App.verify_identity()
    def verify_identity(identity: Identity | NoIdentity) -> bool:
        assert identity is not NO_IDENTITY
        return True

    @App.view(model=HTTPForbidden)
    def make_unauthorized(self: HTTPForbidden, request: Request[App]) -> str:
        @request.after
        def set_status_code(response: Response) -> None:
            response.status_code = 401

        return "Unauthorized"

    c = Client(App())

    response = c.get("/foo", status=401)

    headers = {
        "Authorization": "Basic " + str(base64.b64encode(b"user:wrong").decode())
    }
    response = c.get("/foo", headers=headers, status=401)

    headers = {
        "Authorization": "Basic " + str(base64.b64encode(b"user:secret").decode())
    }
    response = c.get("/foo", headers=headers)
    assert response.body == b"Model: foo"


def test_basic_auth_identity_policy_errors() -> None:
    class App(morepath.App):
        pass

    class Model:
        def __init__(self, id: str) -> None:
            self.id = id

    class Permission:
        pass

    @App.path(model=Model, path="{id}", variables=lambda model: {"id": model.id})
    def get_model(id: str) -> Model:
        return Model(id)

    @App.permission_rule(model=Model, permission=Permission)
    def get_permission(
        identity: Identity,
        model: Model,
        permission: Permission,
    ) -> bool:
        return bool(identity.userid == "user" and identity.password == "sëcret")

    @App.view(model=Model, permission=Permission)
    def default(self: Model, request: Request[App]) -> str:
        return f"Model: {self.id}"

    @App.identity_policy()
    def policy() -> BasicAuthIdentityPolicy:
        return BasicAuthIdentityPolicy()

    @App.verify_identity()
    def verify_identity(identity: Identity | NoIdentity) -> bool:
        return True

    c = Client(App())

    response = c.get("/foo", status=403)

    headers = {"Authorization": "Something"}
    response = c.get("/foo", headers=headers, status=403)

    headers = {"Authorization": "Something other"}
    response = c.get("/foo", headers=headers, status=403)

    headers = {"Authorization": "Basic " + "nonsense"}
    response = c.get("/foo", headers=headers, status=403)

    headers = {"Authorization": "Basic " + "nonsense1"}
    response = c.get("/foo", headers=headers, status=403)

    # fallback to utf8
    headers = {
        "Authorization": "Basic "
        + str(base64.b64encode("user:sëcret".encode()).decode())
    }
    response = c.get("/foo", headers=headers)
    assert response.body == b"Model: foo"

    # fallback to latin1
    headers = {
        "Authorization": "Basic "
        + str(base64.b64encode("user:sëcret".encode("latin1")).decode())
    }
    response = c.get("/foo", headers=headers)
    assert response.body == b"Model: foo"

    # unknown encoding
    headers = {
        "Authorization": "Basic "
        + str(base64.b64encode("user:sëcret".encode("cp500")).decode())
    }
    response = c.get("/foo", headers=headers, status=403)

    headers = {
        "Authorization": "Basic "
        + str(base64.b64encode("usersëcret".encode()).decode())
    }
    response = c.get("/foo", headers=headers, status=403)

    headers = {
        "Authorization": "Basic "
        + str(base64.b64encode("user:sëcret:".encode()).decode())
    }
    response = c.get("/foo", headers=headers, status=403)


def test_basic_auth_remember() -> None:
    class App(morepath.App):
        pass

    @App.path(path="{id}", variables=lambda model: {"id": model.id})
    class Model:
        def __init__(self, id: str) -> None:
            self.id = id

    @App.view(model=Model)
    def default(self: Model, request: Request[App]) -> Response:
        # will not actually do anything as it's a no-op for basic
        # auth, but at least won't crash
        response = Response()
        request.app.remember_identity(response, request, Identity("foo"))
        return response

    @App.identity_policy()
    def policy() -> BasicAuthIdentityPolicy:
        return BasicAuthIdentityPolicy()

    c = Client(App())

    response = c.get("/foo", status=200)
    assert response.body == b""


def test_basic_auth_forget() -> None:
    class App(morepath.App):
        pass

    @App.path(path="{id}")
    class Model:
        def __init__(self, id: str) -> None:
            self.id = id

    @App.view(model=Model)
    def default(self: Model, request: Request[App]) -> Response:
        # will not actually do anything as it's a no-op for basic
        # auth, but at least won't crash
        response = Response(content_type="text/plain")
        request.app.forget_identity(response, request)
        return response

    @App.identity_policy()
    def policy() -> BasicAuthIdentityPolicy:
        return BasicAuthIdentityPolicy()

    c = Client(App())

    response = c.get("/foo", status=200)
    assert response.body == b""

    assert sorted(response.headers.items()) == [
        ("Content-Length", "0"),
        ("Content-Type", "text/plain; charset=UTF-8"),
        ("WWW-Authenticate", 'Basic realm="Realm"'),
    ]


def test_login() -> None:
    class App(morepath.App):
        pass

    @App.identity_policy()
    def get_identity_policy() -> BasicAuthIdentityPolicy:
        return BasicAuthIdentityPolicy()

    class Login:
        pass

    @App.path(model=Login, path="login")
    def get_login() -> Login:
        return Login()

    @App.json(model=Login, request_method="POST")
    def login(self: Login, request: Request[App]) -> dict[str, Any]:
        username = request.POST.get("username")
        password = request.POST.get("password")
        if not user_has_password(username, password):
            raise HTTPProxyAuthenticationRequired("Invalid username/password")

        return {
            "username": username,
        }

    def user_has_password(username: object, password: object) -> bool:
        return username == "user" and password == "password"

    c = Client(App())
    r = c.post("/login", "username=user&password=false", status=407)
    r = c.post("/login", "username=not_exists&password=password", status=407)
    r = c.post("/login", "username=user&password=password")

    assert r.json == {
        "username": "user",
    }
