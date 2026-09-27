---
subject: Physics
grade: 11
unit: 4
title: Dynamics
hours: 6
area: Mechanics
---

Kinematics described motion; dynamics explains it. The explanation lies in
Newton's three laws, and the quantity that makes them work is **linear
momentum**. From it come force and impulse; from the third law comes the
conservation of momentum; from careful bookkeeping of forces come the free-body
diagrams that solve most mechanics problems. The unit closes with two effects
present in every real machine — torque and friction.

::: key How to attack any dynamics problem
Draw the body alone. Mark every force acting **on** it. Choose axes. Write
$\sum F = ma$ along each axis and, if the body can turn, $\sum \tau = 0$ about a
convenient point. Most marks in this unit are earned by that sequence.
:::

## 4.1 Linear momentum, Impulse

A body stays at rest or in uniform motion unless an external force acts —
**Newton's first law**. It defines force as *that which changes the state of
motion*, and names the resistance to that change **inertia**, measured by mass.

::: definition Linear momentum
The linear momentum of a body is the product of its mass and its velocity,

$$ \vec{p} = m\vec{v} $$

It is a vector along the velocity. Its SI unit is kg m s⁻¹ (equivalently N s)
and its dimensional formula is $[MLT^{-1}]$.
:::

**Newton's second law** states that the rate of change of linear momentum of a
body is directly proportional to the applied force and takes place in the
direction of the force:

$$ \vec{F} \propto \frac{d\vec{p}}{dt} = \frac{d(m\vec{v})}{dt} $$

::: derivation $F = ma$ from Newton's second law
We start from the statement of the second law — force is proportional to the rate
of change of momentum — and reach the familiar working formula $F = ma$.

**Step 1 — write the law as an equation.** "Proportional to" means "equal to, apart
from a constant". Call that constant $k$:

$$ F = k\,\frac{dp}{dt} $$

**Step 2 — put in the definition of momentum**, $p = mv$:

$$ F = k\,\frac{d(mv)}{dt} $$

**Step 3 — take the mass outside the differentiation.** This step needs the mass to
be **constant**; a constant multiplier can always be moved outside a derivative:

$$ F = k\,m\,\frac{dv}{dt} $$

**Step 4 — recognise the derivative.** By definition $dv/dt$ is the acceleration
$a$:

$$ F = k\,m\,a $$

**Step 5 — fix the constant $k$ by choosing the unit of force.** We *define* one
newton as the force that gives a mass of 1 kg an acceleration of 1 m s⁻². Putting
$F = 1$, $m = 1$, $a = 1$ into Step 4:

$$ 1 = k \times 1 \times 1 \;\Longrightarrow\; k = 1 $$

**Step 6 — substitute $k = 1$:**

$$ F = ma $$

**Result.** $\vec{F} = m\vec{a}$, with the acceleration in the same direction as
the force.

**What it means.** The same force gives a small mass a big acceleration and a big
mass a small one — mass is the measure of inertia.

**Condition used.** Step 3 assumed the **mass does not change**. For a rocket
burning fuel or a raindrop collecting water, go back to $F = dp/dt$ and
differentiate the product properly. The law also holds only in an inertial
(non-accelerating) frame.
:::

### Impulse

::: definition Impulse
Impulse is the product of a force and the time for which it acts. For a constant
force $\vec{J} = \vec{F}\,\Delta t$; for a varying force,

$$ \vec{J} = \int_{t_1}^{t_2} \vec{F}\,dt $$
:::

::: derivation Impulse–momentum theorem: $J = mv - mu$
We start from Newton's second law in its momentum form and reach the statement
that the impulse of a force equals the change in momentum it produces.

**Step 1 — the second law.** Force is the rate of change of momentum:

$$ \vec{F} = \frac{d\vec{p}}{dt} $$

**Step 2 — multiply both sides by $dt$.** This just moves $dt$ to the other side, so
that we have "force times a tiny time" on the left:

$$ \vec{F}\,dt = d\vec{p} $$

**Step 3 — add up all the tiny bits.** The contact lasts from $t_1$ to $t_2$, during
which the momentum goes from $\vec{p}_1$ to $\vec{p}_2$. Adding up tiny pieces is
what integration does, so we integrate both sides between matching limits:

$$ \int_{t_1}^{t_2}\vec{F}\,dt = \int_{\vec{p}_1}^{\vec{p}_2} d\vec{p} $$

**Step 4 — do the right-hand integral.** Integrating $d\vec{p}$ simply gives
$\vec{p}$, so we evaluate it at the two limits:

$$ \int_{t_1}^{t_2}\vec{F}\,dt = \vec{p}_2 - \vec{p}_1 $$

**Step 5 — name the left-hand side.** By definition, that integral *is* the impulse
$\vec{J}$:

$$ \vec{J} = \vec{p}_2 - \vec{p}_1 $$

**Step 6 — put in $p = mv$.** With initial velocity $\vec{u}$ and final velocity
$\vec{v}$:

$$ \vec{J} = m\vec{v} - m\vec{u} $$

**Step 7 — the constant-force version.** If we replace the real changing force by
its average value $F_{av}$ acting for the whole time $\Delta t = t_2 - t_1$, the
integral becomes a simple product:

$$ F_{av}\,\Delta t = mv - mu $$

**Result.**

$$ \vec{J} = \int_{t_1}^{t_2}\vec{F}\,dt = m\vec{v} - m\vec{u}
= F_{av}\,\Delta t $$

**What it means.** The area under a force–time graph is the momentum handed over.
For a fixed change of momentum, a longer contact time means a smaller force — which
is the whole idea behind airbags, crumple zones and a cricketer drawing his hands
back while catching.

**Condition used.** The mass is constant, and $\vec{F}$ is the **net** force on the
body. Impulse is a vector, so in a rebound problem you must give $u$ and $v$
opposite signs.
:::

::: tip The examiner is looking for
(i) $F = dp/dt$ quoted as the *starting point*; (ii) the step $F\,dt = dp$;
(iii) integration with **both** sets of limits written in; (iv) the final statement
in words — "impulse = change in momentum"; (v) the unit N s = kg m s⁻¹. In numerical
parts, signs: a rebound needs $v$ and $u$ with opposite signs.
:::

```figure caption="Force-time graph for a collision lasting 10 ms. The shaded area is the impulse; the dashed line is the constant average force that would deliver the same impulse."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8, 2.8))
t = np.linspace(0, 10, 400)
F = 1100 * np.sin(np.pi * t / 10) ** 1.0
Fav = np.trapezoid(F, t) / 10.0
ax.plot(t, F, color=ACCENT, lw=2)
ax.fill_between(t, 0, F, color=ACCENT, alpha=0.12)
ax.hlines(Fav, 0, 10, color='#d9534f', lw=1.4, ls='--')
ax.annotate('$F_{av}$', (10.15, Fav), color='#d9534f', fontsize=10, va='center')
ax.annotate('area $=$ impulse $= \\Delta p$', (5, 330), ha='center', color=INK,
            fontsize=9.5)
ax.set_xlabel('time  $t$  (ms)'); ax.set_ylabel('force  $F$  (N)')
ax.set_xlim(0, 11.6); ax.set_ylim(0, 1250)
ax.spines[['top', 'right']].set_visible(False)
ax.grid(True, alpha=0.5)
```

::: tip Why safety devices work
For a given collision $\Delta p$ is fixed. Since $F_{av} = \Delta p/\Delta t$, the
only way to cut the force is to **stretch the time** — the physics of airbags,
crumple zones, helmet padding and the long-jump sand pit.
:::

::: example Worked example 4.1
**Problem.** A ball of mass $0.2\ \text{kg}$ moving at $20\ \text{m s}^{-1}$
strikes a wall normally and rebounds at $15\ \text{m s}^{-1}$. If the contact
lasts $0.01\ \text{s}$, find the impulse and the average force on the ball.

**Solution.** Take the direction *away* from the wall as positive, so
$u = -20\ \text{m s}^{-1}$ and $v = +15\ \text{m s}^{-1}$.

$$ J = mv - mu = 0.2\,[15 - (-20)] = 0.2 \times 35 = 7\ \text{N s} $$

$$ F_{av} = \frac{J}{\Delta t} = \frac{7}{0.01} = 700\ \text{N} $$
:::

## 4.2 Conservation of linear momentum

**Newton's third law**: to every action there is an equal and opposite reaction.
The two forces act on **different** bodies, along the same line, and appear and
vanish together.

::: derivation Conservation of linear momentum from Newton's third law
We start from Newton's third law applied to two colliding bodies and reach the
statement that their total momentum is the same before and after the collision.

**Setting up.** Two smooth spheres A and B of masses $m_1$ and $m_2$ move along the
same straight line with velocities $u_1$ and $u_2$, where $u_1 > u_2$ so that A
catches up with B. They touch for a short time $t$ and then separate with
velocities $v_1$ and $v_2$. No outside force (no friction, no push) acts on the
pair.

**Step 1 — name the two contact forces.** While they touch, B pushes A with a force
$F_{12}$ and A pushes B with a force $F_{21}$.

**Step 2 — apply the third law.** Action and reaction are equal in size and opposite
in direction:

$$ F_{12} = -F_{21} $$

**Step 3 — write each force as a rate of change of momentum.** By the second law,
the force on a body equals its change in momentum divided by the time. For A the
momentum changes from $m_1u_1$ to $m_1v_1$:

$$ F_{12} = \frac{m_1v_1 - m_1u_1}{t} $$

and for B, from $m_2u_2$ to $m_2v_2$:

$$ F_{21} = \frac{m_2v_2 - m_2u_2}{t} $$

**Step 4 — substitute both into Step 2:**

$$ \frac{m_1v_1 - m_1u_1}{t} = -\,\frac{m_2v_2 - m_2u_2}{t} $$

**Step 5 — multiply both sides by $t$.** The contact time is the same for both
bodies — they touch and separate together — so it cancels:

$$ m_1v_1 - m_1u_1 = -(m_2v_2 - m_2u_2) $$

**Step 6 — open the bracket on the right:**

$$ m_1v_1 - m_1u_1 = -m_2v_2 + m_2u_2 $$

**Step 7 — collect the "before" terms on one side and the "after" terms on the
other.** Add $m_1u_1$ to both sides and add $m_2v_2$ to both sides:

$$ m_1v_1 + m_2v_2 = m_1u_1 + m_2u_2 $$

**Result.**

$$ m_1u_1 + m_2u_2 = m_1v_1 + m_2v_2 $$

**What it means.** Whatever violence happens during the contact — however the bodies
squash, heat up or break — the *total* momentum of the pair is unchanged. Momentum
is only passed from one body to the other.

**Conditions used.** (i) No **net external force** acts on the pair during the
collision; this is why the third-law pair could cancel. (ii) The contact time is
the same for both bodies. (iii) Momentum is a vector: in one dimension you must
give leftward velocities a minus sign, and in two dimensions you conserve the $x$
and $y$ components separately. Note that kinetic energy is *not* assumed to be
conserved — this proof works for inelastic collisions too.
:::

::: tip The examiner is looking for
(i) A "before and after" diagram with $m_1, m_2, u_1, u_2, v_1, v_2$ labelled;
(ii) the third-law statement $F_{12} = -F_{21}$; (iii) each force written as
change of momentum over time; (iv) the cancelling of $t$ with the reason;
(v) the final equation *and* the sentence "total momentum before = total momentum
after, provided no external force acts". The condition in (v) carries a mark on
its own.
:::

```figure caption="Head-on collision. Whatever happens during contact, the total momentum $m_1u_1 + m_2u_2$ before equals $m_1v_1 + m_2v_2$ after."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle
fig, ax = plt.subplots(figsize=(4.8, 2.6))
def ball(x, y, r, c, lab):
    ax.add_patch(Circle((x, y), r, facecolor=c, alpha=0.25, edgecolor=c, lw=1.4))
    ax.annotate(lab, (x, y), ha='center', va='center', color=INK, fontsize=9.5)
def vel(x, y, dx, lab, c):
    ax.annotate('', xy=(x + dx, y), xytext=(x, y),
                arrowprops=dict(arrowstyle='-|>', color=c, lw=1.6, shrinkA=0,
                                shrinkB=0, mutation_scale=12))
    ax.annotate(lab, (x + dx / 2, y + 0.30), ha='center', color=c, fontsize=9.5)
ball(0.8, 2.3, 0.42, ACCENT, 'A'); ball(3.4, 2.3, 0.58, '#2e8b57', 'B')
vel(1.35, 2.3, 0.9, '$u_1$', ACCENT); vel(4.05, 2.3, 0.45, '$u_2$', '#2e8b57')
ball(0.8, 0.4, 0.42, ACCENT, 'A'); ball(3.4, 0.4, 0.58, '#2e8b57', 'B')
vel(0.35, 0.4, -0.5, '$v_1$', ACCENT); vel(4.05, 0.4, 1.1, '$v_2$', '#2e8b57')
ax.annotate('before', (-1.0, 2.3), ha='left', va='center', color=MUTED, fontsize=9.5)
ax.annotate('after', (-1.0, 0.4), ha='left', va='center', color=MUTED, fontsize=9.5)
ax.plot([-1.1, 5.6], [1.35, 1.35], color=GRID, lw=1.0)
ax.set_xlim(-1.2, 5.7); ax.set_ylim(-0.4, 3.1); ax.set_aspect('equal'); ax.axis('off')
```

It also follows directly from $\vec{F} = d\vec{p}/dt$: zero net external force
means $d\vec{p}/dt = 0$.

::: key Principle of conservation of linear momentum
If no net external force acts on a system, its total linear momentum stays
constant in magnitude and direction, however the bodies inside it interact.
:::

| Situation | How momentum is conserved |
|---|---|
| Recoil of a gun | forward momentum of bullet = backward momentum of gun |
| Explosion of a shell at rest | vector sum of the fragment momenta is zero |
| Rocket and jet propulsion | gases ejected backwards; rocket gains equal forward momentum |

::: caution Action and reaction never cancel
The two third-law forces act on **different bodies**, so they never add to zero
on one body. A horse pulls a cart because the forward force on the cart and the
backward force on the horse act on different objects.
:::

::: example Worked example 4.2
**Problem.** A bullet of mass $20\ \text{g}$ is fired from a gun of mass
$4\ \text{kg}$ with a muzzle velocity of $400\ \text{m s}^{-1}$. Find the recoil
velocity of the gun.

**Solution.** Before firing the system is at rest, so the total momentum is zero.
With $V$ the recoil velocity,

$$ 0 = m_b v_b + m_g V = (0.020)(400) + 4V \;\Rightarrow\; V = -\frac{8}{4} = -2\ \text{m s}^{-1} $$

The gun recoils at $2\ \text{m s}^{-1}$, opposite to the bullet and far slower
because it is 200 times more massive.
:::

## 4.3 Application of Newton's laws

The routine is always the same: isolate one body, draw its **free-body diagram**,
choose axes along and across the motion, and write $\sum F = ma$ for each axis.

```figure caption="Atwood machine. Isolating each mass gives $m_1g - T = m_1a$ and $T - m_2g = m_2a$."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
fig, ax = plt.subplots(figsize=(4.2, 3.2))
ax.add_patch(Circle((0, 3.4), 0.55, facecolor='none', edgecolor=INK, lw=1.5))
ax.add_patch(Circle((0, 3.4), 0.07, facecolor=INK, edgecolor='none'))
ax.plot([0, 0], [3.95, 4.5], color=INK, lw=1.2)
ax.plot([-0.55, -0.55], [1.5, 3.4], color=INK, lw=1.2)
ax.plot([0.55, 0.55], [0.7, 3.4], color=INK, lw=1.2)
th = np.linspace(0, np.pi, 60)
ax.plot(0.55 * np.cos(th), 3.4 + 0.55 * np.sin(th), color=INK, lw=1.2)
ax.add_patch(Rectangle((-1.05, 0.9), 1.0, 0.6, facecolor=ACCENT, alpha=0.22,
                       edgecolor=ACCENT, lw=1.3))
ax.add_patch(Rectangle((0.05, 0.1), 1.0, 0.6, facecolor='#2e8b57', alpha=0.22,
                       edgecolor='#2e8b57', lw=1.3))
ax.annotate('$m_2$', (-0.55, 1.2), ha='center', va='center', fontsize=10, color=INK)
ax.annotate('$m_1$', (0.55, 0.4), ha='center', va='center', fontsize=10, color=INK)
def far(x, y, dy, lab, c, side=1):
    ax.annotate('', xy=(x, y + dy), xytext=(x, y),
                arrowprops=dict(arrowstyle='-|>', color=c, lw=1.5, shrinkA=0,
                                shrinkB=0, mutation_scale=11))
    ax.annotate(lab, (x + 0.16 * side, y + dy * 0.7), ha='left' if side > 0 else 'right',
                color=c, fontsize=9.5)
far(-0.55, 1.5, 0.75, '$T$', '#d9534f')
far(0.55, 0.7, 0.75, '$T$', '#d9534f')
far(-0.55, 0.9, -0.75, '$m_2g$', INK, side=-1)
far(0.55, 0.1, -0.75, '$m_1g$', INK)
ax.annotate('', xy=(-1.55, 1.75), xytext=(-1.55, 0.95),
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.3, shrinkA=0,
                            shrinkB=0, mutation_scale=11))
ax.annotate('$a$', (-1.72, 1.35), ha='right', va='center', color=MUTED, fontsize=9.5)
ax.annotate('', xy=(1.55, 0.05), xytext=(1.55, 0.85),
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.3, shrinkA=0,
                            shrinkB=0, mutation_scale=11))
ax.annotate('$a$', (1.72, 0.45), ha='left', va='center', color=MUTED, fontsize=9.5)
ax.set_xlim(-2.4, 2.4); ax.set_ylim(-0.9, 4.7); ax.set_aspect('equal'); ax.axis('off')
```

::: derivation Acceleration and tension in an Atwood machine
We start from $F = ma$ written separately for each hanging mass, and reach formulas
for the acceleration of the system and the tension in the string.

**Setting up.** Two masses $m_1$ and $m_2$, with $m_1 > m_2$, hang from the two ends
of a light inextensible string passing over a smooth pulley. Two facts follow from
those words, and they are worth marks:

- *Inextensible* string: the string cannot stretch, so when $m_1$ goes down by
  1 cm, $m_2$ goes up by 1 cm. Both masses therefore have the **same** acceleration
  $a$.
- *Light* string over a *smooth* pulley: no force is needed to accelerate the string
  itself and none is lost to friction, so the tension $T$ is the **same** everywhere
  in the string.

Since $m_1 > m_2$, common sense says $m_1$ goes down and $m_2$ goes up.

**Step 1 — free-body equation for $m_1$.** Two forces act on it: its weight $m_1g$
downwards and the tension $T$ upwards. It accelerates downwards, so take downwards
as positive for this mass. Net force $=$ mass $\times$ acceleration:

$$ m_1g - T = m_1a $$

**Step 2 — free-body equation for $m_2$.** The same two forces act, but this mass
accelerates upwards, so take upwards as positive for it:

$$ T - m_2g = m_2a $$

**Step 3 — add the two equations.** We add them because $T$ appears with a minus
sign in one and a plus sign in the other, so it will disappear:

$$ (m_1g - T) + (T - m_2g) = m_1a + m_2a $$

**Step 4 — cancel $T$ and collect terms.** On the left $-T + T = 0$; on the right
take out the common factor $a$:

$$ m_1g - m_2g = (m_1 + m_2)a $$

**Step 5 — take out $g$ on the left:**

$$ (m_1 - m_2)g = (m_1 + m_2)a $$

**Step 6 — divide both sides by $(m_1 + m_2)$ to get $a$ alone:**

$$ a = \frac{(m_1 - m_2)g}{m_1 + m_2} $$

**Step 7 — now find $T$.** Go back to Step 2 and make $T$ the subject by adding
$m_2g$ to both sides:

$$ T = m_2g + m_2a = m_2(g + a) $$

**Step 8 — substitute the $a$ we just found:**

$$ T = m_2\left(g + \frac{(m_1 - m_2)g}{m_1 + m_2}\right) $$

**Step 9 — put the bracket over one common denominator $(m_1+m_2)$:**

$$ T = m_2\left(\frac{g(m_1 + m_2) + g(m_1 - m_2)}{m_1 + m_2}\right) $$

**Step 10 — expand the top line:**

$$ T = m_2\left(\frac{m_1g + m_2g + m_1g - m_2g}{m_1 + m_2}\right) $$

**Step 11 — the two $m_2g$ terms cancel, leaving $2m_1g$:**

$$ T = m_2\cdot\frac{2m_1g}{m_1 + m_2} $$

**Step 12 — write it tidily:**

$$ T = \frac{2m_1m_2\,g}{m_1 + m_2} $$

**Result.**

$$ a = \frac{(m_1 - m_2)g}{m_1 + m_2}, \qquad T = \frac{2m_1m_2\,g}{m_1 + m_2} $$

**What it means.** The unbalanced force is only the *difference* in weights
$(m_1-m_2)g$, but it has to move the *total* mass $(m_1+m_2)$ — so the machine
slows gravity down, which is exactly why Atwood used it to measure $g$. If
$m_1 = m_2$ then $a = 0$ and $T = m_1g$, as expected. Also note
$m_2g < T < m_1g$: the tension always lies between the two weights.

**Assumptions used.** Light inextensible string, frictionless and massless pulley,
no air resistance. If the pulley had mass, part of the torque would go into
spinning it and $a$ would be smaller.
:::

**Apparent weight in a lift.** A weighing machine reads the normal reaction $R$
it exerts, not the true weight.

| Motion of the lift | Equation | Apparent weight $R$ |
|---|---|---|
| At rest or uniform velocity | $R - mg = 0$ | $mg$ |
| Accelerating upward with $a$ | $R - mg = ma$ | $m(g + a)$ — feels heavier |
| Accelerating downward with $a$ | $mg - R = ma$ | $m(g - a)$ — feels lighter |
| Cable breaks, free fall $a = g$ | $mg - R = mg$ | $0$ — weightlessness |

**Smooth inclined plane.** Resolving the weight along and perpendicular to a
plane inclined at $\theta$ gives

$$ mg\sin\theta = ma \;\Rightarrow\; a = g\sin\theta, \qquad R = mg\cos\theta $$

::: example Worked example 4.3
**Problem.** Masses of $5\ \text{kg}$ and $3\ \text{kg}$ hang from the ends of a
light string over a frictionless pulley. Find the acceleration of the system and
the tension in the string. Take $g = 10\ \text{m s}^{-2}$.

**Solution.**

$$ a = \frac{(m_1-m_2)g}{m_1+m_2} = \frac{(5-3)(10)}{8} = 2.5\ \text{m s}^{-2} $$

$$ T = \frac{2m_1m_2g}{m_1+m_2} = \frac{2(5)(3)(10)}{8} = 37.5\ \text{N} $$

Check: $T - m_2g = 37.5 - 30 = 7.5\ \text{N} = (3)(2.5)$. ✓
:::

## 4.4 Moment, torque and equilibrium

::: definition Moment of a force (torque)
The moment, or torque, of a force about a point is the product of the force and
the perpendicular distance of its line of action from that point:

$$ \tau = F \times d_{\perp} = rF\sin\theta, \qquad \vec{\tau} = \vec{r}\times\vec{F} $$

Its SI unit is the newton metre (N m) and its dimensional formula is
$[ML^{2}T^{-2}]$. It is a vector directed along the axis of rotation.
:::

A torque is positive when it turns the body anticlockwise. A force whose line of
action passes *through* the point has zero moment, and a force at right angles to
the arm has the largest moment — hence the door handle far from the hinge.

A **couple** is a pair of equal, opposite, parallel forces on different lines.
Their resultant is zero, so a couple gives pure rotation. Its moment,
$\tau = F \times$ (perpendicular distance between them), is the same about
**every** point.

```figure caption="Principle of moments. The beam balances when $W_1d_1 = W_2d_2$; the pivot supplies the upward reaction $R$."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle
fig, ax = plt.subplots(figsize=(4.8, 2.6))
ax.add_patch(Rectangle((-4.2, -0.12), 8.4, 0.24, facecolor=GRID, edgecolor=INK, lw=1.1))
ax.add_patch(Polygon([[-0.45, -0.75], [0.45, -0.75], [0, -0.13]], closed=True,
                     facecolor=MUTED, edgecolor=INK, lw=1.0))
for x, lab, c in [(-3.0, '$W_1$', ACCENT), (2.2, '$W_2$', '#2e8b57')]:
    ax.annotate('', xy=(x, -1.15), xytext=(x, -0.14),
                arrowprops=dict(arrowstyle='-|>', color=c, lw=1.7, shrinkA=0,
                                shrinkB=0, mutation_scale=12))
    ax.annotate(lab, (x, -1.30), ha='center', va='top', color=c, fontsize=10)
ax.annotate('', xy=(0, 1.25), xytext=(0, 0.13),
            arrowprops=dict(arrowstyle='-|>', color='#d9534f', lw=1.7, shrinkA=0,
                            shrinkB=0, mutation_scale=12))
ax.annotate('$R$', (0.14, 1.20), ha='left', va='top', color='#d9534f', fontsize=10)
for x0, x1, lab in [(-3.0, 0, '$d_1$'), (0, 2.2, '$d_2$')]:
    ax.annotate('', xy=(x1, 0.62), xytext=(x0, 0.62),
                arrowprops=dict(arrowstyle='<|-|>', color=MUTED, lw=1.0,
                                shrinkA=0, shrinkB=0, mutation_scale=9))
    ax.annotate(lab, ((x0 + x1) / 2, 0.72), ha='center', color=MUTED, fontsize=9.5)
ax.plot([-3.0, -3.0], [0.12, 0.62], color=MUTED, lw=0.7, ls=':')
ax.plot([2.2, 2.2], [0.12, 0.62], color=MUTED, lw=0.7, ls=':')
ax.plot([0, 0], [0.12, 0.62], color=MUTED, lw=0.7, ls=':')
ax.set_xlim(-4.7, 4.7); ax.set_ylim(-2.0, 1.6); ax.set_aspect('equal'); ax.axis('off')
```

::: key Conditions for equilibrium
A rigid body under coplanar forces is in equilibrium when **both**:

1. $\sum \vec{F} = 0$, i.e. $\sum F_x = 0$ and $\sum F_y = 0$ (no translation);
2. $\sum \tau = 0$ about **any** point (no rotation).

Condition 2 alone is the **principle of moments**: clockwise moments equal
anticlockwise moments.
:::

| Type of equilibrium | On slight displacement | Centre of gravity | Example |
|---|---|---|---|
| Stable | returns to its original position | rises | cone on its base |
| Unstable | moves further away | falls | cone on its apex |
| Neutral | stays in the new position | height unchanged | cone on its side |

::: example Worked example 4.4
**Problem.** A uniform plank $4\ \text{m}$ long and of weight $200\ \text{N}$
rests on supports at its two ends. A boy of weight $500\ \text{N}$ stands
$1\ \text{m}$ from the left-hand support. Find the reaction at each support.

**Solution.** Let $R_1$ and $R_2$ be the left and right reactions. The weight of
the uniform plank acts at its centre, $2\ \text{m}$ from either end.

Vertical equilibrium: $R_1 + R_2 = 200 + 500 = 700\ \text{N}$.

Taking moments about the left-hand support:

$$ R_2 \times 4 = 200 \times 2 + 500 \times 1 = 900 $$

$$ R_2 = 225\ \text{N}, \qquad R_1 = 700 - 225 = 475\ \text{N} $$

The support nearer the boy carries the larger share.
:::

## 4.5 Solid friction: Laws of solid friction and their verifications

::: definition Solid friction
Friction is the force acting along the surface of contact between two solid
bodies that opposes their relative motion, or the tendency to it. It arises from
interlocking and adhesion between the microscopic high points of the surfaces.
:::

Push a resting block gently and it does not move: friction has grown to match the
push exactly. This self-adjusting force is **static friction**. At some push the
block just begins to slide, and the friction then is the **limiting friction**.
Once sliding, the resistance settles at a smaller, nearly constant
**kinetic (dynamic) friction**.

```figure caption="Friction against applied force. Static friction grows to match the applied force up to the limiting value, then drops to the smaller, roughly constant kinetic friction."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8, 2.8))
Pl, Fk = 4.0, 3.1
p1 = np.linspace(0, Pl, 120)
p2 = np.linspace(Pl, 8.0, 120)
ax.plot(p1, p1, color=ACCENT, lw=2.0)
ax.plot([Pl, Pl], [Pl, Fk], color=ACCENT, lw=2.0, ls=':')
ax.plot(p2, np.full_like(p2, Fk), color=ACCENT, lw=2.0)
ax.plot([Pl], [Pl], 'o', color='#d9534f', ms=5)
ax.hlines(Pl, 0, Pl, color=MUTED, lw=0.8, ls=':')
ax.hlines(Fk, 0, 8.0, color=MUTED, lw=0.8, ls=':')
ax.annotate('limiting friction', (Pl, Pl), textcoords='offset points',
            xytext=(8, 10), color='#d9534f', fontsize=9.2)
ax.annotate('kinetic friction $f_k$', (8.0, Fk), textcoords='offset points',
            xytext=(0, -16), ha='right', color=INK, fontsize=9.2)
# label parked in the clear wedge below the rising static line
ax.annotate('static: $f = P$', (2.80, 1.20), ha='center', va='center',
            color=INK, fontsize=9.2)
ax.annotate('body at rest', (2.0, 0.35), ha='center', color=MUTED, fontsize=8.6)
ax.annotate('body slides', (6.0, 0.35), ha='center', color=MUTED, fontsize=8.6)
ax.axvline(Pl, color=GRID, lw=1.0)
ax.set_xlabel('applied force  $P$'); ax.set_ylabel('force of friction  $f$')
ax.set_xlim(0, 8.4); ax.set_ylim(0, 5.6)
ax.set_xticks([]); ax.set_yticks([])
ax.spines[['top', 'right']].set_visible(False)
```
The **coefficients of friction** are ratios to the normal reaction $N$:

$$ \mu_s = \frac{f_{limiting}}{N}, \qquad \mu_k = \frac{f_k}{N}, \qquad \mu_k < \mu_s $$

A ratio of two forces, $\mu$ has no units: about 0.6 for rubber on concrete,
0.3 for wood on wood, 0.04 for steel on ice.

### Laws of solid friction

**Static friction**

1. Limiting friction is directly proportional to the normal reaction:
   $f_{limiting} = \mu_s N$.
2. It is independent of the apparent area of contact, provided the normal
   reaction is unchanged.
3. It depends on the nature, material and roughness of the two surfaces.

**Kinetic friction**

1. Kinetic friction is directly proportional to the normal reaction,
   $f_k = \mu_k N$.
2. It is independent of the apparent area of contact.
3. It is independent of the relative velocity at moderate speeds.
4. It depends on the nature of the surfaces and is always less than the limiting
   friction.

### Angle of friction and angle of repose

The **angle of friction** $\lambda$ is the angle between the normal reaction and
the resultant of the normal reaction and the limiting friction, so

$$ \tan\lambda = \frac{\mu_s N}{N} = \mu_s $$

The **angle of repose** $\theta$ is the smallest inclination of a plane at which
a body placed on it just begins to slide.

```figure caption="A block on the point of sliding down a rough plane. Along the slope $mg\sin\theta = f = \mu_s mg\cos\theta$, so $\mu_s = \tan\theta$."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Arc
fig, ax = plt.subplots(figsize=(4.8, 3.2))
th = np.radians(30)
A = np.array([0.0, 6 * np.tan(th)]); B = np.array([6.0, 0.0]); O = np.array([0.0, 0.0])
ax.add_patch(Polygon([O, B, A], closed=True, facecolor=GRID, alpha=0.5,
                     edgecolor=INK, lw=1.2))
d = (B - A) / np.linalg.norm(B - A)
n = np.array([-d[1], d[0]])
if n[1] < 0:
    n = -n
M = A + 0.42 * (B - A)
corners = [M - 0.7 * d, M + 0.7 * d, M + 0.7 * d + 0.62 * n, M - 0.7 * d + 0.62 * n]
ax.add_patch(Polygon(corners, closed=True, facecolor=ACCENT, alpha=0.25,
                     edgecolor=ACCENT, lw=1.3))
G = M + 0.31 * n
slope_deg = np.degrees(np.arctan2(d[1], d[0]))
def av(vec, c, ls='-'):
    ax.annotate('', xy=G + vec, xytext=G,
                arrowprops=dict(arrowstyle='-|>', color=c, lw=1.6, linestyle=ls,
                                shrinkA=0, shrinkB=0, mutation_scale=12))
def lab(pos, text, c, rot=0.0):
    ax.text(pos[0], pos[1], text, color=c, fontsize=9.5, ha='center',
            va='center', rotation=rot, rotation_mode='anchor')
av(np.array([0.0, -1.9]), INK)
av(1.5 * n, '#d9534f')
av(-1.4 * d, '#2e8b57')
av(1.35 * d, MUTED, ls=(0, (3, 2)))
av(-1.25 * n, MUTED, ls=(0, (3, 2)))
# labels kept off the slope line: the two slope-parallel ones are rotated
lab(G + np.array([0.0, -1.9]) + np.array([0.62, 0.30]), '$mg$', INK)
lab(G + 1.5 * n + np.array([0.18, 0.26]), '$N$', '#d9534f')
lab(G - 1.4 * d + 0.42 * n, '$f$', '#2e8b57')
lab(G + 1.35 * d + 0.52 * n, r'$mg\sin\theta$', MUTED, rot=slope_deg)
lab(G - 1.25 * n + np.array([-0.35, -0.52]), r'$mg\cos\theta$', MUTED)
ax.add_patch(Arc(B, 2.6, 2.6, theta1=150, theta2=180, color=INK, lw=1.0))
ax.annotate(r'$\theta$', (B[0] - 1.55, 0.22), color=INK, fontsize=10.5)
ax.set_xlim(-1.6, 7.0); ax.set_ylim(-0.8, 4.3); ax.set_aspect('equal'); ax.axis('off')
```
::: derivation The angle of repose equals the angle of friction
We start from a block that is *just about* to slide down a rough slope, and reach
the result $\mu_s = \tan\theta$ — which also proves that the angle of repose and the
angle of friction are the same angle.

**Setting up.** A block of mass $m$ rests on a rough plane whose tilt $\theta$ is
slowly increased. At the **angle of repose** the block is on the very point of
sliding: it is still in equilibrium, but the friction has reached its largest
possible value, $f_{limiting} = \mu_s N$.

Choose axes along the slope and perpendicular to the slope — not horizontal and
vertical. Then the only force needing to be resolved is the weight $mg$, which acts
vertically downwards.

**Step 1 — resolve the weight.** The angle between the weight and the perpendicular
to the slope is also $\theta$ (simple geometry of the tilted plane). So the weight
splits into a part pressing into the slope and a part pulling down the slope:

$$ \text{into the slope} = mg\cos\theta, \qquad
\text{down the slope} = mg\sin\theta $$

**Step 2 — balance perpendicular to the slope.** The block does not sink into the
plane or lift off it, so the normal reaction $N$ exactly balances the pressing
component:

$$ N = mg\cos\theta $$

**Step 3 — balance along the slope.** The block is not yet moving, so the friction
up the slope exactly balances the component pulling it down:

$$ f_{limiting} = mg\sin\theta $$

**Step 4 — divide Step 3 by Step 2.** Dividing one true equation by another is
allowed as long as we are not dividing by zero, and $N \ne 0$ here:

$$ \frac{f_{limiting}}{N} = \frac{mg\sin\theta}{mg\cos\theta} $$

**Step 5 — cancel $mg$, which appears on top and bottom:**

$$ \frac{f_{limiting}}{N} = \frac{\sin\theta}{\cos\theta} $$

**Step 6 — use $\sin\theta/\cos\theta = \tan\theta$:**

$$ \frac{f_{limiting}}{N} = \tan\theta $$

**Step 7 — identify the left-hand side.** By definition, limiting friction divided
by normal reaction is the coefficient of static friction:

$$ \mu_s = \tan\theta $$

**Step 8 — compare with the angle of friction.** The angle of friction $\lambda$ is
defined by $\mu_s = \tan\lambda$. Two tangents are equal, so for angles between
$0^{\circ}$ and $90^{\circ}$ the angles themselves are equal:

$$ \tan\theta = \tan\lambda \;\Longrightarrow\; \theta = \lambda $$

**Result.**

$$ \mu_s = \tan\theta, \qquad \text{angle of repose} = \text{angle of friction} $$

**What it means.** $mg$ cancelled in Step 5, so the angle of repose does **not**
depend on the mass of the block — only on what the two surfaces are made of. This is
why a heap of dry sand always settles to the same slope, whether the heap is small
or huge, and it gives a one-line laboratory method for $\mu_s$: tilt until it
slides, then measure $\tan\theta = h/b$.

**Conditions used.** The block is on the **point** of sliding (so friction is at its
limiting value — not before, not after), the plane is straight, and no other force
such as a push or a string tension acts on the block.
:::

::: tip The examiner is looking for
(i) A labelled diagram with $mg$, $N$, $f$ and the slope angle $\theta$ marked;
(ii) axes taken **along and perpendicular to** the plane; (iii) the two
equilibrium equations $N = mg\cos\theta$ and $f = mg\sin\theta$; (iv) the division
step; (v) the sentence "the mass cancels, so the angle of repose is independent of
mass". Students who resolve horizontally and vertically instead usually get lost —
resolve along the plane.
:::

### Verifying the laws

**(a) Horizontal board, pulley and scale pan.** A block on a horizontal board is
joined by a light string passing over a smooth pulley at the edge to a scale pan.
Weights are added slowly until the block just begins to move; the pan weight then
equals the limiting friction.

- Add known weights **on top of the block** to change $N$. The graph of limiting
  friction against $N$ is a straight line through the origin of slope $\mu_s$ —
  the first law.
- Rest the same block on a face of different area under the same load: the pan
  weight is unchanged — the second law.
- Change the material, or polish the board: the reading changes — the third law.

**(b) Inclined-plane method.** Raise one end of a hinged plane until the block
just slides and measure the height $h$ and base $b$: $\mu_s = \tan\theta = h/b$.
Different masses give the same angle, so $\mu$ is independent of mass and area.

::: caution Three things students get wrong about friction
1. Friction is **not always** $\mu N$ — that is only its limiting or kinetic
   value. A block at rest under a 5 N push feels 5 N of friction, even if
   $\mu N = 20\ \text{N}$.
2. Friction opposes *relative* motion. The friction driving a walking person or a
   car forwards acts **forwards**.
3. $\mu$ can exceed 1, and it has no units.
:::

Friction makes walking, gripping and braking possible, but wastes energy as heat
and wears parts away; it is reduced by lubricants, bearings and polishing.

::: example Worked example 4.5
**Problem.** A block of mass $10\ \text{kg}$ rests on a horizontal floor for
which $\mu_s = 0.4$ and $\mu_k = 0.3$. Take $g = 10\ \text{m s}^{-2}$.
(a) What least horizontal force starts it moving?
(b) What is its acceleration if that force keeps acting?

**Solution.** The normal reaction is $N = mg = 100\ \text{N}$.

(a) $f_{limiting} = \mu_s N = 0.4 \times 100 = 40\ \text{N}$, so the least force
is $40\ \text{N}$.

(b) Once sliding, friction falls to $f_k = \mu_k N = 0.3 \times 100 = 30\ \text{N}$:

$$ ma = P - f_k = 40 - 30 = 10\ \text{N} \;\Rightarrow\; a = 1\ \text{m s}^{-2} $$

The block jerks into motion — the reason a heavy crate shoots forward the moment
it starts to slide.
:::

## Chapter summary

- $\vec{p} = m\vec{v}$ (kg m s⁻¹, $[MLT^{-1}]$); $\vec{F} = d\vec{p}/dt$, becoming
  $\vec{F} = m\vec{a}$ only for constant mass.
- Impulse $\vec{J} = \vec{F}\Delta t = \int\vec{F}dt = m\vec{v} - m\vec{u}$, the area
  under the $F$–$t$ graph; a longer $\Delta t$ means a smaller $F_{av}$.
- $m_1u_1 + m_2u_2 = m_1v_1 + m_2v_2$: momentum of an isolated system is
  conserved — recoil, explosions, rocket propulsion.
- Atwood: $a = (m_1-m_2)g/(m_1+m_2)$, $T = 2m_1m_2g/(m_1+m_2)$; apparent weight in
  a lift is $m(g \pm a)$, zero in free fall.
- Torque $\tau = rF\sin\theta = \vec{r}\times\vec{F}$ (N m); a couple has moment
  $F \times d$ about every point.
- Equilibrium needs $\sum\vec{F} = 0$ **and** $\sum\tau = 0$ (principle of moments).
- Friction: $f_{limiting} = \mu_s N$, $f_k = \mu_k N$, $\mu_k < \mu_s$, independent
  of apparent area, and $\mu_s = \tan\theta = \tan\lambda$.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The rate of change of linear momentum of a body is equal to <span class="marks">[1]</span>
   (a) impulse (b) the applied force (c) work done (d) power
2. A rigid body is in complete equilibrium when <span class="marks">[1]</span>
   (a) $\sum F = 0$ only (b) $\sum \tau = 0$ only (c) both $\sum F = 0$ and $\sum \tau = 0$ (d) its velocity is zero
3. The coefficient of friction <span class="marks">[1]</span>
   (a) has the unit newton (b) has the unit N m⁻¹ (c) is dimensionless (d) has dimension $[MLT^{-2}]$
4. A body just slides down a plane inclined at $30^{\circ}$ to the horizontal. The coefficient of static friction is <span class="marks">[1]</span>
   (a) 0.50 (b) 0.58 (c) 0.87 (d) 1.73

::: note Answers to Group A
**1.** (b) — Newton's second law is $F = dp/dt$.
**2.** (c) — translational and rotational equilibrium are both needed.
**3.** (c) — it is a ratio of two forces.
**4.** (b) — $\mu_s = \tan 30^{\circ} = 0.577$.
:::

**Group B — Short answer (5 marks each)**

1. Define linear momentum and impulse. Show that the impulse of a force equals
   the change of momentum it produces, and explain why a long-jump pit is filled
   with sand. <span class="marks">[5]</span>
2. State Newton's third law and hence prove the principle of conservation of
   linear momentum for two bodies colliding head-on. <span class="marks">[5]</span>
3. A bullet of mass $10\ \text{g}$ is fired from a gun of mass $5\ \text{kg}$
   with a muzzle velocity of $300\ \text{m s}^{-1}$. Calculate the recoil
   velocity of the gun. <span class="marks">[5]</span>
4. Two masses of $6\ \text{kg}$ and $4\ \text{kg}$ hang from the ends of a light
   string over a smooth pulley. Find the acceleration of the system and the
   tension in the string. Take $g = 10\ \text{m s}^{-2}$. <span class="marks">[5]</span>
5. A uniform metre rule of weight $2\ \text{N}$ balances on a knife edge at the
   $30\ \text{cm}$ mark when a weight $W$ hangs at the $10\ \text{cm}$ mark. Find
   $W$ and the reaction at the knife edge. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Outline: state both definitions, derive $J = mv - mu$ from $F = dp/dt$, and
note that sand lengthens $\Delta t$ so $F_{av} = \Delta p/\Delta t$ falls.

**2.** Outline: as in the derivation in §4.2.

**3.** Total momentum before firing is zero, so $0 = (0.010)(300) + 5V$, giving
$V = -0.6\ \text{m s}^{-1}$: the gun recoils at $0.6\ \text{m s}^{-1}$.

**4.** $a = \dfrac{(6-4)(10)}{6+4} = 2\ \text{m s}^{-2}$ and
$T = \dfrac{2(6)(4)(10)}{10} = 48\ \text{N}$.

**5.** The weight of the uniform rule acts at the $50\ \text{cm}$ mark,
$20\ \text{cm}$ right of the knife edge, while $W$ hangs $20\ \text{cm}$ to the
left. Moments about the knife edge give $W \times 20 = 2 \times 20$, so
$W = 2\ \text{N}$, and the reaction is $R = 2 + 2 = 4\ \text{N}$ upwards.
:::

**Group C — Long answer (8 marks each)**

1. (a) State Newton's second law of motion and use it to derive $F = ma$,
   explaining why this form fails for a body of changing mass. <span class="marks">[4]</span>
   (b) A machine gun fires $20$ bullets per second, each of mass $30\ \text{g}$,
   with a muzzle speed of $400\ \text{m s}^{-1}$. Find the force required to hold
   the gun steady. <span class="marks">[4]</span>
2. (a) State the laws of solid friction and describe an experiment to verify that
   limiting friction is directly proportional to the normal reaction. <span class="marks">[5]</span>
   (b) A block of mass $5\ \text{kg}$ rests on a horizontal surface with
   $\mu_s = 0.5$ and $\mu_k = 0.4$. Taking $g = 10\ \text{m s}^{-2}$, find
   (i) the least horizontal force that starts it moving and (ii) its acceleration
   if that force continues to act. <span class="marks">[3]</span>

::: note Answers to Group C
**1.** (b) Each bullet carries momentum
$mv = 0.030 \times 400 = 12\ \text{kg m s}^{-1}$, and 20 are fired per second, so

$$ F = \frac{\Delta p}{\Delta t} = 20 \times 12 = 240\ \text{N} $$

**2.** (b) $N = mg = 50\ \text{N}$. (i) $f_{limiting} = 0.5 \times 50 = 25\ \text{N}$.
(ii) $f_k = 0.4 \times 50 = 20\ \text{N}$, so $a = (25-20)/5 = 1\ \text{m s}^{-2}$.
:::
