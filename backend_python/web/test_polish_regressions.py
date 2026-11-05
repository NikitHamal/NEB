"""Guards for the auth/composer polish pass: spam-folder hint, onboarding helper, one-stroke focus,
poll-scope inset and the @ popup that must not close its dialog."""
import os

from django.test import TestCase

WEB = os.path.join(os.path.dirname(__file__), 'static', 'web')


def _read(*parts):
    with open(os.path.join(WEB, *parts), encoding='utf-8') as f:
        return f.read()


class AuthHintTests(TestCase):
    def test_verify_and_reset_panels_mention_spam_folder(self):
        html = self.client.get('/login/').content.decode()
        self.assertGreaterEqual(html.lower().count('spam or junk folder'), 2)

    def test_legacy_email_pages_redirect_to_login(self):
        for url in ('/auth/email/login/', '/auth/email/verify/'):
            r = self.client.get(url)
            self.assertEqual(r.status_code, 302, url)
            self.assertIn('/login/', r['Location'])


class OnboardingHelperTests(TestCase):
    def test_h_flattens_array_children(self):
        js = _read('js', 'neb-edu.js')
        self.assertIn('Array.isArray(c)', js)
        self.assertIn('c.nodeType', js)


class FocusAndInsetTests(TestCase):
    def test_one_stroke_focus_rules_ship(self):
        src = _read('css', 'm3x-app.src.css')
        self.assertIn('app-focus.css', src)
        css = _read('css', 'm3x', 'app-focus.css')
        self.assertIn('outline: 0', css)
        self.assertNotRegex(css, r'box-shadow\s*:\s*(?!none)')
        home = _read('css', 'pages', 'web-home.css')
        i = home.index('.hf-composer-input-btn:focus-visible')
        self.assertNotIn('box-shadow', home[i:i + 160])

    def test_poll_scope_gets_the_panel_inset(self):
        css = _read('css', 'pages', 'forum-post.css')
        self.assertIn('.fp-center-panel > .pb-scope', css)


class MentionPopupTests(TestCase):
    def test_pick_does_not_close_dialog(self):
        home = open(os.path.join(os.path.dirname(__file__), 'templates', 'web', 'home.html'), encoding='utf-8').read()
        self.assertIn('pressedOnBackdrop', home)
        self.assertIn('swallow', _read('js', 'composer-editor.js'))
