#!/usr/bin/env python3
"""Community Health Nursing (BSN 6-7): compute and assert every number in the book.
   --print | --fill files | --verify files   (tokens via tokcommon; python blocks are executed and compared)."""
import sys, os, re, math, subprocess, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tokcommon

def chk(label, got, want):
    ok = got == want if not isinstance(got, float) else abs(got - want) < 1e-9
    if not ok: sys.exit(f"FAIL {label}: {got} != {want}")

T = {}
# ---- Unit 1: PHC, health system, community diagnosis
pop = 42000; wards = 9; fchv = 27
births = pop * 20 / 1000; preg = births * 1.1; u5 = pop * 0.10; wra = pop * 0.24
per_fchv = pop / fchv; per_ward = pop / wards; interval = pop / 30; cl_children = 30 * 7
chk("births", births, 840.0); chk("preg", round(preg), 924); chk("u5", u5, 4200.0); chk("wra", wra, 10080.0)
chk("per_fchv", round(per_fchv), 1556); chk("per_ward", round(per_ward), 4667); chk("interval", interval, 1400.0); chk("cl", cl_children, 210)
anc = 616 / 924 * 100; sba = 588 / 840 * 100; gap = 840 - 588
chk("anc", round(anc, 1), 66.7); chk("sba", sba, 70.0); chk("gap", gap, 252)
T.update(u1_pop="42,000", u1_births=round(births), u1_preg=round(preg), u1_u5="4,200", u1_wra="10,080", u1_perfchv=round(per_fchv),
         u1_perward=round(per_ward), u1_interval="1,400", u1_cluster=cl_children, c_anc=f"{anc:.1f}", c_sba=f"{sba:.1f}", c_gap=gap)
# ---- Unit 2: epidemiology and biostatistics
ir = 150 / 20000 * 1000; pv = 300 / 20000 * 1000
chk("ir", round(ir, 1), 7.5); chk("pv", round(pv, 1), 15.0)
live = 8400; imr = 235 / live * 1000; nmr = 168 / live * 1000; mmr = 13 / live * 1e5
chk("imr", round(imr, 1), 28.0); chk("nmr", round(nmr, 1), 20.0); chk("mmr", round(mmr, 1), 154.8)
rr = (150 / 1000) / (100 / 2000); ar = 150 / 1000 - 100 / 2000; arp = ar / (150 / 1000) * 100
chk("rr", rr, 3.0); chk("ar", round(ar, 2), 0.10); chk("arp", round(arp, 1), 66.7)
orr = (60 * 70) / (40 * 30); chk("or", orr, 3.5)
tp, fn = 90, 10; tn, fp = 720, 180
sens = tp / (tp + fn); spec = tn / (tn + fp); ppv = tp / (tp + fp); npv = tn / (tn + fn); acc = (tp + tn) / 1000
chk("sens", sens, 0.9); chk("spec", spec, 0.8); chk("ppv", round(ppv * 100, 1), 33.3); chk("npv", round(npv * 100, 1), 98.6); chk("acc", acc, 0.81)
xs = [10.2, 11.5, 9.8, 12.1, 10.9, 10.8, 9.5, 12.4]
mean = sum(xs) / 8; sd = math.sqrt(sum((x - mean) ** 2 for x in xs) / 7); se = sd / math.sqrt(8); lo, hi = mean - 2.365 * se, mean + 2.365 * se
chk("mean", round(mean, 2), 10.9); chk("sd", round(sd, 2), 1.05); chk("se", round(se, 2), 0.37); chk("ci", (round(lo, 1), round(hi, 1)), (10.0, 11.8))
chi = 400 * (10 * 160 - 190 * 40) ** 2 / (200 * 200 * 50 * 350); chk("chi", round(chi, 2), 20.57)
n1 = n2 = 10; m1, s1, m2, s2 = 11.2, 1.1, 9.9, 1.3
sp = math.sqrt(((n1 - 1) * s1 ** 2 + (n2 - 1) * s2 ** 2) / (n1 + n2 - 2)); tt = (m1 - m2) / (sp * math.sqrt(1 / n1 + 1 / n2))
chk("sp", round(sp, 3), 1.204); chk("t", round(tt, 2), 2.41)
nss = 1.96 ** 2 * 0.5 * 0.5 / 0.05 ** 2; nadj = math.ceil(math.ceil(nss) / 0.9)
chk("nss", math.ceil(nss), 385); chk("nadj", nadj, 428)
T.update(u2_ir=f"{ir:.1f}", u2_pv=f"{pv:.1f}", u2_imr=f"{imr:.1f}", u2_nmr=f"{nmr:.1f}", u2_mmr=f"{mmr:.1f}", u2_rr=f"{rr:.1f}", u2_ar=f"{ar:.2f}",
         u2_arp=f"{arp:.1f}", u2_or=f"{orr:.1f}", u2_ppv=f"{ppv * 100:.1f}", u2_npv=f"{npv * 100:.1f}", u2_acc=f"{acc * 100:.0f}",
         u2_mean=f"{mean:.1f}", u2_sd=f"{sd:.2f}", u2_se=f"{se:.2f}", u2_lo=f"{lo:.1f}", u2_hi=f"{hi:.1f}", u2_chi=f"{chi:.2f}", u2_sp=f"{sp:.3f}", u2_t=f"{tt:.2f}",
         u2_n=math.ceil(nss), u2_nadj=nadj)
# ---- Unit 3: communicable disease, immunisation, TB, vectors
ve = (0.02 - 0.002) / 0.02 * 100; hit15 = (1 - 1 / 15) * 100; hit6 = (1 - 1 / 6) * 100
chk("ve", round(ve), 90); chk("hit15", round(hit15, 1), 93.3); chk("hit6", round(hit6, 1), 83.3)
bcg = 840 * 1 / (1 - 0.5); bcgv = bcg / 20; mr = 840 * 2 / (1 - 0.25); mrv = mr / 10
chk("bcg", bcg, 1680.0); chk("bcgv", bcgv, 84.0); chk("mr", round(mr), 2240); chk("mrv", round(mrv), 224)
fic = 672 / 840 * 100; drop = (826 - 780) / 826 * 100; dropmr = (826 - 744) / 826 * 100
chk("fic", fic, 80.0); chk("drop", round(drop, 1), 5.6); chk("dropmr", round(dropmr, 1), 9.9)
fdc = 4; ip = 56 * fdc; cp = 112 * fdc; tbdoses = 56 + 112
chk("tb", (ip, cp, tbdoses), (224, 448, 168))
hi = 10 / 80 * 100; ci = 12 / 60 * 100; bi = 12 / 80 * 100; spr = 36 / 400 * 100; api = 45 / 15000 * 1000
chk("indices", (hi, ci, bi, spr, api), (12.5, 20.0, 15.0, 9.0, 3.0))
ar_all = 48 / 1200 * 100; cfr = 3 / 48 * 100; av = 12 / 900 * 100; au = 36 / 300 * 100; cve = (au - av) / au * 100
chk("outbreak", (ar_all, round(cfr, 2), round(av, 2), au, round(cve, 1)), (4.0, 6.25, 1.33, 12.0, 88.9))
T.update(u3_ve=f"{ve:.0f}", u3_hit15=f"{hit15:.1f}", u3_hit6=f"{hit6:.1f}", u3_bcg="1,680", u3_bcgv=f"{bcgv:.0f}", u3_mr="2,240", u3_mrv=f"{mrv:.0f}",
         u3_fic=f"{fic:.0f}", u3_drop=f"{drop:.1f}", u3_dropmr=f"{dropmr:.1f}", u3_ip=ip, u3_cp=cp, u3_tbdoses=tbdoses,
         u3_hi=f"{hi:.1f}", u3_ci=f"{ci:.0f}", u3_bi=f"{bi:.0f}", u3_spr=f"{spr:.0f}", u3_api=f"{api:.1f}",
         c3_ar=f"{ar_all:.1f}", c3_cfr=f"{cfr:.2f}", c3_av=f"{av:.2f}", c3_au=f"{au:.1f}", c3_ve=f"{cve:.1f}")
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
