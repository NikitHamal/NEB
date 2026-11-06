#!/usr/bin/env python3
"""Adult Nursing I (BSN 9): compute and assert every number in the book.
   --print | --fill files | --verify files   (tokens via tokcommon; python blocks are executed and compared)."""
import sys, os, re, math, subprocess, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tokcommon

def chk(label, got, want):
    ok = got == want if not isinstance(got, float) else abs(got - want) < 1e-9
    if not ok: sys.exit(f"FAIL {label}: {got} != {want}")

T = {}
# ---- Unit 1: perioperative care
w = 60; chk("maint", (30*w, 30*w/24, 0.5*w), (1800, 75.0, 30.0))
chk("drip", (1000/8, round(1000/8*20/60, 1), round(1000/8*20/60)), (125.0, 41.7, 42))
ebv = 70*w; chk("abl", (ebv, ebv*(40-30)/40), (4200, 1050.0))
chk("news", 2+1+0+1+2+0+1, 7); chk("ald", 2+2+2+1+2, 9); chk("morph", 5/10, 0.5)
chk("m1", 30*70, 2100); chk("m2", 1000/10*15/60, 25.0); chk("m3", 0.5*80, 40.0); chk("m4", 4/10, 0.4)
chk("c maint", (30*62, 30*62/24, 0.5*62), (1860, 77.5, 31.0)); chk("c news", 0 + 0 + 0 + 0 + 1 + 0, 1)
T.update(u1_maint="1,800", u1_perh=75, u1_urine=30, u1_drip=42, u1_abl="1,050", u1_news=7, u1_ald=9, u1_morph="0.5",
         u1_m1="2,100", u1_m2=25, u1_m3=40, u1_m4="0.4", c_maint="1,860", c_perh="77.5", c_urine=31, c_news=1)
# ---- Unit 2: respiratory nursing
chk("pack", 10/20*30, 15.0); fv, fc, pr = 1.4, 2.9, 2.8
chk("spiro", (round(fv/fc, 2), round(fv/pr*100)), (0.48, 50)); chk("hco3", round(24 + 0.35*(58-40), 1), 30.3)
lit = (2000-500)*0.28; chk("cyl", (round(lit), round(lit/6), 21 + 4*3, 60/0.40), (420, 70, 33, 150.0)); chk("salb", 2.5/5, 0.5); chk("pred", 40//5, 8)
chk("curb", 1+1+1+1+1, 5); cl = (1800-500)*0.28
chk("c2", (round(cl), round(cl/2), int(cl/2//60), int(cl/2%60), 10/20*40, round(1.2/2.7, 2)), (364, 182, 3, 2, 20.0, 0.44))
chk("m1", 20/20*25, 25.0); chk("m2", 200/400*100, 50.0); chk("m3", (1500-500)*0.28/4, 70.0); chk("m4", 80/0.40, 200.0)
T.update(u2_packyr=15, u2_ratio="0.48", u2_pct=50, u2_hco3="30.3", u2_litres=420, u2_mins=70, u2_fio2=33, u2_pf=150, u2_salb="0.5", u2_curb=5, u2_pred=8,
         c2_litres=364, c2_min=182, c2_packyr=20, c2_ratio="0.44", u2_m1=25, u2_m2=50, u2_m3=70, u2_m4=200)
# ---- Unit 3: cardiovascular nursing
chk("bp", (150-94, round((150+2*94)/3, 1)), (56, 112.7)); chk("hr", (300/4, 1500/20, 12*10), (75.0, 75.0, 120))
chk("qtc", round(400/(60/75)**0.5), 447); chk("co", (75*70, round(70/120*100)), (5250, 58))
chk("drug", (40/10, 25000/500, 1000/50), (4.0, 50.0, 20.0))
chk("c3", (round((100+2*60)/3, 1), round(100/60*20), 1*70, 300//75, 80//40), (73.3, 33, 70, 4, 2))
chk("m1", round((120+2*80)/3, 1), 93.3); chk("m2", 300/6, 50.0); chk("m3", 20/10, 2.0); chk("m4", 1000/(25000/250), 10.0)
T.update(u3_pp=56, u3_map="112.7", u3_hr1=75, u3_hr2=75, u3_hr3=120, u3_qtc=447, u3_co="5,250", u3_ef=58, u3_furo=4, u3_hep=20,
         c3_map="73.3", c3_gtt=33, c3_enox=70, c3_asp=4, c3_ator=2, u3_m1="93.3", u3_m2=50, u3_m3=2, u3_m4=10)
# ---- Unit 4: GI and hepatobiliary
bv = 70*60; chk("bleed", (bv, round(0.35*bv), round(120/90, 2), round(0.35*bv*3)), (4200, 1470, 1.33, 4410))
chk("alv", 1+1+1+2+1+1+2+0, 9); chk("obs", (1800+1500, (1800+1500)/24), (3300, 137.5))
def cp_(bil, alb, inr, asc, enc):
    return (1 if bil < 2 else 2 if bil <= 3 else 3) + (1 if alb > 3.5 else 2 if alb >= 2.8 else 3) + (1 if inr < 1.7 else 2 if inr <= 2.3 else 3) + asc + enc
chk("cp", (cp_(1.2, 3.8, 1.2, 1, 1), cp_(3.4, 2.5, 1.8, 3, 2)), (5, 13))
chk("alb", (8*6, 8*6/0.20, round(2.5-0.8, 1), round(1.2*62, 1)), (48, 240.0, 1.7, 74.4))
chk("m", (70*80, round(110/100, 1), 8*7, round(2.8-0.9, 1)), (5600, 1.1, 56, 1.9))
T.update(u4_bv="4,200", u4_loss="1,470", u4_si="1.33", u4_crys="4,410", u4_alv=9, u4_total="3,300", u4_rate="137.5", u4_cpa=5, u4_cpc=13,
         u4_alb=48, u4_albml=240, u4_saag="1.7", u4_prot="74.4", u4_m1="5,600", u4_m2="1.1", u4_m3=56, u4_m4="1.9",
         c4_cp=13, c4_saag="1.7", c4_alb=48, c4_albml=240, c4_prot="74.4")
# ---- Unit 5: haematology and transfusion
import math
chk("idx", (round(24*10/3.6, 1), round(7.0*10/3.6, 1), round(7.0*100/24, 1), round(3*24/45, 1), round(55*(12-7.0)*2.4 + 500), 2000*20/100, 3*65),
    (66.7, 19.4, 29.2, 1.6, 1160, 400.0, 195))
bsa = math.sqrt(160*55/3600); chk("bsa", (round(bsa, 2), round(100*bsa), 50*50*0.5), (1.56, 156, 1250.0))
chk("tr", (350/3.5, round(350/3.5*15/60), 2*15), (100.0, 25, 30))
chk("c5", (round(200/3.1, 1), round(60/3.1, 1), round(600/20, 1), round(50*6*2.4 + 500), 70/50), (64.5, 19.4, 30.0, 1220, 1.4))
chk("m", (round(30*10/4.0), round(300/3*15/60), 60*40*0.5, 3000*10/100), (75, 25, 1200.0, 300.0))
T.update(u5_mcv="66.7", u5_mch="19.4", u5_mchc="29.2", u5_ret="1.6", u5_deficit="1,160", u5_anc=400, u5_elem=195, u5_bsa="1.56", u5_dose=156,
         u5_fviii="1,250", u5_rate=100, u5_gtt=25, u5_first=30, u5_m1=75, u5_m2=25, u5_m3="1,200", u5_m4=300,
         c5_mcv="64.5", c5_mch="19.4", c5_mchc="30.0", c5_def="1,220", c5_rise="1.4", c5_first=30, c5_elem=195)
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
