"""Approve the pending library uploads of one account (used after tools/publish/publish_books.py).

    python manage.py approve_book_uploads <username>            # list what would be approved
    python manage.py approve_book_uploads <username> --yes      # approve them
    python manage.py approve_book_uploads <username> --yes --label NEBians
"""
import time

from django.core.cache import cache
from django.core.management.base import BaseCommand, CommandError

from api.models import Resource


class Command(BaseCommand):
    help = "Approve pending resources uploaded by one account (optionally only one source label)."

    def add_arguments(self, parser):
        parser.add_argument("username")
        parser.add_argument("--label", default="", help="only resources with this source_label")
        parser.add_argument("--yes", action="store_true", help="approve; without it only list")

    def handle(self, *args, username, label, yes, **opts):
        qs = Resource.objects.filter(approval_status="pending", uploaded_by__username=username)
        if label:
            qs = qs.filter(source_label=label)
        items = list(qs.order_by("added_at"))
        if not items:
            raise CommandError(f"No pending uploads from '{username}'.")
        for r in items:
            self.stdout.write(f"{'approve' if yes else 'pending'}  {r.id}  {r.title}")
        if not yes:
            self.stdout.write(f"\n{len(items)} pending. Run again with --yes to approve.")
            return
        now = int(time.time() * 1000)
        qs.update(approval_status="approved", reviewed_at=now, rejection_reason="")
        cache.delete_many(["home_resources", "library_all_resources"])
        self.stdout.write(self.style.SUCCESS(f"{len(items)} approved."))
