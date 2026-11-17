"""Heavy crawlers get a per-minute budget; people, search engines and previews never do."""
from django.core.cache import cache
from django.test import TestCase, override_settings

from nebians import crawler_shield

META = 'Mozilla/5.0 AppleWebKit/537.36 (compatible; meta-externalagent/1.1 (+https://developers.facebook.com/docs/sharing/webmasters/crawler))'
GOOGLE = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
FB_PREVIEW = 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)'
CHROME = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130.0 Safari/537.36'


@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache', 'LOCATION': 'shield-test'}})
class CrawlerShieldTests(TestCase):
    def setUp(self):
        cache.clear()

    def get(self, path, ua):
        return self.client.get(path, HTTP_USER_AGENT=ua, secure=True)

    def test_crawler_is_limited_after_budget(self):
        codes = [self.get('/login/', META).status_code for _ in range(crawler_shield._BUDGET + 3)]
        self.assertEqual(codes[:crawler_shield._BUDGET].count(429), 0)
        self.assertEqual(set(codes[crawler_shield._BUDGET:]), {429})
        resp = self.get('/login/', META)
        self.assertEqual(resp['Retry-After'], '300')

    def test_robots_and_static_always_answer(self):
        for _ in range(crawler_shield._BUDGET + 3):
            self.get('/login/', META)
        self.assertEqual(self.get('/robots.txt', META).status_code, 200)

    def test_search_engines_previews_and_browsers_are_never_limited(self):
        for ua in (GOOGLE, FB_PREVIEW, CHROME):
            codes = {self.get('/login/', ua).status_code for _ in range(crawler_shield._BUDGET + 5)}
            self.assertNotIn(429, codes, ua)

    def test_robots_disallows_claim_form(self):
        self.assertIn('Disallow: /app/schools/verify/', self.get('/robots.txt', CHROME).content.decode())
