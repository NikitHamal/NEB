"""Circuit-diagram helpers for ```figure blocks (resistor, inductor, capacitor, sources, diodes...).

Usage inside a figure block (all names are injected, no import needed):

    fig, ax = ckt_canvas(6, 3.4)                  # axes in data units, axis off, equal aspect
    wire(ax, [(0,0),(0,3),(2,3)])                 # polyline
    res(ax, (2,3), (4,3), "5 Ω")                  # two-terminal elements: a -> b
    vsrc(ax, (0,0), (0,3), "12 V")                # circle source, + toward b
    batt(ax, (0,0), (0,3), "12 V")                # battery, + (long plate) toward b
    isrc(ax, (0,0), (0,3), "3 A")                 # current source, arrow a -> b
    node(ax, (2,3)); gnd(ax, (2,0)); label(ax, (1,1), "I$_1$")
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as _mp

_INK = "#14181f"
_LW = 1.5


def ckt_canvas(w, h, xlim=None, ylim=None):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_aspect("equal")
    ax.axis("off")
    if xlim:
        ax.set_xlim(*xlim)
    if ylim:
        ax.set_ylim(*ylim)
    return fig, ax


def _frame(a, b, body=1.0):
    a = np.array(a, float)
    b = np.array(b, float)
    d = b - a
    n = np.hypot(*d)
    u = d / n
    v = np.array([-u[1], u[0]])
    mid = (a + b) / 2
    s = mid - u * body / 2
    e = mid + u * body / 2
    return a, b, u, v, mid, s, e


def _pl(ax, pts, **kw):
    pts = np.array(pts)
    kw.setdefault("color", _INK)
    kw.setdefault("lw", _LW)
    kw.setdefault("solid_capstyle", "round")
    kw.setdefault("solid_joinstyle", "round")
    ax.plot(pts[:, 0], pts[:, 1], **kw)


def wire(ax, pts):
    _pl(ax, pts)


def node(ax, p, r=4.2):
    ax.plot([p[0]], [p[1]], "o", color=_INK, ms=r, zorder=5)


def terminal(ax, p):
    ax.plot([p[0]], [p[1]], "o", mfc="white", mec=_INK, ms=5, mew=1.3, zorder=5)


def label(ax, p, text, size=8.4, ha="center", va="center", color=_INK, **kw):
    ax.text(p[0], p[1], text, ha=ha, va=va, fontsize=size, color=color, **kw)


def _lab(ax, mid, v, text, side, off=0.42, size=8.4):
    if text:
        q = mid + v * side * off
        ax.text(q[0], q[1], text, ha="center", va="center", fontsize=size, color=_INK)


def res(ax, a, b, text=None, side=1, body=1.0, off=0.40):
    a, b, u, v, mid, s, e = _frame(a, b, body)
    _pl(ax, [a, s]); _pl(ax, [e, b])
    n = 6
    t = np.linspace(0, 1, 2 * n + 1)
    pts = [s]
    for i in range(1, 2 * n):
        amp = 0.17 * (1 if i % 2 else -1)
        pts.append(s + u * body * t[i] + v * amp)
    pts.append(e)
    _pl(ax, pts)
    _lab(ax, mid, v, text, side, off)


def ind(ax, a, b, text=None, side=1, body=1.2, off=0.42):
    a, b, u, v, mid, s, e = _frame(a, b, body)
    _pl(ax, [a, s]); _pl(ax, [e, b])
    loops = 4
    r = body / loops / 2
    pts = []
    for k in range(loops):
        c = s + u * (r + 2 * r * k)
        for q in np.linspace(np.pi, 0, 20):
            pts.append(c + u * r * np.cos(q) + v * r * 1.15 * np.sin(q))
    _pl(ax, pts)
    _lab(ax, mid, v, text, side, off)


def cap(ax, a, b, text=None, side=1, gap=0.26, off=0.5):
    a, b, u, v, mid, s, e = _frame(a, b, gap)
    _pl(ax, [a, s]); _pl(ax, [e, b])
    for p in (s, e):
        _pl(ax, [p - v * 0.4, p + v * 0.4], lw=2.2)
    _lab(ax, mid, v, text, side, off)


def batt(ax, a, b, text=None, side=1, cells=1, off=0.8):
    """Battery; the long plate (+) is nearer to b. The label goes on `side`, the +/- marks on the other."""
    body = 0.26 * (2 * cells - 1)
    a, b, u, v, mid, s, e = _frame(a, b, body)
    _pl(ax, [a, s]); _pl(ax, [e, b])
    for k in range(2 * cells):
        p = s + u * 0.26 * k
        long_ = (k % 2 == 1)
        h = 0.42 if long_ else 0.24
        _pl(ax, [p - v * h, p + v * h], lw=2.2 if long_ else 3.2)
    sv = -side * v
    ax.text(*(e + u * 0.05 + sv * 0.52), "+", fontsize=8, ha="center", va="center", color=_INK)
    ax.text(*(s - u * 0.05 + sv * 0.52), "−", fontsize=8, ha="center", va="center", color=_INK)
    _lab(ax, mid, v, text, side, off)


def vsrc(ax, a, b, text=None, side=1, r=0.34, off=0.62, signs=True):
    a, b, u, v, mid, s, e = _frame(a, b, 2 * r)
    _pl(ax, [a, s]); _pl(ax, [e, b])
    ax.add_patch(_mp.Circle(mid, r, fc="white", ec=_INK, lw=_LW, zorder=3))
    if signs:
        ax.text(*(mid + u * r * 0.5), "+", fontsize=8.5, ha="center", va="center", zorder=4)
        ax.text(*(mid - u * r * 0.5), "−", fontsize=8.5, ha="center", va="center", zorder=4)
    _lab(ax, mid, v, text, side, off)


def acsrc(ax, a, b, text=None, side=1, r=0.34, off=0.62):
    a, b, u, v, mid, s, e = _frame(a, b, 2 * r)
    _pl(ax, [a, s]); _pl(ax, [e, b])
    ax.add_patch(_mp.Circle(mid, r, fc="white", ec=_INK, lw=_LW, zorder=3))
    w = np.array([mid + u * 0.62 * r * x + v * 0.4 * r * np.sin(np.pi * x) for x in np.linspace(-1, 1, 40)])
    ax.plot(w[:, 0], w[:, 1], color=_INK, lw=1.2, zorder=4)
    _lab(ax, mid, v, text, side, off)


def isrc(ax, a, b, text=None, side=1, r=0.34, off=0.62):
    a, b, u, v, mid, s, e = _frame(a, b, 2 * r)
    _pl(ax, [a, s]); _pl(ax, [e, b])
    ax.add_patch(_mp.Circle(mid, r, fc="white", ec=_INK, lw=_LW, zorder=3))
    ax.annotate("", xy=mid + u * r * 0.62, xytext=mid - u * r * 0.62, zorder=4,
                arrowprops=dict(arrowstyle="-|>", color=_INK, lw=1.4, mutation_scale=9))
    _lab(ax, mid, v, text, side, off)


def diode(ax, a, b, text=None, side=1, zener=False, body=0.6, off=0.4):
    a, b, u, v, mid, s, e = _frame(a, b, body)
    _pl(ax, [a, s]); _pl(ax, [e, b])
    h = 0.27
    ax.add_patch(_mp.Polygon([s + v * h, s - v * h, e], closed=True, fc="#eaf1ff", ec=_INK, lw=_LW, zorder=3))
    _pl(ax, [e + v * h, e - v * h])
    if zener:
        _pl(ax, [e + v * h, e + v * h + u * 0.12])
        _pl(ax, [e - v * h, e - v * h - u * 0.12])
    _lab(ax, mid, v, text, side, off)


def gnd(ax, p, down=True):
    p = np.array(p, float)
    d = -1 if down else 1
    _pl(ax, [p, p + [0, 0.18 * d]])
    for i, w in enumerate((0.34, 0.22, 0.10)):
        y = p[1] + d * (0.18 + 0.11 * i)
        _pl(ax, [(p[0] - w, y), (p[0] + w, y)], lw=1.4)


def arrow(ax, a, b, text=None, color=None, lw=1.3, off=0.22, size=8.2):
    a = np.array(a, float); b = np.array(b, float)
    ax.annotate("", xy=b, xytext=a,
                arrowprops=dict(arrowstyle="-|>", color=color or _INK, lw=lw, mutation_scale=9))
    if text:
        d = b - a
        v = np.array([-d[1], d[0]]) / np.hypot(*d)
        m = (a + b) / 2 + v * off
        ax.text(m[0], m[1], text, ha="center", va="center", fontsize=size, color=color or _INK)


def switch(ax, a, b, text=None, side=1, off=0.4):
    a, b, u, v, mid, s, e = _frame(a, b, 0.8)
    _pl(ax, [a, s]); _pl(ax, [e, b])
    _pl(ax, [s, s + u * 0.8 * 0.92 + v * 0.35])
    node(ax, s, 3.5); node(ax, e, 3.5)
    _lab(ax, mid, v, text, side, off)



def mesh(ax, c, r, text=None, cw=True, color="#d9534f", size=8.6):
    """Mesh-current loop: a nearly closed circular arrow centred at c."""
    c = np.array(c, float)
    t0, t1 = (np.radians(60), np.radians(60 - 320)) if cw else (np.radians(120), np.radians(120 + 320))
    th = np.linspace(t0, t1, 60)
    pts = np.array([c + r * np.array([np.cos(q), np.sin(q)]) for q in th])
    ax.plot(pts[:-3, 0], pts[:-3, 1], color=color, lw=1.4, zorder=6)
    ax.annotate("", xy=pts[-1], xytext=pts[-5], zorder=6,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=1.4, mutation_scale=9))
    if text:
        ax.text(c[0], c[1], text, ha="center", va="center", fontsize=size, color=color, zorder=6)


def _bez(p0, p1, p2, n=24):
    t = np.linspace(0, 1, n)[:, None]
    return (1 - t) ** 2 * np.array(p0) + 2 * (1 - t) * t * np.array(p1) + t ** 2 * np.array(p2)


def gate(ax, kind, x, y, w=1.2, h=0.9, lead=0.35, labels=None):
    """Logic gate with its left edge at x, centred on y. kind: AND OR NOT NAND NOR XOR XNOR.
    Returns (input points, output point)."""
    kind = kind.upper()
    top, bot = y + h / 2, y - h / 2
    ec = _INK
    bub = kind in ("NAND", "NOR", "XNOR", "NOT")
    bw = 0.2 * h if bub else 0.0
    wb = w - bw
    if kind in ("AND", "NAND"):
        r = h / 2
        th = np.linspace(np.pi / 2, -np.pi / 2, 30)
        arc = np.array([(x + wb - r + r * np.cos(q), y + r * np.sin(q)) for q in th])
        pts = np.vstack([[(x, top)], arc, [(x, bot)]])
        ax.add_patch(_mp.Polygon(pts, closed=True, fc="#f6f8fc", ec=ec, lw=_LW, zorder=3))
        ins = [(x - lead, y + h / 4), (x - lead, y - h / 4)]
        for p in ins:
            _pl(ax, [p, (x, p[1])])
    elif kind in ("OR", "NOR", "XOR", "XNOR"):
        t = np.linspace(-1, 1, 24)
        back = np.array([(x + 0.2 * wb * (1 - q * q), y + q * h / 2) for q in t])
        up = _bez((x, top), (x + 0.55 * wb, top), (x + wb, y))
        lo = _bez((x + wb, y), (x + 0.55 * wb, bot), (x, bot))
        pts = np.vstack([up, lo, back[::-1][1:]])
        ax.add_patch(_mp.Polygon(pts, closed=True, fc="#f6f8fc", ec=ec, lw=_LW, zorder=3))
        if kind in ("XOR", "XNOR"):
            _pl(ax, [(x - 0.13 * wb + 0.2 * wb * (1 - q * q), y + q * h / 2) for q in t])
        ins = [(x - lead, y + h / 4), (x - lead, y - h / 4)]
        for p in ins:
            xb = x + 0.2 * wb * (1 - (p[1] - y) ** 2 / (h / 2) ** 2)
            _pl(ax, [p, (xb - (0.13 * wb if kind in ("XOR", "XNOR") else 0), p[1])])
    else:  # NOT
        ax.add_patch(_mp.Polygon([(x, top), (x, bot), (x + wb, y)], closed=True,
                                 fc="#f6f8fc", ec=ec, lw=_LW, zorder=3))
        ins = [(x - lead, y)]
        _pl(ax, [ins[0], (x, y)])
    xo = x + w
    if bub:
        ax.add_patch(_mp.Circle((x + wb + bw / 2, y), bw / 2, fc="white", ec=ec, lw=_LW, zorder=4))
    out = (xo + lead, y)
    _pl(ax, [(xo, y), out])
    if labels:
        for p, tx in zip(ins, labels[:len(ins)]):
            ax.text(p[0] - 0.08, p[1], tx, ha="right", va="center", fontsize=8.4)
        if len(labels) > len(ins):
            ax.text(out[0] + 0.08, out[1], labels[-1], ha="left", va="center", fontsize=8.4)
    return ins, out


def transformer(ax, x, y, w=3.0, h=2.4, turns=7, lc="#1d6fb8", rc="#d9534f"):
    """Core-type transformer symbol with primary (left) and secondary (right) windings."""
    limb = 0.55
    ax.add_patch(_mp.Rectangle((x, y), w, h, fc="#d5dae3", ec=_INK, lw=1.3, zorder=1))
    ax.add_patch(_mp.Rectangle((x + limb, y + limb), w - 2 * limb, h - 2 * limb, fc="white", ec=_INK, lw=1.3, zorder=2))
    ys = np.linspace(y + 0.42, y + h - 0.42, turns)
    for yy in ys:
        ax.add_patch(_mp.Ellipse((x + limb / 2, yy), limb + 0.5, 0.17, fc="none", ec=lc, lw=1.6, zorder=3))
        ax.add_patch(_mp.Ellipse((x + w - limb / 2, yy), limb + 0.5, 0.17, fc="none", ec=rc, lw=1.6, zorder=3))
    return {"p_top": (x - 0.25, ys[-1]), "p_bot": (x - 0.25, ys[0]),
            "s_top": (x + w + 0.25, ys[-1]), "s_bot": (x + w + 0.25, ys[0])}


def bjt(ax, x, y, kind="npn", text=None):
    """BJT symbol, base bar at x, centred on y. Returns dict of terminal points B, C, E."""
    sg = 1 if kind == "npn" else -1
    _pl(ax, [(x, y - 0.5), (x, y + 0.5)], lw=2.6)
    B = (x - 0.7, y); _pl(ax, [B, (x, y)])
    C = (x + 0.6, y + 1.1); E = (x + 0.6, y - 1.1)
    _pl(ax, [(x, y + 0.22), (x + 0.6, y + 0.62), C])
    _pl(ax, [(x, y - 0.22), (x + 0.6, y - 0.62), E])
    ax.annotate("", xy=(x + 0.5, y - 0.55) if kind == "npn" else (x + 0.05, y - 0.25),
                xytext=(x + 0.3, y - 0.4) if kind == "npn" else (x + 0.3, y - 0.4), zorder=5,
                arrowprops=dict(arrowstyle="-|>", color=_INK, lw=1.4, mutation_scale=9))
    ax.add_patch(_mp.Circle((x + 0.25, y), 0.95, fc="none", ec=_INK, lw=1.0, zorder=0))
    if text:
        ax.text(x + 1.4, y, text, fontsize=8.4, va="center")
    return {"B": B, "C": C, "E": E}


def opamp(ax, x, y, w=2.4, h=2.4, text=None):
    """Op-amp triangle, left edge at x, centred on y. Inverting (-) input is the upper one.
    Returns dict of terminal points inv, non, out (all on the triangle boundary)."""
    ax.add_patch(_mp.Polygon([(x, y - h / 2), (x, y + h / 2), (x + w, y)], closed=True,
                             fc="#eaf1ff", ec=_INK, lw=_LW, zorder=3))
    dy = h * 0.25
    ax.text(x + 0.22, y + dy, "−", fontsize=11, ha="center", va="center", zorder=4)
    ax.text(x + 0.22, y - dy, "+", fontsize=10, ha="center", va="center", zorder=4)
    if text:
        ax.text(x + w * 0.42, y, text, fontsize=8, ha="center", va="center", zorder=4)
    return {"inv": (x, y + dy), "non": (x, y - dy), "out": (x + w, y)}


def mosfet(ax, x, y, kind="n", mode="enh", text=None):
    """MOSFET symbol (gate bar at x, channel bar to its right, centred on y).
    mode 'enh' = broken channel, 'dep' = continuous channel. Returns dict G, D, S, B (substrate)."""
    cx = x + 0.3
    _pl(ax, [(x, y - 0.6), (x, y + 0.6)], lw=2.4)
    G = (x - 0.7, y); _pl(ax, [G, (x, y)])
    if mode == "enh":
        for a0, b0 in ((0.6, 0.32), (0.18, -0.18), (-0.32, -0.6)):
            _pl(ax, [(cx, y + a0), (cx, y + b0)], lw=2.4)
    else:
        _pl(ax, [(cx, y - 0.6), (cx, y + 0.6)], lw=2.4)
    D = (cx + 0.7, y + 1.1); S = (cx + 0.7, y - 1.1)
    _pl(ax, [(cx, y + 0.5), (cx + 0.7, y + 0.5), D])
    _pl(ax, [(cx, y - 0.5), (cx + 0.7, y - 0.5), S])
    _pl(ax, [(cx, y), (cx + 0.7, y), (cx + 0.7, y - 0.5)])
    if kind == "n":
        ax.annotate("", xy=(cx + 0.02, y), xytext=(cx + 0.4, y), zorder=5,
                    arrowprops=dict(arrowstyle="-|>", color=_INK, lw=1.3, mutation_scale=8))
    else:
        ax.annotate("", xy=(cx + 0.4, y), xytext=(cx + 0.02, y), zorder=5,
                    arrowprops=dict(arrowstyle="-|>", color=_INK, lw=1.3, mutation_scale=8))
    if text:
        ax.text(cx + 1.2, y, text, fontsize=8.4, va="center")
    return {"G": G, "D": D, "S": S, "B": (cx + 0.7, y)}


def blockchain(steps, cols=3, figsize=(5.8, 2.5), colors=None):
    """Rows of rounded boxes joined by arrows (snake order, left to right then next row).
    steps: list of (title, subtitle). Returns the Figure."""
    pal = colors or ["#1d6fb8", "#d9534f", "#2e8b57", "#b8860b", "#6a5acd", "#008b8b"]
    n = len(steps)
    rows = (n + cols - 1) // cols
    fig, ax = plt.subplots(figsize=figsize)
    ax.axis("off")
    w, h, gx, gy = 2.7, 1.25, 0.55, 0.7
    ax.set_xlim(-0.1, cols * w + (cols - 1) * gx + 0.1)
    ax.set_ylim(-0.1, rows * h + (rows - 1) * gy + 0.1)
    pos = []
    for i, (t, sub) in enumerate(steps):
        r, c = divmod(i, cols)
        x = c * (w + gx)
        y = (rows - 1 - r) * (h + gy)
        pos.append((x, y))
        ax.add_patch(_mp.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.18",
                                        fc=pal[i % len(pal)], ec="none"))
        ax.text(x + w / 2, y + h * 0.62, t, ha="center", va="center", color="white", fontsize=7.3, fontweight="bold")
        ax.text(x + w / 2, y + h * 0.27, sub, ha="center", va="center", color="white", fontsize=7.4)
    for i in range(n - 1):
        (x0, y0), (x1, y1) = pos[i], pos[i + 1]
        if y0 == y1:
            ax.annotate("", xy=(x1 - 0.02, y1 + h / 2), xytext=(x0 + w + 0.02, y0 + h / 2),
                        arrowprops=dict(arrowstyle="-|>", color="#5b6472", lw=1.3))
        else:
            ym = y0 - gy / 2
            ax.plot([x0 + w / 2, x0 + w / 2, x1 + w / 2], [y0 - 0.03, ym, ym], color="#5b6472", lw=1.3)
            ax.annotate("", xy=(x1 + w / 2, y1 + h + 0.03), xytext=(x1 + w / 2, ym),
                        arrowprops=dict(arrowstyle="-|>", color="#5b6472", lw=1.3))
    return fig


NAMES = ["ckt_canvas", "wire", "node", "terminal", "label", "res", "ind", "cap", "batt",
         "vsrc", "acsrc", "isrc", "diode", "gnd", "arrow", "switch", "mesh", "gate", "transformer", "blockchain", "bjt", "opamp", "mosfet"]


def namespace():
    g = globals()
    return {n: g[n] for n in NAMES}
