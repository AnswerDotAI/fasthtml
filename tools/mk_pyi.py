#!/usr/bin/env python
from fasthtml.common import *
from fasthtml.components import _all_, hx_attrs_annotations
from fastcore.py2pyi import create_pyi

#create_pyi('fasthtml/core.py', 'fasthtml')
#create_pyi('fasthtml/components.py', 'fasthtml')
#create_pyi('fasthtml/xtend.py', 'fasthtml')
#with open('fasthtml/components.pyi', 'a') as f:
#    attrs_str = ', '.join(f'{t}:Any=None' for t in hx_attrs)
#    f.write(f"\ndef ft_html(tag: str, *c, {attrs_str}, **kwargs): ...\n")
#    f.write(f"def ft_hx(tag: str, *c, {attrs_str}, **kwargs): ...\n")
#    for o in _all_:
#        attrs = (['name'] if o.lower() in named else []) + hx_attrs + evt_attrs
#        attrs_str = ', '.join(f'{t}:{"Any" if t not in hx_attrs_annotations else str(hx_attrs_annotations[t]).replace("typing.","")}=None' for t in attrs)
#        f.write(f"def {o}(*c, {attrs_str}, **kwargs): ...\n")

with open('fasthtml/core.pyi', 'r+') as f:
    methods = """
    def get(self, path:str): 
        ...

    def post(self, path:str): 
        ...

    def put(self, path:str): 
        ...

    def delete(self, path:str): 
        ...

    def patch(self, path:str): 
        ...

    def head(self, path:str): 
        ...

    def options(self, path:str): 
        ...

    def trace(self, path:str): 
        ...\n"""

    lines = f.readlines()
    for i, line in enumerate(lines):
        if line.startswith('all_meths = '):  # Add type stubs of request methods before defination of `all_meths`.
            lines.insert(i, methods)
            break
    f.seek(0)
    f.writelines(lines)
