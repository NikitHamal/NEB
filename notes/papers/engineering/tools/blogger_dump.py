#!/usr/bin/env python3
"""Dump Blogger posts (full text) via the public JSON feed.
Usage: blogger_dump.py BLOG_BASE OUT_DIR [LABEL] [TITLE_REGEX]
Writes OUT_DIR/index.jsonl (title,url,published,labels,pdf/drive links) and OUT_DIR/posts/<slug>.md (plain text of post body)."""
import sys, re, json, os, requests
from bs4 import BeautifulSoup
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36'}
base, out = sys.argv[1].rstrip('/'), sys.argv[2]; label = sys.argv[3] if len(sys.argv) > 3 and sys.argv[3] != '-' else None
tre = re.compile(sys.argv[4], re.I) if len(sys.argv) > 4 else None
os.makedirs(out + '/posts', exist_ok=True); idx = open(out + '/index.jsonl', 'w'); start = 1; n = 0
while True:
    url = f'{base}/feeds/posts/default' + (f'/-/{label}' if label else '') + f'?alt=json&max-results=150&start-index={start}'
    r = requests.get(url, headers=UA, timeout=60)
    if r.status_code != 200: print('stop', r.status_code); break
    ents = r.json().get('feed', {}).get('entry', [])
    if not ents: break
    for e in ents:
        title = e['title']['$t']
        if tre and not tre.search(title): continue
        link = next((l['href'] for l in e['link'] if l['rel'] == 'alternate'), '')
        html = e.get('content', {}).get('$t', '')
        s = BeautifulSoup(html, 'lxml'); text = s.get_text('\n', strip=True)
        links = sorted({a['href'] for a in s.find_all(['a', 'iframe'], href=True) if re.search(r'pdf|drive|docs\.google|mediafire', a['href'], re.I)} | {f['src'] for f in s.find_all('iframe', src=True)})
        slug = re.sub(r'[^A-Za-z0-9]+', '-', title)[:90].strip('-') + f'-{n}'
        open(f'{out}/posts/{slug}.md', 'w').write(f'# {title}\n\nSource: {link}\nPublished: {e["published"]["$t"][:10]}\n\n{text}\n')
        idx.write(json.dumps({'title': title, 'url': link, 'published': e['published']['$t'][:10], 'labels': [c['term'] for c in e.get('category', [])], 'links': links, 'chars': len(text)}, ensure_ascii=False) + '\n'); n += 1
    start += len(ents)
print(n, 'posts')
