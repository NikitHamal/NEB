"""Views Notifications extracted from views.py with enhanced UI/UX and pagination."""
from datetime import datetime, timezone
import json
import time

from django.core.cache import cache
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils.html import escape
from django.views.decorators.http import require_POST

from .view_helpers import _avatar_url, _counters, _ctx, _get_user_id, _user_badge_info
from api.models import Notification, User
from api.notifications import get_notification_url


def _format_compact_time(created_at_ms):
    """Formats timestamp into compact string like '2m', '18m', '1h', 'Mon', 'Jul 23'."""
    if not created_at_ms:
        return ''
    try:
        ts = int(created_at_ms) / 1000
    except (ValueError, TypeError):
        return ''
    now = time.time()
    diff = max(0, now - ts)
    if diff < 60:
        return 'just now'
    if diff < 3600:
        return f'{int(diff / 60)}m'
    if diff < 86400:
        return f'{int(diff / 3600)}h'
    if diff < 604800:
        dt = datetime.fromtimestamp(ts, tz=timezone.utc)
        return dt.strftime('%a')
    if diff < 2592000:
        return f'{int(diff / 86400)}d'
    dt = datetime.fromtimestamp(ts, tz=timezone.utc)
    return dt.strftime('%b %d')


def _enrich_notification(n):
    """Enriches a Notification model instance into structured presentation data."""
    actor = None
    if getattr(n, 'actor_id', None) and not getattr(n, 'actor_anonymous', False):
        try:
            actor = n.actor
        except User.DoesNotExist:
            actor = None

    actor_name = actor.username if actor else None
    if getattr(n, 'actor_anonymous', False):
        actor_name = 'Someone'
    actor_photo = _avatar_url(actor) if actor else None
    actor_badge = _user_badge_info(actor) if actor else None
    url = get_notification_url(n, actor_name=actor_name)
    
    actor_display = actor_name or 'Someone'
    verb = getattr(n, 'verb', '') or 'system'
    
    title = ''
    body = ''
    icon_name = 'notifications'
    icon_theme = 'emerald'
    primary_action = None
    secondary_action = None
    category = 'social'
    
    if verb == 'mention':
        category = 'mentions'
        title = f"{actor_display} mentioned you"
        body = n.message or "Mentioned you in a discussion or comment."
        icon_name = 'alternate_email'
        icon_theme = 'blue'
        primary_action = {'label': 'Reply', 'url': url, 'action': 'reply'}
        secondary_action = {'label': 'View thread', 'url': url, 'action': 'view'}
    elif verb in ('reply', 'reply_reply'):
        category = 'social'
        title = f"{actor_display} replied to your post" if verb == 'reply' else f"{actor_display} replied to your comment"
        body = n.message or "Replied to your discussion thread."
        icon_name = 'chat_bubble'
        icon_theme = 'purple'
        primary_action = {'label': 'Reply', 'url': url, 'action': 'reply'}
        secondary_action = {'label': 'View thread', 'url': url, 'action': 'view'}
    elif verb in ('resource_comment', 'resource_comment_reply'):
        category = 'social'
        title = f"{actor_display} commented on your resource" if verb == 'resource_comment' else f"{actor_display} replied to your comment"
        body = n.message or "Left feedback on your study resource."
        icon_name = 'description'
        icon_theme = 'blue'
        primary_action = {'label': 'Reply', 'url': url, 'action': 'reply'}
        secondary_action = {'label': 'View resource', 'url': url, 'action': 'view'}
    elif verb == 'like_post':
        category = 'social'
        title = f"{actor_display} liked your post"
        body = n.message or "Gave a thumbs up to your forum post."
        icon_name = 'thumb_up'
        icon_theme = 'amber'
        secondary_action = {'label': 'View post', 'url': url, 'action': 'view'}
    elif verb == 'like_reply':
        category = 'social'
        title = f"{actor_display} liked your reply"
        body = n.message or "Gave a thumbs up to your reply."
        icon_name = 'thumb_up'
        icon_theme = 'amber'
        secondary_action = {'label': 'View thread', 'url': url, 'action': 'view'}
    elif verb in ('like_resource', 'like_resource_comment'):
        category = 'social'
        title = f"{actor_display} liked your resource" if verb == 'like_resource' else f"{actor_display} liked your comment"
        body = n.message or "Appreciated your shared resource."
        icon_name = 'thumb_up'
        icon_theme = 'amber'
        secondary_action = {'label': 'View resource', 'url': url, 'action': 'view'}
    elif verb in ('follow', 'follow_request'):
        category = 'social'
        title = f"{actor_display} started following you" if verb == 'follow' else f"{actor_display} requested to follow you"
        body = n.message or "You have a new follower on NEBians."
        icon_name = 'person_add'
        icon_theme = 'blue'
        secondary_action = {'label': 'View profile', 'url': f'/profile/{actor_name}/' if actor_name else '#', 'action': 'view'}
    elif verb == 'resource_approved':
        category = 'system'
        title = "Resource approved"
        body = n.message or "Your study resource was reviewed and approved! It is now live in the library."
        icon_name = 'check_circle'
        icon_theme = 'emerald'
        secondary_action = {'label': 'View resource', 'url': url, 'action': 'view'}
    elif verb == 'resource_rejected':
        category = 'system'
        title = "Resource review update"
        body = n.message or "Your uploaded resource was not approved."
        icon_name = 'cancel'
        icon_theme = 'rose'
        if url and url != '#':
            secondary_action = {'label': 'View details', 'url': url, 'action': 'view'}
    elif verb == 'system':
        category = 'system'
        title = "Workspace backup is ready" if "backup" in (n.message or "").lower() else ("System Announcement" if not n.message or len(n.message) > 45 else n.message)
        body = n.message or "Platform update from NEBians team."
        icon_name = 'cloud_download' if "backup" in (n.message or "").lower() or "download" in (n.message or "").lower() else 'campaign'
        icon_theme = 'emerald'
        if "download" in (n.message or "").lower() or "backup" in (n.message or "").lower():
            secondary_action = {'label': 'Download', 'url': url if url != '#' else 'javascript:void(0)', 'action': 'download'}
        elif url and url != '#':
            secondary_action = {'label': 'View details', 'url': url, 'action': 'view'}
    else:
        category = 'social'
        title = f"Update from {actor_display}"
        body = n.message or "New activity on your account."
        icon_name = 'notifications'
        icon_theme = 'blue'
    has_avatar_actor = bool(actor_photo or (actor_name and verb not in ('system', 'resource_approved', 'resource_rejected')))

    return {
        'id': n.id,
        'verb': verb,
        'title': title,
        'body': body,
        'category': category,
        'icon_name': icon_name,
        'icon_theme': icon_theme,
        'target_type': n.target_type,
        'target_id': n.target_id,
        'reference_type': n.reference_type,
        'reference_id': n.reference_id,
        'is_read': n.is_read,
        'created_at': n.created_at,
        'compact_time': _format_compact_time(n.created_at),
        'actor_name': actor_name,
        'actor_photo_url': actor_photo,
        'actor_id': n.actor_id if (n.actor and not n.actor_anonymous) else None,
        'actor_badge_info': actor_badge,
        'has_avatar_actor': has_avatar_actor,
        'url': url,
        'primary_action': primary_action,
        'secondary_action': secondary_action,
    }


def _filter_notifications_qs(user_id, category_tab='all'):
    """Returns filtered queryset for a specific user and category tab."""
    base_qs = Notification.objects.filter(recipient_id=user_id).select_related('actor').order_by('-created_at')
    if category_tab == 'mentions':
        return base_qs.filter(verb='mention')
    if category_tab == 'system':
        return base_qs.filter(verb__in=['system', 'resource_approved', 'resource_rejected'])
    if category_tab in ('activity', 'social'):
        return base_qs.filter(verb__in=[
            'like_post', 'like_reply', 'like_resource', 'like_resource_comment',
            'reply', 'reply_reply', 'resource_comment', 'resource_comment_reply',
            'follow', 'follow_request'
        ])
    if category_tab == 'unread':
        return base_qs.filter(is_read=False)
    return base_qs


def _get_category_counts(user_id):
    """Computes notification counts for each category tab."""
    base_qs = Notification.objects.filter(recipient_id=user_id)
    all_count = base_qs.count()
    mentions_count = base_qs.filter(verb='mention').count()
    system_count = base_qs.filter(verb__in=['system', 'resource_approved', 'resource_rejected']).count()
    activity_count = base_qs.filter(verb__in=[
        'like_post', 'like_reply', 'like_resource', 'like_resource_comment',
        'reply', 'reply_reply', 'resource_comment', 'resource_comment_reply',
        'follow', 'follow_request'
    ]).count()
    unread_count = base_qs.filter(is_read=False).count()
    
    return {
        'all': all_count,
        'mentions': mentions_count,
        'system': system_count,
        'activity': activity_count,
        'unread': unread_count,
    }


def notifications(request):
    """Full-page notification center with categories and pagination."""
    user_id = _get_user_id(request)
    if not user_id:
        return redirect('web:login')
    
    current_tab = request.GET.get('tab', 'all').strip().lower()
    if current_tab not in ('all', 'mentions', 'system', 'activity', 'unread'):
        current_tab = 'all'
        
    try:
        page = max(1, int(request.GET.get('page', 1)))
    except (TypeError, ValueError):
        page = 1
        
    try:
        page_size = min(50, max(5, int(request.GET.get('page_size', 10))))
    except (TypeError, ValueError):
        page_size = 10

    notifs_qs = _filter_notifications_qs(user_id, current_tab)
    counts = _get_category_counts(user_id)
    
    paginator = Paginator(notifs_qs, page_size)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages if paginator.num_pages > 0 else 1)

    enriched_notifs = [_enrich_notification(n) for n in page_obj.object_list]
    
    context = {
        'notifications': enriched_notifs,
        'page_obj': page_obj,
        'current_tab': current_tab,
        'counts': counts,
        'unread_count': counts['unread'],
        'total_count': counts['all'],
        'page_size': page_size,
    }
    return render(request, 'web/notifications.html', _ctx(request, **context))


def ajax_notifications(request):
    """AJAX: list notifications for current user with filtering, pagination and counts."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    current_tab = request.GET.get('tab', 'all').strip().lower()
    if current_tab not in ('all', 'mentions', 'system', 'activity', 'unread'):
        current_tab = 'all'
        
    try:
        page = max(1, int(request.GET.get('page', 1)))
    except (TypeError, ValueError):
        page = 1
    try:
        page_size = min(50, max(1, int(request.GET.get('page_size', 10))))
    except (TypeError, ValueError):
        page_size = 10

    notifs_qs = _filter_notifications_qs(user_id, current_tab)
    counts = _get_category_counts(user_id)
    
    paginator = Paginator(notifs_qs, page_size)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages if paginator.num_pages > 0 else 1)

    enriched_results = [_enrich_notification(n) for n in page_obj.object_list]
    
    return JsonResponse({
        'results': enriched_results,
        'total': paginator.count,
        'page': page_obj.number,
        'num_pages': paginator.num_pages,
        'has_more': page_obj.has_next(),
        'has_prev': page_obj.has_previous(),
        'start_index': page_obj.start_index() if paginator.count > 0 else 0,
        'end_index': page_obj.end_index() if paginator.count > 0 else 0,
        'counts': counts,
        'unread_count': counts['unread'],
        'current_tab': current_tab,
    })


@require_POST
def ajax_notifications_mark_read(request):
    """AJAX: mark specific or all notifications as read."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        data = {}
    mark_all = data.get('mark_all', False)
    notification_ids = data.get('notification_ids', [])
    if mark_all:
        count = Notification.objects.filter(recipient_id=user_id, is_read=False).update(is_read=True)
        _counters.reset_user_unread_notification_count(user_id)
        cache.delete(f'unread_count:{user_id}')
        return JsonResponse({'success': True, 'marked_count': count, 'unread_count': 0})
    if notification_ids:
        notifs = Notification.objects.filter(recipient_id=user_id, pk__in=notification_ids, is_read=False)
        count = notifs.update(is_read=True)
        unread = Notification.objects.filter(recipient_id=user_id, is_read=False).count()
        User.objects.filter(pk=user_id).update(unread_notification_count=unread)
        cache.delete(f'unread_count:{user_id}')
        return JsonResponse({'success': True, 'marked_count': count, 'unread_count': unread})
    return JsonResponse({'error': 'Provide notification_ids or mark_all=true'}, status=400)


def ajax_notifications_unread_count(request):
    """AJAX: get unread notification count for current user."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'count': 0})
    try:
        user = User.objects.get(pk=user_id)
        count = getattr(user, 'unread_notification_count', 0) or 0
    except User.DoesNotExist:
        count = 0
    return JsonResponse({'count': count})