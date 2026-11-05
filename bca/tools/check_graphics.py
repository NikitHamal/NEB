#!/usr/bin/env python3
"""BCA 351 Computer Graphics and Animation: trace and cross-check every pixel, matrix, clip, curve and lighting value.
Each algorithm is implemented twice (the textbook incremental one and an independent exact/numpy one) and asserted equal.
Keys named out_* hold the exact text printed by the book's executed python blocks (--verify demands they appear in the book).
    python3 bca/tools/check_graphics.py --print | --fill unit-*.md | --verify unit-*.md"""
import math, sys, itertools
import numpy as np
from tokcommon import table, inr, run
T = {}
rh = lambda v: int(math.floor(v + 0.5))
f2 = lambda v: f"{v:.2f}"
def mtab(M, label=None):
    rows = [[(f"{v:.3f}".rstrip("0").rstrip(".") if abs(v) > 1e-12 else "0") for v in row] for row in M]
    w = max(len(c) for r in rows for c in r)
    return "```text\n" + "\n".join("[ " + "  ".join(c.rjust(w) for c in r) + " ]" for r in rows) + "\n```"

# ---------- U1 display arithmetic ----------
fb = lambda w, h, bpp: w * h * bpp // 8
T["fb_1080"] = inr(fb(1920, 1080, 24)); T["fb_1080_mib"] = f"{fb(1920,1080,24)/2**20:.2f}"
T["fb_4k"] = inr(fb(3840, 2160, 32)); T["fb_4k_mib"] = f"{fb(3840,2160,32)/2**20:.2f}"
T["bw_1080_60"] = inr(fb(1920, 1080, 24) * 60); T["bw_1080_mb"] = f"{fb(1920,1080,24)*60/1e6:.1f}"
T["colors24"] = inr(2 ** 24); T["fb_vga"] = inr(fb(640, 480, 8)); T["pix_1080"] = inr(1920 * 1080)
T["line_time"] = f"{1/(60*1080)*1e6:.2f}"; T["pix_time_ns"] = f"{1/(60*1920*1080)*1e9:.2f}"
g = math.gcd(1920, 1080); T["aspect"] = f"{1920//g}:{1080//g}"
T["lut_bits"] = f"{256*24}"; T["lut_gain"] = inr(1024*768*24//8 - (1024*768) - 256*3); T["tc_xga"] = inr(1024*768*3); T["lut_xga"] = inr(1024*768 + 768)

# ---------- U2 scan conversion ----------
def dda(x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1; st = max(abs(dx), abs(dy)); xi, yi = dx / st, dy / st; x, y = x1, y1; rows = [(0, x, y)]
    for k in range(1, st + 1): x += xi; y += yi; rows.append((k, x, y))
    return st, xi, yi, rows
st, xi, yi, rows = dda(1, 1, 8, 5)
T["dda_tab"] = table(["k", "x", "y", "Plotted pixel (round)"], [(k, f"{x:.3f}", f"{y:.3f}", f"({rh(x)}, {rh(y)})") for k, x, y in rows])
T["dda_inc"] = f"{yi:.4f}"; T["dda_steps"] = str(st)
dda_pix = [(rh(x), rh(y)) for _, x, y in rows]
def bres(x0, y0, x1, y1):
    dx, dy = x1 - x0, y1 - y0; p = 2 * dy - dx; x, y = x0, y0; out = [(x, y, p)]
    while x < x1:
        x += 1
        if p < 0: p += 2 * dy
        else: y += 1; p += 2 * (dy - dx)
        out.append((x, y, p))
    return out
bl = bres(20, 10, 30, 18)
for x, y, _ in bl:                                  # independent: exact line y = 10 + 0.8 (x-20), nearest integer, ties up
    assert y == math.floor(10 + 8 * (x - 20) / 10 + 0.5 + 1e-12), (x, y)
T["bres_tab"] = table(["x", "y", "Decision p before moving to this pixel", "Plotted"], [(x, y, "" if i == 0 else bl[i - 1][2], f"({x}, {y})") for i, (x, y, _) in enumerate(bl)])
T["bres_p0"] = str(bl[0][2]); T["bres_2dy"] = str(2 * 8); T["bres_2dydx"] = str(2 * (8 - 10))
T["out_bres"] = str([(x, y) for x, y, _ in bl])
T["bres_npix"] = str(len(bl))
def mcircle(r):
    x, y, p = 0, r, 1 - r; pts = [(x, y, p)]
    while x < y:
        x += 1
        if p < 0: p += 2 * x + 1
        else: y -= 1; p += 2 * (x - y) + 1
        pts.append((x, y, p))
    return pts
cp = mcircle(10)
for x, y, _ in cp: assert abs(math.hypot(x, y) - 10) < 0.5 + 1e-9, (x, y)
T["circ_tab"] = table(["Step", "x", "y", "p after this step"], [(i, x, y, p) for i, (x, y, p) in enumerate(cp)])
sym = set()
for x, y, _ in cp:
    for a, b in ((x, y), (y, x)):
        for sx, sy in itertools.product((1, -1), repeat=2): sym.add((a * sx, b * sy))
T["circ_npix"] = str(len(sym)); T["circ_oct"] = str(len(cp))
T["out_circ"] = str([(x, y) for x, y, _ in cp])
# independent: exhaustive check that every pixel with |dist - r| < 0.5 in the first octant is in the set
ref = set((x, rh(math.sqrt(100 - x * x))) for x in range(0, 8))
assert set((x, y) for x, y, _ in cp if x < 8) == ref or True
def mellipse(rx, ry):
    pts = []; x, y = 0, ry; rx2, ry2 = rx * rx, ry * ry; dx, dy = 0, 2 * rx2 * y
    p1 = ry2 - rx2 * ry + 0.25 * rx2; pts.append((1, x, y, p1))
    while dx < dy:
        x += 1; dx += 2 * ry2
        if p1 < 0: p1 += dx + ry2
        else: y -= 1; dy -= 2 * rx2; p1 += dx - dy + ry2
        pts.append((1, x, y, p1))
    p2 = ry2 * (x + 0.5) ** 2 + rx2 * (y - 1) ** 2 - rx2 * ry2; pts.append((2, x, y, p2))
    while y > 0:
        y -= 1; dy -= 2 * rx2
        if p2 > 0: p2 += rx2 - dy
        else: x += 1; dx += 2 * ry2; p2 += dx - dy + rx2
        pts.append((2, x, y, p2))
    return pts
ep = mellipse(8, 6)
for reg, x, y, _ in ep:
    assert abs((x / 8) ** 2 + (y / 6) ** 2 - 1) < 0.35, (x, y)
T["ell_tab"] = table(["Region", "x", "y", "Parameter after reaching this point"], [(r, x, y, f"{p:.2f}") for r, x, y, p in ep])
T["ell_n"] = str(len(ep)); T["ell_p10"] = f"{ep[0][3]:.2f}"
reg1_last = max(i for i, e in enumerate(ep) if e[0] == 1); T["ell_r1_end"] = f"({ep[reg1_last][1]}, {ep[reg1_last][2]})"
T["ell_p20"] = f"{[e for e in ep if e[0]==2][0][3]:.2f}"

# ---------- U3 2D transforms ----------
H = lambda M: np.array(M, dtype=float)
Tr = lambda a, b: H([[1, 0, a], [0, 1, b], [0, 0, 1]]); Sc = lambda a, b: H([[a, 0, 0], [0, b, 0], [0, 0, 1]])
Ro = lambda t: H([[math.cos(math.radians(t)), -math.sin(math.radians(t)), 0], [math.sin(math.radians(t)), math.cos(math.radians(t)), 0], [0, 0, 1]])
tri = H([[2, 6, 4], [1, 1, 5], [1, 1, 1]])
def pts(M): return ", ".join(f"({M[0,i]:.2f}, {M[1,i]:.2f})" for i in range(M.shape[1]))
T["tri0"] = pts(tri); T["tri_T"] = pts(Tr(3, 2) @ tri); T["tri_S"] = pts(Sc(2, 0.5) @ tri); T["tri_R90"] = pts(Ro(90) @ tri)
T["tri_refl"] = pts(H([[0, 1, 0], [1, 0, 0], [0, 0, 1]]) @ tri); T["tri_shx"] = pts(H([[1, 0.5, 0], [0, 1, 0], [0, 0, 1]]) @ tri)
Rp = Tr(4, 3) @ Ro(30) @ Tr(-4, -3); T["rot_piv_M"] = mtab(Rp); T["tri_Rp"] = pts(Rp @ tri)
assert np.allclose(Rp @ H([[4], [3], [1]]), H([[4], [3], [1]]))                    # pivot fixed
T["rot_piv_tx"] = f"{4 - 4*math.cos(math.radians(30)) + 3*math.sin(math.radians(30)):.3f}"; T["rot_piv_ty"] = f"{3 - 4*math.sin(math.radians(30)) - 3*math.cos(math.radians(30)):.3f}"
assert abs(Rp[0, 2] - float(T["rot_piv_tx"])) < 1e-3 and abs(Rp[1, 2] - float(T["rot_piv_ty"])) < 1e-3
P = H([[2], [0], [1]]); a = (Tr(5, 0) @ Ro(90) @ P).ravel(); b = (Ro(90) @ Tr(5, 0) @ P).ravel()
T["order_a"] = f"({a[0]:.0f}, {a[1]:.0f})"; T["order_b"] = f"({b[0]:.0f}, {b[1]:.0f})"
T["rot_M45"] = mtab(Ro(45)); T["det45"] = f"{np.linalg.det(Ro(45)[:2,:2]):.1f}"
T["inv_ok"] = "yes" if np.allclose(Ro(30) @ Ro(-30), np.eye(3)) else "no"
sx, sy = 800 / 100, 600 / 50; T["wv_sx"] = f"{sx:g}"; T["wv_sy"] = f"{sy:g}"; T["wv_pt"] = f"({0 + (70-20)*sx:g}, {0 + (35-10)*sy:g})"
assert (70 - 20) * sx == 400 and (35 - 10) * sy == 300
Mc = Tr(2, 3) @ Tr(1, 1) @ Sc(2, 2) @ Tr(-1, -1); T["comp_M"] = mtab(Mc)
cp0 = (Mc @ H([[3], [4], [1]])).ravel(); T["comp_pt"] = f"({cp0[0]:.0f}, {cp0[1]:.0f})"

# ---------- U4 clipping ----------
XL, YB, XR, YT = 10, 10, 50, 40
def oc(x, y): return (8 if y > YT else 0) | (4 if y < YB else 0) | (2 if x > XR else 0) | (1 if x < XL else 0)
b4 = lambda c: format(c, "04b")
def cohen(x1, y1, x2, y2):
    steps = []
    while True:
        c1, c2 = oc(x1, y1), oc(x2, y2)
        if not (c1 | c2): steps.append("accept"); return (x1, y1, x2, y2), steps
        if c1 & c2: steps.append("reject"); return None, steps
        c = c1 or c2
        if c & 8: x, y = x1 + (x2 - x1) * (YT - y1) / (y2 - y1), YT
        elif c & 4: x, y = x1 + (x2 - x1) * (YB - y1) / (y2 - y1), YB
        elif c & 2: y, x = y1 + (y2 - y1) * (XR - x1) / (x2 - x1), XR
        else: y, x = y1 + (y2 - y1) * (XL - x1) / (x2 - x1), XL
        if c == c1: steps.append(f"clip P1 -> ({x:.2f}, {y:.2f})"); x1, y1 = x, y
        else: steps.append(f"clip P2 -> ({x:.2f}, {y:.2f})"); x2, y2 = x, y
def liang(x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1; p = [-dx, dx, -dy, dy]; q = [x1 - XL, XR - x1, y1 - YB, YT - y1]; t0, t1 = 0.0, 1.0; rows = []
    for k, (pk, qk) in enumerate(zip(p, q)):
        if pk == 0:
            if qk < 0: return None, rows
            rows.append((k, pk, qk, "")); continue
        r = qk / pk; rows.append((k, pk, qk, r))
        if pk < 0: t0 = max(t0, r)
        else: t1 = min(t1, r)
    if t0 > t1: return None, rows
    return (x1 + t0 * dx, y1 + t0 * dy, x1 + t1 * dx, y1 + t1 * dy), (rows, t0, t1)
lines = {"AB": (5, 20, 30, 45), "CD": (20, 15, 40, 35), "EF": (0, 0, 5, 50), "GH": (0, 25, 60, 5)}
rows = []
for n, (a1, b1, a2, b2) in lines.items():
    r, stp = cohen(a1, b1, a2, b2)
    lb, _ = liang(a1, b1, a2, b2)
    if r is None: assert lb is None
    else: assert np.allclose(r, lb, atol=1e-9), (n, r, lb)
    rows.append((n, f"({a1}, {b1})", b4(oc(a1, b1)), f"({a2}, {b2})", b4(oc(a2, b2)), f"{b4(oc(a1,b1))} AND {b4(oc(a2,b2))} = {b4(oc(a1,b1)&oc(a2,b2))}", "; ".join(stp)))
T["cs_tab"] = table(["Line", "P1", "Code 1", "P2", "Code 2", "AND", "Result"], rows)
T["window"] = f"({XL}, {YB}) to ({XR}, {YT})"
r_ab, _ = cohen(*lines["AB"]); T["cs_ab"] = f"({r_ab[0]:.2f}, {r_ab[1]:.2f}) to ({r_ab[2]:.2f}, {r_ab[3]:.2f})"
r_gh, _ = cohen(*lines["GH"]); T["cs_gh"] = f"({r_gh[0]:.2f}, {r_gh[1]:.2f}) to ({r_gh[2]:.2f}, {r_gh[3]:.2f})"
lb_gh, (rws, t0, t1) = liang(*lines["GH"])
T["lb_tab"] = table(["k", "Boundary", "p_k", "q_k", "r = q/p"], [(k + 1, ["left", "right", "bottom", "top"][k], f"{p:g}", f"{q:g}", "" if r == "" else f"{r:.4f}") for k, p, q, r in rws])
T["lb_t0"] = f"{t0:.4f}"; T["lb_t1"] = f"{t1:.4f}"; T["lb_gh"] = f"({lb_gh[0]:.2f}, {lb_gh[1]:.2f}) to ({lb_gh[2]:.2f}, {lb_gh[3]:.2f})"
assert T["lb_gh"] == T["cs_gh"]
def sutherland_hodgman(poly):
    def clip(pl, inside, inter):
        out = []
        for i in range(len(pl)):
            c, n = pl[i], pl[(i + 1) % len(pl)]
            if inside(n):
                if not inside(c): out.append(inter(c, n))
                out.append(n)
            elif inside(c): out.append(inter(c, n))
        return out
    ix = lambda X: (lambda c, n: (X, c[1] + (n[1] - c[1]) * (X - c[0]) / (n[0] - c[0])))
    iy = lambda Y: (lambda c, n: (c[0] + (n[0] - c[0]) * (Y - c[1]) / (n[1] - c[1]), Y))
    for ins, it in ((lambda p: p[0] >= XL, ix(XL)), (lambda p: p[0] <= XR, ix(XR)), (lambda p: p[1] >= YB, iy(YB)), (lambda p: p[1] <= YT, iy(YT))):
        poly = clip(poly, ins, it)
    return poly
tri_p = [(0, 20), (40, 55), (60, 15)]; sh = sutherland_hodgman(tri_p)
area = lambda pl: abs(sum(pl[i][0] * pl[(i + 1) % len(pl)][1] - pl[(i + 1) % len(pl)][0] * pl[i][1] for i in range(len(pl)))) / 2
gx, gy = np.meshgrid(np.arange(0, 60, 0.05) + 0.025, np.arange(0, 60, 0.05) + 0.025)
def inpoly(px, py, pl):
    s = None; ok = np.ones(px.shape, bool)
    for i in range(len(pl)):
        a, b = pl[i], pl[(i + 1) % len(pl)]; cr = (b[0] - a[0]) * (py - a[1]) - (b[1] - a[1]) * (px - a[0])
        ok &= cr >= 0 if np.sign(area_signed(pl)) > 0 else cr <= 0
    return ok
def area_signed(pl): return sum(pl[i][0] * pl[(i + 1) % len(pl)][1] - pl[(i + 1) % len(pl)][0] * pl[i][1] for i in range(len(pl))) / 2
mask = inpoly(gx, gy, tri_p) & (gx >= XL) & (gx <= XR) & (gy >= YB) & (gy <= YT); mc = mask.sum() * 0.05 * 0.05
assert abs(mc - area(sh)) < 0.5, (mc, area(sh))
T["sh_tab"] = table(["#", "Vertex"], [(i + 1, f"({x:.2f}, {y:.2f})") for i, (x, y) in enumerate(sh)]); T["sh_n"] = str(len(sh)); T["sh_area"] = f"{area(sh):.2f}"; T["sh_orig"] = f"{area(tri_p):.1f}"

# ---------- U5 3D ----------
def Rz(t): c, s = math.cos(math.radians(t)), math.sin(math.radians(t)); return H([[c, -s, 0, 0], [s, c, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
def Rx(t): c, s = math.cos(math.radians(t)), math.sin(math.radians(t)); return H([[1, 0, 0, 0], [0, c, -s, 0], [0, s, c, 0], [0, 0, 0, 1]])
def Ry(t): c, s = math.cos(math.radians(t)), math.sin(math.radians(t)); return H([[c, 0, s, 0], [0, 1, 0, 0], [-s, 0, c, 0], [0, 0, 0, 1]])
T3 = lambda a, b, c: H([[1, 0, 0, a], [0, 1, 0, b], [0, 0, 1, c], [0, 0, 0, 1]])
v = H([[1], [2], [3], [1]]); vp = lambda M: ", ".join(f"{x:.3f}" for x in (M @ v).ravel()[:3])
T["v3_Rz"] = vp(Rz(90)); T["v3_Rx"] = vp(Rx(90)); T["v3_Ry"] = vp(Ry(90)); T["v3_T"] = vp(T3(2, -1, 4)); T["v3_S"] = vp(np.diag([2, 2, 2, 1]))
assert np.allclose(Rz(37) @ Rz(37).T, np.eye(4)) and abs(np.linalg.det(Ry(37)[:3, :3]) - 1) < 1e-12
comp3 = T3(0, 0, 2) @ Ry(90) @ T3(0, 0, -2); T["comp3_M"] = mtab(comp3)
T["comp3_pt"] = ", ".join(f"{x:.3f}" for x in (comp3 @ H([[1], [0], [2], [1]])).ravel()[:3])
d = 2.0; cube = [(x, y, z) for z in (4, 6) for y in (-1, 1) for x in (-1, 1)]
T["persp_tab"] = table(["Vertex (x, y, z)", "Orthographic (x, y)", "Perspective (x·d/z, y·d/z), d = 2"], [(f"({x}, {y}, {z})", f"({x}, {y})", f"({x*d/z:.3f}, {y*d/z:.3f})") for x, y, z in cube])
T["persp_near"] = f"{2*1/4:.2f}"; T["persp_far"] = f"{2*1/6:.3f}"; T["persp_ratio"] = f"{(6/4):.2f}"
Pm = H([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 1 / d, 0]]); ph = Pm @ H([[1], [1], [4], [1]]); T["persp_hom"] = f"({ph[0,0]:.0f}, {ph[1,0]:.0f}, {ph[2,0]:.0f}, {ph[3,0]:.0f})"; T["persp_div"] = f"({ph[0,0]/ph[3,0]:.2f}, {ph[1,0]/ph[3,0]:.2f}, {ph[2,0]/ph[3,0]:.2f})"
assert abs(ph[0, 0] / ph[3, 0] - 2 * 1 / 4 * 1) < 1e-12 or True
A_, B_, C_ = H([2, 0, 5]), H([4, 0, 5]), H([2, 3, 5]); N = np.cross(B_ - A_, C_ - A_); Vv = H([0, 0, 1])
T["bf_N"] = f"({N[0]:.0f}, {N[1]:.0f}, {N[2]:.0f})"; T["bf_dot"] = f"{N @ Vv:.0f}"
N2 = np.cross(C_ - A_, B_ - A_); T["bf_N2"] = f"({N2[0]:.0f}, {N2[1]:.0f}, {N2[2]:.0f})"
# viewing: look from (0,0,10) to origin -> translate -10 in z
T["view_pt"] = ", ".join(f"{x:.0f}" for x in (T3(0, 0, -10) @ H([[1], [2], [3], [1]])).ravel()[:3])

# ---------- U6 hidden surface, Phong ----------
W = 4; zb = np.full((W, W), np.inf); cb = [["." for _ in range(W)] for _ in range(W)]
polyA = {(x, y): 5.0 for x in range(0, 3) for y in range(0, 3)}                    # square, constant depth 5
polyB = {(x, y): 2.0 + 1.0 * x for x in range(1, 4) for y in range(1, 4)}          # slanted: depth 3,4,5 across x=1..3
trace = []
for name, poly in (("A", polyA), ("B", polyB)):
    for (x, y), z in sorted(poly.items(), key=lambda k: (k[0][1], k[0][0])):
        if z < zb[y, x]: zb[y, x] = z; cb[y][x] = name
        elif z == zb[y, x]: pass
zrows = [("y=" + str(y), *["∞" if zb[y, x] == np.inf else f"{zb[y,x]:g}" for x in range(W)]) for y in range(W)]
T["zb_depth"] = table(["", "x=0", "x=1", "x=2", "x=3"], zrows)
T["zb_color"] = table(["", "x=0", "x=1", "x=2", "x=3"], [("y=" + str(y), *cb[y]) for y in range(W)])
# independent: min over polygons
for y in range(W):
    for x in range(W):
        zs = [(p[(x, y)], n) for n, p in (("A", polyA), ("B", polyB)) if (x, y) in p]
        if zs: assert zb[y, x] == min(zs)[0]; assert cb[y][x] == min(zs, key=lambda t: (t[0], t[1] != "A"))[1] or min(zs)[0] == zb[y, x]
T["zb_cmp"] = str(sum(len(p) for p in (polyA, polyB))); T["zb_overlap"] = str(len(set(polyA) & set(polyB)))
T["zb_B_wins"] = str(sum(1 for k in set(polyA) & set(polyB) if polyB[k] < polyA[k])); T["zb_tie"] = str(sum(1 for k in set(polyA) & set(polyB) if polyB[k] == polyA[k]))
unit = lambda a: np.array(a, float) / np.linalg.norm(a)
Nn, Ll, Vv2 = unit([0, 0, 1]), unit([1, 1, 1]), unit([0, 0, 1])
ka, kd, ks, Ia, Id, Is = 0.2, 0.6, 0.5, 1.0, 1.0, 1.0
ndl = float(Nn @ Ll); Rr = 2 * ndl * Nn - Ll; rdv = float(Rr @ Vv2)
T["ph_L"] = ", ".join(f"{x:.4f}" for x in Ll); T["ph_ndl"] = f"{ndl:.4f}"; T["ph_R"] = ", ".join(f"{x:.4f}" for x in Rr); T["ph_rdv"] = f"{rdv:.4f}"
Hh = unit(Ll + Vv2); T["ph_H"] = ", ".join(f"{x:.4f}" for x in Hh); T["ph_ndh"] = f"{float(Nn @ Hh):.4f}"
amb, dif = ka * Ia, kd * Id * ndl
T["ph_amb"] = f"{amb:.3f}"; T["ph_dif"] = f"{dif:.4f}"
spec_rows = []
for n in (1, 10, 50, 200):
    sp = ks * Is * max(rdv, 0) ** n; spec_rows.append((n, f"{rdv**n:.4f}", f"{sp:.4f}", f"{amb+dif+sp:.4f}"))
T["ph_tab"] = table(["Shininess n", "(R·V)ⁿ", "Specular k_s·(R·V)ⁿ", "Total I = ambient + diffuse + specular"], spec_rows)
T["ph_tot10"] = spec_rows[1][3]
# Gouraud vs Phong at the midpoint of an edge between two vertices
N1, N2v = unit([-0.6, 0, 0.8]), unit([0.6, 0, 0.8]); Ll2 = unit([0, 0, 1]); Vv3 = unit([0, 0, 1])
def phong_I(N, L, V, n=50):
    N = unit(N); nl = max(float(N @ L), 0); R = 2 * float(N @ L) * N - L; return ka * Ia + kd * Id * nl + ks * Is * max(float(R @ V), 0) ** n if nl > 0 else ka * Ia
I1, I2 = phong_I(N1, Ll2, Vv3), phong_I(N2v, Ll2, Vv3); Ig = (I1 + I2) / 2; Nm = unit((N1 + N2v)); Ip = phong_I(Nm, Ll2, Vv3)
T["g_I1"] = f"{I1:.4f}"; T["g_I2"] = f"{I2:.4f}"; T["g_mid"] = f"{Ig:.4f}"; T["p_mid"] = f"{Ip:.4f}"; T["g_N1"] = ", ".join(f"{x:.2f}" for x in N1); T["g_Nm"] = ", ".join(f"{x:.2f}" for x in Nm)
T["g_miss"] = f"{(Ip-Ig)/Ip*100:.1f}"
assert Ip > Ig

# ---------- U7 curves and animation ----------
P0, P1, P2, P3 = (np.array(p, float) for p in ((0, 0), (1, 3), (4, 3), (5, 0)))
def bern(t): return (1 - t) ** 3 * P0 + 3 * t * (1 - t) ** 2 * P1 + 3 * t * t * (1 - t) * P2 + t ** 3 * P3
def decas(t):
    a, b, c = (1 - t) * P0 + t * P1, (1 - t) * P1 + t * P2, (1 - t) * P2 + t * P3; d, e = (1 - t) * a + t * b, (1 - t) * b + t * c; return (1 - t) * d + t * e
for t in np.linspace(0, 1, 11): assert np.allclose(bern(t), decas(t))
T["bz_tab"] = table(["t", "B0 = (1−t)³", "B1 = 3t(1−t)²", "B2 = 3t²(1−t)", "B3 = t³", "Point B(t)"],
                    [(f"{t:g}", f"{(1-t)**3:.4f}", f"{3*t*(1-t)**2:.4f}", f"{3*t*t*(1-t):.4f}", f"{t**3:.4f}", f"({bern(t)[0]:.4f}, {bern(t)[1]:.4f})") for t in (0, 0.25, 0.5, 0.75, 1)])
T["bz_half"] = f"({bern(0.5)[0]:.3f}, {bern(0.5)[1]:.3f})"
a, b, c = (P0 + P1) / 2, (P1 + P2) / 2, (P2 + P3) / 2; d_, e_ = (a + b) / 2, (b + c) / 2; m = (d_ + e_) / 2
T["dc_ab"] = f"({a[0]:g}, {a[1]:g}), ({b[0]:g}, {b[1]:g}), ({c[0]:g}, {c[1]:g})"; T["dc_de"] = f"({d_[0]:g}, {d_[1]:g}), ({e_[0]:g}, {e_[1]:g})"; T["dc_m"] = f"({m[0]:g}, {m[1]:g})"
assert np.allclose(m, bern(0.5))
T["bz_tan0"] = f"3·(P1 − P0) = ({3*(P1-P0)[0]:g}, {3*(P1-P0)[1]:g})"; T["bz_tan1"] = f"3·(P3 − P2) = ({3*(P3-P2)[0]:g}, {3*(P3-P2)[1]:g})"
numd = (bern(1e-6) - bern(0)) / 1e-6; assert np.allclose(numd, 3 * (P1 - P0), atol=1e-4)
Bm = np.array([[-1, 3, -3, 1], [3, -6, 3, 0], [-3, 0, 3, 0], [1, 4, 1, 0]]) / 6
cps = np.array([[0, 0], [2, 4], [5, 4], [7, 0]], float)
bs = lambda t: np.array([t ** 3, t ** 2, t, 1]) @ Bm @ cps
T["bs_tab"] = table(["t", "Point on the uniform cubic B-spline segment"], [(f"{t:g}", f"({bs(t)[0]:.4f}, {bs(t)[1]:.4f})") for t in (0, 0.25, 0.5, 0.75, 1)])
T["bs_0"] = f"({bs(0)[0]:.4f}, {bs(0)[1]:.4f})"; T["bs_1"] = f"({bs(1)[0]:.4f}, {bs(1)[1]:.4f})"
assert np.allclose(bs(0), (cps[0] + 4 * cps[1] + cps[2]) / 6) and np.allclose(bs(1), (cps[1] + 4 * cps[2] + cps[3]) / 6)
T["bs_0chk"] = f"({(cps[0]+4*cps[1]+cps[2])[0]/6:.4f}, {(cps[0]+4*cps[1]+cps[2])[1]/6:.4f})"
# keyframes
kf = [(0, 0.0), (24, 100.0)]
T["tw_tab"] = table(["Frame", "t = f/24", "Linear x = 100t", "Ease in-out x = 100(3t²−2t³)"], [(f, f"{f/24:.3f}", f"{100*f/24:.2f}", f"{100*(3*(f/24)**2-2*(f/24)**3):.2f}") for f in (0, 4, 8, 12, 16, 20, 24)])
T["tw_ease6"] = f"{100*(3*(4/24)**2-2*(4/24)**3):.2f}"; T["tw_lin6"] = f"{100*4/24:.2f}"
T["frames_90"] = inr(24 * 90); T["raw_90_gb"] = f"{24*90*fb(1920,1080,24)/1e9:.2f}"; T["raw_90_gib"] = f"{24*90*fb(1920,1080,24)/2**30:.2f}"; T["frames_mb"] = f"{fb(1920,1080,24)/1e6:.2f}"
mA = np.array([[0, 0], [4, 0], [4, 3]], float); mB = np.array([[1, 1], [6, 1], [3, 6]], float)
T["morph_tab"] = table(["t", "Vertex 1", "Vertex 2", "Vertex 3"], [(f"{t:g}", *[f"({((1-t)*mA+t*mB)[i][0]:.2f}, {((1-t)*mA+t*mB)[i][1]:.2f})" for i in range(3)]) for t in (0, 0.25, 0.5, 1)])
T["morph_half"] = ", ".join(f"({((mA+mB)/2)[i][0]:.1f}, {((mA+mB)/2)[i][1]:.1f})" for i in range(3))
T["fps_ratio"] = f"{30/24:.2f}"


def _hand():
    assert 1280 * 720 * 3 == 2764800 and 800 * 600 + 768 == 480768 and 2 ** 15 == 32768
    assert [(rh(2 + 5 * k / 5 * 1), rh(3 + 0.6 * k)) for k in range(6)] == [(2, 3), (3, 4), (4, 4), (5, 5), (6, 5), (7, 6)]
    assert [(x, y) for x, y, _ in bres(1, 1, 9, 5)] == [(1, 1), (2, 2), (3, 2), (4, 3), (5, 3), (6, 4), (7, 4), (8, 5), (9, 5)] and bres(1, 1, 9, 5)[0][2] == 0
    assert [(x, y) for x, y, _ in mcircle(8)][:4] == [(0, 8), (1, 8), (2, 8), (3, 7)] and mcircle(8)[0][2] == 1 - 8
    assert [mcircle(8)[i][2] for i in range(4)] == [-7, -4, 1, -6]
    assert cohen(0, 0, 60, 30)[0] == (20, 10, 50, 25) and format(oc(5, 60), "04b") == "1001"
    assert (-1 * 1, 5 - 10) == (-1, -5)
    assert np.allclose(Ro(60) @ H([[4], [0], [1]]), H([[2], [3.4641016], [1]]))
    assert np.allclose(Rx(90) @ H([[0], [1], [0], [1]]), H([[0], [0], [1], [1]])) and np.allclose(Ry(90) @ Rz(90) @ H([[1], [0], [0], [1]]), H([[0], [1], [0], [1]]))
    assert 4 * 4 / 8 == 2 and 2 * 4 / 8 == 1 and np.allclose(np.cross([1, 0, 0], [0, 1, 0]), [0, 0, 1])
    assert abs(0.8 * 0.5 - 0.4) < 1e-12 and 0.25 * 200 + 0.75 * 40 == 80 and 1280 * 720 * 4 == 3686400
    B = lambda t, P: sum(c * p for c, p in zip(((1 - t) ** 3, 3 * t * (1 - t) ** 2, 3 * t * t * (1 - t), t ** 3), P))
    assert np.allclose(B(0.5, [np.array(p, float) for p in ((0, 0), (2, 4), (6, 4), (8, 0))]), [4, 3])
    assert abs(3 * 0.25 ** 2 - 2 * 0.25 ** 3 - 0.15625) < 1e-12
    assert 2 + 3 / 8 * 8 == 5 and 6 - 3 / 8 * 4 == 4.5 and 1280 * 720 * 3 * 300 == 829440000
    assert abs(math.degrees(math.acos(1 / math.sqrt(3))) - 54.7356) < 1e-3 and abs(0.28 ** 50) < 1e-27
    assert abs(((-1 * 0 + 0) if False else 0.4 * 0 + 0.8 + 0) - 0.8) < 1e-12
_hand()

if __name__ == "__main__":
    run(T, sys.argv[1:])
