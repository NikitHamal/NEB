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
for w in which:
    globals()[w]()
