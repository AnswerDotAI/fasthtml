# Release notes

<!-- do not remove -->

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

