from fasthtml.common import *

def render(item:'Todo'):
    id = f'todo-{item.id}'
    dellink = AX('Delete', hx_delete=f'/todo/{item.id}', target_id=id, hx_swap='delete')
    return Li(item.task, dellink, id=id)

auth = user_pwd_auth(user='s3kret', skip=[r'/favicon\.ico', r'/static/.*', r'.*\.css'])
app,rt,todos,Todo = fast_app(
    'data/tbl.db', middleware=[auth], render=render,
    id=int, task=str, pk='id')

@rt("/")
async def get(request):
    new_frm = Form(hx_post='/', target_id='todo-list', hx_swap='beforeend')(
        Group(
            Input(name='task', placeholder='Task'),
            Button('Add')
        )
    )
    items = Ul(*todos(), id='todo-list')
    logout = A('logout', href=basic_logout(request))
    return Titled('Todo list', new_frm, items, logout)

@rt("/")
async def post(todo:Todo): return todos.insert(todo)

@rt("/todo/{id}")
async def delete(id:int): todos.delete(id)

serve()
