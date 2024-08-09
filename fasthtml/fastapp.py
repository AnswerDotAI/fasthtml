from __future__ import annotations

import inspect,uvicorn
from fastcore.utils import *
from fastlite import *
from fasthtml import *
from fasthtml.live_reload import FastHTMLWithLiveReload

def get_tbl(dt, nm, schema):
    render = schema.pop('render', None)
    tbl = dt[nm]
    if tbl not in dt: tbl.create(**schema)
    else: tbl.create(**schema, transform=True)
    dc = tbl.dataclass()
    if render: dc.__ft__ = render
    return tbl,dc

def app_factory(*args, **kwargs)->FastHTML | FastHTMLWithLiveReload: 
    """Creates a FastHTML or FastHTMLWithLiveReload app instance.
    The type of app created is determined by the "live" key in kwargs.

    Returns:
        FastHTML | FastHTMLWithLiveReload: The app instance.
    """
    if kwargs.pop('live', False):
        return FastHTMLWithLiveReload(*args, **kwargs)
    kwargs.pop('reload_attempts', None)
    kwargs.pop('reload_interval', None)
    return FastHTML(*args, **kwargs)

def fast_app(
        db_file:Optional[str]=None, # Database file name, if needed
        render:Optional[callable]=None, # Function used to render default database class
        hdrs:Optional[tuple]=None, # Additional FT elements to add to <HEAD>
        ftrs:Optional[tuple]=None, # Additional FT elements to add to end of <BODY>
        tbls:Optional[dict]=None, # Mapping from DB table names to dict table definitions
        before:Optional[tuple]|Beforeware=None, # Functions to call prior to calling handler
        middleware:Optional[tuple]=None, # Standard Starlette middleware
        live:bool=False, # Enable live reloading
        debug:bool=False, # Passed to Starlette, indicating if debug tracebacks should be returned on errors
        routes:Optional[tuple]=None, # Passed to Starlette
        exception_handlers:Optional[dict]=None, # Passed to Starlette
        on_startup:Optional[callable]=None, # Passed to Starlette
        on_shutdown:Optional[callable]=None, # Passed to Starlette
        lifespan:Optional[callable]=None, # Passed to Starlette
        default_hdrs=True, # Include default FastHTML headers such as HTMX script?
        pico:Optional[bool]=None, # Include PicoCSS header?
        ws_hdr:bool=False, # Include HTMX websocket extension header?
        secret_key:Optional[str]=None, # Signing key for sessions
        key_fname:str='.sesskey', # Session cookie signing key file name
        session_cookie:str='session_', # Session cookie name
        max_age:int=365*24*3600, # Session cookie expiry time
        sess_path:str='/', # Session cookie path
        same_site:str='lax', # Session cookie same site policy
        sess_https_only:bool=False, # Session cookie HTTPS only?
        sess_domain:Optional[str]=None, # Session cookie domain
        htmlkw:Optional[dict]=None, 
        bodykw:Optional[dict]=None,
        reload_attempts:Optional[int]=1, # Number of reload attempts when live reloading
        reload_interval:Optional[int]=1000, # Time between reload attempts in ms
        **kwargs)->Any:
    h = (picolink,) if pico or (pico is None and default_hdrs) else ()
    if hdrs: h += tuple(hdrs)

    app = app_factory(hdrs=h, ftrs=ftrs, before=before, middleware=middleware, live=live, debug=debug, routes=routes, exception_handlers=exception_handlers,
                  on_startup=on_startup, on_shutdown=on_shutdown, lifespan=lifespan, default_hdrs=default_hdrs, secret_key=secret_key,
                  session_cookie=session_cookie, max_age=max_age, sess_path=sess_path, same_site=same_site, sess_https_only=sess_https_only,
                  sess_domain=sess_domain, key_fname=key_fname, ws_hdr=ws_hdr, htmlkw=htmlkw, reload_attempts=reload_attempts, reload_interval=reload_interval, **(bodykw or {}))

    @app.route("/{fname:path}.{ext:static}")
    async def get(fname:str, ext:str): return FileResponse(f'{fname}.{ext}')
    if not db_file: return app,app.route

    db = database(db_file)
    if not tbls: tbls={}
    if kwargs:
        if isinstance(first(kwargs.values()), dict): tbls = kwargs
        else:
            kwargs['render'] = render
            tbls['items'] = kwargs
    dbtbls = [get_tbl(db.t, k, v) for k,v in tbls.items()]
    if len(dbtbls)==1: dbtbls=dbtbls[0]
    return app,app.route,*dbtbls

def serve(appname=None, app='app', host='0.0.0.0', port=None, reload=True):
    bk = inspect.currentframe().f_back
    glb = bk.f_globals
    code = bk.f_code
    if not appname:
        if glb.get('__name__')=='__main__': appname = Path(glb.get('__file__', '')).stem
        elif code.co_name=='main' and bk.f_back.f_globals.get('__name__')=='__main__': appname = inspect.getmodule(bk).__name__
    if appname:
        if not port: port=int(os.getenv("PORT", default=5001))
        print(f'Link: http://{"localhost" if host=="0.0.0.0" else host}:{port}')
        uvicorn.run(f'{appname}:{app}', host=host, port=port, reload=reload)

def clear(id)->Div: return Div(hx_swap_oob='innerHTML', id=id)
def ContainerX(*cs, **kwargs)->Main: return Main(*cs, **kwargs, cls='container', hx_push_url='true', hx_swap_oob='true', id='main')
def Page(title, *con)->tuple[Title,ContainerX]: return Title(title), ContainerX(H1(title), *con)

