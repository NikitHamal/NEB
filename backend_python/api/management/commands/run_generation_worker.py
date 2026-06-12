"""
Background worker that polls GenerationJob rows and processes them.

Run with: python manage.py run_generation_worker

Options:
  --interval SECONDS   Poll interval (default: 2)
  --once               Process one batch and exit
  --max-jobs N         Max jobs per poll cycle (default: 3)
"""
import logging
import signal
import time

from django.core.management.base import BaseCommand
from django.db import close_old_connections

from api.generation import (
    get_pending_jobs,
    mark_processing,
    mark_failed,
    cancel_stale_jobs,
    cleanup_old_jobs,
)
from api.generation_executors import EXECUTORS
from api.models import GenerationJob

logger = logging.getLogger(__name__)

MAX_RETRIES = 2  # retry a job up to 2 times before marking failed


class Command(BaseCommand):
    help = 'Poll for pending GenerationJobs and process them in the background'

    def add_arguments(self, parser):
        parser.add_argument('--interval', type=int, default=2, help='Poll interval in seconds (default: 2)')
        parser.add_argument('--once', action='store_true', help='Process one batch and exit')
        parser.add_argument('--max-jobs', type=int, default=3, help='Max jobs per poll cycle (default: 3)')

    def handle(self, *args, **options):
        interval = options['interval']
        run_once = options['once']
        max_jobs = options['max_jobs']
        self.running = True

        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

        self.stdout.write(f'Starting generation worker (interval={interval}s, max_jobs={max_jobs})')

        cycle = 0
        while self.running:
            try:
                self._process_cycle(max_jobs)
            except Exception as e:
                logger.exception('Generation worker cycle error: %s', e)
                self.stderr.write(f'Cycle error: {e}')

            cycle += 1
            if cycle % 30 == 0:
                try:
                    cancel_stale_jobs()
                except Exception:
                    pass
            if cycle % 100 == 0:
                try:
                    cleanup_old_jobs(days=7)
                except Exception:
                    pass

            if run_once:
                break

            time.sleep(interval)

        self.stdout.write('Generation worker stopped.')

    def _process_cycle(self, max_jobs):
        close_old_connections()
        jobs = get_pending_jobs(limit=max_jobs)
        for job in jobs:
            if not self.running:
                break
            self._process_job(job)
            close_old_connections()

    def _process_job(self, job):
        executor = EXECUTORS.get(job.job_type)
        if executor is None:
            mark_failed(job, f'Unknown job type: {job.job_type}')
            return

        mark_processing(job)
        # Re-fetch to get fresh state after mark_processing
        job.refresh_from_db()

        logger.info('Processing job %s type=%s', job.id, job.job_type)
        try:
            executor(job)
        except Exception as e:
            logger.exception('Job %s executor failed: %s', job.id, e)
            job.refresh_from_db()
            if job.status == GenerationJob.STATUS_PROCESSING:
                mark_failed(job, str(e)[:2000])

    def _signal_handler(self, signum, frame):
        self.stdout.write('Received signal, shutting down...')
        self.running = False