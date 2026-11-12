from fasthtml.common import *
from starlette.testclient import TestClient
import httpx2, socket, uvicorn
from fasthtml.proxy import ProxyResponse, proxy_headers, proxy_websocket
from contextlib import contextmanager
from threading import Thread
from starlette.applications import Starlette
from starlette.routing import Route, WebSocketRoute
from starlette.responses import StreamingResponse


app, rt = fast_app()
setup_toasts(app)

@rt("/set-toast-get")
def get(session):
    add_toast(session, "Toast get", "info")
    return RedirectResponse('/see-toast')

@rt("/set-toast-post")
def post(session):
    add_toast(session, "Toast post", "info")
    return RedirectResponse('/see-toast')

@rt("/see-toast")
def get(session): return Titled("Hello, world!")

@rt("/see-toast-with-typehint")
def get(session: dict): return Titled("Hello, world!")

@rt("/see-toast-ft-response")
def get(session):
    add_toast(session, "Toast FtResponse", "info")
    return FtResponse(Titled("Hello, world!"))

def test_toasts():
    with TestClient(app) as cli:
        cli.get('/set-toast-get', follow_redirects=False)
        assert 'Toast get' in cli.get('/see-toast-with-typehint').text
        assert 'Toast get' not in cli.get('/see-toast').text
        cli.post('/set-toast-post', follow_redirects=False)
        assert 'Toast post' in cli.get('/see-toast').text
        res = cli.get('/see-toast-ft-response')
        assert 'Toast FtResponse' in res.text
        assert 'id="fh-toast-container"' in res.text

@contextmanager
def running_server(app):
    with socket.create_server(('127.0.0.1', 0)) as sock:
        server = uvicorn.Server(uvicorn.Config(app, port=0, log_level='error'))
        thread = Thread(target=server.run, kwargs=dict(sockets=[sock]), daemon=True)
        thread.start()
        url = f'http://127.0.0.1:{sock.getsockname()[1]}'
        try:
            httpx2.get(url, timeout=5).raise_for_status()
            yield url
        finally:
            server.should_exit = True
            thread.join(5)
            assert not thread.is_alive()

async def echo_http(request):
    body = await request.body()
    response = StreamingResponse(iter([body[:1], body[1:]]), status_code=201, headers={
        'content-type': request.headers.get('content-type', 'application/octet-stream'),
        'x-query': request.url.query, 'x-method': request.method,
        'x-private': request.headers.get('x-private', ''), 'x-auth': request.headers.get('authorization', '')})
    response.raw_headers += [(b'x-tag', value.encode()) for value in request.headers.getlist('x-tag')]
    return response

async def echo_ws(ws):
    if status := ws.query_params.get('deny'): return await ws.send_denial_response(Response(status_code=int(status)))
    await ws.accept(subprotocol='echo')
    await ws.send_text(await ws.receive_text())
    await ws.send_bytes(await ws.receive_bytes())
    await ws.close(code=1000)

def test_proxy():
    upstream = Starlette(routes=[Route('/', echo_http, methods=['GET', 'PATCH']), WebSocketRoute('/ws', echo_ws)])
    with running_server(upstream) as url:
        async def forward_http(request):
            return ProxyResponse(request, url, headers=proxy_headers(request.headers, exclude=(b'authorization',)))
        async def forward_ws(ws): await proxy_websocket(ws, url.replace('http', 'ws')+'/ws?'+ws.url.query)
        app = Starlette(routes=[Route('/', forward_http, methods=['PATCH']), WebSocketRoute('/ws', forward_ws)])
        with TestClient(app) as proxy:
            body = b'["a", {"b":2}]'
            headers = [('Content-Type', 'application/json'), ('X-Tag', 'a'), ('X-Tag', 'b'),
                ('Connection', 'x-private'), ('X-Private', 'internal'), ('Authorization', 'private')]
            res = proxy.patch('/?q=one&q=two', content=body, headers=headers)
            assert (res.status_code, res.content) == (201, body)
            assert res.headers['content-type']=='application/json' and res.headers['x-query']=='q=one&q=two'
            assert (res.headers['x-method'], res.headers['x-private'], res.headers['x-auth']) == ('PATCH', '', '')
            assert res.headers.get_list('x-tag') == ['a', 'b']
            with proxy.websocket_connect('/ws', subprotocols=['echo']) as ws:
                assert ws.accepted_subprotocol == 'echo'
                ws.send_text('hello')
                assert ws.receive_text() == 'hello'
                ws.send_bytes(b'\x00bytes')
                assert ws.receive_bytes() == b'\x00bytes'
                assert ws.receive()['code'] == 1000
            for status in (401, 403, 404):
                with proxy.websocket_connect(f'/ws?deny={status}') as ws: assert ws.receive()['code'] == 1008
