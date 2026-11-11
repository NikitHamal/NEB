"""A host-side MariaDB restart must produce a 503, not a 500.

The log counts 106 "Can't connect to MySQL server" errors, in clusters of 10-25
seconds (25 on 2026-10-09, 7 on 2026-10-14, 2 on 2026-11-11). Each one was a
500, an admin email, and a crash page for a visitor during a window that fixed
itself seconds later.

These tests pin the split that matters: connection-level errors are answered
503 with Retry-After, and every other exception still propagates so a genuine
bug keeps its 500 and its email. They also pin the ordering, because Django
offers an exception to each middleware's process_exception and the API
exception handler above this one answers /api/ errors with a 500 of its own.
"""
import json
import threading
from unittest import mock

from django.db import OperationalError, InterfaceError
from django.http import HttpResponse
from django.test import RequestFactory, TestCase, override_settings
from django.urls import path

from nebians.db_blip import DbBlipMiddleware, is_db_blip

# The exact shape Django hands over: args[0] is the pymysql tuple.
CONNECT_REFUSED = OperationalError((2003, "Can't connect to MySQL server on '127.0.0.1' ([Errno 111] Connection refused)"))
GONE_AWAY = OperationalError((2006, 'MySQL server has gone away'))
LOST_CONNECTION = OperationalError((2013, 'Lost connection to MySQL server during query'))
DEAD_SOCKET = InterfaceError('(0, "")')


def _view(**response_kwargs):
    def inner(request):
        return HttpResponse('ok', **response_kwargs)
    return inner


class DbBlipDetectionTests(TestCase):
    def test_connection_errors_are_blips(self):
        for exc in (CONNECT_REFUSED, GONE_AWAY, LOST_CONNECTION, DEAD_SOCKET):
            self.assertTrue(is_db_blip(exc), exc)

    def test_a_real_bug_is_not_a_blip(self):
        for exc in (
            OperationalError((1062, "Duplicate entry 'x' for key 'username'")),
            OperationalError((1054, "Unknown column 'class' in 'field list'")),
            OperationalError((1406, "Data too long for column 'class'")),
            ValueError('something else entirely'),
            KeyError('class_level'),
        ):
            self.assertFalse(is_db_blip(exc), exc)


class DbBlipResponseTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def _process(self, path='/app/schools/bal-chetna/', exc=CONNECT_REFUSED, **kwargs):
        """Drive the real Django hook, not a hand-rolled call."""
        request = self.factory.get(path, **kwargs)
        return DbBlipMiddleware(lambda r: None).process_exception(request, exc)

    def test_html_page_gets_a_503_with_retry_after(self):
        response = self._process()

        self.assertEqual(response.status_code, 503)
        self.assertEqual(response['Retry-After'], '5')
        self.assertIn(b'moment', response.content)

    def test_api_path_gets_json(self):
        response = self._process(path='/api/users/profile/')

        self.assertEqual(response.status_code, 503)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertIn('retry', json.loads(response.content)['error'])

    def test_json_accept_header_gets_json_too(self):
        response = self._process(headers={'accept': 'application/json'})

        self.assertEqual(response.status_code, 503)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_the_503_is_marked_as_logged_so_django_does_not_email_the_owner(self):
        # BaseHandler.get_response logs every >=400 response at error level on
        # django.request, which has mail_admins. A 503 that stays "unlogged"
        # would send one email per failed request.
        response = self._process()

        self.assertTrue(getattr(response, '_has_been_logged', False))

    def test_a_real_bug_returns_none_so_django_still_500s(self):
        # process_exception returning None is how Django says "not mine".
        for exc in (
            OperationalError((1406, "Data too long for column 'class'")),
            OperationalError((1062, "Duplicate entry 'x' for key 'username'")),
            ValueError('unrelated'),
            KeyError('class_level'),
        ):
            self.assertIsNone(self._process(exc=exc), exc)

    def test_normal_response_passes_through_untouched(self):
        mw = DbBlipMiddleware(_view(status=200))

        self.assertEqual(mw(self.factory.get('/')).status_code, 200)


class DbBlipLoggingTests(TestCase):
    """The owner should hear about the outage once, not once per request."""

    def setUp(self):
        self.factory = RequestFactory()
        self.mw = DbBlipMiddleware(lambda r: None)

    def _blip(self, path='/app/'):
        import nebians.db_blip as db_blip

        db_blip._note(path)

    def test_repeated_blips_log_once_inside_the_window(self):
        import nebians.db_blip as db_blip

        db_blip._last_log_at = 0.0
        with mock.patch.object(db_blip, 'logger') as log:
            for _ in range(10):
                self._blip()
            self.assertEqual(log.warning.call_count, 1)

    def test_a_blip_after_the_window_logs_again(self):
        import nebians.db_blip as db_blip

        db_blip._last_log_at = 0.0
        with mock.patch.object(db_blip, 'logger') as log:
            self._blip()
            db_blip._last_log_at -= db_blip._LOG_EVERY_SECONDS + 1
            self._blip()
            self.assertEqual(log.warning.call_count, 2)

    def test_logging_never_breaks_the_response(self):
        import nebians.db_blip as db_blip

        db_blip._last_log_at = 0.0
        with mock.patch.object(db_blip, 'logger', side_effect=RuntimeError('log broke')):
            request = self.factory.get('/app/')
            self.assertEqual(self.mw.process_exception(request, CONNECT_REFUSED).status_code, 503)


def _blip_view(request):
    raise LOST_CONNECTION


def _bug_view(request):
    raise ValueError('a real bug, not a blip')


urlpatterns = [
    path('api/db-blip/', _blip_view),
    path('app/db-blip/', _blip_view),
    path('api/real-bug/', _bug_view),
]


@override_settings(ROOT_URLCONF=__name__, NEWS_AUTOSYNC=False)
class DbBlipThroughTheRealStackTests(TestCase):
    """The 503 has to survive the middleware that runs before it.

    Django offers an exception to each middleware's process_exception in
    MIDDLEWARE order, and ApiUnhandledExceptionMiddleware answers every /api/
    exception with a 500 plus an error-level log line on django.request (which
    carries mail_admins). It was therefore winning every API request: the
    visitor saw a 500 and the owner got an email, with DbBlipMiddleware sitting
    right there in the list and never getting a turn. It now declines
    connection-level errors and leaves them to the 503.
    """

    def test_api_blip_is_a_503_not_a_500(self):
        response = self.client.get('/api/db-blip/')

        self.assertEqual(response.status_code, 503)
        self.assertEqual(response['Retry-After'], '5')
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_html_blip_is_a_503(self):
        self.assertEqual(self.client.get('/app/db-blip/').status_code, 503)

    def test_the_blip_never_reaches_django_request(self):
        # django.request at ERROR is the mail_admins path: one email per request
        # is the flood this whole module exists to stop.
        with self.assertNoLogs('django.request', level='ERROR'):
            self.client.get('/api/db-blip/')

    def test_a_real_api_bug_still_500s_and_still_logs(self):
        with self.assertLogs('django.request', level='ERROR'):
            response = self.client.get('/api/real-bug/')

        self.assertEqual(response.status_code, 500)
