"""Regression test for #834: _handle() conflicts with form field named 'f'."""
from fasthtml.common import *
from starlette.testclient import TestClient

app, rt = fast_app()

@rt('/upload', methods=['POST'])
def upload(f: str):
    return f'Got: {f}'

@rt('/multi', methods=['POST'])
def multi(f: str, g: str):
    return f'{f},{g}'

cli = TestClient(app)

def test_form_field_named_f():
    """POST with form field 'f' must not crash with 'got multiple values for argument f'."""
    res = cli.post('/upload', data={'f': 'hello'})
    assert res.status_code == 200
    assert 'hello' in res.text

def test_form_field_named_f_with_others():
    """POST with form field 'f' alongside other fields."""
    res = cli.post('/multi', data={'f': 'a', 'g': 'b'})
    assert res.status_code == 200
    assert 'a,b' in res.text

test_form_field_named_f()
test_form_field_named_f_with_others()
