from fasthtml.common import *

app = FastHTML()
rt = app.route

@rt('/')
def get():
    return 'Hello, world!'

serve()