#!/usr/bin/env python3
"""Find body pages that end early (white space above the footer) in a built book PDF.

    python3 gapaudit.py book.pdf [more.pdf ...] [--min 45] [--png DIR]

A page is flagged when the free band between its last content (text, picture, card or table
fill) and the running footer is taller than --min mm AND the next page does not open a chapter
(chapter openers legitimately leave the page above short). Prints page, gap in mm, and the first
words of the next page, so the cause (table, figure, card) is visible at a glance. Exit 0 always;
the totals line `GAPS n pages_wasted x.x` is what batch scripts compare before and after.
"""
import sys, re
import fitz

MM = 72 / 25.4


def content_bottom(page):
    H, W = page.rect.height, page.rect.width
    foot = H - 19 * MM            # running footer band starts here
    low = 0.0
    d = page.get_text("dict")
    for b in d["blocks"]:
        x0, y0, x1, y1 = b["bbox"]
        if y0 >= foot or y1 - y0 > H * 0.9:
            continue
        if b["type"] == 0:
            txt = "".join(s["text"] for l in b["lines"] for s in l["spans"]).strip()
            if not txt:
                continue
            # skip the big watermark glyph
            if max(s["size"] for l in b["lines"] for s in l["spans"]) > 120:
                continue
        low = max(low, min(y1, foot))
    for dr in page.get_drawings():
        r = dr["rect"]
        if r.y0 >= foot or r.height > H * 0.85 or r.width < 3:
            continue
        low = max(low, min(r.y1, foot))
    return low, foot


def first_words(page, n=9):
    H = page.rect.height
    for b in sorted(page.get_text("blocks"), key=lambda b: (b[1], b[0])):
        if b[1] < 14 * MM or b[1] > H * 0.5:
            continue
        t = " ".join(b[4].split())
        if len(t) > 2:
            return " ".join(t.split()[:n])
    return ""


def opens_chapter(page):
    big = 0
    for b in page.get_text("dict")["blocks"]:
        if b["type"] != 0 or b["bbox"][1] > page.rect.height * 0.4:
            continue
        for l in b["lines"]:
            for s in l["spans"]:
                if s["size"] >= 20 and s["text"].strip() and s["size"] < 120:
                    big += 1
    return big > 0


def audit(path, mn=45, png=None):
    doc = fitz.open(path)
    out, waste = [], 0.0
    start = 0
    for i in range(len(doc)):          # skip cover + front matter: start after the contents
        if re.search(r"^\s*(Contents|विषयसूची)\s*$", doc[i].get_text(), re.M):
            start = i + 1
    for i in range(start, len(doc) - 1):
        pg, nx = doc[i], doc[i + 1]
        low, foot = content_bottom(pg)
        gap = (foot - low) / MM
        if gap < mn or opens_chapter(nx):
            continue
        waste += gap / 247.0
        out.append((i + 1, gap, first_words(nx)))
    return len(doc), out, waste


if __name__ == "__main__":
    a = sys.argv[1:]
    mn = 45
    if "--min" in a:
        k = a.index("--min"); mn = float(a[k + 1]); del a[k:k + 2]
    tot, tw = 0, 0.0
    for p in a:
        n, out, w = audit(p, mn)
        print(f"== {p.split('/')[-1]}  pages={n}")
        for pg, g, nxt in out:
            print(f"  p{pg:>3} gap {g:5.1f}mm  next: {nxt[:70]}")
        print(f"  GAPS {len(out)} pages_wasted {w:.1f}")
        tot += len(out); tw += w
    if len(a) > 1:
        print(f"TOTAL GAPS {tot} pages_wasted {tw:.1f}")
