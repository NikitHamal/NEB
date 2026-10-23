#!/usr/bin/env python3
"""Turn the app-captures artifact (Maestro recordings + screenshots) into stage footage.

    python tools/reel/capture/app/footage.py --zip app-captures.zip
    python tools/reel/capture/app/footage.py --url <signed artifact URL>

Writes tools/reel/captures/app/<clip>/%05d.jpg at 30 fps and 720 px wide (the phone screen is
568 px in the frame, so this keeps a little headroom for camera push-ins), stills as JPEG, and
footage.js, the manifest the stage reads: {clip: {n, fps, w, h}}.
"""
import argparse, io, json, os, shutil, subprocess, urllib.request, zipfile
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
DEST = os.path.abspath(os.path.join(HERE, "..", "..", "captures", "app"))
WIDTH = 720
FPS = 30


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=width,height,avg_frame_rate,nb_frames:format=duration", "-of", "json", path],
                         capture_output=True, text=True).stdout
    return json.loads(out or "{}")


def clip(src, name):
    d = os.path.join(DEST, name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vf", f"fps={FPS},scale={WIDTH}:-2:flags=lanczos",
                    "-q:v", "3", os.path.join(d, "%05d.jpg")], check=True)
    n = len([f for f in os.listdir(d) if f.endswith(".jpg")])
    p = probe(src)
    s = (p.get("streams") or [{}])[0]
    h = round(WIDTH * int(s.get("height", 2400)) / int(s.get("width", 1080)))
    return name, {"n": n, "fps": FPS, "w": WIDTH, "h": h, "dur": float((p.get("format") or {}).get("duration", n / FPS))}


def still(src, name):
    d = os.path.join(DEST, "stills")
    os.makedirs(d, exist_ok=True)
    out = os.path.join(d, name + ".jpg")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vf", f"scale={WIDTH * 1.5:.0f}:-2:flags=lanczos", "-q:v", "2", out], check=True)
    return name


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--zip")
    ap.add_argument("--url")
    a = ap.parse_args()
    raw = os.path.join(DEST, "raw")
    shutil.rmtree(raw, ignore_errors=True)
    os.makedirs(raw)
    data = open(a.zip, "rb").read() if a.zip else urllib.request.urlopen(a.url, timeout=300).read()
    zipfile.ZipFile(io.BytesIO(data)).extractall(raw)
    vids, pics = [], []
    for root, _, files in os.walk(raw):
        for f in files:
            p = os.path.join(root, f)
            if f.endswith(".mp4"):
                vids.append((p, os.path.splitext(f)[0].replace("rec-", "")))
            elif f.endswith(".png"):
                pics.append((p, os.path.splitext(f)[0]))
    with ThreadPoolExecutor(8) as ex:
        clips = dict(ex.map(lambda v: clip(*v), vids))
        stills = sorted(ex.map(lambda v: still(*v), pics))
    manifest = {"clips": clips, "stills": stills}
    with open(os.path.join(DEST, "footage.js"), "w") as fh:
        fh.write("window.FOOTAGE = " + json.dumps(manifest, indent=1) + ";\n")
    print(f"{len(clips)} clips, {len(stills)} stills -> {DEST}")
    for k, v in sorted(clips.items()):
        print(f"  {k:16} {v['n']:5} frames  {v['dur']:.1f}s  {v['w']}x{v['h']}")


if __name__ == "__main__":
    main()
