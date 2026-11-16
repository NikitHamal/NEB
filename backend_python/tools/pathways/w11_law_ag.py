"""Adds the TU law seats (LLB and BA LLB 2083) and the AFU agriculture seats (2083/84) to api/data/pathways/wave11.json.

Sources: TU Faculty of Law LL.B entrance result 2083 and admission notice (3,800 seats in 12 campuses; 8,623 applied, 7,538 sat on
2083/02/29), TU BA LL.B notice 2083/84 (570 seats in 6 colleges), AFU undergraduate entrance notice 2083 (BSc Ag Rampur 167,
constituent colleges 54 each and 49 at Khajura and Madichaur, BVSc and AH 100).
Run: python3 backend_python/tools/pathways/w11_law_ag.py   (idempotent: it rebuilds the keys it owns)
"""
import json
from pathlib import Path

FILE = Path(__file__).resolve().parent.parent.parent / 'api' / 'data' / 'pathways' / 'wave11.json'
w = json.loads(FILE.read_text('utf-8'))

NEW = [
    ('p-mmc-dharan', 'Mahendra Multiple Campus, Dharan (Tribhuvan University)', 'Campus', 'Public', 'Sunsari', 'Dharan'),
    ('p-degree-biratnagar', 'Post Graduate (Degree) Campus, Biratnagar (Tribhuvan University)', 'Campus', 'Public', 'Morang', 'Biratnagar'),
    ('p-surkhet-mc', 'Surkhet Multiple Campus (Tribhuvan University)', 'Campus', 'Public', 'Surkhet', 'Birendranagar'),
    ('p-harikhetan', 'Harikhetan Multiple Campus (Tribhuvan University)', 'Campus', 'Public', 'Parsa', 'Birgunj'),
    ('p-national-law', 'National Law College', 'College', 'Private', 'Lalitpur', 'Lalitpur'),
    ('p-cnrm-puranchaur', 'College of Natural Resource Management, Puranchaur (AFU)', 'Campus', 'Public', 'Kaski', 'Puranchaur'),
    ('p-cnrm-kapilakot', 'College of Natural Resource Management, Kapilakot (AFU)', 'Campus', 'Public', 'Sindhuli', 'Kapilakot'),
    ('p-cnrm-tikapur', 'College of Natural Resource Management, Tikapur (AFU)', 'Campus', 'Public', 'Kailali', 'Tikapur'),
    ('p-cnrm-pakhribas', 'College of Natural Resource Management, Pakhribas (AFU)', 'Campus', 'Public', 'Dhankuta', 'Pakhribas'),
    ('p-cnrm-bardibas', 'College of Natural Resource Management, Bardibas (AFU)', 'Campus', 'Public', 'Mahottari', 'Bardibas'),
    ('p-cnrm-khajura', 'College of Natural Resource Management, Khajura (AFU)', 'Campus', 'Public', 'Banke', 'Khajura'),
    ('p-cnrm-madichaur', 'College of Natural Resource Management, Madichaur (AFU)', 'Campus', 'Public', 'Rolpa', 'Madichaur'),
]
LLB = {'p-tu-law': 600, 'p-prithvi': 300, 'p-mmc-dharan': 300, 'p-mmc-nepalgunj': 300, 'p-mbmc-saptari': 300, 'p-butwal': 300,
       'p-padmakanya': 300, 'p-bhaktapur-mc': 300, 'p-rrmc': 300, 'p-degree-biratnagar': 300, 'p-surkhet-mc': 300, 'p-harikhetan': 200}
BALLB = {'p-tu-law': 160, 'p-prithvi': 80, 'p-butwal': 70, 'p-mmc-nepalgunj': 70, 'p-mmc-dharan': 70, 'p-national-law': 120}
AG = {'p-aafu': {'bsc-agri': 167, 'bvsc': 100}, 'p-cnrm-puranchaur': {'bsc-agri': 54}, 'p-cnrm-kapilakot': {'bsc-agri': 54},
      'p-cnrm-tikapur': {'bsc-agri': 54}, 'p-cnrm-pakhribas': {'bsc-agri': 54}, 'p-cnrm-bardibas': {'bsc-agri': 54},
      'p-cnrm-khajura': {'bsc-agri': 49}, 'p-cnrm-madichaur': {'bsc-agri': 49}}
assert sum(LLB.values()) == 3800 and sum(BALLB.values()) == 570

seats, where, notes = w['route_seats'], w.setdefault('where_add', {}), w['note_add']
add_ids = {p[0] for p in NEW}
providers = []
for pid, name, kind, sector, district, place in NEW:
    note = ''
    if pid in LLB:
        note += f'TU LL.B 2083: {LLB[pid]} seats. '
    if pid in BALLB:
        note += f'TU BA LL.B 2083/84: {BALLB[pid]} seats. '
    if pid in AG:
        note += f'BSc Ag 2083/84 seats: {AG[pid]["bsc-agri"]}. '
    seat = max([LLB.get(pid, 0), BALLB.get(pid, 0), *AG.get(pid, {}).values()])
    providers.append({'id': pid, 'name': name, 'kind': kind, 'sector': sector, 'district': district, 'place': place,
                      'note': note.strip(), 'seats': seat})
for table, route, label in ((LLB, 'llb', 'TU LL.B 2083'), (BALLB, 'ba-llb', 'TU BA LL.B 2083/84')):
    for pid, n in table.items():
        seats.setdefault(pid, {})[route] = n
        where.setdefault(route, [])
        if pid not in where[route]:
            where[route].append(pid)
        if pid not in add_ids:
            tag = f'{label}: {n} seats.'
            notes[pid] = (notes.get(pid, '') + ' ' + tag).strip() if tag not in notes.get(pid, '') else notes[pid]
for pid, rs in AG.items():
    seats.setdefault(pid, {}).update(rs)
    for route in rs:
        where.setdefault(route, [])
        if pid not in where[route]:
            where[route].append(pid)
    if pid not in add_ids:
        tag = 'AFU 2083/84 seats: BSc Ag 167, BVSc and AH 100.'
        notes[pid] = (notes.get(pid, '') + ' ' + tag).strip() if tag not in notes.get(pid, '') else notes[pid]
w['providers_add'] = providers
FAQ = [
    {'id': 'fw11-6', 'topic': 'after12', 'q': 'How many LL.B seats are there and how hard is the entrance?', 'go': ['llb'],
     'a': 'Tribhuvan University Faculty of Law allotted 3,800 seats for the three year LL.B in 2083 across 12 campuses: Nepal Law Campus 600, Birgunj (Harikhetan) 200 and 300 each at Pokhara, Dharan, Nepalgunj, Rajbiraj, Butwal, Padma Kanya, Bhaktapur, Janakpur, Biratnagar and Surkhet. For the entrance of 29 Jestha 2083 (12 June 2026), 8,623 candidates applied and 7,538 sat; at Nepal Law Campus 2,312 passed for 600 seats, so the merit list decides. LL.B is a bachelor degree, so you apply after a bachelor in any subject.'},
    {'id': 'fw11-7', 'topic': 'after12', 'q': 'Which colleges offer TU BA LL.B after +2?', 'go': ['ba-llb'],
     'a': 'For 2083/84 the TU Faculty of Law advertised 570 seats in the five year, ten semester BA LL.B: Nepal Law Campus 160, National Law College (Lalitpur) 120, Prithvi Narayan Campus Pokhara 80, and 70 each at Butwal, Nepalgunj and Dharan. You need at least a D grade in +2 of any stream and must pass the entrance exam (23 Shrawan 2083). 20 percent of seats are reserved for women, Janajati, Madhesi, Dalit, disabled, remote area, Muslim, Tharu and other groups. Kathmandu University and Purbanchal University colleges run their own integrated law degrees with separate entrances.'},
    {'id': 'fw11-8', 'topic': 'after12', 'q': 'How many BSc Agriculture seats does AFU have for 2083/84?', 'go': ['bsc-agri', 'bvsc'],
     'a': 'Agriculture and Forestry University set 167 BSc Ag seats at its Rampur campus and 54 at each of its constituent colleges Puranchaur (Kaski), Kapilakot (Sindhuli), Tikapur (Kailali), Pakhribas (Dhankuta) and Bardibas (Mahottari), with 49 each at Khajura (Banke) and Madichaur (Rolpa). BVSc and AH has 100 seats at Rampur. Seats are split into merit (74 at Rampur, 20 at a college), reserved groups and full fee seats, and entrance is a written exam from the Faculty of Agriculture. Tribhuvan University IAAS and other universities run separate entrances.'},
]
w['faq_add'] = [f for f in w['faq_add'] if f['id'] not in {x['id'] for x in FAQ}] + FAQ
FILE.write_text(json.dumps(w, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print('providers', len(providers), 'faq', len(w['faq_add']), 'llb', sum(LLB.values()), 'ballb', sum(BALLB.values()))
