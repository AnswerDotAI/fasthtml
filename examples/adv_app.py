###
# Walkthrough of an idiomatic fasthtml app
###

# This fasthtml app includes functionality from fastcore, starlette, fastlite, and fasthtml itself.
# Run with: `python adv_app.py`
# Importing from `fasthtml.common` brings the key parts of all of these together.
# For simplicity, you can just `from fasthtml.common import *`:
from fasthtml.common import *
# ...or you can import everything into a namespace:
# from fasthtml import common as fh
# ...or you can import each symbol explicitly (which we're commenting out here but including for completeness):
"""
from fasthtml.common import (
    # These are the HTML components we use in this app
    A, AX, Button, Card, Checkbox, Container, Div, Form, Grid, Group, H1, H2, Hidden, Input, Li, Main, Script, Style, Textarea, Title, Titled, Ul,
    # These are FastHTML symbols we'll use
    Beforeware, fast_app, SortableJS, fill_form, picolink, serve,
    # These are from Starlette, Fastlite, fastcore, and the Python stdlib
    FileResponse, NotFoundError, RedirectResponse, database, patch, dataclass
)
"""

from hmac import compare_digest

# You can use any database you want; it'll be easier if you pick a lib that supports the MiniDataAPI spec.
# Here we are using SQLite, with the FastLite library, which supports the MiniDataAPI spec.
db = database('data/utodos.db')
# The `t` attribute is the table collection. The `todos` and `users` tables are not created if they don't exist.
# Instead, you can use the `create` method to create them if needed.
todos,users = db.t.todos,db.t.users
if todos not in db.t:
    # You can pass a dict, or kwargs, to most MiniDataAPI methods.
    users.create(dict(name=str, pwd=str), pk='name')
    todos.create(id=int, title=str, done=bool, name=str, details=str, priority=int, pk='id')
# Although you can just use dicts, it can be helpful to have types for your DB objects.
# The `dataclass` method creates that type, and stores it in the object, so it will use it for any returned items.
Todo,User = todos.dataclass(),users.dataclass()

# Any Starlette response class can be returned by a FastHTML route handler.
# In that case, FastHTML won't change it at all.
# Status code 303 is a redirect that can change POST to GET, so it's appropriate for a login page.
login_redir = RedirectResponse('/login', status_code=303)

# The `before` function is a *Beforeware* function. These are functions that run before a route handler is called.
def before(req, sess):
    # This sets the `auth` attribute in the request scope, and gets it from the session.
    # The session is a Starlette session, which is a dict-like object which is cryptographically signed,
    # so it can't be tampered with.
    # The `auth` key in the scope is automatically provided to any handler which requests it, and can not
    # be injected by the user using query params, cookies, etc, so it should be secure to use.
    auth = req.scope['auth'] = sess.get('auth', None)
    # If the session key is not there, it redirects to the login page.
    if not auth: return login_redir
    # `xtra` is part of the MiniDataAPI spec. It adds a filter to queries and DDL statements,
    # to ensure that the user can only see/edit their own todos.
    todos.xtra(name=auth)

markdown_js = """
import { marked } from "https://cdn.jsdelivr.net/npm/marked/lib/marked.esm.js";
import { proc_htmx} from "https://cdn.jsdelivr.net/gh/answerdotai/fasthtml-js/fasthtml.js";
proc_htmx('.markdown', e => e.innerHTML = marked.parse(e.textContent));
"""

# We will use this in our `exception_handlers` dict
def _not_found(req, exc): return Titled('Oh no!', Div('We could not find that page :('))

# To create a Beforeware object, we pass the function itself, and optionally a list of regexes to skip.
bware = Beforeware(before, skip=[r'/favicon\.ico', r'/static/.*', r'.*\.css', '/login'])
# The `FastHTML` class is a subclass of `Starlette`, so you can use any parameters that `Starlette` accepts.
# In addition, you can add your Beforeware here, and any headers you want included in HTML responses.
# FastHTML includes the "HTMX" and "Surreal" libraries in headers, unless you pass `default_hdrs=False`.
app = FastHTML(before=bware,
               # These are the same as Starlette exception_handlers, except they also support `FT` results
               exception_handlers={404: _not_found},
               # PicoCSS is a particularly simple CSS framework, with some basic integration built in to FastHTML.
               # `picolink` is pre-defined with the header for the PicoCSS stylesheet.
               # You can use any CSS framework you want, or none at all.
               hdrs=(picolink,
                     # `Style` is an `FT` object, which are 3-element lists consisting of:
                     # (tag_name, children_list, attrs_dict).
                     # FastHTML composes them from trees and auto-converts them to HTML when needed.
                     # You can also use plain HTML strings in handlers and headers,
                     # which will be auto-escaped, unless you use `NotStr(...string...)`.
                     Style(':root { --pico-font-size: 100%; }'),
                     # Have a look at fasthtml/js.py to see how these Javascript libraries are added to FastHTML.
                     # They are only 5-10 lines of code each, and you can add your own too.
                     SortableJS('.sortable'),
                     # MarkdownJS is actually provided as part of FastHTML, but we've included the js code here
                     # so that you can see how it works.
                     Script(markdown_js, type='module'))
                )
# We add `rt` as a shortcut for `app.route`, which is what we'll use to decorate our route handlers.
# When using `app.route` (or this shortcut), the only required argument is the path.
# The name of the decorated function (eg `get`, `post`, etc) is used as the HTTP verb for the handler.
rt = app.route

# For instance, this function handles GET requests to the `/login` path.
@rt("/login")
def get():
    # This creates a form with two input fields, and a submit button.
    # All of these components are `FT` objects. All HTML tags are provided in this form by FastHTML.
    # If you want other custom tags (e.g. `MyTag`), they can be auto-generated by e.g
    # `from fasthtml.components import MyTag`.
    # Alternatively, manually call e.g `ft(tag_name, *children, **attrs)`.
    frm = Form(
        # Tags with a `name` attr will have `name` auto-set to the same as `id` if not provided
        Input(id='name', placeholder='Name'),
        Input(id='pwd', type='password', placeholder='Password'),
        Button('login'),
        action='/login', method='post')
    # If a user visits the URL directly, FastHTML auto-generates a full HTML page.
    # However, if the URL is accessed by HTMX, then one HTML partial is created for each element of the tuple.
    # To avoid this auto-generation of a full page, return a `HTML` object, or a Starlette `Response`.
    # `Titled` returns a tuple of a `Title` with the first arg and a `Container` with the rest.
    # See the comments for `Title` later for details.
    return Titled("Login", frm)

# Handlers are passed whatever information they "request" in the URL, as keyword arguments.
# Dataclasses, dicts, namedtuples, TypedDicts, and custom classes are automatically instantiated
# from form data.
# In this case, the `Login` class is a dataclass, so the handler will be passed `name` and `pwd`.
@dataclass
class Login: name:str; pwd:str

# This handler is called when a POST request is made to the `/login` path.
# The `login` argument is an instance of the `Login` class, which has been auto-instantiated from the form data.
# There are a number of special parameter names, which will be passed useful information about the request:
# `session`: the Starlette session; `request`: the Starlette request; `auth`: the value of `scope['auth']`,
# `htmx`: the HTMX headers, if any; `app`: the FastHTML app object.
# You can also pass any string prefix of `request` or `session`.
@rt("/login")
def post(login:Login, sess):
    if not login.name or not login.pwd: return login_redir
    # Indexing into a MiniDataAPI table queries by primary key, which is `name` here.
    # It returns a dataclass object, if `dataclass()` has been called at some point, or a dict otherwise.
    try: u = users[login.name]
    # If the primary key does not exist, the method raises a `NotFoundError`.
    # Here we use this to just generate a user -- in practice you'd probably to redirect to a signup page.
    except NotFoundError: u = users.insert(login)
    # This compares the passwords using a constant time string comparison
    # https://sqreen.github.io/DevelopersSecurityBestPractices/timing-attack/python
    if not compare_digest(u.pwd.encode("utf-8"), login.pwd.encode("utf-8")): return login_redir
    # Because the session is signed, we can securely add information to it. It's stored in the browser cookies.
    # If you don't pass a secret signing key to `FastHTML`, it will auto-generate one and store it in a file `./sesskey`.
    sess['auth'] = u.name
    return RedirectResponse('/', status_code=303)

# Instead of using `app.route` (or the `rt` shortcut), you can also use `app.get`, `app.post`, etc.
# In this case, the function name is not used to determine the HTTP verb.
@app.get("/logout")
def logout(sess):
    del sess['auth']
    return login_redir

# FastHTML uses Starlette's path syntax, and adds a `static` type which matches standard static file extensions.
# You can define your own regex path specifiers -- for instance this is how `static` is defined in FastHTML
# `reg_re_param("static", "ico|gif|jpg|jpeg|webm|css|js|woff|png|svg|mp4|webp|ttf|otf|eot|woff2|txt|xml|html")`
# In this app, we only actually have one static file, which is `favicon.ico`. But it would also be needed if
# we were referencing images, CSS/JS files, etc.
# Note, this function is unnecessary, as the `fast_app()` call already includes this functionality.
# However, it's included here to show how you can define your own static file handler.
@rt("/{fname:path}.{ext:static}")
async def get(fname:str, ext:str): return FileResponse(f'{fname}.{ext}')

# The `patch` decorator, which is defined in `fastcore`, adds a method to an existing class.
# Here we are adding a method to the `Todo` class, which is returned by the `todos` table.
# The `__ft__` method is a special method that FastHTML uses to convert the object into an `FT` object,
# so that it can be composed into an FT tree, and later rendered into HTML.
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

# This is the handler for the main todo list application.
# By including the `auth` parameter, it gets passed the current username, for displaying in the title.
@rt("/")
def get(auth):
    title = f"{auth}'s Todo list"
    top = Grid(H1(title), Div(A('logout', href='/logout'), style='text-align: right'))
    # We don't normally need separate "screens" for adding or editing data. Here for instance,
    # we're using an `hx-post` to add a new todo, which is added to the start of the list (using 'afterbegin').
    new_inp = Input(id="new-title", name="title", placeholder="New Todo")
    add = Form(Group(new_inp, Button("Add")),
               hx_post="/", target_id='todo-list', hx_swap="afterbegin")
    # In the MiniDataAPI spec, treating a table as a callable (i.e with `todos(...)` here) queries the table.
    # Because we called `xtra` in our Beforeware, this queries the todos for the current user only.
    # We can include the todo objects directly as children of the `Form`, because the `Todo` class has `__ft__` defined.
    # This is automatically called by FastHTML to convert the `Todo` objects into `FT` objects when needed.
    # The reason we put the todo list inside a form is so that we can use the 'sortable' js library to reorder them.
    # That library calls the js `end` event when dragging is complete, so our trigger here causes our `/reorder`
    # handler to be called.
    frm = Form(*todos(order_by='priority'),
               id='todo-list', cls='sortable', hx_post="/reorder", hx_trigger="end")
    # We create an empty 'current-todo' Div at the bottom of our page, as a target for the details and editing views.
    card = Card(Ul(frm), header=add, footer=Div(id='current-todo'))
    # PicoCSS uses `<Main class='container'>` page content; `Container` is a tiny function that generates that.
    # A handler can return either a single `FT` object or string, or a tuple of them.
    # In the case of a tuple, the stringified objects are concatenated and returned to the browser.
    # The `Title` tag has a special purpose: it sets the title of the page.
    return Title(title), Container(top, card)

# This is the handler for the reordering of todos.
# It's a POST request, which is used by the 'sortable' js library.
# Because the todo list form created earlier included hidden inputs with the todo IDs,
# they are passed as form data. By using a parameter called (e.g) "id", FastHTML will try to find
# something suitable in the request with this name. In order, it searches as follows:
# path; query; cookies; headers; session keys; form data.
# Although all these are provided in the request as strings, FastHTML will use your parameter's type
# annotation to try to cast the value to the requested type.
# In the case of form data, there can be multiple values with the same key. So in this case,
# the parameter is a list of ints.
@rt("/reorder")
def post(id:list[int]):
    for i,id_ in enumerate(id): todos.update({'priority':i}, id_)
    # HTMX by default replaces the inner HTML of the calling element, which in this case is the todo list form.
    # Therefore, we return the list of todos, now in the correct order, which will be auto-converted to FT for us.
    # In this case, it's not strictly necessary, because sortable.js has already reorder the DOM elements.
    # However, by returning the updated data, we can be assured that there aren't sync issues between the DOM
    # and the server.
    return tuple(todos(order_by='priority'))

# Refactoring components in FastHTML is as simple as creating Python functions.
# The `clr_details` function creates a Div with specific HTMX attributes.
# `hx_swap_oob='innerHTML'` tells HTMX to swap the inner HTML of the target element out-of-band,
# meaning it will update this element regardless of where the HTMX request originated from.
def clr_details(): return Div(hx_swap_oob='innerHTML', id='current-todo')

# This route handler uses a path parameter `{id}` which is automatically parsed and passed as an int.
@rt("/todos/{id}")
def delete(id:int):
    # The `delete` method is part of the MiniDataAPI spec, removing the item with the given primary key.
    todos.delete(id)
    # Returning `clr_details()` ensures the details view is cleared after deletion,
    # leveraging HTMX's out-of-band swap feature.
    # Note that we are not returning *any* FT component that doesn't have an "OOB" swap, so the target element
    # inner HTML is simply deleted. That's why the deleted todo is removed from the list.
    return clr_details()

@rt("/edit/{id}")
async def get(id:int):
    # The `hx_put` attribute tells HTMX to send a PUT request when the form is submitted.
    # `target_id` specifies which element will be updated with the server's response.
    res = Form(Group(Input(id="title"), Button("Save")),
        Hidden(id="id"), Checkbox(id="done", label='Done'),
        Textarea(id="details", name="details", rows=10),
        hx_put="/", target_id=f'todo-{id}', id="edit")
    # `fill_form` populates the form with existing todo data, and returns the result.
    # Indexing into a table (`todos`) queries by primary key, which is `id` here. It also includes
    # `xtra`, so this will only return the id if it belongs to the current user.
    return fill_form(res, todos[id])

@rt("/")
async def put(todo: Todo):
    # `update` is part of the MiniDataAPI spec.
    # Note that the updated todo is returned. By returning the updated todo, we can update the list directly.
    # Because we return a tuple with `clr_details()`, the details view is also cleared.
    return todos.update(todo), clr_details()

@rt("/")
async def post(todo:Todo):
    # `hx_swap_oob='true'` tells HTMX to perform an out-of-band swap, updating this element wherever it appears.
    # This is used to clear the input field after adding the new todo.
    new_inp =  Input(id="new-title", name="title", placeholder="New Todo", hx_swap_oob='true')
    # `insert` returns the inserted todo, which is appended to the start of the list, because we used
    # `hx_swap='afterbegin'` when creating the todo list form.
    return todos.insert(todo), new_inp

@rt("/todos/{id}")
async def get(id:int):
    todo = todos[id]
    # `hx_swap` determines how the update should occur. We use "outerHTML" to replace the entire todo `Li` element.
    btn = Button('delete', hx_delete=f'/todos/{todo.id}',
                 target_id=f'todo-{todo.id}', hx_swap="outerHTML")
    # The "markdown" class is used here because that's the CSS selector we used in the JS earlier.
    # Therefore this will trigger the JS to parse the markdown in the details field.
    # Because `class` is a reserved keyword in Python, we use `cls` instead, which FastHTML auto-converts.
    return Div(H2(todo.title), Div(todo.details, cls="markdown"), btn)

serve()
