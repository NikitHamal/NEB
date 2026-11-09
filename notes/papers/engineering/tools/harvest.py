#!/usr/bin/env python3
"""Regex harvester over RAW html (works where crawl.py/bs4 misses links in JSON-LD/JS).
Usage: harvest.py OUT_TASKS.json DEST_PREFIX META_JSON FOLLOW_REGEX MAXPAGES URL [URL...]
Collects drive file/folder links, sharepoint links, direct pdf/doc(x)/ppt links with anchor text; follows same-host links matching FOLLOW_REGEX (1 level).
Folders are expanded with gdown (listing only). Output is fetch.py-compatible."""
import sys, re, json, urllib.parse as up, requests, warnings
from concurrent.futures import ThreadPoolExecutor
warnings.filterwarnings('ignore')
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0'
out, prefix, meta, follow, maxp = sys.argv[1], sys.argv[2], json.loads(sys.argv[3]), re.compile(sys.argv[4]), int(sys.argv[5]); seeds = sys.argv[6:]
def slug(s): return re.sub(r'[^A-Za-z0-9._-]+', '-', up.unquote(s)).strip('-')[:80]
def get(u):
    try: return u, requests.get(u, headers={'User-Agent': UA}, timeout=20).text
    except Exception: return u, ''
pages = {}
with ThreadPoolExecutor(8) as ex:
    for u, h in ex.map(get, seeds): pages[u] = h
    nxt = []
    for u, h in list(pages.items()):
        for m in re.findall(r'href=["\']([^"\']+)', h):
            a = up.urljoin(u, m).split('#')[0]
            if follow.search(a) and a not in pages and a not in nxt and up.urlparse(a).netloc == up.urlparse(u).netloc: nxt.append(a)
    for u, h in ex.map(get, nxt[:maxp]): pages[u] = h
FILE = re.compile(r'https?://[^"\'\s<>\\]+?\.(?:pdf|docx?|pptx?)(?:\?[^"\'\s<>\\]*)?', re.I)
DRV = re.compile(r'https?://(?:drive|docs)\.google\.com/(?:file/d/|drive/folders/|uc\?[^"\'\s<>]*id=|open\?id=)[\w-]+[^"\'\s<>\\]*|https?://[\w-]+\.sharepoint\.com/:b:/[^"\'\s<>\\]+', re.I)
tasks, seen = [], set()
def add(url, dest, extra):
    if url in seen: return
    seen.add(url); tasks.append({'url': url, 'dest': f'{prefix}/{dest}', 'meta': {**meta, **extra}})
for u, h in pages.items():
    pg = slug(u.rstrip('/').split('/')[-1] or 'index')
    for m in FILE.findall(h):
        add(m.replace('&amp;', '&'), f'{pg}/{slug(m.split("/")[-1].split("?")[0])}', {'page': u})
    for m in DRV.findall(h):
        m = m.replace('&amp;', '&'); i = re.search(r'(?:/file/d/|[?&]id=)([\w-]+)', m); f = re.search(r'/folders/([\w-]+)', m)
        if f:
            try:
                import gdown
                for x in gdown.download_folder(id=f.group(1), skip_download=True, quiet=True, use_cookies=False):
                    add(f'https://drive.google.com/uc?export=download&id={x.id}', f'{pg}/{f.group(1)[:6]}/{slug(x.path)}', {'page': u, 'drive_id': x.id, 'drive_folder': f.group(1)})
            except Exception as e: print('folder fail', f.group(1), str(e)[:50])
        elif i and 'google' in m: add(f'https://drive.google.com/uc?export=download&id={i.group(1)}', f'{pg}/file__{i.group(1)[:10]}.pdf', {'page': u, 'drive_id': i.group(1)})
        elif 'sharepoint' in m: add(m.split('?')[0] + '?download=1', f'{pg}/sp__{slug(m[-12:])}.pdf', {'page': u, 'orig_url': m})
json.dump(tasks, open(out, 'w'), indent=1); print(len(pages), 'pages;', len(tasks), 'tasks')
