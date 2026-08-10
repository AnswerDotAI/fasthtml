from fasthtml.common import *

app, rt = fast_app(htmx=False, htmx4=True)

bad = Div(
    hx_on__after_on_load="console.log(event)",
    hx_on__before_cleanup_element="console.log(event)",
    hx_on__history_cache_miss="console.log(event)",
    hx_on__send_error="console.log(event)",
)
