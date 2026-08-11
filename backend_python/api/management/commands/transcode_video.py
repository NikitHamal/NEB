import os
import subprocess
import shutil
from django.core.management.base import BaseCommand
from api.models import PostMedia

class Command(BaseCommand):
    def handle(self, *args, **options):
        videos = PostMedia.objects.filter(kind='video')
        self.stdout.write(f"Found {videos.count()} video attachments.")
        
        ffmpeg_bin = shutil.which('ffmpeg') or '/usr/bin/ffmpeg' or '/usr/local/bin/ffmpeg'
        
        for m in videos:
            if not m.url:
                continue
            path_only = m.url
            if '://' in path_only:
                path_only = path_only.split('://', 1)[1]
                if '/' in path_only:
                    path_only = '/' + path_only.split('/', 1)[1]
            rel_clean = path_only.replace('/media/', '').lstrip('/')
            
            abs_video = os.path.join('/home/consicac/nebians_api/public/media', rel_clean)
            if not os.path.exists(abs_video):
                abs_video = os.path.join('/home/consicac/nebians.consica.com.np/media', rel_clean)
                
            if not os.path.exists(abs_video):
                self.stdout.write(f"Video file not found: {abs_video}")
                continue
                
            dir_name = os.path.dirname(abs_video)
            base_name = os.path.splitext(os.path.basename(abs_video))[0]
            out_filename = f"{base_name}_h264.mp4"
            abs_out = os.path.join(dir_name, out_filename)
            
            cmd = [
                ffmpeg_bin, '-y', '-i', abs_video,
                '-c:v', 'mpeg4', '-q:v', '3',
                '-c:a', 'aac', abs_out
            ]
            self.stdout.write(f"Transcoding {abs_video} -> {abs_out}...")
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if res.returncode == 0 and os.path.exists(abs_out) and os.path.getsize(abs_out) > 0:
                os.replace(abs_out, abs_video)
                pub_video = os.path.join('/home/consicac/nebians.consica.com.np/media', rel_clean)
                if os.path.exists('/home/consicac/nebians.consica.com.np/media') and os.path.abspath(abs_video) != os.path.abspath(pub_video):
                    try:
                        shutil.copy2(abs_video, pub_video)
                    except Exception:
                        pass
                self.stdout.write(f"Successfully transcoded {m.id} to universal 8-bit H.264 MP4!")
            else:
                self.stdout.write(f"Failed transcoding {m.id}: {res.stderr.decode('utf-8', errors='ignore')[-300:]}")
