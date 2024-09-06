# Run with: python user_app.py
# At signin, enter a user/pw combination and if it doesn't exist, it will be created.
from fasthtml.common import *

db = database('data/utodos.db')
class User: name:str; pwd:str
class Todo: id:int; title:str; done:bool; name:str; details:str
users = db.create(User, pk='name')
todos = db.create(Todo)

id_curr = 'current-todo'
def tid(id): return f'todo-{id}'

def lookup_user(u,p):
    try: user = users[u]
    except NotFoundError: user = users.insert(name=u, pwd=p)
    return user.pwd==p

authmw = user_pwd_auth(lookup_user, skip=[r'/favicon\.ico', r'/static/.*', r'.*\.css'])

def before(auth): todos.xtra(name=auth)

app = FastHTML(middleware=[authmw], before=before,
               hdrs=(picolink,
                     Style(':root { --pico-font-size: 100%; }')))
rt = app.route

@rt("/{fname:path}.{ext:static}")
def get(fname:str, ext:str): return FileResponse(f'{fname}.{ext}')

@patch
def __ft__(self:Todo):
    show = AX(self.title, f'/todos/{self.id}', id_curr)
    edit = AX('edit',     f'/edit/{self.id}' , id_curr)
    dt = '✅ ' if self.done else ''
    return Li(dt, show, ' | ', edit, Hidden(id="id", value=self.id), id=tid(self.id))

def mk_input(**kw): return Input(id="new-title", name="title", placeholder="New Todo", **kw)
def clr_details(): return Div(hx_swap_oob='innerHTML', id=id_curr)

@rt("/")
def get(request, auth):
    add = Form(Group(mk_input(), Button("Add")),
               hx_post="/", target_id='todo-list', hx_swap="beforeend")
    card = Card(Ul(*todos(), id='todo-list'),
                header=add, footer=Div(id=id_curr)),
    top = Grid(Div(A('logout', href=basic_logout(request)), style='text-align: right'))
    return Titled(f"{auth}'s todo list", top, card)

@rt("/todos/{id}")
def delete(id:int):
    todos.delete(id)
    return clr_details()

@rt("/")
def post(todo:Todo):
    return todos.insert(todo), mk_input(hx_swap_oob='true')

@rt("/edit/{id}")
def get(id:int):
    res = Form(Group(Input(id="title"), Button("Save")),
        Hidden(id="id"), CheckboxX(id="done", label='Done'),
        hx_put="/", target_id=tid(id), id="edit")
    return fill_form(res, todos[id])

@rt("/")
def put(todo: Todo):
    return todos.upsert(todo), clr_details()

@rt("/todos/{id}")
def get(id:int):
    todo = todos[id]
    btn = Button('delete', hx_delete=f'/todos/{todo.id}',
                 target_id=tid(todo.id), hx_swap="outerHTML")
    return Div(Div(todo.title), btn)

serve()

