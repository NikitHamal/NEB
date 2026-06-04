import os
import uuid
from urllib.parse import urlparse

from django.core.management.base import BaseCommand
from api.models import Resource


class Command(BaseCommand):
    help = 'Groups duplicate pending resource uploads under a shared upload_group_id rather than merging files.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Scan and report what would be grouped, without modifying the database.'
        )

    def get_base_title(self, title):
        if ' - ' in title:
            return title.rsplit(' - ', 1)[0].strip()
        return title.strip()

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        prefix = '[DRY RUN] ' if dry_run else ''

        self.stdout.write("Fetching all pending resources...")
        pending_resources = list(Resource.objects.filter(approval_status='pending').order_by('added_at'))
        
        if not pending_resources:
            self.stdout.write(self.style.SUCCESS("No pending resources found in the database."))
            return

        self.stdout.write(f"Analyzing {len(pending_resources)} pending resources for duplicates...")

        # Cluster resources by same: uploaded_by_id, subject, grade_level, base_title, and within 5 minutes of each other
        groups = []
        for r in pending_resources:
            placed = False
            r_base = self.get_base_title(r.title)
            for group in groups:
                lead = group[0]
                lead_base = self.get_base_title(lead.title)
                if (lead.uploaded_by_id == r.uploaded_by_id and
                        lead.subject == r.subject and
                        lead.grade_level == r.grade_level and
                        lead_base.lower() == r_base.lower() and
                        abs(lead.added_at - r.added_at) <= 300000): # 5 minutes
                    group.append(r)
                    placed = True
                    break
            if not placed:
                groups.append([r])

        mergeable_groups = []
        for group in groups:
            if len(group) > 1:
                # Group if any member lacks an upload_group_id or is marked incorrectly
                if any(not r.upload_group_id for r in group):
                    mergeable_groups.append(group)

        if not mergeable_groups:
            self.stdout.write(self.style.SUCCESS("No ungrouped duplicate pending resources identified."))
            return

        self.stdout.write(f"Found {len(mergeable_groups)} duplicate group(s) to consolidate.")

        for idx, group in enumerate(mergeable_groups, 1):
            lead = group[0]
            base_title = self.get_base_title(lead.title)
            self.stdout.write(f"\n--- Group {idx}: '{base_title}' ({len(group)} files) ---")
            
            for r in group:
                self.stdout.write(f" - {r.title} (file: {r.file.name if r.file else 'None'}, size: {r.file_size} bytes)")

            if dry_run:
                self.stdout.write(self.style.SUCCESS(f"{prefix}Would group {len(group)} resources under a shared group ID."))
            else:
                group_id = str(uuid.uuid4())
                lead_title = group[0].title
                for sub_idx, r in enumerate(group):
                    r.upload_group_id = group_id
                    if sub_idx == 0:
                        r.is_lead = True
                    else:
                        r.is_lead = False
                        if r.title == lead_title:
                            display_name = ""
                            if r.file:
                                display_name = os.path.splitext(os.path.basename(r.file.name))[0]
                            elif r.file_url:
                                display_name = os.path.splitext(os.path.basename(urlparse(r.file_url).path))[0]
                            if display_name:
                                r.title = f"{lead_title} - {display_name}"
                    r.save()
                self.stdout.write(self.style.SUCCESS(f"Successfully grouped '{base_title}' with group_id {group_id}!"))
