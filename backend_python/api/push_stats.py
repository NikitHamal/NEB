"""Numbers for the admin push history: the overview, one campaign, and when people open pushes.

Everything is an aggregate over `PushCampaign` and `PushDelivery`. Nothing names a person.
Days and hours are local (settings.TIME_ZONE), like the rest of the analytics.
"""
from __future__ import annotations

import time
from collections import Counter, defaultdict

from django.db.models import Count, Sum

from .models import FCMToken, PushCampaign, PushDelivery, Resource, ResourceAlert, ResourceReach, User
from .post_insights import _change, _day_of, _days, _hour_label, _hour_of, _kpi

DAY_MS = 86400000
KIND_LABEL = {'manual': 'Broadcast', 'library': 'Library announcement', 'autopilot': 'Autopilot', 'test': 'Test'}
ERROR_LABEL = {
    'unregistered': 'App was uninstalled or the token expired',
    'sender_id_mismatch': 'Token belongs to another Firebase project',
    'no_credentials': 'Firebase credentials are missing on the server',
    'quota_exceeded': 'Firebase rate limit hit',
    'unavailable': 'Firebase was briefly unavailable',
    'internal': 'Firebase internal error',
    'timeout': 'Firebase did not answer in time',
    'network': 'Network error reaching Firebase',
    'invalid_argument': 'Firebase rejected the message',
    'third_party_auth_error': 'Phone notification service rejected the key',
}
SKIP_LABEL = {
    'autopilot_off': 'Autopilot was off', 'paid': 'Paid resource', 'no_audience': 'Nobody matched class and subject',
    'stale': 'Too old when the round ran', 'gone': 'No longer live',
}
DELAY_BUCKETS = (('5m', 'Within 5 minutes', 5 * 60000), ('1h', 'Within an hour', 3600000),
                 ('6h', 'Within 6 hours', 6 * 3600000), ('24h', 'Within a day', DAY_MS), ('later', 'Later', 10 ** 15))


def _pct(a, b):
    return round(a * 100.0 / b, 1) if b else None


def error_rows(counter) -> list[dict]:
    total = sum(counter.values()) or 0
    return [{'code': k, 'label': ERROR_LABEL.get(k, k.replace('_', ' ').capitalize()), 'count': n,
             'pct': round(n * 100.0 / total, 1) if total else 0} for k, n in Counter(counter).most_common()]


def _window(days: int, now: int):
    cur_from = now - days * DAY_MS
    return cur_from, cur_from - days * DAY_MS


def _agg(qs):
    a = qs.aggregate(c=Count('id'), users=Sum('users_targeted'), pushed=Sum('users_pushed'), dt=Sum('devices_targeted'),
                     da=Sum('devices_accepted'), df=Sum('devices_failed'), pruned=Sum('tokens_pruned'))
    return {k: (v or 0) for k, v in a.items()}


def overview(days: int = 30, kind: str = '') -> dict:
    now = int(time.time() * 1000)
    days = days if days in (7, 30, 90) else 30
    cur_from, prev_from = _window(days, now)
    base = PushCampaign.objects.exclude(status__in=('scheduled', 'canceled')).exclude(kind='test')
    if kind in KIND_LABEL:
        base = base.filter(kind=kind)
    cur_qs, prev_qs = base.filter(created_at__gte=cur_from), base.filter(created_at__gte=prev_from, created_at__lt=cur_from)
    cur, prev = _agg(cur_qs), _agg(prev_qs)

    def opens_of(qs):
        return PushDelivery.objects.filter(campaign__in=qs.values('id')).exclude(opened_at=0)

    cur_opens, prev_opens = opens_of(cur_qs).count(), opens_of(prev_qs).count()
    clicks = PushDelivery.objects.filter(campaign__in=cur_qs.values('id')).exclude(clicked_at=0).count()
    open_rows = list(opens_of(cur_qs).values_list('opened_at', 'opened_via'))
    via = Counter(v or 'inbox' for _t, v in open_rows)

    window = _days(days)
    per_day = defaultdict(lambda: {'campaigns': 0, 'people': 0, 'accepted': 0, 'opens': 0})
    for created, users, acc in cur_qs.values_list('created_at', 'users_targeted', 'devices_accepted'):
        d = per_day[_day_of(created)]
        d['campaigns'] += 1
        d['people'] += users
        d['accepted'] += acc
    for t, _v in open_rows:
        per_day[_day_of(t)]['opens'] += 1
    series = [{'date': d, **per_day.get(d, {'campaigns': 0, 'people': 0, 'accepted': 0, 'opens': 0})} for d in window]

    errors = Counter()
    for e in cur_qs.exclude(errors={}).values_list('errors', flat=True):
        errors.update(e or {})

    by_kind = []
    for k, label in KIND_LABEL.items():
        if k == 'test':
            continue
        a = _agg(cur_qs.filter(kind=k))
        if a['c']:
            by_kind.append({'key': k, 'label': label, 'campaigns': a['c'], 'people': a['users'], 'accepted': a['da']})

    users_total = User.objects.filter(is_bot=False, is_banned=False).count()
    device_users = FCMToken.objects.exclude(user__isnull=True).values('user_id').distinct().count()
    opted_out = User.objects.filter(is_bot=False, notify_new_resources=False).count()
    hours = best_hours()
    return {
        'days': days, 'kind': kind,
        'kpis': {
            'campaigns': _kpi(cur['c'], prev['c']),
            'people': _kpi(cur['users'], prev['users']),
            'accepted': _kpi(cur['da'], prev['da']),
            'opens': _kpi(cur_opens, prev_opens),
        },
        'deliveryRate': _pct(cur['da'], cur['dt']),
        'deliveryRatePrev': _pct(prev['da'], prev['dt']),
        'openRate': _pct(cur_opens, cur['users']),
        'openRatePrev': _pct(prev_opens, prev['users']),
        'clickRate': _pct(clicks, cur['users']),
        'opensVia': {'push': via.get('push', 0), 'inbox': via.get('inbox', 0)},
        'series': series,
        'errors': error_rows(errors),
        'byKind': by_kind,
        'tokensPruned': cur['pruned'],
        'reach': {
            'members': users_total, 'withApp': device_users, 'inboxOnly': max(0, users_total - device_users),
            'appShare': _pct(device_users, users_total), 'optedOut': opted_out,
        },
        'bestHours': hours,
    }


def best_hours(days: int = 90) -> dict:
    """When pushes get opened, from the last `days` of deliveries. Needs a handful of opens to say anything."""
    since = int(time.time() * 1000) - days * DAY_MS
    rows = list(PushDelivery.objects.filter(opened_at__gte=since, opened_via='push').values_list('opened_at', flat=True))
    if len(rows) < 8:
        rows += list(PushDelivery.objects.filter(opened_at__gte=since).values_list('opened_at', flat=True))
    hourly = [0] * 24
    for t in rows:
        hourly[_hour_of(t)] += 1
    top = sorted(range(24), key=lambda h: -hourly[h])[:3] if len(rows) >= 8 else []
    return {'hourly': hourly, 'samples': len(rows), 'top': [{'hour': h, 'label': _hour_label(h)} for h in top if hourly[h]]}


def campaign_detail(c: PushCampaign) -> dict:
    rows = list(PushDelivery.objects.filter(campaign=c).values_list(
        'status', 'devices', 'accepted', 'class_level', 'created_at', 'opened_at', 'opened_via', 'clicked_at'))
    targeted = len(rows)
    with_app = sum(1 for r in rows if r[1] > 0)
    pushed = sum(1 for r in rows if r[2] > 0)
    opened = [r for r in rows if r[5]]
    clicked = sum(1 for r in rows if r[7])
    status = Counter(r[0] for r in rows)
    via = Counter(r[6] or 'inbox' for r in opened)

    delays = Counter()
    for r in opened:
        gap = max(0, r[5] - (c.started_at or r[4] or c.created_at))
        for key, _label, limit in DELAY_BUCKETS:
            if gap <= limit:
                delays[key] += 1
                break
    delay_rows = [{'key': k, 'label': lb, 'count': delays.get(k, 0), 'pct': _pct(delays.get(k, 0), len(opened)) or 0}
                  for k, lb, _l in DELAY_BUCKETS]

    t0 = c.started_at or c.created_at
    first48 = [0] * 48
    for r in opened:
        h = int((r[5] - t0) // 3600000)
        if 0 <= h < 48:
            first48[h] += 1
    hours_of_day = [0] * 24
    for r in opened:
        hours_of_day[_hour_of(r[5])] += 1

    by_class = defaultdict(lambda: [0, 0])
    for r in rows:
        k = r[3] or 'Not set'
        by_class[k][0] += 1
        if r[5]:
            by_class[k][1] += 1
    class_rows = sorted(({'label': k, 'targeted': v[0], 'opened': v[1], 'rate': _pct(v[1], v[0]) or 0}
                         for k, v in by_class.items()), key=lambda x: -x['targeted'])[:8]

    resources = []
    if c.resource_ids:
        alerts = {a.resource_id: a for a in ResourceAlert.objects.filter(resource_id__in=c.resource_ids)}
        reach = defaultdict(lambda: [0, 0])
        for rid, surface in ResourceReach.objects.filter(resource_id__in=c.resource_ids, is_owner=False,
                                                         first_at__gte=t0).values_list('resource_id', 'surface'):
            reach[rid][0] += 1
            if surface == 'notification':
                reach[rid][1] += 1
        for r in Resource.objects.filter(pk__in=c.resource_ids).order_by('-added_at')[:60]:
            a = alerts.get(r.id)
            resources.append({'id': r.id, 'title': r.title, 'subject': r.subject, 'level': r.grade_level,
                              'audience': a.audience_size if a else 0, 'views': reach[r.id][0],
                              'fromPush': reach[r.id][1]})
    errors = error_rows(c.errors or {})
    return {
        'funnel': [
            {'key': 'targeted', 'label': 'People targeted', 'count': targeted, 'pct': 100 if targeted else 0},
            {'key': 'app', 'label': 'Have the app', 'count': with_app, 'pct': _pct(with_app, targeted) or 0},
            {'key': 'pushed', 'label': 'Push accepted', 'count': pushed, 'pct': _pct(pushed, targeted) or 0},
            {'key': 'opened', 'label': 'Opened', 'count': len(opened), 'pct': _pct(len(opened), targeted) or 0},
            {'key': 'clicked', 'label': 'Went on to the page', 'count': clicked, 'pct': _pct(clicked, targeted) or 0},
        ],
        'openRate': _pct(len(opened), targeted),
        'openRateOfPushed': _pct(sum(1 for r in opened if r[2] > 0), pushed),
        'deliveryRate': _pct(c.devices_accepted, c.devices_targeted),
        'opensVia': {'push': via.get('push', 0), 'inbox': via.get('inbox', 0)},
        'status': dict(status),
        'delays': delay_rows,
        'first48': first48,
        'hoursOfDay': hours_of_day,
        'classes': class_rows,
        'errors': errors,
        'resources': resources,
        'durationSec': round((c.finished_at - c.started_at) / 1000.0, 1) if c.finished_at and c.started_at else None,
    }
