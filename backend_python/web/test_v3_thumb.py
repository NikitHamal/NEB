"""Resource thumbnails are the art v3 `thumb` pieces, drawn by code on the site (js/v3-thumb.js) and in the app (v3art/)."""
import os
import re

from django.test import SimpleTestCase

BASE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(BASE))


def read(*parts):
    with open(os.path.join(*parts), encoding='utf-8') as f:
        return f.read()


class V3ThumbTests(SimpleTestCase):
    def test_engine_is_loaded_before_the_painter(self):
        base = read(BASE, 'templates', 'base.html')
        self.assertLess(base.index('web/js/v3-thumb.js'), base.index('web/js/pixel-art.js'))

    def test_painter_uses_v3_for_banners_only(self):
        paint = read(BASE, 'static', 'web', 'js', 'pixel-art.js')
        self.assertIn('NebArtV3', paint)
        self.assertIn('V.thumb(', paint)
        self.assertNotIn('M.thumb(', paint)
        self.assertIn('M.cover(', paint)

    def test_no_scenes_buildings_or_peaks(self):
        js = read(BASE, 'static', 'web', 'js', 'v3-thumb.js')
        self.assertIn("pagoda: 1, stupa: 1, summit: 1", js)
        self.assertNotIn("'ground'", js.split('A.thumbPick')[0].split('var STYLES')[1].split(';')[0])
        self.assertIsNone(re.search(r'<image|<text|Gradient|filter=', js))

    def test_light_and_dark_are_both_drawn_and_themed(self):
        css = read(BASE, 'static', 'web', 'css', 'm3x-app.css')
        self.assertIn('[data-theme="dark"] .m3a.v3t-dark', css)
        self.assertIn('.m3a.v3t-dark { display: none; }', css)

    def test_app_port_exists(self):
        kt = os.path.join(REPO, 'app', 'src', 'main', 'java', 'com', 'neb', 'ians', 'ui', 'components', 'v3art')
        for name in ('V3Core.kt', 'V3Still.kt', 'V3Svg.kt', 'V3Thumb.kt', 'V3Subjects.kt'):
            self.assertTrue(os.path.exists(os.path.join(kt, name)), name)
