#!/usr/bin/env python3
"""Midwifery I (BSN 17-18): compute and assert every number in the book.
   --print | --fill files | --verify files   (tokens via tokcommon; python blocks are executed and compared)."""
import sys, os, re, math, subprocess, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tokcommon

def chk(label, got, want):
    ok = got == want if not isinstance(got, float) else abs(got - want) < 1e-9
    if not ok: sys.exit(f"FAIL {label}: {got} != {want}")

T = {}
# ---- UNITS-BEGIN
# ---- U1-BEGIN
# ---- Unit 1: reproductive anatomy, pelvis, placenta, fetal circulation
chk("cyc", (32 - 14, (32 - 14) - 5, 32 - 14 + 7, 32 + 1, 40 - 14), (18, 13, 25, 33, 26))
chk("oc", (12.0 - 1.5, 11.5 - 1.5, 12.5 - 1.5, 13.0 - 11.5), (10.5, 10.0, 11.0, 1.5))
chk("afi", (round(4.2 + 3.8 + 5.1 + 4.9, 1), 3.0 + 2.5 + 4.0 + 3.5, 3000 // 500), (18.0, 13.0, 6))
T.update(u1_oc="10.5", c1_oc="10.0")
# ---- U1-END
# ---- END OF UNITS (insert new units above this line)

def exec_blocks(files):
    """Run every ```python block that is directly followed by a ```text block; stdout must equal that block."""
    n = 0
    for f in files:
        t = open(f, encoding="utf-8").read()
        for m in re.finditer(r"```python\n(.*?)```\n\n```text\n(.*?)```", t, re.S):
            with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as fh: fh.write(m.group(1))
            out = subprocess.run([sys.executable, fh.name], capture_output=True, text=True).stdout.strip()
            os.unlink(fh.name)
            if out != m.group(2).strip(): sys.exit(f"{f}: python block output mismatch\n--got--\n{out}\n--book--\n{m.group(2).strip()}")
            n += 1
    print(f"verify: {n} executed python blocks match their printed output")

if __name__ == "__main__":
    if sys.argv[1:2] == ["--verify"]:
        exec_blocks(sys.argv[2:])
    tokcommon.run(T, sys.argv[1:])
