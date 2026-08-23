"""Autonomous Neby heartbeat.

Cron (every 10 minutes):
    */10 * * * * cd /home/consicac/nebians_api && source /home/consicac/virtualenv/nebians_api/3.13/bin/activate && python manage.py run_neby_agent --once >> logs/neby_agent.log 2>&1

Daemon:
    python manage.py run_neby_agent --interval 120
"""
import logging
import time

from django.core.management.base import BaseCommand

from api.agent_social.heartbeat import tick_all, tick_neby

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Run Neby (and other autonomous agents) for one tick, or as a daemon.'

    def add_arguments(self, parser):
        parser.add_argument('--once', action='store_true', help='Run a single tick and exit.')
        parser.add_argument('--force', action='store_true', help='Ignore tick interval.')
        parser.add_argument('--interval', type=int, default=120, help='Seconds between ticks in daemon mode.')
        parser.add_argument('--all', action='store_true', dest='all_agents', help='Tick every autonomous persona.')

    def handle(self, *args, **options):
        once = options['once']
        force = options['force']
        interval = max(int(options['interval'] or 120), 30)

        def run():
            if options['all_agents']:
                return tick_all(force=force, source='heartbeat')
            return [tick_neby(force=force, source='heartbeat')]

        if once:
            results = run()
            for row in results:
                if row.get('ok'):
                    self.stdout.write(self.style.SUCCESS(str(row)))
                else:
                    self.stdout.write(self.style.WARNING(str(row)))
            return

        self.stdout.write(f'Neby agent daemon interval={interval}s')
        while True:
            try:
                results = run()
                for row in results:
                    self.stdout.write(str(row))
            except Exception as exc:
                logger.exception('neby agent daemon tick failed')
                self.stderr.write(str(exc))
            time.sleep(interval)
