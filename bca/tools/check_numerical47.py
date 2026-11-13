#!/usr/bin/env python3
"""BCA 253 Numerical Methods, session 47: every number in the NEW sections (1.10-1.14, 2.9-2.12, ...) is computed here.
    python3 bca/tools/check_numerical47.py [u1|u2|u3|u4|u5|u6]   # prints values; asserts cross-checks"""
import math, sys, decimal
import numpy as np
which = sys.argv[1:] or ["u1", "u2", "u3", "u4", "u5", "u6"]

def u1():
    print("== u1")
    import sys as s
    print("eps", s.float_info.epsilon, "0.1+0.2", repr(0.1 + 0.2), "(1+1e-16)-1", (1 + 1e-16) - 1, "1+2^-53==1", 1 + 2**-53 == 1, "1+2^-52", 1 + 2**-52 > 1)
    print("float32 eps", float(np.finfo(np.float32).eps), "max", s.float_info.max, "min", s.float_info.min)
    r, h, dr, dh = 2.50, 10.0, 0.02, 0.1
    V = math.pi * r * r * h; rel = 2 * dr / r + dh / h
    print("V", V, "rel", rel, "dV", V * rel, "bounds", V - V * rel, V + V * rel)
    # quadratic cancellation, 5 significant digits
    from decimal import Decimal as D, getcontext
    getcontext().prec = 5
    b, c = D(1000), D(1)
    disc = (b * b - 4 * c).sqrt()
    naive = (b - disc) / 2; stable = (2 * c) / (b + disc)
    getcontext().prec = 30
    exact = (D(1000) - (D(1000) ** 2 - 4).sqrt()) / 2
    print("disc", disc, "naive", naive, "stable", stable, "exact", exact)
    # Aitken / Steffensen on g(x)=(x+2)^(1/3)
    g = lambda x: (x + 2) ** (1 / 3)
    x0 = 1.5; x1 = g(x0); x2 = g(x1); x3 = g(x2); x4 = g(x3)
    print("fp", x0, x1, x2, x3, x4)
    ait = lambda a, b, c: a - (b - a) ** 2 / (c - 2 * b + a)
    print("aitken(x0,x1,x2)", ait(x0, x1, x2), "aitken(x1,x2,x3)", ait(x1, x2, x3))
    x = 1.5; print("steffensen")
    R = 1.5213797068045676
    for n in range(2):
        a = g(x); b2 = g(a); xn = ait(x, a, b2)
        print(n, f"{x:.8f} {a:.8f} {b2:.8f} -> {xn:.10f} err {abs(xn - R):.2e}")
        x = xn
    # multiple root
    f = lambda x: x**3 - 3 * x + 2; fp = lambda x: 3 * x * x - 3
    x = 2.0; print("newton double root")
    for n in range(8):
        xn = x - f(x) / fp(x); print(n, f"{x:.8f} {f(x):.3e} {fp(x):.4f} {xn:.8f} err {abs(xn - 1):.3e}"); x = xn
    x = 2.0; print("modified m=2")
    for n in range(5):
        xn = x - 2 * f(x) / fp(x); print(n, f"{x:.8f} {xn:.10f} err {abs(xn - 1):.3e}"); x = xn
    # u = f/f'
    fpp = lambda x: 6 * x
    x = 2.0; print("u=f/f' method")
    for n in range(5):
        u = f(x) / fp(x); up = 1 - f(x) * fpp(x) / fp(x) ** 2; xn = x - u / up
        print(n, f"{x:.8f} {xn:.10f} err {abs(xn - 1):.3e}"); x = xn
    # Muller
    h3 = lambda x: x**3 - x - 2
    a, b, c = 1.0, 1.5, 2.0; print("muller")
    for n in range(4):
        h1, h2 = b - a, c - b
        d1, d2 = (h3(b) - h3(a)) / h1, (h3(c) - h3(b)) / h2
        A = (d2 - d1) / (h2 + h1); B = A * h2 + d2; C = h3(c)
        sq = math.sqrt(B * B - 4 * A * C)
        den = B + sq if abs(B + sq) > abs(B - sq) else B - sq
        xn = c - 2 * C / den
        print(n, f"x0={a:.6f} x1={b:.6f} x2={c:.6f} A={A:.6f} B={B:.6f} C={C:.6f} x3={xn:.8f} err {abs(xn - R):.2e}")
        a, b, c = b, c, xn
    # Horner
    p = [1, -6, 11, -6]
    def horner(p, x):
        b = [p[0]]
        for co in p[1:]: b.append(co + x * b[-1])
        return b
    print("horner p(x)=2x3-6x2+2x-1 at 3:", horner([2, -6, 2, -1], 3))
    bb = horner(p, 0.5); print("horner x^3-6x^2+11x-6 at .5", bb)
    x = 0.5; print("newton-horner")
    for n in range(6):
        b_ = horner(p, x); c_ = horner(b_[:-1], x)
        xn = x - b_[-1] / c_[-1]
        print(n, f"{x:.8f} p={b_[-1]:.6f} p'={c_[-1]:.6f} -> {xn:.8f}"); x = xn
    print("deflation by 1:", horner(p, 1.0), " by 3 first:", horner(p, 3.0))
    print("quad roots x^2-5x+6:", np.roots([1, -5, 6]))
    # Wilkinson-like sensitivity: (x-1)(x-2)(x-3)(x-4)(x-5)(x-6) perturb x^5 coefficient
    co = np.poly(np.arange(1, 7)); print("poly6", co)
    co2 = co.copy(); co2[1] -= 1e-4
    print("perturbed roots", np.roots(co2))
    co = np.poly(np.arange(1, 21)); co2 = co.copy(); co2[1] -= 2**-23
    print("wilk20 max imag", np.abs(np.roots(co2).imag).max())
    # order of convergence estimate for Newton on x^3-x-2
    x = 3.0; es = []
    for n in range(7):
        x = x - h3(x) / (3 * x * x - 1); es.append(abs(x - R))
    print("newton errs", es)
    ps = [math.log(es[i + 1] / es[i]) / math.log(es[i] / es[i - 1]) for i in range(1, 4)]
    print("p est", ps)

def u2():
    print("== u2")
    # Neville: cos at x=0.8 from nodes 0,0.5,1.0,1.5
    xs = [0.0, 0.5, 1.0, 1.5]; ys = [math.cos(x) for x in xs]; x = 0.8
    print("cos nodes", ys)
    P = [ys[:]]
    for k in range(1, 4):
        P.append([((x - xs[i]) * P[k-1][i+1] - (x - xs[i+k]) * P[k-1][i]) / (xs[i+k] - xs[i]) for i in range(4 - k)])
    for r in P: print([f"{v:.6f}" for v in r])
    print("true", math.cos(0.8), "err", abs(P[3][0] - math.cos(0.8)))
    # inverse interpolation: f(x)=x^3-x-2 at 1.0,1.2,1.4,1.6; find x with f=0 ; Lagrange in y
    X = [1.0, 1.2, 1.4, 1.6]; Y = [x**3 - x - 2 for x in X]; print("Y", Y)
    def lag(xs_, ys_, t):
        s = 0
        for i in range(len(xs_)):
            L = 1
            for j in range(len(xs_)):
                if j != i: L *= (t - xs_[j]) / (xs_[i] - xs_[j])
            s += ys_[i] * L
        return s
    print("inverse", lag(Y, X, 0.0), "true", 1.5213797068, "using 3 pts (1.2,1.4,1.6):", lag(Y[1:], X[1:], 0.0))
    # Runge: equispaced vs Chebyshev
    f = lambda x: 1 / (1 + 25 * x * x)
    grid = np.linspace(-1, 1, 2001)
    for n in (5, 9, 13):
        xe = np.linspace(-1, 1, n + 1); xc = np.cos((2 * np.arange(n + 1) + 1) * np.pi / (2 * (n + 1)))
        ee = max(abs(lag(xe, f(xe), t) - f(t)) for t in grid[::10]); ec = max(abs(lag(xc, f(xc), t) - f(t)) for t in grid[::10])
        print("n", n, "equi", ee, "cheb", ec)
    n = 4; print("cheb nodes n=4 on [-1,1]:", np.cos((2 * np.arange(5) + 1) * np.pi / 10))
    # error bound example: sin x on [0, pi/2] with nodes 0, pi/4, pi/2 at x=pi/8? bound
    # Stirling: sin at x0=30 deg table step 10? use f=e^x table x=0.5..1.5 step 0.25? central at 1.0
    # difference table with typo detection: y = x^3 at 0..7 with one wrong value
    ys = [0, 1, 8, 27, 74, 125, 216, 343]  # 64 replaced by 74
    d = [ys]
    for k in range(5): d.append([d[-1][i+1] - d[-1][i] for i in range(len(d[-1]) - 1)])
    for r in d: print(r)
    ys2 = [x**3 for x in range(8)]; d2 = [ys2]
    for k in range(4): d2.append([d2[-1][i+1] - d2[-1][i] for i in range(len(d2[-1]) - 1)])
    for r in d2: print(r)
    # Stirling at x=1.0 table e^x step .25? compute f(1.1) with h=0.1 table at 0.8..1.2
    xs = [0.8, 0.9, 1.0, 1.1, 1.2]; ys = [math.exp(x) for x in xs]
    print("e^x", ys); 
    # stirling: x0=1.0, p=(x-x0)/h. we estimate e^1.04
    h = 0.1; p = 0.4
    d1 = [ys[i+1] - ys[i] for i in range(4)]; d2_ = [d1[i+1] - d1[i] for i in range(3)]; d3 = [d2_[i+1] - d2_[i] for i in range(2)]; d4 = d3[1] - d3[0]
    print("d1", d1, "d2", d2_, "d3", d3, "d4", d4)
    st = ys[2] + p * (d1[1] + d1[2]) / 2 + p**2 / 2 * d2_[1] + p * (p**2 - 1) / 6 * (d3[0] + d3[1]) / 2 + p**2 * (p**2 - 1) / 24 * d4
    print("stirling e^1.04", st, "true", math.exp(1.04), "err", abs(st - math.exp(1.04)))
    st3 = ys[2] + p * (d1[1] + d1[2]) / 2 + p**2 / 2 * d2_[1]
    print("stirling 2nd order", st3)
    # least squares: R^2 for data of Q2 in unit 2
    X = np.array([1, 2, 3, 4, 5.]); Yv = np.array([2.1, 3.9, 6.2, 7.8, 10.1])
    A = np.vstack([np.ones(5), X]).T; coef = np.linalg.lstsq(A, Yv, rcond=None)[0]
    res = Yv - A @ coef; SSE = (res**2).sum(); SST = ((Yv - Yv.mean())**2).sum()
    print("coef", coef, "res", res, "SSE", SSE, "SST", SST, "R2", 1 - SSE / SST, "se", math.sqrt(SSE / 3))
    # outlier
    Y2 = Yv.copy(); Y2[4] = 5.0; c2 = np.linalg.lstsq(A, Y2, rcond=None)[0]; print("with outlier", c2)
    # weighted LS: weights 1,1,1,1,0.1 for last
    W = np.diag([1, 1, 1, 1, 0.1]); cw = np.linalg.solve(A.T @ W @ A, A.T @ W @ Y2); print("weighted", cw)
    # Hilbert/normal-equation conditioning: monomial fit degree m on x=1..10
    xx = np.arange(1, 11.0)
    for m in (1, 2, 4, 6):
        V = np.vander(xx, m + 1); print("deg", m, "cond(V)", np.linalg.cond(V), "cond(V^T V)", np.linalg.cond(V.T @ V))
    print("hilbert 5 cond", np.linalg.cond(np.array([[1/(i+j+1) for j in range(5)] for i in range(5)])))
    # piecewise comparisons: sin x on [0,pi], 5 nodes (h=pi/4): linear, natural spline, clamped spline errors
    from scipy.interpolate import CubicSpline
    xn = np.linspace(0, math.pi, 5); yn = np.sin(xn); tt = np.linspace(0, math.pi, 1001)
    lin = np.interp(tt, xn, yn); nat = CubicSpline(xn, yn, bc_type="natural")(tt); cla = CubicSpline(xn, yn, bc_type=((1, 1.0), (1, -1.0)))(tt)
    poly = np.array([lag(xn, yn, t) for t in tt])
    for nm, v in (("linear", lin), ("natural", nat), ("clamped", cla), ("poly4", poly)): print(nm, abs(v - np.sin(tt)).max())
    print("at 1.0: sin", math.sin(1.0), "lin", np.interp(1.0, xn, yn), "nat", CubicSpline(xn, yn, bc_type="natural")(1.0), "cla", CubicSpline(xn, yn, bc_type=((1, 1.0), (1, -1.0)))(1.0))
    # interpolation error bound: sin on nodes 0, pi/4, pi/2, at x = pi/8
    xk = [0, math.pi / 4, math.pi / 2]; t = math.pi / 8
    w = 1
    for xi in xk: w *= (t - xi)
    print("w", w, "bound", abs(w) / 6, "actual err", abs(lag(xk, [math.sin(v) for v in xk], t) - math.sin(t)))

def u3():
    print("== u3")
    # derivative of e^x at 1, forward vs central vs h
    print("h  forward  central  err_f  err_c")
    ex = math.e
    for k in range(1, 17):
        h = 10.0**-k
        fw = (math.exp(1 + h) - math.exp(1)) / h; ce = (math.exp(1 + h) - math.exp(1 - h)) / (2 * h)
        print(f"1e-{k} {fw:.10f} {ce:.10f} {abs(fw-ex):.2e} {abs(ce-ex):.2e}")
    # Richardson on central: D(h)=central h; D(h/2); R=(4D(h/2)-D(h))/3
    f = math.cos; x = 1.0; true = -math.sin(1.0)
    D = lambda h: (f(x + h) - f(x - h)) / (2 * h)
    print("cos' at 1: D(.4)", D(.4), "D(.2)", D(.2), "D(.1)", D(.1), "true", true)
    R1 = [(4 * D(h/2) - D(h)) / 3 for h in (0.4, 0.2)]
    R2 = (16 * R1[1] - R1[0]) / 15
    print("R1", R1, "R2", R2, "errs", [abs(r - true) for r in R1], abs(R2 - true))
    # five-point formula
    h = 0.1; fp5 = (f(x - 2*h) - 8*f(x - h) + 8*f(x + h) - f(x + 2*h)) / (12 * h); print("5pt", fp5, abs(fp5 - true))
    # second derivative
    h = 0.1; f2 = (f(x + h) - 2 * f(x) + f(x - h)) / h**2; print("2nd", f2, "true", -math.cos(1), abs(f2 + math.cos(1)))
    # optimal h estimate
    print("opt h forward ~ 2*sqrt(eps)", 2*math.sqrt(2.2e-16), "central ~ eps^(1/3)", (2.2e-16)**(1/3))
    # strips needed: integral of e^x on [0,1] trapezoid, simpson, tolerance 1e-6
    # trap error <= (b-a)h^2/12 max f'' = e h^2/12 -> h<= sqrt(12e-6/e) ; simpson (b-a)h^4/180 e
    n_t = math.ceil(1 / math.sqrt(12e-6 / math.e)); n_s = math.ceil(1 / (180e-6 / math.e) ** 0.25)
    if n_s % 2: n_s += 1
    print("n trap", n_t, "n simpson", n_s)
    def trap(f, a, b, n): h = (b - a) / n; return h * (f(a)/2 + sum(f(a + i*h) for i in range(1, n)) + f(b)/2)
    def simp(f, a, b, n): h = (b - a) / n; return h/3 * (f(a) + f(b) + 4*sum(f(a + i*h) for i in range(1, n, 2)) + 2*sum(f(a + i*h) for i in range(2, n, 2)))
    I = math.e - 1
    print("trap n_t", trap(math.exp, 0, 1, n_t) - I, "simp n_s", simp(math.exp, 0, 1, n_s) - I)
    for n in (2, 4, 8, 16): print(n, trap(math.exp, 0, 1, n) - I, simp(math.exp, 0, 1, n) - I)
    # midpoint
    def mid(f, a, b, n): h = (b - a) / n; return h * sum(f(a + (i + .5) * h) for i in range(n))
    print("mid n=4", mid(math.exp, 0, 1, 4), "err", mid(math.exp,0,1,4)-I, "trap n=4", trap(math.exp,0,1,4))
    # Boole's rule (4 strips, h=0.25) for e^x
    h = 0.25; xs = [i*h for i in range(5)]; ys = [math.exp(v) for v in xs]
    boole = 2*h/45 * (7*ys[0] + 32*ys[1] + 12*ys[2] + 32*ys[3] + 7*ys[4]); print("boole", boole, boole - I, "simpson n=4", simp(math.exp,0,1,4)-I)
    # Gauss-Legendre
    for n in (2, 3, 4):
        xg, wg = np.polynomial.legendre.leggauss(n); print(n, xg, wg)
        v = 0.5 * sum(w * math.exp(0.5 * (x + 1)) for x, w in zip(xg, wg)); print("GL", n, "e^x [0,1]", v, v - I)
    # sin on [0,pi]
    for n in (2, 3, 4):
        xg, wg = np.polynomial.legendre.leggauss(n); v = math.pi/2 * sum(w * math.sin(math.pi/2 * (x + 1)) for x, w in zip(xg, wg)); print("GL", n, "sin[0,pi]", v, v - 2)
    print("simpson n=2 sin", simp(math.sin, 0, math.pi, 2), "simp 4", simp(math.sin, 0, math.pi, 4))
    # int 1/(1+x^2) 0..1 = pi/4 using GL2, GL3
    for n in (2, 3):
        xg, wg = np.polynomial.legendre.leggauss(n); v = 0.5 * sum(w / (1 + (0.5*(x+1))**2) for x, w in zip(xg, wg)); print("GL atan", n, v, v - math.pi/4)
    # exactness check: GL2 integrates x^3 on [-1,1]
    # adaptive Simpson on sqrt-like (x^0.5) 0..1 and on sin(1/x)? use exp(-x^2)? choose peak function 1/(1e-2 + (x-0.3)^2) 0..1
    cnt = [0]
    def g(x): cnt[0] += 1; return 1 / (0.01 + (x - 0.3)**2)
    def asr(f, a, b, tol, whole, fa, fm, fb, depth=0):
        m = (a + b) / 2; lm = (a + m) / 2; rm = (m + b) / 2; flm = f(lm); frm = f(rm)
        left = (m - a) / 6 * (fa + 4 * flm + fm); right = (b - m) / 6 * (fm + 4 * frm + fb)
        if abs(left + right - whole) <= 15 * tol or depth > 40: return left + right + (left + right - whole) / 15
        return asr(f, a, m, tol/2, left, fa, flm, fm, depth+1) + asr(f, m, b, tol/2, right, fm, frm, fb, depth+1)
    a, b = 0, 1; fa, fb = g(a), g(b); fm = g(.5); whole = (b - a)/6*(fa + 4*fm + fb)
    cnt[0] = 0; val = asr(g, a, b, 1e-8, whole, fa, fm, fb); ncount = cnt[0]
    exact = 10 * (math.atan((1 - 0.3)/0.1) - math.atan(-0.3/0.1))
    print("adaptive", val, exact, abs(val - exact), "evals", ncount)
    # fixed Simpson with same accuracy: find n
    for n in (10, 20, 50, 100, 200, 400, 800, 1600):
        v = simp(lambda x: 1/(0.01 + (x-0.3)**2), 0, 1, n); print(n, abs(v - exact))
    # improper: int_0^1 x^-1/2 : substitution x=t^2 -> int 2 dt = 2 ; simpson fails
    print("sqrt-sing trap n=100 midpoint:", mid(lambda x: x**-0.5, 0, 1, 100), mid(lambda x: x**-0.5, 0, 1, 10000))
    # int_0^inf e^-x^2 = sqrt(pi)/2 via x=t/(1-t)
    h2 = lambda t: math.exp(-(t/(1-t))**2) / (1-t)**2 if t < 1 else 0.0
    print("inf", simp(h2, 0, 1, 40), math.sqrt(math.pi)/2)
    # Monte Carlo e^x on 0..1
    rng = np.random.default_rng(2024)
    for N in (100, 10000, 1000000):
        xs_ = rng.random(N); v = np.exp(xs_).mean(); print("MC", N, v, v - I, "se", np.exp(xs_).std() / math.sqrt(N))

def u4():
    print("== u4")
    # pivoting: [1e-20 1; 1 1] x = [1; 2] ; no pivot vs partial pivot (double)
    e = 1e-20
    m = 1 / e; a22 = 1 - m * 1; b2 = 2 - m * 1; x2 = b2 / a22; x1 = (1 - x2) / e
    print("no pivot", x1, x2, "true ~ (1, 1)")
    # ordinary-size version: 0.0001 x + y = 1 ; x + y = 2 in 3 digit arithmetic
    # Cholesky 3x3
    A = np.array([[4., 12, -16], [12, 37, -43], [-16, -43, 98]]); L = np.linalg.cholesky(A); print("chol L\n", L, np.allclose(L @ L.T, A))
    # Thomas algorithm: tridiagonal 2,-1 system n=5 with b=[1,0,0,0,1]
    n = 5; a = [0, -1, -1, -1, -1]; b = [2] * 5; c = [-1, -1, -1, -1, 0]; d = [1, 0, 0, 0, 1]
    cp = [0] * n; dp = [0] * n; cp[0] = c[0] / b[0]; dp[0] = d[0] / b[0]
    for i in range(1, n):
        den = b[i] - a[i] * cp[i-1]; cp[i] = c[i] / den; dp[i] = (d[i] - a[i] * dp[i-1]) / den
    x = [0] * n; x[-1] = dp[-1]
    for i in range(n - 2, -1, -1): x[i] = dp[i] - cp[i] * x[i+1]
    print("thomas cp", cp, "dp", dp, "x", x)
    T = np.diag(b) + np.diag(a[1:], -1) + np.diag(c[:-1], 1); print(np.linalg.solve(T, d))
    # norms and condition number
    M = np.array([[1, 2], [1.0001, 2.0001]]); print("cond1", np.linalg.cond(M, 1), "cond_inf", np.linalg.cond(M, np.inf), "det", np.linalg.det(M))
    b0 = np.array([3, 3.0001]); b1 = np.array([3, 3.0002]); print(np.linalg.solve(M, b0), np.linalg.solve(M, b1))
    Mi = np.linalg.inv(M); print("inv", Mi, "norm_inf M", np.abs(M).sum(1).max(), "norm_inf inv", np.abs(Mi).sum(1).max())
    H = np.array([[1/(i+j+1) for j in range(3)] for i in range(3)]); print("H3 cond", np.linalg.cond(H, np.inf), "H3 inv\n", np.round(np.linalg.inv(H)))
    # residual vs error: x_approx = (1.1 -?) for M
    xt = np.array([1., 1.]); xa = np.array([2, 0.5]); print("residual", M @ xa - M @ xt, "error", xa - xt)
    xa = np.array([3.0, 0.0]); print("res", M @ xa - np.array([3, 3.0001]), "err", xa - xt)
    # SOR vs Jacobi vs GS on tridiagonal 4,-1 n=5?  use the 1-D Poisson matrix 2,-1 n=9? use (4,-1) n=6
    n = 8; A = 2 * np.eye(n) - np.eye(n, k=1) - np.eye(n, k=-1); bb = np.ones(n)
    def run(w, kind, tol=1e-6, maxit=5000):
        x = np.zeros(n); xs = np.linalg.solve(A, bb)
        for it in range(1, maxit):
            xo = x.copy()
            if kind == "J":
                x = (bb - (A - np.diag(np.diag(A))) @ xo) / np.diag(A)
            else:
                for i in range(n):
                    s = bb[i] - A[i, :i] @ x[:i] - A[i, i+1:] @ xo[i+1:]
                    x[i] = (1 - w) * xo[i] + w * s / A[i, i]
            if np.abs(x - xo).max() < tol: return it
        return None
    print("Jacobi", run(1, "J"), "GS", run(1, "S"))
    for w in (1.0, 1.2, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 1.95):
        print("w", w, run(w, "S"))
    rho = max(abs(np.linalg.eigvals(np.eye(n) - np.diag(1 / np.diag(A)) @ A)))
    wopt = 2 / (1 + math.sqrt(1 - rho**2)); print("rho_J", rho, "rho_GS", rho**2, "wopt", wopt)
    # spectral radius for textbook 3x3 diag dominant system 10x+y+z=12 etc
    A3 = np.array([[10., 1, 1], [2, 10, 1], [2, 2, 10]]); D = np.diag(np.diag(A3))
    TJ = np.eye(3) - np.linalg.inv(D) @ A3; print("rho Jacobi", max(abs(np.linalg.eigvals(TJ))))
    TG = -np.linalg.inv(np.tril(A3)) @ np.triu(A3, 1); print("rho GS", max(abs(np.linalg.eigvals(TG))))
    # non-dominant system where Jacobi diverges: x + 2y = 3, 3x + y = 4? 
    Ab = np.array([[1., 2], [3, 1]]); Dd = np.diag(np.diag(Ab)); print("rho J nondom", max(abs(np.linalg.eigvals(np.eye(2) - np.linalg.inv(Dd) @ Ab))))
    # eigenvalues: Gershgorin and inverse power
    G = np.array([[4., 1, 0], [1, 3, 1], [0, 1, 2]]); print("eig", np.linalg.eigvalsh(G), "gersh centers/radii", [(G[i, i], abs(G[i]).sum() - abs(G[i, i])) for i in range(3)])
    x = np.array([1., 1, 1]); print("power")
    for k in range(8):
        y = G @ x; lam = np.max(abs(y)); rq = (x @ y) / (x @ x); x = y / lam; print(k, np.round(y, 5), round(lam, 6), "RQ", round(rq, 6))
    # inverse power with shift 1.5
    sh = 1.5; x = np.array([1., 1, 1]); print("inverse power shift", sh)
    for k in range(5):
        y = np.linalg.solve(G - sh * np.eye(3), x); lam = y[np.argmax(abs(y))]; x = y / lam; print(k, np.round(x, 5), "eig est", sh + 1 / lam)
    # QR iteration unshifted
    Ak = G.copy()
    for k in range(6):
        Q, R = np.linalg.qr(Ak); Ak = R @ Q
    print("QR after 6", np.round(np.diag(Ak), 5), np.round(Ak, 4))
    # operation counts: Gauss n^3/3 ; time
    for n in (10, 100, 1000): print(n, n**3 // 3, n**2)

if __name__ == "__main__":
    for w in which:
        globals()[w]()
