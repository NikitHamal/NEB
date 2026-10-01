#!/usr/bin/env python3
"""Build one episode end to end: beat clock, picture, voice, and checks.

    tools/manim/scripts/build.py videos/phy11_unit01.py PhysicalQuantities

Runs the four stages in the order they have to happen:

1. ``layout.py beats`` replays the scene without rendering and writes the clock
   that says where each line of narration starts.
2. ``render.sh`` renders the picture with manim.
3. ``mux.py`` drops the recorded narration groups onto that clock and
   normalises the level.
4. ``qa.py`` checks the finished file and leaves a contact sheet.

Everything lands under ``tools/manim/build/``; ``--out`` copies the finished MP4
somewhere else, which is what puts it in front of a viewer.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PIPELINE = os.path.dirname(HERE)
BUILD = os.path.join(PIPELINE, "build")
BEATS = os.path.join(BUILD, "beats.json")


def run(command: list[str], **kwargs) -> None:
    print("+", " ".join(command))
    subprocess.run(command, check=True, **kwargs)


def env() -> dict:
    env = dict(os.environ)
    env["PYTHONPATH"] = "%s:%s" % (
        os.path.join(PIPELINE, "shims"),
        PIPELINE,
    )
    env["LD_LIBRARY_PATH"] = os.environ.get(
        "NEB_GL_STUB_DIR", "/home/user/.nebvideo/stublibs"
    )
    env["PATH"] = "%s:%s" % (
        os.environ.get("NEB_BIN_DIR", "/home/user/.nebvideo/bin"),
        env.get("PATH", ""),
    )
    return env


def main(argv: list[str]) -> int:
    if len(argv) < 3:
        print(__doc__.strip())
        return 2
    scene, name = argv[1], argv[2]
    out = None
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    quality = "-qh"
    if "--quality" in argv:
        quality = argv[argv.index("--quality") + 1]

    python = os.environ.get("NEB_VENV", "/home/user/.nebvideo-venv") + "/bin/python"
    scene_abs = os.path.abspath(scene)
    os.makedirs(BUILD, exist_ok=True)

    # 1. where does each line of narration start?
    run([python, os.path.join(HERE, "layout.py"), "beats", scene_abs, BEATS], env=env())

    # 2. the picture
    video = os.path.join(
        BUILD,
        "videos",
        os.path.splitext(os.path.basename(scene))[0],
        "1080p30",
        "%s.mp4" % name,
    )
    run(["bash", os.path.join(HERE, "render.sh"), scene, name, quality, "--fps", "30"], env=env())

    # 3. the voice
    narrated = video.replace(".mp4", "-narrated.mp4")
    run(
        [python, os.path.join(HERE, "mux.py"), video, os.path.join(PIPELINE, "audio"), narrated, BEATS],
        env=env(),
    )

    # 4. the checks
    run([python, os.path.join(HERE, "qa.py"), narrated], env=env())

    if out:
        os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
        shutil.copyfile(narrated, out)
        print("copied to %s" % out)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
