#!/usr/bin/env python3
"""Recompute every numeric example of BCA 206 Applied Economics (semester-3/applied-economics). python3 bca/tools/check_economics.py"""
import math
def put(k, v): print(f"{k:34s}", v)
# U1
P = (100 - 20) / 5; put("equilibrium P,Q", (P, 100 - 2 * P)); put("ceiling P=10 shortage", (100 - 20) - (20 + 30) )
put("demand shift", ((120 - 20) / 5, 20 + 3 * 20)); P = 95 / 5; put("tax: P,Q,buyer pays,seller gets,rev", (P, 100 - 2 * P, P - 16, P - 5, 5 * (100 - 2 * P))); put("Q4 eq", ((200 - 50) / 6, 200 - 4 * 25, (200 - 80) - (50 + 40)))
# U2
mid = lambda a, b: (a + b) / 2
def arc(q0, q1, p0, p1): return ((q1 - q0) / mid(q0, q1)) / ((p1 - p0) / mid(p0, p1))
put("outlay", (10 * 100, 8 * 130, 8 * 110)); put("arc e (10->8,100->130)", round(arc(100, 130, 10, 8), 3))
put("point e P=20,25,30", tuple(round(-2 * p / (100 - 2 * p), 3) for p in (20, 25, 30))); put("TR at P=25", 25 * 50)
put("income e", round(arc(50, 56, 20000, 24000), 3), ); put("cross e", round(arc(80, 88, 10, 12), 3)); put("supply e", round(arc(200, 260, 50, 60), 3))
put("U2 Q1 arc,TE", (round(arc(200, 150, 20, 25), 3), 20 * 200, 25 * 150)); put("Q2 point", (round(-4 * 5 / 60, 3), round(-4 * 15 / 20, 3), 'P=10')); put("Q7 es", round(arc(500, 560, 100, 110), 3))
# U3
TU = [10, 18, 24, 28, 30]; put("MU", [TU[0]] + [TU[i] - TU[i - 1] for i in range(1, 5)])
X = [16, 12, 8, 4]; Y = [10, 8, 6, 4, 2]; px, py, inc = 4, 2, 20
items = sorted([(X[i] / px, 'X', px, X[i]) for i in range(4)] + [(Y[i] / py, 'Y', py, Y[i]) for i in range(5)], key=lambda t: (-t[0], t[1] == 'X'))
spent = 0; nx = ny = 0; tu = 0
for r, g, c, mu in items:
    if spent + c <= inc: spent += c; tu += mu; nx += g == 'X'; ny += g == 'Y'
put("bundle X,Y,spent,TU", (nx, ny, spent, tu))
M, px, py = 120, 4, 2; x0, y0 = M / (2 * px), M / (2 * py); U = x0 * y0; px2 = 8; x1 = M / (2 * px2)
xc = math.sqrt(U * py / px2); yc = math.sqrt(U * px2 / py); put("opt before", (x0, y0, U)); put("opt after", (x1, M / (2 * py), x1 * M / (2 * py)))
put("hicks x,y,expenditure", (round(xc, 3), round(yc, 3), round(px2 * xc + py * yc, 3))); put("SE,IE,total", (round(xc - x0, 3), round(x1 - xc, 3), x1 - x0))
put("Q6", (80 / 4, 80 / 8, (80 / 4) * (80 / 8))); put("Q3 intercepts", (100 / 5, 100 / 10))
# U4
tvc = [0, 50, 90, 120, 160, 220, 300]
for q in range(1, 7): tc = 100 + tvc[q]; put(f"Q={q} TC,MC,AFC,AVC,AC", (tc, tc - (100 + tvc[q - 1]), round(100 / q, 1), tvc[q] / q, round(tc / q, 2)))
tv = [20, 36, 48, 64, 90]; put("Q2 TC,MC,AVC,AC", ([60 + v for v in tv], [20] + [tv[i] - tv[i - 1] for i in range(1, 5)], [v / (i + 1) for i, v in enumerate(tv)], [(60 + v) / (i + 1) for i, v in enumerate(tv)]))
put("econ profit shop", 500000 - 350000 - 100000 - 30000); put("Q4 MR TR max", (60 / 4, 60 * 15 - 2 * 15 ** 2)); put("Q7", (800 - 500, 800 - 850))
put("AR=100-Q: Q20,Q30,TRmax", ((100 - 20, 100 * 20 - 400, 100 - 40), (70, 2100, 100 - 60, 70 * (1 - 1 / (70 / 30))), (50, 2500)))
# U5
put("P=60 profit", (60 * 5 - 320)); put("P=80 profit", (80 * 6 - 400)); Q = 40; put("monopoly Q,P,TR,TC,profit", (Q, 100 - Q, Q * 60, 500 + 20 * Q, Q * 60 - 500 - 20 * Q)); put("DWL", .5 * 40 * 40)
put("discr Q1,P1,Q2,P2,profit", (40, 60, 20, 40, 40 * 40 + 20 * 20)); put("single price Q,P,profit", (60, 50, (50 - 20) * 60))
put("cartel Q,P,each,joint", (40, 60, (60 - 20) * 20, 1600)); put("cheat A,B", ((50 - 20) * 30, (50 - 20) * 20))
put("Q2 output,profit", ((50 - 10) / 2, (50 - 35) * 20)); put("Q4 mono,profit,comp", ((80 - 20) / 2, 80 - 30, 30 * 50 - 100 - 20 * 30, 80 - 20))
# U6
C, I, G, Xp, Mp, nfia, dep, nit = 600, 200, 150, 100, 120, 20, 50, 40; gdp = C + I + G + Xp - Mp; gnp = gdp + nfia; nnp = gnp - dep; ni = nnp - nit
pi = ni - 30 - 20 + 25; di = pi - 60; put("GDP,GNP,NNP,NI,PI,DI,PCI", (gdp, gnp, nnp, ni, pi, di, ni / 10)); put("income method", 500 + 60 + 50 + 250)
y = 200 / .2; put("2-sector Y,S,k,dY", (y, -100 + .2 * y, 1 / .2, 20 * 5)); put("3-sector Y", 220 / .2); put("value added", (100, 250 - 100, 400 - 250, 100 + 150 + 150))
put("deflator example", (1320 / 1.2, 1320 / 1000 - 1, 1320 / 1.2 / 1000 - 1)); put("Q2 GDP..NI", (800 + 250 + 200 + 150 - 180, 800 + 250 + 200 - 30 + 0, ))
g2 = 800 + 250 + 200 + 150 - 180; put("Q2 chain", (g2, g2 - 30, g2 - 30 - 70, g2 - 30 - 70 - 60)); put("Q3", (100 / .25, 100 / .25 - (50 + .75 * 400), 1 / .25)); put("Q4", (2860 / 1.3, (2860 / 1.3 - 2000) / 2000, 2860 / 2000 - 1))
# U7
put("multiplier 10%,20%", (1 / .1, 1000 / .1, 1000 / .1 - 1000, 1 / .2, 1000 / .2)); put("CPI,inflation", (5900 / 5000 * 100, round((118 - 112) / 112 * 100, 2))); put("value of money 125", 100 / 125)
put("BoP", (-350 + 10 + 300, -350 + 10 + 300 + 30)); put("Q2 ", (5000 / .2, 1 / .2)); put("Q3", ((132 - 120) / 120, 120 / 132 - 1)); put("Q6 BoT", 80 - 300)
# ---- Session 40 depth sections (1.7 surplus and taxes, 2.5 incidence, 3.5 CS/Engel, 4.6 production, 5.8 Cournot/HHI, 6.7 C-function/Lorenz, 7.6 trade/quantity theory)
print("--- session 40 additions")
D = lambda q: 60 - q / 2; S = lambda q: 10 + q / 3          # Qd = 120-2P, Qs = 3P-30
qe = 60; pe = 30; cs = .5 * (60 - pe) * qe; ps = .5 * (pe - 10) * qe; put("1.7 eq CS,PS,total", (cs, ps, cs + ps))
qc = 30; cs_c = 60 * 30 - 30 ** 2 / 4 - 20 * 30; ps_c = .5 * (20 - 10) * 30; put("1.7 ceiling 20: Qd,Qs,short,CS,PS,DWL", (120 - 40, 3 * 20 - 30, 80 - 30, cs_c, ps_c, cs + ps - cs_c - ps_c, .5 * (D(30) - 20) * 30))
qt = (60 - 25) / (.5 + 1 / 3); pb = D(qt); pse = pb - 15; put("1.7 tax 15: Q,Pbuyer,Pseller,revenue,DWL,CS,PS", (qt, pb, pse, 15 * qt, .5 * 15 * (60 - qt), .5 * (60 - pb) * qt, .5 * (pse - 10) * qt))
assert abs(cs + ps - (.5 * (60 - pb) * qt + .5 * (pse - 10) * qt + 15 * qt) - .5 * 15 * (60 - qt)) < 1e-9
for nm, b in (("A b=1", 1), ("B b=3", 3), ("C b=.5", .5)):                    # demand slope b, supply slope c=1
    a = 60 + b * 40; q = (a - 20 + 0) / (b + 1) if False else (a - 32) / (b + 1); pbb = a - b * q
    ed = (1 / b) * 60 / 40; es = 1 * 60 / 40
    put("2.5 tax 12 " + nm, (round(q, 2), round(pbb, 2), round(pbb - 60, 2), round(60 - (pbb - 12), 2), 12 * round(q, 2), round(.5 * 12 * (40 - q), 2), "Ed", round(ed, 3), "Es", es, "buyer share", round(es / (es + ed), 3)))
wtp = [50, 40, 30, 20, 10]; put("3.5 CS price 25", (sum(w - 25 for w in wtp if w >= 25), sum(w - 15 for w in wtp if w >= 15), sum(w - 5 for w in wtp)))
def mid_e(q0, q1, y0, y1): return ((q1 - q0) / mid(q0, q1)) / ((y1 - y0) / mid(y0, y1))
put("3.5 Engel rice,data,bus", (round(mid_e(30, 33, 20, 30), 3), round(mid_e(5, 9, 20, 30), 3), round(mid_e(40, 30, 20, 30), 3)))
Lq = 4 * 50; Kq = 50; put("4.6 cost-min Q=100 (L,K,cost)", (200, 50, 100 * 200 + 400 * 50, math.sqrt(200 * 50), 50 / 200, 100 / 400))
put("4.6 RTS 2^1.2,2^.8,2^1", (round(2 ** 1.2, 3), round(2 ** .8, 3), 2)); put("4.6 SR K=100: AC min", (min((q + 40000 / q, q) for q in range(1, 600)), "MC=2Q at 200", 2 * 200))
r = 80 / 3; Pc = 100 - 2 * r; put("5.8 Cournot q,Q,P,profit each,total", (round(r, 3), round(2 * r, 3), round(Pc, 3), round((Pc - 20) * r, 2), round(2 * (Pc - 20) * r, 2)))
put("5.8 Stackelberg q1,q2,P,pi1,pi2", (40, 20, 40, 20 * 40, 20 * 20)); put("5.8 cartel,competitive", (1600, 0))
put("5.8 HHI", (55 ** 2 + 35 ** 2 + 10 ** 2, 4 * 25 ** 2, 10 * 10 ** 2, 100 ** 2))
Y = 500 / .2; put("6.7 C=200+.8Y: Y,C,S,k,dY(I+50)", (Y, 200 + .8 * Y, Y - 200 - .8 * Y, 5, 250)); put("6.7 tax .25 k", 1 / (1 - .8 * .75)); put("6.7 bal.budget dY", 100 / .2 - .8 * 100 / .2)
sh = [5, 9, 14, 22, 50]; cum = [sum(sh[:i + 1]) for i in range(5)]; area = sum(.2 * (a + b) / 2 / 100 for a, b in zip([0] + cum[:-1], cum)); put("6.7 Lorenz cum, area, Gini", (cum, round(area, 3), round(1 - 2 * area, 3), round(.5 - area, 3)))
put("7.6 CA opp costs", (2 / 3, 1.5, .5, 2)); put("7.6 Nepal no trade", (30, 20)); put("7.6 Nepal trade", (40, 20, 35)); put("7.6 India no trade/trade", ((60, 30), (85, 20), "hc 10 = ginger", 20, "net", 25 - 20))
put("7.6 ToT", 120 / 150 * 100); Qd = lambda p: 120 - p; Qs = lambda p: p - 20
put("7.6 tariff 10: Qd,Qs,imports before/after", (Qd(40), Qs(40), Qd(40) - Qs(40), Qd(50), Qs(50), Qd(50) - Qs(50)))
put("7.6 tariff: CS loss,PS gain,revenue,DWL", (10 * 70 + .5 * 10 * 10, 10 * 20 + .5 * 10 * 10, 10 * 40, 750 - 250 - 400))
put("7.6 MV=PY", (1500 * 4 / 2000, 1650 * 4 / 2000, 1650 / 1500 - 1)); put("7.6 Fisher", (9 - 6, round((1.09 / 1.06 - 1) * 100, 3)))
