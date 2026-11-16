"""collectstatic's compression pool must stay inside the box's thread budget.

Whitenoise 6.12 builds its pool with the ThreadPoolExecutor default,
min(32, cpu_count + 4): 32 threads on the live box's 80 cores. That box is
shared cPanel with a per-account LVE thread budget, and daphne alone holds ~64
threads, so on 2026-11-16 the pool blew the budget and post_process raised
"RuntimeError: can't start new thread" *after* it had already begun rewriting
staticfiles/. The deploy then stopped (correctly) between extraction and the
worker restart.

Importing nebians.storage bounds the pool. These tests pin that, because the
failure mode is silent at import time and only shows up mid-deploy.

Run: ``python manage.py test nebians.test_storage_pool -v 2``
"""
import whitenoise.storage as whitenoise_storage
from django.test import SimpleTestCase, override_settings

import nebians.storage  # noqa: F401  (the import is the behaviour under test)


class BoundedPoolTests(SimpleTestCase):
    def _pool(self):
        return whitenoise_storage.ThreadPoolExecutor()

    def test_whitenoise_uses_our_bounded_factory(self):
        # whitenoise.storage resolves ThreadPoolExecutor from its module globals,
        # so a plain replacement there is what bounds post_process.
        self.assertIs(whitenoise_storage.ThreadPoolExecutor, nebians.storage._bounded_executor)

    def test_default_pool_is_small(self):
        pool = self._pool()
        try:
            self.assertEqual(pool._max_workers, nebians.storage._MAX_POST_PROCESS_WORKERS)
            self.assertLessEqual(pool._max_workers, 8)
        finally:
            pool.shutdown(wait=False)

    @override_settings(STATIC_POST_PROCESS_WORKERS=2)
    def test_the_pool_size_can_be_overridden(self):
        pool = self._pool()
        try:
            self.assertEqual(pool._max_workers, 2)
        finally:
            pool.shutdown(wait=False)

    def test_an_explicit_max_workers_still_wins(self):
        # Nothing else may use this hook to quietly raise the ceiling.
        pool = whitenoise_storage.ThreadPoolExecutor(max_workers=1)
        try:
            self.assertEqual(pool._max_workers, 1)
        finally:
            pool.shutdown(wait=False)
