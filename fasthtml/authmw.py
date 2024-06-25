import base64, binascii, re
from fasthtml.core import *
from fasthtml.starlette import *
from typing import Mapping
from hmac import compare_digest

auth_hdrs = {'WWW-Authenticate': 'Basic realm="login"'}

class BasicAuthMiddleware(MiddlewareBase):
    def __init__(self, app, cb, skip=None): self.app,self.cb,self.skip = app,cb,skip or []

    async def _resp(self, scope, receive, send, resp):
        await (send({"type": "websocket.close", "code": 1000}) if scope["type"]=="websocket" else resp(scope, receive, send))

    async def __call__(self, scope, receive, send) -> None:
        conn = await super().__call__(scope, receive, send)
        if not conn: return
        request = Request(scope, receive)
        if not any(re.match(o+'$', request.url.path) for o in self.skip):
            res = await self.authenticate(conn)
            if not res: res = Response('not authenticated', status_code=401, headers=auth_hdrs)
            if isinstance(res, Response): return await self._resp(scope, receive, send, res)
            scope["auth"] = res
        await self.app(scope, receive, send)

    async def authenticate(self, conn):
        if "Authorization" not in conn.headers: return
        auth = conn.headers["Authorization"]
        try:
            scheme, credentials = auth.split()
            if scheme.lower() != 'basic': return
            decoded = base64.b64decode(credentials).decode("ascii")
        except (ValueError, UnicodeDecodeError, binascii.Error) as exc: raise AuthenticationError('Invalid credentials')
        user, _, pwd = decoded.partition(":")
        if self.cb(user,pwd): return user

def user_pwd_auth(lookup=None, skip=None, **kwargs):
    if isinstance(lookup,Mapping): kwargs = lookup | kwargs
    def cb(u,p):
        if u=='logout' or not u or not p: return
        if callable(lookup): return lookup(u,p)
        return compare_digest(kwargs.get(u,'').encode("utf-8"), p.encode("utf-8"))
    return Middleware(BasicAuthMiddleware, cb=cb, skip=skip)

def basic_logout(request):
    return f'{request.url.scheme}://logout:logout@{request.headers["host"]}/'
