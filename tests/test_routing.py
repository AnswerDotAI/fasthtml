import pytest

from fasthtml.core import FastHTML


def _app():
    return FastHTML(secret_key="synthetic-test-only", sess_cls=None)


def test_default_route_rejects_overlapping_sibling_method():
    app = _app()
    app.route("/shared")(lambda req: "default")

    with pytest.raises(ValueError, match="POST"):
        app.post("/shared")(lambda req: "post")


def test_explicit_disjoint_methods_can_share_path():
    app = _app()
    app.get("/shared", name="shared_get")(lambda req: "get")
    app.post("/shared", name="shared_post")(lambda req: "post")

    assert [route.name for route in app.router.routes if route.path == "/shared"] == [
        "shared_get",
        "shared_post",
    ]


def test_same_name_and_methods_replace_existing_route():
    app = _app()
    app.get("/shared", name="shared")(lambda req: "first")
    app.get("/shared", name="shared")(lambda req: "replacement")

    assert len([route for route in app.router.routes if route.path == "/shared"]) == 1
