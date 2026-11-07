#!/usr/bin/env python3
"""Child Health Nursing (BSN 21-22): compute and assert every number in the book.
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
# ---- Unit 1: child health, growth, immunisation
_exp = (9 + 9) / 2; _wt = 7.0
chk("maya", (f"{_exp:.1f}", f"{_wt / _exp * 100:.0f}", f"{(_wt - 8.2) / 0.9:.1f}", round((_wt - 3.0) * 1000 / 9), 120 * 3 * (1 / 0.75) / 10, 144 - 132, f"{132 / 150 * 100:.1f}", f"{(144 - 132) / 144 * 100:.1f}", 0.5 + 0.1 + 0.5, 15 * _wt, 15 * _wt / 25, round(0.01 * _wt, 2)), ("9.0", "78", "-1.3", 444, 48.0, 12, "88.0", "8.3", 1.1, 105.0, 4.2, 0.07))
chk("pq1", (2 * 4 + 8, (6 + 9) / 2, f"{(13.5 - 17.0) / 1.5:.1f}", 90 / 0.6, f"{(200 - 170) / 200 * 100:.0f}", 15 * 8 / 25, 2 * 3 + 8, 6 * 3 + 77), (16, 7.5, "-2.3", 150.0, "15", 4.8, 14, 95))
T.update(c1_exp="9.0", c1_pct="78", c1_z="-1.3")
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
