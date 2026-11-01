import uuid

from django.test import TestCase

from api.cleanup import delete_reply_with_cleanup
from api.models import Post, Reply, User


def _user(username, **kw):
    return User.objects.create(
        id=str(uuid.uuid4()),
        username=username,
        email=f'{username}@example.com',
        email_verified=True,
        display_name=username.title(),
        **kw,
    )


class ReplyDeletionCounterTests(TestCase):
    def test_deleting_a_subtree_removes_every_reply_from_the_post_count(self):
        author = _user('counter_author')
        post = Post.objects.create(
            id=str(uuid.uuid4()), user=author, title='Thread',
            content='body', category='General', reply_count=3, created_at=1,
        )
        top = Reply.objects.create(
            id=str(uuid.uuid4()), post=post, user=author, content='top',
            reply_count=2, created_at=2,
        )
        child = Reply.objects.create(
            id=str(uuid.uuid4()), post=post, user=author, parent_reply=top,
            content='child', reply_count=1, created_at=3,
        )
        Reply.objects.create(
            id=str(uuid.uuid4()), post=post, user=author, parent_reply=child,
            content='grandchild', reply_count=0, created_at=4,
        )
        User.objects.filter(pk=author.pk).update(reply_count=3)

        delete_reply_with_cleanup(child.id)

        post.refresh_from_db()
        top.refresh_from_db()
        author.refresh_from_db()
        self.assertEqual(post.reply_count, 1)
        self.assertEqual(top.reply_count, 1)
        self.assertEqual(Reply.objects.filter(post=post).count(), 1)
        self.assertEqual(author.reply_count, 1)
