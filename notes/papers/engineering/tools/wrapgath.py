#!/usr/bin/env python3
"""Wrap every single-line $$...$$ display that holds 2+ relations (=, \\Longrightarrow, ...) in
\\begin{gathered}...\\end{gathered} so the pipeline's aligned-splitter leaves it alone (one display = one centred line).
Usage: python3 wrapgath.py content/<id>.md ...   (idempotent; skips lines that already contain \\begin)"""
import re, sys
REL = re.compile(r'(?<![<>!\\])=|\\Longrightarrow|\\Rightarrow|\\implies|\\Leftrightarrow|\\approx|\\le(?![a-z])|\\ge(?![a-z])')
for fn in sys.argv[1:]:
    out, n = [], 0
    for ln in open(fn, encoding='utf-8').read().split('\n'):
        m = re.fullmatch(r'\$\$(.+)\$\$', ln.strip())
        if m and '\\begin' not in ln and '\\tag' not in ln and len(REL.findall(m.group(1))) >= 2:
            ln = '$$\\begin{gathered}' + m.group(1) + '\\end{gathered}$$'; n += 1
        out.append(ln)
    # blank line before/after each single-line display (a display glued to a text line renders as an indented bar)
    res = []
    for i, ln in enumerate(out):
        disp = ln.strip().startswith('$$') and ln.strip().endswith('$$') and len(ln.strip()) > 4
        if disp and res and res[-1].strip() and not res[-1].lstrip().startswith(('-', '|', '1.', '2.', '3.')) : res.append('')
        res.append(ln)
        if disp and i + 1 < len(out) and out[i + 1].strip() and not out[i + 1].lstrip().startswith('$$'): res.append('')
    open(fn, 'w', encoding='utf-8').write('\n'.join(res)); print(fn, 'wrapped', n)
