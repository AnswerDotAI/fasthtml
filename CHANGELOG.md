# Release notes

<!-- do not remove -->


## 0.3.4

### New Features

- Experimental new named-based HTMX routing system ([#267](https://github.com/AnswerDotAI/fasthtml/issues/267))
  - `uri` function to constract `url_for` path params
  - patch `HTTPConnection.url_path_for`
  - replace HTTP verb FT attr names with `hx-` prefixed versions, and look up values in route names (with `link` used for `href` attrs)
  - Default route paths to `/{func.__name__}`
  - Default route method to `post` if func name isn't an http verb
  - Support skipping `()` in route decorators


## 0.3.3

### New Features

- Default route name to function name if method provided ([#263](https://github.com/AnswerDotAI/fasthtml/issues/263))
- `surreal` and `htmx` bool params for `FastHTML` and `fast_app` ([#258](https://github.com/AnswerDotAI/fasthtml/issues/258))


## 0.3.2

### New Features

- generic list annotated params double-wrapped ([#253](https://github.com/AnswerDotAI/fasthtml/issues/253))
- Add `Prev()` ([#253](https://github.com/AnswerDotAI/fasthtml/issues/253))
- `ft_cfg` config defaults ([#251](https://github.com/AnswerDotAI/fasthtml/issues/251))
- Make `fill_form` set selected option ([#185](https://github.com/AnswerDotAI/fasthtml/pull/185)), thanks to [@ostwilkens](https://github.com/ostwilkens)

### Bugs Squashed

- Use re.fullmatch for Beforeware ([#221](https://github.com/AnswerDotAI/fasthtml/pull/221)), thanks to [@justbur](https://github.com/justbur)


## 0.3.0

### Breaking changes

- Do not make session vars available as direct params ([#237](https://github.com/AnswerDotAI/fasthtml/issues/237))

### New Features

- Add surreal.js helpers `Me`, `Any`, `On` ([#238](https://github.com/AnswerDotAI/fasthtml/issues/238))
- Add support for application/json in POST requests ([#234](https://github.com/AnswerDotAI/fasthtml/pull/234)), thanks to [@khoaHyh](https://github.com/khoaHyh)
- Wrap Starlette's session in an AttrDict ([#213](https://github.com/AnswerDotAI/fasthtml/pull/213)), thanks to [@jbellis](https://github.com/jbellis)
- Handle mismatches between existing db and schema ([#202](https://github.com/AnswerDotAI/fasthtml/pull/202)), thanks to [@ncoop57](https://github.com/ncoop57)
- Raise warning if type is not passed ([#195](https://github.com/AnswerDotAI/fasthtml/issues/195))

### Bugs Squashed

- railway deploy doesn't check for project name ([#230](https://github.com/AnswerDotAI/fasthtml/pull/230)), thanks to [@gautam-e](https://github.com/gautam-e)


## 0.2.4

### Bugs Squashed

- Signature may not resolve types from str ([#198](https://github.com/AnswerDotAI/fasthtml/issues/198))


## 0.2.3

### New Features

- Add `attrs1st` formatting to html2ft ([#193](https://github.com/AnswerDotAI/fasthtml/pull/193)), thanks to [@AndrewRPerkins](https://github.com/AndrewRPerkins)


## 0.2.2

### New Features

- Check for railway app version ([#192](https://github.com/AnswerDotAI/fasthtml/issues/192))
- Update `flat_xt` to handle single FT item ([#190](https://github.com/AnswerDotAI/fasthtml/issues/190))
- Support FT in HTTPException handling ([#175](https://github.com/AnswerDotAI/fasthtml/issues/175))
- Add `pep8_app.py` ([#163](https://github.com/AnswerDotAI/fasthtml/issues/163))
- Add support for LaTeX formula rendering when rendering markdown ([#158](https://github.com/AnswerDotAI/fasthtml/pull/158)), thanks to [@yym68686](https://github.com/yym68686)
- Add to request: `req.hdrs,req.ftrs,req.htmlkw,req.bodykw` ([#152](https://github.com/AnswerDotAI/fasthtml/issues/152))
- Add htmlkw to `fast_app` ([#145](https://github.com/AnswerDotAI/fasthtml/pull/145)), thanks to [@ranzuh](https://github.com/ranzuh)
- Add `Form` for multipart form data; initial poetry compatibility for `serve` ([#137](https://github.com/AnswerDotAI/fasthtml/issues/137))
- changes toast names to avoid conflict with bootstrap ([#133](https://github.com/AnswerDotAI/fasthtml/pull/133)), thanks to [@vacmar01](https://github.com/vacmar01)
- Automatically move ('title','meta','link','style','base') into head ([#122](https://github.com/AnswerDotAI/fasthtml/issues/122))
- Allow for `Any` or `FT` as return type of routes ([#112](https://github.com/AnswerDotAI/fasthtml/issues/112))


## 0.2.1


### Bugs Squashed

- railway deploy did not connect mount point on first use ([#89](https://github.com/AnswerDotAI/fasthtml/issues/89))


## 0.2.0

- Initial launch version


## 0.1.11

### Breaking changes

- Rename `run_uv` to `serve` ([#84](https://github.com/AnswerDotAI/fasthtml/issues/84))


## 0.1.10

### Dependencies

- Update for fastcore XT to FT name change


## 0.1.9

### New Features

- Skip redundent formatting in `loose_format` ([#79](https://github.com/AnswerDotAI/fasthtml/issues/79))
- Add `htmlkw` param to `FastHTML` ([#78](https://github.com/AnswerDotAI/fasthtml/issues/78))


## 0.1.8

### New Features

- Remove comments in html2xt ([#76](https://github.com/AnswerDotAI/fasthtml/issues/76))
- Handle relative paths in `Social` ([#70](https://github.com/AnswerDotAI/fasthtml/issues/70))
- Add `ftrs` for scripts etc at end of body element ([#62](https://github.com/AnswerDotAI/fasthtml/issues/62))
- Updated html2xt to use unpacked dicts when attr keys are not valid python names ([#57](https://github.com/AnswerDotAI/fasthtml/pull/57)), thanks to [@matdmiller](https://github.com/matdmiller)

### Bugs Squashed

- fix social relative urls ([#77](https://github.com/AnswerDotAI/fasthtml/issues/77))


## 0.1.7

### New Features

- Add `indent` to `html2xt` ([#53](https://github.com/AnswerDotAI/fasthtml/issues/53))
- New `fasthtml.ft` namespace for components ([#50](https://github.com/AnswerDotAI/fasthtml/issues/50))
- Add `bodykw` in `fast_app` ([#49](https://github.com/AnswerDotAI/fasthtml/issues/49))


## 0.1.6

### New Features

- `File` function ([#48](https://github.com/AnswerDotAI/fasthtml/issues/48))
- Remove picolink in `fast_app` if `default_hdrs` is False ([#47](https://github.com/AnswerDotAI/fasthtml/pull/47)), thanks to [@pydanny](https://github.com/pydanny)


## 0.1.5

### New Features

- Add `Favicon` and `Socials` header creators ([#45](https://github.com/AnswerDotAI/fasthtml/issues/45))
- `cookie` function ([#43](https://github.com/AnswerDotAI/fasthtml/issues/43))


## 0.1.4

### New Features

- `ScriptX` and `StyleX` for templated generation from external files ([#42](https://github.com/AnswerDotAI/fasthtml/issues/42))


## 0.1.2

### Breaking changes

- `fast_app` returns `app.route` as well as app ([#38](https://github.com/AnswerDotAI/fasthtml/issues/38))

### New Features

- Add viewport and charset to Meta by default ([#36](https://github.com/AnswerDotAI/fasthtml/issues/36))
- New function `run_js` ([#36](https://github.com/AnswerDotAI/fasthtml/issues/36))


## 0.1.1

### New Features

- Add `fasthtml.toasts` ([#35](https://github.com/AnswerDotAI/fasthtml/issues/35))
- 'Afterware' support
- Add `injects` to request
- Basic websocket support ([#29](https://github.com/AnswerDotAI/fasthtml/issues/29))
- Support `meta` tags in returned tuple ([#28](https://github.com/AnswerDotAI/fasthtml/issues/28))
- Support npm provider in jsdelivr ([#27](https://github.com/AnswerDotAI/fasthtml/issues/27))

### Bugs Squashed

- `Style` does not accept multiple positional args correctly ([#34](https://github.com/AnswerDotAI/fasthtml/issues/34))


## 0.1.0

### New Features

- Add `railway_deploy` ([#26](https://github.com/AnswerDotAI/fasthtml/issues/26))


## 0.0.17

### New Features

- Add `run_uv()` ([#25](https://github.com/AnswerDotAI/fasthtml/issues/25))
- New demo app ([#25](https://github.com/AnswerDotAI/fasthtml/issues/25))
- Add `Container` component ([#24](https://github.com/AnswerDotAI/fasthtml/issues/24))
- Add all HTML elements ([#22](https://github.com/AnswerDotAI/fasthtml/issues/22))
- Add svg.py ([#21](https://github.com/AnswerDotAI/fasthtml/issues/21))


## 0.0.16

### New Features

- Update dashes to underscores in attrs in `html2xt` ([#20](https://github.com/AnswerDotAI/fasthtml/issues/20))
- Rename fasthtml.all to fasthtml.common ([#19](https://github.com/AnswerDotAI/fasthtml/issues/19))


## 0.0.15

### New Features

- Add `Titled` ([#18](https://github.com/AnswerDotAI/fasthtml/issues/18))
- Disable PicoCSS font scaling
- Use constant time string comparison for password checking, h/t José Valim ([#17](https://github.com/AnswerDotAI/fasthtml/issues/17))


## 0.0.14

### New Features

- Add surreal js and scope scripts to default headers, and add `default_hdrs` bool to allow removing default headers ([#16](https://github.com/AnswerDotAI/fasthtml/issues/16))
- Add xtend.py `Script` and `Style` that do not need `NotStr` ([#15](https://github.com/AnswerDotAI/fasthtml/issues/15))
- Add `jsd` ([#14](https://github.com/AnswerDotAI/fasthtml/issues/14))
- Handle lists of `hdrs` ([#14](https://github.com/AnswerDotAI/fasthtml/issues/14))
- Autogen HTML wrapper for non-htmx partials ([#13](https://github.com/AnswerDotAI/fasthtml/issues/13))

### Bugs Squashed

- `html2txt` only parses first partial ([#12](https://github.com/AnswerDotAI/fasthtml/issues/12))


## 0.0.13

### New Features

- Add `html2xt` ([#11](https://github.com/AnswerDotAI/fasthtml/issues/11))


## 0.0.12

### New Features

- Live Reloading ([#9](https://github.com/AnswerDotAI/fasthtml/pull/9)), thanks to [@comhar](https://github.com/comhar)
- Add `adv_app` example ([#8](https://github.com/AnswerDotAI/fasthtml/issues/8))

### Bugs Squashed

- use `sqlite_minutils` in all.py ([#10](https://github.com/AnswerDotAI/fasthtml/issues/10))


## 0.0.10

### New Features

- sortable js support ([#7](https://github.com/AnswerDotAI/fasthtml/issues/7))
- Add `MarkdownJS` and support textareas ([#6](https://github.com/AnswerDotAI/fasthtml/issues/6))
- Handle multi-value form data correctly


## 0.0.9

### New Features

- Module `__getattr__` for components ([#5](https://github.com/AnswerDotAI/fasthtml/issues/5))
- add railway cli link command ([#4](https://github.com/AnswerDotAI/fasthtml/issues/4))


## 0.0.5

### Bugs Squashed

- fix body arg parsing ([#2](https://github.com/AnswerDotAI/fasthtml/issues/2))


## 0.0.3

- Init release

