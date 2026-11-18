"""Profile overview (api/profile_glance.py): three glance tiles and Studying now, public data only."""
import time
import uuid

from django.core.cache import cache
from django.test import Client, TestCase

from api.models import Post, Reply, Resource, User
from api.profile_glance import build, short


def _user(**kw):
    d = {'id': str(uuid.uuid4()), 'username': f'u_{uuid.uuid4().hex[:8]}', 'email': f'{uuid.uuid4().hex[:8]}@t.com',
         'created_at': int(time.time() * 1000), 'email_verified': True, 'display_name': 'T', 'gender': 'Other',
         'dob': '2005-06-15', 'role': 'student', 'class_level': 'Class 11'}
    d.update(kw)
    return User.objects.create(**d)


def _post(user, **kw):
    d = {'id': str(uuid.uuid4()), 'user': user, 'title': 'Current electricity', 'content': 'x', 'category': 'Physics',
         'created_at': int(time.time() * 1000)}
    d.update(kw)
    return Post.objects.create(**d)


class ShortTests(TestCase):
    def test_short_numbers(self):
        self.assertEqual([short(n) for n in (0, 999, 1200, 12400, 212000, 1_500_000)],
                         ['0', '999', '1.2k', '12k', '212k', '1.5M'])


class GlanceTests(TestCase):
    def setUp(self):
        cache.clear()

    def test_empty_member_has_three_tiles_and_no_studying_card(self):
        out = build(_user())
        self.assertEqual(len(out['glance']), 3)
        self.assertIsNone(out['studying'])

    def test_student_tiles_and_studying_now(self):
        u = _user()
        post = _post(u, view_count=1240)
        Reply.objects.create(id=str(uuid.uuid4()), post=post, user=u, content='a', kind='answer', label='accepted',
                             created_at=int(time.time() * 1000))
        out = build(u)
        self.assertEqual([g['label'] for g in out['glance']], ['Reads on my posts', 'Accepted answers', 'Day streak'])
        self.assertEqual(out['glance'][0]['value'], '1.2k')
        self.assertEqual(out['glance'][2]['value'], '1')
        s = out['studying']
        self.assertEqual((s['subject'], s['postId'], s['streak']), ('Physics', post.id, 1))
        self.assertEqual(len(s['week']), 7)
        self.assertGreaterEqual(s['today'], 1)

    def test_anonymous_posts_never_show(self):
        u = _user()
        _post(u, is_anonymous=True, view_count=500)
        out = build(u)
        self.assertEqual(out['glance'][0]['value'], '0')
        self.assertIsNone(out['studying'])

    def test_contributor_tiles_use_approved_resources_only(self):
        u = _user()
        now = int(time.time() * 1000)
        for status, views in (('approved', 2400), ('pending', 9000)):
            Resource.objects.create(id=str(uuid.uuid4()), title='N', uploaded_by=u, added_at=now, approval_status=status,
                                    view_count=views, download_count=10, like_count=3)
        out = build(u)
        self.assertEqual([g['label'] for g in out['glance']], ['Total reads', 'Downloads', 'Likes'])
        self.assertEqual(out['glance'][0]['value'], '2.4k')
        self.assertIsNone(out['studying'])

    def test_stats_endpoint_returns_glance(self):
        u = _user()
        r = Client().get(f'/api/users/profile/{u.username}/stats/')
        self.assertEqual(r.status_code, 200)
        body = r.json()
        self.assertEqual(len(body['glance']), 3)
        self.assertIn('studying', body)
