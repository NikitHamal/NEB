---
subject: Mathematics
grade: BCA
unit: 10
title: Circle and Conic Sections
hours: 3
area: Coordinate Geometry
---

Conics carry about three questions: the centre or radius of a circle, the focus or latus rectum of a parabola, and the eccentricity or axis of an ellipse or hyperbola. Everything is a substitution into a standard form; the work is recognising which form you have.

::: key What the paper asks from this chapter
- **Circle**: $(x-h)^2+(y-k)^2=r^2$, general form, tangent conditions.
- **Parabola** $y^2=4ax$: focus, directrix, latus rectum.
- **Ellipse** and **hyperbola**: axes, foci, eccentricity, asymptotes.
- **Eccentricity**: circle 0, ellipse < 1, parabola 1, hyperbola > 1.
:::

## 10.1 Circle: equation, centre, radius, tangent

- Centre $(h,k)$, radius $r$: $(x-h)^2+(y-k)^2=r^2$. Centre at the origin: $x^2+y^2=r^2$.
- General form $x^2+y^2+2gx+2fy+c=0$: centre $(-g,-f)$, radius $\sqrt{g^2+f^2-c}$. It passes through the origin when $c=0$.
- A line touches a circle when the distance from the centre to the line equals $r$.
- Tangent at $(x_1,y_1)$ to $x^2+y^2=r^2$: $xx_1+yy_1=r^2$. Length of tangent from an outside point $=\sqrt{x_1^2+y_1^2-r^2}$.
- A point is inside, on or outside according as $x_1^2+y_1^2-r^2$ is negative, zero or positive.

```photogrid label="10.1" cols="3" ratio="1.0" caption="The people behind the conics. (a) A page of Apollonius of Perga's Conica (about 200 BC), the first book to name the parabola, ellipse and hyperbola. (b) Johannes Kepler (1571-1630), who showed that planets move on ellipses with the Sun at one focus. (c) A parabolic dish: every incoming ray is sent to the single focus, which is why satellite dishes and torch reflectors are parabolas."
@ photo id="bcamath/apollonius" cap="Apollonius, Conica (printed edition)"
focus 0.5 0.4
@ photo id="bcamath/kepler" cap="Kepler: planets move on ellipses"
focus 0.5 0.3
@ photo id="bca104/dish" cap="Parabolic dish: all rays to the focus"
focus 0.5 0.45
```

```svgfig label="10.1" caption="A circle from its general equation, computed. x^2 + y^2 - 6x + 4y - 12 = 0 has g = -3, f = 2, so centre (3, -2) and radius sqrt(9 + 4 + 12) = 5. The point (6, 2) lies on it, and the tangent there is perpendicular to the radius: slope -3/4, equation 3x + 4y - 26 = 0, whose distance from the centre is exactly 5. From the outside point (3, 6) the tangent length is sqrt(64 - 25) = sqrt(39) = 6.24."
import math
g, ff, c = -3, 2, -12; cx0, cy0 = -g, -ff; r = math.sqrt(g * g + ff * ff - c)
assert (cx0, cy0, r) == (3, -2, 5.0) and (6 - 3) ** 2 + (2 + 2) ** 2 == 25
d = abs(3 * 3 + 4 * -2 - 26) / 5; assert d == 5.0 and (4 / 3) * (-3 / 4) == -1.0
S1 = 3 ** 2 + 6 ** 2 - 6 * 3 + 4 * 6 - 12; assert S1 == 39 and round(math.sqrt(S1), 2) == 6.24 and (6 - cy0) ** 2 + 0 == 64
f = Fig(780, 330)
ax = Axes(f, 30, 14, 330, 300, (-3, 9), (-8, 8) if False else (-8, 8))
ax.grid(2, 2, size=10); ax.axes("x", "y")
pxs = ax.X(9) - ax.X(8)
f.raw('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#dbeafe" fill-opacity="0.5" stroke="%s" stroke-width="2.4"/>' % (ax.X(3), ax.Y(-2), 5 * pxs, NAVY))
ax.curve(lambda x: (26 - 3 * x) / 4, 0, 9, color=RED, sw=2)
f.line(ax.X(3), ax.Y(-2), ax.X(6), ax.Y(2), color=TEAL, sw=1.8, dash=True)
ax.pt(3, -2, "centre (3, -2)", r=4.5, color=NAVY, dx=8, dy=16); ax.pt(6, 2, "(6, 2)", r=5, color=RED, dx=-10, dy=-10, anchor="end"); ax.pt(3, 6, "(3, 6)", r=5, color=AMBER, dx=8, dy=-8)
f.text(ax.X(7.5), ax.Y(-0.3), "r = 5", size=11, color=TEAL, bold=True)
f.text(560, 30, "From the general equation", size=11.5, color=NAVY, bold=True)
for j, (t, col) in enumerate([("x^2 + y^2 + 2gx + 2fy + c = 0", NAVY), ("g = -3, f = 2, c = -12", SLATE), ("centre (-g, -f) = (3, -2)", SLATE), ("radius sqrt(g^2 + f^2 - c) = sqrt(25) = 5", TEAL), ("tangent at (6, 2): 3x + 4y - 26 = 0", SLATE), ("distance from centre = 25/5 = 5 = r", TEAL), ("(3, 6): S1 = 9 + 36 - 18 + 24 - 12 = 39", SLATE), ("tangent length = sqrt(S1) = 6.24", RED), ("S1 > 0 outside, = 0 on, < 0 inside", RED)]):
    f.text(400, 64 + j * 28, t, size=10, color=col, anchor="start", bold=(col in (NAVY, RED)))
```

## 10.2 Parabola, ellipse and hyperbola in standard form

| Conic | Equation | Key facts |
|---|---|---|
| Parabola | $y^2=4ax$ | vertex $(0,0)$, focus $(a,0)$, directrix $x=-a$, latus rectum $4a$, $e=1$ |
| Parabola | $x^2=4ay$ | opens upward, focus $(0,a)$ |
| Ellipse ($a>b$) | $\frac{x^2}{a^2}+\frac{y^2}{b^2}=1$ | $e=\sqrt{1-\frac{b^2}{a^2}}$, foci $(\pm ae,0)$, major axis $2a$, latus rectum $\frac{2b^2}{a}$, area $\pi ab$ |
| Hyperbola | $\frac{x^2}{a^2}-\frac{y^2}{b^2}=1$ | $e=\sqrt{1+\frac{b^2}{a^2}}$, foci $(\pm ae,0)$, asymptotes $y=\pm\frac{b}{a}x$ |
| Rect. hyperbola | $xy=c^2$ or $x^2-y^2=a^2$ | asymptotes at right angles |

For an ellipse the larger denominator belongs to the major axis, so $\frac{x^2}{16}+\frac{y^2}{25}=1$ has its major axis along the $y$-axis. Distance between the foci $=2ae$.

```svgfig label="10.2" caption="The three standard conics with their numbers computed. (a) Parabola y^2 = 8x: a = 2, focus (2, 0), directrix x = -2, latus rectum 4a = 8. (b) Ellipse x^2/25 + y^2/9 = 1: a = 5, b = 3, c = sqrt(25 - 9) = 4, e = 4/5 = 0.8, foci (+-4, 0). (c) Hyperbola x^2/16 - y^2/9 = 1: a = 4, b = 3, c = sqrt(16 + 9) = 5, e = 5/4 = 1.25, asymptotes y = +-(3/4)x."
import math
a = 2; assert 4 * a == 8
A, B = 5, 3; Cc = math.sqrt(A * A - B * B); e1 = Cc / A; assert (Cc, e1) == (4.0, 0.8) and 2 * B * B / A == 3.6
a2, b2 = 4, 3; c2 = math.sqrt(a2 * a2 + b2 * b2); e2 = c2 / a2; assert (c2, e2) == (5.0, 1.25)
for x in (4, 6, 8): assert abs(x * x / 16 - (b2 * math.sqrt(x * x / 16 - 1)) ** 2 / 9 - 1) < 1e-9
f = Fig(780, 330)
def panel(i, title):
    cx = 10 + i * 258
    f.box(cx, 6, 250, 318, "", fill=SOFT, stroke="#cbd5e1", r=4); f.text(cx + 125, 24, title, size=11, color=NAVY, bold=True); return cx
cx = panel(0, "y^2 = 8x")
ax = Axes(f, cx + 18, 36, 214, 214, (-4, 8), (-8, 8)); ax.grid(2, 2, labels=False); ax.axes("", "")
ax.curve(lambda x: math.sqrt(8 * x), 0, 8, color=NAVY, sw=2.5); ax.curve(lambda x: -math.sqrt(8 * x), 0, 8, color=NAVY, sw=2.5)
ax.vline(-2, color=RED); ax.pt(2, 0, "F (2, 0)", r=4.5, color=TEAL, dx=4, dy=-10, size=10)
f.text(cx + 125, 268, "focus (2, 0), directrix x = -2", size=10, color=SLATE, bold=True); f.text(cx + 125, 288, "latus rectum 4a = 8,  e = 1", size=10, color=NAVY, bold=True); f.text(cx + 125, 308, "ax^2 type: opens right", size=10, color=SLATE)
cx = panel(1, "x^2/25 + y^2/9 = 1")
ax = Axes(f, cx + 18, 36, 214, 214, (-6, 6), (-6, 6)); ax.grid(2, 2, labels=False); ax.axes("", "")
ax.curve(lambda x: 3 * math.sqrt(max(0, 1 - x * x / 25)), -5, 5, color=NAVY, sw=2.5); ax.curve(lambda x: -3 * math.sqrt(max(0, 1 - x * x / 25)), -5, 5, color=NAVY, sw=2.5)
ax.pt(4, 0, "F2", r=4.5, color=TEAL, dx=3, dy=-8, size=10); ax.pt(-4, 0, "F1", r=4.5, color=TEAL, dx=-3, dy=-8, size=10, anchor="end")
f.text(cx + 125, 268, "a = 5, b = 3, c = 4, foci (+-4, 0)", size=10, color=SLATE, bold=True); f.text(cx + 125, 288, "e = c/a = 0.8 (less than 1)", size=10, color=NAVY, bold=True); f.text(cx + 125, 308, "sum of focal distances = 2a = 10", size=10, color=SLATE)
cx = panel(2, "x^2/16 - y^2/9 = 1")
ax = Axes(f, cx + 18, 36, 214, 214, (-9, 9), (-9, 9)); ax.grid(3, 3, labels=False); ax.axes("", "")
for sg in (1, -1):
    ax.curve(lambda x, sg=sg: sg * 3 * math.sqrt(max(0, x * x / 16 - 1)), 4, 9, color=NAVY, sw=2.5); ax.curve(lambda x, sg=sg: sg * 3 * math.sqrt(max(0, x * x / 16 - 1)), -9, -4, color=NAVY, sw=2.5)
ax.curve(lambda x: 0.75 * x, -9, 9, color=AMBER, sw=1.2, dash=True); ax.curve(lambda x: -0.75 * x, -9, 9, color=AMBER, sw=1.2, dash=True)
ax.pt(5, 0, "F2", r=4.5, color=TEAL, dx=3, dy=14, size=10); ax.pt(-5, 0, "F1", r=4.5, color=TEAL, dx=-3, dy=14, size=10, anchor="end")
f.text(cx + 125, 268, "a = 4, b = 3, c = 5, foci (+-5, 0)", size=10, color=SLATE, bold=True); f.text(cx + 125, 288, "e = 5/4 = 1.25 (more than 1)", size=10, color=NAVY, bold=True); f.text(cx + 125, 308, "asymptotes y = +-(3/4)x (dashed)", size=10, color=AMBER, bold=True)
```

```svgfig label="10.3" caption="Eccentricity classifies every conic. e = 0 is a circle, 0 < e < 1 an ellipse, e = 1 a parabola and e > 1 a hyperbola. The scale shows the conics computed above: the circle of radius 5 (e = 0), the ellipse (0.8), the parabola (1) and the hyperbola (1.25). Right: the same curves arise when a plane slices a cone at steeper and steeper angles."
import math
es = [("circle", 0.0), ("ellipse", math.sqrt(25 - 9) / 5), ("parabola", 1.0), ("hyperbola", math.sqrt(16 + 9) / 4)]
assert [round(e, 2) for _, e in es] == [0.0, 0.8, 1.0, 1.25]
f = Fig(780, 300)
X = lambda e: 40 + e * 260
f.line(X(0), 150, X(1.6), 150, color=SLATE, sw=2)
for v in (0, 0.4, 0.8, 1.0, 1.2, 1.6): f.line(X(v), 144, X(v), 156, color=SLATE, sw=1.4); f.text(X(v), 172, "%g" % v, size=10.5, color=SLATE, bold=True)
f.box(X(0), 138, X(1) - X(0), 8, "", fill="#bbf7d0", stroke="#bbf7d0"); f.box(X(1), 138, X(1.6) - X(1), 8, "", fill="#fecaca", stroke="#fecaca")
for i, (nm, e) in enumerate(es):
    y = [90, 212, 90, 246][i]
    f.line(X(e), 150, X(e), y + (14 if y < 150 else -14), color=TEAL, sw=1.2); f.circle(X(e), 150, 5, fill=RED, stroke=RED)
    f.text(X(e) + (40 if i == 0 else 0), y, "%s: e = %g" % (nm, round(e, 2)), size=10, color=NAVY, bold=True, anchor=("start" if i == 0 else "middle"))
f.text(170, 40, "e = c / a  (distance to focus / distance to centre)", size=11, color=NAVY, bold=True)
f.text(170, 270, "ellipse: e < 1,  parabola: e = 1,  hyperbola: e > 1", size=10.5, color=SLATE)
f.text(590, 30, "Slicing a cone", size=11.5, color=NAVY, bold=True)
f.poly([(590, 60), (540, 250), (640, 250)], fill="#e0f2fe", stroke=NAVY, sw=1.6)
f.line(530, 200, 650, 200, color=RED, sw=2); f.text(690, 204, "circle", size=10.5, color=RED, bold=True)
f.line(530, 215, 650, 170, color=TEAL, sw=2); f.text(690, 172, "ellipse", size=10.5, color=TEAL, bold=True)
f.line(560, 90, 640, 250, color=AMBER, sw=2); f.text(690, 128, "parabola", size=10.5, color=AMBER, bold=True)
f.line(600, 70, 600, 250, color=NAVY, sw=2); f.text(690, 98, "hyperbola", size=10.5, color=NAVY, bold=True)
```

## 10.3 Eight traps in circles and conics

Conic questions come from a small set of formulas, and the hardest part is knowing which letters mean what. These eight traps are drawn from the model questions on circles, parabolas, ellipses and hyperbolas.

1. **The centre in $(x-h)^2+(y-k)^2=r^2$ is $(h,k)$; in the general form it is $(-g,-f)$.** For $(x-3)^2+(y+2)^2=25$ the centre is $(3,-2)$, so the sign inside the bracket is opposite to the coordinate. For $x^2+y^2-6x+4y-12=0$ we have $g=-3$, $f=2$, centre $(3,-2)$, radius $\sqrt{9+4+12}=5$ (Fig 10.1). The radius squared must be positive, or there is no real circle.
2. **Test a point by comparing distances.** Compute $S_1=x_1^2+y_1^2+2gx_1+2fy_1+c$ for the point: negative means inside, zero means on the circle and positive means outside. The tangent length from an outside point is $\sqrt{S_1}$. For $(3,6)$ that is $\sqrt{39}=6.24$.
3. **A tangent is perpendicular to the radius.** A line touches a circle when its distance from the centre equals $r$. The tangent at $(x_1,y_1)$ on $x^2+y^2=r^2$ is $xx_1+yy_1=r^2$. If the radius slope is $\frac43$ the tangent slope is $-\frac34$.
4. **Use the diameter form when two end points are given.** The circle with diameter ends $(x_1,y_1)$ and $(x_2,y_2)$ is $(x-x_1)(x-x_2)+(y-y_1)(y-y_2)=0$. This is faster than finding the centre and radius separately. A circle through the origin has $c=0$.
5. **Parabola $y^2=4ax$ has focus $(a,0)$, directrix $x=-a$ and latus rectum $4a$.** For $y^2=8x$, $a=2$, so the focus is $(2,0)$ (Fig 10.2). The form $x^2=4ay$ opens upward instead. Do not take the coefficient 8 as $a$: it equals $4a$.
6. **For the ellipse, the bigger denominator decides the major axis.** In $\frac{x^2}{25}+\frac{y^2}{9}=1$ we have $a=5$, $b=3$, $c^2=a^2-b^2=16$, $e=\frac45$, foci $(\pm4,0)$. The latus rectum is $\frac{2b^2}{a}=3.6$ and the sum of focal distances is $2a=10$. Always $e<1$.
7. **For the hyperbola, $c^2=a^2+b^2$ and the sign between the terms is minus.** In $\frac{x^2}{16}-\frac{y^2}{9}=1$ we get $c=5$, $e=\frac54=1.25$ and asymptotes $y=\pm\frac34x$. A rectangular hyperbola has $a=b$, so $e=\sqrt2$. Do not use the ellipse relation $a^2-b^2$ here.
8. **Name the conic from the general equation.** Equal coefficients of $x^2$ and $y^2$ give a circle; same sign but unequal give an ellipse; opposite signs give a hyperbola; only one squared term gives a parabola (Fig 10.3). A quick check is the eccentricity: $0$, below 1, equal to 1, above 1.

### 10.3.1 Worked checks

**Q. Find the centre and radius of $x^2+y^2-6x+4y-12=0$, and the length of the tangent from $(3,6)$.**

**Answer.** $2g=-6$, $2f=4$, so the centre is $(3,-2)$ and $r=\sqrt{9+4+12}=5$. Tangent length $=\sqrt{S_1}=\sqrt{9+36-18+24-12}=\sqrt{39}\approx6.24$. Check: the distance from $(3,6)$ to the centre is 8 and $\sqrt{64-25}=\sqrt{39}$.

**Q. For $y^2=12x$ find the focus, directrix and length of the latus rectum.**

**Answer.** $4a=12$, so $a=3$. The focus is $(3,0)$, the directrix is $x=-3$ and the latus rectum is $4a=12$. The point $(3,6)$ lies on the curve since $36=12\times3$, and it is an end of the latus rectum.

**Q. Find the eccentricity and foci of $\frac{x^2}{25}+\frac{y^2}{9}=1$.**

**Answer.** $a=5$, $b=3$, $c=\sqrt{25-9}=4$, so $e=\frac45=0.8$ and the foci are $(\pm4,0)$. Check: the sum of distances from $(0,3)$ to the foci is $5+5=10=2a$.

## Formula and fact sheet

| Item | Result |
|---|---|
| Circle general | centre $(-g,-f)$, $r=\sqrt{g^2+f^2-c}$ |
| Parabola $y^2=4ax$ | focus $(a,0)$, directrix $x=-a$ |
| Ellipse | $e^2=1-\frac{b^2}{a^2}$ |
| Hyperbola | $e^2=1+\frac{b^2}{a^2}$ |

## Chapter summary

- Complete the square or use $g,f,c$ to read a circle off its equation.
- For $y^2=4ax$ read $a$ from the coefficient: $y^2=12x$ gives $a=3$.
- Ellipse: $e<1$; hyperbola: $e>1$.
- Major axis follows the larger denominator.
- Tangent length is $\sqrt{S_1}$, the power of the point.

## Practice questions

**Set A — Recall (20 questions)**

1. The radius of the circle $x^2+y^2=25$ is
   (a) 25 (b) 10 (c) 5 (d) 2.5
2. The centre of $(x-2)^2+(y+3)^2=16$ is
   (a) $(-2,3)$ (b) $(2,-3)$ (c) $(2,3)$ (d) $(-2,-3)$
3. The focus of $y^2=4x$ is
   (a) $(4,0)$ (b) $(0,1)$ (c) $(2,0)$ (d) $(1,0)$
4. The eccentricity of a parabola is
   (a) 1 (b) 0 (c) less than 1 (d) greater than 1
5. The directrix of $y^2=8x$ is
   (a) $x=2$ (b) $x=-2$ (c) $x=-8$ (d) $y=-2$
6. The length of the latus rectum of $y^2=12x$ is
   (a) 3 (b) 6 (c) 12 (d) 24
7. The centre of $x^2+y^2-4x+6y-12=0$ is
   (a) $(2,-3)$ (b) $(-2,3)$ (c) $(4,-6)$ (d) $(-4,6)$
8. The eccentricity of a circle is
   (a) 1 (b) greater than 1 (c) 0.5 (d) 0
9. The eccentricity of a hyperbola is
   (a) 0 (b) 1 (c) greater than 1 (d) less than 1
10. The length of the major axis of $\frac{x^2}{25}+\frac{y^2}{9}=1$ is
    (a) 5 (b) 10 (c) 6 (d) 3
11. The foci of $\frac{x^2}{25}+\frac{y^2}{9}=1$ are
    (a) $(\pm4,0)$ (b) $(\pm5,0)$ (c) $(\pm3,0)$ (d) $(0,\pm4)$
12. The circle with centre the origin and radius 3 is
    (a) $x^2+y^2=3$ (b) $x+y=9$ (c) $x^2-y^2=9$ (d) $x^2+y^2=9$
13. The vertex of $y^2=4ax$ is
    (a) $(a,0)$ (b) $(-a,0)$ (c) $(0,0)$ (d) $(0,a)$
14. The asymptotes of $\frac{x^2}{a^2}-\frac{y^2}{b^2}=1$ are
    (a) $y=\pm\frac{b}{a}x$ (b) $y=\pm\frac{a}{b}x$ (c) $y=\pm x$ (d) $x=\pm a$
15. The radius of $x^2+y^2+2gx+2fy+c=0$ is
    (a) $g^2+f^2-c$ (b) $\sqrt{g^2+f^2-c}$ (c) $\sqrt{g^2+f^2+c}$ (d) $g+f-c$
16. The parabola $x^2=4ay$ with $a>0$ opens
    (a) to the right (b) to the left (c) downward (d) upward
17. Which point lies on $x^2+y^2=25$?
    (a) $(2,3)$ (b) $(4,4)$ (c) $(3,4)$ (d) $(5,5)$
18. For $\frac{x^2}{16}+\frac{y^2}{25}=1$ the major axis lies along the
    (a) $y$-axis (b) $x$-axis (c) line $y=x$ (d) none: it is a circle
19. The focus of $x^2=8y$ is
    (a) $(2,0)$ (b) $(0,2)$ (c) $(0,8)$ (d) $(8,0)$
20. The curve $xy=4$ represents
    (a) a parabola (b) an ellipse (c) a circle (d) a rectangular hyperbola

::: note Answers and explanations — Set A
**1.** (c) — r² = 25.
**2.** (b) — centre is (h, k) with the signs reversed inside the brackets.
**3.** (d) — 4a = 4, a = 1.
**4.** (a) — by definition.
**5.** (b) — 4a = 8, a = 2, directrix x = −2.
**6.** (c) — the latus rectum is 4a = 12.
**7.** (a) — 2g = −4 and 2f = 6 give (−g, −f) = (2, −3).
**8.** (d) — a circle is an ellipse with a = b.
**9.** (c) — hyperbola has e > 1.
**10.** (b) — 2a = 10.
**11.** (a) — c² = 25 − 9 = 16.
**12.** (d) — x² + y² = r².
**13.** (c) — the vertex is the origin.
**14.** (a) — slope b/a.
**15.** (b) — remember the square root.
**16.** (d) — x² = 4ay opens up when a > 0.
**17.** (c) — 9 + 16 = 25.
**18.** (a) — 25 is the larger denominator, under y².
**19.** (b) — 4a = 8, a = 2, focus (0, 2).
**20.** (d) — xy = c² is a rectangular hyperbola.
:::

**Set B — Understanding (12 questions)**

1. The circle with centre $(3,4)$ passing through the origin is
   (a) $x^2+y^2-6x-8y=0$ (b) $x^2+y^2-6x-8y+25=0$ (c) $x^2+y^2=25$ (d) $x^2+y^2+6x+8y=0$
2. The radius of $x^2+y^2-6x+8y-11=0$ is
   (a) 11 (b) 5 (c) 36 (d) 6
3. The line $y=5$ and the circle $x^2+y^2=25$
   (a) do not meet (b) cut at two points (c) touch each other (d) meet at the centre
4. The parabola with vertex at the origin and focus $(3,0)$ is
   (a) $y^2=3x$ (b) $y^2=12x$ (c) $x^2=12y$ (d) $y^2=6x$
5. The eccentricity of $\frac{x^2}{25}+\frac{y^2}{16}=1$ is
   (a) $\frac{4}{5}$ (b) $\frac{5}{3}$ (c) $\frac{9}{25}$ (d) $\frac{3}{5}$
6. The eccentricity of $\frac{x^2}{9}-\frac{y^2}{16}=1$ is
   (a) $\frac{5}{3}$ (b) $\frac{3}{5}$ (c) $\frac{4}{3}$ (d) $\frac{25}{9}$
7. The latus rectum of $\frac{x^2}{25}+\frac{y^2}{9}=1$ has length
   (a) 5 (b) $\frac{9}{5}$ (c) $\frac{18}{5}$ (d) 10
8. The tangent to $x^2+y^2=25$ at $(3,4)$ is
   (a) $4x+3y=25$ (b) $3x+4y=25$ (c) $3x-4y=25$ (d) $x+y=7$
9. The distance between the foci of $\frac{x^2}{25}+\frac{y^2}{9}=1$ is
   (a) 4 (b) 5 (c) 10 (d) 8
10. A circle has the join of $(0,0)$ and $(6,8)$ as a diameter. Its radius is
    (a) 5 (b) 10 (c) 7 (d) 14
11. The area of $x^2+y^2=49$ (take $\pi=\frac{22}{7}$) is
    (a) 44 (b) 154 (c) 308 (d) 49
12. On $y^2=4x$, the positive value of $y$ when $x=9$ is
    (a) 3 (b) 9 (c) 6 (d) 36

::: note Answers and explanations — Set B
**1.** (a) — (x − 3)² + (y − 4)² = 25 expands to this with c = 0.
**2.** (d) — g = −3, f = 4: √(9 + 16 + 11) = 6.
**3.** (c) — the distance from the centre is 5 = r, so tangent.
**4.** (b) — a = 3 so y² = 12x.
**5.** (d) — √(1 − 16/25) = 3/5.
**6.** (a) — √(1 + 16/9) = 5/3.
**7.** (c) — 2b²/a = 18/5.
**8.** (b) — xx₁ + yy₁ = r².
**9.** (d) — 2ae = 2 × 4 = 8.
**10.** (a) — diameter = √(36 + 64) = 10.
**11.** (b) — (22/7) × 49 = 154.
**12.** (c) — y² = 36.
:::

**Set C — Application (8 questions)**

1. The radius of $x^2+y^2+4x-2y-4=0$ is
   (a) 9 (b) 2 (c) 4 (d) 3
2. The length of the tangent from $(5,0)$ to $x^2+y^2=9$ is
   (a) 4 (b) 5 (c) 16 (d) 3
3. A circle of radius 3 lies in the first quadrant touching both axes. Its centre is at distance from the origin
   (a) 3 (b) 6 (c) $3\sqrt{2}$ (d) 9
4. On $y^2=16x$, the distance of the point with $x=5$ from the focus is
   (a) 4 (b) 9 (c) 5 (d) 20
5. The area of the ellipse $\frac{x^2}{4}+y^2=1$ is
   (a) $2\pi$ (b) $4\pi$ (c) $\pi$ (d) $\frac{\pi}{2}$
6. The angle between the asymptotes of $x^2-y^2=1$ is
   (a) 30° (b) 45° (c) 60° (d) 90°
7. The number of tangents that can be drawn to a circle from a point outside it is
   (a) 1 (b) 2 (c) 3 (d) 0
8. The point $(2,2)$ with respect to the circle $x^2+y^2=9$ is
   (a) outside (b) on the circle (c) inside (d) cannot be said

::: note Answers and explanations — Set C
**1.** (d) — g = 2, f = −1: √(4 + 1 + 4) = 3.
**2.** (a) — √(25 − 9) = 4.
**3.** (c) — centre (3, 3), distance 3√2.
**4.** (b) — focal distance = x + a = 5 + 4.
**5.** (a) — π × 2 × 1.
**6.** (d) — asymptotes y = ±x are perpendicular.
**7.** (b) — two tangents from an external point.
**8.** (c) — 4 + 4 = 8 < 9.
:::
