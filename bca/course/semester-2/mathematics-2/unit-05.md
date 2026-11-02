---
subject: Mathematics II
grade: BCA Semester 2
unit: 5
title: Vectors in Space, Lines and Planes
area: BCA 154 · Mathematics II · Unit 5
---

Three-dimensional geometry is the mathematics of games, graphics engines, robotics and CAD. Vectors describe positions, directions, lines and planes with simple algebra. This unit completes the course with the products of vectors and their geometry.

::: key What this unit gives you
- Vectors in ℝ³: components, length, direction cosines, dot and cross products.
- Areas, volumes and the scalar triple product.
- Equations of lines and planes; distances and angles; intersections.
- Applications in graphics: normals, lighting, back-face culling.
:::

## 5.1 Vectors in three dimensions

A vector **a** = (a₁, a₂, a₃) = a₁**i** + a₂**j** + a₃**k**, with length |**a**| = √(a₁² + a₂² + a₃²). The vector from P(x₁, y₁, z₁) to Q(x₂, y₂, z₂) is PQ = (x₂ − x₁, y₂ − y₁, z₂ − z₁). A **unit vector** has length 1: â = **a**/|**a**|. **Direction cosines** are cos α = a₁/|a|, cos β = a₂/|a|, cos γ = a₃/|a|, with cos²α + cos²β + cos²γ = 1.

**Dot (scalar) product:** **a · b** = a₁b₁ + a₂b₂ + a₃b₃ = |a||b| cos θ. It is zero iff the vectors are perpendicular; it gives angles, projections (scalar projection of a on b = a·b/|b|) and work (W = F · d).

**Cross (vector) product:** **a × b** = (a₂b₃ − a₃b₂, a₃b₁ − a₁b₃, a₁b₂ − a₂b₁), written as the determinant of [[i, j, k], [a₁, a₂, a₃], [b₁, b₂, b₃]]. Its direction is perpendicular to both a and b (right-hand rule); its length is **|a||b| sin θ**, the **area of the parallelogram** spanned by a and b. a × b = −(b × a); a × a = 0; the cross product is *not* commutative or associative.

::: example Worked example
a = (1, 2, 3), b = (4, −5, 6).
**a · b** = 4 − 10 + 18 = **12**; |a| = √14 ≈ 3.742, |b| = √77 ≈ 8.775; cos θ = 12/√1078 = 0.3655 ⇒ **θ ≈ 68.6°**.
**a × b** = (2·6 − 3·(−5), 3·4 − 1·6, 1·(−5) − 2·4) = **(27, 6, −13)**. Check perpendicularity: (27, 6, −13) · a = 27 + 12 − 39 = 0 ✓ and · b = 108 − 30 − 78 = 0 ✓.
**Area of the triangle** with sides a and b from a common vertex = ½ |a × b| = ½ √(729 + 36 + 169) = ½ √934 ≈ **15.28**.
:::

**Scalar triple product** [a, b, c] = a · (b × c) = det of the 3 × 3 matrix with rows a, b, c. Its absolute value is the **volume of the parallelepiped** on a, b, c; the volume of a tetrahedron is one sixth of that. The three vectors are **coplanar** iff the triple product is 0. Example: a = (1, 0, 0), b = (1, 1, 0), c = (1, 1, 1): det = 1, so the volume is 1 and the tetrahedron has volume 1/6.

## 5.2 Lines in space

A line through the point P₀ = (x₀, y₀, z₀) with direction **d** = (l, m, n):

- **Vector form:** **r** = **r₀** + t**d**.
- **Parametric:** x = x₀ + lt, y = y₀ + mt, z = z₀ + nt.
- **Symmetric:** (x − x₀)/l = (y − y₀)/m = (z − z₀)/n.

Through two points A and B, take d = B − A. **Angle between two lines** = angle between their direction vectors. Lines are parallel if their directions are proportional; perpendicular if d₁ · d₂ = 0. In 3-D two lines may also be **skew** (neither parallel nor intersecting).

**Shortest distance from a point P to a line** (through A, direction d): **|AP × d| / |d|**. **Distance between skew lines** through A₁, A₂ with directions d₁, d₂: |(A₂ − A₁) · (d₁ × d₂)| / |d₁ × d₂|.

::: example Worked example
Line L: r = (1, 2, 3) + t(2, −1, 0). Distance of the point P = (3, 1, 3) from L: AP = (2, −1, 0), d = (2, −1, 0); AP × d = **0**, so the distance is 0, and P lies on L (t = 1). For P = (1, 2, 5): AP = (0, 0, 2); AP × d = (0·0 − 2(−1), 2·2 − 0·0, 0) = (2, 4, 0); |AP × d| = √20, |d| = √5, distance = √20/√5 = **2**.
:::

## 5.3 Planes

A plane through P₀ with **normal** vector n = (A, B, C): **n · (r − r₀) = 0**, i.e. **Ax + By + Cz = D** with D = n · r₀. Through three points A, B, C: the normal is n = (B − A) × (C − A).

::: example Worked example
The plane through (1, 0, 0), (0, 1, 0), (0, 0, 1): AB = (−1, 1, 0), AC = (−1, 0, 1); n = AB × AC = (1·1 − 0·0, 0·(−1) − (−1)·1, (−1)·0 − 1·(−1)) = (1, 1, 1). Equation: **x + y + z = 1** (check each point ✓).
:::

**Distance from a point (x₁, y₁, z₁) to the plane Ax + By + Cz = D:** **|Ax₁ + By₁ + Cz₁ − D| / √(A² + B² + C²)**. Example: the point (1, 2, 3) and the plane 2x − y + 2z = 5: |2 − 2 + 6 − 5|/√9 = **1/3**.

**Angle between two planes** = angle between their normals: cos θ = |n₁ · n₂|/(|n₁||n₂|). Planes are parallel if the normals are proportional, perpendicular if n₁ · n₂ = 0. **Intersection of two planes** is a line with direction n₁ × n₂. **Line and plane:** substitute the parametric line into the plane equation; one solution for t gives the intersection point, no solution means parallel, any t means the line lies in the plane. Example: line (t, 2t, 3t) meets x + y + z = 12 when 6t = 12, so t = 2 and the point is (2, 4, 6).

Three planes meet at a point, along a line, or not at all: this is exactly the 3 × 3 linear system of Unit 2 (rank 3, rank 2 consistent, or inconsistent).

## 5.4 Spheres and applications

A **sphere** with centre (a, b, c) and radius r: (x − a)² + (y − b)² + (z − c)² = r². Example: x² + y² + z² − 2x + 4y − 6z = 11 becomes (x − 1)² + (y + 2)² + (z − 3)² = 11 + 1 + 4 + 9 = 25, so the centre is (1, −2, 3) and the radius is **5**.

**In computer graphics:**
- The **normal** to a triangle (v₁, v₂, v₃) is (v₂ − v₁) × (v₃ − v₁); normalise it for lighting.
- **Diffuse lighting:** brightness ∝ max(0, n̂ · l̂), where l̂ is the unit vector towards the light (Lambert's law): a surface facing the light (θ = 0) gets full brightness, at 60° it gets cos 60° = 0.5, at 90° it gets 0.
- **Back-face culling:** skip a triangle whose normal has a non-positive dot product with the view direction.
- **Reflection:** r = d − 2(d · n̂) n̂ for incoming direction d and unit normal n̂.
- **Ray–plane intersection** (ray tracing): t = (D − n · o)/(n · d).
- **Physics:** work W = F · d; torque τ = r × F; magnetic force F = q v × B.

## Formula and fact sheet

- a · b = Σaᵢbᵢ = |a||b|cos θ; a × b has length |a||b| sin θ, direction perpendicular.
- Triangle area = ½|a × b|; parallelepiped volume = |a · (b × c)|; coplanar iff the triple product is 0.
- Line: r = r₀ + td. Distance point–line = |AP × d|/|d|.
- Plane: n · r = D. Distance point–plane = |n · P − D|/|n|. Planes meet along direction n₁ × n₂.
- Sphere: (x − a)² + (y − b)² + (z − c)² = r².
- Reflection r = d − 2(d · n̂)n̂.

## Chapter summary

- The dot product measures alignment and angles; the cross product measures area and gives normals.
- The triple product measures volume and tests coplanarity.
- Lines and planes have vector, parametric and Cartesian forms, with simple distance and angle formulas.
- The same operations drive lighting, culling and reflection in graphics, and torque and work in physics.

## Practice

1. For a = (2, −1, 3), b = (1, 4, −2) find a · b, a × b, the angle between them and the area of the parallelogram.
2. Find the volume of the parallelepiped with edges (1, 2, 3), (0, 1, 4), (5, 6, 0).
3. Are the vectors (1, 2, 3), (2, 4, 6) and (1, 0, 1) coplanar? Is (1, 0, 0), (0, 1, 0), (0, 0, 1) coplanar?
4. Write the equation of the line through A(1, 2, 3) and B(3, 2, 1) and find where it meets the plane x + y + z = 10.
5. Find the plane through (1, 1, 1), (2, 0, 1) and (0, 1, 3).
6. Find the distance from (2, 3, 4) to the plane x + 2y + 2z = 3.
7. Find the angle between the planes x + y + z = 1 and x − y + 2z = 3.
8. Find the centre and radius of x² + y² + z² − 4x + 6y − 2z − 2 = 0.
9. A light shines along direction l̂ = (0, 0, 1) at a surface with unit normal (0.6, 0, 0.8). Find the diffuse brightness factor.
10. Find the reflection of d = (1, −1, 0) off a surface with unit normal (0, 1, 0).

::: note Answers and worked solutions
**1.** a · b = 2 − 4 − 6 = **−8**. a × b = ((−1)(−2) − 3·4, 3·1 − 2·(−2), 2·4 − (−1)·1) = (2 − 12, 3 + 4, 8 + 1) = **(−10, 7, 9)**. |a| = √14, |b| = √21; cos θ = −8/√294 = −0.4666 ⇒ **θ ≈ 117.8°**. Area = |a × b| = √(100 + 49 + 81) = **√230 ≈ 15.17**.
**2.** det [[1, 2, 3], [0, 1, 4], [5, 6, 0]] = 1 (this matrix has det 1, Unit 1): volume **1**.
**3.** First set: the triple product is 0 because the second vector is twice the first, so **coplanar**. Second set: det = 1 ≠ 0, so **not** coplanar.
**4.** d = B − A = (2, 0, −2). Line: (1 + 2t, 2, 3 − 2t). Substituting: (1 + 2t) + 2 + (3 − 2t) = 6, which is never 10, so the line is **parallel** to the plane and never meets it.
**5.** u = (1, −1, 0), v = (−1, 0, 2); n = u × v = ((−1)(2) − 0·0, 0·(−1) − 1·2, 1·0 − (−1)(−1)) = (−2, −2, −1) ⇒ use (2, 2, 1). Plane: 2x + 2y + z = 5 (check (1,1,1): 5 ✓; (2,0,1): 5 ✓; (0,1,3): 5 ✓).
**6.** |2 + 6 + 8 − 3|/√(1 + 4 + 4) = 13/3 ≈ **4.33**.
**7.** n₁ = (1, 1, 1), n₂ = (1, −1, 2): n₁·n₂ = 2; |n₁| = √3, |n₂| = √6; cos θ = 2/√18 = 0.4714 ⇒ **θ ≈ 61.9°**.
**8.** (x − 2)² + (y + 3)² + (z − 1)² = 2 + 4 + 9 + 1 = 16: centre **(2, −3, 1)**, radius **4**.
**9.** n̂ · l̂ = 0.8, so brightness factor **0.8** (surface faces the light at about 36.9°).
**10.** d · n̂ = −1; r = d − 2(−1)n̂ = (1, −1, 0) + 2(0, 1, 0) = **(1, 1, 0)** (the vertical component flips, as a ball bouncing off a floor).
:::
