from starlette.responses import FileResponse
from fastcore.utils import *
from fastcore.xml import *
from fasthtml import *
from sqlite_utils import Database
from fastlite import *

def fast_app(db=None, hdrs=None, **kwargs):
    h = (picolink,)
    if hdrs: h += hdrs
    app = FastHTML(hdrs=h)
    @app["/{fname:path}.{ext:static}"]
    async def get(fname:str, ext:str): return FileResponse(f'{fname}.{ext}')
    if not db: return app

    db = Database(db)
    items = db.t.items
    if items not in db.t: items.create(**kwargs)
    dc = items.dataclass()
    return app,items,dc

def clear(id): return Div(hx_swap_oob='innerHTML', id=id)

