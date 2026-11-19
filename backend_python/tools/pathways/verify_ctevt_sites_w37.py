"""Verifies candidate websites for CTEVT institutes from the e-mail domain on the official mapping portal.

A site is kept only when it answers HTTP 200 and its title or first 250 KB of text holds a distinctive word of the
institute name (not a generic word). Writes ctevt_sites_w37.json {inst_cd: url}. Never trusts an unopened link.
"""
import json
import re
import ssl
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36'
CTX = ssl.create_default_context()
FREE = ('gmail', 'yahoo', 'hotmail', 'outlook', 'mail.com', 'live.com', 'icloud', 'ymail', 'rediff', 'protonmail')
GENERIC = set('ctevt institute institution college school technical health science sciences polytechnic nepal nepalese secondary campus pvt ltd the of and for education educational academy foundation vocational training centre center multiple higher private limited annex engineering technology medical memorial research hospital community model shree sri trust pratisthan consortium'.split())


def words(name):
    name = re.sub(r'\(.*?\)', ' ', name.lower())
    return [w for w in re.sub(r'[^a-z ]', ' ', name).split() if w not in GENERIC and len(w) > 3]


def probe(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': 'text/html,*/*'})
    try:
        with urllib.request.urlopen(req, timeout=15, context=CTX) as r:
            if r.status != 200:
                return None, ''
            return r.geturl(), r.read(250000).decode('utf-8', 'ignore').lower()
    except Exception:
        return None, ''


def check(item):
    code, inst = item
    dom = inst['email'].split('@')[-1].strip().lower().rstrip('.,;') if inst.get('email') and '@' in inst['email'] else ''
    if not dom or any(f in dom for f in FREE) or '.' not in dom:
        return code, None, 'no domain'
    ws = words(inst['name']) or words(inst['list_name'])
    for url in ('https://www.' + dom, 'https://' + dom, 'http://www.' + dom, 'http://' + dom):
        final, text = probe(url)
        if final and ws and any(w in text for w in ws):
            return code, final.rstrip('/'), 'ok'
        if final:
            return code, None, 'no name word on ' + final
    return code, None, 'dead'


def main():
    insts = json.loads((HERE / 'ctevt_mapping_2083.json').read_text())['institutes']
    todo = [(str(i['inst_cd']), i) for i in insts]
    out, why = {}, {}
    with ThreadPoolExecutor(12) as ex:
        for code, url, reason in ex.map(check, todo):
            why[reason.split(' on ')[0]] = why.get(reason.split(' on ')[0], 0) + 1
            if url:
                out[code] = url
    (HERE / 'ctevt_sites_w37.json').write_text(json.dumps(out, indent=0) + '\n')
    print(len(out), 'verified of', len(todo), why)


if __name__ == '__main__':
    main()
