"""Library autopilot: tell the right people when a resource lands, and nobody else.

A resource that goes live (created approved, or approved from the review queue) gets a
`ResourceAlert` row. A worker then waits for the uploads to settle (a 92 file upload becomes ONE
round, not 92), finds the people it is for, and sends each of them ONE message.

Who it is for: a member whose class is the resource's class AND who picked that subject (or, for
programme courses, whose programme matches). They can switch it off (`User.notify_new_resources`).

Why it does not spam:
  - one push per person per round, however many resources match (a digest);
  - at most `daily_cap` autopilot pushes per person per rolling 24 hours; beyond that the message
    still lands in the inbox, silently;
  - nothing buzzes during quiet hours (Nepal time); the round waits until morning;
  - rounds wait for `settle_minutes` of silence, so bulk uploads coalesce;
  - the uploader is never told about their own upload;
  - stale resources (older than three days when the round runs) are dropped.

Resources that were already in the library before the autopilot existed have no alert row, so
they are never announced automatically. Staff announce them by hand from the admin Autopilot tab,
which uses the same audience and digest rules (`announce`).
"""
from __future__ import annotations

import logging
import re
import sys
import threading
import time
import uuid
from collections import defaultdict
from datetime import datetime
from zoneinfo import ZoneInfo

from django.conf import settings
from django.db.models.signals import post_save, pre_save

from . import push_engine
from .models import PushCampaign, PushDelivery, PushSettings, Resource, ResourceAlert, User

logger = logging.getLogger(__name__)

STALE_MS = 3 * 86400000
MIN = 60000

_ALIASES = {
    'science': 'science and technology', 'science & technology': 'science and technology',
    'english': 'compulsory english', 'nepali': 'compulsory nepali',
    'math': 'mathematics', 'maths': 'mathematics', 'optional math': 'optional mathematics',
    'optional maths': 'optional mathematics', 'computer': 'computer science',
    'social': 'social studies and human values education', 'social studies': 'social studies and human values education',
    'accounts': 'accountancy', 'account': 'accountancy',
}


def get_settings() -> PushSettings:
    obj, _ = PushSettings.objects.get_or_create(pk=1)
    return obj


# ---- matching ----------------------------------------------------------------

def norm_level(value) -> str:
    """'Class 10 / SEE', 'Class 10' and '10' are one level; 'Bachelors' stays itself."""
    s = re.sub(r'\s+', ' ', str(value or '').strip().lower())
    m = re.match(r'^(?:class\s*)?(\d{1,2})(?:\s*/.*)?$', s)
    return m.group(1) if m else s


def level_variants(value) -> list[str]:
    n = norm_level(value)
    if n.isdigit():
        out = [n, f'Class {n}']
        if n == '10':
            out.append('Class 10 / SEE')
        return out
    return [str(value).strip()] if value else []


def norm_subject(value) -> str:
    s = re.sub(r'\s+', ' ', str(value or '').strip().lower()).replace(' and ', ' and ')
    return _ALIASES.get(s, s)


_ROMAN = re.compile(r'\s+(i|ii|iii|iv|1|2|3|4)$')


def subject_matches(user_subject: str, resource_subject: str) -> bool:
    a, b = norm_subject(user_subject), norm_subject(resource_subject)
    if not a or not b:
        return False
    if a == b:
        return True
    # "Mathematics" matches "Mathematics II", never "Optional Mathematics".
    return _ROMAN.sub('', b) == a or _ROMAN.sub('', a) == b


def user_subjects(raw) -> list[str]:
    return [s.strip() for s in str(raw or '').split(',') if s.strip()]


def audience_for(resource: Resource) -> list[str]:
    """Ids of the people this resource is for. Respects the opt-out. Excludes the uploader."""
    if not resource.grade_level:
        return []
    variants = level_variants(resource.grade_level)
    if not variants:
        return []
    from django.db.models import Q
    q = Q()
    for v in variants:
        q |= Q(class_level__iexact=v)
    qs = (User.objects.filter(q, is_bot=False, is_banned=False, notify_new_resources=True)
          .exclude(pk=resource.uploaded_by_id or ''))
    prog = (resource.program or '').strip().lower()
    out = []
    for uid, subjects, edu_program in qs.values_list('id', 'subjects', 'edu_program').iterator():
        if any(subject_matches(s, resource.subject) for s in user_subjects(subjects)):
            out.append(uid)
        elif prog and (edu_program or '').strip().lower() == prog:
            out.append(uid)
    return out


# ---- time ----------------------------------------------------------------------

def _local_hour(ms: int) -> int:
    return datetime.fromtimestamp(ms / 1000.0, ZoneInfo(settings.TIME_ZONE)).hour


def in_quiet_hours(ms: int, cfg: PushSettings | None = None) -> bool:
    cfg = cfg or get_settings()
    start, end, h = cfg.quiet_start_hour, cfg.quiet_end_hour, _local_hour(ms)
    if start == end:
        return False
    return (h >= start or h < end) if start > end else (start <= h < end)


# ---- queue ---------------------------------------------------------------------

def enqueue(resource: Resource) -> ResourceAlert | None:
    cfg = get_settings()
    if not resource.is_lead or resource.approval_status != 'approved':
        return None
    alert, created = ResourceAlert.objects.get_or_create(
        resource=resource, defaults={'state': 'pending', 'queued_at': push_engine.now_ms()})
    if not created:
        return alert
    skip = ''
    if not cfg.autopilot_enabled:
        skip = 'autopilot_off'
    elif resource.is_paid and not cfg.include_paid:
        skip = 'paid'
    if skip:
        ResourceAlert.objects.filter(pk=alert.pk).update(state='skipped', reason=skip, processed_at=push_engine.now_ms())
        return alert
    ensure_worker()
    return alert


def _prefix(resource: Resource) -> str:
    return f'{resource.subject}'.strip() or 'Library'


def _level_label(grade_level: str) -> str:
    n = norm_level(grade_level)
    if n.isdigit():
        return f'Class {n}'
    return grade_level or 'your level'


def compose(resources: list[Resource]) -> tuple[str, str, str, str]:
    """(title, body, target_type, target_id) for one person's matching resources."""
    first = resources[0]
    if len(resources) == 1:
        title = f'New {first.subject} resource' if first.subject else 'New in the library'
        return title, first.title, 'resource', first.id
    subjects = []
    for r in resources:
        if r.subject and r.subject not in subjects:
            subjects.append(r.subject)
    levels = {norm_level(r.grade_level) for r in resources if r.grade_level}
    if len(subjects) == 1:
        title = f'{len(resources)} new {subjects[0]} resources'
        if len(levels) == 1:
            title += f' added for {_level_label(first.grade_level)}'
    else:
        title = f'{len(resources)} new resources for you'
    shown = [r.title for r in resources[:2]]
    extra = len(resources) - len(shown)
    body = ' and '.join(shown) if extra <= 0 else f"{', '.join(shown)} and {extra} more"
    if len(subjects) > 1:
        body = ', '.join(subjects[:3]) + (f' and {len(subjects) - 3} more' if len(subjects) > 3 else '')
    return title, body[:180], 'resource', first.id


def _recent_push_counts(user_ids, since_ms) -> dict:
    out = {}
    ids = list(user_ids)
    for i in range(0, len(ids), 500):
        for uid in (PushDelivery.objects.filter(user_id__in=ids[i:i + 500], status='sent', created_at__gte=since_ms,
                                                campaign__kind='autopilot').values_list('user_id', flat=True)):
            out[uid] = out.get(uid, 0) + 1
    return out


def _build_messages(resources: list[Resource], *, respect_caps: bool, cfg: PushSettings):
    """Per person digest. Returns (messages, per_resource_audience_size)."""
    per_user = defaultdict(list)
    sizes = {}
    for r in resources:
        aud = audience_for(r)
        sizes[r.id] = len(aud)
        for uid in aud:
            per_user[uid].append(r)
    capped = _recent_push_counts(per_user, push_engine.now_ms() - 86400000) if respect_caps else {}
    messages = []
    for uid, rs in per_user.items():
        rs.sort(key=lambda r: (-r.added_at, r.title))
        title, body, ttype, tid = compose(rs)
        push, hold = True, ''
        if respect_caps and capped.get(uid, 0) >= cfg.daily_cap:
            push, hold = False, 'capped'
        messages.append(push_engine.Message(
            user_id=uid, title=title, body=body, target_type=ttype, target_id=tid,
            url=f'/app/reader/{tid}/?src=push', push=push, hold=hold))
    return messages, sizes


def preview(resource_ids) -> dict:
    """What announcing these resources would do, without sending anything."""
    cfg = get_settings()
    resources = list(Resource.objects.filter(pk__in=list(resource_ids), approval_status='approved'))
    messages, sizes = _build_messages(resources, respect_caps=False, cfg=cfg)
    from .models import FCMToken
    uids = [m.user_id for m in messages]
    with_device = set()
    for i in range(0, len(uids), 500):
        with_device.update(FCMToken.objects.filter(user_id__in=uids[i:i + 500]).values_list('user_id', flat=True))
    sample = None
    if messages:
        m = max(messages, key=lambda m: len(m.body))
        sample = {'title': m.title, 'body': m.body}
    return {
        'resources': len(resources), 'people': len(messages), 'devices_people': len(with_device),
        'inbox_only': len(messages) - len(with_device),
        'would_send_as_singles': sum(sizes.values()),
        'sizes': sizes, 'sample': sample,
    }


def _finish(alerts, resources_by_id, sizes, campaign, state):
    now = push_engine.now_ms()
    for a in alerts:
        size = sizes.get(a.resource_id, 0)
        if size:
            ResourceAlert.objects.filter(pk=a.pk).update(
                state=state, processed_at=now, audience_size=size, campaign_id=campaign.id if campaign else '', reason='')
        else:
            ResourceAlert.objects.filter(pk=a.pk).update(state='skipped', reason='no_audience', processed_at=now)


def announce(resource_ids, created_by=None, sync=False) -> PushCampaign | None:
    """Staff announce uploads by hand: same audience and digest rules, no cap, no quiet hours."""
    cfg = get_settings()
    resources = list(Resource.objects.filter(pk__in=list(resource_ids), approval_status='approved'))
    if not resources:
        return None
    messages, sizes = _build_messages(resources, respect_caps=False, cfg=cfg)
    campaign = push_engine.create_campaign(
        kind='library', title=f'{len(resources)} library upload{"s" if len(resources) != 1 else ""}',
        body='', target_type='resource', audience_label=f'Matched by class and subject, {len(messages)} people',
        resource_ids=[r.id for r in resources], created_by=created_by, note='Announced by hand')
    alerts = []
    for r in resources:
        a, _ = ResourceAlert.objects.get_or_create(resource=r, defaults={'queued_at': push_engine.now_ms()})
        alerts.append(a)

    def run():
        try:
            push_engine.deliver(campaign, messages)
        finally:
            _finish(alerts, {r.id: r for r in resources}, sizes, campaign, 'manual')

    if sync:
        run()
        campaign.refresh_from_db()
    else:
        push_engine.run_in_background(lambda: run())
    return campaign


def unannounced_ids(limit: int = 2000) -> list[str]:
    """Live library resources the autopilot never saw (uploaded before it shipped) or skipped as a bulk upload."""
    return list(Resource.objects.filter(approval_status='approved', is_lead=True, alert__isnull=True)
                .order_by('-added_at').values_list('id', flat=True)[:limit])


def announce_unnotified(created_by=None, sync=False) -> PushCampaign | None:
    """One tap batch mode: every never announced live resource, one digest per person."""
    ids = unannounced_ids()
    return announce(ids, created_by=created_by, sync=sync) if ids else None


def flush_pending(force: bool = False, now_ms: int | None = None) -> PushCampaign | None:
    """One autopilot round. Safe to call from many workers: rows are claimed atomically."""
    now = now_ms or push_engine.now_ms()
    cfg = get_settings()
    pending = list(ResourceAlert.objects.filter(state='pending').order_by('queued_at'))
    if not pending:
        return None
    if not cfg.autopilot_enabled and not force:
        ResourceAlert.objects.filter(pk__in=[a.pk for a in pending], state='pending').update(
            state='skipped', reason='autopilot_off', processed_at=now)
        return None
    if not force:
        if in_quiet_hours(now, cfg):
            return None
        newest, oldest = max(a.queued_at for a in pending), min(a.queued_at for a in pending)
        if now - newest < cfg.settle_minutes * MIN and now - oldest < cfg.max_wait_minutes * MIN:
            return None
    token = f'run:{uuid.uuid4().hex[:12]}'
    ResourceAlert.objects.filter(pk__in=[a.pk for a in pending], state='pending').update(state='sending', reason=token)
    claimed = list(ResourceAlert.objects.filter(state='sending', reason=token).select_related('resource'))
    if not claimed:
        return None
    live, dead = [], []
    for a in claimed:
        r = a.resource
        if r.approval_status != 'approved' or not r.is_lead:
            dead.append((a, 'gone'))
        elif now - (r.added_at or a.queued_at) > STALE_MS and now - a.queued_at > STALE_MS:
            dead.append((a, 'stale'))
        elif r.is_paid and not cfg.include_paid:
            dead.append((a, 'paid'))
        else:
            live.append(a)
    for a, why in dead:
        ResourceAlert.objects.filter(pk=a.pk).update(state='skipped', reason=why, processed_at=now)
    if not live:
        return None
    resources = [a.resource for a in live]
    messages, sizes = _build_messages(resources, respect_caps=True, cfg=cfg)
    if not messages:
        _finish(live, {}, sizes, None, 'sent')
        return None
    campaign = push_engine.create_campaign(
        kind='autopilot', title=f'{len(resources)} new resource{"s" if len(resources) != 1 else ""}', body='',
        target_type='resource', audience_label=f'Matched by class and subject, {len(messages)} people',
        resource_ids=[r.id for r in resources], note='Autopilot')
    try:
        push_engine.deliver(campaign, messages)
    finally:
        _finish(live, {r.id: r for r in resources}, sizes, campaign, 'sent')
    campaign.refresh_from_db()
    return campaign


def tick() -> dict:
    """Everything time based: due scheduled broadcasts and the autopilot round. Cron or worker calls this."""
    out = {'scheduled': 0, 'autopilot': None}
    try:
        out['scheduled'] = push_engine.run_due_scheduled()
        c = flush_pending()
        out['autopilot'] = c.id if c else None
    except Exception:  # noqa: BLE001
        logger.exception('push tick failed')
    return out


# ---- background worker (best effort; `manage.py push_tick` from cron is the safety net) ----

_worker_lock = threading.Lock()
_worker = None


def _testing() -> bool:
    return 'test' in sys.argv or bool(getattr(settings, 'TESTING', False))


def ensure_worker():
    global _worker
    if _testing():
        return
    with _worker_lock:
        if _worker and _worker.is_alive():
            return

        def loop():
            from django.db import close_old_connections
            idle = 0
            while idle < 30:
                close_old_connections()
                try:
                    tick()
                    busy = ResourceAlert.objects.filter(state='pending').exists() or \
                        PushCampaign.objects.filter(status='scheduled').exists()
                except Exception:  # noqa: BLE001
                    busy = False
                idle = 0 if busy else idle + 1
                time.sleep(20)
            close_old_connections()

        _worker = threading.Thread(target=loop, daemon=True, name='resource-alerts')
        _worker.start()


# ---- signal wiring -------------------------------------------------------------

def _remember_status(sender, instance, **kwargs):
    prev = ''
    if instance.pk:
        prev = Resource.objects.filter(pk=instance.pk).values_list('approval_status', flat=True).first() or ''
    instance._prev_approval = prev


def _on_saved(sender, instance, created, **kwargs):
    if getattr(instance, '_skip_alert', False) or kwargs.get('raw'):
        return
    if instance.approval_status != 'approved' or not instance.is_lead:
        return
    if created or getattr(instance, '_prev_approval', '') != 'approved':
        try:
            enqueue(instance)
        except Exception:  # noqa: BLE001
            logger.exception('resource alert enqueue failed')


def register_hooks():
    pre_save.connect(_remember_status, sender=Resource, dispatch_uid='resource_alert_pre')
    post_save.connect(_on_saved, sender=Resource, dispatch_uid='resource_alert_post')
