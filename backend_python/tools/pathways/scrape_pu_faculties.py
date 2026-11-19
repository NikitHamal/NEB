"""Reads the Purbanchal University faculty pages (purbanchaluniversity.edu.np/faculties/...) and writes pu_colleges.json:
{faculty: {"programs": [[name, duration]], "colleges": [{name, address, district, programs}]}}.
Run: python3 backend_python/tools/pathways/scrape_pu_faculties.py   (needs network)"""
import json
import re
import urllib.request
from pathlib import Path

BASE = 'http://purbanchaluniversity.edu.np/faculties/'
PAGES = {'management': 'faculty-of-management14-32-07', 'science': 'faculty-of-science-technology11-10-47',
         'health': 'faculty-of-medical-allied-sciences11-43-25', 'arts': 'faculty-of-arts14-53-05',
         'education': 'faculty-of-education12-03-21', 'law': 'faculty-of-law12-03-45',
         'engineering': 'faculty-of-engineering10-30-59'}


def lines(html):
    html = re.sub(r'<script.*?</script>|<style.*?</style>', '', html, flags=re.S)
    txt = re.sub(r'<[^>]+>', '\n', html)
    txt = txt.replace('&amp;', '&').replace('&nbsp;', ' ').replace('&#160;', ' ')
    return [re.sub(r'\s+', ' ', x).strip() for x in txt.split('\n') if x.strip()]


def parse(ls):
    out = {'programs': [], 'colleges': []}
    try:
        i = ls.index('Programs')
        j = ls.index('College')
    except ValueError:
        return out
    k = i + 3
    while k < j and ls[k - 0:k + 1]:
        if ls[k].isdigit() and k + 3 < j + 1:
            out['programs'].append([ls[k + 1], ls[k + 2]])
            k += 4
        else:
            k += 1
    k = j + 3
    while k < len(ls):
        if ls[k].isdigit() and k + 4 < len(ls) and not ls[k + 1].isdigit():
            out['colleges'].append({'name': ls[k + 1], 'address': ls[k + 2], 'district': ls[k + 3], 'programs': ls[k + 4]})
            k += 5
        else:
            k += 1
    return out


if __name__ == '__main__':
    res = {}
    for key, slug in PAGES.items():
        html = urllib.request.urlopen(urllib.request.Request(BASE + slug, headers={'User-Agent': 'Mozilla/5.0'}), timeout=40).read().decode('utf8', 'ignore')
        res[key] = parse(lines(html))
        print(key, len(res[key]['programs']), len(res[key]['colleges']))
    (Path(__file__).resolve().parent / 'pu_colleges.json').write_text(json.dumps(res, indent=1, ensure_ascii=False))
