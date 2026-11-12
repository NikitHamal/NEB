import datetime as dt
import re
from pathlib import Path

from django.core.cache import cache
from django.test import Client, TestCase

from api.models import SiteTheme
from web import site_themes


class LandingAndAppPrefixTests(TestCase):
    def setUp(self):
        cache.clear()
        self.client = Client()

    def test_landing_is_its_own_light_page(self):
        r = self.client.get('/')
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Past papers.')
        self.assertContains(r, 'Pick your level.')
        self.assertNotContains(r, 'For students in Nepal')
        self.assertNotContains(r, 'material3.css')
        self.assertContains(r, 'href="/app/library/"')


class LandingDesignRulesTests(TestCase):
    """The founder's hard rules for the landing page, kept as tests so a later edit cannot undo them."""

    def setUp(self):
        cache.clear()
        base = Path(__file__).resolve().parent / 'static' / 'web'
        self.css = (base / 'css' / 'landing.css').read_text(encoding='utf-8') + (base / 'css' / 'm3x.css').read_text(encoding='utf-8')
        self.js = (base / 'js' / 'landing.js').read_text(encoding='utf-8') + (base / 'js' / 'm3x.js').read_text(encoding='utf-8')
        self.html = self.client.get('/').content.decode()

    def test_no_box_shadows_or_drop_shadows(self):
        for src in (self.css, self.html):
            self.assertNotRegex(src, r'box-shadow\s*:\s*(?!\s*none)')
            self.assertNotIn('drop-shadow', src)
            self.assertNotIn('text-shadow', src)

    def test_no_gradients(self):
        self.assertNotRegex(self.css + self.html, r'(linear|radial|conic)-gradient')
        self.assertNotIn('<linearGradient', self.html)

    def test_no_nepali_script_or_emoji(self):
        for src in (self.html, self.css, self.js):
            self.assertIsNone(re.search('[\u0900-\u097F]', src), 'Devanagari on the landing page')
            self.assertIsNone(re.search('[\U0001F000-\U0001FAFF\u2600-\u27BF]', src), 'emoji on the landing page')

    def test_no_live_badge_and_no_stale_page_count(self):
        self.assertNotRegex(self.html, r'(?i)>\s*live\s*<')
        self.assertNotIn('6,000', self.html)
        self.assertNotRegex(self.html, r'(?i)\b(six thousand|\d[\d,]*k?\+? pages)\b')

    def test_every_level_renders_a_tab_and_a_panel(self):
        from .views_landing import LEVELS
        self.assertLessEqual(len(LEVELS), 8, 'landing.css only has tab rules for eight levels')
        for i in range(len(LEVELS)):
            self.assertContains(self.client.get('/'), 'id="lv-%d"' % i)
            self.assertContains(self.client.get('/'), 'lv-panel-%d' % i)

    def test_springs_and_shapes_are_generated(self):
        self.assertIn('--shape-cookie:polygon(', self.css)
        self.assertIn('--spring:linear(', self.css)


    def test_app_home_lives_under_app(self):
        self.assertEqual(self.client.get('/app/').status_code, 200)
        self.assertEqual(self.client.get('/app/library/').status_code, 200)

    def test_old_page_urls_redirect_permanently_and_keep_method_and_query(self):
        r = self.client.get('/library/?grade=Class%2012&sort=new')
        self.assertEqual(r.status_code, 308)
        self.assertEqual(r['Location'], '/app/library/?grade=Class%2012&sort=new')
        r = self.client.post('/forum/create/')
        self.assertEqual(r.status_code, 308)
        self.assertEqual(r['Location'], '/app/forum/create/')

    def test_api_auth_and_ajax_stay_at_the_root(self):
        self.assertNotEqual(self.client.get('/login/').status_code, 308)
        self.assertEqual(self.client.get('/robots.txt').status_code, 200)
        self.assertIn('/app/profile/edit/', self.client.get('/robots.txt').content.decode())

    def test_sitemap_points_at_app_pages(self):
        body = self.client.get('/sitemap-pages.xml').content.decode()
        self.assertIn('/app/library/', body)
        self.assertNotIn('consica.com.np/library/', body)

    def test_every_sitemap_file_serves_well_formed_xml(self):
        from xml.etree import ElementTree
        urlset = '{http://www.sitemaps.org/schemas/sitemap/0.9}urlset'
        for name in ('pages', 'library', 'forum', 'profiles'):
            r = self.client.get('/sitemap-%s.xml' % name)
            self.assertEqual(r.status_code, 200, name)
            self.assertEqual(ElementTree.fromstring(r.content).tag, urlset, name)
        self.assertTrue(len(ElementTree.fromstring(
            self.client.get('/sitemap-pages.xml').content)), 'pages is never empty')


class SiteThemeResolutionTests(TestCase):
    def setUp(self):
        cache.clear()

    def test_everyday_when_nothing_is_set(self):
        self.assertEqual(site_themes.resolve(dt.date(2026, 10, 18))['key'], 'everyday')

    def test_schedule_window_is_inclusive(self):
        SiteTheme.objects.create(key='dashain', starts_on=dt.date(2026, 10, 11), ends_on=dt.date(2026, 10, 25))
        self.assertEqual(site_themes.resolve(dt.date(2026, 10, 11))['key'], 'dashain')
        self.assertEqual(site_themes.resolve(dt.date(2026, 10, 25))['key'], 'dashain')
        self.assertEqual(site_themes.resolve(dt.date(2026, 10, 26))['key'], 'everyday')

    def test_a_theme_switched_on_now_beats_the_schedule(self):
        SiteTheme.objects.create(key='dashain', starts_on=dt.date(2026, 10, 1), ends_on=dt.date(2026, 10, 30))
        SiteTheme.objects.create(key='exams', is_forced=True)
        self.assertEqual(site_themes.resolve(dt.date(2026, 10, 18))['key'], 'exams')

    def test_garland_points_sit_on_the_string(self):
        data = site_themes.decor_data('dashain')
        self.assertEqual(len(data['dots']), 24)
        self.assertTrue(all(6 <= d['y'] <= 38 for d in data['dots']))
        self.assertTrue(data['path'].startswith('M0 6 Q'))

    def test_theme_reaches_the_landing_page(self):
        SiteTheme.objects.create(key='tihar', is_forced=True)
        site_themes.invalidate()
        r = Client().get('/')
        self.assertContains(r, 'data-site-theme="tihar"')
        self.assertContains(r, 'st-decor-tihar')

    def test_admin_page_needs_staff(self):
        r = Client().get('/admin/themes/')
        self.assertEqual(r.status_code, 302)


class AppThemeTests(TestCase):
    def setUp(self):
        cache.clear()

    def test_a_festive_theme_recolours_the_app_and_shows_the_season_card(self):
        SiteTheme.objects.create(key='tihar', is_forced=True)
        site_themes.invalidate()
        r = Client().get('/app/')
        self.assertContains(r, 'html[data-site-theme="tihar"]{--md-primary:#9A4600')
        self.assertContains(r, 'html[data-theme="dark"][data-site-theme="tihar"]')
        self.assertContains(r, 'class="st-season"')
        self.assertContains(r, 'st-motif-diyo')

    def test_everyday_leaves_the_app_alone(self):
        r = Client().get('/app/')
        self.assertNotContains(r, 'class="st-season"')
        self.assertNotContains(r, '--md-primary:#')

    def test_every_festive_theme_has_an_app_palette(self):
        for key in site_themes.THEMES:
            if key != site_themes.DEFAULT_KEY:
                self.assertIn(key, site_themes.APP)
                self.assertEqual(len(site_themes.APP[key]['light']), 4)

    def test_the_apps_can_ask_for_the_live_theme(self):
        r = Client().get('/api/site-theme/')
        self.assertEqual(r.json()['festive'], False)
        SiteTheme.objects.create(key='monsoon', is_forced=True)
        site_themes.invalidate()
        d = Client().get('/api/site-theme/').json()
        self.assertTrue(d['festive'])
        self.assertEqual(d['light']['primary'], '#006A60')
        self.assertEqual(d['motif'], 'drop')
        self.assertIn('cta', d['card'])


class M3XDesignSystemTests(TestCase):
    """The m3x layer is shared by the landing page and every app page: it carries the same hard rules."""

    def setUp(self):
        base = Path(__file__).resolve().parent / 'static' / 'web' / 'css'
        self.shared = (base / 'm3x.css').read_text(encoding='utf-8')
        self.app = (base / 'm3x-app.css').read_text(encoding='utf-8')

    def test_no_shadows_or_gradients_in_the_design_system(self):
        for src in (self.shared, self.app):
            self.assertNotRegex(src, r'box-shadow\s*:\s*(?!\s*none)')
            self.assertNotRegex(src, r'(drop|text)-shadow\s*:\s*(?!\s*none)')
            # A gradient may only be a mask (the scroll-edge fade on a toolbar); it never paints a colour.
            painted = re.sub(r'(?:-webkit-)?mask-image\s*:[^;}]*;?', '', src)
            self.assertNotRegex(painted, r'(linear|radial|conic)-gradient')

    def test_brand_blue_comes_from_the_logo(self):
        self.assertIn('--md-primary: #0058df', self.shared)
        self.assertIn('--ink: #06235f', self.shared)

    def test_landing_and_app_share_one_brand_partial_and_one_pill_nav(self):
        root = Path(__file__).resolve().parent / 'templates'
        for tpl in ('landing/_nav.html', 'base.html'):
            src = (root / tpl).read_text(encoding='utf-8')
            self.assertIn('components/_brand.html', src, tpl)
            self.assertIn('data-m3-nav', src, tpl)

    def test_app_pages_load_the_design_system(self):
        html = self.client.get('/app/library/').content.decode()
        self.assertIn('css/m3x.css', html)
        self.assertIn('css/m3x-app.css', html)
        self.assertIn('js/m3x.js', html)
