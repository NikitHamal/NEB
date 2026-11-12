#!/usr/bin/env python3
"""BCA 304 MIS and e-Business: recompute every number (HHI, bullwhip, EOQ, safety stock, EMV/EVPI/regret, decision-table
coverage, NPV/IRR/payback/ROI/TCO/break-even, ALE, password entropy, LTV/CAC, multilateral netting, weighted scoring).
    python3 bca/tools/check_mis.py --print | --fill unit-*.md | --verify unit-*.md"""
import math, sys, itertools
import numpy as np
from tokcommon import table, inr, run
T = {}

# ---- Porter-style weighted force scoring and HHI ----
forces = [("Threat of new entrants", 0.20, 4), ("Bargaining power of suppliers", 0.15, 2), ("Bargaining power of buyers", 0.25, 5),
          ("Threat of substitutes", 0.25, 4), ("Rivalry among competitors", 0.15, 4)]
assert abs(sum(w for _, w, _ in forces) - 1) < 1e-9
fs = sum(w * r for _, w, r in forces)
T["force_tab"] = table(["Force", "Weight", "Intensity (1 low – 5 high)", "Weight × intensity"], [(n, w, r, f"{w*r:.2f}") for n, w, r in forces] + [("**Total**", "1.00", "", f"**{fs:.2f}**")])
T["force_total"] = f"{fs:.2f}"
shares = [("Wallet A", 45), ("Wallet B", 30), ("Wallet C", 15), ("Wallet D", 10)]
hhi = sum(s * s for _, s in shares)
T["hhi_tab"] = table(["Firm", "Share s (%)", "s²"], [(n, s, s * s) for n, s in shares] + [("**HHI**", "100", f"**{hhi}**")])
T["hhi"] = f"{hhi}"
hhi_after = hhi - 15**2 - 10**2 + 25**2
T["hhi_after"] = f"{hhi_after}"; T["hhi_delta"] = f"{hhi_after - hhi}"
assert hhi_after - hhi == 2 * 15 * 10

# ---- Bullwhip ----
def bw(L, p): return 1 + 2 * L / p + 2 * L * L / p**2
p = 4; stages = [("Retailer", 1), ("Wholesaler", 2), ("Distributor", 2), ("Factory", 3)]
rows = []; cum = 1.0
for n, L in stages:
    f = bw(L, p); cum *= f; rows.append((n, L, f"{f:.3f}", f"{cum:.2f}", f"{math.sqrt(cum):.2f}"))
T["bw_tab"] = table(["Stage", "Lead time L (weeks)", "Stage factor 1 + 2L/p + 2L²/p²", "Cumulative Var(order)/Var(demand)", "Std-dev ratio"], rows)
T["bw_cum"] = f"{cum:.2f}"; T["bw_sd"] = f"{math.sqrt(cum):.2f}"; T["bw_ret"] = f"{bw(1, 4):.3f}"
T["bw_L1p4"] = f"{bw(1, 4):.3f}"; T["bw_L1p8"] = f"{bw(1, 8):.3f}"
# five-week trace: order-up-to S_t = (L+1)*MA_p(D), q_t = D_t + S_t - S_{t-1}, p=2, L=1
D = [100, 100, 120, 100, 100, 100]; Lh, ph = 1, 2
S = []; Q = []
for t in range(len(D)):
    hist = D[max(0, t - ph + 1):t + 1]; ma = sum(hist) / len(hist); S.append((Lh + 1) * ma)
    Q.append(D[t] if t == 0 else D[t] + S[t] - S[t - 1])
T["bw_trace"] = table(["Week t", "Demand D", "Moving average of last 2", "Order-up-to S = 2 × MA", "Order q = D + S − S(prev)"],
                     [(t + 1, D[t], f"{S[t]/2:.0f}", f"{S[t]:.0f}", f"{Q[t]:.0f}") for t in range(len(D))])
T["bw_qmax"] = f"{max(Q):.0f}"; T["bw_qmin"] = f"{min(Q):.0f}"
assert max(Q) == 140 and min(Q) == 80, Q

# ---- EOQ / safety stock ----
Dm, Sc, H = 12000, 500, 20
eoq = math.sqrt(2 * Dm * Sc / H)
tc = lambda q: Dm / q * Sc + q / 2 * H
best = min(range(100, 3000), key=tc); assert abs(best - eoq) <= 1
T["eoq"] = f"{eoq:.1f}"; T["eoq_n"] = f"{Dm/eoq:.2f}"; T["eoq_cycle"] = f"{eoq/Dm*365:.1f}"
T["eoq_tc"] = inr(tc(eoq)); T["eoq_ord"] = inr(Dm / eoq * Sc); T["eoq_hold"] = inr(eoq / 2 * H)
T["eoq_tc1000"] = inr(tc(1000)); T["eoq_tc500"] = inr(tc(500))
z, sd, Ld, dd = 1.645, 40, 9, 150
ss = z * sd * math.sqrt(Ld); rop = dd * Ld + ss
T["ss"] = f"{ss:.1f}"; T["rop"] = f"{rop:.1f}"; T["rop_base"] = f"{dd*Ld}"
T["ss_L16"] = f"{z*sd*math.sqrt(16):.1f}"

# ---- EMV, EVPI, criteria ----
states = ["High demand", "Medium", "Low"]; prob = [0.3, 0.5, 0.2]
acts = {"Large on-premise server": [900, 400, -300], "Cloud, auto-scaling": [700, 450, 100], "Small server": [300, 250, 150]}
P = np.array(list(acts.values()), dtype=float); pr = np.array(prob)
emv = P @ pr
T["pay_tab"] = table(["Alternative (Rs '000 profit)"] + states + ["EMV"], [(a, *v, f"{e:.0f}") for (a, v), e in zip(acts.items(), emv)])
bi = int(np.argmax(emv)); T["emv_best"] = list(acts)[bi]; T["emv_best_val"] = f"{emv[bi]:.0f}"
epc = float(np.max(P, axis=0) @ pr); evpi = epc - emv[bi]
T["epc"] = f"{epc:.0f}"; T["evpi"] = f"{evpi:.0f}"
mm = P.min(axis=1); T["maximin_best"] = list(acts)[int(np.argmax(mm))]; T["maximin_val"] = f"{mm.max():.0f}"
reg = P.max(axis=0) - P; mr = reg.max(axis=1)
T["reg_tab"] = table(["Alternative (regret, Rs '000)"] + states + ["Maximum regret"], [(a, *[f"{x:.0f}" for x in r], f"{m:.0f}") for a, r, m in zip(acts, reg, mr)])
T["minimax_best"] = list(acts)[int(np.argmin(mr))]; T["minimax_val"] = f"{mr.min():.0f}"
lap = P.mean(axis=1); T["laplace_best"] = list(acts)[int(np.argmax(lap))]; T["laplace_val"] = f"{lap.max():.1f}"
alpha = 0.6; hur = alpha * P.max(axis=1) + (1 - alpha) * P.min(axis=1)
T["hurwicz_tab"] = ", ".join(f"{a} = {h:.0f}" for a, h in zip(acts, hur)); T["hurwicz_best"] = list(acts)[int(np.argmax(hur))]
assert abs(evpi - (epc - emv.max())) < 1e-9
# decision tree: build now vs pilot
pS = 0.6; big_win, big_loss = 800, -300; pilot_cost = 50
emv_now = pS * big_win + (1 - pS) * big_loss
pilot_ok = 0.85; pilot_bad = 0.15
# pilot shows "good" with P(g)=0.5; posterior chance of success given good 0.9, given bad 0.3 (consistent with 0.6)
Pg = 0.5; Pgs = 0.9; Pbs = 0.3; assert abs(Pg * Pgs + (1 - Pg) * Pbs - pS) < 1e-9
ev_good = Pgs * big_win + (1 - Pgs) * big_loss; ev_bad = Pbs * big_win + (1 - Pbs) * big_loss
roll_good = max(ev_good, 0); roll_bad = max(ev_bad, 0)
emv_pilot = Pg * roll_good + (1 - Pg) * roll_bad - pilot_cost
T["tree_now"] = f"{emv_now:.0f}"; T["tree_evg"] = f"{ev_good:.0f}"; T["tree_evb"] = f"{ev_bad:.0f}"; T["tree_pilot"] = f"{emv_pilot:.0f}"
T["tree_roll_bad"] = f"{roll_bad:.0f}"; T["tree_pilot_gross"] = f"{Pg*roll_good+(1-Pg)*roll_bad:.0f}"
T["tree_choice"] = "pilot first" if emv_pilot > emv_now else "build now"
T["tree_value_pilot"] = f"{emv_pilot - emv_now:.0f}"

# ---- decision table coverage ----
conds = ["Existing customer", "Salary account", "Amount ≤ 5× salary"]
rules = {"R1": (True, True, True, "Approve"), "R2": (True, True, False, "Refer to manager"), "R3": (True, False, None, "Refer to manager"), "R4": (False, None, True, "Refer to manager"), "R5": (False, None, False, "Reject")}
cover = {c: [] for c in itertools.product([True, False], repeat=3)}
for r, (a, b, c, _) in rules.items():
    for combo in cover:
        if all(x is None or x == y for x, y in zip((a, b, c), combo)): cover[combo].append(r)
assert all(len(v) == 1 for v in cover.values()), cover
sym = lambda x: "—" if x is None else ("Y" if x else "N")
T["dt_tab"] = table(["Condition / action"] + list(rules), [(c, *[sym(v[i]) for v in rules.values()]) for i, c in enumerate(conds)] + [("**Action**", *[v[3] for v in rules.values()])])
T["dt_full"] = table(["Customer", "Salary a/c", "≤ 5× salary", "Matching rule", "Action"], [("Y" if k[0] else "N", "Y" if k[1] else "N", "Y" if k[2] else "N", v[0], rules[v[0]][3]) for k, v in cover.items()])
T["dt_n"] = f"{len(cover)}"

# ---- investment appraisal ----
cf = [-1200000, 350000, 400000, 450000, 400000, 300000]; r = 0.12
npv = lambda rate, c=cf: sum(x / (1 + rate) ** t for t, x in enumerate(c))
lo, hi = 0.0, 1.0
for _ in range(200):
    mid = (lo + hi) / 2
    if npv(mid) > 0: lo = mid
    else: hi = mid
irr = lo; assert abs(npv(irr)) < 1e-4
rowsn = []; cumu = 0; cumd = 0; pb = dpb = None
for t, x in enumerate(cf):
    d = x / (1 + r) ** t; prev, prevd = cumu, cumd; cumu += x; cumd += d
    if t > 0 and pb is None and cumu >= 0: pb = (t - 1) + (-prev) / x
    if t > 0 and dpb is None and cumd >= 0: dpb = (t - 1) + (-prevd) / d
    rowsn.append((t, inr(x), f"{1/(1+r)**t:.4f}", inr(d), inr(cumu), inr(cumd)))
T["npv_tab"] = table(["Year", "Cash flow (Rs)", "Discount factor 1/1.12ᵗ", "Present value (Rs)", "Cumulative (Rs)", "Cumulative PV (Rs)"], rowsn)
T["npv"] = inr(npv(r)); T["irr"] = f"{irr*100:.2f}"; T["pb"] = f"{pb:.2f}"; T["dpb"] = f"{dpb:.2f}"
T["pi"] = f"{(npv(r) + 1200000) / 1200000:.3f}"
tot_in = sum(cf[1:]); T["tot_in"] = inr(tot_in); T["tot_net"] = inr(tot_in - 1200000)
T["npv_8"] = inr(npv(0.08)); T["npv_20"] = inr(npv(0.20)); T["npv_irr_check"] = f"{abs(npv(irr)):.4f}"
dep = 1200000 / 5; avg_profit = (tot_in - 1200000) / 5
T["roi_avg"] = inr(avg_profit); T["roi"] = f"{avg_profit/1200000*100:.1f}"; T["roi_cash"] = f"{(tot_in-1200000)/1200000*100:.1f}"; T["arr_avg_inv"] = f"{avg_profit/(1200000/2)*100:.1f}"
# TCO on-prem vs cloud, 5 years, undiscounted and discounted
onprem = {"Hardware and installation": [900000, 0, 0, 0, 0, 0], "Software licences": [250000, 0, 0, 0, 0, 0],
          "Staff (1 admin)": [0, 480000, 480000, 480000, 480000, 480000], "Power, cooling, space": [0, 90000, 90000, 90000, 90000, 90000],
          "Support contract (AMC)": [0, 120000, 120000, 120000, 120000, 120000], "Hardware refresh": [0, 0, 0, 0, 0, 0]}
cloud = {"Migration and setup": [200000, 0, 0, 0, 0, 0], "Subscription (per user)": [0, 540000, 560000, 600000, 640000, 680000],
         "Staff (0.5 admin)": [0, 240000, 240000, 240000, 240000, 240000], "Bandwidth upgrade": [0, 60000, 60000, 60000, 60000, 60000], "Training": [0, 50000, 20000, 20000, 20000, 20000]}
def tcosum(d): return [sum(v[t] for v in d.values()) for t in range(6)]
to, tcl = tcosum(onprem), tcosum(cloud)
T["tco_tab"] = table(["Year", "On-premise (Rs)", "Cloud (Rs)"], [(t, inr(to[t]), inr(tcl[t])) for t in range(6)] + [("**5-year TCO**", f"**{inr(sum(to))}**", f"**{inr(sum(tcl))}**")])
pvc = lambda c: sum(x / (1 + r) ** t for t, x in enumerate(c))
T["tco_on"] = inr(sum(to)); T["tco_cl"] = inr(sum(tcl)); T["tco_on_pv"] = inr(pvc(to)); T["tco_cl_pv"] = inr(pvc(tcl))
T["tco_diff"] = inr(sum(to) - sum(tcl)); T["tco_cheaper"] = "cloud" if pvc(tcl) < pvc(to) else "on-premise"
T["tco_on_peryear"] = inr(sum(to) / 5)
# break-even
FC, vc, price = 180000, 12, 30
be = FC / (price - vc); T["be_units"] = inr(be); T["be_cm"] = f"{price-vc}"; T["be_rev"] = inr(be * price)
T["be_20k"] = inr(20000 * (price - vc) - FC); T["be_cmr"] = f"{(price-vc)/price*100:.0f}"

# ---- risk ----
AV, EF, ARO = 2000000, 0.4, 0.25
sle = AV * EF; ale = sle * ARO; ale2 = sle * 0.05; cost = 70000
T["sle"] = inr(sle); T["ale"] = inr(ale); T["ale_after"] = inr(ale2); T["ale_saved"] = inr(ale - ale2); T["ale_net"] = inr(ale - ale2 - cost)
T["ale_roi"] = f"{(ale-ale2-cost)/cost*100:.0f}"
def ent(n, L): return L * math.log2(n)
pwd = [("8 random lowercase letters", 26, 8), ("8 random chars from 95 printable ASCII", 95, 8), ("12 random lowercase letters", 26, 12),
       ("4 random words from a 2,048-word list", 2048, 4), ("6 random words from a 2,048-word list", 2048, 6)]
rate = 1e10
def crack(bits): s = 2 ** (bits - 1) / rate; return s
def human(s):
    for u, k in (("years", 31557600), ("days", 86400), ("hours", 3600), ("minutes", 60)):
        if s >= k: return f"{s/k:,.1f} {u}"
    return f"{s:.2f} seconds"
T["pw_tab"] = table(["Password scheme", "Space size", "Entropy (bits)", "Average time at 10¹⁰ guesses/s"],
                    [(n, f"{a**L:.2e}", f"{ent(a, L):.1f}", human(crack(ent(a, L)))) for n, a, L in pwd])
T["pw_8"] = f"{ent(95,8):.1f}"; T["pw_12"] = f"{ent(26,12):.1f}"; T["pw_w6"] = f"{ent(2048,6):.0f}"

# ---- e-commerce funnel, LTV/CAC ----
vis = 100000; stepsr = [("Add to cart", 0.05), ("Start checkout", 0.40), ("Complete payment", 0.70)]
n = vis; frows = [("Visitors", vis, "")]
for nm, rr in stepsr:
    n = n * rr; frows.append((nm, f"{n:,.0f}", f"{rr*100:.0f}%"))
orders = n; conv = orders / vis
T["funnel_tab"] = table(["Funnel stage", "Users", "Step rate"], frows); T["conv"] = f"{conv*100:.2f}"; T["orders"] = f"{orders:,.0f}"
aov, gm = 2400, 0.22; ad = 150000
cac = ad / orders; gp = aov * gm
T["aov_gp"] = f"{gp:.0f}"; T["cac"] = f"{cac:.2f}"; T["first_loss"] = f"{gp-cac:.2f}"
churn = 0.25; orders_per_year = 3; ltv = gp * orders_per_year / churn
T["ltv"] = inr(ltv); T["ltv_cac"] = f"{ltv/cac:.1f}"; T["life"] = f"{1/churn:.0f}"
# Metcalfe
T["met_1k"] = inr(1000 * 999 / 2); T["met_2k"] = inr(2000 * 1999 / 2)

# ---- multilateral netting ----
banks = ["A", "B", "C", "D"]
M = np.array([[0, 120, 80, 60], [90, 0, 50, 100], [110, 70, 0, 40], [30, 130, 90, 0]])
gross = int(M.sum()); sent = M.sum(axis=1); recv = M.sum(axis=0); net = recv - sent
assert net.sum() == 0
T["net_mat"] = table(["From \\ To"] + banks + ["Total sent"], [(b, *M[i], sent[i]) for i, b in enumerate(banks)] + [("**Total received**", *recv, gross)])
T["net_tab"] = table(["Bank", "Sent", "Received", "Net position", "Settles"], [(b, sent[i], recv[i], f"{net[i]:+d}", "receives" if net[i] > 0 else ("pays" if net[i] < 0 else "—")) for i, b in enumerate(banks)])
T["net_gross"] = f"{gross}"; T["net_settle"] = f"{int(net[net > 0].sum())}"; T["net_saving"] = f"{(1-net[net>0].sum()/gross)*100:.1f}"
# bilateral netting for comparison
bil = sum(abs(M[i, j] - M[j, i]) for i in range(4) for j in range(i + 1, 4)); T["net_bil"] = f"{bil}"

# ---- ERP vendor weighted scoring ----
crit = [("Functional fit", 0.30), ("Total cost (5 yr)", 0.25), ("Local support in Nepal", 0.20), ("Integration / APIs", 0.15), ("Vendor viability", 0.10)]
vend = {"Vendor X": [8, 5, 9, 6, 7], "Vendor Y": [9, 4, 6, 9, 9], "Vendor Z": [6, 9, 7, 5, 6]}
sc = {v: sum(w * s for (_, w), s in zip(crit, ss_)) for v, ss_ in vend.items()}
T["ws_tab"] = table(["Criterion", "Weight"] + list(vend), [(c, w, *[vend[v][i] for v in vend]) for i, (c, w) in enumerate(crit)] + [("**Weighted score**", "1.00", *[f"**{sc[v]:.2f}**" for v in vend])])
T["ws_best"] = max(sc, key=sc.get); T["ws_best_val"] = f"{max(sc.values()):.2f}"
T["ws_x"] = f"{sc['Vendor X']:.2f}"; T["ws_y"] = f"{sc['Vendor Y']:.2f}"; T["ws_z"] = f"{sc['Vendor Z']:.2f}"


def _hand_checks():
    # practice answers computed by hand in the book
    assert abs(math.sqrt(2 * 4800 * 300 / 12) - 489.9) < 0.05 and abs(2.326 * 25 * 2 - 116.3) < 0.05
    w2 = [0.20, 0.35, 0.20, 0.15, 0.10]
    alt = {v: sum(a * b for a, b in zip(w2, s)) for v, s in vend.items()}
    assert {k: round(x, 2) for k, x in alt.items()} == {"Vendor X": 6.75, "Vendor Y": 6.65, "Vendor Z": 7.10}, alt
    assert abs(sum(0.3 * a + 0.5 * b + 0.2 * c for a, b, c in [acts["Small server"]]) - 245) < 1e-9
    assert (1600 + 900 + 400 + 100) == 3000 and 500 * 499 // 2 == 124750 and 1000 * 999 // 2 == 499500
    assert round(80000 * .04 * .5 * .8) == 1280 and abs(10 * math.log2(62) - 59.5) < 0.05
    af = sum(1 / 1.1 ** t for t in (1, 2, 3)); assert abs(2e5 * af - 5e5 + 2630) < 5, (2e5 * af - 5e5)
    assert 240000 / 30 == 8000 and 10000 * 30 - 240000 == 60000
    assert abs(fs - 0.5 - 3.45) < 1e-9
_hand_checks()

if __name__ == "__main__":
    run(T, sys.argv[1:])
