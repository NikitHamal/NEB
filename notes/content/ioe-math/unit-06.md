---
subject: Mathematics
grade: IOE
unit: 6
title: Vectors and their Products
hours: 3
area: Mathematics
---

Vectors carry about **3 questions** (our estimate). The booklet's model question — the projection of $\vec b=2\hat i+3\hat j-2\hat k$ on $\vec a=\hat i+2\hat j+3\hat k$ — is typical: a dot product, a cross product, or a scalar triple product, computed from components. The whole chapter reduces to four formulas used fluently.

::: key What the paper asks from this chapter
- Components, magnitude, unit vector, section formula, collinearity.
- Dot product: $\vec a\cdot\vec b=ab\cos\theta$; projection of $\vec b$ on $\vec a$ is $\dfrac{\vec a\cdot\vec b}{|\vec a|}$.
- Cross product: $|\vec a\times\vec b|=ab\sin\theta$, area of a triangle $\frac{1}{2}|\vec a\times\vec b|$.
- Scalar triple product: volume, coplanarity ($[\vec a\,\vec b\,\vec c]=0$).
- Linear dependence: two vectors are dependent iff parallel; three iff coplanar.
:::

## 6.1 Vectors in plane and space, algebra, linear combination, dependence

A vector has magnitude and direction. For $\vec a=a_1\hat i+a_2\hat j+a_3\hat k$: $|\vec a|=\sqrt{a_1^2+a_2^2+a_3^2}$ and the **unit vector** is $\hat a=\vec a/|\vec a|$. Direction cosines $\frac{a_1}{|\vec a|},\frac{a_2}{|\vec a|},\frac{a_3}{|\vec a|}$. The vector $\overrightarrow{AB}=\vec b-\vec a$ (head minus tail).

- Triangle law: $\overrightarrow{AB}+\overrightarrow{BC}=\overrightarrow{AC}$; the parallelogram law; $|\vec a\pm\vec b|^2=a^2+b^2\pm2\vec a\cdot\vec b$.
- **Section formula:** point dividing $AB$ in the ratio $m:n$ internally is $\dfrac{m\vec b+n\vec a}{m+n}$ (externally $\dfrac{m\vec b-n\vec a}{m-n}$); midpoint $\frac{\vec a+\vec b}{2}$; centroid $\frac{\vec a+\vec b+\vec c}{3}$.
- **Collinear points** $A,B,C$: $\overrightarrow{AC}=k\,\overrightarrow{AB}$.
- **Linear combination:** $\vec r=x\vec a+y\vec b+z\vec c$. A set is **linearly dependent** if some non-trivial combination is zero: two vectors iff parallel; three iff coplanar ($[\vec a\,\vec b\,\vec c]=0$); any four in space always. Three non-coplanar vectors form a basis of space.

## 6.2 Product of two vectors, scalar and vector product, scalar triple product

### Scalar (dot) product

$\vec a\cdot\vec b=ab\cos\theta=a_1b_1+a_2b_2+a_3b_3$; commutative and distributive. $\hat i\cdot\hat i=1$, $\hat i\cdot\hat j=0$. $\vec a\cdot\vec a=|\vec a|^2$. **Perpendicular iff $\vec a\cdot\vec b=0$.**
$\cos\theta=\dfrac{\vec a\cdot\vec b}{|\vec a||\vec b|}$. **Projection** of $\vec b$ on $\vec a$: $\dfrac{\vec a\cdot\vec b}{|\vec a|}$ (a scalar); the vector component is that times $\hat a$. **Work** $=\vec F\cdot\vec d$. $(\vec a+\vec b)\cdot(\vec a-\vec b)=a^2-b^2$.

### Vector (cross) product

$\vec a\times\vec b=ab\sin\theta\,\hat n$ (right-hand rule), anticommutative; $\hat i\times\hat j=\hat k$, $\hat j\times\hat k=\hat i$, $\hat k\times\hat i=\hat j$.
$$\vec a\times\vec b=(det | \hat i&\hat j&\hat k ; a_1&a_2&a_3 ; b_1&b_2&b_3 |).$$
$|\vec a\times\vec b|^2=a^2b^2-(\vec a\cdot\vec b)^2$ (Lagrange). **Parallel iff $\vec a\times\vec b=\vec 0$.** Area of a parallelogram with sides $\vec a,\vec b$ is $|\vec a\times\vec b|$; of the triangle, half. A unit vector perpendicular to both: $\pm\dfrac{\vec a\times\vec b}{|\vec a\times\vec b|}$. Moment of a force: $\vec r\times\vec F$.

### Triple products

$[\vec a\,\vec b\,\vec c]=\vec a\cdot(\vec b\times\vec c)=$ the 3×3 determinant of components; cyclic invariant, changes sign when two vectors swap. **Volume** of the parallelepiped $=|[\vec a\,\vec b\,\vec c]|$; tetrahedron $=\frac{1}{6}|[\vec a\,\vec b\,\vec c]|$. **Coplanar iff $[\vec a\,\vec b\,\vec c]=0$.** Vector triple product: $\vec a\times(\vec b\times\vec c)=\vec b(\vec a\cdot\vec c)-\vec c(\vec a\cdot\vec b)$ ("BAC minus CAB").

::: caution
The dot product is a **scalar**, the cross product a **vector**. $\vec a\times(\vec b\times\vec c)\ne(\vec a\times\vec b)\times\vec c$. The projection can be negative.
:::

```photogrid label="6.1" cols="2" ratio="1.2" caption="Adding vectors. (a) In a tug of war the rope tension is a vector: the pull has a size and a direction, and the result depends on both. (b) Three ropes tied to a ring pull with 120 N at 0 degrees, 100 N at 120 degrees and 80 N at 240 degrees. Adding components gives Rx = 30 N and Ry = 17.32 N, so the resultant has magnitude 34.64 N at 30 degrees. Drawn head to tail, the three forces and the resultant form a closed polygon. A fourth force of 34.64 N at 210 degrees would give equilibrium. Any three vectors in a plane are linearly dependent."
@ photo id="ioemath/tug" cap="Tug of war: each team pulls with a force that has a size and a direction"
fit 1.2
focus 0.5 0.5
@ svg cap="Resultant of 120 N, 100 N and 80 N at 120 degrees spacing"
import math
F = [(120, 0), (100, 120), (80, 240)]
v = [(m * math.cos(math.radians(a)), m * math.sin(math.radians(a))) for m, a in F]
rx = sum(a for a, b in v); ry = sum(b for a, b in v)
mag = math.hypot(rx, ry); ang = math.degrees(math.atan2(ry, rx))
assert abs(rx - 30) < 1e-9 and abs(ry - 10 * math.sqrt(3)) < 1e-9 and abs(mag - 34.641) < 1e-3 and abs(ang - 30) < 1e-9
import itertools
d = [[v[i][0], v[i][1], 1] for i in range(3)]
det = d[0][0] * (d[1][1] - d[2][1]) - d[0][1] * (d[1][0] - d[2][0]) + (d[1][0] * d[2][1] - d[1][1] * d[2][0])
facts = dict(rx="%.0f" % rx, ry="%.2f" % ry, mag="%.2f" % mag, ang="%.0f" % ang, opp="%.0f" % (ang + 180))
f = Fig(300, 236)
f.text(150, 14, "forces drawn to scale, head to tail", size=10.5, color=NAVY, bold=True)
s = 1.6; ox, oy = 40, 172
pt = [(ox, oy)]
for a, b in v: pt.append((pt[-1][0] + a * s, pt[-1][1] - b * s))
cols = [NAVY, AMBER, TEAL]; names = ["F1 120 N", "F2 100 N", "F3 80 N"]
for i in range(3):
    f.arrow([pt[i], pt[i + 1]], color=cols[i], sw=2)
f.arrow([pt[0], pt[3]], color=RED, sw=2.4)
f.text(pt[0][0] + 96, pt[0][1] + 14, names[0], size=10.5, color=NAVY, bold=True)
f.text((pt[1][0] + pt[2][0]) / 2 + 36, (pt[1][1] + pt[2][1]) / 2, names[1], size=10.5, color=AMBER, bold=True)
f.text((pt[2][0] + pt[3][0]) / 2 - 38, (pt[2][1] + pt[3][1]) / 2, names[2], size=10.5, color=TEAL, bold=True)
f.text(pt[0][0] + 30, pt[0][1] - 24, "R", size=12, color=RED, bold=True)
f.text(150, 204, "Rx = %.0f N,  Ry = %.2f N" % (rx, ry), size=10.5, color=SLATE, bold=True)
f.text(150, 221, "|R| = %.2f N at %.0f degrees" % (mag, ang), size=10.5, color=RED, bold=True)
```

```photogrid label="6.2" cols="2" ratio="1.2" caption="The vector product. (a) A torque wrench measures the turning effect of a force, which is the vector product tau = r x F, with magnitude r F sin(theta). (b) For a handle length r = 0.40 m and a force F = 150 N at 60 degrees to the handle, the cross product of the vectors r = (0.40, 0, 0) and F = 150 (cos 60, sin 60, 0) is (0, 0, 51.96), so the torque is 51.96 N m along the axis of the bolt. The check r . tau = 0 and F . tau = 0 confirms that the result is perpendicular to both vectors. The torque is greatest at 90 degrees (60 N m) and zero at 0 and 180 degrees."
@ photo id="ioemath/wrench" cap="A click torque wrench: turning effect equals r cross F"
fit 1.2
focus 0.5 0.5
@ svg cap="Torque of a 150 N push on a 0.40 m handle vs angle"
import math
r = (0.40, 0, 0)
cross = lambda a, b: (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
dot = lambda a, b: sum(x * y for x, y in zip(a, b))
Fv = lambda th: (150 * math.cos(math.radians(th)), 150 * math.sin(math.radians(th)), 0)
tau = cross(r, Fv(60))
assert abs(tau[2] - 0.4 * 150 * math.sin(math.radians(60))) < 1e-9 and abs(dot(r, tau)) < 1e-9 and abs(dot(Fv(60), tau)) < 1e-9
angs = [0, 30, 60, 90, 120, 150, 180]
val = [abs(cross(r, Fv(a))[2]) for a in angs]
assert max(val) == val[3] and abs(val[3] - 60) < 1e-9 and val[0] < 1e-9 and val[-1] < 1e-9
facts = dict(tz="%.2f" % tau[2], tmax="%.0f" % val[3])
f = Fig(300, 236)
f.text(150, 14, "torque = 0.40 x 150 x sin(theta)  (N m)", size=10.5, color=NAVY, bold=True)
base = 168
for i, (a, v_) in enumerate(zip(angs, val)):
    x = 22 + i * 38; h = v_ * 1.7
    hot = a == 60
    f.box(x, base - h, 28, max(h, 1), "", fill=(SAND if hot else BLUE), stroke=(AMBER if hot else NAVY), r=1, sw=1.2)
    f.text(x + 14, base - h - 8, "%.1f" % v_, size=10.5, color=(AMBER if hot else NAVY), bold=True)
    f.text(x + 14, base + 14, "%d" % a, size=10.5, color=SLATE, bold=True)
f.line(16, base, 290, base, color=SLATE, sw=1.4)
f.text(150, base + 30, "angle between handle and force (degrees)", size=10.5, color=SLATE)
f.text(150, 214, "at 60 degrees: tau = (0, 0, %.2f) N m" % tau[2], size=10.5, color=AMBER, bold=True)
```

```photogrid label="6.3" cols="2" ratio="1.2" caption="The dot product as work. (a) A steep-gradient sign warns drivers that gravity has a large component along the road. (b) Take a 1,200 kg car on a 20 per cent grade (rise 1 for every 5 along the ground), so the angle is 11.31 degrees. The weight is W = (0, -11,760) N. Along 100 m of road the displacement is d = (98.06, 19.61) m, and W . d = -230,633 J, which equals -m g h for a rise of 19.61 m. The part of the weight pulling along the road is m g sin(theta) = 2306 N, and this is the force the brakes must resist."
@ photo id="ioemath/gradient" cap="A road-gradient warning sign: a car on a slope"
fit 1.2
focus 0.5 0.5
@ svg cap="Weight and displacement on a 20 per cent grade"
import math
m, g = 1200, 9.8
th = math.atan(0.2)
W = (0, -m * g); d = (100 * math.cos(th), 100 * math.sin(th))
work = W[0] * d[0] + W[1] * d[1]
h = 100 * math.sin(th); par = m * g * math.sin(th)
assert abs(work + m * g * h) < 1e-6 and abs(math.degrees(th) - 11.31) < 0.01 and abs(par - 2306.4) < 1
facts = dict(th="%.2f" % math.degrees(th), dx="%.2f" % d[0], dy="%.2f" % d[1], w="{:,.0f}".format(work), h="%.2f" % h, par="%.0f" % par)
f = Fig(300, 236)
f.text(150, 14, "m = 1,200 kg, grade 20 per cent", size=10.5, color=NAVY, bold=True)
ox, oy = 24, 124; L = 250; rise = 0.2 * L
f.poly([(ox, oy), (ox + L, oy), (ox + L, oy - rise)], fill=SOFT, stroke=SLATE, sw=1.6)
cx, cy = ox + 150, oy - 0.2 * 150
u = (math.cos(th), -math.sin(th))
f.circle(cx, cy - 6, 5, fill=NAVY, stroke=NAVY)
f.arrow([(cx, cy - 6), (cx, cy - 6 + 62)], color=RED, sw=2)
f.arrow([(cx, cy - 6), (cx - u[0] * 62 * math.sin(th), cy - 6 - u[1] * 62 * math.sin(th))], color=AMBER, sw=2.4)
f.arrow([(ox + 16, oy - 3), (ox + 16 + 90 * u[0], oy - 3 + 90 * u[1])], color=TEAL, sw=2.2)
f.text(cx + 8, cy + 54, "W", size=11, color=RED, bold=True, anchor="start")
f.text(ox + 62, oy - 10, "d", size=11, color=TEAL, bold=True)
f.text(150, 158, "red W = 11,760 N down;  teal d = 100 m along the road", size=10.5, color=SLATE)
f.text(150, 174, "amber: m g sin(theta) = %.0f N along the road" % par, size=10.5, color=AMBER, bold=True)
f.text(150, 190, "theta = %.2f degrees" % math.degrees(th), size=10.5, color=SLATE, bold=True)
f.text(150, 206, "W . d = {:,.0f} J  (= -m g h, h = %.2f m)".format(work) % h, size=10.5, color=NAVY, bold=True)
f.text(150, 222, "negative work: gravity opposes the climb", size=10.5, color=SLATE)
```

## Formula and fact sheet

| Topic | Result |
|---|---|
| angle | $\cos\theta=\frac{\vec a\cdot\vec b}{ab}$ |
| projection of $\vec b$ on $\vec a$ | $\frac{\vec a\cdot\vec b}{|\vec a|}$ |
| triangle area | $\frac{1}{2}|\vec a\times\vec b|$ |
| Lagrange | $|\vec a\times\vec b|^2=a^2b^2-(\vec a\cdot\vec b)^2$ |
| volume | $|[\vec a\,\vec b\,\vec c]|$; tetrahedron $\frac{1}{6}$ of it |
| triple product | $\vec a\times(\vec b\times\vec c)=\vec b(\vec a\cdot\vec c)-\vec c(\vec a\cdot\vec b)$ |

## Chapter summary

- Head minus tail gives $\overrightarrow{AB}$; the section formula weights the opposite end.
- Dot product zero means perpendicular; cross product zero means parallel; triple product zero means coplanar.
- Projection is $\frac{\vec a\cdot\vec b}{|\vec a|}$, a signed scalar.
- Areas come from $|\vec a\times\vec b|$, volumes from the scalar triple product.

## Practice questions

**Set A — Recall (10 questions)**

1. For $\vec a=2\hat i+3\hat j+\hat k$ and $\vec b=\hat i-\hat j+2\hat k$, $\vec a\cdot\vec b$ equals
   (a) 7 (b) 5 (c) 1 (d) $-1$
2. The magnitude of $3\hat i+4\hat j-12\hat k$ is
   (a) 13 (b) 19 (c) 11 (d) 5
3. $\hat i\times\hat j$ equals
   (a) 0 (b) $-\hat k$ (c) 1 (d) $\hat k$
4. The vectors $2\hat i+\lambda\hat j+\hat k$ and $\hat i-2\hat j+3\hat k$ are perpendicular for $\lambda=$
   (a) 2 (b) $5/2$ (c) $3/2$ (d) 1
5. The area of the parallelogram with adjacent sides $\hat i+\hat j$ and $\hat j+\hat k$ is
   (a) 2 (b) $\sqrt{2}$ (c) $\sqrt{3}$ (d) 3
6. If $[\vec a\,\vec b\,\vec c]=0$, the three vectors are
   (a) coplanar (b) parallel (c) mutually perpendicular (d) collinear
7. The angle between $\hat i+\hat j$ and $\hat j$ is
   (a) $30^\circ$ (b) $60^\circ$ (c) $90^\circ$ (d) $45^\circ$
8. The midpoint of $A(2,4,6)$ and $B(4,0,2)$ is
   (a) $(6,4,8)$ (b) $(3,2,4)$ (c) $(1,2,2)$ (d) $(3,4,2)$
9. The unit vector along $3\hat i-4\hat j$ is
   (a) $\dfrac{3\hat i-4\hat j}{25}$ (b) $3\hat i-4\hat j$ (c) $\dfrac{3\hat i+4\hat j}{5}$ (d) $\dfrac{3\hat i-4\hat j}{5}$
10. If $|\vec a|=5$ and $|\vec b|=3$, then $(\vec a+\vec b)\cdot(\vec a-\vec b)$ is
    (a) 16 (b) 34 (c) 4 (d) 25

::: note Answers and explanations — Set A
**1.** (c) — $2-3+2=1$.
**2.** (a) — $\sqrt{9+16+144}=13$.
**3.** (d) — right-hand rule: $\hat i\times\hat j=\hat k$ ($\hat j\times\hat i=-\hat k$).
**4.** (b) — $2-2\lambda+3=0\Rightarrow\lambda=\frac{5}{2}$.
**5.** (c) — $\vec a\times\vec b=(1,-1,1)$, magnitude $\sqrt{3}$.
**6.** (a) — a zero scalar triple product means the vectors lie in one plane.
**7.** (d) — $\cos\theta=\frac{1}{\sqrt{2}}$.
**8.** (b) — average of the coordinates.
**9.** (d) — divide by the magnitude 5.
**10.** (a) — $|\vec a|^2-|\vec b|^2=25-9=16$.
:::

**Set B — Understanding (7 questions)**

1. The projection of $\vec b=2\hat i+3\hat j-2\hat k$ on $\vec a=\hat i+2\hat j+3\hat k$ is
   (a) $2/\sqrt{17}$ (b) $2/\sqrt{14}$ (c) $2/7$ (d) $-2/7$
2. If $|\vec a|=3$, $|\vec b|=4$ and the angle between them is $30^\circ$, then $|\vec a\times\vec b|$ is
   (a) 12 (b) $6\sqrt{3}$ (c) 6 (d) 3
3. The vectors $2\hat i-\hat j+\hat k$, $\hat i+2\hat j-3\hat k$ and $3\hat i+\lambda\hat j+5\hat k$ are coplanar for $\lambda=$
   (a) 4 (b) $-1$ (c) 1 (d) $-4$
4. The area of the triangle with vertices $(1,0,0)$, $(0,1,0)$, $(0,0,1)$ is
   (a) $\frac{\sqrt{3}}{2}$ (b) $\sqrt{3}$ (c) $\frac{1}{2}$ (d) $\frac{3}{2}$
5. The volume of the parallelepiped with edges $\hat i+\hat j$, $\hat j+\hat k$, $\hat k+\hat i$ is
   (a) 1 (b) 4 (c) 2 (d) 3
6. A unit vector perpendicular to both $\hat i+\hat j$ and $\hat j+\hat k$ is
   (a) $\frac{\hat i+\hat j+\hat k}{\sqrt{3}}$ (b) $\frac{\hat i-\hat j+\hat k}{\sqrt{3}}$ (c) $\frac{\hat i-\hat j-\hat k}{3}$ (d) $\frac{\hat i+\hat j-\hat k}{\sqrt{3}}$
7. The value of $\hat i\times(\hat j\times\hat i)$ is
   (a) $\hat j$ (b) $0$ (c) $-\hat j$ (d) $\hat k$

::: note Answers and explanations — Set B
**1.** (b) — $\vec a\cdot\vec b=2+6-6=2$, $|\vec a|=\sqrt{14}$. The projection of $\vec b$ on $\vec a$ divides by $|\vec a|$.
**2.** (c) — $3\cdot4\sin30^\circ=6$.
**3.** (d) — the determinant is $28+7\lambda=0$.
**4.** (a) — $\overrightarrow{AB}\times\overrightarrow{AC}=(1,1,1)$; half of $\sqrt{3}$.
**5.** (c) — $(det | 1&1&0 ; 0&1&1 ; 1&0&1 |)=1+1=2$.
**6.** (b) — $(\hat i+\hat j)\times(\hat j+\hat k)=\hat i-\hat j+\hat k$, magnitude $\sqrt{3}$.
**7.** (a) — $\hat j\times\hat i=-\hat k$, and $\hat i\times(-\hat k)=\hat j$. Check with BAC–CAB: $\hat j(\hat i\cdot\hat i)-\hat i(\hat i\cdot\hat j)=\hat j$.
:::

**Set C — Application (6 questions)**

1. The points $(1,1,1)$, $(2,3,4)$ and $(3,5,\lambda)$ are collinear when $\lambda=$
   (a) 6 (b) 7 (c) 8 (d) 5
2. The work done by $\vec F=2\hat i+3\hat j+\hat k$ in moving a particle from $(1,1,1)$ to $(3,2,4)$ is
   (a) 10 (b) 12 (c) 8 (d) 9
3. If $\vec a,\vec b$ are unit vectors at $60^\circ$ to each other, $|\vec a+\vec b|$ is
   (a) $\sqrt{2}$ (b) 2 (c) 1 (d) $\sqrt{3}$
4. If $|\vec a|=2$, $|\vec b|=3$ and $\vec a\cdot\vec b=3$, then $|\vec a\times\vec b|$ is
   (a) 3 (b) 6 (c) 9 (d) $3\sqrt{3}$
5. The vectors $2\hat i+3\hat j$ and $\hat i+\lambda\hat j$ are linearly dependent for $\lambda=$
   (a) $2/3$ (b) $3/2$ (c) 6 (d) $1/6$
6. The volume of the tetrahedron with vertices $O$, $(1,0,0)$, $(0,2,0)$, $(0,0,3)$ is
   (a) 1 (b) 6 (c) 3 (d) 2

::: note Answers and explanations — Set C
**1.** (b) — $\overrightarrow{AB}=(1,2,3)$, $\overrightarrow{AC}=(2,4,\lambda-1)$ must be $2\overrightarrow{AB}$: $\lambda-1=6$.
**2.** (a) — displacement $(2,1,3)$: $4+3+3=10$.
**3.** (d) — $|\vec a+\vec b|^2=1+1+2\cdot\frac{1}{2}=3$.
**4.** (d) — $|\vec a\times\vec b|^2=36-9=27$.
**5.** (b) — parallel: $\frac{2}{1}=\frac{3}{\lambda}$.
**6.** (a) — $\frac{1}{6}|1\cdot2\cdot3|=1$.
:::

**Group D — Model answers for long questions (10 marks each, for deeper revision)**

1. For $\mathbf a=(1,2,3)$ and $\mathbf b=(2,-1,1)$ find the scalar product, angle, vector product, parallelogram area and projection. <span class="marks">[10]</span>
2. Use the scalar triple product to test coplanarity and to find volumes; find the work done by a force and the torque of a force. <span class="marks">[10]</span>

### Model answer D1: Scalar and vector products (10 marks)

**Introduction.** The **scalar (dot) product** is $\mathbf a\cdot\mathbf b=\lvert\mathbf a\rvert\lvert\mathbf b\rvert\cos\theta=a_1b_1+a_2b_2+a_3b_3$; the **vector (cross) product** $\mathbf a\times\mathbf b$ has magnitude $\lvert\mathbf a\rvert\lvert\mathbf b\rvert\sin\theta$ and is perpendicular to both vectors.

**Solution.**

| Quantity | Working | Value |
|---|---|---|
| $\mathbf a\cdot\mathbf b$ | $2-2+3$ | $3$ |
| $\lvert\mathbf a\rvert,\ \lvert\mathbf b\rvert$ | $\sqrt{14},\ \sqrt6$ | $3.742,\ 2.449$ |
| Angle $\theta$ | $\cos\theta=\frac{3}{\sqrt{84}}=0.327$ | $70.9^\circ$ |
| $\mathbf a\times\mathbf b$ | $(2\cdot1-3(-1),\ 3\cdot2-1\cdot1,\ 1(-1)-2\cdot2)$ | $(5,5,-5)$ |
| Area of parallelogram | $\lvert\mathbf a\times\mathbf b\rvert=\sqrt{75}$ | $8.66$ |
| Projection of $\mathbf a$ on $\mathbf b$ | $\frac{\mathbf a\cdot\mathbf b}{\lvert\mathbf b\rvert}=\frac{3}{\sqrt6}$ | $1.22$ |

**Checks.** $(\mathbf a\times\mathbf b)\cdot\mathbf a=5+10-15=0$ and $(\mathbf a\times\mathbf b)\cdot\mathbf b=10-5-5=0$, so the result is perpendicular to both. The area of the triangle with these sides is half: $4.33$.

**Properties.**

1. $\mathbf a\cdot\mathbf b=\mathbf b\cdot\mathbf a$, but $\mathbf a\times\mathbf b=-\mathbf b\times\mathbf a$.
2. Two non-zero vectors are perpendicular if $\mathbf a\cdot\mathbf b=0$ and parallel if $\mathbf a\times\mathbf b=\mathbf 0$.
3. $\hat i\cdot\hat i=1$, $\hat i\times\hat j=\hat k$.
4. Section formula: the point dividing $\mathbf a$ and $\mathbf b$ in the ratio $m:n$ is $\frac{m\mathbf b+n\mathbf a}{m+n}$.

**Conclusion.** The dot product measures how much two vectors point together and the cross product measures the area they span.

### Model answer D2: Triple product, work and torque (10 marks)

**Introduction.** The **scalar triple product** $[\mathbf a\ \mathbf b\ \mathbf c]=\mathbf a\cdot(\mathbf b\times\mathbf c)$ equals the determinant of the three vectors. Its absolute value is the volume of the parallelepiped.

**1. Coplanarity.** Three vectors are coplanar if $[\mathbf a\ \mathbf b\ \mathbf c]=0$. For $\mathbf a=(1,2,3)$, $\mathbf b=(2,-1,1)$, $\mathbf c=(1,1,2)$:
$$\begin{vmatrix}1&2&3\\2&-1&1\\1&1&2\end{vmatrix}=1(-2-1)-2(4-1)+3(2+1)=-3-6+9=0.$$
So they are **coplanar**: indeed $\mathbf c=\frac35\mathbf a+\frac15\mathbf b$, since $\frac35+\frac25=1$, $\frac65-\frac15=1$ and $\frac95+\frac15=2$.

**2. Volume.** For $\mathbf c=(3,1,0)$: the determinant $=1(0-1)-2(0-3)+3(2+3)=-1+6+15=20$. The parallelepiped has volume $20$ and the tetrahedron has volume $\frac{20}{6}=3.33$.

**3. Work done.** $W=\mathbf F\cdot\mathbf d$. For $\mathbf F=(2,3,1)\ \text{N}$ and $\mathbf d=(3,-1,2)\ \text{m}$: $W=6-3+2=5\ \text{J}$.

**4. Torque.** $\boldsymbol\tau=\mathbf r\times\mathbf F$. For $\mathbf r=(2,1,0)$ and $\mathbf F=(1,-1,3)$: $\boldsymbol\tau=(1\cdot3-0,\ 0-2\cdot3,\ 2(-1)-1\cdot1)=(3,-6,-3)$, with magnitude $\sqrt{9+36+9}=\sqrt{54}=7.35\ \text{N m}$.

| Quantity | Formula | Value |
|---|---|---|
| Coplanarity test | $[\mathbf a\ \mathbf b\ \mathbf c]=0$ | $0$ (coplanar) |
| Parallelepiped volume | $\lvert[\mathbf a\ \mathbf b\ \mathbf c]\rvert$ | $20$ |
| Work | $\mathbf F\cdot\mathbf d$ | $5\ \text{J}$ |
| Torque | $\mathbf r\times\mathbf F$ | $7.35\ \text{N m}$ |

**Identity.** $\mathbf a\times(\mathbf b\times\mathbf c)=\mathbf b(\mathbf a\cdot\mathbf c)-\mathbf c(\mathbf a\cdot\mathbf b)$.

**Conclusion.** The triple product gives volume and a coplanarity test, and the two products model work and torque in physics.
