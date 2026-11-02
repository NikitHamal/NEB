---
subject: Mathematics
grade: IOE
unit: 5
title: Calculus
hours: 8
area: Mathematics
---

Calculus is, with algebra, the heaviest block of the paper (our estimate: about **8 questions**). The official booklet's model questions include a hyperbolic-inverse derivative and a first-order linear differential equation, so the syllabus is read broadly: standard limits, derivatives of inverse and hyperbolic functions, tangent / rate / extremum problems, a definite integral or an area, and a first-order differential equation. Speed comes from knowing the standard results cold.

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
