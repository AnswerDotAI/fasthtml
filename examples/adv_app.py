from dataclasses import dataclass
from fasthtml.all import *
from fasthtml.js import MarkdownJS, SortableJS
from starlette.responses import RedirectResponse
from hmac import compare_digest

db = database('data/utodos.db')
todos,users = db.t.todos,db.t.users
if todos not in db.t:
    users.create(name=str, pwd=str, pk='name')
    todos.create(id=int, title=str, done=bool, name=str, details=str, priority=int, pk='id')
Todo,User = todos.dataclass(),users.dataclass()

id_curr = 'current-todo'
def tid(id): return f'todo-{id}'
login_redir = RedirectResponse('/login', status_code=303)

def before(req, sess):
    auth = req.scope['auth'] = sess.get('auth', None)
    if not auth: return login_redir
    todos.xtra(name=auth)

app = FastHTML(before=Beforeware(before, skip=[r'/favicon\.ico', r'/static/.*', r'.*\.css', '/login']),
               hdrs=(picolink,
                     Style(':root { --pico-font-size: 100%; }'),
                     SortableJS('.sortable', 'todo-list'),
                     MarkdownJS('.markdown')))
rt = app.route

@rt("/login")
def get():
    frm = Form(
        Input(id='name', placeholder='Name'),
        Input(id='pwd', type='password', placeholder='Password'),
        Button('login'),
        action='/login', method='post')
    return Title("Login"), Main(H1('Login'), frm, cls='container')

@dataclass
class Login: name:str; pwd:str

@rt("/login")
def post(login:Login, sess):
    if not login.name or not login.pwd: return login_redir
    try: u = users[login.name]
    except NotFoundError: u = users.insert(login)
    # This compares the passwords using a constant time string comparison
    # https://sqreen.github.io/DevelopersSecurityBestPractices/timing-attack/python
    if not compare_digest(u.pwd.encode("utf-8"), login.pwd.encode("utf-8")): return login_redir
    sess['auth'] = u.name
    return RedirectResponse('/', status_code=303)

@rt("/logout")
def get(sess):
    del sess['auth']
    return login_redir

@rt("/{fname:path}.{ext:static}")
async def get(fname:str, ext:str): return FileResponse(f'{fname}.{ext}')

@patch
def __xt__(self:Todo):
    show = AX(self.title, f'/todos/{self.id}', id_curr)
    edit = AX('edit',     f'/edit/{self.id}' , id_curr)
    dt = '✅ ' if self.done else ''
    cts = (dt, show, ' | ', edit, Hidden(id="id", value=self.id), Hidden(id="priority", value="0"))
    return Li(Div(*cts, id=tid(self.id)), id=tid(self.id), hx_swap='innerHTML')

def mk_input(**kw): return Input(id="new-title", name="title", placeholder="New Todo", **kw)
def clr_details(): return Div(hx_swap_oob='innerHTML', id=id_curr)

@rt("/reorder")
def post(id:list[int]):
    for i,id_ in enumerate(id): todos.update({'priority':i}, id_)

@rt("/")
def get(request, auth):
    t = todos(order_by='priority')
    add = Form(Group(mk_input(), Button("Add")),
               hx_post="/", target_id='todo-list', hx_swap="afterbegin")
    frm = Form(*todos(order_by='priority'),
               id='todo-list', cls='sortable', hx_post="/reorder", hx_trigger="end", hx_swap="none")
    card = Card(Ul(frm), header=add, footer=Div(id=id_curr))
    title = 'Todo list'
    top = Grid(H1(f"{auth}'s {title}"), Div(A('logout', href='/logout'), style='text-align: right'))
    return Title(title), Main(top, card, cls='container')

@rt("/todos/{id}")
def delete(id:int):
    todos.delete(id)
    return clr_details()

@rt("/")
async def post(todo:Todo):
    return todos.insert(todo), mk_input(hx_swap_oob='true')

@rt("/edit/{id}")
async def get(id:int):
    res = Form(Group(Input(id="title"), Button("Save")),
        Hidden(id="id"), Checkbox(id="done", label='Done'),
        Textarea(id="details", name="details", rows=10),
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
    return Div(Div(todo.title), Div(todo.details, cls="markdown"), btn)
