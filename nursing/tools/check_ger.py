#!/usr/bin/env python3
"""Geriatric Nursing (BSN 11): compute and assert every number in the book.
   --print | --fill files | --verify files   (tokens via tokcommon; python blocks are executed and compared)."""
import sys, os, re, math, subprocess, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tokcommon

def chk(label, got, want):
    ok = got == want if not isinstance(got, float) else abs(got - want) < 1e-9
    if not ok: sys.exit(f"FAIL {label}: {got} != {want}")

T = {}
# ---- Unit 1: ageing, Nepal demography, CGA
_share = 2.97 / 29.16 * 100; _rise = (2.97 - 2.154) / 2.154 * 100
_t14 = math.log(14 / _share) / math.log(1.0329 / 1.0092)
chk("dem", (round(_share, 1), round(_rise, 1), round(70 / 3.29, 1), round(_t14, 1)), (10.2, 37.9, 21.3, 13.7))
_b = [10, 0, 5, 5, 10, 5, 10, 10, 10, 5]
chk("cga", (sum([0, 1, 1, 1, 0, 1]), sum(_b), round(4 / 6, 2), sum([0, 1, 1, 1, 1])), (4, 70, 0.67, 4))
chk("m", (round(2.97 / 29.16 * 100, 1), 4 / 8, round(60 * 60 / (72 * 1.2), 1)), (10.2, 0.5, 41.7))
_cg = (140 - 78) * 46 / (72 * 1.1) * 0.85
chk("c", (round(6 / 52 * 100, 1), round(46 / 1.5 ** 2, 1), round(_cg, 1), round(4 / 7, 2), 30 * 46, round(1.2 * 46)), (11.5, 20.4, 30.6, 0.57, 1380, 55))
T.update(u1_old="2.97", u1_share="10.2", u1_rise="37.9", u1_dbl="21.3", u1_t14="13.7", u1_katz=4, u1_barthel=70, u1_gait="0.67", u1_tug=14, u1_fried=4,
         u1_m1="10.2", u1_m2="0.50", u1_m3="41.7", c_loss="11.5", c_bmi="20.4", c_crcl="30.6", c_gait="0.57", c_kcal="1,380", c_prot=55)
# ---- Unit 2: falls, mobility, musculoskeletal
chk("f", (25 + 15 + 15 + 10, 140 - 108, 80 - 70, round(6 / 1500 * 1000, 1), f"{0.28 * 2.97e6:,.0f}", f"{0.35 * 2.97e6:,.0f}"), (65, 32, 10, 4.0, "831,600", "1,039,500"))
chk("h", (15 * 60, 1.5 * 60, 30 * 60, 36), (900, 90.0, 1800, 36))
chk("m", (25 + 15 + 20 + 20, 150 - 124, 15 * 40), (80, 26, 600))
chk("c", (150 - 118, 84 - 70, 25 + 15 + 20 + 20 + 15, 15 * 55, 1.5 * 55, 30 * 55, 24 + 8), (32, 14, 95, 825, 82.5, 1650, 32))
T.update(u2_lo="831,600", u2_hi="1,039,500", u2_morse=65, u2_sys=32, u2_dia=10, u2_rate="4.0", u2_para=900, u2_prot=90, u2_kcal="1,800", u2_hr=36,
         u2_m1=80, u2_m2=26, u2_m3=600, c2_sys=32, c2_dia=14, c2_morse=95, c2_hr=32, c2_para=825, c2_prot="82.5", c2_kcal="1,650")
# ---- Unit 3: delirium, dementia, depression
chk("lo", (f"{0.05 * 2.97e6:,.0f}", f"{0.08 * 2.97e6:,.0f}"), ("148,500", "237,600"))
chk("d", (0 + 2 + 1 + 4, round(0.5 / 5.0, 1)), (7, 0.1))
_tp, _fn, _fp, _tn = 45, 5, 20, 130
chk("acc", (round(_tp / (_tp + _fn) * 100, 1), round(_tn / (_tn + _fp) * 100, 1), round(_tp / (_tp + _fp) * 100, 1), round(_tn / (_tn + _fn) * 100, 1), (_tp + _fn) / 200 * 100, 2 + 2, 1 + 0), (90.0, 86.7, 69.2, 96.3, 25.0, 4, 1))
chk("m", (round(36 / 40 * 100), 10 * 28 // 5, round(0.5 / 5, 1)), (90, 56, 0.1))
chk("c", (30 * 58, 28 + 2 * 28, 14 * 7), (1740, 84, 98))
T.update(u3_lo="148,500", u3_hi="237,600", u3_4at=7, u3_hal="0.1", u3_sens="90.0", u3_spec="86.7", u3_ppv="69.2", u3_npv="96.3", u3_prev="25.0", u3_mc=4, u3_mc2=1,
         u3_m1=90, u3_m2=56, u3_m3="0.1", c3_tabs=84, c3_kcal="1,740", c3_fluid="1,740", c3_hrs=98)
# ---- Unit 4: medicines in older adults
_cg = lambda age, wt, cr, f=1.0: (140 - age) * wt / (72 * cr) * f
chk("pk", (round(_cg(84, 45, 1.2, 0.85), 1), 1.0 * 45, round(5 * 80 / 24, 1), round(5 * 20 / 24, 1), 3 + 1 + 1 + 1), (24.8, 45.0, 16.7, 4.2, 6))
chk("ad", ((60 - 12) / 60 * 100, 15 * 45, 60 * 45, f"{60 * 45:,}", round(500 * 20 / 360)), (80.0, 675, 2700, "2,700", 28))
chk("m", (round(_cg(80, 70, 1.0), 1), round(5 * 80 / 24, 1), round(250 * 20 / 240)), (58.3, 16.7, 21))
chk("c", (round(_cg(81, 52, 1.3), 1), 3 + 3 + 1, round(2.4 * 18), round(15 / 10 * 100), 4 * 2), (32.8, 7, 43, 150, 8))
T.update(u4_crcl="24.8", u4_enox=45, u4_ss="16.7", u4_ss20="4.2", u4_acb=6, u4_adh="80.0", u4_para=675, u4_max="2,700", u4_gtt=28, u4_m1="58.3", u4_m2="16.7", u4_m3=21,
         c4_crcl="32.8", c4_n=11, c4_acb=7, c4_mg=43, c4_d10=150, c4_taper=8)
# ---- Unit 5: pressure injury, incontinence, abuse, palliative care
chk("pi", (sum([3, 2, 1, 2, 2, 1]), 24 // 2, round(1.25 * 60), round(1.5 * 60), f"{30 * 60:,}", f"{35 * 60:,}", 5 * 4, 4 * 3, round((20 - 12) / 20 * 100, 1), f"{0.157 * 2.97e6:,.0f}"),
    (11, 12, 75, 90, "1,800", "2,100", 20, 12, 40.0, "466,290"))
chk("bl", (round(700 / 1800 * 100, 1), 112 - 25, 5 * 6, 5 * 6 / 6), (38.9, 87, 30, 5.0))
chk("m", (3 + 3 + 2 + 2 + 3 + 2, round(450 / 1200 * 100, 1), 60 / 6), (15, 37.5, 10.0))
chk("c", (2 + 1 + 1 + 1 + 2 + 1, 24 // 2, 1.5 * 48, 35 * 48, 3 * 2, (12 - 6) / 12 * 100, 146 - 30), (8, 12, 72.0, 1680, 6, 50.0, 116))
T.update(u5_abuse="466,290", u5_braden=11, u5_turns=12, u5_plo=75, u5_phi=90, u5_klo="1,800", u5_khi="2,100", u5_a0=20, u5_a1=12, u5_red="40.0", u5_npi="38.9", u5_pvr=180,
         u5_pad=87, u5_mor=30, u5_bt=5, u5_m1=15, u5_m2="37.5", u5_m3=10, c5_braden=8, c5_turns=12, c5_prot=72, c5_kcal="1,680", c5_fluid="1,680", c5_a0=12, c5_a1=6, c5_red="50.0", c5_pad=116)
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
