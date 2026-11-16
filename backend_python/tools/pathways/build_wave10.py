"""Builds api/data/pathways/wave10.json from w10_csit.py, w10_bca.py, w10_misc.py and w10_faq.py.

Wave 10: BSc CSIT seat quota 2083 for all 61 colleges, the TU BCA college list, +2 colleges, three health colleges whose town
is now known, and corrections (Commonwealth is closed to Nepal, NL Scholarship, work rules for Hungary and China).
Run: python3 backend_python/tools/pathways/build_wave10.py
"""
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import w10_bca as B  # noqa: E402
import w10_csit as C  # noqa: E402
import w10_faq as F  # noqa: E402
import w10_misc as X  # noqa: E402

DATA = HERE.parent.parent / 'api' / 'data' / 'pathways'
LABEL = {'bsc-nursing': 'BSc Nursing', 'bns': 'BNS', 'bpharm': 'BPharm', 'bph': 'BPH', 'bmlt': 'BSc MLT', 'bpt': 'BPT', 'bsc-mit': 'BSc MIT', 'boptom': 'BOptom', 'bams': 'BAMS'}
CEILING = {'bsc-nursing': 1036000, 'bpharm': 777000, 'bmlt': 777000, 'bpt': 777000, 'boptom': 777000, 'bams': 1131930}


def existing_ids():
    spec = importlib.util.spec_from_file_location('pw', HERE.parent.parent / 'api' / 'pathways.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return {p['id'] for p in mod.payload()['providers']}


OLD = existing_ids() - {p['id'] for p in (json.loads((DATA / 'wave10.json').read_text('utf-8'))['providers_add'] if (DATA / 'wave10.json').exists() else [])}
REG = {}
ADD = {}


def split(n):
    open_ = round(n * 0.8)
    return open_, n - open_


def ensure(key, name=None, district=None, place=None, kind=None, sector=None):
    if key.startswith('p-') and key in OLD:
        return key
    if key in REG:
        return REG[key]
    assert name and district, f'unknown college {key}'
    pid = key if key.startswith('p-') else 'p-' + key
    assert pid not in OLD, f'{pid} clashes with an existing provider'
    kind = kind or ('Campus' if name.endswith('Campus') or 'Campus (' in name else 'College')
    sector = sector or ('Community' if 'Multiple Campus' in name else 'Private')
    ADD[pid] = {'id': pid, 'name': name, 'kind': kind, 'sector': sector, 'district': district, 'place': place}
    REG[key] = pid
    return pid


where, seats, notes, bits = {}, {}, {}, {}


def offer(route, pid, text=None):
    where.setdefault(route, [])
    if pid not in where[route]:
        where[route].append(pid)
    if text:
        bits.setdefault(pid, []).append(text)


tot_c = tot_p = 0
for key, name, district, place in C.NEW_CONSTITUENT:
    ensure(key, name, district, place, 'Campus', 'Public')
for key, n in C.CONSTITUENT:
    pid = ensure(key)
    tot_c += n
    o, s = split(n)
    seats.setdefault(pid, {})['bsc-csit'] = n
    offer('bsc-csit', pid, f'BSc CSIT quota 2083: {n} seats ({o} open, {s} Samabesi).')
for key, name, district, place, n in C.PRIVATE:
    pid = ensure(key, name, district, place)
    tot_p += n
    o, s = split(n)
    seats.setdefault(pid, {})['bsc-csit'] = n
    offer('bsc-csit', pid, f'BSc CSIT quota 2083: {n} seats ({o} open, {s} Samabesi).')
assert (tot_c, tot_p) == (1224, 1884), (tot_c, tot_p)
assert len(C.CONSTITUENT) == 16 and len(C.PRIVATE) == 45

for key, name, district, place in B.BCA:
    if name:
        ensure(key, name, district, place, 'Campus' if key == 'saraswati-mc' else None, 'Public' if key == 'saraswati-mc' else None)
    offer('bca', ensure(key), 'Runs the TU BCA (FoHSS entrance exam).')

for key, name, district, place, sector, streams in X.PLUS2:
    pid = ensure(key, name, district, place, None, sector)
    for r in streams:
        offer(r, pid)
    labels = {'plus2-science': 'Science', 'plus2-management': 'Management', 'plus2-humanities': 'Humanities', 'plus2-law': 'Law'}
    bits.setdefault(pid, []).append('NEB +2 streams: ' + ', '.join(labels[r] for r in streams) + '.')

mec = json.loads((HERE / 'mec2083_seats.json').read_text('utf-8'))
health_fees = {}
for pid, name, district, place, note, names in X.HEALTH:
    ADD[pid] = {'id': pid, 'name': name, 'kind': 'College', 'sector': 'Private', 'district': district, 'place': place, 'note': note}
    got = {}
    for prog, rows in mec.items():
        rid = X.PROGRAM_ROUTE.get(prog)
        for nm, n in rows:
            if rid and nm in names and n:
                got[rid] = got.get(rid, 0) + n
    assert got, name
    seats[pid] = got
    ADD[pid]['seats'] = max(got.values())
    bits.setdefault(pid, []).append('MEC seats for 2083/84: ' + ', '.join(f'{LABEL[rid]} {n}' for rid, n in got.items()) + '.')
    for rid in got:
        offer(rid, pid)
        if rid in CEILING:
            health_fees.setdefault(pid, {})[rid] = [CEILING[rid], CEILING[rid]]

offer('bim', 'p-shankerdev', 'BITM seats: 66.')
seats['p-shankerdev'] = {'bim': 66}
for pid, parts in bits.items():
    if pid in ADD:
        ADD[pid]['note'] = (ADD[pid].get('note', '') + ' ' + ' '.join(parts)).strip()
        if 'bsc-csit' in seats.get(pid, {}) and 'seats' not in ADD[pid]:
            ADD[pid]['seats'] = seats[pid]['bsc-csit']
    else:
        text = ' '.join(p for p in parts if not p.startswith('Runs the TU BCA'))
        if text:
            notes[pid] = text

out = {
    'providers_add': list(ADD.values()),
    'where_add': where,
    'route_seats': seats,
    'note_add': notes,
    'provider_extra': {'p-kathford': {'district': 'Lalitpur', 'place': 'Balkumari'}},
    'fees': health_fees,
    'scholarship_extra': X.SCHOLARSHIP_EXTRA,
    'scholarship_drop': X.SCHOLARSHIP_DROP,
    'abroad_extra': X.ABROAD_EXTRA,
    'route_update': X.ROUTE_UPDATE,
    'faq_add': F.FAQ_ADD,
    'faq_update': F.FAQ_UPDATE,
}
(DATA / 'wave10.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print('providers', len(ADD), 'csit', tot_c + tot_p, 'bca', len(where['bca']), 'plus2', {r: len(where[r]) for r in where if r.startswith('plus2')})
