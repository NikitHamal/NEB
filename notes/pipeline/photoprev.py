#!/usr/bin/env python3
"""Render every ```photo block of a chapter to PNG so the overlays can be seen.

Usage: python3 photoprev.py ../content/bio11/unit-01.md /tmp/mine

Overlay coordinates are guesses until you have looked at the result — a label
that lands on the structure it names, or a leader line that points at nothing,
renders perfectly happily. Same bar as preview.py sets for drawn figures.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import photo  # noqa: E402

path = sys.argv[1]
outdir = sys.argv[2] if len(sys.argv) > 2 else "/tmp/photoprev"
os.makedirs(outdir, exist_ok=True)
for f in os.listdir(outdir):
    if f.endswith(".png"):
        os.remove(os.path.join(outdir, f))

text = open(path, encoding="utf-8").read()
blocks = re.findall(r"^```photo([^\n]*)\n(.*?)^```\s*$", text, re.S | re.M)
print(f"{len(blocks)} photo blocks")
for i, (info, script) in enumerate(blocks, 1):
    at = photo.parse_attrs(info)
    aid = at.get("id", "?")
    try:
        wpct = float(at.get("width", "88"))
    except ValueError:
        wpct = 88.0
    src = photo.render(aid, script, wpct)
    if not src:
        print(f"  photo{i:02d} FAILED  {aid}")
        continue
    dest = os.path.join(outdir, f"photo{i:02d}.png")
    with open(src, "rb") as a, open(dest, "wb") as b:
        b.write(a.read())
    ops, keys, _ = photo.parse_script(script)
    print(f"  photo{i:02d} OK  {aid}  width={wpct:.0f}%  "
          f"{len(ops)} overlays, {len(keys)} key entries -> {dest}")
if photo.FAILS:
    print("\nfailures:")
    for aid, err in photo.FAILS:
        print(f"  {aid}: {err.strip().splitlines()[-1][:160]}")
