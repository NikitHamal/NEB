---
subject: Mathematics I
grade: BCA Semester 1
unit: 8
title: Vectors in Space, Lines and Planes
area: BCA 104 · Mathematics I · Unit 8
---

Three-dimensional geometry is the mathematics of games, graphics engines, robotics and CAD. Vectors describe positions, directions, lines and planes with simple algebra. This unit completes the course with the products of vectors and their geometry.

::: key What this unit gives you
- Vectors in $\mathbb{R}^{3}$: components, length, direction cosines, dot and cross products.
- Areas, volumes and the scalar triple product.
- Equations of lines and planes; distances and angles; intersections.
- Applications in graphics: normals, lighting, back-face culling.
:::

## 8.1 Vectors in three dimensions

A vector **a** = $(a_{1} ,\  a_{2} ,\  a_{3}) = a_{1}$***i*** + $a_{2}$***j*** + $a_{3}$***k***, with length |**a**| = $\sqrt{a_{1}^{2} + a_{2}^{2} + a_{3}^{2}}$. The vector from $P (x_{1} ,\  y_{1} ,\  z_{1})$ to $Q (x_{2} ,\  y_{2} ,\  z_{2})$ is $P Q = (x_{2} - x_{1} ,\  y_{2} - y_{1} ,\  z_{2} - z_{1})$. A **unit vector** has length 1: â = **a**/|**a**|. **Direction cosines** are $\cos \alpha = \frac{a_{1}}{|a|} ,\  \cos \beta = \frac{a_{2}}{|a|} ,\  \cos \gamma = \frac{a_{3}}{|a|}$, with $\cos^{2} \alpha + \cos^{2} \beta + \cos^{2} \gamma = 1$.

**Dot (scalar) product:** **$a \cdot b$** = $a_{1} b_{1} + a_{2} b_{2} + a_{3} b_{3} = |a| |b| \cos \theta$. It is zero iff the vectors are perpendicular; it gives angles, projections (scalar projection of a on *b* = a·b/|b|) and work $(W = F \cdot d)$.

**Cross (vector) product:** **$a \times b$** = $(a_{2} b_{3} - a_{3} b_{2} ,\  a_{3} b_{1} - a_{1} b_{3} ,\  a_{1} b_{2} - a_{2} b_{1})$, written as the determinant of $\begin{bmatrix} i & j & k \\ a_{1} & a_{2} & a_{3} \\ b_{1} & b_{2} & b_{3} \end{bmatrix}$. Its direction is perpendicular to both a and *b* (right-hand rule); its length is **$|a| |b| \sin \theta$**, the **area of the parallelogram** spanned by a and *b*. $a \times b = - (b \times a) ;\  a \times a = 0$; the cross product is *not* commutative or associative.

::: example Worked example

$$a = (1 ,\  2 ,\  3) ,\  b = (4 ,\  - 5 ,\  6)$$

**$a \cdot b$** = $4 - 10 + 18$ = **12**; $|a| = \sqrt{14} \approx 3.742 ,\  |b| = \sqrt{77} \approx 8.775 ;\  \cos \theta = \frac{12}{\sqrt{1078}} = 0.3655$ ⇒ **$\theta \approx 68.6 ^{\circ}$**.

**$a \times b$** = (2·6 − 3·(−5), 3·4 − 1·6, 1·(−5) − 2·4) = **(27, 6, −13)**. Check perpendicularity: $(27 ,\  6 ,\  - 13) \cdot a = 27 + 12 - 39 = 0$ ✓ and · $b = 108 - 30 - 78 = 0$ ✓.

**Area of the triangle** with sides a and *b* from a common vertex = $\frac{1}{2}$ |a × b| = $\frac{1}{2} \sqrt{729 + 36 + 169} = \frac{1}{2} \sqrt{934}$ ≈ **15.28**.
:::

**Scalar triple product** $[a ,\  b ,\  c] = a \cdot (b \times c) = \det$ of the $3 \times 3$ matrix with rows $a ,\  b ,\  c$. Its absolute value is the **volume of the parallelepiped** on $a ,\  b ,\  c$; the volume of a tetrahedron is one sixth of that. The three vectors are **coplanar** iff the triple product is 0. Example: $a = (1 ,\  0 ,\  0) ,\  b = (1 ,\  1 ,\  0) ,\  c = (1 ,\  1 ,\  1)$: $\det = 1$, so the volume is 1 and the tetrahedron has volume $\frac{1}{6}$.

## 8.2 Lines in space

A line through the point $P_{0} = (x_{0} ,\  y_{0} ,\  z_{0})$ with direction ***d*** = $(l ,\  m ,\  n)$:

- **Vector form:** ***r*** = **$r_{0}$** + *t****d***.
- **Parametric:** $x = x_{0}$ + lt, $y = y_{0} + m t ,\  z = z_{0} + n t$.
- **Symmetric:** $\frac{(x - x_{0})}{l} = \frac{(y - y_{0})}{m} = \frac{(z - z_{0})}{n}$.

Through two points A and B, take $d = B - A$. **Angle between two lines** = angle between their direction vectors. Lines are parallel if their directions are proportional; perpendicular if $d_{1} \cdot d_{2} = 0$. In $3 - D$ two lines may also be **skew** (neither parallel nor intersecting).

**Shortest distance from a point P to a line** (through A, direction *d*): **|AP × d| / $|d|$**. **Distance between skew lines** through $A_{1} ,\  A_{2}$ with directions $d_{1} ,\  d_{2}$: $\frac{|(A_{2} - A_{1}) \cdot (d_{1} \times d_{2})|}{|d_{1} \times d_{2}|}$.

::: example Worked example
Line L: $r = (1 ,\  2 ,\  3) + t (2 ,\  - 1 ,\  0)$. Distance of the point $P = ( 3 ,\  1$, 3) from L: $A P = (2 ,\  - 1 ,\  0) ,\  d = (2 ,\  - 1 ,\  0) ;\  A P \times d$ = **0**, so the distance is 0, and P lies on $L (t = 1)$. For $P = (1 ,\  2 ,\  5)$: $A P = (0 ,\  0 ,\  2) ;\  A P \times d$ = (0·0 − $2 (- 1)$, 2·2 − 0·0, $0 ) = ( 2 ,\  4 ,\  0$); |AP × d| = $\sqrt{20} ,\  |d| = \sqrt{5}$, distance = $\frac{\sqrt{20}}{\sqrt{5}}$ = **2**.
:::

## 8.3 Planes

A plane through $P_{0}$ with **normal** vector $n = (A ,\  B ,\  C)$: **$n \cdot (r - r_{0}) = 0$**, i.e. **Ax + By + Cz = D** with $D = n \cdot r_{0}$. Through three points A, B, C: the normal is $n = (B - A) \times (C - A)$.

::: example Worked example
The plane through (1, 0, 0), (0, 1, 0), (0, 0, 1): $A B = (- 1 ,\  1 ,\  0) ,\  A C = (- 1 ,\  0 ,\  1) ;\  n = A B \times A C$ = (1·1 − 0·0, 0·(−1) − (−1)·1, (−1)·0 − 1·(−1)) = (1, 1, 1). Equation: **$x + y + z = 1$** (check each point ✓).
:::

**Distance from a point $(x_{1} ,\  y_{1} ,\  z_{1})$ to the plane Ax + By + Cz = D:** **$\mid A x_{1} + B y_{1} + C z_{1}$ − D| / $\sqrt{A^{2} + B^{2} + C^{2}}$**. Example: the point (1, 2, 3) and the plane $2 x - y + 2 z = 5$: |2 − $2 + 6 - 5 \mid / \sqrt{9}$ = **$\frac{1}{3}$**.

**Angle between two planes** = angle between their normals: $\cos \theta = \frac{|n_{1} \cdot n_{2}|}{(|n_{1}| |n_{2}|)}$. Planes are parallel if the normals are proportional, perpendicular if $n_{1} \cdot n_{2} = 0$. **Intersection of two planes** is a line with direction $n_{1} \times n_{2}$. **Line and plane:** substitute the parametric line into the plane equation; one solution for *t* gives the intersection point, no solution means parallel, any *t* means the line lies in the plane. Example: line $(t ,\  2 t ,\  3 t)$ meets $x + y + z = 12$ when $6 t = 12$, so $t = 2$ and the point is (2, 4, 6).

Three planes meet at a point, along a line, or not at all: this is exactly the $3 \times 3$ linear system of Unit 4 (rank 3, rank 2 consistent, or inconsistent).

## 8.4 Spheres and applications

A **sphere** with centre $(a ,\  b ,\  c)$ and radius *r*: $(x - a)^{2} + (y - b)^{2} + (z - c)^{2} = r^{2}$. Example: $x^{2} + y^{2} + z^{2} - 2 x + 4 y - 6 z = 11$ becomes $(x - 1)^{2} + (y + 2)^{2} + (z - 3)^{2} = 11 + 1 + 4 + 9 = 25$, so the centre is (1, −2, 3) and the radius is **5**.

**In computer graphics:**
- The **normal** to a triangle $(v_{1} ,\  v_{2} ,\  v_{3})$ is $(v_{2} - v_{1}) \times (v_{3} - v_{1})$; normalise it for lighting.
- **Diffuse lighting:** brightness ∝ $\max ( 0$, n̂ · l̂), where l̂ is the unit vector towards the light (Lambert's law): a surface facing the light $(\theta = 0)$ gets full brightness, at $60 ^{\circ}$ it gets $\cos 60 ^{\circ} = 0.5$, at $90 ^{\circ}$ it gets 0.
- **Back-face culling:** skip a triangle whose normal has a non-positive dot product with the view direction.
- **Reflection:** $r = d - 2 ( d$ · n̂) n̂ for incoming direction *d* and unit normal n̂.
- **Ray–plane intersection** (ray tracing): $t = \frac{D - n \cdot o}{n \cdot d}$.
- **Physics:** work $W = F \cdot d$; torque $\tau = r \times F$; magnetic force $F = q v \times B$.

## 8.5 A plane, its normal and the distance to a point

A plane is fixed by one point $P_{0}$ and one **normal vector *n*** that is perpendicular to every direction inside the plane. A point X lies on the plane exactly when $(X - P_{0}) \cdot n = 0$, which expands to $a x$ + by + $c z = d$ with $n = (a ,\  b ,\  c)$. The same normal gives the distance from any point Q to the plane, *d* = |(Q − $P_{0}$) · n| ÷ $|n|$ (Figure 8.1). In graphics, the normal tells which way a surface faces and therefore how bright it looks under a lamp.

```svgfig label="8.1" caption="A plane with normal *n* at the point P0. The foot F is the closest point of the plane to Q; the length of QF is the distance from Q to the plane, which equals the projection of (Q - P0) on the unit normal."
f = Fig(580, 220)
f.poly([(130, 180), (390, 180), (470, 130), (210, 130)], fill=BLUE, stroke=NAVY)
f.text(150, 196, "plane  ax + by + cz = d", size=11, color=NAVY, bold=True, anchor="start")
f.circle(300, 155, 4.5, fill=NAVY, stroke=NAVY)
f.text(285, 172, "P0", size=11, color=NAVY, bold=True)
f.arrow([(300, 155), (300, 55)], color=RED, sw=2.4)
f.text(312, 70, "n (normal)", size=11, color=RED, bold=True, anchor="start")
f.circle(390, 150, 4, fill=TEAL, stroke=TEAL)
f.text(400, 160, "F", size=11, color=TEAL, bold=True, anchor="start")
f.circle(390, 50, 4.5, fill=AMBER, stroke=AMBER)
f.text(402, 48, "Q", size=11, color=AMBER, bold=True, anchor="start")
f.line(390, 54, 390, 146, color=AMBER, sw=1.8, dash=True)
f.text(480, 98, "d = |(Q - P0) . n| / |n|", size=11, color=NAVY, bold=True, anchor="middle")
f.arrow([(300, 155), (386, 151)], color=SLATE, sw=1.4)
```

## 8.6 Eight uses of vectors in space

1. **3D graphics and games.** Every object is a mesh of triangles with normal vectors. The dot product of the normal with the light direction gives the brightness of each triangle. A phone game does millions of these products per second.
2. **GPS and surveying.** A position in space is a vector, and distances between points are vector lengths. Survey teams on mountain routes compute heights and slopes with vector methods. Everest height measurements combine many such vectors.
3. **Physics and work.** Work done by a force is the dot product $F \cdot d$; torque is the cross product $r \times F$. Engineers use them to size motors and cranes. A tractor pulling at an angle does less useful work, as the cosine shows.
4. **Aviation and navigation.** Velocity of an aircraft is the sum of its air velocity and the wind vector. Pilots compute heading and ground speed by vector addition. Flights to Lukla depend on exactly this calculation.
5. **Robotics and CNC machines.** A tool path is a series of lines in space given by a point and a direction. The machine follows the parametric equation of each line. 3D printers work the same way layer by layer.
6. **Collision detection.** To know whether a ball hits a wall, the program finds where a line meets a plane or computes the distance to it. A game engine does this for every object at every frame.
7. **Architecture and structures.** Forces in a truss are vectors that must sum to zero at each joint. Planes describe roofs, walls and slopes. Earthquake-resistant design checks these vector balances.
8. **Computer vision and AR.** An augmented-reality $a p p$ finds a flat surface in the camera image (a plane) and places a virtual object on it using the normal. The camera's position and direction are vectors in space.

```photogrid label="8.1" cols="2" ratio="1.2" caption="A landing is a line meeting a plane. (a) A Buddha Air ATR 42 landing at Pokhara. (b) Treat the runway as the plane $z = 0$ and the aeroplane as the point ($- 5000 ,\  300 ,\  300 ) m ( x$ along the runway, *y* sideways, *z* height) moving with velocity $\frac{(50 ,\  - 3 ,\  - 2.6) m}{s}$. Its path is $r (t) = (- 5000 + 50 t ,\  300 - 3 t ,\  300 - 2.6 t)$. The path meets the plane when $300 - 2.6 t = 0$, that is $t = 115.4 s$, at the point (769, -46, 0): 769 *m* beyond the origin mark and 46 *m* to one side. The speed is $|v| = \mathrm{sqrt} (50^{2} + 3^{2} + 2.6^{2}) = \frac{50.2 m}{s}$ (180.6 km/h) and the descent angle is arctan(2.6 / $50.09 ) = 2.97$ degrees, close to the 3 degree glide slope pilots follow. The numbers are illustrative, not from a flight record."
@ photo id="bcamath/atr42" cap="ATR 42 landing at Pokhara"
fit 1.2
focus 0.5 0.55
@ svg cap="Line r(t) meets the runway plane z = 0"
import math
x0, y0, z0 = -5000.0, 300.0, 300.0; vx, vy, vz = 50.0, -3.0, -2.6
t = -z0 / vz; X = x0 + vx * t; Y = y0 + vy * t
assert round(t, 1) == 115.4 and round(X) == 769 and round(Y) == -46
sp = math.sqrt(vx ** 2 + vy ** 2 + vz ** 2); ang = math.degrees(math.atan2(-vz, math.hypot(vx, vy)))
assert round(sp, 1) == 50.2 and round(sp * 3.6, 1) == 180.6 and round(ang, 2) == 2.97
f = Fig(300, 240)
sx = 250 / 6000.0; zx = 0.28; gx = 20; gy = 150
px = lambda x: gx + (x + 5000) * sx
f.line(gx, gy, 280, gy, color=SLATE, sw=2.4)
f.box(px(0) - 1, gy - 1, 2, 12, "", fill=AMBER, stroke=AMBER, r=0)
f.arrow([(px(x0), gy - z0 * zx), (px(X), gy)], color=TEAL, sw=2.2)
f.circle(px(x0), gy - z0 * zx, 5, fill=NAVY, stroke=NAVY)
f.circle(px(X), gy, 5, fill=RED, stroke=RED)
f.text(px(x0) + 6, gy - z0 * zx - 10, "start (-5000, 300, 300)", size=10.5, color=NAVY, bold=True, anchor="start")
f.text(px(0), gy + 26, "mark x = 0", size=10.5, color=AMBER, bold=True)
f.text(px(X) + 4, gy - 12, "touchdown", size=10.5, color=RED, bold=True)
f.text(150, 192, "side view (height drawn 4x larger than length)", size=10.5, color=SLATE)
f.text(150, 210, "t = 115.4 s, point (769, -46, 0) m", size=10.5, color=TEAL, bold=True)
f.text(150, 228, "speed 50.2 m/s, descent angle 2.97 degrees", size=10.5, color=NAVY, bold=True)
```

```photogrid label="8.2" cols="2" ratio="1.2" caption="Planes, normals and areas on a pyramid. (a) The Great Pyramid of Giza. (b) Take the original base 230.3 *m* by 230.3 *m* and height 146.6 *m*, with the base centred at the origin. A face passes through $A = (115.15 ,\  - 115.15 ,\  0) ,\  B = ( 115.15 ,\  115.15$, 0) and the apex $C = (0 ,\  0 ,\  146.6)$. The normal is $n = A B x$ AC = (33,762, 0, 26,519), whose length is 42,931.7. The face leans at $\arccos \left( \frac{n_{z}}{|n|} \right) = 51.85$ degrees to the ground, the same as arctan(146.6 / 115.15). Half the length of the cross product is the face area, 21,466 square metres; four faces cover 85,863 square metres. The volume $\left( \frac{1}{3} \right) x$ base area *x* height is 2,591,795 cubic metres, and the centre of the base is 90.6 *m* from each face plane."
@ photo id="bcamath/pyramid" cap="The Great Pyramid of Giza"
fit 1.2
focus 0.5 0.5
@ svg cap="Face normal, slope and area of the pyramid"
import numpy as np, math
b = 230.3; h = 146.6
A = np.array([b / 2, -b / 2, 0]); B = np.array([b / 2, b / 2, 0]); C = np.array([0, 0, h])
n = np.cross(B - A, C - A); L = np.linalg.norm(n)
phi = math.degrees(math.acos(n[2] / L))
assert np.allclose(n, [33761.98, 0, 26519.045], atol=0.01) and round(L, 1) == 42931.7
assert round(phi, 2) == 51.85 == round(math.degrees(math.atan(h / (b / 2))), 2)
assert round(L / 2) == 21466 and round(2 * L) == 85863 and round(b * b * h / 3) == 2591795
assert round(abs(n @ (-A)) / L, 1) == 90.6
f = Fig(300, 240)
x0, x1, ax = 30, 250, 140; yb = 150; yt = 150 - 146.6 / 115.15 * 110
f.poly([(x0, yb), (x1, yb), (ax, yt)], fill=SAND, stroke=AMBER, sw=2)
mx, my = (x1 + ax) / 2, (yb + yt) / 2
nx, ny = n[0] / L, n[2] / L
f.arrow([(mx, my), (mx + nx * 46, my - ny * 46)], color=RED, sw=2.4)
f.text(mx + nx * 46 + 4, my - ny * 46 - 6, "n", size=12, color=RED, bold=True, anchor="start")
f.text(x1 - 34, yb - 8, "51.85 deg", size=10.5, color=NAVY, bold=True)
f.text(ax - 12, yt + 14, "C", size=11, color=AMBER, bold=True)
f.line(ax, yb, ax, yt, color=SLATE, sw=1, dash=True)
f.text(ax - 28, (yb + yt) / 2, "146.6 m", size=10.5, color=SLATE, bold=True)
f.text(ax, yb + 16, "230.3 m", size=10.5, color=SLATE, bold=True)
f.text(150, 192, "n = AB x AC = (33,762, 0, 26,519), |n| = 42,931.7", size=10.5, color=RED, bold=True)
f.text(150, 210, "face 21,466 m2; four faces 85,863 m2", size=10.5, color=NAVY, bold=True)
f.text(150, 228, "volume 2,591,795 m3; centre to face 90.6 m", size=10.5, color=SLATE)
```

## Formula and fact sheet

- $a \cdot b = \sum a_{i} b_{i}$ = |a||b|cos $\theta ;\  a \times b$ has length $|a| |b| \sin \theta$, direction perpendicular.
- Triangle area = $\frac{1}{2} \mid a$ × b|; parallelepiped volume = |a · (*b* × c)|; coplanar iff the triple product is 0.
- Line: $r = r_{0} + t d$. Distance point–line = |AP × $d |/| d \mid$.
- Plane: $n \cdot r = D$. Distance point–plane = |n · $P - D |/| n \mid$. Planes meet along direction $n_{1} \times n_{2}$.
- Sphere: $(x - a)^{2} + (y - b)^{2} + (z - c)^{2} = r^{2}$.
- Reflection $r = d - 2 ( d$ · n̂)n̂.

## Chapter summary

- The dot product measures alignment and angles; the cross product measures area and gives normals.
- The triple product measures volume and tests coplanarity.
- Lines and planes have vector, parametric and Cartesian forms, with simple distance and angle formulas.
- The same operations drive lighting, culling and reflection in graphics, and torque and work in physics.

## Practice

1. For $a = (2 ,\  - 1 ,\  3) ,\  b = (1 ,\  4 ,\  - 2)$ find $a \cdot b ,\  a \times b$, the angle between them and the area of the parallelogram.
2. Find the volume of the parallelepiped with edges (1, 2, 3), (0, 1, 4), (5, 6, 0).
3. Are the vectors (1, 2, 3), (2, 4, 6) and (1, 0, 1) coplanar? Is (1, 0, 0), (0, 1, 0), (0, 0, 1) coplanar?
4. Write the equation of the line through $A ( 1 ,\  2$, 3) and $B ( 3 ,\  2$, 1) and find where it meets the plane $x + y + z = 10$.
5. Find the plane through (1, 1, 1), (2, 0, 1) and (0, 1, 3).
6. Find the distance from (2, 3, 4) to the plane $x + 2 y + 2 z = 3$.
7. Find the angle between the planes $x + y + z = 1$ and $x - y + 2 z = 3$.
8. Find the centre and radius of $x^{2} + y^{2} + z^{2} - 4 x + 6 y - 2 z - 2 = 0$.
9. A light shines along direction l̂ = (0, 0, 1) at a surface with unit normal (0.6, 0, 0.8). Find the diffuse brightness factor.
10. Find the reflection of $d = ( 1 ,\  - 1$, 0) off a surface with unit normal (0, 1, 0).

::: note Answers and worked solutions
**1.** $a \cdot b = 2 - 4 - 6$ = **−8**. $a \times b = ( (- 1) (- 2)$ − 3·4, 3·1 − 2·(−2), 2·4 − (−1)·1) = $(2 - 12 ,\  3 + 4 ,\  8 + 1)$ = **(−10, 7, 9)**. $|a| = \sqrt{14} ,\  |b| = \sqrt{21} ;\  \cos \theta = - \frac{8}{\sqrt{294}} = - 0.4666$ ⇒ **$\theta \approx 117.8 ^{\circ}$**. Area = |a × b| = $\sqrt{100 + 49 + 81}$ = **$\sqrt{230} \approx 15.17$**.

**2.** $\det \begin{bmatrix} 1 & 2 & 3 \\ 0 & 1 & 4 \\ 5 & 6 & 0 \end{bmatrix} = 1$ (this matrix has $\det 1$, Unit 3): volume **1**.

**3.** First set: the triple product is 0 because the second vector is twice the first, so **coplanar**. Second set: $\det = 1 \neq 0$, so **not** coplanar.

**4.** $d = B - A = (2 ,\  0 ,\  - 2)$. Line: $(1 + 2 t ,\  2 ,\  3 - 2 t)$. Substituting: $(1 + 2 t) + 2 + (3 - 2 t) = 6$, which is never 10, so the line is **parallel** to the plane and never meets it.

**5.** $u = (1 ,\  - 1 ,\  0) ,\  v = (- 1 ,\  0 ,\  2) ;\  n = u \times v = ( (- 1) (2)$ − 0·0, 0·(−1) − 1·2, 1·0 − $(- 1) (- 1) ) = ( - 2 ,\  - 2 ,\  - 1$) ⇒ use (2, 2, 1). Plane: $2 x + 2 y + z = 5$ (check (1,1,1): 5 ✓; (2,0,1): 5 ✓; (0,1,3): 5 ✓).

**6.** |2 + $6 + 8 - 3 \mid / \sqrt{1 + 4 + 4} = \frac{13}{3}$ ≈ **4.33**.

**7.** $n_{1} = (1 ,\  1 ,\  1) ,\  n_{2} = (1 ,\  - 1 ,\  2)$: $n_{1} \cdot n_{2} = 2 ;\  |n_{1}| = \sqrt{3} ,\  |n_{2}| = \sqrt{6} ;\  \cos \theta = \frac{2}{\sqrt{18}} = 0.4714$ ⇒ **$\theta \approx 61.9 ^{\circ}$**.

**8.** $(x - 2)^{2} + (y + 3)^{2} + (z - 1)^{2} = 2 + 4 + 9 + 1 = 16$: centre **(2, −3, 1)**, radius **4**.

**9.** n̂ · l̂ = 0.8, so brightness factor **0.8** (surface faces the light at about $36.9 ^{\circ}$).

**10.** *d* · n̂ = −1; r = d − 2(−1)n̂ = (1, −1, 0) + 2(0, 1, 0) = **(1, 1, 0)** (the vertical component flips, as a ball bouncing off a floor).
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Find the equation of the line through $A ( 1 ,\  2$, 3) and $B ( 4 ,\  6$, 8) in vector, parametric and symmetric form, and find where it meets the plane $z = 0$.**

*Introduction.* A line in space is fixed by a point and a direction vector.

*Direction.* $A B = B - A = (3 ,\  4 ,\  5)$.

*Forms.* Vector form: $r = (1 ,\  2 ,\  3) + t (3 ,\  4 ,\  5)$. Parametric: $x = 1 + 3 t ,\  y = 2 + 4 t ,\  z = 3 + 5 t$. Symmetric: $(x - 1) \div 3 = (y - 2) \div 4 = (z - 3) \div 5$.

*Intersection with $z = 0 . \ast 3 + 5 t = 0$ gives $t = - \frac{3}{5}$. Then $x = 1 - \frac{9}{5} = - \frac{4}{5}$ and $y = 2 - \frac{12}{5} = - \frac{2}{5}$, so the line meets the plane $z = 0$ at $\left( - \frac{4}{5} ,\  - \frac{2}{5} ,\  0 \right)$.

*Check.* B is reached at $t = 1$: (4, 6, 8). *Conclusion.* The line is $r = (1 ,\  2 ,\  3) + t (3 ,\  4 ,\  5)$, meeting $z = 0$ at (−0.8, −0.4, 0).

**Q2 (10 marks). Find the equation of the plane through $P (1 ,\  0 ,\  0) ,\  Q ( 0 ,\  2$, 0) and $R (0 ,\  0 ,\  3)$, the distance of (1, 1, 1) from it and the area of triangle PQR. State the properties of the dot and cross products used.**

*Introduction.* Dot and cross products give the angle, the area and the normal that define a plane. They are the main tools of vectors in space.

*Dot and cross product.*

1. **Dot product.** $a \cdot b = |a| |b| \cos \theta = a_{1} b_{1} + a_{2} b_{2} + a_{3} b_{3}$. It is zero exactly when a and *b* are perpendicular.
2. **Cross product.** $a \times b$ is perpendicular to both a and *b*, with length $|a| |b| \sin \theta$ equal to the area of the parallelogram they span.
3. **Direction rule.** $a \times b = - (b \times a)$, so order matters.

*Step 1: two vectors in the plane.* $P Q = ( - 1 ,\  2$, 0) and $P R = (- 1 ,\  0 ,\  3)$.

*Step 2: normal.* $n = P Q \times P R$ = (2·3 − 0·0, 0·(−1) − (−1)·3, (−1)·0 − 2·(−1)) = (6, 3, 2).

*Step 3: equation.* $6 (x - 1) + 3 y + 2 z = 0$, so **$6 x + 3 y + 2 z = 6$**. Check Q: $6 \times 0 + 3 \times 2 = 6$, and R: $2 \times 3 = 6$.

*Step 4: distance of $(1 ,\  1 ,\  1) . \ast$ |6 + $3 + 2$ − 6| ÷ $\sqrt{36 + 9 + 4} = 5 \div 7 \approx 0.714$.

*Step 5: area of triangle PQR.* $\frac{1}{2} |n| = \frac{1}{2} \times 7$ = **3.5** square units.

| Quantity | Formula | Value here |
|---|---|---|
| Normal | $P Q \times P R$ | (6, 3, 2) |
| Plane | $n \cdot (X - P) = 0$ | $6 x + 3 y + 2 z = 6$ |
| Distance | $\mid a x_{0} + b y_{0} + c z_{0}$ − d\| ÷ $|n|$ | $\frac{5}{7}$ |
| Triangle area | $\frac{1}{2}$ \|PQ × PR\| | 3.5 |

*Conclusion.* The cross product gives the plane and the area, and the dot product gives the distance; the plane is $6 x + 3 y + 2 z = 6$, the point is $\frac{5}{7}$ away and the triangle has area 3.5.
