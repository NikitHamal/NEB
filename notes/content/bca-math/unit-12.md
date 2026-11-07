---
subject: Mathematics
grade: BCA
unit: 12
title: Limits and Differentiation
hours: 4
area: Calculus
---

Calculus is 6–8 of the 50 questions, shared between this chapter and the next. The questions are rarely deep: a standard limit, a derivative by the product or quotient rule, a slope of a tangent, a maximum or minimum. The Dean's Office model asks $\lim_{x\to0}\frac{|\sin x|}{x}$ (it does not exist) and the derivative of $x^2\cos x$. Know the standard limits and the derivative table and these are quick.

::: key What the paper asks from this chapter
- **Standard limits**: $\frac{\sin x}{x}\to1$, $\frac{x^n-a^n}{x-a}\to na^{n-1}$, $(1+x)^{1/x}\to e$, $\frac{e^x-1}{x}\to1$.
- **Derivatives**: power, trig, exponential, log; product, quotient, chain.
- **Applications**: slope of tangent, maximum/minimum, rate of change, increasing/decreasing.
:::

## 12.1 Limits of algebraic and trigonometric functions

- Substitute first. If you get $\frac{0}{0}$, factor and cancel, or use a standard limit.
- $\lim_{x\to a}\frac{x^n-a^n}{x-a}=na^{n-1}$; $\lim_{x\to0}\frac{\sin x}{x}=\lim_{x\to0}\frac{\tan x}{x}=1$; $\lim_{x\to0}\frac{\sin kx}{x}=k$; $\lim_{x\to0}\frac{1-\cos x}{x^2}=\frac{1}{2}$.
- $\lim_{x\to0}\frac{e^x-1}{x}=1$, $\lim_{x\to0}\frac{\ln(1+x)}{x}=1$, $\lim_{x\to0}(1+x)^{1/x}=e$.
- At infinity divide by the highest power: $\lim_{x\to\infty}\frac{3x^2+2x}{x^2+5}=3$.
- A limit exists only if the left and right limits agree: $\frac{|\sin x|}{x}$ tends to $-1$ from the left and $+1$ from the right, so it does not exist.

```svgfig label="12.1" caption="Limits as the value a function approaches. (a) sin x / x is undefined at x = 0 but approaches 1: at x = 0.1 it is 0.99833 and at x = 0.01 it is 0.99998 (x in radians). (b) (x^2 - 9)/(x - 3) equals x + 3 for every x except 3, so the graph is the line y = x + 3 with a hole at (3, 6); the limit at 3 is 6 even though the function has no value there. Making f(3) = 6 repairs the hole."
import math
sinc = lambda x: math.sin(x) / x
assert round(sinc(0.1), 5) == 0.99833 and round(sinc(0.01), 5) == 0.99998 and abs(sinc(1e-6) - 1) < 1e-9
g = lambda x: (x * x - 9) / (x - 3)
assert all(abs(g(x) - (x + 3)) < 1e-9 for x in (2.9, 2.99, 3.01, 3.1)) and round(g(2.999), 3) == 5.999
f = Fig(780, 320)
ax = Axes(f, 30, 20, 330, 250, (-10, 10), (-0.4, 1.2))
ax.grid(5, 0.4, size=10); ax.axes("x", "y")
ax.curve(lambda x: sinc(x) if abs(x) > 1e-9 else 1, -10, 10, color=NAVY, sw=2.4, n=400)
ax.pt(0, 1, "", r=4.5, color=RED, hollow=True); f.text(ax.X(0) + 10, ax.Y(1) - 8, "limit 1 at x = 0", size=10.5, color=RED, bold=True, anchor="start")
f.text(190, 296, "y = sin x / x  (no value at 0, limit 1)", size=10.5, color=NAVY, bold=True)
ax2 = Axes(f, 400, 20, 250, 250, (-1, 7), (0, 10))
ax2.grid(1, 2, size=10); ax2.axes("x", "y")
ax2.curve(lambda x: x + 3, -1, 7, color=TEAL, sw=2.4); ax2.pt(3, 6, "hole (3, 6)", r=5, color=RED, dx=10, dy=18, hollow=True)
f.text(525, 296, "y = (x^2 - 9)/(x - 3) = x + 3, limit 6 at x = 3", size=10, color=TEAL, bold=True)
f.text(715, 60, "Standard", size=10.5, color=NAVY, bold=True); f.text(715, 80, "limits", size=10.5, color=NAVY, bold=True)
for j, t in enumerate(["sin x / x -> 1", "(e^x - 1)/x -> 1", "(1 - cos x)/x^2 -> 1/2", "(x^n - a^n)/(x - a) -> n a^(n-1)", "(1 + 1/x)^x -> e"]):
    f.text(668, 110 + j * 26, t, size=9.5, color=SLATE, anchor="start")
```

## 12.2 Continuity

$f$ is continuous at $a$ if $\lim_{x\to a}f(x)=f(a)$. To make $f(x)=\frac{x^2-9}{x-3}$ continuous at 3, define $f(3)=6$ (the limit).

```svgfig label="12.2" caption="The derivative is the limit of secant slopes. For f(x) = x^2 at x = 1, the secant slope from x = 1 to 1 + h is 2 + h: 3 for h = 1, 2.1 for h = 0.1 and 2.01 for h = 0.01, closing in on f'(1) = 2. The tangent there is y - 1 = 2(x - 1), i.e. y = 2x - 1. The graph shows the parabola, the secant for h = 1 and the tangent."
fn = lambda x: x * x
sec = lambda h: (fn(1 + h) - fn(1)) / h
assert [round(sec(h), 6) for h in (1, 0.1, 0.01)] == [3.0, 2.1, 2.01] and abs(sec(1e-7) - 2) < 1e-6
f = Fig(780, 320)
ax = Axes(f, 30, 20, 330, 270, (-1, 3.5), (-1, 9))
ax.grid(1, 1, size=10); ax.axes("x", "y")
ax.curve(fn, -1, 3, color=NAVY, sw=2.5); ax.curve(lambda x: 3 * x - 2, -0.5, 3.2, color=AMBER, sw=1.8, dash=True); ax.curve(lambda x: 2 * x - 1, -0.5, 3.2, color=RED, sw=2.4)
ax.pt(1, 1, "(1, 1)", r=5, color=RED, dx=10, dy=18); ax.pt(2, 4, "(2, 4)", r=4, color=AMBER, dx=-8, dy=-8, anchor="end")
f.text(ax.X(-0.9), ax.Y(8.2), "y = x^2", size=11, color=NAVY, bold=True, anchor="start"); f.text(ax.X(2.3), ax.Y(2.3), "tangent y = 2x - 1", size=10.5, color=RED, bold=True, anchor="start"); f.text(ax.X(0.2), ax.Y(5), "secant (h = 1), slope 3", size=10.5, color=AMBER, bold=True, anchor="start")
f.text(570, 30, "Secant slopes at x = 1", size=11.5, color=NAVY, bold=True)
for j, h in enumerate([1, 0.5, 0.1, 0.01, 0.001]):
    f.box(430, 48 + j * 34, 300, 28, "h = %g:  slope = %g" % (h, round(sec(h), 4)), fill=(SOFT if j % 2 else BLUE), stroke="#cbd5e1", size=11, bold=True, color=NAVY, r=3)
f.text(580, 240, "limit: f'(1) = 2 (h goes to 0)", size=11.5, color=RED, bold=True)
f.text(580, 266, "f'(x) = lim [f(x+h) - f(x)] / h", size=10.5, color=SLATE)
```

## 12.3 Derivatives, rules and standard results

| $f(x)$ | $f'(x)$ | $f(x)$ | $f'(x)$ |
|---|---|---|---|
| $x^n$ | $nx^{n-1}$ | $\sin x$ | $\cos x$ |
| constant | 0 | $\cos x$ | $-\sin x$ |
| $e^x$ | $e^x$ | $\tan x$ | $\sec^2x$ |
| $a^x$ | $a^x\ln a$ | $\ln x$ | $\frac{1}{x}$ |
| $\sqrt{x}$ | $\frac{1}{2\sqrt{x}}$ | $\frac{1}{x}$ | $-\frac{1}{x^2}$ |

Product: $(uv)'=u'v+uv'$. Quotient: $\left(\frac{u}{v}\right)'=\frac{u'v-uv'}{v^2}$. Chain: $\frac{d}{dx}f(g(x))=f'(g(x))g'(x)$. Example: $\frac{d}{dx}(x^2\cos x)=2x\cos x-x^2\sin x$.

```photogrid label="12.1" cols="3" ratio="1.0" caption="Calculus, invented twice. (a) Gottfried Wilhelm Leibniz (1646-1716), who gave us the notation dy/dx and the integral sign. (b) Sir Isaac Newton (1642-1727, portrait of 1689), who developed the same ideas as fluxions. (c) A speedometer: the dial shows the derivative of distance with respect to time."
@ photo id="bcamath/leibniz" cap="Leibniz: the notation dy/dx"
focus 0.5 0.3
@ photo id="bcamath/newton" cap="Newton: fluxions"
focus 0.5 0.3
@ photo id="bca104/speedo" cap="Speedometer: rate of change of distance"
focus 0.5 0.5
```

```svgfig label="12.3" caption="A function and its derivative together. f(x) = x^3 - 3x has f'(x) = 3x^2 - 3 = 0 at x = -1 and 1. f''(x) = 6x gives f''(-1) = -6 < 0 (a maximum, f = 2) and f''(1) = 6 > 0 (a minimum, f = -2). Where f' is positive f rises; where f' is negative f falls, and the turning points of f are the zeros of f'."
fn = lambda x: x ** 3 - 3 * x; d1 = lambda x: 3 * x * x - 3; d2 = lambda x: 6 * x
assert [d1(-1), d1(1)] == [0, 0] and (fn(-1), fn(1)) == (2, -2) and d2(-1) == -6 and d2(1) == 6
f = Fig(780, 320)
ax = Axes(f, 30, 20, 350, 270, (-2.5, 2.5), (-4, 6))
ax.grid(1, 2, size=10); ax.axes("x", "y")
ax.curve(fn, -2.3, 2.3, color=NAVY, sw=2.6); ax.curve(d1, -2.3, 2.3, color=TEAL, sw=2.2, dash=True)
ax.pt(-1, 2, "max (-1, 2)", r=5, color=RED, dx=-8, dy=-10, anchor="end"); ax.pt(1, -2, "min (1, -2)", r=5, color=RED, dx=8, dy=20)
f.text(ax.X(1.9), ax.Y(2.4), "f", size=12, color=NAVY, bold=True); f.text(ax.X(-1.8), ax.Y(5), "f' (dashed)", size=11, color=TEAL, bold=True, anchor="start")
f.text(600, 30, "Test for turning points", size=11.5, color=NAVY, bold=True)
for j, (t, c) in enumerate([("f(x) = x^3 - 3x", NAVY), ("f'(x) = 3x^2 - 3 = 0  gives  x = -1, 1", SLATE), ("f''(x) = 6x", SLATE), ("f''(-1) = -6 < 0: MAXIMUM, f = 2", RED), ("f''(1) = 6 > 0: MINIMUM, f = -2", RED), ("f' > 0: f increasing (x < -1, x > 1)", TEAL), ("f' < 0: f decreasing (-1 < x < 1)", TEAL), ("f' = 0 alone is not enough: y = x^3", SLATE)]):
    f.text(420, 64 + j * 30, t, size=10.5, color=c, anchor="start", bold=(c in (NAVY, RED)))
```

```svgfig label="12.4" caption="Optimisation and related rates, computed. (a) A rectangle of perimeter 40 has area A = x(20 - x); A' = 20 - 2x = 0 at x = 10, so the maximum area is 100 (a square). (b) A circular ripple with radius 5 cm growing at 2 cm/s: dA/dt = 2 pi r dr/dt = 2 pi x 5 x 2 = 62.83 cm2/s. A balloon of radius 3 cm growing at 0.5 cm/s: dV/dt = 4 pi r^2 dr/dt = 18 pi = 56.55 cm3/s."
import math
A = lambda x: x * (20 - x); assert max(A(x / 10) for x in range(0, 201)) == 100 and A(10) == 100
dA = 2 * math.pi * 5 * 2; dV = 4 * math.pi * 9 * 0.5; assert round(dA, 2) == 62.83 and round(dV, 2) == 56.55 and round(dV, 2) == round(18 * math.pi, 2)
f = Fig(780, 320)
ax = Axes(f, 30, 20, 330, 250, (0, 20), (0, 110))
ax.grid(5, 20, size=10); ax.axes("x", "A")
ax.curve(A, 0, 20, color=NAVY, sw=2.6); ax.pt(10, 100, "max: x = 10, A = 100", r=5, color=RED, dx=-10, dy=-12, anchor="middle")
f.text(190, 296, "A = x(20 - x), perimeter 2(x + 20 - x) = 40", size=10.5, color=NAVY, bold=True)
f.text(560, 30, "Related rates (chain rule)", size=11.5, color=NAVY, bold=True)
for j, (t, c) in enumerate([("ripple: A = pi r^2", NAVY), ("dA/dt = 2 pi r dr/dt", SLATE), ("r = 5, dr/dt = 2:  dA/dt = 20 pi", SLATE), ("= 62.83 cm2/s", RED), ("balloon: V = (4/3) pi r^3", NAVY), ("dV/dt = 4 pi r^2 dr/dt", SLATE), ("r = 3, dr/dt = 0.5:  dV/dt = 18 pi", SLATE), ("= 56.55 cm3/s", RED), ("two numbers with sum S: max product (S/2)^2", TEAL)]):
    f.text(410, 64 + j * 27, t, size=10.5, color=c, anchor="start", bold=(c in (NAVY, RED)))
```

## 12.5 Eight traps in limits and differentiation

Calculus questions in the entrance paper are mostly one-step rules, so the trap is almost always a missed rule or a value substituted too early. These eight traps cover the model questions on limits, derivatives and maxima.

1. **Substitute first, and treat $\frac00$ as a signal.** If direct substitution gives a number, that number is the limit. If it gives $\frac00$, factor and cancel, rationalise or use a standard limit: $\frac{x^2-9}{x-3}=x+3$ so the limit at 3 is 6 (Fig 12.1). A limit describes where $f$ is heading, not what $f$ equals at the point.
2. **Know the standard limits and their conditions.** $\lim_{x\to0}\frac{\sin x}{x}=1$ only for $x$ in radians and $x\to0$, and $\lim_{x\to0}\frac{\sin kx}{x}=k$. Also $\lim\frac{1-\cos x}{x^2}=\frac12$, $\lim\frac{e^x-1}{x}=1$ and $\lim_{x\to\infty}\left(1+\frac1x\right)^x=e$. A common slip is to say $\lim\frac{\sin x}{x}=1$ as $x\to\infty$, when it is 0.
3. **At infinity, divide by the highest power.** For $\frac{3x^2+2x}{x^2+5}$ the limit is 3. If the numerator's degree is lower the limit is 0, and if it is higher the limit is infinite. Do not cancel the leading terms without dividing the whole expression.
4. **Check both sides and the value for continuity.** A limit exists only if the left and right limits agree, so $\frac{|x|}{x}$ has no limit at 0. A function is continuous at $a$ when $f(a)$ exists, $\lim_{x\to a}f(x)$ exists and the two are equal. To repair $\frac{x^2-9}{x-3}$ define $f(3)=6$.
5. **Apply the right rule, and the chain rule every time.** Product: $(uv)'=u'v+uv'$, quotient: $\frac{u'v-uv'}{v^2}$ with the order $u'v-uv'$, and chain: differentiate the outside, then multiply by the derivative of the inside. So $\frac{d}{dx}\sin2x=2\cos2x$, $\frac{d}{dx}a^x=a^x\ln a$ and $\frac{d}{dx}\tan x=\sec^2x$. The derivative of a constant is 0.
6. **Tangent uses $f'(a)$; normal uses its negative reciprocal.** The tangent at $x=1$ on $y=x^2$ has slope 2 and equation $y=2x-1$ (Fig 12.2). The normal has slope $-\frac12$. Check that the tangent passes through the point of contact.
7. **$f'=0$ finds candidates; $f''$ decides.** $f''<0$ means a maximum and $f''>0$ means a minimum (Fig 12.3). If $f''=0$ the test fails: $y=x^3$ has $f'(0)=0$ but no turning point. On a closed interval also compare the end-point values.
8. **For rates, link the variables by the chain rule, and keep units.** $\frac{dA}{dt}=\frac{dA}{dr}\cdot\frac{dr}{dt}$, so a ripple of radius 5 cm growing at 2 cm/s has $\frac{dA}{dt}=62.83$ cm$^2$/s (Fig 12.4). Write the quantity to optimise in a single variable before differentiating. For two numbers with a fixed sum, the product is greatest when they are equal.

### 12.5.1 Worked checks

**Q. Evaluate $\lim_{x\to2}\frac{x^2-4}{x-2}$ and $\lim_{x\to0}\frac{\sin3x}{x}$.**

**Answer.** Factor: $\frac{(x-2)(x+2)}{x-2}=x+2\to4$. For the second use $\lim\frac{\sin kx}{x}=k$, so the limit is 3. Both would give $\frac00$ if substituted straight in.

**Q. Differentiate $y=x^2\cos x$ and find the tangent to $y=x^2$ at $x=1$.**

**Answer.** Product rule: $y'=2x\cos x-x^2\sin x$. For the tangent, $f'(1)=2$ and $f(1)=1$, so $y-1=2(x-1)$, i.e. $y=2x-1$. This is the red line in Fig 12.2.

**Q. Two positive numbers have sum 20. Find the greatest possible product.**

**Answer.** Let the numbers be $x$ and $20-x$, so $P=20x-x^2$ and $P'=20-2x=0$ gives $x=10$. $P''=-2<0$, so this is a maximum, $P=10\times10=100$. Check: $9\times11=99<100$.

## 12.4 Tangents, maxima, minima and rates

- Slope of the tangent at $x=a$ is $f'(a)$; the tangent is parallel to $y=mx+c$ where $f'(x)=m$.
- Stationary points: $f'(x)=0$. Then $f''>0$ gives a minimum, $f''<0$ a maximum. $f'>0$ means increasing.
- Rates: $\frac{dA}{dt}=\frac{dA}{dr}\cdot\frac{dr}{dt}$. For a circle $\frac{dA}{dr}=2\pi r$; for a sphere $\frac{dV}{dr}=4\pi r^2$.
- Two numbers with sum $S$ have maximum product $\left(\frac{S}{2}\right)^2$.

## Formula and fact sheet

| Item | Result |
|---|---|
| $\frac{d}{dx}x^n$ | $nx^{n-1}$ |
| Product / quotient | $u'v+uv'$ / $\frac{u'v-uv'}{v^2}$ |
| $\lim\frac{\sin x}{x}$ | 1 |
| Max/min test | $f'=0$; $f''<0$ max, $f''>0$ min |

## Chapter summary

- Substitute, then factor or use a standard limit for $\frac{0}{0}$.
- $\lim\frac{|\sin x|}{x}$ does not exist at 0.
- Differentiate by the product rule when two functions of $x$ multiply.
- Stationary points need $f'=0$; the sign of $f''$ decides the type.
- Rates multiply by the chain rule.

## Practice questions

**Set A — Recall (20 questions)**

1. $\lim_{x\to0}\frac{\sin x}{x}$ equals
   (a) 0 (b) infinity (c) 1 (d) $-1$
2. $\frac{d}{dx}(x^3)$ equals
   (a) $3x^2$ (b) $x^2$ (c) $3x$ (d) $\frac{x^4}{4}$
3. $\frac{d}{dx}(\sin x)$ equals
   (a) $-\cos x$ (b) $\sin x$ (c) $-\sin x$ (d) $\cos x$
4. $\frac{d}{dx}(\ln x)$ equals
   (a) $x$ (b) $\frac{1}{x}$ (c) $\ln x$ (d) $e^x$
5. $\frac{d}{dx}(e^x)$ equals
   (a) $e^x$ (b) $xe^{x-1}$ (c) 1 (d) $\ln x$
6. $\lim_{x\to2}\frac{x^2-4}{x-2}$ equals
   (a) 0 (b) 2 (c) 4 (d) does not exist
7. $\frac{d}{dx}(\cos x)$ equals
   (a) $\sin x$ (b) $\cos x$ (c) $-\cos x$ (d) $-\sin x$
8. The derivative of a constant is
   (a) 1 (b) 0 (c) the constant itself (d) infinity
9. $\lim_{x\to\infty}\frac{1}{x}$ equals
   (a) infinity (b) 1 (c) 0 (d) $-1$
10. $\frac{d}{dx}(\tan x)$ equals
    (a) $\sec^2x$ (b) $\cot x$ (c) $-\csc^2x$ (d) $\sec x\tan x$
11. If $f(x)=x^2$, then $f'(3)$ is
    (a) 9 (b) 3 (c) 2 (d) 6
12. $f$ has a local minimum at $x=a$ if $f'(a)=0$ and $f''(a)$ is
    (a) negative (b) positive (c) zero (d) undefined
13. $\lim_{x\to0}\frac{e^x-1}{x}$ equals
    (a) 1 (b) 0 (c) $e$ (d) infinity
14. $\frac{d}{dx}(5x^2+3x)$ equals
    (a) $5x+3$ (b) $10x$ (c) $10x+3$ (d) $10x^2+3$
15. The slope of the tangent to $y=x^2$ at $x=2$ is
    (a) 2 (b) 8 (c) 1 (d) 4
16. $\frac{d}{dx}(uv)$ equals
    (a) $u'v'$ (b) $u'v+uv'$ (c) $u'v-uv'$ (d) $\frac{u'v-uv'}{v^2}$
17. $\lim_{x\to0}(1+x)^{1/x}$ equals
    (a) 1 (b) 0 (c) $e$ (d) infinity
18. $\frac{d}{dx}\left(\frac{1}{x}\right)$ equals
    (a) $-\frac{1}{x^2}$ (b) $\frac{1}{x^2}$ (c) $\ln x$ (d) $-\frac{1}{x}$
19. $\lim_{x\to0}\frac{\tan x}{x}$ equals
    (a) 0 (b) infinity (c) $-1$ (d) 1
20. $\frac{d}{dx}(\sqrt{x})$ equals
    (a) $\frac{1}{\sqrt{x}}$ (b) $\frac{1}{2\sqrt{x}}$ (c) $2\sqrt{x}$ (d) $\frac{\sqrt{x}}{2}$

::: note Answers and explanations — Set A
**1.** (c) — the basic trigonometric limit.
**2.** (a) — power rule.
**3.** (d) — sin → cos.
**4.** (b) — the log derivative.
**5.** (a) — eˣ is its own derivative.
**6.** (c) — (x − 2)(x + 2)/(x − 2) → 4.
**7.** (d) — cos → −sin.
**8.** (b) — constants do not change.
**9.** (c) — 1/x shrinks to 0.
**10.** (a) — tan → sec².
**11.** (d) — 2x at x = 3 is 6.
**12.** (b) — f″ > 0 gives a minimum.
**13.** (a) — standard limit.
**14.** (c) — 10x + 3.
**15.** (d) — 2x at x = 2.
**16.** (b) — product rule; (d) is the quotient rule.
**17.** (c) — definition of e.
**18.** (a) — −x⁻².
**19.** (d) — tan x ≈ x for small x.
**20.** (b) — ½x^(−1/2).
:::

**Set B — Understanding (12 questions)**

1. $\lim_{x\to0}\frac{\sin3x}{x}$ equals
   (a) 1 (b) 3 (c) $\frac{1}{3}$ (d) 0
2. $\frac{d}{dx}(x^2\cos x)$ equals
   (a) $2x\cos x+x^2\sin x$ (b) $-2x\sin x$ (c) $2x\cos x$ (d) $2x\cos x-x^2\sin x$
3. $\lim_{x\to\infty}\frac{3x^2+2x}{x^2+5}$ equals
   (a) 2 (b) 0 (c) 3 (d) infinity
4. $\lim_{x\to0}\frac{1-\cos x}{x^2}$ equals
   (a) $\frac{1}{2}$ (b) 1 (c) 0 (d) 2
5. $\lim_{x\to1}\frac{x^3-1}{x-1}$ equals
   (a) 0 (b) 1 (c) 2 (d) 3
6. $\frac{d}{dx}\left(\frac{x}{x+1}\right)$ equals
   (a) $\frac{1}{x+1}$ (b) $\frac{1}{(x+1)^2}$ (c) $\frac{x}{(x+1)^2}$ (d) $-\frac{1}{(x+1)^2}$
7. The minimum value of $x^2-4x+7$ is
   (a) 3 (b) 7 (c) 2 (d) 4
8. $f(x)=x^3-3x$ has a local maximum at $x=$
   (a) 1 (b) 0 (c) $-1$ (d) 3
9. The tangent to $y=x^3$ at $(1,1)$ meets the $y$-axis at
   (a) $(0,2)$ (b) $(0,-2)$ (c) $(0,3)$ (d) $(0,-3)$
10. The rate of change of the area of a circle with respect to its radius at $r=5$ is
    (a) $25\pi$ (b) $5\pi$ (c) $\pi$ (d) $10\pi$
11. $\lim_{x\to0}\frac{|\sin x|}{x}$
    (a) does not exist (b) equals 1 (c) equals $-1$ (d) equals 0
12. $f(x)=\frac{x^2-9}{x-3}$ for $x\ne3$ is continuous at 3 if $f(3)$ equals
    (a) 0 (b) 3 (c) 6 (d) 9

::: note Answers and explanations — Set B
**1.** (b) — sin 3x / x → 3.
**2.** (d) — product rule: 2x·cos x + x²(−sin x).
**3.** (c) — leading coefficients 3/1.
**4.** (a) — standard limit ½.
**5.** (d) — n aⁿ⁻¹ = 3.
**6.** (b) — ((x + 1) − x)/(x + 1)².
**7.** (a) — (x − 2)² + 3.
**8.** (c) — f′ = 3x² − 3 = 0 at ±1; f″ = 6x is negative at −1.
**9.** (b) — tangent y = 3x − 2.
**10.** (d) — 2πr = 10π.
**11.** (a) — left limit −1, right limit +1.
**12.** (c) — the limit is x + 3 = 6.
:::

**Set C — Application (8 questions)**

1. $\lim_{x\to0}\frac{\sin5x}{\sin2x}$ equals
   (a) $\frac{2}{5}$ (b) 1 (c) 3 (d) $\frac{5}{2}$
2. Two positive numbers have sum 20. Their greatest possible product is
   (a) 100 (b) 96 (c) 99 (d) 120
3. A spherical balloon's radius grows at 2 cm/s. At $r=3$ cm the volume grows at
   (a) $36\pi$ cm³/s (b) $24\pi$ cm³/s (c) $72\pi$ cm³/s (d) $18\pi$ cm³/s
4. The local maximum value of $x^3-6x^2+9x$ is
   (a) 0 (b) 4 (c) 9 (d) 3
5. If $y=\sin x\cos x$, then $\frac{dy}{dx}$ at $x=0$ is
   (a) 0 (b) $\frac{1}{2}$ (c) $-1$ (d) 1
6. $\frac{d}{dx}(xe^x)$ at $x=0$ is
   (a) 0 (b) $e$ (c) 1 (d) 2
7. The tangent to $y=x^2$ is parallel to $y=4x+1$ at the point
   (a) $(2,4)$ (b) $(4,16)$ (c) $(1,1)$ (d) $(-2,4)$
8. $f(x)=2x^3-9x^2+12x$ is decreasing on
   (a) $x<1$ (b) $1<x<2$ (c) $x>2$ (d) all real numbers

::: note Answers and explanations — Set C
**1.** (d) — (5x)/(2x) as x → 0.
**2.** (a) — x(20 − x) is greatest at x = 10.
**3.** (c) — 4πr² · dr/dt = 4π · 9 · 2.
**4.** (b) — maximum at x = 1: 1 − 6 + 9 = 4 (the minimum 0 is at x = 3).
**5.** (d) — dy/dx = cos 2x, equal to 1 at 0.
**6.** (c) — eˣ(1 + x) = 1.
**7.** (a) — 2x = 4 gives x = 2, y = 4.
**8.** (b) — f′ = 6(x − 1)(x − 2) is negative between 1 and 2.
:::
