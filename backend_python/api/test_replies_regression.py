"""GET /api/posts/<id>/replies/ must answer 200 for a post that has replies.

Session 68: a missing `Reply` import in api/view_helpers.py turned every such request
into a 500 (NameError) for about 90 minutes. The query-budget suite covered it but was
not in the CI test list. This test is small, fast and always listed."""
import uuid

from django.core.cache import cache
from django.test import Client, TestCase

from api.models import Post, Reply, User, UserAuthToken
from api.security import AUTH_TOKEN_TTL_MS, hash_auth_token
from api.utils import now_ms


class RepliesEndpointRegression(TestCase):
    @classmethod
    def setUpTestData(cls):
        now = now_ms()
        cls.author = User.objects.create(id='rr-a', username='rra', email='rra@x.np', display_name='RR A',
                                         email_verified=True, created_at=now)
        cls.viewer = User.objects.create(id='rr-v', username='rrv', email='rrv@x.np', display_name='RR V',
                                         email_verified=True, created_at=now)
        cls.raw_token = f'tok-{uuid.uuid4().hex}'
        UserAuthToken.objects.create(id=str(uuid.uuid4()), user=cls.viewer, token_hash=hash_auth_token(cls.raw_token),
                                     created_at=now, last_used_at=now, revoked_at=0, expires_at=now + AUTH_TOKEN_TTL_MS)
        cls.post = Post.objects.create(id='rr-p', user=cls.author, title='Energy', content='Why?',
                                       category='Physics', created_at=now)
        cls.empty_post = Post.objects.create(id='rr-e', user=cls.author, title='Quiet', content='Hi',
                                             category='Physics', created_at=now)
        Reply.objects.bulk_create([Reply(id=f'rr-r{i}', post=cls.post, user=cls.author, content='yes',
                                         created_at=now + i) for i in range(3)])

    def setUp(self):
        cache.clear()
        self.client = Client()

    def test_replies_signed_in_and_anonymous(self):
        url = f'/api/posts/{self.post.id}/replies/'
        for headers in ({'HTTP_AUTHORIZATION': f'Bearer {self.raw_token}'}, {}):
            r = self.client.get(url, **headers)
            self.assertEqual(r.status_code, 200, r.content[:300])
            body = r.json()
            rows = body.get('replies') or body.get('results') or body
            self.assertEqual(len(rows), 3)

    def test_post_without_replies(self):
        r = self.client.get(f'/api/posts/{self.empty_post.id}/replies/')
        self.assertEqual(r.status_code, 200)
