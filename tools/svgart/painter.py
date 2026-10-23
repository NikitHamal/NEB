"""One drawing vocabulary, two looks.

Scenes call a Painter (`p.form`, `p.solid`, `p.line`, `p.glow`, `p.sky` ...) with colour *roles*
rather than colours; RisoPainter lights forms in stipple under a paper grain, FlatPainter gives
them a hard two-tone shade and hairline detail on a cream ground. The same scene therefore draws
in both looks, and the pixel look is made from either by pixel.py.
"""
import math

from kit import FLAT, RISO, Rng, Svg, f, hill, ridge, smooth, star_path


def shade_hex(c, k):
    """Darken (k < 1) or lighten (k > 1) a #rrggbb colour."""
    r, g, b = int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16)
    if k <= 1:
        r, g, b = r * k, g * k, b * k
    else:
        t = k - 1
        r, g, b = r + (255 - r) * t, g + (255 - g) * t, b + (255 - b) * t
    return "#%02x%02x%02x" % (max(0, min(255, int(r))), max(0, min(255, int(g))), max(0, min(255, int(b))))


class Painter:
    look = ""
    roles = {}

    def __init__(self, w, h, title, seed):
        self.s = Svg(w, h, title)
        self.rng = Rng(seed)
        self.w, self.h = w, h

    def c(self, role):
        return self.roles.get(role, role)

    # subclasses implement these
    def sky(self, kind="day"): ...
    def form(self, d, role, size=100, light=(0.35, 0.05)): ...
    def finish(self): ...

    def solid(self, d, role, op=None):
        self.s.path(d, self.c(role), op=op)

    def line(self, d, role, sw=2.0, op=None):
        self.s.path(d, stroke=self.c(role), sw=sw, op=op)

    def circle(self, x, y, r, role, op=None):
        self.s.circle(x, y, r, self.c(role), op=op)

    def disc(self, x, y, r, role, light=(0.35, 0.2)):
        self.form(circle_d(x, y, r), role, r * 2, light)

    def glow(self, x, y, r, role="a", strength=1.0):
        pass

    def svg(self):
        self.finish()
        return self.s.svg()


def circle_d(x, y, r):
    return "M%s %sa%s %s 0 1 0 %s 0a%s %s 0 1 0 %s 0Z" % (f(x - r), f(y), f(r), f(r), f(r * 2), f(r), f(r), f(-r * 2))


def rrect_d(x, y, w, h, r):
    r = min(r, w / 2, h / 2)
    return ("M%s %sh%sa%s %s 0 0 1 %s %sv%sa%s %s 0 0 1 %s %sh%sa%s %s 0 0 1 %s %sv%sa%s %s 0 0 1 %s %sZ" % (
        f(x + r), f(y), f(w - 2 * r), f(r), f(r), f(r), f(r), f(h - 2 * r), f(r), f(r), f(-r), f(r), f(-(w - 2 * r)),
        f(r), f(r), f(-r), f(-r), f(-(h - 2 * r)), f(r), f(r), f(r), f(-r)))


# ---------------------------------------------------------------- riso
class RisoPainter(Painter):
    look = "riso"
    roles = {
        "a": RISO["lemon"], "b": RISO["salmon"], "c": RISO["peri"], "d": RISO["plum"], "e": RISO["cream"],
        "f": RISO["rose"], "g": RISO["teal"], "h": RISO["peach"], "ink": RISO["ink"], "dark": RISO["periD"],
        "ground": RISO["periD"], "ground2": RISO["peri"], "page": "#fff4de", "skin": "#e8a27f", "hair": RISO["plum"],
        "leaf": RISO["teal"], "leaf2": "#5aa7a2", "brown": RISO["plumL"],
    }
    SKIES = {
        "day": (RISO["sky1"], RISO["sky2"], RISO["sky4"]),
        "dusk": (RISO["sky0"], RISO["sky2"], RISO["sky3"]),
        "night": ("#2a2560", "#4b4a9c", "#8b78bf"),
        "dawn": ("#7a7fd2", "#d7a7c9", "#f6c49c"),
        "plain": (RISO["sky1"], RISO["sky1"], RISO["sky2"]),
    }

    def sky(self, kind="dusk"):
        t, m, l = self.SKIES.get(kind, self.SKIES["dusk"])
        self.s.rect(0, 0, self.w, self.h, self.s.lin([(0, t), (0.6, m), (1, l)]))
        if kind == "night":
            self.stars(int(self.w * self.h / 9000), self.h * 0.7)

    def stars(self, n, ymax, role="e"):
        for k in range(n):
            x, y, r = self.rng.u(0, self.w), self.rng.u(0, ymax), self.rng.u(0.8, 2.0) * self.w / 1200
            if self.rng.u() < 0.12:
                self.s.path(star_path(x, y, r * 3.2, r * 0.7), self.c(role), op=0.9)
            else:
                self.s.circle(x, y, r, self.c(role), op=self.rng.u(0.35, 0.9))

    def form(self, d, role, size=100, light=(0.35, 0.05), shade=True, lit="a", strength=1.0):
        base = self.c(role)
        lightc = self.c(lit) if role != lit else "#fff7b0"
        if role in ("e", "page"):
            lightc = "#ffffff"
        self.s.path(d, base)
        cid = self.s.clip(d)
        st = self.s.stipple(max(0.6, min(1.6, size / 260)))
        lx, ly = light
        k = strength
        self.s.group(lambda: self.s.path(d, self.s.rad([(0, lightc, 0.95 * k), (0.5, lightc, 0.55 * k), (1, lightc, 0)], lx, ly, 0.75)), filt=st, clip=cid)
        if shade:
            sc = self.c("d") if role not in ("d", "ink") else "#000000"
            self.s.group(lambda: self.s.path(d, self.s.rad([(0, sc, 0.9), (0.55, sc, 0.5), (1, sc, 0)], 1 - lx * 0.6, 1.0, 0.85)), filt=st, clip=cid)

    def glow(self, x, y, r, role="a", strength=1.0):
        col = self.c(role)
        self.s.group(lambda: self.s.circle(x, y, r, self.s.rad([(0, col, min(1, strength)), (0.3, col, 0.75 * strength), (1, col, 0)])),
                     filt=self.s.stipple(max(0.7, r / 200)))

    def ground(self, y, kind="hills"):
        for k, role in enumerate(("ground2", "ground")):
            d = hill(-40, self.w + 40, self.h + 10, y + k * (self.h - y) * 0.3, self.rng, n=4)
            self.form(d, role, self.w * 0.6, light=(0.7, 0.0), shade=False, lit="h", strength=0.55)

    def mountains(self, base, peaks, role="dark", snow=True):
        d = ridge(-20, self.w + 20, base, peaks, self.rng)
        self.form(d, role, self.w * 0.5, light=(0.8, 0.0), shade=False, lit="h", strength=0.6)
        if snow:
            for px, ph, pw in peaks:
                if ph > self.h * 0.25:
                    cap = "M%s %sL%s %sL%s %sQ%s %s %s %sZ" % (f(px - pw * 0.18), f(base - ph * 0.8), f(px), f(base - ph), f(px + pw * 0.2), f(base - ph * 0.78),
                                                          f(px), f(base - ph * 0.72), f(px - pw * 0.18), f(base - ph * 0.8))
                    self.s.path(cap, self.c("e"), op=0.85)

    def detail(self, d, role="e", sw=1.5, op=0.7):
        """Hairline details are quiet in riso: thinner and softer."""
        self.s.path(d, stroke=self.c(role), sw=sw * 0.8, op=op * 0.7)

    def finish(self):
        self.s.grain_over(0.5)


# ---------------------------------------------------------------- flat
class FlatPainter(Painter):  # noqa: D101
    look = "flat"
    roles = {
        "a": FLAT["must"], "b": FLAT["coral"], "c": FLAT["lav"], "d": FLAT["vio"], "e": FLAT["cream"],
        "f": FLAT["rose"], "g": FLAT["teal"], "h": FLAT["mustL"], "ink": FLAT["ink"], "dark": FLAT["vio"],
        "ground": FLAT["olive"], "ground2": FLAT["sage"], "page": "#fffaf0", "skin": FLAT["brown"], "hair": FLAT["ink"],
        "leaf": FLAT["olive"], "leaf2": FLAT["sage"], "brown": FLAT["brown"],
    }
    SKIES = {
        "day": (FLAT["bg"], FLAT["bg"]), "dusk": ("#f8e3cc", FLAT["bg"]), "night": ("#3d3466", "#5b4d8f"),
        "dawn": ("#fde6cf", FLAT["bg"]), "plain": (FLAT["bg"], FLAT["bg"]),
    }

    def sky(self, kind="day"):
        a, b = self.SKIES.get(kind, self.SKIES["day"])
        self.s.rect(0, 0, self.w, self.h, self.s.lin([(0, a), (1, b)]) if a != b else a)
        self.night = kind == "night"
        if self.night:
            for k in range(int(self.w * self.h / 12000)):
                x, y = self.rng.u(0, self.w), self.rng.u(0, self.h * 0.7)
                if self.rng.u() < 0.2:
                    self.s.path(star_path(x, y, 6, 1.6), FLAT["mustL"])
                else:
                    self.s.circle(x, y, self.rng.u(1, 2.2), FLAT["cream"], op=0.8)
        else:
            for k in range(int(self.w * self.h / 14000)):
                self.s.circle(self.rng.u(0, self.w), self.rng.u(0, self.h), self.rng.u(1.5, 3), FLAT["bg2"])

    def form(self, d, role, size=100, light=(0.35, 0.05), shade=True, lit="a", strength=1.0):
        base = self.c(role)
        self.s.path(d, base)
        if shade:
            # the classic flat shade: the shape's own outline, nudged away from the light, kept inside it
            cid = self.s.clip(d)
            dx = (0.5 - light[0]) * size * 0.28 + size * 0.02
            dy = (0.5 - light[1]) * size * 0.16
            dk = shade_hex(base, 0.78)
            self.s.group(lambda: self.s.path(d, dk), clip=cid, tf="translate(%s %s)" % (f(dx), f(dy)))
            self.s.group(lambda: self.s.path(d, base), clip=cid, tf="translate(%s %s)" % (f(-dx * 0.05), f(-dy * 0.05)))

    def glow(self, x, y, r, role="a", strength=1.0):
        col = self.c(role)
        for k, (rr, op) in enumerate(((1.0, 0.18), (0.7, 0.22), (0.45, 0.3))):
            self.s.circle(x, y, r * rr * 0.75, col, op=op * strength)

    def ground(self, y, kind="hills"):
        for k, role in enumerate(("ground2", "ground")):
            d = hill(-40, self.w + 40, self.h + 10, y + k * (self.h - y) * 0.3, self.rng, n=4)
            self.s.path(d, self.c(role))

    def mountains(self, base, peaks, role="c", snow=True):
        d = ridge(-20, self.w + 20, base, peaks, self.rng)
        col = self.c(role) if not getattr(self, "night", False) else "#4a3d7c"
        self.s.path(d, col)
        for px, ph, pw in peaks:
            sh = "M%s %sL%s %sL%s %sZ" % (f(px), f(base - ph), f(px + pw * 0.95), f(base), f(px + pw * 0.15), f(base))
            self.s.group(lambda sh=sh: self.s.path(sh, shade_hex(col, 0.85)), clip=self.s.clip(d))
            if snow and ph > self.h * 0.25:
                cap = "M%s %sL%s %sL%s %sL%s %sL%s %sZ" % (f(px - pw * 0.2), f(base - ph * 0.78), f(px), f(base - ph), f(px + pw * 0.22), f(base - ph * 0.76),
                                                       f(px + pw * 0.06), f(base - ph * 0.82), f(px - pw * 0.06), f(base - ph * 0.74))
                self.s.path(cap, FLAT["cream"])

    def detail(self, d, role="e", sw=1.5, op=0.7):
        self.s.path(d, stroke=self.c(role), sw=sw, op=op)

    def stars(self, n, ymax, role="e"):
        for k in range(n):
            self.s.path(star_path(self.rng.u(0, self.w), self.rng.u(0, ymax), 6, 1.6), FLAT["mustL"])

    def finish(self):
        self.s.grain_over(0.16)


LOOKS = {"riso": RisoPainter, "flat": FlatPainter}
