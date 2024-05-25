import uvicorn
from starlette.responses import FileResponse, RedirectResponse, JSONResponse, HTMLResponse
from starlette.exceptions import HTTPException
from fastcore.utils import *
from fastcore.xml import *
from fasthtml import *
from starlette.requests import Request

from impl import *

htmxscr = Script(
    src="https://unpkg.com/htmx.org@1.9.12", crossorigin="anonymous",
    integrity="sha384-ujb1lZYygJmzgSwoxRggbCHcjc0rB2XoQrxeTUQyRjrOnlCoYta87iKBWq3EsdM2")
mycss = Link(rel="stylesheet", href="picovars.css")

class NotFoundException(HTTPException):
    def __init__(self, detail=None): return super().__init__(404, detail=detail)

async def not_found(request: Request, exc: Exception):
    return HTMLResponse(content=exc.detail, status_code=exc.status_code)

app = FastHTML(hdrs=(htmxscr, picolink, mycss),
               exception_handlers={ 404: not_found, NotFoundException: not_found })

reg_re_param("static", "ico|gif|jpg|jpeg|webm|css|js")
@app.get("/{fname:path}.{ext:static}")
async def image(fname:str, ext:str): return FileResponse(f'{fname}.{ext}')
@app.get("/static/{fname:path}")
async def static(fname:str): return FileResponse(f'static/{fname}')

def mk_input(**kw): return Input(id="new-title", name="title", placeholder="New Todo", **kw)

@app.get("/")
async def get_todos(req):
    add = Form(Group(mk_input(), Button("Add")),
               hx_post="/", target_id=id_list, hx_swap="beforeend")
    card = Card(Ul(*TODO_LIST, id=id_list),
                header=add, footer=Div(id=id_curr)),
    title = 'Todo list'
    return (title, Main(H1(title), card, cls='container'))

@app.post("/")
async def add_item(todo:TodoItem):
    todo.id = len(TODO_LIST)+1
    TODO_LIST.append(todo)
    return todo, mk_input(hx_swap_oob='true')

def clr_details(): return Div(hx_swap_oob='innerHTML', id=id_curr)

@app.get("/edit/{id}")
async def edit_item(id:int): return get_editform(id)

@app.put("/")
async def update(todo: TodoItem):
    fill_dataclass(todo, find_todo(todo.id))
    return todo, clr_details()

@app.delete("/todos/{id}")
async def del_todo(id:int):
    TODO_LIST.remove(find_todo(id))
    return clr_details()

@app.get("/todos/{id}")
async def get_todo(id:int):
    todo = find_todo(id)
    btn = Button('delete', hx_delete=f'/todos/{todo.id}',
                 target_id=tid(todo.id), hx_swap="outerHTML")
    return Div(Div(todo.title), btn)

if __name__ == "__main__": uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
