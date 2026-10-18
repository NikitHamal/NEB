"""Query budgets for the busiest pages. Each of these was hundreds of queries once (one per
user per deferred avatar field, one per row for images and likes); the budgets keep it that way."""
import time
import uuid

from django.core.cache import cache
from django.db import connection
from django.test import Client, TestCase
from django.test.utils import CaptureQueriesContext

from api.models import Post, Resource, User


class QueryBudgetTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        now = int(time.time() * 1000)
        users = [User(id=str(uuid.uuid4()), username=f'qb{i}', email=f'qb{i}@x.np', display_name=f'QB {i}',
                      email_verified=True, created_at=now, contribution_score=100 - i) for i in range(40)]
        User.objects.bulk_create(users)
        Post.objects.bulk_create([Post(id=str(uuid.uuid4()), user=users[i % 40], title=f'Q {i}', content='How?',
                                       category='Physics', created_at=now - i) for i in range(40)])
        Resource.objects.bulk_create([Resource(id=str(uuid.uuid4()), title=f'physics {i}', subject='Physics',
                                               grade_level='Class 12', type='PDF', approval_status='approved',
                                               is_lead=True, added_at=now - i, uploaded_by=users[i % 40],
                                               source_type='user') for i in range(40)])

    def setUp(self):
        cache.clear()
        self.client = Client()

    def assertBudget(self, url, budget):
        with CaptureQueriesContext(connection) as ctx:
            r = self.client.get(url)
        self.assertEqual(r.status_code, 200, url)
        self.assertLessEqual(len(ctx.captured_queries), budget, f'{url}: {len(ctx.captured_queries)} queries')

    def test_forum_does_not_query_per_contributor(self):
        self.assertBudget('/app/forum/', 30)

    def test_leaderboard_does_not_query_per_user(self):
        self.assertBudget('/app/forum/leaderboard/', 15)

    def test_search_api_does_not_query_per_row(self):
        self.assertBudget('/api/search/?q=physics', 20)

    def test_resources_api_does_not_query_per_row(self):
        self.assertBudget('/api/resources/', 12)

    def test_suggested_feed_does_not_query_per_card(self):
        self.assertBudget('/api/feed/suggested/', 20)
