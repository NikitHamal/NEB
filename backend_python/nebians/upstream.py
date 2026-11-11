"""A provider outage is not a broken page.

The PDF tutor asks Qwen's anonymous sessions first and then walks Neby's
provider chain. Both are other people's servers, and both go dark as a group:
Qwen's session pool refills fail in bulk, and the free proxies behind the chain
get rate-limited together. That used to answer 502, which Django logs at error
level on django.request, which carries mail_admins: one email per question
typed, for as long as the outage lasts.

An upstream outage is a 503 with Retry-After. The client can retry, the visitor
reads an honest sentence, and the owner gets one WARNING per window instead of
one email per request. This is the same bargain `nebians.db_blip` makes for the
database, and it keeps the same boundary: only a provider that answered nothing
lands here. Anything that raises still raises, still 500s, and still emails.
"""
import logging
import threading
import time

from django.http import JsonResponse

RETRY_AFTER = 20
LOG_EVERY_SECONDS = 60.0

logger = logging.getLogger('nebians.upstream')

_lock = threading.Lock()
_last_log_at = 0.0


def _note(path, detail=''):
    """Log the first failure, then at most one line per window."""
    global _last_log_at
    now = time.monotonic()
    with _lock:
        quiet = (now - _last_log_at) < LOG_EVERY_SECONDS
        if not quiet:
            _last_log_at = now
    try:
        if quiet:
            return
        if detail:
            logger.warning('upstream answered nothing, serving 503: %s (%s)', path, detail)
        else:
            logger.warning('upstream answered nothing, serving 503: %s', path)
    except Exception:
        # Logging must never be the reason a request fails.
        pass


def unavailable(path, message, detail=''):
    """503 the client can retry on, without Django mailing the owner about it."""
    _note(path, detail)
    response = JsonResponse({'error': message, 'code': 'UPSTREAM_UNAVAILABLE'}, status=503)
    response['Retry-After'] = str(RETRY_AFTER)
    # BaseHandler.get_response logs every >=400 at error level on django.request,
    # which carries mail_admins. log_response() returns early once this flag is
    # set, so an outage costs the one line above instead of an email per request.
    response['Cache-Control'] = 'no-store'
    response._has_been_logged = True
    return response
