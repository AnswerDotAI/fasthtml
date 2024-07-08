import inspect,uvicorn
from fastcore.utils import *
from fastlite import *
from fasthtml import *
from fasthtml.live_reload import FastHTMLWithLiveReload

def get_tbl(dt, nm, schema):
    render = schema.pop('render', None)
    tbl = dt[nm]
    if tbl not in dt: tbl.create(**schema)
    dc = tbl.dataclass()
    if render: dc.__xt__ = render
    return tbl,dc

def fast_app(db=None, render=None, hdrs=None, tbls=None, before=None, middleware=None, live=False, debug=False, routes=None, exception_handlers=None,
             on_startup=None, on_shutdown=None, lifespan=None, default_hdrs=True, secret_key=None, session_cookie='session_', max_age=365*24*3600,
             sess_path='/', same_site='lax', sess_https_only=False, sess_domain=None, key_fname='.sesskey', **kwargs):
    h = (picolink,)
    if hdrs: h += tuple(hdrs)
    app_cls = FastHTMLWithLiveReload if live else FastHTML
    app = app_cls(hdrs=h, before=before, middleware=middleware, debug=debug, routes=routes, exception_handlers=exception_handlers,
                  on_startup=on_startup, on_shutdown=on_shutdown, lifespan=lifespan, default_hdrs=default_hdrs, secret_key=secret_key,
                  session_cookie=session_cookie, max_age=max_age, sess_path=sess_path, same_site=same_site, sess_https_only=sess_https_only,
                  sess_domain=sess_domain, key_fname=key_fname)
    @app.route("/{fname:path}.{ext:static}")
    async def get(fname:str, ext:str): return FileResponse(f'{fname}.{ext}')
    if not db: return app,app.route

    db = database(db)
    if not tbls: tbls={}
    if kwargs:
        if isinstance(first(kwargs.values()), dict): tbls = kwargs
        else:
            kwargs['render'] = render
            tbls['items'] = kwargs
    dbtbls = [get_tbl(db.t, k, v) for k,v in tbls.items()]
    if len(dbtbls)==1: dbtbls=dbtbls[0]
    return app,app.route,*dbtbls

def run_uv(fname=None, app='app', host='0.0.0.0', port=None, reload=True):
    glb = inspect.currentframe().f_back.f_globals
    if glb.get('__name__') == '__main__':
        if not fname: fname = Path(glb.get('__file__', '')).stem
        if not port: port=int(os.getenv("PORT", default=5001))
        print(f'Link: http://{"localhost" if host=="0.0.0.0" else host}:{port}')
        uvicorn.run(f"{fname}:app", host=host, port=port, reload=reload)

def clear(id): return Div(hx_swap_oob='innerHTML', id=id)
def ContainerX(*cs, **kwargs): return Main(*cs, **kwargs, cls='container', hx_push_url='true', hx_swap_oob='true', id='main')
def Page(title, *con): return Title(title), ContainerX(H1(title), *con)

