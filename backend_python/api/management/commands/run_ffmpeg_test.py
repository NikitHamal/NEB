import subprocess
import os
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        inp = "/home/consicac/nebians_api/public/media/forum_media/videos/forum_-x3bSGRzWdkTJk9-.mp4"
        out = "/home/consicac/nebians_api/public/media/forum_media/videos/test_h264.mp4"
        
        cmds = [
            # Test 1: Level 5.1 H.264 with scale 720:1280
            ["ffmpeg", "-y", "-i", inp, "-vf", "scale=720:1280,format=yuv420p", "-c:v", "libx264", "-profile:v", "high", "-level", "5.1", "-preset", "fast", "-crf", "23", "-c:a", "aac", out],
            # Test 2: Level 5.1 H.264 full resolution
            ["ffmpeg", "-y", "-i", inp, "-c:v", "libx264", "-profile:v", "high", "-level", "5.1", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "23", "-c:a", "aac", out],
            # Test 3: Main profile level 4.2 scaled
            ["ffmpeg", "-y", "-i", inp, "-vf", "scale=540:960,format=yuv420p", "-c:v", "libx264", "-profile:v", "main", "-level", "4.2", "-preset", "fast", "-crf", "23", "-c:a", "aac", out],
        ]
        
        for idx, cmd in enumerate(cmds, 1):
            self.stdout.write(f"\n--- TRYING TEST {idx} ---")
            self.stdout.write(" ".join(cmd))
            r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            self.stdout.write(f"Return code: {r.returncode}")
            if r.returncode == 0:
                self.stdout.write(f"SUCCESS! Output size: {os.path.getsize(out)} bytes")
                # Replace original file with the transcoded H264 MP4
                os.replace(out, inp)
                pub = "/home/consicac/nebians.consica.com.np/media/forum_media/videos/forum_-x3bSGRzWdkTJk9-.mp4"
                if os.path.exists(pub):
                    import shutil
                    try: shutil.copy2(inp, pub)
                    except Exception: pass
                self.stdout.write(f"Replaced video file with working H264 MP4!")
                break
            else:
                self.stdout.write(f"STDERR: {r.stderr[-800:]}")
