from fasthtml.core import *
from fasthtml.components import *
from fasthtml.xtend import *

tcid = 'toast-container'
sk = "toasts"
toast_css = """
.toast-container {
    position: fixed; top: 20px; left: 50%; transform: translateX(-50%); z-index: 1000;
    display: flex; flex-direction: column; align-items: center; width: 100%;
    pointer-events: none; opacity: 0; transition: opacity 0.3s ease-in-out;
}
.toast {
    background-color: #333; color: white;
    padding: 12px 20px; border-radius: 4px; margin-bottom: 10px;
    max-width: 80%; width: auto; text-align: center;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
.toast-info { background-color: #2196F3; }
.toast-success { background-color: #4CAF50; }
.toast-warning { background-color: #FF9800; }
.toast-error { background-color: #F44336; }
"""

toast_js = """
export function proc_htmx(sel, func) {
  htmx.onLoad(elt => {
    const elements = any(sel, elt);
    if (elt.matches && elt.matches(sel)) elements.unshift(elt);
    elements.forEach(func);
  });
}
proc_htmx('.toast-container', async function(toast) {
    await sleep(100);
    toast.style.opacity = '0.8';
    await sleep(3000);
    toast.style.opacity = '0';
    await sleep(300);
    toast.remove();
});
"""

def add_toast(sess, message, typ="info"):
    assert typ in ("info", "success", "warning", "error"), '`typ` not in ("info", "success", "warning", "error")'
    sess.setdefault(sk, []).append((message, typ))

def render_toasts(sess):
    toasts = [Div(msg, cls=f"toast toast-{typ}") for msg,typ in sess.pop(sk, [])]
    return Div(Div(*toasts, cls="toast-container"),
               hx_swap_oob="afterbegin:body")

def toast_after(resp, req, sess):
    if sk in sess: req.injects.append(render_toasts(sess))

def setup_toasts(app):
    app.router.hdrs += (Style(toast_css), Script(toast_js, type="module"))
    app.router.after.append(toast_after)

