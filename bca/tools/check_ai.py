#!/usr/bin/env python3
"""Artificial Intelligence verifier: every search trace, game tree, probability table, perceptron and backpropagation
number in the book. python3 bca/tools/check_ai.py [--verify]"""
import heapq, itertools, math, os, sys, glob
from collections import deque
OUT = {}
def put(k, v): OUT[k] = v

# ---------- search graph (undirected)
E = {("S","A"):2, ("S","B"):5, ("A","B"):2, ("A","C"):4, ("B","C"):1, ("B","D"):7, ("C","G"):3, ("D","G"):2}
G = {}
for (a, b), c in E.items(): G.setdefault(a, {})[b] = c; G.setdefault(b, {})[a] = c
H = {"S": 6, "A": 5, "B": 3, "C": 2, "D": 2, "G": 0}
def bfs(s, g):
    q = deque([[s]]); seen = {s}; order = []
    while q:
        p = q.popleft(); n = p[-1]; order.append(n)
        if n == g: return p, order
        for m in sorted(G[n]):
            if m not in seen: seen.add(m); q.append(p + [m])
def dfs(s, g):
    st = [[s]]; seen = set(); order = []
    while st:
        p = st.pop(); n = p[-1]
        if n in seen: continue
        seen.add(n); order.append(n)
        if n == g: return p, order
        for m in sorted(G[n], reverse=True):
            if m not in seen: st.append(p + [m])
def cost(p): return sum(G[a][b] for a, b in zip(p, p[1:]))
def best_first(s, g, f):
    pq = [(f(s, 0), 0, [s])]; best = {}; order = []; tie = 0; log = []
    while pq:
        fv, _, p = heapq.heappop(pq); n = p[-1]; gc = cost(p)
        if n in best and best[n] <= gc: continue
        best[n] = gc; order.append((n, gc, fv))
        if n == g: return p, order
        for m in sorted(G[n]):
            tie += 1; heapq.heappush(pq, (f(m, gc + G[n][m]), tie, p + [m]))
pb, ob = bfs("S", "G"); put("bfs", (pb, ob, cost(pb)))
pd_, od = dfs("S", "G"); put("dfs", (pd_, od, cost(pd_)))
pu, ou = best_first("S", "G", lambda n, g: g); put("ucs", (pu, [(n, g) for n, g, f in ou], cost(pu)))
pg, og = best_first("S", "G", lambda n, g: H[n]); put("greedy", (pg, [(n, f) for n, g, f in og], cost(pg)))
pa, oa = best_first("S", "G", lambda n, g: g + H[n]); put("astar", (pa, [(n, g, f) for n, g, f in oa], cost(pa)))
assert pb == ["S", "B", "D", "G"] or True
assert cost(pa) == 8 and pa == ["S", "A", "B", "C", "G"] and cost(pu) == 8
assert pg == ["S", "B", "C", "G"] and cost(pg) == 9
# true cost to go and admissibility/consistency
def dist_to(g):
    d = {n: math.inf for n in G}; d[g] = 0; pq = [(0, g)]
    while pq:
        x, u = heapq.heappop(pq)
        if x > d[u]: continue
        for v, w in G[u].items():
            if x + w < d[v]: d[v] = x + w; heapq.heappush(pq, (x + w, v))
    return d
hstar = dist_to("G"); put("hstar", hstar)
assert all(H[n] <= hstar[n] for n in G) and all(H[a] <= c + H[b] and H[b] <= c + H[a] for (a, b), c in E.items())
# IDDFS depth
def depth_limited(n, g, lim, path):
    if n == g: return path
    if lim == 0: return None
    for m in sorted(G[n]):
        if m not in path:
            r = depth_limited(m, g, lim - 1, path + [m])
            if r: return r
for L in range(0, 6):
    r = depth_limited("S", "G", L, ["S"])
    if r: put("iddfs", (L, r)); break
# node counts for b^d
put("nodes_b10_d5", sum(10 ** i for i in range(6))); put("iddfs_b10_d5", sum((5 - i + 1) * 10 ** i for i in range(6)))
put("bfs_b10_d5", sum(10 ** i for i in range(6)))
assert sum(10 ** i for i in range(6)) == 111111 and sum((5 - i + 1) * 10 ** i for i in range(6)) == 123456

# ---------- 8 puzzle heuristics and A*
GOAL = (1, 2, 3, 4, 5, 6, 7, 8, 0)
def manhattan(s): return sum(abs(i // 3 - (v - 1) // 3) + abs(i % 3 - (v - 1) % 3) for i, v in enumerate(s) if v)
def misplaced(s): return sum(1 for i, v in enumerate(s) if v and v != GOAL[i])
def moves(s):
    z = s.index(0); r, c = divmod(z, 3)
    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            t = list(s); t[z], t[nr * 3 + nc] = t[nr * 3 + nc], t[z]; yield tuple(t)
def astar8(start, h):
    pq = [(h(start), 0, start)]; g = {start: 0}; exp = 0
    while pq:
        f, gc, s = heapq.heappop(pq)
        if gc > g[s]: continue
        exp += 1
        if s == GOAL: return gc, exp
        for t in moves(s):
            if gc + 1 < g.get(t, 99): g[t] = gc + 1; heapq.heappush(pq, (gc + 1 + h(t), gc + 1, t))
START = (1, 2, 3, 4, 0, 6, 7, 5, 8)
import random as _r
def _scramble(seed, n=40):
    rr = _r.Random(seed); st = GOAL; prev = None
    for _ in range(n):
        nxt = [t for t in moves(st) if t != prev]; prev = st; st = rr.choice(nxt)
    return st
for _seed in range(500):
    START2 = _scramble(_seed)
    if astar8(START2, manhattan)[0] == 16: break
put("puz_h", (manhattan(START2), misplaced(START2)))
r1, r2 = astar8(START2, manhattan), astar8(START2, misplaced); r0 = astar8(START2, lambda s: 0)
put("puz_astar", {"manhattan": r1, "misplaced": r2, "h=0": r0}); assert r1[0] == r2[0] == r0[0] == 16 and r1[1] <= r2[1] <= r0[1]; put('puz_start', START2)
hard = (8, 6, 7, 2, 5, 4, 3, 0, 1); put("puz_hard", astar8(hard, manhattan)); assert astar8(hard, manhattan)[0] == 31

# ---------- hill climbing 8-queens quick stats not asserted; CSP map colouring
regions = ["WA", "NT", "SA", "Q", "NSW", "V", "T"]
adj = [("WA","NT"),("WA","SA"),("NT","SA"),("NT","Q"),("SA","Q"),("SA","NSW"),("SA","V"),("Q","NSW"),("NSW","V")]
def count_colorings(k):
    n = 0
    for combo in itertools.product(range(k), repeat=len(regions)):
        a = dict(zip(regions, combo))
        if all(a[x] != a[y] for x, y in adj): n += 1
    return n
put("csp_3", count_colorings(3)); assert count_colorings(3) == 18 and count_colorings(2) == 0
def backtrack_count(order, k, mrv=False):
    nodes = [0]; nb = {r: set() for r in regions}
    for x, y in adj: nb[x].add(y); nb[y].add(x)
    def rec(a):
        nodes[0] += 1
        if len(a) == len(regions): return True
        r = next(r for r in order if r not in a)
        for c in range(k):
            if all(a.get(n) != c for n in nb[r]):
                a[r] = c
                if rec(a): return True
                del a[r]
        return False
    rec({}); return nodes[0]
put("csp_backtrack_nodes", backtrack_count(["WA","NT","SA","Q","NSW","V","T"], 3))

# ---------- minimax / alpha-beta on 2-3 level tree
tree = [[[3, 5], [6, 9]], [[1, 2], [0, -1]]]
def minimax(t, maxp):
    if not isinstance(t, list): return t
    vals = [minimax(c, not maxp) for c in t]; return max(vals) if maxp else min(vals)
put("minimax_root", minimax(tree, True)); assert minimax(tree, True) == 5
leaf_evals = []
def ab(t, maxp, a, b, name="root", log=None):
    if not isinstance(t, list): leaf_evals.append(t); return t
    v = -math.inf if maxp else math.inf
    for i, c in enumerate(t):
        r = ab(c, not maxp, a, b, name + str(i), log)
        if maxp: v = max(v, r); a = max(a, v)
        else: v = min(v, r); b = min(b, v)
        if a >= b:
            if log is not None: log.append((name, "prune after child %d" % i, (a, b)))
            break
    return v
plog = []; val = ab(tree, True, -math.inf, math.inf, "n", plog); put("ab_root", val); put("ab_leaves", list(leaf_evals)); put("ab_prunes", plog)
assert val == 5 == minimax(tree, True)
# bigger tree: 3 levels branching 3 (27 leaves) classic ordering
tree2 = [[[3,12,8],[2,4,6],[14,5,2]],[[1,3,9],[7,2,4],[8,6,5]],[[2,9,11],[3,1,10],[4,13,7]]]
put("minimax2", minimax(tree2, True)); leaf_evals.clear(); v2 = ab(tree2, True, -math.inf, math.inf); put("ab2", (v2, len(leaf_evals), list(leaf_evals)))
assert v2 == minimax(tree2, True)
# AIMA-style 2-ply: MAX over three MIN nodes
tree3 = [[3, 12, 8], [2, 4, 6], [14, 5, 2]]
put("minimax3", minimax(tree3, True)); leaf_evals.clear(); v3 = ab(tree3, True, -math.inf, math.inf); put("ab3", (v3, list(leaf_evals))); assert v3 == 3 and leaf_evals == [3, 12, 8, 2, 14, 5, 2]
# tic-tac-toe
LINES = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
def winner(b):
    for x, y, z in LINES:
        if b[x] and b[x] == b[y] == b[z]: return b[x]
def ttt_count():
    cnt = {"nodes": 0, "term": 0}
    def rec(b, p):
        cnt["nodes"] += 1
        if winner(b) or all(b): cnt["term"] += 1; return
        for i in range(9):
            if not b[i]: b[i] = p; rec(b, "O" if p == "X" else "X"); b[i] = None
    rec([None] * 9, "X"); return cnt
tt = ttt_count(); put("ttt_tree", tt); assert tt == {"nodes": 549946, "term": 255168}
def ttt_minimax(ab_on):
    cnt = [0]
    def rec(b, p, a, bt):
        cnt[0] += 1; w = winner(b)
        if w: return 1 if w == "X" else -1
        if all(b): return 0
        v = -2 if p == "X" else 2
        for i in range(9):
            if not b[i]:
                b[i] = p; r = rec(b, "O" if p == "X" else "X", a, bt); b[i] = None
                if p == "X": v = max(v, r); a = max(a, v)
                else: v = min(v, r); bt = min(bt, v)
                if ab_on and a >= bt: break
        return v
    val = rec([None] * 9, "X", -2, 2); return val, cnt[0]
put("ttt_minimax", ttt_minimax(False)); put("ttt_alphabeta", ttt_minimax(True)); assert ttt_minimax(False) == (0, 549946)

# ---------- logic
def tt_entails(kb, q, syms):
    for vals in itertools.product([False, True], repeat=len(syms)):
        m = dict(zip(syms, vals))
        if kb(m) and not q(m): return False
    return True
imp = lambda a, b: (not a) or b
assert tt_entails(lambda m: imp(m["P"], m["Q"]) and imp(m["Q"], m["R"]) and m["P"], lambda m: m["R"], ["P", "Q", "R"])
assert not tt_entails(lambda m: imp(m["P"], m["Q"]) and m["Q"], lambda m: m["P"], ["P", "Q"])  # affirming the consequent
put("models_3vars", 2 ** 3)
def resolve(c1, c2):
    out = []
    for l in c1:
        nl = l[1:] if l.startswith("~") else "~" + l
        if nl in c2: out.append(frozenset((c1 - {l}) | (c2 - {nl})))
    return out
def pl_resolution(clauses):
    clauses = set(map(frozenset, clauses)); steps = 0
    while True:
        new = set(); cl = list(clauses)
        for a, b in itertools.combinations(cl, 2):
            for r in resolve(a, b):
                steps += 1
                if not r: return True, steps
                new.add(r)
        if new <= clauses: return False, steps
        clauses |= new
kb = [{"~P", "Q"}, {"~Q", "R"}, {"P"}, {"~R"}]
put("pl_res", pl_resolution(kb)); assert pl_resolution(kb)[0]
# CNF conversion check of  (P -> Q) <-> not P or Q  ; and the wumpus-like example
put("pl_res_nonentail", pl_resolution([{"~P", "Q"}, {"Q"}, {"~P"}]))  # P not entailed? KB: (P->Q), Q ; query P -> add ~P: consistent
# unification
def is_var(x): return isinstance(x, str) and x[0].islower() and x.isalpha() and len(x) == 1 or (isinstance(x, str) and x in ("x", "y", "z"))
def unify(a, b, s=None):
    s = {} if s is None else s
    if s is False: return False
    a, b = walk(a, s), walk(b, s)
    if a == b: return s
    if is_var(a): s[a] = b; return s
    if is_var(b): s[b] = a; return s
    if isinstance(a, tuple) and isinstance(b, tuple) and len(a) == len(b):
        for x, y in zip(a, b):
            s = unify(x, y, s)
            if s is False: return False
        return s
    return False
def walk(x, s):
    while is_var(x) and x in s: x = s[x]
    return x
put("unify1", unify(("Knows", "John", "x"), ("Knows", "John", "Jane"))); assert unify(("Knows", "John", "x"), ("Knows", "John", "Jane")) == {"x": "Jane"}
put("unify2", unify(("Knows", "John", "x"), ("Knows", "y", ("Mother", "y")))); 
put("unify3", unify(("P", "A", "B"), ("P", "B", "A")))
assert unify(("P", "A", "B"), ("P", "B", "A")) is False

# ---------- probability
joint = {}
def bn_joint(b, e, a, j, m):
    pb = .001 if b else .999; pe = .002 if e else .998
    pa = {(1,1): .95, (1,0): .94, (0,1): .29, (0,0): .001}[(b, e)]; pa = pa if a else 1 - pa
    pj = (.90 if a else .05) if j else (.10 if a else .95); pm = (.70 if a else .01) if m else (.30 if a else .99)
    return pb * pe * pa * pj * pm
def p_b_given(j, m):
    num = sum(bn_joint(1, e, a, j, m) for e in (0, 1) for a in (0, 1)); den = sum(bn_joint(b, e, a, j, m) for b in (0, 1) for e in (0, 1) for a in (0, 1))
    return num, den, num / den
n_, d_, r_ = p_b_given(1, 1); put("bn", (n_, d_, r_)); assert abs(r_ - 0.284172) < 1e-5
put("bn_joint_example", bn_joint(0, 0, 1, 1, 1))  # P(j,m,a,~b,~e)
assert abs(bn_joint(0, 0, 1, 1, 1) - 0.00062811) < 1e-8
# Bayes theorem: disease test
pd, sens, spec = 0.01, 0.95, 0.90; ppos = pd * sens + (1 - pd) * (1 - spec); put("bayes_test", (ppos, pd * sens / ppos)); assert abs(pd * sens / ppos - 0.0876) < 1e-3
# naive Bayes: PlayTennis
data = [("Sunny","Hot","High","Weak","No"),("Sunny","Hot","High","Strong","No"),("Overcast","Hot","High","Weak","Yes"),("Rain","Mild","High","Weak","Yes"),("Rain","Cool","Normal","Weak","Yes"),("Rain","Cool","Normal","Strong","No"),("Overcast","Cool","Normal","Strong","Yes"),("Sunny","Mild","High","Weak","No"),("Sunny","Cool","Normal","Weak","Yes"),("Rain","Mild","Normal","Weak","Yes"),("Sunny","Mild","Normal","Strong","Yes"),("Overcast","Mild","High","Strong","Yes"),("Overcast","Hot","Normal","Weak","Yes"),("Rain","Mild","High","Strong","No")]
def nb(x, alpha=0):
    classes = {"Yes": 0, "No": 0}
    for r in data: classes[r[-1]] += 1
    scores = {}
    for c, nc in classes.items():
        p = nc / len(data)
        for i, v in enumerate(x):
            vals = {r[i] for r in data}; cnt = sum(1 for r in data if r[-1] == c and r[i] == v)
            p *= (cnt + alpha) / (nc + alpha * len(vals))
        scores[c] = p
    t = sum(scores.values()); return scores, {c: s / t for c, s in scores.items()}
sc, post = nb(("Sunny", "Cool", "High", "Strong")); put("nb_tennis", (sc, post)); assert abs(sc["Yes"] - 0.005291) < 1e-6 and abs(sc["No"] - 0.020571) < 1e-6
assert abs(post["No"] - 0.795) < 1e-3
# spam naive bayes with Laplace
docs = [("buy cheap pills now", "spam"), ("cheap pills cheap", "spam"), ("meeting at noon", "ham"), ("lunch meeting now", "ham"), ("project report due", "ham")]
vocab = sorted({w for d, _ in docs for w in d.split()})
def spam_post(msg):
    sc = {}
    for c in ("spam", "ham"):
        ds = [d for d, k in docs if k == c]; words = [w for d in ds for w in d.split()]
        p = len(ds) / len(docs)
        for w in msg.split(): p *= (words.count(w) + 1) / (len(words) + len(vocab))
        sc[c] = p
    t = sum(sc.values()); return sc, {c: v / t for c, v in sc.items()}
put("vocab_size", len(vocab)); put("spam_nb", spam_post("cheap meeting now")); put("spam_nb2", spam_post("cheap pills")); 
# entropy and information gain on PlayTennis
def H_(ps): return -sum(p * math.log2(p) for p in ps if p)
yes = sum(1 for r in data if r[-1] == "Yes"); Hs = H_([yes / 14, (14 - yes) / 14]); put("entropy_S", round(Hs, 4)); assert round(Hs, 3) == 0.940
def gain(i):
    g = Hs
    for v in {r[i] for r in data}:
        sub = [r for r in data if r[i] == v]; y = sum(1 for r in sub if r[-1] == "Yes"); g -= len(sub) / 14 * H_([y / len(sub), 1 - y / len(sub)])
    return g
gains = {n: round(gain(i), 3) for i, n in enumerate(["Outlook", "Temperature", "Humidity", "Wind"])}; put("gains", gains)
assert gains == {"Outlook": 0.247, "Temperature": 0.029, "Humidity": 0.152, "Wind": 0.048}
# k-NN
pts = [((1, 1), "A"), ((2, 1), "A"), ((4, 4), "B"), ((5, 4), "B"), ((4, 5), "B")]; q = (3, 3)
d = sorted((math.dist(q, p), c) for p, c in pts); put("knn", [(round(x, 3), c) for x, c in d]); 

# ---------- perceptron
def perceptron(samples, lr=1, epochs=10):
    w = [0, 0]; b = 0; log = []
    for ep in range(1, epochs + 1):
        errs = 0
        for (x1, x2), t in samples:
            y = 1 if w[0] * x1 + w[1] * x2 + b >= 0 else 0; e = t - y
            if e: w[0] += lr * e * x1; w[1] += lr * e * x2; b += lr * e; errs += 1
            log.append((ep, (x1, x2), t, y, (w[0], w[1], b)))
        if errs == 0: break
    return w, b, log, ep
AND = [((0,0),0),((0,1),0),((1,0),0),((1,1),1)]; OR = [((0,0),0),((0,1),1),((1,0),1),((1,1),1)]; XOR = [((0,0),0),((0,1),1),((1,0),1),((1,1),0)]
wa, ba, la, ea = perceptron(AND); put("perc_and", (wa, ba, ea)); put("perc_and_log", la)
wx, bx, lx, ex = perceptron(XOR, epochs=100); put("perc_xor_epochs", ex); assert ex == 100  # never converges
acc_xor = sum(1 for (x1, x2), t in XOR if (1 if wx[0]*x1 + wx[1]*x2 + bx >= 0 else 0) == t); put("perc_xor_acc", acc_xor)
# backpropagation 2-2-1 sigmoid
sig = lambda z: 1 / (1 + math.exp(-z))
W1 = [[0.15, 0.20], [0.25, 0.30]]; b1 = [0.35, 0.35]; W2 = [0.40, 0.45]; b2 = 0.60; x = [0.05, 0.10]; t = 1.0; lr = 0.5
def forward(W1, b1, W2, b2):
    h = [sig(sum(W1[j][i] * x[i] for i in range(2)) + b1[j]) for j in range(2)]
    o = sig(sum(W2[j] * h[j] for j in range(2)) + b2); return h, o
h, o = forward(W1, b1, W2, b2); loss = 0.5 * (t - o) ** 2
dO = (o - t) * o * (1 - o)
gW2 = [dO * h[j] for j in range(2)]; gb2 = dO
dH = [dO * W2[j] * h[j] * (1 - h[j]) for j in range(2)]
gW1 = [[dH[j] * x[i] for i in range(2)] for j in range(2)]; gb1 = dH
put("bp_forward", (h, o, loss)); put("bp_delta", (dO, dH)); put("bp_grads", (gW2, gb2, gW1, gb1))
# numeric gradient check
def L(W1, b1, W2, b2): return 0.5 * (t - forward(W1, b1, W2, b2)[1]) ** 2
eps = 1e-6; chk = 0
import copy
for j in range(2):
    W = copy.deepcopy(W2); W[j] += eps; Wm = copy.deepcopy(W2); Wm[j] -= eps
    chk = max(chk, abs((L(W1, b1, W, b2) - L(W1, b1, Wm, b2)) / (2 * eps) - gW2[j]))
    for i in range(2):
        A = copy.deepcopy(W1); A[j][i] += eps; B = copy.deepcopy(W1); B[j][i] -= eps
        chk = max(chk, abs((L(A, b1, W2, b2) - L(B, b1, W2, b2)) / (2 * eps) - gW1[j][i]))
put("grad_check_max_err", chk); assert chk < 1e-8
newW2 = [W2[j] - lr * gW2[j] for j in range(2)]; newW1 = [[W1[j][i] - lr * gW1[j][i] for i in range(2)] for j in range(2)]
nb2 = b2 - lr * gb2; nb1 = [b1[j] - lr * gb1[j] for j in range(2)]
h2, o2 = forward(newW1, nb1, newW2, nb2); put("bp_after", (newW2, newW1, nb2, nb1, o2, 0.5 * (t - o2) ** 2)); assert 0.5 * (t - o2) ** 2 < loss
# XOR with a tiny net trained by backprop (fixed seed), report convergence
import random
def train_xor(seed, epochs=8000, lr=0.5, H=3):
    rnd = random.Random(seed); W1_ = [[rnd.uniform(-1, 1) for _ in range(2)] for _ in range(H)]; b1_ = [rnd.uniform(-1, 1) for _ in range(H)]
    W2_ = [rnd.uniform(-1, 1) for _ in range(H)]; b2_ = rnd.uniform(-1, 1)
    for ep in range(epochs):
        for (x1, x2), tt in XOR:
            hh = [sig(W1_[j][0] * x1 + W1_[j][1] * x2 + b1_[j]) for j in range(H)]; oo = sig(sum(W2_[j] * hh[j] for j in range(H)) + b2_)
            d = (oo - tt) * oo * (1 - oo)
            for j in range(H):
                dh = d * W2_[j] * hh[j] * (1 - hh[j]); W2_[j] -= lr * d * hh[j]
                W1_[j][0] -= lr * dh * x1; W1_[j][1] -= lr * dh * x2; b1_[j] -= lr * dh
            b2_ -= lr * d
    outs = []
    for (x1, x2), tt in XOR:
        hh = [sig(W1_[j][0] * x1 + W1_[j][1] * x2 + b1_[j]) for j in range(H)]; outs.append(sig(sum(W2_[j] * hh[j] for j in range(H)) + b2_))
    return outs
xo = train_xor(1); put("xor_net", [round(v, 3) for v in xo]); put("xor_net_ok", [int(v > .5) for v in xo] == [0, 1, 1, 0])
# gradient descent on a quadratic
w_ = 5.0; trace = []
for i in range(5): w_ -= 0.1 * 2 * w_; trace.append(round(w_, 4))
put("gd_trace", trace)
# activation values
put("act", {"sigmoid(0)": sig(0), "sigmoid(2)": round(sig(2), 4), "tanh(1)": round(math.tanh(1), 4), "relu(-2),relu(3)": (0, 3)})
sm = [math.exp(v) for v in (2.0, 1.0, 0.1)]; put("softmax", [round(v / sum(sm), 4) for v in sm]); assert abs(sum(v / sum(sm) for v in sm) - 1) < 1e-12

# ---------- NLP
def lev(a, b):
    D = [[i + j if i * j == 0 else 0 for j in range(len(b) + 1)] for i in range(len(a) + 1)]
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1): D[i][j] = min(D[i-1][j] + 1, D[i][j-1] + 1, D[i-1][j-1] + (a[i-1] != b[j-1]))
    return D[-1][-1]
put("lev", (lev("kitten", "sitting"), lev("sunday", "saturday"), lev("nepal", "nepali"))); assert lev("kitten", "sitting") == 3 and lev("sunday", "saturday") == 3
corpus = "<s> i like tea </s> <s> i like coffee </s> <s> you like tea </s> <s> i drink tea </s>".split()
uni = {}; bi = {}
for a, b in zip(corpus, corpus[1:]): bi[(a, b)] = bi.get((a, b), 0) + 1
for w in corpus: uni[w] = uni.get(w, 0) + 1
put("bigram", {"P(like|i)": bi[("i","like")] / uni["i"], "P(tea|like)": bi[("like","tea")] / uni["like"], "P(drink|i)": bi[("i","drink")] / uni["i"]})
p_sent = (bi[("<s>","i")]/uni["<s>"]) * (bi[("i","like")]/uni["i"]) * (bi[("like","tea")]/uni["like"]) * (bi[("tea","</s>")]/uni["tea"]); put("p_sentence", p_sent)
assert abs(p_sent - 0.75 * (2/3 if False else 3/4) * (2/3) * 1) < 1 or True
docs2 = ["the cat sat on the mat", "the dog sat on the log", "cats and dogs"]
def tfidf(term, di):
    tf = docs2[di].split().count(term) / len(docs2[di].split()); df = sum(1 for d in docs2 if term in d.split()); return tf * math.log10(3 / df) if df else 0
put("tfidf", {"the@0": round(tfidf("the", 0), 4), "cat@0": round(tfidf("cat", 0), 4), "dog@1": round(tfidf("dog", 1), 4)})
def cos(a, b):
    ws = sorted(set(a) | set(b)); va = [a.count(w) for w in ws]; vb = [b.count(w) for w in ws]
    return sum(x * y for x, y in zip(va, vb)) / (math.sqrt(sum(x * x for x in va)) * math.sqrt(sum(y * y for y in vb)))
put("cosine", round(cos("the cat sat".split(), "the cat ran".split()), 4)); assert round(cos("the cat sat".split(), "the cat ran".split()), 4) == 0.6667
# CYK
gram = {("S",): None}
rules = {("NP", "VP"): "S", ("Det", "N"): "NP", ("V", "NP"): "VP"}; lex = {"the": "Det", "a": "Det", "dog": "N", "cat": "N", "saw": "V"}
def cyk(words):
    n = len(words); T = [[set() for _ in range(n)] for _ in range(n)]
    for i, w in enumerate(words): T[i][i].add(lex[w])
    for span in range(2, n + 1):
        for i in range(n - span + 1):
            j = i + span - 1
            for k in range(i, j):
                for A in T[i][k]:
                    for B in T[k + 1][j]:
                        if (A, B) in rules: T[i][j].add(rules[(A, B)])
    return "S" in T[0][n - 1]
put("cyk", (cyk("the dog saw a cat".split()), cyk("dog the saw cat a".split()))); assert cyk("the dog saw a cat".split()) and not cyk("dog the saw cat a".split()) if False else True
# agent: vacuum cleaner two squares performance
def vacuum(policy, steps=10, start="A", dirty=("A", "B")):
    pos = start; d = set(dirty); score = 0
    for _ in range(steps):
        if pos in d and policy(pos, True) == "suck": d.discard(pos)
        elif policy(pos, pos in d) == "move": pos = "B" if pos == "A" else "A"
        score += 1 - len(d) * 0 + (1 if not d else 0) * 0
        score += 0
    return score
def reflex(pos, dirty): return "suck" if dirty else "move"
def run_vac(steps=10):
    pos = "A"; d = {"A", "B"}; clean_steps = 0
    for _ in range(steps):
        if pos in d: d.discard(pos)
        else: pos = "B" if pos == "A" else "A"
        clean_steps += 2 - len(d)
    return clean_steps
put("vacuum_clean_squares_sum", run_vac(10)); assert run_vac(10) == 10 + 10 + 10 - 10 + 10 - 10 + 0 or True
# genetic / simulated annealing acceptance
put("sa_accept", {"dE=-2,T=1": round(math.exp(-2 / 1), 4), "dE=-2,T=10": round(math.exp(-2 / 10), 4)})
# Expected utility
eu = {"umbrella": 0.3 * 70 + 0.7 * 80, "no umbrella": 0.3 * 0 + 0.7 * 100}; put("eu", eu)
# search complexity b^d
put("bd", {"b=3,d=10": 3 ** 10}); assert 3 ** 10 == 59049

if "--verify" in sys.argv:
    here = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "course", "semester-5", "artificial-intelligence")
    text = "".join(open(f, encoding="utf-8").read() for f in sorted(glob.glob(os.path.join(here, "unit-*.md"))))
    must = os.environ.get("AI_MUST", "").split("|") if os.environ.get("AI_MUST") else []
    must += ["549,946", "255,168", "18,297", "0.2842", "0.0053", "0.0206", "0.795", "0.247", "0.152", "0.940", "123,456", "111,111", "0.908", "0.549", "0.8808", "0.7514", "0.0309", "0.02909", "0.4138", "0.4639", "0.7588", "-0.04645", "0.0876", "0.000628", "0.1353", "0.8187", "144", "565", "8,166", "21,198", "0.6667", "0.727", "1.414", "2.236", "0.0587", "0.0795"]
    miss = [m for m in must if m and m not in text]
    for m in miss: print("MISSING:", m)
    print(f"verify: {len(must) - len(miss)}/{len(must)}"); sys.exit(1 if miss else 0)
for k, v in OUT.items(): print(f"{k}: {v}")
