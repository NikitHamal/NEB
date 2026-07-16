"""Background worker that polls CodingTask rows and processes them.

Run with: python manage.py run_coding_agent_worker

Options:
  --interval SECONDS   Poll interval (default: 3)
  --once               Process one batch and exit
  --max-tasks N        Max tasks per poll cycle (default: 1)
"""
import logging
import signal
import time

from django.core.management.base import BaseCommand
from django.db import close_old_connections

from api.coding_agent.queue import get_pending_tasks, cancel_stale_tasks, cleanup_old_tasks
from api.coding_agent.engine import process_task
from api.models import CodingTask

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Poll for pending CodingTasks and process them with the AI coding agent'

    def add_arguments(self, parser):
        parser.add_argument('--interval', type=int, default=3, help='Poll interval in seconds (default: 3)')
        parser.add_argument('--once', action='store_true', help='Process one batch and exit')
        parser.add_argument('--max-tasks', type=int, default=1, help='Max tasks per poll cycle (default: 1)')

    def handle(self, *args, **options):
        interval = options['interval']
        run_once = options['once']
        max_tasks = options['max_tasks']
        self.running = True

        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

        self.stdout.write(f'Starting coding agent worker (interval={interval}s, max_tasks={max_tasks})')

        cycle = 0
        while self.running:
            try:
                self._process_cycle(max_tasks)
            except Exception as e:
                logger.exception('Coding agent worker cycle error: %s', e)
                self.stderr.write(f'Cycle error: {e}')

            cycle += 1
            if cycle % 60 == 0:
                try:
                    cancel_stale_tasks()
                except Exception:
                    pass
            if cycle % 200 == 0:
                try:
                    cleanup_old_tasks(days=30)
                except Exception:
                    pass

            if run_once:
                break

            time.sleep(interval)

        self.stdout.write('Coding agent worker stopped.')

    def _process_cycle(self, max_tasks):
        close_old_connections()
        tasks = get_pending_tasks(limit=max_tasks)
        for task in tasks:
            if not self.running:
                break
            self._process_task(task)
            close_old_connections()

    def _process_task(self, task):
        if task.status == CodingTask.STATUS_COMPLETED or task.status == CodingTask.STATUS_STOPPED:
            return
        if task.status == CodingTask.STATUS_FAILED:
            return

        logger.info('Processing coding task %s: %s', task.id, task.title)
        try:
            process_task(task.id)
        except Exception as e:
            logger.exception('Coding task %s failed: %s', task.id, e)
            task.refresh_from_db()
            if task.status in (CodingTask.STATUS_RUNNING, CodingTask.STATUS_QUEUED):
                from api.coding_agent.queue import mark_failed
                mark_failed(task, str(e)[:2000])

    def _signal_handler(self, signum, frame):
        self.stdout.write('Received signal, shutting down...')
        self.running = False
