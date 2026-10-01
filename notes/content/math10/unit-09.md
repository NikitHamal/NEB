---
subject: Mathematics
grade: 10
unit: 9
title: Radical and Surd
hours: 0
area: Compulsory Mathematics
---

The diagonal of a square of side 1 cm is $\sqrt{2}$ cm. No fraction and no terminating or repeating decimal equals $\sqrt{2}$ exactly, so we leave it as a **radical** and calculate with it as a symbol. A **surd** is such an irrational root. This chapter shows how to classify roots, simplify them, add, subtract, multiply and divide them, and — the main skill for the exam — **rationalise a denominator** using a conjugate. These steps lead directly to the surds you meet later in trigonometry, coordinate geometry and quadratic equations.

::: key What the SEE asks from this chapter
Usual questions: (i) **simplify** an expression with surds (3 marks); (ii) **rationalise** the denominator of a fraction such as $\frac{3}{\sqrt{7}-\sqrt{5}}$ and simplify; (iii) if $x=2+\sqrt{3}$, find $x+\frac{1}{x}$, $x^2+\frac{1}{x^2}$ or $x^3+\frac{1}{x^3}$ (4 marks); (iv) find $a$ and $b$ when $\frac{3+\sqrt{2}}{3-\sqrt{2}}=a+b\sqrt{2}$; (v) solve a simple equation containing a square root. Always **check** answers to radical equations in the original equation.
:::

## 9.1 Radical and Surd: concepts, formulas and worked problems

### Radicals and surds

::: definition Radical, index and radicand
An expression $\sqrt[n]{a}$ is called a **radical**. Here $n$ is the **index** (or **order**) of the radical, $a$ is the **radicand**, and $\sqrt{\;}$ is the radical sign. The radical $\sqrt[n]{a}$ means the number whose $n$-th power is $a$, so $\left(\sqrt[n]{a}\right)^n=a$. When $n=2$ it is written $\sqrt{a}$ (square root); $\sqrt[3]{a}$ is the cube root.
:::

::: definition Surd
A **surd** is a radical $\sqrt[n]{a}$ where $a$ is a positive **rational** number and the value of the root is **irrational** (it cannot be written as a fraction).
:::

| Radical | Value | Surd? |
|---|---|---|
| $\sqrt{16}$ | 4 | No — rational |
| $\sqrt{18}$ | $3\sqrt{2}$ | Yes — irrational |
| $\sqrt[3]{27}$ | 3 | No — rational |
| $\sqrt[3]{5}$ | $1.7099\ldots$ | Yes |
| $\sqrt{\frac{4}{9}}$ | $\frac{2}{3}$ | No — rational |
| $\sqrt{\pi}$ | irrational but radicand $\pi$ is not rational | No — not a surd |

Every surd is a radical, but not every radical is a surd.

::: derivation $\sqrt{2}$ is irrational
We assume that $\sqrt{2}$ is rational and reach a contradiction. So $\sqrt{2}$ cannot be rational.

**Setting up.** Suppose $\sqrt{2}=\dfrac pq$, where $p$ and $q$ are whole numbers with **no common factor** (the fraction is in its lowest terms).

**Step 1 — square both sides.**

$$ 2=\frac{p^2}{q^2} \;\Rightarrow\; p^2=2q^2 $$

**Step 2 — $p$ is even.** $p^2$ equals $2q^2$, which is even. A square is even only if the number itself is even, so $p=2k$ for some whole number $k$.

**Step 3 — substitute $p=2k$.**

$$ (2k)^2=2q^2 \;\Rightarrow\; 4k^2=2q^2 \;\Rightarrow\; q^2=2k^2 $$

**Step 4 — $q$ is even too.** By the same reasoning $q$ is even.

**Result.** Both $p$ and $q$ are even, so they share the factor 2. This contradicts "no common factor". Hence $\sqrt{2}$ is **not** rational.

**What it means.** $\sqrt{2}$ is a non-terminating, non-repeating decimal $1.41421356\ldots$. It can be located on the number line, but only by geometry (figure below), not as a fraction.
:::

```figure caption="√2 is the diagonal of a unit square. Swinging the diagonal down to the number line with a compass marks the exact point √2 ≈ 1.414."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(4.6, 2.4))
ax.add_patch(Rectangle((0, 0), 1, 1, fc='#dbeafe', ec=INK, lw=1.2))
ax.plot([0, 1], [0, 1], color=SERIES[1], lw=1.6)
t = np.linspace(0, np.pi/4, 40)
ax.plot(np.sqrt(2)*np.cos(t), np.sqrt(2)*np.sin(t), color=MUTED, lw=1.0, ls='--')
ax.plot([-0.3, 2.3], [0, 0], color=INK, lw=1.0)
for v, lab in [(0, '0'), (1, '1'), (2, '2')]:
    ax.plot([v, v], [-0.05, 0.05], color=INK, lw=1.0)
    ax.text(v, -0.17, lab, ha='center', va='top', fontsize=8.5)
ax.plot([np.sqrt(2)], [0], 'o', color=SERIES[1], ms=5)
ax.text(np.sqrt(2) + 0.04, -0.17, '√2', ha='center', va='top', fontsize=9, color=SERIES[1])
ax.text(0.36, 0.64, '√2', fontsize=9, color=SERIES[1], ha='right', va='center')
ax.text(0.5, 1.07, '1', ha='center', fontsize=8.5); ax.text(1.07, 0.5, '1', ha='left', va='center', fontsize=8.5)
ax.set_xlim(-0.5, 2.5); ax.set_ylim(-0.6, 1.35); ax.set_aspect('equal'); ax.axis('off')
```

### Laws of surds

Let $a,b$ be positive rational numbers and $m,n$ positive integers.

::: key Laws of radicals
$$ \sqrt[n]{a}\times\sqrt[n]{b}=\sqrt[n]{ab} \qquad \frac{\sqrt[n]{a}}{\sqrt[n]{b}}=\sqrt[n]{\frac ab} \qquad \left(\sqrt[n]{a}\right)^n=a $$
$$ \sqrt[n]{a^m}=a^{m/n} \qquad \sqrt[m]{\sqrt[n]{a}}=\sqrt[mn]{a} $$

Note: $\sqrt{a+b}\ne\sqrt{a}+\sqrt{b}$ and $\sqrt{a-b}\ne\sqrt{a}-\sqrt{b}$. For example $\sqrt{9+16}=5$, but $\sqrt{9}+\sqrt{16}=7$.
:::

### Types of surds

| Term | Meaning | Example |
|---|---|---|
| **Pure (entire) surd** | no rational factor outside the radical | $\sqrt{18}$, $\sqrt[3]{24}$ |
| **Mixed surd** | a rational number times a surd | $3\sqrt{2}$, $2\sqrt[3]{3}$ |
| **Simple (monomial) surd** | a single term | $5\sqrt{3}$ |
| **Binomial surd** | two terms, at least one a surd | $2+\sqrt{3}$, $\sqrt{5}-\sqrt{2}$ |
| **Like (similar) surds** | same radicand and same order | $2\sqrt{3}$ and $7\sqrt{3}$ |
| **Unlike surds** | different radicand or order | $\sqrt{2}$ and $\sqrt{3}$ |

::: example Simplifying radicals
**Problem.** Express as a mixed surd in simplest form: (a) $\sqrt{72}$, (b) $\sqrt[3]{54}$.

**Solution.** Take out the largest perfect square (or cube) factor.

(a) $\sqrt{72}=\sqrt{36\times 2}=\sqrt{36}\times\sqrt{2}=6\sqrt{2}$.

(b) $\sqrt[3]{54}=\sqrt[3]{27\times 2}=\sqrt[3]{27}\times\sqrt[3]{2}=3\sqrt[3]{2}$.
:::

::: example Mixed surd to pure surd
**Problem.** Express $3\sqrt{2}$ and $2\sqrt[3]{3}$ as entire (pure) surds.

**Solution.** Put the number inside the radical raised to the index.

$3\sqrt{2}=\sqrt{3^2}\times\sqrt{2}=\sqrt{9\times 2}=\sqrt{18}$.

$2\sqrt[3]{3}=\sqrt[3]{2^3\times 3}=\sqrt[3]{24}$.
:::

### Addition and subtraction

Only **like surds** can be added or subtracted: add or subtract the numbers in front, keep the surd. Unlike surds must first be simplified; if they are still unlike, leave the expression as it is.

::: example Adding and subtracting surds
**Problem.** Simplify (a) $\sqrt{50}+\sqrt{18}-\sqrt{8}$, (b) $3\sqrt{12}-\sqrt{27}$.

**Solution.** (a) $\sqrt{50}=5\sqrt{2}$, $\sqrt{18}=3\sqrt{2}$, $\sqrt{8}=2\sqrt{2}$.

$$ \sqrt{50}+\sqrt{18}-\sqrt{8}=5\sqrt{2}+3\sqrt{2}-2\sqrt{2}=6\sqrt{2} $$

(b) $3\sqrt{12}=3\times 2\sqrt{3}=6\sqrt{3}$ and $\sqrt{27}=3\sqrt{3}$.

$$ 3\sqrt{12}-\sqrt{27}=6\sqrt{3}-3\sqrt{3}=3\sqrt{3} $$
:::

::: caution Common mistakes
- $\sqrt{2}+\sqrt{3}=\sqrt{5}$ is **wrong**. Unlike surds cannot be combined: $\sqrt{2}+\sqrt{3}\approx 3.146$ but $\sqrt{5}\approx 2.236$.
- $\sqrt{a+b}=\sqrt{a}+\sqrt{b}$ is wrong. Square roots do not split over addition.
- Stopping at $\sqrt{72}$ when the answer should be $6\sqrt{2}$. Always simplify to the mixed form.
- Forgetting to simplify before adding: $\sqrt{50}$ and $\sqrt{18}$ look unlike but are both multiples of $\sqrt{2}$.
:::

### Multiplication and division

For like orders, multiply the numbers outside together and the numbers inside together.

::: example Multiplication
**Problem.** Simplify (a) $\sqrt{6}\times\sqrt{15}$, (b) $(2\sqrt{3}+\sqrt{5})(2\sqrt{3}-\sqrt{5})$, (c) $(\sqrt{5}+\sqrt{3})^2$.

**Solution.** (a) $\sqrt{6}\times\sqrt{15}=\sqrt{90}=\sqrt{9\times 10}=3\sqrt{10}$.

(b) Use $(a+b)(a-b)=a^2-b^2$ with $a=2\sqrt{3}$, $b=\sqrt{5}$:

$$ (2\sqrt{3})^2-(\sqrt{5})^2=4\times 3-5=12-5=7 $$

(c) Use $(a+b)^2=a^2+2ab+b^2$:

$$ (\sqrt{5})^2+2\sqrt{5}\sqrt{3}+(\sqrt{3})^2=5+2\sqrt{15}+3=8+2\sqrt{15} $$
:::

::: tip The identity $(a+b)(a-b)=a^2-b^2$
When a binomial surd is multiplied by its conjugate (the same two terms with the sign between them reversed), the surds disappear and the result is rational: $(3+\sqrt{2})(3-\sqrt{2})=9-2=7$.
:::

### Comparing surds of different order

To compare $\sqrt[m]{a}$ and $\sqrt[n]{b}$, first write both with a **common index** (the LCM of $m$ and $n$), then compare the radicands.

```figure caption="Position on the number line: √3 ≈ 1.732 lies to the right of the cube root of 5 ≈ 1.710, although it is a smaller-looking radicand."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8, 2.3))
ax.plot([1.2, 2.5], [0, 0], color=INK, lw=1.2)
for v in [1.25, 1.5, 1.75, 2.0, 2.25, 2.5]:
    ax.plot([v, v], [-0.04, 0.04], color=INK, lw=1.0)
    ax.text(v, -0.1, str(v), ha='center', va='top', fontsize=8)
pts = [(np.sqrt(2), '√2', 0.30, SERIES[0]), (5**(1/3), r'$\sqrt[3]{5}$', 0.80, SERIES[2]), (np.sqrt(3), '√3', 0.30, SERIES[1]), (np.sqrt(5), '√5', 0.30, SERIES[3])]
for v, lab, h, col in pts:
    ax.plot([v], [0], 'o', color=col, ms=5)
    ax.plot([v, v], [0.03, h - 0.03], color=col, lw=0.8)
    ax.text(v, h, lab, ha='center', va='bottom', fontsize=9, color=col)
ax.text(1.2, 0.95, '', fontsize=1)
ax.set_xlim(1.15, 2.55); ax.set_ylim(-0.4, 1.2); ax.axis('off')
```

::: example Which is greater?
**Problem.** Which is greater, $\sqrt{3}$ or $\sqrt[3]{5}$?

**Solution.** The orders are 2 and 3; their LCM is 6.

$$ \sqrt{3}=3^{1/2}=3^{3/6}=\sqrt[6]{3^3}=\sqrt[6]{27} $$
$$ \sqrt[3]{5}=5^{1/3}=5^{2/6}=\sqrt[6]{5^2}=\sqrt[6]{25} $$

Since $27>25$, $\sqrt[6]{27}>\sqrt[6]{25}$. Therefore $\sqrt{3}>\sqrt[3]{5}$.

(Check by decimals: $\sqrt{3}=1.732$ and $\sqrt[3]{5}=1.710$ ✓.)
:::

### Rationalisation

A denominator containing a surd is awkward to work with and to evaluate. **Rationalising** means multiplying the numerator and the denominator by a suitable surd so that the denominator becomes rational.

::: definition Conjugate surds
The **conjugate** of $a+\sqrt{b}$ is $a-\sqrt{b}$ (and the conjugate of $\sqrt{a}+\sqrt{b}$ is $\sqrt{a}-\sqrt{b}$). The product of conjugates is always rational:

$$ (a+\sqrt{b})(a-\sqrt{b})=a^2-b \qquad (\sqrt{a}+\sqrt{b})(\sqrt{a}-\sqrt{b})=a-b $$
:::

::: key How to rationalise
| Denominator | Multiply top and bottom by |
|---|---|
| $\sqrt{a}$ | $\sqrt{a}$ (since $\sqrt{a}\times\sqrt{a}=a$) |
| $a+\sqrt{b}$ | its conjugate $a-\sqrt{b}$ |
| $\sqrt{a}+\sqrt{b}$ | its conjugate $\sqrt{a}-\sqrt{b}$ |
| $\sqrt{a}-\sqrt{b}$ | its conjugate $\sqrt{a}+\sqrt{b}$ |

Multiplying numerator and denominator by the same non-zero number does not change the value of the fraction.
:::

::: example Monomial denominator
**Problem.** Rationalise the denominator: (a) $\dfrac{1}{\sqrt{3}}$, (b) $\dfrac{6}{2\sqrt{3}}$.

**Solution.** (a) $\dfrac{1}{\sqrt{3}}\times\dfrac{\sqrt{3}}{\sqrt{3}}=\dfrac{\sqrt{3}}{3}$.

(b) $\dfrac{6}{2\sqrt{3}}=\dfrac{3}{\sqrt{3}}=\dfrac{3\sqrt{3}}{3}=\sqrt{3}$.
:::

::: example Binomial denominator
**Problem.** Rationalise: (a) $\dfrac{1}{\sqrt{5}-2}$, (b) $\dfrac{3}{\sqrt{7}-\sqrt{5}}$, (c) $\dfrac{5}{3+\sqrt{7}}$.

**Solution.** (a) Multiply by the conjugate $\sqrt{5}+2$:

$$ \frac{1}{\sqrt{5}-2}\times\frac{\sqrt{5}+2}{\sqrt{5}+2}=\frac{\sqrt{5}+2}{5-4}=\sqrt{5}+2 $$

(b) Multiply by $\sqrt{7}+\sqrt{5}$:

$$ \frac{3(\sqrt{7}+\sqrt{5})}{(\sqrt{7})^2-(\sqrt{5})^2}=\frac{3(\sqrt{7}+\sqrt{5})}{7-5}=\frac{3(\sqrt{7}+\sqrt{5})}{2} $$

(c) Multiply by $3-\sqrt{7}$:

$$ \frac{5(3-\sqrt{7})}{9-7}=\frac{5(3-\sqrt{7})}{2} $$
:::

::: example A fraction with two binomials
**Problem.** Simplify $\dfrac{\sqrt{3}+1}{\sqrt{3}-1}$.

**Solution.** Multiply top and bottom by $\sqrt{3}+1$:

$$ \frac{(\sqrt{3}+1)^2}{(\sqrt{3})^2-1^2}=\frac{3+2\sqrt{3}+1}{3-1}=\frac{4+2\sqrt{3}}{2}=2+\sqrt{3} $$
:::

::: example Sum of conjugate reciprocals
**Problem.** Show that $\dfrac{1}{2+\sqrt{3}}+\dfrac{1}{2-\sqrt{3}}=4$.

**Solution.** $\dfrac{1}{2+\sqrt{3}}=\dfrac{2-\sqrt{3}}{4-3}=2-\sqrt{3}$ and $\dfrac{1}{2-\sqrt{3}}=\dfrac{2+\sqrt{3}}{4-3}=2+\sqrt{3}$.

Sum $=(2-\sqrt{3})+(2+\sqrt{3})=4$. ✓
:::

::: example Using decimal values
**Problem.** Given $\sqrt{2}=1.414$ and $\sqrt{3}=1.732$, find the value of $\dfrac{1}{\sqrt{3}-\sqrt{2}}$ to 3 decimal places.

**Solution.** Rationalise first, because dividing by $0.318$ would be awkward:

$$ \frac{1}{\sqrt{3}-\sqrt{2}}=\frac{\sqrt{3}+\sqrt{2}}{3-2}=\sqrt{3}+\sqrt{2}=1.732+1.414=3.146 $$
:::

### Values of expressions: $x+\frac{1}{x}$ and its powers

If $x=a+\sqrt{b}$ then $\dfrac{1}{x}$ is its conjugate divided by a rational number, and often simply the conjugate. This makes the sum $x+\frac{1}{x}$ a **rational** number, which can then be squared and cubed with the identities

::: key Identities for $x$ and $\frac{1}{x}$
$$ x^2+\frac{1}{x^2}=\left(x+\frac{1}{x}\right)^2-2 \qquad x^2+\frac{1}{x^2}=\left(x-\frac{1}{x}\right)^2+2 $$
$$ x^3+\frac{1}{x^3}=\left(x+\frac{1}{x}\right)^3-3\left(x+\frac{1}{x}\right) $$
:::

::: example Value of powers
**Problem.** If $x=2+\sqrt{3}$, find (a) $\dfrac{1}{x}$, (b) $x+\dfrac{1}{x}$, (c) $x^2+\dfrac{1}{x^2}$, (d) $x^3+\dfrac{1}{x^3}$.

**Solution.** (a) $\dfrac{1}{x}=\dfrac{1}{2+\sqrt{3}}=\dfrac{2-\sqrt{3}}{4-3}=2-\sqrt{3}$.

(b) $x+\dfrac{1}{x}=(2+\sqrt{3})+(2-\sqrt{3})=4$.

(c) $x^2+\dfrac{1}{x^2}=\left(x+\dfrac{1}{x}\right)^2-2=4^2-2=14$.

(d) $x^3+\dfrac{1}{x^3}=\left(x+\dfrac{1}{x}\right)^3-3\left(x+\dfrac{1}{x}\right)=4^3-3\times 4=64-12=52$.

Check of (c): $x-\dfrac{1}{x}=2\sqrt{3}$, so $x^2+\dfrac{1}{x^2}=(2\sqrt{3})^2+2=12+2=14$ ✓.
:::

::: example Finding the rational and irrational parts
**Problem.** If $\dfrac{3+\sqrt{2}}{3-\sqrt{2}}=a+b\sqrt{2}$ where $a$ and $b$ are rational, find $a$ and $b$.

**Solution.** Multiply by the conjugate $3+\sqrt{2}$:

$$ \frac{(3+\sqrt{2})^2}{9-2}=\frac{9+6\sqrt{2}+2}{7}=\frac{11+6\sqrt{2}}{7}=\frac{11}{7}+\frac{6}{7}\sqrt{2} $$

Comparing rational and irrational parts: $a=\dfrac{11}{7}$ and $b=\dfrac{6}{7}$.
:::

::: example Difference of two conjugate fractions
**Problem.** Show that $\dfrac{\sqrt{5}+2}{\sqrt{5}-2}-\dfrac{\sqrt{5}-2}{\sqrt{5}+2}=8\sqrt{5}$.

**Solution.** Rationalise each fraction. The denominator in both is $(\sqrt{5})^2-2^2=5-4=1$.

$$ \frac{\sqrt{5}+2}{\sqrt{5}-2}=(\sqrt{5}+2)^2=5+4\sqrt{5}+4=9+4\sqrt{5} $$
$$ \frac{\sqrt{5}-2}{\sqrt{5}+2}=(\sqrt{5}-2)^2=5-4\sqrt{5}+4=9-4\sqrt{5} $$

Subtracting: $(9+4\sqrt{5})-(9-4\sqrt{5})=8\sqrt{5}$. ✓
:::

::: example A square root of a binomial surd
**Problem.** Simplify $\sqrt{3+2\sqrt{2}}$.

**Solution.** Try to write $3+2\sqrt{2}$ as a perfect square $(a+b)^2=a^2+b^2+2ab$. We need $a^2+b^2=3$ and $2ab=2\sqrt{2}$. Take $a=1$ and $b=\sqrt{2}$: then $a^2+b^2=1+2=3$ and $2ab=2\sqrt{2}$ ✓.

$$ 3+2\sqrt{2}=(1+\sqrt{2})^2 \;\Rightarrow\; \sqrt{3+2\sqrt{2}}=1+\sqrt{2} $$
:::

::: example Rectangle with surd sides
**Problem.** A rectangle has length $(3+\sqrt{5})$ cm and breadth $(3-\sqrt{5})$ cm. Find its area and perimeter.

**Solution.** Area $=(3+\sqrt{5})(3-\sqrt{5})=9-5=4\text{ cm}^2$.

Perimeter $=2\left[(3+\sqrt{5})+(3-\sqrt{5})\right]=2\times 6=12$ cm.

Both answers are rational, because the sides are conjugates.
:::

### Equations with square roots

To remove a square root, **square both sides**. This can introduce an extra (false) solution, so every answer must be **checked** in the original equation.

::: example Simple radical equations
**Problem.** Solve (a) $\sqrt{x+5}=7$, (b) $\sqrt{x+7}=x-5$.

**Solution.** (a) Square both sides: $x+5=49$, so $x=44$. Check: $\sqrt{44+5}=\sqrt{49}=7$ ✓.

(b) Square both sides: $x+7=(x-5)^2=x^2-10x+25$.

$$ x^2-11x+18=0 \;\Rightarrow\; (x-2)(x-9)=0 \;\Rightarrow\; x=2\ \text{or}\ x=9 $$

Check $x=9$: LHS $=\sqrt{16}=4$, RHS $=9-5=4$ ✓.

Check $x=2$: LHS $=\sqrt{9}=3$, RHS $=2-5=-3$. These are not equal, so **$x=2$ is rejected**.

The solution is $x=9$.
:::

::: caution Always check
A square root sign means the **positive** root. When you square an equation like $\sqrt{x+7}=x-5$, the false answer $x=2$ makes the right side negative. Substitute every answer back in; reject any that fail.
:::

### Surds in geometry

Surds appear whenever Pythagoras' theorem gives a non-perfect square.

::: example Diagonal and height
**Problem.** (a) Find the diagonal of a square of side 5 cm. (b) Find the height of an equilateral triangle of side 6 cm.

**Solution.** (a) $d=\sqrt{5^2+5^2}=\sqrt{50}=5\sqrt{2}$ cm $\approx 7.07$ cm.

(b) The height splits the base into 3 cm and 3 cm: $h=\sqrt{6^2-3^2}=\sqrt{27}=3\sqrt{3}$ cm $\approx 5.20$ cm.
:::

```figure caption="The square-root spiral: each new right-angled triangle has one leg equal to 1 and the other leg equal to the previous hypotenuse, so the hypotenuses are √2, √3, √4, √5, √6, √7."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.4, 3.4))
pts = [0j, 1+0j]
for k in range(2, 8):
    p = pts[-1]
    pts.append(p + 1j*p/abs(p))
for k in range(1, len(pts)):
    ax.plot([0, pts[k].real], [0, pts[k].imag], color=SERIES[0], lw=0.9)
for k in range(1, len(pts) - 1):
    ax.plot([pts[k].real, pts[k+1].real], [pts[k].imag, pts[k+1].imag], color=INK, lw=1.0)
ax.plot([0, 1], [0, 0], color=INK, lw=1.0)
offs = {1: (0.1, -0.2), 2: (0.12, 0.1), 3: (-0.1, 0.12), 4: (-0.15, 0.06), 5: (-0.15, -0.1), 6: (0.0, -0.22), 7: (0.12, -0.15)}
for k in range(1, len(pts)):
    z = pts[k]
    ax.plot([z.real], [z.imag], 'o', color=ACCENT, ms=3.5)
    dx, dy = offs[k]
    ax.text(z.real + dx*1.0, z.imag + dy*1.0, ('√%d' % k) if k > 1 else '1', fontsize=8, ha='left' if dx >= 0 else 'right', va='center')
ax.set_xlim(-2.8, 2.2); ax.set_ylim(-1.2, 2.4); ax.set_aspect('equal'); ax.axis('off')
```

::: tip Quick surd values to remember
$\sqrt{2}\approx 1.414$, $\sqrt{3}\approx 1.732$, $\sqrt{5}\approx 2.236$, $\sqrt{6}\approx 2.449$, $\sqrt{7}\approx 2.646$. Rationalise before substituting a decimal value — it avoids dividing by a small number.
:::

## 9.2 Exercises of the SEE type

### Method

1. **Simplify** each radical first: take out perfect-square factors.
2. **Add or subtract** only like surds.
3. **Multiply** conjugates with $(a+b)(a-b)=a^2-b^2$; expand squares with $(a\pm b)^2$.
4. **Rationalise** by the conjugate of the denominator; simplify the numerator and cancel common factors.
5. For $x=a+\sqrt{b}$: find $\frac{1}{x}$, then $x+\frac{1}{x}$, then use the identities for squares and cubes.
6. For equations with a root: isolate the root, square, solve, and **check**.

## Chapter summary

- A surd $\sqrt[n]{a}$ ($a$ rational) is irrational; $\sqrt{16}$, $\sqrt[3]{27}$ are not surds; $\sqrt{2}$, $\sqrt[3]{5}$ are.
- $\sqrt{a}\times\sqrt{b}=\sqrt{ab}$; $\frac{\sqrt{a}}{\sqrt{b}}=\sqrt{\frac ab}$; $(\sqrt{a})^2=a$; but $\sqrt{a+b}\ne\sqrt{a}+\sqrt{b}$.
- Add and subtract only like surds after simplifying: $5\sqrt{2}+3\sqrt{2}=8\sqrt{2}$.
- Conjugate of $a+\sqrt{b}$ is $a-\sqrt{b}$; product $=a^2-b$ (rational).
- Rationalise $\frac{1}{\sqrt{a}}$ by $\sqrt{a}$; rationalise $\frac{1}{\sqrt{a}\pm\sqrt{b}}$ by $\sqrt{a}\mp\sqrt{b}$, giving denominator $a-b$.
- If $x=2+\sqrt{3}$ then $\frac{1}{x}=2-\sqrt{3}$, $x+\frac{1}{x}=4$, $x^2+\frac{1}{x^2}=14$, $x^3+\frac{1}{x^3}=52$.
- $x^2+\frac{1}{x^2}=(x+\frac{1}{x})^2-2$ and $x^3+\frac{1}{x^3}=(x+\frac{1}{x})^3-3(x+\frac{1}{x})$.
- Compare surds of different order by writing both with the LCM of the indices.
- Radical equations: square both sides and **check** each answer.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. Which of the following is a surd? <span class="marks">[1]</span>
   (a) $\sqrt{16}$ (b) $\sqrt{18}$ (c) $\sqrt[3]{8}$ (d) $\sqrt{\frac{9}{4}}$
2. The rationalising factor of $\sqrt{5}$ is <span class="marks">[1]</span>
   (a) $\sqrt{5}$ (b) 5 (c) $\sqrt{5}-1$ (d) $\frac{1}{5}$
3. The conjugate of $3+\sqrt{2}$ is <span class="marks">[1]</span>
   (a) $-3-\sqrt{2}$ (b) $3-\sqrt{2}$ (c) $\sqrt{2}-3$ (d) $3+\sqrt{2}$
4. The simplest form of $\sqrt{50}$ is <span class="marks">[1]</span>
   (a) $25\sqrt{2}$ (b) $10\sqrt{5}$ (c) $5\sqrt{2}$ (d) $2\sqrt{5}$
5. The value of $(\sqrt{3}+\sqrt{2})(\sqrt{3}-\sqrt{2})$ is <span class="marks">[1]</span>
   (a) 5 (b) 1 (c) $\sqrt{6}$ (d) $1+2\sqrt{6}$

::: note Answers to Group A
**1.** (b) — $\sqrt{18}=3\sqrt{2}$ is irrational; the others equal $4$, $2$, $\frac{3}{2}$.
**2.** (a) — $\sqrt{5}\times\sqrt{5}=5$.
**3.** (b) — change the sign between the terms.
**4.** (c) — $\sqrt{25\times 2}=5\sqrt{2}$.
**5.** (b) — $3-2=1$.
:::

**Group B — Short answer (2 marks each)**

1. Simplify $\sqrt{72}$. <span class="marks">[2]</span>
2. Simplify $\sqrt{12}+\sqrt{27}$. <span class="marks">[2]</span>
3. Rationalise the denominator of $\dfrac{6}{\sqrt{3}}$. <span class="marks">[2]</span>
4. Express $3\sqrt{2}$ as an entire surd. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** $\sqrt{36\times 2}=6\sqrt{2}$.
**2.** $2\sqrt{3}+3\sqrt{3}=5\sqrt{3}$.
**3.** $\frac{6}{\sqrt{3}}\times\frac{\sqrt{3}}{\sqrt{3}}=\frac{6\sqrt{3}}{3}=2\sqrt{3}$.
**4.** $3\sqrt{2}=\sqrt{9\times 2}=\sqrt{18}$.
:::

**Group C — Short answer (3 marks each)**

1. Rationalise the denominator of $\dfrac{3}{\sqrt{7}-\sqrt{5}}$. <span class="marks">[3]</span>
2. Simplify $(\sqrt{5}+\sqrt{3})^2$ and $(\sqrt{5}+\sqrt{3})(\sqrt{5}-\sqrt{3})$. <span class="marks">[3]</span>
3. If $x=2+\sqrt{3}$, find $x+\dfrac{1}{x}$. <span class="marks">[3]</span>
4. Simplify $\sqrt{50}+\sqrt{18}-\sqrt{8}$. <span class="marks">[3]</span>

::: note Answers to Group C
**1.** $\frac{3(\sqrt{7}+\sqrt{5})}{7-5}=\frac{3(\sqrt{7}+\sqrt{5})}{2}$.
**2.** $(\sqrt{5}+\sqrt{3})^2=5+2\sqrt{15}+3=8+2\sqrt{15}$. $(\sqrt{5}+\sqrt{3})(\sqrt{5}-\sqrt{3})=5-3=2$.
**3.** $\frac{1}{x}=\frac{1}{2+\sqrt{3}}=\frac{2-\sqrt{3}}{4-3}=2-\sqrt{3}$. $x+\frac{1}{x}=(2+\sqrt{3})+(2-\sqrt{3})=4$.
**4.** $5\sqrt{2}+3\sqrt{2}-2\sqrt{2}=6\sqrt{2}$.
:::

**Group D — Long answer (4 marks each)**

1. If $x=3+2\sqrt{2}$, find $x+\dfrac{1}{x}$, $x^2+\dfrac{1}{x^2}$ and $x^3+\dfrac{1}{x^3}$. <span class="marks">[4]</span>
2. Simplify $\dfrac{\sqrt{3}+1}{\sqrt{3}-1}+\dfrac{\sqrt{3}-1}{\sqrt{3}+1}$. <span class="marks">[4]</span>
3. If $\dfrac{3+\sqrt{2}}{3-\sqrt{2}}=a+b\sqrt{2}$, find the rational numbers $a$ and $b$. <span class="marks">[4]</span>
4. Solve $\sqrt{x+7}=x-5$. <span class="marks">[4]</span>

::: note Answers to Group D
**1.** $\frac{1}{x}=\frac{1}{3+2\sqrt{2}}=\frac{3-2\sqrt{2}}{9-8}=3-2\sqrt{2}$. $x+\frac{1}{x}=6$. $x^2+\frac{1}{x^2}=6^2-2=34$. $x^3+\frac{1}{x^3}=6^3-3\times 6=216-18=198$.
**2.** $\frac{(\sqrt{3}+1)^2+(\sqrt{3}-1)^2}{(\sqrt{3})^2-1}=\frac{(4+2\sqrt{3})+(4-2\sqrt{3})}{2}=\frac{8}{2}=4$.
**3.** $\frac{(3+\sqrt{2})^2}{9-2}=\frac{11+6\sqrt{2}}{7}$, so $a=\frac{11}{7}$ and $b=\frac{6}{7}$.
**4.** Square both sides: $x+7=x^2-10x+25$, so $x^2-11x+18=0$ and $x=2$ or $9$. Check $x=9$: $\sqrt{16}=4=9-5$ ✓. Check $x=2$: $\sqrt{9}=3\ne 2-5=-3$ ✗. So $x=9$.
:::
