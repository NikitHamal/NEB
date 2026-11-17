"""Write the small list copies (192 px avatars, 480 px covers) next to stored images.

Feeds, comments and cards ask ``api.image_variants.variant_url`` and get the small file when it
exists. Only files that rows point at are processed, newest first, inside a time budget, so a
deploy never waits on this. Originals are never changed or deleted. Safe to run again.

    python manage.py make_list_copies --dry-run
    python manage.py make_list_copies --seconds 60
"""
import os
import time

from django.conf import settings
from django.core.management.base import BaseCommand

from api.image_variants import AVATAR, COVER, variant_name, write_variant
from api.models import Resource, User, UserPhoto


class Command(BaseCommand):
    help = 'Write small list copies of avatars and resource covers (originals kept).'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true')
        parser.add_argument('--seconds', type=int, default=90, help='Stop after this many seconds.')
        parser.add_argument('--limit', type=int, default=0, help='Write at most N copies (0 = no cap).')

    def _names(self, urls, marker):
        out = []
        seen = set()
        for url in urls:
            if not url or marker not in url:
                continue
            name = url.partition(marker)[2].split('?')[0]
            if name and '/' not in name and name not in seen:
                seen.add(name)
                out.append(name)
        return out

    def handle(self, *args, **options):
        dry, limit = options['dry_run'], options['limit'] or 0
        deadline = time.monotonic() + max(5, options['seconds'])
        media = str(settings.MEDIA_ROOT)

        avatars = list(User.objects.filter(photo_url__contains=AVATAR[0]).values_list('photo_url', flat=True))
        avatars += list(UserPhoto.objects.filter(url__contains=AVATAR[0]).values_list('url', flat=True))
        covers = list(Resource.objects.filter(thumbnail_url__contains=COVER[0]).order_by('-added_at')
                      .values_list('thumbnail_url', flat=True))
        jobs = [(AVATAR, 'profile_photos', self._names(avatars, AVATAR[0])),
                (COVER, 'resource_thumbnails', self._names(covers, COVER[0]))]

        written = skipped = failed = saved = 0
        for kind, folder, names in jobs:
            root = os.path.join(media, folder)
            for name in names:
                if time.monotonic() > deadline or (limit and written >= limit):
                    break
                vname = variant_name(name, kind)
                if not vname or os.path.isfile(os.path.join(root, vname)):
                    skipped += 1
                    continue
                src = os.path.join(root, name)
                if not os.path.isfile(src):
                    skipped += 1
                    continue
                if dry:
                    written += 1
                    continue
                got = write_variant(src, kind, root)
                if got > 0:
                    written += 1
                    saved += got
                elif got < 0:
                    failed += 1
                else:
                    skipped += 1
        self.stdout.write(
            f'list copies: {"would write" if dry else "wrote"} {written}, skipped {skipped}, '
            f'failed {failed}, saves {saved // 1024} KB per full load')
