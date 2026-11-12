---
subject: Mathematics
grade: BCA
unit: 5
title: Sequences and Series
hours: 2
area: Algebra
---

Two questions a year come from sequences, and the Dean's Office model had a seven-day "1 paisa, 2 paisa, 4 paisa" savings problem. The question is almost always one of five things: the $n$th term of an AP or GP, a sum, an AM or GM, a "which term is", or a sum to infinity. Memorise the formulas below and each takes under a minute.

::: key What the paper asks from this chapter
- **AP**: $a_n=a+(n-1)d$, $S_n=\frac{n}{2}[2a+(n-1)d]$, three numbers in AP, insert means.
- **GP**: $a_n=ar^{n-1}$, $S_n=\frac{a(r^n-1)}{r-1}$, $S_\infty=\frac{a}{1-r}$.
- **Special sums**: $\sum n$, $\sum n^2$, $\sum n^3$, odd and even numbers.
- **Means**: $AM=\frac{a+b}{2}$, $GM=\sqrt{ab}$, and $AM\ge GM$.
:::

## 5.1 Arithmetic progression

- $a_n=a+(n-1)d$; number of terms $n=\frac{l-a}{d}+1$.
- $S_n=\frac{n}{2}[2a+(n-1)d]=\frac{n}{2}(a+l)$.
- $a,b,c$ in AP $\iff 2b=a+c$. For three numbers in AP write $a-d,a,a+d$ (sum $=3a$).
- To insert $m$ means between $a$ and $b$: $d=\frac{b-a}{m+1}$.
- If $S_n$ is given, $a_n=S_n-S_{n-1}$ and $a_1=S_1$.

```svgfig label="5.1" caption="Gauss's trick drawn as a rectangle. Writing the sum 1 + 2 + ... + n twice, once forwards and once backwards, makes a rectangle n wide and n + 1 tall, so S = n(n + 1)/2; for n = 10 that is 10 x 11 / 2 = 55 and for n = 100 it is 5,050. The bars on the right are an AP with a = 3, d = 4: the 10th term is 3 + 9 x 4 = 39 and the sum of ten terms is 10/2 x (3 + 39) = 210."
n = 10
assert sum(range(1, n + 1)) == n * (n + 1) // 2 == 55 and sum(range(1, 101)) == 5050
a, d = 3, 4; terms = [a + i * d for i in range(10)]
assert terms[-1] == a + 9 * d == 39 and sum(terms) == 210 == 10 * (2 * a + 9 * d) // 2
f = Fig(780, 320)
f.text(190, 22, "S + S reversed = n rows of (n + 1)", size=11.5, color=NAVY, bold=True)
c = 22; x0, y0 = 50, 40
for i in range(n):
    for j in range(n + 1):
        mine = j <= i
        f.box(x0 + j * c, y0 + i * c, c - 2, c - 2, "", fill=("#bfdbfe" if mine else "#fde68a"), stroke="#ffffff", r=1)
f.text(x0 + 6 * c, y0 + n * c + 20, "blue = 1 + 2 + ... + 10,  gold = the same sum turned round", size=10.5, color=SLATE)
f.text(x0 + 6 * c, y0 + n * c + 42, "2S = 10 x 11 = 110, so S = 55", size=11.5, color=RED, bold=True)
f.text(600, 22, "AP: 3, 7, 11, ... (d = 4)", size=11.5, color=NAVY, bold=True)
for i, t in enumerate(terms):
    f.box(430, 36 + i * 22, t * 5, 19, str(t), fill=("#bbf7d0" if i == 9 else "#dbeafe"), stroke=NAVY, size=10, bold=True, r=2)
f.text(440, 300, "a_10 = 39,   S_10 = 210", size=11.5, color=RED, bold=True, anchor="start")
f.text(440, 280, "S_n = (n/2)[2a + (n - 1)d]", size=10.5, color=SLATE, anchor="start")
```

## 5.2 Geometric progression

- $a_n=ar^{n-1}$, $r=\frac{a_2}{a_1}$. $S_n=\frac{a(r^n-1)}{r-1}$ for $r\ne1$; for $|r|<1$, $S_\infty=\frac{a}{1-r}$.
- $a,b,c$ in GP $\iff b^2=ac$. Three numbers in GP: $\frac{a}{r},a,ar$ (product $=a^3$).
- Recurring decimal: $0.\overline{6}=\frac{0.6}{1-0.1}=\frac{2}{3}$.
- **Harmonic progression**: the reciprocals of its terms form an AP.

```svgfig label="5.2" caption="A geometric progression grows or shrinks by a constant FACTOR. (a) 2, 6, 18, ... with r = 3: the sixth term is 2 x 3^5 = 486 and the sum of six terms is 2(3^6 - 1)/(3 - 1) = 728. (b) With |r| < 1 the sum settles: 1 + 1/2 + 1/4 + ... = a/(1 - r) = 2, drawn as a strip that is halved again and again. So 0.777... = 7/9 and 0.333... = 1/3."
from fractions import Fraction as F
g = [2 * 3 ** i for i in range(6)]; assert g[-1] == 486 and sum(g) == 728 == 2 * (3 ** 6 - 1) // (3 - 1)
ps = [F(1) - F(1, 2 ** k) + 1 for k in range(0, 8)]
assert F(1) / (1 - F(1, 2)) == 2 and F(7, 10) / (1 - F(1, 10)) == F(7, 9) and F(3, 10) / (1 - F(1, 10)) == F(1, 3)
f = Fig(780, 320)
f.text(190, 22, "(a) r = 3: terms explode", size=11.5, color=NAVY, bold=True)
for i, t in enumerate(g):
    h = 22 + t * 0.42
    f.box(30 + i * 56, 270 - h, 46, h, "", fill="#bfdbfe", stroke=NAVY, r=2)
    f.text(53 + i * 56, 270 - h - 8, str(t), size=10.5, color=NAVY, bold=True)
    f.text(53 + i * 56, 288, "t%d" % (i + 1), size=10, color=SLATE)
f.text(190, 310, "S_6 = 2(3^6 - 1)/2 = 728", size=11, color=RED, bold=True)
f.text(580, 22, "(b) r = 1/2: the sum stops at 2", size=11.5, color=NAVY, bold=True)
x = 430; W = 320
for k in range(7):
    w = W / 2 ** (k + 1) * 1.0
    f.box(x, 50, w, 70, ("1" if k == 0 else ("1/2" if k == 1 else ("1/4" if k == 2 else ""))), fill=(["#bfdbfe", "#bbf7d0", "#fde68a"][k % 3]), stroke=NAVY, size=10.5, bold=True, r=1); x += w
f.text(590, 140, "1 + 1/2 + 1/4 + ... fills a strip of length 2", size=10.5, color=SLATE)
f.text(590, 172, "S infinity = a/(1 - r) = 1/(1 - 1/2) = 2", size=11.5, color=NAVY, bold=True)
f.text(590, 204, "0.777... = 0.7/(1 - 0.1) = 7/9", size=11, color=TEAL, bold=True)
f.text(590, 228, "0.333... = 1/3", size=11, color=TEAL, bold=True)
f.text(590, 262, "needs |r| < 1 (here r = 1/2)", size=10.5, color=RED, bold=True)
f.text(590, 286, "for r = 3 there is no sum to infinity", size=10.5, color=RED, bold=True)
```

## 5.3 Special sums and mixed problems

| Sum | Value |
|---|---|
| $1+2+\dots+n$ | $\frac{n(n+1)}{2}$ |
| $1+3+5+\dots$ ($n$ odd numbers) | $n^2$ |
| $2+4+\dots+2n$ | $n(n+1)$ |
| $1^2+2^2+\dots+n^2$ | $\frac{n(n+1)(2n+1)}{6}$ |
| $1^3+2^3+\dots+n^3$ | $\left[\frac{n(n+1)}{2}\right]^2$ |

::: example Doubling savings
**Problem.** You save 1 paisa on day 1, 2 on day 2, 4 on day 3, and so on. Total for a week?

**Solution.** GP with $a=1$, $r=2$, $n=7$: $S=\frac{2^7-1}{2-1}=127$ paisa.
:::

```photogrid label="5.1" cols="3" ratio="1.0" caption="Fibonacci in two places. (a) Leonardo of Pisa, called Fibonacci (about 1170-1250), in an engraving: his book Liber Abaci (1202) carried Hindu-Arabic numerals to Europe and posed the rabbit problem that gives 1, 1, 2, 3, 5, 8, ... (b) His statue in the Camposanto of Pisa. (c) A sunflower head: its seeds spiral in 34 and 55 curves, two neighbouring Fibonacci numbers."
@ photo id="bcamath/fibport" cap="Fibonacci (Leonardo of Pisa)"
focus 0.5 0.35
@ photo id="bcamath/fibstatue" cap="Statue of Fibonacci, Pisa"
focus 0.5 0.25
@ photo id="bcamath/sunflower" cap="Sunflower: spirals in 34 and 55"
focus 0.5 0.5
```

```svgfig label="5.3" caption="Square sums, computed. For n = 10: the sum of n is 55, the sum of n^2 is 10 x 11 x 21 / 6 = 385, and the sum of n^3 is 3,025 = 55^2, so the sum of cubes is the SQUARE of the sum of integers. Partial sums of cubes for n = 1 to 6 are 1, 9, 36, 100, 225, 441, the squares of 1, 3, 6, 10, 15, 21. Also 1 + 3 + 5 + ... (n odd numbers) = n^2."
n = 10
s1 = sum(range(1, n + 1)); s2 = sum(i * i for i in range(1, n + 1)); s3 = sum(i ** 3 for i in range(1, n + 1))
assert (s1, s2, s3) == (55, 385, 3025) and s2 == n * (n + 1) * (2 * n + 1) // 6 and s3 == s1 ** 2
cum = [sum(i ** 3 for i in range(1, k + 1)) for k in range(1, 7)]; tri = [k * (k + 1) // 2 for k in range(1, 7)]
assert cum == [1, 9, 36, 100, 225, 441] and cum == [t * t for t in tri] and sum(range(1, 2 * 8, 2)) == 64
f = Fig(780, 320)
f.text(200, 22, "Sums for n = 10", size=11.5, color=NAVY, bold=True)
for j, (t, v, col) in enumerate([("sum of n = n(n+1)/2", s1, "#bfdbfe"), ("sum of n^2 = n(n+1)(2n+1)/6", s2, "#bbf7d0"), ("sum of n^3 = [n(n+1)/2]^2", s3, "#fde68a")]):
    y = 48 + j * 60; w = v * 0.095
    f.box(30, y, w, 34, "", fill=col, stroke=NAVY, r=3)
    f.text(30 + w + 8, y + 17, "{:,}".format(v), size=12, color=NAVY, bold=True, anchor="start", vmid=True)
    f.text(30, y + 50, t, size=10.5, color=SLATE, anchor="start", bold=True)
f.text(200, 250, "3,025 = 55 x 55: cubes add up to a perfect square", size=11, color=RED, bold=True)
f.text(200, 276, "odd numbers: 1 + 3 + 5 + ... + 15 = 8^2 = 64", size=10.5, color=TEAL, bold=True)
f.text(600, 22, "Cubes add to squares of triangular numbers", size=11, color=NAVY, bold=True)
for k in range(6):
    y = 48 + k * 40
    f.text(430, y + 14, "1^3 + ... + %d^3" % (k + 1), size=10.5, color=SLATE, anchor="start", vmid=True)
    f.box(560, y, cum[k] * 0.4 + 6, 26, "", fill="#dbeafe", stroke=NAVY, r=2)
    f.text(560 + cum[k] * 0.4 + 14, y + 13, "%d = %d^2" % (cum[k], tri[k]), size=10.5, color=TEAL, bold=True, anchor="start", vmid=True)
```

```svgfig label="5.4" caption="Fibonacci squares and the golden angle. (a) Squares of side 1, 1, 2, 3, 5, 8, 13 fit together into a rectangle 21 x 13. The ratios of neighbouring terms 2, 1.5, 1.667, 1.6, 1.625, 1.615 close in on the golden ratio 1.618. (b) Seeds placed at a turn of 137.5 degrees each (the golden angle) form the sunflower spirals; 300 seeds are plotted by the cell."
import math
fib = [1, 1]
while len(fib) < 7: fib.append(fib[-1] + fib[-2])
assert fib == [1, 1, 2, 3, 5, 8, 13] and sum(x * x for x in fib) == 13 * 21
rat = [fib[i + 1] / fib[i] for i in range(1, 6)]; assert [round(r, 3) for r in rat] == [1.0 * 2, 1.5, 1.667, 1.6, 1.625][:5] 
phi = (1 + math.sqrt(5)) / 2; assert round(phi, 3) == 1.618 and abs(fib[6] / fib[5] - phi) < 0.01
x0, y0, x1, y1 = 0, 0, 1, 1; sq = [(0, 0, 1)]
s = 1; sq.append((1, 0, 1)); x1 = 2
order = ["top", "left", "bottom", "right"]
for k in range(2, 7):
    side = fib[k]; d = order[(k - 2) % 4]
    if d == "top": assert x1 - x0 == side; sq.append((x0, y1, side)); y1 += side
    elif d == "left": assert y1 - y0 == side; sq.append((x0 - side, y0, side)); x0 -= side
    elif d == "bottom": assert x1 - x0 == side; sq.append((x0, y0 - side, side)); y0 -= side
    else: assert y1 - y0 == side; sq.append((x1, y0, side)); x1 += side
assert (x1 - x0, y1 - y0) == (13, 21)
f = Fig(780, 320); u = 9
cols = ["#bfdbfe", "#bbf7d0", "#fde68a", "#fecaca", "#e9d5ff", "#bfdbfe", "#bbf7d0"]
for (x, y, sd), col in zip(sq, cols):
    f.box(20 + (x - x0) * u, 20 + (y1 - y - sd) * u, sd * u, sd * u, str(sd) if sd >= 3 else "", fill=col, stroke=NAVY, size=12, bold=True, r=0)
f.text(160, 232, "21 x 13 rectangle from squares 1, 1, 2, 3, 5, 8, 13", size=10.5, color=SLATE)
f.text(160, 258, "ratios: 2, 1.5, 1.667, 1.6, 1.625, 1.615 -> 1.618", size=11, color=NAVY, bold=True)
f.text(160, 282, "golden ratio = (1 + sqrt 5)/2", size=11, color=TEAL, bold=True)
cx, cy = 560, 150; ga = math.radians(137.508)
for i in range(1, 301):
    r = 7.6 * math.sqrt(i); th = i * ga
    f.circle(cx + r * math.cos(th), cy + r * math.sin(th), 2.6, fill=("#f59e0b" if i % 2 else "#92400e"), stroke="#78350f", sw=0.4)
f.text(560, 22, "(b) 300 seeds at the golden angle 137.5 deg", size=11, color=NAVY, bold=True)
f.text(560, 300, "34 and 55 spirals appear", size=10.5, color=SLATE, bold=True)
```

## 5.4 Eight traps in sequences and series

Progression questions are formula questions with a hidden counting step. The usual errors are off-by-one slips in $n$, or applying an infinite-sum formula to a ratio that is too big. These eight traps are checked against the figures above.

1. **The $n$-th term has $n-1$, not $n$.** For an AP, $a_n=a+(n-1)d$, so the 10th term of $3,7,11,\ldots$ is $3+9\times4=39$ and not $3+10\times4$ (Fig 5.1). The same applies to a GP: $a_n=ar^{n-1}$, so the sixth term of $2,6,18,\ldots$ is $2\times3^5=486$. Always count how many steps you take from the first term.
2. **Count the terms before you sum.** The number of terms in $a,a+d,\ldots,l$ is $\frac{l-a}{d}+1$. The list $7,10,13,\ldots,100$ has $\frac{93}{3}+1=32$ terms, not 31. Then $S=\frac n2(a+l)$ is the quickest way to add them.
3. **Choose the symmetric form for three or four terms in AP.** Three terms are $a-d,a,a+d$, so their sum is $3a$ at once. Four terms are $a-3d,a-d,a+d,a+3d$ with common difference $2d$. The arithmetic mean of two numbers is $\frac{x+y}{2}$, and if $x,y,z$ are in AP then $2y=x+z$.
4. **The sum to infinity needs $|r|<1$.** $S_\infty=\frac{a}{1-r}$ is valid only when the ratio is between $-1$ and 1 (Fig 5.2). For $r=3$ the terms keep growing and there is no sum. Recurring decimals are good examples: $0.777\ldots=\frac{0.7}{1-0.1}=\frac79$.
5. **Geometric mean uses a square root and three terms in GP use $\frac ar,a,ar$.** The geometric mean of $x$ and $y$ is $\sqrt{xy}$, so the GM of 4 and 9 is 6, while the AM is 6.5. For positive numbers AM is never less than GM. If three numbers in GP have product 216, the middle number is $\sqrt[3]{216}=6$.
6. **Know the three standard sums and when to subtract.** $\sum n=\frac{n(n+1)}{2}$, $\sum n^2=\frac{n(n+1)(2n+1)}{6}$ and $\sum n^3=\left[\frac{n(n+1)}{2}\right]^2$ (Fig 5.3). For a sum that starts at 6 and ends at 20, use $S(20)-S(5)$, not $S(20)-S(6)$. The sum of the first $n$ odd numbers is $n^2$.
7. **Identify the type before using a formula.** A constant difference means AP and a constant ratio means GP, so check two gaps first. Some series are neither: $\frac{1}{1\cdot2}+\frac1{2\cdot3}+\cdots$ telescopes, because $\frac1{n(n+1)}=\frac1n-\frac1{n+1}$, so the sum of $n$ terms is $\frac{n}{n+1}$. Differences of differences point to a polynomial formula.
8. **Fibonacci questions use "add the last two".** The sequence $1,1,2,3,5,8,13,\ldots$ has $F_n=F_{n-1}+F_{n-2}$, and the ratio $\frac{F_{n+1}}{F_n}$ tends to $1.618$ (Fig 5.4). Check whether the question starts counting at $F_1=1$ or $F_0=0$. In money problems, equal yearly raises are an AP while percentage raises are a GP, so a salary of Rs 30,000 with a Rs 2,000 raise is an AP, and with a 5 percent raise it is a GP.

### 5.4.1 Worked checks

**Q. Find the 20th term and the sum of the first 20 terms of $3,7,11,\ldots$**

**Answer.** $a=3,d=4$, so $a_{20}=3+19\times4=79$. $S_{20}=\frac{20}{2}(3+79)=10\times82=820$. Check with the other formula: $\frac{20}{2}[6+19\times4]=10\times82=820$.

**Q. Find the sum of the first six terms of $2,6,18,\ldots$ and the sum to infinity of $8,4,2,\ldots$**

**Answer.** The first is a GP with $r=3$: $S_6=\frac{2(3^6-1)}{3-1}=728$, which matches Fig 5.2. The second has $r=\frac12$, so $S_\infty=\frac{8}{1-\frac12}=16$. The infinite sum exists because $|r|<1$.

**Q. Evaluate $1^2+2^2+\cdots+10^2$ and $1^3+2^3+\cdots+10^3$.**

**Answer.** $\sum n^2=\frac{10\times11\times21}{6}=385$. $\sum n^3=\left(\frac{10\times11}{2}\right)^2=55^2=3025$. These match the bars in Fig 5.3.

## Formula and fact sheet

| Item | AP | GP |
|---|---|---|
| $n$th term | $a+(n-1)d$ | $ar^{n-1}$ |
| Sum | $\frac{n}{2}[2a+(n-1)d]$ | $\frac{a(r^n-1)}{r-1}$ |
| Condition | $2b=a+c$ | $b^2=ac$ |
| Mean | $\frac{a+b}{2}$ | $\sqrt{ab}$ |

## Chapter summary

- Count terms first: $n=\frac{l-a}{d}+1$.
- $S_n$ for AP is $n$ times the average of first and last.
- Use $\frac{a}{r},a,ar$ for three GP numbers and $a-d,a,a+d$ for AP.
- $S_\infty$ exists only when $|r|<1$.
- $a_n=S_n-S_{n-1}$ recovers terms from sums.
- $AM\ge GM$, with equality only when the numbers are equal.

## Practice questions

**Set A — Recall (20 questions)**

1. The 10th term of the AP 2, 5, 8, … is
   (a) 27 (b) 30 (c) 32 (d) 29
2. The sum of the first 20 natural numbers is
   (a) 210 (b) 200 (c) 420 (d) 190
3. The 5th term of the GP 3, 6, 12, … is
   (a) 24 (b) 96 (c) 48 (d) 45
4. The arithmetic mean of 4 and 16 is
   (a) 8 (b) 10 (c) 12 (d) 20
5. The geometric mean of 4 and 16 is
   (a) 10 (b) 12 (c) 6 (d) 8
6. The sum $1+2+4+8+16+32+64$ is
   (a) 64 (b) 128 (c) 127 (d) 126
7. The sum of the first $n$ odd numbers is
   (a) $n^2$ (b) $n(n+1)$ (c) $\frac{n(n+1)}{2}$ (d) $2n$
8. The sum to infinity of $1+\frac{1}{2}+\frac{1}{4}+\cdots$ is
   (a) 1 (b) 2 (c) $\frac{3}{2}$ (d) infinite
9. If $a,b,c$ are in AP, then
   (a) $b^2=ac$ (b) $b=a+c$ (c) $2b=a+c$ (d) $b=ac$
10. The common ratio of 2, $-6$, 18, … is
    (a) 3 (b) $-2$ (c) 4 (d) $-3$
11. The sum of the first 10 even natural numbers is
    (a) 100 (b) 110 (c) 55 (d) 120
12. $1^3+2^3+3^3$ equals
    (a) 36 (b) 14 (c) 6 (d) 27
13. The common difference of 7, 4, 1, … is
    (a) 3 (b) 11 (c) $-4$ (d) $-3$
14. $1^2+2^2+3^2+4^2+5^2$ equals
    (a) 15 (b) 225 (c) 55 (d) 50
15. In a harmonic progression the reciprocals of the terms form
    (a) an AP (b) a GP (c) an HP (d) a constant sequence
16. The number of terms in the AP 5, 9, 13, …, 41 is
    (a) 9 (b) 10 (c) 11 (d) 12
17. The 3rd term of the GP with first term 2 and ratio 3 is
    (a) 12 (b) 9 (c) 18 (d) 54
18. The sum of the first $n$ natural numbers is
    (a) $n^2$ (b) $n(n+1)$ (c) $\frac{n(n-1)}{2}$ (d) $\frac{n(n+1)}{2}$
19. The sum to infinity of the GP 3, 1, $\frac{1}{3}$, … is
    (a) $\frac{9}{2}$ (b) 4 (c) 6 (d) 9
20. Which of the following is a GP?
    (a) 1, 3, 5, 7 (b) 3, 9, 27, 81 (c) 2, 4, 6, 8 (d) 1, 4, 9, 16

::: note Answers and explanations — Set A
**1.** (d) — 2 + 9 × 3 = 29.
**2.** (a) — 20 × 21 / 2 = 210.
**3.** (c) — 3 × 2⁴ = 48.
**4.** (b) — (4 + 16)/2 = 10.
**5.** (d) — √(4 × 16) = 8; GM is below AM.
**6.** (c) — (2⁷ − 1)/(2 − 1) = 127.
**7.** (a) — 1 + 3 + 5 + … = n².
**8.** (b) — a/(1 − r) = 1/(1/2) = 2.
**9.** (c) — the middle term is the average of its neighbours; (a) is for a GP.
**10.** (d) — 18 / (−6) = −3.
**11.** (b) — n(n + 1) = 10 × 11 = 110.
**12.** (a) — 1 + 8 + 27 = 36 = (1 + 2 + 3)².
**13.** (d) — 4 − 7 = −3.
**14.** (c) — 5 × 6 × 11 / 6 = 55.
**15.** (a) — that is the definition of an HP.
**16.** (b) — (41 − 5)/4 + 1 = 10.
**17.** (c) — 2 × 3² = 18.
**18.** (d) — n(n + 1)/2; (b) is the sum of even numbers.
**19.** (a) — 3 / (1 − 1/3) = 9/2.
**20.** (b) — constant ratio 3.
:::

**Set B — Understanding (12 questions)**

1. The sum of the first 10 terms of the AP 3, 7, 11, … is
   (a) 200 (b) 210 (c) 220 (d) 190
2. Which term of the AP 3, 8, 13, … is 78?
   (a) 14th (b) 15th (c) 17th (d) 16th
3. Three numbers in AP have sum 27. The middle number is
   (a) 9 (b) 8 (c) 10 (d) 12
4. Three numbers in GP have product 216. The middle number is
   (a) 8 (b) 12 (c) 6 (d) 9
5. A GP has first term 5 and fifth term 80, with positive ratio. The ratio is
   (a) 3 (b) 2 (c) 4 (d) 16
6. The sum $1+3+9+27+81+243$ is
   (a) 364 (b) 243 (c) 363 (d) 729
7. The first term of an AP is 3 and the sum of its first 5 terms is 35. The common difference is
   (a) 4 (b) 3 (c) 1 (d) 2
8. The sum of all multiples of 3 between 1 and 50 is
   (a) 400 (b) 425 (c) 408 (d) 416
9. The sum $2+4+6+\cdots+100$ is
   (a) 2,550 (b) 5,050 (c) 2,500 (d) 5,100
10. The sum to infinity of $0.6+0.06+0.006+\cdots$ is
    (a) 0.6 (b) 0.7 (c) 1 (d) $\frac{2}{3}$
11. For what $n$ is $1+2+\cdots+n=55$?
    (a) 9 (b) 11 (c) 10 (d) 12
12. If three arithmetic means are inserted between 4 and 20, the second mean is
    (a) 10 (b) 12 (c) 14 (d) 16

::: note Answers and explanations — Set B
**1.** (b) — 5(6 + 36) = 210.
**2.** (d) — 3 + (n − 1)5 = 78 gives n = 16.
**3.** (a) — sum = 3 × middle, so 27/3 = 9.
**4.** (c) — (a/r)(a)(ar) = a³ = 216, a = 6.
**5.** (b) — r⁴ = 16, so r = 2.
**6.** (a) — (3⁶ − 1)/2 = 364.
**7.** (d) — (5/2)(6 + 4d) = 35 gives d = 2.
**8.** (c) — 3, 6, …, 48 is 16 terms; 16(3 + 48)/2 = 408.
**9.** (a) — 50 × 51 = 2,550; 5,050 is the sum of 1 to 100.
**10.** (d) — 0.6/(1 − 0.1) = 2/3.
**11.** (c) — 10 × 11/2 = 55.
**12.** (b) — d = 16/4 = 4, so the means are 8, 12, 16.
:::

**Set C — Application (8 questions)**

1. A man saves Rs 100 in the first month and Rs 20 more each month than the month before. His total saving in 12 months is
   (a) Rs 2,400 (b) Rs 2,640 (c) Rs 2,520 (d) Rs 2,280
2. If the sum of the first $n$ terms of an AP is $3n^2+2n$, its common difference is
   (a) 6 (b) 5 (c) 3 (d) 11
3. A GP has first term 1 and common ratio 3. Its 5th term is
   (a) 27 (b) 64 (c) 243 (d) 81
4. Three numbers in GP have sum 14 and product 64. The largest is
   (a) 6 (b) 8 (c) 10 (d) 12
5. The sum $1^2+2^2+\cdots+10^2$ is
   (a) 3,025 (b) 55 (c) 385 (d) 100
6. The sum $1^3+2^3+\cdots+10^3$ is
   (a) 385 (b) 55 (c) 2,025 (d) 3,025
7. The sum of the AP 25, 22, 19, …, 1 is
   (a) 117 (b) 126 (c) 108 (d) 130
8. If $x$, $x+2$, $x+8$ are in GP, then $x$ is
   (a) 2 (b) 1 (c) 4 (d) 3

::: note Answers and explanations — Set C
**1.** (c) — (12/2)(200 + 11 × 20) = 6 × 420 = 2,520.
**2.** (a) — a₁ = 5, a₂ = 16 − 5 = 11, so d = 6.
**3.** (d) — 1 × 3⁴ = 81; (c) is the 6th term.
**4.** (b) — numbers 2, 4, 8: sum 14, product 64.
**5.** (c) — 10 × 11 × 21 / 6 = 385.
**6.** (d) — (55)² = 3,025.
**7.** (a) — 9 terms; 9 × (25 + 1)/2 = 117.
**8.** (b) — (x + 2)² = x(x + 8) gives 4x + 4 = 8x, x = 1.
:::
