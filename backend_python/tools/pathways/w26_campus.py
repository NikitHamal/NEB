"""Wave 26: constituent campuses of Tribhuvan University that the dataset did not list yet, and community campuses from NPCA.

Sources (opened on 2026-11-18):
- Official TU campus list https://tu.edu.np/campuses (8 pages, 64 campuses, each with an official subdomain, all HTTP 200).
  Each campus page below was read: address line, establishment text and the "Our Courses" block.
- NPCA (Nepal Public Campuses Association) member pages https://npca.edu.np/campus_details/<id>, ids 1 to 635, 495 live pages,
  scraped by tools/pathways/scrape_npca.py and saved to tools/pathways/npca_campuses.json. A campus is added only when
  (a) the NPCA address names a district, or the campus name does (21 of them) or its site names it twice in its address block,
  (b) it is not already in the dataset, (c) it lists at least one programme. Its website is kept only when the page opened (HTTP < 400).
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent

# (suffix, name, district, place, website, note, routes)
TU_ROWS = [
    ('tu-mmc', 'Maharajgunj Medical Campus (Institute of Medicine, TU)', 'Kathmandu', 'Maharajgunj', 'https://mmc.tu.edu.np',
     'Established 1972 (2029 BS) as the first medical education centre of Nepal and the oldest constituent campus of the Institute of Medicine. '
     'Its official page lists 40+ graduate, postgraduate and super-specialty courses in medical, dental, laboratory technology, pharmacy, optometry, '
     'radiography, speech and language pathology and perfusion technology. Seats are counted under the Institute of Medicine entry. Phone 01-4514792.',
     ['mbbs', 'bds', 'bmlt', 'bpharm', 'boptom', 'baslp', 'bperfusion-anesthesia', 'md-ms']),
    ('tu-mnc', 'Maharajgunj Nursing Campus (Institute of Medicine, TU)', 'Kathmandu', 'Maharajgunj', 'https://mnc.tu.edu.np',
     'Campus page lists B.Sc. Nursing, Bachelor of Nursing Science (Adult, Child, Community and Psychiatric tracks) and the Master of Nursing '
     '(Psychiatric, Adult, Pediatric, Women Health Development). The campus text says the MN began in 2051 BS, B.Sc. Nursing in 2062 BS and PhD Nursing in 2068 BS. Phone 01-4720423.',
     ['bsc-nursing', 'bns', 'msc-nursing']),
    ('tu-gac', 'Gauradaha Agriculture Campus (IAAS, TU)', 'Jhapa', 'Gauradaha', 'https://gac.tu.edu.np',
     'The only constituent campus of the TU Institute of Agriculture and Animal Science in Koshi Province. Offers B.Sc.Ag. (4 years); its notice board (2026-10-01) announces '
     'local quota and IDF seat admission. Practice field of 5.5 bigha in front of the campus.',
     ['bsc-agri']),
    ('tu-rampur', 'Rampur Campus (IAAS, TU)', 'Chitwan', 'Rampur, Khairahani', 'https://rc.tu.edu.np',
     'The first agriculture college of TU, started in 1972 at Pulchowk and moved to Rampur, Chitwan in 1974 (campus land 235 ha). Offers B.Sc.Ag. Official page: Institute of Agriculture and Animal Science.',
     ['bsc-agri']),
    ('tu-pyc', 'Public Youth Campus (TU)', 'Kathmandu', 'Yapikhya Marg, Chhetrapati, Dhobichaur', 'https://pyc.tu.edu.np',
     'TU Faculty of Management constituent campus, established 1971 (2028 BS) after the New Education System Plan. Courses on its page: BBA, BBM, MBS and MBM. Phone 9851326760.',
     ['bba', 'bbm', 'mbs']),
    ('tu-bbc', 'Bishwa Bhasa Campus (TU)', 'Kathmandu', 'Pradarshani Marg', 'https://bbc.tu.edu.np',
     'TU foreign language campus. Its notices (2026) publish results of German, Italian, Japanese and Spanish language levels (II to VI) and a level test, and it has a section for foreign students. Course fees are not on the page.',
     ['foreign-lang-work']),
]

# NPCA ids that are already in the dataset under another name or id (checked by name and district), or garbage rows
SKIP_NPCA = {
    2, 13, 33, 60, 91, 102, 103, 152, 166, 167, 195, 148, 271, 299, 226, 380, 429, 579, 218, 25, 121, 202, 293, 296, 306, 309,
    310, 313, 317, 326, 333, 337, 348, 485, 543, 545, 574, 357, 274, 35,
}
NAME_FIX = {
    4: 'Radijyula Shiksha Campus', 9: 'Shree Ramprasad Tamang Janta Multiple Campus', 12: 'Gaurishankar Multiple Campus', 17: 'Sapahi College',
    21: 'Ram Raja (M. B. Shah) Multiple Campus', 96: 'Tejganga Multiple Campus', 113: 'Nepal Aadarsha Multiple Campus',
    153: 'Dronachal Multiple Campus', 165: 'Gadhimai Multiple Campus', 287: 'Krishna Baijanath Multiple Campus',
    382: 'Adarsha Multiple Campus', 404: 'Bangad Campus', 498: 'Khotang Campus', 581: 'Rastriya Campus', 584: 'Chamunda College',
    613: 'Turmakhand Multiple Campus',
}
PLACE_FIX = {83: 'Dillibazar', 17: 'Kolhabi-4, Sapahi', 96: 'Panauti', 581: 'Dattu, Mahakali'}
NO_WEB = {600}  # NPCA lists its own site (npca.edu.np) for this campus, which is not the campus site
NPCA_NOTE = 'Community campus on the Nepal Public Campuses Association (NPCA) member list. '


def _tidy(addr, district):
    a = re.sub(r'\s+', ' ', addr).strip(' ,.-')
    if a in ('Offered Programs', 'Official Address') or len(a) > 42:
        return district
    a = re.sub(r',?\s*' + re.escape(district) + r'\s*$', '', a, flags=re.I).strip(' ,.-')
    return a or district


def _title(name):
    n = re.sub(r'\s+', ' ', name).strip()
    return n.title() if n.upper() == n or n.lower() == n else n


def npca_rows(existing_names_by_district):
    rows = json.loads((HERE / 'npca_campuses.json').read_text(encoding='utf-8'))
    out = []
    for r in rows:
        if not r['district'] or r['npca_id'] in SKIP_NPCA or not r['routes']:
            continue
        name = NAME_FIX.get(r['npca_id']) or _title(r['name'])
        key = re.sub(r'[^a-z]', '', name.lower().replace('multiple', '').replace('campus', ''))
        if any(key and key == k for k in existing_names_by_district.get(r['district'], [])):
            continue
        out.append((r, name))
    return out
