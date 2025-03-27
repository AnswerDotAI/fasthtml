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

@patch
def __ft__(self:Todo):
    # Some FastHTML tags have an 'X' suffix, which means they're "extended" in some way.
    # For instance, here `AX` is an extended `A` tag, which takes 3 positional arguments:
    # `(text, hx_get, target_id)`.
    # All underscores in FT attrs are replaced with hyphens, so this will create an `hx-get` attr,
    # which HTMX uses to trigger a GET request.
    # Generally, most of your route handlers in practice (as in this demo app) are likely to be HTMX handlers.
    # For instance, for this demo, we only have two full-page handlers: the '/login' and '/' GET handlers.
    show = AX(self.title, f'/todos/{self.id}', 'current-todo')
    edit = AX('edit',     f'/edit/{self.id}' , 'current-todo')
    dt = '✅ ' if self.done else ''
    # FastHTML provides some shortcuts. For instance, `Hidden` is defined as simply:
    # `return Input(type="hidden", value=value, **kwargs)`
    cts = (dt, show, ' | ', edit, Hidden(id="id", value=self.id), Hidden(id="priority", value="0"))
    # Any FT object can take a list of children as positional args, and a dict of attrs as keyword args.
    return Li(*cts, id=f'todo-{self.id}')

def user_auth_before(req, sess):
    auth = req.scope['auth'] = sess.get('auth', None)
    if not auth: return login_redir
    db.todos.xtra(name=auth)

beforeware = Beforeware(
    user_auth_before,
    skip=[r'/favicon\.ico', r'/static/.*', r'.*\.css', r'.*\.js', '/login']
)
app, rt = fast_app(hdrs=Theme.blue.headers()+[SortableJS('.sortable'),],before=beforeware)

# Authentication
login_redir = Redirect('/login')

@rt('/login')
def get():
    frm = Form(
        LabelInput("Name", name='name'),
        LabelInput("Password", name='pwd', type='password'),
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

@rt
def logout(sess):
    del sess['auth']
    return login_redir    

# Dashboard and control handlers
@rt
def index(auth):
    top = Grid(Div(A('logout', href=logout), style='text-align: right'))
    new_inp = Input(id="new-title", name="title", placeholder="New Todo")
    add = Form(Group(new_inp, Button("Add")),
               hx_post=add_todo, target_id='todo-list', hx_swap="afterbegin")
    frm = Form(*db.todos(order_by='priority'),
               id='todo-list', cls='sortable', hx_post=reorder, hx_trigger="end")

    card = Card(Ul(frm), header=add, footer=Div(id='current-todo'))
    return Titled(f"{auth}'s Todo list", Container(top, card))

@rt
def add_todo(todo:Todo, auth):
    new_inp =  LabelInput('Title', id="new-title", name="title", placeholder="New Todo", hx_swap_oob='true')
    # `insert` returns the inserted todo, which is appended to the start of the list, because we used
    # `hx_swap='afterbegin'` when creating the todo list form.
    return db.todos.insert(todo), new_inp

@rt
def reorder(id:list[int]):
    for i,id_ in enumerate(id): db.todos.update({'priority':i}, id_)
    # HTMX by default replaces the inner HTML of the calling element, which in this case is the todo list form.
    # Therefore, we return the list of todos, now in the correct order, which will be auto-converted to FT for us.
    # In this case, it's not strictly necessary, because sortable.js has already reorder the DOM elements.
    # However, by returning the updated data, we can be assured that there aren't sync issues between the DOM
    # and the server.
    return tuple(db.todos(order_by='priority'))


serve()