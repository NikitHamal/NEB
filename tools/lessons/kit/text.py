import re

from manim import DOWN, LEFT, UP, MathTex, Tex, Text, VGroup

from . import theme as th

DEVA_RE = re.compile(r"[ऀ-ॿ]")
NE_DIGITS = str.maketrans("0123456789", "०१२३४५६७८९")


def is_deva(s):
    return bool(DEVA_RE.search(s))


def ne_num(x):
    return str(x).translate(NE_DIGITS)


def T(s, size=34, color=th.INK, weight="NORMAL", font=None, display=False, **kw):
    if font is None:
        if is_deva(s):
            font = th.DEVA
        else:
            font = th.LATIN_DISPLAY if display else th.LATIN_BODY
    if font == th.DEVA and weight in ("BOLD", "SEMIBOLD") :
        weight = "SEMIBOLD" if weight == "SEMIBOLD" else "BOLD"
    return Text(s, font=font, font_size=size, color=color, weight=weight, **kw)


def para(s, width=11.0, size=30, color=th.BODY, weight="NORMAL", line_gap=0.18, align="left", font=None):
    words = s.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        probe = T(trial, size=size, weight=weight, font=font)
        if probe.width > width and cur:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    if cur:
        lines.append(cur)
    g = VGroup(*[T(l, size=size, color=color, weight=weight, font=font) for l in lines])
    edge = LEFT if align == "left" else None
    if edge is not None:
        g.arrange(DOWN, aligned_edge=LEFT, buff=line_gap)
    else:
        g.arrange(DOWN, buff=line_gap)
    return g


def M(*tex, size=44, color=th.INK, **kw):
    return MathTex(*tex, font_size=size, color=color, **kw)


def TX(s, size=34, color=th.INK, **kw):
    return Tex(s, font_size=size, color=color, **kw)
