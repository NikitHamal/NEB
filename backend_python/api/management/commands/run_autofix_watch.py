"""Auto-fix watcher daemon.

Polls GitHub Actions for failed runs on every auto-fix-enabled project and
queues background-agent repair sessions with the failing job log attached.

Run under cron:
  */2 * * * * cd /path && python manage.py run_autofix_watch --once
or as a long-lived process (default interval 120s).
"""
from __future__ import annotations

import logging
import signal
import time

from django.core.management.base import BaseCommand
from django.db import close_old_connections

from api.background_agent.autofix import scan_failed_runs

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Watch failed GitHub Actions runs and queue background-agent auto-fix sessions.'

    def add_arguments(self, parser):
        parser.add_argument('--interval', type=int, default=120, help='Poll interval in seconds')
        parser.add_argument('--once', action='store_true', help='Run one scan and exit')
        parser.add_argument('--max-sessions', type=int, default=3, help='Max sessions to queue per scan')

    def handle(self, *args, **options):
        interval = options['interval']
        run_once = options['once']
        max_sessions = options['max_sessions']
        self.running = True

        def _stop(*_):
            self.running = False
        signal.signal(signal.SIGINT, _stop)
        signal.signal(signal.SIGTERM, _stop)

        self.stdout.write(self.style.NOTICE(
            'autofix watcher started (interval=%ss, max_sessions=%d)' % (interval, max_sessions)
        ))
        while self.running:
            try:
                close_old_connections()
                created = scan_failed_runs(max_sessions=max_sessions)
                if created:
                    self.stdout.write('queued %d auto-fix session(s)' % created)
            except Exception as exc:  # noqa: BLE001
                logger.exception('autofix watcher cycle error: %s', exc)
                self.stderr.write('cycle error: %s' % exc)
            if run_once:
                break
            for _ in range(interval * 2):
                if not self.running:
                    break
                time.sleep(0.5)
        self.stdout.write('autofix watcher stopped.')
