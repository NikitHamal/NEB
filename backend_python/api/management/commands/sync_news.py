from django.core.management.base import BaseCommand

from services import news_sources
from services.news_sync import run_sync


class Command(BaseCommand):
    help = 'Import official notices and education news into the blog (the autopilot, run by hand or cron).'

    def add_arguments(self, parser):
        parser.add_argument('--source', action='append', choices=[s['key'] for s in news_sources.SOURCES],
                            help='Only this source (repeatable). Default: every enabled source.')
        parser.add_argument('--force', action='store_true', help='Also run sources an admin switched off.')

    def handle(self, *args, **opts):
        for r in run_sync(only=opts['source'], force=opts['force']):
            self.stdout.write('%-14s +%-3d %s' % (r['key'], r['new'], r['status']))
