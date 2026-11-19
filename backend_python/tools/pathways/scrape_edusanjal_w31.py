"""Wave 31: reads the public Edusanjal college directory (https://edusanjal.com/college/?page=N, 66 pages) and writes edusanjal_list_w31.json
with each card's name, slug, affiliations and address. Used only to find colleges missing from our dataset; every row added is then read on its own page.
Polite: one request per 0.6 seconds, a normal user agent.
"""
import html
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

OUT = Path(__file__).resolve().parent / 'edusanjal_list_w31.json'
UA = {'User-Agent': 'Mozilla/5.0 (compatible; NEBians data check)'}


def get(url):
    for _ in range(3):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=25).read().decode('utf-8', 'replace')
        except Exception as e:  # noqa: BLE001
            err = e
            time.sleep(2)
    print('FAIL', url, err, file=sys.stderr)
    return ''


rows = {}
last = int(sys.argv[1]) if len(sys.argv) > 1 else 66
for page in range(1, last + 1):
    h = get(f'https://edusanjal.com/college/?page={page}')
    for card in h.split('<div class="overflow-hidden rounded-sm bg-white shadow-xl">')[1:]:
        m = re.search(r'<a href="/college/([^/"]+)/" class="text-xl[^"]*"><span class="grow min-w-0">(.*?)</span>', card)
        if not m:
            continue
        slug, name = m.group(1), html.unescape(m.group(2)).strip()
        aff = [html.unescape(x).strip() for x in re.findall(r'<a href="/university/[^"]+/" class="">(.*?)</a>', card)]
        ad = re.search(r'title="Address".*?<span class="ml-2">(.*?)</span>', card, re.S)
        rows[slug] = {'slug': slug, 'name': name, 'aff': aff, 'address': html.unescape(ad.group(1)).strip() if ad else ''}
    print(page, len(rows), flush=True)
    time.sleep(0.6)
OUT.write_text(json.dumps(list(rows.values()), ensure_ascii=False, indent=0), encoding='utf-8')
print('done', len(rows))
