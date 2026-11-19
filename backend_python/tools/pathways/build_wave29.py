"""Builds api/data/pathways/wave29.json from w29_lbu.py (LBU campuses, NOU note) and, when present, w29_abroad.py (ABROAD_UPDATE),
w29_faq.py (FAQ_ADD), w29_more.py (extra upper case keys written as they are, for example PROVIDER_UPDATE).

Run: python3 backend_python/tools/pathways/build_wave29.py   (never hand edit wave29.json)
"""
import importlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent.parent))
DATA = HERE.parent.parent / 'api' / 'data' / 'pathways'
if (DATA / 'wave29.json').exists():
    (DATA / 'wave29.json').unlink()
from api import pathways as P  # noqa: E402
import w29_lbu as L  # noqa: E402
import w29_nsu as N  # noqa: E402

base = P.payload()
by_id = {p['id']: p for p in base['providers']}
route_ids = {r['id'] for r in base['routes']}

providers_add, where_add, note_add = [], {}, {}


def link(pid, routes):
    for r in routes:
        assert r in route_ids, r
        where_add.setdefault(r, [])
        if pid not in where_add[r]:
            where_add[r].append(pid)


for pid, name, kind, sector, dist, place, site, progs, routes, extra in L.CAMPUSES:
    assert pid not in by_id, pid
    providers_add.append({'id': pid, 'name': name, 'kind': kind, 'sector': sector, 'district': dist, 'place': place, 'website': site,
                          'note': f'Lumbini Buddhist University affiliated or constituent campus ({L.CK}, lbu.edu.np). Programmes on the LBU page: {progs}. {extra}'})
    link(pid, routes)

for pid, name, dist, place, phone, extra in N.ROWS:
    assert pid not in by_id, pid
    providers_add.append({'id': pid, 'name': name, 'kind': 'Campus', 'sector': 'Public', 'district': dist, 'place': place,
                          'note': (f'Nepal Sanskrit University constituent or affiliated Vidyapeeth, phone {phone} ({N.CK}; collegenp.com, Edusanjal, Justapedia, Falano College '
                                   f'list it; nsu.edu.np did not answer). {extra} The lists do not name its programmes or seats, so confirm the current intake with the campus.').replace('  ', ' ')})
    link(pid, N.ROUTES)
for pid, text in N.NOTE_ADD.items():
    assert pid in by_id, pid
    note_add[pid] = text
assert 'p-lbu' in by_id and 'p-nou' in by_id
note_add['p-lbu'] = L.LBU_NOTE
link('p-lbu', L.LBU_ROUTES)
note_add['p-nou'] = L.NOU_NOTE
note_add['p-nsu'] = N.NSU_NOTE
link('p-nou', L.NOU_ROUTES)

out = {'providers_add': providers_add, 'where_add': where_add, 'note_add': note_add}
for mod, attr, key in (('w29_abroad', 'ABROAD_UPDATE', 'abroad_update'), ('w29_faq', 'FAQ_ADD', 'faq_add')):
    try:
        m = importlib.import_module(mod)
    except ImportError:
        continue
    out[key] = getattr(m, attr)
try:
    M = importlib.import_module('w29_more')
    for key in dir(M):
        if key.isupper() and not key.startswith('_'):
            out[key.lower()] = getattr(M, key)
except ImportError:
    pass
text = json.dumps(out, ensure_ascii=False, indent=1)
for _bad in ('--', '\u2014', '\u2013'):
    if _bad in text:
        _i = text.index(_bad)
        print('BAD', repr(text[_i - 80:_i + 40]))
assert '\u2014' not in text and '\u2013' not in text and '--' not in text
assert not [ch for ch in text if ord(ch) > 0x2fff]
(DATA / 'wave29.json').write_text(text + '\n', encoding='utf-8')
print('wave29.json', len(text), 'bytes;', len(providers_add), 'providers;', sum(len(v) for v in where_add.values()), 'route links;', len(note_add), 'notes;',
      len(out.get('abroad_update', {})), 'abroad;', len(out.get('faq_add', [])), 'faq')
