---
subject: Mathematics
grade: BCA
unit: 3
title: Sets, Relations and Functions
hours: 2
area: Algebra
---

Sets and functions give about two questions in the paper, and they are among the most predictable: a Venn-diagram word problem, a count of subsets or relations, the domain of a function, and a composite or inverse. The Dean's Office model asks "A − (B ∪ C)" and a 120-student maths/statistics problem. Learn the counting formulas and the vocabulary, and these are quick marks.

::: key What the paper asks from this chapter
- **Venn counting**: $n(A\cup B)=n(A)+n(B)-n(A\cap B)$ and its three-set form.
- **Counting**: subsets $2^n$, proper subsets $2^n-1$, $n(A\times B)=mn$, relations $2^{mn}$.
- **Laws**: De Morgan, $A-B=A\cap B'$, distributive laws.
- **Relations**: reflexive, symmetric, transitive, equivalence.
- **Functions**: one-one, onto, domain of $\sqrt{\ }$ and $\frac{1}{x}$, composite and inverse.
:::

## 3.1 Sets, subsets, operations and Venn-diagram word problems

- A set with $n$ elements has $2^n$ subsets, $2^n-1$ proper subsets, and $\binom{n}{r}$ subsets of exactly $r$ elements. The power set has $2^n$ elements.
- $A-B=A\cap B'$. $A\,\Delta\,B=(A-B)\cup(B-A)$ and $n(A\Delta B)=n(A)+n(B)-2n(A\cap B)$.
- **De Morgan**: $(A\cup B)'=A'\cap B'$, $(A\cap B)'=A'\cup B'$.
- **Distributive**: $A-(B\cup C)=(A-B)\cap(A-C)$ and $A-(B\cap C)=(A-B)\cup(A-C)$.
- $n(A\cup B\cup C)=n(A)+n(B)+n(C)-n(A\cap B)-n(B\cap C)-n(C\cap A)+n(A\cap B\cap C)$.
- $A\cup A'=U$, $A\cap A'=\varnothing$, and $A\subseteq B$ gives $A\cup B=B$ and $A\cap B=A$.

::: example Maths and statistics
**Problem.** Of 120 students, 90 take mathematics and 72 take statistics; 10 take neither. How many take both?

**Solution.** $n(M\cup S)=120-10=110$. Both $=90+72-110=52$.
:::

```photogrid label="3.1" cols="3" ratio="1.0" caption="The people and places behind sets. (a) John Venn (1834-1923), the English logician who popularised the overlapping-circle diagram in 1880. (b) The Drypool Bridge in Hull, England, carries a giant Venn diagram as its decoration. (c) Georg Cantor (1845-1918), the founder of set theory, who proved that some infinite sets are strictly bigger than others."
@ photo id="bcamath/venn" cap="John Venn"
focus 0.5 0.3
@ photo id="bcamath/vennbridge" cap="Venn diagram on Drypool Bridge, Hull"
focus 0.45 0.5
@ photo id="bcamath/cantor" cap="Georg Cantor, founder of set theory"
focus 0.5 0.3
```

```svgfig label="3.1" caption="A three-set Venn diagram with every region counted. The eight regions add to 50 students. From the regions: n(A) = 12 + 5 + 3 + 2 = 22, n(B) = 21, n(C) = 17, and n(A union B union C) = 44 both by adding the seven shaded regions and by the inclusion-exclusion formula 22 + 21 + 17 - 7 - 6 - 5 + 2. Six students belong to none of the sets."
reg = {"A": 12, "B": 10, "C": 8, "AB": 5, "BC": 4, "CA": 3, "ABC": 2}; none = 6
tot = sum(reg.values()) + none; assert tot == 50
nA = reg["A"] + reg["AB"] + reg["CA"] + reg["ABC"]; nB = reg["B"] + reg["AB"] + reg["BC"] + reg["ABC"]; nC = reg["C"] + reg["BC"] + reg["CA"] + reg["ABC"]
nAB, nBC, nCA = reg["AB"] + reg["ABC"], reg["BC"] + reg["ABC"], reg["CA"] + reg["ABC"]
U = sum(reg.values()); assert (nA, nB, nC, U) == (22, 21, 17, 44) and nA + nB + nC - nAB - nBC - nCA + reg["ABC"] == 44
f = Fig(780, 320)
f.box(20, 12, 420, 296, "", fill="#f8fafc", stroke=SLATE, r=4); f.text(40, 30, "U = 50", size=11, color=SLATE, bold=True, anchor="start")
for (cx, cy, col, nm) in [(170, 125, "#2563eb", "A"), (270, 125, "#16a34a", "B"), (220, 205, "#d97706", "C")]:
    f.raw('<circle cx="%d" cy="%d" r="85" fill="%s" fill-opacity="0.22" stroke="%s" stroke-width="2"/>' % (cx, cy, col, col))
f.text(112, 62, "A", size=14, color="#2563eb", bold=True); f.text(328, 62, "B", size=14, color="#16a34a", bold=True); f.text(220, 300, "C", size=14, color="#d97706", bold=True)
for (x, y, k) in [(138, 115, "A"), (302, 115, "B"), (220, 252, "C"), (220, 100, "AB"), (178, 190, "CA"), (262, 190, "BC"), (220, 156, "ABC")]:
    f.text(x, y, str(reg[k]), size=15, color=NAVY, bold=True)
f.text(405, 290, "none: 6", size=11, color=RED, bold=True, anchor="end")
f.text(610, 34, "Counting with the regions", size=11.5, color=NAVY, bold=True)
rows = ["n(A) = 12+5+3+2 = 22", "n(B) = 10+5+4+2 = 21", "n(C) = 8+4+3+2 = 17", "n(A and B) = 5+2 = 7", "n(B and C) = 4+2 = 6", "n(C and A) = 3+2 = 5", "n(all three) = 2", "union = 22+21+17-7-6-5+2 = 44", "neither = 50 - 44 = 6", "only one set = 12+10+8 = 30"]
for j, t in enumerate(rows):
    f.text(480, 64 + j * 24, t, size=10.5, color=(RED if j in (7, 8) else SLATE), anchor="start", bold=(j in (7, 8)))
```

## 3.2 Relations and their types

- A relation from $A$ to $B$ is any subset of $A\times B$. If $n(A)=m$ and $n(B)=n$ there are $2^{mn}$ relations.
- On a set $A$: **reflexive** if $(a,a)\in R$ for all $a$; **symmetric** if $(a,b)\in R\Rightarrow(b,a)\in R$; **transitive** if $(a,b),(b,c)\in R\Rightarrow(a,c)\in R$; **equivalence** if all three.
- "$a$ divides $b$" on the positive integers is reflexive and transitive but not symmetric. "$=$" is an equivalence relation; "$<$" is only transitive.
- Domain = set of first coordinates; range = set of second coordinates that actually occur.

```svgfig label="3.2" caption="Subsets of {1, 2, 3}, counted by brute force in the cell. The 8 = 2^3 subsets sit in rows by size, 1 + 3 + 3 + 1 (Pascal's row). Proper subsets exclude the set itself, so 2^3 - 1 = 7; non-empty proper subsets are 2^3 - 2 = 6. The bars on the right show how fast 2^n grows: 10 elements already give 1,024 subsets."
import itertools, math
S = [1, 2, 3]
subs = [c for r in range(4) for c in itertools.combinations(S, r)]
assert len(subs) == 8 and [len([c for c in subs if len(c) == r]) for r in range(4)] == [1, 3, 3, 1]
assert [math.comb(3, r) for r in range(4)] == [1, 3, 3, 1] and 2 ** 10 == 1024
f = Fig(780, 320)
f.text(200, 20, "All 8 subsets of {1, 2, 3}", size=11.5, color=NAVY, bold=True)
lab = lambda c: "{" + ",".join(map(str, c)) + "}" if c else "{ } (empty)"
rowsy = {0: 60, 1: 120, 2: 190, 3: 255}
pos = {r: 0 for r in range(4)}
for c in subs:
    r = len(c); n = math.comb(3, r); w = 112; x0 = 200 - (n * w + (n - 1) * 8) / 2 + pos[r] * (w + 8); pos[r] += 1
    f.box(x0, rowsy[r], w, 34, lab(c), fill=("#bbf7d0" if r == 3 else ("#fecaca" if r == 0 else "#bfdbfe")), stroke=NAVY, size=10.5, bold=True, r=3)
for r, t in [(0, "size 0: 1 subset"), (1, "size 1: 3"), (2, "size 2: 3"), (3, "size 3: 1 (the set)")]:
    f.text(20, rowsy[r] + 50, t, size=10, color=SLATE, anchor="start")
f.text(600, 20, "Number of subsets 2^n", size=11.5, color=NAVY, bold=True)
for n in range(1, 11):
    y = 38 + (n - 1) * 27; w = 2 ** n * 0.3
    f.box(520, y, max(w, 2), 18, "", fill=("#fde68a" if n == 3 else "#bfdbfe"), stroke=NAVY, r=1)
    f.text(510, y + 9, "n=%d" % n, size=10, color=SLATE, anchor="end", vmid=True)
    f.text(520 + max(w, 2) + 6, y + 9, "{:,}".format(2 ** n), size=10, color=NAVY, bold=True, anchor="start", vmid=True)
```

```svgfig label="3.3" caption="Relations on {1, 2, 3}, by brute force. There are 2^9 = 512 relations (every subset of the 9 ordered pairs); 2^6 = 64 are reflexive, 2^6 = 64 are symmetric, and exactly 5 are equivalence relations (one for each way of splitting the set into groups: 1 + 3 + 1). The table tests four sample relations; only R2 is an equivalence relation."
import itertools
A = [1, 2, 3]; pairs = [(a, b) for a in A for b in A]
def refl(R): return all((a, a) in R for a in A)
def symm(R): return all((b, a) in R for (a, b) in R)
def trans(R): return all((a, d) in R for (a, b) in R for (c, d) in R if b == c)
allR = [set(c) for r in range(10) for c in itertools.combinations(pairs, r)]
nr = len(allR); nrefl = sum(refl(R) for R in allR); nsym = sum(symm(R) for R in allR); neq = sum(refl(R) and symm(R) and trans(R) for R in allR)
assert (nr, nrefl, nsym, neq) == (512, 64, 64, 5)
S = [("R1 = {(1,1),(2,2)}", {(1, 1), (2, 2)}), ("R2 = {(1,1),(2,2),(3,3),(1,2),(2,1)}", {(1, 1), (2, 2), (3, 3), (1, 2), (2, 1)}), ("R3 = {(1,1),(2,2),(3,3),(1,2)}", {(1, 1), (2, 2), (3, 3), (1, 2)}), ("R4 = {(1,2),(2,3),(1,3)}", {(1, 2), (2, 3), (1, 3)})]
f = Fig(780, 300)
hd = ["relation on {1,2,3}", "reflexive", "symmetric", "transitive", "equivalence"]; xs = [30, 400, 490, 585, 685]
for h, x in zip(hd, xs): f.text(x, 28, h, size=10.5, color=NAVY, bold=True, anchor="start")
for j, (nm, R) in enumerate(S):
    y = 60 + j * 44
    f.box(20, y - 16, 740, 38, "", fill=(MINT if refl(R) and symm(R) and trans(R) else SOFT), stroke="#cbd5e1", r=3)
    f.text(30, y + 3, nm, size=10, color=SLATE, anchor="start", vmid=True)
    for x, v in zip(xs[1:4], [refl(R), symm(R), trans(R)]):
        f.text(x + 18, y + 3, "yes" if v else "no", size=11, color=(TEAL if v else RED), bold=True, anchor="start", vmid=True)
    e = refl(R) and symm(R) and trans(R); f.text(xs[4] + 18, y + 3, "YES" if e else "no", size=11, color=(TEAL if e else RED), bold=True, anchor="start", vmid=True)
f.text(390, 250, "All 512 relations on 3 elements: 64 reflexive, 64 symmetric, 5 equivalence", size=11, color=NAVY, bold=True)
f.text(390, 276, "Empty relation: symmetric and transitive but NOT reflexive", size=10.5, color=RED, bold=True)
```

## 3.3 Functions, domain, range, composite and inverse functions

- A function from $A$ to $B$ gives every element of $A$ **exactly one** image. With $n(A)=m$, $n(B)=n$ there are $n^m$ functions and $\frac{n!}{(n-m)!}$ one-one functions ($m\le n$).
- **One-one**: different inputs, different outputs. **Onto**: range = codomain. **Bijective**: both.
- **Domain rules**: $\frac{1}{g(x)}$ needs $g(x)\ne0$; $\sqrt{g(x)}$ needs $g(x)\ge0$; $\log g(x)$ needs $g(x)>0$.
- **Composite**: $(f\circ g)(x)=f(g(x))$. In general $f\circ g\ne g\circ f$.
- **Inverse** exists only for a bijection: swap $x$ and $y$ and solve. If $f(x)=3x-6$ then $f^{-1}(x)=\frac{x+6}{3}$, and $f(f^{-1}(x))=x$.
- Even: $f(-x)=f(x)$ ($x^2$, $|x|$). Odd: $f(-x)=-f(x)$ ($x^3$, $\sin x$).

::: caution
$f(x)=x^2$ on $\mathrm{R}$ is neither one-one ($f(2)=f(-2)$) nor onto (no negative outputs). Check both before saying "bijective".
:::

```svgfig label="3.4" caption="The four kinds of mapping, with the counts checked by brute force. From A = {1, 2, 3} to B = {a, b} there are 2^3 = 8 functions, none one-one (3 > 2) and 6 onto; from {1, 2} to {a, b, c} there are 3^2 = 9 functions, 3 x 2 = 6 one-one and none onto. A function must give every element of A exactly one arrow; the range is the set of elements of B that are actually hit."
import itertools
def funcs(A, B): return [dict(zip(A, v)) for v in itertools.product(B, repeat=len(A))]
def one(g): return len(set(g.values())) == len(g)
def onto(g, B): return set(g.values()) == set(B)
A1, B1 = [1, 2, 3], ["a", "b"]; F1 = funcs(A1, B1)
assert (len(F1), sum(one(g) for g in F1), sum(onto(g, B1) for g in F1)) == (8, 0, 6)
A2, B2 = [1, 2], ["a", "b", "c"]; F2 = funcs(A2, B2)
assert (len(F2), sum(one(g) for g in F2), sum(onto(g, B2) for g in F2)) == (9, 6, 0)
f = Fig(780, 330)
cases = [("one-one, into", [1, 2], ["a", "b", "c"], {1: "a", 2: "b"}, "distinct arrows; c is not hit"),
         ("many-one, onto", [1, 2, 3], ["a", "b"], {1: "a", 2: "a", 3: "b"}, "two arrows meet at a"),
         ("one-one and onto", [1, 2, 3], ["a", "b", "c"], {1: "b", 2: "c", 3: "a"}, "bijection: inverse exists"),
         ("many-one, into", [1, 2, 3], ["a", "b", "c"], {1: "a", 2: "a", 3: "b"}, "c unused, a used twice")]
for i, (t, A, B, m, note) in enumerate(cases):
    cx = 15 + i * 192
    f.box(cx, 10, 180, 310, "", fill=SOFT, stroke="#cbd5e1", r=4)
    f.text(cx + 90, 24, t, size=11, color=NAVY, bold=True)
    ya = {e: 80 + k * 50 for k, e in enumerate(A)}; yb = {e: 80 + k * 50 for k, e in enumerate(B)}
    f.raw('<ellipse cx="%d" cy="130" rx="26" ry="%d" fill="#dbeafe" stroke="%s" stroke-width="1.4"/>' % (cx + 45, 18 + 26 * len(A), NAVY))
    f.raw('<ellipse cx="%d" cy="130" rx="26" ry="%d" fill="#fef3c7" stroke="%s" stroke-width="1.4"/>' % (cx + 135, 18 + 26 * len(B), AMBER))
    for e in A: f.text(cx + 45, ya[e] + 4, str(e), size=11, color=NAVY, bold=True)
    for e in B: f.text(cx + 135, yb[e] + 4, e, size=11, color=AMBER, bold=True)
    for e, v in m.items(): f.arrow([(cx + 58, ya[e]), (cx + 122, yb[v])], color=SLATE, sw=1.5)
    f.text(cx + 90, 262, note, size=10, color=SLATE)
    f.text(cx + 90, 290, "A to B" if i else "A to B", size=10, color=SLATE)
```

```svgfig label="3.5" caption="Composite and inverse functions for f(x) = 2x + 3 and g(x) = x^2. At x = 2: (f o g)(2) = f(4) = 11 but (g o f)(2) = g(7) = 49, so composition is not commutative. The inverse f^-1(x) = (x - 3)/2 undoes f (f^-1(7) = 2) and its graph is the mirror image of f in the line y = x."
fn = lambda x: 2 * x + 3; g = lambda x: x * x; inv = lambda y: (y - 3) / 2
assert fn(g(2)) == 11 and g(fn(2)) == 49 and inv(7) == 2 and all(inv(fn(x)) == x for x in range(-5, 6))
f = Fig(780, 320)
ax = Axes(f, 40, 20, 300, 270, (-4, 8), (-4, 8))
ax.grid(2, 2); ax.axes("x", "y")
ax.curve(fn, -4, 8, color=NAVY, sw=2.4); ax.curve(inv, -4, 8, color=TEAL, sw=2.4); ax.curve(lambda x: x, -4, 8, color=AMBER, sw=1.4, dash=True)
ax.pt(2, 7, "", r=4, color=RED); ax.pt(7, 2, "", r=4, color=RED)
f.text(300, 90, "f", size=12, color=NAVY, bold=True); f.text(300, 245, "f inverse", size=11, color=TEAL, bold=True, anchor="end"); f.text(290, 180, "y = x", size=10.5, color=AMBER, bold=True, anchor="end")
f.text(560, 30, "Composite and inverse at x = 2", size=11.5, color=NAVY, bold=True)
for j, (t, c) in enumerate([("(f o g)(x) = f(g(x)) = 2x^2 + 3", SLATE), ("(f o g)(2) = f(4) = 11", NAVY), ("(g o f)(x) = (2x + 3)^2", SLATE), ("(g o f)(2) = g(7) = 49", NAVY), ("11 and 49 differ: f o g is not g o f", RED), ("f inverse(x) = (x - 3)/2", TEAL), ("f inverse(7) = 2 because f(2) = 7", TEAL), ("(f o g) inverse = g inverse o f inverse", SLATE)]):
    f.text(420, 64 + j * 30, t, size=10.5, color=c, anchor="start", bold=(c in (RED, NAVY)))
```

## 3.4 Eight traps in sets, relations and functions

Set questions are shorter than they look, and nearly every wrong option is a plausible slip. These eight traps come from the model questions on subsets, equivalence relations and composite functions.

1. **The empty set is a subset of every set, and $\{\varnothing\}$ is not empty.** A set with $n$ elements has $2^n$ subsets, including $\varnothing$ and the set itself (Fig 3.2). The proper subsets exclude the set itself, so there are $2^n-1$, and the non-empty proper subsets number $2^n-2$. The set $\{\varnothing\}$ has one element, so $n(\{\varnothing\})=1$, not 0.
2. **"Neither" is the universal total minus the union.** If 100 students are asked and 60 like tea, 50 like coffee and 20 like both, the union is $60+50-20=90$ and 10 like neither. Always subtract the intersection once, or the overlap is counted twice. With three sets use the full formula with the triple intersection added back (Fig 3.1).
3. **"Only A" is not the same as "A".** The region "only A" removes the parts shared with $B$ and $C$, so in Fig 3.1 only A has 12 students while $n(A)$ is 22. A question that says "exactly two of the sets" wants $5+4+3=12$, and "at least two" adds the triple region to get 14. Read these words carefully and draw the diagram.
4. **$A-B$ is not $B-A$, and De Morgan flips the sign.** $A-B=A\cap B'$ is what is in $A$ but not in $B$. The laws $(A\cup B)'=A'\cap B'$ and $(A\cap B)'=A'\cup B'$ swap union and intersection when you take the complement. A symmetric difference takes both one-sided parts, so $n(A\Delta B)=n(A)+n(B)-2n(A\cap B)$.
5. **A relation is a set of ordered pairs.** $(a,b)$ is not the same as $(b,a)$, so $n(A\times B)=mn$ and the number of relations from $A$ to $B$ is $2^{mn}$, which is 512 for $A=B=\{1,2,3\}$ (Fig 3.3). The number of reflexive relations is $2^{n^2-n}=64$ because the diagonal pairs are forced. Do not confuse the count of relations with the count of functions.
6. **Equivalence needs all three properties.** Reflexive, symmetric and transitive must all hold. The relation $\{(1,1),(2,2)\}$ on $\{1,2,3\}$ is not reflexive because $(3,3)$ is missing, and $\{(1,2),(2,1)\}$ is symmetric but not transitive. The empty relation is symmetric and transitive but not reflexive on a non-empty set.
7. **A function gives every input exactly one output.** Domain is the set of inputs, codomain is the set where outputs may lie, and range is the set of outputs actually reached (Fig 3.4). Onto means range equals codomain, and one-one means different inputs give different outputs. For $m$ inputs and $n$ outputs there are $n^m$ functions, and $n(n-1)\cdots(n-m+1)$ of them are one-one.
8. **Composite order is right to left, and only a bijection has an inverse.** $(f\circ g)(x)=f(g(x))$ means apply $g$ first, and in general $f\circ g\neq g\circ f$ (Fig 3.5). An inverse exists only when the function is both one-one and onto, and then $(f\circ g)^{-1}=g^{-1}\circ f^{-1}$ with the order reversed. To find $f^{-1}$, write $y=f(x)$, solve for $x$, then swap the letters.

### 3.4.1 Worked checks

**Q. In a class of 80, 45 play football, 38 play volleyball and 12 play both. How many play neither and how many play exactly one game?**

**Answer.** Union $=45+38-12=71$, so neither $=80-71=9$. Exactly one game $=71-12=59$, and the check $33+26=59$ (football only $45-12=33$, volleyball only $38-12=26$) agrees. The 9 plus 59 plus 12 add to 80.

**Q. How many relations, and how many reflexive relations, are there on a set with 3 elements?**

**Answer.** There are $3\times3=9$ ordered pairs and each is either in or out, so $2^9=512$ relations. A reflexive relation must contain the 3 diagonal pairs, so only the other 6 pairs are free: $2^6=64$. Fig 3.3 confirmed both numbers by listing every relation.

**Q. If $f(x)=2x+3$ and $g(x)=x^2$, find $(f\circ g)(2)$, $(g\circ f)(2)$ and $f^{-1}(7)$.**

**Answer.** $g(2)=4$ so $(f\circ g)(2)=f(4)=11$. $f(2)=7$ so $(g\circ f)(2)=g(7)=49$. For the inverse, $y=2x+3$ gives $x=\frac{y-3}{2}$, so $f^{-1}(7)=\frac{7-3}{2}=2$, which agrees with $f(2)=7$.

## Formula and fact sheet

| Item | Result |
|---|---|
| Subsets / proper subsets | $2^n$ / $2^n-1$ |
| $n(A\times B)$ | $mn$ |
| Relations from $A$ to $B$ | $2^{mn}$ |
| Functions / one-one functions | $n^m$ / $\frac{n!}{(n-m)!}$ |
| $n(A\cup B)$ | $n(A)+n(B)-n(A\cap B)$ |
| De Morgan | $(A\cup B)'=A'\cap B'$ |

## Chapter summary

- Count with $n(A\cup B)=n(A)+n(B)-n(A\cap B)$; "neither" is the total minus the union.
- A set of $n$ elements has $2^n$ subsets, one of them the empty set.
- $A-B$ means $A\cap B'$.
- Equivalence = reflexive + symmetric + transitive.
- A function gives each input exactly one output; check one-one and onto separately.
- Domain: no zero denominators, no negative square roots, positive log arguments.
- To invert, swap $x$ and $y$; to compose, work from the inside out.

## Practice questions

**Set A — Recall (20 questions)**

1. The number of subsets of a set with 3 elements is
   (a) 6 (b) 8 (c) 9 (d) 3
2. If $n(A)=3$ and $n(B)=4$, then $n(A\times B)$ is
   (a) 7 (b) 1 (c) 81 (d) 12
3. $A-B$ equals
   (a) $A\cap B'$ (b) $A'\cap B$ (c) $A\cup B'$ (d) $A'\cup B$
4. By De Morgan's law, $(A\cup B)'$ equals
   (a) $A'\cup B'$ (b) $A\cap B$ (c) $A'\cap B'$ (d) $A\cup B'$
5. The number of proper subsets of $\{a,b,c\}$ is
   (a) 6 (b) 8 (c) 3 (d) 7
6. A relation that is reflexive, symmetric and transitive is called
   (a) a partial order (b) an equivalence relation (c) a function (d) an identity map
7. If $f(x)=2x+3$, then $f(4)$ is
   (a) 11 (b) 9 (c) 14 (d) 8
8. The domain of $f(x)=\frac{1}{x-2}$ is
   (a) all real numbers (b) $x>2$ (c) $\mathrm{R}-\{2\}$ (d) $x\ne-2$
9. If $f(x)=x^2$ and $g(x)=x+1$, then $(f\circ g)(2)$ is
   (a) 5 (b) 9 (c) 25 (d) 6
10. The inverse of $f(x)=3x-6$ is
    (a) $3x+6$ (b) $\frac{x-6}{3}$ (c) $\frac{x}{3}-6$ (d) $\frac{x+6}{3}$
11. If $n(A)=20$, $n(B)=15$ and $n(A\cap B)=5$, then $n(A\cup B)$ is
    (a) 30 (b) 35 (c) 40 (d) 25
12. Which of the following is the empty set?
    (a) $\{0\}$ (b) $\{\varnothing\}$ (c) $\{x\in\mathrm{R}: x^2=-1\}$ (d) $\{x: x=x\}$
13. $A\cap A'$ equals
    (a) $A$ (b) $U$ (c) $A'$ (d) $\varnothing$
14. The range of $f(x)=x^2$, $x\in\mathrm{R}$, is
    (a) $y\ge0$ (b) all real numbers (c) $y>0$ (d) $y\le0$
15. A function that is both one-one and onto is called
    (a) injective only (b) bijective (c) constant (d) identity only
16. If $A\subseteq B$, then $A\cup B$ equals
    (a) $A$ (b) $A\cap B$ (c) $B$ (d) $U$
17. The number of relations from a 2-element set to a 3-element set is
    (a) 64 (b) 36 (c) 8 (d) 9
18. The function $f(x)=x^3$ is
    (a) even (b) neither even nor odd (c) constant (d) odd
19. $A\cup A$ equals
    (a) $\varnothing$ (b) $A$ (c) $U$ (d) $A'$
20. The number of elements in the power set of a 4-element set is
    (a) 8 (b) 4 (c) 16 (d) 32

::: note Answers and explanations — Set A
**1.** (b) — 2³ = 8, including the empty set and the set itself.
**2.** (d) — n(A×B) = 3 × 4 = 12.
**3.** (a) — A − B keeps what is in A and not in B: A ∩ B′.
**4.** (c) — complement of a union is the intersection of complements.
**5.** (d) — 2³ − 1 = 7; only the set itself is excluded.
**6.** (b) — the three properties together define an equivalence relation.
**7.** (a) — 2(4) + 3 = 11.
**8.** (c) — the denominator vanishes only at x = 2.
**9.** (b) — g(2) = 3 and f(3) = 9. (f∘g) means g first.
**10.** (d) — y = 3x − 6 gives x = (y + 6)/3.
**11.** (a) — 20 + 15 − 5 = 30.
**12.** (c) — x² = −1 has no real solution. {0} and {∅} each have one element.
**13.** (d) — nothing is in both A and its complement.
**14.** (a) — squares are never negative, and 0 is attained.
**15.** (b) — one-one and onto together is bijective.
**16.** (c) — if A is inside B, joining adds nothing new.
**17.** (a) — subsets of a 6-element product: 2⁶ = 64.
**18.** (d) — (−x)³ = −x³.
**19.** (b) — idempotent law.
**20.** (c) — 2⁴ = 16.
:::

**Set B — Understanding (12 questions)**

1. Of 120 students, 90 take mathematics, 72 take statistics and 10 take neither. The number taking both is
   (a) 42 (b) 48 (c) 52 (d) 62
2. In a class of 40, 25 play football, 20 play cricket and 5 play neither. The number playing both is
   (a) 10 (b) 15 (c) 5 (d) 20
3. The domain of $f(x)=\sqrt{x-3}$ is
   (a) $x>3$ (b) $x\le3$ (c) all real numbers (d) $x\ge3$
4. If $f(x)=2x+1$ and $g(x)=x^2$, then $(f\circ g)(3)$ is
   (a) 7 (b) 19 (c) 49 (d) 13
5. The number of functions from a 3-element set to a 2-element set is
   (a) 8 (b) 9 (c) 6 (d) 5
6. $R=\{(1,1),(2,2),(3,3),(1,2)\}$ on $\{1,2,3\}$ is
   (a) symmetric only (b) an equivalence relation (c) reflexive and transitive but not symmetric (d) not reflexive
7. If $f(x)=3x+2$, then $f^{-1}(11)$ is
   (a) 1 (b) 2 (c) 5 (d) 3
8. If $A=\{1,2,3\}$ and $B=\{2,3,4\}$, then $(A-B)\cup(B-A)$ is
   (a) $\{2,3\}$ (b) $\{1,4\}$ (c) $\{1,2,3,4\}$ (d) $\{1\}$
9. If $f(x)=|x|$, then $f(-3)+f(3)$ is
   (a) 0 (b) 3 (c) 6 (d) $-6$
10. The function $f(x)=x^2+1$ on $\mathrm{R}$ is
    (a) one-one and onto (b) one-one into (c) many-one onto (d) many-one into
11. If $n(A)=4$, $n(B)=3$ and $n(A\cap B)=2$, then $n(A\,\Delta\,B)$ is
    (a) 3 (b) 5 (c) 1 (d) 7
12. The number of one-one functions from $\{1,2\}$ to $\{a,b,c\}$ is
    (a) 9 (b) 6 (c) 8 (d) 5

::: note Answers and explanations — Set B
**1.** (c) — union = 110; both = 90 + 72 − 110 = 52.
**2.** (a) — union = 35; both = 25 + 20 − 35 = 10.
**3.** (d) — need x − 3 ≥ 0; at x = 3 the root is 0, which is defined.
**4.** (b) — g(3) = 9, f(9) = 19. Computing g(f(3)) = 49 reverses the order.
**5.** (a) — each of 3 inputs has 2 choices: 2³ = 8; (b) is 3².
**6.** (c) — reflexive, transitive, but (1,2) has no (2,1).
**7.** (d) — 3x + 2 = 11 gives x = 3.
**8.** (b) — A − B = {1}, B − A = {4}.
**9.** (c) — 3 + 3 = 6.
**10.** (d) — f(1) = f(−1), and the range is y ≥ 1, not all of ℝ.
**11.** (a) — 4 + 3 − 2·2 = 3.
**12.** (b) — 3 × 2 = 6 ordered choices without repetition.
:::

**Set C — Application (8 questions)**

1. In a group of 100 people, 60 like tea, 50 like coffee and 20 like both. The number liking neither is
   (a) 0 (b) 5 (c) 20 (d) 10
2. If $f(x)=2x-1$ and $g(x)=\frac{x+1}{2}$, then $f(g(x))$ equals
   (a) 0 (b) $x$ (c) $2x$ (d) $x+1$
3. The number of subsets of a 5-element set having exactly 2 elements is
   (a) 10 (b) 20 (c) 5 (d) 25
4. On the positive integers, "$a$ divides $b$" is
   (a) an equivalence relation (b) symmetric (c) reflexive and transitive but not symmetric (d) symmetric and transitive only
5. If $f(x)=ax+b$, $f(1)=5$ and $f(2)=8$, then $f(5)$ is
   (a) 15 (b) 17 (c) 20 (d) 14
6. In a universal set of 50 elements, $n(A)=30$, $n(B)=25$ and $n(A\cup B)=45$. Then $n(A\cap B)$ is
   (a) 5 (b) 15 (c) 20 (d) 10
7. The range of $f(x)=3x-2$ defined on $\{1,2,3\}$ is
   (a) $\{1,4,7\}$ (b) $\{3,6,9\}$ (c) $\{2,4,6\}$ (d) $\{1,2,3\}$
8. The number of functions from $\{1,2\}$ to $\{a,b,c\}$ is
   (a) 8 (b) 6 (c) 9 (d) 64

::: note Answers and explanations — Set C
**1.** (d) — union = 60 + 50 − 20 = 90, so neither = 10.
**2.** (b) — 2·(x+1)/2 − 1 = x; f and g are inverses.
**3.** (a) — C(5,2) = 10.
**4.** (c) — a | a and transitive, but 2 | 4 does not give 4 | 2.
**5.** (b) — a = 3, b = 2, so f(5) = 17.
**6.** (d) — 30 + 25 − 45 = 10.
**7.** (a) — f(1), f(2), f(3) = 1, 4, 7.
**8.** (c) — 3² = 9; (b) 6 counts only the one-one ones.
:::
