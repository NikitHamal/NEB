"""Cheap visual check of a lesson: render some parts at 360p and 3 fps (no audio mix, no
encode pass), then lay out evenly spaced frames on a contact sheet you can actually look at.

    python3 frames.py scripts/phy12/unit_02.py 1,2          # parts 1 and 2 -> .work/frames/phy12-unit_02-p1,2.png
    python3 frames.py scripts/phy12/unit_02.py 3 --count 30  # denser sheet
    python3 frames.py scripts/phy12/unit_02.py all --dry     # whole lesson, no drawing: catches errors fast

Parts are the indices passed to `self.parts(...)` (0 = cold open). Narration is still
synthesised (and cached), so timing on the sheet is the real timing. Full-quality renders
are done with build.py on a bigger machine."""
import argparse
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, ".work")
sys.path.insert(0, HERE)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("script")
    ap.add_argument("parts", help="comma separated part indices, e.g. 0 or 2,3")
    ap.add_argument("--count", type=int, default=24)
    ap.add_argument("--fps", default="3")
    ap.add_argument("--dry", action="store_true", help="run the whole scene logic without drawing a frame: catches errors in seconds")
    a = ap.parse_args()
    script = os.path.abspath(a.script)
    name = os.path.splitext(os.path.basename(script))[0]
    book = os.path.basename(os.path.dirname(script))
    tag = f"{book}-{name}-p{a.parts}"
    media = os.path.join(WORK, "media", "frames-" + tag)
    out_dir = os.path.join(WORK, "frames")
    os.makedirs(out_dir, exist_ok=True)
    from prefetch import prefetch
    prefetch(script)
    if a.dry:
        env = dict(os.environ, PYTHONPATH=HERE + os.pathsep + os.environ.get("PYTHONPATH", ""))
        if a.parts != "all":
            env["LESSON_ONLY"] = a.parts
        os.makedirs(media + "-dry", exist_ok=True)
        subprocess.run(["manim", "render", "--dry_run", "--fps", "4", "-r", "320,180", "--media_dir", media + "-dry", "--disable_caching", "-v", "WARNING", "--progress_bar", "none", script, "Lesson"],
                       env=env, cwd=HERE, check=True)
        print("dry run ok")
        return
    env = dict(os.environ, LESSON_ONLY=a.parts, PYTHONPATH=HERE + os.pathsep + os.environ.get("PYTHONPATH", ""))
    subprocess.run(["manim", "render", "--disable_caching", "-r", "640,360", "--fps", a.fps, "--media_dir", media,
                    "-o", tag, "--progress_bar", "none", "-v", "WARNING", script, "Lesson"], env=env, cwd=HERE, check=True)
    raw = None
    for dp, _, fs in os.walk(os.path.join(media, "videos")):
        for f in fs:
            if f == tag + ".mp4":
                raw = os.path.join(dp, f)
    from contact import sheet
    png = os.path.join(out_dir, tag + ".png")
    sheet(raw, png, a.count, cols=4, w=480)
    print(png)


if __name__ == "__main__":
    main()
