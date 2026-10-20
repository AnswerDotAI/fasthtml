from fasthtml.common import *
from starlette.testclient import TestClient
from typing import Annotated

app, rt = fast_app()
cli = TestClient(app)

@rt("/query")
def get(user_id: Annotated[str, Alias("user-id")]): return f"q:{user_id}"

@rt("/form", methods=["post"])
def post(user_id: Annotated[str, Alias("user-id")]): return f"f:{user_id}"

@rt("/path/{item_id}")
def get(item_id: Annotated[int, Alias("item_id")]): return f"p:{item_id}"

@rt("/header")
def get(x_api_key: Annotated[str, Alias("X-Api-Key")]): return f"h:{x_api_key}"

@rt("/cookie")
def get(req, session_id: Annotated[str, Alias("session-id")]): return f"c:{session_id}"

@rt("/int")
def get(count: Annotated[int, Alias("the-count")]): return f"i:{count + 1}"

@rt("/plain")
def get(user_id: str): return f"plain:{user_id}"

@rt("/missing")
def get(user_id: Annotated[str, Alias("user-id")]): return user_id

def test_query_alias(): assert cli.get('/query?user-id=abc').text == 'q:abc'
def test_form_alias(): assert cli.post('/form', data={'user-id': 'abc'}).text == 'f:abc'
def test_path_alias(): assert cli.get('/path/7').text == 'p:7'
def test_header_alias(): assert cli.get('/header', headers={'X-Api-Key': 'k1'}).text == 'h:k1'
def test_cookie_alias(): assert cli.get('/cookie', cookies={'session-id': 's1'}).text == 'c:s1'
def test_int_alias(): assert cli.get('/int?the-count=4').text == 'i:5'
def test_plain_unchanged(): assert cli.get('/plain?user_id=z').text == 'plain:z'
def test_snake_name_not_used_for_alias(): assert cli.get('/query?user_id=abc').status_code == 400
def test_missing_message_uses_alias():
    r = cli.get('/missing')
    assert r.status_code == 400 and 'Missing required field: user-id' in r.text
