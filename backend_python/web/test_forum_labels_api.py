import uuid

from django.core.cache import cache
from django.test import TestCase
from rest_framework.test import APIClient

from api.models import Post, Reply, User
from api.security import issue_auth_token


def _user(username, **kw):
    return User.objects.create(
        id=str(uuid.uuid4()), username=username, email=f'{username}@example.com',
        email_verified=True, display_name=username.title(), role='student', **kw,
    )


class ForumLabelApiTests(TestCase):
    def setUp(self):
        cache.clear()
        self.asker = _user('asker')
        self.helper = _user('helper')
        self.post = Post.objects.create(
            id=str(uuid.uuid4()), user=self.asker, title='Why is Zeff higher?', content='Explain.',
            category='Science', created_at=1_700_000_000_000,
        )

    def _client(self, user):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + issue_auth_token(user))
        return client

    def test_reply_kind_is_stored_and_serialized(self):
        res = self._client(self.helper).post(
            f'/api/posts/{self.post.id}/replies/', {'content': 'Think of charge.', 'kind': 'hint'}, format='json')
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.json()['kind'], 'hint')
        self.assertEqual(Reply.objects.get(pk=res.json()['id']).kind, 'hint')

    def test_unknown_kind_falls_back_to_comment(self):
        res = self._client(self.helper).post(
            f'/api/posts/{self.post.id}/replies/', {'content': 'Hi', 'kind': 'nonsense'}, format='json')
        self.assertEqual(res.json()['kind'], 'comment')

    def test_author_labels_through_the_api(self):
        reply = Reply.objects.create(
            id=str(uuid.uuid4()), post=self.post, user=self.helper, content='x', kind='answer',
            created_at=1_700_000_000_001)
        res = self._client(self.asker).post(f'/api/replies/{reply.id}/label/', {'label': 'accepted'}, format='json')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['label'], 'accepted')
        self.post.refresh_from_db()
        self.assertTrue(self.post.is_resolved)
        self.assertEqual(self.post.accepted_reply_id, reply.id)

    def test_replier_cannot_label_and_unknown_is_rejected(self):
        reply = Reply.objects.create(
            id=str(uuid.uuid4()), post=self.post, user=self.helper, content='x', kind='answer',
            created_at=1_700_000_000_001)
        self.assertEqual(self._client(self.helper).post(
            f'/api/replies/{reply.id}/label/', {'label': 'correct'}, format='json').status_code, 403)
        self.assertEqual(self._client(self.asker).post(
            f'/api/replies/{reply.id}/label/', {'label': 'nope'}, format='json').status_code, 400)

    def test_list_reports_can_label_to_the_author_only(self):
        Reply.objects.create(
            id=str(uuid.uuid4()), post=self.post, user=self.helper, content='x', kind='answer',
            created_at=1_700_000_000_001)
        mine = self._client(self.asker).get(f'/api/posts/{self.post.id}/replies/').json()
        theirs = self._client(self.helper).get(f'/api/posts/{self.post.id}/replies/').json()
        rows = lambda body: body if isinstance(body, list) else next(v for v in body.values() if isinstance(v, list))
        self.assertTrue(rows(mine)[0]['canLabel'])
        self.assertFalse(rows(theirs)[0]['canLabel'])
