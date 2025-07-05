### Walkthrough of an idiomatic fasthtml app ###

# This fasthtml app includes functionality from fastcore, starlette, fastlite, and fasthtml itself.
# Run with: `python adv_app.py`
# Importing from `fasthtml.common` brings the key parts of all of these together. We recommend using a wildcard import since only necessary parts are exported by the module.
from fasthtml.common import *
from hmac import compare_digest

# We recommend using sqlite for most apps, as it is simple, fast, and scalable. `database()` creates the db if it doesn't exist.
db = database('data/utodos.db')
# Create regular classes for your database tables. There are auto-converted to fastcore flexiclasses, which are like dataclasses, but with some extra functionality.
class User: name:str; pwd:str
class Todo: id:int; title:str; done:bool; name:str; details:str; priority:int
# The `create` method creates a table in the database, if it doesn't already exist. The `pk` argument specifies the primary key for the table. If not provided, it defaults to 'id'.
users = db.create(User, pk='name')
# The `transform` argument is used to automatically update the database table, if it exists, to match the class definition. It is a simple and effective migration system for less complex needs. Use the `fastmigrate` package for more sophisticated migrations.
todos = db.create(Todo, transform=True)

# Any Starlette response class can be returned by a FastHTML route handler. In that case, FastHTML won't change it at all.
login_redir = RedirectResponse('/login', status_code=303)

# The `before` function is a *Beforeware* function. These are functions that run before a route handler is called.
def before(req, sess):
    # This sets the `auth` attribute in the request scope, and gets it from the session. The session is a Starlette session, which is a dict-like object which is cryptographically signed, so it can't be tampered with.
    # The `auth` key in the scope is automatically provided to any handler which requests it, and can not be injected by the user using query params, cookies, etc, so it should be secure to use.
    auth = req.scope['auth'] = sess.get('auth', None)
    if not auth: return login_redir
    # `xtra` adds a filter to queries and DDL statements, to ensure that the user can only see/edit their own todos.
    todos.xtra(name=auth)

# Beforeware objects require the function itself, and optionally a list of regexes to skip.
bware = Beforeware(before, skip=[r'/favicon\.ico', r'/static/.*', r'.*\.css', '/login', '/send_login'])

markdown_js = """
import { marked } from "https://cdn.jsdelivr.net/npm/marked/lib/marked.esm.js";
proc_htmx('.markdown', e => e.innerHTML = marked.parse(e.textContent));
"""

# The `FastHTML` class is a subclass of `Starlette`, so you can use any parameters that `Starlette` accepts. In addition, you can add your Beforeware here, and any headers you want included in HTML responses.
def _not_found(req, exc): return Titled('Oh no!', Div('We could not find that page :('))
app = FastHTML(before=bware,
               # These are the same as Starlette exception_handlers, except they also support `FT` results
               exception_handlers={404: _not_found},
               # PicoCSS is a simple CSS system for getting started; for more complex styling try MonsterUI (which wraps uikit and Tailwind)
               hdrs=(picolink, # PicoCSS headers
                     # Look at fasthtml/js.py to see how to add Javascript libraries to FastHTML, like this one.
                     SortableJS('.sortable'),
                     # MarkdownJS is actually provided as part of FastHTML, but we've included the js code here so that you can see how it works.
                     Script(markdown_js, type='module'))
                )
# We add `rt` as a shortcut for `app.route`, which is what we'll use to decorate our route handlers.
rt = app.route

# FastHTML uses Starlette's path syntax, and adds a `static` type which matches standard static file extensions. You can define your own regex path specifiers -- for instance this is how `static` is defined in FastHTML `reg_re_param("static", "ico|gif|jpg|jpeg|webm|css|js|woff|png|svg|mp4|webp|ttf|otf|eot|woff2|txt|xml|html")`
# Provide param to `rt` to use full Starlette route syntax.
@rt("/{fname:path}.{ext:static}", methods=['GET'])
def static_handler(fname:str, ext:str): return FileResponse(f'{fname}.{ext}')

# This function handles GET and POST requests to the `/login` path, because the name of the function automatically becomes the path for the route handler, and GET/POST are available by default. We recommend generally sticking to just these two HTTP verbs.
@rt
def login():
    # This creates a form with two input fields, and a submit button. `Input`, `Form`, etc are `FT` (fasttag) objects. FastHTML composes them from trees and auto-converts them to HTML when needed.
    # You can also use plain HTML strings in handlers and headers, which will be auto-escaped, unless you use `Safe(...string...)`. If you want other custom tags (e.g. `MyTag`), they can be auto-generated by e.g:
    #   `from fasthtml.components import MyTag`.
    # fasttag objects are callable. Calling them adds children and attributes to the tag. Therefore you can use them like this:
    frm = Form(action=send_login, method='post')(
        # Tags with a `name` attr will have `name` auto-set to the same as `id` if not provided
        Input(id='name', placeholder='Name'),
        Input(id='pwd', type='password', placeholder='Password'),
        Button('login'))
    # If a user visits the URL directly, FastHTML auto-generates a full HTML page. However, if the URL is accessed by HTMX, then one HTML partial is created for each element of the tuple.
    # To avoid this auto-generation of a full page, return a `HTML` object, or a Starlette `Response`.
    # `Titled` returns a tuple of a `Title` with the first arg and a `Container` with the rest.
    # A handler can return either a single `FT` object or string, or a tuple of them.
    # In the case of a tuple, the stringified objects are concatenated and returned to the browser. The `Title` tag has a special purpose: it sets the title of the page (this is HTMX's built in behavior for title HTML partials).
    return Titled("Login", frm)

# Handlers are passed whatever information they "request" in the URL, as keyword arguments.
# This handler is called when a POST request is made to the `/login` path. The `login` argument is an instance of the `Login` class, which has been auto-instantiated from the form data.
# There are a number of special parameter names, which will be passed useful information about the request: `session`: the Starlette session; `request`: the Starlette request; `auth`: the value of `scope['auth']`, `htmx`: the HTMX headers, if any; `app`: the FastHTML app object.
# You can also pass any string prefix of `request` or `session`.
@rt
def send_login(name:str, pwd:str, sess):
    if not name or not pwd: return login_redir
    # Indexing into a table queries by primary key, which is `name` here.
    try: u = users[name]
    # If the primary key does not exist, the method raises a `NotFoundError`. Here we use this to just generate a user -- in practice you'd probably to redirect to a signup page.
    # Note that `insert` (and all similar db methods) returns the row object, so we can use it to get the new user.
    except NotFoundError: u = users.insert(name=name, pwd=pwd)
    if not compare_digest(u.pwd.encode("utf-8"), pwd.encode("utf-8")): return login_redir
    # Because the session is signed, we can securely add information to it. It's stored in the browser cookies. If you don't pass a secret signing key to `FastHTML`, it will auto-generate one and store it in a file `./sesskey`.
    sess['auth'] = u.name
    return RedirectResponse('/', status_code=303)

@rt
def logout(sess):
    del sess['auth']
    return login_redir

# Refactoring components in FastHTML is as simple as creating Python functions. The `clr_details` function creates a Div with specific HTMX attributes.
# `hx_swap_oob='innerHTML'` tells HTMX to swap the inner HTML of the target element out-of-band, meaning it will update this element regardless of where the HTMX request originated from. This returned div is empty, so it will clear the details view.
def clr_details(): return Div(hx_swap_oob='innerHTML', id='current-todo')

# Dataclasses, dicts, namedtuples, TypedDicts, and custom classes are automatically instantiated from form data.
# In this case, the `Todo` class is a flexiblass (a subclass of dataclass), so the handler will be passed all the field names of it.
@rt
def update(todo: Todo):
    # The updated todo is returned. By returning the updated todo, we can update the list directly. Because we return a tuple with `clr_details()`, the details view is also cleared.
    # Later on, the `__ft__` method of the `Todo` class will be called to convert it to a fasttag.
    return todos.update(todo), clr_details()

@rt
def edit(id:int):
    # `target_id` specifies which element will be updated with the server's response (it's a shortcut for hx_target=f"#{...}").
    # CheckboxX add an extra hidden field with the same name as the checkbox, so that it can be submitted as part of the form data. This is useful for boolean fields, where you want to know if the field was checked or not.
    res = Form(hx_post=update, target_id=f'todo-{id}', id="edit")(
        Group(Input(id="title"), Button("Save")),
        Hidden(id="id"), CheckboxX(id="done", label='Done'),
        Textarea(id="details", name="details", rows=10))
    # `fill_form` populates the form with existing todo data, and returns the result. Indexing into a table (`todos`) queries by primary key, which is `id` here. It also includes `xtra`, so this will only return the id if it belongs to the current user.
    return fill_form(res, todos[id])

@rt
def rm(id:int):
    # `delete` removes the item with the given primary key.
    todos.delete(id)
    # Returning `clr_details()` ensures the details view is cleared after deletion, leveraging HTMX's out-of-band swap feature.
    # Note that we are not returning *any* FT component that doesn't have an "OOB" swap, so the target element inner HTML is simply deleted.
    return clr_details()

@rt
def show(id:int):
    todo = todos[id]
    # `hx_swap` determines how the update should occur. We use "outerHTML" to replace the entire todo `Li` element.
    # `rm.to(id=todo.id)` is a shortcut for `f'/rm?id={todo.id}'`. All routes have this `to` method.
    btn = Button('delete', hx_post=rm.to(id=todo.id),
                 hx_target=f'#todo-{todo.id}', hx_swap="outerHTML")
    # The "markdown" class is used here because that's the CSS selector we used in the JS earlier. This will trigger the JS to parse the markdown.
    # Because `class` is a reserved keyword in Python, we use `cls` instead, which FastHTML auto-converts.
    return Div(H2(todo.title), Div(todo.details, cls="markdown"), btn)

# `fastcore.patch` adds a method to an existing class.
# The `__ft__` method is a special method that FastHTML uses to convert the object into an `FT` object, so that it can be composed into an FT tree, and later rendered into HTML.
@patch
def __ft__(self:Todo):
    # Some FastHTML tags have an 'X' suffix, which means they're "extended" in some way. For instance, here `AX` is an extended `A` tag, which takes 3 positional arguments: `(text, hx_get, target_id)`.
    # All underscores in FT attrs are replaced with hyphens, so this will create an `hx-get` attr, which HTMX uses to trigger a GET request.
    # Generally, most of your route handlers in practice (as in this demo app) are likely to be HTMX handlers.
    ashow = AX(self.title, show.to(id=self.id), 'current-todo')
    aedit = AX('edit',     edit.to(id=self.id), 'current-todo')
    dt = '✅ ' if self.done else ''
    # FastHTML provides some shortcuts. For instance, `Hidden` is defined as simply: `return Input(type="hidden", value=value, **kwargs)`
    cts = (dt, ashow, ' | ', aedit, Hidden(id="id", value=self.id), Hidden(id="priority", value="0"))
    # Any FT object can take a list of children as positional args, and a dict of attrs as keyword args.
    return Li(*cts, id=f'todo-{self.id}')

@rt
def create(todo:Todo):
    # `hx_swap_oob='true'` tells HTMX to perform an out-of-band swap, updating this element wherever it appears. This is used to clear the input field after adding the new todo.
    new_inp =  Input(id="new-title", name="title", placeholder="New Todo", hx_swap_oob='true')
    # `insert` returns the inserted todo, which is appended to the list start, because we used `hx_swap='afterbegin'` when creating the form.
    return todos.insert(todo), new_inp

# Because the todo list form created earlier included hidden inputs with the todo IDs, they are included in the form data. By using a parameter called (e.g) "id", FastHTML will try to find something suitable in the request with this name. In order, it searches as follows: path; query; cookies; headers; session keys; form data.
# FastHTML will use your parameter's type annotation to try to cast the value to the requested type. In the case of form data, there can be multiple values with the same key. So in this case, the parameter is a list of ints.
@rt
def reorder(id:list[int]):
    # Normally running a query in a loop like this would be really slow. But sqlite is at least as fast as a file system, so this pattern is actually idiomatic and efficient.
    for i,id_ in enumerate(id): todos.update({'priority':i}, id_)
    # HTMX by default replaces the inner HTML of the calling element, which in this case is the todo list form. Therefore, we return the list of todos, now in the correct order, which will be auto-converted to FT for us.
    # In this case, it's not strictly necessary, because sortable.js has already reorder the DOM elements. However, by returning the updated data, we can be assured that there aren't sync issues between the DOM and the server.
    return tuple(todos(order_by='priority'))

# This is the handler for the main todo list application. By including the `auth` parameter, it gets passed the current username, for displaying in the title. `index()` is a special name for the main route handler, and is called when the root path `/` is accessed.
@rt
def index(auth):
    title = f"{auth}'s Todo list"
    top = Grid(H1(title), Div(A('logout', href=logout), style='text-align: right'))
    new_inp = Input(id="new-title", name="title", placeholder="New Todo")
    add = Form(Group(new_inp, Button("Add")),
               hx_post=create, target_id='todo-list', hx_swap="afterbegin")
    # Treating a table as a callable (i.e with `todos(...)` here) queries the table. Because we called `xtra` in our Beforeware, this queries the todos for the current user only.
    # We can include the todo objects directly as children of the `Form`, because the `Todo` class has `__ft__` defined. This is automatically called by FastHTML to convert the `Todo` objects into `FT` objects when needed.
    # The reason we put the todo list inside a form is so that we can use the 'sortable' js library to reorder them. That library calls the js `end` event when dragging is complete, so our trigger here causes our `/reorder` handler to be called.
    frm = Form(*todos(order_by='priority'),
               id='todo-list', cls='sortable', hx_post=reorder, hx_trigger="end")
    # We create an empty 'current-todo' Div at the bottom of our page, as a target for the details and editing views.
    card = Card(P('Drag/drop todos to reorder them'),
                Ul(frm),
                header=add, footer=Div(id='current-todo'))
    # PicoCSS uses `<Main class='container'>` page content; `Container` is a tiny function that generates that.
    return Title(title), Container(top, card)

# You do not need `if __name__ == '__main__':` in FastHTML apps, because `serve()` handles this automatically. By default it reloads the app when the source code changes.
serve()
