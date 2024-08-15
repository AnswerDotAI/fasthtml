# Run with: python basic_app.py
from fasthtml.common import *

def render(todo):
    show = AX(todo.title, f'/todos/{todo.id}', 'current-todo')
    edit = AX('edit',     f'/edit/{todo.id}' , 'current-todo')
    dt = ' (done)' if todo.done else ''
    return Li(show, dt, ' | ', edit, id=f'todo-{todo.id}')

app,rt,todos,Todo = fast_app('data/todos.db', render, id=int, title=str, done=bool, pk='id')

@rt("/")
def get():
    inp = Input(id="new-title", name="title", placeholder="New Todo")
    add = Form(Group(inp, Button("Add")), hx_post="/", target_id='todo-list', hx_swap="beforeend")
    card = Card(Ul(*todos(), id='todo-list'), header=add, footer=Div(id='current-todo')),
    return Titled('Todo list', card)

@rt("/")
def post(todo:Todo):
    return todos.insert(todo), Input(id="new-title", name="title", placeholder="New Todo", hx_swap_oob='true')

@rt("/edit/{id}")
def get(id:int):
    res = Form(Group(Input(id="title"), Button("Save")),
        Hidden(id="id"), CheckboxX(id="done", label='Done'),
        hx_put="/", target_id=f'todo-{id}', id="edit")
    return fill_form(res, todos[id])

@rt("/")
def put(todo: Todo): return todos.upsert(todo), clear('current-todo')

@rt("/todos/{id}")
def get(id:int):
    todo = todos[id]
    btn = Button('delete', hx_delete=f'/todos/{todo.id}', target_id=f'todo-{id}', hx_swap="outerHTML")
    return Div(Div(todo.title), btn)

@rt("/todos/{id}")
def delete(id:int):
    todos.delete(id)
    return clear('current-todo')

serve()

