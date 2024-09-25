from fasthtml.common import *

app = FastHTML(ws_hdr=True)
rt = app.route

msgs = []
@rt('/')
def home(): return Div(
    Div(Ul(*[Li(m) for m in msgs], id='msg-list')),
    Form(Input(id='msg'), id='form', ws_send=True),
    hx_ext='ws', ws_connect='/ws')

users = {}
def on_conn(ws, send): users[str(id(ws))] = send
def on_disconn(ws): users.pop(str(id(ws)), None)

@app.ws('/ws', conn=on_conn, disconn=on_disconn)
async def ws(msg:str):
    msgs.append(msg)
    # Use associated `send` function to send message to each user
    for u in users.values(): await u(Ul(*[Li(m) for m in msgs], id='msg-list'))

serve()