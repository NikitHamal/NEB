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
# ---- U2-BEGIN
# ---- Unit 2: family planning
from datetime import date as _d, datetime as _dt, timedelta as _td
chk("kamala", (6 * 1200 / 4800, 1200 / 120 + 450 / 15 + 320 / 4 + 15 * 4.6 + 10 * 2.5, 26 - 18, 32 - 11, _d(2025, 3, 3) + _td(weeks=13), _d(2025, 3, 3) + _td(weeks=17), _dt(2025, 3, 15, 22) + _td(hours=72)), (1.5, 214.0, 8, 21, _d(2025, 6, 2), _d(2025, 6, 30), _dt(2025, 3, 18, 22)))
chk("pq2", (3 * 1200 / 1200, 600 / 120, 60 / 4, 27 - 18, _d(2025, 1, 10) + _td(weeks=13), round(1000 * 0.07)), (3.0, 5.0, 15.0, 9, _d(2025, 4, 11), 70))
# ---- U2-END
# ---- U3-BEGIN
# ---- Unit 3: menstrual disorders, infertility, menopause
chk("radha", (f"{72 / 1.57 ** 2:.1f}", f"{72 * 0.95:.1f}", f"{72 * 0.95 / 1.57 ** 2:.1f}", f"{72 * 0.9 / 1.57 ** 2:.1f}", f"{25 * 1.57 ** 2:.1f}", f"{72 - 25 * 1.57 ** 2:.1f}", 35 - 14, 3.0 * 10, f"{0.5 * 4.5 * 3.0 * 2.5:.1f}", f"{(1 - 0.85 ** 12) * 100:.1f}", f"{(1 - 0.9 ** 6) * 100:.1f}", 2.5 * 5, f"{(0.62 - 1.0) / 0.12:.1f}", 1200 - 700), ("29.2", "68.4", "27.7", "26.3", "61.6", "10.4", 21, 30.0, "16.9", "85.8", "46.9", 12.5, "-3.2", 500))
chk("pq3", (f"{78 / 1.6 ** 2:.1f}", 80 * 0.05, 2.5 * 12, 32 - 14, f"{(1 - 0.75 ** 6) * 100:.1f}", f"{(0.70 - 1.0) / 0.1:.1f}", 1200 - 750), ("30.5", 4.0, 30.0, 18, "82.2", "-3.0", 450))
# ---- U3-END
# ---- U4-BEGIN
# ---- Unit 4: gynaecological cancers
import math as _m
chk("via", (70, 285, f"{70 / 355 * 100:.1f}", f"{1615 / 1645 * 100:.1f}", 90, 190, f"{90 / 280 * 100:.1f}", f"{1710 / 1720 * 100:.1f}", f"{840 / 4200 * 100:.1f}", 0.7 * 4200 - 840, 100000 * 0.9 / 0.8, f"{_m.sqrt(152 * 50 / 3600):.2f}", f"{40 * _m.sqrt(152 * 50 / 3600):.1f}", round(1000 * 20 / 480), 0.5 * 60 * 24, 365 * 5), (70, 285, "19.7", "98.2", 90, 190, "32.1", "99.4", "20.0", 2100.0, 112500.0, "1.45", "58.1", 42, 720.0, 1825))
chk("pq4", (45 / 50 * 100, 810 / 900 * 100, 80 / 200 * 100, 600 / 2000 * 100, 50000 * 0.9, 40 * 1.6, round(500 * 15 / 240)), (90.0, 90.0, 40.0, 30.0, 45000.0, 64.0, 31))
# ---- U4-END
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
