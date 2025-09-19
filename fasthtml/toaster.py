from fastcore.xml import FT
from fasthtml.core import FtResponse
from fasthtml.components import *
from fasthtml.xtend import *

tcid='fh-toast-container'
sk = "toasts"
toast_css = """
#fh-toast-container {
    position: fixed; inset: 20px 0; z-index: 1000; max-width: 80vw;
    display: flex; flex-direction: column; align-items: center;
    gap: 10px; pointer-events: none; margin: 0 auto;
}
.fh-toast {
    background-color: #333; color: white;
    padding: 12px 28px 12px 20px; border-radius: 4px;
    text-align: center; opacity: 0.9; position: relative;
    & > * { pointer-events: auto; };
    transition: opacity 150ms ease-in-out; min-width: 400px;
    @starting-style { opacity: 0.2; };
}
.fh-toast-dismiss {
    position: absolute; top: .2em; right: .4em;
    line-height: 1rem; padding: 0 .2em .2em .2em;
    border-radius: 15%; filter:drop-shadow(0 0 1px black);
    background: inherit; color:inherit;
    transition: filter 150ms ease-in-out;
    filter:brightness(0.8); &:hover { filter:brightness(0.9); }
}
.fh-toast-info { background-color: #2196F3; }
.fh-toast-success { background-color: #4CAF50; }
.fh-toast-warning { background-color: #FF9800; }
.fh-toast-error { background-color: #F44336; }
"""

js = '''htmx.onLoad(() => {
if (!htmx.find('#fh-toast-container')) {
    const ctn = document.createElement('div');
    ctn.id = 'fh-toast-container';
    document.body.appendChild(ctn);
    }
});'''

def Toast(message: str, typ: str = "info", dismiss: bool = False, duration:int=5000):
    x_btn = Button('x', cls="fh-toast-dismiss", onclick="htmx.remove(this?.parentElement);") if dismiss else None
    return Div(Span(message), x_btn, cls=f"fh-toast fh-toast-{typ}", hx_on_transitionend=f"setTimeout(() => this?.remove(), {duration});")

def add_toast(sess, message: str, typ: str = "info", dismiss: bool = False):
    assert typ in ("info", "success", "warning", "error"), '`typ` not in ("info", "success", "warning", "error")'
    sess.setdefault(sk, []).append((message, typ, dismiss))

def render_toasts(sess):
    toasts = [Toast(msg, typ, dismiss, sess['toast_duration']) for msg, typ, dismiss in sess.pop(sk, [])]
    return Div(*toasts, id=tcid, hx_swap_oob=f'beforeend:#{tcid}')

def toast_after(resp, req, sess):
    if sk in sess and (not resp or isinstance(resp, (tuple,FT,FtResponse))):
        sess['toast_duration'] = req.app.state.toast_duration
        req.injects.append(render_toasts(sess))

def setup_toasts(app, duration=5000):
    app.state.toast_duration = duration
    app.hdrs += [Style(toast_css), Script(js)]
    app.after.append(toast_after)
