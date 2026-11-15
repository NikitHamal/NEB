"""Writes ioe-enct251-2082-bhadra.md (Discrete Structure, BEI II/II, regular).  python3 gen_ds2.py <outdir>"""
import sys, os, re, itertools, heapq
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else "."
src = open(os.path.join(HERE, "gen_ds.py")).read()
s0 = src.index("HELP = "); s1 = src.index("\n\nFIG_NFA")
HELP = eval(src[s0 + 7:s1])

# ---------- computations ----------
# Q2 validity by brute force
ok = all((not ((not p or q) and (p or r) and (not r or s))) or (q or s) for p, q, r, s in itertools.product([0, 1], repeat=4))
assert ok
# Q4 validity
assert all((not ((not a or b) and (a or c) and (not c or d))) or (b or d) for a, b, c, d in itertools.product([0, 1], repeat=4))
# Q5 DFA
D5 = {("q0", "a"): "q1", ("q0", "b"): "T", ("q1", "a"): "T", ("q1", "b"): "q2", ("q2", "a"): "X", ("q2", "b"): "T", ("T", "a"): "T", ("T", "b"): "T", ("X", "a"): "X", ("X", "b"): "X"}
def run(w):
    q = "q0"; tr = [q]
    for ch in w: q = D5[(q, ch)]; tr.append(q)
    return tr
for n in range(0, 9):
    for w in map("".join, itertools.product("ab", repeat=n)):
        assert (run(w)[-1] != "X") == (not w.startswith("aba")), w
w1, w2 = "abbabab", "abaabaaab"
t1, t2 = run(w1), run(w2); assert t1[-1] == "T" and t2[-1] == "X"
# Q6 regex
rx = re.compile(r"^(0|10)*(1)?$")
for n in range(0, 13):
    for w in map("".join, itertools.product("01", repeat=n)):
        assert bool(rx.match(w)) == ("11" not in w), w
# Q9 bubble sort
def bubble(a):
    a = a[:]; rows = []
    for p in range(len(a) - 1):
        sw = 0
        for j in range(len(a) - 1 - p):
            if a[j] > a[j + 1]: a[j], a[j + 1] = a[j + 1], a[j]; sw += 1
        rows.append((p + 1, a[:], sw))
        if sw == 0: break
    return rows
BS = bubble([67, 45, 54, 2, 29])
assert BS[-1][1] == [2, 29, 45, 54, 67]
bs_md = "| Pass | Array after the pass | Swaps |\n|---|---|---|\n| initial | 67, 45, 54, 2, 29 | - |\n" + "\n".join("| %d | %s | %d |" % (p, ", ".join(map(str, a)), s) for p, a, s in BS) + "\n"
# Q12 Kruskal
KE = [("S", "B", 4), ("S", "C", 10), ("B", "C", 3), ("B", "D", 5), ("C", "D", 6), ("D", "F", 6), ("E", "F", 8), ("C", "E", 9), ("E", "G", 5), ("F", "G", 2), ("F", "H", 7), ("G", "H", 4), ("C", "K", 7), ("E", "K", 14), ("G", "K", 1)]
par = {}
def find(x):
    par.setdefault(x, x)
    while par[x] != x: par[x] = par[par[x]]; x = par[x]
    return x
kt = []; mst = []; tot = 0
for i, (u, v, w) in enumerate(sorted(KE, key=lambda e: (e[2], e[0] + e[1])), 1):
    if find(u) != find(v): par[find(u)] = find(v); mst.append((u, v)); tot += w; kt.append("| %d | %s%s | %d | **accept** |" % (i, u, v, w))
    else: kt.append("| %d | %s%s | %d | reject (forms a cycle) |" % (i, u, v, w))
assert tot == 30 and len(mst) == 8
kruskal_md = "| # | Edge | Weight | Decision |\n|---|---|---|---|\n" + "\n".join(kt) + "\n"
# Q13 Dijkstra
DE = [("A", "B", 8), ("A", "C", 2), ("B", "C", 3), ("B", "D", 5), ("C", "D", 9), ("C", "E", 8), ("D", "F", 3), ("E", "F", 8), ("E", "G", 12), ("F", "G", 6), ("F", "H", 7), ("G", "H", 4)]
adj = {}
for u, v, w in DE: adj.setdefault(u, []).append((v, w)); adj.setdefault(v, []).append((u, w))
dist = {v: 1e9 for v in adj}; dist["A"] = 0; prev = {}; done = []; rows = []
V = sorted(adj)
while len(done) < len(V):
    u = min((v for v in V if v not in done), key=lambda v: dist[v]); done.append(u)
    for v, w in adj[u]:
        if v not in done and dist[u] + w < dist[v]: dist[v] = dist[u] + w; prev[v] = u
    rows.append("| %d | %s | %s | %s |" % (len(done), u, "{" + ", ".join(done) + "}", ", ".join("%s=%s" % (v, "∞" if dist[v] >= 1e9 else dist[v]) for v in V if v not in done)))
def path(v):
    p = [v]
    while p[-1] in prev: p.append(prev[p[-1]])
    return "-".join(reversed(p))
assert dist == {"A": 0, "C": 2, "B": 5, "D": 10, "E": 10, "F": 13, "G": 19, "H": 20}
dij_md = "| Step | Vertex made permanent | Permanent set | Tentative labels of the rest |\n|---|---|---|---|\n" + "\n".join(rows) + "\n"
res_md = "| Vertex | A | B | C | D | E | F | G | H |\n|---|---|---|---|---|---|---|---|---|\n| d(A, v) | " + " | ".join(str(dist[v]) for v in "ABCDEFGH") + " |\n| Path | A | " + " | ".join(path(v) for v in "BCDEFGH") + " |\n"
PREV = repr(prev)

# ---------- figures ----------
def fig(caption, code):
    return '```figure caption="%s"\n%s```\n' % (caption, code)

FIG_Q6 = fig("The given automaton: start state A, accepting states A and B (double circles), dead state C.", HELP + r'''fig,ax=plt.subplots(figsize=(5.2,2.0)); ax.axis("off"); ax.set_xlim(-1.4,8.6); ax.set_ylim(-1.6,1.9); ax.set_aspect("equal")
A=(0,0);B=(3.4,0);C=(6.8,0)
N(ax,A,"A",fin=True,st=True); N(ax,B,"B",fin=True); N(ax,C,"C")
E(ax,A,B,"1"); E(ax,B,C,"1"); E(ax,B,A,"0",rad=-0.55,dl=(0,-0.1)); L(ax,A,"0"); L(ax,C,"0, 1")
''')
FIG_DFA5 = fig("DFA for strings over {a, b} that do not start with aba (q0, q1, q2, T accepting; X is the dead state reached after the prefix aba).", HELP + r'''fig,ax=plt.subplots(figsize=(6.4,2.6)); ax.axis("off"); ax.set_xlim(-1.4,10.6); ax.set_ylim(-2.4,3.6); ax.set_aspect("equal")
q0=(0,1);q1=(2.8,2.4);q2=(5.6,2.4);X=(8.4,2.4);T=(4.2,-0.9)
N(ax,q0,"q0",fin=True,st=True); N(ax,q1,"q1",fin=True); N(ax,q2,"q2",fin=True); N(ax,X,"X"); N(ax,T,"T",fin=True)
E(ax,q0,q1,"a"); E(ax,q1,q2,"b"); E(ax,q2,X,"a"); E(ax,q0,T,"b"); E(ax,q1,T,"a",dl=(-0.35,0)); E(ax,q2,T,"b",dl=(0.35,0)); L(ax,X,"a, b"); L(ax,T,"a, b")
''')
FIG_TREE = fig("Derivation (parse) tree of w = 000111111 for S -> 0S11 | 011.", r'''fig,ax=plt.subplots(figsize=(4.4,3.4)); ax.axis("off"); ax.set_xlim(-3.6,3.6); ax.set_ylim(-5.4,0.8)
def node(x,y,t,c=INK,b=False): ax.text(x,y,t,ha="center",va="center",fontsize=10,color=c,fontweight="bold" if b else "normal")
def ln(x1,y1,x2,y2): ax.plot([x1,x2],[y1,y2],color=INK,lw=1)
# redraw: the middle child of each level is the next S; place last S with children 0 1 1
ax.clear(); ax.axis("off"); ax.set_xlim(-3.6,3.6); ax.set_ylim(-5.6,0.8)
lv=[0,-1.7,-3.4]
for k,yy in enumerate(lv):
    node(0,yy,"S",ACCENT,True)
    kids=[(-1.5,"0"),(0,"S"),(1.0,"1"),(1.8,"1")] if k<2 else [(-1.2,"0"),(0,"1"),(1.2,"1")]
    for dx,t in kids:
        ln(0,yy-0.2,dx,yy-1.45); node(dx,yy-1.7,t,ACCENT if t=="S" else INK,t=="S")
for t,yy in zip(["S => 0S11","=> 00S1111","=> 000111111"],[0,-1.7,-3.4]): ax.text(2.4,yy,t,fontsize=7.5,va="center")
ax.set_xlim(-2.2,4.8)
''')
FIG_CUBE = fig("The 3-dimensional hypercube Q3: 8 vertices (3-bit strings), 12 edges (vertices adjacent when they differ in exactly one bit).", r'''fig,ax=plt.subplots(figsize=(3.4,3.2)); ax.axis("off"); ax.set_aspect("equal")
P={}
for i,b in enumerate(["000","100","110","010"]): P[b]=[(0,0),(2,0),(2,2),(0,2)][i]
for i,b in enumerate(["001","101","111","011"]): P[b]=[(0.9,0.8),(2.9,0.8),(2.9,2.8),(0.9,2.8)][i]
for a in P:
    for b in P:
        if a<b and sum(x!=y for x,y in zip(a,b))==1:
            back=(a[2]=="1" or b[2]=="1") and False
            ax.plot([P[a][0],P[b][0]],[P[a][1],P[b][1]],color=INK,lw=1.3,zorder=1)
for k,p in P.items():
    ax.scatter([p[0]],[p[1]],s=520,color="white",edgecolor=INK,zorder=3); ax.text(p[0],p[1],k,ha="center",va="center",fontsize=7,zorder=4)
ax.set_xlim(-0.6,3.5); ax.set_ylim(-0.6,3.4)
''')
def graph_fig(caption, edges, pos, hl=(), w=5.6, h=3.0, xl=(-0.8,9.0), yl=(-0.8,4.6), dashed=()):
    code = "E=%r\nM=%r\nDASH=%r\nP=%r\n" % (edges, [tuple(x) for x in hl], list(dashed), pos) + r'''fig,ax=plt.subplots(figsize=(%s,%s)); ax.axis("off"); ax.set_aspect("equal")
def inM(u,v): return (u,v) in M or (v,u) in M
for u,v,w in E:
    t=inM(u,v)
    ax.plot([P[u][0],P[v][0]],[P[u][1],P[v][1]],color=ACCENT if t else "#9aa",lw=3.0 if t else 1.1,zorder=1)
    mx,my=(P[u][0]+P[v][0])/2,(P[u][1]+P[v][1])/2
    ax.text(mx,my,str(w),fontsize=8,ha="center",va="center",bbox=dict(fc="white",ec="none",pad=0.6),zorder=4,color="#b00020" if t else INK)
for u,v in DASH:
    ax.plot([P[u][0],P[v][0]],[P[u][1],P[v][1]],color="#9aa",lw=1.1,ls="--",zorder=1)
    ax.text((P[u][0]+P[v][0])/2,(P[u][1]+P[v][1])/2,"?",fontsize=8,ha="center",va="center",bbox=dict(fc="white",ec="none",pad=0.6),zorder=4)
for k,p in P.items(): ax.scatter([p[0]],[p[1]],s=330,color="white",edgecolor=INK,zorder=3); ax.text(p[0],p[1],k,ha="center",va="center",fontsize=9,zorder=5)
ax.set_xlim%r; ax.set_ylim%r
''' % (w, h, xl, yl)
    return fig(caption, code)
KP = {"S": (0, 2.0), "B": (2, 3.4), "C": (2, 1.6), "D": (4.4, 3.4), "E": (4.4, 1.7), "F": (6.6, 3.4), "G": (6.6, 1.7), "H": (8.6, 2.6), "K": (4.4, 0)}
FIG_KQ = graph_fig("The graph of Question 12 (the weight of the vertical edge DE is not printed on the scan, drawn dashed).", KE, KP, dashed=[("D", "E")], yl=(-0.8, 4.2))
FIG_KS = graph_fig("Minimum spanning tree by Kruskal's algorithm (thick edges, total weight 30).", KE, KP, hl=mst, dashed=[("D", "E")], yl=(-0.8, 4.2))
DP = {"A": (0, 1.0), "B": (2, 2.3), "C": (2, 0), "D": (4.4, 2.3), "E": (4.4, 0), "F": (6.6, 2.3), "G": (6.6, 0), "H": (8.6, 1.2)}
FIG_DQ = graph_fig("The graph of Question 13.", DE, DP, yl=(-0.8, 3.2), h=2.6)
FIG_DS = graph_fig("Shortest-path tree from A (thick edges): d = 2, 5, 10, 10, 13, 19, 20 for C, B, D, E, F, G, H.", DE, DP, hl=[(v, u) for v, u in prev.items()], yl=(-0.8, 3.2), h=2.6)
FIG_TAB = fig("Semantic tableau for the hypotheses A->B, ~A->C, C->D and the negated conclusion ~(~B->D): every branch closes (x).", r'''fig,ax=plt.subplots(figsize=(5.6,4.4)); ax.axis("off"); ax.set_xlim(-3.4,3.6); ax.set_ylim(-9.2,0.8)
def t(x,y,s,c=INK,ha="center"): ax.text(x,y,s,ha=ha,va="center",fontsize=8,color=c)
def ln(a,b): ax.plot([a[0],b[0]],[a[1],b[1]],color=INK,lw=1)
L=[(0,0,"1. A -> B   (given)"),(0,-0.7,"2. ~A -> C   (given)"),(0,-1.4,"3. C -> D   (given)"),(0,-2.1,"4. ~(~B -> D)   (negated conclusion)"),(0,-2.8,"5. ~B   (from 4)"),(0,-3.5,"6. ~D   (from 4)")]
for x,y,s in L: t(x,y,s)
ln((0,-3.8),(-1.6,-4.7)); ln((0,-3.8),(1.6,-4.7))
t(-1.6,-5.0,"~A   (from 1)"); t(1.6,-5.0,"B   (from 1)"); t(1.6,-5.6,"x  contradicts 5",ACCENT)
ln((-1.6,-5.3),(-2.6,-6.2)); ln((-1.6,-5.3),(-0.6,-6.2))
t(-2.6,-6.5,"A   (from 2)"); t(-2.6,-7.1,"x  contradicts ~A",ACCENT); t(-0.6,-6.5,"C   (from 2)")
ln((-0.6,-6.8),(-1.6,-7.7)); ln((-0.6,-6.8),(0.4,-7.7))
t(-1.6,-8.0,"~C   (from 3)"); t(-1.6,-8.6,"x  contradicts C",ACCENT); t(0.4,-8.0,"D   (from 3)"); t(0.4,-8.6,"x  contradicts 6",ACCENT)
''')

# ---------- paper ----------
d = r'''---
file: NEBians-IOE-Past-Paper-Discrete-Structure-ENCT251-2082-Bhadra.pdf
subject: Discrete Structure
level: BE · Year II / Part II
code: ENCT 251
year_bs: 2082 Bhadra
cal: BS
year_ad: 2025
stream: BEI
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular (New Course). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
Explain different types of function. State the converse, contrapositive and inverse of the conditional statement "My insurance company will pay me money only if the flood destroys my house or the fire destroys my house." [[3+2]]

@q 2
Define the term counter example and witness with example. Using rules of inferences, show that the hypotheses "If you send me an e-mail message, then I will finish writing the program," "If you do not send me an e-mail message, then I will go to sleep early," and "If I go to sleep early, then I will wake up feeling refreshed" lead to the conclusion "If I do not finish writing the program, then I will wake up feeling refreshed." You are required to show each step and give reasons for those steps before you come to the desired conclusion from the hypothesis. [[2+3]]

@q 3
Use the Principle of Mathematical Induction to verify that, for any positive integer $n$, $n^{3}+2n$ is divisible by 3. [[3]]

@q 4
Check validity of the given statement using method of tableaux: $A \to B$, $\neg A \to C$, $C \to D$; hence $\neg B \to D$. [[4]]

@q 5
Give formal definition of DFA. Design a deterministic finite automata that accepts all the strings that does not starts with aba over $\Sigma = \{a, b\}$. Also check for string $w_1$ = abbabab and $w_2$ = abaabaaab is accepted or rejected. [[2+5]]

@q 6
Derive the regular expression for the given automata. [[4]]

''' + FIG_Q6 + r'''
@q 7
Write the CFG for the language $L: 0^{n}1^{2n}$ for $n \ge 1$. Also generate the string $w = 000111111$ and draw its derivation tree. [[3]]

@q 8
Derive the explicit formula for the Fibonacci series using recurrence relation. [[4]]

@q 9
Derive the worst-case time complexity for binary search algorithm. Sort the given data using bubble sort 67, 45, 54, 2, 29. [[2+2]]

@q 10
Define wheel graph. Draw 3-dimensional hypercube ($Q_3$). Show that the total number of edges in any complete graph is $\dfrac{n(n-1)}{2}$. [[1+1+3]]

@q 11
State and prove Euler's Formula for planar graph. [[4]]

@q 12
What are saturated edges? State Max-Cut Min Flow theorem. Find the minimum spanning tree using Kruskal's algorithm from the graph given below. [[1+2+4]]

''' + FIG_KQ + r'''
@q 13
Find the shortest distance from vertex A to all other vertex using Dijkstra's algorithm. [[5]]

''' + FIG_DQ + r'''
<!-- SOLUTIONS -->

@s 1
**Types of function.** A function $f : A \to B$ assigns to every element $a \in A$ exactly one element $f(a) \in B$.

| Type | Definition | Example |
|---|---|---|
| One-to-one (injective) | $f(a_1) = f(a_2) \Rightarrow a_1 = a_2$ | $f(x) = 2x + 1$ on $\mathbb{R}$ |
| Onto (surjective) | every $b \in B$ is $f(a)$ for some $a$ (range = codomain) | $f(x) = x^{3}$ from $\mathbb{R}$ to $\mathbb{R}$ |
| One-to-one correspondence (bijective) | both injective and onto; only these have an inverse | $f(x) = x + 5$ on $\mathbb{Z}$ |
| Into function | range is a proper subset of the codomain | $f(x) = x^{2}$ from $\mathbb{R}$ to $\mathbb{R}$ |
| Constant function | $f(x) = c$ for all $x$ | $f(x) = 7$ |
| Identity function | $I_A(x) = x$ | $I_{\mathbb{Z}}$ |
| Inverse function | $f^{-1}(b) = a \iff f(a) = b$, exists iff $f$ is bijective | $f(x) = 2x \Rightarrow f^{-1}(x) = x/2$ |
| Composite function | $(g \circ f)(x) = g(f(x))$ | $f(x) = x + 1$, $g(x) = x^{2}$: $(g \circ f)(x) = (x+1)^{2}$ |
| Floor / ceiling | $\lfloor x \rfloor$ largest integer $\le x$, $\lceil x \rceil$ smallest integer $\ge x$ | $\lfloor 3.7 \rfloor = 3$, $\lceil 3.2 \rceil = 4$ |

**Translating the statement.** Let $p$: "my insurance company will pay me money", $f$: "the flood destroys my house", $r$: "the fire destroys my house". "$p$ only if ($f$ or $r$)" means payment can happen only when a disaster happened, so

$$p \to (f \vee r)$$

| Form | Symbolic | In words |
|---|---|---|
| Converse | $(f \vee r) \to p$ | If the flood destroys my house or the fire destroys my house, then my insurance company will pay me money. |
| Inverse | $\neg p \to \neg (f \vee r)$, i.e. $\neg p \to (\neg f \wedge \neg r)$ | If my insurance company does not pay me money, then neither the flood nor the fire destroys my house. |
| Contrapositive | $\neg (f \vee r) \to \neg p$, i.e. $(\neg f \wedge \neg r) \to \neg p$ | If neither the flood nor the fire destroys my house, then my insurance company will not pay me money. |

The contrapositive is logically equivalent to the original statement; the converse and the inverse are equivalent to each other (but not to the original).

@s 2
**Counter example.** To disprove $\forall x\, P(x)$ it is enough to find one element $c$ in the domain for which $P(c)$ is false; $c$ is the counter example. Example: for $P(x)$: "$x^{2} > x$" over the reals, $x = 1$ (or $x = \tfrac12$) is a counter example, so $\forall x\,(x^{2} > x)$ is false.

**Witness.** To prove $\exists x\, P(x)$ it is enough to exhibit one element $c$ with $P(c)$ true; $c$ is the witness (an existence proof). Example: for $P(x)$: "$x^{2} = 2$" over the reals, $x = \sqrt{2}$ is a witness, so $\exists x\, (x^{2} = 2)$ is true.

**The argument.** Let $p$: you send me an e-mail message, $q$: I finish writing the program, $r$: I go to sleep early, $s$: I wake up feeling refreshed.

Hypotheses: $p \to q$, $\ \neg p \to r$, $\ r \to s$. Conclusion: $\neg q \to s$.

| Step | Statement | Reason |
|---|---|---|
| 1 | $p \to q$ | Hypothesis |
| 2 | $\neg q \to \neg p$ | Contrapositive of step 1 |
| 3 | $\neg p \to r$ | Hypothesis |
| 4 | $\neg q \to r$ | Hypothetical syllogism on steps 2 and 3 |
| 5 | $r \to s$ | Hypothesis |
| 6 | $\neg q \to s$ | Hypothetical syllogism on steps 4 and 5 |

Step 6 is "If I do not finish writing the program, then I will wake up feeling refreshed", the required conclusion. $\blacksquare$ (A check of all 16 truth assignments of $p, q, r, s$ confirms that no assignment makes all three hypotheses true and the conclusion false.)

@s 3
Let $P(n)$: $3 \mid n^{3} + 2n$.

**Basis step** ($n = 1$): $1 + 2 = 3$, divisible by 3, so $P(1)$ is true.

**Inductive hypothesis:** assume $P(k)$ for some $k \ge 1$, i.e. $k^{3} + 2k = 3m$ for some integer $m$.

**Inductive step:**

$$(k+1)^{3} + 2(k+1) = k^{3} + 3k^{2} + 3k + 1 + 2k + 2 = (k^{3} + 2k) + 3(k^{2} + k + 1)$$

The first bracket equals $3m$ by hypothesis and the second term has the factor 3, so

$$(k+1)^{3} + 2(k+1) = 3\,(m + k^{2} + k + 1)$$

is divisible by 3, i.e. $P(k+1)$ is true.

By the principle of mathematical induction, $n^{3} + 2n$ is divisible by 3 for every positive integer $n$. $\blacksquare$

@s 4
**Method of tableaux (refutation).** The argument is valid exactly when the hypotheses together with the **negation of the conclusion** give a contradiction on every branch.

Negated conclusion: $\neg(\neg B \to D) \equiv \neg B \wedge \neg D$.

''' + FIG_TAB + r'''
1. From $A \to B \equiv \neg A \vee B$ the tableau splits into the branches $\neg A$ and $B$.
2. Branch $B$ contradicts $\neg B$ (closed).
3. In branch $\neg A$, the premise $\neg A \to C \equiv A \vee C$ splits into $A$ and $C$. Branch $A$ contradicts $\neg A$ (closed).
4. In branch $C$, the premise $C \to D \equiv \neg C \vee D$ splits into $\neg C$ and $D$. Branch $\neg C$ contradicts $C$; branch $D$ contradicts $\neg D$ (both closed).

Every branch is closed, so the premises cannot be true while $\neg B \to D$ is false.

$$\boxed{\,\text{The argument is valid: } A \to B,\ \neg A \to C,\ C \to D \ \therefore\ \neg B \to D\,}$$

(Direct check: $\neg B \Rightarrow \neg A$ by contraposition of $A \to B$, then $C$ by $\neg A \to C$, then $D$ by $C \to D$.)

@s 5
**Formal definition of a DFA.** A deterministic finite automaton is a 5-tuple $M = (Q, \Sigma, \delta, q_0, F)$ where

- $Q$ is a finite, non-empty set of states,
- $\Sigma$ is a finite input alphabet,
- $\delta : Q \times \Sigma \to Q$ is the transition function (exactly one next state for every state and symbol),
- $q_0 \in Q$ is the start state,
- $F \subseteq Q$ is the set of accepting (final) states.

A string $w$ is accepted if $\hat\delta(q_0, w) \in F$.

**Design.** The language is $L = \{w \in \{a,b\}^{*} : w \text{ does not start with } aba\}$. Track how much of the forbidden prefix $aba$ has been read:

- $q_0$: nothing read yet (the empty string does not start with $aba$, so it is accepted),
- $q_1$: the prefix read so far is $a$,
- $q_2$: the prefix read so far is $ab$,
- $X$: the prefix $aba$ has been read, a **dead** (non-accepting) state,
- $T$: the string has already departed from $aba$ (it started with $b$, $aa$ or $abb$) and can never start with $aba$, an accepting trap state.

| $\delta$ | $a$ | $b$ |
|---|---|---|
| $\to q_0$ (final) | $q_1$ | $T$ |
| $q_1$ (final) | $T$ | $q_2$ |
| $q_2$ (final) | $X$ | $T$ |
| $T$ (final) | $T$ | $T$ |
| $X$ | $X$ | $X$ |

$M = (\{q_0, q_1, q_2, T, X\}, \{a, b\}, \delta, q_0, \{q_0, q_1, q_2, T\})$.

''' + FIG_DFA5 + r'''
(The automaton was checked by computer against the definition "does not begin with aba" for every string up to length 8.)

**Test of $w_1$ = abbabab:**

$$q_0 \xrightarrow{a} q_1 \xrightarrow{b} q_2 \xrightarrow{b} T \xrightarrow{a} T \xrightarrow{b} T \xrightarrow{a} T \xrightarrow{b} T$$

The final state $T$ is accepting, so $w_1$ is **accepted** (it starts with $abb$, not $aba$).

**Test of $w_2$ = abaabaaab:**

$$q_0 \xrightarrow{a} q_1 \xrightarrow{b} q_2 \xrightarrow{a} X \xrightarrow{a} X \xrightarrow{b} X \xrightarrow{a} X \xrightarrow{a} X \xrightarrow{a} X \xrightarrow{b} X$$

The final state $X$ is not accepting, so $w_2$ is **rejected** (it starts with $aba$).

$$\boxed{\,w_1 = abbabab \text{ is accepted;}\quad w_2 = abaabaaab \text{ is rejected}\,}$$

@s 6
Reading the automaton: states $A$ (start, accepting) and $B$ (accepting), dead state $C$. Transitions: $A \xrightarrow{0} A$, $A \xrightarrow{1} B$, $B \xrightarrow{0} A$, $B \xrightarrow{1} C$, $C \xrightarrow{0,1} C$.

**State equations** ($q_X$ = the set of strings that take the machine from the start to $X$):

$$q_A = \varepsilon + q_A\,0 + q_B\,0, \qquad q_B = q_A\,1, \qquad q_C = q_B\,1 + q_C(0 + 1)$$

Substitute $q_B = q_A 1$ in the first equation:

$$q_A = \varepsilon + q_A\,0 + q_A\,10 = \varepsilon + q_A\,(0 + 10)$$

By Arden's theorem ($R = Q + RP \Rightarrow R = QP^{*}$) with $Q = \varepsilon$, $P = 0 + 10$:

$$q_A = (0 + 10)^{*}, \qquad q_B = (0 + 10)^{*}\,1$$

The accepting states are $A$ and $B$, so the language is the union

$$\boxed{\,r = (0 + 10)^{*} + (0 + 10)^{*}1 = (0 + 10)^{*}(\varepsilon + 1)\,}$$

**Meaning:** the machine accepts exactly the binary strings that do **not contain two consecutive 1s** (a second 1 straight after a 1 sends it to the dead state $C$). Every 1 is followed by a 0 (block $10$) except possibly the last symbol. This was verified by computer on all strings of length up to 12.

@s 7
**Grammar.** Each $0$ must be matched by exactly two $1$s, so generate a $0$ on the left and two $1$s on the right in each step: $G = (\{S\}, \{0, 1\}, P, S)$ with

$$S \to 0S11 \ \mid\ 011$$

The base production $S \to 011$ gives $n = 1$ and each use of $S \to 0S11$ increases $n$ by one, so $L(G) = \{0^{n}1^{2n} : n \ge 1\}$.

**Derivation of $w = 000111111$** ($n = 3$, three 0s and six 1s): use $S \to 0S11$ twice and then $S \to 011$:

$$S \Rightarrow 0S11 \Rightarrow 00S1111 \Rightarrow 00\,011\,1111 = 000111111$$

''' + FIG_TREE + r'''
Reading the leaves of the tree from left to right gives $0,0,0,1,1,1,1,1,1 = 000111111$.

@s 8
**Recurrence.** The Fibonacci numbers satisfy

$$F_n = F_{n-1} + F_{n-2} \quad (n \ge 2), \qquad F_0 = 0,\ F_1 = 1$$

This is a linear homogeneous recurrence of order 2 with constant coefficients. Try $F_n = r^{n}$:

$$r^{n} = r^{n-1} + r^{n-2}$$

Dividing by $r^{n-2}$ gives the characteristic equation

$$r^{2} - r - 1 = 0$$

$$r = \frac{1 \pm \sqrt{5}}{2}$$

Let $\varphi = \dfrac{1+\sqrt5}{2}$ (golden ratio) and $\psi = \dfrac{1-\sqrt5}{2}$. The roots are distinct, so the general solution is

$$F_n = \alpha\,\varphi^{n} + \beta\,\psi^{n}$$

**Initial conditions:**

$$F_0 = \alpha + \beta = 0 \quad\text{so}\quad \beta = -\alpha$$

$$F_1 = \alpha\varphi + \beta\psi = \alpha(\varphi - \psi) = \alpha\sqrt5 = 1$$

$$\text{hence}\quad \alpha = \frac{1}{\sqrt5},\quad \beta = -\frac{1}{\sqrt5}$$

$$\boxed{\,F_n = \frac{1}{\sqrt5}\left[\left(\frac{1+\sqrt5}{2}\right)^{n} - \left(\frac{1-\sqrt5}{2}\right)^{n}\right]\,}$$

(Binet's formula.) **Check:** $F_2 = \dfrac{\varphi^{2} - \psi^{2}}{\sqrt5} = \dfrac{(\varphi - \psi)(\varphi + \psi)}{\sqrt5} = \dfrac{\sqrt5 \cdot 1}{\sqrt5} = 1$ and $F_5 = 5$. Since $|\psi| < 1$, $F_n$ is the integer nearest to $\varphi^{n}/\sqrt5$.

@s 9
**Worst-case complexity of binary search.** Binary search looks at the middle element of a sorted list of $n$ elements and discards one half. The worst case is an unsuccessful search (or a hit on the last probe). With $T(n)$ the number of comparisons:

$$T(n) = T\!\left(\frac{n}{2}\right) + 1, \qquad T(1) = 1$$

Unrolling $k$ times:

$$T(n) = T\!\left(\frac{n}{2^{k}}\right) + k$$

The list is exhausted when $n/2^{k} = 1$, i.e. $k = \log_2 n$:

$$T(n) = T(1) + \log_2 n = 1 + \log_2 n$$

$$\boxed{\,T_{\text{worst}}(n) = \lfloor \log_2 n \rfloor + 1 = O(\log n)\,}$$

(Best case $O(1)$ when the middle element is the key.) For example, 1000 items need at most 10 probes.

**Bubble sort of 67, 45, 54, 2, 29.** In every pass adjacent pairs are compared and swapped if out of order, so the largest remaining element "bubbles" to the end:

''' + bs_md + r'''
Pass 4 makes no swap, so the list is sorted:

$$\boxed{\,2,\ 29,\ 45,\ 54,\ 67\,}$$

@s 10
**Wheel graph.** The wheel graph $W_n$ is obtained from a cycle $C_n$ (the rim) by adding one new vertex (the hub) joined to every vertex of the cycle by a spoke. $W_n$ has $n + 1$ vertices and $2n$ edges ($W_3 = K_4$, and $W_6$ has 7 vertices and 12 edges).

**Hypercube $Q_3$.** $Q_n$ has $2^{n}$ vertices, the $n$-bit strings, two being adjacent iff they differ in exactly one bit. $Q_3$ has $8$ vertices, is $3$-regular and has $\dfrac{8 \cdot 3}{2} = 12$ edges.

''' + FIG_CUBE + r'''
**Number of edges in $K_n$.** In the complete graph $K_n$ every pair of distinct vertices is joined by exactly one edge.

*Proof 1 (counting pairs).* The number of edges equals the number of 2-element subsets of the $n$ vertices:

$$|E| = \binom{n}{2} = \frac{n(n-1)}{2}$$

*Proof 2 (handshaking lemma).* Each vertex is adjacent to the other $n - 1$ vertices, so $\deg(v) = n - 1$ for all $n$ vertices. Since the sum of the degrees is twice the number of edges,

$$2\,|E| = \sum_{v} \deg(v) = n(n-1) \ \Rightarrow\ |E| = \frac{n(n-1)}{2}. \ \blacksquare$$

*Proof 3 (induction).* $K_1$ has $0$ edges $= 1\cdot 0/2$. If $K_k$ has $k(k-1)/2$ edges, then $K_{k+1}$ adds one vertex joined to the $k$ old vertices: $\dfrac{k(k-1)}{2} + k = \dfrac{k(k+1)}{2}$. $\blacksquare$

@s 11
**Euler's formula.** For a connected planar graph with $v$ vertices, $e$ edges and $f$ faces (regions, including the outer unbounded face) drawn in the plane without crossings,

$$v - e + f = 2$$

**Proof (induction on the number of edges $e$).**

*Basis.* A connected graph with $e = 0$ is a single vertex: $v = 1$, $f = 1$, so $v - e + f = 1 - 0 + 1 = 2$. (A tree with $v$ vertices has $e = v - 1$, $f = 1$, and $v - (v-1) + 1 = 2$ also holds.)

*Inductive step.* Assume the formula holds for all connected planar graphs with $e - 1$ edges, and let $G$ be a connected planar graph with $e \ge 1$ edges.

*Case 1: $G$ has no cycle.* Then $G$ is a tree, $e = v - 1$ and $f = 1$, so $v - e + f = v - (v-1) + 1 = 2$.

*Case 2: $G$ has a cycle.* Choose an edge $x$ on a cycle. It separates two different faces (the inside and the outside of the cycle). Remove it: the graph $G' = G - x$ stays connected, has $e - 1$ edges, the same $v$ vertices, and the two faces merge into one, so it has $f - 1$ faces. By the inductive hypothesis

$$v - (e - 1) + (f - 1) = 2 \ \Rightarrow\ v - e + f = 2$$

So the formula holds for $G$. By induction it holds for every connected planar graph. $\blacksquare$

**Corollaries.** For a simple connected planar graph with $v \ge 3$: $e \le 3v - 6$ (each face is bounded by at least 3 edges and each edge borders two faces, $3f \le 2e$); hence $K_5$ ($e = 10 > 9$) is non-planar.

@s 12
**Saturated edge.** In a flow network with capacities $c(u,v)$ and a flow $f$, an edge is **saturated** when its flow equals its capacity, $f(u,v) = c(u,v)$. No more flow can be pushed through a saturated edge along its direction (it has zero residual capacity).

**Max-flow min-cut theorem** (the question writes "Max-Cut Min Flow"). In a flow network the value of the maximum flow from the source $s$ to the sink $t$ equals the capacity of a minimum cut separating $s$ from $t$:

$$\max |f| = \min_{(S, T)} c(S, T), \qquad c(S, T) = \sum_{u \in S,\ v \in T} c(u, v)$$

A flow is maximum exactly when there is no augmenting path in the residual network; the vertices reachable from $s$ then form the source side $S$ of a minimum cut, and every edge from $S$ to $T$ is saturated.

**Kruskal's algorithm.** Sort the edges by weight and add each edge in turn unless it closes a cycle, until $v - 1$ edges are chosen. The graph has 9 vertices ($S, B, C, D, E, F, G, H, K$), so the tree needs 8 edges. (The vertical edge $DE$ has no weight printed in the scan; in the sorted list it could only matter if its weight were below 6, and for any weight of 6 or more it is rejected because $D$ and $E$ are already connected, so the answer does not depend on it.)

''' + kruskal_md + r'''
Spanning tree edges: $GK (1),\ FG (2),\ BC (3),\ SB (4),\ GH (4),\ BD (5),\ EG (5),\ DF (6)$.

$$\text{Total weight} = 1 + 2 + 3 + 4 + 4 + 5 + 5 + 6 = 30$$

''' + FIG_KS + r'''
$$\boxed{\,\text{Minimum spanning tree weight} = 30\,}$$

(The weight is unique; the tie between $DF$ and $CD$ at 6 resolves in favour of $DF$ because $CD$ would close the cycle $B$-$C$-$D$.)

@s 13
**Dijkstra's algorithm.** Label the source $0$ and every other vertex $\infty$. Repeatedly make permanent the unvisited vertex with the smallest tentative distance, then relax all its edges: $d(v) = \min\big(d(v),\ d(u) + w(u,v)\big)$.

Edges read from the figure: $AB = 8$, $AC = 2$, $BC = 3$, $BD = 5$, $CD = 9$, $CE = 8$, $DF = 3$, $EF = 8$, $EG = 12$, $FG = 6$, $FH = 7$, $GH = 4$.

''' + dij_md + r'''
Highlights of the relaxations: $d(C) = 2$ (direct $AC$); $d(B) = \min(8,\ 2 + 3) = 5$ via $C$; $d(D) = \min(2 + 9,\ 5 + 5) = 10$ via $B$; $d(E) = 2 + 8 = 10$; $d(F) = \min(10 + 3,\ 10 + 8) = 13$ via $D$; $d(G) = \min(10 + 12,\ 13 + 6) = 19$ via $F$; $d(H) = \min(13 + 7,\ 19 + 4) = 20$ via $F$.

**Result (shortest distance from $A$):**

''' + res_md + r'''
''' + FIG_DS + r'''
$$\boxed{\,d(A,B) = 5,\ d(A,C) = 2,\ d(A,D) = 10,\ d(A,E) = 10,\ d(A,F) = 13,\ d(A,G) = 19,\ d(A,H) = 20\,}$$
'''
os.makedirs(OUT, exist_ok=True)
open(os.path.join(OUT, "ioe-enct251-2082-bhadra.md"), "w").write(d)
print("written", len(d))
