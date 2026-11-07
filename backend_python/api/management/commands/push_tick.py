"""Run everything time based in the push system once: due scheduled broadcasts and the library
autopilot round. The in-process worker does this too; cron is the safety net:

    */5 * * * * cd backend_python && python manage.py push_tick
"""
from django.core.management.base import BaseCommand

from api import resource_alerts


class Command(BaseCommand):
    help = 'Send due scheduled broadcasts and run the library autopilot round.'

    def add_arguments(self, parser):
        parser.add_argument('--force', action='store_true', help='Ignore quiet hours and the settle window.')

    def handle(self, *args, **opts):
        if opts['force']:
            c = resource_alerts.flush_pending(force=True)
            self.stdout.write(f'autopilot campaign: {c.id if c else None}')
            return
        self.stdout.write(str(resource_alerts.tick()))
