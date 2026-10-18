import datetime as dt

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
        self.assertContains(r, 'Study <em class="lp-mark lp-mark-a">materials</em>')
        self.assertNotContains(r, 'material3.css')
        self.assertContains(r, 'href="/app/library/"')

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
        body = self.client.get('/sitemap.xml').content.decode()
        self.assertIn('/app/library/', body)
        self.assertNotIn('consica.com.np/library/', body)


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
