#!/usr/bin/env python3
"""Retry failed Drive downloads (virus-scan/large-file interstitials) via gdown.
Usage: retry_gdown.py TASKS.json MANIFEST.jsonl   (retries tasks whose latest manifest status is not ok/exists; appends results)
Run from repo root. Uses 4 threads, 100 s overall budget by default (env BUDGET)."""
import sys, os, json, time, hashlib, warnings
from concurrent.futures import ThreadPoolExecutor
warnings.filterwarnings('ignore')
import gdown
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import fetch
tasks = json.load(open(sys.argv[1])); man = sys.argv[2]
done = set()
if os.path.exists(man):
    for l in open(man):
        r = json.loads(l)
        if r['status'] in ('ok', 'exists'): done.add(r['url'])
todo = [t for t in tasks if t['url'] not in done and 'id=' in t['url'] and not os.path.exists(os.path.join(fetch.ROOT, t['dest']))]
T0 = time.time(); BUD = float(os.environ.get('BUDGET', 100))
def one(t):
    rec = {'url': t['url'], 'dest': t['dest'], 'meta': {**t.get('meta', {}), 'via': 'gdown'}}
    if time.time() - T0 > BUD: rec['status'] = 'skipped-budget'; return rec
    dest = os.path.join(fetch.ROOT, t['dest']); os.makedirs(os.path.dirname(dest), exist_ok=True)
    try:
        fid = t['url'].split('id=')[1]
        p = gdown.download(id=fid, output=dest, quiet=True, use_cookies=False)
        if not p or not os.path.exists(dest): rec['status'] = 'gdown-fail'; return rec
        data = open(dest, 'rb').read()
        if not (data[:5] == b'%PDF-' or data[:4] in (b'PK\x03\x04', b'\xd0\xcf\x11\xe0')): os.remove(dest); rec['status'] = 'notfile'; return rec
        rec.update(status='ok', sha256=hashlib.sha256(data).hexdigest(), bytes=len(data))
        if data[:5] == b'%PDF-': rec['pages'], rec['title'] = fetch.info(dest)
    except Exception as e: rec['status'] = 'err:' + str(e)[:60]
    return rec
with ThreadPoolExecutor(4) as ex: res = list(ex.map(one, todo))
with open(man, 'a') as f:
    for r in res: f.write(json.dumps(r, ensure_ascii=False) + '\n')
from collections import Counter; print(len(todo), 'todo', Counter(r['status'].split(':')[0] for r in res), sum(r.get('bytes', 0) for r in res))
