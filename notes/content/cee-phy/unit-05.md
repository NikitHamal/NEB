---
subject: Physics
grade: CEE
unit: 5
title: Circular Motion and Simple Harmonic Motion
hours: 2
area: Mechanics
---

Circular motion and simple harmonic motion (SHM) are the two great *repeating*
motions of mechanics, and they are close relatives: SHM is the shadow of uniform
circular motion on a diameter. Of the **10 Mechanics questions** (official weightage),
we estimate about **2** come from this chapter. The favourites are the minimum speed
in a vertical circle, banking and friction on curved roads, the velocity and
acceleration of SHM at a given displacement, energy in SHM, and how the period of a
pendulum or a spring changes — on the Moon, in a lift, or with a cut spring.

::: key What the paper asks from this chapter
- $v = r\omega$, $\omega = 2\pi/T = 2\pi f$; centripetal acceleration $v^2/r = \omega^2r$ towards the centre; it does no work.
- Level road $v_{max} = \sqrt{\mu rg}$; banking $\tan\theta = v^2/rg$; hump of a bridge $v = \sqrt{gr}$.
- Vertical circle on a string: $v_{top} \ge \sqrt{gr}$, $v_{bottom} \ge \sqrt{5gr}$; $T_{bottom} - T_{top} = 6mg$.
- SHM: $a = -\omega^2x$; $v = \omega\sqrt{A^2 - x^2}$; $v_{max} = A\omega$, $a_{max} = A\omega^2$; phases 0, $\pi/2$, $\pi$.
- Energy $\frac{1}{2}m\omega^2A^2$; KE = PE at $x = A/\sqrt{2}$; energy oscillates at twice the frequency.
- $T = 2\pi\sqrt{l/g}$ and $T = 2\pi\sqrt{m/k}$: what each depends on, and springs in series and parallel.
- Forced oscillation and resonance: amplitude is largest when the driving frequency equals the natural frequency.
:::

## 5.1 Angular quantities; centripetal acceleration and force

### Angular quantities

| Quantity | Definition | SI unit | Link with linear quantity |
|---|---|---|---|
| Angular displacement $\theta$ | angle swept by the radius: $\theta = s/r$ | rad | arc $s = r\theta$ |
| Angular velocity $\omega$ | $\omega = d\theta/dt$; uniform: $\omega = 2\pi/T = 2\pi f$ | rad s⁻¹ | $v = r\omega$ |
| Angular acceleration $\alpha$ | $\alpha = d\omega/dt$ | rad s⁻² | tangential $a_t = r\alpha$ |
| Time period $T$ / frequency $f$ | time for one revolution / revolutions per second | s / Hz | $f = 1/T$ |

1 revolution = 2π rad = 360°. For a machine turning at $N$ rpm,
$\omega = 2\pi N/60$ rad s⁻¹. Hands of a clock: second hand $2\pi/60$ rad s⁻¹, minute
hand $2\pi/3600$, hour hand $2\pi/43\,200$ (ratios 60 : 1 between second and minute
hands, 12 : 1 between minute and hour hands). The Earth spins at about
7.3 × 10⁻⁵ rad s⁻¹. All points of a rigid rotating body have the **same** $\omega$ but
speeds $v = r\omega$ that grow with distance from the axis.

### Centripetal acceleration and force

In **uniform circular motion** the speed is constant but the direction of the
velocity changes all the time, so the body **accelerates**. The acceleration points
along the radius **towards the centre** (centripetal) and has magnitude

$$ a_c = \frac{v^2}{r} = \omega^2r = v\omega $$

By the second law there must be a net inward force, the **centripetal force**:

$$ F_c = \frac{mv^2}{r} = m\omega^2r $$

The centripetal force is not a new kind of force: it is whichever real force (or
resultant) points to the centre — the tension in a string, friction on a turning car,
gravity on a satellite, the electric pull on an electron in Bohr's atom, the normal
reaction of a wall.

| In uniform circular motion | Constant? |
|---|---|
| speed, kinetic energy, angular velocity, magnitude of acceleration | yes |
| velocity, linear momentum, acceleration (directions change) | no |
| angular momentum about the centre | yes |
| work done by the centripetal force | always zero (force ⟂ velocity) |

If the speed also changes (non-uniform circular motion), there is a tangential
acceleration $a_t = dv/dt$ as well, and the total acceleration is
$\sqrt{a_c^2 + a_t^2}$.

::: caution Centrifugal force
"Centrifugal force" $mv^2/r$, pointing outward, appears only to an observer **in the
rotating frame** — it is a pseudo force, not the reaction to the centripetal force.
When the string of a whirling stone breaks, the stone flies off along the **tangent**,
not radially outward.
:::

::: example Worked example 5.1 — a whirled stone
**Problem.** A 0.5 kg stone tied to a 1 m string is whirled in a horizontal circle at
2 revolutions per second. Find its speed, its acceleration and the tension (ignore
gravity's effect on the string).

**Solution.** $\omega = 2\pi f = 4\pi$ rad s⁻¹; $v = r\omega = 4\pi = 12.6$ m s⁻¹;
$a = \omega^2r = 16\pi^2 = 158$ m s⁻²; $T = ma = 79$ N. Doubling the rate of turning
would make the tension four times as large.
:::

## 5.2 Motion in a horizontal and in a vertical circle

### Horizontal circles

| Situation | Force supplying $mv^2/r$ | Result |
|---|---|---|
| Car on a **level** curved road | friction, $\mu mg$ at most | $v_{max} = \sqrt{\mu rg}$ (independent of mass) |
| Road **banked** at angle $\theta$, no friction needed | horizontal component of the normal reaction, $N\sin\theta$ | $\tan\theta = \frac{v^2}{rg}$ |
| Banked road with friction $\mu$ | normal reaction and friction together | $v_{max} = \sqrt{rg\frac{\mu + \tan\theta}{1 - \mu\tan\theta}}$ |
| Cyclist rounding a bend | friction; he leans inward at angle $\theta$ from the vertical | $\tan\theta = \frac{v^2}{rg}$ |
| Conical pendulum (string length $L$ at angle $\theta$ to vertical) | horizontal component of tension: $T\sin\theta = mv^2/r$, $T\cos\theta = mg$ | $\tan\theta = \frac{v^2}{rg}$; period $2\pi\sqrt{L\cos\theta/g}$ |
| Rider on the vertical wall of a "well of death" | normal reaction of the wall; friction $\mu N$ holds up the weight | $v_{min} = \sqrt{rg/\mu}$ |

Banking lets vehicles turn without depending on friction, which is why outer edges of
curves on highways and railway tracks (the outer rail) are raised.

### Vertical circle

A body of mass $m$ on a string of length $r$ whirled in a **vertical** circle: gravity
helps at the top and opposes at the bottom, and the speed changes around the circle
(energy conservation: $v_{bottom}^2 = v_{top}^2 + 4gr$).

```figure caption="A stone whirled in a vertical circle on a string. At the top, tension and weight both point to the centre; at the bottom they are opposite, so the string is tightest there."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle
fig, ax = plt.subplots(figsize=(4.8,3.6))
R = 1.4
ax.add_patch(Circle((0,0), R, fill=False, ec=MUTED, lw=1.0, ls=(0,(4,2))))
ax.plot([0],[0],'o', color=INK, ms=4)
ax.text(0.12, -0.08, 'O', fontsize=9, color=INK, va='top')
def arr(a, b, col, lw=1.8):
    ax.annotate('', xy=b, xytext=a, arrowprops=dict(arrowstyle='-|>', color=col, lw=lw,
                shrinkA=0, shrinkB=0, mutation_scale=12), zorder=5)
ax.plot([0,0],[0,R], color=INK, lw=0.8, zorder=2); ax.plot([0,0],[0,-R], color=INK, lw=0.8, zorder=2)
for y in (R, -R):
    ax.add_patch(Circle((0,y), 0.11, color=ACCENT, zorder=6))
arr((0.18, R-0.05), (0.18, R-0.75), '#A8271F'); ax.text(0.3, R-0.62, 'T', color='#A8271F', fontsize=10)
arr((-0.18, R-0.05), (-0.18, R-0.75), INK); ax.text(-0.33, R-0.62, 'mg', color=INK, fontsize=9.5, ha='right')
arr((0.13, R+0.02), (0.95, R+0.02), MUTED, lw=1.3); ax.text(0.98, R+0.12, 'v', color=MUTED, fontsize=10)
arr((0.18, -R+0.05), (0.18, -R+0.75), '#A8271F'); ax.text(0.3, -R+0.5, 'T', color='#A8271F', fontsize=10)
arr((-0.18, -R-0.05), (-0.18, -R-0.75), INK); ax.text(-0.33, -R-0.6, 'mg', color=INK, fontsize=9.5, ha='right')
arr((-0.13, -R-0.02), (-0.95, -R-0.02), MUTED, lw=1.3); ax.text(-1.0, -R+0.1, 'v', color=MUTED, fontsize=10, ha='right')
ax.text(1.75, 1.35, 'top:  T + mg = mv²/r', fontsize=8.5, color=INK, va='center')
ax.text(1.75, 0.95, 'string just slack: v = √(gr)', fontsize=8.5, color=MUTED, va='center')
ax.text(1.75, -1.0, 'bottom:  T − mg = mv²/r', fontsize=8.5, color=INK, va='center')
ax.text(1.75, -1.4, 'to loop: v ≥ √(5gr)', fontsize=8.5, color=MUTED, va='center')
ax.set_xlim(-1.7, 4.9); ax.set_ylim(-2.3, 1.95); ax.set_aspect('equal'); ax.axis('off')
```

| Point of the circle (string) | Tension | Least speed to complete the loop |
|---|---|---|
| Top | $T_{top} = \frac{mv_{top}^2}{r} - mg$ | $\sqrt{gr}$ (string just slack, $T_{top} = 0$) |
| Horizontal (side) | $T = \frac{mv^2}{r}$ | $\sqrt{3gr}$ |
| Bottom | $T_{bottom} = \frac{mv_{bottom}^2}{r} + mg$ | $\sqrt{5gr}$ |
| Difference | $T_{bottom} - T_{top} = 6mg$ (for any speed that completes the loop) | |

If the body is on a light **rigid rod** instead of a string, the rod can push as well
as pull, so the body need only *reach* the top: $v_{top} \ge 0$ and
$v_{bottom} \ge \sqrt{4gr} = 2\sqrt{gr}$. A bucket of water swung in a vertical circle
does not spill if $v_{top} \ge \sqrt{gr}$ — at that speed the water's weight alone
supplies the centripetal force.

**Over a hump and through a dip.** A car at the top of a convex bridge of radius $r$:
$N = mg - mv^2/r$ (it feels lighter), and it leaves the road when $v = \sqrt{gr}$. At the
bottom of a dip: $N = mg + mv^2/r$ (it presses harder). A pilot pulling out of a dive
feels the same extra weight.

::: example Worked example 5.2 — roads and loops
**Problem.** ($g = 10$ m s⁻²) (a) Find the greatest speed of a car on a level curve of
radius 100 m if $\mu = 0.4$. (b) At what angle should a curve of radius 45 m be banked
for 15 m s⁻¹? (c) A 0.2 kg stone on a 1 m string has speed 8 m s⁻¹ at the bottom of a
vertical circle. Find its speed and the tension at the top, and the tension at the
bottom.

**Solution.** (a) $v = \sqrt{\mu rg} = \sqrt{400} = 20$ m s⁻¹ = 72 km h⁻¹.
(b) $\tan\theta = 225/450 = 0.5$, $\theta = 26.6^{\circ}$.
(c) $v_{top}^2 = 64 - 4(10)(1) = 24$, $v_{top} = 4.9$ m s⁻¹ (above $\sqrt{gr} = 3.2$, so
the loop is completed). $T_{top} = 0.2(24) - 2 = 2.8$ N; $T_{bottom} = 0.2(64) + 2 = 14.8$ N.
The difference, 12 N, is $6mg$.
:::

## 5.3 Simple harmonic motion: displacement, velocity, acceleration, restoring force, energy, period and frequency

::: definition Simple harmonic motion
A body executes **simple harmonic motion** when its acceleration (equivalently, the
restoring force on it) is directly proportional to its displacement from a fixed mean
position and always directed towards that position: $F = -kx$, $a = -\omega^2x$.
:::

The solution of $a = -\omega^2x$ is

$$ x = A\sin(\omega t + \phi) $$

| Term | Meaning |
|---|---|
| $A$ | **amplitude** — the greatest displacement from the mean position |
| $\omega t + \phi$ | **phase** — tells the position and direction of motion at time $t$ |
| $\phi$ | **initial phase (epoch)** — the phase at $t = 0$ |
| $\omega = \sqrt{k/m}$ | **angular frequency** (rad s⁻¹) |
| $T = 2\pi/\omega$ | **period**; $f = 1/T = \omega/2\pi$ is the **frequency** (Hz) |

Every SHM is periodic, but not every periodic motion is SHM (the Earth's orbit, a
bouncing ball). SHM is the **projection of uniform circular motion** on a diameter: a
point moving round a circle of radius $A$ at angular speed $\omega$ has a shadow on a
diameter that moves exactly as $x = A\sin(\omega t + \phi)$.

### Velocity and acceleration

$$ v = \frac{dx}{dt} = A\omega\cos(\omega t + \phi) = \pm\,\omega\sqrt{A^2 - x^2}, \qquad a = -\omega^2x $$

| | At the mean position ($x = 0$) | At an extreme ($x = \pm A$) |
|---|---|---|
| Speed | maximum, $v_{max} = A\omega$ | zero |
| Acceleration and restoring force | zero | maximum, $a_{max} = A\omega^2$, $F_{max} = kA$ |
| Kinetic energy | maximum | zero |
| Potential energy | zero (minimum) | maximum |

**Phase relations:** velocity leads displacement by $\pi/2$; acceleration leads
velocity by $\pi/2$; acceleration and displacement are in **antiphase** ($\pi$ apart).
The $v$–$x$ graph is an ellipse (a circle if $v$ is plotted in units of $\omega$); the
$a$–$x$ graph is a straight line of slope $-\omega^2$ through the origin.

```figure caption="Displacement, velocity and acceleration in SHM over one period. Velocity is greatest when the displacement is zero; acceleration is always opposite to the displacement."
import numpy as np, matplotlib.pyplot as plt
fig, axs = plt.subplots(3, 1, figsize=(4.8,3.6), sharex=True)
t = np.linspace(0, 1.0, 400); w = 2*np.pi
data = [(np.sin(w*t), 'x', ACCENT, 'A'), (np.cos(w*t), 'v', '#0B6A62', 'Aω'), (-np.sin(w*t), 'a', '#A8271F', 'Aω²')]
for ax, (y, lab, c, amp) in zip(axs, data):
    ax.plot(t, y, color=c, lw=1.9)
    ax.axhline(0, color=MUTED, lw=0.7)
    ax.set_ylim(-1.35, 1.35); ax.set_yticks([-1, 1]); ax.set_yticklabels(['−'+amp, '+'+amp])
    ax.set_ylabel(lab, rotation=0, labelpad=12, va='center')
    ax.spines[['top','right']].set_visible(False)
    for q in (0.25, 0.5, 0.75): ax.axvline(q, color=GRID, lw=0.8, zorder=0)
axs[-1].set_xticks([0, 0.25, 0.5, 0.75, 1.0]); axs[-1].set_xticklabels(['0', 'T/4', 'T/2', '3T/4', 'T'])
axs[-1].set_xlabel('time')
fig.subplots_adjust(hspace=0.25)
```

### Energy in SHM

With $k = m\omega^2$:

$$ K = \frac{1}{2}m\omega^2(A^2 - x^2), \qquad U = \frac{1}{2}m\omega^2x^2, \qquad E = K + U = \frac{1}{2}m\omega^2A^2 = \frac{1}{2}kA^2 $$

The total energy is constant and proportional to the **square of the amplitude** and
to the **square of the frequency**. $K = U$ when $x = A/\sqrt{2}$. At $x = A/2$,
$U = E/4$ and $K = 3E/4$. Kinetic and potential energy each vary **periodically with
twice the frequency** of the motion (period $T/2$), because each reaches its maximum
twice per cycle.

```figure caption="Energy against displacement in SHM. The potential energy is a parabola, the kinetic energy an inverted parabola, and their sum is constant; they are equal at x = ±A/√2."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6,2.7))
x = np.linspace(-1, 1, 300)
ax.plot(x, x**2, color=ACCENT, lw=1.9, label='potential energy U')
ax.plot(x, 1 - x**2, color='#A8271F', lw=1.9, label='kinetic energy K')
ax.plot(x, np.ones_like(x), color=INK, lw=1.4, ls=(0,(4,2)), label='total E')
for s in (-1, 1):
    xe = s/np.sqrt(2)
    ax.plot([xe, xe], [0, 0.5], color=MUTED, lw=0.8, ls=':')
    ax.plot([xe], [0.5], 'o', color=INK, ms=4)
ax.set_xticks([-1, -1/np.sqrt(2), 0, 1/np.sqrt(2), 1]); ax.set_xticklabels(['−A', '−A/√2', '0', 'A/√2', 'A'])
ax.set_yticks([0, 0.5, 1]); ax.set_yticklabels(['0', 'E/2', 'E'])
ax.set_xlabel('displacement  x'); ax.set_ylabel('energy')
ax.set_xlim(-1.08, 1.08); ax.set_ylim(0, 1.5)
ax.spines[['top','right']].set_visible(False)
ax.legend(loc='upper center', ncol=3, fontsize=8, frameon=False)
```

::: example Worked example 5.3 — reading an SHM equation
**Problem.** A particle moves as $x = 0.1\sin(4\pi t)$ (metres, seconds). Find the
amplitude, frequency, period, maximum speed and maximum acceleration.

**Solution.** $A = 0.1$ m; $\omega = 4\pi$ rad s⁻¹, so $f = \omega/2\pi = 2$ Hz and
$T = 0.5$ s. $v_{max} = A\omega = 0.4\pi = 1.26$ m s⁻¹;
$a_{max} = A\omega^2 = 1.6\pi^2 = 15.8$ m s⁻².
:::

::: tip Time inside one oscillation
From the mean position, the particle reaches $x = A/2$ in $T/12$ (since $\sin\omega t = \frac{1}{2}$
at $\omega t = \pi/6$) and then needs another $T/6$ to reach $x = A$. It moves fastest
near the middle and slowly near the ends — so a pendulum spends most of its time near
the extremes.
:::


::: example Worked example — reading a turning point from an SHM energy split
A particle in SHM has total energy 16 J. At a displacement of half the amplitude (x = A/2), find the kinetic and potential energies.

Potential energy varies as x² and equals the total at x = A, so at A/2 it is (1/2)² = **¼** of the total: PE = 4 J, KE = **12 J**. The same square law settles the favourite variants: KE = PE when x = A/√2 (≈ 0.71A, *not* at A/2), and at x = A/√2 the speed is vmax/√2. Most wrong answers here come from treating PE as proportional to x instead of x².
:::

::: caution Trap — what the pendulum's period ignores
T = 2π√(l/g) contains **no mass and no amplitude** (for small swings): a heavier bob or a slightly wider swing does not change the period — the two most common distractors in this unit. What does change it: length, g (longer on the Moon/top of a mountain, shorter in a lift accelerating upward... where effective g becomes g + a) and, for the spring–mass system instead, the mass and the spring constant.
:::

## 5.4 Simple pendulum and spring–mass system; forced oscillation and resonance

### Simple pendulum

A point mass (bob) on a light, inextensible string of length $l$, displaced by a small
angle $\theta$, feels a restoring force $mg\sin\theta \approx mg\theta = mg\,x/l$ along
its arc. This is SHM with $\omega^2 = g/l$:

$$ T = 2\pi\sqrt{\frac{l}{g}} $$

valid for **small amplitudes** (a few degrees). $T$ does not depend on the mass of the
bob, nor (for small swings) on the amplitude — the isochronism of the pendulum. $l$ is
measured from the point of suspension to the **centre** of the bob.

| Change | Effect on $T = 2\pi\sqrt{l/g}$ |
|---|---|
| Length × 4 | $T$ × 2 ($T \propto \sqrt{l}$) |
| Heavier bob, same length | no change |
| On the Moon ($g/6$) | $T \times \sqrt{6} \approx 2.45$ |
| Lift accelerating **up** at $a$ (or descending and slowing) | $T = 2\pi\sqrt{l/(g + a)}$ — shorter |
| Lift accelerating **down** at $a$ | $T = 2\pi\sqrt{l/(g - a)}$ — longer |
| Freely falling lift or orbiting satellite | no restoring force: no oscillation ($T \to \infty$) |
| Summer (metal rod expands) | $l$ rises, $T$ rises: a pendulum clock **loses** time |
| Clock taken up Mount Everest or down a deep mine | $g$ smaller, $T$ longer: the clock **loses** time |

The **seconds pendulum** has a period of 2 s (each swing 1 s); its length is
$l = gT^2/4\pi^2 \approx 0.99$ m for $g = 9.8$ m s⁻² (exactly 1 m if $g = \pi^2$ m s⁻²).

### Spring–mass system

A mass $m$ on a spring of force constant $k$ (Hooke's law $F = -kx$):

$$ T = 2\pi\sqrt{\frac{m}{k}}, \qquad f = \frac{1}{2\pi}\sqrt{\frac{k}{m}} $$

- $T$ does **not** depend on $g$: the same on the Moon, in a lift or on a slope
  (horizontal or vertical spring alike).
- For a vertical spring with static extension $e = mg/k$: $T = 2\pi\sqrt{e/g}$.
- To double $T$, put on four times the mass.

| Springs combined | Effective force constant | Period with mass $m$ |
|---|---|---|
| Two springs $k_1$, $k_2$ in **series** | $\frac{1}{k} = \frac{1}{k_1} + \frac{1}{k_2}$ (two equal: $k/2$) | larger ($\sqrt{2}T$ for two equal) |
| Two springs in **parallel** | $k = k_1 + k_2$ (two equal: $2k$) | smaller ($T/\sqrt{2}$ for two equal) |
| Spring cut into $n$ equal pieces | each piece has $nk$ (half a spring is twice as stiff) | one piece: $T/\sqrt{n}$ |

::: example Worked example 5.4 — pendulum and spring
**Problem.** (a) A pendulum beats exactly 2 s on Earth. What is its period on the
Moon, where $g$ is one-sixth? (b) A 1 kg mass on a spring of force constant
400 N m⁻¹. Find the period. (c) A mass hung on a vertical spring stretches it by
9.8 cm. Find the period of vertical oscillation ($g = 9.8$ m s⁻²).

**Solution.** (a) $T \propto 1/\sqrt{g}$: $2\sqrt{6} = 4.9$ s.
(b) $T = 2\pi\sqrt{1/400} = \pi/10 = 0.31$ s.
(c) $T = 2\pi\sqrt{e/g} = 2\pi\sqrt{0.098/9.8} = 2\pi(0.1) = 0.63$ s. A spring clock would keep
the same time on the Moon; a pendulum clock would not.
:::

::: caution Pendulum versus spring
$T = 2\pi\sqrt{l/g}$ depends on $g$ but not on mass; $T = 2\pi\sqrt{m/k}$ depends on
mass but not on $g$. Options that mix these up — "the pendulum's period doubles if the
mass is doubled", "the spring's period changes on the Moon" — are the usual traps.
:::

### Damped, free and forced oscillations; resonance

- **Free (natural) oscillation:** a system displaced and released oscillates at its own
  **natural frequency** $f_0$, fixed by its build ($\sqrt{k/m}/2\pi$ or $\sqrt{g/l}/2\pi$).
- **Damped oscillation:** friction and air resistance take energy away, so the
  **amplitude decreases** with time (the frequency stays almost the same). Shock
  absorbers in vehicles damp the oscillations of the springs on purpose.
- **Forced oscillation:** a periodic external force drives the system; after a while it
  oscillates at the **frequency of the driving force**, not at its own.
- **Resonance:** when the driving frequency equals (or is very close to) the natural
  frequency, the system absorbs energy most readily and the amplitude becomes **maximum**.
  The smaller the damping, the taller and sharper the resonance peak.

```figure caption="Amplitude of a forced oscillator against the driving frequency f, for three amounts of damping. Resonance occurs at the natural frequency $f_0$; light damping gives a tall, sharp peak."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,2.8))
r = np.linspace(0.01, 2.0, 600)
for z, c, lab in [(0.06, '#A8271F', 'light damping'), (0.15, ACCENT, 'moderate'), (0.45, MUTED, 'heavy damping')]:
    A = 1/np.sqrt((1 - r**2)**2 + (2*z*r)**2)
    ax.plot(r, A, color=c, lw=1.8, label=lab)
ax.axvline(1.0, color=INK, lw=0.8, ls=':')
ax.set_xticks([0, 1, 2]); ax.set_xticklabels(['0', 'f₀', '2f₀'])
ax.set_yticks([])
ax.set_xlabel('driving frequency  f'); ax.set_ylabel('amplitude')
ax.set_xlim(0, 2.0); ax.set_ylim(0, 9.5)
ax.spines[['top','right']].set_visible(False)
ax.legend(loc='upper right', fontsize=8, frameon=False)
```

**Examples of resonance:** a swing pushed in step with its own rhythm goes higher and
higher; soldiers **break step** when marching across a suspension bridge so that their
rhythm cannot drive it at its natural frequency; a singer's sustained note at the right
pitch can shatter a wine glass; a radio or TV set is *tuned* by adjusting the natural
frequency of its circuit to that of the station (electrical resonance, Chapter 16);
in an earthquake, buildings whose natural frequency matches the frequency of the ground
shaking sway most violently.

## Formula and fact sheet

| Topic | Formula or fact |
|---|---|
| Angular quantities | $\theta = s/r$; $\omega = 2\pi/T = 2\pi f = 2\pi N/60$; $v = r\omega$; $a_t = r\alpha$ |
| Centripetal | $a = v^2/r = \omega^2r = v\omega$; $F = mv^2/r$; does no work |
| Level road | $v_{max} = \sqrt{\mu rg}$ |
| Banking / cyclist / conical pendulum | $\tan\theta = v^2/rg$; conical pendulum $T = 2\pi\sqrt{L\cos\theta/g}$ |
| Banked road with friction | $v_{max} = \sqrt{rg(\mu + \tan\theta)/(1 - \mu\tan\theta)}$ |
| Hump / dip | $N = mg \mp mv^2/r$; leaves a hump at $v = \sqrt{gr}$ |
| Vertical circle (string) | $v_{top} \ge \sqrt{gr}$, $v_{side} \ge \sqrt{3gr}$, $v_{bottom} \ge \sqrt{5gr}$; $T_b - T_t = 6mg$ |
| Vertical circle (rod) | $v_{bottom} \ge 2\sqrt{gr}$ |
| SHM | $a = -\omega^2x$; $x = A\sin(\omega t + \phi)$; $v = \omega\sqrt{A^2 - x^2}$ |
| SHM maxima | $v_{max} = A\omega$ (mean position); $a_{max} = A\omega^2$ (extremes) |
| Phases | $v$ leads $x$ by $\pi/2$; $a$ and $x$ differ by $\pi$ |
| SHM energy | $E = \frac{1}{2}m\omega^2A^2 = \frac{1}{2}kA^2$; $K = U$ at $A/\sqrt{2}$; energies vary at $2f$ |
| Simple pendulum | $T = 2\pi\sqrt{l/g}$; seconds pendulum $T = 2$ s, $l \approx 0.99$ m; in lift $g \to g \pm a$ |
| Spring–mass | $T = 2\pi\sqrt{m/k} = 2\pi\sqrt{e/g}$; series $1/k = 1/k_1 + 1/k_2$; parallel $k_1 + k_2$; $n$ pieces $nk$ each |
| Resonance | driving frequency = natural frequency → maximum amplitude; less damping, sharper peak |

## Chapter summary

- In uniform circular motion speed is constant but velocity is not; the acceleration
  $v^2/r = \omega^2r$ points to the centre, and the centripetal force does no work.
- The centripetal force is supplied by a real force: friction on a level road
  ($v_{max} = \sqrt{\mu rg}$), the normal reaction on a banked road
  ($\tan\theta = v^2/rg$), tension, gravity.
- In a vertical circle on a string the least speeds are $\sqrt{gr}$ at the top and
  $\sqrt{5gr}$ at the bottom; the tension is greatest at the bottom, by $6mg$ more than
  at the top.
- SHM: acceleration $= -\omega^2\times$ displacement; $x = A\sin(\omega t + \phi)$,
  $v = \omega\sqrt{A^2 - x^2}$; speed is greatest at the mean position, acceleration
  at the extremes.
- Total energy $\frac{1}{2}m\omega^2A^2$ is constant; KE = PE at $x = A/\sqrt{2}$;
  each form of energy oscillates at twice the frequency.
- Simple pendulum $T = 2\pi\sqrt{l/g}$ (independent of mass, depends on $g$); spring
  $T = 2\pi\sqrt{m/k}$ (depends on mass, independent of $g$).
- Springs in series are softer, in parallel stiffer; half a spring is twice as stiff.
- Forced oscillations take the driver's frequency; at resonance (driving frequency =
  natural frequency) the amplitude is greatest, more sharply so with less damping.

## Practice questions

**Set A — Recall (22 questions)**

1. The SI unit of angular velocity is
   (a) rad s⁻¹ (b) m s⁻¹ (c) rad s⁻² (d) rev
2. For a body in uniform circular motion, the quantity that stays constant is its
   (a) velocity (b) acceleration (c) speed (d) linear momentum
3. The centripetal acceleration of a body moving with speed v in a circle of radius r is
   (a) $v/r$ (b) $v^{2}r$ (c) $vr^{2}$ (d) $v^{2}/r$
4. The centripetal acceleration of a body in uniform circular motion is directed
   (a) along the tangent (b) towards the centre (c) away from the centre (d) perpendicular to the plane of the circle
5. The work done by the centripetal force on a body in one complete revolution is
   (a) $mv^{2}$ (b) $2\pi rF$ (c) zero (d) $\frac{1}{2}mv^{2}$
6. Centrifugal force is
   (a) a pseudo force observed in a rotating frame (b) the reaction to the centripetal force (c) a real force that pulls bodies outward (d) another name for gravity
7. The least speed that a stone on a string of length r must have at the highest point to complete a vertical circle is
   (a) zero (b) $\sqrt{gr}$ (c) $\sqrt{3gr}$ (d) $\sqrt{5gr}$
8. The least speed that a stone on a string of length r must have at the lowest point to complete a vertical circle is
   (a) $\sqrt{2gr}$ (b) $\sqrt{gr}$ (c) $\sqrt{3gr}$ (d) $\sqrt{5gr}$
9. A road is banked at angle θ so that vehicles can turn at speed v on a curve of radius r without needing friction. Then
   (a) $\tan\theta = v^{2}/rg$ (b) $\sin\theta = v^{2}/rg$ (c) $\tan\theta = rg/v^{2}$ (d) $\cos\theta = v^{2}/rg$
10. The greatest speed at which a car can take a level curve of radius r, if the coefficient of friction is μ, is
   (a) $\mu rg$ (b) $\sqrt{rg/\mu}$ (c) $\sqrt{\mu rg}$ (d) $\sqrt{\mu g/r}$
11. A motion is simple harmonic when the acceleration is
   (a) constant (b) proportional to the displacement and directed towards the mean position (c) proportional to the velocity (d) proportional to the square of the displacement
12. In SHM, the speed of the particle is greatest
   (a) at the extreme positions (b) halfway between the mean and an extreme (c) nowhere — it is constant (d) at the mean position
13. In SHM, the acceleration of the particle is greatest
   (a) at the extreme positions (b) at the mean position (c) halfway between the mean and an extreme (d) nowhere — it is constant
14. The phase difference between the displacement and the acceleration of a particle in SHM is
   (a) zero (b) π/4 (c) π/2 (d) π
15. The total energy of a particle in SHM is proportional to the
   (a) amplitude (b) square of the amplitude (c) square root of the amplitude (d) cube of the amplitude
16. The period of a simple pendulum of length l is
   (a) $2\pi\sqrt{g/l}$ (b) $2\pi\sqrt{l/g}$ (c) $\frac{1}{2\pi}\sqrt{l/g}$ (d) $2\pi lg$
17. The period of a mass m attached to a spring of force constant k is
   (a) $2\pi\sqrt{k/m}$ (b) $\frac{1}{2\pi}\sqrt{m/k}$ (c) $2\pi\sqrt{mk}$ (d) $2\pi\sqrt{m/k}$
18. The period of a seconds pendulum is
   (a) 2 s (b) 1 s (c) 0.5 s (d) 60 s
19. Resonance occurs when the frequency of the driving force
   (a) is twice the natural frequency (b) is half the natural frequency (c) equals the natural frequency of the system (d) is zero
20. In a damped oscillation, with time
   (a) the frequency increases steadily (b) the amplitude decreases (c) the amplitude increases (d) the total energy stays constant
21. The phase difference between the velocity and the displacement of a particle in SHM is
   (a) π (b) zero (c) π/2 (d) 2π
22. The angular velocity ω of a body completing one revolution in time T is
   (a) $2\pi T$ (b) $T/2\pi$ (c) $\pi/T$ (d) $2\pi/T$

::: note Answers and explanations — Set A
**1.** (a) — angle (radian) per second. rad s⁻² is angular acceleration.
**2.** (c) — the direction of motion changes all the time, so velocity, momentum and the acceleration vector change; only the speed (and KE) stay constant.
**3.** (d) — $a = v^2/r = \omega^2r$.
**4.** (b) — it is centre-seeking (centripetal); the velocity is along the tangent.
**5.** (c) — the force is perpendicular to the velocity at every instant, so it does no work in any part of the motion.
**6.** (a) — it is a fictitious force felt in a rotating (non-inertial) frame; the centripetal force has no outward "reaction" acting on the same body.
**7.** (b) — at the top the string is just slack when $mg = mv^2/r$, giving $v = \sqrt{gr}$. Zero is the answer for a rigid rod.
**8.** (d) — energy: $v_b^2 = v_t^2 + 4gr = gr + 4gr = 5gr$.
**9.** (a) — $N\cos\theta = mg$ and $N\sin\theta = mv^2/r$; dividing, $\tan\theta = v^2/rg$.
**10.** (c) — friction supplies the centripetal force: $\mu mg = mv^2/r$, so $v = \sqrt{\mu rg}$.
**11.** (b) — the defining condition of SHM: $a = -\omega^2x$.
**12.** (d) — $v = \omega\sqrt{A^2 - x^2}$ is greatest, $A\omega$, at $x = 0$.
**13.** (a) — $|a| = \omega^2|x|$ is greatest, $A\omega^2$, at $x = \pm A$, where the particle is momentarily at rest.
**14.** (d) — $a = -\omega^2x$: acceleration is always opposite to displacement, a phase difference of $\pi$.
**15.** (b) — $E = \frac{1}{2}m\omega^2A^2$; double the amplitude, four times the energy.
**16.** (b) — $T = 2\pi\sqrt{l/g}$ for small swings. (a) has $l$ and $g$ the wrong way round: $\sqrt{l/g}$ has the unit of time, $\sqrt{g/l}$ of frequency.
**17.** (d) — $\omega = \sqrt{k/m}$, so $T = 2\pi/\omega = 2\pi\sqrt{m/k}$.
**18.** (a) — a seconds pendulum takes 1 s for each swing, so its full period is 2 s.
**19.** (c) — at resonance the driver is in step with the natural oscillation and the amplitude is greatest.
**20.** (b) — resistive forces remove energy, so the amplitude dies away; the frequency changes very little.
**21.** (c) — $v = A\omega\cos(\omega t + \phi) = A\omega\sin(\omega t + \phi + \pi/2)$: velocity leads displacement by $\pi/2$.
**22.** (d) — one revolution is $2\pi$ rad in time $T$, so $\omega = 2\pi/T$.
:::

**Set B — Understanding (14 questions)**

1. A car turns a corner on a level road. The centripetal force on it is provided by
   (a) the weight of the car (b) the normal reaction of the road (c) the friction between the tyres and the road (d) the engine
2. The speed of a body moving in a circle of fixed radius is doubled. The centripetal force needed becomes
   (a) twice (b) half (c) four times (d) one quarter
3. For a stone whirled in a vertical circle on a string, the tension at the lowest point exceeds that at the highest point by
   (a) 6mg (b) 2mg (c) 4mg (d) mg
4. A pendulum clock that keeps correct time in Kathmandu is taken to the top of Mount Everest. There it will
   (a) gain time, because g is smaller (b) keep correct time (c) stop completely (d) lose time, because g is smaller
5. A mass–spring system and a simple pendulum both have a period of 1 s on the Earth. On the Moon,
   (a) both periods are unchanged (b) the spring's period is unchanged and the pendulum's increases (c) the pendulum's period is unchanged and the spring's increases (d) both periods increase
6. A simple pendulum is suspended in a lift. Its period decreases when the lift
   (a) moves up with uniform velocity (b) accelerates downward (c) falls freely (d) accelerates upward
7. A simple pendulum is suspended in a freely falling lift. It will
   (a) oscillate with its usual period (b) oscillate faster (c) not oscillate at all (d) oscillate more slowly but still regularly
8. In SHM of amplitude A, the kinetic and potential energies are equal at a displacement of
   (a) A/2 (b) A/√2 (c) A/4 (d) A
9. The amplitude of a particle in SHM is doubled, with no other change. Its period
   (a) is unchanged and its total energy becomes four times (b) doubles and its energy doubles (c) is halved and its energy becomes four times (d) is unchanged and its energy doubles
10. A mass m on a spring of force constant k oscillates with period T. The spring is cut into two equal halves and the same mass is hung from one half. The new period is
   (a) √2 T (b) 2T (c) T/√2 (d) T/2
11. A particle executes SHM with frequency f. Its kinetic energy varies periodically with frequency
   (a) f/2 (b) f (c) 4f (d) 2f
12. Soldiers are ordered to break step when crossing a suspension bridge so that
   (a) the bridge is not set into resonance (b) the bridge carries less weight (c) they reach the other side faster (d) friction on the bridge is reduced
13. For a particle in SHM, the graph of acceleration against displacement is
   (a) a parabola (b) a circle (c) a straight line of positive slope through the origin (d) a straight line of negative slope through the origin
14. A car goes over the top of a convex (humped) bridge at speed v. The normal force of the road on the car there is
   (a) greater than its weight (b) less than its weight (c) equal to its weight (d) zero at any speed

::: note Answers and explanations — Set B
**1.** (c) — on a level road only static friction acts towards the centre; that is why cars skid on wet or icy bends.
**2.** (c) — $F = mv^2/r$; doubling $v$ makes $F$ four times.
**3.** (a) — $T_b = mv_b^2/r + mg$, $T_t = mv_t^2/r - mg$ and $v_b^2 - v_t^2 = 4gr$; subtracting gives $6mg$.
**4.** (d) — $g$ is smaller on the summit, so $T = 2\pi\sqrt{l/g}$ is longer; the clock ticks fewer times per hour and loses time. (a) has the right reason but the wrong result.
**5.** (b) — $T = 2\pi\sqrt{m/k}$ does not contain $g$; $T = 2\pi\sqrt{l/g}$ grows when $g$ falls.
**6.** (d) — accelerating upward, the effective $g$ is $g + a$, so $T = 2\pi\sqrt{l/(g + a)}$ is shorter. Uniform velocity changes nothing.
**7.** (c) — in free fall the effective $g$ is zero, so there is no restoring force; the bob stays wherever it is relative to the lift.
**8.** (b) — $\frac{1}{2}m\omega^2x^2 = \frac{1}{2}m\omega^2(A^2 - x^2)$ gives $x^2 = A^2/2$. At $A/2$, $U$ is only one quarter of $E$.
**9.** (a) — the period of SHM is independent of amplitude; the energy $\frac{1}{2}m\omega^2A^2$ goes as $A^2$.
**10.** (c) — half a spring has force constant $2k$, so $T' = 2\pi\sqrt{m/2k} = T/\sqrt{2}$.
**11.** (d) — $K = \frac{1}{2}m\omega^2A^2\cos^2(\omega t)$ and $\cos^2$ repeats twice per cycle, so KE oscillates at $2f$.
**12.** (a) — a regular marching rhythm close to the bridge's natural frequency could build up a dangerously large resonant oscillation.
**13.** (d) — $a = -\omega^2x$ is a straight line through the origin with slope $-\omega^2$.
**14.** (b) — at the top, $mg - N = mv^2/r$, so $N = mg - mv^2/r$; the car feels lighter and loses contact if $v$ reaches $\sqrt{gr}$.
:::

**Set C — Application (12 questions)**

1. A 0.5 kg stone tied to a string 1 m long is whirled in a horizontal circle at 2 revolutions per second. The tension in the string is about
   (a) 2 N (b) 79 N (c) 6.3 N (d) 158 N
2. A car moves at 10 m s⁻¹ round a curve of radius 20 m. Its centripetal acceleration is
   (a) 5 m s⁻² (b) 2 m s⁻² (c) 0.5 m s⁻² (d) 200 m s⁻²
3. The coefficient of friction between the tyres and a level road is 0.4. The greatest speed at which a car can take a curve of radius 100 m is (g = 10 m s⁻²)
   (a) 50 m s⁻¹ (b) 4 m s⁻¹ (c) 32 m s⁻¹ (d) 20 m s⁻¹
4. A curve of radius 40 m is banked at 45°. The speed at which a car can take it with no need for friction is (g = 10 m s⁻²)
   (a) 400 m s⁻¹ (b) 20 m s⁻¹ (c) 14 m s⁻¹ (d) 28 m s⁻¹
5. A stone tied to a string 2 m long is to be whirled in a vertical circle (g = 10 m s⁻²). The least speed it must have at the lowest point is
   (a) 4.5 m s⁻¹ (b) 7.7 m s⁻¹ (c) 10 m s⁻¹ (d) 20 m s⁻¹
6. A car crosses the top of a humped bridge whose radius of curvature is 40 m (g = 10 m s⁻²). It just loses contact with the road at a speed of
   (a) 20 m s⁻¹ (b) 400 m s⁻¹ (c) 6.3 m s⁻¹ (d) 40 m s⁻¹
7. The displacement of a particle is $x = 0.05\sin(10t)$ metres (t in s). Its maximum acceleration is
   (a) 0.5 m s⁻² (b) 50 m s⁻² (c) 0.05 m s⁻² (d) 5 m s⁻²
8. A particle executes SHM of amplitude 10 cm and period π s. Its speed when it is 6 cm from the mean position is
   (a) 8 cm s⁻¹ (b) 12 cm s⁻¹ (c) 16 cm s⁻¹ (d) 20 cm s⁻¹
9. A 1 kg mass oscillates on a spring of force constant 400 N m⁻¹. Its period is about
   (a) 0.05 s (b) 0.31 s (c) 3.14 s (d) 0.63 s
10. A pendulum has a period of 2 s on the Earth. On the Moon, where g is one-sixth of its value on Earth, its period is about
   (a) 4.9 s (b) 12 s (c) 0.82 s (d) 2 s
11. A 0.1 kg particle executes SHM with amplitude 0.1 m and angular frequency 10 rad s⁻¹. Its total energy is
   (a) 0.5 J (b) 0.005 J (c) 0.1 J (d) 0.05 J
12. A particle in SHM has a period of 2.4 s. The least time it takes to move from the mean position to half the amplitude is
   (a) 0.6 s (b) 0.4 s (c) 0.2 s (d) 1.2 s

::: note Answers and explanations — Set C
**1.** (b) — $\omega = 2\pi f = 4\pi$ rad s⁻¹; $T = m\omega^2r = 0.5(16\pi^2)(1) = 79$ N. (c) uses $\omega$ instead of $\omega^2$.
**2.** (a) — $a = v^2/r = 100/20 = 5$ m s⁻². (c) is $v/r$, (b) is $r/v$ and (d) is $vr$; only $v^2/r$ has the unit of acceleration.
**3.** (d) — $v = \sqrt{\mu rg} = \sqrt{0.4\times100\times10} = 20$ m s⁻¹ (72 km h⁻¹). (c) forgets $\mu$; (a) divides by $\mu$ instead of multiplying.
**4.** (b) — $v = \sqrt{rg\tan\theta} = \sqrt{40\times10\times1} = 20$ m s⁻¹. (a) forgets the square root.
**5.** (c) — $v_{min} = \sqrt{5gr} = \sqrt{5\times10\times2} = 10$ m s⁻¹. (a) is $\sqrt{gr}$, the least speed at the top, and (b) is $\sqrt{3gr}$, at the side.
**6.** (a) — contact is lost when $mg = mv^2/r$: $v = \sqrt{gr} = \sqrt{400} = 20$ m s⁻¹.
**7.** (d) — $A = 0.05$ m, $\omega = 10$ rad s⁻¹; $a_{max} = A\omega^2 = 0.05\times100 = 5$ m s⁻². (a) is the maximum speed $A\omega$.
**8.** (c) — $\omega = 2\pi/T = 2$ rad s⁻¹; $v = \omega\sqrt{A^2 - x^2} = 2\sqrt{100 - 36} = 16$ cm s⁻¹. (a) forgets to multiply by $\omega$.
**9.** (b) — $T = 2\pi\sqrt{m/k} = 2\pi\sqrt{1/400} = 2\pi/20 = 0.31$ s.
**10.** (a) — $T \propto 1/\sqrt{g}$: $T = 2\sqrt{6} = 4.9$ s. (b) multiplies by 6 instead of $\sqrt{6}$; (c) divides.
**11.** (d) — $E = \frac{1}{2}m\omega^2A^2 = \frac{1}{2}(0.1)(100)(0.01) = 0.05$ J.
**12.** (c) — $x = A\sin\omega t = A/2$ at $\omega t = \pi/6$, i.e. $t = T/12 = 2.4/12 = 0.2$ s. (b) is $T/6$, the time from $A/2$ on to $A$.
:::
