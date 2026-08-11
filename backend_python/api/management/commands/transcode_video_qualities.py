from django.core.management.base import BaseCommand
from api.models import PostMedia
from api.security import auto_transcode_video_qualities, auto_transcode_video_to_h264

class Command(BaseCommand):
    help = 'Transcodes all video attachments into multi-resolution variants (720p, 480p, 360p)'

    def handle(self, *args, **options):
        videos = PostMedia.objects.filter(kind='video')
        self.stdout.write(f"Found {videos.count()} video attachments.")
        for v in videos:
            self.stdout.write(f"Processing video {v.id}: {v.url} ...")
            auto_transcode_video_to_h264(v.url)
            quals = auto_transcode_video_qualities(v.url)
            self.stdout.write(self.style.SUCCESS(f"  Done! Qualities generated: {[q['label'] for q in quals]}"))
