"""Management command to recalculate all denormalized counters.

Recalculates from actual data in the database, fixing any counter drift
caused by deletion bugs, race conditions, or manual DB edits.

Fixes:
- User counters (post_count, reply_count, follower_count, etc.)
- Post.reply_count (actual number of replies on each post)
- Reply.reply_count (actual number of child replies)

Usage:
    python manage.py recalculate_counters
    python manage.py recalculate_counters --dry-run
    python manage.py recalculate_counters --user neby
"""
from django.core.management.base import BaseCommand
from django.db.models import Count, F

from api.models import User, Post, Reply, PostLike, ReplyLike, Follow


class Command(BaseCommand):
    help = 'Recalculate all denormalized counters from actual data.'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', help='Show what would change without updating.')
        parser.add_argument('--user', type=str, help='Only recalculate user counters for a specific username.')

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        prefix = '[DRY RUN] ' if dry_run else ''

        self._recalculate_user_counters(options, dry_run, prefix)
        self._recalculate_post_reply_counts(dry_run, prefix)
        self._recalculate_reply_reply_counts(dry_run, prefix)

    def _recalculate_user_counters(self, options, dry_run, prefix):
        qs = User.objects.all()
        if options.get('user'):
            qs = qs.filter(username__iexact=options['user'])

        user_ids = list(qs.values_list('id', flat=True))
        self.stdout.write(f'\n{prefix}Recalculating user counters for {len(user_ids)} users...')

        post_counts = dict(
            Post.objects.filter(user_id__in=user_ids)
            .values('user_id').annotate(c=Count('id'))
            .values_list('user_id', 'c')
        )
        reply_counts = dict(
            Reply.objects.filter(user_id__in=user_ids)
            .values('user_id').annotate(c=Count('id'))
            .values_list('user_id', 'c')
        )
        follower_counts = dict(
            Follow.objects.filter(following_id__in=user_ids)
            .values('following_id').annotate(c=Count('id'))
            .values_list('following_id', 'c')
        )
        following_counts = dict(
            Follow.objects.filter(follower_id__in=user_ids)
            .values('follower_id').annotate(c=Count('id'))
            .values_list('follower_id', 'c')
        )

        likes_given = {}
        for model in [PostLike, ReplyLike]:
            for uid, cnt in (model.objects.filter(user_id__in=user_ids)
                             .values('user_id').annotate(c=Count('id'))
                             .values_list('user_id', 'c')):
                likes_given[uid] = likes_given.get(uid, 0) + cnt

        likes_received = {}
        for model, owner_field in [(PostLike, 'post__user_id'), (ReplyLike, 'reply__user_id')]:
            for uid, cnt in (model.objects.filter(**{owner_field + '__in': user_ids})
                             .values(owner_field).annotate(c=Count('id'))
                             .values_list(owner_field, 'c')):
                likes_received[uid] = likes_received.get(uid, 0) + cnt

        updated = 0
        for user in qs.iterator():
            pc = post_counts.get(user.id, 0)
            rc = reply_counts.get(user.id, 0)
            fc = follower_counts.get(user.id, 0)
            fwc = following_counts.get(user.id, 0)
            lg = likes_given.get(user.id, 0)
            lr = likes_received.get(user.id, 0)
            score = (pc * 3) + (rc * 2) + lg + (lr * 2)

            changed = (
                user.post_count != pc or
                user.reply_count != rc or
                user.follower_count != fc or
                user.following_count != fwc or
                user.likes_given_count != lg or
                user.likes_received_count != lr or
                user.contribution_score != score
            )

            if changed:
                self.stdout.write(
                    f'{prefix}{user.username}: '
                    f'posts {user.post_count}->{pc}, '
                    f'replies {user.reply_count}->{rc}, '
                    f'followers {user.follower_count}->{fc}, '
                    f'following {user.following_count}->{fwc}, '
                    f'likes_given {user.likes_given_count}->{lg}, '
                    f'likes_received {user.likes_received_count}->{lr}, '
                    f'score {user.contribution_score}->{score}'
                )
                if not dry_run:
                    User.objects.filter(pk=user.id).update(
                        post_count=pc,
                        reply_count=rc,
                        follower_count=fc,
                        following_count=fwc,
                        likes_given_count=lg,
                        likes_received_count=lr,
                        contribution_score=score,
                    )
                updated += 1

        self.stdout.write(self.style.SUCCESS(
            f'{prefix}{updated} users had drifted counters. '
            f'{len(user_ids) - updated} users were already correct.'
        ))

    def _recalculate_post_reply_counts(self, dry_run, prefix):
        self.stdout.write(f'\n{prefix}Recalculating Post.reply_count...')
        actual_counts = dict(
            Reply.objects.values('post_id')
            .annotate(c=Count('id'))
            .values_list('post_id', 'c')
        )
        posts = Post.objects.all()
        updated = 0
        for post in posts.iterator():
            actual = actual_counts.get(post.id, 0)
            if post.reply_count != actual:
                self.stdout.write(
                    f'{prefix}Post "{post.title}" (id={post.id}): '
                    f'reply_count {post.reply_count}->{actual}'
                )
                if not dry_run:
                    Post.objects.filter(pk=post.id).update(reply_count=actual)
                updated += 1
        self.stdout.write(self.style.SUCCESS(
            f'{prefix}{updated} posts had drifted reply_count. '
            f'{posts.count() - updated} posts were already correct.'
        ))

    def _recalculate_reply_reply_counts(self, dry_run, prefix):
        self.stdout.write(f'\n{prefix}Recalculating Reply.reply_count...')
        actual_counts = dict(
            Reply.objects.filter(parent_reply_id__isnull=False)
            .values('parent_reply_id')
            .annotate(c=Count('id'))
            .values_list('parent_reply_id', 'c')
        )
        replies = Reply.objects.all()
        updated = 0
        for reply in replies.iterator():
            actual = actual_counts.get(reply.id, 0)
            if reply.reply_count != actual:
                self.stdout.write(
                    f'{prefix}Reply id={reply.id}: '
                    f'reply_count {reply.reply_count}->{actual}'
                )
                if not dry_run:
                    Reply.objects.filter(pk=reply.id).update(reply_count=actual)
                updated += 1
        total = Reply.objects.count()
        self.stdout.write(self.style.SUCCESS(
            f'{prefix}{updated} replies had drifted reply_count. '
            f'{total - updated} replies were already correct.'
        ))