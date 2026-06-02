"""Management command to process pending Neby AI tasks.

Run via cron every minute:
    * * * * * cd /home/consicac/nebians_api && source /home/consicac/virtualenv/nebians_api/3.13/bin/activate && python manage.py process_neby_tasks >> /home/consicac/nebians_api/logs/neby_cron.log 2>&1

Or run manually:
    python manage.py process_neby_tasks
    python manage.py process_neby_tasks --max 5      # process at most 5 tasks
    python manage.py process_neby_tasks --retry       # also retry failed tasks
"""
import logging
import time

from django.core.management.base import BaseCommand
from api.models import NebyTask
from api.neby import process_neby_task, is_neby_enabled

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Process pending Neby AI tasks from the task queue'

    def add_arguments(self, parser):
        parser.add_argument(
            '--max',
            type=int,
            default=10,
            help='Maximum number of tasks to process in one run (default: 10)',
        )
        parser.add_argument(
            '--retry',
            action='store_true',
            help='Also retry failed tasks (max 3 attempts)',
        )
        parser.add_argument(
            '--max-attempts',
            type=int,
            default=3,
            help='Max attempts before giving up on a task (default: 3)',
        )

    def handle(self, *args, **options):
        if not is_neby_enabled():
            self.stdout.write('Neby is disabled, skipping.')
            return

        max_tasks = options['max']
        retry_failed = options['retry']
        max_attempts = options['max_attempts']

        queryset = NebyTask.objects.filter(status='pending')
        if retry_failed:
            queryset = queryset | NebyTask.objects.filter(
                status='failed', attempts__lt=max_attempts
            )

        tasks = queryset.order_by('created_at')[:max_tasks]

        processed = 0
        for task in tasks:
            start = time.time()
            self.stdout.write(f'Processing task {task.id} ({task.trigger}, post={task.post_id})...')
            try:
                process_neby_task(task)
                task.refresh_from_db()
                elapsed = time.time() - start
                self.stdout.write(self.style.SUCCESS(
                    f'  Task {task.id}: {task.status} in {elapsed:.1f}s'
                ))
            except Exception as e:
                elapsed = time.time() - start
                self.stdout.write(self.style.ERROR(
                    f'  Task {task.id}: exception {e} in {elapsed:.1f}s'
                ))
                logger.error(f'Neby task {task.id} exception: {e}', exc_info=True)
            processed += 1

        self.stdout.write(f'Done. Processed {processed} task(s).')