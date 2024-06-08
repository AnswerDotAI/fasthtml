from fastcore.utils import *
from fasthtml.components import Script

def MarkdownJS(sel):
    src = f"""
import {{ marked }} from "https://cdn.jsdelivr.net/npm/marked/lib/marked.esm.js";
htmx.onLoad(elt => htmx.findAll(elt, "{sel}").forEach(e => e.innerHTML = marked.parse(e.textContent)));
"""
    return Script(NotStr(src), type='module')
