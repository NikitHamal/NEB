"""Audit provider websites: DNS/HTTP liveness plus a content check that the page text names the provider.
Usage: python3 backend_python/tools/pathways/audit_sites.py  (writes /tmp/site_audit.json)
"""
import json, re, ssl, sys, html, urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from api import pathways as P  # noqa: E402
STOP = {'multiple', 'campus', 'college', 'tu', 'tribhuvan', 'university', 'shree', 'sri', 'shri', 'school', 'institute', 'technical',
        'polytechnic', 'ctevt', 'secondary', 'higher', 'the', 'and', 'for', 'sciences', 'science', 'nursing', 'education', 'academy',
        'international', 'community', 'public', 'private', 'medical', 'health', 'management', 'engineering', 'technology', 'hospital'}
ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
def fetch(u):
    for _ in range(2):
        try:
            r = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'}), timeout=15, context=ctx)
            t = r.read(250000).decode('utf8', 'ignore')
            return r.status, t
        except urllib.error.HTTPError as e:
            return e.code, ''
        except Exception as e:
            err = type(e).__name__
    return err, ''
def toks(name):
    s = re.sub(r'\(.*?\)', ' ', name.lower())
    return [t for t in re.findall(r'[a-z]+', s) if t not in STOP and len(t) > 3]
def audit(p):
    st, t = fetch(p['website'])
    t = re.sub(r'<script.*?</script>|<style.*?</style>', ' ', t, flags=re.S)
    text = html.unescape(re.sub(r'<[^>]+>', ' ', t)).lower()
    tk = toks(p['name'])
    hit = [k for k in tk if k in text]
    return {'id': p['id'], 'name': p['name'], 'site': p['website'], 'status': st, 'tokens': tk, 'hit': hit, 'chars': len(text)}
if __name__ == '__main__':
    d = P.payload()
    prov = [p for p in d['providers'] if p.get('website')]
    with ThreadPoolExecutor(16) as ex:
        res = list(ex.map(audit, prov))
    Path('/tmp/site_audit.json').write_text(json.dumps(res, ensure_ascii=False))
    live = [r for r in res if isinstance(r['status'], int) and r['status'] < 400]
    miss = [r for r in live if r['tokens'] and not r['hit'] and r['chars'] > 200]
    print(len(res), 'checked,', len(live), 'live,', len(miss), 'live pages that never name the provider')
    for r in miss:
        print(r['id'], '|', r['name'][:50], '|', r['site'], '|', r['tokens'])
