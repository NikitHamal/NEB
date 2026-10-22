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


class SignedInQueryBudgetTests(TestCase):
    """The same, for the pages a signed-in student sees. Each budget is the page's count with
    the batching in place; a per-row lookup coming back pushes it past the budget."""

    @classmethod
    def setUpTestData(cls):
        from api.models import Bookmark, Poll, PollOption, PostImage, Reply
        now = int(time.time() * 1000)
        cls.me = User.objects.create(id=str(uuid.uuid4()), username='qb_me', email='qb_me@x.np', display_name='Me',
                                     gender='female', class_level='12', email_verified=True, created_at=now)
        authors = [User(id=str(uuid.uuid4()), username=f'qbs{i}', email=f'qbs{i}@x.np', email_verified=True,
                        created_at=now) for i in range(12)]
        User.objects.bulk_create(authors)
        posts = [Post(id=str(uuid.uuid4()), user=authors[i % 12], title=f'Accountancy {i}', content='How?',
                      category='Accountancy', created_at=now - i) for i in range(12)]
        Post.objects.bulk_create(posts)
        PostImage.objects.bulk_create([PostImage(id=str(uuid.uuid4()), post=p, image_url=f'https://x.np/{p.id}.png',
                                                 created_at=now) for p in posts])
        polls = [Poll(id=str(uuid.uuid4()), post=p, question='Which?', created_at=now) for p in posts[:6]]
        Poll.objects.bulk_create(polls)
        PollOption.objects.bulk_create([PollOption(id=str(uuid.uuid4()), poll=poll, text=f'Option {k}', order=k)
                                        for poll in polls for k in range(3)])
        replies = [Reply(id=str(uuid.uuid4()), post=posts[i], user=authors[(i + 1) % 12], content='Like this.',
                         created_at=now - i) for i in range(12)]
        Reply.objects.bulk_create(replies)
        resources = [Resource(id=str(uuid.uuid4()), title=f'Accountancy notes {i}', subject='Accountancy',
                              grade_level='Class 12', type='PDF', approval_status='approved', is_lead=True,
                              added_at=now - i, uploaded_by=authors[i % 12], source_type='user') for i in range(12)]
        Resource.objects.bulk_create(resources)
        Bookmark.objects.bulk_create(
            [Bookmark(id=str(uuid.uuid4()), user=cls.me, target_type='post', target_id=p.id, created_at=now - k)
             for k, p in enumerate(posts)]
            + [Bookmark(id=str(uuid.uuid4()), user=cls.me, target_type='reply', target_id=r.id, created_at=now - 50 - k)
               for k, r in enumerate(replies)]
            + [Bookmark(id=str(uuid.uuid4()), user=cls.me, target_type='resource', target_id=r.id,
                        created_at=now - 100 - k) for k, r in enumerate(resources)])

    def setUp(self):
        from api.security import issue_auth_token
        from api.serializers import UserSerializer
        cache.clear()
        self.client = Client()
        session = self.client.session
        session['auth_token'] = issue_auth_token(self.me)
        session['user_data'] = dict(UserSerializer(self.me).data)
        session.save()

    def assertBudget(self, url, budget):
        with CaptureQueriesContext(connection) as ctx:
            r = self.client.get(url)
        self.assertEqual(r.status_code, 200, url)
        self.assertLessEqual(len(ctx.captured_queries), budget, f'{url}: {len(ctx.captured_queries)} queries')
        return r

    def test_bookmarks_do_not_query_per_bookmark(self):
        r = self.assertBudget('/app/bookmarks/', 11)
        self.assertContains(r, 'Accountancy notes 11')
        self.assertContains(r, 'Reply on Accountancy 11')
