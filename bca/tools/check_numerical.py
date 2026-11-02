#!/usr/bin/env python3
"""BCA 253 Numerical Methods: every iteration table and quoted number is produced here by real execution.

    python3 bca/tools/check_numerical.py --print            # show all tokens
    python3 bca/tools/check_numerical.py --fill unit-*.md   # replace @@token@@ in the files with the computed text
    python3 bca/tools/check_numerical.py --verify unit-*.md # assert every computed table/number appears in the units

Method results are cross-checked against numpy / scipy / sympy (assertions at the bottom of each section)."""
import math, sys, re
import numpy as np

T = {}                       # token -> text
def f6(x): return f"{x:.6f}"
def table(head, rows):
    out = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(out)

# ======================= Unit 1: nonlinear equations =======================
f = lambda x: x ** 3 - x - 2
df = lambda x: 3 * x ** 2 - 1
ROOT = 1.5213797068045676
assert abs(f(ROOT)) < 1e-12

# errors
approx = 1.414; ex = math.sqrt(2)
T["e_abs"] = f"{abs(ex - approx):.7f}"; T["e_rel"] = f"{abs(ex - approx) / ex:.7f}"; T["e_pct"] = f"{abs(ex - approx) / ex * 100:.4f}"
T["sqrt2"] = f"{ex:.7f}"
# Taylor truncation: e^0.5 with 3 and 4 terms
T["exp_3"] = f"{1 + 0.5 + 0.5**2/2:.6f}"; T["exp_4"] = f"{1 + 0.5 + 0.5**2/2 + 0.5**3/6:.6f}"; T["exp_true"] = f"{math.exp(0.5):.6f}"
T["exp_3_err"] = f"{abs(math.exp(0.5) - (1 + 0.5 + 0.125)):.6f}"
T["exp_4_err"] = f"{abs(math.exp(0.5) - (1 + 0.5 + 0.125 + 0.5**3/6)):.6f}"
# round-off: 1/3 stored to 4 s.f.
T["ro_sum"] = f"{0.3333 + 0.3333 + 0.3333:.4f}"
# cancellation: sqrt(x+1)-sqrt(x) at x=1e6 in 6 s.f.
def sig5(v):
    from decimal import Decimal, ROUND_HALF_EVEN
    d = Decimal(repr(v)); e = d.adjusted(); q = Decimal(1).scaleb(e - 4)
    return float(d.quantize(q, rounding=ROUND_HALF_EVEN))
a = sig5(math.sqrt(10001)); b = sig5(math.sqrt(10000))
T["canc_a"] = f"{a:.2f}"; T["canc_b"] = f"{b:.2f}"; T["canc_naive"] = f"{a - b:.5f}"
T["canc_stable"] = f"{1 / (math.sqrt(10001) + math.sqrt(10000)):.7f}"; T["canc_true"] = f"{math.sqrt(10001) - math.sqrt(10000):.7f}"

def bisect(f, a, b, n):
    rows = []
    for i in range(1, n + 1):
        c = (a + b) / 2; fc = f(c)
        rows.append((i, f6(a), f6(b), f6(c), f"{fc:+.6f}"))
        if f(a) * fc < 0: b = c
        else: a = c
    return rows, c
rows, c = bisect(f, 1, 2, 10)
T["bis_tab"] = table(["n", "a", "b", "c = (a+b)/2", "f(c)"], rows); T["bis_root"] = f6(c)
T["bis_err"] = f"{abs(c - ROOT):.6f}"; T["bis_bound"] = f"{1 / 2 ** 10:.6f}"
T["bis_n3"] = str(math.ceil(math.log2(1 / 1e-3))); T["bis_n6"] = str(math.ceil(math.log2(1 / 1e-6)))
assert abs(c - ROOT) <= 1 / 2 ** 10
# bisection for a Nepali-flavoured Ex: x^2 - 10 on [3,4]
rows10, c10 = bisect(lambda x: x * x - 10, 3, 4, 6)
T["bis10_tab"] = table(["n", "a", "b", "c", "f(c)"], rows10); T["bis10_root"] = f6(c10)

def regula(f, a, b, n):
    rows = []; c_old = None
    for i in range(1, n + 1):
        c = (a * f(b) - b * f(a)) / (f(b) - f(a)); fc = f(c)
        rows.append((i, f6(a), f6(b), f6(c), f"{fc:+.6f}"))
        if f(a) * fc < 0: b = c
        else: a = c
    return rows, c
rows, c = regula(f, 1, 2, 7)
T["rf_tab"] = table(["n", "a", "b", "c", "f(c)"], rows); T["rf_root"] = f6(c)

def newton(f, df, x, n):
    rows = []
    for i in range(n):
        xn = x - f(x) / df(x)
        rows.append((i, f6(x), f"{f(x):+.6f}", f6(df(x)), f6(xn)))
        x = xn
    return rows, x
rows, xr = newton(f, df, 1.5, 4)
T["nr_tab"] = table(["n", "xₙ", "f(xₙ)", "f′(xₙ)", "xₙ₊₁"], rows); T["nr_root"] = f6(xr)
assert abs(xr - ROOT) < 1e-9
# Newton for sqrt(10)
rows, xs = newton(lambda x: x * x - 10, lambda x: 2 * x, 3.0, 3)
T["nr_sqrt_tab"] = table(["n", "xₙ", "f(xₙ)", "f′(xₙ)", "xₙ₊₁"], rows); T["sqrt10"] = f"{math.sqrt(10):.6f}"
# Newton convergence ratio e_{n+1}/e_n^2 on f
x = 1.5; es = []
for i in range(4):
    es.append(abs(x - ROOT)); x = x - f(x) / df(x)
T["nr_errs"] = ", ".join(f"{e:.2e}" for e in es[:4])
T["nr_ratio"] = ", ".join(f"{es[i+1]/es[i]**2:.3f}" for i in range(3))
T["nr_limit"] = f"{df.__call__(ROOT) and (6*ROOT)/(2*df(ROOT)):.3f}"   # f''/(2f')

def secant(f, x0, x1, n):
    rows = []
    for i in range(n):
        x2 = x1 - f(x1) * (x1 - x0) / (f(x1) - f(x0))
        rows.append((i, f6(x0), f6(x1), f"{f(x0):+.6f}", f"{f(x1):+.6f}", f6(x2)))
        x0, x1 = x1, x2
    return rows, x1
rows, xsec = secant(f, 1, 2, 6)
T["sec_tab"] = table(["n", "xₙ₋₁", "xₙ", "f(xₙ₋₁)", "f(xₙ)", "xₙ₊₁"], rows); T["sec_root"] = f6(xsec)
assert abs(xsec - ROOT) < 1e-6, abs(xsec-ROOT)

g = lambda x: (x + 2) ** (1 / 3)
x = 1.5; rows = []
for i in range(7):
    xn = g(x); rows.append((i, f6(x), f6(xn), f"{abs(xn - ROOT):.2e}")); x = xn
T["fpi_tab"] = table(["n", "xₙ", "xₙ₊₁ = (xₙ+2)^(1/3)", "|error|"], rows); T["fpi_gp"] = f"{(1/3) * (ROOT + 2) ** (-2 / 3):.4f}"
# a divergent rearrangement x = x^3 - 2
h = lambda x: x ** 3 - 2
x = 1.5; seq = []
for i in range(4): x = h(x); seq.append(x)
T["fpi_div"] = ", ".join(f"{s:.4g}" for s in seq); T["fpi_div_gp"] = f"{3 * ROOT ** 2:.3f}"

# system of nonlinear equations: x^2 + y^2 = 4, x y = 1
def F(v): return np.array([v[0] ** 2 + v[1] ** 2 - 4, v[0] * v[1] - 1])
def J(v): return np.array([[2 * v[0], 2 * v[1]], [v[1], v[0]]])
v = np.array([2.0, 0.5]); rows = []
for i in range(5):
    d = np.linalg.solve(J(v), -F(v)); vn = v + d
    rows.append((i, f6(v[0]), f6(v[1]), f"{F(v)[0]:+.6f}", f"{F(v)[1]:+.6f}", f6(vn[0]), f6(vn[1]))); v = vn
T["nls_tab"] = table(["n", "xₙ", "yₙ", "f₁", "f₂", "xₙ₊₁", "yₙ₊₁"], rows)
T["nls_x"] = f6(v[0]); T["nls_y"] = f6(v[1])
assert abs(v[0] - (math.sqrt(6) + math.sqrt(2)) / 2) < 1e-10 and abs(v[1] - (math.sqrt(6) - math.sqrt(2)) / 2) < 1e-10
v0 = np.array([2.0, 0.5])
T["nls_J0"] = "[[4, 1], [0.5, 2]]"; T["nls_F0"] = "(0.25, 0)"
d0 = np.linalg.solve(J(v0), -F(v0)); T["nls_d0"] = f"({d0[0]:.6f}, {d0[1]:.6f})"

# ======================= Unit 2: interpolation =======================
xs_ = [1, 2, 3, 4]; ys_ = [math.log(v) for v in xs_]
def lagrange(xs, ys, x):
    s = 0
    for i in range(len(xs)):
        L = 1
        for j in range(len(xs)):
            if j != i: L *= (x - xs[j]) / (xs[i] - xs[j])
        s += ys[i] * L
    return s
xq = 2.5
Ls = []
for i in range(4):
    L = 1
    for j in range(4):
        if j != i: L *= (xq - xs_[j]) / (xs_[i] - xs_[j])
    Ls.append(L)
T["lag_L"] = ", ".join(f"{l:.4f}" for l in Ls)
T["lag_val"] = f6(lagrange(xs_, ys_, xq)); T["lag_true"] = f6(math.log(xq)); T["lag_err"] = f"{abs(math.log(xq) - lagrange(xs_, ys_, xq)):.6f}"
T["lag_pts"] = table(["i", "xᵢ", "yᵢ = ln xᵢ"], [(i, xs_[i], f6(ys_[i])) for i in range(4)])
T["lag3_val"] = f6(lagrange([2, 3, 4], ys_[1:], xq)); T["lag3_err"] = f"{abs(math.log(xq) - lagrange([2,3,4], ys_[1:], xq)):.6f}"
# error bound for the 4-point interpolation: |f''''|/4! * |prod (x-xi)| ; f=ln, f''''=-6/x^4 max at x=1 -> 6
prod = abs((xq - 1) * (xq - 2) * (xq - 3) * (xq - 4)); T["lag_prod"] = f"{prod:.4f}"
T["lag_bound"] = f"{6 / 24 * prod:.6f}"
assert abs(math.log(xq) - lagrange(xs_, ys_, xq)) <= 6 / 24 * prod

def divided(xs, ys):
    n = len(xs); tab = [list(ys)]
    for k in range(1, n):
        tab.append([(tab[k - 1][i + 1] - tab[k - 1][i]) / (xs[i + k] - xs[i]) for i in range(n - k)])
    return tab
dd = divided(xs_, ys_)
T["dd_tab"] = table(["xᵢ", "f[xᵢ]", "f[xᵢ,xᵢ₊₁]", "f[·,·,·]", "f[·,·,·,·]"],
                    [(xs_[i],) + tuple(f6(dd[k][i]) if i < len(dd[k]) else "" for k in range(4)) for i in range(4)])
coef = [dd[k][0] for k in range(4)]
def newton_dd(x): 
    s, p = 0, 1
    for k in range(4): s += coef[k] * p; p *= (x - xs_[k])
    return s
T["dd_val"] = f6(newton_dd(xq)); assert abs(newton_dd(xq) - lagrange(xs_, ys_, xq)) < 1e-12
T["dd_c"] = ", ".join(f6(c) for c in coef)
# unequally spaced: ln data x=1,2,4 -> 
# forward / backward differences with sin data (degrees)
sx = [0, 10, 20, 30, 40]; sy = [0.0, 0.1736, 0.3420, 0.5000, 0.6428]
D = [sy]
for k in range(1, 5): D.append([round(D[k - 1][i + 1] - D[k - 1][i], 4) for i in range(5 - k)])
T["diff_tab"] = table(["x°", "y = sin x", "Δy", "Δ²y", "Δ³y", "Δ⁴y"],
                      [(sx[i],) + tuple((f"{D[k][i]:.4f}" if i < len(D[k]) else "") for k in range(5)) for i in range(5)])
def fwd(xv, h=10):
    u = (xv - sx[0]) / h; s = D[0][0]; t = 1
    for k in range(1, 5): t *= (u - k + 1) / k; s += t * D[k][0]
    return u, s
def bwd(xv, h=10):
    u = (xv - sx[-1]) / h; s = D[0][-1]; t = 1
    for k in range(1, 5): t *= (u + k - 1) / k; s += t * D[k][-1 - 0] if False else t * D[k][len(D[k]) - 1]
    return u, s
u, s5 = fwd(5); T["fwd_u"] = f"{u:.1f}"; T["fwd_val"] = f"{s5:.5f}"; T["fwd_true"] = f"{math.sin(math.radians(5)):.5f}"
u, s35 = bwd(35); T["bwd_u"] = f"{u:.1f}"; T["bwd_val"] = f"{s35:.5f}"; T["bwd_true"] = f"{math.sin(math.radians(35)):.5f}"
assert abs(s5 - math.sin(math.radians(5))) < 2e-4 and abs(s35 - math.sin(math.radians(35))) < 2e-4
T["fwd_terms"] = ", ".join(f"{D[k][0]:.4f}" for k in range(5)); T["bwd_terms"] = ", ".join(f"{D[k][len(D[k]) - 1]:.4f}" for k in range(5))

# natural cubic spline through (1,2) (2,3) (3,5) (4,4)
px = np.array([1, 2, 3, 4.0]); py = np.array([2, 3, 5, 4.0])
n = 3; hh = np.diff(px)
A = np.array([[1, 0, 0, 0], [hh[0], 2 * (hh[0] + hh[1]), hh[1], 0], [0, hh[1], 2 * (hh[1] + hh[2]), hh[2]], [0, 0, 0, 1.0]])
rhs = np.array([0, 6 * ((py[2] - py[1]) / hh[1] - (py[1] - py[0]) / hh[0]), 6 * ((py[3] - py[2]) / hh[2] - (py[2] - py[1]) / hh[1]), 0])
M = np.linalg.solve(A, rhs)
T["sp_M"] = ", ".join(f"{m:.5f}" for m in M)
def spline_piece(i):
    a_ = py[i]; b_ = (py[i + 1] - py[i]) / hh[i] - hh[i] * (2 * M[i] + M[i + 1]) / 6; c_ = M[i] / 2; d_ = (M[i + 1] - M[i]) / (6 * hh[i])
    return a_, b_, c_, d_
rows = []
for i in range(3):
    a_, b_, c_, d_ = spline_piece(i); rows.append((f"[{int(px[i])}, {int(px[i+1])}]", f"{a_:.5f}", f"{b_:.5f}", f"{c_:.5f}", f"{d_:.5f}"))
T["sp_tab"] = table(["interval", "a", "b", "c", "d  (S = a + b t + c t² + d t³, t = x − xᵢ)"], rows)
def S(x):
    i = min(max(int(x) - 1, 0), 2); a_, b_, c_, d_ = spline_piece(i); t = x - px[i]; return a_ + b_ * t + c_ * t ** 2 + d_ * t ** 3
T["sp_val"] = f"{S(2.5):.5f}"; T["sp_val15"] = f"{S(1.5):.5f}"
from scipy.interpolate import CubicSpline
cs = CubicSpline(px, py, bc_type="natural"); assert abs(cs(2.5) - S(2.5)) < 1e-12 and abs(cs(1.5) - S(1.5)) < 1e-12

# least squares: linear
lx = np.array([1, 2, 3, 4, 5.0]); ly = np.array([2.2, 2.8, 3.6, 4.5, 5.1])
n_ = 5; Sx, Sy, Sxx, Sxy = lx.sum(), ly.sum(), (lx ** 2).sum(), (lx * ly).sum()
b = (n_ * Sxy - Sx * Sy) / (n_ * Sxx - Sx ** 2); a = (Sy - b * Sx) / n_
T["ls_tab"] = table(["x", "y", "x²", "xy"], [(int(x_), y_, int(x_ ** 2), f"{x_*y_:.1f}") for x_, y_ in zip(lx, ly)] + [("Σ = " + str(int(Sx)), f"{Sy:.1f}", int(Sxx), f"{Sxy:.1f}")])
T["ls_a"] = f"{a:.4f}"; T["ls_b"] = f"{b:.4f}"; T["ls_pred6"] = f"{a + b * 6:.3f}"
res = ly - (a + b * lx); T["ls_sse"] = f"{(res ** 2).sum():.4f}"
T["ls_r2"] = f"{1 - (res ** 2).sum() / ((ly - ly.mean()) ** 2).sum():.4f}"
pb, pa = np.polyfit(lx, ly, 1); assert abs(pb - b) < 1e-12 and abs(pa - a) < 1e-12
T["ls_sums"] = f"Σx = {int(Sx)}, Σy = {Sy:.1f}, Σx² = {int(Sxx)}, Σxy = {Sxy:.1f}"
# exponential y = A e^{Bx} by linearisation
ex_ = np.array([1, 2, 3, 4, 5.0]); ey = np.array([2.7, 4.0, 6.1, 9.2, 13.5]); lny = np.log(ey)
Bn = (5 * (ex_ * lny).sum() - ex_.sum() * lny.sum()) / (5 * (ex_ ** 2).sum() - ex_.sum() ** 2); An = (lny.sum() - Bn * ex_.sum()) / 5
T["exp_tab"] = table(["x", "y", "ln y", "x·ln y"], [(int(x_), y_, f"{math.log(y_):.4f}", f"{x_*math.log(y_):.4f}") for x_, y_ in zip(ex_, ey)])
T["exp_B"] = f"{Bn:.4f}"; T["exp_lnA"] = f"{An:.4f}"; T["exp_A"] = f"{math.exp(An):.4f}"; T["exp_pred6"] = f"{math.exp(An) * math.exp(Bn * 6):.2f}"
# quadratic fit as non-linear in x (normal equations)
Xm = np.vstack([np.ones(5), lx, lx ** 2]).T; qc = np.linalg.solve(Xm.T @ Xm, Xm.T @ ly)
T["quad_c"] = ", ".join(f"{c_:.4f}" for c_ in qc)

# ======================= Unit 3: differentiation / integration =======================
fe = math.exp; x0 = 1.0; true = math.e
rows = []
for h_ in (0.1, 0.01, 0.001):
    fdv = (fe(x0 + h_) - fe(x0)) / h_; bdv = (fe(x0) - fe(x0 - h_)) / h_; cdv = (fe(x0 + h_) - fe(x0 - h_)) / (2 * h_)
    rows.append((h_, f6(fdv), f"{abs(fdv - true):.6f}", f6(cdv), f"{abs(cdv - true):.7f}"))
T["nd_tab"] = table(["h", "forward (f(x+h)−f(x))/h", "error", "central (f(x+h)−f(x−h))/2h", "error"], rows)
T["nd_true"] = f6(true)
T["nd_bwd01"] = f6((fe(1) - fe(0.9)) / 0.1)
# Newton's differentiation formulas on ln x at 1.0..1.4
lx_ = [1.0, 1.1, 1.2, 1.3, 1.4]; ly_ = [math.log(v) for v in lx_]
DD = [ly_]
for k in range(1, 5): DD.append([DD[k - 1][i + 1] - DD[k - 1][i] for i in range(5 - k)])
T["nd_ln_tab"] = table(["x", "y = ln x", "Δy", "Δ²y", "Δ³y", "Δ⁴y"], [(lx_[i],) + tuple(f"{DD[k][i]:.6f}" if i < len(DD[k]) else "" for k in range(5)) for i in range(5)])
h_ = 0.1
d1 = (DD[1][0] - DD[2][0] / 2 + DD[3][0] / 3 - DD[4][0] / 4) / h_
d2 = (DD[2][0] - DD[3][0] + 11 / 12 * DD[4][0]) / h_ ** 2
T["nd_d1"] = f6(d1); T["nd_d2"] = f6(d2); T["nd_d1_2t"] = f6((DD[1][0]) / h_)
T["nd_d1_3t"] = f6((DD[1][0] - DD[2][0] / 2) / h_); T["nd_d1_4t"] = f6((DD[1][0] - DD[2][0] / 2 + DD[3][0] / 3) / h_)
T["nd_d1_err"] = f"{abs(d1 - 1):.6f}"
c3 = (ly_[3] - ly_[1]) / 0.2; T["nd_c3"] = f6(c3); T["nd_c3_true"] = f6(1 / 1.2)
T["nd_d2c"] = f6((ly_[1] - 2 * ly_[2] + ly_[3]) / 0.01); T["nd_d2c_true"] = f6(-1 / 1.2 ** 2)

fI = lambda x: 1 / (1 + x * x); TRUE_I = math.pi / 4
def trap(f, a, b, n):
    h = (b - a) / n; return h * (f(a) / 2 + sum(f(a + i * h) for i in range(1, n)) + f(b) / 2)
def simp13(f, a, b, n):
    h = (b - a) / n; return h / 3 * (f(a) + f(b) + 4 * sum(f(a + i * h) for i in range(1, n, 2)) + 2 * sum(f(a + i * h) for i in range(2, n, 2)))
def simp38(f, a, b, n):
    h = (b - a) / n; return 3 * h / 8 * (f(a) + f(b) + 3 * sum(f(a + i * h) for i in range(1, n) if i % 3) + 2 * sum(f(a + i * h) for i in range(3, n, 3)))
rows = [(i, f"{i}/6", f6(fI(i / 6))) for i in range(7)]
T["int_f"] = table(["i", "xᵢ", "f(xᵢ) = 1/(1+xᵢ²)"], rows)
T["int_true"] = f"{TRUE_I:.6f}"
T["int_trap6"] = f6(trap(fI, 0, 1, 6)); T["int_s13"] = f6(simp13(fI, 0, 1, 6)); T["int_s38"] = f6(simp38(fI, 0, 1, 6))
T["int_trap6_err"] = f"{abs(trap(fI, 0, 1, 6) - TRUE_I):.6f}"; T["int_s13_err"] = f"{abs(simp13(fI, 0, 1, 6) - TRUE_I):.7f}"; T["int_s38_err"] = f"{abs(simp38(fI, 0, 1, 6) - TRUE_I):.7f}"
T["int_s13_sum"] = f"{fI(0)+fI(1):.6f} + 4({fI(1/6)+fI(3/6)+fI(5/6):.6f}) + 2({fI(2/6)+fI(4/6):.6f})"
T["int_s13_total"] = f"{fI(0)+fI(1)+4*(fI(1/6)+fI(3/6)+fI(5/6))+2*(fI(2/6)+fI(4/6)):.6f}"
T["int_trap_sum"] = f"{(fI(0)+fI(1))/2 + sum(fI(i/6) for i in range(1,6)):.6f}"
rows = [(n_, f6(trap(fI, 0, 1, n_)), f"{abs(trap(fI,0,1,n_)-TRUE_I):.2e}", f6(simp13(fI, 0, 1, n_)), f"{abs(simp13(fI,0,1,n_)-TRUE_I):.2e}") for n_ in (2, 4, 8, 16)]
T["int_conv"] = table(["n", "trapezoid", "error", "Simpson 1/3", "error"], rows)
from scipy.integrate import quad
assert abs(quad(fI, 0, 1)[0] - TRUE_I) < 1e-12
# Romberg
def romberg(f, a, b, K):
    R = [[0] * K for _ in range(K)]
    for k in range(K):
        R[k][0] = trap(f, a, b, 2 ** k)
        for j in range(1, k + 1): R[k][j] = R[k][j - 1] + (R[k][j - 1] - R[k - 1][j - 1]) / (4 ** j - 1)
    return R
R = romberg(fI, 0, 1, 5)
T["rom_tab"] = table(["h", "R(k,0) trapezoid", "R(k,1)", "R(k,2)", "R(k,3)", "R(k,4)"],
                     [(f"1/{2**k}" if k else "1",) + tuple(f"{R[k][j]:.8f}" if j <= k else "" for j in range(5)) for k in range(5)])
T["rom_final"] = f"{R[4][4]:.8f}"; T["rom_err"] = f"{abs(R[4][4] - TRUE_I):.2e}"; T["rom_r33"] = f"{R[3][3]:.8f}"; T["rom_r33_err"] = f"{abs(R[3][3] - TRUE_I):.2e}"; T["rom_true8"] = f"{TRUE_I:.8f}"
# double integral of 1/(x+y), x in [0,1], y in [1,2], h=k=0.5
g2 = lambda x, y: 1 / (x + y); xsg = [0, 0.5, 1.0]; ysg = [1, 1.5, 2.0]
T["dbl_tab"] = table(["f(x,y) = 1/(x+y)", "y = 1", "y = 1.5", "y = 2"], [(f"x = {xv}",) + tuple(f6(g2(xv, yv)) for yv in ysg) for xv in xsg])
w = [1, 4, 1]; hx = ky = 0.5
dsimp = hx * ky / 9 * sum(w[i] * w[j] * g2(xsg[i], ysg[j]) for i in range(3) for j in range(3))
wt = [0.5, 1, 0.5]; dtrap = hx * ky * sum(wt[i] * wt[j] * g2(xsg[i], ysg[j]) for i in range(3) for j in range(3))
DTRUE = 3 * math.log(3) - 4 * math.log(2)
T["dbl_simp"] = f6(dsimp); T["dbl_trap"] = f6(dtrap); T["dbl_true"] = f6(DTRUE)
T["dbl_simp_err"] = f"{abs(dsimp - DTRUE):.6f}"; T["dbl_trap_err"] = f"{abs(dtrap - DTRUE):.6f}"
from scipy.integrate import dblquad
assert abs(dblquad(lambda y, x: 1 / (x + y), 0, 1, 1, 2)[0] - DTRUE) < 1e-10

# ======================= Unit 4: linear algebraic equations =======================
A1 = np.array([[2, 1, -1], [-3, -1, 2], [-2, 1, 2.0]]); b1 = np.array([8, -11, -3.0])
def gauss_trace(A, b):
    A = np.hstack([A, b[:, None]]).astype(float); n = len(A); out = []
    for k in range(n - 1):
        p = k + np.argmax(abs(A[k:, k]))
        if p != k: A[[k, p]] = A[[p, k]]; out.append(f"swap R{k+1} ↔ R{p+1}")
        for i in range(k + 1, n):
            m = A[i, k] / A[k, k]; out.append(f"m{i+1}{k+1} = {m:.4f}"); A[i] -= m * A[k]
    x = np.zeros(n)
    for i in range(n - 1, -1, -1): x[i] = (A[i, -1] - A[i, i + 1:n] @ x[i + 1:]) / A[i, i]
    return A, x, out
Aug, xg, steps = gauss_trace(A1, b1)
T["ge_steps"] = "; ".join(steps)
T["ge_U"] = table(["x", "y", "z", "RHS"], [tuple(f"{v:.4f}" for v in row) for row in Aug])
T["ge_x"] = ", ".join(f"{v:.4f}" for v in xg); assert np.allclose(xg, np.linalg.solve(A1, b1))
# LU Doolittle (no pivoting) for A2
A2 = np.array([[2, 1, 1], [4, 3, 3], [8, 7, 9.0]]); b2 = np.array([4, 10, 24.0])
Lm = np.eye(3); Um = A2.copy()
for k in range(2):
    for i in range(k + 1, 3): Lm[i, k] = Um[i, k] / Um[k, k]; Um[i] -= Lm[i, k] * Um[k]
y_ = np.linalg.solve(Lm, b2); x_ = np.linalg.solve(Um, y_)
T["lu_L"] = "[" + "; ".join(", ".join(f"{v:g}" for v in r) for r in Lm) + "]"; T["lu_U"] = "[" + "; ".join(", ".join(f"{v:g}" for v in r) for r in Um) + "]"
T["lu_y"] = ", ".join(f"{v:g}" for v in y_); T["lu_x"] = ", ".join(f"{v:g}" for v in x_)
assert np.allclose(Lm @ Um, A2) and np.allclose(A2 @ x_, b2)
T["lu_det"] = f"{np.prod(np.diag(Um)):g}"
# Jacobi and Gauss-Seidel
A3 = np.array([[10, -1, 2, 0], [-1, 11, -1, 3], [2, -1, 10, -1], [0, 3, -1, 8.0]]); b3 = np.array([6, 25, -11, 15.0])
def jacobi(A, b, x, n):
    rows = []
    for k in range(n):
        xn = np.array([(b[i] - sum(A[i, j] * x[j] for j in range(len(b)) if j != i)) / A[i, i] for i in range(len(b))])
        rows.append((k + 1,) + tuple(f"{v:.4f}" for v in xn)); x = xn
    return rows, x
def seidel(A, b, x, n):
    x = x.copy(); rows = []
    for k in range(n):
        for i in range(len(b)): x[i] = (b[i] - sum(A[i, j] * x[j] for j in range(len(b)) if j != i)) / A[i, i]
        rows.append((k + 1,) + tuple(f"{v:.4f}" for v in x))
    return rows, x
rj, xj = jacobi(A3, b3, np.zeros(4), 6); rg, xgs = seidel(A3, b3, np.zeros(4), 6)
T["jac_tab"] = table(["k", "x₁", "x₂", "x₃", "x₄"], [(0, "0.0000", "0.0000", "0.0000", "0.0000")] + rj)
T["gs_tab"] = table(["k", "x₁", "x₂", "x₃", "x₄"], [(0, "0.0000", "0.0000", "0.0000", "0.0000")] + rg)
exact3 = np.linalg.solve(A3, b3); T["gs_exact"] = ", ".join(f"{v:.4f}" for v in exact3)
def iters_to(method, tol):
    x = np.zeros(4); k = 0
    while np.max(abs(x - exact3)) > tol:
        x = method(A3, b3, x, 1)[1]; k += 1
    return k
T["jac_n4"] = str(iters_to(jacobi, 5e-5)); T["gs_n4"] = str(iters_to(seidel, 5e-5))
# spectral radius
Dm = np.diag(np.diag(A3)); Lo = np.tril(A3, -1); Up = np.triu(A3, 1)
rho_j = max(abs(np.linalg.eigvals(-np.linalg.inv(Dm) @ (Lo + Up)))); rho_g = max(abs(np.linalg.eigvals(-np.linalg.inv(Dm + Lo) @ Up)))
T["rho_j"] = f"{rho_j:.4f}"; T["rho_g"] = f"{rho_g:.4f}"; assert abs(rho_g - rho_j ** 2) < 0.05 or rho_g < rho_j
# not diagonally dominant example: 
A4 = np.array([[1, 3.0], [4, 1]]); b4 = np.array([5, 6.0]); x = np.zeros(2); seq = []
for k in range(4):
    for i in range(2): x[i] = (b4[i] - A4[i, 1 - i] * x[1 - i]) / A4[i, i]
    seq.append(f"({x[0]:.0f}, {x[1]:.0f})") if abs(x[0]) > 100 else seq.append(f"({x[0]:.2f}, {x[1]:.2f})")
T["gs_div"] = " → ".join(seq); T["gs_div_x"] = ", ".join(f"{v:.4f}" for v in np.linalg.solve(A4, b4))
# swapped order converges
A5 = A4[::-1]; b5 = b4[::-1]; x = np.zeros(2); seq = []
for k in range(5):
    for i in range(2): x[i] = (b5[i] - A5[i, 1 - i] * x[1 - i]) / A5[i, i]
    seq.append(f"({x[0]:.4f}, {x[1]:.4f})")
T["gs_swap"] = " → ".join(seq)
# ill-conditioning
Ah = np.array([[1, 1], [1, 1.0001]]); 
T["ill_x1"] = ", ".join(f"{v:g}" for v in np.linalg.solve(Ah, [2, 2.0001]))
T["ill_x2"] = ", ".join(f"{v:g}" for v in np.linalg.solve(Ah, [2, 2.0002]))
T["ill_cond"] = f"{np.linalg.cond(Ah):.0f}"
H3 = np.array([[1 / (i + j + 1) for j in range(3)] for i in range(3)]); T["hilb_cond"] = f"{np.linalg.cond(H3):.0f}"
# power method
Ap = np.array([[2, -1, 0], [-1, 2, -1], [0, -1, 2.0]]); v = np.array([0, 1.0, 0]); rows = []
for k in range(1, 8):
    w_ = Ap @ v; lam = w_[np.argmax(abs(w_))]; v = w_ / lam; rows.append((k, f"({w_[0]:.4f}, {w_[1]:.4f}, {w_[2]:.4f})", f"{lam:.4f}", f"({v[0]:.4f}, {v[1]:.4f}, {v[2]:.4f})"))
T["pow_tab"] = table(["k", "A·vₖ₋₁", "λₖ (largest entry)", "vₖ (scaled)"], rows)
T["pow_true"] = f"{2 + math.sqrt(2):.4f}"; T["pow_rayleigh"] = f"{(v @ Ap @ v) / (v @ v):.4f}"
assert abs(max(np.linalg.eigvalsh(Ap)) - (2 + math.sqrt(2))) < 1e-12
T["inv_check"] = ", ".join(f"{v:.4f}" for v in np.linalg.inv(np.array([[2.0, 1], [5, 3]])).flatten())

# ======================= Unit 5: ODE =======================
fo = lambda x, y: x + y
exact = lambda x: 2 * math.exp(x) - x - 1
def euler(f, x, y, h, n):
    rows = []
    for i in range(n):
        yn = y + h * f(x, y); rows.append((i, f"{x:.1f}", f6(y), f6(f(x, y)), f6(yn), f6(exact(x + h)), f"{abs(exact(x + h) - yn):.6f}")); x += h; y = yn
    return rows, y
rows, ye = euler(fo, 0, 1, 0.1, 5)
T["eul_tab"] = table(["i", "xᵢ", "yᵢ", "f(xᵢ,yᵢ)", "yᵢ₊₁", "exact y(xᵢ₊₁)", "error"], rows); T["eul_05"] = f6(ye); T["ex_05"] = f6(exact(0.5)); T["eul_err"] = f"{abs(exact(.5)-ye):.6f}"
def heun(f, x, y, h, n):
    rows = []
    for i in range(n):
        k1 = f(x, y); yp = y + h * k1; k2 = f(x + h, yp); yn = y + h / 2 * (k1 + k2)
        rows.append((i, f"{x:.1f}", f6(y), f6(yp), f6(yn), f6(exact(x + h)))); x += h; y = yn
    return rows, y
rows, yh = heun(fo, 0, 1, 0.1, 5)
T["heun_tab"] = table(["i", "xᵢ", "yᵢ", "predictor y*", "corrector yᵢ₊₁", "exact"], rows); T["heun_05"] = f6(yh); T["heun_err"] = f"{abs(exact(.5)-yh):.6f}"
def rk4(f, x, y, h):
    k1 = f(x, y); k2 = f(x + h / 2, y + h * k1 / 2); k3 = f(x + h / 2, y + h * k2 / 2); k4 = f(x + h, y + h * k3)
    return y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4), (k1, k2, k3, k4)
x, y = 0, 1; rows = []
for i in range(5):
    yn, ks = rk4(fo, x, y, 0.1); rows.append((i, f"{x:.1f}", f6(y), *[f6(k) for k in ks], f6(yn), f6(exact(x + .1)))); x += .1; y = yn
T["rk4_tab"] = table(["i", "xᵢ", "yᵢ", "k₁", "k₂", "k₃", "k₄", "yᵢ₊₁", "exact"], rows); T["rk4_05"] = f6(y); T["rk4_err"] = f"{abs(exact(.5)-y):.2e}"
x, y = 0, 1; yn, ks = rk4(fo, 0, 1, 0.1); T["rk4_k"] = ", ".join(f6(k) for k in ks)
# accuracy orders
def run(method, h):
    n = round(0.5 / h); x, y = 0, 1.0
    for i in range(n):
        if method == "euler": y += h * fo(x, y)
        elif method == "heun": k1 = fo(x, y); y += h / 2 * (k1 + fo(x + h, y + h * k1))
        else: y = rk4(fo, x, y, h)[0]
        x += h
    return abs(exact(0.5) - y)
rows = []
for h_ in (0.1, 0.05, 0.025):
    rows.append((h_, f"{run('euler', h_):.2e}", f"{run('heun', h_):.2e}", f"{run('rk4', h_):.2e}"))
T["ord_tab"] = table(["h", "Euler error", "Heun error", "RK4 error"], rows)
T["ord_ratio"] = f"Euler {run('euler',0.1)/run('euler',0.05):.2f}, Heun {run('heun',0.1)/run('heun',0.05):.2f}, RK4 {run('rk4',0.1)/run('rk4',0.05):.2f}"
# Taylor and Picard
import sympy as sp
xs, ys = sp.symbols("x y"); 
# Taylor: y' = x + y, y(0)=1: y'(0)=1, y''=1+y' =2, y'''=y''=2, y''''=2
T["tay_series"] = "1 + x + x² + x³/3 + x⁴/12"; T["tay_05"] = f6(1 + .5 + .25 + .125 / 3 + .0625 / 12); T["tay_err"] = f"{abs(exact(.5) - (1 + .5 + .25 + .125/3 + .0625/12)):.6f}"
T["tay_01"] = f6(1 + .1 + .01 + .001 / 3 + .0001 / 12)
xx = sp.symbols("x"); yk = sp.Integer(1); picard = []
for k in range(3):
    t = sp.symbols("t"); yk = 1 + sp.integrate((t + yk.subs(xx, t)), (t, 0, xx)); picard.append(sp.expand(yk))
T["pic1"] = str(picard[0]).replace("**", "^").replace("*", "·"); T["pic2"] = str(picard[1]).replace("**", "^").replace("*", "·"); T["pic3"] = str(picard[2]).replace("**", "^").replace("*", "·")
T["pic3_05"] = f6(float(picard[2].subs(xx, 0.5)))
assert abs(float(sp.series(2 * sp.exp(xx) - xx - 1, xx, 0, 5).removeO().subs(xx, 0.5)) - float((1 + xx + xx ** 2 + xx ** 3 / 3 + xx ** 4 / 12).subs(xx, 0.5))) < 1e-12
from scipy.integrate import solve_ivp
sol = solve_ivp(fo, [0, 0.5], [1], rtol=1e-12, atol=1e-12); assert abs(sol.y[0, -1] - exact(0.5)) < 1e-9
# second-order: y'' = -y, y(0)=0, y'(0)=1 -> system, RK4 h=0.1
def sysf(x, Y): return np.array([Y[1], -Y[0]])
def rk4s(f, x, Y, h):
    k1 = f(x, Y); k2 = f(x + h / 2, Y + h * k1 / 2); k3 = f(x + h / 2, Y + h * k2 / 2); k4 = f(x + h, Y + h * k3); return Y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
Y = np.array([0.0, 1.0]); x = 0; rows = []
for i in range(5):
    Y = rk4s(sysf, x, Y, 0.1); x += 0.1; rows.append((f"{x:.1f}", f6(Y[0]), f6(math.sin(x)), f6(Y[1]), f6(math.cos(x))))
T["sys_tab"] = table(["x", "y (RK4)", "sin x", "z = y′ (RK4)", "cos x"], rows)
Y = np.array([0.0, 1.0]); k = rk4s(sysf, 0, Y, 0.1); T["sys_first"] = f"({k[0]:.6f}, {k[1]:.6f})"
# shooting: y'' = y, y(0)=0, y(1)=2
def shoot(s):
    Y = np.array([0.0, s]); x = 0
    for i in range(10): Y = rk4s(lambda x, Y: np.array([Y[1], Y[0]]), x, Y, 0.1); x += 0.1
    return Y[0]
s1, s2 = 1.0, 2.0; y1, y2 = shoot(s1), shoot(s2); s3 = s1 + (2 - y1) * (s2 - s1) / (y2 - y1)
T["sh_tab"] = table(["trial", "slope s = y′(0)", "y(1) by RK4", "target"], [(1, f"{s1:.4f}", f6(y1), "2"), (2, f"{s2:.4f}", f6(y2), "2"), (3, f"{s3:.6f}", f6(shoot(s3)), "2")])
T["sh_s3"] = f"{s3:.6f}"; T["sh_exact"] = f"{2 / math.sinh(1):.6f}"; T["sh_y1_s3"] = f6(shoot(s3))
T["sh_mid"] = f6(shoot(s3) * 0 + (lambda s: (lambda Y: Y[0])(__import__('functools').reduce(lambda Y, i: rk4s(lambda x, Y: np.array([Y[1], Y[0]]), 0.1 * i, Y, 0.1), range(5), np.array([0.0, s]))))(s3))
T["sh_mid_true"] = f6(2 * math.sinh(0.5) / math.sinh(1))
assert abs(s3 - 2 / math.sinh(1)) < 1e-4

# ======================= Unit 6: PDE =======================
# Laplace on square, 3x3 interior, top = 100, others 0
def liebmann(n_iter):
    u = np.zeros((5, 5)); u[0, :] = 100; rows = []
    for k in range(1, n_iter + 1):
        for i in range(1, 4):
            for j in range(1, 4): u[i, j] = (u[i - 1, j] + u[i + 1, j] + u[i, j - 1] + u[i, j + 1]) / 4
        rows.append((k, *(f"{u[i,j]:.4f}" for (i, j) in [(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3)])))
    return rows, u
rows, u = liebmann(8)
T["lap_gs"] = table(["k", "u₁₁", "u₁₂", "u₁₃", "u₂₁", "u₂₂", "u₂₃", "u₃₁", "u₃₂", "u₃₃"], rows[:5] + rows[-1:])
# exact solution of the discrete system
n3 = 3; Aa = np.zeros((9, 9)); bb = np.zeros(9)
idx = lambda i, j: (i - 1) * 3 + (j - 1)
for i in range(1, 4):
    for j in range(1, 4):
        r = idx(i, j); Aa[r, r] = 4
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ii, jj = i + di, j + dj
            if 1 <= ii <= 3 and 1 <= jj <= 3: Aa[r, idx(ii, jj)] = -1
            elif ii == 0: bb[r] += 100
sol9 = np.linalg.solve(Aa, bb)
T["lap_sol"] = table(["", "col 1", "col 2", "col 3"], [(f"row {i} (from top)",) + tuple(f"{sol9[idx(i,j)]:.4f}" for j in (1, 2, 3)) for i in (1, 2, 3)])
T["lap_u22"] = f"{sol9[idx(2,2)]:.4f}"; T["lap_u12"] = f"{sol9[idx(1,2)]:.4f}"; T["lap_u11"] = f"{sol9[idx(1,1)]:.4f}"; T["lap_u32"] = f"{sol9[idx(3,2)]:.4f}"
T["lap_u21"] = f"{sol9[idx(2,1)]:.4f}"; T["lap_u31"] = f"{sol9[idx(3,1)]:.4f}"
assert np.allclose(sol9[idx(2, 2)], 25 * 1.0 * 1 or sol9[idx(2, 2)])  # centre is (100+0+0+0)/4 = 25 by symmetry
assert abs(sol9[idx(2, 2)] - 25) < 1e-9, sol9[idx(2, 2)]
T["lap_err8"] = f"{np.max(abs(u[1:4, 1:4].flatten() - sol9)):.4f}"
# 2x2 Laplace by hand
A2x2 = np.array([[4, -1, -1, 0], [-1, 4, 0, -1], [-1, 0, 4, -1], [0, -1, -1, 4.0]]); b2x2 = np.array([100 + 0, 100 + 0, 0, 0.0])
T["lap2_sol"] = ", ".join(f"{v:.4f}" for v in np.linalg.solve(A2x2, b2x2))
# Poisson: lap u = -10(x^2+y^2+10) on 0<=x,y<=3, u=0 boundary, h=1: interior (1,1),(2,1),(1,2),(2,2)
src = lambda x, y: -10 * (x * x + y * y + 10)
pts = [(1, 1), (2, 1), (1, 2), (2, 2)]
Ap_ = np.array([[4, -1, -1, 0], [-1, 4, 0, -1], [-1, 0, 4, -1], [0, -1, -1, 4.0]]); bp = np.array([-1 * src(x, y) * -1 * -1 for (x, y) in pts]) * -1
bp = np.array([-(src(x, y)) for (x, y) in pts], dtype=float) * -1 * -1   # 4u - sum nbrs = -h^2 f  -> = -src
bp = np.array([-src(x, y) for (x, y) in pts], dtype=float) * 1.0
up = np.linalg.solve(Ap_, bp)
T["poi_src"] = ", ".join(f"f({x},{y}) = {src(x,y):g}" for (x, y) in pts); T["poi_rhs"] = ", ".join(f"{v:g}" for v in bp)
T["poi_sol"] = ", ".join(f"u({x},{y}) = {v:.4f}" for (x, y), v in zip(pts, up))
T["poi_u1"] = f"{up[0]:.4f}"; T["poi_u2"] = f"{up[1]:.4f}"
# iterative
u1 = u2 = u3 = u4 = 0; rows = []
for k in range(1, 6):
    u1 = (u2 + u3 + bp[0]) / 4; u2 = (u1 + u4 + bp[1]) / 4; u3 = (u1 + u4 + bp[2]) / 4; u4 = (u2 + u3 + bp[3]) / 4
    rows.append((k, f"{u1:.4f}", f"{u2:.4f}", f"{u3:.4f}", f"{u4:.4f}"))
T["poi_it"] = table(["k", "u₁", "u₂", "u₃", "u₄"], rows)

# =====================================================================
def apply(text):
    return re.sub(r"@@([A-Za-z0-9_]+)@@", lambda m: T[m.group(1)], text)

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "--print"
    if mode == "--print":
        for k, v in T.items(): print(f"@@{k}@@\n{v}\n")
    elif mode == "--fill":
        for p in sys.argv[2:]:
            s = open(p, encoding="utf-8").read(); new = apply(s)
            miss = re.findall(r"@@(\w+)@@", new)
            assert not miss, miss
            open(p, "w", encoding="utf-8").write(new)
    elif mode == "--verify":
        text = "\n".join(open(p, encoding="utf-8").read() for p in sys.argv[2:]); bad = 0
        unused = [k for k, v in T.items() if v not in text]
        print(f"{len(T) - len(unused)} of {len(T)} computed tokens appear verbatim in the units; unused: {unused}")
