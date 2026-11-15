"""Replace the PDF of already published library books with a rebuilt file, from a staging folder.

The browser upload path cannot carry these files (LSAPI answers 500 Request Timeout well below the
size of a rebuilt book), so the new PDFs are streamed to the server and swapped here. Each resource
keeps its id, listing text and thumbnail, so links and search results survive; only the file changes.

    python manage.py replace_book_files /home/consicac/nebians_api/tmp/newpdfs --map tools/publish/published.json
    python manage.py replace_book_files /home/consicac/nebians_api/tmp/newpdfs --map ... --dry-run
    python manage.py replace_book_files /home/consicac/nebians_api/tmp/newpdfs --map ... --slug cs8 cee-phy

The map is the publisher's slug -> resource id file (tools/publish/published.json); a staged file is
named <slug>.pdf. Files that are byte identical to what is already stored are skipped. Every replaced
resource is set back to pending so the usual approval step runs:

    python manage.py approve_book_uploads nebians --yes
"""
import hashlib
import json
import os
import time

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand, CommandError

from api.models import Resource

STORAGE_DIR = 'resources/books'


def md5_of(path):
    h = hashlib.md5()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


class Command(BaseCommand):
    help = "Swap the stored PDF of published books with rebuilt files staged on disk."

    def add_arguments(self, parser):
        parser.add_argument('directory', help='folder holding <slug>.pdf files')
        parser.add_argument('--map', required=True, help='JSON file of slug -> resource id')
        parser.add_argument('--slug', nargs='*', default=[], help='only these slugs')
        parser.add_argument('--dry-run', action='store_true')
        parser.add_argument('--pending', action='store_true', default=True,
                            help='set replaced resources back to pending (default)')

    def handle(self, *args, **opts):
        directory = opts['directory']
        if not os.path.isdir(directory):
            raise CommandError('no such directory: %s' % directory)
        with open(opts['map'], encoding='utf-8') as fh:
            published = json.load(fh)
        slugs = opts['slug'] or list(published)
        unknown = [s for s in slugs if s not in published]
        if unknown:
            raise CommandError('not in the map: %s' % ', '.join(sorted(unknown)))

        replaced = skipped = missing = 0
        for slug in slugs:
            path = os.path.join(directory, slug + '.pdf')
            if not os.path.exists(path):
                missing += 1
                continue
            with open(path, 'rb') as fh:
                head = fh.read(5)
            if head != b'%PDF-':
                self.stderr.write('%s is not a PDF, skipped' % slug)
                missing += 1
                continue
            try:
                resource = Resource.objects.get(id=published[slug])
            except Resource.DoesNotExist:
                self.stderr.write('%s: resource %s is gone, skipped' % (slug, published[slug]))
                missing += 1
                continue

            new_md5 = md5_of(path)
            if resource.file and os.path.exists(resource.file.path) and md5_of(resource.file.path) == new_md5:
                skipped += 1
                continue
            if opts['dry_run']:
                self.stdout.write('would replace  %-52s %8.1f MB' % (slug, os.path.getsize(path) / 1048576))
                replaced += 1
                continue

            name = os.path.join(STORAGE_DIR, slug + '.pdf')
            with open(path, 'rb') as fh:
                stored = default_storage.save(name, ContentFile(fh.read()))
            old = resource.file.name if resource.file else ''
            resource.file = stored
            resource.file_size = os.path.getsize(path)
            resource.file_url = ''
            resource.approval_status = 'pending' if opts['pending'] else resource.approval_status
            resource.rejection_reason = ''
            resource.reviewed_at = 0
            resource.save(update_fields=['file', 'file_size', 'file_url', 'approval_status',
                                         'rejection_reason', 'reviewed_at'])
            if old and old != stored:
                try:
                    default_storage.delete(old)
                except OSError:
                    pass
            replaced += 1
            self.stdout.write('replaced       %-52s %8.1f MB' % (slug, resource.file_size / 1048576))

        self.stdout.write('\n%d replaced, %d already current, %d missing'
                          % (replaced, skipped, missing))
        if replaced and not opts['dry_run'] and opts['pending']:
            self.stdout.write('Approve with: python manage.py approve_book_uploads <username> --yes')
