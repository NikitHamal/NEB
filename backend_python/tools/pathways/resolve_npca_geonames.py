"""Wave 27: second district resolver for NPCA campuses (address is a town or a tole, not a local level).

Source: GeoNames Nepal dump (download.geonames.org/export/dump/NP.zip + admin2Codes.txt): place names with their district.
Precision of a bare name match is only about 80 percent (names repeat and GeoNames is incomplete), so a district is accepted only when
(a) the address words match places in at most 4 districts, (b) the campus has a live website, and (c) the site text names exactly one
of those districts and at most 3 districts in all. Run: python3 resolve_npca_geonames.py  (writes npca_district_map2.json)
"""
import collections
import concurrent.futures as cf
import io
import json
import re
import ssl
import urllib.request
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
DIST = ("Achham Arghakhanchi Baglung Baitadi Bajhang Bajura Banke Bara Bardiya Bhaktapur Bhojpur Chitwan Dadeldhura Dailekh Dang "
        "Darchula Dhading Dhankuta Dhanusha Dolakha Dolpa Doti Gorkha Gulmi Humla Ilam Jajarkot Jhapa Jumla Kailali Kalikot Kanchanpur "
        "Kapilvastu Kaski Kathmandu Kavrepalanchok Khotang Lalitpur Lamjung Mahottari Makwanpur Manang Morang Mugu Mustang Myagdi "
        "Nawalparasi Nuwakot Okhaldhunga Palpa Panchthar Parbat Parsa Pyuthan Ramechhap Rasuwa Rautahat Rolpa Rukum Rupandehi Salyan "
        "Sankhuwasabha Saptari Sarlahi Sindhuli Sindhupalchok Siraha Solukhumbu Sunsari Surkhet Syangja Tanahu Taplejung Terhathum Udayapur").split()
FIX = {'Tanahun': 'Tanahu'}
STOP = {'bazar', 'bazaar', 'chowk', 'tole', 'municipality', 'ward', 'no', 'rural', 'near', 'road', 'marg', 'sadak', 'campus', 'official', 'address'}
ctx = ssl._create_unverified_context()


def get(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'}), timeout=120, context=ctx).read()


def build_index():
    adm = {}
    for line in get('https://download.geonames.org/export/dump/admin2Codes.txt').decode('utf-8').splitlines():
        p = line.split('\t')
        if p[0].startswith('NP.'):
            adm[p[0]] = p[2]
    z = zipfile.ZipFile(io.BytesIO(get('https://download.geonames.org/export/dump/NP.zip')))
    idx = collections.defaultdict(set)
    for line in z.read('NP.txt').decode('utf-8').splitlines():
        p = line.split('\t')
        d = adm.get('NP.%s.%s' % (p[10], p[11]))
        if p[6] in ('P', 'A') and d:
            for nm in {p[2]} | set(p[3].split(',')):
                k = re.sub(r'[^a-z]', '', nm.lower())
                if len(k) >= 4:
                    idx[k].add(FIX.get(d, d))
    return idx


def segs(addr):
    out = []
    for x in re.split(r'[,;/()]', re.sub(r'[-\d]+', ' ', addr)):
        w = [t for t in re.findall(r'[A-Za-z]+', x) if t.lower() not in STOP]
        if w:
            out.append(''.join(w).lower())
            if len(w) > 1:
                out.append(w[0].lower())
    return out


def page(u):
    try:
        t = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'}), timeout=12, context=ctx).read(300000)
        return re.sub(r'<[^>]+>', ' ', t.decode('utf-8', 'ignore')).lower()
    except Exception:
        return ''


def main():
    idx = build_index()
    rows = json.loads((HERE / 'npca_campuses.json').read_text(encoding='utf-8'))
    done = {int(k) for k in json.loads((HERE / 'npca_district_map.json').read_text(encoding='utf-8'))}
    todo = [r for r in rows if not r['district'] and r['npca_id'] not in done and r['routes']
            and r.get('web') and isinstance(r.get('live'), int) and r['live'] < 400]

    def work(r):
        cand = set()
        seg = ''
        for s in segs(r['addr']):
            if idx.get(s):
                cand |= idx[s]
                seg = seg or s
        if not cand or len(cand) > 4:
            return None
        t = page(r['web'])
        inpage = [d for d in DIST if d.lower() in t]
        hit = [c for c in cand if c.split()[0].lower() in t]
        if len(hit) == 1 and len(inpage) <= 3:
            return r['npca_id'], {'district': hit[0], 'candidates': sorted(cand), 'site_names': inpage}
    out = {}
    with cf.ThreadPoolExecutor(12) as ex:
        for res in ex.map(work, todo):
            if res:
                out[res[0]] = res[1]
    # Nawalparasi is split in two districts in the dataset; leave those out
    out = {k: v for k, v in out.items() if v['district'] != 'Nawalparasi'}
    (HERE / 'npca_district_map2.json').write_text(json.dumps(out, indent=0), encoding='utf-8')
    print(len(out))


if __name__ == '__main__':
    main()
