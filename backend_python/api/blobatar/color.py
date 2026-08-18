"""Port of blobatar/src/color.ts — OKLCh palette construction."""

import math


def _to_linear(l, c, h):
    r = (h * math.pi) / 180
    a = c * math.cos(r)
    b = c * math.sin(r)

    l_ = l + 0.3963377774 * a + 0.2158037573 * b
    m_ = l - 0.1055613458 * a - 0.0638541728 * b
    s_ = l - 0.0894841775 * a - 1.291485548 * b

    L = l_ * l_ * l_
    M = m_ * m_ * m_
    S = s_ * s_ * s_

    return [
        4.0767416621 * L - 3.3077115913 * M + 0.2309699292 * S,
        -1.2684380046 * L + 2.6097574011 * M - 0.3413193965 * S,
        -0.0041960863 * L - 0.7034186147 * M + 1.707614701 * S,
    ]


def _in_gamut(rgb):
    return all(-1e-4 <= v <= 1 + 1e-4 for v in rgb)


def _resolve(color):
    l, c, h = color
    rgb = _to_linear(l, c, h)
    if not _in_gamut(rgb):
        lo = 0
        hi = c
        for _ in range(12):
            mid = (lo + hi) / 2
            if _in_gamut(_to_linear(l, mid, h)):
                lo = mid
            else:
                hi = mid
        rgb = _to_linear(l, lo, h)
    return [min(1, max(0, v)) for v in rgb]


def _luminance(color):
    l, c, h = color
    r, g, b = _resolve((l, c, h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    x = _luminance(a)
    y = _luminance(b)
    return (max(x, y) + 0.05) / (min(x, y) + 0.05)


def ensure_contrast(fg, bg, minimum):
    if contrast(fg, bg) >= minimum:
        return fg

    lean = 1 if fg[0] >= bg[0] else -1
    for direction in (lean, -lean):
        probe = list(fg)
        for _ in range(60):
            probe[0] = min(1, max(0, probe[0] + direction * 0.02))
            if contrast(tuple(probe), bg) >= minimum:
                return tuple(probe)
            if probe[0] == 0 or probe[0] == 1:
                break

    black = (0, 0, fg[2])
    white = (1, 0, fg[2])
    return black if contrast(black, bg) >= contrast(white, bg) else white


def to_hex(color):
    out = "#"
    for v in _resolve(color):
        s = 12.92 * v if v <= 0.0031308 else 1.055 * math.pow(v, 1 / 2.4) - 0.055
        out += format(math.floor(s * 255 + 0.5), "02x")
    return out


TONES = [
    (0.2, (0.86, 0.085)),
    (0.36, (0.9, 0.028)),
    (0.62, (0.73, 0.135)),
    (0.8, (0.62, 0.165)),
    (0.93, (0.87, 0.16)),
    (1.0, (0.34, 0.035)),
]


def _tone_at(v):
    for edge, tone in TONES:
        if v < edge:
            return tone
    return TONES[0][1]


DARK_SURFACE = (0.145, 0, 0)
SURFACE_FLOOR = 1.5

FLOORS = [
    ("head", "bg", 1.25),
    ("eye", "head", 4.5),
]


def ramp(hue, enforce=True, tone=0):
    t = _tone_at(tone)
    head = ensure_contrast((t[0], t[1], hue), DARK_SURFACE, SURFACE_FLOOR)
    r = {
        "bg": (0.965, 0.01, hue),
        "head": head,
        "eye": (0.17, 0.02, hue) if head[0] >= 0.5 else (0.97, 0.012, hue),
    }
    if enforce:
        for fg, bg, minimum in FLOORS:
            r[fg] = ensure_contrast(r[fg], r[bg], minimum)
    return r


def palette(hue, enforce=True, tone=0):
    return {k: to_hex(v) for k, v in ramp(hue, enforce, tone).items()}
