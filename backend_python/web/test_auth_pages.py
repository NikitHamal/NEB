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
