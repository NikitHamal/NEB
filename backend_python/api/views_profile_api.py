"""JSON API for profile tab feeds (mobile parity with the legacy ajax views).

Response envelopes and query params intentionally match the ajax originals so
the mobile client only changes base URLs. Serializers are reused from
web.view_helpers via function-level imports (same cycle-avoidance precedent
as api.serializers).
"""
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from .models import Post, Reply, Resource, User
from .security import get_user_by_auth_token


def _resolve_viewer(request):
    """Anonymous allowed; Bearer token or DRF-authenticated user when present."""
    req_user = getattr(request, 'user', None)
    if req_user is not None and getattr(req_user, 'is_authenticated', False) \
            and not getattr(req_user, 'is_bot', False):
        return req_user
    auth_header = request.headers.get('Authorization', '')
    if auth_header.startswith('Bearer '):
        try:
            u = get_user_by_auth_token(auth_header[7:].strip())
            if not u.is_locked:
                return u
        except Exception:  # noqa: BLE001 - invalid/expired tokens resolve to anonymous
            pass
    return None


def _page_bounds(request):
    try:
        offset = max(0, int(request.GET.get('offset', 0)))
    except (TypeError, ValueError):
        offset = 0
    try:
        limit = min(25, max(1, int(request.GET.get('limit', 10))))
    except (TypeError, ValueError):
        limit = 10
    return offset, limit


def _load_profile(username, request):
    """Returns (profile_user, viewer_user, error_response)."""
    try:
        profile_user = User.objects.get(username=username)
    except User.DoesNotExist:
        return None, None, JsonResponse({'error': 'User not found'}, status=404)
    viewer_user = _resolve_viewer(request)
    from web.view_helpers import _can_view_locked_profile
    if not _can_view_locked_profile(viewer_user, profile_user):
        return None, None, JsonResponse({'error': 'This profile is private'}, status=403)
    return profile_user, viewer_user, None


@require_GET
def user_profile_activity_api(request, username):
    from web.view_helpers import _serialize_posts
    profile_user, viewer_user, err = _load_profile(username, request)
    if err:
        return err
    offset, limit = _page_bounds(request)
    viewer_id = viewer_user.pk if viewer_user else None
    qs = Post.objects.select_related('user').filter(
        user_id=profile_user.id, is_anonymous=False
    ).order_by('-created_at')[offset:offset + limit]
    total_count = Post.objects.filter(user_id=profile_user.id, is_anonymous=False).count()
    posts = _serialize_posts(qs, viewer_id)
    return JsonResponse({
        'posts': posts,
        'has_more': (offset + len(posts)) < total_count,
        'total_count': total_count,
    })


@require_GET
def user_profile_replies_api(request, username):
    from web.view_helpers import _serialize_replies
    profile_user, viewer_user, err = _load_profile(username, request)
    if err:
        return err
    offset, limit = _page_bounds(request)
    viewer_id = viewer_user.pk if viewer_user else None
    qs = Reply.objects.select_related('user', 'post').filter(
        user_id=profile_user.id, is_anonymous=False, is_archived=False
    ).order_by('-created_at')[offset:offset + limit]
    total_count = Reply.objects.filter(
        user_id=profile_user.id, is_anonymous=False, is_archived=False
    ).count()
    replies = _serialize_replies(qs, viewer_id)
    return JsonResponse({
        'replies': replies,
        'has_more': (offset + len(replies)) < total_count,
        'total_count': total_count,
    })


@require_GET
def user_profile_resources_api(request, username):
    from web.view_helpers import _serialize_resources
    profile_user, viewer_user, err = _load_profile(username, request)
    if err:
        return err
    offset, limit = _page_bounds(request)
    is_self = bool(viewer_user and viewer_user.pk == profile_user.pk)
    if is_self:
        # Owners see their pending/rejected uploads; the public does not.
        base_qs = Resource.objects.filter(uploaded_by_id=profile_user.id, is_lead=True)
    else:
        base_qs = Resource.objects.filter(
            uploaded_by_id=profile_user.id, approval_status='approved', is_lead=True
        )
    rows = list(base_qs.order_by('-added_at')[offset:offset + limit])
    total_count = base_qs.count()
    return JsonResponse({
        'resources': _serialize_resources(rows),
        'has_more': (offset + len(rows)) < total_count,
        'total_count': total_count,
    })
