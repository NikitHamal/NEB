"""M3 Expressive furniture for the printed books: colour roles and the cover art.

One accent per book (spine.meta_for) is turned into the same role pairs the web
design system uses (fill + on-fill, container + on-container), so a Physics book is
the same blue family as the Physics chip in the app. Everything here is flat:
no gradients, no shadows, finite radii.
"""
import hashlib, math, os, re

HERE = os.path.dirname(os.path.abspath(__file__))


def _rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _hex(c):
    return "#%02x%02x%02x" % tuple(max(0, min(255, round(v))) for v in c)


def mix(a, b, t):
    """t of b over a."""
    A, B = _rgb(a), _rgb(b)
    return _hex([A[i] + (B[i] - A[i]) * t for i in range(3)])


def lum(h):
    def f(v):
        v /= 255
        return v / 12.92 if v <= .03928 else ((v + .055) / 1.055) ** 2.4
    r, g, b = _rgb(h)
    return .2126 * f(r) + .7152 * f(g) + .0722 * f(b)


def tones(accent):
    """Role set derived from one accent. Fill/on-fill pairs always keep contrast."""
    a = accent
    # keep the brand fill dark enough for white labels
    while lum(a) > .22:
        a = mix(a, "#000000", .12)
    return {
        "accent": a,
        "on_accent": "#ffffff",
        "container": mix("#ffffff", a, .10),
        "container_hi": mix("#ffffff", a, .20),
        "on_container": mix(a, "#000000", .52),
        "cover": mix(a, "#000000", .30),
        "cover_hi": mix(a, "#ffffff", .16),
        "cover_lo": mix(a, "#000000", .12),
        "cover_tint": mix(a, "#ffffff", .34),
        "cover_pale": mix(a, "#ffffff", .80),
    }


def css_vars(accent):
    t = tones(accent)
    return (":root{" + ";".join(f"--{k.replace('_', '-')}:{v}" for k, v in t.items()) +
            f";--accent-wash:{t['container']}}}")


# --------------------------------------------------------------------- shapes
def _poly(pts):
    return "M" + " L".join(f"{x:.2f} {y:.2f}" for x, y in pts) + " Z"


def cookie(cx, cy, r, lobes=9, depth=.075, rot=0, n=240):
    pts = []
    for i in range(n):
        th = 2 * math.pi * i / n
        rr = r * (1 + depth * math.cos(lobes * th + rot))
        pts.append((cx + rr * math.cos(th), cy + rr * math.sin(th)))
    return _poly(pts)


def squircle(cx, cy, r, p=4.2, rot=0, n=200):
    pts = []
    for i in range(n):
        th = 2 * math.pi * i / n
        c, s = math.cos(th), math.sin(th)
        x = r * math.copysign(abs(c) ** (2 / p), c)
        y = r * math.copysign(abs(s) ** (2 / p), s)
        xr = x * math.cos(rot) - y * math.sin(rot)
        yr = x * math.sin(rot) + y * math.cos(rot)
        pts.append((cx + xr, cy + yr))
    return _poly(pts)


def flower(cx, cy, r, petals=6, depth=.22, rot=0, n=300):
    return cookie(cx, cy, r, petals, depth, rot, n)


def mark_svg(fill="#ffffff", size_mm=11):
    """The flat two-tone N used as the page watermark, recoloured."""
    src = open(os.path.join(HERE, "brand", "watermark.svg"), encoding="utf-8").read()
    paths = re.findall(r'<path d="([^"]+)"', src)
    body = "".join(f'<path d="{d}" fill="{fill}" opacity="{1 if i == 0 else .72 if i == 1 else .5}"/>'
                   for i, d in enumerate(paths))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="34 26 920 1344" '
            f'style="height:{size_mm}mm;width:{size_mm * 920 / 1344:.2f}mm">{body}</svg>')


def cover_art(slug, accent):
    """Full-bleed flat cover art: big M3E shapes in tonal steps of the accent.
    Four arrangements, picked by the book slug so a shelf of books is not one picture."""
    t = tones(accent)
    k = int(hashlib.md5(slug.encode()).hexdigest(), 16) % 4
    W, H = 210, 297
    hi, lo, tint, pale = t["cover_hi"], t["cover_lo"], t["cover_tint"], t["cover_pale"]
    if k == 0:
        s = [(cookie(176, 62, 88, 9, .07, .3), hi), (squircle(26, 262, 62, 4.4, .4), lo),
             (flower(188, 258, 26, 6, .2, .2), tint), (cookie(192, 150, 12, 8, .1), pale)]
    elif k == 1:
        s = [(squircle(190, 58, 80, 4.0, .5), hi), (cookie(18, 250, 70, 10, .06), lo),
             (cookie(152, 270, 20, 7, .14, .5), tint), (flower(190, 152, 12, 5, .24), pale)]
    elif k == 2:
        s = [(flower(168, 50, 84, 7, .13, .1), hi), (squircle(30, 270, 54, 4.6, -.3), lo),
             (squircle(184, 252, 22, 3.6, .3), tint), (cookie(192, 148, 11, 9, .09), pale)]
    else:
        s = [(cookie(196, 70, 96, 12, .045, .2), hi), (flower(20, 258, 64, 8, .12, .4), lo),
             (squircle(160, 266, 22, 4.2, .6), tint), (cookie(190, 152, 12, 6, .14), pale)]
    parts = "".join(f'<path d="{d}" fill="{c}"/>' for d, c in s)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
            f'width="{W}mm" height="{H}mm" style="position:absolute;left:0;top:0">{parts}</svg>')
