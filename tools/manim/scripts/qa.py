#!/usr/bin/env python3
"""Quality checks on a finished episode MP4.

    tools/manim/scripts/qa.py path/to/episode.mp4 [--frames 12]

Reports what a reviewer would otherwise check by hand: the container and codec,
the real duration against the beat log, the audio level, and a contact sheet of
frames spread through the episode so the picture can be eyeballed in one image.
Exits non-zero if anything is actually wrong.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PIPELINE = os.path.dirname(HERE)


def ffmpeg() -> str:
    try:
        import imageio_ffmpeg

        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:  # pragma: no cover
        return "ffmpeg"


def probe(path: str) -> dict:
    out = subprocess.run(
        [ffmpeg(), "-hide_banner", "-i", path], capture_output=True, text=True
    ).stderr
    info: dict = {"raw": out}
    for line in out.splitlines():
        line = line.strip()
        if line.startswith("Duration:"):
            info["duration"] = line.split("Duration:")[1].split(",")[0].strip()
        if "Video:" in line:
            for token in line.split(","):
                token = token.strip()
                if "x" in token and token[0].isdigit():
                    info["resolution"] = token
                if token.endswith("fps"):
                    info["fps"] = token
            for codec in ("h264", "hevc", "vp9"):
                if codec in line:
                    info["video_codec"] = codec
        if "Audio:" in line:
            for codec in ("aac", "mp3", "opus"):
                if codec in line:
                    info["audio_codec"] = codec
    return info


def loudness(path: str) -> str:
    out = subprocess.run(
        [
            ffmpeg(),
            "-hide_banner",
            "-nostats",
            "-i",
            path,
            "-af",
            "loudnorm=print_format=summary",
            "-f",
            "null",
            "-",
        ],
        capture_output=True,
        text=True,
    ).stderr
    keep = {}
    for line in out.splitlines():
        if ":" in line and line.split(":")[0].strip() in (
            "Input Integrated",
            "Input True Peak",
            "Input LRA",
        ):
            keep[line.split(":")[0].strip()] = line.split(":")[1].strip()
    return ", ".join("%s %s" % item for item in sorted(keep.items())) or "unknown"


def _seconds(stamp: str) -> float:
    parts = [float(p) for p in stamp.split(":")]
    while len(parts) < 3:
        parts.insert(0, 0.0)
    return parts[0] * 3600 + parts[1] * 60 + parts[2]


def info_duration(path: str) -> str:
    return probe(path).get("duration", "0:00:00")


def contact_sheet(path: str, out: str, count: int) -> None:
    """Pull ``count`` frames spread through the file and tile them."""

    from PIL import Image, ImageDraw

    workdir = os.path.join(os.path.dirname(os.path.abspath(out)), "qa")
    os.makedirs(workdir, exist_ok=True)
    seconds = _seconds(info_duration(path))
    step = max(1, int(seconds / max(1, count)))
    subprocess.run(
        [ffmpeg(), "-y", "-loglevel", "error", "-i", path, "-vf", "fps=1/%d" % step, "%s/q%%03d.png" % workdir],
        check=True,
    )
    files = sorted(
        os.path.join(workdir, f) for f in os.listdir(workdir) if f.endswith(".png")
    )[:count]
    cols = 3
    rows = (len(files) + cols - 1) // cols
    w, h = 640, 360
    sheet = Image.new("RGB", (cols * w, rows * h), (18, 18, 22))
    draw = ImageDraw.Draw(sheet)
    for i, f in enumerate(files):
        sheet.paste(Image.open(f).resize((w, h)), ((i % cols) * w, (i // cols) * h))
        draw.text(((i % cols) * w + 8, (i // cols) * h + 6), os.path.basename(f), fill=(255, 200, 60))
    sheet.save(out)


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__.strip())
        return 2
    path = argv[1]
    count = 12
    if "--frames" in argv:
        count = int(argv[argv.index("--frames") + 1])

    info = probe(path)
    problems = []
    print("file            %s" % path)
    print("size            %.2f MB" % (os.path.getsize(path) / 1e6))
    print("duration        %s" % info.get("duration", "?"))
    print("resolution      %s" % info.get("resolution", "?"))
    print("frame rate      %s" % info.get("fps", "?"))
    print("video codec     %s" % info.get("video_codec", "?"))
    print("audio codec     %s" % info.get("audio_codec", "?"))
    print("loudness        %s" % loudness(path))

    if info.get("resolution") != "1920x1080":
        problems.append("resolution is %s, expected 1920x1080" % info.get("resolution"))
    if not info.get("audio_codec"):
        problems.append("no audio stream")
    if "nan" in info.get("duration", "nan") or "N/A" in info.get("duration", "N/A"):
        problems.append("no duration -- the file may be truncated")

    beats_path = os.path.join(PIPELINE, "build", "beats.json")
    if os.path.exists(beats_path):
        with open(beats_path, encoding="utf-8") as handle:
            beats = json.load(handle)
        print("beat log        %d beats, last at %.1f s" % (len(beats), max(beats.values())))
        seconds = _seconds(info["duration"])
        if seconds < max(beats.values()):
            problems.append("the video ends before the last beat does")

    sheet = os.path.join(os.path.dirname(os.path.abspath(path)), "qa-sheet.png")
    contact_sheet(path, sheet, count)
    print("contact sheet   %s" % sheet)

    if problems:
        print("\nFAILED:")
        for problem in problems:
            print("  - %s" % problem)
        return 1
    print("\nOK")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
