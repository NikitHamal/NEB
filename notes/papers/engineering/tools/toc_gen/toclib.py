"""Theory of Computation helpers: DFA/NFA/PDA/TM simulators, trace formatters and figure helpers.

Figure helpers are used inside ```figure blocks of the paper markdown:
    import sys, os; sys.path.insert(0, os.path.join(os.getcwd(), 'notes/papers/engineering/tools/toc_gen')); import toclib
    toclib.graph(nodes, edges)  /  toclib.tree(('S', ['a', ('S', [...])]))
"""
import itertools, re
from collections import deque

INK = "#14181f"; ACC = "#1d6fb8"; RED = "#b00020"; MUT = "#5b6472"


# ----------------------------------------------------------------------------- automata
def dfa_run(delta, start, finals, w):
    q = start; path = [q]
    for ch in w:
        q = delta[(q, ch)]; path.append(q)
    return q in finals, path


def nfa_closure(eps, S):
    S = set(S); st = list(S)
    while st:
        q = st.pop()
        for r in eps.get(q, ()):
            if r not in S: S.add(r); st.append(r)
    return frozenset(S)


def subset_construct(delta, eps, start, finals, alphabet):
    """delta[(q,a)] -> set; eps[q] -> set. Returns (states_order, table, finals_set)."""
    s0 = nfa_closure(eps, {start}); order = [s0]; table = {}; todo = deque([s0])
    while todo:
        S = todo.popleft()
        for a in alphabet:
            T = set()
            for q in S: T |= set(delta.get((q, a), ()))
            T = nfa_closure(eps, T); table[(S, a)] = T
            if T not in order: order.append(T); todo.append(T)
    return order, table, {S for S in order if S & set(finals)}


def minimise(states, alphabet, delta, start, finals):
    """Partition refinement (Moore). Returns (blocks, log)."""
    reach = {start}; st = [start]
    while st:
        q = st.pop()
        for a in alphabet:
            r = delta[(q, a)]
            if r not in reach: reach.add(r); st.append(r)
    states = [s for s in states if s in reach]
    P = [frozenset(s for s in states if s in finals), frozenset(s for s in states if s not in finals)]
    P = [b for b in P if b]; log = [list(P)]
    while True:
        idx = {q: i for i, b in enumerate(P) for q in b}; new = []
        for b in P:
            g = {}
            for q in b: g.setdefault(tuple(idx[delta[(q, a)]] for a in alphabet), set()).add(q)
            new += [frozenset(v) for v in g.values()]
        if len(new) == len(P): return P, log
        P = new; log.append(list(P))


# ----------------------------------------------------------------------------- Turing machine
def tm_run(delta, start, accept, w, blank="_", maxsteps=20000):
    """delta[(q, sym)] = (q2, write, 'L'|'R'|'S'). Returns (accepted, configs)."""
    tape = list(w) if w else [blank]; head = 0; q = start; cfgs = []
    for _ in range(maxsteps):
        cfgs.append((q, "".join(tape), head))
        if q in accept: return True, cfgs
        sym = tape[head] if head < len(tape) else blank
        if (q, sym) not in delta: return False, cfgs
        q2, wr, mv = delta[(q, sym)]
        if head >= len(tape): tape.append(blank)
        tape[head] = wr
        head += {"L": -1, "R": 1, "S": 0}[mv]
        if head < 0: tape.insert(0, blank); head = 0
        if head >= len(tape): tape.append(blank)
        q = q2
    raise RuntimeError("TM did not halt")


def tm_output(cfgs, blank="_"):
    return cfgs[-1][1].strip(blank)


def cfg_str(c, blank="_"):
    q, tape, head = c
    t = tape.ljust(head + 1, blank)
    left = t[:head]; right = t[head:]
    left = left.lstrip(blank); right = right.rstrip(blank) or blank
    return left + "[" + q + "]" + right


def trace_md(cfgs, per=3, maxlines=60):
    ids = [cfg_str(c) for c in cfgs]
    if len(ids) > maxlines: ids = ids[:maxlines // 2] + ["..."] + ids[-maxlines // 2:]
    rows = []
    for i in range(0, len(ids), per):
        rows.append(" ⊢ ".join("`%s`" % s if s != "..." else "…" for s in ids[i:i + per]))
    return "\n\n".join(rows)


def tm_table(delta, blank_name="B"):
    rows = ["| State | Read | Write | Move | Next |", "|---|---|---|---|---|"]
    for (q, s), (q2, wr, mv) in delta.items():
        rows.append("| %s | %s | %s | %s | %s |" % (q, s.replace("_", blank_name), wr.replace("_", blank_name), mv, q2))
    return "\n".join(rows)


# ----------------------------------------------------------------------------- PDA
def pda_run(delta, start, finals, w, z0="Z", accept_by="final", maxcfg=200000):
    """delta: list of (q, a or '', top, q2, push) with push a string (top at index 0)."""
    init = (start, 0, z0); seen = {init: None}; dq = deque([init])
    while dq:
        c = dq.popleft(); q, i, stk = c
        if i == len(w) and ((accept_by == "final" and q in finals) or (accept_by == "empty" and stk == "")):
            path = []
            while c is not None: path.append(c); c = seen[c]
            return True, path[::-1]
        for (p, a, t, p2, push) in delta:
            if p != q or not stk or stk[0] != t: continue
            if a == "" or (i < len(w) and w[i] == a):
                n = (p2, i + (1 if a else 0), push + stk[1:])
                if n not in seen: seen[n] = c; dq.append(n)
        if len(seen) > maxcfg: break
    return False, []


def id_str(w, c):
    q, i, stk = c
    return "(%s, %s, %s)" % (q, w[i:] or "ε", stk or "ε")


def pda_trace_md(w, path, per=3):
    ids = ["`%s`" % id_str(w, c) for c in path]
    return "\n\n".join(" ⊢ ".join(ids[i:i + per]) for i in range(0, len(ids), per))


# ----------------------------------------------------------------------------- language checks
def lang_equal(py_regex, pred, alphabet, n=12):
    r = re.compile("^(?:%s)$" % py_regex)
    for L in range(n + 1):
        for t in itertools.product(alphabet, repeat=L):
            s = "".join(t)
            if bool(r.match(s)) != bool(pred(s)): return False, s
    return True, None


def strings(alphabet, n):
    for L in range(n + 1):
        for t in itertools.product(alphabet, repeat=L): yield "".join(t)


# ----------------------------------------------------------------------------- figures
def graph(nodes, edges, loops=(), scale=0.62, width=6.4, fs=7.6, R=0.38, pad=1.1):
    """nodes: {name: (x, y, flags)}; flags is a comma list of 's' (start), 'f' (final), 'label:text'.
    edges: (a, b, label, rad); loops: (node, label, 'up'|'down')."""
    import matplotlib.pyplot as plt, matplotlib.patches as mp
    xs = [p[0] for p in nodes.values()]; ys = [p[1] for p in nodes.values()]
    down = any(l[2] == "down" for l in loops)
    xl = (min(xs) - pad - 0.8, max(xs) + pad); yl = (min(ys) - pad - (0.5 if down else 0), max(ys) + pad + 0.5)
    w = (xl[1] - xl[0]) * scale; h = (yl[1] - yl[0]) * scale
    if width and w > width: h *= width / w; w = width
    fig, ax = plt.subplots(figsize=(w, h)); ax.axis("off"); ax.set_xlim(*xl); ax.set_ylim(*yl); ax.set_aspect("equal")
    for k, (x, y, fl) in nodes.items():
        parts = fl.split(",")
        ax.add_patch(mp.Circle((x, y), R, fc="white", ec=INK, lw=1.2, zorder=3))
        if "f" in parts: ax.add_patch(mp.Circle((x, y), R - 0.08, fc="none", ec=INK, lw=1.0, zorder=4))
        lab = k
        for p in parts:
            if p.startswith("label:"): lab = p[6:]
        ax.text(x, y, lab, ha="center", va="center", fontsize=fs, zorder=5)
        if "s" in parts:
            ax.annotate("", xy=(x - R, y), xytext=(x - R - 0.8, y), arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.1))
    for (a, b, t, rad) in edges:
        A = nodes[a][:2]; B = nodes[b][:2]
        ax.annotate("", xy=B, xytext=A, arrowprops=dict(arrowstyle="-|>", color=ACC, lw=1.1, shrinkA=15, shrinkB=15,
                    connectionstyle="arc3,rad=%s" % rad), zorder=2)
        dx, dy = B[0] - A[0], B[1] - A[1]
        m = ((A[0] + B[0]) / 2 + 0.5 * rad * dy, (A[1] + B[1]) / 2 - 0.5 * rad * dx)
        ax.text(m[0], m[1], t, ha="center", va="center", fontsize=fs - 0.2, color=RED,
                bbox=dict(fc="white", ec="none", pad=0.4), zorder=6)
    for (n, t, side) in loops:
        x, y = nodes[n][:2]; s = 1 if side == "up" else -1
        ax.add_patch(mp.Arc((x, y + s * (R + 0.2)), 0.62, 0.62, theta1=-20 if s > 0 else 160, theta2=200 if s > 0 else 380,
                            ec=ACC, lw=1.1, zorder=2))
        ax.text(x, y + s * (R + 0.68), t, ha="center", va="center", fontsize=fs - 0.2, color=RED)
    return fig


def tree(root, dx=0.62, dy=0.95, fs=8.5):
    """root = (label, [children]); a child that is a str is a leaf (terminal)."""
    import matplotlib.pyplot as plt
    counter = [0]; nid = [0]; items = []

    def layout(node, depth):
        nid[0] += 1; me = nid[0]
        if isinstance(node, str):
            x = counter[0]; counter[0] += 1
            items.append((me, node, x, depth, [], True)); return me, x
        lab, kids = node; res = [layout(k, depth + 1) for k in kids]
        x = sum(r[1] for r in res) / len(res)
        items.append((me, lab, x, depth, [r[0] for r in res], False)); return me, x
    layout(root, 0)
    byid = {i[0]: i for i in items}; maxd = max(i[3] for i in items); n = max(counter[0], 1)
    fig, ax = plt.subplots(figsize=(max(2.6, n * dx + 0.6), (maxd + 1) * dy + 0.4)); ax.axis("off")
    ax.set_xlim(-0.8, n - 0.2); ax.set_ylim(-maxd - 0.6, 0.6)
    for (i, lab, x, d, kids, leaf) in items:
        for k in kids:
            _, _, x2, d2, _, _ = byid[k]
            ax.plot([x, x2], [-d - 0.16, -d2 + 0.16], color=INK, lw=0.9, zorder=1)
    for (i, lab, x, d, kids, leaf) in items:
        ax.text(x, -d, lab, ha="center", va="center", fontsize=fs, color=(RED if leaf else ACC),
                fontweight=("normal" if leaf else "bold"), zorder=3, bbox=dict(fc="white", ec="none", pad=0.6))
    return fig
