# Run with: uvicorn user_app_sql_model:app --reload
# At signin, enter a user/pw combination and if it doesn't exist, it will be created.
from fasthtml.common import *

if __name__ == '__main__':
    # Exiting because SQLAlchemy's processes will otherwise collide
    # with the uvicorn server's processes. Have to be run externally. 
    print("Run with: uvicorn user_app_sql_model:app --reload")
    import sys; sys.exit()

try:
    from sqlmodel import SQLModel, create_engine, Session, select, Field
    from sqlalchemy.exc import NoResultFound
except ImportError:
    print("Please install sqlmodel with 'pip install sqlmodel'")
    exit()

sqlite_file_name = "data/utodos.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# db = database(sqlite_file_name)
class User(SQLModel, table=True): name:str=Field(default=None, primary_key=True); pwd:str
class Todo(SQLModel, table=True): id:int=Field(default=None, primary_key=True); title:str; done:bool=False; name:str; details:str=''


engine = create_engine(sqlite_url, echo=True)

SQLModel.metadata.create_all(engine)

id_curr = 'current-todo'
def tid(id): return f'todo-{id}'

def lookup_user(u,p):
    with Session(engine) as session:
        stmt = select(User).where(User.name == u)
        try:
            user = session.exec(stmt).one()
        except NoResultFound:
            user = User(name=u, pwd=p)
            session.add(user)
            session.commit()
            session.refresh(user)
        return user.pwd==p

authmw = user_pwd_auth(lookup_user, skip=[r'/favicon\.ico', r'/static/.*', r'.*\.css'])

# def before(auth): todos.xtra(name=auth)

# app, rt = fast_app(middleware=[authmw], before=before,
#                hdrs=(picolink,
#                      Style(':root { --pico-font-size: 100%; }')))

app, rt = fast_app(middleware=[authmw], debug=True)

@patch
def __ft__(self:Todo):
    show = AX(self.title, f'/todos/{self.id}', id_curr)
    edit = AX('edit',     f'/edit/{self.id}' , id_curr)
    dt = '✅ ' if self.done else ''
    return Li(dt, show, ' | ', edit, Hidden(id="id", value=self.id), id=tid(self.id))

def mk_input(**kw): return Input(id="new-title", name="title", placeholder="New Todo", **kw)
def clr_details(): return Div(hx_swap_oob='innerHTML', id=id_curr)

def todos(auth: str, id: int | None = None):   
    with Session(engine) as session:
        if id:
            return session.exec(select(Todo).where(Todo.name == auth).where(Todo.id == id)).one()
        return session.exec(select(Todo).where(Todo.name == auth)).all()    

@rt("/")
async def get(request, auth):

    add = Form(Group(mk_input(), Button("Add")),
               hx_post="/", target_id='todo-list', hx_swap="beforeend")
    card = Card(Ul(*todos(auth), id='todo-list'),
                header=add, footer=Div(id=id_curr)),
    top = Grid(Div(A('logout', href=basic_logout(request)), style='text-align: right'))
    return Titled(f"{auth}'s todo list", top, card)

@rt("/todos/{id}")
async def delete(id:int, auth):
    with Session(engine) as session:
        todo = session.exec(select(Todo).where(Todo.name == auth).where(Todo.id == id))
        session.delete(todo.one())
        session.commit()
    return clr_details()

@rt("/")
async def post(auth, todo:Todo):
    todo.name = auth
    with Session(engine) as session:
        session.add(todo)
        session.commit()
        session.refresh(todo)
    return todo, mk_input(hx_swap_oob='true')

@rt("/edit/{id}")
async def get(id:int, auth):
    res = Form(Group(Input(id="title"), Button("Save")),
        Hidden(id="id"), Checkbox(id="done", label='Done'),
        hx_put="/", target_id=tid(id), id="edit")
    return fill_form(res, todos(auth, id))

@rt("/")
async def put(todo: Todo):
    return todos.upsert(todo), clr_details()

@rt("/todos/{id}")
async def get(id:int, auth):
    todo = todos(auth, id)
    btn = Button('delete', hx_delete=f'/todos/{todo.id}',
                 target_id=tid(todo.id), hx_swap="outerHTML")
    return Div(Div(todo.title), btn)
