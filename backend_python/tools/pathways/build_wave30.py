"""Builds api/data/pathways/wave30.json from w30_mu.py (Mid-West University 2083/84 notice), w30_sites.py (checked websites),
w30_sch.py (domestic scholarships) and w30_faq.py.

Run: python3 backend_python/tools/pathways/build_wave30.py   (never hand edit wave30.json)
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent.parent))
DATA = HERE.parent.parent / 'api' / 'data' / 'pathways'
if (DATA / 'wave30.json').exists():
    (DATA / 'wave30.json').unlink()
from api import pathways as P  # noqa: E402
import w30_mu as M  # noqa: E402
import w30_sites as S  # noqa: E402
import w30_sch as C  # noqa: E402
import w30_faq as F  # noqa: E402

base = P.payload()
by_id = {p['id']: p for p in base['providers']}
route_ids = {r['id'] for r in base['routes']}
used_sites = {(p.get('website') or '').rstrip('/').split('//')[-1].replace('www.', '') for p in base['providers']}
providers_add, where_add, note_add, provider_update = [], {}, {}, {}


def link(pid, routes):
    for r in routes:
        assert r in route_ids, r
        where_add.setdefault(r, [])
        if pid not in where_add[r]:
            where_add[r].append(pid)


for pid, name, kind, sector, dist, place, site, progs, routes, extra in M.NEW:
    assert pid not in by_id, pid
    row = {'id': pid, 'name': name, 'kind': kind, 'sector': sector, 'district': dist, 'place': place}
    if site:
        row['website'] = site
    row['note'] = f'Listed on the Mid-West University 2083/84 bachelor admission notice ({M.CK}) with: {progs}. {extra}'
    providers_add.append(row)
    link(pid, routes)

assert 'p-mu' in by_id
note_add['p-mu'] = M.MU_NOTE
link('p-mu', M.MU_ROUTES)
provider_update['p-mu'] = {'website': 'https://mwu.edu.np'}
for pid, (progs, routes, phones, addr) in M.CAMPUS_NOTES.items():
    assert pid in by_id, pid
    note_add[pid] = f'Mid-West University 2083/84 notice ({M.CK}): {addr}; programmes open: {progs}. Phone {phones}.'
    link(pid, routes)

sites = 0
for pid, (url, name, title) in S.WEBSITES.items():
    assert pid in by_id, pid
    assert not by_id[pid].get('website'), pid
    key = url.rstrip('/').split('//')[-1].replace('www.', '')
    assert key not in used_sites, (pid, key)
    used_sites.add(key)
    provider_update.setdefault(pid, {})['website'] = url
    note_add[pid] = (note_add.get(pid, '') + ' Website checked 19 Nov 2026: the page names the college and its town or district.').strip()
    sites += 1
print('websites', sites)

out = {'providers_add': providers_add, 'where_add': where_add, 'note_add': note_add, 'provider_update': provider_update,
       'scholarships_add': C.SCHOLARSHIPS_ADD, 'scholarship_extra': C.SCHOLARSHIP_EXTRA, 'faq_add': F.FAQ_ADD}
text = json.dumps(out, ensure_ascii=False, indent=1)
for _bad in ('--', '\u2014', '\u2013'):
    if _bad in text:
        _i = text.index(_bad)
        print('BAD', repr(text[_i - 80:_i + 40]))
assert '\u2014' not in text and '\u2013' not in text and '--' not in text
assert not [ch for ch in text if ord(ch) > 0x2fff]
(DATA / 'wave30.json').write_text(text + '\n', encoding='utf-8')
print('wave30.json', len(text), 'bytes;', len(providers_add), 'providers;', sum(len(v) for v in where_add.values()), 'route links;', len(note_add), 'notes;',
      len(C.SCHOLARSHIPS_ADD), 'scholarships;', len(F.FAQ_ADD), 'faq')
