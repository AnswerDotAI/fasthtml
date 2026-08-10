from fasthtml.common import *

app, rt = fast_app()

bad = Div(
    Button("Load", hx_action="/items", hx_method="get"),
    Div(hx_config="timeout:1s"),
    Div(hx_ignore=True),
)
