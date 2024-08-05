from fastcore.utils import *
from fasthtml.xtend import Script,jsd,Style,Link

def light_media(css): return Style('@media (prefers-color-scheme: light) {%s}' %css)
def  dark_media(css): return Style('@media (prefers-color-scheme:  dark) {%s}' %css)

marked_imp = """import { marked } from "https://cdn.jsdelivr.net/npm/marked/lib/marked.esm.js";
    import { proc_htmx } from "https://cdn.jsdelivr.net/gh/answerdotai/fasthtml-js/fasthtml.js";
"""

def MarkdownJS(sel='.marked'):
    src = "proc_htmx('%s', e => e.innerHTML = marked.parse(e.textContent));" % sel
    return Script(marked_imp+src, type='module')

def KatexMarkdownJS(sel='.marked', katex_tags='$'):
    right_tags = '\\$' if katex_tags=='$' else '\\]'
    src = """
    import katex from "https://cdn.jsdelivr.net/npm/katex/dist/katex.mjs";
    const renderInlineMath = tex => katex.renderToString(tex, {throwOnError: false, displayMode: false});
    const renderBlockMath = tex => katex.renderToString(tex, {throwOnError: false, displayMode: true});

    proc_htmx('%s', e => {
    e.innerHTML = marked.parse(e.textContent)
    .replace(/%s{2}\\n*(.+?)\\n*%s{2}/g, (_, tex) => renderBlockMath(tex))
    .replace(/%s{1}\\n*(.+?)\\n*%s{1}/g, (_, tex) => renderInlineMath(tex))
    });
    """ % (sel, "\\"+katex_tags, right_tags, "\\"+katex_tags, right_tags)
    return (Script(marked_imp+src, type='module'),
            Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css"))


def HighlightJS(sel='pre code', langs='python', light='atom-one-light', dark='atom-one-dark'):
    src = """
hljs.addPlugin(new CopyButtonPlugin());
hljs.configure({'cssSelector': '%s'});
htmx.onLoad(hljs.highlightAll);""" % sel
    hjs = 'highlightjs','cdn-release', 'build'
    hjc = 'arronhunt'  ,'highlightjs-copy', 'dist'
    if isinstance(langs, str): langs = [langs]
    langjs = [jsd(*hjs, f'languages/{lang}.min.js') for lang in langs]
    return [jsd(*hjs, f'styles/{dark}.css', typ='css', media="(prefers-color-scheme: dark)"),
            jsd(*hjs, f'styles/{light}.css', typ='css', media="(prefers-color-scheme: light)"),
            jsd(*hjs, f'highlight.min.js'),
            jsd(*hjc, 'highlightjs-copy.min.js'),
            jsd(*hjc, 'highlightjs-copy.min.css', typ='css'),
            light_media('.hljs-copy-button {background-color: #2d2b57;}'),
            *langjs, Script(src, type='module')]


def SortableJS(sel='.sortable', ghost_class='blue-background-class'):
    src = """
import {Sortable} from 'https://cdn.jsdelivr.net/npm/sortablejs/+esm';
import {proc_htmx} from "https://cdn.jsdelivr.net/gh/answerdotai/fasthtml-js/fasthtml.js";
proc_htmx('%s', Sortable.create);
""" % sel
    return Script(src, type='module')
