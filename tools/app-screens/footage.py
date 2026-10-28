#!/usr/bin/env python3
"""Turn the app-captures artifact (Maestro recordings + screenshots) into stage footage.

    python tools/app-screens/footage.py --zip run-a.zip --zip run-b.zip --out ../Video/neb/tools/reel/captures/app
    python tools/app-screens/footage.py --url <signed artifact URL> [--url ...] --out <same>

With several artifacts, later ones win clip by clip, but only when their recording decodes: a flow
that crashed mid-recording leaves an MP4 without an index, and the earlier take is kept.

Writes <out>/<clip>/%05d.jpg at 30 fps and 1080 px wide, stills as JPEG, and footage.js, the
manifest the reel stage reads: {clips: {clip: {n, fps, w, h, dur}}, stills: [...]}. Point --out at
the reel's captures/app in the Videos repo; the default is app-footage/ beside this script.
"""
import argparse, io, json, os, shutil, subprocess, urllib.request, zipfile
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
DEST = os.path.abspath(os.path.join(HERE, "app-footage"))
WIDTH = 1080
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
                    "-q:v", "2", os.path.join(d, "%05d.jpg")], check=True)
    n = len([f for f in os.listdir(d) if f.endswith(".jpg")])
    p = probe(src)
    s = (p.get("streams") or [{}])[0]
    h = round(WIDTH * int(s.get("height", 2400)) / int(s.get("width", 1080)))
    return name, {"n": n, "fps": FPS, "w": WIDTH, "h": h, "dur": float((p.get("format") or {}).get("duration", n / FPS))}


def still(src, name):
    d = os.path.join(DEST, "stills")
    os.makedirs(d, exist_ok=True)
    out = os.path.join(d, name + ".jpg")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vf", f"scale={WIDTH}:-2:flags=lanczos", "-q:v", "2", out], check=True)
    return name


def decodes(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                       capture_output=True, text=True)
    return r.returncode == 0 and r.stdout.strip() not in ("", "N/A")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--zip", action="append", default=[])
    ap.add_argument("--url", action="append", default=[])
    ap.add_argument("--out", default=DEST)
    a = ap.parse_args()
    global DEST
    DEST = os.path.abspath(a.out)
    raw = os.path.join(DEST, "raw")
    shutil.rmtree(raw, ignore_errors=True)
    os.makedirs(raw)
    sources = [open(z, "rb").read() for z in a.zip] + [urllib.request.urlopen(u, timeout=300).read() for u in a.url]
    vids, pics = {}, {}
    for k, data in enumerate(sources):
        d = os.path.join(raw, f"take{k}")
        zipfile.ZipFile(io.BytesIO(data)).extractall(d)
        for root, _, files in os.walk(d):
            for f in files:
                p = os.path.join(root, f)
                name = os.path.splitext(f)[0]
                if f.endswith(".mp4") and decodes(p):
                    vids[name.replace("rec-", "")] = p
                elif f.endswith(".png") and not name.startswith(("debug-", "end-", "login-")):
                    pics[name] = p
    with ThreadPoolExecutor(8) as ex:
        clips = dict(ex.map(lambda kv: clip(kv[1], kv[0]), vids.items()))
        stills = sorted(ex.map(lambda kv: still(kv[1], kv[0]), pics.items()))
    manifest = {"clips": clips, "stills": stills}
    with open(os.path.join(DEST, "footage.js"), "w") as fh:
        fh.write("window.FOOTAGE = " + json.dumps(manifest, indent=1) + ";\n")
    print(f"{len(clips)} clips, {len(stills)} stills from {len(sources)} capture runs -> {DEST}")
    for k, v in sorted(clips.items()):
        print(f"  {k:16} {v['n']:5} frames  {v['dur']:.1f}s  {v['w']}x{v['h']}")


if __name__ == "__main__":
    main()
