"""Tiny SVG diagram kit for authored ```svgfig blocks (boxes, arrows, labels, plain shapes).

Arrowheads are drawn as polygons (no <marker>), so every renderer shows them. Text is wrapped by
hand with newlines; Fig.lint() estimates text width and reports labels that overflow their box."""
import html, math

NAVY, SLATE, TEAL, AMBER, RED = "#1e3a8a", "#334155", "#0f766e", "#b45309", "#b91c1c"
SOFT, BLUE, MINT, SAND, ROSE = "#f8fafc", "#eff6ff", "#ecfdf5", "#fffbeb", "#fef2f2"
FONT = "Inter, 'DejaVu Sans', Arial, sans-serif"
WARN = []


def _e(s):
    return html.escape(str(s), quote=False)


class Fig:
    def __init__(self, w, h, name=""):
        self.w, self.h, self.name, self.o, self.boxes = w, h, name, [], []

    def box(self, x, y, w, h, label="", fill=BLUE, stroke=NAVY, color=None, size=11, bold=False,
            r=6, dash=False, sw=1.4, anchor="middle"):
        d = ' stroke-dasharray="5 3"' if dash else ""
        self.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" '
                      f'stroke="{stroke}" stroke-width="{sw}"{d}/>')
        if label:
            tx = x + w / 2 if anchor == "middle" else x + 8
            self.text(tx, y + h / 2, label, size=size, color=color or stroke, bold=bold,
                      anchor=anchor, vmid=True)
            self.boxes.append((label, w, h, size, bold))
        return self

    def text(self, x, y, s, size=11, color=SLATE, bold=False, anchor="middle", vmid=False, italic=False):
        lines = str(s).split("\n")
        lh = size * 1.22
        y0 = y - (len(lines) - 1) * lh / 2 + (size * 0.35 if vmid else 0)
        wt = ' font-weight="700"' if bold else ""
        it = ' font-style="italic"' if italic else ""
        for i, ln in enumerate(lines):
            self.o.append(f'<text x="{x}" y="{y0 + i * lh:.1f}" font-family="{FONT}" font-size="{size}" '
                          f'fill="{color}" text-anchor="{anchor}"{wt}{it}>{_e(ln)}</text>')
        return self

    def line(self, x1, y1, x2, y2, color=SLATE, sw=1.4, dash=False):
        d = ' stroke-dasharray="5 3"' if dash else ""
        self.o.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{sw}"{d}/>')
        return self

    def arrow(self, pts, color=SLATE, sw=1.5, dash=False, both=False, label=None, lpos=None, lsize=9.5,
              lcolor=None):
        d = ' stroke-dasharray="5 3"' if dash else ""
        P = list(pts)

        def head(p, q):
            ang = math.atan2(q[1] - p[1], q[0] - p[0])
            L, W = 9, 4.2
            bx, by = q[0] - L * math.cos(ang), q[1] - L * math.sin(ang)
            a = (bx - W * math.sin(ang), by + W * math.cos(ang))
            b = (bx + W * math.sin(ang), by - W * math.cos(ang))
            self.o.append(f'<polygon points="{q[0]},{q[1]} {a[0]:.1f},{a[1]:.1f} {b[0]:.1f},{b[1]:.1f}" fill="{color}"/>')
            return bx, by
        e = list(P)
        e[-1] = head(P[-2], P[-1])
        if both:
            e[0] = head(P[1], P[0])
        self.o.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="%s"%s/>' % (
            " ".join(f"{a:.1f},{b:.1f}" for a, b in e), color, sw, d))
        if label:
            lx, ly = lpos or ((P[0][0] + P[-1][0]) / 2, (P[0][1] + P[-1][1]) / 2 - 5)
            self.text(lx, ly, label, size=lsize, color=lcolor or color, bold=True)
        return self

    def circle(self, cx, cy, r, fill=BLUE, stroke=NAVY, sw=1.4, label="", size=10, color=None, bold=True):
        self.o.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
        if label:
            self.text(cx, cy, label, size=size, color=color or stroke, bold=bold, vmid=True)
        return self

    def poly(self, pts, fill=BLUE, stroke=NAVY, sw=1.4, label="", lx=None, ly=None, size=11, color=None, bold=True):
        self.o.append('<polygon points="%s" fill="%s" stroke="%s" stroke-width="%s"/>' % (
            " ".join(f"{a},{b}" for a, b in pts), fill, stroke, sw))
        if label:
            self.text(lx, ly, label, size=size, color=color or stroke, bold=bold, vmid=True)
        return self

    def raw(self, s):
        self.o.append(s)
        return self

    def lint(self):
        for label, w, h, size, bold in self.boxes:
            ls = label.split("\n")
            tw = max(len(x) for x in ls) * size * (0.60 if bold else 0.56)
            if tw > w - 6 or len(ls) * size * 1.22 > h - 2:
                WARN.append(f"{self.name}: label may overflow its box ({w}x{h}): {label[:40]!r}")

    def svg(self):
        self.lint()
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" '
                f'width="{self.w}" height="{self.h}">'
                f'<rect x="0" y="0" width="{self.w}" height="{self.h}" fill="#ffffff"/>'
                + "".join(self.o) + "</svg>")


def render(code, name=""):
    ns = {k: v for k, v in globals().items() if not k.startswith("__")}
    ns["__name__"] = "svgfig"
    exec(code, ns)
    f = ns.get("f")
    if not isinstance(f, Fig):
        raise ValueError("svgfig code must assign a Fig to `f`")
    f.name = name or f.name
    return f.svg()


class Axes:
    """Cartesian plot area inside a Fig: Axes(f, left, top, w, h, (xmin, xmax), (ymin, ymax)).

    ax.grid(dx, dy) / ax.axes(...) draw the frame; ax.curve(fn, a, b) plots y = fn(x) and breaks the
    line at poles; ax.area(fn, a, b) shades under a curve; ax.pt / ax.hline / ax.vline / ax.tag add marks.
    """

    def __init__(self, f, left, top, w, h, xr, yr, name=""):
        self.f, self.l, self.t, self.w, self.h = f, left, top, w, h
        self.x0, self.x1 = xr
        self.y0, self.y1 = yr

    def X(self, x):
        return round(self.l + (x - self.x0) / (self.x1 - self.x0) * self.w, 2)

    def Y(self, y):
        return round(self.t + self.h - (y - self.y0) / (self.y1 - self.y0) * self.h, 2)

    def grid(self, dx=1, dy=1, labels=True, size=9.5, xfmt=None, yfmt=None):
        f = self.f
        fx = xfmt or (lambda v: f"{v:g}")
        fy = yfmt or (lambda v: f"{v:g}")
        k = math.ceil(self.x0 / dx - 1e-9)
        while k * dx <= self.x1 + 1e-9:
            x = k * dx
            f.line(self.X(x), self.Y(self.y0), self.X(x), self.Y(self.y1), color="#e2e8f0", sw=0.8)
            if labels and abs(x) > 1e-9:
                f.text(self.X(x), self.Y(max(self.y0, min(0, self.y1))) + 13, fx(x), size=size, color=SLATE)
            k += 1
        k = math.ceil(self.y0 / dy - 1e-9)
        while k * dy <= self.y1 + 1e-9:
            y = k * dy
            f.line(self.X(self.x0), self.Y(y), self.X(self.x1), self.Y(y), color="#e2e8f0", sw=0.8)
            if labels and abs(y) > 1e-9:
                f.text(self.X(max(self.x0, min(0, self.x1))) - 5, self.Y(y) + 3.5, fy(y), size=size, color=SLATE, anchor="end")
            k += 1
        return self

    def axes(self, xl="x", yl="y", color=SLATE):
        f = self.f
        ya = self.Y(max(self.y0, min(0, self.y1)))
        xa = self.X(max(self.x0, min(0, self.x1)))
        f.arrow([(self.X(self.x0), ya), (self.X(self.x1) + 6, ya)], color=color, sw=1.4)
        f.arrow([(xa, self.Y(self.y0)), (xa, self.Y(self.y1) - 6)], color=color, sw=1.4)
        f.text(self.X(self.x1) + 4, ya - 7, xl, size=11, color=color, italic=True, anchor="end")
        f.text(xa + 8, self.Y(self.y1) + 2, yl, size=11, color=color, italic=True, anchor="start")
        return self

    def _pts(self, fn, a, b, n):
        segs, cur = [], []
        lim = (self.y1 - self.y0) * 1.5
        for i in range(n + 1):
            x = a + (b - a) * i / n
            try:
                y = fn(x)
                ok = isinstance(y, (int, float)) and abs(y) < 1e6 and self.y0 - lim < y < self.y1 + lim
            except (ZeroDivisionError, ValueError, OverflowError):
                ok = False
            if ok:
                y = max(self.y0 - lim, min(self.y1 + lim, y))
                cur.append((self.X(x), self.Y(y)))
            elif cur:
                segs.append(cur)
                cur = []
        if cur:
            segs.append(cur)
        return segs

    def curve(self, fn, a=None, b=None, color=NAVY, sw=2.2, dash=False, n=240, label=None, lx=None, ly=None, lsize=11):
        a = self.x0 if a is None else a
        b = self.x1 if b is None else b
        d = ' stroke-dasharray="6 4"' if dash else ""
        for seg in self._pts(fn, a, b, n):
            if len(seg) > 1:
                p = " ".join(f"{x},{y}" for x, y in seg)
                self.f.raw(f'<clipPath id="c{id(self)}"><rect x="{self.l}" y="{self.t}" width="{self.w}" height="{self.h}"/></clipPath>'
                           f'<polyline points="{p}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linejoin="round" '
                           f'clip-path="url(#c{id(self)})"{d}/>')
        if label:
            self.f.text(lx, ly, label, size=lsize, color=color, bold=True, anchor="start")
        return self

    def area(self, fn, a, b, fill="#bfdbfe", opacity=0.75, n=120, fn2=None):
        top = [(self.X(a + (b - a) * i / n), self.Y(fn(a + (b - a) * i / n))) for i in range(n + 1)]
        g = fn2 or (lambda x: 0)
        bot = [(self.X(a + (b - a) * i / n), self.Y(g(a + (b - a) * i / n))) for i in range(n, -1, -1)]
        p = " ".join(f"{x},{y}" for x, y in top + bot)
        self.f.raw(f'<polygon points="{p}" fill="{fill}" fill-opacity="{opacity}" stroke="none"/>')
        return self

    def bars(self, fn, a, b, n, mode="left", fill="#fde68a", stroke=AMBER):
        dx = (b - a) / n
        for i in range(n):
            xl = a + i * dx
            h = fn(xl if mode == "left" else xl + dx if mode == "right" else xl + dx / 2)
            self.f.raw(f'<rect x="{self.X(xl)}" y="{min(self.Y(h), self.Y(0))}" width="{round(self.X(xl + dx) - self.X(xl), 2)}" '
                       f'height="{round(abs(self.Y(0) - self.Y(h)), 2)}" fill="{fill}" fill-opacity="0.8" stroke="{stroke}" stroke-width="1"/>')
        return self

    def pt(self, x, y, label="", r=4.2, color=RED, dx=8, dy=-8, size=10.5, anchor="start", hollow=False):
        self.f.raw(f'<circle cx="{self.X(x)}" cy="{self.Y(y)}" r="{r}" fill="{"#fff" if hollow else color}" stroke="{color}" stroke-width="1.8"/>')
        if label:
            self.f.text(self.X(x) + dx, self.Y(y) + dy, label, size=size, color=color, bold=True, anchor=anchor)
        return self

    def hline(self, y, x0=None, x1=None, color=AMBER, dash=True, sw=1.4):
        x0 = self.x0 if x0 is None else x0
        x1 = self.x1 if x1 is None else x1
        self.f.line(self.X(x0), self.Y(y), self.X(x1), self.Y(y), color=color, sw=sw, dash=dash)
        return self

    def vline(self, x, y0=None, y1=None, color=AMBER, dash=True, sw=1.4):
        y0 = self.y0 if y0 is None else y0
        y1 = self.y1 if y1 is None else y1
        self.f.line(self.X(x), self.Y(y0), self.X(x), self.Y(y1), color=color, sw=sw, dash=dash)
        return self

    def tag(self, x, y, s, size=10.5, color=SLATE, bold=False, anchor="middle"):
        self.f.text(self.X(x), self.Y(y), s, size=size, color=color, bold=bold, anchor=anchor)
        return self
