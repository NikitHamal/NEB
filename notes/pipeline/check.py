#!/usr/bin/env python3
"""Validate one chapter markdown file: renders all math and figure code.

Usage: python3 check.py ../content/phy11/unit-03.md
Exits non-zero and prints every failure if anything does not compile.
"""
import sys, os, re
os.environ.setdefault("FIG_LINT", "1")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mathsvg, figrun, md2html, photo

def main(path):
    text = open(path, encoding="utf-8").read()
    slug = os.path.basename(os.path.dirname(path))
    mathsvg.FAILS.clear(); figrun.FAILS.clear(); figrun.LINT.clear(); md2html.LEAKS.clear()
    photo.FAILS.clear(); photo.USED.clear(); mathsvg.OVERWIDE.clear()
    meta, html, _ = md2html.convert(text, f"{slug}-{os.path.basename(path)}", 1)

    words = len(re.sub(r"<[^>]+>", " ", html).split())
    figs = html.count("<figcaption>")
    pics = html.count('class="nobreak photo"')
    exs  = len(re.findall(r'class="box example"', html))
    ok = True
    if mathsvg.FAILS:
        ok = False
        print(f"\n!! {len(mathsvg.FAILS)} MATH FAILURES")
        for tex, err in mathsvg.FAILS:
            print(f"   {tex.strip()[:90]!r}\n     -> {err}")
    if md2html.LEAKS:
        ok = False
        print(f"\n!! {len(md2html.LEAKS)} UNPAIRED $ (raw LaTeX would reach the PDF)")
        for ln in md2html.LEAKS[:12]:
            print(f"   {ln}")
    if figrun.FAILS:
        ok = False
        print(f"\n!! {len(figrun.FAILS)} FIGURE FAILURES")
        for code, err in figrun.FAILS:
            print(f"   -> {err}")
    if photo.FAILS:
        ok = False
        print(f"\n!! {len(photo.FAILS)} PHOTO FAILURES")
        for aid, err in photo.FAILS:
            print(f"   {aid} -> {err.strip().splitlines()[-1][:140]}")
    if figrun.LINT:
        ok = False
        print(f"\n!! {len(figrun.LINT)} FIGURE LEGIBILITY PROBLEMS (min {figrun.MIN_PT}pt, no overprinted labels)")
        for _, msg in figrun.LINT[:40]:
            print(f"   {msg}")
    wide = mathsvg.OVERWIDE
    if wide:
        ok = False
        print(f"\n!! {len(wide)} DISPLAY EQUATIONS TOO WIDE for the text column")
        print("   (break them at an = sign into two $$…$$ blocks, or shorten them)")
        for tex, w in wide:
            print(f"   {w:.0f}mm  {tex.strip()[:100]!r}")
    for k in ("subject", "grade", "unit", "title", "hours"):
        if not meta.get(k):
            ok = False; print(f"!! frontmatter missing: {k}")
    print(f"\n{path}: {words} words, {figs} figures, {pics} photos, {exs} worked examples, "
          f"{'OK' if ok else 'FAILED'}")
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
