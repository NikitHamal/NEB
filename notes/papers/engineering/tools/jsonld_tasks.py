#!/usr/bin/env python3
"""Build fetch.py tasks from schema.org ItemList JSON-LD (DigitalDocument items) embedded in a page.
Usage: jsonld_tasks.py PAGE_URL OUT_TASKS.json DEST_PREFIX META_JSON"""
import sys, re, json, requests, urllib.parse as up
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0'
def slug(s): return re.sub(r'[^A-Za-z0-9._-]+', '-', s).strip('-')[:90]
def walk(o):
    if isinstance(o, dict):
        if o.get('@type') == 'DigitalDocument' and o.get('url'): yield o
        for v in o.values(): yield from walk(v)
    elif isinstance(o, list):
        for v in o: yield from walk(v)
url, out, prefix, meta = sys.argv[1], sys.argv[2], sys.argv[3], json.loads(sys.argv[4])
h = requests.get(url, headers={'User-Agent': UA}, timeout=40).text
tasks, seen = [], set()
for m in re.finditer(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', h, re.S):
    try: j = json.loads(m.group(1))
    except Exception: continue
    for d in walk(j):
        u = d['url']; i = re.search(r'(?:/file/d/|[?&]id=)([\w-]+)', u)
        if u in seen: continue
        seen.add(u)
        name = d.get('name', 'file')
        if i and 'google' in u:
            fu = f'https://drive.google.com/uc?export=download&id={i.group(1)}'; fid = i.group(1)[:8]
        else: fu = u; fid = ''
        sem = slug(d.get('educationalLevel', 'misc')).lower()
        tasks.append({'url': fu, 'dest': f'{prefix}/{sem}/{slug(name)}__{fid}.pdf', 'meta': {**meta, 'label': name, 'description': d.get('description', ''), 'page': url}})
json.dump(tasks, open(out, 'w'), indent=1); print(len(tasks), 'tasks')
