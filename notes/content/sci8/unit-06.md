---
subject: Science and Technology
grade: 8
unit: 6
title: Force and Motion
hours: 0
area: Science and Technology
---

A bullock cart moves when the bullocks pull it. A football changes direction
when a boot hits it. A bucket of water feels lighter inside a well than on the
ground. All three are questions about **force** — a push or a pull — and about
what force does to motion. This unit takes motion first, then the lever, which
is the oldest machine people ever used, and finally pressure, which explains
everything from a needle to a dam and from a floating boat to a heavy stone
that sinks.

::: key What this unit asks of you
You should be able to define distance, displacement, speed, velocity and
acceleration with their units, read and draw distance-time and velocity-time
graphs, state the three classes of lever with an example of each and calculate
mechanical advantage, calculate pressure in solids and liquids, and explain
atmospheric pressure, upthrust, Archimedes' principle and floatation.
:::

## 6.1 Motion

An object is said to be in **motion** if its position changes with time
compared with its surroundings.

**Distance** is the total length of the path travelled; it has size but no
direction. **Displacement** is the straight-line distance from the starting
point to the finishing point, together with the direction.

::: example Distance and displacement in one journey
**Problem.** A girl walks 30 m east along a straight road, then turns and walks
40 m north. Find (a) the distance she walked, and (b) her displacement.

**Solution.** (a) Distance is the whole path:
$30+40=70$ m.

(b) The displacement is the straight line from the start to the end. The two
parts are at right angles, so use Pythagoras:
$\sqrt{30^2+40^2}=\sqrt{900+1600}=\sqrt{2500}=50$ m, directed north-east.

**Answer.** Distance 70 m; displacement 50 m towards the north-east.

**What it shows.** Distance can never be smaller than displacement, and it is
usually larger. If she had walked 30 m east and then 30 m back, the distance
would be 60 m but the displacement would be zero.
:::

### 6.1.1 Speed, velocity and acceleration

$$\text{speed}=\frac{\text{distance travelled}}{\text{time taken}},
\qquad \text{velocity}=\frac{\text{displacement}}{\text{time taken}}$$

Speed is a scalar (size only); velocity is a vector (size and direction). The
SI unit of both is the metre per second, m/s.

**Acceleration** is the rate of change of velocity:

$$a=\frac{v-u}{t}$$

where $u$ is the initial velocity, $v$ the final velocity and $t$ the time
taken. Its unit is m/s². A negative acceleration means the object is slowing
down; it is called retardation or deceleration.

| Kind of motion | Speed | Acceleration | Example |
|---|---|---|---|
| Uniform velocity | constant, same direction | zero | a train at steady speed on a straight track |
| Uniform acceleration | increases by the same amount each second | constant, positive | a stone falling |
| Retardation | decreases | constant, negative | a bus braking |

::: caution Speed and velocity are not the same word
A bus going round and round a circular park at 30 km/h has a constant *speed*
but a changing *velocity*, because its direction keeps changing — and a change
in velocity is an acceleration. This is why a body moving in a circle at steady
speed is still accelerating.
:::

### 6.1.2 Graphs of motion

```figure caption="Two graphs of the same journey. The distance-time graph flattens where the object stands still; the velocity-time graph drops to zero at the same moment."
import numpy as np
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(5.1, 2.6))
t = np.array([0, 2, 4, 6, 8, 10])
d = np.array([0, 8, 16, 16, 16, 26])
ax1.plot(t, d, "-o", color=ACCENT, lw=1.5, ms=3.5)
ax1.set_xlabel("time (s)", fontsize=8)
ax1.set_ylabel("distance (m)", fontsize=8)
ax1.set_title("distance-time", fontsize=8.5, color=INK)
v = np.array([4, 4, 4, 0, 0, 5])
ax2.step(t, v, where="post", color=SERIES[1], lw=1.5)
ax2.set_xlabel("time (s)", fontsize=8)
ax2.set_ylabel("velocity (m/s)", fontsize=8)
ax2.set_title("velocity-time", fontsize=8.5, color=INK)
for ax in (ax1, ax2):
    ax.tick_params(labelsize=7.5, length=0)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(True, color=GRID, lw=0.5)
    ax.set_axisbelow(True)
fig.tight_layout()
```

| On a distance-time graph | What it means |
|---|---|
| horizontal line | the object is not moving |
| straight sloping line | steady speed; a steeper slope means a greater speed |
| curve getting steeper | the object is accelerating |

| On a velocity-time graph | What it means |
|---|---|
| horizontal line | constant velocity; the area under it is the distance |
| line sloping up | acceleration; the slope is the acceleration |
| line sloping down to zero | retardation |

**Slope of a distance-time graph** $=\frac{\text{change in distance}}{\text{change in time}}=$ speed.

::: example Reading a distance-time graph
**Problem.** On the graph above, find the speed between 0 s and 4 s, and
describe what happens between 4 s and 8 s.

**Solution.** Between 0 s and 4 s the distance changes from 0 m to 16 m, so

$$\text{speed}=\frac{16-0}{4-0}=4\ \text{m/s}$$

Between 4 s and 8 s the distance stays at 16 m, so the change is zero and the
speed is zero: the object is standing still. The graph is horizontal for those
four seconds, which is exactly what a stationary object gives.

**Answer.** 4 m/s; the object is at rest from 4 s to 8 s.
:::

### 6.1.3 Force and its effects

A **force** is a push or a pull that changes, or tends to change, the state of
rest or of motion of a body, or its shape. Force is measured in **newtons (N)**.

A force can: (1) start a body moving; (2) stop a moving body; (3) change its
speed; (4) change its direction; (5) change its shape or size.

| Force | What it is |
|---|---|
| Muscular force | exerted by the muscles of a person or animal |
| Gravitational force | the pull of the earth on every object |
| Magnetic force | the pull or push of a magnet on iron |
| Electrostatic force | the push or pull between electric charges |
| Frictional force | opposes motion between two surfaces in contact |
| Buoyant force | the upward push of a liquid or gas |

### 6.1.4 Newton's laws of motion

**First law (law of inertia).** A body at rest stays at rest and a body in
uniform motion keeps moving in a straight line unless an external force acts on
it. This is why a passenger falls forward when a bus brakes suddenly, and
backward when it starts suddenly. The tendency of a body to resist a change in
its state is called **inertia**.

**Second law.** The acceleration produced is directly proportional to the force
and inversely proportional to the mass: $F=ma$ for a constant mass. A cricket
ball and a football hit with the same force accelerate differently, because
their masses are different.

**Third law.** To every action there is an equal and opposite reaction. A
swimmer pushes the water backward, and the water pushes the swimmer forward. A
rocket pushes gas downward and the gas pushes the rocket upward.

::: tip Inertia in a Nepali bus
When the bus stops suddenly, your body keeps moving forward because of inertia,
and you fall towards the front. The driver's remedy is not to brake all at once
but to slow down gradually, and your remedy is to hold the bar rather than rely
on your legs. A heavy loaded truck has more inertia than a bicycle, which is why
it takes much longer to stop.
:::

## 6.2 Lever

A **simple machine** is a device that makes work easier by changing the size or
direction of a force. The lever is one of the six simple machines.

A lever is a rigid bar that turns about a fixed point called the **fulcrum**.
The force we apply is the **effort** and the force we overcome is the **load**.

| Class | Position of the fulcrum | Examples |
|---|---|---|
| First | between the load and the effort | seesaw, scissors, pliers, beam balance, crowbar |
| Second | at one end, with the load between the fulcrum and the effort | wheelbarrow, nutcracker, bottle opener |
| Third | at one end, with the effort between the fulcrum and the load | fishing rod, broom, tongs (*chimta*), human forearm |

```figure caption="The three classes of lever. The class is decided by one question only: what sits between the other two?"
fig, ax = plt.subplots(figsize=(5.1, 2.9))
ax.set_xlim(0, 10)
ax.set_ylim(0, 6.4)
ax.axis("off")
rows = [("First class", 5.4, "F", 4.6, "load", 1.2, "effort", 8.6),
        ("Second class", 3.4, "F", 0.9, "load", 4.6, "effort", 8.6),
        ("Third class", 1.4, "F", 0.9, "load", 8.6, "effort", 4.6)]
for name, y, fname, fx, lname, lx, ename, ex in rows:
    ax.plot([0.6, 9.4], [y, y], color=INK, lw=2.2)
    ax.plot([fx], [y], "v", color=SERIES[2], ms=8)
    ax.text(fx, y - 0.55, "fulcrum", ha="center", fontsize=6.3, color=SERIES[2])
    ax.annotate("", xy=(lx, y + 0.05), xytext=(lx, y + 0.85),
                arrowprops=dict(arrowstyle="->", color=SERIES[1], lw=1.3))
    ax.text(lx, y + 1.05, lname, ha="center", fontsize=6.5, color=SERIES[1])
    ax.annotate("", xy=(ex, y + 0.05), xytext=(ex, y + 0.85),
                arrowprops=dict(arrowstyle="->", color=ACCENT, lw=1.3))
    ax.text(ex, y + 1.05, ename, ha="center", fontsize=6.5, color=ACCENT)
    ax.text(0.15, y + 0.95, name, ha="left", fontsize=6.9, color=INK)
ax.text(5.0, 0.35, "first: F between;  second: load between;  third: effort between",
        ha="center", fontsize=6.5, color=MUTED)
fig.tight_layout()
```

### 6.2.1 Principle of moments

The turning effect of a force about a point is called its **moment**, and

$$\text{moment}=\text{force}\times\text{perpendicular distance from the fulcrum}$$

**Principle of moments.** When a lever is balanced, the total clockwise moment
equals the total anticlockwise moment.

**Mechanical advantage (MA)** tells how many times the machine multiplies the
force:

$$\text{MA}=\frac{\text{load}}{\text{effort}}$$

::: example A balanced metre scale
**Problem.** A metre scale is balanced at its centre. A load of 20 N is hung
15 cm from the fulcrum on the left. How far from the fulcrum must an effort of
12 N be applied on the right to balance it?

**Solution.** By the principle of moments,

$$\text{load}\times\text{load arm}=\text{effort}\times\text{effort arm}$$

$$20\times15=12\times d\;\Longrightarrow\;300=12d\;\Longrightarrow\;d=25\ \text{cm}$$

**Answer.** 25 cm from the fulcrum on the right.

**Check.** $12\times25=300$, which equals $20\times15$. Balanced.
:::

::: example Mechanical advantage of a crowbar
**Problem.** A crowbar is used to lift a stone of weight 600 N. The effort
applied is 150 N. Find the mechanical advantage, and say what it means.

**Solution.**

$$\text{MA}=\frac{\text{load}}{\text{effort}}=\frac{600}{150}=4$$

**Meaning.** The crowbar multiplies the applied force four times: every 1 N of
effort lifts 4 N of load. A machine with a mechanical advantage greater than 1
makes the work easier to do, though the effort still has to move further than
the load does.

**Note.** MA has no unit, because it is a ratio of two forces.
:::

## 6.3 Pressure

**Pressure** is the force acting normally (at right angles) on unit area:

$$P=\frac{F}{A}$$

Its SI unit is the pascal (Pa), where 1 Pa = 1 N/m². The same force gives more
pressure on a smaller area — which is why a nail is sharp at the point and broad
at the head, and why a camel's wide foot does not sink into sand.

### 6.3.1 Pressure in solids, liquids and gases

| | How pressure behaves | Example |
|---|---|---|
| Solids | depends on the weight and on the area of contact; a smaller area gives greater pressure | sharp knife cuts better than a blunt one |
| Liquids | increases with depth and with the density of the liquid; acts equally in all directions at the same depth | a dam wall is made thicker at the bottom |
| Gases | a gas fills its container and exerts pressure on the walls in all directions | pumping air into a football |

For a liquid of density $d$ at depth $h$:

$$P=h\,d\,g$$

where $g$ is the acceleration due to gravity, about 9.8 m/s².

::: caution Pressure is not force
A heavy tractor with wide wheels and a needle pressed by a finger may exert the
same force, but the needle exerts enormously greater pressure because its area
is tiny. Whenever a question mentions pressure, look for **both** the force and
the area.
:::

### 6.3.2 Atmospheric pressure

The layer of air around the earth has weight, and it presses on everything at
the surface. This is **atmospheric pressure**. At sea level it is about
101,325 Pa, which is why it is also called one atmosphere (1 atm). It falls as
you go higher, because there is less air above you.

Atmospheric pressure explains drinking with a straw: you lower the pressure
inside the straw, and the atmosphere pushes the liquid up. It also explains why
a syringe fills: pulling the plunger creates low pressure inside, and the
atmospheric pressure pushes the liquid in.

### 6.3.3 Upthrust, Archimedes' principle and floatation

Anything put into a liquid feels an upward push called **upthrust** or buoyant
force. It is caused by the fact that pressure in a liquid is greater at a
greater depth, so the upward push on the bottom of the object is larger than the
downward push on its top.

**Archimedes' principle.** When a body is wholly or partly immersed in a fluid,
it experiences an upthrust equal to the weight of the fluid displaced.

$$F_{\text{upthrust}}=V\,d\,g$$

where $V$ is the volume of fluid displaced, $d$ its density and $g$ the
acceleration due to gravity.

| Condition | What happens | Example |
|---|---|---|
| weight of body $>$ upthrust | the body sinks | iron nail, stone |
| weight of body $=$ upthrust | the body floats wholly inside | a fish suspended in water |
| weight of body $<$ upthrust | the body floats partly out | wooden log, boat, ice |

A ship floats although it is made of iron because its hollow shape makes it
displace a great volume of water, so the upthrust is large enough to hold its
weight. A submarine changes its weight by taking water into or blowing water out
of its ballast tanks.

```figure caption="Why the pressure rises with depth, and why the bottom of a dam is thick. The water above pushes down on the water below, so each layer carries the weight of all the layers above it."
fig, ax = plt.subplots(figsize=(4.9, 2.8))
ax.set_xlim(0, 10)
ax.set_ylim(0, 6)
ax.axis("off")
ax.add_patch(plt.Rectangle((1.0, 0.8), 5.4, 4.4, fc=ACCENT, alpha=0.18,
                           ec=ACCENT, lw=1.1))
for x, y, l in [(2.2, 4.6, "1 m"), (3.4, 3.4, "2 m"), (4.6, 2.2, "3 m"), (5.8, 1.2, "4 m")]:
    ax.text(x, y, l, ha="center", va="center", fontsize=6.4, color=INK)
for y, n in [(4.4, 1), (3.2, 2), (2.0, 3), (1.0, 4)]:
    ax.annotate("", xy=(0.55, y), xytext=(0.55, y + 0.5 + n * 0.12),
                arrowprops=dict(arrowstyle="->", color=SERIES[1], lw=0.9 + 0.25 * n))
ax.text(0.35, 5.5, "pressure", ha="left", fontsize=6.6, color=SERIES[1])
ax.plot([6.4, 6.4, 7.0, 7.0], [0.8, 5.2, 4.4, 0.0], color=INK, lw=2.4)
ax.text(7.3, 3.0, "dam wall:\\nthick at the bottom", ha="left", fontsize=6.5, color=INK)
fig.tight_layout()
```

::: example Upthrust on a stone
**Problem.** A stone of volume 200 cm³ is fully immersed in water. Find the
upthrust on it. (Density of water $=1000$ kg/m³, $g=9.8$ m/s².)

**Solution.** Convert the volume to SI: $200\ \text{cm}^3=200\times10^{-6}\
\text{m}^3=2\times10^{-4}$ m³.

$$F=Vdg=2\times10^{-4}\times1000\times9.8=1.96\ \text{N}$$

**Answer.** The upthrust is 1.96 N, directed vertically upward.

**What it means.** If the stone's weight is more than 1.96 N it sinks; the
effect of the upthrust is to make it feel lighter by 1.96 N — that is, its
apparent weight is its real weight minus the upthrust.
:::

::: example Pressure on the ground
**Problem.** A box weighing 300 N stands on a face of area 0.5 m². Find the
pressure. What happens to the pressure if the box is turned so that the contact
area becomes 0.25 m²?

**Solution.** With $A=0.5$ m²:

$$P=\frac{F}{A}=\frac{300}{0.5}=600\ \text{Pa}$$

With $A=0.25$ m²:

$$P=\frac{300}{0.25}=1200\ \text{Pa}$$

**Answer.** 600 Pa, then 1200 Pa — halving the area doubles the pressure.

**What it means.** The weight has not changed at all. Only the area of contact
changed, and the pressure changed with it. This is the whole reason for wide
foundations under buildings and wide tyres on tractors.
:::

## Chapter summary

- **Distance** is the path length; **displacement** is the straight line from
  start to finish with its direction.
- $\text{speed}=\frac{\text{distance}}{\text{time}}$,
  $a=\frac{v-u}{t}$; speed is a scalar, velocity a vector.
- On a distance-time graph the slope gives speed; on a velocity-time graph the
  slope gives acceleration and the area gives the distance.
- A **force** is a push or a pull, measured in newtons; it can start, stop,
  speed up, slow down, turn or deform a body.
- **Newton's laws**: inertia; $F=ma$; every action has an equal and opposite
  reaction.
- A **lever** turns about a fulcrum; the three classes differ by which of
  fulcrum, load and effort lies in the middle.
- **Principle of moments**: load × load arm = effort × effort arm.
  **Mechanical advantage** = load ÷ effort, and has no unit.
- $P=\frac{F}{A}$ in solids; in liquids $P=hdg$, and pressure rises with depth.
- **Atmospheric pressure** at sea level is about 101,325 Pa; a straw and a
  syringe work because of it.
- **Archimedes' principle**: upthrust equals the weight of fluid displaced,
  $F=Vdg$. A body floats if the upthrust equals its weight.

## Practice questions

**Group A — Objective (1 mark each)**

1. The SI unit of force is the <span class="marks">[1]</span>
   (a) joule (b) newton (c) pascal (d) watt
2. A body moving in a circle at constant speed has
   <span class="marks">[1]</span>
   (a) zero acceleration (b) changing velocity (c) zero speed (d) no force
3. The fulcrum of a wheelbarrow lies <span class="marks">[1]</span>
   (a) between the load and the effort (b) at one end, with the load in the
   middle (c) at one end, with the effort in the middle (d) at the centre of
   the wheel
4. The pressure of a liquid at depth $h$ is given by
   <span class="marks">[1]</span>
   (a) $hd$ (b) $hdg$ (c) $hg$ (d) $\frac{d}{hg}$
5. A body floats when <span class="marks">[1]</span>
   (a) its weight is greater than the upthrust (b) its weight equals the
   upthrust (c) there is no upthrust (d) its density is greater than water
6. Pressure is measured in <span class="marks">[1]</span>
   (a) newton (b) pascal (c) joule (d) metre

::: note Answers to Group A
**1.** (b) — the newton, named after Isaac Newton.
**2.** (b) — the direction changes, so the velocity changes and there is an
acceleration towards the centre.
**3.** (b) — the load is between the fulcrum and the effort: second class.
**4.** (b) — pressure $=h\,d\,g$.
**5.** (b) — floating means the upthrust exactly balances the weight.
**6.** (b) — 1 pascal is 1 newton per square metre.
:::

**Group B — Short answer (2 marks each)**

1. Distinguish between speed and velocity with one example.
   <span class="marks">[2]</span>
2. State Newton's first law of motion and give one example from daily life.
   <span class="marks">[2]</span>
3. Name the three classes of lever and give one example of each.
   <span class="marks">[2]</span>
4. Why is a dam wall thicker at the bottom than at the top?
   <span class="marks">[2]</span>

::: note Answers to Group B
**1.** Speed is the distance travelled per unit time and has size only; velocity
is the displacement per unit time and has both size and direction. Example: a
bus going round a circular park at a steady 30 km/h has constant speed but
constantly changing velocity, because its direction keeps changing.
**2.** A body at rest remains at rest and a body in uniform motion continues in
a straight line with the same velocity unless an external force acts on it.
Example: a passenger standing in a bus falls forward when the driver brakes
suddenly, because the passenger's body tends to keep moving while the bus stops.
**3.** First class — fulcrum in the middle: seesaw or scissors. Second class —
load in the middle: wheelbarrow or nutcracker. Third class — effort in the
middle: fishing rod or tongs.
**4.** The pressure of a liquid increases with depth, $P=hdg$. The water at the
bottom of a full reservoir presses with the weight of all the water above it, so
the wall must be stronger and thicker there; at the top there is little water
above, so the wall can be thin.
:::

**Group C — Long answer (4 marks each)**

1. A car starts from rest and reaches a velocity of 20 m/s in 8 s. Find
   (i) its acceleration, (ii) the distance it travels in that time, assuming
   uniform acceleration. Also draw the shape of its velocity-time graph and say
   what the area under the graph means. <span class="marks">[4]</span>
2. State Archimedes' principle. Explain, using it, why an iron nail sinks in
   water but a ship made of iron floats, and find the upthrust on a body of
   volume 500 cm³ fully immersed in water
   ($d=1000$ kg/m³, $g=9.8$ m/s²). <span class="marks">[4]</span>

::: note Answers to Group C
**1.** (i) $a=\frac{v-u}{t}=\frac{20-0}{8}=2.5$ m/s². (ii) For uniform
acceleration the average velocity is $\frac{u+v}{2}=\frac{0+20}{2}=10$ m/s, so
the distance is $10\times8=80$ m. (Alternatively use
$s=ut+\frac12at^2=0+\frac12(2.5)(64)=80$ m.) **Graph.** The velocity-time graph
is a straight line rising from the origin to the point (8 s, 20 m/s); its slope
is the acceleration, 2.5 m/s². The area under the line is
$\frac12\times8\times20=80$, which is the distance travelled in metres.
**2.** **Archimedes' principle.** When a body is wholly or partly immersed in a
fluid, it experiences an upthrust equal to the weight of the fluid displaced.
**Why the nail sinks.** An iron nail is solid, so it displaces only its own
small volume of water; the upthrust is much less than the nail's weight, so the
resultant force is downwards and it sinks. **Why a ship floats.** A ship is
hollow, so although its weight is enormous its hull displaces a very large
volume of water. The upthrust — the weight of all that displaced water — is made
equal to the ship's weight, and the ship floats. **Calculation.**
$V=500\ \text{cm}^3=500\times10^{-6}=5\times10^{-4}$ m³;
$F=Vdg=5\times10^{-4}\times1000\times9.8=4.9$ N.
:::
