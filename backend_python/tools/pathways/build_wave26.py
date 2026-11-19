"""Builds api/data/pathways/wave26.json from w26_campus.py, w26_sites.py (and w26_abroad.py / w26_faq.py when present).

Wave 26 (adds to waves 12 to 25, no overlap):
- website audit: 38 dead guessed domains replaced from the official TU list / NPCA / own pages or dropped, 10 generic tu.edu.np links
- 6 TU constituent campuses missing from the dataset (official TU campus list)
- community campuses from the NPCA member list (programmes and websites verified live)
Run: python3 backend_python/tools/pathways/build_wave26.py   (never hand edit wave26.json)
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent.parent))
DATA = HERE.parent.parent / 'api' / 'data' / 'pathways'
if (DATA / 'wave26.json').exists():
    (DATA / 'wave26.json').unlink()
from api import pathways as P  # noqa: E402
import w26_campus as C  # noqa: E402
import w26_sites as S  # noqa: E402

base = P.payload()
by_id = {p['id']: p for p in base['providers']}
by_d = {}
for p in base['providers']:
    k = re.sub(r'[^a-z]', '', re.sub(r'\(.*?\)', '', p['name'].lower()).replace('multiple', '').replace('campus', ''))
    by_d.setdefault(p['district'], []).append(k)

npca = {r['npca_id']: r for r in json.loads((HERE / 'npca_campuses.json').read_text(encoding='utf-8'))}
providers_add, where_add = [], {}


def add(row, routes):
    assert row['id'] not in by_id and row['id'] not in {x['id'] for x in providers_add}, row['id']
    providers_add.append(row)
    for r in routes:
        where_add.setdefault(r, []).append(row['id'])


for suf, name, dist, place, site, note, routes in C.TU_ROWS:
    add({'id': 'p-w26-' + suf, 'name': name, 'kind': 'Campus', 'sector': 'Public', 'district': dist, 'place': place,
         'website': site, 'note': note}, routes)

ROUTE_NAME = {'bed': 'B.Ed.', 'med': 'M.Ed.', 'bbs': 'BBS', 'mbs': 'MBS', 'ba': 'BA', 'ma': 'MA', 'bicte': 'BICTE', 'bba': 'BBA',
              'bca': 'BCA', 'bsc-science': 'B.Sc.', 'bbm': 'BBM', 'bim': 'BIM', 'mba': 'MBA', 'bhm': 'BHM', 'bfa': 'BFA',
              'bsc-csit': 'B.Sc. CSIT', 'bit': 'BIT'}
for r, name in C.npca_rows(by_d):
    prog = ', '.join(ROUTE_NAME[x] for x in r['routes'])
    note = C.NPCA_NOTE + f'Programmes listed there: {prog}.'
    if r.get('est_bs'):
        note += f" Established {r['est_bs']} BS."
    if r.get('qaa'):
        note += f" QAA status on NPCA: {r['qaa']}."
    ph = re.sub(r'\D', '', r.get('phone') or '')
    if 7 <= len(ph) <= 10:
        note += f" Phone {r['phone']}."
    row = {'id': f"p-w26-npca-{r['npca_id']}", 'name': name, 'kind': 'Campus', 'sector': 'Community', 'district': r['district'],
           'place': C.PLACE_FIX.get(r['npca_id']) or C._tidy(r['addr'], r['district']).title() if (C.PLACE_FIX.get(r['npca_id']) or C._tidy(r['addr'], r['district'])).isupper() else (C.PLACE_FIX.get(r['npca_id']) or C._tidy(r['addr'], r['district'])), 'note': note}
    if r['npca_id'] not in C.NO_WEB and r.get('web') and isinstance(r.get('live'), int) and 0 < r['live'] < 400:
        row['website'] = r['web']
    add(row, r['routes'])

provider_update, website_drop = {}, list(S.DROP)
for pid, host in S.TU_OFFICIAL.items():
    provider_update[pid] = {'website': f'https://{host}.tu.edu.np'}
for pid, nid in S.NPCA_IDS.items():
    r = npca[nid]
    assert r['web'] and 0 < r['live'] < 400, (pid, nid)
    provider_update[pid] = {'website': r['web']}
for pid, url in S.OWN_SITES.items():
    provider_update[pid] = {'website': url}
for pid in list(provider_update) + website_drop:
    assert pid in by_id, pid
assert not set(provider_update) & set(website_drop)

out = {'providers_add': providers_add, 'where_add': where_add, 'provider_update': provider_update, 'website_drop': website_drop}
for mod, key in (('w26_abroad', 'abroad_update'), ('w26_faq', 'faq_add')):
    try:
        m = __import__(mod)
    except ImportError:
        continue
    for k in ('ABROAD_UPDATE', 'FAQ_ADD', 'ABROAD_ADD_FIELDS'):
        if hasattr(m, k):
            out[{'ABROAD_UPDATE': 'abroad_update', 'FAQ_ADD': 'faq_add', 'ABROAD_ADD_FIELDS': 'abroad_update'}[k]] = getattr(m, k)
text = json.dumps(out, ensure_ascii=False, indent=1)
assert '\u2014' not in text and '\u2013' not in text and '--' not in text
assert not [ch for ch in text if ord(ch) > 0x2fff]
(DATA / 'wave26.json').write_text(text + '\n', encoding='utf-8')
print('wave26.json', len(text), 'bytes;', len(providers_add), 'providers;', sum(len(v) for v in where_add.values()), 'route links;',
      len(provider_update), 'site updates;', len(website_drop), 'sites dropped')
for p in providers_add:
    if 'npca' in p['id']:
        print(p['id'], '|', p['name'][:45], '|', p['district'], '|', p['place'][:25], '|', p.get('website', '-'))
