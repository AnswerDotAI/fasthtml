from fasthtml.common import *

app,rt,todos,Todo = fast_app('data/todos.db', id=int, task=str, done=bool, pk='id')

def TodoRow(todo):
    return Li(
        A(todo.task, href=f'/todos/{todo.id}'),
        (' (done)' if todo.done else '') + ' | ',
        A('edit',     href=f'/edit/{todo.id}'),
        id=f'todo-{todo.id}'
    )

def home():
    add = Form(
            Group(
                Input(name="task", placeholder="New Todo"),
                Button("Add")
            ), action="/", method='post'
        )
    card = Card(
                Ul(*map(TodoRow, todos()), id='todo-list'),
                header=add,
                footer=Div(id='current-todo')
            )
    return Titled('Todo list', card)

@rt("/")
def get(): return home()

@rt("/")
def post(todo:Todo):
    todos.insert(todo)
    return home()

@rt("/update")
def post(todo: Todo):
    todos.update(todo)
    return home()

@rt("/remove")
def get(id:int):
    todos.delete(id)
    return home()

@rt("/edit/{id}")
def get(id:int):
    res = Form(
            Group(
                Input(id="task"),
                Button("Save")
            ),
            Hidden(id="id"),
            CheckboxX(id="done", label='Done'),
            A('Back', href='/', role="button"),
            action="/update", id="edit", method='post'
        )
    frm = fill_form(res, todos[id])
    return Titled('Edit Todo', frm)

@rt("/todos/{id}")
def get(id:int):
    contents = Div(
        Div(todos[id].task),
        A('Delete', href=f'/remove?id={id}', role="button"),
        A('Back', href='/', role="button")
    )
    return Titled('Todo details', contents)

serve()

