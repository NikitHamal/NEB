"""Three app features the API had broken: resource comments (GET answered 400 since July),
notifications paging (has_more was always false, so the app never asked for page 2) and the
@mention picker (api/users/search/ did not exist)."""
import uuid

from django.test import Client, TestCase

from api.models import Follow, Notification, Resource, ResourceComment, User, UserAuthToken
from api.security import AUTH_TOKEN_TTL_MS, hash_auth_token
from api.utils import now_ms


class ApiFixesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        now = now_ms()
        cls.viewer = User.objects.create(id='fx-viewer', username='viewer', email='v@x.np', display_name='Viewer',
                                         email_verified=True, created_at=now)
        cls.ram = User.objects.create(id='fx-ram', username='ramesh', email='r@x.np', display_name='Ramesh',
                                      email_verified=True, created_at=now, class_level='12')
        cls.aram = User.objects.create(id='fx-aram', username='aramesh', email='a@x.np', display_name='',
                                       email_verified=True, created_at=now)
        User.objects.create(id='fx-locked', username='rameshlocked', email='l@x.np', email_verified=True,
                            created_at=now, is_locked=True)
        User.objects.create(id='fx-unverified', username='rameshnew', email='n@x.np', email_verified=False, created_at=now)
        Follow.objects.create(follower=cls.viewer, following=cls.ram, created_at=now)
        Follow.objects.create(follower=cls.aram, following=cls.ram, created_at=now)
        cls.raw = f'tok-{uuid.uuid4().hex}'
        UserAuthToken.objects.create(id=str(uuid.uuid4()), user=cls.viewer, token_hash=hash_auth_token(cls.raw),
                                     created_at=now, last_used_at=now, revoked_at=0, expires_at=now + AUTH_TOKEN_TTL_MS)
        cls.resource = Resource.objects.create(id='fx-res', title='Notes', subject='Physics', grade_level='Class 12',
                                               type='PDF', approval_status='approved', is_lead=True, added_at=now,
                                               uploaded_by=cls.ram, source_type='user')
        ResourceComment.objects.create(id='fx-c1', resource=cls.resource, user=cls.ram, content='Great notes',
                                       created_at=now)
        Notification.objects.bulk_create([
            Notification(id=f'fx-n{i}', recipient=cls.viewer, actor=cls.ram, verb='like_post', target_type='post',
                         target_id='p', created_at=now - i) for i in range(45)])

    def auth(self):
        return {'HTTP_AUTHORIZATION': f'Bearer {self.raw}'}

    def test_resource_comments_are_listed(self):
        r = Client().get(f'/api/resources/{self.resource.id}/comments/')
        self.assertEqual(r.status_code, 200, r.content)
        self.assertEqual([c['content'] for c in r.json()['comments']], ['Great notes'])

    def test_notifications_say_when_there_is_another_page(self):
        c = Client()
        first = c.get('/api/notifications/?page=1&page_size=20', **self.auth()).json()
        self.assertEqual((len(first['notifications']), first['has_more']), (20, True))
        last = c.get('/api/notifications/?page=3&page_size=20', **self.auth()).json()
        self.assertEqual((len(last['notifications']), last['has_more']), (5, False))
        exact = c.get('/api/notifications/?page=1&page_size=45', **self.auth()).json()
        self.assertEqual((len(exact['notifications']), exact['has_more']), (45, False))

    def test_user_search_for_mentions(self):
        r = Client().get('/api/users/search/?q=@rame', **self.auth())
        self.assertEqual(r.status_code, 200)
        rows = r.json()
        # verified, unlocked accounts only; a username starting with the term comes first
        self.assertEqual([u['username'] for u in rows], ['ramesh', 'aramesh'])
        ram = rows[0]
        self.assertEqual((ram['display_name'], ram['class_level'], ram['follower_count'], ram['is_following'], ram['is_self']),
                         ('Ramesh', '12', 2, True, False))
        self.assertEqual(rows[1]['display_name'], 'aramesh')
        self.assertTrue(rows[1]['photo_url'])
        self.assertEqual(Client().get('/api/users/search/?q=r').json(), [])
