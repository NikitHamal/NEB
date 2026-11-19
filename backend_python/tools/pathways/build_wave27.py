"""Builds api/data/pathways/wave27.json from w27_campus.py (NPCA campuses placed with the local-level list) and, when present,
w27_sites.py (PROVIDER_UPDATE, WEBSITE_DROP, PROVIDERS_ADD, WHERE_ADD), w27_abroad.py (ABROAD_UPDATE), w27_faq.py (FAQ_ADD).

Run: python3 backend_python/tools/pathways/build_wave27.py   (never hand edit wave27.json)
"""
import importlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent.parent))
DATA = HERE.parent.parent / 'api' / 'data' / 'pathways'
if (DATA / 'wave27.json').exists():
    (DATA / 'wave27.json').unlink()
from api import pathways as P  # noqa: E402
import w26_campus as C26  # noqa: E402
import w27_campus as C  # noqa: E402

base = P.payload()
by_id = {p['id']: p for p in base['providers']}
by_d = {}
for p in base['providers']:
    k = re.sub(r'[^a-z]', '', re.sub(r'\(.*?\)', '', p['name'].lower()).replace('multiple', '').replace('campus', ''))
    by_d.setdefault(p['district'], []).append(k)

ROUTE_NAME = {'bed': 'B.Ed.', 'med': 'M.Ed.', 'bbs': 'BBS', 'mbs': 'MBS', 'ba': 'BA', 'ma': 'MA', 'bicte': 'BICTE', 'bba': 'BBA',
              'bca': 'BCA', 'bsc-science': 'B.Sc.', 'bbm': 'BBM', 'bim': 'BIM', 'mba': 'MBA', 'bhm': 'BHM', 'bfa': 'BFA',
              'bsc-csit': 'B.Sc. CSIT', 'bit': 'BIT'}
providers_add, where_add = [], {}


def add(row, routes):
    assert row['id'] not in by_id and row['id'] not in {x['id'] for x in providers_add}, row['id']
    providers_add.append(row)
    for r in routes:
        assert r in {x['id'] for x in base['routes']}, r
        where_add.setdefault(r, []).append(row['id'])


for r, name in C.npca_rows(by_d):
    prog = ', '.join(ROUTE_NAME[x] for x in r['routes'])
    note = C.NOTE + f'Programmes listed there: {prog}.'
    if r.get('est_bs'):
        note += f" Established {r['est_bs']} BS."
    if r.get('qaa'):
        note += f" QAA status on NPCA: {r['qaa']}."
    ph = re.sub(r'\D', '', r.get('phone') or '')
    if 7 <= len(ph) <= 10:
        note += f" Phone {r['phone']}."
    if r['palika']:
        note += f" District placed from the MoFAGA local level list ({', '.join(r['palika'])} is a local level of {r['district']})."
    else:
        note += f" District placed from the GeoNames place list and confirmed by the campus website, which names {r['district']}."
    place = C.PLACE.get(r['npca_id'])
    if not place:
        place = C26._tidy(r['addr'], r['district'])
        if place.isupper() or place.islower():
            place = place.title()
    row = {'id': f"p-w27-npca-{r['npca_id']}", 'name': name, 'kind': 'Campus', 'sector': 'Community', 'district': r['district'],
           'place': place, 'note': note}
    if r['npca_id'] not in C.NO_WEB and r.get('web') and isinstance(r.get('live'), int) and 0 < r['live'] < 400:
        row['website'] = r['web']
    add(row, r['routes'])

out = {'providers_add': providers_add, 'where_add': where_add}
try:
    S = importlib.import_module('w27_sites')
except ImportError:
    S = None
if S:
    for row, routes in getattr(S, 'PROVIDERS_ADD', []):
        add(row, routes)
    out['provider_update'] = dict(getattr(S, 'PROVIDER_UPDATE', {}))
    out['website_drop'] = list(getattr(S, 'WEBSITE_DROP', []))
    for pid in list(out['provider_update']) + out['website_drop']:
        assert pid in by_id or pid in {x['id'] for x in providers_add}, pid
    for r, ids in getattr(S, 'WHERE_ADD', {}).items():
        where_add.setdefault(r, []).extend(ids)
for mod, attr, key in (('w27_abroad', 'ABROAD_UPDATE', 'abroad_update'), ('w27_faq', 'FAQ_ADD', 'faq_add')):
    try:
        m = importlib.import_module(mod)
    except ImportError:
        continue
    out[key] = getattr(m, attr)
text = json.dumps(out, ensure_ascii=False, indent=1)
assert '\u2014' not in text and '\u2013' not in text and '--' not in text
assert not [ch for ch in text if ord(ch) > 0x2fff]
(DATA / 'wave27.json').write_text(text + '\n', encoding='utf-8')
print('wave27.json', len(text), 'bytes;', len(providers_add), 'providers;', sum(len(v) for v in where_add.values()), 'route links;',
      len(out.get('provider_update', {})), 'site updates;', len(out.get('website_drop', [])), 'sites dropped')
