"""Tests for the desktop browser hand-off sign-in (api/desktop_auth.py)."""
import base64
import hashlib
import secrets

from django.core.cache import cache
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from . import desktop_auth
from .models import User


def _pkce():
    verifier = secrets.token_urlsafe(48)
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b'=').decode()
    return verifier, challenge


@override_settings(REST_FRAMEWORK={
    'DEFAULT_THROTTLE_CLASSES': [],
    'DEFAULT_THROTTLE_RATES': {},
})
class DesktopAuthFlowTests(TestCase):
    def setUp(self):
        cache.clear()
        self.client = APIClient()
        self.user = User.objects.create(pk='u-desktop', username='aarav', email='a@example.com', created_at=1)

    def _start(self, challenge):
        return self.client.post('/api/auth/desktop/start/', {'challenge': challenge, 'device': 'Windows 11'}, format='json')

    def test_full_flow_issues_a_token_exactly_once(self):
        verifier, challenge = _pkce()
        r = self._start(challenge)
        self.assertEqual(r.status_code, 200)
        state = r.data['state']
        self.assertIn(f'/desktop-auth/?state={state}', r.data['loginUrl'])

        poll = lambda v=verifier: self.client.post('/api/auth/desktop/poll/', {'state': state, 'verifier': v}, format='json')
        self.assertEqual(poll().status_code, 202)                       # nobody approved yet

        self.assertTrue(desktop_auth.approve(state, self.user.pk))
        self.assertFalse(desktop_auth.approve(state, 'someone-else'))   # cannot be re-approved / hijacked

        ok = poll()
        self.assertEqual(ok.status_code, 200)
        self.assertEqual(ok.data['status'], 'success')
        self.assertTrue(ok.data['authToken'])
        self.assertEqual(ok.data['user']['username'], 'aarav')

        self.assertEqual(poll().status_code, 410)                       # one use only

    def test_wrong_verifier_cannot_collect_and_does_not_consume(self):
        verifier, challenge = _pkce()
        state = self._start(challenge).data['state']
        desktop_auth.approve(state, self.user.pk)
        attacker, _ = _pkce()
        bad = self.client.post('/api/auth/desktop/poll/', {'state': state, 'verifier': attacker}, format='json')
        self.assertEqual(bad.status_code, 410)
        good = self.client.post('/api/auth/desktop/poll/', {'state': state, 'verifier': verifier}, format='json')
        self.assertEqual(good.status_code, 200)

    def test_malformed_input_is_rejected(self):
        self.assertEqual(self._start('short').status_code, 400)
        self.assertEqual(self.client.post('/api/auth/desktop/poll/', {'state': 'x', 'verifier': 'y'}, format='json').status_code, 400)

    def test_denied_request_is_gone(self):
        verifier, challenge = _pkce()
        state = self._start(challenge).data['state']
        desktop_auth.deny(state)
        r = self.client.post('/api/auth/desktop/poll/', {'state': state, 'verifier': verifier}, format='json')
        self.assertEqual(r.status_code, 410)

    def test_banned_user_gets_no_token(self):
        verifier, challenge = _pkce()
        state = self._start(challenge).data['state']
        desktop_auth.approve(state, self.user.pk)
        User.objects.filter(pk=self.user.pk).update(is_banned=True)
        r = self.client.post('/api/auth/desktop/poll/', {'state': state, 'verifier': verifier}, format='json')
        self.assertEqual(r.status_code, 403)

    def test_device_name_is_sanitised(self):
        self.assertEqual(desktop_auth.clean_device_name('<script>alert(1)</script>'), 'scriptalert(1)script')
        self.assertEqual(desktop_auth.clean_device_name(''), 'NEBians Desktop')


class DesktopAuthPageTests(TestCase):
    def setUp(self):
        cache.clear()

    def test_unknown_state_renders_expired_page(self):
        r = self.client.get('/desktop-auth/?state=nope')
        self.assertEqual(r.status_code, 410)
        self.assertEqual(r['X-Frame-Options'], 'DENY')

    def test_signed_out_visitor_is_sent_to_login_with_next(self):
        _, challenge = _pkce()
        state = desktop_auth.create_request(challenge, 'Linux')
        r = self.client.get(f'/desktop-auth/?state={state}')
        self.assertEqual(r.status_code, 302)
        self.assertIn('/login/?next=', r['Location'])

    def _signed_in(self, client):
        from .security import issue_auth_token
        user = User.objects.create(pk='u-web', username='sita', email='s@example.com', created_at=1)
        session = client.session
        session['auth_token'] = issue_auth_token(user)
        session.save()
        return user

    def test_signed_in_user_sees_consent_and_allow_approves(self):
        from django.test import Client
        verifier, challenge = _pkce()
        state = desktop_auth.create_request(challenge, 'Windows 11')
        c = Client(enforce_csrf_checks=True)
        user = self._signed_in(c)
        page = c.get(f'/desktop-auth/?state={state}')
        self.assertEqual(page.status_code, 200)
        self.assertContains(page, 'Windows 11')
        self.assertContains(page, '@sita')
        # CSRF is enforced: a forged cross-site POST without the token is refused.
        self.assertEqual(c.post('/desktop-auth/', {'state': state, 'decision': 'allow'}).status_code, 403)
        self.assertEqual(desktop_auth.peek(state)['status'], 'pending')
        token = page.cookies['csrftoken'].value
        done = c.post('/desktop-auth/', {'state': state, 'decision': 'allow', 'csrfmiddlewaretoken': token})
        self.assertEqual(done.status_code, 200)
        self.assertEqual(desktop_auth.peek(state)['user_pk'], user.pk)
        r = APIClient().post('/api/auth/desktop/poll/', {'state': state, 'verifier': verifier}, format='json')
        self.assertEqual(r.status_code, 200)

    def test_deny_discards_request(self):
        from django.test import Client
        _, challenge = _pkce()
        state = desktop_auth.create_request(challenge, 'Mac')
        c = Client()
        self._signed_in(c)
        c.post('/desktop-auth/', {'state': state, 'decision': 'deny'})
        self.assertIsNone(desktop_auth.peek(state))
