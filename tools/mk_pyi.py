from fasthtml.common import *
from fasthtml.components import _all_
from fastcore.py2pyi import create_pyi

both_attrs = html_attrs+hx_attrs

create_pyi('../fasthtml/components.py', 'fasthtml')
create_pyi('../fasthtml/xtend.py', 'fasthtml')
with open('../fasthtml/components.pyi', 'a') as f:
    attrs_str = ', '.join(f'{t}:str|None=None' for t in both_attrs)
    f.write(f"\ndef ft_html(tag: str, *c, {attrs_str}, **kwargs): ...\n")
    f.write(f"def ft_hx(tag: str, *c, {attrs_str}, **kwargs): ...\n")
    for o in _all_:
        attrs = (['name'] if o.lower() in named else []) + both_attrs
        attrs_str = ', '.join(f'{t}:str|None=None' for t in attrs)
        f.write(f"def {o}(*c, {attrs_str}, **kwargs): ...\n")
