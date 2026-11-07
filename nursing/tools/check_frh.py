#!/usr/bin/env python3
"""Family and Reproductive Health Nursing (BSN 23-24): compute and assert every number in the book.
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
# ---- Unit 1: reproductive health, abortion, violence
from datetime import date as _d, timedelta as _td
_asfr = [65, 135, 120, 65, 28, 8, 1]
chk("sabina", (round(5 * sum(_asfr) / 1000, 2), round(1200 / 25000 * 1000, 1), 57 + 21, f"{43 / 78 * 100:.1f}", (_d(2025, 3, 16) - _d(2025, 1, 12)).days, _d(2025, 1, 12) + _td(days=84), 800 // 200, round(0.23 * 400)), (2.11, 48.0, 78, "55.1", 63, _d(2025, 4, 6), 4, 92))
chk("pq1", (5 * 380 / 1000, 900 / 20000 * 1000, 40 / 80 * 100, (_d(2025, 4, 27) - _d(2025, 2, 2)).days // 7, 800 // 200, 78 - 57), (1.9, 45.0, 50.0, 12, 4, 21))
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
