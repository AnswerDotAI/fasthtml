from fastcore.utils import *
from fasthtml.xtend import ScriptX,jsd

def MarkdownJS(sel='.marked'):
    src = """
import { marked } from "https://cdn.jsdelivr.net/npm/marked/lib/marked.esm.js";
htmx.onLoad(elt => htmx.findAll(elt, "%s").forEach(e => e.innerHTML = marked.parse(e.textContent)));
""" % sel
    return ScriptX(src, type='module')


def HighlightJS(sel='pre code', langs='python', light='atom-one-light', dark='atom-one-dark'):
    if isinstance(langs, str): langs = [langs]
    src = """
hljs.addPlugin(new CopyButtonPlugin());
hljs.configure({'cssSelector': '%s'});
htmx.onLoad(hljs.highlightAll);""" % sel

    hjs = 'highlightjs','cdn-release', 'build'
    hjc = 'arronhunt'  ,'highlightjs-copy', 'dist'
    langjs = [jsd(*hjs, f'languages/{lang}.min.js') for lang in langs]
    return [jsd(*hjs, f'styles/{dark}.css', typ='css', media="(prefers-color-scheme: dark)"),
            jsd(*hjs, f'styles/{light}.css', typ='css', media="(prefers-color-scheme: light)"),
            jsd(*hjs, f'highlight.min.js'),
            jsd(*hjc, 'highlightjs-copy.min.js'),
            jsd(*hjc, 'highlightjs-copy.min.css', typ='css'),
            *langjs, ScriptX(src, type='module')]


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
    return ScriptX(src, type='module')

