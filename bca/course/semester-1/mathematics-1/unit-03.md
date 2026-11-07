---
subject: Mathematics I
grade: BCA Semester 1
unit: 3
title: Differentiation
area: BCA 104 · Mathematics I · Unit 3
---

The **derivative** measures the instantaneous rate of change of a function: the slope of its tangent line, the speed of a moving object, the marginal cost of one more item. This unit defines it, builds the rules that make it mechanical, and extends them to implicit, logarithmic, parametric and higher-order cases.

::: key What this unit gives you
- The derivative as a limit; differentiability versus continuity.
- The full table of derivatives and the sum, product, quotient and chain rules.
- Implicit differentiation, logarithmic differentiation, parametric differentiation.
- Higher-order derivatives and the nth derivative of standard functions.
:::

## 3.1 The derivative from first principles

The **derivative** of *f* at *x* is

$$f' (x) = \lim_{h \to 0} \frac{f (x + h) - f (x)}{h}$$

if the limit exists. Geometrically it is the slope of the tangent to $y = f (x)$ at *x*; it is also written $\frac{d y}{d x}$ or Df(x).

::: example Worked example: first principles
**$f (x) = x^{2}$.** $\frac{f (x + h) - f (x)}{h} = \frac{[(x + h)^{2} - x^{2}]}{h} = \frac{(2 x h + h^{2})}{h} = 2 x + h$ → **$2 x$**.

**$f (x) = \sqrt{x}$.** $\frac{\sqrt{x + h} - \sqrt{x}}{h} = \frac{h}{h \left( \sqrt{x + h} + \sqrt{x} \right)} = \frac{1}{\sqrt{x + h} + \sqrt{x}}$ → **$\frac{1}{2 \sqrt{x}}$**.

**$f (x) = \sin x$.** $\frac{\sin (x + h) - \sin x}{h} = \frac{\sin x (\cos h - 1)}{h} + \frac{\cos x (\sin h)}{h} \to \sin x \cdot 0 + \cos x \cdot 1$ = **$\cos x$**.
:::

**Differentiability.** If *f* is differentiable at a, it is continuous at a. The converse is false: $f (x) = |x|$ is continuous at 0 but has a corner there. The left slope is −1 and the right slope is +1, so $f' (0)$ does not exist. A function also fails to be differentiable at a vertical tangent or a discontinuity.

```svgfig label="3.1" caption="From secant to tangent for $f (x) = x^{2}$ at $P (1 ,\  1)$. The slope of the secant PQ is $\frac{f (1 + h) - f (1)}{h}$. As *h* shrinks, Q slides down the curve towards P and the secant turns into the tangent, whose slope 2 is the derivative $f' (1)$."
f = Fig(740, 290)
a = Axes(f, 30, 14, 350, 255, (-0.5, 3.2), (-0.5, 7.5)); a.grid(1, 1).axes()
a.curve(lambda x: x * x, color=NAVY, sw=2.6)
a.curve(lambda x: 1 + 3.5 * (x - 1), -0.2, 2.9, color=AMBER, sw=1.6, dash=True)
a.curve(lambda x: 1 + 2.75 * (x - 1), -0.2, 2.9, color=TEAL, sw=1.6, dash=True)
a.curve(lambda x: 2 * x - 1, -0.3, 2.9, color=RED, sw=2.4)
a.pt(1, 1, "P(1, 1)", dx=8, dy=18); a.pt(2.5, 6.25, "Q₁", color=AMBER, dx=10, dy=-10, anchor="start"); a.pt(1.75, 3.0625, "Q₂", color=TEAL, dx=16, dy=24, anchor="start")
f.text(a.X(1.9), a.Y(2.0), "tangent: slope 2", size=10.5, color=RED, bold=True, anchor="start")
f.text(430, 28, "Slope of the secant PQ", size=12, color=NAVY, bold=True, anchor="start")
rows = [("h = 1.5", "Q = (2.5, 6.25)", "3.5"), ("h = 0.75", "Q = (1.75, 3.0625)", "2.75"), ("h = 0.1", "Q = (1.1, 1.21)", "2.1"), ("h = 0.01", "Q = (1.01, 1.0201)", "2.01"), ("h → 0", "Q → P", "2  (derivative)")]
for i, (h, q, s) in enumerate(rows):
    y = 40 + i * 42
    f.box(430, y, 90, 32, h, fill=BLUE, stroke=NAVY, color=NAVY, size=11, bold=True); f.box(526, y, 120, 32, q, fill=SOFT, stroke="#94a3b8", color=SLATE, size=9.5)
    f.box(652, y, 82, 32, s, fill=MINT if i == 4 else SAND, stroke=TEAL if i == 4 else AMBER, size=10 if i == 4 else 11.5, bold=True)
f.text(430, 270, "slope = ((1 + h)² − 1)/h = 2 + h  →  2", size=11, color=SLATE, anchor="start")
```

```photogrid label="3.1" cols="3" ratio="1.0" caption="Derivative = rate of change. (a) The speedometer of a car shows the derivative of distance with respect to time. (b) Isaac Newton (1643-1727) and (c) Gottfried Wilhelm Leibniz (1646-1716) developed calculus independently; the notation $\frac{d y}{d x}$ is Leibniz's, the dot notation is Newton's."
@ photo id="bca104/speedo" cap="Speedometer: v = ds/dt"
fit 1.0
focus 0.5 0.5
call 0.5 0.93 0.5 0.62 "Reads ds/dt in km/h"
@ photo id="bca104/newton" cap="Isaac Newton"
fit 1.0
focus 0.5 0.6
@ photo id="bca104/leibniz" cap="G. W. Leibniz"
fit 1.0
focus 0.5 0.62
```

## 3.2 Rules of differentiation

| Rule | Statement |
|---|---|
| Constant | $(c)' = 0$ |
| Power | $(x^{n})' = n x^{n-1}$ (any real *n*) |
| Constant multiple, sum | $(c f)' = c f' ;\  (f \pm g)' = f' \pm g'$ |
| Product | $(f g)' = f' g + f g'$ |
| Quotient | $\left( \frac{f}{g} \right)' = \frac{f' g - f g'}{g^{2}}$ |
| Chain | $(f (g (x)))' = f' (g (x)) \cdot g' (x)$ |

**Table of standard derivatives**

| $f (x)$ | $f' (x)$ | $f (x)$ | $f' (x)$ |
|---|---|---|---|
| $e^{x}$ | $e^{x}$ | $a^{x}$ | $a^{x} \ln a$ |
| $\ln x$ | $\frac{1}{x}$ | $\log_{a} x$ | $\frac{1}{x \ln a}$ |
| $\sin x$ | $\cos x$ | $\cos x$ | $- \sin x$ |
| $\tan x$ | $\sec^{2} x$ | $\cot x$ | $- \csc^{2} x$ |
| $\sec x$ | $\sec x \tan x$ | $\csc x$ | $- \csc x \cot x$ |
| $\sin^{-1} x$ | $\frac{1}{\sqrt{1 - x^{2}}}$ | $\cos^{-1} x$ | $- \frac{1}{\sqrt{1 - x^{2}}}$ |
| $\tan^{-1} x$ | $\frac{1}{(1 + x^{2})}$ | $|x|$ | $\frac{x}{|x|} (x \neq 0)$ |

::: example Worked example: product, quotient, chain
**(a)** $\frac{d}{d x} (x^{2} \sin x) = 2 x \sin x + x^{2} \cos x$.

**(b)** $\frac{d}{d x} \left[ \frac{x^{2} + 1}{x - 1} \right] = \frac{2 x (x - 1) - (x^{2} + 1)}{(x - 1)^{2}}$ = **$\frac{x^{2} - 2 x - 1}{(x - 1)^{2}}$**.

**(c)** $\frac{d}{d x} \sin (3 x^{2}) = \cos (3 x^{2}) \cdot 6 x$ = **$6 x \cos 3 x^{2}$**.

**(d)** $\frac{d}{d x} e^{x^{2} + 1}$ = **$2 x e^{x^{2} + 1}$**.

**(e)** $\frac{d}{d x} \ln (x^{2} + 4) = \frac{2 x}{x^{2} + 4}$.

**(f)** $\frac{d}{d x} \sqrt{1 + x^{3}} = \left( \frac{1}{2} \right) (1 + x^{3})^{- \frac{1}{2}} \cdot 3 x^{2}$ = **$\frac{3 x^{2}}{2 \sqrt{1 + x^{3}}}$**.

**(g)** $\frac{d}{d x} \tan^{-1} (2 x) = \frac{2}{(1 + 4 x^{2})}$.
:::

**Chain rule in layers.** For $y = \sin^{3} (2 x)$: outer cube, middle sine, inner $2 x$. $y' = 3 \sin^{2} (2 x) \cdot \cos (2 x) \cdot 2 = 6 \sin^{2} (2 x) \cos (2 x)$.

```svgfig label="3.2" caption="A function and its derivative, read together. For $f (x) = x^{3} - 3 x$ (top) the derivative is $f' (x) = 3 x^{2} - 3$ (bottom). Where $f'$ is positive *f* rises, where $f'$ is negative *f* falls, and where $f' = 0 (x = \pm 1)$ the graph of *f* has a flat tangent: a local maximum at $x = - 1$ and a local minimum at $x = 1$."
f = Fig(740, 330)
a = Axes(f, 40, 12, 660, 140, (-2.3, 2.3), (-3.2, 3.2)); a.grid(1, 1).axes()
a.curve(lambda x: x**3 - 3 * x, color=NAVY, sw=2.6); a.pt(-1, 2, "local max (−1, 2)", dx=8, dy=-6); a.pt(1, -2, "local min (1, −2)", dx=-8, dy=18, anchor="end")
f.text(a.X(1.5), a.Y(2.8), "f(x) = x³ − 3x", size=11.5, color=NAVY, bold=True, anchor="start")
b = Axes(f, 40, 178, 660, 140, (-2.3, 2.3), (-3.5, 6.5)); b.grid(1, 2).axes()
b.curve(lambda x: 3 * x * x - 3, color=TEAL, sw=2.6); b.pt(-1, 0, "f′ = 0", dx=-8, dy=-8, anchor="end"); b.pt(1, 0, "f′ = 0", dx=8, dy=-8)
f.text(b.X(1.2), b.Y(5.6), "f′(x) = 3x² − 3", size=11.5, color=TEAL, bold=True, anchor="start")
for x in (-1, 1): f.line(a.X(x), a.Y(3.2), a.X(x), b.Y(-3.5), color=AMBER, sw=1.2, dash=True)
f.text(a.X(-1.9), b.Y(-1.7), "f′ > 0: f rising", size=10, color=TEAL, bold=True); f.text(a.X(0), b.Y(-2.4), "f′ < 0: f falling", size=10, color=TEAL, bold=True); f.text(a.X(1.9), b.Y(-1.7), "f′ > 0: rising", size=10, color=TEAL, bold=True)
```

## 3.3 Implicit differentiation

When *y* is defined implicitly by an equation in *x* and *y*, differentiate both sides with respect to *x*, treating *y* as a function of *x* (so $\frac{d}{d x} y^{2} = 2 y y'$), then solve for $y'$.

::: example Worked example
**$x^{2} + y^{2} = 25$.** $2 x + 2 y y' = 0$, so $y' = - \frac{x}{y}$. At (3, 4): slope $- \frac{3}{4}$, so the tangent is $y - 4 = - \left( \frac{3}{4} \right) (x - 3)$, i.e. $3 x + 4 y = 25$.

**$x^{3} + y^{3} = 6 x y$.** $3 x^{2} + 3 y^{2} y' = 6 y + 6 x y'$, so $y' (3 y^{2} - 6 x) = 6 y - 3 x^{2}$, giving **$y' = \frac{(2 y - x^{2})}{y^{2} - 2 x}$**.
:::

## 3.4 Logarithmic differentiation

For products and quotients with many factors, or for variable exponents $f (x)^{g (x)}$, take ln first: $\ln y = g \ln f$, then differentiate: $\frac{y'}{y} = \ldots$

::: example Worked example
**$y = x^{x}$.** $\ln y = x \ln x$, so $\frac{y'}{y} = \ln x + 1$ and **$y' = x^{x} (\ln x + 1)$**.

**$y = \frac{x^{2} (x + 1)^{3}}{\sqrt{x - 2}}$.** $\ln y = 2 \ln x + 3 \ln (x + 1) - \frac{1}{2} \ln (x - 2)$, so $\frac{y'}{y} = \frac{2}{x} + \frac{3}{x + 1} - \frac{1}{2 (x - 2)}$.

**$y = (\sin x)^{x}$.** $\ln y = x \ln \sin x ;\  y' = (\sin x)^{x} [\ln \sin x + x \cot x]$.
:::

## 3.5 Parametric differentiation

If $x = x (t) ,\  y = y (t)$, then **$\dfrac{dy}{dx} = \dfrac{dy/dt}{dx/dt}$** and **$\frac{d^{2} y}{d x^{2}} = \frac{\frac{d}{d t} \left( \frac{d y}{d x} \right)}{\frac{d x}{d t}}$**.

::: example Worked example
$x = t^{2} ,\  y = t^{3}$. $\frac{d x}{d t} = 2 t ,\  \frac{d y}{d t} = 3 t^{2}$, so $\frac{d y}{d x} = \frac{3 t}{2}$. Then $\frac{d^{2} y}{d x^{2}} = \frac{\frac{3}{2}}{2 t}$ = **$\frac{3}{4 t}$**.

For $x = a \cos t ,\  y = a \sin t ( a$ circle): $\frac{d y}{d x} = - \cot t$.
:::

## 3.6 Higher-order derivatives

The second derivative $f'' = \frac{d}{d x} (f')$ measures how the slope itself changes (concavity, acceleration). In general $f^{(n)}$ is the nth derivative.

| *y* | $y^{n} - t h$ derivative |
|---|---|
| $e^{ax}$ | $a^{n} e^{ax}$ |
| $\sin x$ | $\sin \left( x + \frac{n \pi}{2} \right)$ |
| $\cos x$ | $\cos \left( x + \frac{n \pi}{2} \right)$ |
| $(a x + b)^{m}$ | $m (m - 1) \ldots (m - n + 1) a^{n} (a x + b)^{m - n}$ |
| $\ln (a x + b)$ | $\frac{(- 1)^{n-1} (n - 1) ! a^{n}}{(a x + b)^{n}}$ |
| $\frac{1}{x + a}$ | $\frac{(- 1)^{n} n !}{(x + a)^{n+1}}$ |

::: example Worked example
**$y = x^{3} - 4 x^{2} + 5 x$:** $y' = 3 x^{2} - 8 x + 5 ,\  y'' = 6 x - 8 ,\  y''' = 6 ,\  y^{(4)} = 0$.

**$y = e^{2 x}$:** $y^{(n)} = 2^{n} e^{2 x}$; the 5th derivative is 32 $e^{2 x}$.

**$y = \sin x$:** $y'' = - \sin x ,\  y'''' = \sin x$ (period 4).

**If $y = a \cos (\ln x) + b \sin (\ln x)$, show $x^{2} y'' + x y' + y = 0$.** $y' = \frac{- a \sin (\ln x) + b \cos (\ln x)}{x}$, so $x y' = - a \sin + b \cos$. Differentiate: $y' + x y'' = ( - a \cos - b$ sin)/x, so $x y' + x^{2} y'' = - y$. Hence $x^{2} y'' + x y' + y = 0$. ∎
:::

**Leibniz's theorem** for the nth derivative of a product:

$$(uv)^{(n)} = \sum_{k=0}^{n} \binom{n}{k}\, u^{(n-k)}\, v^{(k)}$$

For $(x^2 e^x)''$: take $u = x^2$ and $v = e^x$. Then $(x^2 e^x)'' = x^2 e^x + 2(2x)\,e^x + 2\,e^x = (x^2 + 4x + 2)\,e^x$.

```svgfig label="3.3" caption="Implicit differentiation on the circle $x^{2} + y^{2} = 25$. Differentiating both sides gives $2x + 2y\,\dfrac{dy}{dx} = 0$, so $\frac{d y}{d x} = - \frac{x}{y}$. At $P(3, 4)$ the slope is $- \frac{3}{4}$, and the tangent is perpendicular to the radius OP (whose slope is $\frac{4}{3}$)."
f = Fig(740, 300)
a = Axes(f, 20, 10, 280, 280, (-7, 7), (-7, 7)); a.grid(1, 1, labels=False).axes()
a.curve(lambda x: math.sqrt(25 - x * x), -5, 5, color=NAVY, sw=2.6, n=300); a.curve(lambda x: -math.sqrt(25 - x * x), -5, 5, color=NAVY, sw=2.6, n=300)
a.curve(lambda x: 4 - 0.75 * (x - 3), -1.5, 7, color=RED, sw=2.2); a.curve(lambda x: 4 * x / 3, 0, 3, color=TEAL, sw=2, dash=True)
a.pt(3, 4, "P(3, 4)", dx=8, dy=-8); a.pt(0, 0, "O", r=3, color=SLATE, dx=-8, dy=14, anchor="end")
f.text(a.X(5.0), a.Y(3.5), "tangent", size=11, color=RED, bold=True, anchor="start")
steps = [("1. Differentiate both sides with respect to x", r"\frac{d}{dx}(x^2) + \frac{d}{dx}(y^2) = \frac{d}{dx}(25)"), ("2. Treat y as a function of x (chain rule)", r"2x + 2y \cdot \frac{dy}{dx} = 0"), ("3. Solve for dy/dx", r"\frac{dy}{dx} = -\frac{x}{y}"), ("4. Put in the point (3, 4)", r"m = -\frac{3}{4}"), ("5. Tangent line: y - 4 = m(x - 3)", r"3x + 4y = 25")]
for i, (s, e) in enumerate(steps):
    y = 18 + i * 56
    f.box(330, y, 395, 50, "", fill=BLUE if i % 2 == 0 else SOFT, stroke="#cbd5e1", r=12)
    f.text(344, y + 17, s, size=10.5, color=NAVY, bold=True, anchor="start"); f.math(344, y + 41, e, size=12.5, color=SLATE)
```

## 3.7 Eight uses of derivatives

1. **Speed and acceleration.** If $s (t)$ is the position of a vehicle, then $v = \frac{d s}{d t}$ is its speed and $a = \frac{d v}{d t} = \frac{d^{2} s}{d t^{2}}$ is its acceleration. A Kathmandu microbus driver feels the second derivative when the bus brakes at Koteshwor. Traffic engineers use these to set safe speed limits.
2. **Finding maximum profit and minimum cost.** A business writes profit as a function $P (x)$ of the number of items and solves $P' (x) = 0$. A bakery in Butwal can find the number of cakes that earns most. The second derivative then confirms that the point is a maximum and not a minimum.
3. **Tangent lines and linear approximation.** Near a point a curve looks like its tangent, so $f (x) \approx f (a) + f' (a) (x - a)$. Calculators use this to find $\sqrt{4.02} \approx 2 + 0.02 / 4 = 2.005$ quickly. Graphics software draws smooth curves in the same way.
4. **Machine learning and gradient descent.** To train a model, a computer finds the minimum of an error function by moving against the derivative. A positive slope means "go left", a negative slope means "go right". This is how recommendation and speech systems learn.
5. **Related rates.** When one quantity changes, others linked to it change too. If water is pumped into a tank at a known rate, the derivative tells how fast the level rises. Municipal water engineers use it for the tanks of the Melamchi supply.
6. **Growth and decay models.** The derivative of a population or an investment tells how fast it grows. For $P = P_{0} e^{kt}$ we get $\frac{dP}{dt} = kP$, so growth is proportional to size. This links directly to the differential equations in Unit 6.
7. **Curve sketching and optimisation in design.** The first derivative shows where a graph rises and falls, and the second shows its curvature (Figure 3.2). Designers use these to shape road curves, bridge cables and the packaging of a drink can.
8. **Sensitivity and economics.** The derivative of cost with respect to quantity is the marginal cost, the extra cost of one more unit. A hydropower plant uses marginal cost to decide how many turbines to run. In any formula, a large derivative warns that a small error in input gives a large error in output.

## Formula and fact sheet

- $f' (x) = \lim \frac{f (x + h) - f (x)}{h}$.
- $(x^{n})' = n x^{n-1} ;\  (e^{x})' = e^{x} ;\  (\ln x)' = \frac{1}{x} ;\  (\sin x)' = \cos x ;\  (\cos x)' = - \sin x ;\  (\tan x)' = \sec^{2} x$.
- $(f g)' = f' g + f g' ;\  \left( \frac{f}{g} \right)' = \frac{f' g - f g'}{g^{2}}$; chain: $f' (g) \cdot g'$.
- Implicit: differentiate both sides, $y'$ appears with each *y*.
- Log differentiation for $f^{g}$: $y' = y \left( g' \ln f + \frac{g f'}{f} \right)$.
- Parametric: $\frac{d y}{d x}$ = ẏ/ẋ.
- Differentiable ⇒ continuous (not conversely).

## Chapter summary

- The derivative is the limit of difference quotients, equal to the slope of the tangent.
- A small table plus four rules (sum, product, quotient, chain) handles nearly every function.
- Implicit, logarithmic and parametric methods cover curves not written as $y = f (x)$.
- Higher derivatives and nth-derivative formulas appear in series and in applications.

## Practice

1. Differentiate from first principles $f (x) = \frac{1}{x}$.
2. Differentiate: (a) $x^{3} e^{x}$, (b) $\frac{\ln x}{x^{2}}$, (c) $\sin (x^{2}) \cos (3 x)$, (d) $\tan^{-1} (x^{2})$.
3. Differentiate $y = (1 + x^{2})^{5}$ and $y = \sqrt{\sin x + \cos x}$.
4. Find $\frac{d y}{d x}$ if $x^{2} y + y^{3} = 10$ at (1, 2).
5. Differentiate $y = x^{\sin x}$.
6. If $x = 2 \cos t ,\  y = 3 \sin t$ find $\frac{d y}{d x}$ and $\frac{d^{2} y}{d x^{2}}$.
7. Find the nth derivative of $y = \frac{1}{x + 2}$ and of $y = \sin 3 x$.
8. Prove that if $y = e^{x} \sin x$ then $y'' - 2 y' + 2 y = 0$.
9. Find the point on $y = x^{2} - 4 x + 5$ where the tangent is parallel to the x-axis.
10. Is $f (x)$ = |x − 1| differentiable at 1? Justify.

::: note Answers and worked solutions
**1.** $\frac{\frac{1}{x + h} - \frac{1}{x}}{h} = - \frac{h}{h x (x + h)} = - \frac{1}{x (x + h)}$ → **$- \frac{1}{x^{2}}$**.

**2.** (a) **$x^{2} e^{x} (3 + x)$**. (b) $\frac{\frac{1}{x} \cdot x^{2} - \ln x \cdot 2 x}{x^{4}}$ = **$\frac{1 - 2 \ln x}{x^{3}}$**. (c) **$2 x \cos (x^{2}) \cos 3 x - 3 \sin (x^{2}) \sin 3 x$**. (d) **$\frac{2 x}{(1 + x^{4})}$**.

**3.** **$10 x (1 + x^{2})^{4}$**; **$\frac{\cos x - \sin x}{2 \sqrt{\sin x + \cos x}}$**.

**4.** $2 x y + x^{2} y' + 3 y^{2} y' = 0$, so $y' = - \frac{2 x y}{(x^{2} + 3 y^{2})}$. At (1, 2): $- \frac{4}{1 + 12}$ = **$- \frac{4}{13}$**. (Check: 1·2 + $8 = 10$ ✓.)

**5.** $\ln y = \sin x \cdot \ln x ,\  y' = x^{\sin x} \left[ \cos x \ln x + \frac{\sin x}{x} \right]$.

**6.** $\frac{d y}{d x} = \frac{3 \cos t}{- 2 \sin t}$ = **$- \left( \frac{3}{2} \right) \cot t$**. $\frac{d^{2} y}{d x^{2}} = \frac{\left( \frac{3}{2} \right) \csc^{2} t}{- 2 \sin t}$ = **$- \left( \frac{3}{4} \right) \csc^{3} t$**.

**7.** $\frac{(- 1)^{n} n !}{(x + 2)^{n+1}}$; **$3^{n} \sin \left( 3 x + \frac{n \pi}{2} \right)$**.

**8.** $y' = e^{x} (\sin x + \cos x) ,\  y'' = e^{x} (2 \cos x)$. Then $y'' - 2 y' + 2 y = e^{x} [2 \cos x - 2 \sin x - 2 \cos x + 2 \sin x] = 0$. ∎

**9.** $y' = 2 x - 4 = 0 \Rightarrow x = 2 ,\  y = 1$: **(2, 1)**.

**10.** No. Left slope −1, right slope +1, so the two one-sided derivatives differ at the corner $x = 1$ although *f* is continuous there.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q (5 marks). Find the derivative of $f (x) = \sqrt{x}$ from first principles. Find also the slope of the curve at $x = 4$.**

The **derivative** of *f* at *x* is defined by the limit $f' (x) = \lim_{h \to 0} \frac{f (x + h) - f (x)}{h}$, provided the limit exists. It is the slope of the tangent line (Figure 3.1).

1. Write the difference quotient: $\frac{\sqrt{x + h} - \sqrt{x}}{h}$. Putting $h = 0$ gives $\frac{0}{0}$, so we rationalise.
2. Multiply top and bottom by the conjugate $\sqrt{x + h} + \sqrt{x}$. The numerator becomes $(x + h) - x = h$.
3. The quotient is $\frac{h}{h \left( \sqrt{x + h} + \sqrt{x} \right)} = \frac{1}{\sqrt{x + h} + \sqrt{x}}$ for $h \neq 0$.
4. Let $h \to 0$: the denominator tends to $\sqrt{x} + \sqrt{x} = 2 \sqrt{x}$.

So **$f' (x) = \frac{1}{2 \sqrt{x}}$** for $x > 0$. At $x = 4$ the slope is $\frac{1}{2 \times 2}$ = **$\frac{1}{4}$**, and the tangent line is $y - 2 = \frac{1}{4} (x - 4)$. *Check:* between $x = 4$ and $x = 4.04 ,\  \sqrt{4.04} - \sqrt{4} = 2.00998 - 2 = 0.00998$, and $0.00998 / 0.04 \approx 0.2495$, close to $\frac{1}{4}$.

**Q (5 marks). If $x^{3} + y^{3} = 6 x y$, find $\frac{d y}{d x}$ by implicit differentiation and the slope of the tangent at (3, 3).**

When *y* cannot be easily written as a function of *x* we differentiate both sides with respect to *x*, remembering that *y* depends on *x*, so $\frac{d (y^{3})}{d x} = 3 y^{2} \cdot \frac{d y}{d x}$ (chain rule).

1. Differentiate: $3 x^{2} + 3 y^{2} \cdot \frac{d y}{d x} = 6 y + 6 x \cdot \frac{d y}{d x}$ (the product rule is used on $6 x y$).
2. Collect the $\frac{d y}{d x}$ terms on one side: $3 y^{2} \cdot \frac{d y}{d x} - 6 x \cdot \frac{d y}{d x} = 6 y - 3 x^{2}$.
3. Factor: $\frac{d y}{d x} (3 y^{2} - 6 x) = 6 y - 3 x^{2}$.
4. Divide: **$\frac{d y}{d x} = \frac{(2 y - x^{2})}{y^{2} - 2 x}$**.
5. At (3, 3): the numerator is $6 - 9 = - 3$ and the denominator is $9 - 6 = 3$, so the slope is **−1**.

The point (3, 3) lies on the curve $(27 + 27 = 54 = 6 \times 9)$, so the question is valid. The tangent there is $y - 3 = - (x - 3)$, that is $x + y = 6$. This curve is the *folium of Descartes*, and the symmetry about $y = x$ explains the slope −1 at its point on that line.

**Q (10 marks). Define the derivative and explain its geometrical meaning. State and illustrate the main rules of differentiation, and explain implicit, logarithmic and parametric differentiation with one example each.**

**Introduction.** The derivative of $y = f (x)$ is $f' (x) = \frac{d y}{d x} = \lim_{h \to 0} \frac{f (x + h) - f (x)}{h}$. Geometrically it is the **slope of the tangent** at the point $(x ,\  f (x))$, the limit of secant slopes as the second point approaches the first (Figure 3.1). Physically it is the instantaneous rate of change, such as speed from distance (Plate 3.1a).

**Rules of differentiation.**

| Rule | Formula | Example |
|---|---|---|
| Constant, power | $\frac{d (x^{n})}{d x} = n x^{n-1}$ | $\frac{d (x^{4} - 2 x^{3})}{d x} = 4 x^{3} - 6 x^{2}$ |
| Sum | $(u + v)' = u' + v'$ |  |
| Product | $(u v)' = u' v + u v'$ | $\frac{d (x^{2} e^{x})}{d x} = e^{x} (x^{2} + 2 x)$ |
| Quotient | $\left( \frac{u}{v} \right)' = \frac{u' v - u v'}{v^{2}}$ | $\frac{d \left( \frac{x + 1}{x - 1} \right)}{d x} = - \frac{2}{(x - 1)^{2}}$ |
| Chain | $\frac{d f (g (x))}{d x} = f' (g (x)) g' (x)$ | $\frac{d (\sin x^{2})}{d x} = 2 x \cos x^{2}$ |

**Standard derivatives.** $(\sin x)' = \cos x ,\  (\cos x)' = - \sin x ,\  (e^{x})' = e^{x} ,\  (\ln x)' = \frac{1}{x} ,\  (\tan x)' = \sec^{2} x$.

**Implicit differentiation.** For $x^{2} + y^{2} = 25$ differentiate both sides: $2x + 2y\,\dfrac{dy}{dx} = 0$, so $\frac{d y}{d x} = - \frac{x}{y}$; at (3, 4) the slope is $- \frac{3}{4}$ (Figure 3.3).

**Logarithmic differentiation.** For $y = x^{x}$ take logarithms: $\ln y = x \ln x$. Differentiate: $\frac{y'}{y} = \ln x + 1$, so **$y' = x^{x} (\ln x + 1)$**. It is the method for variable exponents and long products.

**Parametric differentiation.** If $x = a \cos t ,\  y = a \sin t$, then $\dfrac{dy}{dx} = \dfrac{dy/dt}{dx/dt} = \dfrac{a \cos t}{- a \sin t}$ = **$- \cot t$**, and the second derivative is $\frac{d^{2} y}{d x^{2}} = ( \frac{d}{d t}$ of dy/dx)/(dx/dt) = $\frac{\csc^{2} t}{- a \sin t}$ = **$- \frac{1}{a \sin^{3} t}$**.

**Higher derivatives.** Differentiating again gives $f''$, which measures curvature: $f'' > 0$ means the graph bends upward, $f'' < 0$ downward. If *s* is position, then $s''$ is acceleration.

**Relation to the graph.** Where $f' > 0$ the function rises; where $f' = 0$ the tangent is flat, giving a possible maximum or minimum (Figure 3.2).

**Conclusion.** The derivative is a limit, and the rules allow us to compute it quickly without returning to the limit each time. In Unit 4 it will be used to optimise, approximate and sketch.
