---
subject: Mathematics
grade: 12
unit: 16
title: Mechanics (alternative to Unit 15)
hours: 12
area: Computational Methods OR Mechanics
---

Mechanics is the mathematics of forces and motion. **Statics** asks when a body
stays still: the forces on it must cancel, and so must their turning effects.
**Dynamics** asks how a body moves when they do not cancel, and the answer is
Newton's second law. This chapter is the **full alternative to Unit 15**: the CDC
syllabus offers Computational Methods *or* Mechanics as the final $12$-hour unit,
your school teaches one of them, and the question paper sets the two as
alternatives. Everything you need for the Mechanics option is here — nothing is
left in Unit 15.

::: key What the exam asks
Statics questions are nearly always "three concurrent forces in equilibrium" —
resolve, or use Lami's theorem. Dynamics questions are $F = ma$ applied to one
body at a time, or a projectile with $T$, $H$ and $R$ to find. Group C usually
wants a *derivation* (Lami's theorem, or the range formula) followed by a
numerical part. Take $g = 10\ \text{m s}^{-2}$ unless the question says otherwise,
and **always draw the free-body diagram** — markers give a mark for it.
:::

## 16.1 Statics: triangle law of forces; Lami's theorem

### Force as a vector

A **force** has magnitude (newtons, N) and direction, so forces add like vectors.
The single force that has the same effect as two or more forces together is their
**resultant**.

::: derivation Resultant of two forces (parallelogram law)
Let $P$ and $Q$ act at a point $O$ with angle $\theta$ between them. Complete the
parallelogram; the diagonal is the resultant $R$. Resolve along and perpendicular
to $P$:

$$ R\cos\alpha = P + Q\cos\theta, \qquad R\sin\alpha = Q\sin\theta $$

Square and add. Since $\cos^2\alpha + \sin^2\alpha = 1$,

$$ R^2 = (P + Q\cos\theta)^2 + (Q\sin\theta)^2
= P^2 + 2PQ\cos\theta + Q^2(\cos^2\theta + \sin^2\theta) $$

$$ R = \sqrt{P^2 + Q^2 + 2PQ\cos\theta} $$

Dividing the two starting equations gives the direction of $R$, measured from $P$:

$$ \tan\alpha = \frac{Q\sin\theta}{P + Q\cos\theta} $$
:::

Two special cases are worth remembering: $\theta = 0^\circ$ gives $R = P+Q$, and
$\theta = 90^\circ$ gives $R = \sqrt{P^2+Q^2}$.

The reverse operation, **resolution**, replaces one force by two perpendicular
components. A force $F$ at angle $\theta$ to the $x$-axis has components
$F\cos\theta$ and $F\sin\theta$.

```figure caption="Left: the parallelogram law — $R = \sqrt{P^2+Q^2+2PQ\cos\theta}$ at angle $\alpha$ to $P$. Right: resolution of a force $F$ into $F\cos\theta$ along $x$ and $F\sin\theta$ along $y$."
import numpy as np
fig, axes = plt.subplots(1, 2, figsize=(5.2,2.6))
ax = axes[0]
P = np.array([2.6, 0.0]); Q = np.array([1.35, 1.95]); R = P + Q
def arr(ax, a, b, c, lw=2.0, ls='-'):
    ax.annotate('', xy=b, xytext=a, arrowprops=dict(arrowstyle='-|>', color=c,
                lw=lw, ls=ls, mutation_scale=12, shrinkA=0, shrinkB=0))
ax.plot([P[0], R[0]], [P[1], R[1]], color=MUTED, lw=0.9, ls=(0,(3,2)))
ax.plot([Q[0], R[0]], [Q[1], R[1]], color=MUTED, lw=0.9, ls=(0,(3,2)))
arr(ax, (0,0), P, ACCENT); arr(ax, (0,0), Q, '#2e8b57'); arr(ax, (0,0), R, '#d9534f', 2.4)
th = np.linspace(0, np.arctan2(Q[1], Q[0]), 40)
ax.plot(0.62*np.cos(th), 0.62*np.sin(th), color=MUTED, lw=0.9)
th2 = np.linspace(0, np.arctan2(R[1], R[0]), 40)
ax.plot(0.95*np.cos(th2), 0.95*np.sin(th2), color='#d9534f', lw=0.9)
ax.text(0.80, 0.90, r'$\theta$', fontsize=10, color=MUTED)
ax.text(1.13, 0.30, r'$\alpha$', fontsize=10, color='#d9534f')
ax.text(2.62, -0.24, '$P$', fontsize=10.5, color=ACCENT)
ax.text(1.16, 2.06, '$Q$', fontsize=10.5, color='#2e8b57')
ax.text(3.62, 2.12, '$R$', fontsize=11, color='#d9534f')
ax.text(-0.30, -0.26, '$O$', fontsize=10, color=INK)
ax.set_xlim(-0.55, 4.55); ax.set_ylim(-0.55, 2.55)
ax.set_aspect('equal'); ax.axis('off')
ax = axes[1]
F = np.array([2.35, 1.70])
ax.plot([F[0], F[0]], [0, F[1]], color=MUTED, lw=0.9, ls=(0,(3,2)))
ax.plot([0, F[0]], [F[1], F[1]], color=MUTED, lw=0.9, ls=(0,(3,2)))
arr(ax, (0,0), (3.3,0), INK, 1.1); arr(ax, (0,0), (0,2.35), INK, 1.1)
arr(ax, (0,0), F, '#d9534f', 2.4)
arr(ax, (0,0), (F[0],0), ACCENT, 2.0)
arr(ax, (0,0), (0,F[1]), '#2e8b57', 2.0)
th = np.linspace(0, np.arctan2(F[1], F[0]), 40)
ax.plot(0.72*np.cos(th), 0.72*np.sin(th), color=MUTED, lw=0.9)
ax.text(0.80, 0.26, r'$\theta$', fontsize=10, color=MUTED)
ax.text(2.42, 1.76, '$F$', fontsize=11, color='#d9534f')
ax.text(0.92, -0.35, r'$F\cos\theta$', fontsize=9.4, color=ACCENT)
ax.text(-0.52, 1.92, r'$F\sin\theta$', fontsize=9.4, color='#2e8b57', rotation=90)
ax.text(3.34, -0.05, '$x$', fontsize=10, color=INK)
ax.text(-0.05, 2.44, '$y$', fontsize=10, color=INK)
ax.set_xlim(-0.75, 3.7); ax.set_ylim(-0.6, 2.65)
ax.set_aspect('equal'); ax.axis('off')
fig.tight_layout()
```

::: example Worked example 16.1
**Problem.** Two forces of $5$ N and $12$ N act at a point at right angles. Find
the magnitude of the resultant and the angle it makes with the $5$ N force.

**Solution.** With $\theta = 90^\circ$, $\cos\theta = 0$:

$$ R = \sqrt{5^2 + 12^2} = \sqrt{25+144} = \sqrt{169} = 13\ \text{N} $$

$$ \tan\alpha = \frac{12\sin 90^\circ}{5 + 12\cos 90^\circ} = \frac{12}{5} = 2.4 $$

$$ \alpha = \tan^{-1}(2.4) = 67.4^\circ $$

The resultant is $13$ N at $67.4^\circ$ to the $5$ N force.
:::

::: example Worked example 16.2
**Problem.** Forces of $5$ N and $3$ N act at a point with $60^\circ$ between
them. Find their resultant, and state the force needed to keep the point in
equilibrium.

**Solution.** $\cos 60^\circ = \tfrac12$, so

$$ R = \sqrt{5^2 + 3^2 + 2(5)(3)\left(\tfrac12\right)} = \sqrt{25+9+15}
= \sqrt{49} = 7\ \text{N} $$

$$ \tan\alpha = \frac{3\sin 60^\circ}{5 + 3\cos 60^\circ}
= \frac{3(0.8660)}{5+1.5} = \frac{2.598}{6.5} = 0.3997
\;\Longrightarrow\; \alpha = 21.8^\circ $$

The **equilibrant** is the force that balances the resultant: it has the same
magnitude, $7$ N, but the opposite direction, i.e. at $21.8^\circ + 180^\circ$ to
the $5$ N force.
:::

### The triangle law and the polygon of forces

::: definition Triangle law of forces
If **three forces acting at a point** can be represented in magnitude and
direction by the three sides of a triangle **taken in order**, the forces are in
equilibrium.

Its converse is equally useful: if three concurrent forces are in equilibrium,
they can be represented by the sides of some triangle taken in order — so drawing
them head to tail gives a **closed** triangle.
:::

Extending head-to-tail drawing to more forces gives the **polygon of forces**: any
number of concurrent forces are in equilibrium exactly when their head-to-tail
polygon closes. If it does not close, the closing side (drawn from the last head
back to the first tail) is the *equilibrant*, and its reverse is the resultant.

```figure caption="(a) Three concurrent forces at $O$. (b) Drawn head to tail they close into a triangle, so they are in equilibrium. (c) Five concurrent forces in equilibrium close into a polygon."
import numpy as np
fig, axes = plt.subplots(1, 3, figsize=(5.2,2.2))
def arr(ax, a, b, c, lw=2.0):
    ax.annotate('', xy=b, xytext=a, arrowprops=dict(arrowstyle='-|>', color=c,
                lw=lw, mutation_scale=11, shrinkA=0, shrinkB=0))
P = np.array([1.0, 0.0]); Q = np.array([-0.5, 0.95]); Rv = -(P + Q)
ax = axes[0]
for v, c, lab, off in [(P, ACCENT, '$P$', (0.10, -0.22)), (Q, '#2e8b57', '$Q$', (-0.36, 0.10)),
                       (Rv, '#d9534f', '$R$', (-0.12, -0.34))]:
    arr(ax, (0,0), v, c); ax.text(v[0]+off[0], v[1]+off[1], lab, fontsize=10.5, color=c)
ax.plot([0],[0],'o',color=INK,ms=4); ax.text(0.06, 0.10, '$O$', fontsize=9.5, color=INK)
ax.set_title('(a) forces at a point', fontsize=8.6, pad=6)
ax.set_xlim(-1.25, 1.55); ax.set_ylim(-1.75, 1.25)
ax.set_aspect('equal'); ax.axis('off')
ax = axes[1]
pts = [np.array([0,0]), P, P+Q, P+Q+Rv]
for i, (c, lab) in enumerate([(ACCENT, '$P$'), ('#2e8b57', '$Q$'), ('#d9534f', '$R$')]):
    arr(ax, pts[i], pts[i+1], c)
    m = (pts[i] + pts[i+1])/2
    ax.text(m[0]+0.10, m[1]+0.08, lab, fontsize=10.5, color=c)
ax.set_title('(b) closed triangle', fontsize=8.6, pad=6)
ax.set_xlim(-0.45, 1.55); ax.set_ylim(-0.75, 1.55)
ax.set_aspect('equal'); ax.axis('off')
ax = axes[2]
angs = np.array([20, 85, 150, 215, 300])*np.pi/180
mags = np.array([1.0, 0.75, 0.9, 0.85, 0.95])
vs = np.stack([mags*np.cos(angs), mags*np.sin(angs)], axis=1)
vs[-1] = -vs[:-1].sum(axis=0)
pts = np.vstack([[0.0, 0.0], np.cumsum(vs, axis=0)])
ax.plot(pts[:,0], pts[:,1], color=MUTED, lw=0.8)
for i in range(len(vs)):
    arr(ax, pts[i], pts[i+1], SERIES[i % 6], 1.7)
ax.plot([0], [0], 'o', color=INK, ms=3.5)
ax.set_title('(c) closed polygon', fontsize=8.6, pad=6)
ax.set_xlim(-1.45, 1.55); ax.set_ylim(-1.05, 1.95)
ax.set_aspect('equal'); ax.axis('off')
fig.tight_layout()
```

::: example Worked example 16.3
**Problem.** Three forces of $3$ N, $4$ N and $5$ N act at a point and keep it in
equilibrium. Find the angle between the $3$ N and the $4$ N forces.

**Solution.** In equilibrium the $5$ N force must be the equilibrant of the other
two, so the resultant of the $3$ N and $4$ N forces is $5$ N. If $\theta$ is the
angle between them,

$$ 5^2 = 3^2 + 4^2 + 2(3)(4)\cos\theta $$
$$ 25 = 9 + 16 + 24\cos\theta \;\Longrightarrow\; 24\cos\theta = 0
\;\Longrightarrow\; \cos\theta = 0 $$

$$ \theta = 90^\circ $$

The $3$ N and $4$ N forces are perpendicular. (The head-to-tail triangle is the
$3$–$4$–$5$ right-angled triangle.)
:::

### Lami's theorem

::: key Lami's theorem
If three coplanar forces $P$, $Q$, $R$ acting at a point are in equilibrium, then

$$ \frac{P}{\sin\alpha} = \frac{Q}{\sin\beta} = \frac{R}{\sin\gamma} $$

where $\alpha$ is the angle **between the other two** forces $Q$ and $R$, $\beta$
the angle between $R$ and $P$, and $\gamma$ the angle between $P$ and $Q$. Note
$\alpha + \beta + \gamma = 360^\circ$.
:::

::: derivation Lami's theorem from the triangle of forces
Because the three forces are in equilibrium, drawing them head to tail gives a
closed triangle $ABC$ with $AB$, $BC$, $CA$ representing $P$, $Q$, $R$.

Each side of this triangle is parallel to one of the forces, so the **interior**
angle of the triangle between the sides representing $Q$ and $R$ is the
*supplement* of the angle $\alpha$ between the forces themselves: it equals
$180^\circ - \alpha$. In the same way the other two interior angles are
$180^\circ - \beta$ and $180^\circ - \gamma$.

Apply the sine law to triangle $ABC$ — each side is proportional to the sine of
the opposite angle:

Now match each force to the angle **opposite** its own side. The side
representing $P$ is opposite the interior angle $180^\circ - \alpha$, so

$$ \frac{P}{\sin(180^\circ - \alpha)} = \frac{Q}{\sin(180^\circ - \beta)}
= \frac{R}{\sin(180^\circ - \gamma)} $$

and since $\sin(180^\circ - x) = \sin x$,

$$ \frac{P}{\sin\alpha} = \frac{Q}{\sin\beta} = \frac{R}{\sin\gamma} $$
:::

```figure caption="Lami's theorem. A weight $W$ hangs at $O$ from two strings. The three forces $T_1$, $T_2$, $W$ are in equilibrium, so $T_1/\sin\alpha = T_2/\sin\beta = W/\sin\gamma$, where each angle is the one between the *other* two forces."
import numpy as np
fig, ax = plt.subplots(figsize=(4.6,3.2))
a1, a2 = np.radians(150.0), np.radians(60.0)
u1 = np.array([np.cos(a1), np.sin(a1)])
u2 = np.array([np.cos(a2), np.sin(a2)])
uw = np.array([0.0, -1.0])
CE = 1.45
ax.plot([-2.75, 2.75], [CE, CE], color=INK, lw=1.8)
for x0 in np.arange(-2.65, 2.75, 0.28):
    ax.plot([x0, x0-0.15], [CE, CE+0.17], color=MUTED, lw=0.9)
for u in (u1, u2):
    ax.plot([0, u[0]*CE/u[1]], [0, CE], color=MUTED, lw=1.3)
ax.plot([0, 0], [0, -1.05], color=MUTED, lw=1.3)
def arr(a, b, c, lw=2.3):
    ax.annotate('', xy=b, xytext=a, arrowprops=dict(arrowstyle='-|>', color=c,
                lw=lw, mutation_scale=13, shrinkA=0, shrinkB=0), zorder=6)
arr((0,0), u1*1.20, ACCENT); arr((0,0), u2*1.20, '#2e8b57')
arr((0,0), uw*1.25, '#d9534f')
ax.plot([0],[0],'o',color=INK,ms=5.5, zorder=7)
ax.text(0.10, 0.10, '$O$', fontsize=10.5, color=INK)
ax.text(u1[0]*1.30-0.30, u1[1]*1.30+0.04, '$T_1$', fontsize=11.5, color=ACCENT)
ax.text(u2[0]*1.30+0.16, u2[1]*1.30-0.20, '$T_2$', fontsize=11.5, color='#2e8b57')
ax.text(0.20, -1.24, '$W$', fontsize=11.5, color='#d9534f')
r = 0.62
for lo, hi, lab in [(66, 144, r'$\gamma$'), (156, 264, r'$\beta$'), (276, 414, r'$\alpha$')]:
    th = np.radians(np.linspace(lo, hi, 80))
    ax.plot(r*np.cos(th), r*np.sin(th), color=MUTED, lw=1.0)
    m = np.radians((lo+hi)/2)
    ax.text((r+0.24)*np.cos(m)-0.07, (r+0.24)*np.sin(m)-0.08, lab,
            fontsize=11, color=INK)
ax.add_patch(plt.Rectangle((-0.20, -1.72), 0.40, 0.40, facecolor='#dfe3ea',
                           edgecolor=INK, lw=1.2))
ax.text(0.30, -1.62, 'weight $W$', fontsize=9.0, color=INK)
ax.text(-2.80, 1.74, r'$\alpha+\beta+\gamma = 360^{\circ}$', fontsize=9.2, color=MUTED)
ax.set_xlim(-2.90, 2.90); ax.set_ylim(-2.0, 2.0)
ax.set_aspect('equal'); ax.axis('off')
```

::: example Worked example 16.4
**Problem.** A body of weight $100$ N hangs at $O$ from two light strings $OA$ and
$OB$ attached to a horizontal ceiling, $OA$ making $30^\circ$ and $OB$ making
$60^\circ$ with the ceiling. Find the tension in each string.

**Solution.** The three forces at $O$ are $T_1$ (along $OA$), $T_2$ (along $OB$)
and the weight $W = 100$ N vertically down.

The angle between $T_1$ and $T_2$ is $180^\circ - 30^\circ - 60^\circ = 90^\circ$.
$T_1$ makes $30^\circ$ with the ceiling, so it makes $90^\circ + 30^\circ =
120^\circ$ with the downward vertical; similarly $T_2$ makes $150^\circ$ with it.
Check: $90 + 120 + 150 = 360^\circ$.

By Lami's theorem, each force over the sine of the angle between the other two:

$$ \frac{T_1}{\sin 150^\circ} = \frac{T_2}{\sin 120^\circ} = \frac{100}{\sin 90^\circ} $$

$$ T_1 = 100\sin 150^\circ = 100(0.5) = 50\ \text{N} $$
$$ T_2 = 100\sin 120^\circ = 100(0.8660) = 86.6\ \text{N} $$

**Check by resolving.** Horizontally $T_1\cos 30^\circ = T_2\cos 60^\circ$:
$50(0.8660) = 43.3$ and $86.6(0.5) = 43.3$ — equal. Vertically
$T_1\sin 30^\circ + T_2\sin 60^\circ = 25 + 75 = 100 = W$. Correct.
:::

::: caution Lami pairs a force with the *opposite* angle
$\sin\alpha$ under $P$ means $\alpha$ is the angle between $Q$ and $R$ — the two
forces that are **not** $P$. Writing $P/\sin(\text{angle next to } P)$ is the
standard error and loses every mark in the question. Also, Lami's theorem works
only for **exactly three** concurrent forces; with four or more, resolve instead.
:::

### Moment of a force

A force also turns a body. The **moment** (or torque) of a force about a point is

::: definition Moment of a force
$$ M = F \times d $$
where $d$ is the perpendicular distance from the point to the line of action of
$F$. The unit is the newton metre (N m). Anticlockwise moments are taken
positive.
:::

::: key Conditions for equilibrium of a rigid body
$$ \sum F_x = 0, \qquad \sum F_y = 0, \qquad \sum M = 0 $$
The first two stop it sliding; the third stops it turning. Take moments about a
point through which an unknown force passes — that unknown then disappears from
the equation.
:::

```figure caption="A uniform beam $AB$ of weight $200$ N on supports at its ends carries a $300$ N load $1$ m from $A$. Taking moments about $A$ removes $R_A$ from the equation and gives $R_B = 175$ N at once."
import numpy as np
fig, ax = plt.subplots(figsize=(5.0,2.6))
ax.add_patch(plt.Rectangle((0, 0), 4, 0.26, facecolor='#dfe3ea',
                           edgecolor=INK, lw=1.3))
def arr(a, b, c, lw=2.1):
    ax.annotate('', xy=b, xytext=a, arrowprops=dict(arrowstyle='-|>', color=c,
                lw=lw, mutation_scale=12, shrinkA=0, shrinkB=0))
arr((0, -0.95), (0, -0.04), '#2e8b57'); arr((4, -0.95), (4, -0.04), '#2e8b57')
arr((2, 1.20), (2, 0.30), '#d9534f'); arr((1, 1.20), (1, 0.30), ACCENT)
ax.text(2.08, 1.24, 'weight $200$ N', fontsize=9.2, color='#d9534f')
ax.text(0.16, 1.24, 'load $300$ N', fontsize=9.2, color=ACCENT)
ax.text(-0.62, -0.72, '$R_A$', fontsize=10.5, color='#2e8b57')
ax.text(4.12, -0.72, '$R_B$', fontsize=10.5, color='#2e8b57')
ax.text(-0.14, 0.42, '$A$', fontsize=10.5, color=INK)
ax.text(3.92, 0.42, '$B$', fontsize=10.5, color=INK)
for x0, x1, y0, lab in [(0, 1, -1.45, '$1$ m'), (1, 2, -1.45, '$1$ m'), (2, 4, -1.95, '$2$ m')]:
    ax.annotate('', xy=(x0, y0), xytext=(x1, y0),
                arrowprops=dict(arrowstyle='<|-|>', color=MUTED, lw=0.9, mutation_scale=7))
    ax.text((x0+x1)/2, y0-0.30, lab, fontsize=8.8, color=MUTED, ha='center')
ax.plot([2, 2], [0, -1.90], color=MUTED, lw=0.7, ls=':')
ax.plot([1, 1], [0, -1.40], color=MUTED, lw=0.7, ls=':')
ax.set_xlim(-0.85, 4.85); ax.set_ylim(-2.45, 1.75)
ax.set_aspect('equal'); ax.axis('off')
```

::: example Worked example 16.5
**Problem.** A uniform beam $AB$ of length $4$ m and weight $200$ N rests
horizontally on supports at $A$ and $B$. A load of $300$ N is hung $1$ m from $A$.
Find the reactions at the supports.

**Solution.** The beam is uniform, so its weight acts at the midpoint, $2$ m from
$A$. Let the (vertical) reactions be $R_A$ and $R_B$.

**Moments about $A$** (anticlockwise positive; $R_A$ passes through $A$ so it
contributes nothing):

$$ R_B(4) - 200(2) - 300(1) = 0 $$
$$ 4R_B = 400 + 300 = 700 \;\Longrightarrow\; R_B = 175\ \text{N} $$

**Vertical forces:**

$$ R_A + R_B = 200 + 300 = 500 \;\Longrightarrow\; R_A = 500 - 175 = 325\ \text{N} $$

**Check by taking moments about $B$:**
$325(4) - 200(2) - 300(3) = 1300 - 400 - 900 = 0$. Correct.
:::

### Free-body diagrams

A **free-body diagram** shows one body alone, with every force acting *on it*
drawn as an arrow **starting at the point where that force is applied**. Draw
nothing else: no forces the body exerts on other things, and no velocities.

```figure caption="Free-body diagram of a block on a rough plane inclined at $\theta$, pulled by a force $P$ up the plane. Every arrow starts at the point where its force acts. The weight $mg$ is resolved (dashed) into $mg\sin\theta$ down the slope and $mg\cos\theta$ into the surface."
import numpy as np
fig, ax = plt.subplots(figsize=(5.0,3.2))
th = np.radians(30.0)
L = 5.0
ax.plot([0, L*np.cos(th)], [0, L*np.sin(th)], color=INK, lw=2.0)
ax.plot([0, L*np.cos(th)], [0, 0], color=INK, lw=1.2)
ax.plot([L*np.cos(th), L*np.cos(th)], [0, L*np.sin(th)], color=MUTED, lw=0.9, ls=(0,(4,3)))
for t in np.linspace(0.10, 0.97, 13):
    x0 = t*L*np.cos(th)
    ax.plot([x0, x0-0.17], [t*L*np.sin(th), t*L*np.sin(th)-0.21], color=MUTED, lw=0.8)
thd = np.linspace(0, th, 40)
ax.plot(1.05*np.cos(thd), 1.05*np.sin(thd), color=MUTED, lw=0.9)
ax.text(1.14, 0.20, r'$\theta$', fontsize=11, color=MUTED)
u = np.array([np.cos(th), np.sin(th)])
n = np.array([-np.sin(th), np.cos(th)])
w, h = 1.05, 0.72
C = 2.75*u + (h/2)*n
corners = [C + a*w/2*u + b*h/2*n for a, b in [(-1,-1), (1,-1), (1,1), (-1,1)]]
ax.add_patch(plt.Polygon(corners, closed=True, facecolor='#dfe3ea',
                         edgecolor=INK, lw=1.4, zorder=3))
contact = C - (h/2)*n
def arr(a, b, c, lw=2.2, ls='-'):
    ax.annotate('', xy=b, xytext=a, arrowprops=dict(arrowstyle='-|>', color=c,
                lw=lw, ls=ls, mutation_scale=12, shrinkA=0, shrinkB=0), zorder=6)
arr(contact, contact + 1.75*n, '#2e8b57')
arr(contact, contact - 1.45*u, '#b8860b')
arr(C, C + 1.60*u, ACCENT)
mg = 1.45
arr(C, C - np.array([0.0, mg]), '#d9534f')
arr(C, C - mg*np.sin(th)*u, '#d9534f', 1.3, (0,(3,2)))
arr(C, C - mg*np.cos(th)*n, '#d9534f', 1.3, (0,(3,2)))
t1 = contact + 1.82*n; ax.text(t1[0]-0.08, t1[1]+0.08, '$N$', fontsize=11.5, color='#2e8b57')
t2 = contact - 1.52*u; ax.text(t2[0]-0.18, t2[1]+0.20, '$f$', fontsize=11.5, color='#b8860b')
t3 = C + 1.68*u; ax.text(t3[0]+0.06, t3[1]+0.02, '$P$', fontsize=11.5, color=ACCENT)
ax.text(C[0]+0.10, C[1]-mg-0.16, '$mg$', fontsize=11.5, color='#d9534f')
q1 = C - mg*np.sin(th)*u
ax.text(q1[0]-1.06, q1[1]+0.22, r'$mg\sin\theta$', fontsize=9.2, color='#d9534f')
q2 = C - mg*np.cos(th)*n
ax.text(q2[0]+0.10, q2[1]-0.12, r'$mg\cos\theta$', fontsize=9.2, color='#d9534f')
ax.text(C[0]-0.16, C[1]-0.08, 'm', fontsize=10, color=INK, zorder=7)
ax.set_xlim(-0.6, 5.9); ax.set_ylim(-2.1, 4.2)
ax.set_aspect('equal'); ax.axis('off')
```

::: example Worked example 16.6
**Problem.** A body of mass $20$ kg rests on a **smooth** plane inclined at
$30^\circ$ to the horizontal. Find the force $P$, acting up the line of greatest
slope, needed to keep it in equilibrium, and the normal reaction.
(Take $g = 10\ \text{m s}^{-2}$.)

**Solution.** Weight $= mg = 20(10) = 200$ N. Smooth means $f = 0$. Resolve along
and perpendicular to the plane.

Along the plane: $\;P = mg\sin 30^\circ = 200\left(\tfrac12\right) = 100\ \text{N}$

Perpendicular: $\;N = mg\cos 30^\circ = 200\left(\dfrac{\sqrt{3}}{2}\right)
= 100\sqrt{3} = 173.2\ \text{N}$

So $P = 100$ N and $N = 173.2$ N.
:::

## 16.2 Dynamics: Newton's laws of motion

::: definition Newton's three laws
**First law.** A body stays at rest, or moves with constant velocity in a
straight line, unless an external force acts on it. (This defines *force* as the
thing that changes motion, and *inertia* as the reluctance to change.)

**Second law.** The rate of change of momentum of a body is proportional to the
resultant force and takes place in the direction of that force:

$$ F = \frac{d(mv)}{dt} = ma \quad\text{for constant } m $$

**Third law.** To every action there is an equal and opposite reaction; the two
act on *different* bodies.
:::

**Momentum** is $p = mv$ (kg m s$^{-1}$). Rewriting the second law over a time
$\Delta t$ gives the **impulse–momentum** equation

$$ F\,\Delta t = mv - mu $$

and because the action–reaction pair in a collision are equal and opposite for
the same time, the total momentum of an isolated system is unchanged:

::: key Conservation of linear momentum
$$ m_1u_1 + m_2u_2 = m_1v_1 + m_2v_2 $$
Momentum is conserved in every collision; kinetic energy is conserved only in a
*perfectly elastic* one.
:::

For motion in a straight line with constant acceleration the three equations of
motion apply, and vertical motion under gravity is the case $a = \pm g$:

$$ v = u + at, \qquad s = ut + \tfrac12 at^2, \qquad v^2 = u^2 + 2as $$

::: key Work, energy and power
$$ W = Fs\cos\theta, \qquad \text{K.E.} = \tfrac12 mv^2, \qquad
\text{P.E.} = mgh, \qquad P = \frac{W}{t} = Fv $$

**Work–energy theorem.** The work done by the resultant force equals the change
in kinetic energy:
$$ W = \tfrac12 mv^2 - \tfrac12 mu^2 $$
:::

::: example Worked example 16.7
**Problem.** A body of mass $3$ kg at rest on a smooth horizontal floor is acted
on by a horizontal force of $12$ N. Find (a) the acceleration, (b) the velocity
after $5$ s, (c) the distance travelled in that time, and (d) the work done.

**Solution.** (a) $F = ma \Rightarrow a = \dfrac{12}{3} = 4\ \text{m s}^{-2}$.

(b) $v = u + at = 0 + 4(5) = 20\ \text{m s}^{-1}$.

(c) $s = ut + \tfrac12 at^2 = 0 + \tfrac12(4)(25) = 50\ \text{m}$.

(d) $W = Fs = 12(50) = 600\ \text{J}$.

**Check with the work–energy theorem:**
$\tfrac12 mv^2 - 0 = \tfrac12(3)(20)^2 = 600\ \text{J}$. The two agree.
:::

::: example Worked example 16.8
**Problem.** A block of mass $10$ kg is pulled along a rough horizontal floor by a
horizontal force of $40$ N. The coefficient of friction is $0.25$. Find the
acceleration. ($g = 10\ \text{m s}^{-2}$.)

**Solution.** Vertically there is no acceleration, so the normal reaction is

$$ N = mg = 10(10) = 100\ \text{N} $$

Friction opposes the motion: $\;f = \mu N = 0.25(100) = 25\ \text{N}$.

Horizontally, the resultant force is $40 - 25 = 15$ N, so

$$ a = \frac{F_{\text{net}}}{m} = \frac{15}{10} = 1.5\ \text{m s}^{-2} $$
:::

```figure caption="Two masses joined by a light inextensible string over a smooth pulley, with a separate free-body diagram for each. The string tension $T$ is the same throughout; the heavier mass accelerates down and the lighter one up, with the same magnitude $a$."
import numpy as np
fig, ax = plt.subplots(figsize=(5.0,3.2))
ax.plot([-1.1, 1.1], [4.25, 4.25], color=INK, lw=1.6)
for x0 in np.arange(-1.0, 1.15, 0.24):
    ax.plot([x0, x0-0.13], [4.25, 4.40], color=MUTED, lw=0.8)
ax.plot([0, 0], [3.5, 4.25], color=INK, lw=1.2)
ax.add_patch(plt.Circle((0, 2.6), 0.9, facecolor='#eef1f5', edgecolor=INK, lw=1.5))
ax.plot([0], [2.6], 'o', color=INK, ms=3.5)
tt = np.linspace(0, np.pi, 90)
ax.plot(0.9*np.cos(tt), 2.6 + 0.9*np.sin(tt), color=INK, lw=1.5)
ax.plot([-0.9, -0.9], [2.6, 1.15], color=INK, lw=1.3)
ax.plot([0.9, 0.9], [2.6, 1.15], color=INK, lw=1.3)
ax.add_patch(plt.Rectangle((-1.35, 0.45), 0.9, 0.7, facecolor='#dfe3ea', edgecolor=INK, lw=1.3))
ax.add_patch(plt.Rectangle((0.45, 0.45), 0.9, 0.7, facecolor='#dfe3ea', edgecolor=INK, lw=1.3))
ax.text(-0.90, 0.68, '$m_2$', fontsize=10, ha='center', color=INK)
ax.text(0.90, 0.68, '$m_1$', fontsize=10, ha='center', color=INK)
ax.text(1.25, 2.95, 'smooth pulley', fontsize=8.8, color=MUTED)
def arr(a, b, c, lw=2.1):
    ax.annotate('', xy=b, xytext=a, arrowprops=dict(arrowstyle='-|>', color=c,
                lw=lw, mutation_scale=11, shrinkA=0, shrinkB=0), zorder=6)
for cx, mlab, adir in [(-0.9, '$m_2g$', 1), (0.9, '$m_1g$', -1)]:
    arr((cx, 0.80), (cx, 1.62), '#2e8b57')
    arr((cx, 0.80), (cx, -0.42), '#d9534f')
    ax.text(cx+0.14, 1.46, '$T$', fontsize=10.5, color='#2e8b57')
    ax.text(cx+0.10, -0.60, mlab, fontsize=10.5, color='#d9534f')
arr((-2.15, 0.45), (-2.15, 1.15), ACCENT)
arr((2.15, 1.15), (2.15, 0.45), ACCENT)
ax.text(-2.60, 0.68, '$a$', fontsize=10.5, color=ACCENT)
ax.text(2.26, 0.68, '$a$', fontsize=10.5, color=ACCENT)
ax.text(0.0, -1.30, 'lighter mass:  $T - m_2g = m_2a$', fontsize=9.0, ha='center', color=INK)
ax.text(0.0, -1.95, 'heavier mass:  $m_1g - T = m_1a$', fontsize=9.0, ha='center', color=INK)
ax.set_xlim(-3.3, 3.3); ax.set_ylim(-2.45, 4.55)
ax.set_aspect('equal'); ax.axis('off')
```

::: example Worked example 16.9
**Problem.** Masses of $5$ kg and $3$ kg hang from the ends of a light
inextensible string passing over a smooth fixed pulley. Find the acceleration of
the system and the tension in the string. ($g = 10\ \text{m s}^{-2}$.)

**Solution.** Let $a$ be the common acceleration and $T$ the tension. Take the
direction of motion as positive for each block.

For the $5$ kg mass (moving down): $\;5g - T = 5a$, i.e. $50 - T = 5a$.
For the $3$ kg mass (moving up): $\;T - 3g = 3a$, i.e. $T - 30 = 3a$.

**Add** the two equations; $T$ cancels:

$$ 50 - 30 = 8a \;\Longrightarrow\; a = \frac{20}{8} = 2.5\ \text{m s}^{-2} $$

Substitute back: $\;T = 30 + 3(2.5) = 37.5\ \text{N}$.

**Check** in the other equation: $50 - 37.5 = 12.5 = 5(2.5)$. Correct.

In general $a = \dfrac{(m_1-m_2)g}{m_1+m_2}$ and $T = \dfrac{2m_1m_2 g}{m_1+m_2}$.
:::

::: example Worked example 16.10
**Problem.** A person of mass $60$ kg stands in a lift. Find the reaction of the
floor on the person when the lift (a) accelerates upwards at
$2\ \text{m s}^{-2}$, (b) accelerates downwards at $2\ \text{m s}^{-2}$, (c) falls
freely. ($g = 10\ \text{m s}^{-2}$.)

**Solution.** Two forces act on the person: the weight $mg$ down and the floor
reaction $R$ up.

(a) Upward acceleration: $\;R - mg = ma$, so

$$ R = m(g+a) = 60(10+2) = 720\ \text{N} $$

(b) Downward acceleration: $\;mg - R = ma$, so

$$ R = m(g-a) = 60(10-2) = 480\ \text{N} $$

(c) Free fall means $a = g$, so $R = m(g-g) = 0$ — the person feels weightless.
:::

::: example Worked example 16.11
**Problem.** A ball of mass $0.15$ kg strikes a wall normally at
$20\ \text{m s}^{-1}$ and rebounds at $15\ \text{m s}^{-1}$. Find the impulse on
the ball, and the average force if the contact lasts $0.05$ s.

**Solution.** Take the direction towards the wall as positive, so the rebound
velocity is $-15\ \text{m s}^{-1}$.

$$ \text{Impulse} = mv - mu = 0.15(-15) - 0.15(20) = -2.25 - 3.00 = -5.25 $$

The impulse is $5.25\ \text{N s}$ directed **away from the wall**.

$$ F = \frac{\text{impulse}}{\Delta t} = \frac{5.25}{0.05} = 105\ \text{N} $$
:::

::: example Worked example 16.12
**Problem.** A trolley of mass $3$ kg moving at $4\ \text{m s}^{-1}$ collides with
a stationary trolley of mass $5$ kg and the two move off together. Find the common
velocity and the kinetic energy lost.

**Solution.** Conservation of momentum:

$$ 3(4) + 5(0) = (3+5)v \;\Longrightarrow\; 12 = 8v \;\Longrightarrow\;
v = 1.5\ \text{m s}^{-1} $$

Kinetic energy before $= \tfrac12(3)(4)^2 = 24\ \text{J}$.
Kinetic energy after $= \tfrac12(8)(1.5)^2 = 9\ \text{J}$.

$$ \text{Energy lost} = 24 - 9 = 15\ \text{J} $$

The collision is **inelastic**: momentum is conserved but $15$ J becomes heat and
sound.
:::

::: example Worked example 16.13
**Problem.** A stone is thrown vertically upwards from the ground with a speed of
$20\ \text{m s}^{-1}$. Find the greatest height, the time to reach it and the
total time in the air. ($g = 10\ \text{m s}^{-2}$.)

**Solution.** Taking upwards positive, $u = 20$ and $a = -10$.

At the highest point $v = 0$, so from $v^2 = u^2 + 2as$:

$$ 0 = 400 - 20s \;\Longrightarrow\; s = 20\ \text{m} $$

From $v = u + at$: $\;0 = 20 - 10t \Rightarrow t = 2\ \text{s}$.

By symmetry the fall takes the same time, so the total time in the air is
$4\ \text{s}$.
:::

::: caution One body at a time
In a pulley or lift question, write $F = ma$ **separately for each body**, with
its own set of forces, and never mix the two into one equation. And use the
*resultant* force on that body — for the $5$ kg mass above it is $5g - T$, not
$5g$.
:::

## 16.3 Dynamics: projectile motion

A **projectile** is a body given an initial velocity and then left to gravity
alone (air resistance ignored). The key idea is that the horizontal and vertical
motions are completely independent:

- horizontally there is no force, so the velocity $u\cos\theta$ is constant;
- vertically there is a constant acceleration $-g$.

::: derivation Trajectory, time of flight, greatest height and range
Project a body from the origin with speed $u$ at angle $\theta$ above the
horizontal. After time $t$,

$$ x = (u\cos\theta)\,t, \qquad y = (u\sin\theta)\,t - \tfrac12 g t^2 $$

**Trajectory.** From the first, $t = \dfrac{x}{u\cos\theta}$. Substituting,

$$ y = x\tan\theta - \frac{g x^2}{2u^2\cos^2\theta} $$

which is of the form $y = ax - bx^2$: a **parabola**.

**Time of flight.** The body lands when $y = 0$ and $t \ne 0$:

$$ t\left(u\sin\theta - \tfrac12 g t\right) = 0
\;\Longrightarrow\; T = \frac{2u\sin\theta}{g} $$

**Greatest height.** The vertical velocity $u\sin\theta - gt$ is zero at
$t = \dfrac{u\sin\theta}{g} = \dfrac{T}{2}$, and then

$$ H = u\sin\theta\cdot\frac{u\sin\theta}{g} - \frac{g}{2}\cdot\frac{u^2\sin^2\theta}{g^2}
= \frac{u^2\sin^2\theta}{2g} $$

**Horizontal range.** $R = (u\cos\theta)T = u\cos\theta\cdot\dfrac{2u\sin\theta}{g}$,
and $2\sin\theta\cos\theta = \sin 2\theta$, so

$$ R = \frac{u^2\sin 2\theta}{g} $$
:::

::: key Maximum range and complementary angles
$R = \dfrac{u^2\sin 2\theta}{g}$ is greatest when $\sin 2\theta = 1$, i.e.
$2\theta = 90^\circ$:

$$ \theta = 45^\circ, \qquad R_{\max} = \frac{u^2}{g} $$

Because $\sin(180^\circ - 2\theta) = \sin 2\theta$, the angles $\theta$ and
$90^\circ - \theta$ give the **same range** — so $30^\circ$ and $60^\circ$ carry a
ball equally far, though not equally high or for equally long.
:::

```figure caption="Trajectory for $u = 20\ \mathrm{m\,s^{-1}}$ at $\theta = 30^{\circ}$, $g = 10\ \mathrm{m\,s^{-2}}$: time of flight $T = 2$ s, greatest height $H = 5$ m, range $R = 34.6$ m. At the top the velocity is horizontal, of size $u\cos\theta = 17.3\ \mathrm{m\,s^{-1}}$."
import numpy as np
fig, ax = plt.subplots(figsize=(5.1,2.9))
u, g = 20.0, 10.0
th = np.radians(30.0)
T = 2*u*np.sin(th)/g; H = (u*np.sin(th))**2/(2*g); R = u*u*np.sin(2*th)/g
t = np.linspace(0, T, 300)
x = u*np.cos(th)*t; y = u*np.sin(th)*t - 0.5*g*t**2
ax.plot(x, y, color=ACCENT, lw=2.2, zorder=4)
ax.axhline(0, color=INK, lw=1.2)
ax.plot([R/2, R/2], [0, H], color=MUTED, lw=0.9, ls=(0,(3,2)))
ax.annotate('', xy=(R/2, H), xytext=(R/2, 0),
            arrowprops=dict(arrowstyle='<|-|>', color='#2e8b57', lw=1.2, mutation_scale=8))
ax.text(R/2+0.9, H/2-0.30, '$H = 5$ m', fontsize=9.2, color='#2e8b57')
ax.annotate('', xy=(0, -1.55), xytext=(R, -1.55),
            arrowprops=dict(arrowstyle='<|-|>', color='#d9534f', lw=1.2, mutation_scale=8))
ax.text(R/2, -2.35, '$R = 34.6$ m', fontsize=9.4, color='#d9534f', ha='center')
def arr(a, b, c, lw=1.9):
    ax.annotate('', xy=b, xytext=a, arrowprops=dict(arrowstyle='-|>', color=c,
                lw=lw, mutation_scale=11, shrinkA=0, shrinkB=0), zorder=6)
arr((0,0), (7.3, 4.2), '#b8860b', 2.2)
ax.text(5.6, 4.35, '$u = 20$', fontsize=9.6, color='#b8860b')
thd = np.linspace(0, th, 40)
ax.plot(4.2*np.cos(thd), 4.2*np.sin(thd), color=MUTED, lw=0.9)
ax.text(4.75, 0.55, r'$\theta = 30^{\circ}$', fontsize=9.4, color=MUTED)
arr((R/2, H), (R/2+6.2, H), '#6a5acd', 2.0)
ax.text(R/2+1.0, H+0.55, r'$u\cos\theta = 17.3$', fontsize=9.0, color='#6a5acd')
ax.plot([R/2], [H], 'o', color=INK, ms=4.5, zorder=7)
ax.plot([R], [0], 'o', color=INK, ms=4.5, zorder=7)
ax.text(R-9.6, 0.70, '$t = T = 2$ s', fontsize=9.0, color=INK)
ax.text(0.5, -1.1, '$t = 0$', fontsize=9.0, color=INK)
ax.set_xlim(-2.2, 41); ax.set_ylim(-3.6, 7.3)
ax.set_xlabel('horizontal distance (m)'); ax.set_ylabel('height (m)')
ax.spines[['top','right','left','bottom']].set_visible(False)
ax.set_yticks([0, 2, 4, 6]); ax.set_xticks([0, 10, 20, 30, 40])
ax.grid(True, alpha=.35)
```

```figure caption="Trajectories for $u = 20\ \mathrm{m\,s^{-1}}$, $g = 10\ \mathrm{m\,s^{-2}}$ at five angles. The $45^{\circ}$ path (thick) reaches farthest, $R_{\max} = u^2/g = 40$ m, and the complementary pairs $15^{\circ}/75^{\circ}$ and $30^{\circ}/60^{\circ}$ land at the same spot."
import numpy as np
fig, ax = plt.subplots(figsize=(5.1,2.9))
u, g = 20.0, 10.0
for i, a in enumerate([15, 30, 45, 60, 75]):
    th = np.radians(a)
    T = 2*u*np.sin(th)/g
    t = np.linspace(0, T, 250)
    x = u*np.cos(th)*t; y = u*np.sin(th)*t - 0.5*g*t**2
    thick = (a == 45)
    ax.plot(x, y, color=SERIES[i % 6], lw=2.6 if thick else 1.5,
            label=f'${a}' + r'^{\circ}$')
    ax.plot([x[-1]], [0], 'o', color=SERIES[i % 6], ms=4.2)
ax.axhline(0, color=INK, lw=1.1)
ax.annotate('', xy=(40, -1.3), xytext=(0, -1.3),
            arrowprops=dict(arrowstyle='<|-|>', color=INK, lw=1.1, mutation_scale=8))
ax.text(20, -2.8, r'$R_{\max} = u^2/g = 40$ m', fontsize=9.2, color=INK, ha='center')
ax.text(43.0, 19.4, r'$15^{\circ}$ and $75^{\circ}$ both land at $20$ m',
        fontsize=8.6, color=MUTED, ha='right')
ax.text(43.0, 17.4, r'$30^{\circ}$ and $60^{\circ}$ both land at $34.6$ m',
        fontsize=8.6, color=MUTED, ha='right')
ax.set_xlim(-1.5, 44); ax.set_ylim(-4.2, 21.5)
ax.set_xlabel('horizontal distance (m)'); ax.set_ylabel('height (m)')
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.35); ax.legend(loc='upper left', ncol=1, handlelength=1.3)
```

::: example Worked example 16.14
**Problem.** A ball is projected with a speed of $20\ \text{m s}^{-1}$ at
$30^\circ$ to the horizontal. Find (a) the time of flight, (b) the greatest
height, (c) the horizontal range, and (d) the speed of the ball $1$ s after
projection. ($g = 10\ \text{m s}^{-2}$.)

**Solution.** $u\cos\theta = 20\cos 30^\circ = 17.32\ \text{m s}^{-1}$ and
$u\sin\theta = 20\sin 30^\circ = 10\ \text{m s}^{-1}$.

(a) $\;T = \dfrac{2u\sin\theta}{g} = \dfrac{2(10)}{10} = 2\ \text{s}$

(b) $\;H = \dfrac{u^2\sin^2\theta}{2g} = \dfrac{(10)^2}{2(10)} = 5\ \text{m}$

(c) $\;R = \dfrac{u^2\sin 2\theta}{g} = \dfrac{400\sin 60^\circ}{10}
= 40(0.8660) = 34.6\ \text{m}$

(d) At $t = 1$ s the horizontal component is still $17.32\ \text{m s}^{-1}$ and
the vertical component is $10 - 10(1) = 0$. The ball is at the top of its path,
so its speed is $17.3\ \text{m s}^{-1}$, horizontal.
:::

::: example Worked example 16.15
**Problem.** A stone is thrown **horizontally** at $20\ \text{m s}^{-1}$ from the
top of a cliff $45$ m high. Find the time to reach the ground, the horizontal
distance travelled, and the speed with which it strikes the ground.
($g = 10\ \text{m s}^{-2}$.)

**Solution.** Take downwards positive for the vertical motion; the initial
vertical velocity is zero.

$$ 45 = 0 + \tfrac12(10)t^2 \;\Longrightarrow\; t^2 = 9 \;\Longrightarrow\;
t = 3\ \text{s} $$

Horizontal distance $= 20(3) = 60\ \text{m}$.

At landing the horizontal velocity is still $20\ \text{m s}^{-1}$ and the
vertical one is $v_y = 0 + 10(3) = 30\ \text{m s}^{-1}$, so

$$ v = \sqrt{20^2 + 30^2} = \sqrt{400+900} = \sqrt{1300} = 36.1\ \text{m s}^{-1} $$

at an angle $\tan^{-1}\left(\dfrac{30}{20}\right) = 56.3^\circ$ below the
horizontal.
:::

::: example Worked example 16.16
**Problem.** A ball is projected with speed $20\ \text{m s}^{-1}$. Find the two
angles of projection that give a horizontal range of $20$ m, and the maximum range
possible with this speed. ($g = 10\ \text{m s}^{-2}$.)

**Solution.** $\;R = \dfrac{u^2\sin 2\theta}{g}$, so

$$ 20 = \frac{400\sin 2\theta}{10} = 40\sin 2\theta
\;\Longrightarrow\; \sin 2\theta = \frac12 $$

$$ 2\theta = 30^\circ \text{ or } 150^\circ \;\Longrightarrow\;
\theta = 15^\circ \text{ or } 75^\circ $$

The two angles are complementary, as expected. The maximum range is at
$45^\circ$:

$$ R_{\max} = \frac{u^2}{g} = \frac{400}{10} = 40\ \text{m} $$
:::

::: caution Do not use $s = ut + \frac12at^2$ across both directions at once
Horizontal and vertical motions are separate problems that share only the time
$t$. Horizontally $a = 0$, so $x = (u\cos\theta)t$ — never
$x = (u\cos\theta)t + \frac12 gt^2$. Solve the vertical equation for $t$ first,
then feed that $t$ into the horizontal one.
:::

## Chapter summary

- Resultant of $P$ and $Q$ at angle $\theta$:
  $R = \sqrt{P^2+Q^2+2PQ\cos\theta}$, at $\tan\alpha = \dfrac{Q\sin\theta}{P+Q\cos\theta}$
  to $P$. Resolution: components $F\cos\theta$, $F\sin\theta$.
- **Triangle law.** Three concurrent forces are in equilibrium exactly when they
  form a closed head-to-tail triangle; with more forces, a closed polygon.
- **Lami's theorem.** For three concurrent forces in equilibrium,
  $\dfrac{P}{\sin\alpha} = \dfrac{Q}{\sin\beta} = \dfrac{R}{\sin\gamma}$, each
  angle being between the *other* two forces.
- **Moment** $M = F\times d$; a rigid body is in equilibrium when
  $\sum F_x = 0$, $\sum F_y = 0$ and $\sum M = 0$.
- **Newton's laws.** $F = ma$; impulse $F\Delta t = mv - mu$; momentum
  $m_1u_1 + m_2u_2 = m_1v_1 + m_2v_2$ is conserved in every collision.
- Atwood machine: $a = \dfrac{(m_1-m_2)g}{m_1+m_2}$,
  $T = \dfrac{2m_1m_2g}{m_1+m_2}$. Lift: $R = m(g \pm a)$.
- Work $W = Fs\cos\theta$; work–energy theorem
  $W = \tfrac12 mv^2 - \tfrac12 mu^2$; power $P = Fv$.
- **Projectile** ($u$, $\theta$): $y = x\tan\theta - \dfrac{gx^2}{2u^2\cos^2\theta}$,
  $T = \dfrac{2u\sin\theta}{g}$, $H = \dfrac{u^2\sin^2\theta}{2g}$,
  $R = \dfrac{u^2\sin2\theta}{g}$, with $R_{\max} = \dfrac{u^2}{g}$ at
  $\theta = 45^\circ$ and equal ranges for $\theta$ and $90^\circ-\theta$.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The resultant of two equal forces $P$ acting at $120^\circ$ to each other is <span class="marks">[1]</span>
   (a) $2P$ (b) $P\sqrt{3}$ (c) $P$ (d) $0$
2. Three concurrent forces in equilibrium, drawn head to tail, form <span class="marks">[1]</span>
   (a) a straight line (b) a closed triangle (c) a right angle (d) a circle
3. In Lami's theorem, the force $P$ is divided by the sine of the angle <span class="marks">[1]</span>
   (a) between $P$ and $Q$ (b) between $P$ and $R$ (c) between $Q$ and $R$ (d) of $90^\circ$
4. The SI unit of impulse is the same as that of <span class="marks">[1]</span>
   (a) force (b) energy (c) momentum (d) power
5. A projectile has maximum horizontal range when the angle of projection is <span class="marks">[1]</span>
   (a) $30^\circ$ (b) $45^\circ$ (c) $60^\circ$ (d) $90^\circ$
6. At the highest point of its path a projectile's velocity is <span class="marks">[1]</span>
   (a) zero (b) vertical (c) horizontal, $u\cos\theta$ (d) equal to $u$
7. The reaction of the floor on a person of mass $m$ in a lift falling freely is <span class="marks">[1]</span>
   (a) $mg$ (b) $2mg$ (c) $mg/2$ (d) zero

::: note Answers to Group A
**1.** (c) — $R = \sqrt{P^2+P^2+2P^2\cos 120^\circ} = \sqrt{2P^2 - P^2} = P$.

**2.** (b) — that is exactly the triangle law of forces.

**3.** (c) — each force pairs with the angle between the *other* two.

**4.** (c) — impulse $= F\Delta t = mv - mu$, a change of momentum (N s $=$ kg m s$^{-1}$).

**5.** (b) — $R = u^2\sin2\theta/g$ is greatest when $\sin2\theta = 1$.

**6.** (c) — the vertical component is momentarily zero, the horizontal one never changes.

**7.** (d) — free fall means $a = g$, so $R = m(g-g) = 0$.
:::

**Group B — Short answer (5 marks each)**

1. Two forces of $7$ N and $8$ N act at a point with an angle of $60^\circ$
   between them. Find the magnitude of the resultant and the angle it makes with
   the $7$ N force. <span class="marks">[5]</span>
2. State Lami's theorem. A body of weight $100$ N hangs at a point $O$ from two
   strings making angles of $30^\circ$ and $60^\circ$ with the **vertical**, on
   opposite sides. Find the tension in each string. <span class="marks">[5]</span>
3. A uniform rod $AB$ of length $6$ m and weight $120$ N rests horizontally on
   supports at $A$ and $B$. A weight of $180$ N hangs from a point $2$ m from
   $A$. Find the reactions at the supports. <span class="marks">[5]</span>
4. A body of mass $5$ kg is pulled along a rough horizontal floor by a horizontal
   force of $30$ N against a frictional force of $10$ N. Find the acceleration and
   the distance travelled in $4$ s starting from rest. <span class="marks">[5]</span>
5. A bullet of mass $20$ g is fired with a speed of $400\ \text{m s}^{-1}$ from a
   gun of mass $4$ kg. Find the recoil speed of the gun and the kinetic energy of
   the bullet. <span class="marks">[5]</span>
6. A ball is projected with a speed of $40\ \text{m s}^{-1}$ at $30^\circ$ to the
   horizontal. Find the time of flight, the greatest height and the horizontal
   range. ($g = 10\ \text{m s}^{-2}$.) <span class="marks">[5]</span>

::: note Answers to Group B
**1.** $R = \sqrt{7^2 + 8^2 + 2(7)(8)\cos 60^\circ} = \sqrt{49+64+56}
= \sqrt{169} = 13\ \text{N}$.

$$ \tan\alpha = \frac{8\sin 60^\circ}{7 + 8\cos 60^\circ} = \frac{6.928}{11}
= 0.6299 \;\Longrightarrow\; \alpha = 32.2^\circ $$

So the resultant is $13$ N at $32.2^\circ$ to the $7$ N force.

**2.** *Lami's theorem.* If three coplanar forces acting at a point are in
equilibrium, each force is proportional to the sine of the angle between the
other two:
$\dfrac{P}{\sin\alpha} = \dfrac{Q}{\sin\beta} = \dfrac{R}{\sin\gamma}$.

Here $T_1$ makes $30^\circ$ with the upward vertical and $T_2$ makes $60^\circ$ on
the other side, so the angle between $T_1$ and $T_2$ is $90^\circ$; the angle
between $T_1$ and $W$ (downward) is $180^\circ - 30^\circ = 150^\circ$, and
between $T_2$ and $W$ it is $180^\circ - 60^\circ = 120^\circ$.

$$ \frac{T_1}{\sin 120^\circ} = \frac{T_2}{\sin 150^\circ} = \frac{100}{\sin 90^\circ} $$

$$ T_1 = 100\sin 120^\circ = 86.6\ \text{N}, \qquad
T_2 = 100\sin 150^\circ = 50\ \text{N} $$

Check: horizontally $86.6\sin 30^\circ = 43.3 = 50\sin 60^\circ$; vertically
$86.6\cos 30^\circ + 50\cos 60^\circ = 75 + 25 = 100$. Correct.

**3.** The weight of the uniform rod acts at its midpoint, $3$ m from $A$. Taking
moments about $A$:

$$ R_B(6) = 120(3) + 180(2) = 360 + 360 = 720 \;\Longrightarrow\; R_B = 120\ \text{N} $$

Resolving vertically: $R_A + R_B = 120 + 180 = 300$, so $R_A = 180\ \text{N}$.

Check about $B$: $180(6) - 120(3) - 180(4) = 1080 - 360 - 720 = 0$. Correct.

**4.** Resultant force $= 30 - 10 = 20\ \text{N}$, so

$$ a = \frac{20}{5} = 4\ \text{m s}^{-2} $$

$$ s = ut + \tfrac12at^2 = 0 + \tfrac12(4)(4)^2 = 32\ \text{m} $$

**5.** Momentum before firing is zero, so by conservation (taking the bullet's
direction positive), with $m_b = 0.02$ kg:

$$ 0 = 0.02(400) + 4v \;\Longrightarrow\; 4v = -8 \;\Longrightarrow\;
v = -2\ \text{m s}^{-1} $$

The gun recoils at $2\ \text{m s}^{-1}$ in the opposite direction.

$$ \text{K.E. of bullet} = \tfrac12(0.02)(400)^2 = 1600\ \text{J} $$

**6.** $u\sin\theta = 40\sin 30^\circ = 20\ \text{m s}^{-1}$.

$$ T = \frac{2u\sin\theta}{g} = \frac{40}{10} = 4\ \text{s} $$
$$ H = \frac{u^2\sin^2\theta}{2g} = \frac{400}{20} = 20\ \text{m} $$
$$ R = \frac{u^2\sin 2\theta}{g} = \frac{1600\sin 60^\circ}{10}
= 160(0.8660) = 138.6\ \text{m} $$
:::

**Group C — Long answer (8 marks each)**

1. (a) State the triangle law of forces and use it, with the sine law, to prove
   Lami's theorem. <span class="marks">[4]</span>
   (b) A weight of $60$ N is supported by two strings attached to a point, one
   horizontal and the other making $30^\circ$ with the vertical. Find the tension
   in each string. <span class="marks">[4]</span>
2. (a) State Newton's three laws of motion and deduce $F = ma$ from the second
   law. <span class="marks">[3]</span>
   (b) Masses of $12$ kg and $8$ kg hang from the ends of a light string passing
   over a smooth pulley. Find the acceleration, the tension, and the distance
   fallen by the heavier mass in $2$ s from rest.
   ($g = 10\ \text{m s}^{-2}$.) <span class="marks">[5]</span>
3. (a) Derive expressions for the time of flight, the greatest height and the
   horizontal range of a projectile fired with speed $u$ at an angle $\theta$, and
   hence show that the range is greatest when $\theta = 45^\circ$. <span class="marks">[5]</span>
   (b) A ball is projected at $30\ \text{m s}^{-1}$. Find the two angles of
   projection giving a range of $45$ m, and the greatest height in each case.
   ($g = 10\ \text{m s}^{-2}$.) <span class="marks">[3]</span>

::: note Answers to Group C
**1.** (a) *Triangle law.* If three forces acting at a point are represented in
magnitude and direction by the three sides of a triangle taken in order, they are
in equilibrium.

*Proof of Lami's theorem.* Let $P$, $Q$, $R$ be in equilibrium at $O$, with
$\alpha$ the angle between $Q$ and $R$, $\beta$ between $R$ and $P$, $\gamma$
between $P$ and $Q$. Draw the forces head to tail: by the converse of the triangle
law they close into a triangle $ABC$ whose sides $AB$, $BC$, $CA$ represent
$P$, $Q$, $R$.

Each side is parallel to its force, so the interior angle of the triangle opposite
the side representing $P$ equals $180^\circ - \alpha$, and similarly for the
others. By the sine law, each side is proportional to the sine of the opposite
angle:

$$ \frac{P}{\sin(180^\circ - \alpha)} = \frac{Q}{\sin(180^\circ - \beta)}
= \frac{R}{\sin(180^\circ - \gamma)} $$

Since $\sin(180^\circ - x) = \sin x$,

$$ \frac{P}{\sin\alpha} = \frac{Q}{\sin\beta} = \frac{R}{\sin\gamma} $$

(b) Let $T_1$ be the horizontal tension and $T_2$ the tension in the string at
$30^\circ$ to the vertical. Resolving:

horizontally $\;T_2\sin 30^\circ = T_1$; vertically $\;T_2\cos 30^\circ = 60$.

$$ T_2 = \frac{60}{\cos 30^\circ} = \frac{60}{0.8660} = 69.3\ \text{N} $$
$$ T_1 = T_2\sin 30^\circ = 69.3(0.5) = 34.6\ \text{N} $$

(By Lami's theorem the same numbers come from
$\frac{T_1}{\sin 150^\circ} = \frac{T_2}{\sin 90^\circ} = \frac{60}{\sin 120^\circ}$.)

**2.** (a) *First law:* a body continues at rest or in uniform motion in a
straight line unless acted on by an external force. *Second law:* the rate of
change of momentum is proportional to the applied force and is in its direction.
*Third law:* action and reaction are equal in magnitude and opposite in direction,
and act on different bodies.

From the second law, with $p = mv$,

$$ F \propto \frac{d(mv)}{dt} = m\frac{dv}{dt} = ma $$

for constant mass. Choosing the newton so that the constant of proportionality is
$1$ gives $F = ma$.

(b) For the $12$ kg mass moving down and the $8$ kg mass moving up:

$$ 12g - T = 12a \quad (1), \qquad T - 8g = 8a \quad (2) $$

Adding, $\;4g = 20a$, so

$$ a = \frac{4(10)}{20} = 2\ \text{m s}^{-2} $$

From (2), $\;T = 8(10) + 8(2) = 96\ \text{N}$.
(Check in (1): $120 - 96 = 24 = 12(2)$.)

$$ s = \tfrac12 at^2 = \tfrac12(2)(2)^2 = 4\ \text{m} $$

**3.** (a) With the origin at the point of projection,
$x = (u\cos\theta)t$ and $y = (u\sin\theta)t - \frac12gt^2$.

*Time of flight:* set $y = 0$; then $t\left(u\sin\theta - \frac12gt\right) = 0$,
and the non-zero root is

$$ T = \frac{2u\sin\theta}{g} $$

*Greatest height:* the vertical velocity $u\sin\theta - gt$ vanishes at
$t = u\sin\theta/g$, and substituting gives

$$ H = \frac{u^2\sin^2\theta}{g} - \frac{u^2\sin^2\theta}{2g}
= \frac{u^2\sin^2\theta}{2g} $$

*Range:* $R = (u\cos\theta)T = \dfrac{2u^2\sin\theta\cos\theta}{g}
= \dfrac{u^2\sin 2\theta}{g}$.

Since $u$ and $g$ are fixed, $R$ is greatest when $\sin2\theta$ is greatest, i.e.
$\sin 2\theta = 1$, giving $2\theta = 90^\circ$, $\theta = 45^\circ$ and
$R_{\max} = u^2/g$.

(b) $\;45 = \dfrac{900\sin 2\theta}{10} = 90\sin 2\theta$, so
$\sin 2\theta = \tfrac12$ and $2\theta = 30^\circ$ or $150^\circ$:

$$ \theta = 15^\circ \quad\text{or}\quad \theta = 75^\circ $$

Greatest heights, from $H = \dfrac{u^2\sin^2\theta}{2g} = 45\sin^2\theta$:

$$ \theta = 15^\circ: \; H = 45(0.2588)^2 = 3.01\ \text{m}; \qquad
\theta = 75^\circ: \; H = 45(0.9659)^2 = 41.99\ \text{m} $$

The ranges are equal but the high trajectory rises about fourteen times higher.
:::
