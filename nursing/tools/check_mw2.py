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
# ---- U2-BEGIN
# ---- Unit 2: postpartum haemorrhage
_loss = 780 + (460 - 140); _bv = 100 * 55
chk("pph", (_loss, f"{_loss / _bv * 100:.1f}", f"{124 / 84:.2f}", 3 * _loss, 60 / 15, 1000 / (60 / 15), round(20 / (1000 / (60 / 15)) * 60, 1), 1000 / 100, 250 * 8, 800 // 200), (1100, "20.0", "1.48", 3300, 4.0, 250.0, 4.8, 10.0, 2000, 4))
chk("pq2", (540 - 120, 3 * 800, 40 / 1000 * 125, 1000 / 100, f"{2100 / 6000 * 100:.0f}"), (420, 2400, 5.0, 10.0, "35"))
T.update(c2_si="1.48", c2_pct="20", c2_fluid="3,300")
# ---- U2-END
# ---- U3-BEGIN
# ---- Unit 3: hypertension, eclampsia, anaemia, GDM
_map = (176 + 2 * 118) / 3
_g = 4 + 10 + 5 * 5
_gz = 55 * (11 - 7.0) * 2.4 + 500
chk("htn", (f"{_map:.1f}", f"{0.75 * _map:.0f}", _g, 20 / 500 * 1000, 1000 / (20 / 500 * 1000), 1 / 0.1, 80 * 24, 30 * 4, round(_gz), -(-_gz // 200)), ("137.3", "103", 39, 40.0, 25.0, 10.0, 1920, 120, 1028, 6.0))
chk("pq3", (f"{(160 + 2 * 110) / 3:.1f}", 5 * 1, 20 / 500 * 25, 50 * (11 - 8) * 2.4 + 500, f"{5.1 * 18:.0f}", f"{10.0 * 18:.0f}", f"{8.5 * 18:.0f}"), ("126.7", 5, 1.0, 860.0, "92", "180", "153"))
T.update(c3_map="137.3", c3_vials="39", c3_urine="120")
# ---- U3-END
# ---- U4-BEGIN
# ---- Unit 4: abnormal labour
chk("dyst", ((38 - 13) * 155, f"{120 / 90:.2f}", 5 * 45, 2 * (24 // 6), f"{125 / 60 * 15:.0f}", [m / 10 * 60 for m in (2, 4, 8, 16, 32)], [m / 10 * 15 for m in (2, 4, 8, 16, 32)], 4 * 30, 25 / (200 / 200)), (3875, "1.33", 225, 8, "31", [12.0, 24.0, 48.0, 96.0, 192.0], [3.0, 6.0, 12.0, 24.0, 48.0], 120, 25.0))
chk("pq4", (8 / 10 * 60, (36 - 12) * 155, 5 * 60, 25 / 1, (5 - 1) * 30, (36 - 13) * 155), (48.0, 3720, 300, 25.0, 120, 3565))
T.update(c4_si="1.33", c4_efw="3,875", c4_gent="225")
# ---- U4-END
# ---- U5-BEGIN
# ---- Unit 5: puerperal complications and the high-risk newborn
_kg, _p, _sbp, _dbp, _rr = 58, 118, 98, 60, 24
_q = (_rr >= 22) + (_sbp <= 100) + 0
chk("sepsis", (_q, f"{_p / _sbp:.2f}", f"{(_sbp + 2 * _dbp) / 3:.1f}", 5 * _kg, 2 * (24 // 6), 500 * (24 // 8), 30 * _kg, f"{30 * _kg / 3:.0f}", f"{30 * _kg / 3 / 60 * 15:.0f}", 1 * _kg), (2, "1.20", "72.7", 290, 8, 1500, 1740, "580", "145", 58))
_w = 1.8
chk("neo", (f"{120 * _w:.0f}", f"{120 * _w / 8:.0f}", f"{120 * _w / 24:.0f}", f"{3 * _w:.1f}", f"{50 * _w:.0f}", 6 * 4, f"{15 * _w:.0f}", -(-200 // (15 * _w)), f"{2 * _w:.1f}", f"{6 * _w * 60 / 100:.1f}", f"{15 * 17.1:.0f}", f"{260 / 17.1:.1f}", 60 / 40, 1 + 1 + 1 + 1 + 0, 2 + 2 + 1 + 1 + 1), ("216", "27", "9", "5.4", "90", 24, "27", 8.0, "3.6", "6.5", "256", "15.2", 1.5, 4, 7))
chk("pq5", (30 * 52, f"{3 * 1.6:.1f}", f"{20 * 17.1:.0f}", 20 * 2.8, 100 * 2.4 / 8, 60 / 40), (1560, "4.8", "342", 56.0, 30.0, 1.5))
T.update(c5_qsofa="2", c5_si="1.20", c5_fluid="1,740", c5_gtt="145", c5_gent="290", c5_bfluid="216", c5_bfeed="27", c5_bgent="5.4", c5_bamp="90")
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
