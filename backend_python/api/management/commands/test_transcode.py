import subprocess
import os
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        inp = "/home/consicac/nebians_api/public/media/forum_media/videos/forum_-x3bSGRzWdkTJk9-.mp4"
        out = "/home/consicac/nebians_api/public/media/forum_media/videos/forum_-x3bSGRzWdkTJk9-_h264.mp4"
        
        cmd = [
            'ffmpeg', '-y', '-i', inp,
            '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-preset', 'fast', '-crf', '23',
            '-c:a', 'aac', out
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.stdout.write(f"Return code: {res.returncode}")
        if res.returncode == 0:
            self.stdout.write(f"Success! Output size: {os.path.getsize(out)} bytes")
            os.replace(out, inp)
            self.stdout.write("Replaced original video file with transcoded H264 MP4!")
        else:
            self.stdout.write(f"Err: {res.stderr.decode('utf-8', errors='ignore')[-500:]}")
