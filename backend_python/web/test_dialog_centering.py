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


class CoverPreviewTests(SimpleTestCase):
    """The picker shows small lazy WebP previews (a few KB each), never 175 vector files or a megabyte sprite."""

    def test_every_cover_has_a_light_and_dark_preview(self):
        import json
        base = os.path.join(CSS, '..', 'img', 'm3x')
        ids = [r[0] for r in json.load(open(os.path.join(base, 'covers.json')))['covers']]
        for theme in ('light', 'dark'):
            missing = [i for i in ids if not os.path.isfile(os.path.join(base, 'cover', 'prev', theme, i + '.webp'))]
            self.assertEqual(missing, [], theme)

    def test_previews_stay_small(self):
        base = os.path.join(CSS, '..', 'img', 'm3x', 'cover', 'prev', 'light')
        big = [f for f in os.listdir(base) if os.path.getsize(os.path.join(base, f)) > 40000]
        self.assertEqual(big, [])

    def test_picker_tiles_are_lazy_and_sprite_is_gone(self):
        tpl = open(os.path.join(settings.BASE_DIR, 'web', 'templates', 'web', 'profile.html'), encoding='utf-8').read()
        self.assertIn('loading="lazy"', tpl)
        self.assertNotIn('sprite', tpl)
