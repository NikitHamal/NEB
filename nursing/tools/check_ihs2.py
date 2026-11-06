#!/usr/bin/env python3
"""Integrated Health Sciences II (BSN 2-3): compute and assert every number in the book.
   --print | --fill files | --verify files   (tokens via tokcommon; python blocks are executed and compared)."""
import sys, os, re, math, subprocess, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tokcommon

def chk(label, got, want):
    ok = got == want if not isinstance(got, float) else abs(got - want) < 1e-9
    if not ok: sys.exit(f"FAIL {label}: {got} != {want}")

T = {}
mapf = lambda s, d: (s + 2 * d) / 3
# ---- Unit 1: nervous system and special senses
csf = 0.35 * 1440
nernst = 61.5 * math.log10(5 / 150)
m1 = mapf(130, 80); cpp = m1 - 25; cpp45 = m1 - 45
chk("csf", round(csf), 504); chk("nernst", round(nernst, 1), -90.8)
chk("map1", round(m1, 1), 96.7); chk("cpp", round(cpp, 1), 71.7); chk("cpp45", round(cpp45, 1), 51.7)
gcs1 = 3 + 4 + 5; gcs2 = 1 + 2 + 3
power = 43 + 19; focal = 1000 / power; myopia = -1 / 0.40; f25 = 100 / 2.5
chk("gcs", (gcs1, gcs2), (12, 6)); chk("power", power, 62); chk("myopia", myopia, -2.5); chk("f25", f25, 40.0)
cm = mapf(150, 90); ccpp = cm - 28; mg = 0.5 * 60; mml = mg / 0.2; drip = mml * 15 / 20
chk("case map", cm, 110.0); chk("case cpp", ccpp, 82.0); chk("mannitol", (mg, mml), (30.0, 150.0)); chk("drip", drip, 112.5)
chk("gcs case", (2 + 2 + 4, 1 + 2 + 4), (8, 7))
T.update(u1_csf=round(csf), u1_nernst=f"{nernst:.1f}", u1_map=f"{m1:.1f}", u1_cpp=f"{cpp:.1f}", u1_cpp45=f"{cpp45:.1f}",
         u1_gcs1=gcs1, u1_gcs2=gcs2, u1_eye_power=power, u1_eye_f=f"{focal:.1f}", u1_myopia=f"{myopia:.2f}", u1_f25=f"{f25:.0f}",
         c_gcs1=8, c_gcs2=7, c_map=f"{cm:.1f}", c_cpp=f"{ccpp:.1f}", c_mann_g=f"{mg:.0f}", c_mann_ml=f"{mml:.0f}", c_drip=math.ceil(drip))
# ---- Unit 2: endocrine
iod = 5 * 30
a1c = 7.0; eag = 28.7 * a1c - 46.7; tdd = 0.5 * 60; cf = 1800 / tdd; icr = 500 / tdd; corr = (250 - 110) / cf
chk("iodine", iod, 150); chk("eag", round(eag, 1), 154.2); chk("eag mmol", round(eag / 18.016, 1), 8.6)
chk("tdd", tdd, 30.0); chk("cf", cf, 60.0); chk("icr", round(icr, 1), 16.7); chk("corr", round(corr, 1), 2.3)
chk("a1c from eag 200", round((200 + 46.7) / 28.7, 1), 8.6)
chk("g126", round(126 / 18.016, 1), 7.0); chk("g200", round(200 / 18.016, 1), 11.1)
ag = 132 - (96 + 8); cna = 132 + 0.016 * (480 - 100); osm = 2 * 132 + 480 / 18.016
chk("ag", ag, 28); chk("cna", round(cna, 1), 138.1); chk("osm", round(osm, 1), 290.6); chk("glmm", round(480 / 18.016, 1), 26.6)
gtt = 1000 * 15 / 60; ins = 0.1 * 70
chk("gtt", gtt, 250.0); chk("ins", ins, 7.0); chk("ins mL/h", ins / (50 / 50), 7.0)
T.update(u2_iodine=iod, u2_eag=f"{eag:.1f}", u2_eag_mmol=f"{eag / 18.016:.1f}", u2_tdd=f"{tdd:.0f}", u2_basal=f"{tdd / 2:.0f}",
         u2_icr=f"{icr:.1f}", u2_cf=f"{cf:.1f}", u2_corr=f"{corr:.1f}", u2_g126=f"{126 / 18.016:.1f}", u2_g200=f"{200 / 18.016:.1f}",
         c_ag=ag, c_cna=f"{cna:.1f}", c_osm=f"{osm:.1f}", c_gl_mmol=f"{480 / 18.016:.1f}", c_gtt=f"{gtt:.0f}", c_ins=f"{ins:.0f}")
# ---- Unit 3: renal, fluids, acid-base
cg = (140 - 60) * 70 / (72 * 1.4); cgf = (140 - 55) * 55 / (72 * 1.1) * 0.85
lit = 125 * 1440 / 1000; reab = (1 - 1.5 / lit) * 100; clr = 120 * 1 / 1.0
tbw = 0.6 * 60; m18 = 4 * 10 + 2 * 8; m70 = 40 + 20 + 50; uo = 0.5 * 70; winter = 1.5 * 14 + 8
fwd = 0.6 * 60 * (160 / 140 - 1); na8 = 0.6 * 60 * 8 / 0.513
chk("cg", round(cg, 1), 55.6); chk("cgf", round(cgf, 1), 50.2); chk("lit", lit, 180.0); chk("reab", round(reab, 1), 99.2)
chk("clr", clr, 120.0); chk("tbw", (tbw, tbw * 2 / 3, tbw / 3, tbw / 4, tbw / 12), (36.0, 24.0, 12.0, 9.0, 3.0))
chk("m18", m18, 56); chk("m70", m70, 110); chk("uo", uo, 35.0); chk("winter", winter, 29.0)
chk("fwd", round(fwd, 1), 5.1); chk("na8", round(na8), 561)
ccg = (140 - 58) * 60 / (72 * 6.5); ufr = 3000 / 4; ufkg = ufr / 60; dex = 25 / 0.5; fl = 200 + 500
chk("ccg", round(ccg, 1), 10.5); chk("ufkg", ufkg, 12.5); chk("dex", dex, 50.0); chk("ufkg<13", ufkg < 13, True)
T.update(u3_litres=f"{lit:.0f}", u3_reab=f"{reab:.1f}", u3_cg=f"{cg:.1f}", u3_cg_f=f"{cgf:.1f}", u3_clear=f"{clr:.0f}",
         u3_tbw=f"{tbw:.0f}", u3_icf=f"{tbw * 2 / 3:.0f}", u3_ecf=f"{tbw / 3:.0f}", u3_int=f"{tbw / 4:.0f}", u3_plasma=f"{tbw / 12:.0f}",
         u3_m18=m18, u3_m70=m70, u3_uo=f"{uo:.0f}", u3_winter=f"{winter:.0f}", u3_fwd=f"{fwd:.1f}", u3_na8=f"{na8:.0f}",
         c3_crcl=f"{ccg:.1f}", c3_dex=f"{dex:.0f}", c3_ufkg=f"{ufkg:.1f}", c3_fluid=fl)
# ---- Unit 4: reproductive system and early pregnancy
from datetime import date, timedelta
lmp = date(2025, 6, 1); edd = lmp + timedelta(days=280); gdays = (date(2025, 10, 12) - lmp).days
naeg = date(2026, 3, 8)                       # LMP + 7 days + 9 months
chk("naegele == 280 d", edd, naeg); chk("ga", (gdays // 7, gdays % 7), (19, 0))
pearl = 3 * 1200 / (500 * 12); gan = 55 * (11 - 9.5) * 2.4 + 500; left = 280 - gdays
chk("pearl", pearl, 0.6); chk("ganzoni", round(gan), 698); chk("days left", left, 147); chk("tablets enough", 180 >= left, True)
chk("ov", (28 - 14, 32 - 14), (14, 18))
T.update(u4_ov28=28 - 14, u4_ov32=32 - 14, u4_ga_w=gdays // 7, u4_pearl=f"{pearl:.1f}", u4_edd=edd.strftime("%d %b %Y"),
         c4_ganzoni=f"{gan:.0f}", c4_days=left)
# ---- Unit 5: musculoskeletal, skin, burns
park = 4 * 70 * 40; h8 = park / 2 / 8; h16 = park / 2 / 16; tsc = (0.62 - 0.94) / 0.12; crutch = 170 - 40
chk("park", (park, h8, h16), (11200, 700.0, 350.0)); chk("tscore", round(tsc, 2), -2.67); chk("crutch", crutch, 130)
chk("osteoporosis", tsc <= -2.5, True)
tb = 18 + 9 + 9; ctot = 4 * 55 * tb; chalf = ctot / 2; c8 = chalf / 8; c16 = chalf / 16; cgtt = chalf / 6 * 20 / 60; cuo = 0.5 * 55; ccal = 25 * 55 + 40 * tb
chk("burn", (tb, ctot, chalf, c8, c16), (36, 7920, 3960.0, 495.0, 247.5)); chk("gtt", cgtt, 220.0); chk("uo", cuo, 27.5); chk("curreri", ccal, 2815)
chk("remaining 6h rate", round(chalf / 6), 660)
T.update(u5_crutch=crutch, u5_park=park, u5_h8=f"{h8:.0f}", u5_h16=f"{h16:.0f}", u5_t=f"{tsc:.2f}",
         c5_tbsa=tb, c5_total=ctot, c5_half=f"{chalf:.0f}", c5_h8=f"{c8:.0f}", c5_h16=f"{c16}", c5_gtt=f"{cgtt:.0f}", c5_h6=f"{chalf / 6:.0f}", c5_uo=f"{cuo}", c5_cal=ccal)
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
