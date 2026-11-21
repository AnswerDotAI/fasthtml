import json
from fasthtml.vite import vite_headers

def test_vite_headers_transitive_dedupe_and_cycles(tmp_path):
    manifest = {
        'src/index.js': dict(file='assets/index.js', css=['assets/app.css'], imports=['_a.js', '_b.js']),
        '_a.js': dict(file='assets/a.js', css=['assets/shared.css', 'assets/app.css'], imports=['_shared.js', 'src/index.js']),
        '_b.js': dict(file='assets/b.js', imports=['_shared.js']),
        '_shared.js': dict(file='assets/shared.js', css=['assets/shared.css'], imports=['_a.js']),
        'unused.js': dict(file='assets/unused.js', css=['assets/unused.css']),
    }
    mdir = tmp_path/'.vite'
    mdir.mkdir()
    (mdir/'manifest.json').write_text(json.dumps(manifest))

    hdrs = vite_headers(tmp_path, base='/frontend/')
    tags = [(h.tag, h.attrs) for h in hdrs]
    assert tags == [
        ('link', {'rel': 'stylesheet', 'href': '/frontend/assets/app.css'}),
        ('link', {'rel': 'stylesheet', 'href': '/frontend/assets/shared.css'}),
        ('script', {'type': 'module', 'src': '/frontend/assets/index.js'}),
        ('link', {'rel': 'modulepreload', 'href': '/frontend/assets/shared.js'}),
        ('link', {'rel': 'modulepreload', 'href': '/frontend/assets/a.js'}),
        ('link', {'rel': 'modulepreload', 'href': '/frontend/assets/b.js'}),
    ]

    rel = [h.attrs.get('href') or h.attrs.get('src') for h in vite_headers(tmp_path, base='./')]
    assert rel[0] == './assets/app.css' and rel[2] == './assets/index.js'

