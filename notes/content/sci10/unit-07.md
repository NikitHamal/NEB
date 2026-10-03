---
subject: Science and Technology
grade: 10
unit: 7
title: Motion and Force
hours: 0
area: Science and Technology
---

Everything around us moves, or stays still because forces balance. A bus starts, a football flies, a ripe mango falls from a tree, the Moon circles the Earth. In this unit you learn the three simple laws that explain all of these. Isaac Newton wrote them down more than 300 years ago, and engineers still use them to design vehicles, bridges and rockets. You will also learn what momentum is, why a heavy lorry is harder to stop than a cycle, why all things fall to the ground, and how weight is different from mass.

::: key What SEE asks from this unit
Expect definitions (force, momentum, mass, weight, free fall), the statements of Newton's three laws, the formulae $F = ma$, $p = mv$, $F = G\dfrac{m_1 m_2}{d^2}$, $W = mg$, and numericals on each. Also expect reasoning questions that start with "Why …?" such as "Why do we fall forward when a bus stops suddenly?".
:::

## 7.1 Newton's laws

### Force and its effects

A **force** is a push or a pull. We cannot see a force, but we see what it does. A force can:

- start a body moving or stop it (kicking a football at rest, a goalkeeper catching it),
- speed up or slow down a moving body,
- change the direction of motion (a cricket bat hitting a ball back),
- change the shape or size of a body (pressing a sponge, stretching a spring).

The SI unit of force is the **newton (N)**. Forces are vectors: each has a size and a direction. When two or more forces act on a body, we add them as vectors. The single force that has the same effect as all of them together is the **net force** (or resultant force).

- Two forces in the same direction: net force = sum.
- Two forces in opposite directions: net force = difference, in the direction of the larger one.
- If the net force is zero, the forces are **balanced**. If it is not zero, they are **unbalanced**.

### Newton's first law (law of inertia)

::: definition Newton's first law
A body at rest remains at rest, and a body in motion continues to move with constant speed in a straight line, unless an external unbalanced force acts on it.
:::

This tells us that a body does not change its state of rest or motion by itself. The property of a body to resist any change in its state of rest or of uniform motion is called **inertia**. This is why the first law is also called the law of inertia.

**Inertia depends on mass.** The greater the mass of a body, the greater its inertia. A loaded truck is harder to start and harder to stop than an empty one.

Types of inertia:

| Type | Meaning | Example |
|---|---|---|
| Inertia of rest | A body at rest stays at rest | Dust falls out of a carpet when you beat it; passengers jerk backward when a bus starts suddenly |
| Inertia of motion | A moving body stays in motion | Passengers fall forward when a moving bus brakes; a runner cannot stop at once |
| Inertia of direction | A body keeps its direction of motion | Mud flies off a turning wheel along the tangent; passengers lean outward when a bus takes a sharp turn |

::: caution Inertia is not a force
Students often write "inertia is a force that keeps the body moving". This is wrong. Inertia is a **property** (a tendency) of matter. It is measured by mass. Only a push or a pull is a force.
:::

### Newton's second law

Think of pushing an empty cart and a full cart with the same push. The empty cart speeds up faster. Now push the same cart with a small and then a large force. The large force gives a larger acceleration. Newton put this in the second law.

::: definition Newton's second law
The rate of change of momentum of a body is directly proportional to the unbalanced force applied on it, and the change takes place in the direction of the force.
:::

For a body of constant mass this gives the working form of the law:

$$ F = ma $$

where $F$ is the net force in newtons, $m$ is the mass in kg, and $a$ is the acceleration in m s⁻².

::: key Definition of the newton
One newton is the force that gives a mass of 1 kg an acceleration of 1 m s⁻². So $1\ \text{N} = 1\ \text{kg m s}^{-2}$.
:::

We can see from $a = F/m$ that acceleration is directly proportional to force when mass is fixed, and inversely proportional to mass when force is fixed.

```figure caption="Newton's second law. Left: acceleration is proportional to force for a fixed mass. Right: acceleration falls as mass increases for a fixed force of 12 N."
import numpy as np, matplotlib.pyplot as plt
fig, (a1, a2) = plt.subplots(1, 2, figsize=(5.0, 2.6))
F = np.linspace(0, 12, 50)
a1.plot(F, F/2.0, color=ACCENT, lw=2)
a1.set_xlabel('force F (N)'); a1.set_ylabel('acceleration a (m/s2)')
a1.set_title('m = 2 kg', fontsize=9, color=INK)
a1.set_xlim(0, 12); a1.set_ylim(0, 6.5)
a1.spines[['top','right']].set_visible(False); a1.grid(True, alpha=.5)
m = np.linspace(1, 12, 80)
a2.plot(m, 12.0/m, color='#A8271F', lw=2)
a2.set_xlabel('mass m (kg)'); a2.set_ylabel('acceleration a (m/s2)')
a2.set_title('F = 12 N', fontsize=9, color=INK)
a2.set_xlim(0, 12); a2.set_ylim(0, 13)
a2.spines[['top','right']].set_visible(False); a2.grid(True, alpha=.5)
fig.tight_layout()
```

::: example Force and acceleration
**Problem.** A force of 20 N acts on a box of mass 5 kg lying on a smooth floor. (a) Find its acceleration. (b) If a friction force of 5 N opposes the motion, find the new acceleration.

**Solution.**
(a) $a = \dfrac{F}{m} = \dfrac{20}{5} = 4\ \text{m s}^{-2}$.

(b) Net force $= 20 - 5 = 15$ N. So $a = \dfrac{15}{5} = 3\ \text{m s}^{-2}$.
:::

::: example Finding the force on a car
**Problem.** A car of mass 800 kg speeds up from rest to 20 m s⁻¹ in 10 s. Find the force the engine must supply to the car, ignoring friction.

**Solution.** Acceleration $a = \dfrac{v-u}{t} = \dfrac{20-0}{10} = 2\ \text{m s}^{-2}$.

Force $F = ma = 800 \times 2 = 1600$ N.
:::

### Newton's third law

::: definition Newton's third law
To every action there is an equal and opposite reaction. The action and the reaction act on two different bodies.
:::

Forces always come in pairs. If body A pushes body B with force $F_{AB}$, then B pushes A with a force $F_{BA}$ of the same size but opposite direction:

$$ F_{AB} = -F_{BA} $$

Examples from daily life:

- **Walking.** Your foot pushes the ground backward; the ground pushes you forward.
- **Swimming.** The swimmer pushes the water backward; the water pushes the swimmer forward.
- **Rocket and jet.** Hot gas is thrown out backward at high speed; the gas pushes the rocket forward.
- **Gun recoil.** The gun pushes the bullet forward; the bullet pushes the gun backward.
- **Rowing a boat.** The oar pushes water backward, the water pushes the boat forward.
- **Balloon.** Air rushes out of the mouth of a released balloon, and the balloon shoots the other way.

::: caution Why action and reaction do not cancel
Action and reaction are equal and opposite, yet they do not cancel each other. They act on **different** bodies. Forces cancel only when they act on the **same** body. A horse pulls a cart and the cart pulls the horse back with an equal force, but the cart still moves, because the force that the ground exerts on the horse is larger than the pull of the cart.
:::

## 7.2 Momentum

### Linear momentum

A cricket ball and a tennis ball move at the same speed. The cricket ball hurts more when it hits you. A slow-moving truck is harder to stop than a fast cycle. The quantity that includes both mass and velocity is **momentum**.

::: definition Momentum
The momentum of a body is the product of its mass and its velocity.
:::

$$ p = mv $$

The SI unit is **kg m s⁻¹**. Momentum is a vector and points in the direction of the velocity. A body at rest has zero momentum.

### Force and change of momentum

Suppose a body of mass $m$ changes its velocity from $u$ to $v$ in time $t$ under a constant force $F$. Newton's second law in its original form says force equals the rate of change of momentum.

::: derivation $F = ma$ from the change of momentum
We start from Newton's second law and reach the formula $F = ma$.

**Setting up.** A body of mass $m$ has initial velocity $u$ and final velocity $v$ after time $t$.

**Step 1 — initial and final momentum.**

$$ p_1 = mu, \qquad p_2 = mv $$

**Step 2 — change of momentum.**

$$ \Delta p = mv - mu = m(v-u) $$

**Step 3 — rate of change of momentum.** Divide by the time taken:

$$ \frac{\Delta p}{t} = \frac{m(v-u)}{t} $$

**Step 4 — use the second law.** Force is proportional to this rate. Choosing the unit of force so that the constant is 1:

$$ F = \frac{m(v-u)}{t} $$

**Step 5 — acceleration.** Since $a = \dfrac{v-u}{t}$,

$$ F = ma $$

**Result.** $F = \dfrac{\Delta p}{t} = ma$.

**What it means.** The same change of momentum can be produced by a large force for a short time or a small force for a long time. Mass is taken as constant.
:::

::: tip The examiner is looking for
Write the initial and final momentum, the change, divide by $t$, then replace $(v-u)/t$ by $a$. Three marks usually go to the change of momentum, the use of the second law and the final result.
:::

### Impulse

From $F = \dfrac{mv - mu}{t}$ we get $Ft = mv - mu$. The product $F \times t$ is called **impulse**. It equals the change in momentum. Its unit is N s, which is the same as kg m s⁻¹.

This explains many everyday safety ideas:

- A cricketer pulls his hands back while catching a fast ball. The time of stopping is longer, so the force on the hands is smaller.
- A high jumper lands on a thick foam bed instead of hard ground. The stopping time is longer, so the force is smaller.
- Cars have air bags and crumple zones. They increase the time of the collision and so reduce the force on the passengers.
- A person jumping from a height bends the knees on landing.

::: example Stopping a car
**Problem.** A car of mass 1200 kg moves at 15 m s⁻¹. The brakes bring it to rest in 6 s. Find (a) its initial momentum and (b) the average braking force.

**Solution.**
(a) $p = mv = 1200 \times 15 = 18000$ kg m s⁻¹.

(b) Final momentum is zero, so $\Delta p = 0 - 18000 = -18000$ kg m s⁻¹.

$F = \dfrac{\Delta p}{t} = \dfrac{-18000}{6} = -3000$ N.

The magnitude of the braking force is 3000 N. The minus sign shows that it acts opposite to the motion.
:::

### Conservation of linear momentum

::: definition Law of conservation of momentum
When two or more bodies act on each other and no external force acts on the system, the total momentum of the system remains constant. Total momentum before collision equals total momentum after collision.
:::

For two bodies of masses $m_1$ and $m_2$ with initial velocities $u_1$ and $u_2$ and final velocities $v_1$ and $v_2$:

$$ m_1 u_1 + m_2 u_2 = m_1 v_1 + m_2 v_2 $$

::: derivation Conservation of momentum from Newton's laws
We use the second and third laws for two colliding bodies.

**Setting up.** Body A (mass $m_1$, velocity $u_1$) hits body B (mass $m_2$, velocity $u_2$) with $u_1 > u_2$. They touch for a time $t$. After the collision their velocities are $v_1$ and $v_2$.

**Step 1 — force on B by A.** From the second law:

$$ F_{AB} = \frac{m_2 v_2 - m_2 u_2}{t} $$

**Step 2 — force on A by B.**

$$ F_{BA} = \frac{m_1 v_1 - m_1 u_1}{t} $$

**Step 3 — use the third law.** The two forces are equal and opposite, so $F_{AB} = -F_{BA}$:

$$ \frac{m_2 v_2 - m_2 u_2}{t} = -\frac{m_1 v_1 - m_1 u_1}{t} $$

**Step 4 — cancel $t$ and rearrange.**

$$ m_2 v_2 - m_2 u_2 = m_1 u_1 - m_1 v_1 $$

$$ m_1 u_1 + m_2 u_2 = m_1 v_1 + m_2 v_2 $$

**Result.** Total momentum before = total momentum after.

**Condition.** No external unbalanced force acts on the two-body system.
:::

Applications of the law: recoil of a gun, the working of rockets and jet planes, the motion of a boat when a person jumps off it, and collisions between vehicles or balls.

```figure caption="Collision of two trolleys. The total momentum 4 x 6 = 24 kg m/s before the collision is the same as (4 + 2) x 4 = 24 kg m/s after the trolleys stick together."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
fig, ax = plt.subplots(figsize=(4.8, 2.6))
ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis('off')
def cart(x, y, w, col, lab):
    ax.add_patch(Rectangle((x, y+0.3), w, 0.9, fc=col, ec=INK, lw=1.2))
    ax.add_patch(Circle((x+0.3, y+0.3), 0.25, fc='white', ec=INK))
    ax.add_patch(Circle((x+w-0.3, y+0.3), 0.25, fc='white', ec=INK))
    ax.text(x+w/2, y+0.75, lab, ha='center', va='center', fontsize=8.5, color='white')
ax.text(0.2, 5.5, 'Before', fontsize=9.5, color=INK, weight='bold')
cart(0.8, 3.7, 2.0, ACCENT, '4 kg')
cart(5.0, 3.7, 1.4, '#A8271F', '2 kg')
ax.annotate('', xy=(4.0, 5.1), xytext=(1.2, 5.1), arrowprops=dict(arrowstyle='->', color=INK))
ax.text(2.6, 4.75, 'u1 = 6 m/s', ha='center', fontsize=8.5, color=INK)
ax.text(5.7, 5.05, 'u2 = 0', ha='center', fontsize=8.5, color=INK)
ax.plot([0.2, 9.8], [3.7, 3.7], color=MUTED, lw=1)
ax.text(0.2, 2.5, 'After', fontsize=9.5, color=INK, weight='bold')
cart(3.0, 0.5, 2.0, ACCENT, '4 kg')
cart(5.0, 0.5, 1.4, '#A8271F', '2 kg')
ax.annotate('', xy=(7.3, 2.3), xytext=(3.7, 2.3), arrowprops=dict(arrowstyle='->', color=INK))
ax.text(5.5, 1.95, 'v = 4 m/s (together)', ha='center', fontsize=8.5, color=INK)
ax.plot([0.2, 9.8], [0.5, 0.5], color=MUTED, lw=1)
```

::: example Collision
**Problem.** A trolley of mass 4 kg moving at 6 m s⁻¹ hits a trolley of mass 2 kg at rest. They stick together. Find their common velocity.

**Solution.** Momentum before $= 4 \times 6 + 2 \times 0 = 24$ kg m s⁻¹.

After the collision the combined mass is $4 + 2 = 6$ kg moving at $v$:

$6v = 24$, so $v = 4\ \text{m s}^{-1}$.
:::

::: example Recoil of a gun
**Problem.** A gun of mass 4 kg fires a bullet of mass 20 g at 300 m s⁻¹. Find the recoil velocity of the gun.

**Solution.** Mass of bullet $= 20\ \text{g} = 0.02$ kg. Initially both are at rest, so total momentum is zero.

After firing: $0 = m_b v_b + m_g v_g$, so

$$ v_g = -\frac{m_b v_b}{m_g} = -\frac{0.02 \times 300}{4} = -1.5\ \text{m s}^{-1} $$

The gun recoils at 1.5 m s⁻¹ opposite to the bullet.
:::

## 7.3 Gravitation

### Universal law of gravitation

An apple falls from a tree. The Moon does not fall to Earth, but it keeps circling it. Newton saw that one force explains both: the force of **gravitation**, an attraction between every two bodies in the universe.

```photo id="sci10/earthrise" caption="The Earth rising above the Moon, photographed by the Apollo 8 crew in 1968. The Moon is held in its orbit round the Earth by gravitation." width="70"
```

::: definition Newton's law of universal gravitation
Every body in the universe attracts every other body with a force that is directly proportional to the product of their masses and inversely proportional to the square of the distance between their centres.
:::

$$ F = G\,\frac{m_1 m_2}{d^{2}} $$

Here $G$ is the **universal gravitational constant**, $G = 6.67 \times 10^{-11}\ \text{N m}^2\text{ kg}^{-2}$. Its value is the same everywhere in the universe. The force is always attractive, and the two bodies pull each other with equal and opposite forces (third law).

::: example Force between two bodies
**Problem.** Find the gravitational force between two masses of 10 kg each placed 1 m apart.

**Solution.**
$F = \dfrac{6.67\times10^{-11} \times 10 \times 10}{1^2} = 6.67 \times 10^{-9}$ N.

This is extremely small. That is why we do not feel two ordinary objects attract each other. Gravity is noticeable only when at least one mass is huge, like the Earth.
:::

What happens if the distance doubles? Since $F \propto 1/d^2$, the force becomes $\tfrac14$. If either mass doubles, the force doubles.

### Gravity of the Earth

The force with which the Earth pulls a body toward its centre is called the **force of gravity**. The acceleration produced by this force is the **acceleration due to gravity**, $g$.

::: derivation Expression for $g$ on the Earth's surface
We equate the gravitational force to the weight of a body.

**Setting up.** Let the Earth have mass $M$ and radius $R$. A body of mass $m$ is on its surface.

**Step 1 — law of gravitation.** The pull of the Earth on the body is

$$ F = \frac{GMm}{R^2} $$

**Step 2 — Newton's second law.** This force gives the body acceleration $g$:

$$ F = mg $$

**Step 3 — equate.**

$$ mg = \frac{GMm}{R^2} $$

**Step 4 — cancel $m$.**

$$ g = \frac{GM}{R^2} $$

**Result.** $g = GM/R^2$.

**What it means.** $g$ does not depend on the mass of the falling body. It depends only on the mass and radius of the Earth.
:::

With $M = 6 \times 10^{24}$ kg and $R = 6.4 \times 10^{6}$ m we get $g \approx 9.8\ \text{m s}^{-2}$. Using the same formula the value of $g$ on the Moon is about $1.6\ \text{m s}^{-2}$, which is about $\tfrac16$ of that on the Earth.

### Variation of $g$

The value of $g$ is not exactly the same everywhere.

| Place | Effect on $g$ | Reason |
|---|---|---|
| Poles | Maximum (about 9.83 m s⁻²) | The Earth is slightly flattened, so the radius is smallest |
| Equator | Minimum (about 9.78 m s⁻²) | Radius is largest |
| Going up a mountain or into the air | Decreases | $d$ from the centre increases |
| Going down a mine | Decreases | Less mass of the Earth lies below you |
| Centre of the Earth | Zero | The pull from all sides cancels |

Kathmandu (about 1,400 m) has a slightly smaller $g$ than the sea-level plain at Birgunj, but the difference is far too small to notice in daily life.

```figure caption="Variation of g with height above the Earth's surface (R = 6400 km). g falls as 1/(R + h)^2."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6, 2.7))
R = 6400.0
h = np.linspace(0, 20000, 200)
g = 9.8*(R/(R+h))**2
ax.plot(h, g, color=ACCENT, lw=2)
ax.plot([0], [9.8], 'o', color=INK, ms=4)
ax.plot([6400], [9.8/4], 'o', color='#A8271F', ms=4)
ax.annotate('surface: 9.8', (0, 9.8), xytext=(1500, 9.3), fontsize=8.5, color=INK)
ax.annotate('h = R: g/4 = 2.45', (6400, 2.45), xytext=(7500, 4.2), fontsize=8.5, color=INK,
            arrowprops=dict(arrowstyle='-', color=MUTED))
ax.set_xlabel('height h above the surface (km)'); ax.set_ylabel('g (m/s2)')
ax.set_xlim(0, 20000); ax.set_ylim(0, 11)
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.5)
fig.tight_layout()
```

### Kepler and orbits (brief)

Satellites stay in orbit because gravity supplies the centripetal force that keeps them moving in a circle. The Moon is a natural satellite of the Earth; man-made satellites are launched by rockets. The higher the orbit, the longer the time for one revolution.

## 7.4 Weight and mass

**Mass** is the quantity of matter in a body. **Weight** is the force with which the Earth (or any planet) pulls the body toward its centre.

From $F = ma$ with $a = g$:

$$ W = mg $$

| Mass | Weight |
|---|---|
| Quantity of matter in a body | Force of gravity on the body |
| Scalar | Vector (directed toward the centre of the Earth) |
| SI unit: kg | SI unit: N |
| Constant everywhere | Changes with place because $g$ changes |
| Never zero | Zero at the centre of the Earth, or in free space far from all bodies |
| Measured by a beam balance | Measured by a spring balance |

::: example Weight on the Earth and the Moon
**Problem.** A student has a mass of 60 kg. Find the weight on the Earth ($g = 9.8$ m s⁻²) and on the Moon ($g = 1.63$ m s⁻²).

**Solution.**
On Earth: $W = 60 \times 9.8 = 588$ N.

On the Moon: $W = 60 \times 1.63 \approx 98$ N.

The mass is 60 kg at both places. Only the weight changes, to about one sixth.
:::

::: caution kg-weight
In daily life we say "my weight is 60 kg". Strictly, 60 kg is the mass. The weight is 588 N. In exams, always give weight in newtons unless the question asks for kg-wt (1 kg-wt = 9.8 N).
:::

### Weightlessness

A spring balance on which you stand shows a reading equal to the reaction force of the floor. In a freely falling lift, or inside an orbiting spacecraft, you and the floor fall together, so the floor does not push on you. The reading is zero. You *feel* weightless even though gravity still acts on you. Astronauts in the International Space Station float for this reason: they are in constant free fall around the Earth.

## 7.5 Free fall

### Meaning

::: definition Free fall
The motion of a body falling toward the Earth under the action of gravity alone, with no air resistance, is called free fall.
:::

```photo id="sci10/apollo-feather" caption="A feather lying on the lunar surface after astronaut David Scott dropped it together with a hammer during Apollo 15 (1971). With no air to slow it down, the feather fell as fast as the hammer." width="66"
```

In free fall, the acceleration is $g$ for every body, whatever its mass. A coin and a feather fall at the same rate in a vacuum. In air, the feather falls slowly only because of air resistance. Galileo is said to have shown this long ago; astronaut David Scott repeated it on the Moon in 1971 with a hammer and a feather, and both reached the ground together.

### Equations of motion for free fall

The three equations of uniformly accelerated motion with $a$ replaced by $g$:

| Body dropped from rest, falling down ($u = 0$) | Body thrown upward with speed $u$ |
|---|---|
| $v = gt$ | $v = u - gt$ |
| $h = \tfrac12 g t^2$ | $h = ut - \tfrac12 g t^2$ |
| $v^2 = 2gh$ | $v^2 = u^2 - 2gh$ |

For a body thrown upward: at the highest point $v = 0$. Maximum height $H = \dfrac{u^2}{2g}$, time to the top $t = \dfrac{u}{g}$, and the total time of flight $= \dfrac{2u}{g}$. The body returns to the starting point with the same speed $u$ it was thrown with.

For easy calculation SEE questions often use $g = 10$ m s⁻² when the question says so; otherwise use 9.8.

```figure caption="Velocity-time graph for a stone thrown upward at 20 m/s (g = 10 m/s2). It rises for 2 s, stops, then falls back, passing the starting point at 4 s."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6, 2.7))
t = np.linspace(0, 4, 50)
v = 20 - 10*t
ax.plot(t, v, color=ACCENT, lw=2)
ax.axhline(0, color=MUTED, lw=1)
ax.fill_between(t, v, 0, where=(v >= 0), color=ACCENT, alpha=.15)
ax.fill_between(t, v, 0, where=(v <= 0), color='#A8271F', alpha=.15)
ax.text(0.7, 4, 'rising\n(area = 20 m)', fontsize=8.5, color=INK)
ax.text(2.1, -18, 'falling\n(area = 20 m)', fontsize=8.5, color=INK)
ax.set_xlabel('time t (s)'); ax.set_ylabel('velocity v (m/s), up positive')
ax.set_xlim(0, 4); ax.set_ylim(-22, 22)
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.5)
fig.tight_layout()
```

::: example A stone dropped from a height
**Problem.** A stone is dropped from the top of a 45 m high cliff. Taking $g = 10$ m s⁻², find (a) the time it takes to reach the ground and (b) its speed when it hits the ground.

**Solution.** $u = 0$, $h = 45$ m.

(a) $h = \tfrac12 g t^2$, so $45 = 5t^2$, $t^2 = 9$, $t = 3$ s.

(b) $v = gt = 10 \times 3 = 30\ \text{m s}^{-1}$.

Check: $v^2 = 2gh = 2 \times 10 \times 45 = 900$, so $v = 30$ m s⁻¹. ✓
:::

::: example A ball thrown upward
**Problem.** A ball is thrown vertically upward with a speed of 20 m s⁻¹. Take $g = 10$ m s⁻². Find (a) the maximum height reached and (b) the total time it stays in the air.

**Solution.**
(a) At the top $v = 0$. Using $v^2 = u^2 - 2gh$: $0 = 400 - 20h$, so $h = 20$ m.

(b) Time to the top: $t = \dfrac{u}{g} = \dfrac{20}{10} = 2$ s. Total time of flight $= 2 \times 2 = 4$ s.
:::

::: example Depth of a well
**Problem.** A stone dropped into a well takes 2 s to reach the water. How deep is the water surface? ($g = 9.8$ m s⁻².)

**Solution.** $h = \tfrac12 g t^2 = \tfrac12 \times 9.8 \times 2^2 = 19.6$ m.
:::

### Terminal velocity

In air, a falling raindrop or a parachutist feels an upward air resistance that grows with speed. Soon the air resistance equals the weight. The net force is zero, the acceleration is zero, and the body falls at a constant speed called the **terminal velocity**. A parachute greatly increases the air resistance, so the terminal velocity is small and the landing is safe.

## Chapter summary

- Force is a push or a pull; unit newton. Net force zero means the forces are balanced.
- Newton's first law: a body keeps its state of rest or uniform motion unless an unbalanced force acts. Inertia depends on mass.
- Newton's second law: $F = ma$; also $F = \dfrac{\Delta p}{t}$. 1 N gives 1 kg an acceleration of 1 m s⁻².
- Newton's third law: action and reaction are equal and opposite and act on different bodies.
- Momentum $p = mv$ (kg m s⁻¹); impulse $Ft = mv - mu$. Without external force, $m_1u_1 + m_2u_2 = m_1v_1 + m_2v_2$.
- Gravitation: $F = G\dfrac{m_1 m_2}{d^2}$ with $G = 6.67\times10^{-11}$ N m² kg⁻²; $g = \dfrac{GM}{R^2} = 9.8$ m s⁻²; $g$ is greatest at the poles and zero at the Earth's centre.
- Weight $W = mg$ (newton) changes from place to place; mass (kg) does not.
- Free fall: $v = gt$, $h = \tfrac12 gt^2$, $v^2 = 2gh$; for upward throw $H = \dfrac{u^2}{2g}$, time of flight $\dfrac{2u}{g}$.

## Practice questions

**Group A — Objective (1 mark each)**

1. Which of these has the greatest inertia? <span class="marks">[1]</span>
   (a) a cricket ball (b) a cycle (c) a loaded truck (d) a football
2. The SI unit of momentum is <span class="marks">[1]</span>
   (a) N (b) kg m s⁻¹ (c) kg m s⁻² (d) J
3. The value of $g$ at the centre of the Earth is <span class="marks">[1]</span>
   (a) 9.8 m s⁻² (b) 6.67 m s⁻² (c) zero (d) infinite
4. The weight of a body on the Moon compared with the Earth is about <span class="marks">[1]</span>
   (a) 6 times (b) the same (c) one sixth (d) zero
5. If the distance between two masses is doubled, the gravitational force becomes <span class="marks">[1]</span>
   (a) double (b) half (c) one quarter (d) four times

::: note Answers to Group A
**1.** (c) — a loaded truck has the greatest mass.
**2.** (b) — $p = mv$ gives kg m s⁻¹.
**3.** (c) — attractions from all sides cancel at the centre.
**4.** (c) — $g$ on the Moon is about $\tfrac16$ of $g$ on the Earth.
**5.** (c) — $F \propto 1/d^2$, so $F$ becomes $\tfrac14$.
:::

**Group B — Short answer (2 marks each)**

1. Why do passengers fall forward when a moving bus stops suddenly? <span class="marks">[2]</span>
2. State Newton's third law and give one example. <span class="marks">[2]</span>
3. Define momentum. What is its SI unit? <span class="marks">[2]</span>
4. Differentiate between mass and weight (any two points). <span class="marks">[2]</span>
5. Why does a cricketer pull his hands back while catching a fast ball? <span class="marks">[2]</span>

::: note Answers to Group B
**1.** The passengers' bodies are moving with the bus. When the bus stops, the feet stop with the floor, but the upper body keeps moving forward because of inertia of motion.
**2.** To every action there is an equal and opposite reaction. Example: when a gun fires a bullet forward, the bullet pushes the gun backward (recoil).
**3.** Momentum is the product of mass and velocity, $p = mv$. Unit: kg m s⁻¹.
**4.** Mass is the quantity of matter and is measured in kg; weight is the force of gravity on the body and is measured in N. Mass is constant everywhere; weight changes with $g$.
**5.** Pulling back the hands increases the time of stopping the ball. Since $F = \Delta p / t$, a longer time means a smaller force on the hands, so they do not get hurt.
:::

**Group C — Long answer (4 marks each)**

1. A force of 30 N acts on a body of mass 6 kg for 4 s. Starting from rest, find (a) the acceleration, (b) the final velocity and (c) the momentum gained. <span class="marks">[4]</span>
2. A bullet of mass 25 g leaves a rifle of mass 5 kg at 400 m s⁻¹. Calculate the recoil velocity of the rifle. <span class="marks">[4]</span>
3. State Newton's law of gravitation and derive an expression for the acceleration due to gravity on the Earth's surface. <span class="marks">[4]</span>
4. A ball is thrown upward with a velocity of 30 m s⁻¹ ($g = 10$ m s⁻²). Find the maximum height it reaches and the time taken to return to the thrower. <span class="marks">[4]</span>
5. A stone falls freely from rest for 5 s ($g = 9.8$ m s⁻²). Find the distance it falls and its final speed. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** (a) $a = F/m = 30/6 = 5$ m s⁻². (b) $v = u + at = 0 + 5 \times 4 = 20$ m s⁻¹. (c) $p = mv = 6 \times 20 = 120$ kg m s⁻¹ (also $Ft = 30 \times 4 = 120$ N s).
**2.** $m_b = 0.025$ kg. Momentum is conserved: $0 = 0.025 \times 400 + 5 v$, so $v = -10/5 = -2$ m s⁻¹. The rifle recoils at 2 m s⁻¹.
**3.** Law: $F = Gm_1m_2/d^2$ (state in words). Derivation: pull of the Earth on mass $m$ is $GMm/R^2$; this equals $mg$; cancelling $m$ gives $g = GM/R^2$.
**4.** $H = u^2/2g = 900/20 = 45$ m. Time up $= u/g = 3$ s; total time $= 6$ s.
**5.** $h = \tfrac12 g t^2 = \tfrac12 \times 9.8 \times 25 = 122.5$ m. $v = gt = 9.8 \times 5 = 49$ m s⁻¹.
:::
