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

## Formula and fact sheet

- Circle $(x - h)^{2} + (y - k)^{2} = r^{2}$. Parabola $y^{2} = 4 a x$: focus $(a, 0)$, directrix $x = -a$.
- Ellipse $\frac{x^{2}}{a^{2}} + \frac{y^{2}}{b^{2}} = 1$: $c^{2} = a^{2} - b^{2}$, $e = \frac{c}{a}$. Hyperbola $\frac{x^{2}}{a^{2}} - \frac{y^{2}}{b^{2}} = 1$: $c^{2} = a^{2} + b^{2}$, asymptotes $y = \pm \frac{b}{a} x$.
- Polar: $r = \frac{\ell}{1 + e \cos \theta}$; $e = 0$ circle, $e < 1$ ellipse, $e = 1$ parabola, $e > 1$ hyperbola.

## Chapter summary

- Every conic is defined by a focus, a directrix and the eccentricity $e$.
- Reading $a$, $b$, $c$ from the standard equation gives the foci, vertices, directrices, eccentricity and asymptotes.
- In polar form with a focus at the pole, one equation describes all four curves.

## Practice

1. Find the centre and radius of $x^{2} + y^{2} + 6 x - 8 y = 0$.
2. For $y^{2} = 16 x$ find the focus, directrix and length of the latus rectum.
3. Find the equation of the parabola with focus $(0, -2)$ and vertex at the origin.
4. For $9 x^{2} + 16 y^{2} = 144$ find $a$, $b$, $e$ and the foci.
5. For $\frac{x^{2}}{9} - \frac{y^{2}}{16} = 1$ find $e$, the foci and the asymptotes.
6. Name the conic $r = \frac{4}{1 + \cos \theta}$ and find its focus-to-vertex distance.
7. Find the equation of the ellipse with foci $(\pm 3, 0)$ and $e = \frac{3}{5}$.
8. Show that $x^{2} + y^{2} - 2 x + 4 y + 6 = 0$ is not a real circle.

::: note Answers and worked solutions
**1.** $g = 3$, $f = -4$, $c = 0$: centre $(-3, 4)$, radius $\sqrt{9 + 16} = $ **5**.

**2.** $4 a = 16$, $a = 4$: focus **$(4, 0)$**, directrix **$x = -4$**, latus rectum **16**.

**3.** Opens downward, $a = 2$: **$x^{2} = -8 y$**.

**4.** $\frac{x^{2}}{16} + \frac{y^{2}}{9} = 1$: $a = 4$, $b = 3$, $c = \sqrt{7}$, **$e = \frac{\sqrt{7}}{4} \approx 0.661$**, foci $(\pm \sqrt{7}, 0)$.

**5.** $a = 3$, $b = 4$, $c = 5$: **$e = \frac{5}{3}$**, foci $(\pm 5, 0)$, asymptotes **$y = \pm \frac{4}{3} x$**.

**6.** $e = 1$: a **parabola**; at $\theta = 0$, $r = 2$ (the vertex is 2 units from the focus), and $\ell = 4 = 2 a$ gives $a = 2$.

**7.** $c = 3$, $e = \frac{c}{a} = \frac{3}{5} \Rightarrow a = 5$, $b^{2} = 25 - 9 = 16$: **$\frac{x^{2}}{25} + \frac{y^{2}}{16} = 1$**.

**8.** $g = -1$, $f = 2$, $c = 6$: $g^{2} + f^{2} - c = 1 + 4 - 6 = -1 < 0$, so the radius would be imaginary; there is **no real circle**.
:::
