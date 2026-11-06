"""Forum thread tools: reply labels and the composer's live preview."""
import json

from api.models import Reply, User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .view_helpers import _clear_page_cache, _get_user_id, _rate_limit
from . import forum_labels
from .forum_label_service import apply_label


def _reply_payload(reply, viewer_id, is_admin):
    post = reply.post
    return {
        'id': reply.id,
        'postId': reply.post_id,
        'label': reply.label or '',
        'labelInfo': forum_labels.label_info(reply.label),
        'labeledAt': reply.labeled_at or 0,
        'postResolved': bool(post.is_resolved),
        'acceptedReplyId': post.accepted_reply_id or '',
    }


@require_POST
def ajax_label_reply(request, reply_id):
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    if _rate_limit(request, 'label_reply', 60, 60):
        return JsonResponse({'error': 'Too many requests. Please slow down.'}, status=429)
    try:
        data = json.loads(request.body or b'{}')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    label = str(data.get('label') or '').strip().lower()
    if label and label not in forum_labels.LABEL_KEYS:
        return JsonResponse({'error': 'Unknown label'}, status=400)
    try:
        reply = Reply.objects.select_related('post').get(pk=reply_id)
    except Reply.DoesNotExist:
        return JsonResponse({'error': 'Reply not found'}, status=404)
    viewer = User.objects.filter(pk=user_id).only('id', 'is_admin').first()
    is_admin = bool(viewer and viewer.is_admin)
    post = reply.post
    if not forum_labels.can_label(user_id, is_admin, post.user_id):
        return JsonResponse({'error': 'Only the author of this discussion can label replies.'}, status=403)

    apply_label(reply, label, user_id)
    _clear_page_cache()
    return JsonResponse(_reply_payload(reply, user_id, is_admin))


@require_POST
def ajax_forum_preview(request):
    from django.template import Context, Template
    user_id = _get_user_id(request)
    if not user_id:
        return JsonResponse({'error': 'Please log in again.'}, status=401)
    if _rate_limit(request, 'forum_preview', 90, 60):
        return JsonResponse({'error': 'Too many requests. Please slow down.'}, status=429)
    try:
        data = json.loads(request.body or b'{}')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    content = str(data.get('content') or '')[:10000]
    html = Template('{% load web_extras %}{{ c|mention_links }}').render(Context({'c': content}))
    return JsonResponse({'html': html})
