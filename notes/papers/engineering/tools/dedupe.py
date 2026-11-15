#!/usr/bin/env python3
"""Remove files from NEW manifest whose sha256 (original bytes) already appears in another manifest. Usage: dedupe.py NEW_MANIFEST.jsonl"""
import sys, json, glob, os
base = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'); new = sys.argv[1]
seen = {}
for f in glob.glob(base + '/manifests/*.jsonl'):
    if os.path.abspath(f) == os.path.abspath(new): continue
    for l in open(f):
        r = json.loads(l)
        if r.get('status') == 'ok' and r.get('sha256'): seen.setdefault(r['sha256'], r['dest'])
n = 0; mine = set()
for l in open(new):
    r = json.loads(l)
    if r.get('status') != 'ok' or not r.get('sha256'): continue
    p = os.path.join(base, 'sources', r['dest'])
    if (r['sha256'] in seen or r['sha256'] in mine) and os.path.exists(p): os.remove(p); n += 1; print('dup', r['dest'], '==', seen.get(r['sha256'], 'self'))
    mine.add(r['sha256'])
print('removed', n)
