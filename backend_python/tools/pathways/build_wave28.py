"""Builds api/data/pathways/wave28.json from w28_pu.py (Purbanchal University official college lists) and, when present,
w28_abroad.py (ABROAD_UPDATE), w28_faq.py (FAQ_ADD), w28_more.py (extra keys written as they are).

Run: python3 backend_python/tools/pathways/build_wave28.py   (never hand edit wave28.json)
"""
import importlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent.parent))
DATA = HERE.parent.parent / 'api' / 'data' / 'pathways'
if (DATA / 'wave28.json').exists():
    (DATA / 'wave28.json').unlink()
from api import pathways as P  # noqa: E402
import w28_pu as W  # noqa: E402
import w28_rju as R  # noqa: E402

base = P.payload()
by_id = {p['id']: p for p in base['providers']}
route_ids = {r['id'] for r in base['routes']}
existing = {}
for p in base['providers']:
    existing.setdefault((W.key(p['name']), p['district']), p['id'])
npca = {(W.key(x['name']), x['district']) for x in json.loads((HERE / 'npca_campuses.json').read_text(encoding='utf-8'))}

providers_add, where_add, route_seats, note_add = [], {}, {}, {}
stats = {'new': 0, 'matched': 0, 'skipped': 0}


def label(it):
    return it['text'].replace('  ', ' ')


for (k, dist), e in W.rows().items():
    if (k, dist) in W.SKIP:
        stats['skipped'] += 1
        continue
    pid = W.MATCH.get((k, dist)) or existing.get((k, dist))
    items = e['items']
    routes = list(dict.fromkeys(i['route'] for i in items if i['route']))
    seats = {}
    for i in items:
        if i['route'] and i['seats']:
            seats[i['route']] = max(seats.get(i['route'], 0), i['seats'])
    facs = ' and '.join(W.FAC_NAME[f] for f in dict.fromkeys(e['facs']))
    listing = '; '.join(label(i) for i in items).rstrip('.')
    if pid:
        stats['matched'] += 1
        assert pid in by_id, pid
        note_add[pid] = (f"Purbanchal University official college list ({facs}, purbanchaluniversity.edu.np, checked 19 Nov 2026) approves "
                         f"these programmes and yearly quotas here: {listing}.")
        have = by_id[pid].get('route_seats') or {}
        new_seats = {r: s for r, s in seats.items() if r not in have}
        if new_seats:
            route_seats[pid] = new_seats
    else:
        stats['new'] += 1
        pid = 'p-w28-pu-' + W.slug(e['name']) + '-' + dist.lower().replace(' ', '')
        sector = 'Community' if (k, dist) in npca else W.sector_of(e['name'], set()) or 'Not stated'
        kind = 'Campus' if 'campus' in e['name'].lower() else 'College'
        undergrad = sum(s for r, s in seats.items() if r not in W.POSTGRAD)
        sec_txt = ' The PU list does not give the sector.' if sector == 'Not stated' else ''
        if (k, dist) in npca:
            sec_txt = ' Also on the NPCA community campus member list.'
        row = {'id': pid, 'name': e['name'], 'kind': kind, 'sector': sector, 'district': dist, 'place': e['place'],
               'note': (f"Purbanchal University affiliated college at {e['place']}, listed on the PU {facs} page "
                        f"(purbanchaluniversity.edu.np, checked 19 Nov 2026) with approved programmes and quotas: {listing}.{sec_txt} "
                        "Quotas are the university approval, not a fee or admission guarantee; confirm the current intake with the college.")}
        if undergrad:
            row['seats'] = undergrad
        if seats:
            row['route_seats'] = seats
        assert pid not in by_id and pid not in {x['id'] for x in providers_add}, pid
        providers_add.append(row)
    for r in routes:
        assert r in route_ids, r
        where_add.setdefault(r, [])
        if pid not in where_add[r]:
            where_add[r].append(pid)

# Rajarshi Janak University: its own row gets the campus programmes, the 47 affiliated colleges are added without course links
note_add['p-rju'] = R.RJU_NOTE
for r in R.RJU_ROUTES:
    where_add.setdefault(r, [])
    if 'p-rju' not in where_add[r]:
        where_add[r].append('p-rju')
rju_new = rju_old = 0
for e in R.affiliated():
    k = W.key(e['name'])
    pid = R.MATCH.get((k, e['district'])) or existing.get((k, e['district']))
    if pid:
        rju_old += 1
        note_add[pid] = (note_add.get(pid, '') + ' ' if pid in note_add else '') + (
            f"Rajarshi Janak University lists it as an affiliated college ({e['address']}; rju.edu.np, checked 19 Nov 2026).")
        continue
    if (k, e['district']) in R.MERGE_NEW:
        row = next(x for x in providers_add if x['id'] == R.MERGE_NEW[(k, e['district'])])
        row['note'] += f" Rajarshi Janak University also lists it as an affiliated college ({e['address']}; rju.edu.np, checked 19 Nov 2026)."
        rju_old += 1
        continue
    rju_new += 1
    pid = 'p-w28-rju-' + R.slug(e['name']) + '-' + e['district'].lower().replace(' ', '')
    assert pid not in by_id and pid not in {x['id'] for x in providers_add}, pid
    sector = 'Community' if (k, e['district']) in npca else W.sector_of(e['name'], set()) or 'Not stated'
    providers_add.append({'id': pid, 'name': e['name'], 'kind': 'Campus' if 'campus' in e['name'].lower() else 'College', 'sector': sector,
                          'district': e['district'], 'place': e['place'],
                          'note': (f"Affiliated to Rajarshi Janak University (official list at rju.edu.np/affiliated-colleges, checked 19 Nov 2026), address {e['address']}. "
                                   "The list does not name the programmes, so ask the college which RJU courses and seats it runs this year.")})
stats['rju_new'], stats['rju_matched'] = rju_new, rju_old

# the new rows hold route_seats inline; matched rows get theirs through route_seats
out = {'providers_add': providers_add, 'where_add': where_add, 'route_seats': route_seats, 'note_add': note_add}
for mod, attr, key in (('w28_abroad', 'ABROAD_UPDATE', 'abroad_update'), ('w28_faq', 'FAQ_ADD', 'faq_add')):
    try:
        m = importlib.import_module(mod)
    except ImportError:
        continue
    out[key] = getattr(m, attr)
try:
    M = importlib.import_module('w28_more')
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
(DATA / 'wave28.json').write_text(text + '\n', encoding='utf-8')
print('wave28.json', len(text), 'bytes;', stats, sum(len(v) for v in where_add.values()), 'route links;', len(note_add), 'notes')
