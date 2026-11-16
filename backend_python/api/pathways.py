"""Pathways: the study and career dataset shared by the web page and the Android app.

The JSON lives in `api/data/pathways/` (routes_*.json, careers.json, places.json). It is merged once per process
and served as one payload with an ETag. Money is NPR, monthly for salaries and total programme cost for fees; all
figures are indicative ranges reviewed in `REVIEWED`, and every screen says so.
"""
import hashlib
import json
from functools import lru_cache
from pathlib import Path

DATA = Path(__file__).resolve().parent / 'data' / 'pathways'
REVIEWED = '2026-11'


def _load(name):
    with open(DATA / name, encoding='utf-8') as fh:
        return json.load(fh)


@lru_cache(maxsize=1)
def payload():
    a, b, c = _load('routes_a.json'), _load('routes_b.json'), _load('routes_c.json')
    places, extra = _load('places.json'), _load('extra_places.json')
    wave3, wave4, wave4_places = _load('wave3.json'), _load('wave4.json'), _load('wave4_places.json')
    wave5, wave5_places = _load('wave5.json'), _load('wave5_places.json')
    routes = (
        a['routes'] + b['routes'] + c['routes'] + _load('routes_d.json')['routes']
        + wave3['routes'] + wave4['routes'] + wave5['routes']
    )
    by_id = {r['id']: r for r in routes}
    for src in (extra, wave3, wave4, wave4_places, wave5, wave5_places):
        for rid, more in src.get('where_add', {}).items():
            by_id[rid]['where'] = list(by_id[rid].get('where') or []) + more
        for rid, more in src.get('careers_add', {}).items():
            by_id[rid]['careers'] = list(by_id[rid].get('careers') or []) + more
        for rid, more in src.get('next_add', {}).items():
            by_id[rid]['next'] = list(by_id[rid].get('next') or []) + more
    for r in routes:
        for k in ('where', 'careers', 'next'):
            r[k] = list(dict.fromkeys(r.get(k) or []))
    abroad = places['abroad'] + extra['abroad'] + wave3['abroad'] + wave4_places['abroad'] + wave5_places['abroad']
    abroad_by_id = {x['id']: x for x in abroad}
    for src in (wave4_places, wave5_places):
        for aid, more in src.get('abroad_scholarships_add', {}).items():
            abroad_by_id[aid]['scholarships'] = list(dict.fromkeys(list(abroad_by_id[aid].get('scholarships') or []) + more))
    careers = (
        _load('careers.json')['careers'] + _load('extra_careers.json')['careers']
        + wave3['careers'] + wave4['careers'] + wave5['careers']
    )
    providers = (
        places['providers'] + extra['providers'] + wave3['providers']
        + wave4_places['providers'] + wave5_places['providers']
    )
    scholarships = (
        places['scholarships'] + extra['scholarships'] + wave3['scholarships']
        + wave4_places['scholarships'] + wave5_places['scholarships']
    )
    govt_file = _load('govt.json')
    govt = govt_file['govt']
    guides = _load('guides.json')['guides'] if (DATA / 'guides.json').exists() else []
    w6c, w6p, w6g = _load('wave6_careers.json'), _load('wave6_places.json'), _load('wave6_govt.json')
    scholarships = scholarships + w6p['scholarships_add']
    for pool, extras in (
        (careers, w6c['career_extra']), (providers, w6p['provider_extra']), (scholarships, w6p['scholarship_extra']), (abroad, w6p['abroad_extra']),
    ):
        by = {x['id']: x for x in pool}
        for xid, more in extras.items():
            by[xid].update(more)
    abroad_by = {a['id']: a for a in abroad}
    for sc in scholarships:
        cid = sc.get('country')
        if cid and sc['id'] not in abroad_by[cid].setdefault('scholarships', []):
            abroad_by[cid]['scholarships'].append(sc['id'])
    govt = govt + w6g['govt_add']
    govt_by = {g['id']: g for g in govt}
    for gid, more in w6g['govt_extra'].items():
        more = dict(more)
        if more.pop('quota_on', False):
            more['quota'] = w6g['quota']
        govt_by[gid].update(more)
    for g in govt:
        if g.get('ladder') and g.get('pay'):
            g['note'] = (g.get('note') or '').rstrip() + ' ' + w6g['pay_note']
    guides = guides + w6g['guides']
    route_by = {r['id']: r for r in routes}
    for rid, more in _load('wave6_routes.json')['route_extra'].items():
        route_by[rid].update(more)
    faq_all = _load('faq.json')['faq'] + _load('wave6_faq.json')['faq']
    data = {
        'reviewed': REVIEWED,
        'stages': a['stages'],
        'routes': routes,
        'careers': careers,
        'providers': providers,
        'scholarships': scholarships,
        'abroad': abroad,
        'topics': _load('faq.json')['topics'],
        'faq': faq_all,
        'govt_tracks': govt_file['tracks'],
        'govt': govt,
        'guides': guides,
    }
    body = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    data['etag'] = hashlib.md5(body.encode('utf-8')).hexdigest()[:16]
    return data


def problems(data=None):
    """Broken references, used by the tests so a typo in the JSON fails CI instead of a screen."""
    d = data or payload()
    out = []
    for key in ('routes', 'careers', 'providers', 'scholarships', 'abroad'):
        seen = set()
        for x in d[key]:
            if x['id'] in seen:
                out.append(f"duplicate {key}: {x['id']}")
            seen.add(x['id'])
    ids = {k: {x['id'] for x in d[k]} for k in ('routes', 'careers', 'providers', 'scholarships')}
    stages = {s['id'] for s in d['stages']}
    for r in d['routes']:
        if r['stage'] not in stages:
            out.append(f"{r['id']}: stage {r['stage']}")
        for key, pool in (('careers', 'careers'), ('next', 'routes'), ('where', 'providers')):
            for ref in r.get(key, []):
                if ref not in ids[pool]:
                    out.append(f"{r['id']}.{key}: {ref}")
        if len(r['fee']) != 2 or r['fee'][0] > r['fee'][1]:
            out.append(f"{r['id']}: fee")
    topics = {t['id'] for t in d.get('topics', [])}
    seen_faq = set()
    for f in d.get('faq', []):
        if f['id'] in seen_faq:
            out.append(f"duplicate faq: {f['id']}")
        seen_faq.add(f['id'])
        if f['topic'] not in topics:
            out.append(f"{f['id']}: topic {f['topic']}")
        for ref in f.get('go', []):
            if ref not in ids['routes']:
                out.append(f"{f['id']}.go: {ref}")
    try:
        from .models import NEPAL_DISTRICTS
        valid_districts = set(NEPAL_DISTRICTS)
    except Exception:
        valid_districts = None
    for p in d['providers']:
        if not p.get('district') or (valid_districts and p.get('district') not in valid_districts):
            out.append(f"{p['id']}: district {p.get('district')}")
    for a in d['abroad']:
        for ref in a.get('scholarships', []):
            if ref not in ids['scholarships']:
                out.append(f"{a['id']}: scholarship {ref}")
    ids['careers'] = {c['id'] for c in d['careers']}
    route_where = {r['id']: set(r.get('where') or []) for r in d['routes']}
    for p in d['providers']:
        for rid, fee in (p.get('fees') or {}).items():
            if rid not in route_where or p['id'] not in route_where[rid] or len(fee) != 2 or fee[0] > fee[1]:
                out.append(f"{p['id']}: fees {rid}")
    for r in d['routes']:
        if r.get('exam_id') and r['exam_id'] not in {g['id'] for g in d.get('govt', [])}:
            out.append(f"{r['id']}: exam_id {r['exam_id']}")
    scholarship_ids = ids['scholarships']
    abroad_ids = {a['id'] for a in d['abroad']}
    govt_ids = {g['id'] for g in d.get('govt', [])}
    for s in d['scholarships']:
        if s.get('country') and s['country'] not in abroad_ids:
            out.append(f"{s['id']}: country {s['country']}")
        if s.get('open') and (len(s['open']) != 2 or not all(1 <= m <= 12 for m in s['open'])):
            out.append(f"{s['id']}: open months")
    for c in d['careers']:
        ex = (c.get('licence') or {}).get('exam')
        if ex and ex not in govt_ids:
            out.append(f"{c['id']}: licence exam {ex}")
    seen_g = set()
    for g in d.get('govt', []):
        if g['id'] in seen_g:
            out.append(f"duplicate govt: {g['id']}")
        seen_g.add(g['id'])
        if g.get('career') and g['career'] not in ids['careers']:
            out.append(f"{g['id']}: career {g['career']}")
        if g.get('track') not in {t['id'] for t in d.get('govt_tracks', [])}:
            out.append(f"{g['id']}: track {g.get('track')}")
        if g.get('ladder') and not 0 <= g.get('rung', -1) < len(g['ladder']):
            out.append(f"{g['id']}: rung")
        if g.get('quota') and abs(sum(v for _, v in g['quota']) - 100) > 0.01:
            out.append(f"{g['id']}: quota total")
    targets = {'route': ids['routes'], 'career': ids['careers'], 'exam': govt_ids, 'guide': {x['id'] for x in d.get('guides', [])}}
    for gd in d.get('guides', []):
        kind, _, ref = (gd.get('link') or ':').partition(':')
        if gd.get('link') and ref not in targets.get(kind, set()):
            out.append(f"guide {gd['id']}: link {gd['link']}")
        for step in gd['steps']:
            if len(step) != 4 or step[3] not in ('online', 'in person'):
                out.append(f"guide {gd['id']}: step {step[0]}")
    return out
