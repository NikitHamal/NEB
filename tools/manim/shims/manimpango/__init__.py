"""A ``manimpango``-compatible text renderer built on FreeType glyph outlines.

Why this module exists
----------------------
Manim turns text into vector mobjects by asking Pango to render the text into
an SVG file and then parsing that SVG back into ``VMobject``\\ s.  Pango is not
installable on this machine, so this module reimplements the slice of the
``manimpango`` API that Manim uses, but draws the glyphs itself with FreeType
and writes the same kind of SVG: one ``<path>`` per glyph, in the same
coordinate conventions Pango/cairo use (em size in SVG units, first line's box
top at ``START_Y``, baseline advance ``line_spacing``).

What is implemented
--------------------
* ``MarkupUtils.text2svg`` -- Pango-markup text laid out with word wrapping.
* ``text2svg`` -- the per-``TextSetting`` variant used by ``manim.Text``.
* ``MarkupUtils.validate``, ``PangoUtils.remove_last_M``, ``list_fonts``,
  ``register_font`` / ``unregister_font``, ``TextSetting``, ``pango_version``.

Geometry conventions (chosen to match cairo's SVG surface + Pango)
------------------------------------------------------------------
* ``size`` is the em size in SVG user units (1 unit = 1 pt at 72 dpi, exactly
  what ``cairo_svg_surface_create`` produces), so FreeType is asked for a pixel
  size equal to ``size``.
* The first line's *layout box top* sits at ``(START_X, START_Y)``; the
  baseline therefore lands at ``START_Y + ascent``.
* Line ``n``'s baseline is ``START_Y + ascent + line_spacing * n``.
* Wrapping happens at ``pango_width`` when given, else at ``width``.

The NEBians brand font (Poppins) ships with the repository, so the videos use
the same typeface as the app.
"""

from __future__ import annotations

import math
import os
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Sequence

import freetype

__all__ = [
    "MarkupUtils",
    "PangoUtils",
    "TextSetting",
    "Style",
    "Weight",
    "list_fonts",
    "register_font",
    "unregister_font",
    "text2svg",
    "text2markup",
    "pango_version",
    "cairo_version",
]


# --------------------------------------------------------------------------
# enums -- plain strings, matching manimpango's enums module
# --------------------------------------------------------------------------
class Style:
    NORMAL = "NORMAL"
    OBLIQUE = "OBLIQUE"
    ITALIC = "ITALIC"


class Weight:
    THIN = "THIN"
    ULTRALIGHT = "ULTRALIGHT"
    LIGHT = "LIGHT"
    SEMILIGHT = "SEMILIGHT"
    BOOK = "BOOK"
    NORMAL = "NORMAL"
    MEDIUM = "MEDIUM"
    SEMIBOLD = "SEMIBOLD"
    BOLD = "BOLD"
    ULTRABOLD = "ULTRABOLD"
    EXTRABOLD = "EXTRABOLD"
    HEAVY = "HEAVY"
    ULTRAHEAVY = "ULTRAHEAVY"


# Weight name -> preferred Poppins file stem.  Poppins ships Regular, Medium,
# SemiBold, Bold, ExtraBold and Black; everything lighter falls back to Regular.
_WEIGHT_TO_FILE = {
    Weight.THIN: "Regular",
    Weight.ULTRALIGHT: "Regular",
    Weight.LIGHT: "Regular",
    Weight.SEMILIGHT: "Regular",
    Weight.BOOK: "Regular",
    Weight.NORMAL: "Regular",
    Weight.MEDIUM: "Medium",
    Weight.SEMIBOLD: "SemiBold",
    Weight.BOLD: "Bold",
    Weight.ULTRABOLD: "Bold",
    Weight.EXTRABOLD: "ExtraBold",
    Weight.HEAVY: "ExtraBold",
    Weight.ULTRAHEAVY: "Black",
}

_MARKUP_WEIGHTS = {
    "thin": Weight.THIN,
    "ultralight": Weight.ULTRALIGHT,
    "light": Weight.LIGHT,
    "semilight": Weight.SEMILIGHT,
    "book": Weight.BOOK,
    "normal": Weight.NORMAL,
    "medium": Weight.MEDIUM,
    "semibold": Weight.SEMIBOLD,
    "bold": Weight.BOLD,
    "ultrabold": Weight.ULTRABOLD,
    "extrabold": Weight.EXTRABOLD,
    "heavy": Weight.HEAVY,
    "ultraheavy": Weight.ULTRAHEAVY,
}


@dataclass
class TextSetting:
    """One styled span of a string, as Manim's ``Text`` builds them."""

    start: int
    end: int
    font: str = ""
    slant: str = Style.NORMAL
    weight: str = Weight.NORMAL
    color: str | None = None
    line_num: int = -1


@dataclass
class _Run:
    """A maximal span of text sharing one style."""

    text: str
    font: str | None = None
    slant: str = Style.NORMAL
    weight: str = Weight.NORMAL
    color: str | None = None
    opacity: float = 1.0
    size_scale: float = 1.0
    rise: float = 0.0  # baseline shift, in em units


# --------------------------------------------------------------------------
# font book
# --------------------------------------------------------------------------
def _candidate_font_dirs() -> list[Path]:
    dirs: list[Path] = []
    env = os.environ.get("NEB_FONT_DIRS")
    if env:
        dirs.extend(Path(p) for p in env.split(os.pathsep) if p)
    here = Path(__file__).resolve()
    repo = here.parents[4] if len(here.parents) > 4 else here.parent
    dirs.append(repo / "tools" / "manim" / "assets" / "fonts")
    dirs.append(repo / "tools" / "video" / "assets" / "fonts")
    dirs.append(repo / "notes" / "pipeline" / "fonts")
    for extra in (
        "/usr/share/fonts",
        "/usr/local/share/fonts",
        Path.home() / ".local/share/fonts",
    ):
        dirs.append(Path(extra))
    # matplotlib ships DejaVu + STIX; useful as a last-resort fallback.
    try:
        import matplotlib

        dirs.append(Path(matplotlib.get_data_path()) / "fonts" / "ttf")
    except Exception:  # pragma: no cover
        pass
    seen, out = set(), []
    for d in dirs:
        if d not in seen:
            seen.add(d)
            out.append(d)
    return out


def _family_from_filename(stem: str) -> tuple[str, str]:
    """``Poppins-SemiBold`` -> ``("Poppins", "SemiBold")``."""
    if "-" in stem:
        family, _, sub = stem.partition("-")
        return family, sub
    return stem, ""


class _FontBook:
    """Discovers font files and resolves (family, slant, weight) to a path."""

    _instance: "_FontBook | None" = None

    def __init__(self) -> None:
        self._faces: dict[str, dict[str, str]] = {}
        self._extra: dict[str, dict[str, str]] = {}
        self._scan()

    @classmethod
    def instance(cls) -> "_FontBook":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def reset(cls) -> None:
        cls._instance = None
        _FACE_CACHE.clear()

    def _scan(self) -> None:
        for directory in _candidate_font_dirs():
            if not directory.is_dir():
                continue
            for path in sorted(directory.rglob("*")):
                if path.suffix.lower() not in (".ttf", ".otf", ".ttc"):
                    continue
                family, sub = _family_from_filename(path.stem)
                self._faces.setdefault(family, {})[sub.lower()] = str(path)

    # -- registration ---------------------------------------------------
    def add_file(self, path: str | Path) -> bool:
        path = Path(path)
        if not path.is_file():
            return False
        family, sub = _family_from_filename(path.stem)
        try:
            face = freetype.Face(str(path))
            fam = face.family_name
            if fam:
                family = fam.decode("utf-8", "replace") if isinstance(fam, bytes) else fam
        except Exception:
            pass
        self._extra.setdefault(family, {})[sub.lower()] = str(path)
        return True

    def remove_file(self, path: str | Path) -> bool:
        path = Path(path)
        family, sub = _family_from_filename(path.stem)
        table = self._extra.get(family, {})
        return table.pop(sub.lower(), None) is not None

    # -- resolution -----------------------------------------------------
    def families(self) -> list[str]:
        names = set(self._faces) | set(self._extra)
        names |= {"sans", "sans-serif", "serif", "monospace", "mono", "cursive", "fantasy"}
        return sorted(names)

    def _tables(self, family: str) -> dict[str, str]:
        low = (family or "").lower()
        for table in (self._extra, self._faces):
            for name, entries in table.items():
                if name.lower() == low:
                    return entries
        # fuzzy: family name contained in the file family
        for table in (self._extra, self._faces):
            for name, entries in table.items():
                if low and (low in name.lower() or name.lower() in low):
                    return entries
        return {}

    def resolve(self, family: str | None, slant: str, weight: str) -> str | None:
        """Return a font file path for the requested style."""
        wanted = _WEIGHT_TO_FILE.get(weight, "Regular")
        italic = slant in (Style.ITALIC, Style.OBLIQUE)

        def pick(table: dict[str, str]) -> str | None:
            if not table:
                return None
            if italic:
                for key in ("italic", "oblique", f"{wanted}italic", f"{wanted}italic"):
                    if key in table:
                        return table[key]
            if wanted in table:
                return table[wanted]
            # nearest available weight
            order = [
                "Regular", "Medium", "SemiBold", "Bold", "ExtraBold", "Black",
                "Light", "Thin",
            ]
            if wanted in order:
                idx = order.index(wanted)
                for delta in range(1, len(order)):
                    for j in (idx - delta, idx + delta):
                        if 0 <= j < len(order) and order[j] in table:
                            return table[order[j]]
            return next(iter(table.values()))

        # explicit family first
        if family:
            table = self._tables(family)
            path = pick(table)
            if path:
                return path
        # pseudo families
        low = (family or "").lower()
        if low in ("monospace", "mono", "courier", "courier new"):
            for name in ("JetBrainsMono", "DejaVuSansMono", "LiberationMono", "UbuntuMono"):
                path = pick(self._tables(name))
                if path:
                    return path
        else:
            for name in ("Poppins", "Inter", "DejaVuSans", "LiberationSans", "NotoSans"):
                path = pick(self._tables(name))
                if path:
                    return path
        return None


# --------------------------------------------------------------------------
# FreeType face cache
# --------------------------------------------------------------------------
_FACE_CACHE: dict[tuple[str, int], freetype.Face] = {}
_METRICS_CACHE: dict[tuple[str, int], tuple[float, float]] = {}
_GLYPH_CACHE: dict[tuple[str, int, int], list[tuple]] = {}


def _face(path: str, pixel_size: int) -> freetype.Face:
    key = (path, pixel_size)
    face = _FACE_CACHE.get(key)
    if face is None:
        face = freetype.Face(path)
        face.set_pixel_sizes(0, pixel_size)
        _FACE_CACHE[key] = face
    return face


def _ascent_descent(path: str, pixel_size: int) -> tuple[float, float]:
    key = (path, pixel_size)
    cached = _METRICS_CACHE.get(key)
    if cached is None:
        face = _face(path, pixel_size)
        metrics = face.size
        cached = (metrics.ascender / 64.0, -metrics.descender / 64.0)
        _METRICS_CACHE[key] = cached
    return cached


def _glyph_commands(path: str, pixel_size: int, gindex: int) -> list[tuple]:
    """Outline of one glyph as command tuples, y already flipped for SVG."""
    key = (path, pixel_size, gindex)
    cached = _GLYPH_CACHE.get(key)
    if cached is not None:
        return cached
    face = _face(path, pixel_size)
    face.load_glyph(gindex, freetype.FT_LOAD_NO_BITMAP | freetype.FT_LOAD_NO_HINTING)
    outline = face.glyph.outline
    commands: list[tuple] = []
    if outline.n_contours > 0 and outline.n_points > 0:
        points = [(p[0] / 64.0, -p[1] / 64.0) for p in outline.points]
        tags = list(outline.tags)
        contours = list(outline.contours)
        start = 0
        for end in contours:
            seg_pts = points[start : end + 1]
            seg_tags = tags[start : end + 1]
            commands.extend(_decompose_contour(seg_pts, seg_tags))
            start = end + 1
    _GLYPH_CACHE[key] = commands
    return commands


def _decompose_contour(pts: list[tuple[float, float]], tags: list[int]) -> list[tuple]:
    """TrueType contour (on/off curve points) -> SVG path commands."""
    n = len(pts)
    if n < 2:
        return []
    ons = [bool(t & 1) for t in tags]
    if not any(ons):
        return []
    if ons[0]:
        start = pts[0]
        items = list(zip(pts[1:], ons[1:]))
    else:
        # implied on-curve start: midpoint of last and first point
        start = ((pts[-1][0] + pts[0][0]) / 2.0, (pts[-1][1] + pts[0][1]) / 2.0)
        items = list(zip(pts, ons))
    commands: list[tuple] = [("M", start)]
    i = 0
    m = len(items)
    while i < m:
        pt, on = items[i]
        if on:
            commands.append(("L", pt))
            i += 1
            continue
        ctrl = pt
        if i + 1 < m:
            npt, non = items[i + 1]
            if non:
                commands.append(("Q", ctrl, npt))
                i += 2
            else:
                mid = ((ctrl[0] + npt[0]) / 2.0, (ctrl[1] + npt[1]) / 2.0)
                commands.append(("Q", ctrl, mid))
                i += 1
        else:
            commands.append(("Q", ctrl, start))
            i += 1
    commands.append(("Z",))
    return commands


def _fmt(value: float) -> str:
    text = f"{value:.2f}"
    if text == "-0.00":
        return "0.00"
    return text


def _commands_to_d(
    commands: list[tuple], dx: float, dy: float
) -> str:
    parts: list[str] = []
    for cmd in commands:
        if cmd[0] == "M":
            parts.append(f"M {_fmt(cmd[1][0] + dx)} {_fmt(cmd[1][1] + dy)}")
        elif cmd[0] == "L":
            parts.append(f"L {_fmt(cmd[1][0] + dx)} {_fmt(cmd[1][1] + dy)}")
        elif cmd[0] == "Q":
            parts.append(
                f"Q {_fmt(cmd[1][0] + dx)} {_fmt(cmd[1][1] + dy)} "
                f"{_fmt(cmd[2][0] + dx)} {_fmt(cmd[2][1] + dy)}"
            )
        elif cmd[0] == "Z":
            parts.append("Z")
    return " ".join(parts)


# --------------------------------------------------------------------------
# markup parsing
# --------------------------------------------------------------------------
_ENTITIES = {
    "&amp;": "&",
    "&lt;": "<",
    "&gt;": ">",
    "&quot;": '"',
    "&apos;": "'",
}


def _validate_markup(markup: str) -> str:
    """Return an error message, or ``''`` when the markup is acceptable."""
    if not isinstance(markup, str):
        return "markup must be a string"
    try:
        root = ET.fromstring(f"<neb-root>{markup}</neb-root>")
    except ET.ParseError as exc:
        return f"markup is not well-formed: {exc}"
    for element in root.iter():
        tag = element.tag.split("}")[-1]
        if tag not in _ALLOWED_TAGS:
            return f"unknown tag <{tag}>"
        for key in element.attrib:
            name = key.split("}")[-1]
            if name not in _ALLOWED_ATTRS:
                return f"unknown attribute '{name}' on <{tag}>"
    return ""


_ALLOWED_TAGS = {
    "neb-root", "b", "i", "u", "s", "sub", "sup", "big", "small", "tt", "span",
    "a", "mark",
}
_ALLOWED_ATTRS = {
    "foreground", "fgcolor", "color", "background", "bgcolor", "alpha",
    "font_family", "face", "font", "font_size", "size", "font_style", "style",
    "font_weight", "weight", "font_variant", "variant", "font_stretch",
    "stretch", "font_features", "features", "rise", "underline", "underline_color",
    "overline", "overline_color", "strikethrough", "strikethrough_color",
    "fallback", "lang", "letter_spacing", "line_height", "insert_hyphens",
    "allow_breaks", "text_transform", "segment", "href", "dir", "justify",
    "wrap", "ellipsize", "single_paragraph_mode", "gravity", "gravity_hint",
}


def _runs_from_markup(
    markup: str,
    default_font: str | None,
    default_slant: str,
    default_weight: str,
    default_color: str | None,
) -> list[_Run]:
    try:
        root = ET.fromstring(f"<neb-root>{markup}</neb-root>")
    except ET.ParseError:
        # fall back to treating the whole thing as plain text
        return [_Run(markup, default_font, default_slant, default_weight, default_color)]

    runs: list[_Run] = []

    def walk(node: ET.Element, style: dict) -> None:
        text = node.text or ""
        if text:
            runs.append(_Run(text, **style))
        for child in node:
            tag = child.tag.split("}")[-1]
            child_style = dict(style)
            if tag in ("b", "strong"):
                child_style["weight"] = Weight.BOLD
            elif tag in ("i", "em"):
                child_style["slant"] = Style.ITALIC
            elif tag in ("tt", "code"):
                child_style["font"] = "monospace"
            elif tag == "big":
                child_style["size_scale"] = style["size_scale"] * 1.2
            elif tag == "small":
                child_style["size_scale"] = style["size_scale"] / 1.2
            elif tag == "sub":
                child_style["rise"] = style["rise"] - 0.2
            elif tag == "sup":
                child_style["rise"] = style["rise"] + 0.35
            elif tag == "span":
                _apply_span_attributes(child, child_style)
            walk(child, child_style)
            tail = child.tail or ""
            if tail:
                runs.append(_Run(tail, **style))

    base = {
        "font": default_font,
        "slant": default_slant,
        "weight": default_weight,
        "color": default_color,
        "opacity": 1.0,
        "size_scale": 1.0,
        "rise": 0.0,
    }
    walk(root, base)
    return [r for r in runs if r.text]


def _apply_span_attributes(node: ET.Element, style: dict) -> None:
    for key, value in node.attrib.items():
        name = key.split("}")[-1].lower()
        if name in ("foreground", "fgcolor", "color"):
            style["color"] = value
        elif name == "background":
            pass  # backgrounds are not supported (Manim never asks for them)
        elif name == "alpha":
            try:
                style["opacity"] = max(0.0, min(1.0, float(value)))
            except ValueError:
                pass
        elif name == "font_family":
            style["font"] = value
        elif name == "font_style":
            style["slant"] = Style.ITALIC if value.lower() in ("italic", "oblique") else Style.NORMAL
        elif name == "font_weight":
            style["weight"] = _MARKUP_WEIGHTS.get(value.lower(), Weight.NORMAL)
        elif name == "font_size":
            scale = _parse_font_size(value)
            if scale:
                style["size_scale"] = style["size_scale"] * scale
        elif name == "rise":
            try:
                style["rise"] = style["rise"] + float(value)
            except ValueError:
                pass


def _parse_font_size(value: str) -> float | None:
    text = value.strip().lower()
    if text in ("small", "x-small", "xx-small"):
        return 0.8
    if text in ("large", "x-large", "xx-large"):
        return 1.2
    match = re.match(r"^([\d.]+)\s*(pt|px|em|%)?$", text)
    if not match:
        return None
    number = float(match.group(1))
    unit = match.group(2) or "pt"
    if unit == "%":
        return number / 100.0
    return number / 10.0  # caller scales by size/10


# --------------------------------------------------------------------------
# layout
# --------------------------------------------------------------------------
@dataclass
class _PlacedGlyph:
    d: str
    x: float
    y: float
    color: str | None
    opacity: float


def _shape_run(
    run: _Run, book: _FontBook, size: float, disable_ligatures: bool
) -> list[tuple[str, int, float, float]]:
    """Glyph placements for one run: (path, gindex, advance, rise)."""
    path = book.resolve(run.font, run.slant, run.weight)
    if path is None:
        raise RuntimeError(
            "no usable font found; put .ttf files in tools/manim/assets/fonts "
            "or set NEB_FONT_DIRS"
        )
    pixel_size = max(1, int(round(size * run.size_scale)))
    face = _face(path, pixel_size)
    out: list[tuple[str, int, float, float]] = []
    previous = 0
    for char in run.text:
        gindex = face.get_char_index(char)
        if gindex == 0 and char not in (" ", "\t", "\n"):
            # missing glyph: fall back to a visible replacement
            gindex = face.get_char_index("?")
        advance = 0.0
        if gindex:
            face.load_glyph(
                gindex, freetype.FT_LOAD_NO_BITMAP | freetype.FT_LOAD_NO_HINTING
            )
            advance = face.glyph.advance.x / 64.0
            if previous:
                kern = face.get_kerning(previous, gindex, freetype.FT_KERNING_UNFITTED)
                advance += kern.x / 64.0
        previous = gindex
        out.append((path, gindex, advance, run.rise))
    return out


def _layout(
    runs: Sequence[_Run],
    book: _FontBook,
    size: float,
    line_spacing: float,
    start_x: float,
    start_y: float,
    max_width: float,
    disable_ligatures: bool,
) -> list[_PlacedGlyph]:
    # 1. tokenise into words, honouring explicit newlines
    words: list[tuple[_Run, str]] = []
    for run in runs:
        for token in re.split(r"(\n)", run.text):
            if token == "\n":
                words.append((run, "\n"))
            elif token:
                words.append((run, token))

    # 2. greedy line breaking
    lines: list[list[tuple[_Run, str]]] = [[]]
    for run, token in words:
        if token == "\n":
            lines.append([])
            continue
        candidate = "".join(t for _, t in lines[-1]) + token
        width = _measure(candidate, lines[-1] + [(run, token)], book, size, disable_ligatures)
        if lines[-1] and width > max_width:
            lines.append([(run, token)])
        else:
            lines[-1].append((run, token))

    # 3. place glyphs
    placed: list[_PlacedGlyph] = []
    for line_num, line in enumerate(lines):
        baseline = start_y + line_spacing * line_num
        pen_x = start_x
        for run, token in line:
            path = book.resolve(run.font, run.slant, run.weight)
            if path is None:
                continue
            pixel_size = max(1, int(round(size * run.size_scale)))
            face = _face(path, pixel_size)
            previous = 0
            for char in token:
                gindex = face.get_char_index(char)
                if gindex == 0 and char not in (" ", "\t"):
                    gindex = face.get_char_index("?")
                if gindex:
                    face.load_glyph(
                        gindex, freetype.FT_LOAD_NO_BITMAP | freetype.FT_LOAD_NO_HINTING
                    )
                    commands = _glyph_commands(path, pixel_size, gindex)
                    if commands:
                        placed.append(
                            _PlacedGlyph(
                                _commands_to_d(commands, pen_x, baseline - run.rise * size),
                                pen_x,
                                baseline - run.rise * size,
                                run.color,
                                run.opacity,
                            )
                        )
                    advance = face.glyph.advance.x / 64.0
                    if previous:
                        kern = face.get_kerning(
                            previous, gindex, freetype.FT_KERNING_UNFITTED
                        )
                        advance += kern.x / 64.0
                    pen_x += advance
                    previous = gindex
                else:
                    # space / unmapped: advance without drawing
                    face.load_char(
                        char, freetype.FT_LOAD_NO_BITMAP | freetype.FT_LOAD_NO_HINTING
                    )
                    pen_x += face.glyph.advance.x / 64.0
                    previous = 0
    return placed


def _measure(
    text: str,
    line: Sequence[tuple[_Run, str]],
    book: _FontBook,
    size: float,
    disable_ligatures: bool,
) -> float:
    """Width of ``text`` laid out with the styles present in ``line``."""
    if not text:
        return 0.0
    # Fast path: measure with the style of the last run (styles rarely change
    # mid-word), which is what word wrapping actually needs.
    run = line[-1][0] if line else _Run(text)
    total = 0.0
    for glyph in _shape_run(_Run(text, run.font, run.slant, run.weight), book, size, disable_ligatures):
        total += glyph[2]
    return total


# --------------------------------------------------------------------------
# SVG writing
# --------------------------------------------------------------------------
def _write_svg(
    file_name: str,
    glyphs: Sequence[_PlacedGlyph],
    width: float,
    height: float,
) -> str:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{_fmt(width)}pt" '
        f'height="{_fmt(height)}pt" viewBox="0 0 {_fmt(width)} {_fmt(height)}">',
    ]
    for glyph in glyphs:
        attrs = f'd="{glyph.d}"'
        if glyph.color:
            attrs += f' fill="{glyph.color}"'
            if glyph.opacity < 1.0:
                attrs += f' fill-opacity="{glyph.opacity:.3f}"'
        else:
            attrs += ' fill="#000000"'
        lines.append(f"<path {attrs}/>")
    lines.append("</svg>")
    with open(file_name, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")
    return file_name


class MarkupUtils:
    @staticmethod
    def validate(markup: str) -> str:
        return _validate_markup(markup)

    @staticmethod
    def text2svg(
        text: str,
        font: str | None,
        slant: str,
        weight: str,
        size: float,
        line_spacing: float,
        disable_liga: bool,
        file_name: str,
        START_X: int,
        START_Y: int,
        width: int,
        height: int,
        *,
        justify: bool | None = None,
        indent: float | int | None = None,
        alignment=None,
        pango_width: int | None = None,
    ) -> str:
        """Render markup text to an SVG file (Pango/cairo conventions)."""
        book = _FontBook.instance()
        runs = _runs_from_markup(text, font, slant, weight, None)
        if not runs:
            runs = [_Run(" ", font, slant, weight, None)]
        first_path = book.resolve(runs[0].font, runs[0].slant, runs[0].weight)
        ascent, _ = _ascent_descent(first_path, max(1, int(round(size))))
        baseline0 = START_Y + ascent
        wrap = float(pango_width) if pango_width else float(width)
        glyphs = _layout(
            runs, book, size, line_spacing, START_X, baseline0, wrap, disable_liga
        )
        return _write_svg(file_name, glyphs, float(width), float(height))


class PangoUtils:
    @staticmethod
    def str2style(string: str) -> str:
        styles = {"NORMAL": Style.NORMAL, "ITALIC": Style.ITALIC, "OBLIQUE": Style.OBLIQUE}
        try:
            return styles[string]
        except KeyError:
            raise AttributeError("There is no Style Called %s" % string)

    @staticmethod
    def str2weight(string: str) -> str:
        weights = {name: name for name in (
            "THIN", "ULTRALIGHT", "LIGHT", "SEMILIGHT", "BOOK", "NORMAL", "MEDIUM",
            "SEMIBOLD", "BOLD", "ULTRABOLD", "HEAVY", "ULTRAHEAVY",
        )}
        try:
            return weights[string]
        except KeyError:
            raise AttributeError("There is no Font Weight Called %s" % string)

    @staticmethod
    def remove_last_M(file_name: str) -> None:
        """Remove the trailing ``M`` Pango/cairo leave in the last path."""
        with open(file_name, "r", encoding="utf-8") as handle:
            content = handle.read()
        content = re.sub(r'Z M [^A-Za-z]*? "\/>', 'Z "\/>', content)
        with open(file_name, "w", encoding="utf-8") as handle:
            handle.write(content)


def text2svg(
    settings: Sequence[TextSetting],
    size: float,
    line_spacing: float,
    disable_liga: bool,
    file_name: str,
    START_X: int,
    START_Y: int,
    width: int,
    height: int,
    orig_text: str,
    pango_width: int | None = None,
) -> str:
    """Render ``TextSetting`` spans to an SVG file (``manim.Text`` path)."""
    book = _FontBook.instance()
    first_path = None
    for setting in settings:
        first_path = book.resolve(setting.font, setting.slant, setting.weight)
        if first_path:
            break
    if first_path is None:
        first_path = book.resolve(None, Style.NORMAL, Weight.NORMAL)
    if first_path is None:
        raise RuntimeError(
            "no usable font found; put .ttf files in tools/manim/assets/fonts "
            "or set NEB_FONT_DIRS"
        )
    ascent, _ = _ascent_descent(first_path, max(1, int(round(size))))
    wrap = float(pango_width) if pango_width else float(width)

    glyphs: list[_PlacedGlyph] = []
    offset_x = 0.0
    last_line = None
    for setting in settings:
        if setting.line_num != last_line:
            offset_x = 0.0
            last_line = setting.line_num
        text = orig_text[setting.start : setting.end].replace("\n", " ")
        if not text:
            continue
        run = _Run(
            text,
            font=setting.font or None,
            slant=setting.slant,
            weight=setting.weight,
            color=setting.color,
        )
        path = book.resolve(run.font, run.slant, run.weight)
        if path is None:
            continue
        pixel_size = max(1, int(round(size)))
        face = _face(path, pixel_size)
        baseline = START_Y + ascent + line_spacing * setting.line_num
        pen_x = START_X + offset_x
        previous = 0
        for char in text:
            gindex = face.get_char_index(char)
            if gindex:
                face.load_glyph(
                    gindex, freetype.FT_LOAD_NO_BITMAP | freetype.FT_LOAD_NO_HINTING
                )
                commands = _glyph_commands(path, pixel_size, gindex)
                if commands:
                    glyphs.append(
                        _PlacedGlyph(
                            _commands_to_d(commands, pen_x, baseline),
                            pen_x,
                            baseline,
                            setting.color,
                            1.0,
                        )
                    )
                advance = face.glyph.advance.x / 64.0
                if previous:
                    kern = face.get_kerning(previous, gindex, freetype.FT_KERNING_UNFITTED)
                    advance += kern.x / 64.0
                pen_x += advance
                previous = gindex
            else:
                face.load_char(
                    char, freetype.FT_LOAD_NO_BITMAP | freetype.FT_LOAD_NO_HINTING
                )
                pen_x += face.glyph.advance.x / 64.0
                previous = 0
        offset_x = pen_x - START_X
    return _write_svg(file_name, glyphs, float(width), float(height))


def text2markup(
    text: str,
    font: str | None = None,
    slant: str = Style.NORMAL,
    weight: str = Weight.NORMAL,
) -> str:
    return text


def list_fonts() -> list[str]:
    return _FontBook.instance().families()


class _FontRegistration:
    def __init__(self, path: str, book: _FontBook):
        self.path = path
        self.book = book

    def __enter__(self) -> "_FontRegistration":
        return self

    def __exit__(self, *exc) -> None:
        self.book.remove_file(self.path)

    def __bool__(self) -> bool:
        return True


def register_font(font_file: str | Path) -> _FontRegistration:
    path = str(Path(font_file).resolve())
    book = _FontBook.instance()
    book.add_file(path)
    return _FontRegistration(path, book)


def unregister_font(font_file: str | Path) -> bool:
    return _FontBook.instance().remove_file(str(Path(font_file).resolve()))


def pango_version() -> str:
    return "1.50.14 (freetype shim)"


def cairo_version() -> str:
    return "1.18.4 (skia-raster shim)"
