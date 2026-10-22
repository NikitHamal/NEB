"""The suggested feed's shared candidate pools are reused per process only while they are
the entry the shared cache holds, and never carry one viewer's state into another request."""
import uuid
from unittest import mock

from django.core.cache import cache
from django.test import TestCase

from api import views_feed
from api.models import Post, Resource, User
from api.utils import now_ms


class FeedPoolReuseTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        now = now_ms()
        cls.author = User.objects.create(id='pool-author', username='poolauthor', email='p@x.np', email_verified=True,
                                         created_at=now)
        Post.objects.bulk_create([Post(id=f'pool-p{i}', user=cls.author, title=f'T{i}', content='c', category='Physics',
                                       created_at=now - i) for i in range(5)])
        Resource.objects.bulk_create([Resource(id=f'pool-r{i}', title=f'R{i}', subject='Physics', type='PDF',
                                               approval_status='approved', added_at=now - i, uploaded_by=cls.author)
                                      for i in range(5)])

    def setUp(self):
        cache.clear()
        views_feed._local_pools.clear()

    def test_reuses_the_current_entry_without_fetching_it_again(self):
        first = views_feed._candidate_pools()
        with mock.patch.object(cache, 'get', wraps=cache.get) as get:
            again = views_feed._candidate_pools()
        self.assertIs(again, first)
        self.assertEqual([c.args[0] for c in get.call_args_list], [views_feed._POOLS_STAMP_KEY])

    def test_a_new_shared_entry_replaces_the_local_one(self):
        views_feed._candidate_pools()
        cache.clear()  # e.g. expired, or another process rebuilt it
        Post.objects.create(id='pool-new', user=self.author, title='Newest', content='c', category='Physics',
                            created_at=now_ms() + 1000)
        posts, _resources = views_feed._candidate_pools()
        self.assertEqual(posts[0][0].id, 'pool-new')

    def test_an_expired_local_entry_is_not_served(self):
        views_feed._candidate_pools()
        stamp, _expires, pools = views_feed._local_pools['entry']
        views_feed._local_pools['entry'] = (stamp, 0, pools)
        cache.delete(views_feed._POOLS_KEY)
        self.assertIsNot(views_feed._candidate_pools(), pools)

    def test_decks_get_their_own_copies(self):
        deck, _note = views_feed.build_suggested_deck(None, limit=6)
        kind, obj = next((k, o) for k, o in deck if k == 'resource')
        obj._viewer_liked = True
        again, _note = views_feed.build_suggested_deck(None, limit=6)
        same = next(o for k, o in again if k == 'resource' and o.id == obj.id)
        self.assertIsNot(same, obj)
        self.assertFalse(hasattr(same, '_viewer_liked'))
        self.assertEqual(same.uploaded_by.username, 'poolauthor')  # relations come along, no query
