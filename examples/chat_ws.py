from fasthtml.common import *

app = FastHTML(ws_hdr=True)
rt = app.route

def mk_inp(): return Input(id='msg')
nid = 'msg-list'

messages = []
@rt('/')
def home():
    return Div(
        Div(Ul(*[Li(m) for m in messages], id=nid)),
        Form(mk_inp(), id='form', ws_send=True),
        hx_ext='ws', ws_connect='/ws')

users = {}
def on_connect(ws, send):
    connection_id = str(id(ws))
    users[connection_id] = send
def on_disconnect(ws):
    connection_id = str(id(ws))
    if connection_id in users:
        users.pop(connection_id)

@app.ws('/ws', conn=on_connect, disconn=on_disconnect)
async def ws(msg:str):
    messages.append(msg)
    for u in users.values():
        await u(Ul(*[Li(m) for m in messages], id=nid))

serve()