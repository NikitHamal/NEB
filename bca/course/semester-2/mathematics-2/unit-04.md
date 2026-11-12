---
subject: Mathematics II
grade: BCA Semester 2
unit: 4
title: Integration
area: BCA 154 · Mathematics II · Unit 4
---

Integration reverses differentiation and also adds up infinitely many infinitesimal pieces. With it we compute areas, volumes, total change, averages and, in the next unit, solve differential equations.

::: key What this unit gives you
- Antiderivatives, the table of standard integrals, and the substitution, parts and partial-fraction methods.
- The definite integral, the Fundamental Theorem of Calculus, and its properties.
- Area between curves, volume of revolution, average value, and improper integrals.
- Surface area of a solid of revolution, and numerical integration by the trapezoidal and Simpson rules with error bounds.
:::

## 4.1 Indefinite integrals

F is an **antiderivative** of *f* if $F' = f$. The family of all antiderivatives is the **indefinite integral** $\int f (x) \,d x = F (x) + C$, where C is an arbitrary constant.

| $f (x)$ | $\int f \,d x$ | $f (x)$ | $\int f \,d x$ |
|---|---|---|---|
| $x^{n} (n \neq - 1)$ | $\frac{x^{n+1}}{n + 1}$ | $\frac{1}{x}$ | ln\|x\| |
| $e^{x}$ | $e^{x}$ | $a^{x}$ | $\frac{a^{x}}{\ln}$ a |
| $\sin x$ | $- \cos x$ | $\cos x$ | $\sin x$ |
| $\sec^{2} x$ | $\tan x$ | $\csc^{2} x$ | $- \cot x$ |
| $\sec x \tan x$ | $\sec x$ | $\frac{1}{(1 + x^{2})}$ | $\tan^{-1} x$ |
| $\frac{1}{\sqrt{1 - x^{2}}}$ | $\sin^{-1} x$ | $\tan x$ | ln\|sec x\| |
| $\frac{1}{\sqrt{x^{2} + a^{2}}}$ | ln\|x + $\sqrt{x^{2} + a^{2}} \mid$ | $\frac{1}{(x^{2} - a^{2})}$ | $\left( \frac{1}{2 a} \right)$ ln\|(x − $a ) / ( x$ + a)\| |

Linearity: *∫* (af + bg) = $a \int f + b \int g$. Always check an answer by differentiating it.

::: example Worked example

$$\int (3 x^{2} + 2 x + 1) \,d x = x^{3} + x^{2} + x + C$$

$$\int \left( \sqrt{x} + \frac{1}{x^{2}} \right) \,d x = \left( \frac{2}{3} \right) x^{\frac{3}{2}} - \frac{1}{x} + C$$

$$\int \sin^{2} x \,d x = \frac{\int (1 - \cos 2 x)}{2} \,d x = \frac{x}{2} - \frac{\sin 2 x}{4} + C$$

:::

```photogrid label="4.1" cols="3" ratio="1.2" caption="Integration in history and in Nepal. (a) Archimedes of Syracuse (*c*. 287-212 BC) found areas and volumes by the method of exhaustion, the ancestor of the integral. (b) Bernhard Riemann (1826-1866) gave the definition by sums that we use today. (c) The reservoir wall of the Kaligandaki A hydropower station in Syangja: the force of water on the wall is an integral of pressure over depth."
@ photo id="bca104/archimedes" cap="Archimedes (painting by D. Fetti, 1620)"
fit 1.2
focus 0.5 0.7
@ photo id="bca104/riemann" cap="Bernhard Riemann"
fit 1.2
focus 0.5 0.72
@ photo id="bca104/kgdam" cap="Kaligandaki A dam, Syangja"
fit 1.2
call 0.5 0.93 0.5 0.6 "F = ∫ ρ g h w dh"
```

## 4.2 Integration by substitution

If an integral has the form $\int f (g (x)) g' (x) \,d x$, put $u = g (x) ,\  d u = g' (x) d x$, and integrate in *u*.

::: example Worked example
**(a)** $\int 2 x e^{x^{2}} \,d x$: $u = x^{2} ,\  d u = 2 x d x$, so $\int e^{u} \,d u = e^{x^{2}} + C$.

**(b)** $\frac{\int x}{x^{2} + 1} \,d x$: $u = x^{2} + 1 ,\  d u = 2 x d x$, so $\frac{1}{2} \frac{\int d u}{u}$ = **$\frac{1}{2} \ln (x^{2} + 1) + C$**.

**(c)** $\int \tan x \,d x = \frac{\int \sin x}{\cos x} \,d x$: $u = \cos x ,\  d u = - \sin x d x$, so −ln|cos x| + C = ln|sec x| + C.

**(d)** $\int \cos^{3} x \,d x = \int (1 - \sin^{2} x) \cos x \,d x$: $u = \sin x$, so $\sin x - \frac{\sin^{3} x}{3} + C$.

**(e)** $\frac{\int 1}{x \ln x} \,d x$: $u = \ln x$, so ln|ln x| + C.

**(f)** $\int (2 x + 3)^{5} \,d x = \frac{(2 x + 3)^{6}}{12} + C$.
:::

## 4.3 Integration by parts

From $(u v)' = u' v + u v'$: **$\int u \,d v = u v - \int v \,d u$**. Choose *u* in the order **LIATE** (Logarithmic, Inverse trig, Algebraic, Trig, Exponential): the first type that appears becomes *u*.

::: example Worked example
**(a)** $\int x e^{x} \,d x$: $u = x ,\  \,d v = e^{x} \,d x \Rightarrow x e^{x} - \int e^{x} \,d x$ = **$(x - 1) e^{x} + C$**.

**(b)** $\int x^{2} \ln x \,d x$: $u = \ln x ,\  \,d v = x^{2} \,d x \Rightarrow \left( \frac{x^{3}}{3} \right) \ln x - \frac{\int x^{2}}{3} \,d x$ = **$\left( \frac{x^{3}}{3} \right) \ln x - \frac{x^{3}}{9} + C$**.

**(c)** $\int \ln x \,d x$: $u = \ln x ,\  d v = d x \Rightarrow x \ln x - x + C$.

**(d)** $\int x \sin x \,d x = - x \cos x + \sin x + C$.

**(e)** $\int e^{x} \sin x \,d x = I$. By parts twice, $I = e^{x} \sin x - e^{x} \cos x - I$, so **$I = \frac{e^{x} (\sin x - \cos x)}{2} + C$**.

**(f)** $\int \tan^{-1} x \,d x = x \tan^{-1} x - \frac{1}{2} \ln (1 + x^{2}) + C$.
:::

## 4.4 Partial fractions

A proper rational function $\frac{P (x)}{Q (x)}$ (degree P < degree Q) is split into simpler fractions by factors of Q: a linear factor $(x - a)$ gives $\frac{A}{x - a}$; a repeated factor $(x - a)^{2}$ gives $\frac{A}{x - a} + \frac{B}{(x - a)^{2}}$; an irreducible quadratic gives (Ax + $B ) / ( x^{2} + p x + q$). If the degree of P ≥ degree of Q, divide first.

::: example Worked example
**(a)** $\frac{1}{(x - 1) (x + 2)} = \frac{A}{x - 1} + \frac{B}{x + 2}$. Then $1 = A (x + 2) + B (x - 1) ;\  x = 1$ gives $A = \frac{1}{3} ;\  x = - 2$ gives $B = - \frac{1}{3}$. So $\int = \frac{1}{3}$ ln|x − 1| − $\frac{1}{3}$ ln|x + 2| = **$\frac{1}{3}$ ln|(x − $1 ) / ( x$ + 2)| + C**.

**(b)** $\frac{3 x + 5}{((x + 1)^{2})} = \frac{3}{x + 1} + \frac{2}{(x + 1)^{2}}$. $\int = 3$ ln|x + 1| − $\frac{2}{x + 1} + C$.

**(c)** $\frac{\int (x^{2} + 1)}{x - 1} \,d x$: divide, $x^{2} + 1 = (x - 1) (x + 1) + 2$, so $\int \left( x + 1 + \frac{2}{x - 1} \right) \,d x = \frac{x^{2}}{2} + x + 2$ ln|x − 1| + C.
:::

## 4.5 The definite integral and the Fundamental Theorem

The **definite integral** $\int_{a}^{b} f (x) \,d x$ is the limit of Riemann sums $\sum f (x_{i}) \Delta x$, the signed area between the graph and the x-axis from a to *b*. The **Fundamental Theorem of Calculus** connects it to antiderivatives:

- **Part 1**: if $F (x) = \int_{a}^{x} f (t) \,d t$ then $F' (x) = f (x)$.
- **Part 2**: **$\int_{a}^{b} f (x) \,d x = F (b) - F (a)$** for any antiderivative F.

**Properties.** $\int_{a}^{b} f = - \int_{a}^{b} f ;\  \int_{a}^{a} f = 0 ;\  \int_{a}^{b} f = \int_{a}^{c} f + \int^{cb} f ;\  \int_{a}^{b} f (x) \,d x = \int_{a}^{b} f (a + b - x) \,d x$; for even $f ,\  \int_{-a}^{a} f = 2 \int_{0}^{a} f$; for odd $f ,\  \int_{-a}^{a} f = 0$. When substituting in a definite integral, change the limits too.

::: example Worked example
**(a)** $\int_{0}^{\pi} \sin x \,d x = [- \cos x]_{0}^{\pi} = 1 + 1$ = **2**.

**(b)** $\frac{\int_{1}^{2} d x}{x} = \ln 2 - \ln 1$ = **$\ln 2 \approx 0.693$**.

**(c)** $\int_{0}^{1} 2 x e^{x^{2}} \,d x$: $u = x^{2}$, limits $0 \to 1$: $\int_{0}^{1} e^{u} \,d u$ = **$e - 1 \approx 1.718$**.

**(d)** $\int_{0}^{\frac{\pi}{2}} \sin^{3} x \,d x = \int_{0}^{\frac{\pi}{2}} (1 - \cos^{2} x) \sin x \,d x ,\  u = \cos x$: $\int_{0}^{1} (1 - u^{2}) \,d u = 1 - \frac{1}{3}$ = **$\frac{2}{3}$**.

**(e)** $\int_{-1}^{1} x^{3} \,d x$ = **0** (odd function).

**(f)** $\int_{0}^{1} x e^{x} \,d x = [(x - 1) e^{x}]_{0}^{1} = 0 - (- 1)$ = **1**.
:::

```svgfig label="4.1" caption="Riemann sums for the area under $f (x) = x^{2}$ on [0, 2]. (a) Four left rectangles under-estimate (1.75). (b) Four right rectangles over-estimate (3.75). (c) Twenty mid-point rectangles are almost exact. As $n \to \infty$ every version tends to the definite integral $\int_{0}^{2} x^{2} \,d x = \frac{8}{3} \approx 2.6667$."
f = Fig(780, 250)
fx = lambda x: x * x
mid = sum(fx(0.05 + 0.1 * k) * 0.1 for k in range(20))
for i, (mode, n, t, val) in enumerate([("left", 4, "(a) left sum, n = 4", "1.75"), ("right", 4, "(b) right sum, n = 4", "3.75"), ("mid", 20, "(c) mid-point sum, n = 20", f"{mid:.4f}")]):
    cx = 8 + i * 258
    f.box(cx, 4, 246, 242, "", fill=SOFT, stroke="#cbd5e1")
    f.text(cx + 123, 22, t, size=11, color=NAVY, bold=True)
    a = Axes(f, cx + 22, 34, 208, 150, (-0.2, 2.3), (-0.3, 4.6)); a.grid(1, 1, size=8.5)
    a.bars(fx, 0, 2, n, mode=mode); a.curve(fx, 0, 2.3, color=NAVY, sw=2.4); a.axes("", "")
    f.text(cx + 123, 214, "sum ≈ " + val, size=12, color=TEAL if i == 2 else AMBER, bold=True); f.text(cx + 123, 235, "exact value 8/3 = 2.6667", size=9.5, color=SLATE)
```

## 4.6 Applications

**Area between curves.** If $f \geq g$ on $[a ,\  b]$: $A = \int_{a}^{b} [f (x) - g (x)] \,d x$. If the curves cross, split at the intersections.

**Volume of revolution** about the x-axis (disc method): $V = \pi \int_{a}^{b} [f (x)]^{2} \,d x$; with a hole (washer): $V = \pi \int (R^{2} - r^{2}) \,d x$. About the y-axis (shell method): $V = 2 \pi \int x f (x) \,d x$.

**Average value** of *f* on $[a ,\  b]$: $\left( \frac{1}{b - a} \right) \int_{a}^{b} f \,d x$. **Arc length**: $L = \int_{a}^{b} \sqrt{1 + (f')^{2}} \,d x$. **Total change**: *∫* of a rate gives the net change (distance = *∫* speed $d t$).

::: example Worked example
**Area** between $y = x$ and $y = x^{2}$: intersections $x = 0 ,\  1 ;\  A = \int_{0}^{1} (x - x^{2}) \,d x = \frac{1}{2} - \frac{1}{3}$ = **$\frac{1}{6}$**.

**Area** under $y = \sin x$ from 0 to *π*: **2**.

**Volume** of $y = x^{2}$ about the x-axis from 0 to 1: $V = \pi \int_{0}^{1} x^{4} \,d x$ = **$\frac{\pi}{5}$**. For $y = \sqrt{x}$ on [0, 4]: $V = \pi \int_{0}^{4} x \,d x$ = **$8 \pi$**.

**Average value** of $f (x) = x^{2}$ on [0, 3]: $\left( \frac{1}{3} \right) \left( \frac{27}{3} \right)$ = **3**.

**Net displacement** for velocity $v (t) = 3 t^{2} - 6 t + 2$ from $t = 0$ to 2: $[t^{3} - 3 t^{2} + 2 t]_{0}^{2} = 8 - 12 + 4$ = **0** (the body returns to its start; the *distance* travelled is $\int |v| \,d t$, which is larger).
:::

```svgfig label="4.2" caption="Two applications of the definite integral. (a) The area between $y = x$ and $y = x^{2}$ on [0, 1] is $\int_{0}^{1} (x - x^{2}) \,d x = \frac{1}{2} - \frac{1}{3} = \frac{1}{6}$. (b) Rotating $y = \sqrt{x}$ about the x-axis for $0 \leq x \leq 4$ sweeps out a solid made of thin discs of radius $\sqrt{x}$, so $V = \pi \int_{0}^{4} x \,d x = 8 \pi \approx 25.13$ cubic units."
f = Fig(780, 270)
f.box(8, 4, 330, 262, "", fill=SOFT, stroke="#cbd5e1"); f.text(173, 22, "(a) area between two curves", size=11, color=NAVY, bold=True)
a = Axes(f, 40, 36, 270, 190, (-0.1, 1.2), (-0.1, 1.2)); a.grid(0.5, 0.5, size=8.5)
a.area(lambda x: x, 0, 1, fn2=lambda x: x * x, fill="#99f6e4"); a.axes()
a.curve(lambda x: x, color=NAVY, sw=2.4); a.curve(lambda x: x * x, color=RED, sw=2.4)
f.text(a.X(0.7), a.Y(0.9), "y = x", size=11, color=NAVY, bold=True, anchor="start"); f.text(a.X(0.78), a.Y(0.4), "y = x²", size=11, color=RED, bold=True, anchor="start"); f.text(173, 250, "area = 1/6 ≈ 0.1667", size=11, color=TEAL, bold=True)
f.box(346, 4, 426, 262, "", fill=SOFT, stroke="#cbd5e1"); f.text(559, 22, "(b) solid of revolution about the x-axis", size=11, color=NAVY, bold=True)
b = Axes(f, 370, 36, 380, 190, (-0.4, 4.6), (-2.4, 2.4)); b.area(lambda x: math.sqrt(x), 0, 4, fn2=lambda x: -math.sqrt(x), fill="#bfdbfe", opacity=0.6)
for xv in (1, 2, 3, 4):
    f.raw(f'<ellipse cx="{b.X(xv)}" cy="{b.Y(0)}" rx="6" ry="{round(b.Y(0) - b.Y(math.sqrt(xv)), 2)}" fill="none" stroke="{TEAL}" stroke-width="1.3"/>')
b.axes(); b.curve(math.sqrt, 0, 4, color=NAVY, sw=2.4); b.curve(lambda x: -math.sqrt(x), 0, 4, color=NAVY, sw=1.6, dash=True)
f.text(b.X(1.0), b.Y(1.9), "y = √x, rotated", size=11, color=NAVY, bold=True, anchor="start"); f.text(559, 250, "V = π ∫₀⁴ x dx = 8π ≈ 25.13", size=11, color=TEAL, bold=True)
```

## 4.7 Improper integrals

An integral with an infinite limit or an infinite integrand is defined as a limit.

::: example Worked example
**(a)** $\int_{1}^{\infty} x^{-2} \,d x = \lim_{b \to \infty} \left[ - \frac{1}{x} \right]_{1}^{b} = 1 - 0$ = **1** (converges).

**(b)** $\frac{\int_{1}^{\infty} 1}{x} \,d x = \lim \ln b = \infty$ (**diverges**).

**(c)** $\int_{0}^{1} x^{- \frac{1}{2}} \,d x = \lim_{a \to 0^{+}} \left[ 2 \sqrt{x} \right]_{a}^{1}$ = **2** (converges).

**(d)** $\int_{0}^{\infty} e^{- x} \,d x$ = **1**.

**Rule:** $\int_{1}^{\infty} x^{- p} \,d x$ converges iff $p > 1 ;\  \int_{0}^{1} x^{- p} \,d x$ converges iff $p < 1$.
:::

```svgfig label="4.3" caption="Improper integrals over an infinite interval. (a) The area under $y = \frac{1}{x^{2}}$ from 1 to infinity is finite: $\frac{\int_{1}^{b} d x}{x^{2}} = 1 - \frac{1}{b} \to 1$. (b) The area under $y = \frac{1}{x}$ is infinite: $\frac{\int_{1}^{b} d x}{x} = \ln b \to \infty$. Both curves tend to 0, yet only the first area is finite."
f = Fig(780, 240)
for i, (fn, t, s, c) in enumerate([(lambda x: 1 / (x * x), "(a) y = 1/x²", "converges: area = 1", TEAL), (lambda x: 1 / x, "(b) y = 1/x", "diverges: area = ∞", RED)]):
    cx = 8 + i * 388
    f.box(cx, 4, 376, 232, "", fill=SOFT, stroke="#cbd5e1"); f.text(cx + 188, 22, t, size=11.5, color=NAVY, bold=True)
    a = Axes(f, cx + 36, 34, 320, 150, (0, 6.5), (0, 1.2)); a.grid(1, 0.5, size=8.5)
    a.area(fn, 1, 6.5, fill="#99f6e4" if i == 0 else "#fecaca"); a.axes(); a.curve(fn, 1, 6.5, color=NAVY, sw=2.4); a.vline(1, 0, 1.2, color=AMBER)
    f.text(cx + 188, 222, s, size=11.5, color=c, bold=True)
```

## 4.8 Surface area of a solid of revolution

When the arc $y = f(x)$, $a \le x \le b$, is rotated about the x-axis it sweeps out a surface. A thin strip of arc of length $ds = \sqrt{1 + (f')^{2}}\,dx$ at height $y$ sweeps a ring of radius $y$ and width $ds$, whose area is $2\pi y\,ds$. Adding the rings gives

$$S = 2\pi \int_{a}^{b} f(x) \sqrt{1 + [f'(x)]^{2}}\,dx.$$

For rotation about the y-axis of $x = g(y)$ the formula is $S = 2\pi \int_{c}^{d} g(y) \sqrt{1 + [g'(y)]^{2}}\,dy$. The volume formulas of Section 4.6 and this surface formula are the *volume and surface integrals* named in the TU syllabus.

::: example Worked example
**Cone.** Rotate $y = x$ for $0 \le x \le 1$ about the x-axis. Here $y' = 1$, so $S = 2\pi \int_{0}^{1} x\sqrt{2}\,dx = 2\pi\sqrt{2} \cdot \frac{1}{2} = \pi\sqrt{2} \approx 4.443$. (Check: a cone of slant height $\sqrt{2}$ and base radius 1 has curved area $\pi r l = \pi\sqrt{2}$.)

**Sphere.** Rotate $y = \sqrt{r^{2} - x^{2}}$ on $-r \le x \le r$. Then $y' = -\frac{x}{y}$ and $y\sqrt{1 + y'^{2}} = \sqrt{y^{2} + x^{2}} = r$, so $S = 2\pi \int_{-r}^{r} r\,dx = 2\pi r \cdot 2r = $ **$4\pi r^{2}$**, the familiar area of a sphere.

**Paraboloid.** For $y = \sqrt{x}$, $0 \le x \le 4$: $y' = \frac{1}{2\sqrt{x}}$ and $y\sqrt{1 + y'^{2}} = \sqrt{x}\sqrt{1 + \frac{1}{4x}} = \frac{1}{2}\sqrt{4x + 1}$. So $S = \pi \int_{0}^{4} \sqrt{4x + 1}\,dx = \frac{\pi}{6}\left[(4x + 1)^{3/2}\right]_{0}^{4} = \frac{\pi}{6}(17\sqrt{17} - 1) \approx 36.18$.
:::

## 4.9 Numerical integration

Some integrals, such as $\int e^{-x^{2}}\,dx$, have no antiderivative in elementary functions, and in practice the function is often known only as a **table of measured values**. Then the area is **approximated** by replacing the curve with simple shapes over equal strips of width $h = \frac{b - a}{n}$, with ordinates $y_i = f(a + ih)$.

### Trapezoidal rule

Replace the curve on each strip by a straight chord. The strip is a trapezoid of area $\frac{h}{2}(y_{i} + y_{i+1})$. Adding the *n* strips:

$$\int_{a}^{b} f\,dx \approx \frac{h}{2}\left[y_{0} + 2(y_{1} + y_{2} + \cdots + y_{n-1}) + y_{n}\right].$$

### Simpson's 1/3 rule

Take the strips in **pairs** and fit a parabola through three consecutive points. The area under the parabola gives, for **even** *n*,

$$\int_{a}^{b} f\,dx \approx \frac{h}{3}\left[y_{0} + 4(y_{1} + y_{3} + \cdots + y_{n-1}) + 2(y_{2} + y_{4} + \cdots + y_{n-2}) + y_{n}\right].$$

The weights run $1, 4, 2, 4, 2, \ldots, 4, 1$. **Simpson's 3/8 rule** fits cubics through four points and needs *n* to be a multiple of 3: $\frac{3h}{8}\left[y_{0} + 3y_{1} + 3y_{2} + 2y_{3} + 3y_{4} + 3y_{5} + 2y_{6} + \cdots + y_{n}\right]$.

### Error

For a smooth function, $|E_{T}| \le \frac{(b - a)h^{2}}{12} \max|f''|$ and $|E_{S}| \le \frac{(b - a)h^{4}}{180} \max|f^{(4)}|$. Halving *h* therefore cuts the trapezoidal error by about **4** and the Simpson error by about **16**. Simpson's rule is **exact for polynomials up to degree 3** because $f^{(4)} = 0$ for them.

```svgfig label="4.3" caption="Two ways to approximate $\int_{0}^{1} \frac{dx}{1 + x^{2}} = \frac{\pi}{4}$ with $n = 4$ strips. (a) The trapezoidal rule joins the ordinates by chords and gives $0.78279$. (b) Simpson's rule fits a parabola through each pair of strips and gives $0.78539$, within $6 \times 10^{-6}$ of $\frac{\pi}{4} = 0.785398$."
f = Fig(780, 270)
g = lambda x: 1 / (1 + x * x)
f.box(8, 4, 372, 262, "", fill=SOFT, stroke="#cbd5e1"); f.text(194, 22, "(a) trapezoidal rule", size=11, color=NAVY, bold=True)
a = Axes(f, 44, 36, 310, 190, (-0.05, 1.1), (0, 1.15)); a.grid(0.25, 0.25, size=8.5)
for i in range(4):
    x0, x1 = i / 4, (i + 1) / 4
    f.poly([(a.X(x0), a.Y(0)), (a.X(x0), a.Y(g(x0))), (a.X(x1), a.Y(g(x1))), (a.X(x1), a.Y(0))], fill="#99f6e4", stroke=TEAL, sw=1.3)
a.axes(); a.curve(g, 0, 1, color=NAVY, sw=2.4)
f.text(194, 250, "T = 0.78279 (error 2.6 × 10⁻³)", size=11, color=TEAL, bold=True)
f.box(388, 4, 384, 262, "", fill=SOFT, stroke="#cbd5e1"); f.text(580, 22, "(b) Simpson's 1/3 rule", size=11, color=NAVY, bold=True)
b = Axes(f, 424, 36, 322, 190, (-0.05, 1.1), (0, 1.15)); b.grid(0.25, 0.25, size=8.5)
def par(xa, xm, xb):
    ya, ym, yb = g(xa), g(xm), g(xb)
    return lambda x: ya * (x - xm) * (x - xb) / ((xa - xm) * (xa - xb)) + ym * (x - xa) * (x - xb) / ((xm - xa) * (xm - xb)) + yb * (x - xa) * (x - xm) / ((xb - xa) * (xb - xm))
for (xa, xm, xb) in ((0, 0.25, 0.5), (0.5, 0.75, 1.0)):
    q = par(xa, xm, xb)
    b.area(q, xa, xb, fill="#fde68a", opacity=0.8)
b.axes(); b.curve(g, 0, 1, color=NAVY, sw=2.4)
for (xa, xm, xb) in ((0, 0.25, 0.5), (0.5, 0.75, 1.0)):
    b.curve(par(xa, xm, xb), xa, xb, color=RED, sw=1.8, dash=True)
f.text(580, 250, "S = 0.78539 (error 6 × 10⁻⁶)", size=11, color=TEAL, bold=True)
```

```python
import math
# Trapezoidal and Simpson's rules for the integral of 1/(1+x^2) from 0 to 1 (exact value pi/4)
g = lambda x: 1 / (1 + x * x)
def trapezoid(f, a, b, n):
    h = (b - a) / n
    return h / 2 * (f(a) + f(b) + 2 * sum(f(a + i * h) for i in range(1, n)))
def simpson(f, a, b, n):          # n must be even
    h = (b - a) / n
    s = f(a) + f(b) + 4 * sum(f(a + i * h) for i in range(1, n, 2)) + 2 * sum(f(a + i * h) for i in range(2, n, 2))
    return h / 3 * s
exact = math.pi / 4
print("exact      %.7f" % exact)
for n in (4, 8, 16):
    t, s = trapezoid(g, 0, 1, n), simpson(g, 0, 1, n)
    print("n = %2d  trapezoid %.7f (err %.2e)   simpson %.7f (err %.2e)" % (n, t, abs(t - exact), s, abs(s - exact)))
# Simpson is exact for a cubic: integral of x^3 on [0, 2] is 4
print("cubic, simpson n=2:", simpson(lambda x: x ** 3, 0, 2, 2))
# A table of measured speeds (m/s) every 10 s: distance travelled
v = [0, 3, 8, 14, 17, 18, 18]
h = 10
trap = h / 2 * (v[0] + v[-1] + 2 * sum(v[1:-1]))
simp = h / 3 * (v[0] + v[-1] + 4 * (v[1] + v[3] + v[5]) + 2 * (v[2] + v[4]))
print("distance in 60 s: trapezoid %.2f m, simpson %.2f m" % (trap, simp))
```
```output
exact      0.7853982
n =  4  trapezoid 0.7827941 (err 2.60e-03)   simpson 0.7853922 (err 6.01e-06)
n =  8  trapezoid 0.7847471 (err 6.51e-04)   simpson 0.7853981 (err 3.78e-08)
n = 16  trapezoid 0.7852354 (err 1.63e-04)   simpson 0.7853982 (err 5.91e-10)
cubic, simpson n=2: 4.0
distance in 60 s: trapezoid 690.00 m, simpson 693.33 m
```
::: example Worked example
**Table of measured values.** A bus has the speeds $v = 0, 3, 8, 14, 17, 18, 18$ m/s at $t = 0, 10, \ldots, 60$ s. The distance is $\int_{0}^{60} v\,dt$ with $h = 10$ and $n = 6$.

Trapezoidal: $\frac{10}{2}[0 + 18 + 2(3 + 8 + 14 + 17 + 18)] = 5(18 + 120) = 690$ m.

Simpson: $\frac{10}{3}[0 + 18 + 4(3 + 14 + 18) + 2(8 + 17)] = \frac{10}{3}(18 + 140 + 50) = \frac{2080}{3} \approx 693.3$ m.

The two estimates differ by 3.3 m (about 0.5%), which is typical when the data are smooth; Simpson's value is normally the better one.
:::

::: note Bound on the error
For $\int_{0}^{1} \frac{dx}{1 + x^{2}}$ with $n = 4$, $\max|f''| = 2$ (at $x = 0$), so $|E_{T}| \le \frac{1 \cdot 0.25^{2}}{12} \cdot 2 \approx 0.0104$. The actual error $0.0026$ is inside this bound. The bound is a guarantee, not a prediction.
:::

## 4.10 Eight uses of integration

1. **Area of irregular land.** The area under a curve is a definite integral, so surveyors and map software can find the area of a plot with a curved boundary. In Nepal land is measured in ropani and kattha, and the same idea converts a measured outline into area. A smaller strip width gives a more exact answer (Figure 4.1).
2. **Volume of tanks and solids.** Cutting a solid into thin discs and adding them gives volume (Figure 4.2b). Water tank, bottle and $d a m$ designers use it to know how much each shape holds. The reservoir of a hydropower plant is estimated this way.
3. **Distance from speed.** If the speed $v (t)$ of a bus is known, the distance travelled is $\int v \,d t$. A GPS tracker adds many small distances to give the trip length. This is the reverse of differentiation: position is the integral of speed.
4. **Work, force and pressure.** The pressure on a $d a m$ wall increases with depth, so the total force is an integral of pressure over the wall (Plate 4.1c). Engineers of the Kaligandaki and Marsyangdi plants need this to make the wall strong enough. A constant-force formula alone would be wrong.
5. **Probability and statistics.** For a continuous variable, the probability that a value lies between a and *b* is the area under its density curve. The normal curve of exam marks is integrated to find how many students score above 60. Tribhuvan University result analysis is built on such areas.
6. **Electricity and signals.** The charge stored in a capacitor is the integral of the current, and the energy used by a house is the integral of power over time. Nepal Electricity Authority meters add power over hours in the same way. Digital signal processing also integrates signals to find their average and energy.
7. **Computer graphics and numerical methods.** Computers cannot do symbolic integration for every function, so they use Riemann-type sums such as the trapezoidal and Simpson's rules. These give an accurate area with a fast loop. Games and simulations use them for physics.
8. **Average value and economics.** The average value of a function on $[a ,\  b]$ is $\left( \frac{1}{b - a} \right) \int f \,d x$. An economist finds the average daily electricity demand or the total revenue from a marginal revenue curve. The consumer surplus in a market is also an area between two curves.

## Formula and fact sheet

- $\int x^{n} \,d x = \frac{x^{n+1}}{n + 1} ;\  \frac{\int d x}{x}$ = ln|x|; $\int e^{x} = e^{x} ;\  \int \sin = - \cos ;\  \int \cos = \sin$.
- Substitution: $u = g (x)$. Parts: $\int u \,d v = u v - \int v \,d u$, LIATE.
- FTC: $\int_{a}^{b} f = F (b) - F (a)$. Even: $2 \int_{0}^{a}$; odd: 0.
- Area = *∫* (top − bottom). Disc volume = $\pi \int f^{2}$. Average = $\left( \frac{1}{b - a} \right) \int f$.
- Improper: $\int_{1}^{\infty} x^{- p}$ converges for $p > 1$.
- Surface of revolution: $S = 2 \pi \int y \sqrt{1 + y'^{2}} \,d x$.
- Trapezoidal: $\frac{h}{2} [y_0 + 2 (y_1 + \cdots + y_{n-1}) + y_n]$. Simpson 1/3 ($n$ even): $\frac{h}{3} [y_0 + 4 (\text{odd}) + 2 (\text{even}) + y_n]$. Errors $\propto h^{2}$ and $h^{4}$.

## Chapter summary

- Surfaces of revolution use $2 \pi y \, ds$; integrals with no elementary antiderivative or only tabulated data are approximated by the trapezoidal and Simpson rules.
- Integration is reverse differentiation; always add C for indefinite integrals and verify by differentiating.
- Substitution undoes the chain rule, parts undoes the product rule, partial fractions handle rational functions.
- The Fundamental Theorem lets us compute definite integrals from antiderivatives.
- Areas, volumes, averages and total change are all definite integrals; improper integrals are limits.

## Practice

1. Evaluate (a) $\int \left( 4 x^{3} - \frac{3}{x} + e^{x} \right) \,d x$, (b) $\int (x^{2} + 1)^{2} \,d x$, (c) $\int \cos^{2} x \,d x$.
2. Evaluate by substitution (a) $\int x \sqrt{x^{2} + 4} \,d x$, (b) $\int e^{3 x + 1} \,d x$, (c) $\int \sin x \cos^{4} x \,d x$.
3. Evaluate by parts (a) $\int x \cos x \,d x$, (b) $\int x e^{2 x} \,d x$, (c) $\int x \ln x \,d x$.
4. Evaluate $\frac{\int (2 x + 3)}{(x - 1) (x + 2)} \,d x$.
5. Evaluate (a) $\int_{0}^{2} (3 x^{2} - 2 x) \,d x$, (b) $\int_{0}^{\frac{\pi}{4}} \sec^{2} x \,d x$, (c) $\frac{\int_{1}^{e} (\ln x)}{x} \,d x$.
6. Find the area enclosed by $y = x^{2}$ and $y = 4 x - x^{2}$.
7. Find the volume generated by revolving $y = x^{2}$ about the x-axis between $x = 1$ and $x = 2$.
8. Find the average value of $\sin x$ on $[0 ,\  \pi]$.
9. Does $\frac{\int_{1}^{\infty} 1}{\sqrt{x}} \,d x$ converge? Does $\frac{\int_{1}^{\infty} 1}{x^{\frac{3}{2}}} \,d x$?
10. If $F (x) = \int_{0}^{x} t e^{t} \,d t$ find $F' (x)$ and $F (1)$.
11. Find the surface area generated by rotating $y = 2 x$, $0 \le x \le 3$, about the x-axis.
12. Estimate $\int_{0}^{1} e^{-x^{2}} \,d x$ with $n = 4$ by the trapezoidal rule and Simpson's 1/3 rule.
13. Show that Simpson's rule with $n = 2$ is exact for $\int_{0}^{2} x^{3} \,d x$.
14. The depths (m) of a river at 2 m intervals across a 8 m channel are 0, 2, 3, 2.5, 1. Estimate the cross-sectional area by both rules.

::: note Answers and worked solutions
**1.** (a) $x^{4} - 3$ ln|x| + $e^{x} + C$. (b) $\frac{x^{5}}{5} + \frac{2 x^{3}}{3} + x + C$. (c) $\frac{x}{2} + \frac{\sin 2 x}{4} + C$.

**2.** (a) $u = x^{2} + 4$: $\frac{1}{3} (x^{2} + 4)^{\frac{3}{2}} + C$. (b) $\frac{1}{3} e^{3 x + 1} + C$. (c) $u = \cos x$: $- \frac{\cos^{5} x}{5} + C$.

**3.** (a) $x \sin x + \cos x + C$. (b) $\left( \frac{x}{2} \right) e^{2 x} - \frac{e^{2 x}}{4} + C$. (c) $\left( \frac{x^{2}}{2} \right) \ln x - \frac{x^{2}}{4} + C$.

**4.** $\frac{2 x + 3}{(x - 1) (x + 2)} = \frac{A}{x - 1} + \frac{B}{x + 2}$: $A = \frac{5}{3} ,\  B = \frac{1}{3}$. *∫* = **$\left( \frac{5}{3} \right)$ ln|x − 1| + $\left( \frac{1}{3} \right)$ ln|x + 2| + C**.

**5.** (a) $[x^{3} - x^{2}]_{0}^{2} = 8 - 4$ = **4**. (b) $\tan \left( \frac{\pi}{4} \right) - 0$ = **1**. (c) [ (ln x)²/2 ]₁^e = **$\frac{1}{2}$**.

**6.** Intersections: $x^{2} = 4 x - x^{2} \Rightarrow x = 0 ,\  2$. $A = \int_{0}^{2} (4 x - 2 x^{2}) \,d x = \left[ 2 x^{2} - \frac{2 x^{3}}{3} \right]_{0}^{2} = 8 - \frac{16}{3}$ = **$\frac{8}{3}$**.

**7.** $V = \pi \int_{1}^{2} x^{4} \,d x = \frac{\pi (32 - 1)}{5}$ = **$\frac{31 \pi}{5} \approx 19.48$**.

**8.** $\left( \frac{1}{\pi} \right) [- \cos x]_{0}^{\pi} = \frac{2}{\pi}$ ≈ **0.637**.

**9.** $\int_{1}^{\infty} x^{- \frac{1}{2}}$ diverges $\left( p = \frac{1}{2} \leq 1 \right)$. $\int_{1}^{\infty} x^{- \frac{3}{2}} = \left[ - 2 x^{- \frac{1}{2}} \right]_{1}^{\infty}$ = **2**, converges.

**10.** $F' (x) = x e^{x}$. $F (1) = \int_{0}^{1} t e^{t} \,d t = [(t - 1) e^{t}]_{0}^{1}$ = **1**.

**11.** $y' = 2$, so $S = 2 \pi \int_{0}^{3} 2 x \sqrt{5} \,d x = 4 \pi \sqrt{5} \cdot \frac{9}{2} = $ **$18 \pi \sqrt{5} \approx 126.4$** square units. (Cone check: $\pi r l$ with $r = 6$, $l = 3 \sqrt{5}$ gives the same.)

**12.** $h = 0.25$; ordinates $1, 0.939413, 0.778801, 0.569783, 0.367879$. Trapezoidal $= 0.125 [1.367879 + 2 (2.287997)] \approx$ **0.74298**. Simpson $= \frac{0.25}{3} [1.367879 + 4 (1.509196) + 2 (0.778801)] \approx$ **0.74686**. The true value is 0.746824, so Simpson is far closer.

**13.** $h = 1$, $y_0 = 0$, $y_1 = 1$, $y_2 = 8$. Simpson $= \frac{1}{3} [0 + 4 (1) + 8] = 4$, and $\int_{0}^{2} x^{3} \,d x = \frac{16}{4} = 4$. ∎ (The error term contains $f^{(4)}$, which is zero for a cubic.)

**14.** Trapezoidal: $\frac{2}{2} [0 + 1 + 2 (2 + 3 + 2.5)] = 16$ m². Simpson: $\frac{2}{3} [0 + 1 + 4 (2 + 2.5) + 2 (3)] = \frac{2}{3} \cdot 25 \approx$ **16.67 m²**.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q (5 marks). Evaluate $\int x e^{x} \,d x$ by parts and hence find $\int_{0}^{1} x e^{x} \,d x$.**

**Integration by parts** comes from the product rule: $\int u \,d v = u v - \int v \,d u$. The skill is to choose *u* so that $d u$ is simpler than *u*. The order of preference is *LIATE*: Logarithmic, Inverse trigonometric, Algebraic, Trigonometric, Exponential.

1. In $x e^{x}$ the algebraic factor *x* comes before the exponential, so let $u = x$ and $d v = e^{x} d x$.
2. Then $d u = d x$ and $v = e^{x}$.
3. Apply the formula: $\int x e^{x} \,d x = x e^{x} - \int e^{x} \,d x$.
4. The remaining integral is $e^{x}$, so $\int x e^{x} \,d x = x e^{x} - e^{x} + C$ = **$(x - 1) e^{x} + C$**.
5. Check by differentiating: $\frac{d}{d x} [(x - 1) e^{x}] = e^{x} + (x - 1) e^{x} = x e^{x}$ ✓.

For the definite integral use the Fundamental Theorem: $\int_{0}^{1} x e^{x} \,d x = [(x - 1) e^{x}]_{0}^{1} = (0) (e) - (- 1) (1)$ = **1**. The area under the curve $y = x e^{x}$ between $x = 0$ and $x = 1$ is exactly one square unit.

**Q (5 marks). Find the area between $y = x$ and $y = x^{2}$ and the volume generated when the curve $y = \sqrt{x} ,\  0 \leq x \leq 4$, is rotated about the x-axis.**

*Area (Figure $5.2 a ) . \ast$ The curves meet where $x = x^{2}$, that is $x = 0$ and $x = 1$. Between them the line is above the parabola (at $x = 0.5$: $0.5 > 0.25$). The area is the integral of (upper − lower): $\int_{0}^{1} (x - x^{2}) \,d x = \left[ \frac{x^{2}}{2} - \frac{x^{3}}{3} \right]_{0}^{1} = \frac{1}{2} - \frac{1}{3}$ = **$\frac{1}{6}$ square unit**.

*Volume (Figure $5.2 b ) . \ast$ A thin slice at position *x* is a disc of radius $y = \sqrt{x}$ and thickness $d x$, so its volume is $\pi y^{2} d x = \pi x d x$. Adding all slices from 0 to 4:

$V = \pi \int_{0}^{4} x \,d x = \pi \left[ \frac{x^{2}}{2} \right]_{0}^{4} = \pi \times 8$ = **$8 \pi \approx 25.13$ cubic units**.

*Remark.* The disc formula is $V = \pi \int y^{2} \,d x$. If the region lies between two curves a washer (a disc with a hole) is used: $V = \pi \int (R^{2} - r^{2}) \,d x$. Always sketch the region first and write which curve is on top.

**Q (10 marks). Define the definite integral through Riemann sums. State the Fundamental Theorem of Calculus. Explain the methods of integration (substitution, parts, partial fractions) with an example of each, and explain improper integrals.**

**Introduction.** Integration reverses differentiation and also measures accumulated quantities such as area, distance and volume. The **indefinite integral** $\int f \,d x$ is the family of antiderivatives $F (x) + C$, and the **definite integral** $\int_{a}^{b} f \,d x$ is a number, the signed area under the curve.

**Riemann sums (Figure 4.1).** Divide $[a ,\  b]$ into *n* strips of width $\Delta x = \frac{b - a}{n}$, build a rectangle of height $f (x_{i})$ on each, and add: $\sum f (x_{i}) \Delta x$. The definite integral is the limit of this sum as $n \to \infty$. For $f = x^{2}$ on [0, 2] the sums are 1.75 (left, $n = 4$), 3.75 (right, $n = 4$) and tend to **$\frac{8}{3}$**.

**Fundamental Theorem of Calculus.** (1) If $F (x) = \int_{a}^{x} f (t) \,d t$ then $F' (x) = f (x)$. (2) If $G' = f$ then $\int_{a}^{b} f \,d x = G (b) - G (a)$. Example: $\int_{0}^{2} x^{2} \,d x = \left[ \frac{x^{3}}{3} \right]_{0}^{2} = \frac{8}{3}$ ✓.

**Methods of integration.**

| Method | When used | Example | Result |
|---|---|---|---|
| Substitution | a function and its derivative appear | $\int 2 x \cos (x^{2}) \,d x ,\  u = x^{2}$ | $\sin (x^{2}) + C$ |
| By parts | product of different types | $\int x e^{x} \,d x ,\  u = x$ | $(x - 1) e^{x} + C$ |
| Partial fractions | rational function with factorable denominator | $\frac{\int (3 x + 5)}{(x + 1) (x + 2)} \,d x$ | 2 ln\|x + 1\| + ln\|x + 2\| + C |

For the last example write $\frac{3 x + 5}{(x + 1) (x + 2)} = \frac{A}{x + 1} + \frac{B}{x + 2}$. Then $3 x + 5 = A (x + 2) + B (x + 1)$; putting $x = - 1$ gives $A = 2$ and $x = - 2$ gives $B = 1$.

**Applications (Figure 4.2).** Area between curves is $\int ( \mathrm{upper}$ − lower)dx, volume of revolution is $\pi \int y^{2} \,d x$, and average value is $\left( \frac{1}{b - a} \right) \int f \,d x$.

**Improper integrals (Figure 4.3).** An integral with an infinite limit is defined by a limit: $\frac{\int_{1}^{\infty} d x}{x^{2}} = \lim_{b \to \infty} \left( 1 - \frac{1}{b} \right)$ = **1** (converges), but $\frac{\int_{1}^{\infty} d x}{x} = \lim \ln b = \infty$ (diverges). The p-test: $\frac{\int_{1}^{\infty} d x}{x^{p}}$ converges if and only if $p > 1$.

**Conclusion.** Integration accumulates small pieces into a total. The Fundamental Theorem makes it practical by connecting it with antiderivatives, and the three methods cover most examination problems.
