"""Pre-build lint for paper sources. usage: python3 notes/papers/tools/lint.py <md-file> [...]
Exit 1 on any ERROR. Checks: table cell pipes, @mcq shape, stacked \\frac, \\times typo, TODO markers,
float == in checks/*.py, figure caption, nested same-quote f-strings in pipeline/*.py. WARN: long inline math."""
import re, sys, glob, os
errs, warns = [], []
def lint_md(path):
    t = open(path, encoding="utf-8").read()
    lines = t.split("\n")
    cols = None
    for i, l in enumerate(lines, 1):
        if l.startswith("|"):
            body = re.sub(r"\\\|", "", l).strip().strip("|")
            n = body.count("|") + 1
            if re.match(r"^\|[\s:|-]+\|$", l): cols = n; continue
            if cols is None: cols = n
            elif n != cols: errs.append(f"{path}:{i} table row has {n} cells, expected {cols} (unescaped |?)")
            if n >= 8: warns.append(f"{path}:{i} table with {n} columns may cramp")
        else:
            cols = None
        for m in re.finditer(r"(?<!\$)\$([^$\n]+)\$(?!\$)", l):
            s = m.group(1)
            if s.count("\\frac") >= 2: errs.append(f"{path}:{i} inline math with 2+ \\frac will stack")
            if len(s) > 80: warns.append(f"{path}:{i} inline math over 80 chars")
        if re.search(r"\\\\times|[^\\a-zA-Z]times\s*\d", l) and "$" in l: warns.append(f"{path}:{i} check 'times' usage")
        if re.search(r"\b(TODO|FIXME|PLACEHOLDER)\b", l): errs.append(f"{path}:{i} placeholder marker")
    for m in re.finditer(r"@mcq (\d+)\n(.*?)(?=\n@|\n##|\Z)", t, re.S):
        blk = m.group(2)
        if "@opts" not in blk: errs.append(f"{path}: @mcq {m.group(1)} has no @opts")
        else:
            o = re.search(r"@opts(?:-col)?\s+(.*)", blk).group(1)
            if len(o.split(" | ")) != 4: errs.append(f"{path}: @mcq {m.group(1)} needs exactly 4 options")
    for m in re.finditer(r"```figure([^\n]*)\n", t):
        if "caption=" not in m.group(1): errs.append(f"{path}: figure block without caption")
def lint_py():
    for f in glob.glob(os.path.join(os.path.dirname(__file__), "..", "checks", "*.py")):
        for i, l in enumerate(open(f), 1):
            if re.match(r"\s*assert .*==\s*-?\d+\.\d+", l): warns.append(f"{f}:{i} float == in legacy check (use abs(a-b)<0.01)")
    for f in glob.glob(os.path.join(os.path.dirname(__file__), "..", "..", "pipeline", "*.py")):
        for i, l in enumerate(open(f), 1):
            if re.search(r'f"[^"]*\{[^}"]*"[^"]*"[^}]*\}[^"]*"', l): errs.append(f"{f}:{i} same-quote nested f-string")
for p in sys.argv[1:]: lint_md(p)
lint_py()
for w in warns: print("WARN", w)
for e in errs: print("ERROR", e)
print(f"lint: {len(errs)} errors, {len(warns)} warnings"); sys.exit(1 if errs else 0)
