#!/usr/bin/env python3
"""BCA 252 Software Engineering: recompute every number (COCOMO, function points, cyclomatic complexity with executed
test cases, CPM/PERT, earned value, reliability, risk exposure, design/maintenance metrics).
    python3 bca/tools/check_se.py --print | --fill unit-*.md | --verify unit-*.md"""
import math, sys, re, ast, textwrap
T = {}
def table(head, rows):
    return "\n".join(["| " + " | ".join(head) + " |", "|" + "---|" * len(head)] + ["| " + " | ".join(str(c) for c in r) + " |" for r in rows])

# ---------- COCOMO (basic) ----------
modes = {"Organic": (2.4, 1.05, 2.5, 0.38), "Semi-detached": (3.0, 1.12, 2.5, 0.35), "Embedded": (3.6, 1.20, 2.5, 0.32)}
K = 32
rows = []; res = {}
for m, (a, b, c, d) in modes.items():
    E = a * K ** b; D = c * E ** d; res[m] = (E, D, E / D); rows.append((m, f"{a} × 32^{b} = {E:.1f}", f"{c} × {E:.1f}^{d} = {D:.1f}", f"{E/D:.1f}"))
T["coc_tab"] = table(["Mode", "Effort E = a(KLOC)^b (person-months)", "Duration D = c·E^d (months)", "Average staff E/D"], rows)
T["coc_org_E"] = f"{res['Organic'][0]:.1f}"; T["coc_org_D"] = f"{res['Organic'][1]:.1f}"; T["coc_org_N"] = f"{res['Organic'][2]:.1f}"
T["coc_emb_E"] = f"{res['Embedded'][0]:.1f}"
T["coc_prod"] = f"{K * 1000 / res['Organic'][0]:.0f}"
# intermediate COCOMO
drv = {"RELY (high)": 1.15, "CPLX (high)": 1.15, "ACAP (high)": 0.86, "TOOL (high)": 0.91}
eaf = 1
for v in drv.values(): eaf *= v
Enom = 3.2 * K ** 1.05; Eadj = Enom * eaf
T["icoc_tab"] = table(["Cost driver", "Multiplier"], [(k, f"{v:.2f}") for k, v in drv.items()] + [("**EAF = product**", f"**{eaf:.4f}**")])
T["icoc_nom"] = f"{Enom:.1f}"; T["icoc_adj"] = f"{Eadj:.1f}"; T["icoc_eaf"] = f"{eaf:.4f}"
T["icoc_D"] = f"{2.5 * Eadj ** 0.38:.1f}"
# ---------- Function points ----------
W = {"EI": (3, 4, 6), "EO": (4, 5, 7), "EQ": (3, 4, 6), "ILF": (7, 10, 15), "EIF": (5, 7, 10)}
cnt = {"EI": (5, 3, 2), "EO": (4, 2, 1), "EQ": (3, 2, 0), "ILF": (2, 1, 0), "EIF": (1, 1, 0)}
rows = []; ufp = 0
for k in W:
    tot = sum(c * w for c, w in zip(cnt[k], W[k])); ufp += tot
    rows.append((k, *cnt[k], f"{cnt[k][0]}×{W[k][0]} + {cnt[k][1]}×{W[k][1]} + {cnt[k][2]}×{W[k][2]}", tot))
T["fp_tab"] = table(["Type", "Low", "Average", "High", "Calculation (weights 3/4/6 etc.)", "Subtotal"], rows + [("**UFP**", "", "", "", "", f"**{ufp}**")])
gsc = [3, 2, 4, 3, 3, 4, 3, 2, 3, 3, 2, 3, 2, 3]; assert len(gsc) == 14
vaf = 0.65 + 0.01 * sum(gsc); fp = ufp * vaf
T["fp_ufp"] = str(ufp); T["fp_gsc"] = ", ".join(map(str, gsc)); T["fp_sum"] = str(sum(gsc)); T["fp_vaf"] = f"{vaf:.2f}"; T["fp_fp"] = f"{fp:.2f}"
T["fp_loc"] = f"{fp * 53:,.0f}"; T["fp_kloc"] = f"{fp * 53 / 1000:.2f}"; T["fp_eff"] = f"{fp / 10:.1f}"
T["fp_w_in"] = str(5 * 3 + 3 * 4 + 2 * 6)
# ---------- Cyclomatic complexity ----------
SRC = '''def classify(a, b, c):
    if a <= 0 or b <= 0 or c <= 0:
        return "invalid"
    if a + b <= c or a + c <= b or b + c <= a:
        return "not a triangle"
    if a == b and b == c:
        return "equilateral"
    if a == b or b == c or a == c:
        return "isosceles"
    return "scalene"
'''
tree = ast.parse(SRC); dec = 0
for n in ast.walk(tree):
    if isinstance(n, (ast.If, ast.For, ast.While)): dec += 1
    elif isinstance(n, ast.BoolOp): dec += len(n.values) - 1
ns = {}; exec(SRC, ns)
T["cc_src"] = SRC.rstrip(); T["cc_dec"] = str(dec); T["cc_v"] = str(dec + 1)
cases = [((0, 4, 5), "a ≤ 0 (first condition)"), ((3, 4, 9), "a + b ≤ c"), ((5, 5, 5), "all equal"), ((5, 5, 8), "a = b only"), ((3, 4, 5), "all different")]
T["cc_tests"] = table(["Test (a, b, c)", "Path exercised", "Result"], [(f"({a}, {b}, {c})", why, ns["classify"](a, b, c)) for (a, b, c), why in cases])
# graph formula: nodes/edges for a simple if-else-while example
GSRC = '''def grade(m):
    if m < 0 or m > 100:
        return "invalid"
    elif m >= 80:
        return "A"
    elif m >= 60:
        return "B"
    elif m >= 40:
        return "C"
    return "F"
'''
gd = 0
for n_ in ast.walk(ast.parse(GSRC)):
    if isinstance(n_, (ast.If, ast.For, ast.While)): gd += 1
    elif isinstance(n_, ast.BoolOp): gd += len(n_.values) - 1
gns = {}; exec(GSRC, gns)
T["gr_src"] = GSRC.rstrip(); T["gr_dec"] = str(gd); T["gr_v"] = str(gd + 1)
gcases = [(-5, "m < 0 (first operand of or)"), (101, "m > 100 (second operand)"), (85, "m ≥ 80"), (65, "60 ≤ m < 80"), (45, "40 ≤ m < 60"), (20, "m < 40 (falls through)")]
T["gr_tests"] = table(["Test m", "Independent path", "grade(m) returned"], [(m, w, gns["grade"](m)) for m, w in gcases])
assert gd + 1 == len(gcases)
# BVA / ECP
def valid_age(x): return 18 <= x <= 60
bva = [17, 18, 19, 59, 60, 61]
T["bva_tab"] = table(["Input age", "Class", "Expected", "valid_age() returned"], [(x, "valid" if 18 <= x <= 60 else "invalid", "accept" if 18 <= x <= 60 else "reject", "accept" if valid_age(x) else "reject") for x in bva])
# ---------- CPM ----------
acts = {"A": (3, []), "B": (4, ["A"]), "C": (2, ["A"]), "D": (5, ["B"]), "E": (3, ["C"]), "F": (4, ["D", "E"]), "G": (2, ["F"])}
ES, EF = {}, {}
for a in acts:  # topological as listed
    d, pre = acts[a]; ES[a] = max([EF[p] for p in pre], default=0); EF[a] = ES[a] + d
proj = max(EF.values()); LF, LS = {}, {}
for a in reversed(list(acts)):
    succ = [s for s in acts if a in acts[s][1]]
    LF[a] = min([LS[s] for s in succ], default=proj); LS[a] = LF[a] - acts[a][0]
rows = [(a, acts[a][0], ",".join(acts[a][1]) or "—", ES[a], EF[a], LS[a], LF[a], LS[a] - ES[a], "**yes**" if LS[a] == ES[a] else "no") for a in acts]
T["cpm_tab"] = table(["Activity", "Duration", "Predecessors", "ES", "EF", "LS", "LF", "Slack", "Critical?"], rows)
crit = [a for a in acts if LS[a] == ES[a]]; T["cpm_path"] = " → ".join(crit); T["cpm_len"] = str(proj)
T["cpm_noncrit"] = ", ".join(f"{a} (slack {LS[a]-ES[a]})" for a in acts if LS[a] != ES[a])
# PERT
est = {"A": (2, 3, 6), "B": (3, 4, 7), "D": (4, 5, 12), "F": (3, 4, 5), "G": (1, 2, 3)}
rows = []; mu = 0; var = 0
for a, (o, m, p) in est.items():
    te = (o + 4 * m + p) / 6; s = (p - o) / 6; mu += te; var += s * s; rows.append((a, o, m, p, f"{te:.2f}", f"{s:.3f}", f"{s*s:.3f}"))
T["pert_tab"] = table(["Activity (on critical path A-B-D-F-G)", "o", "m", "p", "tₑ = (o + 4m + p)/6", "σ = (p − o)/6", "σ²"], rows)
T["pert_mu"] = f"{mu:.2f}"; T["pert_var"] = f"{var:.3f}"; T["pert_sd"] = f"{math.sqrt(var):.3f}"
Phi = lambda z: 0.5 * (1 + math.erf(z / math.sqrt(2)))
D = 20; z = (D - mu) / math.sqrt(var); T["pert_z"] = f"{z:.2f}"; T["pert_p"] = f"{Phi(z) * 100:.1f}"
D2 = 18; z2 = (D2 - mu) / math.sqrt(var); T["pert_z2"] = f"{z2:.2f}"; T["pert_p2"] = f"{Phi(z2) * 100:.1f}"
T["pert_p_check"] = f"{Phi(1.0)*100:.1f}"
# ---------- Earned value ----------
BAC, PV, EV, AC = 500000, 250000, 200000, 240000
CPI = EV / AC; SPI = EV / PV; CV = EV - AC; SV = EV - PV; EAC = BAC / CPI; ETC = EAC - AC; VAC = BAC - EAC; TCPI = (BAC - EV) / (BAC - AC)
T["evm_tab"] = table(["Measure", "Formula", "Value"], [("Cost variance CV", "EV − AC", f"{CV:,}"), ("Schedule variance SV", "EV − PV", f"{SV:,}"), ("CPI", "EV / AC", f"{CPI:.3f}"), ("SPI", "EV / PV", f"{SPI:.3f}"),
    ("EAC", "BAC / CPI", f"{EAC:,.0f}"), ("ETC", "EAC − AC", f"{ETC:,.0f}"), ("VAC", "BAC − EAC", f"{VAC:,.0f}"), ("TCPI (to BAC)", "(BAC − EV)/(BAC − AC)", f"{TCPI:.3f}")])
T["evm_cpi"] = f"{CPI:.3f}"; T["evm_spi"] = f"{SPI:.3f}"; T["evm_eac"] = f"{EAC:,.0f}"; T["evm_vac"] = f"{VAC:,.0f}"; T["evm_pctc"] = f"{EV/BAC*100:.0f}"
# ---------- reliability / quality ----------
mttf, mttr = 1000, 2
T["rel_avail"] = f"{mttf/(mttf+mttr)*100:.3f}"; T["rel_R100"] = f"{math.exp(-100/mttf):.4f}"; T["rel_lambda"] = f"{1/mttf:.3f}"
T["rel_down"] = f"{(1 - mttf/(mttf+mttr)) * 8760:.1f}"
T["dre"] = f"{80/(80+20)*100:.0f}"; T["dd"] = f"{45/32:.2f}"
# ---------- risk exposure ----------
risks = [("Key developer leaves", 0.3, 40), ("Requirements change late", 0.6, 25), ("Third-party API changes", 0.2, 30), ("Hardware delivered late", 0.5, 10), ("Estimate too low by 25 %", 0.4, 50)]
rows = [(r, p, l, f"{p*l:.1f}") for r, p, l in sorted(risks, key=lambda x: -x[1] * x[2])]
T["risk_tab"] = table(["Risk", "Probability", "Loss (person-days)", "Exposure = P × L"], rows)
T["risk_total"] = f"{sum(p*l for _, p, l in risks):.1f}"; T["risk_top"] = rows[0][0]
# ---------- design / maintenance / code metrics ----------
hk = 6 * (3 * 2) ** 2
T["hk"] = str(hk); T["hk2"] = str(6 * (1 * 1) ** 2)
n1, n2, N1, N2 = 10, 7, 24, 15; n = n1 + n2; N = N1 + N2; V = N * math.log2(n)
T["hal_n"] = str(n); T["hal_N"] = str(N); T["hal_V"] = f"{V:.1f}"; T["hal_D"] = f"{(n1/2)*(N2/n2):.2f}"; T["hal_E"] = f"{(n1/2)*(N2/n2)*V:.0f}"
T["hal_B"] = f"{V/3000:.3f}"
act = 0.15; sde = res["Organic"][0]; T["mnt_ame"] = f"{act*sde:.1f}"; T["mnt_act"] = "15"; T["mnt_sde"] = f"{sde:.1f}"
T["mnt_cost_ratio"] = f"{(1-0.0)*100:.0f}"
# cost of change multiplier example
T["coc_loc"] = f"{K}"
T["mi"] = ""  # placeholder (unused)
del T["mi"]
# fan-in/out
def apply(t): return re.sub(r"@@([A-Za-z0-9_]+)@@", lambda m: T[m.group(1)], t)
if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "--print"
    if mode == "--print":
        for k, v in T.items(): print(f"@@{k}@@ " + (v if "\n" not in v else "\n" + v))
    elif mode == "--fill":
        for p in sys.argv[2:]:
            s = apply(open(p, encoding="utf-8").read()); assert not re.findall(r"@@(\w+)@@", s); open(p, "w", encoding="utf-8").write(s)
    elif mode == "--verify":
        text = "\n".join(open(p, encoding="utf-8").read() for p in sys.argv[2:]); un = [k for k, v in T.items() if v not in text]
        print(f"{len(T)-len(un)} of {len(T)} computed tokens appear verbatim; unused: {un}")
