from django.db import transaction

from api.models import Reply
from api.utils import now_ms


def apply_label(reply, label, actor_id):
    post = reply.post
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
        reply.labeled_by_id = actor_id if label else None
        reply.labeled_at = now if label else 0
        reply.save(update_fields=['label', 'labeled_by', 'labeled_at'])

    if label in ('accepted', 'correct', 'helpful') and reply.user_id and reply.user_id != actor_id and label != previous:
        try:
            from api.notifications import notify_system
            phrase = {'accepted': 'was accepted as the answer', 'correct': 'was marked correct',
                      'helpful': 'was marked helpful'}[label]
            notify_system(reply.user_id, 'Your reply on "%s" %s.' % (post.title[:60], phrase),
                          target_type='post', target_id=post.id)
        except Exception:
            pass
    try:
        from api import realtime as _rt
        _rt.broadcast_reply_updated(post.id, reply.id, {'label': label, 'labeled_at': reply.labeled_at})
    except Exception:
        pass
    return previous
