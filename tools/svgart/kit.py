"""Drawing kit for the NEBians SVG art library.

Three looks, all plain SVG written by code:

  riso  - risograph/screen-print grain: flat monumental shapes whose light and shade fall off in
          stipple rather than smooth gradients, a soft glow, a paper grain over everything, and a
          tight palette of periwinkle, lemon, salmon-peach and plum (issue #62, first reference).
  flat  - warm editorial vector: a cream ground, organic rounded shapes, two tones per object and
          hair-thin line details (veins, folds, petals), coral, mustard, lavender, olive and sage
          (issue #62, second reference).
  pixel - the same scenes as crisp pixel art: a low-resolution canvas with ordered dithering,
          written out as merged <path> runs with crispEdges.

Everything is seeded, so a rebuild writes the same files.
"""
import math
import random

# ---------------------------------------------------------------- palettes
RISO = {
    "sky0": "#5f63b8", "sky1": "#7d7fd0", "sky2": "#b79ad0", "sky3": "#f0a184", "sky4": "#f4c09c",
    "peri": "#6c72cf", "periD": "#3f3f96", "plum": "#2c1838", "plumL": "#4a2a55",
    "lemon": "#f4e35a", "lemonD": "#e7c73e", "salmon": "#ea8f72", "peach": "#f6b994", "cream": "#f7e9d4",
    "rose": "#d9667a", "teal": "#3c8f96", "ink": "#1d1430",
}
FLAT = {
    "bg": "#fbf1dd", "bg2": "#f5e4c6", "lav": "#a99be9", "lavL": "#c5baf3", "vio": "#5b3d9e", "vioD": "#43297d",
    "must": "#f4c75e", "mustL": "#f9dc8f", "coral": "#ee8a56", "coralD": "#d06a3b", "olive": "#8eac4c", "oliveD": "#6c8a37",
    "sage": "#bdd27a", "brown": "#a86347", "brownD": "#7c3f2a", "ink": "#3b2a4a", "cream": "#fff8ea", "sky": "#cfe0e6",
    "teal": "#5aa6a0", "rose": "#e7738a",
}


class Rng:
    def __init__(self, seed):
        self.r = random.Random(seed)

    def u(self, a=0.0, b=1.0):
        return a + (b - a) * self.r.random()

    def i(self, a, b):
        return self.r.randint(a, b)

    def pick(self, xs):
        return self.r.choice(xs)


def f(v):
    """Compact number for SVG."""
    s = ("%.1f" % v).rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


class Svg:
    """An SVG under construction: defs, body, and a few filters every look shares."""

    def __init__(self, w, h, title=""):
        self.w, self.h, self.title = w, h, title
        self.defs, self.body = [], []
        self._ids = 0
        self._filters = set()

    def id(self, p="g"):
        self._ids += 1
        return "%s%d" % (p, self._ids)

    def add(self, s):
        self.body.append(s)

    def defn(self, s):
        self.defs.append(s)

    # ---- gradients
    def lin(self, stops, x1=0, y1=0, x2=0, y2=1, units="objectBoundingBox"):
        gid = self.id("l")
        st = "".join('<stop offset="%s" stop-color="%s"%s/>' % (f(o), c, (' stop-opacity="%s"' % f(a)) if a < 1 else "")
                     for o, c, a in [(s + (1,))[:3] for s in stops])
        self.defn('<linearGradient id="%s" x1="%s" y1="%s" x2="%s" y2="%s" gradientUnits="%s">%s</linearGradient>'
                  % (gid, f(x1), f(y1), f(x2), f(y2), units, st))
        return "url(#%s)" % gid

    def rad(self, stops, cx=0.5, cy=0.5, r=0.5, units="objectBoundingBox"):
        gid = self.id("r")
        st = "".join('<stop offset="%s" stop-color="%s"%s/>' % (f(o), c, (' stop-opacity="%s"' % f(a)) if a < 1 else "")
                     for o, c, a in [(s + (1,))[:3] for s in stops])
        self.defn('<radialGradient id="%s" cx="%s" cy="%s" r="%s" gradientUnits="%s">%s</radialGradient>'
                  % (gid, f(cx), f(cy), f(r), units, st))
        return "url(#%s)" % gid

    # ---- filters
    def stipple(self, scale=1.0):
        """Turns soft alpha into stipple: a gradient's falloff becomes a field of dots, the way a
        risograph lays down a tint. Use on shading and glow layers drawn with fading alpha."""
        key = "st%s" % f(scale)
        if key not in self._filters:
            self._filters.add(key)
            freq = 0.9 / scale
            self.defn(
                '<filter id="%s" x="-5%%" y="-5%%" width="110%%" height="110%%" color-interpolation-filters="sRGB">'
                '<feTurbulence type="fractalNoise" baseFrequency="%s" numOctaves="2" seed="7" result="n"/>'
                '<feColorMatrix in="n" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1.6 0 0 0 -0.3" result="na"/>'
                '<feComposite in="SourceAlpha" in2="na" operator="arithmetic" k1="0" k2="1" k3="1" k4="-0.5" result="s"/>'
                '<feComponentTransfer in="s" result="m"><feFuncA type="linear" slope="14" intercept="-7"/></feComponentTransfer>'
                '<feComponentTransfer in="SourceGraphic" result="o"><feFuncA type="linear" slope="0" intercept="1"/></feComponentTransfer>'
                '<feComposite in="o" in2="m" operator="in"/></filter>' % (key, f(freq)))
        return "url(#%s)" % key

    def paper(self):
        """A fine paper grain laid over the whole picture."""
        if "paper" not in self._filters:
            self._filters.add("paper")
            self.defn(
                '<filter id="paper" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB">'
                '<feTurbulence type="fractalNoise" baseFrequency="1.1" numOctaves="2" seed="3" stitchTiles="stitch"/>'
                '<feColorMatrix type="matrix" values="0 0 0 0 0.1 0 0 0 0 0.05 0 0 0 0 0.15 0 0 0 -2.2 1.35"/>'
                '</filter>')
        return "url(#paper)"

    def soft(self, sd=6):
        key = "bl%s" % f(sd)
        if key not in self._filters:
            self._filters.add(key)
            self.defn('<filter id="%s" x="-30%%" y="-30%%" width="160%%" height="160%%"><feGaussianBlur stdDeviation="%s"/></filter>' % (key, f(sd)))
        return "url(#%s)" % key

    # ---- drawing
    def path(self, d, fill="none", stroke=None, sw=None, op=None, filt=None, extra=""):
        a = ['d="%s"' % d, 'fill="%s"' % fill]
        if stroke:
            a.append('stroke="%s"' % stroke)
            a.append('stroke-width="%s" stroke-linecap="round" stroke-linejoin="round"' % f(sw or 1))
        if op is not None and op < 1:
            a.append('opacity="%s"' % f(op))
        if filt:
            a.append('filter="%s"' % filt)
        self.add("<path %s%s/>" % (" ".join(a), extra))

    def rect(self, x, y, w, h, fill, rx=0, op=None, filt=None):
        self.add('<rect x="%s" y="%s" width="%s" height="%s"%s fill="%s"%s%s/>' % (
            f(x), f(y), f(w), f(h), (' rx="%s"' % f(rx)) if rx else "", fill,
            (' opacity="%s"' % f(op)) if op is not None and op < 1 else "", (' filter="%s"' % filt) if filt else ""))

    def circle(self, cx, cy, r, fill, op=None, filt=None, stroke=None, sw=None):
        self.add('<circle cx="%s" cy="%s" r="%s" fill="%s"%s%s%s/>' % (
            f(cx), f(cy), f(r), fill, (' opacity="%s"' % f(op)) if op is not None and op < 1 else "",
            (' filter="%s"' % filt) if filt else "",
            (' stroke="%s" stroke-width="%s"' % (stroke, f(sw or 1))) if stroke else ""))

    def ellipse(self, cx, cy, rx, ry, fill, op=None, filt=None, rot=0):
        self.add('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s"%s%s%s/>' % (
            f(cx), f(cy), f(rx), f(ry), fill, (' opacity="%s"' % f(op)) if op is not None and op < 1 else "",
            (' filter="%s"' % filt) if filt else "", (' transform="rotate(%s %s %s)"' % (f(rot), f(cx), f(cy))) if rot else ""))

    def group(self, inner, filt=None, clip=None, op=None, tf=None):
        """A group. A clip stays put when the content is transformed: the clip sits on an outer
        group and the transform on an inner one (on one element the clip would move too)."""
        a = []
        if filt: a.append('filter="%s"' % filt)
        if clip: a.append('clip-path="url(#%s)"' % clip)
        if op is not None and op < 1: a.append('opacity="%s"' % f(op))
        if tf and not clip: a.append('transform="%s"' % tf)
        self.add("<g %s>" % " ".join(a))
        if tf and clip:
            self.add('<g transform="%s">' % tf)
        inner()
        if tf and clip:
            self.add("</g>")
        self.add("</g>")

    def clip(self, d):
        cid = self.id("c")
        self.defn('<clipPath id="%s"><path d="%s"/></clipPath>' % (cid, d))
        return cid

    def grain_over(self, op=0.55):
        self.rect(0, 0, self.w, self.h, "#000", filt=self.paper(), op=op)

    def svg(self):
        t = ("<title>%s</title>" % self.title) if self.title else ""
        return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d">%s<defs>%s</defs>%s</svg>'
                % (self.w, self.h, self.w, self.h, t, "".join(self.defs), "".join(self.body)))


# ---------------------------------------------------------------- shape helpers
def blob(cx, cy, rx, ry, rng, n=9, wob=0.12, rot=0.0):
    """A soft closed organic shape through n points, smoothed with cubic Beziers."""
    pts = []
    for k in range(n):
        a = rot + k / n * 2 * math.pi
        r = 1 + rng.u(-wob, wob)
        pts.append((cx + math.cos(a) * rx * r, cy + math.sin(a) * ry * r))
    return smooth(pts, closed=True)


def smooth(pts, closed=False, t=0.18):
    """Catmull-Rom through pts as cubic Beziers."""
    n = len(pts)
    if n < 2:
        return ""
    d = "M%s %s" % (f(pts[0][0]), f(pts[0][1]))
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        p0 = pts[(i - 1) % n] if (closed or i > 0) else pts[i]
        p1 = pts[i]
        p2 = pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) * t * 2, p1[1] + (p2[1] - p0[1]) * t * 2)
        c2 = (p2[0] - (p3[0] - p1[0]) * t * 2, p2[1] - (p3[1] - p1[1]) * t * 2)
        d += "C%s %s %s %s %s %s" % (f(c1[0]), f(c1[1]), f(c2[0]), f(c2[1]), f(p2[0]), f(p2[1]))
    return d + ("Z" if closed else "")


def ridge(x0, x1, base, peaks, rng, jag=0.25, steps=60):
    """A mountain range silhouette: the skyline of overlapping peaks (x, height, width), closed to base."""
    pts = []
    for k in range(steps + 1):
        x = x0 + (x1 - x0) * k / steps
        y = 0.0
        for px, ph, pw in peaks:
            d = abs(x - px) / pw
            y = max(y, ph * max(0.0, 1 - d) ** 1.15)
        y *= 1 + rng.u(-jag, jag) * 0.15
        pts.append((x, base - y))
    d = "M%s %s" % (f(x0), f(base))
    d += "".join("L%s %s" % (f(x), f(y)) for x, y in pts)
    return d + "L%s %sZ" % (f(x1), f(base))


def hill(x0, x1, base, top, rng, n=6):
    """A rolling hill band: a smooth crest at about [top] (sum of two slow waves), filled to below [base]."""
    ph1, ph2, amp = rng.u(0, 6.28), rng.u(0, 6.28), (base - top) * 0.18
    pts = []
    for k in range(n * 4 + 1):
        x = x0 + (x1 - x0) * k / (n * 4)
        t = (x - x0) / (x1 - x0)
        pts.append((x, top + amp * math.sin(t * 6.28 * 0.9 + ph1) + amp * 0.5 * math.sin(t * 6.28 * 2.1 + ph2)))
    d = smooth(pts)
    return d + "L%s %sL%s %sZ" % (f(x1), f(base + 400), f(x0), f(base + 400))


def leaf(x, y, length, width, angle):
    """A pointed leaf from its base (x, y) along angle (degrees): returns (outline, midrib)."""
    a = math.radians(angle)
    tx, ty = x + math.cos(a) * length, y + math.sin(a) * length
    nx, ny = -math.sin(a) * width, math.cos(a) * width
    m1 = (x + math.cos(a) * length * 0.45, y + math.sin(a) * length * 0.45)
    d = ("M%s %s" % (f(x), f(y)) +
         "Q%s %s %s %s" % (f(m1[0] + nx), f(m1[1] + ny), f(tx), f(ty)) +
         "Q%s %s %s %sZ" % (f(m1[0] - nx), f(m1[1] - ny), f(x), f(y)))
    rib = "M%s %sQ%s %s %s %s" % (f(x), f(y), f(m1[0] + nx * 0.15), f(m1[1] + ny * 0.15), f(tx - math.cos(a) * length * 0.1), f(ty - math.sin(a) * length * 0.1))
    return d, rib


def petal_flower(cx, cy, r, n, rot=0.0, pr=0.42):
    """A cup flower seen from the side-ish: n rounded petals fanned upward. Returns petal paths."""
    out = []
    for k in range(n):
        a = math.radians(rot - 150 + 120 * k / max(1, n - 1))
        tx, ty = cx + math.cos(a) * r, cy + math.sin(a) * r
        nx, ny = -math.sin(a) * r * pr, math.cos(a) * r * pr
        out.append("M%s %sQ%s %s %s %sQ%s %s %s %sZ" % (
            f(cx), f(cy), f(cx + (tx - cx) * 0.6 + nx), f(cy + (ty - cy) * 0.6 + ny), f(tx), f(ty),
            f(cx + (tx - cx) * 0.6 - nx), f(cy + (ty - cy) * 0.6 - ny), f(cx), f(cy)))
    return out


def star_path(cx, cy, r1, r2, n=4, rot=-90):
    pts = []
    for k in range(n * 2):
        r = r1 if k % 2 == 0 else r2
        a = math.radians(rot + 180 * k / n)
        pts.append("%s %s" % (f(cx + math.cos(a) * r), f(cy + math.sin(a) * r)))
    return "M" + "L".join(pts) + "Z"
