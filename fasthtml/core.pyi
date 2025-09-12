"""The `FastHTML` subclass of `Starlette`, along with the `RouterX` and `RouteX` classes it automatically uses."""
__all__ = ['empty', 'htmx_hdrs', 'fh_cfg', 'htmx_resps', 'htmx_exts', 'htmxsrc', 'fhjsscr', 'surrsrc', 'scopesrc', 'viewport', 'charset', 'cors_allow', 'iframe_scr', 'all_meths', 'devtools_loc', 'parsed_date', 'snake2hyphens', 'HtmxHeaders', 'HttpHeader', 'HtmxResponseHeaders', 'form2dict', 'parse_form', 'JSONResponse', 'flat_xt', 'Beforeware', 'EventStream', 'signal_shutdown', 'uri', 'decode_uri', 'flat_tuple', 'noop_body', 'respond', 'is_full_page', 'Redirect', 'get_key', 'qp', 'def_hdrs', 'FastHTML', 'nested_name', 'serve', 'Client', 'RouteFuncs', 'APIRouter', 'cookie', 'reg_re_param', 'MiddlewareBase', 'FtResponse', 'unqid']
import json, uuid, inspect, types, signal, asyncio, threading, inspect, random, contextlib
from fastcore.utils import *
from fastcore.xml import *
from fastcore.meta import use_kwargs_dict
from types import UnionType, SimpleNamespace as ns, GenericAlias
from typing import Optional, get_type_hints, get_args, get_origin, Union, Mapping, TypedDict, List, Any
from datetime import datetime, date
from dataclasses import dataclass, fields
from collections import namedtuple
from inspect import isfunction, ismethod, Parameter, get_annotations
from functools import wraps, partialmethod, update_wrapper
from http import cookies
from urllib.parse import urlencode, parse_qs, quote, unquote
from copy import copy, deepcopy
from warnings import warn
from dateutil import parser as dtparse
from httpx import ASGITransport, AsyncClient
from anyio import from_thread
from uuid import uuid4, UUID
from base64 import b85encode, b64encode
from .starlette import *

def _params(f):
    ...
empty = Parameter.empty

def parsed_date(s: str):
    """Convert `s` to a datetime"""
    ...

def snake2hyphens(s: str):
    """Convert `s` from snake case to hyphenated and capitalised"""
    ...
htmx_hdrs = dict(boosted='HX-Boosted', current_url='HX-Current-URL', history_restore_request='HX-History-Restore-Request', prompt='HX-Prompt', request='HX-Request', target='HX-Target', trigger_name='HX-Trigger-Name', trigger='HX-Trigger')

@dataclass
class HtmxHeaders:
    boosted: str | None = None
    current_url: str | None = None
    history_restore_request: str | None = None
    prompt: str | None = None
    request: str | None = None
    target: str | None = None
    trigger_name: str | None = None
    trigger: str | None = None

    def __bool__(self):
        ...

def _get_htmx(h):
    ...

def _mk_list(t, v):
    ...
fh_cfg = AttrDict(indent=True)

def _fix_anno(t, o):
    """Create appropriate callable type for casting a `str` to type `t` (or first type in `t` if union)"""
    ...

def _form_arg(k, v, d):
    """Get type by accessing key `k` from `d`, and use to cast `v`"""
    ...

@dataclass
class HttpHeader:
    k: str
    v: str

def _to_htmx_header(s):
    ...
htmx_resps = dict(location=None, push_url=None, redirect=None, refresh=None, replace_url=None, reswap=None, retarget=None, reselect=None, trigger=None, trigger_after_settle=None, trigger_after_swap=None)

@use_kwargs_dict(**htmx_resps)
def HtmxResponseHeaders(**kwargs):
    """HTMX response headers"""
    ...

def _annotations(anno):
    """Same as `get_annotations`, but also works on namedtuples"""
    ...

def _is_body(anno):
    ...

def _formitem(form, k):
    """Return single item `k` from `form` if len 1, otherwise return list"""
    ...

def form2dict(form: FormData) -> dict:
    """Convert starlette form data to a dict"""
    ...

async def parse_form(req: Request) -> FormData:
    """Starlette errors on empty multipart forms, so this checks for that situation"""
    ...

async def _from_body(req, p):
    ...

class JSONResponse(JSONResponseOrig):
    """Same as starlette's version, but auto-stringifies non serializable types"""

    def render(self, content: Any) -> bytes:
        ...

async def _find_p(req, arg: str, p: Parameter):
    """In `req` find param named `arg` of type in `p` (`arg` is ignored for body types)"""
    ...

async def _wrap_req(req, params):
    ...

def flat_xt(lst):
    """Flatten lists"""
    ...

class Beforeware:

    def __init__(self, f, skip=None):
        ...

async def _handle(f, args, **kwargs):
    ...

def _find_wsp(ws, data, hdrs, arg: str, p: Parameter):
    """In `data` find param named `arg` of type in `p` (`arg` is ignored for body types)"""
    ...

def _wrap_ws(ws, data, params):
    ...

async def _send_ws(ws, resp):
    ...

def _ws_endp(recv, conn=None, disconn=None):
    ...

def EventStream(s):
    """Create a text/event-stream response from `s`"""
    ...

def signal_shutdown():
    ...

def uri(_arg, **kwargs):
    ...

def decode_uri(s):
    ...
from starlette.convertors import StringConvertor
StringConvertor.regex = '[^/]*'

@patch
def to_string(self: StringConvertor, value: str) -> str:
    ...

@patch
def url_path_for(self: HTTPConnection, name: str, **path_params):
    ...
_verbs = dict(get='hx-get', post='hx-post', put='hx-post', delete='hx-delete', patch='hx-patch', link='href')

def _url_for(req, t):
    ...

def _find_targets(req, resp):
    ...

def _apply_ft(o):
    ...

def _to_xml(req, resp, indent):
    ...
_iter_typs = (tuple, list, map, filter, range, types.GeneratorType)

def flat_tuple(o):
    """Flatten lists"""
    ...

def noop_body(c, req):
    """Default Body wrap function which just returns the content"""
    ...

def respond(req, heads, bdy):
    """Default FT response creation function"""
    ...

def is_full_page(req, resp):
    ...

def _part_resp(req, resp):
    ...

def _xt_cts(req, resp):
    ...

def _is_ft_resp(resp):
    ...

def _resp(req, resp, cls=empty, status_code=200):
    ...

class Redirect:
    """Use HTMX or Starlette RedirectResponse as required to redirect to `loc`"""

    def __init__(self, loc):
        ...

    def __response__(self, req):
        ...

async def _wrap_call(f, req, params):
    ...
htmx_exts = {'morph': 'https://cdn.jsdelivr.net/npm/idiomorph@0.7.3/dist/idiomorph-ext.min.js', 'head-support': 'https://cdn.jsdelivr.net/npm/htmx-ext-head-support@2.0.3/head-support.js', 'preload': 'https://cdn.jsdelivr.net/npm/htmx-ext-preload@2.1.0/preload.js', 'class-tools': 'https://cdn.jsdelivr.net/npm/htmx-ext-class-tools@2.0.1/class-tools.js', 'loading-states': 'https://cdn.jsdelivr.net/npm/htmx-ext-loading-states@2.0.0/loading-states.js', 'multi-swap': 'https://cdn.jsdelivr.net/npm/htmx-ext-multi-swap@2.0.0/multi-swap.js', 'path-deps': 'https://cdn.jsdelivr.net/npm/htmx-ext-path-deps@2.0.0/path-deps.js', 'remove-me': 'https://cdn.jsdelivr.net/npm/htmx-ext-remove-me@2.0.0/remove-me.js', 'ws': 'https://cdn.jsdelivr.net/npm/htmx-ext-ws@2.0.3/ws.js', 'chunked-transfer': 'https://cdn.jsdelivr.net/npm/htmx-ext-transfer-encoding-chunked@0.4.0/transfer-encoding-chunked.js'}
htmxsrc = Script(src='https://cdn.jsdelivr.net/npm/htmx.org@2.0.4/dist/htmx.min.js')
fhjsscr = Script(src='https://cdn.jsdelivr.net/gh/answerdotai/fasthtml-js@1.0.12/fasthtml.js')
surrsrc = Script(src='https://cdn.jsdelivr.net/gh/answerdotai/surreal@main/surreal.js')
scopesrc = Script(src='https://cdn.jsdelivr.net/gh/gnat/css-scope-inline@main/script.js')
viewport = Meta(name='viewport', content='width=device-width, initial-scale=1, viewport-fit=cover')
charset = Meta(charset='utf-8')

def get_key(key=None, fname='.sesskey'):
    ...

def _list(o):
    ...

def _wrap_ex(f, status_code, hdrs, ftrs, htmlkw, bodykw, body_wrap):
    ...

def qp(p: str, **kw) -> str:
    """Add parameters kw to path p"""
    ...

def def_hdrs(htmx=True, surreal=True):
    """Default headers for a FastHTML app"""
    ...
cors_allow = Middleware(CORSMiddleware, allow_credentials=True, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])
iframe_scr = Script(NotStr("\n    function sendmsg() {\n        window.parent.postMessage({height: document.documentElement.offsetHeight}, '*');\n    }\n    window.onload = function() {\n        sendmsg();\n        document.body.addEventListener('htmx:afterSettle',    sendmsg);\n        document.body.addEventListener('htmx:wsAfterMessage', sendmsg);\n    };"))

class FastHTML(Starlette):

    def __init__(self, debug=False, routes=None, middleware=None, title: str='FastHTML page', exception_handlers=None, on_startup=None, on_shutdown=None, lifespan=None, hdrs=None, ftrs=None, exts=None, before=None, after=None, surreal=True, htmx=True, default_hdrs=True, sess_cls=SessionMiddleware, secret_key=None, session_cookie='session_', max_age=365 * 24 * 3600, sess_path='/', same_site='lax', sess_https_only=False, sess_domain=None, key_fname='.sesskey', body_wrap=noop_body, htmlkw=None, nb_hdrs=False, canonical=True, **bodykw):
        ...

    def add_route(self, route):
        ...

    def _endp(self, f, body_wrap):
        ...

    def _add_ws(self, func, path, conn, disconn, name, middleware):
        ...

    def ws(self, path: str, conn=None, disconn=None, name=None, middleware=None):
        """Add a websocket route at `path`"""
        ...

    def _add_route(self, func, path, methods, name, include_in_schema, body_wrap):
        ...

    def route(self, path: str=None, methods=None, name=None, include_in_schema=True, body_wrap=None):
        """Add a route at `path`"""
        ...

    def set_lifespan(self, value):
        ...

    def static_route_exts(self, prefix='/', static_path='.', exts='static'):
        """Add a static route at URL path `prefix` with files from `static_path` and `exts` defined by `reg_re_param()`"""
        ...

    def static_route(self, ext='', prefix='/', static_path='.'):
        """Add a static route at URL path `prefix` with files from `static_path` and single `ext` (including the '.')"""
        ...

    def setup_ws(app, f=noop):
        ...

    def devtools_json(self, path=None, uuid=None):
        ...
all_meths = 'get post put delete patch head trace options'.split()

def _mk_locfunc(f, p):
    ...

def nested_name(f):
    """Get name of function `f` using '_' to join nested function names"""
    ...
for o in all_meths:
    setattr(FastHTML, o, partialmethod(FastHTML.route, methods=o))

def serve(appname=None, app='app', host='0.0.0.0', port=None, reload=True, reload_includes: list[str] | str | None=None, reload_excludes: list[str] | str | None=None):
    """Run the app in an async server, with live reload set as the default."""
    ...

class Client:
    """A simple httpx ASGI client that doesn't require `async`"""

    def __init__(self, app, url='http://testserver'):
        ...

    def _sync(self, method, url, **kwargs):
        ...
for o in ('get', 'post', 'delete', 'put', 'patch', 'options'):
    setattr(Client, o, partialmethod(Client._sync, o))

class RouteFuncs:

    def __init__(self):
        ...

    def __setattr__(self, name, value):
        ...

    def __getattr__(self, name):
        ...

    def __dir__(self):
        ...

class APIRouter:
    """Add routes to an app"""

    def __init__(self, prefix: str | None=None, body_wrap=noop_body):
        ...

    def _wrap_func(self, func, path=None):
        ...

    def __call__(self, path: str=None, methods=None, name=None, include_in_schema=True, body_wrap=None):
        """Add a route at `path`"""
        ...

    def __getattr__(self, name):
        ...

    def to_app(self, app):
        """Add routes to `app`"""
        ...

    def ws(self, path: str, conn=None, disconn=None, name=None, middleware=None):
        """Add a websocket route at `path`"""
        ...
for o in all_meths:
    setattr(APIRouter, o, partialmethod(APIRouter.__call__, methods=o))

def cookie(key: str, value='', max_age=None, expires=None, path='/', domain=None, secure=False, httponly=False, samesite='lax'):
    """Create a 'set-cookie' `HttpHeader`"""
    ...

def reg_re_param(m, s):
    ...
reg_re_param('path', '.*?')
_static_exts = 'ico gif jpg jpeg webm css js woff png svg mp4 webp ttf otf eot woff2 txt html map pdf zip tgz gz csv mp3 wav ogg flac aac doc docx xls xlsx ppt pptx epub mobi bmp tiff avi mov wmv mkv xml yaml yml rar 7z tar bz2 htm xhtml apk dmg exe msi swf iso'.split()
reg_re_param('static', '|'.join(_static_exts))

class MiddlewareBase:

    async def __call__(self, scope, receive, send) -> None:
        ...

class FtResponse:
    """Wrap an FT response with any Starlette `Response`"""

    def __init__(self, content, status_code: int=200, headers=None, cls=HTMLResponse, media_type: str | None=None, background: BackgroundTask | None=None):
        ...

    def __response__(self, req):
        ...

def unqid(seeded=False):
    ...

def _add_ids(s):
    ...
devtools_loc = '/.well-known/appspecific/com.chrome.devtools.json'