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
# ---- U3-BEGIN
# ---- Unit 3: antenatal care, screening, pre-eclampsia, BPCR
chk("hmis", (30000 * 20 // 1000, round(540 / 600 * 100), round(432 / 600 * 100), round((540 - 432) / 540 * 100), round(450 / 600 * 100), round(462 / 600 * 100), 600 * 180, round(600 * 180 * 1.1)), (600, 90, 72, 20, 75, 77, 108000, 118800))
chk("mg", (round((160 + 2 * 110) / 3, 1), 4 / 0.5, 5 / 0.5, 4 + 10, 5 / 0.5, 5 * 6, 30 * 4, 1 / 0.1), (126.7, 8.0, 10.0, 14, 10.0, 30, 120, 10.0))
chk("pq", (350 / 500 * 100, round((150 + 200) / 3, 1)), (70.0, 116.7))
T.update(c3_map="126.7", u3_ifa="108,000", u3_stock="118,800")
# ---- U3-END
# ---- U4-BEGIN
# ---- Unit 4: normal labour
from datetime import datetime as _dt
_a, _f, _b, _p, _t7 = _dt(2026, 3, 14, 6, 0), _dt(2026, 3, 14, 10, 45), _dt(2026, 3, 14, 11, 30), _dt(2026, 3, 14, 11, 42), _dt(2026, 3, 14, 8, 30)
chk("stg", ((_f - _a).seconds // 60, (_b - _f).seconds // 60, (_p - _b).seconds // 60, round(2 / ((_t7 - _a).seconds / 3600), 1), 3 + 3 + 2 + 2 + 2, 2 + 1 + 1 + 1 + 1), (285, 45, 12, 0.8, 12, 6))
chk("oxy", (60 / 20, round(1000 / 3), round(20 / (1000 / 3 / 60), 1), 600 // 200, 400 - 120, 620 - 120, 1000 / (60 / 15)), (3.0, 333, 3.6, 3, 280, 500, 250.0))
T.update(c4_bishop="12", c4_active="4 h 45 min")
# ---- U4-END
# ---- U5-BEGIN
# ---- Unit 5: newborn, puerperium, lactation
from datetime import date as _d, timedelta as _td
chk("apg", (2 + 2 + 2 + 1 + 1, 2 + 2 + 2 + 1 + 2, 1 + 1 + 1 + 1 + 0, 2 + 1 + 1 + 1 + 0), (8, 9, 4, 5))
chk("wt", (f"{(3000 - 2790) / 3000 * 100:.1f}", 100 * 2790 / 1000, f"{100 * 2790 / 1000 / 8:.1f}", f"{(3200 - 2950) / 3200 * 100:.1f}", 100 * 2.95, f"{100 * 2.95 / 8:.1f}", f"{(3500 - 3200) / 3500 * 100:.1f}"), ("7.0", 279.0, "34.9", "7.8", 295.0, "36.9", "8.6"))
chk("pnc", ([(_d(2026, 3, 10) + _td(days=k)).strftime("%d %b") for k in (1, 3, 7, 42)], (_d(2026, 3, 10) + _td(days=7)).strftime("%d %b")), (["11 Mar", "13 Mar", "17 Mar", "21 Apr"], "17 Mar"))
T.update(c5_loss="7.8", c5_feed="36.9")
# ---- U5-END
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
