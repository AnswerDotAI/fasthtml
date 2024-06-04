from fasthtml.all import *

db = database('data/utodos.db')
todos,users = db.t.todos,db.t.users
if todos not in db.t:
    users.create(name=str, pwd=str, pk='name')
    todos.create(id=int, title=str, done=bool, name=str, pk='id')
Todo,User = todos.dataclass(),users.dataclass()

id_curr = 'current-todo'
def tid(id): return f'todo-{id}'

def lookup_user(u,p):
    try: user = users[u]
    except NotFoundError: user = users.insert(name=u, pwd=p)
    return user.pwd==p

css = Style(':root { --pico-font-size: 100%; }')
authmw = user_pwd_auth(lookup_user, skip=[r'/favicon\.ico', r'/static/.*', r'.*\.css'])

def before(auth): todos.xtra(name=auth)

app = FastHTML(hdrs=(picolink, css), middleware=authmw, before=before)
rt = app.route

@rt("/{fname:path}.{ext:static}")
async def get(fname:str, ext:str): return FileResponse(f'{fname}.{ext}')

@patch
def __xt__(self:Todo):
    show = AX(self.title, f'/todos/{self.id}', id_curr)
    edit = AX('edit',     f'/edit/{self.id}' , id_curr)
    dt = ' (done)' if self.done else ''
    return Li(show, dt, ' | ', edit, id=tid(self.id))

def mk_input(**kw): return Input(id="new-title", name="title", placeholder="New Todo", **kw)
def clr_details(): return Div(hx_swap_oob='innerHTML', id=id_curr)

@rt("/")
async def get(request, auth):
    add = Form(Group(mk_input(), Button("Add")),
               hx_post="/", target_id='todo-list', hx_swap="beforeend")
    card = Card(Ul(*todos(), id='todo-list'),
                header=add, footer=Div(id=id_curr)),
    title = 'Todo list'
    top = Grid(H1(f"{auth}'s {title}"), Div(A('logout', href=basic_logout(request)), style='text-align: right'))
    return Title(title), Main(top, card, cls='container')

@rt("/todos/{id}")
async def delete(id:int):
    todos.delete(id)
    return clr_details()

@rt("/")
async def post(todo:Todo):
    return todos.insert(todo), mk_input(hx_swap_oob='true')

@rt("/edit/{id}")
async def get(id:int):
    res = Form(Group(Input(id="title"), Button("Save")),
        Hidden(id="id"), Checkbox(id="done", label='Done'),
        hx_put="/", target_id=tid(id), id="edit")
    return fill_form(res, todos[id])

@rt("/")
async def put(todo: Todo):
    return todos.upsert(todo), clr_details()

@rt("/todos/{id}")
async def get(id:int):
    todo = todos[id]
    btn = Button('delete', hx_delete=f'/todos/{todo.id}',
                 target_id=tid(todo.id), hx_swap="outerHTML")
    return Div(Div(todo.title), btn)
