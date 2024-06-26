# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/01_components.ipynb.

# %% auto 0
__all__ = ['voids', 'named', 'html_attrs', 'hx_attrs', 'show', 'xt_html', 'xt_hx', 'fill_form', 'fill_dataclass', 'find_inputs',
           'html2xt', 'A', 'Abbr', 'Address', 'Area', 'Article', 'Aside', 'Audio', 'B', 'Base', 'Bdi', 'Bdo',
           'Blockquote', 'Body', 'Br', 'Button', 'Canvas', 'Caption', 'Cite', 'Code', 'Col', 'Colgroup', 'Data',
           'Datalist', 'Dd', 'Del', 'Details', 'Dfn', 'Dialog', 'Div', 'Dl', 'Dt', 'Em', 'Embed', 'Fencedframe',
           'Fieldset', 'Figcaption', 'Figure', 'Footer', 'Form', 'H1', 'Head', 'Header', 'Hgroup', 'Hr', 'Html', 'I',
           'Iframe', 'Img', 'Input', 'Ins', 'Kbd', 'Label', 'Legend', 'Li', 'Link', 'Main', 'Map', 'Mark', 'Menu',
           'Meta', 'Meter', 'Nav', 'Noscript', 'Object', 'Ol', 'Optgroup', 'Option', 'Output', 'P', 'Picture',
           'PortalExperimental', 'Pre', 'Progress', 'Q', 'Rp', 'Rt', 'Ruby', 'S', 'Samp', 'Script', 'Search', 'Section',
           'Select', 'Slot', 'Small', 'Source', 'Span', 'Strong', 'Style', 'Sub', 'Summary', 'Sup', 'Table', 'Tbody',
           'Td', 'Template', 'Textarea', 'Tfoot', 'Th', 'Thead', 'Time', 'Title', 'Tr', 'Track', 'U', 'Ul', 'Var',
           'Video', 'Wbr']

# %% ../nbs/01_components.ipynb 2
from dataclasses import dataclass, asdict, is_dataclass, make_dataclass, replace, astuple, MISSING

from bs4 import BeautifulSoup

from fastcore.utils import *
from fastcore.xml import *
from fastcore.meta import use_kwargs, delegates

try: from IPython import display
except ImportError: display=None

# %% ../nbs/01_components.ipynb 4
def show(xt,*rest):
    if rest: xt = (xt,)+rest
    return display.HTML(to_xml(xt))

# %% ../nbs/01_components.ipynb 5
voids = set('area base br col command embed hr img input keygen link meta param source track wbr !doctype'.split())
named = set('a button form frame iframe img input map meta object param select textarea'.split())
html_attrs = 'id cls title style accesskey contenteditable dir draggable enterkeyhint hidden inert inputmode lang popover spellcheck tabindex translate'.split()
hx_attrs = 'get post put delete patch trigger target swap include select indicator push_url confirm disable replace_url on'
hx_attrs = html_attrs + [f'hx_{o}' for o in hx_attrs.split()]

# %% ../nbs/01_components.ipynb 6
def xt_html(tag: str, *c, id=None, cls=None, title=None, style=None, **kwargs):
    kwargs['id'],kwargs['cls'],kwargs['title'],kwargs['style'] = id,cls,title,style
    tag,c,kw = xt(tag, *c, **kwargs)
    if tag in named and 'id' in kw and 'name' not in kw: kw['name'] = kw['id']
    return XT(tag,c,kw, void_=tag in voids)

# %% ../nbs/01_components.ipynb 7
@use_kwargs(hx_attrs, keep=True)
def xt_hx(tag: str, *c, target_id=None, **kwargs):
    if target_id: kwargs['hx_target'] = '#'+target_id
    return xt_html(tag, *c, **kwargs)

# %% ../nbs/01_components.ipynb 8
_g = globals()
_all_ = [
    'A', 'Abbr', 'Address', 'Area', 'Article', 'Aside', 'Audio', 'B', 'Base', 'Bdi', 'Bdo', 'Blockquote', 'Body', 'Br',
    'Button', 'Canvas', 'Caption', 'Cite', 'Code', 'Col', 'Colgroup', 'Data', 'Datalist', 'Dd', 'Del', 'Details', 'Dfn',
    'Dialog', 'Div', 'Dl', 'Dt', 'Em', 'Embed', 'Fencedframe', 'Fieldset', 'Figcaption', 'Figure', 'Footer', 'Form',
    'H1', 'Head', 'Header', 'Hgroup', 'Hr', 'Html', 'I', 'Iframe', 'Img', 'Input', 'Ins', 'Kbd', 'Label', 'Legend', 'Li',
    'Link', 'Main', 'Map', 'Mark', 'Menu', 'Meta', 'Meter', 'Nav', 'Noscript', 'Object', 'Ol', 'Optgroup', 'Option', 'Output',
    'P', 'Picture', 'PortalExperimental', 'Pre', 'Progress', 'Q', 'Rp', 'Rt', 'Ruby', 'S', 'Samp', 'Script', 'Search',
    'Section', 'Select', 'Slot', 'Small', 'Source', 'Span', 'Strong', 'Style', 'Sub', 'Summary', 'Sup', 'Table', 'Tbody',
    'Td', 'Template', 'Textarea', 'Tfoot', 'Th', 'Thead', 'Time', 'Title', 'Tr', 'Track', 'U', 'Ul', 'Var', 'Video', 'Wbr']
for o in _all_: _g[o] = partial(xt_hx, o.lower())

# %% ../nbs/01_components.ipynb 12
def _fill_item(item, obj):
    if not isinstance(item,list): return item
    tag,cs,attr = item
    if isinstance(cs,tuple): cs = tuple(_fill_item(o, obj) for o in cs)
    name = attr.get('name', None)
    val = None if name is None else obj.get(name, None)
    if val is not None:
        if tag=='input':
            if attr.get('type', '') in ('checkbox','radio'):
                if val: attr['checked'] = '1'
                else: attr.pop('checked', '')
            else: attr['value'] = val
        if tag=='textarea': cs=(val,)
    return XT(tag,cs,attr)

# %% ../nbs/01_components.ipynb 13
def fill_form(form:XT, obj)->XT:
    "Fills named items in `form` using attributes in `obj`"
    if not isinstance(obj,dict): obj = asdict(obj)
    return _fill_item(form, obj)

# %% ../nbs/01_components.ipynb 15
def fill_dataclass(src, dest):
    "Modifies dataclass in-place and returns it"
    for nm,val in asdict(src).items(): setattr(dest, nm, val)
    return dest

# %% ../nbs/01_components.ipynb 17
def find_inputs(e, tags='input', **kw):
    # Recursively find all elements in `e` with `tags` and attrs matching `kw`
    if not isinstance(e, (list,tuple)): return []
    inputs = []
    if isinstance(tags,str): tags = [tags]
    elif tags is None: tags = []
    cs = e
    if isinstance(e, list):
        tag,cs,attr = e
        if e[0] in tags and kw.items()<=e[2].items(): inputs.append(e)
    for o in cs: inputs += find_inputs(o, tags, **kw)
    return inputs

# %% ../nbs/01_components.ipynb 21
def __getattr__(tag):
    if tag.startswith('_') or tag[0].islower(): raise AttributeError
    tag = tag.replace("_", "-")
    def _f(*c, target_id=None, **kwargs): return xt_hx(tag, *c, target_id=target_id, **kwargs)
    return _f

# %% ../nbs/01_components.ipynb 22
def html2xt(html):
    rev_map = {'class': 'cls', 'for': 'fr'}
    
    def _parse(elm, lvl=0):
        if isinstance(elm, str): return repr(elm.strip()) if elm.strip() else ''
        if isinstance(elm, list): return '\n'.join(_parse(o, lvl) for o in elm)
        tag_name = elm.name.capitalize()
        if tag_name=='[document]': return _parse(list(elm.children), lvl)
        cts = elm.contents
        cs = [repr(c.strip()) if isinstance(c, str) else _parse(c, lvl+1)
              for c in cts if str(c).strip()]
        attrs = []
        for key, value in elm.attrs.items():
            if isinstance(value,(tuple,list)): value = " ".join(value)
            attrs.append(f'{rev_map.get(key, key).replace("-", "_")}={value!r}')
        spc = " "*lvl*2
        onlychild = not cts or (len(cts)==1 and isinstance(cts[0],str))
        j = ', ' if onlychild else f',\n{spc}'
        inner = j.join(filter(None, cs+attrs))
        if onlychild: return f'{tag_name}({inner})'
        return f'{tag_name}(\n{spc}{inner}\n{" "*(lvl-1)*2})'

    return _parse(BeautifulSoup(html.strip(), 'html.parser'), 1)
