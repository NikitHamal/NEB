"""A short database outage must not read as a broken site.

The host restarts MariaDB from time to time. The log counts 106 "Can't connect
to MySQL server" errors, clustered rather than spread: 25 on 2026-10-09, 7 on
2026-10-14, 2 on 2026-11-11. Each cluster is a 10 to 25 second window in which
every DB-touching request raised, Django mailed the owner a 500 per request, and
the visitor saw a crash page for a condition that fixes itself in seconds.

This middleware answers 503 with Retry-After instead, and logs one line. Only
connection-level errors are caught:

  2003  cannot connect to the server
  2006  server has gone away
  2013  lost connection during the query
        plus pymysql's InterfaceError for a socket that closed mid-request

A real bug still raises, still 500s, and still reaches the owner. The test
suite pins both halves of that split.
"""
import logging
import threading
import time

from django.db import InterfaceError

logger = logging.getLogger('nebians.db_blip')

# MySQL/PyMySQL error codes that mean "the server is not there", not "the query
# is wrong". Anything else re-raises untouched.
_CONNECT_CODES = frozenset({2003, 2006, 2013})
_CONNECT_TEXT = (
    'gone away',
    'lost connection',
    "can't connect",
    'connection refused',
    'server closed the connection',
)

_RETRY_AFTER = 5
_LOG_EVERY_SECONDS = 30.0

_HTML = (
    '<!doctype html><html lang="en"><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1">'
    '<title>NEBians is right back</title>'
    '<style>body{margin:0;min-height:100vh;display:grid;place-items:center;'
    'font-family:Poppins,system-ui,sans-serif;background:var(--md-surface,#fff);'
    'color:var(--md-on-surface,#111)}.b{text-align:center;padding:24px}'
    '.s{width:44px;height:44px;margin:0 auto 20px;border-radius:50%;'
    'border:3px solid var(--md-primary,#1b6ef3);border-right-color:transparent;'
    'animation:r 1s linear infinite}@keyframes r{to{transform:rotate(360deg)}}'
    'p{margin:8px 0 0;color:var(--md-on-surface-variant,#555);font-size:.95rem}</style>'
    '</head><body><div class="b"><div class="s"></div>'
    '<h1>Give us a moment</h1>'
    '<p>NEBians is catching its breath. This page will work in a few seconds.</p>'
    '</div></body></html>'
)

_log_lock = threading.Lock()
_last_log_at = 0.0


def is_db_blip(exc) -> bool:
    """True only for the connection-level failures this middleware handles."""
    # A DB-API InterfaceError is only ever a broken connection or a socket that
    # closed mid-query, never a bad query, so it needs no code check.
    if isinstance(exc, InterfaceError):
        return True
    args = getattr(exc, 'args', None) or ()
    first = args[0] if args else None
    if isinstance(first, tuple) and first and isinstance(first[0], int):
        return first[0] in _CONNECT_CODES
    text = str(first if first is not None else exc).lower()
    return any(hint in text for hint in _CONNECT_TEXT)


def _note(path: str) -> None:
    """Log the first blip, then at most one line every 30 seconds.

    A 20-second outage on a busy page is dozens of requests; the owner needs to
    know it happened, not to receive a hundred copies of the same sentence.
    """
    global _last_log_at
    now = time.monotonic()
    with _log_lock:
        quiet = (now - _last_log_at) < _LOG_EVERY_SECONDS
        if not quiet:
            _last_log_at = now
    if quiet:
        return
    logger.warning('database unavailable, serving 503: %s', path)


def _response(request):
    from django.http import HttpResponse, JsonResponse

    if request.path.startswith('/api/') or 'application/json' in request.headers.get('Accept', ''):
        response = JsonResponse({'error': 'Service briefly unavailable. Please retry.'}, status=503)
    else:
        response = HttpResponse(_HTML, status=503, content_type='text/html')
    response['Retry-After'] = str(_RETRY_AFTER)
    # Django logs every 4xx/5xx at error level on django.request, which carries
    # mail_admins: without this the owner gets one email per failed request,
    # which is exactly the flood this middleware exists to stop. log_response()
    # returns early once this flag is set, and our own WARNING above is the
    # record that the outage happened.
    response._has_been_logged = True
    return response


class DbBlipMiddleware:
    """Turn a database restart into a 503 instead of a 500 and an email flood.

    Django converts an exception raised in the view at the innermost wrapper, so
    `process_exception` is the only place a middleware can intercept it. It must
    sit below `ApiUnhandledExceptionMiddleware` in MIDDLEWARE, because Django
    calls `process_exception` from the bottom of the list upwards.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        if not is_db_blip(exception):
            return None
        _note(request.path)
        return _response(request)
