"""Remove a bot account's forum content without touching the account itself.

Policy for this cleanup:
  * every post authored by the bot is deleted (with its replies),
  * bot replies on other people's posts are deleted unless a human replied to
    that bot reply (``--no-keep-replied`` overrides),
  * the bot's likes and follows are removed through the normal services so
    target counters stay correct,
  * autonomy is switched off; mention-triggered replies keep working.

Default is a dry run. Pass ``--apply`` to delete. A JSON snapshot of everything
the command touches is written to ``backups/`` before the first delete.
"""
import json
import os
import time

from django.conf import settings
from django.core.cache import cache
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

from api import services
from api.cleanup import delete_post_with_cleanup, delete_reply_with_cleanup
from api.models import (
    Follow, NebyTask, Post, PostLike, Reply, ReplyLike, User,
)


class Command(BaseCommand):
    help = 'Delete a bot account\'s posts/replies, preserving bot replies that humans answered.'

    def add_arguments(self, parser):
        parser.add_argument('--username', required=True, help='Bot username to purge')
        parser.add_argument('--apply', action='store_true', help='Actually delete (default: dry run)')
        parser.add_argument(
            '--no-keep-replied',
            dest='keep_replied',
            action='store_false',
            default=True,
            help='Also delete bot replies that received a human reply',
        )
        parser.add_argument(
            '--keep-autonomy',
            action='store_true',
            help='Do not switch the bot persona to autonomy off',
        )

    def handle(self, *args, **options):
        username = options['username'].strip()
        bot = User.objects.filter(username__iexact=username, is_bot=True).first()
        if not bot:
            raise CommandError(f'No bot user named @{username}.')

        posts = list(Post.objects.filter(user=bot).order_by('created_at'))
        bot_replies = list(
            Reply.objects.filter(user=bot)
            .exclude(post__user=bot)
            .select_related('post')
            .order_by('created_at')
        )

        delete_replies, keep_replies = [], []
        for reply in bot_replies:
            human_children = list(
                Reply.objects.filter(parent_reply=reply).exclude(user=bot).select_related('user')
            )
            if options['keep_replied'] and human_children:
                keep_replies.append((reply, human_children))
            else:
                delete_replies.append(reply)

        post_ids = [p.id for p in posts]
        reply_ids = [r.id for r in delete_replies]

        post_likes = PostLike.objects.filter(user=bot).select_related('post')
        reply_likes = ReplyLike.objects.filter(user=bot).select_related('reply')
        follows = Follow.objects.filter(follower=bot).select_related('following')

        self.stdout.write(self.style.MIGRATE_HEADING(f'Purge plan for @{bot.username}'))
        self.stdout.write(f'  posts to delete:       {len(posts)}')
        for post in posts:
            self.stdout.write(f'    - {post.title[:90]}')
        self.stdout.write(f'  bot replies to delete: {len(delete_replies)}')
        self.stdout.write(f'  bot replies to keep:   {len(keep_replies)} (human reply exists)')
        for reply, children in keep_replies:
            child_names = ', '.join(sorted({c.user.username for c in children if c.user}))
            self.stdout.write(f'    - on "{reply.post.title[:60]}" (replied by {child_names})')
        self.stdout.write(f'  likes to remove:       {post_likes.count()} posts, {reply_likes.count()} replies')
        self.stdout.write(f'  follows to remove:     {follows.count()}')

        if not options['apply']:
            self.stdout.write(self.style.WARNING('\nDry run. Re-run with --apply to delete.'))
            return

        snapshot_path = self._write_snapshot(bot, posts, bot_replies, post_likes, reply_likes, follows)
        self.stdout.write(self.style.SUCCESS(f'\nSnapshot: {snapshot_path}'))

        if not options['keep_autonomy']:
            from api.agent_social.models import AgentPersona
            updated = AgentPersona.objects.filter(user_id=bot.id).update(autonomy_enabled=False)
            self.stdout.write(f'Autonomy off for {updated} persona(s).')

        for post in posts:
            delete_post_with_cleanup(post.id)
        self.stdout.write(f'Deleted {len(posts)} post(s).')

        deleted = 0
        for reply in delete_replies:
            try:
                delete_reply_with_cleanup(reply.id)
                deleted += 1
            except Reply.DoesNotExist:
                pass
        self.stdout.write(f'Deleted {deleted} bot repl(y/ies).')

        for like in list(PostLike.objects.filter(user=bot)):
            try:
                services.toggle_post_like(bot, like.post_id)
            except Post.DoesNotExist:
                pass
        for like in list(ReplyLike.objects.filter(user=bot)):
            try:
                services.toggle_reply_like(bot, like.reply_id)
            except Reply.DoesNotExist:
                pass
        for follow in list(Follow.objects.filter(follower=bot)):
            services.toggle_follow(bot, follow.following_id, desired='unfollow')
        self.stdout.write('Removed remaining bot likes/follows.')

        call_command('recalculate_counters', verbosity=0)
        cache.delete_many([
            'home_resources', 'home_posts', 'home_stats_v2', 'forum_all_posts',
            'forum_contributors', 'sitemap_xml', 'admin_stats',
        ])
        try:
            cache.delete_pattern('forum_hot_ids:*')
        except AttributeError:
            pass

        remaining_posts = Post.objects.filter(user=bot).count()
        remaining_replies = Reply.objects.filter(user=bot).count()
        self.stdout.write(self.style.SUCCESS(
            f'Done. @{bot.username} now has {remaining_posts} post(s), {remaining_replies} repl(y/ies).'
        ))
        self.stdout.write('Replies on bot posts that humans wrote are deleted with the post, per policy.')

    def _write_snapshot(self, bot, posts, bot_replies, post_likes, reply_likes, follows):
        payload = {
            'created_at': int(time.time()),
            'bot': {'id': bot.id, 'username': bot.username},
            'posts': list(Post.objects.filter(id__in=[p.id for p in posts]).values()),
            'post_replies': list(
                Reply.objects.filter(post_id__in=[p.id for p in posts]).values()
            ),
            'bot_replies': list(
                Reply.objects.filter(id__in=[r.id for r in bot_replies]).values()
            ),
            'post_likes': list(post_likes.values()),
            'reply_likes': list(reply_likes.values()),
            'follows': list(follows.values()),
            'tasks': list(NebyTask.objects.filter(post_id__in=[p.id for p in posts]).values()),
        }
        directory = os.path.join(settings.BASE_DIR, 'backups')
        os.makedirs(directory, exist_ok=True)
        filename = f'purge_{bot.username}_{int(time.time())}.json'
        path = os.path.join(directory, filename)
        with open(path, 'w', encoding='utf-8') as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=2, default=str)
        return path
