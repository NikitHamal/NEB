---
subject: Physics
grade: 11
unit: 23
title: DC Circuits
hours: 10
area: Electricity and Magnetism
---

A direct-current (DC) circuit is a closed path in which charge is pushed round
in one steady direction by a source such as a cell, a battery or a DC power
supply. This is the longest unit in the electricity area, and it is the most
practical: almost every measuring instrument you meet in the school laboratory —
ammeter, voltmeter, metre bridge, potentiometer — is a DC circuit designed to
answer one question accurately. Here you learn what current really is at the
level of the electrons, how resistance arises, how to reduce any network to a
single resistance, how to analyse networks that refuse to reduce (Kirchhoff),
and finally where the energy goes.

::: key What the examiner asks from this unit
Every year this unit supplies a derivation (drift velocity, series/parallel,
Wheatstone balance, or $V = E - Ir$), a network numerical, and one instrument
question (metre bridge, potentiometer, or converting a galvanometer). Learn the
four derivations properly and practise reducing networks quickly.
:::

## 23.1 Electric Currents; Drift velocity and its relation with current

An **electric current** is the rate of flow of charge across a section of a
conductor. If a charge $\Delta Q$ crosses a section in time $\Delta t$,

$$ I_{av} = \frac{\Delta Q}{\Delta t}, \qquad I = \frac{dQ}{dt} $$

The SI unit is the **ampere** (A): $1\ \text{A} = 1\ \text{C s}^{-1}$. Current is
a scalar, even though we draw arrows for it. By convention the arrow shows the
direction in which *positive* charge would move — in a metal the actual carriers
are electrons, moving the opposite way.

A related quantity is the **current density**, the current per unit
cross-sectional area:

$$ J = \frac{I}{A} \qquad (\text{unit: A m}^{-2}) $$

### Why a drift velocity exists

In a metal the outermost electrons are free. Even with no battery connected they
fly about randomly at about $10^{5}\ \text{m s}^{-1}$, colliding with the
vibrating ions roughly every $\tau \approx 10^{-14}\ \text{s}$. Because the
directions are random, the *average* velocity is zero and there is no current.

When a battery maintains a field $E$ inside the wire, every electron gets a small
extra acceleration $a = eE/m$ between collisions. Each collision wipes out the
memory of the previous push, so on average the electrons acquire a small steady
velocity opposite to $E$:

$$ v_d = \frac{eE\tau}{m} $$

::: definition Drift velocity
Drift velocity is the average velocity with which free electrons in a conductor
move along the conductor under an applied electric field. Its magnitude is of the
order of $10^{-4}\ \text{m s}^{-1}$ — less than a millimetre per second.
:::

```figure caption="Free electrons drift slowly opposite to the field $E$. Every electron within a distance $v_d\Delta t$ of the shaded section crosses it in time $\Delta t$."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(5.0,3.0))

ax.add_patch(Rectangle((0.6,1.6), 4.8, 1.4, fc='#eef2f7', ec=INK, lw=1.3, zorder=1))
ax.add_patch(Rectangle((3.0,1.6), 1.3, 1.4, fc=ACCENT, ec='none', alpha=0.20, zorder=2))
ax.plot([3.0,3.0],[1.6,3.0], color=INK, lw=1.4, ls='--', zorder=4)

rng = np.random.default_rng(7)
xs = rng.uniform(0.95,5.05,12); ys = rng.uniform(1.98,2.42,12)
ax.plot(xs, ys, 'o', ms=5.2, color='#d9534f', zorder=5)
for x,y in zip(xs,ys):
    ax.annotate('', xy=(x-0.30,y), xytext=(x,y),
                arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=0.9, mutation_scale=7), zorder=4)

# external circuit: + terminal on the left, so I runs left along the bottom wire
p = np.array([(0.6,2.3),(0.05,2.3),(0.05,0.45),(2.86,0.45)], float)
ax.plot(p[:,0], p[:,1], color=INK, lw=1.4, zorder=3)
p2 = np.array([(3.14,0.45),(5.95,0.45),(5.95,2.3),(5.4,2.3)], float)
ax.plot(p2[:,0], p2[:,1], color=INK, lw=1.4, zorder=3)
ax.plot([2.86,2.86],[0.18,0.72], color=INK, lw=1.4)
ax.plot([3.14,3.14],[0.30,0.60], color=INK, lw=3.2)
ax.annotate('+', (2.70,0.82), color=INK, fontsize=10, ha='center')
ax.annotate('$-$', (3.32,0.82), color=INK, fontsize=10, ha='center')
ax.annotate('', xy=(1.4,0.45), xytext=(2.2,0.45),
            arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.2, mutation_scale=10))

# conventional current (top lane), drift velocity (top lane, right)
ax.annotate('', xy=(2.65,2.78), xytext=(1.75,2.78),
            arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.8, mutation_scale=12), zorder=6)
ax.annotate('$I$', (1.66,2.78), ha='right', va='center', color=ACCENT, fontsize=10)
ax.annotate('', xy=(4.35,2.78), xytext=(5.05,2.78),
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.4, mutation_scale=11), zorder=6)
ax.annotate('$v_d$', (5.12,2.78), ha='left', va='center', color=MUTED, fontsize=10)
# field inside (bottom lane)
ax.annotate('', xy=(1.95,1.78), xytext=(1.15,1.78),
            arrowprops=dict(arrowstyle='-|>', color='#2e8b57', lw=1.4, mutation_scale=11), zorder=6)
ax.annotate('$E$', (1.06,1.78), ha='right', va='center', color='#2e8b57', fontsize=10)

ax.annotate('area $A$', (3.0,3.12), ha='center', color=INK, fontsize=9.2)
ax.annotate('', xy=(3.0,1.45), xytext=(4.3,1.45),
            arrowprops=dict(arrowstyle='<|-|>', color=INK, lw=1.0, mutation_scale=9))
ax.annotate('$v_d\\Delta t$', (3.65,1.16), ha='center', color=INK, fontsize=9.5)
ax.annotate('free electrons', (4.05,1.78), ha='center', color='#d9534f', fontsize=9.0)

ax.set_xlim(-0.55,6.45); ax.set_ylim(0.0,3.45); ax.axis('off')
```

::: derivation Relation between current and drift velocity, $I = nAv_de$
We start from the definition of current as charge per second and reach a formula
linking it to the slow drift of the free electrons.

**Setting up.** A metal wire has cross-sectional area $A$. It contains $n$ free
electrons in every cubic metre, each carrying charge $e$. Under the applied
field they all drift along the wire with the same average speed $v_d$. Fix your
attention on one cross-section of the wire and count the charge that crosses it
in a time $\Delta t$.

**Step 1 — find how far an electron travels in the time $\Delta t$.** Distance
equals speed times time:

$$ l = v_d\,\Delta t $$

**Step 2 — identify which electrons manage to cross the section.** Only those
starting no further back than $l$ can reach it in time. They are exactly the
electrons inside a cylinder of length $l$ and end area $A$.

**Step 3 — find the volume of that cylinder.** Volume = area $\times$ length:

$$ \text{Volume} = A\,l = A v_d\,\Delta t $$

**Step 4 — find how many electrons are inside it.** Number = number per unit
volume $\times$ volume:

$$ N = n \times A v_d \Delta t $$

**Step 5 — find the total charge those electrons carry.** Charge = number
$\times$ charge on each:

$$ \Delta Q = N e = n A v_d \Delta t\, e $$

**Step 6 — use the definition of current, charge per unit time.**

$$ I = \frac{\Delta Q}{\Delta t} = \frac{n A v_d \Delta t\, e}{\Delta t} $$

**Step 7 — cancel $\Delta t$ from top and bottom.**

$$ I = n A v_d e $$

**Step 8 — divide both sides by $A$ to get the current density.** Current
density $J$ is current per unit area:

$$ J = \frac{I}{A} = n e v_d $$

**Result.** $I = nAv_de$, and equivalently $J = nev_d$.

**What it means.** The current is large not because the electrons are fast but
because $n$ is enormous — about $10^{29}$ per cubic metre in copper. That is why
a drift velocity of a fraction of a millimetre per second still gives amperes of
current. Doubling the current in a given wire only doubles $v_d$.

**Conditions used.** A steady current; a uniform conductor of constant area $A$;
one kind of charge carrier, all drifting with the same average speed; and $n$
constant along the wire.
:::

::: tip The examiner is looking for
1. The distance $v_d\Delta t$ and the statement that the electrons which cross
   are those inside a cylinder of that length.
2. Volume $= Av_d\Delta t$, then number $= nAv_d\Delta t$.
3. Charge $\Delta Q = nAv_d\Delta t\,e$.
4. $I = \Delta Q/\Delta t$ and the cancellation of $\Delta t$.
:::

::: example Worked example 23.1
**Problem.** A copper wire of cross-section $1.0\ \text{mm}^{2}$ carries a current
of $5.0\ \text{A}$. Copper has $n = 8.5\times10^{28}$ free electrons per cubic
metre and $e = 1.6\times10^{-19}\ \text{C}$. Find the drift velocity, and the time
an electron takes to drift $1\ \text{m}$ along the wire.

**Solution.** $A = 1.0\ \text{mm}^{2} = 1.0\times10^{-6}\ \text{m}^{2}$.

$$ v_d = \frac{I}{nAe} = \frac{5.0}{(8.5\times10^{28})(1.0\times10^{-6})(1.6\times10^{-19})} $$

The denominator is $8.5\times10^{28}\times10^{-6} = 8.5\times10^{22}$, and
$8.5\times10^{22}\times1.6\times10^{-19} = 1.36\times10^{4}$. Hence

$$ v_d = \frac{5.0}{1.36\times10^{4}} = 3.7\times10^{-4}\ \text{m s}^{-1} $$

Time for $1\ \text{m}$: $t = 1/(3.7\times10^{-4}) = 2.7\times10^{3}\ \text{s}$,
about $45$ minutes.
:::

::: caution Then why does the bulb light instantly?
The electrons crawl, but the *electric field* that sets them moving is
established along the whole wire at nearly the speed of light. Electrons
everywhere in the circuit — including those already inside the filament — start
drifting almost at once. Nothing has to travel from the switch to the bulb.
:::

## 23.2 Ohm's law, Electrical Resistance, Resistivity, Conductivity

::: definition Ohm's law
The current flowing through a conductor is directly proportional to the potential
difference across its ends, provided its physical conditions (temperature,
length, cross-section, nature of material) remain constant:
$V \propto I$, i.e. $V = IR$.
:::

The constant $R$ is the **resistance** of the conductor. Its SI unit is the **ohm**
($\Omega$): a conductor has a resistance of one ohm if a potential difference of
one volt drives a current of one ampere through it.

$$ R = \frac{V}{I} \qquad (1\ \Omega = 1\ \text{V A}^{-1}) $$

Experiment shows that for a uniform wire the resistance is proportional to its
length $l$ and inversely proportional to its area of cross-section $A$:

$$ R = \rho\,\frac{l}{A} $$

$\rho$ is the **resistivity** (specific resistance) of the material, with unit
$\Omega\ \text{m}$. Numerically it is the resistance of a piece of the material
one metre long and one square metre in cross-section. Its reciprocal is the
**conductivity**

$$ \sigma = \frac{1}{\rho} \qquad (\text{unit: } \Omega^{-1}\ \text{m}^{-1}\ \text{or S m}^{-1}) $$

::: key Resistance vs resistivity
Resistance depends on the material *and* on the shape and size of the specimen.
Resistivity depends only on the material and its temperature. Cutting a wire in
half halves its resistance but leaves its resistivity unchanged.
:::

| Material | $\rho$ at 20 °C (Ω m) | Class |
|---|---|---|
| Silver | $1.59\times10^{-8}$ | conductor |
| Copper | $1.68\times10^{-8}$ | conductor (house wiring) |
| Aluminium | $2.65\times10^{-8}$ | conductor (transmission lines) |
| Tungsten | $5.60\times10^{-8}$ | lamp filament |
| Nichrome | $1.10\times10^{-6}$ | heating element |
| Germanium | $0.46$ | semiconductor |
| Silicon (pure) | $\approx 640$ | semiconductor |
| Glass | $10^{10} - 10^{14}$ | insulator |

::: derivation Microscopic form of Ohm's law, $\rho = \dfrac{m}{ne^{2}\tau}$
We start from the drift velocity of the free electrons and reach an explanation
of *why* a metal obeys Ohm's law, together with a formula for its resistivity.

**Setting up.** A wire of length $l$ and area $A$ carries a current $I$ under a
potential difference $V$. It has $n$ free electrons per unit volume, each of
mass $m$ and charge $e$, and $\tau$ is the average time between two collisions
of an electron with the vibrating ions.

**Step 1 — write the field inside the wire.** The field is uniform along the
wire, so from $E = V/d$ with $d = l$:

$$ E = \frac{V}{l} $$

**Step 2 — write the drift velocity produced by that field.** From §23.1, the
electron is accelerated for an average time $\tau$ before each collision, giving

$$ v_d = \frac{eE\tau}{m} $$

**Step 3 — start from the current equation of §23.1.**

$$ I = nAv_de $$

**Step 4 — substitute the drift velocity from Step 2.**

$$ I = nAe\cdot\frac{eE\tau}{m} $$

**Step 5 — collect the two factors of $e$.**

$$ I = \frac{ne^{2}\tau A}{m}\,E $$

**Step 6 — substitute the field from Step 1.**

$$ I = \frac{ne^{2}\tau A}{m}\cdot\frac{V}{l} $$

**Step 7 — divide both sides by $I$ and multiply by the big fraction,
so as to make $V/I$ the subject.**

$$ \frac{V}{I} = \frac{m}{ne^{2}\tau}\cdot\frac{l}{A} $$

**Step 8 — recognise $V/I$ as the resistance.**

$$ R = \frac{m}{ne^{2}\tau}\cdot\frac{l}{A} $$

**Step 9 — compare this, term by term, with the experimental law
$R = \rho l/A$.** The factor multiplying $l/A$ must be the resistivity:

$$ \rho = \frac{m}{ne^{2}\tau} $$

**Result.** The resistivity of a metal is $\rho = m/(ne^{2}\tau)$, and the
resistance is $R = \rho l/A$.

**What it means.** Not one of $m$, $n$, $e$ or $\tau$ depends on the applied
voltage, so at a fixed temperature $R$ is a constant — and $V = IR$, which *is*
Ohm's law. The formula also explains heating: warmer ions vibrate harder, the
electrons collide sooner, $\tau$ falls and $\rho$ rises.

**Conditions used.** A metal with free electrons as the only carriers; constant
temperature (so $\tau$ is fixed); and a uniform wire in a steady state.
:::

For a metal over a moderate range of temperature,

$$ R_t = R_0(1 + \alpha t) $$

where $\alpha$ is the temperature coefficient of resistance (for copper
$\alpha \approx 4.0\times10^{-3}\ ^{\circ}\text{C}^{-1}$). For semiconductors and
electrolytes $\alpha$ is **negative**: resistance falls as temperature rises,
because heating frees many more charge carriers.

::: example Worked example 23.2
**Problem.** A copper wire is $10\ \text{m}$ long and $1.0\ \text{mm}$ in
diameter ($\rho = 1.68\times10^{-8}\ \Omega\ \text{m}$). (a) Find its resistance.
(b) The wire is now stretched uniformly to twice its original length. What is its
new resistance?

**Solution.**

(a) $A = \pi r^{2} = \pi(0.5\times10^{-3})^{2} = 7.85\times10^{-7}\ \text{m}^{2}$.

$$ R = \frac{\rho l}{A} = \frac{1.68\times10^{-8}\times10}{7.85\times10^{-7}} = 0.214\ \Omega $$

(b) Stretching does not change the volume, so $A'l' = Al$. With $l' = 2l$ we get
$A' = A/2$. Hence

$$ R' = \rho\frac{l'}{A'} = \rho\frac{2l}{A/2} = 4\rho\frac{l}{A} = 4R = 0.856\ \Omega $$

In general $R \propto l^{2}$ for a stretched wire of fixed volume.
:::

## 23.3 Current-voltage relations: Ohmic and Non-Ohmic resistance

A conductor that obeys Ohm's law is **ohmic**: its $I$–$V$ graph is a straight
line through the origin, and $R = V/I$ is the same at every point. A conductor
whose $I$–$V$ graph is not a straight line through the origin is **non-ohmic**.

```figure caption="$I$–$V$ characteristics. Only the metallic conductor is ohmic; the lamp and the diode are not."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,3.0))
V = np.linspace(-1.2, 3.0, 500)

ax.plot(V, 9.0*V, color=SERIES[0], lw=1.9, label='metallic conductor')
lamp = np.clip(17.0*np.sign(V)*np.abs(V)**0.55, -13.5, 33.0)
ax.plot(V, lamp, color=SERIES[1], lw=1.9, label='filament lamp')
dio = np.where(V > 0.62, 38.0*np.abs(V-0.62)**1.6, 0.0) + np.where(V < 0, -0.4, 0.0)
ax.plot(V, np.clip(dio, -13.5, 33.0), color=SERIES[2], lw=1.9, label='semiconductor diode')

ax.axhline(0, color=MUTED, lw=0.9); ax.axvline(0, color=MUTED, lw=0.9)
ax.annotate('$0.6$ V', (0.66,-5.5), color=SERIES[2], fontsize=8.4, ha='left')
ax.set_xlabel('potential difference  $V$  (V)')
ax.set_ylabel('current  $I$  (mA)')
ax.set_xlim(-1.3,3.1); ax.set_ylim(-14,34)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.5)
ax.legend(loc='upper left', fontsize=8.0)
```

| Ohmic | Non-ohmic |
|---|---|
| $I$–$V$ graph is a straight line through origin | graph is curved, or does not pass through origin |
| $R = V/I$ constant | $R = V/I$ changes with $V$ |
| Same behaviour for either polarity | may depend on the direction of current |
| Metals at constant temperature, nichrome, carbon resistors | filament lamp, diode, thermistor, electrolyte, gas discharge tube, transistor |

A **filament lamp** is non-ohmic only because the current heats the tungsten: as
$V$ rises the filament goes from about 300 K to about 2500 K, its resistance
rises several times, and the graph bends towards the $V$-axis. A **junction
diode** conducts almost nothing until the forward voltage reaches about
$0.6\ \text{V}$ (silicon), and blocks current completely in reverse.

::: caution Slope is not always resistance
For a non-ohmic device, the resistance at a point is $V/I$ (the slope of the
*chord* from the origin), **not** $dV/dI$ (the slope of the tangent, which is the
*dynamic* resistance). For an ohmic conductor the two happen to be equal — which
is why students confuse them.
:::

## 23.4 Resistances in series and parallel

Any combination of resistors between two terminals can be replaced by one
**equivalent resistance** $R_{eq}$ that would draw the same current from the same
supply.

```figure caption="Left: resistors in series carry the same current and share the voltage. Right: resistors in parallel have the same voltage and share the current."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, axes = plt.subplots(1, 2, figsize=(5.2,2.7))

def wire(ax, pts, lw=1.3):
    p = np.array(pts, float); ax.plot(p[:,0], p[:,1], color=INK, lw=lw, zorder=2)

def res_h(ax, x, y, lab, w=0.66, h=0.26):
    ax.add_patch(Rectangle((x-w/2,y-h/2), w, h, fc='white', ec=INK, lw=1.2, zorder=3))
    ax.annotate(lab, (x, y+h/2+0.07), ha='center', va='bottom', fontsize=8.8, color=INK)

def res_v(ax, x, y, lab, w=0.26, h=0.62):
    ax.add_patch(Rectangle((x-w/2,y-h/2), w, h, fc='white', ec=INK, lw=1.2, zorder=3))
    ax.annotate(lab, (x+w/2+0.10, y), ha='left', va='center', fontsize=8.8, color=INK)

def cell_h(ax, x, y, lab='$V$'):
    ax.plot([x-0.08,x-0.08],[y-0.28,y+0.28], color=INK, lw=1.4, zorder=3)
    ax.plot([x+0.08,x+0.08],[y-0.15,y+0.15], color=INK, lw=3.2, zorder=3)
    ax.annotate(lab, (x, y-0.42), ha='center', va='top', fontsize=9.0, color=INK)

def cell_v(ax, x, y, lab='$V$'):
    ax.plot([x-0.26,x+0.26],[y+0.08,y+0.08], color=INK, lw=1.4, zorder=3)
    ax.plot([x-0.14,x+0.14],[y-0.08,y-0.08], color=INK, lw=3.2, zorder=3)
    ax.annotate(lab, (x-0.34, y), ha='right', va='center', fontsize=9.0, color=INK)

# --- series ---
ax = axes[0]
wire(ax, [(0.35,0.55),(0.35,2.15),(3.65,2.15),(3.65,0.55),(2.08,0.55)])
wire(ax, [(1.92,0.55),(0.35,0.55)])
cell_h(ax, 2.0, 0.55)
for x, lab in [(1.0,'$R_1$'), (2.0,'$R_2$'), (3.0,'$R_3$')]:
    res_h(ax, x, 2.15, lab)
ax.annotate('', xy=(1.60,2.15), xytext=(1.38,2.15),
            arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.5, mutation_scale=11), zorder=4)
ax.annotate('$I$', (1.49,1.88), ha='center', va='top', color=ACCENT, fontsize=9.2)
ax.set_title('series', fontsize=9.6)
ax.set_xlim(-0.25,4.0); ax.set_ylim(-0.1,2.6); ax.axis('off')

# --- parallel: the right-hand rail is itself the third branch ---
ax = axes[1]
wire(ax, [(0.55,0.55),(0.55,1.22)]); wire(ax, [(0.55,1.48),(0.55,2.15)])
cell_v(ax, 0.55, 1.35)
wire(ax, [(0.55,2.15),(3.35,2.15)]); wire(ax, [(0.55,0.55),(3.35,0.55)])
for x, lab in [(1.45,'$R_1$'), (2.40,'$R_2$'), (3.35,'$R_3$')]:
    wire(ax, [(x,2.15),(x,1.66)]); wire(ax, [(x,1.04),(x,0.55)])
    res_v(ax, x, 1.35, lab)
for x in (1.45,2.40):
    ax.plot([x],[2.15],'o',color=INK,ms=4.0,zorder=5)
    ax.plot([x],[0.55],'o',color=INK,ms=4.0,zorder=5)
ax.annotate('', xy=(1.20,2.15), xytext=(0.95,2.15),
            arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.5, mutation_scale=11), zorder=4)
ax.annotate('$I$', (1.07,1.88), ha='center', va='top', color=ACCENT, fontsize=9.2)
ax.set_title('parallel', fontsize=9.6)
ax.set_xlim(-0.25,4.0); ax.set_ylim(-0.1,2.6); ax.axis('off')
```

::: derivation Equivalent resistance in series, $R_{eq} = R_1 + R_2 + R_3$
We start from the two facts that define a series connection and reach the rule
for the single resistor that could replace the three.

**Setting up.** Three resistors $R_1$, $R_2$, $R_3$ are joined end to end across
a supply of p.d. $V$. The p.d. across them are $V_1$, $V_2$, $V_3$.

**Step 1 — state why the current is the same in all three.** There is only one
path, and charge does not pile up anywhere, so whatever flows into $R_1$ must
flow out of $R_3$:

$$ I_1 = I_2 = I_3 = I $$

**Step 2 — state why the voltages add.** Moving from one end of the chain to the
other, the total fall in potential is the sum of the separate falls:

$$ V = V_1 + V_2 + V_3 $$

**Step 3 — write each p.d. from Ohm's law, $V = IR$.**

$$ V_1 = IR_1,\qquad V_2 = IR_2,\qquad V_3 = IR_3 $$

**Step 4 — substitute these into Step 2.**

$$ V = IR_1 + IR_2 + IR_3 $$

**Step 5 — write the same total p.d. for the single equivalent resistor.** By
definition $R_{eq}$ carries the same current $I$ at the same total p.d. $V$:

$$ V = IR_{eq} $$

**Step 6 — set the two expressions for $V$ equal.**

$$ IR_{eq} = IR_1 + IR_2 + IR_3 $$

**Step 7 — divide every term by $I$**, which is the same throughout by Step 1:

$$ R_{eq} = R_1 + R_2 + R_3 $$

**Result.** In series the resistances simply add.

**What it means.** Each extra resistor adds more length of "difficult path", so
the total is always **larger** than the largest single resistor.

**Conditions used.** One single path with nothing joined at the junctions, and
each resistor obeying Ohm's law at the temperature it reaches.
:::

::: derivation Equivalent resistance in parallel, $\dfrac{1}{R_{eq}} = \sum\dfrac{1}{R_i}$
We start from the two facts that define a parallel connection and reach the rule
for the single replacement resistor.

**Setting up.** Three resistors $R_1$, $R_2$, $R_3$ are connected between the
same two points, across a p.d. $V$. They carry currents $I_1$, $I_2$, $I_3$.

**Step 1 — state why the p.d. is the same across all three.** Every resistor has
its two ends joined to the same two points, so each feels the same potential
difference:

$$ V_1 = V_2 = V_3 = V $$

**Step 2 — state why the currents add.** At the junction the incoming current
splits into the three branches, and by Kirchhoff's first law nothing is lost:

$$ I = I_1 + I_2 + I_3 $$

**Step 3 — write each branch current from Ohm's law, $I = V/R$.**

$$ I_1 = \frac{V}{R_1},\qquad I_2 = \frac{V}{R_2},\qquad I_3 = \frac{V}{R_3} $$

**Step 4 — substitute these into Step 2.**

$$ I = \frac{V}{R_1} + \frac{V}{R_2} + \frac{V}{R_3} $$

**Step 5 — write the same total current for the single equivalent resistor.**

$$ I = \frac{V}{R_{eq}} $$

**Step 6 — set the two expressions for $I$ equal.**

$$ \frac{V}{R_{eq}} = \frac{V}{R_1} + \frac{V}{R_2} + \frac{V}{R_3} $$

**Step 7 — divide every term by $V$**, which is the same for all of them by
Step 1:

$$ \frac{1}{R_{eq}} = \frac{1}{R_1} + \frac{1}{R_2} + \frac{1}{R_3} $$

**Step 8 — write the special case of just two resistors.** Add the two fractions
over a common denominator and turn the result upside down:

$$ R_{eq} = \frac{R_1R_2}{R_1 + R_2} $$

**Result.** In parallel the reciprocals add; for two resistors this is "product
over sum".

**What it means.** Each new branch gives the current another road to travel, so
the combination is always **smaller** than the smallest resistor in it. This is
why adding appliances in a house circuit lowers the total resistance and raises
the total current drawn.

**Conditions used.** All the resistors share the same two nodes, the connecting
wires have negligible resistance, and each resistor is ohmic.
:::

In a parallel pair the current divides in the inverse ratio of the resistances:

$$ I_1 = I\,\frac{R_2}{R_1+R_2}, \qquad I_2 = I\,\frac{R_1}{R_1+R_2} $$

::: example Worked example 23.3
**Problem.** A battery of emf $12\ \text{V}$ and negligible internal resistance is
connected to a $2\ \Omega$ resistor in series with a parallel combination of
$3\ \Omega$ and $6\ \Omega$. Find (a) the equivalent resistance, (b) the current
drawn from the battery, and (c) the current in each parallel branch.

**Solution.**

(a) Parallel part: $R_p = \dfrac{3\times6}{3+6} = \dfrac{18}{9} = 2\ \Omega$.
Total: $R_{eq} = 2 + 2 = 4\ \Omega$.

(b) $I = \dfrac{V}{R_{eq}} = \dfrac{12}{4} = 3\ \text{A}$.

(c) Voltage across the parallel section: $V_p = IR_p = 3\times2 = 6\ \text{V}$.
So $I_{3} = 6/3 = 2\ \text{A}$ and $I_{6} = 6/6 = 1\ \text{A}$.

Check: $2 + 1 = 3\ \text{A}$, as required.
:::

### Kirchhoff's laws

Many networks — a bridge, or two cells feeding one resistor — cannot be reduced
by series and parallel rules at all. Kirchhoff's two laws solve every such
network.

::: key Kirchhoff's laws
**First law (junction law).** The algebraic sum of the currents meeting at any
junction is zero: $\sum I = 0$. Currents entering the junction are taken positive
and those leaving negative. *This is conservation of charge* — charge does not
pile up at a junction.

**Second law (loop law).** In any closed loop, the algebraic sum of the emfs
equals the algebraic sum of the $IR$ products:
$\sum E = \sum IR$. *This is conservation of energy* — a unit charge taken once
round a loop returns to the same potential.
:::

::: memory Sign rules that never fail
1. Choose a direction for each unknown current and mark it. A negative answer
   simply means the real current is the other way.
2. Go round the loop in one fixed sense (say clockwise).
3. A resistance traversed **along** the assumed current gives $+IR$; against it,
   $-IR$.
4. A cell traversed from $-$ to $+$ inside it gives $+E$; from $+$ to $-$ gives $-E$.
:::

```figure caption="A two-loop network. Applying the junction law at B gives $I_3 = I_1 + I_2$; the loop law applied to loops 1 and 2 then fixes both currents."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(5.0,2.9))

def wire(pts, lw=1.3):
    p = np.array(pts, float); ax.plot(p[:,0], p[:,1], color=INK, lw=lw, zorder=2)

def res_v(x, y, lab, w=0.26, h=0.62):
    ax.add_patch(Rectangle((x-w/2,y-h/2), w, h, fc='white', ec=INK, lw=1.2, zorder=3))
    ax.annotate(lab, (x+w/2+0.10, y), ha='left', va='center', fontsize=9.0, color=INK)

def cell_h(x, y, lab):
    ax.plot([x-0.08,x-0.08],[y-0.30,y+0.30], color=INK, lw=1.4, zorder=3)
    ax.plot([x+0.08,x+0.08],[y-0.16,y+0.16], color=INK, lw=3.2, zorder=3)
    ax.annotate(lab, (x, y+0.40), ha='center', fontsize=9.0, color=INK)

wire([(0.3,2.3),(4.7,2.3)]); wire([(0.3,0.5),(4.7,0.5)])
wire([(0.3,0.5),(0.3,2.3)]); wire([(4.7,0.5),(4.7,2.3)])
wire([(2.5,0.5),(2.5,1.09)]); wire([(2.5,1.71),(2.5,2.3)])
res_v(2.5, 1.4, '$R$')

cell_h(1.05, 2.3, '$E_1,\\ r_1$')
cell_h(3.95, 2.3, '$E_2,\\ r_2$')

for x, y, lab, off in [(2.5,2.3,'B',(0.14,0.16)), (2.5,0.5,'C',(0.14,-0.26))]:
    ax.plot([x],[y],'o', color=INK, ms=4.5, zorder=5)
    ax.annotate(lab, (x+off[0], y+off[1]), fontsize=9.4, color=INK)

ax.annotate('', xy=(2.15,2.3), xytext=(1.70,2.3),
            arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.5, mutation_scale=11), zorder=6)
ax.annotate('$I_1$', (1.92,2.42), ha='center', color=ACCENT, fontsize=9.4)
ax.annotate('', xy=(2.85,2.3), xytext=(3.30,2.3),
            arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.5, mutation_scale=11), zorder=6)
ax.annotate('$I_2$', (3.08,2.42), ha='center', color=ACCENT, fontsize=9.4)
ax.annotate('', xy=(2.5,1.72), xytext=(2.5,2.16),
            arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.5, mutation_scale=11), zorder=6)
ax.annotate('$I_3$', (2.36,1.95), ha='right', va='center', color=ACCENT, fontsize=9.4)

ax.annotate('loop 1', (1.42,1.38), ha='center', fontsize=9.2, color=MUTED)
ax.annotate('loop 2', (3.58,1.38), ha='center', fontsize=9.2, color=MUTED)
ax.set_xlim(-0.1,5.1); ax.set_ylim(0.05,2.9); ax.axis('off')
```

::: example Worked example 23.4
**Problem.** In the network of the figure, $E_1 = 8\ \text{V}$ with
$r_1 = 1\ \Omega$ (left branch), $E_2 = 10\ \text{V}$ with $r_2 = 4\ \Omega$
(right branch), and the middle branch BC is a $R = 2\ \Omega$ resistor. Find the
current in each branch.

**Solution.** Let $I_1$ and $I_2$ flow towards B in the left and right branches.
By the junction law at B the middle branch carries $I_3 = I_1 + I_2$ downwards.

Loop 1 (left cell and $R$):

$$ E_1 = I_1r_1 + I_3R \;\Rightarrow\; 8 = I_1 + 2(I_1+I_2) = 3I_1 + 2I_2 $$

Loop 2 (right cell and $R$):

$$ E_2 = I_2r_2 + I_3R \;\Rightarrow\; 10 = 4I_2 + 2(I_1+I_2) = 2I_1 + 6I_2 $$

From the first, $I_2 = (8-3I_1)/2$. Substituting in the second:

$$ 2I_1 + 3(8-3I_1) = 10 \;\Rightarrow\; -7I_1 = -14 \;\Rightarrow\; I_1 = 2\ \text{A} $$

Then $I_2 = (8-6)/2 = 1\ \text{A}$ and $I_3 = 3\ \text{A}$.

Check with energy: the cells supply $8(2) + 10(1) = 26\ \text{W}$; the resistors
dissipate $2^{2}(1) + 1^{2}(4) + 3^{2}(2) = 4 + 4 + 18 = 26\ \text{W}$.
:::

### The Wheatstone bridge

The Wheatstone bridge is the standard way of measuring an unknown resistance
accurately, because at balance the answer depends only on a *ratio* — no ammeter
or voltmeter reading is needed.

```figure caption="The Wheatstone bridge balances when $P/Q = R/S$; the metre bridge is its practical form, balanced by sliding the jockey along a uniform 1 m wire."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
fig, axes = plt.subplots(1, 2, figsize=(5.2,2.9))

def wire(ax, pts, lw=1.3):
    p = np.array(pts, float); ax.plot(p[:,0], p[:,1], color=INK, lw=lw, zorder=2)

def rot_res(ax, p0, p1, lab, w=0.30, off=(0,0)):
    p0 = np.array(p0, float); p1 = np.array(p1, float)
    d = p1-p0; L = np.hypot(*d); u = d/L; nv = np.array([-u[1],u[0]])
    a = p0 + u*(L/2 - 0.42) - nv*w/2
    ang = np.degrees(np.arctan2(d[1], d[0]))
    ax.add_patch(Rectangle(tuple(a), 0.84, w, angle=ang, fc='white', ec=INK, lw=1.2, zorder=3))
    m = p0 + u*L/2
    ax.annotate(lab, (m[0]+off[0], m[1]+off[1]), ha='center', va='center',
                fontsize=9.2, color=INK, zorder=5)

def galv(ax, x, y, r=0.21):
    ax.add_patch(Circle((x,y), r, fc='white', ec=INK, lw=1.2, zorder=4))
    ax.annotate('G', (x,y), ha='center', va='center', fontsize=8.6, color=INK, zorder=5)

def cell_h(ax, x, y):
    ax.plot([x-0.08,x-0.08],[y-0.28,y+0.28], color=INK, lw=1.4, zorder=3)
    ax.plot([x+0.08,x+0.08],[y-0.15,y+0.15], color=INK, lw=3.2, zorder=3)

# --- Wheatstone bridge (diamond), galvanometer between B and D ---
ax = axes[0]
A=(0.35,1.45); B=(1.85,2.45); C=(3.35,1.45); D=(1.85,0.45)
for p,q in [(A,B),(B,C),(A,D),(D,C)]:
    wire(ax,[p,q])
rot_res(ax, A,B,'$P$', off=(-0.26,0.26)); rot_res(ax, B,C,'$Q$', off=(0.26,0.26))
rot_res(ax, A,D,'$R$', off=(-0.26,-0.26)); rot_res(ax, D,C,'$S$', off=(0.26,-0.26))
wire(ax,[(1.85,2.45),(1.85,1.66)]); wire(ax,[(1.85,1.24),(1.85,0.45)])
galv(ax, 1.85, 1.45)
wire(ax,[A,(0.35,-0.35),(1.77,-0.35)]); wire(ax,[(1.93,-0.35),(3.35,-0.35),C])
wire(ax,[(3.35,-0.35),(3.35,1.45)])
cell_h(ax, 1.85, -0.35)
ax.annotate('$E$', (1.85,-0.62), ha='center', va='top', fontsize=9.2, color=INK)
for p,lab,off in [(A,'A',(-0.22,0.0)),(B,'B',(0.0,0.22)),(C,'C',(0.22,0.0)),(D,'D',(0.22,-0.14))]:
    ax.plot([p[0]],[p[1]],'o',color=INK,ms=4.2,zorder=5)
    ax.annotate(lab,(p[0]+off[0],p[1]+off[1]), ha='center', va='center', fontsize=9.4, color=INK)
ax.set_xlim(-0.2,3.9); ax.set_ylim(-0.95,2.9); ax.axis('off')
ax.set_title('Wheatstone bridge', fontsize=9.4)

# --- metre bridge ---
ax = axes[1]
ax.add_patch(Rectangle((0.3,0.55), 3.3, 0.16, fc='#e8edf4', ec=INK, lw=1.1, zorder=2))
for xx, t in [(0.3,'0'),(1.95,'50'),(3.6,'100')]:
    ax.plot([xx,xx],[0.40,0.55], color=MUTED, lw=0.9)
    ax.annotate(t,(xx,0.20), ha='center', va='top', fontsize=8.0, color=MUTED)
ax.annotate('metre wire (cm)', (1.95,-0.10), ha='center', va='top', fontsize=8.2, color=MUTED)
wire(ax,[(0.3,0.63),(0.3,2.25),(1.28,2.25)]); wire(ax,[(2.12,2.25),(3.6,2.25),(3.6,0.63)])
ax.add_patch(Rectangle((0.62,2.10), 0.78, 0.30, fc='white', ec=INK, lw=1.2, zorder=3))
ax.annotate('$X$', (1.01,2.52), ha='center', fontsize=9.2, color=INK)
ax.add_patch(Rectangle((2.42,2.10), 0.78, 0.30, fc='white', ec=INK, lw=1.2, zorder=3))
ax.annotate('$R$', (2.81,2.52), ha='center', fontsize=9.2, color=INK)
wire(ax,[(1.40,2.25),(2.12,2.25)])
ax.plot([1.95],[2.25],'o',color=INK,ms=4.2,zorder=5)
wire(ax,[(1.95,2.25),(1.95,1.73)])
galv(ax, 1.95, 1.52)
wire(ax,[(1.95,1.31),(1.95,1.05),(1.42,1.05),(1.42,0.78)])
ax.annotate('', xy=(1.42,0.72), xytext=(1.42,0.98),
            arrowprops=dict(arrowstyle='-|>', color='#d9534f', lw=1.4, mutation_scale=10), zorder=4)
ax.annotate('jockey', (1.36,1.25), ha='right', va='center', fontsize=8.2, color='#d9534f')
wire(ax,[(0.3,0.63),(0.3,-0.75),(1.77,-0.75)]); wire(ax,[(1.93,-0.75),(3.6,-0.75),(3.6,0.63)])
cell_h(ax, 1.85, -0.75)
ax.annotate('$l$', (0.80,0.76), ha='center', va='bottom', fontsize=9.2, color=INK)
ax.annotate('$100-l$', (2.70,0.76), ha='center', va='bottom', fontsize=9.2, color=INK)
ax.set_xlim(-0.15,4.0); ax.set_ylim(-1.15,2.9); ax.axis('off')
ax.set_title('metre bridge', fontsize=9.4)
```

::: derivation Balance condition of the Wheatstone bridge, $\dfrac{P}{Q} = \dfrac{R}{S}$
We start from the fact that the galvanometer reads zero and reach a simple
relation between the four arm resistances.

**Setting up.** Four resistances $P$, $Q$, $R$, $S$ form the arms AB, BC, AD and
DC of a diamond. A galvanometer joins B to D, and a cell is connected across A
and C. The bridge is called **balanced** when the galvanometer shows no
deflection.

**Step 1 — say what "no deflection" means for the potentials.** No current flows
through the galvanometer only if there is no potential difference driving it, so
B and D must be at the same potential:

$$ V_B = V_D $$

**Step 2 — follow the currents.** Since nothing leaks away at B into the
galvanometer, the current $I_1$ that enters through $P$ carries straight on
through $Q$. In the same way the current $I_2$ through $R$ carries on through
$S$.

**Step 3 — write the p.d. across the two upper arms.** Ohm's law gives

$$ V_A - V_B = I_1P \qquad\text{and}\qquad V_A - V_D = I_2R $$

**Step 4 — these two are equal, because $V_B = V_D$ from Step 1.**

$$ I_1P = I_2R \qquad (1) $$

**Step 5 — write the p.d. across the two lower arms.**

$$ V_B - V_C = I_1Q \qquad\text{and}\qquad V_D - V_C = I_2S $$

**Step 6 — these two are also equal, for the same reason.**

$$ I_1Q = I_2S \qquad (2) $$

**Step 7 — divide equation (1) by equation (2).** Both sides are non-zero, so
the division is allowed:

$$ \frac{I_1P}{I_1Q} = \frac{I_2R}{I_2S} $$

**Step 8 — cancel $I_1$ on the left and $I_2$ on the right.**

$$ \frac{P}{Q} = \frac{R}{S} $$

**Step 9 — rearrange to find the unknown arm.** If $P$, $Q$ and $R$ are known
and $S$ is the unknown, cross-multiply and divide:

$$ S = \frac{QR}{P} $$

**Result.** The bridge is balanced when $P/Q = R/S$, and the unknown resistance
is then $S = QR/P$.

**What it means.** The currents $I_1$ and $I_2$ cancelled, so the answer does
not depend on the emf of the cell, on its internal resistance, or on the
resistance of the galvanometer and the leads. Only a *ratio* of resistances is
measured, which is why the method is so accurate.

**Conditions used.** The galvanometer must read exactly zero (true balance), all
four arms must be ohmic, and the resistances must not drift as they warm up.
:::

::: tip The examiner is looking for
1. A labelled diagram of the diamond with $P, Q, R, S$, the galvanometer between
   B and D, and the cell across A and C.
2. The statement $V_B = V_D$ at balance, with the reason.
3. The two current paths $I_1$ through $P$ and $Q$, $I_2$ through $R$ and $S$.
4. The two equations $I_1P = I_2R$ and $I_1Q = I_2S$.
5. Dividing one by the other and cancelling the currents to get $P/Q = R/S$.
:::

::: tip Why balance methods beat direct measurement
At balance the galvanometer carries no current, so its resistance, the resistance
of the connecting wires and the emf and internal resistance of the cell **do not
enter the answer at all**. Only a ratio of resistances does. That is why bridge
and potentiometer methods are called *null methods* and are far more accurate
than an ammeter–voltmeter measurement.
:::

### The metre bridge

The metre bridge is the Wheatstone bridge built around a uniform resistance wire
exactly one metre long. The unknown $X$ is put in the left gap and a resistance
box $R$ in the right gap; the two parts of the wire on either side of the jockey
replace the other two arms. Because the wire is uniform, its resistance is
proportional to its length, so if the balance point is at $l$ cm from the left end,

$$ \frac{X}{R} = \frac{l}{100-l} \;\Longrightarrow\; X = R\,\frac{l}{100-l} $$

::: example Worked example 23.5
**Problem.** In a metre bridge the unknown resistance $X$ is in the left gap and
a $5\ \Omega$ resistance box in the right gap. The balance point is found at
$60\ \text{cm}$ from the left end. (a) Find $X$. (b) $X$ is a wire of length
$1.0\ \text{m}$ and diameter $0.40\ \text{mm}$; find its resistivity.

**Solution.**

(a)

$$ X = R\,\frac{l}{100-l} = 5\times\frac{60}{40} = 7.5\ \Omega $$

(b) $A = \pi r^{2} = \pi(0.20\times10^{-3})^{2} = 1.26\times10^{-7}\ \text{m}^{2}$.

$$ \rho = \frac{XA}{l} = \frac{7.5\times1.26\times10^{-7}}{1.0} = 9.4\times10^{-7}\ \Omega\ \text{m} $$
:::

::: caution Keep the balance point near the middle
Take readings with $l$ between about $40$ and $60\ \text{cm}$ by choosing a
suitable $R$. Near the ends, a small error in $l$ produces a large percentage
error in $X$, and the unaccounted resistance of the end connections (end error)
matters most there.
:::

### Converting a galvanometer into an ammeter and a voltmeter

A galvanometer is a sensitive current detector with resistance $G$ that gives
full-scale deflection for a very small current $I_g$. Series and parallel
combinations turn it into a practical meter.

**Ammeter.** Connect a small resistance $S$ (a **shunt**) in parallel, so that
most of the current bypasses the coil. If the meter is to read up to $I$, then the
shunt carries $I - I_g$ and, since both have the same potential difference,

$$ I_gG = (I-I_g)S \;\Longrightarrow\; S = \frac{I_gG}{I-I_g} $$

**Voltmeter.** Connect a large resistance $R$ (a **multiplier**) in series, so
that only $I_g$ flows when the full voltage $V$ is applied:

$$ V = I_g(G+R) \;\Longrightarrow\; R = \frac{V}{I_g} - G $$

| | Ammeter | Voltmeter |
|---|---|---|
| Made by | low shunt in parallel | high multiplier in series |
| Connected | in series with the element | in parallel with the element |
| Ideal resistance | zero | infinite |
| Effect of a real meter | slightly reduces the current | slightly reduces the pd |

::: example Worked example 23.6
**Problem.** A galvanometer of resistance $100\ \Omega$ gives full-scale
deflection for $1.0\ \text{mA}$. Convert it into (a) an ammeter reading
$0-1.0\ \text{A}$ and (b) a voltmeter reading $0-10\ \text{V}$.

**Solution.**

(a)

$$ S = \frac{I_gG}{I-I_g} = \frac{(1.0\times10^{-3})(100)}{1.0-1.0\times10^{-3}}
= \frac{0.100}{0.999} = 0.100\ \Omega $$

so a shunt of about $0.1\ \Omega$ is connected in parallel.

(b)

$$ R = \frac{V}{I_g} - G = \frac{10}{1.0\times10^{-3}} - 100 = 10000 - 100 = 9900\ \Omega $$

so a $9900\ \Omega$ multiplier is connected in series.
:::

## 23.5 Potential divider

Two resistors in series across a supply form a **potential divider** (voltage
divider). The supply voltage divides between them in the ratio of their
resistances, so the output taken across $R_2$ is

$$ V_{out} = V_{in}\,\frac{R_2}{R_1+R_2} $$

If the two resistors are the two parts of a single uniform wire or a track with a
sliding contact, $V_{out}$ can be varied continuously from $0$ to $V_{in}$ — this
is how a volume control works. A **rheostat** (two terminals) can only reduce the
voltage down to a limit set by the load; a potential divider (three terminals)
can take the output all the way down to zero, which is why it is preferred.

```figure caption="Left: a potential divider gives $V_{out} = V_{in}R_2/(R_1+R_2)$. Right: the potentiometer — the jockey J is moved until the galvanometer reads zero."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
fig, axes = plt.subplots(1, 2, figsize=(5.2,2.9))

def wire(ax, pts, lw=1.3):
    p = np.array(pts, float); ax.plot(p[:,0], p[:,1], color=INK, lw=lw, zorder=2)

def res_v(ax, x, y, lab, w=0.28, h=0.62):
    ax.add_patch(Rectangle((x-w/2,y-h/2), w, h, fc='white', ec=INK, lw=1.2, zorder=3))
    ax.annotate(lab, (x+w/2+0.10, y), ha='left', va='center', fontsize=9.2, color=INK)

def galv(ax, x, y, r=0.21):
    ax.add_patch(Circle((x,y), r, fc='white', ec=INK, lw=1.2, zorder=4))
    ax.annotate('G', (x,y), ha='center', va='center', fontsize=8.6, color=INK, zorder=5)

def cell_v(ax, x, y):          # cell in a vertical wire: plates horizontal
    ax.plot([x-0.26,x+0.26],[y+0.08,y+0.08], color=INK, lw=1.4, zorder=3)
    ax.plot([x-0.14,x+0.14],[y-0.08,y-0.08], color=INK, lw=3.2, zorder=3)

def cell_h(ax, x, y):          # cell in a horizontal wire: plates vertical
    ax.plot([x-0.08,x-0.08],[y-0.28,y+0.28], color=INK, lw=1.4, zorder=3)
    ax.plot([x+0.08,x+0.08],[y-0.15,y+0.15], color=INK, lw=3.2, zorder=3)

# --- potential divider ---
ax = axes[0]
wire(ax,[(0.55,0.35),(0.55,1.22)]); wire(ax,[(0.55,1.48),(0.55,2.35),(1.75,2.35)])
cell_v(ax, 0.55, 1.35)
ax.annotate('$V_{in}$', (0.24,1.35), ha='right', va='center', fontsize=9.2, color=INK)
wire(ax,[(1.75,2.35),(1.75,1.91)]); res_v(ax, 1.75, 1.60, '$R_1$')
wire(ax,[(1.75,1.29),(1.75,1.01)]); res_v(ax, 1.75, 0.70, '$R_2$')
wire(ax,[(1.75,0.39),(1.75,0.35),(0.55,0.35)])
wire(ax,[(1.75,1.15),(2.85,1.15)]); wire(ax,[(1.75,0.35),(2.85,0.35)])
ax.plot([1.75],[1.15],'o',color=INK,ms=4.2,zorder=5)
ax.plot([2.85,2.85],[1.15,0.35],'o',color=INK,ms=4.2,zorder=5,fillstyle='none')
ax.annotate('', xy=(3.05,0.42), xytext=(3.05,1.08),
            arrowprops=dict(arrowstyle='<|-|>', color=ACCENT, lw=1.2, mutation_scale=9))
ax.annotate('$V_{out}$', (3.16,0.75), ha='left', va='center', fontsize=9.2, color=ACCENT)
ax.set_xlim(-0.15,4.0); ax.set_ylim(-0.1,2.8); ax.axis('off')
ax.set_title('potential divider', fontsize=9.4)

# --- potentiometer ---
ax = axes[1]
ax.add_patch(Rectangle((0.35,0.55), 3.1, 0.16, fc='#e8edf4', ec=INK, lw=1.1, zorder=2))
ax.annotate('A', (0.20,0.63), ha='right', va='center', fontsize=9.4, color=INK)
ax.annotate('B', (3.60,0.63), ha='left', va='center', fontsize=9.4, color=INK)
wire(ax,[(0.35,0.63),(0.35,2.25),(1.77,2.25)]); wire(ax,[(1.93,2.25),(3.45,2.25),(3.45,0.63)])
cell_h(ax, 1.85, 2.25)
ax.annotate('driver cell  $E_0$', (1.85,2.50), ha='center', va='bottom', fontsize=8.6, color=INK)
wire(ax,[(0.35,0.63),(0.35,-0.70),(1.17,-0.70)])
cell_h(ax, 1.25, -0.70)
ax.annotate('$E$', (1.25,-0.98), ha='center', va='top', fontsize=9.2, color=INK)
wire(ax,[(1.33,-0.70),(2.09,-0.70)])
galv(ax, 2.30, -0.70)
wire(ax,[(2.51,-0.70),(2.85,-0.70),(2.85,0.12),(2.25,0.12),(2.25,0.48)])
ax.annotate('', xy=(2.25,0.53), xytext=(2.25,0.22),
            arrowprops=dict(arrowstyle='-|>', color='#d9534f', lw=1.4, mutation_scale=10), zorder=4)
ax.annotate('J', (2.12,0.30), ha='right', va='center', fontsize=9.4, color='#d9534f')
ax.annotate('', xy=(2.25,0.92), xytext=(0.35,0.92),
            arrowprops=dict(arrowstyle='<|-|>', color=ACCENT, lw=1.1, mutation_scale=9))
ax.annotate('$l$', (1.30,1.02), ha='center', va='bottom', fontsize=9.2, color=ACCENT)
ax.set_xlim(-0.2,4.0); ax.set_ylim(-1.35,2.8); ax.axis('off')
ax.set_title('potentiometer', fontsize=9.4)
```

### The potentiometer

A potentiometer is a potential divider made from a long uniform resistance wire
AB (usually 4 m or 10 m of manganin, arranged in 1 m lengths) carrying a steady
current from a driver cell of emf $E_0$. Because the wire is uniform, the
potential falls uniformly along it. The **potential gradient** is

$$ k = \frac{\text{pd across AB}}{\text{length AB}} \qquad (\text{V m}^{-1}) $$

and the pd across the first $l$ metres is $V = kl$.

::: key Principle of the potentiometer
The cell being tested is connected with its positive terminal to A, through a
galvanometer to the jockey. The jockey is slid until the galvanometer reads
**zero**. At that balance point the cell drives no current, so the pd it would
supply is exactly balanced by the pd $kl$ across the wire, and the reading is the
cell's **emf**, not its terminal pd:
$$ E = kl $$
:::

**Comparison of two emfs.** Balancing the two cells separately at lengths $l_1$
and $l_2$ gives $E_1 = kl_1$ and $E_2 = kl_2$, hence

$$ \frac{E_1}{E_2} = \frac{l_1}{l_2} $$

**Internal resistance of a cell.** First balance the cell on open circuit at
length $l_1$, so $E = kl_1$. Then close a known resistance $R$ across the cell and
re-balance at $l_2$, so the terminal pd is $V = kl_2$. Since $E = I(R+r)$ and
$V = IR$,

$$ \frac{E}{V} = \frac{R+r}{R} = \frac{l_1}{l_2}
\;\Longrightarrow\; r = R\left(\frac{l_1-l_2}{l_2}\right) $$

::: example Worked example 23.7
**Problem.** A potentiometer wire AB is $10.0\ \text{m}$ long and the whole
$2.0\ \text{V}$ of the driver cell falls across it. A cell connected in the
secondary circuit balances at $7.50\ \text{m}$ from A. When a $4.0\ \Omega$
resistor is connected across this cell, the balance length becomes
$6.00\ \text{m}$. Find (a) the potential gradient, (b) the emf of the cell and
(c) its internal resistance.

**Solution.**

(a) $k = \dfrac{2.0}{10.0} = 0.20\ \text{V m}^{-1}$.

(b) $E = kl_1 = 0.20\times7.50 = 1.50\ \text{V}$.

(c) Terminal pd $V = kl_2 = 0.20\times6.00 = 1.20\ \text{V}$, so

$$ r = R\left(\frac{l_1-l_2}{l_2}\right) = 4.0\times\frac{7.50-6.00}{6.00}
= 4.0\times0.25 = 1.0\ \Omega $$
:::

::: caution The potentiometer will not balance if...
...the positive terminals of the driver cell and the test cell are not both
connected to the same end A, or if the emf of the test cell is greater than the
pd across the whole wire. In both cases the galvanometer deflects the same way at
every point of the wire — that is the symptom to recognise in the lab.
:::

## 23.6 Electromotive force of a source, internal resistance

::: definition emf and terminal potential difference
The **electromotive force** $E$ of a source is the energy given to each coulomb
of charge driven round the complete circuit; it equals the pd across the
terminals of the source on **open circuit**. The **terminal potential difference**
$V$ is the pd across the terminals when the source is actually delivering current.
Both are measured in volts; emf is not a force.
:::

Every real cell has some resistance of its own — the resistance of its
electrolyte and electrodes — called the **internal resistance** $r$. When the
cell drives a current, part of the emf is used up inside the cell itself.

::: derivation Terminal potential difference of a cell, $V = E - Ir$
We start from the energy given to each coulomb by the cell and reach a formula
for the voltage you would actually measure across its terminals.

**Setting up.** A cell of emf $E$ and internal resistance $r$ drives a steady
current $I$ through an external resistance $R$. The emf is the energy the cell
gives to each coulomb; that energy has to be shared between the two resistances
the charge meets.

**Step 1 — apply conservation of energy per coulomb around the loop.** The
energy supplied to each coulomb equals the energy it gives up in the outside
circuit plus the energy it gives up inside the cell:

$$ E = (\text{p.d. across } R) + (\text{p.d. across } r) $$

**Step 2 — write each p.d. from Ohm's law.** The same current $I$ passes through
both, since the cell and $R$ are in one single loop:

$$ E = IR + Ir $$

**Step 3 — take $I$ out as a common factor and solve for the current.**

$$ E = I(R + r)\quad\Longrightarrow\quad I = \frac{E}{R + r} $$

**Step 4 — say what the voltmeter across the terminals actually reads.** The
terminals are the two ends of $R$, so the terminal p.d. is

$$ V = IR $$

**Step 5 — go back to Step 2 and make $IR$ the subject.** Subtract $Ir$ from
both sides:

$$ IR = E - Ir $$

**Step 6 — replace $IR$ by $V$, using Step 4.**

$$ V = E - Ir $$

**Result.** The terminal potential difference is $V = E - Ir$, and the current
in the circuit is $I = E/(R+r)$.

**What it means.** The term $Ir$ is the "lost volts" — the part of the emf spent
pushing the current through the cell's own resistance. It also gives a way to
measure $E$ and $r$: a graph of $V$ against $I$ is a straight line whose
intercept is $E$ and whose slope is $-r$.

**Conditions used.** A steady current in a single loop; $E$ and $r$ treated as
constant (in a real cell $r$ grows as the cell ages); and the cell is
discharging. If the cell is being **charged**, the current is reversed and
$V = E + Ir$ instead.
:::

So the terminal pd is always **less** than the emf while the cell is discharging,
and the graph of $V$ against $I$ is a straight line of intercept $E$ and slope
$-r$. If the terminals are short-circuited ($R = 0$), the current is limited only
by $r$: $I_{max} = E/r$. This is why a "dead" torch cell, whose $r$ has grown
large, still shows nearly $1.5\ \text{V}$ on a voltmeter but cannot light a bulb.

| Connection | Equivalent emf | Equivalent internal resistance | Use when |
|---|---|---|---|
| $n$ identical cells in series | $nE$ | $nr$ | $R$ is much larger than $r$ |
| $n$ identical cells in parallel | $E$ | $r/n$ | $R$ is much smaller than $r$ |

::: example Worked example 23.8
**Problem.** A cell gives a terminal pd of $1.40\ \text{V}$ when it supplies
$0.40\ \text{A}$, and $1.20\ \text{V}$ when it supplies $0.80\ \text{A}$. Find the
emf and internal resistance of the cell, and the current if its terminals were
short-circuited.

**Solution.** Using $V = E - Ir$ twice:

$$ 1.40 = E - 0.40r, \qquad 1.20 = E - 0.80r $$

Subtracting the second from the first: $0.20 = 0.40r$, so $r = 0.50\ \Omega$.
Then $E = 1.40 + 0.40(0.50) = 1.60\ \text{V}$.

Short-circuit current: $I = E/r = 1.60/0.50 = 3.2\ \text{A}$.
:::

## 23.7 Work and power in electrical circuits

::: derivation Electrical power, $P = VI = I^{2}R = \dfrac{V^{2}}{R}$
We start from the definition of potential difference and reach the three forms
of the power formula.

**Setting up.** A steady current $I$ flows for a time $t$ through a resistor $R$
across which the potential difference is $V$.

**Step 1 — use the definition of potential difference.** Potential difference is
work done per unit charge, so the work done on a charge $Q$ falling through $V$
is

$$ W = QV $$

**Step 2 — express the charge in terms of the current.** Current is charge per
second, so in a time $t$ a steady current $I$ carries

$$ Q = It $$

**Step 3 — substitute this into Step 1.**

$$ W = VIt $$

**Step 4 — divide by the time to get the power.** Power is work done per second:

$$ P = \frac{W}{t} = \frac{VIt}{t} $$

**Step 5 — cancel $t$.**

$$ P = VI $$

**Step 6 — get the second form.** For an ohmic resistor, Ohm's law gives
$V = IR$; put that in place of $V$:

$$ P = (IR)I $$

**Step 7 — multiply out.**

$$ P = I^{2}R $$

**Step 8 — get the third form.** Start again from $P = VI$ and this time replace
$I$ by $V/R$:

$$ P = V\left(\frac{V}{R}\right) $$

**Step 9 — multiply out.**

$$ P = \frac{V^{2}}{R} $$

**Result.**

$$ P = VI = I^{2}R = \frac{V^{2}}{R} $$

and the heat produced in a time $t$ is $H = I^{2}Rt$.

**What it means.** All three expressions give the same number for the same
resistor — choose whichever uses the two quantities you already know. In a
series circuit the current is common, so $P = I^{2}R$ is the quick one; in a
parallel circuit the voltage is common, so $P = V^{2}/R$ is.

**Conditions used.** Steady current and steady p.d.; and Steps 6 to 9 need the
element to be **ohmic**, so that $V = IR$ holds. The general form $P = VI$ works
for any device, ohmic or not.
:::

For a source of emf $E$ delivering current $I$, the total power generated is
$P = EI$; of this, $I^{2}r$ is wasted inside the source and $VI = I^2R$ reaches
the external circuit.

::: key Joule's law of heating
In a pure resistance all the electrical work appears as heat:
$$ H = I^{2}Rt \quad \text{joules} $$
The heat produced is proportional to (i) the square of the current, (ii) the
resistance, and (iii) the time. In calories, $H = I^{2}Rt/4.2$.
:::

::: tip Which form of $P$ to use
Use $P = I^{2}R$ when the elements are in **series** (same $I$): the largest
resistance dissipates most power. Use $P = V^{2}/R$ when they are in **parallel**
(same $V$): the smallest resistance dissipates most power. Choosing the right form
makes "which bulb is brighter?" questions immediate.
:::

::: caution The 100 W bulb is not always the brighter one
Two bulbs rated $100\ \text{W}$ and $60\ \text{W}$ at $220\ \text{V}$ have
resistances $484\ \Omega$ and $807\ \Omega$. Joined **in series**, the same
current flows, so $P = I^2R$ makes the $60\ \text{W}$ bulb glow brighter. Power
ratings only hold at the rated voltage.
:::

Electrical energy is sold in **kilowatt-hours**: $1\ \text{kWh} = 1000\ \text{W}
\times 3600\ \text{s} = 3.6\times10^{6}\ \text{J}$. This is the "unit" on a NEA
bill.

::: example Worked example 23.9
**Problem.** An electric heater is marked $1500\ \text{W}$, $220\ \text{V}$.
(a) Find its resistance and the current it draws. (b) How long does it take to
heat $2.0\ \text{kg}$ of water from $20\ ^{\circ}\text{C}$ to
$100\ ^{\circ}\text{C}$, assuming no heat is lost? Take
$c = 4200\ \text{J kg}^{-1}\ ^{\circ}\text{C}^{-1}$. (c) If it runs $2$ hours a
day for $30$ days, what does it cost at Rs $10$ per unit?

**Solution.**

(a) $R = \dfrac{V^{2}}{P} = \dfrac{220^{2}}{1500} = \dfrac{48400}{1500} = 32.3\ \Omega$;
$I = \dfrac{P}{V} = \dfrac{1500}{220} = 6.8\ \text{A}$.

(b) Heat needed: $Q = mc\Delta\theta = 2.0\times4200\times80 = 6.72\times10^{5}\ \text{J}$.

$$ t = \frac{Q}{P} = \frac{6.72\times10^{5}}{1500} = 448\ \text{s} \approx 7.5\ \text{min} $$

(c) Energy $= 1.5\ \text{kW}\times2\ \text{h}\times30 = 90\ \text{kWh}$, so the
cost is $90\times10 =$ Rs $900$.
:::

## Chapter summary

- Current is $I = dQ/dt$; in a metal $I = nAv_de$ and $J = I/A = nev_d$, with a
  drift velocity of order $10^{-4}\ \text{m s}^{-1}$.
- Ohm's law: $V = IR$ at constant temperature. $R = \rho l/A$,
  $\sigma = 1/\rho$, and microscopically $\rho = m/(ne^{2}\tau)$.
- Ohmic conductors give a straight $I$–$V$ line through the origin; lamps, diodes
  and thermistors are non-ohmic.
- Series: $R_{eq} = R_1+R_2+R_3$. Parallel: $1/R_{eq} = 1/R_1+1/R_2+1/R_3$.
- Kirchhoff: $\sum I = 0$ at a junction (charge conservation);
  $\sum E = \sum IR$ round a loop (energy conservation).
- Wheatstone bridge balances when $P/Q = R/S$; the metre bridge form is
  $X = Rl/(100-l)$.
- Galvanometer to ammeter: shunt $S = I_gG/(I-I_g)$ in parallel. To voltmeter:
  multiplier $R = V/I_g - G$ in series.
- Potential divider: $V_{out} = V_{in}R_2/(R_1+R_2)$. Potentiometer: $E = kl$,
  $E_1/E_2 = l_1/l_2$, and $r = R(l_1-l_2)/l_2$.
- For a source, $I = E/(R+r)$ and $V = E - Ir$; power $P = VI = I^{2}R = V^{2}/R$
  and heat $H = I^{2}Rt$.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The drift velocity of free electrons in a copper wire carrying a normal
   current is of the order of <span class="marks">[1]</span>
   (a) $10^{8}\ \text{m s}^{-1}$ (b) $10^{5}\ \text{m s}^{-1}$ (c) $10^{-4}\ \text{m s}^{-1}$ (d) $10^{-10}\ \text{m s}^{-1}$
2. A wire of resistance $R$ is stretched uniformly until its length is doubled.
   Its new resistance is <span class="marks">[1]</span>
   (a) $R/2$ (b) $2R$ (c) $4R$ (d) $R/4$
3. Three resistors of $6\ \Omega$ each are connected in parallel. The equivalent
   resistance is <span class="marks">[1]</span>
   (a) $18\ \Omega$ (b) $6\ \Omega$ (c) $3\ \Omega$ (d) $2\ \Omega$
4. Kirchhoff's junction law is a statement of the conservation of <span class="marks">[1]</span>
   (a) energy (b) charge (c) momentum (d) mass
5. A galvanometer is converted into an ammeter by connecting <span class="marks">[1]</span>
   (a) a high resistance in series (b) a low resistance in series
   (c) a high resistance in parallel (d) a low resistance in parallel
6. A $100\ \text{W}$ and a $60\ \text{W}$ bulb, both rated $220\ \text{V}$, are
   joined in series across $220\ \text{V}$. Then <span class="marks">[1]</span>
   (a) the $100\ \text{W}$ bulb is brighter (b) the $60\ \text{W}$ bulb is brighter
   (c) both are equally bright (d) neither glows

::: note Answers to Group A
**1.** (c) — from $v_d = I/nAe$, a few tenths of a millimetre per second.
**2.** (c) — volume is constant, so $A$ halves and $R \propto l^{2}$ gives $4R$.
**3.** (d) — $1/R_{eq} = 3/6$, so $R_{eq} = 2\ \Omega$.
**4.** (b) — charge cannot accumulate at a junction.
**5.** (d) — a low shunt in parallel carries the excess current.
**6.** (b) — same current in series, and $P = I^{2}R$ with $R_{60} > R_{100}$.
:::

**Group B — Short answer (5 marks each)**

1. Define drift velocity and derive the relation $I = nAv_de$ for a metallic
   conductor. <span class="marks">[5]</span>
2. Distinguish between ohmic and non-ohmic conductors with one $I$–$V$ graph and
   two examples of each. <span class="marks">[5]</span>
3. Derive expressions for the equivalent resistance of three resistors connected
   (a) in series and (b) in parallel. <span class="marks">[5]</span>
4. A battery of emf $10\ \text{V}$ and negligible internal resistance is connected
   to a $2\ \Omega$ resistor in series with a parallel combination of $4\ \Omega$
   and $12\ \Omega$. Find the equivalent resistance, the current drawn, and the
   current in each parallel branch. <span class="marks">[5]</span>
5. A cell of emf $2.0\ \text{V}$ and internal resistance $0.5\ \Omega$ is
   connected across a $4.5\ \Omega$ resistor. Find the current, the terminal
   potential difference, and the power dissipated in the external resistor. <span class="marks">[5]</span>
6. In a metre bridge experiment the unknown resistance $X$ is in the left gap and
   a $6\ \Omega$ resistance box in the right gap. The balance point is at
   $40\ \text{cm}$ from the left end. Find $X$, and state where the balance point
   would be if the two were interchanged. <span class="marks">[5]</span>

::: note Answers to Group B
**4.** Parallel part: $4\times12/16 = 3\ \Omega$; total $= 2+3 = 5\ \Omega$.
Current drawn $I = 10/5 = 2\ \text{A}$. Pd across the parallel part
$= 2\times3 = 6\ \text{V}$, so $I_4 = 6/4 = 1.5\ \text{A}$ and
$I_{12} = 6/12 = 0.5\ \text{A}$ (sum $= 2\ \text{A}$, as it must be).

**5.** $I = E/(R+r) = 2.0/5.0 = 0.40\ \text{A}$;
$V = IR = 0.40\times4.5 = 1.8\ \text{V}$ (or $E - Ir = 2.0-0.2$);
$P = I^{2}R = 0.16\times4.5 = 0.72\ \text{W}$.

**6.** $X = R\,l/(100-l) = 6\times40/60 = 4\ \Omega$. On interchanging, the
balance length measured from the left end becomes $100-40 = 60\ \text{cm}$,
since now $R/X = l'/(100-l')$ gives $6/4 = 60/40$.

**1., 2., 3.** are bookwork: see §23.1, §23.3 and §23.4 respectively. Marks are
awarded for the labelled diagram, the statement of the principle, and each
algebraic step.
:::

**Group C — Long answer (8 marks each)**

1. (a) State Kirchhoff's laws of electrical networks and name the conservation
   principle behind each. <span class="marks">[2]</span>
   (b) Draw a Wheatstone bridge and derive its balance condition. <span class="marks">[3]</span>
   (c) In a metre bridge, an unknown resistance in the left gap balances against
   $3\ \Omega$ in the right gap at $75\ \text{cm}$ from the left end. Find the
   unknown resistance. <span class="marks">[3]</span>
2. (a) Define emf and terminal potential difference and derive $V = E - Ir$. <span class="marks">[3]</span>
   (b) Describe how a potentiometer is used to measure the internal resistance of
   a cell, deriving the formula used. <span class="marks">[3]</span>
   (c) A cell balances at $250\ \text{cm}$ of a potentiometer wire; with a
   $5\ \Omega$ resistor across it the balance length falls to $200\ \text{cm}$.
   Find its internal resistance. <span class="marks">[2]</span>
3. (a) Derive $P = I^{2}R$ from the definition of potential difference, and state
   Joule's law of heating. <span class="marks">[3]</span>
   (b) A battery of emf $12\ \text{V}$ and internal resistance $1\ \Omega$ is
   connected to a $3\ \Omega$ resistor in series with a parallel combination of
   $6\ \Omega$ and $12\ \Omega$. Find the current drawn, the terminal potential
   difference, and the power dissipated in the $6\ \Omega$ resistor. <span class="marks">[5]</span>

::: note Answers to Group C
**1.(c)** $X = R\,l/(100-l) = 3\times75/25 = 9\ \Omega$.

**2.(c)** $r = R(l_1-l_2)/l_2 = 5\times(250-200)/200 = 5\times0.25 = 1.25\ \Omega$.

**3.(b)** Parallel part $= 6\times12/18 = 4\ \Omega$; total
$= 3+4+1 = 8\ \Omega$. Current $I = 12/8 = 1.5\ \text{A}$. Terminal pd
$V = E - Ir = 12 - 1.5 = 10.5\ \text{V}$. Pd across the parallel part
$= 1.5\times4 = 6\ \text{V}$, so the $6\ \Omega$ resistor carries $1.0\ \text{A}$
and dissipates $P = I^{2}R = 1.0^{2}\times6 = 6\ \text{W}$.

**1.(a), 1.(b), 2.(a), 2.(b), 3.(a)** are bookwork: see the boxed statements in
§23.4, the Wheatstone derivation, §23.6 and §23.7.
:::
