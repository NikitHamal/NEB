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

## 3.6 Seeing the ideas: moving shapes, order and the viewport

A transformation is a matrix applied to every vertex. The triangle with vertices (1, 1), (4, 1) and (2, 3) is the test shape for every figure below; the pale triangle is the original and the coloured one is the result. No photograph is used in this unit because the topic is pure geometry; the pictures that matter are the graphs.

```svgfig label="3.1" caption="Five basic transformations of the triangle (1,1), (4,1), (2,3). Translation by (3, 1) gives (4,2), (7,2), (5,4); scaling by (1.5, 1.5) about the origin gives (1.5,1.5), (6,1.5), (3,4.5); rotation by 90 degrees gives (-1,1), (-1,4), (-3,2); reflection about the x-axis gives (1,-1), (4,-1), (2,-3); shear in x with sh = 0.5 gives (1.5,1), (4.5,1), (3.5,3)."
f = Fig(580, 262)
T = [(1, 1), (4, 1), (2, 3)]
cases = [("Translate (3,1)", [(x + 3, y + 1) for x, y in T], AMBER), ("Scale 1.5", [(1.5 * x, 1.5 * y) for x, y in T], TEAL), ("Rotate 90 deg", [(-y, x) for x, y in T], RED), ("Reflect in x-axis", [(x, -y) for x, y in T], NAVY), ("Shear x, sh 0.5", [(x + 0.5 * y, y) for x, y in T], SLATE)]
for i, (n, P, col) in enumerate(cases):
    ox = 6 + (i % 3) * 192; oy = 6 + (i // 3) * 128
    X = lambda v: ox + 62 + v * 12; Y = lambda v: oy + 64 - v * 12
    f.box(ox, oy, 184, 122, "", fill="#f8fafc", stroke="#cbd5e1", sw=1)
    f.line(ox + 6, Y(0), ox + 178, Y(0), color="#94a3b8", sw=0.9); f.line(X(0), oy + 4, X(0), oy + 104, color="#94a3b8", sw=0.9)
    f.poly([(X(x), Y(y)) for x, y in T], fill="#e2e8f0", stroke=SLATE, sw=1)
    f.poly([(X(x), Y(y)) for x, y in P], fill="none", stroke=col, sw=2)
    f.text(ox + 92, oy + 113, n, size=10, color=col, bold=True)
```

```svgfig label="3.2" caption="Order matters. The point (1, 1) is scaled by 2 and translated by (3, 0). Scale first, then translate: (1,1) -> (2,2) -> (5,2). Translate first, then scale: (1,1) -> (4,1) -> (8,2). Matrix products are not commutative, so M2 times M1 is not M1 times M2; with column vectors the matrix nearest the point acts first."
f = Fig(580, 190)
X = lambda v: 40 + v * 30; Y = lambda v: 150 - v * 30
f.line(30, Y(0), 330, Y(0), color="#94a3b8"); f.line(X(0), 150, X(0), 20, color="#94a3b8")
f.circle(X(1), Y(1), 5, fill=SLATE, stroke=SLATE)
f.arrow([(X(1), Y(1)), (X(2), Y(2))], color=TEAL, sw=1.8); f.arrow([(X(2), Y(2)), (X(5), Y(2))], color=TEAL, sw=1.8)
f.arrow([(X(1), Y(1) + 8), (X(4), Y(1) + 8)], color=RED, sw=1.8, dash=True); f.arrow([(X(4), Y(1) + 8), (X(8), Y(2))], color=RED, sw=1.8, dash=True)
f.circle(X(5), Y(2), 6, fill=MINT, stroke=TEAL, label="", size=9); f.circle(X(8), Y(2), 6, fill=ROSE, stroke=RED)
f.text(X(5), Y(2) - 14, "(5,2)", size=10, color=TEAL, bold=True); f.text(X(8), Y(2) - 14, "(8,2)", size=10, color=RED, bold=True)
f.box(360, 20, 214, 56, "Scale, then translate:\nT . S . P = (5, 2)", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(360, 90, 214, 56, "Translate, then scale:\nS . T . P = (8, 2)", fill=ROSE, stroke=RED, size=10.5, bold=True)
f.text(467, 172, "The two results differ by 3 units in x", size=10, color=SLATE, bold=True)
```

```svgfig label="3.3" caption="Rotation about a pivot as three steps: translate the pivot (2, 1) to the origin, rotate by 90 degrees, translate back. The vertices (2,1), (6,1), (4,4) become (0,0), (4,0), (2,3), then (0,0), (0,4), (-3,2), then (2,1), (2,5), (-1,3). The pivot vertex never moves."
f = Fig(580, 214)
panels = [("1 Original", [(2, 1), (6, 1), (4, 4)], SLATE), ("2 Move pivot to origin", [(0, 0), (4, 0), (2, 3)], AMBER), ("3 Rotate 90 deg", [(0, 0), (0, 4), (-3, 2)], RED), ("4 Move back", [(2, 1), (2, 5), (-1, 3)], TEAL)]
for i, (n, P, col) in enumerate(panels):
    ox = 6 + i * 144
    X = lambda v: ox + 70 + v * 15; Y = lambda v: 120 - v * 15
    f.box(ox, 6, 136, 170, "", fill="#f8fafc", stroke="#cbd5e1", sw=1)
    f.line(ox + 4, Y(0), ox + 132, Y(0), color="#94a3b8", sw=0.9); f.line(X(0), 10, X(0), 150, color="#94a3b8", sw=0.9)
    f.poly([(X(x), Y(y)) for x, y in P], fill="none", stroke=col, sw=2)
    f.text(ox + 68, 164, n, size=9.6, color=col, bold=True)
f.text(290, 198, "M = T(2,1) . R(90) . T(-2,-1) = [[0, -1, 3], [1, 0, -1], [0, 0, 1]]", size=10.5, color=NAVY, bold=True)
```

```svgfig label="3.4" caption="Window-to-viewport mapping. The window (20,10)-(120,60) of the world map is shown in the viewport (0,0)-(800,600), so sx = 800/100 = 8 and sy = 600/50 = 12. The point (70, 35) at the centre of the window lands at (400, 300), the centre of the viewport. Because 8 is not 12 the picture is stretched vertically (aspect ratio 2 to 1.33)."
f = Fig(580, 190)
f.box(10, 20, 240, 120, "", fill=SAND, stroke=AMBER, sw=2)
f.text(130, 12, "world window (20,10)-(120,60)", size=10, color=AMBER, bold=True)
f.circle(130, 80, 6, fill=RED, stroke=RED); f.text(130, 102, "(70, 35)", size=10, color=RED, bold=True)
f.arrow([(256, 80), (324, 80)], color=SLATE, sw=2.2, label="sx = 8, sy = 12", lpos=(290, 66))
f.box(330, 20, 240, 120, "", fill=MINT, stroke=TEAL, sw=2)
f.text(450, 12, "viewport (0,0)-(800,600)", size=10, color=TEAL, bold=True)
f.circle(450, 80, 6, fill=RED, stroke=RED); f.text(450, 102, "(400, 300)", size=10, color=RED, bold=True)
f.text(290, 168, "xv = xv_min + (xw - xw_min) sx ,  yv = yv_min + (yw - yw_min) sy", size=10.5, color=NAVY, bold=True)
```

Two photographs make two of the transformations concrete: a reflection in still water, and a wheel turning about its hub. The numbers below are computed with the same 3 x 3 homogeneous matrices as the chapter.

```photogrid label="3.1" cols="2" ratio="1.2" caption="Reflection is a matrix. (a) The Taj Mahal and its image in the long pool: every point (x, y) above the water line appears at (x, -y) below it. (b) The reflection about the x-axis is the matrix with rows (1, 0, 0), (0, -1, 0), (0, 0, 1). Applied to a simple outline of the building it flips the picture, and every distance is unchanged (a rigid motion). The determinant is -1, which signals that left and right hand order is reversed. The matrices for the y-axis and the line y = x are listed with the image of the point (3, 2)."
@ photo id="bcaeng/taj" cap="Taj Mahal and its reflection"
fit 1.2
focus 0.5 0.5
@ svg cap="Reflection about the x-axis (computed)"
pts = [(0, 0), (0, 2), (2, 2), (2, 5), (2.5, 5), (2.5, 2), (3, 2), (3, 4), (4, 5), (5, 4), (6, 5), (7, 4), (7, 2), (7.5, 2), (7.5, 5), (8, 5), (8, 2), (10, 2), (10, 0)]
def mul(A, B): return [[sum(A[i][k] * B[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
def app(M, p): return (M[0][0] * p[0] + M[0][1] * p[1] + M[0][2], M[1][0] * p[0] + M[1][1] * p[1] + M[1][2])
RX = [[1, 0, 0], [0, -1, 0], [0, 0, 1]]; RY = [[-1, 0, 0], [0, 1, 0], [0, 0, 1]]; RD = [[0, 1, 0], [1, 0, 0], [0, 0, 1]]
refl = [app(RX, p) for p in pts]
det = RX[0][0] * RX[1][1] - RX[0][1] * RX[1][0]
d0 = math.dist(pts[3], pts[8]); d1 = math.dist(refl[3], refl[8])
assert det == -1 and abs(d0 - d1) < 1e-12 and app(RX, (3, 2)) == (3, -2) and app(RY, (3, 2)) == (-3, 2) and app(RD, (3, 2)) == (2, 3)
assert mul(RX, RX) == [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
f = Fig(300, 252)
sx, ox, oy = 22, 38, 92
f.line(10, oy, 290, oy, color=SLATE, sw=1.2, dash=True)
f.poly([(ox + x * sx * 0.9, oy - y * 15) for x, y in pts], fill=BLUE, stroke=NAVY, sw=1.3)
f.poly([(ox + x * sx * 0.9, oy - y * 15) for x, y in refl], fill=MINT, stroke=TEAL, sw=1.3)
f.text(10, oy - 6, "x-axis (water line)", size=9, color=SLATE, bold=True, anchor="start")
f.text(150, 12, "(x, y) -> (x, -y):  det = %d,  distances kept" % det, size=9.5, color=NAVY, bold=True)
f.text(10, 196, "image of (3, 2):  x-axis (3, -2)   y-axis (-3, 2)   y = x (2, 3)", size=9.5, color=TEAL, bold=True, anchor="start")
f.box(8, 208, 284, 36, "reflect twice about the same axis and you are back:\nRX x RX = identity matrix (asserted)", fill=SAND, stroke=AMBER, size=9.5, bold=True)
```

```photogrid label="3.2" cols="2" ratio="0.9" caption="Rotation about a pivot, step by step. (a) The London Eye turns about its hub, not about the origin of the picture. (b) A model wheel with hub (2, 1) and radius 2 carries 8 gondolas. The composite matrix M = T(2, 1) x R(45 degrees) x T(-2, -1) moves every gondola 45 degrees round the hub: the first gondola goes from (2, 3) to (0.586, 2.414). Every gondola stays exactly 2 units from the hub, and eight applications of M bring all of them back to where they started. The values are computed in the figure."
@ photo id="bca-cg/eye" cap="London Eye turning about its hub"
fit 0.9
focus 0.5 0.55
@ svg cap="Eight gondolas, M = T R T^-1 (45 degrees)"
th = math.radians(45); c, s = math.cos(th), math.sin(th); hx, hy = 2, 1
def mul(A, B): return [[sum(A[i][k] * B[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
def app(M, p): return (M[0][0] * p[0] + M[0][1] * p[1] + M[0][2], M[1][0] * p[0] + M[1][1] * p[1] + M[1][2])
T1 = [[1, 0, hx], [0, 1, hy], [0, 0, 1]]; R = [[c, -s, 0], [s, c, 0], [0, 0, 1]]; T0 = [[1, 0, -hx], [0, 1, -hy], [0, 0, 1]]
M = mul(T1, mul(R, T0))
g = [(2.0, 3.0)]
for _ in range(7): g.append(app(M, g[-1]))
back = app(M, g[-1])
assert all(abs(math.dist(p, (hx, hy)) - 2) < 1e-9 for p in g) and abs(back[0] - 2) < 1e-9 and abs(back[1] - 3) < 1e-9
assert abs(g[1][0] - 0.5858) < 1e-3 and abs(g[1][1] - 2.4142) < 1e-3
f = Fig(300, 248)
U = 44; X = lambda x: 150 + (x - hx) * U; Y = lambda y: 104 - (y - hy) * U
f.circle(X(hx), Y(hy), 2 * U, fill="#f8fafc", stroke=SLATE, sw=1.2)
for i, (x, y) in enumerate(g):
    f.line(X(hx), Y(hy), X(x), Y(y), color="#cbd5e1", sw=1.0)
    f.circle(X(x), Y(y), 9, fill=(AMBER if i == 0 else BLUE), stroke=(AMBER if i == 0 else NAVY), label=str(i + 1), size=9)
f.circle(X(hx), Y(hy), 4, fill=RED, stroke=RED)
f.text(X(hx) + 8, Y(hy) + 14, "hub (2, 1)", size=9, color=RED, bold=True, anchor="start")
f.text(150, 206, "M = [[%.3f, %.3f, %.3f], [%.3f, %.3f, %.3f], [0, 0, 1]]" % (M[0][0], M[0][1], M[0][2], M[1][0], M[1][1], M[1][2]), size=9, color=NAVY, bold=True)
f.text(150, 224, "gondola 1: (2, 3) -> (%.3f, %.3f); 8 steps = back home" % g[1], size=9.5, color=TEAL, bold=True)
f.text(150, 241, "all 8 stay exactly 2 units from the hub", size=9, color=SLATE, bold=True)
```

### 3.6.1 Eight uses of two-dimensional transformations

1. **Moving windows and icons.** Dragging a window on a screen is a translation of all its pixels. Resizing it is a scaling. Every operating system applies these matrices thousands of times a second.
2. **Zoom and pan in maps.** A map app such as Pathao maps a window of the world to the phone screen using the window-to-viewport formula. Zooming changes the window size; panning moves it. The same formula works for any scale.
3. **Rotating and flipping pictures.** A photo taken sideways is turned upright by a 90 degree rotation. A mirror selfie is a reflection about the y-axis. Image editors use these matrices.
4. **Fonts and logos.** Letters are stored as curves and scaled to any size without loss of quality. Italic text is made by a shear. A newspaper headline and a visiting card use the same outline.
5. **Animation of sprites.** A game moves a character by translating it and turns it by rotating it about its centre. Combining the two needs a composite matrix, usually rotation about a pivot. Smooth motion depends on correct order.
6. **User-interface layout.** A screen designed for one phone is scaled to another with different width and height. Differential scaling or letterboxing keeps buttons usable. The viewport formula decides the stretch.
7. **CAD and drawing tools.** Engineers copy, rotate and mirror parts of a drawing, such as the repeated windows of a building plan. Each operation is a matrix, and a drawing records them for later editing. Undo is simply the inverse matrix.
8. **Printing and exporting.** Sending a page to a printer maps page units to printer dots. A change of paper size is a scaling and a shift. Correct mapping keeps text sharp and margins equal.

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


## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Why are homogeneous coordinates used in computer graphics? Give the matrices of translation, scaling and rotation.**

*Introduction.* Scaling and rotation can be written as 2 x 2 matrix products, but translation is an addition, so a sequence of different transformations cannot be combined into one matrix. Homogeneous coordinates fix this (section 3.1).

1. **Uniform representation.** A point (x, y) is written (x, y, 1), and every transformation becomes a 3 x 3 matrix.
2. **Composition.** A sequence of transformations becomes one matrix by multiplication, applied to many points at once.
3. **Efficiency.** One combined matrix is applied to each vertex instead of several steps.
4. **Hardware.** Graphics hardware is built for fast 3 x 3 and 4 x 4 matrix multiplication.
5. **Extension to 3D.** The same idea with 4 x 4 matrices handles perspective projection.

| Transformation | Matrix |
|---|---|
| Translation (tx, ty) | [[1, 0, tx], [0, 1, ty], [0, 0, 1]] |
| Scaling (sx, sy) | [[sx, 0, 0], [0, sy, 0], [0, 0, 1]] |
| Rotation by t | [[cos t, -sin t, 0], [sin t, cos t, 0], [0, 0, 1]] |

*Example.* Translating (1, 1) by (3, 1) with the matrix gives (4, 2) (Figure 3.1).

*Conclusion.* Homogeneous coordinates let every basic transformation be a matrix, so any combination is one matrix product.

**Q2 (5 marks). Rotate the triangle A(2,1), B(6,1), C(4,4) by 90 degrees anticlockwise about the vertex A. Give the composite matrix and the new vertices.**

*Introduction.* Rotation matrices rotate about the origin, so the pivot A(2, 1) is first moved to the origin, then the rotation is applied, then the shift is undone (section 3.4, Figure 3.3).

*Matrices.* M = T(2, 1) . R(90) . T(-2, -1), applied right to left. With R(90) = [[0, -1, 0], [1, 0, 0], [0, 0, 1]] the product is

M = [[0, -1, 3], [1, 0, -1], [0, 0, 1]].

*Check by steps.* Subtract (2, 1): A' = (0, 0), B' = (4, 0), C' = (2, 3). Rotate (x, y) to (-y, x): (0, 0), (0, 4), (-3, 2). Add (2, 1): **A'' = (2, 1), B'' = (2, 5), C'' = (-1, 3)**.

| Vertex | Original | Result |
|---|---|---|
| A | (2, 1) | (2, 1) |
| B | (6, 1) | (2, 5) |
| C | (4, 4) | (-1, 3) |

*Verification.* The matrix gives for C: x' = -4 + 3 = -1 and y' = 4 - 1 = 3, which agrees. A is unchanged because it is the pivot, and the side lengths are preserved (AB = 4 before and after).

*Conclusion.* Rotation about a pivot is translate, rotate, translate back; the combined matrix does all three in one step.

**Q3 (10 marks). Explain composite two-dimensional transformations, showing that the order matters, and derive the window-to-viewport transformation with a numerical example.**

*Introduction.* Real drawings need several transformations in sequence. Because each is a matrix, the sequence is a matrix product (sections 3.4, 3.5).

*Composite transformations.* For M1 followed by M2 followed by M3 the combined matrix is M = M3 . M2 . M1: the matrix nearest the point acts first. Rotation about an arbitrary pivot, scaling about a point and reflection about an arbitrary line are all built this way (Figure 3.3).

*Order matters.* Matrix multiplication is not commutative. Take the point (1, 1), scaling S(2, 2) and translation T(3, 0). Scale then translate: (1, 1) -> (2, 2) -> (5, 2). Translate then scale: (1, 1) -> (4, 1) -> (8, 2). The results differ (Figure 3.2). Exceptions that commute: two translations, two rotations about the same point, and uniform scaling with rotation.

*Window-to-viewport.* The window is the part of the world to show, with corners (xw_min, yw_min) and (xw_max, yw_max); the viewport is the screen area, with corners (xv_min, yv_min) and (xv_max, yv_max). The steps are: translate the window corner to the origin, scale by sx = (xv_max - xv_min) / (xw_max - xw_min) and sy = (yv_max - yv_min) / (yw_max - yw_min), then translate to the viewport corner. Hence

xv = xv_min + (xw - xw_min) sx and yv = yv_min + (yw - yw_min) sy.

*Example.* Window (20, 10)-(120, 60) to viewport (0, 0)-(800, 600): sx = 800 / 100 = 8 and sy = 600 / 50 = 12. The point (70, 35) maps to xv = (70 - 20) x 8 = 400 and yv = (35 - 10) x 12 = 300, the centre of the viewport (Figure 3.4). Since sx is not equal to sy the picture is stretched vertically; to keep shape, choose sx = sy and leave empty margins (letterboxing).

| Quantity | Value |
|---|---|
| sx | 8 |
| sy | 12 |
| (70, 35) maps to | (400, 300) |
| Window aspect | 2.00 |
| Viewport aspect | 1.33 |

*Conclusion.* Composite transformations and the viewport mapping together move every vertex from world coordinates to screen pixels; the order of the matrices must always be checked.
