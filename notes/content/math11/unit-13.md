---
subject: Mathematics
grade: 11
unit: 13
title: Coordinates in Space
hours: 6
area: Analytic Geometry
---

Everything you have done in coordinate geometry so far has lived on a flat sheet.
Real objects — a kite over Tundikhel, a drone above Pokhara, the corner of a room
— need a third number to fix them. This unit adds a $z$-axis perpendicular to the
$x$ and $y$ axes, and rebuilds the three basic tools in three dimensions: the
**distance formula**, the **section formula**, and the **direction cosines** that
describe which way a line points.

::: key What the exam asks
Expect one short question on the distance or section formula and one longer
question on direction cosines. The two results you must be able to *derive* are
$AB = \sqrt{(x_2-x_1)^{2}+(y_2-y_1)^{2}+(z_2-z_1)^{2}}$ and
$l^{2}+m^{2}+n^{2} = 1$.
:::

## 13.1 Points in space

Take three mutually perpendicular lines through a point $O$ — the **origin** —
and call them the $x$-, $y$- and $z$-axes. Taken in pairs they determine three
**coordinate planes**:

| Plane | Contains the axes | Equation |
|---|---|---|
| $xy$-plane | $x$ and $y$ | $z = 0$ |
| $yz$-plane | $y$ and $z$ | $x = 0$ |
| $zx$-plane | $z$ and $x$ | $y = 0$ |

These three planes cut space into **eight octants**. The first octant is the one
in which all three coordinates are positive; the others are labelled by the sign
pattern of $(x,y,z)$.

```figure caption="The three coordinate planes $x=0$, $y=0$ and $z=0$ cut space into eight octants. The first octant, where $x$, $y$ and $z$ are all positive, is shaded."
import numpy as np, matplotlib.pyplot as plt
fig = plt.figure(figsize=(4.6,3.6))
ax = fig.add_subplot(projection='3d')
ax.set_axis_off()
L = 2.4
for v, lab in [((L,0,0), 'X'), ((0,L,0), 'Y'), ((0,0,L), 'Z')]:
    ax.plot([0,v[0]],[0,v[1]],[0,v[2]], color=INK, lw=1.4)
    ax.text(v[0]*1.18, v[1]*1.18, v[2]*1.12, lab, color=INK, fontsize=11)
for v in [(-L,0,0),(0,-L,0),(0,0,-L)]:
    ax.plot([0,v[0]],[0,v[1]],[0,v[2]], color=MUTED, lw=0.9, ls=(0,(4,3)))
g = np.linspace(-1.8, 1.8, 2)
A, B = np.meshgrid(g, g)
Z0 = np.zeros_like(A)
ax.plot_surface(A, B, Z0, color=MUTED, alpha=0.13, shade=False)
ax.plot_surface(Z0, A, B, color=MUTED, alpha=0.13, shade=False)
ax.plot_surface(A, Z0, B, color=MUTED, alpha=0.13, shade=False)
c = 1.5
faces = [([[0,0],[c,c]], [[0,c],[0,c]], [[c,c],[c,c]]),
         ([[c,c],[c,c]], [[0,c],[0,c]], [[0,0],[c,c]]),
         ([[0,c],[0,c]], [[c,c],[c,c]], [[0,0],[c,c]])]
for X, Y, Z in faces:
    ax.plot_surface(np.array(X,float), np.array(Y,float), np.array(Z,float),
                    color=ACCENT, alpha=0.26, shade=False)
ax.text(1.05, 1.05, 1.95, 'octant I', color=ACCENT, fontsize=10)
ax.text(-1.25, 1.75, 0.06, r'$z=0$', color=MUTED, fontsize=9)
ax.text(-0.1, 1.95, -1.6, r'$x=0$', color=MUTED, fontsize=9)
ax.text(0.15, 0.05, -0.36, 'O', color=INK, fontsize=10)
ax.set_xlim(-L,L); ax.set_ylim(-L,L); ax.set_zlim(-L,L)
ax.set_box_aspect((1,1,1))
ax.view_init(elev=20, azim=34)
```

A point $P$ in space is fixed by an ordered triple $(x, y, z)$: drop a
perpendicular from $P$ to the $xy$-plane meeting it at $M$, then $x$ and $y$ are
the usual plane coordinates of $M$ and $z = PM$, taken positive above the plane.

::: key Distances from the planes, the axes and the origin
For $P(x,y,z)$:

- distance from the $yz$-, $zx$- and $xy$-planes: $|x|$, $|y|$, $|z|$
- distance from the $x$-, $y$- and $z$-axes: $\sqrt{y^{2}+z^{2}}$,
  $\sqrt{z^{2}+x^{2}}$, $\sqrt{x^{2}+y^{2}}$
- distance from the origin: $OP = \sqrt{x^{2}+y^{2}+z^{2}}$
:::

```figure caption="The point $P(3,4,5)$. The box built on the coordinate planes shows how the triple is read off; $M(3,4,0)$ is the foot of the perpendicular from $P$ to the $xy$-plane."
import numpy as np, matplotlib.pyplot as plt
fig = plt.figure(figsize=(4.8,3.8))
ax = fig.add_subplot(projection='3d')
ax.set_axis_off()
L = 6.4
for v, lab in [((L,0,0), 'X'), ((0,L,0), 'Y'), ((0,0,L), 'Z')]:
    ax.plot([0,v[0]],[0,v[1]],[0,v[2]], color=INK, lw=1.2)
    ax.text(v[0]*1.06, v[1]*1.06, v[2]*1.04, lab, color=INK, fontsize=11)
box = [(0,0,0),(3,0,0),(3,4,0),(0,4,0),(0,0,5),(3,0,5),(3,4,5),(0,4,5)]
edges = [(0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7)]
for i,j in edges:
    a,b = np.array(box[i],float), np.array(box[j],float)
    ax.plot([a[0],b[0]],[a[1],b[1]],[a[2],b[2]], color=MUTED, lw=0.9, ls=(0,(3,3)))
ax.plot([0,3],[0,4],[0,5], color='#d9534f', lw=2.1)
ax.plot([3,3],[4,4],[0,5], color='#2e8b57', lw=1.6)
ax.scatter(3,4,5, color=ACCENT, s=34, depthshade=False)
ax.scatter(3,4,0, color='#2e8b57', s=28, depthshade=False)
ax.text(3.0, 5.3, 5.35, 'P(3, 4, 5)', color=ACCENT, fontsize=10)
ax.text(3.1, 4.5, -1.15, 'M(3, 4, 0)', color='#2e8b57', fontsize=10)
ax.text(3.5, 0.05, -1.0, 'x = 3', color=MUTED, fontsize=9)
ax.text(-0.5, 4.2, -1.1, 'y = 4', color=MUTED, fontsize=9)
ax.text(0.15, -1.75, 4.8, 'z = 5', color=MUTED, fontsize=9)
ax.text(0.2, 0.1, -0.85, 'O', color=INK, fontsize=10)
ax.set_xlim(0,L); ax.set_ylim(0,L); ax.set_zlim(0,L)
ax.set_box_aspect((1,1,1))
ax.view_init(elev=18, azim=32)
```

::: example Worked example 13.1 — distances from planes and axes
**Problem.** For the point $P(3,-4,5)$ find (i) its distance from the $xy$-plane,
(ii) its distance from the $x$-axis, (iii) its distance from the origin, and
(iv) the octant it lies in.

**Solution.**

(i) The distance from the $xy$-plane is $|z| = 5$ units.

(ii) The distance from the $x$-axis ignores the $x$-coordinate:

$$ \sqrt{y^{2}+z^{2}} = \sqrt{(-4)^{2}+5^{2}} = \sqrt{16+25} = \sqrt{41} \approx 6.40\ \text{units} $$

(iii) $OP = \sqrt{3^{2}+(-4)^{2}+5^{2}} = \sqrt{9+16+25} = \sqrt{50} = 5\sqrt{2} \approx 7.07$ units.

(iv) The signs are $(+,-,+)$, so $P$ lies in the fourth octant.
:::

::: caution Which coordinate do you drop?
Distance from a **plane** uses the *one* coordinate perpendicular to it; distance
from an **axis** uses the *other two*. Students routinely swap these. A quick
memory check: a point can be far from the $x$-axis while having a huge
$x$-coordinate, so $x$ cannot appear in that distance.
:::

## 13.2 Distance between two points

::: derivation The distance formula in space
Let $A(x_1,y_1,z_1)$ and $B(x_2,y_2,z_2)$ be two points. Complete the rectangular
box whose edges are parallel to the axes and which has $AB$ as a space diagonal.
Let $M$ be the corner $(x_2,y_2,z_1)$ — vertically below $B$ and in the same
horizontal plane as $A$.

**Step 1 — the horizontal diagonal.** $A$ and $M$ have the same $z$, so by the
two-dimensional distance formula

$$ AM^{2} = (x_2-x_1)^{2}+(y_2-y_1)^{2} $$

**Step 2 — the vertical edge.** $MB$ is parallel to the $z$-axis, so
$MB = |z_2-z_1|$ and $MB$ is perpendicular to the plane containing $AM$, hence
perpendicular to $AM$.

**Step 3 — Pythagoras in $\triangle AMB$, right-angled at $M$.**

$$ AB^{2} = AM^{2}+MB^{2} = (x_2-x_1)^{2}+(y_2-y_1)^{2}+(z_2-z_1)^{2} $$

$$ AB = \sqrt{(x_2-x_1)^{2}+(y_2-y_1)^{2}+(z_2-z_1)^{2}} $$

Putting $A$ at the origin gives $OB = \sqrt{x_2^{2}+y_2^{2}+z_2^{2}}$.
:::

```figure caption="Deriving the distance formula: $AB$ is the space diagonal of a box with edges parallel to the axes, and $AB^{2}=AM^{2}+MB^{2}$ with $\\triangle AMB$ right-angled at $M$."
import numpy as np, matplotlib.pyplot as plt
fig = plt.figure(figsize=(4.8,3.6))
ax = fig.add_subplot(projection='3d')
ax.set_axis_off()
A = np.array([0.0,0.0,0.0]); B = np.array([4.0,3.0,3.0])
M = np.array([B[0],B[1],A[2]])
verts = [(A[0],A[1],A[2]),(B[0],A[1],A[2]),(B[0],B[1],A[2]),(A[0],B[1],A[2]),
         (A[0],A[1],B[2]),(B[0],A[1],B[2]),(B[0],B[1],B[2]),(A[0],B[1],B[2])]
edges = [(0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7)]
for p, q in edges:
    u, v = np.array(verts[p]), np.array(verts[q])
    ax.plot([u[0],v[0]],[u[1],v[1]],[u[2],v[2]], color=MUTED, lw=0.9, ls=(0,(3,3)))
ax.plot([A[0],B[0]],[A[1],B[1]],[A[2],B[2]], color='#d9534f', lw=2.4)
ax.plot([A[0],M[0]],[A[1],M[1]],[A[2],M[2]], color=ACCENT, lw=2.0)
ax.plot([M[0],B[0]],[M[1],B[1]],[M[2],B[2]], color='#2e8b57', lw=2.0)
for pt, col in [(A, INK), (B, INK), (M, INK)]:
    ax.scatter(*pt, color=col, s=26, depthshade=False)
ax.text(0.0, 0.0, -1.15, r'$A(x_1,y_1,z_1)$', color=INK, fontsize=9.5, ha='center')
ax.text(3.6, 3.0, 3.75, r'$B(x_2,y_2,z_2)$', color=INK, fontsize=9.5, ha='center')
ax.text(4.0, 3.0, -1.15, r'$M(x_2,y_2,z_1)$', color=INK, fontsize=9.5, ha='center')
ax.text(2.1, 1.3, -0.45, 'AM', color=ACCENT, fontsize=10)
ax.text(4.35, 3.2, 1.4, 'MB', color='#2e8b57', fontsize=10)
ax.text(1.5, 1.9, 1.55, 'AB', color='#d9534f', fontsize=10)
d = (A-M)/np.linalg.norm(A-M)*0.55
ax.plot([M[0]+d[0], M[0]+d[0], M[0]],[M[1]+d[1], M[1]+d[1], M[1]],
        [M[2], M[2]+0.55, M[2]+0.55], color=MUTED, lw=1.0)
ax.set_xlim(-1.0,5.0); ax.set_ylim(-1.0,4.0); ax.set_zlim(-1.6,4.2)
ax.set_box_aspect((1.25,1,1))
ax.view_init(elev=17, azim=-56)
```

::: example Worked example 13.2 — recognising a triangle
**Problem.** Show that the points $A(0,7,10)$, $B(-1,6,6)$ and $C(-4,9,6)$ are the
vertices of a right-angled isosceles triangle.

**Solution.** Work with the *squares* of the lengths — no surds are needed.

$$ AB^{2} = (-1-0)^{2}+(6-7)^{2}+(6-10)^{2} = 1+1+16 = 18 $$

$$ BC^{2} = (-4+1)^{2}+(9-6)^{2}+(6-6)^{2} = 9+9+0 = 18 $$

$$ CA^{2} = (0+4)^{2}+(7-9)^{2}+(10-6)^{2} = 16+4+16 = 36 $$

Since $AB^{2} = BC^{2}$, the triangle is isosceles. Since
$AB^{2}+BC^{2} = 18+18 = 36 = CA^{2}$, the converse of Pythagoras' theorem gives a
right angle at $B$. So $\triangle ABC$ is right-angled and isosceles, with
$AB = BC = 3\sqrt{2}$ and $CA = 6$.
:::

::: example Worked example 13.3 — an equilateral triangle
**Problem.** Prove that $A(1,2,3)$, $B(2,3,1)$ and $C(3,1,2)$ form an equilateral
triangle.

**Solution.**

$$ AB^{2} = 1^{2}+1^{2}+(-2)^{2} = 6, \quad BC^{2} = 1^{2}+(-2)^{2}+1^{2} = 6,
\quad CA^{2} = (-2)^{2}+1^{2}+1^{2} = 6 $$

All three sides equal $\sqrt{6}$ units, so the triangle is equilateral.
:::

::: example Worked example 13.4 — a point on an axis
**Problem.** Find the point on the $y$-axis that is equidistant from $A(3,1,2)$
and $B(5,5,2)$.

**Solution.** Any point on the $y$-axis has the form $P(0,y,0)$. The condition
$PA^{2} = PB^{2}$ gives

$$ (0-3)^{2}+(y-1)^{2}+(0-2)^{2} = (0-5)^{2}+(y-5)^{2}+(0-2)^{2} $$

$$ 9+y^{2}-2y+1+4 = 25+y^{2}-10y+25+4 $$

$$ 14-2y = 54-10y \;\Rightarrow\; 8y = 40 \;\Rightarrow\; y = 5 $$

The point is $(0,5,0)$.

**Check.** $PA = \sqrt{9+16+4} = \sqrt{29}$ and $PB = \sqrt{25+0+4} = \sqrt{29}$ ✓.
:::

### The section formula

::: derivation The section formula in space
Let $P(x,y,z)$ divide the join of $A(x_1,y_1,z_1)$ and $B(x_2,y_2,z_2)$ internally
in the ratio $m:n$, so $AP:PB = m:n$.

Drop perpendiculars $AL$, $PN$, $BM$ from $A$, $P$, $B$ to the $xy$-plane. These
three perpendiculars are parallel, so they lie in one plane, and the line $AB$
cuts them proportionally.

Draw through $A$ a line parallel to $LM$, meeting $PN$ at $R$ and $BM$ at $S$.
Then $RP = z-z_1$ and $SB = z_2-z_1$, and $\triangle APR$ and $\triangle ABS$ are
similar (equal angles, since $RP$ and $SB$ are parallel), so

$$ \frac{z-z_1}{z_2-z_1} = \frac{RP}{SB} = \frac{AP}{AB} = \frac{m}{m+n} $$

Cross-multiplying, $(m+n)(z-z_1) = m(z_2-z_1)$, so
$(m+n)z = mz_2+nz_1$, that is

$$ z = \frac{mz_2+nz_1}{m+n} $$

The same argument applied to the other two pairs of coordinate planes gives $x$
and $y$, so

$$ P = \left(\frac{mx_2+nx_1}{m+n},\ \frac{my_2+ny_1}{m+n},\ \frac{mz_2+nz_1}{m+n}\right) $$

For **external** division replace $n$ by $-n$:
$P = \left(\dfrac{mx_2-nx_1}{m-n},\ \dfrac{my_2-ny_1}{m-n},\ \dfrac{mz_2-nz_1}{m-n}\right)$.
:::

::: key Midpoint and centroid
- Midpoint ($m=n=1$):
  $\left(\dfrac{x_1+x_2}{2},\ \dfrac{y_1+y_2}{2},\ \dfrac{z_1+z_2}{2}\right)$
- Centroid of the triangle with vertices $A$, $B$, $C$:
  $\left(\dfrac{x_1+x_2+x_3}{3},\ \dfrac{y_1+y_2+y_3}{3},\ \dfrac{z_1+z_2+z_3}{3}\right)$
:::

```figure caption="Deriving the section formula. The perpendiculars $AL$, $PN$, $BM$ to the $xy$-plane are parallel; drawing $ARS$ parallel to $LM$ makes $\\triangle APR$ and $\\triangle ABS$ similar, so $RP:SB = AP:AB = m:(m+n)$."
import numpy as np, matplotlib.pyplot as plt
fig = plt.figure(figsize=(4.8,3.6))
ax = fig.add_subplot(projection='3d')
ax.set_axis_off()
g = np.array([[0.0,0.0],[6.0,6.0]])
gy = np.array([[0.0,5.2],[0.0,5.2]])
ax.plot_surface(g, gy, np.zeros_like(g), color=MUTED, alpha=0.12, shade=False)
A = np.array([1.0,1.0,1.0]); B = np.array([5.0,4.2,4.6])
P = (2*B+A)/3.0
L = np.array([A[0],A[1],0.0]); M = np.array([B[0],B[1],0.0])
N = np.array([P[0],P[1],0.0])
R = np.array([P[0],P[1],A[2]]); S = np.array([B[0],B[1],A[2]])
ax.plot([A[0],B[0]],[A[1],B[1]],[A[2],B[2]], color=ACCENT, lw=2.3)
for U, V in [(A,L),(P,N),(B,M)]:
    ax.plot([U[0],V[0]],[U[1],V[1]],[U[2],V[2]], color=MUTED, lw=1.0, ls=(0,(3,3)))
ax.plot([A[0],S[0]],[A[1],S[1]],[A[2],S[2]], color='#b8860b', lw=1.3, ls=(0,(5,3)))
ax.plot([L[0],M[0]],[L[1],M[1]],[L[2],M[2]], color=MUTED, lw=1.0)
ax.plot([R[0],P[0]],[R[1],P[1]],[R[2],P[2]], color='#2e8b57', lw=2.0)
ax.plot([S[0],B[0]],[S[1],B[1]],[S[2],B[2]], color='#d9534f', lw=2.0)
pts = [(A,'A',INK,(-0.35,0.0,0.30),'center'), (P,'P',INK,(0.0,0.0,0.38),'center'),
       (B,'B',INK,(0.0,0.0,0.38),'center'),
       (L,'L',MUTED,(0.0,0.0,-0.60),'center'), (N,'N',MUTED,(0.0,0.0,-0.60),'center'),
       (M,'M',MUTED,(0.0,0.0,-0.60),'center'),
       (R,'R',MUTED,(-0.55,0.0,-0.12),'center'), (S,'S',MUTED,(0.45,0.0,-0.12),'center')]
for pt, lab, col, d, ha in pts:
    ax.scatter(*pt, color=col, s=22, depthshade=False)
    ax.text(pt[0]+d[0], pt[1]+d[1], pt[2]+d[2], lab, color=col, fontsize=10.5, ha=ha)
ax.set_xlim(0,6.4); ax.set_ylim(0,5.4); ax.set_zlim(-0.6,5.4)
ax.set_box_aspect((6.4,5.4,6.0))
ax.view_init(elev=17, azim=-62)
```

::: example Worked example 13.5 — internal and external division
**Problem.** Find the coordinates of the points dividing the join of $A(2,-1,3)$
and $B(4,3,1)$ in the ratio $3:2$ (i) internally and (ii) externally.

**Solution.** Here $m = 3$, $n = 2$, so $m+n = 5$ and $m-n = 1$.

(i) Internally:

$$ x = \frac{3(4)+2(2)}{5} = \frac{16}{5}, \quad
y = \frac{3(3)+2(-1)}{5} = \frac{7}{5}, \quad
z = \frac{3(1)+2(3)}{5} = \frac{9}{5} $$

The point is $\left(\dfrac{16}{5},\ \dfrac{7}{5},\ \dfrac{9}{5}\right)$.

(ii) Externally:

$$ x = \frac{3(4)-2(2)}{1} = 8, \quad y = \frac{3(3)-2(-1)}{1} = 11, \quad
z = \frac{3(1)-2(3)}{1} = -3 $$

The point is $(8,\ 11,\ -3)$.
:::

::: example Worked example 13.6 — finding the ratio
**Problem.** In what ratio does the $yz$-plane divide the join of $A(2,4,5)$ and
$B(3,5,-4)$?

**Solution.** Let the plane cut $AB$ in the ratio $k:1$ at the point

$$ \left(\frac{3k+2}{k+1},\ \frac{5k+4}{k+1},\ \frac{-4k+5}{k+1}\right) $$

Every point of the $yz$-plane has $x = 0$, so

$$ \frac{3k+2}{k+1} = 0 \;\Rightarrow\; 3k+2 = 0 \;\Rightarrow\; k = -\frac23 $$

A negative ratio means **external** division: the $yz$-plane divides $AB$
externally in the ratio $2:3$.
:::

## 13.3 Direction cosines and direction ratios

A line in space is aimed by the three angles it makes with the positive
directions of the axes.

::: definition Direction angles and direction cosines
If a directed line through the origin makes angles $\alpha$, $\beta$, $\gamma$
with the positive $x$-, $y$- and $z$-axes, then $\alpha$, $\beta$, $\gamma$ are
its **direction angles** and

$$ l = \cos\alpha, \qquad m = \cos\beta, \qquad n = \cos\gamma $$

are its **direction cosines**, written $(l, m, n)$.
:::

```figure caption="Direction angles: $OP$ makes angles $\alpha$, $\beta$, $\gamma$ with the positive $x$-, $y$- and $z$-axes, and $l=\cos\alpha$, $m=\cos\beta$, $n=\cos\gamma$."
import numpy as np, matplotlib.pyplot as plt
fig = plt.figure(figsize=(4.6,3.6))
ax = fig.add_subplot(projection='3d')
ax.set_axis_off()
L = 3.2
for v, lab, ha in [((L,0,0), 'X', 'right'), ((0,L,0), 'Y', 'left'), ((0,0,L), 'Z', 'center')]:
    ax.plot([0,v[0]],[0,v[1]],[0,v[2]], color=INK, lw=1.2)
    ax.text(v[0]*1.14, v[1]*1.14, v[2]*1.09, lab, color=INK, fontsize=11, ha=ha)
u = np.array([1.0,2.0,2.0]); u = u/np.linalg.norm(u)
P = 2.9*u
ax.plot([0,P[0]],[0,P[1]],[0,P[2]], color='#d9534f', lw=2.3)
ax.scatter(*P, color='#d9534f', s=30, depthshade=False)
ax.text(P[0]+0.1, P[1]+0.1, P[2]+0.25, 'P(x, y, z)', color='#d9534f', fontsize=9.5)
axes = [(np.array([1.0,0,0]), r'$\alpha$', ACCENT, 1.75),
        (np.array([0,1.0,0]), r'$\beta$', '#2e8b57', 1.50),
        (np.array([0,0,1.0]), r'$\gamma$', '#b8860b', 1.50)]
for e, lab, col, rad in axes:
    t = np.linspace(0, 1, 60)[:, None]
    arc = (1-t)*e + t*u
    arc = rad*arc/np.linalg.norm(arc, axis=1)[:, None]
    ax.plot(arc[:,0], arc[:,1], arc[:,2], color=col, lw=1.3)
    tag = arc[9]*1.30
    ax.text(tag[0], tag[1], tag[2], lab, color=col, fontsize=11, ha='center')
# projection of P on the xy-plane
ax.plot([P[0],P[0]],[P[1],P[1]],[0,P[2]], color=MUTED, lw=0.9, ls=(0,(3,3)))
ax.text(0.1, 0.06, -0.42, 'O', color=INK, fontsize=10)
ax.set_xlim(-0.7,L+0.5); ax.set_ylim(-0.7,L+0.5); ax.set_zlim(-0.7,L+0.5)
ax.set_box_aspect((1,1,1))
ax.view_init(elev=20, azim=36)
```

::: derivation The relation $l^{2}+m^{2}+n^{2} = 1$
Let $P(x,y,z)$ be a point on the directed line through the origin, with
$OP = r = \sqrt{x^{2}+y^{2}+z^{2}}$.

Drop a perpendicular $PA$ from $P$ to the $x$-axis. Then $OA = x$ and
$\triangle OAP$ is right-angled at $A$, so

$$ \cos\alpha = \frac{OA}{OP} = \frac{x}{r} $$

Similarly $\cos\beta = \dfrac{y}{r}$ and $\cos\gamma = \dfrac{z}{r}$, so

$$ l = \frac{x}{r}, \qquad m = \frac{y}{r}, \qquad n = \frac{z}{r} $$

Squaring and adding,

$$ l^{2}+m^{2}+n^{2} = \frac{x^{2}+y^{2}+z^{2}}{r^{2}} = \frac{r^{2}}{r^{2}} = 1 $$
:::

::: caution Three cosines, but only two free choices
$l^{2}+m^{2}+n^{2} = 1$ means the three direction cosines are **not**
independent — you cannot pick all three. In particular no set like
$(\frac12,\frac12,\frac12)$ can be direction cosines, since
$\frac14+\frac14+\frac14 \ne 1$. Note also
$\sin^{2}\alpha+\sin^{2}\beta+\sin^{2}\gamma = 3-1 = 2$.
:::

### Direction ratios

Any three numbers $a$, $b$, $c$ proportional to $l$, $m$, $n$ are called
**direction ratios** of the line. Direction ratios are far more convenient,
because you may scale them freely. To recover the direction cosines, divide by
the length:

$$ l = \pm\frac{a}{\sqrt{a^{2}+b^{2}+c^{2}}}, \quad
m = \pm\frac{b}{\sqrt{a^{2}+b^{2}+c^{2}}}, \quad
n = \pm\frac{c}{\sqrt{a^{2}+b^{2}+c^{2}}} $$

The $\pm$ appears because a line has two opposite directions.

::: key Direction ratios of a join, and the angle between two lines
- The line through $A(x_1,y_1,z_1)$ and $B(x_2,y_2,z_2)$ has direction ratios
  $$ (x_2-x_1,\ y_2-y_1,\ z_2-z_1) $$
- If two lines have direction cosines $(l_1,m_1,n_1)$ and $(l_2,m_2,n_2)$, the
  angle $\theta$ between them satisfies
  $$ \cos\theta = l_1l_2+m_1m_2+n_1n_2 $$
- In terms of direction ratios,
  $$ \cos\theta = \frac{a_1a_2+b_1b_2+c_1c_2}{\sqrt{a_1^{2}+b_1^{2}+c_1^{2}}\ \sqrt{a_2^{2}+b_2^{2}+c_2^{2}}} $$
- **Perpendicular:** $a_1a_2+b_1b_2+c_1c_2 = 0$. **Parallel:**
  $\dfrac{a_1}{a_2} = \dfrac{b_1}{b_2} = \dfrac{c_1}{c_2}$.
:::

```figure caption="The angle between two lines through the origin with direction ratios $(2,2,1)$ and $(4,1,8)$ is $\cos^{-1}\tfrac23 \approx 48.2^{\circ}$."
import numpy as np, matplotlib.pyplot as plt
fig = plt.figure(figsize=(4.6,3.4))
ax = fig.add_subplot(projection='3d')
ax.set_axis_off()
L = 3.0
for v, lab, ha in [((L,0,0), 'X', 'right'), ((0,L,0), 'Y', 'left'), ((0,0,L), 'Z', 'center')]:
    ax.plot([0,v[0]],[0,v[1]],[0,v[2]], color=INK, lw=1.0)
    ax.text(v[0]*1.16, v[1]*1.16, v[2]*1.10, lab, color=MUTED, fontsize=10, ha=ha)
u = np.array([2.0,2.0,1.0]); u = u/np.linalg.norm(u)
v = np.array([4.0,1.0,8.0]); v = v/np.linalg.norm(v)
for w, col, lab, d, ha in [(u, ACCENT, '(2, 2, 1)', (0.0,0.10,0.45), 'left'),
                           (v, '#2e8b57', '(4, 1, 8)', (0.0,-0.35,0.14), 'right')]:
    ax.plot([0,2.5*w[0]],[0,2.5*w[1]],[0,2.5*w[2]], color=col, lw=2.2)
    ax.text(2.5*w[0]+d[0], 2.5*w[1]+d[1], 2.5*w[2]+d[2], lab, color=col,
            fontsize=9.5, ha=ha)
t = np.linspace(0, 1, 60)[:, None]
arc = (1-t)*u + t*v
arc = 1.35*arc/np.linalg.norm(arc, axis=1)[:, None]
ax.plot(arc[:,0], arc[:,1], arc[:,2], color='#d9534f', lw=1.5)
mid = arc[30]*1.30
ax.text(mid[0], mid[1], mid[2], r'$\theta$', color='#d9534f', fontsize=11)
ax.text(0.08, 0.05, -0.40, 'O', color=INK, fontsize=10)
ax.set_xlim(-0.7,L+0.6); ax.set_ylim(-0.7,L+0.6); ax.set_zlim(-0.7,L+0.6)
ax.set_box_aspect((1,1,1))
ax.view_init(elev=14, azim=22)
```

::: example Worked example 13.7 — a missing direction angle
**Problem.** A line makes angles $60^{\circ}$ and $45^{\circ}$ with the positive
$x$- and $y$-axes. Find the angle it makes with the positive $z$-axis, and its
direction cosines.

**Solution.** $l = \cos 60^{\circ} = \frac12$ and $m = \cos 45^{\circ} = \frac{1}{\sqrt{2}}$.
Using $l^{2}+m^{2}+n^{2} = 1$,

$$ n^{2} = 1-\frac14-\frac12 = \frac14 \;\Rightarrow\; n = \pm\frac12 $$

So $\gamma = 60^{\circ}$ or $\gamma = 120^{\circ}$, and the direction cosines are

$$ \left(\frac12,\ \frac{1}{\sqrt{2}},\ \frac12\right)
\quad\text{or}\quad \left(\frac12,\ \frac{1}{\sqrt{2}},\ -\frac12\right) $$
:::

::: example Worked example 13.8 — direction cosines of a join
**Problem.** Find the direction ratios and direction cosines of the line joining
$A(1,2,3)$ and $B(2,4,5)$.

**Solution.** Direction ratios are the differences:

$$ (2-1,\ 4-2,\ 5-3) = (1,\ 2,\ 2) $$

Their length is $\sqrt{1^{2}+2^{2}+2^{2}} = \sqrt{9} = 3$, so the direction cosines
are

$$ \left(\frac13,\ \frac23,\ \frac23\right) $$

**Check.** $\frac19+\frac49+\frac49 = \frac99 = 1$ ✓.
:::

::: example Worked example 13.9 — angle between two lines
**Problem.** Find the acute angle between two lines whose direction ratios are
$(2,2,1)$ and $(4,1,8)$.

**Solution.**

$$ a_1a_2+b_1b_2+c_1c_2 = 2(4)+2(1)+1(8) = 8+2+8 = 18 $$

$$ \sqrt{a_1^{2}+b_1^{2}+c_1^{2}} = \sqrt{4+4+1} = 3, \qquad
\sqrt{a_2^{2}+b_2^{2}+c_2^{2}} = \sqrt{16+1+64} = 9 $$

$$ \cos\theta = \frac{18}{3\times 9} = \frac{18}{27} = \frac23 $$

$$ \theta = \cos^{-1}\frac23 \approx 48.19^{\circ} $$
:::

::: example Worked example 13.10 — collinearity
**Problem.** Show that the points $A(1,2,3)$, $B(4,0,4)$ and $C(-2,4,2)$ are
collinear.

**Solution.** Direction ratios of $AB$: $(4-1,\ 0-2,\ 4-3) = (3,-2,1)$.
Direction ratios of $AC$: $(-2-1,\ 4-2,\ 2-3) = (-3,2,-1)$.

Since $(-3,2,-1) = -1\times(3,-2,1)$, the two sets are proportional, so $AB$ and
$AC$ are parallel lines. They share the point $A$, so they are the same line and
$A$, $B$, $C$ are collinear.

(The negative factor tells us $A$ lies *between* $B$ and $C$.)
:::

::: tip Use squares and ratios, not surds
In three dimensions almost every standard question can be settled without ever
taking a square root: compare $AB^{2}$ with $BC^{2}$ for triangles, and compare
*ratios* $a_1:b_1:c_1$ with $a_2:b_2:c_2$ for parallel lines. You lose marks to
arithmetic slips, not to missing ideas.
:::

## Chapter summary

- Three mutually perpendicular axes give three coordinate planes ($x=0$, $y=0$,
  $z=0$) and eight octants; a point is an ordered triple $(x,y,z)$.
- Distance of $P(x,y,z)$ from the $xy$-plane is $|z|$; from the $x$-axis is
  $\sqrt{y^{2}+z^{2}}$; from the origin is $\sqrt{x^{2}+y^{2}+z^{2}}$.
- $AB = \sqrt{(x_2-x_1)^{2}+(y_2-y_1)^{2}+(z_2-z_1)^{2}}$.
- Section formula (internal, ratio $m:n$):
  $\left(\dfrac{mx_2+nx_1}{m+n},\ \dfrac{my_2+ny_1}{m+n},\ \dfrac{mz_2+nz_1}{m+n}\right)$;
  for external division replace $n$ by $-n$. Midpoint is the case $m=n$;
  centroid is the average of the three vertices.
- Direction cosines $l = \cos\alpha$, $m = \cos\beta$, $n = \cos\gamma$ satisfy
  $l^{2}+m^{2}+n^{2} = 1$, and $l = \dfrac{x}{r}$, $m = \dfrac{y}{r}$,
  $n = \dfrac{z}{r}$ with $r = OP$.
- Direction ratios $(a,b,c)$ are any numbers proportional to $(l,m,n)$; divide by
  $\sqrt{a^{2}+b^{2}+c^{2}}$ to get the direction cosines.
- The join of $A$ and $B$ has direction ratios $(x_2-x_1, y_2-y_1, z_2-z_1)$.
- $\cos\theta = l_1l_2+m_1m_2+n_1n_2$; lines are perpendicular when
  $a_1a_2+b_1b_2+c_1c_2 = 0$ and parallel when their direction ratios are
  proportional.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The distance of the point $(2,-3,6)$ from the origin is <span class="marks">[1]</span>
   (a) $5$ (b) $7$ (c) $11$ (d) $\sqrt{41}$
2. The number of octants into which the coordinate planes divide space is <span class="marks">[1]</span>
   (a) 4 (b) 6 (c) 8 (d) 12
3. If $l$, $m$, $n$ are direction cosines then $l^{2}+m^{2}+n^{2}$ equals <span class="marks">[1]</span>
   (a) $0$ (b) $1$ (c) $2$ (d) $3$
4. The direction ratios of the line joining $(1,0,2)$ and $(3,4,5)$ are <span class="marks">[1]</span>
   (a) $(2,4,3)$ (b) $(4,4,7)$ (c) $(3,0,10)$ (d) $(-2,-4,-7)$
5. The distance of the point $(1,-2,3)$ from the $y$-axis is <span class="marks">[1]</span>
   (a) $1$ (b) $2$ (c) $\sqrt{10}$ (d) $\sqrt{13}$
6. Two lines with direction ratios $(1,2,-1)$ and $(3,-1,1)$ are <span class="marks">[1]</span>
   (a) parallel (b) perpendicular (c) coincident (d) inclined at $60^{\circ}$

::: note Answers to Group A
**1.** (b) — $\sqrt{4+9+36} = \sqrt{49} = 7$.
**2.** (c) — three planes, each giving two sides: $2^{3} = 8$.
**3.** (b) — proved in §13.3.
**4.** (a) — $(3-1,\ 4-0,\ 5-2) = (2,4,3)$.
**5.** (c) — ignore $y$: $\sqrt{1^{2}+3^{2}} = \sqrt{10}$.
**6.** (b) — $1(3)+2(-1)+(-1)(1) = 3-2-1 = 0$.
:::

**Group B — Short answer (5 marks each)**

1. Derive the formula for the distance between the points $A(x_1,y_1,z_1)$ and
   $B(x_2,y_2,z_2)$. <span class="marks">[5]</span>
2. Show that the points $(-2,3,5)$, $(1,2,3)$ and $(7,0,-1)$ are collinear. <span class="marks">[5]</span>
3. Find the ratio in which the $zx$-plane divides the join of $A(-2,4,7)$ and
   $B(3,-5,8)$. <span class="marks">[5]</span>
4. A line makes angles $90^{\circ}$ and $135^{\circ}$ with the positive $x$- and
   $y$-axes. Find the angle it makes with the positive $z$-axis and write down
   its direction cosines. <span class="marks">[5]</span>
5. Find the angle between the lines whose direction ratios are $(1,1,2)$ and
   $(\sqrt{3}-1,\ -\sqrt{3}-1,\ 4)$. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Complete the rectangular box on $AB$ as a space diagonal, with
$M(x_2,y_2,z_1)$. $A$ and $M$ lie in the plane $z = z_1$, so
$AM^{2} = (x_2-x_1)^{2}+(y_2-y_1)^{2}$. The edge $MB$ is parallel to the $z$-axis,
so $MB = |z_2-z_1|$ and $MB \perp AM$. Pythagoras in $\triangle AMB$ gives
$AB^{2} = AM^{2}+MB^{2}$, hence
$AB = \sqrt{(x_2-x_1)^{2}+(y_2-y_1)^{2}+(z_2-z_1)^{2}}$.

**2.** Let $A(-2,3,5)$, $B(1,2,3)$, $C(7,0,-1)$. Direction ratios of $AB$ are
$(3,-1,-2)$ and of $AC$ are $(9,-3,-6) = 3\times(3,-1,-2)$. The ratios are
proportional and the lines share $A$, so the three points are collinear.
(Alternatively $AB = \sqrt{9+1+4} = \sqrt{14}$, $BC = \sqrt{36+4+16} = \sqrt{56} = 2\sqrt{14}$,
$AC = \sqrt{81+9+36} = \sqrt{126} = 3\sqrt{14}$, and $AB+BC = AC$.)

**3.** Let the $zx$-plane cut $AB$ in the ratio $k:1$. The dividing point is
$\left(\frac{3k-2}{k+1},\ \frac{-5k+4}{k+1},\ \frac{8k+7}{k+1}\right)$. On the
$zx$-plane $y = 0$, so $-5k+4 = 0$ and $k = \frac45$. The ratio is $4:5$
internally.

**4.** $l = \cos 90^{\circ} = 0$ and $m = \cos 135^{\circ} = -\frac{1}{\sqrt{2}}$. Then
$n^{2} = 1-0-\frac12 = \frac12$, so $n = \pm\frac{1}{\sqrt{2}}$ and
$\gamma = 45^{\circ}$ or $135^{\circ}$. The direction cosines are
$\left(0,\ -\frac{1}{\sqrt{2}},\ \frac{1}{\sqrt{2}}\right)$ or
$\left(0,\ -\frac{1}{\sqrt{2}},\ -\frac{1}{\sqrt{2}}\right)$.

**5.** $a_1a_2+b_1b_2+c_1c_2 = 1(\sqrt{3}-1)+1(-\sqrt{3}-1)+2(4) = -2+8 = 6$.
The lengths are $\sqrt{1+1+4} = \sqrt{6}$ and
$\sqrt{(\sqrt{3}-1)^{2}+(\sqrt{3}+1)^{2}+16} = \sqrt{(4-2\sqrt{3})+(4+2\sqrt{3})+16} = \sqrt{24} = 2\sqrt{6}$.
So $\cos\theta = \dfrac{6}{\sqrt{6}\cdot 2\sqrt{6}} = \dfrac{6}{12} = \dfrac12$, giving
$\theta = 60^{\circ}$.
:::

**Group C — Long answer (8 marks each)**

1. (a) Define the direction cosines of a line and prove that
   $l^{2}+m^{2}+n^{2} = 1$. <span class="marks">[5]</span>
   (b) A line makes angles $60^{\circ}$, $45^{\circ}$ with the $x$- and $y$-axes.
   Find the angle it makes with the $z$-axis. <span class="marks">[3]</span>
2. The vertices of a triangle are $A(3,-1,2)$, $B(1,-3,-4)$ and $C(-1,1,2)$.
   (a) Find the lengths of the three sides and classify the triangle. <span class="marks">[4]</span>
   (b) Find the centroid, and the length of the median from $A$. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** (a) If a directed line through the origin makes angles $\alpha$, $\beta$,
$\gamma$ with the positive axes, its direction cosines are
$l = \cos\alpha$, $m = \cos\beta$, $n = \cos\gamma$. Take $P(x,y,z)$ on the line
with $OP = r$. Dropping a perpendicular from $P$ to the $x$-axis at $A$ gives a
right angle at $A$ with $OA = x$, so $\cos\alpha = \frac{x}{r}$; similarly
$\cos\beta = \frac{y}{r}$, $\cos\gamma = \frac{z}{r}$. Hence
$$ l^{2}+m^{2}+n^{2} = \frac{x^{2}+y^{2}+z^{2}}{r^{2}} = \frac{r^{2}}{r^{2}} = 1 $$

(b) $l = \cos 60^{\circ} = \frac12$, $m = \cos 45^{\circ} = \frac{1}{\sqrt{2}}$, so
$n^{2} = 1-\frac14-\frac12 = \frac14$ and $n = \pm\frac12$. Therefore
$\gamma = 60^{\circ}$ or $120^{\circ}$.

**2.** (a)
$AB^{2} = (1-3)^{2}+(-3+1)^{2}+(-4-2)^{2} = 4+4+36 = 44$, so $AB = 2\sqrt{11}$.
$BC^{2} = (-1-1)^{2}+(1+3)^{2}+(2+4)^{2} = 4+16+36 = 56$, so $BC = 2\sqrt{14}$.
$CA^{2} = (3+1)^{2}+(-1-1)^{2}+(2-2)^{2} = 16+4+0 = 20$, so $CA = 2\sqrt{5}$.
All three sides are different and $AB^{2}+CA^{2} = 44+20 = 64 \ne 56$, so the
triangle is **scalene** and not right-angled.

(b) Centroid
$G = \left(\frac{3+1-1}{3},\ \frac{-1-3+1}{3},\ \frac{2-4+2}{3}\right) = \left(1,\ -1,\ 0\right)$.
The midpoint of $BC$ is $D = \left(\frac{1-1}{2},\ \frac{-3+1}{2},\ \frac{-4+2}{2}\right) = (0,-1,-1)$,
so the median from $A$ has length
$$ AD = \sqrt{(0-3)^{2}+(-1+1)^{2}+(-1-2)^{2}} = \sqrt{9+0+9} = \sqrt{18} = 3\sqrt{2}\ \text{units} $$
:::
