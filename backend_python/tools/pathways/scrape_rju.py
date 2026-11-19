"""Reads the Rajarshi Janak University site: affiliated colleges (rju.edu.np/affiliated-colleges/) and the course search
(rju.edu.np/course-search/, 2 pages) into rju_affiliated.json and rju_courses.json.
Run: python3 backend_python/tools/pathways/scrape_rju.py   (needs network)"""
import json
import re
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent


def get(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'}), timeout=40).read().decode('utf8', 'ignore')


def flat(h):
    h = re.sub(r'<script.*?</script>|<style.*?</style>', '', h, flags=re.S)
    t = re.sub(r'<[^>]+>', '|', h).replace('&amp;', '&').replace('&#038;', '&').replace('&#8211;', '-')
    return re.sub(r'\s+', ' ', re.sub(r'\|[\s|]*\|', '|', t))


if __name__ == '__main__':
    t = flat(get('https://rju.edu.np/affiliated-colleges/'))
    body = t[t.rfind('Affiliated Colleges|'):]
    aff = [[a.strip(), b.strip()] for a, b in re.findall(r'\|([^|]+)\|([^|]*?Nepal)\|Email:', body)]
    (HERE / 'rju_affiliated.json').write_text(json.dumps(aff, indent=1, ensure_ascii=False))
    courses = []
    for pg in ('', 'page/2/'):
        t = flat(get('https://rju.edu.np/course-search/' + pg + '?course-keywords=&campus=&level='))
        for m in re.finditer(r'\|([A-Za-z.\- ]{2,12})\|([^|]+)\|Campus : \|([^|]+)\|Level : \|(\w+)\|', t):
            courses.append(list(m.groups()))
    (HERE / 'rju_courses.json').write_text(json.dumps(courses, indent=1, ensure_ascii=False))
    print(len(aff), 'affiliated colleges;', len(courses), 'courses')
