# Run with: uvicorn first_app:app --reload
from fasthtml.fastapp import *

app,rt,todos,Todo = fast_app('data/todos.db', id=int, title=str, done=bool, pk='id')

def TodoRow(todo):
    return Li(
        A(todo.title, hx_get=f'/todos/{todo.id}'),
        (' (done)' if todo.done else '') + ' | ',
        A('edit',     hx_get=f'/edit/{todo.id}'),
        id=f'todo-{todo.id}'
    )

def home():
    add = Form(
            Group(
                Input(name="title", placeholder="New Todo"),
                Button("Add")
            ), hx_post="/"
        )
    card = Card(
                Ul(*map(TodoRow, todos()), id='todo-list'),
                header=add,
                footer=Div(id='current-todo')
            )
    return Page('Todo list', card)

@rt("/")
def get(): return home()

@rt("/")
def post(todo:Todo):
    todos.insert(todo)
    return home()

@rt("/")
def put(todo: Todo):
    todos.upsert(todo)
    return home()

@rt("/")
def delete(id:int):
    todos.delete(id)
    return home()

@rt("/edit/{id}")
def get(id:int):
    res = Form(
            Group(
                Input(id="title"),
                Button("Save")
            ),
            Hidden(id="id"),
            Checkbox(id="done", label='Done'),
            Button('Back', hx_get='/'),
            hx_put="/", id="edit"
        )
    frm = fill_form(res, todos[id])
    return Page('Edit Todo', frm)

@rt("/todos/{id}")
def get(id:int):
    contents = Div(
        Div(todos[id].title),
        Button('Delete', hx_delete='/', value=id, name="id"),
        Button('Back', hx_get='/')
    )
    return Page('Todo details', contents)

