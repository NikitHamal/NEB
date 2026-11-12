---
subject: Hardware Workshop
grade: BCA Semester 1
unit: 1
title: Introduction to Hardware (Electronic Components)
area: BCA 106 · Hardware Workshop · Unit 1
---

Every computer is built from a few dozen kinds of electronic component. Before you assemble a PC you should be able to pick up a loose resistor, capacitor, diode, transistor or chip, say what it is, read its markings, test it with a multimeter and judge whether it is working. This unit is the bench manual for that skill: electrical basics and safety, passive components, active components, connectors and switches, datasheets and packages, and testing.

::: key What this unit gives you
- Voltage, current, resistance and power with Ohm's law, and the safety rules of the electronics bench.
- Passive components: resistors (colour code, series and parallel), capacitors and inductors.
- Active components: diodes, LEDs, transistors, MOSFET logic gates and integrated circuits.
- Connectors, switches, relays, buzzers and crystals; reading a datasheet; package types (DIP, SMD, TO-92, TO-220).
- Testing with a multimeter, component tester and ESR meter; a component-identification test.
:::

## 1.1 Introduction to electronics and bench safety

**Electronics** deals with circuits in which small currents carry power or information. Three quantities describe every circuit:

| Quantity | Symbol | Unit | Meaning |
|---|---|---|---|
| Voltage | V | volt (V) | the electrical "push" between two points |
| Current | I | ampere (A) | the flow of charge per second |
| Resistance | R | ohm (Ω) | opposition to current |
| Power | P | watt (W) | rate of energy use, P = V × I |

**Ohm's law:** V = I × R. Hence I = V / R and R = V / I. Power can also be written P = I²R = V² / R.

::: example Worked example: Ohm's law and power
A 330 Ω resistor is connected across a 9 V battery. Current I = 9 / 330 = **27.3 mA**. Power P = V × I = 9 × 0.0273 = **0.245 W**, so a 0.25 W resistor would run at its limit and a **0.5 W** part is the safe choice (rule: choose at least twice the computed power).
:::

**Multiples.** 1 kΩ = 1,000 Ω; 1 MΩ = 1,000,000 Ω; 1 mA = 0.001 A; 1 µF = 10⁻⁶ F; 1 nF = 10⁻⁹ F; 1 pF = 10⁻¹² F.

**Voltage divider.** Two resistors R1 and R2 in series across a source V give an output across R2 of Vout = V × R2 / (R1 + R2). With 9 V, R1 = 10 kΩ and R2 = 5 kΩ, Vout = 9 × 5 / 15 = **3 V**. Sensors and the voltage-sense circuits on motherboards use this idea.

**Safety on the electronics bench**

1. Work only on circuits that are **switched off and unplugged**; use a low-voltage bench supply (3 to 12 V) for practice. Never work on mains voltage (230 V in Nepal) in this lab.
2. Wear an **ESD wrist strap** connected to a grounded point; CMOS chips and MOSFETs are destroyed by static you cannot feel.
3. Check polarity before powering: electrolytic capacitors, LEDs, diodes and ICs can fail or burst if connected backwards.
4. Use the right range on the multimeter and move the red lead back to the V/Ω socket after measuring current; a meter left on the 10 A range will blow a fuse or short a supply.
5. Soldering irons reach 350 °C: use the stand, ventilate the fumes and never touch the tip.
6. Discharge large capacitors with a resistor (not a screwdriver) before touching a circuit.

**Basic electronics kit.** Breadboard (a solderless board whose rows are connected in strips), jumper wires, assorted resistors, capacitors, diodes, LEDs, transistors, ICs, a digital multimeter (DMM), a component tester, a regulated power supply, a soldering iron and desoldering pump, tweezers, side cutters and a magnifier.

## 1.2 Passive components

A **passive** component does not amplify or switch a signal; it only stores, dissipates or passes energy.

### Resistors

A resistor limits current and sets voltages. Its value is printed as **colour bands**, read from the end nearest to the first band.

| Colour | Digit | Multiplier | Tolerance |
|---|---|---|---|
| Black | 0 | ×1 | |
| Brown | 1 | ×10 | ±1 % |
| Red | 2 | ×100 | ±2 % |
| Orange | 3 | ×1 k | |
| Yellow | 4 | ×10 k | |
| Green | 5 | ×100 k | ±0.5 % |
| Blue | 6 | ×1 M | ±0.25 % |
| Violet | 7 | ×10 M | ±0.1 % |
| Grey | 8 | | ±0.05 % |
| White | 9 | | |
| Gold | | ×0.1 | ±5 % |
| Silver | | ×0.01 | ±10 % |

In a **four-band** resistor, bands 1 and 2 are digits, band 3 is the multiplier and band 4 the tolerance. A **five-band** resistor has three digits, then multiplier and tolerance.

::: example Worked example: reading the colour code
Yellow, violet, red, gold: digits 4 and 7, multiplier ×100, so 47 × 100 = **4,700 Ω = 4.7 kΩ ±5 %**; the real value lies between 4,465 Ω and 4,935 Ω. Orange, orange, brown, gold is 33 × 10 = **330 Ω**. Brown, black, orange, gold is 10 × 1,000 = **10 kΩ**. A five-band brown, black, black, red, brown is 100 × 100 = **10 kΩ ±1 %**.
:::

```svgfig label="1.1" caption="A 4.7 kilo-ohm resistor with bands yellow, violet, red and gold. The first two bands are digits (4, 7), the third is the multiplier (x100 = 2 zeros) and the fourth the tolerance (5 per cent). Always read from the side where the bands are closer to the end."
f = Fig(760, 190)
f.line(120, 70, 200, 70, color="#64748b", sw=3)
f.line(560, 70, 640, 70, color="#64748b", sw=3)
f.box(200, 40, 360, 60, "", fill="#e7d3a8", stroke="#7c5a1a")
for x, c in [(235, "#facc15"), (285, "#7c3aed"), (335, "#dc2626"), (500, "#c9a227")]:
    f.box(x, 40, 22, 60, "", fill=c, stroke=c)
for x, s in [(246, "1st band\nyellow = 4"), (296, "2nd band\nviolet = 7"), (346, "3rd band\nred = x100"), (511, "4th band\ngold = 5 %")]:
    f.arrow([(x, 138), (x, 104)], color=NAVY)
    f.text(x, 158, s, size=10.5, color=NAVY, bold=True)
f.text(430, 24, "47 x 100 = 4,700 ohm = 4.7 kilo-ohm, tolerance 5 %", size=11.5, color=SLATE, bold=True)
```

**Series and parallel.** In **series** the values add: R = R1 + R2 (1 kΩ + 2.2 kΩ = 3.2 kΩ). In **parallel** the reciprocals add: 1/R = 1/R1 + 1/R2, so two equal resistors halve the value (1 kΩ ∥ 1 kΩ = 500 Ω) and for two different ones R = R1 × R2 / (R1 + R2): 470 Ω ∥ 330 Ω = 155,100 / 800 = **193.9 Ω**, always less than the smaller one.

**Types.** Carbon-film and metal-film (general use, 0.25 W to 1 W), wire-wound (high power), **variable** resistors or potentiometers (volume knobs, trimmers), **thermistors** (NTC: resistance falls as temperature rises; used for temperature sensing) and **LDRs** (resistance falls in light). **Power rating:** 1/8 W, 1/4 W, 1/2 W and 1 W are common; the part must dissipate P = I²R without overheating.

**SMD resistors** on a motherboard carry numbers, not colours: **103** means 10 × 10³ = 10 kΩ, **472** is 4.7 kΩ, **100** is 10 Ω, and **R22** is 0.22 Ω.

### Capacitors

A capacitor stores energy in an electric field between two plates. Capacitance C is measured in **farads**; practical values are microfarads (µF), nanofarads (nF) and picofarads (pF). It blocks steady (DC) current but passes changing (AC) signals, so it is used for **smoothing** power supplies, **decoupling** chips, timing and filtering.

| Type | Features | Where you find it |
|---|---|---|
| Ceramic | small, no polarity, 1 pF to 1 µF, marked **104** = 10 × 10⁴ pF = 0.1 µF | beside every chip on the motherboard (decoupling) |
| Electrolytic | large values (1 µF to 10,000 µF), **polarised** (negative stripe), voltage rating printed | PSU and motherboard power circuits |
| Polymer / solid | long life, low ESR, no leaking | modern motherboard VRM, graphics cards |
| Film | stable, non-polar | audio, power-factor correction |
| Tantalum | compact, polarised, fails short if over-volted | portable devices |

**Capacitor code.** Three digits: the first two are digits, the third is the number of zeros, in picofarads: 103 = 10,000 pF = **10 nF**; 104 = **100 nF**; 473 = 47,000 pF = **47 nF**. Add the voltage rating (for example 16 V, 25 V).

**Combining.** In parallel capacitances **add** (10 µF + 10 µF = 20 µF); in series 1/C = 1/C1 + 1/C2 (10 µF in series with 10 µF = 5 µF).

::: example Worked example: RC time constant and stored energy
A 10 kΩ resistor charging a 100 µF capacitor has time constant τ = RC = 10,000 × 0.0001 = **1 s**. After one τ the capacitor is at 63 % of the supply; after 5τ = 5 s it is at 99 %. A 1,000 µF capacitor at 12 V stores E = ½CV² = 0.5 × 0.001 × 144 = **0.072 J**. That is little energy, but large PSU capacitors (hundreds of volts) can still give a painful shock after unplugging, which is why you never open a power-supply case.
:::

**Failure sign:** a bulging top, a leak of brown fluid or a vent split on an electrolytic capacitor; such boards crash randomly and must be recapped or replaced.

### Inductors

An inductor is a coil of wire that stores energy in a magnetic field; it resists changes of current. Inductance L is measured in **henry** (H), usually mH or µH. Uses: smoothing and filtering in switching power supplies (the "chokes" beside the CPU socket), transformers, relays and motors. Time constant of an inductor with a resistor: τ = L/R (10 mH with 100 Ω gives 0.1 ms). Energy stored: ½LI². A **transformer** is two coils on one core; the voltage ratio equals the turns ratio (a 230 V to 12 V adapter has about 19:1 turns).

**Identification.** Passive parts on a board: resistors are rectangles with numbers (103), ceramic capacitors are brown or beige and unmarked, electrolytics are cylinders with a stripe, chokes are ferrite rings or square cans marked with µH (for example **R47** = 0.47 µH).

## 1.3 Active components

An **active** component can control current, switch or amplify with the help of an external supply.

### Diodes and LEDs

A **diode** conducts in one direction only, from **anode (+)** to **cathode (−, the stripe)**. In **forward bias** (anode positive) a silicon diode starts to conduct at about **0.6 to 0.7 V** (Schottky 0.2 to 0.3 V, germanium 0.3 V); in **reverse bias** it blocks, apart from a tiny leakage, until breakdown.

| Diode | Use |
|---|---|
| Rectifier (1N4007: 1 A, 1,000 V) | converts AC to DC in adapters and PSUs |
| Schottky | fast, low drop; in switching supplies and USB power paths |
| Zener | holds a fixed voltage in reverse breakdown (3.3 V, 5.1 V); simple regulators |
| LED | emits light when forward-biased; drop 1.8 V (red) to 3.3 V (blue/white) |
| Photodiode | produces current in light; remote receivers, fibre optics |

An **LED** needs a series resistor, because its current rises steeply with voltage: R = (Vs − Vf) / I.

::: example Worked example: LED resistor
Supply 5 V, red LED with Vf = 2 V, wanted current 20 mA: R = (5 − 2) / 0.020 = **150 Ω**, and the resistor dissipates 3 × 0.02 = 0.06 W. If you only have 180 Ω, I = 3 / 180 = **16.7 mA**, a little dimmer but safe. Without any resistor the LED would draw many times its rating and burn out.
:::

```svgfig label="1.2" caption="An LED with its series resistor. Current flows from the positive terminal through the resistor into the anode (long lead) and out of the cathode (short lead, flat side) to the negative terminal. With 5 V, a 2 V LED and 150 ohm, the current is 20 mA."
f = Fig(760, 210)
f.box(40, 70, 90, 70, "5 V\nsupply", fill=SAND, stroke=AMBER, size=11, bold=True)
f.line(130, 85, 250, 85, color=SLATE, sw=2)
f.box(250, 65, 110, 40, "R = 150 ohm", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.line(360, 85, 520, 85, color=SLATE, sw=2)
f.poly([(520, 60), (520, 110), (570, 85)], fill=ROSE, stroke=RED, label="")
f.line(570, 60, 570, 110, color=RED, sw=3)
f.line(570, 85, 640, 85, color=SLATE, sw=2)
f.line(640, 85, 640, 170, color=SLATE, sw=2)
f.line(640, 170, 130, 170, color=SLATE, sw=2)
f.line(130, 140, 130, 170, color=SLATE, sw=2)
f.arrow([(560, 40), (600, 14)], color=AMBER, sw=2)
f.arrow([(580, 45), (620, 19)], color=AMBER, sw=2)
f.text(545, 126, "anode (+)", size=10, color=RED, bold=True)
f.text(610, 126, "cathode (-)", size=10, color=RED, bold=True)
f.arrow([(160, 85), (230, 85)], color=TEAL, label="I = 20 mA", lpos=(195, 66))
f.text(380, 195, "Check: I = (5 V - 2 V) / 150 ohm = 20 mA; resistor power = 3 V x 20 mA = 0.06 W", size=10.5, color=SLATE)
```

**Testing a diode.** Set the multimeter to the diode symbol: red probe on the anode and black on the cathode shows **0.5 to 0.7 V** for silicon (about 1.8 V or more for an LED, which will glow faintly); reversed it shows **OL** (open). A diode that reads low both ways is **shorted**; one that reads OL both ways is **open**.

### Transistors

A **bipolar junction transistor (BJT)** has three terminals: **base (B)**, **collector (C)** and **emitter (E)**. A small base current controls a much larger collector current: Ic = β × Ib (β or hFE is typically 100 to 300). **NPN** types (BC547, 2N2222) conduct when the base is positive with respect to the emitter by about 0.7 V; **PNP** types (BC557, 2N2907) conduct when the base is pulled below the emitter.

Two uses: as an **amplifier** (in the active region) and as an **electronic switch** (driven hard into saturation or off), which is what every logic gate does.

::: example Worked example: transistor as a switch
A 5 V logic output must switch a relay coil that needs 100 mA through an NPN transistor with β = 100. The base current must be at least Ic / β = 0.1 / 100 = 1 mA; to be sure of saturation use about twice that, 2 mA. Rb = (5 − 0.7) / 0.002 = **2,150 Ω**, so choose the standard value **2.2 kΩ** (base current 4.3 / 2,200 = 1.95 mA). Add a **flyback diode** across the relay coil, because the coil produces a voltage spike when switched off.
:::

```svgfig label="1.3" caption="An NPN transistor switching a relay coil. A 2.2 kilo-ohm resistor limits the base current to about 2 mA; the flyback diode across the coil absorbs the voltage spike when the transistor turns off."
f = Fig(760, 230)
f.line(420, 20, 420, 60, color=SLATE, sw=2)
f.text(420, 12, "+5 V", size=10.5, color=AMBER, bold=True)
f.box(380, 60, 80, 56, "Relay\ncoil", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.line(420, 116, 420, 140, color=SLATE, sw=2)
f.circle(400, 168, 30, fill=BLUE, stroke=NAVY, label="NPN", size=10)
f.line(420, 138, 410, 148, color=SLATE, sw=2)
f.line(412, 190, 420, 214, color=SLATE, sw=2)
f.line(300, 214, 540, 214, color=SLATE, sw=2)
f.text(560, 218, "0 V", size=10.5, color=SLATE, bold=True, anchor="start")
f.box(190, 152, 90, 32, "2.2 k", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.line(280, 168, 372, 168, color=SLATE, sw=2)
f.line(100, 168, 190, 168, color=SLATE, sw=2)
f.text(100, 150, "logic input", size=10, color=TEAL, bold=True, anchor="start")
f.line(480, 60, 480, 116, color=SLATE, sw=2)
f.line(420, 60, 480, 60, color=SLATE, sw=2)
f.line(420, 116, 480, 116, color=SLATE, sw=2)
f.poly([(468, 70), (492, 70), (480, 100)], fill=ROSE, stroke=RED)
f.text(540, 88, "flyback diode", size=10.5, color=RED, bold=True, anchor="start")
f.text(440, 140, "C", size=10, color=NAVY, bold=True)
f.text(440, 200, "E", size=10, color=NAVY, bold=True)
f.text(352, 160, "B", size=10, color=NAVY, bold=True)
```

### MOSFET and logic gates

A **MOSFET** (metal-oxide-semiconductor field-effect transistor) has **gate (G)**, **drain (D)** and **source (S)**. The gate voltage, not a gate current, controls the channel, so it draws almost no current. An **N-channel** MOSFET turns on when the gate is about 2 to 4 V above the source; a **P-channel** one turns on when the gate is below the source. Power MOSFETs (for example the IRFZ44N) have an on-resistance of a few milliohms and are the switches in the CPU's voltage regulator on the motherboard.

Logic gates in CPUs and chips are built from complementary pairs (**CMOS**): a P-channel device connects the output to the supply, an N-channel device connects it to ground, and only one of the two conducts at a time, so the circuit uses power only while switching.

| Input A | Gate | P-channel | N-channel | Output |
|---|---|---|---|---|
| 0 (low) | NOT | on | off | **1** |
| 1 (high) | NOT | off | on | **0** |

For a **NAND** gate, two P-channel devices sit in parallel at the top and two N-channel devices in series at the bottom; the output is low only when A = 1 and B = 1 (A and B both high): NAND(0,0) = 1, NAND(0,1) = 1, NAND(1,0) = 1, NAND(1,1) = **0**. NAND is **universal**: any other gate can be built from it.

### Integrated circuits (ICs)

An **IC** packs thousands to billions of transistors on one silicon die. Pin 1 is marked with a dot or a notch; pins are numbered anticlockwise when seen from above.

| IC | What it does |
|---|---|
| 7400 series (7400 NAND, 7404 NOT, 7408 AND, 7432 OR, 7486 XOR) | logic gates, 5 V; 74LS (bipolar) and 74HC (CMOS) families |
| 555 timer | oscillator and timer; astable frequency f = 1.44 / ((R1 + 2R2)C) |
| Op-amp (LM358, LM741) | amplifier, comparator, filter |
| 7805 regulator | fixed 5 V from 7 to 25 V in, up to 1 A |
| Microcontroller (ATmega328) | tiny programmable computer |
| Memory, CPU, chipset | the main chips of a PC |

::: example Worked example: 555 astable (blinking LED)
With R1 = 1 kΩ, R2 = 68 kΩ and C = 10 µF: R1 + 2R2 = 137 kΩ, so f = 1.44 / (137,000 × 0.00001) = 1.44 / 1.37 = **1.05 Hz** (about one blink a second). The duty cycle (time high) is (R1 + R2) / (R1 + 2R2) = 69 / 137 = **50.4 %**.
:::

## 1.4 Connectors, switches, relays, buzzers and crystals

| Component | Purpose and identification | Quick test |
|---|---|---|
| Connectors and headers | joins boards and cables: pin headers (2.54 mm pitch), JST, Molex, USB, DC jack, SATA and ATX power | continuity beep between pin and wire |
| Switches | push button (momentary), toggle, slide, DIP switch; contacts "normally open (NO)" or "normally closed (NC)" | beeps when pressed (NO) |
| Relay | an electromagnet switches a separate high-power contact; coil rating (5, 12 V) is printed, contacts COM, NO, NC | coil resistance 50 to 400 Ω; click when powered |
| Buzzer | active buzzer beeps when given DC; passive buzzer needs a tone signal | short beep from a 3 to 5 V supply |
| Crystal | quartz resonator giving an exact clock (32.768 kHz for real-time clocks, MHz for CPUs); metal can with its frequency printed | needs an oscillator circuit; a meter cannot test it |
| Fuse | melts at its rated current | continuity must beep |

The **CMOS (RTC) crystal** on every motherboard is 32.768 kHz; dividing by 2¹⁵ = 32,768 gives exactly one pulse per second.

## 1.5 Reading datasheets and package types

A **datasheet** is the maker's specification. For any part read: **absolute maximum ratings** (never exceed), **recommended operating conditions**, the **pinout** diagram, key electrical characteristics (for example forward voltage, hFE, Rds(on)), the typical application circuit and the package drawing. Example from a BC547 datasheet: Vce(max) 45 V, Ic(max) 100 mA, hFE 110 to 800, package TO-92, pinout (flat side facing you) C-B-E or E-B-C depending on manufacturer, so always check the sheet.

**Package types**

| Package | Description | Typical parts |
|---|---|---|
| **Through-hole** | leads pass through the board and are soldered on the back | |
| DIP / PDIP | dual in-line, two rows of pins, 2.54 mm pitch; fits a breadboard | 7400 logic, 555, ATmega328 |
| TO-92 | small plastic half-cylinder with 3 leads | BC547, 2N2222, small regulators |
| TO-220 | plastic tab with hole for a heatsink, 3 leads | 7805, IRFZ44N, power transistors |
| **Surface-mount (SMD)** | pads on the board surface, no holes | |
| SOIC / SOT-23 | small gull-wing chips and three-leg transistors | op-amps, small MOSFETs |
| 0603 / 0805 | resistors and capacitors; 0603 is 1.6 × 0.8 mm | everything on a motherboard |
| QFP, BGA | chips with leads on four sides or a grid of solder balls underneath | CPU, chipset, RAM chips, GPU |

BGA chips cannot be hand-soldered; they need a rework station with hot air and pre-heating. Never try to reflow a chip with a lighter.

```photogrid label="1.1" cols="4" ratio="1.1" caption="Real components. (a) A metal-can power transistor (2N3055) with its base, emitter and case-collector pins. (b) Integrated circuits in DIP packages with pin 1 at the notch. (c) A power MOSFET in a TO-220 package with a heatsink tab. (d) A motherboard section where surface-mount parts, chokes and capacitors sit around the CPU socket."
@ photo id="bca101/transistor" cap="Power transistor, metal can"
fit 1.1
@ photo id="bca101/ic-dip" cap="ICs in DIP packages"
fit 1.1
@ photo id="bca101/mosfet" cap="Power MOSFET, TO-220"
fit 1.1
@ photo id="bca101/mobo" cap="Motherboard, SMD parts"
fit 1.1
```

## 1.6 Testing and troubleshooting components

A **digital multimeter (DMM)** measures DC and AC voltage, current, resistance, continuity and diode drop; many also measure capacitance and transistor gain (hFE). A **component tester** identifies the type and pinout of an unknown part automatically; an **ESR meter** measures the equivalent series resistance of a capacitor in circuit.

| Test | Meter setting | Good part | Faulty part |
|---|---|---|---|
| Resistor (out of circuit) | Ω range | within tolerance of the colour code | OL (burnt open) or far from the value |
| Continuity (cable, fuse, switch) | continuity (beep) | beeps | silent |
| Diode / LED | diode symbol | 0.5 to 0.7 V one way, OL the other | 0 V both ways (short) or OL both ways (open) |
| Capacitor | capacitance, or Ω range | value near label; resistance rises slowly as it charges | shorted (0 Ω) or open; low value |
| Electrolytic in circuit | ESR meter | under about 0.5 Ω for 1,000 µF at 16 V | high ESR (above about 1 Ω) |
| Transistor | diode test between B-E and B-C | 0.6 V from base to emitter and to collector (NPN) | short or open between any pair |
| DC supply | DC V | rated voltage (5 V rail 4.75 to 5.25 V) | low, noisy or zero |

**Rules:** switch the circuit off and discharge capacitors; **test resistors out of circuit**, because parallel paths change the reading; never measure resistance on a live circuit; touch the probes, not each other and not the metal tips with your fingers (your body resistance, about 100 kΩ, spoils a high-value reading).

**Faulty versus working: a systematic comparison.** Measure a part you know is good (a reference) and compare. A working 10 kΩ resistor reads 9.5 to 10.5 kΩ; one reading 14 kΩ has drifted (often burnt, with a darkened body). A 1,000 µF capacitor with ESR above 1 Ω, even if its capacitance looks right, causes the random reboots that bulging capacitors cause.

```photogrid label="1.2" cols="2" ratio="1.5" caption="Measuring instruments for the bench. (a) A digital multimeter with its range dial, V/Ω/mA sockets and probes. (b) A POST diagnostic card, a specialised tester that shows the boot code of a PC board (see Unit 7)."
@ photo id="bca106/meter" cap="Digital multimeter"
fit 1.5
@ photo id="bca106/postcard" cap="POST diagnostic card"
fit 1.5
```

## 1.7 Mini project and component identification test

**Mini project: blinking LED.** Build the 555 astable circuit of the worked example on a breadboard: R1 = 1 kΩ between supply and the discharge pin, R2 = 68 kΩ between the discharge and trigger pins, C = 10 µF to ground, output through a 330 Ω resistor to an LED. Measure the blink period with a stopwatch (it should be near 0.95 s: T = 1/1.05) and with the meter.

**Component identification test (typical items).** For each unknown part: (1) name the part; (2) read its value or marking; (3) state its package; (4) test it with the meter; (5) say whether it is good.

| Item | Marking | Expected answer |
|---|---|---|
| A | brown, black, red, gold | 1 kΩ ±5 %; carbon film; meter should read 950 to 1,050 Ω |
| B | 104 ceramic disc | 100 nF; non-polar |
| C | 470 µF 25 V, stripe on one side | electrolytic, polarised; stripe marks the negative lead |
| D | 1N4007 with a band | rectifier diode; band is the cathode |
| E | BC547 in TO-92 | NPN; pins C-B-E with the flat face towards you (check the datasheet) |
| F | 7805 in TO-220 | 5 V regulator; pins input, ground, output |
| G | 16 MHz in a metal can | quartz crystal (clock for a microcontroller) |

## 1.8 Eight rules for working with electronic components

1. **Read the marking first.** The colour code, the printed number or the part code tells you the value; never guess from size.
2. **Respect polarity.** LEDs, diodes, electrolytic capacitors and ICs have a right way round; check the stripe, the long lead or the notch before powering.
3. **Protect against static.** Use the wrist strap, hold chips by their edges and store MOSFETs and ICs in anti-static foam or bags.
4. **Limit the current.** Every LED needs a resistor; every transistor needs a base resistor; calculate it rather than trying values.
5. **Keep to the ratings.** Never exceed the voltage, current and power in the datasheet; leave a safety margin of at least 50 % to 100 %.
6. **Measure with the right setting.** Choose voltage, current or resistance mode before touching the probes; return the leads when done.
7. **Test out of circuit.** Remove (or isolate) a part before measuring its resistance or capacitance.
8. **Keep a tidy bench.** Label drawers, return parts after use and leave the supply switched off while you wire.

## Formula and fact sheet

- Ohm's law V = IR; P = VI = I²R = V²/R. Series R adds; parallel R = R1R2/(R1+R2).
- Colour code: 0 black, 1 brown, 2 red, 3 orange, 4 yellow, 5 green, 6 blue, 7 violet, 8 grey, 9 white; gold ±5 %, silver ±10 %.
- Capacitor code 104 = 100 nF; 103 = 10 nF. τ = RC; E = ½CV².
- LED resistor R = (Vs − Vf)/I. Silicon diode drop 0.6 to 0.7 V.
- Transistor switch: Ib ≥ Ic/β, with 2× overdrive; Rb = (Vin − 0.7)/Ib.
- 555 astable f = 1.44/((R1 + 2R2)C).
- Packages: DIP, TO-92, TO-220 (through-hole); SOT-23, 0603, QFP, BGA (surface-mount).

## Chapter summary

- Voltage, current, resistance and power are linked by Ohm's law; safe practice means a low-voltage supply, ESD protection and correct polarity.
- Passive components (resistors, capacitors, inductors) store or dissipate energy; their values are read from colour bands or printed codes.
- Active components (diodes, LEDs, BJTs, MOSFETs, ICs) switch and amplify; CMOS gates are built from complementary MOSFET pairs and NAND is universal.
- Connectors, switches, relays, buzzers and crystals complete a circuit; datasheets give ratings, pinouts and packages.
- A multimeter, component tester and ESR meter distinguish good parts from faulty ones, and parts must be tested out of circuit.

## Practice

1. State Ohm's law and find the current through a 220 Ω resistor on 5 V; find its power.
2. Decode the resistor bands: (a) red, red, brown, gold; (b) green, blue, orange, silver; (c) brown, black, black, orange, brown.
3. Find the equivalent of 1 kΩ, 2.2 kΩ and 4.7 kΩ (a) in series and (b) the equivalent of 470 Ω in parallel with 330 Ω.
4. Interpret the capacitor markings 104, 473 and 223, and explain how to recognise the negative lead of an electrolytic capacitor.
5. Calculate the series resistor for a green LED (Vf = 2.2 V, 15 mA) on a 5 V supply and choose the nearest standard value.
6. Explain forward and reverse bias and how to test a diode with a multimeter.
7. Compute the base resistor to switch a 60 mA load with a transistor of β = 100 from 5 V (use 2× overdrive).
8. Draw a CMOS inverter and explain why it uses almost no power when idle.
9. Name the package types DIP, TO-92, TO-220, SOT-23 and BGA with one part for each.
10. Compute the blink frequency of a 555 astable with R1 = 1 kΩ, R2 = 10 kΩ and C = 1 µF.

::: note Answers and worked solutions
**1.** V = IR. I = 5 / 220 = **22.7 mA**; P = 5 × 0.0227 = **0.114 W** (a 0.25 W resistor is enough).
**2.** (a) 22 × 10 = **220 Ω ±5 %**; (b) 56 × 1,000 = **56 kΩ ±10 %**; (c) 100 × 1,000 = **100 kΩ ±1 %**.
**3.** (a) 1 + 2.2 + 4.7 = **7.9 kΩ**; (b) 470 × 330 / 800 = **193.9 Ω**.
**4.** 104 = 10 × 10⁴ pF = **100 nF**; 473 = 47 × 10³ pF = **47 nF**; 223 = 22 × 10³ pF = **22 nF**. The negative lead is under the stripe (and is the shorter lead).
**5.** R = (5 − 2.2) / 0.015 = **186.7 Ω**; nearest standard value **180 Ω** (16 mA) or **220 Ω** (12.7 mA).
**6.** Forward bias: anode positive, conducts above about 0.7 V (silicon). Reverse bias: blocks. In diode mode the meter shows 0.5 to 0.7 V one way and OL the other.
**7.** Ib = 0.06 / 100 = 0.6 mA; overdriven 1.2 mA; Rb = (5 − 0.7) / 0.0012 = **3,583 Ω**, choose **3.3 kΩ**.
**8.** A P-channel device above and an N-channel below the output; one is always off, so no steady current flows from supply to ground; power is used only while the output changes.
**9.** DIP: 555 timer; TO-92: BC547; TO-220: 7805; SOT-23: small MOSFET; BGA: CPU or GPU chip.
**10.** f = 1.44 / ((1,000 + 20,000) × 10⁻⁶) = 1.44 / 0.021 = **68.6 Hz**.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q (5 marks). Explain the resistor colour code with two examples.**

A resistor's value is shown by coloured bands. In the common four-band type, the first two bands give digits, the third gives the multiplier (the number of zeros) and the fourth the tolerance (Figure 1.1). Digits: black 0, brown 1, red 2, orange 3, yellow 4, green 5, blue 6, violet 7, grey 8, white 9; gold as tolerance is ±5 % and silver ±10 %.

*Example 1.* Yellow, violet, red, gold: 4, 7, ×100, ±5 %, which is 4,700 Ω = **4.7 kΩ ±5 %**.
*Example 2.* Orange, orange, brown, gold: 3, 3, ×10, ±5 %, which is **330 Ω ±5 %**.

Always verify with a meter, out of circuit; the reading should lie within the tolerance (for 330 Ω: 313.5 to 346.5 Ω).

**Q (10 marks). Describe the passive and active electronic components, giving the function, symbol or marking and a test for each.**

*Introduction.* Electronic circuits use passive components, which store or dissipate energy, and active components, which switch or amplify with an external supply.

*Passive components.*

1. **Resistor.** Limits current; value from colour bands; V = IR; test: resistance range, out of circuit.
2. **Capacitor.** Stores charge; smooths, decouples and times; ceramic code 104 = 100 nF; electrolytic is polarised; test: capacitance or ESR meter; bulging means failure.
3. **Inductor.** Stores energy in a magnetic field; used in chokes and transformers; unit henry; test: continuity and inductance.

*Active components.*

1. **Diode.** Conducts one way; 0.7 V drop for silicon; test in diode mode (Figure 1.2 shows an LED circuit).
2. **LED.** A light-emitting diode that needs a series resistor R = (Vs − Vf)/I.
3. **Transistor (BJT).** A small base current controls a large collector current, Ic = β Ib; used as a switch or amplifier (Figure 1.3).
4. **MOSFET.** Voltage-controlled switch; the basis of CMOS logic and of motherboard voltage regulators.
5. **Integrated circuit.** Many transistors in one package (DIP, SMD, BGA); pin 1 at the notch; read the datasheet for pinout and ratings.

*Other components.* Switches, relays, buzzers, connectors and crystals complete the circuit and supply timing (32.768 kHz for the real-time clock).

*Conclusion.* Identifying a part, reading its datasheet and testing it with a multimeter before use are the basic bench skills for hardware work, and the same parts appear on every motherboard.
