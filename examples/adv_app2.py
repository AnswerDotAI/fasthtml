from fasthtml.common import *
from fasthtml.jupyter import *
from functools import partial
from dataclasses import dataclass
from hmac import compare_digest
from monsterui.all import *

db = database(':memory:')

class User: name:str; pwd:str

class Todo:
    id:int; title:str; done:bool; name:str; details:str; priority:int

db.users = db.create(User, transform=True, pk='name')
db.todos = db.create(Todo, transform=True)


def user_auth_before(req, sess):
    auth = req.scope['auth'] = sess.get('auth', None)
    if not auth: return login_redir
    db.todos.xtra(name=auth)

beforeware = Beforeware(
    user_auth_before,
    skip=[r'/favicon\.ico', r'/static/.*', r'.*\.css', r'.*\.js', '/login']
)


app, rt = fast_app(hdrs=Theme.blue.headers(),before=beforeware)

login_redir = Redirect('/login')


@rt
def index(auth):
    top = Grid(Div(A('logout', href=logout), style='text-align: right'))
    new_inp = Input(id="new-title", name="title", placeholder="New Todo")
    add = Form(Group(new_inp, Button("Add")),
               hx_post="/", target_id='todo-list', hx_swap="afterbegin")
    frm = Form(*db.todos(order_by='priority'),
               id='todo-list', cls='sortable', hx_post="/reorder", hx_trigger="end")

    card = Card(Ul(frm), header=add, footer=Div(id='current-todo'))
    return Titled(f"{auth}'s Todo list", Container(top, card))


@rt('/login')
def get():
    frm = Form(
        LabelInput("Name", name='name'),
        LabelInput("Password", name='pwd'),
        Button('login'),
        action='/login', method='post')
    return Titled("Login", frm, cls=ContainerT.sm)

@dataclass
class Login: name:str; pwd:str

@rt("/login")
def post(login:Login, sess):
    if not login.name or not login.pwd: return login_redir
    try: u = db.users[login.name]
    except NotFoundError: u = db.users.insert(login)
    if not compare_digest(u.pwd.encode("utf-8"), login.pwd.encode("utf-8")): return login_redir
    sess['auth'] = u.name
    return Redirect('/')

@app.get("/logout")
def logout(sess):
    del sess['auth']
    return login_redir    

serve()