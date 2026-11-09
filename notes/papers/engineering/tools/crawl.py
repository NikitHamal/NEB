#!/usr/bin/env python3
"""Generic polite crawler for past-paper research.
Usage: crawl.py OUT.json DEPTH MAXPAGES DOMAIN_REGEX SEED [SEED...]
Collects every <a>/<iframe>/<embed>/<source> link; classifies PDFs / docs / Google-Drive / other.
Respects: realistic UA, 15s timeout, 0.2s delay per worker. Output JSON: {pages:{url:title}, files:{url:{from,text}}, drive:{...}}
"""
import sys, re, json, time, urllib.parse as up
from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'
S = requests.Session(); S.headers['User-Agent'] = UA
FILE_RE = re.compile(r'\.(pdf|docx?|pptx?|zip|rar)(\?|$)', re.I)
DRIVE_RE = re.compile(r'(drive\.google\.com|docs\.google\.com|mediafire|dropbox\.com|mega\.nz|1drv\.ms|archive\.org/download|scribd\.com/document)', re.I)
def fetch(u):
    try:
        r = S.get(u, timeout=20)
        if 'html' not in r.headers.get('content-type', '') : return u, None, r.status_code
        return u, r.text, r.status_code
    except Exception as e:
        return u, None, str(e)[:60]
def main():
    out, depth, maxp, dom = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), re.compile(sys.argv[4])
    seeds = sys.argv[5:]
    seen, pages, files, drive = set(seeds), {}, {}, {}
    frontier = list(seeds)
    for d in range(depth + 1):
        if not frontier or len(pages) >= maxp: break
        with ThreadPoolExecutor(8) as ex:
            res = list(ex.map(fetch, frontier[: maxp - len(pages)]))
        nxt = []
        for u, html, code in res:
            if html is None: continue
            soup = BeautifulSoup(html, 'lxml')
            pages[u] = (soup.title.string.strip() if soup.title and soup.title.string else '')[:120]
            for t in soup.find_all(['a', 'iframe', 'embed', 'source', 'link'], href=True) + soup.find_all(['iframe','embed','source'], src=True):
                h = t.get('href') or t.get('src')
                if not h or h.startswith(('#', 'mailto:', 'javascript:', 'tel:')): continue
                h = up.urljoin(u, h).split('#')[0]
                txt = t.get_text(' ', strip=True)[:100]
                if FILE_RE.search(h): files.setdefault(h, {'from': u, 'text': txt})
                elif DRIVE_RE.search(h): drive.setdefault(h, {'from': u, 'text': txt})
                elif dom.search(h) and h not in seen and not re.search(r'\.(jpe?g|png|gif|css|js|svg|ico|webp)(\?|$)', h, re.I):
                    seen.add(h); nxt.append(h)
            # raw regex for urls hidden in scripts
            for m in re.findall(r'https?://[^\s"\'<>\\]+?\.pdf', html, re.I):
                files.setdefault(m, {'from': u, 'text': ''})
        frontier = nxt
        print(f'depth {d}: pages={len(pages)} files={len(files)} drive={len(drive)} next={len(nxt)}', file=sys.stderr)
    json.dump({'pages': pages, 'files': files, 'drive': drive}, open(out, 'w'), indent=1)
if __name__ == '__main__': main()
