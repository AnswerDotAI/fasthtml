"""The `FastHTML` subclass of `Starlette`, along with the `RouterX` and `RouteX` classes it automatically uses."""
__all__ = ['empty', 'htmx_hdrs', 'fh_cfg', 'htmxsrc', 'htmxwssrc', 'fhjsscr', 'htmxctsrc', 'surrsrc', 'scopesrc', 'viewport', 'charset', 'all_meths', 'date', 'snake2hyphens', 'HtmxHeaders', 'str2int', 'HttpHeader', 'form2dict', 'flat_xt', 'Beforeware', 'WS_RouteX', 'uri', 'decode_uri', 'flat_tuple', 'RouteX', 'RouterX', 'get_key', 'FastHTML', 'serve', 'cookie', 'reg_re_param', 'MiddlewareBase']
import json, uuid, inspect, types, uvicorn
from starlette.datastructures import URLPath
from fastcore.utils import *
from fastcore.xml import *
from types import UnionType, SimpleNamespace as ns, GenericAlias
from typing import Optional, get_type_hints, get_args, get_origin, Union, Mapping, TypedDict, List, Any
from datetime import datetime
from dataclasses import dataclass, fields
from collections import namedtuple
from inspect import isfunction, ismethod, Parameter, get_annotations
from functools import wraps, partialmethod, update_wrapper
from http import cookies
from urllib.parse import urlencode, parse_qs, quote, unquote
from copy import copy, deepcopy
from warnings import warn
from dateutil import parser as dtparse
from starlette.requests import HTTPConnection
from .starlette import *
empty = Parameter.empty

def _sig(f):
    ...

def date(s: str):
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

def str2int(s) -> int:
    """Convert `s` to an `int`"""
    ...

def _mk_list(t, v):
    ...
fh_cfg = AttrDict(indent=True)

def _fix_anno(t):
    """Create appropriate callable type for casting a `str` to type `t` (or first type in `t` if union)"""
    ...

def _form_arg(k, v, d):
    """Get type by accessing key `k` from `d`, and use to cast `v`"""
    ...

@dataclass
class HttpHeader:
    k: str
    v: str

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

async def _from_body(req, p):
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

class WS_RouteX(WebSocketRoute):

    def __init__(self, app, path: str, recv, conn: callable=None, disconn: callable=None, *, name=None, middleware=None):
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

def flat_tuple(o):
    """Flatten lists"""
    ...

def _xt_resp(req, resp):
    ...

def _resp(req, resp, cls=empty):
    ...

async def _wrap_call(f, req, params):
    ...

class RouteX(Route):

    def __init__(self, app, path: str, endpoint, *, methods=None, name=None, include_in_schema=True, middleware=None):
        ...

    async def _endp(self, req):
        ...

class RouterX(Router):

    def __init__(self, app, routes=None, redirect_slashes=True, default=None, *, middleware=None):
        ...

    def add_route(self, path: str, endpoint: callable, methods=None, name=None, include_in_schema=True):
        ...

    def add_ws(self, path: str, recv: callable, conn: callable=None, disconn: callable=None, name=None):
        ...
htmxsrc = Script(src='https://unpkg.com/htmx.org@next/dist/htmx.min.js')
htmxwssrc = Script(src='https://unpkg.com/htmx-ext-ws/ws.js')
fhjsscr = Script(src='https://cdn.jsdelivr.net/gh/answerdotai/fasthtml-js@main/fasthtml.js')
htmxctsrc = Script(src='https://unpkg.com/htmx-ext-transfer-encoding-chunked/transfer-encoding-chunked.js')
surrsrc = Script(src='https://cdn.jsdelivr.net/gh/answerdotai/surreal@main/surreal.js')
scopesrc = Script(src='https://cdn.jsdelivr.net/gh/gnat/css-scope-inline@main/script.js')
viewport = Meta(name='viewport', content='width=device-width, initial-scale=1, viewport-fit=cover')
charset = Meta(charset='utf-8')

def get_key(key=None, fname='.sesskey'):
    ...

def _list(o):
    ...

def _wrap_ex(f, hdrs, ftrs, htmlkw, bodykw):
    ...

def _mk_locfunc(f, p):
    ...

class FastHTML(Starlette):

    def __init__(self, debug=False, routes=None, middleware=None, exception_handlers=None, on_startup=None, on_shutdown=None, lifespan=None, hdrs=None, ftrs=None, before=None, after=None, ws_hdr=False, ct_hdr=False, surreal=True, htmx=True, default_hdrs=True, sess_cls=SessionMiddleware, secret_key=None, session_cookie='session_', max_age=365 * 24 * 3600, sess_path='/', same_site='lax', sess_https_only=False, sess_domain=None, key_fname='.sesskey', htmlkw=None, **bodykw):
        ...

    def ws(self, path: str, conn=None, disconn=None, name=None):
        """Add a websocket route at `path`"""
        ...

    def route(self, path: str=None, methods=None, name=None, include_in_schema=True):
        """Add a route at `path`"""
        ...
all_meths = 'get post put delete patch head trace options'.split()
for o in all_meths:
    setattr(FastHTML, o, partialmethod(FastHTML.route, methods=o))

def serve(appname=None, app='app', host='0.0.0.0', port=None, reload=True, reload_includes: list[str] | str | None=None, reload_excludes: list[str] | str | None=None):
    """Run the app in an async server, with live reload set as the default."""
    ...

def cookie(key: str, value='', max_age=None, expires=None, path='/', domain=None, secure=False, httponly=False, samesite='lax'):
    """Create a 'set-cookie' `HttpHeader`"""
    ...

def reg_re_param(m, s):
    ...
reg_re_param('path', '.*?')
reg_re_param('static', 'ico|gif|jpg|jpeg|webm|css|js|woff|png|svg|mp4|webp|ttf|otf|eot|woff2|txt|html|map')

class MiddlewareBase:

    async def __call__(self, scope, receive, send) -> None:
        ...