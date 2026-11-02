#!/usr/bin/env python3
"""Compile and run every complete C program in the course notes and compare with the printed output.

A program is a ```c fence containing `int main`. Optional ```input fence right after it supplies stdin.
The ```output fence that follows is the output the text claims; it must match exactly (trailing space ignored).
    python3 bca/tools/check_c_examples.py bca/course/semester-1/programming-in-c/unit-*.md
"""
import re, subprocess, sys, tempfile, os
bad = total = 0
for path in sys.argv[1:]:
    text = open(path, encoding="utf-8").read()
    pat = re.compile(r"```c\n(.*?)```\n(?:\s*```input\n(.*?)```\n)?(?:\s*```output\n(.*?)```)?", re.S)
    for i, m in enumerate(pat.finditer(text), 1):
        src, inp, out = m.group(1), m.group(2) or "", m.group(3)
        if "int main" not in src:
            continue
        total += 1
        d = tempfile.mkdtemp(); c = os.path.join(d, "p.c"); exe = os.path.join(d, "p")
        open(c, "w").write(src)
        r = subprocess.run(["gcc", "-std=c11", "-Wall", "-o", exe, c, "-lm"], capture_output=True, text=True)
        tag = f"{os.path.basename(os.path.dirname(path))}/{os.path.basename(path)} program {i}"
        if r.returncode:
            bad += 1; print("COMPILE FAIL", tag, r.stderr[:400]); continue
        try:
            run = subprocess.run([exe], input=inp, capture_output=True, text=True, timeout=5, cwd=d)
        except subprocess.TimeoutExpired:
            bad += 1; print("TIMEOUT", tag); continue
        if out is None:
            print("NO OUTPUT BLOCK", tag); bad += 1; continue
        a = [l.rstrip() for l in run.stdout.rstrip().split("\n")]; b = [l.rstrip() for l in out.rstrip().split("\n")]
        if a != b:
            bad += 1; print("MISMATCH", tag, "\n--- actual\n" + run.stdout + "--- claimed\n" + out)
print(f"{total} programs, {bad} problems")
sys.exit(1 if bad else 0)
