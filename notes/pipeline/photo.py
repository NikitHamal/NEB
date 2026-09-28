"""Render a ```photo block: a real image from assets/, plus our own overlays.

A Commons diagram is rarely usable exactly as found — the labels are in the
wrong language, in the wrong terminology, or absent because the useful version
of the file is the "numbers version". So a photo block is the image *plus* a
short overlay script, and the overlay is drawn by us in the book's own type and
palette. The result is a real micrograph or reference diagram that still speaks
NEB's vocabulary.

Block syntax (inside a fenced ```photo … ``` block, one directive per line):

    ```photo id="bio11/mitochondrion" caption="Ultrastructure of a mitochondrion." width="86"
    crop 0.02 0.04 0.98 0.98
    label 0.30 0.88 "Outer membrane"
    call  0.12 0.62 0.38 0.55 "Cristae"
    mark  0.52 0.40 "3"
    box   0.44 0.30 0.20 0.18 "Matrix"
    scale 0.62 0.08 0.24 "1 μm"
    key   1 Outer membrane
    ```

Directives
  crop  L B R T          keep this fraction of the image (y measured from bottom)
  label X Y "text"       text at fractional position, on a soft white plate
  call  X Y TX TY "text" label at (X,Y) with a leader line to the point (TX,TY)
  mark  X Y "n"          small filled disc with a number, for numbered diagrams
  box   X Y W H ["text"] highlight rectangle (x,y = lower-left), optional caption
  arrow X Y TX TY        bare arrow, no text
  scale X Y W "text"     horizontal scale bar of width W with its label
  key   n text           an entry in the numbered key printed *below* the image
  tint  0.18             fade the image towards white, so overlays read cleanly
  #  …                   comment

Everything is cached on a hash of (image bytes, directives, width) so a rebuild
is free.
"""
from __future__ import annotations

import hashlib
import os
import re
import shlex

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

import assets
import figrun

CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "figures", "_photo")
os.makedirs(CACHE, exist_ok=True)

FAILS: list[tuple[str, str]] = []
# asset ids used by the chapters converted so far, in first-use order
USED: list[str] = []

PLATE = dict(fc="#ffffffe8", ec="#c9ced6", lw=0.5, boxstyle="round,pad=0.24")
LBL = 8.2          # overlay label point size at print size
DPI = 250


def _note_used(asset_id: str) -> None:
    if asset_id not in USED:
        USED.append(asset_id)


# ------------------------------------------------------------------ parsing
def parse_attrs(info: str) -> dict:
    return {m.group(1): m.group(2)
            for m in re.finditer(r'(\w+)\s*=\s*"([^"]*)"', info or "")}


def parse_script(body: str) -> tuple[list, list, dict]:
    """-> (draw ops, key entries, options)."""
    ops, keys, opt = [], [], {}
    for raw in (body or "").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        try:
            tok = shlex.split(line)
        except ValueError:
            tok = line.split()
        if not tok:
            continue
        cmd, rest = tok[0].lower(), tok[1:]
        if cmd == "key":
            n = rest[0].rstrip(".") if rest else "?"
            keys.append((n, " ".join(rest[1:])))
        elif cmd == "crop" and len(rest) >= 4:
            opt["crop"] = tuple(float(v) for v in rest[:4])
        elif cmd == "tint" and rest:
            opt["tint"] = float(rest[0])
        else:
            ops.append((cmd, rest))
    return ops, keys, opt


# ------------------------------------------------------------------ drawing
def _draw(ax, ops, ar):
    """Draw overlay ops. Axes are 0..1 in x and 0..ar in y (ar = h/w)."""
    def xy(a, b):
        return float(a), float(b) * ar

    for cmd, r in ops:
        try:
            if cmd == "label":
                x, y = xy(r[0], r[1])
                ax.text(x, y, r[2], fontsize=LBL, color=figrun.INK, ha="center",
                        va="center", bbox=PLATE, zorder=6)
            elif cmd == "call":
                x, y = xy(r[0], r[1])
                tx, ty = xy(r[2], r[3])
                ha = "right" if tx > x else ("left" if tx < x else "center")
                ax.annotate(r[4], xy=(tx, ty), xytext=(x, y), fontsize=LBL,
                            color=figrun.INK, ha=ha, va="center", zorder=6,
                            bbox=PLATE,
                            arrowprops=dict(arrowstyle="-", color=figrun.INK,
                                            lw=0.9, shrinkA=2, shrinkB=1,
                                            connectionstyle="arc3,rad=0"))
            elif cmd == "arrow":
                x, y = xy(r[0], r[1])
                tx, ty = xy(r[2], r[3])
                ax.annotate("", xy=(tx, ty), xytext=(x, y), zorder=6,
                            arrowprops=dict(arrowstyle="-|>", color=figrun.ACCENT,
                                            lw=1.2, shrinkA=0, shrinkB=0))
            elif cmd == "mark":
                x, y = xy(r[0], r[1])
                ax.text(x, y, r[2], fontsize=7.4, color="white", ha="center",
                        va="center", zorder=7, fontweight="bold",
                        bbox=dict(boxstyle="circle,pad=0.26", fc=figrun.ACCENT,
                                  ec="white", lw=0.7))
            elif cmd == "box":
                x, y = xy(r[0], r[1])
                w, h = float(r[2]), float(r[3]) * ar
                ax.add_patch(FancyBboxPatch((x, y), w, h, zorder=5,
                                            boxstyle="round,pad=0.004",
                                            fc="none", ec=figrun.ACCENT, lw=1.2))
                if len(r) > 4 and r[4]:
                    ax.text(x + w / 2, y + h + 0.018 * ar, r[4], fontsize=LBL,
                            color=figrun.ACCENT, ha="center", va="bottom",
                            zorder=6, bbox=PLATE)
            elif cmd == "scale":
                x, y = xy(r[0], r[1])
                w = float(r[2])
                ax.add_patch(Rectangle((x, y), w, 0.010 * ar, fc=figrun.INK,
                                       ec="white", lw=0.5, zorder=6))
                ax.text(x + w / 2, y + 0.024 * ar, r[3], fontsize=7.6,
                        color=figrun.INK, ha="center", va="bottom", zorder=6,
                        bbox=PLATE)
        except (IndexError, ValueError) as e:
            FAILS.append((cmd, f"bad {cmd} directive {r!r}: {e}"))


# ------------------------------------------------------------------- render
def render(asset_id: str, body: str, width_pct: float = 88.0) -> str | None:
    """Composite assets/<asset_id> with its overlays. Returns a PNG path."""
    src = assets.path_for(asset_id)
    if not src:
        FAILS.append((asset_id, f"asset not registered or bytes missing: {asset_id}"))
        return None
    ops, keys, opt = parse_script(body)
    with open(src, "rb") as f:
        digest = hashlib.sha1(f.read()).hexdigest()[:16]
    key = hashlib.sha1(f"{digest}|{body}|{width_pct}|v3".encode()).hexdigest()[:20]
    out = os.path.join(CACHE, key + ".png")
    _note_used(asset_id)
    if os.path.exists(out):
        return out

    # A ```figure block earlier in the chapter may have left its own font
    # override in the shared rcParams; pin ours back so overlay text is
    # predictable, and keep the family a list so Devanagari labels fall
    # through to Noto instead of rendering as tofu boxes.
    matplotlib.rcParams["font.family"] = figrun.FAMILY
    try:
        import matplotlib.image as mpimg
        img = mpimg.imread(src)
        h_px, w_px = img.shape[0], img.shape[1]
        if "crop" in opt:
            l, b, r, t = opt["crop"]
            x0, x1 = int(l * w_px), int(r * w_px)
            y0, y1 = int((1 - t) * h_px), int((1 - b) * h_px)
            img = img[max(y0, 0):min(y1, h_px), max(x0, 0):min(x1, w_px)]
            h_px, w_px = img.shape[0], img.shape[1]
        ar = h_px / float(w_px)

        # Print width: the text column is ~176 mm wide → 6.93 in. Render at the
        # fraction of it this figure will occupy, so overlay point sizes are true.
        w_in = max(2.4, min(6.9, 6.93 * width_pct / 100.0))
        figrun._style()
        fig = plt.figure(figsize=(w_in, w_in * ar), dpi=DPI)
        ax = fig.add_axes([0, 0, 1, 1])
        ax.set_xlim(0, 1)
        ax.set_ylim(0, ar)
        ax.axis("off")
        ax.imshow(img, extent=(0, 1, 0, ar), aspect="auto", zorder=1,
                  interpolation="antialiased")
        if opt.get("tint"):
            ax.add_patch(Rectangle((0, 0), 1, ar, fc="white",
                                   alpha=float(opt["tint"]), ec="none", zorder=2))
        _draw(ax, ops, ar)
        fig.savefig(out, format="png", dpi=DPI, facecolor="white",
                    bbox_inches=None, pad_inches=0)
        plt.close(fig)
        return out
    except Exception as e:                                  # noqa: BLE001
        import traceback
        FAILS.append((asset_id, traceback.format_exc(limit=2)[-400:]))
        plt.close("all")
        return None


def key_html(keys) -> str:
    if not keys:
        return ""
    items = "".join(f'<span class="pk"><i>{n}</i>{t}</span>' for n, t in keys)
    return f'<div class="photokey">{items}</div>'
