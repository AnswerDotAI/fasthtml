# Release notes

<!-- do not remove -->


## 0.12.18

### New Features

- Add canonical link option ([#735](https://github.com/AnswerDotAI/fasthtml/issues/735))
- Add onevent kwargs ([#734](https://github.com/AnswerDotAI/fasthtml/issues/734))


## 0.12.17

### New Features

- Check for "hx-history-restore-request" for identifying full page request ([#733](https://github.com/AnswerDotAI/fasthtml/issues/733))
- Set `"vary": "HX-Request, HX-History-Restore-Request"` ([#733](https://github.com/AnswerDotAI/fasthtml/issues/733))
- Allow background tasks in tuple for non-FT responses ([#733](https://github.com/AnswerDotAI/fasthtml/issues/733))


## 0.12.16

### New Features

- Add morph extension ([#727](https://github.com/AnswerDotAI/fasthtml/issues/727))
- Add `devtools_json` ([#725](https://github.com/AnswerDotAI/fasthtml/issues/725))
- fallback stringify FT with `to_xml` ([#724](https://github.com/AnswerDotAI/fasthtml/issues/724))


## 0.12.15

### New Features

- Pass through kwargs in `show` ([#723](https://github.com/AnswerDotAI/fasthtml/issues/723))


## 0.12.14

### New Features

- docsrc support in `show` ([#717](https://github.com/AnswerDotAI/fasthtml/issues/717))
- Add `GoogleAppClient.consent_url` ([#707](https://github.com/AnswerDotAI/fasthtml/issues/707))

### Bugs Squashed

- Fix Discord Client ([#716](https://github.com/AnswerDotAI/fasthtml/pull/716)), thanks to [@erikgaas](https://github.com/erikgaas)


## 0.12.12

### Bugs Squashed

- inserts toasts at top of the page ([#704](https://github.com/AnswerDotAI/fasthtml/pull/704)), thanks to [@comhar](https://github.com/comhar)


## 0.12.11

### New Features

- Add `Fragment` ([#706](https://github.com/AnswerDotAI/fasthtml/issues/706))


## 0.12.9

### New Features

- Background tasks fix+docs ([#692](https://github.com/AnswerDotAI/fasthtml/pull/692)), thanks to [@pydanny](https://github.com/pydanny)
- Move htmx and ext js to jsdelivr from unpkg ([#698](https://github.com/AnswerDotAI/fasthtml/issues/698))


## 0.12.6

- update `_formitem` so that it doesn't raise `KeyError` ([#694](https://github.com/AnswerDotAI/fasthtml/pull/694)), thanks to [@comhar](https://github.com/comhar)


## 0.12.5

### New Features

- Add additional static file types `zip tgz gz csv mp3 wav ogg flac aac doc docx xls xlsx ppt pptx epub mobi bmp tiff avi mov wmv mkv json xml yaml yml rar 7z tar bz2 htm xhtml apk dmg exe msi swf iso json` ([#678](https://github.com/AnswerDotAI/fasthtml/issues/678))
- Add YouTube embed FastHTML component ([#654](https://github.com/AnswerDotAI/fasthtml/pull/654)), thanks to [@dgwyer](https://github.com/dgwyer)
- Handle type hints on session ([#651](https://github.com/AnswerDotAI/fasthtml/pull/651)), thanks to [@henriwoodcock](https://github.com/henriwoodcock)

### Bugs Squashed

- Add missing monsterui dev dependency ([#685](https://github.com/AnswerDotAI/fasthtml/pull/685)), thanks to [@pydanny](https://github.com/pydanny)
- Toast bug fixes ([#684](https://github.com/AnswerDotAI/fasthtml/pull/684)), thanks to [@curtis-allan](https://github.com/curtis-allan)
- Toast container duplication fix ([#657](https://github.com/AnswerDotAI/fasthtml/pull/657)), thanks to [@curtis-allan](https://github.com/curtis-allan)


## 0.12.4

### New Features

- Add Google Credentials helpers ([#661](https://github.com/AnswerDotAI/fasthtml/issues/661))


## 0.12.3

### New Features

- oauth `login_link` kwargs ([#660](https://github.com/AnswerDotAI/fasthtml/issues/660))

### Bugs Squashed

- Toast container duplication fix ([#657](https://github.com/AnswerDotAI/fasthtml/pull/657)), thanks to [@curtis-allan](https://github.com/curtis-allan)


## 0.12.1

### New Features

- Add JupyUviAsync ([#640](https://github.com/AnswerDotAI/fasthtml/issues/640))
- Handling for query or url params in qp/to ([#638](https://github.com/AnswerDotAI/fasthtml/pull/638)), thanks to [@Isaac-Flath](https://github.com/Isaac-Flath)
- Add pdf extension to static routes ([#616](https://github.com/AnswerDotAI/fasthtml/pull/616)), thanks to [@pydanny](https://github.com/pydanny)

### Bugs Squashed

- `HTML` tag from fastcore.xml is shadowed ([#634](https://github.com/AnswerDotAI/fasthtml/issues/634))
- Exception Handlers Return 200 Status Code Instead of Original Error Code ([#633](https://github.com/AnswerDotAI/fasthtml/issues/633))


## 0.12.0

### Breaking changes

- Update fastlite dep to 0.1.1 ([#626](https://github.com/AnswerDotAI/fasthtml/issues/626))
  - This version of fastlite uses apsw, instead of the stdlib's sqlite3.


## 0.11.0

### Breaking changes

-  FT components now stringify as their id if they have one

### New Features

- Create unique route names for nested functions ([#622](https://github.com/AnswerDotAI/fasthtml/issues/622))
- Pass `id=True` when creating a component to get an auto unique id ([#622](https://github.com/AnswerDotAI/fasthtml/issues/622))
- Add `+` to FT components ([#622](https://github.com/AnswerDotAI/fasthtml/issues/622))


## 0.10.3

### Bugs Squashed

- Update sqlite-minutils to apswutils in fasthtml.common


## 0.10.2

### New Features

- Adds `body_wrap` bits to APIRouter ([#612](https://github.com/AnswerDotAI/fasthtml/pull/612)), thanks to [@ohmeow](https://github.com/ohmeow)
- Fix/add default title ([#604](https://github.com/AnswerDotAI/fasthtml/pull/604)), thanks to [@banditburai](https://github.com/banditburai)
- upgrade to htmx@2.0.4, fasthtml-js@1.0.12, etc to latest version ([#603](https://github.com/AnswerDotAI/fasthtml/pull/603)), thanks to [@pratapvardhan](https://github.com/pratapvardhan)
- Optimise highlightjs usage ([#602](https://github.com/AnswerDotAI/fasthtml/pull/602)), thanks to [@curtis-allan](https://github.com/curtis-allan)
- Use explicit version numbers in cdn links ([#599](https://github.com/AnswerDotAI/fasthtml/pull/599)), thanks to [@curtis-allan](https://github.com/curtis-allan)
- Made route functions accesible from an instance of APIRouter as well … ([#598](https://github.com/AnswerDotAI/fasthtml/pull/598)), thanks to [@ohmeow](https://github.com/ohmeow)
- Improved APIRouter to allow for prefixs and discrovery ([#594](https://github.com/AnswerDotAI/fasthtml/pull/594)), thanks to [@ohmeow](https://github.com/ohmeow)


## 0.10.1

### New Features

- Add `Auth0AppClient`, thanks to 78wesley ([#589](https://github.com/AnswerDotAI/fasthtml/issues/589))
- configurable toast duration ([#587](https://github.com/AnswerDotAI/fasthtml/pull/587)), thanks to [@comhar](https://github.com/comhar)


## 0.10.0

### Breaking changes

- The OAuth API is now simplified to only require `chk_auth`, and no longer uses `login`. `chk_auth` should either return `False` (meaning not authenticated) or a `RedirectResponse`. After authentication, the `auth` parameter will be provided to handlers, which will have the oauth ID.

### New Features

- Simplify OAuth API ([#580](https://github.com/AnswerDotAI/fasthtml/issues/580))
- Include session param in websockets handlers ([#563](https://github.com/AnswerDotAI/fasthtml/pull/563)), thanks to [@callmephilip](https://github.com/callmephilip)
- Add path to jupy HTMX ([#503](https://github.com/AnswerDotAI/fasthtml/issues/503))


## 0.9.1

### New Features

- Add oauth `error_path` ([#570](https://github.com/AnswerDotAI/fasthtml/pull/570)), thanks to [@comhar](https://github.com/comhar)
- Add `qp` to create routes with query params ([#560](https://github.com/AnswerDotAI/fasthtml/issues/560))
- `render_rt()` function enables automatic rendering of FT components in notebook ([#558](https://github.com/AnswerDotAI/fasthtml/issues/558))
- In `HTMX()` `height` is now fixed if passed, and `FT` components can be rendered instead of paths ([#557](https://github.com/AnswerDotAI/fasthtml/issues/557))


## 0.9.0

### Breaking changes

- Rename `.rt` method to `.to` ([#539](https://github.com/AnswerDotAI/fasthtml/issues/539))

### New Features

- Support json request key parameters ([#555](https://github.com/AnswerDotAI/fasthtml/issues/555))
- Add `fh_cfg["auto_name"]` option ([#548](https://github.com/AnswerDotAI/fasthtml/issues/548))
- Allow generators etc as responses ([#547](https://github.com/AnswerDotAI/fasthtml/issues/547))
- Add experimental `body_wrap` attr to `FastHTML` ([#546](https://github.com/AnswerDotAI/fasthtml/issues/546))
- Auto-add headers to notebook in `FastHTML` ([#544](https://github.com/AnswerDotAI/fasthtml/issues/544))
- Allow FT components to be used directly as id and `hx_target` values [#544](https://github.com/AnswerDotAI/fasthtml/issues/544))
- Add `host` param to JupyUvi, defaulting to "0.0.0.0" ([#543](https://github.com/AnswerDotAI/fasthtml/issues/543))
- In-jupyter HTMX web apps! ([#541](https://github.com/AnswerDotAI/fasthtml/issues/541))
- Add HTTP verb methods to `APIRouter` ([#538](https://github.com/AnswerDotAI/fasthtml/issues/538))
- Support `WebSocket` type annotation in `app.ws` handlers ([#538](https://github.com/AnswerDotAI/fasthtml/issues/538))

### Bugs Squashed

- Add `nb_hdrs` to `fast_app` ([#551](https://github.com/AnswerDotAI/fasthtml/pull/551)), thanks to [@Isaac-Flath](https://github.com/Isaac-Flath)


## 0.8.0

### Breaking changes

- `jupy_app` and `FastJupy` removed; their functionality is now built into `fast_app` and `FastHTML` and enabled automatically in notebooks
- `RouteX` and `RouterX` removed; use `FastHTML.add_route` instead

### New Features

- Add `APIRouter` ([#535](https://github.com/AnswerDotAI/fasthtml/issues/535))


## 0.7.1

### Breaking changes

- `ws_hdr` and `cts_hdr` both removed from `FastHTML` and `fast_app`; replaced with `exts`, which takes a list of extension names (e.g. `exts='ws'`)

### New Features

- Unified syntax for common HTMX extensions ([#533](https://github.com/AnswerDotAI/fasthtml/issues/533))
- Allow toasts to work with FtResponse ([#526](https://github.com/AnswerDotAI/fasthtml/pull/526)), thanks to [@tomasz-pankowski](https://github.com/tomasz-pankowski)


## 0.6.14

### New Features

- Replace experimental `Pusher` with experimental `setup_ws` and `ws_client` ([#522](https://github.com/AnswerDotAI/fasthtml/issues/522))
- Add experimental `with_sid()` ([#521](https://github.com/AnswerDotAI/fasthtml/issues/521))
- Ensure FT children are tuples
- Adding mermaidJS for mermaid graphs ([#518](https://github.com/AnswerDotAI/fasthtml/pull/518)), thanks to [@ImtiazKhanDS](https://github.com/ImtiazKhanDS)

### Bugs Squashed

- Uploading a single file on a multiple file field requires try/except ([#513](https://github.com/AnswerDotAI/fasthtml/issues/513))


## 0.6.13

### New Features

- Add `scope` param ([#519](https://github.com/AnswerDotAI/fasthtml/issues/519))
- Allow `FastHTML.ws` to be used without a function ([#519](https://github.com/AnswerDotAI/fasthtml/issues/519))
- Allow setting of xmlns in `Svg` ([#519](https://github.com/AnswerDotAI/fasthtml/issues/519))

### Bugs Squashed

- Add missing `unqid` import ([#519](https://github.com/AnswerDotAI/fasthtml/issues/519))


## 0.6.12

### New Features

- Add `pusher()` for real time DOM updates; add `fh_cfg.auto_id` to automatically add unique IDs ([#517](https://github.com/AnswerDotAI/fasthtml/issues/517))
- Support background tasks ([#512](https://github.com/AnswerDotAI/fasthtml/issues/512))
- Allows for passing route functions ([#511](https://github.com/AnswerDotAI/fasthtml/pull/511)), thanks to [@Isaac-Flath](https://github.com/Isaac-Flath)
- Add path arg to HTMX ([#504](https://github.com/AnswerDotAI/fasthtml/pull/504)), thanks to [@Isaac-Flath](https://github.com/Isaac-Flath)

### Bugs Squashed

- Multi file upload does not work ([#509](https://github.com/AnswerDotAI/fasthtml/issues/509))


## 0.6.10

### New Features

- Document usage with Jupyter ([#469](https://github.com/AnswerDotAI/fasthtml/issues/469))


## 0.6.9

### New Features

- Add `oauth.redir_url` function ([#476](https://github.com/AnswerDotAI/fasthtml/issues/476))


## 0.6.8

### New Features

- Allow for handler names with same name as an http verb, even if path not provided ([#459](https://github.com/AnswerDotAI/fasthtml/issues/459))
- Support explicit iframe height in Jupyter HTMX ([#458](https://github.com/AnswerDotAI/fasthtml/pull/458)), thanks to [@callmephilip](https://github.com/callmephilip)
- Improve type annotations for element attributes ([#453](https://github.com/AnswerDotAI/fasthtml/pull/453)), thanks to [@callmephilip](https://github.com/callmephilip)
- Make compatible w/ ddtrace ([#452](https://github.com/AnswerDotAI/fasthtml/pull/452)), thanks to [@derekgliwa](https://github.com/derekgliwa)


## 0.6.7

### Bugs Squashed

- Remove IPython dep ([#456](https://github.com/AnswerDotAI/fasthtml/issues/456))


## 0.6.6

### New Features

- Add `def_hdrs` ([#446](https://github.com/AnswerDotAI/fasthtml/issues/446))


## 0.6.5

### New Features

- Jupyter compatibility ([#445](https://github.com/AnswerDotAI/fasthtml/issues/445))
- Redefining a route overwrites existing definition (e.g for use in notebooks) ([#444](https://github.com/AnswerDotAI/fasthtml/issues/444))

### Bugs Squashed

- [BUG] d argument is not passed in Path function for SVGs ([#437](https://github.com/AnswerDotAI/fasthtml/issues/437))


## 0.6.4

### New Features

- Pass query params to custom class annotated args ([#439](https://github.com/AnswerDotAI/fasthtml/issues/439))


## 0.6.3

### Bugs Squashed

- `svg.Path` not passing `d` param ([#438](https://github.com/AnswerDotAI/fasthtml/issues/438))


## 0.6.2

### New Features

- Include both `m` (me) and `p` (prev) in `On` and `Prev` handlers, and run after DOM ready ([#429](https://github.com/AnswerDotAI/fasthtml/issues/429))

### Bugs Squashed

- `proc_htmx` not exported correctly ([#434](https://github.com/AnswerDotAI/fasthtml/issues/434))


## 0.6.0

### Breaking changes

- `date` has been renamed to `parsed_date`

### New Features

- Handle non-list/tuple `hdrs` and `ftrs` in `FastHTML()` ([#426](https://github.com/AnswerDotAI/fasthtml/issues/426))
- Handle automatic `datetime.date` form field conversion ([#415](https://github.com/AnswerDotAI/fasthtml/issues/415))

### Bugs Squashed

- Make sure only the selected radio button in a radio group is checked during `form_fill` ([#424](https://github.com/AnswerDotAI/fasthtml/pull/424)), thanks to [@rbavery](https://github.com/rbavery)
- All radio buttons in a radio group are checked during `fill_form` ([#423](https://github.com/AnswerDotAI/fasthtml/issues/423))
- receiving a list[str] as a parameter doesn't work with get request ([#422](https://github.com/AnswerDotAI/fasthtml/issues/422))
- Multipart error when submitting with empty form-data ([#405](https://github.com/AnswerDotAI/fasthtml/issues/405))


## 0.5.3

### New Features

- Add `FtResponse` ([#425](https://github.com/AnswerDotAI/fasthtml/issues/425))
- Add `sid_scr` ([#425](https://github.com/AnswerDotAI/fasthtml/issues/425))
- Scope `On` selector to `p` ([#414](https://github.com/AnswerDotAI/fasthtml/issues/414))
- Store `p=me()` before `On` handler ([#413](https://github.com/AnswerDotAI/fasthtml/issues/413))
- Convert `dict` children in `ft_htmx` and `ft_hx` to kwargs ([#412](https://github.com/AnswerDotAI/fasthtml/issues/412))
- Add reload on CSS and JS file changes ([#401](https://github.com/AnswerDotAI/fasthtml/issues/401))

### Bugs Squashed

- `static_path` ignored in `fast_app` ([#410](https://github.com/AnswerDotAI/fasthtml/issues/410))


## 0.5.2

### New Features

- Greatly improved SVG support ([#409](https://github.com/AnswerDotAI/fasthtml/issues/409))
- Add SVG HTMX helpers: `svg_sel`, `SvgOob`, and `SvgInb` ([#408](https://github.com/AnswerDotAI/fasthtml/issues/408))
- Add `Client` and `Nbsp` ([#403](https://github.com/AnswerDotAI/fasthtml/issues/403))
- Add `Redirect()` and handle magic `__response__` method ([#400](https://github.com/AnswerDotAI/fasthtml/issues/400))
- Add `HtmxResponseHeaders` ([#399](https://github.com/AnswerDotAI/fasthtml/issues/399))
- Add `session` to `OAuth.chk_auth` ([#394](https://github.com/AnswerDotAI/fasthtml/issues/394))
- Add `static_routes` and `static_route_exts` methods to `FastHTML` ([#387](https://github.com/AnswerDotAI/fasthtml/issues/387))

### Bugs Squashed

- toasts do not show if response empty or tuple ([#386](https://github.com/AnswerDotAI/fasthtml/issues/386))
- toasts.py not updated for router refactor ([#385](https://github.com/AnswerDotAI/fasthtml/issues/385))


## 0.5.1

### New Features

- Add `sse_message`, `EventStream`, and `signal_shutdown` ([#384](https://github.com/AnswerDotAI/fasthtml/issues/384))


## 0.5.0

### New Features

- Make hdrs, ftrs, htmlkw, bodykw, etc available to `RouterX` and `RouteX` via `._app` ([#381](https://github.com/AnswerDotAI/fasthtml/issues/381))
- Add `OAuth` class ([#381](https://github.com/AnswerDotAI/fasthtml/issues/381))
    - Move redirect url into methods for oauth
- Add options to change default static media directory ([#373](https://github.com/AnswerDotAI/fasthtml/pull/373)), thanks to [@coreman14](https://github.com/coreman14)
- Add `PicoBusy()` function to display loading spinner during html load ([#372](https://github.com/AnswerDotAI/fasthtml/issues/372))
- Add `HtmxOn()` to allow adding htmx event listeners more easily ([#371](https://github.com/AnswerDotAI/fasthtml/issues/371))
- Set toasts to only work with FT responses ([#368](https://github.com/AnswerDotAI/fasthtml/pull/368)), thanks to [@pydanny](https://github.com/pydanny)
- Routing subapp improvements ([#365](https://github.com/AnswerDotAI/fasthtml/pull/365)), thanks to [@Isaac-Flath](https://github.com/Isaac-Flath)
- Add all HTMX attrs to component signatures ([#363](https://github.com/AnswerDotAI/fasthtml/issues/363))
- Add markdown version of all docs ([#361](https://github.com/AnswerDotAI/fasthtml/issues/361))
- add easy to use chunked transfer extension header ([#346](https://github.com/AnswerDotAI/fasthtml/pull/346)), thanks to [@fabge](https://github.com/fabge)
- Set 404 exception handling to give "404 Not Found" message ([#335](https://github.com/AnswerDotAI/fasthtml/pull/335)), thanks to [@Isaac-Flath](https://github.com/Isaac-Flath)

### Bugs Squashed

- [BUG] Toasts don't show after redirect ([#358](https://github.com/AnswerDotAI/fasthtml/issues/358))


## 0.4.5

### New Features

- Support for web components in html2ft ([#354](https://github.com/AnswerDotAI/fasthtml/issues/354))
- Support `options` http verb as function name ([#350](https://github.com/AnswerDotAI/fasthtml/issues/350))

### Bugs Squashed

- railway deployment not checking deployed projects correctly ([#340](https://github.com/AnswerDotAI/fasthtml/issues/340))
- Socials tag only appears in head tag when added via FastHTML.hdrs ([#324](https://github.com/AnswerDotAI/fasthtml/issues/324))


## 0.4.4

### New Features

- Replace `__call__` with `rt` in handler functions ([#334](https://github.com/AnswerDotAI/fasthtml/issues/334))
- Add `flat_tuple` and use it to allow nested tuples in route responses
- Add `body` parameter for decoded body
- Move pico-specific components to separate module ([#327](https://github.com/AnswerDotAI/fasthtml/issues/327))
- Add "get" and "post" as default methods on routes ([#317](https://github.com/AnswerDotAI/fasthtml/issues/317))
- Support Reverse URL lookups by exposing `url_for` ([#189](https://github.com/AnswerDotAI/fasthtml/issues/189))


## 0.4.3

### New Features

- Fastlite 0.0.9 dep


## 0.4.2

### New Features

- Rename `Checkbox` to `CheckboxX` ([#314](https://github.com/AnswerDotAI/fasthtml/issues/314))
  - CheckboxX also adds a hidden field before the checkbox
- Automatically choose last field in form data if list provided by non-list parameter


## 0.4.1

### Bugs Squashed

- post release fix for `fill_form` ([#309](https://github.com/AnswerDotAI/fasthtml/issues/309))


## 0.4.0

### Breaking changes

- `__init.py__` now only contains `fasthtml.core`

### New Features

- Fastcore 1.7 compatibility ([#307](https://github.com/AnswerDotAI/fasthtml/issues/307))
- Add `fasthtml.basics` for importing the main fasthtml modules


## 0.3.7

### New Features

- Add `reload_includes` and `reload_excludes` options to serve ([#291](https://github.com/AnswerDotAI/fasthtml/pull/291)), thanks to [@pydanny](https://github.com/pydanny)

### Bugs Squashed

- katex.js missing ([#305](https://github.com/AnswerDotAI/fasthtml/issues/305))


## 0.3.6

### Bugs Squashed

- postrelease fix markdown js ([#290](https://github.com/AnswerDotAI/fasthtml/issues/290))


## 0.3.5

### New Features

- Support `dict` value in `hx_vals` ([#288](https://github.com/AnswerDotAI/fasthtml/issues/288))
- Add `sess_cls` param to `FastHTML` ([#284](https://github.com/AnswerDotAI/fasthtml/issues/284))
- Make `index` a special handler name for path "/" get request ([#274](https://github.com/AnswerDotAI/fasthtml/issues/274))
- Use `run_in_threadpool` for non-async handlers ([#270](https://github.com/AnswerDotAI/fasthtml/issues/270))
- Enhance LaTeX rendering in Markdown with support for environments ([#269](https://github.com/AnswerDotAI/fasthtml/pull/269)), thanks to [@rian-dolphin](https://github.com/rian-dolphin)

### Bugs Squashed

- Duplicate parameters in components.pyi ([#255](https://github.com/AnswerDotAI/fasthtml/issues/255))


## 0.3.4

### New Features

- Experimental new named-based HTMX routing system ([#267](https://github.com/AnswerDotAI/fasthtml/issues/267))
  - `uri` function to construct `url_for` path params
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

- Skip redundant formatting in `loose_format` ([#79](https://github.com/AnswerDotAI/fasthtml/issues/79))
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

