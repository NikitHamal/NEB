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
# ---- U2-BEGIN
# ---- Unit 2: newborn disorders and congenital anomalies
_kg = 1.4; _a = 2.9
chk("sunil", (1 + 2 + 1 + 2 + 1, 200 * _kg, 200 * _kg / 80, 20 * _kg, 20 * _kg / 20, 5 * _kg, 5 * _kg / 20, round(80 * _kg), f"{80 * _kg / 24:.1f}", 6 * 4), (7, 280.0, 3.5, 28.0, 1.4, 7.0, 0.35, 112, "4.7", 24))
chk("anju", (f"{(_a - 2.7) / _a * 100:.1f}", round(150 * _a), round(150 * _a / 8), round(150 * _a * 0.67), f"{4.5 - _a:.1f}", round((4.5 - _a) * 1000 / 30), 97 - 93), ("6.9", 435, 54, 291, "1.6", 53, 4))
chk("pq2", (2 + 1 + 1 + 1 + 0, f"{(3.2 - 2.9) / 3.2 * 100:.1f}", 20 * 1.2, 60 * 2.0 / 24, 100 * 1.6 / 80, 96 - 94), (5, "9.4", 24.0, 5.0, 2.0, 2))
# ---- U2-END
# ---- U3-BEGIN
# ---- Unit 3: malnutrition, ARI, diarrhoea
_kg = 7.6; _e = (10 + 9) / 2
chk("rojina", (_e, f"{_kg / _e * 100:.0f}", round(75 * _kg), f"{75 * _kg / 4:.1f}", f"{75 * _kg / 1000:.2f}", 20 * 14, round(30 * _kg), round(70 * _kg), f"{70 * _kg / 5:.1f}", round(70 * _kg / 5), f"{70 * _kg / 5 / 3:.1f}", round(40 * _kg), f"{250 / _kg:.0f}", 2 * 3, round(15 * _kg), f"{15 * _kg / 25:.1f}", round(100 * _kg), f"{100 * _kg / 24:.1f}", 1000 + 50 * 8, f"{1400 / 24:.1f}", 175 * 6.0, 175 * 6.0 / 500, round(0.6 * 12, 1)), (9.5, "80", 570, "142.5", "0.57", 280, 228, 532, "106.4", 106, "35.5", 304, "33", 6, 114, "4.6", 760, "31.7", 1400, "58.3", 1050.0, 2.1, 7.2))
chk("pq3", (75 * 9, 30 * 6, 70 * 12 / 2.5, 1000 + 50 * 8, 175 * 8 / 500, 0.6 * 10), (675, 180, 336.0, 1400, 2.8, 6.0))
# ---- U3-END
# ---- U4-BEGIN
# ---- Unit 4: infections and systemic disorders
import math as _m
_kg = 11.5
chk("bikash", (2 * 200000, f"{15 * _kg:.1f}", f"{15 * _kg / 25:.1f}", f"{20 * _kg:.0f}", f"{20 * _kg * 4:.0f}", f"{(12.0 - 1.2) / 12.0 * 100:.0f}", f"{1.2 / 12.0:.1f}", f"{(1 - 1 / 15) * 100:.1f}", 100 * 12, 100 * 12 / 2, 0.5 * 12), (400000, "172.5", "6.9", "230", "920", "90", "0.1", "93.3", 1200, 600.0, 6.0))
_b = _m.sqrt(90 * 12.5 / 3600)
chk("nephro", (f"{_b:.3f}", f"{60 * _b:.1f}", f"{40 * _b:.1f}", 15 * 12, 15 * 12 / 4, f"{2.4 * 12:.1f}", f"{3 * 2.4 * 12:.1f}"), ("0.559", "33.5", "22.4", 180, 45.0, "28.8", "86.4"))
chk("pq4", (15 * 14 / 25, 100 * 9 / 2, (10 - 2) / 10 * 100, f"{(1 - 1 / 12) * 100:.1f}", 60 * 0.5, 0.5 * 16), (8.4, 450.0, 80.0, "91.7", 30.0, 8.0))
# ---- U4-END
# ---- U5-BEGIN
# ---- Unit 5: emergencies, injury, hospitalised child, rights
_a = 3; _k = 2 * (_a + 4)
_pk = 4 * _k * 15; _mt = 1000 + 50 * (_k - 10)
chk("sumit", (_k, 20 * _k, 10 * _k, 2 * _k, f"{0.01 * _k:.2f}", f"{0.1 * _k:.1f}", 4 * _k, f"{_a / 4 + 4:.2f}", f"{_a / 4 + 3.5:.2f}", 15 * _k, f"{15 * _k / 25:.1f}", 10 * _k / 20, 10 * 500, f"{10 * 500 / _k:.0f}", 150 * _k, 75 * _k, _pk, _pk / 2, _pk / 2 / 8, _mt, f"{_mt / 24:.0f}", f"{0.02 * _k:.2f}", 30 / 120 * 60, 30 / 100 * 60, 12 / 3, 2 + 1 + 2 + 1 + 1), (14, 280, 140, 28, "0.14", "1.4", 56, "4.75", "4.25", 210, "8.4", 7.0, 5000, "357", 2100, 1050, 840, 420.0, 52.5, 1200, "50", "0.28", 15.0, 18.0, 4.0, 7))
chk("pq5", (2 * (5 + 4), 0.1 * 8, 4 * 12, 4 * 20 * 20 / 2, 10 * 12 / 20, 2000 / 10, 1 + 1 + 2 + 1 + 1), (18, 0.8, 48, 800.0, 6.0, 200.0, 6))
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
