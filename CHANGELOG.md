# Release notes

<!-- do not remove -->

## 0.12.44

- Add all HTTP request param handling to websockets too


## 0.12.43

### New Features

- Add ApiReturn class for dual browser/API responses in route handlers ([#831](https://github.com/AnswerDotAI/fasthtml/issues/831))


## 0.12.42

### New Features

- Add uvicorn kwargs to serve() with @delegates(uvicorn.run) and add colored link output ([#830](https://github.com/AnswerDotAI/fasthtml/issues/830))


## 0.12.41

### New Features

- Add async OAuth methods and make OAuth handlers async ([#828](https://github.com/AnswerDotAI/fasthtml/issues/828))
- Add `State` injection support for route handlers via type annotation or arg name ([#827](https://github.com/AnswerDotAI/fasthtml/issues/827))


## 0.12.40

### New Features

- add optional client arg to HTMX for persistent tests ([#824](https://github.com/AnswerDotAI/fasthtml/pull/824)), thanks to [@johnowhitaker](https://github.com/johnowhitaker)

### Bugs Squashed

- Fix return type annotation bug ([#823](https://github.com/AnswerDotAI/fasthtml/pull/823)), thanks to [@erikgaas](https://github.com/erikgaas)


## 0.12.39

### Bugs Squashed

- Fix typo: put='hx-post' → put='hx-put' in `_verbs` mapping ([#821](https://github.com/AnswerDotAI/fasthtml/pull/821)), thanks to [@erikgaas](https://github.com/erikgaas)
- Fix live reload infinite loop on uvicorn >= 0.39 ([#818](https://github.com/AnswerDotAI/fasthtml/pull/818)), thanks to [@erikgaas](https://github.com/erikgaas)


## 0.12.37

### New Features

- Add Apple sign in ([#813](https://github.com/AnswerDotAI/fasthtml/pull/813)), thanks to [@erikgaas](https://github.com/erikgaas)

### Bugs Squashed

- Line defaults suppressed inheriting of stroke color from parent elements ([#804](https://github.com/AnswerDotAI/fasthtml/pull/804)), thanks to [@erikgaas](https://github.com/erikgaas)


## 0.12.37

### New Features

- Add Apple sign in ([#813](https://github.com/AnswerDotAI/fasthtml/pull/813)), thanks to [@erikgaas](https://github.com/erikgaas)
  - Adding sign in with apple. It is slightly different because it requires parsing a p8 file and a post request for the redirect if you want name and email.

Adding PyJWT as a req. It's small and fairly ubiquitous, but I'm down to reconsider.

Fun fact apple sign in does not work on localhost which is super annoying, but you can use solveit easily to test it out : )

- [FEATURE] ([#793](https://github.com/AnswerDotAI/fasthtml/issues/793))
  - Hi my feature request has to do with how we interact with database tables

Currently although they do implement CRUD I feel very limited in how I can manipulate data and interact with tables. I was wondering if by any chance it's possible to instead just load in databases using pandas and interact with tables as data frames? 

This would make it a lot easier and faster to work with data and python users would likely have an easier time developing with pandas dataframes as their API is more familiar and has a ton of features and documentation

### Bugs Squashed

- Line defaults suppressed inheriting of stroke color from parent elements ([#804](https://github.com/AnswerDotAI/fasthtml/pull/804)), thanks to [@erikgaas](https://github.com/erikgaas)
  - Fixes #757 

Line defaults suppressed inheriting of stroke color from parent elements.

- [BUG]  SVG Line should not have some default parameters ([#757](https://github.com/AnswerDotAI/fasthtml/issues/757))
  - in FastHTML 0.12.21 in file ```svg.py``` the ```Line``` is defined with default values for stroke and stroke_width:
```python
def Line(x1, y1, x2=0, y2=0, stroke='black', w=None, stroke_width=1, **kwargs): ...
```
This results that using a line with only coordinates, will also auto generate:  ```stroke="black" stroke-width="1"```
This is wrong as it overrides attributes defined in a parent tag like ```<g>```. 
Eg. this will fail to achieve the result of having red and thick lines:
```python
G(stroke="red", stroke_width="20" )(
        Line(x1=0, y1=0, x2=100, y2=100),
        Line(x1=0, y1=0, x2=10, y2=100),
    )
```
Instead of desired outputs like:
```svg
<line x1="0" y1="0" x2="100" y2="100">
```
will generate lines that have unwanted attributes, that override the parent:
```svg
<line x1="0" y1="0" x2="100" y2="100" stroke="black" stroke-width="1">
```

- [BUG] Toasts are not displayed in version 0.12.12 ([#709](https://github.com/AnswerDotAI/fasthtml/issues/709))
  - Until now, my application used version 0.12.6, and toasts were displayed at the bottom of the screen. But I updated to the latest version 0.12.12, which supposedly fixed the issue, and to my surprise, the toasts no longer appear.
I tested with a simple app, and the toasts show correctly, so I suspect some interference with my code.

I suspect the code in my main.js, which I'm copying below:

```javascript
// DataTables initialization and event handling for HTMX
// This script initializes DataTables on elements with the class "datatable"
document.addEventListener("DOMContentLoaded", () => {
    document.body.addEventListener('htmx:afterSwap', (e) => {
        console.log("📦 htmx:afterSwap event received");

        const tables = document.querySelectorAll(".datatable");
        console.log("🔍 Looking for .datatable...");

        tables.forEach(table => {
            console.log(`➡️ Init DataTable for: #${table.id}`);
            
            if ($.fn.DataTable.isDataTable(table)) {
                console.warn("⚠️ Table already initialized. Destroying existing instance.");

                $(table).DataTable().destroy();

                const clonedTable = table.cloneNode(true);
                table.parentElement.replaceChild(clonedTable, table);
                table = clonedTable;
            }

            const $table = $(table);
            // DataTable configuration in Spanish
            $table.DataTable({
                renderer: 'bootstrap',
                language: {
                    decimal: ",",
                    processing: "Procesando...",
                    search: "Buscar:",
                    lengthMenu: "Mostrar _MENU_",
                    info: "Mostrando (_START_ a _END_) de _TOTAL_ registros",
                    infoEmpty: "No hay datos que mostrar.",
                    infoFiltered: "(filtrado de _MAX_ registros en total)",
                    loadingRecords: "Cargando...",
                    zeroRecords: "No se encontraron registros coincidentes",
                    emptyTable: "No hay datos disponibles en la tabla",
                    paginate: {
                        first: "<<",
                        previous: "<",
                        next: ">",
                        last: ">>"
                    },
                    aria: {
                        sortAscending: ": activar para ordenar la columna de manera ascendente",
                        sortDescending: ": activar para ordenar la columna de manera descendente"
                    }
                },
                layout: {
                    topStart: 'info',
                    topEnd: {
                        search: { placeholder: 'Buscar ...' },
                    },
                    bottomStart: 'pageLength',
                    bottomEnd: {
                        paging: { firstLast: false }
                    }
                },
                initComplete: function () {
                    htmx.process(this.api().table().node());
                },
                drawCallback: function () {
                    const rows = this.api().rows({ page: 'current' }).nodes();
                    rows.each(function (row) {
                        htmx.process(row); // 🔥 this reactivates the buttons in each visible row
                    });
                },
                // dom: 'Bfrtip',
                // buttons: [
                //     {
                //         extend: 'excelHtml5',
                //         text: '<i class="bi bi-file-earmark-excel"></i> Export records',
                //         className: 'btn btn-success btn-sm',
                //         exportOptions: {
                //             modifier: {
                //                 page: 'current'  // Solo exporta los visibles
                //             }
                //         }
                //     }
                // ],
            });

            // Focus on search field
            document.querySelector(`#${table.id}_wrapper .dt-search input`)?.focus();
        });
    });
});

// Bootstrap 5.3.0 - Collapse
// This script handles the collapse functionality of the Bootstrap navbar
document.addEventListener('DOMContentLoaded', function () {
    const navbarCollapse = document.querySelector('.navbar-collapse');
    const navLinks = document.querySelectorAll('.navbar-collapse .nav-link, .navbar-collapse .dropdown-item');

    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            // Do not close if the click was on the dropdown button.
            if (link.getAttribute('data-bs-toggle') === 'dropdown') {
                return;
            }

            // Close the menu if it is expanded.
            if (navbarCollapse.classList.contains('show')) {
                const bsCollapse = bootstrap.Collapse.getInstance(navbarCollapse);
                if (bsCollapse) {
                    bsCollapse.hide();
                }
            }
        });
    });
});
```
This code is meant to interact with Datatable.js and Bootstrap, addressing some unusual behaviors from these two libraries. I suspect the conflict stems from the htmx:afterSwap Listener.

- [BUG] XT undefined in components.py ([#672](https://github.com/AnswerDotAI/fasthtml/issues/672))
  - # `XT` undefined in components.py in FastHTML 0.12.4


**Describe the bug**
In FastHTML version 0.12.4, there is an error in the `components.py` file where `XT` is referenced but not defined. According to the error message, this should be `FT` based on the library's own suggestion. This appears to be a remnant from a transition from using `XT` to `FT` for component types, as mentioned in FastHTML's changelog for version 0.1.10.

The error prevents any application using FastHTML from running, as the import chain fails before any application code can execute. This appears to be a critical issue affecting all users of FastHTML 0.12.4.

**Minimal Reproducible Example**
```python
from fasthtml.core import fast_app
from fasthtml.xtend import Style

# Initialize the FastHTML app
app, rt = fast_app(
    hdrs=[Style("body { font-family: sans-serif; }")]
)

@rt("/")
def get():
    return "Hello, World!"

if __name__ == "__main__":
    from fasthtml.core import serve
    serve()
```

When running the above script, the following error occurs:

```
Traceback (most recent call last):
  File "/path/to/app.py", line 1, in <module>
    from fasthtml.core import fast_app
  File "/path/to/.venv/lib/python3.11/site-packages/fasthtml/__init__.py", line 2, in <module>
    from .core import *
  File "/path/to/.venv/lib/python3.11/site-packages/fasthtml/core.py", line 14, in <module>
    from .xtend import *
  File "/path/to/.venv/lib/python3.11/site-packages/fasthtml/xtend.py", line 15, in <module>
    from .components import *
  File "/path/to/.venv/lib/python3.11/site-packages/fasthtml/components.py", line 85, in <module>
    def fill_form(form:XT, obj)->XT:
                       ^^
NameError: name 'XT' is not defined. Did you mean: 'FT'?
```

**Expected behavior**
The script should run successfully, starting a FastHTML application without any import errors.

**Environment Information**
Please provide the following version information:
- fasthtml version: 0.12.4
- fastcore version: 1.7.29
- fastlite version: 0.1.2
- Python version: 3.11
- Operating system: Linux 6.11.0-18-generic
- Installation method: pip via uv (`uv pip install python-fasthtml`)

**Confirmation**
- [x] I have read the FAQ (https://docs.fastht.ml/explains/faq.html)
- [x] I have provided a minimal reproducible example
- [x] I have included the versions of fastlite, fastcore, and fasthtml
- [x] I understand that this is a volunteer open source project with no commercial support.

**Additional context**
This appears to be a leftover artifact from the transition mentioned in the changelog for version 0.1.10:

```
## 0.1.10

### Dependencies

* Update for fastcore XT to FT name change
```

It seems that in `components.py`, line 85, the type annotation still uses `XT` instead of `FT`, but `XT` is no longer defined in the namespace.

Looking at the error message, the Python interpreter even suggests the correct fix: "Did you mean: 'FT'?", supporting the hypothesis that this is a missed rename.

The fix would likely involve updating the `fill_form` function signature in components.py from:

```python
def fill_form(form:XT, obj)->XT:
```

to:

```python
def fill_form(form:FT, obj)->FT:
```

- [BUG] Pico Search component doesn't work as expected ([#484](https://github.com/AnswerDotAI/fasthtml/issues/484))
  - **Describe the bug**
Using the Pico Search component does not reproduce UI elements like in teh pico docs https://picocss.com/docs/group#search

**Minimal Reproducible Example**
```python
from fasthtml.common import *
app, rt = fast_app(
    hdrs=(picolink,),
)
def search_form():
    return Search(
        Input(name="search", type="search", placeholder="search"),
        Input(type="submit", value="search"),cls="container")
```
result:
```html
<search class="container">       
       <input name="search" type="search" placeholder="search">
       <input type="submit" value="search">
</search>
```
![image](https://github.com/user-attachments/assets/b1482671-4380-4ea8-8090-565961c7b477)

**Expected behavior**
Expected: 
![image](https://github.com/user-attachments/assets/038978ae-6162-4082-ae26-c6b8b15687c3)
 
Visually, the textbox has the correct style but the submit button does not.
Expected html per picocss docs
```html
<form role="search">
  <input name="search" type="search" placeholder="Search" />
  <input type="submit" value="Search" />
</form>
```
**Environment Information**
Please provide the following version information:
- fastlite version: 0.0.11
- fastcore version: 1.7.10
- fasthtml version: 0.6.9

**Confirmation**
Please confirm the following:
- [x] I have read the FAQ (https://docs.fastht.ml/explains/faq.html)
- [x] I have provided a minimal reproducible example
- [x] I have included the versions of fastlite, fastcore, and fasthtml
- [x] I understand that this is a volunteer open source project with no commercial support.

**Additional context**
Add any other context about the problem here.

**Screenshots**
If applicable, add screenshots to help explain your problem.

- [BUG] FastHTML by Example should use a redirect for POST instead of render ([#389](https://github.com/AnswerDotAI/fasthtml/issues/389))
  - **Describe the bug**
This is more a "bug"/question about the tutorial. I was following along and noticed when I got to the [WebPage->Web App](https://docs.fastht.ml/tutorials/by_example.html#web-page---web-app) section that things did not work in the browser. 

1. There seemed to be some loop (that I can not repo) that caused the page to keep adding the last item I submitted
2. After you add an items and get back to the home page, if you refresh the page it wants to do another form submission 

Feels like both issues are because the POST renders the home page instead of redirecting

```
@app.post("/")
def add_message(data:str):
    messages.append(data)
    return home()
```

vs

```
@app.post("/")
def add_message(data: str):
    messages.append(data)
    return RedirectResponse("/", status_code=302)
```

**Expected behavior**
If I am follow a demo, the demo produces best practice web patterns. I had to go looking through GitHub example repos to even find that RedirectResponse is the right way to do this. 

**Environment Information**
Please provide the following version information:
- fastlite version: "0.0.9"
- fastcore version:"1.7.3"
- fasthtml version:"0.5.1"

**Confirmation**
Please confirm the following:
- [x] I have read the FAQ (https://docs.fastht.ml/explains/faq.html)
- [x] I have provided a minimal reproducible example
- [x] I have included the versions of fastlite, fastcore, and fasthtml
- [x] I understand that this is a volunteer open source project with no commercial support.

**Additional context**
Note: problem #1 might have been because I was using an earlier version of fasthtml and recently updated, but #2 to exists still.


## 0.12.36

### Bugs Squashed

- Bump toast z-index to 1090 so toasts appear above modals ([#807](https://github.com/AnswerDotAI/fasthtml/pull/807)), thanks to [@erikgaas](https://github.com/erikgaas)
- Fix StreamingResponse handling in `_resp` ([#792](https://github.com/AnswerDotAI/fasthtml/pull/792)), thanks to [@kenfj](https://github.com/kenfj)
- Add `get_client` ([#800](https://github.com/AnswerDotAI/fasthtml/issues/800))
- Handle str in `show` ([#796](https://github.com/AnswerDotAI/fasthtml/issues/796))

### Bugs Squashed

- Use updated railway return val ([#798](https://github.com/AnswerDotAI/fasthtml/issues/798))
- Only strip newlines when parsing strings ([#797](https://github.com/AnswerDotAI/fasthtml/pull/797)), thanks to [@johnowhitaker](https://github.com/johnowhitaker)
- Fix StreamingResponse handling in `_resp` ([#792](https://github.com/AnswerDotAI/fasthtml/pull/792)), thanks to [@kenfj](https://github.com/kenfj)


## 0.12.33

### New Features

- `render_ft` kw param ([#791](https://github.com/AnswerDotAI/fasthtml/issues/791))


## 0.12.32

### New Features

- Use TestClient to render HTMX components ([#790](https://github.com/AnswerDotAI/fasthtml/issues/790))


## 0.12.31

### New Features

- Use https for canonical ([#789](https://github.com/AnswerDotAI/fasthtml/issues/789))


## 0.12.30

### New Features

- Add LsJson, robots.txt, and sitemap.xml ([#786](https://github.com/AnswerDotAI/fasthtml/issues/786))


## 0.12.29

### New Features

- Add `StaticNoCache` ([#783](https://github.com/AnswerDotAI/fasthtml/issues/783))


## 0.12.28


### Bugs Squashed

- fix broken toasts ([#782](https://github.com/AnswerDotAI/fasthtml/pull/782)), thanks to [@comhar](https://github.com/comhar)
- Fix Railway CLI command ([#781](https://github.com/AnswerDotAI/fasthtml/pull/781)), thanks to [@knollfear](https://github.com/knollfear)


## 0.12.27

### Bugs Squashed

- Correct afterware resp objects ([#778](https://github.com/AnswerDotAI/fasthtml/pull/778)), thanks to [@erikgaas](https://github.com/erikgaas)


## 0.12.26

### Bugs Squashed

- update afterware arg parsing ([#777](https://github.com/AnswerDotAI/fasthtml/pull/777)), thanks to [@comhar](https://github.com/comhar)


## 0.12.25

### New Features

- Use kw args for handler params ([#771](https://github.com/AnswerDotAI/fasthtml/issues/771))


## 0.12.24

### New Features

- Update htmx and ext versions ([#767](https://github.com/AnswerDotAI/fasthtml/issues/767))


## 0.12.23

### New Features

- Add `__from_request__` ([#765](https://github.com/AnswerDotAI/fasthtml/issues/765))
- Handle async `__from_request__` ([#766](https://github.com/AnswerDotAI/fasthtml/issues/766))


## 0.12.22

### New Features

- Support dict params in ws routes ([#759](https://github.com/AnswerDotAI/fasthtml/issues/759))
- Add a small JS snippet to support HTMX requests for toasts
- support x-forwarded-host as source for redirect ([#755](https://github.com/AnswerDotAI/fasthtml/pull/755)), thanks to [@erikgaas](https://github.com/erikgaas)
- Overhaul `adv_app` with more modern idioms ([#754](https://github.com/AnswerDotAI/fasthtml/issues/754))

### Bugs Squashed

- Use data instead of json for oauth ([#761](https://github.com/AnswerDotAI/fasthtml/pull/761)), thanks to [@erikgaas](https://github.com/erikgaas)


## 0.12.21

### New Features

- Handle empty host in `HTMX()` ([#752](https://github.com/AnswerDotAI/fasthtml/issues/752))


## 0.12.20

### New Features

- Add `set_lifespan` ([#744](https://github.com/AnswerDotAI/fasthtml/issues/744))
- Add title= kwarg to `fast_app()` constructor ([#740](https://github.com/AnswerDotAI/fasthtml/pull/740)), thanks to [@mmacpherson](https://github.com/mmacpherson)
- Allow any Mapping children to specify attributes. fix #737 ([#738](https://github.com/AnswerDotAI/fasthtml/pull/738)), thanks to [@gazpachoking](https://github.com/gazpachoking)

### Bugs Squashed

- Correct treatment of empty/boolean attributes in the html2ft function ([#732](https://github.com/AnswerDotAI/fasthtml/pull/732)), thanks to [@renatodamas](https://github.com/renatodamas)
- html2ft handling empty attribute ([#731](https://github.com/AnswerDotAI/fasthtml/issues/731))
- Toasts inserted at bottom of page ([#703](https://github.com/AnswerDotAI/fasthtml/issues/703))


## 0.12.19

### New Features

- `seeded` option for `unqid` ([#741](https://github.com/AnswerDotAI/fasthtml/issues/741))


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

- srcdoc support in `show` ([#717](https://github.com/AnswerDotAI/fasthtml/issues/717))
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

