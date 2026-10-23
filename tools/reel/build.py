#!/usr/bin/env python3
"""One command for the whole reel: cue sheet, score, frames, encode, poster and contact sheet.

    python tools/reel/build.py --name nebians-v1.7-reel            # full 1080x1920 60 fps master
    python tools/reel/build.py --name draft --scale 0.5 --no-blur   # fast 540x960 draft

Outputs land in tools/reel/out/<name>/ (frames are deleted after encoding unless --keep-frames).
"""
import argparse, json, os, shutil, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))


def run(cmd, **kw):
    t0 = time.time()
    print("$", " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True, **kw)
    return time.time() - t0


def status():
    d = os.environ.get("NEB_REEL_STATUS_DIR", "/marimo/neb-reel")
    if not os.path.exists(os.path.join(d, "status.py")):
        return None
    sys.path.insert(0, d)
    import status as st
    return st


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", default="nebians-v1.7-reel")
    ap.add_argument("--out", default=os.path.join(HERE, "out"))
    ap.add_argument("--scale", type=float, default=1.0)
    ap.add_argument("--workers", type=int, default=min(16, (os.cpu_count() or 4) - 2))
    ap.add_argument("--no-blur", dest="blur", action="store_false")
    ap.add_argument("--crf", type=int, default=16)
    ap.add_argument("--keep-frames", action="store_true")
    a = ap.parse_args()
    st = status()
    out = os.path.join(a.out, a.name)
    frames = os.path.join(out, "frames")
    shutil.rmtree(frames, ignore_errors=True)
    os.makedirs(frames, exist_ok=True)
    cues = os.path.join(out, "cues.json")
    wav = os.path.join(out, "audio.wav")
    mp4 = os.path.join(out, f"{a.name}.mp4")

    if st: st.phase("audio", "active")
    run([sys.executable, os.path.join(HERE, "render", "render.py"), "--dump-cues", cues])
    dt = run([sys.executable, os.path.join(HERE, "audio", "audio.py"), "--cues", cues, "--out", wav])
    if st:
        st.phase("audio", "done")
        st.log(f"Score + {len(json.load(open(cues))['cues'])} SFX synthesized in {dt:.0f}s, mastered to -14 LUFS")
        st.phase("render", "active")

    cmd = [sys.executable, os.path.join(HERE, "render", "render.py"), "--out", frames, "--scale", str(a.scale),
           "--workers", str(a.workers)]
    if not a.blur:
        cmd.append("--no-blur")
    dt = run(cmd)
    n = len([f for f in os.listdir(frames) if f.endswith(".jpg")])
    if st:
        st.phase("render", "done")
        st.log(f"{n} frames rendered in {dt:.0f}s ({n / dt:.1f} fps across {a.workers} Chromium workers)")
        st.phase("encode", "active")

    vf = "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p"
    dt = run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-framerate", "60", "-i", os.path.join(frames, "f_%05d.jpg"),
              "-i", wav, "-vf", vf, "-c:v", "libx264", "-preset", "slow", "-crf", str(a.crf), "-profile:v", "high",
              "-x264-params", "aq-mode=3:aq-strength=0.9", "-colorspace", "bt709", "-color_primaries", "bt709",
              "-color_trc", "bt709", "-color_range", "tv", "-c:a", "aac", "-b:a", "256k", "-ar", "48000",
              "-movflags", "+faststart", "-shortest", mp4])
    run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-ss", "28.5", "-i", mp4, "-frames:v", "1",
         "-q:v", "2", os.path.join(out, "poster.jpg")])
    run([sys.executable, os.path.join(HERE, "render", "sheet.py"), frames, os.path.join(out, "contact.jpg"),
         "--cols", "16", "--width", "135", "--step", "15"])
    size = os.path.getsize(mp4) / 1e6
    if st:
        st.phase("encode", "done")
        st.log(f"Encoded {a.name}.mp4: {size:.1f} MB, H.264 + AAC, encode {dt:.0f}s")
        st.stat(**{"Last video": f"{size:.1f} MB"})
    if not a.keep_frames:
        shutil.rmtree(frames, ignore_errors=True)
    print(f"done -> {mp4} ({size:.1f} MB)")


if __name__ == "__main__":
    main()
