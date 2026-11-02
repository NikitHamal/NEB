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
