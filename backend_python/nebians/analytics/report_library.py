"""Admin-only library section of the Analytics page: what people open, read and download.

Fed by `ResourceReach` / `ResourceImpression` (api/resource_reach.py). Aggregates only; nobody is named
(uploaders are shown by display name because they chose to publish under it).
"""
from __future__ import annotations

from collections import Counter

from django.db.models import Count, Q, Sum

from .report_devices import DEVICE_LABEL, _rank

SURFACE_LABEL = {'': 'Unknown', 'library': 'Library', 'search': 'Search', 'subject': 'Subject page', 'profile': 'Profile',
                 'share': 'Shared link', 'direct': 'Direct', 'notification': 'Notification', 'related': 'Related',
                 'home': 'Home'}


def _pct(a, b):
    return round(a * 100.0 / b, 1) if b else None


def build(rng: dict, source: str = 'all') -> dict:
    from api.models import Resource, ResourceImpression, ResourceReach

    start, end = rng['start'], rng['end']
    reach = ResourceReach.objects.filter(first_at__gte=start, first_at__lt=end, is_owner=False)
    if source in ('web', 'app'):
        reach = reach.filter(source=source)
    agg = reach.aggregate(
        views=Count('id'),
        people=Count('viewer', distinct=True),
        reads=Count('id', filter=Q(read=True)),
        downloads=Count('id', filter=Q(downloaded=True)),
        shares=Count('id', filter=Q(shared=True)),
        from_push=Count('id', filter=Q(surface='notification')),
        dwell_total=Sum('dwell_ms', filter=Q(dwell_ms__gt=0)),
        dwell_samples=Count('id', filter=Q(dwell_ms__gt=0)),
    )
    views = agg['views'] or 0
    people = agg['people'] or 0
    reads = agg['reads'] or 0
    downloads = agg['downloads'] or 0
    shares = agg['shares'] or 0
    from_push = agg['from_push'] or 0
    avg_dwell = round((agg['dwell_total'] or 0) / agg['dwell_samples'] / 1000.0, 1) if agg['dwell_samples'] else 0.0

    days = {r['day'] for r in reach.values('day').distinct()}
    imp = 0
    if days:
        qs = ResourceImpression.objects.filter(day__in=days)
        if source in ('web', 'app'):
            qs = qs.filter(source=source)
        imp = qs.aggregate(n=Sum('count'))['n'] or 0

    top_rows = list(
        reach.values('resource_id')
        .annotate(
            views=Count('id'),
            people=Count('viewer', distinct=True),
            dwell=Sum('dwell_ms'),
            reads=Count('id', filter=Q(read=True)),
            downloads=Count('id', filter=Q(downloaded=True)),
            push=Count('id', filter=Q(surface='notification')),
        )
        .order_by('-views')[:10]
    )
    top_ids = [row['resource_id'] for row in top_rows]
    resources_by_id = {
        r.pk: r
        for r in Resource.objects.filter(pk__in=top_ids).select_related('uploaded_by')
    } if top_ids else {}

    top = []
    for row in top_rows:
        r = resources_by_id.get(row['resource_id'])
        if not r:
            continue
        top.append({
            'id': r.pk, 'title': r.title[:80], 'subject': r.subject[:40], 'level': r.grade_level,
            'views': row['views'], 'people': row['people'], 'reads': row['reads'],
            'downloads': row['downloads'], 'push': row['push'],
            'by': (r.uploaded_by.username if r.uploaded_by_id else (r.author_name or 'Admin'))[:30],
        })

    subject_views = Counter()
    for rid, n in reach.values_list('resource_id').annotate(n=Count('id')):
        subject_views[rid] = n
    subj = Counter()
    for rid, subject in Resource.objects.filter(pk__in=list(subject_views)[:2000]).values_list('pk', 'subject'):
        subj[(subject or 'Other').split(',')[0][:40]] += subject_views[rid]

    return {
        'views': views, 'people': people, 'reads': reads, 'downloads': downloads, 'shares': shares,
        'impressions': imp, 'ctr': _pct(views, imp), 'read_rate': _pct(reads, views),
        'download_rate': _pct(downloads, views), 'share_rate': _pct(shares, views),
        'avg_dwell_sec': avg_dwell, 'from_push': from_push, 'push_share': _pct(from_push, views),
        'top': top,
        'surfaces': _rank(Counter(reach.values_list('surface', flat=True)), SURFACE_LABEL),
        'devices': _rank(Counter(reach.values_list('device_class', flat=True)), DEVICE_LABEL),
        'classes': _rank(Counter(c or 'Not set' for c in reach.values_list('class_level', flat=True))),
        'subjects': _rank(subj),
        'sources': _rank(Counter(reach.values_list('source', flat=True)), {'web': 'Website', 'app': 'Android app'}),
    }
