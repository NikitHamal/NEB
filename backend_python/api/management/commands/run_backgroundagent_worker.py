import time
import logging
import signal
from django.core.management.base import BaseCommand
from django.db import close_old_connections
from api.backgroundagent_worker import process_pending_sessions

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Run the background coding agent worker'

    def handle(self, *args, **options):
        self.running = True

        def _signal_handler(signum, frame):
            self.stdout.write('Shutting down background agent worker...')
            self.running = False

        signal.signal(signal.SIGINT, _signal_handler)
        signal.signal(signal.SIGTERM, _signal_handler)

        self.stdout.write('Starting background agent worker...')

        while self.running:
            try:
                close_old_connections()
                process_pending_sessions()
            except Exception as e:
                logger.error(f'Background agent worker error: {e}')

            time.sleep(5)

        self.stdout.write('Background agent worker stopped.')
