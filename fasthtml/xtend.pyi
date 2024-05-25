__all__ = ['picocss', 'picolink', 'picocondcss', 'picocondlink', 'set_pico_cls', 'A', 'AX', 'Checkbox', 'Card', 'Group', 'Search', 'Grid', 'DialogX', 'Hidden']
from html.parser import HTMLParser
from dataclasses import dataclass, asdict
from fastcore.utils import *
from fastcore.xml import *
from fastcore.meta import use_kwargs, delegates
from .components import *
try:
    from IPython import display
except ImportError:
    display = None
picocss = 'https://cdn.jsdelivr.net/npm/@picocss/pico@latest/css/pico.min.css'
picolink = Link(rel='stylesheet', href=picocss)
picocondcss = 'https://cdn.jsdelivr.net/npm/@picocss/pico@latest/css/pico.conditional.min.css'
picocondlink = Link(rel='stylesheet', href=picocondcss)

def set_pico_cls():
    ...

def A(*c, hx_get=None, target_id=None, hx_swap=None, href='#', id=None, cls=None, title=None, style=None, hx_post=None, hx_put=None, hx_delete=None, hx_patch=None, hx_trigger=None, hx_target=None, hx_include=None, hx_select=None, hx_indicator=None, hx_push_url=None, hx_confirm=None, hx_disable=None, hx_replace_url=None, hx_on=None, **kwargs):
    ...

def AX(txt, hx_get=None, target_id=None, hx_swap=None, href='#', *, id=None, cls=None, title=None, style=None, hx_post=None, hx_put=None, hx_delete=None, hx_patch=None, hx_trigger=None, hx_target=None, hx_include=None, hx_select=None, hx_indicator=None, hx_push_url=None, hx_confirm=None, hx_disable=None, hx_replace_url=None, hx_on=None, **kwargs):
    ...

def Checkbox(checked: bool=False, label=None, *, target_id=None, id=None, cls=None, title=None, style=None, hx_get=None, hx_post=None, hx_put=None, hx_delete=None, hx_patch=None, hx_trigger=None, hx_target=None, hx_swap=None, hx_include=None, hx_select=None, hx_indicator=None, hx_push_url=None, hx_confirm=None, hx_disable=None, hx_replace_url=None, hx_on=None, **kwargs):
    ...

def Card(*c, header=None, footer=None, target_id=None, id=None, cls=None, title=None, style=None, hx_get=None, hx_post=None, hx_put=None, hx_delete=None, hx_patch=None, hx_trigger=None, hx_target=None, hx_swap=None, hx_include=None, hx_select=None, hx_indicator=None, hx_push_url=None, hx_confirm=None, hx_disable=None, hx_replace_url=None, hx_on=None, **kwargs):
    ...

def Group(*c, target_id=None, id=None, cls=None, title=None, style=None, hx_get=None, hx_post=None, hx_put=None, hx_delete=None, hx_patch=None, hx_trigger=None, hx_target=None, hx_swap=None, hx_include=None, hx_select=None, hx_indicator=None, hx_push_url=None, hx_confirm=None, hx_disable=None, hx_replace_url=None, hx_on=None, **kwargs):
    ...

def Search(*c, target_id=None, id=None, cls=None, title=None, style=None, hx_get=None, hx_post=None, hx_put=None, hx_delete=None, hx_patch=None, hx_trigger=None, hx_target=None, hx_swap=None, hx_include=None, hx_select=None, hx_indicator=None, hx_push_url=None, hx_confirm=None, hx_disable=None, hx_replace_url=None, hx_on=None, **kwargs):
    ...

def Grid(*c, cls='grid', target_id=None, id=None, title=None, style=None, hx_get=None, hx_post=None, hx_put=None, hx_delete=None, hx_patch=None, hx_trigger=None, hx_target=None, hx_swap=None, hx_include=None, hx_select=None, hx_indicator=None, hx_push_url=None, hx_confirm=None, hx_disable=None, hx_replace_url=None, hx_on=None, **kwargs):
    ...

def DialogX(*c, open=None, header=None, footer=None, id=None, target_id=None, cls=None, title=None, style=None, hx_get=None, hx_post=None, hx_put=None, hx_delete=None, hx_patch=None, hx_trigger=None, hx_target=None, hx_swap=None, hx_include=None, hx_select=None, hx_indicator=None, hx_push_url=None, hx_confirm=None, hx_disable=None, hx_replace_url=None, hx_on=None, **kwargs):
    ...

def Hidden(value: str='', *, target_id=None, id=None, cls=None, title=None, style=None, hx_get=None, hx_post=None, hx_put=None, hx_delete=None, hx_patch=None, hx_trigger=None, hx_target=None, hx_swap=None, hx_include=None, hx_select=None, hx_indicator=None, hx_push_url=None, hx_confirm=None, hx_disable=None, hx_replace_url=None, hx_on=None, **kwargs):
    ...