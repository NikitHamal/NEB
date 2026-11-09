#!/usr/bin/env python3
"""Slow, polite Wayback fallback for dead hosts.
Usage: wayback_fetch.py TASKS.json MANIFEST.jsonl   (tasks as for fetch.py; only status!=ok ones should be passed)
Looks up closest snapshot via archive.org/wayback/available, downloads raw bytes (id_ flag), 5 s between requests, backs off on 429."""
import sys, json, time, os, hashlib, requests, warnings
warnings.filterwarnings('ignore')
sys.path.insert(0, os.path.dirname(__file__))
import fetch
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'
def get(u, tries=5):
    for k in range(tries):
        r = requests.get(u, headers={'User-Agent': UA}, timeout=60)
        if r.status_code == 429: time.sleep(20 * (k + 1)); continue
        return r
    return r
tasks = json.load(open(sys.argv[1])); out = open(sys.argv[2], 'a')
for t in tasks:
    rec = {'url': t['url'], 'dest': t['dest'], 'meta': {**t.get('meta', {}), 'via': 'wayback'}}
    dest = os.path.join(fetch.ROOT, t['dest'])
    try:
        a = get('http://archive.org/wayback/available?url=' + t['url']).json()
        snap = a.get('archived_snapshots', {}).get('closest')
        if not snap: rec['status'] = 'no-snapshot'
        else:
            ts = snap['timestamp']; rec['snapshot'] = ts
            r = get(f'https://web.archive.org/web/{ts}id_/{t["url"]}')
            d = r.content
            if r.status_code == 200 and d[:5] == b'%PDF-' or d[:4] in (b'PK\x03\x04', b'\xd0\xcf\x11\xe0') and r.status_code == 200:
                os.makedirs(os.path.dirname(dest), exist_ok=True); open(dest, 'wb').write(d); rec['status'] = 'ok'
                rec['sha256'] = hashlib.sha256(d).hexdigest(); rec['bytes'] = len(d)
                if d[:5] == b'%PDF-': rec['pages'], rec['title'] = fetch.info(dest)
            else: rec['status'] = f'http{r.status_code}'
    except Exception as e: rec['status'] = 'err:' + str(e)[:50]
    out.write(json.dumps(rec, ensure_ascii=False) + '\n'); out.flush(); time.sleep(5)
