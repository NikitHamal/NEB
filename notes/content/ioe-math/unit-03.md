---
subject: Mathematics
grade: IOE
unit: 3
title: Trigonometry
hours: 4
area: Mathematics
---

Trigonometry carries about **4 questions** (our estimate). Three kinds dominate: a general solution or a count of solutions in $[0,2\pi]$; an inverse-trigonometric identity or principal value; and a triangle question (sine rule, cosine rule, area, inradius, circumradius). All three are formula-driven, and the Section B versions simply chain two formulas.

::: key What the paper asks from this chapter
- General solutions: $\sin\theta=\sin\alpha\Rightarrow\theta=n\pi+(-1)^n\alpha$; $\cos\theta=\cos\alpha\Rightarrow\theta=2n\pi\pm\alpha$; $\tan\theta=\tan\alpha\Rightarrow\theta=n\pi+\alpha$.
- $a\sin\theta+b\cos\theta=c$ has a solution only if $|c|\le\sqrt{a^2+b^2}$.
- Principal-value ranges of $\sin^{-1},\cos^{-1},\tan^{-1}$ and $\sin^{-1}x+\cos^{-1}x=\pi/2$.
- $\tan^{-1}x+\tan^{-1}y=\tan^{-1}\frac{x+y}{1-xy}$ (watch the quadrant when $xy>1$).
- Triangle: $\frac{a}{\sin A}=2R$, cosine rule, $\Delta=\sqrt{s(s-a)(s-b)(s-c)}$, $r=\Delta/s$, $R=abc/4\Delta$.
:::

## 3.1 Trigonometric equations and general values

Principal solutions lie in $[0,2\pi)$; the **general solution** adds all periods.

| Equation | General solution |
|---|---|
| $\sin\theta=0$ / $\cos\theta=0$ / $\tan\theta=0$ | $n\pi$ / $(2n+1)\frac{\pi}{2}$ / $n\pi$ |
| $\sin\theta=\sin\alpha$ | $n\pi+(-1)^n\alpha$ |
| $\cos\theta=\cos\alpha$ | $2n\pi\pm\alpha$ |
| $\tan\theta=\tan\alpha$ | $n\pi+\alpha$ |
| $\sin^2\theta=\sin^2\alpha$ (also $\cos^2$, $\tan^2$) | $n\pi\pm\alpha$ |

**Method.** Reduce to one function (use $\sin^2=1-\cos^2$ or divide by $\cos^2$), factorise, solve each factor. Then count solutions in the given interval. For $a\sin\theta+b\cos\theta=c$ write $a=r\cos\phi$, $b=r\sin\phi$ with $r=\sqrt{a^2+b^2}$ to get $r\sin(\theta+\phi)=c$; the maximum of the left side is $r$.

::: example Quadratic in $\sin x$
**Problem.** Number of solutions of $2\sin^2x-3\sin x+1=0$ in $[0,2\pi]$.

**Solution.** $(2\sin x-1)(\sin x-1)=0$: $\sin x=\tfrac{1}{2}$ gives $\pi/6,5\pi/6$; $\sin x=1$ gives $\pi/2$. Three solutions.
:::

::: caution
When you divide both sides by a trigonometric factor you can lose its zeros: factorise instead. After squaring, check for extra roots.
:::

## 3.2 Inverse trigonometric functions, principal value

| Function | Domain | Principal range |
|---|---|---|
| $\sin^{-1}x$ | $[-1,1]$ | $[-\frac{\pi}{2},\frac{\pi}{2}]$ |
| $\cos^{-1}x$ | $[-1,1]$ | $[0,\pi]$ |
| $\tan^{-1}x$ | $\mathrm{R}$ | $(-\frac{\pi}{2},\frac{\pi}{2})$ |
| $\cot^{-1}x$ | $\mathrm{R}$ | $(0,\pi)$ |
| $\sec^{-1}x$ | $|x|\ge1$ | $[0,\pi]-\{\frac{\pi}{2}\}$ |
| $\csc^{-1}x$ | $|x|\ge1$ | $[-\frac{\pi}{2},\frac{\pi}{2}]-\{0\}$ |

**Identities.** $\sin^{-1}x+\cos^{-1}x=\frac{\pi}{2}$; $\tan^{-1}x+\cot^{-1}x=\frac{\pi}{2}$; $\sin^{-1}(-x)=-\sin^{-1}x$, $\cos^{-1}(-x)=\pi-\cos^{-1}x$; $\tan^{-1}x+\tan^{-1}\frac{1}{x}=\frac{\pi}{2}$ for $x>0$. $2\tan^{-1}x=\sin^{-1}\frac{2x}{1+x^2}$ ($|x|\le1$).

$$\tan^{-1}x\pm\tan^{-1}y=\tan^{-1}\frac{x\pm y}{1\mp xy}$$
valid when $xy<1$ (for $+$); if $x,y>0$ and $xy>1$ add $\pi$. Example: $\tan^{-1}1+\tan^{-1}2+\tan^{-1}3=\pi$.

**$\sin(\sin^{-1}x)=x$ always (for $|x|\le1$), but $\sin^{-1}(\sin x)=x$ only on $[-\frac{\pi}{2},\frac{\pi}{2}]$**: $\sin^{-1}\sin\frac{5\pi}{6}=\frac{\pi}{6}$. For $\cos(\sin^{-1}\frac{3}{5})$ draw the 3-4-5 triangle: $\frac{4}{5}$.

## 3.3 Properties of triangles, in-centre, ortho-centre and circum-centre, solution of triangles

With $s=\frac{a+b+c}{2}$ and area $\Delta$:
- **Sine rule** $\dfrac{a}{\sin A}=\dfrac{b}{\sin B}=\dfrac{c}{\sin C}=2R$.
- **Cosine rule** $\cos A=\dfrac{b^2+c^2-a^2}{2bc}$, $a^2=b^2+c^2-2bc\cos A$.
- **Projection** $a=b\cos C+c\cos B$. **Tangent rule** $\tan\frac{A-B}{2}=\frac{a-b}{a+b}\cot\frac{C}{2}$.
- **Half angles** $\sin\frac{A}{2}=\sqrt{\dfrac{(s-b)(s-c)}{bc}}$, $\cos\frac{A}{2}=\sqrt{\dfrac{s(s-a)}{bc}}$, $\tan\frac{A}{2}=\dfrac{\Delta}{s(s-a)}=\dfrac{r}{s-a}$.
- **Area** $\Delta=\frac{1}{2}ab\sin C=\sqrt{s(s-a)(s-b)(s-c)}$.
- **Circumradius** $R=\dfrac{abc}{4\Delta}$; **inradius** $r=\dfrac{\Delta}{s}=4R\sin\frac{A}{2}\sin\frac{B}{2}\sin\frac{C}{2}$; **exradius** $r_1=\dfrac{\Delta}{s-a}$.
- $\dfrac{1}{r}=\dfrac{1}{r_1}+\dfrac{1}{r_2}+\dfrac{1}{r_3}$, $r_1r_2+r_2r_3+r_3r_1=s^2$.

**Centres.** Circumcentre: perpendicular bisectors meet (equidistant from vertices; in a right triangle it is the midpoint of the hypotenuse, so $R=c/2$). In-centre: angle bisectors meet, at distance $r$ from every side. Orthocentre: altitudes meet; its distance from vertex $A$ is $2R\cos A$. Centroid divides each median 2 : 1.

**Solving triangles.** SSS: cosine rule. SAS: cosine rule then sine rule. ASA: third angle and sine rule. **SSA** is ambiguous: with $A$ acute and $a<b$, there are two triangles if $a>b\sin A$, one right triangle if $a=b\sin A$, none if $a<b\sin A$.

## Formula and fact sheet

| Topic | Result |
|---|---|
| $\sin\theta=\sin\alpha$ | $\theta=n\pi+(-1)^n\alpha$ |
| $\cos\theta=\cos\alpha$ | $\theta=2n\pi\pm\alpha$ |
| max of $a\sin\theta+b\cos\theta$ | $\sqrt{a^2+b^2}$ |
| $\sin^{-1}x+\cos^{-1}x$ | $\pi/2$ |
| $\tan^{-1}x+\tan^{-1}y$ | $\tan^{-1}\frac{x+y}{1-xy}$ |
| $2R$ | $a/\sin A$ |
| $\Delta$ (Heron) | $\sqrt{s(s-a)(s-b)(s-c)}$ |
| $r$, $R$ | $\Delta/s$, $abc/4\Delta$ |

## Chapter summary

- Reduce to one trig function, factorise, then write the general solution of each factor.
- $|c|>\sqrt{a^2+b^2}$ means no solution to $a\sin\theta+b\cos\theta=c$.
- Know the three principal ranges; $\sin^{-1}(\sin x)$ folds $x$ into $[-\pi/2,\pi/2]$.
- For two triangle quantities, find $\Delta$ first (Heron), then $r=\Delta/s$ or $R=abc/4\Delta$.
- A right triangle has $R=$ half the hypotenuse.

## Practice questions

**Set A — Recall (10 questions)**

1. The general solution of $\sin\theta=0$ is
   (a) $2n\pi$ (b) $n\pi$ (c) $(2n+1)\pi/2$ (d) $n\pi/2$
2. The principal value of $\sin^{-1}\frac{1}{2}$ is
   (a) $\pi/3$ (b) $\pi/4$ (c) $\pi/6$ (d) $5\pi/6$
3. The principal range of $\cos^{-1}x$ is
   (a) $[0,\pi]$ (b) $[-\pi/2,\pi/2]$ (c) $(0,\pi)$ (d) $[0,2\pi]$
4. The value of $\tan^{-1}1+\tan^{-1}2+\tan^{-1}3$ is
   (a) $\pi/2$ (b) $3\pi/4$ (c) $2\pi$ (d) $\pi$
5. In a triangle with $a=6$ and $A=30^\circ$, the circumradius $R$ is
   (a) 3 (b) 12 (c) 6 (d) $6\sqrt{3}$
6. The largest angle of the triangle with sides 3, 5, 7 is
   (a) $90^\circ$ (b) $120^\circ$ (c) $135^\circ$ (d) $150^\circ$
7. The area of the triangle with sides 13, 14, 15 is
   (a) 84 (b) 90 (c) 91 (d) 105
8. The number of solutions of $\sin x=\frac{1}{2}$ in $[0,2\pi]$ is
   (a) 1 (b) 3 (c) 4 (d) 2
9. The value of $\cos\big(\sin^{-1}\frac{3}{5}\big)$ is
   (a) $3/4$ (b) $5/4$ (c) $4/5$ (d) $3/5$
10. The inradius of the 3-4-5 right triangle is
    (a) 1 (b) 2 (c) 1.5 (d) 3

::: note Answers and explanations — Set A
**1.** (b) — $\sin\theta=0$ at every multiple of $\pi$.
**2.** (c) — $\sin\frac{\pi}{6}=\frac{1}{2}$ and $\frac{\pi}{6}\in[-\frac{\pi}{2},\frac{\pi}{2}]$; $5\pi/6$ is outside the principal range.
**3.** (a) — $[0,\pi]$; $[-\pi/2,\pi/2]$ is for $\sin^{-1}$.
**4.** (d) — $\tan^{-1}1+\tan^{-1}2=\pi-\tan^{-1}3$ (since $xy=2>1$), so the sum is $\pi$.
**5.** (c) — $2R=\frac{a}{\sin A}=\frac{6}{1/2}=12$, so $R=6$.
**6.** (b) — $\cos C=\frac{9+25-49}{30}=-\frac{1}{2}$, $C=120^\circ$.
**7.** (a) — $s=21$: $\sqrt{21\cdot8\cdot7\cdot6}=\sqrt{7056}=84$.
**8.** (d) — $x=\pi/6$ and $5\pi/6$.
**9.** (c) — draw the 3-4-5 triangle: adjacent side 4, hypotenuse 5.
**10.** (a) — $\Delta=6$, $s=6$, $r=\Delta/s=1$.
:::

**Set B — Understanding (8 questions)**

1. The general solution of $\tan\theta=\sqrt{3}$ is
   (a) $n\pi+\pi/6$ (b) $n\pi+\pi/3$ (c) $2n\pi+\pi/3$ (d) $n\pi\pm\pi/3$
2. The general solution of $\cos2\theta=\cos\theta$ is
   (a) $n\pi/3$ (b) $n\pi$ (c) $2n\pi/3$ (d) $2n\pi$
3. The value of $\sin^{-1}\big(\sin\frac{5\pi}{6}\big)$ is
   (a) $5\pi/6$ (b) $-\pi/6$ (c) $\pi/3$ (d) $\pi/6$
4. In a triangle $a=\sqrt{3}$, $b=1$, $c=2$. The angle $C$ is
   (a) $30^\circ$ (b) $45^\circ$ (c) $60^\circ$ (d) $90^\circ$
5. The value of $\tan^{-1}\frac{1}{2}+\tan^{-1}\frac{1}{3}$ is
   (a) $\pi/4$ (b) $\pi/2$ (c) $\pi/3$ (d) $\pi/6$
6. If the sides of a triangle are in the ratio $2:3:4$, the cosine of the largest angle is
   (a) $1/4$ (b) $11/16$ (c) $-1/4$ (d) $-11/16$
7. The circumradius of the triangle with sides 5, 12, 13 is
   (a) 5 (b) 6.5 (c) 6 (d) 7.5
8. The number of real solutions of $3\sin x+4\cos x=6$ is
   (a) 0 (b) 1 (c) 2 (d) infinite

::: note Answers and explanations — Set B
**1.** (b) — $\tan\frac{\pi}{3}=\sqrt{3}$; the general form is $n\pi+\alpha$ (not $2n\pi\pm\alpha$, which is for cosine).
**2.** (c) — $2\theta=2n\pi\pm\theta$ gives $\theta=2n\pi$ or $\theta=\frac{2n\pi}{3}$; the first set is contained in the second.
**3.** (d) — $\sin\frac{5\pi}{6}=\frac{1}{2}$ and the principal value of $\sin^{-1}\frac{1}{2}$ is $\frac{\pi}{6}$.
**4.** (d) — $\cos C=\frac{3+1-4}{2\sqrt{3}}=0$. Indeed $a^2+b^2=c^2$.
**5.** (a) — $\frac{\frac{1}{2}+\frac{1}{3}}{1-\frac{1}{6}}=\frac{5/6}{5/6}=1$, so $\frac{\pi}{4}$.
**6.** (c) — $\cos C=\frac{4+9-16}{12}=-\frac{1}{4}$.
**7.** (b) — a right triangle: $R=\frac{13}{2}$.
**8.** (a) — the maximum of $3\sin x+4\cos x$ is $\sqrt{9+16}=5<6$.
:::

**Set C — Application (6 questions)**

1. The number of solutions of $2\sin^2x-3\sin x+1=0$ in $[0,2\pi]$ is
   (a) 2 (b) 3 (c) 4 (d) 1
2. The value of $\sin^{-1}\frac{3}{5}+\sin^{-1}\frac{4}{5}$ is
   (a) $\pi/2$ (b) $\pi$ (c) $\pi/3$ (d) $3\pi/4$
3. The inradius of the triangle with sides 9, 10, 17 is
   (a) 3 (b) 1.5 (c) 4 (d) 2
4. The value of $\sin\big(2\tan^{-1}\frac{1}{2}\big)$ is
   (a) $3/5$ (b) $2/5$ (c) $4/5$ (d) $5/4$
5. The smallest positive $x$ with $\sqrt{3}\cos x+\sin x=2$ is
   (a) $\pi/3$ (b) $\pi/2$ (c) $\pi/4$ (d) $\pi/6$
6. In a triangle $a=b=2$ and $C=120^\circ$. The side $c$ is
   (a) $2\sqrt{2}$ (b) 4 (c) $2\sqrt{3}$ (d) 8

::: note Answers and explanations — Set C
**1.** (b) — factorise to $(2\sin x-1)(\sin x-1)=0$: $\frac{\pi}{6},\frac{5\pi}{6},\frac{\pi}{2}$.
**2.** (a) — $\sin^{-1}\frac{4}{5}=\cos^{-1}\frac{3}{5}$, and $\sin^{-1}u+\cos^{-1}u=\frac{\pi}{2}$.
**3.** (d) — $s=18$, $\Delta=\sqrt{18\cdot9\cdot8\cdot1}=36$, $r=36/18=2$.
**4.** (c) — $\sin2\theta=\frac{2\tan\theta}{1+\tan^2\theta}=\frac{1}{5/4}=\frac{4}{5}$.
**5.** (d) — $\sqrt{3}\cos x+\sin x=2\cos(x-\frac{\pi}{6})=2$, so $x=\frac{\pi}{6}$.
**6.** (c) — $c^2=4+4-2\cdot4\cos120^\circ=12$.
:::
