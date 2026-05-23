from fasthtml.common import *

app, rt = fast_app(htmx=False, htmx4=True)

ok = Div(
    Button("Load", hx_action="/items", hx_method="get", hx_target="#items"),
    Div(id="items", hx_config="timeout:1s"),
    Div(hx_ignore=True),
    Div(hx_on__after_init="console.log(event)"),
)
