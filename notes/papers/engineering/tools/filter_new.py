#!/usr/bin/env python3
"""Drop tasks whose URL (or drive id) is already status ok/exists in any manifest.
Usage: filter_new.py TASKS.json OUT.json  (run from anywhere)"""
import sys, json, glob, os, re
base = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'manifests')
def key(u):
    m = re.search(r'(?:/file/d/|[?&]id=)([\w-]+)', u); return m.group(1) if m else u
done = set()
for f in glob.glob(base + '/*.jsonl'):
    for l in open(f):
        try: r = json.loads(l)
        except Exception: continue
        if r.get('status') in ('ok', 'exists'): done.add(key(r['url']))
t = json.load(open(sys.argv[1])); n = [x for x in t if key(x['url']) not in done]
json.dump(n, open(sys.argv[2], 'w'), indent=1); print(len(t), '->', len(n), 'new tasks')
