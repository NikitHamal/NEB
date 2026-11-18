#!/usr/bin/env python3
"""Build the static data files for the Pathways v5 concept.

Reads the same merged payload the web page and the Android app use (`backend_python/api/pathways.py`) and writes
`data.js` (window.PW) and `map-data.js` (window.NM_DATA, the 77-district map) next to this file, so the concept works
from file:// and from GitHub Pages with no server. Run from the repo root: python3 concepts/pathways-v5/build.py
"""
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
API = ROOT / 'backend_python' / 'api' / 'pathways.py'
MAP = ROOT / 'backend_python' / 'web' / 'static' / 'web' / 'data' / 'nepal_map.json'


def load():
    spec = importlib.util.spec_from_file_location('pw', API)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.payload()


def main():
    p = load()
    stats = {
        'routes': len(p['routes']), 'careers': len(p['careers']), 'providers': len(p['providers']),
        'scholarships': len(p['scholarships']), 'abroad': len(p['abroad']), 'govt': len(p['govt']),
        'guides': len(p['guides']), 'faq': len(p['faq']),
        'districts': len({x['district'] for x in p['providers']}),
    }
    p['stats'] = stats
    body = json.dumps(p, separators=(',', ':'), ensure_ascii=False)
    (HERE / 'data.js').write_text('window.PW=' + body + ';\n', encoding='utf-8')
    m = json.dumps(json.load(open(MAP, encoding='utf-8')), separators=(',', ':'))
    (HERE / 'map-data.js').write_text('window.NM_DATA=' + m + ';\n', encoding='utf-8')
    print('data.js', len(body) // 1024, 'KB', stats)


if __name__ == '__main__':
    main()
