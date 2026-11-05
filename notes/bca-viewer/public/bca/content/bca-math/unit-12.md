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

## 12.2 Continuity

$f$ is continuous at $a$ if $\lim_{x\to a}f(x)=f(a)$. To make $f(x)=\frac{x^2-9}{x-3}$ continuous at 3, define $f(3)=6$ (the limit).

## 12.3 Derivatives, rules and standard results

| $f(x)$ | $f'(x)$ | $f(x)$ | $f'(x)$ |
|---|---|---|---|
| $x^n$ | $nx^{n-1}$ | $\sin x$ | $\cos x$ |
| constant | 0 | $\cos x$ | $-\sin x$ |
| $e^x$ | $e^x$ | $\tan x$ | $\sec^2x$ |
| $a^x$ | $a^x\ln a$ | $\ln x$ | $\frac{1}{x}$ |
| $\sqrt{x}$ | $\frac{1}{2\sqrt{x}}$ | $\frac{1}{x}$ | $-\frac{1}{x^2}$ |

Product: $(uv)'=u'v+uv'$. Quotient: $\left(\frac{u}{v}\right)'=\frac{u'v-uv'}{v^2}$. Chain: $\frac{d}{dx}f(g(x))=f'(g(x))g'(x)$. Example: $\frac{d}{dx}(x^2\cos x)=2x\cos x-x^2\sin x$.

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
