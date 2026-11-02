#!/usr/bin/env python3
"""Insert the blank line the house Markdown parser needs before a list that directly follows a paragraph line.
    python3 bca/tools/normalize_md.py bca/course/semester-3/<subject>/unit-*.md"""
import re, sys
for f in sys.argv[1:]:
    L = open(f, encoding="utf-8").read().split("\n"); out = []; fence = False
    for l in L:
        if l.startswith("```"): fence = not fence
        isl = bool(re.match(r"(- |\d+\. )", l))
        if not fence and isl and out and out[-1].strip() and not re.match(r"(- |\d+\. |\s)", out[-1]) and not out[-1].startswith(("|", ":::", "#")):
            out.append("")
        out.append(l)
    open(f, "w", encoding="utf-8").write("\n".join(out))
