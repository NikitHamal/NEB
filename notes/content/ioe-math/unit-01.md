---
subject: Mathematics
grade: IOE
unit: 1
title: Set, Logic and Functions
hours: 3
area: Mathematics
---

This is the smallest chapter of the paper (our estimate: about **3 questions**, mostly Section A), but it is also the vocabulary of every other chapter: you cannot find a domain, an inverse or a range in calculus without it. The questions are short and exact: count something with a Venn diagram, solve an absolute-value inequality, negate a statement, decide whether a function is one-one or onto, or compose two functions. Marks are lost here by carelessness, not by difficulty.

::: key What the paper asks from this chapter
- Counting with sets: $n(A\cup B)=n(A)+n(B)-n(A\cap B)$, subsets $2^n$, De Morgan's laws.
- Inequalities with $|x|$: $|x-a|<r \iff a-r<x<a+r$; $|x-a|>r$ is the outside of that interval.
- Logic: truth tables, negation of $\wedge,\vee,\to$, converse / inverse / contrapositive, tautology.
- Functions: domain and range, injective / surjective / bijective and their counts, even / odd, period.
- Composition $f\circ g$ and the inverse; $(f\circ g)^{-1}=g^{-1}\circ f^{-1}$.
:::

## 1.1 Set, real number system, intervals, absolute value, logic, connectives, laws of logic

### Sets

A **set** is a well-defined collection. $A\subseteq B$ means every element of $A$ is in $B$; $A\subset B$ (proper) also needs $A\ne B$. The **power set** $P(A)$ is the set of all subsets, so $n(P(A))=2^{n}$ when $n(A)=n$; there are $2^n-1$ proper subsets and $2^n-2$ non-empty proper subsets.

| Operation | Symbol | Meaning |
|---|---|---|
| union | $A\cup B$ | in $A$ or $B$ or both |
| intersection | $A\cap B$ | in both |
| difference | $A-B$ | in $A$ but not $B$ |
| complement | $A'$ | in $U$ but not $A$ |
| symmetric difference | $A\,\Delta\,B$ | $(A-B)\cup(B-A)$ |

**Laws.** Commutative, associative, distributive ($A\cap(B\cup C)=(A\cap B)\cup(A\cap C)$), and **De Morgan**: $(A\cup B)'=A'\cap B'$, $(A\cap B)'=A'\cup B'$; also $A-B=A\cap B'$.

**Counting.** $n(A\cup B)=n(A)+n(B)-n(A\cap B)$ and
$$n(A\cup B\cup C)=\sum n(A)-\sum n(A\cap B)+n(A\cap B\cap C).$$
Number of elements in exactly one of $A,B$: $n(A)+n(B)-2n(A\cap B)$.

::: example Tea and coffee
**Problem.** In a class of 60, 35 take tea, 30 take coffee and 10 take both. How many take neither?

**Solution.** Either = $35+30-10=55$, so neither $=60-55=5$.
:::

### Real number system and intervals

$\mathrm{N}\subset\mathrm{W}\subset\mathrm{Z}\subset\mathrm{Q}\subset\mathrm{R}$. Rationals have terminating or repeating decimals; irrationals ($\sqrt{2}$, $\pi$, $e$) have non-terminating, non-repeating ones. Between any two reals there are infinitely many rationals and irrationals.

Intervals: $(a,b)$ open, $[a,b]$ closed, $[a,b)$ and $(a,b]$ half-open; $(-\infty,a)$, $[a,\infty)$ are unbounded. Union and intersection of intervals are the usual set operations on a number line.

### Absolute value

$|x|=x$ if $x\ge0$ and $-x$ if $x<0$; $|x|=\sqrt{x^2}$.

| Inequality ($r>0$) | Solution |
|---|---|
| $|x-a|<r$ | $a-r<x<a+r$ |
| $|x-a|\le r$ | $a-r\le x\le a+r$ |
| $|x-a|>r$ | $x<a-r$ or $x>a+r$ |
| $|f|<|g|$ | square both sides: $f^2<g^2$ |

Triangle inequality: $|a+b|\le|a|+|b|$; $|ab|=|a||b|$.

::: caution Absolute value traps
$|x|<-2$ has **no** solution and $|x|>-2$ is **every** real number. Never "square" an inequality $f<g$ unless both sides are known to be non-negative.
:::

### Logic

A **statement** is a sentence that is either true or false. Connectives: $\neg p$ (not), $p\wedge q$ (and), $p\vee q$ (or, inclusive), $p\to q$ (if $p$ then $q$), $p\leftrightarrow q$ (if and only if).

| $p$ | $q$ | $p\wedge q$ | $p\vee q$ | $p\to q$ | $p\leftrightarrow q$ |
|---|---|---|---|---|---|
| T | T | T | T | T | T |
| T | F | F | T | F | F |
| F | T | F | T | T | F |
| F | F | F | F | T | T |

$p\to q$ is false **only** when $p$ is true and $q$ false, and $p\to q\equiv\neg p\vee q$.

For $p\to q$: **converse** $q\to p$; **inverse** $\neg p\to\neg q$; **contrapositive** $\neg q\to\neg p$. The contrapositive is *equivalent* to the original; the converse and inverse are equivalent to each other but not to it.

**Laws of logic.** De Morgan: $\neg(p\wedge q)\equiv\neg p\vee\neg q$, $\neg(p\vee q)\equiv\neg p\wedge\neg q$; distributive, idempotent, double negation $\neg\neg p\equiv p$; $\neg(p\to q)\equiv p\wedge\neg q$. A **tautology** is always true (e.g. $p\vee\neg p$, $p\to(p\vee q)$); a **contradiction** is always false ($p\wedge\neg p$). Quantifiers: the negation of "for all $x$, $P(x)$" is "there exists $x$ with $\neg P(x)$", and vice versa.

## 1.2 Function, types of functions, inverse and composite functions

A **function** $f:A\to B$ gives each $x\in A$ exactly one $f(x)\in B$. $A$ is the domain, $B$ the codomain, and $\{f(x)\}$ the **range** (a subset of $B$). A vertical line meets a graph at most once.

**Finding a domain:** denominators $\ne0$; even roots need radicand $\ge0$; $\log$ needs argument $>0$ (and base $>0,\ne1$); $\sin^{-1}x,\cos^{-1}x$ need $|x|\le1$.

### One-one, onto, bijective

| Type | Test | Counting ($n(A)=m$, $n(B)=n$) |
|---|---|---|
| injective (one-one) | $f(a)=f(b)\Rightarrow a=b$ | $n(n-1)\cdots(n-m+1)$ |
| surjective (onto) | range = codomain | $n^m-\binom{n}{1}(n-1)^m+\binom{n}{2}(n-2)^m-\cdots$ |
| bijective | both | $n!$ if $m=n$ |
| all functions | | $n^m$ |

A graph passing the **horizontal line test** is injective. A function from $\mathrm{R}$ to $\mathrm{R}$ like $x^2$ is neither (not injective: $f(2)=f(-2)$; not onto: negatives missed); $x^3$ is bijective.

### Standard families

Algebraic (polynomial, rational, root); trigonometric; exponential $a^x$ ($a>0$, range $(0,\infty)$); logarithmic $\log_a x$ (domain $(0,\infty)$, inverse of $a^x$). Log laws: $\log(xy)=\log x+\log y$, $\log(x/y)=\log x-\log y$, $\log x^k=k\log x$, $\log_a b=\dfrac{\log b}{\log a}$.

**Even / odd.** Even: $f(-x)=f(x)$ (graph symmetric about the $y$-axis; $x^2,\cos x,|x|$). Odd: $f(-x)=-f(x)$ ($x^3,\sin x,\tan x$). **Periodic:** $f(x+T)=f(x)$; $\sin ax,\cos ax$ have period $2\pi/|a|$ and $\tan ax$ has $\pi/|a|$.

### Composite and inverse

$(f\circ g)(x)=f(g(x))$; in general $f\circ g\ne g\circ f$, but composition is associative. The **inverse** $f^{-1}$ exists exactly when $f$ is a bijection; to find it solve $y=f(x)$ for $x$ and swap. Then $f(f^{-1}(x))=x$, $(f\circ g)^{-1}=g^{-1}\circ f^{-1}$, and the graphs of $f,f^{-1}$ are mirror images in $y=x$.

::: tip Technique
To find a **range**, solve $y=f(x)$ for $x$ and ask for which $y$ a real $x$ exists (e.g. $y=\frac{1}{1+x^2}\Rightarrow x^2=\frac{1-y}{y}\ge0\Rightarrow 0<y\le1$).
:::

```photogrid label="1.1" cols="2" ratio="1.2" caption="Counting with sets. (a) A Venn design on a bridge in Hull: overlapping circles are the picture of intersection and union. (b) A survey of 100 students on three subjects: the eight regions hold 20, 12, 8, 10, 6, 4, 15 and 25 students. From them n(M) = 51, n(P) = 41, n(C) = 33, n(M and P) = 25, n(M and C) = 21, n(P and C) = 19. The formula n(M or P or C) = n(M) + n(P) + n(C) - n(M and P) - n(M and C) - n(P and C) + n(M and P and C) gives 75, which agrees with 100 - 25 = 75."
@ photo id="bcamath/vennbridge" cap="Venn diagrams worked into the railings of a bridge"
fit 1.2
focus 0.5 0.5
@ svg cap="Three-set survey: inclusion-exclusion checked by regions"
import itertools
R = dict(M=20, P=12, C=8, MP=10, MC=6, PC=4, MPC=15, none=25)
nm = R["M"] + R["MP"] + R["MC"] + R["MPC"]; np_ = R["P"] + R["MP"] + R["PC"] + R["MPC"]; nc = R["C"] + R["MC"] + R["PC"] + R["MPC"]
nmp = R["MP"] + R["MPC"]; nmc = R["MC"] + R["MPC"]; npc = R["PC"] + R["MPC"]
union = nm + np_ + nc - nmp - nmc - npc + R["MPC"]
assert sum(R.values()) == 100 and union == 100 - R["none"] == 75 and (nm, np_, nc, nmp, nmc, npc) == (51, 41, 33, 25, 21, 19)
facts = dict(only_m=R["M"], only_p=R["P"], only_c=R["C"], mp=R["MP"], mc=R["MC"], pc=R["PC"], mpc=R["MPC"], none=R["none"], nm=nm, np_=np_, nc=nc, nmp=nmp, nmc=nmc, npc=npc, union=union)
cen = dict(M=(112, 92), P=(188, 92), C=(150, 150)); r = 54
lab = dict(M=((84, 76), "M"), P=((216, 76), "P"), C=((150, 184), "C"), MP=((150, 66), "MP"), MC=((114, 128), "MC"), PC=((186, 128), "PC"), MPC=((150, 106), "MPC"))
for k, ((x, y), s) in lab.items():
    inside = "".join(c for c in "MPC" if (x - cen[c][0]) ** 2 + (y - cen[c][1]) ** 2 < r * r)
    assert inside == (s if len(s) > 1 else s), (k, inside)
f = Fig(300, 236)
f.text(150, 14, "100 students: Maths M, Physics P, Chemistry C", size=10.5, color=NAVY, bold=True)
cols = dict(M=("#bfdbfe", NAVY), P=("#fde68a", AMBER), C=("#a7f3d0", TEAL))
for c in "MPC":
    f.raw('<circle cx="%d" cy="%d" r="%d" fill="%s" fill-opacity="0.55" stroke="%s" stroke-width="2"/>' % (cen[c][0], cen[c][1], r, cols[c][0], cols[c][1]))
f.text(66, 52, "M", size=12, color=NAVY, bold=True); f.text(234, 52, "P", size=12, color=AMBER, bold=True); f.text(96, 190, "C", size=12, color=TEAL, bold=True)
for k, ((x, y), s) in lab.items():
    f.text(x, y, R[k], size=11.5, color=SLATE, bold=True, vmid=True)
f.text(278, 196, "none: %d" % R["none"], size=10.5, color=RED, bold=True, anchor="end")
f.text(150, 226, "51+41+33-25-21-19+15 = 75", size=10.5, color=NAVY, bold=True)
```

```photogrid label="1.2" cols="2" ratio="1.2" caption="A function is a rule with exactly one output for each input. (a) In a vending machine each button gives one drink, so buttons to drinks is a function; two buttons may give the same drink, and a drink that no button gives lies outside the range. (b) With 3 buttons and 4 drinks there are 64 possible functions (4 choices for each of 3 buttons), of which 24 are one-one (4 x 3 x 2) and 0 are onto, because 3 buttons cannot cover 4 drinks. With 4 buttons and 3 drinks, 81 functions exist, 0 are one-one and 36 are onto; the last number is 3^4 - 3 x 2^4 + 3. All counts are found by listing every function."
@ photo id="ioemath/vending" cap="A vending machine: press a button, get one drink"
fit 1.2
focus 0.5 0.55
@ svg cap="Counting functions by listing every mapping"
import itertools
def count(nA, nB):
    tot = inj = onto = 0
    for m in itertools.product(range(nB), repeat=nA):
        tot += 1; inj += len(set(m)) == nA; onto += len(set(m)) == nB
    return tot, inj, onto
t1, i1, o1 = count(3, 4); t2, i2, o2 = count(4, 3)
assert (t1, i1, o1) == (64, 24, 0) and (t2, i2, o2) == (81, 0, 36) and o2 == 3 ** 4 - 3 * 2 ** 4 + 3
facts = dict(tot1=t1, inj1=i1, onto1=o1, tot2=t2, inj2=i2, onto2=o2)
f = Fig(300, 236)
f.text(150, 14, "one function from 3 buttons to 4 drinks", size=10.5, color=NAVY, bold=True)
btn = ["A1", "A2", "A3"]; drk = ["Cola", "Lemon", "Water", "Juice"]; mp = [0, 0, 2]
for i, b in enumerate(btn): f.box(30, 34 + i * 34, 52, 24, b, fill=BLUE, stroke=NAVY, size=10.5, bold=True, r=12)
for j, d in enumerate(drk): f.box(206, 28 + j * 28, 66, 22, d, fill=(MINT if j in mp else SOFT), stroke=(TEAL if j in mp else SOFT), color=(TEAL if j in mp else SLATE), size=10.5, bold=True, r=11)
for i, j in enumerate(mp): f.arrow([(82, 46 + i * 34), (206, 39 + j * 28)], color=AMBER, sw=1.5)
f.text(150, 140, "A1 and A2 both give Cola: many-one", size=10.5, color=AMBER, bold=True)
f.text(150, 156, "range = {Cola, Water}, Lemon and Juice unused", size=10.5, color=TEAL, bold=True)
rows = [("3 buttons to 4 drinks", "%d" % t1, "%d" % i1, "%d" % o1), ("4 buttons to 3 drinks", "%d" % t2, "%d" % i2, "%d" % o2)]
f.box(10, 176, 280, 20, "", fill=BLUE, stroke=NAVY, r=3)
for x, s in ((14, "case"), (150, "all"), (196, "one-one"), (254, "onto")): f.text(x, 186, s, size=10.5, color=NAVY, bold=True, anchor="start", vmid=True)
for k, (a, b, c, d) in enumerate(rows):
    y = 198 + k * 18
    f.text(14, y + 8, a, size=10.5, color=SLATE, anchor="start", vmid=True)
    for x, s in ((150, b), (196, c), (254, d)): f.text(x, y + 8, s, size=10.5, color=TEAL, bold=True, anchor="start", vmid=True)
```

```photogrid label="1.3" cols="2" ratio="1.2" caption="Logic laws checked by truth tables. (a) A staircase lamp with two switches is on when exactly one switch is up, which is p XOR q; it is also the negation of p if and only if q. (b) The table lists every truth value of p and q. Columns 3 and 4 are identical, so the two statements are equivalent. Columns 5, 6 and 7 are identical, so p implies q equals (not p) or q equals the contrapositive (not q) implies (not p), while the converse in column 8 differs in 2 of the 4 rows. A statement that is true in all rows is a tautology; 4 of the 6 statements tested are tautologies."
@ photo id="bca155/lightswitch" cap="A light switch: the lamp state is a logic function of the switch positions"
fit 1.2
focus 0.5 0.5
@ svg cap="Truth table: XOR, implication, contrapositive, converse"
import itertools
rows = list(itertools.product([1, 0], repeat=2))
imp = lambda a, b: int((not a) or b)
cols = {"xor": [p ^ q for p, q in rows], "nbi": [int(not (p == q)) for p, q in rows], "imp": [imp(p, q) for p, q in rows],
        "ndis": [int((not p) or q) for p, q in rows], "cp": [imp(1 - q, 1 - p) for p, q in rows], "conv": [imp(q, p) for p, q in rows]}
assert cols["xor"] == cols["nbi"] and cols["imp"] == cols["ndis"] == cols["cp"] and cols["conv"] != cols["imp"]
diff = sum(a != b for a, b in zip(cols["conv"], cols["imp"]))
stm = [lambda p, q: p or not p, lambda p, q: imp(p and q, p), lambda p, q: imp(p, q), lambda p, q: imp(p, p or q), lambda p, q: (p ^ q) or (p == q), lambda p, q: imp(q, p)]
taut = sum(all(s(p, q) for p, q in rows) for s in stm)
assert diff == 2 and taut == 4
facts = dict(diff=diff, taut=taut, nstat=len(stm))
f = Fig(300, 236)
f.text(150, 14, "T = 1, F = 0; 2-switch lamp = XOR", size=10.5, color=NAVY, bold=True)
heads = ["p", "q", "XOR", "~(p\n=q)", "p>q", "~p\nv q", "~q>\n~p", "q>p"]
fills = [BLUE, BLUE, MINT, MINT, SAND, SAND, SAND, ROSE]; strokes = [NAVY, NAVY, TEAL, TEAL, AMBER, AMBER, AMBER, RED]
data = [[p, q, cols["xor"][i], cols["nbi"][i], cols["imp"][i], cols["ndis"][i], cols["cp"][i], cols["conv"][i]] for i, (p, q) in enumerate(rows)]
w = 35
for c, h in enumerate(heads): f.box(10 + c * w, 28, w - 2, 30, h, fill=fills[c], stroke=strokes[c], size=10.5, bold=True, r=3)
for r_, row in enumerate(data):
    for c, v in enumerate(row):
        hot = c == 7 and v != row[4]
        f.box(10 + c * w, 60 + r_ * 28, w - 2, 24, str(v), fill=(ROSE if hot else SOFT), stroke=(RED if hot else strokes[c]), size=11, bold=True, r=3, color=(RED if hot else SLATE))
f.line(10, 180, 290, 180, color=SOFT, sw=1)
f.text(150, 192, "columns 3 = 4:  XOR = not (p iff q)", size=10.5, color=TEAL, bold=True)
f.text(150, 208, "columns 5 = 6 = 7:  implication = contrapositive", size=10.5, color=AMBER, bold=True)
f.text(150, 224, "column 8 (converse) differs in %d rows" % diff, size=10.5, color=RED, bold=True)
```

## Formula and fact sheet

| Topic | Result |
|---|---|
| subsets | $2^n$; proper $2^n-1$ |
| union | $n(A\cup B)=n(A)+n(B)-n(A\cap B)$ |
| De Morgan | $(A\cup B)'=A'\cap B'$ |
| $|x|<r$ | $-r<x<r$ |
| $p\to q$ | $\equiv\neg p\vee q$; contrapositive $\neg q\to\neg p$ |
| number of functions | $n^m$; injective $^nP_m$; bijections $n!$ |
| inverse | $(f\circ g)^{-1}=g^{-1}\circ f^{-1}$ |
| period | $\sin ax$: $2\pi/|a|$; $\tan ax$: $\pi/|a|$ |

## Chapter summary

- A set of $n$ elements has $2^n$ subsets, $2^n-1$ proper ones.
- Use inclusion-exclusion; keep the three-set formula's alternating signs.
- $|x-a|<r$ is an interval around $a$; $>r$ is its outside.
- $p\to q$ is false only for T → F; the contrapositive is equivalent, the converse is not.
- Injective means distinct inputs give distinct outputs; onto means range = codomain.
- Inverse exists only for bijections; compose in reverse order to invert a composite.

## Practice questions

**Set A — Recall (14 questions)**

1. The number of subsets of a set with 4 elements is
   (a) 8 (b) 15 (c) 16 (d) 12
2. Which of the following is irrational?
   (a) $0.1010010001\ldots$ (the number of zeros grows by one each time) (b) $22/7$ (c) $\sqrt{49}$ (d) $3.14$
3. The solution set of $|x-3|<2$ is
   (a) $(-1,5)$ (b) $(1,5)$ (c) $(-\infty,1)\cup(5,\infty)$ (d) $[1,5]$
4. The negation of $p\wedge q$ is
   (a) $\neg p\wedge\neg q$ (b) $p\vee q$ (c) $\neg p\wedge q$ (d) $\neg p\vee\neg q$
5. The contrapositive of $p\to q$ is
   (a) $\neg q\to\neg p$ (b) $q\to p$ (c) $\neg p\to\neg q$ (d) $p\to\neg q$
6. If $n(A)=20$, $n(B)=15$ and $n(A\cap B)=7$, then $n(A\cup B)$ is
   (a) 35 (b) 28 (c) 42 (d) 22
7. The number of injective functions from a 3-element set to a 4-element set is
   (a) 64 (b) 12 (c) 81 (d) 24
8. The domain of $f(x)=\sqrt{x-2}+\dfrac{1}{x-5}$ is
   (a) $[2,\infty)$ (b) $(2,5)\cup(5,\infty)$ (c) $[2,5)\cup(5,\infty)$ (d) $\mathrm{R}-\{5\}$
9. The inverse of $f(x)=2x+3$ is
   (a) $\dfrac{x+3}{2}$ (b) $\dfrac{x-3}{2}$ (c) $2x-3$ (d) $\dfrac{1}{2x+3}$
10. If $f(x)=x^2$ and $g(x)=x+1$, then $(f\circ g)(3)$ is
    (a) 16 (b) 10 (c) 12 (d) 9
11. Which function is even?
    (a) $x^3+x$ (b) $\cos x+x^2$ (c) $\sin x$ (d) $x^2+x$
12. The period of $\sin 3x$ is
    (a) $2\pi$ (b) $\pi$ (c) $\pi/3$ (d) $2\pi/3$
13. The value of $\log_2 8+\log_3 9$ is
    (a) 5 (b) 6 (c) 4 (d) 11
14. The function $f:\mathrm{R}\to\mathrm{R}$, $f(x)=x^2$ is
    (a) one-one only (b) onto only (c) neither one-one nor onto (d) bijective

::: note Answers and explanations — Set A
**1.** (c) — $2^4=16$. (b) 15 is the number of *proper* subsets, $2^4-1$.
**2.** (a) — the decimal never terminates or repeats. $22/7$ is a fraction, $\sqrt{49}=7$, $3.14$ terminates.
**3.** (b) — $3-2<x<3+2$. (c) is the answer to $|x-3|>2$.
**4.** (d) — De Morgan: $\neg(p\wedge q)\equiv\neg p\vee\neg q$.
**5.** (a) — contrapositive swaps and negates. (b) is the converse, (c) the inverse.
**6.** (b) — $20+15-7=28$.
**7.** (d) — $4\times3\times2=24$ ($4^3=64$ counts all functions).
**8.** (c) — $x\ge2$ for the root, $x\ne5$ for the fraction; 2 is allowed because the root of 0 is defined.
**9.** (b) — $y=2x+3\Rightarrow x=(y-3)/2$.
**10.** (a) — $g(3)=4$, $f(4)=16$. (b) 10 is $(g\circ f)(3)$.
**11.** (b) — $\cos(-x)+(-x)^2=\cos x+x^2$. $x^3+x$ and $\sin x$ are odd; $x^2+x$ is neither.
**12.** (d) — $2\pi/3$.
**13.** (a) — $3+2$.
**14.** (c) — $f(2)=f(-2)$ and no real $x$ gives $-1$.
:::

**Set B — Understanding (9 questions)**

1. In a group of 60 people, 35 like tea, 30 like coffee and 10 like both. The number who like neither is
   (a) 0 (b) 10 (c) 5 (d) 15
2. The number of integers $x$ with $|2x-1|\le5$ is
   (a) 5 (b) 6 (c) 7 (d) 3
3. The solution of $|x-2|>|x+1|$ is
   (a) $x<\tfrac{1}{2}$ (b) $x>\tfrac{1}{2}$ (c) $x<-1$ (d) every real $x$
4. $p\to q$ is logically equivalent to
   (a) $p\wedge\neg q$ (b) $\neg p\vee q$ (c) $p\vee\neg q$ (d) $\neg p\wedge q$
5. Which is a tautology?
   (a) $p\wedge\neg p$ (b) $p\wedge q$ (c) $p\to(p\vee q)$ (d) $(p\wedge q)\to\neg p$
6. The number of subsets of $\{1,2,3,4,5\}$ that contain both 1 and 2 is
   (a) 4 (b) 6 (c) 16 (d) 8
7. If $f(x)=\dfrac{x+1}{x-1}$ ($x\ne1$), then $f(f(x))$ equals
   (a) $x$ (b) $1/x$ (c) $-x$ (d) $\dfrac{x-1}{x+1}$
8. If $f(x)=2x+1$ and $g(x)=x-3$, then $(g\circ f)^{-1}(5)$ is
   (a) 4 (b) 7 (c) 3.5 (d) 2
9. The range of $f(x)=\dfrac{1}{1+x^2}$ is
   (a) $(0,1)$ (b) $[0,1]$ (c) $(0,\infty)$ (d) $(0,1]$

::: note Answers and explanations — Set B
**1.** (c) — $60-(35+30-10)=5$.
**2.** (b) — $-5\le2x-1\le5\Rightarrow-2\le x\le3$: the integers $-2,-1,0,1,2,3$.
**3.** (a) — square both sides: $x^2-4x+4>x^2+2x+1\Rightarrow 3>6x$. Check $x=0$: $2>1$ ✓.
**4.** (b) — the implication fails only when $p$ true and $q$ false, so it equals $\neg p\vee q$ ($p\wedge\neg q$ is its negation).
**5.** (c) — if $p$ is true then $p\vee q$ is true. (d) fails when $p,q$ are both true.
**6.** (d) — fix 1 and 2 in; each of 3, 4, 5 is in or out: $2^3=8$.
**7.** (a) — $\dfrac{\frac{x+1}{x-1}+1}{\frac{x+1}{x-1}-1}=\dfrac{2x}{2}=x$; $f$ is its own inverse.
**8.** (c) — $(g\circ f)(x)=2x-2$, so the inverse is $\dfrac{y+2}{2}$; at 5 it is 3.5.
**9.** (d) — $x=0$ gives 1; the value never reaches 0. (a) wrongly drops 1.
:::

**Set C — Application (7 questions)**

1. Among 100 students, 50 study Maths, 40 Physics, 30 Chemistry; 20 study Maths and Physics, 15 Physics and Chemistry, 10 Maths and Chemistry, and 5 study all three. How many study at least one subject?
   (a) 80 (b) 85 (c) 70 (d) 75
2. The domain of $f(x)=\log(x^2-5x+6)$ is
   (a) $(2,3)$ (b) $(-\infty,2)\cup(3,\infty)$ (c) $[2,3]$ (d) $\mathrm{R}$
3. The function $f(x)=\ln\!\big(x+\sqrt{x^2+1}\big)$ is
   (a) even (b) periodic (c) odd (d) neither even nor odd
4. The solution set of $|x^2-4|<5$ is
   (a) $(-1,3)$ (b) $(-\sqrt{5},\sqrt{5})$ (c) $(-9,9)$ (d) $(-3,3)$
5. If $f(x+1)=x^2+3x+2$, then $f(x)$ is
   (a) $x^2-x$ (b) $x^2+x$ (c) $x^2+3x$ (d) $x^2+1$
6. The number of onto functions from $\{1,2,3\}$ to $\{a,b\}$ is
   (a) 8 (b) 2 (c) 6 (d) 4
7. If $A=\{1,2\}$, then the number of elements of $P(P(A))$ is
   (a) 16 (b) 8 (c) 4 (d) 32

::: note Answers and explanations — Set C
**1.** (a) — $50+40+30-20-15-10+5=80$.
**2.** (b) — $x^2-5x+6=(x-2)(x-3)>0$ outside the roots.
**3.** (c) — $f(-x)=\ln(\sqrt{x^2+1}-x)=\ln\frac{1}{x+\sqrt{x^2+1}}=-f(x)$.
**4.** (d) — $-5<x^2-4<5\Rightarrow x^2<9$ (the left side $x^2>-1$ always holds), so $-3<x<3$.
**5.** (b) — put $x\to x-1$: $(x-1)^2+3(x-1)+2=x^2+x$.
**6.** (c) — all functions $2^3=8$, minus the 2 constant ones: 6.
**7.** (a) — $n(P(A))=4$, so $n(P(P(A)))=2^4=16$.
:::

**Group D — Model answers for long questions (10 marks each, for deeper revision)**

1. In a survey of 100 students, $n(M)=50$, $n(P)=45$, $n(C)=40$, $n(M\cap P)=20$, $n(P\cap C)=15$, $n(M\cap C)=18$ and $n(M\cap P\cap C)=8$. Find the number in each region, and prove that $(p\to q)\wedge(q\to r)\Rightarrow(p\to r)$ is a tautology. <span class="marks">[10]</span>
2. Find the domain and range of a function, the inverse of a rational function, and compare $f\circ g$ with $g\circ f$. <span class="marks">[10]</span>

### Model answer D1: Sets, Venn diagrams and logic (10 marks)

**Introduction.** For three finite sets the **inclusion–exclusion** rule gives
$$n(M\cup P\cup C)=n(M)+n(P)+n(C)-n(M\cap P)-n(P\cap C)-n(M\cap C)+n(M\cap P\cap C).$$

**Solution.** Work from the middle outwards.

1. **All three:** $8$.
2. **Exactly two:** $M,P$ only $=20-8=12$; $P,C$ only $=15-8=7$; $M,C$ only $=18-8=10$.
3. **Only one:** $M$ only $=50-12-10-8=20$; $P$ only $=45-12-7-8=18$; $C$ only $=40-10-7-8=15$.
4. **Union:** $20+18+15+12+7+10+8=90$, which matches $50+45+40-20-15-18+8=90$.
5. **None of the three:** $100-90=10$.

| Region | Students |
|---|---|
| Only M / only P / only C | 20 / 18 / 15 |
| Exactly two subjects | 29 |
| All three | 8 |
| None | 10 |

**Logic.** A **tautology** is true in every row of the truth table. Since $p\to q\equiv\neg p\vee q$, we test $[(p\to q)\wedge(q\to r)]\to(p\to r)$ in the eight cases of $(p,q,r)$. The antecedent is true only when $p\to q$ and $q\to r$ are both true: $(T,T,T)$, $(F,T,T)$, $(F,F,T)$, $(F,F,F)$ and $(F,T,F)$ is excluded since $q\to r$ is false. In each admitted row, $p\to r$ is true ($TT$, $FT$, $FT$, $FF$). The whole statement is therefore true in all 8 rows: it is a tautology (**hypothetical syllogism**).

**Useful laws.** De Morgan: $\neg(p\wedge q)\equiv\neg p\vee\neg q$. Contrapositive: $p\to q\equiv\neg q\to\neg p$. Inequalities: $\lvert 2x-3\rvert<5\Rightarrow -1<x<4$ and $\lvert x-2\rvert\ge3\Rightarrow x\le-1$ or $x\ge5$.

**Conclusion.** Working from the three-way intersection outwards avoids double counting, and a truth table settles any logical identity.

### Model answer D2: Functions, inverse and composition (10 marks)

**Introduction.** A **function** $f:A\to B$ gives exactly one output for each input. The **domain** is the set of allowed inputs and the **range** is the set of outputs.

**1. Domain and range.** For $f(x)=\frac{\sqrt{x-1}}{x-3}$ we need $x-1\ge0$ and $x\ne3$, so the domain is $[1,\infty)\setminus\{3\}$. For $f(x)=x^2-4x+3=(x-2)^2-1$, the range is $[-1,\infty)$.

**2. Inverse.** A function has an inverse only if it is **one-one and onto**. For $f(x)=\frac{2x+1}{x-3}$ ($x\ne3$):

1. Put $y=\frac{2x+1}{x-3}$, so $y(x-3)=2x+1$.
2. Collect $x$: $x(y-2)=3y+1$, so $x=\frac{3y+1}{y-2}$.
3. Hence $f^{-1}(x)=\frac{3x+1}{x-2}$, with $x\ne2$.
4. Check: $f(f^{-1}(x))=x$. The graph of $f^{-1}$ is the reflection of $f$ in the line $y=x$.

**3. Composite functions.** Let $f(x)=2x+1$ and $g(x)=x^2$.

| Function | Rule | Value at $x=2$ |
|---|---|---|
| $f\circ g$ | $f(g(x))=2x^2+1$ | $9$ |
| $g\circ f$ | $g(f(x))=(2x+1)^2$ | $25$ |

So $f\circ g\ne g\circ f$ in general: composition is not commutative. It is associative, and $(f\circ g)^{-1}=g^{-1}\circ f^{-1}$.

**4. Types.** Even: $f(-x)=f(x)$ (e.g. $x^2$); odd: $f(-x)=-f(x)$ (e.g. $x^3$); one-one: $f(a)=f(b)\Rightarrow a=b$ (horizontal line test).

**Conclusion.** The inverse undoes the function, and the order matters when functions are composed.
