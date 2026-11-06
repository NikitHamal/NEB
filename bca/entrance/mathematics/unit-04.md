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

```svgfig label="4.1" caption="Indices as graphs and as numbers. (a) y = 2^x grows without limit and y = (1/2)^x decays; both pass through (0, 1) because a^0 = 1, and neither ever touches the x-axis. (b) The laws checked on numbers in the cell: 2^5 x 2^3 = 2^8 = 256, (2^3)^2 = 64, 2^-2 = 1/4, 8^(2/3) = 4, 27^(-1/3) = 1/3, and sqrt(72) = 6 sqrt(2)."
import math
assert 2 ** 5 * 2 ** 3 == 2 ** 8 == 256 and (2 ** 3) ** 2 == 64 and 2 ** -2 == 0.25
assert round(8 ** (2 / 3), 9) == 4 and round(27 ** (-1 / 3), 9) == round(1 / 3, 9)
assert round(math.sqrt(72), 9) == round(6 * math.sqrt(2), 9) and round(1 / (math.sqrt(3) - 1), 6) == round((math.sqrt(3) + 1) / 2, 6)
f = Fig(780, 320)
ax = Axes(f, 40, 30, 300, 250, (-3, 3), (0, 8))
ax.grid(1, 2, size=10); ax.axes("x", "y")
ax.curve(lambda x: 2 ** x, -3, 3, color=NAVY, sw=2.4); ax.curve(lambda x: 0.5 ** x, -3, 3, color=TEAL, sw=2.4)
ax.pt(0, 1, "(0, 1)", r=4, color=RED, dx=8, dy=-10, size=10.5)
f.text(305, 60, "2^x", size=12, color=NAVY, bold=True); f.text(78, 60, "(1/2)^x", size=12, color=TEAL, bold=True)
f.text(560, 26, "The laws on real numbers", size=11.5, color=NAVY, bold=True)
cards = [("a^m x a^n = a^(m+n)", "2^5 x 2^3 = 2^8 = 256"), ("(a^m)^n = a^(mn)", "(2^3)^2 = 2^6 = 64"), ("a^-n = 1 / a^n", "2^-2 = 1/4 = 0.25"), ("a^(m/n) = (n-th root of a)^m", "8^(2/3) = 2^2 = 4"), ("a^0 = 1  (a not 0)", "27^(-1/3) = 1/3"), ("surd: sqrt(72) = sqrt(36 x 2)", "= 6 sqrt(2) = 8.485"), ("rationalise 1/(sqrt3 - 1)", "= (sqrt3 + 1)/2 = 1.366")]
for j, (a, b) in enumerate(cards):
    y = 40 + j * 39
    f.box(400, y, 360, 34, "", fill=(SOFT if j % 2 == 0 else BLUE), stroke="#cbd5e1", r=3)
    f.text(410, y + 17, a, size=10.5, color=NAVY, bold=True, anchor="start", vmid=True); f.text(750, y + 17, b, size=10.5, color=TEAL, bold=True, anchor="end", vmid=True)
```

```svgfig label="4.2" caption="Logarithms as graphs and as a ruler. (a) y = log2 x, ln x and log10 x all cross the x-axis at (1, 0), because log of 1 is 0 in every base, and each reaches 1 at x = its own base. (b) A slide rule adds LENGTHS, and length = log10 of the number, so 2 x 3 is read as log 2 + log 3 = 0.3010 + 0.4771 = 0.7782 = log 6."
import math
l2, l3 = math.log10(2), math.log10(3); assert round(l2 + l3, 4) == round(math.log10(6), 4) == 0.7782 and round(l2, 4) == 0.301
assert round(math.log2(64), 9) == 6 and round(math.log10(5), 4) == round(1 - l2, 4) == 0.699
f = Fig(780, 320)
ax = Axes(f, 40, 30, 320, 250, (0, 8), (-3, 3.2))
ax.grid(1, 1, size=10); ax.axes("x", "y")
ax.curve(math.log2, 0.12, 8, color=NAVY, sw=2.4); ax.curve(math.log, 0.05, 8, color=TEAL, sw=2.4); ax.curve(math.log10, 0.02, 8, color=AMBER, sw=2.4)
ax.pt(1, 0, "", r=4, color=RED); ax.pt(2, 1, "", r=3.5, color=NAVY); ax.pt(10 ** 0, 0, "")
f.text(335, 62, "log2 x", size=11, color=NAVY, bold=True, anchor="end"); f.text(335, 98, "ln x", size=11, color=TEAL, bold=True, anchor="end"); f.text(335, 134, "log10 x", size=11, color=AMBER, bold=True, anchor="end")
f.text(580, 26, "(b) Multiplying by adding lengths", size=11.5, color=NAVY, bold=True)
L0, S = 410, 330
for v in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
    x = L0 + math.log10(v) * S
    f.line(x, 78, x, 98, color=SLATE, sw=1.4); f.text(x, 114, str(v), size=10.5, color=SLATE, bold=True)
f.line(L0, 88, L0 + S, 88, color=SLATE, sw=1.4)
x2, x3, x6 = (L0 + math.log10(k) * S for k in (2, 3, 6))
f.box(L0, 150, x2 - L0, 22, "log 2 = 0.301", fill="#bfdbfe", stroke=NAVY, size=10, bold=True, r=2)
f.box(x2, 150, (x6 - x2), 22, "log 3 = 0.477", fill="#fde68a", stroke=AMBER, size=10, bold=True, r=2)
f.line(x6, 130, x6, 190, color=RED, sw=1.6, dash=True)
f.text(x6, 205, "end of the two lengths = log 6 = 0.778", size=10.5, color=RED, bold=True)
f.text(580, 240, "log(ab) = log a + log b", size=11.5, color=NAVY, bold=True)
f.text(580, 264, "log(a/b) = log a - log b    log(a^n) = n log a", size=10.5, color=SLATE)
f.text(580, 288, "log 5 = log(10/2) = 1 - 0.301 = 0.699", size=10.5, color=TEAL, bold=True)
```

## 4.2 Logarithms and their laws

$\log_a x=y\iff a^y=x$ ($a>0$, $a\ne1$, $x>0$). Laws: $\log(mn)=\log m+\log n$; $\log\frac{m}{n}=\log m-\log n$; $\log m^p=p\log m$; $\log_a a=1$; $\log_a1=0$; $\log_ab=\frac{1}{\log_ba}=\frac{\log b}{\log a}$; $a^{\log_ax}=x$. Standard values: $\log_{10}2\approx0.3010$, $\log_{10}3\approx0.4771$, $\log_{10}5=1-\log_{10}2\approx0.6990$. $\log(m+n)$ has **no** expansion.

```photogrid label="4.1" cols="3" ratio="1.0" caption="Logarithms made visible. (a) John Napier of Merchiston (1550-1617), who published the first table of logarithms in 1614. (b) and (c) Two slide rules: before pocket calculators, engineers multiplied by sliding one logarithmic scale along another, exactly as in Fig 4.2(b). Slide rules were still used to design bridges and aircraft in the 1960s."
@ photo id="bcamath/napier" cap="John Napier, inventor of logarithms"
focus 0.5 0.3
@ photo id="bcamath/sliderule" cap="A slide rule: logarithmic scales"
fit 1.0
focus 0.5 0.5
@ photo id="bcamath/sliderule2" cap="Slide rule: add lengths to multiply"
fit 1.0
focus 0.5 0.5
```

## 4.3 Polynomials, remainder and factor theorem

- **Remainder theorem**: $f(x)\div(x-a)$ leaves remainder $f(a)$. **Factor theorem**: $(x-a)$ is a factor iff $f(a)=0$.
- $(a\pm b)^2=a^2\pm2ab+b^2$; $a^3\pm b^3=(a\pm b)(a^2\mp ab+b^2)$; if $a+b+c=0$ then $a^3+b^3+c^3=3abc$.
- If $x+\frac{1}{x}=k$ then $x^2+\frac{1}{x^2}=k^2-2$.

```svgfig label="4.3" caption="The remainder theorem on p(x) = x^3 - 6x^2 + 11x - 6 = (x - 1)(x - 2)(x - 3). Dividing by (x - 4) by synthetic division gives quotient x^2 - 2x + 3 and remainder 6, which equals p(4) = 6 read straight off the curve. p(1) = p(2) = p(3) = 0, so (x - 1), (x - 2) and (x - 3) are factors. The three roots add to 6 and multiply to 6."
p = lambda x: x ** 3 - 6 * x ** 2 + 11 * x - 6
assert [p(1), p(2), p(3)] == [0, 0, 0] and p(4) == 6 and p(0) == -6 and p(-1) == -24
co = [1, -6, 11, -6]; r = 4; row = [co[0]]
for c in co[1:]: row.append(c + row[-1] * r)
assert row == [1, -2, 3, 6]
f = Fig(780, 320)
ax = Axes(f, 40, 20, 340, 270, (-0.5, 4.8), (-8, 10))
ax.grid(1, 2, size=10); ax.axes("x", "y")
ax.curve(p, -0.5, 4.8, color=NAVY, sw=2.5)
for x in (1, 2, 3): ax.pt(x, 0, "", r=4.5, color=RED)
ax.pt(4, 6, "p(4) = 6", r=4.5, color=AMBER, dx=-76, dy=-10, size=10.5)
f.text(520, 28, "Synthetic division by (x - 4)", size=11.5, color=NAVY, bold=True)
xs = [450, 520, 590, 660]
for x, v in zip(xs, co): f.box(x - 28, 50, 56, 30, str(v), fill="#dbeafe", stroke=NAVY, size=12, bold=True, r=3)
f.text(410, 70, "4 |", size=12, color=SLATE, bold=True)
for x, v in zip(xs, [None, 4 * 1, 4 * -2, 4 * 3]):
    if v is not None: f.text(x, 108, "+" + str(v) if v >= 0 else str(v), size=11, color=SLATE, bold=True)
for j, (x, v) in enumerate(zip(xs, row)): f.box(x - 28, 122, 56, 30, str(v), fill=("#fecaca" if j == 3 else "#bbf7d0"), stroke=(RED if j == 3 else TEAL), size=12, bold=True, r=3)
f.text(520, 176, "quotient x^2 - 2x + 3", size=11, color=TEAL, bold=True); f.text(660, 176, "remainder 6", size=11, color=RED, bold=True)
for j, t in enumerate(["Remainder theorem: p(x) divided by (x - a)", "leaves remainder p(a)", "Factor theorem: (x - a) is a factor if p(a) = 0", "roots 1, 2, 3: sum 6 = -b/a, product 6 = -d/a", "p(2) = 8 - 24 + 22 - 6 = 0, so (x - 2) divides p(x)"]):
    f.text(410, 220 + j * 22, t, size=10.5, color=(RED if j == 1 else SLATE), anchor="start", bold=(j == 1))
```

## 4.4 Quadratic equations, nature and sum and product of roots

For $ax^2+bx+c=0$: roots $\frac{-b\pm\sqrt{D}}{2a}$ with $D=b^2-4ac$.

| $D$ | Roots |
|---|---|
| $D>0$, perfect square | real, unequal, rational |
| $D>0$, not a square | real, unequal, irrational |
| $D=0$ | real and equal |
| $D<0$ | imaginary (complex conjugates) |

$\alpha+\beta=-\frac{b}{a}$, $\alpha\beta=\frac{c}{a}$, $\alpha^2+\beta^2=(\alpha+\beta)^2-2\alpha\beta$. The equation with roots $\alpha,\beta$ is $x^2-(\alpha+\beta)x+\alpha\beta=0$. Roots are opposite if $b=0$ and reciprocal if $a=c$. $ax^2+bx+c$ has extreme value $-\frac{D}{4a}$ at $x=-\frac{b}{2a}$.

```svgfig label="4.4" caption="The discriminant D = b^2 - 4ac reads the parabola y = x^2 - 4x + c. (a) c = 3: D = 4 > 0, two real roots, x = 1 and 3. (b) c = 4: D = 0, equal roots, the vertex touches the x-axis at x = 2. (c) c = 5: D = -4 < 0, no real roots, the curve stays above the axis. In every case sum of roots = -b/a = 4 and product = c/a."
import math
def D(c): return 16 - 4 * c
assert (D(3), D(4), D(5)) == (4, 0, -4)
r1 = (4 + math.sqrt(D(3))) / 2; r2 = (4 - math.sqrt(D(3))) / 2; assert (r1, r2) == (3.0, 1.0) and r1 + r2 == 4 and r1 * r2 == 3
f = Fig(780, 320)
for i, (c, t, col, note) in enumerate([(3, "D = 4 > 0", NAVY, "roots 1 and 3"), (4, "D = 0", TEAL, "equal roots, x = 2"), (5, "D = -4 < 0", RED, "no real roots")]):
    cx = 12 + i * 255
    f.box(cx, 8, 245, 304, "", fill=SOFT, stroke="#cbd5e1", r=4)
    ax = Axes(f, cx + 30, 44, 195, 200, (-0.5, 4.5), (-1.5, 5.5))
    ax.grid(1, 1, size=10); ax.axes("", "")
    ax.curve(lambda x, c=c: x * x - 4 * x + c, -0.5, 4.5, color=col, sw=2.5)
    if i == 0: ax.pt(1, 0, "", r=4.5, color=RED); ax.pt(3, 0, "", r=4.5, color=RED)
    if i == 1: ax.pt(2, 0, "", r=4.5, color=RED)
    f.text(cx + 122, 26, "x^2 - 4x + %d,  %s" % (c, t), size=11, color=col, bold=True)
    f.text(cx + 122, 270, note, size=11, color=col, bold=True)
    f.text(cx + 122, 292, "sum 4, product %d" % c if i < 2 else "complex roots 2 +/- i", size=10, color=SLATE)
```

## 4.5 Linear and simultaneous equations, inequalities, equation word problems

- Eliminate one variable; for $x+y=s$, $x-y=d$: $x=\frac{s+d}{2}$, $y=\frac{s-d}{2}$.
- **Consecutive integers**: $n,n+1,\dots$; consecutive even: $n,n+2,\dots$.
- **Inequalities**: multiplying or dividing by a negative reverses the sign. $|x|<a\iff-a<x<a$; $|x|>a\iff x<-a$ or $x>a$.
- **Radical equations**: square both sides, then check every root (extraneous roots appear).

```svgfig label="4.5" caption="Two linear equations are two straight lines. (a) 2x + y = 7 and x - y = 2 meet at one point, (3, 1): the unique solution. (b) 2x + y = 7 and 2x + y = 3 are parallel (same slope, different constant): no solution. (c) 2x + y = 7 and 4x + 2y = 14 are the same line: infinitely many solutions. The test is a1/a2 compared with b1/b2 and c1/c2, and Cramer's rule gives (3, 1) from D = -3."
def solve(a1, b1, c1, a2, b2, c2):
    d = a1 * b2 - a2 * b1
    return None if d == 0 else ((c1 * b2 - c2 * b1) / d, (a1 * c2 - a2 * c1) / d)
assert solve(2, 1, 7, 1, -1, 2) == (3.0, 1.0) and solve(2, 1, 7, 2, 1, 3) is None and solve(2, 1, 7, 4, 2, 14) is None
assert 2 * 1 - 1 * 1 * -1 * -1 * 0 == 2 and (2 * -1 - 1 * 1) == -3
f = Fig(780, 320)
cases = [("unique solution", [(lambda x: 7 - 2 * x, NAVY), (lambda x: x - 2, TEAL)], "2/1 vs 1/-1: slopes differ"), ("no solution", [(lambda x: 7 - 2 * x, NAVY), (lambda x: 3 - 2 * x, TEAL)], "2/2 = 1/1 but 7/3 differs"), ("infinitely many", [(lambda x: 7 - 2 * x, NAVY), (lambda x: 7 - 2 * x, TEAL)], "2/4 = 1/2 = 7/14")]
for i, (t, lines, note) in enumerate(cases):
    cx = 12 + i * 255
    f.box(cx, 8, 245, 304, "", fill=SOFT, stroke="#cbd5e1", r=4)
    ax = Axes(f, cx + 30, 44, 195, 200, (-1, 6), (-3, 8))
    ax.grid(1, 1, size=10); ax.axes("", "")
    for fn, col in lines: ax.curve(fn, -1, 6, color=col, sw=(3.4 if (i == 2 and col == NAVY) else 2.3))
    if i == 0: ax.pt(3, 1, "(3, 1)", r=5, color=RED, dx=8, dy=-10, size=11)
    f.text(cx + 122, 26, t, size=11.5, color=NAVY, bold=True)
    f.text(cx + 122, 268, note, size=10.5, color=SLATE, bold=True)
    f.text(cx + 122, 292, ["x = 3, y = 1", "lines never meet", "every point on the line"][i], size=11, color=RED, bold=True)
```

## 4.6 Eight traps in indices, logarithms, polynomials and equations

Algebra marks are lost to small habits, not to hard ideas. The eight traps below are the ones that appear again and again in the Dean's Office model, and each can be checked with one line of arithmetic.

1. **$a^0=1$, and a negative index means a reciprocal, not a negative number.** So $2^{-2}=\frac14$, not $-4$ and not $-\frac12$ (Fig 4.1). Also $(-2)^2=4$ but $-2^2=-4$, because the power acts before the minus sign. And $(a+b)^n$ is never $a^n+b^n$: $(1+2)^2=9$ but $1^2+2^2=5$.
2. **Fractional powers are roots, and surds do not add inside.** $a^{m/n}$ means take the $n$-th root and then raise to $m$, so $8^{2/3}=2^2=4$ and $27^{-1/3}=\frac13$. The sum $\sqrt{a}+\sqrt{b}$ is not $\sqrt{a+b}$: $\sqrt9+\sqrt{16}=7$ but $\sqrt{25}=5$. To remove a surd from the denominator multiply by the conjugate, as in $\frac{1}{\sqrt3-1}=\frac{\sqrt3+1}{2}$.
3. **The logarithm of a sum is not the sum of logarithms.** The law is $\log(ab)=\log a+\log b$ for a product only, so $\log(2+3)\ne\log2+\log3$ (Fig 4.2). Remember $\log_a1=0$, $\log_aa=1$, and the argument must be positive. A question that says "log" without a base means base 10, while $\ln$ means base $e$.
4. **Know the three working laws and the change of base.** $\log\frac ab=\log a-\log b$, $\log a^n=n\log a$, and $\log_ab=\frac{\log b}{\log a}$, so $\log_ab\times\log_ba=1$. Also $a^{\log_ax}=x$. Typical key results are $\log_264=6$ and $\log5=1-\log2=0.699$, because $5=\frac{10}{2}$.
5. **Use the root of the divisor in the remainder theorem.** The remainder of $p(x)$ divided by $(x-a)$ is $p(a)$, so for $(x+2)$ you substitute $x=-2$, and for $(2x-1)$ you substitute $x=\frac12$ (Fig 4.3). If $p(a)=0$ then $(x-a)$ is a factor. Do not divide by $x$ to "simplify" before you check whether $x=0$ is itself a root.
6. **Read $a$, $b$, $c$ with their signs, then use $-\frac ba$ and $\frac ca$.** For $x^2-5x+6=0$ the sum of roots is $-\frac{-5}{1}=5$ and the product is 6, giving roots 2 and 3. The discriminant $D=b^2-4ac$ decides the nature (Fig 4.4): $D>0$ two real roots, $D=0$ equal roots, $D<0$ none. A quadratic with given roots $\alpha,\beta$ is $x^2-(\alpha+\beta)x+\alpha\beta=0$.
7. **Never cancel a factor that can be zero, and check radical roots.** From $x^2=3x$ the answers are $x=0$ and $x=3$; dividing by $x$ throws away one. Squaring an equation with a square root can create a false root, so substitute back. In inequalities, multiplying or dividing by a negative number reverses the sign, and $|x|<a$ means $-a<x<a$.
8. **Two equations give a point, no point, or a whole line.** Compare $\frac{a_1}{a_2}$, $\frac{b_1}{b_2}$ and $\frac{c_1}{c_2}$: all different slopes gives one solution, equal ratios of $a$ and $b$ but not $c$ gives none, and all three equal gives infinitely many (Fig 4.5). In word problems define each letter in a sentence first, solve, then test the answer against the story, such as ages that must be positive whole numbers.

### 4.6.1 Worked checks

**Q. Given $\log2=0.3010$ and $\log3=0.4771$, find $\log 12$ and $\log 1.5$.**

**Answer.** $\log12=\log(2^2\times3)=2(0.3010)+0.4771=1.0791$. $\log1.5=\log\frac32=\log3-\log2=0.4771-0.3010=0.1761$. Both come from the product, power and quotient laws, never from adding inside the log.

**Q. Find the remainder when $p(x)=x^3-6x^2+11x-6$ is divided by $(x-4)$, and say whether $(x-2)$ is a factor.**

**Answer.** Remainder $=p(4)=64-96+44-6=6$, which synthetic division in Fig 4.3 also gave. For $(x-2)$: $p(2)=8-24+22-6=0$, so yes, $(x-2)$ is a factor. Checking the other roots, $p(1)=0$ and $p(3)=0$ too.

**Q. For $2x^2-7x+3=0$ find the nature of the roots, the roots, and verify the sum and product.**

**Answer.** $D=49-24=25>0$, so the roots are real and unequal. $x=\frac{7\pm5}{4}$ gives $x=3$ and $x=\frac12$. Sum $=\frac72=-\frac{b}{a}$ and product $=\frac32=\frac ca$, which agree.

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
