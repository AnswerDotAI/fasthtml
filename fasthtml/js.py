from fastcore.utils import *
from fasthtml.components import Script

def MarkdownJS(sel):
    src = """
import { marked } from "https://cdn.jsdelivr.net/npm/marked/lib/marked.esm.js";
htmx.onLoad(elt => htmx.findAll(elt, "%s").forEach(e => e.innerHTML = marked.parse(e.textContent)));
""" % sel
    return Script(NotStr(src), type='module')

def SortableJS(sel='.sortable', ghost_class='blue-background-class'):
    src = """
import {Sortable} from 'https://cdn.jsdelivr.net/npm/sortablejs/+esm';

htmx.onLoad(content => {
    content.querySelectorAll("%s").forEach(elm => {
        const s = new Sortable(elm, {
            animation: 150,
            ghostClass: '%s',
            filter: ".htmx-indicator",
            onMove: e => !e.related.classList.contains('htmx-indicator'),
            onEnd: () => s.option("disabled", true),
        });
        htmx.on("htmx:afterSwap", () => s.option("disabled", false), elm);
    });
})
""" % (sel, ghost_class)
    return Script(NotStr(src), type='module')

