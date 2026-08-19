"""Port of blobatar/src/color.ts — OKLCh palette construction + tint machinery (v2)."""

import math

try:
    _cbrt = math.cbrt
except AttributeError:  # pragma: no cover - python < 3.11
    _cbrt = lambda x: x ** (1.0 / 3.0)


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
    (0.14, (0.82, 0.17)),
    (0.3, (0.73, 0.20)),
    (0.5, (0.64, 0.22)),
    (0.7, (0.55, 0.21)),
    (0.87, (0.46, 0.18)),
    (1.0, (0.36, 0.14)),
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


def from_hex(hexstr):
    """sRGB hex -> OKLCh, as (l, c, h). The inverse of to_hex's decode."""
    n = int(hexstr[1:], 16)
    channels = []
    for shift in (16, 8, 0):
        v = (n >> shift) & 255
        s = v / 255
        channels.append(s / 12.92 if s <= 0.04045 else ((s + 0.055) / 1.055) ** 2.4)
    r, g, b = channels

    l = _cbrt(0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b)
    m = _cbrt(0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b)
    s = _cbrt(0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b)

    A = 1.9779984951 * l - 2.428592205 * m + 0.4505937099 * s
    B = 0.0259040371 * l + 0.7827717662 * m - 0.808675766 * s

    return (
        0.2104542553 * l + 0.793617785 * m - 0.0040720468 * s,
        math.hypot(A, B),
        (math.atan2(B, A) * 180) / math.pi,
    )


def mix(a, b, t):
    """Blend two Oklch colors (l, c, h) in OKLab — lerp cartesian a/b."""
    rad = lambda v: (v * math.pi) / 180
    ax = a[1] * math.cos(rad(a[2]))
    ay = a[1] * math.sin(rad(a[2]))
    bx = b[1] * math.cos(rad(b[2]))
    by = b[1] * math.sin(rad(b[2]))
    x = ax + (bx - ax) * t
    y = ay + (by - ay) * t
    return (
        a[0] + (b[0] - a[0]) * t,
        math.hypot(x, y),
        (math.atan2(y, x) * 180) / math.pi,
    )


def mix_hex(a, b, t):
    return to_hex(mix(from_hex(a), from_hex(b), t))


TINT_FLOOR = 4.55

HOT = {"h": 27, "l": 0.58, "pull": 0.6, "c": 0.18}
ROSE = {"h": 358, "l": 0.72, "pull": 0.55, "c": 0.16}
BLUSH = {"h": 12, "l": 0.84, "pull": 0.4, "c": 0.1}
BILE = {"h": 142, "l": 0.66, "pull": 0.6, "c": 0.13}


def tinted(head, eye, t):
    """The palette a tinting pose heads toward, given the pair it tints from."""
    base = from_hex(head)
    base_eye = from_hex(eye)

    hot_head = (
        base[0] + (t["l"] - base[0]) * t["pull"],
        max(base[1], t["c"]),
        t["h"],
    )
    hot_head = ensure_contrast(hot_head, DARK_SURFACE, SURFACE_FLOOR)

    hot_eye = ensure_contrast(base_eye, hot_head, TINT_FLOOR)

    direction = 1 if hot_eye[0] >= hot_head[0] else -1
    head_hex = to_hex(hot_head)
    for _pass in range(40):
        eye_hex = to_hex(hot_eye)
        worst = float("inf")
        for i in range(11):
            tt = i / 10
            worst = min(
                worst,
                contrast(
                    from_hex(mix_hex(eye, eye_hex, tt)),
                    from_hex(mix_hex(head, head_hex, tt)),
                ),
            )
        if worst >= TINT_FLOOR:
            return (head_hex, eye_hex)
        new_l = min(1, max(0, hot_eye[0] + direction * 0.02))
        if new_l == hot_eye[0]:
            return (head_hex, eye_hex)
        hot_eye = (new_l, hot_eye[1], hot_eye[2])

    return (head_hex, to_hex(hot_eye))
