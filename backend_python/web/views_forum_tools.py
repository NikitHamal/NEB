"""Forum thread tools: reply labels and the composer's live preview."""
import json

from .view_helpers import *  # noqa: F401,F403
from . import forum_labels


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
    from api.utils import now_ms
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

    previous = reply.label or ''
    now = now_ms()
    with transaction.atomic():
        if label == 'accepted':
            Reply.objects.filter(post_id=post.id, label='accepted').exclude(pk=reply.pk).update(label='', labeled_at=0)
            post.is_resolved = True
            post.accepted_reply_id = reply.id
            post.save(update_fields=['is_resolved', 'accepted_reply_id'])
        elif previous == 'accepted':
            post.is_resolved = False
            post.accepted_reply_id = ''
            post.save(update_fields=['is_resolved', 'accepted_reply_id'])
        reply.label = label
        reply.labeled_by_id = user_id if label else None
        reply.labeled_at = now if label else 0
        reply.save(update_fields=['label', 'labeled_by', 'labeled_at'])

    if label in ('accepted', 'correct', 'helpful') and reply.user_id and reply.user_id != user_id and label != previous:
        try:
            from api.notifications import notify_system
            phrase = {'accepted': 'was accepted as the answer', 'correct': 'was marked correct',
                      'helpful': 'was marked helpful'}[label]
            notify_system(reply.user_id, 'Your reply on "%s" %s.' % (post.title[:60], phrase),
                          target_type='post', target_id=post.id)
        except Exception:
            pass
    _clear_page_cache()
    try:
        from api import realtime as _rt
        _rt.broadcast_reply_updated(post.id, reply.id, {'label': label, 'labeled_at': reply.labeled_at})
    except Exception:
        pass
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
