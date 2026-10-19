"""Render one lesson script into a finished video.

    python3 tools/lessons/build.py tools/lessons/scripts/phy12/unit_01.py [--draft]

Steps: manim renders picture + narration + sound effects; a synthesised music bed is
ducked under the voice; loudness is normalised; the subtitle track is muxed in; the
master, its .srt, a poster and an index entry land in videos/."""
import argparse
import json
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(ROOT, "videos")
WORK = os.path.join(HERE, ".work")
sys.path.insert(0, HERE)

from kit import sfx  # noqa: E402

GRADE_DIR = {8: "class-08", 10: "class-10", 11: "class-11", 12: "class-12"}


def run(cmd, **kw):
    print("+", " ".join(cmd[:6]), "...", flush=True)
    subprocess.run(cmd, check=True, **kw)


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", path],
                         capture_output=True, text=True).stdout.strip()
    return float(out)


def build(script, draft=False, scene="Lesson", preview=False):
    name = os.path.splitext(os.path.basename(script))[0]
    book = os.path.basename(os.path.dirname(script))
    tag = f"{book}-{name}"
    os.makedirs(WORK, exist_ok=True)
    mode0 = "preview" if preview else ("draft" if draft else "final")
    srt = os.path.join(WORK, f"{tag}-{mode0}.srt")
    meta = os.path.join(WORK, f"{tag}-{mode0}.json")
    env = dict(os.environ, LESSON_SRT=srt, LESSON_META=meta, PYTHONPATH=HERE + os.pathsep + os.environ.get("PYTHONPATH", ""))
    draft = draft or preview
    res = "854,480" if preview else ("1280,720" if draft else "1920,1080")
    fps = "15" if preview else ("24" if draft else "30")
    mode = "preview" if preview else ("draft" if draft else "final")
    media = os.path.join(WORK, "media", f"{tag}-{mode}")
    t0 = time.time()
    from prefetch import prefetch
    n, d = prefetch(script)
    print(f"narration: {n} lines, {d / 60:.1f} min", flush=True)
    run(["manim", "render", "--disable_caching", "-r", res, "--fps", fps, "--media_dir", media,
         "-o", tag, "--progress_bar", "none", "-v", "WARNING", script, scene], env=env, cwd=HERE)
    raw = None
    for dp, _, fs in os.walk(os.path.join(media, "videos")):
        for f in fs:
            if f == tag + ".mp4":
                raw = os.path.join(dp, f)
    m = json.load(open(meta, encoding="utf-8"))
    dur = probe(raw)
    bed = os.path.join(WORK, f"{tag}-{mode}-bed.wav")
    sfx.write_wav(bed, sfx.music_bed(dur, seed=m["unit"] * 7 + m["grade"], mood=m.get("mood", "calm")))
    dest_dir = os.path.join(WORK, "drafts") if draft else os.path.join(OUT, GRADE_DIR[m["grade"]], book)
    os.makedirs(dest_dir, exist_ok=True)
    final = os.path.join(dest_dir, (f"{tag}-{mode}" if draft else name) + ".mp4")
    lang = "nep" if m["lang"] == "ne" else "eng"
    fc = ("[1:a]volume=0.55[bed];[0:a]asplit=2[v1][v2];"
          "[bed][v2]sidechaincompress=threshold=0.02:ratio=8:attack=40:release=600[duck];"
          "[v1][duck]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11[a]")
    crf = "30" if draft else "31"
    run(["ffmpeg", "-y", "-v", "error", "-i", raw, "-i", bed, "-i", srt, "-filter_complex", fc,
         "-map", "0:v", "-map", "[a]", "-map", "2:s",
         "-c:v", "libx264", "-preset", ("medium" if draft else "slow"), "-crf", crf, "-tune", "animation", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", ("128k" if draft else "96k"), "-ar", "48000", "-c:s", "mov_text",
         "-metadata:s:s:0", f"language={lang}", "-metadata:s:a:0", f"language={lang}",
         "-metadata", f"title={m['title']}", "-movflags", "+faststart", final])
    if not draft:
        import shutil
        shutil.copy(srt, os.path.join(dest_dir, name + ".srt"))
        poster = os.path.join(dest_dir, name + ".jpg")
        run(["ffmpeg", "-y", "-v", "error", "-ss", "6", "-i", final, "-frames:v", "1", "-q:v", "4", "-vf", "scale=960:-2", poster])
        index_path = os.path.join(OUT, "index.json")
        idx = json.load(open(index_path, encoding="utf-8")) if os.path.exists(index_path) else {"videos": []}
        rel = os.path.relpath(final, OUT)
        idx["videos"] = [v for v in idx["videos"] if v["file"] != rel]
        idx["videos"].append({
            "file": rel, "subtitles": rel[:-4] + ".srt", "poster": rel[:-4] + ".jpg",
            "book": book, "grade": m["grade"], "unit": m["unit"], "title": m["title"], "subtitle": m.get("subtitle", ""),
            "lang": m["lang"], "sections": m["sections"], "seconds": round(probe(final), 1),
            "script": os.path.relpath(os.path.abspath(script), ROOT),
        })
        idx["videos"].sort(key=lambda v: (-v["grade"], v["book"], v["unit"]))
        json.dump(idx, open(index_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    size = os.path.getsize(final) / 1e6
    print(f"done {final}  {probe(final):.0f}s  {size:.1f} MB  in {time.time() - t0:.0f}s", flush=True)
    return final


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("scripts", nargs="+")
    ap.add_argument("--draft", action="store_true", help="720p24 into .work/drafts")
    ap.add_argument("--preview", action="store_true", help="480p15 into .work/drafts, the cheapest check")
    a = ap.parse_args()
    for s in a.scripts:
        build(os.path.abspath(s), a.draft, preview=a.preview)
