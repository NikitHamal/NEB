"""Wave 39 website finder: for providers without a website, guesses domains from the name, keeps a domain only when it resolves, answers HTTP 200
and its <title> or first 60 KB hold all distinctive words of the name (at most 3) plus the district or place. Output /tmp/w/w39_sites.json for a manual look.
Run: python3 scrape_sites_w39.py [limit]
"""
import json, re, socket, ssl, sys, html as H, urllib.request, importlib.util
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent
spec = importlib.util.spec_from_file_location('pw', ROOT / 'api' / 'pathways.py'); pw = importlib.util.module_from_spec(spec); spec.loader.exec_module(pw)
STOP = {'college', 'campus', 'multiple', 'public', 'international', 'management', 'sciences', 'science', 'technology', 'and', 'of', 'the', 'for', 'higher', 'studies', 'pvt', 'ltd',
        'institute', 'school', 'academy', 'education', 'university', 'secondary', 'technical', 'polytechnic', 'nepal', 'shree', 'sri', 'memorial', 'center', 'centre', 'training',
        'private', 'limited', 'higher', 'community', 'new', 'national', 'city', 'foundation', 'lions', 'ra', 'na', 'ya', 'bhagwati', 'adarsha', 'janata', 'model', 'mahavidyalaya', 'faculty', 'engineering'}
KEEP = {'engineering'}
ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36'
def words(name):
    name = re.sub(r'\(.*?\)', ' ', name)
    return [w for w in re.findall(r'[a-z]+', name.lower()) if (w not in STOP or w in KEEP) and len(w) > 2]
def kind_word(name):
    n = name.lower()
    for k in ('college', 'campus', 'institute', 'academy', 'polytechnic', 'school'):
        if k in n: return k
    return ''
def cands(p):
    ws = words(p['name']); kw = kind_word(p['name']); base = ''.join(ws)
    if not ws: return []
    names = [base, base + kw, base + 'college', base + 'campus', '-'.join(ws), '-'.join(ws) + '-' + kw] if kw else [base, base + 'college']
    ab = re.findall(r'\(([A-Za-z]{2,8})\)', p['name'])
    names += [a.lower() for a in ab] + [a.lower() + 'college' for a in ab]
    if len(ws) >= 2: names.append(''.join(w[0] for w in ws) + kw[:1])
    out = []
    for n in dict.fromkeys(x for x in names if x and 4 <= len(x) <= 40):
        for tld in ('.edu.np', '.com.np', '.com', '.org.np', '.org', '.edu.np'):
            out.append(n + tld)
    return list(dict.fromkeys(out))
def resolves(d):
    try: socket.gethostbyname(d); return True
    except Exception: return False
def get(url, n=60000, t=10):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': UA})
        with urllib.request.urlopen(req, timeout=t, context=ctx) as r:
            return r.geturl(), r.status, r.read(n).decode('utf-8', 'ignore')
    except Exception:
        return None, None, None
def work(p):
    ws = words(p['name'])
    if not ws: return None
    need = ws[:3]
    loc = [w for w in re.findall(r'[a-z]+', (p.get('place') or '').lower() + ' ' + p['district'].lower()) if len(w) > 3]
    for d in cands(p):
        if not resolves(d): continue
        for pre in ('https://', 'http://'):
            u, st, t = get(pre + d)
            if t: break
        if not t or st != 200: continue
        mt = re.search(r'<title[^>]*>(.*?)</title>', t, re.S | re.I); title = H.unescape(mt.group(1)).strip() if mt else ''
        txt = re.sub(r'[^a-z ]', ' ', H.unescape(re.sub(r'<script.*?</script>|<style.*?</style>|<[^>]+>', ' ', t, flags=re.S)).lower())
        low = re.sub(r'[^a-z ]', ' ', title.lower())
        if not all(w in low for w in need): continue
        kw = kind_word(p['name'])
        if kw and kw not in low and kw not in txt[:4000]: continue
        if not any(l in txt for l in loc): continue
        if any(b in txt[:3000] for b in ('domain is for sale', 'buy this domain', 'parked free', 'godaddy', 'under construction')) and len(txt) < 1500: continue
        return {'id': p['id'], 'name': p['name'], 'district': p['district'], 'domain': d, 'final': u, 'title': title[:120], 'loc_ok': any(l in txt for l in loc)}
    return None
if __name__ == '__main__':
    P = [p for p in pw.payload()['providers'] if not p.get('website')]
    P = [p for p in P if not (p['id'].startswith('p-ct37') and 'secondary school' in p['name'].lower())]
    lim = int(sys.argv[1]) if len(sys.argv) > 1 else len(P)
    P = P[:lim]
    print(len(P), 'providers', flush=True)
    with ThreadPoolExecutor(24) as ex: res = list(ex.map(work, P))
    hits = [r for r in res if r]
    json.dump(hits, open('/tmp/w/w39_sites.json', 'w'), indent=1, ensure_ascii=False)
    print(len(hits), 'hits of', len(P))
