#!/usr/bin/env python3
"""Compile and run every ```java block in a book; compare with the ```output block that follows.
   Blocks without a following ```output block are compiled only. Usage: check_java_examples.py <dir>"""
import os, re, subprocess, sys, tempfile, glob
d = sys.argv[1]; fails = 0; n = 0
for md in sorted(glob.glob(os.path.join(d, "unit-*.md"))):
    t = open(md, encoding="utf-8").read()
    for m in re.finditer(r"```java\n(.*?)```(?:\n```output\n(.*?)```)?", t, re.S):
        code, exp = m.group(1), m.group(2)
        cm = re.search(r"public\s+(?:final\s+)?(?:class|interface|enum|record)\s+(\w+)", code) or re.search(r"(?:class|interface)\s+(\w+)", code)
        if not cm: continue
        n += 1; name = cm.group(1); tmp = tempfile.mkdtemp()
        open(os.path.join(tmp, name + ".java"), "w").write(code)
        c = subprocess.run(["javac", "-Xlint:none", name + ".java"], cwd=tmp, capture_output=True, text=True)
        label = f"{os.path.basename(md)}:{name}"
        if c.returncode: print("FAIL compile", label, c.stderr[:300]); fails += 1; continue
        if exp is None: print("ok   (compiled)", label); continue
        r = subprocess.run(["java", name], cwd=tmp, capture_output=True, text=True, timeout=30)
        if r.stdout.strip() == exp.strip(): print("ok  ", label)
        else: print("FAIL output", label, "\n--- got\n" + r.stdout + "--- expected\n" + exp); fails += 1
print(f"{n} programs, {fails} failures"); sys.exit(1 if fails else 0)
