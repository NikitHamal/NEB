"""Admin: push notifications. Compose, history with analytics, and the library autopilot.

The model, sender and numbers live in api/push_engine.py, api/push_stats.py and
api/resource_alerts.py; this module only reads forms and renders.
"""
import datetime
import re
from zoneinfo import ZoneInfo

from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from api import push_audience, push_engine, push_stats, resource_alerts
from api.models import (FCMToken, Post, PushCampaign, PushDelivery, PushSettings, Resource,
                        ResourceAlert, User)

from .view_helpers import _require_staff_admin

TITLE_MAX = 65
BODY_MAX = 240
CLASS_OPTIONS = (
    ('Class 8', 'Class 8'), ('Class 9', 'Class 9'), ('Class 10 / SEE', 'Class 10 / SEE'), ('11', 'Class 11'),
    ('12', 'Class 12'), ('+2 Passout', '+2 Passout'), ('Diploma', 'Diploma'), ('Bachelors', 'Bachelors'),
    ('Masters', 'Masters'), ('PhD', 'PhD'), ('Teacher', 'Teacher'), ('Other', 'Other'),
)
DESTINATIONS = (('none', 'Just the message'), ('library', 'Library'), ('resource', 'One resource'), ('post', 'One forum post'))


def _tabs(active):
    return {'push_tab': active}


def _filters_from(source):
    return push_audience.clean(source)


def _resolve_destination(data):
    """(target_type, target_id, url, error) from the composer's destination fields."""
    dest = (data.get('dest') or 'none').strip()
    ref = (data.get('dest_id') or '').strip()
    if dest == 'library':
        return 'library', '', '/app/library/', ''
    if dest == 'resource':
        m = re.search(r'/reader/([^/?#]+)|/resource/([^/?#]+)', ref)
        rid = (m.group(1) or m.group(2)) if m else ref
        if not rid or not Resource.objects.filter(pk=rid).exists():
            return '', '', '', 'That resource was not found. Paste its id or its reader link.'
        return 'resource', rid, f'/reader/{rid}/', ''
    if dest == 'post':
        m = re.search(r'/post/([^/?#]+)', ref)
        pid = m.group(1) if m else ref
        if not pid or not Post.objects.filter(pk=pid).exists():
            return '', '', '', 'That post was not found. Paste its id or its link.'
        return 'post', pid, f'/forum/post/{pid}/', ''
    return 'system', '', '', ''


def _local_to_ms(value):
    """`datetime-local` text in Nepal time to epoch ms; 0 when blank or malformed."""
    if not value:
        return 0
    try:
        dt = datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M').replace(tzinfo=ZoneInfo(settings.TIME_ZONE))
    except ValueError:
        return 0
    return int(dt.timestamp() * 1000)


def admin_push_notifications(request):
    """Compose. GET with count_only=1 (or XHR) answers the live audience numbers as JSON."""
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    resource_alerts.tick()
    src = request.POST if request.method == 'POST' else request.GET
    filters = _filters_from(src)
    counts = push_audience.counts(filters)

    if request.GET.get('count_only') == '1' or (
            request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'GET'):
        return JsonResponse({'matching_users': counts['users'], 'matching_tokens': counts['devices'], **counts})

    title = (request.POST.get('title') or '').strip()
    body = (request.POST.get('body') or '').strip()
    error = None
    if request.method == 'POST':
        action = request.POST.get('action') or 'send'
        ttype, tid, url, derr = _resolve_destination(request.POST)
        also_inbox = request.POST.get('also_inbox') == '1'
        send_at = _local_to_ms(request.POST.get('send_at', ''))
        if not title or not body:
            error = 'A title and a message are both needed.'
        elif len(title) > TITLE_MAX or len(body) > BODY_MAX:
            error = f'Keep the title under {TITLE_MAX} and the message under {BODY_MAX} characters so phones do not cut it.'
        elif derr:
            error = derr
        elif send_at and send_at <= push_engine.now_ms() + 60000:
            error = 'Pick a time in the future, or clear it to send now.'
        elif action == 'test':
            me = _current_admin(request)
            tokens = FCMToken.objects.filter(user_id=me.id).count() if me else 0
            camp = push_engine.send_manual(
                title=title, body=body, url=url, target_type=ttype, target_id=tid,
                filters={'usernames_or_ids': me.id if me else '-'}, also_inbox=True, created_by=me, kind='test', sync=True)
            return redirect(f"{reverse('web:admin_push_detail', args=[camp.id])}?test=1&dev={tokens}")
        elif counts['users'] == 0:
            error = 'No one matches these filters.'
        else:
            me = _current_admin(request)
            camp = push_engine.send_manual(
                title=title, body=body, url=url, target_type=ttype, target_id=tid, filters=filters,
                also_inbox=also_inbox, created_by=me, scheduled_at=send_at, sync=False)
            return redirect('web:admin_push_detail', campaign_id=camp.id)

    recent = list(PushCampaign.objects.exclude(status='canceled').order_by('-created_at')[:4])
    return render(request, 'admin_panel/push_notifications.html', {
        'is_admin': True, 'active_page': 'push_notifications', **_tabs('compose'),
        'counts': counts, 'filters': filters, 'error_message': error,
        'title_val': title, 'body_val': body, 'title_max': TITLE_MAX, 'body_max': BODY_MAX,
        'class_options': CLASS_OPTIONS, 'roles': push_audience.ROLES, 'devices_choices': push_audience.DEVICE_CHOICES,
        'destinations': DESTINATIONS, 'dest': request.POST.get('dest', 'none'), 'dest_id': request.POST.get('dest_id', ''),
        'also_inbox': request.POST.get('also_inbox', '1') == '1', 'send_at': request.POST.get('send_at', ''),
        'recent': recent,
        # Back-compat names used by older tests and the live counter
        'matching_users': counts['users'], 'matching_tokens': counts['devices'],
        'class_level': filters.get('class_level', ''),
    })


def _current_admin(request):
    from .view_helpers import _get_user_id
    uid = _get_user_id(request)
    return User.objects.filter(pk=uid).first() if uid else None


def admin_push_history(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    resource_alerts.tick()
    kind = request.GET.get('kind', '')
    kind = kind if kind in push_stats.KIND_LABEL else ''
    try:
        days = int(request.GET.get('days', 30))
    except ValueError:
        days = 30
    ov = push_stats.overview(days=days, kind=kind)
    qs = PushCampaign.objects.all()
    if kind:
        qs = qs.filter(kind=kind)
    page = Paginator(qs, 25).get_page(request.GET.get('page'))
    ids = [c.id for c in page.object_list]
    opened = dict(PushDelivery.objects.filter(campaign_id__in=ids).exclude(opened_at=0)
                  .values_list('campaign_id').annotate(n=Count('id')))
    rows = []
    for c in page.object_list:
        o = opened.get(c.id, 0)
        rows.append({
            'c': c, 'kind_label': push_stats.KIND_LABEL.get(c.kind, c.kind), 'opens': o,
            'open_rate': round(o * 100.0 / c.users_targeted, 1) if c.users_targeted else None,
            'delivery': round(c.devices_accepted * 100.0 / c.devices_targeted, 1) if c.devices_targeted else None,
        })
    max_bar = max([max(s['accepted'], s['opens'], 1) for s in ov['series']] + [1])
    for s in ov['series']:
        s['ha'] = max(2, round(s['accepted'] * 100 / max_bar)) if s['accepted'] else 2
        s['ho'] = max(2, round(s['opens'] * 100 / max_bar)) if s['opens'] else 2
    hmax = max(ov['bestHours']['hourly'] + [1])
    ov['bestHours']['bars'] = [{'i': i, 'n': n, 'h': max(3, round(n * 100 / hmax)) if n else 3} for i, n in enumerate(ov['bestHours']['hourly'])]
    return render(request, 'admin_panel/push_history.html', {
        'is_admin': True, 'active_page': 'push_notifications', **_tabs('history'),
        'ov': ov, 'rows': rows, 'page': page, 'kind': kind, 'days': ov['days'], 'max_bar': max_bar,
        'kinds': [('', 'All')] + [(k, v) for k, v in push_stats.KIND_LABEL.items()],
    })


def admin_push_detail(request, campaign_id):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    campaign = get_object_or_404(PushCampaign, pk=campaign_id)
    if request.method == 'POST' and request.POST.get('action') == 'cancel' and campaign.status == 'scheduled':
        PushCampaign.objects.filter(pk=campaign.pk, status='scheduled').update(status='canceled')
        return redirect('web:admin_push_detail', campaign_id=campaign.id)
    d = push_stats.campaign_detail(campaign)
    max_h = max(d['first48'] + [1])
    max_day = max(d['hoursOfDay'] + [1])
    return render(request, 'admin_panel/push_detail.html', {
        'is_admin': True, 'active_page': 'push_notifications', **_tabs('history'),
        'c': campaign, 'd': d, 'kind_label': push_stats.KIND_LABEL.get(campaign.kind, campaign.kind),
        'max_h': max_h, 'max_day': max_day, 'live': campaign.status == 'sending',
        'test_sent': request.GET.get('test') == '1', 'test_devices': request.GET.get('dev', ''),
        'sender': campaign.created_by.username if campaign.created_by_id else 'Autopilot',
        'first48_bars': [{'i': i, 'n': n, 'h': max(3, round(n * 100 / max_h)) if n else 3} for i, n in enumerate(d['first48'])],
        'day_bars': [{'i': i, 'n': n, 'h': max(3, round(n * 100 / max_day)) if n else 3, 'label': push_stats._hour_label(i)}
                     for i, n in enumerate(d['hoursOfDay'])],
    })


def admin_push_autopilot(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return redirect_response
    cfg = resource_alerts.get_settings()
    flash = ''
    if request.method == 'POST':
        action = request.POST.get('action', '')
        if action == 'settings':
            def num(name, lo, hi, default):
                try:
                    return max(lo, min(hi, int(request.POST.get(name, default))))
                except ValueError:
                    return default
            cfg.autopilot_enabled = request.POST.get('autopilot_enabled') == '1'
            cfg.include_paid = request.POST.get('include_paid') == '1'
            cfg.daily_cap = num('daily_cap', 1, 6, cfg.daily_cap)
            cfg.quiet_start_hour = num('quiet_start_hour', 0, 23, cfg.quiet_start_hour)
            cfg.quiet_end_hour = num('quiet_end_hour', 0, 23, cfg.quiet_end_hour)
            cfg.settle_minutes = num('settle_minutes', 1, 120, cfg.settle_minutes)
            cfg.max_wait_minutes = max(cfg.settle_minutes, num('max_wait_minutes', 5, 720, cfg.max_wait_minutes))
            cfg.updated_at = push_engine.now_ms()
            cfg.save()
            flash = 'Autopilot settings saved.'
        elif action == 'run_now':
            camp = resource_alerts.flush_pending(force=True)
            if camp:
                return redirect('web:admin_push_detail', campaign_id=camp.id)
            flash = 'Nothing in the queue matched anyone.'
        elif action == 'skip':
            ResourceAlert.objects.filter(pk=request.POST.get('alert_id') or 0, state='pending').update(
                state='skipped', reason='skipped_by_staff', processed_at=push_engine.now_ms())
            flash = 'Removed from the queue.'
        elif action == 'announce':
            ids = [i for i in request.POST.getlist('resource_ids') if i][:400]
            camp = resource_alerts.announce(ids, created_by=_current_admin(request)) if ids else None
            if camp:
                return redirect('web:admin_push_detail', campaign_id=camp.id)
            flash = 'Pick at least one live resource.'
    resource_alerts.tick()

    pending = list(ResourceAlert.objects.filter(state='pending').select_related('resource').order_by('queued_at')[:30])
    now = push_engine.now_ms()
    quiet_now = resource_alerts.in_quiet_hours(now, cfg)
    show = request.GET.get('show', 'new')
    base = Resource.objects.filter(approval_status='approved', is_lead=True).select_related('alert')
    if show == 'new':
        base = base.filter(alert__isnull=True)
    library = list(base.order_by('-added_at')[:300])
    for r in library:
        a = getattr(r, 'alert', None)
        r.alert_state = a.state if a else ''
        r.alert_reason = push_stats.SKIP_LABEL.get(a.reason, a.reason) if a and a.state == 'skipped' else ''
    eligible = User.objects.filter(is_bot=False, is_banned=False, notify_new_resources=True).exclude(class_level__isnull=True).exclude(class_level='').exclude(subjects__isnull=True).exclude(subjects='')
    members = User.objects.filter(is_bot=False, is_banned=False)
    recent = list(PushCampaign.objects.filter(kind__in=('autopilot', 'library')).order_by('-created_at')[:8])
    skipped = {}
    for reason in ResourceAlert.objects.filter(state='skipped', processed_at__gte=now - 30 * 86400000).values_list('reason', flat=True):
        skipped[reason] = skipped.get(reason, 0) + 1
    return render(request, 'admin_panel/push_autopilot.html', {
        'is_admin': True, 'active_page': 'push_notifications', **_tabs('autopilot'),
        'cfg': cfg, 'flash': flash, 'pending': pending, 'quiet_now': quiet_now, 'library': library, 'show': show,
        'stats': {
            'members': members.count(), 'eligible': eligible.count(),
            'opted_out': members.filter(notify_new_resources=False).count(),
            'sent_30': ResourceAlert.objects.filter(state='sent', processed_at__gte=now - 30 * 86400000).count(),
            'manual_30': ResourceAlert.objects.filter(state='manual', processed_at__gte=now - 30 * 86400000).count(),
            'unannounced': Resource.objects.filter(approval_status='approved', is_lead=True, alert__isnull=True).count(),
        },
        'skipped': [{'label': push_stats.SKIP_LABEL.get(k, k.replace('_', ' ').capitalize()), 'n': v} for k, v in skipped.items()],
        'recent': recent, 'hours': list(range(24)),
        'settle': cfg.settle_minutes,
    })


@require_POST
def admin_push_autopilot_preview(request):
    redirect_response = _require_staff_admin(request)
    if redirect_response:
        return JsonResponse({'error': 'Not allowed'}, status=403)
    import json
    try:
        ids = json.loads(request.body or b'{}').get('ids', [])
    except ValueError:
        ids = []
    ids = [str(i) for i in ids][:400]
    return JsonResponse(resource_alerts.preview(ids))
