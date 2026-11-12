---
subject: Mathematics
grade: IOE
unit: 2
title: Algebra
hours: 8
area: Mathematics
---

Algebra is the **largest block of the Mathematics paper** (our estimate: about 8 of 35 questions). It has four distinct families: matrices and determinants, complex numbers with polynomial equations, sequences with counting, and the binomial / exponential / logarithmic series. Each family has two or three standard question shapes. Learn the shapes and the paper becomes predictable.

::: key What the paper asks from this chapter
- Determinant properties: $|kA|=k^n|A|$, $|AB|=|A||B|$, $|\mathrm{adj}A|=|A|^{n-1}$, rows in AP give 0; the 2×2 inverse.
- Complex numbers: powers of $i$, modulus and argument, $\omega$ identities ($1+\omega+\omega^2=0$, $\omega^3=1$), De Moivre.
- Quadratics: sum and product of roots, discriminant, symmetric functions of roots, roots in a given ratio.
- AP / GP / HP: $n$-th term, sums, infinite GP, $\text{AM}\ge\text{GM}\ge\text{HM}$, $\sum n,\sum n^2,\sum n^3$.
- Counting: arrangements with repeated letters, restrictions (no two together, at least / at most), committees, diagonals.
- Binomial: general term, middle term, constant term, sum $2^n$, approximations; $e^x$ and $\ln(1+x)$ series coefficients.
:::

## 2.1 Matrices and determinants, types and properties, inverse of a matrix

A matrix is an array of $m\times n$ numbers. **Types:** square, row, column, diagonal, scalar, identity $I$, zero, upper / lower triangular, **symmetric** ($A^T=A$), **skew-symmetric** ($A^T=-A$, diagonal zero), **idempotent** ($A^2=A$), **involutory** ($A^2=I$), **nilpotent** ($A^k=0$), **orthogonal** ($AA^T=I$).

**Operations.** Add / subtract same-size matrices; $AB$ exists when columns of $A$ = rows of $B$ and is in general $AB\ne BA$. $(AB)^T=B^TA^T$, $(AB)^{-1}=B^{-1}A^{-1}$. Every square matrix is a sum of a symmetric and a skew-symmetric matrix, $A=\tfrac{1}{2}(A+A^T)+\tfrac{1}{2}(A-A^T)$.

**Determinant.** For $\begin{vmatrix}a&b \\ c&d\end{vmatrix}=ad-bc$; for 3×3 expand along a row with the signs $+-+$. Properties:
- swapping two rows changes the sign; two equal (or proportional) rows give 0;
- a common factor of a row comes out; so $|kA|=k^n|A|$ for an $n\times n$ matrix;
- adding a multiple of one row to another changes nothing;
- $|AB|=|A||B|$, $|A^T|=|A|$, $|A^{-1}|=1/|A|$, $|\mathrm{adj}A|=|A|^{n-1}$, $A\,\mathrm{adj}A=|A|I$.

**Inverse.** $A^{-1}=\dfrac{\mathrm{adj}A}{|A|}$ exists iff $|A|\ne0$ (non-singular). For a 2×2 matrix $A=[a\ b;\ c\ d]$ the inverse is $\dfrac{1}{ad-bc}[d\ -b;\ -c\ a]$: swap the diagonal, negate the other two. Elementary row operations reduce $[A\,|\,I]$ to $[I\,|\,A^{-1}]$.

**Linear systems.** Cramer's rule: $x=D_x/D$, $y=D_y/D$, $z=D_z/D$ when $D\ne0$. If $D=0$ the system has no solution or infinitely many. A homogeneous system has non-trivial solutions iff $D=0$.

::: tip Determinant shortcut
If the entries of the three rows are in arithmetic progression (as in $1,2,3;\ 4,5,6;\ 7,8,9$), $R_3-R_2=R_2-R_1$ makes the determinant 0 at once.
:::

## 2.2 Complex numbers and polynomial equations

$i^2=-1$; $i^{4k}=1$, $i^{4k+1}=i$, $i^{4k+2}=-1$, $i^{4k+3}=-i$. For $z=x+iy$: conjugate $\bar z=x-iy$, modulus $|z|=\sqrt{x^2+y^2}$, $z\bar z=|z|^2$, $\dfrac{1}{z}=\dfrac{\bar z}{|z|^2}$. The **argument** $\theta=\tan^{-1}(y/x)$ in the correct quadrant, principal value in $(-\pi,\pi]$. Polar form $z=r(\cos\theta+i\sin\theta)=re^{i\theta}$.

**De Moivre:** $(\cos\theta+i\sin\theta)^n=\cos n\theta+i\sin n\theta$. The $n$ roots of $z^n=1$ are $e^{2\pi ik/n}$, $k=0,\dots,n-1$. **Cube roots of unity:** $1,\omega,\omega^2$ with $\omega=\dfrac{-1+i\sqrt{3}}{2}$; $1+\omega+\omega^2=0$, $\omega^3=1$, $\omega^2=\bar\omega$. Useful: $1+\omega=-\omega^2$, $(1+\omega)^3=-1$.

Handy: $(1+i)^2=2i$, $\dfrac{1+i}{1-i}=i$, $|z_1z_2|=|z_1||z_2|$, $|z_1+z_2|\le|z_1|+|z_2|$.

### Polynomial equations

For $ax^2+bx+c=0$: roots $\dfrac{-b\pm\sqrt{D}}{2a}$, $D=b^2-4ac$; $\alpha+\beta=-\dfrac{b}{a}$, $\alpha\beta=\dfrac{c}{a}$. $D>0$ real distinct; $D=0$ equal; $D<0$ complex conjugate pair; for rational coefficients and $D$ a perfect square the roots are rational, and irrational roots $p+\sqrt{q}$ come with $p-\sqrt{q}$.

Symmetric functions: $\alpha^2+\beta^2=(\alpha+\beta)^2-2\alpha\beta$; $\alpha^3+\beta^3=(\alpha+\beta)^3-3\alpha\beta(\alpha+\beta)$; $(\alpha-\beta)^2=(\alpha+\beta)^2-4\alpha\beta$. The equation with roots $\alpha,\beta$ is $x^2-(\alpha+\beta)x+\alpha\beta=0$.

For $ax^3+bx^2+cx+d=0$: $\sum\alpha=-\dfrac{b}{a}$, $\sum\alpha\beta=\dfrac{c}{a}$, $\alpha\beta\gamma=-\dfrac{d}{a}$. A polynomial with real coefficients has complex roots in conjugate pairs (so an odd-degree one has at least one real root). **Factor theorem:** $(x-a)$ divides $f$ iff $f(a)=0$. Rational roots $p/q$ have $p\mid$ constant term, $q\mid$ leading coefficient.

## 2.3 Sequence and series, permutation and combination

### Progressions

| | AP | GP | HP |
|---|---|---|---|
| $n$-th term | $a+(n-1)d$ | $ar^{n-1}$ | reciprocals form an AP |
| sum of $n$ terms | $\frac{n}{2}[2a+(n-1)d]=\frac{n}{2}(a+l)$ | $\dfrac{a(r^n-1)}{r-1}$ | – |
| sum to infinity | – | $\dfrac{a}{1-r}$, $|r|<1$ | – |
| mean of $a,b$ | $\frac{a+b}{2}$ | $\sqrt{ab}$ | $\frac{2ab}{a+b}$ |

$\text{AM}\ge\text{GM}\ge\text{HM}$, and $\text{GM}^2=\text{AM}\cdot\text{HM}$ for two numbers. Three numbers in AP: $a-d,a,a+d$; in GP: $a/r,a,ar$. If $S_n$ is known, $t_n=S_n-S_{n-1}$.
**Standard sums:** $\sum n=\dfrac{n(n+1)}{2}$, $\sum n^2=\dfrac{n(n+1)(2n+1)}{6}$, $\sum n^3=\Big[\dfrac{n(n+1)}{2}\Big]^2$. Arithmetico-geometric series: multiply by $r$, subtract. Method of differences: write $t_r$ as $f(r)-f(r+1)$ so the sum telescopes.

### Counting

**Fundamental principle:** independent stages multiply, alternatives add.
$$^nP_r=\frac{n!}{(n-r)!},\quad ^nC_r=\frac{n!}{r!(n-r)!},\quad ^nC_r=\,^nC_{n-r},\quad ^nC_r+\,^nC_{r-1}=\,^{n+1}C_r.$$
- Arrangements of $n$ things with repeats $p,q,r$: $\dfrac{n!}{p!\,q!\,r!}$ (BANANA: $\dfrac{6!}{3!\,2!}=60$).
- Circular arrangements of $n$: $(n-1)!$; of a necklace (flip allowed): $\tfrac{1}{2}(n-1)!$.
- Words using all letters where certain letters stay together: glue them into one block, then multiply by the block's internal arrangements.
- **No two together:** arrange the others first, then place the restricted ones in the gaps: $n!\times\,^{(n+1)}P_r$.
- Digits: the first digit cannot be 0 (four-digit numbers with distinct digits: $9\times9\times8\times7=4536$).
- **At least / at most** selections: add cases or subtract the complement from $^nC_r$ total.
- Diagonals of an $n$-gon: $\dfrac{n(n-3)}{2}=\,^nC_2-n$. Triangles from $n$ points with $k$ collinear: $^nC_3-\,^kC_3$.
- Distribution of $n$ identical items into $r$ boxes (empty allowed): $^{n+r-1}C_{r-1}$.

## 2.4 Binomial theorem, exponential and logarithmic series

$(a+b)^n=\sum_{r=0}^{n}{}^nC_r\,a^{n-r}b^r$ has $n+1$ terms. General term $T_{r+1}={}^nC_r\,a^{n-r}b^r$. Middle term: $T_{n/2+1}$ if $n$ even; two middle terms $T_{(n+1)/2},T_{(n+3)/2}$ if $n$ odd. Constant term: set the power of $x$ to zero ($(x+1/x)^6$: $r=3$, $^6C_3=20$). Sum of coefficients $=2^n$ (put $x=1$); even-place sum = odd-place sum $=2^{n-1}$. Greatest coefficient is $^nC_{n/2}$ for even $n$. Ratio of consecutive terms: $\dfrac{T_{r+1}}{T_r}=\dfrac{n-r+1}{r}\cdot\dfrac{b}{a}$.

For any real $n$ and $|x|<1$:
$$(1+x)^n=1+nx+\frac{n(n-1)}{2!}x^2+\frac{n(n-1)(n-2)}{3!}x^3+\cdots$$
For small $x$: $(1+x)^n\approx1+nx$ (better: add the $x^2$ term). $(1-x)^{-1}=1+x+x^2+\cdots$.

$$e^x=\sum\frac{x^n}{n!},\quad e=\sum\frac{1}{n!}\approx2.71828,\quad a^x=\sum\frac{(x\ln a)^n}{n!},$$
$$\ln(1+x)=x-\frac{x^2}{2}+\frac{x^3}{3}-\cdots\ (-1<x\le1),\qquad \ln\frac{1+x}{1-x}=2\Big(x+\frac{x^3}{3}+\frac{x^5}{5}+\cdots\Big).$$
Also $\ln 2=1-\frac{1}{2}+\frac{1}{3}-\cdots$ and $e^{-1}=\sum\frac{(-1)^n}{n!}$.

```photogrid label="2.1" cols="2" ratio="1.2" caption="Logarithms turn multiplication into addition. (a) A slide rule: the scales are marked at distances proportional to log x, so sliding one scale along the other adds two lengths, and the sum of logarithms is the logarithm of the product (log a + log b = log ab). (b) The rule is modelled as 25 cm long, with x placed at 25 log10 x cm. Multiplying 2.5 by 3.2 adds 9.95 cm and 12.63 cm to give 22.58 cm, the position of 8.0. Reading a position to 0.1 mm limits the answer to about 0.09 per cent."
@ photo id="ioemath/sliderule" cap="A slide rule with its logarithmic scales"
fit 1.2
focus 0.5 0.5
@ svg cap="2.5 x 3.2 by adding lengths on a 25 cm scale"
import math
L = 25.0
pos = lambda x: L * math.log10(x)
a, b = pos(2.5), pos(3.2); prod = 10 ** ((a + b) / L)
err = math.log(10) * 0.01 / L
assert abs(prod - 8.0) < 1e-9 and abs(a - 9.95) < 0.01 and abs(b - 12.63) < 0.01 and abs(err * 100 - 0.092) < 0.001
X = lambda cm: 10 + cm * 280 / L
f = Fig(300, 236)
f.text(150, 14, "x is drawn at 25 log10(x) cm", size=10.5, color=NAVY, bold=True)
f.line(X(0), 60, X(L), 60, color=NAVY, sw=1.6)
for v in range(1, 11):
    f.line(X(pos(v)), 52, X(pos(v)), 68, color=NAVY, sw=1.2); f.text(X(pos(v)), 84, str(v), size=10.5, color=NAVY, bold=True)
f.box(X(0), 110, X(a) - X(0), 22, "9.95 cm  (2.5)", fill=SAND, stroke=AMBER, size=10.5, bold=True, r=3)
f.box(X(a), 110, X(a + b) - X(a), 22, "12.63 cm  (3.2)", fill=MINT, stroke=TEAL, size=10.5, bold=True, r=3)
f.arrow([(X(a + b), 140), (X(a + b), 94)], color=RED)
f.text(X(a + b), 154, "22.58 cm = 8.0", size=10.5, color=RED, bold=True, anchor="end")
f.text(150, 186, "log 2.5 + log 3.2 = %.4f + %.4f = log 8" % (math.log10(2.5), math.log10(3.2)), size=10.5, color=NAVY, bold=True)
f.text(150, 206, "reading error 0.1 mm: %.2f%% of the answer" % (err * 100), size=10.5, color=SLATE)
f.text(150, 226, "so three figures at best", size=10.5, color=SLATE)
```

## Formula and fact sheet

| Topic | Result |
|---|---|
| $|kA|$, $|\mathrm{adj}A|$ | $k^n|A|$, $|A|^{n-1}$ |
| 2×2 inverse | $\frac{1}{ad-bc}[d\ -b;\,-c\ a]$ |
| $\omega$ | $1+\omega+\omega^2=0$, $\omega^3=1$ |
| quadratic | $\alpha+\beta=-b/a$, $\alpha\beta=c/a$, $D=b^2-4ac$ |
| AP sum / GP sum | $\frac{n}{2}[2a+(n-1)d]$ / $a\frac{r^n-1}{r-1}$ |
| $\sum n^2$, $\sum n^3$ | $\frac{n(n+1)(2n+1)}{6}$, $[\frac{n(n+1)}{2}]^2$ |
| $^nC_r$, $^nP_r$ | $\frac{n!}{r!(n-r)!}$, $\frac{n!}{(n-r)!}$ |
| binomial | $T_{r+1}={}^nC_ra^{n-r}b^r$ |
| $e^x$, $\ln(1+x)$ | $\sum x^n/n!$, $x-x^2/2+x^3/3-\cdots$ |

## Chapter summary

- Determinants scale as $k^n$; rows in AP, or two proportional rows, give zero.
- $A^{-1}$ needs $|A|\ne0$; for 2×2 swap the diagonal and negate the rest.
- Reduce powers of $i$ and $\omega$ by their cycles (4 and 3).
- For any quadratic question first write the sum and product of the roots.
- $t_n=S_n-S_{n-1}$ and the infinite GP needs $|r|<1$.
- "No two together" = arrange the others, then fill gaps; "at least" = cases or complement.
- Constant term and coefficient questions are solved by the general term $T_{r+1}$.

## Practice questions

**Set A — Recall (16 questions)**

1. The determinant of the matrix $[2\ 3;\ 4\ 5]$ is
   (a) 22 (b) $-2$ (c) 2 (d) $-22$
2. If $A$ is a $3\times3$ matrix with $|A|=4$, then $|2A|$ equals
   (a) 8 (b) 16 (c) 32 (d) 64
3. For $A=[a\ b;\ c\ d]$ with $ad-bc\ne0$, $A^{-1}$ equals $\dfrac{1}{ad-bc}$ times
   (a) $[d\ -b;\ -c\ a]$ (b) $[d\ b;\ c\ a]$ (c) $[a\ -b;\ -c\ d]$ (d) $[-d\ b;\ c\ -a]$
4. The value of $i^{27}$ is
   (a) $i$ (b) $-i$ (c) 1 (d) $-1$
5. The principal argument of $-1+i$ is
   (a) $\pi/4$ (b) $-\pi/4$ (c) $3\pi/4$ (d) $-3\pi/4$
6. If $\omega$ is a complex cube root of unity, $(1+\omega)^3$ equals
   (a) $-1$ (b) 1 (c) 0 (d) 8
7. The product of the roots of $2x^2-7x+3=0$ is
   (a) $-7/2$ (b) $7/2$ (c) $-3/2$ (d) $3/2$
8. The 20th term of the AP $3,7,11,\dots$ is
   (a) 76 (b) 80 (c) 83 (d) 79
9. The sum to infinity of $9+3+1+\cdots$ is
   (a) 12 (b) 13.5 (c) 27 (d) 13
10. The value of $^8C_3$ is
    (a) 56 (b) 336 (c) 24 (d) 112
11. The number of distinct arrangements of the letters of BANANA is
    (a) 720 (b) 120 (c) 60 (d) 30
12. The number of terms in the expansion of $(x+y)^{10}$ is
    (a) 10 (b) 11 (c) 12 (d) 9
13. The sum of the binomial coefficients in $(1+x)^7$ is
    (a) 64 (b) 49 (c) 256 (d) 128
14. The coefficient of $x^3$ in $e^{2x}$ is
    (a) $8/3$ (b) $4/3$ (c) $2/3$ (d) $1/3$
15. The sum of the series $1-\frac{1}{2}+\frac{1}{3}-\frac{1}{4}+\cdots$ is
    (a) $\ln2$ (b) 1 (c) $e$ (d) $\pi/4$
16. A square matrix $A$ with $A^2=I$ is called
    (a) nilpotent (b) idempotent (c) involutory (d) orthogonal

::: note Answers and explanations — Set A
**1.** (b) — $2\cdot5-3\cdot4=-2$.
**2.** (c) — $|2A|=2^3|A|=32$. (b) wrongly uses $2^2$.
**3.** (a) — the adjoint of a 2×2 matrix swaps $a,d$ and negates $b,c$.
**4.** (b) — $27=4\cdot6+3$, so $i^{27}=i^3=-i$.
**5.** (c) — the point $(-1,1)$ is in the second quadrant: $\pi-\pi/4$.
**6.** (a) — $1+\omega=-\omega^2$, so $(1+\omega)^3=-\omega^6=-1$.
**7.** (d) — $c/a=3/2$. (b) is the sum.
**8.** (d) — $3+19\times4=79$.
**9.** (b) — $a=9$, $r=\frac{1}{3}$: $9/(1-\frac{1}{3})=13.5$.
**10.** (a) — $\frac{8\cdot7\cdot6}{3!}=56$; 336 is $^8P_3$.
**11.** (c) — $\frac{6!}{3!\,2!}=60$.
**12.** (b) — $n+1=11$.
**13.** (d) — $2^7=128$.
**14.** (b) — $\frac{(2x)^3}{3!}=\frac{8}{6}x^3=\frac{4}{3}x^3$.
**15.** (a) — it is $\ln(1+x)$ at $x=1$.
**16.** (c) — involutory. Idempotent is $A^2=A$.
:::

**Set B — Understanding (10 questions)**

1. If $A$ is $3\times3$ with $|A|=-3$, then $|\mathrm{adj}A|$ is
   (a) $-9$ (b) 9 (c) $-3$ (d) 27
2. The value of $\begin{vmatrix}1&2&3 \\ 4&5&6 \\ 7&8&9\end{vmatrix}$ is
   (a) 0 (b) 1 (c) $-1$ (d) 45
3. The value of $(1+i)^8$ is
   (a) 8 (b) $16i$ (c) 16 (d) $-16$
4. If $z=\dfrac{1+i}{1-i}$, then $z^{100}$ equals
   (a) $i$ (b) $-1$ (c) $-i$ (d) 1
5. If $\alpha,\beta$ are the roots of $2x^2-5x+1=0$, then $\alpha^2+\beta^2$ is
   (a) $25/4$ (b) $21/4$ (c) $23/4$ (d) $19/4$
6. The equation $x^2+kx+9=0$ has equal roots for
   (a) $k=\pm6$ (b) $k=6$ only (c) $k=3$ (d) $k=\pm3$
7. If $S_n=3n^2+2n$ for an AP, its 10th term is
   (a) 61 (b) 57 (c) 320 (d) 59
8. Three positive numbers are in GP and their product is 64. The middle number is
   (a) 8 (b) 2 (c) 4 (d) 16
9. Five boys and three girls are seated in a row so that no two girls sit together. The number of ways is
   (a) 4320 (b) 14400 (c) 720 (d) 40320
10. The constant term in the expansion of $\big(x+\frac{1}{x}\big)^6$ is
    (a) 15 (b) 6 (c) 20 (d) 30

::: note Answers and explanations — Set B
**1.** (b) — $|\mathrm{adj}A|=|A|^{n-1}=(-3)^2=9$.
**2.** (a) — rows in AP: $R_3-R_2=R_2-R_1$, so after operations a row of zeros appears.
**3.** (c) — $(1+i)^2=2i$, so $(1+i)^8=(2i)^4=16$.
**4.** (d) — $z=i$; $i^{100}=(i^4)^{25}=1$.
**5.** (b) — $\alpha+\beta=\frac{5}{2}$, $\alpha\beta=\frac{1}{2}$: $\frac{25}{4}-1=\frac{21}{4}$.
**6.** (a) — $D=k^2-36=0$ gives $k=\pm6$.
**7.** (d) — $S_{10}-S_9=320-261=59$ (general term $6n-1$).
**8.** (c) — the terms are $a/r,a,ar$; the product is $a^3=64$, so $a=4$.
**9.** (b) — boys: $5!=120$; the girls take 3 of the 6 gaps in order: $^6P_3=120$; $120\times120=14400$.
**10.** (c) — $T_{r+1}={}^6C_r x^{6-2r}$; constant when $r=3$: $^6C_3=20$.
:::

**Set C — Application (8 questions)**

1. If $\omega$ is a complex cube root of unity, $(1-\omega+\omega^2)(1+\omega-\omega^2)$ equals
   (a) 0 (b) 2 (c) 4 (d) 8
2. The roots of $x^2-6x+k=0$ are in the ratio $1:2$. Then $k$ equals
   (a) 8 (b) 9 (c) 12 (d) 6
3. The sum of all integers from 1 to 100 that are divisible by 3 or 5 is
   (a) 2733 (b) 2318 (c) 2468 (d) 2418
4. The number of four-digit numbers with all digits distinct is
   (a) 5040 (b) 4536 (c) 3024 (d) 4500
5. The number of diagonals of a decagon is
   (a) 45 (b) 40 (c) 35 (d) 25
6. A committee of 4 is chosen from 6 men and 4 women with at least 2 women. The number of ways is
   (a) 115 (b) 90 (c) 210 (d) 125
7. In $(1+x)^n$ the coefficients of the 5th, 6th and 7th terms are in AP. The sum of all possible values of $n$ is
   (a) 21 (b) 14 (c) 7 (d) 28
8. Using the first three terms of the binomial series, $(1.02)^5$ is approximately
   (a) 1.100 (b) 1.102 (c) 1.110 (d) 1.104

::: note Answers and explanations — Set C
**1.** (c) — $1+\omega^2=-\omega$, so the factors are $-2\omega$ and $-2\omega^2$; product $4\omega^3=4$.
**2.** (a) — roots $\alpha,2\alpha$: $3\alpha=6$, $\alpha=2$, $k=2\alpha^2=8$.
**3.** (d) — multiples of 3: $3\cdot\frac{33\cdot34}{2}=1683$; of 5: $5\cdot\frac{20\cdot21}{2}=1050$; of 15: $15\cdot\frac{6\cdot7}{2}=315$; $1683+1050-315=2418$.
**4.** (b) — $9\times9\times8\times7$; the first digit cannot be 0 (5040 is $10\times9\times8\times7$).
**5.** (c) — $\frac{10\cdot7}{2}=35$ ($^{10}C_2-10$).
**6.** (a) — $^4C_2\,^6C_2+{}^4C_3\,^6C_1+{}^4C_4=90+24+1=115$.
**7.** (a) — $^nC_4+{}^nC_6=2\,^nC_5$ reduces to $n^2-21n+98=0$: $n=7,14$; sum 21. Check $n=7$: $35+7=2\times21$.
**8.** (d) — $1+5(0.02)+10(0.02)^2=1+0.1+0.004=1.104$ (exact 1.10408).
:::

**Group D — Model answers for long questions (10 marks each, for deeper revision)**

1. Find the inverse of $A=\begin{pmatrix}1&2&3\\0&1&4\\5&6&0\end{pmatrix}$ and solve $x+2y+3z=6$, $y+4z=5$, $5x+6y=11$. State the properties of determinants. <span class="marks">[10]</span>
2. Solve problems on arrangements, committees, the binomial theorem and the exponential and logarithmic series. <span class="marks">[10]</span>

### Model answer D1: Matrix inverse and a linear system (10 marks)

**Introduction.** A square matrix $A$ has an inverse only if $\det A\ne0$, and $A^{-1}=\frac{1}{\det A}\operatorname{adj}A$.

**Step 1: determinant.** Expanding along the first row, $\det A=1(0-24)-2(0-20)+3(0-5)=-24+40-15=1$.

**Step 2: cofactors.** $C_{11}=-24$, $C_{12}=20$, $C_{13}=-5$, $C_{21}=18$, $C_{22}=-15$, $C_{23}=4$, $C_{31}=5$, $C_{32}=-4$, $C_{33}=1$.

**Step 3: adjoint and inverse.** The adjoint is the transpose of the cofactor matrix, and as $\det A=1$,
$$A^{-1}=\begin{pmatrix}-24&18&5\\20&-15&-4\\-5&4&1\end{pmatrix}.$$

**Step 4: solve $AX=B$** with $B=(6,5,11)^T$, so $X=A^{-1}B$.

| Row | Working | Value |
|---|---|---|
| $x$ | $-24(6)+18(5)+5(11)=-144+90+55$ | $1$ |
| $y$ | $20(6)-15(5)-4(11)=120-75-44$ | $1$ |
| $z$ | $-5(6)+4(5)+1(11)=-30+20+11$ | $1$ |

So $x=y=z=1$. **Check:** $1+2+3=6$, $1+4=5$, $5+6=11$. The same solution comes from **Cramer's rule**, $x=\frac{D_x}{D}$.

**Properties of determinants.**

1. $\det A^T=\det A$ and $\det(AB)=\det A\cdot\det B$.
2. Swapping two rows changes the sign; two equal rows give $0$.
3. Multiplying one row by $k$ multiplies the determinant by $k$.
4. Adding a multiple of one row to another leaves it unchanged.
5. $A\cdot\operatorname{adj}A=(\det A)I$.

**Conclusion.** The inverse method solves a system quickly when $\det A\ne0$; if $\det A=0$ the system has no unique solution.

### Model answer D2: Permutations, binomial theorem and series (10 marks)

**Introduction.** Counting and series are central in the IOE algebra paper.

**1. Permutations.** The letters of COMMITTEE (9 letters: M, T and E twice) can be arranged in $\frac{9!}{2!\,2!\,2!}=\frac{362880}{8}=45{,}360$ ways. A permutation is ${}^nP_r=\frac{n!}{(n-r)!}$ and a combination is ${}^nC_r=\frac{n!}{r!(n-r)!}$.

**2. Committees.** Choose 5 persons from 6 men and 4 women with at least 2 women. Total $={}^{10}C_5=252$. Subtract no woman ${}^6C_5=6$ and one woman ${}^4C_1\cdot{}^6C_4=60$. Answer: $252-6-60=186$.

**3. Binomial theorem.** $(a+b)^n=\sum{}^nC_ra^{n-r}b^r$ with general term $T_{r+1}={}^nC_ra^{n-r}b^r$.

1. Coefficient of $x^3$ in $(1+2x)^6$: ${}^6C_3\cdot2^3=20\times8=160$.
2. Term independent of $x$ in $\left(x^2+\frac1x\right)^9$: $T_{r+1}={}^9C_rx^{18-3r}$, which is $x^0$ when $r=6$, so the term is ${}^9C_6=84$.

**4. Series.**

| Series | Formula | Example |
|---|---|---|
| AP | $S_n=\frac n2[2a+(n-1)d]$ | $3,7,11,\dots$: $S_{20}=10(6+76)=820$ |
| GP (infinite) | $S_\infty=\frac{a}{1-r}$, $\lvert r\rvert<1$ | $8+4+2+\dots=16$ |
| Exponential | $e^x=1+x+\frac{x^2}{2!}+\dots$ | $e\approx2.7181$ (7 terms) |
| Logarithmic | $\ln(1+x)=x-\frac{x^2}{2}+\frac{x^3}{3}-\dots$ | $\ln1.1\approx0.0953$ |

The exponential value is $1+1+0.5+0.1667+0.0417+0.0083+0.0014=2.7181$.

**5. Complex numbers.** $(1+i)^8=\left(\sqrt2\right)^8\left(\cos2\pi+i\sin2\pi\right)=16$ by De Moivre's theorem. The cube roots of unity satisfy $1+\omega+\omega^2=0$ and $\omega^3=1$.

**Conclusion.** Choosing the right formula (arrangement with repetition, complementary counting, general term) gives the answer without long listing.
