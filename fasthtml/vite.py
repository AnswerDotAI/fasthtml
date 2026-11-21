"""Vite+ asset headers and development server integration for FastHTML

Import explicitly from `fasthtml.vite` rather than `fasthtml.common`. Production apps mount a built `dist/` directory and inject hashed asset tags from `.vite/manifest.json`. Development mode (`dev=True`) runs `vp dev` inside the application lifespan for hot module replacement.

```python
from fasthtml.common import FastHTML
from fasthtml.vite import add_vite, vite_headers

app = FastHTML()
add_vite(app, directory='.')
```
"""

__all__ = ['vite_headers', 'add_vite']

import asyncio, json
from pathlib import Path
from .components import Link, Script
from .core import FastHTML, StaticImmutable

def vite_headers(
    outdir, # Build directory containing `.vite/manifest.json`
    entry='src/index.js', # Entry key in the Vite manifest
    base='/', # Public URL prefix, matching Vite's build `base`
):
    "Read a Vite manifest and return its stylesheets, entry script, and module preloads."
    manifest = json.loads((Path(outdir)/'.vite/manifest.json').read_text())
    def _imported(name, seen):
        for imp in manifest[name].get('imports', []):
            if imp in seen: continue
            seen.add(imp)
            yield from _imported(imp, seen)
            yield manifest[imp]

    def _url(path): return f"{base.rstrip('/')}/{path.lstrip('/')}"
    entry_chunk = manifest[entry]
    imported = list(_imported(entry, {entry}))
    css = dict.fromkeys([*entry_chunk.get('css', []), *(c for chunk in imported for c in chunk.get('css', []))])
    return [
        *(Link(rel='stylesheet', href=_url(p)) for p in css),
        Script(type='module', src=_url(entry_chunk['file'])),
        *(Link(rel='modulepreload', href=_url(chunk['file'])) for chunk in imported),
    ]

def add_vite(
    app:FastHTML, # FastHTML application to configure
    entry_file='index.js', # Entry filename under `<dirname>/src/`
    dirname='frontend', # Subdirectory holding the Vite project, also used as URL prefix
    directory='.', # Base directory containing `dirname`
    dev=False, # Own a localhost `vp dev` server with hot module replacement
    port=5173, # Port for the `vp dev` server when `dev=True`
):
    "Configure a FastHTML app to serve Vite+ assets or own a localhost `vp dev` server."
    pwd = Path(directory).resolve()/dirname
    if dev:
        url = f'http://127.0.0.1:{port}/{dirname}'
        previous = app.router.lifespan_context
        async def lifespan(app):
            proc = await asyncio.create_subprocess_exec(
                'vp', 'dev', '--host', '127.0.0.1', '--port', str(port), '--strictPort',
                '--base', f'/{dirname}/', '--logLevel', 'warn', cwd=pwd)
            try:
                async with asyncio.timeout(10):
                    while True:
                        if proc.returncode is not None: raise RuntimeError(f'Vite exited with status {proc.returncode}')
                        try:
                            _,w = await asyncio.open_connection('127.0.0.1', port)
                            w.close()
                            await w.wait_closed()
                            break
                        except OSError: await asyncio.sleep(0.05)
                app.hdrs[0:0] = [Script(type='module', src=f'{url}/@vite/client'),
                    Script(type='module', src=f'{url}/src/{entry_file}')]
                async with previous(app) as state: yield state
            finally:
                if proc.returncode is None: proc.terminate()
                await proc.wait()
        app.set_lifespan(lifespan)
        return
    outdir = pwd/'dist'
    app.mount(f'/{dirname}', app=StaticImmutable(directory=outdir), name=dirname)
    @app.on_event('startup')
    def _(): app.hdrs[0:0] = vite_headers(outdir, entry=f'src/{entry_file}', base=f'/{dirname}/')
