"""List the narration cache files a lesson uses (for pushing one unit at a time):
    python3 ttskeys.py scripts/math12/unit_01.py  ->  prints .cache/tts/<key>.{mp3,json,srt} paths"""
import atexit
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import kit.lesson as lesson  # noqa: E402
import kit.voice as voice  # noqa: E402

_orig = voice.speak
_keys = set()


def _speak(text, lang="en"):
    r = _orig(text, lang)
    _keys.add(os.path.splitext(os.path.basename(r[0]))[0])
    return r


voice.speak = lesson.speak = _speak


@atexit.register
def _dump():
    for k in sorted(_keys):
        for ext in ("mp3", "json", "srt"):
            p = os.path.join(voice.CACHE, f"{k}.{ext}")
            if os.path.exists(p):
                print(os.path.relpath(p, os.getcwd()), file=sys.__stdout__)


if __name__ == "__main__":
    from manim.__main__ import main
    media = f"/tmp/ttskeys-media-{os.getpid()}"
    for sub in ("Tex", "texts", "images"):
        os.makedirs(os.path.join(media, sub), exist_ok=True)
    sys.argv = ["manim", "render", "--dry_run", "--fps", "4", "-r", "320,180", "--media_dir", media, "--disable_caching", "-v", "ERROR", "--progress_bar", "none", sys.argv[1], "Lesson"]
    main()
