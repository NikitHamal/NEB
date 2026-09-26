#!/usr/bin/env python3
"""Validate one chapter markdown file: renders all math and figure code.

Usage: python3 check.py ../content/phy11/unit-03.md
Exits non-zero and prints every failure if anything does not compile.
"""
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mathsvg, figrun, md2html

def main(path):
    text = open(path, encoding="utf-8").read()
    slug = os.path.basename(os.path.dirname(path))
    mathsvg.FAILS.clear(); figrun.FAILS.clear(); md2html.LEAKS.clear()
    meta, html, _ = md2html.convert(text, f"{slug}-{os.path.basename(path)}", 1)

    words = len(re.sub(r"<[^>]+>", " ", html).split())
    figs = html.count("<figcaption>")
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
    for k in ("subject", "grade", "unit", "title", "hours"):
        if not meta.get(k):
            ok = False; print(f"!! frontmatter missing: {k}")
    print(f"\n{path}: {words} words, {figs} figures, {exs} worked examples, "
          f"{'OK' if ok else 'FAILED'}")
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
