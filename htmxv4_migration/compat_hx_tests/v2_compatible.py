from fasthtml.common import *

app, rt = fast_app()

ok = Div(
    Button("Load", hx_get="/items", hx_target="#items", hx_swap="innerHTML"),
    Div(id="items", hx_vals={"page": 1}),
)
