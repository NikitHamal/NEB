"""Offline tests for api.proxy_http (no network — fake sessions only)."""
from django.test import SimpleTestCase

from api import proxy_http as ph


class _FailingCurlSession:
    _neb_plain = False

    def __init__(self):
        self.headers = {"User-Agent": "curl-test"}
        self.cookies = {}
        self.proxies = {}

    def post(self, url, **kwargs):
        raise RuntimeError("Failed to perform, curl: (6) getaddrinfo() thread failed to start")


class _FailingPlainSession(_FailingCurlSession):
    _neb_plain = True


class ProxyHttpTests(SimpleTestCase):
    def test_new_session_plain(self):
        s = ph.new_session(force_requests=True)
        self.assertTrue(ph.is_plain(s))
        s.close()

    def test_new_session_default(self):
        s = ph.new_session()
        self.assertFalse(ph.is_plain(s))
        try:
            s.close()
        except Exception:
            pass

    def test_plain_failure_raises_without_retry(self):
        with self.assertRaises(RuntimeError):
            ph.resilient_post(_FailingPlainSession(), "https://example.com")

    def test_proxy_kwarg_accepted(self):
        s = ph.new_session(force_requests=True)
        try:
            s.proxies.update({"http": "http://127.0.0.1:9", "https": "http://127.0.0.1:9"})
            with self.assertRaises(Exception):
                ph.resilient_get(s, "https://example.com", timeout=1, proxy="http://127.0.0.1:9")
        finally:
            s.close()
