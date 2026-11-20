---
subject: Mathematics
grade: IOE
unit: 4
title: Coordinate Geometry
hours: 6
area: Mathematics
---

Coordinate geometry carries about **6 questions**, and the official booklet's own model question — "the value of $k$ for which $x+y-1=0$ touches $y^2=kx$" — shows the style: a tangency condition, a standard property of a conic, or a plane in space. Memorising the standard forms and the three tangency conditions ($c^2=r^2(1+m^2)$, $c=a/m$, $c^2=a^2m^2\pm b^2$) answers more than half of them.

::: key What the paper asks from this chapter
- Distance of a point from a line, angle between two lines, concurrency, area of a triangle.
- Pair of lines $ax^2+2hxy+by^2=0$: angle $\tan\theta=\frac{2\sqrt{h^2-ab}}{|a+b|}$; perpendicular iff $a+b=0$.
- Circle: centre and radius from the general equation, tangent, length of tangent $\sqrt{S_1}$, radical axis.
- Conics: focus, directrix, latus rectum, eccentricity; tangent in slope form.
- Space: distance, direction cosines, plane equation, distance from a point to a plane.
:::

## 4.1 Straight lines, pair of lines

| Form | Equation |
|---|---|
| slope-intercept | $y=mx+c$ |
| point-slope | $y-y_1=m(x-x_1)$ |
| two-point | $\dfrac{y-y_1}{y_2-y_1}=\dfrac{x-x_1}{x_2-x_1}$ |
| intercept | $\dfrac{x}{a}+\dfrac{y}{b}=1$ |
| normal | $x\cos\alpha+y\sin\alpha=p$ |
| general | $Ax+By+C=0$, slope $-A/B$ |

- **Distance of $(x_1,y_1)$ from $Ax+By+C=0$:** $\dfrac{|Ax_1+By_1+C|}{\sqrt{A^2+B^2}}$. Between parallel lines $Ax+By+C_1=0$, $Ax+By+C_2=0$: $\dfrac{|C_1-C_2|}{\sqrt{A^2+B^2}}$.
- **Angle** between lines of slopes $m_1,m_2$: $\tan\theta=\Big|\dfrac{m_1-m_2}{1+m_1m_2}\Big|$; parallel $m_1=m_2$, perpendicular $m_1m_2=-1$.
- **Family** of lines through the intersection of $L_1=0,L_2=0$: $L_1+\lambda L_2=0$. Three lines are concurrent if the determinant of their coefficients is 0.
- **Area** of the triangle $(x_i,y_i)$: $\tfrac{1}{2}|x_1(y_2-y_3)+x_2(y_3-y_1)+x_3(y_1-y_2)|$.
- Bisectors of the angles between two lines: $\dfrac{A_1x+B_1y+C_1}{\sqrt{A_1^2+B_1^2}}=\pm\dfrac{A_2x+B_2y+C_2}{\sqrt{A_2^2+B_2^2}}$.
- Foot of the perpendicular and image: solve using the normal direction $(A,B)$.

### Pair of lines

$ax^2+2hxy+by^2=0$ (homogeneous) is a pair of lines through the origin with $m_1+m_2=-\frac{2h}{b}$, $m_1m_2=\frac{a}{b}$. Angle: $\tan\theta=\dfrac{2\sqrt{h^2-ab}}{a+b}$. Real and distinct if $h^2>ab$, coincident if $h^2=ab$; **perpendicular if $a+b=0$**. The general second-degree equation $ax^2+2hxy+by^2+2gx+2fy+c=0$ is a pair of lines iff $abc+2fgh-af^2-bg^2-ch^2=0$.

## 4.2 Circles, equations in different forms, tangent and normal

- Centre $(h,k)$, radius $r$: $(x-h)^2+(y-k)^2=r^2$.
- General: $x^2+y^2+2gx+2fy+c=0$, centre $(-g,-f)$, radius $\sqrt{g^2+f^2-c}$.
- Diameter form: ends $(x_1,y_1),(x_2,y_2)$: $(x-x_1)(x-x_2)+(y-y_1)(y-y_2)=0$.
- Parametric: $(h+r\cos\theta,\,k+r\sin\theta)$.
- Through three points: substitute into the general form and solve.

**Tangent at $(x_1,y_1)$:** $xx_1+yy_1+g(x+x_1)+f(y+y_1)+c=0$ (for $x^2+y^2=r^2$: $xx_1+yy_1=r^2$). The normal passes through the centre.
**Line $y=mx+c$ touches $x^2+y^2=r^2$ iff $c^2=r^2(1+m^2)$.**
**Length of tangent** from $P$: $\sqrt{S_1}$ where $S_1$ is the circle's expression at $P$. Chord at distance $d$ from the centre: $2\sqrt{r^2-d^2}$.
**Two circles:** radical axis $S_1-S_2=0$; orthogonal iff $2g_1g_2+2f_1f_2=c_1+c_2$; with centres distance $d$ apart: externally tangent if $d=r_1+r_2$, internally if $d=|r_1-r_2|$.

## 4.3 Conic sections: parabola, ellipse and hyperbola

All conics are $\dfrac{\text{distance from focus}}{\text{distance from directrix}}=e$.

| | Parabola $y^2=4ax$ | Ellipse $\frac{x^2}{a^2}+\frac{y^2}{b^2}=1$ ($a>b$) | Hyperbola $\frac{x^2}{a^2}-\frac{y^2}{b^2}=1$ |
|---|---|---|---|
| $e$ | 1 | $\sqrt{1-b^2/a^2}<1$ | $\sqrt{1+b^2/a^2}>1$ |
| focus | $(a,0)$ | $(\pm ae,0)$ | $(\pm ae,0)$ |
| directrix | $x=-a$ | $x=\pm a/e$ | $x=\pm a/e$ |
| latus rectum | $4a$ | $2b^2/a$ | $2b^2/a$ |
| tangent (slope $m$) | $y=mx+a/m$ | $y=mx\pm\sqrt{a^2m^2+b^2}$ | $y=mx\pm\sqrt{a^2m^2-b^2}$ |
| tangent at $(x_1,y_1)$ | $yy_1=2a(x+x_1)$ | $\frac{xx_1}{a^2}+\frac{yy_1}{b^2}=1$ | $\frac{xx_1}{a^2}-\frac{yy_1}{b^2}=1$ |
| parametric | $(at^2,2at)$ | $(a\cos\theta,b\sin\theta)$ | $(a\sec\theta,b\tan\theta)$ |
| other | vertex origin | major axis $2a$, minor $2b$; sum of focal distances $2a$ | asymptotes $y=\pm\frac{b}{a}x$; $|PF_1-PF_2|=2a$ |

Other orientations: $x^2=4ay$ opens upward with focus $(0,a)$; $y^2=-4ax$ opens left. For a hyperbola $\frac{x^2}{a^2}-\frac{y^2}{b^2}=-1$ the transverse axis is vertical. **Rectangular hyperbola** $xy=c^2$ ($a=b$, $e=\sqrt{2}$); asymptotes are the axes. The focal distance of $(x_1,y_1)$ on the parabola is $x_1+a$. The parabola $y=px^2+qx+r$ has vertex at $x=-\frac{q}{2p}$.

::: example The booklet's tangent question
**Problem.** For what $k$ is $x+y-1=0$ tangent to $y^2=kx$?

**Solution.** $y^2=4ax$ with $a=k/4$. The line is $y=-x+1$, $m=-1$, $c=1$. Condition $c=a/m$: $1=\dfrac{k/4}{-1}$, so $k=-4$.
:::

## 4.4 Coordinates in space, plane and its equation

- **Distance** $\sqrt{(x_2-x_1)^2+(y_2-y_1)^2+(z_2-z_1)^2}$. **Section formula** (ratio $m:n$): $\Big(\dfrac{mx_2+nx_1}{m+n},\dots\Big)$.
- **Direction cosines** $l,m,n$ with $l^2+m^2+n^2=1$; direction ratios $a,b,c$ give $l=\dfrac{a}{\sqrt{a^2+b^2+c^2}}$. A line equally inclined to the axes has $l=m=n=\pm\frac{1}{\sqrt{3}}$.
- **Angle between lines** $\cos\theta=|l_1l_2+m_1m_2+n_1n_2|$.
- **Plane** $ax+by+cz+d=0$ with normal $(a,b,c)$; intercept form $\frac{x}{p}+\frac{y}{q}+\frac{z}{r}=1$; through three points: determinant condition; through $(x_1,y_1,z_1)$ with normal $(a,b,c)$: $a(x-x_1)+b(y-y_1)+c(z-z_1)=0$.
- **Distance of $(x_1,y_1,z_1)$ from the plane:** $\dfrac{|ax_1+by_1+cz_1+d|}{\sqrt{a^2+b^2+c^2}}$. Between parallel planes: $\dfrac{|d_1-d_2|}{\sqrt{a^2+b^2+c^2}}$.
- **Angle between planes** = angle between normals. Plane and line: $\sin\theta=\dfrac{|aL+bM+cN|}{\sqrt{a^2+b^2+c^2}\sqrt{L^2+M^2+N^2}}$.
- Line through $(x_1,y_1,z_1)$ with direction ratios $a,b,c$: $\dfrac{x-x_1}{a}=\dfrac{y-y_1}{b}=\dfrac{z-z_1}{c}$.

```photogrid label="4.1" cols="2" ratio="1.2" caption="The focus of a parabola. (a) A solar dish: its surface is a paraboloid, so every ray parallel to the axis is reflected through one point, the focus. (b) The parabola x^2 = 4 f y has focus (0, f). For a dish 7 m across and 1 m deep, putting x = 3.5, y = 1 gives f = 3.5^2 / 4 = 3.06 m. The path length from a line at the rim level to the focus is checked to be the same for every ray, which is the reason all of them arrive together; the latus rectum (the width through the focus) is 4f."
@ photo id="ioemath/dish" cap="A parabolic solar dish"
fit 1.2
focus 0.5 0.5
@ svg cap="x^2 = 4fy with f = 3.06 m: parallel rays meet at F"
import math
d, hgt = 7.0, 1.0
f_ = (d / 2) ** 2 / (4 * hgt)
y = lambda x: x * x / (4 * f_)
paths = []
for x in (0.5, 1.5, 2.5, 3.5):
    paths.append((hgt - y(x)) + math.hypot(x, y(x) - f_))
assert abs(f_ - 3.0625) < 1e-9 and max(paths) - min(paths) < 1e-9 and abs(paths[0] - (hgt + f_)) < 1e-9
fg = Fig(300, 236)
sx, sy = 36.0, 36.0
X = lambda x: 150 + x * sx; Y = lambda yy: 190 - yy * sy * 0.5 * 2 / 2
fg.line(10, Y(0), 290, Y(0), color=SOFT, sw=1); fg.line(150, Y(0) + 6, 150, 20, color=SOFT, sw=1)
xs = [i * 0.1 - 3.5 for i in range(0, 71)]
for a, b in zip(xs, xs[1:]): fg.line(X(a), Y(y(a)), X(b), Y(y(b)), color=NAVY, sw=2.4)
for x in (-2.5, -1.2, 1.2, 2.5, -3.5, 3.5):
    fg.arrow([(X(x), 20), (X(x), Y(y(x)))], color=AMBER, sw=1.2)
    fg.line(X(x), Y(y(x)), X(0), Y(f_), color=RED, sw=1.2)
fg.circle(X(0), Y(f_), 4, fill=RED, stroke=RED)
fg.text(X(0) + 10, Y(f_) - 4, "F (0, %.2f)" % f_, size=10.5, color=RED, bold=True, anchor="start")
fg.text(150, 212, "f = x²/4y = 3.5² / 4 = %.2f m" % f_, size=10.5, color=NAVY, bold=True)
fg.text(150, 230, "latus rectum 4f = %.2f m; path sums equal" % (4 * f_), size=10.5, color=TEAL, bold=True)
f = fg
```

## Formula and fact sheet

| Topic | Result |
|---|---|
| point–line distance | $\frac{|Ax_1+By_1+C|}{\sqrt{A^2+B^2}}$ |
| angle between lines | $\tan\theta=|\frac{m_1-m_2}{1+m_1m_2}|$ |
| circle tangent | $c^2=r^2(1+m^2)$ |
| tangent length | $\sqrt{S_1}$ |
| parabola | $y=mx+a/m$, LR $=4a$ |
| ellipse / hyperbola $e$ | $\sqrt{1-b^2/a^2}$ / $\sqrt{1+b^2/a^2}$ |
| plane distance | $\frac{|ax_1+by_1+cz_1+d|}{\sqrt{a^2+b^2+c^2}}$ |

## Chapter summary

- Distance, angle and area formulas for lines are one-liners; learn them exactly.
- $x^2+y^2+2gx+2fy+c=0$: centre $(-g,-f)$, radius $\sqrt{g^2+f^2-c}$.
- Tangency to a circle is $c^2=r^2(1+m^2)$; to a parabola $c=a/m$.
- Latus rectum: $4a$ for the parabola, $2b^2/a$ for ellipse and hyperbola.
- A plane's normal is $(a,b,c)$; parallel planes differ only in $d$.

## Practice questions

**Set A — Recall (12 questions)**

1. The slope of the line $3x+4y=12$ is
   (a) $3/4$ (b) $-3/4$ (c) $4/3$ (d) $-4/3$
2. The distance of the origin from the line $3x+4y-10=0$ is
   (a) 2 (b) 10 (c) 5 (d) $2/5$
3. The acute angle between the lines $y=x$ and $y=\sqrt{3}x$ is
   (a) $30^\circ$ (b) $45^\circ$ (c) $15^\circ$ (d) $60^\circ$
4. The centre and radius of $x^2+y^2-6x+8y-11=0$ are
   (a) $(-3,4)$, 6 (b) $(3,-4)$, 36 (c) $(3,-4)$, 5 (d) $(3,-4)$, 6
5. The length of the tangent from $(5,0)$ to $x^2+y^2=9$ is
   (a) 3 (b) 4 (c) 5 (d) 16
6. The focus of the parabola $y^2=8x$ is
   (a) $(4,0)$ (b) $(8,0)$ (c) $(2,0)$ (d) $(0,2)$
7. The length of the latus rectum of $\frac{x^2}{25}+\frac{y^2}{9}=1$ is
   (a) $9/5$ (b) 6 (c) 10 (d) $18/5$
8. The eccentricity of $\frac{x^2}{16}-\frac{y^2}{9}=1$ is
   (a) $5/4$ (b) $4/5$ (c) $7/4$ (d) $3/4$
9. The distance between $(1,2,3)$ and $(4,6,15)$ is
   (a) 12 (b) 13 (c) 11 (d) 14
10. The distance of $(1,2,3)$ from the plane $x+2y+2z=3$ is
    (a) 2 (b) $11/3$ (c) 3 (d) $8/3$
11. $ax^2+2hxy+by^2=0$ represents perpendicular lines if
    (a) $h=0$ (b) $ab=h^2$ (c) $a+b=0$ (d) $a=b$
12. The radius of the circle with the ends of a diameter at $(1,2)$ and $(5,6)$ is
    (a) $2\sqrt{2}$ (b) 4 (c) 8 (d) $4\sqrt{2}$

::: note Answers and explanations — Set A
**1.** (b) — $y=-\frac{3}{4}x+3$.
**2.** (a) — $\frac{|-10|}{\sqrt{9+16}}=2$.
**3.** (c) — slopes 1 and $\sqrt{3}$: $\tan\theta=\frac{\sqrt{3}-1}{\sqrt{3}+1}=2-\sqrt{3}=\tan15^\circ$ (also $60^\circ-45^\circ$).
**4.** (d) — $g=-3$, $f=4$, $c=-11$: centre $(3,-4)$, $r=\sqrt{9+16+11}=6$.
**5.** (b) — $\sqrt{S_1}=\sqrt{25-9}=4$.
**6.** (c) — $4a=8$, $a=2$.
**7.** (d) — $\frac{2b^2}{a}=\frac{18}{5}$.
**8.** (a) — $e=\sqrt{1+\frac{9}{16}}=\frac{5}{4}$.
**9.** (b) — $\sqrt{9+16+144}=13$.
**10.** (d) — $\frac{|1+4+6-3|}{\sqrt{1+4+4}}=\frac{8}{3}$.
**11.** (c) — $a+b=0$ (coefficient sum of $x^2,y^2$).
**12.** (a) — diameter $=\sqrt{16+16}=4\sqrt{2}$, radius $2\sqrt{2}$.
:::

**Set B — Understanding (8 questions)**

1. The line through $(1,2)$ perpendicular to $2x+3y=5$ is
   (a) $3x-2y+1=0$ (b) $3x+2y-7=0$ (c) $2x+3y-8=0$ (d) $2x-3y+4=0$
2. The distance between the parallel lines $x+2y-3=0$ and $x+2y+7=0$ is
   (a) 10 (b) $2\sqrt{5}$ (c) $4/\sqrt{5}$ (d) $\sqrt{5}$
3. The lines $x+y=2$, $2x-y=1$ and $3x+ky=7$ are concurrent for $k=$
   (a) 2 (b) 3 (c) 4 (d) 5
4. The tangent to $x^2+y^2=25$ at $(3,4)$ is
   (a) $4x+3y=25$ (b) $3x-4y=25$ (c) $3x+4y=5$ (d) $3x+4y=25$
5. The line $y=x+c$ touches the circle $x^2+y^2=8$ for
   (a) $c=\pm2$ (b) $c=\pm\sqrt{8}$ (c) $c=\pm4$ (d) $c=\pm8$
6. The parabola with focus $(3,0)$ and directrix $x=-3$ is
   (a) $y^2=12x$ (b) $y^2=6x$ (c) $y^2=3x$ (d) $x^2=12y$
7. An ellipse has foci $(\pm3,0)$ and minor axis of length 8. Its eccentricity is
   (a) $4/5$ (b) $3/5$ (c) $3/4$ (d) $5/3$
8. The plane through $(1,0,0)$, $(0,2,0)$ and $(0,0,3)$ is
   (a) $x+2y+3z=6$ (b) $3x+2y+z=6$ (c) $2x+3y+6z=6$ (d) $6x+3y+2z=6$

::: note Answers and explanations — Set B
**1.** (a) — slope of the given line is $-\frac{2}{3}$, so the perpendicular's is $\frac{3}{2}$: $y-2=\frac{3}{2}(x-1)\Rightarrow3x-2y+1=0$.
**2.** (b) — $\frac{|-3-7|}{\sqrt{5}}=\frac{10}{\sqrt{5}}=2\sqrt{5}$.
**3.** (c) — the first two meet at $(1,1)$; then $3+k=7$.
**4.** (d) — $xx_1+yy_1=r^2$: $3x+4y=25$.
**5.** (c) — $c^2=r^2(1+m^2)=8\times2=16$.
**6.** (a) — $a=3$, $y^2=4ax=12x$.
**7.** (b) — $b=4$, $ae=3$: $a^2=16+9=25$, $a=5$, $e=\frac{3}{5}$.
**8.** (d) — intercept form $x+\frac{y}{2}+\frac{z}{3}=1$; multiply by 6.
:::

**Set C — Application (6 questions)**

1. The area of the triangle with vertices $(1,1)$, $(4,5)$, $(7,2)$ is
   (a) 21 (b) 10.5 (c) 7 (d) 12
2. The circle through $(0,0)$, $(4,0)$ and $(0,6)$ has radius$^2$ equal to
   (a) 5 (b) 25 (c) 13 (d) 10
3. The radical axis of $x^2+y^2=9$ and $x^2+y^2-4x-6y+4=0$ is
   (a) $4x+6y-13=0$ (b) $4x+6y+13=0$ (c) $2x+3y-13=0$ (d) $4x-6y-13=0$
4. The tangent to $y^2=16x$ with slope 1 is
   (a) $x-y-4=0$ (b) $x-y+16=0$ (c) $x+y+4=0$ (d) $x-y+4=0$
5. The tangent of the acute angle between the lines $x^2-5xy+4y^2=0$ is
   (a) $5/3$ (b) $3/5$ (c) $3/4$ (d) $4/5$
6. The plane through $(1,2,3)$ parallel to $x+2y+3z=7$ is
   (a) $3x+2y+z=10$ (b) $x+2y+3z=7$ (c) $x+2y+3z=14$ (d) $x+2y+3z=6$

::: note Answers and explanations — Set C
**1.** (b) — $\frac{1}{2}|1(5-2)+4(2-1)+7(1-5)|=\frac{1}{2}|3+4-28|=10.5$.
**2.** (c) — a right angle at the origin, so the hypotenuse $(4,0)$–$(0,6)$ is a diameter: centre $(2,3)$, $r^2=4+9=13$.
**3.** (a) — $S_1-S_2=(x^2+y^2-9)-(x^2+y^2-4x-6y+4)=4x+6y-13$.
**4.** (d) — $a=4$, $m=1$: $y=x+\frac{a}{m}=x+4$.
**5.** (b) — $h=-\frac{5}{2}$, $a=1$, $b=4$: $\frac{2\sqrt{25/4-4}}{5}=\frac{2\cdot1.5}{5}=\frac{3}{5}$ (factors $(x-y)(x-4y)$, slopes $1,\frac{1}{4}$).
**6.** (c) — same normal $(1,2,3)$; $1+4+9=14$.
:::

**Group D — Model answers for long questions (10 marks each, for deeper revision)**

1. Find the distance from a point to a line, the angle between a pair of lines, and the tangent and tangent length for a circle. <span class="marks">[10]</span>
2. Find the foci, eccentricity and latus rectum of a parabola, ellipse and hyperbola, and solve problems in three dimensions. <span class="marks">[10]</span>

### Model answer D1: Lines and circles (10 marks)

**Introduction.** The distance of $(x_1,y_1)$ from $ax+by+c=0$ is $d=\frac{\lvert ax_1+by_1+c\rvert}{\sqrt{a^2+b^2}}$. For $(3,4)$ and $3x+4y-5=0$: $d=\frac{\lvert9+16-5\rvert}{5}=4$.

**Pair of lines.** The equation $ax^2+2hxy+by^2=0$ represents two lines through the origin, and the angle between them is $\tan\theta=\frac{2\sqrt{h^2-ab}}{\lvert a+b\rvert}$. For $2x^2+5xy+2y^2=0$: $a=b=2$, $h=\frac52$, so $\tan\theta=\frac{2\sqrt{6.25-4}}{4}=\frac{2(1.5)}{4}=0.75$, giving $\theta=36.87^\circ$. Also $2x^2+5xy+2y^2=(2x+y)(x+2y)$, so the lines are $y=-2x$ and $y=-\frac x2$, and the check $\tan\theta=\left|\frac{-2+\frac12}{1+1}\right|=0.75$ agrees.

**Circle $x^2+y^2-4x+6y-12=0$.**

1. Centre $(-g,-f)=(2,-3)$.
2. Radius $r=\sqrt{g^2+f^2-c}=\sqrt{4+9+12}=5$.
3. **Tangent at $(5,1)$** (the point lies on the circle since $9+16=25$): $(x-2)(5-2)+(y+3)(1+3)=25$, so $3x+4y=19$.
4. **Length of tangent from $(10,-3)$:** $\sqrt{S_1}=\sqrt{100+9-40-18-12}=\sqrt{39}=6.24$.
5. **Condition for tangency:** the perpendicular distance from the centre to the line equals the radius. For $3x+4y=19$: $\frac{\lvert6-12-19\rvert}{5}=5$ ✓.

| Result | Formula | Value |
|---|---|---|
| Distance to line | $\frac{\lvert ax_1+by_1+c\rvert}{\sqrt{a^2+b^2}}$ | $4$ |
| Angle of pair | $\frac{2\sqrt{h^2-ab}}{\lvert a+b\rvert}$ | $36.87^\circ$ |
| Radius | $\sqrt{g^2+f^2-c}$ | $5$ |
| Tangent length | $\sqrt{S_1}$ | $\sqrt{39}$ |

**Conclusion.** Standard formulae turn each geometric condition into a short calculation.

### Model answer D2: Conics and the plane (10 marks)

**Introduction.** A conic is the locus of a point whose distance from a **focus** is $e$ times its distance from the **directrix**: parabola ($e=1$), ellipse ($e<1$), hyperbola ($e>1$).

| Conic | Equation | Focus | $e$ | Latus rectum |
|---|---|---|---|---|
| Parabola | $y^2=8x$ | $(2,0)$; directrix $x=-2$ | $1$ | $8$ |
| Ellipse | $\frac{x^2}{25}+\frac{y^2}{9}=1$ | $(\pm4,0)$ | $\frac45$ | $\frac{2b^2}{a}=3.6$ |
| Hyperbola | $\frac{x^2}{16}-\frac{y^2}{9}=1$ | $(\pm5,0)$ | $\frac54$ | $\frac{2b^2}{a}=4.5$ |

**Working.** Ellipse: $a=5$, $b=3$, $c=\sqrt{a^2-b^2}=4$, $e=\frac ca=0.8$. Hyperbola: $a=4$, $b=3$, $c=\sqrt{a^2+b^2}=5$, $e=\frac54$, and the asymptotes are $y=\pm\frac34x$. A parabola $y^2=4ax$ with $4a=8$ has $a=2$. The sum of focal distances in an ellipse is $2a=10$.

**Space geometry.**

1. **Distance** between $(1,2,3)$ and $(4,6,15)$: $\sqrt{9+16+144}=\sqrt{169}=13$.
2. **Plane in intercept form:** the plane through $(1,0,0)$, $(0,2,0)$ and $(0,0,3)$ is $\frac x1+\frac y2+\frac z3=1$, i.e. $6x+3y+2z=6$.
3. **Distance of the origin from the plane:** $\frac{6}{\sqrt{36+9+4}}=\frac67$.
4. **Direction cosines** of a line satisfy $l^2+m^2+n^2=1$; for the join of the first two points the direction ratios are $(3,4,12)$, so the cosines are $\frac{3}{13},\frac{4}{13},\frac{12}{13}$.

**Conclusion.** Identify the conic from its equation, read off $a$, $b$, then calculate $c$, $e$ and the focus, and use intercepts or direction ratios in space.
