"""Coding-agent worker daemon.

Polls for queued / stalled-running sessions and advances them. Designed to
run under cron (`* * * * * cd /path && python manage.py run_coding_agent_worker`)
or as a long-lived process (when started without --once).

State persists in the database, so the worker can be killed and restarted
without losing progress.
"""
import logging
import signal
import time

from django.core.management.base import BaseCommand
from django.db import close_old_connections

from api.coding_agent.worker import advance_queued_sessions

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Poll for queued background-coding-agent sessions and advance them.'

    def add_arguments(self, parser):
        parser.add_argument('--interval', type=int, default=4, help='Poll interval in seconds')
        parser.add_argument('--once', action='store_true', help='Process one batch and exit')
        parser.add_argument('--max-sessions', type=int, default=2, help='Max sessions to advance per poll')
        parser.add_argument('--max-steps', type=int, default=6, help='Max LLM steps per session per poll')

    def handle(self, *args, **options):
        interval = options['interval']
        run_once = options['once']
        max_sessions = options['max_sessions']
        max_steps = options['max_steps']
        self.running = True

        def _stop(*_):
            self.running = False
        signal.signal(signal.SIGINT, _stop)
        signal.signal(signal.SIGTERM, _stop)

        self.stdout.write(self.style.NOTICE(
            'coding_agent worker started (interval=%ss, max_sessions=%d, max_steps=%d)' % (interval, max_sessions, max_steps)
        ))

        while self.running:
            try:
                close_old_connections()
                n = advance_queued_sessions(max_sessions=max_sessions, max_steps_per_session=max_steps)
                if n:
                    self.stdout.write('advanced %d session(s)' % n)
            except Exception as e:  # noqa: BLE001
                logger.exception('coding_agent worker cycle error: %s', e)
                self.stderr.write('cycle error: %s' % e)

            if run_once:
                break
            for _ in range(interval * 2):
                if not self.running:
                    break
                time.sleep(0.5)
        self.stdout.write('coding_agent worker stopped.')
