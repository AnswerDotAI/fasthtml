"""Simple extensions to standard HTML components, such as adding sensible defaults"""
__all__ = ['sid_scr', 'A', 'AX', 'Form', 'Hidden', 'CheckboxX', 'Script', 'Style', 'double_braces', 'undouble_braces', 'loose_format', 'ScriptX', 'replace_css_vars', 'StyleX', 'Nbsp', 'Surreal', 'On', 'Prev', 'Now', 'AnyNow', 'run_js', 'HtmxOn', 'jsd', 'Fragment', 'Titled', 'Socials', 'YouTubeEmbed', 'Favicon', 'clear', 'with_sid']
from dataclasses import dataclass, asdict
from typing import Any
from fastcore.utils import *
from fastcore.xtras import partial_format
from fastcore.xml import *
from fastcore.meta import use_kwargs, delegates
from .core import *
from .components import *
try:
    from IPython import display
except ImportError:
    display = None

def A(*c, hx_get=None, target_id=None, hx_swap=None, href='#', hx_vals=None, hx_target=None, id=None, cls=None, title=None, style=None, accesskey=None, contenteditable=None, dir=None, draggable=None, enterkeyhint=None, hidden=None, inert=None, inputmode=None, lang=None, popover=None, spellcheck=None, tabindex=None, translate=None, hx_post=None, hx_put=None, hx_delete=None, hx_patch=None, hx_trigger=None, hx_swap_oob=None, hx_include=None, hx_select=None, hx_select_oob=None, hx_indicator=None, hx_push_url=None, hx_confirm=None, hx_disable=None, hx_replace_url=None, hx_disabled_elt=None, hx_ext=None, hx_headers=None, hx_history=None, hx_history_elt=None, hx_inherit=None, hx_params=None, hx_preserve=None, hx_prompt=None, hx_request=None, hx_sync=None, hx_validate=None, hx_on_blur=None, hx_on_change=None, hx_on_contextmenu=None, hx_on_focus=None, hx_on_input=None, hx_on_invalid=None, hx_on_reset=None, hx_on_select=None, hx_on_submit=None, hx_on_keydown=None, hx_on_keypress=None, hx_on_keyup=None, hx_on_click=None, hx_on_dblclick=None, hx_on_mousedown=None, hx_on_mouseenter=None, hx_on_mouseleave=None, hx_on_mousemove=None, hx_on_mouseout=None, hx_on_mouseover=None, hx_on_mouseup=None, hx_on_wheel=None, hx_on__abort=None, hx_on__after_on_load=None, hx_on__after_process_node=None, hx_on__after_request=None, hx_on__after_settle=None, hx_on__after_swap=None, hx_on__before_cleanup_element=None, hx_on__before_on_load=None, hx_on__before_process_node=None, hx_on__before_request=None, hx_on__before_swap=None, hx_on__before_send=None, hx_on__before_transition=None, hx_on__config_request=None, hx_on__confirm=None, hx_on__history_cache_error=None, hx_on__history_cache_miss=None, hx_on__history_cache_miss_error=None, hx_on__history_cache_miss_load=None, hx_on__history_restore=None, hx_on__before_history_save=None, hx_on__load=None, hx_on__no_sse_source_error=None, hx_on__on_load_error=None, hx_on__oob_after_swap=None, hx_on__oob_before_swap=None, hx_on__oob_error_no_target=None, hx_on__prompt=None, hx_on__pushed_into_history=None, hx_on__replaced_in_history=None, hx_on__response_error=None, hx_on__send_abort=None, hx_on__send_error=None, hx_on__sse_error=None, hx_on__sse_open=None, hx_on__swap_error=None, hx_on__target_error=None, hx_on__timeout=None, hx_on__validation_validate=None, hx_on__validation_failed=None, hx_on__validation_halted=None, hx_on__xhr_abort=None, hx_on__xhr_loadend=None, hx_on__xhr_loadstart=None, hx_on__xhr_progress=None, **kwargs) -> FT:
    """An A tag; `href` defaults to '#' for more concise use with HTMX"""
    ...

def AX(txt, hx_get=None, target_id=None, hx_swap=None, href='#', *, hx_vals=None, hx_target=None, id=None, cls=None, title=None, style=None, accesskey=None, contenteditable=None, dir=None, draggable=None, enterkeyhint=None, hidden=None, inert=None, inputmode=None, lang=None, popover=None, spellcheck=None, tabindex=None, translate=None, hx_post=None, hx_put=None, hx_delete=None, hx_patch=None, hx_trigger=None, hx_swap_oob=None, hx_include=None, hx_select=None, hx_select_oob=None, hx_indicator=None, hx_push_url=None, hx_confirm=None, hx_disable=None, hx_replace_url=None, hx_disabled_elt=None, hx_ext=None, hx_headers=None, hx_history=None, hx_history_elt=None, hx_inherit=None, hx_params=None, hx_preserve=None, hx_prompt=None, hx_request=None, hx_sync=None, hx_validate=None, hx_on_blur=None, hx_on_change=None, hx_on_contextmenu=None, hx_on_focus=None, hx_on_input=None, hx_on_invalid=None, hx_on_reset=None, hx_on_select=None, hx_on_submit=None, hx_on_keydown=None, hx_on_keypress=None, hx_on_keyup=None, hx_on_click=None, hx_on_dblclick=None, hx_on_mousedown=None, hx_on_mouseenter=None, hx_on_mouseleave=None, hx_on_mousemove=None, hx_on_mouseout=None, hx_on_mouseover=None, hx_on_mouseup=None, hx_on_wheel=None, hx_on__abort=None, hx_on__after_on_load=None, hx_on__after_process_node=None, hx_on__after_request=None, hx_on__after_settle=None, hx_on__after_swap=None, hx_on__before_cleanup_element=None, hx_on__before_on_load=None, hx_on__before_process_node=None, hx_on__before_request=None, hx_on__before_swap=None, hx_on__before_send=None, hx_on__before_transition=None, hx_on__config_request=None, hx_on__confirm=None, hx_on__history_cache_error=None, hx_on__history_cache_miss=None, hx_on__history_cache_miss_error=None, hx_on__history_cache_miss_load=None, hx_on__history_restore=None, hx_on__before_history_save=None, hx_on__load=None, hx_on__no_sse_source_error=None, hx_on__on_load_error=None, hx_on__oob_after_swap=None, hx_on__oob_before_swap=None, hx_on__oob_error_no_target=None, hx_on__prompt=None, hx_on__pushed_into_history=None, hx_on__replaced_in_history=None, hx_on__response_error=None, hx_on__send_abort=None, hx_on__send_error=None, hx_on__sse_error=None, hx_on__sse_open=None, hx_on__swap_error=None, hx_on__target_error=None, hx_on__timeout=None, hx_on__validation_validate=None, hx_on__validation_failed=None, hx_on__validation_halted=None, hx_on__xhr_abort=None, hx_on__xhr_loadend=None, hx_on__xhr_loadstart=None, hx_on__xhr_progress=None, **kwargs) -> FT:
    """An A tag with just one text child, allowing hx_get, target_id, and hx_swap to be positional params"""
    ...

def Form(*c, enctype='multipart/form-data', target_id=None, hx_vals=None, hx_target=None, id=None, cls=None, title=None, style=None, accesskey=None, contenteditable=None, dir=None, draggable=None, enterkeyhint=None, hidden=None, inert=None, inputmode=None, lang=None, popover=None, spellcheck=None, tabindex=None, translate=None, hx_get=None, hx_post=None, hx_put=None, hx_delete=None, hx_patch=None, hx_trigger=None, hx_swap=None, hx_swap_oob=None, hx_include=None, hx_select=None, hx_select_oob=None, hx_indicator=None, hx_push_url=None, hx_confirm=None, hx_disable=None, hx_replace_url=None, hx_disabled_elt=None, hx_ext=None, hx_headers=None, hx_history=None, hx_history_elt=None, hx_inherit=None, hx_params=None, hx_preserve=None, hx_prompt=None, hx_request=None, hx_sync=None, hx_validate=None, hx_on_blur=None, hx_on_change=None, hx_on_contextmenu=None, hx_on_focus=None, hx_on_input=None, hx_on_invalid=None, hx_on_reset=None, hx_on_select=None, hx_on_submit=None, hx_on_keydown=None, hx_on_keypress=None, hx_on_keyup=None, hx_on_click=None, hx_on_dblclick=None, hx_on_mousedown=None, hx_on_mouseenter=None, hx_on_mouseleave=None, hx_on_mousemove=None, hx_on_mouseout=None, hx_on_mouseover=None, hx_on_mouseup=None, hx_on_wheel=None, hx_on__abort=None, hx_on__after_on_load=None, hx_on__after_process_node=None, hx_on__after_request=None, hx_on__after_settle=None, hx_on__after_swap=None, hx_on__before_cleanup_element=None, hx_on__before_on_load=None, hx_on__before_process_node=None, hx_on__before_request=None, hx_on__before_swap=None, hx_on__before_send=None, hx_on__before_transition=None, hx_on__config_request=None, hx_on__confirm=None, hx_on__history_cache_error=None, hx_on__history_cache_miss=None, hx_on__history_cache_miss_error=None, hx_on__history_cache_miss_load=None, hx_on__history_restore=None, hx_on__before_history_save=None, hx_on__load=None, hx_on__no_sse_source_error=None, hx_on__on_load_error=None, hx_on__oob_after_swap=None, hx_on__oob_before_swap=None, hx_on__oob_error_no_target=None, hx_on__prompt=None, hx_on__pushed_into_history=None, hx_on__replaced_in_history=None, hx_on__response_error=None, hx_on__send_abort=None, hx_on__send_error=None, hx_on__sse_error=None, hx_on__sse_open=None, hx_on__swap_error=None, hx_on__target_error=None, hx_on__timeout=None, hx_on__validation_validate=None, hx_on__validation_failed=None, hx_on__validation_halted=None, hx_on__xhr_abort=None, hx_on__xhr_loadend=None, hx_on__xhr_loadstart=None, hx_on__xhr_progress=None, **kwargs) -> FT:
    """A Form tag; identical to plain `ft_hx` version except default `enctype='multipart/form-data'`"""
    ...

def Hidden(value: Any='', id: Any=None, *, target_id=None, hx_vals=None, hx_target=None, cls=None, title=None, style=None, accesskey=None, contenteditable=None, dir=None, draggable=None, enterkeyhint=None, hidden=None, inert=None, inputmode=None, lang=None, popover=None, spellcheck=None, tabindex=None, translate=None, hx_get=None, hx_post=None, hx_put=None, hx_delete=None, hx_patch=None, hx_trigger=None, hx_swap=None, hx_swap_oob=None, hx_include=None, hx_select=None, hx_select_oob=None, hx_indicator=None, hx_push_url=None, hx_confirm=None, hx_disable=None, hx_replace_url=None, hx_disabled_elt=None, hx_ext=None, hx_headers=None, hx_history=None, hx_history_elt=None, hx_inherit=None, hx_params=None, hx_preserve=None, hx_prompt=None, hx_request=None, hx_sync=None, hx_validate=None, hx_on_blur=None, hx_on_change=None, hx_on_contextmenu=None, hx_on_focus=None, hx_on_input=None, hx_on_invalid=None, hx_on_reset=None, hx_on_select=None, hx_on_submit=None, hx_on_keydown=None, hx_on_keypress=None, hx_on_keyup=None, hx_on_click=None, hx_on_dblclick=None, hx_on_mousedown=None, hx_on_mouseenter=None, hx_on_mouseleave=None, hx_on_mousemove=None, hx_on_mouseout=None, hx_on_mouseover=None, hx_on_mouseup=None, hx_on_wheel=None, hx_on__abort=None, hx_on__after_on_load=None, hx_on__after_process_node=None, hx_on__after_request=None, hx_on__after_settle=None, hx_on__after_swap=None, hx_on__before_cleanup_element=None, hx_on__before_on_load=None, hx_on__before_process_node=None, hx_on__before_request=None, hx_on__before_swap=None, hx_on__before_send=None, hx_on__before_transition=None, hx_on__config_request=None, hx_on__confirm=None, hx_on__history_cache_error=None, hx_on__history_cache_miss=None, hx_on__history_cache_miss_error=None, hx_on__history_cache_miss_load=None, hx_on__history_restore=None, hx_on__before_history_save=None, hx_on__load=None, hx_on__no_sse_source_error=None, hx_on__on_load_error=None, hx_on__oob_after_swap=None, hx_on__oob_before_swap=None, hx_on__oob_error_no_target=None, hx_on__prompt=None, hx_on__pushed_into_history=None, hx_on__replaced_in_history=None, hx_on__response_error=None, hx_on__send_abort=None, hx_on__send_error=None, hx_on__sse_error=None, hx_on__sse_open=None, hx_on__swap_error=None, hx_on__target_error=None, hx_on__timeout=None, hx_on__validation_validate=None, hx_on__validation_failed=None, hx_on__validation_halted=None, hx_on__xhr_abort=None, hx_on__xhr_loadend=None, hx_on__xhr_loadstart=None, hx_on__xhr_progress=None, **kwargs) -> FT:
    """An Input of type 'hidden'"""
    ...

def CheckboxX(checked: bool=False, label=None, value='1', id=None, name=None, *, target_id=None, hx_vals=None, hx_target=None, cls=None, title=None, style=None, accesskey=None, contenteditable=None, dir=None, draggable=None, enterkeyhint=None, hidden=None, inert=None, inputmode=None, lang=None, popover=None, spellcheck=None, tabindex=None, translate=None, hx_get=None, hx_post=None, hx_put=None, hx_delete=None, hx_patch=None, hx_trigger=None, hx_swap=None, hx_swap_oob=None, hx_include=None, hx_select=None, hx_select_oob=None, hx_indicator=None, hx_push_url=None, hx_confirm=None, hx_disable=None, hx_replace_url=None, hx_disabled_elt=None, hx_ext=None, hx_headers=None, hx_history=None, hx_history_elt=None, hx_inherit=None, hx_params=None, hx_preserve=None, hx_prompt=None, hx_request=None, hx_sync=None, hx_validate=None, hx_on_blur=None, hx_on_change=None, hx_on_contextmenu=None, hx_on_focus=None, hx_on_input=None, hx_on_invalid=None, hx_on_reset=None, hx_on_select=None, hx_on_submit=None, hx_on_keydown=None, hx_on_keypress=None, hx_on_keyup=None, hx_on_click=None, hx_on_dblclick=None, hx_on_mousedown=None, hx_on_mouseenter=None, hx_on_mouseleave=None, hx_on_mousemove=None, hx_on_mouseout=None, hx_on_mouseover=None, hx_on_mouseup=None, hx_on_wheel=None, hx_on__abort=None, hx_on__after_on_load=None, hx_on__after_process_node=None, hx_on__after_request=None, hx_on__after_settle=None, hx_on__after_swap=None, hx_on__before_cleanup_element=None, hx_on__before_on_load=None, hx_on__before_process_node=None, hx_on__before_request=None, hx_on__before_swap=None, hx_on__before_send=None, hx_on__before_transition=None, hx_on__config_request=None, hx_on__confirm=None, hx_on__history_cache_error=None, hx_on__history_cache_miss=None, hx_on__history_cache_miss_error=None, hx_on__history_cache_miss_load=None, hx_on__history_restore=None, hx_on__before_history_save=None, hx_on__load=None, hx_on__no_sse_source_error=None, hx_on__on_load_error=None, hx_on__oob_after_swap=None, hx_on__oob_before_swap=None, hx_on__oob_error_no_target=None, hx_on__prompt=None, hx_on__pushed_into_history=None, hx_on__replaced_in_history=None, hx_on__response_error=None, hx_on__send_abort=None, hx_on__send_error=None, hx_on__sse_error=None, hx_on__sse_open=None, hx_on__swap_error=None, hx_on__target_error=None, hx_on__timeout=None, hx_on__validation_validate=None, hx_on__validation_failed=None, hx_on__validation_halted=None, hx_on__xhr_abort=None, hx_on__xhr_loadend=None, hx_on__xhr_loadstart=None, hx_on__xhr_progress=None, **kwargs) -> FT:
    """A Checkbox optionally inside a Label, preceded by a `Hidden` with matching name"""
    ...

def Script(code: str='', *, id=None, cls=None, title=None, style=None, attrmap=None, valmap=None, ft_cls=None, **kwargs) -> FT:
    """A Script tag that doesn't escape its code"""
    ...

def Style(*c, id=None, cls=None, title=None, style=None, attrmap=None, valmap=None, ft_cls=None, **kwargs) -> FT:
    """A Style tag that doesn't escape its code"""
    ...

def double_braces(s):
    """Convert single braces to double braces if next to special chars or newline"""
    ...

def undouble_braces(s):
    """Convert double braces to single braces if next to special chars or newline"""
    ...

def loose_format(s, **kw):
    """String format `s` using `kw`, without being strict about braces outside of template params"""
    ...

def ScriptX(fname, src=None, nomodule=None, type=None, _async=None, defer=None, charset=None, crossorigin=None, integrity=None, **kw):
    """A `script` element with contents read from `fname`"""
    ...

def replace_css_vars(css, pre='tpl', **kwargs):
    """Replace `var(--)` CSS variables with `kwargs` if name prefix matches `pre`"""
    ...

def StyleX(fname, **kw):
    """A `style` element with contents read from `fname` and variables replaced from `kw`"""
    ...

def Nbsp():
    """A non-breaking space"""
    ...

def Surreal(code: str):
    """Wrap `code` in `domReadyExecute` and set `m=me()` and `p=me('-')`"""
    ...

def On(code: str, event: str='click', sel: str='', me=True):
    """An async surreal.js script block event handler for `event` on selector `sel,p`, making available parent `p`, event `ev`, and target `e`"""
    ...

def Prev(code: str, event: str='click'):
    """An async surreal.js script block event handler for `event` on previous sibling, with same vars as `On`"""
    ...

def Now(code: str, sel: str=''):
    """An async surreal.js script block on selector `me(sel)`"""
    ...

def AnyNow(sel: str, code: str):
    """An async surreal.js script block on selector `any(sel)`"""
    ...

def run_js(js, id=None, **kw):
    """Run `js` script, auto-generating `id` based on name of caller if needed, and js-escaping any `kw` params"""
    ...

def HtmxOn(eventname: str, code: str):
    ...

def jsd(org, repo, root, path, prov='gh', typ='script', ver=None, esm=False, **kwargs) -> FT:
    """jsdelivr `Script` or CSS `Link` tag, or URL"""
    ...

class Fragment(FT):
    """An empty tag, used as a container"""

    def __init__(self, *c):
        ...

def Titled(title: str='FastHTML app', *args, cls='container', target_id=None, hx_vals=None, hx_target=None, id=None, style=None, accesskey=None, contenteditable=None, dir=None, draggable=None, enterkeyhint=None, hidden=None, inert=None, inputmode=None, lang=None, popover=None, spellcheck=None, tabindex=None, translate=None, hx_get=None, hx_post=None, hx_put=None, hx_delete=None, hx_patch=None, hx_trigger=None, hx_swap=None, hx_swap_oob=None, hx_include=None, hx_select=None, hx_select_oob=None, hx_indicator=None, hx_push_url=None, hx_confirm=None, hx_disable=None, hx_replace_url=None, hx_disabled_elt=None, hx_ext=None, hx_headers=None, hx_history=None, hx_history_elt=None, hx_inherit=None, hx_params=None, hx_preserve=None, hx_prompt=None, hx_request=None, hx_sync=None, hx_validate=None, hx_on_blur=None, hx_on_change=None, hx_on_contextmenu=None, hx_on_focus=None, hx_on_input=None, hx_on_invalid=None, hx_on_reset=None, hx_on_select=None, hx_on_submit=None, hx_on_keydown=None, hx_on_keypress=None, hx_on_keyup=None, hx_on_click=None, hx_on_dblclick=None, hx_on_mousedown=None, hx_on_mouseenter=None, hx_on_mouseleave=None, hx_on_mousemove=None, hx_on_mouseout=None, hx_on_mouseover=None, hx_on_mouseup=None, hx_on_wheel=None, hx_on__abort=None, hx_on__after_on_load=None, hx_on__after_process_node=None, hx_on__after_request=None, hx_on__after_settle=None, hx_on__after_swap=None, hx_on__before_cleanup_element=None, hx_on__before_on_load=None, hx_on__before_process_node=None, hx_on__before_request=None, hx_on__before_swap=None, hx_on__before_send=None, hx_on__before_transition=None, hx_on__config_request=None, hx_on__confirm=None, hx_on__history_cache_error=None, hx_on__history_cache_miss=None, hx_on__history_cache_miss_error=None, hx_on__history_cache_miss_load=None, hx_on__history_restore=None, hx_on__before_history_save=None, hx_on__load=None, hx_on__no_sse_source_error=None, hx_on__on_load_error=None, hx_on__oob_after_swap=None, hx_on__oob_before_swap=None, hx_on__oob_error_no_target=None, hx_on__prompt=None, hx_on__pushed_into_history=None, hx_on__replaced_in_history=None, hx_on__response_error=None, hx_on__send_abort=None, hx_on__send_error=None, hx_on__sse_error=None, hx_on__sse_open=None, hx_on__swap_error=None, hx_on__target_error=None, hx_on__timeout=None, hx_on__validation_validate=None, hx_on__validation_failed=None, hx_on__validation_halted=None, hx_on__xhr_abort=None, hx_on__xhr_loadend=None, hx_on__xhr_loadstart=None, hx_on__xhr_progress=None, **kwargs) -> FT:
    """An HTML partial containing a `Title`, and `H1`, and any provided children"""
    ...

def Socials(title, site_name, description, image, url=None, w=1200, h=630, twitter_site=None, creator=None, card='summary'):
    """OG and Twitter social card headers"""
    ...

def YouTubeEmbed(video_id: str, *, width: int=560, height: int=315, start_time: int=0, no_controls: bool=False, title: str='YouTube video player', cls: str='', **kwargs):
    """Embed a YouTube video"""
    ...

def Favicon(light_icon, dark_icon):
    """Light and dark favicon headers"""
    ...

def clear(id):
    ...
sid_scr = Script('\nfunction uuid() {\n    return [...crypto.getRandomValues(new Uint8Array(10))].map(b=>b.toString(36)).join(\'\');\n}\n\nsessionStorage.setItem("sid", sessionStorage.getItem("sid") || uuid());\n\nhtmx.on("htmx:configRequest", (e) => {\n    const sid = sessionStorage.getItem("sid");\n    if (sid) {\n        const url = new URL(e.detail.path, window.location.origin);\n        url.searchParams.set(\'sid\', sid);\n        e.detail.path = url.pathname + url.search;\n    }\n});\n')

def with_sid(app, dest, path='/'):
    ...