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
    )


def decrement_user_post_count(user_id):
    from .models import User
    User.objects.filter(pk=user_id, post_count__gt=0).update(
        post_count=F('post_count') - 1,
        contribution_score=F('contribution_score') - 3,
    )


def increment_user_reply_count(user_id):
    from .models import User
    User.objects.filter(pk=user_id).update(
        reply_count=F('reply_count') + 1,
        contribution_score=F('contribution_score') + 2,
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
    )


def decrement_user_likes_received(user_id):
    from .models import User
    User.objects.filter(pk=user_id, likes_received_count__gt=0).update(
        likes_received_count=F('likes_received_count') - 1,
        contribution_score=F('contribution_score') - 2,
    )


def increment_user_follower_count(user_id):
    from .models import User
    User.objects.filter(pk=user_id).update(follower_count=F('follower_count') + 1)


def decrement_user_follower_count(user_id):
    from .models import User
    User.objects.filter(pk=user_id, follower_count__gt=0).update(follower_count=F('follower_count') - 1)


def increment_user_following_count(user_id):
    from .models import User
    User.objects.filter(pk=user_id).update(following_count=F('following_count') + 1)


def decrement_user_following_count(user_id):
    from .models import User
    User.objects.filter(pk=user_id, following_count__gt=0).update(following_count=F('following_count') - 1)


def increment_user_unread_notification_count(user_id):
    from .models import User
    User.objects.filter(pk=user_id).update(unread_notification_count=F('unread_notification_count') + 1)


def decrement_user_unread_notification_count(user_id, amount=1):
    from .models import User
    if amount <= 0:
        return
    User.objects.filter(pk=user_id, unread_notification_count__gt=0).update(
        unread_notification_count=F('unread_notification_count') - amount
    )


def reset_user_unread_notification_count(user_id):
    from .models import User
    User.objects.filter(pk=user_id).update(unread_notification_count=0)


def batch_decrement_likes_given(user_ids):
    """Decrement likes_given_count and contribution_score for multiple users.
    Each user gets decremented by 1 (one like removed per user)."""
    if not user_ids:
        return
    from .models import User
    User.objects.filter(pk__in=user_ids, likes_given_count__gt=0).update(
        likes_given_count=F('likes_given_count') - 1,
        contribution_score=F('contribution_score') - 1,
    )


def batch_decrement_likes_received(user_id_count_map):
    """Decrement likes_received_count and contribution_score for users.
    user_id_count_map is {user_id: count} where count is how many likes received to subtract."""
    if not user_id_count_map:
        return
    from .models import User
    for uid, count in user_id_count_map.items():
        if count <= 0:
            continue
        User.objects.filter(pk=uid, likes_received_count__gte=count).update(
            likes_received_count=F('likes_received_count') - count,
            contribution_score=F('contribution_score') - (count * 2),
        )


def batch_decrement_reply_counts(user_ids):
    """Decrement reply_count and contribution_score for multiple users.
    Each user gets decremented by 1 (one reply removed per user)."""
    if not user_ids:
        return
    from .models import User
    User.objects.filter(pk__in=user_ids, reply_count__gt=0).update(
        reply_count=F('reply_count') - 1,
        contribution_score=F('contribution_score') - 2,
    )