"""Execute authored matplotlib figure code -> cached SVG. House style applied globally."""
import hashlib, os, io, traceback, warnings
import matplotlib
import matplotlib.patches as mpatches
import fonts
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

warnings.filterwarnings("ignore")
CACHE = os.path.join(os.path.dirname(__file__), "..", "figures", "_fig")
os.makedirs(CACHE, exist_ok=True)
FAILS = []

# Nebians figure house style
INK      = "#14181f"
MUTED    = "#5b6472"
GRID     = "#dfe3ea"
ACCENT   = "#1d6fb8"     # primary
SERIES   = ["#1d6fb8", "#d9534f", "#2e8b57", "#b8860b", "#6a5acd", "#008b8b"]

FAMILY   = ["Inter", "DejaVu Sans", "Noto Sans Devanagari"]
TARGET_W = 5.9          # inches; the text column is 6.93 in

fonts.ensure()   # static bold instances, so fontweight="bold" is actually bold

matplotlib.rcParams.update({
    # A family *list* (not the "sans-serif" generic) is what turns on
    # matplotlib's per-glyph fallback, so a Nepali label falls through to Noto
    # while arrows and maths signs still come from Inter/DejaVu.
    "font.family": FAMILY,
    "mathtext.fontset": "stix",
    "font.size": 8.6,
    "axes.labelsize": 8.8, "axes.titlesize": 9.4,
    "xtick.labelsize": 8.0, "ytick.labelsize": 8.0, "legend.fontsize": 8.0,
    "axes.labelcolor": INK, "axes.edgecolor": "#aab0ba", "axes.titlecolor": INK,
    "text.color": INK, "xtick.color": MUTED, "ytick.color": MUTED,
    "grid.color": GRID, "grid.linewidth": 0.7,
    "axes.linewidth": 0.9, "lines.linewidth": 1.7,
    "legend.frameon": False, "figure.dpi": 100, "savefig.transparent": True,
})


def _style():
    matplotlib.rcParams.update({
        "font.family": FAMILY,
        "mathtext.fontset": "stix",
        "svg.fonttype": "path",
        "font.size": 9.5,
        "axes.edgecolor": INK, "axes.linewidth": 0.9,
        "axes.labelcolor": INK, "axes.labelsize": 9.5,
        "axes.titlesize": 10.5, "axes.titleweight": "600", "axes.titlecolor": INK,
        "axes.grid": False, "axes.axisbelow": True,
        "grid.color": GRID, "grid.linewidth": 0.7,
        "xtick.color": MUTED, "ytick.color": MUTED,
        "xtick.labelsize": 8.5, "ytick.labelsize": 8.5,
        "xtick.direction": "out", "ytick.direction": "out",
        "legend.frameon": False, "legend.fontsize": 8.5,
        "figure.facecolor": "none", "axes.facecolor": "none",
        "axes.prop_cycle": matplotlib.cycler(color=SERIES),
        "lines.linewidth": 1.7, "lines.solid_capstyle": "round",
        "patch.linewidth": 0.9,
    })

def run(code: str, chapter_id: str = "") -> str | None:
    """Exec `code`; it must leave a Figure in `fig`. Returns svg path or None."""
    key = hashlib.sha1((code + "|v4").encode()).hexdigest()[:20]
    out = os.path.join(CACHE, key + ".svg")
    if os.path.exists(out):
        return out
    _style()
    # Common patch classes are injected so a figure never fails on a missing
    # import; `plt.Ellipse` and friends do not exist on pyplot.
    ns = {"plt": plt, "np": np, "matplotlib": matplotlib,
          "INK": INK, "MUTED": MUTED, "GRID": GRID, "ACCENT": ACCENT, "SERIES": SERIES,
          "matrix": matrix, "mateq": mateq,
          "flow": flow, "cycle": cycle, "cards": cards,
          "relation": relation, "barh_ranked": barh_ranked,
          "Rectangle": mpatches.Rectangle, "Circle": mpatches.Circle,
          "Ellipse": mpatches.Ellipse, "Polygon": mpatches.Polygon,
          "Arc": mpatches.Arc, "Wedge": mpatches.Wedge,
          "FancyArrow": mpatches.FancyArrow, "FancyArrowPatch": mpatches.FancyArrowPatch,
          "matplotlib.patches": mpatches}
    try:
        exec(compile(code, "<figure>", "exec"), ns)
        fig = ns.get("fig") or plt.gcf()
        if fig is None or not fig.get_axes() and not fig.texts:
            raise RuntimeError("no figure produced")
        # Labels are set in points, so enlarging the canvas enlarges the
        # drawing area without touching type size: the chart reads better on
        # a 176 mm text column, which is 6.9 in wide.
        w, h = fig.get_size_inches()
        if w < TARGET_W:
            scale = min(TARGET_W / w, 1.30)
            fig.set_size_inches(w * scale, h * scale)
        fig.savefig(out, format="svg", transparent=True,
                    bbox_inches="tight", pad_inches=0.04)
        plt.close("all")
        return out
    except Exception:
        FAILS.append((chapter_id, traceback.format_exc(limit=2)[-400:]))
        plt.close("all")
        return None


# ---------------------------------------------------------------- matrices
# mathtext has no \begin{matrix}, so matrices/determinants are drawn as figures.

def matrix(ax, rows, x=0.0, y=0.0, fontsize=11.0, bracket="[",
           colw=0.52, rowh=0.44, color=INK):
    """Draw a bracketed matrix on `ax` in data coords. Returns (width, height).

    rows    : list of lists of strings; cells may contain mathtext ('$a_{11}$')
    bracket : "[" for a matrix, "|" for a determinant, "" for bare entries
    """
    nr = len(rows)
    nc = max(len(r) for r in rows)
    w, h = nc * colw, nr * rowh
    for i, row in enumerate(rows):
        for j, cell in enumerate(row):
            ax.text(x + (j + 0.5) * colw, y + h - (i + 0.5) * rowh, str(cell),
                    ha="center", va="center", fontsize=fontsize, color=color)
    if bracket:
        pad, tick = 0.10, 0.11
        for side in (0, 1):
            bx = x - pad if side == 0 else x + w + pad
            ax.plot([bx, bx], [y - 0.05, y + h + 0.05], color=color, lw=1.1,
                    solid_capstyle="round")
            if bracket == "[":
                d = tick if side == 0 else -tick
                ax.plot([bx, bx + d], [y + h + 0.05] * 2, color=color, lw=1.1)
                ax.plot([bx, bx + d], [y - 0.05] * 2, color=color, lw=1.1)
    return w, h


def mateq(items, fontsize=11.0, colw=0.52, rowh=0.44, gap=0.20, scale=0.55):
    """One-line matrix equation figure. Returns a Figure (assign it to `fig`).

    items: a list, each element one of
      "A ="                       -> plain/mathtext text run
      [[1, 2], [3, 4]]            -> a bracketed matrix
      ("det", [[1, 2], [3, 4]])   -> a determinant with vertical bars
    """
    specs = []
    for it in items:
        if isinstance(it, str):
            specs.append(("t", it, 0.125 * len(it) + 0.10, rowh))
        else:
            if isinstance(it, tuple) and it and it[0] == "det":
                br, rows = "|", it[1]
            else:
                br, rows = "[", it
            nc = max(len(r) for r in rows)
            specs.append(("m", (rows, br), nc * colw + 0.34, len(rows) * rowh))
    W = sum(s[2] for s in specs) + gap * (len(specs) - 1)
    H = max(s[3] for s in specs)
    fig = plt.figure(figsize=(max(W * scale, 1.0), max(H * scale, 0.42)))
    ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off")
    x = 0.0
    for kind, payload, w, h in specs:
        if kind == "t":
            ax.text(x + w / 2, H / 2, payload, ha="center", va="center",
                    fontsize=fontsize, color=INK)
        else:
            rows, br = payload
            matrix(ax, rows, x=x + 0.17, y=H / 2 - h / 2, fontsize=fontsize,
                   bracket=br, colw=colw, rowh=rowh)
        x += w + gap
    ax.set_xlim(-0.12, W + 0.12); ax.set_ylim(-0.14, H + 0.14)
    return fig


# ---------------------------------------------------------------- diagrams
# Chapters need the same half-dozen diagram shapes over and over — a flow of
# steps, a cycle, a row of cards, a relation triangle. Hand-drawing each one
# with FancyBboxPatch produced inconsistent, thin-looking figures, so the
# shapes live here: one call, a consistent look, and text that is fitted to
# the box instead of spilling out of it.

def _card(ax, x, y, w, h, title, body="", color=None, tsize=9.0, bsize=7.4,
          radius=0.055):
    color = color or SERIES[0]
    ax.add_patch(mpatches.FancyBboxPatch(
        (x, y), w, h, boxstyle=f"round,pad=0.004,rounding_size={radius}",
        facecolor=color, edgecolor="none", alpha=0.92, mutation_aspect=1))
    if body:
        ax.text(x + w / 2, y + h * 0.63, title, ha="center", va="center",
                color="white", fontsize=tsize, fontweight="bold")
        ax.text(x + w / 2, y + h * 0.28, body, ha="center", va="center",
                color="white", fontsize=bsize, linespacing=1.25)
    else:
        ax.text(x + w / 2, y + h / 2, title, ha="center", va="center",
                color="white", fontsize=tsize, linespacing=1.25)


def flow(steps, note="", figsize=None, colors=None, wrap=True):
    """A left-to-right flow of steps, each in a rounded card with an arrow."""
    n = len(steps)
    figsize = figsize or (min(2.0 + 1.25 * n, 6.6), 1.85 if not note else 2.15)
    fig, ax = plt.subplots(figsize=figsize)
    colors = colors or [SERIES[i % len(SERIES)] for i in range(n)]
    gap, w = 0.055, (1.0 - 0.055 * (n - 1)) / n
    for i, step in enumerate(steps):
        x = i * (w + gap)
        title, body = (step if isinstance(step, (tuple, list)) else (step, ""))
        _card(ax, x, 0.30, w, 0.52, title, body, colors[i],
              tsize=8.6 if not body else 8.4, bsize=7.0)
        if i < n - 1:
            ax.annotate("", xy=(x + w + gap * 0.95, 0.56),
                        xytext=(x + w + gap * 0.05, 0.56),
                        arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.3))
    if note:
        ax.text(0.5, 0.10, note, ha="center", va="center", color=MUTED,
                fontsize=7.6)
    ax.set_xlim(-0.01, 1.01)
    ax.set_ylim(0.0, 0.92)
    ax.axis("off")
    return fig, ax


def cycle(nodes, centre="", figsize=(4.6, 3.6), colors=None):
    """A closed loop of nodes with arrows — for feedback and vicious cycles."""
    import math
    n = len(nodes)
    fig, ax = plt.subplots(figsize=figsize)
    colors = colors or [SERIES[i % len(SERIES)] for i in range(n)]
    cx, cy, R, r = 0.5, 0.5, 0.33, 0.135
    pts = []
    for i in range(n):
        a = math.pi / 2 - i * 2 * math.pi / n
        pts.append((cx + R * math.cos(a), cy + R * math.sin(a)))
    for (x, y), lab, col in zip(pts, nodes, colors):
        ax.add_patch(mpatches.Circle((x, y), r, facecolor=col,
                                     edgecolor="none", alpha=0.92))
        ax.text(x, y, lab, ha="center", va="center", color="white",
                fontsize=7.8, linespacing=1.2)
    for i in range(n):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % n]
        dx, dy = x2 - x1, y2 - y1
        d = math.hypot(dx, dy)
        ux, uy = dx / d, dy / d
        ax.annotate("", xy=(x2 - ux * (r + 0.02), y2 - uy * (r + 0.02)),
                    xytext=(x1 + ux * (r + 0.02), y1 + uy * (r + 0.02)),
                    arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.3,
                                    connectionstyle="arc3,rad=0.17"))
    if centre:
        ax.text(cx, cy, centre, ha="center", va="center", color=INK,
                fontsize=8.6, fontweight="bold", linespacing=1.25)
    ax.set_xlim(0.02, 0.98)
    ax.set_ylim(0.02, 0.98)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def cards(items, cols=2, figsize=None, colors=None, title_size=9.0):
    """A grid of titled cards — for 'four things', 'five pillars' panels."""
    n = len(items)
    rows = (n + cols - 1) // cols
    figsize = figsize or (min(2.2 + 2.0 * cols, 6.6), 0.95 * rows + 0.45)
    fig, ax = plt.subplots(figsize=figsize)
    colors = colors or [SERIES[i % len(SERIES)] for i in range(n)]
    gx, gy = 0.035, 0.09
    w = (1.0 - gx * (cols - 1)) / cols
    h = (1.0 - gy * (rows - 1)) / rows
    for i, item in enumerate(items):
        title, body = (item if isinstance(item, (tuple, list)) else (item, ""))
        r, c = divmod(i, cols)
        x = c * (w + gx)
        y = 1.0 - (r + 1) * h - r * gy
        _card(ax, x, y, w, h, title, body, colors[i], tsize=title_size,
              bsize=7.2)
    ax.set_xlim(-0.01, 1.01)
    ax.set_ylim(-0.02, 1.02)
    ax.axis("off")
    return fig, ax


def relation(nodes, links, figsize=(5.4, 3.2), colors=None):
    """Three or four boxes joined by labelled arrows (separation of powers,
    cause and effect, the parts of a system)."""
    n = len(nodes)
    fig, ax = plt.subplots(figsize=figsize)
    colors = colors or [SERIES[i % len(SERIES)] for i in range(n)]
    if n == 3:
        pos = [(0.5, 0.78), (0.17, 0.26), (0.83, 0.26)]
    elif n == 4:
        pos = [(0.22, 0.78), (0.78, 0.78), (0.22, 0.24), (0.78, 0.24)]
    else:
        pos = [((i + 0.5) / n, 0.5) for i in range(n)]
    w, h = 0.30, 0.24
    for (cx, cy), node, col in zip(pos, nodes, colors):
        title, body = (node if isinstance(node, (tuple, list)) else (node, ""))
        _card(ax, cx - w / 2, cy - h / 2, w, h, title, body, col,
              tsize=8.6, bsize=7.0)
    for a, b, label in links:
        (x1, y1), (x2, y2) = pos[a], pos[b]
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="<|-|>", color=MUTED, lw=1.2,
                                    shrinkA=26, shrinkB=26))
        if label:
            ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 0.035, label, ha="center",
                    va="center", color=MUTED, fontsize=7.2,
                    linespacing=1.2,
                    bbox=dict(boxstyle="round,pad=0.18", facecolor="white",
                              edgecolor="none"))
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.05, 0.98)
    ax.axis("off")
    return fig, ax


def barh_ranked(labels, values, unit="", figsize=None, color=None,
                highlight=None, fmt="{:g}"):
    """A ranked horizontal bar chart — the safe choice whenever the category
    names are long enough to collide on an x axis."""
    figsize = figsize or (5.9, 0.42 * len(labels) + 0.9)
    fig, ax = plt.subplots(figsize=figsize)
    cols = [(SERIES[3] if (highlight and lab in highlight) else
             (color or SERIES[0])) for lab in labels]
    y = range(len(labels))
    ax.barh(list(y), values, color=cols, height=0.64, edgecolor="white",
            linewidth=1.0)
    span = max(values) if values else 1
    for i, v in zip(y, values):
        ax.text(v + span * 0.015, i, fmt.format(v) + unit, va="center",
                color=INK, fontsize=8.4)
    ax.set_yticks(list(y))
    ax.set_yticklabels(labels, fontsize=8.4)
    ax.invert_yaxis()
    ax.set_xlim(0, span * 1.16)
    ax.grid(axis="x", color=GRID, linewidth=0.7)
    ax.set_axisbelow(True)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.tick_params(colors=MUTED)
    return fig, ax
