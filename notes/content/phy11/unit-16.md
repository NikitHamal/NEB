---
subject: Physics
grade: 11
unit: 16
title: Refraction through prisms
hours: 3
area: Waves and Optics
---

A prism is a block of glass with two plane faces inclined to each other. Because
the two faces are *not* parallel, the two refractions no longer cancel as they did
in a slab: the ray leaves in a new direction, bent towards the thick part of the
glass. That bending is the **angle of deviation**, and it turns out to be smallest
when the light passes through the prism symmetrically. Measuring that smallest
deviation is the standard laboratory method of finding the refractive index of a
transparent solid, and it is the basis of the spectrometer.

::: key The four-formula unit
$A = r_1 + r_2$, $\delta = i_1 + i_2 - A$,
$n = \dfrac{\sin\left(\frac{A+\delta_m}{2}\right)}{\sin\left(\frac{A}{2}\right)}$
and $\delta = (n-1)A$ for a thin prism. Learn the derivations, not just the
results — NEB awards marks for each labelled step.
:::

## 16.1 Minimum deviation condition

The two faces through which light passes are the **refracting surfaces**; the
angle between them is the **refracting angle** or **angle of the prism**, $A$.
Their line of intersection is the **refracting edge** and the third face is the
**base**. A section perpendicular to the refracting edge is the **principal
section** — every diagram in this chapter is a principal section.

| Symbol | Name | Where it is measured |
|---|---|---|
| $A$ | refracting angle (angle of the prism) | between the two refracting faces |
| $i_1$ | angle of incidence | first face, in air |
| $r_1$ | angle of refraction | first face, in glass |
| $r_2$ | angle of incidence inside | second face, in glass |
| $i_2$ | angle of emergence | second face, in air |
| $\delta$ | angle of deviation | between incident and emergent directions |

::: definition Angle of deviation
The **angle of deviation** of a prism is the angle between the direction of the
incident ray produced forward and the direction of the emergent ray produced
backward. It measures how far the prism has turned the light from its original
path.
:::

```figure caption="Refraction through a prism of refracting angle $A$. The ray is refracted at $Q$ and again at $S$, and leaves deviated through the angle $\delta$ from its original direction."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Arc, Polygon
fig, ax = plt.subplots(figsize=(5.0, 3.4))
Adeg, n, i1 = 60.0, 1.5, 60.0
H = 2.8
w = H*np.tan(np.radians(Adeg/2))
apex = np.array([0.0, H]); Lv = np.array([-w, 0.0]); Rv = np.array([w, 0.0])
ax.add_patch(Polygon([apex, Lv, Rv], closed=True, fc=ACCENT, alpha=0.11,
                     ec=INK, lw=1.8))
r1 = np.degrees(np.arcsin(np.sin(np.radians(i1))/n))
r2 = Adeg - r1
i2 = np.degrees(np.arcsin(n*np.sin(np.radians(r2))))
th_in = np.radians(-Adeg/2 + i1)
th_1 = np.radians(-Adeg/2 + r1)
th_out = np.radians(Adeg/2 - i2)
u = lambda a: np.array([np.cos(a), np.sin(a)])
Q = apex + 0.55*(Lv - apex)
M = np.array([[np.cos(th_1), -(Rv - apex)[0]], [np.sin(th_1), -(Rv - apex)[1]]])
tt, uu = np.linalg.solve(M, apex - Q)
S = Q + tt*u(th_1)
Mx = np.array([[np.cos(th_in), -np.cos(th_out)], [np.sin(th_in), -np.sin(th_out)]])
a1, a2 = np.linalg.solve(Mx, S - Q)
X = Q + a1*u(th_in)

def arrow(p, q, c, lw=1.6):
    ax.annotate('', xy=tuple(q), xytext=tuple(p),
                arrowprops=dict(arrowstyle='-|>', color=c, lw=lw,
                                mutation_scale=12, shrinkA=0, shrinkB=0))

arrow(Q - 1.9*u(th_in), Q, SERIES[0])
arrow(Q, S, SERIES[0])
arrow(S, S + 1.9*u(th_out), SERIES[0])
ax.plot([Q[0], X[0] + 0.75*np.cos(th_in)], [Q[1], X[1] + 0.75*np.sin(th_in)],
        color=MUTED, lw=0.9, ls=(0, (3, 2)))
ax.plot([S[0], X[0] - 0.75*np.cos(th_out)], [S[1], X[1] - 0.75*np.sin(th_out)],
        color=MUTED, lw=0.9, ls=(0, (3, 2)))
ax.add_patch(Arc(tuple(X), 1.7, 1.7, theta1=np.degrees(th_out),
                 theta2=np.degrees(th_in), color='#A8271F', lw=1.1))
am = (th_in + th_out)/2
ax.text(X[0] + 1.12*np.cos(am), X[1] + 1.12*np.sin(am), r'$\delta$',
        color='#A8271F', fontsize=12, ha='center', va='center')

nl = np.array([-np.cos(np.radians(Adeg/2)), np.sin(np.radians(Adeg/2))])
nr = np.array([np.cos(np.radians(Adeg/2)), np.sin(np.radians(Adeg/2))])
for P, nn in [(Q, nl), (S, nr)]:
    ax.plot([P[0] - 0.95*nn[0], P[0] + 0.95*nn[0]],
            [P[1] - 0.95*nn[1], P[1] + 0.95*nn[1]],
            color=MUTED, lw=0.9, ls=(0, (2, 2)))
angl = np.degrees(np.arctan2(nl[1], nl[0]))
angr = np.degrees(np.arctan2(nr[1], nr[0]))


def mark(P, a0, a1_, dia, rad, lab, col, fs=10.5):
    ax.add_patch(Arc(tuple(P), dia, dia, theta1=a0, theta2=a1_, color=col, lw=1.0))
    am_ = np.radians((a0 + a1_)/2)
    ax.text(P[0] + rad*np.cos(am_), P[1] + rad*np.sin(am_), lab,
            color=col, fontsize=fs, ha='center', va='center')

mark(Q, angl, angl + i1, 1.0, 0.70, '$i_1$', SERIES[1])
mark(Q, angl + 180, angl + 180 + r1, 0.62, 0.60, '$r_1$', SERIES[2], 9.0)
mark(S, angr + 180 - r2, angr + 180, 0.62, 0.74, '$r_2$', SERIES[2], 9.0)
mark(S, angr - i2, angr, 1.30, 0.86, '$i_2$', SERIES[1])
ax.add_patch(Arc(tuple(apex), 0.9, 0.9, theta1=270 - Adeg/2, theta2=270 + Adeg/2,
                 color=INK, lw=1.0))
ax.text(apex[0], apex[1] - 0.68, '$A$', color=INK, fontsize=11, ha='center')
ax.annotate('Q', tuple(Q), textcoords='offset points', xytext=(-18, 18),
            color=INK, fontsize=10)
ax.annotate('S', tuple(S), textcoords='offset points', xytext=(9, -12),
            color=INK, fontsize=10)
ax.set_xlim(-3.1, 3.6); ax.set_ylim(-0.4, 3.2)
ax.set_aspect('equal'); ax.axis('off')
```

::: derivation The two prism relations, $A = r_1 + r_2$ and $\delta = i_1 + i_2 - A$
We start from pure geometry in the ray diagram — no optics at all in part (a) — and reach the
two equations that every prism question is built on.

**Setting up.** The ray strikes the first face at $Q$ with angle of incidence $i_1$ and is
refracted at $r_1$. Inside the glass it travels to $S$ on the second face, meets the normal
there at $r_2$, and emerges at $i_2$. Let $N$ be the point where the two normals (at $Q$ and at
$S$) cross. $A$ is the refracting angle of the prism, at the vertex where the two faces meet.

**Part (a): $A = r_1 + r_2$**

**Step 1 — look at the quadrilateral $AQNS$.** $NQ$ is the normal at $Q$, so it is
perpendicular to the first face; $NS$ is the normal at $S$, so it is perpendicular to the
second face. Therefore

$$ \angle AQN = 90^{\circ}, \qquad \angle ASN = 90^{\circ} $$

**Step 2 — add up the four angles of the quadrilateral.** They total $360^{\circ}$:

$$ A + 90^{\circ} + \angle QNS + 90^{\circ} = 360^{\circ} $$

**Step 3 — subtract $180^{\circ}$ from both sides:**

$$ A + \angle QNS = 180^{\circ} $$

**Step 4 — now look at triangle $QNS$.** Its three angles are $r_1$ at $Q$, $r_2$ at $S$, and
$\angle QNS$ at $N$, and they add to $180^{\circ}$:

$$ r_1 + r_2 + \angle QNS = 180^{\circ} $$

**Step 5 — compare Steps 3 and 4.** Both left-hand sides equal $180^{\circ}$:

$$ A + \angle QNS = r_1 + r_2 + \angle QNS $$

**Step 6 — cancel $\angle QNS$ from both sides:**

$$ A = r_1 + r_2 $$

---

**Part (b): $\delta = i_1 + i_2 - A$**

**Step 7 — how much the ray turns at the first face.** It arrives along a direction making
$i_1$ with the normal and leaves making $r_1$ with the same normal, so it has been turned
through

$$ \delta_1 = i_1 - r_1 $$

**Step 8 — how much it turns at the second face.** Same argument, in the same rotational
sense:

$$ \delta_2 = i_2 - r_2 $$

**Step 9 — add the two turns.** Both bend the ray the same way, so the total deviation $\delta$
(the exterior angle of the triangle formed by the incident ray produced and the emergent ray
produced backwards) is their sum:

$$ \delta = (i_1 - r_1) + (i_2 - r_2) $$

**Step 10 — group the $i$'s and the $r$'s:**

$$ \delta = (i_1 + i_2) - (r_1 + r_2) $$

**Step 11 — replace $(r_1 + r_2)$ by $A$,** using Part (a):

$$ \delta = i_1 + i_2 - A $$

**Result.**

$$ A = r_1 + r_2, \qquad \delta = i_1 + i_2 - A $$

**What it means.** The first relation is purely geometrical — it holds whatever the glass is
made of. The second says the prism's total bending is shared between the two faces. Together
they reduce four unknown angles to two, which is why every prism numerical is solvable.

**Conditions used.** The ray must lie in a plane perpendicular to the refracting edge (the
"principal section"), and it must actually emerge at the second face — if $r_2$ exceeds the
critical angle, there is no $i_2$ and these relations cannot be used.
:::

### How the deviation varies with the angle of incidence

Keep the prism and the colour of light fixed and slowly increase $i_1$. Each value
of $i_1$ fixes $r_1$, hence $r_2 = A - r_1$, hence $i_2$, hence $\delta$. Plotting
$\delta$ against $i_1$ gives a curve with a single minimum.

```figure caption="Deviation against angle of incidence for an equilateral prism with $n = 1.5$. Any deviation above the minimum is produced by two different angles of incidence; at the minimum the two coincide."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8, 3.0))
A, n = 60.0, 1.5
C = np.degrees(np.arcsin(1/n))
r1 = np.linspace(A - C + 1e-6, C - 1e-6, 500)
i1 = np.degrees(np.arcsin(n*np.sin(np.radians(r1))))
i2 = np.degrees(np.arcsin(n*np.sin(np.radians(A - r1))))
dev = i1 + i2 - A
ax.plot(i1, dev, color=ACCENT, lw=2.0, zorder=3)
k = int(np.argmin(dev))
im, dm = i1[k], dev[k]
ax.plot([im], [dm], 'o', color='#A8271F', ms=5.5, zorder=5)
ax.vlines(im, 34, dm, color=MUTED, lw=0.9, ls=':')
ax.hlines(dm, 25, im, color=MUTED, lw=0.9, ls=':')
lev = 45.0
left = np.interp(lev, dev[:k][::-1], i1[:k][::-1])
right = np.interp(lev, dev[k:], i1[k:])
ax.hlines(lev, left, right, color=SERIES[1], lw=1.0, ls=(0, (4, 2)))
for xv in (left, right):
    ax.vlines(xv, 34, lev, color=SERIES[1], lw=0.8, ls=(0, (2, 2)))
ax.annotate(r'$\delta_m = 37.2^\circ$', (im, dm), textcoords='offset points',
            xytext=(12, -14), color='#A8271F', fontsize=9.5)
ax.annotate(r'$i_1 = i_2$ here', (im, dm), textcoords='offset points',
            xytext=(-6, 26), color='#A8271F', fontsize=9.5, ha='center',
            arrowprops=dict(arrowstyle='-|>', color='#A8271F', lw=1.0, mutation_scale=9))
ax.set_xlabel('angle of incidence  $i_1$  (degrees)')
ax.set_ylabel(r'deviation  $\delta$  (degrees)')
ax.set_xlim(25, 92); ax.set_ylim(34, 60)
ax.spines[['top', 'right']].set_visible(False)
ax.grid(True, alpha=.45)
```

::: derivation At minimum deviation the ray passes symmetrically
We start from the shape of the $\delta$–$i_1$ graph together with the principle of
reversibility, and reach the symmetry condition $i_1 = i_2$, $r_1 = r_2$.

**Step 1 — read the graph.** Draw any horizontal line above the lowest point of the curve. It
cuts the curve **twice**. So for every deviation $\delta$ *greater* than the minimum there are
**two** different angles of incidence that produce the very same deviation. Call them $i$ and
$i'$.

**Step 2 — apply the principle of reversibility.** If a ray enters at $i_1$ and emerges at
$i_2$, then reversing its direction sends a ray in at $i_2$ which emerges at $i_1$ — along the
same path, so with the same deviation $\delta$.

**Step 3 — identify the two roots.** Step 2 gives us two angles of incidence with the same
$\delta$, namely $i_1$ and $i_2$. Step 1 says there are only two. So the pair in Step 1 must be

$$ i = i_1, \qquad i' = i_2 $$

**Step 4 — now slide the horizontal line down.** As $\delta$ decreases towards $\delta_m$, the
two intersection points move towards each other. At the minimum itself the line touches the
curve at exactly **one** point, so the two roots have merged:

$$ i_1 = i_2 $$

**Step 5 — carry this inside the prism.** Snell's law at each face gives
$\sin i_1 = n\sin r_1$ and $\sin i_2 = n\sin r_2$. Equal $i$'s therefore force equal $r$'s:

$$ r_1 = r_2 $$

**Result.** At minimum deviation the ray passes symmetrically, $i_1 = i_2$ and $r_1 = r_2$, and
therefore the refracted ray inside the prism runs **parallel to the base**.

**What it means.** Symmetry is not an extra assumption we make for convenience — it is forced on
us by the shape of the curve. This is why the prism formula of the next section is exact, not
approximate.

**Conditions used.** One prism, one colour, and a ray that actually emerges from the second
face.
:::

::: key The minimum deviation condition
Deviation is a minimum when the ray passes through the prism **symmetrically**:

$$ i_1 = i_2 = i, \qquad r_1 = r_2 = r = \frac{A}{2} $$

and the refracted ray inside the prism is then **parallel to the base** of the
prism.
:::

```figure caption="At minimum deviation the path is symmetrical about the bisector of the refracting angle, and the internal ray runs parallel to the base."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Arc, Polygon
fig, ax = plt.subplots(figsize=(5.0, 3.2))
Adeg, n = 60.0, 1.5
H = 2.8
w = H*np.tan(np.radians(Adeg/2))
apex = np.array([0.0, H]); Lv = np.array([-w, 0.0]); Rv = np.array([w, 0.0])
ax.add_patch(Polygon([apex, Lv, Rv], closed=True, fc=ACCENT, alpha=0.11,
                     ec=INK, lw=1.8))
r = Adeg/2
i1 = np.degrees(np.arcsin(n*np.sin(np.radians(r))))
th_in = np.radians(-Adeg/2 + i1)
th_out = np.radians(Adeg/2 - i1)
u = lambda a: np.array([np.cos(a), np.sin(a)])
Q = apex + 0.5*(Lv - apex)
S = np.array([-Q[0], Q[1]])
Mx = np.array([[np.cos(th_in), -np.cos(th_out)], [np.sin(th_in), -np.sin(th_out)]])
a1, a2 = np.linalg.solve(Mx, S - Q)
X = Q + a1*u(th_in)

def arrow(p, q, c, lw=1.6):
    ax.annotate('', xy=tuple(q), xytext=tuple(p),
                arrowprops=dict(arrowstyle='-|>', color=c, lw=lw,
                                mutation_scale=12, shrinkA=0, shrinkB=0))

arrow(Q - 1.85*u(th_in), Q, SERIES[0])
arrow(Q, S, SERIES[0])
arrow(S, S + 1.85*u(th_out), SERIES[0])
ax.plot([Q[0], X[0] + 0.7*np.cos(th_in)], [Q[1], X[1] + 0.7*np.sin(th_in)],
        color=MUTED, lw=0.9, ls=(0, (3, 2)))
ax.plot([S[0], X[0] - 0.7*np.cos(th_out)], [S[1], X[1] - 0.7*np.sin(th_out)],
        color=MUTED, lw=0.9, ls=(0, (3, 2)))
ax.add_patch(Arc(tuple(X), 1.6, 1.6, theta1=np.degrees(th_out),
                 theta2=np.degrees(th_in), color='#A8271F', lw=1.1))
ax.text(X[0] + 1.02, X[1] + 0.03, r'$\delta_m$', color='#A8271F', fontsize=12,
        ha='center', va='center',
        bbox=dict(fc='white', ec='none', pad=1.5))
nl = np.array([-np.cos(np.radians(Adeg/2)), np.sin(np.radians(Adeg/2))])
nr = np.array([np.cos(np.radians(Adeg/2)), np.sin(np.radians(Adeg/2))])
for P, nn in [(Q, nl), (S, nr)]:
    ax.plot([P[0] - 0.95*nn[0], P[0] + 0.95*nn[0]],
            [P[1] - 0.95*nn[1], P[1] + 0.95*nn[1]],
            color=MUTED, lw=0.9, ls=(0, (2, 2)))
angl = np.degrees(np.arctan2(nl[1], nl[0]))
angr = np.degrees(np.arctan2(nr[1], nr[0]))


def mark(P, a0, a1_, dia, rad, lab, col, fs=10.5):
    ax.add_patch(Arc(tuple(P), dia, dia, theta1=a0, theta2=a1_, color=col, lw=1.0))
    am_ = np.radians((a0 + a1_)/2)
    ax.text(P[0] + rad*np.cos(am_), P[1] + rad*np.sin(am_), lab,
            color=col, fontsize=fs, ha='center', va='center')

mark(Q, angl, angl + i1, 1.0, 0.72, '$i$', SERIES[1])
mark(S, angr - i1, angr, 1.0, 0.92, '$i$', SERIES[1])
ax.add_patch(Arc(tuple(Q), 0.60, 0.60, theta1=angl + 180,
                 theta2=angl + 180 + r, color=SERIES[2], lw=1.0))
ax.add_patch(Arc(tuple(S), 0.60, 0.60, theta1=angr + 180 - r,
                 theta2=angr + 180, color=SERIES[2], lw=1.0))
bis = np.radians(angl + 180 + r/2)
ax.text(Q[0] + 0.62*np.cos(bis), Q[1] + 0.62*np.sin(bis), '$A/2$', color=SERIES[2],
        fontsize=9.5, ha='center', va='center')
ax.text(S[0] - 0.62*np.cos(bis), S[1] + 0.62*np.sin(bis), '$A/2$', color=SERIES[2],
        fontsize=9.5, ha='center', va='center')
ax.add_patch(Arc(tuple(apex), 0.9, 0.9, theta1=270 - Adeg/2, theta2=270 + Adeg/2,
                 color=INK, lw=1.0))
ax.text(apex[0], apex[1] - 0.68, '$A$', color=INK, fontsize=11, ha='center')
ax.plot([Lv[0] - 0.4, Rv[0] + 0.4], [0, 0], color=MUTED, lw=1.0, ls=':')
ax.text(0, -0.55, 'internal ray is parallel to the base',
        color=SERIES[2], fontsize=9.5, ha='center')
ax.annotate('Q', tuple(Q), textcoords='offset points', xytext=(-18, 18),
            color=INK, fontsize=10)
ax.annotate('S', tuple(S), textcoords='offset points', xytext=(-3, -18),
            color=INK, fontsize=10)
ax.set_xlim(-3.1, 3.3); ax.set_ylim(-0.95, 3.15)
ax.set_aspect('equal'); ax.axis('off')
```

::: caution Minimum deviation is not zero deviation
A prism always deviates light — $\delta$ can never be made zero (unlike a
parallel-sided slab, where it always is). "Minimum" means the smallest value the
deviation can be pushed down to, and it is reached at one particular angle of
incidence only.
:::

### When no light emerges

At the second face the internal ray meets the glass–air boundary at $r_2$. If
$r_2$ exceeds the critical angle $C$ the ray is totally internally reflected and
never leaves through that face. Since $r_1$ can never exceed $C$ (its largest
value, at grazing incidence $i_1 = 90^{\circ}$, is exactly $C$), the smallest
possible $r_2$ is $A - C$. So light can emerge only if $A - C \leq C$, that is

$$ A \leq 2C $$

For crown glass, $C = 41.8^{\circ}$, so no light emerges through the second face
of a prism whose refracting angle exceeds about $83.6^{\circ}$.

## 16.2 Relation between angle of prism, minimum deviation and refractive index

::: derivation $n = \dfrac{\sin\left(\dfrac{A+\delta_m}{2}\right)}{\sin\left(\dfrac{A}{2}\right)}$
We start from the two prism relations, add the fact that at minimum deviation the ray passes
symmetrically, and reach a formula for $n$ from two measurable angles.

**Setting up.** At minimum deviation the path through the prism is **symmetrical**: the ray
inside runs parallel to the base, the angle of incidence equals the angle of emergence, and the
two internal angles are equal. So

$$ i_1 = i_2 = i, \qquad r_1 = r_2 = r, \qquad \delta = \delta_m $$

**Step 1 — put the equal internal angles into $A = r_1 + r_2$:**

$$ A = r + r = 2r $$

**Step 2 — divide both sides by 2:**

$$ r = \frac{A}{2} $$

**Step 3 — put the equal external angles into $\delta = i_1 + i_2 - A$:**

$$ \delta_m = i + i - A = 2i - A $$

**Step 4 — add $A$ to both sides:**

$$ A + \delta_m = 2i $$

**Step 5 — divide both sides by 2:**

$$ i = \frac{A + \delta_m}{2} $$

**Step 6 — apply Snell's law at the first face,** where light goes from air into glass:

$$ n = \frac{\sin i}{\sin r} $$

**Step 7 — substitute the expressions for $i$ and $r$ from Steps 5 and 2:**

$$ n = \frac{\sin\left(\dfrac{A+\delta_m}{2}\right)}{\sin\left(\dfrac{A}{2}\right)} $$

**Result.**

$$ n = \frac{\sin\left(\dfrac{A+\delta_m}{2}\right)}{\sin\left(\dfrac{A}{2}\right)} $$

**What it means.** This is the **prism formula**, and it is the standard accurate method for
finding $n$. Everything on the right is an *angle*, and a spectrometer measures angles to within
a few minutes of arc — far more precisely than we could measure a length or a depth. Note also
that a larger $\delta_m$ for the same prism means a larger $n$, which is why violet light
(deviated most) has the largest refractive index.

**Conditions used.** The prism must be set at **minimum deviation**, so that the path is
symmetrical; monochromatic light must be used, since $n$ and $\delta_m$ both depend on colour;
and the surrounding medium must be air.
:::

::: tip The examiner is looking for
1. A labelled diagram with $i_1$, $r_1$, $r_2$, $i_2$, $A$ and $\delta$ marked.
2. The two prism relations quoted or derived.
3. The statement of the symmetry condition at minimum deviation, $i_1 = i_2$ and
   $r_1 = r_2$ — usually worth a mark on its own.
4. $r = A/2$ and $i = (A+\delta_m)/2$, each shown as a separate line.
5. Snell's law at the first face, and the final substitution.
:::

::: tip The laboratory routine
On a spectrometer, rotate the prism table slowly while watching the refracted
image through the telescope. The image moves one way, stops, and turns back. The
turning point is the position of minimum deviation — that "stop and go back"
moment is what the examiner wants described.
:::

::: memory Order of attack for any prism numerical
1. From $i_1$ find $r_1$ using $\sin i_1 = n\sin r_1$.
2. From $A = r_1 + r_2$ find $r_2$.
3. From $n\sin r_2 = \sin i_2$ find $i_2$.
4. From $\delta = i_1 + i_2 - A$ find the deviation.

Reverse the chain if you are given $\delta_m$: $r = A/2$, $i = (A+\delta_m)/2$,
then $n = \sin i/\sin r$. Never mix the two chains in one question.
:::

::: example Worked example 16.1
**Problem.** The angle of minimum deviation of an equilateral glass prism is
$30^{\circ}$. Find the refractive index of the glass and the angle of incidence
at minimum deviation.

**Solution.** An equilateral prism has $A = 60^{\circ}$, and $\delta_m = 30^{\circ}$.

$$ n = \frac{\sin\left(\frac{60^{\circ}+30^{\circ}}{2}\right)}{\sin\left(\frac{60^{\circ}}{2}\right)}
= \frac{\sin 45^{\circ}}{\sin 30^{\circ}} = \frac{0.7071}{0.5} = 1.414 $$

So $n = \sqrt{2} \approx 1.41$. The angle of incidence is

$$ i = \frac{A + \delta_m}{2} = \frac{60^{\circ} + 30^{\circ}}{2} = 45^{\circ} $$

and the angle of refraction inside is $r = A/2 = 30^{\circ}$.
:::

::: example Worked example 16.2
**Problem.** An equilateral prism is made of glass of refractive index $1.5$.
Calculate its angle of minimum deviation.

**Solution.** Here $A = 60^{\circ}$ and $n = 1.5$. Rearranging the prism formula,

$$ \sin\left(\frac{A+\delta_m}{2}\right) = n\sin\frac{A}{2} = 1.5 \times \sin 30^{\circ} = 1.5 \times 0.5 = 0.75 $$

$$ \frac{A+\delta_m}{2} = \sin^{-1}(0.75) = 48.59^{\circ} $$

$$ \delta_m = 2 \times 48.59^{\circ} - 60^{\circ} = 37.18^{\circ} \approx 37.2^{\circ} $$

The light must strike the first face at $48.6^{\circ}$ for this to happen.
:::

::: example Worked example 16.3
**Problem.** A ray strikes one refracting face of an equilateral prism
($n = 1.5$) at an angle of incidence of $45^{\circ}$. Find the angle of refraction
at the first face, the angle of incidence at the second face, the angle of
emergence, and the deviation. Compare the deviation with the minimum value found
in Example 16.2.

**Solution.** At the first face,

$$ \sin r_1 = \frac{\sin 45^{\circ}}{1.5} = \frac{0.7071}{1.5} = 0.4714 \qquad \Rightarrow \qquad r_1 = 28.13^{\circ} $$

Using $A = r_1 + r_2$,

$$ r_2 = 60^{\circ} - 28.13^{\circ} = 31.87^{\circ} $$

At the second face, glass to air,

$$ \sin i_2 = n\sin r_2 = 1.5 \times \sin 31.87^{\circ} = 1.5 \times 0.5280 = 0.7921 $$

$$ i_2 = 52.38^{\circ} $$

The deviation is

$$ \delta = i_1 + i_2 - A = 45^{\circ} + 52.38^{\circ} - 60^{\circ} = 37.38^{\circ} $$

This is slightly **greater** than $\delta_m = 37.18^{\circ}$, as it must be — and
it is only $0.2^{\circ}$ greater even though $i_1$ is $3.6^{\circ}$ away from the
symmetric value. Near the minimum the curve is very flat, which is exactly why
the minimum position is easy to find on a spectrometer.
:::

## 16.3 Deviation in small angle prism

A prism whose refracting angle is only a few degrees is called a **thin** or
**small-angle** prism. For such a prism a beautifully simple result holds.

```figure caption="A thin prism of refracting angle $A = 20^{\circ}$. The emergent ray is turned through $\delta \approx (n-1)A$ from the incident direction, almost independently of how the ray enters."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Arc, Polygon
fig, ax = plt.subplots(figsize=(5.0, 2.9))
Adeg, n, i1 = 20.0, 1.5, 10.0
H = 2.6
w = H*np.tan(np.radians(Adeg/2))
apex = np.array([0.0, H]); Lv = np.array([-w, 0.0]); Rv = np.array([w, 0.0])
ax.add_patch(Polygon([apex, Lv, Rv], closed=True, fc=ACCENT, alpha=0.13,
                     ec=INK, lw=1.7))
r1 = np.degrees(np.arcsin(np.sin(np.radians(i1))/n))
r2 = Adeg - r1
i2 = np.degrees(np.arcsin(n*np.sin(np.radians(r2))))
dev = i1 + i2 - Adeg
th_in = np.radians(-Adeg/2 + i1)
th_1 = np.radians(-Adeg/2 + r1)
th_out = np.radians(Adeg/2 - i2)
u = lambda a: np.array([np.cos(a), np.sin(a)])
Q = apex + 0.5*(Lv - apex)
M = np.array([[np.cos(th_1), -(Rv - apex)[0]], [np.sin(th_1), -(Rv - apex)[1]]])
tt, uu = np.linalg.solve(M, apex - Q)
S = Q + tt*u(th_1)

def arrow(p, q, c, lw=1.6):
    ax.annotate('', xy=tuple(q), xytext=tuple(p),
                arrowprops=dict(arrowstyle='-|>', color=c, lw=lw,
                                mutation_scale=12, shrinkA=0, shrinkB=0))

arrow(Q - 2.6*u(th_in), Q, SERIES[0])
arrow(Q, S, SERIES[0])
arrow(S, S + 2.9*u(th_out), SERIES[0])
ax.plot([Q[0], Q[0] + 4.6*np.cos(th_in)], [Q[1], Q[1] + 4.6*np.sin(th_in)],
        color=MUTED, lw=0.9, ls=(0, (3, 2)))
Mx = np.array([[np.cos(th_in), -np.cos(th_out)], [np.sin(th_in), -np.sin(th_out)]])
a1, a2 = np.linalg.solve(Mx, S - Q)
X = Q + a1*u(th_in)
ax.add_patch(Arc(tuple(X), 3.6, 3.6, theta1=np.degrees(th_out),
                 theta2=np.degrees(th_in), color='#A8271F', lw=1.1))
am = (th_in + th_out)/2
ax.text(X[0] + 2.08*np.cos(am), X[1] + 2.08*np.sin(am), r'$\delta$',
        color='#A8271F', fontsize=12, ha='center', va='center')
ax.add_patch(Arc(tuple(apex), 0.9, 0.9, theta1=270 - Adeg/2, theta2=270 + Adeg/2,
                 color=INK, lw=1.0))
ax.text(apex[0] + 0.42, apex[1] - 0.40, '$A$', color=INK, fontsize=11, ha='left')
ax.annotate('Q', tuple(Q), textcoords='offset points', xytext=(-14, 4), color=INK, fontsize=10)
ax.annotate('S', tuple(S), textcoords='offset points', xytext=(7, 5), color=INK, fontsize=10)
ax.set_xlim(-3.1, 4.6); ax.set_ylim(-0.55, 3.1)
ax.set_aspect('equal'); ax.axis('off')
```

::: derivation $\delta = (n-1)A$ for a thin prism
We start from Snell's law at the two faces with all angles small, and reach a deviation formula
that no longer contains the angle of incidence at all.

**Setting up.** The refracting angle $A$ is small (a few degrees) and the ray enters nearly
normally. Then $A = r_1 + r_2$ forces $r_1$ and $r_2$ to be small, and Snell's law then makes
$i_1$ and $i_2$ small too. All four are small angles measured in radians.

**Step 1 — Snell's law at the first face:**

$$ \frac{\sin i_1}{\sin r_1} = n $$

**Step 2 — use the small-angle approximation $\sin\theta \approx \theta$:**

$$ \frac{i_1}{r_1} = n $$

**Step 3 — make $i_1$ the subject:**

$$ i_1 = n r_1 $$

**Step 4 — repeat the same three steps at the second face:**

$$ i_2 = n r_2 $$

**Step 5 — substitute both into $\delta = i_1 + i_2 - A$:**

$$ \delta = n r_1 + n r_2 - A $$

**Step 6 — take out the common factor $n$:**

$$ \delta = n(r_1 + r_2) - A $$

**Step 7 — replace $(r_1 + r_2)$ by $A$,** using the first prism relation:

$$ \delta = nA - A $$

**Step 8 — take out the common factor $A$:**

$$ \delta = (n - 1)A $$

**Result.**

$$ \delta = (n - 1)A $$

**What it means.** The angle of incidence has vanished from the answer. For a thin prism the
deviation is fixed by the prism itself — its angle and its glass — so you do not need to hunt
for the minimum-deviation position. And because $n$ depends on colour, so does $\delta$: this
one line is the seed of the whole theory of dispersion.

**Conditions used.** $A$ must be small (in practice under about $10^{\circ}$) and the ray must
strike nearly normally, so that $\sin\theta \approx \theta$ is safe in Step 2. For a thick prism
or a slanting ray the formula fails and the full prism formula must be used.
:::

Three consequences matter:

1. **$\delta$ does not depend on $i_1$.** For a thin prism the deviation is
   essentially the same however the ray is aimed (within small angles), so there
   is no need to set it at minimum deviation.
2. **$\delta$ depends on $n$, and $n$ depends on colour.** Violet light, with the
   larger $n$, is deviated more than red. This is the origin of dispersion
   (Unit 18), where the *angular dispersion* is
   $\delta_V - \delta_R = (n_V - n_R)A$.
3. **Thin prisms add.** Two thin prisms placed together with their refracting
   edges the same way deviate light by $\delta_1 + \delta_2$; reversing one
   subtracts. This is how achromatic prism combinations are designed, and how
   optometrists in Kathmandu correct squint with "prism dioptres".

::: example Worked example 16.4
**Problem.** A thin prism of refracting angle $5^{\circ}$ is made of glass of
refractive index $1.52$. Find the deviation it produces. What angle of prism
would be needed to produce the same deviation with glass of $n = 1.65$?

**Solution.** For a thin prism,

$$ \delta = (n-1)A = (1.52 - 1) \times 5^{\circ} = 0.52 \times 5^{\circ} = 2.6^{\circ} $$

For the second glass, requiring the same $\delta = 2.6^{\circ}$,

$$ A' = \frac{\delta}{n'-1} = \frac{2.6^{\circ}}{1.65 - 1} = \frac{2.6^{\circ}}{0.65} = 4^{\circ} $$

A denser glass needs a smaller refracting angle for the same bending — which is
why high-index glass is used where a prism must be kept thin and light.
:::

## Chapter summary

- For a prism of refracting angle $A$: $A = r_1 + r_2$ and
  $\delta = i_1 + i_2 - A$.
- The graph of $\delta$ against $i_1$ has one minimum. Above the minimum, two
  angles of incidence give the same deviation; at the minimum they coincide.
- At minimum deviation the passage is symmetrical: $i_1 = i_2$, $r_1 = r_2 = A/2$,
  and the internal ray is parallel to the base.
- Prism formula:
  $n = \dfrac{\sin\left(\frac{A+\delta_m}{2}\right)}{\sin\left(\frac{A}{2}\right)}$,
  with $i = \dfrac{A+\delta_m}{2}$ at minimum deviation.
- Light can emerge through the second face only if $A \leq 2C$, where $C$ is the
  critical angle; otherwise total internal reflection occurs inside the prism.
- For a thin prism, $\delta = (n-1)A$, independent of the angle of incidence, and
  thin-prism deviations simply add.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. For a prism of refracting angle $A$ at minimum deviation $\delta_m$, the angle of incidence is <span class="marks">[1]</span>
   (a) $A/2$ (b) $\dfrac{A+\delta_m}{2}$ (c) $\delta_m/2$ (d) $A + \delta_m$
2. At minimum deviation the ray inside the prism is <span class="marks">[1]</span>
   (a) parallel to the base (b) normal to the base
   (c) parallel to a refracting face (d) along the base
3. The deviation produced by a thin prism of refracting angle $6^{\circ}$ made of glass of $n = 1.5$ is <span class="marks">[1]</span>
   (a) $2^{\circ}$ (b) $3^{\circ}$ (c) $4^{\circ}$ (d) $9^{\circ}$
4. The refractive index of the material of an equilateral prism whose minimum deviation is $30^{\circ}$ is <span class="marks">[1]</span>
   (a) $1.33$ (b) $1.41$ (c) $1.50$ (d) $1.73$
5. In a prism, the sum of the two angles of refraction $r_1 + r_2$ is equal to <span class="marks">[1]</span>
   (a) the angle of incidence (b) the angle of the prism
   (c) the angle of deviation (d) $90^{\circ}$
6. A ray cannot emerge from the second face of a prism if the refracting angle $A$ is <span class="marks">[1]</span>
   (a) less than $C$ (b) equal to $C$ (c) greater than $2C$ (d) less than $2C$

::: note Answers to Group A
**1.** (b) — from $\delta_m = 2i - A$.
**2.** (a) — symmetrical passage makes the internal ray parallel to the base.
**3.** (b) — $\delta = (n-1)A = 0.5\times6^{\circ} = 3^{\circ}$.
**4.** (b) — $n = \sin45^{\circ}/\sin30^{\circ} = 1.414$.
**5.** (b) — $A = r_1 + r_2$.
**6.** (c) — then $r_2 = A - r_1 > C$ for every $r_1$, so the ray is totally internally reflected.
:::

**Group B — Short answer (5 marks each)**

1. Define the refracting angle of a prism, the angle of deviation and the angle of
   minimum deviation. With a labelled diagram, show that
   $\delta = i_1 + i_2 - A$. <span class="marks">[5]</span>
2. Derive the relation
   $n = \dfrac{\sin\left(\frac{A+\delta_m}{2}\right)}{\sin\left(\frac{A}{2}\right)}$
   between the angle of a prism, its angle of minimum deviation and the refractive
   index of its material. <span class="marks">[5]</span>
3. Show that for a prism of small refracting angle the deviation is
   $\delta = (n-1)A$ and is independent of the angle of incidence. <span class="marks">[5]</span>
4. Calculate the angle of minimum deviation of an equilateral prism made of glass
   of refractive index $1.6$. <span class="marks">[5]</span>
5. The angle of minimum deviation of a prism of refracting angle $60^{\circ}$ is
   $40^{\circ}$. Find the refractive index of its material and the angle of
   incidence at minimum deviation. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Definitions and derivation as in §16.1.

**2.** See the derivation in §16.2.

**3.** See the derivation in §16.3.

**4.** $\sin\left(\dfrac{60^{\circ}+\delta_m}{2}\right) = 1.6\sin30^{\circ} = 0.8$,
so $\dfrac{60^{\circ}+\delta_m}{2} = 53.13^{\circ}$ and
$\delta_m = 106.26^{\circ} - 60^{\circ} = 46.26^{\circ} \approx 46.3^{\circ}$.

**5.** $n = \dfrac{\sin\left(\frac{60^{\circ}+40^{\circ}}{2}\right)}{\sin 30^{\circ}}
= \dfrac{\sin 50^{\circ}}{0.5} = \dfrac{0.7660}{0.5} = 1.532$.
The angle of incidence is $i = \dfrac{A+\delta_m}{2} = 50^{\circ}$.
:::

**Group C — Long answer (8 marks each)**

1. (a) Draw the path of a monochromatic ray through a glass prism and prove that
   $A = r_1 + r_2$ and $\delta = i_1 + i_2 - A$. <span class="marks">[4]</span>
   (b) Sketch the graph of deviation against angle of incidence, and use it to
   show that at minimum deviation the ray passes symmetrically. Hence derive the
   prism formula. <span class="marks">[4]</span>
2. A ray of light is incident at $40^{\circ}$ on one refracting face of an
   equilateral prism of refractive index $1.5$. Calculate (a) the angle of
   refraction at the first face, (b) the angle of incidence at the second face,
   (c) the angle of emergence, and (d) the angle of deviation. Show that this
   deviation is greater than the minimum deviation of the same prism. <span class="marks">[8]</span>

::: note Answer to Group C question 2
(a) $\sin r_1 = \dfrac{\sin 40^{\circ}}{1.5} = \dfrac{0.6428}{1.5} = 0.4285$, so
$r_1 = 25.37^{\circ}$.

(b) $r_2 = A - r_1 = 60^{\circ} - 25.37^{\circ} = 34.63^{\circ}$.

(c) $\sin i_2 = 1.5\sin 34.63^{\circ} = 1.5 \times 0.5682 = 0.8522$, so
$i_2 = 58.47^{\circ}$.

(d) $\delta = i_1 + i_2 - A = 40^{\circ} + 58.47^{\circ} - 60^{\circ} = 38.47^{\circ}$.

For the same prism, $\sin\left(\frac{60^{\circ}+\delta_m}{2}\right) = 1.5\sin30^{\circ} = 0.75$,
giving $\delta_m = 37.18^{\circ}$. Since $38.47^{\circ} > 37.18^{\circ}$, the
deviation here is indeed above the minimum — as it must be for any angle of
incidence other than $48.59^{\circ}$.
:::
