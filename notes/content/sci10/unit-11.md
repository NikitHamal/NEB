---
subject: Science and Technology
grade: 10
unit: 11
title: Electricity and Magnetism
hours: 0
area: Science and Technology
---

Nepal is rich in rivers, and its hydropower stations turn falling water into electricity that lights homes in Kathmandu, runs machines in Birgunj and is even sold to India. How does moving water produce electricity? Why does a heater get hot and a fan spin? How does a mobile charger turn 220 V into 5 V? The answers lie in the close relation between electricity and magnetism. In this unit you will learn Ohm's law and resistance, electrical power and energy, the magnetic effect of an electric current, electromagnetic induction, and the working of the generator and the transformer.

::: key What SEE asks from this unit
$V = IR$, resistors in series and parallel, $R = \rho l/A$, $P = VI$, energy in kWh and electricity bills, Joule's heating law, the rules (right-hand grip, Fleming's left- and right-hand rules), Faraday's law, the working of a DC motor, an AC generator and a transformer, and $V_s/V_p = N_s/N_p$.
:::

**Basic ideas.** An **electric current** is the flow of electric charge (electrons in a metal wire). If a charge $Q$ passes a point in time $t$, the current is

$$ I = \frac{Q}{t} $$

The unit of current is the **ampere (A)**: 1 A = 1 coulomb per second. The **potential difference** (voltage) $V$ between two points is the work done per unit charge in moving charge between them. Its unit is the **volt (V)**: 1 V = 1 joule per coulomb. A cell or battery supplies the potential difference that pushes charge round a circuit. Current is measured by an **ammeter** connected in **series**; potential difference is measured by a **voltmeter** connected in **parallel**. By convention, current flows from the positive terminal to the negative terminal outside the cell, which is opposite to the direction of electron flow.

## 11.1 Ohm's law

::: definition Ohm's law
At constant temperature, the current flowing through a conductor is directly proportional to the potential difference across its ends.
:::

$$ I \propto V \quad\Rightarrow\quad V = IR $$

The constant $R$ is the **resistance** of the conductor. A graph of $V$ against $I$ is a straight line through the origin whose slope is $R$. Conductors that obey Ohm's law are called **ohmic** (a metal wire at constant temperature). A filament lamp or a diode is non-ohmic.

```figure caption="V-I graph for two ohmic conductors. The slope is the resistance, so the steeper line is the larger resistance (5 ohm against 2 ohm)."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.4, 2.8))
I = np.linspace(0, 2.4, 20)
ax.plot(I, 5*I, color='#A8271F', lw=2)
ax.plot(I, 2*I, color=ACCENT, lw=2)
ax.text(1.95, 9.9, 'R = 5 ohm', fontsize=8.5, color='#A8271F')
ax.text(2.0, 3.3, 'R = 2 ohm', fontsize=8.5, color=ACCENT)
ax.set_xlabel('current I (A)'); ax.set_ylabel('potential difference V (V)')
ax.set_xlim(0, 2.9); ax.set_ylim(0, 13)
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.5)
fig.tight_layout()
```

::: example Using Ohm's law
**Problem.** A 12 V battery is connected across a resistor of 4 Ω. Find the current. What potential difference is needed to send 0.5 A through the same resistor?

**Solution.** $I = \dfrac{V}{R} = \dfrac{12}{4} = 3$ A.

For 0.5 A: $V = IR = 0.5 \times 4 = 2$ V.
:::

## 11.2 Resistance

::: definition Resistance
Resistance is the opposition offered by a conductor to the flow of electric current through it. Its SI unit is the ohm (Ω): 1 Ω is the resistance when a potential difference of 1 V drives a current of 1 A.
:::

### Factors affecting the resistance of a wire

1. **Length** $l$: $R \propto l$. A longer wire has more resistance.
2. **Cross-sectional area** $A$: $R \propto 1/A$. A thicker wire has less resistance.
3. **Material**: different materials have different resistivity.
4. **Temperature**: the resistance of a metal rises with temperature.

Combining the first three,

$$ R = \rho\,\frac{l}{A} $$

where $\rho$ is the **resistivity** (specific resistance) of the material, in ohm metre (Ω m). It is the resistance of a wire of unit length and unit cross-section, and depends only on the material (and temperature).

| Material | Resistivity (Ω m) | Use |
|---|---|---|
| Silver | $1.6\times10^{-8}$ | Best conductor, expensive |
| Copper | $1.7\times10^{-8}$ | Connecting wires |
| Aluminium | $2.8\times10^{-8}$ | Overhead power lines |
| Nichrome | $1.1\times10^{-6}$ | Heater coils, electric iron |
| Tungsten | $5.6\times10^{-8}$ | Bulb filament (high melting point) |
| Glass / rubber | $10^{10}$ to $10^{14}$ | Insulators |

::: example Resistance of a wire
**Problem.** Find the resistance of a nichrome wire 5 m long with cross-sectional area $0.5\ \text{mm}^2$. ($\rho = 1.1\times10^{-6}$ Ω m.)

**Solution.** $A = 0.5\ \text{mm}^2 = 0.5\times10^{-6}\ \text{m}^2$.

$R = \rho\dfrac{l}{A} = \dfrac{1.1\times10^{-6} \times 5}{0.5\times10^{-6}} = 11$ Ω.
:::

### Combination of resistors

**Series.** Resistors are joined end to end. The same current flows through each, and the total potential difference is shared.

$$ R_s = R_1 + R_2 + R_3 + \cdots \qquad V = V_1 + V_2 + V_3 $$

**Parallel.** Resistors are connected between the same two points. The potential difference across each is the same, and the current divides.

$$ \frac{1}{R_p} = \frac{1}{R_1} + \frac{1}{R_2} + \frac{1}{R_3} + \cdots \qquad I = I_1 + I_2 + I_3 $$

For two resistors in parallel, $R_p = \dfrac{R_1R_2}{R_1 + R_2}$. The equivalent resistance in parallel is always **smaller** than the smallest resistor.

```figure caption="Left: three resistors in series. Right: two resistors in parallel across a cell. The long thin line of the cell symbol is the positive terminal."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, (a1, a2) = plt.subplots(1, 2, figsize=(5.2, 2.6))
def res(ax, x, y, w=1.6, h=0.6, lab=''):
    ax.add_patch(Rectangle((x - w/2, y - h/2), w, h, fc='white', ec=INK, lw=1.3, zorder=3))
    ax.text(x, y + 0.65, lab, ha='center', fontsize=8.5, color=INK)
def cell(ax, x, y):
    ax.plot([x, x], [y - 0.5, y + 0.5], color=INK, lw=2.5, zorder=3)
    ax.plot([x + 0.35, x + 0.35], [y - 0.25, y + 0.25], color=INK, lw=2.5, zorder=3)
for ax in (a1, a2):
    ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis('off')
a1.set_title('Series', fontsize=9, color=INK)
a1.plot([0.5, 0.5, 9.5, 9.5, 0.5], [1, 5, 5, 1, 1], color=INK, lw=1.3)
res(a1, 2.2, 5, lab='R1'); res(a1, 5.0, 5, lab='R2'); res(a1, 7.8, 5, lab='R3')
cell(a1, 4.8, 1); a1.text(5.6, 0.1, 'cell', fontsize=8, color=INK)
a2.set_title('Parallel', fontsize=9, color=INK)
a2.plot([0.5, 0.5, 9.5, 9.5, 0.5], [0.8, 5, 5, 0.8, 0.8], color=INK, lw=1.3)
a2.plot([3.5, 3.5], [0.8, 5], color=INK, lw=1.3); a2.plot([7.0, 7.0], [0.8, 5], color=INK, lw=1.3)
a2.add_patch(Rectangle((3.5 - 0.4, 2.2), 0.8, 1.6, fc='white', ec=INK, lw=1.3, zorder=3))
a2.add_patch(Rectangle((7.0 - 0.4, 2.2), 0.8, 1.6, fc='white', ec=INK, lw=1.3, zorder=3))
a2.text(2.9, 3.0, 'R1', fontsize=8.5, color=INK, ha='right')
a2.text(8.2, 3.0, 'R2', fontsize=8.5, color=INK, ha='center')
cell(a2, 1.8, 0.8)
fig.tight_layout()
```

::: example Resistors in series
**Problem.** Resistors of 2 Ω, 3 Ω and 5 Ω are connected in series to a 10 V battery. Find the total resistance, the current, and the potential difference across each resistor.

**Solution.** $R_s = 2 + 3 + 5 = 10$ Ω. $I = \dfrac{V}{R_s} = \dfrac{10}{10} = 1$ A.

$V_1 = 1 \times 2 = 2$ V, $V_2 = 1 \times 3 = 3$ V, $V_3 = 1 \times 5 = 5$ V. Check: $2 + 3 + 5 = 10$ V ✓.
:::

::: example Resistors in parallel
**Problem.** A 6 Ω and a 3 Ω resistor are connected in parallel to a 12 V supply. Find the equivalent resistance, the total current and the current in each resistor.

**Solution.** $\dfrac{1}{R_p} = \dfrac{1}{6} + \dfrac{1}{3} = \dfrac{1 + 2}{6} = \dfrac{1}{2}$, so $R_p = 2$ Ω.

Total current $I = \dfrac{12}{2} = 6$ A.

$I_1 = \dfrac{12}{6} = 2$ A and $I_2 = \dfrac{12}{3} = 4$ A. Check: $2 + 4 = 6$ A ✓.
:::

Household appliances are connected in parallel, so that each gets the full 220 V and can be switched on or off independently. Decorative lights in older strings were in series: one failed bulb switched them all off.

## 11.3 Electrical power

### Electrical energy and power

When a charge $Q$ moves through a potential difference $V$, the work done (energy transferred) is $W = QV$. As $Q = It$,

$$ W = VIt $$

**Electrical power** is the rate at which electrical energy is used:

$$ P = \frac{W}{t} = VI = I^{2}R = \frac{V^{2}}{R} $$

The unit is the watt (W). 1 W = 1 J s⁻¹. Larger units: 1 kW = 1000 W, 1 MW = $10^6$ W.

### Commercial unit of energy

The joule is too small for household use. Electrical energy is billed in **kilowatt-hours (kWh)**, called one **unit**.

$$ 1\ \text{kWh} = 1000\ \text{W} \times 3600\ \text{s} = 3.6\times10^{6}\ \text{J} $$

Energy in kWh $=$ power in kW $\times$ time in hours.

::: example Bulb rating
**Problem.** A bulb is marked 100 W, 220 V. Find the current drawn and the resistance of its filament when it works normally.

**Solution.** $I = \dfrac{P}{V} = \dfrac{100}{220} = 0.45$ A.

$R = \dfrac{V^2}{P} = \dfrac{220^2}{100} = \dfrac{48400}{100} = 484$ Ω.
:::

::: example Electricity bill
**Problem.** A house has 5 bulbs of 40 W used for 6 hours daily and a 1 kW heater used for 2 hours daily. Find the energy used in 30 days and the bill at Rs 10 per unit.

**Solution.** Bulbs: $5 \times 40 = 200\ \text{W} = 0.2$ kW; energy per day $= 0.2 \times 6 = 1.2$ kWh.

Heater: $1 \times 2 = 2$ kWh per day.

Total per day $= 3.2$ kWh; in 30 days $= 3.2 \times 30 = 96$ kWh (units).

Bill $= 96 \times 10 =$ Rs 960.
:::

### Heating effect of current (Joule's law)

When current flows through a resistor, electrical energy changes to heat. The heat produced is

$$ H = I^{2}Rt \quad(\text{joule}) $$

The heat produced is proportional to the square of the current, to the resistance, and to the time. Applications: electric heater, iron, toaster, kettle (nichrome wire is used, since it has high resistivity and a high melting point), bulbs (a thin tungsten filament glows white-hot), and the **fuse**.

A **fuse** is a short piece of wire of low melting point placed in series in a circuit. When the current is too large (short circuit or overload), the wire heats, melts and breaks the circuit, saving the appliances and preventing fire. A modern alternative is the miniature circuit breaker (MCB). A fuse is always put in the live wire.

::: example Heat produced
**Problem.** A current of 2 A passes through a resistor of 50 Ω for 10 minutes. Find the heat produced.

**Solution.** $t = 10 \times 60 = 600$ s. $H = I^2Rt = 2^2 \times 50 \times 600 = 4 \times 50 \times 600 = 1.2\times10^5$ J.
:::

::: caution Watt is power, not energy
Do not write "the bulb used 100 W". A watt is a rate (joules per second). The energy used is $P \times t$ in J or kWh. A "unit" of electricity is 1 kWh, an amount of energy, not of power.
:::

## 11.4 Magnetic effect of current

### Oersted's experiment

In 1820 Hans Christian Oersted noticed that a compass needle held near a wire carrying current was deflected. When the current was reversed, the deflection was reversed. So **a current-carrying conductor produces a magnetic field** around it. This showed that electricity and magnetism are linked.

### Magnetic field of a straight wire

The field lines around a straight wire are concentric circles in a plane perpendicular to the wire, with the wire at the centre. Their direction is given by the **right-hand grip rule**: hold the wire in your right hand with the thumb pointing in the direction of the current; the curled fingers show the direction of the magnetic field. The field is stronger near the wire, and stronger when the current is larger.

```figure caption="Magnetic field around a straight wire carrying current out of the page (dot). The field lines are circles running anticlockwise; the field is stronger close to the wire."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(3.6, 3.4))
ax.set_xlim(-4.6, 4.6); ax.set_ylim(-4.9, 4.6); ax.set_aspect('equal'); ax.axis('off')
th = np.linspace(0, 2*np.pi, 200)
for r in (1.2, 2.2, 3.4):
    ax.plot(r*np.cos(th), r*np.sin(th), color=ACCENT, lw=1.4)
    a = np.pi/4
    x, y = r*np.cos(a), r*np.sin(a)
    ax.annotate('', xy=(x - 0.1*np.sin(a), y + 0.1*np.cos(a)), xytext=(x + 0.3*np.sin(a), y - 0.3*np.cos(a)),
                arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.4))
ax.plot([0], [0], 'o', color=INK, ms=9)
ax.plot([0], [0], 'o', color='white', ms=3)
ax.text(0.35, -0.7, 'I', fontsize=9, color=INK)
ax.text(0, -4.6, 'current out of the page', ha='center', fontsize=8.5, color=INK)
```

### Field of a solenoid and electromagnet

A **solenoid** is a long coil of insulated wire wound in a cylinder. When current flows, the field inside is strong and nearly uniform, parallel to the axis; outside it looks like the field of a bar magnet. One end acts as a north pole and the other as a south pole. Looking at an end, if the current flows **anticlockwise** it is the **north** pole; if **clockwise** it is the **south** pole.

An **electromagnet** is a solenoid with a soft iron core. Soft iron is magnetised strongly while the current flows and loses its magnetism when the current stops. The strength can be increased by:

- passing a larger current,
- using more turns of wire,
- using a soft iron core.

Uses: electric bell, crane lifting scrap iron, relay, loudspeaker, MRI machine, magnetic levitation trains.

### Force on a current-carrying conductor in a magnetic field

When a conductor carrying current is placed in a magnetic field, it experiences a force (the motor effect). The force is greatest when the wire is perpendicular to the field, and zero when the wire is parallel to the field. Its size is proportional to the current, the length of wire in the field and the field strength. The direction is given by **Fleming's left-hand rule**:

::: memory Fleming's left-hand rule
Stretch the thumb, forefinger and middle finger of the **left** hand at right angles to each other.
- **F**orefinger → direction of the magnetic **field** (north to south)
- **C**entre (middle) finger → direction of the **current**
- **T**humb → direction of the **thrust** (force) on the conductor
:::

### DC motor

An electric motor changes electrical energy into mechanical energy. A rectangular coil is placed between the north and south poles of a magnet. Its two ends are connected to two halves of a split ring, the **commutator**, which touch two fixed carbon **brushes** joined to a battery.

1. Current flows through the coil. By Fleming's left-hand rule, the forces on the two long sides are equal and opposite (one up, one down). They turn the coil.
2. When the coil becomes vertical, the commutator halves swap brushes and the current in the coil is reversed, so the forces keep turning the coil in the same direction.
3. The coil rotates continuously.

The speed can be increased by increasing the current, the number of turns, the strength of the magnet, or the area of the coil. Motors drive fans, washing machines, mixers, pumps and electric vehicles.

## 11.5 Electromagnetic induction

In 1831 Michael Faraday showed the opposite effect: a magnet can produce a current. When a bar magnet is pushed into a coil connected to a sensitive galvanometer, the needle deflects. When the magnet is pulled out, the needle deflects in the opposite direction. When the magnet is still, there is no deflection.

::: definition Electromagnetic induction
The production of an electromotive force (and a current in a closed circuit) in a conductor whenever the magnetic flux linked with it changes is called electromagnetic induction.
:::

**Faraday's law:** the induced emf is proportional to the rate of change of magnetic flux through the circuit. So the induced emf is larger if:

- the magnet moves faster (the field changes faster),
- the magnet is stronger,
- the coil has more turns.

**Lenz's law:** the direction of the induced current is such that it opposes the change that produced it. (This is the law of conservation of energy: we must do work to push the magnet in.)

::: memory Fleming's right-hand rule
Stretch the thumb, forefinger and middle finger of the **right** hand at right angles. Thumb = direction of **motion** of the conductor; forefinger = direction of the **field**; middle finger = direction of the **induced current**.

Easy way to remember: **left hand for motors** (current in, motion out); **right hand for generators** (motion in, current out).
:::

### Mutual induction

When the current in one coil (primary) changes, a changing magnetic field passes through a neighbouring coil (secondary) and induces an emf in it. This is **mutual induction**. It works only when the current is changing, and is the principle of the transformer.

::: caution Steady current, no induction
A magnet at rest inside a coil, or a steady DC current in the primary coil, induces nothing. Induction needs a **change** in flux. This is why a transformer works only on AC.
:::

## 11.6 Generator and transformer

### AC generator (dynamo)

A generator changes mechanical energy into electrical energy, using electromagnetic induction. A rectangular coil (the armature) rotates between the poles of a strong magnet. As it turns, the magnetic flux through it keeps changing, so an emf is induced. The ends of the coil are connected to two **slip rings**, which rub against carbon brushes that lead to the external circuit.

```photo id="sci10/alternator" caption="A large alternator (AC generator) in a power station. Water or steam turns the rotor, and electromagnetic induction produces the alternating current." width="76"
```

- In half a turn, the induced current flows one way; in the next half it reverses. So the output is an **alternating current (AC)**.
- In Nepal and India, the AC supply is 220 V and 50 Hz: the current reverses direction 100 times a second.
- The output is increased by rotating the coil faster, using a stronger magnet, more turns, or a larger coil.
- If a commutator (split ring) is used in place of slip rings, the output is a pulsating direct current (DC generator).

In a hydropower station, falling water turns a turbine, which turns the coil (or magnet) of a generator. In a thermal power station, steam turns the turbine. Wind and tidal power use the same principle.

| | AC | DC |
|---|---|---|
| Direction | Changes periodically | One direction only |
| Source | AC generator | Cell, battery, solar cell |
| Transmission | Easy to step up and down by transformer; small loss | Not easily |
| Frequency | 50 Hz in Nepal | 0 |

### Transformer

A transformer is a device used to increase (step up) or decrease (step down) an AC voltage. It works on mutual induction.

```photo id="sci10/transformer-pole" caption="A step-down transformer on an electricity pole. It lowers the high voltage of the supply line to a safe voltage for houses." width="56"
```

```figure caption="A transformer. Alternating current in the primary coil sets up a changing magnetic flux in the soft iron core; it induces an alternating emf in the secondary coil."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(4.8, 3.0))
ax.set_xlim(0, 12); ax.set_ylim(0, 8.5); ax.axis('off')
ax.add_patch(Rectangle((3.2, 1.2), 5.6, 4.4, fc='#D9DEE6', ec=INK, lw=1.5))
ax.add_patch(Rectangle((4.4, 2.2), 3.2, 2.4, fc='white', ec=INK, lw=1.5))
for yy in np.linspace(1.9, 4.9, 8):
    ax.plot([2.8, 3.8], [yy, yy + 0.18], color='#A8271F', lw=2)
for yy in np.linspace(1.9, 4.9, 5):
    ax.plot([8.2, 9.2], [yy, yy + 0.18], color=ACCENT, lw=2)
ax.plot([2.8, 1.2, 1.2], [1.9, 1.9, 0.9], color=INK, lw=1.3)
ax.plot([2.8, 1.2, 1.2], [5.0, 5.0, 6.0], color=INK, lw=1.3)
ax.plot([9.2, 10.8, 10.8], [1.9, 1.9, 0.9], color=INK, lw=1.3)
ax.plot([9.2, 10.8, 10.8], [5.0, 5.0, 6.0], color=INK, lw=1.3)
ax.text(1.2, 6.4, 'primary\n(Np turns)\ninput Vp', ha='center', va='bottom', fontsize=8.5, color='#A8271F')
ax.text(10.8, 6.4, 'secondary\n(Ns turns)\noutput Vs', ha='center', va='bottom', fontsize=8.5, color=ACCENT)
ax.text(6.0, 3.4, 'soft iron\ncore', ha='center', fontsize=8.5, color=INK)
```

Construction: a laminated soft iron core, a **primary coil** (input) and a **secondary coil** (output), both insulated and wound on the core. Working: AC in the primary produces a changing magnetic flux in the core; the same flux links the secondary and induces an AC emf of the same frequency.

$$ \frac{V_s}{V_p} = \frac{N_s}{N_p} $$

| | Step-up transformer | Step-down transformer |
|---|---|---|
| Turns | $N_s > N_p$ | $N_s < N_p$ |
| Output voltage | Greater than input | Less than input |
| Output current | Smaller | Larger |
| Use | Raise voltage at the power station for long-distance transmission | Mobile chargers, adapters, local supply to homes |

For an **ideal** transformer (no energy loss), input power equals output power:

$$ V_pI_p = V_sI_s $$

So if the voltage is stepped up, the current is stepped down in the same ratio. A transformer works only on AC, because only a changing current produces a changing flux; with DC it will not work.

**Why transmit at high voltage?** For a given power $P = VI$, a higher voltage means a smaller current $I$. The heat lost in the lines is $I^2R$, so it falls sharply. That is why power is raised to 132 kV or 220 kV (or more) at the station, carried over long wires, and stepped down in stages near towns to 11 kV and finally 220 V for homes.

Losses in real transformers: heat in the coil wires (copper loss), eddy currents in the core (reduced by laminating the core), magnetisation loss, and leakage of flux. Efficiency $= \dfrac{\text{output power}}{\text{input power}} \times 100\%$, typically above 95 %.

::: example Step-down transformer
**Problem.** A transformer has 2000 turns in its primary and 100 turns in its secondary. The primary is connected to a 220 V AC supply. (a) Find the output voltage. (b) If the output current is 2 A, find the input current, assuming an ideal transformer.

**Solution.** (a) $\dfrac{V_s}{V_p} = \dfrac{N_s}{N_p}$, so $V_s = 220 \times \dfrac{100}{2000} = 11$ V. As $V_s < V_p$, it is a step-down transformer.

(b) $V_pI_p = V_sI_s$: $220 \times I_p = 11 \times 2$, so $I_p = \dfrac{22}{220} = 0.1$ A.
:::

::: example Step-up transformer
**Problem.** A generator gives 11 kV. A step-up transformer with 100 turns in the primary raises it to 132 kV. How many turns are in the secondary?

**Solution.** $N_s = N_p \times \dfrac{V_s}{V_p} = 100 \times \dfrac{132}{11} = 1200$ turns.
:::

## Chapter summary

- $I = Q/t$ (A); $V$ = work per unit charge (V). Ohm's law: $V = IR$ at constant temperature.
- $R = \rho l/A$. Series: $R_s = R_1 + R_2 + \cdots$; parallel: $\dfrac{1}{R_p} = \dfrac{1}{R_1} + \dfrac{1}{R_2} + \cdots$.
- Power $P = VI = I^2R = V^2/R$; energy $W = Pt$; 1 kWh = 3.6×10⁶ J. Heat $H = I^2Rt$. A fuse breaks an overloaded circuit.
- A current produces a magnetic field (Oersted). Right-hand grip rule gives its direction; a solenoid with an iron core is an electromagnet.
- A conductor carrying current in a magnetic field feels a force (Fleming's left-hand rule). The DC motor uses it and a split-ring commutator.
- Electromagnetic induction: changing flux induces an emf (Faraday); its direction opposes the change (Lenz). Fleming's right-hand rule gives the direction.
- AC generator: mechanical → electrical energy, slip rings, output AC (50 Hz in Nepal).
- Transformer (AC only): $\dfrac{V_s}{V_p} = \dfrac{N_s}{N_p}$ and $V_pI_p = V_sI_s$ for an ideal one; high-voltage transmission reduces $I^2R$ loss.

## Practice questions

**Group A — Objective (1 mark each)**

1. The SI unit of resistance is <span class="marks">[1]</span>
   (a) volt (b) ampere (c) ohm (d) watt
2. Which rule gives the direction of force on a current-carrying wire in a magnetic field? <span class="marks">[1]</span>
   (a) Fleming's left-hand rule (b) Fleming's right-hand rule (c) Lenz's law (d) Ohm's law
3. A transformer works on <span class="marks">[1]</span>
   (a) DC only (b) AC only (c) both AC and DC (d) neither
4. 1 kWh is equal to <span class="marks">[1]</span>
   (a) $3.6\times10^3$ J (b) $3.6\times10^6$ J (c) $3.6\times10^9$ J (d) 1000 J
5. In an AC generator, the output current reverses direction because of <span class="marks">[1]</span>
   (a) the magnet (b) the slip rings (c) the rotation of the coil (d) the brushes

::: note Answers to Group A
**1.** (c) — resistance is measured in ohm (Ω).
**2.** (a) — thumb force, forefinger field, middle finger current.
**3.** (b) — only a changing current gives a changing flux.
**4.** (b) — 1000 W × 3600 s.
**5.** (c) — as the coil rotates, each side alternately moves up and down through the field, reversing the induced current every half turn.
:::

**Group B — Short answer (2 marks each)**

1. State Ohm's law. <span class="marks">[2]</span>
2. Why are household appliances connected in parallel? <span class="marks">[2]</span>
3. What is a fuse? Where is it connected in a circuit? <span class="marks">[2]</span>
4. State Faraday's law of electromagnetic induction. <span class="marks">[2]</span>
5. Why is electricity transmitted at high voltage? <span class="marks">[2]</span>

::: note Answers to Group B
**1.** At constant temperature, the current through a conductor is directly proportional to the potential difference across its ends: $V = IR$.
**2.** Each appliance receives the full supply voltage (220 V) and can be switched on or off independently of the others.
**3.** A fuse is a wire of low melting point that melts and breaks the circuit when the current is too large. It is connected in series with the live wire.
**4.** The emf induced in a circuit is proportional to the rate of change of magnetic flux linked with it.
**5.** At high voltage the current is small for the same power, so the heat loss $I^2R$ in the wires is much smaller.
:::

**Group C — Long answer (4 marks each)**

1. Three resistors of 4 Ω, 6 Ω and 12 Ω are connected in parallel across a 12 V battery. Find the equivalent resistance and the total current. <span class="marks">[4]</span>
2. An electric iron of 1000 W, 220 V is used for 3 hours a day. Find the energy used in 30 days and the cost at Rs 12 per unit. <span class="marks">[4]</span>
3. Draw a labelled diagram and explain the working of an AC generator. <span class="marks">[4]</span>
4. A step-down transformer has 1000 turns in the primary and 50 turns in the secondary. If the input voltage is 220 V, find the output voltage. If the output current is 4 A, find the input current. <span class="marks">[4]</span>
5. Explain the working of a DC motor with the help of Fleming's left-hand rule. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** $\dfrac{1}{R_p} = \dfrac{1}{4} + \dfrac{1}{6} + \dfrac{1}{12} = \dfrac{3 + 2 + 1}{12} = \dfrac{6}{12} = \dfrac{1}{2}$, so $R_p = 2$ Ω. $I = \dfrac{12}{2} = 6$ A.
**2.** Energy per day $= 1 \text{ kW} \times 3 \text{ h} = 3$ kWh. In 30 days: 90 kWh. Cost $= 90 \times 12 =$ Rs 1080.
**3.** Draw the coil between N and S poles, slip rings and brushes. Explain: the coil rotates, the flux changes, emf is induced; slip rings give AC; current reverses every half turn (50 Hz in Nepal).
**4.** $V_s = 220 \times \dfrac{50}{1000} = 11$ V. $I_p = \dfrac{V_sI_s}{V_p} = \dfrac{11 \times 4}{220} = 0.2$ A.
**5.** Describe the coil in the magnetic field, split-ring commutator, brushes. Forces on the two sides are opposite by the left-hand rule, which turn the coil; the commutator reverses the current each half turn, so the rotation continues in one direction.
:::
