"""Post views and feed impressions.

One *view* is one viewer opening one post on one local day. `Post.view_count`
only moves when a new (post, viewer, day) row appears, so refreshing, the
author checking their own post, and bots do not inflate it. Re-opens and dwell
time are kept on the row for the insights page.
"""
from __future__ import annotations

import time
from datetime import datetime
from zoneinfo import ZoneInfo

from django.conf import settings
from django.db import IntegrityError, transaction
from django.db.models import F

from . import signals
from .models import Follow, Post, PostImpression, PostReach

SURFACES = ('feed', 'search', 'profile', 'share', 'direct', 'notification', 'related')
MAX_DWELL_MS = 30 * 60 * 1000
MAX_IMPRESSION_BATCH = 40


def local_day(ms: int | None = None) -> str:
    tz = ZoneInfo(settings.TIME_ZONE)
    dt = datetime.fromtimestamp((ms if ms is not None else time.time() * 1000) / 1000.0, tz)
    return dt.strftime('%Y-%m-%d')


def _is_bot(request, info) -> bool:
    from nebians.analytics import rules
    return rules.is_bot(info['ua'], is_app=info['source'] == 'app')


def _channel(request, info) -> str:
    if info['source'] == 'app':
        return 'app'
    ref = request.META.get('HTTP_REFERER', '') or ''
    if not ref:
        return 'direct'
    try:
        from nebians.analytics import events, rules
        return rules.classify_referrer(ref, events.own_hosts(request)).channel or 'direct'
    except Exception:
        return 'referral'


def _get_or_create_row(post, viewer, day, defaults):
    """get_or_create that survives two requests racing on the unique (post, viewer, day)."""
    try:
        with transaction.atomic():
            return PostReach.objects.get_or_create(post=post, viewer=viewer, day=day, defaults=defaults)
    except IntegrityError:
        return PostReach.objects.get(post=post, viewer=viewer, day=day), False


def record_view(request, post: Post, user=None, *, surface: str = '', dwell_ms: int = 0) -> dict:
    """Count a view. Returns {'counted': bool, 'view_count': int}."""
    info = signals.describe(request)
    if _is_bot(request, info):
        return {'counted': False, 'view_count': post.view_count}
    now = int(time.time() * 1000)
    day = local_day(now)
    uid = getattr(user, 'pk', None)
    viewer = signals.viewer_tag(uid, day=day, ip=info['ip'], user_agent=info['ua'])
    is_owner = bool(uid and uid == post.user_id)
    surface = surface if surface in SURFACES else ('direct' if not request.META.get('HTTP_REFERER') else 'share')
    dwell_ms = max(0, min(int(dwell_ms or 0), MAX_DWELL_MS))

    row, created = _get_or_create_row(
        post, viewer, day,
        dict(
            first_at=now, last_at=now, hits=1, dwell_ms=dwell_ms, surface=surface,
            source=info['source'], device_class=info['device_class'], os_family=info['os_family'],
            country=info['country'], channel=_channel(request, info), is_member=bool(uid),
            is_follower=bool(uid and Follow.objects.filter(follower_id=uid, following_id=post.user_id).exists()),
            is_owner=is_owner,
        ),
    )
    counted = False
    if created:
        if not is_owner:
            Post.objects.filter(pk=post.pk).update(view_count=F('view_count') + 1)
            counted = True
    else:
        updates = {'last_at': now}
        if dwell_ms:
            updates['dwell_ms'] = max(row.dwell_ms, dwell_ms)
        else:
            updates['hits'] = F('hits') + 1
        PostReach.objects.filter(pk=row.pk).update(**updates)
    count = Post.objects.filter(pk=post.pk).values_list('view_count', flat=True).first() or 0
    return {'counted': counted, 'view_count': count}


def record_impressions(request, post_ids) -> int:
    """Batch of posts that scrolled into view. Unknown ids are ignored."""
    info = signals.describe(request)
    if _is_bot(request, info):
        return 0
    ids = []
    for pid in list(post_ids or [])[:MAX_IMPRESSION_BATCH]:
        pid = str(pid)[:36]
        if pid and pid not in ids:
            ids.append(pid)
    if not ids:
        return 0
    known = set(Post.objects.filter(pk__in=ids).values_list('pk', flat=True))
    day = local_day()
    n = 0
    for pid in ids:
        if pid not in known:
            continue
        row, _ = PostImpression.objects.get_or_create(post_id=pid, day=day, source=info['source'])
        PostImpression.objects.filter(pk=row.pk).update(count=F('count') + 1)
        n += 1
    return n
