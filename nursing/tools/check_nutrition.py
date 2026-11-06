#!/usr/bin/env python3
"""Nutrition and Diet Therapy (BSN 8): compute and assert every number in the book.
   --print | --fill files | --verify files   (tokens via tokcommon; python blocks are executed and compared)."""
import sys, os, re, math, subprocess, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tokcommon

def chk(label, got, want):
    ok = got == want if not isinstance(got, float) else abs(got - want) < 1e-9
    if not ok: sys.exit(f"FAIL {label}: {got} != {want}")

T = {}
# ---- Unit 1: nutrition science, energy, assessment
def hb_(sex, w, h, a): return 88.362 + 13.397*w + 4.799*h + 5.677*a if sex == "M" else 447.593 + 9.247*w + 3.098*h + 4.330*a
def mj_(sex, w, h, a): return 10*w + 6.25*h - 5*a + (5 if sex == "M" else -161)
c_, p_, f_ = 95, 22, 18; kc = c_*4 + p_*4 + f_*9
chk("kcal", kc, 630); chk("pc", round(c_*4/kc*100, 1), 60.3); chk("pp", round(p_*4/kc*100, 1), 14.0); chk("pf", round(f_*9/kc*100, 1), 25.7)
chk("hb", round(hb_("F", 52, 155, 24), 1), 1512.5); chk("mj", round(mj_("F", 52, 155, 24), 1), 1207.8)
tee = hb_("F", 52, 155, 24)*1.55; chk("tee", round(tee), 2344)
chk("hbm", round(hb_("M", 68, 170, 30), 1), 1985.5); chk("mjm", round(mj_("M", 68, 170, 30), 1), 1597.5)
chk("prot", round(0.83*52, 1), 43.2); chk("water", (30*52, 35*52), (1560, 1820))
bmi = 52/1.55**2; whr = 88/98; chk("bmi", round(bmi, 1), 21.6); chk("whr", round(whr, 2), 0.90); chk("ibw", 155-100, 55)
chk("label", 8*9 + 37*4 + 3*4, 232)
chk("m1", 20*4 + 10*4 + 5*9, 165); chk("m2", round(70/1.75**2, 1), 22.9); chk("m3", 8*6.25, 50.0); chk("m4", (60-54)/60*100, 10.0)
cb = 41/1.52**2; cw = (47-41)/47*100; must = (2 if cb < 18.5 else 1 if cb < 20 else 0) + (2 if cw > 10 else 1 if cw >= 5 else 0)
chk("c_bmi", round(cb, 1), 17.7); chk("c_wl", round(cw, 1), 12.8); chk("must", must, 4); chk("c_kcal", 30*41, 1230); chk("c_prot", round(1.2*41, 1), 49.2)
chk("kcal per kg fat", 7700/7, 1100.0)
T.update(u1_kcal=kc, u1_pc=f"{c_*4/kc*100:.1f}", u1_pp=f"{p_*4/kc*100:.1f}", u1_pf=f"{f_*9/kc*100:.1f}", u1_hb=f"{hb_('F',52,155,24):.1f}", u1_mj=f"{mj_('F',52,155,24):.1f}",
         u1_tee="2,344", u1_hbm=f"{hb_('M',68,170,30):.1f}", u1_mjm=f"{mj_('M',68,170,30):.1f}", u1_prot=f"{0.83*52:.1f}", u1_water="1,560 to 1,820",
         u1_bmi=f"{bmi:.1f}", u1_whr=f"{whr:.2f}", u1_ibw=55, u1_label=232, u1_m1=165, u1_m2=f"{70/1.75**2:.1f}", u1_m3=50, u1_m4=10,
         c_bmi=f"{cb:.1f}", c_wl=f"{cw:.1f}", c_must=must, c_kcal=1230, c_prot=f"{1.2*41:.1f}")
# ---- Unit 2: vitamins, minerals, deficiency disorders
b611 = 840 * 0.5; b1259 = 840 * 4; caps = (b611 + b1259) * 2; iu = b611 * 100000 + b1259 * 200000
chk("vitA", (b611, b1259, caps, iu), (420.0, 3360, 7560.0, 714000000.0))
iod = 5 * 30 / 1000 * 1000; salt_pg = 250 / 30; chk("iodine", (iod, round(salt_pg, 1)), (150.0, 8.3))
chk("fe180", 60 * 180, 10800); chk("fs", 325 * 0.20, 65.0)
deficit = 52 * (12 - 8) * 2.4 + 500; days = math.ceil(deficit / 6); chk("deficit", (round(deficit, 1), days), (999.2, 167))
chk("vitD", (400 / 40, 300000 / 40), (10.0, 7500.0)); chk("milk", round(1000 / 120 * 100), 833)
ne = 12 + 600 / 60; chk("ne", ne, 22.0); chk("c2tot", 3 * 200000, 600000)
chk("m2", 200 * 0.33, 66.0); chk("m3", 5 * 15 / 1000 * 1000, 75.0); chk("m4", 8 + 300 / 60, 13.0)
T.update(u2_c611=round(b611), u2_c1259="3,360", u2_caps="7,560", u2_iu="714,000,000", u2_iod=150, u2_saltpg=f"{salt_pg:.1f}", u2_fe180="10,800",
         u2_def=f"{deficit:.1f}".split(".")[0] if False else "999", u2_days=days, u2_milk=833, u2_d=10, u2_stoss="7,500", u2_ne=f"{ne:.0f}",
         c2_tot="600,000", u2_m2=f"{200*0.33:.0f}", u2_m3=75, u2_m4=13)
# ---- Unit 3: life cycle, infant feeding, PEM
pb = 48/1.54**2; chk("preg bmi", round(pb, 1), 20.2)
cf = [615-413, 686-379, 894-346]; chk("cf", cf, [202, 307, 548])
vol = 150*4.8; chk("milk", (vol, vol/8), (720.0, 90.0))
rk = 200*8.0; chk("rutf", (rk, rk/500, math.ceil(rk/500*7), 130*8.0, 130*8.0/8, 200*8.0, 5*8.0), (1600.0, 3.2, 23, 1040.0, 130.0, 1600.0, 40.0))
chk("gomez", round(6.2/9.6*100, 1), 64.6)
chk("m1", 200*6/500, 2.4); chk("m2", 130*5, 650); chk("m3", 5.0/8.0*100, 62.5)
f75 = 130*7.2; chk("c3 f75", (round(f75), round(f75/8), round(200*7.2), round(200*7.2/500, 1), 5*7.2), (936, 117, 1440, 2.9, 36.0))
T.update(u3_bmi=f"{pb:.1f}", u3_cf6=cf[0], u3_cf9=cf[1], u3_cf12=cf[2], u3_milk=720, u3_feed=90, u3_rutf="1,600", u3_sach="3.2", u3_week=23,
         u3_f75="1,040", u3_f75f=130, u3_f100="1,600", u3_gain=40, u3_gomez="64.6", u3_m1="2.4", u3_m2=650, u3_m3="62.5",
         c3_f75=936, c3_f75f=117, c3_rutf="1,440", c3_sach="2.9", c3_gain=36)
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
