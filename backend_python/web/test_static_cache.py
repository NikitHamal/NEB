import os
import re

from django.conf import settings
from django.test import SimpleTestCase, override_settings

from nebians.static_headers import static_cache_headers
from nebians.storage import VersionedStaticFilesStorage

WEB = os.path.join(settings.BASE_DIR, 'web')


def _read(*parts):
    with open(os.path.join(WEB, *parts), encoding='utf-8') as fh:
        return fh.read()


class VersionedStaticTests(SimpleTestCase):
    @override_settings(DEBUG=False)
    def test_scripts_and_styles_carry_a_content_version_but_fonts_do_not(self):
        storage = VersionedStaticFilesStorage()
        js = storage.url('web/js/realtime.js')
        self.assertRegex(js, r'/static/web/js/realtime\.js\?v=[0-9a-f]{10}$')
        css = storage.url('web/css/m3x.css')
        self.assertRegex(css, r'\?v=[0-9a-f]{10}$')
        # A preload only matches the url() in fonts.css when both are identical.
        self.assertNotIn('?', storage.url('web/fonts/app/poppins-400-latin.woff2'))

    @override_settings(DEBUG=False)
    def test_asset_tag_does_not_double_version(self):
        from web.templatetags.asset_tags import asset
        self.assertEqual(asset('web/js/realtime.js').count('?v='), 1)

    def test_cache_headers(self):
        h = {}
        static_cache_headers(h, 'web/js/x.js', '/static/web/js/x.js')
        self.assertIn('immutable', h['Cache-Control'])
        h = {}
        static_cache_headers(h, 'a.woff2', '/static/web/fonts/app/a.woff2')
        self.assertIn('max-age=31536000', h['Cache-Control'])
        h = {}
        static_cache_headers(h, 'logo.png', '/static/web/img/logo.png')
        self.assertNotIn('immutable', h['Cache-Control'])
        self.assertIn('max-age=604800', h['Cache-Control'])


class FontLoadingTests(SimpleTestCase):
    def test_every_preloaded_font_is_the_exact_url_fonts_css_requests(self):
        base = _read('templates', 'base.html')
        css = _read('static', 'web', 'css', 'fonts.css')
        wanted = set(re.findall(r'url\(\.\./(fonts/app/[^)]+)\)', css))
        preloads = re.findall(r"rel=\"preload\" href=\"\{% static 'web/(fonts/app/[^']+)' %\}([^\"]*)\"", base)
        self.assertGreaterEqual(len(preloads), 5)
        for path, query in preloads:
            self.assertIn(path + query, wanted, 'preload %s%s is not requested by fonts.css' % (path, query))

    def test_all_weights_the_app_paints_are_preloaded(self):
        base = _read('templates', 'base.html')
        for weight in (400, 500, 600, 700):
            self.assertIn('poppins-%d-latin.woff2' % weight, base)

    def test_fallback_face_matches_poppins_metrics_and_is_in_the_stack(self):
        css = _read('static', 'web', 'css', 'fonts.css')
        self.assertIn("font-family: 'Poppins Fallback'", css)
        self.assertIn('size-adjust', css)
        tokens = _read('static', 'web', 'css', 'm3x', 'app-fonts.css')
        self.assertIn('"Poppins Fallback"', tokens)

    def test_no_third_party_hosts_block_the_first_paint(self):
        base = _read('templates', 'base.html')
        head = base.split('</head>')[0]
        self.assertNotIn('cdn.jsdelivr.net', head)
        self.assertNotIn('fonts.googleapis.com', head)
        for name in ('canvas.html', 'desktop_auth.html'):
            self.assertNotIn('family=Poppins', _read('templates', 'web', name))
        self.assertNotIn('family=Poppins', _read('templates', 'admin_panel', 'base.html'))

    def test_katex_is_self_hosted_with_every_font(self):
        for name in os.listdir(os.path.join(WEB, 'templates', 'web')):
            if name.endswith('.html'):
                self.assertNotIn('cdn.jsdelivr.net/npm/katex', _read('templates', 'web', name), name)
        css = _read('static', 'web', 'vendor', 'katex', 'katex.min.css')
        for font in set(re.findall(r'url\(fonts/([^)]+\.woff2)\)', css)):
            self.assertTrue(os.path.exists(os.path.join(WEB, 'static', 'web', 'vendor', 'katex', 'fonts', font)), font)
        for script in ('katex.min.js', 'mhchem.min.js', 'auto-render.min.js'):
            self.assertTrue(os.path.exists(os.path.join(WEB, 'static', 'web', 'vendor', 'katex', script)), script)
