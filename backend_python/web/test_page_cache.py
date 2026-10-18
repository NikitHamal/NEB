from django.core.cache import cache
from django.http import HttpResponse
from django.test import RequestFactory, TestCase

from nebians.page_cache import AnonPageCacheMiddleware, _whitelisted


def _ok_view(request):
    token = b'z' * 64
    body = b'<meta name="csrf-token" content="' + token + b'"><p>hello</p>'
    return HttpResponse(body, content_type='text/html')


class AnonPageCacheMiddlewareTests(TestCase):
    def setUp(self):
        cache.clear()
        self.rf = RequestFactory()
        self.mw = AnonPageCacheMiddleware(_ok_view)

    def _get(self, path, **extra):
        req = self.rf.get(path, **extra)
        req.csp_nonce = 'test-nonce'
        return req

    def test_whitelist_matches_live_routes(self):
        self.assertTrue(_whitelisted('/'))
        self.assertTrue(_whitelisted('/app/faq/'))
        self.assertTrue(_whitelisted('/app/library/'))
        self.assertTrue(_whitelisted('/app/forum/'))
        self.assertTrue(_whitelisted('/app/news/'))
        self.assertTrue(_whitelisted('/app/news/some-slug/'))
        self.assertFalse(_whitelisted('/app/'))
        self.assertFalse(_whitelisted('/login/'))
        self.assertTrue(_whitelisted('/app/forum/post/abc/'))

    def test_second_anonymous_request_is_served_from_cache(self):
        first = self.mw(self._get('/app/forum/'))
        self.assertNotIn('X-Page-Cache', first)
        second = self.mw(self._get('/app/forum/'))
        self.assertEqual(second['X-Page-Cache'], 'hit')
        self.assertEqual(second.status_code, 200)
        self.assertIn(b'hello', second.content)

    def test_csrf_token_is_masked_in_storage_and_rebound_per_request(self):
        self.mw(self._get('/app/forum/'))
        stored = cache.get('anonpage:v1:' + __import__('hashlib').sha1(
            '|'.join(('testserver', '/app/forum/', 'd')).encode()).hexdigest())
        self.assertIsNotNone(stored)
        self.assertNotIn(b'z' * 64, stored)
        self.assertIn(b'\x00nebcsrf\x00', stored)
        second = self.mw(self._get('/app/forum/'))
        self.assertNotIn(b'\x00nebcsrf\x00', second.content)
        self.assertNotIn(b'z' * 64, second.content)

    def test_requests_with_a_session_cookie_bypass_the_cache(self):
        self.mw(self._get('/app/forum/'))
        req = self._get('/app/forum/')
        req.COOKIES['sessionid'] = 'anything'
        bypassed = self.mw(req)
        self.assertNotIn('X-Page-Cache', bypassed)
        second = self.mw(self._get('/app/forum/'))
        self.assertEqual(second['X-Page-Cache'], 'hit')

    def test_htmx_requests_bypass_the_cache(self):
        self.mw(self._get('/app/forum/'))
        req = self._get('/app/forum/')
        req.htmx = True
        bypassed = self.mw(req)
        self.assertNotIn('X-Page-Cache', bypassed)
        second = self.mw(self._get('/app/forum/'))
        self.assertEqual(second['X-Page-Cache'], 'hit')
