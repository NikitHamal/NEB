---
subject: Physics
grade: CEE
unit: 3
title: Rotational Dynamics
hours: 1
area: Mechanics
---

Rotational dynamics is linear dynamics re-written for turning: force becomes
torque, mass becomes moment of inertia, momentum becomes angular momentum. Of the
**10 Mechanics questions** (official weightage), we estimate about **1** comes from
this chapter. The MEC syllabus limits moment of inertia to the **uniform rigid rod**,
so expect a rod about its centre or its end, a radius of gyration, a torque or
rotational-power calculation, or a conservation-of-angular-momentum situation such as
a spinning skater.

::: key What the paper asks from this chapter
- Rod: $I = ML^2/12$ about a perpendicular axis through the centre, $ML^2/3$ through an end; the ratio is 4.
- Radius of gyration $k = \sqrt{I/M}$: $L/(2\sqrt{3})$ about the centre, $L/\sqrt{3}$ about an end.
- Parallel-axis theorem $I = I_{cm} + Md^2$; what $I$ depends on (and that it does not depend on $\omega$).
- Torque $\tau = rF\sin\theta$ and $\tau = I\alpha$; rotational work $\tau\theta$, power $\tau\omega$, kinetic energy $\frac{1}{2}I\omega^2$.
- Angular momentum $L = I\omega$, $\tau = dL/dt$; with no external torque $I_1\omega_1 = I_2\omega_2$.
- $K = L^2/2I$: when a skater pulls in, $\omega$ and $K$ rise while $L$ stays the same.
:::

## 3.1 Moment of inertia of a uniform rod and radius of gyration

### Moment of inertia

::: definition Moment of inertia
The **moment of inertia** of a body about an axis is the sum of the products of the
mass of each particle and the square of its perpendicular distance from the axis:
$I = \sum m_ir_i^2$ (or $\int r^2\,dm$). It measures the body's opposition to a
change in its rotational motion about that axis. SI unit kg m²; dimensions $[ML^2]$.
:::

$I$ plays in rotation the part that mass plays in translation. Unlike mass, it is not
fixed for a body: it depends on

1. the **mass** of the body,
2. how that mass is **distributed** about the axis (mass far from the axis counts
   much more, because of $r^2$),
3. the **position and orientation of the axis**.

It does **not** depend on the angular velocity or on the torque applied (for a rigid
body).

### The uniform rod

Take a thin uniform rod of mass $M$ and length $L$, so its mass per unit length is
$M/L$. A slice of length $dx$ at distance $x$ from the axis has mass
$dm = (M/L)\,dx$ and contributes $x^2\,dm$.

- **Axis through the centre, perpendicular to the rod:** $x$ runs from $-L/2$ to
  $+L/2$, and $I = \frac{M}{L}\int x^2\,dx = \frac{M}{L}\cdot\frac{L^3}{12}$.
- **Axis through one end, perpendicular to the rod:** $x$ runs from 0 to $L$, and
  $I = \frac{M}{L}\cdot\frac{L^3}{3}$.

$$ I_{centre} = \frac{ML^2}{12}, \qquad I_{end} = \frac{ML^2}{3} = 4\,I_{centre} $$

| Axis of the rod (mass $M$, length $L$) | Moment of inertia | Radius of gyration $k$ |
|---|---|---|
| Perpendicular, through the centre | $ML^2/12$ (the least for a perpendicular axis) | $L/(2\sqrt{3}) \approx 0.289L$ |
| Perpendicular, through one end | $ML^2/3$ | $L/\sqrt{3} \approx 0.577L$ |
| Perpendicular, at distance $d$ from the centre | $ML^2/12 + Md^2$ | $\sqrt{L^2/12 + d^2}$ |
| Through the centre, at angle $\theta$ to the rod | $(ML^2/12)\sin^2\theta$ | $(L\sin\theta)/(2\sqrt{3})$ |
| Along the rod itself (thin rod) | $\approx 0$ | $\approx 0$ |

```figure caption="A uniform rod about two perpendicular axes. The dot marks the radius of gyration — the distance at which the whole mass, put at one point, would have the same moment of inertia."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,3.0))
L = 5.0
for y0, xa, k, lab1, lab2 in [(2.3, L/2, L/np.sqrt(12), 'axis through the centre', 'I = ML²/12,  k = 0.29 L'),
                              (0.4, 0.0, L/np.sqrt(3), 'axis through one end', 'I = ML²/3,  k = 0.58 L')]:
    ax.plot([0, L], [y0, y0], color=ACCENT, lw=6, solid_capstyle='butt', zorder=3)
    ax.plot([xa, xa], [y0-0.65, y0+0.65], color=INK, lw=1.0, ls=(0,(4,2)), zorder=4)
    ax.plot([xa+k], [y0], 'o', color='#A8271F', ms=6.5, zorder=5)
    ax.annotate('', xy=(xa+k, y0+0.32), xytext=(xa, y0+0.32),
                arrowprops=dict(arrowstyle='<->', color='#A8271F', lw=1.0, shrinkA=0, shrinkB=0))
    ax.text(xa+k/2, y0+0.42, 'k', color='#A8271F', fontsize=9.5, ha='center', va='bottom')
    ax.text(5.4, y0+0.16, lab1, fontsize=8.5, color=MUTED, va='bottom')
    ax.text(5.4, y0-0.12, lab2, fontsize=8.5, color=INK, va='top')
ax.annotate('', xy=(L, -0.55), xytext=(0, -0.55),
            arrowprops=dict(arrowstyle='<->', color=MUTED, lw=0.9, shrinkA=0, shrinkB=0))
ax.text(L/2, -0.65, 'length L, mass M', fontsize=8.5, color=MUTED, ha='center', va='top')
ax.set_xlim(-0.4, 9.6); ax.set_ylim(-1.2, 3.2); ax.axis('off')
```

### Two theorems

- **Parallel-axis theorem:** $I = I_{cm} + Md^2$, where $I_{cm}$ is about a parallel
  axis through the centre of mass and $d$ is the distance between the axes. The
  centre-of-mass axis therefore gives the **least** moment of inertia of all parallel
  axes. Check: $\frac{ML^2}{12} + M\left(\frac{L}{2}\right)^2 = \frac{ML^2}{3}$.
- **Perpendicular-axis theorem** (plane lamina only): $I_z = I_x + I_y$, where $x$ and
  $y$ lie in the plane of the lamina and $z$ is perpendicular to it, all three
  meeting at one point.

### Radius of gyration

::: definition Radius of gyration
The **radius of gyration** $k$ of a body about an axis is the distance from the axis
at which, if the whole mass of the body were concentrated, it would have the same
moment of inertia: $I = Mk^2$, so $k = \sqrt{I/M}$. It is the root-mean-square
distance of the body's particles from the axis. SI unit: metre.
:::

$k$ depends on the axis and on the distribution of mass, but **not** on the total
mass (doubling the mass of a rod doubles $I$ and leaves $k$ the same).

For reference, when a question gives a wheel instead of a rod: ring about its axis
$MR^2$ ($k = R$), disc $MR^2/2$, solid sphere about a diameter $\frac{2}{5}MR^2$,
thin spherical shell $\frac{2}{3}MR^2$. For the same mass and radius a ring has a
larger $I$ than a disc, because all its mass is at the rim — the reason a flywheel
has a heavy rim.

::: example Worked example 3.1 — a rod and a dumb-bell
**Problem.** (a) A uniform rod of mass 1 kg and length 1.2 m. Find $I$ about
perpendicular axes through its centre and through one end, and $k$ about the end.
(b) Two 2 kg balls are fixed at the ends of a light rod 1 m long. Find $I$ about a
perpendicular axis through the centre.

**Solution.** (a) $I_c = 1(1.2)^2/12 = 0.12\ \text{kg m}^2$;
$I_e = 4I_c = 0.48\ \text{kg m}^2$; $k_e = L/\sqrt{3} = 1.2/1.732 = 0.69\ \text{m}$.
(b) Each ball is 0.5 m from the axis: $I = 2\times2(0.5)^2 = 1.0\ \text{kg m}^2$.
A uniform rod of the same total mass (4 kg) would have only
$4(1)^2/12 = 0.33\ \text{kg m}^2$ — mass at the ends counts more.
:::

::: caution Square roots and squares
$I_{end} = 4I_{centre}$, but $k_{end} = 2k_{centre}$ (because $k \propto \sqrt{I}$).
And the parallel-axis theorem adds $Md^2$ only from the **centre-of-mass** axis:
you cannot go from the end axis to another axis by adding $Md^2$ — go back to the
centre first.
:::

## 3.2 Torque, rotational work, kinetic energy and power

### Torque

::: definition Torque
The **torque** (moment of a force) about an axis is the turning effect of the force:
$\vec\tau = \vec r\times\vec F$, of magnitude $\tau = rF\sin\theta = F\,r_\perp$, where
$r_\perp = r\sin\theta$ is the perpendicular distance of the line of action of the
force from the axis (the **moment arm**). SI unit N m; dimensions $[ML^2T^{-2}]$.
:::

```figure caption="Torque about O: only the moment arm $r_\perp = r\sin\theta$ counts. A force whose line of action passes through O (θ = 0) has no turning effect at all."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6,3.0))
th = np.radians(35); P = np.array([3.0, 0.0]); d = np.array([np.cos(th), np.sin(th)])
foot = P + (-(P @ d))*d
ax.plot([-0.2, 3.4], [0, 0], color=MUTED, lw=5, solid_capstyle='round', alpha=0.45, zorder=1)
ax.plot([0], [0], 'o', color=INK, ms=7, zorder=5)
ax.text(-0.1, 0.22, 'O (axis)', fontsize=9, color=INK, ha='center', va='bottom')
ax.annotate('', xy=P, xytext=(0, 0), arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.4,
            shrinkA=4, shrinkB=0, mutation_scale=11), zorder=4)
ax.text(1.6, 0.14, 'r', fontsize=10, color=INK, ha='center', va='bottom')
ax.plot([foot[0], P[0]], [foot[1], P[1]], color=MUTED, lw=1.0, ls=(0, (4, 2)), zorder=2)
ax.annotate('', xy=P + 1.7*d, xytext=P, arrowprops=dict(arrowstyle='-|>', color='#A8271F',
            lw=2.0, shrinkA=0, shrinkB=0, mutation_scale=13), zorder=4)
ax.text(*(P + 1.7*d + np.array([0.12, 0.0])), 'F', fontsize=10, color='#A8271F', ha='left', va='center')
ax.plot([0, foot[0]], [0, foot[1]], color=ACCENT, lw=1.8, zorder=3)
q = 0.16; e1 = -foot/np.linalg.norm(foot); e2 = d
c = foot + q*e1; ax.plot([c[0], c[0]+q*e2[0], foot[0]+q*e2[0]], [c[1], c[1]+q*e2[1], foot[1]+q*e2[1]], color=ACCENT, lw=0.9)
ax.text(0.05, -1.0, 'r⊥ = r sinθ', fontsize=9, color=ACCENT, ha='right', va='center')
a = np.linspace(0, th, 30); ax.plot(P[0] + 0.55*np.cos(a), 0.55*np.sin(a), color=INK, lw=0.9)
ax.text(P[0] + 0.72, 0.12, 'θ', fontsize=10, color=INK)
ax.text(2.3, -0.62, 'line of action', fontsize=8.5, color=MUTED, ha='left', va='center')
ax.set_xlim(-1.6, 5.0); ax.set_ylim(-1.7, 1.45); ax.set_aspect('equal'); ax.axis('off')
```

- The direction of $\vec\tau$ is along the axis, given by the right-hand rule
  (anticlockwise torque is taken positive by convention).
- A force through the axis, or along $\vec r$, gives **zero** torque. A door handle is
  far from the hinges so that a small force gives a large torque.
- A **couple** (two equal, opposite, parallel forces $F$ a distance $d$ apart) has
  zero net force and torque $Fd$ about **every** point: it turns without translating.
- Torque and work share the unit N m and the dimensions $[ML^2T^{-2}]$, but torque is
  a vector and is never written in joules.

### Newton's second law for rotation

For a rigid body turning about a fixed axis, $\tau = I\alpha$ — the rotational form
of $F = ma$. For constant $\alpha$ the rotational equations of motion are exact
copies of the linear ones:

| Linear | Rotational | Link |
|---|---|---|
| displacement $s$ | angle $\theta$ (rad) | $s = r\theta$ |
| velocity $v$ | angular velocity $\omega$ | $v = r\omega$ |
| acceleration $a$ | angular acceleration $\alpha$ | $a_t = r\alpha$ |
| mass $m$ | moment of inertia $I$ | $I = \sum mr^2$ |
| force $F = ma$ | torque $\tau = I\alpha$ | $\tau = rF\sin\theta$ |
| momentum $p = mv$ | angular momentum $L = I\omega$ | $L = rp\sin\theta$ |
| $v = u + at$ | $\omega = \omega_0 + \alpha t$ | |
| $s = ut + \frac{1}{2}at^2$ | $\theta = \omega_0t + \frac{1}{2}\alpha t^2$ | |
| $v^2 = u^2 + 2as$ | $\omega^2 = \omega_0^2 + 2\alpha\theta$ | |
| work $W = Fs$ | work $W = \tau\theta$ | |
| kinetic energy $\frac{1}{2}mv^2$ | kinetic energy $\frac{1}{2}I\omega^2$ | |
| power $P = Fv$ | power $P = \tau\omega$ | |

Number of revolutions $n = \theta/2\pi$; $\omega = 2\pi f = 2\pi N/60$ for $N$ rpm.

### Rotational work, kinetic energy and power

- **Work** done by a constant torque turning a body through angle $\theta$:
  $W = \tau\theta$ (in radians).
- **Rotational kinetic energy:** $K = \frac{1}{2}I\omega^2$ — the sum of
  $\frac{1}{2}mv^2$ over all particles, with $v = r\omega$.
- **Work–energy theorem for rotation:** net work by torques
  $= \frac{1}{2}I\omega^2 - \frac{1}{2}I\omega_0^2$.
- **Power:** $P = \tau\omega$. A motor that gives torque 20 N m at 300 rpm delivers
  $20\times2\pi\times5 = 628\ \text{W}$.
- **Rolling without slipping** (wheel, ball): $v = R\omega$ and
  $K = \frac{1}{2}mv^2 + \frac{1}{2}I\omega^2 = \frac{1}{2}mv^2\left(1 + \frac{k^2}{R^2}\right)$.
  Part of the energy is always rotational, so a rolling body accelerates down a slope
  more slowly than one sliding without friction.

::: example Worked example 3.2 — torque, work and energy
**Problem.** A constant torque of 10 N m acts for 5 s on a wheel with
$I = 2\ \text{kg m}^2$, starting from rest. Find the angular acceleration, the final
angular velocity, the angle turned and the kinetic energy gained.

**Solution.** $\alpha = \tau/I = 5\ \text{rad s}^{-2}$; $\omega = \alpha t = 25\ \text{rad s}^{-1}$;
$\theta = \frac{1}{2}\alpha t^2 = 62.5\ \text{rad}$;
$K = \frac{1}{2}I\omega^2 = \frac{1}{2}(2)(625) = 625\ \text{J}$. Check by work:
$\tau\theta = 10\times62.5 = 625\ \text{J}$.
:::

::: example Worked example 3.3 — a rod swinging down
**Problem.** A uniform rod of length 1.2 m is pivoted freely at one end and released
from rest in the horizontal position ($g = 10\ \text{m s}^{-2}$). Find (a) its
angular acceleration just after release and (b) its angular velocity as it passes
the vertical.

**Solution.** (a) The weight acts at the centre, $L/2$ from the pivot:
$\alpha = \frac{Mg(L/2)}{ML^2/3} = \frac{3g}{2L} = 12.5\ \text{rad s}^{-2}$. (The free
end then starts with acceleration $\alpha L = \frac{3}{2}g$ — **more than** $g$.)
(b) The centre falls $L/2$: $Mg\frac{L}{2} = \frac{1}{2}\cdot\frac{ML^2}{3}\omega^2$, so
$\omega = \sqrt{3g/L} = \sqrt{25} = 5\ \text{rad s}^{-1}$; the tip moves at
$\omega L = 6\ \text{m s}^{-1}$.
:::

::: tip Rods in a hurry
Rod about its end: $I = ML^2/3$, weight acting at $L/2$. Released from horizontal:
$\alpha = 3g/2L$, $\omega_{bottom} = \sqrt{3g/L}$, tip speed $\sqrt{3gL}$. The mass
cancels in all three — if an option contains $M$, it is wrong.
:::

## 3.3 Angular momentum and its conservation

::: definition Angular momentum
The **angular momentum** of a particle about a point is the moment of its linear
momentum: $\vec L = \vec r\times\vec p$, of magnitude $L = mvr\sin\theta = mv\,r_\perp$.
For a rigid body rotating about a fixed axis, $L = I\omega$. SI unit kg m² s⁻¹
$=$ J s; dimensions $[ML^2T^{-1}]$, the same as Planck's constant.
:::

Even a particle moving in a **straight line** has angular momentum about a point
not on that line: $L = mvd$, where $d$ is the perpendicular distance of the line from
the point. If no force acts, $v$ and $d$ stay fixed, so $L$ is constant.

**Torque and angular momentum.** Newton's second law for rotation in its general
form is

$$ \vec\tau = \frac{d\vec L}{dt} $$

A torque acting for a time $\Delta t$ gives an **angular impulse**
$\tau\,\Delta t = \Delta L$.

::: key Principle of conservation of angular momentum
If the net external torque on a system is zero, its total angular momentum is
constant: $I_1\omega_1 = I_2\omega_2$. A body that changes its own shape (and so its
$I$) changes its angular velocity in inverse proportion.
:::

| Situation | What happens and why |
|---|---|
| Ice skater or ballet dancer pulls the arms in | $I$ falls, so $\omega$ rises; arms out again slows the spin |
| Diver or gymnast tucks the body | $I$ falls, more somersaults in the air; opens out to slow before entering the water |
| Person on a rotating stool pulls dumb-bells inward | the stool spins faster |
| Planet nearer the Sun moves faster | gravity is a central force (zero torque about the Sun); $mvr$ constant — this is Kepler's second law (equal areas in equal times) |
| A star collapses into a neutron star | its radius shrinks enormously, so it spins very fast |
| If the Earth shrank with no change of mass | $I \propto R^2$, so the day would shorten as $R^2$ |
| Helicopter tail rotor | its sideways thrust supplies the torque that stops the body spinning opposite to the main rotor |

**Energy is not conserved in the same way.** Since $K = \frac{L^2}{2I}$, with $L$
fixed the kinetic energy is inversely proportional to $I$. When the skater pulls in,
$K$ **increases** — the extra energy is the work her muscles do pulling the arms in.
When a non-rotating disc is dropped onto a spinning one and they turn together, $L$
is conserved but kinetic energy is **lost** (to friction between the discs), just as
in a perfectly inelastic collision.

::: example Worked example 3.4 — a skater and the Earth
**Problem.** (a) A skater spinning at 2 rad s⁻¹ with $I = 4\ \text{kg m}^2$ pulls
her arms in to make $I = 1.6\ \text{kg m}^2$. Find the new angular velocity and the
ratio of final to initial kinetic energy. (b) If the Earth contracted to half its
radius with no change of mass, how long would a day be?

**Solution.** (a) $\omega_2 = I_1\omega_1/I_2 = 4(2)/1.6 = 5\ \text{rad s}^{-1}$.
$K_2/K_1 = I_1/I_2 = 2.5$ (from 8 J to 20 J). (b) $I \propto R^2$ falls to $\frac{1}{4}$,
so $\omega$ becomes 4 times and the period $T = 24/4 = 6$ hours.
:::

::: example Worked example 3.5 — two discs coupled
**Problem.** A disc with $I_1 = 2\ \text{kg m}^2$ spins at 10 rad s⁻¹. A second disc,
$I_2 = 3\ \text{kg m}^2$, at rest, is dropped onto it on the same axle and they turn
together. Find the common angular velocity and the kinetic energy lost.

**Solution.** $\omega = I_1\omega_1/(I_1 + I_2) = 20/5 = 4\ \text{rad s}^{-1}$.
$K_1 = \frac{1}{2}(2)(100) = 100\ \text{J}$; $K_2 = \frac{1}{2}(5)(16) = 40\ \text{J}$:
60 J is lost — the fraction $I_2/(I_1 + I_2) = 0.6$.
:::

::: caution Conserved does not mean unchanged
In a spin with no external torque, $L$ is constant but $\omega$ and $K$ both change
whenever $I$ changes. Options that say "angular velocity unchanged" or "kinetic
energy unchanged" for a skater pulling in her arms are the classic distractors.
:::


::: caution Trap — same mass and radius does not mean same moment of inertia
About an axis through the centre: **ring** MR² > **disc** ½MR² > **solid sphere** (2/5)MR². What matters is how far the mass sits from the axis, not merely how much mass there is — hence in a race down an incline the solid sphere wins and the ring comes last, all with the same M and R. Also keep separate: **radius of gyration** (k, defined by I = Mk²) is not a physical radius of the body.
:::

```photogrid label="3.1" cols="2" ratio="1.2" caption="Rotation made numerical. (a) The platter of a hard disk turns as one rigid body, so every point has the same angular speed but a different linear speed. (b) At 7,200 rpm the angular speed is omega = 2 pi f = 754 rad/s. A point at 10 mm from the axis moves at v = omega r = 7.5 m/s, one at 20 mm at 15.1 m/s and one on the 32.5 mm rim at 24.5 m/s. The centripetal acceleration omega^2 r at the rim is 18,476 m/s^2, about 1,885 g. Treating an assumed 12 g platter as a solid disc, I = (1/2) m r^2 = 6.34e-06 kg m^2 and the rotational kinetic energy (1/2) I omega^2 is 1.80 J."
@ photo id="sci10/hdd" cap="A hard-disk platter spinning at 7,200 revolutions per minute"
fit 1.2
focus 0.5 0.5
@ svg cap="Linear speed and acceleration at three radii, 7,200 rpm"
import math
w = 2 * math.pi * 7200 / 60; m, R = 0.012, 0.0325
r = [0.010, 0.020, 0.0325]; v = [w * x for x in r]; ac = w * w * R
I = 0.5 * m * R * R; ke = 0.5 * I * w * w
assert abs(w - 753.98) < 0.01 and abs(v[2] - 24.50) < 0.01 and abs(ac - 18474) < 5 and abs(ke - 0.5 * 0.5 * m * (v[2]) ** 2) < 1e-9
facts = dict(w="%.0f" % w, v1="%.1f" % v[0], v2="%.1f" % v[1], v3="%.1f" % v[2], ac="{:,.0f}".format(ac), gees="{:,.0f}".format(ac / 9.8), I="%.2e" % I, ke="%.2f" % ke)
f = Fig(300, 236)
f.text(150, 14, "omega = %.0f rad/s  (same for every point)" % w, size=10.5, color=NAVY, bold=True)
cx, cy = 86, 104
for i, rr in enumerate(r):
    pass
f.circle(cx, cy, r[2] / R * 62, fill=BLUE, stroke=NAVY, sw=1.6); f.circle(cx, cy, 4, fill=NAVY, stroke=NAVY)
cols = [TEAL, AMBER, RED]
for i, rr in enumerate(r):
    x = cx + rr / R * 62
    f.line(cx, cy, x, cy, color=cols[i], sw=1.2, dash=True); f.circle(x, cy, 3.5, fill=cols[i], stroke=cols[i])
    f.arrow([(x, cy), (x, cy - v[i] * 1.8)], color=cols[i], sw=2)
f.text(214, 50, "10 mm", size=10.5, color=TEAL, bold=True); f.text(214, 66, "%.1f m/s" % v[0], size=10.5, color=TEAL)
f.text(214, 88, "20 mm", size=10.5, color=AMBER, bold=True); f.text(214, 104, "%.1f m/s" % v[1], size=10.5, color=AMBER)
f.text(214, 126, "32.5 mm", size=10.5, color=RED, bold=True); f.text(214, 142, "%.1f m/s" % v[2], size=10.5, color=RED)
f.text(150, 188, "arrows: linear speed, same scale", size=10.5, color=SLATE)
f.text(150, 204, "rim: omega^2 r = {:,.0f} m/s^2 = {:,.0f} g".format(ac, ac / 9.8), size=10.5, color=NAVY, bold=True)
f.text(150, 220, "KE = (1/2) I omega^2 = %.2f J (12 g, assumed)" % ke, size=10.5, color=NAVY, bold=True)
```

```photogrid label="3.2" cols="2" ratio="1.2" caption="Spinning faster by pulling in the arms. (a) A skater starts a spin with arms and free leg extended and then draws them in. (b) With no external torque the angular momentum L = I w is constant. The cell takes a moment of inertia of 3.0 kg m2 with arms out and 0.9 kg m2 with arms in, and a starting rate of 1.5 turns per second. Then L stays at 28.3 kg m2/s and the rate rises to 5.0 turns per second. The kinetic energy rises from 133 J to 444 J, a factor of 3.33: the extra energy is not free, it comes from the work the skater does against the (apparent) outward pull as the arms move in."
@ photo id="ceephy3/skater" cap="A figure skater in a spin"
fit 1.2
focus 0.5 0.4
@ svg cap="Conservation of angular momentum in a spin"
import math
I1, I2, f1 = 3.0, 0.9, 1.5
w1 = 2 * math.pi * f1
L = I1 * w1
w2 = L / I2
f2 = w2 / (2 * math.pi)
K1, K2 = 0.5 * I1 * w1 ** 2, 0.5 * I2 * w2 ** 2
assert round(f2, 1) == 5.0 and round(K1) == 133 and round(K2) == 444
f = Fig(300, 236)
f.text(150, 12, "L = I w stays at %.1f kg m2/s" % L, size=10.5, color=NAVY, bold=True)
f.text(150, 30, "spin rate, turns per second", size=10, color=SLATE, bold=True)
hbars(f, [("arms out", f1), ("arms in", f2)], vmax=5.2, fmt="%.1f", x0=60, y0=38, bw=170, gap=28)
f.text(150, 112, "kinetic energy, joules", size=10, color=SLATE, bold=True)
hbars(f, [("arms out", K1), ("arms in", K2)], vmax=470, fmt="%.0f", x0=60, y0=120, bw=170, gap=28,
      colors=[(SAND, AMBER), (ROSE, RED)])
f.text(150, 196, "I falls from %.1f to %.1f kg m2 (x%.2f)" % (I1, I2, I2 / I1), size=10.5, color=NAVY, bold=True)
f.text(150, 214, "energy rises x%.2f: the skater's muscles" % (K2 / K1), size=10, color=SLATE, bold=True)
f.text(150, 228, "do the extra work pulling the arms in", size=10, color=SLATE, bold=True)
facts = dict(L=L, f2=f2, K1=K1, K2=K2, r=K2 / K1)
```

## Formula and fact sheet

| Quantity | Formula | SI unit and dimensions |
|---|---|---|
| Moment of inertia | $I = \sum mr^2 = Mk^2$ | kg m², $[ML^2]$ |
| Rod, centre (perpendicular) | $ML^2/12$; $k = L/(2\sqrt{3}) = 0.289L$ | |
| Rod, end (perpendicular) | $ML^2/3$; $k = L/\sqrt{3} = 0.577L$ | |
| Rod, distance $d$ from centre | $ML^2/12 + Md^2$ | |
| Rod through centre at angle $\theta$ | $(ML^2/12)\sin^2\theta$ | |
| Parallel / perpendicular axes | $I = I_{cm} + Md^2$; lamina $I_z = I_x + I_y$ | |
| Torque | $\tau = rF\sin\theta = Fr_\perp = I\alpha$; couple $Fd$ | N m, $[ML^2T^{-2}]$ |
| Rotational kinematics | $\omega = \omega_0 + \alpha t$; $\theta = \omega_0t + \frac{1}{2}\alpha t^2$; $\omega^2 = \omega_0^2 + 2\alpha\theta$ | rad s⁻¹, rad s⁻² |
| Rotational work and power | $W = \tau\theta$; $P = \tau\omega$ | J; W |
| Rotational KE | $K = \frac{1}{2}I\omega^2 = L^2/2I$ | J |
| Rolling | $K = \frac{1}{2}mv^2(1 + k^2/R^2)$, $v = R\omega$ | |
| Angular momentum | $L = I\omega = mvr\sin\theta$; $\tau = dL/dt$; $\tau\Delta t = \Delta L$ | J s, $[ML^2T^{-1}]$ |
| Conservation | $\tau_{ext} = 0$: $I_1\omega_1 = I_2\omega_2$ | |
| Rod released from horizontal, pivot at end | $\alpha_0 = 3g/2L$; $\omega_{vertical} = \sqrt{3g/L}$; tip speed $\sqrt{3gL}$ | |
| Coupled discs | $\omega = I_1\omega_1/(I_1 + I_2)$; KE fraction lost $I_2/(I_1 + I_2)$ | |

## Chapter summary

- Moment of inertia $I = \sum mr^2$ depends on the mass, its distribution and the
  axis — not on the angular velocity; it is the rotational analogue of mass.
- Uniform rod: $ML^2/12$ about the centre, $ML^2/3$ about an end; the centre gives the
  least $I$ of all parallel axes ($I = I_{cm} + Md^2$).
- Radius of gyration $k = \sqrt{I/M}$: $L/(2\sqrt{3})$ about the centre and $L/\sqrt{3}$
  about an end; $k$ doubles when $I$ quadruples.
- Torque $\tau = rF\sin\theta$ (unit N m, never joule) and $\tau = I\alpha$; a force
  through the axis gives no torque; a couple turns without translating.
- Rotational work $\tau\theta$, power $\tau\omega$, kinetic energy $\frac{1}{2}I\omega^2$;
  rotational equations of motion mirror the linear ones.
- Angular momentum $L = I\omega = mvr\sin\theta$ (J s); $\tau = dL/dt$.
- With zero external torque $I\omega$ is constant: the skater, the diver, planets
  moving faster near the Sun; $K = L^2/2I$ rises when $I$ falls.

## Practice questions

**Set A — Recall (21 questions)**

1. The SI unit of moment of inertia is
   (a) kg m⁻² (b) kg m² (c) kg m s⁻¹ (d) N m
2. The moment of inertia of a thin uniform rod of mass M and length L about an axis perpendicular to it through its centre is
   (a) $ML^{2}/12$ (b) $ML^{2}/3$ (c) $ML^{2}/2$ (d) $ML^{2}$
3. The moment of inertia of a thin uniform rod of mass M and length L about an axis perpendicular to it through one end is
   (a) $ML^{2}/12$ (b) $ML^{2}/4$ (c) $ML^{2}/3$ (d) $ML^{2}/6$
4. The radius of gyration of a thin uniform rod of length L about a perpendicular axis through its centre is
   (a) $L/\sqrt{3}$ (b) $L/12$ (c) $L/2$ (d) $L/(2\sqrt{3})$
5. The moment of inertia of a rigid body does NOT depend on
   (a) its angular velocity (b) its mass (c) the distribution of its mass (d) the position of the axis of rotation
6. According to the parallel-axis theorem, the moment of inertia about an axis at distance d from a parallel axis through the centre of mass is
   (a) $I_{cm} - Md^{2}$ (b) $I_{cm} + Md^{2}$ (c) $I_{cm} + Md$ (d) $I_{cm}Md^{2}$
7. In rotational motion, the quantity that plays the part of mass is
   (a) torque (b) angular momentum (c) moment of inertia (d) angular velocity
8. Torque is the rotational analogue of
   (a) force (b) momentum (c) work (d) power
9. The dimensional formula of torque is
   (a) [MLT⁻²] (b) [ML²T⁻¹] (c) [ML²T⁻³] (d) [ML²T⁻²]
10. The SI unit of angular momentum is
   (a) N m (b) J s⁻¹ (c) J s (d) kg m s⁻¹
11. The rotational kinetic energy of a body of moment of inertia I and angular velocity ω is
   (a) $\frac{1}{2}I\omega^{2}$ (b) $I\omega^{2}$ (c) $\frac{1}{2}I^{2}\omega$ (d) $\frac{1}{2}I\omega$
12. The power delivered by a torque τ to a body rotating at angular velocity ω is
   (a) $\tau/\omega$ (b) $\frac{1}{2}\tau\omega^{2}$ (c) $\tau\omega$ (d) $\tau\omega^{2}$
13. The work done by a constant torque τ in turning a body through an angle θ is
   (a) $\tau/\theta$ (b) $\tau\theta$ (c) $\frac{1}{2}\tau\theta^{2}$ (d) $\tau\theta^{2}$
14. The angular momentum of a system is conserved when
   (a) the net external torque on it is zero (b) the net external force on it is zero (c) its kinetic energy is constant (d) its moment of inertia is constant
15. The rate of change of angular momentum of a body equals
   (a) its moment of inertia (b) its angular velocity (c) the net external torque on it (d) its rotational kinetic energy
16. An ice skater spinning on one toe pulls her arms close to her body. Her angular velocity
   (a) decreases (b) stays the same (c) becomes zero (d) increases
17. The direction of the torque $\vec{\tau} = \vec{r}\times\vec{F}$ is
   (a) along $\vec{r}$ (b) along $\vec{F}$ (c) perpendicular to both $\vec{r}$ and $\vec{F}$ (d) along $\vec{r}+\vec{F}$
18. A couple acting on a rigid body produces
   (a) translation only (b) rotation without translation (c) both rotation and translation (d) neither rotation nor translation
19. A body has angular momentum L and moment of inertia I. Its rotational kinetic energy is
   (a) $L^{2}/2I$ (b) $L/2I$ (c) $2L^{2}/I$ (d) $IL^{2}/2$
20. The radius of gyration of a body about a given axis depends on
   (a) its total mass only (b) its angular velocity (c) the torque applied (d) the distribution of its mass about the axis
21. The relation $L = I\omega$ in rotation corresponds, in linear motion, to
   (a) $F = ma$ (b) $p = mv$ (c) $K = \frac{1}{2}mv^{2}$ (d) $W = Fs$

::: note Answers and explanations — Set A
**1.** (b) — $I = \sum mr^2$: kilogram × metre². N m is the unit of torque.
**2.** (a) — $I = \frac{M}{L}\int_{-L/2}^{L/2}x^2\,dx = ML^2/12$.
**3.** (c) — $ML^2/12 + M(L/2)^2 = ML^2/3$, four times the value about the centre.
**4.** (d) — $k = \sqrt{I/M} = \sqrt{L^2/12} = L/(2\sqrt{3}) \approx 0.29L$. $L/\sqrt{3}$ is the value about an end.
**5.** (a) — $I$ depends on the mass, its distribution and the axis; for a rigid body it is the same at any angular velocity.
**6.** (b) — $I = I_{cm} + Md^2$; the term is always added, so the centre-of-mass axis gives the least value.
**7.** (c) — $I$ resists angular acceleration ($\tau = I\alpha$) as mass resists linear acceleration ($F = ma$).
**8.** (a) — $\tau = I\alpha$ is the rotational form of $F = ma$; angular momentum is the analogue of momentum.
**9.** (d) — $\tau = rF$: $[L][MLT^{-2}] = [ML^2T^{-2}]$, the same as work, though torque is a vector.
**10.** (c) — $L = I\omega$: kg m² s⁻¹ = (kg m² s⁻²) s = J s. J s⁻¹ is the watt.
**11.** (a) — summing $\frac{1}{2}mv^2$ with $v = r\omega$ gives $\frac{1}{2}(\sum mr^2)\omega^2 = \frac{1}{2}I\omega^2$.
**12.** (c) — $P = dW/dt = \tau\,d\theta/dt = \tau\omega$, the analogue of $P = Fv$.
**13.** (b) — $W = \tau\theta$ with $\theta$ in radians, the analogue of $W = Fs$.
**14.** (a) — $\tau_{ext} = dL/dt$, so zero external torque keeps $L$ constant. Zero net force conserves *linear* momentum.
**15.** (c) — $\tau = dL/dt$ is the general form of Newton's second law for rotation.
**16.** (d) — $I\omega$ stays constant (no external torque about the vertical axis); pulling the arms in lowers $I$, so $\omega$ rises.
**17.** (c) — a cross product is perpendicular to the plane containing $\vec r$ and $\vec F$ (right-hand rule); it lies along the axis of rotation.
**18.** (b) — the two forces of a couple add to zero (no translation) but their torque $Fd$ is not zero.
**19.** (a) — $K = \frac{1}{2}I\omega^2 = \frac{(I\omega)^2}{2I} = \frac{L^2}{2I}$, like $K = p^2/2m$.
**20.** (d) — $k = \sqrt{I/M}$; the mass cancels, so $k$ depends only on how the mass is spread about the chosen axis.
**21.** (b) — angular momentum $I\omega$ corresponds to linear momentum $mv$.
:::

**Set B — Understanding (13 questions)**

1. For a thin uniform rod, the ratio of its moment of inertia about a perpendicular axis through one end to that about a parallel axis through its centre is
   (a) 2 (b) 4 (c) 3 (d) 12
2. For a thin uniform rod, the ratio of its radius of gyration about a perpendicular axis through one end to that about a parallel axis through its centre is
   (a) 4 (b) √3 (c) 2 (d) √2
3. A thin uniform rod is turned about each of the axes below. Its moment of inertia is greatest about
   (a) a perpendicular axis through its centre (b) a perpendicular axis through a point L/4 from its centre (c) the axis along its own length (d) a perpendicular axis through one end
4. The angular momentum of a body is doubled while its moment of inertia stays the same. Its rotational kinetic energy becomes
   (a) four times (b) twice (c) half (d) unchanged
5. A skater pulls her arms in while spinning freely. Which statement is correct?
   (a) Her angular momentum increases. (b) Her angular momentum stays the same and her kinetic energy increases. (c) Her kinetic energy stays the same. (d) Her angular velocity decreases.
6. A door handle is fixed far from the hinges because this
   (a) reduces the weight of the door (b) reduces the moment of inertia of the door (c) gives a larger torque for the same force (d) reduces friction at the hinges
7. A force whose line of action passes through the axis of rotation produces
   (a) maximum torque (b) zero torque (c) a couple (d) a torque equal to the force times the length of the body
8. A diver curls into a tuck in mid-air. This
   (a) decreases her moment of inertia and increases her rate of spin (b) increases her angular momentum (c) increases her moment of inertia (d) decreases her angular momentum
9. The net force on a rigid body is zero, but the net torque on it is not zero. The body
   (a) stays in complete equilibrium (b) has a linear acceleration but no angular acceleration (c) has an angular acceleration but no linear acceleration (d) must be at rest
10. A planet sweeps out equal areas in equal times, moving faster when it is nearer the Sun. This follows from the conservation of
   (a) linear momentum (b) kinetic energy (c) mass (d) angular momentum
11. Two uniform rods of the same length have masses M and 2M. About perpendicular axes through their centres, their radii of gyration are in the ratio
   (a) 1 : 1 (b) 1 : 2 (c) 2 : 1 (d) 1 : √2
12. If the Earth shrank to half its present radius with no change in mass, the length of a day would become
   (a) 48 h (b) 12 h (c) 6 h (d) 3 h
13. A uniform rod rotates with the same angular velocity first about a perpendicular axis through its centre and then about a parallel axis through one end. The ratio of its kinetic energies (end : centre) is
   (a) 1 : 4 (b) 2 : 1 (c) 1 : 1 (d) 4 : 1

::: note Answers and explanations — Set B
**1.** (b) — $\frac{ML^2/3}{ML^2/12} = 4$.
**2.** (c) — $k \propto \sqrt{I}$, so the ratio is $\sqrt{4} = 2$ ($L/\sqrt{3}$ against $L/2\sqrt{3}$). The tempting 4 is the ratio of the moments of inertia.
**3.** (d) — by the parallel-axis theorem $I = ML^2/12 + Md^2$ grows with $d$; the end ($d = L/2$) is farthest. About its own length a thin rod has almost no $I$.
**4.** (a) — $K = L^2/2I$; with $I$ fixed, doubling $L$ makes $K$ four times.
**5.** (b) — no external torque, so $L$ is constant; $I$ falls, so $\omega$ rises and $K = L^2/2I$ increases (her muscles do the work).
**6.** (c) — $\tau = Fr_\perp$; a larger moment arm gives more torque from the same push.
**7.** (b) — the moment arm $r_\perp$ is zero, so $\tau = Fr_\perp = 0$ (e.g. pulling a door straight toward the hinge).
**8.** (a) — tucking brings mass close to the axis, lowering $I$; with $L$ constant, $\omega$ increases. $L$ itself cannot change in mid-air (no external torque about the centre of mass).
**9.** (c) — zero net force means no acceleration of the centre of mass; a non-zero torque gives $\alpha = \tau/I$. A couple is the example.
**10.** (d) — the Sun's pull is central, so it exerts no torque about the Sun; $L = mvr_\perp$ stays constant, which is the equal-areas law (areal speed $= L/2m$), and $v$ rises as $r$ falls. Kinetic energy is not constant — it changes as the planet speeds up.
**11.** (a) — $k = L/(2\sqrt{3})$ for both: the radius of gyration does not depend on the mass.
**12.** (c) — $I \propto R^2$ falls to one quarter, so $\omega$ rises four times and the period falls from 24 h to 6 h. (b) uses $I \propto R$.
**13.** (d) — $K = \frac{1}{2}I\omega^2$ with the same $\omega$, so $K \propto I$: $\frac{ML^2/3}{ML^2/12} = 4$.
:::

**Set C — Application (10 questions)**

1. A uniform rod of mass 1 kg and length 1.2 m rotates about a perpendicular axis through one end. Its moment of inertia is
   (a) 0.12 kg m² (b) 0.24 kg m² (c) 0.48 kg m² (d) 1.44 kg m²
2. Two small balls (point masses) of 2 kg each are fixed at the ends of a light rod 1 m long. The moment of inertia of the system about a perpendicular axis through the centre of the rod is
   (a) 1.0 kg m² (b) 0.5 kg m² (c) 2.0 kg m² (d) 4.0 kg m²
3. A constant torque of 10 N m acts on a wheel of moment of inertia 2 kg m², initially at rest, for 5 s. The kinetic energy gained by the wheel is
   (a) 125 J (b) 250 J (c) 1250 J (d) 625 J
4. A uniform rod 1.2 m long, freely pivoted at one end, is released from rest in the horizontal position (g = 10 m s⁻²). Its angular velocity as it passes through the vertical position is
   (a) 2.9 rad s⁻¹ (b) 5 rad s⁻¹ (c) 6 rad s⁻¹ (d) 25 rad s⁻¹
5. An electric motor exerts a torque of 20 N m on a shaft turning at 300 revolutions per minute. The power delivered is about
   (a) 100 W (b) 6000 W (c) 628 W (d) 15 W
6. A skater spinning at 2 rad s⁻¹ with moment of inertia 4 kg m² pulls in her arms and her moment of inertia becomes 1.6 kg m². Her new angular velocity is
   (a) 0.8 rad s⁻¹ (b) 3.2 rad s⁻¹ (c) 2 rad s⁻¹ (d) 5 rad s⁻¹
7. A force of 50 N is applied at the end of a spanner 0.4 m long, at 30° to the length of the spanner. The torque about the nut is
   (a) 10 N m (b) 17.3 N m (c) 20 N m (d) 125 N m
8. The radius of gyration of a uniform rod 60 cm long about a perpendicular axis through one end is about
   (a) 17.3 cm (b) 34.6 cm (c) 30 cm (d) 20 cm
9. A disc of moment of inertia 2 kg m² spins at 10 rad s⁻¹. A second disc of moment of inertia 3 kg m², at rest, is dropped onto it on the same axle and they rotate together. The kinetic energy lost is
   (a) zero (b) 40 J (c) 100 J (d) 60 J
10. A uniform rod, freely pivoted at one end, is released from rest in the horizontal position (g = 10 m s⁻²). Just after release, the linear acceleration of its free end is
   (a) 5 m s⁻² (b) 10 m s⁻² (c) 15 m s⁻² (d) 20 m s⁻²

::: note Answers and explanations — Set C
**1.** (c) — $I = ML^2/3 = 1(1.44)/3 = 0.48$ kg m². 0.12 kg m² is the value about the centre.
**2.** (a) — each ball is 0.5 m from the axis: $I = 2\times2\times0.5^2 = 1.0$ kg m². (d) uses 1 m instead of 0.5 m.
**3.** (d) — $\alpha = \tau/I = 5$ rad s⁻²; $\omega = \alpha t = 25$ rad s⁻¹; $K = \frac{1}{2}(2)(25)^2 = 625$ J (equals $\tau\theta = 10\times62.5$).
**4.** (b) — $Mg\frac{L}{2} = \frac{1}{2}\cdot\frac{ML^2}{3}\omega^2$ gives $\omega = \sqrt{3g/L} = \sqrt{30/1.2} = 5$ rad s⁻¹. 6 is the tip speed in m s⁻¹.
**5.** (c) — $\omega = 2\pi(300/60) = 10\pi$ rad s⁻¹; $P = \tau\omega = 20\times31.4 = 628$ W. (b) multiplies by rpm without converting.
**6.** (d) — $\omega_2 = I_1\omega_1/I_2 = 8/1.6 = 5$ rad s⁻¹. (a) inverts the ratio.
**7.** (a) — $\tau = rF\sin\theta = 0.4\times50\times\sin30^{\circ} = 10$ N m. (b) uses $\cos30^{\circ}$; (c) assumes the force is perpendicular.
**8.** (b) — $k = L/\sqrt{3} = 60/1.732 = 34.6$ cm. 17.3 cm is the value about the centre.
**9.** (d) — $\omega = 20/5 = 4$ rad s⁻¹; KE falls from $\frac{1}{2}(2)(100) = 100$ J to $\frac{1}{2}(5)(16) = 40$ J, a loss of 60 J. (b) is the final KE, not the loss.
**10.** (c) — $\alpha = \frac{Mg(L/2)}{ML^2/3} = \frac{3g}{2L}$, so the end has $a = \alpha L = \frac{3}{2}g = 15$ m s⁻² — more than $g$, which is why (b) is the trap.
:::

**Group D — Model answers for long questions (10 marks each, for deeper revision)**

1. Define torque, moment of inertia and angular momentum. State the law of conservation of angular momentum with examples and solve a numerical. <span class="marks">[10]</span>
2. State the parallel and perpendicular axis theorems and find the moment of inertia of a disc. Explain rolling motion with a numerical. <span class="marks">[10]</span>

```photogrid label="3.H" cols="2" ratio="1.4" caption="Rotation in the real world. (a) A skater spins faster when her arms are drawn in because I falls and L = I w stays constant. (b) An electric motor produces torque on its rotor, which gives angular acceleration alpha = torque / I."
@ photo id="ceephy3/skater" cap="(a) Skater: L = I w is conserved"
fit 1.4
focus 0.5 0.45
@ photo id="ceephy3/motor" cap="(b) Motor rotor under torque"
fit 1.4
focus 0.5 0.5
```

### Model answer D1: torque, moment of inertia and conservation of angular momentum (10 marks)

**Introduction.** Rotational motion has quantities that match linear motion. **Torque** $\vec\tau = \vec r\times\vec F$ turns a body, the **moment of inertia** $I = \sum mr^2$ resists the turning, and **angular momentum** $\vec L = I\vec\omega$ measures the quantity of rotation.

**Relations.**

1. **Torque.** $\tau = rF\sin\theta$, in newton metre. It is zero if the force passes through the axis.
2. **Newton's law for rotation.** $\tau = I\alpha$, the counterpart of $F = ma$.
3. **Angular momentum.** For a particle $\vec L = \vec r\times\vec p$, and for a rigid body $L = I\omega$.
4. **Torque as rate of change.** $\vec\tau = d\vec L/dt$. If $\vec\tau = 0$ then $\vec L$ is constant. This is the law of conservation of angular momentum.
5. **Rotational kinetic energy.** $K = \tfrac12I\omega^2 = L^2/2I$.

**Examples of the law.**

- A skater or diver pulls in the arms or legs, so $I$ falls and $\omega$ rises.
- A person on a rotating turntable holding weights changes the speed by moving the weights.
- Planets move faster near the sun (perihelion), which is Kepler's second law.
- A helicopter needs a tail rotor so that the reaction torque does not spin the body.

| Linear | Rotational |
|---|---|
| $v = u + at$ | $\omega = \omega_0 + \alpha t$ |
| $s = ut + \tfrac12at^2$ | $\theta = \omega_0t + \tfrac12\alpha t^2$ |
| $F = ma$ | $\tau = I\alpha$ |
| $p = mv$ | $L = I\omega$ |

**Numerical.** A skater spins at $2\ \text{rev s}^{-1}$ with $I = 3.0\ \text{kg m}^2$. She pulls her arms in and $I$ becomes $1.0\ \text{kg m}^2$. Then $I_1\omega_1 = I_2\omega_2$ gives $\omega_2 = 3\times2 = 6\ \text{rev s}^{-1}$. The kinetic energy rises from $\tfrac12(3)(4\pi)^2 = 237\ \text{J}$ to $\tfrac12(1)(12\pi)^2 = 711\ \text{J}$, three times larger, because her muscles do work.

**Conclusion.** With no external torque $L$ stays constant, so a smaller moment of inertia means a faster spin.

### Model answer D2: theorems of moment of inertia and rolling (10 marks)

**Introduction.** The moment of inertia depends on the axis. Two theorems let us find it for new axes from known values.

**Theorems.**

1. **Parallel axis theorem.** $I = I_{cm} + Md^2$, where $d$ is the distance between the axis and the parallel axis through the centre of mass. $I_{cm}$ is always the smallest value.
2. **Perpendicular axis theorem** (plane bodies only). $I_z = I_x + I_y$, where $x$ and $y$ are perpendicular axes in the plane and $z$ is perpendicular to the plane.

**Disc.** For a uniform disc of mass $M$ and radius $R$, about its central axis, $I = \tfrac12MR^2$. Using the perpendicular axis theorem with $I_x = I_y$, a diameter gives $I_d = \tfrac14MR^2$. By the parallel axis theorem, the axis through the edge, perpendicular to the plane, has $I = \tfrac12MR^2 + MR^2 = \tfrac32MR^2$.

| Body (axis) | $I$ |
|---|---|
| Ring (centre, perpendicular) | $MR^2$ |
| Disc (centre, perpendicular) | $\tfrac12MR^2$ |
| Solid sphere (diameter) | $\tfrac25MR^2$ |
| Hollow sphere (diameter) | $\tfrac23MR^2$ |
| Rod (centre) / (end) | $\dfrac{ML^2}{12}$ / $\dfrac{ML^2}{3}$ |

**Rolling without slipping.** The point of contact is at rest, so $v = R\omega$. The total kinetic energy is $K = \tfrac12mv^2 + \tfrac12I\omega^2 = \tfrac12mv^2\left(1 + \dfrac{k^2}{R^2}\right)$, where $k$ is the radius of gyration. On an incline of height $h$, energy conservation gives $v = \sqrt{\dfrac{2gh}{1 + k^2/R^2}}$. The acceleration is $a = \dfrac{g\sin\theta}{1 + k^2/R^2}$, so the order of arrival is solid sphere, disc, hollow sphere and ring, whatever their masses and radii.

**Numerical.** A disc ($M = 2\ \text{kg}$, $R = 0.5\ \text{m}$) has $I = \tfrac12(2)(0.25) = 0.25\ \text{kg m}^2$ about its axis. A torque of $3\ \text{N m}$ gives $\alpha = 12\ \text{rad s}^{-2}$, and after $5\ \text{s}$, $\omega = 60\ \text{rad s}^{-1}$ and $K = \tfrac12(0.25)(3600) = 450\ \text{J}$. Rolling down $h = 3\ \text{m}$ ($g = 10$) it reaches $v = \sqrt{2(10)(3)/1.5} = 6.3\ \text{m s}^{-1}$, while a ring gets only $\sqrt{30} = 5.5\ \text{m s}^{-1}$.

**Conclusion.** Axis theorems extend known values of $I$, and a body with its mass closer to the axis rolls down faster.
