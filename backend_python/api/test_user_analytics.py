"""Member analytics: shape, windows, streaks, privacy and a fixed query budget."""
import uuid

from django.core.cache import cache
from django.db import connection
from django.test import Client, SimpleTestCase, TestCase
from django.test.utils import CaptureQueriesContext

from api import user_analytics as ua
from api.models import (Bookmark, Follow, Notification, Post, PostView, Reply, Resource, User, UserAuthToken)
from api.security import AUTH_TOKEN_TTL_MS, hash_auth_token
from api.utils import now_ms

DAY = ua.DAY_MS


class PureRuleTests(SimpleTestCase):
    def test_weekday_and_day_cut_follow_nepal_midnight(self):
        # 2024-01-01 (a Monday) 00:00 in Kathmandu is 2023-12-31 18:15 UTC.
        monday_midnight_utc = 1_704_046_500_000 - 0
        day = ua.day_of(monday_midnight_utc)
        self.assertEqual(ua.date_of(day).isoformat(), '2024-01-01')
        self.assertEqual(ua.weekday_of(day), 0)
        self.assertEqual(ua.day_of(monday_midnight_utc - 1), day - 1)
        self.assertEqual(ua.hour_of(monday_midnight_utc), 0)

    def test_streaks(self):
        today = 1000
        self.assertEqual(ua.streaks({1000, 999, 998, 990}, today)['current'], 3)
        s = ua.streaks({999, 998}, today)  # nothing yet today: the run still stands, but is at risk
        self.assertEqual((s['current'], s['atRisk'], s['activeToday']), (2, True, False))
        self.assertEqual(ua.streaks({1000, 995, 994, 993, 992}, today)['longest'], 4)
        self.assertEqual(ua.streaks(set(), today)['current'], 0)

    def test_pct_change_and_range(self):
        self.assertIsNone(ua.pct_change(5, 0))
        self.assertEqual(ua.pct_change(15, 10), 50)
        self.assertEqual(ua.clamp_range('90'), 90)
        self.assertEqual(ua.clamp_range('12'), ua.DEFAULT_RANGE)
        self.assertEqual(ua.clamp_range(None), ua.DEFAULT_RANGE)

    def test_heatmap_marks_the_future(self):
        today = ua.day_of(1_704_046_500_000)  # a Monday: six days of the week are still ahead
        h = ua.heatmap({today: 3, today - 1: 1}, today)
        self.assertEqual(len(h['cells']), ua.HEAT_WEEKS * 7)
        self.assertEqual([c['level'] for c in h['cells'][-6:]], [-1] * 6)
        self.assertEqual(h['cells'][-7]['count'], 3)


class MemberAnalyticsApiTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        now = now_ms()
        cls.now = now
        cls.me = User.objects.create(id='ua-me', username='uame', email='me@x.np', email_verified=True,
                                     created_at=now - 40 * DAY, contribution_score=70)
        cls.other = User.objects.create(id='ua-o', username='uaother', email='o@x.np', email_verified=True,
                                        created_at=now, contribution_score=500)
        cls.raw = f'tok-{uuid.uuid4().hex}'
        UserAuthToken.objects.create(id=str(uuid.uuid4()), user=cls.me, token_hash=hash_auth_token(cls.raw),
                                     created_at=now, last_used_at=now, revoked_at=0, expires_at=now + AUTH_TOKEN_TTL_MS)
        cls.p1 = Post.objects.create(id='ua-p1', user=cls.me, title='Newton laws', content='x', category='Physics',
                                     created_at=now - 1000, view_count=40, thumbs_up_count=4, reply_count=2)
        Post.objects.create(id='ua-p2', user=cls.me, title='Silent', content='x', category='Physics',
                            created_at=now - 3 * DAY, view_count=3)
        Post.objects.create(id='ua-p3', user=cls.other, title='Theirs', content='x', category='Maths', created_at=now)
        Reply.objects.create(id='ua-r1', post=cls.p1, user=cls.me, content='a', created_at=now - 2 * DAY,
                             kind='answer', label='accepted')
        Reply.objects.create(id='ua-r2', post=cls.p1, user=cls.other, content='b', created_at=now)
        Resource.objects.create(id='ua-res', title='Notes', subject='Physics, Maths', type='PDF', is_lead=True,
                                added_at=now - 5 * DAY, uploaded_by=cls.me, view_count=12, like_count=2)
        Follow.objects.create(follower=cls.other, following=cls.me, created_at=now - DAY)
        PostView.objects.create(id='ua-pv1', post=cls.p1, user=cls.other, viewed_at=now - DAY)
        PostView.objects.create(id='ua-pv2', post=cls.p1, user=cls.me, viewed_at=now - 2 * DAY)
        Bookmark.objects.create(id='ua-b1', user=cls.me, target_type='post', target_id='ua-p3', created_at=now)
        Notification.objects.create(id='ua-n1', recipient=cls.me, actor=cls.other, verb='like_post',
                                    target_type='post', target_id='ua-p1', created_at=now - DAY)

    def setUp(self):
        cache.clear()
        self.client = Client()

    def get(self, path='/api/users/me/analytics/', budget=None):
        with CaptureQueriesContext(connection) as ctx:
            r = self.client.get(path, HTTP_AUTHORIZATION=f'Bearer {self.raw}')
        self.assertEqual(r.status_code, 200, r.content)
        if budget:
            self.assertLessEqual(len(ctx), budget, [q['sql'][:90] for q in ctx.captured_queries])
        return r.json()

    def test_requires_auth(self):
        self.assertIn(Client().get('/api/users/me/analytics/').status_code, (401, 403))

    def test_shape_and_numbers(self):
        d = self.get(budget=34)
        self.assertEqual(d['version'], 2)
        self.assertEqual(d['range']['days'], 30)
        self.assertEqual(len(d['trend']), 30)
        self.assertEqual(len(d['overview']), 6)
        by = {k['key']: k for k in d['overview']}
        self.assertEqual(by['contributions']['value'], 4)  # 2 posts + 1 reply + 1 resource
        self.assertEqual(by['likes']['value'], 1)
        self.assertEqual(by['followers']['value'], 1)
        self.assertEqual(by['readers']['value'], 1)  # the member's own view is not a reader
        self.assertEqual(by['contributions']['series'][-1], 1)  # the first post, written just now
        self.assertEqual(d['stats']['posts'], 2)
        self.assertEqual(d['stats']['postViews'], 43)
        self.assertEqual(d['stats']['bookmarks'], 1)
        self.assertEqual(d['helpfulness']['goodLabels'], 1)
        self.assertEqual(d['helpfulness']['answersWritten'], 1)
        self.assertEqual((d['streak']['current'], d['streak']['longest']), (1, 2))  # today; then 2 and 3 days ago
        self.assertTrue(d['streak']['activeToday'])
        self.assertEqual(d['standing']['level'], 3)
        self.assertEqual(d['standing']['topPercent'], 100)  # one of two scored members is above
        self.assertEqual(d['topPosts'][0]['id'], 'ua-p1')
        self.assertEqual([c['label'] for c in d['topSubjects']], ['Physics', 'Maths'])
        self.assertEqual(len(d['heatmap']['cells']), 17 * 7)
        self.assertEqual(len(d['rhythm']['hours']), 24)
        self.assertTrue(any(i['id'] == 'unanswered' for i in d['insights']))

    def test_legacy_keys_remain(self):
        d = self.get()
        for key in ('stats', 'activityDays', 'topCategories', 'topSubjects', 'topPosts', 'topResources', 'suggestions'):
            self.assertIn(key, d)
        self.assertEqual(len(d['activityDays']), 14)
        for gone in ('studyDocs', 'quizzes', 'flashcards'):
            self.assertNotIn(gone, d['stats'])

    def test_range_param(self):
        self.assertEqual(len(self.get('/api/users/me/analytics/?days=7')['trend']), 7)
        self.assertEqual(len(self.get('/api/users/me/analytics/?days=90')['trend']), 90)
        self.assertEqual(len(self.get('/api/users/me/analytics/?days=5')['trend']), 30)

    def test_never_includes_other_members(self):
        d = self.get()
        self.assertNotIn('Theirs', str(d))
        self.assertNotIn('uaother', str(d))
