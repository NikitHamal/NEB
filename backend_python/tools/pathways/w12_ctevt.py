"""Wave 12, part 1: CTEVT 2083/84 institutes into api/data/pathways/wave12.json (idempotent, owns its keys).

Adds providers (constituent and partnership polytechnics, plus the 45 computer engineering institutes), attaches them to the
diploma routes, adds two new routes (dip-civil-eng, dip-computer-eng) and the free scholarship seat counts as provider notes.
Run: python3 backend_python/tools/pathways/w12_ctevt.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from w12_ctevt_data import COMPUTER, CONST, PROGRAMS  # noqa: E402

FILE = Path(__file__).resolve().parent.parent.parent / 'api' / 'data' / 'pathways' / 'wave12.json'
w = json.loads(FILE.read_text('utf-8')) if FILE.exists() else {}
OWN = ('providers_add', 'where_add', 'note_add', 'route_seats', 'routes_add')
for k in OWN:
    w[k] = {} if k in ('where_add', 'note_add', 'route_seats') else []

providers, where, notes, seats = w['providers_add'], w['where_add'], w['note_add'], w['route_seats']
all_ids = set()


def attach(pid, rid):
    lst = where.setdefault(rid, [])
    if pid not in lst:
        lst.append(pid)


for pid, name, district, place, prog in CONST:
    free = ', '.join(f"{PROGRAMS[k][1]} {n}" for k, n in prog.items())
    text = (f"CTEVT special scholarship 2083/84 (notice of 2 Asar 2083): free seats at this institute are {free}. "
            "Apply on ctevtexam.org.np; Dalit, Muslim, poor, marginalized and 78 remote local level students only.")
    if pid.startswith('='):
        pid = pid[1:]
        notes[pid] = text
    else:
        sector = 'Community' if 'Nursing College' in name else 'Public'
        providers.append({'id': pid, 'name': name, 'kind': 'Institute', 'sector': sector, 'district': district, 'place': place,
                          'website': '', 'note': 'CTEVT constituent or partnership institute. ' + text})
    for k in prog:
        for rid in PROGRAMS[k][0]:
            attach(pid, rid)

for item in COMPUTER:
    name, district, place, typ = item
    if name.startswith('='):
        pid = name[1:]
        notes[pid] = f"CTEVT notice 2083/84 lists Diploma in Computer Engineering here with an approved quota of 48 ({typ})."
    else:
        pid = 'p-w12-ce-' + ''.join(c if c.isalnum() else '-' for c in name.lower()).strip('-')[:48]
        sector = {'Private': 'Private', 'Constituent': 'Public'}.get(typ, 'Community')
        kind = 'School' if typ == 'TECS' else 'College' if typ == 'Private' else 'Institute'
        providers.append({'id': pid, 'name': name, 'kind': kind, 'sector': sector, 'district': district, 'place': place,
                          'website': '', 'note': f"CTEVT notice 2083/84 lists Diploma in Computer Engineering here with an approved quota of 48 ({typ}).",
                          'seats': 48})
    seats.setdefault(pid, {})['dip-computer-eng'] = 48
    attach(pid, 'dip-computer-eng')
    attach(pid, 'dip-engineering')

for p in providers:
    assert p['id'] not in all_ids, p['id']
    all_ids.add(p['id'])
assert len(COMPUTER) == 45

w['routes_add'] = [
    {'id': 'dip-civil-eng', 'stage': 'after10', 'name': 'Diploma in Civil Engineering (CTEVT)', 'kind': 'Diploma', 'group': 'tech',
     'years': '3 years', 'fee': [60000, 380000],
     'entry': 'SEE with C in Mathematics and Science and D+ in English (GPA 1.6 overall), or TSLC in civil with 66.68 percent; CTEVT entrance',
     'about': ('The biggest CTEVT programme by free seats: 640 classified scholarship seats in 2083/84 plus 80 in the special programme. '
               'Sub-engineer posts at municipalities, road and irrigation offices and contractors, and a lateral route to BE Civil.'),
     'exam': 'CTEVT entrance through ITMS; usual quota is 48 seats per institute', 'careers': ['civil-engineer', 'geomatics-engineer'],
     'skills': ['Surveying', 'Estimating and costing', 'AutoCAD', 'Site supervision'], 'next': ['be-civil', 'be-geomatics'],
     'where': [], 'plan': ['Year 1: Drawing, surveying, mechanics, maths', 'Year 2: Structures, hydraulics, materials, estimating',
                           'Year 3: Roads, irrigation, construction management, project and internship'], 'exam_id': 'g-eng'},
    {'id': 'dip-computer-eng', 'stage': 'after10', 'name': 'Diploma in Computer Engineering (CTEVT)', 'kind': 'Diploma', 'group': 'tech',
     'years': '3 years', 'fee': [60000, 380000],
     'entry': 'SEE with at least GPA 1.6 and the CTEVT entrance; one programme at one institute per year on ITMS',
     'about': ('45 institutes run it in 2083/84, each with an approved quota of 48: 16 in Madhesh, 10 in Koshi, 6 in Lumbini, 5 in Karnali, '
               '4 in Bagmati, 3 in Gandaki and 1 in Sudurpashchim. The notice lists it separately from Diploma in Information Technology.'),
     'exam': 'CTEVT entrance through ITMS (full fee application closed 2083 Jestha 13)', 'careers': ['software-dev', 'cyber-security', 'data-analyst'],
     'skills': ['Programming', 'Networking', 'Databases', 'Web development'], 'next': ['be-computer', 'bit', 'bca'],
     'where': [], 'plan': ['Year 1: Programming, electronics, maths', 'Year 2: Data structures, databases, networks, web',
                           'Year 3: Software engineering, security, project and internship']},
]
for r in w['routes_add']:
    r.pop('where')

FILE.write_text(json.dumps(w, ensure_ascii=False, indent=1) + '\n', 'utf-8')
print(len(providers), 'providers;', {k: len(v) for k, v in where.items()})
