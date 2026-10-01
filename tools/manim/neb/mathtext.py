"""Math typesetting for Manim without LaTeX.

Manim's ``MathTex``/``Tex`` mobjects shell out to ``latex`` + ``dvisvgm``,
neither of which exists in this environment.  This module renders the same
kind of maths with **matplotlib's mathtext** engine (the STIX font set, which
is what the NEBians PDF pipeline already uses) and converts the glyph
outlines into a ``VMobject`` so the result behaves exactly like a ``MathTex``
inside any Manim animation.

The conversion follows matplotlib's own ``TextToPath`` recipe:

* the string is parsed at the requested size so that the layout offsets come
  out in points,
* every glyph outline is fetched from a face sized at ``FONT_SCALE`` points
  (a precision trick used by matplotlib) and scaled back down by
  ``fontsize / FONT_SCALE``.

Colouring individual terms (``substrings_to_isolate``) is done by matching the
glyph sequence of each term against the glyph sequence of the whole
expression, which keeps every rendered fragment valid maths - unlike string
splitting, which would feed ``\\frac{`` to the parser on its own.
"""

from __future__ import annotations

import re
from collections.abc import Iterable, Sequence

import matplotlib
import numpy as np
from matplotlib.ft2font import LoadFlags
from matplotlib.mathtext import MathTextParser
from matplotlib.font_manager import FontProperties
from manim import (
    BLACK,
    DEFAULT_FONT_SIZE,
    VMobject,
    VGroup,
)

# Same font set as notes/pipeline/mathsvg.py so notes and video agree.
matplotlib.rcParams.setdefault("mathtext.fontset", "stix")

#: matplotlib's TextToPath precision trick: outlines are always pulled from a
#: face sized at this many points and scaled back down.
FONT_SCALE = 100.0
_DPI = 72

# Manim text sizing constants (manim/mobject/text/text_mobject.py).
TEXT2SVG_ADJUSTMENT_FACTOR = 4.8
TEXT_MOB_SCALE_FACTOR = 0.05

# Fallback colours cycled through when ``substrings_to_isolate`` is used
# without an explicit palette.
DEFAULT_ISOLATE_COLOURS = ("#F5B841", "#4FA3FF", "#7BD88F", "#E879C7", "#FF8A5B")

# --------------------------------------------------------------------------
# LaTeX -> mathtext translation (ported from notes/pipeline/mathsvg.py)
# --------------------------------------------------------------------------

_FIX = [
    (r"\\left\s*\|", "|"),
    (r"\\right\s*\|", "|"),
    (r"\\left\.", ""),
    (r"\\right\.", ""),
    (r"\\left", r"\\left("),
    (r"\\right", r"\\right)"),
    (r"\\(bigg?|Bigg?)[lrm]?", ""),
    (r"\\!", ""),
    (r"\\,", r"\\ "),
    (r"\\;", r"\\ "),
    (r"\\quad", r"\\qquad"),
    (r"\\displaystyle", ""),
    (r"\\limits", ""),
    (r"\\nonumber", ""),
    (r"\\notag", ""),
    (r"\\label\{[^}]*\}", ""),
    (r"\\mathrm\b", r"\\mathdefault"),
    (r"\\textrm\b", r"\\text"),
    (r"\\mbox\b", r"\\text"),
    (r"\\operatorname\b", r"\\mathdefault"),
    (r"\\dfrac", r"\\frac"),
    (r"\\tfrac", r"\\frac"),
    (r"\\ce\b", r"\\text"),
    (r"\\degree", r"^\\circ"),
    (r"\\micro", r"\\mu"),
    (r"\\textbf\b", r"\\mathbf"),
    (r"\\textit\b", r"\\mathit"),
    (r"\\le\b", r"\\leq"),
    (r"\\ge\b", r"\\geq"),
    (r"\\ne\b", r"\\neq"),
    (r"\\to\b", r"\\rightarrow"),
]

_DIGIT_ARG = re.compile(r"\\(frac|binom)\s*([0-9a-zA-Z])\s*([0-9a-zA-Z])")
_ENV = re.compile(
    r"\\begin\{(aligned|align\*?|gather\*?|split|equation\*?)\}"
    r"|\\end\{(aligned|align\*?|gather\*?|split|equation\*?)\}"
)


def _strip_wrapper(s: str, name: str) -> str:
    """Turn ``\\name{...}`` into ``...`` (mathtext has no such command)."""
    needle = "\\" + name + "{"
    out = s
    while needle in out:
        start = out.find(needle)
        depth = 0
        i = start + len(needle) - 1
        for j in range(i, len(out)):
            if out[j] == "{":
                depth += 1
            elif out[j] == "}":
                depth -= 1
                if depth == 0:
                    out = out[:start] + out[start + len(needle) : j] + out[j + 1 :]
                    break
        else:
            break
    return out


def clean_tex(tex: str) -> str:
    """Rewrite a LaTeX-ish string into something mathtext can parse."""
    s = tex.strip()
    if s.startswith("$$") and s.endswith("$$") and len(s) > 3:
        s = s[2:-2].strip()
    s = s.strip("$").strip()
    s = re.sub(r"\s+", " ", s)
    for name in ("boxed", "mbox", "textnormal", "ensuremath", "phantom"):
        s = _strip_wrapper(s, name)
    for pattern, repl in _FIX:
        s = re.sub(pattern, repl, s)
    s = _DIGIT_ARG.sub(r"\\\1{\2}{\3}", s)
    s = _ENV.sub("", s)
    s = re.sub(r"\\\\(?=[A-Za-z])", r"\\", s)
    s = s.replace("&", "").replace("\\\\", "\\ \\ ")
    s = s.strip()
    # mathtext only switches into math mode between $...$; without the
    # delimiters every backslash command is rendered as literal text.
    if not (len(s) > 1 and s.startswith("$") and s.endswith("$")):
        s = "$" + s + "$"
    return s


# --------------------------------------------------------------------------
# mathtext layout -> VMobject
# --------------------------------------------------------------------------


def _point(vertex, ox: float, oy: float, scale: float) -> np.ndarray:
    return np.array([vertex[0] * scale + ox, vertex[1] * scale + oy, 0.0])


def _append_glyph(
    vm: VMobject, verts, codes, ox: float, oy: float, scale: float
) -> None:
    """Add one glyph outline to ``vm`` (already in point units)."""
    i = 0
    n = len(codes)
    start = None
    current = None
    while i < n:
        code = int(codes[i])
        if code == 1:  # MOVETO
            current = _point(verts[i], ox, oy, scale)
            vm.start_new_path(current)
            start = current
            i += 1
        elif code == 2:  # LINETO
            current = _point(verts[i], ox, oy, scale)
            vm.add_line_to(current)
            i += 1
        elif code == 3:  # CURVE3 (quadratic)
            ctrl = _point(verts[i], ox, oy, scale)
            end = _point(verts[i + 1], ox, oy, scale)
            handle1 = current + (2.0 / 3.0) * (ctrl - current)
            handle2 = end + (2.0 / 3.0) * (ctrl - end)
            vm.add_cubic_bezier_curve_to(handle1, handle2, end)
            current = end
            i += 2
        elif code == 4:  # CURVE4 (cubic)
            h1 = _point(verts[i], ox, oy, scale)
            h2 = _point(verts[i + 1], ox, oy, scale)
            end = _point(verts[i + 2], ox, oy, scale)
            vm.add_cubic_bezier_curve_to(h1, h2, end)
            current = end
            i += 3
        elif code == 79:  # CLOSEPOLY
            if start is not None:
                vm.add_line_to(start)
                current = start
            i += 1
        else:  # pragma: no cover - unknown path code
            i += 1


def _append_rect(vm: VMobject, x: float, y: float, w: float, h: float) -> None:
    corners = [
        np.array([x, y, 0.0]),
        np.array([x + w, y, 0.0]),
        np.array([x + w, y + h, 0.0]),
        np.array([x, y + h, 0.0]),
    ]
    vm.start_new_path(corners[0])
    for corner in corners[1:]:
        vm.add_line_to(corner)
    vm.add_line_to(corners[0])


def _parse_math(tex: str, size: float):
    """Parse ``tex``; returns ``(width, height, descent, glyphs, rects)``."""
    parser = MathTextParser("path")
    return parser.parse(
        clean_tex(tex),
        dpi=_DPI,
        prop=FontProperties(size=size),
    )


def _glyph_outline(font, glyph_index: int, fontsize: float):
    font.clear()
    font.set_size(FONT_SCALE, _DPI)
    font.load_glyph(glyph_index, LoadFlags.NO_HINTING)
    verts, codes = font.get_path()
    # points -> Manim units, using the same factor ``Text`` uses so that a
    # ``font_size`` of 48 means the same thing for maths and for prose.
    return verts, codes, fontsize / FONT_SCALE * TEXT_MOB_SCALE_FACTOR


def _term_signature(term: str, size: float) -> tuple[int, ...]:
    """Glyph-index fingerprint of ``term`` at ``size`` points."""
    _w, _h, _d, glyphs, _r = _parse_math(term, size)
    return tuple(g[3] for g in glyphs)


def _colour_map(tex: str, size: float, terms: Sequence[str], palette) -> list | None:
    """Per-glyph colours for ``tex``, or ``None`` when nothing is isolated."""
    if not terms:
        return None
    _w, _h, _d, glyphs, _r = _parse_math(tex, size)
    indices = [g[3] for g in glyphs]
    signatures = [
        (_term_signature(term, size), palette[i % len(palette)])
        for i, term in enumerate(terms)
    ]
    colours: list = [None] * len(glyphs)
    i = 0
    while i < len(glyphs):
        for signature, colour in signatures:
            n = len(signature)
            if n and tuple(indices[i : i + n]) == signature:
                for j in range(i, i + n):
                    colours[j] = colour
                i += n
                break
        else:
            i += 1
    return colours


def _build_pieces(
    tex: str,
    size: float,
    color,
    fill_opacity: float,
    terms: Sequence[str] = (),
    palette=(),
) -> list[tuple[VMobject, object, int | None]]:
    """Render ``tex`` into ``(VMobject, colour, term)`` runs on a y=0 baseline.

    ``term`` is the index into ``terms`` the run belongs to, or ``None``.
    """
    width, height, descent, glyphs, rects = _parse_math(tex, size)
    factor = TEXT_MOB_SCALE_FACTOR
    glyphs = [(f, fs, c, g, ox * factor, oy * factor) for f, fs, c, g, ox, oy in glyphs]
    rects = [(x * factor, y * factor, w * factor, h * factor) for x, y, w, h in rects]
    colours = _colour_map(tex, size, terms, palette) if terms else None
    resolved = [
        (colours[i] if colours else None) or color for i in range(len(glyphs))
    ]
    # Which isolated term (if any) each colour belongs to.
    term_of_colour = {}
    for index in range(len(terms)):
        term_of_colour[palette[index % len(palette)]] = index

    # Contiguous runs of one colour become a single VMobject.
    runs: list[tuple[list, object]] = []
    for i, glyph in enumerate(glyphs):
        colour = resolved[i]
        if runs and runs[-1][1] == colour:
            runs[-1][0].append(glyph)
        else:
            runs.append(([glyph], colour))

    out: list[tuple[VMobject, object, int | None]] = []
    spans: list[tuple[float, float]] = []
    for run_glyphs, colour in runs:
        vm = VMobject()
        for font, fontsize, _ccode, glyph_index, ox, oy in run_glyphs:
            verts, codes, scale = _glyph_outline(font, glyph_index, fontsize)
            if len(codes):
                _append_glyph(vm, verts, codes, ox, oy, scale)
        out.append((vm, colour, term_of_colour.get(colour)))
        spans.append((min(g[4] for g in run_glyphs), max(g[4] for g in run_glyphs)))

    # Rules (fraction bars, radical signs) take the colour of what they span.
    for x, y, w, h in rects:
        if w <= 0 or h <= 0:
            continue
        middle = x + w / 2
        target = None
        for (lo, hi), entry in zip(spans, out):
            if lo <= middle <= hi:
                target = entry
                break
        if target is None and out:
            target = out[0]
        if target is None:
            vm = VMobject()
            _append_rect(vm, x, y, w, h)
            vm.set_fill(color, opacity=fill_opacity)
            vm.set_stroke(width=0)
            out.append((vm, color, None))
        else:
            _append_rect(target[0], x, y, w, h)

    for vm, colour, _term in out:
        vm.set_fill(colour, opacity=fill_opacity)
        vm.set_stroke(width=0)
    return out


# --------------------------------------------------------------------------
# Mobjects
# --------------------------------------------------------------------------


class NebMathTex(VGroup):
    """Drop-in replacement for ``MathTex`` backed by matplotlib mathtext.

    Parameters mirror ``MathTex``: ``font_size`` is in *pixels* (48 by
    default, exactly like ``Text``), ``color`` fills everything, and
    ``substrings_to_isolate`` + ``isolate_colors`` colour individual terms.
    """

    def __init__(
        self,
        *tex_strings: str,
        color=None,
        font_size: float = DEFAULT_FONT_SIZE,
        fill_opacity: float = 1.0,
        stroke_width: float = 0.0,
        substrings_to_isolate: Iterable[str] | str | None = None,
        isolate_colors: Sequence | None = None,
        **kwargs,
    ) -> None:
        if color is None:
            color = kwargs.pop("color", None)
        if color is None:
            color = BLACK
        self._font_size = font_size
        self._fill_opacity = fill_opacity

        terms: list[str] = []
        if substrings_to_isolate:
            if isinstance(substrings_to_isolate, str):
                substrings_to_isolate = [substrings_to_isolate]
            terms = [t for t in substrings_to_isolate if t]
        palette = (
            list(isolate_colors)
            if isolate_colors
            else list(DEFAULT_ISOLATE_COLOURS)
        )

        # 48 px in Manim == 10 pt of real type, exactly like ``Text``.
        size = font_size / TEXT2SVG_ADJUSTMENT_FACTOR
        VGroup.__init__(self)
        for index, tex in enumerate(tex_strings):
            pieces = _build_pieces(
                tex, size, color, fill_opacity, terms, palette
            )
            for vm, _colour, term in pieces:
                vm.neb_term = term
                self.add(vm)
        self._n_tex = len(tex_strings)
        self._terms = terms
        # The mobjects making up each isolated term, so a scene can highlight
        # one term without re-parsing the expression.
        self.isolate_mobs = [
            VGroup(
                *[
                    vm
                    for vm in self.submobjects
                    if getattr(vm, "neb_term", None) == index
                ]
            )
            for index in range(len(terms))
        ]

    @property
    def font_size(self) -> float:
        return self._font_size

    @font_size.setter
    def font_size(self, value: float) -> None:
        self._font_size = value
        scale = value / self._font_size
        self.scale(scale)

    def get_tex(self) -> list[str]:
        return list(getattr(self, "_tex_strings", []))


class NebTex(NebMathTex):
    """``NebTex``: several strings, each an isolated argument (like ``Tex``)."""
