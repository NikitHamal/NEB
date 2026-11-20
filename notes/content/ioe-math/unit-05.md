---
subject: Mathematics
grade: IOE
unit: 5
title: Calculus
hours: 8
area: Mathematics
---

Calculus is, with algebra, the heaviest block of the paper. The official booklet's model questions include a hyperbolic-inverse derivative and a first-order linear differential equation, so the syllabus is read broadly: standard limits, derivatives of inverse and hyperbolic functions, tangent / rate / extremum problems, a definite integral or an area, and a first-order differential equation. Speed comes from knowing the standard results cold.

::: key What the paper asks from this chapter
- Standard limits and L'Hôpital: $\frac{\sin x}{x}$, $\frac{1-\cos x}{x^2}$, $\frac{e^x-1}{x}$, $(1+x)^{1/x}$.
- Derivative table, including $\sin^{-1},\tan^{-1}$, $\sinh^{-1},\cosh^{-1},\tanh^{-1},\mathrm{sech}^{-1}$; parametric and implicit forms.
- Tangent and normal, related rates, maxima and minima (second-derivative test).
- Integrals: substitution, by parts, $\int e^x(f+f')dx$, Wallis, the property $\int_0^af(x)dx=\int_0^af(a-x)dx$.
- Area under a curve and between two curves.
- Differential equations: order, degree, separable, homogeneous, linear (integrating factor), exact.
:::

## 5.1 Limit and continuity of functions, indeterminate forms, L'Hospital's rule

$\lim_{x\to a}f(x)=L$ exists iff the left and right limits both equal $L$. $f$ is **continuous** at $a$ if $\lim_{x\to a}f(x)=f(a)$. Polynomials, $e^x$, $\sin x$ are continuous everywhere; rational functions except at zeros of the denominator.

| Standard limit ($x\to0$) | Value |
|---|---|
| $\dfrac{\sin x}{x},\ \dfrac{\tan x}{x},\ \dfrac{\sin^{-1}x}{x},\ \dfrac{\tan^{-1}x}{x}$ | 1 |
| $\dfrac{1-\cos x}{x^2}$ | $\frac{1}{2}$ |
| $\dfrac{e^x-1}{x},\ \dfrac{\ln(1+x)}{x}$ | 1 |
| $\dfrac{a^x-1}{x}$ | $\ln a$ |
| $\dfrac{(1+x)^n-1}{x}$ | $n$ |
| $(1+x)^{1/x}$, and $\big(1+\frac{1}{x}\big)^x$ as $x\to\infty$ | $e$ |
| $\dfrac{x^n-a^n}{x-a}$ ($x\to a$) | $na^{n-1}$ |

**Indeterminate forms:** $\frac{0}{0},\frac{\infty}{\infty},0\cdot\infty,\infty-\infty,1^\infty,0^0,\infty^0$. **L'Hôpital:** for $\frac{0}{0}$ or $\frac{\infty}{\infty}$, $\lim\frac{f}{g}=\lim\frac{f'}{g'}$ (repeat if still indeterminate). Convert $0\cdot\infty$ to a quotient, $\infty-\infty$ to a single fraction, and take logarithms for $1^\infty,0^0,\infty^0$. Example: $\lim_{x\to0}\frac{\tan x-\sin x}{x^3}=\lim\frac{\tan x(1-\cos x)}{x^3}=\frac{1}{2}$. As $x\to\infty$ the highest power of a rational function decides the limit.

::: caution
L'Hôpital applies only to $\frac{0}{0}$ or $\frac{\infty}{\infty}$ forms. Using it on $\frac{\sin x}{x}$ as $x\to\infty$ is wrong (the limit is 0 by the squeeze theorem). For continuity of a piecewise function, set the left limit, the right limit and the value equal — and solve for the unknown constant.
:::

## 5.2 Derivatives, rules, applications

**Rules:** sum, product $(uv)'=u'v+uv'$, quotient $\big(\frac{u}{v}\big)'=\frac{u'v-uv'}{v^2}$, chain $\frac{dy}{dx}=\frac{dy}{du}\frac{du}{dx}$; parametric $\frac{dy}{dx}=\frac{dy/dt}{dx/dt}$; implicit: differentiate both sides; logarithmic differentiation for $x^x$, $u^v$: $\frac{d}{dx}x^x=x^x(1+\ln x)$.

| $f(x)$ | $f'(x)$ | $f(x)$ | $f'(x)$ |
|---|---|---|---|
| $x^n$ | $nx^{n-1}$ | $\sin^{-1}x$ | $\frac{1}{\sqrt{1-x^2}}$ |
| $e^x$, $a^x$ | $e^x$, $a^x\ln a$ | $\tan^{-1}x$ | $\frac{1}{1+x^2}$ |
| $\ln x$, $\log_ax$ | $\frac{1}{x}$, $\frac{1}{x\ln a}$ | $\sec^{-1}x$ | $\frac{1}{|x|\sqrt{x^2-1}}$ |
| $\sin x$, $\cos x$ | $\cos x$, $-\sin x$ | $\sinh x$, $\cosh x$ | $\cosh x$, $\sinh x$ |
| $\tan x$, $\cot x$ | $\sec^2x$, $-\csc^2x$ | $\tanh x$ | $\mathrm{sech}^2x$ |
| $\sec x$, $\csc x$ | $\sec x\tan x$, $-\csc x\cot x$ | $\sinh^{-1}x$ | $\frac{1}{\sqrt{x^2+1}}$ |
| $\ln(\sec x+\tan x)$ | $\sec x$ | $\cosh^{-1}x$ ($x>1$) | $\frac{1}{\sqrt{x^2-1}}$ |
| $\sqrt{x}$ | $\frac{1}{2\sqrt{x}}$ | $\tanh^{-1}x$ ($|x|<1$) | $\frac{1}{1-x^2}$ |
| | | $\mathrm{sech}^{-1}x$ ($0<x<1$) | $\frac{-1}{x\sqrt{1-x^2}}$ |

Hyperbolic: $\sinh x=\frac{e^x-e^{-x}}{2}$, $\cosh x=\frac{e^x+e^{-x}}{2}$, $\cosh^2x-\sinh^2x=1$; $\sinh^{-1}x=\ln(x+\sqrt{x^2+1})$, $\cosh^{-1}x=\ln(x+\sqrt{x^2-1})$, $\tanh^{-1}x=\frac{1}{2}\ln\frac{1+x}{1-x}$. The derivative of $\mathrm{sech}^{-1}x=\cosh^{-1}(1/x)$ exists only inside its domain $0<x<1$ — the reason the booklet's model answer is "$x<1$".

**Higher derivatives** and Leibniz: $\frac{d^n}{dx^n}e^{ax}=a^ne^{ax}$, $\frac{d^n}{dx^n}\sin x=\sin(x+\frac{n\pi}{2})$. **Rolle** (continuous on $[a,b]$, differentiable inside, $f(a)=f(b)$ gives $f'(c)=0$) and **Mean value theorem** $f'(c)=\frac{f(b)-f(a)}{b-a}$.

### Applications

- **Tangent** at $(x_1,y_1)$: slope $f'(x_1)$; **normal** slope $-\frac{1}{f'(x_1)}$. A horizontal tangent has $f'=0$.
- **Rate of change:** differentiate the relation with respect to time. Sphere: $V=\frac{4}{3}\pi r^3\Rightarrow\frac{dV}{dt}=4\pi r^2\frac{dr}{dt}$. Ladder: $x^2+y^2=L^2\Rightarrow x\dot x+y\dot y=0$.
- **Maxima and minima.** Critical points: $f'(x)=0$. Second-derivative test: $f''<0$ local max, $f''>0$ local min. For a closed interval compare the critical values with the endpoint values. $x^2-4x+7$ has minimum $3$ at $x=2$. Given perimeter or sum, a rectangle / product is maximal when the parts are equal.
- Increasing where $f'>0$, decreasing where $f'<0$; concave up where $f''>0$; a point of inflection where $f''$ changes sign.

## 5.3 Integration, definite integral, area

**Standard integrals** ($+C$ omitted): $\int x^n=\frac{x^{n+1}}{n+1}$ ($n\ne-1$), $\int\frac{1}{x}=\ln|x|$, $\int e^{ax}=\frac{e^{ax}}{a}$, $\int a^x=\frac{a^x}{\ln a}$, $\int\sin=-\cos$, $\int\cos=\sin$, $\int\sec^2=\tan$, $\int\csc^2=-\cot$, $\int\sec\tan=\sec$, $\int\tan x=\ln|\sec x|$, $\int\sec x=\ln|\sec x+\tan x|$.
$$\int\frac{dx}{x^2+a^2}=\frac{1}{a}\tan^{-1}\frac{x}{a},\qquad \int\frac{dx}{\sqrt{a^2-x^2}}=\sin^{-1}\frac{x}{a}.$$
$$\int\frac{dx}{x^2-a^2}=\frac{1}{2a}\ln\Big|\frac{x-a}{x+a}\Big|,\qquad \int\frac{dx}{\sqrt{x^2\pm a^2}}=\ln\big|x+\sqrt{x^2\pm a^2}\big|.$$
$\int\sqrt{a^2-x^2}\,dx=\frac{x}{2}\sqrt{a^2-x^2}+\frac{a^2}{2}\sin^{-1}\frac{x}{a}$. $\int\frac{f'(x)}{f(x)}dx=\ln|f|$.

**Methods.** *Substitution* ($\int\frac{x}{x^2+1}dx=\frac{1}{2}\ln(x^2+1)$). *By parts* $\int uv'=uv-\int u'v$, with $u$ chosen by ILATE (Inverse, Log, Algebraic, Trig, Exponential): $\int xe^xdx=xe^x-e^x$; $\int\ln x\,dx=x\ln x-x$. *Special:* $\int e^x[f(x)+f'(x)]dx=e^xf(x)$. *Partial fractions* for rational functions.

**Definite integral.** $\int_a^bf=F(b)-F(a)$. Properties: $\int_a^bf(x)dx=\int_a^bf(a+b-x)dx$; $\int_{-a}^af=2\int_0^af$ if $f$ even, $0$ if odd; $\int_0^{\pi/2}\frac{\sin x}{\sin x+\cos x}dx=\frac{\pi}{4}$ (also with $\sin^n,\cos^n$); Wallis: $\int_0^{\pi/2}\sin^nx\,dx=\frac{n-1}{n}\cdot\frac{n-3}{n-2}\cdots$ (times $\frac{\pi}{2}$ if $n$ even). $\int_0^{\pi/2}\sin^2x\,dx=\frac{\pi}{4}$.

**Area.** Under $y=f(x)$ from $a$ to $b$: $\int_a^b|f|\,dx$; between curves: $\int_a^b(f-g)\,dx$ where $f\ge g$; with respect to $y$: $\int x\,dy$. Circle area $\pi r^2$, area of an ellipse $\pi ab$. Area between $y^2=4ax$ and $x^2=4ay$: $\frac{16a^2}{3}$. Intersect the curves first to find the limits.

## 5.4 Differential equations

**Order** = highest derivative present; **degree** = its power after removing radicals and fractions of derivatives. $\big(\frac{d^2y}{dx^2}\big)^3+\big(\frac{dy}{dx}\big)^4+y=0$ has order 2, degree 3.

| Type | Form | Method |
|---|---|---|
| separable | $\frac{dy}{dx}=f(x)g(y)$ | $\int\frac{dy}{g}=\int f\,dx$ |
| homogeneous | $\frac{dy}{dx}=F\big(\frac{y}{x}\big)$ | put $y=vx$ |
| linear | $\frac{dy}{dx}+Py=Q$ | IF $=e^{\int P\,dx}$; $y\cdot\text{IF}=\int Q\cdot\text{IF}\,dx$ |
| exact | $M\,dx+N\,dy=0$, $\frac{\partial M}{\partial y}=\frac{\partial N}{\partial x}$ | $\int M\,dx$ (y const) + terms of $N$ free of $x$ $=C$ |

If $M\,dx+N\,dy=0$ is not exact, try an integrating factor: $e^{\int\frac{M_y-N_x}{N}dx}$ when that depends only on $x$. Examples: $\frac{dy}{dx}+\frac{2}{x}y=x^2$ has IF $x^2$; $\frac{dy}{dx}+y=e^{-x}$ gives $y=(x+C)e^{-x}$. The number of arbitrary constants in the general solution equals the order.

```photogrid label="5.1" cols="2" ratio="1.2" caption="A limit as a squeeze. (a) Archimedes trapped the circle between regular polygons drawn inside and outside it. (b) For a circle of diameter 1, the inscribed n-gon has perimeter n sin(pi/n) and the circumscribed one n tan(pi/n). For n = 6, 12, 24, 48, 96 the bounds close in from 3.0000 and 3.4641 to 3.1410 and 3.1427, so pi lies between them, and the 96-gon gives Archimedes own bounds 223/71 = 3.1408 and 22/7 = 3.1429. The lower bound is pi times sin(x)/x at x = pi/n, so the limit of sin(x)/x = 1 as x tends to 0 is exactly why the bounds converge to pi."
@ photo id="ioemath/archpoly" cap="Archimedes: polygons inside and outside a circle"
fit 1.2
focus 0.5 0.5
@ svg cap="Perimeter bounds for pi from n = 6 to 96 sides"
import math
ns = [6, 12, 24, 48, 96]
lo = [n * math.sin(math.pi / n) for n in ns]; up = [n * math.tan(math.pi / n) for n in ns]
assert all(a < math.pi < b for a, b in zip(lo, up)) and lo == sorted(lo) and up == sorted(up, reverse=True)
assert 223 / 71 < lo[-1] and up[-1] < 22 / 7
assert abs(lo[-1] - math.pi * math.sin(math.pi / 96) / (math.pi / 96)) < 1e-12
facts = dict(l6="%.4f" % lo[0], u6="%.4f" % up[0], l96="%.4f" % lo[-1], u96="%.4f" % up[-1], a71="%.4f" % (223 / 71), a7="%.4f" % (22 / 7))
f = Fig(300, 236)
f.text(150, 14, "bounds on pi squeeze together as n grows", size=10.5, color=NAVY, bold=True)
Y = lambda v: 30 + (3.5 - v) / (3.5 - 2.95) * 120
X = lambda i: 50 + i * 54
f.line(40, Y(math.pi), 285, Y(math.pi), color=RED, sw=1.4, dash=True); f.text(284, Y(math.pi) - 6, "pi = 3.1416", size=10.5, color=RED, bold=True, anchor="end")
for i in range(5):
    f.circle(X(i), Y(up[i]), 4, fill=AMBER, stroke=AMBER); f.circle(X(i), Y(lo[i]), 4, fill=TEAL, stroke=TEAL)
    f.text(X(i), 166, str(ns[i]), size=10.5, color=NAVY, bold=True)
    if i: f.line(X(i - 1), Y(up[i - 1]), X(i), Y(up[i]), color=AMBER, sw=1.4); f.line(X(i - 1), Y(lo[i - 1]), X(i), Y(lo[i]), color=TEAL, sw=1.4)
f.text(X(0) + 6, Y(up[0]) - 8, "%.4f" % up[0], size=10.5, color=AMBER, bold=True, anchor="start"); f.text(X(0) + 6, Y(lo[0]) + 16, "%.4f" % lo[0], size=10.5, color=TEAL, bold=True, anchor="start")
f.text(150, 182, "n = number of sides", size=10.5, color=SLATE)
f.text(150, 200, "n = 96:  %.4f < pi < %.4f" % (lo[-1], up[-1]), size=10.5, color=NAVY, bold=True)
f.text(150, 217, "amber: n tan(pi/n)   teal: n sin(pi/n)", size=10.5, color=SLATE)
```

```photogrid label="5.2" cols="2" ratio="1.2" caption="The derivative is a limit of average speeds. (a) A speedometer reports the speed at one instant, which no stopwatch can measure directly. (b) A car has distance s(t) = 0.8 t^2 + 2t metres. Its average speed from t = 5 s over a gap h is 11.60 m/s for h = 2, 10.80 for h = 1, 10.08 for h = 0.1 and 10.008 for h = 0.01. These approach 10 m/s, which is ds/dt = 1.6 t + 2 at t = 5, or 36 km/h. The dashed secant tilts towards the solid tangent as h shrinks. The distance formula is an assumed model, not data from the photo."
@ photo id="ioemath/speedo" cap="A speedometer shows the derivative of distance at this instant"
fit 1.2
focus 0.5 0.5
@ svg cap="Difference quotients of s = 0.8 t^2 + 2 t at t = 5"
s = lambda t: 0.8 * t * t + 2 * t
dq = lambda h: (s(5 + h) - s(5)) / h
v = 1.6 * 5 + 2
assert abs(dq(1e-6) - v) < 1e-4 and abs(dq(2) - 11.6) < 1e-9 and abs(v * 3.6 - 36) < 1e-9
facts = dict(q1="%.2f" % dq(2), q2="%.2f" % dq(1), q3="%.2f" % dq(0.1), q4="%.3f" % dq(0.01), v="%d" % v, kmh="%d" % (v * 3.6))
f = Fig(300, 236)
f.text(150, 14, "s(t) = 0.8 t^2 + 2 t   (metres)", size=10.5, color=NAVY, bold=True)
X = lambda t: 34 + t * 30; Y = lambda d: 150 - d * 1.6
f.line(30, Y(0), 285, Y(0), color=SOFT, sw=1.2); f.line(34, 150, 34, 28, color=SOFT, sw=1.2)
pts = [(t / 10, s(t / 10)) for t in range(0, 81)]
for (a, b), (c, d) in zip(pts, pts[1:]): f.line(X(a), Y(b), X(c), Y(d), color=NAVY, sw=2.4)
tan = lambda t: s(5) + v * (t - 5)
f.line(X(2.5), Y(tan(2.5)), X(7.6), Y(tan(7.6)), color=RED, sw=1.6)
sec = lambda t: s(5) + dq(3) * (t - 5)
f.line(X(3), Y(sec(3)), X(8), Y(sec(8)), color=AMBER, sw=1.4, dash=True)
f.circle(X(5), Y(s(5)), 4, fill=RED, stroke=RED); f.circle(X(8), Y(s(8)), 3.5, fill=AMBER, stroke=AMBER)
f.text(X(5) + 8, Y(s(5)) + 16, "t = 5", size=10.5, color=RED, bold=True, anchor="start")
for k, t in enumerate((0, 2, 4, 6, 8)): f.text(X(t), 162, str(t), size=10.5, color=SLATE)
f.text(150, 174, "t (s)", size=10.5, color=SLATE)
f.box(10, 182, 280, 20, "", fill=BLUE, stroke=NAVY, r=3)
for x, hh in zip((20, 78, 136, 200, 246), ("h = 2", "1", "0.1", "0.01", "to 0")): f.text(x, 192, hh, size=10.5, color=NAVY, bold=True, anchor="start", vmid=True)
for x, val in zip((20, 78, 136, 200), (dq(2), dq(1), dq(0.1), dq(0.01))): f.text(x, 214, ("%.3f" if val < 10.05 and val != 11.6 and abs(val-10)<0.01 else "%.2f") % val, size=10.5, color=TEAL, bold=True, anchor="start", vmid=True)
f.text(246, 214, "10 m/s", size=10.5, color=RED, bold=True, anchor="start", vmid=True)
```

```photogrid label="5.3" cols="2" ratio="1.2" caption="Related rates. (a) A ladder leaning on a wall. If its foot moves away, the top comes down, and the two speeds are linked by x^2 + y^2 = L^2. (b) For L = 5 m and a foot moving out at 0.5 m/s, differentiating gives y dy/dt = -x dx/dt, so dy/dt = -(x / y)(0.5). At x = 3 m the top is 4 m high and falls at 0.375 m/s; at x = 4.5 m it falls at 1.032 m/s and at x = 4.9 m at 2.462 m/s. The fall speeds up without limit as x tends to 5 m, and each value is confirmed by a small finite difference."
@ photo id="ioemath/ladder" cap="A ladder leaning on a wall: the top slides down as the foot moves out"
fit 1.2
focus 0.5 0.5
@ svg cap="Ladder of 5 m: top speed at five foot positions"
import math
L, vx = 5.0, 0.5
y = lambda x: math.sqrt(L * L - x * x)
rate = lambda x: -x / y(x) * vx
fd = lambda x: (y(x + vx * 1e-6) - y(x)) / 1e-6
for x in (1, 3, 4, 4.5, 4.9): assert abs(rate(x) - fd(x)) < 1e-4 * max(1, abs(rate(x)))
assert abs(rate(3) + 0.375) < 1e-12
facts = dict(r3="%.3f" % abs(rate(3)), r45="%.3f" % abs(rate(4.5)), r49="%.3f" % abs(rate(4.9)))
f = Fig(300, 236)
f.text(150, 14, "ladder L = 5 m, foot speed 0.5 m/s", size=10.5, color=NAVY, bold=True)
sc = 22; ox, oy = 40, 138
f.line(ox, 26, ox, oy, color=SLATE, sw=3); f.line(ox, oy, 280, oy, color=SLATE, sw=3)
for x, col in ((1.5, SOFT), (3, RED), (4.5, AMBER)):
    f.line(ox, oy - y(x) * sc, ox + x * sc, oy, color=col if col != SOFT else "#94a3b8", sw=2.4 if x == 3 else 1.6, dash=(x != 3))
f.text(ox + 52, oy - 4 * sc + 4, "y = 4", size=10.5, color=RED, bold=True, anchor="start")
f.text(ox + 3 * sc / 2 + 22, oy + 14, "x = 3", size=10.5, color=RED, bold=True)
f.box(10, 160, 280, 20, "", fill=BLUE, stroke=NAVY, r=3)
xs = (1, 3, 4, 4.5, 4.9)
for i, x in enumerate(xs):
    f.text(14 + i * 56, 170, "x = %g" % x, size=10.5, color=NAVY, bold=True, anchor="start", vmid=True)
    f.text(14 + i * 56, 194, "%.3f" % rate(x), size=10.5, color=RED if x == 3 else TEAL, bold=True, anchor="start", vmid=True)
f.text(150, 214, "dy/dt in m/s: negative = top moving down", size=10.5, color=SLATE)
```

```photogrid label="5.4" cols="2" ratio="1.2" caption="Area as a limit of sums. (a) A planimeter measures the area inside a traced outline, which is a mechanical definite integral. (b) The area under y = x^2 from 0 to 3 is cut into n strips. With n = 6 the left-hand sum is 6.875 and the trapezoid sum 9.125; with n = 96 they are 8.860 and 9.000. The exact value is the integral of x^2 from 0 to 3, which is 3^3 / 3 = 9. The left sum is 23.6 per cent low at n = 6, while the trapezoid error is smaller and falls four times each time n is doubled."
@ photo id="bca204/planimeter" cap="A planimeter: a mechanical integrator that measures area"
fit 1.2
focus 0.5 0.5
@ svg cap="Left sums and trapezoids for the area under y = x^2"
f_ = lambda x: x * x
def left(n): h = 3 / n; return sum(f_(i * h) for i in range(n)) * h
def trap(n): h = 3 / n; return (f_(0) / 2 + sum(f_(i * h) for i in range(1, n)) + f_(3) / 2) * h
assert abs(trap(96) - 9) < 0.002 and abs(left(6) - 6.875) < 1e-9
assert abs((trap(12) - 9) / (trap(6) - 9) - 0.25) < 1e-9
facts = dict(l6="%.3f" % left(6), t6="%.3f" % trap(6), l96="%.3f" % left(96), t96="%.3f" % trap(96), el6="%.1f" % ((9 - left(6)) / 9 * 100))
f = Fig(300, 236)
f.text(150, 14, "area under y = x^2 on [0, 3], exact = 9", size=10.5, color=NAVY, bold=True)
X = lambda x: 40 + x * 76; Y = lambda y: 134 - y * 11
n = 6; h = 3 / n
for i in range(n): f.box(X(i * h), Y(f_(i * h)), X(h) - X(0), Y(0) - Y(f_(i * h)), "", fill=SAND, stroke=AMBER, r=0, sw=1)
pts = [(i / 30, f_(i / 30)) for i in range(0, 91)]
for (a, b), (c, d) in zip(pts, pts[1:]): f.line(X(a), Y(b), X(c), Y(d), color=NAVY, sw=2.4)
f.line(30, Y(0), 276, Y(0), color=SLATE, sw=1.4)
for x in range(4): f.text(X(x), 148, str(x), size=10.5, color=SLATE)
f.box(10, 160, 280, 20, "", fill=BLUE, stroke=NAVY, r=3)
for x, hh in zip((14, 66, 130, 200), ("n", "left sum", "trapezoid", "error of trap.")): f.text(x, 170, hh, size=10.5, color=NAVY, bold=True, anchor="start", vmid=True)
for k, nn in enumerate((6, 24, 96)):
    y = 192 + k * 15
    f.text(14, y, str(nn), size=10.5, color=SLATE, bold=True, anchor="start", vmid=True)
    f.text(66, y, "%.3f" % left(nn), size=10.5, color=AMBER, bold=True, anchor="start", vmid=True)
    f.text(130, y, "%.4f" % trap(nn), size=10.5, color=TEAL, bold=True, anchor="start", vmid=True)
    f.text(200, y, "%.5f" % (trap(nn) - 9), size=10.5, color=RED, bold=True, anchor="start", vmid=True)
```

```photogrid label="5.5" cols="2" ratio="1.2" caption="A differential equation from cooling. (a) A hot drink loses heat faster when it is much hotter than the room. (b) Newton law of cooling says dT/dt = -k (T - Ta). Separating variables and integrating gives T = Ta + (T0 - Ta) e^(-kt). Take assumed readings Ta = 25, T0 = 90 and T = 70 after 10 minutes. Then k = ln(65/45) / 10 = 0.0368 per minute, and the drink reaches 60 degrees at t = 16.8 minutes. Euler steps of 5 minutes give 68.3 degrees at t = 10 and steps of 1 minute give 69.7, against the exact 70, so smaller steps follow the true solution."
@ photo id="bca104/coffee" cap="A hot drink cools towards room temperature"
fit 1.2
focus 0.5 0.5
@ svg cap="Cooling curve: exact solution and Euler steps"
import math
Ta, T0 = 25.0, 90.0
k = math.log(65 / 45) / 10
T = lambda t: Ta + (T0 - Ta) * math.exp(-k * t)
t60 = math.log(65 / 35) / k
def euler(h, tend):
    t, x = 0.0, T0
    while t < tend - 1e-9: x += h * (-k * (x - Ta)); t += h
    return x
assert abs(T(10) - 70) < 1e-9 and abs(T(t60) - 60) < 1e-9
assert abs(euler(1, 10) - 70) < abs(euler(5, 10) - 70)
facts = dict(k="%.4f" % k, t60="%.1f" % t60, e5="%.1f" % euler(5, 10), e1="%.1f" % euler(1, 10))
f = Fig(300, 236)
f.text(150, 14, "T(t) = 25 + 65 e^(-kt), k = %.4f per min" % k, size=10.5, color=NAVY, bold=True)
X = lambda t: 40 + t * 7.4; Y = lambda v: 160 - (v - 20) * 1.7
f.line(36, Y(20), 280, Y(20), color=SOFT, sw=1.2); f.line(X(0), 160, X(0), 28, color=SOFT, sw=1.2)
f.line(X(0), Y(Ta), 280, Y(Ta), color="#94a3b8", sw=1.2, dash=True); f.text(278, Y(Ta) - 6, "room 25", size=10.5, color=SLATE, bold=True, anchor="end")
pts = [(t / 2, T(t / 2)) for t in range(0, 61)]
for (a, b), (c, d) in zip(pts, pts[1:]): f.line(X(a), Y(b), X(c), Y(d), color=NAVY, sw=2.4)
for h, col in ((5, AMBER), (1, TEAL)):
    t, x = 0.0, T0
    while t < 30 - 1e-9:
        x2 = x + h * (-k * (x - Ta)); f.line(X(t), Y(x), X(t + h), Y(x2), color=col, sw=1.4, dash=(h == 5)); t += h; x = x2
f.circle(X(10), Y(70), 4, fill=RED, stroke=RED); f.text(X(10) + 8, Y(70) - 6, "70 at 10 min", size=10.5, color=RED, bold=True, anchor="start")
for t in (0, 10, 20, 30): f.text(X(t), 174, str(t), size=10.5, color=SLATE)
f.text(150, 188, "t (minutes)", size=10.5, color=SLATE)
f.text(150, 204, "navy exact, amber dashed Euler h = 5, teal Euler h = 1", size=10.5, color=SLATE)
f.text(150, 220, "Euler at t = 10: %.1f (h=5), %.1f (h=1), exact 70" % (euler(5, 10), euler(1, 10)), size=10.5, color=TEAL, bold=True)
```

## Formula and fact sheet

| Topic | Result |
|---|---|
| $\lim\frac{\sin x}{x}$, $\lim\frac{1-\cos x}{x^2}$ | $1$, $\frac{1}{2}$ |
| $\lim(1+x)^{1/x}$ | $e$ |
| $\frac{d}{dx}\sinh^{-1}x$ | $\frac{1}{\sqrt{x^2+1}}$ |
| normal slope | $-1/f'$ |
| $\int e^x(f+f')$ | $e^xf$ |
| $\int\frac{dx}{a^2+x^2}$ | $\frac{1}{a}\tan^{-1}\frac{x}{a}$ |
| area between curves | $\int(f-g)\,dx$ |
| linear ODE IF | $e^{\int P\,dx}$ |

## Chapter summary

- Standard limits plus L'Hôpital settle every limit; check the form before using L'Hôpital.
- Chain rule, parametric and logarithmic differentiation cover all derivative types.
- Critical points from $f'=0$; the sign of $f''$ decides max or min; compare endpoints on closed intervals.
- Integrate by substitution, by parts (ILATE) or by the $e^x(f+f')$ pattern; use symmetry for definite integrals.
- Areas: find the intersections, then integrate top minus bottom.
- Classify a first-order equation (separable, homogeneous, linear, exact) before solving.

## Practice questions

**Set A — Recall (14 questions)**

1. The value of $\lim_{x\to0}\dfrac{\sin3x}{x}$ is
   (a) 1 (b) 3 (c) $1/3$ (d) 0
2. The value of $\lim_{x\to0}(1+2x)^{1/x}$ is
   (a) $e$ (b) $2e$ (c) $e^2$ (d) 1
3. $\dfrac{d}{dx}\tan^{-1}x$ equals
   (a) $\dfrac{1}{1+x^2}$ (b) $\dfrac{1}{\sqrt{1-x^2}}$ (c) $-\dfrac{1}{1+x^2}$ (d) $\sec^2x$
4. $\displaystyle\int e^{2x}dx$ equals
   (a) $2e^{2x}+C$ (b) $e^{2x}+C$ (c) $\dfrac{e^x}{2}+C$ (d) $\dfrac{e^{2x}}{2}+C$
5. The value of $\displaystyle\int_0^{\pi}\sin x\,dx$ is
   (a) 2 (b) 0 (c) 1 (d) $\pi$
6. The order and degree of $\big(\frac{d^2y}{dx^2}\big)^3+\big(\frac{dy}{dx}\big)^4+y=0$ are
   (a) 3, 2 (b) 2, 3 (c) 2, 1 (d) 3, 3
7. The general solution of $\dfrac{dy}{dx}=y$ is
   (a) $y=Cx$ (b) $y=x+C$ (c) $y=Ce^x$ (d) $y=C\ln x$
8. The integrating factor of $\dfrac{dy}{dx}+\dfrac{2}{x}y=x^2$ is
   (a) $2x$ (b) $e^{2x}$ (c) $\ln x^2$ (d) $x^2$
9. $\dfrac{d}{dx}\big(e^x\sin x\big)$ equals
   (a) $e^x\cos x$ (b) $e^x(\sin x+\cos x)$ (c) $e^x(\sin x-\cos x)$ (d) $-e^x\sin x$
10. The slope of the tangent to $y=x^3-3x$ at $x=2$ is
    (a) 3 (b) 6 (c) 9 (d) 12
11. The local maximum value of $f(x)=3x-x^3$ is
    (a) 2 (b) $-2$ (c) 0 (d) 4
12. The value of $\lim_{x\to0}\dfrac{1-\cos x}{x^2}$ is
    (a) 0 (b) 1 (c) 2 (d) $1/2$
13. The area under $y=x^2$ from $x=0$ to $x=3$ is
    (a) 3 (b) 9 (c) 27 (d) 6
14. The value of $\displaystyle\int_0^1xe^x\,dx$ is
    (a) 0 (b) $e$ (c) 1 (d) $e-1$

::: note Answers and explanations — Set A
**1.** (b) — $\frac{\sin3x}{x}=3\cdot\frac{\sin3x}{3x}\to3$.
**2.** (c) — $(1+2x)^{1/x}=[(1+2x)^{1/2x}]^2\to e^2$.
**3.** (a) — standard derivative.
**4.** (d) — $\frac{e^{2x}}{2}$; (a) differentiates instead.
**5.** (a) — $[-\cos x]_0^\pi=1+1=2$.
**6.** (b) — highest derivative is the second (order 2), raised to the power 3 (degree 3).
**7.** (c) — separate: $\frac{dy}{y}=dx$, $\ln y=x+c$.
**8.** (d) — $e^{\int\frac{2}{x}dx}=e^{2\ln x}=x^2$.
**9.** (b) — product rule.
**10.** (c) — $3x^2-3=12-3=9$.
**11.** (a) — $f'=3-3x^2=0$ at $x=\pm1$; $f''=-6x<0$ at $x=1$, $f(1)=2$.
**12.** (d) — $\frac{1-\cos x}{x^2}\to\frac{1}{2}$.
**13.** (b) — $\frac{x^3}{3}\Big|_0^3=9$.
**14.** (c) — by parts: $[xe^x-e^x]_0^1=(e-e)-(0-1)=1$.
:::

**Set B — Understanding (10 questions)**

1. The value of $\lim_{x\to0}\dfrac{\tan x-\sin x}{x^3}$ is
   (a) $1/2$ (b) 1 (c) 0 (d) $1/3$
2. The function $f(x)=\dfrac{x^2-4}{x-2}$ ($x\ne2$) with $f(2)=k$ is continuous at 2 when $k=$
   (a) 0 (b) 2 (c) 4 (d) no value
3. If $y=\ln(\sec x+\tan x)$, then $\dfrac{dy}{dx}$ equals
   (a) $\tan x$ (b) $\sec^2x$ (c) $\sec x\tan x$ (d) $\sec x$
4. If $x=t^2$ and $y=t^3$, then $\dfrac{dy}{dx}$ at $t=2$ is
   (a) 6 (b) 3 (c) 12 (d) $3/2$
5. The radius of a sphere grows at 2 cm/s. When $r=5$ cm the volume grows at
   (a) $100\pi$ (b) $50\pi$ (c) $200\pi$ cm³/s (d) $400\pi$
6. The minimum value of $x^2-4x+7$ is
   (a) 7 (b) 4 (c) 2 (d) 3
7. $\displaystyle\int\frac{x}{x^2+1}dx$ equals
   (a) $\ln(x^2+1)+C$ (b) $\tfrac{1}{2}\ln(x^2+1)+C$ (c) $\tan^{-1}x+C$ (d) $2\ln(x^2+1)+C$
8. The value of $\displaystyle\int_0^{\pi/2}\sin^2x\,dx$ is
   (a) $\pi/4$ (b) $\pi/2$ (c) 1 (d) $\pi/8$
9. The area enclosed between $y=x$ and $y=x^2$ is
   (a) $1/2$ (b) $1/3$ (c) $1/6$ (d) $1/12$
10. The solution of $\dfrac{dy}{dx}=\dfrac{x+y}{x}$ is
    (a) $y=x(\ln x+C)$ (b) $y=x\ln x+C$ (c) $y=x+C\ln x$ (d) $y=Cx^2$

::: note Answers and explanations — Set B
**1.** (a) — $\tan x-\sin x=\tan x(1-\cos x)\approx x\cdot\frac{x^2}{2}$.
**2.** (c) — $\frac{x^2-4}{x-2}=x+2\to4$; continuity needs $k=4$.
**3.** (d) — $\frac{\sec x\tan x+\sec^2x}{\sec x+\tan x}=\sec x$.
**4.** (b) — $\frac{3t^2}{2t}=\frac{3t}{2}=3$ at $t=2$.
**5.** (c) — $\frac{dV}{dt}=4\pi r^2\frac{dr}{dt}=4\pi\cdot25\cdot2=200\pi$.
**6.** (d) — $(x-2)^2+3$.
**7.** (b) — substitute $u=x^2+1$.
**8.** (a) — $\int\frac{1-\cos2x}{2}=\frac{1}{2}\big[\frac{\pi}{2}\big]=\frac{\pi}{4}$.
**9.** (c) — $\int_0^1(x-x^2)dx=\frac{1}{2}-\frac{1}{3}=\frac{1}{6}$.
**10.** (a) — homogeneous: $y=vx$ gives $xv'=1$, $v=\ln x+C$.
:::

**Set C — Application (8 questions)**

1. The value of $\lim_{x\to0}\dfrac{e^x-1-x}{x^2}$ is
   (a) 0 (b) 1 (c) 2 (d) $1/2$
2. The maximum value of $f(x)=xe^{-x}$ for $x>0$ is
   (a) $1/e$ (b) $e$ (c) 1 (d) $1/(2e)$
3. The normal to $y=x^2$ at $(1,1)$ is
   (a) $2x+y-3=0$ (b) $x+2y-3=0$ (c) $x-2y+1=0$ (d) $2x-y-1=0$
4. The value of $\displaystyle\int_0^{\pi/2}\dfrac{\sin x}{\sin x+\cos x}dx$ is
   (a) $\pi/2$ (b) 1 (c) $\pi/8$ (d) $\pi/4$
5. The area enclosed by $y^2=4x$ and $y=x$ is
   (a) $16/3$ (b) 4 (c) $8/3$ (d) $32/3$
6. A 5 m ladder slides with its foot moving away from the wall at 3 m/s. When the foot is 3 m from the wall, the top slides down at (m/s)
   (a) $4/3$ (b) $9/4$ (c) $3/4$ (d) 4
7. The general solution of $\dfrac{dy}{dx}+y=e^{-x}$ is
   (a) $y=(x+C)e^{-x}$ (b) $y=(x+C)e^{x}$ (c) $y=e^{-x}+C$ (d) $y=xe^x+C$
8. The integrating factor of $\dfrac{dy}{dx}+\dfrac{x}{1+x}y=1+x$ is
   (a) $e^x$ (b) $(1+x)e^x$ (c) $\dfrac{e^x}{1+x}$ (d) $\dfrac{e^x}{x}$

::: note Answers and explanations — Set C
**1.** (d) — $e^x-1-x=\frac{x^2}{2}+\frac{x^3}{6}+\cdots$.
**2.** (a) — $f'=e^{-x}(1-x)=0$ at $x=1$; $f(1)=1/e$ and $f''(1)<0$.
**3.** (b) — tangent slope 2, normal slope $-\frac{1}{2}$: $y-1=-\frac{1}{2}(x-1)$.
**4.** (d) — $I=\int_0^{\pi/2}\frac{\cos x}{\sin x+\cos x}dx$ by $x\to\frac{\pi}{2}-x$; $2I=\frac{\pi}{2}$.
**5.** (c) — meet at $x=0,4$: $\int_0^4(2\sqrt{x}-x)dx=\frac{32}{3}-8=\frac{8}{3}$.
**6.** (b) — $x^2+y^2=25$: $x\dot x+y\dot y=0$ with $x=3$, $y=4$: $9+4\dot y=0$, $|\dot y|=\frac{9}{4}$.
**7.** (a) — IF $=e^x$: $(ye^x)'=1$, so $ye^x=x+C$.
**8.** (c) — $\int\frac{x}{1+x}dx=x-\ln(1+x)$, so IF $=\frac{e^x}{1+x}$.
:::

**Group D — Model answers for long questions (10 marks each, for deeper revision)**

1. Evaluate limits (standard forms, L'Hospital's rule), test continuity, and solve an optimisation and a tangent problem. <span class="marks">[10]</span>
2. Evaluate integrals (by parts), find an area, and solve first-order differential equations including Newton's law of cooling. <span class="marks">[10]</span>

### Model answer D1: Limits, derivatives and applications (10 marks)

**Introduction.** A function is **continuous** at $a$ if $\lim_{x\to a}f(x)=f(a)$. Standard limits: $\lim_{x\to0}\frac{\sin x}{x}=1$, $\lim_{x\to0}\frac{e^x-1}{x}=1$, $\lim_{x\to0}(1+x)^{1/x}=e$.

**Limits.**

1. $\lim_{x\to0}\frac{1-\cos x}{x^2}=\lim\frac{2\sin^2(x/2)}{x^2}=\frac12$.
2. **L'Hospital's rule** for $\frac00$ or $\frac\infty\infty$: $\lim_{x\to0}\frac{x-\sin x}{x^3}=\lim\frac{1-\cos x}{3x^2}=\lim\frac{\sin x}{6x}=\frac16$.

**Optimisation (open box).** A square sheet of side $12\ \text{cm}$ has corner squares of side $x$ cut off and the sides are folded up.

1. Volume $V=x(12-2x)^2$.
2. $\frac{dV}{dx}=(12-2x)^2-4x(12-2x)=(12-2x)(12-6x)$.
3. Setting it to zero: $x=6$ (no box) or $x=2$.
4. $\frac{d^2V}{dx^2}<0$ at $x=2$, so it is a **maximum**: $V_{\max}=2(8)^2=128\ \text{cm}^3$.

**Tangent.** For $y=x^3-3x+2$ at $x=2$: $y=4$, $\frac{dy}{dx}=3x^2-3=9$, so the tangent is $y-4=9(x-2)$, i.e. $y=9x-14$. The normal has slope $-\frac19$.

| Topic | Rule | Result |
|---|---|---|
| Limit | L'Hospital | $\frac16$ |
| Maximum volume | $V'=0$, $V''<0$ | $128\ \text{cm}^3$ at $x=2$ |
| Tangent | slope $=y'$ | $y=9x-14$ |

**Conclusion.** Derivatives give slopes and extreme values, and L'Hospital's rule resolves indeterminate forms.

### Model answer D2: Integration and differential equations (10 marks)

**Introduction.** Integration reverses differentiation, and a definite integral gives an area: $\int_a^bf(x)\,dx=F(b)-F(a)$.

**1. Integration by parts.** $\int u\,dv=uv-\int v\,du$. For $\int xe^x\,dx$ let $u=x$, $dv=e^xdx$: $=xe^x-e^x+C=e^x(x-1)+C$.

**2. Area.** The area between $y=x$ and $y=x^2$ (they meet at $x=0$ and $x=1$) is $\int_0^1(x-x^2)\,dx=\left[\frac{x^2}{2}-\frac{x^3}{3}\right]_0^1=\frac12-\frac13=\frac16$ square units. Also $\int_0^1\frac{dx}{1+x^2}=\tan^{-1}1=\frac\pi4$.

**3. Separable equation.** $\frac{dy}{dx}=xy\Rightarrow\int\frac{dy}{y}=\int x\,dx\Rightarrow y=Ce^{x^2/2}$.

**4. Linear equation.** $\frac{dy}{dx}+2y=e^{-x}$ with $y(0)=2$.

1. Integrating factor $=e^{\int2\,dx}=e^{2x}$.
2. $\frac{d}{dx}(ye^{2x})=e^{x}$, so $ye^{2x}=e^x+C$.
3. $y=e^{-x}+Ce^{-2x}$, and $y(0)=2\Rightarrow1+C=2\Rightarrow C=1$.
4. Solution: $y=e^{-x}+e^{-2x}$.

**5. Newton's law of cooling.** $\frac{dT}{dt}=-k(T-T_a)$ gives $T=T_a+(T_0-T_a)e^{-kt}$. A drink at $100^\circ\text{C}$ in a $20^\circ\text{C}$ room: $T=20+80e^{-kt}$. If $T=50$ at $t=10\ \text{min}$: $30=80e^{-10k}$, so $k=\frac{\ln(8/3)}{10}=0.0981\ \text{min}^{-1}$. At $t=20$: $T=20+80e^{-1.962}=20+80(0.1406)=31.25^\circ\text{C}$.

| Problem | Method | Answer |
|---|---|---|
| $\int xe^x$ | By parts | $e^x(x-1)+C$ |
| Area between curves | $\int(\text{top}-\text{bottom})$ | $\frac16$ |
| Linear ODE | Integrating factor | $e^{-x}+e^{-2x}$ |
| Cooling | Separate variables | $31.25^\circ\text{C}$ |

**Conclusion.** The choice between substitution, parts, separation and an integrating factor depends on the form of the integrand or equation.
