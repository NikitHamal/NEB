---
subject: Mathematics
grade: 11
unit: 11
title: Straight Line
hours: 7
area: Analytic Geometry
---

Coordinate geometry turns a picture into an equation, so that a question about
shape becomes a question about algebra. This unit completes the study of the
straight line begun in Grade 10 with the two results that carry almost all the
marks: **how far a point is from a line**, and **where the bisectors of the angle
between two lines lie**. Both follow from one idea — that the perpendicular
distance is the shortest distance from a point to a line.

::: key What the exam asks
The distance formula $d = \dfrac{|ax_1+by_1+c|}{\sqrt{a^{2}+b^{2}}}$ and the
bisector pair $\dfrac{a_1x+b_1y+c_1}{\sqrt{a_1^{2}+b_1^{2}}} = \pm\dfrac{a_2x+b_2y+c_2}{\sqrt{a_2^{2}+b_2^{2}}}$
are the two formulae to know cold. Group C usually asks for the **derivation** of
the first and an **identification** (which bisector is the acute one, which
contains the origin) for the second.
:::

## 11.1 Length of perpendicular from a given point to a given line

### Revision — the standard forms of a straight line

Every straight line in the plane has the equation $ax+by+c=0$ with $a$, $b$ not
both zero; this is the **general form**. It can be rewritten in whichever special
form the data suggests.

| Form | Equation | Use when you know |
|---|---|---|
| Slope–intercept | $y = mx+c$ | slope and $y$-intercept |
| Point–slope | $y-y_1 = m(x-x_1)$ | slope and one point |
| Two-point | $y-y_1 = \dfrac{y_2-y_1}{x_2-x_1}(x-x_1)$ | two points |
| Intercept | $\dfrac{x}{a}+\dfrac{y}{b} = 1$ | both intercepts |
| Normal | $x\cos\alpha+y\sin\alpha = p$ | perpendicular from origin |

Here $m = \tan\theta$, where $\theta$ is the **inclination**: the angle the line
makes with the positive $x$-axis, measured anticlockwise, $0^{\circ}\le\theta<180^{\circ}$.

```figure caption="Slope–intercept form. The line $y=mx+c$ cuts the $y$-axis at $c$ and has inclination $\theta$ with $m=\tan\theta$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.4,2.8))
m, c = 0.8, 1.2
x = np.linspace(-2.2, 4.2, 100)
ax.plot(x, m*x+c, color=ACCENT, lw=2.1)
ax.axhline(0, color=INK, lw=1.0); ax.axvline(0, color=INK, lw=1.0)
x0 = -c/m
t = np.linspace(0, np.arctan(m), 40)
ax.plot(x0+1.1*np.cos(t), 1.1*np.sin(t), color='#d9534f', lw=1.2)
ax.annotate(r'$\theta$', (x0+1.25, 0.16), color='#d9534f', fontsize=11)
ax.plot([0],[c],'o',color=ACCENT,ms=5.5)
ax.annotate('c', (0,c), textcoords='offset points', xytext=(-12,-2),
            color=INK, fontsize=10.5)
px = 2.6
ax.plot([px],[m*px+c],'o',color='#2e8b57',ms=5.5)
ax.annotate(r'$(x_1,y_1)$', (px,m*px+c), textcoords='offset points',
            xytext=(6,-4), color='#2e8b57', fontsize=9.5)
ax.annotate(r'$y=mx+c$', (4.1, m*4.1+c), textcoords='offset points',
            xytext=(-4,8), ha='right', color=ACCENT, fontsize=10)
ax.set_xlim(-2.4,4.6); ax.set_ylim(-1.4,4.8)
ax.set_xticks([]); ax.set_yticks([])
ax.spines[['top','right','bottom','left']].set_visible(False)
```

```figure caption="Intercept form $x/a+y/b=1$: the line cuts the axes at $A(a,0)$ and $B(0,b)$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.2,2.7))
a, b = 4.0, 3.0
ax.plot([a,0],[0,b], color=ACCENT, lw=2.1)
ax.axhline(0, color=INK, lw=1.0); ax.axvline(0, color=INK, lw=1.0)
ax.plot([a,0],[0,b],'o',color=ACCENT,ms=5.5)
ax.annotate('A(a, 0)', (a,0), textcoords='offset points', xytext=(4,-13),
            color=INK, fontsize=9.5)
ax.annotate('B(0, b)', (0,b), textcoords='offset points', xytext=(6,4),
            color=INK, fontsize=9.5)
ax.annotate('', xy=(a,-0.42), xytext=(0,-0.42),
            arrowprops=dict(arrowstyle='<->', color=MUTED, lw=1.0, mutation_scale=8))
ax.text(a/2, -0.62, 'a', ha='center', va='top', color=MUTED, fontsize=9.5)
ax.annotate('', xy=(-0.42,b), xytext=(-0.42,0),
            arrowprops=dict(arrowstyle='<->', color=MUTED, lw=1.0, mutation_scale=8))
ax.text(-0.62, b/2, 'b', ha='right', va='center', color=MUTED, fontsize=9.5)
ax.set_xlim(-1.5,5.2); ax.set_ylim(-1.3,4.0)
ax.set_xticks([]); ax.set_yticks([]); ax.set_aspect('equal')
ax.spines[['top','right','bottom','left']].set_visible(False)
```

::: derivation The normal form $x\cos\alpha+y\sin\alpha = p$
Let $ON$ be the perpendicular from the origin to the line, of length $p>0$, making
an angle $\alpha$ with the positive $x$-axis. The foot of the perpendicular is

$$ N = (p\cos\alpha,\; p\sin\alpha) $$

The slope of $ON$ is $\tan\alpha$, so the line, being perpendicular to $ON$, has
slope $-\cot\alpha = -\dfrac{\cos\alpha}{\sin\alpha}$. Using point–slope form at $N$:

$$ y-p\sin\alpha = -\frac{\cos\alpha}{\sin\alpha}\left(x-p\cos\alpha\right) $$

Multiply through by $\sin\alpha$:

$$ y\sin\alpha-p\sin^{2}\alpha = -x\cos\alpha+p\cos^{2}\alpha $$

$$ x\cos\alpha+y\sin\alpha = p\left(\cos^{2}\alpha+\sin^{2}\alpha\right) = p $$
:::

```figure caption="Normal form: $p$ is the length of the perpendicular $ON$ from the origin and $\alpha$ is its inclination."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.2,3.0))
al = np.radians(52); p = 2.0
N = np.array([p*np.cos(al), p*np.sin(al)])
d = np.array([-np.sin(al), np.cos(al)])
P1, P2 = N-2.6*d, N+2.2*d
ax.plot([P1[0],P2[0]],[P1[1],P2[1]], color=ACCENT, lw=2.1)
ax.plot([0,N[0]],[0,N[1]], color='#d9534f', lw=1.8)
ax.axhline(0, color=INK, lw=1.0); ax.axvline(0, color=INK, lw=1.0)
sq = 0.24
ax.plot([N[0]-sq*d[0], N[0]-sq*d[0]-sq*np.cos(al), N[0]-sq*np.cos(al)],
        [N[1]-sq*d[1], N[1]-sq*d[1]-sq*np.sin(al), N[1]-sq*np.sin(al)],
        color=MUTED, lw=1.0)
t = np.linspace(0, al, 40)
ax.plot(0.62*np.cos(t), 0.62*np.sin(t), color='#d9534f', lw=1.1)
ax.annotate(r'$\alpha$', (0.74, 0.22), color='#d9534f', fontsize=11)
ax.annotate('p', (N[0]/2, N[1]/2), textcoords='offset points', xytext=(-13,4),
            color='#d9534f', fontsize=11)
ax.plot([N[0]],[N[1]],'o',color='#d9534f',ms=5)
ax.annotate('N', (N[0],N[1]), textcoords='offset points', xytext=(7,2),
            color=INK, fontsize=10)
ax.annotate('O', (0,0), textcoords='offset points', xytext=(-12,-12),
            color=INK, fontsize=10)
ax.annotate(r'$x\cos\alpha+y\sin\alpha=p$', (P2[0],P2[1]),
            textcoords='offset points', xytext=(-6,6), ha='right',
            color=ACCENT, fontsize=9.5)
ax.set_xlim(-1.6,4.4); ax.set_ylim(-1.2,4.0)
ax.set_xticks([]); ax.set_yticks([]); ax.set_aspect('equal')
ax.spines[['top','right','bottom','left']].set_visible(False)
```

To put a general equation into normal form, move the constant to the right so it
is positive, then divide by $\sqrt{a^{2}+b^{2}}$.

::: example Worked example 11.1 — reduction to normal form
**Problem.** Reduce $x+\sqrt{3}\,y-8 = 0$ to normal form and state $p$ and $\alpha$.

**Solution.** Write it as $x+\sqrt{3}y = 8$ (right side already positive). Here
$\sqrt{a^{2}+b^{2}} = \sqrt{1+3} = 2$. Dividing by $2$:

$$ \frac{1}{2}x+\frac{\sqrt{3}}{2}y = 4 $$

Comparing with $x\cos\alpha+y\sin\alpha = p$ gives $\cos\alpha = \frac12$,
$\sin\alpha = \frac{\sqrt{3}}{2}$, so $\alpha = 60^{\circ}$ and $p = 4$.
:::

### Angle between two lines

::: derivation The angle between two lines
Let the lines have inclinations $\theta_1$ and $\theta_2$, so their slopes are
$m_1 = \tan\theta_1$ and $m_2 = \tan\theta_2$. In the triangle formed with the
$x$-axis, the exterior-angle theorem gives the angle $\theta$ between the lines as

$$ \theta = \theta_1-\theta_2 $$

Taking tangents and using the compound-angle formula,

$$ \tan\theta = \tan(\theta_1-\theta_2) = \frac{\tan\theta_1-\tan\theta_2}{1+\tan\theta_1\tan\theta_2}
= \frac{m_1-m_2}{1+m_1m_2} $$

The two lines cut at two supplementary angles; taking the modulus selects the
acute one:

$$ \tan\theta = |\frac{m_1-m_2}{1+m_1m_2}| $$
:::

::: key Parallel and perpendicular
- Parallel: $\theta = 0$, so $m_1 = m_2$. In general form, $\dfrac{a_1}{a_2} = \dfrac{b_1}{b_2}$.
- Perpendicular: $\theta = 90^{\circ}$, so the denominator vanishes:
  $1+m_1m_2 = 0$, i.e. $m_1m_2 = -1$. In general form, $a_1a_2+b_1b_2 = 0$.
:::

```figure caption="The angle between two lines: $\\theta=\\theta_1-\\theta_2$, so $\\tan\\theta=(m_1-m_2)/(1+m_1m_2)$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,2.9))
t1, t2 = np.radians(66), np.radians(24)
P = np.array([2.3, 1.0])
for th, col, lab in [(t1, ACCENT, r'$L_1$'), (t2, '#2e8b57', r'$L_2$')]:
    x0 = P[0]-P[1]/np.tan(th)
    xe = x0+3.1/np.tan(th)
    xs = np.array([x0-0.85, xe])
    ax.plot(xs, np.tan(th)*(xs-x0), color=col, lw=2.0)
    ax.annotate(lab, (xe, 3.1), textcoords='offset points',
                xytext=(4,-2), color=col, fontsize=10)
    a = np.linspace(0, th, 40)
    r = 0.62
    ax.plot(x0+r*np.cos(a), r*np.sin(a), color=MUTED, lw=1.0)
    ax.annotate(r'$\theta_1$' if th == t1 else r'$\theta_2$',
                (x0+(r+0.28)*np.cos(th/2), (r+0.28)*np.sin(th/2)),
                ha='center', va='center', color=MUTED, fontsize=10)
a = np.linspace(t2, t1, 40)
ax.plot(P[0]+0.85*np.cos(a), P[1]+0.85*np.sin(a), color='#d9534f', lw=1.4)
ax.annotate(r'$\theta$', (P[0]+1.08*np.cos((t1+t2)/2), P[1]+1.08*np.sin((t1+t2)/2)),
            ha='center', va='center', color='#d9534f', fontsize=11)
ax.plot([P[0]],[P[1]],'o',color=INK,ms=4)
ax.axhline(0, color=INK, lw=1.0)
ax.set_xlim(-0.9,7.6); ax.set_ylim(-0.45,3.7)
ax.set_xticks([]); ax.set_yticks([])
ax.spines[['top','right','bottom','left']].set_visible(False)
```

::: example Worked example 11.2 — angle between two lines
**Problem.** Find the acute angle between $3x+y-5=0$ and $x+2y-3=0$.

**Solution.** Rewrite in slope form: $y = -3x+5$ gives $m_1 = -3$;
$y = -\frac12x+\frac32$ gives $m_2 = -\frac12$.

$$ \tan\theta = |\frac{m_1-m_2}{1+m_1m_2}|
= |\frac{-3+\frac12}{1+\frac32}| = |\frac{-\frac52}{\frac52}| = 1 $$

So $\theta = 45^{\circ}$.
:::

### The perpendicular distance from a point to a line

::: derivation Length of the perpendicular from $P(x_1,y_1)$ to $ax+by+c=0$
Let the line meet the axes at $A\left(-\dfrac{c}{a},0\right)$ and
$B\left(0,-\dfrac{c}{b}\right)$, and let $PM$ be the perpendicular from
$P(x_1,y_1)$ to the line, of length $d$.

**Step 1 — area of $\triangle PAB$ two ways.** Using the coordinate formula,

$$ \text{area} = \frac12|x_1\left(0+\frac{c}{b}\right)+\left(-\frac{c}{a}\right)\left(-\frac{c}{b}-y_1\right)+0\left(y_1-0\right)| $$

$$ = \frac12|\frac{cx_1}{b}+\frac{c^{2}}{ab}+\frac{cy_1}{a}|
= \frac12|\frac{c}{ab}||ax_1+by_1+c| $$

**Step 2 — the same area as base $\times$ height.** Taking $AB$ as base and $PM$
as height,

$$ \text{area} = \frac12\,AB\cdot d, \qquad
AB = \sqrt{\frac{c^{2}}{a^{2}}+\frac{c^{2}}{b^{2}}} = \frac{|c|\sqrt{a^{2}+b^{2}}}{|ab|} $$

**Step 3 — equate and solve for $d$.**

$$ \frac12\cdot\frac{|c|\sqrt{a^{2}+b^{2}}}{|ab|}\cdot d
= \frac12\cdot\frac{|c|}{|ab|}|ax_1+by_1+c| $$

The factor $\dfrac{|c|}{2|ab|}$ cancels from both sides, leaving

$$ d = \frac{|ax_1+by_1+c|}{\sqrt{a^{2}+b^{2}}} $$
:::

```figure caption="Perpendicular distance. The area of $\triangle PAB$ computed from coordinates and as $\tfrac12 AB\cdot d$ gives $d=|ax_1+by_1+c|/\sqrt{a^{2}+b^{2}}$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6,3.0))
a, b, c = 3.0, 4.0, -12.0
A = np.array([-c/a, 0.0]); B = np.array([0.0, -c/b])
P = np.array([4.6, 3.4])
xs = np.array([-0.9, 6.2])
ax.plot(xs, (-c-a*xs)/b, color=ACCENT, lw=2.1)
ax.fill([P[0],A[0],B[0]],[P[1],A[1],B[1]], color=ACCENT, alpha=0.08)
ax.plot([P[0],A[0],B[0],P[0]],[P[1],A[1],B[1],P[1]], color=MUTED, lw=1.0, ls='--')
n = np.array([a,b])/np.hypot(a,b)
t = (a*P[0]+b*P[1]+c)/np.hypot(a,b)
M = P - t*n
ax.plot([P[0],M[0]],[P[1],M[1]], color='#d9534f', lw=1.9)
u = (A-B)/np.linalg.norm(A-B); s = 0.32
ax.plot([M[0]+s*u[0], M[0]+s*u[0]+s*n[0], M[0]+s*n[0]],
        [M[1]+s*u[1], M[1]+s*u[1]+s*n[1], M[1]+s*n[1]], color=MUTED, lw=1.0)
for pt, lab, off in [(P,r'$P(x_1,y_1)$',(6,4)), (A,'A',(4,-13)), (B,'B',(-14,2)),
                     (M,'M',(6,6))]:
    ax.plot([pt[0]],[pt[1]],'o',color=INK,ms=4.2)
    ax.annotate(lab, pt, textcoords='offset points', xytext=off, color=INK, fontsize=9.5)
ax.annotate('d', (P+M)/2, textcoords='offset points', xytext=(7,2),
            color='#d9534f', fontsize=11)
ax.annotate(r'$ax+by+c=0$', (4.9,(-c-a*4.9)/b), textcoords='offset points',
            xytext=(8,-4), ha='left', va='top', color=ACCENT, fontsize=9.5)
ax.axhline(0, color=INK, lw=1.0); ax.axvline(0, color=INK, lw=1.0)
ax.set_xlim(-1.6,6.6); ax.set_ylim(-1.2,4.6)
ax.set_xticks([]); ax.set_yticks([]); ax.set_aspect('equal')
ax.spines[['top','right','bottom','left']].set_visible(False)
```

::: caution Normalise before you substitute
The formula needs the line in the form $ax+by+c=0$ — **everything on one side**.
For $3x = 4y+7$ you must first write $3x-4y-7=0$. And the denominator is
$\sqrt{a^{2}+b^{2}}$, never $a+b$.
:::

Putting $(x_1,y_1) = (0,0)$ gives the distance of the line from the origin:

$$ d_{O} = \frac{|c|}{\sqrt{a^{2}+b^{2}}} $$

which is exactly the $p$ of the normal form.

::: example Worked example 11.3
**Problem.** Find the length of the perpendicular from $(3,-5)$ to the line
$3x-4y-26 = 0$, and from the origin to $12x-5y+26=0$.

**Solution.** For the first, $a=3$, $b=-4$, $c=-26$ and $\sqrt{a^{2}+b^{2}} = \sqrt{9+16} = 5$:

$$ d = \frac{|3(3)-4(-5)-26|}{5} = \frac{|9+20-26|}{5} = \frac{3}{5} = 0.6\ \text{units} $$

For the second, $\sqrt{144+25} = 13$ and the point is the origin:

$$ d = \frac{|12(0)-5(0)+26|}{13} = \frac{26}{13} = 2\ \text{units} $$
:::

::: example Worked example 11.4 — altitude and area of a triangle
**Problem.** The vertices of a triangle are $A(1,1)$, $B(4,0)$ and $C(0,3)$. Find
the length of the altitude from $A$ to $BC$, and hence the area of the triangle.

**Solution.** $B$ and $C$ are the $x$- and $y$-intercepts of $BC$, so the intercept
form gives $\dfrac{x}{4}+\dfrac{y}{3} = 1$, i.e.

$$ 3x+4y-12 = 0 $$

The altitude from $A$ is the perpendicular distance from $A(1,1)$ to this line:

$$ h = \frac{|3(1)+4(1)-12|}{\sqrt{9+16}} = \frac{|-5|}{5} = 1\ \text{unit} $$

The base is $BC = \sqrt{(4-0)^{2}+(0-3)^{2}} = \sqrt{16+9} = 5$ units, so

$$ \text{area} = \tfrac12\times 5\times 1 = 2.5\ \text{square units} $$
:::

```figure caption="Worked example 11.4: the altitude from $A(1,1)$ to the line $3x+4y-12=0$ has length exactly $1$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.2,2.8))
A = np.array([1.0,1.0]); B = np.array([4.0,0.0]); C = np.array([0.0,3.0])
ax.plot([A[0],B[0],C[0],A[0]],[A[1],B[1],C[1],A[1]], color=ACCENT, lw=2.0)
ax.fill([A[0],B[0],C[0]],[A[1],B[1],C[1]], color=ACCENT, alpha=0.08)
n = np.array([3.0,4.0])/5.0
t = (3*A[0]+4*A[1]-12)/5.0
M = A - t*n
ax.plot([A[0],M[0]],[A[1],M[1]], color='#d9534f', lw=1.8)
u = (B-C)/np.linalg.norm(B-C); s = 0.22
ax.plot([M[0]+s*u[0], M[0]+s*u[0]-s*n[0], M[0]-s*n[0]],
        [M[1]+s*u[1], M[1]+s*u[1]-s*n[1], M[1]-s*n[1]], color=MUTED, lw=1.0)
ax.annotate('h = 1', (A+M)/2, textcoords='offset points', xytext=(-16,3),
            ha='right', color='#d9534f', fontsize=9.5)
for pt, lab, off in [(A,'A(1, 1)',(-8,-16)), (B,'B(4, 0)',(4,-13)), (C,'C(0, 3)',(4,4))]:
    ax.plot([pt[0]],[pt[1]],'o',color=INK,ms=4.5)
    ax.annotate(lab, pt, textcoords='offset points', xytext=off, color=INK, fontsize=9.2)
ax.annotate(r'$3x+4y-12=0$', (2.0,1.5), textcoords='offset points', xytext=(16,10),
            color=ACCENT, fontsize=9)
ax.axhline(0, color=INK, lw=1.0); ax.axvline(0, color=INK, lw=1.0)
ax.set_xlim(-0.9,5.4); ax.set_ylim(-0.9,3.9)
ax.set_xticks([]); ax.set_yticks([]); ax.set_aspect('equal')
ax.spines[['top','right','bottom','left']].set_visible(False)
```

### Distance between two parallel lines

Parallel lines have the same $a$ and $b$, so write them as $ax+by+c_1=0$ and
$ax+by+c_2=0$. Take **any** point on the first, for instance
$\left(-\frac{c_1}{a},0\right)$, and find its distance from the second:

$$ d = \frac{|a\left(-\frac{c_1}{a}\right)+b(0)+c_2|}{\sqrt{a^{2}+b^{2}}}
= \frac{|c_2-c_1|}{\sqrt{a^{2}+b^{2}}} $$

::: caution Make the coefficients identical first
$3x+4y-9=0$ and $6x+8y-15=0$ are parallel but you cannot subtract the constants
yet. Divide the second by $2$ to get $3x+4y-7.5=0$; only then is
$d = \dfrac{|-7.5+9|}{5} = \dfrac{1.5}{5} = 0.3$.
:::

```figure caption="Two parallel lines $ax+by+c_1=0$ and $ax+by+c_2=0$; the gap between them is $|c_2-c_1|/\\sqrt{a^{2}+b^{2}}$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6,2.8))
a, b = 3.0, 4.0
xs = np.array([-0.6, 5.0])
for c, col, lab, dy in [(-12.0, ACCENT, r'$ax+by+c_1=0$', 9),
                        (-2.0, '#2e8b57', r'$ax+by+c_2=0$', 10)]:
    ys = (-c-a*xs)/b
    ax.plot(xs, ys, color=col, lw=2.0)
    ax.annotate(lab, (xs[0], ys[0]), textcoords='offset points',
                xytext=(0,dy), ha='left', color=col, fontsize=9)
n = np.array([a,b])/np.hypot(a,b)
P = np.array([2.4, (12-3*2.4)/4])
Q = P-(10.0/5.0)*n
ax.annotate('', xy=(Q[0],Q[1]), xytext=(P[0],P[1]),
            arrowprops=dict(arrowstyle='<->', color='#d9534f', lw=1.6, mutation_scale=10))
ax.annotate('d', (P+Q)/2, textcoords='offset points', xytext=(9,4),
            color='#d9534f', fontsize=11)
ax.set_xlim(-0.9,5.4); ax.set_ylim(-1.0,4.2)
ax.set_aspect('equal'); ax.axis('off')
```

::: example Worked example 11.5 — points at a given distance
**Problem.** Find the points on the line $x+y = 4$ that are at a distance of
$1$ unit from the line $4x+3y-10 = 0$.

**Solution.** Any point on $x+y=4$ can be written $P(t,\,4-t)$. Its distance from
the second line is

$$ \frac{|4t+3(4-t)-10|}{\sqrt{16+9}} = \frac{|t+2|}{5} $$

Setting this equal to $1$ gives $|t+2| = 5$, so $t+2 = 5$ or $t+2 = -5$, i.e.
$t = 3$ or $t = -7$.

The points are $(3,\,1)$ and $(-7,\,11)$ — one on each side of the line.
:::

::: example Worked example 11.6 — foot of the perpendicular and image
**Problem.** Find the foot of the perpendicular from $P(1,2)$ to the line
$3x+4y-1=0$, and the image of $P$ in that line.

**Solution.** The perpendicular from $P$ has slope $\frac{4}{3}$ (the negative
reciprocal of $-\frac34$), so its equation is

$$ y-2 = \frac43(x-1) \;\Rightarrow\; 4x-3y+2 = 0 $$

Solving $3x+4y = 1$ and $4x-3y = -2$ simultaneously: multiplying the first by $3$
and the second by $4$ and adding gives $9x+16x = 3-8$, so $25x = -5$ and
$x = -\frac15$. Then $y = \frac{1-3\left(-\frac15\right)}{4} = \frac{1+\frac35}{4} = \frac25$.

Foot $M = \left(-\dfrac15,\ \dfrac25\right)$.

The image $P'$ is such that $M$ is the midpoint of $PP'$, so

$$ P' = (2M_x-x_1,\ 2M_y-y_1) = \left(-\tfrac25-1,\ \tfrac45-2\right)
= \left(-\tfrac75,\ -\tfrac65\right) $$

**Check.** The distance from $P$ to the line is $\frac{|3+8-1|}{5} = 2$, and
$PM = \sqrt{\left(1+\frac15\right)^{2}+\left(2-\frac25\right)^{2}} = \sqrt{\frac{36}{25}+\frac{64}{25}} = 2$ ✓.
:::

## 11.2 Bisectors of the angles between two straight lines

### The pair of bisectors

Two intersecting lines create two pairs of vertically opposite angles, and
therefore **two** bisectors. They are always perpendicular to each other.

::: derivation Equations of the two bisectors
A point lies on an angle bisector exactly when it is **equidistant from the two
arms**. So let $P(x,y)$ be a point on a bisector of the angles between

$$ L_1: a_1x+b_1y+c_1 = 0, \qquad L_2: a_2x+b_2y+c_2 = 0 $$

Equating the two perpendicular distances,

$$ \frac{|a_1x+b_1y+c_1|}{\sqrt{a_1^{2}+b_1^{2}}} = \frac{|a_2x+b_2y+c_2|}{\sqrt{a_2^{2}+b_2^{2}}} $$

Removing the modulus signs introduces a $\pm$, and the locus splits into the two
straight lines

$$ \frac{a_1x+b_1y+c_1}{\sqrt{a_1^{2}+b_1^{2}}} = \pm\,\frac{a_2x+b_2y+c_2}{\sqrt{a_2^{2}+b_2^{2}}} $$

Both pass through the point of intersection of $L_1$ and $L_2$, since there both
numerators vanish.
:::

::: key Identifying the bisectors
First rewrite **both** equations so that the constant terms $c_1$ and $c_2$ are
**positive**. Then:

- The **$+$ sign** gives the bisector of the angle **containing the origin**.
- The **$-$ sign** gives the bisector of the other angle.
- If $a_1a_2+b_1b_2 < 0$ the origin lies in the **acute** angle, so the $+$
  bisector is the acute-angle bisector. If $a_1a_2+b_1b_2 > 0$ the origin lies in
  the obtuse angle and the $-$ bisector is the acute one.
:::

An independent check that never fails: find the angle $\theta$ between one
original line and a candidate bisector. If $\tan\theta < 1$ (i.e. $\theta<45^{\circ}$)
that candidate bisects the acute angle.

```figure caption="The lines $3x-4y+7=0$ and $12x+5y-2=0$ with both bisectors (dashed). The origin lies in the shaded angle, bisected by $11x-3y+9=0$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,3.4))
X, Y = np.meshgrid(np.linspace(-3.2,3.2,400), np.linspace(-2.2,3.6,400))
L1 = 3*X-4*Y+7; L2 = 12*X+5*Y-2
mask = ((np.sign(L1) == np.sign(7.0)) & (np.sign(L2) == np.sign(-2.0))).astype(float)
ax.contourf(X, Y, mask, levels=[0.5,1.5], colors=[MUTED], alpha=0.13)
xs = np.linspace(-3.2, 3.2, 200)
for a, b, c, col, lw, ls, lab in [
        (3,-4,7, ACCENT, 2.0, '-', r'$3x-4y+7=0$'),
        (12,5,-2, '#2e8b57', 2.0, '-', r'$12x+5y-2=0$'),
        (11,-3,9, '#d9534f', 1.5, '--', r'$11x-3y+9=0$'),
        (21,77,-101, '#6a5acd', 1.5, '--', r'$21x+77y-101=0$')]:
    ax.plot(xs, (-c-a*xs)/b, color=col, lw=lw, ls=ls, label=lab)
ax.plot([0],[0],'o',color=INK,ms=5.5)
ax.annotate('O', (0,0), textcoords='offset points', xytext=(9,2),
            color=INK, fontsize=10.5)
ax.plot([-3/7],[10/7],'o',color=INK,ms=4)
ax.axhline(0, color=INK, lw=0.9); ax.axvline(0, color=INK, lw=0.9)
ax.set_xlim(-3.2,3.2); ax.set_ylim(-2.2,3.6)
ax.set_xticks([-2,0,2]); ax.set_yticks([-2,0,2])
ax.spines[['top','right']].set_visible(False)
ax.legend(loc='lower left', fontsize=7.4, ncol=2, columnspacing=0.8,
          handlelength=1.6, borderpad=0.35, frameon=True, framealpha=0.92,
          facecolor='white', edgecolor='none')
```

::: example Worked example 11.7 — the two bisectors
**Problem.** Find the equations of the bisectors of the angles between
$3x-4y+7 = 0$ and $12x+5y-2 = 0$, and state which bisects the angle containing
the origin.

**Solution.** Here $\sqrt{9+16} = 5$ and $\sqrt{144+25} = 13$, so the bisectors are

$$ \frac{3x-4y+7}{5} = \pm\,\frac{12x+5y-2}{13} $$

Cross-multiplying, $13(3x-4y+7) = \pm 5(12x+5y-2)$, i.e.
$39x-52y+91 = \pm(60x+25y-10)$.

**Taking $+$:** $39x-52y+91-60x-25y+10 = 0$, giving

$$ -21x-77y+101 = 0 \;\Rightarrow\; 21x+77y-101 = 0 $$

**Taking $-$:** $39x-52y+91+60x+25y-10 = 0$, giving

$$ 99x-27y+81 = 0 \;\Rightarrow\; 11x-3y+9 = 0 $$

**Which contains the origin?** Rewrite both lines with positive constants:
$3x-4y+7=0$ (already) and $-12x-5y+2=0$. Now the $+$ combination is

$$ \frac{3x-4y+7}{5} = \frac{-12x-5y+2}{13} \;\Rightarrow\; 99x-27y+81 = 0
\;\Rightarrow\; 11x-3y+9 = 0 $$

So $11x-3y+9=0$ bisects the angle **containing the origin**, and
$21x+77y-101=0$ bisects the other.

**Check.** Their slopes are $\frac{11}{3}$ and $-\frac{21}{77} = -\frac{3}{11}$;
the product is $-1$, so the two bisectors are perpendicular, as they must be.
:::

::: example Worked example 11.8 — which bisector is the acute one?
**Problem.** Find the bisectors of the angles between $4x+3y-6 = 0$ and
$5x+12y+9 = 0$, and identify the bisector of the acute angle.

**Solution.** Make both constants positive: $-4x-3y+6 = 0$ and $5x+12y+9 = 0$.
Then $\sqrt{16+9} = 5$ and $\sqrt{25+144} = 13$, and the bisectors are

$$ \frac{-4x-3y+6}{5} = \pm\,\frac{5x+12y+9}{13} $$

**Origin bisector ($+$):** $13(-4x-3y+6) = 5(5x+12y+9)$, so
$-52x-39y+78 = 25x+60y+45$, giving $77x+99y-33 = 0$, i.e.

$$ 7x+9y-3 = 0 $$

**Other bisector ($-$):** $-52x-39y+78 = -25x-60y-45$, giving
$-27x+21y+123 = 0$, i.e.

$$ 9x-7y-41 = 0 $$

**Acute or obtuse?** With the positive-constant forms, $a_1a_2+b_1b_2 = (-4)(5)+(-3)(12) = -56 < 0$,
so the origin lies in the **acute** angle. Hence $7x+9y-3=0$ is the acute-angle
bisector.

**Independent check.** The slope of $4x+3y-6=0$ is $-\frac43$ and of $7x+9y-3=0$
is $-\frac79$. Then

$$ \tan\theta = |\frac{-\frac43+\frac79}{1+\frac{28}{27}}|
= |\frac{-\frac{5}{9}}{\frac{55}{27}}| = \frac{5}{9}\cdot\frac{27}{55} = \frac{3}{11} $$

Since $\frac{3}{11} < 1$, the angle is less than $45^{\circ}$ — it really is the
acute bisector ✓.
:::

::: example Worked example 11.9 — bisectors as a locus
**Problem.** Find the locus of a point that moves so that it is equidistant from
the lines $x+2y-3 = 0$ and $2x-y+5 = 0$.

**Solution.** Let the point be $P(x,y)$. Both denominators are
$\sqrt{1+4} = \sqrt{5}$, so the condition is

$$ \frac{|x+2y-3|}{\sqrt{5}} = \frac{|2x-y+5|}{\sqrt{5}}
\;\Rightarrow\; |x+2y-3| = |2x-y+5| $$

Hence $x+2y-3 = \pm(2x-y+5)$.

**Plus:** $x+2y-3 = 2x-y+5 \Rightarrow x-3y+8 = 0$.

**Minus:** $x+2y-3 = -2x+y-5 \Rightarrow 3x+y+2 = 0$.

The locus is the **pair of perpendicular bisectors** $x-3y+8=0$ and $3x+y+2=0$
(slopes $\frac13$ and $-3$, product $-1$ ✓). Note that the two original lines are
themselves perpendicular, so the bisectors make $45^{\circ}$ with each of them.
:::

::: tip Keep the signs straight
The commonest bisector error is forgetting to make $c_1$ and $c_2$ positive before
choosing the sign. If you only need *both* bisector equations, the sign
arrangement does not matter; it matters only when the question asks *which*
bisector contains the origin or bisects the acute angle.
:::

## Chapter summary

- General form $ax+by+c=0$; slope $m = -a/b = \tan\theta$ where $\theta$ is the
  inclination. Forms: $y=mx+c$, $y-y_1=m(x-x_1)$, $x/a+y/b=1$,
  $x\cos\alpha+y\sin\alpha=p$.
- Angle between two lines: $\tan\theta = |\dfrac{m_1-m_2}{1+m_1m_2}|$;
  parallel if $m_1=m_2$, perpendicular if $m_1m_2=-1$ or $a_1a_2+b_1b_2=0$.
- Perpendicular distance from $(x_1,y_1)$ to $ax+by+c=0$:
  $d = \dfrac{|ax_1+by_1+c|}{\sqrt{a^{2}+b^{2}}}$; from the origin,
  $d = \dfrac{|c|}{\sqrt{a^{2}+b^{2}}} = p$.
- Distance between the parallel lines $ax+by+c_1=0$ and $ax+by+c_2=0$ is
  $\dfrac{|c_1-c_2|}{\sqrt{a^{2}+b^{2}}}$, after making $a$ and $b$ identical.
- The bisectors of the angles between two lines are
  $\dfrac{a_1x+b_1y+c_1}{\sqrt{a_1^{2}+b_1^{2}}} = \pm\dfrac{a_2x+b_2y+c_2}{\sqrt{a_2^{2}+b_2^{2}}}$,
  and they are perpendicular to each other.
- With $c_1,c_2>0$: the $+$ sign gives the bisector of the angle containing the
  origin; that angle is acute when $a_1a_2+b_1b_2<0$.
- A bisector can always be identified by testing whether $\tan\theta<1$ for the
  angle it makes with one of the original lines.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The distance of the point $(1,2)$ from the line $3x+4y-5 = 0$ is <span class="marks">[1]</span>
   (a) $\frac{6}{5}$ (b) $\frac{5}{6}$ (c) $6$ (d) $\frac{6}{7}$
2. The lines $2x+3y-1=0$ and $3x-2y+5=0$ are <span class="marks">[1]</span>
   (a) parallel (b) perpendicular (c) coincident (d) inclined at $45^{\circ}$
3. The perpendicular distance of the line $4x-3y+10=0$ from the origin is <span class="marks">[1]</span>
   (a) $10$ (b) $2$ (c) $\frac{10}{7}$ (d) $5$
4. The number of bisectors of the angles between two intersecting lines is <span class="marks">[1]</span>
   (a) 1 (b) 2 (c) 3 (d) infinitely many
5. In the normal form $x\cos\alpha+y\sin\alpha = p$, the quantity $p$ is always <span class="marks">[1]</span>
   (a) negative (b) zero (c) positive (d) equal to the slope
6. The two bisectors of the angles between two lines always <span class="marks">[1]</span>
   (a) are parallel (b) are perpendicular (c) pass through the origin (d) coincide

::: note Answers to Group A
**1.** (a) — $\frac{|3+8-5|}{\sqrt{9+16}} = \frac{6}{5}$.
**2.** (b) — $a_1a_2+b_1b_2 = 6-6 = 0$.
**3.** (b) — $\frac{|10|}{\sqrt{16+9}} = 2$.
**4.** (b) — one for each pair of vertically opposite angles.
**5.** (c) — $p$ is a length, taken positive by definition.
**6.** (b) — the two bisected angles are supplementary, so the bisectors differ by $90^{\circ}$.
:::

**Group B — Short answer (5 marks each)**

1. Derive the formula for the length of the perpendicular from the point
   $(x_1,y_1)$ to the line $ax+by+c=0$. <span class="marks">[5]</span>
2. Find the distance between the parallel lines $4x-3y+5 = 0$ and
   $8x-6y-13 = 0$. <span class="marks">[5]</span>
3. Find the length of the perpendicular drawn from the point $(4,1)$ to the line
   joining $(2,-1)$ and $(6,5)$. <span class="marks">[5]</span>
4. Find the equations of the bisectors of the angles between $x+2y-11=0$ and
   $3x-6y-5=0$. <span class="marks">[5]</span>
5. Reduce $\sqrt{3}\,x+y-10 = 0$ to the normal form and hence find the length of
   the perpendicular from the origin and its inclination. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Let the line meet the axes at $A\left(-\frac{c}{a},0\right)$ and
$B\left(0,-\frac{c}{b}\right)$ and let $d$ be the length of the perpendicular $PM$.
The coordinate formula gives
$\text{area}(\triangle PAB) = \frac12|\frac{c}{ab}||ax_1+by_1+c|$, while
$\text{area} = \frac12 AB\cdot d$ with
$AB = \frac{|c|\sqrt{a^{2}+b^{2}}}{|ab|}$. Equating and cancelling
$\frac{|c|}{2|ab|}$ gives $d = \dfrac{|ax_1+by_1+c|}{\sqrt{a^{2}+b^{2}}}$.

**2.** Divide the second equation by $2$: $4x-3y-6.5 = 0$. Now the coefficients
match, and $\sqrt{16+9} = 5$, so
$d = \dfrac{|5-(-6.5)|}{5} = \dfrac{11.5}{5} = 2.3$ units.

**3.** The line through $(2,-1)$ and $(6,5)$ has slope $\frac{5+1}{6-2} = \frac32$,
so $y+1 = \frac32(x-2)$, i.e. $3x-2y-8 = 0$. Then
$d = \dfrac{|3(4)-2(1)-8|}{\sqrt{9+4}} = \dfrac{2}{\sqrt{13}}$ units
$\approx 0.555$ units.

**4.** $\sqrt{1+4} = \sqrt{5}$ and $\sqrt{9+36} = \sqrt{45} = 3\sqrt{5}$. The
bisectors are $\dfrac{x+2y-11}{\sqrt{5}} = \pm\dfrac{3x-6y-5}{3\sqrt{5}}$, i.e.
$3(x+2y-11) = \pm(3x-6y-5)$.
Plus: $3x+6y-33 = 3x-6y-5 \Rightarrow 12y = 28 \Rightarrow y = \frac73$, i.e.
$3y-7 = 0$.
Minus: $3x+6y-33 = -3x+6y+5 \Rightarrow 6x = 38 \Rightarrow 3x-19 = 0$.
The bisectors are $3y-7=0$ and $3x-19=0$ — a horizontal and a vertical line, so
perpendicular ✓.

**5.** $\sqrt{3}x+y = 10$ with $\sqrt{3+1} = 2$. Dividing by $2$:
$\frac{\sqrt{3}}{2}x+\frac12 y = 5$. Comparing with $x\cos\alpha+y\sin\alpha = p$,
$\cos\alpha = \frac{\sqrt{3}}{2}$ and $\sin\alpha = \frac12$, so $\alpha = 30^{\circ}$
and $p = 5$ units.
:::

**Group C — Long answer (8 marks each)**

1. (a) Derive the equations of the bisectors of the angles between the lines
   $a_1x+b_1y+c_1 = 0$ and $a_2x+b_2y+c_2 = 0$. <span class="marks">[4]</span>
   (b) Hence find the bisectors of the angles between $3x+4y+7 = 0$ and
   $12x-5y-8 = 0$, and identify the one that bisects the angle containing the
   origin. <span class="marks">[4]</span>
2. The vertices of a triangle are $A(2,1)$, $B(8,1)$ and $C(2,9)$.
   (a) Find the equation of $BC$. <span class="marks">[3]</span>
   (b) Find the length of the perpendicular from $A$ to $BC$ and hence the area
   of the triangle. <span class="marks">[5]</span>

::: note Answers to Group C
**1.** (a) A point $P(x,y)$ lies on a bisector precisely when it is equidistant
from the two lines, so
$\dfrac{|a_1x+b_1y+c_1|}{\sqrt{a_1^{2}+b_1^{2}}} = \dfrac{|a_2x+b_2y+c_2|}{\sqrt{a_2^{2}+b_2^{2}}}$.
Dropping the modulus signs gives the $\pm$, so the locus is the pair of lines
$\dfrac{a_1x+b_1y+c_1}{\sqrt{a_1^{2}+b_1^{2}}} = \pm\dfrac{a_2x+b_2y+c_2}{\sqrt{a_2^{2}+b_2^{2}}}$.
Both pass through the intersection of the given lines.

(b) $\sqrt{9+16} = 5$, $\sqrt{144+25} = 13$, so
$\dfrac{3x+4y+7}{5} = \pm\dfrac{12x-5y-8}{13}$, i.e. $13(3x+4y+7) = \pm 5(12x-5y-8)$.
Plus: $39x+52y+91 = 60x-25y-40 \Rightarrow 21x-77y-131 = 0$.
Minus: $39x+52y+91 = -60x+25y+40 \Rightarrow 99x+27y+51 = 0 \Rightarrow 33x+9y+17 = 0$.
For the origin: with positive constants the lines are $3x+4y+7=0$ and
$-12x+5y+8=0$, and the $+$ combination gives
$13(3x+4y+7) = 5(-12x+5y+8)$, i.e. $39x+52y+91 = -60x+25y+40$, which is
$99x+27y+51 = 0$, i.e. $33x+9y+17 = 0$. So $33x+9y+17=0$ bisects the angle
containing the origin. (Slopes $\frac{21}{77} = \frac{3}{11}$ and $-\frac{33}{9} = -\frac{11}{3}$;
their product is $-1$ ✓.)

**2.** (a) $B(8,1)$ and $C(2,9)$ give slope $\dfrac{9-1}{2-8} = -\dfrac{8}{6} = -\dfrac43$.
Using point–slope at $B$: $y-1 = -\frac43(x-8)$, so $3y-3 = -4x+32$, i.e.
$$ 4x+3y-35 = 0 $$

(b) The perpendicular from $A(2,1)$ has length
$d = \dfrac{|4(2)+3(1)-35|}{\sqrt{16+9}} = \dfrac{|-24|}{5} = 4.8$ units.
$BC = \sqrt{(2-8)^{2}+(9-1)^{2}} = \sqrt{36+64} = 10$ units, so
$\text{area} = \frac12\times 10\times 4.8 = 24$ square units.
Check with the determinant formula:
$\frac12|2(1-9)+8(9-1)+2(1-1)| = \frac12|-16+64| = 24$ ✓.
:::
