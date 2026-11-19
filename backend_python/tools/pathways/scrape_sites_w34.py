"""Wave 34 website finder: for providers without a website, tries name derived .edu.np/.com.np/.org.np domains and keeps a hit only if the
page answers HTTP 200 and its <title> contains every distinctive word of the college name. Output: /tmp/w/hits.json (checked, then copied into w34_sites.py)."""
import json, re, ssl, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, '.')
from api import pathways
STOP = {'college', 'campus', 'multiple', 'public', 'international', 'management', 'sciences', 'science', 'technology', 'and', 'of', 'the', 'for', 'higher', 'studies', 'pvt', 'ltd',
        'institute', 'school', 'academy', 'education', 'university', 'degree', 'tribhuvan', 'affiliated', 'private', 'limited', 'center', 'centre'}
ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
def words(name):
    name = re.sub(r'\(.*?\)', ' ', name)
    return [w for w in re.findall(r'[a-z]+', name.lower()) if w not in STOP and len(w) > 2]
def cands(p):
    ws = words(p['name'])
    allw = [w for w in re.findall(r'[a-z]+', re.sub(r'\(.*?\)', ' ', p['name']).lower()) if w not in ('and', 'of', 'the', 'pvt', 'ltd', 'limited')]
    if not ws: return []
    base = ''.join(ws); full = ''.join(allw)
    out = []
    for b in dict.fromkeys([base, full, ''.join(ws[:2]) if len(ws) > 1 else None]):
        if b and 4 <= len(b) <= 30:
            for tld in ('edu.np', 'com.np', 'org.np'):
                out.append(f'{b}.{tld}')
    return out[:6]
def title(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 NEBiansBot'})
        with urllib.request.urlopen(req, timeout=7, context=ctx) as r:
            if r.status != 200: return None
            html = r.read(60000).decode('utf-8', 'ignore')
        m = re.search(r'<title[^>]*>(.*?)</title>', html, re.S | re.I)
        return re.sub(r'\s+', ' ', m.group(1)).strip() if m else ''
    except Exception:
        return None
def work(p):
    ws = words(p['name'])
    for c in cands(p):
        t = title('https://' + c)
        if t is not None:
            tl = re.sub(r'[^a-z ]', ' ', t.lower())
            if ws and all(w in tl for w in ws[:3]):
                return p['id'], 'https://' + c, t
    return None
d = pathways.payload()
nw = [p for p in d['providers'] if not p.get('website')]
with ThreadPoolExecutor(24) as ex:
    res = [r for r in ex.map(work, nw) if r]
json.dump(res, open('/tmp/w/hits.json', 'w'), indent=1)
print(len(nw), 'checked', len(res), 'hits')
for r in res: print(r)
