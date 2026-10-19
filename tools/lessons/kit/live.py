"""Cheap live readouts: glyphs are rendered once and switched by opacity, so a counter
can update on every frame without re-rendering text (which is the slowest thing Manim does)."""
import numpy as np
from manim import VGroup, always_redraw, Rectangle, Dot

from . import theme as th
from .text import T

DIGITS = "0123456789"


class Counter(VGroup):
    """A fixed-width integer readout. `digits` slots, monospaced, updates for free."""

    def __init__(self, value=0, digits=3, size=30, color=th.INK, weight="SEMIBOLD",
                 suffix="", unit_size=0.72, **kw):
        super().__init__(**kw)
        glyphs = [T(d, size=size, color=color, weight=weight) for d in DIGITS]
        self.adv = max(g.width for g in glyphs) * 1.04
        self.digits = digits
        self._slots = []
        for _ in range(digits):
            slot = VGroup(*[g.copy() for g in glyphs])
            for g in slot:
                g.set_opacity(0)
            self._slots.append(slot)
            self.add(slot)
        x = 0.0
        for slot in self._slots:
            for g in slot:
                g.move_to([x + self.adv / 2, 0, 0])
            x += self.adv
        self.suffix = None
        if suffix:
            self.suffix = T(suffix, size=size * unit_size, color=color, weight=weight)
            self.suffix.move_to([x + self.suffix.width / 2 + 0.05, 0, 0])
            self.add(self.suffix)
        self.set_value(value)

    def set_value(self, v):
        v = int(round(max(0.0, v)))
        s = str(v)
        s = s[-self.digits:].rjust(self.digits)
        for slot, ch in zip(self._slots, s):
            for k, g in enumerate(slot):
                g.set_opacity(1.0 if ch != " " and k == int(ch) else 0.0)
        return self

    def bind(self, tracker, scale=1.0):
        """Follow a ValueTracker."""
        self.add_updater(lambda m: m.set_value(tracker.get_value() * scale))
        return self


def live_counter(tracker, value=0, **kw):
    c = Counter(value=value, **kw)
    c.bind(tracker)
    return c


class Bars(VGroup):
    """Vertical bars on a common baseline, drawn up from the base with one call."""

    def __init__(self, heights, width=0.5, gap=0.35, color=th.SKY, base=0.0, **kw):
        super().__init__(**kw)
        self._bars = []
        x = 0.0
        for h in heights:
            r = Rectangle(width=width, height=max(0.001, h), stroke_width=0, fill_color=color,
                          fill_opacity=0.85)
            r.move_to([x, base + max(0.001, h) / 2, 0])
            self._bars.append(r)
            self.add(r)
            x += width + gap
        self.set_x(0.0)

    def set_x(self, x0):
        self.shift([x0 - self.get_left()[0], 0, 0])
        return self


def dot_row(n, radius=0.09, gap=0.26, color=th.SKY, fill=1.0):
    return VGroup(*[Dot(radius=radius, color=color).set_fill(color, fill) for _ in range(n)]).arrange([1, 0, 0], buff=gap)
