---
subject: Science and Technology
grade: 8
unit: 8
title: Electricity and Magnetism
hours: 0
area: Science and Technology
---

Sumnima dropped a bar magnet in the laboratory and it broke into pieces. Each piece
still attracted and repelled the others — every piece was a complete magnet. Just
then the lights went off; the teacher said the MCB had tripped because of a fault in
the circuit. This unit explains both events: what makes a substance a magnet, how
the earth itself behaves as a magnet, and how electricity is brought safely into our
homes, measured and paid for.

::: key What this unit asks of you
State the properties of magnets; tell natural from artificial magnets; explain the
molecular theory of magnetism, demagnetisation and how to keep a magnet; describe
terrestrial magnetism, its evidence and uses, declination and dip; explain static
electricity, current, potential difference, resistance and Ohm's law; describe the
devices of household wiring (main switch, meter, distribution board, MCB, fuse,
switch, plug and socket, bulb) and the live, neutral and earth wires; wire a plug;
and calculate electrical energy and the electricity bill with $E=P\times N\times t$.
:::

## 8.1 Magnets, magnetic substances and the magnetic field

A **magnet** is a substance that attracts iron, cobalt and nickel, and has a north pole
(N) and a south pole (S). Substances attracted by a magnet are **magnetic
substances** (iron, cobalt, nickel, steel); others such as wood, plastic, copper and
aluminium are **non-magnetic**.

**Properties of a magnet** (Activity 8.1, with a freely suspended bar magnet):
(1) it attracts magnetic substances, most strongly at its poles; (2) a freely
suspended magnet always comes to rest in the **north–south direction**; (3) **like poles
repel, unlike poles attract**; (4) poles always exist in pairs — a broken magnet gives
smaller complete magnets.

The space around a magnet in which its force can be felt is the **magnetic field**. It
is shown by **magnetic lines of force**, which run from the N-pole to the S-pole outside
the magnet. They are crowded near the poles, where the field is strongest.

```figure caption="Magnetic lines of force around a bar magnet. Outside the magnet they run from N to S and are closest together near the poles."
fig, ax = plt.subplots(figsize=(4.8, 3.0))
Y, X = np.mgrid[-2.2:2.2:120j, -3.2:3.2:160j]
def field(px, q):
    dx, dy = X - px, Y
    r3 = (dx ** 2 + dy ** 2) ** 1.5 + 1e-3
    return q * dx / r3, q * dy / r3
u1, v1 = field(-1.0, 1); u2, v2 = field(1.0, -1)
U, V = u1 + u2, v1 + v2
inside = (abs(X) < 1.25) & (abs(Y) < 0.32)
U[inside] = np.nan; V[inside] = np.nan
ang = np.linspace(0, 2 * np.pi, 16, endpoint=False)
seeds = np.array([[-1.0 + 0.45 * np.cos(a), 0.45 * np.sin(a)] for a in ang
                  if abs(0.45 * np.sin(a)) > 0.33 or 0.45 * np.cos(a) < -0.25])
ax.streamplot(X, Y, U, V, start_points=seeds, color=ACCENT, linewidth=0.9, density=4,
              arrowsize=0.9, integration_direction="forward", maxlength=20)
seeds2 = np.array([[1.0 - 0.45 * np.cos(a), 0.45 * np.sin(a)] for a in ang
                   if 0.45 * np.cos(a) < -0.25 and abs(0.45 * np.sin(a)) <= 0.33])
ax.streamplot(X, Y, U, V, start_points=seeds2, color=ACCENT, linewidth=0.9, density=4,
              arrowsize=0.9, integration_direction="backward", maxlength=20)
ax.add_patch(plt.Rectangle((-1.25, -0.3), 1.25, 0.6, fc=SERIES[1], ec=INK))
ax.add_patch(plt.Rectangle((0, -0.3), 1.25, 0.6, fc="#9fb7d9", ec=INK))
ax.text(-0.62, 0, "N", ha="center", va="center", fontsize=10, color="white", weight="bold")
ax.text(0.62, 0, "S", ha="center", va="center", fontsize=10, color=INK, weight="bold")
ax.set_xlim(-3.2, 3.2); ax.set_ylim(-2.2, 2.2); ax.set_aspect("equal"); ax.axis("off")
fig.tight_layout()
```

### 8.1.1 Natural and artificial magnets

| Natural magnet | Artificial magnet |
|---|---|
| has magnetic properties naturally; found in the earth's crust | magnetic properties are given by people as needed |
| **lodestone** (magnetite, an iron ore) | bar, horseshoe, needle, ring magnets; electromagnets |
| irregular shape; strength cannot be changed | any shape; strength can be changed |
| weak | can be made strong; temporary or permanent |

An **electromagnet** is an artificial magnet made by passing electric current through a
coil (solenoid) of insulated wire wound on a soft-iron core (Activity 8.2: wind enamelled
copper wire on an iron nail and connect it to a 1.5 V cell through a switch; the nail
picks up pins only while the switch is ON).

**Uses of magnets:** in radios, televisions, fans, refrigerators, induction cookers,
electric bells, generators and motors; in computers, hard disks, headphones and sensors;
in **MRI** machines in hospitals; electromagnets lift iron plates in factories and ports;
**magnetic compass** for direction; magnetic locks on doors.

### 8.1.2 Molecular theory of magnetism

Proposed by the German scientist **Weber** and developed by **J. A. Ewing**:

1. Every magnetic substance is made of tiny **molecular magnets**, each with its own N
   and S poles.
2. In an **unmagnetised** substance the molecular magnets point in random directions and
   form **closed chains**, so their effects cancel.
3. When the substance is **magnetised**, the molecular magnets line up in one direction
   in **open chains**; free N-poles collect at one end and free S-poles at the other.
4. When all molecular magnets are aligned, the magnet cannot become any stronger — this
   is **magnetic saturation**.

```figure caption="Molecular theory: in an unmagnetised bar the molecular magnets form closed chains in random directions (left); in a magnet they line up in open chains (right)."
fig, axs = plt.subplots(1, 2, figsize=(5.0, 2.2))
rng = np.random.default_rng(3)
for k, ax in enumerate(axs):
    ax.add_patch(plt.Rectangle((0, 0), 6, 2.4, fc="#f3f3f3", ec=INK))
    for i in range(6):
        for j in range(3):
            x, y = 0.5 + i * 1.0, 0.4 + j * 0.8
            a = rng.uniform(0, 2 * np.pi) if k == 0 else 0.0
            dx, dy = 0.35 * np.cos(a), 0.35 * np.sin(a)
            ax.annotate("", xy=(x + dx, y + dy), xytext=(x - dx, y - dy),
                        arrowprops=dict(arrowstyle="-|>", color=SERIES[1] if k else MUTED, lw=1.2))
    ax.set_xlim(-0.5, 6.5); ax.set_ylim(-0.7, 2.6); ax.axis("off")
    ax.text(3, -0.45, "unmagnetised iron" if k == 0 else "magnet: S ... N", ha="center", fontsize=7.8, color=INK)
fig.tight_layout()
```

### 8.1.3 Demagnetisation and keeping a magnet

**Demagnetisation** is the loss of the magnetic property of a magnet. It happens when the
aligned molecular magnets are thrown back into random directions (closed chains).

| Cause | What it does |
|---|---|
| heating | molecules vibrate strongly and lose their alignment |
| hammering or dropping | jolts disturb the alignment |
| passing alternating current (a.c.) through a coil around it | the current keeps reversing and shakes the molecules out of line (Activity 8.3) |
| keeping like poles together for a long time | repulsion disturbs the alignment |
| natural loss | an old magnet kept without a keeper slowly weakens |

**To keep a magnet strong:** do not heat, hammer or drop it; keep it away from wires
carrying current; store bar magnets in pairs with **unlike poles side by side** and soft-
iron **keepers** across the ends.

## 8.2 Terrestrial magnetism and the magnetic compass

The earth behaves like a huge magnet. Its magnetism is called **terrestrial magnetism**
(geomagnetism). It is produced by the movement (convection currents) of molten iron and
nickel in the earth's **outer core**. The earth's magnetic poles are near — but not at —
the geographic poles, and they shift slowly. The pole of the earth-magnet that lies near
the geographic north is actually a magnetic **south** pole; that is why it attracts the N-
pole of a compass needle.

**Evidence:** (1) a freely suspended magnet always rests north–south; (2) an iron rod
buried north–south for a long time becomes slightly magnetised; (3) neutral points are
found where the fields of a magnet and the earth cancel; (4) natural magnets (lodestone)
exist in the earth.

**Applications:** the earth's magnetic field turns aside harmful charged particles of the
solar wind towards the poles (where they cause auroras), protecting life; magnetism in
igneous rocks helps to estimate their age and to find new ores; the **magnetic compass**
— a small magnetised needle pivoted freely — shows direction to travellers, ships,
submarines and aeroplanes (Activity 8.4). Many mobile phones also contain a compass sensor.

**Elements of terrestrial magnetism**

| Element | Meaning |
|---|---|
| Geographic meridian | vertical plane through the geographic north and south poles |
| Magnetic meridian | vertical plane in which a freely suspended magnet rests |
| **Magnetic declination** | the angle between the geographic meridian and the magnetic meridian at a place; it is used to correct compass readings in navigation and differs from place to place |
| **Angle of dip (inclination)** | the angle made by a freely suspended magnetic needle with the **horizontal**; measured with a **dip circle**. It is **0° at the magnetic equator**, **90° at the magnetic poles**, and about 42° in Kathmandu |

::: caution Declination and dip are different angles
Declination is a horizontal angle (between true north and magnetic north). Dip is a
vertical angle (between the needle and the horizontal). It is the **dip** that is 0° at the
magnetic equator and 90° at the magnetic poles, because there the needle points straight
down into the earth.
:::

## 8.3 Static electricity and electric charge

Rub a plastic comb with dry hair and it picks up small bits of paper. Rubbing transfers
tiny negatively charged particles (**electrons**) from one body to the other: the body
that gains electrons becomes **negatively** charged, the one that loses them **positively**
charged. Charge that stays on a body without flowing is **static electricity**. **Like
charges repel; unlike charges attract.** Lightning is a huge discharge of static charge
between clouds and the earth; tall buildings are protected by **lightning conductors**.

## 8.4 Electric circuit, current, potential difference and resistance

An **electric circuit** is a closed path of conductors through which current flows from
the positive terminal of a source (cell) through a load (bulb) back to the negative
terminal. A **switch** opens or closes the circuit.

| Quantity | Meaning | Unit | Measured by |
|---|---|---|---|
| Electric current (I) | rate of flow of charge | ampere (A) | ammeter, in series |
| Potential difference (V) | the "push" that drives charge between two points | volt (V) | voltmeter, in parallel |
| Resistance (R) | opposition to the flow of current | ohm (Ω) | from $R=\frac{V}{I}$ |

Loads may be joined in **series** (one path; the same current through each; one bulb
fails, all go off) or in **parallel** (separate paths; each gets the full voltage and can
be switched separately). House lights are in **parallel**; decorative disco lights are in series.

## 8.5 Ohm's law and its verification

::: definition Ohm's law
At constant temperature, the current flowing through a conductor is directly
proportional to the potential difference across its ends: $V\propto I$, or $V=IR$.
:::

**Verification:** connect a cell (or several cells), an ammeter, a resistance wire and a
switch in series, with a voltmeter across the wire. Increase the number of cells and
record V and I each time. The ratio $\frac{V}{I}$ stays the same, and a graph of V against
I is a straight line through the origin.

::: example Using Ohm's law
**Problem.** A current of 0.5 A flows through a bulb connected to 220 V. Find its resistance.

**Solution.** $R=\frac{V}{I}=\frac{220\ \text{V}}{0.5\ \text{A}}=440\ \Omega$.
:::

## 8.6 Household electrification: wiring, fuse, earthing and safety

Bringing electricity from the power house to homes through transmission lines is
**household electrification**. High-voltage electricity from the national grid is stepped
down by a substation **transformer** and supplied to houses at **220 V**. Wiring inside a
house with all safety measures is **domestic wiring**; copper cables are used.

**Order of devices:** service line → **electric meter** → **main switch** → **distribution
board with MCBs / fuses** → switches → sockets and lamps.

| Device | Work |
|---|---|
| Main (master) switch | turns the supply of the whole house on or off; allows 15 A or 30 A; in series with all loads |
| Electric meter | records the electrical energy used, in units (kWh); kept in a meter box in series with the main switch |
| Distribution board | divides the supply into separate circuits for different rooms and appliances |
| **MCB** (miniature circuit breaker) | automatic switch that **trips** (opens) when too much current flows (overload or short circuit); it can be switched on again without replacing anything |
| **Fuse** | a short thin wire of **tin and lead alloy** with **low melting point** (and high resistance) in a ceramic holder; it **melts** when excess current flows, breaking the circuit; 5 A–30 A fuses are used in houses; connected in series in the **live wire** |
| Switch | makes or breaks the circuit of an appliance; connected in series in the **live wire** |
| Plug and socket | connect appliances to the supply; 2-pin or 3-pin |
| Bulb | changes electrical energy into light; filament (tungsten), fluorescent, CFL, LED; connected in **parallel** |

### 8.6.1 Live, neutral and earth wires

| Wire | Description | Colour (textbook) |
|---|---|---|
| **Live (phase)** | carries current at high potential (220 V); touching it gives a shock; switch and fuse are put in it | red (brown in new cables) |
| **Neutral** | at zero potential; completes the circuit back to the supply | black or blue |
| **Earth** | connects the metal body of each appliance to a metal plate buried deep in moist ground; safety wire | green or green-yellow |

::: definition Earthing
**Earthing** is connecting the metal body of an appliance to the ground through a wire of
low resistance, so that any leaking current flows instantly into the earth instead of
through a person. It prevents electric shock and fires. The earth pin of a 3-pin plug is the
top, thickest pin.
:::

Different colours are used so that the live, neutral and earth wires are not mixed up and
faults are easy to find and repair. The switch and fuse are put in the **live wire** so that
when the switch is off or the fuse has melted, the appliance is completely cut off from the
high potential and is safe to touch.

```figure caption="House lamps are wired in parallel between the live and neutral wires, each with its own switch in the live wire; the fuse is also in the live wire."
fig, ax = plt.subplots(figsize=(5.0, 2.8))
ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
ax.plot([0.6, 9.5], [5.0, 5.0], color=SERIES[1], lw=2)
ax.plot([0.6, 9.5], [1.0, 1.0], color=INK, lw=2)
ax.text(0.5, 5.3, "live (220 V)", fontsize=7.8, color=SERIES[1])
ax.text(0.5, 0.45, "neutral", fontsize=7.8, color=INK)
ax.add_patch(plt.Rectangle((2.1, 4.8), 0.9, 0.4, fc="white", ec=INK))
ax.text(2.55, 4.35, "fuse", ha="center", fontsize=7.6, color=INK)
for x in (3.8, 6.0, 8.2):
    ax.plot([x, x], [5.0, 4.2], color=INK, lw=1.2)
    ax.plot([x, x + 0.35], [4.2, 3.75], color=INK, lw=1.2)
    ax.plot(x, 4.2, "o", ms=3, color=INK); ax.plot(x, 3.6, "o", ms=3, color=INK)
    ax.plot([x, x], [3.6, 2.85], color=INK, lw=1.2)
    ax.add_patch(plt.Circle((x, 2.5), 0.35, fc="#fff3c4", ec=INK))
    ax.plot([x - 0.24, x + 0.24], [2.26, 2.74], color=INK, lw=0.8)
    ax.plot([x - 0.24, x + 0.24], [2.74, 2.26], color=INK, lw=0.8)
    ax.plot([x, x], [2.15, 1.0], color=INK, lw=1.2)
    ax.text(x + 0.5, 3.95, "switch", fontsize=7.4, color=MUTED)
ax.text(8.7, 2.45, "lamp", fontsize=7.4, color=MUTED)
fig.tight_layout()
```

### 8.6.2 Wiring a three-pin plug

1. Switch off the main switch first (an adult must be present).
2. Unscrew and open the cover of the plug.
3. Remove about 1.5 cm of the outer insulation of the cable and expose the three wires;
   strip a little insulation from each.
4. Twist the bare strands of each wire.
5. Connect the **live** (red/brown) wire to the **right-hand** pin (the one with the fuse),
   the **neutral** (black/blue) wire to the **left-hand** pin, and the **earth** (green/yellow)
   wire to the **top** pin; tighten each screw.
6. Clamp the cable firmly with the cord grip so that it cannot pull out.
7. Replace and screw the cover; test with a tester before use.

::: caution Electricity can kill
Never touch switches with wet hands; never put fingers or metal into a socket; do not
overload a socket with many plugs; replace damaged wires; use the correct fuse and
earthed 3-pin plugs for metal appliances; switch off the main switch before any repair.
:::

## 8.7 The electric meter, the unit (kWh) and the electricity bill

The commercial unit of electrical energy is the **kilowatt-hour (kWh)**, called one
**unit**. One unit is the energy used by an appliance of power **1000 W (1 kW)** working for
**1 hour**. ($1\ \text{kWh}=1000\ \text{W}\times3600\ \text{s}=3.6\times10^6$ J.)

$$E=P\times N\times t$$

where $E$ is energy in kWh, $P$ the power of one appliance in kW, $N$ the number of
appliances and $t$ the time in hours. **Bill = units × rate.** (If the meter shows 40 units
and the rate is Rs 8 per unit, the bill is $40\times8=$ Rs 320.)

::: example Monthly bill for bulbs (textbook example)
**Problem.** Four 60 W bulbs are used for 3.5 h a day. Find the monthly (30-day) bill at
Rs 8.50 per unit.

**Solution.** $P=60$ W $=0.06$ kW, $N=4$, $t=3.5$ h.
Energy per day $=0.06\times4\times3.5=0.84$ kWh.
Energy per month $=0.84\times30=25.2$ units.
Bill $=25.2\times8.50=$ **Rs 214.20**.
:::

::: example Bill for several appliances
**Problem.** A house uses five 20 W LED bulbs for 6 h a day, one 1000 W rice cooker for 1 h a
day and one 100 W television for 4 h a day. Find the units used in 30 days and the bill at
Rs 10 per unit.
**Solution.** LED bulbs: $0.02\times5\times6=0.6$ kWh. Cooker: $1\times1\times1=1.0$ kWh.
TV: $0.1\times1\times4=0.4$ kWh. Per day $=0.6+1.0+0.4=2.0$ kWh.
In 30 days $=2.0\times30=60$ units. Bill $=60\times10=$ **Rs 600**.
:::

::: tip Convert watts to kilowatts first
Divide the power in watts by 1000 before multiplying by hours; and change minutes into
hours (40 min $=\frac{40}{60}$ h). Most wrong answers come from skipping one of these steps.
:::

## 8.8 Magnetic effect of current; the electric bell

A wire carrying current produces a **magnetic field** around it (Oersted's discovery: a
compass needle near a current-carrying wire turns). A coil of wire on a soft-iron core
becomes a strong **electromagnet** while current flows and loses its magnetism when the
current stops. Its strength increases with more turns of wire and more current.

**Electric bell.** When the switch is pressed, current flows through the coils of an
electromagnet; it attracts a soft-iron **armature**, so the **hammer** strikes the **gong**.
As the armature moves, the circuit breaks at the **contact screw**; the electromagnet stops
working and a spring pulls the armature back, which closes the circuit again. This repeats
quickly, so the bell rings continuously while the switch is pressed.

Electromagnets are also used in cranes, motors, loudspeakers, relays, MRI machines and
magnetic door locks. The link between electricity and magnetism also works the other way:
moving a magnet in a coil produces current, which is how generators in hydropower plants work.

```photo id="sci10/electromagnet" caption="An electromagnet lifting scrap iron. Its magnetism lasts only while current flows in the coil." width="58"
```

## Chapter summary

- Magnets attract iron, cobalt and nickel; like poles repel, unlike poles attract; a
  suspended magnet points north–south.
- Natural magnet: lodestone. Artificial: bar, horseshoe, electromagnet.
- Molecular theory (Weber, Ewing): aligned molecular magnets = magnet; random = unmagnetised;
  all aligned = saturation. Heating, hammering, a.c. and like-pole storage demagnetise.
- Earth is a magnet (molten iron in the outer core). Declination: angle between geographic
  and magnetic meridians. Dip: angle with the horizontal (0° at magnetic equator, 90° at poles).
- $V=IR$ (Ohm's law); current in A, p.d. in V, resistance in Ω.
- House supply 220 V: meter → main switch → distribution board (MCB/fuse) → switches →
  loads in parallel. Fuse and switch in the live wire; earth wire protects from shock.
- 1 unit = 1 kWh; $E=P\times N\times t$; bill = units × rate.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. Which of the following is a natural magnet? <span class="marks">[1]</span>
   (a) limestone (b) nickel (c) lodestone (d) electromagnet
2. In household wiring, the switch is connected in the <span class="marks">[1]</span>
   (a) neutral wire (b) earth wire (c) fuse wire (d) live wire
3. How is earthing done in household wiring? <span class="marks">[1]</span>
   (a) any wire is buried in the earth (b) a green wire is buried in the earth (c) a wire from the plug is joined to the earth (d) an earth wire from every appliance is connected to a plate buried in the earth
4. The angle of dip at the magnetic equator is <span class="marks">[1]</span>
   (a) 0° (b) 42° (c) 60° (d) 90°
5. The fuse wire is made of an alloy of <span class="marks">[1]</span>
   (a) copper and zinc (b) tin and lead (c) iron and nickel (d) tungsten
6. One unit of electricity equals <span class="marks">[1]</span>
   (a) 1 W h (b) 1 kW h (c) 1 kW s (d) 1000 kW h

::: note Answers to Group A
**1.** (c). **2.** (d). **3.** (d). **4.** (a) — the needle lies horizontal. **5.** (b) — low melting point. **6.** (b).
:::

**Group B — Short answer (2 marks each)** *(Textbook exercise 2–4.)*

1. Differentiate: (a) natural and artificial magnet (b) plug and socket (c) live and neutral wire. <span class="marks">[3]</span>
2. Give reasons: (a) A magnet is demagnetised by hammering. (b) The angle of dip at the magnetic poles is 90°. (c) Different coloured wires are used in house wiring. (d) The fuse is connected in the live wire. <span class="marks">[4]</span>
3. What are the causes of demagnetisation? Explain one. <span class="marks">[2]</span>
4. Explain the molecular theory of magnetism with a diagram. <span class="marks">[2]</span>
5. Write three uses of magnets. <span class="marks">[2]</span>
6. What is terrestrial magnetism? Write three applications. <span class="marks">[2]</span>
7. "Magnetisation of magnetic materials in nature is the effect of terrestrial magnetism." Justify. <span class="marks">[2]</span>
8. What is earthing? Why is it necessary? <span class="marks">[2]</span>
9. According to the molecular theory, can a magnetic substance become a magnet and a magnet lose its magnetism? Justify. <span class="marks">[2]</span>
10. Is there a connection between magnetism and electricity? Explain with an activity. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** (a) See the table in 8.1.1. (b) A plug is fitted at the end of an appliance's cable and has pins; a socket is fixed on the wall, connected to the supply, and has holes into which the plug fits. (c) The live wire carries current at high potential (220 V), gives a shock, and has the switch and fuse; the neutral wire is at zero potential and completes the circuit.
**2.** (a) The jolts disturb the aligned molecular magnets into random closed chains. (b) At the magnetic poles the earth's field is vertical, so a freely suspended needle points straight down, at 90° to the horizontal. (c) So that live, neutral and earth wires are not confused, and faults can be found and repaired safely. (d) When the fuse melts, the appliance is cut off from the high potential and becomes safe; a fuse in the neutral would leave the appliance live.
**3.** Heating, hammering or dropping, passing a.c. through a coil around it, keeping like poles together, natural ageing. *Heating:* heat makes the molecular magnets vibrate so strongly that they lose their parallel alignment and form closed chains.
**4.** See 8.1.2 and its figure: random closed chains in unmagnetised iron; aligned open chains in a magnet; all aligned at saturation.
**5.** Electric motors, generators and bells; compass for direction; MRI in hospitals; electromagnetic cranes; speakers and hard disks.
**6.** The magnetic property of the earth, produced by molten iron and nickel moving in the outer core. Applications: compass navigation; shielding the earth from charged particles of the solar wind; estimating the age of rocks and finding ores.
**7.** Iron ores lying in the earth's field for ages become magnetised, forming lodestone; an iron rod buried north–south for a long time becomes a weak magnet. Both are magnetised by the earth's field.
**8.** Connecting the metal body of an appliance to the ground through a low-resistance wire. If the live wire touches the body, the current flows into the ground at once (and the fuse/MCB trips) instead of through a person, preventing shock and fire.
**9.** Yes. Magnetism depends only on the arrangement of the molecular magnets. If the random molecules of iron are aligned (by rubbing with a magnet or by current), the iron becomes a magnet; if the aligned molecules of a magnet are disturbed (by heating, hammering or a.c.), it loses its magnetism. Non-magnetic substances like wood have no molecular magnets and cannot be magnetised.
**10.** Yes. Wind insulated wire round an iron nail and connect it to a cell through a switch: the nail attracts pins only while current flows — current produces magnetism. Conversely, moving a magnet in a coil produces current (generator).
:::

**Group C — Numerical and long answer (4 marks each)**

1. Bhawana's meter records 15 units in 15 days. Find the average monthly bill at Rs 9.50 per unit. <span class="marks">[2]</span>
2. Eight 25 W bulbs are used for 4 h 40 min daily. Find the energy used per day in units. <span class="marks">[2]</span>
3. Sharmila's sub-meter records 8.5 units in a month (30 days) for one 65 W bulb. Find the average daily time the bulb is used. <span class="marks">[2]</span>
4. A municipality runs 14 street lights of 1500 W each for 6.5 h daily. Find the monthly (30-day) bill at Rs 12.50 per unit. <span class="marks">[3]</span>
5. What is household electrification? Name the devices from the meter to the lamp, and write the features of the live and neutral wires. <span class="marks">[4]</span>
6. Write the steps of wiring a three-pin plug. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** Units per day $=\frac{15}{15}=1$; per month $=1\times30=30$ units. Bill $=30\times9.50=$ **Rs 285**. *(The textbook prints Rs 1425; that would need 150 units a month, i.e. 75 units in 15 days. With the data as given, the bill is Rs 285.)*
**2.** $P=25$ W $=0.025$ kW, $N=8$, $t=4\frac{40}{60}=4.667$ h. $E=0.025\times8\times4.667=0.933$ units. *(The textbook prints 0.0932; the correct value is about 0.933 units.)*
**3.** Units per day $=\frac{8.5}{30}=0.2833$ kWh. $t=\frac{E}{P}=\frac{0.2833}{0.065}=4.36$ h (about 4 h 22 min).
**4.** $E$ per day $=1.5\times14\times6.5=136.5$ units; per month $=136.5\times30=4095$ units. Bill $=4095\times12.50=$ **Rs 51,187.50**.
**5.** Bringing electricity from the power house to homes through transmission lines and wiring the house safely. Devices: service line → electric meter → main switch → distribution board with MCBs/fuses → switches → lamps and sockets. Live wire: high potential (220 V), gives shock, red/brown, has switch and fuse. Neutral wire: zero potential, completes the circuit, black/blue.
**6.** See the seven steps in 8.6.2 (switch off; open cover; strip insulation; twist strands; live to right pin with fuse, neutral to left, earth to top; clamp the cord; close and test).
:::
