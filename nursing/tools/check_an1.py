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
