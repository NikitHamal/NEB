"""Scrapes the official CTEVT institute mapping portal (mapping.ctevt.org.np) for fiscal year 2083.

Writes tools/pathways/ctevt_mapping_2083.json: {"institutes": [{inst_cd, name, district, province, type, phone, email,
website, principal, programs: [[name, quota, enrolled]]}]}.
Run: python3 backend_python/tools/pathways/scrape_ctevt_w37.py
The portal lists only institutes with an approved quota for the year; the type is Private, Partnership, Constituent or TECS.
"""
import json
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

BASE = 'https://mapping.ctevt.org.np/ajax/'
OUT = Path(__file__).resolve().parent / 'ctevt_mapping_2083.json'
YEAR = '2083'


def get(path, **params):
    url = BASE + path + '?' + urllib.parse.urlencode(params)
    for attempt in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=60) as r:
                return json.loads(r.read().decode('utf-8'))
        except Exception:
            time.sleep(1.5 * (attempt + 1))
    return {'success': False}


def listing(province, itype):
    return get('institutes', year=YEAR, level_cd='', faculty_cd='', sub_faculty_cd='', institute_type=itype,
               province_cd=province, district_cd='', mun_cd='').get('result') or []


def main():
    base = {}
    for prov in range(1, 8):
        for itype in ('', ):
            for row in listing(prov, itype):
                row['province_cd'] = prov
                base[row['inst_cd']] = row
        print('province', prov, len(base))
    codes = sorted(base, key=int)

    def detail(code):
        res = get('institute_details', inst_cd=code, year=YEAR).get('result') or []
        return code, (res[0] if res else None)

    with ThreadPoolExecutor(8) as ex:
        details = dict(ex.map(detail, codes))
    out = []
    for code in codes:
        b, d = base[code], details.get(code) or {}
        out.append({
            'inst_cd': int(code), 'name': (d.get('inst_name') or b['name']).strip(), 'list_name': b['name'].strip(),
            'district': b.get('district_name'), 'province': d.get('province_name'), 'province_cd': b['province_cd'],
            'municipality': d.get('vdc_name'), 'type': d.get('status_name'), 'phone': d.get('telephone'),
            'email': d.get('email'), 'website': b.get('website') or d.get('website'), 'principal': d.get('principal_name'),
            'lat': b.get('latitude'), 'lng': b.get('longitude'),
            'programs': [[p['program_name'], int(p['total_quota'] or 0), int(p['total_enrollment'] or 0)] for p in d.get('programs') or []],
            'list_program': b.get('program'),
        })
    OUT.write_text(json.dumps({'year': YEAR, 'source': 'mapping.ctevt.org.np/ajax/institutes and institute_details', 'institutes': out},
                              ensure_ascii=False, indent=0) + '\n', encoding='utf-8')
    print('institutes', len(out), 'with details', sum(1 for o in out if o['programs']))


if __name__ == '__main__':
    main()
