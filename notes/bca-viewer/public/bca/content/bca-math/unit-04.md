---
subject: Mathematics
grade: BCA
unit: 4
title: Indices, Logarithms, Polynomials and Quadratic Equations
hours: 3
area: Algebra
---

Algebra manipulation questions are the backbone of the BCA paper. Three of the 50 questions come from here, but the same skills are needed in sequences, matrices and calculus, so a weak spot costs you in other chapters too. The Dean's Office model asks the nature of roots of $x^2-8x+16=0$, a root-to-constant question, and simple equation word problems ("product of two consecutive even numbers is 288").

::: key What the paper asks from this chapter
- **Indices**: combine bases, solve $a^x=a^y$, evaluate fractional powers.
- **Logs**: product, quotient, power laws; change of base; given $\log 2$ and $\log 3$, find another.
- **Quadratics**: discriminant and nature of roots, $\alpha+\beta$ and $\alpha\beta$, forming equations, finding a constant.
- **Polynomials**: remainder and factor theorem, identities with $x+\frac{1}{x}$.
- **Equations and inequalities**: simultaneous equations, consecutive numbers, sign reversal.
:::

## 4.1 Laws of indices and surds

$a^ma^n=a^{m+n}$, $\frac{a^m}{a^n}=a^{m-n}$, $(a^m)^n=a^{mn}$, $(ab)^n=a^nb^n$, $a^0=1$, $a^{-n}=\frac{1}{a^n}$, $a^{m/n}=\sqrt[n]{a^m}$. If $a^x=a^y$ and $a\ne0,\pm1$ then $x=y$. Factor common powers: $2^{x+2}-2^x=2^x(4-1)=3\cdot2^x$. A **surd** such as $\sqrt{5}$ is an irrational root; $(\sqrt{a}+\sqrt{b})(\sqrt{a}-\sqrt{b})=a-b$ rationalises $\frac{1}{\sqrt{a}+\sqrt{b}}$.

## 4.2 Logarithms and their laws

$\log_a x=y\iff a^y=x$ ($a>0$, $a\ne1$, $x>0$). Laws: $\log(mn)=\log m+\log n$; $\log\frac{m}{n}=\log m-\log n$; $\log m^p=p\log m$; $\log_a a=1$; $\log_a1=0$; $\log_ab=\frac{1}{\log_ba}=\frac{\log b}{\log a}$; $a^{\log_ax}=x$. Standard values: $\log_{10}2\approx0.3010$, $\log_{10}3\approx0.4771$, $\log_{10}5=1-\log_{10}2\approx0.6990$. $\log(m+n)$ has **no** expansion.

## 4.3 Polynomials, remainder and factor theorem

- **Remainder theorem**: $f(x)\div(x-a)$ leaves remainder $f(a)$. **Factor theorem**: $(x-a)$ is a factor iff $f(a)=0$.
- $(a\pm b)^2=a^2\pm2ab+b^2$; $a^3\pm b^3=(a\pm b)(a^2\mp ab+b^2)$; if $a+b+c=0$ then $a^3+b^3+c^3=3abc$.
- If $x+\frac{1}{x}=k$ then $x^2+\frac{1}{x^2}=k^2-2$.

## 4.4 Quadratic equations, nature and sum and product of roots

For $ax^2+bx+c=0$: roots $\frac{-b\pm\sqrt{D}}{2a}$ with $D=b^2-4ac$.

| $D$ | Roots |
|---|---|
| $D>0$, perfect square | real, unequal, rational |
| $D>0$, not a square | real, unequal, irrational |
| $D=0$ | real and equal |
| $D<0$ | imaginary (complex conjugates) |

$\alpha+\beta=-\frac{b}{a}$, $\alpha\beta=\frac{c}{a}$, $\alpha^2+\beta^2=(\alpha+\beta)^2-2\alpha\beta$. The equation with roots $\alpha,\beta$ is $x^2-(\alpha+\beta)x+\alpha\beta=0$. Roots are opposite if $b=0$ and reciprocal if $a=c$. $ax^2+bx+c$ has extreme value $-\frac{D}{4a}$ at $x=-\frac{b}{2a}$.

## 4.5 Linear and simultaneous equations, inequalities, equation word problems

- Eliminate one variable; for $x+y=s$, $x-y=d$: $x=\frac{s+d}{2}$, $y=\frac{s-d}{2}$.
- **Consecutive integers**: $n,n+1,\dots$; consecutive even: $n,n+2,\dots$.
- **Inequalities**: multiplying or dividing by a negative reverses the sign. $|x|<a\iff-a<x<a$; $|x|>a\iff x<-a$ or $x>a$.
- **Radical equations**: square both sides, then check every root (extraneous roots appear).

## Formula and fact sheet

| Topic | Result |
|---|---|
| Discriminant | $D=b^2-4ac$ |
| Sum, product of roots | $-\frac{b}{a}$, $\frac{c}{a}$ |
| Remainder theorem | $f(a)$ |
| Log laws | $\log mn=\log m+\log n$, $\log m^p=p\log m$ |
| Change of base | $\log_ab=\frac{\log b}{\log a}$ |
| $x+\frac{1}{x}=k$ | $x^2+\frac{1}{x^2}=k^2-2$ |

## Chapter summary

- Reduce to a common base before equating indices.
- $\log(m+n)$ cannot be split; $\log(mn)$ can.
- $D$ decides the nature of roots; $D=0$ gives equal roots.
- Use $\alpha+\beta$ and $\alpha\beta$ instead of solving for the roots.
- $f(a)$ is the remainder on division by $(x-a)$.
- A negative multiplier reverses an inequality.
- Always substitute back after squaring.

## Practice questions

**Set A — Recall (20 questions)**

1. The value of $2^3\times2^4$ is
   (a) 64 (b) 32 (c) 128 (d) 256
2. The value of $\log_{10}1000$ is
   (a) 3 (b) 10 (c) 100 (d) 1
3. For $x\ne0$, $x^0$ equals
   (a) 0 (b) $x$ (c) undefined (d) 1
4. The sum of the roots of $x^2-5x+6=0$ is
   (a) 6 (b) 5 (c) $-5$ (d) 1
5. The product of the roots of $2x^2-7x+3=0$ is
   (a) $-\frac{3}{2}$ (b) $\frac{7}{2}$ (c) $\frac{3}{2}$ (d) $\frac{2}{3}$
6. The discriminant of $x^2-6x+9=0$ is
   (a) 36 (b) 18 (c) $-36$ (d) 0
7. $\log_a(mn)$ equals
   (a) $\log_am+\log_an$ (b) $\log_am\cdot\log_an$ (c) $\log_am-\log_an$ (d) $n\log_am$
8. The value of $8^{2/3}$ is
   (a) 2 (b) 4 (c) $\frac{16}{3}$ (d) 8
9. For the equation $x^2-8x+16=0$ the roots are
   (a) imaginary and unequal (b) rational and unequal (c) irrational (d) real and equal
10. The remainder when $x^2+3x+2$ is divided by $(x-1)$ is
    (a) 0 (b) 2 (c) 6 (d) 1
11. $\log_aa$ equals
    (a) 1 (b) 0 (c) $a$ (d) undefined
12. The value of $(\sqrt{5}+\sqrt{3})(\sqrt{5}-\sqrt{3})$ is
    (a) 8 (b) 2 (c) 15 (d) $\sqrt{2}$
13. If $x-5=1$, then $x+7$ equals
    (a) 5 (b) 7 (c) 13 (d) 12
14. $(x+y)^2$ equals
    (a) $x^2+y^2$ (b) $x^2+xy+y^2$ (c) $x^2-2xy+y^2$ (d) $x^2+2xy+y^2$
15. The roots of $x^2-9=0$ are
    (a) 3, $-3$ (b) 9, $-9$ (c) 3 only (d) 0, 9
16. If $2^x=32$, then $x$ is
    (a) 4 (b) 5 (c) 6 (d) 16
17. If one root of $x^2-7x+c=0$ is 3, then $c$ is
    (a) 10 (b) 21 (c) 12 (d) 4
18. The value of $\log_381$ is
    (a) 4 (b) 27 (c) 3 (d) 9
19. The solution of $-2x>6$ is
    (a) $x>-3$ (b) $x>3$ (c) $x<3$ (d) $x<-3$
20. $|x|<2$ means
    (a) $x<2$ (b) $-2<x<2$ (c) $x<-2$ or $x>2$ (d) $x>-2$

::: note Answers and explanations — Set A
**1.** (c) — 2⁷ = 128; multiplying powers adds exponents (not 2¹² = 4096 either).
**2.** (a) — 10³ = 1000.
**3.** (d) — any non-zero number to the power 0 is 1.
**4.** (b) — −b/a = 5.
**5.** (c) — c/a = 3/2.
**6.** (d) — 36 − 36 = 0, a perfect square.
**7.** (a) — product becomes a sum.
**8.** (b) — 8^(2/3) = (∛8)² = 4.
**9.** (d) — D = 64 − 64 = 0.
**10.** (c) — f(1) = 1 + 3 + 2 = 6.
**11.** (a) — a¹ = a.
**12.** (b) — a² − b² pattern: 5 − 3 = 2.
**13.** (c) — x = 6, so x + 7 = 13.
**14.** (d) — the middle term is +2xy.
**15.** (a) — x² = 9 has two roots, ±3.
**16.** (b) — 32 = 2⁵.
**17.** (c) — 9 − 21 + c = 0, so c = 12.
**18.** (a) — 3⁴ = 81.
**19.** (d) — dividing by −2 reverses the sign: x < −3.
**20.** (b) — |x| < 2 is a band around zero; (c) is |x| > 2.
:::

**Set B — Understanding (12 questions)**

1. If $3^{x+1}=81$, then $x$ is
   (a) 2 (b) 4 (c) 1 (d) 3
2. Given $\log_{10}2=0.301$, the value of $\log_{10}8$ is
   (a) 0.602 (b) 0.903 (c) 1.204 (d) 0.301
3. If $\alpha,\beta$ are the roots of $x^2-5x+6=0$, then $\alpha^2+\beta^2$ is
   (a) 13 (b) 25 (c) 37 (d) 11
4. If the roots of $x^2+px+q=0$ are 2 and 3, then $p+q$ is
   (a) 11 (b) $-1$ (c) 1 (d) 5
5. The quadratic equation whose roots are 2 and $-3$ is
   (a) $x^2-x-6=0$ (b) $x^2+5x+6=0$ (c) $x^2-5x-6=0$ (d) $x^2+x-6=0$
6. $kx^2-6x+9=0$ has equal roots when $k$ equals
   (a) 1 (b) 2 (c) 4 (d) 9
7. $(x-2)$ is a factor of $x^3-3x^2+kx+2$. Then $k$ is
   (a) 0 (b) 1 (c) 2 (d) $-1$
8. If $x+\frac{1}{x}=3$, then $x^2+\frac{1}{x^2}$ is
   (a) 5 (b) 6 (c) 7 (d) 9
9. The product of two consecutive even numbers is 288. Their sum is
   (a) 34 (b) 30 (c) 32 (d) 36
10. The sum of two numbers is 15 and their difference is 3. The larger is
    (a) 8 (b) 9 (c) 10 (d) 12
11. If $2^{x+2}-2^x=12$, then $x$ is
    (a) 1 (b) 3 (c) 4 (d) 2
12. The solution of $\sqrt{x+6}=x$ is
    (a) $-2$ (b) 6 (c) 3 (d) 3 and $-2$

::: note Answers and explanations — Set B
**1.** (d) — 81 = 3⁴, so x + 1 = 4.
**2.** (b) — log 8 = 3 log 2 = 0.903.
**3.** (a) — 5² − 2·6 = 13.
**4.** (c) — p = −5, q = 6, so p + q = 1.
**5.** (d) — sum −1, product −6, so x² + x − 6.
**6.** (a) — D = 36 − 36k = 0.
**7.** (b) — f(2) = 8 − 12 + 2k + 2 = 0 gives k = 1.
**8.** (c) — 3² − 2 = 7.
**9.** (a) — 16 × 18 = 288; sum 34.
**10.** (b) — (15 + 3)/2 = 9.
**11.** (d) — 2ˣ(4 − 1) = 12, so 2ˣ = 4.
**12.** (c) — x² − x − 6 = 0 gives 3 or −2, but −2 fails since √4 ≠ −2.
:::

**Set C — Application (8 questions)**

1. The value of $1^3+2^3+(-3)^3$ is
   (a) $-18$ (b) $-6$ (c) 0 (d) 18
2. The minimum value of $x^2-6x+11$ is
   (a) 11 (b) 3 (c) 0 (d) 2
3. The sum of the squares of two consecutive positive integers is 85. Their product is
   (a) 30 (b) 35 (c) 42 (d) 56
4. If $x-y=2$ and $x+y=10$, then $xy$ is
   (a) 20 (b) 24 (c) 16 (d) 32
5. If $x+\frac{1}{x}=\frac{5}{2}$, the values of $x$ are
   (a) 5 and $\frac{1}{5}$ (b) 3 and $\frac{1}{3}$ (c) 1 and 4 (d) 2 and $\frac{1}{2}$
6. The value of $\log_28+\log_39$ is
   (a) 5 (b) 6 (c) 17 (d) 4
7. The roots of $x^2-5x+k=0$ differ by 1. Then $k$ is
   (a) 4 (b) 5 (c) 6 (d) 8
8. How many integers $x$ satisfy $x>-1$ and $3x+2<14$?
   (a) 3 (b) 4 (c) 5 (d) 2

::: note Answers and explanations — Set C
**1.** (a) — a + b + c = 0, so the sum of cubes is 3abc = 3(1)(2)(−3) = −18.
**2.** (d) — (x − 3)² + 2, minimum 2.
**3.** (c) — 6² + 7² = 85, product 42.
**4.** (b) — x = 6, y = 4, xy = 24.
**5.** (d) — 2x² − 5x + 2 = 0 gives x = 2 or 1/2.
**6.** (a) — 3 + 2 = 5.
**7.** (c) — roots 2 and 3, so k = 6.
**8.** (b) — x < 4 and x > −1 gives 0, 1, 2, 3.
:::
