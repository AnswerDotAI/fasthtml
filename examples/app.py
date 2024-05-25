from starlette.responses import FileResponse, RedirectResponse, JSONResponse, HTMLResponse
from fastcore.utils import *
from fastcore.xml import *
from fasthtml import *

from impl import *

htmxscr = Script(
    src="https://unpkg.com/htmx.org@1.9.12", crossorigin="anonymous",
    integrity="sha384-ujb1lZYygJmzgSwoxRggbCHcjc0rB2XoQrxeTUQyRjrOnlCoYta87iKBWq3EsdM2")
mycss = Link(rel="stylesheet", href="picovars.css")

app = FastHTML()

reg_re_param("static", "ico|gif|jpg|jpeg|webm|css|js")
@app.get("/{fname:path}.{ext:static}")
async def image(fname:str, ext:str): return FileResponse(f'{fname}.{ext}')
@app.get("/static/{fname:path}")
async def static(fname:str): return FileResponse(f'static/{fname}')

@app.get("/")
async def get_todos(req):
    return Html(
        Head(Title('TODO list'), htmxscr, picolink, mycss),
        Body(Main(H1('Todo list'), get_card(TODO_LIST), cls='container')))

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
