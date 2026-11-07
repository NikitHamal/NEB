"""Sending and measuring pushes.

Everything that reaches a phone on purpose goes through `deliver`: a broadcast from the admin
composer, an announced batch of library uploads, an autopilot digest. One path means one set of
numbers. Each send is a `PushCampaign`; each person it touched is a `PushDelivery` row, which is
what the history page, the open-rate and the failure breakdown are built from.

An inbox row (`Notification`, tagged with `campaign_id`) is created for everyone by default, so a
person without the app still sees the message on the web, and opens are measurable on both sides.
"""
from __future__ import annotations

import logging
import threading
import time
import uuid
from collections import Counter
from dataclasses import dataclass, field

from django.db import close_old_connections
from django.db.models import F

from . import fcm_utils, push_audience
from .models import FCMToken, Notification, PushCampaign, PushDelivery, User

logger = logging.getLogger(__name__)

CHUNK = 200
INBOX_VERBS = {'library': 'new_resource', 'autopilot': 'new_resource'}


def now_ms() -> int:
    return int(time.time() * 1000)


@dataclass
class Message:
    user_id: str
    title: str
    body: str = ''
    url: str = ''
    target_type: str = 'system'
    target_id: str = ''
    push: bool = True
    hold: str = ''          # when push is False: 'capped' | 'quiet' | ''
    extra: dict = field(default_factory=dict)


def create_campaign(*, kind='manual', title='', body='', url='', target_type='system', target_id='',
                    audience=None, audience_label='', also_inbox=True, resource_ids=None,
                    created_by=None, scheduled_at=0, status=None, note='') -> PushCampaign:
    return PushCampaign.objects.create(
        id=str(uuid.uuid4()), kind=kind, title=title[:120], body=body, url=url[:300],
        target_type=target_type, target_id=target_id, audience=audience or {},
        audience_label=audience_label[:240], also_inbox=also_inbox, resource_ids=resource_ids or [],
        created_by=created_by, created_at=now_ms(), scheduled_at=scheduled_at or 0,
        status=status or ('scheduled' if scheduled_at else 'sending'), note=note[:240],
    )


def _inbox_text(title: str, body: str) -> str:
    return f'{title}\n{body}' if body else title


def _chunks(items, n):
    for i in range(0, len(items), n):
        yield items[i:i + n]


def _broadcast_inbox(rows):
    """Tell open web tabs; best effort and capped so a big send never stalls on sockets."""
    try:
        from . import realtime as _rt
        for n in rows[:3000]:
            _rt.broadcast_notification(n.recipient_id, {
                'id': n.id, 'verb': n.verb, 'actor_id': None, 'actor_anonymous': False,
                'actor_name': 'NEBians', 'actor_photo_url': '', 'target_type': n.target_type,
                'target_id': n.target_id, 'reference_type': '', 'reference_id': '',
                'message': n.message, 'created_at': n.created_at, 'url': '',
            })
    except Exception:  # noqa: BLE001
        logger.debug('inbox broadcast skipped', exc_info=True)


def deliver(campaign: PushCampaign, messages: list[Message]) -> PushCampaign:
    """Run a campaign for `messages` (one per person). Blocks until FCM has answered."""
    close_old_connections()
    t0 = now_ms()
    msgs = {}
    for m in messages:
        msgs.setdefault(str(m.user_id), m)          # one message per person per campaign
    ids = list(msgs)
    PushCampaign.objects.filter(pk=campaign.pk).update(status='sending', started_at=t0, users_targeted=len(ids))

    tokens: dict[str, list[str]] = {}
    classes: dict[str, str] = {}
    for chunk in _chunks(ids, 500):
        for uid, tok in FCMToken.objects.filter(user_id__in=chunk).values_list('user_id', 'token'):
            tokens.setdefault(uid, []).append(tok)
        for uid, cl in User.objects.filter(pk__in=chunk).values_list('id', 'class_level'):
            classes[uid] = cl or ''

    verb = INBOX_VERBS.get(campaign.kind, 'system')
    notif_ids: dict[str, str] = {}
    if campaign.also_inbox:
        rows = []
        for uid in ids:
            m = msgs[uid]
            nid = str(uuid.uuid4())
            notif_ids[uid] = nid
            rows.append(Notification(
                id=nid, recipient_id=uid, actor=None, verb=verb, target_type=m.target_type or 'system',
                target_id=(m.target_id or campaign.id)[:36], message=_inbox_text(m.title, m.body),
                campaign_id=campaign.id, is_read=False, created_at=t0))
        for chunk in _chunks(rows, 500):
            Notification.objects.bulk_create(chunk)
        for chunk in _chunks(ids, 500):
            User.objects.filter(pk__in=chunk).update(unread_notification_count=F('unread_notification_count') + 1)
        _broadcast_inbox(rows)

    deliveries = {}
    for uid in ids:
        m = msgs[uid]
        devs = tokens.get(uid, [])
        status = 'queued' if (m.push and devs) else (m.hold or ('inbox' if campaign.also_inbox else 'nodevice'))
        if not m.push and m.hold == '':
            status = 'inbox' if campaign.also_inbox else 'nodevice'
        deliveries[uid] = PushDelivery(
            campaign=campaign, user_id=uid, notification_id=notif_ids.get(uid, ''), status=status,
            devices=len(devs), class_level=classes.get(uid, '')[:40], created_at=t0)
    for chunk in _chunks(list(deliveries.values()), 500):
        PushDelivery.objects.bulk_create(chunk, ignore_conflicts=True)
    # bulk_create leaves primary keys unset on some databases; read the rows back.
    deliveries = {d.user_id: d for d in PushDelivery.objects.filter(campaign=campaign)}

    errors = Counter()
    sent_users = devices_ok = devices_bad = devices_total = 0
    for chunk in _chunks([u for u in ids if deliveries[u].status == 'queued'], CHUNK):
        for uid in chunk:
            m, d = msgs[uid], deliveries[uid]
            payload = {
                'verb': verb, 'target_type': m.target_type or 'system', 'target_id': m.target_id or '',
                'url': m.url, 'campaign_id': campaign.id, 'notification_id': d.notification_id,
                'kind': campaign.kind, **m.extra,
            }
            result = fcm_utils.send_fcm_detailed(tokens[uid], m.title, m.body, payload)
            ok = sum(1 for a, _c in result.values() if a)
            bad = len(result) - ok
            devices_total += len(result)
            devices_ok += ok
            devices_bad += bad
            for a, code in result.values():
                if not a:
                    errors[code] += 1
            d.accepted = ok
            if ok:
                d.status = 'sent'
                sent_users += 1
            else:
                d.status = 'failed'
                d.error = next((c for a, c in result.values() if not a), 'unknown')[:60]
        PushDelivery.objects.bulk_update([deliveries[u] for u in chunk], ['status', 'accepted', 'error'])
        PushCampaign.objects.filter(pk=campaign.pk).update(
            users_pushed=sent_users, devices_targeted=devices_total, devices_accepted=devices_ok,
            devices_failed=devices_bad, errors=dict(errors))

    held = sum(1 for d in deliveries.values() if d.status in ('capped', 'quiet'))
    inbox_only = sum(1 for d in deliveries.values() if d.status in ('inbox', 'nodevice'))
    pruned = sum(c for k, c in errors.items() if k in ('unregistered', 'sender_id_mismatch'))
    failed_all = devices_total > 0 and devices_ok == 0
    PushCampaign.objects.filter(pk=campaign.pk).update(
        status='failed' if failed_all and not campaign.also_inbox else 'sent', finished_at=now_ms(),
        users_pushed=sent_users, users_inbox_only=inbox_only, users_suppressed=held,
        devices_targeted=devices_total, devices_accepted=devices_ok, devices_failed=devices_bad,
        tokens_pruned=pruned, errors=dict(errors))
    campaign.refresh_from_db()
    return campaign


def run_in_background(fn, *args, **kwargs):
    """Fire-and-forget worker thread for the admin request; tests call `fn` directly."""
    def _run():
        try:
            fn(*args, **kwargs)
        except Exception:  # noqa: BLE001
            logger.exception('push worker crashed')
            cid = args[0] if args and isinstance(args[0], str) else ''
            if cid:
                PushCampaign.objects.filter(pk=cid).update(status='failed', finished_at=now_ms(), note='Worker crashed, see logs')
        finally:
            close_old_connections()
    t = threading.Thread(target=_run, daemon=True, name='push-send')
    t.start()
    return t


def run_manual(campaign_id: str) -> PushCampaign:
    """Resolve the stored audience now and send the campaign's own text to everyone in it."""
    campaign = PushCampaign.objects.get(pk=campaign_id)
    user_ids = list(push_audience.queryset(campaign.audience).values_list('id', flat=True))
    messages = [Message(user_id=u, title=campaign.title, body=campaign.body, url=campaign.url,
                        target_type=campaign.target_type or 'system', target_id=campaign.target_id)
                for u in user_ids]
    return deliver(campaign, messages)


def send_manual(*, title, body, url='', target_type='system', target_id='', filters=None, also_inbox=True,
                created_by=None, scheduled_at=0, kind='manual', sync=False) -> PushCampaign:
    filters = push_audience.clean(filters or {})
    campaign = create_campaign(
        kind=kind, title=title, body=body, url=url, target_type=target_type, target_id=target_id,
        audience=filters, audience_label=push_audience.describe(filters), also_inbox=also_inbox,
        created_by=created_by, scheduled_at=scheduled_at)
    if scheduled_at and scheduled_at > now_ms():
        return campaign
    if sync:
        return run_manual(campaign.id)
    run_in_background(run_manual, campaign.id)
    return campaign


def run_due_scheduled() -> int:
    """Start campaigns whose time has come. Each is claimed atomically, so two workers never double send."""
    n = 0
    for cid in list(PushCampaign.objects.filter(status='scheduled', scheduled_at__lte=now_ms()).values_list('id', flat=True)):
        if PushCampaign.objects.filter(pk=cid, status='scheduled').update(status='sending'):
            run_manual(cid)
            n += 1
    return n


# ---- opens -----------------------------------------------------------------

def mark_opened(notification_ids, via='inbox') -> int:
    """A person read the inbox row or tapped the push. First open wins; later ones add nothing."""
    ids = [i for i in (notification_ids or []) if i]
    if not ids:
        return 0
    return PushDelivery.objects.filter(notification_id__in=ids, opened_at=0).update(opened_at=now_ms(), opened_via=via)


def mark_all_opened_for_user(user_id, via='inbox') -> int:
    ids = list(Notification.objects.filter(recipient_id=user_id, is_read=False).exclude(campaign_id='')
               .values_list('id', flat=True)[:500])
    return mark_opened(ids, via)


def record_push_open(user, campaign_id='', notification_id='') -> bool:
    """The app reports a tap on a push. Also reads the matching inbox row so the badge stays honest."""
    qs = PushDelivery.objects.filter(user_id=user.id)
    if notification_id:
        qs = qs.filter(notification_id=notification_id)
    elif campaign_id:
        qs = qs.filter(campaign_id=campaign_id)
    else:
        return False
    row = qs.first()
    if not row:
        return False
    updates = {}
    if not row.opened_at:
        updates.update(opened_at=now_ms(), opened_via='push')
    updates['clicked_at'] = row.clicked_at or now_ms()
    PushDelivery.objects.filter(pk=row.pk).update(**updates)
    if row.notification_id:
        Notification.objects.filter(pk=row.notification_id, recipient_id=user.id, is_read=False).update(is_read=True)
    return True


def record_click(user_id, campaign_id) -> None:
    """The person went on to open the thing the message pointed at (resource page, link)."""
    if user_id and campaign_id:
        PushDelivery.objects.filter(user_id=user_id, campaign_id=campaign_id, clicked_at=0).update(clicked_at=now_ms())
        PushDelivery.objects.filter(user_id=user_id, campaign_id=campaign_id, opened_at=0).update(opened_at=now_ms(), opened_via='push')
