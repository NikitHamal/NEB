from django.test import SimpleTestCase, TestCase

from nebians.canonical_url import clean_query


class CleanQueryTests(SimpleTestCase):
    def test_strips_referral_and_tracking(self):
        q, changed = clean_query('from=AppAgg.com&utm_campaign=AppAgg.com&utm_medium=referral&q=IOE')
        self.assertTrue(changed)
        self.assertEqual(q, 'q=IOE')

    def test_keeps_real_filters(self):
        q, changed = clean_query('grade=Class+12&sort=top&from=2024-01-01')
        self.assertFalse(changed)
        self.assertIn('sort=top', q)

    def test_empty(self):
        self.assertEqual(clean_query(''), ('', False))


class RedirectTests(TestCase):
    def test_www_host_redirects_to_bare_host(self):
        r = self.client.get('/app/library/?q=IOE', HTTP_HOST='www.nebians.consica.com.np')
        self.assertEqual(r.status_code, 301)
        self.assertEqual(r['Location'], 'https://nebians.consica.com.np/app/library/?q=IOE')

    def test_tracking_params_redirect(self):
        r = self.client.get('/about/?utm_source=x&from=AppAgg.com')
        self.assertEqual(r.status_code, 301)
        self.assertEqual(r['Location'], 'https://nebians.consica.com.np/about/')

    def test_robots_and_llms(self):
        robots = self.client.get('/robots.txt').content.decode()
        self.assertIn('User-agent: GPTBot', robots)
        self.assertIn('Disallow: /login/', robots)
        self.assertIn('Sitemap:', robots)
        llms = self.client.get('/llms.txt')
        self.assertEqual(llms.status_code, 200)
        self.assertIn('# NEBians', llms.content.decode())
