---
subject: Optional Mathematics
grade: 10
unit: 7
title: Conic Sections and Circle
hours: 0
area: Units
---

A bicycle wheel, the path of a football kicked high, the shape of a satellite dish and the orbit of a planet are all curves you can get by slicing a cone with a flat plane. These curves are the **conic sections**. The simplest one, the **circle**, is also the easiest to handle with algebra, because it is just "all points at a fixed distance from a fixed point". This chapter names the four conic sections and then builds the equation of a circle in its three forms: centre–radius, diameter, and general. It ends with the questions the SEE asks: find the centre and radius, find the equation from given conditions, and find the circle through three points.

::: key What the SEE asks from this chapter
Expect (i) the centre and radius from an equation such as $x^2+y^2-6x+8y-11=0$; (ii) the equation of a circle from its centre and radius, or from the ends of a diameter; (iii) the circle through three given points; (iv) a circle that touches the axes or has its centre on given lines. The whole chapter rests on the distance formula $d=\sqrt{(x_2-x_1)^2+(y_2-y_1)^2}$.
:::

```photo id="omath10/satellite-dish" caption="A satellite dish is a paraboloid. Rays arriving parallel to its axis all reflect to a single point, the focus — the property that makes the parabola a conic worth studying." width="66"
```

## 7.1 Conic sections: circle, parabola, ellipse and hyperbola

### The cone

Take two lines $AB$ and $CD$ that cross at a point $O$ at an acute angle. Rotate $AB$ about $CD$. The line $AB$ sweeps out a surface called a **right circular cone**. The point $O$ is the **vertex**, $CD$ is the **axis**, $AB$ is a **generator** (a slant edge) and the angle between the axis and a generator is the **semi-vertical angle** $\alpha$. If the rotation is continued on both sides of $O$ we get a **double cone**.

### Cutting the cone

Cut a cone with a flat plane. The shape of the cut depends on the angle $\beta$ the plane makes with the axis, compared with the semi-vertical angle $\alpha$ of the cone.

| Plane | Section | How to remember it |
|---|---|---|
| perpendicular to the axis (parallel to the base) | **circle** | cut a carrot straight across |
| tilted, cutting every generator of one nappe | **ellipse** | cut a carrot at a slant: an oval |
| parallel to one generator (slant edge) | **parabola** | one open curve, like a thrown ball's path |
| steeper than a generator, cutting both nappes | **hyperbola** | two separate open branches |

```figure caption="Top row: the cone seen from the side with the cutting plane drawn as a line. Bottom row: the section it produces. Circle, ellipse, parabola and hyperbola."
import numpy as np, matplotlib.pyplot as plt
fig, axs = plt.subplots(2, 4, figsize=(5.0, 2.9), gridspec_kw={'height_ratios':[1.25, 1]})
names = ['Circle', 'Ellipse', 'Parabola', 'Hyperbola']
betas = [0, 25, 60, 80]
a = np.tan(np.radians(30))
for k in range(4):
    ax = axs[0, k]
    ax.plot([-2*a, 2*a], [-2, 2], color=INK, lw=1.0)
    ax.plot([-2*a, 2*a], [2, -2], color=INK, lw=1.0)
    b = np.radians(betas[k])
    cx, cy = 0.0, 1.1
    L = 1.0 if betas[k] < 70 else 1.9
    ax.plot([cx-L*np.cos(b), cx+L*np.cos(b)], [cy-L*np.sin(b), cy+L*np.sin(b)], color=SERIES[1], lw=1.6)
    ax.plot([0, 0], [-2.2, 2.2], color=MUTED, lw=0.6, ls='--')
    ax.set_xlim(-1.7, 1.7); ax.set_ylim(-2.3, 2.3); ax.set_aspect('equal'); ax.axis('off')
    ax.set_title(names[k], fontsize=8, pad=1)
t = np.linspace(0, 2*np.pi, 200)
axs[1, 0].plot(np.cos(t), np.sin(t), color=ACCENT, lw=1.5)
axs[1, 1].plot(1.4*np.cos(t), 0.9*np.sin(t), color=ACCENT, lw=1.5)
u = np.linspace(-1.4, 1.4, 100)
axs[1, 2].plot(u**2*0.7, u, color=ACCENT, lw=1.5)
v = np.linspace(-1.2, 1.2, 100)
axs[1, 3].plot(np.cosh(v), np.sinh(v), color=ACCENT, lw=1.5)
axs[1, 3].plot(-np.cosh(v), np.sinh(v), color=ACCENT, lw=1.5)
for ax in axs[1]:
    ax.set_aspect('equal'); ax.axis('off')
axs[1, 0].set_xlim(-1.7, 1.7); axs[1, 1].set_xlim(-1.7, 1.7); axs[1, 2].set_xlim(-0.3, 1.7); axs[1, 3].set_xlim(-2.2, 2.2)
fig.tight_layout(pad=0.3)
```

A circle is the special case of an ellipse in which the plane is perpendicular to the axis. In every case the section is a **curve with a simple description as a locus** (the path of a moving point). For a circle the rule is:

::: definition Circle
A **circle** is the locus of a point that moves in a plane so that its distance from a fixed point (the **centre**) is always constant. The constant distance is the **radius**.
:::

| Conic | Locus description (for interest) | Eccentricity $e$ |
|---|---|---|
| Circle | fixed distance from the centre | $0$ |
| Ellipse | sum of distances from two foci is constant | $0<e<1$ |
| Parabola | equal distance from a focus and a line (directrix) | $e=1$ |
| Hyperbola | difference of distances from two foci is constant | $e>1$ |

At Grade 10 we study only the **equation of the circle**; the other conics are met in Grade 11 and 12.

::: example Naming the conic
**Problem.** A plane cuts a cone (i) parallel to its base, (ii) parallel to a slant edge, (iii) at a slant, without being parallel to any edge. Name each section.

**Solution.** (i) circle; (ii) parabola; (iii) ellipse. If the plane cuts both halves of a double cone, parallel to the axis, we get a hyperbola.
:::

## 7.2 Equation of a circle: centre and radius form

::: derivation Equation of a circle with centre $(h,k)$ and radius $r$
**Setting up.** Let the centre be $M(h,k)$, the radius $r$, and let $P(x,y)$ be **any** point on the circle.

**Step 1 — use the definition.** $P$ lies on the circle exactly when $MP=r$.

**Step 2 — distance formula.**

$$ MP=\sqrt{(x-h)^2+(y-k)^2}=r $$

**Step 3 — square both sides.**

$$ (x-h)^2+(y-k)^2=r^2 $$

**Result.** This is the equation of the circle. If the centre is the origin, $h=k=0$ and it becomes $x^2+y^2=r^2$.

**What it means.** Every point that satisfies the equation is exactly $r$ from the centre, and every point on the circle satisfies it. To read off the centre, take the numbers that are **subtracted** from $x$ and $y$ (with their signs reversed).
:::

```figure caption="A circle of centre $M(h,k)$ and radius $r$. The point $P(x,y)$ is on the circle when $MP=r$, i.e. $(x-h)^2+(y-k)^2=r^2$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.2, 3.4))
h, k, r = 3, 2.5, 2
t = np.linspace(0, 2*np.pi, 200)
ax.plot(h+r*np.cos(t), k+r*np.sin(t), color=ACCENT, lw=1.7)
ax.plot([h], [k], 'o', color=INK, ms=4)
ang = np.radians(35)
px, py = h+r*np.cos(ang), k+r*np.sin(ang)
ax.plot([h, px], [k, py], color=INK, lw=1.1)
ax.plot([px], [py], 'o', color=SERIES[1], ms=4.5)
ax.text(h-0.15, k-0.35, 'M(h, k)', fontsize=8.5, ha='right')
ax.text(px+0.1, py+0.1, 'P(x, y)', fontsize=8.5)
ax.text(h+0.55, k+0.12, 'r', fontsize=9, color=INK)
ax.annotate('', xy=(5.6, 0), xytext=(-0.3, 0), arrowprops=dict(arrowstyle='->', color=MUTED, lw=0.8))
ax.annotate('', xy=(0, 5.2), xytext=(0, -0.3), arrowprops=dict(arrowstyle='->', color=MUTED, lw=0.8))
ax.plot([h, h], [0, k], color=MUTED, lw=0.7, ls='--'); ax.plot([0, h], [k, k], color=MUTED, lw=0.7, ls='--')
ax.text(h, -0.45, 'h', fontsize=8.5, ha='center'); ax.text(-0.2, k, 'k', fontsize=8.5, ha='right', va='center')
ax.set_xlim(-0.6, 6.0); ax.set_ylim(-0.8, 5.5); ax.set_aspect('equal'); ax.axis('off')
fig.tight_layout(pad=0.3)
```

::: key Circle: centre–radius form
$$ (x-h)^2+(y-k)^2=r^2 \qquad\text{centre }(h,k),\ \text{radius }r $$

$$ x^2+y^2=r^2 \qquad\text{centre at the origin} $$
:::

::: example Centre and radius from the equation
**Problem.** Find the centre and radius of (a) $(x-2)^2+y^2=4$; (b) $(x+2)^2+(y-1)^2=9$; (c) $x^2+y^2=25$.

**Solution.** Compare with $(x-h)^2+(y-k)^2=r^2$.

(a) $y^2=(y-0)^2$, so $h=2$, $k=0$, $r^2=4$: centre $(2,0)$, radius $2$.

(b) $(x+2)=(x-(-2))$, so $h=-2$, $k=1$, $r^2=9$: centre $(-2,1)$, radius $3$.

(c) centre $(0,0)$, radius $5$.
:::

::: example Equation from centre and radius
**Problem.** Find the equation of the circle (a) with centre at the origin and radius $4$; (b) with centre $(-4,5)$ and radius $6$.

**Solution.** (a) $x^2+y^2=16$.

(b) $(x+4)^2+(y-5)^2=36$. Expand: $x^2+8x+16+y^2-10y+25=36$, so

$$ x^2+y^2+8x-10y+5=0 $$
:::

::: example Circle passing through the origin
**Problem.** A circle has centre $(-3,4)$ and passes through the origin. Find its equation.

**Solution.** The radius is the distance from the centre to the origin: $r=\sqrt{(-3)^2+4^2}=5$.

$$ (x+3)^2+(y-4)^2=25 \;\Rightarrow\; x^2+6x+9+y^2-8y+16=25 $$

$$ x^2+y^2+6x-8y=0 $$

Check: $(0,0)$ gives $0=0$. ✓
:::

### Circles that touch the axes

A circle of radius $r$ **touches the $x$-axis** when the distance from its centre to the axis equals $r$, i.e. $|k|=r$. It touches the $y$-axis when $|h|=r$. If it touches both axes in the first quadrant, $h=k=r$.

::: example Circle touching both axes
**Problem.** Find the equation of the circle of radius $4$ that touches both axes in the first quadrant.

**Solution.** The centre is $4$ units from each axis, so $(h,k)=(4,4)$ and $r=4$.

$$ (x-4)^2+(y-4)^2=16 \;\Rightarrow\; x^2+y^2-8x-8y+16=0 $$
:::

::: example Circle touching the $x$-axis
**Problem.** Find the equation of the circle with centre $(2,3)$ that touches the $x$-axis.

**Solution.** The distance from the centre to the $x$-axis is $|k|=3$, so $r=3$.

$$ (x-2)^2+(y-3)^2=9 \;\Rightarrow\; x^2+y^2-4x-6y+4=0 $$
:::

## 7.3 Diameter form and the general equation of a circle

### The diameter form

::: derivation Equation of a circle on the diameter $AB$
**Setting up.** Let $A(x_1,y_1)$ and $B(x_2,y_2)$ be the ends of a diameter, and $P(x,y)$ any other point on the circle.

**Step 1 — the angle in a semicircle.** The angle in a semicircle is a right angle, so $\angle APB=90^\circ$. Therefore the lines $PA$ and $PB$ are perpendicular and the product of their slopes is $-1$.

**Step 2 — slopes.**

$$ \frac{y-y_1}{x-x_1}\times\frac{y-y_2}{x-x_2}=-1 $$

**Step 3 — clear the fractions.**

$$ (y-y_1)(y-y_2)=-(x-x_1)(x-x_2) $$

**Result.**

$$ (x-x_1)(x-x_2)+(y-y_1)(y-y_2)=0 $$

**What it means.** Given only the ends of a diameter, no centre or radius is needed. (The points $A$ and $B$ themselves satisfy the equation, since one factor is zero in each product.)
:::

::: example Diameter form
**Problem.** Find the equation of the circle whose diameter has ends $(4,-1)$ and $(3,-4)$.

**Solution.**

$$ (x-4)(x-3)+(y+1)(y+4)=0 \;\Rightarrow\; x^2-7x+12+y^2+5y+4=0 $$

$$ x^2+y^2-7x+5y+16=0 $$
:::

::: example Diameter with both centre and radius
**Problem.** The ends of a diameter are $A(-2,3)$ and $B(4,-5)$. Find the equation of the circle, its centre and radius.

**Solution.** $(x+2)(x-4)+(y-3)(y+5)=0$ gives $x^2-2x-8+y^2+2y-15=0$, i.e.

$$ x^2+y^2-2x+2y-23=0 $$

Centre = midpoint of $AB=\left(\dfrac{-2+4}{2},\dfrac{3-5}{2}\right)=(1,-1)$. Radius $=\dfrac12AB=\dfrac12\sqrt{6^2+8^2}=\dfrac{10}{2}=5$.

Check: $(x-1)^2+(y+1)^2=25$ expands to $x^2+y^2-2x+2y-23=0$. ✓
:::

```figure caption="The circle on diameter $AB$ with $A(-2,3)$ and $B(4,-5)$. Every point $P$ on it sees $AB$ at a right angle."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.2, 3.6))
t = np.linspace(0, 2*np.pi, 300)
ax.plot(1+5*np.cos(t), -1+5*np.sin(t), color=ACCENT, lw=1.7)
A, B = (-2, 3), (4, -5)
ax.plot([A[0], B[0]], [A[1], B[1]], color=INK, lw=1.2)
ang = np.radians(110)
P = (1+5*np.cos(ang), -1+5*np.sin(ang))
ax.plot([A[0], P[0], B[0]], [A[1], P[1], B[1]], color=SERIES[1], lw=1.1)
for p, n, dx, dy in [(A, 'A(−2, 3)', -0.2, 0.3), (B, 'B(4, −5)', 0.2, -0.6), (P, 'P', -0.3, 0.2), ((1, -1), 'centre (1, −1)', 0.3, 0.25)]:
    ax.plot([p[0]], [p[1]], 'o', color=INK, ms=3.5)
    ax.text(p[0]+dx, p[1]+dy, n, fontsize=8.5, ha='left' if dx > 0 else 'right')
ax.axhline(0, color=MUTED, lw=0.7); ax.axvline(0, color=MUTED, lw=0.7)
ax.set_xlim(-5.8, 7.8); ax.set_ylim(-6.8, 5.6); ax.set_aspect('equal')
ax.grid(color=GRID, lw=0.5); ax.spines[['top','right']].set_visible(False)
fig.tight_layout(pad=0.4)
```

### The general equation

Expand $(x-h)^2+(y-k)^2=r^2$:

$$ x^2+y^2-2hx-2ky+(h^2+k^2-r^2)=0 $$

It has the form of an equation with $x^2$ and $y^2$ having **equal coefficients** (both $1$) and **no $xy$ term**. Write $g=-h$, $f=-k$ and $c=h^2+k^2-r^2$:

$$ x^2+y^2+2gx+2fy+c=0 $$

To find the centre and radius, complete the square:

$$ (x+g)^2+(y+f)^2=g^2+f^2-c $$

::: key General equation of a circle
$$ x^2+y^2+2gx+2fy+c=0 $$

$$ \text{centre }(-g,-f), \qquad \text{radius } r=\sqrt{g^2+f^2-c} $$

It is a real circle only if $g^2+f^2-c>0$. If this is $0$ it is a single point; if it is negative there is no real circle. If the equation has $ax^2+ay^2+\dots$, divide through by $a$ first.
:::

::: caution Half the coefficient, with the sign changed
In $x^2+y^2+6x-8y+9=0$ the coefficient of $x$ is $6=2g$, so $g=3$ and the centre has $x$-coordinate $-3$, not $+3$. The coefficient of $y$ is $-8=2f$, so $f=-4$ and the centre is $(-3,4)$. Always **halve** the coefficient, then **change the sign**.
:::

::: example Centre and radius from the general equation
**Problem.** Find the centre and radius of (a) $x^2+y^2-6x+8y-11=0$; (b) $2x^2+2y^2-4x+8y-8=0$.

**Solution.** (a) $2g=-6\Rightarrow g=-3$; $2f=8\Rightarrow f=4$; $c=-11$. Centre $=(-g,-f)=(3,-4)$. Radius $=\sqrt{9+16+11}=\sqrt{36}=6$.

(b) Divide by $2$: $x^2+y^2-2x+4y-4=0$. $g=-1$, $f=2$, $c=-4$. Centre $=(1,-2)$. Radius $=\sqrt{1+4+4}=3$.
:::

::: example An equation that is not a circle
**Problem.** Does $x^2+y^2+2x+4y+10=0$ represent a circle?

**Solution.** $g=1$, $f=2$, $c=10$. $g^2+f^2-c=1+4-10=-5<0$. The radius would be $\sqrt{-5}$, which is not real, so **no real circle** is represented.
:::

::: example Where does a circle meet the axes?
**Problem.** Find where the circle $x^2+y^2-6x-8y=0$ meets the coordinate axes.

**Solution.** Put $y=0$: $x^2-6x=0\Rightarrow x(x-6)=0$, so $x=0$ or $6$. The circle meets the $x$-axis at $(0,0)$ and $(6,0)$.

Put $x=0$: $y^2-8y=0\Rightarrow y=0$ or $8$. It meets the $y$-axis at $(0,0)$ and $(0,8)$.

The centre is $(3,4)$ and the radius is $5$.
:::

### Position of a point

For a circle $x^2+y^2+2gx+2fy+c=0$ and a point $(x_1,y_1)$, let $S_1=x_1^2+y_1^2+2gx_1+2fy_1+c$.

| Value of $S_1$ | Point is |
|---|---|
| $S_1<0$ | inside the circle |
| $S_1=0$ | on the circle |
| $S_1>0$ | outside the circle |

For $x^2+y^2-6x-8y=0$: the point $(1,1)$ gives $1+1-6-8=-12<0$, **inside**; the point $(6,8)$ gives $36+64-36-64=0$, **on** the circle; the point $(8,8)$ gives $64+64-48-64=16>0$, **outside**.

## 7.4 Circle through three points and circles under given conditions

Three points not on one line determine exactly one circle. Substitute each point into $x^2+y^2+2gx+2fy+c=0$ to get three linear equations in $g$, $f$ and $c$ and solve them.

::: example Circle through three points (general form)
**Problem.** Find the equation of the circle through $(1,1)$, $(4,4)$ and $(5,1)$.

**Solution.** Substitute each point into $x^2+y^2+2gx+2fy+c=0$:

- $(1,1)$: $2+2g+2f+c=0$ — equation (i)
- $(4,4)$: $32+8g+8f+c=0$ — equation (ii)
- $(5,1)$: $26+10g+2f+c=0$ — equation (iii)

(iii) − (i): $24+8g=0$, so $g=-3$. (ii) − (i): $30+6g+6f=0$, so $g+f=-5$ and $f=-2$. Then (i): $2-6-4+c=0$, so $c=8$.

$$ x^2+y^2-6x-4y+8=0 $$

Centre $(3,2)$, radius $\sqrt{9+4-8}=\sqrt{5}$.
:::

::: example Circle through the origin and two axis points
**Problem.** Find the circle through $(0,0)$, $(6,0)$ and $(0,8)$.

**Solution.** $(0,0)$ gives $c=0$. $(6,0)$: $36+12g=0$, $g=-3$. $(0,8)$: $64+16f=0$, $f=-4$.

$$ x^2+y^2-6x-8y=0 $$

Centre $(3,4)$, radius $5$. (The angle at the origin is $90^\circ$, so the hypotenuse from $(6,0)$ to $(0,8)$ of length $10$ is a diameter. ✓)
:::

### A shortcut: the centre is equidistant

The centre $(h,k)$ is the same distance from all three points. Setting $(h-x_1)^2+(k-y_1)^2=(h-x_2)^2+(k-y_2)^2$ gives a **linear** equation in $h$ and $k$ (the perpendicular bisector of the chord). Two such equations give the centre; then the radius is the distance to any one point.

::: example The same circle by the perpendicular-bisector method
**Problem.** Find the centre and radius of the circle through $A(1,1)$, $B(4,4)$ and $C(5,1)$, using equal distances.

**Solution.** Let the centre be $M(h,k)$. $MA=MC$: $(h-1)^2+(k-1)^2=(h-5)^2+(k-1)^2\Rightarrow-2h+1=-10h+25\Rightarrow h=3$.

$MA=MB$: $(h-1)^2+(k-1)^2=(h-4)^2+(k-4)^2\Rightarrow-2h-2k+2=-8h-8k+32\Rightarrow6h+6k=30\Rightarrow h+k=5$. With $h=3$, $k=2$.

Centre $(3,2)$; $r^2=MA^2=(3-1)^2+(2-1)^2=5$. Equation $(x-3)^2+(y-2)^2=5$. ✓ (same as above)
:::

```figure caption="The circle through $A(1,1)$, $B(4,4)$ and $C(5,1)$: centre $(3,2)$, radius $\sqrt{5}$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.2, 3.4))
t = np.linspace(0, 2*np.pi, 300)
ax.plot(3+np.sqrt(5)*np.cos(t), 2+np.sqrt(5)*np.sin(t), color=ACCENT, lw=1.7)
pts = {'A(1, 1)': (1, 1, -0.2, -0.45), 'B(4, 4)': (4, 4, 0.15, 0.1), 'C(5, 1)': (5, 1, 0.15, -0.45)}
xs = [1, 4, 5, 1]; ys = [1, 4, 1, 1]
ax.plot(xs, ys, color=MUTED, lw=0.9)
for n, (px, py, dx, dy) in pts.items():
    ax.plot([px], [py], 'o', color=INK, ms=4)
    ax.text(px+dx, py+dy, n, fontsize=8.5)
ax.plot([3], [2], 'o', color=SERIES[1], ms=4)
ax.text(3.1, 2.15, 'M(3, 2)', fontsize=8.5, color=SERIES[1])
ax.axhline(0, color=MUTED, lw=0.7); ax.axvline(0, color=MUTED, lw=0.7)
ax.set_xlim(-0.5, 6.4); ax.set_ylim(-0.6, 4.7); ax.set_aspect('equal')
ax.grid(color=GRID, lw=0.5); ax.spines[['top','right']].set_visible(False)
fig.tight_layout(pad=0.4)
```

::: example Four points on one circle (concyclic)
**Problem.** Show that $(1,1)$, $(4,4)$, $(5,1)$ and $(4,0)$ lie on one circle.

**Solution.** The circle through the first three is $x^2+y^2-6x-4y+8=0$. For $(4,0)$: $16+0-24-0+8=0$. ✓ The fourth point satisfies the equation, so the four points are **concyclic**.
:::

::: example Centre on the intersection of two lines
**Problem.** Find the circle whose centre is the point of intersection of $x+y=5$ and $x-y=1$ and which passes through the origin.

**Solution.** Adding the equations: $2x=6$, $x=3$; then $y=2$. Centre $(3,2)$. Radius$^2=3^2+2^2=13$.

$$ (x-3)^2+(y-2)^2=13 \;\Rightarrow\; x^2+y^2-6x-4y=0 $$
:::

::: example Centre on a line
**Problem.** A circle passes through $(2,0)$ and $(0,2)$ and its centre lies on the line $x=y$. Find its equation when it also passes through $(4,2)$.

**Solution.** Use the general form with the three points. $(2,0)$: $4+4g+c=0$. $(0,2)$: $4+4f+c=0$. $(4,2)$: $20+8g+4f+c=0$. The first two give $g=f$. Then $20+12g+c=0$ and $4+4g+c=0$: subtract, $16+8g=0$, so $g=-2$, $f=-2$ and $c=4$.

$$ x^2+y^2-4x-4y+4=0 $$

Centre $(2,2)$ (on $x=y$ ✓), radius $\sqrt{4+4-4}=2$.
:::

::: tip The examiner is looking for
The correct choice of form: centre–radius if the centre is known; diameter form if the ends of a diameter are given; general form with three simultaneous equations if three points are given. Marks are given for the substitutions, solving for $g,f,c$, and the final equation in the form $x^2+y^2+2gx+2fy+c=0$.
:::

## 7.5 Exercises of the SEE type

### Method for any question

1. Read what is given: centre and radius, a diameter, three points, or a condition (touching an axis, centre on a line).
2. Choose the form: $(x-h)^2+(y-k)^2=r^2$, the diameter form, or $x^2+y^2+2gx+2fy+c=0$.
3. For centre and radius from a general equation: divide so the coefficient of $x^2$ is $1$; halve the $x$ and $y$ coefficients and change signs.
4. Always expand to the form $x^2+y^2+\dots=0$ if the question says "find the equation", unless the centre–radius form is asked.
5. Check one given point in your final equation.

## Chapter summary

- Conic sections: circle (cut parallel to base), ellipse (slanted cut), parabola (cut parallel to a generator), hyperbola (cut of a double cone steeper than a generator).
- A circle is the locus of a point at a fixed distance (radius) from a fixed point (centre).
- Centre–radius form: $(x-h)^2+(y-k)^2=r^2$; with centre at the origin, $x^2+y^2=r^2$.
- Diameter form: $(x-x_1)(x-x_2)+(y-y_1)(y-y_2)=0$.
- General form: $x^2+y^2+2gx+2fy+c=0$ with centre $(-g,-f)$ and radius $\sqrt{g^2+f^2-c}$.
- It is a real circle only if $g^2+f^2-c>0$.
- A circle touches the $x$-axis if $r=|k|$, the $y$-axis if $r=|h|$; touching both in the first quadrant, $h=k=r$.
- Circle through three points: substitute into the general form and solve for $g,f,c$.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The section of a cone cut by a plane parallel to its base is a <span class="marks">[1]</span>
   (a) parabola (b) ellipse (c) circle (d) hyperbola
2. The centre of the circle $(x-3)^2+(y+4)^2=49$ is <span class="marks">[1]</span>
   (a) $(3,4)$ (b) $(-3,4)$ (c) $(3,-4)$ (d) $(-3,-4)$
3. The radius of the circle $x^2+y^2-4x+6y-12=0$ is <span class="marks">[1]</span>
   (a) 3 (b) 4 (c) 5 (d) 25
4. The equation of the circle with centre at the origin and radius 5 is <span class="marks">[1]</span>
   (a) $x^2+y^2=5$ (b) $x^2+y^2=10$ (c) $x^2+y^2=25$ (d) $x+y=25$
5. The circle $x^2+y^2-8x-8y+16=0$ touches <span class="marks">[1]</span>
   (a) only the $x$-axis (b) only the $y$-axis (c) both axes (d) neither axis

::: note Answers to Group A
**1.** (c) — a cut parallel to the base is a circle.
**2.** (c) — $(x-3)^2+(y-(-4))^2$ gives centre $(3,-4)$.
**3.** (c) — $g=-2$, $f=3$, $c=-12$: $r=\sqrt{4+9+12}=5$.
**4.** (c) — $r^2=25$.
**5.** (c) — centre $(4,4)$ and $r=\sqrt{16+16-16}=4$, so the distance to each axis equals the radius.
:::

**Group B — Short answer (2 marks each)**

1. Find the equation of the circle with centre $(0,0)$ and radius $7$. <span class="marks">[2]</span>
2. Find the centre and radius of $(x+1)^2+(y-2)^2=16$. <span class="marks">[2]</span>
3. Find the equation of the circle with centre $(1,-2)$ and radius $3$. <span class="marks">[2]</span>
4. Find the equation of the circle whose diameter has ends $(0,0)$ and $(6,8)$. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** $x^2+y^2=49$.
**2.** Centre $(-1,2)$, radius $4$.
**3.** $(x-1)^2+(y+2)^2=9\Rightarrow x^2+y^2-2x+4y-4=0$.
**4.** $(x-0)(x-6)+(y-0)(y-8)=0\Rightarrow x^2+y^2-6x-8y=0$.
:::

**Group C — Short answer (3 marks each)**

1. Find the centre and radius of $x^2+y^2+10x-4y+13=0$. <span class="marks">[3]</span>
2. Find the equation of the circle with centre $(2,-3)$ passing through $(5,1)$. <span class="marks">[3]</span>
3. Find the equation of the circle of radius $5$ that touches both axes in the first quadrant. <span class="marks">[3]</span>
4. Show that the point $(3,4)$ lies on the circle $x^2+y^2=25$ and find whether $(2,5)$ is inside or outside it. <span class="marks">[3]</span>

::: note Answers to Group C
**1.** $g=5$, $f=-2$, $c=13$. Centre $(-5,2)$. $r=\sqrt{25+4-13}=\sqrt{16}=4$.
**2.** $r^2=(5-2)^2+(1+3)^2=9+16=25$. $(x-2)^2+(y+3)^2=25\Rightarrow x^2+y^2-4x+6y-12=0$.
**3.** Centre $(5,5)$, $r=5$: $(x-5)^2+(y-5)^2=25\Rightarrow x^2+y^2-10x-10y+25=0$.
**4.** $3^2+4^2=25$, so $(3,4)$ is on the circle. For $(2,5)$: $4+25=29>25$, so it is outside.
:::

**Group D — Long answer (4 marks each)**

1. Find the equation of the circle passing through $(2,0)$, $(0,2)$ and $(4,2)$. Write down its centre and radius. <span class="marks">[4]</span>
2. Find the equation of the circle whose centre is the point of intersection of $2x+y=7$ and $x-y=-1$ and whose radius is $3$. <span class="marks">[4]</span>
3. Find the equation of the circle whose diameter has ends $(-3,2)$ and $(5,-4)$. Does it pass through the origin? <span class="marks">[4]</span>
4. Find where the circle $x^2+y^2-10x-24y=0$ meets the axes and the length of its diameter. <span class="marks">[4]</span>

::: note Answers to Group D
**1.** Using the general form (see the worked example): $x^2+y^2-4x-4y+4=0$, centre $(2,2)$, radius $2$.
**2.** Adding: $3x=6$, $x=2$; then $y=3$. Centre $(2,3)$, $r=3$. $(x-2)^2+(y-3)^2=9\Rightarrow x^2+y^2-4x-6y+4=0$.
**3.** $(x+3)(x-5)+(y-2)(y+4)=0\Rightarrow x^2-2x-15+y^2+2y-8=0\Rightarrow x^2+y^2-2x+2y-23=0$. At $(0,0)$: $-23\neq0$, so it does not pass through the origin.
**4.** $g=-5$, $f=-12$, $c=0$. Centre $(5,12)$, $r=\sqrt{25+144}=13$, diameter $26$. $y=0$: $x^2-10x=0$, $x=0,10$. $x=0$: $y^2-24y=0$, $y=0,24$. It meets the axes at $(0,0)$, $(10,0)$ and $(0,24)$.
:::

