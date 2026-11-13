#!/usr/bin/env python3
"""Recompute every number added to BCA 154 Mathematics II unit 6 (session 43). Run: /tmp/v/bin/python bca/tools/check_math2_u6.py"""
from fractions import Fraction as F
import numpy as np
from scipy.optimize import linprog
ok = True
def chk(label, a, b, tol=1e-6):
    global ok
    good = abs(float(a) - float(b)) < tol if not isinstance(a, (list, tuple, np.ndarray)) else np.allclose(a, b, atol=tol)
    ok &= bool(good); print("ok  " if good else "FAIL", label, a if good else (a, b))
def lp(c, A, b, sense="max", **kw):
    cc = [-v for v in c] if sense == "max" else c
    r = linprog(cc, A_ub=A, b_ub=b, **kw); return r
# diet problem min 20x+30y, 2x+y>=8, x+2y>=10
r = linprog([20, 30], A_ub=[[-2, -1], [-1, -2]], b_ub=[-8, -10]); chk("diet x,y", r.x, [2, 4]); chk("diet Z", r.fun, 160)
# its dual: max 8u+10v, 2u+v<=20, u+2v<=30
r = lp([8, 10], [[2, 1], [1, 2]], [20, 30]); chk("dual u,v", r.x, [10/3, 40/3]); chk("dual W", -r.fun, 160)
# 3 variable production
r = lp([5, 4, 3], [[2, 3, 1], [4, 1, 2], [3, 4, 2]], [5, 11, 8]); chk("3var x", r.x, [2, 0, 1]); chk("3var Z", -r.fun, 13)
# special cases
r = linprog([-1, -1], A_ub=[[1, 1], [-1, -1]], b_ub=[2, -4]); print("infeasible status", r.status); ok &= r.status == 2
r = linprog([-1, -1], A_ub=[[1, -1], [-1, 1]], b_ub=[2, 3]); print("unbounded status", r.status); ok &= r.status == 3
r = lp([2, 2], [[1, 1], [1, 0], [0, 1]], [4, 3, 3]); chk("alt Z", -r.fun, 8)
# sensitivity of product mix  max 3x+2y, x+y<=b1, x+3y<=6
for b1 in (4, 6, 7):
    r = lp([3, 2], [[1, 1], [1, 3]], [b1, 6]); print("b1", b1, r.x, -r.fun)
for c1 in (1.5, 2, 3):
    r = lp([c1, 2], [[1, 1], [1, 3]], [4, 6]); print("c1", c1, r.x, -r.fun)
# practice 1 path O(0,0)->C(0,2)->B(3,1): max 2x+3y
r = lp([2, 3], [[1, 1], [1, 3]], [4, 6]); chk("p1", -r.fun, 9)
# Gauss-Jordan inverse
A = np.array([[2, 1, 1], [1, 3, 2], [1, 0, 0]], float); print("det", np.linalg.det(A)); print(np.linalg.inv(A))
# ill conditioning
A2 = np.array([[1, 1], [1, 1.0001]]); print("cond", np.linalg.cond(A2)); print(np.linalg.solve(A2, [2, 2.0001]), np.linalg.solve(A2, [2, 2.0002]))
# 3 s.f. pivoting demo
def r3(v):
    return float(f"{v:.3g}")
m = r3(1/0.0001); a22 = r3(1 - r3(m*0.0001)); a22 = r3(1 - r3(m*1)); b2 = r3(2 - r3(m*1)); y = r3(b2/a22); x = r3(r3(1 - r3(1*y))/0.0001)
print("no pivot", m, a22, b2, y, x)
m = r3(0.0001/1); a22 = r3(1 - r3(m*1)); b2 = r3(1 - r3(m*2)); y = r3(b2/a22); x = r3(2 - y); print("pivot", m, a22, b2, y, x)
# Gauss-Seidel / Jacobi with reordering
def gs(A, b, x0, n, jac=False):
    x = list(x0); out = []
    for k in range(n):
        old = list(x)
        for i in range(len(b)):
            src = old if jac else x
            x[i] = (b[i] - sum(A[i][j]*src[j] for j in range(len(b)) if j != i)) / A[i][i]
        out.append(list(x))
    return out
Abad = [[1, 2, 10], [10, 1, 1], [2, 10, 1]]; bbad = [35, 15, 25]
for k, row in enumerate(gs(Abad, bbad, [0, 0, 0], 4), 1): print("bad order GS", k, [round(v, 3) for v in row])
Agood = [[10, 1, 1], [2, 10, 1], [1, 2, 10]]; bgood = [15, 25, 35]
for k, row in enumerate(gs(Agood, bgood, [0, 0, 0], 6), 1): print("GS", k, [round(v, 4) for v in row])
for k, row in enumerate(gs(Agood, bgood, [0, 0, 0], 6, True), 1): print("Jac", k, [round(v, 4) for v in row])
# LU of the Gauss example
import scipy.linalg as sl
P, L, U = sl.lu(np.array([[2, 1, -1], [-3, -1, 2], [-2, 1, 2]], float)); print(P, L, U, sep="\n")
# false position & secant & Newton on x^3-x-2
f = lambda x: x**3 - x - 2; fp = lambda x: 3*x*x - 1; root = 1.5213797068045676
a, b = 1.0, 2.0
for n in range(1, 6):
    c = (a*f(b) - b*f(a)) / (f(b) - f(a)); print("RF", n, round(c, 5), round(f(c), 5)); 
    if f(a)*f(c) < 0: b = c
    else: a = c
x0, x1 = 1.0, 2.0
for n in range(1, 6):
    x2 = x1 - f(x1)*(x1 - x0)/(f(x1) - f(x0)); print("sec", n, round(x2, 6), round(f(x2), 6)); x0, x1 = x1, x2
x = 1.5
for n in range(1, 4): x = x - f(x)/fp(x); print("NR", n, x, abs(x-root))
# error comparison table
a, b = 1.0, 2.0; eb = []
for n in range(1, 9):
    m = (a+b)/2; eb.append(abs(m-root)); (b := m) if f(a)*f(m) < 0 else (a := m)
print("bisect errors", ["%.1e" % e for e in eb])
# Newton failure cycle x^3-2x+2 from 0
g = lambda x: x**3 - 2*x + 2; gp = lambda x: 3*x*x - 2
x = 0.0
for n in range(6): x = x - g(x)/gp(x); print("cycle", n+1, x)
# sqrt 10 Newton
x = 3.0
for n in range(1, 5): x = (x + 10/x)/2; print("sqrt10", n, "%.10f" % x)
# EMI rate: loan 100000, 12 months, EMI 9000 -> monthly rate r ; 100000 = 9000*(1-(1+r)^-12)/r
h = lambda r: 9000*(1-(1+r)**-12)/r - 100000
lo, hi = 0.001, 0.05
for n in range(1, 8):
    m = (lo+hi)/2; print("emi bis", n, round(m, 5), round(h(m), 1)); lo, hi = (m, hi) if h(m) > 0 else (lo, m)
from scipy.optimize import brentq
r = brentq(h, 0.001, 0.05); print("emi r", r, "annual", 12*r)
print("ALL OK" if ok else "SOME FAILED")
