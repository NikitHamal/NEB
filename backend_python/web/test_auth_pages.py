"""Sign-in page on the m3x system: four panels, no role question, flat design."""
import os
import re

from django.test import TestCase

CSS = os.path.join(os.path.dirname(__file__), 'static', 'web', 'css', 'm3x')


class LoginPageTests(TestCase):
    def test_login_page_has_all_four_panels_and_no_role_step(self):
        r = self.client.get('/login/')
        self.assertEqual(r.status_code, 200)
        html = r.content.decode()
        for pid in ('panel-login', 'panel-signup', 'panel-verify', 'panel-forgot'):
            self.assertIn(f'id="{pid}"', html)
        # role is asked once, in the welcome flow, so the sign-up form never defaults it
        self.assertNotIn('signup-role', html)
        self.assertNotIn('select-role', html)
        self.assertIn('web/js/auth', html)

    def test_legacy_signup_url_opens_the_signup_panel(self):
        r = self.client.get('/auth/email/signup/')
        self.assertEqual(r.status_code, 302)
        self.assertIn('panel=email-signup', r['Location'])


class FlatDesignTests(TestCase):
    def _css(self, name):
        with open(os.path.join(CSS, name), encoding='utf-8') as f:
            return f.read()

    def test_new_screens_are_flat(self):
        for name in ('app-auth.css', 'app-onboard.css'):
            css = self._css(name)
            self.assertNotRegex(css, r'box-shadow\s*:\s*(?!none)', name)
            self.assertNotIn('gradient(', css, name)
            self.assertNotRegex(css, r'border-radius:\s*0[;\s]', name)

    def test_templates_have_no_emoji_or_live_badges(self):
        base = os.path.join(os.path.dirname(__file__), 'templates', 'web')
        emoji = re.compile('[\U0001F300-\U0001FAFF\u2600-\u27BF]')
        for name in ('login.html', 'onboarding.html', '_auth_social.html'):
            with open(os.path.join(base, name), encoding='utf-8') as f:
                text = f.read()
            self.assertIsNone(emoji.search(text), name)
            self.assertNotIn('LIVE', text, name)


class NativeGoogleOAuthTests(TestCase):
    def test_api_google_oauth_links_existing_verified_email_account(self):
        import json
        from unittest.mock import patch
        from api.models import User

        existing = User.objects.create(
            id='email_user_1',
            username='student_np',
            email='student@example.com',
            email_verified=True,
            created_at=1000,
        )
        fake_info = {
            'userId': 'google_sub_999',
            'email': 'student@example.com',
            'email_verified': True,
            'displayName': 'Aarav Sharma',
            'photoUrl': 'https://example.com/p.jpg',
        }
        with patch('api.views_auth.verify_google_token', return_value=fake_info):
            r = self.client.post(
                '/api/auth/google/',
                data=json.dumps({'idToken': 'fake-id-token'}),
                content_type='application/json',
            )
        self.assertEqual(r.status_code, 200)
        body = r.json()
        self.assertEqual(body['status'], 'success')
        self.assertFalse(body['isNewUser'])
        self.assertTrue(body.get('authToken'))
        self.assertEqual(body['user']['id'], existing.id)
        self.assertEqual(body['user']['username'], 'student_np')

    def test_mobile_oauth_deep_link_includes_profile_fields(self):
        from types import SimpleNamespace
        from web.views_auth import _mobile_auth_deep_link

        u = SimpleNamespace(
            id='u_123',
            username='aarati_np',
            email='aarati@example.com',
            display_name='Aarati Sharma',
            photo_url='https://example.com/a.jpg',
        )
        resp = _mobile_auth_deep_link('tok_abc', False, u)
        self.assertEqual(resp.status_code, 302)
        loc = resp['Location']
        self.assertTrue(loc.startswith('nebians://auth-callback?'))
        self.assertIn('authToken=tok_abc', loc)
        self.assertIn('userId=u_123', loc)
        self.assertIn('username=aarati_np', loc)
        self.assertIn('displayName=Aarati+Sharma', loc)

    def test_api_google_oauth_deduplicates_temp_username_on_prefix_collision(self):
        import json
        from unittest.mock import patch
        from api.models import User

        User.objects.create(
            id='10987654_first',
            username='user_10987654',
            email='first@example.com',
            email_verified=True,
            created_at=1000,
        )
        fake_info = {
            'userId': '10987654_second',
            'email': 'second@example.com',
            'email_verified': True,
            'displayName': 'Second Student',
            'photoUrl': '',
        }
        with patch('api.views_auth.verify_google_token', return_value=fake_info):
            r = self.client.post(
                '/api/auth/google/',
                data=json.dumps({'idToken': 'fake-id-token-2'}),
                content_type='application/json',
            )
        self.assertEqual(r.status_code, 200)
        body = r.json()
        self.assertTrue(body['isNewUser'])
        self.assertEqual(body['user']['username'], 'user_10987654_1')

    def test_mobile_github_callback_links_existing_verified_public_email(self):
        from types import SimpleNamespace
        from unittest.mock import patch
        from api.models import User

        existing = User.objects.create(
            id='email_gh_1',
            username='gh_student_np',
            email='ghstudent@example.com',
            email_verified=True,
            created_at=1000,
        )

        def fake_get(url, *args, **kwargs):
            if url.endswith('/user/emails'):
                return SimpleNamespace(json=lambda: [{'email': 'ghstudent@example.com', 'primary': True, 'verified': True}])
            return SimpleNamespace(json=lambda: {'id': 778899, 'login': 'ghstudent', 'name': 'GH Student', 'email': 'ghstudent@example.com', 'avatar_url': ''})

        with self.settings(GITHUB_CLIENT_ID='cid', GITHUB_CLIENT_SECRET='csec'), \
             patch('requests.post', return_value=SimpleNamespace(json=lambda: {'access_token': 'gh_tok_1'})), \
             patch('requests.get', side_effect=fake_get):
            r = self.client.get('/auth/github/callback/?code=abc&state=mobile_github')
        self.assertEqual(r.status_code, 302)
        self.assertTrue(r['Location'].startswith('nebians://auth-callback?'))
        self.assertIn(f'userId={existing.id}', r['Location'])
        self.assertIn('username=gh_student_np', r['Location'])
