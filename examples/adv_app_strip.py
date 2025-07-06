from fasthtml.common import *
from hmac import compare_digest

db = database('data/utodos.db')
class User: name:str; pwd:str
class Todo: id:int; title:str; done:bool; name:str; details:str; priority:int
users = db.create(User, pk='name')
todos = db.create(Todo, transform=True)

login_redir = RedirectResponse('/login', status_code=303)

def before(req, sess):
    auth = req.scope['auth'] = sess.get('auth', None)
    if not auth: return login_redir
    todos.xtra(name=auth)

bware = Beforeware(before, skip=[r'/favicon\.ico', r'/static/.*', r'.*\.css', '/login', '/send_login'])

def _not_found(req, exc): return Titled('Oh no!', Div('We could not find that page :('))
app,rt = fast_app(before=bware, exception_handlers={404: _not_found},
                  hdrs=(SortableJS('.sortable'), MarkdownJS()))

@rt
def login():
    frm = Form(action=send_login, method='post')(
        Input(id='name', placeholder='Name'),
        Input(id='pwd', type='password', placeholder='Password'),
        Button('login'))
    return Titled("Login", frm)

@rt
def send_login(name:str, pwd:str, sess):
    if not name or not pwd: return login_redir
    try: u = users[name]
    except NotFoundError: u = users.insert(name=name, pwd=pwd)
    if not compare_digest(u.pwd.encode("utf-8"), pwd.encode("utf-8")): return login_redir
    sess['auth'] = u.name
    return RedirectResponse('/', status_code=303)

@rt
def logout(sess):
    del sess['auth']
    return login_redir

def clr_details(): return Div(hx_swap_oob='innerHTML', id='current-todo')

@rt
def update(todo: Todo): return todos.update(todo), clr_details()

@rt
def edit(id:int):
    res = Form(hx_post=update, target_id=f'todo-{id}', id="edit")(
        Group(Input(id="title"), Button("Save")),
        Hidden(id="id"), CheckboxX(id="done", label='Done'),
        Textarea(id="details", name="details", rows=10))
    return fill_form(res, todos[id])

@rt
def rm(id:int):
    todos.delete(id)
    return clr_details()

@rt
def show(id:int):
    todo = todos[id]
    btn = Button('delete', hx_post=rm.to(id=todo.id),
                 hx_target=f'#todo-{todo.id}', hx_swap="outerHTML")
    return Div(H2(todo.title), Div(todo.details, cls="marked"), btn)

@patch
def __ft__(self:Todo):
    ashow = AX(self.title, show.to(id=self.id), 'current-todo')
    aedit = AX('edit',     edit.to(id=self.id), 'current-todo')
    dt = '✅ ' if self.done else ''
    cts = (dt, ashow, ' | ', aedit, Hidden(id="id", value=self.id), Hidden(id="priority", value="0"))
    return Li(*cts, id=f'todo-{self.id}')

@rt
def create(todo:Todo):
    new_inp =  Input(id="new-title", name="title", placeholder="New Todo", hx_swap_oob='true')
    return todos.insert(todo), new_inp

@rt
def reorder(id:list[int]):
    for i,id_ in enumerate(id): todos.update({'priority':i}, id_)
    return tuple(todos(order_by='priority'))

@rt
def index(auth):
    title = f"{auth}'s Todo list"
    top = Grid(H1(title), Div(A('logout', href=logout), style='text-align: right'))
    new_inp = Input(id="new-title", name="title", placeholder="New Todo")
    add = Form(Group(new_inp, Button("Add")),
               hx_post=create, target_id='todo-list', hx_swap="afterbegin")
    frm = Form(*todos(order_by='priority'),
               id='todo-list', cls='sortable', hx_post=reorder, hx_trigger="end")
    card = Card(P('Drag/drop todos to reorder them'),
                Ul(frm),
                header=add, footer=Div(id='current-todo'))
    return Title(title), Container(top, card)

serve()

