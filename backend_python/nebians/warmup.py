"""Pay the lazy first-request costs once, in the LSAPI parent, so forked workers start hot.

LiteSpeed's lswsgi imports ``passenger_wsgi`` in ONE parent process and forks every request
worker from it (a new worker appears on each burst after idle). Django imports most of the
site on the first request, so every freshly forked worker made one visitor wait 1 to 3 s
(redis client 0.5 s, every view module, template compilation). Anything done here is
inherited copy-on-write by every later fork and costs nothing per worker.

Rules: no network, no database connection, no thread (sockets and threads do not survive a
fork); a hard time budget; every step isolated so a failure can only skip an optimisation.
"""
import logging
import os
import time

logger = logging.getLogger(__name__)

BUDGET_SECONDS = 12.0


def _template_names():
    from django.conf import settings
    names = []
    for base in settings.BASE_DIR.joinpath('web', 'templates').glob('**/*.html'):
        rel = base.relative_to(settings.BASE_DIR / 'web' / 'templates').as_posix()
        if rel.startswith(('admin_panel/', 'themes/')):
            continue
        names.append(rel)
    # base layouts and the busiest pages first, in case the budget runs out
    names.sort(key=lambda n: (0 if n in ('base.html', 'landing/index.html') else 1, n))
    return names


def warm():
    started = time.monotonic()
    done = []

    def step(label, fn):
        if time.monotonic() - started > BUDGET_SECONDS:
            return
        try:
            fn()
            done.append(label)
        except Exception as exc:  # an optimisation must never stop the site from starting
            logger.warning('warmup %s skipped: %s', label, type(exc).__name__)

    def imports():
        import redis  # noqa: F401  (0.5 s: pulled in lazily by the first cache call)
        import redis.asyncio  # noqa: F401
        import nebians.cache_fallback  # noqa: F401
        import pymysql  # noqa: F401
        import rest_framework.throttling  # noqa: F401
        import PIL.Image  # noqa: F401

    def backends():
        # Builds the wrapper objects only: no socket is opened until first use.
        from django.db import connections
        connections['default']
        from django.core.cache import caches
        caches['default']

    def urlconf():
        from django.urls import get_resolver
        get_resolver()._populate()  # imports every view module

    def templates():
        from django.template.loader import get_template
        for name in _template_names():
            if time.monotonic() - started > BUDGET_SECONDS:
                break
            try:
                get_template(name)
            except Exception:
                pass

    step('imports', imports)
    step('backends', backends)
    step('urlconf', urlconf)
    step('templates', templates)

    try:  # belt and braces: nothing connected may be inherited by a child
        from django.db import connections
        connections.close_all()
    except Exception:
        pass
    logger.info('warmup %s in %.1fs (pid %s)', ','.join(done), time.monotonic() - started, os.getpid())
