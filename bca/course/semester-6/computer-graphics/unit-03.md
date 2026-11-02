---
subject: Computer Graphics and Animation
grade: BCA Semester 6
unit: 3
title: Two-Dimensional Transformations and Viewing
hours: 7
area: BCA 351 · Computer Graphics and Animation · Unit 3
---

To animate a spinning logo, zoom a map or place the same window icon at different places, a program moves, scales and turns shapes by changing the coordinates of their points. Doing this with separate formulas for each operation is clumsy because combining them (rotate *about a point*, then scale, then move) means juggling many formulas. The elegant answer is **homogeneous coordinates**: add a third coordinate so that translation, like rotation and scaling, becomes a matrix multiplication, and any sequence of transformations collapses into a *single* matrix. Every matrix and every transformed point in this unit was recomputed with numpy and the algebraic identities asserted by the checker.

::: key What this unit gives you
- The basic 2D transformations: translation, scaling, rotation, reflection and shear, in homogeneous matrix form.
- Composite transformations, including rotation about an arbitrary pivot; why order matters.
- Window-to-viewport mapping.
- Worked numerical examples on a triangle.
:::

## 3.1 Points, vectors and homogeneous coordinates

A point in the plane is (x, y). In **homogeneous coordinates** it is written (x, y, 1) as a column vector, and a transformation is a 3 × 3 matrix M applied as **P′ = M · P**. Translation, which is addition in ordinary coordinates (x + tₓ, y + t_y), becomes multiplication in this notation, and that is the whole reason for the extra coordinate. A homogeneous point (x, y, w) with w ≠ 0 represents the ordinary point (x/w, y/w); points with w = 0 are *points at infinity* (directions), which Unit 5 uses for perspective.

We use the **column-vector convention**, in which matrices are applied right to left (P′ = M₃M₂M₁P applies M₁ first). Some books use row vectors and left-to-right order; the results are the same, so check the convention before copying a matrix.

## 3.2 The basic transformations

| Transformation | Equations | Matrix |
|---|---|---|
| **Translation** by (tₓ, t_y) | x′ = x + tₓ, y′ = y + t_y | [[1, 0, tₓ], [0, 1, t_y], [0, 0, 1]] |
| **Scaling** by (sₓ, s_y) about the origin | x′ = sₓx, y′ = s_yy | [[sₓ, 0, 0], [0, s_y, 0], [0, 0, 1]] |
| **Rotation** by θ (anticlockwise) about the origin | x′ = x cos θ − y sin θ, y′ = x sin θ + y cos θ | [[cos θ, −sin θ, 0], [sin θ, cos θ, 0], [0, 0, 1]] |
| **Reflection** about the x-axis | x′ = x, y′ = −y | [[1, 0, 0], [0, −1, 0], [0, 0, 1]] |
| **Reflection** about the y-axis | x′ = −x, y′ = y | [[−1, 0, 0], [0, 1, 0], [0, 0, 1]] |
| **Reflection** about the line y = x | x′ = y, y′ = x | [[0, 1, 0], [1, 0, 0], [0, 0, 1]] |
| **Shear in x** by sh | x′ = x + sh·y, y′ = y | [[1, sh, 0], [0, 1, 0], [0, 0, 1]] |

Scaling with sₓ = s_y is **uniform** (preserves shape); different factors give **differential** scaling. A factor greater than 1 enlarges and moves points away from the origin; less than 1 reduces; negative factors reflect. **Rotation** derives from polar coordinates: a point at radius r and angle φ rotated by θ has x′ = r cos(φ + θ) = x cos θ − y sin θ and y′ = r sin(φ + θ) = x sin θ + y cos θ. A rotation matrix is **orthogonal**: its inverse is its transpose, equivalently the rotation by −θ; its determinant is 1, so lengths and angles (and areas) are preserved. The determinant of 45° rotation computed by the checker is 1.0, and for 45° the matrix is

```text
[  0.707  -0.707       0 ]
[  0.707   0.707       0 ]
[      0       0       1 ]
```

The inverse of a translation negates tₓ and t_y; of a scaling uses 1/sₓ and 1/s_y; of a rotation uses −θ (the checker confirms R(30°)·R(−30°) = I: yes). A **shear** slides layers of the picture sideways in proportion to height, used for italic text and in projections.

## 3.3 Transforming an object

The triangle with vertices A(2, 1), B(6, 1), C(4, 5) is transformed by each matrix applied to all three vertices at once (the points are the columns of a 3 × 3 matrix).

| Transformation | New vertices A′, B′, C′ |
|---|---|
| Original | (2.00, 1.00), (6.00, 1.00), (4.00, 5.00) |
| Translation by (3, 2) | (5.00, 3.00), (9.00, 3.00), (7.00, 7.00) |
| Scaling by (2, 0.5) about the origin | (4.00, 0.50), (12.00, 0.50), (8.00, 2.50) |
| Rotation by 90° about the origin | (-1.00, 2.00), (-1.00, 6.00), (-5.00, 4.00) |
| Reflection about y = x | (1.00, 2.00), (1.00, 6.00), (5.00, 4.00) |
| Shear in x with sh = 0.5 | (2.50, 1.00), (6.50, 1.00), (6.50, 5.00) |

Check some by hand: rotation by 90° maps (x, y) to (−y, x), so (2, 1) becomes (−1, 2) and (4, 5) becomes (−5, 4). Scaling by (2, 0.5) takes the base from length 4 to length 8 and the height from 4 to 2: area changes by the determinant 2 × 0.5 = 1, so the area is unchanged even though the shape is distorted. For the shear, the point (4, 5) moves by 0.5 × 5 = 2.5 to x = 6.5, and the base (y = 1) moves only 0.5.

## 3.4 Composite transformations

Applying several transformations in sequence equals multiplying their matrices, **right to left**: for a sequence M₁ then M₂ then M₃ the combined matrix is M = M₃M₂M₁, computed once and then applied to every vertex. This is much cheaper than transforming each point three times.

**Order matters** because matrix multiplication is not commutative (except for special pairs such as two rotations, two translations, or uniform scaling with rotation). Take P = (2, 0). *Rotate by 90° about the origin, then translate by (5, 0)*: P goes to (0, 2) and then to **(5, 2)**. *Translate first, then rotate*: P goes to (7, 0) and then to **(0, 7)**. The same two operations give different answers in different orders.

### Rotation about an arbitrary pivot

Rotation matrices rotate about the *origin*. To rotate about a point (xₚ, yₚ): (1) translate the pivot to the origin, (2) rotate, (3) translate back: **M = T(xₚ, yₚ) · R(θ) · T(−xₚ, −yₚ)**. For a rotation of 30° about the pivot (4, 3):

```text
[  0.866    -0.5   2.036 ]
[    0.5   0.866  -1.598 ]
[      0       0       1 ]
```

The translation column is (xₚ − xₚ cos θ + y_p sin θ, yₚ − xₚ sin θ − yₚ cos θ) = (2.036, -1.598), and the pivot itself is a fixed point (the checker verifies M·(4, 3, 1) = (4, 3, 1)). The triangle moves to (3.27, 0.27), (6.73, 2.27), (3.00, 4.73). **Scaling about a fixed point** (xf, yf) follows the same pattern: M = T(xf, yf) · S(sₓ, s_y) · T(−xf, −yf).

::: example A combined transformation
Scale by 2 about the point (1, 1), then move by (2, 3): M = T(2, 3) · T(1, 1) · S(2, 2) · T(−1, −1), which multiplies out to

```text
[ 2  0  1 ]
[ 0  2  2 ]
[ 0  0  1 ]
```

The point (3, 4) is first shifted by (−1, −1) to (2, 3), scaled to (4, 6), shifted back by (1, 1) to (5, 7) (this is the scaling about (1, 1): 1 + 2·2 = 5 and 1 + 2·3 = 7), and finally moved by (2, 3) to **(7, 10)**; the single matrix gives the same answer in one multiplication.
:::

## 3.5 Coordinate systems and the window-to-viewport transformation

Objects live in **world coordinates** (metres, ward-map units). The part of the world to display is the **window**; the part of the screen on which it appears is the **viewport**. The **window-to-viewport transformation** maps a point (xw, yw) to (xv, yv) preserving its *relative position*:

**xv = xv_min + (xw − xw_min) · sx, yv = yv_min + (yw − yw_min) · sy,**

with **sx = (xv_max − xv_min)/(xw_max − xw_min)** and **sy = (yv_max − yv_min)/(yw_max − yw_min)**. It is a translation of the window corner to the origin, a scaling, and a translation to the viewport corner. If sx ≠ sy the picture is **distorted**; equal factors preserve the aspect ratio.

::: example Window (20, 10)–(120, 60) to viewport (0, 0)–(800, 600)
sx = 800/100 = **8**, sy = 600/50 = **12**. The window's centre point (70, 35) maps to **(400, 300)**, the centre of the viewport, but circles would become tall ellipses because sy exceeds sx. Choosing a window with the viewport's aspect ratio (4:3) removes the distortion. Zooming means shrinking the window; panning means moving it.
:::

## Chapter summary

- Homogeneous coordinates (x, y, 1) turn translation into matrix multiplication; sequences collapse into one matrix applied right to left.
- Translation, scaling, rotation, reflection and shear have standard 3 × 3 matrices; rotation matrices are orthogonal with determinant 1.
- Order matters: translate-then-rotate differs from rotate-then-translate.
- Rotation or scaling about a point is T(p) · R or S · T(−p).
- Window-to-viewport mapping scales and shifts with sx and sy; unequal factors distort.

## Practice

1. Write the homogeneous matrix for translation by (−2, 5) and apply it to (3, 3).
2. Rotate the point (4, 0) by 60° about the origin.
3. Scale the triangle (1, 1), (3, 1), (2, 4) by 2 about the origin.
4. Write the composite matrix to rotate by θ about (xₚ, yₚ).
5. Does rotating then scaling non-uniformly give the same result as scaling then rotating? Explain.
6. Reflect (3, 2) about the x-axis, the y-axis and the line y = x.
7. A shear in y has matrix [[1, 0, 0], [sh, 1, 0], [0, 0, 1]]. Apply sh = 2 to (3, 1).
8. Map the window point (60, 35) from window (20, 10)–(120, 60) to viewport (100, 100)–(500, 300).
9. What is the determinant of a rotation matrix and what does it tell you?
10. Why are homogeneous coordinates used?

::: note Answers and worked solutions
**1.** T = [[1, 0, −2], [0, 1, 5], [0, 0, 1]]; (3, 3) goes to (1, 8).
**2.** x′ = 4 cos 60° = 2, y′ = 4 sin 60° = 3.464: **(2, 3.46)**.
**3.** Vertices become **(2, 2), (6, 2), (4, 8)**.
**4.** M = T(xₚ, yₚ) · R(θ) · T(−xₚ, −yₚ).
**5.** No, in general. Non-uniform scaling stretches along the axes; if applied after a rotation it stretches the rotated shape along the original axes, which is different from rotating a stretched shape. They commute only for uniform scaling.
**6.** About x-axis: (3, −2). About y-axis: (−3, 2). About y = x: (2, 3).
**7.** x′ = 3, y′ = 2·3 + 1 = **7**: (3, 7).
**8.** sx = 400/100 = 4, sy = 200/50 = 4. xv = 100 + (60 − 20)·4 = 260; yv = 100 + (35 − 10)·4 = 200: **(260, 200)**.
**9.** +1; the rotation preserves lengths, angles and area (it is a rigid motion, not a reflection).
**10.** They make translation a matrix product so that all transformations compose by matrix multiplication into a single matrix.
:::
