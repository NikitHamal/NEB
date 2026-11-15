"""Create (or refresh) the past paper library resources from a staged folder.

Built for the 68 rebuilt NEB board papers: the browser upload path cannot carry the batch and the
listing text has to be generated, not typed, so the metadata comes from
tools/publish/papers_listing.json (written by tools/publish/build_papers.py) and the files are
streamed to the server first.

    python manage.py import_past_papers /home/consicac/nebians_api/tmp/papers --owner nebians
    python manage.py import_past_papers /home/consicac/nebians_api/tmp/papers --owner nebians --dry-run
    python manage.py import_past_papers /home/consicac/nebians_api/tmp/papers --owner nebians --only 12-phy-2082-general
    python manage.py import_past_papers /home/consicac/nebians_api/tmp/papers --owner nebians --refresh-metadata

The folder holds listing.json, <slug>.pdf and <slug>.jpg. A paper that already exists (same title and
type) keeps its id, view and download counts; --refresh-metadata also rewrites its listing text.
Files are stored under deterministic names (papers/<slug>.pdf), so a re-run replaces rather than
duplicates. Resources are created approved and attributed to --owner.
"""
import json
import os
import time
import uuid

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand, CommandError

from api.models import Resource, User

SITE = 'https://nebians.consica.com.np'
PDF_DIR = 'papers'
COVER_DIR = 'resource_thumbnails'

LISTING_FIELDS = ('title', 'description', 'subject', 'grade_level', 'year', 'exam_type', 'type',
                  'faculty', 'program', 'author_name', 'source_label', 'tags')


def store(path, name):
    with open(path, 'rb') as fh:
        return default_storage.save(name, ContentFile(fh.read()))


class Command(BaseCommand):
    help = "Create or refresh the past paper resources from a staged folder of PDFs, covers and listing.json."

    def add_arguments(self, parser):
        parser.add_argument('directory', help='folder with listing.json, <slug>.pdf and <slug>.jpg')
        parser.add_argument('--owner', default='nebians', help='username that owns the resources')
        parser.add_argument('--only', nargs='*', default=[], help='only these slugs')
        parser.add_argument('--dry-run', action='store_true')
        parser.add_argument('--refresh-metadata', action='store_true',
                            help='rewrite the listing text of papers that already exist')
        parser.add_argument('--limit', type=int, default=0)

    def handle(self, *args, **opts):
        directory = opts['directory']
        listing_path = os.path.join(directory, 'listing.json')
        if not os.path.exists(listing_path):
            raise CommandError('no listing.json in %s' % directory)
        with open(listing_path, encoding='utf-8') as fh:
            listing = json.load(fh)
        if opts['only']:
            listing = [x for x in listing if x['slug'] in opts['only']]
        if opts['limit']:
            listing = listing[:opts['limit']]
        try:
            owner = User.objects.get(username=opts['owner'])
        except User.DoesNotExist:
            raise CommandError('no such account: %s' % opts['owner'])

        now = int(time.time() * 1000)
        created = updated = unchanged = failed = 0
        for item in listing:
            slug = item['slug']
            pdf = os.path.join(directory, slug + '.pdf')
            jpg = os.path.join(directory, slug + '.jpg')
            if not os.path.exists(pdf):
                self.stderr.write('%s: PDF missing' % slug)
                failed += 1
                continue
            existing = Resource.objects.filter(file__endswith='%s/%s.pdf' % (PDF_DIR, slug)).first()
            if not existing:
                existing = Resource.objects.filter(title=item['title'], type=item['type']).first()

            if existing and not opts['refresh_metadata']:
                stored = existing.file.name if existing.file else ''
                size = os.path.getsize(pdf)
                if stored == '%s/%s.pdf' % (PDF_DIR, slug) and existing.file_size == size:
                    unchanged += 1
                    continue
            if opts['dry_run']:
                self.stdout.write('%s  %s' % ('refresh' if existing else 'create', item['title']))
                created += 1
                continue

            pdf_name = store(pdf, '%s/%s.pdf' % (PDF_DIR, slug))
            cover_name = store(jpg, '%s/paper_%s.jpg' % (COVER_DIR, slug)) if os.path.exists(jpg) else ''

            record = existing or Resource(id=str(uuid.uuid4()))
            record.file = pdf_name
            record.file_url = ''
            record.file_size = os.path.getsize(pdf)
            if cover_name:
                record.thumbnail_url = '%s/media/%s' % (SITE, cover_name)
            for field in LISTING_FIELDS:
                if item.get(field) is not None:
                    setattr(record, field, item[field])
            record.source_type = 'admin'
            record.approval_status = 'approved'
            record.rejection_reason = ''
            record.reviewed_at = now
            if not record.added_at:
                record.added_at = now
            if not record.uploaded_by_id:
                record.uploaded_by = owner
            record.save()

            if existing:
                updated += 1
                self.stdout.write('refreshed  %s' % item['title'])
            else:
                created += 1
                self.stdout.write('created    %s' % item['title'])

        self.stdout.write('\n%d created, %d refreshed, %d already current, %d failed'
                          % (created, updated, unchanged, failed))
