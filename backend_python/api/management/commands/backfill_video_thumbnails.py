"""Backfill cover thumbnails for already-uploaded video resources.

Walks every stored video file (mp4/mkv/webm/mov/avi/wmv/flv/3gp/m4v, or
type='Video') that has no ``thumbnail_url`` and extracts a frame with
ffmpeg (~1s in, falling back to the first frame). Resources that already
have a cover — uploaded, pasted, or previously extracted — are skipped.

Requires ffmpeg in PATH; runs purely best-effort per file and never
deletes or modifies the video itself.

Usage:
    # Preview which videos would get a cover:
    python manage.py backfill_video_thumbnails --dry-run

    # Backfill everything:
    python manage.py backfill_video_thumbnails

    # Only the first 25 hits (testing):
    python manage.py backfill_video_thumbnails --limit 25
"""
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Q

from api.models import Resource
from api.security import (
    VIDEO_EXTENSIONS,
    extract_video_thumbnail_frame,
    is_video_file_path,
)


class Command(BaseCommand):
    help = 'Extract cover thumbnails for video resources that lack one (ffmpeg).'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true',
                            help='Show what would be extracted without writing anything.')
        parser.add_argument('--limit', type=int, default=0,
                            help='Process at most N resources (0 = no limit).')

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        limit = options['limit'] or 0

        video_ext_filter = Q()
        for ext in sorted(VIDEO_EXTENSIONS):
            video_ext_filter |= Q(file__iendswith=ext)

        qs = (Resource.objects
              .filter(Q(thumbnail_url__isnull=True) | Q(thumbnail_url=''))
              .filter(video_ext_filter | Q(type__iexact='video'))
              .filter(file__gt='')
              .order_by('-added_at'))

        base = getattr(settings, 'SITE_URL', 'https://nebians.consica.com.np').rstrip('/')
        scanned = processed = skipped = failed = 0
        for resource in qs.iterator(chunk_size=100):
            file_path = str(resource.file or '')
            if not is_video_file_path(file_path):
                skipped += 1
                continue
            if limit and processed >= limit:
                break
            scanned += 1
            if dry_run:
                self.stdout.write(f"  [dry-run] {resource.id} {file_path}")
                processed += 1
                continue
            thumb_rel = extract_video_thumbnail_frame(file_path)
            if not thumb_rel:
                failed += 1
                self.stdout.write(self.style.WARNING(
                    f"  could not extract: {resource.id} {file_path}"))
                continue
            resource.thumbnail_url = base + settings.MEDIA_URL + thumb_rel
            resource.save(update_fields=['thumbnail_url'])
            processed += 1
            self.stdout.write(f"  ok: {resource.id} -> {thumb_rel}")

        # Process forum video attachments (PostMedia)
        from api.models import PostMedia
        from api.security import generate_video_thumbnail
        forum_qs = PostMedia.objects.filter(kind='video').filter(Q(thumbnail_url__isnull=True) | Q(thumbnail_url=''))
        self.stdout.write(f"Found {forum_qs.count()} forum video attachments needing thumbnails.")
        for pm in forum_qs:
            if limit and processed >= limit:
                break
            if dry_run:
                self.stdout.write(f"  [dry-run forum] {pm.id} {pm.url}")
                processed += 1
                continue
            thumb_rel = generate_video_thumbnail(pm.url)
            if not thumb_rel:
                failed += 1
                self.stdout.write(self.style.WARNING(f"  could not extract forum video: {pm.id} {pm.url}"))
                continue
            pm.thumbnail_url = thumb_rel if thumb_rel.startswith('http') else (base + thumb_rel)
            pm.save(update_fields=['thumbnail_url'])
            processed += 1
            self.stdout.write(f"  ok forum: {pm.id} -> {pm.thumbnail_url}")

        summary = (f"done: {processed} thumbnailed, {failed} failed, "
                   f"{skipped} non-video-file rows skipped")
        if dry_run:
            summary = f"[dry-run] {summary}"
        self.stdout.write(self.style.SUCCESS(summary))
