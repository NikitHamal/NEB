"""
Helper functions to keep denormalized User counters in sync.

Call these from wherever a Post, Reply, PostLike, ReplyLike, or Follow
is created or deleted. They update the relevant User counter fields
atomically using F() expressions.
"""
from django.db.models import F


def increment_user_post_count(user_id):
    from .models import User
    User.objects.filter(pk=user_id).update(
        post_count=F('post_count') + 1,
        contribution_score=F('contribution_score') + 3,
        nebians_points=F('nebians_points') + 3,
    )


def increment_user_reply_count(user_id):
    from .models import User
    User.objects.filter(pk=user_id).update(
        reply_count=F('reply_count') + 1,
        contribution_score=F('contribution_score') + 2,
        nebians_points=F('nebians_points') + 2,
    )


def decrement_user_reply_count(user_id):
    from .models import User
    User.objects.filter(pk=user_id, reply_count__gt=0).update(
        reply_count=F('reply_count') - 1,
        contribution_score=F('contribution_score') - 2,
    )


def increment_user_likes_given(user_id):
    from .models import User
    User.objects.filter(pk=user_id).update(
        likes_given_count=F('likes_given_count') + 1,
        contribution_score=F('contribution_score') + 1,
        nebians_points=F('nebians_points') + 1,
    )


def decrement_user_likes_given(user_id):
    from .models import User
    User.objects.filter(pk=user_id, likes_given_count__gt=0).update(
        likes_given_count=F('likes_given_count') - 1,
        contribution_score=F('contribution_score') - 1,
    )


def increment_user_likes_received(user_id):
    from .models import User
    User.objects.filter(pk=user_id).update(
        likes_received_count=F('likes_received_count') + 1,
        contribution_score=F('contribution_score') + 2,
        nebians_points=F('nebians_points') + 2,
    )


def decrement_user_likes_received(user_id):
    from .models import User
    User.objects.filter(pk=user_id, likes_received_count__gt=0).update(
        likes_received_count=F('likes_received_count') - 1,
        contribution_score=F('contribution_score') - 2,
    )


def increment_user_unread_notification_count(user_id):
    from django.core.cache import cache
    from .models import User
    User.objects.filter(pk=user_id).update(unread_notification_count=F('unread_notification_count') + 1)
    cache.delete(f'unread_count:{user_id}')


def decrement_user_unread_notification_count(user_id, amount=1):
    from django.core.cache import cache
    from .models import User
    if amount <= 0:
        return
    User.objects.filter(pk=user_id, unread_notification_count__gt=0).update(
        unread_notification_count=F('unread_notification_count') - amount
    )
    cache.delete(f'unread_count:{user_id}')


def reset_user_unread_notification_count(user_id):
    from django.core.cache import cache
    from .models import User
    User.objects.filter(pk=user_id).update(unread_notification_count=0)
    cache.delete(f'unread_count:{user_id}')


def increment_user_resource_approved(user_id):
    """Award contribution points when a resource is approved."""
    from .models import User
    User.objects.filter(pk=user_id).update(
        contribution_score=F('contribution_score') + 10,
        nebians_points=F('nebians_points') + 10,
    )


