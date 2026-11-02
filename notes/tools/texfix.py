#!/usr/bin/env python3
"""Brace the TeX shorthand matplotlib mathtext rejects: \\frac12 -> \\frac{1}{2}, \\sqrt3 -> \\sqrt{3}."""
import re, sys
for p in sys.argv[1:]:
    s = open(p, encoding="utf-8").read()
    o = s
    s = re.sub(r"\\frac(\d)\{(\d+)\}", r"\\frac{\1}{\2}", s)
    s = re.sub(r"\\frac(\d)(\d)", r"\\frac{\1}{\2}", s)
    s = re.sub(r"\\sqrt(\d)", r"\\sqrt{\1}", s)
    if s != o:
        open(p, "w", encoding="utf-8", newline="\n").write(s)
        print("fixed", p)
