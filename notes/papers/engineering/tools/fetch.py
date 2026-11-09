#!/usr/bin/env python3
"""Bulk downloader with manifest.
Usage: fetch.py TASKS.json MANIFEST.jsonl [--root DIR]
TASKS.json: list of {"url","dest" (relative to repo root notes/papers/engineering/sources),"meta":{...}}
Downloads in parallel (8), validates %PDF/office magic, dedupes by sha256, appends manifest lines:
 {url,dest,sha256,bytes,pages,title,meta,status}
"""
import sys, json, os, hashlib, re, warnings
from concurrent.futures import ThreadPoolExecutor
warnings.filterwarnings('ignore')
import requests
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'
ROOT = os.environ.get('PAPERS_ROOT', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sources'))
def info(path):
    try:
        import pymupdf
        d = pymupdf.open(path); n = len(d)
        t = ' '.join(d[0].get_text().split())[:140] if n else ''
        return n, t
    except Exception as e:
        return 0, ''
def one(t):
    url, dest = t['url'], os.path.join(ROOT, t['dest'])
    rec = {'url': url, 'dest': t['dest'], 'meta': t.get('meta', {})}
    if os.path.exists(dest) and os.path.getsize(dest) > 500:
        data = open(dest, 'rb').read(); rec['status'] = 'exists'
    else:
        try:
            r = requests.get(url, headers={'User-Agent': UA, 'Referer': t.get('referer', url)}, timeout=60, allow_redirects=True)
            data = r.content
            if r.status_code != 200: rec['status'] = f'http{r.status_code}'; return rec
            if not (data[:5] == b'%PDF-' or data[:4] in (b'PK\x03\x04', b'\xd0\xcf\x11\xe0', b'\x89PNG') or data[:3] == b'\xff\xd8\xff'): rec['status'] = 'notfile:' + r.headers.get('content-type', '')[:30]; return rec
            os.makedirs(os.path.dirname(dest), exist_ok=True); open(dest, 'wb').write(data); rec['status'] = 'ok'
        except Exception as e:
            rec['status'] = 'err:' + str(e)[:50]; return rec
    rec['sha256'] = hashlib.sha256(data).hexdigest(); rec['bytes'] = len(data)
    if data[:5] == b'%PDF-': rec['pages'], rec['title'] = info(dest)
    return rec
if __name__ == '__main__':
    tasks = json.load(open(sys.argv[1])); man = sys.argv[2]
    if '--root' in sys.argv: ROOT = sys.argv[sys.argv.index('--root') + 1]
    with ThreadPoolExecutor(8) as ex: res = list(ex.map(one, tasks))
    with open(man, 'a') as f:
        for r in res: f.write(json.dumps(r, ensure_ascii=False) + '\n')
    from collections import Counter
    print(Counter(r['status'].split(':')[0] for r in res), 'total bytes', sum(r.get('bytes', 0) for r in res))
