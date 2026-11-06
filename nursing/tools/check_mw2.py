#!/usr/bin/env python3
"""Midwifery II (BSN 19-20): compute and assert every number in the book.
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
# ---- Unit 1: bleeding in pregnancy
_si, _bv = 118 / 86, 100 * 60
chk("shock", (f"{_si:.2f}", _bv, f"{1200 / _bv * 100:.1f}", 110 / 100, 1000 / (100 * 50) * 100), ("1.37", 6000, "20.0", 1.1, 20.0))
chk("hcg", (round((1500 - 1200) / 1200 * 100), round((2100 - 1200) / 1200 * 100), round((1400 - 1000) / 1000 * 100), f"{(2900 - 2400) / 2900 * 100:.1f}"), (25, 75, 40, "17.2"))
_bsa = (160 * 55 / 3600) ** 0.5
chk("mtx", (f"{_bsa:.2f}", round(50 * _bsa), 50 * 1.6, 800 // 200, 600 // 200, 6 / 4, 6 * 4), ("1.56", 78, 80.0, 4, 3, 1.5, 24))
T.update(c1_si="1.37", c1_pct="20")
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
