"""Management command to (re)compress existing uploaded resource files.

Applies lossy compression to images (JPEG q=85, PNG/BMP/GIF → WebP q=88)
and lossless compression to PDFs. Files that can't be made smaller are
left untouched. The original file is replaced in-place; only the storage
path changes when the extension changes (e.g. PNG → WebP).

Usage:
    # Preview what would change without touching any files:
    python manage.py compress_existing_resources --dry-run

    # Compress every resource file:
    python manage.py compress_existing_resources

    # Compress only PDFs:
    python manage.py compress_existing_resources --types pdf

    # Compress only images:
    python manage.py compress_existing_resources --types image

    # Limit to the first 50 resources (useful for testing):
    python manage.py compress_existing_resources --limit 50
"""
import os
from io import BytesIO

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand

from api.models import Resource
from api.compression import (
    compress_resource_file,
    IMAGE_EXTENSIONS,
    PDF_EXTENSION,
)


class Command(BaseCommand):
    help = (
        "Lossy-compress image files and lossless-compress PDFs for all "
        "existing resources that have a locally stored file."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help="Show what would change without modifying any files or DB records.",
        )
        parser.add_argument(
            '--types',
            choices=['all', 'image', 'pdf'],
            default='all',
            help="Which file types to compress (default: all).",
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=None,
            help="Process at most this many resources (useful for testing).",
        )

    def handle(self, *args, **options):
        dry_run  = options['dry_run']
        file_types = options['types']
        limit    = options['limit']
        prefix   = '[DRY RUN] ' if dry_run else ''

        # Fetch resources that have a locally stored file
        qs = Resource.objects.exclude(file='').exclude(file=None)
        if limit:
            qs = qs[:limit]

        total = qs.count()
        self.stdout.write(f"{prefix}Found {total} resources with stored files. Starting compression…\n")

        total_original  = 0
        total_compressed = 0
        skipped         = 0
        errors          = 0
        changed         = 0

        for resource in qs:
            file_field = resource.file
            if not file_field:
                continue

            storage_path = str(file_field)
            _, dot_ext   = os.path.splitext(storage_path)
            ext          = dot_ext.lower()

            # Filter by requested type
            if file_types == 'image' and ext not in IMAGE_EXTENSIONS:
                skipped += 1
                continue
            if file_types == 'pdf' and ext != PDF_EXTENSION:
                skipped += 1
                continue
            if ext not in IMAGE_EXTENSIONS and ext != PDF_EXTENSION:
                skipped += 1
                continue

            # Read original bytes from storage
            try:
                with default_storage.open(storage_path, 'rb') as fh:
                    original_data = fh.read()
            except Exception as exc:
                self.stdout.write(
                    self.style.ERROR(f"  ERROR reading {storage_path}: {exc}")
                )
                errors += 1
                continue

            original_size = len(original_data)
            total_original += original_size

            # Determine lossless flag: PDFs are always lossless; images use lossy
            lossless = (ext == PDF_EXTENSION)

            # Run compression
            try:
                result = compress_resource_file(
                    BytesIO(original_data), ext, lossless=lossless
                )
            except Exception as exc:
                self.stdout.write(
                    self.style.ERROR(f"  ERROR compressing {storage_path}: {exc}")
                )
                errors += 1
                total_compressed += original_size
                continue

            if result is None:
                # No improvement possible
                self.stdout.write(f"  SKIP  {storage_path} — no reduction possible")
                skipped += 1
                total_compressed += original_size
                continue

            content_file, new_ext = result
            compressed_data = content_file.read()
            compressed_size = len(compressed_data)

            savings_bytes = original_size - compressed_size
            savings_pct   = (savings_bytes / original_size * 100) if original_size else 0
            total_compressed += compressed_size

            # Build new storage path (may change if ext changed, e.g. PNG → WebP)
            if new_ext != ext:
                base_path = os.path.splitext(storage_path)[0]
                new_storage_path = base_path + new_ext
            else:
                new_storage_path = storage_path

            self.stdout.write(
                f"  {'WOULD COMPRESS' if dry_run else 'COMPRESS'} "
                f"{storage_path} → {new_storage_path}  "
                f"{original_size:,} → {compressed_size:,} bytes "
                f"({savings_pct:.1f}% saved)"
            )

            if not dry_run:
                try:
                    # Write compressed file to new path
                    if default_storage.exists(new_storage_path) and new_storage_path != storage_path:
                        default_storage.delete(new_storage_path)
                    default_storage.save(new_storage_path, ContentFile(compressed_data))

                    # Delete old file only if path changed
                    if new_storage_path != storage_path:
                        try:
                            default_storage.delete(storage_path)
                        except Exception:
                            pass  # Old file gone already — not critical

                    # Update DB record
                    resource.file      = new_storage_path
                    resource.file_size = compressed_size
                    resource.save(update_fields=['file', 'file_size'])
                    changed += 1

                except Exception as exc:
                    self.stdout.write(
                        self.style.ERROR(f"    ERROR saving {new_storage_path}: {exc}")
                    )
                    errors += 1
                    continue
            else:
                changed += 1  # Count as "would change" in dry-run

        # Summary
        saved_mb = (total_original - total_compressed) / (1024 * 1024)
        orig_mb  = total_original / (1024 * 1024)
        comp_mb  = total_compressed / (1024 * 1024)

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(
            f"{prefix}Done. "
            f"{'Would compress' if dry_run else 'Compressed'}: {changed}  |  "
            f"Skipped: {skipped}  |  Errors: {errors}"
        ))
        self.stdout.write(self.style.SUCCESS(
            f"{prefix}Storage: {orig_mb:.2f} MB → {comp_mb:.2f} MB  "
            f"({'would save' if dry_run else 'saved'} {saved_mb:.2f} MB)"
        ))
