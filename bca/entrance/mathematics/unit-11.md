---
subject: Mathematics
grade: BCA
unit: 11
title: Vectors
hours: 2
area: Vectors
---

Vectors give one or two questions: a magnitude, a dot product, a perpendicularity condition or an area from a cross product. Everything follows from component arithmetic in $\mathbf{i},\mathbf{j},\mathbf{k}$, so the chapter is short and the marks are cheap.

::: key What the paper asks from this chapter
- **Components**: magnitude $\sqrt{a_1^2+a_2^2+a_3^2}$, unit vector $\frac{\mathbf{a}}{|\mathbf{a}|}$, vector $\overrightarrow{AB}=B-A$.
- **Dot product**: $\mathbf{a}\cdot\mathbf{b}=|\mathbf{a}||\mathbf{b}|\cos\theta=a_1b_1+a_2b_2+a_3b_3$; perpendicular iff $0$.
- **Cross product**: $|\mathbf{a}\times\mathbf{b}|=|\mathbf{a}||\mathbf{b}|\sin\theta$ = area of the parallelogram; parallel iff $\mathbf{0}$.
:::

## 11.1 Vector algebra, position vectors and unit vectors

- $\mathbf{a}=a_1\mathbf{i}+a_2\mathbf{j}+a_3\mathbf{k}$, $|\mathbf{a}|=\sqrt{a_1^2+a_2^2+a_3^2}$. The unit vector is $\hat{\mathbf{a}}=\frac{\mathbf{a}}{|\mathbf{a}|}$ and has magnitude 1.
- $\overrightarrow{AB}=\mathbf{b}-\mathbf{a}$ (head minus tail). The midpoint of $A,B$ has position vector $\frac{\mathbf{a}+\mathbf{b}}{2}$; the point dividing $AB$ in $m:n$ is $\frac{m\mathbf{b}+n\mathbf{a}}{m+n}$.
- Add and subtract component by component; $k\mathbf{a}$ scales every component.

```photogrid label="11.1" cols="3" ratio="1.0" caption="Where vectors came from. (a) Sir William Rowan Hamilton (1805-1865), who invented quaternions and with them the dot and cross products and the words vector and scalar. (b) The plaque on Broom Bridge, Dublin, where on 16 October 1843 he scratched i^2 = j^2 = k^2 = ijk = -1, the rule behind i x j = k. (c) A compass rose: a direction plus a distance is a vector, and eight unit vectors point to the eight compass directions."
@ photo id="bcamath/hamilton" cap="W. R. Hamilton, inventor of quaternions"
focus 0.5 0.3
@ photo id="bcamath/broom" cap="Broom Bridge plaque: i^2 = j^2 = k^2 = ijk = -1"
focus 0.55 0.4
@ photo id="bcamath/windrose" cap="Compass rose: direction and distance"
focus 0.5 0.5
```

```svgfig label="11.1" caption="Vector algebra on a = (3, 4) and b = (1, -2), computed. a + b = (4, 2) is the diagonal of the parallelogram on a and b, a - b = (2, 6) joins the tips, |a| = sqrt(9 + 16) = 5 and the unit vector in the direction of a is a/|a| = (0.6, 0.8), whose length is 1. The position vector of AB is OB - OA (head minus tail)."
import math
a, b = (3, 4), (1, -2)
s = (a[0] + b[0], a[1] + b[1]); dd = (a[0] - b[0], a[1] - b[1]); na = math.hypot(*a); u = (a[0] / na, a[1] / na)
assert s == (4, 2) and dd == (2, 6) and na == 5 and u == (0.6, 0.8) and abs(math.hypot(*u) - 1) < 1e-12
assert math.hypot(*s) <= na + math.hypot(*b)
f = Fig(780, 320)
ax = Axes(f, 30, 14, 360, 290, (-2, 6), (-4, 6))
ax.grid(1, 1, size=10); ax.axes("x", "y")
P = lambda v: (ax.X(v[0]), ax.Y(v[1]))
f.poly([P((0, 0)), P(a), P(s), P(b)], fill="#fef3c7", stroke="#fef3c7", sw=1)
f.line(*P(a), *P(s), color=SLATE, sw=1.2, dash=True); f.line(*P(b), *P(s), color=SLATE, sw=1.2, dash=True)
f.arrow([P((0, 0)), P(a)], color=NAVY, sw=2.6); f.arrow([P((0, 0)), P(b)], color=TEAL, sw=2.6); f.arrow([P((0, 0)), P(s)], color=RED, sw=2.6)
f.arrow([P((0, 0)), P(u)], color=AMBER, sw=2.6)
f.text(P(a)[0] - 14, P(a)[1] - 8, "a (3, 4)", size=11, color=NAVY, bold=True, anchor="end"); f.text(P(b)[0] - 8, P(b)[1] + 14, "b (1, -2)", size=11, color=TEAL, bold=True, anchor="end")
f.text(P(s)[0] + 10, P(s)[1] + 4, "a + b (4, 2)", size=11, color=RED, bold=True, anchor="start"); f.text(P(u)[0] + 12, P(u)[1] + 16, "unit u", size=10, color=AMBER, bold=True, anchor="start")
f.text(570, 30, "Checked on a and b", size=11.5, color=NAVY, bold=True)
for j, (t, c) in enumerate([("a + b = (3+1, 4-2) = (4, 2)", RED), ("a - b = (3-1, 4+2) = (2, 6)", SLATE), ("|a| = sqrt(3^2 + 4^2) = 5", NAVY), ("unit vector = a/|a| = (3/5, 4/5)", AMBER), ("|u| = sqrt(0.36 + 0.64) = 1", SLATE), ("2a - 3b = (6-3, 8+6) = (3, 14)", SLATE), ("AB = OB - OA (head minus tail)", NAVY), ("|a + b| = 4.47 <= |a| + |b| = 7.47", TEAL)]):
    f.text(410, 64 + j * 30, t, size=10.5, color=c, anchor="start", bold=(c in (RED, NAVY)))
```

## 11.2 Dot product, cross product and their applications

- $\mathbf{i}\cdot\mathbf{i}=1$, $\mathbf{i}\cdot\mathbf{j}=0$. $\cos\theta=\frac{\mathbf{a}\cdot\mathbf{b}}{|\mathbf{a}||\mathbf{b}|}$. Projection of $\mathbf{a}$ on $\mathbf{b}$ is $\frac{\mathbf{a}\cdot\mathbf{b}}{|\mathbf{b}|}$. Work $=\mathbf{F}\cdot\mathbf{d}$. $|\mathbf{a}+\mathbf{b}|^2=|\mathbf{a}|^2+|\mathbf{b}|^2+2\mathbf{a}\cdot\mathbf{b}$.
- $\mathbf{i}\times\mathbf{j}=\mathbf{k}$, $\mathbf{j}\times\mathbf{k}=\mathbf{i}$, $\mathbf{k}\times\mathbf{i}=\mathbf{j}$; reversing the order flips the sign: $\mathbf{j}\times\mathbf{i}=-\mathbf{k}$. $\mathbf{a}\times\mathbf{a}=\mathbf{0}$. The result is a **vector**; the dot product is a **scalar**.
- Area of parallelogram $=|\mathbf{a}\times\mathbf{b}|$; of triangle $=\frac{1}{2}|\mathbf{a}\times\mathbf{b}|$.

```svgfig label="11.2" caption="The dot product measures alignment. For a = (3, 4) and b = (2, -1): a . b = 3 x 2 + 4 x (-1) = 2, |a| = 5, |b| = sqrt5, so cos t = 2/(5 sqrt5) = 0.179 and t = 79.7 degrees; the projection of a on b is a.b/|b| = 0.894. The vectors (3, 4) and (4, -3) give 12 - 12 = 0, so they are perpendicular. Work done by F = (2, 3) over d = (4, 1) is F . d = 11."
import math
a, b = (3, 4), (2, -1); dot = a[0] * b[0] + a[1] * b[1]; na, nb = math.hypot(*a), math.hypot(*b)
c = dot / (na * nb); t = math.degrees(math.acos(c)); proj = dot / nb
assert dot == 2 and round(c, 3) == 0.179 and round(t, 1) == 79.7 and round(proj, 3) == 0.894
assert 3 * 4 + 4 * -3 == 0 and 2 * 4 + 3 * 1 == 11
f = Fig(780, 320)
ax = Axes(f, 30, 14, 330, 290, (-2, 5), (-3, 5))
ax.grid(1, 1, size=10); ax.axes("x", "y")
P = lambda v: (ax.X(v[0]), ax.Y(v[1]))
f.arrow([P((0, 0)), P(a)], color=NAVY, sw=2.6); f.arrow([P((0, 0)), P(b)], color=TEAL, sw=2.6); f.arrow([P((0, 0)), P((4, -3))], color=RED, sw=2, dash=True)
k = dot / (nb * nb); pj = (k * b[0], k * b[1]); f.line(*P(a), *P(pj), color=SLATE, sw=1.2, dash=True); f.circle(*P(pj), 4, fill=AMBER, stroke=AMBER)
f.text(P(a)[0] + 10, P(a)[1] - 6, "a (3, 4)", size=11, color=NAVY, bold=True, anchor="start"); f.text(P(b)[0] + 8, P(b)[1] + 16, "b (2, -1)", size=11, color=TEAL, bold=True, anchor="start")
f.text(P((4, -3))[0] + 6, P((4, -3))[1] - 6, "(4, -3) perp. to a", size=10, color=RED, bold=True, anchor="end")
f.text(P((0.4, 0.5))[0], P((0.4, 0.5))[1] - 4, "79.7 deg", size=10, color=SLATE, bold=True, anchor="start")
f.text(570, 30, "Dot product facts", size=11.5, color=NAVY, bold=True)
for j, (t, col) in enumerate([("a . b = a1 b1 + a2 b2 = |a||b| cos t", NAVY), ("a . b = 3(2) + 4(-1) = 2", SLATE), ("cos t = 2/(5 x 2.236) = 0.179", SLATE), ("t = 79.7 degrees", RED), ("projection of a on b = a.b/|b| = 0.894", TEAL), ("a . b = 0  means perpendicular", RED), ("a . a = |a|^2,  i . i = 1,  i . j = 0", SLATE), ("work = F . d = 2(4) + 3(1) = 11", TEAL)]):
    f.text(410, 64 + j * 30, t, size=10.5, color=col, anchor="start", bold=(col in (NAVY, RED)))
```

```svgfig label="11.3" caption="The cross product of a = (1, 2, 3) and b = (4, 5, 6) is a x b = (2 x 6 - 3 x 5, 3 x 4 - 1 x 6, 1 x 5 - 2 x 4) = (-3, 6, -3). It is perpendicular to both (dot products 0), its length sqrt(54) = 7.35 is the area of the parallelogram on a and b, and b x a = (3, -6, 3) points the opposite way, so the order matters."
import math
a, b = (1, 2, 3), (4, 5, 6)
cr = lambda p, q: (p[1] * q[2] - p[2] * q[1], p[2] * q[0] - p[0] * q[2], p[0] * q[1] - p[1] * q[0])
dt = lambda p, q: sum(x * y for x, y in zip(p, q))
c = cr(a, b); assert c == (-3, 6, -3) and dt(c, a) == 0 and dt(c, b) == 0 and cr(b, a) == (3, -6, 3)
area = math.sqrt(dt(c, c)); assert round(area, 2) == 7.35 and abs(area - math.sqrt(dt(a, a) * dt(b, b) - dt(a, b) ** 2)) < 1e-9
assert cr((1, 0, 0), (0, 1, 0)) == (0, 0, 1) and cr((0, 1, 0), (1, 0, 0)) == (0, 0, -1)
f = Fig(780, 320)
f.text(180, 22, "Determinant layout", size=11.5, color=NAVY, bold=True)
rows = [["i", "j", "k"], [1, 2, 3], [4, 5, 6]]
for i, r in enumerate(rows):
    for j, v in enumerate(r): f.box(40 + j * 60, 40 + i * 40, 54, 34, str(v), fill=("#fde68a" if i == 0 else "#dbeafe"), stroke="#cbd5e1", size=13, bold=True, color=NAVY, r=3)
for j, t in enumerate(["i (2x6 - 3x5) = -3 i", "- j (1x6 - 3x4) = +6 j  (middle sign flips)", "+ k (1x5 - 2x4) = -3 k", "a x b = (-3, 6, -3)"]):
    f.text(30, 190 + j * 26, t, size=10.5, color=(RED if j == 3 else SLATE), anchor="start", bold=(j == 3))
f.text(30, 306, "i x j = k,  j x k = i,  k x i = j;  reversed order gives a minus", size=10, color=TEAL, bold=True, anchor="start")
f.text(570, 22, "Checks", size=11.5, color=NAVY, bold=True)
for j, (t, col) in enumerate([("(a x b) . a = -3 + 12 - 9 = 0", TEAL), ("(a x b) . b = -12 + 30 - 18 = 0", TEAL), ("|a x b| = sqrt(9 + 36 + 9) = 7.35", RED), ("= area of the parallelogram", RED), ("triangle area = 7.35 / 2 = 3.67", SLATE), ("b x a = (3, -6, 3) = -(a x b)", NAVY), ("|a x b| = |a||b| sin t", NAVY), ("a x b = 0  means a and b are parallel", SLATE)]):
    f.text(400, 56 + j * 30, t, size=10.5, color=col, anchor="start", bold=(col in (RED, NAVY)))
```

## 11.3 Eight traps in vectors

Vector questions are short, but each mixes a scalar result with a vector result, and the paper loves to test the difference. These eight traps cover the model questions.

1. **A vector has magnitude and direction; a scalar has only size.** The magnitude of $\vec a=(3,4)$ is $\sqrt{3^2+4^2}=5$, and the unit vector is $\hat a=\frac{\vec a}{|\vec a|}=\left(\frac35,\frac45\right)$ (Fig 11.1). A unit vector always has length 1, so check this. Do not write $|\vec a|$ as $3+4$.
2. **Head minus tail.** The vector from $A$ to $B$ is $\vec{AB}=\vec{OB}-\vec{OA}$, the position vector of the end point minus the start. For $A(1,2)$ and $B(7,10)$ this is $(6,8)$. The midpoint has position vector $\frac{\vec a+\vec b}{2}$, and the internal ratio $m:n$ gives $\frac{m\vec b+n\vec a}{m+n}$.
3. **Parallel means a scalar multiple.** $\vec a\parallel\vec b$ when $\vec a=\lambda\vec b$, so $(2,6)$ and $(1,3)$ are parallel with $\lambda=2$. Three points are collinear if $\vec{AB}$ and $\vec{BC}$ are parallel. Equal vectors have equal components, not just equal length.
4. **The dot product gives a number.** $\vec a\cdot\vec b=a_1b_1+a_2b_2=|a||b|\cos\theta$ is a scalar (Fig 11.2). It is zero when the vectors are perpendicular, so $(3,4)\cdot(4,-3)=0$. Also $\vec a\cdot\vec a=|\vec a|^2$, $\hat i\cdot\hat i=1$ and $\hat i\cdot\hat j=0$.
5. **Angle and projection come from the dot product.** $\cos\theta=\frac{\vec a\cdot\vec b}{|a||b|}$, and the scalar projection of $\vec a$ on $\vec b$ is $\frac{\vec a\cdot\vec b}{|\vec b|}$. The vector projection multiplies that by $\hat b$, giving $\frac{\vec a\cdot\vec b}{|\vec b|^2}\vec b$. A question that asks for "the component" wants the scalar one.
6. **The cross product gives a vector, and the order matters.** $\vec a\times\vec b=-\vec b\times\vec a$, with magnitude $|a||b|\sin\theta$, and it is perpendicular to both (Fig 11.3). In the determinant the middle sign flips, which is the term most students get wrong. $\vec a\times\vec b=\vec0$ means the vectors are parallel.
7. **Areas and work come from the two products.** The parallelogram on $\vec a,\vec b$ has area $|\vec a\times\vec b|$, and the triangle has half of that. Work done is $W=\vec F\cdot\vec d$ (a scalar), while the moment of a force is $\vec r\times\vec F$ (a vector). For $F=(2,3)$ and $d=(4,1)$, $W=11$.
8. **Do not treat vectors like numbers.** $|\vec a+\vec b|\ne|\vec a|+|\vec b|$ unless the vectors point the same way. $(\vec a+\vec b)^2=|a|^2+2\vec a\cdot\vec b+|b|^2$, and an expression such as $\vec a\cdot\vec b\cdot\vec c$ has no meaning because the first dot is a scalar. There is no division of one vector by another.

### 11.3.1 Worked checks

**Q. Find the magnitude and unit vector of $3\hat i+4\hat j$, and the angle between $(3,4)$ and $(2,-1)$.**

**Answer.** $|\vec a|=5$ and the unit vector is $0.6\hat i+0.8\hat j$. The dot product is $6-4=2$, $|\vec b|=\sqrt5$, so $\cos\theta=\frac{2}{5\sqrt5}=0.179$ and $\theta=79.7^\circ$. This is the angle drawn in Fig 11.2.

**Q. Find $\vec a\times\vec b$ for $\vec a=(1,2,3)$ and $\vec b=(4,5,6)$, and the area of the parallelogram.**

**Answer.** $\vec a\times\vec b=(12-15,\,12-6,\,5-8)=(-3,6,-3)$. The area is $\sqrt{9+36+9}=\sqrt{54}\approx7.35$. Check: $(-3,6,-3)\cdot(1,2,3)=-3+12-9=0$, so the result is perpendicular to $\vec a$.

**Q. Find $\lambda$ so that $(2,\lambda)$ is perpendicular to $(3,-4)$, and the work done by $F=(2,3)$ over $d=(4,1)$.**

**Answer.** Perpendicular means the dot product is zero: $6-4\lambda=0$, so $\lambda=\frac32$. Work $=2(4)+3(1)=11$ units. Both answers use the scalar dot product.

## Formula and fact sheet

| Item | Result |
|---|---|
| Magnitude | $\sqrt{a_1^2+a_2^2+a_3^2}$ |
| Dot product | $a_1b_1+a_2b_2+a_3b_3=|\mathbf{a}||\mathbf{b}|\cos\theta$ |
| Perpendicular / parallel | $\mathbf{a}\cdot\mathbf{b}=0$ / $\mathbf{a}\times\mathbf{b}=\mathbf{0}$ |
| Triangle area | $\frac{1}{2}|\mathbf{a}\times\mathbf{b}|$ |

## Chapter summary

- A vector from $A$ to $B$ is $B-A$.
- Dot product gives a number, cross product gives a vector.
- Perpendicular means dot product zero.
- $|\mathbf{a}\times\mathbf{b}|$ is a parallelogram area.
- Unit vectors are found by dividing by the magnitude.

## Practice questions

**Set A — Recall (20 questions)**

1. The magnitude of $3\mathbf{i}+4\mathbf{j}$ is
   (a) 7 (b) 1 (c) 25 (d) 5
2. $\mathbf{i}\cdot\mathbf{j}$ equals
   (a) 0 (b) 1 (c) $\mathbf{k}$ (d) $-1$
3. $\mathbf{i}\times\mathbf{j}$ equals
   (a) $-\mathbf{k}$ (b) 0 (c) $\mathbf{k}$ (d) 1
4. For $\mathbf{a}=(1,2,3)$ and $\mathbf{b}=(4,5,6)$, $\mathbf{a}\cdot\mathbf{b}$ is
   (a) 28 (b) 32 (c) 21 (d) 15
5. Two non-zero vectors are perpendicular when
   (a) their dot product is 1 (b) their dot product is $-1$ (c) their cross product is zero (d) their dot product is zero
6. The unit vector along $3\mathbf{i}+4\mathbf{j}$ is
   (a) $3\mathbf{i}+4\mathbf{j}$ (b) $\frac{3\mathbf{i}+4\mathbf{j}}{25}$ (c) $\frac{3\mathbf{i}+4\mathbf{j}}{5}$ (d) $\frac{4\mathbf{i}+3\mathbf{j}}{5}$
7. $\mathbf{a}\times\mathbf{a}$ equals
   (a) the zero vector (b) $|\mathbf{a}|^2$ (c) $\mathbf{a}$ (d) 1
8. $|\mathbf{a}\times\mathbf{b}|$ is the area of a
   (a) triangle (b) parallelogram (c) rectangle only (d) circle
9. The angle between $\mathbf{i}$ and $\mathbf{j}$ is
   (a) 0° (b) 45° (c) 90° (d) 180°
10. If $\mathbf{a}$ and $\mathbf{b}$ point the same way, $\mathbf{a}\cdot\mathbf{b}$ equals
    (a) 0 (b) $|\mathbf{a}|+|\mathbf{b}|$ (c) $\frac{|\mathbf{a}|}{|\mathbf{b}|}$ (d) $|\mathbf{a}||\mathbf{b}|$
11. For $A(1,2,3)$ and $B(4,6,8)$, $\overrightarrow{AB}$ is
    (a) $3\mathbf{i}+4\mathbf{j}+5\mathbf{k}$ (b) $5\mathbf{i}+8\mathbf{j}+11\mathbf{k}$ (c) $-3\mathbf{i}-4\mathbf{j}-5\mathbf{k}$ (d) $4\mathbf{i}+6\mathbf{j}+8\mathbf{k}$
12. The magnitude of $\mathbf{i}+\mathbf{j}+\mathbf{k}$ is
    (a) 3 (b) $\sqrt{3}$ (c) 1 (d) 2
13. $\mathbf{j}\times\mathbf{i}$ equals
    (a) $\mathbf{k}$ (b) 0 (c) $-\mathbf{k}$ (d) 1
14. $\mathbf{k}\cdot\mathbf{k}$ equals
    (a) 0 (b) $\mathbf{k}$ (c) $-1$ (d) 1
15. The projection of $\mathbf{a}$ on $\mathbf{b}$ is
    (a) $\frac{\mathbf{a}\cdot\mathbf{b}}{|\mathbf{b}|}$ (b) $\frac{\mathbf{a}\cdot\mathbf{b}}{|\mathbf{a}|}$ (c) $|\mathbf{a}||\mathbf{b}|$ (d) $\mathbf{a}\times\mathbf{b}$
16. Two vectors are parallel when
    (a) $\mathbf{a}\cdot\mathbf{b}=0$ (b) $|\mathbf{a}|=|\mathbf{b}|$ (c) $\mathbf{a}\times\mathbf{b}=\mathbf{0}$ (d) $\mathbf{a}+\mathbf{b}=\mathbf{0}$
17. The position vector of the midpoint of $A(2,4)$ and $B(6,8)$ is
    (a) $8\mathbf{i}+12\mathbf{j}$ (b) $4\mathbf{i}+6\mathbf{j}$ (c) $3\mathbf{i}+5\mathbf{j}$ (d) $2\mathbf{i}+2\mathbf{j}$
18. The magnitude of $2\mathbf{i}-2\mathbf{j}+\mathbf{k}$ is
    (a) 3 (b) 1 (c) 5 (d) 9
19. If $|\mathbf{a}|=3$, $|\mathbf{b}|=4$ and the angle between them is 90°, then $\mathbf{a}\cdot\mathbf{b}$ is
    (a) 12 (b) 7 (c) 1 (d) 0
20. The cross product of two vectors is a
    (a) scalar (b) vector (c) matrix (d) plain number

::: note Answers and explanations — Set A
**1.** (d) — √(9 + 16) = 5.
**2.** (a) — i and j are perpendicular.
**3.** (c) — right-hand rule.
**4.** (b) — 4 + 10 + 18 = 32.
**5.** (d) — a·b = |a||b|cos 90° = 0; (c) describes parallel vectors.
**6.** (c) — divide by the magnitude 5.
**7.** (a) — sin 0° = 0.
**8.** (b) — the triangle is half of it.
**9.** (c) — axes are perpendicular.
**10.** (d) — cos 0° = 1.
**11.** (a) — head minus tail: (3, 4, 5).
**12.** (b) — √(1 + 1 + 1).
**13.** (c) — swapping the order flips the sign.
**14.** (d) — a unit vector's square is 1.
**15.** (a) — scalar projection divides by |b|.
**16.** (c) — parallel vectors have a zero cross product.
**17.** (b) — average of the coordinates.
**18.** (a) — √(4 + 4 + 1) = 3.
**19.** (d) — cos 90° = 0.
**20.** (b) — the cross product is a vector; the dot product is a scalar.
:::

**Set B — Understanding (12 questions)**

1. The angle between $\mathbf{a}=\mathbf{i}+\mathbf{j}$ and $\mathbf{b}=\mathbf{i}-\mathbf{j}$ is
   (a) 90° (b) 45° (c) 60° (d) 0°
2. $\mathbf{a}=\lambda\mathbf{i}+4\mathbf{j}$ and $\mathbf{b}=2\mathbf{i}-\mathbf{j}$ are perpendicular when $\lambda$ is
   (a) 1 (b) 4 (c) 2 (d) $-2$
3. The magnitude of $\mathbf{i}\times(\mathbf{i}+\mathbf{j})$ is
   (a) 0 (b) 2 (c) $\sqrt{2}$ (d) 1
4. The area of the parallelogram with adjacent sides $3\mathbf{i}$ and $4\mathbf{j}$ is
   (a) 7 (b) 12 (c) 6 (d) 1
5. The area of the triangle with sides $2\mathbf{i}$ and $3\mathbf{j}$ from a vertex is
   (a) 3 (b) 6 (c) 12 (d) 5
6. The vector from $A(1,1)$ to $B(4,5)$ has magnitude
   (a) 7 (b) 3 (c) 4 (d) 5
7. If $|\mathbf{a}|=|\mathbf{b}|=1$ and $\mathbf{a}\cdot\mathbf{b}=\frac{1}{2}$, the angle between them is
   (a) 30° (b) 45° (c) 60° (d) 90°
8. For $\mathbf{a}=\mathbf{i}+2\mathbf{j}+3\mathbf{k}$ and $\mathbf{b}=2\mathbf{i}-\mathbf{j}+\mathbf{k}$, $\mathbf{a}\cdot\mathbf{b}$ is
   (a) 5 (b) 3 (c) 0 (d) 7
9. The projection of $3\mathbf{i}+4\mathbf{j}$ on $\mathbf{i}$ is
   (a) 5 (b) 4 (c) 7 (d) 3
10. A vector perpendicular to $3\mathbf{i}+4\mathbf{j}$ is
    (a) $4\mathbf{i}-3\mathbf{j}$ (b) $3\mathbf{i}+4\mathbf{j}$ (c) $4\mathbf{i}+3\mathbf{j}$ (d) $3\mathbf{i}-4\mathbf{j}$
11. If $|\mathbf{a}|=2$, $|\mathbf{b}|=3$ and the angle is 30°, then $\mathbf{a}\cdot\mathbf{b}$ is
    (a) 6 (b) $3\sqrt{3}$ (c) 3 (d) $6\sqrt{3}$
12. With $|\mathbf{a}|=2$, $|\mathbf{b}|=3$ and the angle 30°, $|\mathbf{a}\times\mathbf{b}|$ is
    (a) 6 (b) $3\sqrt{3}$ (c) 3 (d) 1.5

::: note Answers and explanations — Set B
**1.** (a) — a·b = 1 − 1 = 0.
**2.** (c) — 2λ − 4 = 0.
**3.** (d) — i × i = 0 and i × j = k, magnitude 1.
**4.** (b) — |3i × 4j| = 12.
**5.** (a) — ½ × 6 = 3.
**6.** (d) — (3, 4): magnitude 5.
**7.** (c) — cos θ = ½.
**8.** (b) — 2 − 2 + 3 = 3.
**9.** (d) — the i-component is 3.
**10.** (a) — 12 − 12 = 0.
**11.** (b) — 6 cos 30° = 3√3.
**12.** (c) — 6 sin 30° = 3.
:::

**Set C — Application (8 questions)**

1. The vectors $\mathbf{i}+\lambda\mathbf{j}+\mathbf{k}$ and $2\mathbf{i}+4\mathbf{j}+2\mathbf{k}$ are parallel when $\lambda$ is
   (a) 1 (b) 2 (c) 4 (d) $\frac{1}{2}$
2. The magnitude of $\mathbf{i}+\mathbf{j}$ is
   (a) 2 (b) 1 (c) 0 (d) $\sqrt{2}$
3. A force $2\mathbf{i}+3\mathbf{j}$ moves a body through $4\mathbf{i}+\mathbf{j}$. The work done is
   (a) 11 (b) 14 (c) 5 (d) 6
4. The area of the triangle $A(0,0)$, $B(4,0)$, $C(0,3)$ found by $\frac{1}{2}|\overrightarrow{AB}\times\overrightarrow{AC}|$ is
   (a) 12 (b) 7 (c) 6 (d) 3.5
5. If $\mathbf{a}\perp\mathbf{b}$ with $|\mathbf{a}|=3$ and $|\mathbf{b}|=4$, then $|\mathbf{a}+\mathbf{b}|^2$ is
   (a) 7 (b) 25 (c) 49 (d) 5
6. The angle between $\mathbf{i}+\mathbf{j}$ and $\mathbf{j}+\mathbf{k}$ is
   (a) 60° (b) 30° (c) 45° (d) 90°
7. The point dividing the join of the origin and $6\mathbf{i}$ in the ratio 1:2 has position vector
   (a) $3\mathbf{i}$ (b) $4\mathbf{i}$ (c) $\mathbf{i}$ (d) $2\mathbf{i}$
8. Which of these is a unit vector?
   (a) $\mathbf{i}+\mathbf{j}$ (b) $\frac{\mathbf{i}+\mathbf{j}}{2}$ (c) $\frac{\mathbf{i}+\mathbf{j}+\mathbf{k}}{\sqrt{3}}$ (d) $\mathbf{i}+\mathbf{j}+\mathbf{k}$

::: note Answers and explanations — Set C
**1.** (b) — the second vector is twice (1, 2, 1).
**2.** (d) — √2.
**3.** (a) — 8 + 3 = 11.
**4.** (c) — AB × AC = 12 k, half is 6.
**5.** (b) — 9 + 16 + 0 = 25.
**6.** (a) — cos θ = 1/(√2·√2) = ½.
**7.** (d) — (1·6i + 2·0)/3 = 2i.
**8.** (c) — its magnitude is √(3/3) = 1.
:::
