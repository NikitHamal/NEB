"""Public JSON API for news/announcements (mobile app parity).

Reads are public; view tracking is a separate POST so scrapers and cached
fetches no longer inflate view counts.
"""
from django.db.models import F
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from .models import Announcement
from .news_serializers import serialize_announcement

PAGE_SIZE = 12
_MAX_TRACKED_SLUGS = 200


@require_GET
def news_list_api(request):
    qs = Announcement.objects.select_related('author').filter(status='published')
    category = (request.GET.get('category') or '').strip()
    if category:
        qs = qs.filter(category=category)
    try:
        page = max(1, int(request.GET.get('page', '1')))
    except (TypeError, ValueError):
        page = 1
    offset = (page - 1) * PAGE_SIZE
    rows = list(qs.order_by('-is_pinned', '-published_at')[offset:offset + PAGE_SIZE + 1])
    has_more = len(rows) > PAGE_SIZE
    return JsonResponse({
        'ok': True,
        'items': [serialize_announcement(a) for a in rows[:PAGE_SIZE]],
        'page': page,
        'has_more': has_more,
    })


@require_GET
def news_detail_api(request, slug):
    try:
        a = Announcement.objects.select_related('author').get(slug=slug, status='published')
    except Announcement.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)
    related = Announcement.objects.filter(
        status='published', category=a.category
    ).exclude(pk=a.pk).select_related('author').order_by('-published_at')[:4]
    return JsonResponse({
        'ok': True,
        'item': serialize_announcement(a, include_content=True),
        'related': [serialize_announcement(r) for r in related],
    })


@csrf_exempt
@require_POST
def news_track_view(request, slug):
    """Count one view per real article open.

    Cookie clients (web beacon) are de-duplicated per session; app clients
    (bearer, no session) count each explicit call.
    """
    try:
        a = Announcement.objects.only('id').get(slug=slug, status='published')
    except Announcement.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)

    seen = request.session.get('viewed_news_slugs', [])
    if slug in seen:
        return JsonResponse({'ok': True, 'counted': False})

    Announcement.objects.filter(pk=a.pk).update(view_count=F('view_count') + 1)
    seen.append(slug)
    request.session['viewed_news_slugs'] = seen[-_MAX_TRACKED_SLUGS:]
    return JsonResponse({'ok': True, 'counted': True})
