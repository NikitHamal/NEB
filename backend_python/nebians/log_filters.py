"""Logging filters for production noise control.

Sep 2026 incident: a Redis outage made every request 500 and each one emailed
the admins via the ``mail_admins`` handler, flooding the inbox. The app now
degrades gracefully without Redis, but any residual cache-transport error must
still never send mail. Attach ``SkipRedisNoiseFilter`` to ``mail_admins`` only;
file/console logging is unaffected so the signal is still on disk.
"""
import logging


class SkipRedisNoiseFilter(logging.Filter):
    def filter(self, record):
        try:
            if record.exc_info:
                exc_type = record.exc_info[0]
                name = getattr(exc_type, '__name__', '') or ''
                module = getattr(exc_type, '__module__', '') or ''
                haystack = (name + ' ' + module).lower()
                if 'redis' in haystack or 'connection' in haystack:
                    return False
            message = str(record.getMessage()).lower()
            if 'redis' in message and (
                'refused' in message
                or 'econnrefused' in message
                or 'connection' in message
                or 'timeout' in message
                or 'unavailable' in message
            ):
                return False
        except Exception:
            pass
        return True


try:
    import re as _re
    from django.views.debug import SafeExceptionReporterFilter as _SafeFilter

    class RedactingExceptionReporterFilter(_SafeFilter):
        """Admin error emails dump every setting. Django masks names holding KEY, SECRET, PASS,
        TOKEN, API and AUTH, which let the Redis URL (password inside), the cache and channel
        layer dicts and the DB account through in the Nov 2026 report. Mask those as well."""
        hidden_settings = _re.compile(
            _SafeFilter.hidden_settings.pattern + r'|REDIS|CACHE|CHANNEL|DATABASE|DB_|BRIDGE|SALT|_URL$|DSN',
            flags=_re.I,
        )
except Exception:  # Django not importable (tooling that imports this module alone)
    RedactingExceptionReporterFilter = None
