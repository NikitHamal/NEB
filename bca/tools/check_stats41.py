#!/usr/bin/env python3
"""BCA 205 session 41: recompute every number quoted in the new sections 2.5-2.6, 3.5-3.6, 4.7-4.8, 6.11, 7.7."""
import math, numpy as np, statistics as st
from math import comb, exp
from scipy import stats
ok = lambda a, b, tol=0.006: abs(a - b) <= tol * max(1, abs(b))
def chk(name, a, b, tol=0.006):
    print(("ok   " if ok(a, b, tol) else "FAIL ") + name, round(a, 4), b); assert ok(a, b, tol), name
# unit 2
chk("GM growth", math.prod([1.1, 1.2, 1.5]) ** (1 / 3), 1.2557); chk("HM 60/40", st.harmonic_mean([60, 40]), 48)
chk("weighted", (2 * 72 + 3 * 85 + 60) / 6, 76.5); chk("GM 2,8,4", st.geometric_mean([2, 8, 4]), 4); chk("HM 2,8,4", st.harmonic_mean([2, 8, 4]), 3.429)
d = np.array([1, 2, 3, 4, 10.]); m = d - d.mean(); mu = [(m ** k).mean() for k in range(5)]
chk("g1", mu[3] / mu[2] ** 1.5, 1.138); chk("b2", mu[4] / mu[2] ** 2, 2.788)
chk("Bowley q13", (34.58 + 18.5 - 2 * 26.11) / (34.58 - 18.5), 0.054, 0.02)
# unit 3
x = np.array([2, 3, 4, 5, 6, 7, 8.]); y = np.array([45, 50, 58, 60, 68, 72, 80.]); r = np.corrcoef(x, y)[0, 1]; b, a = np.polyfit(x, y, 1)
chk("r", r, 0.9945); chk("b", b, 5.679); chk("a", a, 33.464); res = y - (a + b * x); chk("se", math.sqrt((res ** 2).sum() / 5), 1.4117)
chk("t of r", r * math.sqrt(5) / math.sqrt(1 - r * r), 21.3, 0.01)
chk("r12.3", (0.8 - 0.42) / math.sqrt(0.51 * 0.64), 0.665); chk("R", math.sqrt((0.64 + 0.49 - 0.672) / 0.64), 0.846)
chk("PE", 0.6745 * 0.36 / 5, 0.0486, 0.01)
# unit 4
chk("hyp", comb(6, 2) * comb(14, 3) / comb(20, 5), 0.3522); chk("geo", 0.8 ** 4 * 0.2, 0.0819, 0.01); chk("exp", exp(-1.5), 0.2231)
chk("normal approx", stats.norm.cdf(5.5 / math.sqrt(24)), 0.869, 0.005); chk("exact", stats.binom.cdf(45, 100, .4), 0.8689)
chk("clt", 1 - stats.norm.cdf(1.5), 0.0668)
# unit 6
chk("t one", 4 / 1.5, 2.667); chk("p one", 2 * (1 - stats.t.cdf(4 / 1.5, 15)), 0.0176, 0.02)
sp2 = (9 * 36 + 11 * 49) / 20; se = math.sqrt(sp2 * (1 / 10 + 1 / 12)); chk("sp2", sp2, 43.15); chk("t two", 6 / se, 2.13, 0.01)
bf = np.array([12, 15, 11, 14, 13, 16, 12, 15.]); af = np.array([10, 13, 11, 11, 12, 13, 10, 14.]); chk("paired t", stats.ttest_rel(bf, af).statistic, 4.78, 0.01)
chk("prop z", (0.59 - 0.5) / math.sqrt(0.25 / 200), 2.55, 0.01); chk("beta", stats.norm.cdf((50 + 1.645 * 10 / 6 - 54) / (10 / 6)), 0.225, 0.02)
# unit 7
L = ["ABCD", "BCDA", "CDAB", "DABC"]; Y = np.array([[39, 34, 35, 40], [37, 27, 38, 28], [28, 31, 31, 29], [36, 22, 31, 21.]])
CF = Y.sum() ** 2 / 16; sst = (Y ** 2).sum() - CF; ssr = (Y.sum(1) ** 2).sum() / 4 - CF; ssc = (Y.sum(0) ** 2).sum() / 4 - CF
T = {k: sum(Y[i, j] for i in range(4) for j in range(4) if L[i][j] == k) for k in "ABCD"}; sstr = sum(v * v for v in T.values()) / 4 - CF
sse = sst - ssr - ssc - sstr; chk("SSE", sse, 8.875); chk("F", sstr / 3 / (sse / 6), 36.3, 0.01)
chk("F one-way", stats.f_oneway(*[[Y[i, j] for i in range(4) for j in range(4) if L[i][j] == k] for k in "ABCD"]).statistic, 1.95, 0.01)
chk("LSD", stats.t.ppf(.975, 6) * math.sqrt(2 * sse / 6 / 4), 2.10, 0.01)
print("ALL OK")
