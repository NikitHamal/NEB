from django.db import migrations
from django.db.models import Count, F


def backfill_user_counters(apps, schema_editor):
    User = apps.get_model('api', 'User')
    Post = apps.get_model('api', 'Post')
    Reply = apps.get_model('api', 'Reply')
    PostLike = apps.get_model('api', 'PostLike')
    ReplyLike = apps.get_model('api', 'ReplyLike')
    Follow = apps.get_model('api', 'Follow')

    user_ids = list(User.objects.values_list('id', flat=True))

    post_counts = dict(Post.objects.filter(user_id__in=user_ids).values('user_id').annotate(c=Count('id')).values_list('user_id', 'c'))
    reply_counts = dict(Reply.objects.filter(user_id__in=user_ids).values('user_id').annotate(c=Count('id')).values_list('user_id', 'c'))
    follower_counts = dict(Follow.objects.filter(following_id__in=user_ids).values('following_id').annotate(c=Count('id')).values_list('following_id', 'c'))
    following_counts = dict(Follow.objects.filter(follower_id__in=user_ids).values('follower_id').annotate(c=Count('id')).values_list('follower_id', 'c'))

    likes_given = {}
    for model in [PostLike, ReplyLike]:
        for uid, cnt in model.objects.filter(user_id__in=user_ids).values('user_id').annotate(c=Count('id')).values_list('user_id', 'c'):
            likes_given[uid] = likes_given.get(uid, 0) + cnt

    likes_received = {}
    for model, owner_field in [(PostLike, 'post__user_id'), (ReplyLike, 'reply__user_id')]:
        for uid, cnt in model.objects.filter(**{owner_field + '__in': user_ids}).values(owner_field).annotate(c=Count('id')).values_list(owner_field, 'c'):
            likes_received[uid] = likes_received.get(uid, 0) + cnt

    for user in User.objects.iterator():
        pc = post_counts.get(user.id, 0)
        rc = reply_counts.get(user.id, 0)
        fc = follower_counts.get(user.id, 0)
        fwc = following_counts.get(user.id, 0)
        lg = likes_given.get(user.id, 0)
        lr = likes_received.get(user.id, 0)
        score = (pc * 3) + (rc * 2) + lg + (lr * 2)
        User.objects.filter(pk=user.id).update(
            post_count=pc,
            reply_count=rc,
            follower_count=fc,
            following_count=fwc,
            likes_given_count=lg,
            likes_received_count=lr,
            contribution_score=score,
        )


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_add_denormalized_user_counters'),
    ]

    operations = [
        migrations.RunPython(backfill_user_counters, migrations.RunPython.noop),
    ]