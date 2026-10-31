"""A token handed to a client must actually authenticate.

Regression this file exists for (Oct 2026): the new-user branches of
`web/views_auth.py` minted tokens by hand —

    auth_token = User.generate_token()
    db_user.auth_token = hash_auth_token(auth_token)
    db_user.save()

— which writes the hash into `users.auth_token` but never creates the
`UserAuthToken` session row. When the resolver started requiring a live session
row (`_token_usable` rejects a zero expiry), every one of those tokens
authenticated *nothing*. A brand-new Google/GitHub signup reached onboarding
holding a dead token, and the final `POST /api/users/profile/` answered
`401 {"detail": "Authentication credentials were not provided."}` — so the
account stayed half-created forever and the person retried with a new email.

Every test here signs a user up through one of the real entry points and then
asserts the token that entry point produced resolves via
`get_user_by_auth_token`.
"""
import json
import urllib.parse
from unittest import mock

from django.test import TestCase

from api.models import User, UserAuthToken
from api.security import get_user_by_auth_token


def _google_info(user_id, email, name='New Person'):
    return {
        'userId': user_id,
        'email': email,
        'email_verified': True,
        'displayName': name,
        'photoUrl': '',
    }


class _Response:
    """The slice of requests.Response these views use."""

    def __init__(self, payload):
        self._payload = payload

    def json(self):
        return self._payload


def _deep_link_token(response):
    """Pull authToken out of a nebians://auth-callback deep link."""
    assert response.status_code == 302, response.content
    location = response['Location']
    assert 'authToken=' in location, location
    query = urllib.parse.parse_qs(urllib.parse.urlparse(location).query)
    return query['authToken'][0], location


class SignInTokenTests(TestCase):
    def assert_token_authenticates(self, raw_token, expected_user_id):
        user = get_user_by_auth_token(raw_token)
        self.assertEqual(user.pk, expected_user_id)
        self.assertTrue(
            UserAuthToken.objects.filter(user_id=expected_user_id, revoked_at=0).exists(),
            'a session row must exist for every token handed to a client',
        )

    def _session_token(self):
        return self.client.session['auth_token']

    def test_web_google_signup_token_authenticates(self):
        from web import views_auth

        info = _google_info('google_new_1', 'google_new_1@example.com')
        with mock.patch.object(views_auth, 'verify_google_token', return_value=info):
            response = self.client.post(
                '/auth/google/',
                data=json.dumps({'idToken': 'fake-id-token'}),
                content_type='application/json',
            )

        self.assertEqual(response.status_code, 200, response.content)
        self.assertTrue(response.json()['isNewUser'])
        self.assert_token_authenticates(self._session_token(), 'google_new_1')

    def test_mobile_google_callback_token_authenticates(self):
        from web import views_auth

        info = _google_info('google_new_2', 'google_new_2@example.com')
        with mock.patch.object(views_auth, 'verify_google_token', return_value=info), \
                mock.patch('requests.post', return_value=_Response({'id_token': 'fake-id-token'})):
            response = self.client.get(
                '/auth/google/callback/',
                {'code': 'auth-code', 'state': 'mobile_google'},
            )

        token, location = _deep_link_token(response)
        self.assertIn('isNewUser=true', location)
        self.assert_token_authenticates(token, 'google_new_2')

    def test_mobile_github_callback_token_authenticates(self):
        github_user = {
            'id': 987654,
            'email': 'github_new@example.com',
            'name': 'GitHub New',
            'login': 'github_new',
            'avatar_url': '',
        }

        def fake_get(url, **_kwargs):
            if url.endswith('/user/emails'):
                return _Response([{'email': github_user['email'], 'primary': True, 'verified': True}])
            return _Response(github_user)

        with mock.patch('requests.post', return_value=_Response({'access_token': 'gh-access'})), \
                mock.patch('requests.get', side_effect=fake_get):
            response = self.client.get(
                '/auth/github/callback/',
                {'code': 'auth-code', 'state': 'mobile_github'},
            )

        token, location = _deep_link_token(response)
        self.assertIn('isNewUser=true', location)
        self.assert_token_authenticates(token, 'github_987654')

    def test_returning_google_user_gets_a_fresh_working_token(self):
        User.objects.create(
            id='google_returning',
            username='user_return1',
            email='google_returning@example.com',
            email_verified=True,
            created_at=1,
        )
        from web import views_auth

        info = _google_info('google_returning', 'google_returning@example.com')
        with mock.patch.object(views_auth, 'verify_google_token', return_value=info):
            response = self.client.post(
                '/auth/google/',
                data=json.dumps({'idToken': 'fake-id-token'}),
                content_type='application/json',
            )

        self.assertFalse(response.json()['isNewUser'])
        self.assert_token_authenticates(self._session_token(), 'google_returning')

    def test_signed_up_user_can_save_a_profile(self):
        """The exact journey that failed: sign up, then POST the profile."""
        from web import views_auth

        info = _google_info('google_profile_1', 'google_profile_1@example.com')
        with mock.patch.object(views_auth, 'verify_google_token', return_value=info):
            self.client.post(
                '/auth/google/',
                data=json.dumps({'idToken': 'fake-id-token'}),
                content_type='application/json',
            )

        token = self._session_token()
        response = self.client.post(
            '/api/users/profile/',
            data=json.dumps({
                'username': 'new_person',
                'dob': '2009-05-04',
                'gender': 'Female',
                'role': 'student',
                'classLevel': 'Class 11',
                'pradesh': 'Sudurpashchim',
                'district': 'Baitadi',
                'school': 'Siddheshwar',
            }),
            content_type='application/json',
            HTTP_AUTHORIZATION=f'Bearer {token}',
        )

        self.assertEqual(response.status_code, 200, response.content)
        user = User.objects.get(pk='google_profile_1')
        self.assertEqual(user.username, 'new_person')
        self.assertEqual(user.district, 'Baitadi')
        self.assertEqual(user.display_name, 'New Person')
