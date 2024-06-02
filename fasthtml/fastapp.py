from fasthtml.all import *

def get_tbl(dt, nm, schema):
    render = schema.pop('render', None)
    tbl = dt[nm]
    if tbl not in dt: tbl.create(**schema)
    dc = tbl.dataclass()
    if render: dc.__xt__ = render
    return tbl,dc

def fast_app(db=None, render=None, hdrs=None, tbls=None, **kwargs):
    h = (picolink,)
    if hdrs: h += tuple(hdrs)
    app = FastHTML(hdrs=h)
    @app.route("/{fname:path}.{ext:static}")
    async def get(fname:str, ext:str): return FileResponse(f'{fname}.{ext}')
    if not db: return app

    if not tbls: tbls={}
    if kwargs:
        kwargs['render'] = render
        tbls['items'] = kwargs
    db = Database(db)
    db.enable_wal()
    dbtbls = [get_tbl(db.t, k, v) for k,v in tbls.items()]
    if len(dbtbls)==1: dbtbls=dbtbls[0]
    return app,*dbtbls

def clear(id): return Div(hx_swap_oob='innerHTML', id=id)
target = dict(hx_target='main', hx_swap='outerHTML')

def Container(*cs, **kwargs): return Main(*cs, **kwargs, cls='container', hx_push_url='true', hx_swap_oob='true', id='main')
def Page(title, *con): return Title(title), Container(H1(title), *con)

