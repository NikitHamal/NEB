from django.core.management.base import BaseCommand
from api.models import PostMedia
from web.view_helpers import _serialize_post

class Command(BaseCommand):
    def handle(self, *args, **options):
        pm = PostMedia.objects.get(id="ad9aa6ad-442a-4a1f-af04-1269236613fa")
        self.stdout.write(f"PostMedia thumbnail_url in DB: '{pm.thumbnail_url}'")
        self.stdout.write(f"PostMedia post_id: '{pm.post_id}'")
        if pm.post:
            data = _serialize_post(pm.post)
            self.stdout.write(f"Serialized post attachments: {data.get('attachments')}")
