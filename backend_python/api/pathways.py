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
    govt_tracks = [dict(t, group=t.get('group', 'gov')) for t in govt_file['tracks']]
    govt_groups = [{'id': 'gov', 'label': 'Government'}]
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
    w7 = _load('wave7.json')
    providers = providers + w7['providers_add']
    for rid, more in w7['where_add'].items():
        route_by[rid]['where'] = list(dict.fromkeys(list(route_by[rid].get('where') or []) + more))
    for pool, extras in ((providers, w7['provider_extra']), (scholarships, w7['scholarship_extra'])):
        by = {x['id']: x for x in pool}
        for xid, more in extras.items():
            by[xid].update(more)
    w8 = _load('wave8.json')
    providers = providers + w8['providers_add']
    for rid, more in w8['where_add'].items():
        route_by[rid]['where'] = list(dict.fromkeys(list(route_by[rid].get('where') or []) + more))
    by_provider = {x['id']: x for x in providers}
    for pid, s8 in w8['seats'].items():
        by_provider[pid]['seats'] = s8['seats']
        by_provider[pid]['note'] = ((by_provider[pid].get('note') or '').rstrip() + ' ' + s8['text']).strip()
    for pool, extras in ((scholarships, w8['scholarship_extra']), (abroad, w8['abroad_extra'])):
        by = {x['id']: x for x in pool}
        for xid, more in extras.items():
            by[xid].update(more)
    w9, w9e, w9g = _load('wave9.json'), _load('wave9_extra.json'), _load('wave9_eng.json')
    providers = providers + w9['providers_add'] + w9g['providers_add']
    by_provider = {x['id']: x for x in providers}
    for src in (w9, w9g):
        for rid, more in src['where_add'].items():
            route_by[rid]['where'] = list(dict.fromkeys(list(route_by[rid].get('where') or []) + more))
        for pid, rs in src['route_seats'].items():
            by_provider[pid]['route_seats'] = rs
        for pid, text in src['note_add'].items():
            by_provider[pid]['note'] = ((by_provider[pid].get('note') or '').rstrip() + ' ' + text).strip()
        for pid, n in src['seats_if_empty'].items():
            if not by_provider[pid].get('seats'):
                by_provider[pid]['seats'] = n
    for pid, fees in w9['fees'].items():
        by_provider[pid]['fees'] = {**(by_provider[pid].get('fees') or {}), **fees}
    for pool, extras in ((scholarships, w9e['scholarship_extra']), (abroad, w9e['abroad_extra'])):
        by = {x['id']: x for x in pool}
        for xid, more in extras.items():
            by[xid].update(more)
    faq_all = _load('faq.json')['faq'] + _load('wave6_faq.json')['faq'] + w7['faq_add'] + w8['faq_add'] + w9e['faq_add']
    if (DATA / 'wave10.json').exists():
        w10 = _load('wave10.json')
        providers = providers + w10['providers_add']
        by_provider = {x['id']: x for x in providers}
        for rid, more in w10['where_add'].items():
            route_by[rid]['where'] = list(dict.fromkeys(list(route_by[rid].get('where') or []) + more))
        for pid, rs in w10['route_seats'].items():
            by_provider[pid]['route_seats'] = {**(by_provider[pid].get('route_seats') or {}), **rs}
        for pid, text in w10['note_add'].items():
            by_provider[pid]['note'] = ((by_provider[pid].get('note') or '').rstrip() + ' ' + text).strip()
        for pid, more in w10['provider_extra'].items():
            by_provider[pid].update(more)
        for pid, fees in w10['fees'].items():
            by_provider[pid]['fees'] = {**(by_provider[pid].get('fees') or {}), **fees}
        for pool, extras in ((scholarships, w10['scholarship_extra']), (abroad, w10['abroad_extra'])):
            by = {x['id']: x for x in pool}
            for xid, more in extras.items():
                by[xid].update(more)
        by_sch = {x['id']: x for x in scholarships}
        for sid, keys in w10['scholarship_drop'].items():
            for k in keys:
                by_sch[sid].pop(k, None)
        for rid, upd in w10['route_update'].items():
            r = route_by[rid]
            if upd.get('name'):
                r['name'] = upd['name']
            if upd.get('about_add'):
                r['about'] = ((r.get('about') or '').rstrip() + ' ' + upd['about_add']).strip()
        faq_all = faq_all + w10['faq_add']
        faq_by = {f['id']: f for f in faq_all}
        for fid, upd in w10['faq_update'].items():
            faq_by[fid].update(upd)
    if (DATA / 'wave11.json').exists():
        w11 = _load('wave11.json')
        providers = providers + w11.get('providers_add', [])
        by_provider = {x['id']: x for x in providers}
        for rid, more in w11['where_add'].items():
            route_by[rid]['where'] = list(dict.fromkeys(list(route_by[rid].get('where') or []) + more))
        for pid, rs in w11['route_seats'].items():
            by_provider[pid]['route_seats'] = {**(by_provider[pid].get('route_seats') or {}), **rs}
        for pid, text in w11['note_add'].items():
            by_provider[pid]['note'] = ((by_provider[pid].get('note') or '').rstrip() + ' ' + text).strip()
        by_sch = {x['id']: x for x in scholarships}
        for sid, more in w11['scholarship_extra'].items():
            by_sch[sid].update(more)
        for gid, upd in w11['govt_update'].items():
            upd = dict(upd)
            add = upd.pop('note_add', None)
            govt_by[gid].update(upd)
            if add:
                govt_by[gid]['note'] = ((govt_by[gid].get('note') or '').rstrip() + ' ' + add).strip()
        for g in govt:
            if g.get('note'):
                g['note'] = g['note'].replace(w6g['pay_note'], w11['pay_note'])
        for pool, extras in ((abroad, w11.get('abroad_extra', {})),):
            by = {x['id']: x for x in pool}
            for xid, more in extras.items():
                by[xid].update(more)
        faq_all = faq_all + w11['faq_add']
    if (DATA / 'wave12.json').exists():
        w12 = _load('wave12.json')
        routes = routes + [{**r, 'where': []} for r in w12.get('routes_add', [])]
        route_by = {r['id']: r for r in routes}
        providers = providers + w12.get('providers_add', [])
        by_provider = {x['id']: x for x in providers}
        for rid, more in w12.get('where_add', {}).items():
            route_by[rid]['where'] = list(dict.fromkeys(list(route_by[rid].get('where') or []) + more))
        for pid, rs in w12.get('route_seats', {}).items():
            by_provider[pid]['route_seats'] = {**(by_provider[pid].get('route_seats') or {}), **rs}
        for src_key in ('note_add', 'provider_notes'):
            for pid, text in w12.get(src_key, {}).items():
                by_provider[pid]['note'] = ((by_provider[pid].get('note') or '').rstrip() + ' ' + text).strip()
        for pid, fees in w12.get('provider_fees', {}).items():
            by_provider[pid]['fees'] = {**(by_provider[pid].get('fees') or {}), **fees}
        scholarships = scholarships + w12.get('scholarships_add', [])
        by_sch = {x['id']: x for x in scholarships}
        for sid, more in w12.get('scholarship_extra', {}).items():
            by_sch[sid].update(more)
        abroad = abroad + w12.get('abroad_add', []) + w12.get('abroad_more', [])
        abroad_by = {a['id']: a for a in abroad}
        for sc in scholarships:
            cid = sc.get('country')
            if cid and sc['id'] not in abroad_by[cid].setdefault('scholarships', []):
                abroad_by[cid]['scholarships'].append(sc['id'])
        for aid, more in w12.get('abroad_update', {}).items():
            abroad_by[aid].update(more)
        guides = guides + w12.get('guides_add', []) + w12.get('guides_more', [])
        careers = careers + w12.get('careers_new', [])
        for rid, more in w12.get('career_links', {}).items():
            route_by[rid]['careers'] = list(dict.fromkeys(list(route_by[rid].get('careers') or []) + more))
        faq_all = faq_all + w12.get('faq_add', []) + w12.get('faq_more', []) + w12.get('faq_extra', []) + w12.get('faq_visa', [])
        for rid, text in w12.get('route_exam', {}).items():
            route_by[rid]['exam'] = text
    if (DATA / 'wave13.json').exists():
        w13 = _load('wave13.json')
        providers = providers + w13['providers_add']
        by_provider = {x['id']: x for x in providers}
        route_by = {r['id']: r for r in routes}
        for rid, more in w13['where_add'].items():
            route_by[rid]['where'] = list(dict.fromkeys(list(route_by[rid].get('where') or []) + more))
        for pid, fees in w13['fees'].items():
            by_provider[pid]['fees'] = {**(by_provider[pid].get('fees') or {}), **fees}
        for pid, text in w13['note_add'].items():
            by_provider[pid]['note'] = ((by_provider[pid].get('note') or '').rstrip() + ' ' + text).strip()
        for old, new in w13['exam_sub']:
            for r in routes:
                if old in (r.get('exam') or ''):
                    r['exam'] = r['exam'].replace(old, new)
        scholarships = scholarships + w13['scholarships_add']
        by_sch = {x['id']: x for x in scholarships}
        for sid, more in w13['scholarship_extra'].items():
            by_sch[sid].update(more)
        abroad_by = {a['id']: a for a in abroad}
        for aid, more in w13['abroad_extra'].items():
            abroad_by[aid].update(more)
        for sc in w13['scholarships_add']:
            cid = sc.get('country')
            if cid and sc['id'] not in abroad_by[cid].setdefault('scholarships', []):
                abroad_by[cid]['scholarships'].append(sc['id'])
        guides = guides + w13['guides_add']
        faq_all = faq_all + w13['faq_add']
        faq_by = {f['id']: f for f in faq_all}
        for fid, upd in w13['faq_update'].items():
            faq_by[fid].update(upd)
    if (DATA / 'wave14.json').exists():
        w14 = _load('wave14.json')
        abroad = abroad + w14['abroad_add']
        abroad_by = {a['id']: a for a in abroad}
        for aid, more in w14['abroad_update'].items():
            abroad_by[aid].update(more)
        for aid, text in w14.get('abroad_note_add', {}).items():
            abroad_by[aid]['note'] = ((abroad_by[aid].get('note') or '').rstrip() + ' ' + text).strip()
        scholarships = scholarships + w14['scholarships_add']
        by_sch = {x['id']: x for x in scholarships}
        for sid, more in w14['scholarship_extra'].items():
            by_sch[sid].update(more)
        for sc in w14['scholarships_add']:
            cid = sc.get('country')
            if cid and sc['id'] not in abroad_by[cid].setdefault('scholarships', []):
                abroad_by[cid]['scholarships'].append(sc['id'])
        by_provider = {x['id']: x for x in providers}
        for pid, more in w14.get('provider_update', {}).items():
            by_provider[pid].update(more)
        for pid, fees in w14.get('fees', {}).items():
            by_provider[pid]['fees'] = {**(by_provider[pid].get('fees') or {}), **fees}
        for pid, text in w14.get('note_add', {}).items():
            by_provider[pid]['note'] = ((by_provider[pid].get('note') or '').rstrip() + ' ' + text).strip()
        by_govt = {g['id']: g for g in govt}
        for gid, text in w14.get('govt_note_add', {}).items():
            by_govt[gid]['note'] = ((by_govt[gid].get('note') or '').rstrip() + ' ' + text).strip()
        guides = guides + w14['guides_add']
        faq_all = faq_all + w14['faq_add']
    if (DATA / 'wave15.json').exists():
        w15 = _load('wave15.json')
        abroad = abroad + w15['abroad_add']
        abroad_by = {a['id']: a for a in abroad}
        for aid, more in w15['abroad_update'].items():
            abroad_by[aid].update(more)
        scholarships = scholarships + w15['scholarships_add']
        by_sch = {x['id']: x for x in scholarships}
        for sid, more in w15['scholarship_extra'].items():
            by_sch[sid].update(more)
        for sc in w15['scholarships_add']:
            cid = sc.get('country')
            if cid and sc['id'] not in abroad_by[cid].setdefault('scholarships', []):
                abroad_by[cid]['scholarships'].append(sc['id'])
        providers = providers + w15['providers_add']
        by_provider = {x['id']: x for x in providers}
        for pid, more in w15['provider_update'].items():
            by_provider[pid].update(more)
        route_by = {r['id']: r for r in routes}
        for rid, more in w15['where_add'].items():
            route_by[rid]['where'] = list(dict.fromkeys(list(route_by[rid].get('where') or []) + more))
        for rid, text in w15['route_about_add'].items():
            route_by[rid]['about'] = ((route_by[rid].get('about') or '').rstrip() + ' ' + text).strip()
        govt = govt + w15['govt_add']
        by_govt = {g['id']: g for g in govt}
        for gid, text in w15['govt_note_add'].items():
            by_govt[gid]['note'] = ((by_govt[gid].get('note') or '').rstrip() + ' ' + text).strip()
        faq_all = faq_all + w15['faq_add']
    if (DATA / 'wave17.json').exists():
        w17 = _load('wave17.json')
        govt_groups = w17['govt_groups']
        govt_tracks = govt_tracks + w17['govt_tracks_add']
        govt = govt + w17['govt_add']
        for rid, eid in w17['route_exam'].items():
            for r in routes:
                if r['id'] == rid and not r.get('exam_id'):
                    r['exam_id'] = eid
    if (DATA / 'wave16.json').exists():
        w16 = _load('wave16.json')
        abroad = abroad + w16['abroad_add']
        abroad_by = {a['id']: a for a in abroad}
        for aid, more in w16['abroad_update'].items():
            abroad_by[aid].update(more)
        scholarships = scholarships + w16['scholarships_add']
        by_sch = {x['id']: x for x in scholarships}
        for sid, more in w16['scholarship_extra'].items():
            by_sch[sid].update(more)
        for sc in w16['scholarships_add']:
            cid = sc.get('country')
            if cid and sc['id'] not in abroad_by[cid].setdefault('scholarships', []):
                abroad_by[cid]['scholarships'].append(sc['id'])
        for aid, text in w16['abroad_note_add'].items():
            abroad_by[aid]['note'] = ((abroad_by[aid].get('note') or '').rstrip() + ' ' + text).strip()
        guides = guides + w16['guides_add']
        providers = providers + w16['providers_add']
        by_provider = {x['id']: x for x in providers}
        route_by = {r['id']: r for r in routes}
        for rid, more in w16['where_add'].items():
            route_by[rid]['where'] = list(dict.fromkeys(list(route_by[rid].get('where') or []) + more))
        for pid, fees in w16['fees'].items():
            by_provider[pid]['fees'] = {**(by_provider[pid].get('fees') or {}), **fees}
        for pid, text in w16['provider_note_add'].items():
            by_provider[pid]['note'] = ((by_provider[pid].get('note') or '').rstrip() + ' ' + text).strip()
        for rid, text in w16['route_about_add'].items():
            route_by[rid]['about'] = ((route_by[rid].get('about') or '').rstrip() + ' ' + text).strip()
        for rid, pairs in w16['text_swap']['route'].items():
            for old, new in pairs:
                assert old in route_by[rid]['about'], (rid, old)
                route_by[rid]['about'] = route_by[rid]['about'].replace(old, new)
        faq_all = faq_all + w16['faq_add']
        faq_by = {f['id']: f for f in faq_all}
        for fid, pairs in w16['text_swap']['faq'].items():
            for old, new in pairs:
                assert old in faq_by[fid]['a'], (fid, old)
                faq_by[fid]['a'] = faq_by[fid]['a'].replace(old, new)
    if (DATA / 'wave18.json').exists():
        w18 = _load('wave18.json')
        scholarships = scholarships + w18['scholarships_add']
        abroad_by = {a['id']: a for a in abroad}
        for sc in w18['scholarships_add']:
            cid = sc.get('country')
            if cid and sc['id'] not in abroad_by[cid].setdefault('scholarships', []):
                abroad_by[cid]['scholarships'].append(sc['id'])
        for aid, more in w18['abroad_update'].items():
            abroad_by[aid].update(more)
        for aid, text in w18['abroad_note_add'].items():
            abroad_by[aid]['note'] = ((abroad_by[aid].get('note') or '').rstrip() + ' ' + text).strip()
        govt_tracks = govt_tracks + w18['govt_tracks_add']
        govt = govt + w18['govt_add']
        career_by = {c['id']: c for c in careers}
        for cid, lic in w18['career_licence'].items():
            career_by[cid]['licence'] = lic
        route_by = {r['id']: r for r in routes}
        for rid, eid in w18['route_exam'].items():
            route_by[rid]['exam_id'] = eid
        for rid, plan in w18['route_plan'].items():
            if not route_by[rid].get('plan'):
                route_by[rid]['plan'] = plan
        guides = guides + w18['guides_add']
        providers = providers + w18['providers_add']
        by_provider = {x['id']: x for x in providers}
        for rid, more in w18['where_add'].items():
            route_by[rid]['where'] = list(dict.fromkeys(list(route_by[rid].get('where') or []) + more))
        for pid, url in w18['provider_websites'].items():
            if not by_provider[pid].get('website'):
                by_provider[pid]['website'] = url
        faq_all = faq_all + w18['faq_add']
    if (DATA / 'wave19.json').exists():
        w19 = _load('wave19.json')
        providers = providers + w19['providers_add']
        by_provider = {x['id']: x for x in providers}
        route_by = {r['id']: r for r in routes}
        for rid, more in w19['where_add'].items():
            route_by[rid]['where'] = list(dict.fromkeys(list(route_by[rid].get('where') or []) + more))
        for pid, rs in w19['route_seats'].items():
            by_provider[pid]['route_seats'] = {**(by_provider[pid].get('route_seats') or {}), **rs}
        for pid, fees in w19.get('fees', {}).items():
            by_provider[pid]['fees'] = {**(by_provider[pid].get('fees') or {}), **fees}
        for pid, text in w19['provider_note_add'].items():
            by_provider[pid]['note'] = ((by_provider[pid].get('note') or '').rstrip() + ' ' + text).strip()
        for pid, url in w19['provider_websites'].items():
            if not by_provider[pid].get('website'):
                by_provider[pid]['website'] = url
        govt = govt + w19['govt_add']
        for rid, eid in w19['route_exam'].items():
            if not route_by[rid].get('exam_id'):
                route_by[rid]['exam_id'] = eid
        career_by = {c['id']: c for c in careers}
        for cid, lic in w19['career_licence'].items():
            career_by[cid]['licence'] = lic
        guides = guides + w19['guides_add']
        scholarships = scholarships + w19['scholarships_add']
        abroad_by = {a['id']: a for a in abroad}
        for sc in w19['scholarships_add']:
            cid = sc.get('country')
            if cid and sc['id'] not in abroad_by[cid].setdefault('scholarships', []):
                abroad_by[cid]['scholarships'].append(sc['id'])
        for aid, text in w19['abroad_note_add'].items():
            abroad_by[aid]['note'] = ((abroad_by[aid].get('note') or '').rstrip() + ' ' + text).strip()
        faq_all = faq_all + w19['faq_add']
    if (DATA / 'wave20.json').exists():
        w20 = _load('wave20.json')
        govt = govt + w20['govt_add']
        route_by = {r['id']: r for r in routes}
        for rid, eid in w20['route_exam'].items():
            route_by[rid]['exam_id'] = eid
        guides = guides + w20['guides_add']
        providers = providers + w20['providers_add']
        by_provider = {x['id']: x for x in providers}
        for rid, more in w20['where_add'].items():
            route_by[rid]['where'] = list(dict.fromkeys(list(route_by[rid].get('where') or []) + more))
        for pid, rs in w20['route_seats'].items():
            by_provider[pid]['route_seats'] = {**(by_provider[pid].get('route_seats') or {}), **rs}
        for pid, fees in w20.get('fees', {}).items():
            by_provider[pid]['fees'] = {**(by_provider[pid].get('fees') or {}), **fees}
        for pid, text in w20.get('provider_note_add', {}).items():
            by_provider[pid]['note'] = ((by_provider[pid].get('note') or '').rstrip() + ' ' + text).strip()
        for pid, url in w20['provider_websites'].items():
            if not by_provider[pid].get('website'):
                by_provider[pid]['website'] = url
        by_sch = {x['id']: x for x in scholarships}
        for sid, more in w20['scholarship_extra'].items():
            by_sch[sid].update(more)
        faq_all = faq_all + w20['faq_add']
    if (DATA / 'visa.json').exists():
        vj = _load('visa.json')
        for a_ in abroad:
            a_['visa'] = vj['visa'].get(a_['id'], vj['default'])
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
        'govt_tracks': govt_tracks,
        'govt_groups': govt_groups,
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
    for p in d['providers']:
        for rid, n in (p.get('route_seats') or {}).items():
            if rid not in route_where or p['id'] not in route_where[rid] or not isinstance(n, int) or n <= 0:
                out.append(f"{p['id']}: route_seats {rid}")
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
