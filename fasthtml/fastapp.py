"""The `fast_app` convenience wrapper"""

import inspect,uvicorn
from fastcore.utils import *
from fastlite import *
from .basics import *
from .pico import *
from .starlette import *
from .live_reload import FastHTMLWithLiveReload

__all__ = ['fast_app']

def _get_tbl(dt, nm, schema):
    render = schema.pop('render', None)
    tbl = dt[nm]
    if tbl not in dt: tbl.create(**schema)
    else: tbl.create(**schema, transform=True)
    dc = tbl.dataclass()
    if render: dc.__ft__ = render
    return tbl,dc

def _app_factory(*args, **kwargs) -> FastHTML | FastHTMLWithLiveReload:
    "Creates a FastHTML or FastHTMLWithLiveReload app instance"
    if kwargs.pop('live', False): return FastHTMLWithLiveReload(*args, **kwargs)
    kwargs.pop('reload_attempts', None)
    kwargs.pop('reload_interval', None)
    return FastHTML(*args, **kwargs)

def fast_app(
        db_file:Optional[str]=None, # Database file name, if needed
        render:Optional[callable]=None, # Function used to render default database class
        hdrs:Optional[tuple]=None, # Additional FT elements to add to <HEAD>
        ftrs:Optional[tuple]=None, # Additional FT elements to add to end of <BODY>
        tbls:Optional[dict]=None, # Experimental mapping from DB table names to dict table definitions
        before:Optional[tuple]|Beforeware=None, # Functions to call prior to calling handler
        middleware:Optional[tuple]=None, # Standard Starlette middleware
        live:bool=False, # Enable live reloading
        debug:bool=False, # Passed to Starlette, indicating if debug tracebacks should be returned on errors
        title:str="FastHTML page", # Default page title
        routes:Optional[tuple]=None, # Passed to Starlette
        exception_handlers:Optional[dict]=None, # Passed to Starlette
        on_startup:Optional[callable]=None, # Passed to Starlette
        on_shutdown:Optional[callable]=None, # Passed to Starlette
        lifespan:Optional[callable]=None, # Passed to Starlette
        default_hdrs=True, # Include default FastHTML headers such as HTMX script?
        pico:Optional[bool]=None, # Include PicoCSS header?
        surreal:Optional[bool]=True, # Include surreal.js/scope headers?
        htmx:Optional[bool]=True, # Include HTMX header?
        exts:Optional[list|str]=None, # HTMX extension names to include
        canonical:bool=True, # Automatically include canonical link?
        secret_key:Optional[str]=None, # Signing key for sessions
        key_fname:str='.sesskey', # Session cookie signing key file name
        session_cookie:str='session_', # Session cookie name
        max_age:int=365*24*3600, # Session cookie expiry time
        sess_path:str='/', # Session cookie path
        same_site:str='lax', # Session cookie same site policy
        sess_https_only:bool=False, # Session cookie HTTPS only?
        sess_domain:Optional[str]=None, # Session cookie domain
        htmlkw:Optional[dict]=None, # Attrs to add to the HTML tag
        bodykw:Optional[dict]=None, # Attrs to add to the Body tag
        reload_attempts:Optional[int]=1, # Number of reload attempts when live reloading
        reload_interval:Optional[int]=1000, # Time between reload attempts in ms
        static_path:str=".",  # Where the static file route points to, defaults to root dir
        body_wrap:callable=noop_body, # FT wrapper for body contents
        nb_hdrs:bool=False, # If in notebook include headers inject headers in notebook DOM?
        **kwargs)->Any:
    "Create a FastHTML or FastHTMLWithLiveReload app."
    h = (picolink,) if pico or (pico is None and default_hdrs) else ()
    if hdrs: h += tuple(hdrs)

    app = _app_factory(hdrs=h, ftrs=ftrs, before=before, middleware=middleware, live=live, debug=debug, title=title, routes=routes, exception_handlers=exception_handlers,
                  on_startup=on_startup, on_shutdown=on_shutdown, lifespan=lifespan, default_hdrs=default_hdrs, secret_key=secret_key, canonical=canonical,
                  session_cookie=session_cookie, max_age=max_age, sess_path=sess_path, same_site=same_site, sess_https_only=sess_https_only,
                  sess_domain=sess_domain, key_fname=key_fname, exts=exts, surreal=surreal, htmx=htmx, htmlkw=htmlkw,
                  reload_attempts=reload_attempts, reload_interval=reload_interval, body_wrap=body_wrap, nb_hdrs=nb_hdrs, **(bodykw or {}))
    app.static_route_exts(static_path=static_path)
    if not db_file: return app,app.route

    db = database(db_file)
    if not tbls: tbls={}
    if kwargs:
        if isinstance(first(kwargs.values()), dict): tbls = kwargs
        else:
            kwargs['render'] = render
            tbls['items'] = kwargs
    dbtbls = [_get_tbl(db.t, k, v) for k,v in tbls.items()]
    if len(dbtbls)==1: dbtbls=dbtbls[0]
    return app,app.route,*dbtbls

