#!/usr/bin/env python3
"""Verifier for BCA 156 Principles of Management: recomputes every number in the book.

Break-even, decision criteria (EMV, maximax, maximin, Laplace, Hurwicz, minimax regret), critical path,
Graicunas' relationships, span-of-control levels, expectancy motivation, variance and control limits,
DPMO / Six Sigma, Likert-style weighted scores.   python3 bca/tools/check_management.py [-v]
"""
import sys, itertools
V = "-v" in sys.argv
FAILS = []


def check(name, got, want):
    ok = got == want
    print(("ok   " if ok else "FAIL ") + name + (f"  -> {got}" if V or not ok else "") + ("" if ok else f"  want {want}"))
    if not ok: FAILS.append(name)


# ---- break-even
FC, P, VC = 60000, 50, 30
bep = FC / (P - VC)
check("BEP units = 3000, sales Rs 150,000", (bep, bep * P), (3000.0, 150000.0))
check("units for profit Rs 20,000 = 4000", (FC + 20000) / (P - VC), 4000.0)
check("contribution margin ratio 40%", (P - VC) / P, 0.4)
check("margin of safety at 4000 units = 25%", (4000 - 3000) / 4000, 0.25)
check("profit at 3500 units = 10,000", 3500 * (P - VC) - FC, 10000)

# ---- decision table
T = {"A": [80, 50, -20], "B": [60, 40, 10], "C": [45, 40, 30]}
pr = [0.3, 0.5, 0.2]
emv = {k: round(sum(p * x for p, x in zip(pr, v)), 2) for k, v in T.items()}
check("EMV A 45, B 40, C 39.5", emv, {"A": 45.0, "B": 40.0, "C": 39.5})
check("maximax -> A (80)", max(T, key=lambda k: max(T[k])), "A")
check("maximin -> C (30)", max(T, key=lambda k: min(T[k])), "C")
lap = {k: round(sum(v) / 3, 2) for k, v in T.items()}
check("Laplace A 36.67, B 36.67, C 38.33 -> C", (lap, max(lap, key=lap.get)), ({"A": 36.67, "B": 36.67, "C": 38.33}, "C"))
hur = {k: round(0.7 * max(v) + 0.3 * min(v), 2) for k, v in T.items()}
check("Hurwicz 0.7: A 50, B 45, C 40.5 -> A", (hur, max(hur, key=hur.get)), ({"A": 50.0, "B": 45.0, "C": 40.5}, "A"))
colmax = [max(T[k][i] for k in T) for i in range(3)]
reg = {k: [colmax[i] - T[k][i] for i in range(3)] for k in T}
check("regret table", reg, {"A": [0, 0, 50], "B": [20, 10, 20], "C": [35, 10, 0]})
check("minimax regret -> B (20)", min(T, key=lambda k: max(reg[k])), "B")
check("EVPI = EV with perfect information 55 - best EMV 45 = 10", round(sum(p * m for p, m in zip(pr, colmax)) - 45, 2), 10.0)
check("EV with perfect information = 24 + 25 + 6 = 55", round(sum(p * m for p, m in zip(pr, colmax)), 2), 55.0)
# decision tree: build plant big (win 0.6: 200, lose 0.4: -80) vs small (win 0.6: 60, lose: 10)
big = 0.6 * 200 + 0.4 * -80
small = 0.6 * 60 + 0.4 * 10
check("decision tree big 88, small 40", (round(big, 1), round(small, 1)), (88.0, 40.0))

# ---- critical path
dur = {"A": 4, "B": 6, "C": 5, "D": 3}
paths = {"A-B-D": dur["A"] + dur["B"] + dur["D"], "A-C-D": dur["A"] + dur["C"] + dur["D"]}
check("critical path A-B-D 13, A-C-D 12, slack C = 1", (paths, 13 - 12), ({"A-B-D": 13, "A-C-D": 12}, 1))
te = lambda a, m, b: round((a + 4 * m + b) / 6, 2)
check("PERT te (2,4,6)=4 ; (3,5,13)=6.0 ; (1,2,9)=3.0", (te(2, 4, 6), te(3, 5, 13), te(1, 2, 9)), (4.0, 6.0, 3.0))
check("PERT variance ((b-a)/6)^2 for (3,5,13) = 2.78", round(((13 - 3) / 6) ** 2, 2), 2.78)

# ---- span of control
gr = lambda n: n * (2 ** (n - 1) + n - 1)
check("Graicunas n=3,4,5,6 -> 18, 44, 100, 222", [gr(n) for n in (3, 4, 5, 6)], [18, 44, 100, 222])


def levels(workers, span):
    lv, tot, cur = 0, 0, workers
    while cur > 1:
        cur = -(-cur // span); tot += cur; lv += 1
    return lv, tot


check("625 operatives span 5 -> 4 manager levels, 156 managers", levels(625, 5), (4, 156))
check("625 operatives span 25 -> 2 levels, 26 managers", levels(625, 25), (2, 26))
check("1000 operatives span 10 -> 3 levels, 111 managers", levels(1000, 10), (3, 111))

# ---- motivation / leadership
check("Expectancy 0.8 x 0.9 x 7 = 5.04", round(0.8 * 0.9 * 7, 2), 5.04)
check("Expectancy with E=0 -> 0", 0 * 0.9 * 7, 0)
check("Fayol principles 14; Maslow 5; Deming points 14", (14, 5, 14), (14, 5, 14))

# ---- control
check("variance: budget 120000 actual 135000 = +15000 (12.5% over)", (135000 - 120000, (135000 - 120000) / 120000 * 100), (15000, 12.5))
check("control limits mean 50, sd 2: 44 and 56", (50 - 3 * 2, 50 + 3 * 2), (44, 56))
check("DPMO 34 defects / (500 units x 4 opp) = 17,000", 34 / (500 * 4) * 1_000_000, 17000.0)
check("yield 98.3%", round((1 - 34 / (500 * 4)) * 100, 1), 98.3)
check("Six Sigma = 3.4 DPMO (with 1.5 sigma shift): 99.99966%", round(100 - 3.4 / 1e6 * 100, 5), 99.99966)
check("inventory EOQ sqrt(2DS/H): D=1200,S=50,H=6 -> 141", round((2 * 1200 * 50 / 6) ** 0.5), 141)
check("ROI 30000/200000 = 15%", 30000 / 200000 * 100, 15.0)
check("Pareto: 20% of 10 causes = 2; they explain 8+7 of 25 = 60%", (10 * 0.2, (8 + 7) / 25 * 100), (2.0, 60.0))
check("weighted score: 0.5*8 + 0.3*6 + 0.2*9 = 7.6", round(0.5 * 8 + 0.3 * 6 + 0.2 * 9, 1), 7.6)
check("SWOT-style weighted: 3 options pick max", max({"X": 7.6, "Y": 7.1, "Z": 6.9}, key=lambda k: {"X": 7.6, "Y": 7.1, "Z": 6.9}[k]), "X")
check("ratio: 8 hours, 4 workers x 120 units = 480 -> productivity 15 units/hour per worker", 480 / (8 * 4), 15.0)
check("Taylor piece-rate: standard 100 units; 120 produced at Rs 5 -> higher rate Rs 6 -> pay 720", 120 * 6, 720)

import math
def _lv(w, sp):
    cur, t, l = w, 0, 0
    while cur > 1:
        cur = math.ceil(cur / sp); t += cur; l += 1
    return l, t
check("810 operatives span 3 -> 7 levels, 407 managers", _lv(810, 3), (7, 407))
check("810 operatives span 10 -> 91 managers", _lv(810, 10)[1], 91)
check("expectancy 0.6 x 0.5 x 8 = 2.4", round(0.6 * 0.5 * 8, 2), 2.4)
check("Q5: BEP 90000/(80-50) = 3000 units, Rs 240000; 4000 for profit 30000", (90000 / 30, 90000 / 30 * 80, 120000 / 30), (3000.0, 240000.0, 4000.0))
check("Q6 big EV 100, small 70", (0.5 * 300 + 0.5 * -100, 70), (100.0, 70))
check("Q7 critical path A-C-D 12, slack B 2", (3 + 7 + 2, 12 - (3 + 5 + 2)), (12, 2))
check("budget 800000 vs 920000: 120000 = 15%", (920000 - 800000, (920000 - 800000) / 800000 * 100), (120000, 15.0))
check("control limit 57 > 56 out of control", 57 > 50 + 3 * 2, True)
check("DPMO 25/(1000*5)*1e6 = 5000", 25 / (1000 * 5) * 1e6, 5000.0)

print(); print("ALL PASS" if not FAILS else f"{len(FAILS)} FAIL(S): {FAILS}")
sys.exit(1 if FAILS else 0)
