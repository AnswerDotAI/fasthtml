from asyncio import sleep
from fasthtml.common import *

app = FastHTML(ws_hdr=True)
rt = app.route

def mk_inp(): return Input(id='msg')
nid = 'notifications'

@rt('/')
async def get():
    cts = Div(
        Div(id=nid),
        Form(mk_inp(), id='form', ws_send=True),
        hx_ext='ws', ws_connect='/ws')
    return Titled('Websocket Test', cts)

async def on_connect(send): await send(Div('Hello, you have connected', id=nid))
async def on_disconnect( ): print('Disconnected!')

@app.ws('/ws', conn=on_connect, disconn=on_disconnect)
async def ws(msg:str, send):
    await send(Div('Hello ' + msg, id=nid))
    await sleep(2)
    return Div('Goodbye ' + msg, id=nid), mk_inp()

serve()

