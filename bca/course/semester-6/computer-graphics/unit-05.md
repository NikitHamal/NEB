---
subject: Computer Graphics and Animation
grade: BCA Semester 6
unit: 5
title: Three-Dimensional Transformations, Projection and Viewing
hours: 7
area: BCA 351 · Computer Graphics and Animation · Unit 5
---

A screen is flat, yet a game shows a mountain range receding into the distance. To get there, a renderer places 3D objects in a world, positions a virtual camera, and *projects* the scene onto a 2D image plane. This unit extends the 2D matrices of Unit 3 to 3D (4 × 4 homogeneous matrices), explains the two families of projection, parallel and perspective, with a worked cube, and describes how a view is specified. The numbers in the tables were computed with numpy; orthogonality and determinant properties of the rotation matrices were asserted by the checker.

::: key What this unit gives you
- 3D homogeneous coordinates and the 4 × 4 matrices for translation, scaling and rotation about each axis.
- Composite 3D transformations, including rotation about a line parallel to an axis.
- Parallel (orthographic) and perspective projection with the projection matrix and perspective divide.
- The viewing pipeline, view volume, and back-face detection with normal vectors.
:::

## 5.1 Three-dimensional homogeneous transformations

A 3D point is the column vector (x, y, z, 1), and transformations are 4 × 4 matrices. We use a **right-handed** coordinate system: x to the right, y up, and z towards the viewer (so a camera looks down the negative z-axis). Rotation angles are positive anticlockwise when looking from the positive end of the axis towards the origin.

| Transformation | Matrix |
|---|---|
| **Translation** (tₓ, t_y, t_z) | Identity with tₓ, t_y, t_z in the fourth column |
| **Scaling** (sₓ, s_y, s_z) | diag(sₓ, s_y, s_z, 1) |
| **Rotation about z** by θ | [[cos θ, −sin θ, 0, 0], [sin θ, cos θ, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]] |
| **Rotation about x** by θ | [[1, 0, 0, 0], [0, cos θ, −sin θ, 0], [0, sin θ, cos θ, 0], [0, 0, 0, 1]] |
| **Rotation about y** by θ | [[cos θ, 0, sin θ, 0], [0, 1, 0, 0], [−sin θ, 0, cos θ, 0], [0, 0, 0, 1]] |

Rotation about z is exactly the 2D rotation, with z unchanged; the other two are obtained by cycling the axes (x → y → z → x), which is why the sign of sin θ in the *y*-rotation looks reversed. Reflections about a coordinate plane negate one coordinate (for instance the xy-plane: z → −z), and shears add multiples of one coordinate to another. As in 2D, composite transformations multiply right to left, and the **order matters**: rotating 90° about x then 90° about y differs from the reverse order.

Applying each to the point (1, 2, 3):

| Transformation | Result |
|---|---|
| Rotation by 90° about z | (-2.000, 1.000, 3.000) |
| Rotation by 90° about x | (1.000, -3.000, 2.000) |
| Rotation by 90° about y | (3.000, 2.000, -1.000) |
| Translation by (2, −1, 4) | (3.000, 1.000, 7.000) |
| Uniform scaling by 2 | (2.000, 4.000, 6.000) |

By hand, rotation about z by 90° maps (x, y) → (−y, x), so (1, 2, 3) → (−2, 1, 3); rotation about x by 90° maps (y, z) → (−z, y), so (1, 2, 3) → (1, −3, 2); about y by 90° maps (x, z) → (z, −x), giving (3, 2, −1). The checker confirmed that every rotation matrix times its transpose is the identity and its 3 × 3 determinant is 1, so rotations preserve lengths.

**Rotation about an arbitrary axis.** For an axis *parallel* to a coordinate axis through a point, translate the axis onto the coordinate axis, rotate, translate back (as in 2D). For a general axis the standard method aligns the axis with a coordinate axis through two rotations, rotates, and undoes them; the compact alternative is **Rodrigues' formula** or a **quaternion**, which also avoids *gimbal lock* when Euler angles are used.

::: example Rotating about a vertical line at x = 0, z = 2
To turn an object 90° about the vertical line through (0, y, 2): M = T(0, 0, 2)·R_y(90°)·T(0, 0, −2):

```text
[  0   0   1  -2 ]
[  0   1   0   0 ]
[ -1   0   0   2 ]
[  0   0   0   1 ]
```

The point (1, 0, 2), which lies 1 unit to the right of the axis, goes to **(0.000, 0.000, 1.000)**: it is still 1 unit from the axis, but now lies along the z direction (at z = 1) instead of the x direction, as a quarter turn about the line should do. (Writing the translations the other way round, T(0, 0, −2)·R_y·T(0, 0, 2), would rotate about the wrong line and send the point to (4, 0, −3): the order of the outer translations matters.)
:::

## 5.2 Projection

**Projection** maps 3D points onto a 2D **projection plane** along **projectors** (lines). There are two families.

**Parallel projection** sends projectors in a *common direction*. In **orthographic** projection the direction is perpendicular to the plane; onto the plane z = 0 the matrix simply drops z: (x, y, z) → (x, y). It preserves parallel lines and relative sizes (good for engineering drawings: top, front and side views). **Oblique** projection (cavalier, cabinet) uses a slanted direction, keeping one face true-shape; **axonometric** projections (isometric) rotate the object so that three faces are visible with equal foreshortening along the axes.

**Perspective projection** sends projectors through a single **centre of projection** (the eye), so that distant objects appear smaller, as in a photograph. Put the eye at the origin looking down +z with the projection plane at z = d. By similar triangles a point (x, y, z) maps to

**x′ = x·d / z, y′ = y·d / z.**

In homogeneous form the matrix is [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 1/d, 0]]: multiplying (x, y, z, 1) gives (x, y, z, z/d), and the **perspective divide** (dividing by the fourth coordinate w = z/d) yields (x·d/z, y·d/z, d). The point (1, 1, 4) with d = 2 becomes the homogeneous point **(1, 1, 4, 2)**, which divides to **(0.50, 0.50, 2.00)**: the projected x and y are 0.50, and the depth value is kept for hidden-surface tests.

A cube of side 2 centred on the z-axis with its near face at z = 4 and its far face at z = 6, viewed with d = 2:

| Vertex (x, y, z) | Orthographic (x, y) | Perspective (x·d/z, y·d/z), d = 2 |
|---|---|---|
| (-1, -1, 4) | (-1, -1) | (-0.500, -0.500) |
| (1, -1, 4) | (1, -1) | (0.500, -0.500) |
| (-1, 1, 4) | (-1, 1) | (-0.500, 0.500) |
| (1, 1, 4) | (1, 1) | (0.500, 0.500) |
| (-1, -1, 6) | (-1, -1) | (-0.333, -0.333) |
| (1, -1, 6) | (1, -1) | (0.333, -0.333) |
| (-1, 1, 6) | (-1, 1) | (-0.333, 0.333) |
| (1, 1, 6) | (1, 1) | (0.333, 0.333) |

The near face projects to ±0.50 and the far face to ±0.333: the far face is smaller by the ratio 6/4 = 1.50, which is perspective **foreshortening**. In orthographic projection both faces would coincide (±1). Parallel edges that are not parallel to the projection plane (the cube's edges along z) *converge* to a **vanishing point**: lines parallel to the z-axis meet at the centre. Perspective projections are described by the number of principal vanishing points (one-, two- or three-point perspective). Because depth is divided out, perspective is not an affine transformation: parallel lines do not stay parallel, and equal distances do not remain equal.

| | Parallel (orthographic) | Perspective |
|---|---|---|
| Projectors | Parallel | Converge at the eye |
| Size vs distance | Constant | Falls with distance |
| Parallel lines | Stay parallel | Converge at vanishing points |
| Use | CAD, engineering drawings | Games, film, realistic images |

## 5.3 Viewing

To view a scene from an arbitrary camera, a **viewing transformation** first moves the world so that the camera sits at the origin looking along a standard direction. A camera is described by an **eye position**, a **look-at point** and an **up vector**. From these a camera coordinate frame is built: the *forward* axis f = normalise(look-at − eye); the *right* axis r = normalise(f × up); and the true *up* axis u = r × f. The view matrix is a rotation (rows r, u, −f) times a translation by −eye. For the simple case of a camera at (0, 0, 10) looking at the origin, the view matrix is just a translation by (0, 0, −10): the point (1, 2, 3) goes to (1, 2, -7), 7 units in front of the camera.

The **view volume** is the region the camera sees: a **box** for orthographic projection, and a **frustum** (truncated pyramid bounded by the near and far planes and four side planes, set by the field of view and aspect ratio) for perspective. Geometry outside it is clipped (Unit 4, in 3D). A **perspective projection matrix** maps the frustum to a standard cube (**normalised device coordinates**), after which the *same* clipping and viewport mapping work for every camera.

The **3D viewing pipeline** is therefore: world coordinates → *view transformation* → camera coordinates → *projection transformation* → clip coordinates → clipping → perspective divide → normalised coordinates → *viewport transformation* → screen coordinates.

## 5.4 Back-face detection

A closed solid has faces pointing outward; faces turned away from the viewer cannot be seen, and discarding them (**back-face culling**) halves the work for typical models. A polygon's **normal** is the cross product of two edges taken in a consistent (say anticlockwise) vertex order. If **N · V > 0**, where V points from the surface towards the viewer, the face is front-facing; if N · V ≤ 0 it is a back face.

For the triangle A(2, 0, 5), B(4, 0, 5), C(2, 3, 5): N = (B − A) × (C − A) = (2, 0, 0) × (0, 3, 0) = **(0, 0, 6)**. With the viewer looking along −z so that V = (0, 0, 1), N · V = **6** > 0, so the face is **visible**. If the vertex order is reversed (A, C, B) the normal becomes (0, 0, -6) and the face is culled. Back-face culling is only a *partial* hidden-surface method: it cannot decide the order between two front-facing faces, so overlapping objects need the methods of Unit 6.

## Chapter summary

- 3D transformations are 4 × 4 matrices; rotations about x, y, z are orthogonal matrices with determinant 1; order of composition matters.
- Orthographic projection drops z; perspective projection divides by depth: x′ = x·d/z, y′ = y·d/z, via a matrix and a perspective divide.
- Perspective causes foreshortening and vanishing points; parallel projection preserves parallel lines and sizes.
- Viewing needs an eye, a look-at point and an up vector, a view volume (frustum) and a pipeline ending in the viewport transform.
- Back-face culling tests N · V > 0 using the polygon normal.

## Practice

1. Write the 4 × 4 matrix for translation by (3, −2, 5).
2. Rotate (0, 1, 0) by 90° about the x-axis.
3. Rotate (1, 0, 0) by 90° about the z-axis then 90° about the y-axis. Give the final point.
4. Project the point (4, 2, 8) with perspective projection d = 4.
5. Why does perspective projection need a division by depth?
6. What is a vanishing point?
7. Differentiate orthographic and oblique projection.
8. Compute the normal of the triangle (0, 0, 0), (1, 0, 0), (0, 1, 0) taken in that order.
9. For viewer direction V = (0, 0, 1), is the triangle in question 8 front-facing?
10. Why is back-face culling not enough for hidden-surface removal?

::: note Answers and worked solutions
**1.** Identity with last column (3, −2, 5, 1).
**2.** Rotation about x maps (y, z) → (y cos θ − z sin θ, y sin θ + z cos θ) = (0 − 0, 1 + 0) → y′ = 0, z′ = 1: **(0, 0, 1)**.
**3.** About z: (1, 0, 0) → (0, 1, 0). About y: the matrix [[0, 0, 1], [0, 1, 0], [−1, 0, 0]] applied to (0, 1, 0) gives (0, 1, 0). Final point **(0, 1, 0)** (it lies on the y-axis, which the y-rotation leaves fixed).
**4.** x′ = 4·4/8 = **2**, y′ = 2·4/8 = **1**: (2, 1).
**5.** Similar triangles: image size is proportional to 1/distance, which is a division by z.
**6.** The point at which projections of parallel lines (not parallel to the image plane) meet.
**7.** Orthographic projectors are perpendicular to the projection plane; oblique projectors are parallel to each other but slanted.
**8.** (1, 0, 0) × (0, 1, 0) = (0, 0, 1).
**9.** N · V = 1 > 0: front-facing.
**10.** It only removes faces pointing away; two front-facing surfaces can still overlap, so their depth order must be resolved (Z-buffer, painter's algorithm).
:::
