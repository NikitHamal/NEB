---
subject: Physics
grade: 11
unit: 5
title: Work, energy and power
hours: 6
area: Mechanics
---

Newton's laws tell you the force on a body at every instant. Often you do not
care about every instant — you only want to know how fast the body ends up, or
how much fuel the engine burned. Work and energy answer those questions in one
line where dynamics would need a page. This unit builds the idea of work, turns
it into kinetic and potential energy, and ends with the one law that survives
every situation: energy is conserved.

::: key What the examiner asks here
Three things come up year after year: the work–energy theorem applied to a rough
surface, the conservation of energy on a track or pendulum, and one-dimensional
collisions. Learn to decide in one glance whether a problem is a *force* problem
or an *energy* problem — energy is almost always faster.
:::

## 5.1 Work done by a constant force and a variable force

In ordinary speech "work" means effort. In physics it means something much
narrower: a force does work only when its point of application **moves**, and
only the component of the force **along** the displacement counts.

::: definition Work done by a constant force
If a constant force of magnitude $F$ acts on a body while the body undergoes a
displacement $s$, and $\theta$ is the angle between the force and the
displacement, the work done by the force is

$$ W = F s \cos\theta = \vec{F}\cdot\vec{s} $$

Work is a **scalar**. Its SI unit is the joule (J); $1\ \text{J} = 1\ \text{N m}$.
:::

```figure caption="Only the component $F\cos\theta$ along the displacement does work. The vertical component $F\sin\theta$ reduces the normal reaction but does no work."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Arc
fig, ax = plt.subplots(figsize=(4.8,2.7))
ax.add_patch(Rectangle((1.0,0.6),1.5,0.9, fc='#dfe6ef', ec=INK, lw=1.2))
ax.plot([0,7.4],[0.6,0.6], color=INK, lw=1.4)
for x in np.arange(0.1,7.4,0.38):
    ax.plot([x,x-0.18],[0.6,0.38], color=MUTED, lw=0.8)
th = np.radians(37); O = np.array([2.5, 1.05])
d = np.array([np.cos(th), np.sin(th)]); pn = np.array([-np.sin(th), np.cos(th)])
ax.annotate('', xy=O + 2.0*d, xytext=O,
            arrowprops=dict(arrowstyle='-|>', color='#d9534f', lw=2.0, mutation_scale=14))
# F label set off the arrow shaft on its free side
ax.annotate('$F$', O + 1.2*d + 0.45*pn, ha='center', va='center',
            color='#d9534f', fontsize=10)
ax.annotate('', xy=(O[0] + 2.0*np.cos(th), O[1]), xytext=tuple(O),
            arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.5, mutation_scale=12))
ax.annotate(r'$F\cos\theta$', (3.4,1.05), textcoords='offset points', xytext=(-8,-15),
            color=ACCENT, fontsize=9.5)
ax.plot([O[0] + 2.0*np.cos(th)]*2, [O[1], O[1] + 2.0*np.sin(th)], color=MUTED, lw=0.9, ls=':')
ax.annotate(r'$F\sin\theta$', (O[0] + 2.0*np.cos(th), O[1] + 0.6*np.sin(th)),
            textcoords='offset points', xytext=(9,0), color=MUTED, fontsize=9.5)
ax.add_patch(Arc(tuple(O), 1.4, 1.4, theta1=0, theta2=37, color=INK, lw=0.9))
ta = np.radians(18.5)
ax.annotate(r'$\theta$', (O[0] + 0.94*np.cos(ta), O[1] + 0.94*np.sin(ta)),
            ha='center', va='center', color=INK, fontsize=10)
ax.annotate('', xy=(6.6,0.15), xytext=(1.0,0.15),
            arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.2, mutation_scale=11))
ax.annotate('$s$', (3.8,0.15), textcoords='offset points', xytext=(0,-13), color=INK, fontsize=10)
ax.set_xlim(-0.2,7.6); ax.set_ylim(-0.6,3.2); ax.set_aspect('equal'); ax.axis('off')
```
The cosine controls the sign, and the sign is physical:

| Angle $\theta$ | $\cos\theta$ | Work | Example |
|---|---|---|---|
| $0^{\circ}$ | $+1$ | positive, maximum | a falling stone and its weight |
| acute | $+$ | positive | pulling a cart with a slanted rope |
| $90^{\circ}$ | $0$ | **zero** | normal reaction; centripetal force; a coolie carrying a load on level ground |
| obtuse | $-$ | negative | brakes on a moving car |
| $180^{\circ}$ | $-1$ | negative, maximum | friction on a sliding block |

::: caution Zero work is not zero effort
A porter on the Ghorepani trail carrying a 40 kg *doko* horizontally does **no**
work on the load in the physics sense, because the supporting force is vertical
and the displacement is horizontal. He tires because his muscles keep contracting
and relaxing — that is physiological work, not mechanical work on the load.
:::

**Variable force.** Most real forces change as the body moves — the pull of a
spring, the drag on a bus, the thrust of a rocket. Split the displacement into
strips so narrow that $F$ is effectively constant across each strip, do $F\,dx$
for each, and add:

$$ W = \lim_{\Delta x \to 0}\sum F\,\Delta x = \int_{x_1}^{x_2} F\,dx $$

::: key Work is the area under the force–displacement graph
This is true whatever the shape of the graph. Area above the axis is positive
work, area below is negative work.
:::

For a spring obeying Hooke's law the applied force needed is $F = kx$, a straight
line through the origin. Stretching it from $0$ to $x$ sweeps out a triangle of
base $x$ and height $kx$:

$$ W = \int_{0}^{x} kx\,dx = \tfrac{1}{2}kx^{2} $$

```figure caption="Work done is the area under the $F$–$x$ graph. For a spring $F = kx$, so the area from $0$ to $x$ is the triangle $\frac{1}{2}kx^2$."
import numpy as np, matplotlib.pyplot as plt
fig, (a1,a2) = plt.subplots(1,2, figsize=(5.2,2.5))
x = np.linspace(0,5,300); F = 6 + 5*np.sin(x/1.7)
a1.plot(x,F,color=ACCENT,lw=1.9)
a1.fill_between(x,0,F,where=(x>=1)&(x<=4),color=ACCENT,alpha=0.16)
a1.annotate('$W$',(2.5,3.2),color=INK,fontsize=11,ha='center')
a1.set_xlim(0,5); a1.set_ylim(0,13)
a1.set_xticks([1,4]); a1.set_xticklabels(['$x_1$','$x_2$']); a1.set_yticks([])
a1.set_xlabel('displacement $x$'); a1.set_ylabel('force $F$')
a1.set_title('general variable force', fontsize=9)
k = 2.4; xs = np.linspace(0,4,100)
a2.plot(xs,k*xs,color='#d9534f',lw=1.9)
a2.fill_between(xs,0,k*xs,color='#d9534f',alpha=0.16)
a2.annotate(r'$\frac{1}{2}kx^2$',(1.6,2.6),color=INK,fontsize=11)
a2.set_xlim(0,5); a2.set_ylim(0,13)
a2.set_xticks([4]); a2.set_xticklabels(['$x$']); a2.set_yticks([])
a2.set_xlabel('extension $x$'); a2.set_ylabel('force $F = kx$')
a2.set_title('spring', fontsize=9)
for a in (a1,a2):
    a.spines[['top','right']].set_visible(False)
fig.tight_layout()
```

::: example Worked example 5.1
**Problem.** A crate of mass $10\ \text{kg}$ is dragged $10\ \text{m}$ across a
horizontal floor by a rope inclined at $37^{\circ}$ above the horizontal with a
tension of $100\ \text{N}$. The coefficient of kinetic friction is $0.2$.
Take $g = 10\ \text{m s}^{-2}$, $\cos 37^{\circ} = 0.8$, $\sin 37^{\circ} = 0.6$.
Find the work done by each force and the final speed if the crate starts at rest.

**Solution.** Work by the tension:

$$ W_T = Ts\cos\theta = 100 \times 10 \times 0.8 = 800\ \text{J} $$

The vertical component of the tension lifts part of the weight, so the normal
reaction is

$$ N = mg - T\sin\theta = 100 - 60 = 40\ \text{N} $$

Friction is $f = \mu N = 0.2 \times 40 = 8\ \text{N}$, opposite the motion, so

$$ W_f = -f s = -8 \times 10 = -80\ \text{J} $$

Weight and normal reaction are both perpendicular to the displacement, so each
does **zero** work. Net work $= 800 - 80 = 720\ \text{J}$. By the work–energy
theorem,

$$ \tfrac{1}{2}mv^{2} = 720 \;\Longrightarrow\; 5v^{2} = 720 \;\Longrightarrow\; v = 12\ \text{m s}^{-1} $$
:::

## 5.2 Power

Two labourers carry the same load of bricks to the same roof. One takes ten
minutes, the other twenty. Both do the same work; the first is twice as
**powerful**.

::: definition Power
Power is the rate of doing work, or equivalently the rate of transfer of energy.

$$ P_{av} = \frac{W}{t}, \qquad P = \frac{dW}{dt} $$

The SI unit is the watt (W): $1\ \text{W} = 1\ \text{J s}^{-1}$. Commercial units
are the kilowatt ($10^{3}$ W) and the horsepower ($1\ \text{hp} = 746\ \text{W}$).
:::

If a constant force $\vec{F}$ moves a body at velocity $\vec{v}$, then in time
$dt$ the displacement is $\vec{v}\,dt$ and $dW = \vec{F}\cdot\vec{v}\,dt$, so

$$ P = \vec{F}\cdot\vec{v} = Fv\cos\theta $$

This is the form to use for vehicles: at steady speed the driving force equals
the total resisting force, so $P = Fv$ immediately gives the engine power.

::: caution Kilowatt-hour is energy, not power
The unit on a Nepal Electricity Authority bill, the kilowatt-hour, is a unit of
**energy**: $1\ \text{kW h} = 1000 \times 3600 = 3.6 \times 10^{6}\ \text{J}$.
"Units consumed" means joules used, not power.
:::

::: example Worked example 5.2
**Problem.** A pump raises $600$ litres of water per minute from a well
$20\ \text{m}$ deep in Chitwan. Taking $g = 10\ \text{m s}^{-2}$ and the density
of water as $1000\ \text{kg m}^{-3}$, find (a) the useful output power and (b) the
input power if the pump is $80\%$ efficient.

**Solution.** $600$ litres has mass $600\ \text{kg}$, delivered in $60\ \text{s}$,
so the mass lifted per second is $\dot{m} = 10\ \text{kg s}^{-1}$.

(a) Useful power:

$$ P_{out} = \frac{mgh}{t} = \dot{m}gh = 10 \times 10 \times 20 = 2000\ \text{W} = 2\ \text{kW} $$

(b) Efficiency $\eta = P_{out}/P_{in}$, so

$$ P_{in} = \frac{2000}{0.80} = 2500\ \text{W} = 2.5\ \text{kW} $$
:::

## 5.3 Work–energy theorem; kinetic and potential energy

**Energy** is the capacity to do work; it is measured in joules, like work.
Mechanical energy comes in two forms.

::: derivation The work–energy theorem, and why $K = \frac{1}{2}mv^{2}$
We start from the definition of work and Newton's second law, and reach the result
that the work done on a body equals the change in the quantity $\frac{1}{2}mv^{2}$
— which is why we give that quantity the special name *kinetic energy*.

**Setting up.** A constant net force $F$ acts on a body of mass $m$ in the direction
it is moving. The body's speed rises from $u$ to $v$ while it moves a distance $s$.

**Step 1 — write down the work.** The force is along the displacement, so
$\theta = 0$ and $\cos\theta = 1$:

$$ W_{net} = F s $$

**Step 2 — replace $F$ using Newton's second law.** The net force on a constant mass
is $F = ma$:

$$ W_{net} = m\,a\,s $$

**Step 3 — get $as$ from the equations of motion.** The third equation of motion for
constant acceleration is

$$ v^{2} = u^{2} + 2as $$

**Step 4 — make $as$ the subject.** Subtract $u^{2}$ from both sides:

$$ v^{2} - u^{2} = 2as $$

**Step 5 — divide both sides by 2:**

$$ as = \frac{v^{2} - u^{2}}{2} $$

**Step 6 — substitute this into Step 2.** This is the key move: it replaces the
force-and-distance picture by a speed picture:

$$ W_{net} = m\left(\frac{v^{2} - u^{2}}{2}\right) $$

**Step 7 — multiply the $m$ into the bracket, term by term:**

$$ W_{net} = \tfrac{1}{2}mv^{2} - \tfrac{1}{2}mu^{2} $$

**Step 8 — name the two terms.** The expression $\frac{1}{2}mv^{2}$ depends only on
the mass and the speed at that instant, so it is a property of the *state* of the
body. We call it the kinetic energy:

$$ K = \tfrac{1}{2}mv^{2} $$

**Step 9 — rewrite Step 7 in that language.** With $K_i = \frac{1}{2}mu^{2}$ and
$K_f = \frac{1}{2}mv^{2}$:

$$ W_{net} = K_f - K_i = \Delta K $$

**Result.** The **work–energy theorem**:

$$ W_{net} = \tfrac{1}{2}mv^{2} - \tfrac{1}{2}mu^{2} = \Delta K $$

The net work done by all the forces acting on a body equals the change in its
kinetic energy. As a special case, a body at rest that is accelerated to speed $v$
has had $\frac{1}{2}mv^{2}$ of work done on it — so that is the energy stored in its
motion.

**What it means.** Positive net work speeds a body up; negative net work (friction,
brakes) slows it down. Because $K$ depends on $v^{2}$, doubling the speed needs four
times the work — the reason stopping distances grow so fast with speed.

**Conditions used.** Steps 1–5 assumed a **constant** force acting **along** the
motion and a constant mass. The theorem itself is more general: for a varying force
you replace $Fs$ by $\int F\,dx$ and reach the same answer. $W_{net}$ must be the
work of the **net** force — friction work included, with its minus sign.
:::

::: tip The examiner is looking for
(i) $W = Fs$ with the statement that the force is along the displacement;
(ii) $F = ma$ substituted; (iii) $v^{2} = u^{2}+2as$ quoted and rearranged for
$as$; (iv) the substitution, and (v) the final line named as the work–energy
theorem in words. If the question says "for a variable force", you must start from
$W = \int F\,dx$ instead.
:::

Because $p = mv$, kinetic energy and momentum are linked by

$$ K = \frac{p^{2}}{2m}, \qquad p = \sqrt{2mK} $$

**Potential energy** is energy a body has because of its *position* or
*configuration*. Lifting a mass $m$ slowly through a height $h$ needs an upward
force $mg$ through a distance $h$, so the work stored is

$$ U = mgh $$

measured from whatever level you choose as zero. For a stretched or compressed
spring the stored **elastic potential energy** is $U = \frac{1}{2}kx^{2}$, the
area found in §5.1.

::: tip Choose the zero of potential energy first
Only *changes* in potential energy are physical. Write "taking the ground as
$U = 0$" as the first line of your answer — examiners give credit for it, and it
stops sign errors later.
:::

::: example Worked example 5.3
**Problem.** A block of mass $2\ \text{kg}$ slides along a rough horizontal
surface at $10\ \text{m s}^{-1}$ and comes to rest. If $\mu = 0.25$ and
$g = 10\ \text{m s}^{-2}$, how far does it travel? What is the retarding force?

**Solution.** The only force doing work is friction,
$f = \mu mg = 0.25 \times 2 \times 10 = 5\ \text{N}$, acting backwards.
By the work–energy theorem, $-fs = 0 - \frac{1}{2}mu^{2}$:

$$ s = \frac{mu^{2}}{2f} = \frac{2 \times 100}{2 \times 5} = 20\ \text{m} $$

The retarding force is $5\ \text{N}$ and the stopping distance is $20\ \text{m}$.
Note that the stopping distance goes as $u^{2}$: double the speed, four times the
distance. That is the physics behind highway speed limits on the Mugling road.
:::

## 5.4 Conservation of energy

::: key Principle of conservation of energy
Energy can neither be created nor destroyed; it can only be converted from one
form to another. The total energy of an isolated system is constant.
:::

When only gravity and other conservative forces act, the mechanical form of the
law applies:

$$ K + U = \text{constant} \qquad \Longrightarrow \qquad \tfrac{1}{2}mv^{2} + mgh = \tfrac{1}{2}mu^{2} + mgh_0 $$

::: derivation Mechanical energy is conserved for a freely falling body
We start with a body of mass $m$ released from rest at a height $H$, and show that
at *every* point of its fall the sum $K + U$ has the same value $mgH$.

**Setting up.** Take the ground as the level where $U = 0$ (always write this line
down). Let the body have fallen to a height $h$ above the ground, so the distance
already fallen is $H - h$.

**Step 1 — the potential energy at height $h$.** By definition $U = mgh$:

$$ U = mgh $$

**Step 2 — find the speed at height $h$.** Apply $v^{2} = u^{2} + 2as$ to the fall
so far. It started from rest, so $u = 0$; the acceleration is $g$ downwards and the
distance fallen is $(H - h)$:

$$ v^{2} = 0 + 2g(H - h) $$

so

$$ v^{2} = 2g(H - h) $$

**Step 3 — the kinetic energy at height $h$.** Put this $v^{2}$ into
$K = \frac{1}{2}mv^{2}$:

$$ K = \tfrac{1}{2}m \cdot 2g(H - h) $$

**Step 4 — the 2 and the $\frac{1}{2}$ cancel:**

$$ K = mg(H - h) $$

**Step 5 — add the two energies:**

$$ K + U = mg(H - h) + mgh $$

**Step 6 — open the bracket:**

$$ K + U = mgH - mgh + mgh $$

**Step 7 — the two $mgh$ terms cancel:**

$$ K + U = mgH $$

**Result.** At every height $h$ during the fall,

$$ K + U = mgH = \text{constant} $$

**Check the two ends.** At the top, $h = H$: $U = mgH$ and $K = 0$. At the ground,
$h = 0$: $U = 0$ and $K = mgH$, so the landing speed is $v = \sqrt{2gH}$. The answer
$mgH$ is the same at both ends and everywhere in between.

**What it means.** Potential energy is not destroyed, it is *converted*: for every
joule of $U$ lost, exactly one joule of $K$ appears. Note that $h$ disappeared from
the answer — that is the whole content of the conservation law.

**Conditions used.** Air resistance is neglected (otherwise some energy becomes heat
and $K + U$ falls), $g$ is constant over the height $H$, and the body is released
from **rest**. If it were thrown down with speed $u$, the constant total would be
$mgH + \frac{1}{2}mu^{2}$ instead.
:::

```figure caption="Energy of a body falling freely from height $H$. $U$ falls linearly, $K$ rises linearly, and the total $K+U = mgH$ stays constant."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6,2.8))
h = np.linspace(0,20,200); m=1.0; g=10.0; H=20.0
U = m*g*h; K = m*g*(H-h); E = U+K
ax.plot(h,U,color=ACCENT,lw=1.9,label='potential energy $U$')
ax.plot(h,K,color='#d9534f',lw=1.9,label='kinetic energy $K$')
ax.plot(h,E,color='#2e8b57',lw=2.0,ls='--',label='total $K+U$')
ax.set_xlabel('height above ground $h$ (m)')
ax.set_ylabel('energy (J per kg)')
ax.set_xlim(0,20); ax.set_ylim(0,212)
ax.invert_xaxis()
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.5)
# legend lifted out of the plot: inside, the two sloping lines run through it
ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1.01), ncol=3, fontsize=8.4,
          columnspacing=1.5, handlelength=1.7)
```
::: caution Conservation is not "mechanical energy is always constant"
If friction, air resistance or a collision is involved, mechanical energy is
**not** conserved — some is converted to heat and sound. Total energy is still
conserved. In that case use the work–energy theorem with the friction work
included, not $K+U=$ constant.
:::

## 5.5 Conservative and non-conservative forces

::: definition Conservative force
A force is **conservative** if the work it does in moving a body between two
points is independent of the path taken, and consequently the work it does around
any closed path is zero. A potential energy function can be defined for it, with
$F = -\,dU/dx$. A force for which this fails is **non-conservative**.
:::

Lift a 1 kg bag from the courtyard to the first floor of a house in Bhaktapur.
Carry it straight up the stairs, or up to the second floor and back down — the
work done against gravity is the same, $mgh$, because only the *change of height*
matters. Gravity is conservative. Drag the same bag across the floor by a long
route and a short route, and friction takes far more energy on the long route.
Friction is non-conservative.

| | Conservative | Non-conservative |
|---|---|---|
| Work depends on path? | No | Yes |
| Work in a closed loop | zero | non-zero (usually negative) |
| Potential energy defined? | Yes | No |
| Energy recoverable? | Fully | No — degraded to heat |
| Examples | gravity, spring force, electrostatic force | friction, air drag, viscous force, tension in an inelastic string |

When both kinds act, the work–energy theorem splits as

$$ W_{c} + W_{nc} = \Delta K, \qquad W_{c} = -\Delta U
\;\Longrightarrow\; W_{nc} = \Delta K + \Delta U = \Delta E $$

So the work done by non-conservative forces measures exactly how much mechanical
energy is lost.

## 5.6 Elastic and inelastic collisions

In every collision between two isolated bodies the external forces are negligible
during the short contact time, so **linear momentum is always conserved**.
Whether kinetic energy is also conserved decides the type.

| | Elastic | Inelastic | Perfectly inelastic |
|---|---|---|---|
| Momentum | conserved | conserved | conserved |
| Kinetic energy | conserved | not conserved | maximum loss |
| Bodies after impact | separate | separate | move together |
| Coefficient of restitution $e$ | $1$ | $0 < e < 1$ | $0$ |
| Example | collision of gas molecules, alpha particle and nucleus | ball bouncing to a lower height | bullet embedding in a block; mud thrown at a wall |

::: derivation Final velocities in a one-dimensional elastic collision
We start from the two conservation laws — momentum and kinetic energy — and reach
formulas for the velocities of both bodies after the collision.

**Setting up.** Masses $m_1$ and $m_2$ move along the same straight line with
velocities $u_1$ and $u_2$ before impact and $v_1$ and $v_2$ after it. All four are
*signed* quantities: rightward positive, leftward negative.

**Step 1 — momentum is conserved** (no external force during the short contact):

$$ m_1u_1 + m_2u_2 = m_1v_1 + m_2v_2 \qquad (1) $$

**Step 2 — kinetic energy is conserved** (this is what "elastic" means):

$$ \tfrac{1}{2}m_1u_1^{2} + \tfrac{1}{2}m_2u_2^{2}
= \tfrac{1}{2}m_1v_1^{2} + \tfrac{1}{2}m_2v_2^{2} $$

**Step 3 — clear the $\frac{1}{2}$** by multiplying every term by 2:

$$ m_1u_1^{2} + m_2u_2^{2} = m_1v_1^{2} + m_2v_2^{2} \qquad (2) $$

**Step 4 — group body 1 on the left in equation (1).** Take the $m_1$ terms to the
left and the $m_2$ terms to the right:

$$ m_1u_1 - m_1v_1 = m_2v_2 - m_2u_2 $$

Take out the common factors:

$$ m_1(u_1 - v_1) = m_2(v_2 - u_2) \qquad (3) $$

**Step 5 — do the same to equation (2):**

$$ m_1u_1^{2} - m_1v_1^{2} = m_2v_2^{2} - m_2u_2^{2} $$

$$ m_1(u_1^{2} - v_1^{2}) = m_2(v_2^{2} - u_2^{2}) \qquad (4) $$

**Step 6 — factorise both differences of squares** using
$x^{2} - y^{2} = (x-y)(x+y)$:

$$ m_1(u_1 - v_1)(u_1 + v_1) = m_2(v_2 - u_2)(v_2 + u_2) $$

**Step 7 — divide this by equation (3).** The left side of (3) is identical to the
first factor on the left here, and the same for the right — so those factors cancel.
(This needs $u_1 \ne v_1$, i.e. a real collision actually happened.)

$$ u_1 + v_1 = v_2 + u_2 \qquad (5) $$

**Step 8 — rearrange (5) into its physical form.** Subtract $u_2$ and $v_1$ from both
sides:

$$ u_1 - u_2 = v_2 - v_1 $$

In words: **the relative velocity of separation equals the relative velocity of
approach.** This is the most useful single line in the whole topic.

**Step 9 — make $v_2$ the subject of (5):**

$$ v_2 = u_1 + v_1 - u_2 $$

**Step 10 — substitute this $v_2$ into the momentum equation (1):**

$$ m_1u_1 + m_2u_2 = m_1v_1 + m_2(u_1 + v_1 - u_2) $$

**Step 11 — open the bracket:**

$$ m_1u_1 + m_2u_2 = m_1v_1 + m_2u_1 + m_2v_1 - m_2u_2 $$

**Step 12 — collect every $v_1$ term on the right and everything else on the left.**
Move $m_2u_1$ across (it becomes negative) and $-m_2u_2$ across (it becomes
positive):

$$ m_1u_1 - m_2u_1 + m_2u_2 + m_2u_2 = m_1v_1 + m_2v_1 $$

**Step 13 — factorise both sides:**

$$ (m_1 - m_2)u_1 + 2m_2u_2 = (m_1 + m_2)v_1 $$

**Step 14 — divide both sides by $(m_1+m_2)$:**

$$ v_1 = \left(\frac{m_1 - m_2}{m_1 + m_2}\right)u_1 + \frac{2m_2u_2}{m_1 + m_2} $$

**Step 15 — get $v_2$ the same way.** From (5), $v_1 = v_2 + u_2 - u_1$. Put that into
(1):

$$ m_1u_1 + m_2u_2 = m_1(v_2 + u_2 - u_1) + m_2v_2 $$

**Step 16 — open the bracket:**

$$ m_1u_1 + m_2u_2 = m_1v_2 + m_1u_2 - m_1u_1 + m_2v_2 $$

**Step 17 — collect the $v_2$ terms on the right and the rest on the left:**

$$ 2m_1u_1 + m_2u_2 - m_1u_2 = (m_1 + m_2)v_2 $$

**Step 18 — factorise the $u_2$ terms and divide by $(m_1+m_2)$:**

$$ v_2 = \frac{2m_1u_1}{m_1 + m_2} + \left(\frac{m_2 - m_1}{m_1 + m_2}\right)u_2 $$

**Result.**

$$ v_1 = \left(\frac{m_1-m_2}{m_1+m_2}\right)u_1 + \frac{2m_2u_2}{m_1+m_2},
\qquad v_2 = \left(\frac{m_2-m_1}{m_1+m_2}\right)u_2 + \frac{2m_1u_1}{m_1+m_2} $$

**What it means.** The outcome depends on the **mass ratio**, not on how hard the
bodies hit. If $m_1 = m_2$ the first bracket is zero and the bodies simply swap
velocities. If $m_1 \ll m_2$ the first bracket is nearly $-1$, so the light body
bounces straight back.

**Conditions used.** One-dimensional (head-on) collision; kinetic energy exactly
conserved ($e = 1$); no external force during contact; signs kept consistently.
Step 7 also assumed the bodies really did interact ($u_1 \ne v_1$).
:::

::: tip The examiner is looking for
(i) Both conservation equations written down and *labelled*; (ii) the factorising of
the energy equation into a difference of two squares; (iii) the division step with
the words "dividing (4) by (3)"; (iv) the relative-velocity result
$u_1 - u_2 = v_2 - v_1$ stated in words — it is often a mark on its own;
(v) substitution back into momentum to get both final velocities. Check your answer
by putting $m_1 = m_2$ and seeing the velocities swap.
:::

Three special cases are worth memorising, all with $u_2 = 0$:

- **Equal masses** ($m_1 = m_2$): $v_1 = 0$, $v_2 = u_1$ — the bodies exchange
  velocities. This is the carrom-striker result.
- **Heavy hits light** ($m_1 \gg m_2$): $v_1 \approx u_1$, $v_2 \approx 2u_1$ —
  the light body is flung away at twice the speed.
- **Light hits heavy** ($m_1 \ll m_2$): $v_1 \approx -u_1$, $v_2 \approx 0$ — the
  light body bounces straight back with almost unchanged speed.

```figure caption="Head-on elastic collision of a $2$ kg body at $6\ \mathrm{m\,s^{-1}}$ with a stationary $4$ kg body. The lighter body rebounds; momentum and kinetic energy both balance."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle
fig, ax = plt.subplots(figsize=(5.0,2.6))
def body(x,y,r,lab,c):
    ax.add_patch(Circle((x,y), r, fc=c, ec=INK, lw=1.1, alpha=.85))
    ax.annotate(lab,(x,y),ha='center',va='center',fontsize=8.6,color='white')
def vel(x,y,dx,lab,c,dy=7):
    ax.annotate('', xy=(x+dx,y), xytext=(x,y),
        arrowprops=dict(arrowstyle='-|>', color=c, lw=1.7, mutation_scale=12))
    ax.annotate(lab,(x+dx/2,y),textcoords='offset points',xytext=(0,dy),
                ha='center', va='bottom' if dy > 0 else 'top', color=c, fontsize=8.8)
ax.annotate('before', (0.1,2.85), fontsize=9.2, color=MUTED)
body(1.2,2.6,0.34,'2 kg',ACCENT); body(4.2,2.6,0.44,'4 kg','#2e8b57')
vel(1.7,2.6,1.2,r'$6\ \mathrm{m\,s^{-1}}$',INK)
ax.annotate('at rest',(4.2,2.6),textcoords='offset points',xytext=(0,26),
            ha='center',color=MUTED,fontsize=8.8)
ax.annotate('after', (0.1,0.95), fontsize=9.2, color=MUTED)
body(1.6,0.7,0.34,'2 kg',ACCENT); body(4.6,0.7,0.44,'4 kg','#2e8b57')
# rebound speed labelled below its arrow so it cannot collide with "after"
vel(1.2,0.7,-0.95,r'$2\ \mathrm{m\,s^{-1}}$','#d9534f',dy=-8)
vel(5.15,0.7,1.5,r'$4\ \mathrm{m\,s^{-1}}$',INK)
ax.set_xlim(0,7.2); ax.set_ylim(0,3.4); ax.set_aspect('equal'); ax.axis('off')
```
**Perfectly inelastic collision.** The bodies stick together and move with a
common velocity $v$. Momentum conservation alone fixes it:

$$ v = \frac{m_1u_1 + m_2u_2}{m_1+m_2} $$

and the kinetic energy lost, which appears as heat, sound and deformation, is

$$ \Delta K = \frac{1}{2}\left(\frac{m_1m_2}{m_1+m_2}\right)(u_1-u_2)^{2} $$

::: example Worked example 5.4
**Problem.** A body of mass $2\ \text{kg}$ moving at $6\ \text{m s}^{-1}$ collides
head-on with a stationary body of mass $4\ \text{kg}$. Find the velocities after
impact if the collision is (a) perfectly elastic, (b) perfectly inelastic, and
find the energy lost in (b).

**Solution.** (a) With $u_1 = 6\ \text{m s}^{-1}$, $u_2 = 0$:

$$ v_1 = \frac{m_1-m_2}{m_1+m_2}u_1 = \frac{2-4}{6}\times 6 = -2\ \text{m s}^{-1} $$
$$ v_2 = \frac{2m_1}{m_1+m_2}u_1 = \frac{4}{6}\times 6 = 4\ \text{m s}^{-1} $$

The $2\ \text{kg}$ body rebounds at $2\ \text{m s}^{-1}$. *Check:* momentum before
$= 12\ \text{kg m s}^{-1}$, after $= 2(-2)+4(4) = 12$ ✓; kinetic energy before
$= 36\ \text{J}$, after $= 4 + 32 = 36\ \text{J}$ ✓.

(b) Sticking together:

$$ v = \frac{2 \times 6 + 0}{2+4} = 2\ \text{m s}^{-1} $$

Kinetic energy before $= 36\ \text{J}$; after $= \frac{1}{2}(6)(2)^{2} = 12\ \text{J}$.
Energy lost $= 24\ \text{J}$, i.e. two-thirds of the original kinetic energy.
:::

::: example Worked example 5.5
**Problem.** A bullet of mass $10\ \text{g}$ travelling at $400\ \text{m s}^{-1}$
embeds itself in a wooden block of mass $1.99\ \text{kg}$ suspended by a long
string. Find the speed of the block just after impact and the height it rises.
Take $g = 10\ \text{m s}^{-2}$.

**Solution.** The collision is perfectly inelastic, so momentum is conserved
*during* the impact but kinetic energy is not:

$$ v = \frac{0.010 \times 400}{0.010 + 1.99} = \frac{4.0}{2.00} = 2\ \text{m s}^{-1} $$

*After* the impact no friction acts, so mechanical energy is conserved during the
swing:

$$ \tfrac{1}{2}Mv^{2} = Mgh \;\Longrightarrow\; h = \frac{v^{2}}{2g} = \frac{4}{20} = 0.2\ \text{m} $$

The block rises $20\ \text{cm}$. This arrangement is the **ballistic pendulum**,
used to measure bullet speeds.
:::

::: caution Do not use energy conservation during the collision
Momentum is conserved in *every* collision; kinetic energy only in an elastic
one. Write the momentum equation for the impact and the energy equation for what
happens before or after it — never the other way round.
:::

## Chapter summary

- Work by a constant force: $W = Fs\cos\theta = \vec{F}\cdot\vec{s}$, a scalar in
  joules. Zero when the force is perpendicular to the displacement.
- Work by a variable force: $W = \int F\,dx$ = area under the $F$–$x$ graph.
  For a spring, $W = \frac{1}{2}kx^{2}$.
- Power $P = W/t = \vec{F}\cdot\vec{v}$; $1\ \text{hp} = 746\ \text{W}$ and
  $1\ \text{kW h} = 3.6\times 10^{6}\ \text{J}$.
- Work–energy theorem: $W_{net} = \Delta K$, with $K = \frac{1}{2}mv^{2} = p^{2}/2m$.
- Potential energy: $U = mgh$ (gravitational), $U = \frac{1}{2}kx^{2}$ (elastic).
- Conservation of energy: $K + U$ is constant when only conservative forces act;
  otherwise $W_{nc} = \Delta K + \Delta U$.
- Conservative forces do path-independent work and zero work round a closed loop;
  friction and drag do not.
- All collisions conserve momentum. Elastic ones also conserve kinetic energy and
  give $u_1 - u_2 = v_2 - v_1$; perfectly inelastic ones lose
  $\frac{1}{2}\frac{m_1m_2}{m_1+m_2}(u_1-u_2)^{2}$.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. A coolie carries a load horizontally along a level platform. The work done by
   him on the load is <span class="marks">[1]</span>
   (a) $mgh$ (b) zero (c) negative (d) $mgs$
2. The area under a force–displacement graph represents <span class="marks">[1]</span>
   (a) power (b) impulse (c) work done (d) momentum
3. A body of mass $m$ has momentum $p$. Its kinetic energy is <span class="marks">[1]</span>
   (a) $mp^{2}$ (b) $p^{2}/2m$ (c) $p^{2}/m$ (d) $2mp^{2}$
4. Which of the following is a non-conservative force? <span class="marks">[1]</span>
   (a) gravitational force (b) spring force (c) electrostatic force (d) viscous force
5. In a perfectly inelastic collision, the quantity that is **not** conserved is <span class="marks">[1]</span>
   (a) linear momentum (b) total energy (c) kinetic energy (d) mass

::: note Answers to Group A
**1.** (b) — the supporting force is vertical, the displacement horizontal, so $\theta = 90^{\circ}$.
**2.** (c) — $W = \int F\,dx$ is exactly the area under the curve.
**3.** (b) — $K = \frac{1}{2}mv^2$ and $p = mv$, so $K = p^2/2m$.
**4.** (d) — viscous drag depends on the path and dissipates energy as heat.
**5.** (c) — momentum and total energy are conserved; kinetic energy is lost to heat and deformation.
:::

**Group B — Short answer (5 marks each)**

1. Define work, energy and power, and state their SI units. Show that the
   work done by a variable force is the area under the force–displacement
   graph. <span class="marks">[5]</span>
2. State and prove the work–energy theorem for a body moving under a constant
   force. <span class="marks">[5]</span>
3. Distinguish between conservative and non-conservative forces with two examples
   of each. <span class="marks">[5]</span>
4. A car of mass $1000\ \text{kg}$ moves up an incline of $1$ in $20$ at a steady
   $20\ \text{m s}^{-1}$ against a frictional resistance of $200\ \text{N}$.
   Calculate the power developed by the engine. Take $g = 10\ \text{m s}^{-2}$. <span class="marks">[5]</span>
5. A spring of force constant $200\ \text{N m}^{-1}$ is compressed by
   $0.10\ \text{m}$ and used to push a block of mass $0.50\ \text{kg}$ along a
   frictionless table. Find the elastic potential energy stored and the speed of
   the block when the spring returns to its natural length. <span class="marks">[5]</span>

::: note Answers to Group B
**4.** At steady speed the driving force balances gravity component plus friction:
$F = mg\sin\theta + R = 1000 \times 10 \times \frac{1}{20} + 200 = 500 + 200 = 700\ \text{N}$.
Then $P = Fv = 700 \times 20 = 14000\ \text{W} = 14\ \text{kW}$.

**5.** $U = \frac{1}{2}kx^{2} = \frac{1}{2}(200)(0.10)^{2} = 1.0\ \text{J}$.
All of it becomes kinetic energy: $\frac{1}{2}(0.50)v^{2} = 1.0$, so
$v^{2} = 4.0$ and $v = 2.0\ \text{m s}^{-1}$.

**1., 2., 3.** See §5.1, the derivation box in §5.3, and the comparison table in §5.5.
:::

**Group C — Long answer (8 marks each)**

1. (a) State the principle of conservation of energy. <span class="marks">[2]</span>
   (b) Show that for a body falling freely from a height $H$ the sum of its
   kinetic and potential energies is the same at every point of the fall. <span class="marks">[4]</span>
   (c) A stone of mass $0.5\ \text{kg}$ is dropped from $45\ \text{m}$. Find its
   kinetic energy and its speed when it is $20\ \text{m}$ above the ground
   ($g = 10\ \text{m s}^{-2}$). <span class="marks">[2]</span>
2. (a) Derive expressions for the final velocities of two bodies undergoing a
   perfectly elastic head-on collision, and deduce the result for equal
   masses. <span class="marks">[6]</span>
   (b) A $5\ \text{kg}$ body moving at $4\ \text{m s}^{-1}$ collides with a
   stationary $3\ \text{kg}$ body and they move off together. Find their common
   velocity and the kinetic energy lost. <span class="marks">[2]</span>

::: note Answers to Group C
**1.** (b) See §5.4: at height $h$, $v^{2} = 2g(H-h)$ so $K = mg(H-h)$ while
$U = mgh$, giving $K+U = mgH$ everywhere.
(c) The stone has fallen $45 - 20 = 25\ \text{m}$, so
$K = mg(H-h) = 0.5 \times 10 \times 25 = 125\ \text{J}$ and
$v = \sqrt{2K/m} = \sqrt{500} = 22.4\ \text{m s}^{-1}$.

**2.** (a) See the derivation box in §5.6; for $m_1 = m_2$ the prefactor
$(m_1-m_2)/(m_1+m_2)$ vanishes, so with $u_2=0$ we get $v_1 = 0$, $v_2 = u_1$ —
the bodies exchange velocities.
(b) $v = \dfrac{5 \times 4 + 0}{5+3} = 2.5\ \text{m s}^{-1}$.
$K_i = \frac{1}{2}(5)(16) = 40\ \text{J}$, $K_f = \frac{1}{2}(8)(2.5)^{2} = 25\ \text{J}$,
so the loss is $15\ \text{J}$.
:::
