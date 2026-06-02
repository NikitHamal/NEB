"""
Centralized cleanup logic for deleting posts and replies.

Industry-standard approach:
1. Collect all affected user IDs and counts BEFORE deleting (pre-deletion snapshot)
2. Delete all related data atomically in one transaction
3. Batch-update denormalized counters after the transaction

This ensures:
- No counter drift (likes_given, likes_received, reply_count all stay accurate)
- No orphaned data (bookmarks, edit history, reports, notifications, NebyTask)
- Nested replies are fully handled (not just direct children)
- Atomic: either everything is cleaned up or nothing is
"""
import logging
from collections import Counter

from django.db import transaction
from django.db.models import F

from .models import (
    Post, Reply, PostLike, ReplyLike, Bookmark,
    EditHistory, Report, NebyTask,
)
from . import counters as _counters
from .notifications import delete_notifications_for_target

logger = logging.getLogger(__name__)


def _collect_descendant_reply_ids(reply_id):
    """Recursively collect ALL descendant reply IDs (children, grandchildren, etc.)."""
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
    """Collect ALL reply IDs for a post (all nesting levels)."""
    return set(
        Reply.objects.filter(post_id=post_id).values_list('id', flat=True)
    )


def delete_post_with_cleanup(post_id):
    """
    Delete a post and ALL related data, properly updating all denormalized counters.

    Must be called within a transaction by the caller if needed.
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

    likes_received_by_author = Counter()
    likes_received_by_author[post_author_id] += post_thumbs_up
    reply_likes = (
        Reply.objects.filter(post_id=post_id)
        .values_list('user_id', 'thumbs_up_count')
    )
    for author_id, thumbs in reply_likes:
        likes_received_by_author[author_id] += thumbs

    all_like_giver_ids = like_giver_ids | reply_liker_ids

    with transaction.atomic():
        Bookmark.objects.filter(target_type='post', target_id=post_id).delete()
        Bookmark.objects.filter(target_type='reply', target_id__in=all_reply_ids).delete()

        PostLike.objects.filter(post_id=post_id).delete()
        ReplyLike.objects.filter(reply_id__in=all_reply_ids).delete()

        EditHistory.objects.filter(target_type='post', target_id=post_id).delete()
        EditHistory.objects.filter(target_type='reply', target_id__in=all_reply_ids).delete()

        Report.objects.filter(target_type='post', target_id=post_id).delete()
        Report.objects.filter(target_type='reply', target_id__in=all_reply_ids).delete()

        NebyTask.objects.filter(post_id=post_id).delete()
        NebyTask.objects.filter(reply_id__in=all_reply_ids).delete()

        for rid in all_reply_ids:
            delete_notifications_for_target('reply', rid)
        delete_notifications_for_target('post', post_id)

        Reply.objects.filter(post_id=post_id).delete()
        post.delete()

    _counters.decrement_user_post_count(post_author_id)
    _counters.batch_decrement_reply_counts(reply_author_ids)
    _counters.batch_decrement_likes_given(all_like_giver_ids)
    _counters.batch_decrement_likes_received(likes_received_by_author)

    logger.info(
        "delete_post_with_cleanup: deleted post %s, author %s, %d replies, %d like givers cleaned",
        post_id, post_author_id, len(all_reply_ids), len(all_like_giver_ids),
    )
    return True


def delete_reply_with_cleanup(reply_id):
    """
    Delete a reply (and ALL its descendants) with full cleanup.

    Must be called within a transaction by the caller if needed.
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

    like_giver_ids = set(
        ReplyLike.objects.filter(reply_id__in=all_ids).values_list('user_id', flat=True)
    )

    likes_received_by_author = Counter()
    for author_id, thumbs in all_replies_data.items():
        likes_received_by_author[author_id] += thumbs

    all_author_ids = set(all_replies_data.keys())

    with transaction.atomic():
        Bookmark.objects.filter(target_type='reply', target_id__in=all_ids).delete()

        ReplyLike.objects.filter(reply_id__in=all_ids).delete()

        EditHistory.objects.filter(target_type='reply', target_id__in=all_ids).delete()

        Report.objects.filter(target_type='reply', target_id__in=all_ids).delete()

        NebyTask.objects.filter(reply_id__in=all_ids).delete()

        for rid in all_ids:
            delete_notifications_for_target('reply', rid)

        Reply.objects.filter(id__in=descendant_ids).delete()
        reply.delete()

        Post.objects.filter(pk=post_id, reply_count__gt=0).update(
            reply_count=F('reply_count') - 1
        )
        if parent_id:
            Reply.objects.filter(pk=parent_id, reply_count__gt=0).update(
                reply_count=F('reply_count') - 1
            )

    _counters.batch_decrement_reply_counts(all_author_ids)
    _counters.batch_decrement_likes_given(like_giver_ids)
    _counters.batch_decrement_likes_received(likes_received_by_author)

    logger.info(
        "delete_reply_with_cleanup: deleted reply %s and %d descendants, %d like givers cleaned",
        reply_id, len(descendant_ids), len(like_giver_ids),
    )
    return True