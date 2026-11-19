"""Wave 28: Purbanchal University affiliated colleges and their approved programmes and seat quotas.

Source: the PU faculty pages (Management, Science and Technology, Medical and Allied Sciences, Arts, Education, Law) at
http://purbanchaluniversity.edu.np/faculties/..., read on 19 November 2026 by scrape_pu_faculties.py into pu_colleges.json.
Every row on those pages has a college, an address, a district and "Approved Programs/Quotas". Engineering is already in wave 9.
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
FAC_NAME = {'management': 'Faculty of Management', 'science': 'Faculty of Science and Technology',
            'health': 'Faculty of Medical and Allied Sciences', 'arts': 'Faculty of Arts', 'education': 'Faculty of Education',
            'law': 'Faculty of Law'}

DISTRICT_FIX = {'Sunsary': 'Sunsari', 'Illam': 'Ilam', 'Kapilbastu': 'Kapilvastu', 'Tanahun': 'Tanahu', 'Makawanpur': 'Makwanpur'}
# the PU table says Nawalparasi for places that are in one of the two new districts
DISTRICT_BY_PLACE = {('Nawalparasi', 'Kawasoti'): 'Nawalparasi East', ('Nawalparasi', 'Kawashoti'): 'Nawalparasi East'}

# PU programme text (lower case, no spaces or dots) to our route id
PROG = {'bba': 'bba', 'bbs': 'bbs', 'bhm': 'bhm', 'bca': 'bca', 'bcait': 'bca', 'bit': 'bit', 'mba': 'mba', 'mca': 'mca',
        'bscag': 'bsc-agri', 'bschonsag': 'bsc-agri', 'bscforestry': 'bsc-forestry', 'btechfood': 'btech-food',
        'bvscah': 'bvsc', 'bed': 'bed', 'med': 'med', 'oneyearbed': None, 'llb': 'llb', 'balbl': 'ba-llb', 'balb': 'ba-llb',
        'bsw': 'bsw', 'msw': 'msw', 'ba': 'ba', 'ma': 'ma', 'bamcj': 'bjmc', 'bscnursing': 'bsc-nursing', 'bsn': 'bsc-nursing',
        'bph': 'bph', 'bpharm': 'bpharm', 'bscmlt': 'bmlt', 'mph': 'mph', 'mpa': 'mpa', 'mpharm': 'mpharm', 'bttm': 'bttm',
        'btts': 'bttm', 'bfdm': 'bfd-design'}
PROG_LABEL = {'bba': 'BBA', 'bbs': 'BBS', 'bhm': 'BHM', 'bca': 'BCA', 'bit': 'BIT', 'mba': 'MBA', 'mca': 'MCA',
              'bsc-agri': 'B.Sc. (Hons.) Ag.', 'bsc-forestry': 'B.Sc. Forestry', 'btech-food': 'B.Tech. Food', 'bvsc': 'B.V.Sc. and A.H.',
              'bed': 'B.Ed.', 'med': 'M.Ed.', 'llb': 'LL.B.', 'ba-llb': 'B.A. LL.B.', 'bsw': 'BSW', 'msw': 'MSW', 'ba': 'BA', 'ma': 'MA',
              'bjmc': 'BAMCJ', 'bsc-nursing': 'B.Sc. Nursing', 'bph': 'BPH', 'bpharm': 'B.Pharm', 'bmlt': 'B.Sc. MLT', 'mph': 'MPH',
              'mpa': 'MPA', 'mpharm': 'M.Pharm', 'bttm': 'Travel and Tourism', 'bfd-design': 'BFDM'}


def split_prog(text):
    parts, depth, cur = [], 0, ''
    for ch in text:
        if ch == '(':
            depth += 1
        elif ch == ')':
            depth -= 1
        if ch == ',' and depth == 0:
            parts.append(cur.strip())
            cur = ''
        else:
            cur += ch
    if cur.strip():
        parts.append(cur.strip())
    return parts


def parse_item(item):
    """'MBA (Spring/Fall)-33/33' -> ('mba', 66, 'MBA (Spring/Fall) 33/33')"""
    m = re.match(r'^(.*?)(?:\s*-\s*([\d/]+))?$', item.strip())
    name, q = m.group(1), m.group(2)
    base = re.sub(r'\(.*?\)', '', name).lower()
    base = re.sub(r'[^a-z]', '', base.replace('b. sc', 'bsc').replace('b.sc', 'bsc'))
    base = base.replace('inai', '')
    seats = sum(int(x) for x in q.split('/')) if q else None
    return base, seats, name.strip(), q


def load():
    return json.loads((HERE / 'pu_colleges.json').read_text(encoding='utf-8'))


def norm_district(d, address=''):
    d = d.strip()
    if (d, address.strip()) in DISTRICT_BY_PLACE:
        return DISTRICT_BY_PLACE[(d, address.strip())]
    return DISTRICT_FIX.get(d, d)


def key(s):
    s = re.sub(r'\(.*?\)', '', s.lower()).replace('&', ' and ')
    s = re.sub(r'\b(pvt|ltd|private|limited|the)\b', ' ', s)
    s = s.replace('multiple campus', 'multiple college').replace("int'l", 'international')
    return re.sub(r'[^a-z]', '', s)


DISTRICT_FIX.update({'Lalitipur': 'Lalitpur', 'Okhaldunga': 'Okhaldhunga'})
PROG.update({'ballb': 'ba-llb', 'bpharmacy': 'bpharm', 'pbns': 'bns', 'bachelorofmedicineandbachelorofsurgery': 'mbbs'})
PROG_LABEL.update({'bns': 'PBNS', 'mbbs': 'MBBS'})
POSTGRAD = {'mba', 'mca', 'med', 'msw', 'ma', 'mph', 'mpa', 'mpharm'}

# PU row (name key, district) to an existing provider id; checked by hand against the existing note and place
MATCH = {
    ('kantipurcitycollege', 'Kathmandu'): 'p-kantipur-city', ('himalayanwhitehouseinternationalcollege', 'Kathmandu'): 'p-hwic',
    ('collegeofinformationtechnologyandengineering', 'Kathmandu'): 'p-cite', ('novelacademy', 'Kaski'): 'p-novel',
    ('nepalpolytechnicinstitute', 'Chitwan'): 'p-nepal-polytechnic', ('aryanschoolofengineeringandmanagement', 'Kathmandu'): 'p-aryan-eng',
    ('collegeofappliedfoodanddairytechnology', 'Lalitpur'): 'p-cafodat',
    ('himalayancollegeofagriculturalsciencesandtechnology', 'Kathmandu'): 'p-hicast', ('janakpurcommunitycollege', 'Dhanusha'): 'p-w25-ku-janakpur-cc',
    ('madanbhandarimemorialacademy', 'Morang'): 'p-w24-pu-mbman', ('balkumaricampus', 'Chitwan'): 'p-w24-iost-balkumari',
    ('chakrabartihabieducationacademycollegeofnursingscience', 'Bhaktapur'): 'p-chakrabarti',
    ('southasianschooloftourismandhotelmanagement', 'Morang'): 'p-sasthm',
    ('gyandeepacademy', 'Dang'): 'p-gyan-deep', ('nagarikcollegeofhealthsciences', 'Kathmandu'): 'p-nagarik-health',
    ('nationalacademyformedicalscience', 'Kathmandu'): 'p-nams-pu', ('sanjeevanicollegeofmedicalscience', 'Rupandehi'): 'p-sanjeevani',
    ('valleycollegeoftechnicalscience', 'Kathmandu'): 'p-valley-tech', ('npinarayanisamudayikhospital', 'Chitwan'): 'p-npi-narayani',
    ('chakrabartihabieducationacademy', 'Kathmandu'): 'p-chakrabarti', ('chakrabartihabieducationalacademy', 'Kathmandu'): 'p-chakrabarti',
    ('kasthamandapcollegeofmanagement', 'Kathmandu'): 'p-kasthamandap', ('khwopaengineeringcollege', 'Bhaktapur'): 'p-khwopa-eng',
}
# not added: the page name could be the same institution as an existing row and one source is not enough to decide
SKIP = {('royalsoftechcollege', 'Siraha')}
NOT_PRIVATE = {('publiccampus', 'Morang'): 'Community', ('saraswatipubliccampus', 'Morang'): 'Community'}
COMMUNITY_WORDS = ('community', 'samudayik', 'public campus', 'janata', 'tribhuvan campus', 'multiple campus')
PRIVATE_WORDS = ('pvt', 'ltd', 'international', 'college of', 'academy', 'school of', 'valley', 'foundation', 'trust', 'hospital', 'institute',
                 'management', 'business', 'professional', 'technology', 'nursing', 'health', 'law college', 'college of law')


def sector_of(name, npca_names):
    low = name.lower()
    if re.sub(r'\s', '', low).startswith(('p.u.', 'purbanchaluniversity')):
        return 'Public'
    if key(name) in npca_names or any(w in low for w in ('community', 'samudayik')):
        return 'Community'
    if any(w in low for w in PRIVATE_WORDS):
        return 'Private'
    return ''


def slug(name):
    s = re.sub(r'\(.*?\)', '', name.lower()).replace('&', 'and')
    s = re.sub(r'\b(pvt|ltd)\b', '', s)
    return re.sub(r'-+', '-', re.sub(r'[^a-z0-9]+', '-', s)).strip('-')[:48].strip('-')


def rows():
    """Merge the six faculty tables into one entry per (college, district)."""
    d = load()
    out = {}
    for fac in FAC_NAME:
        for c in d[fac]['colleges']:
            dist = norm_district(c['district'], c['address'])
            k = (key(c['name']), dist)
            e = out.setdefault(k, {'name': re.sub(r'\s+', ' ', c['name']).strip(), 'district': dist, 'place': c['address'].strip(), 'facs': [], 'items': []})
            e['facs'].append(fac)
            for it in split_prog(c['programs']):
                base, seats, name, q = parse_item(it)
                route = PROG.get(base)
                if base == 'btech' and '(food)' in it.lower():
                    route = 'btech-food'
                e['items'].append({'fac': fac, 'base': base, 'seats': seats, 'text': it.strip(), 'route': route})
    return out
