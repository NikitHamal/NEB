"""The NEBians video design system.

Colour is not re-decided here: it is read straight out of
``tools/design/palette.py``, the same single source of truth the Android app
and the web client are generated from, so a video, a note and a screen can
never drift apart.  The only choice made in this file is *which* roles to use
and at what size, because video has constraints an app does not (a 1 px
hairline is fine on a phone and aliases badly on a 1080p timeline).

Run ``python3 tools/manim/neb/theme.py`` to print the palette the renderer will
actually use.
"""

from __future__ import annotations

import inspect
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_HERE, "..", "..", ".."))
for _p in (os.path.join(_ROOT, "tools", "design"), _HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import palette as _palette  # noqa: E402  (tools/design/palette.py)

from manim import (  # noqa: E402
    DOWN,
    FadeIn,
    FadeOut,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
    Circle,
    Line,
    Mobject,
    RoundedRectangle,
    Scene,
    Text,
    ValueTracker,
    VGroup,
    always_redraw,
)

# ── Colour ─────────────────────────────────────────────────────────────────
# Straight from the palette's dark theme.  The video background is one step
# below the app's page (surfaceContainerLowest rather than surface): projected
# or full-screened, a mid-graphite page reads as a grey box.
N = _palette.N
B = _palette.B
S = _palette.S
V = _palette.V
DARK = _palette.DARK

BG = N[6]              # #101216  page
SURFACE = N[10]        # #191B20  card
SURFACE_RAISED = N[14]  # #212329  raised card / input
SURFACE_HIGH = N[20]   # #2B2D35  chip fill
HAIRLINE = N[32]       # #3F424C  card border
OUTLINE = N[60]        # #787D8A  strong border

TEXT = DARK["onBackground"]          # #E7E9ED  primary
TEXT_SECOND = DARK["onSurfaceVariant"]  # #A9AEB9
TEXT_MUTED = DARK["onSurfaceTertiary"]  # #878C99

ACCENT = DARK["primary"]        # #B4C5FF  brand blue
ACCENT_STRONG = B[70]           # #6E9BFF
ACCENT_DEEP = B[40]             # #004AC6
ACCENT_SOFT = B[30]             # #003EA8
VIOLET = DARK["tertiary"]       # #C4B5FD
WARN = DARK["error"]            # #FFB4AB  caution / wrong
GOOD = B[80]                    # #B4C5FF  correct answer
STEEL = S[70]                   # #9DAAC2

# The palette has no yellow; the accent ramp is what a highlight is made of.
HIGHLIGHT_CYCLE = (ACCENT, VIOLET, ACCENT_STRONG, WARN, STEEL)

# ── Type ───────────────────────────────────────────────────────────────────
FONT = "Poppins"

TITLE_SIZE = 62
H1_SIZE = 40
H2_SIZE = 36
BODY_SIZE = 30
SMALL_SIZE = 25
TINY_SIZE = 21

# ── Layout ─────────────────────────────────────────────────────────────────
# 16:9.  Manim's frame is 14.222 x 8 units at any pixel height.
FRAME_W = 14.2222
FRAME_H = 8.0
MARGIN_X = 0.9
MARGIN_TOP = 0.55
MARGIN_BOTTOM = 0.5
CONTENT_W = FRAME_W - 2 * MARGIN_X
CONTENT_H = FRAME_H - MARGIN_TOP - MARGIN_BOTTOM
LEFT_EDGE = -FRAME_W / 2 + MARGIN_X
RIGHT_EDGE = FRAME_W / 2 - MARGIN_X
TOP_EDGE = FRAME_H / 2 - MARGIN_TOP
BOTTOM_EDGE = -FRAME_H / 2 + MARGIN_BOTTOM

# ── Stroke widths ──────────────────────────────────────────────────────────
# Manim does not measure stroke width in frame units: the camera multiplies it
# by ``cairo_line_width_multiple`` (0.01) before handing it to cairo, so a
# width of 1 is one hundredth of a frame unit.  Designing in pixels is far
# easier to reason about, and 1080p is the resolution every episode is cut for.
FRAME_PIXELS = 1920
PIXELS_PER_UNIT = FRAME_PIXELS / FRAME_W  # 135 px per frame unit


def stroke(pixels: float) -> float:
    """Manim stroke width for a line ``pixels`` wide at 1080p."""
    return pixels * 100.0 / PIXELS_PER_UNIT


# The widths the design system actually uses, in pixels at 1080p.
HAIRLINE_W = stroke(1.6)  # card and table borders: visible, never heavy
RULE_W = stroke(2.4)      # section underline, ticks
STRONG_W = stroke(4.0)    # emphasis: progress bar, marked divisions

# ── Motion ─────────────────────────────────────────────────────────────────
# One vocabulary of durations so the whole episode breathes at one rate.
T_QUICK = 0.35
T_BEAT = 0.6
T_SLOW = 0.9
T_SECTION = 1.1

# ── Convenience colours for gradients and rules ────────────────────────────
GRADIENT = (N[8], N[6])


def card(
    width: float,
    height: float,
    fill: str = SURFACE,
    border: str = HAIRLINE,
    border_width: float = 0.022,
    radius: float = 0.16,
    fill_opacity: float = 1.0,
):
    """The one card in the system: a fill plus a hairline you can actually see."""
    return RoundedRectangle(
        width=width,
        height=height,
        corner_radius=radius,
        stroke_color=border,
        stroke_width=border_width,
        fill_color=fill,
        fill_opacity=fill_opacity,
    )


def chip(text: str, size: int = SMALL_SIZE, color: str = ACCENT, **kwargs):
    """A small rounded label (dimension tags, '§ 1.1', ...)."""
    label = Text(text, font=FONT, weight="MEDIUM", font_size=size, color=color, **kwargs)
    box = RoundedRectangle(
        width=label.width + 0.42,
        height=label.height + 0.3,
        corner_radius=0.14,
        stroke_color=HAIRLINE,
        stroke_width=stroke(1.6),
        fill_color=SURFACE_RAISED,
        fill_opacity=1.0,
    )
    return VGroup(box, label)


def rule(width: float = CONTENT_W, color: str = HAIRLINE, y: float = 0.0, opacity: float = 1.0):
    line = Line(
        LEFT * width / 2, RIGHT * width / 2, stroke_color=color, stroke_width=stroke(1.4)
    )
    line.move_to(ORIGIN + UP * y)
    if opacity < 1:
        line.set_stroke(color=color, opacity=opacity)
    return line


def dot(color: str = ACCENT, radius: float = 0.055):
    return Circle(radius=radius, fill_color=color, fill_opacity=1.0, stroke_width=0)


class NebEpisode(Scene):
    """Base scene: background, footer, and a progress bar that tracks sections.

    An episode is written as a list of sections.  ``open_section`` fades in a
    header and advances the progress bar; ``close_section`` takes everything in
    ``self._section_mobs`` back off screen.  ``hold`` waits for the narration,
    which is what keeps picture and voice in step -- see
    ``tools/manim/scripts/timings.py``.
    """

    #: shown in the footer, e.g. "Class 11 Physics · Unit 1"
    subject_line = ""
    #: episode title for the title card
    episode_title = ""
    #: number of sections, used to lay out the progress bar
    total_sections = 1
    #: how long the narration for each beat runs, in seconds.  Written by
    #: tools/manim/scripts/make_timings.py once the voice-over exists, and read
    #: back here so picture and voice stay in step without re-cutting the scene.
    timings: dict = {}
    #: file the timings are read from, relative to the scene module
    timings_file = "timings.json"
    #: where each beat's narration starts, in seconds of scene time.  Filled in
    #: as the episode plays, then written out so the muxer knows exactly where
    #: to drop each recorded line of voice-over.
    _beat_log: dict = {}

    def setup(self) -> None:
        super().setup()
        self.camera.background_color = BG
        self._section_mobs: list[Mobject] = []
        self._section_index = 0
        self._progress = ValueTracker(0.0)
        self.timings = self._load_timings()
        self._beat_log = {}
        self._build_chrome()

    def _load_timings(self) -> dict:
        """Read per-beat narration durations, if the voice-over has been cut.

        ``NEB_TIMING_SCALE`` shrinks every hold, which is only useful for a
        quick preview render: the picture still visits every beat, the episode
        just runs faster than the voice would.
        """
        try:
            here = os.path.dirname(os.path.abspath(inspect.getfile(type(self))))
        except (TypeError, OSError):
            return {}
        path = os.path.join(here, self.timings_file)
        data: dict = {}
        if os.path.exists(path):
            with open(path, encoding="utf-8") as handle:
                data = json.load(handle)
        scale = float(os.environ.get("NEB_TIMING_SCALE", "1") or 1)
        if scale != 1:
            data = {key: value * scale for key, value in data.items()}
        return data

    def beat(self, key: str, animations=(), run_time: float = T_BEAT, lead: float = 0.0):
        """Play ``animations``, then wait for the narration beat ``key``.

        ``lead`` is a deliberate pause before the animations start, used where
        the voice needs to land before the picture moves.
        """
        if lead > 0:
            self.wait(lead)
        if animations:
            self.play(*animations, run_time=run_time)
        self._beat_log[key] = round(self.renderer.time, 3)
        self.hold(self.timings.get(key, 0.0) - run_time - lead)

    def _dump_beat_log(self) -> None:
        """Write where each beat's narration starts, for the muxer."""
        if not self._beat_log:
            return
        path = os.environ.get("NEB_BEAT_LOG")
        if not path:
            return
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(self._beat_log, handle, indent=2, sort_keys=True)
            handle.write("\n")

    def tear_down(self) -> None:
        super().tear_down()
        self._dump_beat_log()

    # ── chrome ─────────────────────────────────────────────────────────────
    #: y of the progress bar and of the footer, from the bottom of the frame
    BAR_Y = -FRAME_H / 2 + 0.14
    FOOTER_Y = -FRAME_H / 2 + 0.42

    def _build_chrome(self) -> None:
        y = self.BAR_Y
        self._bar_anchor = LEFT * (CONTENT_W / 2)
        self._progress_line = always_redraw(
            lambda: Line(
                self._bar_anchor,
                self._bar_anchor
                + RIGHT
                * max(CONTENT_W * self._progress.get_value(), 1e-4),
                stroke_color=ACCENT,
                stroke_width=stroke(4),
            )
        )
        self._progress_line.move_to(self._bar_anchor + DOWN * y)
        self._track_line = Line(
            self._bar_anchor,
            self._bar_anchor + RIGHT * CONTENT_W,
            stroke_color=N[24],
            stroke_width=stroke(4),
        ).move_to(self._bar_anchor + DOWN * y)

        brand = Text(
            "NEBians",
            font=FONT,
            weight="SEMIBOLD",
            font_size=TINY_SIZE,
            color=TEXT_SECOND,
        )
        subject = Text(
            self.subject_line,
            font=FONT,
            weight="REGULAR",
            font_size=TINY_SIZE,
            color=TEXT_MUTED,
        )
        footer = VGroup(brand, subject).arrange(RIGHT, buff=0.28)
        footer.move_to(
            [
                self._bar_anchor[0],
                self.FOOTER_Y,
                0,
            ],
            aligned_edge=LEFT,
        )
        self._chrome = VGroup(self._track_line, self._progress_line, footer)
        self.add(self._chrome)

    def set_progress(self, fraction: float) -> None:
        self._progress.set_value(min(max(fraction, 0.0), 1.0))

    # ── sections ───────────────────────────────────────────────────────────
    def open_section(
        self,
        title: str,
        kicker: str | None = None,
        run_time: float = T_SECTION,
        shift: float = 0.28,
    ):
        """Fade in a section header; returns the header group."""
        self._section_index += 1
        self.set_progress(self._section_index / self.total_sections)
        head = VGroup()
        if kicker:
            kick = Text(
                kicker,
                font=FONT,
                weight="MEDIUM",
                font_size=SMALL_SIZE,
                color=ACCENT,
            )
            head.add(kick)
        title_mob = Text(
            title,
            font=FONT,
            weight="SEMIBOLD",
            font_size=H1_SIZE,
            color=TEXT,
        )
        head.add(title_mob)
        head.arrange(DOWN, buff=0.16, aligned_edge=LEFT)
        head.move_to(TOP_EDGE * UP + LEFT_EDGE * RIGHT, aligned_edge=UP + LEFT)
        underline = Line(
            head.get_left(),
            head.get_left() + RIGHT * 1.9,
            stroke_color=ACCENT,
            stroke_width=stroke(3),
        ).next_to(head, DOWN, buff=0.18)
        group = VGroup(head, underline)
        group.shift(UP * shift)
        group.set_opacity(0)
        self.play(group.animate.shift(DOWN * shift).set_opacity(1), run_time=run_time)
        self._section_mobs.append(group)
        return group

    def close_section(self, run_time: float = T_BEAT) -> None:
        if not self._section_mobs:
            return
        mobs = [m for m in self._section_mobs if m is not None]
        if mobs:
            self.play(*[m.animate.shift(DOWN * 0.3).set_opacity(0) for m in mobs], run_time=run_time)
        for m in mobs:
            self.remove(m)
        self._section_mobs = []

    def hold(self, seconds: float) -> None:
        """Wait for the narration to catch up (no-op for a negative duration)."""
        if seconds > 0:
            self.wait(seconds)

    def swap(self, old, new, run_time: float = T_BEAT, shift: float = UP * 0.25):
        """Crossfade one group out and another in."""
        self.play(FadeOut(old, shift=shift), FadeIn(new, shift=shift), run_time=run_time)
        self.remove(old)
        self._section_mobs.append(new)
        return new
