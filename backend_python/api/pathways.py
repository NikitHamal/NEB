"""Pathways: the study and career dataset shared by the web page and the Android app.

The JSON lives in `api/data/pathways/` (routes_*.json, careers.json, places.json). It is merged once per process
and served as one payload with an ETag. Money is NPR, monthly for salaries and total programme cost for fees; all
figures are indicative ranges reviewed in `REVIEWED`, and every screen says so.
"""
import hashlib
import json
from functools import lru_cache
from pathlib import Path

DATA = Path(__file__).resolve().parent / 'data' / 'pathways'
REVIEWED = '2026-05'


def _load(name):
    with open(DATA / name, encoding='utf-8') as fh:
        return json.load(fh)


@lru_cache(maxsize=1)
def payload():
    a, b, c = _load('routes_a.json'), _load('routes_b.json'), _load('routes_c.json')
    places = _load('places.json')
    routes = a['routes'] + b['routes'] + c['routes']
    for r in routes:
        r['where'] = list(dict.fromkeys(r.get('where') or []))
    data = {
        'reviewed': REVIEWED,
        'stages': a['stages'],
        'routes': routes,
        'careers': _load('careers.json')['careers'],
        'providers': places['providers'],
        'scholarships': places['scholarships'],
        'abroad': places['abroad'],
    }
    body = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    data['etag'] = hashlib.md5(body.encode('utf-8')).hexdigest()[:16]
    return data


def problems(data=None):
    """Broken references, used by the tests so a typo in the JSON fails CI instead of a screen."""
    d = data or payload()
    out = []
    ids = {k: {x['id'] for x in d[k]} for k in ('routes', 'careers', 'providers', 'scholarships')}
    stages = {s['id'] for s in d['stages']}
    for r in d['routes']:
        if r['stage'] not in stages:
            out.append(f"{r['id']}: stage {r['stage']}")
        for key, pool in (('careers', 'careers'), ('next', 'routes'), ('where', 'providers')):
            for ref in r.get(key, []):
                if ref not in ids[pool]:
                    out.append(f"{r['id']}.{key}: {ref}")
        if len(r['fee']) != 2 or r['fee'][0] > r['fee'][1]:
            out.append(f"{r['id']}: fee")
    for a in d['abroad']:
        for ref in a.get('scholarships', []):
            if ref not in ids['scholarships']:
                out.append(f"{a['id']}: scholarship {ref}")
    return out
