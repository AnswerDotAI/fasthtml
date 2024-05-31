from fasthtml.fastapp import *

def render(todo):
    show = AX(todo.title, f'/todos/{todo.id}', 'current-todo')
    edit = AX('edit',     f'/edit/{todo.id}' , 'current-todo')
    dt = ' (done)' if todo.done else ''
    return Li(show, dt, ' | ', edit, id=f'todo-{todo.id}')

app,(todos,Todo) = fast_app('todos.db', render, id=int, title=str, done=bool, pk='id')

@app["/"]
def get():
    inp = Input(id="new-title", name="title", placeholder="New Todo")
    add = Form(Group(inp, Button("Add")), hx_post="/", target_id='todo-list', hx_swap="beforeend")
    card = Card(Ul(*todos(), id='todo-list'), header=add, footer=Div(id='current-todo')),
    return 'Todo list', Main(H1('Todos'), card, cls='container')

@app["/"]
def post(todo:Todo):
    return todos.insert(todo), Input(id="new-title", name="title", placeholder="New Todo", hx_swap_oob='true')

@app["/edit/{id}"]
def get(id:int):
    res = Form(Group(Input(id="title"), Button("Save")),
        Hidden(id="id"), Checkbox(id="done", label='Done'),
        hx_put="/", target_id=f'todo-{id}', id="edit")
    return fill_form(res, todos.get(id))

@app["/"]
def put(todo: Todo): return todos.upsert(todo), clear('current-todo')

@app["/todos/{id}"]
def get(id:int):
    todo = todos.get(id)
    btn = Button('delete', hx_delete=f'/todos/{todo.id}', target_id=f'todo-{id}', hx_swap="outerHTML")
    return Div(Div(todo.title), btn)

@app["/todos/{id}"]
def delete(id:int):
    todos.delete(id)
    return clear('current-todo')

