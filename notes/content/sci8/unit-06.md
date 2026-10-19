---
subject: Science and Technology
grade: 8
unit: 6
title: Force and Motion
hours: 0
area: Science and Technology
---

Every object in the universe is either at rest or in motion. To decide which, we
compare it with a **reference point** — a point, place or object that we treat as
fixed. A force is needed to make a body at rest start moving, or to stop a moving
body. In this unit we measure motion (speed, velocity, relative velocity, average
velocity and acceleration), read motion graphs, study forces and Newton's laws,
learn how a lever makes work easy, and study pressure in solids, liquids and
gases, including upthrust and floating.

::: key What this unit asks of you
Use the formulas $v=\frac{s}{t}$, $a=\frac{v-u}{t}$, average velocity
$=\frac{u+v}{2}$, relative velocity $v_A-v_B$ or $v_A+v_B$; $E\times E.D.=L\times L.D.$,
$MA=\frac{L}{E}$, $VR=\frac{E.D.}{L.D.}$, $\eta=\frac{MA}{VR}\times100\%$; $P=\frac{F}{A}$ and
$P=hdg$. Always write the data, the formula, the substitution with units, and the
answer with its unit.
:::

## 6.1 Motion: distance, displacement, speed, velocity and acceleration

An object is in **motion** if it changes its position with respect to a reference
point or its surroundings (a flying aeroplane, a rolling ball). It is at **rest** if
it does not change its position (houses, trees, a parked bus). Rest and motion are
**relative**: a passenger sitting in a moving bus is at rest with respect to the bus
but in motion with respect to the trees outside.

**Uniform motion:** equal distances in equal intervals of time. **Non-uniform
motion:** unequal distances in equal intervals of time.

| Distance | Displacement |
|---|---|
| total length of the path travelled | shortest distance between the start and end points in a particular direction |
| has magnitude only (scalar) | has magnitude and direction (vector) |
| never zero once a body has moved | can be zero (a runner who returns to the start) |

### 6.1.1 Speed and velocity

::: definition Speed and velocity
**Speed** is the distance travelled by a body in unit time: $S=\frac{d}{t}$.
**Velocity** is the distance travelled in unit time in a particular direction (the
rate of change of displacement): $v=\frac{s}{t}$. The SI unit of both is **m/s**.
Speed is a scalar; velocity is a vector.
:::

A speed of 20 m/s means 20 m is covered every second. The speed of sound in air
is about 332 m/s. To change km/h into m/s, multiply by $\frac{1000}{3600}=\frac{5}{18}$.

### 6.1.2 Relative velocity

The **relative velocity** of a body is its velocity with respect to another body
(or reference point).

| Case | Relative velocity of A with respect to B | What passengers feel |
|---|---|---|
| same direction, same speed | $v_{AB}=v_A-v_B=0$ | the other bus seems to be at rest |
| same direction, different speeds | $v_{AB}=v_A-v_B$ | the other bus seems slow |
| opposite directions | $v_{AB}=v_A+v_B$ | the other bus seems very fast |

::: example Relative velocity of two buses (textbook example)
**Problem.** Buses A and B move in the same direction at 15 m/s and 10 m/s. Find the
velocity of A relative to B. What is it if they move in opposite directions?

**Solution.** $v_A=15$ m/s, $v_B=10$ m/s.
Same direction: $v_{AB}=v_A-v_B=15-10=5$ m/s.
Opposite directions: $v_{AB}=v_A+v_B=15+10=25$ m/s.
:::

### 6.1.3 Average velocity

In non-uniform motion the velocity keeps changing, so we use the **average
velocity**: the total displacement divided by the total time,

$$\bar{v}=\frac{\text{total displacement}}{\text{total time}}$$

If the velocity changes steadily from $u$ (initial) to $v$ (final),
$\bar{v}=\frac{u+v}{2}$.

::: example Average velocity
**Problem.** A body covers 10 m in 3 s and then 17 m in 6 s in the same direction.
Find its average velocity.

**Solution.** $\bar{v}=\frac{10+17}{3+6}=\frac{27\ \text{m}}{9\ \text{s}}=3$ m/s.
:::

### 6.1.4 Acceleration and retardation

::: definition Acceleration
**Acceleration** is the change in velocity of a body in unit time (the rate of
change of velocity): $a=\frac{v-u}{t}$. Its SI unit is **m/s²**. A body in uniform
velocity has zero acceleration. When the velocity decreases ($v<u$), the
acceleration is negative; negative acceleration is called **retardation**
(deceleration).
:::

A body starting from rest has $u=0$; a body that stops has $v=0$.

::: example Acceleration and retardation of a bus
**Problem (a).** A bus starts from rest and reaches 25 m/s in 10 s. Find its
acceleration.
**Solution.** $u=0$, $v=25$ m/s, $t=10$ s.
$a=\frac{v-u}{t}=\frac{25-0}{10}=2.5$ m/s².

**Problem (b).** A bus moving at 20 m/s stops in 4 s. Find its retardation.
**Solution.** $u=20$ m/s, $v=0$, $t=4$ s.
$a=\frac{0-20}{4}=-5$ m/s², so the retardation is **5 m/s²**.
:::

| Acceleration | Retardation |
|---|---|
| velocity increases ($v>u$) | velocity decreases ($v<u$) |
| positive value | negative acceleration |
| e.g. a bus starting from the bus park | e.g. a bus braking at a stop |

## 6.2 Distance-time and velocity-time graphs

```figure caption="Graphs of one journey: steady motion for 4 s, rest from 4 s to 8 s, then faster steady motion."
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(5.1, 2.6))
t = np.array([0, 2, 4, 6, 8, 10])
d = np.array([0, 8, 16, 16, 16, 26])
ax1.plot(t, d, "-o", color=ACCENT, lw=1.5, ms=3.5)
ax1.set_xlabel("time (s)", fontsize=8)
ax1.set_ylabel("distance (m)", fontsize=8)
ax1.set_title("distance-time", fontsize=8.5, color=INK)
v = np.array([4, 4, 0, 0, 5, 5])
ax2.step(t, v, where="post", color=SERIES[1], lw=1.5)
ax2.set_xlabel("time (s)", fontsize=8)
ax2.set_ylabel("velocity (m/s)", fontsize=8)
ax2.set_title("velocity-time", fontsize=8.5, color=INK)
ax2.set_ylim(0, 6)
ax2.set_yticks([0, 2, 4, 6])
ax1.set_yticks([0, 10, 20, 30])
for a in (ax1, ax2):
    a.set_xticks([0, 2, 4, 6, 8, 10])
for ax in (ax1, ax2):
    ax.tick_params(labelsize=7.5, length=0)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(True, color=GRID, lw=0.5)
    ax.set_axisbelow(True)
fig.tight_layout()
```

| On a distance-time graph | Meaning |
|---|---|
| horizontal line | body at rest |
| straight sloping line | uniform speed; steeper line = greater speed; slope = speed |
| curve becoming steeper | accelerating |

| On a velocity-time graph | Meaning |
|---|---|
| horizontal line | uniform velocity; area under the line = distance |
| line sloping up | acceleration; slope = acceleration |
| line sloping down | retardation |

::: example Reading the graphs
**Problem.** From the graphs, find the speed from 0 to 4 s and from 8 to 10 s, and the
total distance.

**Solution.** 0–4 s: speed $=\frac{16-0}{4-0}=4$ m/s. 4–8 s: the line is flat, so the
body is at rest. 8–10 s: speed $=\frac{26-16}{10-8}=5$ m/s. Total distance = 26 m
(check from the v–t graph: area $=4\times4+0+5\times2=26$ m).
:::

## 6.3 Force and its effects; balanced and unbalanced forces

A **force** is a push or pull that changes or tends to change the state of rest or
motion of a body, or its shape. Its SI unit is the **newton (N)**. On the earth, the
weight of a 1 kg mass is about 10 N (more exactly 9.8 N).

**Effects of force:** it can (1) move a body at rest, (2) stop a moving body,
(3) change its speed, (4) change its direction, (5) change its shape or size.

**Balanced forces** are forces on a body whose resultant is zero: the body stays at
rest or keeps moving uniformly (e.g. equal teams in a tug of war, a book on a table).
**Unbalanced forces** have a non-zero resultant and change the motion (one team pulls
harder; a kicked football).

## 6.4 Newton's laws of motion in everyday examples

**First law (law of inertia).** A body at rest remains at rest, and a body in uniform
motion keeps moving in a straight line, unless an external unbalanced force acts on
it. The property of a body to resist a change in its state is **inertia**; more mass
means more inertia. *Examples:* passengers fall forward when a bus stops suddenly and
backward when it starts suddenly; dust leaves a carpet when it is beaten.

**Second law.** The acceleration of a body is directly proportional to the applied
force and inversely proportional to its mass: $F=ma$. *Example:* the same push gives an
empty cart more acceleration than a loaded one. A force of 1 N gives a 1 kg mass an
acceleration of 1 m/s².

**Third law.** To every action there is an equal and opposite reaction. *Examples:* a
swimmer pushes water back and moves forward; a rocket pushes hot gases down and goes up;
a gun recoils when fired.

::: example Using F = ma
**Problem.** A force of 600 N acts on a motorcycle of mass 150 kg. Find its acceleration.

**Solution.** $a=\frac{F}{m}=\frac{600\ \text{N}}{150\ \text{kg}}=4$ m/s².
:::

```photo id="sci10/apollo-feather" caption="On the Moon, where there is no air, a feather and a hammer dropped together reach the ground together: gravity gives all bodies the same acceleration." width="62"
```

## 6.5 Lever: classes, principle of moments and mechanical advantage

::: definition Lever
A **lever** is a rigid bar that can turn about a fixed point called the
**fulcrum (F)**. The force applied is the **effort (E)**; the body lifted is the
**load (L)**. The distance from fulcrum to load is the **load distance (L.D.)**; from
fulcrum to effort, the **effort distance (E.D.)**.
:::

Archimedes is said to have claimed: "Give me a lever and a place to stand, and I can
move the world."

### 6.5.1 Classes of lever

```figure caption="The three classes of lever. The class depends on which of fulcrum (F), load (L) and effort (E) is in the middle."
fig, ax = plt.subplots(figsize=(5.2, 2.3))
ax.set_xlim(0, 3.15); ax.set_ylim(-0.8, 0.8); ax.axis("off")
cases = [("First class: F in middle", ["L", "F", "E"], "dhiki, scissors,\nbeam balance"),
         ("Second class: L in middle", ["F", "L", "E"], "nutcracker,\nwheelbarrow"),
         ("Third class: E in middle", ["F", "E", "L"], "fire tongs,\nshovel, hammer")]
for k, (title, labels, ex) in enumerate(cases):
    o = k * 1.07
    ax.plot([o + 0.05, o + 0.95], [0, 0], color=INK, lw=3)
    for x, l in zip([o + 0.1, o + 0.5, o + 0.9], labels):
        if l == "F":
            ax.add_patch(plt.Polygon([[x - 0.06, -0.22], [x + 0.06, -0.22], [x, 0]], fc=MUTED, ec=INK))
            ax.text(x, -0.36, "F", ha="center", va="center", fontsize=8, color=INK)
        elif l == "L":
            ax.add_patch(plt.Rectangle((x - 0.05, 0.02), 0.1, 0.14, fc=SERIES[3], ec=INK))
            ax.text(x, 0.3, "L", ha="center", va="center", fontsize=8, color=INK)
        else:
            ax.annotate("", xy=(x, 0.03), xytext=(x, 0.3), arrowprops=dict(arrowstyle="->", color=SERIES[1], lw=1.4))
            ax.text(x, 0.42, "E", ha="center", va="center", fontsize=8, color=SERIES[1])
    ax.text(o + 0.5, 0.68, title, ha="center", fontsize=7.2, color=INK)
    ax.text(o + 0.5, -0.62, ex, ha="center", va="center", fontsize=7.0, color=MUTED)
fig.tight_layout()
```

| Class | Arrangement | Examples |
|---|---|---|
| First | fulcrum between load and effort | *dhiki*, scissors, beam balance, crowbar, see-saw |
| Second | load between fulcrum and effort | nutcracker, lemon squeezer, wheelbarrow |
| Third | effort between fulcrum and load | fire tongs, shovel, hammer |

### 6.5.2 Principle of lever (principle of moments)

Hang masses on both sides of a metre scale balanced at its middle (Activity 6.3). The
scale balances whenever

$$E\times E.D.=L\times L.D.$$

So **the longer the effort distance, the smaller the effort needed**.

::: example Effort on a crowbar (textbook example)
**Problem.** A load of 800 N is lifted with a crowbar. The load distance is 50 cm and
the effort distance is 1.5 m. Find the effort.

**Solution.** $L=800$ N, $L.D.=50$ cm $=0.5$ m, $E.D.=1.5$ m.
$E\times1.5=800\times0.5$, so $E=\frac{400}{1.5}=266.67$ N.
:::

### 6.5.3 Mechanical advantage, velocity ratio and efficiency

- **Mechanical advantage (MA)** $=\frac{\text{load}}{\text{effort}}=\frac{L}{E}$. MA = 4
  means the machine lifts a load 4 times the effort. It has no unit and is
  **reduced by friction**.
- **Velocity ratio (VR)** $=\frac{\text{distance moved by effort}}{\text{distance moved by load}}=\frac{E.D.}{L.D.}$.
  It has no unit and is **not affected by friction**.
- **Input work** = effort × effort distance; **output work** = load × load distance.
- **Efficiency** $\eta=\frac{\text{output work}}{\text{input work}}\times100\%=\frac{MA}{VR}\times100\%$.

Because of friction, some input work is wasted, so MA < VR and the efficiency of a real
machine is **always less than 100 %**. A machine with 100 % efficiency is an imaginary
**ideal machine**.

::: example MA, VR and efficiency (textbook example)
**Problem.** An effort of 150 N lifts a load of 600 N. The effort moves 7.5 m and the
load moves 1.5 m. Find MA, VR and efficiency.

**Solution.**
$MA=\frac{L}{E}=\frac{600}{150}=4$; $VR=\frac{7.5}{1.5}=5$;
$\eta=\frac{4}{5}\times100\%=80\%$.
:::

::: caution Units in the lever formula
Both distances must be in the same unit (both cm or both m). Mixing 50 cm with 1.5 m
without converting gives a wrong answer.
:::

## 6.6 Pressure in solids, liquids and gases; atmospheric pressure

A pen pressed on the wrist with its pointed end hurts more than with its blunt end; a
brick standing on its narrow face sinks deeper into foam. The same force has a bigger
effect on a smaller area.

::: definition Pressure
**Pressure** is the force acting perpendicularly on unit area: $P=\frac{F}{A}$. Its SI
unit is **N/m²**, called the **pascal (Pa)**. One pascal is the pressure produced by a
force of 1 N acting perpendicularly on 1 m².
:::

::: example Pressure of a cupboard (textbook example)
**Problem.** A cupboard of weight 1800 N stands on 1.5 m². Find the pressure. What is it
if the area is 3 m²?

**Solution.** $P=\frac{1800}{1.5}=1200$ Pa. With 3 m²: $P=\frac{1800}{3}=600$ Pa.
Doubling the area halves the pressure.
:::

**Increasing pressure:** sharp ploughshare, knife, sickle and nail tips (small area).
**Reducing pressure:** wide foundations of houses, broad back wheels of tractors, double
tyres on buses and trucks, broad feet of camels, wide straps on school bags.

### 6.6.1 Pressure in liquids

Water squirts farthest from the lowest hole of a bottle (Activity 6.6): liquid pressure
**increases with depth**. A liquid presses **in all directions**.

::: derivation Pressure at the bottom of a liquid column: P = hdg
We find the pressure due to a liquid column of height $h$ and density $d$.

**Setting up.** A container of cross-section area $A$ holds liquid to height $h$; $g$ is
the acceleration due to gravity.

**Step 1 — volume of liquid.** $V=A\times h$.

**Step 2 — mass of liquid.** $m=d\times V=d\times A\times h$.

**Step 3 — weight of liquid (the force on the bottom).** $F=mg=A\,h\,d\,g$.

**Step 4 — pressure = force ÷ area.** $P=\frac{A\,h\,d\,g}{A}$.

**Result.** $P=hdg$.

**What it means.** Liquid pressure depends on depth $h$, density $d$ and $g$ — not on the
shape of the container or the amount of liquid.
:::

::: example Pressure in a water tank
**Problem.** Find the pressure at the bottom of a 2 m deep tank full of water
($d=1000$ kg/m³, $g=9.8$ m/s²).

**Solution.** $P=hdg=2\times1000\times9.8=19\,600$ Pa.

**Problem.** A pressure of 800 Pa acts at the bottom of a 3 m column of a liquid. Find
its density.

**Solution.** $d=\frac{P}{hg}=\frac{800}{3\times9.8}=\frac{800}{29.4}=27.21$ kg/m³.
:::

**Applications:** dams and water tanks are thicker at the bottom; deep-sea divers wear
special suits; water tanks are placed high on the roof; mercury bottles have thick
bottoms. A bucket fills faster on the ground floor than upstairs because the depth of
water below the tank — and so the pressure — is greater there. Blood pressure is
greater in the feet than in the head for the same reason.

### 6.6.2 Air pressure, compressed air and atmospheric pressure

Air can be **compressed** into tyres, balls and cylinders; compressed air has more
pressure than the atmosphere and heats up when compressed. It drives air hammers,
drills and wrenches, and works the **air brakes** of trains, buses and trucks. Its
pressure is measured with a **pressure gauge**.

The earth is covered by air, which has weight. The pressure exerted by the weight of
the atmosphere on unit area of the earth's surface is **atmospheric pressure**. It is
greatest at sea level, about **760 mmHg ≈ 1.01 × 10⁵ Pa**, and decreases with height.
It is measured with a **barometer**. Aeroplanes keep the air pressure inside the cabin
suitable for breathing.

*Activities.* A glass full of water covered with cardboard can be turned upside down
without the water falling — the air pressure from below holds the card. A can heated
with a little water, closed tightly and cooled gets crushed — the steam inside
condenses, the pressure inside falls, and the outside air pressure crushes the can.

**Uses of atmospheric pressure:** drinking with a straw, filling a fountain pen, filling
a syringe, pumping air into a bicycle tyre. When the piston is pulled back, the
pressure inside falls and the outside air pushes the liquid in.

A **manometer** (U-tube with coloured liquid) measures the pressure of a gas or liquid:
the extra pressure pushes the liquid down in one limb and up in the other; the
difference in levels $h$ measures the pressure.

```figure caption="A U-tube manometer. The extra pressure from the gas supply pushes the liquid down on the left; the difference in levels h measures it."
fig, ax = plt.subplots(figsize=(4.2, 2.8))
ax.set_xlim(0, 10)
ax.set_ylim(0, 6.6)
ax.axis("off")
ax.plot([3, 3, 7, 7], [5.6, 1.0, 1.0, 5.6], color=INK, lw=8, solid_joinstyle="round", solid_capstyle="round")
ax.plot([3, 3, 7, 7], [5.6, 1.0, 1.0, 5.6], color="white", lw=5.5, solid_joinstyle="round", solid_capstyle="round")
ax.plot([3, 3, 7, 7], [2.4, 1.0, 1.0, 4.4], color=ACCENT, lw=5.5, solid_joinstyle="round")
ax.plot([3, 1.2], [5.6, 5.6], color=INK, lw=2)
ax.text(1.1, 6.05, "gas supply", ha="left", fontsize=7.8, color=INK)
ax.annotate("", xy=(3, 2.7), xytext=(3, 5.2), arrowprops=dict(arrowstyle="->", color=SERIES[1], lw=1.2))
ax.plot([3.4, 8.2], [2.4, 2.4], color=MUTED, lw=0.8, ls="--")
ax.plot([7.4, 8.2], [4.4, 4.4], color=MUTED, lw=0.8, ls="--")
ax.annotate("", xy=(8.0, 4.4), xytext=(8.0, 2.4), arrowprops=dict(arrowstyle="<->", color=INK, lw=1))
ax.text(8.3, 3.4, "h", fontsize=9, color=INK, va="center")
ax.text(7.0, 6.05, "open to air", ha="center", fontsize=7.8, color=INK)
fig.tight_layout()
```

## 6.7 Archimedes' principle, upthrust, floatation and density

A body in a liquid feels an upward push called **upthrust** (buoyant force), because
the pressure on its lower surface (deeper) is greater than on its upper surface. A
stone feels lighter in water for this reason.

::: definition Archimedes' principle
When a body is wholly or partly immersed in a fluid, it experiences an upthrust equal
to the weight of the fluid displaced by it. Upthrust $=V\,d\,g$, where $V$ is the volume
of fluid displaced and $d$ its density.
:::

**Density** is mass per unit volume, $d=\frac{m}{V}$ (kg/m³ or g/cm³). Water has a
density of 1000 kg/m³ (1 g/cm³).

| Condition | Result | Example |
|---|---|---|
| weight > upthrust (body denser than liquid) | sinks | stone, iron nail |
| weight = upthrust | floats fully immersed | fish, submarine at a fixed depth |
| weight < maximum upthrust (body less dense) | floats partly out | wood, ice, a ship |

A floating body displaces liquid equal to its own weight (**law of floatation**). An
iron ship floats because its hollow shape displaces a large volume of water. A
submarine sinks or rises by filling or emptying its tanks with water.

::: example Upthrust on a stone
**Problem.** A stone of volume 200 cm³ is fully immersed in water. Find the upthrust
($d=1000$ kg/m³, $g=9.8$ m/s²).

**Solution.** $V=200$ cm³ $=200\times10^{-6}$ m³ $=2\times10^{-4}$ m³.
Upthrust $=Vdg=2\times10^{-4}\times1000\times9.8=1.96$ N (upwards). The stone seems
1.96 N lighter in water.
:::

## Chapter summary

- Rest and motion are relative to a reference point. Speed $=\frac{d}{t}$, velocity
  $=\frac{s}{t}$ (m/s); velocity has direction.
- Relative velocity: $v_A-v_B$ (same direction), $v_A+v_B$ (opposite).
- Average velocity = total displacement ÷ total time $=\frac{u+v}{2}$ for steady change.
- Acceleration $a=\frac{v-u}{t}$ (m/s²); negative acceleration is retardation.
- Slope of d–t graph = speed; slope of v–t graph = acceleration; area under v–t = distance.
- Newton: inertia; $F=ma$; action = reaction.
- Lever: $E\times E.D.=L\times L.D.$; $MA=\frac{L}{E}$, $VR=\frac{E.D.}{L.D.}$,
  $\eta=\frac{MA}{VR}\times100\%$ (< 100 % because of friction).
- Pressure $P=\frac{F}{A}$ (Pa); liquid pressure $P=hdg$; atmospheric pressure at sea
  level = 760 mmHg; barometer, manometer, pressure gauge.
- Upthrust = weight of fluid displaced (Archimedes); a body floats if it is less dense
  than the liquid.

## Practice questions

**Group A — Multiple choice (1 mark each)** *(Textbook exercises.)*

1. The condition of a body that does not change its position with respect to its surroundings is <span class="marks">[1]</span>
   (a) motion (b) velocity (c) rest (d) speed
2. The relative velocity of two bodies moving in opposite directions is <span class="marks">[1]</span>
   (a) $v_A/v_B$ (b) $v_A-v_B$ (c) $v_A\times v_B$ (d) $v_A+v_B$
3. The shortest distance between two points in a particular direction is <span class="marks">[1]</span>
   (a) speed (b) displacement (c) average velocity (d) relative velocity
4. Average velocity is calculated for <span class="marks">[1]</span>
   (a) non-uniform motion (b) uniform motion (c) zero acceleration (d) a body at rest
5. The SI unit of acceleration is <span class="marks">[1]</span>
   (a) m/s (b) m/s² (c) N m²/kg² (d) m²
6. Which statement is true? <span class="marks">[1]</span>
   (a) uniform motion gives negative acceleration (b) non-uniform motion has no acceleration (c) positive acceleration is retardation (d) the rate of change of velocity is acceleration
7. Which is a second-class lever? <span class="marks">[1]</span>
   (a) shovel (b) *dhiki* (c) nutcracker (d) hammer
8. The principle of a lever in balance is <span class="marks">[1]</span>
   (a) E × E.D. = L × L.D. (b) E = L (c) E.D. = L.D. (d) MA = efficiency
9. The work done by the effort is called <span class="marks">[1]</span>
   (a) input work (b) output work (c) friction (d) gravitational work
10. Which is not affected by friction? <span class="marks">[1]</span>
   (a) mechanical advantage (b) velocity ratio (c) efficiency (d) input work
11. Which statement is true? <span class="marks">[1]</span>
   (a) the product of load and effort is VR (b) the effort moves less than the load (c) MA and VR have units (d) efficiency is output work ÷ input work in percent
12. The SI unit of pressure is <span class="marks">[1]</span>
   (a) N m (b) N/m² (c) m/s² (d) N m²/kg²
13. Which statement is true? <span class="marks">[1]</span>
   (a) less area, more pressure (b) area does not affect pressure (c) pressure rises with area (d) pressure is the same for any force
14. Atmospheric pressure at sea level is <span class="marks">[1]</span>
   (a) 760 mmHg (b) 700 mmHg (c) 1000 mmHg (d) 750 mmHg
15. The pressure of water at a depth of 60 m ($g=9.8$ m/s², $d=1000$ kg/m³) is <span class="marks">[1]</span>
   (a) 588 Pa (b) 5880 Pa (c) 58 800 Pa (d) 588 000 Pa
16. Atmospheric pressure is measured by a <span class="marks">[1]</span>
   (a) thermometer (b) barometer (c) manometer (d) lactometer
17. The pressure of compressed air is measured by a <span class="marks">[1]</span>
   (a) pressure gauge (b) rain gauge (c) lactometer (d) thermometer
18. The air brake works on <span class="marks">[1]</span>
   (a) atmospheric pressure (b) compressed air (c) liquid pressure (d) upthrust

::: note Answers to Group A
**1.** (c). **2.** (d). **3.** (b). **4.** (a). **5.** (b). **6.** (d). **7.** (c) — the load (nut) is between hinge and hand. **8.** (a). **9.** (a). **10.** (b). **11.** (d). **12.** (b). **13.** (a). **14.** (a). **15.** (d) — $60\times1000\times9.8=588\,000$ Pa. **16.** (b). **17.** (a). **18.** (b).
:::

**Group B — Short answer (2 marks each)**

1. Differentiate: (a) distance and displacement (b) average velocity and relative velocity (c) acceleration and retardation. <span class="marks">[3]</span>
2. Define reference point, relative velocity and retardation. <span class="marks">[3]</span>
3. Differentiate: (a) mechanical advantage and velocity ratio (b) input work and output work. <span class="marks">[2]</span>
4. Give reasons: (a) The efficiency of a lever is never 100 %. (b) A wheelbarrow is easier to push when the load is moved towards the wheel. (c) MA is always less than VR. <span class="marks">[3]</span>
5. Which class of lever is a pair of scissors? What can a lever with MA more than 1 do? Write other advantages of a lever besides making work easy. <span class="marks">[2]</span>
6. Give reasons: (a) Football boots have studs. (b) A ploughshare is made sharp. (c) The bottom of a dam is wider than its top. (d) A bucket fills faster on the ground floor than upstairs. <span class="marks">[4]</span>
7. How can we show that a liquid exerts pressure? Write two applications of liquid pressure. <span class="marks">[2]</span>
8. What is atmospheric pressure? Write two uses of it. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** (a) See the table in 6.1. (b) Average velocity is the total displacement ÷ total time of one body in non-uniform motion; relative velocity is the velocity of one body with respect to another. (c) See the table in 6.1.4.
**2.** A reference point is a fixed point, line or place with which the position of a body is compared. Relative velocity is the velocity of a body with respect to another body. Retardation is the rate of decrease of velocity (negative acceleration).
**3.** (a) MA = load ÷ effort, affected by friction, always less than VR; VR = effort distance ÷ load distance, not affected by friction. (b) Input work = effort × effort distance (work put into the machine); output work = load × load distance (useful work done by it); output is less than input.
**4.** (a) Some input work is always lost against friction, so output work is less than input work. (b) The load distance becomes shorter, so by $E\times E.D.=L\times L.D.$ less effort is needed. (c) Friction reduces MA but does not change VR.
**5.** First class (the pivot is between blade and handle). A lever with MA > 1 lifts a load larger than the effort (multiplies force). Other advantages: changes the direction of the force, increases speed or distance of movement (third class), and allows work at a convenient place (tongs keep hands away from fire).
**6.** (a) The small area of the studs gives large pressure, so they grip the ground. (b) A sharp edge has small area, so a small force gives large pressure to cut the soil. (c) Liquid pressure increases with depth, so the bottom must be strongest. (d) The depth of water below the tank (h) is greater at the ground floor, so pressure $hdg$ and the flow are greater.
**7.** Make holes at different heights in a bottle full of water; water comes out from all holes (pressure acts sideways) and spurts farthest from the lowest hole (pressure increases with depth). Applications: dams thick at the bottom; tanks kept high; divers' suits.
**8.** The pressure exerted by the weight of air on unit area of the earth's surface (760 mmHg at sea level). Uses: drinking with a straw, filling a syringe or fountain pen, pumping tyres.
:::

**Group C — Numerical and long answer (4 marks each)**

1. A bus covers 4.2 km in 7 minutes. Find its average velocity. <span class="marks">[2]</span>
2. A car starts from rest and reaches 30 m/s in 12 s. Find its acceleration. <span class="marks">[2]</span>
3. A car starts from rest with an acceleration of 5 m/s² for 6 s. Find its final velocity and average velocity. <span class="marks">[3]</span>
4. Brakes give a car a retardation of 2 m/s² and it stops in 4 s. Find its initial velocity. <span class="marks">[2]</span>
5. Two motorcycles move at 50 km/h and 60 km/h. Find their relative velocity in the same and opposite directions. <span class="marks">[2]</span>
6. An effort of 75 N lifts a load of 300 N placed 25 cm from the fulcrum. Find the effort distance. <span class="marks">[2]</span>
7. Sarad (550 N) sits 1.5 m from the centre of a see-saw. How far from the centre must Nirmal (300 N) sit to balance him? <span class="marks">[2]</span>
8. An effort of 300 N lifts a load of 900 N with a 2 m first-class lever; the load is 50 cm from the fulcrum and the effort is at the other end. Find MA, VR and efficiency. <span class="marks">[3]</span>
9. Prove that $P=hdg$. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** $s=4.2$ km $=4200$ m, $t=7$ min $=420$ s. $\bar{v}=\frac{4200}{420}=10$ m/s.
**2.** $a=\frac{v-u}{t}=\frac{30-0}{12}=2.5$ m/s².
**3.** $v=u+at=0+5\times6=30$ m/s. Average velocity $=\frac{u+v}{2}=\frac{0+30}{2}=15$ m/s. *(The answer printed in the textbook, 15 m/s and 7.5 m/s, would be correct only for an acceleration of 2.5 m/s²; with 5 m/s² the correct values are 30 m/s and 15 m/s.)*
**4.** Retardation $=\frac{u-v}{t}$, so $2=\frac{u-0}{4}$ and $u=8$ m/s.
**5.** Same direction: $60-50=10$ km/h. Opposite directions: $60+50=110$ km/h.
**6.** $E\times E.D.=L\times L.D.$: $75\times E.D.=300\times25$, so $E.D.=\frac{7500}{75}=100$ cm $=1$ m.
**7.** $300\times d=550\times1.5$, so $d=\frac{825}{300}=2.75$ m.
**8.** $L.D.=0.5$ m, $E.D.=2-0.5=1.5$ m. $MA=\frac{900}{300}=3$; $VR=\frac{1.5}{0.5}=3$; $\eta=\frac{3}{3}\times100\%=100\%$ (an ideal lever, friction neglected).
**9.** See the derivation box in 6.6.1: $V=Ah$, $m=dAh$, $F=mg=Ahdg$, $P=\frac{F}{A}=hdg$.
:::
