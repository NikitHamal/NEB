"""Place built lesson videos into videos/ for pushing, splitting any that are too big for one GitHub blob.

    python3 tools/lessons/publish.py STAGE_DIR BOOK UNIT [UNIT ...]

STAGE_DIR/BOOK/unit_NN.{mp4,srt,jpg,meta.json} are the files build.py wrote. A video up to LIMIT_MB is
copied as videos/class-GG/BOOK/unit_NN.mp4; a bigger one is cut, without re-encoding, at keyframes near
chapter starts into unit_NN.part1.mp4, unit_NN.part2.mp4 … with matching .srt files. Every part is a
playable video. videos/index.json gets one entry per unit listing its parts with exact start/end times,
so tools/lessons/merge_videos.py can rebuild the single file losslessly. Prints the repo paths written."""
import json
import math
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(ROOT, "videos")
GRADE_DIR = {8: "class-08", 10: "class-10", 11: "class-11", 12: "class-12"}
LIMIT_MB = float(os.environ.get("PUBLISH_LIMIT_MB", 24.0))
TARGET_MB = float(os.environ.get("PUBLISH_TARGET_MB", 20.0))


def probe(path):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", path],
                                capture_output=True, text=True).stdout.strip())


def keyframes(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-skip_frame", "nokey", "-show_entries", "frame=pts_time",
                          "-of", "csv=p=0", path], capture_output=True, text=True).stdout.split()
    return sorted(float(x.strip(",")) for x in out if x.strip(", "))


def srt_cues(path):
    blocks = re.split(r"\n\s*\n", open(path, encoding="utf-8").read().strip())
    cues = []
    for b in blocks:
        lines = b.strip().splitlines()
        if len(lines) < 2 or "-->" not in lines[1]:
            continue
        a, z = [t.strip() for t in lines[1].split("-->")]
        cues.append((ts_in(a), ts_in(z), "\n".join(lines[2:])))
    return cues


def ts_in(s):
    h, m, rest = s.split(":")
    sec, ms = rest.split(",")
    return int(h) * 3600 + int(m) * 60 + int(sec) + int(ms) / 1000


def ts_out(x):
    x = max(0.0, x)
    h, r = divmod(x, 3600)
    m, s = divmod(r, 60)
    ms = int(round((s - int(s)) * 1000))
    if ms == 1000:
        s, ms = int(s) + 1, 0
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{ms:03d}"


def write_srt(path, cues, start, end):
    n = 0
    with open(path, "w", encoding="utf-8") as f:
        for a, z, t in cues:
            if z <= start or a >= end:
                continue
            n += 1
            f.write(f"{n}\n{ts_out(max(a, start) - start)} --> {ts_out(min(z, end) - start)}\n{t}\n\n")


def cut_points(dur, mb, chapters, keys):
    n = max(1, math.ceil(mb / TARGET_MB))
    if n == 1:
        return []
    starts = [c[0] for c in chapters if 0 < c[0] < dur]
    cuts = []
    for k in range(1, n):
        ideal = dur * k / n
        near = min(starts, key=lambda t: abs(t - ideal)) if starts else ideal
        if abs(near - ideal) > dur / (2 * n):
            near = ideal
        kf = min((t for t in keys if t > 0), key=lambda t: abs(t - near))
        if kf not in cuts and 0 < kf < dur:
            cuts.append(kf)
    return sorted(cuts)


def publish(stage, book, unit):
    name = f"unit_{int(unit):02d}"
    src = os.path.join(stage, book)
    mp4, srt, jpg = (os.path.join(src, name + e) for e in (".mp4", ".srt", ".jpg"))
    meta = json.load(open(os.path.join(src, name + ".meta.json"), encoding="utf-8"))
    rel_dir = os.path.join(GRADE_DIR[meta["grade"]], book)
    dest = os.path.join(OUT, rel_dir)
    os.makedirs(dest, exist_ok=True)
    for f in os.listdir(dest):
        if re.fullmatch(rf"{name}(\.part\d+)?\.(mp4|srt)", f):
            os.remove(os.path.join(dest, f))
    dur = probe(mp4)
    mb = os.path.getsize(mp4) / 1e6
    chapters = meta.get("chapters") or [[0.0, "Introduction"]]
    written = []
    parts = []
    if mb <= LIMIT_MB:
        shutil.copy(mp4, os.path.join(dest, name + ".mp4"))
        write_srt(os.path.join(dest, name + ".srt"), srt_cues(srt), 0.0, dur + 1)
        parts.append({"file": f"{rel_dir}/{name}.mp4", "subtitles": f"{rel_dir}/{name}.srt", "start": 0.0, "end": round(dur, 2), "mb": round(mb, 1)})
    else:
        cuts = cut_points(dur, mb, chapters, keyframes(mp4))
        tmp = os.path.join(dest, f".{name}.seg%d.mp4")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", mp4, "-map", "0", "-c", "copy", "-f", "segment", "-segment_format", "mp4",
                        "-segment_times", ",".join(f"{c:.3f}" for c in cuts), "-reset_timestamps", "1", "-movflags", "+faststart", tmp], check=True)
        cues = srt_cues(srt)
        bounds = [0.0] + cuts + [dur]
        k = 0
        while os.path.exists(tmp % k):
            pf = os.path.join(dest, f"{name}.part{k + 1}.mp4")
            os.replace(tmp % k, pf)
            t0, t1 = bounds[k], bounds[k + 1]
            write_srt(os.path.join(dest, f"{name}.part{k + 1}.srt"), cues, t0, t1)
            parts.append({"file": f"{rel_dir}/{name}.part{k + 1}.mp4", "subtitles": f"{rel_dir}/{name}.part{k + 1}.srt",
                          "start": round(t0, 3), "end": round(t1, 3), "mb": round(os.path.getsize(pf) / 1e6, 1)})
            k += 1
        assert k == len(bounds) - 1, f"expected {len(bounds) - 1} parts, got {k}"
    shutil.copy(jpg, os.path.join(dest, name + ".jpg"))
    for p in parts:
        written += [os.path.join("videos", p["file"]), os.path.join("videos", p["subtitles"])]
    written.append(os.path.join("videos", rel_dir, name + ".jpg"))
    index_path = os.path.join(OUT, "index.json")
    idx = json.load(open(index_path, encoding="utf-8")) if os.path.exists(index_path) else {"videos": []}
    vid = f"{rel_dir}/{name}.mp4"
    idx["videos"] = [v for v in idx["videos"] if v.get("id", v.get("file")) != vid]
    idx["videos"].append({
        "id": vid, "file": parts[0]["file"], "parts": parts, "poster": f"{rel_dir}/{name}.jpg",
        "book": book, "grade": meta["grade"], "unit": meta["unit"], "title": meta["title"], "subtitle": meta.get("subtitle", ""),
        "lang": meta["lang"], "sections": meta["sections"], "seconds": round(dur, 1), "chapters": chapters, "mb": round(mb, 1),
        "script": f"tools/lessons/scripts/{book}/{name}.py",
    })
    idx["videos"].sort(key=lambda v: (-v["grade"], v["book"], v["unit"]))
    json.dump(idx, open(index_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    written.append("videos/index.json")
    return written, dur, mb, len(parts), meta


if __name__ == "__main__":
    stage, book = sys.argv[1], sys.argv[2]
    for u in sys.argv[3:]:
        files, dur, mb, n, meta = publish(stage, book, u)
        print(json.dumps({"unit": int(u), "title": meta["title"], "minutes": round(dur / 60, 1), "mb": round(mb, 1), "parts": n, "files": files}, ensure_ascii=False))
