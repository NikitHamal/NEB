import io
import os
import time
import uuid
import zipfile
from collections import defaultdict
from urllib.parse import urlparse

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand

from api.models import Resource


class Command(BaseCommand):
    help = 'Groups and merges duplicate pending resource uploads into a single PDF or ZIP archive.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Scan and report what would be merged, without modifying files or database.'
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

        mergeable_groups = [g for g in groups if len(g) > 1]
        
        if not mergeable_groups:
            self.stdout.write(self.style.SUCCESS("No duplicate pending groups identified for merging."))
            return

        self.stdout.write(f"Found {len(mergeable_groups)} duplicate group(s) to merge.")

        for idx, group in enumerate(mergeable_groups, 1):
            lead = group[0]
            base_title = self.get_base_title(lead.title)
            self.stdout.write(f"\n--- Group {idx}: '{base_title}' ({len(group)} files) ---")
            
            saved_files = []
            for r in group:
                if r.file:
                    self.stdout.write(f" - {r.title} ({r.file.name}, size: {r.file_size} bytes)")
                    saved_files.append({
                        'path': r.file.name,
                        'size': r.file_size,
                        'name': os.path.basename(r.file.name)
                    })
                else:
                    self.stdout.write(f" - {r.title} (No local file, URL: {r.file_url})")

            if not saved_files:
                self.stdout.write(self.style.WARNING("No physical files in this group. Skipping merging."))
                continue

            if len(saved_files) != len(group):
                self.stdout.write(self.style.WARNING("Some resources are missing files. Skipping merging to avoid loss."))
                continue

            # Determine if we can merge to PDF
            can_merge_pdf = True
            for sf in saved_files:
                ext = os.path.splitext(sf['name'])[1].lower()
                if ext not in ('.pdf', '.png', '.jpg', '.jpeg', '.webp', '.gif', '.bmp', '.tiff'):
                    can_merge_pdf = False
                    break

            merged_data = None
            merged_ext = None

            if can_merge_pdf:
                self.stdout.write("Merging files into a single PDF document...")
                try:
                    from pypdf import PdfMerger
                    from PIL import Image
                    
                    merger = PdfMerger()
                    opened_files = []
                    try:
                        for sf in saved_files:
                            ext = os.path.splitext(sf['name'])[1].lower()
                            if ext == '.pdf':
                                f_obj = default_storage.open(sf['path'], 'rb')
                                opened_files.append(f_obj)
                                merger.append(f_obj)
                            else:
                                with default_storage.open(sf['path'], 'rb') as f:
                                    img_data = f.read()
                                img = Image.open(io.BytesIO(img_data))
                                img = img.convert('RGB')
                                pdf_io = io.BytesIO()
                                img.save(pdf_io, 'PDF')
                                pdf_io.seek(0)
                                opened_files.append(pdf_io)
                                merger.append(pdf_io)
                        
                        out_stream = io.BytesIO()
                        merger.write(out_stream)
                        merger.close()
                        merged_data = out_stream.getvalue()
                        merged_ext = '.pdf'
                    finally:
                        for f_obj in opened_files:
                            try:
                                f_obj.close()
                            except Exception:
                                pass
                except Exception as e:
                    self.stderr.write(self.style.ERROR(f"Failed to merge to PDF: {e}"))
                    merged_data = None

            if not merged_data:
                self.stdout.write("Falling back to zipping files...")
                try:
                    zip_buffer = io.BytesIO()
                    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                        for sf in saved_files:
                            with default_storage.open(sf['path'], 'rb') as f:
                                content = f.read()
                            zip_file.writestr(sf['name'], content)
                    merged_data = zip_buffer.getvalue()
                    merged_ext = '.zip'
                except Exception as e:
                    self.stderr.write(self.style.ERROR(f"Failed to create fallback ZIP archive: {e}"))

            if merged_data and merged_ext:
                if dry_run:
                    self.stdout.write(self.style.SUCCESS(f"{prefix}Would merge {len(group)} files into a single {merged_ext[1:].upper()} and delete {len(group)-1} database duplicate records."))
                else:
                    merged_filename = f"{uuid.uuid4().hex[:12]}_{int(time.time())}{merged_ext}"
                    merged_path_relative = os.path.join('resources', merged_filename)
                    final_path = default_storage.save(merged_path_relative, ContentFile(merged_data))
                    final_size = len(merged_data)

                    # Reconstruct URL
                    old_url = lead.file_url
                    if old_url and (old_url.startswith('http://') or old_url.startswith('https://')):
                        parsed = urlparse(old_url)
                        domain_prefix = f"{parsed.scheme}://{parsed.netloc}"
                        lead.file_url = domain_prefix + settings.MEDIA_URL + final_path
                    else:
                        lead.file_url = settings.MEDIA_URL + final_path

                    # Update lead resource
                    lead.title = base_title
                    lead.file = final_path
                    lead.file_size = final_size
                    if merged_ext == '.zip' and lead.type == 'PDF':
                        lead.type = 'Note'
                    lead.save()

                    # Delete duplicate records
                    for other in group[1:]:
                        other.delete()

                    # Clean up old individual files from storage
                    for sf in saved_files:
                        if sf['path']:
                            try:
                                default_storage.delete(sf['path'])
                            except Exception:
                                pass

                    self.stdout.write(self.style.SUCCESS(f"Successfully consolidated group into '{base_title}'!"))
            else:
                self.stderr.write(self.style.ERROR("Could not merge this group."))
