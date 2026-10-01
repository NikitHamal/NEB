"""Reusable visual components for the NEBians video series.

Everything an episode needs beyond raw ``Text``/``NebMathTex``: cards, bullet
lists, key/value rows, quiz beats, and the two figures that Unit 1 actually
needs (the accuracy/precision target and the vernier calliper).  Each builder
returns plain Manim mobjects so any animation in the library works on them.
"""

from __future__ import annotations

import numpy as np
from manim import (
    DOWN,
    Table,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
    Circle,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    Line,
    Mobject,
    RoundedRectangle,
    SurroundingRectangle,
    Text,
    Transform,
    VGroup,
    Write,
)

from neb.mathtext import NebMathTex
from neb.theme import (
    ACCENT,
    ACCENT_STRONG,
    BG,
    BODY_SIZE,
    CONTENT_W,
    FONT,
    HAIRLINE,
    H1_SIZE,
    HIGHLIGHT_CYCLE,
    LEFT_EDGE,
    N,
    OUTLINE,
    RIGHT_EDGE,
    SMALL_SIZE,
    SURFACE,
    SURFACE_HIGH,
    SURFACE_RAISED,
    TEXT,
    TEXT_MUTED,
    TEXT_SECOND,
    stroke,
    TINY_SIZE,
    VIOLET,
    WARN,
    card,
    chip,
    dot,
    rule,
)


# ── Text helpers ────────────────────────────────────────────────────────────
_WIDTH_CACHE: dict = {}


def measure(text: str, size: int = BODY_SIZE, weight: str = "REGULAR") -> float:
    """Width of ``text`` in Manim units (cached; scene-build time only)."""
    key = (text, size, weight)
    if key not in _WIDTH_CACHE:
        mob = Text(text, font=FONT, weight=weight, font_size=size)
        _WIDTH_CACHE[key] = mob.width
    return _WIDTH_CACHE[key]


def wrap(text: str, width: float, size: int = BODY_SIZE, weight: str = "REGULAR") -> list[str]:
    """Greedy word wrap to ``width`` Manim units (manim 0.18 has no auto-wrap)."""
    lines, current = [], ""
    for word in text.split():
        candidate = f"{current} {word}".strip()
        if current and measure(candidate, size, weight) > width:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines


def prose(
    text: str,
    size: int = BODY_SIZE,
    color: str = TEXT,
    weight: str = "REGULAR",
    width: float | None = None,
    line_spacing: float | None = None,
    **kwargs,
) -> Text:
    """Body copy, wrapped to ``width`` Manim units when one is given."""
    if width is not None:
        text = "\n".join(wrap(text, width, size, weight))
    if line_spacing is None:
        return Text(text, font=FONT, weight=weight, font_size=size, color=color, **kwargs)
    return Text(
        text,
        font=FONT,
        weight=weight,
        font_size=size,
        color=color,
        line_spacing=line_spacing,
        **kwargs,
    )


def heading(text: str, size: int = H1_SIZE, color: str = TEXT, weight: str = "SEMIBOLD") -> Text:
    return Text(text, font=FONT, weight=weight, font_size=size, color=color)


def kicker(text: str, color: str = ACCENT, size: int = SMALL_SIZE) -> Text:
    return Text(text, font=FONT, weight="MEDIUM", font_size=size, color=color)


def caption(text: str, color: str = TEXT_MUTED, size: int = SMALL_SIZE) -> Text:
    return Text(text, font=FONT, weight="REGULAR", font_size=size, color=color)


def bullets(
    items,
    size: int = BODY_SIZE,
    color: str = TEXT,
    bullet_color: str = ACCENT,
    buff: float = 0.34,
    dot_radius: float = 0.055,
    **kwargs,
) -> VGroup:
    """A bulleted list; ``items`` are strings (or ready-made mobjects)."""
    rows = []
    for item in items:
        if isinstance(item, Mobject):
            body = item
        else:
            body = Text(
                item, font=FONT, weight="REGULAR", font_size=size, color=color, **kwargs
            )
        marker = dot(bullet_color, radius=dot_radius)
        row = VGroup(marker, body).arrange(RIGHT, buff=0.28, aligned_edge=ORIGIN)
        marker.align_to(body, UP).shift(DOWN * 0.11)
        rows.append(row)
    group = VGroup(*rows).arrange(DOWN, buff=buff, aligned_edge=LEFT)
    return group


def numbered(items, size: int = BODY_SIZE, color: str = TEXT, number_color: str = ACCENT, **kwargs):
    rows = []
    for i, item in enumerate(items, start=1):
        body = (
            item
            if isinstance(item, Mobject)
            else Text(item, font=FONT, weight="REGULAR", font_size=size, color=color, **kwargs)
        )
        num = Text(
            f"{i}", font=FONT, weight="SEMIBOLD", font_size=size, color=number_color
        )
        rows.append(VGroup(num, body).arrange(RIGHT, buff=0.3, aligned_edge=ORIGIN))
    return VGroup(*rows).arrange(DOWN, buff=0.3, aligned_edge=LEFT)


def table(
    rows,
    header: bool = True,
    font_size: int = SMALL_SIZE,
    header_size: int | None = None,
    header_color: str = ACCENT,
    body_color: str = TEXT_SECOND,
    align=LEFT,
    h_buff: float = 0.9,
    v_buff: float = 0.42,
    line_color: str = HAIRLINE,
    highlight_rows=(),
    highlight_color: str = ACCENT,
):
    """A hairline table, the notes' pipe tables in video form.

    Cells may be strings or ready-made mobjects; the first row is treated as a
    header (accent coloured, medium weight) unless ``header=False``.
    """
    header_size = header_size or font_size
    cells = []
    for r, row in enumerate(rows):
        line = []
        for cell in row:
            if isinstance(cell, Mobject):
                line.append(cell)
                continue
            if r == 0 and header:
                line.append(
                    Text(
                        cell,
                        font=FONT,
                        weight="MEDIUM",
                        font_size=header_size,
                        color=header_color,
                    )
                )
            else:
                colour = highlight_color if r in highlight_rows else body_color
                line.append(
                    Text(
                        cell,
                        font=FONT,
                        weight="REGULAR",
                        font_size=font_size,
                        color=colour,
                    )
                )
        cells.append(line)
    # manim 0.18's Table runs every cell through ``element_to_mobject``, so an
    # identity is needed to hand it mobjects we already styled ourselves.
    def _identity(item, **_):
        return item

    mob = Table(
        cells,
        element_to_mobject=_identity,
        include_outer_lines=True,
        line_config={"stroke_color": line_color, "stroke_width": stroke(1.4)},
        h_buff=h_buff,
        v_buff=v_buff,
        arrange_in_grid_config={"cell_alignment": align},
    )
    return mob


def kv_rows(rows, **kwargs):
    """Two-column key/value table (a convenience wrapper around ``table``)."""
    return table([[k, v] for k, v in rows], header=False, **kwargs)


# ── Cards ──────────────────────────────────────────────────────────────────
def panel(width: float, height: float, fill: str = SURFACE, **kwargs):
    return card(width, height, fill=fill, **kwargs)


def callout(label: str, body: str, accent: str = ACCENT, width: float = 6.0):
    """The notes' ``::: key`` / ``::: caution`` box, in video form."""
    lab = Text(label, font=FONT, weight="SEMIBOLD", font_size=SMALL_SIZE, color=accent)
    txt = prose(body, size=SMALL_SIZE, color=TEXT_SECOND, width=width - 0.9)
    inner = VGroup(lab, txt).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
    box = card(inner.width + 0.8, inner.height + 0.62, fill=SURFACE_RAISED, border=accent)
    inner.move_to(box.get_center())
    bar = RoundedRectangle(
        width=0.07,
        height=inner.height + 0.34,
        corner_radius=0.035,
        stroke_width=0,
        fill_color=accent,
        fill_opacity=1.0,
    ).move_to(box.get_left() + RIGHT * 0.14)
    return VGroup(box, bar, inner)


def equation_card(
    tex: str,
    label: str | None = None,
    width: float = 5.4,
    font_size: int = 46,
    color: str = TEXT,
    fill: str = SURFACE,
    accent: str = ACCENT,
    substrings_to_isolate=None,
    isolate_colors=None,
):
    """A centred equation in a card, with an optional label above it."""
    eq = NebMathTex(
        tex,
        color=color,
        font_size=font_size,
        substrings_to_isolate=substrings_to_isolate,
        isolate_colors=isolate_colors,
    )
    if eq.width > width - 0.9:
        eq.scale((width - 0.9) / eq.width)
    parts = [eq]
    if label:
        lab = Text(label, font=FONT, weight="MEDIUM", font_size=TINY_SIZE, color=TEXT_MUTED)
        parts.append(lab)
        inner = VGroup(eq, lab).arrange(DOWN, buff=0.26)
    else:
        inner = eq
    box = card(inner.width + 0.9, inner.height + 0.66, fill=fill, border=accent)
    inner.move_to(box.get_center())
    return VGroup(box, inner)


def highlight(
    mobject: Mobject, color: str = ACCENT, buff: float = 0.18, stroke_width: float = 3.0
):
    return SurroundingRectangle(
        mobject, color=color, buff=buff, stroke_width=stroke_width, corner_radius=0.1
    )


# ── Numbers and digits ─────────────────────────────────────────────────────
def digits(value: str, start: int, size: int = 56, weight: str = "MEDIUM"):
    """Render a number as individually addressable digit mobjects.

    ``start`` is the index of the first *significant* digit: everything from
    there on is drawn in the accent colour, everything before it (the leading
    zeros and the point) is muted.  So ``digits("0.00250", 4)`` greys out
    ``0.00`` and lights up ``250``.
    """
    group = VGroup()
    for i, ch in enumerate(value):
        colour = ACCENT if i >= start else TEXT_MUTED
        group.add(Text(ch, font=FONT, weight=weight, font_size=size, color=colour))
    group.arrange(RIGHT, buff=0.03)
    group.digit_mobs = list(group.submobjects)
    return group


# ── Figures ────────────────────────────────────────────────────────────────
def target_diagram(panel_size: float = 1.8, ring_color: str = OUTLINE, hit_color: str = TEXT_MUTED):
    """The accuracy / precision bullseye: four panels, five shots each.

    accurate + precise, precise only, accurate only, neither -- exactly the
    figure in ``notes/content/phy11/unit-01.md``.
    """
    tight = np.array(
        [[0.10, 0.16], [-0.14, 0.05], [0.04, -0.15], [0.17, -0.04], [-0.06, -0.09]]
    )
    loose = np.array(
        [[0.46, 0.50], [-0.52, 0.18], [0.10, -0.56], [0.58, -0.20], [-0.30, -0.34]]
    )
    panels = [
        ((0.0, 0.0), tight, "accurate + precise", ACCENT),
        ((0.50, 0.34), tight, "precise, not accurate", VIOLET),
        ((0.0, 0.0), loose, "accurate, not precise", ACCENT_STRONG),
        ((0.40, 0.28), loose, "neither", WARN),
    ]
    scale = panel_size / 2.4
    out = VGroup()
    for centre, offsets, title, colour in panels:
        rings = VGroup()
        for radius in (1.0, 0.66, 0.33):
            rings.add(
                Circle(
                    radius=radius * scale,
                    stroke_color=ring_color,
                    stroke_width=stroke(1.6),
                    fill_opacity=0,
                )
            )
        rings.add(
            Circle(radius=0.1 * scale, fill_color=hit_color, fill_opacity=1, stroke_width=0)
        )
        shots = VGroup()
        for dx, dy in offsets:
            shots.add(
                Dot(
                    point=[centre[0] * scale + dx * scale, centre[1] * scale + dy * scale, 0],
                    radius=0.125 * scale,
                    color=colour,
                )
            )
        label = Text(
            title, font=FONT, weight="MEDIUM", font_size=23, color=TEXT_SECOND
        )
        label.next_to(rings, DOWN, buff=0.18)
        out.add(VGroup(rings, shots, label))
    out.arrange_in_grid(rows=2, cols=2, buff=0.55)
    return out


def vernier(reading_mm: float = 13.4, width: float = 9.6):
    """A 10-division vernier calliper reading ``reading_mm`` millimetres.

    Ten vernier divisions span nine main-scale millimetres, so the least count
    is 0.1 mm: the vernier zero sits past 13 mm and its 4th division lines up.
    """
    span = 30.0  # millimetres drawn
    px_per_mm = width / span
    main = VGroup()
    ticks = VGroup()
    for mm in range(int(span) + 1):
        h = 0.62 if mm % 10 == 0 else (0.42 if mm % 5 == 0 else 0.26)
        x = mm * px_per_mm
        ticks.add(
            Line([x, 0, 0], [x, -h, 0], stroke_color=TEXT_SECOND, stroke_width=stroke(1.5))
        )
        if mm % 10 == 0:
            num = Text(str(mm // 10), font=FONT, weight="MEDIUM", font_size=22, color=TEXT_SECOND)
            num.move_to([x, 0.34, 0])
            main.add(num)
    main.add(ticks)
    spine = Line(
        [0, 0, 0], [span * px_per_mm, 0, 0], stroke_color=TEXT, stroke_width=stroke(2.6)
    )
    main.add(spine)
    main_label = caption("main scale (cm)")
    main_label.next_to(main, UP, buff=0.1).align_to(main, LEFT)

    # The vernier jaw: 10 divisions over 9 mm, zero at the reading.
    v0 = reading_mm
    vernier_span = 9.0
    vticks = VGroup()
    for k in range(11):
        x = (v0 + 0.9 * k) * px_per_mm
        vticks.add(
            Line([x, 0, 0], [x, 0.5, 0], stroke_color=ACCENT, stroke_width=stroke(1.5))
        )
    vspine = Line(
        [(v0 - 1.0) * px_per_mm, 0, 0],
        [(v0 + vernier_span + 1.0) * px_per_mm, 0, 0],
        stroke_color=ACCENT,
        stroke_width=stroke(2.6),
    )
    jaw_body = RoundedRectangle(
        width=(vernier_span + 1.6) * px_per_mm,
        height=0.5,
        corner_radius=0.08,
        stroke_color=ACCENT,
        stroke_width=stroke(1.8),
        fill_color=SURFACE_HIGH,
        fill_opacity=1.0,
    )
    jaw_body.move_to([(v0 + vernier_span / 2) * px_per_mm, -0.13, 0])
    jaw = VGroup(jaw_body, vspine, vticks)
    jaw.shift(DOWN * 0.34)

    # The coinciding division: the 4th, since 13.4 = 13 + 4 x 0.1.
    coinciding = int(round((reading_mm - int(reading_mm)) * 10))
    mark = Line(
        [(v0 + 0.9 * coinciding) * px_per_mm, -0.14, 0],
        [(v0 + 0.9 * coinciding) * px_per_mm, 0.66, 0],
        stroke_color=VIOLET,
        stroke_width=stroke(4),
    )
    mark.shift(DOWN * 0.34)
    zero = Line(
        [v0 * px_per_mm, -0.14, 0],
        [v0 * px_per_mm, 0.76, 0],
        stroke_color=ACCENT,
        stroke_width=stroke(4),
    )
    zero.shift(DOWN * 0.34)

    note = caption(
        "ten vernier divisions span nine millimetres, so the least count is 0.1 mm"
    )
    note.next_to(jaw, DOWN, buff=0.34)
    group = VGroup(main, main_label, jaw, mark, zero, note)
    group.vernier_zero = zero
    group.coincidence = mark
    group.coinciding_index = coinciding
    return group


def dimension_tag(formula: str, size: int = 34, color: str = ACCENT):
    return NebMathTex(formula, color=color, font_size=size)


# ── Quiz beat ──────────────────────────────────────────────────────────────
def quiz(
    question: str,
    options: list[str],
    correct: int,
    width: float = 7.8,
    question_size: int = 29,
    option_size: int = 25,
):
    """A multiple-choice beat: question, options, then the reveal."""
    q = prose(question, size=question_size, color=TEXT, weight="MEDIUM", width=width - 1.2)
    rows = VGroup()
    boxes, texts, badges = [], [], []
    letters = "abcd"
    for i, option in enumerate(options):
        body = Text(
            option, font=FONT, weight="REGULAR", font_size=option_size, color=TEXT_SECOND
        )
        badge = Circle(
            radius=0.165, stroke_color=OUTLINE, stroke_width=stroke(1.6), fill_opacity=0
        )
        letter = Text(
            letters[i], font=FONT, weight="SEMIBOLD", font_size=option_size - 4, color=TEXT_MUTED
        )
        badge.add(letter)
        row = VGroup(badge, body).arrange(RIGHT, buff=0.3, aligned_edge=ORIGIN)
        box = card(row.width + 0.6, row.height + 0.3, fill=SURFACE, border=HAIRLINE)
        box.move_to(row.get_center())
        rows.add(VGroup(box, badge, body))
        boxes.append(box)
        texts.append(body)
        badges.append(letter)
    rows.arrange(DOWN, buff=0.16, aligned_edge=LEFT)
    inner = VGroup(q, rows).arrange(DOWN, buff=0.34, aligned_edge=LEFT)
    outer = card(inner.width + 0.9, inner.height + 0.66, fill=BG, border=HAIRLINE)
    inner.move_to(outer.get_center())
    group = VGroup(outer, inner)
    group.question = q
    group.option_boxes = boxes
    group.option_texts = texts
    group.option_letters = badges
    group.correct = correct
    return group


def reveal_quiz(group: VGroup, correct: int | None = None):
    """Animations that mark the right answer and dim the rest."""
    correct = group.correct if correct is None else correct
    anims = []
    for i, (box, text, letter) in enumerate(
        zip(group.option_boxes, group.option_texts, group.option_letters)
    ):
        if i == correct:
            anims.append(box.animate.set_stroke(color=ACCENT, width=0.05))
            anims.append(text.animate.set_color(TEXT))
            anims.append(letter.animate.set_color(ACCENT))
        else:
            anims.append(box.animate.set_stroke(opacity=0.35))
            anims.append(text.animate.set_color(TEXT_MUTED))
            anims.append(letter.animate.set_color(TEXT_MUTED))
    return anims


# ── Title card ─────────────────────────────────────────────────────────────
def title_card(
    kicker_text: str,
    title: str,
    subtitle: str | None = None,
    accent: str = ACCENT,
):
    kick = Text(kicker_text, font=FONT, weight="MEDIUM", font_size=26, color=accent)
    main = Text(title, font=FONT, weight="BOLD", font_size=64, color=TEXT)
    parts = [kick, main]
    if subtitle:
        parts.append(
            Text(subtitle, font=FONT, weight="REGULAR", font_size=26, color=TEXT_SECOND)
        )
    group = VGroup(*parts).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
    underline = Line(
        group.get_left(),
        group.get_left() + RIGHT * 2.4,
        stroke_color=accent,
        stroke_width=stroke(4),
    ).next_to(group, DOWN, buff=0.32)
    return VGroup(group, underline)


def progress_dots(total: int, active: int, color: str = ACCENT, inactive: str = SURFACE_HIGH):
    dots = VGroup()
    for i in range(total):
        dots.add(
            dot(color if i == active else inactive, radius=0.05 if i == active else 0.038)
        )
    return dots.arrange(RIGHT, buff=0.16)
