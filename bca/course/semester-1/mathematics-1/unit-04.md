---
subject: Mathematics I
grade: BCA Semester 1
unit: 4
title: Applications of Derivatives
area: BCA 104 · Mathematics I · Unit 4
---

Derivatives are used to describe tangents, rates, optimum values and approximations. This unit turns the differentiation rules of Unit 3 into tools for solving problems: tangent lines, related rates, maxima and minima, the mean value theorems, L'Hôpital's rule and Taylor/Maclaurin series.

::: key What this unit gives you
- Tangent and normal lines; rates of change and related rates.
- Increasing/decreasing functions, maxima and minima, optimisation, concavity.
- Rolle's theorem, the mean value theorem, L'Hôpital's rule.
- Maclaurin and Taylor series, with numerical approximation.
:::

## 4.1 Tangent and normal

The tangent to $y = f (x)$ at $(a ,\  f (a))$ has slope $m = f' (a)$: **$y - f (a) = f' (a) (x - a)$**. The normal is perpendicular, with slope $- \frac{1}{f' (a)}$ (if $f' (a) \neq 0$).

::: example Worked example
For $y = x^{3} - 2 x + 1$ at $x = 1$: $y (1) = 0$ and $y' = 3 x^{2} - 2 = 1$. Tangent: $y = x - 1$. Normal: slope −1, so $y = - (x - 1) = 1 - x$.
:::

## 4.2 Rates of change and related rates

$\frac{d y}{d x}$ is the rate of change of *y* with respect to *x*. For a position function $s (t)$: velocity $v = \frac{d s}{d t}$, acceleration $a = \frac{d v}{d t} = \frac{d^{2} s}{d t^{2}}$.

**Related rates**: two quantities are tied by an equation; differentiate it with respect to time.

::: example Worked example: sliding ladder
A 10 *m* ladder leans on a wall; the foot slides away at 2 $\frac{m}{s}$. How fast does the top fall when the foot is 6 *m* from the wall? $x^{2} + y^{2} = 100 \Rightarrow 2 x x' + 2 y y' = 0 \Rightarrow y' = - \left( \frac{x}{y} \right) x'$. When $x = 6 ,\  y = 8$, so $y' = - \left( \frac{6}{8} \right) (2)$ = **$- \frac{1.5 m}{s}$** (the top slides down at 1.5 $\frac{m}{s}$).
:::

::: example Worked example: expanding circle
The radius of a circular oil slick grows at 3 cm/s. At $r = 10$ cm, $\dfrac{dA}{dt} = 2\pi r\,\dfrac{dr}{dt} = 2\pi (10)(3) = \mathbf{60\pi \approx 188.5\ \mathrm{cm^{2}/s}}$.
:::

```svgfig label="4.1" caption="A related-rates problem. A 10 *m* ladder leans on a wall; its foot is pulled away at 1 $\frac{m}{s}$. The distances satisfy $x^{2} + y^{2} = 100$, so differentiating with respect to time gives 2x·dx/dt + 2y·dy/dt = 0. When $x = 6 m$ we have $y = 8 m$, and the top slides down at 0.75 $\frac{m}{s}$."
f = Fig(740, 250)
f.line(60, 20, 60, 225, color=SLATE, sw=3); f.line(40, 225, 300, 225, color=SLATE, sw=3)
for k in range(0, 9): f.line(60, 40 + k * 22, 48, 52 + k * 22, color="#94a3b8", sw=1)
f.line(60, 65, 180, 225, color=NAVY, sw=5); f.poly([(180, 225), (170, 225), (180, 213)], fill=AMBER, stroke=AMBER)
f.circle(60, 65, 4, fill=RED, stroke=RED); f.circle(180, 225, 4, fill=RED, stroke=RED)
f.text(135, 130, "ladder 10 m", size=11, color=NAVY, bold=True, anchor="start"); f.text(38, 150, "y = 8 m", size=11, color=TEAL, bold=True, anchor="end"); f.text(120, 243, "x = 6 m", size=11, color=TEAL, bold=True)
f.arrow([(185, 238), (245, 238)], color=RED, sw=2, label="dx/dt = 1 m/s", lpos=(250, 242)); f.arrow([(75, 80), (75, 120)], color=RED, sw=2, label="dy/dt = ?", lpos=(80, 104))
steps = [("Relation", "x² + y² = 10²"), ("Differentiate w.r.t. time t", "2x (dx/dt) + 2y (dy/dt) = 0"), ("Solve", "dy/dt = −(x/y)(dx/dt)"), ("Substitute x = 6, y = 8, dx/dt = 1", "dy/dt = −(6/8)(1) = −0.75 m/s")]
for i, (s, e) in enumerate(steps):
    y = 20 + i * 58
    f.box(400, y, 330, 50, "", fill=BLUE if i % 2 == 0 else SOFT, stroke="#cbd5e1")
    f.text(412, y + 20, s, size=10.5, color=NAVY, bold=True, anchor="start"); f.text(412, y + 39, e, size=12, color=SLATE, anchor="start")
```

## 4.3 Increasing, decreasing, maxima and minima

- $f' (x) > 0$ on an interval ⇒ *f* increasing; $f' (x) < 0$ ⇒ decreasing.
- A **critical point** is where $f' (x) = 0$ or $f'$ does not exist. Local maxima and minima occur only at critical points.
- **First-derivative test**: $f'$ changes + to − ⇒ local max; − to + ⇒ local min; no change ⇒ neither.
- **Second-derivative test**: at $f' (c) = 0$, if $f'' (c) > 0$ then local min; $f'' (c) < 0$ ⇒ local max; $f'' (c) = 0$ ⇒ test fails.
- **Concavity**: $f'' > 0$ concave up (holds water); $f'' < 0$ concave down. A **point of inflection** is where concavity changes ($f'' = 0$ and changes sign).
- On a closed interval $[a ,\  b]$ the **absolute** extremes occur at critical points or the endpoints, so compare all candidates.

::: example Worked example: full analysis of a cubic
$f (x) = x^{3} - 6 x^{2} + 9 x + 1$. $f' = 3 x^{2} - 12 x + 9 = 3 (x - 1) (x - 3)$. $f'' = 6 x - 12$.

At $x = 1$: $f'' = - 6 < 0$, local **maximum**, $f (1) = 5$. At $x = 3$: $f'' = 6 > 0$, local **minimum**, $f (3) = 1$. Inflection at $f'' = 0 ,\  x = 2 ,\  f (2) = 3$. *f* is increasing on ($- \infty$, 1) and $(3 ,\  \infty)$, decreasing on (1, 3).

On [0, 4]: $f (0) = 1 ,\  f (1) = 5 ,\  f (3) = 1 ,\  f (4) = 5$. Absolute max 5 (at $x = 1$ and $x = 4$), absolute min 1 (at $x = 0$ and $x = 3$).
:::

## 4.4 Optimisation

Steps: (1) draw and name variables; (2) write the quantity to optimise; (3) use the constraint to reduce it to one variable; (4) find critical points and test; (5) answer the question asked, with units.

::: example Worked example: open box
From a 12 cm × 12 cm square, cut equal squares of side *x* from the corners and fold up an open box. $V = x (12 - 2 x)^{2}$ for $0 < x < 6$. $V' = (12 - 2 x)^{2} - 4 x (12 - 2 x) = (12 - 2 x) (12 - 6 x) = 0 \Rightarrow x = 2 ( x = 6$ gives $V = 0$). $V''$ at $x = 2$ is negative ($V'$ goes + to −), so maximum **$V = 2 \times 8^{2} = 128 \mathrm{cm}^{3}$**.
:::

::: example Worked example: fixed perimeter
A rectangle has perimeter 40 *m*. Width *w*, length $20 - w ;\  A = w (20 - w) ,\  A' = 20$ − 2w = $0 \Rightarrow w = 10 ,\  A'' = - 2 < 0$. Maximum area 100 $m^{2}$, a square.
:::

::: example Worked example: minimum cost can
A closed cylindrical can must hold 500 $\mathrm{cm}^{3}$. Minimise surface area $S = 2 \pi r^{2} + 2 \pi r h$ with $h = \frac{500}{(\pi r^{2})}$: $S = 2 \pi r^{2} + \frac{1000}{r}$. $S' = 4 \pi r - \frac{1000}{r^{2}} = 0 \Rightarrow r^{3} = \frac{250}{\pi} ,\  r \approx 4.30$ cm, *h* = 2r ≈ 8.60 cm. The best can has height equal to its diameter.
:::

```svgfig label="4.2" caption="Optimisation: the closed cylindrical can of volume 1000 $\mathrm{cm}^{3}$ with least material. With $h = \frac{1000}{(\pi r^{2})}$ the surface area is $S (r) = 2 \pi r^{2} + \frac{2000}{r}$. Setting $S' (r) = 4 \pi r - \frac{2000}{r^{2}} = 0$ gives $r = \left( \frac{500}{\pi} \right)^{\frac{1}{3}} \approx 5.42$ cm, *h* = 2r ≈ 10.84 cm and $S \approx 553.6 \mathrm{cm}^{2}$. Too thin a can (small *r*) or too wide a can (large *r*) wastes metal."
f = Fig(740, 270)
S = lambda r: 2 * math.pi * r * r + 2000 / r
a = Axes(f, 60, 14, 380, 220, (2, 10), (450, 1050)); a.grid(2, 100).axes("r (cm)", "S (cm²)")
a.curve(S, color=NAVY, sw=2.6); r0 = (500 / math.pi) ** (1 / 3)
a.pt(r0, S(r0), "minimum: r = 5.42 cm, S = 553.6 cm²", dx=10, dy=-14); a.vline(r0, 450, S(r0), color=AMBER)
for i, (r, c) in enumerate([(3.5, "thin: r = 3.5, h = 26.0, S = 648"), (r0, "best: r = 5.42, h = 10.84, S = 553.6"), (8.5, "wide: r = 8.5, h = 4.4, S = 689")]):
    y = 40 + i * 62
    h = 1000 / (math.pi * r * r); wpx = r * 6.5; hpx = min(h * 2.4, 56)
    cx = 500
    f.box(cx - wpx / 2 + 40, y + 56 - hpx, wpx, hpx, "", fill=MINT if i == 1 else SOFT, stroke=TEAL if i == 1 else SLATE)
    a1, a2 = c.split(", S = ")[0], "S = " + c.split(", S = ")[1] + " cm²"
    f.text(cx + 90, y + 24, a1, size=10, color=TEAL if i == 1 else SLATE, bold=(i == 1), anchor="start"); f.text(cx + 90, y + 40, a2, size=10, color=TEAL if i == 1 else SLATE, bold=(i == 1), anchor="start")
```

## 4.5 Mean value theorems

**Rolle's theorem.** If *f* is continuous on $[a ,\  b]$, differentiable on $(a ,\  b)$ and $f (a) = f (b)$, then $f' (c) = 0$ for some *c* in $(a ,\  b)$.

**Mean value theorem (MVT).** If *f* is continuous on $[a ,\  b]$ and differentiable on $(a ,\  b)$, there is *c* in $(a ,\  b)$ with **$f' (c) = \frac{f (b) - f (a)}{b - a}$**, a tangent parallel to the chord.

::: example Worked example
**Rolle:** $f (x) = x^{2} - 4 x + 3$ on [1, 3]: $f (1) = f (3) = 0 ;\  f' (x) = 2 x - 4 = 0$ at $c = 2$, inside the interval ✓.

**MVT:** $f (x) = x^{3}$ on [0, 2]: slope of chord $= \frac{8 - 0}{2} = 4$.

Set $f' (c) = 3 c^{2} = 4$, so $c = \frac{2}{\sqrt{3}} \approx 1.155$, which lies in $(0, 2)$ ✓.

**Use:** MVT proves that if $f' = 0$ on an interval then *f* is constant, and gives inequalities such as $|\sin a - \sin b| \le |a - b|$.
:::

```svgfig label="4.3" caption="Mean Value Theorem for $f (x) = x^{3}$ on [0, 2]. The secant through (0, 0) and (2, 8) has slope 4. Somewhere between, the tangent has the same slope: $f' (c) = 3 c^{2} = 4$ gives $c = \frac{2}{\sqrt{3}} \approx 1.155$. The tangent at c is parallel to the secant."
f = Fig(560, 270)
a = Axes(f, 40, 12, 490, 230, (-0.4, 2.5), (-1.5, 10)); a.grid(0.5, 2).axes()
a.curve(lambda x: x**3, color=NAVY, sw=2.6); a.curve(lambda x: 4 * x, -0.3, 2.4, color=AMBER, sw=1.8, dash=True)
c = 2 / math.sqrt(3); a.curve(lambda x: c**3 + 4 * (x - c), 0.2, 2.2, color=RED, sw=2.2)
a.pt(0, 0, "A(0, 0)", dx=12, dy=-16); a.pt(2, 8, "B(2, 8)", dx=-10, dy=-6, anchor="end"); a.pt(c, c**3, "c ≈ 1.155", color=RED, dx=10, dy=18)
f.text(a.X(0.06), a.Y(5.6), "secant AB: slope 4", size=10.5, color=AMBER, bold=True, anchor="start"); f.text(a.X(1.62), a.Y(0.95), "tangent at c: slope 4", size=10.5, color=RED, bold=True, anchor="start")
```

## 4.6 L'Hôpital's rule

If $\lim \frac{f}{g}$ gives **$\frac{0}{0}$ or $\frac{\infty}{\infty}$** and $\lim \frac{f'}{g'}$ exists (or is $\pm \infty$), then **$\lim \frac{f}{g} = \lim \frac{f'}{g'}$**. It can be applied repeatedly. Other forms $(0 \cdot \infty ,\  \infty - \infty ,\  1^{\infty} ,\  0^{0} ,\  \infty^{0})$ are first rewritten as a quotient, using ln for exponent forms.

::: example Worked example
**(a)** $\lim_{x \to 0} \frac{e^{x} - 1 - x}{x^{2}}$: $\frac{0}{0} \to \frac{e^{x} - 1}{2 x}$: $\frac{0}{0} \to \frac{e^{x}}{2}$ → **$\frac{1}{2}$**.

**(b)** $\lim_{x \to 0} \frac{\sin x - x}{x^{3}} \to \frac{\cos x - 1}{(3 x^{2})} \to \frac{- \sin x}{6 x} \to \frac{- \cos x}{6}$ → **$- \frac{1}{6}$**.

**(c)** $\lim_{x \to 0^{+}} x \ln x = \lim \frac{\ln x}{\frac{1}{x}} = \lim \frac{\frac{1}{x}}{- \frac{1}{x^{2}}} = \lim (- x)$ = **0**.

**(d)** $\lim_{x \to 0^{+}} x^{x}$: $\ln y = x \ln x \to 0$, so $y \to e^{0}$ = **1**.

**(e)** $\lim_{x \to \infty} \frac{\ln x}{x}$: $\frac{\infty}{\infty} \to \frac{1/x}{1}$ → **0**. A logarithm grows slower than any power.

**(f)** $\lim_{x \to \infty} (1 + \frac{1}{x})^{x}$ has the form $1^{\infty}$. Put $y = (1 + \frac{1}{x})^{x}$.

$\ln y = \frac{\ln(1 + 1/x)}{1/x}$: $\frac{0}{0} \to \frac{1}{1 + 1/x} \to 1$, so $y \to e^{1}$ = **e**.
:::

## 4.7 Taylor and Maclaurin series

If *f* has derivatives of all orders at a, its **Taylor series** is

$$f (x) = f (a) + f' (a) (x - a) + \frac{f'' (a) (x - a)^{2}}{2 !} + \frac{f''' (a) (x - a)^{3}}{3 !} + \ldots$$

With $a = 0$ it is the **Maclaurin series**. The first *n* terms form a polynomial approximation, the remainder is the error.

| Function | Maclaurin series | Valid for |
|---|---|---|
| $e^{x}$ | $1 + x + \frac{x^{2}}{2 !} + \frac{x^{3}}{3 !} + \ldots$ | all *x* |
| $\sin x$ | $x - \frac{x^{3}}{3 !} + \frac{x^{5}}{5 !} - \ldots$ | all *x* |
| $\cos x$ | $1 - \frac{x^{2}}{2 !} + \frac{x^{4}}{4 !} - \ldots$ | all *x* |
| $\ln (1 + x)$ | $x - \frac{x^{2}}{2} + \frac{x^{3}}{3} - \ldots$ | $- 1 < x \leq 1$ |
| $\frac{1}{1 - x}$ | $1 + x + x^{2} + x^{3} + \ldots$ | $|x| < 1$ |
| $(1 + x)^{n}$ | $1 + n x + \frac{n (n - 1) x^{2}}{2 !} + \ldots$ | $|x| < 1$ |

::: example Worked example: approximation
$\sin (0.1) \approx 0.1 - \frac{(0.1)^{3}}{6} = 0.1 - 0.000167$ = **0.099833** (true value 0.0998334). $\sqrt{1.02} = (1 + 0.02)^{\frac{1}{2}} \approx 1 + 0.01 - 0.00005$ = **1.00995**. Also $e^{0.2} \approx 1 + 0.2 + 0.02 + 0.001333 + 0.0000667 = 1.221400$ (true 1.221403).
:::

**Linear approximation (differentials).** $f (x + \Delta x) \approx f (x) + f' (x) \Delta x$. For ∛8.1: $f (x) = x^{\frac{1}{3}} ,\  f' (8) = \frac{1}{12}$, so ∛8.1 ≈ $2 + 0.1 / 12 = 2.00833$.

```photogrid label="4.1" cols="3" ratio="1.0" caption="Taylor and Maclaurin series. (a) Brook Taylor (1685-1731) published the general series in 1715; Colin Maclaurin made the case $x = 0$ famous. (b) The polynomials $P_{1} = x ,\  P_{3} = x - \frac{x^{3}}{6}$ and $P_{5} = x - \frac{x^{3}}{6} + \frac{x^{5}}{120}$ hug $\sin x$ near 0, and each extra term widens the match. (c) The same idea for $e^{x}$: the first terms $1 + x + \frac{x^{2}}{2}$ give $e^{0} . 1$ correct to three decimals."
@ photo id="bca104/taylor" cap="Brook Taylor, 1720"
fit 1.0
focus 0.5 0.7
@ svg cap="Maclaurin polynomials of sin x"
f = Fig(250, 250)
a = Axes(f, 28, 12, 205, 200, (-4.5, 4.5), (-2.5, 2.5)); a.grid(2, 1, size=8.5).axes("", "")
a.curve(math.sin, color=NAVY, sw=2.6)
a.curve(lambda x: x, color=AMBER, sw=1.4); a.curve(lambda x: x - x**3 / 6, color=TEAL, sw=1.4); a.curve(lambda x: x - x**3 / 6 + x**5 / 120, color=RED, sw=1.4)
f.text(125, 232, "navy sin x · amber P₁ · teal P₃ · red P₅", size=8.5, color=SLATE)
@ svg cap="Error of e^0.1 by Maclaurin terms"
f = Fig(250, 250)
vals = [("1", 1.0), ("1 + x", 1.1), ("+ x²/2", 1.105), ("+ x³/6", 1.105167)]
f.text(125, 22, "e^0.1 = 1.105171 (exact)", size=11, color=NAVY, bold=True)
for i, (t, v) in enumerate(vals):
    y = 40 + i * 48; err = abs(1.105171 - v)
    f.box(14, y, 92, 40, t, fill=BLUE, stroke=NAVY, color=NAVY, size=11, bold=True); f.box(112, y, 126, 40, "", fill=SOFT, stroke="#94a3b8")
    f.text(175, y + 18, f"{v:.6f}", size=11.5, color=NAVY, bold=True); f.text(175, y + 33, f"error {err:.6f}", size=8.5, color=RED)
```

## 4.8 Eight uses of the applications of derivatives

1. **Cheapest and strongest designs.** Engineers minimise material for a fixed volume, as in the can of Figure 4.2. A ghee or soft-drink company saves thousands of rupees of metal by using the best radius-to-height ratio. The same method is used for tanks, pipes and packaging.
2. **Maximum profit and revenue.** If the price per ticket falls, more people buy, so revenue is price × number and has a maximum. Setting the derivative to zero finds the best price. Cinema halls in Kathmandu and bus companies use the idea when setting fares.
3. **Related rates in construction and water supply.** The ladder problem (Figure 4.1) shows how one moving distance forces others to change. The same chain-rule thinking tells how fast the level in a tank rises while it is filled. It is needed for safe design of dams and reservoirs.
4. **Speeding cars and safety.** Speed is the derivative of position, and the Mean Value Theorem (Figure 4.3) guarantees that a car covering 120 km in 2 hours was going exactly 60 km/h at some moment. Highway cameras in some countries use average speed over a stretch for this reason. It is a simple proof from calculus.
5. **Curve sketching and graph reading.** The first derivative shows where a function rises, falls or turns, and the second shows how it bends. Data analysts use this to find peaks in sales, demand or website traffic. Software draws a good graph automatically in the same way.
6. **Finding roots with Newton's method.** To solve $f (x) = 0$ start from a guess $x_{0}$ and repeat $x_{1} = x_{0} - \frac{f (x_{0})}{f' (x_{0})}$. Each step uses the tangent line, and the sequence converges very fast. Calculators and computers find square roots this way.
7. **Indeterminate limits by L'Hôpital's rule.** When a limit is $\frac{0}{0}$ or $\frac{\infty}{\infty}$ we can differentiate the top and bottom separately. For example $\lim_{x \to 0} \frac{e^{x} - 1 - x}{x^{2}} = \frac{1}{2}$. This saves long algebra in examination problems and in algorithm analysis.
8. **Approximation by Taylor series.** Calculators compute $\sin x ,\  \cos x$ and $e^{x}$ by adding the first few terms of a Maclaurin series (Plate 4.1). The error is small because the terms shrink quickly. Without Taylor series, computers could not evaluate these functions at all.

```photogrid label="4.2" cols="2" ratio="1.2" caption="Optimisation with a number you can feel. (a) The aluminium top of a drinks can: the metal used for a can is a surface-area problem with a fixed volume. (b) For a 330 millilitre can the surface area is $S (r) = 2$ pi *r* squared + 2V / *r*. Setting the derivative to zero gives $r = ( \frac{V}{2}$ pi) to the one-third power = 3.74 centimetres and a height of exactly twice the radius, 7.49 centimetres, with surface 264.4 square centimetres; a numerical minimiser confirmed the result. A can of the common radius 3.3 centimetres has height 9.65 centimetres and surface 268.4, only 1.5 per cent more, because the curve is very flat near its minimum. Real cans are taller than the optimum for grip, stacking and printing, so the calculus answer is the cheapest, not always the best, design."
@ photo id="bcamath/can" cap="The top of a drinks can"
fit 1.2
focus 0.5 0.5
@ svg cap="330 mL can: surface area vs radius"
import math
from scipy.optimize import minimize_scalar
V = 330.0
S = lambda r: 2 * math.pi * r * r + 2 * V / r
res = minimize_scalar(S, bounds=(1, 10), method="bounded")
ropt = (V / (2 * math.pi)) ** (1 / 3)
assert abs(res.x - ropt) < 1e-3
hopt = V / (math.pi * ropt ** 2)
assert abs(hopt - 2 * ropt) < 1e-6
rreal = 3.3
hreal = V / (math.pi * rreal ** 2)
sav = 100 * (S(rreal) - S(ropt)) / S(rreal)
facts = dict(r=round(ropt, 2), h=round(hopt, 2), smin=round(S(ropt), 1), sreal=round(S(rreal), 1), hreal=round(hreal, 2), sav=round(sav, 1))
f = Fig(300, 246)
f.text(150, 12, "S(r) = 2 pi r^2 + 2V/r, V = 330 cm3", size=10.5, color=NAVY, bold=True)
x0, y0, W, H = 40, 160, 240, 110
X = lambda r: x0 + (r - 2) / 4 * W
Y = lambda s: y0 - (s - 250) / 150 * H
prev = None
for i in range(0, 101):
    r = 2 + i * 0.04
    p = (X(r), Y(min(S(r), 400)))
    if prev: f.line(prev[0], prev[1], p[0], p[1], color=NAVY, sw=2)
    prev = p
f.line(x0, y0, x0 + W, y0, color=SLATE)
for r in (2, 3, 4, 5, 6):
    f.text(X(r), y0 + 13, str(r), size=10.5, color=SLATE)
f.text(x0 + W / 2, y0 + 28, "radius r (cm)", size=10.5, color=SLATE)
f.circle(X(ropt), Y(S(ropt)), 5, fill="#bbf7d0", stroke=TEAL)
f.text(x0 + 6, 40, "min %.1f at r=%.2f" % (S(ropt), ropt), size=10.5, color=TEAL, bold=True, anchor="start")
f.circle(X(rreal), Y(S(rreal)), 5, fill="#fecaca", stroke=RED)
f.text(x0 + 6, 56, "real can r=3.3: %.1f" % S(rreal), size=10.5, color=RED, bold=True, anchor="start")
f.text(150, 222, "best can: h = 2r = %.2f cm" % hopt, size=10.5, color=NAVY, bold=True)
f.text(150, 238, "optimum is flat: only %.1f%% saving" % sav, size=10.5, color=SLATE)
```

## Formula and fact sheet

- Tangent at a: $y - f (a) = f' (a) (x - a)$; normal slope $- \frac{1}{f' (a)}$.
- Critical point: $f' = 0$ or undefined. $f'' > 0$ min, $f'' < 0$ max.
- MVT: $f' (c) = \frac{f (b) - f (a)}{b - a}$; Rolle is the case $f (a) = f (b)$.
- L'Hôpital: $\frac{0}{0}$ or $\frac{\infty}{\infty}$ → differentiate top and bottom separately.
- Maclaurin: $e^{x} ,\  \sin x ,\  \cos x ,\  \ln (1 + x) ,\  (1 + x)^{n}$ as in the table.
- Related rates: write the relation, differentiate with respect to *t*, substitute.

## Chapter summary

- The derivative gives tangents, rates, and the shape of a graph (increasing, decreasing, concave).
- Optimisation reduces a real problem to one variable and tests critical points and endpoints.
- Rolle and the MVT link the average slope to an instantaneous slope; L'Hôpital turns indeterminate limits into derivative quotients.
- Taylor series replace a function by polynomials and enable numerical approximation.

## Practice

1. Find the tangent and normal to $y = x^{2} - 3 x + 2$ at $x = 2$.
2. A balloon's radius grows at 2 cm/s. Find the rate at which its volume grows when $r = 5$ cm.
3. Find the local extrema and inflection point of $f (x) = 2 x^{3} - 9 x^{2} + 12 x$.
4. Find the dimensions of the rectangle of maximum area inscribed in a circle of radius R.
5. A farmer has 200 *m* of fence for a rectangular pen against a river wall (no fence along the river). Find the maximum area.
6. Verify the MVT for $f (x) = x^{2}$ on [1, 3].
7. Evaluate (a) $\lim_{x \to 0} \frac{e^{x} - e^{- x}}{\sin x}$, (b) $\lim_{x \to 0} \frac{\tan x - x}{x^{3}}$, (c) $\lim_{x \to 0} (\cos x)^{\frac{1}{x^{2}}}$.
8. Write the Maclaurin series of $\cos x$ up to $x^{4}$ and use it to estimate $\cos (0.2)$.
9. Use a linear approximation for $\sqrt{26}$.
10. Show that $x - \frac{x^{2}}{2} < \ln (1 + x) < x$ for $x > 0$.

::: note Answers and worked solutions
**1.** $y (2) = 0 ,\  y' = 2 x - 3 = 1$. Tangent $y = x - 2$; normal $y = - (x - 2) = 2 - x$.

**2.** $V = \left( \frac{4}{3} \right) \pi r^{3}$, $\dfrac{dV}{dt} = 4\pi r^{2}\,\dfrac{dr}{dt} = 4\pi \cdot 25 \cdot 2 = \mathbf{200\pi \approx 628.3\ \mathrm{cm^{3}/s}}$.

**3.** $f' = 6 x^{2} - 18 x + 12 = 6 (x - 1) (x - 2) ;\  f'' = 12 x - 18$. $x = 1$: $f'' = - 6$, **max** $f (1) = 5$. $x = 2$: $f'' = 6$, **min** $f (2) = 4$. Inflection at $x = 1.5 ,\  f (1.5) = 4.5$.

**4.** With sides *x* and $y ,\  x^{2} + y^{2} = 4 R^{2}$ and $A = x y$. Maximising $A^{2} = x^{2} (4 R^{2} - x^{2})$ gives $x^{2} = 2 R^{2}$, so $x = y = R \sqrt{2}$: a **square** of area $2 R^{2}$.

**5.** Width *w* (two sides), length 200 − 2w: $A = w ( 200$ − 2w), $A' = 200$ − 4w = $0 \Rightarrow w = 50$, length 100, **$A = 5000 m^{2}$**.

**6.** Chord slope ($9 - 1 ) / 2 = 4 ;\  f' (c) = 2 c = 4 \Rightarrow c = 2 \in ( 1$, 3) ✓.

**7.** (a) $\frac{0}{0} \to \frac{e^{x} + e^{- x}}{\cos x}$ → **2**. (b) → $\frac{\sec^{2} x - 1}{(3 x^{2})} = \frac{\tan^{2} x}{(3 x^{2})}$ → **$\frac{1}{3}$**. (c) $\ln y = \frac{\ln \cos x}{x^{2}} \to \frac{- \tan x}{2 x}$ → **$- \frac{1}{2}$**, so the limit is **$e^{- \frac{1}{2}}$**.

**8.** $\cos x \approx 1 - \frac{x^{2}}{2} + \frac{x^{4}}{24} ;\  \cos 0.2 \approx 1 - 0.02 + 0.0000667$ = **0.980067** (true 0.980067).

**9.** $f (x) = \sqrt{x}$ at 25: $f'$ = 1/(2·5) = $0.1 ;\  \sqrt{26} \approx 5 + 0.1$ = **5.1** (true 5.0990).

**10.** Let $g (x) = \ln (1 + x) - x + \frac{x^{2}}{2}$. $g (0) = 0$ and $g' = \frac{1}{1 + x} - 1 + x = \frac{x^{2}}{1 + x} > 0$, so $g > 0$ for $x > 0$. Let $h (x) = x - \ln (1 + x) ;\  h (0) = 0 ,\  h' = \frac{x}{1 + x} > 0$, so $h > 0$. ∎
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q (5 marks). Find the local maximum and minimum values of $f (x) = 2 x^{3} - 9 x^{2} + 12 x + 1$ and say where the function is increasing.**

A local extreme can occur only at a **critical point**, where $f' (x) = 0$ (or $f'$ does not exist). The **second derivative test** then decides: $f'' < 0$ gives a local maximum and $f'' > 0$ a local minimum.

1. Differentiate: $f' (x) = 6 x^{2} - 18 x + 12 = 6 (x^{2} - 3 x + 2) = 6 (x - 1) (x - 2)$.
2. Critical points: $f' = 0$ gives $x = 1$ and $x = 2$.
3. Second derivative: $f'' (x) = 12 x - 18$. At $x = 1 ,\  f'' = - 6 < 0$, so $x = 1$ is a **local maximum**. At $x = 2 ,\  f'' = 6 > 0$, so $x = 2$ is a **local minimum**.
4. Values: $f (1) = 2 - 9 + 12 + 1$ = **6** (maximum) and $f (2) = 16 - 36 + 24 + 1$ = **5** (minimum).
5. Sign of $f'$: positive for $x < 1$, negative for $1 < x < 2$, positive for $x > 2$.

| Interval | $x < 1$ | $1 < x < 2$ | $x > 2$ |
|---|---|---|---|
| $f' (x)$ | + | − | + |
| *f* | increasing | decreasing | increasing |

So *f* is increasing on ($- \infty$, 1) and $(2 ,\  \infty)$ and decreasing on (1, 2). The "maximum" 6 is only *local*: the cubic has no global maximum, because $f \to \infty$ as $x \to \infty$.

**Q (5 marks). Write the Maclaurin series of $e^{x}$ up to the term in $x^{4}$ and use it to estimate $e^{0} . 5$. Find the error.**

The **Maclaurin series** of *f* is $f (0) + f' (0) x + \frac{f'' (0) x^{2}}{2 !} + \frac{f''' (0) x^{3}}{3 !} + \ldots$, the Taylor series about 0 (Plate 4.1).

1. For $f (x) = e^{x}$ every derivative is $e^{x}$, so every derivative at 0 equals 1.
2. Therefore $e^{x} = 1 + x + \frac{x^{2}}{2 !} + \frac{x^{3}}{3 !} + \frac{x^{4}}{4 !} + \ldots$
3. Put $x = 0.5$: $1 + 0.5 + 0.125 + 0.5^{3} / 6 + 0.5^{4} / 24 = 1 + 0.5 + 0.125 + 0.020833 + 0.002604$.
4. The sum is **1.648438**.
5. The true value is $e^{0} . 5 = 1.648721$, so the error is about **0.00028**, less than the first omitted term $\frac{x^{5}}{5 !} = 0.000260$ (plus smaller ones).

*Conclusion:* four terms give three correct decimals. More terms give more accuracy, and for small $|x|$ the series converges very fast, which is how calculators evaluate $e^{x}$.

**Q (10 marks). State the Mean Value Theorem with its geometrical meaning and verify it for $f (x) = x^{3}$ on [0, 2]. Explain the steps of an optimisation problem with the example of a closed can of volume 1000 $\mathrm{cm}^{3}$, and state L'Hôpital's rule with an example.**

**Introduction.** The derivative tells how a function changes, so it can describe, estimate and optimise real systems. Three results of this unit are the Mean Value Theorem, optimisation and L'Hôpital's rule.

**Mean Value Theorem (MVT).** If *f* is continuous on $[a ,\  b]$ and differentiable on $(a ,\  b)$, there is at least one *c* in $(a ,\  b)$ with $f' (c) = \frac{f (b) - f (a)}{b - a}$. *Geometrically*, some tangent is parallel to the secant joining the end points (Figure 4.3). *Verification:* for $f (x) = x^{3}$ on [0, 2] the secant slope is $\frac{8 - 0}{2} = 4$. Solve $f' (c) = 3 c^{2} = 4$, so $c = \frac{2}{\sqrt{3}} \approx 1.155$, which lies in (0, 2). ✓ Rolle's theorem is the special case $f (a) = f (b)$, where $f' (c) = 0$.

**Optimisation steps (Figure 4.2).**
1. Draw a picture and name the variables (radius *r*, height *h*).
2. Write the quantity to optimise: $S = 2 \pi r^{2} + 2 \pi r h$.
3. Use the constraint $V = \pi r^{2} h = 1000$ to remove *h*: $S (r) = 2 \pi r^{2} + \frac{2000}{r}$.
4. Differentiate and solve $S' (r) = 4 \pi r - \frac{2000}{r^{2}} = 0$, giving $r^{3} = \frac{500}{\pi}$, so **$r \approx 5.42$ cm**.
5. Check it is a minimum: $S'' = 4 \pi + \frac{4000}{r^{3}} > 0$.
6. State the answer: $h = \frac{1000}{(\pi r^{2})} \approx 10.84$ cm = 2r, and S ≈ **553.6 $\mathrm{cm}^{2}$**. The best can has height equal to its diameter.

**L'Hôpital's rule.** If $\lim \frac{f}{g}$ has the form $\frac{0}{0}$ or $\frac{\infty}{\infty}$, then $\lim \frac{f}{g} = \lim \frac{f'}{g'}$ provided the latter exists. Example: $\lim_{x \to 0} \frac{x - \sin x}{x^{3}}$ is $\frac{0}{0}$; differentiating gives $\frac{1 - \cos x}{(3 x^{2})}$, still $\frac{0}{0}$; again gives $\frac{\sin x}{6 x}$ → **$\frac{1}{6}$**. Another: $\lim_{x \to \infty} \frac{\ln x}{x}$ is $\frac{\infty}{\infty}$ and equals $\lim \frac{\frac{1}{x}}{1} = 0$, so logarithms grow slower than any power.

**Comparison of the three tools.**

| Tool | Needs | Gives |
|---|---|---|
| MVT | continuity on $[a ,\  b]$, differentiable inside | a point where the slope equals the average slope |
| Optimisation | a function of one variable | the best $\left( \frac{\max}{\min} \right)$ value |
| L'Hôpital | an indeterminate form $\frac{0}{0}$ or $\frac{\infty}{\infty}$ | the value of the limit |

**Conclusion.** The derivative is a practical tool: it finds the cheapest can, proves facts about speed, and evaluates difficult limits. These three results are the standard long questions of this unit.
