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
