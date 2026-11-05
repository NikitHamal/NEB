"""What posts and comments reveal about their author and the viewer."""
from types import SimpleNamespace

from django.test import TestCase

from api.models import Bookmark, Post, Reply, User
from api.serializers import PostSerializer, ReplySerializer
from api.utils import now_ms, uuid_str


def _user(name, **extra):
    return User.objects.create(
        id=f'u-{name}', username=name, email=f'{name}@example.com',
        email_verified=True, created_at=now_ms(), **extra,
    )


class ForumSerializerTests(TestCase):
    def setUp(self):
        self.author = _user('author')
        self.viewer = _user('viewer')
        self.post = Post.objects.create(
            id=uuid_str(), user=self.author, title='T', content='C', category='general',
            created_at=now_ms(),
        )
        self.reply = Reply.objects.create(
            id=uuid_str(), post=self.post, user=self.author, content='R', created_at=now_ms(),
        )

    def _data(self, serializer, obj, viewer=None, **context):
        request = SimpleNamespace(user=viewer) if viewer else None
        return serializer(obj, context={'request': request, **context}).data

    def test_public_content_names_its_author(self):
        for serializer, obj in ((PostSerializer, self.post), (ReplySerializer, self.reply)):
            data = self._data(serializer, obj)
            self.assertEqual(data['authorName'], 'author')
            self.assertEqual(data['authorId'], self.author.id)
            self.assertFalse(data['authorIsBot'])

    def test_anonymous_content_hides_the_author(self):
        Post.objects.filter(pk=self.post.pk).update(is_anonymous=True)
        Reply.objects.filter(pk=self.reply.pk).update(is_anonymous=True)
        self.post.refresh_from_db()
        self.reply.refresh_from_db()
        for serializer, obj in ((PostSerializer, self.post), (ReplySerializer, self.reply)):
            data = self._data(serializer, obj)
            self.assertNotEqual(data['authorName'], 'author')
            self.assertEqual((data['authorId'], data['authorPhotoUrl']), ('', ''))
            self.assertIsNone(data['authorBadgeInfo'])

    def test_deleted_author_is_labelled(self):
        self.author.delete()
        self.post.refresh_from_db()
        self.assertEqual(self._data(PostSerializer, self.post)['authorName'], 'Deleted user')

    def test_is_owner_only_for_the_author(self):
        self.assertTrue(self._data(PostSerializer, self.post, self.author)['isOwner'])
        self.assertFalse(self._data(PostSerializer, self.post, self.viewer)['isOwner'])
        self.assertFalse(self._data(PostSerializer, self.post)['isOwner'])

    def test_bookmark_state_reads_the_prefetched_set_or_the_table(self):
        Bookmark.objects.create(
            id=uuid_str(), user=self.viewer, target_type='reply', target_id=self.reply.id,
            created_at=now_ms(),
        )
        self.assertTrue(self._data(ReplySerializer, self.reply, self.viewer)['isBookmarked'])
        self.assertFalse(self._data(PostSerializer, self.post, self.viewer)['isBookmarked'])
        prefetched = self._data(ReplySerializer, self.reply, self.viewer, bookmarked_reply_ids=set())
        self.assertFalse(prefetched['isBookmarked'])
        self.assertFalse(self._data(ReplySerializer, self.reply)['isBookmarked'])

    def test_thumbs_up_uses_the_prefetched_set_for_its_own_kind(self):
        data = self._data(PostSerializer, self.post, self.viewer, liked_post_ids={self.post.id})
        self.assertTrue(data['isThumbedUp'])
        data = self._data(ReplySerializer, self.reply, self.viewer, liked_post_ids={self.reply.id},
                          liked_reply_ids=set())
        self.assertFalse(data['isThumbedUp'])

    def test_only_the_post_author_or_an_admin_can_label_a_comment(self):
        self.assertTrue(self._data(ReplySerializer, self.reply, self.author)['canLabel'])
        self.assertFalse(self._data(ReplySerializer, self.reply, self.viewer)['canLabel'])
        admin = _user('boss', is_admin=True)
        self.assertTrue(self._data(ReplySerializer, self.reply, admin)['canLabel'])
        self.assertFalse(self._data(ReplySerializer, self.reply)['canLabel'])
