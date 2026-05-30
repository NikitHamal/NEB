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