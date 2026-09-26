---
subject: Physics
grade: 12
unit: 1
title: Rotational dynamics
hours: 7
area: Mechanics
---

A spinning flywheel, a turning grinding stone at a mill in Bhaktapur, the rotor
of a Kulekhani turbine — none of these move from place to place, yet they
clearly have motion and energy. To describe them we need a second set of
mechanics, built on angle instead of distance. Every idea you learned in Grade
11 has a rotational twin: displacement becomes angle, mass becomes moment of
inertia, force becomes torque. Learn the dictionary and most of this unit
writes itself.

::: key The translation table is the whole unit
Every rotational formula in this chapter is a linear formula with the symbols
swapped: $s \to \theta$, $v \to \omega$, $a \to \alpha$, $m \to I$,
$F \to \tau$, $p \to L$. If you can recall the linear result, you can rebuild
the rotational one.
:::

## 1.1 Equation of angular motion; Relation between linear and angular kinematics

When a rigid body rotates about a fixed axis, every particle of it moves in a
circle centred on that axis. Different particles travel different distances in
the same time, but all of them sweep the **same angle**. That is why angle, not
distance, is the natural variable.

The **angular displacement** $\theta$ is measured in radians, defined by

$$ \theta = \frac{s}{r} $$

where $s$ is the arc length and $r$ the radius. The **angular velocity** and
**angular acceleration** are then

$$ \omega = \frac{d\theta}{dt}, \qquad \alpha = \frac{d\omega}{dt} = \frac{d^{2}\theta}{dt^{2}} $$

with units rad s⁻¹ and rad s⁻².

```figure caption="A rigid body rotating about an axis through $O$ perpendicular to the page. Every point sweeps the same angle $\theta$, but a point at radius $r$ moves with speed $v = r\omega$ along the tangent."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.4,3.0))
R = 1.0
th = np.linspace(0, 2*np.pi, 400)
ax.plot(R*np.cos(th), R*np.sin(th), color=MUTED, lw=1.2)
ax.fill(R*np.cos(th), R*np.sin(th), color=ACCENT, alpha=0.07)
a = np.radians(52)
P = np.array([R*np.cos(a), R*np.sin(a)])
ax.plot([0, R], [0, 0], color=MUTED, lw=1.0, ls='--')
ax.plot([0, P[0]], [0, P[1]], color=INK, lw=1.5)
ta = np.linspace(0, a, 80)
ax.plot(0.30*np.cos(ta), 0.30*np.sin(ta), color='#A8271F', lw=1.3)
ax.annotate(r'$\theta$', (0.46*np.cos(a/2 - np.radians(6)),
            0.46*np.sin(a/2 - np.radians(6))), color='#A8271F',
            fontsize=10, ha='center', va='center')
ax.plot(R*np.cos(ta), R*np.sin(ta), color='#A8271F', lw=3.0, solid_capstyle='butt')
ax.annotate('arc $s=r\\theta$', (R*np.cos(a*0.45), R*np.sin(a*0.45)),
            textcoords='offset points', xytext=(12, 6), color='#A8271F', fontsize=9)
that = np.array([-np.sin(a), np.cos(a)])
ax.annotate('', xy=P + 0.80*that, xytext=P,
            arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.8, mutation_scale=13))
ax.annotate(r'$v=r\omega$', P + 0.80*that, textcoords='offset points',
            xytext=(-6, 8), color=ACCENT, fontsize=9.5)
rhat = P/np.linalg.norm(P)
ax.annotate('', xy=P - 0.52*rhat, xytext=P,
            arrowprops=dict(arrowstyle='-|>', color='#0B6A62', lw=1.6, mutation_scale=12))
ax.annotate(r'$a_c=r\omega^2$', P - 0.30*rhat, textcoords='offset points',
            xytext=(-14, 12), color='#0B6A62', fontsize=9, ha='right')
ax.annotate(r'$r$', P*0.62, textcoords='offset points', xytext=(-6, 11),
            color=INK, fontsize=10)
ax.plot([0], [0], 'o', color=INK, ms=4.5)
ax.annotate('$O$', (0, 0), textcoords='offset points', xytext=(-11, -11),
            color=INK, fontsize=10)
tc = np.linspace(np.radians(190), np.radians(300), 60)
ax.plot(0.55*np.cos(tc), 0.55*np.sin(tc), color=MUTED, lw=1.2)
ax.annotate('', xy=(0.55*np.cos(tc[-1]), 0.55*np.sin(tc[-1])),
            xytext=(0.55*np.cos(tc[-4]), 0.55*np.sin(tc[-4])),
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.2, mutation_scale=10))
ax.annotate(r'$\omega$', (0.62*np.cos(np.radians(250)), 0.62*np.sin(np.radians(250))),
            color=MUTED, fontsize=10, ha='center')
ax.set_xlim(-1.35, 1.75); ax.set_ylim(-1.35, 1.6)
ax.set_aspect('equal'); ax.axis('off')
```

If $\alpha$ is **constant**, integrating twice gives the equations of angular
motion, exactly parallel to the linear ones:

$$ \omega = \omega_0 + \alpha t, \qquad \theta = \omega_0 t + \tfrac{1}{2}\alpha t^{2},
\qquad \omega^{2} = \omega_0^{2} + 2\alpha\theta $$

and the angle turned in the $n^{\text{th}}$ second is
$\theta_n = \omega_0 + \frac{\alpha}{2}(2n-1)$.

Because $s = r\theta$ and $r$ is fixed for a given particle, differentiating
gives the **link between the linear and angular pictures**:

$$ v = r\omega, \qquad a_t = r\alpha, \qquad a_c = \frac{v^{2}}{r} = r\omega^{2} $$

Here $a_t$ is the **tangential** acceleration (it changes the speed) and $a_c$
is the **centripetal** acceleration (it changes the direction). The resultant
linear acceleration has magnitude $a = \sqrt{a_t^{2} + a_c^{2}}$.

| Linear quantity | Rotational quantity | Connection |
|---|---|---|
| Displacement $s$ (m) | Angular displacement $\theta$ (rad) | $s = r\theta$ |
| Velocity $v$ (m s⁻¹) | Angular velocity $\omega$ (rad s⁻¹) | $v = r\omega$ |
| Acceleration $a$ (m s⁻²) | Angular acceleration $\alpha$ (rad s⁻²) | $a_t = r\alpha$ |
| Mass $m$ (kg) | Moment of inertia $I$ (kg m²) | $I = \sum m r^{2}$ |
| Force $F$ (N) | Torque $\tau$ (N m) | $\tau = rF\sin\phi$ |
| Momentum $p = mv$ | Angular momentum $L = I\omega$ | $L = rp\sin\phi$ |

::: caution Radians, never degrees or rpm
$v = r\omega$, $s = r\theta$ and $\tau = I\alpha$ are true **only** when angles
are in radians. Convert first: $1\ \text{rev} = 2\pi\ \text{rad}$, and
$N$ rev min⁻¹ means $\omega = 2\pi N/60$ rad s⁻¹.
:::

::: example Worked example 1.1
**Problem.** A grinding wheel starts from rest and reaches $300$ rev min⁻¹ in
$10\ \text{s}$ with uniform angular acceleration. Find (a) the angular
acceleration, (b) the number of revolutions made, and (c) the linear speed of a
point $0.40\ \text{m}$ from the axis at the end.

**Solution.**
(a) $\omega = \dfrac{2\pi \times 300}{60} = 10\pi = 31.4\ \text{rad s}^{-1}$, so

$$ \alpha = \frac{\omega - \omega_0}{t} = \frac{10\pi - 0}{10} = \pi = 3.14\ \text{rad s}^{-2} $$

(b) $\theta = \tfrac{1}{2}\alpha t^{2} = \tfrac{1}{2}(\pi)(10)^{2} = 50\pi\ \text{rad}$.
Number of revolutions $= 50\pi / 2\pi = 25$ revolutions.

(c) $v = r\omega = 0.40 \times 31.4 = 12.6\ \text{m s}^{-1}$.
:::

## 1.2 Kinetic energy of rotation of rigid body

Think of the rigid body as a collection of particles of masses
$m_1, m_2, \ldots$ at perpendicular distances $r_1, r_2, \ldots$ from the axis.
All share the same $\omega$, so particle $i$ has speed $v_i = r_i\omega$.

::: derivation Rotational kinetic energy
The total kinetic energy is the sum of the kinetic energies of the particles:

$$ E_k = \sum_i \tfrac{1}{2}m_i v_i^{2} = \sum_i \tfrac{1}{2}m_i (r_i\omega)^{2}
= \tfrac{1}{2}\left(\sum_i m_i r_i^{2}\right)\omega^{2} $$

The bracket contains only the masses and their distances from the axis — it is a
property of the body and the axis, not of the motion. Calling it the **moment
of inertia** $I$,

$$ E_k = \tfrac{1}{2}I\omega^{2} $$
:::

Compare $\frac{1}{2}mv^{2}$: the moment of inertia plays exactly the role that
mass plays in translation. A body that is also moving forward (a rolling wheel)
has total kinetic energy $\frac{1}{2}mv^{2} + \frac{1}{2}I\omega^{2}$.

## 1.3 Moment of inertia; Radius of gyration

::: definition Moment of inertia
The moment of inertia of a body about a given axis is the sum of the products of
the mass of each particle and the square of its perpendicular distance from that
axis: $I = \sum m_i r_i^{2}$, or $I = \int r^{2}\,dm$ for a continuous body. Its
SI unit is kg m² and its dimensional formula is $[ML^{2}]$.
:::

Moment of inertia measures **rotational inertia** — the opposition a body offers
to a change in its angular velocity. Unlike mass it is not a single number for a
body: it depends on (i) the total mass, (ii) how that mass is distributed, and
(iii) **which axis** is chosen. Mass placed far from the axis counts much more,
because the distance is squared.

Two theorems shorten most calculations:

- **Parallel axis theorem.** $I = I_{cm} + Md^{2}$, where $I_{cm}$ is about a
  parallel axis through the centre of mass and $d$ is the separation.
- **Perpendicular axis theorem** (plane laminae only).
  $I_z = I_x + I_y$, the $z$-axis being perpendicular to the lamina.

| Body (mass $M$) | Axis | Moment of inertia | Radius of gyration $k$ |
|---|---|---|---|
| Thin rod, length $L$ | ⊥ through centre | $ML^{2}/12$ | $L/\sqrt{12}$ |
| Thin rod, length $L$ | ⊥ through one end | $ML^{2}/3$ | $L/\sqrt{3}$ |
| Ring, radius $R$ | central, ⊥ to plane | $MR^{2}$ | $R$ |
| Disc, radius $R$ | central, ⊥ to plane | $MR^{2}/2$ | $R/\sqrt{2}$ |
| Solid cylinder, radius $R$ | own axis | $MR^{2}/2$ | $R/\sqrt{2}$ |
| Solid sphere, radius $R$ | diameter | $2MR^{2}/5$ | $R\sqrt{2/5}$ |
| Hollow sphere, radius $R$ | diameter | $2MR^{2}/3$ | $R\sqrt{2/3}$ |

The **radius of gyration** $k$ is the distance from the axis at which the whole
mass could be concentrated as a single point without changing the moment of
inertia:

$$ I = Mk^{2} \qquad \Longrightarrow \qquad k = \sqrt{\frac{I}{M}} $$

::: example Worked example 1.2
**Problem.** A solid disc flywheel of mass $20\ \text{kg}$ and radius
$0.50\ \text{m}$ spins at $120$ rev min⁻¹. Find its moment of inertia, radius of
gyration and rotational kinetic energy.

**Solution.**
$$ I = \tfrac{1}{2}MR^{2} = \tfrac{1}{2}(20)(0.50)^{2} = 2.5\ \text{kg m}^{2} $$
$$ k = \sqrt{I/M} = \sqrt{2.5/20} = \sqrt{0.125} = 0.354\ \text{m} $$

which is indeed $R/\sqrt{2}$. With $\omega = 2\pi(120)/60 = 4\pi = 12.57\ \text{rad s}^{-1}$,

$$ E_k = \tfrac{1}{2}I\omega^{2} = \tfrac{1}{2}(2.5)(12.57)^{2} = 197\ \text{J} $$
:::

## 1.4 Moment of inertia of a uniform rod

::: derivation Uniform thin rod, axis through the centre
Take a rod of mass $M$ and length $L$, of uniform linear mass density
$\lambda = M/L$. Let the axis pass through the centre $C$, perpendicular to the
rod. Consider a small element of length $dx$ at a distance $x$ from $C$; its
mass is $dm = \lambda\,dx = (M/L)\,dx$ and its moment of inertia is
$x^{2}\,dm$.

Summing over the whole rod, $x$ runs from $-L/2$ to $+L/2$:

$$ I_C = \int_{-L/2}^{+L/2} x^{2}\frac{M}{L}dx
= \frac{M}{L}\left[\frac{x^{3}}{3}\right]_{-L/2}^{+L/2}
= \frac{M}{3L}\left(\frac{L^{3}}{8} + \frac{L^{3}}{8}\right) $$

$$ I_C = \frac{ML^{2}}{12} $$
:::

::: derivation Same rod, axis through one end
Now put the axis at the end $A$, so $x$ runs from $0$ to $L$:

$$ I_A = \int_{0}^{L} x^{2}\frac{M}{L}dx = \frac{M}{L}\left[\frac{x^{3}}{3}\right]_{0}^{L}
= \frac{ML^{2}}{3} $$

Check with the parallel axis theorem: the end is a distance $d = L/2$ from the
centre of mass, so

$$ I_A = I_C + M\left(\frac{L}{2}\right)^{2} = \frac{ML^{2}}{12} + \frac{ML^{2}}{4}
= \frac{ML^{2}}{3} \quad \checkmark $$
:::

```figure caption="Moment of inertia of a uniform rod. The shaded element of mass $dm=(M/L)dx$ sits a distance $x$ from the axis. Shifting the axis from the centre to the end raises $I$ from $ML^2/12$ to $ML^2/3$."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(4.9,2.9))
def rod(y, xaxis, label, Ilab):
    ax.add_patch(Rectangle((-1, y-0.085), 2, 0.17, facecolor=ACCENT,
                           alpha=0.20, edgecolor=INK, lw=1.1))
    ax.plot([xaxis, xaxis], [y-0.55, y+0.55], color='#A8271F', lw=1.4, ls='--')
    ax.plot([xaxis], [y], 'o', color='#A8271F', ms=4.5)
    ax.annotate(label, (xaxis, y+0.57), color='#A8271F', fontsize=9,
                ha=('center' if xaxis == 0 else 'left'), va='bottom')
    ax.annotate(Ilab, (1.15, y), color=INK, fontsize=10, va='center')
rod(0.75, 0.0, 'axis through centre', r'$I=\dfrac{ML^2}{12}$')
rod(-0.75, -1.0, 'axis through end', r'$I=\dfrac{ML^2}{3}$')
# element on the top rod
ax.add_patch(Rectangle((0.44, 0.75-0.085), 0.13, 0.17, facecolor='#A8271F',
                       alpha=0.85, edgecolor='none'))
ax.annotate('', xy=(0.44, 0.52), xytext=(0.0, 0.52),
            arrowprops=dict(arrowstyle='<|-|>', color=INK, lw=1.0, mutation_scale=9))
ax.annotate('$x$', (0.22, 0.47), color=INK, fontsize=9.5, ha='center', va='top')
ax.annotate('$dx$', (0.505, 0.90), color='#A8271F', fontsize=9.5, ha='center', va='bottom')
# length marker on the bottom rod
ax.annotate('', xy=(1.0, -1.18), xytext=(-1.0, -1.18),
            arrowprops=dict(arrowstyle='<|-|>', color=MUTED, lw=1.0, mutation_scale=9))
ax.annotate('$L$', (0.0, -1.24), color=MUTED, fontsize=9.5, ha='center', va='top')
ax.set_xlim(-1.5, 2.3); ax.set_ylim(-1.7, 1.5)
ax.set_aspect('equal'); ax.axis('off')
```

## 1.5 Torque and angular acceleration for a rigid body

A force applied to a body that is free to rotate produces a turning effect
called **torque** (or moment of force). If the force $\vec{F}$ acts at a point
whose position vector from the axis is $\vec{r}$, and $\phi$ is the angle
between them,

$$ \tau = rF\sin\phi = F\,(r\sin\phi) = F \times (\text{perpendicular distance from the axis}) $$

The quantity $d = r\sin\phi$ is the **moment arm**. Torque is largest when the
force is applied perpendicular to $\vec{r}$ and as far from the axis as
possible — which is why a door handle is fitted at the edge, not next to the
hinge. The SI unit is N m; torque is a vector, $\vec{\tau} = \vec{r}\times\vec{F}$.

```figure caption="Torque about the axis at $O$. Only the component $F\sin\phi$ perpendicular to $\vec{r}$ turns the body; the moment arm is $d = r\sin\phi$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.7,2.9))
O = np.array([0.0, 0.0])
A = np.array([2.4, 0.55])
phi = np.radians(55)
rhat = (A-O)/np.linalg.norm(A-O)
ang_r = np.arctan2(rhat[1], rhat[0])
fdir = np.array([np.cos(ang_r+phi), np.sin(ang_r+phi)])
# body: shaded irregular plate
tt = np.linspace(0, 2*np.pi, 200)
bx = 1.35 + 1.35*np.cos(tt); by = 0.30 + 0.85*np.sin(tt)
ax.fill(bx, by, color=ACCENT, alpha=0.09)
ax.plot(bx, by, color=MUTED, lw=1.0)
# r vector
ax.annotate('', xy=A, xytext=O, arrowprops=dict(arrowstyle='-|>', color=INK,
            lw=1.6, mutation_scale=12))
ax.annotate(r'$\vec{r}$', O + (A-O)*0.55, textcoords='offset points',
            xytext=(-2, -14), color=INK, fontsize=10)
# force
F = A + 1.5*fdir
ax.annotate('', xy=F, xytext=A, arrowprops=dict(arrowstyle='-|>', color='#A8271F',
            lw=1.9, mutation_scale=13))
ax.annotate(r'$\vec{F}$', F, textcoords='offset points', xytext=(3, 2),
            color='#A8271F', fontsize=10)
# line of action (dashed both ways)
ext = np.array([A - 2.6*fdir, A + 2.2*fdir])
ax.plot(ext[:, 0], ext[:, 1], color='#A8271F', lw=0.9, ls=':')
# perpendicular from O to line of action
t = np.dot(O - A, fdir)
foot = A + t*fdir
ax.plot([O[0], foot[0]], [O[1], foot[1]], color='#0B6A62', lw=1.4, ls='--')
ax.annotate('$d=r\\sin\\phi$', (O+foot)/2, textcoords='offset points',
            xytext=(-2, -21), color='#0B6A62', fontsize=9.5, ha='center')
perp = np.array([-fdir[1], fdir[0]])
sq = 0.17
ax.plot([foot[0]-sq*perp[0], foot[0]-sq*perp[0]+sq*fdir[0], foot[0]+sq*fdir[0]],
        [foot[1]-sq*perp[1], foot[1]-sq*perp[1]+sq*fdir[1], foot[1]+sq*fdir[1]],
        color='#0B6A62', lw=0.9)
# angle phi arc at A
aa = np.linspace(ang_r + np.pi, ang_r + np.pi + phi, 60)
# arc between -r direction reversed: draw between r-direction and F-direction at A
aa = np.linspace(ang_r, ang_r + phi, 60)
ax.plot(A[0] + 0.55*np.cos(aa), A[1] + 0.55*np.sin(aa), color=MUTED, lw=1.1)
ax.annotate(r'$\phi$', (A[0] + 0.78*np.cos(ang_r + phi/2),
                        A[1] + 0.78*np.sin(ang_r + phi/2)),
            color=MUTED, fontsize=10, ha='center', va='center')
ax.plot([O[0]], [O[1]], 'o', color=INK, ms=5)
ax.annotate('$O$', O, textcoords='offset points', xytext=(-12, -6), color=INK, fontsize=10)
ax.plot([A[0]], [A[1]], 'o', color=INK, ms=3.5)
ax.set_xlim(-1.4, 4.0); ax.set_ylim(-1.35, 2.45)
ax.set_aspect('equal'); ax.axis('off')
```

::: derivation Torque equals $I\alpha$
Take one particle of mass $m_i$ at distance $r_i$. The tangential force on it
is, by Newton's second law, $F_i = m_i a_{ti} = m_i r_i\alpha$, because every
particle of a rigid body shares the same $\alpha$. The torque of this force
about the axis is

$$ \tau_i = F_i r_i = m_i r_i^{2}\alpha $$

Adding over all particles, the internal forces cancel in pairs (Newton's third
law), so the resultant external torque is

$$ \tau = \sum_i m_i r_i^{2}\alpha = \left(\sum_i m_i r_i^{2}\right)\alpha $$

$$ \tau = I\alpha $$

This is the rotational form of $F = ma$.
:::

::: example Worked example 1.3
**Problem.** A uniform rod of mass $2\ \text{kg}$ and length $1\ \text{m}$ is
hinged at one end and held horizontal. It is released from rest. Find its
initial angular acceleration and the initial linear acceleration of the free
end. Take $g = 9.8\ \text{m s}^{-2}$.

**Solution.** The weight acts at the centre of mass, $0.5\ \text{m}$ from the
hinge, so the torque about the hinge is

$$ \tau = Mg\frac{L}{2} = 2 \times 9.8 \times 0.5 = 9.8\ \text{N m} $$

About the end, $I = ML^{2}/3 = 2(1)^{2}/3 = 0.667\ \text{kg m}^{2}$. Hence

$$ \alpha = \frac{\tau}{I} = \frac{9.8}{0.667} = 14.7\ \text{rad s}^{-2} $$

The free end has $a_t = L\alpha = 1 \times 14.7 = 14.7\ \text{m s}^{-2}$, which
is **greater than $g$**. A coin resting on the far end of the rod is therefore
left behind when the rod is released.
:::

## 1.6 Work and power in rotational motion

When a torque $\tau$ turns a body through a small angle $d\theta$, the force
$F = \tau/r$ acts through an arc $ds = r\,d\theta$, so the work done is

$$ dW = F\,ds = \frac{\tau}{r}\,(r\,d\theta) = \tau\,d\theta $$

For a constant torque, $W = \tau\theta$. The **power** is the rate of doing this
work:

$$ P = \frac{dW}{dt} = \tau\frac{d\theta}{dt} = \tau\omega $$

the exact analogue of $P = Fv$. And since $\tau = I\alpha = I\,\omega\,d\omega/d\theta$,

$$ W = \int \tau\,d\theta = \int_{\omega_1}^{\omega_2} I\omega\,d\omega
= \tfrac{1}{2}I\omega_2^{2} - \tfrac{1}{2}I\omega_1^{2} $$

which is the **work–energy theorem for rotation**: the work done by the
resultant torque equals the change in rotational kinetic energy.

::: example Worked example 1.4
**Problem.** An electric motor at a rice mill in Jhapa delivers a constant
torque of $25\ \text{N m}$ while running at $1500$ rev min⁻¹. Find the power
output, and the work done in one minute.

**Solution.** $\omega = \dfrac{2\pi \times 1500}{60} = 50\pi = 157.1\ \text{rad s}^{-1}$.

$$ P = \tau\omega = 25 \times 157.1 = 3927\ \text{W} \approx 3.93\ \text{kW} $$

In $60\ \text{s}$, $W = Pt = 3927 \times 60 = 2.36 \times 10^{5}\ \text{J}$.
:::

## 1.7 Angular momentum; conservation of angular momentum

::: definition Angular momentum
The angular momentum of a particle about a point is the moment of its linear
momentum: $L = rp\sin\phi = mvr\sin\phi$. For a rigid body rotating about a
fixed axis, $L = I\omega$. Its SI unit is kg m² s⁻¹ (or J s).
:::

Differentiating $L = I\omega$ for a rigid body ($I$ constant about a fixed axis),

$$ \frac{dL}{dt} = I\frac{d\omega}{dt} = I\alpha = \tau $$

So **torque is the rate of change of angular momentum**, just as force is the
rate of change of linear momentum. Written this way the result is more general:
it holds even when $I$ changes.

::: key Principle of conservation of angular momentum
If the resultant external torque on a system is zero, then $dL/dt = 0$, so
$L = I\omega$ is constant:

$$ I_1\omega_1 = I_2\omega_2 $$

A body that reduces its moment of inertia must spin faster, and vice versa.
:::

```figure caption="Conservation of angular momentum, seen from above. Pulling the masses in reduces $I$, so $\omega$ rises to keep $L=I\omega$ fixed."
import numpy as np, matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 2, figsize=(5.0,2.6))
def panel(ax, arm, title, sub, nsweep):
    tt = np.linspace(0, 2*np.pi, 200)
    ax.plot(1.55*np.cos(tt), 1.55*np.sin(tt), color=GRID, lw=1.2)
    ax.fill(0.32*np.cos(tt), 0.32*np.sin(tt), color=ACCENT, alpha=0.25)
    ax.plot(0.32*np.cos(tt), 0.32*np.sin(tt), color=INK, lw=1.1)
    for s in (+1, -1):
        ax.plot([s*0.3, s*arm], [0, 0], color=INK, lw=1.6)
        ax.add_patch(plt.Circle((s*arm, 0), 0.20, facecolor='#A8271F',
                                edgecolor='none'))
    sw = np.linspace(np.radians(60), np.radians(60+nsweep), 60)
    ax.plot(1.15*np.cos(sw), 1.15*np.sin(sw), color='#0B6A62', lw=1.6)
    ax.annotate('', xy=(1.15*np.cos(sw[-1]), 1.15*np.sin(sw[-1])),
                xytext=(1.15*np.cos(sw[-5]), 1.15*np.sin(sw[-5])),
                arrowprops=dict(arrowstyle='-|>', color='#0B6A62', lw=1.6,
                                mutation_scale=12))
    ax.annotate(title, (0, -1.95), color=INK, fontsize=9.5, ha='center')
    ax.annotate(sub, (0, 1.75), color='#0B6A62', fontsize=9.5, ha='center')
    ax.set_xlim(-2.0, 2.0); ax.set_ylim(-2.3, 2.15)
    ax.set_aspect('equal'); ax.axis('off')
panel(axes[0], 1.35, 'arms out: large $I$', 'small $\\omega$', 50)
panel(axes[1], 0.55, 'arms in: small $I$', 'large $\\omega$', 150)
fig.subplots_adjust(wspace=0.02)
```

Everyday consequences, all examined regularly:

- An **ice skater or a dancer** spins faster on folding the arms in.
- A **diver** tucks to somersault quickly, then stretches out to slow the spin
  before entering the water.
- A **planet** moves faster when nearer the Sun; since gravity is a central
  force its torque about the Sun is zero. This is Kepler's second law.
- A spinning **top or a bicycle wheel** resists being tipped over, because
  tipping it would change the direction of $\vec{L}$.

::: caution Angular momentum is conserved, kinetic energy is not
When a skater pulls the arms in, $L$ stays the same but
$E_k = L^{2}/2I$ **increases** because $I$ falls. The extra energy comes from the
muscular work done in pulling the arms inwards against the outward (centrifugal)
effect. Conversely, when two rotating discs are coupled together, energy is lost
to friction while $L$ is conserved.
:::

::: example Worked example 1.5
**Problem.** A student sits on a frictionless rotating stool with arms
outstretched, holding weights. The moment of inertia of the system is
$6\ \text{kg m}^{2}$ and it rotates at $2\ \text{rad s}^{-1}$. He pulls his arms
in, reducing the moment of inertia to $2\ \text{kg m}^{2}$. Find the new angular
velocity and the change in kinetic energy.

**Solution.** No external torque acts about the vertical axis, so angular
momentum is conserved:

$$ I_1\omega_1 = I_2\omega_2 \Rightarrow 6 \times 2 = 2 \times \omega_2
\Rightarrow \omega_2 = 6\ \text{rad s}^{-1} $$

$$ E_1 = \tfrac{1}{2}(6)(2)^{2} = 12\ \text{J}, \qquad
E_2 = \tfrac{1}{2}(2)(6)^{2} = 36\ \text{J} $$

The kinetic energy increases by $24\ \text{J}$, supplied by the work the student
does in pulling the weights inwards.
:::

## Chapter summary

- For constant $\alpha$: $\omega = \omega_0 + \alpha t$,
  $\theta = \omega_0 t + \frac{1}{2}\alpha t^{2}$, $\omega^{2} = \omega_0^{2} + 2\alpha\theta$;
  and $s = r\theta$, $v = r\omega$, $a_t = r\alpha$, $a_c = r\omega^{2}$.
- Rotational kinetic energy $E_k = \frac{1}{2}I\omega^{2}$, where
  $I = \sum m_i r_i^{2} = \int r^{2}dm$ is the moment of inertia.
- Radius of gyration: $I = Mk^{2}$, so $k = \sqrt{I/M}$. Parallel axis:
  $I = I_{cm} + Md^{2}$; perpendicular axis (laminae): $I_z = I_x + I_y$.
- Uniform rod of mass $M$, length $L$: $I = ML^{2}/12$ about the centre and
  $ML^{2}/3$ about one end.
- Torque $\tau = rF\sin\phi$ and $\tau = I\alpha$, the rotational form of $F = ma$.
- Work $W = \tau\theta$, power $P = \tau\omega$, and
  $W = \frac{1}{2}I\omega_2^{2} - \frac{1}{2}I\omega_1^{2}$.
- Angular momentum $L = I\omega$ with $\tau = dL/dt$. If $\tau = 0$ then
  $I_1\omega_1 = I_2\omega_2$: angular momentum is conserved, but kinetic energy
  need not be.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The moment of inertia of a uniform rod of mass $M$ and length $L$ about an
   axis through one end and perpendicular to it is <span class="marks">[1]</span>
   (a) $ML^{2}/12$ (b) $ML^{2}/3$ (c) $ML^{2}/2$ (d) $ML^{2}$
2. The rotational analogue of mass is <span class="marks">[1]</span>
   (a) torque (b) angular velocity (c) moment of inertia (d) angular momentum
3. A body of moment of inertia $2\ \text{kg m}^{2}$ rotates at
   $3\ \text{rad s}^{-1}$. Its rotational kinetic energy is <span class="marks">[1]</span>
   (a) $3\ \text{J}$ (b) $6\ \text{J}$ (c) $9\ \text{J}$ (d) $18\ \text{J}$
4. A skater spinning with arms outstretched folds her arms in. Her angular
   velocity increases because <span class="marks">[1]</span>
   (a) her angular momentum increases (b) an external torque acts on her
   (c) her moment of inertia decreases while $L$ is constant
   (d) her kinetic energy is conserved
5. The power delivered by a torque $\tau$ at angular velocity $\omega$ is <span class="marks">[1]</span>
   (a) $\tau\theta$ (b) $\tau\omega$ (c) $I\omega$ (d) $\tau/\omega$

::: note Answers to Group A
**1.** (b) — integrating $x^{2}dm$ from $0$ to $L$ gives $ML^{2}/3$.
**2.** (c) — $I$ appears in $\tau = I\alpha$ exactly where $m$ appears in $F = ma$.
**3.** (c) — $E_k = \frac{1}{2}(2)(3)^{2} = 9\ \text{J}$.
**4.** (c) — no external torque, so $I\omega$ is fixed and $\omega$ must rise.
**5.** (b) — $P = dW/dt = \tau\,d\theta/dt = \tau\omega$.
:::

**Group B — Short answer (5 marks each)**

1. Define moment of inertia and radius of gyration. On what factors does the
   moment of inertia of a body depend? <span class="marks">[5]</span>
2. Derive the relation $\tau = I\alpha$ for a rigid body rotating about a fixed
   axis. <span class="marks">[5]</span>
3. A flywheel of mass $50\ \text{kg}$ in the form of a uniform disc of radius
   $0.40\ \text{m}$ rotates at $300$ rev min⁻¹. Calculate its kinetic energy and
   the constant torque needed to stop it in $10\ \text{s}$. <span class="marks">[5]</span>
4. A disc of moment of inertia $2\ \text{kg m}^{2}$ rotating at
   $10\ \text{rad s}^{-1}$ is suddenly coupled to a stationary coaxial disc of
   moment of inertia $3\ \text{kg m}^{2}$. Find the common angular velocity and
   the loss of kinetic energy. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Outline: state $I = \sum m_i r_i^{2}$ (unit kg m², dimensions $[ML^{2}]$)
and $k = \sqrt{I/M}$. $I$ depends on the total mass, on the distribution of that
mass about the axis, and on the position and direction of the axis itself.

**2.** Outline: for particle $i$, $F_i = m_i r_i\alpha$, so
$\tau_i = m_i r_i^{2}\alpha$; sum over all particles (internal torques cancel in
pairs) to get $\tau = (\sum m_i r_i^{2})\alpha = I\alpha$.

**3.** $I = \frac{1}{2}MR^{2} = \frac{1}{2}(50)(0.40)^{2} = 4\ \text{kg m}^{2}$;
$\omega = 2\pi(300)/60 = 31.42\ \text{rad s}^{-1}$.
$E_k = \frac{1}{2}(4)(31.42)^{2} = 1974\ \text{J}$.
Retardation $\alpha = 31.42/10 = 3.142\ \text{rad s}^{-2}$, so
$\tau = I\alpha = 4 \times 3.142 = 12.6\ \text{N m}$.

**4.** Angular momentum is conserved: $2 \times 10 = (2+3)\omega$, so
$\omega = 4\ \text{rad s}^{-1}$.
$E_1 = \frac{1}{2}(2)(10)^{2} = 100\ \text{J}$,
$E_2 = \frac{1}{2}(5)(4)^{2} = 40\ \text{J}$; loss $= 60\ \text{J}$, dissipated
as heat by friction between the coupled discs.
:::

**Group C — Long answer (8 marks each)**

1. (a) Define moment of inertia and radius of gyration. <span class="marks">[3]</span>
   (b) Derive an expression for the moment of inertia of a uniform rod of mass
   $M$ and length $L$ about an axis through its centre and perpendicular to its
   length, and hence, using the parallel axis theorem, about an axis through one
   end. <span class="marks">[5]</span>
2. (a) Show that the kinetic energy of a rigid body rotating about a fixed axis
   is $\frac{1}{2}I\omega^{2}$. <span class="marks">[3]</span>
   (b) A flywheel of mass $100\ \text{kg}$ and radius of gyration $0.50\ \text{m}$
   rotates at $600$ rev min⁻¹. A constant retarding torque brings it to rest in
   $40\ \text{s}$. Find its moment of inertia, its initial kinetic energy, the
   retarding torque, and the number of revolutions it makes before stopping. <span class="marks">[5]</span>

::: note Answer to Group C question 2(b)
$I = Mk^{2} = 100 \times (0.50)^{2} = 25\ \text{kg m}^{2}$.

$\omega_0 = 2\pi(600)/60 = 20\pi = 62.83\ \text{rad s}^{-1}$, so
$E_k = \frac{1}{2}(25)(62.83)^{2} = 4.93 \times 10^{4}\ \text{J}$.

$\alpha = (0 - 62.83)/40 = -1.571\ \text{rad s}^{-2}$, so the retarding torque is
$|\tau| = I|\alpha| = 25 \times 1.571 = 39.3\ \text{N m}$.

$\theta = \frac{1}{2}(\omega_0 + 0)t = \frac{1}{2}(62.83)(40) = 1257\ \text{rad}$,
so the number of revolutions $= 1257/2\pi = 200$.
:::
