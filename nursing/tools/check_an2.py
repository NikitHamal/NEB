#!/usr/bin/env python3
"""Adult Nursing II (BSN 10): compute and assert every number in the book.
   --print | --fill files | --verify files   (tokens via tokcommon; python blocks are executed and compared)."""
import sys, os, re, math, subprocess, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tokcommon

def chk(label, got, want):
    ok = got == want if not isinstance(got, float) else abs(got - want) < 1e-9
    if not ok: sys.exit(f"FAIL {label}: {got} != {want}")

T = {}
# ---- Unit 1: renal and urinary nursing
cg = lambda age, wt, cr, f=1.0: (140 - age) * wt / (72 * cr) * f
chk("cg", (round(cg(64, 60, 3.6), 1), round(cg(70, 50, 1.4, 0.85), 1), round(cg(58, 56, 6.8), 1)), (17.6, 29.5, 9.4))
chk("uo", (0.5 * 70, 0.5 * 70 * 6, round(150 / 70 / 6, 2)), (35.0, 210.0, 0.36))
chk("kdigo", (2.5 / 1.0, 3.0 / 1.0), (2.5, 3.0))
chk("clcr", 90 * (1200 / 1440) / 1.5, 50.0)
chk("urr", ((120 - 36) / 120 * 100, (120 - 30) / 120 * 100 + 0, round(3.5 / 58 * 100, 1)), (70.0, 75.0, 6.0))
chk("fluid", (300 + 500, (1000 + 800) - (700 + 100), 50 * 50 // 100, round(60 * 50)), (800, 1000, 25, 3000))
chk("cauti", 4 / 1250 * 1000, 3.2); chk("intake", 2500 / 16, 156.25)
chk("m", (0.5 * 80, 2.0 / 50 * 100, 70 * 50, 8.0 * 1), (40.0, 4.0, 3500, 8.0))
chk("c", (round(cg(58, 56, 6.8), 1), 6.8 / 1.2, 0.5 * 56, round(61.5 - 56, 1), round((61.5 - 56) / 56 * 100, 1), 500 + 100, 56 * 50), (9.4, 6.8 / 1.2, 28.0, 5.5, 9.8, 600, 2800))
T.update(u1_cg="17.6", u1_cgf="29.5", u1_uo35=35, u1_uo6=210, u1_uorate="0.36", u1_kdigo="2.5", u1_clcr=50, u1_urr=70, u1_idwg="6.0",
         u1_fl=800, u1_bal="1,000", u1_cauti="3.2", u1_perh=156, u1_epo="3,000",
         u1_m1=40, u1_m2="4.0", u1_m3="3,500", u1_m4=75,
         c_cg="9.4", c_uo="28", c_gain="5.5", c_pct="9.8", c_fl=600, c_epo="2,800")
# ---- Unit 2: endocrine and diabetes nursing
eag = lambda a: 28.7 * a - 46.7
tdd = 0.5 * 70; cf = 1800 / tdd; icr = 500 / tdd
chk("d1", (round(eag(8.0)), round(eag(8.0) / 18, 1), round(78 / 1.65 ** 2, 1), tdd, tdd / 2, round(tdd / 2 / 3, 1), round(cf, 1), round((250 - 120) / cf, 1), round(icr, 1), round(60 / icr, 1)),
    (183, 10.2, 28.7, 35.0, 17.5, 5.8, 51.4, 2.5, 14.3, 4.2))
chk("dka", (130 - (94 + 8), round(130 + 1.6 * (600 - 100) / 100), round(2 * 130 + 600 / 18, 1), 0.1 * 70, round(1000 * 20 / 120), 50 * 0.5, 150 * 0.10, round(90 / 120, 2), round(1.6 * 60)),
    (28, 138, 293.3, 7.0, 167, 25.0, 15.0, 0.75, 96))
chk("m", (round(eag(7.0)), 140 - (104 + 24), 0.1 * 60, round(1.6 * 50)), (154, 12, 6.0, 80))
c_tdd = 0.5 * 68; c_cf = 1800 / c_tdd
chk("c", (round(eag(9.4)), round(68 / 1.55 ** 2, 1), c_tdd, round(c_cf, 1), round((340 - 140) / c_cf, 1), round(95 / 125, 2)), (223, 28.3, 34.0, 52.9, 3.8, 0.76))
T.update(u2_eag=183, u2_eagm="10.2", u2_bmi="28.7", u2_tdd=35, u2_basal="17.5", u2_bolus="5.8", u2_cf="51.4", u2_corr="2.5", u2_icr="14.3", u2_meal="4.2",
         u2_ag=28, u2_cna=138, u2_osm="293.3", u2_inf=7, u2_gtt=167, u2_d50=25, u2_d10=15, u2_abi="0.75", u2_thy=96,
         u2_m1=154, u2_m2=12, u2_m3=6, u2_m4=80, c2_eag=223, c2_bmi="28.3", c2_tdd=34, c2_cf="52.9", c2_corr="3.8", c2_abi="0.76")
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
