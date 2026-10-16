---
subject: Science and Technology
grade: 8
unit: 8
title: Electricity and Magnetism
hours: 0
area: Science and Technology
---

Switch on a light and something invisible happens inside the wire. Hold a
magnet near a pin and the pin jumps without anything touching it. The two
effects are joined: a current makes a magnet, and a moving magnet makes a
current. This unit begins with the magnet, then looks at the electricity that
comes into a house — the circuit, the resistance, the fuse, the meter — and
ends with the electricity bill, which every household must be able to read.

::: key What this unit asks of you
You should be able to describe the poles and field of a magnet, explain
terrestrial magnetism and the magnetic compass, define current, potential
difference and resistance with their units, state and use Ohm's law, describe
the wiring of a house with a fuse, a switch and earthing, read an electric
meter and calculate an electricity bill, and explain the magnetic effect of
current and the working of an electric bell.
:::

## 8.1 Magnet

A **magnet** is an object that attracts iron, cobalt and nickel. Naturally
occurring magnetite (lodestone) was the first magnet known; today magnets are
made artificially by placing iron in a strong magnetic field.

### 8.1.1 Poles and the magnetic field

The region of a magnet where the attraction is strongest is its **pole**. Every
magnet has two poles, a north pole and a south pole, even when it is broken into
pieces — each piece becomes a complete magnet with its own two poles.

**Laws of magnetism.**
1. Like poles repel each other.
2. Unlike poles attract each other.

A **magnetic field** is the region around a magnet in which its force can be
felt. Its direction at any point is the direction in which the north pole of a
small compass points there. Field lines run from the north pole to the south
pole outside the magnet, and they never cross each other.

```figure caption="The magnetic field of a bar magnet drawn from field lines. The lines are closest together at the poles, which is why the attraction is strongest there, and they never cross."
import numpy as np
fig, ax = plt.subplots(figsize=(5.0, 2.7))
ax.set_xlim(-3.4, 3.4)
ax.set_ylim(-2.0, 2.0)
ax.axis("off")
ax.add_patch(plt.Rectangle((-1.6, -0.35), 3.2, 0.7, fc="#c9ccd1", ec=INK, lw=1.2))
ax.text(-1.15, 0, "N", ha="center", va="center", fontsize=8, color=INK)
ax.text(1.15, 0, "S", ha="center", va="center", fontsize=8, color=INK)
th = np.linspace(0, 2 * np.pi, 400)
for a in (0.9, 1.5, 2.2, 3.0):
    xs = a * np.cos(th)
    ys = 0.62 * a * np.sin(th)
    keep = np.abs(xs) < 3.2
    ax.plot(xs[keep], ys[keep], color=ACCENT, lw=0.9, alpha=0.85)
ax.annotate("", xy=(2.3, 0.95), xytext=(2.1, 0.85),
            arrowprops=dict(arrowstyle="->", color=ACCENT, lw=1.1))
ax.annotate("", xy=(-2.3, 0.95), xytext=(-2.1, 0.85),
            arrowprops=dict(arrowstyle="->", color=ACCENT, lw=1.1))
ax.text(0, -1.75, "field lines run N to S outside the magnet", ha="center",
        fontsize=6.6, color=MUTED)
fig.tight_layout()
```

### 8.1.2 Terrestrial magnetism and the compass

The earth itself behaves like a huge magnet. Its magnetic poles are near, but
not exactly at, the geographic poles, and they are reversed: the earth's
magnetic north pole is near the geographic north. A freely suspended magnet
always comes to rest pointing north-south, and a **magnetic compass** uses this
to find direction.

- The **magnetic declination** is the small angle between magnetic north and
  true north at a place, which is why a compass does not point exactly at the
  geographic pole.
- The **magnetic axis** of the earth is tilted by about 11° from its axis of
  rotation, which is why the magnetic poles move slowly over the years.
- A compass is unreliable near iron, a loudspeaker or a magnet; keep it away
  from your phone and your steel bottle.

## 8.2 Electricity

### 8.2.1 Static electricity

Rub a plastic comb on dry hair and it will pick up small pieces of paper. The
rubbing has transferred electrons from one body to the other, so one body has
extra electrons and is **negatively charged**, while the other has lost them and
is **positively charged**. Charges of the same kind repel and charges of
opposite kinds attract. A lightning flash is static electricity on a huge scale:
charges built up in the clouds are discharged between cloud and cloud, or
between cloud and earth.

### 8.2.2 Current, potential difference and resistance

| Quantity | Meaning | Symbol | SI unit | Measured with |
|---|---|---|---|---|
| Electric current | the rate of flow of charge | $I$ | ampere (A) | ammeter, in series |
| Potential difference | the work done to move unit charge between two points | $V$ | volt (V) | voltmeter, in parallel |
| Resistance | the opposition to the flow of current | $R$ | ohm (Ω) | ohmmeter |

**Ohm's law.** At constant temperature, the current through a conductor is
directly proportional to the potential difference across its ends:

$$V=IR,\qquad I=\frac{V}{R},\qquad R=\frac{V}{I}$$

A conductor obeys Ohm's law if its $V$-$I$ graph is a straight line through the
origin. Metals do; a filament bulb does not, because the filament gets hot and
its resistance changes.

```figure caption="A simple circuit drawn with proper symbols. The ammeter goes in series with the bulb and the voltmeter in parallel with it; a switch controls the whole circuit."
fig, ax = plt.subplots(figsize=(5.0, 2.6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 5.6)
ax.axis("off")
ax.add_patch(plt.Rectangle((1.2, 1.2), 7.6, 3.2, fill=False, ec=INK, lw=1.6))
ax.plot([2.6, 3.4], [1.2, 1.2], color="white", lw=3.0)
ax.plot([2.6, 2.6], [1.15, 1.75], color=INK, lw=1.4)
ax.plot([3.4, 4.3], [1.2, 1.9], color=INK, lw=1.4)
ax.text(3.0, 0.55, "switch", ha="center", fontsize=6.6, color=INK)
ax.add_patch(plt.Circle((5.6, 1.2), 0.42, fill=False, ec=SERIES[1], lw=1.4))
ax.text(5.6, 0.55, "bulb", ha="center", fontsize=6.6, color=SERIES[1])
ax.add_patch(plt.Circle((1.2, 2.8), 0.42, fill=False, ec=SERIES[2], lw=1.4))
ax.text(1.2, 2.8, "A", ha="center", va="center", fontsize=7.0, color=SERIES[2])
ax.text(0.55, 2.8, "ammeter", ha="right", va="center", fontsize=6.6, color=SERIES[2])
ax.add_patch(plt.Circle((4.4, 4.4), 0.42, fill=False, ec=ACCENT, lw=1.4))
ax.text(4.4, 4.4, "V", ha="center", va="center", fontsize=7.0, color=ACCENT)
ax.text(4.4, 5.1, "voltmeter, in parallel", ha="center", fontsize=6.6, color=ACCENT)
ax.add_patch(plt.Rectangle((7.9, 2.2), 1.2, 1.2, fc="white", ec=INK, lw=1.3))
ax.plot([8.5, 8.5], [2.2, 3.4], color=INK, lw=1.3)
ax.plot([8.15, 8.85], [4.05, 4.05], color=INK, lw=1.6)
ax.plot([8.15, 8.85], [4.3, 4.3], color=INK, lw=2.6)
ax.text(9.3, 4.2, "cell /\\nbattery", ha="left", va="center", fontsize=6.5, color=INK)
ax.text(5.0, 0.05, "current flows from the positive terminal, round the circuit, back to the negative",
        ha="center", fontsize=6.2, color=MUTED)
fig.tight_layout()
```

::: example Ohm's law
**Problem.** A bulb of resistance 24 Ω is connected to a 12 V battery. Find the
current through it. If the current is increased to 0.75 A, what potential
difference is needed?

**Solution.** Using $I=\frac{V}{R}$:

$$I=\frac{12}{24}=0.5\ \text{A}$$

For the second part, $V=IR=0.75\times24=18$ V.

**Answer.** 0.5 A; 18 V.

**Check.** $0.5\times24=12$ ✓ and $0.75\times24=18$ ✓ — the units, volts,
amperes and ohms, match Ohm's law directly.
:::

### 8.2.3 Series and parallel connection

| | Series | Parallel |
|---|---|---|
| Path for the current | one only | more than one |
| Current | the same everywhere | divides between the branches |
| Potential difference | divides between the components | the same across each branch |
| If one component breaks | the whole circuit stops | the other branches still work |
| Used for | a string of fairy lights, a fuse | house wiring |

House wiring is **parallel** so that each appliance gets the full 220 V and can
be switched on and off independently.

### 8.2.4 Household electrification

The mains supply in Nepal is about 220 V and 50 Hz alternating current. The
supply enters the house through a **fuse or a miniature circuit breaker (MCB)**,
then the **main switch**, then the **energy meter**, and then the distribution
board.

| Part | Function |
|---|---|
| Live wire (red or brown) | carries the current to the appliance |
| Neutral wire (black or blue) | completes the circuit back to the supply |
| Earth wire (green or yellow) | a safety wire connected to the ground; it gives a fault current an easy path to the earth, so the fuse blows instead of the person being shocked |
| Fuse | a thin wire of low melting point that melts when the current is too large, breaking the circuit |
| MCB | a switch that trips automatically and can be reset; it does the same job as a fuse |
| Switch | connects and breaks the circuit; it is always put in the live wire, never in the neutral |
| Energy meter | measures the electrical energy used, in kilowatt-hours |

```figure caption="The path of the mains supply into a house, and why the switch belongs in the live wire. If the switch were on the neutral side, the appliance would stay connected to the live wire even when the switch was off."
fig, ax = plt.subplots(figsize=(5.1, 2.7))
ax.set_xlim(0, 10)
ax.set_ylim(0, 5.8)
ax.axis("off")
steps = [("Pole", 0.9), ("Fuse /\\nMCB", 2.9), ("Main\\nswitch", 5.0),
         ("Energy\\nmeter", 7.1), ("Distribution\\nboard", 9.2)]
for name, x in steps:
    ax.text(x, 4.0, name, ha="center", va="center", fontsize=6.8, color=INK,
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=ACCENT, lw=1.0))
for i in range(4):
    x0 = 0.9 + i * 2.1
    ax.annotate("", xy=(x0 + 1.05, 4.0), xytext=(x0 + 0.55, 4.0),
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.0))
ax.plot([0.9, 9.2], [2.6, 2.6], color="#b00020", lw=1.5)
ax.text(0.9, 2.15, "live", ha="left", fontsize=6.5, color="#b00020")
ax.plot([0.9, 9.2], [1.9, 1.9], color=INK, lw=1.5)
ax.text(0.9, 1.45, "neutral", ha="left", fontsize=6.5, color=INK)
ax.plot([0.9, 9.2], [1.2, 1.2], color="#2f7d32", lw=1.5)
ax.text(0.9, 0.75, "earth", ha="left", fontsize=6.5, color="#2f7d32")
ax.plot([9.2, 9.2], [1.2, 1.9], color=GRID, lw=1.0, ls="--")
ax.text(5.0, 5.35, "the switch is always placed in the live wire", ha="center",
        fontsize=6.7, color=MUTED)
fig.tight_layout()
```

::: caution Never work on a live wire
Treat every wire as live until you have personally switched off the main switch
and checked. Water and electricity together are deadly: never touch a switch
with wet hands, never pour water on an electrical fire, and never use a bare
wire in place of a fuse. A fuse is sized for the wire it protects; a thick
copper wire in a fuse holder turns a small fault into a fire.
:::

### 8.2.5 Energy, the meter and the bill

The **kilowatt-hour (kWh)** is the unit of electrical energy the meter measures.
One unit on the meter is one kilowatt-hour.

$$1\ \text{kWh}=1000\ \text{W}\times3600\ \text{s}=3.6\times10^6\ \text{J}$$

$$\text{energy (kWh)}=\frac{\text{power (W)}\times\text{time (h)}}{1000}$$

::: example The household electricity bill
**Problem.** A house uses: 4 LED bulbs of 10 W for 5 hours a day each, a fan of
75 W for 6 hours a day, and a television of 60 W for 4 hours a day. The tariff
is Rs 9 per unit. Find the monthly bill for 30 days, and the bill if the fan is
run for 8 hours instead.

**Solution.** Daily energy:

- Bulbs: $4\times10\times5=200$ Wh
- Fan: $75\times6=450$ Wh
- Television: $60\times4=240$ Wh

Total $=200+450+240=890$ Wh $=0.89$ kWh per day.

For 30 days: $0.89\times30=26.7$ kWh, and
$26.7\times9=\text{Rs }240.30$.

With the fan on for 8 hours, the fan uses $75\times8=600$ Wh, so the daily total
becomes $200+600+240=1040$ Wh $=1.04$ kWh; for 30 days that is 31.2 kWh and
$31.2\times9=\text{Rs }280.80$.

**Answer.** Rs 240.30, or Rs 280.80 with the longer fan use.

**What it shows.** Two extra hours of the fan a day costs about Rs 40 a month.
The bill is a record of behaviour, not of luck.
:::

### 8.2.6 Magnetic effect of current and the electric bell

A wire carrying a current behaves like a magnet: the effect was first shown by
Hans Christian Oersted in 1820. The magnetic field is strongest close to the
wire, and if the wire is wound into a coil with an iron core, the arrangement is
an **electromagnet**. An electromagnet has two advantages over a permanent
magnet: it is magnetic only while the current flows, and its strength can be
changed by changing the current or the number of turns.

| Use | What the electromagnet does |
|---|---|
| Electric bell | pulls a hammer that strikes the gong |
| Telephone earpiece | vibrates a diaphragm to make sound |
| Loudspeaker | moves a coil in a magnetic field |
| Crane | lifts and drops scrap iron |
| Motor and generator | converts between electrical and kinetic energy |
| MRI machine | a very strong field to look inside the body |

In an **electric bell**, the current flows through the coil, the electromagnet
attracts the soft-iron armature, and the hammer strikes the gong. The same
movement breaks the contact at the screw, so the current stops, the electromagnet
lets go, the spring pulls the armature back, the contact is made again, and the
whole thing repeats — which is why a bell rings continuously while the button is
pressed.

```photo id="sci10/electromagnet" caption="An electromagnet lifting scrap iron. Its magnetism lasts only while the current flows." width="62"
```

```photo id="sci10/transformer-pole" caption="A pole-mounted distribution transformer. It steps the voltage down for household supply." width="62"
```

## Chapter summary

- A magnet attracts iron, cobalt and nickel; like poles repel and unlike poles
  attract; poles cannot be separated.
- Magnetic field lines run from north to south outside the magnet and never
  cross.
- The earth is a magnet; a compass points magnetic north, which differs from
  true north by the declination.
- Charge is gained or lost by friction; like charges repel, unlike attract.
- Current (A) is the rate of flow of charge, potential difference (V) is the
  work per unit charge, resistance (Ω) is the opposition.
- **Ohm's law:** $V=IR$; the $V$-$I$ graph of an ohmic conductor is a straight
  line through the origin.
- Series circuits share the potential difference and have one path; parallel
  circuits share the current and give each branch the full voltage, which is why
  houses are wired in parallel.
- A fuse or MCB protects the circuit, the earth wire protects the person, and
  the switch belongs in the live wire.
- $\text{energy (kWh)}=\frac{P\times t}{1000}$; one unit is 3.6 × 10⁶ J.
- A current has a magnetic effect; an electromagnet can be switched on and off,
  which is what makes the electric bell, the motor and the crane work.

## Practice questions

**Group A — Objective (1 mark each)**

1. The SI unit of electric current is the <span class="marks">[1]</span>
   (a) volt (b) ampere (c) ohm (d) watt
2. Like poles of two magnets <span class="marks">[1]</span>
   (a) attract (b) repel (c) do nothing (d) become one pole
3. In a house, the switch is always connected in the
   <span class="marks">[1]</span>
   (a) neutral wire (b) earth wire (c) live wire (d) fuse wire
4. An instrument that measures potential difference is a
   <span class="marks">[1]</span>
   (a) ammeter (b) voltmeter (c) galvanometer (d) energy meter
5. One kilowatt-hour equals <span class="marks">[1]</span>
   (a) 1000 J (b) 3600 J (c) $3.6\times10^6$ J (d) $3.6\times10^3$ J
6. The magnetic effect of current was first shown by
   <span class="marks">[1]</span>
   (a) Ohm (b) Oersted (c) Newton (d) Faraday

::: note Answers to Group A
**1.** (b) — the ampere.
**2.** (b) — like poles repel.
**3.** (c) — otherwise the appliance stays connected to the live wire.
**4.** (b) — the voltmeter, connected in parallel.
**5.** (c) — 1000 W for 3600 s.
**6.** (b) — Hans Christian Oersted, in 1820.
:::

**Group B — Short answer (2 marks each)**

1. State the two laws of magnetism and name two magnetic substances.
   <span class="marks">[2]</span>
2. Define current, potential difference and resistance with their SI units.
   <span class="marks">[2]</span>
3. Why is the earth wire needed in a house circuit?
   <span class="marks">[2]</span>
4. Give two differences between an electromagnet and a permanent magnet.
   <span class="marks">[2]</span>

::: note Answers to Group B
**1.** Like poles repel each other; unlike poles attract each other. Magnetic
substances: iron and nickel (also cobalt and steel).
**2.** Current is the rate of flow of electric charge, measured in amperes (A).
Potential difference is the work done in moving unit charge between two points,
measured in volts (V). Resistance is the opposition offered by a conductor to
the flow of current, measured in ohms (Ω).
**3.** The earth wire connects the metal body of an appliance to the ground. If
the live wire touches the body because of a fault, the current flows straight to
the earth instead of through the person touching it, and the large current blows
the fuse or trips the MCB, which cuts off the supply.
**4.** An electromagnet is magnetic only while current flows and its strength can
be changed by changing the current or the number of turns; a permanent magnet is
magnetic all the time and its strength is fixed. An electromagnet can have its
poles reversed by reversing the current; a permanent magnet cannot.
:::

**Group C — Long answer (4 marks each)**

1. A heater of resistance 44 Ω is connected to a 220 V supply. Find the current
   through it. If it is used for 3 hours a day, find the energy used in 30 days
   and the bill at Rs 9 per unit. <span class="marks">[4]</span>
2. Draw a labelled circuit diagram containing a cell, a switch, a bulb, an
   ammeter and a voltmeter. State Ohm's law and describe how you would verify it
   in the laboratory. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** $I=\frac{V}{R}=\frac{220}{44}=5$ A. Power
$P=VI=220\times5=1100$ W $=1.1$ kW. Energy per day
$=1.1\times3=3.3$ kWh; for 30 days $=3.3\times30=99$ kWh. Bill
$=99\times9=\text{Rs }891$.
**2.** **Diagram.** Draw a rectangular circuit with the cell (long line positive,
short thick line negative), a switch, and a bulb in series; place the ammeter in
series in the same loop, and the voltmeter in parallel across the bulb.
**Ohm's law.** At constant temperature, the current flowing through a conductor
is directly proportional to the potential difference across its ends, so
$V=IR$. **Verification.** (i) Connect a nichrome wire (or a fixed resistor) with
an ammeter in series and a voltmeter in parallel, and a variable number of cells
or a rheostat to change the voltage. (ii) Switch on and record the ammeter
reading $I$ and the voltmeter reading $V$. (iii) Repeat for at least five
different voltages and tabulate $V$, $I$ and $\frac{V}{I}$. (iv) Plot a graph of
$V$ against $I$; it comes out as a straight line through the origin, and its
slope is the resistance. (v) The value of $\frac{V}{I}$ is nearly the same in
every row, which proves the law. **Precaution.** Keep the current small and
switch off between readings, so that the wire does not heat up — the law holds
only at constant temperature.
:::
