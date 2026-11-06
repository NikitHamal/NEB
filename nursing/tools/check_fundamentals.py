#!/usr/bin/env python3
"""Fundamentals of Nursing (BSN 4-5): compute and assert every number in the book.
   --print | --fill files | --verify files   (tokens via tokcommon; python blocks are executed and compared)."""
import sys, os, re, math, subprocess, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tokcommon

def chk(label, got, want):
    ok = got == want if not isinstance(got, float) else abs(got - want) < 1e-9
    if not ok: sys.exit(f"FAIL {label}: {got} != {want}")

T = {}
# ---- Unit 1: nursing workload (NHPPD)
beds, occ, nhppd = 24, 0.75, 4.0
pts = round(beds * occ); hrs = pts * nhppd; shifts = hrs / 8
chk("u1 pts", pts, 18); chk("u1 hrs", hrs, 72.0)
T.update(u1_pts=pts, u1_hrs=f"{hrs:.0f}", u1_shifts=f"{shifts:.0f}")
# ---- Unit 2: Braden scale (6-23; <=9 very high, 10-12 high, 13-14 moderate, 15-18 mild)
def braden(*s):
    assert len(s) == 6 and all(1 <= x <= 4 for x in s) and s[5] <= 3
    t = sum(s); r = ("VERY HIGH" if t <= 9 else "HIGH" if t <= 12 else "MODERATE" if t <= 14 else "MILD" if t <= 18 else "NO RISK")
    return t, r
b1 = braden(2, 2, 2, 2, 3, 1); b2 = braden(3, 3, 3, 3, 3, 2)
chk("braden1", b1, (12, "HIGH")); chk("braden2", b2, (17, "MILD"))
T.update(braden_total=b1[0], braden_risk=b1[1], braden2_total=b2[0], braden2_risk=b2[1], turns24=24 // 2)
# ---- Unit 3: vital signs
mapf = lambda s, d: (s + 2 * d) / 3
T.update(map1=f"{mapf(120,80):.1f}", map2=f"{mapf(90,60):.1f}", map3=f"{mapf(160,100):.1f}",
         pp1=120 - 80, pr15=18 * 4, rr30=9 * 2,
         c2f=f"{38.5*9/5+32:.1f}", f2c=f"{(98.6-32)*5/9:.1f}", f2c2=f"{(102.2-32)*5/9:.1f}",
         bmi=f"{54/1.58**2:.1f}", gcs=3 + 4 + 5, shock=f"{110/88:.2f}", io_bal=1850 - 1500)
chk("map1", T["map1"], "93.3"); chk("bmi", T["bmi"], "21.6"); chk("c2f", T["c2f"], "101.3")
# unit 3 case-study numbers quoted in the long answer (not tokens)
chk("case MAP", round(mapf(100, 60)), 73); chk("case SI", round(108/100, 2), 1.08)
chk("map2", T["map2"], "70.0"); chk("gcs", T["gcs"], 12)
# ---- Unit 4: infection control
chl_g = 0.5 / 35 * 1000; parts_water = 5 / 0.5 - 1; dil01 = 5000 * 0.1 / 5
chk("chl", round(chl_g, 2), 14.29); chk("parts", parts_water, 9.0)
T.update(chl_g=f"{chl_g:.2f}", chl_parts=f"{parts_water:.0f}", chl_10L=f"{10/ (5/0.5):.0f}",
         dil01_ml=f"{dil01:.0f}", ns_exp=f"{500*0.003:.1f}", ns_1000=f"{1000*0.003:.0f}")
# ---- Unit 5: medication maths
drip = 1000 * 20 / (8 * 60); micro = 125 * 60 / 60
T.update(tabs=500 // 250, liq_ml=f"{125/250*5:.1f}", gent_ml=f"{80/40:.1f}", para_mg=15 * 12,
         para_ml=f"{15*12/120*5:.1f}", drip_macro=round(drip), drip_exact=f"{drip:.2f}", drip_micro=f"{micro:.0f}",
         inf_hrs=f"{500/100:.0f}", young=f"{6/(6+12)*500:.1f}", bsa=f"{math.sqrt(110*18/3600):.2f}")
chk("drip", T["drip_macro"], 42); chk("bsa", T["bsa"], "0.74")

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
