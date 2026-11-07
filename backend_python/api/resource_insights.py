"""Insights for people who upload to the library (web sheet + Android) and for staff.

`build(resource)` is one resource. `overview(user)` is everything one uploader has in the library plus
their posts. Everything is an aggregate: reach rows only hold keyed hashes, nobody is ever named.
Days are local midnight in settings.TIME_ZONE like the rest of the analytics.
"""
from __future__ import annotations

import statistics
import time
from collections import Counter, defaultdict
from datetime import datetime, timedelta

from django.db.models import Sum

from .models import (Bookmark, Post, PostReach, PushDelivery, Resource, ResourceAlert, ResourceComment,
                     ResourceImpression, ResourceReach)
from .post_insights import (CHANNEL_LABEL, DEVICE_LABEL, DWELL_BUCKETS, OS_LABEL, _change, _day_of, _days,
                            _hour_label, _hour_of, _kpi, _split, _tz)

VERSION = 1
RANGES = (7, 30, 90)
SURFACE_LABEL = {'library': 'Library', 'search': 'Search', 'subject': 'Subject page', 'profile': 'Profile',
                 'share': 'Shared link', 'direct': 'Direct', 'notification': 'Notification', 'related': 'Related',
                 'home': 'Home'}
FIELDS = ('resource_id', 'viewer', 'day', 'first_at', 'dwell_ms', 'surface', 'source', 'device_class', 'os_family',
          'country', 'channel', 'class_level', 'is_member', 'read', 'downloaded', 'shared')
CHUNK = 400


def _chunks(items, n=CHUNK):
    items = list(items)
    for i in range(0, len(items), n):
        yield items[i:i + n]


def _windows(days: int):
    window = _days(days)
    first = datetime.strptime(window[0], '%Y-%m-%d').date()
    prev = [(first - timedelta(days=days - i)).strftime('%Y-%m-%d') for i in range(days)]
    start_ms = int(datetime.strptime(prev[0], '%Y-%m-%d').replace(tzinfo=_tz()).timestamp() * 1000)
    return window, prev, start_ms


def _rows(ids, day_set):
    out = []
    for part in _chunks(ids):
        out.extend(ResourceReach.objects.filter(resource_id__in=part, is_owner=False, day__in=day_set)
                   .values_list(*FIELDS))
    return [dict(zip(FIELDS, r)) for r in out]


def _core(ids: list[str], days: int) -> dict:
    """Numbers shared by one resource and by an uploader's whole shelf."""
    days = days if days in RANGES else 30
    window, prev_window, start_ms = _windows(days)
    cur_set, prev_set = set(window), set(prev_window)
    rows = _rows(ids, cur_set | prev_set)
    cur = [r for r in rows if r['day'] in cur_set]
    prev = [r for r in rows if r['day'] in prev_set]

    imp_rows = []
    for part in _chunks(ids):
        imp_rows.extend(ResourceImpression.objects.filter(resource_id__in=part, day__in=cur_set | prev_set)
                        .values_list('resource_id', 'day', 'count'))
    imp = sum(c for _r, d, c in imp_rows if d in cur_set)
    imp_prev = sum(c for _r, d, c in imp_rows if d in prev_set)

    saves, comments = [], []
    for part in _chunks(ids):
        saves.extend(Bookmark.objects.filter(target_type='resource', target_id__in=part, created_at__gte=start_ms)
                     .values_list('created_at', flat=True))
        comments.extend(ResourceComment.objects.filter(resource_id__in=part, created_at__gte=start_ms)
                        .values_list('created_at', flat=True))
    save_day = Counter(_day_of(t) for t in saves)
    com_day = Counter(_day_of(t) for t in comments)

    def count(rs, flag):
        return sum(1 for r in rs if r[flag])

    uniq = {r['viewer'] for r in cur}
    uniq_prev = {r['viewer'] for r in prev}
    dwell = [r['dwell_ms'] / 1000.0 for r in cur if r['dwell_ms'] > 0]
    dwell_prev = [r['dwell_ms'] / 1000.0 for r in prev if r['dwell_ms'] > 0]
    avg = round(sum(dwell) / len(dwell), 1) if dwell else 0
    avg_prev = round(sum(dwell_prev) / len(dwell_prev), 1) if dwell_prev else 0
    saves_cur = sum(n for d, n in save_day.items() if d in cur_set)
    saves_prev = sum(n for d, n in save_day.items() if d in prev_set)
    com_cur = sum(n for d, n in com_day.items() if d in cur_set)
    com_prev = sum(n for d, n in com_day.items() if d in prev_set)

    v_day, u_day, r_day, d_day = Counter(), defaultdict(set), Counter(), Counter()
    for r in cur:
        v_day[r['day']] += 1
        u_day[r['day']].add(r['viewer'])
        r_day[r['day']] += 1 if r['read'] else 0
        d_day[r['day']] += 1 if r['downloaded'] else 0
    i_day = Counter()
    for _r, d, c in imp_rows:
        i_day[d] += c
    series = [{'date': d, 'views': v_day.get(d, 0), 'unique': len(u_day.get(d, ())), 'reads': r_day.get(d, 0),
               'downloads': d_day.get(d, 0), 'impressions': i_day.get(d, 0), 'saves': save_day.get(d, 0),
               'comments': com_day.get(d, 0)} for d in window]

    hours = Counter(_hour_of(r['first_at']) for r in cur)
    hourly = [hours.get(h, 0) for h in range(24)]
    peak = max(range(24), key=lambda h: hourly[h]) if any(hourly) else None

    seen: dict[str, set] = defaultdict(set)
    for part in _chunks(ids):
        for viewer, day in ResourceReach.objects.filter(resource_id__in=part, is_owner=False,
                                                        viewer__in=list(uniq)[:CHUNK]).values_list('viewer', 'day'):
            seen[viewer].add(day)
    returning = sum(1 for v in uniq if len(seen[v]) > 1)
    members = len({r['viewer'] for r in cur if r['is_member']})

    dwell_buckets = []
    for key, label, lo, hi in DWELL_BUCKETS:
        n = sum(1 for s in dwell if lo <= s < hi)
        dwell_buckets.append({'key': key, 'label': label, 'count': n,
                              'pct': round(n * 100.0 / len(dwell), 1) if dwell else 0})

    views, reads, downs = len(cur), count(cur, 'read'), count(cur, 'downloaded')
    shares = count(cur, 'shared')
    notif = sum(1 for r in cur if r['surface'] == 'notification')
    alerts = list(ResourceAlert.objects.filter(resource_id__in=ids[:CHUNK], state__in=('sent', 'manual')))
    camp_ids = {a.campaign_id for a in alerts if a.campaign_id}
    pushed_clicks = PushDelivery.objects.filter(campaign_id__in=camp_ids).exclude(clicked_at=0).count() if camp_ids else 0

    classes = Counter(r['class_level'] or 'Not set' for r in cur)
    return {
        'version': VERSION, 'days': days, 'range': {'from': window[0], 'to': window[-1]},
        'kpis': {
            'views': _kpi(views, len(prev)), 'uniqueViewers': _kpi(len(uniq), len(uniq_prev)),
            'impressions': _kpi(imp, imp_prev), 'reads': _kpi(reads, count(prev, 'read')),
            'downloads': _kpi(downs, count(prev, 'downloaded')), 'shares': _kpi(shares, count(prev, 'shared')),
            'saves': _kpi(saves_cur, saves_prev), 'comments': _kpi(com_cur, com_prev),
            'avgDwellSec': _kpi(avg, avg_prev),
        },
        'ctr': round(views * 100.0 / imp, 1) if imp else None,
        'readRate': round(reads * 100.0 / views, 1) if views else None,
        'downloadRate': round(downs * 100.0 / views, 1) if views else None,
        'funnel': [
            {'key': 'impressions', 'label': 'Saw it in a list', 'count': imp},
            {'key': 'views', 'label': 'Opened it', 'count': views},
            {'key': 'reads', 'label': 'Read or played it', 'count': reads},
            {'key': 'downloads', 'label': 'Downloaded it', 'count': downs},
        ],
        'series': series, 'hourly': hourly, 'peakHour': peak,
        'peakHourLabel': _hour_label(peak) if peak is not None else '',
        'audience': {'members': members, 'guests': max(0, len(uniq) - members), 'returning': returning,
                     'newViewers': max(0, len(uniq) - returning)},
        'surfaces': _split(Counter(r['surface'] or 'direct' for r in cur), SURFACE_LABEL),
        'channels': _split(Counter(r['channel'] or 'direct' for r in cur if r['source'] == 'web'), CHANNEL_LABEL),
        'devices': _split(Counter(r['device_class'] for r in cur), DEVICE_LABEL),
        'os': _split(Counter(r['os_family'] for r in cur), OS_LABEL),
        'sources': _split(Counter(r['source'] for r in cur), {'web': 'Website', 'app': 'Android app'}),
        'countries': _split(Counter(r['country'] for r in cur if r['country']), None, 6),
        'classes': _split(classes, None, 6),
        'dwell': {'avgSec': avg, 'medianSec': round(statistics.median(dwell), 1) if dwell else 0,
                  'buckets': dwell_buckets, 'samples': len(dwell)},
        'push': {'announced': len(alerts), 'notified': sum(a.audience_size for a in alerts), 'views': notif,
                 'shareOfViews': round(notif * 100.0 / views, 1) if views else None, 'taps': pushed_clicks},
        'hasData': bool(rows or imp_rows),
        '_rows': cur,
    }


def build(resource: Resource, days: int = 30) -> dict:
    d = _core([resource.pk], days)
    cur = d.pop('_rows')
    mine = list(Resource.objects.filter(uploaded_by_id=resource.uploaded_by_id, is_lead=True)
                .values_list('view_count', flat=True)) if resource.uploaded_by_id else []
    median = int(statistics.median(mine)) if mine else 0
    d.update({
        'resourceId': resource.pk, 'title': resource.title[:120], 'subject': resource.subject[:60],
        'gradeLevel': resource.grade_level, 'type': resource.type, 'status': resource.approval_status,
        'addedAt': resource.added_at,
        'ageDays': max(0, int((time.time() * 1000 - resource.added_at) / 86400000)),
        'lifetime': {
            'views': resource.view_count, 'likes': resource.like_count, 'comments': resource.comment_count,
            'downloads': resource.download_count,
            'bookmarks': Bookmark.objects.filter(target_type='resource', target_id=resource.pk).count(),
            'uniqueViewers': ResourceReach.objects.filter(resource=resource, is_owner=False)
                             .values('viewer').distinct().count(),
            'impressions': ResourceImpression.objects.filter(resource=resource).aggregate(n=Sum('count'))['n'] or 0,
        },
        'standing': {
            'rank': sum(1 for v in mine if v > resource.view_count) + 1, 'of': len(mine), 'medianViews': median,
            'vsMedian': _change(resource.view_count, median) if len(mine) > 1 else None,
        },
    })
    d['insights'] = _tips(d, single=True)
    return d


def overview(user, days: int = 30) -> dict:
    """Everything one uploader has in the library, plus their forum posts."""
    res = list(Resource.objects.filter(uploaded_by=user).order_by('-added_at')[:1000])
    ids = [r.pk for r in res]
    d = _core(ids, days) if ids else _core(['-'], days)
    cur = d.pop('_rows')
    per = defaultdict(lambda: {'views': 0, 'viewers': set(), 'reads': 0, 'downloads': 0, 'shares': 0, 'dwell': []})
    for r in cur:
        p = per[r['resource_id']]
        p['views'] += 1
        p['viewers'].add(r['viewer'])
        p['reads'] += 1 if r['read'] else 0
        p['downloads'] += 1 if r['downloaded'] else 0
        p['shares'] += 1 if r['shared'] else 0
        if r['dwell_ms']:
            p['dwell'].append(r['dwell_ms'] / 1000.0)
    window = {x['date'] for x in d['series']}
    imp = Counter()
    for part in _chunks(ids):
        for rid, day, c in ResourceImpression.objects.filter(resource_id__in=part, day__in=window).values_list('resource_id', 'day', 'count'):
            imp[rid] += c
    table = []
    for r in res:
        p = per.get(r.pk)
        views = p['views'] if p else 0
        table.append({
            'id': r.pk, 'title': r.title[:100], 'subject': r.subject[:60], 'gradeLevel': r.grade_level, 'type': r.type,
            'status': r.approval_status, 'addedAt': r.added_at, 'isPaid': r.is_paid,
            'views': views, 'unique': len(p['viewers']) if p else 0, 'reads': p['reads'] if p else 0,
            'downloads': p['downloads'] if p else 0, 'shares': p['shares'] if p else 0,
            'impressions': imp.get(r.pk, 0),
            'avgDwellSec': round(sum(p['dwell']) / len(p['dwell']), 1) if p and p['dwell'] else 0,
            'lifetimeViews': r.view_count, 'lifetimeLikes': r.like_count, 'lifetimeComments': r.comment_count,
            'lifetimeDownloads': r.download_count,
        })
    table.sort(key=lambda x: (-x['views'], -x['lifetimeViews'], -x['addedAt']))
    by_subject = Counter()
    sub_of = {r.pk: (r.subject or 'Other')[:40] for r in res}
    for r in cur:
        by_subject[sub_of.get(r['resource_id'], 'Other')] += 1
    d.update({
        'totals': {
            'resources': len(res), 'live': sum(1 for r in res if r.approval_status == 'approved'),
            'pending': sum(1 for r in res if r.approval_status == 'pending'),
            'views': sum(r.view_count for r in res), 'likes': sum(r.like_count for r in res),
            'comments': sum(r.comment_count for r in res), 'downloads': sum(r.download_count for r in res),
        },
        'resources': table[:40],
        'subjects': _split(by_subject, None, 6),
        'posts': _posts_block(user, d['days']),
    })
    d['insights'] = _tips(d, single=False)
    return d


def _posts_block(user, days: int) -> dict:
    posts = list(Post.objects.filter(user=user).order_by('-created_at')[:300])
    if not posts:
        return {'count': 0, 'views': 0, 'viewsPrev': 0, 'change': None, 'likes': 0, 'replies': 0, 'top': []}
    window, prev_window, _s = _windows(days)
    ids = [p.pk for p in posts]
    per, cur_n, prev_n = Counter(), 0, 0
    cur_set, prev_set = set(window), set(prev_window)
    for part in _chunks(ids):
        for pid, day in PostReach.objects.filter(post_id__in=part, is_owner=False, day__in=cur_set | prev_set).values_list('post_id', 'day'):
            if day in cur_set:
                per[pid] += 1
                cur_n += 1
            else:
                prev_n += 1
    top = sorted(posts, key=lambda p: (-per.get(p.pk, 0), -p.view_count))[:5]
    return {
        'count': len(posts), 'views': cur_n, 'viewsPrev': prev_n, 'change': _change(cur_n, prev_n),
        'likes': sum(p.thumbs_up_count for p in posts), 'replies': sum(p.reply_count for p in posts),
        'top': [{'id': p.pk, 'title': (p.title or 'Untitled')[:90], 'views': per.get(p.pk, 0),
                 'lifetimeViews': p.view_count, 'likes': p.thumbs_up_count, 'replies': p.reply_count} for p in top],
    }


def _tips(d: dict, single: bool) -> list[dict]:
    tips: list[dict] = []
    k = d['kpis']
    what = 'this resource' if single else 'your resources'

    def add(tone, title, body):
        tips.append({'tone': tone, 'title': title, 'body': body})

    if not d['hasData']:
        add('info', 'Nothing tracked yet', 'Opens are counted from now on. Check back after a few students open it.')
        return tips
    ch = k['views']['change']
    if ch is not None and k['views']['prev'] >= 5 and abs(ch) >= 25:
        add('up' if ch > 0 else 'down', f"Views {'up' if ch > 0 else 'down'} {abs(round(ch))}%",
            f"{k['views']['value']} opens in the last {d['days']} days against {k['views']['prev']} before.")
    push = d['push']
    if push['views'] and push['shareOfViews'] is not None and push['shareOfViews'] >= 15:
        add('up', f"{round(push['shareOfViews'])}% of opens came from a notification",
            f"{push['notified']} students were told about {what} when it went live.")
    elif push['notified'] and not push['views']:
        add('info', f"{push['notified']} students were notified", 'No one has opened it from the notification yet.')
    rr = d.get('readRate')
    if rr is not None and k['views']['value'] >= 10:
        add('up' if rr >= 50 else 'down', f'{round(rr)}% went on to read it',
            'Most people who open it use it.' if rr >= 50 else 'A clearer title and cover help people commit to reading.')
    dr = d.get('downloadRate')
    if dr and k['views']['value'] >= 10:
        add('up', f'{round(dr)}% downloaded it', 'Downloads mean students want it offline for exams.')
    dw = d['dwell']
    if dw['samples'] >= 5:
        quick = next((b['pct'] for b in dw['buckets'] if b['key'] == 'under5'), 0)
        if quick >= 50:
            add('down', f'{quick}% left in under 5 seconds', 'Check the title and subject match what is inside.')
    if d['peakHourLabel'] and k['views']['value'] >= 5:
        add('info', f"Most opens come around {d['peakHourLabel']}", 'Upload a little before this time to catch the peak.')
    cl = d.get('classes') or []
    if cl and cl[0]['label'] != 'Not set' and k['views']['value'] >= 8:
        add('info', f"{round(cl[0]['pct'])}% of readers are in {cl[0]['label']}", 'Tag the class level so the right students are notified.')
    if single:
        st = d['standing']
        if st['of'] > 3 and st['vsMedian'] is not None:
            add('up' if st['vsMedian'] >= 0 else 'info', f"#{st['rank']} of your {st['of']} uploads by views",
                f"{'Above' if st['vsMedian'] >= 0 else 'Below'} your median of {st['medianViews']} views.")
    return tips[:6]
