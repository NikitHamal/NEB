"""Shrink oversized profile photos (they were stored exactly as uploaded, 1 to 1.4 MB each).

For every local ``/media/profile_photos/`` file that is a full-size original, write a small
WebP next to it (``<name>_o.webp``, long side at most 640 px, EXIF-upright) and point
``users.photo_url`` and ``user_photos.url`` at it. Originals are NEVER deleted or edited, so a
cached feed, an old app build or a rollback keeps working. A row changes only when the new
file is at least 15% smaller. Safe to run again: optimized files are skipped.

    python manage.py optimize_profile_photos --dry-run
    python manage.py optimize_profile_photos --limit 25
"""
import os
from io import BytesIO

from django.conf import settings
from django.core.management.base import BaseCommand
from PIL import Image

from api.models import User, UserPhoto
from api.security import AVATAR_MAX_EDGE, optimize_avatar_image

MARKER = '/media/profile_photos/'
SKIP_BELOW_BYTES = 60 * 1024


class Command(BaseCommand):
    help = 'Write small WebP copies of oversized profile photos and repoint the database at them.'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true')
        parser.add_argument('--limit', type=int, default=0, help='Optimize at most N photos (0 = all).')

    def handle(self, *args, **options):
        dry = options['dry_run']
        limit = options['limit'] or 0
        root = os.path.join(str(settings.MEDIA_ROOT), 'profile_photos')

        urls = set(User.objects.filter(photo_url__contains=MARKER).values_list('photo_url', flat=True))
        urls |= set(UserPhoto.objects.filter(url__contains=MARKER).values_list('url', flat=True))

        done = skipped = failed = 0
        saved = 0
        for url in sorted(urls):
            if limit and done >= limit:
                break
            prefix, _, name = url.partition(MARKER)
            name = name.split('?')[0]
            if not name or '/' in name or name.endswith('_o.webp'):
                skipped += 1
                continue
            src = os.path.join(root, name)
            if not os.path.isfile(src):
                skipped += 1
                continue
            old_size = os.path.getsize(src)
            try:
                with Image.open(src) as im:
                    small_enough = max(im.size) <= AVATAR_MAX_EDGE and old_size < SKIP_BELOW_BYTES
                    if small_enough:
                        skipped += 1
                        continue
                    im.load()
                    out = BytesIO()
                    optimize_avatar_image(im).save(out, format='WEBP', quality=85, method=4)
            except Exception as exc:  # unreadable file: leave the row alone
                failed += 1
                self.stderr.write(f'skip {name}: {type(exc).__name__}')
                continue
            data = out.getvalue()
            if len(data) > old_size * 0.85:
                skipped += 1
                continue
            new_name = os.path.splitext(name)[0] + '_o.webp'
            new_url = prefix + MARKER + new_name
            if dry:
                self.stdout.write(f'would shrink {name}: {old_size // 1024} KB -> {len(data) // 1024} KB')
                done += 1
                saved += old_size - len(data)
                continue
            dest = os.path.join(root, new_name)
            if not os.path.isfile(dest):
                tmp = dest + '.tmp'
                with open(tmp, 'wb') as fh:
                    fh.write(data)
                os.replace(tmp, dest)
            User.objects.filter(photo_url=url).update(photo_url=new_url)
            UserPhoto.objects.filter(url=url).update(url=new_url)
            done += 1
            saved += old_size - len(data)
        self.stdout.write(
            f'photos: {"would shrink" if dry else "shrunk"} {done}, skipped {skipped}, '
            f'failed {failed}, saves {saved // 1024} KB per full load of all avatars')
