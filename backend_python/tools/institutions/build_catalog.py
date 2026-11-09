"""Build api/data/institutions.json.gz, the catalogue of Nepal's schools, colleges and universities.

Sources (all open data, attribution kept in INSTITUTIONS_STATUS.md):
  OpenStreetMap  amenity=school|college|university inside Nepal (ODbL), via Overpass
  Wikidata       educational institutions in Nepal: official website, inception year
  OSM districts  admin_level=6 polygons, used to place every point in a district
  curated.json   hand checked official sites for the best known institutions

Run:  python3 tools/institutions/build_catalog.py [--refresh] [--no-web-check]
Raw downloads are cached in $INST_RAW (default /tmp/inst_raw); the website checks in web_checks.json.
"""
import gzip
import json
import math
import os
import re
import sys
import time
import unicodedata
import urllib.request
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE.parent.parent / 'api' / 'data' / 'institutions.json.gz'
RAW = Path(os.environ.get('INST_RAW', '/tmp/inst_raw'))
RAW.mkdir(parents=True, exist_ok=True)
UA = 'NEBiansCatalogBuilder/1.0 (https://nebians.consica.com.np)'
OVERPASS = 'https://overpass-api.de/api/interpreter'
Q_AREA = '[out:json][timeout:240];area["ISO3166-1"="NP"][admin_level=2]->.a;'
Q_SCHOOLS = Q_AREA + '(nwr["amenity"~"^(school|college|university)$"]["name"](area.a););out center tags qt;'
Q_DISTRICTS = Q_AREA + 'rel(area.a)["boundary"="administrative"]["admin_level"="6"];out geom qt;'
Q_WIKIDATA = """SELECT ?i ?iLabel ?web ?inc ?locLabel ?coord WHERE {
  ?i wdt:P17 wd:Q837 . ?i wdt:P31/wdt:P279* ?type .
  VALUES ?type { wd:Q3918 wd:Q2385804 wd:Q3914 wd:Q23002054 wd:Q875538 wd:Q902104 wd:Q9826 wd:Q15936437 }
  OPTIONAL { ?i wdt:P856 ?web } OPTIONAL { ?i wdt:P571 ?inc }
  OPTIONAL { ?i wdt:P131 ?loc } OPTIONAL { ?i wdt:P625 ?coord }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en,ne". } }"""

PROVINCES = {
    '1': 'Bhojpur Dhankuta Ilam Jhapa Khotang Morang Okhaldhunga Panchthar Sankhuwasabha Solukhumbu Sunsari Taplejung Terhathum Udayapur',
    '2': 'Bara Dhanusha Mahottari Parsa Rautahat Saptari Sarlahi Siraha',
    '3': 'Bhaktapur Chitwan Dhading Dolakha Kathmandu Kavrepalanchok Lalitpur Makwanpur Nuwakot Ramechhap Rasuwa Sindhuli Sindhupalchok',
    '4': 'Baglung Gorkha Kaski Lamjung Manang Mustang Myagdi Nawalparasi-East Parbat Syangja Tanahu',
    '5': 'Arghakhanchi Banke Bardiya Dang Gulmi Kapilvastu Palpa Pyuthan Rolpa Rukum-East Nawalparasi-West Rupandehi',
    '6': 'Dailekh Dolpa Humla Jajarkot Jumla Kalikot Mugu Salyan Surkhet Rukum-West',
    '7': 'Achham Baitadi Bajhang Bajura Dadeldhura Darchula Doti Kailali Kanchanpur',
}
DISTRICT_PROVINCE = {d.replace('-', ' '): p for p, s in PROVINCES.items() for d in s.split()}
ALIASES = {'Eastern Rukum': 'Rukum East', 'Western Rukum District': 'Rukum West', 'Nawalparasi W': 'Nawalparasi West',
           'Nawalpur District': 'Nawalparasi East', 'Sindhupalchowk': 'Sindhupalchok', 'Tanahun': 'Tanahu',
           'Tehrathum': 'Terhathum', 'Darchula District (Nepal)': 'Darchula', 'Ilam District': 'Ilam',
           'Kanchanpur District': 'Kanchanpur'}
GENERIC = {'school', 'college', 'campus', 'university', 'high school', 'primary school', 'secondary school',
           'boarding school', 'english school', 'public school', 'unknown', 'no name', 'noname'}
DEV = re.compile(r'[\u0900-\u097F]')
LAT = re.compile(r'[A-Za-z]')


def fetch(name, url=None, data=None, headers=None, refresh=False):
    path = RAW / name
    if path.exists() and not refresh and path.stat().st_size > 1000:
        return json.loads(path.read_text())
    for attempt in range(5):
        req = urllib.request.Request(url, data=data, headers={'User-Agent': UA, **(headers or {})})
        try:
            body = urllib.request.urlopen(req, timeout=300).read()
            parsed = json.loads(body)
            path.write_bytes(body)
            return parsed
        except Exception as exc:
            print('retry', name, exc)
            time.sleep(10 * (attempt + 1))
    raise SystemExit('could not fetch ' + name)


def overpass(name, query, refresh):
    return fetch(name, OVERPASS, urllib.parse.urlencode({'data': query}).encode(), refresh=refresh)


def norm(name):
    s = unicodedata.normalize('NFKD', name.lower())
    s = re.sub(r'\b(shree|shri|sri|sree|the|st)\b', '', s)
    s = re.sub(r'[^a-z\u0900-\u097F0-9]', '', s)
    return s


def tidy(name):
    name = re.sub(r'\s+', ' ', (name or '').replace('_', ' ')).strip(' -,.;:')
    if LAT.search(name) and (name.islower() or name.isupper()) and len(name) > 4:
        name = name.title()
    return name


def kind_of(name, amenity):
    n = name.lower()
    if amenity == 'university' or re.search(r'university|विश्वविद्यालय', n):
        return 'university'
    if re.search(r'campus|क्याम्पस|college|collage|कलेज|महाविद्यालय|vidyapeeth|polytechnic|\+2|plus two|\bplus\b', n):
        return 'college'
    if re.search(r'school|vidyalaya|vidhyalaya|bidhyalaya|vidya mandir|academy|montessori|विद्यालय|बिद्यालय|स्कूल|higher secondary', n):
        return 'school'
    if re.search(r'institute|training|technical|ctevt|तालिम|प्रतिष्ठान|research|centre|center', n):
        return 'institute'
    return amenity if amenity in ('college', 'school') else 'institute'


def clean_url(u):
    u = (u or '').strip().split(';')[0].strip()
    if not u or ' ' in u:
        return ''
    if not re.match(r'^https?://', u, re.I):
        u = 'https://' + u
    p = urllib.parse.urlparse(u)
    if not p.netloc or '.' not in p.netloc or p.netloc.lower().startswith('l.facebook'):
        return ''
    return u.rstrip('/')


def load_districts(refresh):
    out = []
    for rel in overpass('districts.json', Q_DISTRICTS, refresh)['elements']:
        t = rel['tags']
        raw = t.get('name:en') or t.get('name')
        name = ALIASES.get(raw, raw)
        name = re.sub(r' District$', '', name)
        if name not in DISTRICT_PROVINCE:
            print('UNMAPPED DISTRICT', raw)
            continue
        segs = []
        for m in rel.get('members', []):
            g = m.get('geometry')
            if m['type'] == 'way' and g and len(g) > 1:
                pts = np.array([[p['lon'], p['lat']] for p in g])
                segs.append(np.hstack([pts[:-1], pts[1:]]))
        e = np.vstack(segs)
        out.append((name, e, (e[:, [0, 2]].min(), e[:, [1, 3]].min(), e[:, [0, 2]].max(), e[:, [1, 3]].max())))
    return out


def locate(districts, lat, lon):
    hits = []
    for name, e, (x0, y0, x1, y1) in districts:
        if not (x0 <= lon <= x1 and y0 <= lat <= y1):
            continue
        a = (e[:, 1] > lat) != (e[:, 3] > lat)
        xs = e[:, 0] + (lat - e[:, 1]) * (e[:, 2] - e[:, 0]) / np.where(e[:, 3] == e[:, 1], 1, e[:, 3] - e[:, 1])
        if int(np.count_nonzero(a & (lon < xs))) % 2 == 1:
            return name
        hits.append(name)
    return ''


def dist_km(a, b):
    return math.hypot((a[0] - b[0]) * 111, (a[1] - b[1]) * 111 * math.cos(math.radians(a[0])))


def main():
    refresh = '--refresh' in sys.argv
    districts = load_districts(refresh)
    recs = []
    for e in overpass('osm_schools.json', Q_SCHOOLS, refresh)['elements']:
        t = e['tags']
        lat, lon = (e.get('lat'), e.get('lon')) if e['type'] == 'node' else (e['center']['lat'], e['center']['lon'])
        ne = tidy(t.get('name:ne') or (t['name'] if DEV.search(t['name']) else ''))
        en = tidy(t.get('name:en') or (t['name'] if LAT.search(t['name']) and not DEV.search(t['name']) else ''))
        name = en or ne
        if len(name) < 4 or name.lower() in GENERIC or re.fullmatch(r'[\d\W]+', name):
            continue
        place = ''
        for k in ('addr:city', 'addr:municipality', 'addr:place', 'location', 'addr:suburb', 'addr:hamlet'):
            if t.get(k):
                place = tidy(t[k])[:80]
                break
        recs.append({'name': name, 'name_ne': ne if en else '', 'kind': kind_of(name + ' ' + ne, t['amenity']),
                     'place': place, 'website': clean_url(t.get('website') or t.get('contact:website') or t.get('url')),
                     'phone': (t.get('phone') or t.get('contact:phone') or '').split(';')[0].strip()[:30],
                     'lat': round(lat, 5), 'lon': round(lon, 5), 'est': '', 'source': 'osm', 'osm': e['id']})
    print('osm records', len(recs))

    by_norm = {}
    for r in recs:
        by_norm.setdefault(norm(r['name']), []).append(r)

    def merge_or_add(rec):
        cands = by_norm.get(norm(rec['name']), [])
        best = None
        for c in cands:
            if rec['lat'] is None or c['lat'] is None:
                d = 0 if len(cands) == 1 else 99
            else:
                d = dist_km((rec['lat'], rec['lon']), (c['lat'], c['lon']))
            if d < 6 and (best is None or d < best[0]):
                best = (d, c)
        if best:
            c = best[1]
            c['website'] = c['website'] or rec['website']
            c['est'] = c['est'] or rec['est']
            c['source'] += '+' + rec['source']
            return c
        recs.append(rec)
        by_norm.setdefault(norm(rec['name']), []).append(rec)
        return rec

    wd = fetch('wikidata.json', 'https://query.wikidata.org/sparql?format=json&query=' + urllib.parse.quote(Q_WIKIDATA),
               headers={'Accept': 'application/sparql-results+json'}, refresh=refresh)['results']['bindings']
    items = {}
    for b in wd:
        it = items.setdefault(b['i']['value'], {'web': '', 'inc': '', 'loc': '', 'coord': None, 'label': ''})
        label = b.get('iLabel', {}).get('value', '')
        if label and not re.fullmatch(r'Q\d+', label):
            it['label'] = label
        it['web'] = it['web'] or clean_url(b.get('web', {}).get('value'))
        it['inc'] = it['inc'] or b.get('inc', {}).get('value', '')[:4].lstrip('-')
        it['loc'] = it['loc'] or b.get('locLabel', {}).get('value', '')
        m = re.match(r'Point\(([-\d.]+) ([-\d.]+)\)', b.get('coord', {}).get('value', ''))
        if m and not it['coord']:
            it['coord'] = (float(m.group(2)), float(m.group(1)))
    added = 0
    for it in items.values():
        if len(it['label']) < 4:
            continue
        lat, lon = it['coord'] or (None, None)
        before = len(recs)
        merge_or_add({'name': tidy(it['label']), 'name_ne': '', 'kind': kind_of(it['label'], ''), 'place': '',
                      'website': it['web'], 'phone': '', 'lat': lat, 'lon': lon, 'est': it['inc'],
                      'source': 'wikidata', 'osm': 0, 'loc': it['loc']})
        added += len(recs) - before
    print('wikidata items', len(items), 'new', added)

    extra = json.loads((HERE.parent.parent / 'api' / 'data' / 'institution_sites.json').read_text())
    for c in json.loads((HERE / 'curated.json').read_text()) + extra:
        hit = merge_or_add({'name': c['name'], 'name_ne': '', 'kind': c['kind'], 'place': c.get('place', ''),
                            'website': clean_url(c['website']), 'phone': c.get('phone', ''), 'lat': c.get('lat'),
                            'lon': c.get('lon'), 'est': c.get('est', ''), 'source': 'curated', 'osm': 0,
                            'loc': c.get('district', '')})
        hit['website'] = clean_url(c['website'])
        hit['kind'] = c['kind']
        hit['keep'] = True

    recs = [r for r in recs if r.get('keep') or r['source'] != 'wikidata' or (
        r['website'] or r.get('loc')) and not re.search(r'research|department|faculty|initiative|laborator|center|centre', r['name'], re.I)]
    for r in recs:
        d = locate(districts, r['lat'], r['lon']) if r['lat'] is not None else ''
        if not d:
            loc = re.sub(r' (District|Municipality|Metropolitan City|Sub-Metropolitan City)$', '', r.get('loc', ''))
            d = ALIASES.get(loc, loc) if ALIASES.get(loc, loc) in DISTRICT_PROVINCE else ''
        r['district'] = d
        r['province'] = DISTRICT_PROVINCE.get(d, '')

    seen = {}
    for r in sorted(recs, key=lambda r: (not r['website'], r['source'] == 'osm', r['name'])):
        key = (norm(r['name']), round(r['lat'], 2) if r['lat'] is not None else r['district'],
               round(r['lon'], 2) if r['lon'] is not None else '')
        if key in seen:
            keep = seen[key]
            keep['website'] = keep['website'] or r['website']
            keep['phone'] = keep['phone'] or r['phone']
            keep['name_ne'] = keep['name_ne'] or r['name_ne']
            continue
        seen[key] = r
    recs = list(seen.values())
    print('after dedupe', len(recs))

    if '--no-web-check' not in sys.argv:
        check_websites(recs)

    slugs = set()
    rows = []
    for r in sorted(recs, key=lambda r: (not r['website'], r['province'] == '', r['name'].lower())):
        base = re.sub(r'[^a-z0-9]+', '-', unicodedata.normalize('NFKD', r['name']).encode('ascii', 'ignore').decode().lower()).strip('-')[:70]
        if len(base) < 3:
            base = 'inst-%s' % (r['osm'] or abs(hash(r['name'])) % 10 ** 7)
        slug = base
        for suffix in (r['district'].lower().replace(' ', '-'), str(r['osm'] or '')):
            if slug in slugs and suffix:
                slug = (base + '-' + suffix)[:90]
        n = 2
        while slug in slugs:
            slug = '%s-%d' % (base[:80], n)
            n += 1
        slugs.add(slug)
        rows.append([slug, r['name'], r['name_ne'], r['kind'], r['district'], r['province'], r['place'], r['website'],
                     r['phone'], r['lat'], r['lon'], r['est'], r['source']])
    cols = ['slug', 'name', 'name_ne', 'kind', 'district', 'province', 'place', 'website', 'phone', 'lat', 'lon', 'est', 'source']
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(OUT, 'wt', encoding='utf-8', compresslevel=9) as fh:
        json.dump({'v': 1, 'cols': cols, 'rows': rows}, fh, ensure_ascii=False, separators=(',', ':'))
    kinds = {}
    for r in rows:
        kinds[r[3]] = kinds.get(r[3], 0) + 1
    print('wrote', OUT, len(rows), kinds, 'with website', sum(1 for r in rows if r[7]),
          'with district', sum(1 for r in rows if r[4]), OUT.stat().st_size // 1024, 'KB')


def check_websites(recs):
    cache_path = RAW / 'web_checks.json'
    cache = json.loads(cache_path.read_text()) if cache_path.exists() else {}
    urls = sorted({r['website'] for r in recs if r['website']} - set(cache))

    def probe(u):
        host = urllib.parse.urlparse(u).netloc.lower()
        if 'facebook.com' in host or 'instagram.com' in host:
            return u, True
        for method in ('HEAD', 'GET'):
            try:
                req = urllib.request.Request(u, method=method, headers={'User-Agent': 'Mozilla/5.0 (compatible; NEBiansBot/1.0)'})
                code = urllib.request.urlopen(req, timeout=12).status
                return u, code < 500
            except urllib.error.HTTPError as exc:
                if exc.code in (401, 403, 405, 406, 429) and method == 'GET':
                    return u, True
                if exc.code in (401, 403, 429):
                    return u, True
            except Exception:
                pass
        return u, False

    print('checking', len(urls), 'websites')
    with ThreadPoolExecutor(24) as pool:
        for u, ok in pool.map(probe, urls):
            cache[u] = ok
    cache_path.write_text(json.dumps(cache))
    dropped = 0
    for r in recs:
        if r['website'] and not cache.get(r['website']):
            r['website'] = ''
            dropped += 1
    print('dropped dead websites', dropped)


if __name__ == '__main__':
    main()
