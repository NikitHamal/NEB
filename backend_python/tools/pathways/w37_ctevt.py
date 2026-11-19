"""Wave 37 CTEVT institutes from the official mapping portal (mapping.ctevt.org.np, fiscal year 2083/84).

Source rows are in ctevt_mapping_2083.json (scrape_ctevt_w37.py): institute, district, municipality, type (Private, Partnership,
Constituated, TECS), phone, e-mail and every programme with its approved quota and current enrolment.
ctevt_match_w37.json maps 89 portal rows to providers already in the data (name and district matched, then read by hand).
ctevt_sites_w37.json holds websites opened live and checked for a distinctive name word (verify_ctevt_sites_w37.py).
Seats are the approved CTEVT quota for the year, not the number of free seats; fees are not on the portal and are not stated.
"""
import json
import re
from pathlib import Path

from api import pathways as _pw

HERE = Path(__file__).resolve().parent
_RAW = json.loads((HERE / 'ctevt_mapping_2083.json').read_text(encoding='utf-8'))['institutes']
_MATCH = {int(k): v for k, v in json.loads((HERE / 'ctevt_match_w37.json').read_text()).items()}
_SITES = {int(k): v for k, v in json.loads((HERE / 'ctevt_sites_w37.json').read_text()).items()}
_DROP_SITES = {118, 1218, 84}  # Nepal Army and Chitwan Medical College pages, not the institute's own site
_DM = {'Makawanpur': 'Makwanpur', 'Nawalparasi (East)': 'Nawalparasi East', 'Nawalparasi (West)': 'Nawalparasi West',
       'Rukum (East) ': 'Rukum East', 'Rukum (West) ': 'Rukum West', 'Sindhupalchowk': 'Sindhupalchok', 'Tanahun': 'Tanahu',
       'Tehrathum': 'Terhathum'}
_BASE = _pw.payload()
_BY_ID = {p['id']: p for p in _BASE['providers']}
_ROUTE_IDS = {r['id'] for r in _BASE['routes']}

ENG = ('Electrical', 'Mechanical', 'Automobile', 'Architecture', 'Electronics', 'Mechatronics', 'Refrigeration', 'Biomedical',
       'Agricultural Engineering')


def routes_for(name):
    """Pathways routes a CTEVT programme belongs to; the first is the specific one."""
    n = name.lower()
    if n.startswith('pre-diploma'):
        return ['pre-diploma']
    out = []
    if 'civil engineering' in n:
        out = ['dip-civil-eng', 'dip-engineering']
    elif 'computer engineering' in n:
        out = ['dip-computer-eng', 'dip-engineering']
    elif 'information technology' in n:
        out = ['dip-it-computer']
    elif 'geomatics' in n:
        out = ['dip-geomatics', 'dip-engineering']
    elif any(k.lower() in n for k in ENG):
        out = ['dip-mech-auto-arch', 'dip-engineering']
    elif 'general medicine' in n:
        out = ['pcl-general-medicine', 'dip-health']
    elif 'pharmacy' in n:
        out = ['dip-pharmacy', 'dip-health']
    elif 'nursing' in n:
        out = ['pcl-nursing']
    elif 'medical laboratory' in n:
        out = ['pcl-cmlt', 'dip-health']
    elif 'radiography' in n:
        out = ['pcl-radiography', 'dip-health']
    elif 'ophthalmic' in n:
        out = ['pcl-ophthalmic', 'dip-health']
    elif 'dental' in n:
        out = ['pcl-dental', 'dip-health']
    elif 'ayurved' in n or 'physiotherapy' in n:
        out = ['pcl-ayurveda-physio', 'dip-health']
    elif 'midwifery' in n or 'yog' in n or 'acupuncture' in n:
        out = ['dip-health']
    elif 'agriculture' in n or 'food' in n:
        out = ['dip-agriculture']
    elif 'forestry' in n:
        out = ['dip-forestry']
    elif 'hotel' in n:
        out = ['dip-hospitality']
    return out


def _short(prog):
    s = prog.replace('Diploma/PCL in ', '').replace('Pre-diploma in ', 'Pre-diploma ')
    return s.replace('Livestock Production/Animal Health', 'Livestock and Animal Health').replace('Agriculture/Plant Science', 'Plant Science')


def _clean(s):
    return re.sub(r'\s+', ' ', (s or '').replace(' ,', ',')).strip(' ,')


def _parts(c):
    dist = _DM.get(c['district'], c['district'])
    segs = [_clean(x) for x in c['name'].split(',')]
    segs = [x for x in segs if x]
    while len(segs) > 1 and re.sub(r'\W', '', segs[-1]).lower() == re.sub(r'\W', '', dist).lower():
        segs.pop()
    return segs, dist


def _kind(name):
    low = name.lower()
    for key, kind in (('campus', 'Campus'), ('college', 'College'), ('school', 'School'), ('academy', 'Institute'), ('institute', 'Institute'), ('polytechnic', 'Institute')):
        if key in low:
            return kind
    return 'Institute'


def _sector(t):
    return {'Private': 'Private', 'Constituated': 'Public', 'Partnership': 'Community', 'TECS': 'Community'}.get(t, 'Not stated')


def _type_text(t):
    return {'Private': 'private institute affiliated to CTEVT', 'Constituated': 'CTEVT constituent institute (run by CTEVT)',
            'Partnership': 'CTEVT partnership institute', 'TECS': 'technical school annex run inside a community secondary school under the CTEVT TECS programme'}.get(t, 'CTEVT institute')


def _contact(c):
    bits = []
    free = any(f in (c.get('email') or '').lower() for f in ('gmail', 'yahoo', 'hotmail', 'outlook', 'ymail'))
    parts = [x.strip() for x in re.split(r'[/,;]', c.get('phone') or '') if x.strip()]
    land = [x for x in parts if re.fullmatch(r'0\d{1,2}[- ]?\d{5,7}', re.sub(r'\s+', '', x))]  # landlines only, personal mobiles are not published
    if land:
        bits.append('phone ' + ' / '.join(land))
    if c.get('email') and '@' in c['email'] and not free:
        bits.append('e-mail ' + _clean(c['email']).lower())
    return ('Contact on the portal: ' + ', '.join(bits) + '.') if bits else ''


def _quota_text(c):
    rows = [f"{_short(n)} {q}" + (f" ({e} enrolled)" if e else '') for n, q, e in c['programs'] if q]
    return 'Approved CTEVT quota for 2083/84' + (' (students enrolled so far)' if any(e for _, _, e in c['programs']) else '') + ': ' + ', '.join(rows) + '.'


def _seat_map(c):
    out = {}
    for n, q, _e in c['programs']:
        rs = routes_for(n)
        if not rs or q <= 0:
            continue
        for r in rs:
            if r in _ROUTE_IDS:
                out[r] = out.get(r, 0) + q
    return out


PROVIDERS_ADD, WHERE_ADD, ROUTE_SEATS, NOTE_ADD, PROVIDER_UPDATE = [], {}, {}, {}, {}
_new_ids = set()
for c in _RAW:
    code = c['inst_cd']
    seats = _seat_map(c)
    if not seats or not c['programs']:
        continue
    pid = _MATCH.get(code)
    site = None if code in _DROP_SITES else _SITES.get(code)
    if pid:
        old = _BY_ID[pid]
        have = old.get('route_seats') or {}
        new_rs = {r: n for r, n in seats.items() if r not in have}
        if new_rs:
            ROUTE_SEATS[pid] = new_rs
        for r in seats:
            WHERE_ADD.setdefault(r, [])
            if pid not in WHERE_ADD[r]:
                WHERE_ADD[r].append(pid)
        NOTE_ADD[pid] = f"{_quota_text(c)} Source: CTEVT institute mapping portal. {_contact(c)}".strip()
        upd = {}
        if site and not old.get('website'):
            upd['website'] = site
        if not old.get('seats'):
            upd['seats'] = sum(q for _n, q, _e in c['programs'])
        if upd:
            PROVIDER_UPDATE[pid] = upd
        continue
    segs, dist = _parts(c)
    name = ', '.join(segs)
    place = segs[-1] if len(segs) > 1 else re.sub(r'-\d+$', '', _clean(c.get('municipality') or '')) or dist
    pid = f'p-ct37-{code}'
    row = {'id': pid, 'name': name, 'kind': _kind(segs[0]), 'sector': _sector(c['type']), 'district': dist, 'place': place,
           'seats': sum(q for _n, q, _e in c['programs']), 'route_seats': seats,
           'note': f"{_type_text(c['type'])[0].upper() + _type_text(c['type'])[1:]} in {dist}. {_quota_text(c)} Source: CTEVT institute mapping portal. {_contact(c)}".strip()}
    if site:
        row['website'] = site
    PROVIDERS_ADD.append(row)
    for r in seats:
        WHERE_ADD.setdefault(r, []).append(pid)


# Route level totals from the same portal rows (institutes with a quota, programme quotas summed per route).
ROUTE_NOTE_ADD = {}
_PROV = {1: 'Koshi', 2: 'Madhesh', 3: 'Bagmati', 4: 'Gandaki', 5: 'Lumbini', 6: 'Karnali', 7: 'Sudurpashchim'}
_agg = {}
for _c in _RAW:
    for _n, _q, _e in _c['programs']:
        for _r in routes_for(_n)[:1] + (['dip-engineering'] if 'dip-engineering' in routes_for(_n) else []) + (['dip-health'] if 'dip-health' in routes_for(_n) else []):
            _a = _agg.setdefault(_r, {'inst': set(), 'quota': 0, 'enr': 0, 'prov': {}})
            _a['inst'].add(_c['inst_cd'])
            _a['quota'] += _q
            _a['enr'] += _e
            _a['prov'][_c['province_cd']] = _a['prov'].get(_c['province_cd'], 0) + _q
for _r, _a in _agg.items():
    if _r not in _ROUTE_IDS:
        continue
    _top = sorted(_a['prov'].items(), key=lambda kv: -kv[1])[:3]
    ROUTE_NOTE_ADD[_r] = (f"CTEVT mapping portal, fiscal year 2083/84: {len(_a['inst'])} institutes hold an approved quota of {_a['quota']:,} seats for this track "
                          f"({_a['enr']:,} students enrolled so far); the largest quotas are in " + ', '.join(f"{_PROV[k]} ({v:,})" for k, v in _top) + '.')

ROUTE_NOTE_ADD['dip-computer-eng'] += ' The earlier CTEVT table of free seats listed 45 institutes at 48 seats each, while the live portal lists 48 institutes (2,296 seats in total), so the two official sources differ by three institutes.'
