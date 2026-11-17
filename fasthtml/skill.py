# NB: this file is designed for an LLM reader, not a human. Add it to your LLM's context and ask it to explain.
r"""Write and review idiomatic FastHTML apps.

## Read first

- index: https://www.fastht.ml/docs/llms.txt
- concise guide: https://www.fastht.ml/docs/ref/concise_guide.html.md
- handlers, binding, responses: https://www.fastht.ml/docs/ref/handlers.html.md
- routing: https://www.fastht.ml/docs/explains/routes.html.md
- role model: `examples/adv_app_strip.py`; https://raw.githubusercontent.com/AnswerDotAI/fasthtml/main/examples/adv_app_strip.py

## Idioms

- FT: Python call; positional children, keyword attributes; return FT or tuple. No templates, serializers or JSON-rendering pipeline.
- `@rt`: function-name path; GET+POST default. Normally no verb restrictions. When needed, `@rt('/x')` + `def get(...)` infers GET; no redundant `methods=`.
- handler references: `hx_post=save`, `href=edit.to(id=record.id)`; no copied URL strings
- typed handler arguments bind form/query fields; `req`, `sess`, `auth` injected. No FastAPI `Depends`, `Form`, `response_model`.
- HTMX action → FT fragment; `target_id`, `hx_swap` on caller. Normal requests gain document boilerplate.
- components: small functions; record rendering: `__ft__`. No controller/form-class framework.
- `Titled`: title+H1+Container
- shared auth: Beforeware; authorize actions as well as pages
- `from fasthtml.common import *`; `app,rt = fast_app()`; `serve()`; no `__main__` guard
"""
