import json
import uuid

from django.test import Client, TestCase

from api.models import User
from api.security import hash_auth_token
from web.api_client import get_session_user


def _full_user_data(user):
    return {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'photo_url': user.photo_url or '',
        'display_name': user.display_name,
        'role': user.role,
        'dob': user.dob,
        'gender': user.gender,
        'class_level': user.class_level,
        'school': user.school,
        'bio': user.bio,
        'email_verified': user.email_verified,
    }


class AvatarSessionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            id=str(uuid.uuid4()),
            username='session_tester',
            email='session_tester@example.com',
            email_verified=True,
            display_name='Session Tester',
            gender='Male',
            class_level='12',
            school='NAST',
            bio='hello',
            dob='2005-01-01',
            role='student',
        )
        self.raw_token = User.generate_token()
        self.user.auth_token = hash_auth_token(self.raw_token)
        self.user.save(update_fields=['auth_token'])

    def _login_session(self, client, user_data):
        s = client.session
        s['auth_token'] = self.raw_token
        s['user_data'] = user_data
        s.save()

    def test_customize_keeps_profile_fields_in_session(self):
        client = Client()
        self._login_session(client, _full_user_data(self.user))
        resp = client.post(
            '/ajax/avatar/customize/',
            data=json.dumps({'use_pp': True}),
            content_type='application/json',
        )
        self.assertEqual(resp.status_code, 200)
        session_user = client.session.get('user_data')
        self.assertEqual(session_user.get('gender'), 'Male')
        self.assertEqual(session_user.get('class_level'), '12')
        self.assertEqual(session_user.get('email'), 'session_tester@example.com')
        self.assertEqual(session_user.get('school'), 'NAST')
        self.assertEqual(session_user.get('bio'), 'hello')
        self.assertEqual(session_user.get('dob'), '2005-01-01')

    def test_clobbered_session_is_healed_on_read(self):
        client = Client()
        self._login_session(client, {
            'id': self.user.id,
            'username': self.user.username,
            'display_name': self.user.display_name,
            'role': self.user.role,
            'photo_url': self.user.photo_url or '',
            'email_verified': True,
            'avatar_bg': '',
            'avatar_hue': -1,
            'avatar_tone': -1.0,
            'avatar_anim': 'bob',
            'avatar_shape': '',
            'avatar_expression': '',
            'avatar_color': '',
            'avatar_bg_color': '',
            'avatar_eye_color': '',
            'avatar_use_pp': True,
        })
        home = client.get('/')
        self.assertEqual(home.status_code, 200)
        session_user = client.session.get('user_data')
        self.assertEqual(session_user.get('gender'), 'Male')
        self.assertEqual(session_user.get('class_level'), '12')
        self.assertEqual(session_user.get('email'), 'session_tester@example.com')

    def test_heal_helper_returns_rebuilt_dict(self):
        from django.test import RequestFactory
        factory = RequestFactory()
        request = factory.get('/')
        from django.contrib.sessions.backends.db import SessionStore
        request.session = SessionStore()
        request.session['auth_token'] = self.raw_token
        request.session['user_data'] = {
            'id': self.user.id,
            'username': self.user.username,
            'avatar_anim': 'bob',
        }
        healed = get_session_user(request)
        self.assertEqual(healed.get('gender'), 'Male')
        self.assertEqual(healed.get('class_level'), '12')
        self.assertEqual(request.session['user_data'].get('email'), 'session_tester@example.com')