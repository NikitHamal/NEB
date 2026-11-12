---
subject: Mathematics
grade: BCA
unit: 9
title: Straight Line and Distance Formulas
hours: 4
area: Coordinate Geometry
---

Coordinate geometry is where most scoring happens for students who like algebra, and the Dean's Office model tests the slope of $2x-4y=9$ and "equally inclined to both axes". The questions are formula substitutions: distance, midpoint, slope, equation of a line, distance of a point from a line. Practise until each takes 30 seconds.

::: key What the paper asks from this chapter
- **Distance, section, midpoint, centroid, area** formulas.
- **Slope**: $\frac{y_2-y_1}{x_2-x_1}=\tan\theta$; slope of $Ax+By+C=0$ is $-\frac{A}{B}$.
- **Equations**: slope-intercept, point-slope, two-point, intercept form.
- **Lines**: parallel ($m_1=m_2$), perpendicular ($m_1m_2=-1$), angle between lines.
- **Distance from a point to a line** and between parallel lines.
:::

## 9.1 Distance, section and area formulas

- $d=\sqrt{(x_2-x_1)^2+(y_2-y_1)^2}$; distance from the origin $\sqrt{x^2+y^2}$.
- Point dividing $A,B$ internally in $m:n$: $\left(\frac{mx_2+nx_1}{m+n},\frac{my_2+ny_1}{m+n}\right)$; midpoint $m=n=1$.
- Centroid: $\left(\frac{x_1+x_2+x_3}{3},\frac{y_1+y_2+y_3}{3}\right)$.
- Area of a triangle $=\frac{1}{2}\left|x_1(y_2-y_3)+x_2(y_3-y_1)+x_3(y_1-y_2)\right|$; three points are collinear when it is 0.

```photogrid label="9.1" cols="2" ratio="1.0" caption="The two Frenchmen who joined algebra to geometry. (a) Rene Descartes (1596-1650), portrait by Frans Hals: his La Geometrie (1637) gave every point a pair of numbers, which is why we say Cartesian coordinates. (b) Pierre de Fermat (1607-1665), shown in his bust at the Capitole in Toulouse, who found the same idea independently and used it to study lines and curves."
@ photo id="bcamath/descartes" cap="Rene Descartes, Cartesian coordinates"
focus 0.5 0.3
@ photo id="bcamath/fermat" cap="Pierre de Fermat, bust in Toulouse"
focus 0.5 0.4
```

```svgfig label="9.1" caption="Distance, midpoint, section and area on the plane, computed. For A(1, 2) and B(7, 10): AB = sqrt(6^2 + 8^2) = 10 (a 3-4-5 triangle scaled by 2), the midpoint is (4, 6), and the point P dividing AB internally in the ratio 1 : 2 is ((1 x 7 + 2 x 1)/3, (1 x 10 + 2 x 2)/3) = (3, 4.67). The triangle (0,0), (4,0), (0,3) has area (1/2)|4 x 3| = 6."
import math
from fractions import Fraction as F
A, B = (1, 2), (7, 10)
d = math.hypot(B[0] - A[0], B[1] - A[1]); mid = ((A[0] + B[0]) / 2, (A[1] + B[1]) / 2)
P = (F(1 * B[0] + 2 * A[0], 3), F(1 * B[1] + 2 * A[1], 3))
assert d == 10 and mid == (4, 6) and P == (3, F(14, 3))
ar = lambda p, q, r: abs(p[0] * (q[1] - r[1]) + q[0] * (r[1] - p[1]) + r[0] * (p[1] - q[1])) / 2
assert ar((0, 0), (4, 0), (0, 3)) == 6 and ar((0, 0), (1, 1), (2, 2)) == 0
f = Fig(780, 320)
ax = Axes(f, 40, 20, 340, 260, (-1, 9), (-1, 12))
ax.grid(1, 2, size=10); ax.axes("x", "y")
f.line(ax.X(1), ax.Y(2), ax.X(7), ax.Y(10), color=NAVY, sw=2.4)
f.line(ax.X(1), ax.Y(2), ax.X(7), ax.Y(2), color=SLATE, sw=1.2, dash=True); f.line(ax.X(7), ax.Y(2), ax.X(7), ax.Y(10), color=SLATE, sw=1.2, dash=True)
ax.pt(1, 2, "A(1, 2)", r=5, color=NAVY, dx=8, dy=14); ax.pt(7, 10, "B(7, 10)", r=5, color=NAVY, dx=-8, dy=-8, anchor="end")
ax.pt(4, 6, "M(4, 6)", r=5, color=RED, dx=10, dy=6); ax.pt(3, 14 / 3, "P(3, 4.67)", r=5, color=TEAL, dx=10, dy=22)
f.text(ax.X(4), ax.Y(2) + 18, "6", size=11, color=SLATE, bold=True); f.text(ax.X(7) + 12, ax.Y(6), "8", size=11, color=SLATE, bold=True)
f.text(600, 30, "Formulas, checked", size=11.5, color=NAVY, bold=True)
for j, (t, c) in enumerate([("AB = sqrt[(x2-x1)^2 + (y2-y1)^2] = 10", NAVY), ("midpoint = ((x1+x2)/2, (y1+y2)/2) = (4, 6)", SLATE), ("internal m : n = 1 : 2", SLATE), ("P = ((m x2 + n x1)/(m+n), (m y2 + n y1)/(m+n))", SLATE), ("P = (3, 14/3)", TEAL), ("external m : n: use (m x2 - n x1)/(m - n)", SLATE), ("area = (1/2)|x1(y2-y3) + x2(y3-y1) + x3(y1-y2)|", NAVY), ("triangle (0,0),(4,0),(0,3): area 6", TEAL), ("area 0 means the 3 points are collinear", RED)]):
    f.text(430, 64 + j * 27, t, size=10, color=c, anchor="start", bold=(c in (NAVY, RED)))
```

## 9.2 Slope and forms of the equation of a line

| Form | Equation |
|---|---|
| Slope-intercept | $y=mx+c$ |
| Point-slope | $y-y_1=m(x-x_1)$ |
| Two-point | $\frac{y-y_1}{y_2-y_1}=\frac{x-x_1}{x_2-x_1}$ |
| Intercept | $\frac{x}{a}+\frac{y}{b}=1$ |
| General | $Ax+By+C=0$, slope $-\frac{A}{B}$ |

The $x$-axis is $y=0$, the $y$-axis is $x=0$. A line at angle $\theta$ with the $x$-axis has slope $\tan\theta$. "Equally inclined to both axes" means $m=\pm1$.

```svgfig label="9.2" caption="Slope and intercepts. A line through (3, 0) and (0, 2) has slope (2 - 0)/(0 - 3) = -2/3, intercept form x/3 + y/2 = 1 and general form 2x + 3y - 6 = 0 (slope = -a/b = -2/3). On the right the same slope idea for four lines: y = 2x + 1 (steep), y = x (45 degrees), y = 0 (horizontal) and y = -x (falling)."
import math
m = (2 - 0) / (0 - 3); assert round(m, 6) == round(-2 / 3, 6) and -2 / 3 == -(2) / 3
for x, y in [(3, 0), (0, 2), (1.5, 1), (-3, 4)]: assert abs(2 * x + 3 * y - 6) < 1e-9
assert round(math.degrees(math.atan(1)), 6) == 45 and round(math.degrees(math.atan(2)), 2) == 63.43
f = Fig(780, 320)
ax = Axes(f, 30, 20, 250, 250, (-2, 5), (-2, 5))
ax.grid(1, 1, size=10); ax.axes("x", "y")
ax.curve(lambda x: (6 - 2 * x) / 3, -2, 5, color=NAVY, sw=2.5)
ax.pt(3, 0, "(3, 0)", r=5, color=RED, dx=6, dy=-10); ax.pt(0, 2, "(0, 2)", r=5, color=RED, dx=8, dy=-8)
f.text(150, 296, "x/3 + y/2 = 1:  slope -2/3, intercepts 3 and 2", size=10.5, color=NAVY, bold=True)
ax2 = Axes(f, 330, 20, 250, 250, (-3, 3), (-3, 3))
ax2.grid(1, 1, size=10); ax2.axes("x", "y")
for fn, col, nm, lx, ly in [(lambda x: 2 * x + 1, NAVY, "m = 2 (63.4 deg)", 0.0, 2.6), (lambda x: x, TEAL, "m = 1 (45 deg)", 1.0, 2.1), (lambda x: 0, AMBER, "m = 0", -2.9, 0.3), (lambda x: -x, RED, "m = -1 (135 deg)", -2.9, 2.5)]:
    ax2.curve(fn, -3, 3, color=col, sw=2.3)
    f.text(ax2.X(lx), ax2.Y(ly), nm, size=10, color=col, bold=True, anchor="start")
f.text(670, 30, "Forms of a line", size=11.5, color=NAVY, bold=True)
for j, (t, c) in enumerate([("y = mx + c  (slope, y-intercept)", SLATE), ("y - y1 = m(x - x1)  (point-slope)", SLATE), ("(y-y1)/(y2-y1) = (x-x1)/(x2-x1)", SLATE), ("x/a + y/b = 1  (intercepts a, b)", SLATE), ("ax + by + c = 0:  m = -a/b", NAVY), ("vertical line x = k: slope undefined", RED), ("horizontal line y = k: slope 0", RED)]):
    f.text(600, 62 + j * 30, t, size=10, color=c, anchor="start", bold=(c in (NAVY, RED)))
```

## 9.3 Angle between lines, parallel and perpendicular lines, distance from a point

- $\tan\theta=\left|\frac{m_1-m_2}{1+m_1m_2}\right|$. Parallel: $m_1=m_2$. Perpendicular: $m_1m_2=-1$.
- Distance of $(x_1,y_1)$ from $Ax+By+C=0$: $\frac{|Ax_1+By_1+C|}{\sqrt{A^2+B^2}}$.
- Distance between parallel lines $Ax+By+C_1=0$ and $Ax+By+C_2=0$: $\frac{|C_1-C_2|}{\sqrt{A^2+B^2}}$ (make $A,B$ equal first).
- Intersection of two lines: solve the equations simultaneously.

```svgfig label="9.3" caption="Angle between lines and distance from a point, computed. The lines y = x (m1 = 1) and y = 3x (m2 = 3) meet at the angle with tan t = |(m1 - m2)/(1 + m1 m2)| = 2/4 = 0.5, so t = 26.57 degrees. The distance of (2, 3) from 3x + 4y - 12 = 0 is |6 + 12 - 12|/5 = 6/5 = 1.2, the length of the perpendicular whose foot is (1.28, 2.04)."
import math
t = math.degrees(math.atan(abs((1 - 3) / (1 + 1 * 3)))); assert round(t, 2) == 26.57 and round(math.degrees(math.atan(3) - math.atan(1)), 2) == 26.57
a, b, c = 3, 4, -12; px, py = 2, 3
d = abs(a * px + b * py + c) / math.hypot(a, b); assert d == 1.2
k = (a * px + b * py + c) / (a * a + b * b); fx, fy = px - a * k, py - b * k
assert abs(a * fx + b * fy + c) < 1e-9 and abs(math.hypot(px - fx, py - fy) - 1.2) < 1e-9 and (round(fx, 2), round(fy, 2)) == (1.28, 2.04)
f = Fig(780, 320)
ax = Axes(f, 30, 20, 250, 250, (-1, 5), (-1, 5))
ax.grid(1, 1, size=10); ax.axes("x", "y")
ax.curve(lambda x: x, -1, 5, color=NAVY, sw=2.4); ax.curve(lambda x: 3 * x, -1, 5, color=TEAL, sw=2.4)
f.text(ax.X(3.7), ax.Y(3.5), "y = x", size=11, color=NAVY, bold=True); f.text(ax.X(0.45), ax.Y(4.4), "y = 3x", size=11, color=TEAL, bold=True)
f.text(150, 296, "angle between them = 26.57 degrees", size=10.5, color=RED, bold=True)
ax2 = Axes(f, 330, 20, 250, 250, (-1, 5), (-1, 5))
ax2.grid(1, 1, size=10); ax2.axes("x", "y")
ax2.curve(lambda x: (12 - 3 * x) / 4, -1, 5, color=NAVY, sw=2.4)
f.line(ax2.X(2), ax2.Y(3), ax2.X(fx), ax2.Y(fy), color=RED, sw=2)
ax2.pt(2, 3, "(2, 3)", r=5, color=RED, dx=8, dy=-8); ax2.pt(fx, fy, "foot", r=4, color=AMBER, dx=-8, dy=18, anchor="end")
f.text(ax2.X(3.2), ax2.Y(2.1), "3x + 4y = 12", size=10.5, color=NAVY, bold=True, anchor="start")
f.text(ax2.X(2.1), ax2.Y(3.35), "d = 1.2", size=11, color=RED, bold=True, anchor="start")
f.text(670, 30, "Rules", size=11.5, color=NAVY, bold=True)
for j, (t, c) in enumerate([("tan t = |(m1 - m2)/(1 + m1 m2)|", NAVY), ("parallel: m1 = m2", SLATE), ("perpendicular: m1 m2 = -1", SLATE), ("distance = |a x1 + b y1 + c| / sqrt(a^2 + b^2)", NAVY), ("(2,3) to 3x+4y-12=0: 6/5 = 1.2", TEAL), ("parallel lines: |c1 - c2| / sqrt(a^2 + b^2)", SLATE), ("3x+4y-12=0 and 3x+4y+3=0: 15/5 = 3", TEAL)]):
    f.text(600, 62 + j * 32, t, size=10, color=c, anchor="start", bold=(c in (NAVY,)))
```

## 9.4 Eight traps in the straight line

Coordinate geometry is mostly substitution into formulas, so the marks go to students who choose the right formula and keep the signs. These eight traps appear in the Dean's Office model and in earlier papers.

1. **The distance formula squares the differences, so signs do not matter.** For $A(1,2)$ and $B(7,10)$ we get $\sqrt{6^2+8^2}=10$ (Fig 9.1). Students sometimes forget the square root and answer 100. Check that the answer is the same whichever point you call $A$.
2. **Section formula: the ratio $m:n$ pairs $m$ with the second point.** For internal division $P=\left(\frac{mx_2+nx_1}{m+n},\frac{my_2+ny_1}{m+n}\right)$, so a ratio of $1:2$ puts $P$ closer to $A$. For external division change the plus signs in the denominator and the numerator to minus. The midpoint is the special case $1:1$.
3. **Area of a triangle needs the absolute value.** Use $\frac12\left|x_1(y_2-y_3)+x_2(y_3-y_1)+x_3(y_1-y_2)\right|$, so a negative result becomes positive. If the value is zero, the three points are collinear, which is how "show that the points lie on a line" is answered. Check with the triangle $(0,0),(4,0),(0,3)$, area 6.
4. **Slope is rise over run.** $m=\frac{y_2-y_1}{x_2-x_1}=\tan\theta$, with $\theta$ measured anticlockwise from the positive x-axis (Fig 9.2). A horizontal line has slope 0, while a vertical line has no slope at all, not zero. Do not mix up the order of subtraction in the numerator and denominator.
5. **Know what each form gives you.** $y=mx+c$ shows slope and y-intercept, and $\frac xa+\frac yb=1$ shows both intercepts, not the slope. For $ax+by+c=0$ the slope is $-\frac ab$ and the y-intercept is $-\frac cb$. The line $2x+3y=6$ has slope $-\frac23$, not $\frac23$.
6. **Parallel lines share the slope; perpendicular slopes multiply to $-1$.** A line parallel to $3x+4y-12=0$ is $3x+4y+k=0$, with the same $a$ and $b$. A line perpendicular to it is $4x-3y+k=0$: swap $a$ and $b$ and change one sign. Check that $-\frac34\times\frac43=-1$.
7. **The angle between lines uses the absolute value.** $\tan\theta=\left|\frac{m_1-m_2}{1+m_1m_2}\right|$ gives the acute angle, so for $y=x$ and $y=3x$ it is $\tan^{-1}0.5=26.57^\circ$ (Fig 9.3). If $1+m_1m_2=0$ the lines are perpendicular and the angle is $90^\circ$. The obtuse angle is $180^\circ$ minus the acute one.
8. **Distance from a point: bring the equation to $ax+by+c=0$ first.** $d=\frac{|ax_1+by_1+c|}{\sqrt{a^2+b^2}}$, so for the point $(2,3)$ and $3x+4y-12=0$ we get $\frac{6}{5}=1.2$. For the distance between two parallel lines, make the coefficients of $x$ and $y$ equal first, then use $\frac{|c_1-c_2|}{\sqrt{a^2+b^2}}$. Forgetting the square root in the denominator is the commonest slip.

### 9.4.1 Worked checks

**Q. Find the distance between $A(1,2)$ and $B(7,10)$, the midpoint, and the point dividing $AB$ internally in the ratio $1:2$.**

**Answer.** $AB=\sqrt{36+64}=10$. Midpoint $=(4,6)$. Ratio $1:2$: $P=\left(\frac{7+2}{3},\frac{10+4}{3}\right)=\left(3,\frac{14}{3}\right)$. $AP=\frac{10}{3}$, one third of $AB$, which agrees.

**Q. Find the equation of the line through $(2,3)$ and $(4,7)$, and its intercepts.**

**Answer.** Slope $=\frac{7-3}{4-2}=2$. Point-slope: $y-3=2(x-2)$, so $y=2x-1$. The y-intercept is $-1$ and the x-intercept is $\frac12$. Check that $(4,7)$ satisfies $7=2(4)-1$.

**Q. Find the distance of $(2,3)$ from $3x+4y-12=0$ and the angle between $y=x$ and $y=3x$.**

**Answer.** $d=\frac{|6+12-12|}{\sqrt{9+16}}=\frac65=1.2$. For the angle, $\tan\theta=\left|\frac{1-3}{1+3}\right|=0.5$, so $\theta=26.57^\circ$. Both results are drawn in Fig 9.3.

## Formula and fact sheet

| Item | Result |
|---|---|
| Slope | $\frac{y_2-y_1}{x_2-x_1}$ |
| Perpendicular | $m_1m_2=-1$ |
| Point-line distance | $\frac{\lvert Ax_1+By_1+C\rvert}{\sqrt{A^2+B^2}}$ |
| Triangle area (vertices) | $\frac{1}{2}\lvert\ldots\rvert$ |

## Chapter summary

- Use $d=\sqrt{\Delta x^2+\Delta y^2}$; memorise 3-4-5 and 5-12-13.
- Convert $Ax+By+C=0$ to slope $-A/B$.
- Intercept form needs both intercepts non-zero.
- Parallel lines have equal slopes; perpendicular slopes multiply to $-1$.
- In the point-line formula the denominator is $\sqrt{A^2+B^2}$.

## Practice questions

**Set A — Recall (20 questions)**

1. The distance between $(0,0)$ and $(3,4)$ is
   (a) 5 (b) 7 (c) 25 (d) 1
2. The slope of the line through $(1,2)$ and $(3,6)$ is
   (a) $\frac{1}{2}$ (b) 4 (c) 2 (d) 3
3. The midpoint of $(2,4)$ and $(6,8)$ is
   (a) $(8,12)$ (b) $(3,5)$ (c) $(4,5)$ (d) $(4,6)$
4. The slope of the line $2x-4y=9$ is
   (a) 2 (b) $\frac{1}{2}$ (c) $-\frac{1}{2}$ (d) $-2$
5. The $y$-intercept of $y=3x+5$ is
   (a) 3 (b) $-5$ (c) 5 (d) 8
6. Lines with slopes 2 and $-\frac{1}{2}$ are
   (a) perpendicular (b) parallel (c) coincident (d) neither
7. The slope of a line making 45° with the positive $x$-axis is
   (a) 0 (b) $-1$ (c) not defined (d) 1
8. The centroid of the triangle $(0,0)$, $(6,0)$, $(0,9)$ is
   (a) $(3,4.5)$ (b) $(2,3)$ (c) $(6,9)$ (d) $(1,1.5)$
9. The equation of the line through the origin with slope 2 is
   (a) $y=2x$ (b) $y=x+2$ (c) $x=2y$ (d) $y=2$
10. The distance of the origin from $3x+4y-10=0$ is
    (a) 10 (b) 5 (c) 1 (d) 2
11. The $x$-intercept of $2x+3y=6$ is
    (a) 2 (b) 6 (c) 3 (d) 1
12. Two lines are parallel when their slopes are
    (a) product $-1$ (b) equal (c) sum zero (d) reciprocal
13. The equation of the $y$-axis is
    (a) $y=0$ (b) $y=x$ (c) $x=y$ (d) $x=0$
14. The line $\frac{x}{2}+\frac{y}{3}=1$ meets the $x$-axis at
    (a) $(2,0)$ (b) $(3,0)$ (c) $(0,2)$ (d) $(0,3)$
15. The point dividing $(0,0)$ and $(6,0)$ internally in the ratio $1:2$ is
    (a) $(3,0)$ (b) $(4,0)$ (c) $(2,0)$ (d) $(1,0)$
16. The slope of a line perpendicular to a line of slope 3 is
    (a) 3 (b) $-\frac{1}{3}$ (c) $\frac{1}{3}$ (d) $-3$
17. The area of the triangle $(0,0)$, $(4,0)$, $(0,3)$ is
    (a) 6 (b) 12 (c) 7 (d) 3.5
18. The slope of $ax+by+c=0$ is
    (a) $\frac{a}{b}$ (b) $-\frac{b}{a}$ (c) $\frac{b}{a}$ (d) $-\frac{a}{b}$
19. The distance between $(1,1)$ and $(4,5)$ is
    (a) 4 (b) 5 (c) 7 (d) 25
20. The line through $(0,3)$ with slope $-1$ is
    (a) $y=x+3$ (b) $y=-x-3$ (c) $y=-x+3$ (d) $y=3x-1$

::: note Answers and explanations — Set A
**1.** (a) — √(9 + 16) = 5.
**2.** (c) — (6 − 2)/(3 − 1) = 2.
**3.** (d) — average the coordinates: (4, 6).
**4.** (b) — y = x/2 − 9/4; or −A/B = 2/4.
**5.** (c) — the constant in y = mx + c.
**6.** (a) — 2 × (−½) = −1.
**7.** (d) — tan 45° = 1.
**8.** (b) — (6/3, 9/3).
**9.** (a) — y = mx with m = 2.
**10.** (d) — |−10|/√(9 + 16) = 2.
**11.** (c) — set y = 0: x = 3.
**12.** (b) — equal slopes; (a) is perpendicular.
**13.** (d) — every point on the y-axis has x = 0.
**14.** (a) — set y = 0: x = 2.
**15.** (c) — x = (1×6 + 2×0)/3 = 2.
**16.** (b) — negative reciprocal.
**17.** (a) — ½ × 4 × 3.
**18.** (d) — rearrange to y = −(a/b)x − c/b.
**19.** (b) — 3-4-5 triangle.
**20.** (c) — y = mx + c with m = −1, c = 3.
:::

**Set B — Understanding (12 questions)**

1. The line through $(1,2)$ and $(k,-5)$ is equally inclined to both axes. A possible value of $k$ is
   (a) 3 (b) 5 (c) 7 (d) 8
2. The angle between the line $y=x$ and the $x$-axis is
   (a) 30° (b) 45° (c) 60° (d) 90°
3. The distance of $(2,3)$ from $3x-4y+5=0$ is
   (a) $\frac{1}{5}$ (b) 1 (c) 5 (d) $\frac{1}{25}$
4. The line through $(2,3)$ and $(4,7)$ is
   (a) $y=2x+1$ (b) $y=2x+3$ (c) $y=2x-1$ (d) $y=x+1$
5. The distance between the parallel lines $3x+4y+5=0$ and $3x+4y-10=0$ is
   (a) 15 (b) 5 (c) 1 (d) 3
6. The lines $x+y=5$ and $x-y=1$ meet at
   (a) $(2,3)$ (b) $(3,2)$ (c) $(4,1)$ (d) $(1,4)$
7. The points $(1,2)$, $(2,4)$, $(3,k)$ are collinear when $k$ is
   (a) 6 (b) 5 (c) 7 (d) 8
8. The slope of a line perpendicular to $2x+3y=6$ is
   (a) $-\frac{2}{3}$ (b) $\frac{2}{3}$ (c) $\frac{3}{2}$ (d) $-\frac{3}{2}$
9. The $x$-axis divides the join of $(1,2)$ and $(3,-4)$ in the ratio
   (a) 2:1 (b) 1:2 (c) 1:1 (d) 3:1
10. The line $y=\sqrt{3}\,x$ makes with the $x$-axis an angle of
    (a) 60° (b) 30° (c) 45° (d) 120°
11. The line with $x$-intercept 4 and $y$-intercept 6 is
    (a) $2x+3y=12$ (b) $3x+2y=6$ (c) $x+y=10$ (d) $3x+2y=12$
12. The area of the triangle $(1,1)$, $(5,1)$, $(3,4)$ is
    (a) 12 (b) 3 (c) 6 (d) 8

::: note Answers and explanations — Set B
**1.** (d) — slope −7/(k − 1) = ±1 gives k = 8 or −6; only 8 is listed.
**2.** (b) — tan θ = 1.
**3.** (a) — |6 − 12 + 5| / 5 = 1/5.
**4.** (c) — slope 2; y − 3 = 2(x − 2).
**5.** (d) — |5 − (−10)| / 5 = 3.
**6.** (b) — adding: x = 3, then y = 2.
**7.** (a) — the points lie on y = 2x.
**8.** (c) — original slope −2/3; perpendicular is 3/2.
**9.** (b) — y-coordinate zero: (−4m + 2n) = 0, so m : n = 1 : 2.
**10.** (a) — tan θ = √3.
**11.** (d) — x/4 + y/6 = 1, times 12.
**12.** (c) — base 4, height 3: ½ × 4 × 3.
:::

**Set C — Application (8 questions)**

1. The line through $(2,3)$ parallel to $3x-y=4$ has $y$-intercept
   (a) 3 (b) $-3$ (c) 6 (d) $-6$
2. The perimeter of the triangle with vertices $(0,0)$, $(4,0)$, $(4,3)$ is
   (a) 7 (b) 10 (c) 14 (d) 12
3. A point $P$ lies on $y=x$ and is equidistant from $(0,0)$ and $(4,0)$. $P$ is
   (a) $(2,2)$ (b) $(4,4)$ (c) $(1,1)$ (d) $(2,0)$
4. The angle between lines of slopes 3 and $\frac{1}{2}$ is
   (a) 30° (b) 60° (c) 45° (d) 90°
5. The distance of $(2,1)$ from $x+y+1=0$ is
   (a) 4 (b) $2\sqrt{2}$ (c) $\sqrt{2}$ (d) $4\sqrt{2}$
6. The line $2x+3y=12$ with the axes encloses a triangle of area
   (a) 24 (b) 6 (c) 10 (d) 12
7. The centroid of $(1,2)$, $(3,4)$, $(5,9)$ is
   (a) $(3,4)$ (b) $(2,5)$ (c) $(3,5)$ (d) $(9,15)$
8. The point $(k,2)$ lies on $2x-3y+2=0$. Then $k$ is
   (a) 2 (b) 1 (c) 3 (d) 4

::: note Answers and explanations — Set C
**1.** (b) — y − 3 = 3(x − 2) gives y = 3x − 3.
**2.** (d) — sides 4, 3 and 5.
**3.** (a) — equidistant means x = 2, so P = (2, 2).
**4.** (c) — |(3 − ½)/(1 + 3/2)| = 1.
**5.** (b) — |2 + 1 + 1|/√2 = 2√2.
**6.** (d) — intercepts 6 and 4: ½ × 6 × 4.
**7.** (c) — (9/3, 15/3).
**8.** (a) — 2k − 6 + 2 = 0.
:::
