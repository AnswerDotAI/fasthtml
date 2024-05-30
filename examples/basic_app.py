from fastapp import *

app,todos,Todo = fast_app('todos.db', id=int, title=str, done=bool, pk='id')

def row(todo):
    show = AX(todo.title, f'/todos/{todo.id}', 'current-todo')
    edit = AX('edit',     f'/edit/{todo.id}' , 'current-todo')
    dt = ' (done)' if todo.done else ''
    return Li(show, dt, ' | ', edit, id=f'todo-{todo.id}')

@app["/"]
async def get():
    inp = Input(id="new-title", name="title", placeholder="New Todo")
    add = Form(Group(inp, Button("Add")),
               hx_post="/", target_id='todo-list', hx_swap="beforeend")
    rows = [row(o) for o in todos()]
    card = Card(Ul(*rows, id='todo-list'),
                header=add, footer=Div(id='current-todo')),
    return 'Todo list', Main(H1('Todos'), card, cls='container')

@app["/todos/{id}"]
async def delete(id:int):
    todos.delete(id)
    return clear('current-todo')

@app["/"]
async def post(todo:Todo):
    return (row(todos.insert(todo)),
            Input(id="new-title", name="title", placeholder="New Todo", hx_swap_oob='true'))

@app["/edit/{id}"]
async def get(id:int):
    res = Form(Group(Input(id="title"), Button("Save")),
        Hidden(id="id"), Checkbox(id="done", label='Done'),
        hx_put="/", target_id=f'todo-{id}', id="edit")
    return fill_form(res, todos.get(id))

@app["/"]
async def put(todo: Todo): return row(todos.upsert(todo)), clear('current-todo')

@app["/todos/{id}"]
async def get(id:int):
    todo = todos.get(id)
    btn = Button('delete', hx_delete=f'/todos/{todo.id}',
                 target_id=f'todo-{id}', hx_swap="outerHTML")
    return Div(Div(todo.title), btn)

