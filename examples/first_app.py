from fasthtml.fastapp import *

app,todos,Todo = fast_app('todos.db', id=int, title=str, done=bool, pk='id')
rt = app.route

def TodoRow(todo):
    show = A(todo.title, hx_get=f'/todos/{todo.id}')
    edit = A('edit',     hx_get=f'/edit/{todo.id}')
    dt = ' (done)' if todo.done else ''
    return Li(show, dt, ' | ', edit, id=f'todo-{todo.id}')

def home():
    inp = Input(name="title", placeholder="New Todo")
    add = Form(Group(inp, Button("Add")), hx_post="/")
    rows = map(TodoRow, todos())
    card = Card(Ul(*rows, id='todo-list'), header=add, footer=Div(id='current-todo'))
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
    grp = Group(Input(id="title"), Button("Save"))
    btn_back = Button('Back', hx_get='/')
    res = Form(grp, Hidden(id="id"), Checkbox(id="done", label='Done'), btn_back,
               hx_put="/", id="edit")
    frm = fill_form(res, todos.get(id))
    return Page('Edit Todo', frm)

@rt("/todos/{id}")
def get(id:int):
    btn_del =  Button('Delete', hx_delete='/', value=id, name="id")
    btn_back = Button('Back', hx_get='/')
    return Page('Todo details', Div(todos.get(id).title), btn_del, btn_back)

