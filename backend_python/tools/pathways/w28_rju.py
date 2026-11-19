"""Wave 28: Rajarshi Janak University. Source: rju.edu.np/affiliated-colleges/ (47 colleges with ward address, read 19 Nov 2026),
rju.edu.np/course-search/ and rju.edu.np/campuses/ (programmes of the University Campus and the constituent campuses).
The affiliated list gives no programmes, so those colleges are listed without course links."""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
DISTRICT = {'Kapilbastu': 'Kapilvastu'}
# RJU list row (name key, district) to an existing provider; same place and same institution on both lists
MATCH = {('relianceinternationalcollege', 'Kathmandu'): 'p-reliance', ('saharacollege', 'Surkhet'): 'p-sahara-surkhet',
         ('jsmurarkacollegelahan', 'Siraha'): 'p-w24-iost-jsm-lahan'}
# same campus as a row added from the Purbanchal University list (both address the same town)
MERGE_NEW = {('annapurnacampussaptari', 'Saptari'): 'p-w28-pu-annapurna-multiple-campus-saptari'}


def key(s):
    s = re.sub(r'\(.*?\)', '', s.lower()).replace('&', ' and ').replace('pvt', '').replace('ltd', '')
    return re.sub(r'[^a-z]', '', s)


def affiliated():
    out = []
    for name, addr in json.loads((HERE / 'rju_affiliated.json').read_text(encoding='utf-8')):
        parts = [x.strip() for x in addr.replace(', Nepal', '').split(',')]
        dist = re.sub(r'-\d+$', '', parts[-1])
        dist = DISTRICT.get(dist, dist)
        place = ', '.join(parts[:-1]) if len(parts) > 1 else parts[0]
        if dist == 'Kathmandu' and len(parts) == 1:
            place = 'Kathmandu'
        out.append({'name': name.strip(), 'district': dist, 'place': place or dist, 'address': addr})
    return out


def slug(name):
    s = re.sub(r'\(.*?\)', '', name.lower())
    s = re.sub(r'\b(pvt|ltd)\b', '', s)
    return re.sub(r'-+', '-', re.sub(r'[^a-z0-9]+', '-', s)).strip('-')[:48].strip('-')


RJU_NOTE = ('Rajarshi Janak University (rju.edu.np, checked 19 Nov 2026) lists on its course search: M.Phil. in Management, M.Phil. in Eastern '
            'Philosophy, MBA, BBA, BDBM (Digital Business Management), BCA, B.Sc. CSIT, BIT, BPH, B.Sc. MLT, BJMC, LL.B., LL.M. and B.A. LL.B. at the University Campus. '
            'Gaushala Engineering Campus (the second constituent campus) runs the Bachelor in Civil Engineering, Mahagadhi Mai Campus runs BIT and Pandit '
            'Mangal Kumar Upadhyay Multiple Campus runs B.Sc. Agriculture; the site does not give a district for those campuses. '
            'The university also lists 47 affiliated colleges.')
RJU_ROUTES = ['llb', 'bjmc', 'bsc-agri', 'bit']
