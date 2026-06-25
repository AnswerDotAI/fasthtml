from fasthtml.common import fast_app
from starlette.testclient import TestClient

def test_fast_app_static_ext_route_does_not_shadow_post():
    app, rt = fast_app()

    @rt("/x/{a}/{path:path}", methods=["GET", "POST", "PUT"])
    async def catchall(a: str, path: str, request):
        return {"matched": True, "a": a, "path": path, "method": request.method}

    client = TestClient(app)

    # Assert that POST requests ending in static extensions hit the dynamic endpoint instead of throwing a 404
    assert client.post("/x/SID/file.xls").status_code == 200
    assert client.post("/x/SID/sub/file.xlsx").status_code == 200
