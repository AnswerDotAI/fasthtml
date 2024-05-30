import uvicorn
from dataclasses import dataclass
from starlette.responses import FileResponse, RedirectResponse, JSONResponse, HTMLResponse
from starlette.requests import Request
from starlette.exceptions import HTTPException
from fastcore.utils import *
from fastcore.xml import *
from fasthtml import *

from sqlite_utils import Database
from fastlite import *
from fastlite.kw import *

db = Database('todos.db')
todos = db.t.todos
if todos not in db.t: todos.create(id=int, title=str, done=bool, pk='id')
Todo = todos.dataclass()

id_curr,id_list = 'current-todo','todo-list'
def tid(id): return f'todo-{id}'

@patch
def __xt__(self:Todo):
    show = AX(self.title, f'/todos/{self.id}', id_curr)
    edit = AX('edit',     f'/edit/{self.id}' , id_curr)
    dt = ' (done)' if self.done else ''
    return Li(show, dt, ' | ', edit, id=tid(self.id))

app = FastHTML(hdrs=(picolink, Link(rel="stylesheet", href="picovars.css")))

@app.get("/{fname:path}.{ext:static}")
async def static(fname:str, ext:str): return FileResponse(f'{fname}.{ext}')

def mk_input(**kw): return Input(id="new-title", name="title", placeholder="New Todo", **kw)
def clr_details(): return Div(hx_swap_oob='innerHTML', id=id_curr)

@app.get("/")
async def get_todos():
    add = Form(Group(mk_input(), Button("Add")),
               hx_post="/", target_id=id_list, hx_swap="beforeend")
    card = Card(Ul(*todos(), id=id_list),
                header=add, footer=Div(id=id_curr)),
    title = 'Todo list'
    return title, Main(H1(title), card, cls='container')

@app.delete("/todos/{id}")
async def del_todo(id:int):
    todos.delete(id)
    return clr_details()

@app.post("/")
async def add_item(todo:Todo): return todos.insert(todo), mk_input(hx_swap_oob='true')

@app.get("/edit/{id}")
async def edit_item(id:int):
    res = Form(Group(Input(id="title"), Button("Save")),
        Hidden(id="id"), Checkbox(id="done", label='Done'),
        hx_put="/", target_id=tid(id), id="edit")
    return fill_form(res, todos.get(id))

@app.put("/")
async def update(todo: Todo): return todos.upsert(todo), clr_details()

@app.get("/todos/{id}")
async def get_todo(id:int):
    todo = todos.get(id)
    btn = Button('delete', hx_delete=f'/todos/{todo.id}',
                 target_id=tid(todo.id), hx_swap="outerHTML")
    return Div(Div(todo.title), btn)
