"""Query budgets for the API endpoints the Android app calls most.

Each list below holds 25-40 rows, so a query per row (the N+1 these budgets replaced: one
per follower, per paid card, per analytics number, per related announcement) would blow
the budget many times over. See scripts/perf_probe.py for the measurements behind them."""
import uuid
from decimal import Decimal

from django.core.cache import cache
from django.db import connection
from django.test import Client, TestCase
from django.test.utils import CaptureQueriesContext

from api.models import (Announcement, Bookmark, Follow, Notification, PaymentVerification, Post, PostImage, PostLike,
                        Reply, Resource, ResourceLike, User, UserAuthToken)
from api.security import AUTH_TOKEN_TTL_MS, hash_auth_token
from api.utils import now_ms

N = 30


class ApiQueryBudgetTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        now = now_ms()
        users = [User(id=f'qb-{i}', username=f'qb{i}', email=f'qb{i}@x.np', display_name=f'QB {i}', email_verified=True,
                      created_at=now, school='Alpha School', class_level='12', verification_level=i % 3,
                      photo_url=f'https://example.np/{i}.png' if i % 2 else None) for i in range(N + 2)]
        User.objects.bulk_create(users)
        cls.viewer, cls.star, others = users[0], users[1], users[2:]
        cls.raw_token = f'tok-{uuid.uuid4().hex}'
        UserAuthToken.objects.create(id=str(uuid.uuid4()), user=cls.viewer, token_hash=hash_auth_token(cls.raw_token),
                                     created_at=now, last_used_at=now, revoked_at=0, expires_at=now + AUTH_TOKEN_TTL_MS)
        Follow.objects.bulk_create([Follow(follower=u, following=cls.star, created_at=now - i) for i, u in enumerate(others)]
                                   + [Follow(follower=cls.star, following=u, created_at=now - i) for i, u in enumerate(others)]
                                   + [Follow(follower=cls.viewer, following=u, created_at=now) for u in others[:20]])
        posts = [Post(id=f'qp-{i}', user=others[i % len(others)], title=f'physics energy {i}', content='force?',
                      category='Physics', created_at=now - i) for i in range(N)]
        Post.objects.bulk_create(posts)
        cls.busy_post = posts[0]
        PostImage.objects.bulk_create([PostImage(id=f'qi-{i}', post=p, image_url='/media/x.jpg', created_at=now)
                                       for i, p in enumerate(posts)])
        PostLike.objects.bulk_create([PostLike(post=p, user=cls.viewer) for p in posts[::2]])
        Reply.objects.bulk_create([Reply(id=f'qr-{i}', post=cls.busy_post, user=others[i % len(others)], content='yes',
                                         created_at=now + i) for i in range(N)])
        resources = [Resource(id=f'qres-{i}', title=f'physics notes {i}', subject='Physics', grade_level='Class 12',
                              type='PDF', approval_status='approved', is_lead=True, added_at=now - i,
                              uploaded_by=others[i % len(others)], source_type='user', is_paid=i % 3 == 0,
                              price=Decimal('50') if i % 3 == 0 else Decimal('0')) for i in range(N)]
        Resource.objects.bulk_create(resources)
        cls.resource = resources[1]
        ResourceLike.objects.bulk_create([ResourceLike(resource=r, user=cls.viewer) for r in resources[::4]])
        PaymentVerification.objects.bulk_create([
            PaymentVerification(id=f'qpv-{i}', buyer=cls.viewer, resource=r, seller=r.uploaded_by, amount=r.price,
                                status=('approved', 'pending', 'rejected')[i % 3], created_at=now)
            for i, r in enumerate(resources[::3])])
        Bookmark.objects.bulk_create([Bookmark(id=f'qbm-{i}', user=cls.viewer, target_type='post', target_id=p.id,
                                               created_at=now - i) for i, p in enumerate(posts[:20])])
        Notification.objects.bulk_create([Notification(id=f'qn-{i}', recipient=cls.viewer, actor=others[i % len(others)],
                                                       verb='like_post', target_type='post', target_id=posts[0].id,
                                                       created_at=now - i) for i in range(40)])
        Announcement.objects.bulk_create([Announcement(id=f'qa-{i}', title=f'Notice {i}', slug=f'notice-{i}',
                                                       content='Results are out.', category='notice', status='published',
                                                       author=others[i], published_at=now - i, created_at=now)
                                          for i in range(6)])

    def setUp(self):
        cache.clear()
        self.client = Client()

    def get(self, url, budget, signed_in=True, status=200):
        headers = {'HTTP_AUTHORIZATION': f'Bearer {self.raw_token}'} if signed_in else {}
        with CaptureQueriesContext(connection) as ctx:
            r = self.client.get(url, **headers)
        self.assertEqual(r.status_code, status, url)
        sql = [q['sql'] for q in ctx.captured_queries]
        self.assertLessEqual(len(sql), budget, f'{url}: {len(sql)} queries\n' + '\n'.join(s[:150] for s in sql))
        return r, sql

    def test_follower_lists_join_both_users(self):
        for who in (self.star, self.viewer):
            self.get(f'/api/users/{who.id}/followers/', 4)
            self.get(f'/api/users/{who.id}/following/', 4)
        self.get(f'/api/users/{self.star.id}/followers/', 3, signed_in=False)

    def test_private_analytics_is_a_fixed_number_of_aggregates(self):
        r, _sql = self.get('/api/users/me/analytics/', 20)
        self.assertEqual(len(r.json()['activityDays']), 14)

    def test_resource_cards_do_not_query_per_paid_card(self):
        r, _sql = self.get('/api/resources/?page_size=50', 8)
        self.assertEqual(len(r.json()['results']), N)
        self.get('/api/resources/?sort=trending&page_size=50', 8)
        self.get('/api/resources/?page_size=50', 3, signed_in=False)

    def test_resource_detail_reads_like_state_once(self):
        r, _sql = self.get(f'/api/resources/{self.resource.id}/', 4)
        self.assertTrue(r.json()['isLiked'] is r.json()['is_liked'])

    def test_search_does_not_count_matches(self):
        r, sql = self.get('/api/search/?q=physics', 16)
        self.assertEqual(len(r.json()['resources']), 25)
        self.assertFalse([s for s in sql if 'COUNT(' in s.upper()], 'search counted rows it never returns')
        self.get('/api/search/?q=physics', 7, signed_in=False)
        self.get('/api/search/?q=physics&page=99', 4, status=404)

    def test_notifications_page_without_a_count(self):
        r, sql = self.get('/api/notifications/', 2)
        self.assertEqual(len(r.json()['notifications']), 30)
        self.assertFalse([s for s in sql if 'COUNT(' in s.upper()])
        self.get('/api/notifications/?page=9', 2, status=404)

    def test_forum_lists(self):
        self.get('/api/posts/', 10)
        self.get('/api/posts/?sort=discussed', 10)
        self.get(f'/api/posts/{self.busy_post.id}/replies/', 6)
        self.get('/api/bookmarks/', 3)

    def test_suggested_feed(self):
        self.get('/api/feed/suggested/', 17)
        self.get('/api/feed/suggested/', 7)  # interests and candidate pools now cached

    def test_profile_popup_and_stats(self):
        self.get(f'/ajax/user-popup/{self.star.username}/', 5)
        self.get(f'/api/users/profile/{self.star.username}/stats/', 7)

    def test_news_detail_joins_related_authors(self):
        self.get('/app/news/notice-0/', 11, signed_in=False)  # 15 when the 4 related authors were fetched one by one
