"""An upstream provider going dark must not email the owner once per request.

Django logs every 5xx response at error level on django.request, and that
logger carries mail_admins. The PDF tutor answered 502 whenever every provider
answered nothing, so a provider outage arrived as one email per question typed.
These tests pin the replacement: a 503 the client can retry, one WARNING per
window, and no django.request log line at all.
"""
import json
from unittest import mock

from django.test import SimpleTestCase

from nebians import upstream


class UpstreamResponseTests(SimpleTestCase):
    def setUp(self):
        upstream._last_log_at = 0.0

    def test_it_is_a_503_the_client_can_retry(self):
        response = upstream.unavailable('/api/resources/x/pdf-assistant/', 'Neby is busy.')

        self.assertEqual(response.status_code, 503)
        self.assertEqual(response['Retry-After'], str(upstream.RETRY_AFTER))
        self.assertEqual(json.loads(response.content)['code'], 'UPSTREAM_UNAVAILABLE')
        self.assertEqual(json.loads(response.content)['error'], 'Neby is busy.')

    def test_django_does_not_log_or_mail_it_again(self):
        # log_response() returns early once this flag is set; without it every
        # failed request is one admin email.
        response = upstream.unavailable('/api/x/', 'Neby is busy.')

        self.assertTrue(getattr(response, '_has_been_logged', False))

    def test_a_busy_provider_is_not_cached(self):
        self.assertEqual(upstream.unavailable('/api/x/', 'busy')['Cache-Control'], 'no-store')


class UpstreamLoggingTests(SimpleTestCase):
    def setUp(self):
        upstream._last_log_at = 0.0

    def test_repeated_failures_log_once_inside_the_window(self):
        with mock.patch.object(upstream, 'logger') as log:
            for _ in range(10):
                upstream.unavailable('/api/x/', 'busy', 'qwen pool empty')
        self.assertEqual(log.warning.call_count, 1)
        self.assertIn('qwen pool empty', log.warning.call_args[0][-1])

    def test_a_failure_after_the_window_logs_again(self):
        with mock.patch.object(upstream, 'logger') as log:
            upstream.unavailable('/api/x/', 'busy')
            upstream._last_log_at -= upstream.LOG_EVERY_SECONDS + 1
            upstream.unavailable('/api/x/', 'busy')
        self.assertEqual(log.warning.call_count, 2)

    def test_logging_never_breaks_the_response(self):
        with mock.patch.object(upstream, 'logger', side_effect=RuntimeError('log broke')):
            self.assertEqual(upstream.unavailable('/api/x/', 'busy').status_code, 503)
