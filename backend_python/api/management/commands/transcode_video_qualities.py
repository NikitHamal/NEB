import os
from django.core.management.base import BaseCommand
from api.models import PostMedia
from api.security import auto_transcode_video_qualities, auto_transcode_video_to_h264

class Command(BaseCommand):
    help = 'Transcodes all video attachments into H.264 multi-resolution variants (720p, 480p, 360p)'

    def handle(self, *args, **options):
        videos = PostMedia.objects.filter(kind='video')
        self.stdout.write(f"Found {videos.count()} video attachments.")
        for v in videos:
            self.stdout.write(f"Processing video {v.id}: {v.url} ...")
            base_path = v.url.split('?')[0]
            if '://' in base_path:
                base_path = '/' + base_path.split('://', 1)[1].split('/', 1)[1]
            base_clean = base_path.replace('/media/', '').lstrip('/')
            
            for p_dir in ['/home/consicac/nebians_api/public/media', '/home/consicac/nebians.consica.com.np/media']:
                target = os.path.join(p_dir, base_clean)
                dir_n, base_n = os.path.dirname(target), os.path.splitext(os.path.basename(target))[0]
                for suffix in ['_360p.mp4', '_480p.mp4', '_720p.mp4', '_test_360p.mp4', '_test_360p_small.mp4']:
                    f_old = os.path.join(dir_n, base_n + suffix)
                    if os.path.exists(f_old):
                        try:
                            os.remove(f_old)
                        except Exception:
                            pass

            auto_transcode_video_to_h264(v.url)
            quals = auto_transcode_video_qualities(v.url)
            self.stdout.write(self.style.SUCCESS(f"  Done! H.264 qualities generated: {[q['label'] for q in quals]}"))
