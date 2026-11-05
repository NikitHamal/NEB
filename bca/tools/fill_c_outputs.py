#!/usr/bin/env python3
"""Run every complete ```c program (contains `int main`) in the given markdown files and insert the real
output as an ```output fence right after it (replacing an existing one). Use once after writing a unit, review the
output, then check with tools/check_c_examples.py.   python3 bca/tools/fill_c_outputs.py unit-*.md"""
import re, subprocess, sys, tempfile, os
pat = re.compile(r"(```c\n(.*?)```\n)(?:\s*```output\n.*?```\n)?", re.S)
for path in sys.argv[1:]:
    text = open(path, encoding="utf-8").read()
    def repl(m):
        src = m.group(2)
        if "int main" not in src: return m.group(0)
        d = tempfile.mkdtemp(); c = os.path.join(d, "p.c"); exe = os.path.join(d, "p")
        open(c, "w").write(src)
        r = subprocess.run(["gcc", "-std=c11", "-Wall", "-o", exe, c, "-lm"], capture_output=True, text=True)
        if r.returncode: print("COMPILE FAIL", path, r.stderr[:500]); return m.group(0)
        out = subprocess.run([exe], capture_output=True, text=True, timeout=10, cwd=d).stdout
        return m.group(1) + "```output\n" + out + "```\n"
    new = pat.sub(repl, text)
    if new != text: open(path, "w", encoding="utf-8").write(new)
