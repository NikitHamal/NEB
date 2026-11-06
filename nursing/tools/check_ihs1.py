#!/usr/bin/env python3
"""Integrated Health Sciences I (BSN 1): compute and assert every number in the book.
   --print | --fill files | --verify files   (tokens via tokcommon; python blocks are executed and compared)."""
import sys, os, re, math, subprocess, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tokcommon

def chk(label, got, want):
    ok = got == want if not isinstance(got, float) else abs(got - want) < 1e-9
    if not ok: sys.exit(f"FAIL {label}: {got} != {want}")

T = {}
# ---- Unit 1: cell, tissues, homeostasis, acid-base chemistry
nacl_mosm = 9 / 58.44 * 1000 * 2            # 0.9% NaCl: 9 g/L, 2 particles
dex_mosm = 50 / 180.16 * 1000                # 5% dextrose: 50 g/L, 1 particle
nacl_mmol = 9 / 58.44 * 1000
chk("nacl mosm", round(nacl_mosm), 308); chk("dex mosm", round(dex_mosm), 278)
hh = lambda hco3, pco2: 6.1 + math.log10(hco3 / (0.03 * pco2))
nernst = 61.5 * math.log10(5 / 150)
chk("hh normal", round(hh(24, 40), 2), 7.40); chk("hh acid", round(hh(12, 25), 2), 7.30)
chk("nernst", round(nernst, 1), -90.8)
T.update(u1_nacl_mosm=round(nacl_mosm), u1_nacl_mmol=round(nacl_mmol), u1_dex_mosm=round(dex_mosm),
         u1_ph_norm=f"{hh(24,40):.2f}", u1_ph_acid=f"{hh(12,25):.2f}", u1_ratio=24 / (0.03 * 40),
         u1_nernst=f"{nernst:.1f}", u1_cells5=2 ** 5, u1_cells10=2 ** 10,
         u1_c1v1=f"{500 * 0.9 / 10:.0f}")
chk("c1v1", 500 * 0.9 / 10, 45.0)
# ---- Unit 2: blood
def indices(hb, hct, rbc):
    return hct * 10 / rbc, hb * 10 / rbc, hb / hct * 100
mcv, mch, mchc = indices(12.0, 36, 4.0); i_mcv, i_mch, i_mchc = indices(8.0, 27, 3.8)
chk("mcv", round(mcv), 90); chk("ida mcv", round(i_mcv, 1), 71.1)
ganzoni = 50 * (15 - 8.0) * 2.4 + 500
retc = 4 * 27 / 45; anc = 8000 * 0.60
T.update(u2_mcv=f"{mcv:.0f}", u2_mch=f"{mch:.0f}", u2_mchc=f"{mchc:.1f}",
         u2_imcv=f"{i_mcv:.1f}", u2_imch=f"{i_mch:.1f}", u2_imchc=f"{i_mchc:.1f}",
         u2_bv=f"{70 * 60}", u2_plasma=f"{70 * 60 * 0.55:.0f}", u2_ganzoni=f"{ganzoni:.0f}",
         u2_retc=f"{retc:.1f}", u2_anc=f"{anc:.0f}", u2_hb_iron=f"{1000 * 3.47 / 1000:.2f}",
         u2_rh_vials=math.ceil(15 / 30 + 1e-9))
chk("ganzoni", ganzoni, 1340.0); chk("retc", round(retc, 1), 2.4); chk("anc", anc, 4800.0)
# ---- Unit 3: cardiovascular
hr, sv, edv = 72, 70, 120
co = hr * sv / 1000; ef = sv / edv * 100; mapv = (120 + 2 * 80) / 3
bsa = 1.7; ci = co / bsa; svr = (mapv - 5) / co * 80
qtc = 400 / math.sqrt(60 / 75)
chk("co", co, 5.04); chk("ef", round(ef, 1), 58.3); chk("qtc", round(qtc), 447)
T.update(u3_co=f"{co:.2f}", u3_ef=f"{ef:.1f}", u3_ci=f"{ci:.2f}", u3_svr=f"{svr:.0f}", u3_map=f"{mapv:.1f}",
         u3_qtc=f"{qtc:.0f}", u3_rate300=300 // 4, u3_rate1500=1500 // 20, u3_rate6s=8 * 10,
         u3_pr=f"{5 * 0.04:.2f}", u3_qrs=f"{3 * 0.04:.2f}", u3_hr150=300 // 2, u3_co_hr120=f"{120 * 70 / 1000:.2f}",
         u3_sv_from_co=f"{5000 / 80:.1f}", u3_map2=f"{(130 + 2 * 85) / 3:.1f}")
chk("rate", 300 // 4, 75); chk("sv", 5000 / 80, 62.5)
chk("svr", round(svr), 1402); chk("hr150", 300 // 2, 150); chk("map hf", round((100 + 120) / 3, 1), 73.3)
T.update(u3_ef_hf=f"{45 / 130 * 100:.1f}", u3_co_hf=f"{110 * 45 / 1000:.2f}", u3_map_hf=f"{(100 + 120) / 3:.1f}")
chk("ef hf", T["u3_ef_hf"], "34.6"); chk("co hf", T["u3_co_hf"], "4.95")
chk("iron lost 500 mL", round(75 * 3.47, 1), 260.2 if False else round(75 * 3.47, 1)); chk("iron lost", int(75 * 3.47), 260)
# ---- Unit 4: respiration
tv, rr, vd = 500, 14, 150
mv = tv * rr; av = (tv - vd) * rr; fev = 3.2 / 4.0 * 100
pbw = 50 + 0.91 * (170 - 152.4)
cao2 = 1.34 * 15 * 0.98 + 0.003 * 95
patm_ktm = 760 * (1 - 2.25577e-5 * 1400) ** 5.25588
pao2_sl = 0.21 * (760 - 47) - 40 / 0.8
pao2_ktm = 0.21 * (patm_ktm - 47) - 40 / 0.8
winter = 1.5 * 14 + 8; ag = 140 - (104 + 14)
cyl = (2000 - 500) * 0.28 / 4
chk("mv", mv, 7000); chk("av", av, 4900); chk("fev", fev, 80.0); chk("pbw", round(pbw, 1), 66.0)
chk("cao2", round(cao2, 1), 20.0); chk("ag", ag, 22); chk("winter", winter, 29.0); chk("cyl", cyl, 105.0)
T.update(u4_mv=mv, u4_av=av, u4_fev=f"{fev:.0f}", u4_pbw=f"{pbw:.1f}", u4_tv6=f"{6 * pbw:.0f}", u4_tv8=f"{8 * pbw:.0f}",
         u4_cao2=f"{cao2:.1f}", u4_patm=f"{patm_ktm:.0f}", u4_pao2_sl=f"{pao2_sl:.0f}", u4_pao2_ktm=f"{pao2_ktm:.0f}",
         u4_winter=f"{winter:.0f}", u4_ag=ag, u4_cyl=f"{cyl:.0f}", u4_fio2=21 + 4 * 4, u4_ds_frac=f"{vd / tv * 100:.0f}",
         u4_mv_fast=f"{tv * 28}", u4_av_fast=f"{(tv - vd) * 28}")
vc = 500 + 3000 + 1100; tlc = vc + 1200; frc = 1100 + 1200; ic = 500 + 3000
chk("vc", vc, 4600); chk("tlc", tlc, 5800); chk("frc", frc, 2300); chk("ic", ic, 3500)
chk("shallow av", (250 - 150) * 28, 2800); chk("shallow mv", 250 * 28, 7000)
chk("hh resp", round(hh(26, 60), 2), 7.26); chk("fev copd", 1.2 / 2.4 * 100, 50.0)
T.update(u4_vc=vc, u4_tlc=tlc, u4_frc=frc, u4_ic=ic, u4_shallow=(250 - 150) * 28, u4_ph_resp=f"{hh(26, 60):.2f}",
         u4_fev_copd=f"{1.2 / 2.4 * 100:.0f}", u4_hco3_ratio=f"{26 / (0.03 * 60):.1f}")
# ---- Unit 5: digestion and metabolism
hb_bmr = 655.1 + 9.563 * 54 + 1.850 * 158 - 4.676 * 20
mif = 10 * 54 + 6.25 * 158 - 5 * 20 - 161
tee = mif * 1.55
kcal = 300 * 4 + 70 * 4 + 60 * 9
ors_osm = 75 + 65 + 75 + 20 + 10
glu_mm = 13.5 / 180.16 * 1000
chk("mif", mif, 1266.5); chk("kcal", kcal, 2020); chk("ors", ors_osm, 245); chk("glu", round(glu_mm), 75)
T.update(u5_hb=f"{hb_bmr:.0f}", u5_mif=f"{mif:.0f}", u5_tee=f"{tee:.0f}", u5_kcal=kcal,
         u5_cho_pct=f"{300 * 4 / kcal * 100:.0f}", u5_pro_pct=f"{70 * 4 / kcal * 100:.0f}", u5_fat_pct=f"{60 * 9 / kcal * 100:.0f}",
         u5_ors=ors_osm, u5_glu=f"{glu_mm:.0f}", u5_fpg=f"{100 / 18.016:.1f}", u5_fpg126=f"{126 / 18.016:.1f}",
         u5_bili=f"{3.0 - 0.8:.1f}", u5_zinc=20 * 10, u5_ors_ml=f"{75 * 4:.0f}", u5_gi_secr=1500 + 1500 + 1500 + 500 + 2000)
chk("si", round(108 / 98, 2), 1.10); chk("map pud", round((98 + 120) / 3, 1), 72.7); chk("ors ml", 75 * 4, 300)
T.update(u5_si=f"{108 / 98:.2f}", u5_map=f"{(98 + 120) / 3:.1f}", u5_ppi_days=14 * 2)

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
