from fasthtml.common import *
from starlette.testclient import TestClient

app, rt = fast_app()
cli = TestClient(app)

@rt("/test-f")
def post(f: str):
    return Titled("Success", P(f"Value: {f}"))

def test_argument_f_collision():
    res = cli.post('/test-f', data={'f': 'hello'})
    assert res.status_code == 200
    assert 'Value: hello' in res.text

test_argument_f_collision()
