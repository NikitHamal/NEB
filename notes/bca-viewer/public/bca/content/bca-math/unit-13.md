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

## 13.2 Methods: substitution and integration by parts

- **Substitution**: put $u=g(x)$. In particular $\int\frac{f'(x)}{f(x)}dx=\ln|f(x)|+C$, so $\int\frac{2x}{x^2+1}dx=\ln(x^2+1)+C$.
- **By parts**: $\int u\,dv=uv-\int v\,du$, choosing $u$ in the order Inverse trig, Log, Algebraic, Trig, Exponential (ILATE). Example: $\int xe^x dx=(x-1)e^x+C$; $\int_1^e\ln x\,dx=1$.

## 13.3 Definite integrals and area

- $\int_a^bf\,dx=F(b)-F(a)$. Reversing limits changes the sign; $\int_a^bf=\int_a^cf+\int_c^bf$.
- Over $[-a,a]$: an odd function gives 0 ($\int_{-1}^1x^3dx=0$); an even function gives $2\int_0^a$.
- $\int_0^\pi\sin x\,dx=2$, $\int_0^{\pi/2}\cos x\,dx=1$.
- Area between $y=f(x)$, the $x$-axis and $x=a,b$ is $\int_a^b|f|dx$; between two curves, $\int_a^b(f-g)dx$ with $f\ge g$.

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
