---
subject: Mathematics
grade: 12
unit: 8
title: Conic Sections
hours: 20
area: Analytic Geometry
---

Slice a double cone with a flat plane and the edge of the cut is a **conic
section**. Tilt the plane a little and you get a circle, an ellipse, a parabola
or a hyperbola — four curves that look different but come from one construction
and obey one rule. This is the longest unit in Analytic Geometry, and it is the
most mechanical: almost every question is *find the curve from its data* or
*find the data from its curve*, plus a tangent. Learn the four standard
equations and the table of elements that goes with each, and the unit becomes
arithmetic.

```figure caption="One plane, four curves. As the cutting plane tilts from perpendicular to the axis (circle) past the slant of the cone (parabola) and beyond (hyperbola, which cuts both nappes), the section changes shape. The eccentricity $e$ measures the tilt."
import numpy as np, matplotlib.pyplot as plt

fig = plt.figure(figsize=(5.2, 4.5))
H = 2.2
th = np.linspace(0, 2*np.pi, 90)
zc = np.linspace(-H, H, 60)
TH, ZC = np.meshgrid(th, zc)
Xc, Yc = np.abs(ZC)*np.cos(TH), np.abs(ZC)*np.sin(TH)

#        m     c     x-range of plane patch        name        subtitle
cases = [(0.0, 1.35, (-1.9, 1.9), 'Circle',    'plane ⊥ axis,  e = 0'),
         (0.35, 1.0, (-1.1, 1.9), 'Ellipse',   'tilt < slant,  e < 1'),
         (1.0, 1.15, (-1.4, 1.0), 'Parabola',  'tilt = slant,  e = 1'),
         (2.4, 0.70, (-1.2, 0.6), 'Hyperbola', 'tilt > slant,  e > 1')]

for k, (m, c, (xa, xb), name, sub) in enumerate(cases):
    ax = fig.add_subplot(2, 2, k+1, projection='3d')
    ax.plot_surface(Xc, Yc, ZC, color=MUTED, alpha=0.15, linewidth=0,
                    rstride=3, cstride=6, shade=False)
    for t0 in np.linspace(0, np.pi, 7):
        ax.plot([-H*np.cos(t0), 0, H*np.cos(t0)], [-H*np.sin(t0), 0, H*np.sin(t0)],
                [H, 0, H], color=MUTED, lw=0.5, alpha=0.75)
    ax.plot([0, 0], [0, 0], [-H, H], color=MUTED, lw=0.7, ls=':')

    s = np.linspace(-1.9, 1.9, 2)
    Xp, Yp = np.meshgrid(np.linspace(xa, xb, 2), s)
    ax.plot_surface(Xp, Yp, m*Xp + c, color=ACCENT, alpha=0.22, linewidth=0, shade=False)

    A, B, C = m*m - 1.0, 2*m*c, c*c
    xs = np.linspace(-4, 4, 2400)
    y2 = A*xs**2 + B*xs + C
    ok = (y2 >= 0) & (np.abs(m*xs + c) <= H) & (xs >= xa) & (xs <= xb)
    ys = np.sqrt(np.clip(y2, 0, None))
    idx = np.where(ok)[0]
    runs = np.split(idx, np.where(np.diff(idx) > 1)[0] + 1) if len(idx) else []
    for r in runs:
        if len(r) < 2: continue
        ax.plot(xs[r], ys[r], m*xs[r] + c, color='#d9534f', lw=2.1)
        ax.plot(xs[r], -ys[r], m*xs[r] + c, color='#d9534f', lw=2.1)
    ax.set_title(name + '\n' + sub, fontsize=8.2, pad=-6)
    ax.set_xlim(-H, H); ax.set_ylim(-H, H); ax.set_zlim(-H, H)
    ax.set_box_aspect((1, 1, 1.0), zoom=1.34)
    ax.view_init(elev=(26 if k == 1 else 13), azim=-62)
    ax.set_axis_off()
fig.subplots_adjust(left=0.0, right=1.0, top=0.99, bottom=0.0, wspace=-0.14, hspace=0.06)
```

The unified rule behind all four curves is a statement about distances.

::: definition Focus–directrix definition of a conic
A **conic section** is the set of all points $P$ in a plane whose distance from a
fixed point $S$ (the **focus**) is a constant multiple $e$ of its distance from a
fixed straight line (the **directrix**):

$$ \frac{PS}{PM} = e $$

where $PM$ is the perpendicular distance from $P$ to the directrix. The constant
$e$ is the **eccentricity**. The line through $S$ perpendicular to the directrix
is the **axis** of the conic; the point where the conic crosses its axis is a
**vertex**.
:::

```figure caption="Three conics sharing one focus $S$ and one directrix. The ratio $PS/PM$ is the same at every point of a given curve; its value decides the shape."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0, 3.9))
k = 2.0                       # focus S = (k, 0); directrix is the y-axis x = 0
YM = 2.7
ax.axvline(0, color=INK, lw=1.4)
ax.text(-0.18, 2.35, 'directrix', rotation=90, va='top', ha='right',
        fontsize=9.0, color=INK)
ax.axhline(0, color=MUTED, lw=0.7, ls=':')
for e, col, lab in [(0.6, SERIES[2], 'e = 0.6  ellipse'),
                    (1.0, ACCENT,    'e = 1  parabola'),
                    (1.5, SERIES[1], 'e = 1.5  hyperbola')]:
    x = np.linspace(-1, 8, 4000)
    y2 = (e*x)**2 - (x - k)**2
    m = (y2 >= 0) & (x >= 0) & (np.sqrt(np.clip(y2, 0, None)) <= YM)
    idx = np.where(m)[0]
    runs = np.split(idx, np.where(np.diff(idx) > 1)[0] + 1) if len(idx) else []
    for j, r in enumerate(runs):
        if len(r) < 2: continue
        yy = np.sqrt(y2[r])
        ax.plot(x[r], yy, color=col, lw=1.8, label=lab if j == 0 else None)
        ax.plot(x[r], -yy, color=col, lw=1.8)
ax.plot([k], [0], 'o', color=INK, ms=5)
ax.annotate('$S$ (focus)', (k, 0), textcoords='offset points', xytext=(2, -14),
            fontsize=9.4, color=INK)
# a point P on the ellipse, with PS and PM
xp = 4.2
yp = np.sqrt((0.6*xp)**2 - (xp - k)**2)
ax.plot([xp], [yp], 'o', color=INK, ms=5)
ax.plot([k, xp], [0, yp], color=INK, lw=1.3)
ax.plot([0, xp], [yp, yp], color=INK, lw=1.3, ls='--')
ax.plot([0], [yp], 'o', color=INK, ms=4)
ax.annotate('$P$', (xp, yp), textcoords='offset points', xytext=(5, 2), fontsize=9.4)
ax.annotate('$M$', (0, yp), textcoords='offset points', xytext=(5, 5), fontsize=9.4)
ax.annotate('$PS$', (3.1, yp/2 - 0.05), textcoords='offset points', xytext=(-24, -2),
            fontsize=9.2, color=INK)
ax.annotate('$PM$', (2.1, yp), textcoords='offset points', xytext=(-10, 5),
            fontsize=9.2, color=INK)
ax.text(2.55, -2.35, r'$\frac{PS}{PM} = e$  for every point $P$', fontsize=10.4,
        color=INK, ha='center')
ax.set_xlim(-0.75, 6.6); ax.set_ylim(-2.95, 2.95)
ax.set_aspect('equal'); ax.axis('off')
ax.legend(loc='upper right', fontsize=8.4, handlelength=1.4)
```

| Eccentricity | Curve |
|---|---|
| $e = 0$ | circle (a limiting case: the directrix moves off to infinity) |
| $0 < e < 1$ | ellipse |
| $e = 1$ | parabola |
| $e > 1$ | hyperbola |

### Recognising a conic from its equation

Every conic in this unit has an equation of the form

$$ Ax^{2} + By^{2} + 2gx + 2fy + c = 0 $$

with no $xy$ term, because we always choose axes parallel to the axes of the
curve. The two leading coefficients alone tell you which curve you have, before
any completing of squares.

| Signs of $A$ and $B$ | Curve |
|---|---|
| $A = B \ne 0$ | circle |
| exactly one of $A$, $B$ is zero | parabola |
| $A \ne B$, same sign | ellipse |
| $A$ and $B$ opposite in sign | hyperbola |

So $4x^{2}+9y^{2}-16x+18y-11=0$ is an ellipse (both positive, unequal),
$9x^{2}-16y^{2}=144$ is a hyperbola (opposite signs), and
$y^{2}-8y-4x+20=0$ is a parabola (no $x^{2}$ term at all). Identify the curve
first; the arithmetic that follows is then routine.

::: memory Order of work for any "find the elements" question
1. **Divide** so that the coefficient of the squared term(s) is tidy.
2. **Complete the square** in $x$, in $y$, or in both.
3. **Match** the result to a standard form and write down $a$ and $b$ (or $r$).
4. **Compute $e$** from the correct relation for that curve.
5. Only then quote centre/vertex, foci, directrices and latus rectum — each of
   them measured **from the centre or vertex**, not from the origin.

Steps 1-3 are worth marks on their own, so write them out even if you can see
the answer.
:::

A **latus rectum** is the chord through a focus perpendicular to the axis. Its
length appears in almost every question, so it is worth knowing for each curve.
Every conic is also described by a second-degree equation in $x$ and $y$; for the
curves in this unit that equation has no $xy$ term, so it always factors into a
recognisable standard form after completing the square.

::: key What the exam asks
Three question shapes cover the whole unit.
1. **Build the curve.** You are given a focus, a directrix, foci and an
   eccentricity, vertices, or the length of a latus rectum. Fit them into
   the standard equation.
2. **Read the curve.** You are given an equation, often untidy. Complete the
   square, match it to a standard form, then quote centre/vertex, foci,
   directrices, eccentricity and latus rectum.
3. **Tangency.** Either "is this line a tangent?" (use the condition) or
   "find the tangent and normal at this point" (use the $T = 0$ rule).

Write the standard form down first, every time. Most lost marks come from
starting to calculate before the equation has been put in standard form.
:::

## 8.1 Condition of tangency of a line to a circle

### The equation of a circle, in all its forms

A **circle** is the set of points at a fixed distance $r$ (the radius) from a
fixed point $C$ (the centre). Everything else follows from the distance formula.

::: derivation The four forms of the equation of a circle
**1. Centre–radius form.** Let the centre be $C(h,k)$ and let $P(x,y)$ be any
point of the circle. Then $CP = r$, so by the distance formula

$$ \sqrt{(x-h)^{2} + (y-k)^{2}} = r $$

Squaring both sides removes the root and gives the **standard form**

$$ (x-h)^{2} + (y-k)^{2} = r^{2} $$

**2. Centre at the origin.** Put $h = k = 0$:

$$ x^{2} + y^{2} = r^{2} $$

**3. General form.** Expand the standard form:

$$ x^{2} + y^{2} - 2hx - 2ky + (h^{2}+k^{2}-r^{2}) = 0 $$

Write $g = -h$, $f = -k$ and $c = h^{2}+k^{2}-r^{2}$. Then every circle has an
equation of the shape

$$ x^{2} + y^{2} + 2gx + 2fy + c = 0 $$

Reading this backwards, the centre is $(-g,-f)$ — *half the coefficients, sign
changed* — and since $r^{2} = h^{2}+k^{2}-c$,

$$ r = \sqrt{g^{2} + f^{2} - c} $$

The equation represents a real circle only when $g^{2}+f^{2}-c > 0$. If it is
zero the "circle" is the single point $(-g,-f)$; if it is negative there are no
real points at all.

**4. Diameter form.** If $A(x_1,y_1)$ and $B(x_2,y_2)$ are the ends of a
diameter, then the angle $APB$ in the semicircle is a right angle for every
point $P(x,y)$ on the circle. The slopes of $PA$ and $PB$ therefore multiply to
$-1$:

$$ \frac{y-y_1}{x-x_1}\cdot\frac{y-y_2}{x-x_2} = -1 $$

Clearing the denominators gives the **diameter form**

$$ (x-x_1)(x-x_2) + (y-y_1)(y-y_2) = 0 $$
:::

Two consequences are used constantly. A circle that **touches the $x$-axis** has
$|k| = r$; one that **touches the $y$-axis** has $|h| = r$; one that touches both
has centre $(\pm r, \pm r)$. And a general second-degree equation
$ax^{2}+by^{2}+2hxy+2gx+2fy+c = 0$ is a circle only if $a = b$ and $h = 0$ — so
if the coefficients of $x^{2}$ and $y^{2}$ differ, **divide through** before
reading off the centre.

::: caution Divide by the coefficient of $x^{2}$ first
For $3x^{2}+3y^{2}-12x+18y-6=0$ the centre is *not* $(6,-9)$. Divide by $3$ to
get $x^{2}+y^{2}-4x+6y-2=0$ first; then $2g=-4$, $2f=6$, so the centre is
$(2,-3)$ and $r = \sqrt{4+9+2} = \sqrt{15}$.
:::

### When does a line meet a circle?

Let the line be $y = mx+c$ and the circle $x^{2}+y^{2} = a^{2}$ with centre $O$
and radius $a$. Let $d$ be the perpendicular distance from $O$ to the line.
There are exactly three possibilities.

```figure caption="A line and the circle $x^2+y^2=25$. Only the perpendicular distance $d$ from the centre matters: the line cuts, touches, or misses according as $d<r$, $d=r$ or $d>r$."
import numpy as np, matplotlib.pyplot as plt
r = 5.0
fig, axes = plt.subplots(1, 3, figsize=(5.2, 2.5))
th = np.linspace(0, 2*np.pi, 400)
cases = [(5.0, 'd < r\ntwo points: secant', SERIES[2]),
         (5*np.sqrt(5), 'd = r\none point: tangent', ACCENT),
         (15.0, 'd > r\nno point: misses', SERIES[1])]
for ax, (c, lab, col) in zip(axes, cases):
    ax.plot(r*np.cos(th), r*np.sin(th), color=INK, lw=1.4)
    x = np.linspace(-9, 5, 50)
    ax.plot(x, 2*x + c, color=col, lw=1.8)
    fx, fy = -2*c/5, c/5
    ax.plot([0, fx], [0, fy], color=MUTED, lw=1.2, ls='--')
    ax.plot([0], [0], 'o', color=INK, ms=3.6)
    ax.plot([fx], [fy], 'o', color=col, ms=3.6)
    ax.text(fx/2, fy/2, '$d=%.2f$' % (c/np.sqrt(5)), fontsize=8.0, color=MUTED,
            ha='center', va='center', rotation=-26.6,
            bbox=dict(facecolor='white', edgecolor='none', pad=0.6))
    ax.plot([0, r*np.cos(-0.62)], [0, r*np.sin(-0.62)], color=INK, lw=1.0)
    ax.text(2.4, -1.4, '$r=5$', fontsize=8.2, color=INK, ha='center', va='top')
    ax.set_title(lab, fontsize=8.3, pad=3)
    ax.set_xlim(-9.6, 7.2); ax.set_ylim(-7.4, 9.0)
    ax.set_aspect('equal'); ax.axis('off')
fig.subplots_adjust(wspace=0.02)
```

::: derivation Condition for $y = mx + c$ to touch $x^{2}+y^{2} = a^{2}$
**Algebraic route.** Substitute $y = mx+c$ into the circle:

$$ x^{2} + (mx+c)^{2} = a^{2} $$
$$ (1+m^{2})x^{2} + 2mcx + (c^{2}-a^{2}) = 0 $$

This quadratic gives the $x$-coordinates of the intersection points. The line
touches the circle when the two points coincide, i.e. when the discriminant is
zero:

$$ (2mc)^{2} - 4(1+m^{2})(c^{2}-a^{2}) = 0 $$
$$ 4m^{2}c^{2} - 4c^{2} + 4a^{2} - 4m^{2}c^{2} + 4a^{2}m^{2} = 0 $$
$$ a^{2}(1+m^{2}) = c^{2} $$

**Geometric route (quicker).** The line touches the circle exactly when the
perpendicular distance from the centre equals the radius. For
$mx - y + c = 0$ and centre $(0,0)$,

$$ \frac{|c|}{\sqrt{m^{2}+1}} = a \quad\Longrightarrow\quad c^{2} = a^{2}(1+m^{2}) $$

Both routes give the same answer, and the second is the one to use in an exam.
:::

::: key Tangency to a circle — the three facts
For the circle $x^{2}+y^{2}=a^{2}$:

$$ y = mx + c \ \text{ is a tangent} \iff c^{2} = a^{2}(1+m^{2}) $$

so the two tangents of slope $m$ are $\;y = mx \pm a\sqrt{1+m^{2}}$, and the
point of contact is $\left(-\dfrac{a^{2}m}{c},\ \dfrac{a^{2}}{c}\right)$.

For the line $lx+my+n = 0$ the same condition reads $n^{2} = a^{2}(l^{2}+m^{2})$.

For **any** circle, centre $C$ and radius $r$: the line touches it if and only if
the perpendicular distance from $C$ to the line equals $r$.
:::

::: example Worked example 8.1
**Problem.** Find the equation of the circle passing through the points
$(0,0)$, $(6,0)$ and $(0,8)$. State its centre and radius.

**Solution.** Take the general form $x^{2}+y^{2}+2gx+2fy+c = 0$ and substitute
each point in turn.

Through $(0,0)$: $\;c = 0$.

Through $(6,0)$: $\;36 + 12g + c = 0 \Rightarrow 12g = -36 \Rightarrow g = -3$.

Through $(0,8)$: $\;64 + 16f + c = 0 \Rightarrow 16f = -64 \Rightarrow f = -4$.

So the circle is

$$ x^{2} + y^{2} - 6x - 8y = 0 $$

Centre $= (-g,-f) = (3,4)$ and $r = \sqrt{g^{2}+f^{2}-c} = \sqrt{9+16-0} = 5$.

**Check.** The distance from $(3,4)$ to $(6,0)$ is $\sqrt{9+16} = 5$. Correct.
:::

::: example Worked example 8.2
**Problem.** (a) Find the centre and radius of $x^{2}+y^{2}-8x+6y-11 = 0$.
(b) Find the equation of the circle with centre $(3,4)$ which touches the line
$4x-3y+10 = 0$.

**Solution.** (a) Compare with $x^{2}+y^{2}+2gx+2fy+c=0$: $\;2g = -8$ so $g=-4$;
$2f = 6$ so $f = 3$; $c = -11$.

$$ \text{centre} = (-g,-f) = (4,-3), \qquad
r = \sqrt{16 + 9 + 11} = \sqrt{36} = 6 $$

(b) A circle touches a line when the perpendicular distance from the centre to
the line equals the radius. For the line $4x-3y+10=0$ and the point $(3,4)$,

$$ r = \frac{|4(3) - 3(4) + 10|}{\sqrt{4^{2}+(-3)^{2}}} = \frac{|12-12+10|}{5}
= \frac{10}{5} = 2 $$

So the circle is $(x-3)^{2} + (y-4)^{2} = 4$, i.e.
$x^{2}+y^{2}-6x-8y+21 = 0$.
:::

::: example Worked example 8.3
**Problem.** Find the value of $c$ for which the line $y = 2x + c$ touches the
circle $x^{2}+y^{2} = 20$. Find the point of contact for the positive value.

**Solution.** Here $a^{2} = 20$ and $m = 2$. The condition of tangency is

$$ c^{2} = a^{2}(1+m^{2}) = 20(1+4) = 100 \quad\Longrightarrow\quad c = \pm 10 $$

For $c = 10$ the point of contact is

$$ \left(-\frac{a^{2}m}{c},\ \frac{a^{2}}{c}\right)
= \left(-\frac{20 \times 2}{10},\ \frac{20}{10}\right) = (-4,  2) $$

**Check.** $(-4)^{2} + 2^{2} = 20$, and $2(-4)+10 = 2$. The point lies on both.
:::

::: tip Which tangency condition to use
If the line is given in the form $y = mx+c$, use $c^{2} = a^{2}(1+m^{2})$.
If it is given as $lx+my+n=0$, or if the circle is not centred at the origin,
use "distance from centre $=$ radius". Never expand and take discriminants in an
exam unless you are explicitly asked to *derive* the condition.
:::

## 8.2 Tangent and normal to a circle

The **tangent** at a point of a circle is the line touching it there; the
**normal** is the line through that point perpendicular to the tangent. For a
circle the normal is especially simple, because the radius is already
perpendicular to the tangent.

```figure caption="Tangent and normal to $x^2+y^2=25$ at $P(3,4)$. The radius $CP$ is perpendicular to the tangent, so the normal is just the line $CP$ produced."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.7, 3.3))
th = np.linspace(0, 2*np.pi, 400)
ax.plot(5*np.cos(th), 5*np.sin(th), color=INK, lw=1.5)
ax.axhline(0, color=GRID, lw=0.9); ax.axvline(0, color=GRID, lw=0.9)
xn = np.linspace(-4.2, 7.4, 40)
ax.plot(xn, 4*xn/3, color=SERIES[1], lw=1.7)               # normal 4x-3y=0
x = np.linspace(-2.6, 9.4, 40)
ax.plot(x, (25 - 3*x)/4, color=ACCENT, lw=1.9)             # tangent 3x+4y=25
ax.plot([0, 3], [0, 4], color=INK, lw=2.2)
for P, lab, off in [((0, 0), '$C(0,0)$', (-42, -13)), ((3, 4), '$P(3,4)$', (-34, 12))]:
    ax.plot([P[0]], [P[1]], 'o', color=INK, ms=4.6)
    ax.annotate(lab, P, textcoords='offset points', xytext=off, fontsize=9.2)
u = np.array([3, 4])/5.0; v = np.array([4, -3])/5.0
Q = np.array([3.0, 4.0]); s = 0.62
ax.plot(*zip(Q - s*u, Q - s*u + s*v, Q + s*v), color=MUTED, lw=1.0)
ax.annotate('radius $CP$', (1.5, 2.0), textcoords='offset points', xytext=(-58, -4),
            fontsize=8.8, color=INK)
ax.text(7.2, 1.7, 'tangent  $3x+4y=25$', fontsize=8.8, color=ACCENT,
        ha='center', va='bottom', rotation=-27)
ax.text(-3.4, -4.0, 'normal  $4x-3y=0$', fontsize=8.8, color=SERIES[1],
        ha='left', va='bottom', rotation=40)
ax.annotate('the normal always\npasses through $C$', (0.9, -0.1), (2.2, -4.6),
            fontsize=8.6, color=MUTED, ha='left',
            arrowprops=dict(arrowstyle='->', color=MUTED, lw=0.8))
ax.set_xlim(-7.4, 10.4); ax.set_ylim(-6.6, 8.4)
ax.set_aspect('equal'); ax.axis('off')
```

::: derivation Tangent and normal at a point of a circle
Let $P(x_1,y_1)$ lie on $x^{2}+y^{2} = a^{2}$, so $x_1^{2}+y_1^{2} = a^{2}$.

The radius $CP$ joins $(0,0)$ to $(x_1,y_1)$, so its slope is $y_1/x_1$. The
tangent is perpendicular to the radius, so its slope is $-x_1/y_1$. Using the
point–slope form,

$$ y - y_1 = -\frac{x_1}{y_1}(x - x_1) $$
$$ yy_1 - y_1^{2} = -xx_1 + x_1^{2} $$
$$ xx_1 + yy_1 = x_1^{2} + y_1^{2} = a^{2} $$

So the tangent at $(x_1,y_1)$ is

$$ xx_1 + yy_1 = a^{2} $$

For the general circle $x^{2}+y^{2}+2gx+2fy+c = 0$ the same argument (or
differentiation) gives the **rule of $T = 0$**: replace $x^{2}$ by $xx_1$,
$y^{2}$ by $yy_1$, $2x$ by $x+x_1$ and $2y$ by $y+y_1$:

$$ xx_1 + yy_1 + g(x+x_1) + f(y+y_1) + c = 0 $$

The **normal** passes through $P$ and the centre, so for $x^{2}+y^{2}=a^{2}$ it
is the line through the origin with slope $y_1/x_1$:

$$ y_1 x - x_1 y = 0 $$

and for the general circle it is the line joining $(-g,-f)$ to $(x_1,y_1)$.
:::

::: key Tangent facts for the circle
- Tangent at $(x_1,y_1)$ on $x^{2}+y^{2}=a^{2}$: $\;xx_1+yy_1 = a^{2}$.
- Normal at $(x_1,y_1)$: passes through the centre — always.
- **Length of the tangent** from an external point $P(x_1,y_1)$ to
  $S \equiv x^{2}+y^{2}+2gx+2fy+c = 0$:
  $$ PT = \sqrt{S_1} = \sqrt{x_1^{2}+y_1^{2}+2gx_1+2fy_1+c} $$
  because $PT^{2} = CP^{2} - r^{2}$ by Pythagoras.
- **Pair of tangents** from $P$: $\;SS_1 = T^{2}$.
- **Director circle** (locus of points from which the two tangents are
  perpendicular) of $x^{2}+y^{2}=a^{2}$: $\;x^{2}+y^{2} = 2a^{2}$.
:::

::: example Worked example 8.4
**Problem.** Find the equations of the tangent and the normal to the circle
$x^{2}+y^{2} = 25$ at the point $(3,4)$.

**Solution.** First check the point lies on the circle: $9 + 16 = 25$. It does.

*Tangent.* Use $xx_1+yy_1 = a^{2}$ with $(x_1,y_1) = (3,4)$ and $a^{2}=25$:

$$ 3x + 4y = 25 $$

*Normal.* The normal passes through the centre $(0,0)$ and through $(3,4)$, so
its slope is $4/3$:

$$ y = \frac{4}{3}x \quad\Longrightarrow\quad 4x - 3y = 0 $$

**Check.** The perpendicular distance from $(0,0)$ to $3x+4y-25 = 0$ is
$25/\sqrt{9+16} = 25/5 = 5$, which is the radius. The tangent is correct, and
the product of the slopes, $\left(-\tfrac34\right)\left(\tfrac43\right) = -1$,
confirms the normal.
:::

::: example Worked example 8.5
**Problem.** From the point $(7,1)$, tangents are drawn to the circle
$x^{2}+y^{2} = 25$. Find (a) the length of each tangent, (b) the equations of the
two tangents, and (c) the angle between them.

**Solution.** (a) With $S \equiv x^{2}+y^{2}-25$,

$$ PT = \sqrt{S_1} = \sqrt{7^{2} + 1^{2} - 25} = \sqrt{49+1-25} = \sqrt{25} = 5 $$

(b) Any line through $(7,1)$ with slope $m$ is $y - 1 = m(x-7)$, i.e.
$y = mx + (1-7m)$. So $c = 1-7m$. Apply $c^{2} = a^{2}(1+m^{2})$:

$$ (1-7m)^{2} = 25(1+m^{2}) $$
$$ 1 - 14m + 49m^{2} = 25 + 25m^{2} $$
$$ 24m^{2} - 14m - 24 = 0 \quad\Longrightarrow\quad 12m^{2} - 7m - 12 = 0 $$

$$ m = \frac{7 \pm \sqrt{49 + 576}}{24} = \frac{7 \pm 25}{24}
= \frac{4}{3} \ \text{ or } -\frac{3}{4} $$

The tangents are

$$ y - 1 = \frac43(x-7) \Rightarrow 4x - 3y - 25 = 0, \qquad
y - 1 = -\frac34(x-7) \Rightarrow 3x + 4y - 25 = 0 $$

(c) The product of the slopes is $\left(\tfrac43\right)\left(-\tfrac34\right) =
-1$, so the tangents are **perpendicular**: the angle is $90^{\circ}$. This had
to happen, because $7^{2}+1^{2} = 50 = 2(25)$ puts $(7,1)$ on the director
circle.
:::

## 8.3 Standard equation of parabola

A **parabola** is the conic with $e = 1$: every point of it is *equally* far from
the focus and from the directrix.

::: derivation Standard equation of the parabola
Choose the axes to make the algebra as simple as possible. Let the focus be
$S(a,0)$ with $a>0$, and let the directrix be the line $x = -a$, i.e.
$x+a = 0$. The origin is then midway between focus and directrix, so the origin
is the vertex.

Let $P(x,y)$ be any point on the curve and $M$ the foot of the perpendicular
from $P$ to the directrix. The defining condition $PS = PM$ gives

$$ \sqrt{(x-a)^{2} + y^{2}} = |x + a| $$

Square both sides:

$$ (x-a)^{2} + y^{2} = (x+a)^{2} $$
$$ x^{2} - 2ax + a^{2} + y^{2} = x^{2} + 2ax + a^{2} $$

The $x^{2}$ and $a^{2}$ terms cancel, leaving

$$ y^{2} = 4ax $$

This is the **standard equation of the parabola**. Because the right side must be
non-negative, $x \ge 0$: the curve lies entirely to the right of the tangent at
the vertex, and it opens towards the focus.

**Latus rectum.** Put $x = a$ in $y^{2}=4ax$: $\;y^{2} = 4a^{2}$, so
$y = \pm 2a$. The latus rectum runs from $(a,2a)$ to $(a,-2a)$ and its length is

$$ \text{latus rectum} = 4a $$

which is why the coefficient is written as $4a$ rather than as a single letter.
:::

```figure caption="The parabola $y^2=4ax$ with $a=2$, fully labelled: vertex $A$, focus $S(a,0)$, directrix $x+a=0$, axis along $Ox$, and latus rectum $LL'$ of length $4a$."
import numpy as np, matplotlib.pyplot as plt
a = 2.0
fig, ax = plt.subplots(figsize=(5.0, 4.3))
t = np.linspace(-1.25, 1.25, 400)
ax.plot(a*t**2, 2*a*t, color=ACCENT, lw=2.0)
ax.annotate('', xy=(6.0, 0), xytext=(-4.0, 0),
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=0.9))
ax.text(5.95, -0.42, 'axis of the parabola', color=MUTED, fontsize=8.6, ha='right', va='top')
ax.plot([-a, -a], [-4.3, 4.3], color=SERIES[1], lw=1.5, ls='--')
ax.text(-a - 0.25, 3.3, 'directrix\n$x+a=0$', color=SERIES[1], fontsize=8.8,
        ha='right', va='center')
ax.plot([a, a], [-2*a, 2*a], color=SERIES[2], lw=2.0)
ax.plot([a, a], [-2*a, 2*a], 'o', color=SERIES[2], ms=4)
ax.text(a + 0.3, 2*a, "$L(a,\\,2a)$", color=SERIES[2], fontsize=8.6, ha='left', va='center')
ax.text(a + 0.3, -2*a, "$L'(a,-2a)$", color=SERIES[2], fontsize=8.6, ha='left', va='center')
ax.text(a + 0.3, 1.55, 'latus rectum\n$LL\' = 4a$', color=SERIES[2], fontsize=8.8,
        ha='left', va='center')
for P, lab, off in [((0, 0), "vertex\n$A(0,0)$", (-7, 13)), ((a, 0), "focus $S(a,0)$", (7, 9))]:
    ax.plot([P[0]], [P[1]], 'o', color=INK, ms=4.8)
    ax.annotate(lab, P, textcoords='offset points', xytext=off, fontsize=9.0,
                ha=('right' if P[0] == 0 else 'left'))
for x0, x1 in [(-a, 0), (0, a)]:
    ax.annotate('', xy=(x0, -0.7), xytext=(x1, -0.7),
                arrowprops=dict(arrowstyle='<|-|>', color=INK, lw=0.8, mutation_scale=7))
    ax.text((x0 + x1)/2, -1.25, '$a$', color=INK, fontsize=9.2, ha='center')
ax.text(-4.3, -4.05, 'eccentricity $e = 1$:  every point is\nas far from $S$ as from the directrix',
        fontsize=8.8, ha='left', va='center', color=INK)
ax.set_xlim(-4.5, 6.1); ax.set_ylim(-4.75, 4.65)
ax.set_aspect('equal'); ax.axis('off')
```

Replacing $x$ by $-x$, or swapping $x$ and $y$, turns the curve to face the other
three directions. All four forms have vertex at the origin.

```figure caption="The four standard parabolas with vertex at the origin. The curve always opens towards its focus and away from its directrix."
import numpy as np, matplotlib.pyplot as plt
fig, axes = plt.subplots(2, 2, figsize=(5.2, 3.6))
a = 1.0
t = np.linspace(-2.05, 2.05, 300)
cases = [('$y^2 = 4ax$',  (a*t**2,  2*a*t),  (a, 0),  'x', -a, 'opens right'),
         ('$y^2 = -4ax$', (-a*t**2, 2*a*t),  (-a, 0), 'x',  a, 'opens left'),
         ('$x^2 = 4ay$',  (2*a*t,   a*t**2), (0, a),  'y', -a, 'opens up'),
         ('$x^2 = -4ay$', (2*a*t,  -a*t**2), (0, -a), 'y',  a, 'opens down')]
for ax, (eq, (X, Y), F, axis, d, words) in zip(axes.ravel(), cases):
    ax.plot(X, Y, color=ACCENT, lw=1.9)
    ax.axhline(0, color=GRID, lw=0.9); ax.axvline(0, color=GRID, lw=0.9)
    if axis == 'x':
        ax.axvline(d, color=SERIES[1], lw=1.3, ls='--')
        ax.text(d + (0.25 if d > 0 else -0.25), 3.3,
                'x = %s' % ('a' if d > 0 else '−a'), color=SERIES[1],
                fontsize=8.0, ha=('left' if d > 0 else 'right'), va='center')
        ax.plot([F[0], F[0]], [-2*a, 2*a], color=MUTED, lw=1.0)
    else:
        ax.axhline(d, color=SERIES[1], lw=1.3, ls='--')
        ax.text(3.9, d + (0.28 if d > 0 else -0.28),
                'y = %s' % ('a' if d > 0 else '−a'), color=SERIES[1],
                fontsize=8.0, ha='right', va=('bottom' if d > 0 else 'top'))
        ax.plot([-2*a, 2*a], [F[1], F[1]], color=MUTED, lw=1.0)
    ax.plot([F[0]], [F[1]], 'o', color=INK, ms=4.0)
    ax.plot([0], [0], 'o', color=INK, ms=3.2)
    ax.annotate('$S$', F, textcoords='offset points', xytext=(4, 3), fontsize=8.6)
    ax.set_title(eq + '   ' + words, fontsize=8.6, pad=2)
    ax.set_xlim(-4.4, 4.4); ax.set_ylim(-4.4, 4.4)
    ax.set_aspect('equal'); ax.axis('off')
fig.subplots_adjust(wspace=0.02, hspace=0.22)
```

::: key The four standard parabolas
| Equation | Opens | Axis | Vertex | Focus | Directrix | Latus rectum |
|---|---|---|---|---|---|---|
| $y^{2} = 4ax$ | right | $y=0$ | $(0,0)$ | $(a,0)$ | $x=-a$ | $4a$ |
| $y^{2} = -4ax$ | left | $y=0$ | $(0,0)$ | $(-a,0)$ | $x=a$ | $4a$ |
| $x^{2} = 4ay$ | up | $x=0$ | $(0,0)$ | $(0,a)$ | $y=-a$ | $4a$ |
| $x^{2} = -4ay$ | down | $x=0$ | $(0,0)$ | $(0,-a)$ | $y=a$ | $4a$ |

For all of them $e = 1$, and $a > 0$ is the distance from the vertex to the
focus. **Shifted vertex:** if the vertex moves to $(h,k)$ the equations become
$(y-k)^{2} = \pm 4a(x-h)$ and $(x-h)^{2} = \pm 4a(y-k)$. Everything else shifts
with it: the focus is $a$ units from the vertex *along* the axis, the directrix
is $a$ units from it on the other side.

A convenient parametric form of $y^{2}=4ax$ is $\;x = at^{2},\ y = 2at$.
:::

::: caution The square tells you the axis
Which variable is squared decides which way the parabola opens. In
$y^{2} = 4ax$ *only $y$ is squared*, so the axis is horizontal. In
$x^{2}=4ay$ the axis is vertical. Students who memorise "$4a$ goes with $x$"
without noticing this reverse the whole diagram.
:::

::: example Worked example 8.6
**Problem.** Find the equation of the parabola with vertex at the origin, axis
along the $x$-axis, passing through the point $(3,-6)$. State its focus,
directrix and latus rectum.

**Solution.** Axis along $Ox$ and vertex at the origin means the form is
$y^{2} = 4ax$ (the point has $x>0$, so it opens right). Substitute $(3,-6)$:

$$ (-6)^{2} = 4a(3) \quad\Longrightarrow\quad 36 = 12a \quad\Longrightarrow\quad a = 3 $$

Hence $4a = 12$ and the parabola is

$$ y^{2} = 12x $$

Focus $(a,0) = (3,0)$; directrix $x = -3$; latus rectum $= 4a = 12$ units;
eccentricity $e=1$.
:::

::: example Worked example 8.7
**Problem.** Reduce $y^{2} - 8y - 4x + 20 = 0$ to standard form and find its
vertex, focus, directrix, axis and length of latus rectum.

**Solution.** Only $y$ is squared, so collect the $y$ terms and complete the
square.

$$ y^{2} - 8y = 4x - 20 $$
$$ y^{2} - 8y + 16 = 4x - 20 + 16 $$
$$ (y-4)^{2} = 4x - 4 = 4(x-1) $$

Compare with $(y-k)^{2} = 4a(x-h)$: $\;h = 1$, $k = 4$, $4a = 4$ so $a = 1$.

- Vertex: $(1,4)$.
- Axis: horizontal through the vertex, $y = 4$. Opens to the right.
- Focus: $a=1$ unit right of the vertex, $(1+1, 4) = (2,4)$.
- Directrix: $1$ unit left of the vertex, $x = 1-1 = 0$, i.e. the $y$-axis.
- Latus rectum: $4a = 4$ units.

**Check.** Take the point of the curve with $y=6$: $(6-4)^{2} = 4(x-1)$ gives
$x = 2$. Distance to focus $(2,4)$ is $\sqrt{0+4} = 2$; distance to the line
$x=0$ is $2$. Equal, as required.
:::

::: example Worked example 8.8
**Problem.** Find the vertex, focus, directrix and latus rectum of
$x^{2} - 4x - 8y + 20 = 0$.

**Solution.** Now $x$ is squared, so the axis is vertical.

$$ x^{2} - 4x = 8y - 20 $$
$$ x^{2} - 4x + 4 = 8y - 20 + 4 $$
$$ (x-2)^{2} = 8y - 16 = 8(y-2) $$

Compare with $(x-h)^{2} = 4a(y-k)$: $h=2$, $k=2$, $4a = 8$ so $a = 2$; the
parabola opens **upwards**.

- Vertex $(2,2)$; axis $x = 2$.
- Focus: $2$ units above the vertex, $(2, 2+2) = (2,4)$.
- Directrix: $2$ units below, $y = 2-2 = 0$, the $x$-axis.
- Latus rectum $= 4a = 8$ units.
:::

::: example Worked example 8.9
**Problem.** A suspension bridge across the Karnali has a parabolic cable. The
span between the two towers is $80$ m, each tower rises $20$ m above the
roadway, and the lowest point of the cable is $4$ m above the roadway. Find the
height of the cable at a point $20$ m horizontally from the lowest point.

**Solution.** Put the origin at the lowest point of the cable, with the $y$-axis
vertical. Then the cable is $x^{2} = 4ay$ (opening upward, vertex at the
origin).

Each tower is $40$ m horizontally from the lowest point and rises
$20 - 4 = 16$ m above it, so the cable passes through $(40,16)$:

$$ 40^{2} = 4a(16) \quad\Longrightarrow\quad 1600 = 64a \quad\Longrightarrow\quad 4a = 100 $$

So the cable is $x^{2} = 100y$. At $x = 20$:

$$ 400 = 100y \quad\Longrightarrow\quad y = 4 $$

That is $4$ m above the lowest point of the cable, so the height above the
roadway is $4 + 4 = 8$ m.
:::

## 8.4 Tangent and normal to a parabola

```figure caption="Tangent and normal to $y^2=12x$ at $P(3,6)$. The tangent meets the axis at $T(-3,0)$ and the normal at $G(9,0)$; here $TS = SP$ and the subnormal $SG = 2a = 6$ is the same for every point of the parabola."
import numpy as np, matplotlib.pyplot as plt
a = 3.0
fig, ax = plt.subplots(figsize=(4.7, 4.2))
t = np.linspace(-1.55, 1.95, 400)
ax.plot(a*t**2, 2*a*t, color=INK, lw=1.8)
ax.axhline(0, color=GRID, lw=1.0); ax.axvline(0, color=GRID, lw=1.0)
x = np.linspace(-4.6, 7.2, 40)
ax.plot(x, x + 3, color=ACCENT, lw=1.8)                 # tangent  y = x+3
xn = np.linspace(0.2, 11.6, 40)
ax.plot(xn, 9 - xn, color=SERIES[1], lw=1.8)            # normal   x+y = 9
ax.plot([3, 3], [0, 6], color=MUTED, lw=1.0, ls=':')
for P, lab, off in [((3, 6), '$P(3,6)$', (7, 4)), ((3, 0), '$S(3,0)$', (2, -14)),
                    ((-3, 0), '$T(-3,0)$', (-6, 7)), ((9, 0), '$G(9,0)$', (0, -14))]:
    ax.plot([P[0]], [P[1]], 'o', color=INK, ms=4.4)
    ax.annotate(lab, P, textcoords='offset points', xytext=off, fontsize=8.8,
                ha=('right' if P[0] < 0 else 'left'))
u = np.array([1, 1])/np.sqrt(2); v = np.array([1, -1])/np.sqrt(2)
Q = np.array([3.0, 6.0]); s = 0.75
ax.plot(*zip(Q - s*u, Q - s*u + s*v, Q + s*v), color=MUTED, lw=1.0)
ax.text(-4.3, -0.9, 'tangent  $y = x+3$', color=ACCENT, fontsize=9.0, rotation=39,
        ha='left', va='center')
ax.text(8.4, 3.3, 'normal  $x+y=9$', color=SERIES[1], fontsize=9.0, ha='center', va='center')
ax.annotate('', xy=(3, -2.4), xytext=(9, -2.4),
            arrowprops=dict(arrowstyle='<|-|>', color=MUTED, lw=0.8, mutation_scale=7))
ax.text(6.0, -2.9, 'subnormal $= 2a = 6$', color=MUTED, fontsize=8.5, ha='center', va='top')
ax.text(-4.4, 8.6, '$y^2 = 12x$', color=INK, fontsize=10.0, ha='left')
ax.set_xlim(-5.0, 11.8); ax.set_ylim(-5.4, 9.6)
ax.set_aspect('equal'); ax.axis('off')
```

::: derivation Tangent and normal at a point of a parabola
Let $P(x_1,y_1)$ lie on $y^{2} = 4ax$. Differentiate the equation implicitly:

$$ 2y \frac{dy}{dx} = 4a \quad\Longrightarrow\quad \frac{dy}{dx} = \frac{2a}{y} $$

At $P$ the gradient of the tangent is therefore $2a/y_1$, and the tangent is

$$ y - y_1 = \frac{2a}{y_1}(x - x_1) $$
$$ yy_1 - y_1^{2} = 2ax - 2ax_1 $$

Now use $y_1^{2} = 4ax_1$ to replace $y_1^{2}$:

$$ yy_1 = 2ax - 2ax_1 + 4ax_1 = 2a(x + x_1) $$

So the **tangent at $(x_1,y_1)$** is

$$ yy_1 = 2a(x + x_1) $$

which is again the rule $T=0$: replace $y^{2}$ by $yy_1$ and $x$ by
$\tfrac12(x+x_1)$.

The **normal** is perpendicular to the tangent, so its gradient is $-y_1/(2a)$:

$$ y - y_1 = -\frac{y_1}{2a}(x - x_1) $$
:::

::: derivation Condition for $y = mx+c$ to touch $y^{2} = 4ax$
Substitute $y = mx+c$ into $y^{2}=4ax$:

$$ (mx+c)^{2} = 4ax $$
$$ m^{2}x^{2} + (2mc - 4a)x + c^{2} = 0 $$

For a tangent the two roots must coincide, so the discriminant vanishes:

$$ (2mc-4a)^{2} - 4m^{2}c^{2} = 0 $$
$$ 4m^{2}c^{2} - 16amc + 16a^{2} - 4m^{2}c^{2} = 0 $$
$$ 16a^{2} = 16amc \quad\Longrightarrow\quad c = \frac{a}{m} \quad (m \ne 0) $$

So every line of the form

$$ y = mx + \frac{a}{m} $$

touches $y^{2}=4ax$. Putting $c = a/m$ back into the quadratic gives the double
root $x = a/m^{2}$, and then $y = 2a/m$, so the **point of contact** is

$$ \left(\frac{a}{m^{2}},\ \frac{2a}{m}\right) $$
:::

::: key Parabola $y^{2}=4ax$ — tangent and normal
| | Cartesian point $(x_1,y_1)$ | Parametric point $(at^{2},2at)$ | Slope form |
|---|---|---|---|
| Tangent | $yy_1 = 2a(x+x_1)$ | $ty = x + at^{2}$ | $y = mx + \dfrac{a}{m}$ |
| Normal | $y - y_1 = -\dfrac{y_1}{2a}(x-x_1)$ | $y = -tx + 2at + at^{3}$ | $y = mx - 2am - am^{3}$ |

Useful extras, all provable from the figure above:
- The tangent at $(x_1,y_1)$ meets the axis at $(-x_1,0)$, and the tangent at the
  vertex is the $y$-axis.
- **Subnormal** $=2a$, the same at every point.
- The tangent at any point bisects the angle between the focal radius and the
  line through the point parallel to the axis — the reflector property used in
  headlamps and dish antennas.
:::

::: example Worked example 8.10
**Problem.** Find the equations of the tangent and normal to the parabola
$y^{2} = 12x$ at the point $(3,6)$.

**Solution.** Check: $6^{2} = 36 = 12(3)$. The point is on the curve. Here
$4a = 12$, so $a = 3$ and $2a = 6$.

*Tangent.* $yy_1 = 2a(x+x_1)$ with $(x_1,y_1) = (3,6)$:

$$ 6y = 6(x+3) \quad\Longrightarrow\quad y = x + 3 $$

*Normal.* Gradient $= -y_1/(2a) = -6/6 = -1$:

$$ y - 6 = -1(x-3) \quad\Longrightarrow\quad x + y = 9 $$

**Check.** The tangent $y = x+3$ has $m=1$ and $c=3 = a/m = 3/1$. The condition
of tangency holds.
:::

::: example Worked example 8.11
**Problem.** Show that the line $y = 2x+2$ is a tangent to the parabola
$y^{2} = 16x$ and find the point of contact.

**Solution.** For $y^{2}=16x$, $4a = 16$ so $a = 4$. The line has $m = 2$ and
$c = 2$. The condition of tangency is $c = a/m$:

$$ \frac{a}{m} = \frac{4}{2} = 2 = c $$

The condition is satisfied, so the line touches the parabola. The point of
contact is

$$ \left(\frac{a}{m^{2}},\ \frac{2a}{m}\right)
= \left(\frac{4}{4},\ \frac{8}{2}\right) = (1, 4) $$

**Check.** $4^{2} = 16 = 16(1)$, and $2(1)+2 = 4$. The point is on both.
:::

::: example Worked example 8.12
**Problem.** Find the equation of the normal to the parabola $y^{2} = 4x$ at the
point $(4,4)$.

**Solution.** Here $4a = 4$, so $a = 1$. In parametric form
$(at^{2},2at) = (t^{2},2t)$, and $(4,4)$ gives $t = 2$.

Use the parametric normal $y = -tx + 2at + at^{3}$ with $t=2$, $a=1$:

$$ y = -2x + 4 + 8 = -2x + 12 \quad\Longrightarrow\quad 2x + y = 12 $$

**Check with the Cartesian form.** Gradient of the normal is
$-y_1/(2a) = -4/2 = -2$, and $y - 4 = -2(x-4)$ gives $2x+y = 12$. The same.
:::

## 8.5 Standard equation of ellipse

An **ellipse** is the conic with $0 < e < 1$. Because $e<1$ the curve closes up:
the focus is nearer than the directrix, so the curve can never escape.

::: derivation Standard equation of the ellipse
Let the focus be $S(ae,0)$ and the directrix the line $x = a/e$, with
$0 < e < 1$. (This choice of letters is deliberate; $a$ will turn out to be the
semi-major axis.) For any point $P(x,y)$ on the conic, $PS = e PM$ gives

$$ \sqrt{(x-ae)^{2} + y^{2}} = e\left|x - \frac{a}{e}\right| = |ex - a| $$

Squaring:

$$ x^{2} - 2aex + a^{2}e^{2} + y^{2} = e^{2}x^{2} - 2aex + a^{2} $$

The $-2aex$ terms cancel. Gather like terms:

$$ x^{2}(1-e^{2}) + y^{2} = a^{2}(1-e^{2}) $$

Divide throughout by $a^{2}(1-e^{2})$, which is positive because $e<1$:

$$ \frac{x^{2}}{a^{2}} + \frac{y^{2}}{a^{2}(1-e^{2})} = 1 $$

Now **define** $b^{2} = a^{2}(1-e^{2})$. Since $0<e<1$ we have $b < a$, and the
equation becomes the **standard equation of the ellipse**

$$ \frac{x^{2}}{a^{2}} + \frac{y^{2}}{b^{2}} = 1, \qquad a > b > 0 $$

Two relations follow immediately and must be memorised:

$$ b^{2} = a^{2} - a^{2}e^{2} \quad\Longrightarrow\quad
a^{2}e^{2} = a^{2}-b^{2}, \qquad e = \sqrt{1 - \frac{b^{2}}{a^{2}}} $$

**Symmetry gives a second focus.** Replacing $x$ by $-x$ leaves the equation
unchanged, so the curve is symmetric about the $y$-axis; hence $S_1(-ae,0)$ is a
focus too, with directrix $x = -a/e$.

**Latus rectum.** Put $x = ae$ in the standard equation:

$$ \frac{a^{2}e^{2}}{a^{2}} + \frac{y^{2}}{b^{2}} = 1
\quad\Longrightarrow\quad y^{2} = b^{2}(1-e^{2}) = \frac{b^{4}}{a^{2}} $$

so $y = \pm b^{2}/a$ and the length of each latus rectum is $2b^{2}/a$.

**Focal distance property.** From $PS = e PM = e\left(\dfrac ae - x\right)$ we get
$PS = a - ex$, and similarly $PS_1 = a + ex$. Therefore

$$ PS + PS_1 = 2a $$

*The sum of the distances from any point of an ellipse to the two foci is
constant and equal to the major axis.* This is the "string and two pins"
construction.
:::

```figure caption="The ellipse $x^2/25+y^2/9=1$ ($a=5$, $b=3$, $e=0.8$): centre $O$, vertices $A,A_1$, minor-axis ends $B,B_1$, foci $S,S_1$ at $(\pm ae,0)$, directrices $x=\pm a/e$, and latus recta of length $2b^2/a$."
import numpy as np, matplotlib.pyplot as plt
a, b = 5.0, 3.0
e = 0.8
fig, ax = plt.subplots(figsize=(5.2, 3.35))
th = np.linspace(0, 2*np.pi, 500)
ax.plot(a*np.cos(th), b*np.sin(th), color=INK, lw=1.9)
ax.axhline(0, color=GRID, lw=1.0); ax.axvline(0, color=GRID, lw=1.0)
for s in (1, -1):
    ax.plot([s*a*e, s*a*e], [-b*b/a, b*b/a], color=SERIES[2], lw=2.0)
    ax.plot([s*a*e], [0], 'o', color=INK, ms=4.6)
    ax.plot([s*a/e, s*a/e], [-4.1, 4.1], color=SERIES[1], lw=1.4, ls='--')
ax.plot([a, -a, 0, 0], [0, 0, b, -b], 'o', color=INK, ms=3.8)
ax.plot([0], [0], 'o', color=INK, ms=3.8)
ax.text(-4.0, 0.42, "$S_1(-ae,0)$", fontsize=8.5, ha='center', va='bottom')
ax.text(4.0, 0.42, "$S(ae,0)$", fontsize=8.5, ha='center', va='bottom')
ax.text(-5.25, -0.15, "$A_1(-a,0)$", fontsize=8.5, ha='right', va='center')
ax.text(5.25, -0.15, "$A(a,0)$", fontsize=8.5, ha='left', va='center')
ax.text(0.18, -0.3, "$C$", fontsize=8.8, ha='left', va='top')
ax.text(0.15, 3.05, "$B(0,b)$", fontsize=8.5, ha='left', va='bottom')
ax.text(0.15, -3.1, "$B_1(0,-b)$", fontsize=8.5, ha='left', va='top')
ax.text(6.35, 3.4, 'directrix\n$x = a/e$', color=SERIES[1], fontsize=8.4,
        ha='left', va='top')
ax.text(-6.35, 3.4, 'directrix\n$x = -a/e$', color=SERIES[1], fontsize=8.4,
        ha='right', va='top')
ax.annotate('latus rectum $= 2b^2/a$', (4.0, 1.8), (2.1, 3.85), color=SERIES[2],
            fontsize=8.5, ha='center',
            arrowprops=dict(arrowstyle='->', color=SERIES[2], lw=0.8))
ax.text(0, -4.35, '$b^2 = a^2(1-e^2)$,  $e<1$;  major axis $2a$,  minor axis $2b$',
        fontsize=8.8, ha='center', va='center', color=INK)
ax.set_xlim(-8.6, 8.6); ax.set_ylim(-4.8, 4.5)
ax.set_aspect('equal'); ax.axis('off')
```

If the larger denominator sits under $y^{2}$ the ellipse is *taller than it is
wide* and every element turns through $90^{\circ}$.

```figure caption="The same two numbers, swapped. Left: $x^2/25+y^2/9=1$, major axis along $Ox$, foci $(\pm4,0)$. Right: $x^2/9+y^2/25=1$, major axis along $Oy$, foci $(0,\pm4)$. The foci always lie on the major axis."
import numpy as np, matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 2, figsize=(5.2, 3.0))
th = np.linspace(0, 2*np.pi, 400)
for ax, (p, q, horiz) in zip(axes, [(5.0, 3.0, True), (3.0, 5.0, False)]):
    ax.plot(p*np.cos(th), q*np.sin(th), color=INK, lw=1.8)
    ax.axhline(0, color=GRID, lw=1.0); ax.axvline(0, color=GRID, lw=1.0)
    c = np.sqrt(abs(p*p - q*q))
    F = [(c, 0), (-c, 0)] if horiz else [(0, c), (0, -c)]
    for f in F:
        ax.plot([f[0]], [f[1]], 'o', color=SERIES[1], ms=4.6)
    ax.plot([0], [0], 'o', color=INK, ms=3.4)
    if horiz:
        ax.plot([-p, p], [0, 0], color=ACCENT, lw=2.4)
        ax.plot([0, 0], [-q, q], color=SERIES[2], lw=2.4)
        ax.text(0, 3.45, 'major axis along $x$', color=ACCENT, fontsize=8.4, ha='center')
        ax.text(c, -0.55, '$(ae,0)$', color=SERIES[1], fontsize=8.0, ha='center', va='top')
        ax.text(-c, -0.55, '$(-ae,0)$', color=SERIES[1], fontsize=8.0, ha='center', va='top')
        ax.set_title('$a > b$:  $\\frac{x^2}{25}+\\frac{y^2}{9}=1$', fontsize=9.0, pad=4)
        ax.text(0, -4.5, '$a=5,\\ b=3,\\ e=\\frac{4}{5}$', fontsize=8.8, ha='center')
    else:
        ax.plot([0, 0], [-q, q], color=ACCENT, lw=2.4)
        ax.plot([-p, p], [0, 0], color=SERIES[2], lw=2.4)
        ax.text(-0.35, 2.6, 'major axis\nalong $y$', color=ACCENT, fontsize=8.4,
                ha='right', va='center')
        ax.text(0.55, c + 0.3, '$(0,be)$', color=SERIES[1], fontsize=8.0,
                ha='center', va='bottom')
        ax.text(0.65, -c - 0.3, '$(0,-be)$', color=SERIES[1], fontsize=8.0,
                ha='center', va='top')
        ax.set_title('$b > a$:  $\\frac{x^2}{9}+\\frac{y^2}{25}=1$', fontsize=9.0, pad=4)
        ax.text(0, -6.1, '$a=3,\\ b=5,\\ e=\\frac{4}{5}$', fontsize=8.8, ha='center')
    ax.set_xlim(-6.4, 6.4); ax.set_ylim(-6.6, 6.0)
    ax.set_aspect('equal'); ax.axis('off')
fig.subplots_adjust(wspace=0.04)
```

::: key Ellipse $\dfrac{x^{2}}{a^{2}} + \dfrac{y^{2}}{b^{2}} = 1$ — elements
| Element | $a > b$ (major axis $Ox$) | $b > a$ (major axis $Oy$) |
|---|---|---|
| Centre | $(0,0)$ | $(0,0)$ |
| Vertices | $(\pm a, 0)$ | $(0,\pm b)$ |
| Major / minor axis | $2a$ / $2b$ | $2b$ / $2a$ |
| Eccentricity | $e = \sqrt{1 - b^{2}/a^{2}}$ | $e = \sqrt{1 - a^{2}/b^{2}}$ |
| Foci | $(\pm ae, 0)$ | $(0, \pm be)$ |
| Directrices | $x = \pm a/e$ | $y = \pm b/e$ |
| Latus rectum | $2b^{2}/a$ | $2a^{2}/b$ |

**Rule to remember:** the foci and the directrices always belong to the
**larger** denominator. Shifted centre $(h,k)$:
$\dfrac{(x-h)^{2}}{a^{2}} + \dfrac{(y-k)^{2}}{b^{2}} = 1$.
Parametric form: $x = a\cos\theta$, $y = b\sin\theta$.
:::

::: caution Do not force $a>b$
If you are handed $\dfrac{x^{2}}{9} + \dfrac{y^{2}}{25} = 1$, do **not** rename
things so that $a=5$. Keep $a^{2}=9$ under $x^{2}$ and $b^{2}=25$ under $y^{2}$,
notice that $b>a$, and use the right-hand column of the table. The foci are
$(0,\pm 4)$, not $(\pm 4,0)$.
:::

::: example Worked example 8.13
**Problem.** Find the equation of the ellipse whose foci are $(\pm 4, 0)$ and
whose eccentricity is $2/3$.

**Solution.** The foci are on the $x$-axis, so the form is
$x^{2}/a^{2} + y^{2}/b^{2} = 1$ with $a>b$ and foci $(\pm ae,0)$.

$$ ae = 4, \quad e = \frac23 \quad\Longrightarrow\quad a = \frac{4}{2/3} = 6 $$

$$ b^{2} = a^{2}(1-e^{2}) = 36\left(1 - \frac49\right) = 36 \times \frac59 = 20 $$

The ellipse is

$$ \frac{x^{2}}{36} + \frac{y^{2}}{20} = 1 $$

**Check.** $a^{2}-b^{2} = 36-20 = 16 = (ae)^{2} = 4^{2}$. Correct.
:::

::: example Worked example 8.14
**Problem.** For the ellipse $9x^{2} + 25y^{2} = 225$, find the lengths of the
axes, the eccentricity, the foci, the directrices and the latus rectum.

**Solution.** Divide throughout by $225$ to reach standard form:

$$ \frac{9x^{2}}{225} + \frac{25y^{2}}{225} = 1
\quad\Longrightarrow\quad \frac{x^{2}}{25} + \frac{y^{2}}{9} = 1 $$

So $a^{2} = 25$, $b^{2} = 9$, i.e. $a = 5$, $b = 3$, and $a>b$: the major axis
lies along $Ox$.

- Major axis $2a = 10$; minor axis $2b = 6$.
- Eccentricity: $e = \sqrt{1 - \dfrac{9}{25}} = \sqrt{\dfrac{16}{25}}
  = \dfrac45$.
- Foci: $ae = 5 \times \dfrac45 = 4$, so $(\pm 4, 0)$.
- Directrices: $x = \pm \dfrac{a}{e} = \pm \dfrac{5}{4/5} = \pm \dfrac{25}{4}$.
- Latus rectum: $\dfrac{2b^{2}}{a} = \dfrac{2 \times 9}{5} = \dfrac{18}{5}$
  $= 3.6$ units.
:::

::: example Worked example 8.15
**Problem.** Reduce $4x^{2} + 9y^{2} - 16x + 18y - 11 = 0$ to standard form.
Find its centre, the lengths of its axes and its eccentricity.

**Solution.** Group and complete the square in each variable.

$$ 4(x^{2}-4x) + 9(y^{2}+2y) = 11 $$
$$ 4(x^{2}-4x+4) + 9(y^{2}+2y+1) = 11 + 16 + 9 $$
$$ 4(x-2)^{2} + 9(y+1)^{2} = 36 $$

Divide by $36$:

$$ \frac{(x-2)^{2}}{9} + \frac{(y+1)^{2}}{4} = 1 $$

So the centre is $(2,-1)$, with $a^{2}=9$, $b^{2}=4$, i.e. $a=3$, $b=2$ and
$a>b$.

- Major axis $2a = 6$ (parallel to $Ox$); minor axis $2b = 4$.
- Eccentricity $e = \sqrt{1 - \dfrac49} = \dfrac{\sqrt{5}}{3} \approx 0.745$.
- Foci: $ae = \sqrt{5}$, so $(2 \pm \sqrt{5},  -1)$.
:::

### Tangent and normal to an ellipse

::: derivation Condition for $y=mx+c$ to touch the ellipse
Write the ellipse as $b^{2}x^{2} + a^{2}y^{2} = a^{2}b^{2}$ and substitute
$y = mx+c$:

$$ b^{2}x^{2} + a^{2}(mx+c)^{2} = a^{2}b^{2} $$
$$ (b^{2} + a^{2}m^{2})x^{2} + 2a^{2}mc x + a^{2}(c^{2}-b^{2}) = 0 $$

Set the discriminant to zero for a tangent:

$$ 4a^{4}m^{2}c^{2} - 4(b^{2}+a^{2}m^{2}) a^{2}(c^{2}-b^{2}) = 0 $$

Divide by $4a^{2}$ and expand:

$$ a^{2}m^{2}c^{2} = (b^{2}+a^{2}m^{2})(c^{2}-b^{2})
= b^{2}c^{2} - b^{4} + a^{2}m^{2}c^{2} - a^{2}m^{2}b^{2} $$

Cancel $a^{2}m^{2}c^{2}$ from both sides and divide by $b^{2}$:

$$ 0 = c^{2} - b^{2} - a^{2}m^{2} \quad\Longrightarrow\quad
c^{2} = a^{2}m^{2} + b^{2} $$

So $y = mx \pm \sqrt{a^{2}m^{2}+b^{2}}$ are the two tangents of slope $m$.

**Tangent at a point.** Differentiating $\dfrac{x^{2}}{a^{2}} +
\dfrac{y^{2}}{b^{2}} = 1$ gives $\dfrac{2x}{a^{2}} + \dfrac{2y}{b^{2}}
\dfrac{dy}{dx} = 0$, so at $(x_1,y_1)$ the gradient is $-\dfrac{b^{2}x_1}{a^{2}y_1}$
and

$$ y - y_1 = -\frac{b^{2}x_1}{a^{2}y_1}(x-x_1) $$

Multiplying out and using $\dfrac{x_1^{2}}{a^{2}}+\dfrac{y_1^{2}}{b^{2}}=1$ tidies
this to the $T=0$ form

$$ \frac{xx_1}{a^{2}} + \frac{yy_1}{b^{2}} = 1 $$
:::

```figure caption="Tangent and normal at a point. Left: the ellipse $x^2/25+y^2/16=1$ at $P(3, 3.2)$. Right: the hyperbola $x^2/16-y^2/9=1$ at $P(5, 2.25)$. In both cases the tangent comes from the $T=0$ rule and the normal is the perpendicular to it at $P$."
import numpy as np, matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 2, figsize=(5.2, 2.95))
# ---- ellipse x^2/25 + y^2/16 = 1 at P(3, 16/5)
ax = axes[0]
th = np.linspace(0, 2*np.pi, 400)
ax.plot(5*np.cos(th), 4*np.sin(th), color=INK, lw=1.7)
x = np.linspace(-2.0, 8.2, 20); ax.plot(x, (25 - 3*x)/5, color=ACCENT, lw=1.6)
xn = np.linspace(-0.9, 4.4, 20); ax.plot(xn, (25*xn - 27)/15, color=SERIES[1], lw=1.6)
ax.plot([3], [3.2], 'o', color=INK, ms=4.2)
ax.text(2.4, 4.0, '$P(3,\\frac{16}{5})$', fontsize=8.2, ha='right', va='bottom')
ax.text(0.7, -4.3, 'tangent  $3x+5y=25$', color=ACCENT, fontsize=7.9,
        ha='center', va='center')
ax.text(0.7, -5.1, 'normal  $25x-15y=27$', color=SERIES[1], fontsize=7.9,
        ha='center', va='center')
ax.set_title('$\\frac{x^2}{25}+\\frac{y^2}{16}=1$', fontsize=9.2, pad=3)
# ---- hyperbola x^2/16 - y^2/9 = 1 at P(5, 9/4)
ax2 = axes[1]
t = np.linspace(-1.05, 1.05, 300)
for s in (1, -1):
    ax2.plot(s*4*np.cosh(t), 3*np.sinh(t), color=INK, lw=1.7)
xa = np.linspace(-4.6, 4.6, 10)
ax2.plot(xa, 0.75*xa, color=MUTED, lw=0.9, ls='--')
ax2.plot(xa, -0.75*xa, color=MUTED, lw=0.9, ls='--')
x = np.linspace(1.4, 8.2, 20); ax2.plot(x, (5*x - 16)/4, color=ACCENT, lw=1.6)
xn = np.linspace(2.5, 8.2, 20); ax2.plot(xn, (125 - 16*xn)/20, color=SERIES[1], lw=1.6)
ax2.plot([5], [2.25], 'o', color=INK, ms=4.2)
ax2.text(4.35, 3.4, '$P(5,\\frac{9}{4})$', fontsize=8.2, ha='right', va='bottom')
ax2.text(0.7, -4.3, 'tangent  $5x-4y=16$', color=ACCENT, fontsize=7.9,
         ha='center', va='center')
ax2.text(0.7, -5.1, 'normal  $16x+20y=125$', color=SERIES[1], fontsize=7.9,
         ha='center', va='center')
ax2.set_title('$\\frac{x^2}{16}-\\frac{y^2}{9}=1$', fontsize=9.2, pad=3)
for a in axes:
    a.plot([-7.0, 8.4], [0, 0], color=GRID, lw=0.9)
    a.plot([0, 0], [-3.9, 5.2], color=GRID, lw=0.9)
    a.set_xlim(-7.2, 8.6); a.set_ylim(-5.6, 5.4)
    a.set_aspect('equal'); a.axis('off')
fig.subplots_adjust(wspace=0.03)
```

::: key Ellipse — tangency
- Condition of tangency of $y=mx+c$: $\;c^{2} = a^{2}m^{2}+b^{2}$.
- Tangent at $(x_1,y_1)$: $\;\dfrac{xx_1}{a^{2}} + \dfrac{yy_1}{b^{2}} = 1$.
- Normal at $(x_1,y_1)$: $\;\dfrac{a^{2}x}{x_1} - \dfrac{b^{2}y}{y_1} = a^{2}-b^{2}$.
- Tangent at the parametric point $(a\cos\theta, b\sin\theta)$:
  $\;\dfrac{x\cos\theta}{a} + \dfrac{y\sin\theta}{b} = 1$.
- Director circle: $x^{2}+y^{2} = a^{2}+b^{2}$.
:::

::: example Worked example 8.16
**Problem.** Find the equations of the tangent and normal to the ellipse
$\dfrac{x^{2}}{25} + \dfrac{y^{2}}{16} = 1$ at the point $\left(3, \dfrac{16}{5}\right)$.

**Solution.** Check the point: $\dfrac{9}{25} + \dfrac{(16/5)^{2}}{16}
= \dfrac{9}{25} + \dfrac{256/25}{16} = \dfrac{9}{25} + \dfrac{16}{25} = 1$. Good.

*Tangent.* $\dfrac{xx_1}{a^{2}} + \dfrac{yy_1}{b^{2}} = 1$ with $a^{2}=25$,
$b^{2}=16$:

$$ \frac{3x}{25} + \frac{(16/5)y}{16} = 1
\quad\Longrightarrow\quad \frac{3x}{25} + \frac{y}{5} = 1 $$

Multiply by $25$:

$$ 3x + 5y = 25 $$

*Normal.* $\dfrac{a^{2}x}{x_1} - \dfrac{b^{2}y}{y_1} = a^{2}-b^{2}$:

$$ \frac{25x}{3} - \frac{16y}{16/5} = 25 - 16
\quad\Longrightarrow\quad \frac{25x}{3} - 5y = 9 $$

Multiply by $3$:

$$ 25x - 15y = 27 $$

**Check.** The tangent has slope $-3/5$; the normal has slope $25/15 = 5/3$.
The product is $-1$, as it must be.
:::

## 8.6 Standard equation of hyperbola

A **hyperbola** is the conic with $e > 1$. The focus is now *further* from the
vertex than the directrix, and the curve escapes to infinity in two separate
branches.

::: derivation Standard equation of the hyperbola
Take the focus $S(ae,0)$ and the directrix $x = a/e$, exactly as for the
ellipse, but now with $e>1$. The condition $PS = e PM$ again gives

$$ (x-ae)^{2} + y^{2} = (ex-a)^{2} $$
$$ x^{2}(1-e^{2}) + y^{2} = a^{2}(1-e^{2}) $$

This is the *same* intermediate equation as for the ellipse — the whole
difference is the sign of $1-e^{2}$. Since $e>1$, write it as
$-(e^{2}-1)$ and multiply through by $-1$:

$$ x^{2}(e^{2}-1) - y^{2} = a^{2}(e^{2}-1) $$

Divide by $a^{2}(e^{2}-1)$:

$$ \frac{x^{2}}{a^{2}} - \frac{y^{2}}{a^{2}(e^{2}-1)} = 1 $$

Define $b^{2} = a^{2}(e^{2}-1)$ and the **standard equation of the hyperbola**
appears:

$$ \frac{x^{2}}{a^{2}} - \frac{y^{2}}{b^{2}} = 1 $$

with

$$ b^{2} = a^{2}e^{2} - a^{2} \quad\Longrightarrow\quad a^{2}e^{2} = a^{2}+b^{2},
\qquad e = \sqrt{1 + \frac{b^{2}}{a^{2}}} \;>1 $$

**Asymptotes.** Solve for $y$: $\;y = \pm\dfrac{b}{a}\sqrt{x^{2}-a^{2}}
= \pm\dfrac{b}{a}x\sqrt{1 - \dfrac{a^{2}}{x^{2}}}$. As $|x| \to \infty$ the root
tends to $1$, so the curve approaches the pair of lines

$$ y = \pm\frac{b}{a}x, \qquad \text{i.e.}\quad
\frac{x^{2}}{a^{2}} - \frac{y^{2}}{b^{2}} = 0 $$

**Latus rectum.** Putting $x = ae$ gives $y = \pm b^{2}/a$, so each latus rectum
has length $2b^{2}/a$ — the same expression as for the ellipse.

**Focal distance property.** $PS = |ex - a|$ and $PS_1 = |ex+a|$, so

$$ |PS_1 - PS| = 2a $$

*the difference* of the focal distances is constant, where for the ellipse it
was the sum.
:::

```figure caption="The hyperbola $x^2/16-y^2/9=1$ ($a=4$, $b=3$, $e=1.25$) with its asymptotes $y=\pm\frac34x$ dashed, its foci, directrices and latus recta; the green curve is the conjugate hyperbola $y^2/9-x^2/16=1$, which shares the same asymptotes."
import numpy as np, matplotlib.pyplot as plt
a, b, e = 4.0, 3.0, 1.25
fig, ax = plt.subplots(figsize=(5.2, 4.15))
t = np.linspace(-1.42, 1.42, 400)
for s in (1, -1):
    ax.plot(s*a*np.cosh(t), b*np.sinh(t), color=INK, lw=2.0)
    ax.plot(a*np.sinh(t), s*b*np.cosh(t), color=SERIES[2], lw=1.5)
ax.axhline(0, color=GRID, lw=1.0)
ax.plot([0, 0], [-7.2, 6.9], color=GRID, lw=1.0)
xa = np.linspace(-9.1, 9.1, 10)
ax.plot(xa, b*xa/a, color=SERIES[1], lw=1.2, ls='--')
ax.plot(xa, -b*xa/a, color=SERIES[1], lw=1.2, ls='--')
for s in (1, -1):
    ax.plot([s*a*e], [0], 'o', color=INK, ms=4.8)
    ax.plot([s*a], [0], 'o', color=INK, ms=4.0)
    ax.plot([s*a/e, s*a/e], [-7.0, 6.9], color=MUTED, lw=1.1, ls=':')
    ax.plot([s*a*e, s*a*e], [-b*b/a, b*b/a], color=ACCENT, lw=2.4)
ax.text(6.0, -0.5, '$S(ae,0)$', fontsize=8.5, ha='left', va='center')
ax.text(-6.0, -0.5, '$S_1(-ae,0)$', fontsize=8.5, ha='right', va='center')
ax.text(3.6, 0.65, '$A(a,0)$', fontsize=8.4, ha='right', va='center')
ax.text(-3.6, 0.65, '$A_1(-a,0)$', fontsize=8.4, ha='left', va='center')
ax.text(a/e + 0.25, -7.15, '$x=\\frac{a}{e}$', color=MUTED, fontsize=8.4,
        ha='left', va='bottom')
ax.text(-a/e - 0.25, -7.15, '$x=-\\frac{a}{e}$', color=MUTED, fontsize=8.4,
        ha='right', va='bottom')
ax.annotate('asymptotes  $y=\\pm\\frac{b}{a}x$', xy=(2.6, 1.95), xytext=(0.2, -2.3),
            color=SERIES[1], fontsize=8.8, ha='center', va='center',
            arrowprops=dict(arrowstyle='->', color=SERIES[1], lw=0.8))
ax.annotate('latus rectum $=\\frac{2b^2}{a}$', xy=(5.0, 0.95), xytext=(7.2, 3.4),
            color=ACCENT, fontsize=8.4, ha='center', va='center',
            arrowprops=dict(arrowstyle='->', color=ACCENT, lw=0.8))
ax.text(-9.9, 8.0, '$\\frac{x^2}{a^2}-\\frac{y^2}{b^2}=1$,   $b^2=a^2(e^2-1)$,   $e>1$',
        color=INK, fontsize=9.4, ha='left', va='center')
ax.text(9.9, 8.0, 'conjugate:  $\\frac{y^2}{b^2}-\\frac{x^2}{a^2}=1$',
        color=SERIES[2], fontsize=9.4, ha='right', va='center')
ax.set_xlim(-10.1, 10.1); ax.set_ylim(-7.7, 8.9)
ax.set_aspect('equal'); ax.axis('off')
```

::: key Hyperbola $\dfrac{x^{2}}{a^{2}} - \dfrac{y^{2}}{b^{2}} = 1$ — elements
| Element | Value |
|---|---|
| Centre | $(0,0)$ |
| Vertices | $(\pm a, 0)$ — the curve does not cross $Oy$ |
| Transverse / conjugate axis | $2a$ / $2b$ |
| Eccentricity | $e = \sqrt{1 + b^{2}/a^{2}} > 1$ |
| Foci | $(\pm ae, 0)$, with $a^{2}e^{2} = a^{2}+b^{2}$ |
| Directrices | $x = \pm a/e$ |
| Latus rectum | $2b^{2}/a$ |
| Asymptotes | $y = \pm \dfrac{b}{a}x$ |

- **Conjugate hyperbola:** $\dfrac{y^{2}}{b^{2}} - \dfrac{x^{2}}{a^{2}} = 1$, with
  foci $(0,\pm be)$ and eccentricity $e_1 = \sqrt{1+a^{2}/b^{2}}$. It shares the
  asymptotes, and $\dfrac{1}{e^{2}} + \dfrac{1}{e_1^{2}} = 1$.
- **Rectangular (equilateral) hyperbola:** $a = b$, so
  $x^{2}-y^{2}=a^{2}$, asymptotes $y = \pm x$ at right angles, and
  $e = \sqrt{2}$.
- Condition of tangency of $y = mx+c$: $\;c^{2} = a^{2}m^{2} - b^{2}$.
- Tangent at $(x_1,y_1)$: $\;\dfrac{xx_1}{a^{2}} - \dfrac{yy_1}{b^{2}} = 1$.
- Normal at $(x_1,y_1)$: $\;\dfrac{a^{2}x}{x_1} + \dfrac{b^{2}y}{y_1} = a^{2}+b^{2}$.
:::

::: caution $a^{2}e^{2} = a^{2}+b^{2}$, not $a^{2}-b^{2}$
For the ellipse $b^{2} = a^{2}(1-e^{2})$ and $a^{2}e^{2} = a^{2}-b^{2}$; for the
hyperbola $b^{2} = a^{2}(e^{2}-1)$ and $a^{2}e^{2} = a^{2}+b^{2}$. One sign flip
changes the eccentricity, the foci and the directrices together. Decide which
conic you have *before* touching $e$.
:::

::: example Worked example 8.17
**Problem.** Find the equation of the hyperbola whose foci are $(\pm 5,0)$ and
whose eccentricity is $5/4$.

**Solution.** The foci are on the $x$-axis, so the form is
$\dfrac{x^{2}}{a^{2}} - \dfrac{y^{2}}{b^{2}} = 1$ with foci $(\pm ae,0)$.

$$ ae = 5, \quad e = \frac54 \quad\Longrightarrow\quad a = \frac{5}{5/4} = 4 $$

$$ b^{2} = a^{2}(e^{2}-1) = 16\left(\frac{25}{16} - 1\right) = 25 - 16 = 9 $$

The hyperbola is

$$ \frac{x^{2}}{16} - \frac{y^{2}}{9} = 1 $$

**Check.** $a^{2}+b^{2} = 16+9 = 25 = (ae)^{2}$. Correct.
:::

::: example Worked example 8.18
**Problem.** For the hyperbola $9x^{2} - 16y^{2} = 144$, find the vertices,
eccentricity, foci, directrices, length of latus rectum and the asymptotes.

**Solution.** Divide by $144$:

$$ \frac{x^{2}}{16} - \frac{y^{2}}{9} = 1 $$

so $a^{2}=16$, $b^{2}=9$, i.e. $a = 4$, $b = 3$.

- Vertices: $(\pm 4, 0)$; transverse axis $2a = 8$, conjugate axis $2b = 6$.
- Eccentricity: $e = \sqrt{1 + \dfrac{9}{16}} = \sqrt{\dfrac{25}{16}}
  = \dfrac54$.
- Foci: $ae = 4 \times \dfrac54 = 5$, so $(\pm 5, 0)$.
- Directrices: $x = \pm \dfrac{a}{e} = \pm \dfrac{4}{5/4} = \pm \dfrac{16}{5}$.
- Latus rectum: $\dfrac{2b^{2}}{a} = \dfrac{18}{4} = \dfrac92 = 4.5$ units.
- Asymptotes: $y = \pm \dfrac{b}{a}x = \pm \dfrac34 x$, i.e. $3x \pm 4y = 0$.
:::

::: example Worked example 8.19
**Problem.** Find the equations of the tangent and the normal to the hyperbola
$\dfrac{x^{2}}{16} - \dfrac{y^{2}}{9} = 1$ at the point $\left(5, \dfrac94\right)$.

**Solution.** Check: $\dfrac{25}{16} - \dfrac{(9/4)^{2}}{9}
= \dfrac{25}{16} - \dfrac{81/16}{9} = \dfrac{25}{16} - \dfrac{9}{16} = 1$. Good.

*Tangent.* $\dfrac{xx_1}{a^{2}} - \dfrac{yy_1}{b^{2}} = 1$:

$$ \frac{5x}{16} - \frac{(9/4)y}{9} = 1
\quad\Longrightarrow\quad \frac{5x}{16} - \frac{y}{4} = 1 $$

Multiply by $16$:

$$ 5x - 4y = 16 $$

*Normal.* $\dfrac{a^{2}x}{x_1} + \dfrac{b^{2}y}{y_1} = a^{2}+b^{2}$:

$$ \frac{16x}{5} + \frac{9y}{9/4} = 16+9
\quad\Longrightarrow\quad \frac{16x}{5} + 4y = 25 $$

Multiply by $5$:

$$ 16x + 20y = 125 $$

**Check.** Tangent slope $= 5/4$; normal slope $= -16/20 = -4/5$. Their product
is $-1$.
:::

::: key The four conics side by side
| | Circle | Parabola | Ellipse $(a>b)$ | Hyperbola |
|---|---|---|---|---|
| Standard equation | $x^{2}+y^{2}=a^{2}$ | $y^{2}=4ax$ | $\dfrac{x^{2}}{a^{2}}+\dfrac{y^{2}}{b^{2}}=1$ | $\dfrac{x^{2}}{a^{2}}-\dfrac{y^{2}}{b^{2}}=1$ |
| Eccentricity | $e=0$ | $e=1$ | $e=\sqrt{1-\dfrac{b^{2}}{a^{2}}}<1$ | $e=\sqrt{1+\dfrac{b^{2}}{a^{2}}}>1$ |
| Centre / vertex | centre $(0,0)$ | vertex $(0,0)$ | centre $(0,0)$ | centre $(0,0)$ |
| Vertices | every point | $(0,0)$ | $(\pm a,0)$ | $(\pm a,0)$ |
| Foci | centre only | $(a,0)$ | $(\pm ae,0)$ | $(\pm ae,0)$ |
| Relation | — | — | $a^{2}e^{2}=a^{2}-b^{2}$ | $a^{2}e^{2}=a^{2}+b^{2}$ |
| Directrices | none | $x=-a$ | $x=\pm \dfrac ae$ | $x=\pm \dfrac ae$ |
| Latus rectum | — | $4a$ | $\dfrac{2b^{2}}{a}$ | $\dfrac{2b^{2}}{a}$ |
| Asymptotes | none | none | none | $y=\pm\dfrac ba x$ |
| Tangency of $y=mx+c$ | $c^{2}=a^{2}(1+m^{2})$ | $c=\dfrac am$ | $c^{2}=a^{2}m^{2}+b^{2}$ | $c^{2}=a^{2}m^{2}-b^{2}$ |
| Tangent at $(x_1,y_1)$ | $xx_1+yy_1=a^{2}$ | $yy_1=2a(x+x_1)$ | $\dfrac{xx_1}{a^{2}}+\dfrac{yy_1}{b^{2}}=1$ | $\dfrac{xx_1}{a^{2}}-\dfrac{yy_1}{b^{2}}=1$ |

Learn this table. Roughly a third of the marks in this unit are a direct
read-off from one of its rows.
:::

## Chapter summary

- A **conic** is the locus of $P$ with $PS/PM = e$, where $S$ is the focus and the
  directrix gives $PM$. $e=0$ circle, $0<e<1$ ellipse, $e=1$ parabola,
  $e>1$ hyperbola. The **latus rectum** is the focal chord perpendicular to the
  axis.
- **Circle:** $(x-h)^{2}+(y-k)^{2}=r^{2}$; general form
  $x^{2}+y^{2}+2gx+2fy+c=0$ has centre $(-g,-f)$ and
  $r=\sqrt{g^{2}+f^{2}-c}$; diameter form
  $(x-x_1)(x-x_2)+(y-y_1)(y-y_2)=0$.
- A line **touches** a circle when the perpendicular distance from the centre
  equals the radius; for $x^{2}+y^{2}=a^{2}$ and $y=mx+c$ this is
  $c^{2}=a^{2}(1+m^{2})$, with contact point $(-a^{2}m/c,\ a^{2}/c)$.
- Tangent to $x^{2}+y^{2}=a^{2}$ at $(x_1,y_1)$ is $xx_1+yy_1=a^{2}$; the normal
  always passes through the centre; the length of the tangent from $(x_1,y_1)$ is
  $\sqrt{S_1}$; the director circle is $x^{2}+y^{2}=2a^{2}$.
- **Parabola:** $y^{2}=4ax$ has vertex $(0,0)$, focus $(a,0)$, directrix $x=-a$,
  latus rectum $4a$, parametric point $(at^{2},2at)$. Three sign/axis variants
  give the other three orientations.
- Parabola tangency: $y=mx+a/m$ touches at $(a/m^{2}, 2a/m)$; the tangent at
  $(x_1,y_1)$ is $yy_1=2a(x+x_1)$; the subnormal is always $2a$.
- **Ellipse:** $\dfrac{x^{2}}{a^{2}}+\dfrac{y^{2}}{b^{2}}=1$ with
  $b^{2}=a^{2}(1-e^{2})$; foci $(\pm ae,0)$, directrices $x=\pm a/e$, latus
  rectum $2b^{2}/a$, and $PS+PS_1=2a$. If $b>a$ everything rotates onto the
  $y$-axis.
- **Hyperbola:** $\dfrac{x^{2}}{a^{2}}-\dfrac{y^{2}}{b^{2}}=1$ with
  $b^{2}=a^{2}(e^{2}-1)$; foci $(\pm ae,0)$, directrices $x=\pm a/e$, latus
  rectum $2b^{2}/a$, asymptotes $y=\pm bx/a$, and $|PS_1-PS|=2a$. Rectangular
  when $a=b$, where $e=\sqrt{2}$.
- Tangency conditions in one line: circle $c^{2}=a^{2}(1+m^{2})$; parabola
  $c=a/m$; ellipse $c^{2}=a^{2}m^{2}+b^{2}$; hyperbola $c^{2}=a^{2}m^{2}-b^{2}$.
  Tangents at a point all follow the rule $T=0$.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The radius of the circle $x^{2}+y^{2}-4x+6y-12 = 0$ is <span class="marks">[1]</span>
   (a) $3$ (b) $4$ (c) $5$ (d) $6$
2. The line $y = x + c$ touches the circle $x^{2}+y^{2} = 8$ when $c$ equals <span class="marks">[1]</span>
   (a) $\pm 2$ (b) $\pm 2\sqrt{2}$ (c) $\pm 4$ (d) $\pm 8$
3. The eccentricity of the ellipse $16x^{2} + 25y^{2} = 400$ is <span class="marks">[1]</span>
   (a) $\dfrac{3}{5}$ (b) $\dfrac{4}{5}$ (c) $\dfrac{5}{4}$ (d) $\dfrac{9}{25}$
4. The focus of the parabola $y^{2} = -8x$ is <span class="marks">[1]</span>
   (a) $(2,0)$ (b) $(-2,0)$ (c) $(0,2)$ (d) $(0,-2)$
5. The foci of the hyperbola $\dfrac{x^{2}}{9} - \dfrac{y^{2}}{16} = 1$ are <span class="marks">[1]</span>
   (a) $(\pm 4,0)$ (b) $(\pm 5,0)$ (c) $(0,\pm 5)$ (d) $(\pm 7,0)$
6. The length of the latus rectum of $\dfrac{x^{2}}{16} + \dfrac{y^{2}}{9} = 1$ is <span class="marks">[1]</span>
   (a) $\dfrac{9}{2}$ (b) $\dfrac{9}{4}$ (c) $\dfrac{32}{3}$ (d) $6$
7. The tangent to the circle $x^{2}+y^{2} = 25$ at the point $(3,4)$ is <span class="marks">[1]</span>
   (a) $4x+3y=25$ (b) $3x+4y=25$ (c) $3x-4y=25$ (d) $4x-3y=0$
8. The eccentricity of a rectangular hyperbola is <span class="marks">[1]</span>
   (a) $1$ (b) $\sqrt{2}$ (c) $2$ (d) $\dfrac{1}{\sqrt{2}}$
9. The directrix of the parabola $y^{2} = 12x$ is <span class="marks">[1]</span>
   (a) $x = 3$ (b) $x = -3$ (c) $y = -3$ (d) $x = -12$
10. The length of the tangent drawn from $(4,3)$ to the circle $x^{2}+y^{2} = 9$ is <span class="marks">[1]</span>
    (a) $3$ (b) $4$ (c) $5$ (d) $\sqrt{34}$

::: note Answers to Group A
**1.** (c) — $g=-2$, $f=3$, $c=-12$, so $r = \sqrt{4+9+12} = \sqrt{25} = 5$.

**2.** (c) — $c^{2} = a^{2}(1+m^{2}) = 8(1+1) = 16$, so $c = \pm4$.

**3.** (a) — dividing by $400$ gives $\dfrac{x^{2}}{25}+\dfrac{y^{2}}{16}=1$, so
$e = \sqrt{1-\tfrac{16}{25}} = \tfrac35$.

**4.** (b) — $4a = 8$ so $a = 2$; the curve opens left, focus $(-a,0) = (-2,0)$.

**5.** (b) — $a^{2}e^{2} = a^{2}+b^{2} = 9+16 = 25$, so $ae = 5$.

**6.** (a) — $a^{2}=16$, $b^{2}=9$, and $\dfrac{2b^{2}}{a} = \dfrac{18}{4}
= \dfrac92$.

**7.** (b) — $xx_1+yy_1 = a^{2}$ gives $3x+4y = 25$.

**8.** (b) — $a=b$ makes $e = \sqrt{1 + a^{2}/a^{2}} = \sqrt{2}$.

**9.** (b) — $4a=12$ so $a=3$; the directrix is $x = -a = -3$.

**10.** (b) — $\sqrt{S_1} = \sqrt{16+9-9} = 4$.
:::

**Group B — Short answer (5 marks each)**

1. Find the equation of the circle passing through the points $(-1,1)$ and
   $(6,2)$ whose centre lies on the line $2x+y = 4$. State its centre and
   radius. <span class="marks">[5]</span>
2. Find the equations of the tangents to the circle $x^{2}+y^{2} = 16$ which are
   parallel to the line $3x+4y = 5$. <span class="marks">[5]</span>
3. Find the vertex, focus, directrix, axis and length of latus rectum of the
   parabola $y^{2}+4y+4x-4 = 0$. <span class="marks">[5]</span>
4. Find the equation of the tangent to the parabola $y^{2} = 8x$ which makes an
   angle of $45^{\circ}$ with the $x$-axis. Find the point of contact and the
   equation of the normal there. <span class="marks">[5]</span>
5. Find the equation of the ellipse whose foci are $(\pm 3, 0)$ and whose latus
   rectum has length $\dfrac{32}{5}$. Also find its
   eccentricity. <span class="marks">[5]</span>
6. Find the eccentricity, foci, directrices and length of latus rectum of the
   hyperbola $25x^{2} - 144y^{2} = 3600$. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Let the circle be $x^{2}+y^{2}+2gx+2fy+c = 0$, centre $(-g,-f)$.

Through $(-1,1)$: $\;1+1-2g+2f+c = 0 \Rightarrow -2g+2f+c = -2$.
Through $(6,2)$: $\;36+4+12g+4f+c = 0 \Rightarrow 12g+4f+c = -40$.
Centre on $2x+y=4$: $\;2(-g)+(-f) = 4 \Rightarrow 2g+f = -4$.

From the third equation $f = -4-2g$. Substituting into the first two:
$-2g+2(-4-2g)+c=-2 \Rightarrow -6g+c = 6$, and
$12g+4(-4-2g)+c = -40 \Rightarrow 4g+c = -24$. Subtracting,
$10g = -30$, so $g = -3$, then $c = -24-4(-3) = -12$ and $f = -4+6 = 2$.

$$ x^{2}+y^{2}-6x+4y-12 = 0 $$

Centre $(3,-2)$ and $r = \sqrt{9+4+12} = 5$. (Check: the distance from $(3,-2)$
to $(6,2)$ is $\sqrt{9+16}=5$.)

**2.** Lines parallel to $3x+4y=5$ have slope $m = -\dfrac34$. With $a^{2}=16$,

$$ c^{2} = a^{2}(1+m^{2}) = 16\left(1+\frac{9}{16}\right) = 25
\quad\Longrightarrow\quad c = \pm 5 $$

So $y = -\dfrac34 x \pm 5$, i.e.

$$ 3x + 4y = 20 \qquad\text{and}\qquad 3x + 4y = -20 $$

Check: the distance from $(0,0)$ to $3x+4y-20=0$ is $20/5 = 4 = r$.

**3.** Only $y$ is squared, so complete the square in $y$:

$$ y^{2}+4y = 4-4x \Rightarrow y^{2}+4y+4 = 8-4x \Rightarrow (y+2)^{2} = -4(x-2) $$

Compare with $(y-k)^{2} = -4a(x-h)$: $h=2$, $k=-2$, $4a=4$ so $a=1$, and the
parabola opens **left**.

Vertex $(2,-2)$; axis $y = -2$; focus $1$ unit left of the vertex, $(1,-2)$;
directrix $1$ unit right, $x = 3$; latus rectum $4a = 4$ units.

**4.** $y^{2}=8x$ gives $4a=8$, so $a=2$. A $45^{\circ}$ line has $m = \tan 45^{\circ} = 1$.
For a tangent, $c = \dfrac{a}{m} = 2$, so the tangent is

$$ y = x+2 $$

Point of contact $\left(\dfrac{a}{m^{2}}, \dfrac{2a}{m}\right) = (2,4)$.
(Check: $4^{2} = 16 = 8(2)$.)

Normal gradient $= -\dfrac{y_1}{2a} = -\dfrac{4}{4} = -1$, so
$y-4 = -(x-2)$, i.e.

$$ x + y = 6 $$

**5.** Foci $(\pm 3,0)$ lie on $Ox$, so $a>b$, $ae = 3$ and
$a^{2}-b^{2} = 9$. The latus rectum gives

$$ \frac{2b^{2}}{a} = \frac{32}{5} \quad\Longrightarrow\quad b^{2} = \frac{16a}{5} $$

Substituting into $a^{2}-b^{2}=9$:

$$ a^{2} - \frac{16a}{5} = 9 \Rightarrow 5a^{2}-16a-45 = 0
\Rightarrow (a-5)(5a+9) = 0 $$

so $a = 5$ (the negative root is rejected), and $b^{2} = \dfrac{16 \times 5}{5}
= 16$. The ellipse is

$$ \frac{x^{2}}{25} + \frac{y^{2}}{16} = 1 $$

with $e = \dfrac{ae}{a} = \dfrac35$.

**6.** Divide by $3600$:

$$ \frac{x^{2}}{144} - \frac{y^{2}}{25} = 1 $$

so $a = 12$, $b = 5$.

$$ e = \sqrt{1 + \frac{25}{144}} = \sqrt{\frac{169}{144}} = \frac{13}{12} $$

Foci: $ae = 12 \times \dfrac{13}{12} = 13$, so $(\pm 13, 0)$.
Directrices: $x = \pm\dfrac ae = \pm\dfrac{12}{13/12} = \pm\dfrac{144}{13}$.
Latus rectum: $\dfrac{2b^{2}}{a} = \dfrac{50}{12} = \dfrac{25}{6}$ units.
:::

**Group C — Long answer (8 marks each)**

1. (a) Define a conic section in terms of focus, directrix and eccentricity, and
   derive the standard equation $y^{2} = 4ax$ of a parabola. <span class="marks">[5]</span>
   (b) Hence find the vertex, focus, directrix and length of latus rectum of
   $y^{2} - 6y - 8x + 25 = 0$. <span class="marks">[3]</span>
2. (a) Derive the standard equation $\dfrac{x^{2}}{a^{2}} + \dfrac{y^{2}}{b^{2}} = 1$
   of an ellipse from the focus–directrix definition, stating clearly where
   $b^{2} = a^{2}(1-e^{2})$ comes from. <span class="marks">[5]</span>
   (b) Find the axes, eccentricity, foci, directrices and latus rectum of
   $25x^{2} + 9y^{2} = 225$. <span class="marks">[3]</span>
3. (a) Find the condition that the line $y = mx+c$ is a tangent to the ellipse
   $\dfrac{x^{2}}{a^{2}} + \dfrac{y^{2}}{b^{2}} = 1$. <span class="marks">[4]</span>
   (b) Hence find the tangents of slope $1$ to $\dfrac{x^{2}}{16} + \dfrac{y^{2}}{9} = 1$. <span class="marks">[2]</span>
   (c) Find the tangent and the normal to $\dfrac{x^{2}}{9} + \dfrac{y^{2}}{4} = 1$
   at the point $\left(\sqrt{5}, \dfrac43\right)$. <span class="marks">[2]</span>

::: note Answers to Group C
**1. (a)** A conic section is the locus of a point $P$ whose distance from a
fixed point $S$ (focus) bears a constant ratio $e$ (eccentricity) to its
distance from a fixed line (directrix): $PS = e PM$. For a parabola $e = 1$.

Take $S(a,0)$ and the directrix $x+a = 0$, so that the origin bisects the
perpendicular from $S$ to the directrix. For $P(x,y)$,

$$ PS = PM \Rightarrow \sqrt{(x-a)^{2}+y^{2}} = |x+a| $$
$$ (x-a)^{2}+y^{2} = (x+a)^{2} $$
$$ x^{2}-2ax+a^{2}+y^{2} = x^{2}+2ax+a^{2} $$
$$ y^{2} = 4ax $$

Putting $x=a$ gives $y=\pm2a$, so the latus rectum has length $4a$.

**(b)** $y^{2}-6y = 8x-25$, so $y^{2}-6y+9 = 8x-16$, i.e.

$$ (y-3)^{2} = 8(x-2) $$

Here $4a = 8$, so $a = 2$; the parabola opens right from vertex $(2,3)$.
Focus $(2+2, 3) = (4,3)$; directrix $x = 2-2 = 0$; axis $y = 3$; latus rectum
$= 8$ units.

**2. (a)** Let $S(ae,0)$ be the focus and $x = a/e$ the directrix, with
$0<e<1$. For $P(x,y)$, $PS = e PM$ gives

$$ \sqrt{(x-ae)^{2}+y^{2}} = e\left|x-\frac ae\right| = |ex-a| $$
$$ x^{2}-2aex+a^{2}e^{2}+y^{2} = e^{2}x^{2}-2aex+a^{2} $$
$$ x^{2}(1-e^{2}) + y^{2} = a^{2}(1-e^{2}) $$

Dividing by $a^{2}(1-e^{2})$, which is positive because $e<1$,

$$ \frac{x^{2}}{a^{2}} + \frac{y^{2}}{a^{2}(1-e^{2})} = 1 $$

The denominator under $y^{2}$ is a positive constant; calling it $b^{2}$, i.e.
defining $b^{2} = a^{2}(1-e^{2})$, gives
$\dfrac{x^{2}}{a^{2}} + \dfrac{y^{2}}{b^{2}} = 1$ with $b<a$. Rearranging the
definition also gives $a^{2}e^{2} = a^{2}-b^{2}$.

**(b)** Divide by $225$: $\;\dfrac{x^{2}}{9} + \dfrac{y^{2}}{25} = 1$. Here
$a^{2}=9$ and $b^{2}=25$, so $b>a$ and the **major axis is along $Oy$**.

Major axis $2b = 10$; minor axis $2a = 6$.
$e = \sqrt{1-\dfrac{a^{2}}{b^{2}}} = \sqrt{1-\dfrac{9}{25}} = \dfrac45$.
Foci $(0,\pm be) = (0,\pm 4)$. Directrices $y = \pm\dfrac be = \pm\dfrac{25}{4}$.
Latus rectum $\dfrac{2a^{2}}{b} = \dfrac{18}{5}$ units.

**3. (a)** Write the ellipse as $b^{2}x^{2}+a^{2}y^{2} = a^{2}b^{2}$ and put
$y = mx+c$:

$$ (b^{2}+a^{2}m^{2})x^{2} + 2a^{2}mc x + a^{2}(c^{2}-b^{2}) = 0 $$

For tangency the roots coincide, so the discriminant is zero:

$$ 4a^{4}m^{2}c^{2} = 4a^{2}(b^{2}+a^{2}m^{2})(c^{2}-b^{2}) $$
$$ a^{2}m^{2}c^{2} = b^{2}c^{2}-b^{4}+a^{2}m^{2}c^{2}-a^{2}m^{2}b^{2} $$
$$ 0 = b^{2}\left(c^{2}-b^{2}-a^{2}m^{2}\right)
\quad\Longrightarrow\quad c^{2} = a^{2}m^{2}+b^{2} $$

**(b)** With $a^{2}=16$, $b^{2}=9$, $m=1$: $\;c^{2} = 16+9 = 25$, so $c=\pm5$
and the tangents are

$$ y = x+5 \qquad\text{and}\qquad y = x-5 $$

**(c)** Check the point: $\dfrac59 + \dfrac{16/9}{4} = \dfrac59+\dfrac49 = 1$.

Tangent $\dfrac{xx_1}{a^{2}}+\dfrac{yy_1}{b^{2}} = 1$:

$$ \frac{\sqrt{5} x}{9} + \frac{(4/3)y}{4} = 1 \Rightarrow
\frac{\sqrt{5} x}{9}+\frac{y}{3} = 1 \Rightarrow \sqrt{5} x + 3y = 9 $$

Normal $\dfrac{a^{2}x}{x_1}-\dfrac{b^{2}y}{y_1} = a^{2}-b^{2}$:

$$ \frac{9x}{\sqrt{5}} - \frac{4y}{4/3} = 9-4 \Rightarrow
\frac{9x}{\sqrt{5}} - 3y = 5 \Rightarrow 9x - 3\sqrt{5} y = 5\sqrt{5} $$
:::
