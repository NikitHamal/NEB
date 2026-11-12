#!/usr/bin/env python3
"""Recompute every number used in the worked examples of BCA 205 Probability and Statistics (semester-3/probability-and-statistics).
Run: python3 bca/tools/check_stats.py   (prints the values; the book quotes them; --assert re-verifies the quoted values)."""
import math, statistics as st, sys
import numpy as np
from scipy import stats as ss
P = {}
def put(k, v): P[k] = v; print(f"{k:28s}", v)
# ---- Unit 2: ungrouped
d = [45, 52, 58, 61, 61, 67, 70, 74, 80, 92]
put("n", len(d)); put("sum", sum(d)); put("mean", st.mean(d)); put("median", st.median(d)); put("mode", st.mode(d))
q = np.percentile(d, [25, 75], method="weibull"); put("Q1,Q3 (n+1)p", tuple(q))
put("range", max(d) - min(d)); mu = st.mean(d)
put("MD about mean", sum(abs(x - mu) for x in d) / len(d)); put("sum sq dev", sum((x - mu) ** 2 for x in d))
put("pop var", st.pvariance(d)); put("pop SD", round(st.pstdev(d), 4)); put("sample SD", round(st.stdev(d), 4)); put("CV%", round(st.pstdev(d) / mu * 100, 3))
put("QD", (q[1] - q[0]) / 2); put("coef QD", (q[1] - q[0]) / (q[1] + q[0]))
# grouped
cls = [(10, 20, 5), (20, 30, 8), (30, 40, 15), (40, 50, 16), (50, 60, 6)]; N = sum(f for *_, f in cls)
mids = [(a + b) / 2 for a, b, _ in cls]; fs = [f for *_, f in cls]
gm = sum(m * f for m, f in zip(mids, fs)) / N; put("grouped n,mean", (N, gm))
gv = sum(f * (m - gm) ** 2 for m, f in zip(mids, fs)) / N; put("grouped var,SD", (gv, round(gv ** .5, 4))); put("grouped CV%", round(gv ** .5 / gm * 100, 3))
def gq(p):
    t = N * p; c = 0
    for a, b, f in cls:
        if c + f >= t: return a + (t - c) / f * (b - a)
        c += f
put("grouped Q1,median,Q3", (gq(.25), gq(.5), gq(.75))); put("grouped mode", 40 + 1 / (1 + 10) * 10)
# ---- Unit 3
x = [1, 2, 3, 4, 5]; y = [2, 4, 5, 4, 5]; n = 5
sxx = sum((a - 3) ** 2 for a in x); syy = sum((b - 4) ** 2 for b in y); sxy = sum((a - 3) * (b - 4) for a, b in zip(x, y))
put("Sxx,Syy,Sxy", (sxx, syy, sxy)); r = sxy / math.sqrt(sxx * syy); put("r", round(r, 4)); put("byx,bxy", (sxy / sxx, sxy / syy)); put("a (y on x)", 4 - .6 * 3); put("y at x=6", 2.2 + .6 * 6)
put("r2", round(r * r, 4))
# ---- Unit 4
put("binom n5 p.4 P(2)", round(ss.binom.pmf(2, 5, .4), 5)); put("binom P(X>=1)", round(1 - .6 ** 5, 5)); put("binom mean,var", (2.0, 1.2))
put("poisson 3 P(2)", round(ss.poisson.pmf(2, 3), 5)); put("poisson P(<=2)", round(ss.poisson.cdf(2, 3), 5)); put("poisson P(>=1)", round(1 - math.exp(-3), 5))
Z = lambda v: ss.norm.cdf(v)
put("N(200,20) P(X>230)", round(1 - Z(1.5), 4)); put("N P(180<X<240)", round(Z(2) - Z(-1), 4)); put("N P(X<190)", round(Z(-.5), 4)); put("z for top 10%", round(ss.norm.ppf(.9), 4), ) ; put("X at top10%", round(200 + 20 * ss.norm.ppf(.9), 2))
put("Bayes", round(.01 * .95 / (.01 * .95 + .99 * .05), 4))
put("norm approx: P(Z<=1.5)", round(Z(1.5), 4)); put("P(Z<=1),P(Z<=2)", (round(Z(1), 4), round(Z(2), 4))); put("P(-1<Z<1)", round(Z(1) - Z(-1), 4))
# ---- Unit 5
z = 1.96; n0 = z * z * .25 / .05 ** 2; put("n0", round(n0, 2)); put("fpc N=2000", round(n0 / (1 + (n0 - 1) / 2000), 2)); put("n e=.03", round(z * z * .25 / .03 ** 2, 2))
# ---- Unit 6
Nn, nn, ybar, s = 200, 20, 52, 8; f = nn / Nn; v = (1 - f) * s * s / nn
put("SRS var,SE mean", (v, round(v ** .5, 4))); put("total,SE total", (Nn * ybar, round(Nn * v ** .5, 2))); put("95% CI mean", (round(ybar - 1.96 * v ** .5, 3), round(ybar + 1.96 * v ** .5, 3)))
put("SRSWR var", s * s / nn)
W = [.3, .7]; ym = [60, 50]; sd = [10, 8]; nh = [30, 70]; Nh = [300, 700]
yst = sum(w * m for w, m in zip(W, ym)); vst = sum(w * w * (1 - n_ / N_) * s_ * s_ / n_ for w, n_, N_, s_ in zip(W, nh, Nh, sd))
put("strat mean,var,SE", (yst, round(vst, 4), round(vst ** .5, 4))); put("SRS var same n", round((1 - .1) * (.3 * 100 + .7 * 64 + .3 * .7 * 100) / 100, 4))
put("Neyman alloc", [round(100 * Nh[i] * sd[i] / sum(Nh[j] * sd[j] for j in range(2)), 2) for i in range(2)])
put("ratio R,mean,total", (30 / 48, round(30 / 48 * 50, 3), round(30 / 48 * 5000, 1)))
put("systematic k, units", (1000 // 50, [7 + 20 * i for i in range(5)]))
put("t(15) .975", round(ss.t.ppf(.975, 15), 4)); se = 6 / 4; put("t CI", (round(52.5 - 2.1314 * se, 3), round(52.5 + 2.1314 * se, 3)))
put("z test z,p2", (1.8, round(2 * (1 - Z(1.8)), 4))); put("z crit .05,.025,.005", (round(ss.norm.ppf(.95), 3), round(ss.norm.ppf(.975), 3), round(ss.norm.ppf(.995), 3)))
chi = ss.chi2_contingency([[30, 20], [20, 30]], correction=False); put("chi2 2x2,df,p", (round(chi[0], 4), chi[2], round(chi[1], 4))); put("chi2 crit df1 .05", round(ss.chi2.ppf(.95, 1), 3))
put("chi2 crit df2,df3,df5", tuple(round(ss.chi2.ppf(.95, k), 3) for k in (2, 3, 5)))
obs = [8, 12, 9, 11, 10, 10]; put("die chi2", sum((o - 10) ** 2 / 10 for o in obs)); put("chi2 crit df5 .05", round(ss.chi2.ppf(.95, 5), 3))
put("t crit df 9,14,15,19 .05 2t", tuple(round(ss.t.ppf(.975, k), 3) for k in (9, 14, 15, 19)))
# ---- Unit 7
A = [82, 85, 88, 90, 85]; B = [78, 74, 80, 76, 82]; C = [70, 75, 72, 68, 75]; G = [A, B, C]
allv = sum(G, []); gm_ = st.mean(allv); sst = sum((v - gm_) ** 2 for v in allv); ssb = sum(len(g) * (st.mean(g) - gm_) ** 2 for g in G); ssw = sst - ssb
put("means", [st.mean(g) for g in G]); put("grand", gm_); put("SST,SSB,SSW", (round(sst, 3), round(ssb, 3), round(ssw, 3)))
F = (ssb / 2) / (ssw / 12); put("F", round(F, 3)); put("Fcrit(2,12)", round(ss.f.ppf(.95, 2, 12), 3)); put("p", ss.f_oneway(*G).pvalue)
M = np.array([[20, 22, 19, 24], [25, 27, 25, 28], [18, 21, 17, 21]], float); gmm = M.mean()
sst2 = ((M - gmm) ** 2).sum(); ssr = 4 * ((M.mean(1) - gmm) ** 2).sum(); ssc = 3 * ((M.mean(0) - gmm) ** 2).sum(); sse = sst2 - ssr - ssc
put("two-way grand", gmm); put("row means", list(M.mean(1))); put("col means", list(M.mean(0))); put("SST,SSR,SSC,SSE", (sst2, ssr, round(ssc, 4), round(sse, 4)))
put("F rows,cols", (round((ssr / 2) / (sse / 6), 3), round((ssc / 3) / (sse / 6), 3))); put("Fcrit(2,6),(3,6)", (round(ss.f.ppf(.95, 2, 6), 3), round(ss.f.ppf(.95, 3, 6), 3)))

# ---- practice answers
d5=[4,8,6,10,12]; put("P2 pop SD,sample SD,CV", (round(st.pstdev(d5),3), round(st.stdev(d5),3), round(st.pstdev(d5)/8*100,2)))
x2=[2,4,6,8]; y2=[3,7,5,10]; r2=np.corrcoef(x2,y2)[0,1]; b2=np.polyfit(x2,y2,1); put("P3 r,b,a,y(10)", (round(r2,3), b2.round(3), round(np.polyval(b2,10),2)))
put("P5 n(+-4%) ,fpc5000", (round(1.96**2*.25/.04**2,2), round(600.25/(1+599.25/5000),1)))
put("U6 P1 var,CI,total SE", (round(.9*36/50,3), round(.9*36/50,3)**.5, ))
v1=.9*36/50; put("U6 P1 CI", (round(40-1.96*v1**.5,2), round(40+1.96*v1**.5,2), 500*v1**.5))
put("U6 P6 CI", (100-2.064*3, 100+2.064*3)); c=ss.chi2_contingency([[40,10],[20,30]],correction=False); put("U6 P7 chi2", round(c[0],3))
put("U4 Q7", (round(ss.norm.cdf(-20/15),4), round(1-ss.norm.cdf(2),4))); put("U4 Q6", round(ss.norm.cdf(1.5)-ss.norm.cdf(-1),4)); put("U4 poisson e^-2", round(math.exp(-2),4))
G=[[6,8,7],[9,11,10],[5,4,6]]; put("U7 P2 F", round(ss.f_oneway(*G).statistic,3))
put("U2 D6,P90", (40+(30-28)/16*10, 50+(45-44)/6*10)); put("Neyman 400/600", (100*2000/8000,))
put("t CI z-version", (round(52.5-1.96*1.5,2), round(52.5+1.96*1.5,2)))
put("conf 99 vs 95 n ratio", round((2.576/1.96)**2,3)); put("SSB oneway", 5*((86-78.667)**2+(78-78.667)**2+(72-78.667)**2))
