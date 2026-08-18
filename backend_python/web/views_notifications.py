"""Views Notifications extracted from views.py."""
from .view_helpers import *  # noqa: F401,F403
from api.notifications import get_notification_url

def notifications(request):
    """Full-page notification center."""
    user_id = _get_user_id(request)
    if not user_id:
        return redirect('web:login')
    notifs = Notification.objects.filter(recipient_id=user_id).select_related('actor')[:50]
    VERB_LABELS = {
        'like_post': 'liked your post',
        'like_reply': 'liked your reply',
        'like_resource': 'liked your resource',
        'like_resource_comment': 'liked your comment',
        'reply': 'replied to your post',
        'reply_reply': 'replied to your comment',
        'resource_comment': 'commented on your resource',
        'resource_comment_reply': 'replied to your comment',
        'follow': 'started following you',
        'mention': 'mentioned you',
        'resource_approved': '',
        'resource_rejected': '',
        'system': '',
    }
    notif_data = []
    for n in notifs:
        actor_name = n.actor.username if n.actor else None
        safe_actor_name = escape(actor_name) if actor_name else None
        actor_photo = _avatar_url(n.actor) if n.actor else None
        actor_id_val = n.actor_id if n.actor else None
        actor_badge = _user_badge_info(n.actor) if n.actor else None
        verb_label = VERB_LABELS.get(n.verb, n.verb)
        if n.verb == 'system':
            text = escape(n.message or 'System notification')
        elif safe_actor_name:
            text = f'<strong>{safe_actor_name}</strong> <span class="notif-verb">{escape(verb_label)}</span>'
        else:
            text = f'<span class="notif-verb">{escape(verb_label)}</span>'
        url = get_notification_url(n, actor_name=actor_name)
        notif_data.append({
            'id': n.id,
            'verb': n.verb,
            'targetType': n.target_type,
            'targetId': n.target_id,
            'referenceType': n.reference_type,
            'referenceId': n.reference_id,
            'message': n.message,
            'isRead': n.is_read,
            'createdAt': n.created_at,
            'actorName': actor_name,
            'actorPhotoUrl': actor_photo,
            'actorId': actor_id_val,
            'actorBadgeInfo': actor_badge,
            'text': text,
            'url': url,
        })
    return render(request, 'web/notifications.html', _ctx(request, notifications=notif_data))

def ajax_notifications(request):
    """AJAX: list notifications for current user."""
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    try:
        page = max(1, int(request.GET.get('page', 1)))
    except (TypeError, ValueError):
        page = 1
    try:
        page_size = min(100, max(1, int(request.GET.get('page_size', 20))))
    except (TypeError, ValueError):
        page_size = 20
    offset = (page - 1) * page_size
    notifs = Notification.objects.filter(recipient_id=user_id).select_related('actor').order_by('-created_at')
    total = notifs.count()
    notifs_page = notifs[offset:offset + page_size]
    results = []
    for n in notifs_page:
        actor_badge = _user_badge_info(n.actor) if n.actor else None
        actor_name = n.actor.username if n.actor else None
        results.append({
            'id': n.id,
            'verb': n.verb,
            'targetType': n.target_type,
            'targetId': n.target_id,
            'referenceType': n.reference_type,
            'referenceId': n.reference_id,
            'message': n.message,
            'isRead': n.is_read,
            'createdAt': n.created_at,
            'actorName': actor_name,
            'actorPhotoUrl': _avatar_url(n.actor) if n.actor else None,
            'actorId': n.actor_id if n.actor else None,
            'actorBadgeInfo': actor_badge,
            'url': get_notification_url(n, actor_name=actor_name),
        })
    return JsonResponse({
        'results': results,
        'total': total,
        'page': page,
        'hasMore': (offset + page_size) < total,
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
        return JsonResponse({'success': True, 'marked_count': count})
    if notification_ids:
        notifs = Notification.objects.filter(recipient_id=user_id, pk__in=notification_ids, is_read=False)
        count = notifs.update(is_read=True)
        unread = Notification.objects.filter(recipient_id=user_id, is_read=False).count()
        User.objects.filter(pk=user_id).update(unread_notification_count=unread)
        cache.delete(f'unread_count:{user_id}')
        return JsonResponse({'success': True, 'marked_count': count})
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