#!/usr/bin/env python3
"""Turn crawl.py output into fetch.py tasks.
Usage: build_tasks.py CRAWL.json OUT_TASKS.json DEST_PREFIX META_JSON [FROM_REGEX]
Drive file links -> uc?export=download&id=; Drive folder links are expanded with gdown (listing only);
direct file links kept as is. Names come from the link text / URL basename."""
import sys, json, re, os, urllib.parse as up, warnings
warnings.filterwarnings('ignore')
def slug(s): return re.sub(r'[^A-Za-z0-9._-]+', '-', up.unquote(s)).strip('-')[:90]
d = json.load(open(sys.argv[1])); prefix = sys.argv[3]; meta = json.loads(sys.argv[4]); fr = re.compile(sys.argv[5]) if len(sys.argv) > 5 else None
tasks, seen = [], set()
def add(url, dest, extra):
    if url in seen: return
    seen.add(url); tasks.append({'url': url, 'dest': f'{prefix}/{dest}', 'meta': {**meta, **extra}})
for u, v in list(d['files'].items()) + list(d['drive'].items()):
    if fr and not fr.search(v['from']): continue
    page = slug(v['from'].rstrip('/').split('/')[-1] or 'index')
    ex = {'label': v['text'], 'page': v['from']}
    m = re.search(r'/folders/([\w-]+)', u)
    i = re.search(r'(?:/file/d/|[?&]id=)([\w-]+)', u)
    if m:
        try:
            import gdown
            for x in gdown.download_folder(id=m.group(1), skip_download=True, quiet=True, use_cookies=False):
                add(f'https://drive.google.com/uc?export=download&id={x.id}', f'{page}/{m.group(1)[:6]}/{slug(x.path)}', {**ex, 'drive_id': x.id, 'drive_folder': m.group(1)})
        except Exception as e: print('folder fail', m.group(1), str(e)[:60])
    elif i and 'google.com' in u:
        add(f'https://drive.google.com/uc?export=download&id={i.group(1)}', f'{page}/{slug(v["text"] or "file")}__{i.group(1)[:8]}.pdf', {**ex, 'drive_id': i.group(1)})
    elif re.search(r'\.(pdf|docx?|pptx?)(\?|$)', u, re.I):
        add(u, f'{page}/{slug(u.split("/")[-1])}', ex)
json.dump(tasks, open(sys.argv[2], 'w')); print(len(tasks), 'tasks')
