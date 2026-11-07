"""Who a broadcast reaches. One filter vocabulary shared by the admin composer (live counts),
the sender and the campaign record, so the number staff see is the number that gets sent.

Filters are a plain dict (stored on the campaign as JSON). Every key is optional.
"""
from __future__ import annotations

import datetime
import time
from collections import Counter

from django.db.models import Q

from .models import FCMToken, User

FILTER_KEYS = ('class_level', 'gender', 'min_age', 'max_age', 'pradesh', 'district', 'school',
               'role', 'subject', 'joined_days', 'active_days', 'inactive_days', 'device',
               'usernames_or_ids')
ROLES = (('student', 'Students'), ('teacher', 'Teachers'), ('institution', 'Institutions'), ('explorer', 'Explorers'))
DEVICE_CHOICES = (('', 'Everyone'), ('with', 'Has the app'), ('without', 'Inbox only'))
DAY_MS = 86400000


def clean(raw) -> dict:
    """Keep known keys, trimmed strings only, drop blanks."""
    out = {}
    for key in FILTER_KEYS:
        value = raw.get(key, '') if hasattr(raw, 'get') else ''
        value = str(value or '').strip()
        if value:
            out[key] = value[:500]
    return out


def _int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def queryset(filters: dict):
    f = clean(filters)
    qs = User.objects.filter(is_bot=False, is_banned=False)
    if f.get('class_level'):
        qs = qs.filter(class_level__iexact=f['class_level'])
    if f.get('gender'):
        qs = qs.filter(gender__iexact=f['gender'])
    if f.get('pradesh'):
        qs = qs.filter(pradesh__icontains=f['pradesh'])
    if f.get('district'):
        qs = qs.filter(district__icontains=f['district'])
    if f.get('school'):
        qs = qs.filter(school__icontains=f['school'])
    if f.get('role') in dict(ROLES):
        qs = qs.filter(role=f['role'])
    if f.get('subject'):
        qs = qs.filter(subjects__icontains=f['subject'])
    today = datetime.date.today()
    min_age, max_age = _int(f.get('min_age')), _int(f.get('max_age'))
    if min_age is not None:
        qs = qs.filter(dob__lte=f"{today.year - min_age:04d}-{today.month:02d}-{today.day:02d}").exclude(dob='')
    if max_age is not None:
        qs = qs.filter(dob__gte=f"{today.year - max_age - 1:04d}-{today.month:02d}-{today.day:02d}").exclude(dob='')
    now = int(time.time() * 1000)
    joined, active, inactive = _int(f.get('joined_days')), _int(f.get('active_days')), _int(f.get('inactive_days'))
    if joined:
        qs = qs.filter(created_at__gte=now - joined * DAY_MS)
    if active:
        qs = qs.filter(last_active__gte=now - active * DAY_MS)
    if inactive:
        qs = qs.filter(last_active__lt=now - inactive * DAY_MS)
    if f.get('usernames_or_ids'):
        items = [x.strip() for x in f['usernames_or_ids'].split(',') if x.strip()]
        if items:
            qs = qs.filter(Q(username__in=items) | Q(id__in=items))
    if f.get('device') == 'with':
        qs = qs.filter(fcm_tokens__isnull=False).distinct()
    elif f.get('device') == 'without':
        qs = qs.filter(fcm_tokens__isnull=True)
    return qs


def describe(filters: dict) -> str:
    """Short label for history rows: 'Class 10 / SEE, Bagmati, active 30 days'."""
    f = clean(filters)
    if not f:
        return 'Everyone'
    parts = []
    if f.get('usernames_or_ids'):
        n = len([x for x in f['usernames_or_ids'].split(',') if x.strip()])
        parts.append(f'{n} chosen {"person" if n == 1 else "people"}')
    if f.get('class_level'):
        parts.append(f['class_level'] if not f['class_level'].isdigit() else f"Class {f['class_level']}")
    if f.get('role'):
        parts.append(dict(ROLES).get(f['role'], f['role']))
    if f.get('subject'):
        parts.append(f['subject'])
    if f.get('gender'):
        parts.append(f['gender'])
    if f.get('min_age') or f.get('max_age'):
        parts.append(f"age {f.get('min_age', '0')} to {f.get('max_age', 'any')}")
    for key in ('pradesh', 'district', 'school'):
        if f.get(key):
            parts.append(f[key])
    if f.get('joined_days'):
        parts.append(f"joined in {f['joined_days']} days")
    if f.get('active_days'):
        parts.append(f"active in {f['active_days']} days")
    if f.get('inactive_days'):
        parts.append(f"away {f['inactive_days']} days")
    if f.get('device') == 'with':
        parts.append('has the app')
    elif f.get('device') == 'without':
        parts.append('inbox only')
    return ', '.join(parts)[:240] or 'Everyone'


def counts(filters: dict) -> dict:
    """Live numbers for the composer: people, people with a device, devices, top classes."""
    qs = queryset(filters)
    ids = list(qs.values_list('id', flat=True)[:50000])
    users = len(ids)
    device_users, devices = 0, 0
    for i in range(0, len(ids), 500):
        chunk = ids[i:i + 500]
        rows = FCMToken.objects.filter(user_id__in=chunk).values_list('user_id', flat=True)
        per = Counter(rows)
        device_users += len(per)
        devices += sum(per.values())
    classes = Counter(qs.exclude(class_level__isnull=True).exclude(class_level='')
                      .values_list('class_level', flat=True)[:50000])
    return {
        'users': users, 'device_users': device_users, 'devices': devices,
        'inbox_only': max(0, users - device_users),
        'classes': [{'label': k, 'count': v} for k, v in classes.most_common(5)],
    }
