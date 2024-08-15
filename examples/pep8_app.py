###
# Walkthrough of an idiomatic fasthtml app, made PEP-8 et al friendly
###

# This fasthtml app includes functionality from fastcore, starlette, fastlite, and fasthtml itself.
# Run with: `python adv_app.py`
from fasthtml import common as fh
from hmac import compare_digest
from dataclasses import dataclass
from fastcore.utils import patch


class User:
    name: str
    pwd: str


class Todo:
    id: int
    title: str
    done: bool
    name: str
    details: str
    priority: int


db = fh.database('data/todos_p8.db')
users = db.create(User, pk='name')
todos = db.create(Todo)

# Any Starlette response class can be returned by a FastHTML route handler.
login_redir = fh.RedirectResponse('/login', status_code=303)


# The `before` function is a *Beforeware* function, that runs before a handler.
def before(req, sess):
    # This sets the `auth` attribute in the request scope, and gets it from the session.
    auth = req.scope['auth'] = sess.get('auth', None)
    if not auth: return login_redir
    # `xtra` is part of the MiniDataAPI spec. It adds a filter to queries and DDL statements
    todos.xtra(name=auth)


bware = fh.Beforeware(before, skip=[r'/favicon\.ico', r'/static/.*', r'.*\.css', '/login'])
# The `FastHTML` class is a subclass of `Starlette`, so you can use any parameters that `Starlette` accepts.
app, rt = fh.fast_app(before=bware, hdrs=(fh.SortableJS('.sortable'), fh.KatexMarkdownJS(sel='.markdown')))


@app.get("/login")
def login():
    # This creates a form with two input fields, and a submit button.
    frm = fh.Form(
        fh.Input(id='name', placeholder='Name'),
        fh.Input(id='pwd', type='password', placeholder='Password'),
        fh.Button('login'),
        action='/login',
        method='post'
    )
    return fh.Titled("Login", frm)


# Handlers are passed whatever information they "request" in the URL, as keyword arguments.
@dataclass
class Login:
    name: str
    pwd: str


# This handler is called when a POST request is made to the `/login` path.
@app.post("/login")
def login_post(login: Login, sess):
    if not login.name or not login.pwd: return login_redir
    # Indexing into a MiniDataAPI table queries by primary key, which is `name` here.
    try:
        u = users[login.name]
    except fh.NotFoundError:
        u = users.insert(login)
    if not compare_digest(u.pwd.encode("utf-8"), login.pwd.encode("utf-8")): return login_redir
    # Because the session is signed, we can securely add information to it.
    sess['auth'] = u.name
    return fh.RedirectResponse('/', status_code=303)


@app.get("/logout")
def logout(sess):
    del sess['auth']
    return login_redir


# FastHTML uses Starlette's path syntax, and adds a `static` type.
@app.get("/{fname:path}.{ext:static}")
async def static(fname: str, ext: str):
    return fh.FileResponse(f'{fname}.{ext}')


# The `patch` decorator, which is defined in `fastcore`, adds a method to an existing class.
# The `__ft__` method is a method that FastHTML uses to convert the object into an `FT`
@patch
def __ft__(self: Todo):
    # Some FastHTML tags have an 'X' suffix, which means they're "extended" in some way.
    show = fh.AX(self.title, f'/todos/{self.id}', 'current-todo')
    edit = fh.AX('edit', f'/edit/{self.id}', 'current-todo')
    dt = '✅ ' if self.done else ''
    cts = (dt, show, ' | ', edit, fh.Hidden(id="id", value=self.id), fh.Hidden(id="priority", value="0"))
    # Any FT object can take a list of children as positional args, and a dict of attrs as keyword args.
    return fh.Li(*cts, id=f'todo-{self.id}')


# This is the handler for the main todo list application.
@app.get("/")
def get(auth):
    title = f"{auth}'s Todo list"
    top = fh.Grid(fh.H1(title), fh.Div(fh.A('logout', href='/logout'), style='text-align: right'))
    new_inp = fh.Input(id="new-title", name="title", placeholder="New Todo")
    grp = fh.Group(new_inp, fh.Button("Add"))
    add = fh.Form(grp, hx_post="/", target_id='todo-list', hx_swap="afterbegin")
    # In the MiniDataAPI spec, treating a table as a callable (i.e with `todos(...)` here) queries the table.
    frm = fh.Form(*todos(order_by='priority'), id='todo-list', cls='sortable', hx_post="/reorder", hx_trigger="end")
    # We create an empty 'current-todo' Div at the bottom of our page, as a target for the details and editing views.
    card = fh.Card(fh.Ul(frm), header=add, footer=fh.Div(id='current-todo'))
    # PicoCSS uses `<Main class='container'>` page content; `Container` is a tiny function that generates that.
    return fh.Title(title), fh.Container(top, card)


# This is the handler for the reordering of todos.
# It's a POST request, which is used by the 'sortable' js library.
@app.post("/reorder")
def reorder(id: list[int]):
    for i, id_ in enumerate(id):
        todos.update({'priority': i}, id_)
    return tuple(todos(order_by='priority'))


def clr_details():
    return fh.Div(hx_swap_oob='innerHTML', id='current-todo')


# This route handler uses a path parameter `{id}` which is automatically parsed and passed as an int.
@app.delete("/todos/{id}")
def delete(id: int):
    todos.delete(id)
    # Returning `clr_details()` ensures the details view is cleared after deletion.
    # Note that we are not returning *any* FT component that doesn't have an "OOB" swap
    return clr_details()


@app.get("/edit/{id}")
async def edit(id: int):
    # The `hx_put` attribute tells HTMX to send a PUT request when the form is submitted.
    res = fh.Form(
        fh.Group(fh.Input(id="title"), fh.Button("Save")),
        fh.Hidden(id="id"),
        fh.CheckboxX(id="done", label='Done'),
        fh.Textarea(id="details", name="details", rows=10),
        hx_put="/",
        target_id=f'todo-{id}',
        id="edit"
    )
    # `fill_form` populates the form with existing todo data, and returns the result.
    return fh.fill_form(res, todos[id])


@app.put("/")
async def put(todo: Todo):
    return todos.upsert(todo), clr_details()


@app.post("/")
async def post(todo: Todo):
    # This is used to clear the input field after adding the new todo.
    new_inp = fh.Input(id="new-title", name="title", placeholder="New Todo", hx_swap_oob='true')
    # `insert` returns the inserted todo, which is appended to the start of the list.
    return todos.insert(todo), new_inp


@app.get("/todos/{id}")
async def get_todo(id: int):
    todo = todos[id]
    btn = fh.Button('delete', hx_delete=f'/todos/{todo.id}', target_id=f'todo-{todo.id}', hx_swap="outerHTML")
    # The "markdown" class is used here because that's the CSS selector we used in the JS earlier.
    # Because `class` is a reserved keyword in Python, we use `cls` instead, which FastHTML auto-converts.
    return fh.Div(fh.H2(todo.title), fh.Div(todo.details, cls="markdown"), btn)


fh.serve(port=8000)
