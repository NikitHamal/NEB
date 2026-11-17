"""Admin-only device and content-performance sections of the Analytics page.

Reads the private `ActorSignal` table (see api/signals.py) and post reach rows.
Everything is an aggregate except the "recent sign-ups" table, which goes from
a user to their signal by recomputing the keyed tag (one way). Nothing here is
reachable outside the staff-guarded analytics view.
"""
from __future__ import annotations

from collections import Counter, defaultdict

from django.db.models import Count, Sum


KIND_LABEL = {'signup': 'Sign-ups', 'post': 'Posts', 'reply': 'Comments', 'vote': 'Poll votes',
              'like': 'Likes', 'option': 'Options added'}
DEVICE_LABEL = {'mobile': 'Phone', 'tablet': 'Tablet', 'desktop': 'Computer', 'other': 'Other', '': 'Unknown'}
OS_LABEL = {'android': 'Android', 'ios': 'iOS', 'windows': 'Windows', 'mac': 'macOS', 'linux': 'Linux',
            'chromeos': 'ChromeOS', '': 'Unknown'}


def _rank(counter: Counter, labels: dict | None = None, limit: int = 8) -> list[dict]:
    total = sum(counter.values())
    rows = [{'name': (labels or {}).get(k, k or 'Unknown'), 'count': n} for k, n in counter.most_common(limit) if n]
    top = rows[0]['count'] if rows else 0
    for r in rows:
        r['display'] = f"{r['count']:,}"
        r['pct'] = round(r['count'] * 100 / total, 1) if total else 0
        r['width'] = round(r['count'] * 100 / top, 1) if top else 0
    return rows


def _summary(sig, detail: dict) -> str:
    bits = [OS_LABEL.get(sig.os_family, sig.os_family or 'Unknown OS')]
    model = detail.get('model')
    if model:
        bits.append(f"{detail.get('brand', '')} {model}".strip())
    elif sig.device_class:
        bits.append(DEVICE_LABEL.get(sig.device_class, sig.device_class))
    if sig.source == 'app':
        bits.append(f'app {sig.app_version}' if sig.app_version else 'app')
    elif sig.browser:
        bits.append(sig.browser)
    return ' · '.join(b for b in bits if b)


def build(rng: dict, source: str = 'all') -> dict:
    from api import signals
    from api.models import (ActorSignal, Poll, PollOption, PollVote, Post, PostImpression, PostReach, User)

    start, end = rng['start'], rng['end']
    qs = ActorSignal.objects.filter(created_at__gte=start, created_at__lt=end)
    if source in ('web', 'app'):
        qs = qs.filter(source=source)
    rows = list(qs.values('kind', 'actor', 'source', 'device_class', 'os_family', 'browser', 'app_version'))

    by_kind: dict[str, list] = defaultdict(list)
    for r in rows:
        by_kind[r['kind']].append(r)

    signups = by_kind.get('signup', [])
    su_devices = Counter(r['device_class'] for r in signups)
    su_os = Counter(r['os_family'] for r in signups)
    su_src = Counter(r['source'] for r in signups)
    su_browser = Counter(r['browser'] for r in signups if r['source'] == 'web')
    app_versions = Counter(r['app_version'] or 'unknown' for r in rows if r['source'] == 'app')

    # Which sign-up device types go on to take part (any post, comment, vote or like in range)
    actors_active = {r['actor'] for k in ('post', 'reply', 'vote', 'like') for r in by_kind.get(k, [])}
    activation = []
    for dc in ('mobile', 'tablet', 'desktop'):
        group = [r for r in signups if r['device_class'] == dc]
        if group:
            act = sum(1 for r in group if r['actor'] in actors_active)
            activation.append({'name': DEVICE_LABEL[dc], 'count': len(group), 'pct': round(act * 100 / len(group), 1),
                               'display': f'{len(group):,}', 'width': round(act * 100 / len(group), 1)})

    matrix = []
    for kind in ('signup', 'post', 'reply', 'vote', 'like', 'option'):
        items = by_kind.get(kind, [])
        if not items:
            continue
        c = Counter(r['device_class'] for r in items)
        total = len(items)
        app_n = sum(1 for r in items if r['source'] == 'app')
        matrix.append({
            'label': KIND_LABEL[kind], 'total': total, 'phone': c.get('mobile', 0), 'tablet': c.get('tablet', 0),
            'desktop': c.get('desktop', 0), 'app_pct': round(app_n * 100 / total) if total else 0,
            'phone_pct': round(c.get('mobile', 0) * 100 / total) if total else 0,
            'actors': len({r['actor'] for r in items}),
        })

    # Precise hardware, aggregated only (decrypts the newest app rows)
    models, androids, screens = Counter(), Counter(), Counter()
    recent = (qs.filter(source='app', kind__in=('signup', 'login')).exclude(detail='')
              .order_by('-created_at').values_list('detail', flat=True)[:1500])
    for blob in recent:
        d = signals.unseal(blob)
        if d.get('model'):
            models[f"{d.get('brand', '')} {d['model']}".strip()] += 1
        if d.get('os'):
            androids[d['os']] += 1
        if d.get('screen'):
            screens[d['screen']] += 1

    # Recent sign-ups with their device (user -> tag, never tag -> user)
    users = list(User.objects.filter(created_at__gte=start, created_at__lt=end).order_by('-created_at')[:25])
    tag_to_user = {signals.actor_tag(u.pk): u for u in users}
    found = {}
    for s in ActorSignal.objects.filter(kind='signup', actor__in=list(tag_to_user)):
        found[s.actor] = s
    recent_signups = []
    for tag, u in tag_to_user.items():
        s = found.get(tag)
        recent_signups.append({
            'name': u.display_name or u.username, 'username': u.username, 'at': u.created_at,
            'device': _summary(s, signals.unseal(s.detail)) if s else 'Before device tracking',
            'source': (s.source if s else ''), 'tracked': bool(s),
        })
    recent_signups.sort(key=lambda r: -r['at'])

    # Post performance from reach rows (batched in 2 queries instead of 2 per post)
    reach = PostReach.objects.filter(first_at__gte=start, first_at__lt=end, is_owner=False)
    if source in ('web', 'app'):
        reach = reach.filter(source=source)
    top_rows = list(reach.values('post_id').annotate(views=Count('id'), dwell=Sum('dwell_ms')).order_by('-views')[:8])
    top_ids = [r['post_id'] for r in top_rows]
    posts_by_id = {
        p['id']: p
        for p in Post.objects.filter(pk__in=top_ids).values('id', 'title', 'reply_count', 'thumbs_up_count')
    } if top_ids else {}
    imp_by_id = dict(
        PostImpression.objects.filter(post_id__in=top_ids).values_list('post_id').annotate(n=Sum('count'))
    ) if top_ids else {}
    top_posts = []
    for row in top_rows:
        post = posts_by_id.get(row['post_id'])
        if not post:
            continue
        imp = imp_by_id.get(post['id']) or 0
        top_posts.append({
            'id': post['id'], 'title': post['title'][:80], 'views': row['views'],
            'reactions': post['reply_count'] + post['thumbs_up_count'],
            'dwell': round((row['dwell'] or 0) / max(row['views'], 1) / 1000),
            'ctr': round(row['views'] * 100 / imp, 1) if imp else None,
        })
    reach_devices = Counter(reach.values_list('device_class', flat=True))
    reach_surface = Counter(reach.values_list('surface', flat=True))

    polls_created = Poll.objects.filter(created_at__gte=start, created_at__lt=end)
    poll_stats = {
        'created': polls_created.count(),
        'in_comments': polls_created.filter(reply__isnull=False).count(),
        'open': polls_created.filter(allow_add_options=True).count(),
        'options_added': PollOption.objects.filter(added_by__isnull=False, created_at__gte=start, created_at__lt=end).count(),
        'votes': PollVote.objects.filter(created_at__gte=start, created_at__lt=end).count(),
    }

    return {
        'tracked': len(rows),
        'signups': len(signups),
        'signup_devices': _rank(su_devices, DEVICE_LABEL),
        'signup_os': _rank(su_os, OS_LABEL),
        'signup_sources': _rank(su_src, {'web': 'Website', 'app': 'Android app'}),
        'signup_browsers': _rank(su_browser),
        'activation': activation,
        'matrix': matrix,
        'app_versions': _rank(app_versions),
        'app_models': _rank(models),
        'app_android': _rank(androids),
        'app_screens': _rank(screens, limit=6),
        'recent_signups': recent_signups,
        'top_posts': top_posts,
        'reach_devices': _rank(reach_devices, DEVICE_LABEL),
        'reach_surfaces': _rank(reach_surface, {'': 'Unknown', 'feed': 'Feed', 'search': 'Search', 'profile': 'Profile',
                                              'share': 'Shared link', 'direct': 'Direct', 'notification': 'Notification',
                                              'related': 'Related posts'}),
        'polls': poll_stats,
    }
