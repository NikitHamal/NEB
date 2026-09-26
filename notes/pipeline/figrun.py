"""Execute authored matplotlib figure code -> cached SVG. House style applied globally."""
import hashlib, os, io, traceback, warnings
import matplotlib
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

matplotlib.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Inter", "DejaVu Sans"],
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
        "font.family": "sans-serif",
        "font.sans-serif": ["Inter", "DejaVu Sans"],
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
    key = hashlib.sha1((code + "|v3").encode()).hexdigest()[:20]
    out = os.path.join(CACHE, key + ".svg")
    if os.path.exists(out):
        return out
    _style()
    ns = {"plt": plt, "np": np, "matplotlib": matplotlib,
          "INK": INK, "MUTED": MUTED, "GRID": GRID, "ACCENT": ACCENT, "SERIES": SERIES,
          "matrix": matrix, "mateq": mateq}
    try:
        exec(compile(code, "<figure>", "exec"), ns)
        fig = ns.get("fig") or plt.gcf()
        if fig is None or not fig.get_axes() and not fig.texts:
            raise RuntimeError("no figure produced")
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
