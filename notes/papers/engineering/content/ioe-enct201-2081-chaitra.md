---
file: NEBians-IOE-Past-Paper-Computer-Graphics-and-Visualization-ENCT201-2081-Chaitra.pdf
subject: Computer Graphics and Visualization
level: BE · Year II / Part I
code: ENCT201
year_bs: 2081 Chaitra
cal: BS
year_ad: 2025
stream: BEI, BCT
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular (New Course). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
What is computer visualization? Calculate the frame buffer size for a raster system recording a video for 1 min with resolution of $1280\times1024$ and storing 24 bits per pixel with a refresh rate of 25 fps. [[1+4]]

@q 2
(a) How the decision parameter can be used to draw a Circle? Draw the circle with the radius 7 and centre (10,15). [[2+5]]

(b) Differentiate between boundary fill and flood fill Algorithm. [[3]]

(c) Use the Cohen-Sutherland line clipping algorithm to clip two lines $P_1(40,50)$ - $P_2(75,45)$ and $P_3(70,20)$ - $P_4(100,10)$ against a window A (50,10), B (80,10), C (80,40) and D (50,40). [[4]]

@q 3
(a) Suppose there is a rectangle whose coordinates are A(1,1), B(4,1), C(4,4), D(1,4) and the window coordinates are (2,2), (5,2), (5,5), (2,5) and the given viewport location is (0.5,0), (1,0), (1,0.5), (0.5,0.5). Calculate the viewing transformation. [[4]]

(b) Write the steps required to rotate an object in 3D about arbitrary axis. Explain about the perspective projection. [[5]]

(c) Differentiate between Parallel Projection and Oblique Projection. [[3]]

@q 4
Define spline curve. Explain Hermite curve for 3-degree polynomial with required expression. [[1+4]]

@q 5
Why do you mean by back face detection? Explain the Z buffer method for visible surface detection in detail with its limitation. [[1+4]]

@q 6
Explain the Phong shading algorithm. Mention the advantages of fast Phong shading overphong shading method. [[1+4]]

@q 7
What is raster animation? Explain about motion specification in computer animation. [[2+5]]

@q 8
Explain distributed scene rendering in brief. Differentiate between AR, VR and MR technology. [[3+4]]
<!-- SOLUTIONS -->

@s 1
**Computer visualization** is the use of computer graphics to turn data (measurements, simulation results, databases, medical scans) into pictures, charts, 3D models and animations, so that people can see structure, patterns and relationships that are hard to find in raw numbers. It has two main branches: *scientific visualization* (spatial data such as flow fields, CT/MRI volumes, weather) and *information visualization* (abstract data such as networks, trees, statistics, dashboards).

**Frame buffer size.** One frame: $1280\times1024=1\,310\,720$ pixels, each of 24 bits $=3$ bytes:

$$\text{one frame}=1\,310\,720\times24\ \text{bits}=31\,457\,280\ \text{bits}=3\,932\,160\ \text{bytes}=3.75\ \text{MiB}.$$

The frame buffer of the raster system that *displays* the video needs to hold this one frame ($\approx\mathbf{3.75}$ **MB**; refreshing at 25 fps only repeats it). If the whole 1-minute video is *recorded* (stored), the number of frames is $25\times60=1500$:

$$1500\times3\,932\,160\ \text{bytes}=5\,898\,240\,000\ \text{bytes}\approx\boxed{5.9\times10^{9}\ \text{bytes}\approx5.49\ \text{GiB}}$$

(Bandwidth needed: $3\,932\,160\times25\approx98.3$ MB per second, uncompressed.)

@s 2
**(a) Midpoint (decision-parameter) circle algorithm.** Circle function $f(x,y)=x^2+y^2-r^2$ (centre at the origin): $f<0$ inside, $f=0$ on, $f>0$ outside the circle. Because of **8-way symmetry** only the octant from $(0,r)$ to $x=y$ ($45^\circ$) is calculated; each point $(x,y)$ gives $(\pm x,\pm y)$ and $(\pm y,\pm x)$.

Having plotted $(x_k,y_k)$, the next pixel is $(x_k+1,y_k)$ or $(x_k+1,y_k-1)$. Evaluate $f$ at the **midpoint** between the two candidates; this value is the decision parameter

$$p_k=f\!\left(x_k+1,\ y_k-\tfrac12\right)=(x_k+1)^2+\left(y_k-\tfrac12\right)^2-r^2 .$$

- $p_k<0$: the midpoint is inside the circle, so the upper pixel $(x_k+1,y_k)$ is closer. $p_{k+1}=p_k+2x_{k+1}+1$.
- $p_k\ge0$: the midpoint is outside, choose $(x_k+1,y_k-1)$. $p_{k+1}=p_k+2x_{k+1}+1-2y_{k+1}$.
- Initial value at $(0,r)$: $p_0=\tfrac54-r\approx1-r$ for integer $r$.

**Circle of radius 7, centre (10, 15).** $p_0=1-7=-6$, start at $(0,7)$:

| $k$ | $p_k$ | next point $(x_{k+1},y_{k+1})$ | $p_{k+1}$ |
|---|---|---|---|
| 0 | $-6$ | $(1,7)$ | $-6+2(1)+1=-3$ |
| 1 | $-3$ | $(2,7)$ | $-3+2(2)+1=2$ |
| 2 | $2$ | $(3,6)$ | $2+2(3)+1-2(6)=-3$ |
| 3 | $-3$ | $(4,6)$ | $-3+2(4)+1=6$ |
| 4 | $6$ | $(5,5)$ | $6+2(5)+1-2(5)=7$ |

The loop stops at $x\ge y$ (at $(5,5)$). Octant points relative to the centre: $(0,7),(1,7),(2,7),(3,6),(4,6),(5,5)$. Adding the centre $(10,15)$, the octant points on the screen are $(10,22),(11,22),(12,22),(13,21),(14,21),(15,20)$, and each $(x,y)$ is plotted at the eight symmetric positions $(10\pm x,\ 15\pm y)$ and $(10\pm y,\ 15\pm x)$ (with $x,y$ the relative values). For instance $(3,6)$ gives $(13,21),(7,21),(13,9),(7,9),(16,18),(4,18),(16,12),(4,12)$.

```figure caption="Question 2(a): pixels of the circle of radius 7 with centre (10, 15) from the midpoint algorithm (octant points in red, symmetric images in blue)."
import numpy as np
x, y, p = 0, 7, 1 - 7; octant = [(0, 7)]
while x < y:
    x += 1
    if p < 0: p += 2 * x + 1
    else: y -= 1; p += 2 * x + 1 - 2 * y
    octant.append((x, y))
pts = set()
for (a, b) in octant:
    for sx in (-1, 1):
        for sy in (-1, 1):
            pts.add((10 + sx * a, 15 + sy * b)); pts.add((10 + sx * b, 15 + sy * a))
fig, ax = plt.subplots(figsize=(3.6, 3.6)); ax.set_aspect("equal")
oc = {(10 + a, 15 + b) for a, b in octant}
ax.scatter([q[0] for q in pts if q not in oc], [q[1] for q in pts if q not in oc], s=22, color=ACCENT, marker="s")
ax.scatter([q[0] for q in oc], [q[1] for q in oc], s=26, color="#b00020", marker="s"); ax.plot([10], [15], "k+", ms=7)
t = np.linspace(0, 2 * np.pi, 200); ax.plot(10 + 7 * np.cos(t), 15 + 7 * np.sin(t), color=MUTED, lw=0.7)
ax.set_xticks(range(2, 19, 2)); ax.set_yticks(range(8, 24, 2)); ax.tick_params(labelsize=6); ax.grid(alpha=0.25)
```

**(b) Boundary fill against flood fill.**

| Basis | Boundary-fill | Flood-fill |
|---|---|---|
| Region defined by | a closed boundary drawn in a single boundary colour | a region of pixels all having the same interior (old) colour |
| Stop condition | stops when it meets the boundary colour (or the fill colour) | stops when it meets a pixel whose colour is not the old colour |
| Input | seed point, fill colour, boundary colour | seed point, fill colour, old colour |
| Interior | may contain several colours | must be a single colour (it fills only the connected area of the old colour) |
| Boundary | must be one colour and closed | any shape/colour; no single boundary colour needed |
| Typical use | filling shapes drawn with an outline (paint-bucket in outlined cartoons) | recolouring an area of an image (paint-bucket in image editors) |

Both methods are recursive (or stack/queue based) and use 4-connected or 8-connected neighbours: a 4-connected fill cannot enter narrow diagonal gaps, an 8-connected fill may leak through diagonal boundaries, and deep recursion can overflow the stack, so scan-line (span) versions are used in practice.

**(c) Cohen-Sutherland clipping.** Window: $x_{min}=50$, $x_{max}=80$, $y_{min}=10$, $y_{max}=40$. The 4-bit region code is TBRL (Top: $y>40$, Bottom: $y<10$, Right: $x>80$, Left: $x<50$).

| Point | Test | Code |
|---|---|---|
| $P_1(40,50)$ | left, above | 1001 |
| $P_2(75,45)$ | above | 1000 |
| $P_3(70,20)$ | inside | 0000 |
| $P_4(100,10)$ | $x>80$; $y=10$ is on the boundary, not below | 0010 |

*Line $P_1P_2$:* the logical AND of the codes is $1001\wedge1000=1000\ne0$ (both ends lie above the window), so the line is **trivially rejected**: nothing is visible.

*Line $P_3P_4$:* the codes are 0000 and 0010: one end inside, so the line is *partly visible*. $P_4$ is to the right, so clip against $x=80$. The slope is $m=\dfrac{10-20}{100-70}=-\dfrac13$:

$$y=y_3+m(80-x_3)=20-\tfrac13(10)=16.67 .$$

New end point $P_4'(80,\,16.67)$ with code 0000. Both end codes are 0000, so the line is accepted: **visible part from $(70,20)$ to $(80,16.67)$**.

```figure caption="Question 2(c): window ABCD, rejected line P1P2 and clipped line P3P4 (visible part thick)."
import matplotlib.patches as mp
fig, ax = plt.subplots(figsize=(4.4, 3.2)); ax.add_patch(mp.Rectangle((50, 10), 30, 30, fc="#1d6fb815", ec=INK, lw=1.5))
ax.plot([40, 75], [50, 45], color=MUTED, lw=1.2, ls="--"); ax.plot([70, 100], [20, 10], color=MUTED, lw=1.2, ls="--"); ax.plot([70, 80], [20, 16.67], color="#b00020", lw=3)
for (p, n, dx, dy) in (((40, 50), "P1", -4, 1), ((75, 45), "P2", 1, 1.5), ((70, 20), "P3", -4, 1.5), ((100, 10), "P4", 1, 1), ((80, 16.67), "P4'", 1, 2)):
    ax.plot(*p, "o", color=INK, ms=3.5); ax.text(p[0] + dx, p[1] + dy, n, fontsize=7)
for (p, n) in (((50, 10), "A"), ((80, 10), "B"), ((80, 40), "C"), ((50, 40), "D")): ax.text(p[0] + (-3 if p[0] == 50 else 1), p[1] + (-3 if p[1] == 10 else 1), n, fontsize=7, color=ACCENT)
ax.set_xlim(35, 105); ax.set_ylim(4, 55); ax.set_aspect("equal"); ax.grid(alpha=0.2); ax.tick_params(labelsize=6)
```

@s 3
**(a) Window-to-viewport transformation.** Window: $x_{w,min}=2$, $x_{w,max}=5$, $y_{w,min}=2$, $y_{w,max}=5$. Viewport: $x_{v,min}=0.5$, $x_{v,max}=1$, $y_{v,min}=0$, $y_{v,max}=0.5$. The window point $(x_w,y_w)$ maps to the viewport point

$$x_v=x_{v,min}+(x_w-x_{w,min})\,s_x,\quad y_v=y_{v,min}+(y_w-y_{w,min})\,s_y,\qquad s_x=\frac{x_{v,max}-x_{v,min}}{x_{w,max}-x_{w,min}}=\frac{0.5}{3}=\frac16,\ \ s_y=\frac{0.5}{3}=\frac16 .$$

As a composite: translate the window corner to the origin, scale by $(s_x,s_y)$, translate to the viewport corner:

$$M=T(0.5,0)\,S\!\left(\tfrac16,\tfrac16\right)T(-2,-2)=\begin{bmatrix}\tfrac16&0&0.5-\tfrac26\\0&\tfrac16&-\tfrac26\\0&0&1\end{bmatrix}=\begin{bmatrix}0.1667&0&0.1667\\0&0.1667&-0.3333\\0&0&1\end{bmatrix}.$$

So $x_v=\dfrac{x_w+1}{6}$ and $y_v=\dfrac{y_w-2}{6}$. Applying $M$ to the rectangle:

| Vertex | $(x_w,y_w)$ | $(x_v,y_v)$ |
|---|---|---|
| A | (1, 1) | (0.333, $-0.167$) |
| B | (4, 1) | (0.833, $-0.167$) |
| C | (4, 4) | (0.833, 0.333) |
| D | (1, 4) | (0.333, 0.333) |

The rectangle $ABCD$ extends outside the window on the left ($x<2$) and bottom ($y<2$). Only the part inside the window, $(2,2)$ to $(4,4)$, is displayed: after clipping it maps to the viewport rectangle $(0.5,\,0)$ to $(0.833,\,0.333)$. Corners: $(2,2)\to(0.5,0)$, $(4,2)\to(0.833,0)$, $(4,4)\to(0.833,0.333)$, $(2,4)\to(0.5,0.333)$ (all inside the viewport $0.5\le x_v\le1$, $0\le y_v\le0.5$).

```figure caption="Question 3(a): the rectangle ABCD, the window (2,2)-(5,5) and the viewport (0.5,0)-(1,0.5); only the part inside the window is mapped (shaded)."
import matplotlib.patches as mp
fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.2, 2.7))
a1.add_patch(mp.Rectangle((2, 2), 3, 3, fc="none", ec=INK, lw=1.5)); a1.add_patch(mp.Rectangle((1, 1), 3, 3, fc="none", ec=ACCENT, lw=1.2, ls="--")); a1.add_patch(mp.Rectangle((2, 2), 2, 2, fc="#1d6fb833", ec="none"))
for (p, n) in (((1, 1), "A"), ((4, 1), "B"), ((4, 4), "C"), ((1, 4), "D")): a1.text(p[0] - 0.25, p[1] - 0.3, n, fontsize=7, color=ACCENT)
a1.set_xlim(0, 6); a1.set_ylim(0, 6); a1.set_aspect("equal"); a1.set_title("world: window (solid)", fontsize=7.5); a1.grid(alpha=0.2); a1.tick_params(labelsize=6)
a2.add_patch(mp.Rectangle((0.5, 0), 0.5, 0.5, fc="none", ec=INK, lw=1.5)); a2.add_patch(mp.Rectangle((0.5, 0), 1/3, 1/3, fc="#1d6fb833", ec="#b00020", lw=1.2))
a2.set_xlim(0.3, 1.1); a2.set_ylim(-0.1, 0.6); a2.set_aspect("equal"); a2.set_title("viewport (0.5,0)-(1,0.5)", fontsize=7.5); a2.grid(alpha=0.2); a2.tick_params(labelsize=6)
```

**(b) Rotation about an arbitrary axis in 3D.** Let the axis pass through the point $P_1(x_1,y_1,z_1)$ with unit direction vector $\mathbf u=(a,b,c)$, and let the rotation angle be $\theta$. Reduce the problem to a rotation about the $z$-axis:

1. **Translate** $P_1$ to the origin: $T(-x_1,-y_1,-z_1)$, so the axis passes through the origin.
2. **Rotate about the $x$-axis** by $\alpha$ so that $\mathbf u$ lies in the $xz$-plane: with $d=\sqrt{b^2+c^2}$, $\cos\alpha=c/d$, $\sin\alpha=b/d$; $R_x(\alpha)=\begin{bmatrix}1&0&0\\0&c/d&-b/d\\0&b/d&c/d\end{bmatrix}$ (4x4 with the homogeneous row and column).
3. **Rotate about the $y$-axis** by $\beta$ so that $\mathbf u$ coincides with the $z$-axis: $\cos\beta=d$, $\sin\beta=-a$ ($R_y$ rotates $(a,0,d)$ onto $(0,0,1)$).
4. **Rotate by $\theta$ about the $z$-axis:** $R_z(\theta)$.
5. **Undo the alignment:** $R_y^{-1}(\beta)$ then $R_x^{-1}(\alpha)$.
6. **Translate back:** $T(x_1,y_1,z_1)$.

$$M=T(x_1,y_1,z_1)\;R_x^{-1}(\alpha)\;R_y^{-1}(\beta)\;R_z(\theta)\;R_y(\beta)\;R_x(\alpha)\;T(-x_1,-y_1,-z_1),\qquad \mathbf P'=M\mathbf P .$$

(Check: $R_x(\alpha)$ sends $(a,b,c)$ to $(a,0,d)$ because $y'=(cb-bc)/d=0$ and $z'=(b^2+c^2)/d=d$; $R_y(\beta)$ then sends it to $(0,0,a^2+d^2)=(0,0,1)$ since $|\mathbf u|=1$.) If the axis is parallel to a coordinate axis, only steps 1, 4 and 6 are needed.

**Perspective projection.** The projectors are lines from the points of the object to a single **centre of projection** (the eye). Where they cut the view plane they form the image, so the size of the image decreases with distance (perspective foreshortening) and parallel lines that are not parallel to the view plane converge at **vanishing points**. With the centre of projection at the origin and the view plane at $z=d$, similar triangles give

$$x_p=\frac{x\,d}{z},\qquad y_p=\frac{y\,d}{z},\qquad \begin{bmatrix}x_h\\y_h\\z_h\\w\end{bmatrix}=\begin{bmatrix}1&0&0&0\\0&1&0&0\\0&0&1&0\\0&0&1/d&0\end{bmatrix}\begin{bmatrix}x\\y\\z\\1\end{bmatrix},\quad x_p=\frac{x_h}{w},\ y_p=\frac{y_h}{w}.$$

The number of principal vanishing points (1, 2 or 3) gives **one-, two- and three-point perspective** according to how many axes cut the view plane. Perspective looks realistic but does not preserve sizes, angles or parallelism.

**(c) Parallel projection against oblique projection.** An oblique projection is a *kind* of parallel projection, so the comparison is between the orthographic (perpendicular) form and the oblique form.

| Basis | Parallel (orthographic) projection | Oblique projection |
|---|---|---|
| Projectors | parallel to each other **and perpendicular** to the view plane | parallel to each other but **inclined** (not perpendicular) to the view plane |
| Faces parallel to the view plane | true shape and size | true shape and size |
| Faces/edges perpendicular to the view plane | shown as points / lines (not visible as depth) | drawn along a receding axis at angle $\alpha$ (30° or 45°), so depth is visible in one view |
| Views | front, top, side (several views needed) | one pictorial view (3D look) |
| Types | multiview, axonometric (isometric, dimetric, trimetric) | cavalier (scale 1 on the receding axis, $\tan\phi=1$, $\phi=45^\circ$) and cabinet (scale 1/2, $\tan\phi=2$, $\phi\approx63.4^\circ$) |
| Matrix | $x_p=x,\ y_p=y$ | $x_p=x+z\,L_1\cos\alpha,\ y_p=y+z\,L_1\sin\alpha$ ($L_1=1/\tan\phi$) |
| Use | engineering drawing, CAD, architecture plans | quick pictorial sketches |

@s 4
**Spline curve.** A spline is a smooth, flexible curve made of **piecewise polynomial** segments (usually cubic) that join with specified continuity ($C^0$ position, $C^1$ tangent, $C^2$ curvature) at the **control points / knots**. The name comes from the flexible drafting strip held by weights. Splines either **interpolate** the control points (Hermite, Cardinal, Catmull-Rom) or **approximate** them (Bézier, B-spline).

**Hermite curve (cubic).** A Hermite segment is defined by its two end points $\mathbf P_0,\mathbf P_1$ and the tangent vectors there, $\mathbf D_0=\mathbf P'(0)$ and $\mathbf D_1=\mathbf P'(1)$. The cubic polynomial in the parameter $u\in[0,1]$ is

$$\mathbf P(u)=\mathbf a u^3+\mathbf b u^2+\mathbf c u+\mathbf d,\qquad \mathbf P'(u)=3\mathbf au^2+2\mathbf bu+\mathbf c .$$

Boundary conditions: $\mathbf P(0)=\mathbf d=\mathbf P_0$; $\mathbf P(1)=\mathbf a+\mathbf b+\mathbf c+\mathbf d=\mathbf P_1$; $\mathbf P'(0)=\mathbf c=\mathbf D_0$; $\mathbf P'(1)=3\mathbf a+2\mathbf b+\mathbf c=\mathbf D_1$. Solving for the coefficients:

$$\mathbf a=2\mathbf P_0-2\mathbf P_1+\mathbf D_0+\mathbf D_1,\quad \mathbf b=-3\mathbf P_0+3\mathbf P_1-2\mathbf D_0-\mathbf D_1,\quad \mathbf c=\mathbf D_0,\quad \mathbf d=\mathbf P_0 .$$

In matrix form, with the Hermite basis matrix $M_H$:

$$\mathbf P(u)=\begin{bmatrix}u^3&u^2&u&1\end{bmatrix}\underbrace{\begin{bmatrix}2&-2&1&1\\-3&3&-2&-1\\0&0&1&0\\1&0&0&0\end{bmatrix}}_{M_H}\begin{bmatrix}\mathbf P_0\\\mathbf P_1\\\mathbf D_0\\\mathbf D_1\end{bmatrix}$$

or $\mathbf P(u)=\mathbf P_0H_0(u)+\mathbf P_1H_1(u)+\mathbf D_0H_2(u)+\mathbf D_1H_3(u)$ with the **blending (Hermite) functions**

$$H_0=2u^3-3u^2+1,\quad H_1=-2u^3+3u^2,\quad H_2=u^3-2u^2+u,\quad H_3=u^3-u^2 .$$

Properties: the curve passes through $\mathbf P_0$ and $\mathbf P_1$; the longer the tangent vector, the more the curve follows its direction before turning; adjacent segments join with $C^1$ continuity if the end tangent of one equals the start tangent of the next.

```figure caption="Question 4: Hermite blending functions (left) and an example segment with P0 = (0,0), P1 = (4,0), D0 = (0,4), D1 = (0,-4) (right)."
import numpy as np
u = np.linspace(0, 1, 100); H0 = 2*u**3 - 3*u**2 + 1; H1 = -2*u**3 + 3*u**2; H2 = u**3 - 2*u**2 + u; H3 = u**3 - u**2
fig, (a, b) = plt.subplots(1, 2, figsize=(6.4, 2.6))
for h, n, c in ((H0, "H0", INK), (H1, "H1", ACCENT), (H2, "H2", "#b00020"), (H3, "H3", "#2a9d5c")): a.plot(u, h, label=n, color=c, lw=1.3)
a.legend(fontsize=6.5); a.grid(alpha=0.25); a.set_xlabel("u", fontsize=7); a.tick_params(labelsize=6)
P0, P1, D0, D1 = np.array([0, 0]), np.array([4, 0]), np.array([0, 4]), np.array([0, -4])
C = np.outer(H0, P0) + np.outer(H1, P1) + np.outer(H2, D0) + np.outer(H3, D1)
b.plot(C[:, 0], C[:, 1], color=ACCENT, lw=1.6)
for (p, d, n) in ((P0, D0, "P0"), (P1, D1, "P1")): b.annotate("", xy=p + d * 0.5, xytext=p, arrowprops=dict(arrowstyle="-|>", color="#b00020", lw=1.1)); b.text(p[0] - 0.2, p[1] - 0.45, n, fontsize=7)
b.set_aspect("equal"); b.grid(alpha=0.25); b.tick_params(labelsize=6); b.set_ylim(-1, 3.5)
```

For this example $x(u)=4H_1=4(3u^2-2u^3)$ and $y(u)=4H_2-4H_3=4u-4u^2=4u(1-u)$; at $u=0.5$ the point is $(2,\,1)$ (the curve rises to $y_{max}=1$ at the middle and comes back down to $P_1$ with the downward tangent).

@s 5
**Back-face detection.** A polygon facing away from the viewer cannot be seen if the object is a closed solid, so it can be discarded before any further hidden-surface processing. A face with plane equation $Ax+By+Cz+D=0$ has outward normal $\mathbf N=(A,B,C)$. With $\mathbf V$ the vector from the eye towards the face, the polygon is a **back face** if

$$\mathbf V\cdot\mathbf N>0 .$$

In viewing/projection coordinates, looking along the $-z_v$ axis, this reduces to a test on the sign of $C$ only: the face is a back face if $C\le0$ (its normal points away from the viewer). The test removes about half of the polygons of a closed convex object, but it cannot decide visibility among front faces (concave objects, several objects), so another method is still needed.

**Z-buffer (depth-buffer) method.** It is an **image-space** method that compares the depth of surfaces at every pixel. Two buffers of the screen size are used: the *frame (refresh) buffer* holds the colour of each pixel and the *depth buffer* holds the depth $z$ of the nearest surface found so far for each pixel.

```text
for every pixel (x, y):                       # initialise
    depth[x, y] = 1.0  (far plane);  frame[x, y] = background colour
for every polygon:
    for every pixel (x, y) covered by the projection of the polygon:
        z = depth of the polygon at (x, y)      # from its plane equation
        if z < depth[x, y]:                     # nearer than what is stored
            depth[x, y] = z
            frame[x, y] = colour of the polygon at (x, y)
```

The depth of the polygon at the pixel comes from the plane equation $z=\dfrac{-Ax-By-D}{C}$. Moving one pixel along a scan line changes the depth by a constant, $z(x+1,y)=z(x,y)-\dfrac AC$, and to the next scan line $z(x,y-1)=z(x,y)+\dfrac BC$ (incremental, only one addition per pixel). Polygons can be processed in any order, and the visible surface is the one with the smallest depth stored when all are done.

*Advantages:* simple, no sorting, works for any surfaces (even intersecting), easy in hardware, time roughly proportional to the number of pixels covered.

*Limitations:*

1. Needs a large extra memory, a depth buffer as big as the frame buffer (e.g. 24 or 32 bits per pixel).
2. Only the nearest surface is stored, so **transparent / translucent surfaces** cannot be rendered correctly (the A-buffer is needed).
3. One depth per pixel gives **aliasing** (jagged edges); there is no area coverage information.
4. **Limited depth precision** causes z-fighting for surfaces that are close together, since the depth is quantised.
5. **Overdraw:** every polygon is rasterised even if it is later hidden, so time is wasted on hidden surfaces.
6. Each object's depth must be recomputed for each pixel it covers, which is costly for scenes with many small polygons.

@s 6
**Phong shading algorithm (normal-vector interpolation).** Unlike Gouraud shading, which interpolates the *intensity*, Phong shading interpolates the **surface normal vectors** across the polygon and applies the illumination model at every pixel, so highlights fall inside polygons and are rendered correctly.

1. Compute the unit normal of each polygon. At every vertex find the **average normal** of all polygons that share that vertex: $\mathbf N_v=\dfrac{\sum\mathbf N_k}{\left|\sum\mathbf N_k\right|}$.
2. Interpolate the normals linearly along the polygon edges between the vertices, for each scan line: $\mathbf N_a=\mathbf N_1+\dfrac{y_a-y_1}{y_2-y_1}(\mathbf N_2-\mathbf N_1)$.
3. Interpolate along the scan line between the two edge intersections: $\mathbf N_x=\mathbf N_a+\dfrac{x-x_a}{x_b-x_a}(\mathbf N_b-\mathbf N_a)$.
4. At each pixel **normalise** $\mathbf N_x$ and evaluate the illumination model $I=k_aI_a+k_dI_l(\mathbf N\cdot\mathbf L)+k_sI_l(\mathbf R\cdot\mathbf V)^{n_s}$ with this normal.
5. Write the intensity to the frame buffer.

The result is smooth shading with accurate specular highlights and few Mach bands, but it costs a normalisation (square root and division), the illumination equation and the specular power for every pixel.

**Fast Phong shading** approximates the calculation to remove most of that cost:

- uses the halfway vector $\mathbf H=\dfrac{\mathbf L+\mathbf V}{|\mathbf L+\mathbf V|}$ instead of recomputing $\mathbf R$ at every pixel: $(\mathbf N\cdot\mathbf H)^{n_s}$ with one dot product;
- evaluates the intensity along a scan line by a **quadratic (Taylor-series) approximation** $I(x)\approx Ax^2+Bx+C$ and incremental forward differences, $I_{x+1}=I_x+\Delta I_x$, $\Delta I_{x+1}=\Delta I_x+2A$ (only additions);
- avoids the per-pixel normalisation, square root and exponentiation.

**Advantages of fast Phong shading over (full) Phong shading:** (i) much faster, a few additions per pixel instead of a normalisation and exponent; (ii) lower hardware / computation cost, suited to real-time systems; (iii) the quality is almost the same as Phong's: smooth surfaces and good specular highlights, much better than flat and Gouraud shading; (iv) easy incremental implementation along scan lines; (v) the cost is close to that of Gouraud shading.

@s 7
**Raster animation.** Animation produced on a raster system by manipulating the pixels of the **frame buffer** rather than redrawing the geometry. Typical methods:

1. **Raster operations (bit-blt):** blocks of pixels (sprites, cells) are copied, moved, combined by logical operations (AND/OR/XOR) from one place of the frame buffer to another, so the object appears to move across the screen.
2. **Colour-table (lookup-table) animation:** the pixel values are not changed; the colour entries of the look-up table are cycled or changed, so the displayed colours change (water flow, flashing, cycling colours).
3. **Double buffering:** the next frame is drawn in a back buffer while the front buffer is displayed, and the two are swapped during the vertical retrace, which prevents flicker and tearing.

**Motion specification.** It defines how the objects move and how the parameters (position, orientation, scale, colour, shape) change with time. The main ways:

| Method | Idea | Example |
|---|---|---|
| **Direct motion specification** | the animator gives the position, rotation angle and scale as explicit functions of time, or by key frames and interpolation | a ball moves with $x(t)=x_0+vt$, rotation $\theta(t)=\omega t$; in-betweens from key frames by linear or spline interpolation $\mathbf p(t)=(1-t)\mathbf p_0+t\mathbf p_1$ |
| **Goal-directed (task-level) specification** | the motion is given as a high-level goal and the system works out the detailed motion | "walk to the door", "pick up the cup": the system plans the path |
| **Kinematic specification** | geometric motion without forces, using positions, velocities and accelerations: *forward kinematics* (joint angles give the end position) and *inverse kinematics* (the end position gives the joint angles) | a robot arm / character limb reaching for an object |
| **Dynamic specification** | the motion results from forces and torques using Newton's laws, $\mathbf F=m\mathbf a$, with mass, gravity, friction and collisions (physically-based) | falling and bouncing cloth, water, rigid-body crashes |

In practice a sequence is built from **key frames**: the animator specifies the key poses, and the computer generates the **in-between frames** by interpolation at the frame rate of 24-30 frames per second. Interpolation can be linear (constant speed) or by splines with ease-in / ease-out (acceleration), and the paths and speed curves can be edited.

@s 8
**Distributed scene rendering.** High-quality rendering (ray tracing, global illumination, film frames) takes minutes or hours per frame on one computer, so the work is divided among many networked computers (a **render farm**, a cluster or the cloud) that work in parallel:

```figure caption="Question 8: distributed rendering with a master node and many render nodes."
import matplotlib.patches as mp
fig, ax = plt.subplots(figsize=(5.8, 2.4)); ax.axis("off"); ax.set_xlim(0, 12); ax.set_ylim(0, 4.6)
def box(x, y, w, h, t, fc="white", fs=6.8): ax.add_patch(mp.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.1", fc=fc, ec=INK, lw=1.2)); ax.text(x + w / 2, y + h / 2, t, ha="center", va="center", fontsize=fs)
box(0.2, 1.6, 2.6, 1.4, "Scene +\nanimation files\n(assets, textures)", "#eef3fa"); box(3.6, 1.6, 2.6, 1.4, "Master / scheduler\nsplits the job,\nbalances the load", "#eef3fa")
for i in range(4):
    y = 0.2 + i * 1.1; box(7.4, y, 2.2, 0.85, "render node %d" % (i + 1), fs=6.6)
    ax.annotate("", xy=(7.4, y + 0.42), xytext=(6.2, 2.3), arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=1.0)); ax.annotate("", xy=(10.6, 2.3), xytext=(9.6, y + 0.42), arrowprops=dict(arrowstyle="-", color=ACCENT, lw=1.0))
box(10.6, 1.7, 1.3, 1.2, "Image\nassembler", "#eef3fa", fs=6.4); ax.annotate("", xy=(3.6, 2.3), xytext=(2.8, 2.3), arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=1.2))
```

The main ways to split the work: (i) **frame-level** (each node renders different frames of an animation, which is the simplest and scales best); (ii) **image-space / tile** (each node renders a different region or scan lines of the same image, "sort-first"); (iii) **object-space** (each node renders a subset of the objects/data and the partial images are merged by depth, "sort-last"). The master assigns the jobs dynamically (load balancing), the nodes read shared assets over the network, and the partial results are collected and assembled into the final images. Advantages: much shorter rendering time, ability to handle huge scenes, scalability; problems: network traffic, load imbalance, synchronisation, and cost of the infrastructure.

**AR, VR and MR.**

| Basis | Virtual Reality (VR) | Augmented Reality (AR) | Mixed Reality (MR) |
|---|---|---|---|
| Environment | fully computer-generated; the real world is blocked out | the real world with computer-generated objects overlaid | real and virtual objects coexist and **interact** in the same space |
| Immersion | complete immersion | partial; the user stays in the real world | partial to high |
| Devices | opaque head-mounted display, controllers, trackers | smartphone, tablet, smart glasses | see-through head-set with spatial mapping (HoloLens, Quest passthrough) |
| Interaction | with the virtual world only | virtual content overlaid, little interaction with the real objects | virtual objects respond to the real surfaces and vice versa (occlusion, anchoring) |
| Tracking | head and hand tracking | camera + SLAM, GPS, markers | full spatial / depth mapping of the room |
| Examples | VR games, flight simulators, virtual tours | Pokémon GO, AR navigation, IKEA Place | virtual screens pinned to a wall, holographic surgery planning |
| In the reality-virtuality continuum | virtual end | closer to the real end | in between (includes AR and augmented virtuality) |
