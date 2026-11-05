#!/usr/bin/env python3
"""BCA 305 Society and Technology: recompute every number (Moore growth, Cronbach alpha and TAM regression, Rogers adopter
categories from the normal curve, logistic and Bass diffusion, Gini/Lorenz and composite digital-divide index, ETA penalty table,
UN-style e-government index, fairness metrics from confusion matrices, PUE/energy/carbon).
    python3 bca/tools/check_society.py --print | --fill unit-*.md | --verify unit-*.md"""
import math, sys
import numpy as np
from tokcommon import table, inr, run
T = {}
phi = lambda x: 0.5 * (1 + math.erf(x / math.sqrt(2)))

# ---- Moore ----
T["moore_tab"] = table(["Year", "Years since 1971", "Doublings (÷ 2)", "Predicted transistors"], [(y, y - 1971, f"{(y-1971)/2:.1f}", f"{2300 * 2 ** ((y-1971)/2):,.0f}") for y in (1971, 1981, 1991, 2001, 2011, 2021)])
T["moore_2021"] = f"{2300 * 2 ** 25:,.0f}"; T["moore_x"] = f"{2**25:,.0f}"
dt = math.log(2) / math.log(1.41); T["moore_rate"] = f"{(2 ** 0.5 - 1) * 100:.1f}"

# ---- TAM survey ----
PU = np.array([[5,5,4,5],[4,4,4,3],[2,3,2,2],[5,4,5,5],[3,3,4,3],[4,5,4,4],[2,2,1,2],[3,4,3,3]])
PEOU = np.array([[4,4,5],[3,4,3],[2,2,3],[5,5,4],[3,2,3],[4,4,4],[2,1,2],[4,3,3]])
BI = np.array([5, 3, 2, 5, 3, 4, 1, 4])
def alpha(X):
    k = X.shape[1]; return k / (k - 1) * (1 - X.var(axis=0, ddof=1).sum() / X.sum(axis=1).var(ddof=1))
pu, pe = PU.mean(axis=1), PEOU.mean(axis=1)
T["tam_data"] = table(["Resp."] + [f"PU{i}" for i in range(1, 5)] + [f"PEOU{i}" for i in range(1, 4)] + ["BI", "PU mean", "PEOU mean"], [(i + 1, *PU[i], *PEOU[i], BI[i], f"{pu[i]:.2f}", f"{pe[i]:.2f}") for i in range(8)])
T["alpha_pu"] = f"{alpha(PU):.3f}"; T["alpha_peou"] = f"{alpha(PEOU):.3f}"
r_pu = np.corrcoef(pu, BI)[0, 1]; r_pe = np.corrcoef(pe, BI)[0, 1]; r_pp = np.corrcoef(pu, pe)[0, 1]
T["r_pu"] = f"{r_pu:.3f}"; T["r_pe"] = f"{r_pe:.3f}"; T["r_pp"] = f"{r_pp:.3f}"
X = np.column_stack([np.ones(8), pu, pe]); coef, *_ = np.linalg.lstsq(X, BI, rcond=None)
pred = X @ coef; r2 = 1 - ((BI - pred) ** 2).sum() / ((BI - BI.mean()) ** 2).sum()
T["tam_b0"] = f"{coef[0]:.3f}"; T["tam_b1"] = f"{coef[1]:.3f}"; T["tam_b2"] = f"{coef[2]:.3f}"; T["tam_r2"] = f"{r2:.3f}"
T["tam_pred"] = f"{coef[0] + coef[1] * 4 + coef[2] * 4:.2f}"

# ---- Rogers categories ----
cats = [("Innovators", -99, -2), ("Early adopters", -2, -1), ("Early majority", -1, 0), ("Late majority", 0, 1), ("Laggards", 1, 99)]
rg = []; rows = []
for n, a, b in cats:
    pa = phi(b) - phi(a) if abs(a) < 50 and abs(b) < 50 else (phi(b) if a < -50 else 1 - phi(a)); rg.append(pa)
rog_txt = ["2.5", "13.5", "34", "34", "16"]
T["rogers_tab"] = table(["Category", "Cut-offs (σ from mean adoption time)", "Normal-curve area", "Rogers' rounded share"],
                        [("Innovators", "below −2σ", f"{rg[0]*100:.2f}%", "2.5%"), ("Early adopters", "−2σ to −1σ", f"{rg[1]*100:.2f}%", "13.5%"),
                         ("Early majority", "−1σ to mean", f"{rg[2]*100:.2f}%", "34%"), ("Late majority", "mean to +1σ", f"{rg[3]*100:.2f}%", "34%"), ("Laggards", "above +1σ", f"{rg[4]*100:.2f}%", "16%")])
assert abs(sum(rg) - 1) < 1e-12
T["rg_inn"] = f"{rg[0]*100:.2f}"; T["rg_early_cum"] = f"{(rg[0]+rg[1])*100:.2f}"

# ---- logistic + Bass ----
K, rr, t0 = 100.0, 0.9, 6
T["log_tab"] = table(["Year t", "Adoption % = 100/(1 + e^(−0.9(t−6)))", "New adopters this year (points)"],
                     [(t, f"{K/(1+math.exp(-rr*(t-t0))):.1f}", "" if t == 0 else f"{K/(1+math.exp(-rr*(t-t0))) - K/(1+math.exp(-rr*(t-1-t0))):.1f}") for t in range(0, 13, 2) if True])
logv = [K / (1 + math.exp(-rr * (t - t0))) for t in range(0, 13)]
T["log_max"] = f"{K*rr/4:.1f}"; T["log_t0"] = "6"; T["log_0"] = f"{logv[0]:.1f}"
p, q, m = 0.03, 0.40, 500000
F = lambda t: (1 - math.exp(-(p + q) * t)) / (1 + (q / p) * math.exp(-(p + q) * t))
tstar = math.log(q / p) / (p + q); T["bass_tstar"] = f"{tstar:.2f}"; T["bass_F_tstar"] = f"{F(tstar)*100:.1f}"
T["bass_tab"] = table(["Year t", "Cumulative F(t)", "Cumulative adopters", "New adopters in year"], [(t, f"{F(t)*100:.1f}%", f"{m*F(t):,.0f}", f"{m*(F(t)-F(t-1)):,.0f}" if t else f"{m*F(0):,.0f}") for t in range(0, 13)])
ann = [m * (F(t) - F(t - 1)) for t in range(1, 13)]; peak_year = 1 + int(np.argmax(ann))
T["bass_peak_year"] = f"{peak_year}"; T["bass_peak_n"] = f"{max(ann):,.0f}"; T["bass_p_share"] = f"{p/(p+q)*100:.1f}"
T["bass_f1"] = f"{m*F(1):,.0f}"; T["bass_f12"] = f"{F(12)*100:.1f}"
# peak sales by continuous formula check
peak_cont = m * (p + q) ** 2 / (4 * q); T["bass_peak_cont"] = f"{peak_cont:,.0f}"
assert peak_cont >= max(ann) * 0.98

# ---- Gini / DDI ----
prov = [("Koshi", 4.97, 62, 21, 48, 42), ("Madhesh", 6.1, 41, 9, 35, 25), ("Bagmati", 6.1, 82, 40, 70, 68), ("Gandaki", 2.4, 70, 25, 58, 50),
        ("Lumbini", 5.1, 55, 15, 45, 38), ("Karnali", 1.7, 28, 4, 24, 20), ("Sudurpashchim", 2.7, 36, 6, 30, 27)]
tot = sum(r[1] for r in prov)
T["prov_tab"] = table(["Province (invented data)", "Population (million)", "Internet use %", "Fixed broadband per 100 homes", "Smartphone %", "Digital-skills %"], prov)
users = [(r[0], r[1], r[1] * r[2] / 100) for r in prov]; U = sum(u[2] for u in users)
srt = sorted(users, key=lambda u: u[2] / u[1]); cx = cy = 0; pts = [(0, 0)]; gsum = 0
rows = []
for n, pop, us in srt:
    nx, ny = cx + pop / tot, cy + us / U; gsum += (nx - cx) * (ny + cy); rows.append((n, f"{pop/tot*100:.1f}%", f"{us/U*100:.1f}%", f"{nx*100:.1f}%", f"{ny*100:.1f}%")); cx, cy = nx, ny
gini = 1 - gsum
T["lorenz_tab"] = table(["Province (poorest access first)", "Population share", "Internet-user share", "Cumulative population", "Cumulative users"], rows)
T["gini"] = f"{gini:.3f}"; T["national_use"] = f"{U/tot*100:.1f}"; T["users_m"] = f"{U:.2f}"; T["pop_m"] = f"{tot:.2f}"
mn = lambda i: min(r[i] for r in prov); mx = lambda i: max(r[i] for r in prov)
ddi = {r[0]: np.mean([(r[i] - mn(i)) / (mx(i) - mn(i)) for i in (2, 3, 4, 5)]) for r in prov}
T["ddi_tab"] = table(["Province", "Internet", "Broadband", "Smartphone", "Skills", "DDI (mean of 4)"],
                     [(r[0], *[f"{(r[i]-mn(i))/(mx(i)-mn(i)):.2f}" for i in (2, 3, 4, 5)], f"{ddi[r[0]]:.3f}") for r in prov])
T["ddi_top"] = max(ddi, key=ddi.get); T["ddi_bot"] = min(ddi, key=ddi.get); T["ddi_top_v"] = f"{max(ddi.values()):.3f}"; T["ddi_bot_v"] = f"{min(ddi.values()):.3f}"
T["use_ratio"] = f"{prov[2][2]/prov[5][2]:.2f}"; T["bb_ratio"] = f"{prov[2][3]/prov[5][3]:.1f}"
fem, mal = 38.0, 52.0; T["gg"] = f"{fem/mal:.3f}"; T["gg_gap"] = f"{mal-fem:.0f}"
# ---- ETA penalty table (sections on which secondary sources agree) ----
eta = [(44, "Pirating, destroying or altering computer source code", 3, 200000), (45, "Unauthorised access to computer material", 3, 200000),
       (46, "Damage to a computer or information system", 3, 200000), (47, "Publication of illegal material in electronic form", 5, 100000), (52, "Computer fraud", 2, 100000)]
T["eta_tab"] = table(["Section", "Offence", "Maximum imprisonment", "Maximum fine (Rs)"], [(s, o, f"{y} years", inr(f)) for s, o, y, f in eta])
T["eta_sum_y"] = f"{sum(e[2] for e in eta)}"; T["eta_sum_f"] = inr(sum(e[3] for e in eta))
T["eta_case_y"] = f"{3+5}"; T["eta_case_f"] = inr(200000 + 100000)
T["eta_3y"] = ", ".join(str(e[0]) for e in eta if e[2] == 3)

# ---- e-government index ----
osi, tii, hci = 0.52, 0.41, 0.63; egdi = (osi + tii + hci) / 3; T["egdi"] = f"{egdi:.3f}"; T["egdi_sum"] = f"{osi+tii+hci:.2f}"
ppl, saved_h, wage, trips = 120000, 3.5, 60, 2
T["eg_trips"] = inr(ppl * trips); T["eg_hours"] = inr(ppl * trips * saved_h); T["eg_value"] = inr(ppl * trips * saved_h * wage)
cost = 4500000; T["eg_net"] = inr(ppl * trips * saved_h * wage - cost)
# ---- fairness ----
cm = {"Urban applicants (A)": dict(TP=80, FP=20, FN=10, TN=90), "Rural applicants (B)": dict(TP=30, FP=10, FN=30, TN=80)}
def met(c):
    n = sum(c.values()); P = c["TP"] + c["FN"]; N = c["FP"] + c["TN"]
    return dict(n=n, sel=(c["TP"] + c["FP"]) / n, tpr=c["TP"] / P, fpr=c["FP"] / N, ppv=c["TP"] / (c["TP"] + c["FP"]), acc=(c["TP"] + c["TN"]) / n, prev=P / n)
mA, mB = [met(c) for c in cm.values()]
T["cm_tab"] = table(["Group", "TP", "FP", "FN", "TN", "n"], [(k, *c.values(), sum(c.values())) for k, c in cm.items()])
T["met_tab"] = table(["Metric", "Group A", "Group B"], [("Selection rate (TP+FP)/n", f"{mA['sel']:.3f}", f"{mB['sel']:.3f}"), ("True-positive rate TP/(TP+FN)", f"{mA['tpr']:.3f}", f"{mB['tpr']:.3f}"),
          ("False-positive rate FP/(FP+TN)", f"{mA['fpr']:.3f}", f"{mB['fpr']:.3f}"), ("Precision TP/(TP+FP)", f"{mA['ppv']:.3f}", f"{mB['ppv']:.3f}"),
          ("Accuracy", f"{mA['acc']:.3f}", f"{mB['acc']:.3f}"), ("Base rate of repayers", f"{mA['prev']:.3f}", f"{mB['prev']:.3f}")])
T["dp_diff"] = f"{mA['sel']-mB['sel']:.3f}"; T["di"] = f"{mB['sel']/mA['sel']:.3f}"
T["tpr_gap"] = f"{mA['tpr']-mB['tpr']:.3f}"; T["fpr_gap"] = f"{mA['fpr']-mB['fpr']:.3f}"; T["ppv_gap"] = f"{mA['ppv']-mB['ppv']:.3f}"
T["di_pass"] = "fails" if mB["sel"] / mA["sel"] < 0.8 else "passes"
fpr_impl = mB["prev"] / (1 - mB["prev"]) * (1 - mA["ppv"]) / mA["ppv"] * mA["tpr"]
T["fpr_impl"] = f"{fpr_impl:.3f}"; T["fpr_A"] = f"{mA['fpr']:.3f}"
assert abs(mA["fpr"] - mA["prev"] / (1 - mA["prev"]) * (1 - mA["ppv"]) / mA["ppv"] * mA["tpr"]) < 1e-12
# ---- PUE and carbon ----
IT, TOTAL = 100.0, 150.0; pue = TOTAL / IT; hours = 8760
T["pue"] = f"{pue:.2f}"; T["dcie"] = f"{IT/TOTAL*100:.1f}"; T["e_total"] = inr(TOTAL * hours); T["e_it"] = inr(IT * hours); T["e_over"] = inr((TOTAL - IT) * hours)
pue2 = 1.3; tot2 = IT * pue2; T["e_total2"] = inr(tot2 * hours); T["e_save"] = inr((TOTAL - tot2) * hours); T["pue2_kw"] = f"{tot2:.0f}"
rate = 12; T["e_cost_save"] = inr((TOTAL - tot2) * hours * rate)
ef_hydro, ef_avg = 0.02, 0.5
T["co2_avg"] = f"{TOTAL*hours*ef_avg/1000:,.1f}"; T["co2_hydro"] = f"{TOTAL*hours*ef_hydro/1000:,.1f}"; T["co2_save_avg"] = f"{(TOTAL-tot2)*hours*ef_avg/1000:,.1f}"
use_kwh = 50 * 8 * 250 / 1000; emb = 300
rows = []
for yrs in (3, 4, 5, 6):
    use_c = use_kwh * ef_avg; rows.append((yrs, f"{emb/yrs:.1f}", f"{use_c:.1f}", f"{emb/yrs+use_c:.1f}"))
T["laptop_tab"] = table(["Service life (years)", "Embodied per year (kg CO₂e)", "Use per year at 0.5 kg/kWh", "Annual total"], rows)
T["use_kwh"] = f"{use_kwh:.0f}"; T["use_co2"] = f"{use_kwh*ef_avg:.0f}"; T["lap3"] = f"{emb/3+use_kwh*ef_avg:.1f}"; T["lap5"] = f"{emb/5+use_kwh*ef_avg:.1f}"
T["lap_cut"] = f"{(1-(emb/5+use_kwh*ef_avg)/(emb/3+use_kwh*ef_avg))*100:.1f}"
col = 1000; flow = [("Collected by formal recyclers", 120), ("Reused / refurbished", 80), ("Sent informally to scrap dealers", 450), ("Stored at home or office", 300), ("Landfill or burnt", 50)]
assert sum(f[1] for f in flow) == col
T["ew_tab"] = table(["Fate of 1,000 kg of discarded devices (illustrative)", "kg", "Share"], [(n, k, f"{k/col*100:.0f}%") for n, k in flow])
T["ew_formal"] = f"{(120+80)/col*100:.0f}"


def _hand():
    assert 2300 * 2 ** 15 == 75366400 and 2 ** 5 == 32
    assert abs(math.log(0.3 / 0.02) / 0.32 - 8.46) < 0.01 and 100 * 0.6 / 4 == 15
    assert abs(41 / 28 - 1.46) < 0.005 and 45 / 60 == 0.75
    assert 3 + 2 == 5 and 200000 + 100000 == 300000
    assert abs((0.6 + 0.3 + 0.75) / 3 - 0.55) < 1e-9 and 50000 * 4 * 50 == 10000000
    c = dict(TP=40, FP=10, FN=20, TN=30); mm = met(c)
    assert (mm["sel"], round(mm["tpr"], 3), mm["fpr"], mm["ppv"]) == (0.5, 0.667, 0.25, 0.8)
    assert 128 / 80 == 1.6 and 80 / 128 == 0.625 and 128 * 8760 == 1121280 and 128 * 8760 * 10 == 11212800
    assert 240 / 4 + 100 == 160 and 240 / 6 + 100 == 140
    assert abs(mA["tpr"] - 0.889) < 0.001 and abs(mA["prev"] - 0.45) < 1e-9 and abs(mB["prev"] - 0.40) < 1e-9
_hand()

if __name__ == "__main__":
    run(T, sys.argv[1:])
