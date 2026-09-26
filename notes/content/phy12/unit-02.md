---
subject: Physics
grade: 12
unit: 2
title: Periodic motion
hours: 6
area: Mechanics
---

A motion that repeats itself in equal intervals of time is **periodic**. If, in
addition, the body moves to and fro about a fixed point, the motion is
**oscillatory**. The swinging of a temple bell, the trembling of the ground
during an earthquake, the vibration of a sitar string and the current in a radio
circuit are all oscillations, and all of them are built out of one simple
pattern — simple harmonic motion. This unit sets up that pattern, its energy,
two standard applications, and what happens when friction or an external driver
is added.

::: key What makes a motion simple harmonic
A motion is simple harmonic if the acceleration is **proportional to the
displacement from the mean position and always directed towards it**. Every
result in this chapter follows from that one sentence, so learn it exactly.
:::

## 2.1 Equation of simple harmonic motion (SHM)

::: definition Simple harmonic motion
Simple harmonic motion is the oscillation of a body in which the restoring force
(and hence the acceleration) is directly proportional to the displacement from
the mean position and is directed opposite to that displacement:

$$ F = -kx \qquad \text{or} \qquad a = -\omega^{2}x, \qquad \omega^{2} = \frac{k}{m} $$
:::

The constant $\omega$ is the **angular frequency** (rad s⁻¹). The minus sign is
the physics: it says the force always pushes the body back towards $x = 0$.

::: derivation From $a = -\omega^2 x$ to $x = A\sin(\omega t + \phi)$
Write the acceleration as $a = v\,dv/dx$ and separate the variables:

$$ v\frac{dv}{dx} = -\omega^{2}x \;\Longrightarrow\; \int v\,dv = -\omega^{2}\int x\,dx $$

$$ \frac{v^{2}}{2} = -\frac{\omega^{2}x^{2}}{2} + C $$

The body is momentarily at rest at the extreme position $x = A$ (the
**amplitude**), so $C = \omega^{2}A^{2}/2$ and

$$ v = \omega\sqrt{A^{2} - x^{2}} $$

Writing $v = dx/dt$ and separating again,

$$ \int\frac{dx}{\sqrt{A^{2}-x^{2}}} = \int \omega\,dt
\;\Longrightarrow\; \sin^{-1}\frac{x}{A} = \omega t + \phi $$

$$ x = A\sin(\omega t + \phi) $$

where the constant of integration $\phi$ is the **initial phase** or epoch.
:::

Differentiating the displacement gives the velocity and acceleration:

$$ v = \frac{dx}{dt} = A\omega\cos(\omega t + \phi), \qquad
a = \frac{dv}{dt} = -A\omega^{2}\sin(\omega t + \phi) = -\omega^{2}x $$

The **period** is the time for one complete oscillation and the **frequency** is
its reciprocal:

$$ T = \frac{2\pi}{\omega} = 2\pi\sqrt{\frac{m}{k}}, \qquad f = \frac{1}{T} = \frac{\omega}{2\pi} $$

| Position | Displacement | Speed | Acceleration |
|---|---|---|---|
| Mean position ($x=0$) | $0$ | maximum, $A\omega$ | $0$ |
| Extreme position ($x=\pm A$) | $\pm A$ | $0$ | maximum, $\omega^{2}A$ |

```figure caption="SHM is the projection of uniform circular motion on a diameter. As $P$ moves round the circle of radius $A$ with angular velocity $\omega$, its foot $N$ executes $y = A\sin\omega t$."
import numpy as np, matplotlib.pyplot as plt
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(5.2,2.7),
                               gridspec_kw={'width_ratios':[1, 1.2]})
A = 1.0; a = np.radians(52)
th = np.linspace(0, 2*np.pi, 400)
ax1.plot(A*np.cos(th), A*np.sin(th), color=MUTED, lw=1.2)
P = np.array([A*np.cos(a), A*np.sin(a)])
ax1.plot([0, P[0]], [0, P[1]], color=INK, lw=1.3)
ax1.plot([P[0], 0], [P[1], P[1]], color=MUTED, lw=0.9, ls=':')
ax1.plot([-1.25, 1.25], [0, 0], color=GRID, lw=1.0)
ax1.plot([0, 0], [-1.25, 1.25], color=GRID, lw=1.0)
ax1.plot([P[0]], [P[1]], 'o', color=ACCENT, ms=5)
ax1.plot([0], [P[1]], 'o', color='#A8271F', ms=5)
ax1.annotate('$P$', P, textcoords='offset points', xytext=(5, 2), color=ACCENT, fontsize=9.5)
ax1.annotate('$N$', (0, P[1]), textcoords='offset points', xytext=(-14, 1),
             color='#A8271F', fontsize=9.5)
ta = np.linspace(0, a, 60)
ax1.plot(0.30*np.cos(ta), 0.30*np.sin(ta), color=INK, lw=1.0)
ax1.annotate(r'$\omega t$', (0.47*np.cos(a/2), 0.47*np.sin(a/2)), color=INK,
             fontsize=9, ha='center', va='center')
ax1.annotate(r'$A$', P*0.55, textcoords='offset points', xytext=(-13, 3),
             color=INK, fontsize=9.5)
ax1.annotate(r'$y$', (0, P[1]*0.5), textcoords='offset points', xytext=(-13, -2),
             color='#A8271F', fontsize=9.5)
ax1.plot([0, 0], [0, P[1]], color='#A8271F', lw=2.2, solid_capstyle='butt')
ax1.set_xlim(-1.3, 1.3); ax1.set_ylim(-1.3, 1.3)
ax1.set_aspect('equal'); ax1.axis('off')
t = np.linspace(0, 2*np.pi, 400)
ax2.plot(t, A*np.sin(t), color=ACCENT, lw=1.8)
ax2.plot([a], [A*np.sin(a)], 'o', color='#A8271F', ms=5)
ax2.plot([0, a], [A*np.sin(a)]*2, color=MUTED, lw=0.9, ls=':')
ax2.axhline(0, color=GRID, lw=1.0)
ax2.set_xticks([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi])
ax2.set_xticklabels(['0', '$T/4$', '$T/2$', '$3T/4$', '$T$'])
ax2.set_yticks([-1, 0, 1]); ax2.set_yticklabels(['$-A$', '0', '$A$'])
ax2.set_xlabel('time  $t$'); ax2.set_ylabel('displacement  $y$')
ax2.set_ylim(-1.45, 1.45)
ax2.spines[['top','right']].set_visible(False)
```

```figure caption="Displacement, velocity and acceleration in SHM. Velocity leads displacement by $\pi/2$; acceleration is exactly out of phase with displacement ($\pi$)."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,2.8))
t = np.linspace(0, 2*np.pi, 500)
ax.plot(t, np.sin(t), color=ACCENT, lw=1.8, label=r'$x = A\sin\omega t$')
ax.plot(t, np.cos(t), color='#2e8b57', lw=1.6, ls='--', label=r'$v/\omega$')
ax.plot(t, -np.sin(t), color='#A8271F', lw=1.6, ls=':', label=r'$a/\omega^2$')
ax.axhline(0, color=GRID, lw=1.0)
ax.set_xticks([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi])
ax.set_xticklabels(['0', '$T/4$', '$T/2$', '$3T/4$', '$T$'])
ax.set_yticks([-1, 0, 1]); ax.set_yticklabels(['$-A$', '0', '$A$'])
ax.set_xlabel('time  $t$')
ax.set_xlim(0, 2*np.pi); ax.set_ylim(-1.55, 1.85)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, axis='y', alpha=.45)
ax.legend(ncol=3, loc='upper center', fontsize=8.2, columnspacing=1.2)
```

::: example Worked example 2.1
**Problem.** A particle executes SHM of amplitude $5\ \text{cm}$ and period
$2\ \text{s}$. Find (a) its maximum velocity, (b) its maximum acceleration, and
(c) its velocity and acceleration when the displacement is $3\ \text{cm}$.

**Solution.** $\omega = 2\pi/T = 2\pi/2 = \pi = 3.14\ \text{rad s}^{-1}$ and
$A = 0.05\ \text{m}$.

(a) $v_{\max} = A\omega = 0.05 \times 3.14 = 0.157\ \text{m s}^{-1}$.

(b) $a_{\max} = A\omega^{2} = 0.05 \times (3.14)^{2} = 0.493\ \text{m s}^{-2}$.

(c) $v = \omega\sqrt{A^{2}-x^{2}} = 3.14\sqrt{0.05^{2}-0.03^{2}}
= 3.14 \times 0.04 = 0.126\ \text{m s}^{-1}$, and
$|a| = \omega^{2}x = 9.87 \times 0.03 = 0.296\ \text{m s}^{-2}$, directed
towards the mean position.
:::

## 2.2 Energy in SHM

The restoring force is $F = -kx$ with $k = m\omega^{2}$. The work done against
it in moving from $0$ to $x$ is stored as **potential energy**:

$$ U = \int_0^x kx\,dx = \tfrac{1}{2}kx^{2} = \tfrac{1}{2}m\omega^{2}x^{2} $$

The **kinetic energy** follows from $v = \omega\sqrt{A^{2}-x^{2}}$:

$$ K = \tfrac{1}{2}mv^{2} = \tfrac{1}{2}m\omega^{2}(A^{2}-x^{2}) $$

Adding them, the $x^{2}$ terms cancel:

$$ E = K + U = \tfrac{1}{2}m\omega^{2}A^{2} = \tfrac{1}{2}kA^{2} = \text{constant} $$

::: key Total energy in SHM
The total energy is constant, proportional to the **square of the amplitude**
and to the **square of the frequency**. Doubling the amplitude quadruples the
energy. Energy is continuously exchanged between $K$ and $U$: all kinetic at
the mean position, all potential at the extremes.
:::

Averaged over a full cycle, $\langle K\rangle = \langle U\rangle = \frac{1}{4}m\omega^{2}A^{2}$,
i.e. each is half the total.

```figure caption="Kinetic and potential energy against displacement. The two parabolas always add to the constant total $E=\frac{1}{2}kA^2$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,2.8))
A = 1.0; k = 1.0
x = np.linspace(-A, A, 300)
U = 0.5*k*x**2; K = 0.5*k*(A**2 - x**2); E = 0.5*k*A**2
ax.plot(x, U, color='#A8271F', lw=1.8, label='potential energy $U$')
ax.plot(x, K, color='#2e8b57', lw=1.8, label='kinetic energy $K$')
ax.axhline(E, color=ACCENT, lw=1.8, ls='--', label='total energy $E$')
ax.set_xticks([-A, 0, A]); ax.set_xticklabels(['$-A$', '$0$', '$+A$'])
ax.set_yticks([0, E]); ax.set_yticklabels(['$0$', r'$\frac{1}{2}kA^2$'])
ax.set_xlabel('displacement  $x$'); ax.set_ylabel('energy')
ax.set_ylim(0, 0.78); ax.set_xlim(-1.15, 1.15)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.4)
ax.legend(loc='upper center', ncol=1, fontsize=8.2)
```

::: example Worked example 2.2
**Problem.** A body of mass $0.5\ \text{kg}$ attached to a spring of force
constant $200\ \text{N m}^{-1}$ oscillates with amplitude $0.10\ \text{m}$. Find
the period, the total energy, and the kinetic and potential energies when the
displacement is $0.05\ \text{m}$.

**Solution.** $\omega = \sqrt{k/m} = \sqrt{200/0.5} = 20\ \text{rad s}^{-1}$, so

$$ T = \frac{2\pi}{\omega} = \frac{2\pi}{20} = 0.314\ \text{s} $$
$$ E = \tfrac{1}{2}kA^{2} = \tfrac{1}{2}(200)(0.10)^{2} = 1.0\ \text{J} $$

At $x = 0.05\ \text{m}$:
$U = \frac{1}{2}(200)(0.05)^{2} = 0.25\ \text{J}$, so
$K = E - U = 0.75\ \text{J}$.
The speed there is $v = \sqrt{2K/m} = \sqrt{2(0.75)/0.5} = 1.73\ \text{m s}^{-1}$.
:::

## 2.3 Application of SHM: vertical oscillation of mass suspended from coiled spring

Hang a mass $m$ from a light spiral spring of force constant $k$. The spring
stretches by an amount $e$ until the elastic force balances the weight:

$$ mg = ke \qquad \Longrightarrow \qquad k = \frac{mg}{e} $$

This stretched position is the new mean position.

::: derivation Period of vertical oscillation
Pull the mass a further distance $x$ down and release it. The spring now pulls
up with force $k(e+x)$ while the weight $mg$ acts down, so the resultant
(restoring) force is

$$ F = mg - k(e+x) = ke - ke - kx = -kx $$

The weight cancels exactly — it only shifts the mean position, it does not
affect the motion about it. Hence $ma = -kx$, i.e.

$$ a = -\frac{k}{m}x $$

which is SHM with $\omega = \sqrt{k/m}$, so

$$ T = 2\pi\sqrt{\frac{m}{k}} = 2\pi\sqrt{\frac{e}{g}} $$
:::

The second form is useful in the laboratory: measure the static extension $e$
produced by the load and you can predict the period, or measure $T$ and $e$ and
obtain $g = 4\pi^{2}e/T^{2}$.

```figure caption="Vertical oscillation of a mass on a spring. The weight is cancelled by the static extension $e$, leaving a restoring force $-kx$ about the new mean position."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(4.9,3.4))
def spring(x0, ytop, ybot, n=8, w=0.16):
    ys = np.linspace(ytop, ybot, 2*n+2)
    xs = np.full(ys.shape, float(x0))
    idx = np.arange(1, len(ys)-1)
    xs[1:-1] = x0 + w*np.where(idx % 2 == 0, 1.0, -1.0)
    ax.plot(xs, ys, color=INK, lw=1.2)
def block(x0, y):
    ax.add_patch(Rectangle((x0-0.30, y-0.28), 0.60, 0.28, facecolor=ACCENT,
                           alpha=0.30, edgecolor=INK, lw=1.0))
    ax.annotate('$m$', (x0, y-0.14), color=INK, fontsize=9, ha='center', va='center')
for x0, lab in [(0, '(a) unloaded'), (1.9, '(b) equilibrium'),
                (4.0, '(c) displaced')]:
    ax.plot([x0-0.55, x0+0.55], [0, 0], color=INK, lw=1.7)
    for xh in np.linspace(x0-0.52, x0+0.44, 6):
        ax.plot([xh, xh+0.11], [0, 0.14], color=MUTED, lw=0.8)
    ax.annotate(lab, (x0, -4.15), color=INK, fontsize=8.6, ha='center', va='top')
# (a) unloaded
spring(0, 0, -1.3)
ax.plot([-0.62, 0.62], [-1.3, -1.3], color=MUTED, lw=0.8, ls=':')
# (b) equilibrium
spring(1.9, 0, -2.1); block(1.9, -2.1)
ax.plot([1.9-0.68, 1.9+0.80], [-1.3, -1.3], color=MUTED, lw=0.8, ls=':')
ax.annotate('', xy=(2.66, -2.1), xytext=(2.66, -1.3),
            arrowprops=dict(arrowstyle='<|-|>', color='#A8271F', lw=1.0, mutation_scale=9))
ax.annotate('$e$', (2.74, -1.70), color='#A8271F', fontsize=9.5, va='center')
ax.annotate('$mg = ke$', (1.9, -2.66), color=MUTED, fontsize=8.6, ha='center')
# (c) displaced
spring(4.0, 0, -2.8); block(4.0, -2.8)
ax.plot([4.0-0.62, 4.0+0.92], [-2.1, -2.1], color=MUTED, lw=0.8, ls=':')
ax.annotate('', xy=(3.45, -2.8), xytext=(3.45, -2.1),
            arrowprops=dict(arrowstyle='<|-|>', color='#A8271F', lw=1.0, mutation_scale=9))
ax.annotate('$x$', (3.37, -2.45), color='#A8271F', fontsize=9.5,
            ha='right', va='center')
ax.annotate('', xy=(4.55, -2.02), xytext=(4.55, -2.80),
            arrowprops=dict(arrowstyle='-|>', color='#0B6A62', lw=1.5, mutation_scale=11))
ax.annotate('$k(e+x)$', (4.63, -2.40), color='#0B6A62', fontsize=9,
            ha='left', va='center')
ax.annotate('', xy=(4.0, -3.90), xytext=(4.0, -3.16),
            arrowprops=dict(arrowstyle='-|>', color='#0B6A62', lw=1.5, mutation_scale=11))
ax.annotate('$mg$', (4.12, -3.58), color='#0B6A62', fontsize=9, va='center')
ax.set_xlim(-0.95, 5.80); ax.set_ylim(-5.0, 0.55)
ax.set_aspect('equal'); ax.axis('off')
```

::: example Worked example 2.3
**Problem.** A mass of $0.5\ \text{kg}$ hung from a light spiral spring stretches
it by $10\ \text{cm}$. Find the force constant of the spring and the period of
vertical oscillation. Take $g = 9.8\ \text{m s}^{-2}$.

**Solution.**

$$ k = \frac{mg}{e} = \frac{0.5 \times 9.8}{0.10} = 49\ \text{N m}^{-1} $$
$$ T = 2\pi\sqrt{\frac{e}{g}} = 2\pi\sqrt{\frac{0.10}{9.8}} = 2\pi(0.101) = 0.635\ \text{s} $$

The frequency is $f = 1/T = 1.58\ \text{Hz}$. Note that the answer needs only
$e$ and $g$ — the mass cancels, because a heavier mass also stretches the spring
more.
:::

## 2.4 Angular SHM; simple pendulum

In **angular SHM** the body is displaced through an angle $\theta$ and the
restoring **torque** is proportional to that angle:

$$ \tau = -c\theta \;\Longrightarrow\; I\frac{d^{2}\theta}{dt^{2}} = -c\theta
\;\Longrightarrow\; T = 2\pi\sqrt{\frac{I}{c}} $$

where $c$ is the torsional constant and $I$ the moment of inertia about the
axis. A torsion pendulum and the coil of a moving-coil galvanometer behave this
way.

```figure caption="Simple pendulum. The component $mg\sin\theta$ is the restoring force; $mg\cos\theta$ merely balances the tension."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.4,3.2))
L = 2.6; th = np.radians(26)
O = np.array([0.0, 0.0])
B = np.array([L*np.sin(th), -L*np.cos(th)])
ax.plot([-0.75, 0.75], [0, 0], color=INK, lw=1.8)
for xh in np.linspace(-0.7, 0.62, 7):
    ax.plot([xh, xh+0.14], [0, 0.16], color=MUTED, lw=0.9)
ax.plot([0, 0], [0, -L-0.25], color=MUTED, lw=0.9, ls='--')
ax.plot([O[0], B[0]], [O[1], B[1]], color=INK, lw=1.3)
ax.add_patch(plt.Circle(B, 0.19, facecolor=ACCENT, alpha=0.45, edgecolor=INK, lw=1.1))
ta = np.linspace(-np.pi/2, -np.pi/2 + th, 60)
ax.plot(0.85*np.cos(ta), 0.85*np.sin(ta), color='#A8271F', lw=1.1)
ax.annotate(r'$\theta$', (1.02*np.cos(-np.pi/2+th/2), 1.02*np.sin(-np.pi/2+th/2)),
            color='#A8271F', fontsize=10, ha='center', va='center')
ax.annotate('$L$', (B[0]*0.62, B[1]*0.62), textcoords='offset points',
            xytext=(9, 5), color=INK, fontsize=10)
W = np.array([0.0, -1.15])
ax.annotate('', xy=B+W, xytext=B, arrowprops=dict(arrowstyle='-|>', color='#0B6A62',
            lw=1.6, mutation_scale=12))
ax.annotate('$mg$', B+W, textcoords='offset points', xytext=(-2, -12),
            color='#0B6A62', fontsize=9.5, ha='center', va='top')
rad = np.array([np.sin(th), -np.cos(th)])
tan = np.array([np.cos(th), np.sin(th)])
c1 = 1.15*np.cos(th); c2 = 1.15*np.sin(th)
ax.annotate('', xy=B+c1*rad, xytext=B, arrowprops=dict(arrowstyle='-|>',
            color=MUTED, lw=1.3, mutation_scale=11))
ax.annotate(r'$mg\cos\theta$', B+c1*rad, textcoords='offset points', xytext=(6, -4),
            color=MUTED, fontsize=9, ha='left', va='center')
ax.annotate('', xy=B-c2*tan, xytext=B, arrowprops=dict(arrowstyle='-|>',
            color='#A8271F', lw=1.6, mutation_scale=12))
ax.annotate(r'$mg\sin\theta$', B-c2*tan, textcoords='offset points', xytext=(-3, 8),
            color='#A8271F', fontsize=9, ha='right', va='bottom')
ax.plot([B[0], (B+W)[0]], [B[1], (B+W)[1]], color=GRID, lw=0.8)
ax.plot([(B+W)[0], (B+c1*rad)[0]], [(B+W)[1], (B+c1*rad)[1]], color=GRID, lw=0.8, ls=':')
ax.plot([(B+W)[0], (B-c2*tan)[0]], [(B+W)[1], (B-c2*tan)[1]], color=GRID, lw=0.8, ls=':')
ax.set_xlim(-1.35, 2.95); ax.set_ylim(-4.0, 0.55)
ax.set_aspect('equal'); ax.axis('off')
```

::: derivation Period of a simple pendulum
A simple pendulum is a point mass (bob) of mass $m$ hung by a light inextensible
string of length $L$ from a rigid support. When the string makes an angle
$\theta$ with the vertical, the weight $mg$ is resolved into $mg\cos\theta$
along the string (balanced by the tension) and $mg\sin\theta$ perpendicular to
it. The second component is the restoring force:

$$ F = -mg\sin\theta $$

For **small** angles, $\sin\theta \approx \theta$ in radians, and the
displacement along the arc is $x = L\theta$, so

$$ F = -mg\theta = -\frac{mg}{L}x \;\Longrightarrow\; a = -\frac{g}{L}x $$

This is SHM with $\omega^{2} = g/L$, hence

$$ T = 2\pi\sqrt{\frac{L}{g}} $$
:::

The four **laws of the simple pendulum** follow directly: $T \propto \sqrt{L}$
(law of length); $T \propto 1/\sqrt{g}$ (law of gravity); $T$ is independent of
the **mass** of the bob; and $T$ is independent of the **amplitude** so long as
it is small (law of isochronism). A **seconds pendulum** has $T = 2\ \text{s}$,
so it takes one second for each swing.

::: caution The small-angle condition is not optional
$T = 2\pi\sqrt{L/g}$ comes from replacing $\sin\theta$ by $\theta$, which is
accurate only for amplitudes of a few degrees (up to about $4^{\circ}$). For
larger swings the real period is longer, and the motion is periodic but no
longer simple harmonic.
:::

::: example Worked example 2.4
**Problem.** Find the length of a seconds pendulum at a place where
$g = 9.8\ \text{m s}^{-2}$. If this pendulum clock is carried to a place where
$g = 9.78\ \text{m s}^{-2}$, how much time will it lose in one day?

**Solution.** From $T = 2\pi\sqrt{L/g}$,

$$ L = \frac{gT^{2}}{4\pi^{2}} = \frac{9.8 \times 2^{2}}{4\pi^{2}} = 0.993\ \text{m} $$

At the new place the same pendulum has period

$$ T' = 2\pi\sqrt{\frac{0.993}{9.78}} = 2.002\ \text{s} $$

The clock still counts every swing as $2\ \text{s}$. In one real day it makes
$86400/2.002 = 43156$ oscillations and therefore records only
$43156 \times 2 = 86312\ \text{s}$.

Time lost per day $= 86400 - 86312 = 88\ \text{s}$, i.e. about
$1\ \text{minute}\ 28\ \text{s}$ slow.
:::

## 2.5 Oscillatory motion: Damped oscillation, Forced oscillation and resonance

Real oscillators lose energy to friction and air resistance, so the amplitude
falls with time. This is **damped oscillation**. For small speeds the resistive
force is proportional to the velocity, $F_d = -bv$, and Newton's second law
gives

$$ m\frac{d^{2}x}{dt^{2}} + b\frac{dx}{dt} + kx = 0 $$

whose light-damping solution is

$$ x = A_0 e^{-bt/2m}\sin(\omega' t + \phi), \qquad
\omega' = \sqrt{\frac{k}{m} - \frac{b^{2}}{4m^{2}}} $$

The amplitude decays exponentially as $A = A_0e^{-bt/2m}$, and because
$E \propto A^{2}$ the energy decays twice as fast. Damping also makes the
oscillation slightly **slower** ($\omega' < \omega_0$).

| Case | Condition | Behaviour | Example |
|---|---|---|---|
| Under-damped | $b$ small | oscillates with decaying amplitude | pendulum in air |
| Critically damped | $b^{2} = 4mk$ | returns to rest in the **shortest time**, no oscillation | dead-beat galvanometer |
| Over-damped | $b$ large | returns to rest slowly, no oscillation | pendulum in thick oil |

If an external periodic force $F_0\sin\omega_d t$ is applied, the oscillator
settles into a **forced oscillation** at the **driver's** frequency $\omega_d$,
not its own. The steady amplitude is

$$ A = \frac{F_0/m}{\sqrt{(\omega_0^{2}-\omega_d^{2})^{2} + (b\omega_d/m)^{2}}} $$

::: definition Resonance
Resonance is the large increase in the amplitude of a forced oscillation that
occurs when the frequency of the driving force becomes equal to the natural
frequency of the oscillator ($\omega_d = \omega_0$). At resonance the driver
feeds energy to the oscillator in step with its motion, and the amplitude is
limited only by damping.
:::

```figure caption="Left: amplitude of a damped oscillation decays as $A_0e^{-bt/2m}$. Right: resonance curves — lighter damping gives a taller, sharper peak at $\omega_d=\omega_0$."
import numpy as np, matplotlib.pyplot as plt
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(5.2,2.6))
t = np.linspace(0, 12, 700); g = 0.22
env = np.exp(-g*t)
ax1.plot(t, env*np.sin(3.2*t), color=ACCENT, lw=1.3)
ax1.plot(t, env, color='#A8271F', lw=1.2, ls='--')
ax1.plot(t, -env, color='#A8271F', lw=1.2, ls='--')
ax1.annotate(r'$A_0e^{-bt/2m}$', (6.4, np.exp(-g*6.4)+0.10), color='#A8271F',
             fontsize=8.6, ha='center')
ax1.axhline(0, color=GRID, lw=1.0)
ax1.set_xlabel('time  $t$'); ax1.set_ylabel('displacement  $x$')
ax1.set_yticks([]); ax1.set_xticks([])
ax1.set_ylim(-1.35, 1.5); ax1.set_xlim(0, 12)
ax1.spines[['top','right']].set_visible(False)
w = np.linspace(0.05, 2.1, 600); w0 = 1.0
for gam, c, lab in [(0.10, '#A8271F', 'light'), (0.25, ACCENT, 'medium'),
                    (0.55, '#2e8b57', 'heavy')]:
    ax2.plot(w, 1.0/np.sqrt((w0**2 - w**2)**2 + (gam*w)**2), color=c, lw=1.5, label=lab)
ax2.axvline(w0, color=MUTED, lw=0.9, ls=':')
ax2.set_xlabel(r'driving frequency  $\omega_d$'); ax2.set_ylabel('amplitude  $A$')
ax2.set_xticks([w0]); ax2.set_xticklabels([r'$\omega_0$'])
ax2.set_yticks([]); ax2.set_ylim(0, 11.5); ax2.set_xlim(0, 2.1)
ax2.spines[['top','right']].set_visible(False)
ax2.legend(title='damping', fontsize=7.8, title_fontsize=7.8, loc='upper right')
fig.subplots_adjust(wspace=0.35)
```

Resonance is useful and dangerous in equal measure: it lets a radio pick out one
station, makes a sitar's sympathetic strings sing, and allows a small push at
the right moment to swing a child high. But it also destroyed the Tacoma Narrows
bridge, is why soldiers break step on a bridge, and is why buildings whose
natural frequency matches the shaking of an earthquake — as some did in the
Gorkha earthquake of 2015 — suffer the worst damage.

::: example Worked example 2.5
**Problem.** A damped oscillator has mass $0.2\ \text{kg}$ and damping constant
$b = 0.04\ \text{kg s}^{-1}$. After what time does (a) the amplitude fall to
$1/e$ of its initial value, and (b) the energy fall to $1/e$ of its initial
value?

**Solution.** (a) $A = A_0e^{-bt/2m}$, so $A = A_0/e$ when $bt/2m = 1$:

$$ t = \frac{2m}{b} = \frac{2 \times 0.2}{0.04} = 10\ \text{s} $$

(b) $E \propto A^{2}$, so $E = E_0e^{-bt/m}$, and $E = E_0/e$ when

$$ t = \frac{m}{b} = \frac{0.2}{0.04} = 5\ \text{s} $$

The energy decays in half the time the amplitude does.
:::

## Chapter summary

- SHM: $a = -\omega^{2}x$, with $x = A\sin(\omega t + \phi)$,
  $v = A\omega\cos(\omega t+\phi) = \omega\sqrt{A^{2}-x^{2}}$ and
  $T = 2\pi/\omega = 2\pi\sqrt{m/k}$.
- Speed is maximum ($A\omega$) at the mean position; acceleration is maximum
  ($\omega^{2}A$) at the extremes. SHM is the projection of uniform circular
  motion on a diameter.
- $U = \frac{1}{2}m\omega^{2}x^{2}$, $K = \frac{1}{2}m\omega^{2}(A^{2}-x^{2})$,
  and the total $E = \frac{1}{2}m\omega^{2}A^{2} = \frac{1}{2}kA^{2}$ is constant.
- Mass on a vertical spring: $mg = ke$ and $T = 2\pi\sqrt{m/k} = 2\pi\sqrt{e/g}$;
  the weight only shifts the mean position.
- Angular SHM: $\tau = -c\theta$ gives $T = 2\pi\sqrt{I/c}$. Simple pendulum:
  $T = 2\pi\sqrt{L/g}$ for small amplitude, independent of the mass of the bob.
- Damped oscillation: $A = A_0e^{-bt/2m}$, $\omega' = \sqrt{k/m - b^{2}/4m^{2}}$;
  critical damping returns the system to rest fastest.
- A forced oscillator vibrates at the driver's frequency; at resonance
  ($\omega_d = \omega_0$) the amplitude is maximum and is limited only by damping.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. In simple harmonic motion the acceleration is <span class="marks">[1]</span>
   (a) constant (b) proportional to displacement and in the same direction
   (c) proportional to displacement and oppositely directed
   (d) inversely proportional to displacement
2. The total energy of a particle executing SHM is proportional to <span class="marks">[1]</span>
   (a) $A$ (b) $A^{2}$ (c) $1/A$ (d) $\sqrt{A}$
3. The period of a simple pendulum does **not** depend on <span class="marks">[1]</span>
   (a) its length (b) the acceleration due to gravity (c) the mass of the bob
   (d) any of these
4. A mass $m$ hanging from a spring of force constant $k$ oscillates with period <span class="marks">[1]</span>
   (a) $2\pi\sqrt{k/m}$ (b) $2\pi\sqrt{m/k}$ (c) $2\pi\sqrt{mk}$ (d) $\frac{1}{2\pi}\sqrt{m/k}$
5. At resonance the amplitude of a forced oscillation is <span class="marks">[1]</span>
   (a) zero (b) minimum (c) maximum (d) independent of damping

::: note Answers to Group A
**1.** (c) — this is the definition, $a = -\omega^{2}x$.
**2.** (b) — $E = \frac{1}{2}m\omega^{2}A^{2}$.
**3.** (c) — mass cancels between the restoring force and the inertia.
**4.** (b) — $\omega = \sqrt{k/m}$, so $T = 2\pi/\omega = 2\pi\sqrt{m/k}$.
**5.** (c) — the driving frequency matches the natural frequency, so energy is
fed in step with the motion.
:::

**Group B — Short answer (5 marks each)**

1. Define simple harmonic motion. Show that the motion of a mass attached to a
   spring obeying Hooke's law is simple harmonic, and obtain its period. <span class="marks">[5]</span>
2. Derive expressions for the kinetic and potential energies of a particle in
   SHM and show that the total energy is constant. <span class="marks">[5]</span>
3. A particle of mass $0.2\ \text{kg}$ executes SHM of amplitude
   $0.10\ \text{m}$ with angular frequency $10\ \text{rad s}^{-1}$. Find its
   total energy, and its kinetic and potential energies at a displacement of
   $0.05\ \text{m}$. <span class="marks">[5]</span>
4. A load of $0.5\ \text{kg}$ stretches a light spiral spring by $5\ \text{cm}$.
   Find the force constant of the spring and the period of vertical oscillation
   of the load. ($g = 9.8\ \text{m s}^{-2}$) <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Outline: state the definition; for a spring $F = -kx$, so
$a = -(k/m)x = -\omega^{2}x$ with $\omega = \sqrt{k/m}$, which is SHM; hence
$T = 2\pi\sqrt{m/k}$.

**2.** Outline: $U = \int_0^x kx\,dx = \frac{1}{2}m\omega^{2}x^{2}$;
$K = \frac{1}{2}mv^{2} = \frac{1}{2}m\omega^{2}(A^{2}-x^{2})$; adding,
$E = \frac{1}{2}m\omega^{2}A^{2}$, independent of $x$.

**3.** $E = \frac{1}{2}m\omega^{2}A^{2} = \frac{1}{2}(0.2)(10)^{2}(0.10)^{2} = 0.1\ \text{J}$.
At $x = 0.05\ \text{m}$:
$U = \frac{1}{2}(0.2)(100)(0.05)^{2} = 0.025\ \text{J}$ and
$K = 0.1 - 0.025 = 0.075\ \text{J}$.

**4.** $k = mg/e = (0.5 \times 9.8)/0.05 = 98\ \text{N m}^{-1}$;
$T = 2\pi\sqrt{e/g} = 2\pi\sqrt{0.05/9.8} = 0.449\ \text{s}$.
:::

**Group C — Long answer (8 marks each)**

1. (a) Define simple harmonic motion and, starting from $a = -\omega^{2}x$,
   derive the expression $x = A\sin(\omega t+\phi)$ and hence
   $v = \omega\sqrt{A^{2}-x^{2}}$. <span class="marks">[5]</span>
   (b) Sketch how the kinetic and potential energies vary with displacement, and
   state where each is maximum. <span class="marks">[3]</span>
2. (a) Derive an expression for the period of a simple pendulum, stating clearly
   the assumptions made. <span class="marks">[5]</span>
   (b) A seconds pendulum is set up in Kathmandu, where
   $g = 9.79\ \text{m s}^{-2}$. Find its length. If it is then taken to a place
   where $g = 9.81\ \text{m s}^{-2}$, how much time will it gain in a day? <span class="marks">[3]</span>

::: note Answer to Group C question 2(b)
$L = \dfrac{gT^{2}}{4\pi^{2}} = \dfrac{9.79 \times 4}{4\pi^{2}} = 0.992\ \text{m}$.

At the new place, $T' = 2\pi\sqrt{0.992/9.81} = 1.998\ \text{s}$.

In one real day the pendulum makes $86400/1.998 = 43244$ oscillations, and the
clock records $43244 \times 2 = 86488\ \text{s}$.

Gain per day $= 86488 - 86400 \approx 88\ \text{s}$.
:::
