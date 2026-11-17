"""Library reach: views, reads, downloads, shares and list impressions of resources.

One *view* is one viewer opening one resource on one local day (the `post_reach` twin).
`Resource.view_count` and `Resource.download_count` only move for a new (resource, viewer, day)
that is not the uploader and not a bot, so refreshes and bots do not inflate them.

Everything here is best effort: a tracking failure is logged and swallowed, it can never fail a page.
A tap that came from a push (`src=push`) also marks the matching `PushDelivery` as clicked, which is
what closes the push funnel (sent -> opened -> went on to the resource).
"""
from __future__ import annotations

import logging
import time

from django.db import IntegrityError, transaction
from django.db.models import F

from . import signals
from .models import PushCampaign, PushDelivery, Resource, ResourceAlert, ResourceImpression, ResourceReach
from .post_reach import MAX_DWELL_MS, MAX_IMPRESSION_BATCH, _channel, _is_bot, local_day

logger = logging.getLogger(__name__)

SURFACES = ('library', 'search', 'subject', 'profile', 'share', 'direct', 'notification', 'related', 'home')
ACTIONS = ('read', 'download', 'share')
PUSH_SOURCES = ('push', 'inbox')


def norm_surface(value: str, request=None, src: str = '') -> str:
    """Where the person came from. A push tap always wins; unknown values fall back to direct / share."""
    if (src or '').lower() in PUSH_SOURCES:
        return 'notification'
    value = (value or '').lower()[:12]
    if value in SURFACES:
        return value
    if request is not None and request.META.get('HTTP_REFERER'):
        return 'share'
    return 'direct'


def attribute_push(user_id, resource_id: str) -> int:
    """The person opened the resource a push pointed at: mark the delivery clicked. Returns rows touched."""
    if not user_id or not resource_id:
        return 0
    campaign_ids = set()
    alert = ResourceAlert.objects.filter(resource_id=resource_id).values_list('campaign_id', flat=True).first()
    if alert:
        campaign_ids.add(alert)
    campaign_ids.update(PushCampaign.objects.filter(target_type='resource', target_id=resource_id)
                        .values_list('id', flat=True)[:20])
    touched = 0
    now = int(time.time() * 1000)
    for cid in campaign_ids:
        qs = PushDelivery.objects.filter(user_id=user_id, campaign_id=cid)
        touched += qs.filter(clicked_at=0).update(clicked_at=now)
        qs.filter(opened_at=0).update(opened_at=now, opened_via='push')
    return touched


def _row(resource: Resource, viewer: str, day: str, defaults: dict):
    """get_or_create that survives two requests racing on the unique (resource, viewer, day)."""
    try:
        with transaction.atomic():
            return ResourceReach.objects.get_or_create(resource=resource, viewer=viewer, day=day, defaults=defaults)
    except IntegrityError:
        return ResourceReach.objects.get(resource=resource, viewer=viewer, day=day), False


def record_view(request, resource: Resource, user=None, *, surface: str = '', dwell_ms: int = 0, src: str = '') -> dict:
    """Count a view. Returns {'counted': bool, 'view_count': int}."""
    try:
        info = signals.describe(request)
        if _is_bot(request, info):
            return {'counted': False, 'view_count': resource.view_count}
        now = int(time.time() * 1000)
        day = local_day(now)
        uid = getattr(user, 'pk', None)
        viewer = signals.viewer_tag(uid, day=day, ip=info['ip'], user_agent=info['ua'])
        is_owner = bool(uid and uid == resource.uploaded_by_id)
        surface = norm_surface(surface, request, src)
        dwell_ms = max(0, min(int(dwell_ms or 0), MAX_DWELL_MS))
        row, created = _row(resource, viewer, day, dict(
            first_at=now, last_at=now, hits=1, dwell_ms=dwell_ms, surface=surface, source=info['source'],
            device_class=info['device_class'], os_family=info['os_family'], country=info['country'],
            channel=_channel(request, info), class_level=(getattr(user, 'class_level', '') or '')[:40],
            is_member=bool(uid), is_owner=is_owner))
        counted = False
        if created:
            if not is_owner and resource.approval_status == 'approved':
                Resource.objects.filter(pk=resource.pk).update(view_count=F('view_count') + 1)
                counted = True
        else:
            updates = {'last_at': now}
            if dwell_ms:
                updates['dwell_ms'] = max(row.dwell_ms, dwell_ms)
            else:
                updates['hits'] = F('hits') + 1
            if surface == 'notification' and row.surface != 'notification':
                updates['surface'] = surface
            ResourceReach.objects.filter(pk=row.pk).update(**updates)
        if surface == 'notification' and uid and not is_owner:
            attribute_push(uid, resource.pk)
        count = Resource.objects.filter(pk=resource.pk).values_list('view_count', flat=True).first() or 0
        return {'counted': counted, 'view_count': count}
    except Exception:  # noqa: BLE001 - tracking never fails a request
        logger.exception('resource view tracking failed')
        return {'counted': False, 'view_count': resource.view_count}


def record_action(request, resource: Resource, user=None, action: str = '') -> dict:
    """read | download | share. Sets the flag on today's row (creating it when the view beacon was missed)."""
    if action not in ACTIONS:
        return {'ok': False, 'error': 'Unknown action'}
    try:
        info = signals.describe(request)
        if _is_bot(request, info):
            return {'ok': False}
        now = int(time.time() * 1000)
        day = local_day(now)
        uid = getattr(user, 'pk', None)
        viewer = signals.viewer_tag(uid, day=day, ip=info['ip'], user_agent=info['ua'])
        is_owner = bool(uid and uid == resource.uploaded_by_id)
        row, created = _row(resource, viewer, day, dict(
            first_at=now, last_at=now, hits=1, surface='direct', source=info['source'],
            device_class=info['device_class'], os_family=info['os_family'], country=info['country'],
            channel=_channel(request, info), class_level=(getattr(user, 'class_level', '') or '')[:40],
            is_member=bool(uid), is_owner=is_owner))
        field = {'read': 'read', 'download': 'downloaded', 'share': 'shared'}[action]
        first_time = not getattr(row, field)
        ResourceReach.objects.filter(pk=row.pk).update(**{field: True, 'last_at': now})
        if action == 'download' and first_time and not is_owner and resource.approval_status == 'approved':
            Resource.objects.filter(pk=resource.pk).update(download_count=F('download_count') + 1)
        return {'ok': True, 'first': first_time}
    except Exception:  # noqa: BLE001
        logger.exception('resource action tracking failed')
        return {'ok': False}


def record_impressions(request, resource_ids) -> int:
    """Batch of resource cards that scrolled into view. Unknown ids are ignored."""
    try:
        info = signals.describe(request)
        if _is_bot(request, info):
            return 0
        ids = []
        for rid in list(resource_ids or [])[:MAX_IMPRESSION_BATCH]:
            rid = str(rid)[:36]
            if rid and rid not in ids:
                ids.append(rid)
        if not ids:
            return 0
        known = set(Resource.objects.filter(pk__in=ids).values_list('pk', flat=True))
        valid = [rid for rid in ids if rid in known]
        if not valid:
            return 0
        day = local_day()
        source = info['source']
        # One read, one bulk insert (conflicts ignored) and one update for the whole batch;
        # it used to be get_or_create + update per card, 3 queries each, on every scroll.
        have = set(ResourceImpression.objects.filter(
            resource_id__in=valid, day=day, source=source).values_list('resource_id', flat=True))
        fresh = [rid for rid in valid if rid not in have]
        if fresh:
            ResourceImpression.objects.bulk_create(
                [ResourceImpression(resource_id=rid, day=day, source=source, count=0) for rid in fresh],
                ignore_conflicts=True)
        ResourceImpression.objects.filter(resource_id__in=valid, day=day, source=source).update(count=F('count') + 1)
        return len(valid)
    except Exception:  # noqa: BLE001
        logger.exception('resource impression tracking failed')
        return 0
