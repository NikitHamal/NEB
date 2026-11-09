from django.core.management.base import BaseCommand

from api.institutions import import_catalog


class Command(BaseCommand):
    help = 'Add institutions from api/data/institutions.json.gz that are not in the database yet.'

    def add_arguments(self, parser):
        parser.add_argument('--path', default='')

    def handle(self, *args, **opts):
        added, existing = import_catalog(opts['path'] or None)
        self.stdout.write('added %d, already present %d' % (added, existing))
