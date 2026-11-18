"""Native <dialog> elements must stay centred.

The site reset (`* { margin: 0 }`) zeroes the browser's `margin: auto` on a dialog, so a modal pins to the
top-left corner. material3/01-tokens-typography.css restores it with `dialog { margin: auto }`. These tests
keep that rule in the source and in the shipped bundle, and stop any dialog rule from zeroing the margin
again. Cover picker rows also need a size that does not depend on their images loading.
"""
import os
import re

from django.conf import settings
from django.test import SimpleTestCase

CSS = os.path.join(settings.BASE_DIR, 'web', 'static', 'web', 'css')


def read(*parts):
    with open(os.path.join(CSS, *parts), encoding='utf-8') as fh:
        return fh.read()


class DialogCenteringTests(SimpleTestCase):
    def test_reset_keeps_dialog_margin_auto(self):
        for name in ('material3/01-tokens-typography.css', 'material3.css'):
            self.assertRegex(read(*name.split('/')), r'(?m)^dialog\s*\{\s*margin:\s*auto', name)

    def test_no_dialog_rule_zeroes_margin(self):
        bad = []
        for root, _d, files in os.walk(CSS):
            for name in files:
                if not name.endswith('.css') or '.src.' in name:
                    continue
                text = open(os.path.join(root, name), encoding='utf-8', errors='ignore').read()
                for sel, body in re.findall(r'([^{}]*dialog[^{}]*)\{([^{}]*)\}', text):
                    parts = [x.strip() for x in sel.split(',')]
                    if not any(re.search(r'(^|[\s>])(dialog|\.[\w-]*-dialog)(\[open\]|:modal)?$', x) for x in parts):
                        continue
                    if '.neb-dialog' in sel or '@media' in sel:
                        continue
                    if re.search(r'(^|;)\s*margin\s*:\s*0\s*(;|$)', body.strip()):
                        bad.append('%s: %s' % (name, sel.strip()[:60]))
        self.assertEqual(bad, [])

    def test_cover_tiles_have_their_own_height(self):
        css = read('m3x', 'app-profile-v3.css')
        self.assertIn('.cv-grid', css)
        self.assertRegex(css, r'\.cv-grid\s*\{[^}]*align-content:\s*start')
        self.assertRegex(css, r'\.cv-grid\s*\{[^}]*min-height:\s*0')


class CoverArtByCodeTests(SimpleTestCase):
    """Covers and thumbnails are drawn by code (js/m3x-art.js, M3xEngine in the app). No image files, no per-tile requests."""

    def test_no_cover_image_files_are_shipped(self):
        base = os.path.join(CSS, '..', 'img', 'm3x')
        self.assertEqual(sorted(os.listdir(base)), ['covers.json'])

    def test_every_cover_row_has_a_seed_and_the_engine_ships(self):
        import json
        base = os.path.join(CSS, '..')
        rows = json.load(open(os.path.join(base, 'img', 'm3x', 'covers.json')))['covers']
        self.assertTrue(rows and all(len(r) == 4 and isinstance(r[3], int) for r in rows))
        engine = open(os.path.join(base, 'js', 'm3x-art.js'), encoding='utf-8').read()
        self.assertIn('NebM3x', engine)
        self.assertLess(len(engine), 60000)

    def test_picker_tiles_are_drawn_lazily(self):
        tpl = open(os.path.join(settings.BASE_DIR, 'web', 'templates', 'web', 'profile.html'), encoding='utf-8').read()
        tpl += open(os.path.join(settings.BASE_DIR, 'web', 'templates', 'web', 'partials', '_cover_picker.html'), encoding='utf-8').read()
        self.assertIn('data-m3x-tile', tpl)
        self.assertNotIn('.webp', tpl)
        self.assertNotIn('Downloads', tpl)


class CoverFitAndPersistTests(SimpleTestCase):
    """The cover is drawn for the box it sits in, and the saved pick reaches the template (a refresh used to fall back to the default)."""

    def _read(self, *parts):
        return open(os.path.join(settings.BASE_DIR, *parts), encoding='utf-8').read()

    def test_profile_view_passes_cover_art_to_the_template(self):
        src = self._read('web', 'views_profile.py')
        self.assertIn("cover_art=profile_data['cover_art']", src)
        self.assertIn("**cov", src)

    def test_engine_takes_the_box_aspect(self):
        base = os.path.join('web', 'static', 'web', 'js')
        engine = self._read(base, 'm3x-art.js')
        self.assertIn('cover: function (id, live, aspect)', engine)
        self.assertIn('thumb: function (family, v, aspect)', engine)
        paint = self._read(base, 'pixel-art.js')
        self.assertIn('ResizeObserver', paint)
        self.assertIn('aspectOf', paint)

    def test_edit_profile_has_the_cover_hero_and_picker(self):
        tpl = self._read('web', 'templates', 'web', 'edit_profile.html')
        self.assertIn('epf-cover', tpl)
        self.assertIn('open-cover-picker', tpl)
        self.assertIn('_cover_picker.html', tpl)
