"""Audit the layout of an episode without rendering it.

Replays ``construct`` with a stand-in scene that records which mobjects are on
screen at each section, then prints their bounding boxes and flags anything
that runs past the safe margins.  Catches overlaps and overflow in a second
instead of a render.

    tools/manim/scripts/layout.py videos/phy11_unit01.py
"""

from __future__ import annotations

import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
for path in (os.path.join(ROOT, "tools", "manim", "shims"), os.path.join(ROOT, "tools", "manim")):
    if path not in sys.path:
        sys.path.insert(0, path)

from manim import Group, VGroup  # noqa: E402
from manim.animation.animation import DEFAULT_ANIMATION_RUN_TIME  # noqa: E402

from neb.theme import (  # noqa: E402
    BOTTOM_EDGE,
    LEFT_EDGE,
    RIGHT_EDGE,
    T_SECTION,
    TOP_EDGE,
)

_OUT = ("FadeOut", "Uncreate", "ShrinkToCenter", "FadeOutAndShift")

CEILING = 2.45  # the section header owns everything above this line


LAST_CLOCK = 0.0
LAST_BEATS: dict = {}
SCENE_PATH = ""


def _scene_timings() -> dict:
    """The narration durations of the scene under audit."""

    path = os.path.join(os.path.dirname(SCENE_PATH), "timings.json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as handle:
            return json.load(handle)
    return {}


def load(path: str):
    spec = importlib.util.spec_from_file_location("episode_under_audit", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    global SCENE_PATH
    SCENE_PATH = path
    return module


def audit(cls) -> list[tuple[str, list]]:
    """Run ``cls.construct`` against a recording scene; return section frames."""

    class Recorder(cls):  # type: ignore[misc, valid-type]
        def setup(self) -> None:
            self._current: list = []
            self.sections: list[tuple[str, list]] = []
            self._section_mobs: list = []
            self._section_index = 0
            self._chrome = VGroup()
            self._clock = 0.0
            # timings.json lives beside the scene, not beside this script
            self.timings = _scene_timings()
            self._beat_log: dict = {}

        def play(self, *animations, **kwargs) -> None:  # type: ignore[override]
            self._clock += kwargs.get("run_time", DEFAULT_ANIMATION_RUN_TIME)
            for animation in animations:
                mobject = getattr(animation, "mobject", None)
                if mobject is None:
                    continue
                name = type(animation).__name__
                if any(tag in name for tag in _OUT):
                    self.remove(mobject)
                else:
                    self.add(mobject)

        def add(self, *mobjects) -> None:  # type: ignore[override]
            for mobject in mobjects:
                if mobject not in self.mobjects:
                    self.mobjects.append(mobject)
                if mobject not in self._current:
                    self._current.append(mobject)

        def remove(self, *mobjects) -> None:  # type: ignore[override]
            for mobject in mobjects:
                if mobject in self.mobjects:
                    self.mobjects.remove(mobject)
                if mobject in self._current:
                    self._current.remove(mobject)

        def wait(self, *args, **kwargs) -> None:  # type: ignore[override]
            self._clock += args[0] if args else kwargs.get("duration", 1.0)
            return None

        def hold(self, seconds: float) -> None:  # type: ignore[override]
            self._clock += max(0.0, seconds)
            return None

        def beat(self, key, animations=(), **kwargs):  # type: ignore[override]
            run_time = kwargs.get("run_time", DEFAULT_ANIMATION_RUN_TIME)
            lead = kwargs.get("lead", 0.0)
            if lead > 0:
                self.wait(lead)
            self.play(*animations, run_time=run_time)
            self._beat_log[key] = round(self._clock, 3)
            self._clock += max(0.0, self.timings.get(key, 0.0) - run_time - lead)
            self.sections.append((key, list(self._current)))

        def open_section(self, title, kicker=None, **kwargs):  # type: ignore[override]
            # the real open_section plays a fade for the header; the clock has
            # to pay for it even though nothing is drawn here
            self._clock += kwargs.get("run_time", T_SECTION)
            self.sections.append((f"[{title}]", list(self._current)))
            return VGroup()

        def close_section(self, **kwargs):  # type: ignore[override]
            self.sections.append(("[close]", list(self._current)))
            self._current = []

    scene = Recorder()
    scene.setup()
    scene.construct()
    global LAST_CLOCK, LAST_BEATS
    LAST_CLOCK = scene._clock
    LAST_BEATS = scene._beat_log
    return scene.sections


def report(sections) -> int:
    problems = 0
    for title, mobjects in sections:
        live = [m for m in mobjects if m is not None]
        if not live:
            continue
        group = Group(*live)
        flags = []
        if group.get_left()[0] < LEFT_EDGE - 0.05:
            flags.append("LEFT %.2f" % group.get_left()[0])
        if group.get_right()[0] > RIGHT_EDGE + 0.05:
            flags.append("RIGHT %.2f" % group.get_right()[0])
        if group.get_top()[1] > TOP_EDGE + 0.05:
            flags.append("TOP %.2f" % group.get_top()[1])
        if group.get_bottom()[1] < BOTTOM_EDGE - 0.05:
            flags.append("BOTTOM %.2f" % group.get_bottom()[1])
        if group.get_top()[1] > CEILING:
            flags.append("CEILING %.2f" % (group.get_top()[1] - CEILING))
        print(
            "%-38s %5.2f x %5.2f  centre (%6.2f, %6.2f)  %s"
            % (
                title[:38],
                group.width,
                group.height,
                group.get_center()[0],
                group.get_center()[1],
                "  ".join(flags),
            )
        )
        if flags:
            problems += 1
    return problems


def scene_classes(module):
    """Every scene class defined in ``module``."""

    for name, obj in sorted(vars(module).items()):
        if not isinstance(obj, type) or obj.__module__ != "episode_under_audit":
            continue
        if not hasattr(obj, "construct") or name.startswith("_"):
            continue
        yield name, obj


def cmd_beats(path: str, out: str) -> int:
    """Replay the scene with no rendering and write the beat clock."""

    module = load(path)
    found = False
    for name, obj in scene_classes(module):
        audit(obj)
        found = True
    if not found or not LAST_BEATS:
        print("no beats recorded")
        return 1
    with open(out, "w", encoding="utf-8") as handle:
        json.dump(LAST_BEATS, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print("wrote %s: %d beats, %.2f s of scene time" % (out, len(LAST_BEATS), LAST_CLOCK))
    return 0


def main(argv: list[str]) -> int:
    if len(argv) > 1 and argv[1] == "beats":
        if len(argv) < 4:
            print("usage: layout.py beats <scene.py> <beats.json>")
            return 2
        return cmd_beats(os.path.abspath(argv[2]), argv[3])
    if len(argv) < 2:
        print(__doc__)
        return 1
    module = load(os.path.abspath(argv[1]))
    total = 0
    for name, obj in scene_classes(module):
        print("=" * 78)
        print(name)
        print("=" * 78)
        try:
            sections = audit(obj)
        except Exception as exc:  # noqa: BLE001
            print("  could not replay construct: %r" % (exc,))
            continue
        total += report(sections)
        print("-" * 78)
    print("%d section(s) out of bounds" % total)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
