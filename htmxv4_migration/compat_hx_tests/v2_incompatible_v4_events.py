from fasthtml.common import *

app, rt = fast_app()

bad = Div(
    hx_on__after_init="console.log(event)",
    hx_on__before_history_update="console.log(event)",
    hx_on__error="console.log(event)",
)
