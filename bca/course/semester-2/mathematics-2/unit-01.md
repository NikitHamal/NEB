---
subject: Mathematics II
grade: BCA Semester 2
unit: 1
title: Limits and Continuity
area: BCA 154 · Mathematics II · Unit 1
---

A **limit** describes what a function approaches near a point, even if it never reaches it. Limits are the foundation of both the derivative (a limit of slopes) and the integral (a limit of sums), and continuity is the property that makes functions well-behaved enough for calculus.

::: key What this unit gives you
- The meaning of $\lim f (x)$ as $x \to a$, one-sided limits, and limits at infinity.
- The limit laws and every standard technique: factoring, rationalising, standard limits, squeeze.
- Continuity, the three types of discontinuity, and the Intermediate Value Theorem.
:::

## 1.1 The idea of a limit

We write **$\lim_{x \to a} f (x) = L$** if $f (x)$ can be made as close to L as we like by taking *x* close enough to a (but $x \neq a$). The value $f (a)$ itself is irrelevant to the limit.

Take $f (x) = \frac{x^{2} - 1}{x - 1}$. It is undefined at 1, but for $x \neq 1$ it equals $x + 1$. As $x \to 1$ the values approach 2, so the limit is 2: $f (0.9) = 1.9 ,\  f (0.99) = 1.99 ,\  f (1.01) = 2.01$.

**One-sided limits.** $\lim_{x \to a^{+}}$ approaches from the right, $\lim_{x \to a^{-}}$ from the left. **The limit exists iff both one-sided limits exist and are equal.**

::: example Worked example: a limit that does not exist
$f (x) = \frac{|x|}{x}$. For $x > 0 ,\  f = 1$; for $x < 0 ,\  f = - 1$. The right limit at 0 is 1, the left limit is −1, so **$\lim_{x \to 0} \frac{|x|}{x}$ does not exist**.
:::

**Limit laws.** If the limits of *f* and *g* exist: the limit of a sum, difference, product and constant multiple is the sum, difference, product and multiple of the limits; the limit of a quotient is the quotient of limits if the denominator's limit ≠ $0 ;\  \lim [f (x)]^{n} = [\lim f (x)]^{n}$. For polynomials and most standard functions, **direct substitution** works: $\lim_{x \to a} P (x) = P (a)$.

```svgfig label="1.1" caption="Three things a limit can do as $x \to a$. (a) The limit exists even though $f (a)$ is undefined: a removable hole. (b) The left and right limits differ, so the limit does not exist: a jump. (c) The values grow without bound: an infinite limit with a vertical asymptote."
f = Fig(780, 250)
specs = [("(a) f(x) = (x² − 1)/(x − 1), x → 1", lambda x: x + 1, (-1, 3), (-1, 4.5)), ("(b) f(x) = |x| / x, x → 0", lambda x: x / abs(x), (-3, 3), (-2, 2)), ("(c) f(x) = 1/x², x → 0", lambda x: 1 / (x * x), (-3, 3), (-1, 8))]
for i, (t, fn, xr, yr) in enumerate(specs):
    cx = 8 + i * 258
    f.box(cx, 6, 246, 238, "", fill=SOFT, stroke="#cbd5e1")
    f.text(cx + 123, 24, t, size=10.5, color=NAVY, bold=True)
    a = Axes(f, cx + 16, 36, 214, 160, xr, yr); a.axes("", "")
    a.curve(fn, color=NAVY, sw=2.4)
    if i == 0:
        a.pt(1, 2, "", hollow=True, color=RED); a.hline(2, -1, 1, color=AMBER); a.vline(1, -1, 2, color=AMBER)
        f.text(cx + 123, 214, "limit = 2, but f(1) is undefined", size=10, color=TEAL, bold=True)
    if i == 1:
        a.pt(0, 1, "", hollow=True, color=RED); a.pt(0, -1, "", hollow=True, color=RED)
        f.text(cx + 123, 214, "left limit −1 ≠ right limit 1", size=10, color=TEAL, bold=True)
    if i == 2:
        a.vline(0, color=RED, dash=False)
        f.text(cx + 123, 214, "f(x) → ∞ from both sides", size=10, color=TEAL, bold=True)
    f.text(cx + 123, 232, ["removable hole", "jump: limit DNE", "infinite limit"][i], size=9.5, color=SLATE)
```

```photogrid label="1.1" cols="3" ratio="1.0" caption="The precise definition of a limit. (a) Augustin-Louis Cauchy (1789-1857) first demanded that calculus be built on limits. (b) Karl Weierstrass (1815-1897) wrote the $\epsilon - \delta$ definition in the form used today. (c) $\lim f (x) = L$ means: for any band of half-width *ε* around L we can find a window of half-width *δ* around a that keeps *f* inside the band."
@ photo id="bca104/cauchy" cap="A.-L. Cauchy, French mathematician"
fit 1.0
focus 0.5 0.72
@ photo id="bca104/weier" cap="K. Weierstrass, German mathematician"
fit 1.0
focus 0.5 0.75
@ svg cap="ε-δ for f(x) = x² near a = 1 (ε = 0.5)"
f = Fig(250, 250)
a = Axes(f, 30, 14, 200, 205, (0, 2), (0, 2.4)); a.grid(1, 1).axes()
f.raw(f'<rect x="{a.X(0)}" y="{a.Y(1.5)}" width="{a.w}" height="{round(a.Y(0.5) - a.Y(1.5), 2)}" fill="#fde68a" fill-opacity="0.55"/>')
f.raw(f'<rect x="{a.X(0.7071)}" y="{a.Y(1.4)}" width="{round(a.X(1.2247) - a.X(0.7071), 2)}" height="{a.h}" fill="#99f6e4" fill-opacity="0.5"/>')
a.curve(lambda x: x * x, color=NAVY, sw=2.4)
a.pt(1, 1, "", r=3.5)
f.text(a.X(1.55), a.Y(1.5) - 4, "L + ε", size=10, color=AMBER, bold=True); f.text(a.X(1.55), a.Y(0.5) + 12, "L − ε", size=10, color=AMBER, bold=True)
f.text(a.X(0.98), a.Y(0) + 26, "a − δ  …  a + δ", size=10, color=TEAL, bold=True)
f.text(125, 244, "L = 1 at a = 1", size=10, color=SLATE)
```

## 1.2 Techniques for finding limits

When substitution gives **$\frac{0}{0}$** (an indeterminate form), rewrite the expression.

**(1) Factor and cancel.**

::: example Worked example
$\lim_{x \to 3} \frac{x^{2} - 9}{x - 3} = \lim (x + 3)$ = **6**.

$\lim_{x \to 2} \frac{x^{3} - 8}{x^{2} - 4} = \lim \frac{(x - 2) (x^{2} + 2 x + 4)}{(x - 2) (x + 2)} = \frac{4 + 4 + 4}{4}$ = **3**.
:::

**(2) Rationalise** (multiply by the conjugate).

::: example Worked example
$\lim_{x \to 0} \frac{\sqrt{x + 4} - 2}{x}$. Multiply top and bottom by $\left( \sqrt{x + 4} + 2 \right)$: numerator becomes $(x + 4) - 4 = x$, so the expression is $\frac{x}{x \left( \sqrt{x + 4} + 2 \right)} = \frac{1}{\sqrt{x + 4} + 2} \to \frac{1}{4}$. Answer **$\frac{1}{4}$**.
:::

**(3) Standard limits** (*x* in radians):

| Limit | Value |
|---|---|
| $\lim_{x \to 0} \frac{\sin x}{x}$ | 1 |
| $\lim_{x \to 0} \frac{1 - \cos x}{x^{2}}$ | $\frac{1}{2}$ |
| $\lim_{x \to 0} \frac{\tan x}{x}$ | 1 |
| $\lim_{x \to 0} \frac{e^{x} - 1}{x}$ | 1 |
| $\lim_{x \to 0} \frac{\ln (1 + x)}{x}$ | 1 |
| $\lim_{x \to 0} \frac{a^{x} - 1}{x}$ | $\ln a$ |
| $\lim_{x \to 0} (1 + x)^{\frac{1}{x}} = \lim_{x \to \infty} \left( 1 + \frac{1}{x} \right)^{x}$ | *e* |
| $\lim_{x \to a} \frac{(x^{n} - a^{n})}{x - a}$ | $n a^{n-1}$ |

::: example Worked example: using the standard limits
**(a)** $\lim_{x \to 0} \frac{\sin 5 x}{3 x} = \left( \frac{5}{3} \right) \cdot \lim \frac{\sin 5 x}{5 x}$ = **$\frac{5}{3}$**.

**(b)** $\lim_{x \to 0} \frac{e^{3 x} - 1}{x} = 3 \cdot \lim \frac{e^{3 x} - 1}{3 x}$ = **3**.

**(c)** $\lim_{x \to \infty} \left( 1 + \frac{2}{x} \right)^{x}$: put $t = \frac{x}{2}$, then $\left( 1 + \frac{1}{t} \right)^{2 t} \to e^{2}$. Answer **$e^{2}$**.

**(d)** $\lim_{x \to 0} \frac{1 - \cos x}{x^{2}} = \lim \frac{2 \sin^{2} \left( \frac{x}{2} \right)}{x^{2}} = 2 \cdot \left( \frac{1}{2} \right)^{2} \cdot \lim \left( \frac{\sin \left( \frac{x}{2} \right)}{\frac{x}{2}} \right)^{2}$ = **$\frac{1}{2}$**.

**(e)** $\lim_{x \to 0} \frac{\tan 2 x - \sin 2 x}{x^{3}}$: $\tan 2 x - \sin 2 x = \tan 2 x (1 - \cos 2 x)$, so the quotient is $\left[ \frac{\tan 2 x}{x} \right] \cdot \left[ \frac{1 - \cos 2 x}{x^{2}} \right] \to 2 \cdot \left( 4 \cdot \frac{1}{2} \right)$ = **4**.
:::

**(4) Squeeze theorem.** If $g (x) \leq f (x) \leq h (x)$ near a and *g* and *h* both → L, then $f \to L$. Example: |x $\sin \left( \frac{1}{x} \right) \mid \leq |x| \to 0$, so $\lim_{x \to 0} x \sin \left( \frac{1}{x} \right) = 0$.

```svgfig label="1.2" caption="The squeeze theorem at work. Near 0 the curve $\frac{\sin x}{x}$ (navy) is trapped between $\cos x$ (teal) below and the line $y = 1$ (amber) above. Both bounds tend to 1, so $\frac{\sin x}{x} \to 1$. The hole at $x = 0$ is hollow because the function is not defined there."
import math
f = Fig(560, 260)
a = Axes(f, 40, 14, 490, 210, (-3.4, 3.4), (-0.5, 1.3)); a.grid(1, 0.5).axes()
a.curve(lambda x: 1, color=AMBER, sw=2); a.curve(math.cos, color=TEAL, sw=2)
a.curve(lambda x: math.sin(x) / x, color=NAVY, sw=2.6)
a.pt(0, 1, "", hollow=True, color=RED)
f.text(a.X(1.0), a.Y(1) - 7, "y = 1", size=11, color=AMBER, bold=True, anchor="start")
f.text(a.X(1.5), a.Y(0.07) + 18, "y = cos x", size=11, color=TEAL, bold=True, anchor="start")
f.text(a.X(0.45), a.Y(0.84) + 4, "sin x / x", size=11, color=NAVY, bold=True, anchor="start")
```

## 1.3 Limits at infinity and infinite limits

For rational functions divide numerator and denominator by the highest power of *x* in the denominator.

::: example Worked example
$\lim_{x \to \infty} \frac{3 x^{2} + 2 x}{5 x^{2} - 1} = \lim \frac{3 + \frac{2}{x}}{5 - \frac{1}{x^{2}}}$ = **$\frac{3}{5}$**.

$\lim_{x \to \infty} \frac{2 x + 1}{x^{2} + 3} = 0$ (degree of top < degree of bottom).

$\lim_{x \to \infty} \frac{x^{3} + 1}{x^{2} + 1} = \infty$ (degree of top > bottom).
:::

For differences of square roots, rationalise:

::: example Worked example
$\lim_{x \to \infty} \left( \sqrt{x^{2} + x} - x \right) = \lim \frac{x}{\sqrt{x^{2} + x} + x} = \lim \frac{1}{\sqrt{1 + \frac{1}{x}} + 1}$ = **$\frac{1}{2}$**.
:::

The line $y = L$ is a **horizontal asymptote** if $f (x) \to L$ as $x \to \pm \infty ;\  x = a$ is a **vertical asymptote** if $f (x) \to \pm \infty$ as $x \to a$ from one side. For $f (x) = \frac{1}{x - 2}$: vertical asymptote $x = 2$, horizontal asymptote $y = 0$. The five other indeterminate forms are $\frac{\infty}{\infty} ,\  \infty - \infty ,\  0 \cdot \infty ,\  1^{\infty}$ and $0^{0}$ (Unit 3 handles them with L'Hôpital's rule).

## 1.4 Continuity

*f* is **continuous at a** if three things hold: (1) $f (a)$ is defined, $(2) \lim_{x \to a} f (x)$ exists, (3) the limit equals $f (a)$. Polynomials, $\sin ,\  \cos ,\  e^{x}$ are continuous everywhere; rational functions and tan, ln, √ are continuous on their domains. Sums, products, quotients (denominator ≠ 0) and compositions of continuous functions are continuous.

**Types of discontinuity**

| Type | Description | Example at $x = 0$ or 1 |
|---|---|---|
| Removable | limit exists but ≠ $f (a)$ or $f (a)$ undefined | $\frac{x^{2} - 1}{x - 1}$ at 1 |
| Jump | left and right limits exist but differ | $\lfloor x \rfloor$ at integers; $\frac{|x|}{x}$ at 0 |
| Infinite | function blows up | $\frac{1}{x}$ at 0 |

::: example Worked example: choose k to make f continuous
$f (x) = \frac{x^{2} - 1}{x - 1}$ for $x \neq 1$ and $f (1) = k$. The limit at 1 is 2, so *f* is continuous only if **$k = 2$**.
:::

::: example Worked example: piecewise continuity
$f (x) = a x + 1$ for $x \leq 2 ;\  f (x) = x^{2} - a$ for $x > 2$. Left limit at $2 = 2 a + 1$; right limit = $4 - a$. Continuity needs $2 a + 1 = 4 - a$, so $3 a = 3$, **$a = 1$**.
:::

**Intermediate Value Theorem (IVT).** If *f* is continuous on $[a ,\  b]$ and N lies between $f (a)$ and $f (b)$, then $f (c) = N$ for some *c* in $(a ,\  b)$. It proves a root exists: $f (x) = x^{3} + x - 1$ has $f (0) = - 1 < 0$ and $f (1) = 1 > 0$, so there is a root in (0, 1). Halving the interval repeatedly (the **bisection method**, studied in Numerical Methods) finds it: $f (0.5) = - 0.375 < 0$, so the root is in $(0.5 ,\  1) ;\  f (0.75) = 0.172 > 0$, so it is in (0.5, 0.75).

```svgfig label="1.3" caption="The Intermediate Value Theorem for $f (x) = x^{3} + x - 1$. Since $f (0) = - 1 < 0$ and $f (1) = 1 > 0$ and *f* is continuous, its graph must cross the x-axis between 0 and 1. The root is $c \approx 0.6823$ (found by bisection)."
f = Fig(560, 270)
a = Axes(f, 40, 14, 490, 220, (-1, 2), (-3, 3.2)); a.grid(0.5, 1).axes()
a.curve(lambda x: x**3 + x - 1, color=NAVY, sw=2.6)
a.pt(0, -1, "f(0) = −1", color=RED, dx=8, dy=16); a.pt(1, 1, "f(1) = 1", color=RED, dx=8, dy=-8)
a.vline(0, -3, -1, color=SLATE); a.vline(1, 0, 1, color=SLATE)
a.pt(0.6823, 0, "c ≈ 0.682", color=TEAL, dx=-8, dy=-12, anchor="end", r=5)
```

## 1.5 Eight uses of limits in computing and daily life

1. **Instantaneous speed.** A speedometer shows the speed at one instant, which is the limit of (distance travelled) / (time taken) as the time interval shrinks to zero. Without limits that phrase would mean $\frac{0}{0}$. A bus driver on the Prithvi Highway reads this limit from the dial every second.
2. **Accuracy of numerical software.** Calculators compute $\sin x ,\  e^{x}$ and $\sqrt{x}$ by repeating a step until the answer stops changing, which is a limit of a sequence. The limit $\lim_{x \to 0} \frac{\sin x}{x} = 1$ is the reason small angles can use $\sin x \approx x$. Every scientific calculator relies on this idea.
3. **Compound interest and the number *e*.** If a bank adds interest *n* times a year, the amount for Rs 1 at 100% is $\left( 1 + \frac{1}{n} \right)^{n}$. As $n \to \infty$ this tends to $e \approx 2.71828$. This limit explains continuous compounding and is used in finance formulas.
4. **Running time of algorithms.** To compare $3 n^{2} + 2 n$ with $n^{2}$ we look at the limit of their ratio as $n \to \infty$, which is 3. A finite non-zero limit tells us both grow at the same rate, so both are $O (n^{2})$. Big-O notation is a limit idea.
5. **Convergence of iterative methods.** Newton's method, gradient descent in machine learning and PageRank all repeat a step and hope that the values settle to a limit. If the limit exists the method has converged. Engineers decide when to stop by checking how close successive values are.
6. **Continuity in digital design.** A real signal such as a voice on a phone call is continuous, and sampling it (Digital Logic, Unit 1) relies on the signal having no sudden jumps between samples. Where a function jumps, a limit does not exist and sampling fails. Continuity is the mathematical guarantee that small changes in input give small changes in output.
7. **Asymptotes and long-term behaviour.** The limit at infinity tells where a quantity settles. A cooling cup of tea approaches room temperature, and the speed of a falling parachutist approaches a terminal speed. In Nepal, the population of a town in a model may level off at the carrying capacity of its land.
8. **Foundation of derivative and integral.** Both the derivative and the definite integral are defined as limits, so every rate-of-change and area calculation in the rest of this book rests on this unit. Even the formula for the area of a circle is the limit of polygon areas. Learning limits well makes Units 2 to 6 much easier.

## Formula and fact sheet

- $\lim \frac{\sin x}{x} = 1 ,\  \lim \frac{1 - \cos x}{x^{2}} = \frac{1}{2} ,\  \lim \frac{e^{x} - 1}{x} = 1 ,\  \lim \frac{\ln (1 + x)}{x} = 1 ,\  \lim \left( 1 + \frac{1}{x} \right)^{x} = e ,\  \lim \frac{a^{x} - 1}{x} = \ln a$.
- $\lim \frac{(x^{n} - a^{n})}{x - a} = n a^{n-1}$.
- Rational at $\infty$: compare degrees (equal → ratio of leading coefficients; top smaller → 0).
- Continuity at a: $f (a)$ defined, limit exists, limit = $f (a)$.
- Limit exists ⇔ left limit = right limit.
- IVT: continuous on $[a ,\  b]$ takes every value between $f (a)$ and $f (b)$.

## Chapter summary

- A limit describes the approached value and ignores the value at the point; both one-sided limits must agree.
- For $\frac{0}{0}$, factor, rationalise or use a standard limit; for $x \to \infty$ divide by the highest power.
- Continuity means the graph can be drawn without lifting the pen; the three kinds of break are removable, jump and infinite.
- The IVT guarantees roots of continuous functions between sign changes.

## Practice

1. Evaluate (a) $\lim_{x \to 2} \frac{x^{2} - 5 x + 6}{x - 2}$, (b) $\lim_{x \to 0} \frac{\sqrt{1 + x} - 1}{x}$, (c) $\lim_{x \to 1} \frac{x^{4} - 1}{x - 1}$.
2. Evaluate (a) $\lim_{x \to 0} \frac{\sin 7 x}{\sin 3 x}$, (b) $\lim_{x \to 0} \frac{1 - \cos 4 x}{x^{2}}$, (c) $\lim_{x \to 0} \frac{e^{2 x} - 1}{\sin 3 x}$.
3. Evaluate (a) $\lim_{x \to \infty} \frac{4 x^{3} - x}{2 x^{3} + 5}$, (b) $\lim_{x \to \infty} \left( 1 + \frac{3}{x} \right)^{x}$, (c) $\lim_{x \to \infty} \left( \sqrt{x^{2} + 3 x} - x \right)$.
4. Does $\lim_{x \to 0} \frac{|x|}{x}$ exist? What about $\lim_{x \to 2}$ |x − $2 \mid / (x - 2)$?
5. Find a so that $f (x) = \frac{\sin 3 x}{x} (x \neq 0) ,\  f (0) = a$ is continuous at 0.
6. Find *k* if $f (x) = k x + 2 (x < 1) ,\  f (x) = 3 x^{2} - k (x \geq 1)$ is continuous.
7. Classify the discontinuities of $f (x) = \frac{x^{2} - 4}{x^{2} - 3 x + 2}$.
8. Show that $x^{5} - 3 x + 1 = 0$ has a root in (0, 1).
9. Using the squeeze theorem find $\lim_{x \to \infty} \frac{\sin x}{x}$.
10. Find the asymptotes of $f (x) = \frac{2 x^{2} + 1}{x^{2} - 1}$.

::: note Answers and worked solutions
**1.** (a) $\frac{(x - 2) (x - 3)}{x - 2}$ → **−1**. (b) rationalise: $\frac{x}{x \left( \sqrt{1 + x} + 1 \right)}$ → **$\frac{1}{2}$**. (c) $n a^{n-1}$ with $n = 4 ,\  a = 1$: **4**.

**2.** (a) $\left( \frac{\sin 7 x}{7 x} \right) \left( \frac{3 x}{\sin 3 x} \right) \left( \frac{7}{3} \right)$ → **$\frac{7}{3}$**. (b) $1 - \cos 4 x = 2 \sin^{2} 2 x$, so 2·4 = **8** (2 $\frac{\sin^{2} 2 x}{x^{2}}$ = 2·(sin 2x / x)² → 2·4). (c) $\frac{e^{2 x} - 1}{x} \to 2$ and $\frac{\sin 3 x}{x} \to 3$, so **$\frac{2}{3}$**.

**3.** (a) **2**. (b) **$e^{3}$**. (c) multiply by conjugate: $\frac{3 x}{\sqrt{x^{2} + 3 x} + x}$ → **$\frac{3}{2}$**.

**4.** The first does not exist (left −1, right +1). The second does not exist for the same reason (left −1, right +1).

**5.** The limit is 3, so **$a = 3$**.

**6.** Left limit at 1: $k + 2$; right: $3 - k$. $k + 2 = 3 - k$ ⇒ **$k = \frac{1}{2}$**.

**7.** $f = \frac{(x - 2) (x + 2)}{(x - 1) (x - 2)}$. At $x = 2$: limit $\frac{4}{1} = 4$ exists, so a **removable** discontinuity. At $x = 1$: denominator → 0, numerator → −3, so an **infinite** discontinuity (vertical asymptote $x = 1$).

**8.** $f (0) = 1 > 0 ,\  f (1) = - 1 < 0 ,\  f$ is continuous, so by the IVT there is a root in (0, 1).

**9.** $- \frac{1}{x} \leq \frac{\sin x}{x} \leq \frac{1}{x}$ and both bounds → 0, so the limit is **0**.

**10.** Vertical: $x = 1$ and $x = - 1$. Horizontal: limit as $x \to \pm \infty$ is 2, so **$y = 2$**.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q (5 marks). Evaluate $\lim_{x \to 0} \frac{\sin 3 x}{\sin 5 x}$. State the standard limit used and show the working.**

Direct substitution gives $\frac{0}{0}$, which is an indeterminate form, so the expression must be rewritten. The standard limit that fits is **$\lim_{u \to 0} \frac{\sin u}{u} = 1$** (*u* in radians). The idea is to make each sine look like $\frac{\sin u}{u}$ by supplying the missing factor in the denominator.

1. Write $\frac{\sin 3 x}{\sin 5 x} = \left[ \frac{\sin 3 x}{3 x} \right] \times \left[ \frac{5 x}{\sin 5 x} \right] \times \left( \frac{3 x}{5 x} \right)$.
2. The factor $\frac{3 x}{5 x} = \frac{3}{5}$ for every $x \neq 0$, so it is constant and equals $\frac{3}{5}$.
3. As $x \to 0$ we also have $3 x \to 0$, so $\frac{\sin 3 x}{3 x} \to 1$ by the standard limit.
4. Similarly $5 x \to 0$, so $\frac{\sin 5 x}{5 x} \to 1$, and its reciprocal $\frac{5 x}{\sin 5 x} \to 1$.
5. By the product law the limit of the product is the product of the limits: $1 \times 1 \times \frac{3}{5}$.

**Answer: $\frac{3}{5}$.** *Check by numbers:* at $x = 0.01 ,\  \frac{\sin 0.03}{\sin 0.05} = 0.0299955 / 0.0499792 \approx 0.6001$, which is close to 0.6. *General rule:* $\lim_{x \to 0} \frac{\sin a x}{\sin b x} = \frac{a}{b}$.

**Q (5 marks). Find *k* so that $f (x) = \frac{x^{2} - 4}{x - 2}$ for $x \neq 2$ and $f (2) = k$ is continuous at $x = 2$. Then show that $x^{3} + x - 1 = 0$ has a root between 0 and 1.**

A function is **continuous at a** if three things hold: $f (a)$ is defined, $\lim_{x \to a} f (x)$ exists, and the two are equal.

*Part $1 . \ast$ For $x \neq 2 ,\  \frac{x^{2} - 4}{x - 2} = \frac{(x - 2) (x + 2)}{x - 2} = x + 2$. So $\lim_{x \to 2} f (x) = 2 + 2 = 4$. For continuity $f (2)$ must equal this limit, so **$k = 4$**. With any other value the graph has a hole or a jump at $x = 2 ( a$ removable discontinuity, Figure 1.1a).

*Part $2 . \ast$ Let $g (x) = x^{3} + x - 1$. A polynomial is continuous everywhere, so *g* is continuous on [0, 1]. Now $g (0) = - 1 < 0$ and $g (1) = 1 + 1 - 1 = 1 > 0$, so the value 0 lies between $g (0)$ and $g (1)$. By the **Intermediate Value Theorem** there is at least one *c* in (0, 1) with $g (c) = 0$ (Figure 1.3). Testing the midpoint, $g (0.5) = 0.125 + 0.5 - 1 = - 0.375 < 0$, so the root is in (0.5, 1); repeating gives $c \approx 0.6823$.

**Q (10 marks). Define the limit of a function and explain one-sided limits, the limit laws, the techniques for evaluating limits, limits at infinity and continuity, with examples.**

**Introduction.** The limit is the central idea of calculus: $\lim_{x \to a} f (x) = L$ means that $f (x)$ can be made as close to L as we please by taking *x* sufficiently close to a, but not equal to a. Formally, for every $\epsilon > 0$ there is a $\delta > 0$ such that 0 < |x − a| < *δ* implies $\mid f (x)$ − L| < *ε* (Figure 1.1, Plate 1.1c). The value $f (a)$ does not matter.

**One-sided limits.** The right limit $(x \to a^{+})$ and left limit $(x \to a^{-})$ look from one side. The limit exists if and only if both exist and are equal. For $f (x) = \frac{|x|}{x}$ the limits at 0 are 1 and −1, so the limit does not exist.

**Limit laws.** The limit of a sum, difference, product, constant multiple and (if the denominator's limit is not 0) quotient is obtained from the individual limits.

**Techniques (for $\frac{0}{0}$).**

| Method | Example | Result |
|---|---|---|
| Factor and cancel | $\lim_{x \to 3} \frac{x^{2} - 9}{x - 3} = \lim (x + 3)$ | 6 |
| Rationalise | $\lim_{x \to 0} \frac{\sqrt{x + 4} - 2}{x} = \lim \frac{1}{\sqrt{x + 4} + 2}$ | $\frac{1}{4}$ |
| Standard limit | $\lim_{x \to 0} \frac{\sin x}{x}$ | 1 |
| Squeeze | $\cos x \leq \frac{\sin x}{x} \leq 1$ near 0 (Figure 1.2) | 1 |

**Limits at infinity.** Divide numerator and denominator by the highest power of *x*. For example $\lim_{x \to \infty} \frac{3 x^{2} + 2 x - 1}{2 x^{2} + 5} = \lim \frac{3 + \frac{2}{x} - \frac{1}{x^{2}}}{2 + \frac{5}{x^{2}}}$ = **$\frac{3}{2}$**, so $y = \frac{3}{2}$ is a horizontal asymptote. Where a denominator tends to 0 and the numerator does not, the limit is infinite and the line $x = a$ is a vertical asymptote (Figure 1.1c). Another useful trick is $\lim_{x \to \infty} \left( \sqrt{x^{2} + x} - x \right) = \lim \frac{x}{\sqrt{x^{2} + x} + x}$ = **$\frac{1}{2}$**.

**Continuity.** *f* is continuous at a if $f (a) = \lim_{x \to a} f (x)$. Discontinuities are *removable* (a hole), *jump* (unequal one-sided limits) or *infinite*. Polynomials, $\sin ,\  \cos$ and $e^{x}$ are continuous everywhere, and sums, products and compositions of continuous functions are continuous. The **IVT** says a continuous function on $[a ,\  b]$ takes every value between $f (a)$ and $f (b)$, which is why bisection finds roots (Figure 1.3).

**Applications.** Instantaneous speed, compound interest (the number *e*) and Big-O analysis all use limits (Section 1.5).

**Conclusion.** Limits turn the impossible $\frac{0}{0}$ into a definite number. The derivative of Unit 2 and the integral of Unit 4 are both limits, so a student who is fluent here is ready for the rest of the course.
