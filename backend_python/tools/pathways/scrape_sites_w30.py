"""Website discovery for provider rows that have none (wave 30).

For every provider without a website it builds candidate domains from the name, keeps only those that resolve and
answer over valid HTTPS, then accepts a candidate only when the page itself names the college (every distinctive word
of the name in the title / headings / first part of the text) and, when the name has a single distinctive word,
also names the district or town. Output: site_candidates_w30b.json (accepted + rejected with evidence).

Run: python3 backend_python/tools/pathways/scrape_sites_w30.py
"""
import concurrent.futures as cf
import json
import re
import socket
import ssl
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent))
from api import pathways as P  # noqa: E402

GENERIC = set('''college campus multiple multi school secondary higher institute institution academy pvt ltd private limited
 and of the for in at nepal nepali community public national international research center centre foundation technical
 polytechnic science sciences technology education educational vidyapeeth vidyalaya boarding sanskrit health
 nursing medical engineering management studies study memorial rastriya ma vi aadarsha adarsha samudayik ekikrit
 bahumukhi sahakari'''.split())
TLDS = ('.edu.np', '.com.np', '.org.np', '.com')
UA = {'User-Agent': 'Mozilla/5.0 (compatible; NEBians-dataset-check/1.0; +https://nebians.com)'}
CTX = ssl.create_default_context()


def words(name):
    name = re.sub(r'\(.*?\)', ' ', name)
    return [w for w in re.findall(r'[a-z0-9]+', name.lower())]


def distinctive(name):
    return [w for w in words(name) if w not in GENERIC and len(w) > 2]


def candidates(p):
    ws = words(p['name'])
    d = distinctive(p['name'])
    if not d:
        return []
    slugs = set()
    slugs.add(''.join(d))
    slugs.add(''.join(w for w in ws if w not in ('and', 'of', 'the', 'pvt', 'ltd')))
    kw = [w for w in ws if w in ('college', 'campus', 'school', 'institute', 'academy')]
    if kw:
        slugs.add(''.join(d) + kw[0])
        slugs.add(''.join(d) + kw[0][:1])
    base = ''.join(d)
    for suf in ('college', 'campus', 'mc', 'mcampus', 'school', 'institute', 'polytechnic', 'academy', 'pi', 'ti', 'nursing', 'hs'):
        slugs.add(base + suf)
    place = re.sub(r'[^a-z]', '', (p.get('place') or '').split(',')[-1].lower())
    dist = re.sub(r'[^a-z]', '', p['district'].lower())
    for loc in {place, dist}:
        if loc and loc not in base and len(loc) > 3:
            slugs.add(base + loc)
            slugs.add(base + 'campus' + loc)
    if len(d) >= 2:
        slugs.add(''.join(w[0] for w in d))
        slugs.add(''.join(w[0] for w in d) + 'c')
        slugs.add(''.join(w[0] for w in d) + 'college')
    slugs = {s for s in slugs if 3 <= len(s) <= 40}
    out = []
    for s in sorted(slugs):
        for t in TLDS:
            out.append(s + t)
    return list(dict.fromkeys(out))


def resolves(host):
    try:
        socket.getaddrinfo(host, 443, proto=socket.IPPROTO_TCP)
        return True
    except OSError:
        return False


def fetch(host):
    try:
        req = urllib.request.Request('https://' + host + '/', headers=UA)
        with urllib.request.urlopen(req, timeout=9, context=CTX) as r:
            raw = r.read(250000)
            final = r.geturl()
            code = r.status
    except Exception as e:  # noqa: BLE001
        return {'err': type(e).__name__ + ':' + str(e)[:60]}
    txt = raw.decode('utf-8', 'ignore')
    title = re.search(r'<title[^>]*>(.*?)</title>', txt, re.S | re.I)
    body = re.sub(r'<script.*?</script>|<style.*?</style>', ' ', txt, flags=re.S | re.I)
    body = re.sub(r'<[^>]+>', ' ', body)
    body = re.sub(r'\s+', ' ', body)
    return {'code': code, 'final': final, 'title': (title.group(1).strip() if title else '')[:140], 'text': body[:6000].lower()}


def check(p):
    d = distinctive(p['name'])
    res = {'id': p['id'], 'name': p['name'], 'tried': 0, 'ok': None}
    seen_final = set()
    for host in candidates(p):
        if not resolves(host):
            continue
        res['tried'] += 1
        f = fetch(host)
        if 'err' in f or f['code'] != 200:
            continue
        fin = re.sub(r'^https?://(www\.)?', '', f['final']).split('/')[0]
        if fin in seen_final:
            continue
        seen_final.add(fin)
        hay = (f['title'] + ' ' + f['text']).lower()
        head = (f['title'] + ' ' + f['text'][:1500]).lower()
        if not all(w in head for w in d):
            continue
        loc = [x.lower() for x in (p['district'], (p.get('place') or '').split(',')[-1].strip()) if x]
        near = any(x and x in hay for x in loc)
        if len(d) == 1 and not near:
            continue
        res['ok'] = {'host': host, 'final': f['final'], 'title': f['title'], 'near': near, 'words': d}
        break
    return res


def main():
    b = P.payload()
    used = {re.sub(r'^https?://(www\.)?', '', (x.get('website') or '')).split('/')[0] for x in b['providers']}
    todo = [p for p in b['providers'] if not p.get('website')]
    only = sys.argv[1:] 
    if only:
        todo = [p for p in todo if any(o in p['id'] for o in only)]
    out = []
    with cf.ThreadPoolExecutor(48) as ex:
        for r in ex.map(check, todo):
            if r['ok'] and re.sub(r'^www\.', '', r['ok']['final'].split('//')[1].split('/')[0]) in used:
                r['dup'] = True
            out.append(r)
            if r['ok']:
                print('OK ', r['id'], r['ok']['final'], '|', r['ok']['title'][:70], flush=True)
    (HERE / 'site_candidates_w30b.json').write_text(json.dumps(out, indent=1))
    print('accepted', sum(1 for r in out if r['ok']), 'of', len(out))


if __name__ == '__main__':
    main()
