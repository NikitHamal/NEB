"""The suggested feed ranks for the reader, spreads topics and authors, and stays cheap."""
import time
import uuid

from django.core.cache import cache
from django.db import connection
from django.test import TestCase
from django.test.utils import CaptureQueriesContext

from .models import Bookmark, Post, Resource, User
from .views_feed import build_suggested_deck


def _user(name, **kw):
    return User.objects.create(id=str(uuid.uuid4()), username=name, email=f'{name}@x.np', display_name=name,
                               email_verified=True, created_at=int(time.time() * 1000), **kw)


class FeedRankingTests(TestCase):
    def setUp(self):
        cache.clear()
        now = int(time.time() * 1000)
        self.me = _user('me', class_level='12')
        self.prolific = _user('prolific')
        self.other = _user('other')
        Post.objects.bulk_create([Post(id=str(uuid.uuid4()), user=self.prolific, title=f'P{i}', content='x', category='Physics',
                                       created_at=now - i * 1000) for i in range(12)])
        Post.objects.bulk_create([Post(id=str(uuid.uuid4()), user=self.other, title=f'C{i}', content='x', category='Chemistry',
                                       created_at=now - 3_600_000 - i) for i in range(4)])
        self.mine = Post.objects.create(id=str(uuid.uuid4()), user=self.me, title='Mine', content='x', category='Biology', created_at=now)
        Resource.objects.bulk_create([Resource(id=str(uuid.uuid4()), title=f'R{i}', subject=s, grade_level=g, type='PDF',
                                               approval_status='approved', added_at=now - i, uploaded_by=self.other, source_type='user')
                                      for i, (s, g) in enumerate([('Maths', 'Class 11'), ('Maths', 'Class 12'), ('English', 'Class 10')])])

    def test_one_author_cannot_fill_the_deck(self):
        deck, _ = build_suggested_deck(self.me, limit=12)
        posts = [o for k, o in deck if k == 'post']
        self.assertTrue(any(p.user_id == self.other.id for p in posts[:4]), 'a second author appears near the top')

    def test_your_own_posts_are_not_suggested_to_you(self):
        deck, _ = build_suggested_deck(self.me, limit=18)
        self.assertNotIn(self.mine, [o for k, o in deck if k == 'post'])

    def test_your_class_lifts_its_resources(self):
        deck, _ = build_suggested_deck(self.me, limit=18)
        first = next(o for k, o in deck if k == 'resource')
        self.assertEqual(first.grade_level, 'Class 12')

    def test_interests_are_weighted_and_cached(self):
        chem = Post.objects.filter(category='Chemistry').first()
        Bookmark.objects.create(id=str(uuid.uuid4()), user=self.me, target_type='post', target_id=chem.id, created_at=1)
        deck, note = build_suggested_deck(self.me, limit=6)
        self.assertEqual(note, '')
        self.assertEqual([o for k, o in deck if k == 'post'][0].category, 'Chemistry')
        with CaptureQueriesContext(connection) as ctx:
            build_suggested_deck(self.me, limit=6)
        self.assertEqual(len(ctx.captured_queries), 0, 'interests and pools both come from cache')
