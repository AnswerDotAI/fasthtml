from fasthtml.common import *
from starlette.testclient import TestClient

app, rt = fast_app()
setup_toasts(app)
cli = TestClient(app)

@rt("/set-toast-get")
def get(request, session):
    add_toast(session, "Toast get", "info")
    return RedirectResponse('/see-toast')

@rt("/set-toast-post")
def post(request, session):
    add_toast(session, "Toast post", "info")
    return RedirectResponse('/see-toast')

@rt("/see-toast")
def get(request, session):
    return Titled("Hello, world!", P(str(session)))

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
