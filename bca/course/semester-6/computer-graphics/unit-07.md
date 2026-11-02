---
subject: Computer Graphics and Animation
grade: BCA Semester 6
unit: 7
title: Curves, Surfaces and Computer Animation
hours: 5
area: BCA 351 · Computer Graphics and Animation · Unit 7
---

Lines and circles cannot draw the outline of the letter "ग", the body of a car or the path of a character's hand. Designers need **curves** they can shape with a few handles and that join smoothly: the Bézier and B-spline curves behind every font, vector-drawing program and animation-path editor. And once shapes can be described, animation changes them over time: **keyframes** fix the important poses and the computer fills in the frames between. This unit gives the mathematics of Bézier and B-spline curves with computed points, surface representation, and the techniques and arithmetic of computer animation: interpolation, easing, morphing, frame rates and storage.

::: key What this unit gives you
- Bézier curves: Bernstein basis, the de Casteljau construction, end tangents, subdivision; the uniform cubic B-spline.
- Polygon meshes and the idea of curved surfaces; fractals and subdivision in outline.
- Animation: keyframes, in-betweening, linear and eased interpolation, morphing, the twelve principles.
- Frame rates, storage arithmetic and animation tools and file formats.
:::

## 7.1 Representing curves

A curve can be given **explicitly** (y = f(x), which cannot represent a vertical tangent or a circle), **implicitly** (f(x, y) = 0, such as x² + y² = r²) or **parametrically** (x = x(t), y = y(t)), which is the standard in graphics because it handles any shape and gives a natural *direction*. Designers want **control points** that guide the curve intuitively. A curve **interpolates** its control points if it passes through them (Lagrange or Hermite curves, which can oscillate), or **approximates** them if it is merely pulled towards them (Bézier and B-splines, which are smooth and predictable). Two curve segments joined at a point have **C⁰** continuity if the positions match, **C¹** if the tangents also match and **C²** if the curvature matches too; **G¹** (geometric) only requires tangent *directions* to match.

## 7.2 Bézier curves

A Bézier curve of degree n with control points P₀ … Pₙ is **B(t) = Σ Bᵢ,ₙ(t) · Pᵢ, 0 ≤ t ≤ 1**, where **Bᵢ,ₙ(t) = C(n, i) tⁱ (1 − t)ⁿ⁻ⁱ** are the **Bernstein polynomials**. For the cubic (n = 3): B(t) = (1 − t)³P₀ + 3t(1 − t)²P₁ + 3t²(1 − t)P₂ + t³P₃. Properties: the curve **starts at P₀ and ends at Pₙ**, is tangent to the first and last segments of the control polygon, lies inside the **convex hull** of the control points, and the basis functions are non-negative and sum to 1 (a *partition of unity*), so each point is a weighted average. Moving one control point changes the whole curve (no local control); to get more shape, join several cubics rather than raising the degree.

::: example A cubic Bézier curve
Control points P₀ = (0, 0), P₁ = (1, 3), P₂ = (4, 3), P₃ = (5, 0).

| t | B0 = (1−t)³ | B1 = 3t(1−t)² | B2 = 3t²(1−t) | B3 = t³ | Point B(t) |
|---|---|---|---|---|---|
| 0 | 1.0000 | 0.0000 | 0.0000 | 0.0000 | (0.0000, 0.0000) |
| 0.25 | 0.4219 | 0.4219 | 0.1406 | 0.0156 | (1.0625, 1.6875) |
| 0.5 | 0.1250 | 0.3750 | 0.3750 | 0.1250 | (2.5000, 2.2500) |
| 0.75 | 0.0156 | 0.1406 | 0.4219 | 0.4219 | (3.9375, 1.6875) |
| 1 | 0.0000 | 0.0000 | 0.0000 | 1.0000 | (5.0000, 0.0000) |

At t = 0.5 the weights are 1/8, 3/8, 3/8, 1/8 and the point is **(2.500, 2.250)**, for instance x = (0 + 3·1 + 3·4 + 5)/8 = 20/8 = 2.5 and y = (0 + 9 + 9 + 0)/8 = 2.25. The end tangents are B′(0) = 3·(P1 − P0) = (3, 9) and B′(1) = 3·(P3 − P2) = (3, -9): the curve leaves P₀ towards P₁ and enters P₃ from P₂. The checker confirmed the Bernstein form against the de Casteljau form at eleven values of t and the end derivative against a numerical difference.
:::

### The de Casteljau algorithm

A numerically stable and geometric way to evaluate B(t): repeatedly interpolate between neighbouring points. For t = 0.5: the midpoints of P₀P₁, P₁P₂, P₂P₃ are (0.5, 1.5), (2.5, 3), (4.5, 1.5); the midpoints of those are (1.5, 2.25), (3.5, 2.25); and the midpoint of the last two is **(2.5, 2.25)**, which is B(0.5). The intermediate points are also the control points of the two halves: the left half has control polygon P₀, (0.5, 1.5), (1.5, 2.25), (2.5, 2.25) and the right half (2.5, 2.25), (3.5, 2.25), (4.5, 1.5), P₃. This is **subdivision**, used to draw a curve by splitting until the pieces are flat enough to draw as lines, and to compute intersections.

## 7.3 B-spline curves

A **B-spline** is a piecewise polynomial that gives **local control** (moving a control point changes only a few spans) and automatic continuity between pieces: a **uniform cubic B-spline** has C² continuity everywhere. For four consecutive control points the segment is

**B(t) = (1/6) [t³ t² t 1] · [[−1, 3, −3, 1], [3, −6, 3, 0], [−3, 0, 3, 0], [1, 4, 1, 0]] · [P₀, P₁, P₂, P₃]ᵀ.**

Unlike a Bézier curve, the B-spline does **not** pass through its end control points: at t = 0 it is at (P₀ + 4P₁ + P₂)/6 and at t = 1 at (P₁ + 4P₂ + P₃)/6.

::: example A cubic B-spline segment
Control points (0, 0), (2, 4), (5, 4), (7, 0).

| t | Point on the uniform cubic B-spline segment |
|---|---|
| 0 | (2.1667, 3.3333) |
| 0.25 | (2.8177, 3.7083) |
| 0.5 | (3.5000, 3.8333) |
| 0.75 | (4.1823, 3.7083) |
| 1 | (4.8333, 3.3333) |

At t = 0 the point is **(2.1667, 3.3333)**, which equals (P₀ + 4P₁ + P₂)/6 = (2.1667, 3.3333), and at t = 1 it is **(4.8333, 3.3333)**. The curve stays well inside the control polygon: smoother, but it neither starts at (0, 0) nor ends at (7, 0). Adding the next control point shifts the window by one and gives the next segment, which meets this one with matching position, tangent and curvature. **NURBS** (non-uniform rational B-splines) add weights and knot spacing to represent exact circles and conics, and are the standard in CAD.
:::

| | Bézier | Uniform cubic B-spline |
|---|---|---|
| Passes through end points | Yes | No |
| Local control | No (global) | Yes |
| Continuity between joined pieces | Must be arranged (C¹ by collinear handles) | C² automatic |
| Typical use | Fonts, vector drawing, easing curves | Smooth paths, CAD (as NURBS) |

## 7.4 Surfaces and 3D models

Most 3D objects are stored as **polygon meshes**: lists of **vertices**, **edges** and **faces** (usually triangles), with per-vertex normals and texture coordinates. Meshes are fast to render but need many polygons for smooth shapes. **Parametric surfaces** extend curves: a **Bézier patch** uses a grid of 4 × 4 control points and S(u, v) = Σ Σ Bᵢ(u) Bⱼ(v) Pᵢⱼ. **Subdivision surfaces** repeatedly refine a coarse mesh into a smooth limit (the method of choice in animated films). **Solid modelling** uses **constructive solid geometry (CSG)** (union, intersection and difference of primitives such as spheres and boxes) and **sweeps**. **Fractals** such as the Koch curve and the Mandelbrot set are generated by repeating a rule at smaller scale; they model coastlines, mountains and clouds with self-similarity. **Procedural modelling** and **particle systems** (fire, smoke, rain) generate geometry with rules and random numbers; **3D scanning** and **photogrammetry** capture real objects.

## 7.5 Computer animation

**Animation** creates the illusion of motion by showing a sequence of still images (frames) quickly enough that the eye blends them (persistence of vision). Film runs at 24 frames per second (fps), television at 25 or 30, games at 30 to 120. Compared with 24 fps, 30 fps has **1.25** times as many frames to produce. Production stages: **storyboarding**, **modelling**, **rigging** (building a skeleton and controls), **animation**, **lighting and rendering**, **compositing** and sound.

**Keyframing.** The animator specifies **keyframes** (extreme poses at chosen times); the computer generates the **in-betweens** by interpolating each animated parameter (position, rotation, scale, colour). Linear interpolation gives x(t) = (1 − t)x₀ + t·x₁, a constant speed with abrupt starts and stops that look mechanical. **Easing** curves give natural acceleration and deceleration. A common one is the **smoothstep** function s(t) = 3t² − 2t³, whose slope is zero at both ends. Moving an object from x = 0 to x = 100 in 24 frames:

| Frame | t = f/24 | Linear x = 100t | Ease in-out x = 100(3t²−2t³) |
|---|---|---|---|
| 0 | 0.000 | 0.00 | 0.00 |
| 4 | 0.167 | 16.67 | 7.41 |
| 8 | 0.333 | 33.33 | 25.93 |
| 12 | 0.500 | 50.00 | 50.00 |
| 16 | 0.667 | 66.67 | 74.07 |
| 20 | 0.833 | 83.33 | 92.59 |
| 24 | 1.000 | 100.00 | 100.00 |

At frame 4 the linear motion has already covered 16.67 units but the eased motion only 7.41: it starts slowly. Animators edit these timing curves as Bézier splines in a graph editor. For rotations, interpolating Euler angles can behave badly (gimbal lock), so systems use **quaternions** and **spherical linear interpolation (slerp)** which follow the shortest rotation at constant angular speed.

**Morphing** transforms one shape into another by interpolating corresponding vertices (**shape morphing**) while cross-dissolving colours (**image morphing**, with warped meshes so that the features align). A triangle with vertices (0, 0), (4, 0), (4, 3) morphed to (1, 1), (6, 1), (3, 6):

| t | Vertex 1 | Vertex 2 | Vertex 3 |
|---|---|---|---|
| 0 | (0.00, 0.00) | (4.00, 0.00) | (4.00, 3.00) |
| 0.25 | (0.25, 0.25) | (4.50, 0.25) | (3.75, 3.75) |
| 0.5 | (0.50, 0.50) | (5.00, 0.50) | (3.50, 4.50) |
| 1 | (1.00, 1.00) | (6.00, 1.00) | (3.00, 6.00) |

At t = 0.5 the vertices are **(0.5, 0.5), (5.0, 0.5), (3.5, 4.5)**, the average of corresponding vertices. The result depends on which vertex corresponds to which (a mismatch makes the shape twist or collapse), and the number of vertices must match, so morphing tools add vertices to the simpler shape.

**Other techniques.** **Skeletal animation** drives a mesh with a hierarchy of bones (with *skinning* weights blending the vertices); **forward kinematics** sets joint angles, **inverse kinematics** finds joint angles that place a hand or foot at a target; **motion capture** records real performers; **physics-based animation** simulates cloth, fluids, rigid bodies and particles using equations of motion; **procedural animation** uses rules (crowds, flocks, **boids**). Disney's **twelve principles of animation** (squash and stretch, anticipation, staging, straight-ahead action and pose-to-pose, follow-through and overlapping action, slow in and slow out, arcs, secondary action, timing, exaggeration, solid drawing and appeal) guide quality in 2D and 3D alike.

### Frames, storage and tools

A 90-second clip at 24 fps has 24 × 90 = **2,160 frames**. Uncompressed full-HD frames at 24 bits are 6.22 MB each, so the raw clip would take 2,160 × 6.22 MB = **13.44 GB** (12.51 GiB); video compression (H.264, H.265, AV1) reduces this by two orders of magnitude by storing only the differences between frames. Image sequences (PNG, EXR) are the usual render output; containers such as MP4 hold compressed video; **GIF** and **animated SVG/CSS** are used on the web; **glTF** and **FBX** carry 3D animated models. Tools: **Blender** (free, complete 3D pipeline), Maya, Houdini for 3D; Toon Boom and Krita for 2D; After Effects for motion graphics. For the web, CSS transitions and the **requestAnimationFrame** loop apply the same easing curves to interface elements.

## Chapter summary

- Parametric curves with control points give designers local, predictable shape control; continuity is described as C⁰, C¹, C².
- Bézier curves use Bernstein weights, pass through the end points, lie in the convex hull and are evaluated by de Casteljau subdivision; the cubic B-spline gives C² continuity and local control but does not pass through the end points.
- 3D shapes are polygon meshes, patches, subdivision surfaces, CSG or procedural models.
- Animation uses keyframes and interpolation; easing (smoothstep 3t² − 2t³) replaces robotic constant speed; morphing interpolates corresponding vertices.
- A 90-second 24 fps full-HD clip is 2,160 frames and 13.44 GB uncompressed.

## Practice

1. Write the cubic Bézier formula and give B(0.5) for control points (0, 0), (2, 4), (6, 4), (8, 0).
2. List four properties of Bézier curves.
3. Explain the de Casteljau construction for t = 0.5.
4. Why are B-splines preferred over a single high-degree Bézier curve for long curves?
5. What is the difference between C¹ and G¹ continuity?
6. Compute the smoothstep value at t = 0.25.
7. Linearly interpolate the point from (2, 6) at frame 0 to (10, 2) at frame 8; give the position at frame 3.
8. Name three principles of animation and explain one.
9. Compute the raw size in MB of 10 seconds of 1280 × 720, 24-bit video at 30 fps.
10. Differentiate forward and inverse kinematics.

::: note Answers and worked solutions
**1.** B(t) = (1 − t)³P₀ + 3t(1 − t)²P₁ + 3t²(1 − t)P₂ + t³P₃. At t = 0.5: x = (0 + 3·2 + 3·6 + 8)/8 = 32/8 = 4; y = (0 + 12 + 12 + 0)/8 = 3. **B(0.5) = (4, 3)**.
**2.** Starts and ends at the end control points; tangent to the first and last control-polygon segments; lies in the convex hull; basis functions sum to 1 (and the curve is affine invariant).
**3.** Take midpoints of each adjacent pair of control points, then midpoints of those, and so on until one point remains; that point is B(0.5), and the intermediate points are the control points of the two half-curves.
**4.** B-splines give local control and automatic C² continuity with low degree; a high-degree Bézier changes globally when one point moves and is numerically awkward.
**5.** C¹ requires equal tangent vectors (direction and magnitude); G¹ requires only equal tangent directions.
**6.** 3(0.0625) − 2(0.015625) = 0.1875 − 0.03125 = **0.15625**.
**7.** t = 3/8: x = 2 + 0.375 × 8 = 5, y = 6 − 0.375 × 4 = 4.5: **(5, 4.5)**.
**8.** E.g. slow in and slow out (ease at the ends), anticipation (a preparatory motion before the main action), squash and stretch (deformation conveying weight); anticipation: a character crouches before jumping.
**9.** One frame = 1280 × 720 × 3 = 27,64,800 bytes; 300 frames = 82,94,40,000 bytes = **829.44 MB**.
**10.** Forward kinematics computes the end position from given joint angles; inverse kinematics finds the joint angles that place the end effector at a target.
:::
