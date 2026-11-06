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
# ---- Unit 3: neurological nursing
chk("n1", (2 + 3 + 4, round((110 + 2 * 70) / 3, 1), round((110 + 2 * 70) / 3 - 30, 1)), (9, 83.3, 53.3))
chk("n2", (0.9 * 70, round(0.9 * 70 * 0.1, 1), round(0.9 * 70 * 0.9, 1), 0.5 * 70, 0.5 * 70 / 20 * 100, round(175 * 15 / 30), 20 * 70, 1400 / 50, 10 / 5, 1 + 1 + 1 + 1),
    (63.0, 6.3, 56.7, 35.0, 175.0, 88, 1400, 28.0, 2.0, 4))
chk("nm", (3 + 4 + 5, 90 - 20, 0.9 * 80, 0.5 * 60 / 20 * 100), (12, 70, 72.0, 150.0))
chk("nc", (4 + 3 + 6, round((180 + 2 * 100) / 3, 1), round(0.9 * 64, 1), round(0.9 * 64 * 0.1, 1), round(0.9 * 64 * 0.9, 1), 0.5 * 64, 0.5 * 64 / 20 * 100, 7.5 + 4.5, 8.5 + 1),
    (13, 126.7, 57.6, 5.8, 51.8, 32.0, 160.0, 12.0, 9.5))
T.update(u3_gcs=9, u3_map="83.3", u3_cpp="53.3", u3_alt=63, u3_bolus="6.3", u3_inf="56.7", u3_man=35, u3_manml=175, u3_gtt=88, u3_phe="1,400", u3_phemin=28, u3_dzp=2, u3_cha=4,
         u3_m1=12, u3_m2=70, u3_m3=72, u3_m4=150, c3_gcs=13, c3_map="126.7", c3_alt="57.6", c3_bolus="5.8", c3_inf="51.8", c3_man=32, c3_manml=160, c3_end="12:00", c3_needle="09:00")
# ---- Unit 4: musculoskeletal and orthopaedic nursing
chk("o", (round((0.62 - 1.0) / 0.12, 1), round(0.1 * 60, 1), 170 - 40, 75 / 25, 15 * 60, 70 - 45, 70 * 60, round(1500 / 4200 * 100, 1), round(70 * 60 * 0.15)),
    (-3.2, 6.0, 130, 3.0, 900, 25, 4200, 35.7, 630))
chk("om", (round((0.75 - 1.0) / 0.10, 1), 158 - 40, 15 * 50, round(0.1 * 70, 1)), (-2.5, 118, 750, 7.0))
chk("oc", (70 * 62, round(1500 / (70 * 62) * 100, 1), round(0.1 * 62, 1), 15 * 62, 172 - 40, 80 - 50), (4340, 34.6, 6.2, 930, 132, 30))
T.update(u4_t="-3.2", u4_trac=6, u4_crutch=130, u4_diclo=3, u4_para=900, u4_dp=25, u4_ebv="4,200", u4_loss="35.7", u4_m1="-2.5", u4_m2=118, u4_m3=750, u4_m4=7,
         c4_ebv="4,340", c4_loss="34.6", c4_trac="6.2", c4_para=930, c4_crutch=132, c4_dp=30)
# ---- Unit 5: oncology and emergency nursing
import math
bsa = lambda h, w: round(math.sqrt(h * w / 3600), 2)
chk("on", (bsa(165, 60), round(600 * bsa(165, 60)), round(60 * bsa(165, 60), 1), round(2500 * 0.28), round(45 / 500 * 100, 1)), (1.66, 996, 99.6, 700, 9.0))
tb = 9 + 18 + 9
chk("em", (tb, 4 * 70 * tb, 4 * 70 * tb // 2, 4 * 70 * tb // 2 // 8, 4 * 70 * tb // 2 // 16, round(126 / 84, 1), round(2 / 0.6, 1), 2 + 4 + 8, 0.5 / 1.0),
    (36, 10080, 5040, 630, 315, 1.5, 3.3, 14, 0.5))
chk("m", (4 * 60 * 20 // 2, 4 * 60 * 20 // 2 // 8, round(3000 * 0.20), bsa(150, 54)), (2400, 300, 600, 1.5))
chk("c", (bsa(158, 52), round(600 * bsa(158, 52)), round(60 * bsa(158, 52), 1), round(1800 * 0.30), 30 * 52, 52 * 0.5), (1.51, 906, 90.6, 540, 1560, 26.0))
T.update(u5_bsa="1.66", u5_cyc=996, u5_doxo="99.6", u5_anc=700, u5_via="9.0", u5_tbsa=36, u5_park="10,080", u5_first="5,040", u5_rate=630, u5_rate2=315, u5_si="1.5", u5_atr="3.3", u5_atrcum=14, u5_adr="0.5",
         u5_m1="2,400", u5_m2=300, u5_m3=600, u5_m4="1.5", c5_bsa="1.51", c5_cyc=906, c5_doxo="90.6", c5_anc=540, c5_fl="1,560", c5_uo=26)
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
