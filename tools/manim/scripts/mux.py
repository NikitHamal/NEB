#!/usr/bin/env python3
"""Mux the narration into a rendered episode.

The voice-over is recorded one group at a time (see ``make_narration.py``), so
each MP3 has to be dropped at the exact scene time where its first beat begins.
That time comes from ``layout.py beats``, which replays the scene and records a
clock, so the audio lines up with the picture without anybody eyeballing it.

    tools/manim/scripts/mux.py \\
        tools/manim/build/videos/phy11_unit01/1080p30/PhysicalQuantities.mp4 \\
        tools/manim/audio \\
        tools/manim/build/videos/phy11_unit01/1080p30/PhysicalQuantities-narrated.mp4

The result is a normal H.264/AAC MP4, loudness-normalised so every episode of
the series lands at the same level.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PIPELINE = os.path.dirname(HERE)

sys.path.insert(0, PIPELINE)

from make_narration import GROUPS  # noqa: E402


def ffmpeg() -> str:
    try:
        import imageio_ffmpeg

        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:  # pragma: no cover
        return "ffmpeg"


def duration(path: str) -> float:
    out = subprocess.run(
        [ffmpeg(), "-hide_banner", "-i", path, "-f", "null", "-"],
        capture_output=True,
        text=True,
    ).stderr
    for line in out.splitlines():
        if "Duration:" in line:
            h, m, sec = line.split("Duration:")[1].split(",")[0].strip().split(":")
            return int(h) * 3600 + int(m) * 60 + float(sec)
    raise RuntimeError("could not read the duration of %s" % path)


def build_audio(audio_dir: str, beats: dict, length: float, workdir: str) -> str:
    """Lay the group MP3s out on one track and normalise it."""

    parts = []
    for name, keys in GROUPS:
        path = os.path.join(audio_dir, "%s.mp3" % name)
        if not os.path.exists(path):
            raise SystemExit("missing narration group %s" % path)
        first = keys[0]
        if first not in beats:
            raise SystemExit("beat %s is not in the beat log" % first)
        offset = int(round(beats[first] * 1000))
        # all=1 delays every channel by the same amount, whatever the codec
        # handed us -- a bare adelay=900 is read as the boolean "all" here.
        parts.append("[%d:a]adelay=all=1:delays=%d[d%d]" % (len(parts), offset, len(parts)))

    labels = "".join("[d%d]" % i for i in range(len(parts)))
    mix = "%samix=inputs=%d:normalize=0:duration=longest[aout]" % (labels, len(parts))
    normalised = os.path.join(workdir, "narration.wav")
    command = (
        [ffmpeg(), "-y", "-hide_banner", "-loglevel", "error"]
        + sum([["-i", os.path.join(audio_dir, "%s.mp3" % name)] for name, _ in GROUPS], [])
        + [
            "-filter_complex",
            "%s;%s" % (";".join(parts), mix)
            + ";[aout]loudnorm=I=-16:TP=-1.5:LRA=11"
            + ",apad=whole_dur=%.3f,atrim=0:%.3f[final]" % (length, length),
            "-map",
            "[final]",
            "-ar",
            "48000",
            "-ac",
            "2",
            normalised,
        ]
    )
    subprocess.run(command, check=True)
    return normalised


def main(argv: list[str]) -> int:
    if len(argv) < 3:
        print(__doc__.strip())
        return 2
    video, audio_dir, out = argv[1], argv[2], argv[3]
    beats_path = argv[4] if len(argv) > 4 else os.path.join(
        PIPELINE, "build", "beats.json"
    )
    if not os.path.exists(beats_path):
        print("no beat log at %s -- run layout.py beats first" % beats_path)
        return 1
    with open(beats_path, encoding="utf-8") as handle:
        beats = json.load(handle)

    length = duration(video)
    workdir = os.path.join(os.path.dirname(os.path.abspath(out)), "muxwork")
    os.makedirs(workdir, exist_ok=True)
    audio = build_audio(audio_dir, beats, length, workdir)

    subprocess.run(
        [
            ffmpeg(),
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            video,
            "-i",
            audio,
            "-map",
            "0:v:0",
            "-map",
            "1:a:0",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "128k",
            "-movflags",
            "+faststart",
            "-shortest",
            out,
        ],
        check=True,
    )
    print("%s  %.1f s  %.2f MB" % (out, duration(out), os.path.getsize(out) / 1e6))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
