---
subject: Physics
grade: 11
unit: 9
title: Heat and Temperature
hours: 3
area: Heat and Thermodynamics
---

Put a hot glass of tea on a cold marble table and, after a while, both are
lukewarm. Something flowed from one to the other, and it stopped flowing when
some property of the two became equal. That "something" is **heat**; that
property is **temperature**. This short unit separates two words that students
use as if they meant the same thing, and then shows that the rule allowing
temperature to be *measured* at all is a law of physics in its own right — the
zeroth law.

::: key Three ideas, three marks each
(1) Heat is energy in transit, temperature is the average molecular kinetic
energy. (2) Heat flows from high to low temperature until thermal equilibrium
is reached. (3) The zeroth law is what lets a thermometer work at all. Almost
every question from this unit is one of these three dressed up differently.
:::

## 9.1 Molecular concept of thermal energy, heat and temperature; cause and direction of heat flow

Every substance is made of molecules that are never at rest. In a solid they
vibrate about fixed lattice positions; in a liquid they vibrate and slide past
one another; in a gas they fly freely and collide. Each molecule therefore has
kinetic energy, and because the molecules attract one another they also have
potential energy.

::: definition Internal energy and thermal energy
The **internal energy** of a body is the total energy of all its molecules —
the sum of their kinetic energies (of translation, rotation and vibration) and
the potential energy stored in the forces between them. The part of the
internal energy that depends on temperature, i.e. the total molecular kinetic
energy, is called the **thermal energy** of the body.
:::

Temperature is not the *total* energy but the *average* energy per molecule. For
an ideal gas the kinetic theory gives the average translational kinetic energy
of one molecule as

$$ \bar{E}_{k} = \frac{3}{2}k_{B}T $$

where $k_{B} = 1.38\times10^{-23}\ \text{J K}^{-1}$ is the Boltzmann constant
and $T$ is the absolute temperature in kelvin. Turn this around and it says
something important: **temperature is a measure of the average kinetic energy of
the molecules of a body.**

::: caution A bucket of water has more thermal energy than a matchstick flame
A flame at $800\ ^{\circ}\text{C}$ has far higher temperature than a bucket of
water at $30\ ^{\circ}\text{C}$, but the bucket holds far more thermal energy
because it contains enormously more molecules. Temperature is *per molecule*;
thermal energy is *total*. Never say "this body contains more heat".
:::

::: definition Heat
Heat is energy that flows from one body to another **because of a temperature
difference between them**. It exists only while it is being transferred: once
it has arrived it is no longer heat, it is internal energy of the receiving
body. Its SI unit is the joule (J).
:::

**Cause and direction of heat flow.** When two bodies at different temperatures
touch, their surface molecules collide. On average the faster molecules of the
hotter body lose kinetic energy in these collisions and the slower molecules of
the colder body gain it. The net result is a transfer of energy from the body at
higher temperature to the body at lower temperature. So:

- The **cause** of heat flow is the *temperature difference*, not a difference in
  the amount of heat, mass or size.
- The **direction** of heat flow is always from higher to lower temperature.
- Flow stops when the temperatures become equal — not when the energies become
  equal.

| | Heat | Temperature |
|---|---|---|
| What it is | energy in transit | measure of average molecular KE |
| SI unit | joule (J) | kelvin (K) |
| Depends on mass? | yes | no |
| Measured with | calorimeter | thermometer |
| Symbol | $Q$ | $T$ or $\theta$ |
| Decides | how much energy moved | which way the energy moves |

::: example Worked example 9.1
**Problem.** Find the average translational kinetic energy of a molecule of a
gas at $27\ ^{\circ}\text{C}$, and state the temperature at which this energy
would be doubled. Take $k_{B} = 1.38\times10^{-23}\ \text{J K}^{-1}$.

**Solution.** $T = 27 + 273 = 300\ \text{K}$.

$$ \bar{E}_{k} = \frac{3}{2}k_{B}T = 1.5 \times 1.38\times10^{-23}\times 300
= 6.21\times10^{-21}\ \text{J} $$

Since $\bar{E}_{k} \propto T$, doubling the energy needs double the **absolute**
temperature: $T = 600\ \text{K} = 327\ ^{\circ}\text{C}$ — not $54\ ^{\circ}\text{C}$.
:::

## 9.2 Thermal equilibrium and Zeroth law of thermodynamics

Two bodies placed in thermal contact exchange energy until the net flow becomes
zero. They are then said to be in **thermal equilibrium**, and experiment shows
that this happens exactly when their temperatures are equal.

```figure caption="A hot body and a cold body in thermal contact. Energy flows until both reach the same temperature; after that the net flow is zero, though molecular collisions continue."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,2.8))
t = np.linspace(0, 12, 400)
Th = 30 + 50*np.exp(-0.42*t)
Tc = 30 - 20*np.exp(-0.42*t)
ax.plot(t, Th, color=SERIES[1], lw=2.0, label='hot body')
ax.plot(t, Tc, color=ACCENT, lw=2.0, label='cold body')
ax.hlines(30, 0, 12, color=MUTED, lw=1.0, ls='--')
ax.annotate('common temperature\n(thermal equilibrium)', (9.2, 30),
            textcoords='offset points', xytext=(-6, 16), fontsize=8.4, color=MUTED,
            ha='center')
ax.annotate('net heat flow', (1.0, 55), textcoords='offset points', xytext=(26, -2),
            fontsize=8.6, color=INK)
ax.annotate('', xy=(1.0, 19.5), xytext=(1.0, 52),
            arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.2, mutation_scale=11))
ax.set_xlabel('time'); ax.set_ylabel(r'temperature  ($^\circ$C)')
ax.set_xlim(0, 12); ax.set_ylim(0, 90)
ax.set_xticks([])
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.45)
ax.legend(loc='upper right', fontsize=8.4)
```

Now suppose body $A$ is in equilibrium with body $C$, and body $B$ is separately
in equilibrium with the same body $C$. Is $A$ then in equilibrium with $B$?
Experiment says yes, always. This result cannot be deduced from the first or
second laws, and it is so basic that it was named the **zeroth** law after the
others had already been numbered.

::: definition Zeroth law of thermodynamics
If two bodies $A$ and $B$ are each separately in thermal equilibrium with a
third body $C$, then $A$ and $B$ are in thermal equilibrium with each other.
:::

```figure caption="Zeroth law. $A$ and $B$ are separated by an insulating wall but each is in contact with $C$ through a conducting wall. If $T_A = T_C$ and $T_B = T_C$, then $T_A = T_B$."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(4.8,2.6))
def box(x, y, w, h, lab, sub):
    ax.add_patch(Rectangle((x,y), w, h, fill=False, ec=INK, lw=1.4))
    ax.text(x+w/2, y+h/2+0.045, lab, ha='center', va='center', fontsize=12, color=INK)
    ax.text(x+w/2, y+h/2-0.105, sub, ha='center', va='center', fontsize=8.6, color=MUTED)
box(0.04, 0.52, 0.40, 0.30, '$A$', 'at $T_A$')
box(0.56, 0.52, 0.40, 0.30, '$B$', 'at $T_B$')
box(0.04, 0.03, 0.92, 0.27, '$C$', 'thermometer, at $T_C$')
ax.add_patch(Rectangle((0.455, 0.52), 0.09, 0.30, facecolor=GRID, ec=MUTED,
                       lw=1.0, hatch='////'))
ax.annotate('insulating wall', (0.50, 0.82), textcoords='offset points',
            xytext=(0, 9), ha='center', fontsize=8.4, color=MUTED)
ax.text(0.50, 0.41, 'conducting walls', ha='center', va='center',
        fontsize=8.4, color=MUTED)
for x0 in (0.15, 0.85):
    ax.annotate('', xy=(x0, 0.305), xytext=(x0, 0.515),
                arrowprops=dict(arrowstyle='<|-|>', color=ACCENT, lw=1.2, mutation_scale=10))
ax.set_xlim(0, 1.0); ax.set_ylim(0.0, 0.99); ax.axis('off')
```

The zeroth law is the licence to use a thermometer. A thermometer is the third
body $C$. We bring it into contact with $A$ and read it, then with $B$ and read
it. If the readings agree, the law guarantees that $A$ and $B$ are in
equilibrium with each other — so the reading is a genuine property of the state
of each body. That property is what we call **temperature**.

::: key What the zeroth law really defines
The zeroth law establishes that temperature exists as a measurable physical
quantity, and that bodies in thermal equilibrium share a common value of it.
Without it, comparing the temperature of Pokhara and Jumla with two different
thermometers would have no meaning.
:::

## 9.3 Thermal equilibrium as working principle of mercury thermometer

Any physical property that changes measurably and reproducibly with temperature
can be used to measure temperature. Such a property is called a **thermometric
property** — the length of a liquid column, the pressure of a fixed mass of gas,
the resistance of a wire, the e.m.f. of a thermocouple.

| Thermometer | Thermometric property | Useful range |
|---|---|---|
| Mercury-in-glass | length of mercury column | $-39\ ^{\circ}$C to $357\ ^{\circ}$C |
| Alcohol-in-glass | length of alcohol column | $-115\ ^{\circ}$C to $78\ ^{\circ}$C |
| Constant-volume gas | pressure of fixed mass of gas | $-270\ ^{\circ}$C to $1500\ ^{\circ}$C |
| Platinum resistance | electrical resistance | $-200\ ^{\circ}$C to $1200\ ^{\circ}$C |
| Thermocouple | thermo-e.m.f. | $-200\ ^{\circ}$C to $1600\ ^{\circ}$C |

A mercury thermometer is a thin-walled glass **bulb** joined to a uniform
capillary tube of very fine bore, sealed after the air above the mercury has
been removed. The bulb holds the mercury; the fine bore makes a small expansion
of the mercury produce a long, easily read movement of the thread.

```figure caption="Mercury-in-glass thermometer. The length of the thread measured from the bulb is $l_0$ at the ice point, $l_{100}$ at the steam point and $l_t$ at the unknown temperature $t$."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
fig, ax = plt.subplots(figsize=(5.0,2.6))
ax.add_patch(Rectangle((0.9, -0.22), 8.7, 0.44, fill=False, ec=INK, lw=1.4))
ax.add_patch(Circle((0.62, 0.0), 0.46, facecolor=SERIES[1], ec=INK, lw=1.4, zorder=3))
ax.add_patch(Rectangle((0.9, -0.13), 5.5, 0.26, facecolor=SERIES[1], ec='none', zorder=2))
for x0, lab in [(2.4, '$0$'), (7.9, '$100$')]:
    ax.plot([x0, x0], [0.22, 0.46], color=INK, lw=1.2)
    ax.text(x0, 0.56, lab, ha='center', fontsize=9, color=INK)
for x0 in np.arange(2.4, 7.91, 0.55):
    ax.plot([x0, x0], [0.22, 0.36], color=MUTED, lw=0.8)
ax.plot([6.4, 6.4], [0.22, 0.60], color=ACCENT, lw=1.3)
ax.text(6.4, 0.70, '$t$', ha='center', fontsize=9.5, color=ACCENT)
def span(x1, x2, y, lab, c):
    ax.annotate('', xy=(x2, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle='<|-|>', color=c, lw=1.1, mutation_scale=8))
    ax.text(x2+0.24, y, lab, ha='left', va='center', fontsize=9, color=c)
span(0.62, 2.4, -0.50, '$l_0$', MUTED)
span(0.62, 6.4, -0.92, '$l_t$', ACCENT)
span(0.62, 7.9, -1.34, '$l_{100}$', MUTED)
ax.text(0.62, 0.80, 'bulb', ha='center', fontsize=8.6, color=MUTED)
ax.text(8.9, -0.70, 'capillary stem', ha='center', fontsize=8.6, color=MUTED)
ax.set_xlim(0, 10.2); ax.set_ylim(-1.66, 1.0)
ax.set_aspect('equal'); ax.axis('off')
```

**How it works — thermal equilibrium is the whole principle.** The bulb is placed
in contact with the body whose temperature is wanted. Heat flows between body and
bulb until the two reach thermal equilibrium, i.e. until the mercury is at the
**same temperature as the body**. The mercury, having a larger expansivity than
glass, has by then moved along the stem to a definite position, and by the zeroth
law that position is a measure of the body's own temperature. Note the two
conditions hidden in this: the thermometer must be left long enough to reach
equilibrium, and it must be small enough that the heat it absorbs does not
noticeably change the body's temperature.

**Calibration.** Two fixed points are used:

- **Lower fixed point (ice point):** the temperature of pure melting ice at
  standard atmospheric pressure, marked $0\ ^{\circ}\text{C}$; the thread length
  is $l_0$.
- **Upper fixed point (steam point):** the temperature of steam above water
  boiling at standard atmospheric pressure, marked $100\ ^{\circ}\text{C}$; the
  thread length is $l_{100}$.

The interval between them is divided into 100 equal parts, which gives the working
formula of every two-fixed-point thermometer.

::: derivation The thermometric formula for any thermometer
We start from the assumption that the thermometric property changes *uniformly* with
temperature, and reach the formula that converts a reading into a temperature.

**Setting up.** Let $X$ be whatever property we measure — the length of a mercury thread,
the pressure of a gas, the resistance of a wire. Its values are $X_0$ at the ice point
($0\ ^{\circ}\text{C}$), $X_{100}$ at the steam point ($100\ ^{\circ}\text{C}$), and
$X_t$ at the unknown temperature $t$.

**Step 1 — assume a straight line.** "Uniform change" means $X$ is a linear function of
$t$, so a graph of $X$ against $t$ is a straight line:

$$ X = a + bt $$

**Step 2 — how much the property changed for the unknown reading.** Subtracting the ice
point value:

$$ X_t - X_0 = (a + bt) - (a + b\times 0) = bt $$

**Step 3 — how much it changed over the whole 100 degrees.** The same subtraction with
$t = 100$:

$$ X_{100} - X_0 = b \times 100 $$

**Step 4 — divide Step 2 by Step 3.** We divide so that the unknown constant $b$ cancels,
and $a$ has already gone:

$$ \frac{X_t - X_0}{X_{100} - X_0} = \frac{bt}{100b} = \frac{t}{100} $$

**Step 5 — multiply both sides by 100:**

$$ t = \frac{X_t - X_0}{X_{100} - X_0}\times 100\ ^{\circ}\text{C} $$

**Result.** For a mercury thermometer, $X$ is the thread length $l$, so

$$ t = \frac{l_t - l_0}{l_{100} - l_0}\times 100\ ^{\circ}\text{C} $$

**What it means.** The unknown constants $a$ and $b$ both dropped out, so we never need to
know them — two fixed points are enough to read any temperature in between. The fraction
is simply "how far along the scale we are", expressed as a fraction of the whole interval.

**Condition used.** The property must change *linearly* with temperature over this range.
If it does not, two different thermometers will disagree at the same real temperature even
though they agree at $0$ and $100\ ^{\circ}\text{C}$.
:::

The three scales in use are related in exactly the same way — each fraction is "how far
along its own scale", and equal fractions mean the same temperature:

$$ \frac{C}{100} = \frac{F-32}{180} = \frac{K-273.15}{100} $$

::: memory Why mercury and not water
- It is a **good conductor** of heat, so it reaches equilibrium quickly.
- It expands **uniformly** over a wide range, giving an evenly divided scale.
- It has a **wide range**: freezes at $-39\ ^{\circ}$C, boils at $357\ ^{\circ}$C.
- Its **specific heat capacity is low**, so it takes very little heat from the
  body being measured.
- It is **opaque and shiny**, so the thread is easy to see.
- It **does not wet glass**, so none is left clinging to the bore.

Water fails on almost every count: it wets glass, is a poor conductor, is
transparent, has a small range and — worst — expands anomalously below
$4\ ^{\circ}$C, so one length would stand for two temperatures.
:::

A **clinical thermometer** is the same instrument with the range narrowed to
about $35\ ^{\circ}$C–$42\ ^{\circ}$C so that each division can be
$0.1\ ^{\circ}$C, and with a **constriction** in the bore just above the bulb.
The constriction lets mercury push past while the thread rises but breaks the
thread when it cools, so the reading is held until the thermometer is shaken
down.

::: example Worked example 9.2
**Problem.** In a mercury thermometer the mercury thread is $5.0\ \text{cm}$ long
at the ice point and $25.0\ \text{cm}$ long at the steam point. (a) What
temperature corresponds to a thread length of $15.6\ \text{cm}$? (b) How long is
the thread at normal body temperature, $37\ ^{\circ}\text{C}$?

**Solution.** (a) Using the calibration formula,

$$ t = \frac{15.6 - 5.0}{25.0 - 5.0}\times100 = \frac{10.6}{20.0}\times100
= 53\ ^{\circ}\text{C} $$

(b) Rearranging, $l_t = l_0 + \dfrac{t}{100}(l_{100}-l_0)
= 5.0 + 0.37\times20.0 = 12.4\ \text{cm}$.
:::

::: example Worked example 9.3
**Problem.** (a) Convert normal body temperature $37\ ^{\circ}\text{C}$ to the
Fahrenheit and Kelvin scales. (b) At what temperature do the Celsius and
Fahrenheit scales give the same reading?

**Solution.** (a) From $\dfrac{C}{100} = \dfrac{F-32}{180}$ we get
$F = \frac{9}{5}C + 32 = \frac{9}{5}(37) + 32 = 66.6 + 32 = 98.6\ ^{\circ}\text{F}$,
and $K = C + 273.15 = 310.15\ \text{K}$.

(b) Put $F = C = x$:

$$ x = \frac{9}{5}x + 32 \ \Rightarrow\ -\frac{4}{5}x = 32 \ \Rightarrow\ x = -40 $$

So $-40\ ^{\circ}\text{C} = -40\ ^{\circ}\text{F}$.
:::

::: example Worked example 9.4
**Problem.** A faulty mercury thermometer reads $5\ ^{\circ}\text{C}$ in melting
ice and $95\ ^{\circ}\text{C}$ in steam. What is the true temperature when it
reads $59\ ^{\circ}\text{C}$?

**Solution.** The faulty scale has 90 of its own divisions between the two fixed
points, so treat its reading like a thread length:

$$ t_{\text{true}} = \frac{59 - 5}{95 - 5}\times100 = \frac{54}{90}\times100
= 60\ ^{\circ}\text{C} $$

The divisions are still equal — only the two end marks are misplaced — so the
correction is a simple proportion.
:::

## Chapter summary

- Internal energy is the total kinetic + potential energy of the molecules;
  thermal energy is its temperature-dependent (kinetic) part.
- Temperature measures the **average** molecular kinetic energy:
  $\bar{E}_{k} = \frac{3}{2}k_{B}T$ with
  $k_{B} = 1.38\times10^{-23}\ \text{J K}^{-1}$.
- Heat is energy in transit due to a temperature difference. Its cause is the
  temperature difference and its direction is always hot $\to$ cold.
- Thermal equilibrium is the state of zero net heat flow, reached when the two
  temperatures become equal.
- Zeroth law: if $A$ and $B$ are each in equilibrium with $C$, they are in
  equilibrium with each other. This is what makes temperature measurable.
- A mercury thermometer works by coming into thermal equilibrium with the body;
  its thermometric property is the length of the mercury thread, and
  $t = \dfrac{l_t-l_0}{l_{100}-l_0}\times100\ ^{\circ}\text{C}$.
- Scale conversion: $\dfrac{C}{100} = \dfrac{F-32}{180} = \dfrac{K-273.15}{100}$.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. Heat flows from body $A$ to body $B$ when placed in contact because $A$ has
   <span class="marks">[1]</span>
   (a) more heat (b) greater mass (c) higher average molecular kinetic energy (d) greater volume
2. The law of thermodynamics that makes temperature a measurable quantity is the
   <span class="marks">[1]</span>
   (a) zeroth law (b) first law (c) second law (d) third law
3. The temperature at which the Celsius and Fahrenheit scales read the same is
   <span class="marks">[1]</span>
   (a) $0^{\circ}$ (b) $-32^{\circ}$ (c) $-40^{\circ}$ (d) $100^{\circ}$
4. The thermometric property of a mercury-in-glass thermometer is the
   <span class="marks">[1]</span>
   (a) pressure of mercury (b) resistance of mercury (c) length of the mercury column (d) mass of mercury
5. A temperature of $300\ \text{K}$ is approximately <span class="marks">[1]</span>
   (a) $27\ ^{\circ}$C (b) $300\ ^{\circ}$C (c) $573\ ^{\circ}$C (d) $-27\ ^{\circ}$C

::: note Answers to Group A
**1.** (c) — temperature, i.e. average molecular KE, decides the direction; the total heat content does not.
**2.** (a) — the zeroth law guarantees a common value shared by bodies in equilibrium.
**3.** (c) — solving $x = \frac{9}{5}x+32$ gives $x = -40$.
**4.** (c) — the measured quantity is the length of the thread in the uniform bore.
**5.** (a) — $300 - 273 = 27\ ^{\circ}$C.
:::

**Group B — Short answer (5 marks each)**

1. Distinguish between heat and temperature on a molecular basis. Explain why a
   bucket of warm water can hold more thermal energy than a small flame at a much
   higher temperature. <span class="marks">[5]</span>
2. State the zeroth law of thermodynamics and explain how it makes the
   measurement of temperature possible. <span class="marks">[5]</span>
3. Explain thermal equilibrium as the working principle of a mercury
   thermometer, and give four reasons why mercury is preferred to water as a
   thermometric liquid. <span class="marks">[5]</span>
4. The mercury thread in a thermometer is $4.0\ \text{cm}$ long at the ice point
   and $24.0\ \text{cm}$ long at the steam point. Find (a) the temperature when
   the thread is $13.0\ \text{cm}$ long and (b) the thread length at
   $65\ ^{\circ}\text{C}$. <span class="marks">[5]</span>
5. Calculate the average translational kinetic energy of a gas molecule at
   $127\ ^{\circ}\text{C}$, and find the temperature in $^{\circ}$C at which it
   is half this value. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Outline: temperature = average molecular KE (an intensive quantity, per
molecule); heat = energy in transit driven by a temperature difference. Thermal
energy is the *total* molecular KE, so it grows with the number of molecules —
a bucket of water has of order $10^{27}$ molecules against a flame's tiny number,
so the total wins even though the energy per molecule is much smaller.

**4.** (a) $t = \dfrac{13.0-4.0}{24.0-4.0}\times100 = \dfrac{9.0}{20.0}\times100 = 45\ ^{\circ}\text{C}$.
(b) $l = 4.0 + 0.65\times20.0 = 17.0\ \text{cm}$.

**5.** $T = 127+273 = 400\ \text{K}$, so
$\bar{E}_k = 1.5\times1.38\times10^{-23}\times400 = 8.28\times10^{-21}\ \text{J}$.
Half of this needs $T = 200\ \text{K} = -73\ ^{\circ}\text{C}$.
:::

**Group C — Long answer (8 marks each)**

1. (a) Explain, on the molecular model, what is meant by thermal energy, heat
   and temperature, and state the cause and direction of heat flow.
   <span class="marks">[4]</span>
   (b) State the zeroth law of thermodynamics and describe the construction and
   working of a mercury-in-glass thermometer, showing how it is calibrated
   between the two fixed points. <span class="marks">[4]</span>
2. (a) Define thermometric property and name the property used in a constant
   volume gas thermometer and in a platinum resistance thermometer.
   <span class="marks">[2]</span>
   (b) A faulty thermometer reads $2\ ^{\circ}\text{C}$ in melting ice and
   $102\ ^{\circ}\text{C}$ in steam. What is the true temperature when it reads
   $77\ ^{\circ}\text{C}$? <span class="marks">[3]</span>
   (c) At what temperature does the Fahrenheit reading become exactly twice the
   Celsius reading? <span class="marks">[3]</span>

::: note Answers to Group C
**2.** (a) A thermometric property is any measurable physical property that
varies continuously, uniformly and reproducibly with temperature. Gas
thermometer: the pressure of a fixed mass of gas at constant volume. Platinum
thermometer: the electrical resistance of the platinum wire.

(b) The faulty scale spans $102 - 2 = 100$ of its own divisions, so
$t_{\text{true}} = \dfrac{77-2}{102-2}\times100 = 75\ ^{\circ}\text{C}$.

(c) Put $F = 2C$ in $F = \frac{9}{5}C + 32$:
$2C = 1.8C + 32 \Rightarrow 0.2C = 32 \Rightarrow C = 160\ ^{\circ}\text{C}$,
and then $F = 320\ ^{\circ}\text{F}$. Check: $\frac{9}{5}(160)+32 = 288+32 = 320$. ✓
:::
