"""Per-post insights for the author (web + app) and for staff.

Everything here is an aggregate. No viewer is ever named: reach rows only hold
keyed hashes, and `ActorSignal` rows are only counted by device. Days are
local midnight in settings.TIME_ZONE, like the rest of the analytics.
"""
from __future__ import annotations

import statistics
import time
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from django.conf import settings
from django.db.models import Sum

from .models import (ActorSignal, Bookmark, Poll, PollVote, Post, PostImpression, PostReach, Reply)

VERSION = 1
RANGES = (7, 30, 90)
DWELL_BUCKETS = (('under5', 'Under 5 s', 0, 5), ('s5_15', '5 to 15 s', 5, 15),
                 ('s15_60', '15 to 60 s', 15, 60), ('over60', 'Over a minute', 60, 10 ** 9))
SURFACE_LABEL = {'feed': 'Feed', 'search': 'Search', 'profile': 'Profile', 'share': 'Shared link',
                 'direct': 'Direct', 'notification': 'Notification', 'related': 'Related posts'}
CHANNEL_LABEL = {'direct': 'Direct', 'search': 'Search engines', 'social': 'Social', 'email': 'Email',
                 'ai': 'AI assistants', 'referral': 'Other sites', 'campaign': 'Campaigns',
                 'internal': 'Inside NEBians', 'app': 'App', '': 'Unknown'}
DEVICE_LABEL = {'mobile': 'Phone', 'tablet': 'Tablet', 'desktop': 'Computer', 'other': 'Other', '': 'Unknown'}
OS_LABEL = {'android': 'Android', 'ios': 'iOS', 'windows': 'Windows', 'mac': 'macOS', 'linux': 'Linux',
            'chromeos': 'ChromeOS', '': 'Unknown'}


def _tz() -> ZoneInfo:
    return ZoneInfo(settings.TIME_ZONE)


def _day_of(ms: int) -> str:
    return datetime.fromtimestamp(ms / 1000.0, _tz()).strftime('%Y-%m-%d')


def _hour_of(ms: int) -> int:
    return datetime.fromtimestamp(ms / 1000.0, _tz()).hour


def _days(n: int) -> list[str]:
    today = datetime.now(_tz()).date()
    return [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(n - 1, -1, -1)]


def _change(cur, prev):
    if prev in (0, None):
        return None if not cur else 100.0
    return round((cur - prev) * 100.0 / prev, 1)


def _kpi(cur, prev):
    return {'value': cur, 'prev': prev, 'change': _change(cur, prev)}


def _split(counter: Counter, labels: dict | None = None, top: int = 6) -> list[dict]:
    total = sum(counter.values()) or 0
    rows = []
    for key, n in counter.most_common(top):
        rows.append({'key': key, 'label': (labels or {}).get(key, key or 'Unknown'), 'count': n,
                     'pct': round(n * 100.0 / total, 1) if total else 0})
    return rows


def _hour_label(h: int) -> str:
    suffix = 'AM' if h < 12 else 'PM'
    return f'{(h % 12) or 12} {suffix}'


def build(post: Post, days: int = 30, staff: bool = False) -> dict:
    days = days if days in RANGES else 30
    window = _days(days)
    prev_window = [(datetime.strptime(window[0], '%Y-%m-%d').date() - timedelta(days=days - i)).strftime('%Y-%m-%d')
                   for i in range(days)]
    cur_set, prev_set = set(window), set(prev_window)
    start_ms = int(datetime.strptime(prev_window[0], '%Y-%m-%d').replace(tzinfo=_tz()).timestamp() * 1000)

    reach_all = list(PostReach.objects.filter(post=post, is_owner=False))
    reach = [r for r in reach_all if r.day in cur_set]
    reach_prev = [r for r in reach_all if r.day in prev_set]

    imp_rows = list(PostImpression.objects.filter(post=post, day__in=cur_set | prev_set))
    imp = sum(r.count for r in imp_rows if r.day in cur_set)
    imp_prev = sum(r.count for r in imp_rows if r.day in prev_set)

    replies = list(Reply.objects.filter(post=post, created_at__gte=start_ms).values_list('created_at', flat=True))
    reply_day = Counter(_day_of(t) for t in replies)
    replies_cur = sum(n for d, n in reply_day.items() if d in cur_set)
    replies_prev = sum(n for d, n in reply_day.items() if d in prev_set)

    sig = list(ActorSignal.objects.filter(ref=post.pk, kind__in=('like', 'reply', 'vote', 'option'),
                                          created_at__gte=start_ms)
               .values_list('kind', 'created_at', 'device_class', 'source', 'os_family', 'ref2'))
    likes_day = Counter(_day_of(t) for k, t, *_ in sig if k == 'like')
    likes_cur = sum(n for d, n in likes_day.items() if d in cur_set)
    likes_prev = sum(n for d, n in likes_day.items() if d in prev_set)

    poll = Poll.objects.filter(post=post).prefetch_related('options').first()
    votes = []
    if poll:
        votes = list(PollVote.objects.filter(poll=poll).values_list('created_at', 'option_id', 'user_id'))
    vote_day = Counter(_day_of(t) for t, _o, _u in votes)
    votes_cur = sum(n for d, n in vote_day.items() if d in cur_set)
    votes_prev = sum(n for d, n in vote_day.items() if d in prev_set)

    uniq = {r.viewer for r in reach}
    uniq_prev = {r.viewer for r in reach_prev}
    dwell_rows = [r.dwell_ms / 1000.0 for r in reach if r.dwell_ms > 0]
    dwell_prev = [r.dwell_ms / 1000.0 for r in reach_prev if r.dwell_ms > 0]
    avg_dwell = round(sum(dwell_rows) / len(dwell_rows), 1) if dwell_rows else 0
    avg_dwell_prev = round(sum(dwell_prev) / len(dwell_prev), 1) if dwell_prev else 0

    reactions = likes_cur + replies_cur + votes_cur
    reactions_prev = likes_prev + replies_prev + votes_prev
    views = len(reach)

    # Daily series
    v_day, u_day = Counter(), defaultdict(set)
    for r in reach:
        v_day[r.day] += 1
        u_day[r.day].add(r.viewer)
    i_day = Counter()
    for r in imp_rows:
        i_day[r.day] += r.count
    series = [{'date': d, 'views': v_day.get(d, 0), 'unique': len(u_day.get(d, ())),
               'impressions': i_day.get(d, 0), 'likes': likes_day.get(d, 0),
               'replies': reply_day.get(d, 0), 'votes': vote_day.get(d, 0)} for d in window]

    # Hour of day
    hours = Counter(_hour_of(r.first_at) for r in reach)
    hourly = [hours.get(h, 0) for h in range(24)]
    peak_hour = max(range(24), key=lambda h: hourly[h]) if any(hourly) else None

    # Audience
    seen_days: dict[str, set] = defaultdict(set)
    for r in reach_all:
        seen_days[r.viewer].add(r.day)
    returning = sum(1 for v in uniq if len(seen_days[v]) > 1)
    members = len({r.viewer for r in reach if r.is_member})
    followers = len({r.viewer for r in reach if r.is_follower})

    surface = Counter(r.surface or 'direct' for r in reach)
    channel = Counter(r.channel or 'direct' for r in reach if r.source == 'web')
    device = Counter(r.device_class for r in reach)
    os_ = Counter(r.os_family for r in reach)
    source = Counter(r.source for r in reach)
    country = Counter(r.country for r in reach if r.country)

    dwell_buckets = []
    for key, label, lo, hi in DWELL_BUCKETS:
        n = sum(1 for s in dwell_rows if lo <= s < hi)
        dwell_buckets.append({'key': key, 'label': label, 'count': n,
                              'pct': round(n * 100.0 / len(dwell_rows), 1) if dwell_rows else 0})

    actions_by_device = {}
    for kind in ('like', 'reply', 'vote'):
        c = Counter(dc for k, t, dc, *_ in sig if k == kind and _day_of(t) in cur_set)
        actions_by_device[kind] = _split(c, DEVICE_LABEL, 4)

    bookmarks = Bookmark.objects.filter(target_type='post', target_id=post.pk).count()

    # Where this post stands among the author's posts
    mine = list(Post.objects.filter(user_id=post.user_id).values_list('view_count', flat=True))
    rank = sum(1 for v in mine if v > post.view_count) + 1
    median_views = int(statistics.median(mine)) if mine else 0
    standing = {
        'rank': rank, 'of': len(mine), 'medianViews': median_views,
        'vsMedian': _change(post.view_count, median_views) if len(mine) > 1 else None,
    }

    out = {
        'version': VERSION,
        'postId': post.pk,
        'title': post.title[:120],
        'days': days,
        'createdAt': post.created_at,
        'ageDays': max(0, int((time.time() * 1000 - post.created_at) / 86400000)),
        'isAnonymous': bool(post.is_anonymous),
        'range': {'from': window[0], 'to': window[-1]},
        'lifetime': {
            'views': post.view_count, 'likes': post.thumbs_up_count, 'replies': post.reply_count,
            'bookmarks': bookmarks, 'pollVotes': poll.total_votes if poll else 0,
            'uniqueViewers': len({r.viewer for r in reach_all}),
            'impressions': PostImpression.objects.filter(post=post).aggregate(n=Sum('count'))['n'] or 0,
        },
        'kpis': {
            'views': _kpi(views, len(reach_prev)),
            'uniqueViewers': _kpi(len(uniq), len(uniq_prev)),
            'impressions': _kpi(imp, imp_prev),
            'reactions': _kpi(reactions, reactions_prev),
            'likes': _kpi(likes_cur, likes_prev),
            'replies': _kpi(replies_cur, replies_prev),
            'avgDwellSec': _kpi(avg_dwell, avg_dwell_prev),
        },
        'ctr': round(views * 100.0 / imp, 1) if imp else None,
        'engagementRate': round(reactions * 100.0 / views, 1) if views else None,
        'series': series,
        'hourly': hourly,
        'peakHour': peak_hour,
        'peakHourLabel': _hour_label(peak_hour) if peak_hour is not None else '',
        'audience': {
            'members': members, 'guests': max(0, len(uniq) - members), 'followers': followers,
            'nonFollowers': max(0, len(uniq) - followers), 'returning': returning,
            'newViewers': max(0, len(uniq) - returning),
        },
        'surfaces': _split(surface, SURFACE_LABEL),
        'channels': _split(channel, CHANNEL_LABEL),
        'devices': _split(device, DEVICE_LABEL),
        'os': _split(os_, OS_LABEL),
        'sources': _split(source, {'web': 'Website', 'app': 'Android app'}),
        'countries': _split(country, None, 6),
        'dwell': {'avgSec': avg_dwell, 'medianSec': round(statistics.median(dwell_rows), 1) if dwell_rows else 0,
                  'buckets': dwell_buckets, 'samples': len(dwell_rows)},
        'actionsByDevice': actions_by_device,
        'standing': standing,
        'hasData': bool(reach_all or imp_rows),
    }

    if poll:
        by_opt = Counter(o for _t, o, _u in votes)
        dev_by_opt: dict[str, Counter] = defaultdict(Counter)
        for k, t, dc, src, osf, ref2 in sig:
            if k == 'vote':
                dev_by_opt[ref2][dc] += 1
        total = sum(by_opt.values())
        voters = len({u for _t, _o, u in votes})
        out['poll'] = {
            'id': poll.id, 'question': poll.question, 'pollType': poll.poll_type,
            'allowAddOptions': poll.allow_add_options, 'totalVotes': poll.total_votes, 'voters': voters,
            'participation': round(voters * 100.0 / len(uniq), 1) if uniq and voters else None,
            'options': [{
                'id': o.id, 'text': o.text, 'votes': by_opt.get(o.id, 0) or o.vote_count,
                'pct': round((by_opt.get(o.id, 0) or o.vote_count) * 100.0 / total, 1) if total else 0,
                'added': bool(o.added_by_id),
                'devices': _split(dev_by_opt.get(o.id, Counter()), DEVICE_LABEL, 3),
            } for o in sorted(poll.options.all(), key=lambda o: o.order)],
        }
    out['insights'] = _insights(out, staff)
    return out


def _insights(d: dict, staff: bool) -> list[dict]:
    tips: list[dict] = []
    k = d['kpis']

    def add(tone, title, body):
        tips.append({'tone': tone, 'title': title, 'body': body})

    if not d['hasData']:
        add('info', 'Nothing tracked yet', 'Views are counted from now on. Check back after a few readers open this post.')
        return tips
    ch = k['views']['change']
    if ch is not None and k['views']['prev'] >= 5 and abs(ch) >= 25:
        add('up' if ch > 0 else 'down', f"Views {'up' if ch > 0 else 'down'} {abs(round(ch))}%",
            f"{k['views']['value']} views in the last {d['days']} days against {k['views']['prev']} before.")
    ctr = d['ctr']
    if ctr is not None and k['impressions']['value'] >= 30:
        add('up' if ctr >= 8 else 'info', f'{ctr}% of people who saw it opened it',
            'Posts in this range usually sit near 6 to 10%. A sharper title lifts it.' if ctr < 6 else 'A strong open rate for a feed post.')
    dw = d['dwell']
    if dw['samples'] >= 5:
        long_pct = next((b['pct'] for b in dw['buckets'] if b['key'] == 'over60'), 0)
        quick = next((b['pct'] for b in dw['buckets'] if b['key'] == 'under5'), 0)
        if quick >= 50:
            add('down', f'{quick}% left in under 5 seconds', 'Open with the answer or the key point in the first lines.')
        elif long_pct >= 25:
            add('up', f'{long_pct}% read for over a minute', 'Readers are staying with it.')
    if d['peakHourLabel'] and k['views']['value'] >= 5:
        add('info', f"Most opens come around {d['peakHourLabel']}", 'Post at this hour next time to reach more readers.')
    dev = d['devices']
    if dev and k['views']['value'] >= 5:
        top = dev[0]
        add('info', f"{round(top['pct'])}% read on a {top['label'].lower()}", 'Keep formatting comfortable for that screen.')
    a = d['audience']
    if a['returning'] and k['uniqueViewers']['value']:
        pct = round(a['returning'] * 100.0 / k['uniqueViewers']['value'])
        if pct >= 15:
            add('up', f'{pct}% came back more than once', 'Repeat readers usually mean a post worth bookmarking.')
    st = d['standing']
    if st['of'] > 3 and st['vsMedian'] is not None:
        add('up' if st['vsMedian'] >= 0 else 'info', f"#{st['rank']} of your {st['of']} posts by views",
            f"{'Above' if st['vsMedian'] >= 0 else 'Below'} your median of {st['medianViews']} views.")
    poll = d.get('poll')
    if poll and poll['voters'] >= 3 and poll['options']:
        lead = max(poll['options'], key=lambda o: o['votes'])
        add('info', f"\"{lead['text'][:40]}\" leads with {round(lead['pct'])}%", f"{poll['voters']} people voted.")
    return tips[:6]
