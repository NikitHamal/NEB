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
# ---- U2-BEGIN
# ---- Unit 2: well-woman care, dating, physiology, minor disorders
from datetime import date, timedelta
_l = date(2025, 10, 12); _e = _l + timedelta(days=280)
chk("edd", (_e, (date(2026, 2, 1) - _l).days, divmod((date(2026, 2, 1) - _l).days, 7), round(32 * 8 / 7, 1), round(32 / 3.5, 1)), (date(2026, 7, 19), 112, (16, 0), 36.6, 9.1))
chk("naeg", (date(2025, 10, 12).replace(year=2026) + timedelta(days=0) == date(2026, 10, 12), date(2025, 10, 12) + timedelta(days=7), date(2026, 1, 20) + timedelta(days=280)), (True, date(2025, 10, 19), date(2026, 10, 27)))
chk("blood", (round(4.5 * 1.4, 2), round(2.7 * 1.5 + 1.8 * 1.25, 2), round(1.8 * 1.25 / 6.3 * 100, 1), round(1.8 / 4.5 * 100)), (6.3, 6.3, 35.7, 40))
_k = date(2025, 9, 8)
chk("kal", ((_k + timedelta(days=280)), divmod((date(2026, 1, 18) - _k).days, 7), f"{52 / 1.55 ** 2:.1f}", 52 + 11.5, 52 + 16, 2 * 60, 2 * 30), (date(2026, 6, 15), (18, 6), "21.6", 63.5, 68.0, 120, 60))
T.update(c2_edd="15 June 2026", c2_bmi="21.6")
# ---- U2-END
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
