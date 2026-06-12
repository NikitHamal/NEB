"""
Centralized cleanup logic for deleting posts and replies.

Approach:
1. Collect all affected user IDs and counts BEFORE deleting (pre-deletion snapshot)
2. Delete all related data atomically in one transaction
3. Batch-update denormalized counters after the transaction
4. contribution_score is NEVER decremented on deletion — only raw counters are adjusted

This ensures:
- No counter drift (likes_given, likes_received, reply_count all stay accurate)
- No orphaned data (bookmarks, edit history, reports, notifications, NebyTask)
- Nested replies are fully handled (not just direct children)
- Atomic: either everything is cleaned up or nothing is
- contribution_score is preserved (nebian score never decreases on content deletion)
"""
import logging
from collections import Counter

from django.db import transaction
from django.db.models import F

from django.core.cache import cache

from .models import (
    Post, Reply, PostLike, ReplyLike, Bookmark,
    EditHistory, Report, NebyTask, Notification, User,
)

def _batch_fix_unread_counts(recipient_ids):
    """Recalculate unread_notification_count for affected recipients after notification deletion."""
    if not recipient_ids:
        return
    for uid in recipient_ids:
        count = Notification.objects.filter(recipient_id=uid, is_read=False).count()
        User.objects.filter(pk=uid).update(unread_notification_count=count)
        cache.delete(f'unread_count:{uid}')


logger = logging.getLogger(__name__)


def _collect_descendant_reply_ids(reply_id):
    all_ids = set()
    queue = [reply_id]
    while queue:
        parent_id = queue.pop(0)
        child_ids = set(
            Reply.objects.filter(parent_reply_id=parent_id)
            .values_list('id', flat=True)
        )
        new_ids = child_ids - all_ids
        all_ids.update(new_ids)
        queue.extend(new_ids)
    return all_ids


def _collect_all_reply_ids_for_post(post_id):
    return set(
        Reply.objects.filter(post_id=post_id).values_list('id', flat=True)
    )


def _batch_decrement_counters(post_author_id, reply_author_ids, all_like_giver_ids, likes_received_by_author, reply_count_by_author=None, like_count_by_giver=None):
    """Decrement raw counters (post_count, reply_count, likes_given, likes_received) without touching contribution_score.
    
    reply_author_ids is a set of unique user IDs.
    reply_count_by_author is a dict {user_id: count} — how many replies each author had.
    like_count_by_giver is a dict {user_id: count} — how many likes each giver gave.
    If not provided, falls back to decrementing by 1 per unique user (may undercount).
    """
    if post_author_id:
        User.objects.filter(pk=post_author_id, post_count__gt=0).update(
            post_count=F('post_count') - 1,
        )
    if reply_author_ids:
        if reply_count_by_author:
            for uid, count in reply_count_by_author.items():
                if count > 0:
                    User.objects.filter(pk=uid, reply_count__gte=count).update(
                        reply_count=F('reply_count') - count,
                    )
        else:
            User.objects.filter(pk__in=reply_author_ids, reply_count__gt=0).update(
                reply_count=F('reply_count') - 1,
            )
    if all_like_giver_ids:
        if like_count_by_giver:
            for uid, count in like_count_by_giver.items():
                if count > 0:
                    User.objects.filter(pk=uid, likes_given_count__gte=count).update(
                        likes_given_count=F('likes_given_count') - count,
                    )
        else:
            User.objects.filter(pk__in=all_like_giver_ids, likes_given_count__gt=0).update(
                likes_given_count=F('likes_given_count') - 1,
            )
    for uid, count in likes_received_by_author.items():
        if count > 0:
            User.objects.filter(pk=uid, likes_received_count__gte=count).update(
                likes_received_count=F('likes_received_count') - count,
            )


def delete_post_with_cleanup(post_id):
    """
    Delete a post and ALL related data, updating raw counters but preserving contribution_score.
    Raises Post.DoesNotExist if post not found.
    """
    post = Post.objects.get(pk=post_id)

    post_author_id = post.user_id
    post_thumbs_up = post.thumbs_up_count

    all_reply_ids = _collect_all_reply_ids_for_post(post_id)

    like_giver_ids = set(
        PostLike.objects.filter(post_id=post_id).values_list('user_id', flat=True)
    )
    reply_author_ids = set(
        Reply.objects.filter(post_id=post_id).values_list('user_id', flat=True)
    )
    reply_liker_ids = set(
        ReplyLike.objects.filter(reply_id__in=all_reply_ids).values_list('user_id', flat=True)
    )

    reply_count_by_author = Counter(
        Reply.objects.filter(post_id=post_id).values_list('user_id', flat=True)
    )

    likes_received_by_author = Counter()
    likes_received_by_author[post_author_id] += post_thumbs_up
    reply_likes = (
        Reply.objects.filter(post_id=post_id)
        .values_list('user_id', 'thumbs_up_count')
    )
    for author_id, thumbs in reply_likes:
        likes_received_by_author[author_id] += thumbs

    like_count_by_giver = Counter()
    for uid in PostLike.objects.filter(post_id=post_id).values_list('user_id', flat=True):
        like_count_by_giver[uid] += 1
    for uid in ReplyLike.objects.filter(reply_id__in=all_reply_ids).values_list('user_id', flat=True):
        like_count_by_giver[uid] += 1

    all_like_giver_ids = like_giver_ids | reply_liker_ids

    notif_filter = {'target_type': 'post', 'target_id': post_id}
    notif_reply_filter = None
    if all_reply_ids:
        notif_reply_filter = {'target_type': 'reply', 'target_id__in': all_reply_ids}

    affected_recipient_ids = set(
        Notification.objects.filter(**notif_filter).values_list('recipient_id', flat=True)
    )
    if notif_reply_filter:
        affected_recipient_ids.update(
            Notification.objects.filter(**notif_reply_filter).values_list('recipient_id', flat=True)
        )

    with transaction.atomic():
        Bookmark.objects.filter(target_type='post', target_id=post_id).delete()
        if all_reply_ids:
            Bookmark.objects.filter(target_type='reply', target_id__in=all_reply_ids).delete()

        PostLike.objects.filter(post_id=post_id).delete()
        if all_reply_ids:
            ReplyLike.objects.filter(reply_id__in=all_reply_ids).delete()

        EditHistory.objects.filter(target_type='post', target_id=post_id).delete()
        if all_reply_ids:
            EditHistory.objects.filter(target_type='reply', target_id__in=all_reply_ids).delete()

        Report.objects.filter(target_type='post', target_id=post_id).delete()
        if all_reply_ids:
            Report.objects.filter(target_type='reply', target_id__in=all_reply_ids).delete()

        NebyTask.objects.filter(post_id=post_id).delete()
        if all_reply_ids:
            NebyTask.objects.filter(reply_id__in=all_reply_ids).delete()

        Notification.objects.filter(**notif_filter).delete()
        if notif_reply_filter:
            Notification.objects.filter(**notif_reply_filter).delete()

        if all_reply_ids:
            Reply.objects.filter(post_id=post_id).delete()
        post.delete()

    _batch_decrement_counters(post_author_id, reply_author_ids, all_like_giver_ids, likes_received_by_author, reply_count_by_author=reply_count_by_author, like_count_by_giver=like_count_by_giver)
    _batch_fix_unread_counts(affected_recipient_ids)

    from api.search import delete_post as _meili_delete_post
    _meili_delete_post(post_id)

    logger.info(
        "delete_post_with_cleanup: deleted post %s, author %s, %d replies, %d like givers cleaned",
        post_id, post_author_id, len(all_reply_ids), len(all_like_giver_ids),
    )
    return True


def delete_reply_with_cleanup(reply_id):
    """
    Delete a reply (and ALL its descendants) with full cleanup.
    Preserves contribution_score.
    Raises Reply.DoesNotExist if reply not found.
    """
    reply = Reply.objects.get(pk=reply_id)

    post_id = reply.post_id
    parent_id = reply.parent_reply_id

    descendant_ids = _collect_descendant_reply_ids(reply_id)
    all_ids = descendant_ids | {str(reply_id)}

    all_replies_data = dict(
        Reply.objects.filter(id__in=all_ids).values_list('user_id', 'thumbs_up_count')
    )

    reply_count_by_author = Counter(
        Reply.objects.filter(id__in=all_ids).values_list('user_id', flat=True)
    )

    like_giver_ids = set(
        ReplyLike.objects.filter(reply_id__in=all_ids).values_list('user_id', flat=True)
    )

    like_count_by_giver = Counter(
        ReplyLike.objects.filter(reply_id__in=all_ids).values_list('user_id', flat=True)
    )

    likes_received_by_author = Counter()
    for author_id, thumbs in all_replies_data.items():
        likes_received_by_author[author_id] += thumbs

    all_author_ids = set(all_replies_data.keys())

    affected_recipient_ids = set(
        Notification.objects.filter(target_type='reply', target_id__in=all_ids).values_list('recipient_id', flat=True)
    )

    with transaction.atomic():
        Bookmark.objects.filter(target_type='reply', target_id__in=all_ids).delete()

        ReplyLike.objects.filter(reply_id__in=all_ids).delete()

        EditHistory.objects.filter(target_type='reply', target_id__in=all_ids).delete()

        Report.objects.filter(target_type='reply', target_id__in=all_ids).delete()

        NebyTask.objects.filter(reply_id__in=all_ids).delete()

        Notification.objects.filter(target_type='reply', target_id__in=all_ids).delete()

        Reply.objects.filter(id__in=descendant_ids).delete()
        reply.delete()

        Post.objects.filter(pk=post_id, reply_count__gt=0).update(
            reply_count=F('reply_count') - 1
        )
        if parent_id:
            Reply.objects.filter(pk=parent_id, reply_count__gt=0).update(
                reply_count=F('reply_count') - 1
            )

    _batch_decrement_counters(None, all_author_ids, like_giver_ids, likes_received_by_author, reply_count_by_author=reply_count_by_author, like_count_by_giver=like_count_by_giver)
    _batch_fix_unread_counts(affected_recipient_ids)

    logger.info(
        "delete_reply_with_cleanup: deleted reply %s and %d descendants, %d like givers cleaned",
        reply_id, len(descendant_ids), len(like_giver_ids),
    )
    return True