---
subject: Physics
grade: CEE
unit: 2
title: "Dynamics: Force, Momentum, Work, Energy and Power"
hours: 2
area: Mechanics
---

Dynamics asks *why* bodies move as they do: forces change momentum, forces do work,
and work changes energy. Of the **10 Mechanics questions** in the Physics paper
(official), we estimate about **2** come from this chapter. They are built on a few
patterns that repeat year after year: the reading of a weighing machine in a lift,
recoil of a gun, impulse from a force–time graph, the link $K = p^2/2m$, power of a
pump or a vehicle, velocities after a collision, and friction on a level road or an
inclined plane.

::: key What the paper asks from this chapter
- Newton's laws: inertia, $F = dp/dt$, action–reaction on *different* bodies; free-body diagrams.
- Apparent weight in a lift, connected bodies and the Atwood machine; Lami's theorem for three forces in equilibrium.
- Impulse = change in momentum = area under the $F$–$t$ graph; conservation of momentum (recoil, explosions, rockets).
- $W = Fs\cos\theta$; work–energy theorem; $K = p^2/2m$; conservation of mechanical energy; $P = Fv$.
- Collisions: elastic and inelastic, coefficient of restitution, equal-mass exchange, kinetic-energy loss.
- Friction: $f \le \mu_sN$, $f_k = \mu_kN$, $\mu_s = \tan\theta_{repose}$, motion on rough inclines.
:::

## 2.1 Newton's laws of motion and the conditions of equilibrium

### The three laws

| Law | Statement | What it gives |
|---|---|---|
| First (law of inertia) | A body stays at rest or in uniform motion in a straight line unless an external net force acts on it. | The idea of **inertia** and a qualitative definition of force; defines inertial frames |
| Second | The rate of change of momentum is proportional to the net external force and takes place in its direction: $\vec F = \frac{d\vec p}{dt}$. | $F = ma$ for constant mass; 1 N gives 1 kg an acceleration of 1 m s⁻² |
| Third | To every action there is an equal and opposite reaction. | Forces come in pairs, acting on **two different bodies** |

**Inertia** is the tendency of a body to resist a change in its state of rest or
uniform motion; **mass** is its measure. There is inertia of rest (passengers jerk
back when a bus starts), of motion (they lurch forward when it brakes) and of
direction (they lean outward on a bend).

The first law is contained in the second (put $F = 0$, then $a = 0$), and the second
contains the third's consequence, conservation of momentum. For a system whose mass
changes at a steady speed, $F = v\,\frac{dm}{dt}$ — the force needed to keep a
conveyor belt moving at speed $v$ while sand drops onto it, or the thrust of a
rocket that ejects gas at relative speed $u$: $F = u\,\frac{dm}{dt}$.

::: caution Action and reaction never cancel
They act on different bodies. A book on a table: the weight of the book (Earth
pulls book) and the normal reaction (table pushes book) are equal and opposite and
act on the *same* body — they balance, but they are **not** an action–reaction
pair. The reaction to the book's weight is the book pulling the Earth upward.
:::

### Standard applications

| Situation | Result |
|---|---|
| Lift accelerating **up** at $a$ (or moving down and slowing) | apparent weight $R = m(g + a)$ |
| Lift accelerating **down** at $a$ (or moving up and slowing) | $R = m(g - a)$ |
| Lift at rest or moving at **constant velocity** | $R = mg$ |
| Lift falling freely ($a = g$) | $R = 0$ — weightlessness |
| Atwood machine, masses $m_1 > m_2$ over a light frictionless pulley | $a = \frac{(m_1 - m_2)g}{m_1 + m_2}$, $T = \frac{2m_1m_2g}{m_1 + m_2}$ |
| Two blocks in contact on a smooth floor, force $F$ on $m_1$ | $a = \frac{F}{m_1 + m_2}$; contact force $= \frac{m_2F}{m_1 + m_2}$ |
| Block on a smooth incline of angle $\theta$ | $a = g\sin\theta$ down the slope; $N = mg\cos\theta$ |

The direction of *velocity* never matters for a weighing machine; only the direction
of the *acceleration* does.

::: example Worked example 2.1 — lift and Atwood machine
**Problem.** (a) A 60 kg student stands on a weighing machine in a lift that
accelerates upward at 2 m s⁻². What does the machine read? (b) Masses of 3 kg and
2 kg hang over a light frictionless pulley. Find the acceleration and the tension
($g = 9.8\ \text{m s}^{-2}$).

**Solution.** (a) $R = m(g + a) = 60(9.8 + 2) = 708\ \text{N}$ (it "reads" 72.2 kg).
(b) $a = (3 - 2)(9.8)/5 = 1.96\ \text{m s}^{-2}$;
$T = 2(3)(2)(9.8)/5 = 23.5\ \text{N}$ — between the two weights (19.6 N and 29.4 N),
as it must be.
:::

### Conditions of equilibrium

A body is in **equilibrium** when it has no linear acceleration and no angular
acceleration.

1. **Translational equilibrium:** the vector sum of all external forces is zero,
   $\sum\vec F = 0$ (so $\sum F_x = 0$, $\sum F_y = 0$).
2. **Rotational equilibrium:** the sum of the moments (torques) about **any** point is
   zero, $\sum\tau = 0$ — the **principle of moments**: clockwise moments = anticlockwise
   moments.

A point object needs only the first; a rigid body needs both. A **couple** (two equal,
opposite, parallel forces not in line) has zero resultant force but a non-zero
torque, so it rotates the body without translating it.

**Lami's theorem.** If three concurrent, coplanar forces $P$, $Q$, $R$ keep a body in
equilibrium, each force is proportional to the sine of the angle between the other
two:

$$ \frac{P}{\sin\alpha} = \frac{Q}{\sin\beta} = \frac{R}{\sin\gamma} $$

where $\alpha$ is the angle between $Q$ and $R$, and so on. Three forces in
equilibrium can be drawn as a closed triangle (forces 3 N, 4 N and 5 N in
equilibrium: the 3 N and 4 N forces are at 90°).

::: example Worked example 2.2 — a lamp on a wire
**Problem.** A 20 N lamp hangs from the midpoint of a wire; the two halves of the
wire make 120° with each other. Find the tension in each half.

**Solution.** Each half makes 60° with the vertical. Vertical balance:
$2T\cos60^{\circ} = 20$, so $T = 20\ \text{N}$. (As the wire is pulled straighter, the
angle approaches 180°, $\cos$ of the half-angle approaches zero and $T$ grows without
limit — a wire carrying a load can never be made perfectly horizontal.)
:::

| Type of equilibrium | After a small displacement | Potential energy | Example |
|---|---|---|---|
| Stable | returns | minimum | cone on its base, ball in a bowl |
| Unstable | moves further away | maximum | cone on its tip |
| Neutral | stays in the new position | constant | cone on its side, ball on a level floor |

## 2.2 Impulse, linear momentum and its conservation

**Linear momentum** $\vec p = m\vec v$ (vector, kg m s⁻¹). **Impulse** of a force is
$\vec J = \vec F\,\Delta t$ for a constant force, or $\int\vec F\,dt$ in general; by
the second law it equals the **change in momentum**:

$$ \vec J = \int \vec F\,dt = \vec p_f - \vec p_i = \Delta\vec p $$

Impulse is the **area under the force–time graph**; its unit, N s, equals kg m s⁻¹.
For a given change of momentum, a longer contact time means a smaller average force
— the physics of a cricketer drawing the hands back, airbags, crumple zones,
the sand pit for long jump, and shock absorbers.

```figure caption="Two catches of the same ball. Equal areas under the curves mean equal impulse (the same change of momentum); the catch that lasts longer needs a much smaller peak force."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,2.7))
t = np.linspace(0, 0.06, 600)
def pulse(t, t0, w, area):
    y = np.where((t>t0)&(t<t0+w), np.sin(np.pi*(t-t0)/w), 0.0)
    return area*np.pi/(2*w)*y
f1 = pulse(t, 0.004, 0.008, 3.0); f2 = pulse(t, 0.004, 0.040, 3.0)
ax.fill_between(t*1000, f1, color='#A8271F', alpha=0.18, lw=0)
ax.fill_between(t*1000, f2, color=ACCENT, alpha=0.18, lw=0)
ax.plot(t*1000, f1, color='#A8271F', lw=1.8)
ax.plot(t*1000, f2, color=ACCENT, lw=1.8)
ax.text(12.5, 520, 'stiff hands: 8 ms,\npeak force ≈ 590 N', color='#A8271F', fontsize=8.5, va='center')
ax.text(30, 175, 'hands drawn back: 40 ms,\npeak force ≈ 120 N', color=ACCENT, fontsize=8.5, va='center')
ax.text(46, 420, 'each area = 3 N s', color=INK, fontsize=8.5, ha='center')
ax.set_xlim(0,60); ax.set_ylim(0,650)
ax.set_xlabel('time  t  (ms)'); ax.set_ylabel('force  F  (N)')
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.5)
```

**Useful results.**

- A ball of mass $m$ hitting a wall normally at speed $v$ and rebounding at the same
  speed: $|\Delta p| = 2mv$ (not zero). At angle $\theta$ to the wall's normal:
  $2mv\cos\theta$.
- A machine gun firing $n$ bullets per second, each of mass $m$ at speed $v$, pushes
  back on the gunner with force $F = nmv$.
- **Kinetic energy and momentum:** $K = \frac{p^2}{2m}$, $p = \sqrt{2mK}$. For the
  same momentum the lighter body has more KE; for the same KE the heavier body has
  more momentum.

::: definition Principle of conservation of linear momentum
If the net external force on a system is zero, its total linear momentum stays
constant: $m_1\vec u_1 + m_2\vec u_2 = m_1\vec v_1 + m_2\vec v_2$. Internal forces
(action–reaction pairs inside the system) cannot change the total.
:::

| Application | What is conserved and what follows |
|---|---|
| Recoil of a gun | $0 = mv + MV$, so $V = -mv/M$; the bullet carries far more KE ($K_b/K_g = M/m$) |
| Explosion of a shell at rest | fragments fly apart with momenta that add to zero |
| Rocket and jet propulsion | gases pushed backward, rocket pushed forward; thrust $= u\,dm/dt$ |
| Person jumping off a boat | boat moves backward |
| Collisions | total momentum before = total momentum after (Section 2.4) |

::: example Worked example 2.3 — recoil and impulse
**Problem.** (a) A 5 kg rifle fires a 20 g bullet at 500 m s⁻¹. Find the recoil
speed and the ratio of the kinetic energies of bullet and rifle. (b) A 0.15 kg
ball reaches a bat at 20 m s⁻¹ and leaves along the same line at 30 m s⁻¹; contact
lasts 0.01 s. Find the average force.

**Solution.** (a) $V = mv/M = 0.02(500)/5 = 2\ \text{m s}^{-1}$, backward. Equal
momenta, so $K \propto 1/m$: $K_b/K_g = 5/0.02 = 250$.
(b) Take the final direction as positive: $\Delta p = 0.15(30) - 0.15(-20) = 7.5\ \text{N s}$;
$F = 7.5/0.01 = 750\ \text{N}$. Forgetting the reversal (using $30 - 20$) gives the
wrong 150 N.
:::

## 2.3 Work, energy and power; the work–energy theorem; conservation of energy

### Work

The **work** done by a constant force is the scalar product of force and
displacement:

$$ W = \vec F\cdot\vec s = Fs\cos\theta $$

Unit: joule (1 J = 1 N m); dimensions $[ML^2T^{-2}]$.

| Sign | When | Examples |
|---|---|---|
| Positive ($0 \le \theta < 90^{\circ}$) | force has a component along the motion | gravity on a falling body; the engine force on a car |
| Zero ($\theta = 90^{\circ}$, or no displacement) | force perpendicular to motion | centripetal force in a circle; a porter carrying a load on a level road (against gravity); pushing a wall |
| Negative ($90^{\circ} < \theta \le 180^{\circ}$) | force opposes the motion | kinetic friction; gravity on a body being lifted; brakes |

For a variable force, $W = \int F\,dx$ = **area under the force–displacement graph**.
For a spring obeying $F = kx$, the work to stretch it from $x_1$ to $x_2$ is
$\frac{1}{2}k(x_2^2 - x_1^2)$ — from 0 to $x$ it is $\frac{1}{2}kx^2$.

### Energy and the work–energy theorem

**Kinetic energy** $K = \frac{1}{2}mv^2$; **gravitational potential energy** near the
Earth $U = mgh$; **elastic potential energy** of a spring $U = \frac{1}{2}kx^2$.

::: key Work–energy theorem
The work done by the **net** force on a body equals the change in its kinetic
energy: $W_{net} = K_f - K_i = \frac{1}{2}mv^2 - \frac{1}{2}mu^2$. It holds for any
force, constant or variable, conservative or not.
:::

A **conservative force** does work that depends only on the start and end points, not
on the path; its work round any closed path is zero, and a potential energy can be
defined for it (gravity, the spring force, the electrostatic force). Friction, air
drag and viscous forces are **non-conservative** (dissipative): their work depends on
the path and turns mechanical energy into heat.

**Conservation of mechanical energy.** If only conservative forces do work,
$K + U$ = constant. A body sliding down any *smooth* track of height $h$ reaches the
bottom with $v = \sqrt{2gh}$, whatever the shape of the track. With friction,
$K_i + U_i = K_f + U_f + (\text{work against friction})$. The **law of conservation
of energy** — energy is neither created nor destroyed, only changed from one form to
another — has no exceptions (mass is a form of energy, $E = mc^2$).

### Power

**Power** is the rate of doing work: $P = \frac{dW}{dt}$; for a force on a moving
body $P = \vec F\cdot\vec v = Fv\cos\theta$. Unit: watt (1 W = 1 J s⁻¹);
dimensions $[ML^2T^{-3}]$. 1 horsepower (hp) ≈ 746 W. The **kilowatt hour** is a
unit of *energy*: 1 kWh = 1000 W × 3600 s = 3.6 × 10⁶ J (one "unit" on an NEA bill).
Efficiency = useful output / input.

::: example Worked example 2.4 — pump and vehicle
**Problem.** (a) A motor pumps 600 kg of water into a tank 20 m above it in 2 min.
Find the minimum power ($g = 9.8\ \text{m s}^{-2}$). (b) A car's engine delivers
30 kW. The total resistance on a level road is 1500 N. Find the car's top speed.

**Solution.** (a) $P = mgh/t = 600(9.8)(20)/120 = 980\ \text{W}$ (more in practice,
since the water also leaves with kinetic energy and the motor is not 100 %
efficient). (b) At top speed the driving force equals the resistance, so
$v = P/F = 30\,000/1500 = 20\ \text{m s}^{-1} = 72\ \text{km h}^{-1}$.
:::

::: caution Momentum and kinetic energy change differently
$K = p^2/2m$, so $K \propto p^2$. If $p$ increases by 50 %, $K$ becomes
$1.5^2 = 2.25$ times — an increase of **125 %**, not 50 % or 100 %. If $K$ increases
by 300 % (four times), $p$ doubles — an increase of 100 %.
:::

## 2.4 Elastic and inelastic collisions

In every collision of an isolated system **linear momentum is conserved** and
**total energy is conserved**; what may not be conserved is *kinetic* energy (part
can become heat, sound or deformation).

| | Elastic | Inelastic | Perfectly inelastic |
|---|---|---|---|
| Momentum | conserved | conserved | conserved |
| Kinetic energy | conserved | not conserved (some lost) | not conserved (maximum loss) |
| After impact | separate | separate | move together (stick) |
| Coefficient of restitution $e$ | $e = 1$ | $0 < e < 1$ | $e = 0$ |
| Examples | collisions of atoms, molecules; nearly, of steel or billiard balls | most real collisions | bullet embedding in a block, mud on a wall |

The **coefficient of restitution** is the ratio of the relative speed of separation
to the relative speed of approach (head-on):

$$ e = \frac{v_2 - v_1}{u_1 - u_2} $$

### Elastic collision in one dimension

For $m_1$ at $u_1$ striking $m_2$ at $u_2$ head-on and elastically:

$$ v_1 = \frac{(m_1 - m_2)u_1 + 2m_2u_2}{m_1 + m_2}, \qquad v_2 = \frac{(m_2 - m_1)u_2 + 2m_1u_1}{m_1 + m_2} $$

| Special case (target at rest, $u_2 = 0$) | Result |
|---|---|
| Equal masses | the bodies **exchange velocities**: $v_1 = 0$, $v_2 = u_1$ |
| Very heavy body hits a very light one | heavy continues at $\approx u_1$; light flies off at $\approx 2u_1$ |
| Very light body hits a very heavy one | light rebounds at $\approx -u_1$; heavy hardly moves |
| Fraction of KE given to the target | $\frac{4m_1m_2}{(m_1 + m_2)^2}$ — 100 % when $m_1 = m_2$ |

This last row is why a **moderator** in a reactor uses light nuclei (hydrogen in
water, deuterium in heavy water, carbon in graphite) to slow neutrons: a neutron
loses most energy when it hits a nucleus of nearly its own mass. In an oblique
elastic collision of two equal masses, one at rest, the two move off **at 90° to
each other**.

### Perfectly inelastic collision

The bodies move off together with
$v = \frac{m_1u_1 + m_2u_2}{m_1 + m_2}$. The kinetic energy lost is
$\frac{m_1m_2(u_1 - u_2)^2}{2(m_1 + m_2)}$; with the target at rest the **fraction**
lost is $\frac{m_2}{m_1 + m_2}$ (one half for equal masses).

**Ballistic pendulum:** a bullet of mass $m$ embeds in a block of mass $M$ that
then swings up a height $h$: $v_{bullet} = \frac{m + M}{m}\sqrt{2gh}$ (momentum
conserved in the impact, energy conserved in the swing — never energy in the
impact).

**Bouncing ball:** dropped from height $h$ onto a floor with coefficient $e$, it
rises to $e^2h$; after $n$ bounces, $e^{2n}h$; and $e = \sqrt{h_2/h_1}$.

::: example Worked example 2.5 — elastic and sticking collisions
**Problem.** A 2 kg trolley at 3 m s⁻¹ hits a 1 kg trolley at rest. Find the
velocities after impact if the collision is (a) elastic, (b) perfectly inelastic, and
(c) the kinetic energy lost in (b).

**Solution.** (a) $v_1 = \frac{(2 - 1)3}{3} = 1\ \text{m s}^{-1}$ and
$v_2 = \frac{2(2)(3)}{3} = 4\ \text{m s}^{-1}$. Check: momentum $6 = 2 + 4$; KE
$9 = 1 + 8$ J. (b) $v = 6/3 = 2\ \text{m s}^{-1}$. (c) KE before 9 J, after
$\frac{1}{2}(3)(2^2) = 6$ J: 3 J lost, which is the fraction $\frac{m_2}{m_1 + m_2} = \frac{1}{3}$.
:::

## 2.5 Solid friction: laws, coefficient, angle of friction and angle of repose

**Friction** is the force that opposes relative motion (or attempted motion) between
two surfaces in contact; it acts along the surfaces. It arises from the
interlocking of surface irregularities and the adhesion at the tiny points of true
contact.

- **Static friction** acts when there is no sliding. It is *self-adjusting*: it is
  exactly as large as needed to prevent slipping, up to a maximum.
- **Limiting friction** is that maximum, reached just as sliding begins:
  $f_s = \mu_sN$.
- **Kinetic (dynamic) friction** acts during sliding: $f_k = \mu_kN$, with
  $\mu_k < \mu_s$.
- **Rolling friction** is much smaller than sliding friction — the reason for wheels
  and ball bearings.

```figure caption="Friction against the applied force. Static friction rises to match the push until the limiting value $\mu_sN$; once the block slides, the friction drops to the smaller kinetic value $\mu_kN$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,2.7))
ax.plot([0,6],[0,6], color=ACCENT, lw=2.0)
ax.plot([6,6.35,10],[6,4.6,4.6], color='#A8271F', lw=2.0)
ax.plot([0,6],[6,6], color=MUTED, lw=0.8, ls=':')
ax.plot([0,10],[4.6,4.6], color=MUTED, lw=0.8, ls=':')
ax.text(2.2, 3.6, 'static friction\n(f = applied force)', fontsize=8.5, color=ACCENT, ha='left', va='center')
ax.annotate('limiting friction', xy=(6,6), xytext=(6.9,6.7), fontsize=8.5, color=INK,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.8))
ax.text(8.2, 3.9, 'kinetic friction', fontsize=8.5, color='#A8271F', ha='center')
ax.text(3.0, 7.9, 'no motion', fontsize=8.5, color=MUTED, ha='center')
ax.text(8.2, 7.9, 'sliding', fontsize=8.5, color=MUTED, ha='center')
ax.axvline(6, color=GRID, lw=0.8, ls='--', zorder=0)
ax.set_xlim(0,10); ax.set_ylim(0,8.6)
ax.set_xticks([]); ax.set_yticks([4.6, 6]); ax.set_yticklabels(['$\\mu_k N$', '$\\mu_s N$'])
ax.set_xlabel('applied force  F'); ax.set_ylabel('friction  f')
ax.spines[['top','right']].set_visible(False)
```

### Laws of limiting friction

1. Friction acts along the common surface, opposite to the (attempted) relative
   motion.
2. Limiting friction is proportional to the normal reaction: $f_s = \mu_sN$.
3. It is **independent of the apparent area of contact** (for the same normal
   reaction).
4. It depends on the nature and condition of the surfaces (material, roughness,
   lubrication).
5. Kinetic friction is nearly independent of the speed (for moderate speeds) and is
   less than limiting friction.

The **coefficient of friction** $\mu = f/N$ is a dimensionless ratio. It is usually
below 1 but can exceed 1 for very clean or sticky surfaces (rubber on dry road).

### Angle of friction and angle of repose

- **Angle of friction** $\lambda$: the angle that the resultant of the limiting
  friction and the normal reaction makes with the normal reaction:
  $\tan\lambda = \frac{f_s}{N} = \mu_s$.
- **Angle of repose** $\theta_r$: the smallest angle of an inclined plane at which a
  body placed on it just begins to slide down. At that angle
  $mg\sin\theta_r = \mu_s\,mg\cos\theta_r$, so $\mu_s = \tan\theta_r$.

Hence **angle of repose = angle of friction**, and neither depends on the mass of the
body. (Sand piles, scree slopes in the hills and grain heaps settle at their angle
of repose.)

```figure caption="Forces on a block resting on a rough incline at the angle of repose. The weight splits into $mg\sin\theta$ down the slope and $mg\cos\theta$ into the slope; friction $f$ balances the first, the normal reaction $N$ the second."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,3.3))
th = np.radians(30); u = np.array([np.cos(th), np.sin(th)]); n = np.array([-np.sin(th), np.cos(th)])
L = 6.0
ax.fill([0, L, L], [0, 0, L*np.tan(th)], color=GRID, ec=INK, lw=1.0)
P = 3.8*u; s = 1.0
corners = [P - s/2*u, P + s/2*u, P + s/2*u + s*n, P - s/2*u + s*n]
ax.fill([c[0] for c in corners], [c[1] for c in corners], color='#DCE6F5', ec=ACCENT, lw=1.3, zorder=3)
C = P + s/2*n
def arrow(a, b, col, ls='-', lw=1.8):
    ax.annotate('', xy=b, xytext=a, arrowprops=dict(arrowstyle='-|>', color=col, lw=lw,
                linestyle=ls, shrinkA=0, shrinkB=0, mutation_scale=12), zorder=5)
W = 1.75
arrow(C, C + np.array([0, -W]), INK)
arrow(C, C + W*np.cos(th)*n, ACCENT)
arrow(P, P + W*np.sin(th)*u, '#A8271F')
arrow(C, C - W*np.sin(th)*u, MUTED, ls=(0,(3,2)), lw=1.3)
arrow(C, C - W*np.cos(th)*n, MUTED, ls=(0,(3,2)), lw=1.3)
ax.text(*(C + np.array([0.14, -W + 0.22])), 'mg', fontsize=9.5, color=INK, ha='left', va='center')
ax.text(*(C + W*np.cos(th)*n + np.array([-0.08, 0.1])), 'N', fontsize=9.5, color=ACCENT, ha='right', va='bottom')
ax.text(*(P + W*np.sin(th)*u + np.array([0.08, -0.05])), 'f', fontsize=9.5, color='#A8271F', ha='left', va='top')
ax.text(*(C - W*np.sin(th)*u + np.array([-0.1, 0.05])), 'mg sinθ', fontsize=8.5, color=MUTED, ha='right', va='bottom')
ax.text(*(C - W*np.cos(th)*n + np.array([0.15, -0.05])), 'mg cosθ', fontsize=8.5, color=MUTED, ha='left', va='top')
a = np.linspace(0, th, 30); ax.plot(1.1*np.cos(a), 1.1*np.sin(a), color=INK, lw=0.9)
ax.text(1.25, 0.28, 'θ', fontsize=10, color=INK)
ax.set_xlim(-0.3, 6.3); ax.set_ylim(-0.2, 4.6); ax.set_aspect('equal'); ax.axis('off')
```

### Friction in calculations

| Situation | Result |
|---|---|
| Block sliding on a rough level floor | deceleration $\mu_kg$; stopping distance $\frac{u^2}{2\mu_kg}$ (independent of mass) |
| Block sliding down a rough incline ($\theta > \theta_r$) | $a = g(\sin\theta - \mu_k\cos\theta)$ |
| Block slides down at constant velocity | $\mu_k = \tan\theta$ |
| Pushing a block up an incline at steady speed | $F = mg(\sin\theta + \mu\cos\theta)$ |
| Least force (along the incline) that stops it sliding down | $F = mg(\sin\theta - \mu\cos\theta)$ |
| Pulling at angle $\alpha$ above the horizontal | $N = mg - F\sin\alpha$ (less friction) |
| Pushing at angle $\alpha$ below the horizontal | $N = mg + F\sin\alpha$ (more friction) |

So it is easier to **pull** a lawn roller than to push it. Friction is not only a
nuisance: walking, the grip of tyres, brakes, belts on pulleys and writing all
depend on it. It is reduced by polishing, lubrication, ball bearings and
streamlining.

::: example Worked example 2.6 — rough incline and braking
**Problem.** (a) A block slides down an incline with $\sin\theta = 0.6$ and
$\mu_k = 0.25$. Find its acceleration ($g = 10\ \text{m s}^{-2}$). (b) A car at
20 m s⁻¹ brakes with its wheels locked on a road with $\mu_k = 0.5$. Find the
stopping distance.

**Solution.** (a) $\cos\theta = 0.8$; $a = 10(0.6 - 0.25\times0.8) = 4\ \text{m s}^{-2}$.
(b) $s = u^2/(2\mu_kg) = 400/10 = 40\ \text{m}$. Double the speed and it becomes
160 m.
:::

::: tip Friction questions in 30 seconds
First decide whether the body **moves**. Compare the applied force (or $mg\sin\theta$)
with the limiting friction $\mu_sN$. If it is smaller, the body stays at rest and the
friction equals the applied force — **not** $\mu N$. A 10 kg box with $\mu_s = 0.5$
pushed with 20 N on a level floor feels 20 N of friction, not 49 N.
:::

## Formula and fact sheet

| Topic | Formula or fact |
|---|---|
| Second law | $\vec F = d\vec p/dt = m\vec a$; variable mass $F = v\,dm/dt$; rocket thrust $u\,dm/dt$ |
| Lift | up-acceleration $m(g + a)$; down-acceleration $m(g - a)$; free fall 0; constant velocity $mg$ |
| Atwood | $a = (m_1 - m_2)g/(m_1 + m_2)$; $T = 2m_1m_2g/(m_1 + m_2)$ |
| Equilibrium | $\sum\vec F = 0$ and $\sum\tau = 0$; Lami: $P/\sin\alpha = Q/\sin\beta = R/\sin\gamma$ |
| Impulse | $J = F\Delta t = \Delta p$ = area under $F$–$t$; rebound from a wall $2mv$ |
| Momentum–KE | $K = p^2/2m$; $p = \sqrt{2mK}$ |
| Recoil | $V = -mv/M$; $K_{bullet}/K_{gun} = M/m$ |
| Machine gun | $F = nmv$ |
| Work | $W = Fs\cos\theta$; spring $\frac{1}{2}k(x_2^2 - x_1^2)$; area under $F$–$x$ |
| Work–energy | $W_{net} = \Delta K$ |
| Power | $P = W/t = Fv$; 1 hp = 746 W; 1 kWh = 3.6 × 10⁶ J |
| Restitution | $e = (v_2 - v_1)/(u_1 - u_2)$; elastic 1, perfectly inelastic 0 |
| Elastic 1-D | $v_1 = [(m_1 - m_2)u_1 + 2m_2u_2]/(m_1 + m_2)$; $v_2 = [(m_2 - m_1)u_2 + 2m_1u_1]/(m_1 + m_2)$ |
| Elastic, target at rest | equal masses exchange velocities; KE fraction transferred $4m_1m_2/(m_1 + m_2)^2$ |
| Perfectly inelastic | $v = (m_1u_1 + m_2u_2)/(m_1 + m_2)$; KE lost $m_1m_2(u_1 - u_2)^2/[2(m_1 + m_2)]$ |
| Bouncing ball | height after $n$ bounces $e^{2n}h$ |
| Friction | $f_s \le \mu_sN$; $f_k = \mu_kN$; $\mu_k < \mu_s$; $\mu_s = \tan\lambda = \tan\theta_{repose}$ |
| Incline | sliding down $a = g(\sin\theta - \mu\cos\theta)$; stopping distance on level $u^2/2\mu g$ |

## Chapter summary

- Inertia is resistance to change of motion, measured by mass; $\vec F = d\vec p/dt$;
  action and reaction are equal, opposite and act on different bodies, so they never
  cancel.
- A weighing machine reads $m(g \pm a)$ according to the direction of the
  *acceleration*; zero in free fall, $mg$ at constant velocity.
- Equilibrium of a rigid body needs zero net force and zero net torque; three
  concurrent forces in equilibrium obey Lami's theorem.
- Impulse = change in momentum = area under the force–time graph; spreading the
  same impulse over more time lowers the force.
- With no external force, total momentum is conserved: recoil, explosions, rockets
  and every collision.
- $W = Fs\cos\theta$; the net work equals the change in kinetic energy; $K = p^2/2m$;
  $P = Fv$.
- Elastic collisions conserve KE ($e = 1$); perfectly inelastic ones stick together
  ($e = 0$) and lose the most KE; equal masses in an elastic head-on collision exchange
  velocities.
- Limiting friction $\mu_sN$ is independent of area of contact; $\mu_k < \mu_s$;
  angle of repose = angle of friction, $\mu_s = \tan\theta_r$.

## Practice questions

**Set A — Recall (21 questions)**

1. Newton's first law of motion gives the concept of
   (a) inertia (b) energy (c) power (d) momentum
2. The SI unit of impulse is
   (a) N (b) N s (c) N m (d) N s⁻¹
3. Action and reaction forces
   (a) act on the same body and cancel each other (b) are unequal when the bodies accelerate (c) act on different bodies and never cancel each other (d) act one after the other
4. A rigid body is in complete (translational and rotational) equilibrium when
   (a) the net force on it is zero (b) the net torque on it is zero (c) it moves with constant speed (d) both the net force and the net torque on it are zero
5. The work done by the centripetal force on a body moving uniformly in a circle is
   (a) zero (b) positive (c) negative (d) equal to its kinetic energy
6. The area under a force–displacement graph gives
   (a) impulse (b) work done (c) power (d) momentum
7. The area under a force–time graph gives
   (a) work done (b) power (c) change in momentum (d) change in kinetic energy
8. The kinetic energy K and momentum p of a body of mass m are related by
   (a) $K = p^{2}/m$ (b) $K = 2mp^{2}$ (c) $K = p/2m$ (d) $K = p^{2}/2m$
9. Which of the following is a conservative force?
   (a) gravitational force (b) kinetic friction (c) air resistance (d) viscous force
10. One kilowatt hour is equal to
   (a) 3.6 × 10³ J (b) 3.6 × 10⁶ J (c) 1000 J (d) 3.6 × 10⁵ J
11. In a perfectly inelastic collision
   (a) both momentum and kinetic energy are conserved (b) neither momentum nor kinetic energy is conserved (c) momentum is conserved and the bodies move together afterwards (d) kinetic energy is conserved but momentum is not
12. The coefficient of restitution for a perfectly elastic collision is
   (a) 0 (b) 0.5 (c) between 0 and 1 (d) 1
13. Two equal masses collide head-on elastically, one of them initially at rest. After the collision
   (a) both move together (b) they exchange velocities (c) both come to rest (d) the moving one rebounds with its own speed
14. The coefficient of static friction $\mu_s$ and the angle of repose $\theta$ are related by
   (a) $\mu_s = \sin\theta$ (b) $\mu_s = \cos\theta$ (c) $\mu_s = \tan\theta$ (d) $\mu_s = \cot\theta$
15. For the same normal reaction, limiting friction between two surfaces is independent of
   (a) the nature of the surfaces (b) the apparent area of contact (c) the roughness of the surfaces (d) the normal reaction
16. Compared with the coefficient of static friction, the coefficient of kinetic friction for the same pair of surfaces is
   (a) smaller (b) equal (c) larger (d) zero
17. Ball bearings are used in machines because
   (a) they increase the normal reaction (b) they increase the area of contact (c) rolling friction is much smaller than sliding friction (d) they remove friction completely
18. The work–energy theorem states that the work done by the net force on a body equals the change in its
   (a) potential energy (b) momentum (c) total energy (d) kinetic energy
19. A man stands on a weighing machine in a lift that falls freely. The machine reads
   (a) zero (b) his true weight (c) twice his weight (d) half his weight
20. Rocket propulsion is an application of
   (a) Newton's first law (b) conservation of linear momentum (c) conservation of kinetic energy (d) Pascal's law
21. One horsepower is approximately
   (a) 500 W (b) 1000 W (c) 100 W (d) 746 W

::: note Answers and explanations — Set A
**1.** (a) — the first law says a body keeps its state unless a net force acts: the property of resisting change is inertia (measured by mass).
**2.** (b) — impulse = force × time, N s, the same as kg m s⁻¹ (the unit of momentum). N m is the unit of work or torque.
**3.** (c) — the third-law pair acts on two different bodies, so the forces cannot cancel; they are equal at every instant, whatever the motion.
**4.** (d) — zero net force gives no linear acceleration; zero net torque gives no angular acceleration. A rigid body needs both.
**5.** (a) — the centripetal force is perpendicular to the velocity at every instant, so $W = Fs\cos90^{\circ} = 0$; the speed does not change.
**6.** (b) — $W = \int F\,dx$ is the area under $F$–$x$. Impulse is the area under $F$–$t$.
**7.** (c) — $\int F\,dt$ = impulse = change in momentum.
**8.** (d) — $K = \frac{1}{2}mv^2 = \frac{(mv)^2}{2m} = \frac{p^2}{2m}$.
**9.** (a) — the work of gravity depends only on the change in height, not on the path; friction, air drag and viscous forces dissipate energy.
**10.** (b) — 1 kWh = 1000 W × 3600 s = 3.6 × 10⁶ J; the kWh is a unit of energy, not power.
**11.** (c) — momentum is conserved in every collision; in a perfectly inelastic one the bodies stick together and the loss of KE is the greatest.
**12.** (d) — $e$ = relative speed of separation / relative speed of approach = 1 when no KE is lost.
**13.** (b) — with $m_1 = m_2$ and $u_2 = 0$, the formulas give $v_1 = 0$ and $v_2 = u_1$: the velocities are exchanged (as in billiards).
**14.** (c) — at the angle of repose $mg\sin\theta = \mu_s mg\cos\theta$, so $\mu_s = \tan\theta$.
**15.** (b) — the third law of friction: for the same normal reaction, the area of contact does not matter. Friction is proportional to $N$, so (d) is wrong.
**16.** (a) — $\mu_k < \mu_s$: it takes more force to start sliding than to keep sliding.
**17.** (c) — bearings replace sliding with rolling, and rolling friction is far smaller; friction is reduced, not removed.
**18.** (d) — $W_{net} = \Delta K$. Work by conservative forces alone equals $-\Delta U$, which is a different statement.
**19.** (a) — in free fall both the man and the machine accelerate at $g$, so $R = m(g - g) = 0$: apparent weightlessness.
**20.** (b) — the exhaust gases are pushed backward and the rocket gains equal forward momentum (equivalently, Newton's third law); kinetic energy is not conserved.
**21.** (d) — 1 hp ≈ 746 W.
:::

**Set B — Understanding (14 questions)**

1. A boy stands on a weighing machine in a lift that is moving upward with a uniform velocity. Compared with his true weight W, the reading is
   (a) more than W (b) less than W (c) equal to W (d) zero
2. A cricketer moves his hands backward while catching a fast ball. He does so to
   (a) reduce the change in momentum (b) increase the time of impact and so reduce the force (c) reduce the impulse to zero (d) increase the force on the ball
3. Two bodies of masses 1 kg and 4 kg have equal kinetic energies. The ratio of their momenta $p_1 : p_2$ is
   (a) 1 : 2 (b) 1 : 4 (c) 4 : 1 (d) 1 : 16
4. A ball of mass m strikes a wall normally with speed v and rebounds with the same speed. The magnitude of the change in its momentum is
   (a) zero (b) mv (c) mv/2 (d) 2mv
5. A gun fires a bullet. Just after firing, compared with the gun, the bullet has
   (a) equal momentum in magnitude and much more kinetic energy (b) more momentum and more kinetic energy (c) equal momentum and equal kinetic energy (d) less momentum and less kinetic energy
6. Pulling a lawn roller at an angle above the horizontal is easier than pushing it at the same angle below the horizontal, because pulling
   (a) increases the normal reaction (b) decreases the normal reaction and hence the friction (c) changes the coefficient of friction (d) reduces the weight of the roller
7. A very heavy ball moving at speed u collides head-on and elastically with a very light ball at rest. The light ball moves off with a speed of about
   (a) u/2 (b) u (c) 2u (d) zero
8. A porter carries a load on his head and walks along a level road at constant speed. The work he does on the load against gravity is
   (a) zero (b) positive (c) negative (d) equal to the weight × distance walked
9. The momentum of a body increases by 50 %. Its kinetic energy increases by
   (a) 50 % (b) 100 % (c) 125 % (d) 150 %
10. A block placed on a rough plane just begins to slide when the plane is tilted to 30°. The coefficient of static friction is
   (a) 0.50 (b) 0.87 (c) 1.73 (d) 0.58
11. A block slides down a rough inclined plane of inclination θ at constant velocity. The coefficient of kinetic friction is
   (a) tan θ (b) sin θ (c) cos θ (d) cot θ
12. A ball dropped from height h bounces on a floor for which the coefficient of restitution is 0.5. It rises to a height of
   (a) h/2 (b) h/8 (c) h/4 (d) h/√2
13. Sand drops steadily at a rate dm/dt onto a conveyor belt moving at constant speed v. The extra force needed to keep the belt moving at that speed is
   (a) zero (b) ½ v dm/dt (c) 2v dm/dt (d) v dm/dt
14. Three forces of 3 N, 4 N and 5 N acting at a point keep it in equilibrium. The angle between the 3 N and 4 N forces is
   (a) 60° (b) 90° (c) 120° (d) 180°

::: note Answers and explanations — Set B
**1.** (c) — uniform velocity means zero acceleration, so $R = mg$. Only acceleration changes the reading, never the direction of motion alone.
**2.** (b) — the change in momentum (impulse) is fixed by the catch; lengthening the contact time reduces the average force $F = \Delta p/\Delta t$.
**3.** (a) — $p = \sqrt{2mK}$; with equal $K$, $p \propto \sqrt{m}$: $\sqrt{1} : \sqrt{4} = 1 : 2$.
**4.** (d) — momentum goes from $+mv$ to $-mv$, a change of $2mv$; it is zero only for speed, not for the vector momentum.
**5.** (a) — total momentum stays zero, so the momenta are equal and opposite; with equal $p$, $K = p^2/2m$ is larger for the lighter bullet (by the ratio $M/m$).
**6.** (b) — the upward component of the pull reduces the normal reaction ($N = mg - F\sin\alpha$), so the friction $\mu N$ is less; pushing adds to $N$.
**7.** (c) — with $m_1 \gg m_2$, $v_2 = 2m_1u_1/(m_1 + m_2) \approx 2u$.
**8.** (a) — his upward force on the load is perpendicular to the horizontal displacement, so the work against gravity is zero (he still tires, but that is not work on the load).
**9.** (c) — $K \propto p^2$: $1.5^2 = 2.25$, so K rises by 125 %.
**10.** (d) — $\mu_s = \tan30^{\circ} = 1/\sqrt{3} \approx 0.58$. 0.50 is $\sin30^{\circ}$ and 0.87 is $\cos30^{\circ}$.
**11.** (a) — constant velocity means zero net force: $mg\sin\theta = \mu_kmg\cos\theta$, so $\mu_k = \tan\theta$.
**12.** (c) — the rebound speed is $e$ times the impact speed, and height $\propto v^2$: $h' = e^2h = 0.25h$.
**13.** (d) — the belt must give the arriving sand momentum at the rate $v\,dm/dt$, so $F = dp/dt = v\,dm/dt$.
**14.** (b) — in equilibrium the three forces form a closed triangle with sides 3, 4, 5, a right-angled triangle, so the 3 N and 4 N forces are perpendicular.
:::

**Set C — Application (12 questions)**

1. A 0.15 kg ball reaches a bat at 20 m s⁻¹ and is hit straight back at 30 m s⁻¹. The contact lasts 0.01 s. The average force on the ball is
   (a) 150 N (b) 300 N (c) 450 N (d) 750 N
2. A 4 kg gun fires a 10 g bullet with a muzzle speed of 400 m s⁻¹. The recoil speed of the gun is
   (a) 1 m s⁻¹ (b) 0.1 m s⁻¹ (c) 4 m s⁻¹ (d) 10 m s⁻¹
3. A 50 kg person stands in a lift that is moving downward and slowing down at 2 m s⁻² (g = 10 m s⁻²). The normal force on the person is
   (a) 400 N (b) 600 N (c) 500 N (d) 100 N
4. Masses of 5 kg and 3 kg hang from the two ends of a light string over a frictionless pulley (g = 9.8 m s⁻²). Their acceleration is
   (a) 1.96 m s⁻² (b) 3.27 m s⁻² (c) 2.45 m s⁻² (d) 4.9 m s⁻²
5. A 2 kg ball moving at 3 m s⁻¹ collides head-on and elastically with a 1 kg ball at rest. Their velocities after the collision are
   (a) 0 and 6 m s⁻¹ (b) 1 m s⁻¹ and 4 m s⁻¹ (c) 2 m s⁻¹ and 2 m s⁻¹ (d) 1.5 m s⁻¹ and 3 m s⁻¹
6. A 10 g bullet moving at 300 m s⁻¹ embeds itself in a 990 g wooden block at rest on a smooth floor. The block moves off at
   (a) 30 m s⁻¹ (b) 0.3 m s⁻¹ (c) 3.03 m s⁻¹ (d) 3 m s⁻¹
7. A motor pumps 600 kg of water into a tank 20 m above it in 2 minutes (g = 9.8 m s⁻²). The minimum power of the motor is
   (a) 98 W (b) 980 W (c) 1960 W (d) 117.6 kW
8. A car's engine delivers 30 kW. If the total resistance on a level road is 1500 N, the greatest steady speed of the car is
   (a) 20 km h⁻¹ (b) 45 km h⁻¹ (c) 72 km h⁻¹ (d) 50 km h⁻¹
9. A car moving at 20 m s⁻¹ skids to rest with locked wheels on a road where $\mu_k = 0.5$ (g = 10 m s⁻²). The skid is
   (a) 20 m long (b) 80 m long (c) 4 m long (d) 40 m long
10. A spring of force constant 200 N m⁻¹ is already stretched by 10 cm. The extra work needed to stretch it further, from 10 cm to 20 cm, is
   (a) 1 J (b) 3 J (c) 4 J (d) 2 J
11. A 20 N lamp hangs from the midpoint of a wire whose two halves make an angle of 120° with each other. The tension in each half is
   (a) 20 N (b) 10 N (c) 11.5 N (d) 40 N
12. A machine gun fires 10 bullets per second, each of mass 20 g, at 500 m s⁻¹. The average force needed to hold the gun steady is
   (a) 10 N (b) 1000 N (c) 100 N (d) 50 N

::: note Answers and explanations — Set C
**1.** (d) — the velocity reverses: $\Delta p = 0.15(30 + 20) = 7.5$ N s; $F = 7.5/0.01 = 750$ N. (a) forgets the reversal (uses 30 − 20).
**2.** (a) — momentum conservation: $V = mv/M = 0.010(400)/4 = 1$ m s⁻¹, opposite to the bullet.
**3.** (b) — moving down and slowing down means the acceleration is **upward**: $R = m(g + a) = 50(12) = 600$ N. (a) wrongly uses $g - a$.
**4.** (c) — $a = (m_1 - m_2)g/(m_1 + m_2) = 2(9.8)/8 = 2.45$ m s⁻².
**5.** (b) — $v_1 = (2 - 1)(3)/3 = 1$ m s⁻¹; $v_2 = 2(2)(3)/3 = 4$ m s⁻¹. Check: momentum $6 = 2 + 4$ and KE $9 = 1 + 8$ J. (c) is the perfectly inelastic answer.
**6.** (d) — perfectly inelastic: $v = mu/(m + M) = 0.01(300)/1.00 = 3$ m s⁻¹. (c) forgets to add the bullet's mass to the block.
**7.** (b) — $P = mgh/t = 600(9.8)(20)/120 = 980$ W. (d) is the energy, 117 600 J, mistaken for power (no division by the time); (c) uses 60 s for 2 min.
**8.** (c) — at top speed the driving force equals the resistance: $v = P/F = 30\,000/1500 = 20$ m s⁻¹ = 72 km h⁻¹. (a) is the right number with the wrong unit.
**9.** (d) — deceleration $\mu_kg = 5$ m s⁻²; $s = u^2/2a = 400/10 = 40$ m.
**10.** (b) — $W = \frac{1}{2}k(x_2^2 - x_1^2) = 100(0.04 - 0.01) = 3$ J. (a) is the work for the first 10 cm, and (c) the work from 0 to 20 cm.
**11.** (a) — each half makes 60° with the vertical: $2T\cos60^{\circ} = 20$ N gives $T = 20$ N.
**12.** (c) — force = momentum delivered per second = $nmv = 10(0.020)(500) = 100$ N.
:::
