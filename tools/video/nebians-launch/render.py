"""Render the Neby film: python3 render.py out.mp4 [--draft]

Frames are drawn with Skia, motion-blurred by averaging sub-frame samples across a
180-degree shutter, piped to ffmpeg as raw RGB and muxed with the synthesised score
(loudness-normalised to -14 LUFS)."""
import os
import subprocess
import sys
import tempfile
import time

import numpy as np
import skia

import film
import score
from kit import H, W


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "neby-launch.mp4"
    draft = "--draft" in sys.argv
    fps = 30 if draft else film.FPS
    samples = 1 if draft else 3
    shutter = 0.5 / fps
    nframes = int(round(film.DURATION * fps))

    wav = os.path.join(tempfile.gettempdir(), "neby-score.wav")
    score.write(wav)

    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-",
           "-i", wav,
           "-map", "0:v", "-map", "1:a",
           "-c:v", "libx264", "-preset", "veryfast" if draft else "slow", "-crf", "23" if draft else "16",
           "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
           "-af", "loudnorm=I=-14:TP=-1.0:LRA=11",
           "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
           "-movflags", "+faststart", "-shortest", out]
    enc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    surf = skia.Surface(W, H)
    canvas = surf.getCanvas()
    acc = np.zeros((H, W, 3), np.float32)
    t0 = time.time()
    for i in range(nframes):
        t = i / fps
        if samples == 1:
            film.frame(canvas, t)
            img = surf.makeImageSnapshot().toarray(colorType=skia.kRGBA_8888_ColorType)[:, :, :3]
        else:
            acc[:] = 0
            for j in range(samples):
                ts = t + (j / (samples - 1) - 0.5) * shutter
                film.frame(canvas, max(0.0, min(film.DURATION - 1e-3, ts)))
                acc += surf.makeImageSnapshot().toarray(colorType=skia.kRGBA_8888_ColorType)[:, :, :3]
            img = (acc / samples + 0.5).astype(np.uint8)
        enc.stdin.write(np.ascontiguousarray(img).tobytes())
        if i % 120 == 0:
            el = time.time() - t0
            print(f"frame {i}/{nframes}  {el:.0f}s", flush=True)
    enc.stdin.close()
    enc.wait()
    print("done", out, f"{time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
