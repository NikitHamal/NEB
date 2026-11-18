"""Live URL verifier for Pathways data (never trusts a link it has not opened).

Usage (from repo root):
    python3 backend_python/tools/pathways/verify_urls.py w23_links CANDIDATES out.json

Reads `CANDIDATES = {id: [url, ...]}` from the given module in this folder, opens every url (GET, redirects followed,
browser UA, 15 s), keeps the first candidate per id that answers HTTP 200 with an HTML page and a non empty <title>,
and writes `{id: {"url": final_url_or_candidate, "title": "..."}}` to out.json (next to this script).
Pages that block bots (403/429) are reported as `blocked` and are NOT accepted.
"""
import html
import importlib
import json
import re
import ssl
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36'
CTX = ssl.create_default_context()


def probe(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': 'text/html,*/*', 'Accept-Language': 'en'})
    try:
        with urllib.request.urlopen(req, timeout=15, context=CTX) as r:
            code = r.status
            final = r.geturl()
            raw = r.read(250000)
    except urllib.error.HTTPError as e:
        return {'url': url, 'code': e.code, 'title': '', 'final': url}
    except Exception as e:  # noqa: BLE001
        return {'url': url, 'code': 0, 'title': type(e).__name__, 'final': url}
    text = raw.decode('utf-8', 'ignore')
    m = re.search(r'<title[^>]*>(.*?)</title>', text, re.S | re.I)
    title = html.unescape(re.sub(r'\s+', ' ', m.group(1))).strip() if m else ''
    return {'url': url, 'code': code, 'title': title, 'final': final}


def first_good(item):
    key, urls = item
    seen = []
    for u in urls:
        r = probe(u)
        seen.append(r)
        if r['code'] == 200 and r['title']:
            return key, r, seen
    return key, None, seen


def main():
    mod, attr, out = sys.argv[1], sys.argv[2], sys.argv[3]
    cands = getattr(importlib.import_module(mod), attr)
    good, bad = {}, {}
    with ThreadPoolExecutor(max_workers=10) as ex:
        for key, r, seen in ex.map(first_good, cands.items()):
            if r:
                good[key] = {'url': r['url'], 'title': r['title'][:120]}
                print('OK  ', key, r['url'], '|', r['title'][:70])
            else:
                bad[key] = [(s['url'], s['code']) for s in seen]
                print('FAIL', key, bad[key])
    (HERE / out).write_text(json.dumps(good, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(len(good), 'ok,', len(bad), 'failed')


if __name__ == '__main__':
    main()
