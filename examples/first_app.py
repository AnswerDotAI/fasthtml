from fasthtml.fastapp import *

def render(todo):
    show = AX(todo.title, f'/todos/{todo.id}', 'current-todo')
    edit = AX('edit',     f'/edit/{todo.id}' , 'current-todo')
    dt = ' (done)' if todo.done else ''
    return Li(show, dt, ' | ', edit, id=f'todo-{todo.id}')

app,todos,Todo = fast_app('todos.db', render, id=int, title=str, done=bool, pk='id')

def home():
    inp = Input(id="new-title", name="title", placeholder="New Todo")
    add = Form(Group(inp, Button("Add")), hx_post="/")
    card = Card(Ul(*todos(), id='todo-list'),
                header=add, footer=Div(id='current-todo'))
    return Title('Todo list'), Container(H1('Todos'), card)

@app["/"]
def get(): return home()

@app["/"]
def post(todo:Todo):
    todos.insert(todo)
    return home()

@app["/"]
def put(todo: Todo):
    todos.upsert(todo)
    return home()

@app["/todos/{id}"]
def delete(id:int):
    todos.delete(id)
    return home()

@app["/edit/{id}"]
def get(id:int):
    newgrp = Group(Input(id="title"), Button("Save"))
    res = Form(newgrp, Hidden(id="id"), Checkbox(id="done", label='Done'),
               hx_put="/", id="edit")
    return fill_form(res, todos.get(id))

@app["/todos/{id}"]
def get(id:int):
    btn = Button('delete', hx_delete=f'/todos/{id}', id="edit")
    return Div(Div(todos.get(id).title), btn)

