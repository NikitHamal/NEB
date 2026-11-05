"""`users.class` is VARCHAR(10) in production while both clients offer
`'Class 10 / SEE'` (14 characters).

Written when MySQL was non-strict, that value was silently truncated to
`'Class 10 /'` (see migration 0159). Under STRICT_TRANS_TABLES the same write
raises `1406, "Data too long for column 'class'"` and the whole profile save
dies with a 500, which is what happened to a user retrying onboarding for two
minutes on 2026-11-05.

SQLite does not enforce VARCHAR widths, so these tests pin the two things that
actually protect the column on every backend: the model width (which
`_overlong_field_error` reads) and the guard itself.
"""
import time
import uuid

from django.test import Client, TestCase

from api.models import User
from api.security import issue_auth_token
from api.serializers import UserSerializer

CLASS_10_SEE = 'Class 10 / SEE'


def _create_user(**kwargs):
    defaults = {
        'id': str(uuid.uuid4()),
        'username': f'testuser_{uuid.uuid4().hex[:8]}',
        'email': f'{uuid.uuid4().hex[:8]}@test.com',
        'created_at': int(time.time() * 1000),
        'email_verified': True,
        'display_name': 'Test Person',
        'gender': 'Other',
        'dob': '2005-06-15',
        'role': 'student',
        'class_level': 'Class 11',
    }
    defaults.update(kwargs)
    return User.objects.create(**defaults)


def _login(client, user):
    session = client.session
    session['auth_token'] = issue_auth_token(user)
    session['user_data'] = dict(UserSerializer(user).data)
    session.save()


class ProfileClassLevelApiTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = _create_user()
        self.auth_header = {'HTTP_AUTHORIZATION': f'Bearer {issue_auth_token(self.user)}'}

    def _post(self, **fields):
        payload = {'username': self.user.username, 'dob': '2005-06-15'}
        payload.update(fields)
        return self.client.post(
            '/api/users/profile/',
            payload,
            content_type='application/json',
            **self.auth_header,
        )

    def test_model_widens_class_level_to_fit_the_client_option(self):
        self.assertEqual(User._meta.get_field('class_level').max_length, 20)
        self.assertLessEqual(len(CLASS_10_SEE), User._meta.get_field('class_level').max_length)

    def test_class_10_see_is_saved_instead_of_500(self):
        response = self._post(classLevel=CLASS_10_SEE, role='student')

        self.assertEqual(response.status_code, 200, response.content)
        self.user.refresh_from_db()
        self.assertEqual(self.user.class_level, CLASS_10_SEE)

    def test_overlong_class_level_is_refused_with_a_message(self):
        response = self._post(classLevel='Class 10 / SEE and then some more')

        self.assertEqual(response.status_code, 400, response.content)
        self.assertEqual(response.json()['field'], 'class_level')
        self.assertIn('class level', response.json()['error'].lower())
        self.user.refresh_from_db()
        self.assertEqual(self.user.class_level, 'Class 11')

    def test_overlong_display_name_is_refused_not_truncated(self):
        response = self._post(displayName='D' * 151, classLevel=CLASS_10_SEE)

        self.assertEqual(response.status_code, 400, response.content)
        self.assertEqual(response.json()['field'], 'display_name')
        self.user.refresh_from_db()
        self.assertEqual(self.user.display_name, 'Test Person')


class ProfileClassLevelWebTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = _create_user(username=f'web{uuid.uuid4().hex[:6]}')
        _login(self.client, self.user)

    def _post(self, **fields):
        payload = {
            'username': self.user.username,
            'dob': '2005-06-15',
            'display_name': 'Test Person',
            'gender': 'Other',
            'role': 'student',
            'class_level': CLASS_10_SEE,
        }
        payload.update(fields)
        return self.client.post('/app/profile/edit/', payload)

    def test_edit_profile_saves_class_10_see(self):
        response = self._post()

        self.assertEqual(response.status_code, 302, response.content[:500])
        self.user.refresh_from_db()
        self.assertEqual(self.user.class_level, CLASS_10_SEE)

    def test_edit_profile_refuses_an_overlong_class_level(self):
        response = self._post(class_level='Class 10 / SEE and then some more')

        self.assertEqual(response.status_code, 200, response.content[:500])
        self.user.refresh_from_db()
        self.assertEqual(self.user.class_level, 'Class 11')
