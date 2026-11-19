"""Wave 27: give a district to NPCA community campuses whose address is only a place name.

Source: palika_district.json (all 753 local levels with their district, from the nepali-canonical dataset that follows the
MoFAGA list). A campus gets a district only when the words of its NPCA address or name contain a local-level name that exists
in exactly one district and is not a common given name (GENERIC). Hits that a human checked and found ambiguous are in BLOCK.
Run: python3 backend_python/tools/pathways/resolve_npca_districts.py  (writes npca_district_map.json)
"""
import collections
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
DIST_FIX = {'Nawalpur': 'Nawalparasi East', 'Nawalparasi': 'Nawalparasi West', 'Tanahun': 'Tanahu', 'Rukum East': 'Rukum East',
            'Rukum West': 'Rukum West', 'Kavre': 'Kavrepalanchok'}
GENERIC = {'multiple', 'campus', 'college', 'shree', 'janta', 'adarsha', 'aadarsh', 'adarsh', 'aadarsha', 'kalika', 'mahendra',
           'janata', 'new', 'bazar', 'chowk', 'school', 'official', 'address', 'offered', 'programs', 'kanchan', 'narayan',
           'mangala', 'chure', 'bhanu', 'bishnu', 'bhimsen', 'saraswati', 'shiva', 'shivalaya', 'buddha', 'jana', 'siddha',
           'gaurishankar', 'gauri', 'kamala', 'krishna', 'surya', 'ganga', 'kali', 'laxmi', 'janaki', 'gandaki', 'rampur'}
# ambiguous or contradicted by the address (a second place in another district), checked by hand
BLOCK = {626: 'Gandaki is a province word', 523: 'Chatara (Sunsari) and Punarbas (Kanchanpur) disagree',
         530: 'Rampur exists in Palpa and Chitwan', 69: 'Baindi not placed in Syangja',
         452: 'Simle not placed in Darchula', 455: 'Mohariya not placed in Tanahu', 354: 'Saga Chowk not placed in Sindhupalchok',
         161: 'Satbise not placed in Lamjung'}


def key(s):
    return re.sub(r'[^a-z]', '', s.lower())


def toks(s):
    w = re.findall(r'[A-Za-z]+', s.lower())
    return [''.join(w[i:i + n]) for n in (3, 2, 1) for i in range(len(w) - n + 1)]


def main():
    g = json.loads((HERE / 'palika_district.json').read_text(encoding='utf-8'))['rows']
    M = collections.defaultdict(set)
    for dist, name, typ in g:
        M[key(name)].add((DIST_FIX.get(dist, dist), name))
    rows = json.loads((HERE / 'npca_campuses.json').read_text(encoding='utf-8'))
    out = {}
    for r in rows:
        if r['district'] or not r['routes'] or r['npca_id'] in BLOCK:
            continue
        hit = collections.OrderedDict()
        for src, s in (('addr', r['addr']), ('name', r['name'])):
            for t in toks(s):
                if t in M and t not in GENERIC and len(t) >= 4:
                    for dist, nm in M[t]:
                        hit[(dist, nm, src)] = 1
        ds = {h[0] for h in hit}
        if len(ds) == 1:
            dist = next(iter(ds))
            names = sorted({h[1] for h in hit})
            out[r['npca_id']] = {'district': dist, 'palika': names, 'from': sorted({h[2] for h in hit})}
    (HERE / 'npca_district_map.json').write_text(json.dumps(out, indent=0), encoding='utf-8')
    print(len(out))


if __name__ == '__main__':
    main()
