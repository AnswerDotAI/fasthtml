"""Streaming HTTP responses, bidirectional WebSocket forwarding, and prefix proxy routes

Register proxy handlers with Starlette's `Route` and `WebSocketRoute`, or build them with `proxy_routes`. FastHTML's normal route injection parses request bodies before calling the handler. Raw routes leave JSON, multipart and other bodies unread for forwarding. Choose the upstream URL and authenticate callers in your application.

`ProxyResponse` streams request and response bodies without decoding them. It reuses a per-event-loop pooled `httpx2.AsyncClient` with cookie persistence disabled so upstream `Set-Cookie` headers never leak across callers. You can pass an explicit `client`, supply filtered request headers, and override response headers through `response.headers`. `fallback` is an optional response for upstream connection failures. Connection attempts time out after 10 seconds. Transfers have no timeout.

`proxy_headers` removes hop-by-hop headers, connection-nominated headers, and any names in `exclude` or `set`, then appends non-None entries from `set`. Repeated end-to-end values remain separate, with lowercase names.

`proxy_websocket` connects upstream before accepting the caller. Upstream HTTP 4xx and 5xx refusals forward their status, body, and content type via `send_denial_response` when the server supports the WebSocket denial extension, or otherwise accept and close the caller with code 1008. It forwards the selected subprotocol and relays text and binary frames. Either peer disconnecting cancels the other forwarding task and closes the upstream connection. Supply a complete URL, including any query parameters.

The relay reads raw ASGI events from `receive()`. A `websocket.receive` event carries `text` or `bytes`. A `websocket.disconnect` event carries a close `code`. `receive_text()` and `receive_bytes()` extract one data field instead.

`proxy_routes` builds Starlette routes for a URL prefix, redirecting bare `/prefix` to `/prefix/` with status 307 (preserving query strings), safely quoting forwarded paths, and optionally adding a matching `WebSocketRoute`. Register raw routes after any application routes that should take precedence. Keep access checks and destination selection in these handlers or in `before`.

```python
from fasthtml.common import FastHTML
from fasthtml.proxy import proxy_headers, proxy_routes

app = FastHTML()
app.router.routes += proxy_routes(
    '/upstream', 'http://127.0.0.1:8000',
    headers=lambda r: proxy_headers(r.headers, exclude=('authorization',), set={'x-user': r.session.get('auth')}),
    ws=True,
)
```
"""

__all__ = ['PROXY_METHODS', 'proxy_headers', 'ProxyResponse', 'proxy_websocket', 'proxy_routes']

import asyncio, inspect, httpx2, websockets
from http.cookiejar import CookieJar, DefaultCookiePolicy
from urllib.parse import quote
from weakref import WeakKeyDictionary
from starlette.responses import RedirectResponse, Response, StreamingResponse
from starlette.routing import Route, WebSocketRoute
from starlette.websockets import WebSocketDisconnect

PROXY_METHODS = ('GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'HEAD', 'OPTIONS')

_clients = WeakKeyDictionary()

def _proxy_client():
    loop = asyncio.get_running_loop()
    client = _clients.get(loop)
    if client is None or client.is_closed:
        client = httpx2.AsyncClient(timeout=httpx2.Timeout(None, connect=10),
            cookies=CookieJar(policy=DefaultCookiePolicy(allowed_domains=[])))
        _clients[loop] = client
    return client

def _hname(k): return (k.encode() if isinstance(k, str) else k).lower()
def _hval(v): return v.encode() if isinstance(v, str) else v

def proxy_headers(
    headers, # Starlette or HTTPX headers exposing `.raw` pairs
    exclude=(), # Additional header names (str or bytes, case-insensitive) to remove
    set=None, # Mapping of header names to str or bytes values to set; always strips incoming headers with those names and skips None values
):
    "Remove hop-by-hop headers before forwarding, optionally stripping and setting headers."
    drop = {b'host', b'connection', b'keep-alive', b'proxy-authenticate', b'proxy-authorization',
        b'te', b'trailer', b'transfer-encoding', b'upgrade',
        b'sec-websocket-key', b'sec-websocket-version', b'sec-websocket-extensions', b'sec-websocket-protocol', b'sec-websocket-accept'}
    drop.update(v.strip().encode() for v in headers.get('connection', '').lower().split(','))
    drop.update(_hname(k) for k in exclude)
    if set: drop.update(_hname(k) for k in set)
    out = [(k.lower(),v) for k,v in headers.raw if k.lower() not in drop]
    if set: out += [(_hname(k), _hval(v)) for k,v in set.items() if v is not None]
    return out

class ProxyResponse(Response):
    "Stream a request and response while keeping their transport open."
    def __init__(
        self,
        request, # Incoming Starlette request
        url, # Upstream URL without query parameters
        headers=None, # Upstream request headers; default removes hop-by-hop fields
        fallback=None, # Optional ASGI response for upstream connection failures
        client=None, # Optional shared httpx2.AsyncClient; default uses a per-loop pooled client
    ):
        super().__init__()
        self.raw_headers = []
        self.request,self.url = request,url
        self.fwd = proxy_headers(request.headers) if headers is None else headers
        self.fallback,self.client = fallback,client

    async def __call__(self, scope, receive, send):
        stream = self.request.stream()
        first = await anext(stream)
        async def body():
            yield first
            async for chunk in stream: yield chunk
        try:
            client = self.client or _proxy_client()
            async with client.stream(self.request.method, self.url, headers=self.fwd,
                params=self.request.url.query, content=body() if first else None) as r:
                response = StreamingResponse(r.aiter_raw(), status_code=r.status_code)
                replaced = {k for k,v in self.raw_headers}
                response.raw_headers = [(k,v) for k,v in proxy_headers(r.headers) if k not in replaced] + self.raw_headers
                await response(scope, receive, send)
        except (httpx2.ConnectError, httpx2.ConnectTimeout):
            if self.fallback is None: raise
            await self.fallback(scope, receive, send)


async def _deny_ws(websocket, response, reason=''):
    if 'websocket.http.response' in websocket.scope.get('extensions', {}): return await websocket.send_denial_response(response)
    await websocket.accept()
    await websocket.close(code=1008, reason=reason)

async def proxy_websocket(
    websocket, # Incoming Starlette WebSocket, not yet accepted
    url, # Complete upstream WebSocket URL, including query parameters
    headers=None, # Additional upstream headers, as a mapping or string/byte pairs
):
    "Relay text and binary frames until either peer disconnects."
    try:
        async with websockets.connect(url, additional_headers=httpx2.Headers(headers).multi_items(),
            subprotocols=websocket.scope['subprotocols'] or None, max_size=None) as target:
            await websocket.accept(subprotocol=target.subprotocol)
            async def to_target():
                while True:
                    message = await websocket.receive()
                    if message['type']=='websocket.disconnect': return
                    await target.send(message['text'] if 'text' in message else message['bytes'])
            async def to_client():
                async for message in target:
                    if isinstance(message, str): await websocket.send_text(message)
                    else: await websocket.send_bytes(message)
            tasks = [asyncio.create_task(to_target()), asyncio.create_task(to_client())]
            try:
                done,_ = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
                for task in done: task.result()
            finally:
                for task in tasks: task.cancel()
                await asyncio.gather(*tasks, return_exceptions=True)
                if websocket.client_state.name!='DISCONNECTED':
                    code = target.close_code if target.close_code not in (None, 1005, 1006, 1015) else 1011
                    await websocket.close(code=code, reason=target.close_reason or '')
    except websockets.exceptions.InvalidStatus as e:
        if e.response.status_code < 400: raise
        resp = Response(bytes(e.response.body), status_code=e.response.status_code,
            media_type=e.response.headers.get('content-type'))
        await _deny_ws(websocket, resp, f'Upstream refused connection ({e.response.status_code})')

async def _run_before(before, conn):
    if not before: return None
    fns = before if isinstance(before, (list, tuple)) else (before,)
    for fn in fns:
        res = fn(conn)
        if inspect.isawaitable(res): res = await res
        if res is not None: return res

def _resolve(val, conn): return val(conn) if callable(val) else val

def proxy_routes(
    prefix, # URL prefix to mount, e.g. '/svelteit' or '/rusty'
    target, # Upstream base URL string, or callable(conn) -> str
    headers=None, # Forwarded headers, or callable(conn) -> headers; default uses proxy_headers
    before=None, # Optional check callable(conn) (sync or async), or sequence of them; non-None return short-circuits
    methods=PROXY_METHODS, # HTTP methods accepted on the proxy routes
    ws=False, # Also register a WebSocketRoute at `{prefix}/{path:path}`?
    redirect_root=True, # Redirect bare `{prefix}` to `{prefix}/` (307, preserving query string)?
    fallback=None, # Optional ASGI response for upstream connection failures
    client=None, # Optional shared httpx2.AsyncClient; default uses a per-loop pooled client
):
    "Return Starlette `Route`s (and optional `WebSocketRoute`) proxying `prefix` to `target`."
    prefix = '/' + prefix.strip('/')
    if prefix == '/': raise ValueError("prefix must not be '/'")
    def _url(conn, scheme=None):
        base = _resolve(target, conn).rstrip('/')
        if scheme: base = base.replace('http', scheme, 1)
        if 'path' not in conn.path_params: return base
        return f"{base}/{quote(conn.path_params['path'], safe='/')}"
    async def forward_http(request):
        if denied := await _run_before(before, request): return denied
        if redirect_root and request.url.path == prefix:
            dest = f'{prefix}/' + (f'?{request.url.query}' if request.url.query else '')
            return RedirectResponse(dest, status_code=307)
        return ProxyResponse(request, _url(request), headers=_resolve(headers, request), fallback=fallback, client=client)
    routes = [Route(prefix, forward_http, methods=methods), Route(f'{prefix}/{{path:path}}', forward_http, methods=methods)]
    if ws:
        async def forward_ws(websocket):
            if denied := await _run_before(before, websocket): return await _deny_ws(websocket, denied)
            url = _url(websocket, 'ws')
            if websocket.url.query: url += f'?{websocket.url.query}'
            try: await proxy_websocket(websocket, url, headers=_resolve(headers, websocket))
            except (websockets.ConnectionClosed, WebSocketDisconnect): pass
        routes.append(WebSocketRoute(f'{prefix}/{{path:path}}', forward_ws))
    return routes

