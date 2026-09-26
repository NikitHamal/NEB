---
subject: Mathematics
grade: 11
unit: 12
title: Pair of Straight Lines
hours: 7
area: Analytic Geometry
---

A single straight line has a first-degree equation. Multiply two such equations
together and you get a **second-degree** equation whose graph is not a curve but
**two straight lines**. This unit runs that idea backwards: given a second-degree
equation in $x$ and $y$, when does it represent a pair of lines, what are the
lines, what angle do they make, and where do their angle bisectors lie?

::: key What the exam asks
Three results carry nearly all the marks: the condition
$abc+2fgh-af^{2}-bg^{2}-ch^{2} = 0$, the angle formula
$\tan\theta = \dfrac{2\sqrt{h^{2}-ab}}{a+b}$, and the bisector pair
$\dfrac{x^{2}-y^{2}}{a-b} = \dfrac{xy}{h}$. Group C almost always asks you to
**derive** the angle formula or the bisector equation from the homogeneous
equation.
:::

## 12.1 General equation of second degree; condition for representing a pair of lines

The most general second-degree equation in two variables is written, by long
convention, as

$$ ax^{2}+2hxy+by^{2}+2gx+2fy+c = 0 $$

The factors of $2$ are put in deliberately so that the formulae below come out
without fractions. So for $2x^{2}+7xy+3y^{2}+8x+14y+8 = 0$ we read off
$a=2$, $h=\frac72$, $b=3$, $g=4$, $f=7$, $c=8$.

::: caution Halve the middle coefficients
$h$, $g$ and $f$ are **half** the coefficients of $xy$, $x$ and $y$. Forgetting
this is the single commonest error in this unit — it makes the condition fail for
an equation that really does represent a pair of lines.
:::

::: derivation The condition for a pair of lines
Suppose the equation factorises into two linear factors:

$$ ax^{2}+2hxy+by^{2}+2gx+2fy+c = (l_1x+m_1y+n_1)(l_2x+m_2y+n_2) $$

Treat the equation as a quadratic **in $x$**, with $y$ as a parameter:

$$ ax^{2}+2(hy+g)x+(by^{2}+2fy+c) = 0 $$

$$ x = \frac{-2(hy+g)\pm\sqrt{4(hy+g)^{2}-4a(by^{2}+2fy+c)}}{2a} $$

For $x$ to be a **linear** function of $y$ — which is what "a pair of straight
lines" means — the expression under the root must be a perfect square in $y$:

$$ (hy+g)^{2}-a(by^{2}+2fy+c) = (h^{2}-ab)y^{2}+2(gh-af)y+(g^{2}-ac) $$

A quadratic $Ay^{2}+By+C$ is a perfect square exactly when its discriminant
$B^{2}-4AC = 0$:

$$ 4(gh-af)^{2}-4(h^{2}-ab)(g^{2}-ac) = 0 $$

Expanding,

$$ g^{2}h^{2}-2afgh+a^{2}f^{2}-\left(g^{2}h^{2}-ach^{2}-abg^{2}+a^{2}bc\right) = 0 $$

$$ -2afgh+a^{2}f^{2}+ach^{2}+abg^{2}-a^{2}bc = 0 $$

Dividing by $-a$ (assuming $a \ne 0$) gives the condition

$$ abc+2fgh-af^{2}-bg^{2}-ch^{2} = 0 $$
:::

::: key The condition, and how to remember it
$$ \Delta = abc+2fgh-af^{2}-bg^{2}-ch^{2} = 0 $$
This is the expansion of the determinant of the symmetric array with rows
$(a,h,g)$, $(h,b,f)$, $(g,f,c)$. Two further facts go with it:

- The two lines are **real and distinct** when $h^{2} > ab$, **coincident** when
  $h^{2} = ab$, and imaginary (only the intersection point is real) when $h^{2}<ab$.
- Their point of intersection is
  $\left(\dfrac{bg-fh}{h^{2}-ab},\ \dfrac{af-gh}{h^{2}-ab}\right)$.
:::

::: example Worked example 12.1 — testing and factorising
**Problem.** Show that $2x^{2}+7xy+3y^{2}+8x+14y+8 = 0$ represents a pair of
straight lines, find them, and find their point of intersection.

**Solution.** Reading off, $a=2$, $b=3$, $c=8$, $h=\frac72$, $g=4$, $f=7$.

$$ \Delta = (2)(3)(8)+2(7)(4)\left(\tfrac72\right)-2(7)^{2}-3(4)^{2}-8\left(\tfrac72\right)^{2} $$

$$ = 48+196-98-48-98 = 0 $$

So it does represent a pair of lines. Also $h^{2}-ab = \frac{49}{4}-6 = \frac{25}{4} > 0$,
so they are real and distinct.

**Factorising.** Treat it as a quadratic in $x$:
$2x^{2}+(7y+8)x+(3y^{2}+14y+8) = 0$. The last bracket factorises as
$(3y+2)(y+4)$, and $2x^{2}+7xy+3y^{2} = (x+3y)(2x+y)$, so we try

$$ (x+3y+2)(2x+y+4) = 0 $$

Expanding checks out: $2x^{2}+xy+4x+6xy+3y^{2}+12y+4x+2y+8 = 2x^{2}+7xy+3y^{2}+8x+14y+8$ ✓.

The lines are $x+3y+2 = 0$ and $2x+y+4 = 0$.

**Point of intersection.** From the second, $y = -4-2x$; substituting,
$x+3(-4-2x)+2 = 0$, so $-5x-10 = 0$ and $x = -2$, giving $y = 0$. The lines meet
at $(-2,\,0)$.

**Check with the formula.**
$\dfrac{bg-fh}{h^{2}-ab} = \dfrac{3(4)-7\left(\frac72\right)}{\frac{25}{4}}
= \dfrac{-\frac{25}{2}}{\frac{25}{4}} = -2$ and
$\dfrac{af-gh}{h^{2}-ab} = \dfrac{2(7)-4\left(\frac72\right)}{\frac{25}{4}} = 0$ ✓.
:::

```figure caption="The equation $2x^{2}+7xy+3y^{2}+8x+14y+8=0$ is the pair of lines $x+3y+2=0$ and $2x+y+4=0$, meeting at $(-2,0)$ at $45^{\circ}$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6,3.0))
xs = np.linspace(-6.0, 2.0, 200)
ax.plot(xs, -(xs+2)/3.0, color=ACCENT, lw=2.0, label=r'$x+3y+2=0$')
ax.plot(xs, -2*xs-4, color='#2e8b57', lw=2.0, label=r'$2x+y+4=0$')
P = np.array([-2.0, 0.0])
a1 = np.arctan2(-1, 3); a2 = np.arctan2(-2, 1)
t = np.linspace(a2, a1, 40)
ax.plot(P[0]+1.0*np.cos(t), P[1]+1.0*np.sin(t), color='#d9534f', lw=1.3)
ax.annotate(r'$45^{\circ}$', (P[0]+1.5*np.cos((a1+a2)/2), P[1]+1.5*np.sin((a1+a2)/2)),
            ha='center', va='center', color='#d9534f', fontsize=10)
ax.plot([P[0]],[P[1]],'o',color=INK,ms=5.5)
ax.annotate('(-2, 0)', P, textcoords='offset points', xytext=(-6,10),
            ha='right', color=INK, fontsize=9.5)
ax.axhline(0, color=INK, lw=0.9); ax.axvline(0, color=INK, lw=0.9)
ax.set_xlim(-6.0,2.0); ax.set_ylim(-3.4,3.4)
ax.set_xticks([-4,-2,0,2]); ax.set_yticks([-2,0,2])
ax.spines[['top','right']].set_visible(False)
ax.legend(loc='upper left', fontsize=8.0)
```

::: example Worked example 12.2 — finding a missing coefficient
**Problem.** Find the values of $k$ for which $2x^{2}+kxy+3y^{2}-5x-5y+2 = 0$
represents a pair of straight lines, and write down the lines for the larger
value.

**Solution.** Here $a=2$, $b=3$, $c=2$, $h=\frac{k}{2}$, $g=-\frac52$, $f=-\frac52$.
Substituting into $\Delta = 0$:

$$ (2)(3)(2)+2\left(-\tfrac52\right)\left(-\tfrac52\right)\left(\tfrac{k}{2}\right)
-2\left(-\tfrac52\right)^{2}-3\left(-\tfrac52\right)^{2}-2\left(\tfrac{k}{2}\right)^{2} = 0 $$

$$ 12+\frac{25k}{4}-\frac{25}{2}-\frac{75}{4}-\frac{k^{2}}{2} = 0 $$

Multiplying by $4$: $48+25k-50-75-2k^{2} = 0$, that is

$$ 2k^{2}-25k+77 = 0 $$

$$ k = \frac{25\pm\sqrt{625-616}}{4} = \frac{25\pm 3}{4} = 7 \ \text{or}\ \frac{11}{2} $$

For $k = 7$ the equation is $2x^{2}+7xy+3y^{2}-5x-5y+2 = 0$, which factorises as

$$ (x+3y-2)(2x+y-1) = 0 $$

so the lines are $x+3y-2 = 0$ and $2x+y-1 = 0$.
:::

::: example Worked example 12.3 — a pair of parallel lines
**Problem.** Show that $x^{2}+4xy+4y^{2}+2x+4y-3 = 0$ represents a pair of
parallel lines and find the distance between them.

**Solution.** Here $a=1$, $h=2$, $b=4$, so $h^{2}-ab = 4-4 = 0$: the "point of
intersection" formula breaks down, which is exactly the signature of **parallel**
lines.

The second-degree part is $x^{2}+4xy+4y^{2} = (x+2y)^{2}$, so put $u = x+2y$:

$$ u^{2}+2u-3 = 0 \;\Rightarrow\; (u+3)(u-1) = 0 $$

The lines are $x+2y+3 = 0$ and $x+2y-1 = 0$. They are parallel (same $a$, $b$),
and the distance between them is

$$ d = \frac{|3-(-1)|}{\sqrt{1^{2}+2^{2}}} = \frac{4}{\sqrt{5}} = \frac{4\sqrt{5}}{5} \approx 1.79\ \text{units} $$
:::

```figure caption="A degenerate case: $x^{2}+4xy+4y^{2}+2x+4y-3=0$ is the pair of parallel lines $x+2y+3=0$ and $x+2y-1=0$, a distance $4/\sqrt{5}$ apart."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.4,2.8))
xs = np.array([-4.0, 3.0])
for c, col, lab in [(3.0, ACCENT, r'$x+2y+3=0$'), (-1.0, '#2e8b57', r'$x+2y-1=0$')]:
    ax.plot(xs, -(xs+c)/2.0, color=col, lw=2.0, label=lab)
n = np.array([1.0,2.0])/np.sqrt(5)
P = np.array([-1.0, -(-1.0+3.0)/2.0])
Q = P+(4/np.sqrt(5))*n
ax.annotate('', xy=(Q[0],Q[1]), xytext=(P[0],P[1]),
            arrowprops=dict(arrowstyle='<->', color='#d9534f', lw=1.6, mutation_scale=10))
ax.annotate(r'$4/\sqrt{5}$', (P+Q)/2, textcoords='offset points', xytext=(12,-8),
            color='#d9534f', fontsize=10)
ax.axhline(0, color=INK, lw=0.9); ax.axvline(0, color=INK, lw=0.9)
ax.set_xlim(-4.4,3.4); ax.set_ylim(-3.2,3.0)
ax.set_xticks([-4,-2,0,2]); ax.set_yticks([-2,0,2])
ax.set_aspect('equal')
ax.spines[['top','right']].set_visible(False)
ax.legend(loc='lower left', fontsize=8.0)
```

## 12.2 Homogeneous second degree equation in x and y

An equation is **homogeneous** of degree two when every term has total degree
exactly two:

$$ ax^{2}+2hxy+by^{2} = 0 $$

Putting $x=0$, $y=0$ satisfies it, so **every such pair passes through the
origin**. This is the case $g=f=c=0$, for which $\Delta = 0$ automatically — a
homogeneous second-degree equation *always* represents a pair of lines through
the origin (real if $h^{2}\ge ab$).

::: derivation Slopes of the two lines
Neither line is vertical when $b \ne 0$, so write each as $y = mx$. Substituting,

$$ ax^{2}+2hmx^{2}+bm^{2}x^{2} = 0 \;\Rightarrow\; bm^{2}+2hm+a = 0 $$

This quadratic has the two slopes $m_1$, $m_2$ as its roots, so

$$ m_1+m_2 = -\frac{2h}{b}, \qquad m_1m_2 = \frac{a}{b} $$

Equivalently, $ax^{2}+2hxy+by^{2} = b(y-m_1x)(y-m_2x)$.
:::

::: key Two quick tests
- **Perpendicular** lines: $m_1m_2 = -1$, i.e. $\dfrac{a}{b} = -1$, i.e.
  $$ a+b = 0 $$ — the coefficient of $x^{2}$ plus the coefficient of $y^{2}$ is zero.
- **Coincident** lines: $m_1 = m_2$, i.e. $h^{2} = ab$.
:::

::: example Worked example 12.4 — separating a homogeneous pair
**Problem.** Find the separate equations of the lines represented by
$6x^{2}+5xy-6y^{2} = 0$, and show that they are perpendicular.

**Solution.** Split the middle term: $5xy = 9xy-4xy$, so

$$ 6x^{2}+9xy-4xy-6y^{2} = 3x(2x+3y)-2y(2x+3y) = (3x-2y)(2x+3y) $$

The lines are $3x-2y = 0$ and $2x+3y = 0$, with slopes $\frac32$ and $-\frac23$.
Their product is $-1$, so the lines are perpendicular.

**Check by the rule.** $a+b = 6+(-6) = 0$ ✓.
:::

```figure caption="The homogeneous equation $6x^{2}+5xy-6y^{2}=0$ splits into $3x-2y=0$ and $2x+3y=0$ — a perpendicular pair through the origin, since $a+b=0$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.2,2.9))
xs = np.linspace(-2.4, 2.4, 100)
ax.plot(xs, 1.5*xs, color=ACCENT, lw=2.0, label=r'$3x-2y=0$')
ax.plot(xs, -2*xs/3.0, color='#2e8b57', lw=2.0, label=r'$2x+3y=0$')
u1 = np.array([2,3])/np.sqrt(13); u2 = np.array([3,-2])/np.sqrt(13)
s = 0.32
ax.plot([s*u1[0], s*(u1[0]+u2[0]), s*u2[0]],
        [s*u1[1], s*(u1[1]+u2[1]), s*u2[1]], color=MUTED, lw=1.0)
ax.plot([0],[0],'o',color=INK,ms=5)
ax.annotate('O', (0,0), textcoords='offset points', xytext=(-16,-15),
            color=INK, fontsize=10)
ax.axhline(0, color=INK, lw=0.9); ax.axvline(0, color=INK, lw=0.9)
ax.set_xlim(-2.6,2.6); ax.set_ylim(-2.6,2.6)
ax.set_xticks([-2,0,2]); ax.set_yticks([-2,0,2]); ax.set_aspect('equal')
ax.spines[['top','right']].set_visible(False)
ax.legend(loc='lower right', fontsize=8.0)
```

### Lines joining the origin to the intersection of a line and a curve

This is a standard exam problem and the only real use of **homogenisation**.
To find the pair of lines joining the origin to the points where the line
$lx+my = n$ cuts the curve $S = 0$, rewrite the line as $\dfrac{lx+my}{n} = 1$ and
use it to multiply up every term of $S$ until every term has degree two. The
resulting homogeneous equation is the required pair.

::: example Worked example 12.5 — homogenisation
**Problem.** Find the equation of the pair of lines joining the origin to the
points of intersection of $x+y = 3$ and $x^{2}+y^{2} = 5$, and the angle between
them.

**Solution.** Write the line as $\dfrac{x+y}{3} = 1$. The curve is
$x^{2}+y^{2} = 5\cdot 1^{2}$, so replacing the $1$:

$$ x^{2}+y^{2} = 5\left(\frac{x+y}{3}\right)^{2} $$

$$ 9x^{2}+9y^{2} = 5\left(x^{2}+2xy+y^{2}\right) $$

$$ 4x^{2}-10xy+4y^{2} = 0 \;\Rightarrow\; 2x^{2}-5xy+2y^{2} = 0 $$

Factorising, $(x-2y)(2x-y) = 0$, so the lines are $y = \frac{x}{2}$ and $y = 2x$.

**Angle.** With $m_1 = 2$, $m_2 = \frac12$,

$$ \tan\theta = |\frac{2-\frac12}{1+1}| = \frac{3}{4}
\;\Rightarrow\; \theta = \tan^{-1}\frac34 \approx 36.87^{\circ} $$

**Check directly.** From $x+y=3$ and $x^{2}+y^{2}=5$ we get $2xy = 9-5 = 4$, so
$xy=2$; $x$ and $y$ are the roots of $t^{2}-3t+2 = 0$, namely $1$ and $2$. The
intersection points are $(1,2)$ and $(2,1)$, and the lines from the origin
through them are indeed $y=2x$ and $y=\frac{x}{2}$ ✓.
:::

```figure caption="Worked example 12.5: the chord $x+y=3$ cuts the circle $x^{2}+y^{2}=5$ at $(1,2)$ and $(2,1)$; the lines from the origin to these points are $2x^{2}-5xy+2y^{2}=0$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.2,3.0))
t = np.linspace(0, 2*np.pi, 300)
r = np.sqrt(5)
ax.plot(r*np.cos(t), r*np.sin(t), color=MUTED, lw=1.3)
xs = np.linspace(-0.4, 3.2, 50)
ax.plot(xs, 3-xs, color='#b8860b', lw=1.6)
ax.annotate(r'$x+y=3$', (3.0, 0.0), textcoords='offset points', xytext=(0,-13),
            ha='right', va='top', color='#b8860b', fontsize=9)
for P, col in [((1,2), ACCENT), ((2,1), '#2e8b57')]:
    ax.plot([0,P[0]],[0,P[1]], color=col, lw=2.0)
    ax.plot([P[0]],[P[1]],'o',color=col,ms=5)
    ax.annotate(f'({P[0]}, {P[1]})', P, textcoords='offset points',
                xytext=(7,4), color=INK, fontsize=9)
ax.plot([0],[0],'o',color=INK,ms=4.5)
ax.annotate('O', (0,0), textcoords='offset points', xytext=(-16,-15),
            color=INK, fontsize=10)
ax.axhline(0, color=INK, lw=0.9); ax.axvline(0, color=INK, lw=0.9)
ax.set_xlim(-2.8,3.4); ax.set_ylim(-2.8,3.0)
ax.set_xticks([-2,0,2]); ax.set_yticks([-2,0,2]); ax.set_aspect('equal')
ax.spines[['top','right']].set_visible(False)
```

::: example Worked example 12.6 — the perpendicular pair
**Problem.** Find the equation of the pair of lines through the origin
perpendicular to the pair $6x^{2}-xy-y^{2} = 0$.

**Solution.** First separate: $6x^{2}-3xy+2xy-y^{2} = 3x(2x-y)+y(2x-y) = (2x-y)(3x+y)$,
so the lines are $y = 2x$ and $y = -3x$.

The perpendiculars through the origin have slopes $-\frac12$ and $\frac13$, i.e.
$x+2y = 0$ and $x-3y = 0$. Multiplying,

$$ (x+2y)(x-3y) = x^{2}-xy-6y^{2} = 0 $$

**The general rule.** Replacing $m$ by $-\frac1m$ in $bm^{2}+2hm+a = 0$ turns it
into $a m^{2}-2hm+b = 0$, so the perpendicular pair to $ax^{2}+2hxy+by^{2}=0$ is

$$ bx^{2}-2hxy+ay^{2} = 0 $$

With $a=6$, $h=-\frac12$, $b=-1$ this gives $-x^{2}+xy+6y^{2} = 0$, i.e.
$x^{2}-xy-6y^{2} = 0$ ✓.
:::

## 12.3 Angle between the pair of lines

::: derivation The angle formula
Let the lines be $y = m_1x$ and $y = m_2x$, so $m_1+m_2 = -\dfrac{2h}{b}$ and
$m_1m_2 = \dfrac{a}{b}$. The angle $\theta$ between them satisfies

$$ \tan\theta = |\frac{m_1-m_2}{1+m_1m_2}| $$

Now $(m_1-m_2)^{2} = (m_1+m_2)^{2}-4m_1m_2 = \dfrac{4h^{2}}{b^{2}}-\dfrac{4a}{b}
= \dfrac{4(h^{2}-ab)}{b^{2}}$, so $|m_1-m_2| = \dfrac{2\sqrt{h^{2}-ab}}{|b|}$. Also
$1+m_1m_2 = 1+\dfrac{a}{b} = \dfrac{a+b}{b}$. Hence

$$ \tan\theta = \frac{2\sqrt{h^{2}-ab}\,/\,|b|}{|a+b|\,/\,|b|}
= \frac{2\sqrt{h^{2}-ab}}{|a+b|} $$

Usually written without the modulus, with the sign chosen to give the acute angle:

$$ \tan\theta = \frac{2\sqrt{h^{2}-ab}}{a+b} $$
:::

The same formula works for a **general** second-degree pair, because shifting the
origin to the point of intersection leaves $a$, $h$, $b$ unchanged and kills
$g$, $f$, $c$. So the angle depends only on the second-degree terms.

::: key Special cases, read straight off
| Condition | Meaning |
|---|---|
| $a+b = 0$ | the lines are perpendicular ($\theta = 90^{\circ}$) |
| $h^{2} = ab$ | the lines are coincident ($\theta = 0$) |
| $h^{2} > ab$ | real, distinct lines |
| $h^{2} < ab$ | no real lines |
:::

::: example Worked example 12.7 — angle of a homogeneous pair
**Problem.** Find the angle between the lines represented by $6x^{2}-xy-y^{2} = 0$.

**Solution.** Here $a = 6$, $2h = -1$ so $h = -\frac12$, and $b = -1$.

$$ h^{2}-ab = \frac14+6 = \frac{25}{4}, \qquad \sqrt{h^{2}-ab} = \frac52 $$

$$ \tan\theta = \frac{2\left(\frac52\right)}{6+(-1)} = \frac{5}{5} = 1
\;\Rightarrow\; \theta = 45^{\circ} $$

**Check.** The lines are $y = 2x$ and $y = -3x$, and
$|\dfrac{2-(-3)}{1+2(-3)}| = |\dfrac{5}{-5}| = 1$ ✓.
:::

```figure caption="The pair $6x^{2}-xy-y^{2}=0$ is $y=2x$ and $y=-3x$; the acute angle between them is $\tan^{-1}1=45^{\circ}$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.2,2.9))
xs = np.linspace(-1.5, 1.5, 100)
ax.plot(xs, 2*xs, color=ACCENT, lw=2.0, label=r'$2x-y=0$')
ax.plot(xs, -3*xs, color='#2e8b57', lw=2.0, label=r'$3x+y=0$')
a1 = np.arctan2(2,1); a2 = np.arctan2(-3,1)+np.pi
t = np.linspace(a1, a2, 60)
ax.plot(1.0*np.cos(t), 1.0*np.sin(t), color='#d9534f', lw=1.3)
ax.annotate(r'$45^{\circ}$', (1.35*np.cos((a1+a2)/2), 1.35*np.sin((a1+a2)/2)),
            ha='center', va='center', color='#d9534f', fontsize=10)
ax.plot([0],[0],'o',color=INK,ms=4.5)
ax.axhline(0, color=INK, lw=0.9); ax.axvline(0, color=INK, lw=0.9)
ax.set_xlim(-2.2,2.2); ax.set_ylim(-3.4,3.4)
ax.set_xticks([-2,0,2]); ax.set_yticks([-2,0,2])
ax.spines[['top','right']].set_visible(False)
ax.legend(loc='lower left', fontsize=8.0, frameon=True, framealpha=0.92,
          facecolor='white', edgecolor='none', borderpad=0.35)
```

::: example Worked example 12.8 — angle of a general pair
**Problem.** Find the acute angle between the lines represented by
$2x^{2}+7xy+3y^{2}+8x+14y+8 = 0$.

**Solution.** Only $a$, $h$, $b$ matter: $a=2$, $h=\frac72$, $b=3$.

$$ h^{2}-ab = \frac{49}{4}-6 = \frac{25}{4} $$

$$ \tan\theta = \frac{2\sqrt{\frac{25}{4}}}{2+3} = \frac{2\left(\frac52\right)}{5} = 1
\;\Rightarrow\; \theta = 45^{\circ} $$

This agrees with Worked example 12.1, where the lines came out as $x+3y+2=0$
(slope $-\frac13$) and $2x+y+4=0$ (slope $-2$):
$|\dfrac{-\frac13+2}{1+\frac23}| = \dfrac{\frac53}{\frac53} = 1$ ✓.
:::

## 12.4 Bisectors of the angles between the pair of lines

::: derivation Equation of the bisector pair
Take the pair $ax^{2}+2hxy+by^{2} = 0$ through the origin, with separate equations
$y-m_1x = 0$ and $y-m_2x = 0$. A point $P(x,y)$ on a bisector is equidistant from
both lines:

$$ \frac{|y-m_1x|}{\sqrt{1+m_1^{2}}} = \frac{|y-m_2x|}{\sqrt{1+m_2^{2}}} $$

Squaring to remove the moduli,

$$ \left(1+m_2^{2}\right)(y-m_1x)^{2} = \left(1+m_1^{2}\right)(y-m_2x)^{2} $$

Expanding and collecting, all the terms in $x^{2}$, $xy$ and $y^{2}$ regroup as

$$ \left(m_1+m_2\right)\left(x^{2}-y^{2}\right) = 2\left(1-m_1m_2\right)xy $$

Now substitute $m_1+m_2 = -\dfrac{2h}{b}$ and $m_1m_2 = \dfrac{a}{b}$:

$$ -\frac{2h}{b}\left(x^{2}-y^{2}\right) = 2\left(1-\frac{a}{b}\right)xy
= \frac{2(b-a)}{b}\,xy $$

Multiplying by $-\dfrac{b}{2}$ gives $h\left(x^{2}-y^{2}\right) = (a-b)xy$, usually
quoted as

$$ \frac{x^{2}-y^{2}}{a-b} = \frac{xy}{h} $$
:::

::: key Properties of the bisector pair
- $h\left(x^{2}-y^{2}\right)-(a-b)xy = 0$ is itself a homogeneous second-degree
  equation, so it is a **pair of lines through the origin**.
- For it, the coefficient of $x^{2}$ is $h$ and of $y^{2}$ is $-h$, whose sum is
  zero — so **the two bisectors are always perpendicular**, whatever the original
  pair.
- If the pair does not pass through the origin, first shift the origin to the
  point of intersection $(x_0,y_0)$, apply the formula, then shift back by
  replacing $x$ with $x-x_0$ and $y$ with $y-y_0$.
:::

::: example Worked example 12.9 — bisectors of a homogeneous pair
**Problem.** Find the equation of the bisectors of the angles between the lines
$6x^{2}-xy-y^{2} = 0$.

**Solution.** Here $a = 6$, $h = -\frac12$, $b = -1$, so $a-b = 7$ and

$$ \frac{x^{2}-y^{2}}{7} = \frac{xy}{-\frac12} = -2xy $$

$$ x^{2}-y^{2} = -14xy \;\Rightarrow\; x^{2}+14xy-y^{2} = 0 $$

**Check.** The sum of the coefficients of $x^{2}$ and $y^{2}$ is $1+(-1) = 0$, so
the bisectors are perpendicular ✓. Their slopes satisfy $1+14m-m^{2} = 0$, i.e.
$m^{2}-14m-1 = 0$, giving $m = 7\pm 5\sqrt{2}$ — approximately $14.07$ and
$-0.071$, whose product is $49-50 = -1$ ✓.
:::

```figure caption="The pair $6x^{2}-xy-y^{2}=0$ (solid) with its angle bisectors $x^{2}+14xy-y^{2}=0$ (dashed). The bisectors are perpendicular to each other."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.4,3.2))
xs = np.linspace(-2.2, 2.2, 100)
ax.plot(xs, 2*xs, color=ACCENT, lw=2.0, label=r'$2x-y=0$')
ax.plot(xs, -3*xs, color='#2e8b57', lw=2.0, label=r'$3x+y=0$')
m1, m2 = 7+5*np.sqrt(2), 7-5*np.sqrt(2)
ax.plot(xs, m2*xs, color='#d9534f', lw=1.5, ls='--', label='bisectors')
ys = np.linspace(-3.2, 3.2, 100)
ax.plot(ys/m1, ys, color='#d9534f', lw=1.5, ls='--')
ax.plot([0],[0],'o',color=INK,ms=4.5)
ax.axhline(0, color=INK, lw=0.9); ax.axvline(0, color=INK, lw=0.9)
ax.set_xlim(-2.4,2.4); ax.set_ylim(-3.4,3.4)
ax.set_xticks([-2,0,2]); ax.set_yticks([-2,0,2])
ax.spines[['top','right']].set_visible(False)
ax.legend(loc='lower left', fontsize=8.0, frameon=True, framealpha=0.92,
          facecolor='white', edgecolor='none', borderpad=0.35)
```

::: example Worked example 12.10 — bisectors of a general pair
**Problem.** Find the bisectors of the angles between the lines
$2x^{2}+7xy+3y^{2}+8x+14y+8 = 0$.

**Solution.** From Worked example 12.1 the lines meet at $(-2,0)$. Shift the
origin there by putting $X = x+2$, $Y = y$, i.e. $x = X-2$, $y = Y$:

$$ 2(X-2)^{2}+7(X-2)Y+3Y^{2}+8(X-2)+14Y+8 = 2X^{2}+7XY+3Y^{2} $$

(as it must be — the shifted pair passes through the new origin). Now apply the
formula with $a=2$, $h=\frac72$, $b=3$, so $a-b = -1$:

$$ \frac{X^{2}-Y^{2}}{-1} = \frac{XY}{\frac72} \;\Rightarrow\;
\frac{7}{2}\left(Y^{2}-X^{2}\right) = XY $$

$$ 7X^{2}+2XY-7Y^{2} = 0 $$

Shifting back with $X = x+2$, $Y = y$:

$$ 7(x+2)^{2}+2(x+2)y-7y^{2} = 0 $$

that is, $7x^{2}+2xy-7y^{2}+28x+4y+28 = 0$.

**Check.** Coefficients of $x^{2}$ and $y^{2}$ sum to $7-7 = 0$, so the two
bisectors are perpendicular ✓, and both pass through $(-2,0)$, since substituting
gives $7(0)+2(0)(0)-0 = 0$ ✓.
:::

::: tip Two-second sanity checks
Before you write the final line of any answer in this unit, check the pair you
have found: multiply your two separate equations back out and compare with the
original; and for any bisector pair confirm that the $x^{2}$ and $y^{2}$
coefficients are negatives of each other.
:::

## Chapter summary

- $ax^{2}+2hxy+by^{2}+2gx+2fy+c = 0$ represents a pair of straight lines exactly
  when $\Delta = abc+2fgh-af^{2}-bg^{2}-ch^{2} = 0$. Remember $h$, $g$, $f$ are
  **half** the coefficients of $xy$, $x$, $y$.
- The lines are real and distinct if $h^{2}>ab$, coincident if $h^{2}=ab$,
  parallel if $h^{2}=ab$ with the pair not degenerate, and not real if $h^{2}<ab$.
- They meet at $\left(\dfrac{bg-fh}{h^{2}-ab},\ \dfrac{af-gh}{h^{2}-ab}\right)$.
- A homogeneous equation $ax^{2}+2hxy+by^{2} = 0$ always represents two lines
  **through the origin**, with $m_1+m_2 = -\dfrac{2h}{b}$ and $m_1m_2 = \dfrac{a}{b}$.
- Angle between the pair: $\tan\theta = \dfrac{2\sqrt{h^{2}-ab}}{a+b}$; they are
  perpendicular when $a+b = 0$ and coincident when $h^{2} = ab$.
- The pair through the origin perpendicular to $ax^{2}+2hxy+by^{2}=0$ is
  $bx^{2}-2hxy+ay^{2} = 0$.
- The bisectors of the angles between the pair are
  $\dfrac{x^{2}-y^{2}}{a-b} = \dfrac{xy}{h}$; they are always perpendicular to
  each other.
- To find the lines joining the origin to the intersections of $lx+my=n$ with a
  curve, **homogenise** the curve using $\dfrac{lx+my}{n} = 1$.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The equation $x^{2}-y^{2} = 0$ represents <span class="marks">[1]</span>
   (a) a circle (b) two perpendicular lines (c) one line (d) no real locus
2. The lines $ax^{2}+2hxy+by^{2}=0$ are perpendicular if <span class="marks">[1]</span>
   (a) $h^{2}=ab$ (b) $a+b=0$ (c) $ab=1$ (d) $h=0$
3. The angle between the pair $x^{2}-2xy+y^{2}=0$ is <span class="marks">[1]</span>
   (a) $0^{\circ}$ (b) $30^{\circ}$ (c) $60^{\circ}$ (d) $90^{\circ}$
4. The bisectors of the angles between a pair of lines are always <span class="marks">[1]</span>
   (a) parallel (b) perpendicular (c) coincident (d) inclined at $60^{\circ}$
5. In $3x^{2}+5xy-2y^{2}+4x-7y+2=0$, the value of $h$ is <span class="marks">[1]</span>
   (a) $5$ (b) $\frac52$ (c) $-2$ (d) $2$
6. The lines represented by $2x^{2}+5xy+2y^{2}=0$ pass through <span class="marks">[1]</span>
   (a) $(1,1)$ (b) $(0,0)$ (c) $(2,2)$ (d) $(1,0)$

::: note Answers to Group A
**1.** (b) — $(x-y)(x+y)=0$, slopes $1$ and $-1$, product $-1$.
**2.** (b) — $m_1m_2 = a/b = -1$ gives $a+b=0$.
**3.** (a) — $h^{2}-ab = 1-1 = 0$, so the lines coincide: $(x-y)^{2}=0$.
**4.** (b) — the bisector pair has $x^{2}$ and $y^{2}$ coefficients $h$ and $-h$, summing to zero.
**5.** (b) — $2h$ is the coefficient of $xy$, so $h = \frac52$.
**6.** (b) — every homogeneous second-degree equation is satisfied by $(0,0)$.
:::

**Group B — Short answer (5 marks each)**

1. Find the separate equations of the lines represented by
   $3x^{2}-8xy-3y^{2} = 0$ and the angle between them. <span class="marks">[5]</span>
2. Find the value of $\lambda$ for which $6x^{2}+11xy-10y^{2}+x+31y+\lambda = 0$
   represents a pair of straight lines. <span class="marks">[5]</span>
3. Prove that the equation $x^{2}+4xy+4y^{2}+4x+8y+3 = 0$ represents a pair of
   parallel lines and find the distance between them. <span class="marks">[5]</span>
4. Find the equation of the bisectors of the angles between the lines
   $2x^{2}-5xy+2y^{2} = 0$. <span class="marks">[5]</span>
5. Find the equation of the pair of lines through the origin perpendicular to
   $x^{2}-3xy+2y^{2} = 0$. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Split the middle term: $3x^{2}-9xy+xy-3y^{2} = 3x(x-3y)+y(x-3y) = (x-3y)(3x+y)$.
So the lines are $x-3y = 0$ and $3x+y = 0$, with slopes $\frac13$ and $-3$. Since
$a+b = 3+(-3) = 0$ the lines are perpendicular, $\theta = 90^{\circ}$ (and indeed
$\frac13\times(-3) = -1$).

**2.** $a=6$, $h=\frac{11}{2}$, $b=-10$, $g=\frac12$, $f=\frac{31}{2}$, $c=\lambda$.
$$ \Delta = 6(-10)\lambda+2\left(\tfrac{31}{2}\right)\left(\tfrac12\right)\left(\tfrac{11}{2}\right)-6\left(\tfrac{31}{2}\right)^{2}+10\left(\tfrac12\right)^{2}-\lambda\left(\tfrac{11}{2}\right)^{2} $$
$$ = -60\lambda+\frac{341}{4}-\frac{2883}{2}+\frac{5}{2}-\frac{121\lambda}{4} $$
Multiplying through by $4$:
$$ -240\lambda+341-5766+10-121\lambda = 0 \;\Rightarrow\; -361\lambda-5415 = 0 $$
$$ \lambda = -\frac{5415}{361} = -15 $$
**Check.** With $\lambda=-15$ the equation factorises as $(3x-2y+5)(2x+5y-3) = 0$,
which expands to $6x^{2}+11xy-10y^{2}+x+31y-15$ ✓.

**3.** $a=1$, $h=2$, $b=4$, so $h^{2}-ab = 4-4 = 0$ and the lines are parallel.
Also $a=1$, $g=2$, $f=4$, $c=3$ give
$\Delta = (1)(4)(3)+2(4)(2)(2)-1(4)^{2}-4(2)^{2}-3(2)^{2} = 12+32-16-16-12 = 0$,
so it is a pair of lines. Putting $u = x+2y$, the equation is $u^{2}+4u+3 = 0$,
i.e. $(u+1)(u+3) = 0$. The lines are $x+2y+1 = 0$ and $x+2y+3 = 0$, and
$d = \dfrac{|3-1|}{\sqrt{1+4}} = \dfrac{2}{\sqrt{5}} = \dfrac{2\sqrt{5}}{5} \approx 0.894$ units.

**4.** For $2x^{2}-5xy+2y^{2} = 0$: $a = 2$, $h = -\frac52$, $b = 2$, so $a-b = 0$.
Written as $h(x^{2}-y^{2}) = (a-b)xy$ the bisector equation reads
$-\frac52(x^{2}-y^{2}) = 0$, so
$$ x^{2}-y^{2} = 0 \;\Rightarrow\; y = x \ \text{and}\ y = -x $$
This is right: the original lines are $(x-2y)(2x-y) = 0$, i.e. $y = \frac{x}{2}$
and $y = 2x$, which are mirror images of each other in $y = x$.

**5.** For $ax^{2}+2hxy+by^{2} = 0$ the perpendicular pair through the origin is
$bx^{2}-2hxy+ay^{2} = 0$. With $a = 1$, $2h = -3$, $b = 2$:
$$ 2x^{2}+3xy+y^{2} = 0 \;\Rightarrow\; (2x+y)(x+y) = 0 $$
**Check.** The original pair is $(x-2y)(x-y) = 0$, slopes $\frac12$ and $1$; the
new pair has slopes $-2$ and $-1$. Each product is $-1$ ✓.
:::

**Group C — Long answer (8 marks each)**

1. (a) Derive the formula $\tan\theta = \dfrac{2\sqrt{h^{2}-ab}}{a+b}$ for the
   angle between the lines $ax^{2}+2hxy+by^{2} = 0$. <span class="marks">[5]</span>
   (b) Hence find the angle between the lines
   $2x^{2}+7xy+3y^{2}+8x+14y+8 = 0$. <span class="marks">[3]</span>
2. (a) Show that $x^{2}+4xy+3y^{2}+4x+10y+3 = 0$ represents a pair of straight
   lines and find them. <span class="marks">[5]</span>
   (b) Find their point of intersection and the angle between them. <span class="marks">[3]</span>

::: note Answers to Group C
**1.** (a) Writing each line as $y = mx$ and substituting gives
$bm^{2}+2hm+a = 0$, so $m_1+m_2 = -\frac{2h}{b}$ and $m_1m_2 = \frac{a}{b}$. Then
$$ (m_1-m_2)^{2} = (m_1+m_2)^{2}-4m_1m_2 = \frac{4h^{2}}{b^{2}}-\frac{4a}{b} = \frac{4(h^{2}-ab)}{b^{2}} $$
so $|m_1-m_2| = \frac{2\sqrt{h^{2}-ab}}{|b|}$, while $1+m_1m_2 = \frac{a+b}{b}$.
Substituting in $\tan\theta = |\frac{m_1-m_2}{1+m_1m_2}|$ and cancelling
$|b|$ gives $\tan\theta = \frac{2\sqrt{h^{2}-ab}}{a+b}$.

(b) $a = 2$, $h = \frac72$, $b = 3$, so $h^{2}-ab = \frac{49}{4}-6 = \frac{25}{4}$ and
$\tan\theta = \frac{2\cdot\frac52}{5} = 1$, giving $\theta = 45^{\circ}$.

**2.** (a) $a=1$, $h=2$, $b=3$, $g=2$, $f=5$, $c=3$.
$$ \Delta = (1)(3)(3)+2(5)(2)(2)-1(5)^{2}-3(2)^{2}-3(2)^{2} = 9+40-25-12-12 = 0 $$
So it is a pair of lines, and $h^{2}-ab = 4-3 = 1 > 0$, so they are real and
distinct. Since $x^{2}+4xy+3y^{2} = (x+y)(x+3y)$, try
$(x+y+p)(x+3y+q)$. Matching the $x$ terms: $p+q = 4$; matching the $y$ terms:
$3p+q = 10$. Subtracting, $2p = 6$, so $p = 3$ and $q = 1$; the constant is
$pq = 3$ ✓. The lines are
$$ x+y+3 = 0 \quad\text{and}\quad x+3y+1 = 0 $$

(b) Subtracting the equations gives $-2y+2 = 0$, so $y = 1$ and then $x = -4$:
they meet at $(-4,\,1)$. (Formula check:
$\frac{bg-fh}{h^{2}-ab} = \frac{3(2)-5(2)}{1} = -4$ and
$\frac{af-gh}{h^{2}-ab} = \frac{1(5)-2(2)}{1} = 1$ ✓.)
The angle: $\tan\theta = \frac{2\sqrt{1}}{1+3} = \frac12$, so
$\theta = \tan^{-1}\frac12 \approx 26.57^{\circ}$. (Direct check: slopes $-1$ and
$-\frac13$, and $|\frac{-1+\frac13}{1+\frac13}| = \frac{2/3}{4/3} = \frac12$ ✓.)
:::
