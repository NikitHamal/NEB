import itertools, re
from sympy import symbols
from sympy.logic import SOPform
from libfig import PRE

def figblock(caption, code, w=5.9, h=2.6, xlim=None, ylim=None, canvas=True):
    head = "fig,ax=ckt_canvas(%s,%s,xlim=%s,ylim=%s)\n" % (w, h, xlim, ylim) if canvas else ""
    return '```figure caption="%s"\n%s%s\n%s```\n' % (caption.replace('"', "'"), PRE.strip() + "\n", head, code.strip() + "\n")

def minimize(ones, dcs, nv):
    """Return list of terms, each a list of (var_index, polarity); var 0 is the MSB."""
    if not ones: return []
    if len(set(ones) | set(dcs)) == 2 ** nv and not (set(range(2**nv)) - set(ones) - set(dcs)):
        return [[]]
    vs = symbols("v0:%d" % nv)
    mt = [[(m >> (nv - 1 - i)) & 1 for i in range(nv)] for m in ones]
    dc = [[(m >> (nv - 1 - i)) & 1 for i in range(nv)] for m in dcs]
    e = SOPform(vs, mt, dc)
    s = str(e)
    if s == "True": return [[]]
    if s == "False": return []
    terms = []
    for t in s.split("|"):
        t = t.strip().strip("()")
        lits = []
        for l in t.split("&"):
            l = l.strip()
            neg = l.startswith("~")
            nm = l.lstrip("~")
            lits.append((int(nm[1:]), 0 if neg else 1))
        lits.sort()
        terms.append(lits)
    return terms

def term_minterms(term, nv):
    out = []
    for m in range(2 ** nv):
        if all(((m >> (nv - 1 - i)) & 1) == p for i, p in term): out.append(m)
    return out

def check_cover(terms, ones, dcs, nv):
    cov = set()
    for t in terms: cov |= set(term_minterms(t, nv))
    assert set(ones) <= cov and cov <= set(ones) | set(dcs), (terms, ones, dcs)

def _tx(n): return re.sub(r"Q(\d)", r"Q_\1", n)
def tex_lit(name, p):
    name = _tx(name)
    return name if p else r"\overline{%s}" % name

def tex_term(t, names):
    return "".join(tex_lit(names[i], p) for i, p in t) if t else "1"

def tex_sop(terms, names):
    if not terms: return "0"
    return " + ".join(tex_term(t, names) for t in terms)

def term_lits_py(terms): return repr([[(i, p) for i, p in t] for t in terms])

GROUP_COLORS = ["#d9534f", "#1d6fb8", "#2e8b57", "#b8860b", "#6a5acd", "#008b8b"]

def kmap_code(nv, ones, dcs, terms, x0, y0, title, names="ABCD", cs=0.6):
    groups = []
    for gi, t in enumerate(terms):
        groups.append((term_minterms(t, nv), GROUP_COLORS[gi % 6]))
    return "kmap(ax,%s,%s,%d,%r,%r,%r,names=%r,cs=%s,title=%r)\n" % (x0, y0, nv, sorted(ones), sorted(dcs), groups, names, cs, title)

def kmap_figure(caption, maps, names, per_row=3, cs=0.6):
    """maps: list of (title, nv, ones, dcs, terms)"""
    code = ""
    nrows = (len(maps) + per_row - 1) // per_row
    nv0 = max(m[1] for m in maps)
    mw = (2 ** (nv0 - 2 if nv0 > 2 else 1) if False else 4) * cs
    colw = 4 * cs + 1.3
    rowh = (4 if nv0 == 4 else 2) * cs + 1.1
    for k, (title, nv, ones, dcs, terms) in enumerate(maps):
        r, c = divmod(k, per_row)
        code += kmap_code(nv, ones, dcs, terms, 0.9 + c * colw, (nrows - 1 - r) * rowh + 0.4, title, names, cs)
    W = per_row * colw + 0.4
    H = nrows * rowh + 0.2
    figw = min(6.6, max(3.2, W * 0.62))
    return figblock(caption, code, w=round(figw, 2), h=round(figw * H / W, 2), xlim="(0,%s)" % round(W, 2), ylim="(-0.2,%s)" % round(H, 2))

# ---- flip-flop excitation ----
X = "X"
def excite(kind, q, qn):
    if kind == "T": return {"T": q ^ qn}
    if kind == "D": return {"D": qn}
    if kind == "JK":
        return {(0, 0): {"J": 0, "K": X}, (0, 1): {"J": 1, "K": X}, (1, 0): {"J": X, "K": 1}, (1, 1): {"J": X, "K": 0}}[(q, qn)]
    if kind == "SR":
        return {(0, 0): {"S": 0, "R": X}, (0, 1): {"S": 1, "R": 0}, (1, 0): {"S": 0, "R": 1}, (1, 1): {"S": X, "R": 0}}[(q, qn)]
PINS = {"T": ["T"], "D": ["D"], "JK": ["J", "K"], "SR": ["S", "R"]}

def design(nq, kind, trans, extra=0, qn_prefix="Q", xnames=("X",)):
    """trans: dict (state, x) -> (next_state, z) for all defined combos; z may be None.
    Variables: Q(nq-1)..Q0 then X's. Returns dict with rows, equations, fin and map list."""
    nv = nq + extra
    qnames = ["%s%d" % (qn_prefix, i) for i in range(nq - 1, -1, -1)] if nq > 1 else [qn_prefix]
    names = qnames + list(xnames[:extra])
    rows = []
    funcs = {}  # (ff index left->right, pin) -> (ones, dcs)
    zf = ([], [])
    for s in range(2 ** nq):
        for x in range(2 ** extra):
            m = (s << extra) | x
            if (s, x) not in trans:
                for f in range(nq):
                    for p in PINS[kind]:
                        funcs.setdefault((f, p), ([], []))[1].append(m)
                zf[1].append(m)
                continue
            ns, z = trans[(s, x)]
            row = {"s": s, "x": x, "ns": ns, "z": z, "pins": {}}
            for f in range(nq):
                bit = nq - 1 - f
                q = (s >> bit) & 1; qn = (ns >> bit) & 1
                ex = excite(kind, q, qn)
                for p, v in ex.items():
                    ones, dcs = funcs.setdefault((f, p), ([], []))
                    if v == 1: ones.append(m)
                    elif v == X: dcs.append(m)
                    row["pins"][(f, p)] = v
            if z == 1: zf[0].append(m)
            rows.append(row)
    eq = {}
    for k, (ones, dcs) in funcs.items():
        t = minimize(ones, dcs, nv)
        check_cover(t, ones, dcs, nv)
        eq[k] = t
    zt = None
    if any(r["z"] is not None for r in rows):
        zt = minimize(zf[0], zf[1], nv); check_cover(zt, zf[0], zf[1], nv)
    return dict(nv=nv, names=names, rows=rows, funcs=funcs, eq=eq, zt=zt, zf=zf, qnames=qnames)

def fin_from(d, kind, nq):
    fin = []
    for f in range(nq):
        dd = {}
        for p in PINS[kind]:
            t = d["eq"][(f, p)]
            if t == []: dd[p] = "0"
            elif t == [[]]: dd[p] = "1"
            else: dd[p] = t
        fin.append(dd)
    return fin

def ff_pin_name(kind, f, qnames, p):
    return "%s_{%s}" % (p, qnames[f][1:] if len(qnames[f]) > 1 else "")

def eq_lines(d, kind, nq):
    out = []
    for f in range(nq):
        for p in PINS[kind]:
            t = d["eq"][(f, p)]
            nm = "%s_{%s}" % (p, d["qnames"][f][1:])
            out.append("%s = %s" % (nm, tex_sop(t, d["names"])))
    return out

def pin_equations_block(d, kind, nq):
    lines = eq_lines(d, kind, nq)
    if d["zt"] is not None: lines.append("Z = " + tex_sop(d["zt"], d["names"]))
    return "$$\\begin{gathered} " + " \\\\ ".join(lines) + " \\end{gathered}$$"

def excitation_table(d, kind, nq, extra_names=(), show_z=False):
    nm = d["qnames"]
    hdr = ["Present " + " ".join(nm)] if False else []
    cols = ["Q" + str(i) if False else n for n in nm]
    h = [("%s" % n) for n in nm] + list(extra_names) + [("%s⁺" % n) for n in nm]
    if show_z: h.append("Z")
    for f in range(nq):
        for p in PINS[kind]: h.append("%s%s" % (p, nm[f][1:]))
    lines = ["| " + " | ".join(h) + " |", "|" + "---|" * len(h)]
    for r in d["rows"]:
        cells = [str((r["s"] >> (nq - 1 - f)) & 1) for f in range(nq)]
        cells += [str(r["x"] >> (len(extra_names) - 1 - j) & 1) for j in range(len(extra_names))]
        cells += [str((r["ns"] >> (nq - 1 - f)) & 1) for f in range(nq)]
        if show_z: cells.append(str(r["z"]))
        for f in range(nq):
            for p in PINS[kind]: cells.append(str(r["pins"][(f, p)]))
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines) + "\n"

def maps_for(d, kind, nq, extra_z=True):
    maps = []
    nv = d["nv"]
    for f in range(nq):
        for p in PINS[kind]:
            ones, dcs = d["funcs"][(f, p)]
            maps.append(("%s%s" % (p, d["qnames"][f][1:]), nv, ones, dcs, d["eq"][(f, p)]))
    if d["zt"] is not None and extra_z:
        maps.append(("Z", nv, d["zf"][0], d["zf"][1], d["zt"]))
    return maps

def circuit_fig(caption, d, kind, nq, extra=()):
    fin = fin_from(d, kind, nq)
    import json
    code = "seqcirc(ax,%r,%r,%r,zterms=%s,extra=%r)\n" % (kind, d["qnames"], fin, repr(d["zt"]) if d["zt"] else "None", list(extra))
    return figblock(caption, code, w=6.9, h=4.6, xlim="(-0.4,%s)" % (6.1 * nq + (8 if d["zt"] else 4) + 3), ylim="(-9.5,3.0)")

# ---- Mealy sequence detector (overlapping) ----
def detector(pattern):
    L = len(pattern)
    def nxt(k, b):
        s = pattern[:k] + b
        z = 1 if s == pattern else 0
        t = s
        while t and not pattern.startswith(t): t = t[1:]
        return len(t) % L if len(t) == L else len(t), z
    trans = {}
    for k in range(L):
        for b in "01":
            ns, z = nxt(k, b)
            if len(pattern[:k] + b) == L and (pattern[:k] + b) == pattern:
                # full match: fall back to longest proper prefix that is a suffix
                t = pattern
                t = t[1:]
                while t and not pattern.startswith(t): t = t[1:]
                ns = len(t)
            trans[(k, int(b))] = (ns, z)
    return trans

def timing_sim(seq, n, d=0.0):
    """seq: list of ints (state after each clock), returns transitions per bit as lists of (t,level)."""
    pass

def bits(s, n): return [(s >> (n - 1 - i)) & 1 for i in range(n)]

def wave_calls(states, nq, names, y0, dstage=0.0, step=1.0, ystep=0.95, ripple=False, x0=0.0, start_time=0.05):
    """states[0] = initial state before 1st clock. Returns code lines drawing each Q (MSB on top)."""
    code = ""
    n = len(states)
    for f in range(nq):
        bit = nq - 1 - f
        lv = (states[0] >> bit) & 1
        tr = [(x0, lv)]
        for k in range(1, n):
            nb = (states[k] >> bit) & 1
            if nb != lv:
                dt = start_time + (dstage * (nq - 1 - f if False else bit) if ripple else 0)
                tr.append((x0 + k * step - step + dt + step * 0 if False else x0 + (k - 1) * step + dt, nb)); lv = nb
        yy = y0 + (nq - 1 - f) * ystep
        code += "wave(ax,%s,%r,%s,%r,x0=%s)\n" % (yy, tr, x0 + (n - 1) * step, names[f], x0)
    return code
