import json
import uuid

from django.test import Client, TestCase

from api.models import User, Post, Reply
from api.blobatar.render import resolve
from api.blobatar.color import contrast, from_hex, to_hex
from web.view_helpers import _build_local_stats


def _mk_user(username, **kw):
    return User.objects.create(
        id=str(uuid.uuid4()),
        username=username,
        email=f'{username}@example.com',
        email_verified=True,
        display_name=username.title(),
        gender='Male',
        class_level='12',
        role='student',
        **kw,
    )


class AnonymousPrivacyTests(TestCase):
    def setUp(self):
        self.owner = _mk_user('privacy_owner')
        self.viewer = _mk_user('privacy_viewer')
        self.post = Post.objects.create(
            id=str(uuid.uuid4()), user=self.owner, title='Normal post',
            content='public content', category='study', created_at=3000,
        )
        self.anon_post = Post.objects.create(
            id=str(uuid.uuid4()), user=self.owner, title='Anonymous post',
            content='hidden content', category='study', created_at=2000,
            is_anonymous=True,
        )
        self.reply = Reply.objects.create(
            id=str(uuid.uuid4()), user=self.owner, post=self.post,
            content='normal reply', created_at=4000,
        )
        self.anon_reply = Reply.objects.create(
            id=str(uuid.uuid4()), user=self.owner, post=self.post,
            content='anonymous reply', created_at=1000, is_anonymous=True,
        )
        self.owner.post_count = 2
        self.owner.reply_count = 2
        self.owner.save(update_fields=['post_count', 'reply_count'])

    def _logged_in(self, client, user):
        s = client.session
        s['user_data'] = {'id': user.id, 'username': user.username, 'gender': user.gender}
        s.save()

    def test_profile_page_excludes_anonymous(self):
        client = Client()
        self._logged_in(client, self.viewer)
        resp = client.get(f'/profile/{self.owner.username}/')
        self.assertEqual(resp.status_code, 200)
        post_ids = [p['id'] for p in resp.context['user_posts']]
        reply_ids = [r['id'] for r in resp.context['user_replies']]
        self.assertIn(self.post.id, post_ids)
        self.assertNotIn(self.anon_post.id, post_ids)
        self.assertIn(self.reply.id, reply_ids)
        self.assertNotIn(self.anon_reply.id, reply_ids)
        self.assertEqual(resp.context['stats']['post_count'], 1)
        self.assertEqual(resp.context['stats']['reply_count'], 1)

    def test_ajax_profile_activity_excludes_anonymous(self):
        client = Client()
        self._logged_in(client, self.viewer)
        resp = client.get(f'/ajax/profile/{self.owner.username}/activity/')
        data = json.loads(resp.content)
        post_ids = [p['id'] for p in data['posts']]
        self.assertIn(self.post.id, post_ids)
        self.assertNotIn(self.anon_post.id, post_ids)
        self.assertEqual(data['total_count'], 1)

    def test_ajax_profile_replies_excludes_anonymous(self):
        client = Client()
        self._logged_in(client, self.viewer)
        resp = client.get(f'/ajax/profile/{self.owner.username}/replies/')
        data = json.loads(resp.content)
        reply_ids = [r['id'] for r in data['replies']]
        self.assertIn(self.reply.id, reply_ids)
        self.assertNotIn(self.anon_reply.id, reply_ids)
        self.assertEqual(data['total_count'], 1)

    def test_instant_search_excludes_anonymous_posts(self):
        client = Client()
        self._logged_in(client, self.viewer)
        resp = client.get('/ajax/search/?q=content')
        data = json.loads(resp.content)
        post_ids = [p['id'] for p in data['results']['posts']]
        self.assertIn(self.post.id, post_ids)
        self.assertNotIn(self.anon_post.id, post_ids)

    def test_api_stats_exclude_anonymous(self):
        from rest_framework.test import APIClient
        client = APIClient()
        client.force_authenticate(user=self.viewer)
        resp = client.get(f'/api/users/profile/{self.owner.username}/stats/')
        self.assertEqual(resp.status_code, 200, resp.data)
        self.assertEqual(resp.data['post_count'], 1)
        self.assertEqual(resp.data['reply_count'], 1)

    def test_build_local_stats_exclude_anonymous(self):
        stats = _build_local_stats(self.owner, exclude_anonymous=True)
        self.assertEqual(stats['post_count'], 1)
        self.assertEqual(stats['reply_count'], 1)
        stats_all = _build_local_stats(self.owner)
        self.assertEqual(stats_all['post_count'], 2)


class BlobatarContrastTests(TestCase):
    def test_blue_bgcolor_forces_visible_head(self):
        default = resolve('privacy_test')
        overridden = resolve('privacy_test', {'palette': {'bg': '#0000ff'}})
        head = overridden['palette']['head']
        ratio = contrast(from_hex(head), from_hex('#0000ff'))
        self.assertGreaterEqual(ratio, 1.25)
        self.assertNotEqual(head, default['palette']['head'])
        eye_ratio = contrast(from_hex(overridden['palette']['eye']), from_hex(head))
        self.assertGreaterEqual(eye_ratio, 4.5)

    def test_light_bgcolor_keeps_dark_head(self):
        resolved = resolve('privacy_test', {'palette': {'bg': '#ffffff'}})
        head = resolved['palette']['head']
        ratio = contrast(from_hex(head), from_hex('#ffffff'))
        self.assertGreaterEqual(ratio, 1.25)

    def test_no_override_unchanged(self):
        default = resolve('privacy_test')
        self.assertEqual(default['palette']['head'], to_hex(from_hex(default['palette']['head'])))