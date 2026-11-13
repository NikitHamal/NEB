---
subject: Mathematics I
grade: BCA Semester 1
unit: 6
title: Analytical Geometry: Conic Sections
area: BCA 104 · Mathematics I · Unit 6
---

Analytical geometry describes curves by equations. The **conic sections** (circle, parabola, ellipse, hyperbola) are the curves obtained by cutting a cone with a plane. They appear in satellite dishes (parabola), planetary orbits (ellipse), GPS and radio navigation (hyperbola) and in computer graphics, where circles and ellipses are drawn pixel by pixel.

::: key What this unit gives you
- The standard equations of the circle, parabola, ellipse and hyperbola, with centre, focus, directrix, vertices and axes.
- The unified definition by **eccentricity** $e$ and the classification $e < 1$, $e = 1$, $e > 1$.
- The polar equation of a conic with a focus at the origin.
- Tangents, normals, parametric forms and focal distances; completing the square for shifted conics.
- Classifying the general second-degree equation and removing the $x y$ term by rotation; applications (dishes, bridges, orbits, navigation).
:::

## 6.1 Defining terms and the conic sections

A conic is the locus of a point $P$ whose distance from a fixed point (the **focus** $F$) is $e$ times its distance from a fixed line (the **directrix**): $PF = e \cdot PD$. The constant $e$ is the **eccentricity**.

| $e$ | Curve |
|---|---|
| $e = 0$ (limit, focus at the centre) | circle |
| $0 < e < 1$ | ellipse |
| $e = 1$ | parabola |
| $e > 1$ | hyperbola |

## 6.2 The circle

The locus of points at a fixed distance $r$ (radius) from the centre $(h, k)$:
$$(x - h)^{2} + (y - k)^{2} = r^{2}, \qquad x^{2} + y^{2} + 2 g x + 2 f y + c = 0 \ \text{(general)},$$
with centre $(-g, -f)$ and radius $\sqrt{g^{2} + f^{2} - c}$. The curve is real only if $g^{2} + f^{2} - c \ge 0$.

::: example Worked example: circle from the general form
$x^{2} + y^{2} - 4 x + 2 y - 20 = 0$: $g = -2$, $f = 1$, $c = -20$. Centre $(2, -1)$ and radius $\sqrt{4 + 1 + 20} = 5$. The equation of the circle with diameter ends $(1, 2)$ and $(5, 6)$ is $(x - 1)(x - 5) + (y - 2)(y - 6) = 0$.
:::

## 6.3 The parabola

The locus of points equidistant from the focus and the directrix ($e = 1$). The standard forms with vertex at the origin:

| Equation | Focus | Directrix | Axis | Opens |
|---|---|---|---|---|
| $y^{2} = 4 a x$ | $(a, 0)$ | $x = -a$ | $x$-axis | right |
| $y^{2} = -4 a x$ | $(-a, 0)$ | $x = a$ | $x$-axis | left |
| $x^{2} = 4 a y$ | $(0, a)$ | $y = -a$ | $y$-axis | up |
| $x^{2} = -4 a y$ | $(0, -a)$ | $y = a$ | $y$-axis | down |

The **latus rectum** (chord through the focus perpendicular to the axis) has length $4 a$. For $y^{2} = 12 x$: $4 a = 12$, $a = 3$, focus $(3, 0)$, directrix $x = -3$, latus rectum 12. With vertex $(h, k)$ replace $x, y$ by $x - h$, $y - k$. **Reflection property:** rays parallel to the axis reflect through the focus, so dishes and headlights use a parabola.

## 6.4 The ellipse

The locus of points whose distances from two foci add to the constant $2 a$. Standard form (centre at the origin, major axis along $x$, $a > b$):
$$\frac{x^{2}}{a^{2}} + \frac{y^{2}}{b^{2}} = 1, \qquad c^{2} = a^{2} - b^{2}, \qquad e = \frac{c}{a} < 1.$$
Foci $(\pm c, 0)$, vertices $(\pm a, 0)$, minor-axis ends $(0, \pm b)$, directrices $x = \pm \frac{a}{e}$, latus rectum $\frac{2 b^{2}}{a}$. If the major axis is vertical, the equation is $\frac{x^{2}}{b^{2}} + \frac{y^{2}}{a^{2}} = 1$ with $a > b$ still the semi-major axis, and the foci are $(0, \pm c)$.

```svgfig label="6.1" caption="The ellipse x^2/25 + y^2/9 = 1: a = 5, b = 3, c = 4, e = 0.8. For every point P on the curve, PF1 + PF2 = 2a = 10."
f = Fig(560, 250)
f.raw('<ellipse cx="280" cy="120" rx="150" ry="90" fill="#bbf7d0" stroke="#0f766e" stroke-width="2.2"/>')
f.line(110, 120, 450, 120, color=NAVY, sw=1.4)
f.line(280, 20, 280, 220, color=NAVY, sw=1.4)
f.circle(160, 120, 4.5, fill=RED, stroke=RED)
f.circle(400, 120, 4.5, fill=RED, stroke=RED)
f.line(160, 120, 330, 52, color=AMBER, sw=1.6)
f.line(400, 120, 330, 52, color=AMBER, sw=1.6)
f.circle(330, 52, 4.5, fill=NAVY, stroke=NAVY)
f.text(160, 140, "F1 (-4, 0)", size=11, color=RED, bold=True)
f.text(400, 140, "F2 (4, 0)", size=11, color=RED, bold=True)
f.text(344, 44, "P", size=12, color=NAVY, bold=True, anchor="start")
f.text(436, 114, "(5, 0)", size=10.5, color=NAVY, anchor="start")
f.text(280, 16, "(0, 3)", size=10.5, color=NAVY)
f.text(280, 242, "PF1 + PF2 = 2a = 10", size=11.5, color=TEAL, bold=True)
```

::: example Worked example: ellipse
$\frac{x^{2}}{25} + \frac{y^{2}}{9} = 1$: $a = 5$, $b = 3$, $c = \sqrt{25 - 9} = 4$, $e = 0.8$, foci $(\pm 4, 0)$, directrices $x = \pm \frac{5}{0.8} = \pm 6.25$, latus rectum $\frac{2 \cdot 9}{5} = 3.6$. A planet's orbit is an ellipse with the Sun at one focus; $e$ of the Earth's orbit is only about 0.017, so it is nearly circular.
:::

## 6.5 The hyperbola

The locus of points whose distances from the two foci differ by the constant $2 a$:
$$\frac{x^{2}}{a^{2}} - \frac{y^{2}}{b^{2}} = 1, \qquad c^{2} = a^{2} + b^{2}, \qquad e = \frac{c}{a} > 1.$$
Foci $(\pm c, 0)$, vertices $(\pm a, 0)$, **asymptotes** $y = \pm \frac{b}{a} x$ (the lines the branches approach), directrices $x = \pm \frac{a}{e}$, latus rectum $\frac{2 b^{2}}{a}$. A **rectangular** hyperbola has $a = b$ ($e = \sqrt{2}$); $x y = c^{2}$ is a rectangular hyperbola with the axes as asymptotes. The conjugate hyperbola is $\frac{y^{2}}{b^{2}} - \frac{x^{2}}{a^{2}} = 1$.

::: example Worked example: hyperbola
$\frac{x^{2}}{16} - \frac{y^{2}}{9} = 1$: $a = 4$, $b = 3$, $c = 5$, $e = \frac{5}{4}$, foci $(\pm 5, 0)$, vertices $(\pm 4, 0)$, asymptotes $y = \pm \frac{3}{4} x$. Navigation systems such as LORAN locate a receiver on a hyperbola because the **difference** in arrival time from two stations is fixed on such a curve.
:::

## 6.6 Conic sections in terms of eccentricity and polar equations

Taking the focus as the **pole** and the axis as the polar axis, the conic with eccentricity $e$ and semi-latus rectum $\ell$ is
$$r = \frac{\ell}{1 + e \cos \theta}.$$
For an ellipse $\ell = \frac{b^{2}}{a}$, for a parabola $\ell = 2 a$, for a hyperbola $\ell = \frac{b^{2}}{a}$. The circle of radius $R$ centred at the pole is $r = R$.

::: example Worked example: polar form of the ellipse
For $\frac{x^{2}}{25} + \frac{y^{2}}{9} = 1$: $e = 0.8$, $\ell = \frac{9}{5} = 1.8$, so $r = \frac{1.8}{1 + 0.8 \cos \theta}$. At $\theta = 0$: $r = \frac{1.8}{1.8} = 1 = a - c$ (nearest point, perihelion); at $\theta = \pi$: $r = \frac{1.8}{0.2} = 9 = a + c$ (farthest point, aphelion).
:::

**Identifying a conic from $A x^{2} + B x y + C y^{2} + \dots = 0$:** with $B = 0$, the curve is a circle if $A = C$, a parabola if $A C = 0$ (only one square term), an ellipse if $A C > 0$ and a hyperbola if $A C < 0$.

## 6.7 Tangents and normals

A **tangent** touches a conic at one point and a **normal** is the perpendicular to the tangent at that point. If $(x_{1}, y_{1})$ lies on the curve, the tangent is obtained by the **"splitting" rule**: replace $x^{2}$ by $x x_{1}$, $y^{2}$ by $y y_{1}$, $x$ by $\frac{x + x_{1}}{2}$ and $y$ by $\frac{y + y_{1}}{2}$.

| Curve | Tangent at $(x_{1}, y_{1})$ | Tangent of slope $m$ is $y = m x + c$ with |
|---|---|---|
| Circle $x^{2} + y^{2} = r^{2}$ | $x x_{1} + y y_{1} = r^{2}$ | $c^{2} = r^{2} (1 + m^{2})$ |
| Parabola $y^{2} = 4 a x$ | $y y_{1} = 2 a (x + x_{1})$ | $c = \frac{a}{m}$ |
| Ellipse $\frac{x^{2}}{a^{2}} + \frac{y^{2}}{b^{2}} = 1$ | $\frac{x x_{1}}{a^{2}} + \frac{y y_{1}}{b^{2}} = 1$ | $c^{2} = a^{2} m^{2} + b^{2}$ |
| Hyperbola $\frac{x^{2}}{a^{2}} - \frac{y^{2}}{b^{2}} = 1$ | $\frac{x x_{1}}{a^{2}} - \frac{y y_{1}}{b^{2}} = 1$ | $c^{2} = a^{2} m^{2} - b^{2}$ |

For a circle with general equation, the tangent at $(x_{1}, y_{1})$ is $x x_{1} + y y_{1} + g (x + x_{1}) + f (y + y_{1}) + c = 0$. The **length of the tangent** from an outside point $(x_{1}, y_{1})$ is $\sqrt{S_{1}}$, where $S_{1} = x_{1}^{2} + y_{1}^{2} + 2 g x_{1} + 2 f y_{1} + c$ is the left side evaluated at that point; if $S_{1} < 0$ the point is inside.

::: example Worked example: tangent and normal to a parabola
For $y^{2} = 8 x$ ($a = 2$) at $(2, 4)$ (check $16 = 8 \cdot 2$): tangent $4 y = 4 (x + 2)$, that is $y = x + 2$, slope 1. The normal has slope $-1$ through $(2, 4)$: $y - 4 = -(x - 2)$, that is $x + y = 6$. A tangent of slope 2 has $c = \frac{a}{m} = 1$, so $y = 2 x + 1$; substituting gives $(2 x + 1)^{2} = 8 x$, that is $4 x^{2} - 4 x + 1 = 0$, a perfect square, so the line touches the curve exactly once.
:::

::: example Worked example: tangent to an ellipse
$\frac{x^{2}}{25} + \frac{y^{2}}{9} = 1$ at $\left( 3, \frac{12}{5} \right)$ (check $\frac{9}{25} + \frac{144}{25 \cdot 9} = 1$): $\frac{3 x}{25} + \frac{(12/5) y}{9} = 1$, which simplifies to $9 x + 20 y = 75$. Tangents of slope $\frac{1}{2}$ have $c^{2} = \frac{25}{4} + 9 = \frac{61}{4}$, so $y = \frac{x}{2} \pm \frac{\sqrt{61}}{2}$.
:::

::: example Worked example: tangent length to a circle
For $x^{2} + y^{2} - 4 x + 2 y - 20 = 0$ and the point $(7, 1)$: $S_{1} = 49 + 1 - 28 + 2 - 20 = 4 > 0$, so the point is outside and the tangent length is $2$. (The radius is 5 and the centre is $(2, -1)$; the distance from the centre is $\sqrt{25 + 4} = 5.385$, and $\sqrt{5.385^{2} - 5^{2}} = 2$.)
:::

## 6.8 Parametric forms and focal distances

A curve can be described by a **parameter** $t$ that moves the point around it. Parametric forms are used by graphics programs to plot a conic: step $t$ and compute $(x, y)$.

| Curve | Point | Parameter |
|---|---|---|
| Circle, centre $(h, k)$ | $(h + r \cos t,\ k + r \sin t)$ | $0 \le t < 2 \pi$ |
| Parabola $y^{2} = 4 a x$ | $(a t^{2},\ 2 a t)$ | any real $t$ |
| Ellipse $\frac{x^{2}}{a^{2}} + \frac{y^{2}}{b^{2}} = 1$ | $(a \cos t,\ b \sin t)$ | $0 \le t < 2 \pi$ |
| Hyperbola $\frac{x^{2}}{a^{2}} - \frac{y^{2}}{b^{2}} = 1$ | $(a \sec t,\ b \tan t)$ | $t \ne \frac{\pi}{2}$ |

**Focal distances.** For a point $P(x, y)$ on an ellipse the distances to the foci $(\pm c, 0)$ are $PF_{1} = a + e x$ and $PF_{2} = a - e x$, whose sum is $2 a$ (the defining property). On the right branch of a hyperbola $PF_{1} = e x + a$ and $PF_{2} = e x - a$, whose difference is $2 a$.

::: example Worked example: the point $t = \frac{\pi}{3}$ on $\frac{x^{2}}{25} + \frac{y^{2}}{9} = 1$
$P = (5 \cos 60^{\circ},\ 3 \sin 60^{\circ}) = (2.5,\ 2.598)$. Direct distances: $PF_{1} = \sqrt{6.5^{2} + 2.598^{2}} = 7$ and $PF_{2} = \sqrt{1.5^{2} + 2.598^{2}} = 3$. Formula: $a + e x = 5 + 0.8 \times 2.5 = 7$ and $a - e x = 5 - 2 = 3$. The sum is $10 = 2 a$.
:::

**Focal chord of a parabola.** For $y^{2} = 4 a x$ the points $t_{1}$ and $t_{2}$ give a chord through the focus exactly when $t_{1} t_{2} = -1$. The length of the focal chord whose ends are $x_{1}$ and $x_{2}$ is $x_{1} + x_{2} + 2 a$; the shortest focal chord is the latus rectum, of length $4 a$.

## 6.9 Translation of axes and completing the square

If the centre (or vertex) of a conic is at $(h, k)$ rather than the origin, shift the axes with $X = x - h$ and $Y = y - k$. To recognise a conic given in general form, **complete the square** in $x$ and $y$ and compare with a standard equation in $X$ and $Y$.

::: example Worked example: an ellipse
$9 x^{2} + 4 y^{2} - 18 x + 16 y - 11 = 0$. Group: $9 (x^{2} - 2 x) + 4 (y^{2} + 4 y) = 11$, so $9 (x - 1)^{2} + 4 (y + 2)^{2} = 11 + 9 + 16 = 36$, that is
$$\frac{(x - 1)^{2}}{4} + \frac{(y + 2)^{2}}{9} = 1.$$
Centre $(1, -2)$. The larger denominator is under $y$, so the major axis is vertical: $a = 3$, $b = 2$, $c = \sqrt{9 - 4} = \sqrt{5}$, $e = \frac{\sqrt{5}}{3} = 0.745$. Foci $(1, -2 \pm \sqrt{5})$, vertices $(1, 1)$ and $(1, -5)$.
:::

::: example Worked example: a parabola
$y^{2} - 4 y - 8 x + 20 = 0$. Then $(y - 2)^{2} = 8 x - 16 = 8 (x - 2)$. Vertex $(2, 2)$, $4 a = 8$ so $a = 2$, opens right: focus $(4, 2)$, directrix $x = 0$, axis $y = 2$, latus rectum 8.
:::

::: example Worked example: a hyperbola
$16 x^{2} - 9 y^{2} - 64 x - 18 y - 89 = 0$. Group: $16 (x - 2)^{2} - 9 (y + 1)^{2} = 89 + 64 - 9 = 144$, so
$$\frac{(x - 2)^{2}}{9} - \frac{(y + 1)^{2}}{16} = 1.$$
Centre $(2, -1)$, $a = 3$, $b = 4$, $c = 5$, $e = \frac{5}{3}$. Foci $(7, -1)$ and $(-3, -1)$, vertices $(5, -1)$ and $(-1, -1)$, asymptotes $y + 1 = \pm \frac{4}{3} (x - 2)$.
:::

```svgfig label="6.2" caption="The parabola y^2 = 4x (a = 1). Every point is as far from the focus F(1, 0) as from the directrix x = -1 (here PF = PD = 2 at P(1, 2)). Rays parallel to the axis reflect through F, which is why a dish collects signals at its focus."
f = Fig(560, 290)
ax = Axes(f, 70, 15, 300, 245, (-2, 6.5), (-3.5, 3.5))
ax.grid(1, 1)
ax.axes("", "")
ax.curve(lambda x: 2 * math.sqrt(x), 0, 3.0, color=NAVY, sw=2.6)
ax.curve(lambda x: -2 * math.sqrt(x), 0, 3.0, color=NAVY, sw=2.6)
ax.vline(-1, -3.5, 3.5, color=RED, dash=True, sw=1.8)
for y0 in (1.0, 2.0, -3.0):
    xp = y0 * y0 / 4
    ax.hline(y0, xp, 6.3, color=AMBER, dash=False, sw=1.5)
    f.line(ax.X(xp), ax.Y(y0), ax.X(1), ax.Y(0), color=TEAL, sw=1.5)
ax.hline(2, -1, 1, color=SLATE, dash=True, sw=1.2)
ax.pt(1, 0, "F (1, 0)", color=RED, dx=9, dy=-9)
ax.pt(1, 2, "P (1, 2)", color=NAVY, dx=8, dy=-12)
ax.pt(-1, 2, "D", color=NAVY, dx=-14, dy=-8)
f.text(ax.X(-1) - 5, ax.Y(-1.5), "x = -1", size=10, color=RED, bold=True, anchor="end")
f.text(390, 110, "Incoming rays", size=10.5, color=AMBER, bold=True, anchor="start")
f.text(390, 126, "(parallel to the axis)", size=10, color=AMBER, anchor="start")
f.text(390, 160, "Reflected rays", size=10.5, color=TEAL, bold=True, anchor="start")
f.text(390, 176, "(all pass through F)", size=10, color=TEAL, anchor="start")
f.text(390, 210, "PF = PD = 2", size=11, color=NAVY, bold=True, anchor="start")
```

## 6.10 The general second-degree equation, rotation and classification

Every conic (and its degenerate cases) has an equation $A x^{2} + B x y + C y^{2} + D x + E y + F = 0$. The sign of the **discriminant** $\Delta = B^{2} - 4 A C$ tells the type.

| $\Delta = B^{2} - 4 A C$ | Non-degenerate curve | Degenerate cases |
|---|---|---|
| $\Delta < 0$ | ellipse ($B = 0$ and $A = C$: circle) | a single point, or no real points |
| $\Delta = 0$ | parabola | one line, two parallel lines, or none |
| $\Delta > 0$ | hyperbola | two intersecting lines |

A term $B x y$ means the axes of the conic are tilted. **Rotate** the axes through the angle $\theta$ with
$$\tan 2 \theta = \frac{B}{A - C}$$
(take $\theta = 45^{\circ}$ if $A = C$), using $x = X \cos \theta - Y \sin \theta$, $y = X \sin \theta + Y \cos \theta$. The new coefficients of $X^{2}$ and $Y^{2}$ are the **eigenvalues** of the matrix $\begin{pmatrix} A & B/2 \\ B/2 & C \end{pmatrix}$ (see Unit 5), and the new axes point along its eigenvectors.

::: example Worked example: $x y = 1$
$A = C = 0$, $B = 1$: $\Delta = 1 > 0$, a hyperbola. Rotate by $45^{\circ}$: $x = \frac{X - Y}{\sqrt{2}}$, $y = \frac{X + Y}{\sqrt{2}}$, so $x y = \frac{X^{2} - Y^{2}}{2} = 1$, that is $\frac{X^{2}}{2} - \frac{Y^{2}}{2} = 1$. It is a rectangular hyperbola with $a = b = \sqrt{2}$, $c = 2$, $e = \sqrt{2}$, vertices $(1, 1)$ and $(-1, -1)$ and foci $(\sqrt{2}, \sqrt{2})$ and $(-\sqrt{2}, -\sqrt{2})$. The axes $x = 0$ and $y = 0$ are its asymptotes.
:::

::: example Worked example: $x^{2} + x y + y^{2} = 3$
$\Delta = 1 - 4 = -3 < 0$: an ellipse. The matrix $\begin{pmatrix} 1 & 1/2 \\ 1/2 & 1 \end{pmatrix}$ has eigenvalues $\frac{3}{2}$ (direction $(1, 1)$) and $\frac{1}{2}$ (direction $(1, -1)$), so $\frac{3}{2} X^{2} + \frac{1}{2} Y^{2} = 3$, that is $\frac{X^{2}}{2} + \frac{Y^{2}}{6} = 1$. The semi-axes are $\sqrt{2}$ along the line $y = x$ and $\sqrt{6}$ along the line $y = -x$. Check: $(1, 1)$ satisfies $1 + 1 + 1 = 3$ and lies $\sqrt{2}$ from the origin.
:::

::: example Worked example: $x^{2} + 4 x y + y^{2} = 3$
$\Delta = 16 - 4 = 12 > 0$: a hyperbola. The eigenvalues of $\begin{pmatrix} 1 & 2 \\ 2 & 1 \end{pmatrix}$ are $3$ (direction $(1, 1)$) and $-1$ (direction $(1, -1)$), so $3 X^{2} - Y^{2} = 3$, that is $X^{2} - \frac{Y^{2}}{3} = 1$: $a = 1$, $b = \sqrt{3}$, $e = 2$. The vertices lie on $y = x$ at $\left( \pm \frac{1}{\sqrt{2}}, \pm \frac{1}{\sqrt{2}} \right)$, at distance 1 from the origin.
:::

**Degenerate conics.** $x^{2} - y^{2} = 0$ is the pair of lines $y = \pm x$ ($\Delta > 0$). $2 x^{2} + 3 x y + y^{2} = (2 x + y)(x + y) = 0$ also gives two lines ($\Delta = 9 - 8 = 1 > 0$). $x^{2} + y^{2} = 0$ is the single point $(0, 0)$. Always test for factorisation before assuming a proper conic.

## 6.11 Properties and applications of the conics

**Focus-directrix check.** For $\frac{x^{2}}{25} + \frac{y^{2}}{9} = 1$ the focus is $(4, 0)$ and the directrix $x = 6.25$. At the point $(0, 3)$: the distance to the focus is $\sqrt{16 + 9} = 5$ and to the directrix is $6.25$; the ratio $\frac{5}{6.25} = 0.8 = e$, as the definition requires.

```svgfig label="6.3" caption="The hyperbola x^2/16 - y^2/9 = 1: a = 4, b = 3, c = 5, e = 5/4. The branches approach the asymptotes y = +-3x/4, which are the diagonals of the dashed 2a by 2b rectangle. At every point |PF1 - PF2| = 2a = 8."
f = Fig(560, 330)
ax = Axes(f, 70, 15, 420, 300, (-8, 8), (-5.7, 5.7))
ax.grid(2, 2)
ax.axes("", "")
ax.curve(lambda x: 0.75 * math.sqrt(x * x - 16), 4, 8, color=NAVY, sw=2.6)
ax.curve(lambda x: -0.75 * math.sqrt(x * x - 16), 4, 8, color=NAVY, sw=2.6)
ax.curve(lambda x: 0.75 * math.sqrt(x * x - 16), -8, -4, color=NAVY, sw=2.6)
ax.curve(lambda x: -0.75 * math.sqrt(x * x - 16), -8, -4, color=NAVY, sw=2.6)
ax.curve(lambda x: 0.75 * x, -7.2, 7.2, color=AMBER, sw=1.5, dash=True)
ax.curve(lambda x: -0.75 * x, -7.2, 7.2, color=AMBER, sw=1.5, dash=True)
for (x0, y0, x1, y1) in ((-4, -3, 4, -3), (-4, 3, 4, 3), (-4, -3, -4, 3), (4, -3, 4, 3)):
    f.line(ax.X(x0), ax.Y(y0), ax.X(x1), ax.Y(y1), color=TEAL, sw=1.2, dash=True)
ax.pt(5, 0, "F2 (5, 0)", color=RED, dx=8, dy=-10)
ax.pt(-5, 0, "F1 (-5, 0)", color=RED, dx=-8, dy=-10, anchor="end")
ax.pt(4, 0, "", color=NAVY, r=3.5)
ax.pt(-4, 0, "", color=NAVY, r=3.5)
f.text(ax.X(4) - 4, ax.Y(0) - 8, "(4, 0)", size=9.5, color=NAVY, bold=True, anchor="end")
f.text(ax.X(-4) + 4, ax.Y(0) - 8, "(-4, 0)", size=9.5, color=NAVY, bold=True, anchor="start")
f.text(ax.X(0.8), ax.Y(2.1), "y = 3x/4", size=10, color=AMBER, bold=True, anchor="start")
f.text(ax.X(0.6), ax.Y(-2.85), "y = -3x/4", size=10, color=AMBER, bold=True, anchor="start")
```

**Satellite dish.** A dish is a paraboloid; its cross-section $x^{2} = 4 a y$. A dish 1.2 m across and 0.2 m deep has the rim point $(0.6, 0.2)$, so $0.36 = 4 a (0.2)$ and $a = 0.45$ m: the receiver sits 0.45 m above the vertex. Flatter dishes (smaller depth) have a larger $a$.

**Suspension-bridge cable.** A cable carrying a uniform deck hangs in a parabola. If the towers are 100 m apart and rise 20 m above the lowest point, take the vertex at the origin: $x^{2} = 4 a y$ with $(50, 20)$ gives $2500 = 80 a$, $a = 31.25$. At 25 m from the centre the height is $\frac{25^{2}}{4 \times 31.25} = 5$ m above the lowest point. (A freely hanging cable is a catenary, not a parabola, but the deck load makes it parabolic.)

**Orbits.** Planets move on ellipses with the Sun at one focus. With semi-major axis $a$ and eccentricity $e$ the nearest and farthest distances are $a (1 - e)$ and $a (1 + e)$ (the polar equation of 6.6). For Earth ($a = 1$ AU, $e = 0.0167$): $0.9833$ AU and $1.0167$ AU. For Halley's comet ($a = 17.8$ AU, $e = 0.967$): $0.587$ AU at perihelion and $35.0$ AU at aphelion, so its ellipse is very long and thin.

```svgfig label="6.4" caption="Polar graphs of r = 3 / (1 + e cos t) for e = 0, 0.5, 1 and 1.5, all with the focus at the pole (the dot) and the same semi-latus rectum 3. As e increases the curve opens from a circle to an ellipse, a parabola and one branch of a hyperbola."
f = Fig(560, 300)
ox, oy, sc = 300, 150, 16
def poly(e, t0, t1, col):
    pts = []
    n = 160
    for i in range(n + 1):
        t = t0 + (t1 - t0) * i / n
        r = 3 / (1 + e * math.cos(t))
        pts.append("%.1f,%.1f" % (ox + sc * r * math.cos(t), oy - sc * r * math.sin(t)))
    f.raw('<polyline points="' + " ".join(pts) + '" fill="none" stroke="' + col + '" stroke-width="2.4"/>')
f.line(30, oy, 540, oy, color=SLATE, sw=1.0)
f.line(ox, 12, ox, 288, color=SLATE, sw=1.0)
poly(0, 0, 2 * math.pi, SLATE)
poly(0.5, 0, 2 * math.pi, TEAL)
poly(1, -2.3, 2.3, AMBER)
poly(1.5, -2.03, 2.03, RED)
f.circle(ox, oy, 4, fill=NAVY, stroke=NAVY)
f.text(30, 24, "e = 0 circle (r = 3)", size=10.5, color=SLATE, bold=True, anchor="start")
f.text(30, 42, "e = 0.5 ellipse", size=10.5, color=TEAL, bold=True, anchor="start")
f.text(30, 60, "e = 1 parabola", size=10.5, color=AMBER, bold=True, anchor="start")
f.text(30, 78, "e = 1.5 hyperbola", size=10.5, color=RED, bold=True, anchor="start")
f.text(30, 96, "dot = pole (the focus)", size=10.5, color=NAVY, bold=True, anchor="start")
```

**Navigation (LORAN-type hyperbolas).** Two radio stations 10 km apart ($c = 5$) send pulses together. A receiver that hears one pulse 8 km of travel later than the other lies on the hyperbola with $2 a = 8$, that is $a = 4$, $b = 3$: the hyperbola of Fig 6.3. A third station gives a second hyperbola and the receiver lies where they cross.

**Whispering gallery.** Sound or light from one focus of an ellipse reflects to the other focus, because the tangent makes equal angles with the two focal lines. Elliptical reflectors are used in dental lamps and in lithotripsy, which concentrates shock waves on a kidney stone at the second focus.

**Computer graphics.** A circle has eight-fold symmetry, so a pixel algorithm computes one octant and mirrors the point $(x, y)$ to $(\pm x, \pm y)$ and $(\pm y, \pm x)$. An ellipse has four-fold symmetry and is drawn from $(a \cos t, b \sin t)$ with small steps of $t$. Parabolas also describe the motion of a projectile (a game object under gravity) and Bézier curves of degree 2.

## Formula and fact sheet

- Circle $(x - h)^{2} + (y - k)^{2} = r^{2}$. Parabola $y^{2} = 4 a x$: focus $(a, 0)$, directrix $x = -a$.
- Ellipse $\frac{x^{2}}{a^{2}} + \frac{y^{2}}{b^{2}} = 1$: $c^{2} = a^{2} - b^{2}$, $e = \frac{c}{a}$. Hyperbola $\frac{x^{2}}{a^{2}} - \frac{y^{2}}{b^{2}} = 1$: $c^{2} = a^{2} + b^{2}$, asymptotes $y = \pm \frac{b}{a} x$.
- Tangent (splitting rule): parabola $y y_{1} = 2 a (x + x_{1})$, ellipse $\frac{x x_{1}}{a^{2}} + \frac{y y_{1}}{b^{2}} = 1$; slope form $c = \frac{a}{m}$ (parabola), $c^{2} = a^{2} m^{2} \pm b^{2}$ (ellipse $+$, hyperbola $-$).
- General conic: $\Delta = B^{2} - 4 A C$ is negative for an ellipse, zero for a parabola, positive for a hyperbola; rotate by $\tan 2 \theta = \frac{B}{A - C}$.
- Focal distances of the ellipse: $a \pm e x$; nearest and farthest orbit distances $a (1 \mp e)$.
- Polar: $r = \frac{\ell}{1 + e \cos \theta}$; $e = 0$ circle, $e < 1$ ellipse, $e = 1$ parabola, $e > 1$ hyperbola.

## Chapter summary

- Every conic is defined by a focus, a directrix and the eccentricity $e$.
- Reading $a$, $b$, $c$ from the standard equation gives the foci, vertices, directrices, eccentricity and asymptotes.
- In polar form with a focus at the pole, one equation describes all four curves.
- Tangents follow the splitting rule; completing the square handles shifted conics; the sign of $B^{2} - 4 A C$ classifies any second-degree curve, and a rotation removes the $x y$ term.

## Practice

1. Find the centre and radius of $x^{2} + y^{2} + 6 x - 8 y = 0$.
2. For $y^{2} = 16 x$ find the focus, directrix and length of the latus rectum.
3. Find the equation of the parabola with focus $(0, -2)$ and vertex at the origin.
4. For $9 x^{2} + 16 y^{2} = 144$ find $a$, $b$, $e$ and the foci.
5. For $\frac{x^{2}}{9} - \frac{y^{2}}{16} = 1$ find $e$, the foci and the asymptotes.
6. Name the conic $r = \frac{4}{1 + \cos \theta}$ and find its focus-to-vertex distance.
7. Find the equation of the ellipse with foci $(\pm 3, 0)$ and $e = \frac{3}{5}$.
8. Show that $x^{2} + y^{2} - 2 x + 4 y + 6 = 0$ is not a real circle.
9. Find the tangent and the normal to $y^{2} = 12 x$ at $(3, 6)$.
10. Find the tangent to $\frac{x^{2}}{16} + \frac{y^{2}}{9} = 1$ at the point with $x = 2$, $y > 0$.
11. Find the length of the tangent from $(5, 4)$ to $x^{2} + y^{2} - 2 x - 4 y - 4 = 0$.
12. For what values of $c$ is $y = x + c$ a tangent to $\frac{x^{2}}{9} + \frac{y^{2}}{4} = 1$?
13. Find the focal distances $PF_{1}$ and $PF_{2}$ of $P \left( 3, \frac{12}{5} \right)$ on $\frac{x^{2}}{25} + \frac{y^{2}}{9} = 1$ and verify that they add to $2 a$.
14. Reduce $4 x^{2} + y^{2} - 8 x + 4 y - 8 = 0$ to standard form and give the centre, $a$, $b$, $e$ and the foci.
15. Reduce $x^{2} - 4 y^{2} - 6 x - 8 y - 11 = 0$ and give the centre, vertices, foci and asymptotes.
16. Classify (a) $3 x^{2} + 2 x y + 3 y^{2} - 8 = 0$, (b) $x^{2} - 2 x y + y^{2} - 4 x = 0$, (c) $x^{2} + 3 x y - y^{2} = 5$; reduce (a) to standard form by rotation.
17. For the rectangular hyperbola $x y = 8$ find $a$, the vertices and the foci.
18. A dish 2 m across and 0.25 m deep: where is the focus?
19. A satellite has perigee 6,800 km and apogee 7,200 km (distances from the centre of the Earth). Find $a$, $e$ and the semi-latus rectum $\ell$ of its orbit.
20. Two bridge towers are 120 m apart and rise 30 m above the lowest point of the cable. Find the parabola and the cable height 40 m from the centre.
21. Two radio stations are 20 km apart and a receiver is 12 km farther from one than from the other. Write the equation of the hyperbola on which it lies (centre at the midpoint, stations on the $x$-axis).
22. Prove that the chord of $y^{2} = 4 a x$ joining the points with parameters $t_{1}$ and $t_{2}$ passes through the focus if and only if $t_{1} t_{2} = -1$.
23. Find the tangents of slope 1 to $\frac{x^{2}}{16} - \frac{y^{2}}{9} = 1$.
24. Identify the conic $r = \frac{6}{2 + \cos \theta}$ and find its perihelion and aphelion distances.

::: note Answers and worked solutions
**1.** $g = 3$, $f = -4$, $c = 0$: centre $(-3, 4)$, radius $\sqrt{9 + 16} = $ **5**.

**2.** $4 a = 16$, $a = 4$: focus **$(4, 0)$**, directrix **$x = -4$**, latus rectum **16**.

**3.** Opens downward, $a = 2$: **$x^{2} = -8 y$**.

**4.** $\frac{x^{2}}{16} + \frac{y^{2}}{9} = 1$: $a = 4$, $b = 3$, $c = \sqrt{7}$, **$e = \frac{\sqrt{7}}{4} \approx 0.661$**, foci $(\pm \sqrt{7}, 0)$.

**5.** $a = 3$, $b = 4$, $c = 5$: **$e = \frac{5}{3}$**, foci $(\pm 5, 0)$, asymptotes **$y = \pm \frac{4}{3} x$**.

**6.** $e = 1$: a **parabola**; at $\theta = 0$, $r = 2$ (the vertex is 2 units from the focus), and $\ell = 4 = 2 a$ gives $a = 2$.

**7.** $c = 3$, $e = \frac{c}{a} = \frac{3}{5} \Rightarrow a = 5$, $b^{2} = 25 - 9 = 16$: **$\frac{x^{2}}{25} + \frac{y^{2}}{16} = 1$**.

**8.** $g = -1$, $f = 2$, $c = 6$: $g^{2} + f^{2} - c = 1 + 4 - 6 = -1 < 0$, so the radius would be imaginary; there is **no real circle**.

**9.** $a = 3$: tangent $6 y = 6 (x + 3)$, that is **$y = x + 3$**. The normal has slope $-1$: $y - 6 = -(x - 3)$, that is **$x + y = 9$**.

**10.** $\frac{4}{16} + \frac{y^{2}}{9} = 1 \Rightarrow y = \frac{3 \sqrt{3}}{2}$. The tangent $\frac{2 x}{16} + \frac{y_{1}\, y}{9} = 1$ becomes $\frac{x}{8} + \frac{\sqrt{3}\, y}{6} = 1$, that is **$3 x + 4 \sqrt{3}\, y = 24$**.

**11.** $S_{1} = 25 + 16 - 10 - 16 - 4 = 11 > 0$, so the length is **$\sqrt{11} = 3.317$**.

**12.** $c^{2} = a^{2} m^{2} + b^{2} = 9 + 4 = 13$, so **$c = \pm \sqrt{13}$**.

**13.** $e = 0.8$, so $PF_{1} = 5 + 0.8 \times 3 = $ **7.4** and $PF_{2} = 5 - 2.4 = $ **2.6**; the sum is $10 = 2 a$.

**14.** $4 (x - 1)^{2} + (y + 2)^{2} = 8 + 4 + 4 = 16$, so $\frac{(x - 1)^{2}}{4} + \frac{(y + 2)^{2}}{16} = 1$: centre **$(1, -2)$**, vertical major axis, $a = 4$, $b = 2$, $c = \sqrt{12} = 2 \sqrt{3}$, $e = \frac{\sqrt{3}}{2}$, foci **$(1, -2 \pm 2 \sqrt{3})$**.

**15.** $(x - 3)^{2} - 4 (y + 1)^{2} = 11 + 9 - 4 = 16$, so $\frac{(x - 3)^{2}}{16} - \frac{(y + 1)^{2}}{4} = 1$: centre **$(3, -1)$**, $a = 4$, $b = 2$, $c = 2 \sqrt{5}$; vertices **$(7, -1)$ and $(-1, -1)$**; foci **$(3 \pm 2 \sqrt{5}, -1)$**; asymptotes **$y + 1 = \pm \frac{1}{2} (x - 3)$**.

**16.** (a) $\Delta = 4 - 36 = -32 < 0$: **ellipse**. The matrix $\begin{pmatrix} 3 & 1 \\ 1 & 3 \end{pmatrix}$ has eigenvalues 4 and 2, so $4 X^{2} + 2 Y^{2} = 8$, that is $\frac{X^{2}}{2} + \frac{Y^{2}}{4} = 1$ (rotation $45^{\circ}$). (b) $\Delta = 4 - 4 = 0$: **parabola** (the quadratic part is $(x - y)^{2}$). (c) $\Delta = 9 + 4 = 13 > 0$: **hyperbola**.

**17.** For $x y = k$ the rotated form is $\frac{X^{2}}{2 k} - \frac{Y^{2}}{2 k} = 1$; with $k = 8$, $a^{2} = 16$, so **$a = 4$**. Vertices $(2 \sqrt{2}, 2 \sqrt{2})$ and $(-2 \sqrt{2}, -2 \sqrt{2})$; $c = a \sqrt{2} = 4 \sqrt{2}$, so the foci are **$(4, 4)$ and $(-4, -4)$**.

**18.** $x^{2} = 4 a y$ through $(1, 0.25)$: $1 = a$, so the focus is **1 m above the vertex**.

**19.** $2 a = 6800 + 7200$, so **$a = 7000$ km**; $c = 200$ km, so **$e = \frac{200}{7000} = 0.0286$**; $\ell = a (1 - e^{2}) = 7000 \left( 1 - \frac{1}{1225} \right) = $ **6994.3 km**.

**20.** $x^{2} = 4 a y$ through $(60, 30)$: $3600 = 120 a$, $a = 30$, so **$x^{2} = 120 y$**. At $x = 40$: $y = \frac{1600}{120} = $ **13.3 m** above the lowest point.

**21.** $2 c = 20$ and $2 a = 12$ give $c = 10$, $a = 6$, $b^{2} = 100 - 36 = 64$: **$\frac{x^{2}}{36} - \frac{y^{2}}{64} = 1$**.

**22.** The chord through $(a t_{1}^{2}, 2 a t_{1})$ and $(a t_{2}^{2}, 2 a t_{2})$ has slope $\frac{2 a (t_{2} - t_{1})}{a (t_{2}^{2} - t_{1}^{2})} = \frac{2}{t_{1} + t_{2}}$, so its line is $y - 2 a t_{1} = \frac{2}{t_{1} + t_{2}} (x - a t_{1}^{2})$. The focus $(a, 0)$ lies on it when $- 2 a t_{1} (t_{1} + t_{2}) = 2 (a - a t_{1}^{2})$, that is $- t_{1}^{2} - t_{1} t_{2} = 1 - t_{1}^{2}$, which gives **$t_{1} t_{2} = -1$**. Every step reverses, so the condition is also sufficient.

**23.** $c^{2} = a^{2} m^{2} - b^{2} = 16 - 9 = 7$, so the tangents are **$y = x + \sqrt{7}$ and $y = x - \sqrt{7}$**.

**24.** Divide by 2: $r = \frac{3}{1 + \frac{1}{2} \cos \theta}$, so $e = \frac{1}{2}$ and $\ell = 3$: an **ellipse**. Perihelion $r(0) = \frac{6}{3} = $ **2**, aphelion $r(\pi) = \frac{6}{1} = $ **6**. Check: $a = \frac{2 + 6}{2} = 4$ and $a (1 - e) = 2$, $a (1 + e) = 6$.
:::
