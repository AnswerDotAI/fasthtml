# FastHTML Upgrade from htmx2 to htmx4

This document summarizes what you need to do to upgrade a FastHTML codebase from htmx v2 to htmx v4. For full htmx migration details, see: https://four.htmx.org/docs/get-started/migration

## What's New

FastHTML now supports htmx v4 via `htmx4=True`. Here are the key changes at the FastHTML level:

| Area | htmx v2 (default) | htmx v4 (`htmx4=True`) |
|------|-------------------|------------------------|
| **Init** | `fast_app()` or `FastHTML()` | Add `htmx4=True` |
| **Extensions** | `exts='ws'`, `exts='sse'` | Same, auto-maps to v4 versions when htmx4=True |
| **WS attributes** | `ws_connect`, `ws_send`, `hx_ext='ws'` | `hx_ws_connect`, `hx_ws_send` (no `hx_ext`) |
| **SSE** | `sse_connect`, `sse_swap`, `hx_ext='sse'` | `hx_sse_connect` (no `hx_ext`, no `sse_swap`) |
| **SSE message** | `sse_message(data)` | `sse_message(data, htmx4=True)` |
| **Multi-target** | `hx_swap_oob` or named SSE events | `HxPartial(content, hx_target='#id')` |
| **Request headers** | `hx_trigger` (value: `id`) | `hx_source` (value: `tag#id`) |
| **Events in JS** | camelCase (`htmx:beforeRequest`) | colon-separated (`htmx:before:request`) |
| **SVG OOB** | Needs `SvgOob()` wrapper | Plain `Svg()` works directly |
| **Attribute inheritance** | Implicit from parent | Explicit via `:inherited` modifier |

---

## Naming

### MetaCharacter

htmx v4 uses `:` as a separator in attribute and event names (for example, `hx-ws:connect` and `htmx:before:request`). Since colons cannot be used in Python keyword arguments, FastHTML sets `metaCharacter="-"`, which replaces all `:` characters with `-`.

The full conversion chain:

| Layer | Example |
|-------|---------|
| htmx v4 default | `htmx:before:request` |
| With `metaCharacter="-"` | `htmx-before-request` |
| FastHTML Python (`_` → `-`) | `htmx_before_request` |

This is configured automatically when you set `htmx4=True`.

### Renamed Events

All events now follow this pattern: `htmx:phase:action[:sub-action]`

Sources: [htmx v4 migration guide: Renamed events](https://four.htmx.org/docs/get-started/migration#renamed-events), [htmx upgrade guide: Step 5 event listeners](https://github.com/bigskysoftware/htmx/blob/four/src/skills/htmx-upgrade-from-htmx2.md#step-5-update-event-listeners)

| htmx 2.x | htmx 4.x |
|-----------|-----------|
| `htmx:afterOnLoad` | `htmx:after:init` |
| `htmx:afterProcessNode` | `htmx:after:init` |
| `htmx:afterRequest` | `htmx:after:request` |
| `htmx:afterSettle` | `htmx:after:swap` |
| `htmx:afterSwap` | `htmx:after:swap` |
| `htmx:beforeCleanupElement` | `htmx:before:cleanup` |
| `htmx:beforeHistorySave` | `htmx:before:history:update` |
| `htmx:beforeHistoryUpdate` | `htmx:before:history:update` |
| `htmx:beforeOnLoad` | `htmx:before:init` |
| `htmx:beforeProcessNode` | `htmx:before:process` |
| `htmx:beforeRequest` | `htmx:before:request` |
| `htmx:beforeSwap` | `htmx:before:swap` |
| `htmx:beforeTransition` | `htmx:before:viewTransition` |
| `htmx:configRequest` | `htmx:config:request` |
| `htmx:historyCacheMiss` | `htmx:before:history:restore` |
| `htmx:historyRestore` | `htmx:before:history:restore` |
| `htmx:load` | `htmx:after:init` |
| `htmx:oobAfterSwap` | `htmx:after:swap` |
| `htmx:oobBeforeSwap` | `htmx:before:swap` |
| `htmx:pushedIntoHistory` | `htmx:after:history:push` |
| `htmx:replacedInHistory` | `htmx:after:history:replace` |
| `htmx:responseError` | `htmx:error` |
| `htmx:sendAbort` | `htmx:error` |
| `htmx:sendError` | `htmx:error` |
| `htmx:swapError` | `htmx:error` |
| `htmx:targetError` | `htmx:error` |
| `htmx:timeout` | `htmx:error` |

---

## Event Structure

In v4, the flat `event.detail` properties were reorganized into a unified `ctx` object:

| v2 | v4 |
|----|-----|
| `event.detail.elt` | `event.detail.ctx.sourceElement` |
| `event.detail.path` | `event.detail.ctx.request.action` |
| `event.detail.target` | `event.detail.ctx.target` |

### Examples affected

**PicoBusy** updated event names and detail path:
```python
def PicoBusy(htmx4=False, metaChar=None):
    if metaChar is None: metaChar = '-' if htmx4 else ':'
    evt = (f'before{metaChar}request', f'after{metaChar}request') if htmx4 else ('beforeRequest', 'afterRequest')
    elt = 'event.detail.ctx.sourceElement' if htmx4 else 'event.detail.elt'
    return (HtmxOn(evt[0], f"{elt}.setAttribute('aria-busy', 'true' )", htmx4=htmx4),
            HtmxOn(evt[1], f"{elt}.setAttribute('aria-busy', 'false')", htmx4=htmx4))
```

---

## Partial

htmx v4 introduces `HxPartial` (`<hx-partial>`) for updating elements **outside the primary swap target**. Each `HxPartial` specifies its own `hx_target`, which makes targeting more explicit than OOB. `hx_swap_oob=True` still works in v4 for simple same-ID replacement.

```python
# Update primary target + another element
return Div("main content"), HxPartial(Div("sidebar update"), hx_target="#sidebar")
```

**Swap ordering changed:**
- **v2:** OOB swaps → primary swap
- **v4:** Primary swap → OOB swaps → partials

---

## Attribute Inheritance

In v2, attributes like `hx-target`, `hx-swap`, and `hx-boost` were inherited implicitly from parent elements. In v4, inheritance is **off by default**; use the `:inherited` modifier instead. With `metaCharacter="-"`, this becomes `_inherited` in FastHTML:

```python
# v2: children inherit hx_target from parent automatically
Div(hx_target="#output")(
    Button("A", hx_get="/a"),
    Button("B", hx_get="/b"),
)

# v4: must opt in to inheritance
Div(hx_target_inherited="#output")(
    Button("A", hx_get="/a"),
    Button("B", hx_get="/b"),
)
```

---

## Request Headers

In v4, the request headers sent by the browser changed:

Sources: [htmx v4 migration guide: Request headers](https://four.htmx.org/docs/get-started/migration#request-headers), [htmx upgrade guide: Step 8 server-side header handling](https://github.com/bigskysoftware/htmx/blob/four/src/skills/htmx-upgrade-from-htmx2.md#step-8-update-server-side-header-handling)

| v2 Header | v4 Header | Notes |
|-----------|-----------|-------|
| `HX-Trigger` | `HX-Source` | Format changed to `tag#id` |
| `HX-Target` | `HX-Target` | Format changed to `tag#id` |
| `HX-Trigger-Name` | *(removed)* | Use `HX-Source` |
| `HX-Prompt` | *(removed)* | Use `hx-confirm` with `js:` prefix |
| *(n/a)* | `HX-Request-Type` | `"partial"` or `"full"` |
| *(n/a)* | `Accept` | Now explicitly `text/html` |

In FastHTML handler signatures:

```python
# v2
async def handle(hx_trigger: str): ...   

# v4
async def handle(hx_source: str): ...  
```

Or use the `HtmxHeaders` dataclass (works in both versions):

```python
async def handle(htmx: HtmxHeaders):
    print(htmx.source, htmx.target, htmx.request_type)
```

**Note:** `hx-trigger`, the *HTML attribute*, is unchanged; only the *request header* was renamed.

---

## WebSocket

### Attribute Changes

| v2 | v4 | Notes |
|----|-----|-------|
| `hx_ext='ws'` | *(remove)* | The extension auto-registers when the script is loaded |
| `ws_connect='/endpoint'` | `hx_ws_connect='/endpoint'` | |
| `ws_send=True` | `hx_ws_send=True` | |

```python
app, rt = fast_app(htmx4=True, exts='ws')

@rt('/')
def get():
    return Titled('WS Demo',
        Div(id='msgs'),
        Form(Input(id='msg', name='msg'),
             hx_ws_send=True),
        hx_ws_connect='/ws')

@app.ws('/ws')
async def ws(msg: str, send):
    await send(Div(f'You said: {msg}',
        id='msgs', hx_swap_oob=True))  # v2: no hx_swap_oob needed
```

### Data Structure

| v2 | v4 |
|----|-----|
| Form fields at root: `data['msg']` | Nested under `values`: `data['values']['msg']` |
| Headers as `data['HEADERS']` | Headers as `data['headers']` (lowercase) |

Although htmx v4 WebSocket support also includes a JSON envelope format for server-to-client messages, FastHTML sends raw HTML for compatibility with htmx v2.

---

## SSE

### Attribute Changes

| v2 | v4 |
|----|-----|
| `sse_connect='/endpoint'` | `hx_sse_connect='/endpoint'` |
| `sse_swap='message'` | *(remove)* |

```python
# v2
Div(hx_ext="sse", sse_connect="/stream", sse_swap="message")

# v4
Div(hx_sse_connect="/stream")
```

### `sse_message`

In v4, the `event:` line must be omitted for default swaps; including it triggers a custom DOM event instead. Pass `htmx4=True`:

```python
# v2
yield sse_message(data)              # sends "event: message\ndata: ...\n\n"

# v4
yield sse_message(data, htmx4=True)  # sends "data: ...\n\n" (no event line)
```

For updating multiple targets (multiplexing), use `HxPartial` in a single message:

```python
yield sse_message(
    (HxPartial(content_a, hx_target="#a"), HxPartial(content_b, hx_target="#b")),
    htmx4=True)
```
