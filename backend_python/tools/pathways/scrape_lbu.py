"""Reads the Lumbini Buddhist University course lists (lbu.edu.np/fbscourses, fhss-courses, fdsas-courses, 19 Nov 2026)
and writes lbu_courses.json: [{code_title, campus, level, semester, credit}]. Run: python3 scrape_lbu.py"""
import json
import re
import subprocess
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).resolve().parent


class P(HTMLParser):
    def __init__(s):
        super().__init__()
        s.o, s.skip = [], 0

    def handle_starttag(s, t, a):
        if t in ('script', 'style', 'noscript'):
            s.skip += 1
        if t in ('p', 'div', 'li', 'tr', 'br', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'section'):
            s.o.append('\n')

    def handle_endtag(s, t):
        if t in ('script', 'style', 'noscript'):
            s.skip -= 1

    def handle_data(s, d):
        if not s.skip:
            s.o.append(d)


def text(url):
    h = subprocess.run(['curl', '-s', '-m', '30', '-L', '-A', 'Mozilla/5.0', url], capture_output=True).stdout.decode('utf8', 'ignore')
    p = P()
    p.feed(h)
    return [x.strip() for x in ''.join(p.o).split('\n') if x.strip()]


def parse(lines):
    out = []
    for i, ln in enumerate(lines):
        if ln.startswith('Department :'):
            title = lines[i - 1]
            rec = {'title': title}
            for nxt in lines[i:i + 6]:
                for k in ('Department', 'Campus', 'Level', 'Semester', 'Credit'):
                    if nxt.startswith(k + ' :'):
                        rec[k.lower()] = nxt.split(':', 1)[1].strip()
            out.append(rec)
    return out


def main():
    rows = []
    for path, pages in (('fbscourses', 3), ('fhss-courses', 3), ('fdsas-courses', 1)):
        for n in range(1, pages + 1):
            url = f'https://lbu.edu.np/{path}/' + (f'page/{n}/' if n > 1 else '')
            for r in parse(text(url)):
                r['page'] = path
                if r not in rows:
                    rows.append(r)
    (HERE / 'lbu_courses.json').write_text(json.dumps(rows, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(len(rows), 'courses')


if __name__ == '__main__':
    main()
