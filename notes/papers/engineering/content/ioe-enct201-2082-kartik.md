---
file: NEBians-IOE-Past-Paper-Computer-Graphics-and-Visualization-ENCT201-2082-Kartik.pdf
subject: Computer Graphics and Visualization
level: BE · Year II / Part I
code: ENCT201
year_bs: 2082 Kartik
cal: BS
year_ad: 2025
stream: BEI, BCT
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Back (New Course). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
Calculate the time required to display a pixel on the monitor of size $1024\times768$ with refresh rate of 60 Hz. Draw block diagram of 3D viewing pipeline. [[3+2]]

@q 2
(a) How is the symmetric property vital while drawing an ellipse? Write an algorithm to draw ellipse in raster graphics system. [[2+5]]

(b) Explain Weiler Atherton polygon clipping with an example. [[5]]

@q 3
(a) Explain the composite rotation in 2D transformation. Given the point (0,0), (1,0), (1,1) and (0,1) where $X_{ref}=-1$ and $Sh_y=0.5$. Calculate and sketch shearing transformation new coordinates. [[4]]

(b) Reflect the object (2, 3), (4,3), (4,5) about the line $y=x+1$. [[4]]

(c) Why we need perspective projection in 3D environment? Explain transformation from world to viewing coordinates. [[2+3]]

@q 4
Illustrate space partitioning representation in brief. How polygon meshes support to represent 3D object? Explain with relevant figures. [[3+3]]

@q 5
Differentiate between image-space and object-space methods for hidden surface detection. How does A-Buffer method determine the hidden surfaces? [[1+4]]

@q 6
Define Specular reflection. Explain Fast Phong shading models with relevant expression. [[1+4]]

@q 7
What is anti-aliasing methods in computer animation? Illustrate typical process of morphing in computer graphics. [[2+5]]

@q 8
Explain key components of a virtual reality system in brief. Write down an application of AR system. [[5+2]]
<!-- SOLUTIONS -->

@s 1
**Time to display one pixel.** The monitor is refreshed 60 times per second, so one frame takes

$$T_{frame}=\frac1{60}\ \text{s}=16.67\ \text{ms}.$$

A frame has $1024\times768=786\,432$ pixels, so (ignoring horizontal and vertical retrace)

$$T_{pixel}=\frac{16.67\ \text{ms}}{786\,432}=\frac{1}{60\times786\,432}\ \text{s}\approx\boxed{21.2\ \text{ns}}$$

(equivalently a pixel clock of about $47.2$ MHz, since $60\times786\,432=47.19\times10^{6}$ pixels per second; with retrace overhead of roughly 25 % the real pixel clock is about 65 MHz, as in the standard XGA mode).

**3D viewing pipeline.** The scene description passes through a sequence of coordinate systems:

```figure caption="Question 1: the 3D viewing pipeline."
import matplotlib.patches as mp
fig, ax = plt.subplots(figsize=(6.4, 2.3)); ax.axis("off"); ax.set_xlim(0, 12.6); ax.set_ylim(0, 3.4)
names = ["Modelling\ncoordinates", "World\ncoordinates", "Viewing\ncoordinates", "Projection\ncoordinates", "Normalised\ncoordinates", "Device\ncoordinates"]
tr = ["modelling\ntransform", "viewing\ntransform", "projection\ntransform", "normalisation\n+ 3D clipping", "viewport\ntransform"]
for i, n in enumerate(names):
    x = 0.1 + i * 2.1
    ax.add_patch(mp.FancyBboxPatch((x, 1.2), 1.7, 1.2, boxstyle="round,pad=0.02,rounding_size=0.1", fc="white", ec=INK, lw=1.2))
    ax.text(x + 0.85, 1.8, n, ha="center", va="center", fontsize=6.6)
    if i < 5:
        ax.annotate("", xy=(x + 2.1, 1.8), xytext=(x + 1.7, 1.8), arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=1.2))
        ax.text(x + 1.9, 0.75, tr[i], ha="center", va="center", fontsize=5.6, color="#b00020")
```

1. **Modelling transformation** places each object (defined in its own modelling coordinates) into the common world coordinate system. 2. **Viewing transformation** moves and rotates the world so the camera (view reference point, view-plane normal, view-up vector) sits at the origin looking along an axis. 3. **Projection transformation** (parallel or perspective) maps the 3D view volume onto the view plane. 4. **Normalisation and clipping** map the view volume to a canonical cube and clip against it. 5. **Workstation (viewport) transformation** maps the normalised coordinates to the pixels of the display device, where hidden surfaces are removed and the pixels are shaded.

@s 2
**(a) Why symmetry matters.** An ellipse centred at the origin with semi-axes $r_x,r_y$, $\dfrac{x^2}{r_x^2}+\dfrac{y^2}{r_y^2}=1$, is symmetric about both axes. If $(x,y)$ is on the curve, so are $(-x,y)$, $(x,-y)$ and $(-x,-y)$. So only **one quadrant** has to be computed and each calculated point is plotted **four times**:

```figure caption="Question 2(a): four-way symmetry of the ellipse; a point (x, y) of the first quadrant gives (-x, y), (x, -y) and (-x, -y)."
import numpy as np
fig, ax = plt.subplots(figsize=(3.4, 2.5)); ax.set_aspect("equal"); ax.axis("off")
t = np.linspace(0, 2 * np.pi, 200); ax.plot(8 * np.cos(t), 6 * np.sin(t), color=INK, lw=1.2)
ax.annotate("", xy=(10, 0), xytext=(-10, 0), arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=0.8)); ax.annotate("", xy=(0, 8), xytext=(0, -8), arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=0.8))
for (x, y, s) in ((5, 4.2, "(x, y)"), (-5, 4.2, "(-x, y)"), (5, -4.2, "(x, -y)"), (-5, -4.2, "(-x, -y)")):
    ax.plot([x], [y], "o", color=ACCENT, ms=4); ax.text(x, y + (0.9 if y > 0 else -1.5), s, ha="center", fontsize=7, color="#b00020")
ax.text(9.2, -1.3, "x", fontsize=7); ax.text(0.5, 7.4, "y", fontsize=7)
```

This cuts the work to a quarter, the calculated points for the other three quadrants cost no arithmetic, and the curve is guaranteed symmetric. (For a circle the 8-way symmetry $(\pm x,\pm y),(\pm y,\pm x)$ is available, but an ellipse has only 4-way symmetry because $r_x\ne r_y$.) The first quadrant is split into two regions at the point where the slope of the tangent is $-1$:

- **Region 1** (slope magnitude $<1$): step in $x$ by $+1$, decide whether $y$ stays or becomes $y-1$.
- **Region 2** (slope magnitude $>1$): step in $y$ by $-1$, decide whether $x$ stays or becomes $x+1$.

**Midpoint ellipse algorithm.** Ellipse function $f(x,y)=r_y^2x^2+r_x^2y^2-r_x^2r_y^2$: $f<0$ inside, $f=0$ on, $f>0$ outside the ellipse. Start at $(0,r_y)$.

```text
Input: rx, ry, centre (xc, yc)
x = 0; y = ry
dx = 2*ry^2*x;  dy = 2*rx^2*y
p1 = ry^2 - rx^2*ry + rx^2/4            # decision parameter, region 1
plot 4 points (xc ± x, yc ± y)
while dx < dy:                          # region 1
    x = x + 1;  dx = dx + 2*ry^2
    if p1 < 0:  p1 = p1 + dx + ry^2
    else:       y = y - 1;  dy = dy - 2*rx^2;  p1 = p1 + dx - dy + ry^2
    plot 4 points (xc ± x, yc ± y)
p2 = ry^2*(x + 1/2)^2 + rx^2*(y - 1)^2 - rx^2*ry^2    # region 2
while y > 0:
    y = y - 1;  dy = dy - 2*rx^2
    if p2 > 0:  p2 = p2 + rx^2 - dy
    else:       x = x + 1;  dx = dx + 2*ry^2;  p2 = p2 + dx - dy + rx^2
    plot 4 points (xc ± x, yc ± y)
```

*Example (computed by running the algorithm).* For $r_x=8$, $r_y=6$ and centre at the origin, the first-quadrant points are: region 1: $(0,6),(1,6),(2,6),(3,6),(4,5),(5,5),(6,4),(7,3)$; region 2: $(8,2),(8,1),(8,0)$. The initial parameter is $p1_0=36-384+16=-332$. Each point is then mirrored into the other three quadrants.

**(b) Weiler-Atherton polygon clipping.** Sutherland-Hodgman produces false connecting edges when a concave polygon is clipped into several pieces; Weiler-Atherton handles this by walking along the *polygon* and the *clip window* alternately. Both are listed as vertex sequences in the same orientation (counter-clockwise here).

1. Find all intersection points of the subject polygon with the clip window. Label each **entering** (the polygon edge goes from outside to inside) or **leaving**, and insert it into both vertex lists.
2. Start at an *entering* intersection and follow the **subject polygon** edges (inside the window) until a *leaving* intersection is reached.
3. At the leaving point turn onto the **clip window boundary** and follow it (same direction) to the next intersection point on the window list.
4. Go on, switching between the subject and the window, until the starting point is reached again: this closes one clipped polygon.
5. If entering intersections remain that were not used, start a new output polygon from one of them. Stop when all are used.

**Example.** Clip window $[0,4]\times[0,4]$ and subject triangle $A(1,-1)$, $B(5,3)$, $C(1,5)$ (counter-clockwise).

```figure caption="Question 2(b): Weiler-Atherton clipping of triangle ABC against the window; I = entering, O = leaving intersection. Output polygon (shaded): I1 O1 I2 O2 I3 O3."
import matplotlib.patches as mp
fig, ax = plt.subplots(figsize=(3.8, 3.3)); ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-1, 6.2); ax.set_ylim(-1.6, 5.7)
ax.add_patch(mp.Rectangle((0, 0), 4, 4, fc="none", ec=INK, lw=1.6)); ax.text(3.8, -0.5, "clip window", fontsize=6.5)
tri = [(1, -1), (5, 3), (1, 5)]; ax.add_patch(mp.Polygon(tri, fc="none", ec=ACCENT, lw=1.2, ls="--"))
out = [(2, 0), (4, 2), (4, 3.5), (3, 4), (1, 4), (1, 0)]; ax.add_patch(mp.Polygon(out, fc="#1d6fb833", ec="#b00020", lw=1.4))
for (p, n) in zip(tri, "ABC"): ax.text(p[0] + (0.2 if n == "B" else -0.35), p[1] + (-0.35 if n == "A" else 0.15), n, fontsize=8)
for (p, n, dx, dy) in (((2, 0), "I1", 0.1, -0.5), ((4, 2), "O1", 0.15, -0.35), ((4, 3.5), "I2", 0.2, 0.0), ((3, 4), "O2", 0.0, 0.3), ((1, 4), "I3", -0.45, 0.2), ((1, 0), "O3", -0.55, -0.3)):
    ax.plot([p[0]], [p[1]], "o", color="#b00020", ms=4); ax.text(p[0] + dx, p[1] + dy, n, fontsize=7, color="#b00020")
```

- Intersections: $AB$ enters at $I_1(2,0)$ and leaves at $O_1(4,2)$; $BC$ enters at $I_2(4,3.5)$ and leaves at $O_2(3,4)$; $CA$ enters at $I_3(1,4)$ and leaves at $O_3(1,0)$.
- Start at $I_1$: follow the triangle to $O_1(4,2)$; turn onto the window (counter-clockwise, up the right side) to $I_2(4,3.5)$; follow the triangle to $O_2(3,4)$; follow the window left along the top to $I_3(1,4)$; follow the triangle to $O_3(1,0)$; follow the window along the bottom to $I_1(2,0)$, closing the loop.
- Clipped polygon: $(2,0),(4,2),(4,3.5),(3,4),(1,4),(1,0)$, a hexagon of area 9.75 square units (shoelace formula, cross-checked with Sutherland-Hodgman).

All three entering points were used, so one output polygon results. For a concave subject that leaves and re-enters the window the algorithm outputs several polygons, which is its advantage over Sutherland-Hodgman.

@s 3
**(a) Composite rotation.** Rotation about a pivot $(x_r,y_r)$ is a composite of three basic transformations: (1) translate the pivot to the origin, (2) rotate by $\theta$ about the origin, (3) translate back:

$$M=T(x_r,y_r)\,R(\theta)\,T(-x_r,-y_r)=\begin{bmatrix}\cos\theta&-\sin\theta&x_r(1-\cos\theta)+y_r\sin\theta\\ \sin\theta&\cos\theta&y_r(1-\cos\theta)-x_r\sin\theta\\0&0&1\end{bmatrix}$$

Two successive rotations about the origin combine by adding the angles, $R(\theta_2)R(\theta_1)=R(\theta_1+\theta_2)$. In general the order matters: matrices are multiplied right to left in the order the operations are applied.

**Shear.** The y-direction shear relative to the reference line $x=x_{ref}$ is

$$x'=x,\qquad y'=y+Sh_y\,(x-x_{ref}),\qquad \begin{bmatrix}1&0&0\\Sh_y&1&-Sh_y\,x_{ref}\\0&0&1\end{bmatrix}.$$

With $x_{ref}=-1$ and $Sh_y=0.5$: $y'=y+0.5(x+1)$.

| Point | $x'$ | $y'$ |
|---|---|---|
| (0, 0) | 0 | $0+0.5(0+1)=0.5$ |
| (1, 0) | 1 | $0+0.5(1+1)=1$ |
| (1, 1) | 1 | $1+0.5(2)=2$ |
| (0, 1) | 0 | $1+0.5(1)=1.5$ |

New coordinates: $(0,0.5),\ (1,1),\ (1,2),\ (0,1.5)$.

```figure caption="Question 3(a): unit square sheared in the y-direction (Sh_y = 0.5, x_ref = -1)."
import matplotlib.patches as mp
fig, ax = plt.subplots(figsize=(3.2, 2.9)); ax.set_aspect("equal"); ax.set_xlim(-1.6, 2); ax.set_ylim(-0.5, 2.5)
ax.axvline(-1, color=MUTED, ls=":", lw=1); ax.text(-1.55, 2.2, "x = x_ref = -1", fontsize=6.5, color=MUTED)
ax.add_patch(mp.Polygon([(0, 0), (1, 0), (1, 1), (0, 1)], fc="none", ec=INK, lw=1.4))
ax.add_patch(mp.Polygon([(0, 0.5), (1, 1), (1, 2), (0, 1.5)], fc="#1d6fb822", ec=ACCENT, lw=1.4))
ax.set_xlabel("x", fontsize=7); ax.set_ylabel("y", fontsize=7); ax.tick_params(labelsize=6); ax.grid(alpha=0.25)
```

**(b) Reflection about $y=x+1$.** The line has slope 1 and intercept 1, so: (1) translate down by 1, $T(0,-1)$; (2) reflect about $y=x$, matrix $\begin{bmatrix}0&1&0\\1&0&0\\0&0&1\end{bmatrix}$; (3) translate back up, $T(0,1)$.

$$M=T(0,1)\,R_{y=x}\,T(0,-1)=\begin{bmatrix}0&1&-1\\1&0&1\\0&0&1\end{bmatrix},\qquad (x,y)\mapsto(y-1,\ x+1).$$

| Vertex | $(x,y)$ | image $(y-1,\ x+1)$ |
|---|---|---|
| A | (2, 3) | (2, 3) |
| B | (4, 3) | (2, 5) |
| C | (4, 5) | (4, 5) |

$A$ and $C$ lie on the mirror line ($3=2+1$ and $5=4+1$), so they do not move. The reflected triangle is $(2,3),(2,5),(4,5)$. Check: $B(4,3)$ and $B'(2,5)$ are at the same distance $2/\sqrt2$ from the line $x-y+1=0$, and the segment $BB'$ is perpendicular to it.

**(c) Why perspective projection?** Parallel (orthographic) projection preserves sizes and parallelism but looks unnatural: an object far from the viewer keeps the same size. Perspective projection makes the projectors converge on the centre of projection, so **distant objects appear smaller** (perspective foreshortening) and parallel lines not parallel to the view plane meet at vanishing points. It gives the realistic view of the human eye and camera, which is needed for walk-throughs, games, simulators and architectural visualisation. With centre of projection at the origin and view plane $z=d$: $x_p=x\,d/z$, $y_p=y\,d/z$.

**World to viewing coordinates.** The viewer is described by the view reference point $\mathbf P_0$ (the eye / origin of the viewing system), the view-plane normal $\mathbf N$ and the view-up vector $\mathbf V$.

1. Translate $\mathbf P_0$ to the origin: $T=\begin{bmatrix}1&0&0&-x_0\\0&1&0&-y_0\\0&0&1&-z_0\\0&0&0&1\end{bmatrix}$.
2. Build the orthonormal viewing axes: $\mathbf n=\dfrac{\mathbf N}{|\mathbf N|}$, $\mathbf u=\dfrac{\mathbf V\times\mathbf n}{|\mathbf V\times\mathbf n|}$, $\mathbf v=\mathbf n\times\mathbf u$.
3. Rotate so that $\mathbf u,\mathbf v,\mathbf n$ become the $x_v,y_v,z_v$ axes: $R=\begin{bmatrix}u_x&u_y&u_z&0\\v_x&v_y&v_z&0\\n_x&n_y&n_z&0\\0&0&0&1\end{bmatrix}$.

$$\mathbf P_{view}=R\,T\,\mathbf P_{world}$$

(equivalent to the usual rotations $R_zR_yR_x$ that align $\mathbf N$ with the $z$-axis).

@s 4
**Space-partitioning representation.** The 3D space containing the object is divided into non-overlapping regions, and each region is tagged as inside, outside or partly occupied; the solid is the union of the occupied regions. Main schemes:

- **Octree.** A cube enclosing the object is subdivided recursively into 8 equal octants. An octant that is completely empty or completely full becomes a leaf (white/black); a partly full octant (grey) is subdivided again, down to a resolution limit. Each node has 8 children, so the data structure is a tree of degree 8; it is the 3D analogue of the quadtree and is compact for large uniform regions, supports fast union/intersection, hidden-surface removal (front-to-back traversal) and ray tracing.
- **BSP (binary space partitioning) tree.** The space is split by a plane into two half-spaces (front/back), recursively; each node stores the splitting plane and polygons lying on it. Traversal in back-to-front order gives the correct painter's order for any viewpoint.
- **Voxels (uniform grid).** The space is a regular 3D grid of cells; simple but memory-hungry ($n^3$).

```figure caption="Question 4: octree. A cube is divided into eight octants (0-7); full (black), empty (white) and mixed (grey) octants; only mixed ones are subdivided."
import matplotlib.patches as mp
fig, ax = plt.subplots(figsize=(5.4, 2.6)); ax.axis("off"); ax.set_xlim(0, 11); ax.set_ylim(-3.2, 2.4); ax.set_aspect("equal")
ax.add_patch(mp.Rectangle((0.2, -1.6), 3, 3, fc="none", ec=INK, lw=1.3)); ax.plot([1.7, 1.7], [-1.6, 1.4], color=INK, lw=1); ax.plot([0.2, 3.2], [-0.1, -0.1], color=INK, lw=1)
cols = {0: "white", 1: "#444", 2: "#bbb", 3: "white", 4: "#444", 5: "white", 6: "white", 7: "#444"}
pos = {0: (0.2, -0.1), 1: (1.7, -0.1), 2: (0.2, -1.6), 3: (1.7, -1.6)}
for k, (x, y) in {0: (0.2, -0.1), 1: (1.7, -0.1), 2: (0.2, -1.6), 3: (1.7, -1.6)}.items():
    ax.add_patch(mp.Rectangle((x, y), 1.5, 1.5, fc=cols[k], ec=INK, lw=0.8, alpha=0.9)); ax.text(x + 0.75, y + 0.75, str(k), ha="center", va="center", fontsize=8, color="#b00020" if cols[k] != "#444" else "white")
ax.text(1.7, 1.75, "top view of the cube", ha="center", fontsize=6.5, color=MUTED)
ax.add_patch(mp.Circle((7.2, 1.6), 0.28, fc="#bbb", ec=INK)); ax.text(7.2, 2.15, "root", ha="center", fontsize=7)
xs = [4.6 + i * 1.05 for i in range(8)]
for i, x in enumerate(xs):
    ax.plot([7.2, x], [1.4, 0.2], color=INK, lw=0.8); ax.add_patch(mp.Circle((x, 0), 0.25, fc=cols[i], ec=INK)); ax.text(x, -0.65, str(i), ha="center", fontsize=7)
ax.plot([xs[2], 5.6, 6.2], [-0.3, -1.2, -1.2], color="none")
for j, x in enumerate([xs[2] - 0.5, xs[2] - 0.17, xs[2] + 0.17, xs[2] + 0.5]):
    ax.plot([xs[2], x], [-0.25, -1.3], color=INK, lw=0.7); ax.add_patch(mp.Circle((x, -1.55), 0.18, fc=["white", "#444", "#444", "white"][j], ec=INK))
ax.text(xs[2], -2.3, "mixed octant 2 is subdivided again", ha="center", fontsize=6.3, color=MUTED)
```

**Polygon meshes.** A polygon mesh is a set of connected polygonal facets (usually triangles or quadrilaterals) that share vertices and edges and approximate the surface of a 3D object. Because every facet is planar, standard rendering hardware can transform, clip, shade and rasterise it quickly, so the mesh is the standard boundary representation. A mesh is stored in three tables:

| Table | Content |
|---|---|
| Vertex table | coordinates $(x,y,z)$ of every vertex $V_1,V_2,\dots$ |
| Edge table | each edge as a pair of vertices, $E_1:(V_1,V_2),\dots$ |
| Polygon (surface) table | each face as a list of edges, $S_1:(E_1,E_2,E_3),\dots$ plus the plane coefficients $A,B,C,D$ and the normal |

How meshes help: (i) the shared tables avoid storing a vertex twice and give a quick consistency check (every edge belongs to two faces); (ii) the plane equation $Ax+By+Cz+D=0$ gives the face normal, used for back-face culling and shading (flat, Gouraud, Phong via vertex normals); (iii) triangle strips and fans cut the transmitted vertices to about one per triangle; (iv) curved surfaces are approximated to any accuracy by refining the mesh; (v) meshes are easy to deform, animate and texture-map.

@s 5
**Image-space against object-space methods.**

| Basis | Object-space methods | Image-space methods |
|---|---|---|
| Works on | the objects / surfaces in 3D (comparing objects with each other) | the pixels of the projected image |
| Decision | which parts of each object are visible | which surface is visible at each pixel |
| Precision | object precision (exact, independent of screen resolution) | screen resolution (pixel precision) |
| Cost | about $O(n^2)$ comparisons for $n$ objects | $O(n\times\text{pixels})$ |
| Examples | back-face detection, painter's (depth sort), BSP-tree, area subdivision (Warnock) | Z-buffer, A-buffer, scan-line, ray casting |

**A-buffer method.** The A-buffer (anti-aliased, area-averaged, accumulation buffer) extends the Z-buffer so that it can handle **transparent surfaces and anti-aliasing**. A Z-buffer stores only one depth per pixel; the A-buffer keeps, for every pixel, a **linked list of surface data**:

```figure caption="Question 5: A-buffer. A pixel position either holds one opaque surface (depth >= 0) or a pointer to a linked list of surface data (depth < 0)."
import matplotlib.patches as mp
fig, ax = plt.subplots(figsize=(5.8, 1.9)); ax.axis("off"); ax.set_xlim(0, 12); ax.set_ylim(-0.4, 3.4)
def box(x, y, w, h, t, fc="white", fs=6.6): ax.add_patch(mp.Rectangle((x, y), w, h, fc=fc, ec=INK, lw=1.1)); ax.text(x + w / 2, y + h / 2, t, ha="center", va="center", fontsize=fs)
box(0.2, 1.9, 3.1, 0.9, "depth ≥ 0:  depth field,\nintensity field (single surface)"); box(0.2, 0.4, 3.1, 0.9, "depth < 0:  depth field,\npointer to surface list")
for i, (n, x) in enumerate((("surface 1", 4.9), ("surface 2", 8.2))):
    box(x, 0.2, 2.8, 1.3, "RGB intensity\nopacity, depth\ncoverage (area %)\nsurface id\nnext pointer", fs=6.2); ax.text(x + 1.4, 1.75, n, ha="center", fontsize=7, color="#b00020")
ax.annotate("", xy=(4.9, 0.85), xytext=(3.3, 0.85), arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=1.2)); ax.annotate("", xy=(8.2, 0.85), xytext=(7.7, 0.85), arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=1.2)); ax.text(11.4, 0.85, "NULL", fontsize=7)
```

Each list node holds: the RGB intensity, the **opacity** (transparency) parameter, the **depth**, the **percent of area coverage** of the pixel, the surface identifier, other rendering parameters and a pointer to the next node.

Procedure: (1) For every polygon scan-converted into a pixel, the algorithm finds the depth and the fraction of the pixel area it covers (using, for example, a $4\times4$ subpixel bit mask). (2) If the surface is opaque and covers the whole pixel, it is compared with the stored depth like in an ordinary Z-buffer (the nearer one is kept, depth field $\ge0$). (3) If it is transparent or covers only part of the pixel, a node is added to the pixel's linked list (the depth field is set negative to show that a list exists). (4) After all surfaces are processed, for each pixel the list is traversed in depth order and the surface intensities are combined with their opacities and coverage to give the final colour (e.g. $I=\alpha_1I_1+(1-\alpha_1)\alpha_2I_2+\cdots$), so edges are anti-aliased and see-through surfaces are blended. The price is extra memory and time compared with the Z-buffer.

@s 6
**Specular reflection.** The bright highlight seen on a shiny surface, caused by the (almost) mirror-like reflection of the light source. The reflected light is concentrated around the **reflection direction** $\mathbf R$, so it is strongest when the viewer's direction $\mathbf V$ coincides with $\mathbf R$, and it has the colour of the light (not of the surface). Phong's empirical model gives the specular intensity

$$I_{spec}=k_s\,I_l\,(\mathbf R\cdot\mathbf V)^{n_s}=k_sI_l\cos^{n_s}\phi,\qquad \mathbf R=2(\mathbf N\cdot\mathbf L)\mathbf N-\mathbf L,$$

where $k_s$ is the specular coefficient, $I_l$ the light intensity, $\phi$ the angle between $\mathbf R$ and $\mathbf V$ and $n_s$ the shininess exponent (1 for dull, 100 or more for metal-like).

**Phong shading (normal-vector interpolation).** Gouraud shading interpolates *intensities* and can miss or smear highlights. Phong shading interpolates the **surface normal** across the polygon and evaluates the lighting model at every pixel: (1) find the average unit normal at each vertex from the surrounding faces; (2) interpolate the normal along the polygon edges and then along each scan line, $\mathbf N_x=\mathbf N_a+\dfrac{x-x_a}{x_b-x_a}(\mathbf N_b-\mathbf N_a)$; (3) normalise $\mathbf N$ and apply the illumination equation $I=k_aI_a+k_dI_l(\mathbf N\cdot\mathbf L)+k_sI_l(\mathbf N\cdot\mathbf H)^{n_s}$ at each pixel. The result is accurate highlights but a heavy computation (a square root, a division and the exponentiation per pixel).

**Fast Phong shading.** It cuts that cost by **approximating** the intensity calculation:

1. The reflection vector is replaced by the **halfway vector** $\mathbf H=\dfrac{\mathbf L+\mathbf V}{|\mathbf L+\mathbf V|}$ (constant for a distant light and viewer), so $(\mathbf R\cdot\mathbf V)^{n_s}$ becomes $(\mathbf N\cdot\mathbf H)^{n_s}$ with one dot product.
2. Along a scan line the normal changes by a constant step, $\mathbf N_{x+1}=\mathbf N_x+\Delta\mathbf N$, so $\mathbf N\cdot\mathbf H$ and $\mathbf N\cdot\mathbf L$ are updated by simple additions (forward differencing) instead of recomputing the interpolation.
3. The illumination, as a function of the pixel position $x$ on the scan line, is approximated by a **quadratic (second-order Taylor) polynomial** $I(x)\approx Ax^2+Bx+C$ whose coefficients are computed once per scan line, so each pixel needs only two additions and no square root or exponentiation:

$$I_{x+1}=I_x+\Delta I_x,\qquad \Delta I_{x+1}=\Delta I_x+2A .$$

Thus Fast Phong keeps almost the quality of Phong shading (good highlights, no Mach bands) at a cost close to Gouraud shading.

@s 7
**Anti-aliasing in computer animation.** *Aliasing* in animation appears in two forms: **spatial aliasing** (jagged edges, "jaggies", from sampling the scene at the pixel grid) and **temporal aliasing** (the sampling in time at a finite frame rate: fast motion looks jerky, and periodic motion looks wrong, such as the wagon-wheel effect where a spoked wheel seems to rotate slowly or backwards). Anti-aliasing methods:

1. **Supersampling (post-filtering):** render at a higher resolution (e.g. $2\times2$ or $4\times4$ samples per pixel) and average the samples to one pixel; random (jittered) sampling removes regular patterns.
2. **Area sampling (pre-filtering):** set the pixel intensity from the area of the pixel covered by each object (as in the A-buffer).
3. **Filtering / low-pass filter** (box, Gaussian, Bartlett) before sampling, which removes frequencies above the Nyquist limit.
4. **Pixel phasing / sub-pixel positioning** for raster hardware.
5. **Temporal anti-aliasing:** raise the frame rate above twice the highest motion frequency (Nyquist), or add **motion blur** by averaging several sub-frame renderings (or by filtering along each object's motion path) within the shutter interval, which turns the strobing into a natural smear.

**Morphing.** Morphing smoothly transforms one image (or shape) into another, as in film transitions from a face to another face. The usual process (image morphing):

```figure caption="Question 7: typical morphing process; source image warped toward the target while the target is warped back, then cross-dissolved."
import matplotlib.patches as mp
fig, ax = plt.subplots(figsize=(6.4, 2.2)); ax.axis("off"); ax.set_xlim(0, 13); ax.set_ylim(-0.6, 3.3)
sq = lambda x, c, t, w=1.5: (ax.add_patch(mp.Rectangle((x, 0.8), w, 1.5, fc=c, ec=INK, lw=1.1)), ax.text(x + w / 2, 0.45, t, ha="center", fontsize=6.4))
sq(0.2, "#d9e6f7", "source image A"); ax.add_patch(mp.Polygon([(2.8, 0.8), (4.3, 1.1), (4.3, 2.0), (2.8, 2.3)], fc="#d9e6f7", ec=INK, lw=1.1)); ax.text(3.55, 0.45, "A warped", ha="center", fontsize=6.4)
ax.add_patch(mp.Polygon([(5.4, 0.8), (6.9, 0.8), (6.9, 2.3), (5.4, 2.3)], fc="#cfe8d4", ec=INK, lw=1.1, alpha=0.6)); ax.add_patch(mp.Polygon([(5.4, 0.8), (6.9, 1.1), (6.9, 2.0), (5.4, 2.3)], fc="#d9e6f7", ec=INK, lw=1.1, alpha=0.6)); ax.text(6.15, 0.45, "cross-dissolve", ha="center", fontsize=6.4)
ax.add_patch(mp.Polygon([(8.0, 0.8), (9.5, 0.8), (9.5, 2.3), (8.0, 2.3)], fc="#cfe8d4", ec=INK, lw=1.1)); ax.text(8.75, 0.45, "B warped", ha="center", fontsize=6.4)
sq(11.2, "#cfe8d4", "target image B")
for x in (1.75 + 0.2, 4.4, 7.0, 9.6): ax.annotate("", xy=(x + 0.9, 1.55), xytext=(x + 0.05, 1.55), arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=1.2))
ax.text(6.5, 3.0, "frame t = 0  ...  0.25  ...  0.5  ...  0.75  ...  1", ha="center", fontsize=6.6, color=MUTED)
```

1. **Key images:** take the two images $A$ (start) and $B$ (end) of equal size.
2. **Correspondence:** mark matching features (eyes, nose, mouth, outline) on both images, using a mesh of control points or pairs of feature lines.
3. **Interpolate the feature geometry:** for the in-between frame at time $t\in[0,1]$ the feature points move linearly, $\mathbf p(t)=(1-t)\mathbf p_A+t\,\mathbf p_B$.
4. **Warp both images:** deform $A$ so that its features move to $\mathbf p(t)$ (forward/reverse mapping with interpolation), and deform $B$ likewise.
5. **Cross-dissolve (colour blend)** the two warped images: $I_t(x,y)=(1-t)\,A_{warp}(x,y)+t\,B_{warp}(x,y)$.
6. **Render the frames** for $t=0,\ \Delta t,\ 2\Delta t,\dots,1$ and play them in sequence at the video frame rate (e.g. 24 or 30 frames per second); anti-alias each frame.

For 3D morphing of two meshes the vertices are matched one to one and interpolated, $\mathbf v(t)=(1-t)\mathbf v_A+t\mathbf v_B$.

@s 8
**Key components of a virtual-reality (VR) system.** A VR system immerses the user in a computer-generated 3D world and responds in real time to the user's movement.

```figure caption="Question 8: components of a VR system and the interaction loop."
import matplotlib.patches as mp
fig, ax = plt.subplots(figsize=(5.8, 2.6)); ax.axis("off"); ax.set_xlim(0, 12); ax.set_ylim(0, 5.3)
def box(x, y, w, h, t, fc="white", fs=6.8): ax.add_patch(mp.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.1", fc=fc, ec=INK, lw=1.2)); ax.text(x + w / 2, y + h / 2, t, ha="center", va="center", fontsize=fs)
box(0.2, 2.0, 2.6, 1.3, "User\n(senses, movement)", "#eef3fa"); box(4.2, 3.6, 3.4, 1.2, "Input devices\ntracker, data glove,\ncontroller, mic"); box(4.2, 0.4, 3.4, 1.2, "Output devices\nHMD / CAVE, audio,\nhaptic feedback")
box(8.6, 1.9, 3.2, 1.5, "VR engine\n(computer, GPU)\nreal-time rendering,\nphysics, collision", "#eef3fa"); box(8.6, 4.0, 3.2, 0.9, "Software + database\n3D models, scenes", fs=6.4)
for (a, b) in (((2.8, 2.9), (4.2, 4.0)), ((7.6, 4.2), (8.6, 3.1)), ((8.6, 2.2), (7.6, 1.2)), ((4.2, 1.0), (2.8, 2.3)), ((10.2, 4.0), (10.2, 3.4))): ax.annotate("", xy=b, xytext=a, arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=1.2))
```

1. **Input devices (sensors/trackers):** position and orientation trackers (magnetic, optical, inertial/IMU), data gloves, 3D mice, joysticks, controllers, voice input; they tell the computer where the user's head and hands are.
2. **Output / display devices:** the head-mounted display (HMD) with stereo lenses, CAVE (projection room) or stereoscopic monitors for vision; 3D spatial audio headphones; **haptic** devices (force-feedback gloves, vibrating controllers) for touch.
3. **VR engine / computer system:** a high-performance computer with a powerful GPU that takes the tracker data, updates the world, performs physics, collision detection and rendering for each eye at 60-90+ frames per second with low latency (under about 20 ms).
4. **Software and database:** the virtual world (3D models, textures, sound, behaviours) and the VR software/API (e.g. Unity, Unreal Engine, OpenXR) that manage the scene graph and interaction.
5. **User and interaction loop:** the user's actions are sensed, processed and fed back in real time through the displays, giving the feeling of **immersion, interaction and presence**.

**An application of an AR system.** Augmented Reality overlays computer-generated information on the live view of the real world (smartphone camera or smart glasses). Applications include **AR navigation** (arrows painted on the real road ahead), **AR in surgery** (a patient's CT/MRI model overlaid on the body to guide the surgeon), **AR furniture placement** (a virtual sofa shown in your room before buying), AR education and training, games (Pokémon GO) and industrial maintenance (repair instructions shown on the machine). In the AR furniture application, the camera captures the room, the tracker (SLAM) finds the floor and its scale, the 3D model is rendered and registered at the chosen position with correct perspective and lighting, and the combined image is displayed live.
