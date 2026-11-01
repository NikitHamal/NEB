import os
import shutil
import tempfile
import uuid
from unittest import mock

from django.core.cache import cache
from django.core.management import call_command
from django.test import TestCase, override_settings

from api.models import Follow, Post, PostLike, Reply, User


def _user(username, **kw):
    return User.objects.create(
        id=str(uuid.uuid4()),
        username=username,
        email=f'{username}@example.com',
        email_verified=True,
        display_name=username.title(),
        **kw,
    )


class PurgeBotContentTests(TestCase):
    def setUp(self):
        cache.clear()
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.bot = _user('neby', is_bot=True)
        self.human = _user('human')

        self.bot_post = Post.objects.create(
            id=str(uuid.uuid4()), user=self.bot, title='Bot explainer',
            content='body', category='Science', reply_count=1, created_at=1,
        )
        self.human_on_bot_post = Reply.objects.create(
            id=str(uuid.uuid4()), post=self.bot_post, user=self.human,
            content='thanks neby', created_at=2,
        )

        self.human_post = Post.objects.create(
            id=str(uuid.uuid4()), user=self.human, title='Human question',
            content='body', category='Math', reply_count=3, created_at=3,
        )
        self.kept_bot_reply = Reply.objects.create(
            id=str(uuid.uuid4()), post=self.human_post, user=self.bot,
            content='helpful answer', reply_count=1, created_at=4,
        )
        self.human_child = Reply.objects.create(
            id=str(uuid.uuid4()), post=self.human_post, user=self.human,
            parent_reply=self.kept_bot_reply, content='that helped', created_at=5,
        )
        self.dead_bot_reply = Reply.objects.create(
            id=str(uuid.uuid4()), post=self.human_post, user=self.bot,
            content='drive-by comment', reply_count=0, created_at=6,
        )

        PostLike.objects.create(post=self.human_post, user=self.bot)
        Follow.objects.create(follower=self.bot, following=self.human, created_at=7)

    def _fake_unlike_post(self, user, post_id):
        PostLike.objects.filter(user=user, post_id=post_id).delete()
        return {'isThumbedUp': False}

    def _fake_unlike_reply(self, user, reply_id):
        return {'isThumbedUp': False}

    def _fake_unfollow(self, user, target_id, desired=None):
        Follow.objects.filter(follower=user, following_id=target_id).delete()
        return {'isFollowing': False}, 200

    def test_dry_run_then_apply_keeps_only_replied_bot_comments(self):
        with override_settings(BASE_DIR=self.tmp):
            call_command('purge_bot_content', username='neby', verbosity=0)
            self.assertTrue(Post.objects.filter(pk=self.bot_post.pk).exists())
            self.assertTrue(Reply.objects.filter(pk=self.dead_bot_reply.pk).exists())

            with mock.patch(
                'api.management.commands.purge_bot_content.services.toggle_post_like',
                side_effect=self._fake_unlike_post,
            ), mock.patch(
                'api.management.commands.purge_bot_content.services.toggle_reply_like',
                side_effect=self._fake_unlike_reply,
            ), mock.patch(
                'api.management.commands.purge_bot_content.services.toggle_follow',
                side_effect=self._fake_unfollow,
            ):
                call_command('purge_bot_content', username='neby', apply=True, verbosity=0)

        self.assertFalse(Post.objects.filter(pk=self.bot_post.pk).exists())
        self.assertFalse(Reply.objects.filter(pk=self.human_on_bot_post.pk).exists())
        self.assertFalse(Reply.objects.filter(pk=self.dead_bot_reply.pk).exists())
        self.assertTrue(Reply.objects.filter(pk=self.kept_bot_reply.pk).exists())
        self.assertTrue(Reply.objects.filter(pk=self.human_child.pk).exists())
        self.assertFalse(PostLike.objects.filter(user=self.bot).exists())
        self.assertFalse(Follow.objects.filter(follower=self.bot).exists())

        self.human_post.refresh_from_db()
        self.assertEqual(self.human_post.reply_count, 2)
        self.assertTrue(os.path.isdir(os.path.join(self.tmp, 'backups')))
        self.assertTrue(os.listdir(os.path.join(self.tmp, 'backups')))
