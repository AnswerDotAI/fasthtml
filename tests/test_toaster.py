from fasthtml.common import *
from starlette.testclient import TestClient

app, rt = fast_app()
setup_toasts(app)
cli = TestClient(app)

@rt("/set-toast-get")
def get(session):
    add_toast(session, "Toast get", "info")
    return RedirectResponse('/see-toast')

@rt("/set-toast-post")
def post(session):
    add_toast(session, "Toast post", "info")
    return RedirectResponse('/see-toast')

@rt("/see-toast")
def get(session):
    return Titled("Hello, world!", P(str(session)))

@rt("/see-toast-with-typehint")
def get(session: dict):
    return Titled("Hello, world!", P(str(session)))

@rt("/see-toast-ft-response")
def get(session):
    add_toast(session, "Toast FtResponse", "info")
    return FtResponse(Titled("Hello, world!", P(str(session))))

def test_get_toaster():
    cli.get('/set-toast-get', follow_redirects=False)
    res = cli.get('/see-toast')
    assert 'Toast get' in res.text

    res = cli.get('/set-toast-get', follow_redirects=True)
    assert 'Toast get' in res.text

def test_post_toaster():
    cli.post('/set-toast-post', follow_redirects=False)
    res = cli.get('/see-toast')
    assert 'Toast post' in res.text

def test_ft_response():
    res = cli.get('/see-toast-ft-response')
    assert 'Toast FtResponse' in res.text

def test_get_toaster_with_typehint():
    res = cli.get('/see-toast-with-typehint', follow_redirects=False)
    assert 'Toast get' in res.text

    res = cli.get('/see-toast-with-typehint', follow_redirects=True)
    assert 'Toast get' in res.text

def test_toast_container_in_response():
    # toasts will not render correctly if the toast container isn't rendered.
    res = cli.get('/see-toast-ft-response')
    assert 'id="fh-toast-container"' in res.text

test_get_toaster()
test_post_toaster()
test_ft_response()
test_toast_container_in_response()
