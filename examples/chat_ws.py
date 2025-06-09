from fasthtml.common import *

app = FastHTML(exts='ws')
rt = app.route

msgs = []
@rt('/')
def home():
    return Div(hx_ext='ws', ws_connect='/ws')(
        Div(Ul(*[Li(m) for m in msgs], id='msg-list')),
        Form(Input(id='msg'), id='form', ws_send=True)
    )

async def ws(msg:str):
    msgs.append(msg)
    await send(Ul(*[Li(m) for m in msgs], id='msg-list'))

send = app.setup_ws(ws)

serve()
