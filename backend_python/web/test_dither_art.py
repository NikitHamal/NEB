import json
import os

from django.conf import settings
from django.test import SimpleTestCase

CSS = os.path.join(settings.BASE_DIR, 'web', 'static', 'web', 'css')
ART = os.path.join(settings.BASE_DIR, 'web', 'static', 'web', 'art')


class DitherArtTests(SimpleTestCase):
    def test_manifest_lists_files_that_exist(self):
        with open(os.path.join(ART, 'dither.json'), encoding='utf-8') as fh:
            items = json.load(fh)['items']
        self.assertGreaterEqual(len(items), 100)
        for it in items:
            self.assertTrue(os.path.exists(os.path.join(ART, it['file'])), it['file'])

    def test_cover_uses_the_dither_mask(self):
        self.assertTrue(os.path.exists(os.path.join(ART, 'dither', 'cover-dunes-mask.png')))
        css = open(os.path.join(CSS, 'm3x-app.css'), encoding='utf-8').read()
        self.assertIn('cover-dunes-mask.png', css)

    def test_follow_button_is_small_with_a_mask_glyph(self):
        css = open(os.path.join(CSS, 'm3x', 'app-follow.css'), encoding='utf-8').read()
        self.assertIn('mask: var(--fg)', css)
        self.assertRegex(css, r'--fh: 26px')
        self.assertNotRegex(css, r'box-shadow:\s*(?!none)')
        self.assertNotRegex(css, r'border-radius:\s*0[;\s]')
