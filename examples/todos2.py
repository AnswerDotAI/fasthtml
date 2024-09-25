from fasthtml.common import *

id_curr = 'current-todo'
id_list = 'todo-list'
def tid(id): return f'todo-{id}'

@dataclass
class TodoItem():
    title: str; id: int = -1; done: bool = False
    def __ft__(self):
        show = AX(self.title, f'/todos/{self.id}', id_curr)
        edit = AX('edit',     f'/edit/{self.id}' , id_curr)
        dt = ' (done)' if self.done else ''
        return Li(show, dt, ' | ', edit, id=tid(self.id))

TODO_LIST = [TodoItem(id=0, title="Start writing todo list", done=True),
             TodoItem(id=1, title="???", done=False),
             TodoItem(id=2, title="Profit", done=False)]

app, rt = fast_app()

def mk_input(**kw): return Input(id="new-title", name="title", placeholder="New Todo", **kw)

@app.get("/")
def get_todos(req):
    add = Form(hx_post="/", target_id=id_list, hx_swap="beforeend")(
        Group(mk_input(), Button("Add"))
    )
    card = Card(Ul(*TODO_LIST, id=id_list),
                header=add, footer=Div(id=id_curr)),
    return Titled('Todo list', card)

@app.post("/")
def add_item(todo:TodoItem):
    todo.id = len(TODO_LIST)+1
    TODO_LIST.append(todo)
    return todo, mk_input(hx_swap_oob='true')

def clr_details(): return Div(hx_swap_oob='innerHTML', id=id_curr)
def find_todo(id): return next(o for o in TODO_LIST if o.id==id)

@app.get("/edit/{id}")
def edit_item(id:int):
    todo = find_todo(id)
    res = Form(hx_put="/", target_id=tid(id), id="edit")(
        Group(Input(id="title"), Button("Save")),
        Hidden(id="id"),
        CheckboxX(id="done", label='Done'),
    )
    return fill_form(res, todo)

@app.put("/")
def update(todo: TodoItem):
    fill_dataclass(todo, find_todo(todo.id))
    return todo, clr_details()

@app.delete("/todos/{id}")
def del_todo(id:int):
    TODO_LIST.remove(find_todo(id))
    return clr_details()

@app.get("/todos/{id}")
def get_todo(id:int):
    todo = find_todo(id)
    btn = Button('delete', hx_delete=f'/todos/{todo.id}',
                 target_id=tid(todo.id), hx_swap="outerHTML")
    return Div(Div(todo.title), btn)

serve()

