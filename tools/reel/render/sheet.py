#!/usr/bin/env python3
"""Contact sheet of rendered frames: python sheet.py FRAMES_DIR OUT.jpg [--cols 8] [--fps 60] [--width 220]"""
import argparse, glob, os, re
from PIL import Image, ImageDraw, ImageFont

ap = argparse.ArgumentParser()
ap.add_argument("frames")
ap.add_argument("out")
ap.add_argument("--cols", type=int, default=8)
ap.add_argument("--fps", type=int, default=60)
ap.add_argument("--width", type=int, default=220)
ap.add_argument("--start", type=float, default=0)
ap.add_argument("--end", type=float, default=1e9)
ap.add_argument("--step", type=int, default=1, help="keep every Nth frame")
a = ap.parse_args()
files = sorted(glob.glob(os.path.join(a.frames, "f_*.jpg")))
items = []
for f in files:
    i = int(re.search(r"f_(\d+)", f).group(1))
    if a.start <= i / a.fps < a.end and i % a.step == 0:
        items.append((i, f))
w = a.width
h = int(w * 16 / 9)
rows = (len(items) + a.cols - 1) // a.cols
sheet = Image.new("RGB", (a.cols * w, rows * (h + 22)), "white")
d = ImageDraw.Draw(sheet)
for k, (i, f) in enumerate(items):
    im = Image.open(f).convert("RGB").resize((w, h))
    x, y = (k % a.cols) * w, (k // a.cols) * (h + 22)
    sheet.paste(im, (x, y))
    d.text((x + 4, y + h + 4), f"{i / a.fps:.2f}s", fill=(10, 22, 54))
sheet.save(a.out, quality=82)
print(f"{len(items)} frames -> {a.out} {sheet.size}")
