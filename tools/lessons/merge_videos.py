"""Rebuild every lesson video from the parts in videos/ into one file each — run this on your own computer.

    python3 tools/lessons/merge_videos.py [--out merged] [--only BOOK] [--check]

Reads videos/index.json. For each lesson it joins the parts listed there with ffmpeg's concat demuxer and
stream copy (no re-encoding, so nothing is lost and it takes seconds), merges the .srt files with the right
time offsets, and writes OUT/class-GG/BOOK/unit_NN.mp4 (+ .srt). A lesson stored as one part is simply copied.
--check compares each merged file's duration with the index and reports any mismatch. Needs ffmpeg/ffprobe."""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
VID = os.path.join(ROOT, "videos")


def probe(path):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", path],
                                capture_output=True, text=True).stdout.strip())


def ts_in(s):
    h, m, rest = s.strip().split(":")
    sec, ms = rest.split(",")
    return int(h) * 3600 + int(m) * 60 + int(sec) + int(ms) / 1000


def ts_out(x):
    h, r = divmod(max(0.0, x), 3600)
    m, s = divmod(r, 60)
    ms = int(round((s - int(s)) * 1000))
    if ms == 1000:
        s, ms = int(s) + 1, 0
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{ms:03d}"


def merge_srt(parts, dst):
    cues = []
    for p in parts:
        path = os.path.join(VID, p["subtitles"])
        if not os.path.exists(path):
            continue
        for blk in re.split(r"\n\s*\n", open(path, encoding="utf-8").read().strip()):
            lines = blk.strip().splitlines()
            if len(lines) < 2 or "-->" not in lines[1]:
                continue
            a, z = lines[1].split("-->")
            cue = [ts_in(a) + p["start"], ts_in(z) + p["start"], "\n".join(lines[2:])]
            if cues and cues[-1][2] == cue[2] and abs(cues[-1][1] - cue[0]) < 0.2:
                cues[-1][1] = cue[1]  # a cue cut in two at a part boundary
            else:
                cues.append(cue)
    with open(dst, "w", encoding="utf-8") as f:
        for n, (a, z, t) in enumerate(cues, 1):
            f.write(f"{n}\n{ts_out(a)} --> {ts_out(z)}\n{t}\n\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(VID, "merged"))
    ap.add_argument("--only", help="book code, e.g. eng12")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    idx = json.load(open(os.path.join(VID, "index.json"), encoding="utf-8"))
    bad = 0
    for v in idx["videos"]:
        if a.only and v["book"] != a.only:
            continue
        parts = v.get("parts") or [{"file": v["file"], "subtitles": v.get("subtitles", v["file"][:-4] + ".srt"), "start": 0.0, "end": v["seconds"]}]
        missing = [p["file"] for p in parts if not os.path.exists(os.path.join(VID, p["file"]))]
        if missing:
            print("skip (missing parts):", v.get("id", v["file"]), missing)
            continue
        dst = os.path.join(a.out, v.get("id") or re.sub(r"\.part\d+\.mp4$", ".mp4", v["file"]))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if len(parts) == 1:
            shutil.copy(os.path.join(VID, parts[0]["file"]), dst)
        else:
            with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as lst:
                for p in parts:
                    lst.write("file '" + os.path.join(VID, p["file"]).replace("'", "'\\''") + "'\n")
            subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst.name, "-map", "0", "-c", "copy",
                            "-movflags", "+faststart", dst], check=True)
            os.unlink(lst.name)
        merge_srt(parts, dst[:-4] + ".srt")
        d = probe(dst)
        ok = abs(d - v["seconds"]) < 1.0
        bad += not ok
        print(("ok  " if ok else "BAD ") + f"{os.path.relpath(dst, a.out)}  {len(parts)} part(s)  {d:.1f}s (index {v['seconds']}s)")
    if a.check and bad:
        sys.exit(f"{bad} file(s) differ in duration from the index")


if __name__ == "__main__":
    main()
