"""Wave 27: community campuses from the NPCA member list whose address is only a place name.

Wave 26 added the 128 NPCA campuses whose address or name carried a district. This wave places more of the 367 others with the
official list of 753 local levels (palika_district.json): resolve_npca_districts.py gives a district only when a local-level
name from the campus address or name belongs to exactly one district (see that script for the stop words and the hand-checked
blocklist). About 20 of the campuses also have a live website that names the district or the local level (checked on 2026-11-19; five more are script-rendered shells that cannot be read).
"""
import json
import re
from pathlib import Path

import w26_campus as C

HERE = Path(__file__).resolve().parent
MAP = {int(k): v for k, v in json.loads((HERE / 'npca_district_map.json').read_text(encoding='utf-8')).items()}
NOTE = ('Community campus on the Nepal Public Campuses Association (NPCA) member list. ')

# clean names (the NPCA field often holds the district, a ward or a town after the name) and places, read from the NPCA row
NAME = {
    19: 'Kanchan Multiple Campus', 30: 'Buddhabhumi Campus', 98: 'Nawa Nepal Campus', 141: 'Janapriya Multiple Campus',
    171: 'Syarpu Multiple Campus', 191: 'Janashikha Campus', 371: 'Amar Jyoti Multiple Campus', 406: 'Gograha College',
    410: 'Bardibas Janata Multiple Campus', 491: 'Janajyoti Campus', 538: 'Daune Devi Multiple Campus', 541: 'Tharpu Campus',
    602: 'Siddha Public College', 585: 'Madhyabindu M. Campus', 72: 'Deukhuri Multiple Campus', 130: 'J. S. Murarka Multiple Campus',
    100: 'Purchaudi Multiple Campus', 560: 'Thalara Multiple Campus', 542: 'Sworgadwari Multiple Campus',
    473: 'Rambha Multiple Campus', 519: 'Banganga Multiple Campus', 460: 'Ramgopalpur Multiple Campus', 288: 'Sotang Public Campus',
    173: 'Chandra Shatrughna Campus', 63: 'Sanibheri Education Campus',
}
PLACE = {
    19: 'Gulariya', 30: 'Barkulpur', 98: 'Jugar', 106: 'Dhulikhel Sanjiwani Bazar-7', 141: 'Pokhara (Janapriya Marg)',
    171: 'Banphikot', 191: 'Chaukhutte, Mellekh', 243: 'Chaurjahari-2', 290: 'Kawasoti-2', 295: 'Gaindakot-5', 359: 'Dharmadevi-5',
    371: 'Tadi-3, Kharanitar', 406: 'Bargachhi, Biratnagar', 410: 'Bardibas', 421: 'Pyuthan', 459: 'Khimti', 475: 'Melamchitar',
    491: 'Madane-6, Purkot Daha', 504: 'Paiyun, Hattiya', 538: 'Bardaghat', 541: 'Yangwarak', 602: 'Pokhara-15, Prativa Tole',
    63: 'Sanibheri-8', 307: 'Bharatpur-11', 177: 'Tilottama-5, Manigram', 140: 'Devdaha-7, Shitalnagar', 211: 'Manahari-8, Simpani',
    300: 'Rangeli-7', 308: 'Bihadi', 343: 'Kajipokhari, Pokhara', 624: 'Ghartigaun', 489: 'Nadipur, Pokhara', 369: 'Shantiban, Pokhara',
    585: 'Madhyabindu', 510: 'Sundar Shanti, Belbari', 547: 'Gyalthum, Melamchi', 560: 'Kholi',
}

# campuses already in the dataset under another name (checked by name and district) or not a campus
# 542 is p-swargadwari-pyuthan (spelled Sworgadwari by NPCA); 46, 86, 519, 288, 410, 475, 569 are halves of an existing combined
# entry (Panini, Kapilvastu and Banganga, Sotang, Bardibas Janata, Indrawati, Gaumukhi); 370, 585, 141 are the same campus as
# p-w26-npca-9, p-w26-npca-145 and p-w24-iost-janapriya-mc
SKIP = {122, 503, 542, 46, 86, 519, 288, 410, 475, 569, 370, 585, 141}
NO_WEB = {370}  # page opens but never names the campus (audit_sites.py), so the link is left out


def npca_rows(by_district):
    rows = json.loads((HERE / 'npca_campuses.json').read_text(encoding='utf-8'))
    out = []
    for r in rows:
        k = r['npca_id']
        if r['district'] or k not in MAP or k in SKIP or not r['routes']:
            continue
        dist = MAP[k]['district']
        name = NAME.get(k) or C.NAME_FIX.get(k) or C._title(r['name'])
        key = re.sub(r'[^a-z]', '', name.lower().replace('multiple', '').replace('campus', ''))
        if any(key and key == x for x in by_district.get(dist, [])):
            continue
        row = dict(r)
        row['district'] = dist
        row['palika'] = MAP[k]['palika']
        out.append((row, name))
    return out
