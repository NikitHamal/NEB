#!/usr/bin/env python3
"""Extract ```figure blocks from a chapter and render each to PNG for eyeballing."""
import sys, os, re, traceback
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import figrun

path = sys.argv[1]
outdir = sys.argv[2] if len(sys.argv) > 2 else "/tmp/figprev"
os.makedirs(outdir, exist_ok=True)
for f in os.listdir(outdir):
    os.remove(os.path.join(outdir, f))
text = open(path, encoding="utf-8").read()
blocks = re.findall(r"^```figure([^\n]*)\n(.*?)^```\s*$", text, re.S | re.M)
print(f"{len(blocks)} figure blocks")
for i, (info, code) in enumerate(blocks, 1):
    figrun._style()
    ns = {"plt": plt, "np": np, "matplotlib": matplotlib, "INK": figrun.INK,
          "MUTED": figrun.MUTED, "GRID": figrun.GRID, "ACCENT": figrun.ACCENT,
          "SERIES": figrun.SERIES}
    try:
        exec(compile(code, f"<fig{i}>", "exec"), ns)
        fig = ns["fig"]
        w, h = fig.get_size_inches()
        assert 4.0 <= w <= 5.2, f"width {w} out of range"
        assert 2.2 <= h <= 4.6, f"height {h} out of range"
        fig.savefig(os.path.join(outdir, f"fig{i:02d}.png"), dpi=155,
                    bbox_inches="tight", pad_inches=0.06, facecolor="white")
        plt.close("all")
        print(f"  fig{i:02d} OK  ({w}x{h} in)")
    except Exception:
        plt.close("all")
        print(f"  fig{i:02d} FAILED\n{traceback.format_exc(limit=3)}")
