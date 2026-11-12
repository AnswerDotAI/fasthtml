"""Streaming HTTP responses and bidirectional WebSocket forwarding

Register proxy handlers with Starlette's `Route` and `WebSocketRoute`. FastHTML's normal route injection parses request bodies before calling the handler. Raw routes leave JSON, multipart and other bodies unread for forwarding. Choose the upstream URL and authenticate callers in your application.

`ProxyResponse` streams request and response bodies without decoding them. It preserves response status and end-to-end headers, including repeated headers. You can supply filtered request headers and override response headers through `response.headers`. `fallback` is an optional response for upstream connection failures. Connection attempts time out after 10 seconds. Transfers have no timeout.

Connection-nominated headers and explicitly excluded names are removed. Repeated end-to-end values remain separate, with lowercase names.

`proxy_websocket` connects upstream before accepting the caller. Upstream HTTP 401, 403 and 404 responses accept and close the caller with code 1008. It forwards the selected subprotocol and relays text and binary frames. Either peer disconnecting cancels the other forwarding task and closes the upstream connection. Supply a complete URL, including any query parameters.

The relay reads raw ASGI events from `receive()`. A `websocket.receive` event carries `text` or `bytes`. A `websocket.disconnect` event carries a close `code`. `receive_text()` and `receive_bytes()` extract one data field instead.

Register raw routes after any application routes that should take precedence. Keep access checks and destination selection in these handlers.

```python
from fasthtml.common import FastHTML
from fasthtml.proxy import ProxyResponse, proxy_websocket
from starlette.routing import Route, WebSocketRoute

app = FastHTML()
async def forward_http(request): return ProxyResponse(request, 'http://127.0.0.1:8000/')
async def forward_ws(ws): await proxy_websocket(ws, 'ws://127.0.0.1:8000/ws')
app.router.routes += [Route('/upstream', forward_http, methods=['GET', 'POST', 'PATCH']),
                      WebSocketRoute('/upstream/ws', forward_ws)]
```
"""

__all__ = ['proxy_headers', 'ProxyResponse', 'proxy_websocket']

import asyncio, httpx2, websockets
from starlette.responses import Response, StreamingResponse

def proxy_headers(
    headers, # Starlette or HTTPX headers exposing `.raw` pairs
    exclude=(), # Additional lowercase byte names to remove
):
    "Remove hop-by-hop headers before forwarding."
    hop = {b'host', b'connection', b'keep-alive', b'proxy-authenticate', b'proxy-authorization',
        b'te', b'trailer', b'transfer-encoding', b'upgrade'}
    hop.update(v.strip().encode() for v in headers.get('connection', '').lower().split(','))
    return [(k.lower(),v) for k,v in headers.raw if k.lower() not in hop and k.lower() not in exclude]

class ProxyResponse(Response):
    "Stream a request and response while keeping their transport open."
    def __init__(
        self,
        request, # Incoming Starlette request
        url, # Upstream URL without query parameters
        headers=None, # Upstream request headers; default removes hop-by-hop fields
        fallback=None, # Optional ASGI response for upstream connection failures
    ):
        super().__init__()
        self.raw_headers = []
        self.request,self.url = request,url
        self.fwd = proxy_headers(request.headers) if headers is None else headers
        self.fallback = fallback

    async def __call__(self, scope, receive, send):
        try:
            async with httpx2.AsyncClient(timeout=httpx2.Timeout(None, connect=10)) as client:
                async with client.stream(self.request.method, self.url, headers=self.fwd,
                    params=self.request.url.query, content=self.request.stream()) as r:
                    response = StreamingResponse(r.aiter_raw(), status_code=r.status_code)
                    replaced = {k for k,v in self.raw_headers}
                    response.raw_headers = [(k,v) for k,v in proxy_headers(r.headers) if k not in replaced] + self.raw_headers
                    await response(scope, receive, send)
        except (httpx2.ConnectError, httpx2.ConnectTimeout):
            if self.fallback is None: raise
            await self.fallback(scope, receive, send)


async def proxy_websocket(
    websocket, # Incoming Starlette WebSocket, not yet accepted
    url, # Complete upstream WebSocket URL, including query parameters
    headers=None, # Additional upstream handshake headers
):
    "Relay text and binary frames until either peer disconnects."
    try:
        async with websockets.connect(url, additional_headers=headers,
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
        if e.response.status_code not in (401, 403, 404): raise
        await websocket.accept()
        await websocket.close(code=1008, reason=f'Upstream refused connection ({e.response.status_code})')

