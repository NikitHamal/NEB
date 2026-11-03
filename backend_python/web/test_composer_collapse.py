"""The home composer compacts in flow, so its own height change is the one
thing that must not be allowed to move the scroll position."""
from pathlib import Path

from django.test import TestCase

WEB = Path(__file__).resolve().parent
HOME_CSS = WEB / 'static' / 'web' / 'css' / 'pages' / 'web-home.css'
HOME_JS = WEB / 'templates' / 'web' / 'home.html'


class ComposerCollapseTests(TestCase):
    def test_the_page_declares_anchoring_off_where_the_composer_lives(self):
        css = HOME_CSS.read_text(encoding='utf-8')
        self.assertIn('html:has(.hf-composer-sticky)', css)
        self.assertIn('overflow-anchor: none', css)

    def test_the_handler_needs_two_thresholds_not_one_hairline(self):
        js = HOME_JS.read_text(encoding='utf-8')
        self.assertIn('top <= stickyTop + 1', js)
        self.assertIn('top >= stickyTop + 12', js)

    def test_the_composer_ships_with_its_own_version_stamp(self):
        html = self.client.get('/app/').content.decode()
        self.assertIn('web-home.css', html)
        self.assertIn('hf-composer-sticky', html)
