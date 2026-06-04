"""Management command to find and manage duplicate resources.

Scans resources for duplicates:
1. File duplicates (identical size and SHA-256 content hash).
2. URL duplicates (identical external file_url).

Supports dry-run, marking duplicates as rejected, or deleting duplicate records.
"""
import hashlib
from collections import defaultdict
from django.core.management.base import BaseCommand
from django.core.files.storage import default_storage
from api.models import Resource


class Command(BaseCommand):
    help = 'Identify and clean up duplicate resource uploads.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--status',
            type=str,
            default='all',
            choices=['all', 'pending', 'approved', 'rejected'],
            help='Filter scanned resources by approval status.'
        )
        parser.add_argument(
            '--reject-duplicates',
            action='store_true',
            help='Mark duplicates as rejected with a duplicate reason.'
        )
        parser.add_argument(
            '--delete-records',
            action='store_true',
            help='Completely delete duplicate database records and delete their associated files.'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Report duplicates but do not modify the database or files.'
        )

    def get_file_hash(self, file_field):
        try:
            hasher = hashlib.sha256()
            # Open file and read in chunks
            with file_field.open('rb') as f:
                for chunk in iter(lambda: f.read(65536), b''):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error reading file {file_field.name}: {str(e)}"))
            return None

    def handle(self, *args, **options):
        status = options['status']
        reject_dups = options['reject_duplicates']
        delete_records = options['delete_records']
        dry_run = options['dry_run']

        if reject_dups and delete_records:
            self.stderr.write(self.style.ERROR("Error: Cannot specify both --reject-duplicates and --delete-records."))
            return

        prefix = '[DRY RUN] ' if dry_run else ''

        # 1. Gather all resources with physical files
        resources_with_files = Resource.objects.filter(file__isnull=False).exclude(file='')
        if status != 'all':
            resources_with_files = resources_with_files.filter(approval_status=status)

        self.stdout.write(f"Scanning {resources_with_files.count()} file-based resources for duplicates...")

        # Group by size to optimize hashing
        size_groups = defaultdict(list)
        for r in resources_with_files:
            size_groups[r.file_size].append(r)

        # Hash files only in groups of size > 1
        hash_groups = defaultdict(list)
        for size, r_list in size_groups.items():
            if len(r_list) < 2:
                continue
            for r in r_list:
                file_hash = self.get_file_hash(r.file)
                if file_hash:
                    hash_groups[file_hash].append(r)

        # Identify duplicate file groups
        file_duplicates_count = 0
        for file_hash, r_list in hash_groups.items():
            if len(r_list) < 2:
                continue
            
            # Sort by added_at (oldest first) so the first uploaded is kept as the original
            r_list.sort(key=lambda x: x.added_at)
            original = r_list[0]
            duplicates = r_list[1:]
            file_duplicates_count += len(duplicates)

            self.stdout.write(self.style.WARNING(
                f"\nDuplicate group found (SHA-256: {file_hash[:12]}..., Size: {original.file_size} bytes):"
            ))
            self.stdout.write(self.style.SUCCESS(
                f"  [ORIGINAL] ID: {original.id} | Title: '{original.title}' | Status: {original.approval_status} | Uploaded: {original.added_at}"
            ))

            for dup in duplicates:
                self.stdout.write(
                    f"  [DUPLICATE] ID: {dup.id} | Title: '{dup.title}' | Status: {dup.approval_status} | Uploaded: {dup.added_at}"
                )

                if dry_run:
                    continue

                if reject_dups:
                    if dup.approval_status != 'rejected':
                        dup.approval_status = 'rejected'
                        dup.rejection_reason = 'Duplicate upload of existing resource.'
                        dup.save()
                        self.stdout.write(self.style.SUCCESS(f"    -> Marked resource {dup.id} as rejected."))
                    else:
                        self.stdout.write(f"    -> Resource {dup.id} is already rejected.")
                
                elif delete_records:
                    self.stdout.write(self.style.ERROR(f"    -> Deleting duplicate resource record {dup.id}..."))
                    dup_file_path = dup.file.name
                    dup.delete()
                    # Also remove the file from storage
                    try:
                        if default_storage.exists(dup_file_path):
                            default_storage.delete(dup_file_path)
                            self.stdout.write(self.style.SUCCESS(f"    -> Deleted duplicate file: {dup_file_path}"))
                    except Exception as e:
                        self.stderr.write(self.style.ERROR(f"    -> Error deleting file {dup_file_path}: {str(e)}"))

        # 2. Gather and scan resources with URLs (in case there are duplicate external link resources)
        resources_with_urls = Resource.objects.filter(file__isnull=True) | Resource.objects.filter(file='')
        if status != 'all':
            resources_with_urls = resources_with_urls.filter(approval_status=status)

        self.stdout.write(f"\nScanning {resources_with_urls.count()} URL-based resources for duplicates...")

        url_groups = defaultdict(list)
        for r in resources_with_urls:
            if r.file_url:
                url_groups[r.file_url].append(r)

        url_duplicates_count = 0
        for url, r_list in url_groups.items():
            if len(r_list) < 2:
                continue

            r_list.sort(key=lambda x: x.added_at)
            original = r_list[0]
            duplicates = r_list[1:]
            url_duplicates_count += len(duplicates)

            self.stdout.write(self.style.WARNING(
                f"\nDuplicate URL group found (URL: {url[:60]}...):"
            ))
            self.stdout.write(self.style.SUCCESS(
                f"  [ORIGINAL] ID: {original.id} | Title: '{original.title}' | Status: {original.approval_status} | Uploaded: {original.added_at}"
            ))

            for dup in duplicates:
                self.stdout.write(
                    f"  [DUPLICATE] ID: {dup.id} | Title: '{dup.title}' | Status: {dup.approval_status} | Uploaded: {dup.added_at}"
                )

                if dry_run:
                    continue

                if reject_dups:
                    if dup.approval_status != 'rejected':
                        dup.approval_status = 'rejected'
                        dup.rejection_reason = 'Duplicate upload of existing resource URL.'
                        dup.save()
                        self.stdout.write(self.style.SUCCESS(f"    -> Marked resource {dup.id} as rejected."))
                
                elif delete_records:
                    self.stdout.write(self.style.ERROR(f"    -> Deleting duplicate resource record {dup.id}..."))
                    dup.delete()

        # Summary
        self.stdout.write("\n" + "=" * 40)
        self.stdout.write(self.style.SUCCESS(
            f"{prefix}Scan complete. Found {file_duplicates_count} file duplicates and {url_duplicates_count} URL duplicates."
        ))
        if dry_run:
            self.stdout.write(self.style.WARNING("Dry run completed. No database or file modifications were made."))
