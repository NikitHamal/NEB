from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse

from api.models import Post, User
from api.security import issue_auth_token
from api.utils import now_ms

MEMBER_ONLY_POSTS = [
    ('web:ajax_like_post', {'post_id': 'p1'}),
    ('web:ajax_like_reply', {'reply_id': 'r1'}),
    ('web:ajax_like_resource', {'resource_id': 'x'}),
    ('web:ajax_create_reply', {'post_id': 'p1'}),
    ('web:ajax_create_post', {}),
    ('web:ajax_report', {}),
    ('web:ajax_bookmark_toggle', {}),
    ('web:ajax_poll_vote', {'poll_id': 'x'}),
    ('web:ajax_upload_inline_image', {}),
]


def _member():
    return User.objects.create(
        id='m1', username='m1', role=User.ROLE_STUDENT, email='m1@example.com', email_verified=True,
        created_at=now_ms(), is_locked=False, is_banned=False,
    )


class SignedInMemberTests(TestCase):
    def setUp(self):
        cache.clear()
        self.client = Client()

    def test_signed_out_callers_get_401_json_and_get_requests_get_405(self):
        for name, kwargs in MEMBER_ONLY_POSTS:
            url = reverse(name, kwargs=kwargs)
            denied = self.client.post(url)
            self.assertEqual((name, denied.status_code), (name, 401))
            self.assertEqual(denied.json(), {'error': 'Please log in again.'})
            self.assertEqual((name, self.client.get(url).status_code), (name, 405))

    def test_a_session_whose_account_is_gone_is_signed_out(self):
        user = _member()
        session = self.client.session
        session['auth_token'] = issue_auth_token(user)
        session.save()
        User.objects.filter(pk=user.pk).delete()
        cache.clear()
        response = self.client.post(reverse('web:ajax_like_post', kwargs={'post_id': 'p1'}))
        self.assertEqual(response.status_code, 401)

    def test_signed_in_member_reaches_the_view_with_their_account(self):
        user = _member()
        author = User.objects.create(
            id='a1', username='a1', role=User.ROLE_STUDENT, email='a1@example.com', email_verified=True,
            created_at=now_ms(), is_locked=False, is_banned=False,
        )
        Post.objects.create(id='p1', user=author, title='t', content='c', category='General', created_at=now_ms())
        session = self.client.session
        session['auth_token'] = issue_auth_token(user)
        session.save()
        response = self.client.post(reverse('web:ajax_like_post', kwargs={'post_id': 'p1'}))
        self.assertEqual(response.status_code, 200, response.content)
        self.assertEqual(self.client.post(reverse('web:ajax_like_post', kwargs={'post_id': 'nope'})).status_code, 404)
