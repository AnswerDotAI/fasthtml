from fasthtml.common import *

app, rt = fast_app(htmx=False, htmx4=True)

bad = Div(
    Div(hx_disabled_elt="this"),
    Div(hx_ext="ws"),
    Div(hx_history="false"),
    Div(hx_history_elt="#history"),
    Div(hx_inherit="*"),
    Div(hx_params="none"),
    Div(hx_prompt="Name?"),
    Div(hx_request="timeout:1s"),
)
