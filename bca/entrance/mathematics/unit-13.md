---
subject: Mathematics
grade: BCA
unit: 13
title: Integration
hours: 3
area: Calculus
---

Integration questions are the easy half of calculus: a standard integral, a definite integral, an area or an integration by substitution or parts. Learn the table and the three rules, and be sure to add $+C$ for indefinite integrals.

::: key What the paper asks from this chapter
- **Standard integrals** and linearity.
- **Substitution** (including $\int\frac{f'}{f}dx=\ln|f|$) and **parts**.
- **Definite integrals** and their properties, **area** under a curve.
:::

## 13.1 Standard integrals and rules

| $f(x)$ | $\int f\,dx$ | $f(x)$ | $\int f\,dx$ |
|---|---|---|---|
| $x^n$ ($n\ne-1$) | $\frac{x^{n+1}}{n+1}+C$ | $\sin x$ | $-\cos x+C$ |
| $\frac{1}{x}$ | $\ln\lvert x\rvert+C$ | $\cos x$ | $\sin x+C$ |
| $e^x$ | $e^x+C$ | $\sec^2x$ | $\tan x+C$ |
| $a^x$ | $\frac{a^x}{\ln a}+C$ | $\frac{1}{1+x^2}$ | $\tan^{-1}x+C$ |
| $\sqrt{x}$ | $\frac{2}{3}x^{3/2}+C$ | $\frac{1}{\sqrt{1-x^2}}$ | $\sin^{-1}x+C$ |

Integrate term by term; constants pull out. $\int(ax+b)^n dx=\frac{(ax+b)^{n+1}}{a(n+1)}+C$ and $\int\frac{dx}{ax+b}=\frac{1}{a}\ln|ax+b|+C$.

```svgfig label="13.1" caption="Integration as a limit of sums, computed. The area under y = x^2 from 0 to 2 is exactly 8/3 = 2.667. With 4 strips the left-hand sum is 1.75 (too small, rectangles under the curve) and the right-hand sum is 3.75 (too big). The table shows both squeezing in on 2.667 as the strips get thinner: with 1000 strips they are 2.6627 and 2.6707."
fn = lambda x: x * x
def L(n): h = 2 / n; return sum(fn(i * h) for i in range(n)) * h
def R(n): h = 2 / n; return sum(fn((i + 1) * h) for i in range(n)) * h
assert (round(L(4), 4), round(R(4), 4)) == (1.75, 3.75) and round(L(1000), 4) == 2.6627 and round(R(1000), 4) == 2.6707 and abs(8 / 3 - L(100000)) < 1e-3
f = Fig(780, 320)
for k, (mode, col, nm) in enumerate([("left", "#bfdbfe", "left sum = 1.75"), ("right", "#fecaca", "right sum = 3.75")]):
    ax = Axes(f, 20 + k * 200, 24, 180, 200, (0, 2.2), (0, 4.4))
    ax.grid(1, 1, size=10); ax.axes("", "")
    ax.bars(fn, 0, 2, 4, mode=mode, fill=col, stroke=NAVY); ax.curve(fn, 0, 2.2, color=NAVY, sw=2.4)
    f.text(110 + k * 200, 248, nm, size=11, color=(NAVY if k == 0 else RED), bold=True)
f.text(210, 276, "4 strips under y = x^2 on [0, 2]; exact area = 8/3", size=10.5, color=SLATE)
f.text(210, 300, "left < 8/3 < right", size=11, color=TEAL, bold=True)
f.text(600, 26, "Squeezing in on 8/3 = 2.6667", size=11.5, color=NAVY, bold=True)
f.text(450, 54, "strips", size=10.5, color=SLATE, bold=True, anchor="start"); f.text(530, 54, "left sum", size=10.5, color=NAVY, bold=True, anchor="start"); f.text(640, 54, "right sum", size=10.5, color=RED, bold=True, anchor="start")
for j, n in enumerate([4, 10, 100, 1000]):
    y = 84 + j * 34
    f.text(450, y, str(n), size=11, color=SLATE, anchor="start", bold=True); f.text(530, y, "%.4f" % L(n), size=11, color=NAVY, anchor="start"); f.text(640, y, "%.4f" % R(n), size=11, color=RED, anchor="start")
f.text(600, 244, "definite integral = limit of the sums", size=11, color=TEAL, bold=True)
f.text(600, 268, "= F(2) - F(0) = 8/3 - 0, F = x^3/3", size=10.5, color=SLATE)
```

## 13.2 Methods: substitution and integration by parts

- **Substitution**: put $u=g(x)$. In particular $\int\frac{f'(x)}{f(x)}dx=\ln|f(x)|+C$, so $\int\frac{2x}{x^2+1}dx=\ln(x^2+1)+C$.
- **By parts**: $\int u\,dv=uv-\int v\,du$, choosing $u$ in the order Inverse trig, Log, Algebraic, Trig, Exponential (ILATE). Example: $\int xe^x dx=(x-1)e^x+C$; $\int_1^e\ln x\,dx=1$.

```svgfig label="13.2" caption="Two standard methods, each checked numerically in the cell. Substitution: for the integral of 2x cos(x^2) dx put u = x^2, du = 2x dx, giving sin(x^2) + C. By parts: the integral of x e^x dx = x e^x - e^x = (x - 1)e^x + C with u = x (algebraic before exponential, LIATE). Then the definite integral from 0 to 1 is [(x - 1)e^x] = 0 - (-1) = 1, the area drawn on the right."
import math
def nd(F, x, h=1e-6): return (F(x + h) - F(x - h)) / (2 * h)
for x in (0.3, 1.1, 2.0):
    assert abs(nd(lambda t: math.sin(t * t), x) - 2 * x * math.cos(x * x)) < 1e-5 and abs(nd(lambda t: (t - 1) * math.exp(t), x) - x * math.exp(x)) < 1e-5
n = 100000; val = sum(((i + 0.5) / n) * math.exp((i + 0.5) / n) for i in range(n)) / n; assert abs(val - 1) < 1e-6
f = Fig(780, 320)
f.box(20, 20, 350, 130, "", fill=SOFT, stroke="#cbd5e1", r=4); f.text(195, 40, "Substitution", size=11.5, color=NAVY, bold=True)
for j, t in enumerate(["integral of 2x cos(x^2) dx", "u = x^2,  du = 2x dx", "= integral of cos u du = sin u + C", "= sin(x^2) + C  (check: derivative 2x cos(x^2))"]):
    f.text(34, 66 + j * 22, t, size=10.5, color=(RED if j == 3 else SLATE), anchor="start", bold=(j == 3))
f.box(20, 164, 350, 150, "", fill=SOFT, stroke="#cbd5e1", r=4); f.text(195, 184, "Integration by parts", size=11.5, color=NAVY, bold=True)
for j, t in enumerate(["integral of u dv = uv - integral of v du", "x e^x: u = x, dv = e^x dx, v = e^x", "= x e^x - integral of e^x dx = (x - 1) e^x + C", "LIATE order for u: Log, Inverse, Algebraic,", "Trig, Exponential;  ln x: take u = ln x, dv = dx"]):
    f.text(34, 210 + j * 21, t, size=10.5, color=SLATE, anchor="start")
ax = Axes(f, 420, 24, 330, 250, (-0.2, 1.4), (-0.2, 4.5))
ax.grid(0.5, 1, size=10); ax.axes("x", "y")
ax.area(lambda x: x * math.exp(x), 0, 1, fill="#bbf7d0"); ax.curve(lambda x: x * math.exp(x), -0.2, 1.4, color=NAVY, sw=2.5)
f.text(ax.X(0.55), ax.Y(0.5), "area = 1", size=12, color=RED, bold=True); f.text(ax.X(0.2), ax.Y(3.6), "y = x e^x", size=11, color=NAVY, bold=True, anchor="start")
f.text(585, 300, "integral 0 to 1 of x e^x = [(x - 1) e^x] = 1", size=10.5, color=TEAL, bold=True)
```

## 13.3 Definite integrals and area

- $\int_a^bf\,dx=F(b)-F(a)$. Reversing limits changes the sign; $\int_a^bf=\int_a^cf+\int_c^bf$.
- Over $[-a,a]$: an odd function gives 0 ($\int_{-1}^1x^3dx=0$); an even function gives $2\int_0^a$.
- $\int_0^\pi\sin x\,dx=2$, $\int_0^{\pi/2}\cos x\,dx=1$.
- Area between $y=f(x)$, the $x$-axis and $x=a,b$ is $\int_a^b|f|dx$; between two curves, $\int_a^b(f-g)dx$ with $f\ge g$.

```photogrid label="13.1" cols="3" ratio="1.0" caption="From areas to integrals. (a) Archimedes (about 287-212 BC), here in a bronze statue at Berlin-Treptow, who found areas and volumes by slicing them into thin pieces. (b) Bernhard Riemann (1826-1866), who defined the definite integral as the limit of sums (Fig 13.1). (c) The Kaligandaki dam in Nepal: engineers integrate the pressure of water over the depth to find the force on the wall."
@ photo id="bcamath/archimedes" cap="Archimedes: slicing to find area"
focus 0.5 0.4
@ photo id="bcamath/riemann" cap="Riemann: the integral as a limit"
focus 0.5 0.3
@ photo id="bca104/kgdam" cap="Kaligandaki dam: force by integration"
focus 0.5 0.5
```

```svgfig label="13.3" caption="Area is not the same as the integral. (a) The area between y = x and y = x^2 on [0, 1] is the integral of (top - bottom) = 1/2 - 1/3 = 1/6 = 0.1667. (b) The integral of sin x from 0 to pi is 2, and from pi to 2 pi it is -2, so the SIGNED integral over a full period is 0, but the true area is |2| + |-2| = 4. Always split at the zeros."
import math
n = 100000
I1 = sum(((i + 0.5) / n - ((i + 0.5) / n) ** 2) for i in range(n)) / n; assert abs(I1 - 1 / 6) < 1e-8
s1 = sum(math.sin(math.pi * (i + 0.5) / n) for i in range(n)) * math.pi / n; assert abs(s1 - 2) < 1e-6
s2 = -s1; assert abs((s1 + s2)) < 1e-9 and abs(abs(s1) + abs(s2) - 4) < 1e-6 and abs(math.cos(0) - math.cos(math.pi) - 2) < 1e-12
f = Fig(780, 320)
ax = Axes(f, 30, 24, 250, 240, (-0.2, 1.3), (-0.2, 1.3))
ax.grid(0.5, 0.5, size=10); ax.axes("x", "y")
ax.area(lambda x: x, 0, 1, fill="#bbf7d0", fn2=lambda x: x * x); ax.curve(lambda x: x, -0.1, 1.2, color=NAVY, sw=2.4); ax.curve(lambda x: x * x, -0.1, 1.1, color=RED, sw=2.4)
f.text(ax.X(0.05), ax.Y(1.1), "y = x", size=11, color=NAVY, bold=True, anchor="start"); f.text(ax.X(0.75), ax.Y(0.32), "y = x^2", size=11, color=RED, bold=True, anchor="start"); f.text(ax.X(0.5), ax.Y(0.38), "1/6", size=12, color=TEAL, bold=True)
f.text(160, 296, "area = integral (x - x^2) dx = 1/2 - 1/3 = 1/6", size=10.5, color=NAVY, bold=True)
ax2 = Axes(f, 330, 24, 300, 240, (0, 6.5), (-1.5, 1.5))
ax2.grid(1.5708, 1, labels=False); ax2.axes("", "")
ax2.area(lambda x: math.sin(x), 0, math.pi, fill="#bbf7d0"); ax2.area(lambda x: math.sin(x), math.pi, 2 * math.pi, fill="#fecaca"); ax2.curve(math.sin, 0, 6.5, color=NAVY, sw=2.4)
for v, t in [(0, "0"), (math.pi, "pi"), (2 * math.pi, "2 pi")]: f.text(ax2.X(v), 280, t, size=10.5, color=SLATE, bold=True)
f.text(ax2.X(1.57), ax2.Y(0.4), "+2", size=12, color=TEAL, bold=True); f.text(ax2.X(4.7), ax2.Y(-0.4), "-2", size=12, color=RED, bold=True)
f.text(480, 300, "signed integral 0, true area 2 + 2 = 4", size=10.5, color=NAVY, bold=True)
f.text(715, 40, "Properties", size=10.5, color=NAVY, bold=True)
for j, t in enumerate(["swap limits: sign flips", "odd f: integral over (-a, a) = 0", "even f: twice that over (0, a)", "integral(0..a) f(x) = integral(0..a) f(a - x)"]):
    f.text(655, 70 + j * 36, t, size=9.5, color=SLATE, anchor="start")
```

## 13.4 Eight traps in integration

Integration questions are checked by differentiating, so most errors are about a missing factor or a forgotten limit. These eight traps are the ones that cost marks in the model paper.

1. **An indefinite integral needs $+C$; a definite integral does not.** $\int(3x^2+2x+1)\,dx=x^3+x^2+x+C$, but $\int_0^2(3x^2+2x+1)\,dx=8+4+2=14$ with no constant. Examiners often put an option with and without $C$. Always check by differentiating your answer.
2. **The power rule fails at $n=-1$.** $\int x^n\,dx=\frac{x^{n+1}}{n+1}$ for $n\ne-1$, and $\int\frac1x\,dx=\ln|x|+C$ (note the absolute value). The integral of a constant $k$ is $kx$. Do not forget to add 1 to the power before dividing.
3. **Divide by the inner derivative.** $\int\cos2x\,dx=\frac12\sin2x+C$ and $\int e^{ax}dx=\frac{e^{ax}}{a}+C$. If you leave out the factor $\frac1a$ your derivative check gives $2\cos2x$, not $\cos2x$. This is the reverse of the chain rule.
4. **In substitution, change everything, including the limits.** Put $u=g(x)$, replace $du=g'(x)\,dx$ and rewrite the limits in $u$, as for $\int2x\cos(x^2)\,dx=\sin(x^2)+C$ (Fig 13.2). If you keep the old limits with the new variable the value is wrong. The integrand must contain $g'(x)$ as a factor.
5. **By parts: $\int u\,dv=uv-\int v\,du$, with $u$ chosen by LIATE.** For $\int xe^x\,dx$ take $u=x$ and get $(x-1)e^x+C$. For $\int\ln x\,dx$ take $u=\ln x$, $dv=dx$ to get $x\ln x-x+C$. Choosing $u=e^x$ makes the integral harder.
6. **A definite integral is $F(b)-F(a)$.** Swapping the limits changes the sign. Split at a point where the function is undefined or changes rule. For an odd function $\int_{-a}^{a}f\,dx=0$, and $\int_{-1}^{1}x^2dx=\frac23$ for an even one.
7. **Area is not the same as the signed integral.** $\int_0^{2\pi}\sin x\,dx=0$ but the area between the curve and the axis is 4 (Fig 13.3). Split at the zeros and add the absolute values. The area between two curves is $\int(\text{upper}-\text{lower})\,dx$.
8. **Memorise the standard forms and verify by differentiation.** $\int\sec^2x\,dx=\tan x$, $\int\frac{dx}{1+x^2}=\tan^{-1}x$, $\int\tan x\,dx=\ln|\sec x|$, $\int a^xdx=\frac{a^x}{\ln a}$ and $\int e^xdx=e^x$. The Riemann sum picture (Fig 13.1) is why the integral of $x^2$ on $[0,2]$ is $\frac83$.

### 13.4.1 Worked checks

**Q. Evaluate $\int(3x^2+2x+1)\,dx$ and $\int_0^2(3x^2+2x+1)\,dx$.**

**Answer.** The indefinite integral is $x^3+x^2+x+C$. The definite integral is $[x^3+x^2+x]_0^2=8+4+2-0=14$. The constant cancels in the definite case.

**Q. Find $\int xe^x\,dx$ and $\int_0^1xe^x\,dx$.**

**Answer.** By parts, $\int xe^xdx=xe^x-e^x+C=(x-1)e^x+C$. Then $\int_0^1=[(x-1)e^x]_0^1=0-(-1)=1$. Differentiating $(x-1)e^x$ gives $xe^x$, which confirms the result.

**Q. Find the area enclosed by $y=x$ and $y=x^2$.**

**Answer.** They meet where $x=x^2$, at $x=0$ and $x=1$, and $y=x$ is above. Area $=\int_0^1(x-x^2)\,dx=\frac12-\frac13=\frac16$. This is the shaded region in Fig 13.3.

## Formula and fact sheet

| Item | Result |
|---|---|
| Power rule | $\int x^ndx=\frac{x^{n+1}}{n+1}+C$ |
| Log rule | $\int\frac{f'}{f}dx=\ln\lvert f\rvert+C$ |
| Parts | $uv-\int v\,du$ |
| Definite | $F(b)-F(a)$ |

## Chapter summary

- Add $+C$ to every indefinite integral and omit it in definite ones.
- $\int\frac{1}{x}dx=\ln|x|$, not $x^0$.
- An odd function over a symmetric interval integrates to zero.
- Use parts when a product has a log, inverse-trig or $x\times e^x$.
- Area under $y=x^2$ from 0 to 3 is 9.

## Practice questions

**Set A — Recall (20 questions)**

1. $\int x^2\,dx$ equals
   (a) $x^3+C$ (b) $\frac{x^3}{3}+C$ (c) $2x+C$ (d) $\frac{x^2}{2}+C$
2. $\int\frac{1}{x}\,dx$ equals
   (a) $x^0+C$ (b) $-\frac{1}{x^2}+C$ (c) $\frac{1}{x^2}+C$ (d) $\ln|x|+C$
3. $\int\cos x\,dx$ equals
   (a) $\sin x+C$ (b) $-\sin x+C$ (c) $-\cos x+C$ (d) $\cos x+C$
4. $\int e^x\,dx$ equals
   (a) $xe^x+C$ (b) $e^{x+1}+C$ (c) $e^x+C$ (d) $\ln x+C$
5. $\int\sin x\,dx$ equals
   (a) $\cos x+C$ (b) $-\cos x+C$ (c) $\sin x+C$ (d) $-\sin x+C$
6. $\int_0^1x\,dx$ equals
   (a) 1 (b) 0 (c) 2 (d) $\frac{1}{2}$
7. $\int\sec^2x\,dx$ equals
   (a) $\sec x\tan x+C$ (b) $\cot x+C$ (c) $\tan x+C$ (d) $-\tan x+C$
8. The integral of zero is
   (a) a constant (b) 0 (c) $x$ (d) 1
9. $\int\frac{1}{1+x^2}\,dx$ equals
   (a) $\ln(1+x^2)+C$ (b) $\sin^{-1}x+C$ (c) $\frac{1}{x}+C$ (d) $\tan^{-1}x+C$
10. $\int_0^23\,dx$ equals
    (a) 3 (b) 6 (c) 9 (d) 2
11. $\int(2x+3)\,dx$ equals
    (a) $2x^2+3x+C$ (b) $x^2+3+C$ (c) $x^2+3x+C$ (d) $2+C$
12. $\int_0^\pi\sin x\,dx$ equals
    (a) 2 (b) 0 (c) 1 (d) $-2$
13. $\int x^{-2}\,dx$ equals
    (a) $\frac{1}{x}+C$ (b) $-\frac{1}{x}+C$ (c) $-2x^{-3}+C$ (d) $\ln x+C$
14. $\int a^x\,dx$ equals
    (a) $a^x+C$ (b) $a^x\ln a+C$ (c) $xa^{x-1}+C$ (d) $\frac{a^x}{\ln a}+C$
15. $\int_{-1}^{1}x^3\,dx$ equals
    (a) 0 (b) $\frac{1}{2}$ (c) 2 (d) $\frac{1}{4}$
16. $\int\sqrt{x}\,dx$ equals
    (a) $\frac{1}{2}x^{-1/2}+C$ (b) $x^{3/2}+C$ (c) $\frac{2}{3}x^{3/2}+C$ (d) $2\sqrt{x}+C$
17. $\int_1^e\frac{1}{x}\,dx$ equals
    (a) $e$ (b) 1 (c) 0 (d) $e-1$
18. $\int\frac{f'(x)}{f(x)}\,dx$ equals
    (a) $f(x)^2+C$ (b) $f'(x)+C$ (c) $\frac{1}{f(x)}+C$ (d) $\ln|f(x)|+C$
19. $\int_0^{\pi/2}\cos x\,dx$ equals
    (a) 1 (b) 0 (c) 2 (d) $-1$
20. The area under $y=x$ from $x=0$ to $x=4$ is
    (a) 4 (b) 16 (c) 8 (d) 2

::: note Answers and explanations — Set A
**1.** (b) — raise the power and divide by it.
**2.** (d) — the exception to the power rule.
**3.** (a) — reverse of differentiating sin.
**4.** (c) — eˣ is its own integral.
**5.** (b) — mind the minus sign.
**6.** (d) — [x²/2] from 0 to 1.
**7.** (c) — d/dx tan x = sec² x.
**8.** (a) — an arbitrary constant.
**9.** (d) — standard result.
**10.** (b) — 3 × 2.
**11.** (c) — x² + 3x + C.
**12.** (a) — [−cos x] = 1 + 1 = 2.
**13.** (b) — x⁻¹/(−1).
**14.** (d) — divide by ln a.
**15.** (a) — odd function over [−1, 1].
**16.** (c) — x^(3/2)/(3/2).
**17.** (b) — ln e − ln 1.
**18.** (d) — substitution u = f(x).
**19.** (a) — sin(π/2) − sin 0.
**20.** (c) — triangle: ½ × 4 × 4 = 8.
:::

**Set B — Understanding (12 questions)**

1. $\int(3x^2+2x+1)\,dx$ equals
   (a) $6x+2+C$ (b) $x^3+x^2+C$ (c) $3x^3+x^2+x+C$ (d) $x^3+x^2+x+C$
2. $\int_1^22x\,dx$ equals
   (a) 3 (b) 4 (c) 2 (d) 1
3. $\int\frac{2x}{x^2+1}\,dx$ equals
   (a) $2\ln x+C$ (b) $x^2+1+C$ (c) $\ln(x^2+1)+C$ (d) $\tan^{-1}x+C$
4. $\int_0^1e^x\,dx$ equals
   (a) $e$ (b) $e-1$ (c) 1 (d) $e+1$
5. $\int xe^x\,dx$ equals
   (a) $(x-1)e^x+C$ (b) $(x+1)e^x+C$ (c) $xe^x+C$ (d) $\frac{e^x}{2}+C$
6. The area bounded by $y=x^2$, the $x$-axis and $x=3$ is
   (a) 27 (b) 3 (c) 6 (d) 9
7. $\int_0^2x^2\,dx$ equals
   (a) 4 (b) $\frac{8}{3}$ (c) $\frac{2}{3}$ (d) 8
8. $\int\cos2x\,dx$ equals
   (a) $\sin2x+C$ (b) $2\sin2x+C$ (c) $\frac{\sin2x}{2}+C$ (d) $-\frac{\sin2x}{2}+C$
9. $\int_{-2}^{2}x^2\,dx$ equals
   (a) $\frac{16}{3}$ (b) 0 (c) $\frac{8}{3}$ (d) 8
10. $\int\frac{dx}{2x+3}$ equals
    (a) $\ln|2x+3|+C$ (b) $2\ln|2x+3|+C$ (c) $-\frac{1}{(2x+3)^2}+C$ (d) $\frac{1}{2}\ln|2x+3|+C$
11. $\int_0^{\pi/4}\sec^2x\,dx$ equals
    (a) 0 (b) 1 (c) $\sqrt{2}$ (d) $\frac{\pi}{4}$
12. The area between $y=x$ and $y=x^2$ from 0 to 1 is
    (a) $\frac{1}{2}$ (b) $\frac{1}{3}$ (c) $\frac{1}{6}$ (d) $\frac{1}{12}$

::: note Answers and explanations — Set B
**1.** (d) — integrate each term; (a) is the derivative.
**2.** (a) — [x²] from 1 to 2 = 4 − 1.
**3.** (c) — numerator is the derivative of the denominator.
**4.** (b) — e − 1.
**5.** (a) — by parts: xeˣ − eˣ.
**6.** (d) — 27/3.
**7.** (b) — 8/3.
**8.** (c) — divide by the inner coefficient 2.
**9.** (a) — 2 × (8/3).
**10.** (d) — remember the 1/2.
**11.** (b) — tan(π/4) − tan 0.
**12.** (c) — ½ − ⅓ = ⅙.
:::

**Set C — Application (8 questions)**

1. $\int_0^1(x+1)^2\,dx$ equals
   (a) 3 (b) $\frac{7}{3}$ (c) $\frac{4}{3}$ (d) $\frac{1}{3}$
2. $\int_0^{\pi/2}\sin x\cos x\,dx$ equals
   (a) 1 (b) $\frac{1}{4}$ (c) 0 (d) $\frac{1}{2}$
3. $\int_1^e\ln x\,dx$ equals
   (a) 1 (b) $e$ (c) $e-1$ (d) 0
4. $\int_0^1\frac{dx}{\sqrt{1-x^2}}$ equals
   (a) 1 (b) $\pi$ (c) $\frac{\pi}{2}$ (d) $\frac{\pi}{4}$
5. The area under $y=2x$ from $x=0$ to $x=3$ is
   (a) 6 (b) 9 (c) 3 (d) 18
6. $\int\frac{x^2+1}{x}\,dx$ equals
   (a) $x^2+\ln|x|+C$ (b) $2x-\frac{1}{x^2}+C$ (c) $\frac{x^2}{2}+C$ (d) $\frac{x^2}{2}+\ln|x|+C$
7. If $\int_0^ax\,dx=8$, then $a$ is
   (a) 2 (b) 8 (c) 4 (d) 16
8. The area enclosed by $y=4-x^2$ and the $x$-axis is
   (a) $\frac{32}{3}$ (b) $\frac{16}{3}$ (c) 8 (d) 16

::: note Answers and explanations — Set C
**1.** (b) — [(x + 1)³/3] = (8 − 1)/3.
**2.** (d) — ½ ∫ sin 2x = ½ [−cos 2x / 2] = ½.
**3.** (a) — [x ln x − x] from 1 to e = 0 − (−1).
**4.** (c) — sin⁻¹ 1 − sin⁻¹ 0.
**5.** (b) — triangle: ½ × 3 × 6.
**6.** (d) — x + 1/x integrates to x²/2 + ln|x|.
**7.** (c) — a²/2 = 8.
**8.** (a) — [4x − x³/3] from −2 to 2 = 32/3.
:::
