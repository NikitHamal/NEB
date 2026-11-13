---
subject: Digital Logic
grade: BCA Semester 1
unit: 1
title: Introduction: Digital Signals, Logic Levels and the Clock
hours: 3
area: BCA 103 · Digital Logic · Unit 1
---

Every program you will ever write finally runs on circuits that know only two conditions: a voltage that is *high* and a voltage that is *low*. Digital logic is the study of how such two-valued signals are combined to do arithmetic, remember values and keep time. It is the bridge from the transistor to the CPU.

::: key What this unit gives you
- Analog vs digital signals, and why computers chose digital.
- Logic levels, noise margin, positive and negative logic.
- Pulse and clock waveform terms: period, frequency, duty cycle, rise/fall time.
- Integrated circuits: SSI, MSI, LSI, VLSI and the logic families TTL and CMOS.
- Family parameters worked with numbers: propagation delay, fan-out, power-delay product, CMOS dynamic power.
- Totem-pole, open-collector and tri-state outputs; pull-up sizing; Schmitt trigger and debouncing.
- Sampling, quantisation, SNR and the data rate of digital audio.
:::

## 1.1 Analog and digital signals

An **analog** signal varies continuously (a microphone voltage, temperature). A **digital** signal takes only a few discrete values, almost always two, written 0 and 1.

| | Analog | Digital |
|---|---|---|
| Values | continuous | discrete (0 and 1) |
| Noise | accumulates and cannot be removed | a small disturbance is ignored; signal can be regenerated |
| Storage | degrades on copying | exact copies, error detection and correction possible |
| Circuits | amplifiers, filters | gates, flip-flops, easy to integrate in huge numbers |
| Accuracy | limited by component tolerance | set by the number of bits |

Digital wins because a threshold decision removes noise: a 0.2 V ripple on a 5 V line changes nothing, but the same ripple on an analog audio signal is heard. Real-world quantities are converted with an **ADC** (analog-to-digital converter) on input and a **DAC** on output. A signal is *sampled* (measured at regular instants) and *quantised* (rounded to one of 2ⁿ levels); an n-bit ADC over a range V gives a step of V / 2ⁿ. For example 8 bits across 0–5 V gives 5 / 256 ≈ 19.5 mV.

```photogrid label="1.1" cols="2" ratio="1.55" caption="Analog versus digital. (a) A real oscilloscope showing a continuous triangle (analog) wave above a two-level square (digital) wave. (b) Sampling an analog wave and quantising each sample to a 3-bit code."
@ photo id="bca103/scope" cap="Tektronix 2235A: analog wave (top trace) and digital pulse train (bottom trace)"
fit 1.55
call 0.20 0.93 0.20 0.70 "Analog: any value"
call 0.20 0.07 0.20 0.32 "Digital: only HIGH or LOW"
@ svg cap="Sampling and 3-bit quantisation"
import math
f = Fig(400, 258)
f.line(30, 20, 30, 220, color=SLATE); f.line(30, 220, 385, 220, color=SLATE)
f.text(14, 18, "V", size=10, color=SLATE); f.text(380, 236, "time", size=10, color=SLATE)
yv = lambda v: 220 - v * 24
pts = [(30 + i * 3.5, yv(4 + 3.4 * math.sin(i / 100 * 2 * math.pi * 1.5))) for i in range(101)]
for a, b in zip(pts, pts[1:]): f.line(a[0], a[1], b[0], b[1], color=NAVY, sw=2)
prev = None
for k in range(16):
    x = 30 + (k + 0.5) * 22; t = (x - 30) / 3.5
    v = 4 + 3.4 * math.sin(t / 100 * 2 * math.pi * 1.5); q = max(0, min(7, round(v)))
    f.line(x, yv(v), x, yv(q), color=RED, sw=1, dash=True)
    f.circle(x, yv(q), 3.5, fill=RED, stroke=RED)
    if k % 3 == 0: f.text(x, 240, format(q, "03b"), size=8.5, color=TEAL, bold=True)
f.text(210, 10, "blue: analog   red: samples   teal: 3-bit codes", size=9, color=SLATE)
```

## 1.2 Logic levels and logic polarity

A digital circuit does not need an exact voltage, only that a signal falls inside the *high* band or the *low* band. For standard 5 V TTL:

| Quantity | Meaning | TTL value |
|---|---|---|
| V_IL(max) | highest input still read as 0 | 0.8 V |
| V_IH(min) | lowest input read as 1 | 2.0 V |
| V_OL(max) | worst-case output for 0 | 0.4 V |
| V_OH(min) | worst-case output for 1 | 2.4 V |

The voltage between 0.8 V and 2.0 V is the **forbidden (undefined) region**. The **noise margin** is how much noise a signal can carry and still be read correctly: NM_H = V_OH(min) − V_IH(min) = 2.4 − 2.0 = 0.4 V; NM_L = V_IL(max) − V_OL(max) = 0.8 − 0.4 = 0.4 V.

**Positive logic**: high = 1, low = 0. **Negative logic**: high = 0, low = 1. Under positive logic a gate that behaves as AND behaves as OR in negative logic; this is the duality used in De Morgan's theorem. Unless stated, assume positive logic.

**Logic families.** *TTL* (transistor-transistor logic, 74xx series, 5 V) was the classic family. *CMOS* (74HCxx, 4000 series) uses almost no power when idle, works over a wide supply range, and dominates today; every microprocessor and memory is CMOS. Comparison: CMOS has far lower static power and, at low supply voltage, can be made as fast as TTL; classic bipolar TTL draws milliwatts per gate even when idle. Fan-out is how many gate inputs one output can drive.

```svgfig label="1.2" caption="Valid TTL voltage bands. A gate guarantees outputs of at least 2.4 V (HIGH) or at most 0.4 V (LOW); the next gate accepts at least 2.0 V as HIGH and at most 0.8 V as LOW. The gaps are the noise margins."
f = Fig(760, 300)
yv = lambda v: 270 - v * 48
f.line(60, yv(0), 60, yv(5), color=SLATE, sw=1.6)
for v in range(6):
    f.line(54, yv(v), 60, yv(v), color=SLATE); f.text(46, yv(v) + 4, f"{v} V", size=9.5, color=SLATE, anchor="end")
f.text(210, 14, "OUTPUT of driving gate", size=11, color=NAVY, bold=True); f.text(560, 14, "INPUT of receiving gate", size=11, color=NAVY, bold=True)
f.box(100, yv(5), 220, yv(2.4) - yv(5), "HIGH output (V_OH min 2.4 V)", fill="#d1fae5", stroke=TEAL, size=10.5, bold=True)
f.box(100, yv(0.4), 220, yv(0) - yv(0.4), "LOW (V_OL max 0.4 V)", fill="#fee2e2", stroke=RED, size=9, bold=True)
f.box(450, yv(5), 220, yv(2.0) - yv(5), "HIGH input (V_IH min 2.0 V)", fill="#d1fae5", stroke=TEAL, size=10.5, bold=True)
f.box(450, yv(2.0), 220, yv(0.8) - yv(2.0), "forbidden zone (1 or 0?)", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.box(450, yv(0.8), 220, yv(0) - yv(0.8), "LOW input (V_IL max 0.8 V)", fill="#fee2e2", stroke=RED, size=10.5, bold=True)
f.arrow([(335, yv(2.4)), (435, yv(2.0))], color=TEAL, sw=1.6)
f.arrow([(335, yv(0.4)), (435, yv(0.8))], color=RED, sw=1.6)
f.text(385, yv(2.2) - 14, "NM_H = 0.4 V", size=10, color=TEAL, bold=True); f.text(385, yv(0.6) - 22, "NM_L = 0.4 V", size=10, color=RED, bold=True)
f.text(690, yv(5) + 16, "5 V supply", size=9, color=SLATE, anchor="start")
```

## 1.3 Pulses and the clock waveform

An ideal digital waveform is a square wave; a real one has a **rise time** t_r and **fall time** t_f, usually measured between 10 % and 90 % of the amplitude, and a **propagation delay** t_pd: the time from an input change to the output change.

For a periodic clock:

- **Period** T: the time of one complete cycle.
- **Frequency** f = 1 / T (hertz).
- **Duty cycle** = t_high / T × 100 %.

A 50 MHz clock has T = 1 / (50 × 10⁶) = 20 ns. A clock with a 6 ns high time in a 20 ns period has a 30 % duty cycle.

Edge terms matter for sequential circuits: the **positive (rising) edge** is the 0 → 1 transition, the **negative (falling) edge** is 1 → 0. A flip-flop triggered by an edge samples its input at that instant only. Two timing requirements follow: the data must be stable for a **setup time** before the edge and a **hold time** after it. If a path through gates takes longer than the clock period minus setup, the circuit fails; this is why there is a maximum clock frequency.

```svgfig label="1.3" caption="Clock waveform: period T, high time t_H, duty cycle t_H/T, rising and falling edges, and the setup and hold window around the active (rising) edge."
f = Fig(760, 250)
H, L = 60, 150; x0 = 70; hi, lo = 80, 120
x = x0; f.line(x - 20, L, x, L, color=NAVY, sw=2.6)
edges = []
for c in range(3):
    f.line(x, L, x, H, color=NAVY, sw=2.6); f.line(x, H, x + hi, H, color=NAVY, sw=2.6)
    f.line(x + hi, H, x + hi, L, color=NAVY, sw=2.6); f.line(x + hi, L, x + hi + lo, L, color=NAVY, sw=2.6)
    edges.append(x); x += hi + lo
f.box(edges[1] - 34, 36, 50, 140, "", fill=SAND, stroke=AMBER, r=2)
f.text(edges[1] - 14, 28, "setup | hold", size=9.5, color=AMBER, bold=True)
f.text(edges[0], 48, "rising edge (0→1)", size=9.5, color=TEAL, bold=True)
f.text(edges[0] + hi, 172, "falling edge (1→0)", size=9.5, color=RED, bold=True)
f.arrow([(edges[0], 200), (edges[1], 200)], color=NAVY, both=True, label="period T = 200 ns  (f = 1/T = 5 MHz)", lpos=(edges[0] + 100, 192))
f.arrow([(edges[1], 226), (edges[1] + hi, 226)], color=TEAL, both=True, label="t_H = 80 ns", lpos=(edges[1] + 40, 240))
f.text(40, H + 4, "1", size=11, color=SLATE, bold=True); f.text(40, L + 4, "0", size=11, color=SLATE, bold=True)
f.text(640, 100, "duty cycle = 80/200 = 40 %", size=10.5, color=NAVY, bold=True)
```

## 1.4 Digital logic operations and integrated circuits

Three basic operations underlie everything: **AND** (output 1 only if all inputs are 1), **OR** (output 1 if any input is 1), **NOT** (inversion). Unit 3 treats them fully. All digital computers, from a calculator to a data centre, are built from millions of these.

**Integrated circuit (IC) scale of integration**

| Scale | Gates per chip | Example |
|---|---|---|
| SSI (small) | < 12 | 7400 quad NAND |
| MSI (medium) | 12 – 99 | 74138 decoder, 7483 4-bit adder, counters |
| LSI (large) | 100 – 9,999 | small memory, early microprocessors |
| VLSI (very large) | 10,000 – 1,000,000 | 8086 (about 29,000 transistors) onwards |
| ULSI | > 1,000,000 | modern CPUs with billions of transistors |

(Boundaries differ slightly between books; learn the order and the examples.) ICs come in DIP (dual in-line package) form for breadboards or surface-mount for production. Chip pins are numbered anticlockwise from the notch; a 14-pin 74xx chip has V_CC on pin 14 and ground on pin 7.

**Digital computer.** A digital computer is a system of gates and flip-flops organised as a CPU (ALU + control unit + registers), memory and I/O, all synchronised by a clock. Understanding how a gate becomes an adder, and a flip-flop becomes a register, is the purpose of this subject.

```photogrid label="1.2" cols="3" ratio="1.0" caption="Inside the 74xx family: (a) an early ceramic 7447 BCD-to-seven-segment decoder, 16-pin DIP; (b) a microscope view of a 74HC00 die with its bond pad; (c) pinout of the 7400 quad NAND chip in DIP-14."
@ photo id="bca103/ic7447" cap="7447 in a ceramic DIP-16 package"
fit 1.0
mark 0.50 0.55 "1"
mark 0.28 0.20 "2"
mark 0.82 0.52 "3"
key 1 Part number printed on the package
key 2 Pins numbered anticlockwise from the notch end
key 3 Ceramic body protects the silicon die
@ photo id="bca103/hc00" cap="74HC00 die under a microscope"
fit 1.0
call 0.50 0.93 0.50 0.62 "Bond pad (wire to pin)"
call 0.50 0.07 0.55 0.15 "Type code in metal"
@ svg cap="7400: four NAND gates, DIP-14"
f = Fig(240, 262)
f.box(80, 20, 80, 224, "", fill=SOFT, stroke=NAVY)
f.poly([(110, 20), (130, 20), (130, 20), (120, 32), (110, 20)], fill=NAVY, stroke=NAVY)
L = ["1A", "1B", "1Y", "2A", "2B", "2Y", "GND"]; R = ["VCC", "4B", "4A", "4Y", "3B", "3A", "3Y"]
for i in range(7):
    y = 44 + i * 30
    f.line(60, y, 80, y, color=SLATE, sw=3); f.line(160, y, 180, y, color=SLATE, sw=3)
    f.text(46, y + 4, L[i], size=10, color=NAVY, bold=True, anchor="end"); f.text(194, y + 4, R[i], size=10, color=NAVY, bold=True, anchor="start")
    f.text(94, y + 4, str(i + 1), size=9, color=AMBER, bold=True); f.text(146, y + 4, str(14 - i), size=9, color=AMBER, bold=True)
f.text(120, 150, "7400", size=13, color=NAVY, bold=True)
```

## 1.5 Advantages and applications of digital systems

Digital systems are not used only because they are modern. They are used because a two-level signal is easy to protect, copy, store and process. Eight advantages explain why a phone call, a bank transfer and a photograph all travel as bits today.

1. **Noise immunity.** A digital receiver only asks "is this signal above or below the threshold?" A small ripple of 0.2 V on a 5 V line does not change the answer. This is why a Fonepay QR payment gives the same amount at the shop and in the bank, even over a poor mobile network.
2. **Exact copying and storage.** A stored number can be copied millions of times with no loss, while a tape copy of an analog song becomes noisier each time. A scanned citizenship certificate in the Nagarik App is bit-for-bit identical to the original file. Memory chips store these bits as charge or magnetic states.
3. **Error detection and correction.** Extra check bits (parity, CRC, Hamming code) can be added to the data. The receiver detects a flipped bit and, with the right code, repairs it. Banking switches such as NCHL's ConnectIPS depend on such checks to avoid wrong credit.
4. **Easy integration on silicon.** All logic is built from a few simple gates, and the same gate layout can be repeated millions of times. This is why a modern CPU with billions of transistors costs only a few thousand rupees. Analog circuits need large, precise components and do not shrink so well.
5. **Programmability.** The same hardware can do a new job by changing the stored program or the data. A single microcontroller can run an ATM screen today and a ticket machine tomorrow. Analog circuits need new components for each new function.
6. **Accuracy that is chosen, not hoped for.** The accuracy of a digital result depends on the number of bits, so adding bits adds accuracy. A 12-bit ADC separates 4096 levels, while a 16-bit ADC separates 65,536. The Department of Hydrology and Meteorology can log river levels at the resolution it needs.
7. **One format for every kind of information.** Text, sound, pictures and video all become bits, so one network carries all of them. Nepal Telecom sends a voice call, a message and a video over the same digital core. This sharing lowers the cost of equipment and cables.
8. **Easy processing, encryption and compression.** Once data is digital, a program can compress it, encrypt it or search it in seconds. The e-Passport, the Tribhuvan University EMIS and online result systems store records in such compact, protected form.

**Limitations.** Digital systems need sampling and quantisation, so some information is lost (quantisation error). They need more bandwidth than a simple analog signal, a clock, and A/D and D/A converters at the boundary with the real world. A power failure can erase volatile memory.

## 1.6 Logic families and their parameters

A **logic family** is a set of gates and chips built with the same technology, the same supply voltage and the same input and output levels, so that any chip of the family can be wired to any other without extra parts. Section 1.2 gave the standard TTL levels; the families differ in how fast they are, how much power they use and how many gates one output can drive.

| Family | Typical delay per gate | Power per gate (static) | Power-delay product | Remark |
|---|---|---|---|---|
| 74 (standard TTL) | 10 ns | 10 mW | 100 pJ | the original 7400 series |
| 74S (Schottky) | 3 ns | 19 mW | 57 pJ | fast but power-hungry |
| 74LS (low-power Schottky) | 9.5 ns | 2 mW | 19 pJ | the classroom favourite for decades |
| 74ALS (advanced LS) | 4 ns | 1.2 mW | 4.8 pJ | faster and cooler than LS |
| 74HC (high-speed CMOS) | about 8 ns | a few microwatts | very small at low speed | rises with clock rate (below) |

(These are the usual textbook and datasheet-typical figures; always read the datasheet of the actual chip, because delay changes with supply voltage, temperature and load.)

The **power-delay product** (PDP) is power multiplied by propagation delay. It is measured in picojoules and is the energy used for one switching event, so it is the fairest single number to compare families: a low value means a family is both quick and frugal. For the 74LS gate, 9.5 ns × 2 mW = 19 pJ; for standard TTL, 10 ns × 10 mW = 100 pJ. LS is therefore about five times better than the original series.

**CMOS draws power only when it switches.** A CMOS gate has almost no static current, but each output change charges and discharges the load capacitance C. The dynamic power is

P = C × V² × f

where V is the supply voltage and f the switching frequency. For a load of 20 pF at 5 V and 1 MHz, P = 20×10⁻¹² × 25 × 10⁶ = 0.5 mW. At 3.3 V it is 20×10⁻¹² × 10.89 × 10⁶ = 0.218 mW, and at 3.3 V and 100 MHz it is 21.8 mW. This explains two design habits: lowering the supply voltage is the most effective way to save power (the voltage is squared), and a CMOS design that is quiet at 1 MHz can still become hot at 100 MHz.

**Fan-out** is the number of gate inputs one output can drive without leaving its guaranteed levels. It is limited by current in both states:

fan-out = min( I_OL(max) / I_IL(max) , I_OH(max) / I_IH(max) )

::: example Worked example: fan-out of standard TTL and LS TTL
Standard 74 gate: I_OL(max) = 16 mA, I_IL(max) = 1.6 mA gives 16 / 1.6 = 10 in the LOW state; I_OH(max) = 0.4 mA and I_IH(max) = 40 µA give 400 / 40 = 10 in the HIGH state. Fan-out = **10**.

74LS gate: I_OL(max) = 8 mA, I_IL(max) = 0.4 mA gives 20; I_OH(max) = 0.4 mA, I_IH(max) = 20 µA gives 20. Fan-out = **20**.

CMOS inputs draw almost no steady current, so their fan-out is limited not by current but by the input capacitance that slows the edge; a practical limit of about 50 is quoted for 74HC.
:::

**Propagation delay** is the time between a change at the input and the resulting change at the output, measured at the 50 % points. It has two values: t_pHL (output falling) and t_pLH (output rising). Their mean is used for estimates. If t_pHL = 8 ns and t_pLH = 12 ns, the average is 10 ns, and a chain of five such gates adds up to 50 ns. If a flip-flop after the chain needs 20 ns of setup time, the shortest clock period that works is 50 + 20 = 70 ns, so the clock cannot exceed 1 / 70 ns ≈ 14.3 MHz. This calculation, repeated for the slowest path of a design, is how the maximum clock rate of a processor is found.

**Interfacing.** A 74HC chip fed from a TTL output may fail, because the TTL HIGH of 2.4 V is below the 3.5 V that a 5 V HC input needs. The 74HCT chips solve this: they are CMOS inside but have TTL-compatible input thresholds. Mixing 5 V and 3.3 V parts needs a level shifter, or at least a check that the HIGH output of the lower-voltage part exceeds V_IH of the other.

## 1.7 Output stages: totem-pole, open-collector and tri-state

How the last transistors of a gate are arranged decides what you may do with its output.

**Totem-pole output.** A standard TTL gate has two transistors in series between the supply and ground. For HIGH the upper one conducts and the lower is off; for LOW it is the opposite. The output is therefore driven actively in both states, which gives sharp edges and a low output resistance. The price is that **two totem-pole outputs must never be joined together**: if one drives HIGH and the other LOW, a large current flows from the supply through both, and the logic level is neither 0 nor 1. The same fault is called **bus contention**.

**Open-collector (open-drain) output.** Here the upper transistor is missing. The output can pull the line LOW, but for HIGH it only lets go, so an external **pull-up resistor** to the supply must raise the line. Several open-collector outputs may share a line: the line is HIGH only if every output lets go, and LOW if any output pulls down. This is the **wired-AND**. It is used for interrupt-request lines, for the I²C bus, and for driving loads such as LEDs and relays at a voltage or current that differs from the logic supply.

The pull-up value is a compromise. If it is too small, the LOW output must sink too much current; if too large, the line rises slowly and the leakage of the off outputs plus the inputs drops the voltage below V_OH(min).

::: example Worked example: pull-up resistor for a wired-AND line
Three open-collector TTL outputs (I_OH leakage 250 µA each) share a line that feeds four standard TTL inputs (I_IL = 1.6 mA, I_IH = 40 µA). Supply 5 V, V_OL(max) = 0.4 V, V_OH(min) = 2.4 V, I_OL(max) = 16 mA.

Minimum R (one output sinks the current of the pull-up and of the four loads when LOW): R_min = (5 − 0.4) / (16 mA − 4 × 1.6 mA) = 4.6 / 9.6 mA ≈ **479 Ω**.

Maximum R (HIGH state: the pull-up must supply three leakages and four input currents and still leave 2.4 V): R_max = (5 − 2.4) / (3 × 0.25 mA + 4 × 0.04 mA) = 2.6 / 0.91 mA ≈ **2857 Ω**.

Any standard value between about 500 Ω and 2.8 kΩ works, for example 1 kΩ.
:::

**Tri-state output.** A tri-state (three-state) buffer has an extra **enable** input. When enabled it behaves as a normal buffer, driving 0 or 1. When disabled its output is **high impedance (Hi-Z)**: electrically disconnected, neither HIGH nor LOW. Many tri-state outputs can therefore share one wire, a **bus**, provided that only one is enabled at a time.

| Enable E | Input A | Output Y |
|---|---|---|
| 0 | X | Hi-Z (disconnected) |
| 1 | 0 | 0 |
| 1 | 1 | 1 |

Memory chips, registers and I/O devices in a computer all put their data on the same data bus through tri-state outputs, and the address decoder of Unit 3 makes sure that exactly one enable is active. The 74244 (octal buffer) and 74245 (bus transceiver) are the common chips.

```svgfig label="1.5" caption="Three tri-state buffers share one data bus. The control logic enables only one (here the register B buffer); the other two are in the high-impedance state, so there is no contention."
f = Fig(760, 270)
f.text(380, 18, "ENABLE lines come from an address decoder (one-hot)", size=10.5, color=NAVY, bold=True)
names = ["Register A", "Register B", "Register C"]; en = [0, 1, 0]
for i, n in enumerate(names):
    y = 44 + i * 64
    f.box(30, y, 120, 40, n, fill=SOFT, stroke=NAVY, size=11, bold=True)
    f.line(150, y + 20, 215, y + 20, color=SLATE, sw=1.6)
    f.poly([(215, y + 4), (215, y + 36), (260, y + 20)], fill="#ffffff", stroke=NAVY, sw=1.6)
    f.line(260, y + 20, 600, y + 20, color=SLATE, sw=1.6)
    f.line(237, y - 14 if i else 28, 237, y + 10, color=TEAL if en[i] else RED, sw=1.6)
    f.text(330, y + 14, "E = " + str(en[i]), size=10.5, color=TEAL if en[i] else RED, bold=True)
    f.text(330, y + 34, "drives the bus" if en[i] else "Hi-Z (disconnected)", size=10, color=SLATE)
f.line(600, 64, 600, 192, color=NAVY, sw=3)
f.arrow([(600, 128), (650, 128)], color=NAVY, sw=1.8)
f.box(650, 108, 100, 40, "Data bus", fill=NAVY, stroke=NAVY, color="#ffffff", size=11, bold=True)
```

## 1.8 Schmitt trigger and switch debouncing

An ordinary gate has one switching threshold. A signal that rises slowly, or is noisy, can cross that threshold several times, and the output then produces a burst of false pulses. A **Schmitt trigger** has two thresholds: the output goes LOW only when the input rises above the upper threshold V_T+ and returns HIGH (for an inverting type) only when the input falls below the lower threshold V_T−. The difference V_H = V_T+ − V_T− is the **hysteresis**. For a 74LS14 hex Schmitt inverter the typical values are V_T+ ≈ 1.6 V and V_T− ≈ 0.8 V, so V_H ≈ 0.8 V; noise smaller than this cannot cause a false change.

```svgfig label="1.6" caption="A noisy, slowly rising input (top) crosses a single threshold several times, so an ordinary inverter (middle) makes a burst of false edges. A Schmitt inverter (bottom) with thresholds V_T- and V_T+ changes once."
import math
f = Fig(760, 400)
N = 100; X0 = 70; DX = 6.0
ys = [236 - 1.7 * k + 13 * math.sin(k * 1.35) for k in range(N + 1)]
for k in range(N): f.line(X0 + k * DX, ys[k], X0 + (k + 1) * DX, ys[k + 1], color=NAVY, sw=1.8)
f.text(X0, 20, "Input voltage: slow ramp plus noise", size=10.5, color=NAVY, bold=True, anchor="start")
YP, YM, YS = 135, 170, 152
f.line(50, YP, 690, YP, color=RED, sw=1.2, dash=True); f.text(696, YP + 4, "V_T+", size=10, color=RED, bold=True, anchor="start")
f.line(50, YM, 690, YM, color=TEAL, sw=1.2, dash=True); f.text(696, YM + 4, "V_T-", size=10, color=TEAL, bold=True, anchor="start")
f.line(50, YS, 690, YS, color=AMBER, sw=1.0, dash=True); f.text(56, YS - 5, "single threshold", size=9, color=AMBER, bold=True, anchor="start")
# inverter outputs: input is "high" when voltage is high (y small)
def trace(levels, ylo, yhi, col):
    for k in range(N):
        a, b = levels[k], levels[k + 1]
        x1, x2 = X0 + k * DX, X0 + (k + 1) * DX
        f.line(x1, yhi if a else ylo, x2, yhi if a else ylo, color=col, sw=2.2)
        if a != b: f.line(x2, ylo, x2, yhi, color=col, sw=2.2)
ordinary = [1 if ys[k] > YS else 0 for k in range(N + 1)]
sch = []; st = 1
for k in range(N + 1):
    if ys[k] < YP: st = 0
    elif ys[k] > YM: st = 1
    sch.append(st)
edges = sum(1 for k in range(N) if ordinary[k] != ordinary[k + 1]); sedges = sum(1 for k in range(N) if sch[k] != sch[k + 1])
f.text(X0, 262, "Ordinary inverter output (%d edges)" % edges, size=10.5, color=SLATE, bold=True, anchor="start")
trace(ordinary, 308, 280, RED)
f.text(X0, 336, "Schmitt inverter output (%d edge)" % sedges, size=10.5, color=SLATE, bold=True, anchor="start")
trace(sch, 382, 354, TEAL)
```

**Switch debouncing.** A mechanical push-button does not close cleanly; its contacts bounce for 1 to 20 ms, and a fast counter would count each bounce as a separate press. There are three standard cures. (1) An **RC filter followed by a Schmitt trigger**: the capacitor smooths the bounce and the hysteresis makes one clean edge. (2) A **set-reset latch** made of two cross-coupled NAND gates with a single-pole double-throw switch: the first touch of the other contact flips the latch and later bounces cannot flip it back. (3) **Software**: ignore the input for about 20 ms after the first edge. Keypads, rotary encoders and the reset button of every board use one of these.

## 1.9 Sampling, quantisation and the cost of going digital

Section 1.1 said that a digital system must convert analog signals at its boundary. Two decisions fix the quality of that conversion.

**Sampling rate.** By the **Nyquist theorem** the sampling frequency must be at least twice the highest frequency in the signal, otherwise high frequencies fold back as false low ones (**aliasing**). A telephone channel keeps frequencies up to about 3.4 kHz and is sampled at 8 kHz. Audio CDs keep up to 20 kHz and sample at 44.1 kHz (the minimum would be 40 kHz; the extra gives the anti-aliasing filter room to work).

**Number of bits.** An n-bit converter has 2ⁿ levels, so the step is V_range / 2ⁿ. A 10-bit ADC on a 5 V range has a step of 5 / 1024 = 4.88 mV; a 12-bit ADC on 3.3 V has 0.806 mV. The error of rounding to the nearest level is at most half a step, and for a full-scale sine wave the signal-to-quantisation-noise ratio is about

SNR ≈ 6.02 n + 1.76 dB

which gives 49.9 dB for 8 bits, 74.0 dB for 12 bits and 98.1 dB for 16 bits. Each extra bit buys about 6 dB.

::: example Worked example: the data rate of digital audio
A stereo CD uses 44,100 samples per second per channel, 16 bits per sample, two channels: 44,100 × 16 × 2 = **1,411,200 bit/s** (about 1.41 Mbit/s), which is 1,411,200 / 8 × 60 ≈ **10.6 MB per minute**. A telephone call uses 8,000 × 8 = 64,000 bit/s. These numbers show the cost mentioned in Section 1.5: digital audio needs far more bandwidth than the analog signal it replaces, and this is the reason that compression (MP3, AAC, Opus) was invented.
:::

## Formula and fact sheet

- Step of an n-bit ADC = V_range / 2ⁿ.
- NM_H = V_OH(min) − V_IH(min); NM_L = V_IL(max) − V_OL(max).
- f = 1 / T; duty cycle = t_high / T.
- Positive logic: H = 1. Negative logic: H = 0. AND ↔ OR under logic inversion.
- TTL thresholds: 0.8 / 2.0 V in, 0.4 / 2.4 V out.
- PDP = t_p × P. CMOS dynamic power P = C V² f. Fan-out = min(I_OL/I_IL, I_OH/I_IH).
- Pull-up: R_min = (Vcc − V_OL) / (I_OL − N·I_IL); R_max = (Vcc − V_OH) / (n·I_OH + N·I_IH).
- Nyquist f_s ≥ 2 f_max; SNR ≈ 6.02 n + 1.76 dB; hysteresis V_H = V_T+ − V_T−.

## Chapter summary

- Digital signals resist noise because they are decided by thresholds.
- Logic levels have guaranteed bands and a forbidden zone; noise margin measures the safety.
- Clocks are described by period, frequency, duty cycle and edges; setup and hold times limit speed.
- ICs range from SSI gates to ULSI processors; CMOS is the dominant family.
- Output stages decide wiring: totem-pole drives both levels, open-collector needs a pull-up and gives wired-AND, tri-state outputs share a bus.
- A Schmitt trigger cleans noisy edges; sampling rate and bit count fix digital-audio quality and cost.

## Practice

1. List four advantages of digital over analog representation.
2. A TTL gate has V_OH(min) = 2.4 V, V_IH(min) = 2.0 V, V_OL(max) = 0.4 V, V_IL(max) = 0.8 V. Compute both noise margins.
3. A 12-bit ADC has a 0–3.3 V input range. What is its resolution in millivolts?
4. A clock runs at 25 MHz with a duty cycle of 40 %. Find the period and the high time.
5. Distinguish positive and negative logic. What does an AND gate become under negative logic?
6. What do setup and hold time mean, and what happens if they are violated?
7. Name the scale of integration of (a) a 7400 chip, (b) a 4-bit counter chip, (c) a modern CPU.
8. A gate has t_pHL = 6 ns and t_pLH = 10 ns. Find the average delay and the highest clock frequency for a path of four such gates followed by a flip-flop with 12 ns setup time.
9. Compute the power-delay product of a gate with delay 4 ns and power 1.2 mW. Which is better, this gate or one with 9.5 ns and 2 mW?
10. A CMOS gate drives 15 pF. Find its dynamic power at 5 V and 2 MHz, and again at 3.3 V.
11. A gate has I_OL(max) = 20 mA, I_IL(max) = 0.5 mA, I_OH(max) = 1 mA and I_IH(max) = 25 µA. Find its fan-out.
12. Why can two totem-pole outputs not be connected together, while two open-collector outputs can?
13. What is the purpose of the enable input of a tri-state buffer, and what is the state called when it is disabled?
14. Explain hysteresis in a Schmitt trigger and give two uses.
15. Find the quantisation step and the SNR of a 14-bit ADC with a 2.5 V range, and the bit rate of mono 48 kHz audio at 24 bits.

::: note Answers and worked solutions
**1.** Noise immunity; exact storage and copying; error detection and correction; easy large-scale integration; programmability.
**2.** NM_H = 2.4 − 2.0 = 0.4 V; NM_L = 0.8 − 0.4 = 0.4 V.
**3.** 3.3 / 4096 = 0.000806 V ≈ 0.81 mV.
**4.** T = 1 / 25 MHz = 40 ns; high time = 0.4 × 40 = 16 ns.
**5.** Positive logic takes the high voltage as 1; negative logic takes it as 0. A gate that is AND in positive logic is OR in negative logic.
**6.** Setup: the data must be stable for a minimum time before the active clock edge; hold: it must stay stable for a minimum time after. Violating them can leave the flip-flop in an undefined (metastable) state or capture the wrong value.
**7.** (a) SSI, (b) MSI, (c) ULSI (VLSI in older classification).
**8.** Average = (6 + 10) / 2 = 8 ns. Four gates = 32 ns; plus 12 ns setup = 44 ns. f_max = 1 / 44 ns ≈ 22.7 MHz.
**9.** PDP = 4 ns × 1.2 mW = 4.8 pJ, which is better than 9.5 ns × 2 mW = 19 pJ (about four times less energy per switching event).
**10.** P = C V² f = 15×10⁻¹² × 25 × 2×10⁶ = 0.75 mW at 5 V; at 3.3 V: 15×10⁻¹² × 10.89 × 2×10⁶ = 0.327 mW.
**11.** LOW state: 20 / 0.5 = 40. HIGH state: 1 mA / 25 µA = 40. Fan-out = 40.
**12.** A totem-pole output drives both levels, so if one drives HIGH and the other LOW a large current flows between them and the level is undefined. An open-collector output can only pull LOW; a pull-up resistor makes HIGH, so any output can pull the common line down without a fight (wired-AND).
**13.** Enable decides whether the buffer drives the line. When disabled the output is high impedance (Hi-Z), electrically disconnected, so that many buffers can share one bus and only one drives it at a time.
**14.** A Schmitt trigger switches at V_T+ when the input rises and at a lower V_T− when it falls; the gap V_H is the hysteresis, so noise smaller than V_H cannot cause false edges. Uses: cleaning slow or noisy signals, debouncing switches, building simple oscillators.
**15.** Step = 2.5 / 16384 = 0.153 mV; SNR ≈ 6.02 × 14 + 1.76 = 86.0 dB. Bit rate = 48,000 × 24 = 1,152,000 bit/s ≈ 1.15 Mbit/s.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q (5 marks). Differentiate analog and digital signals and state any four advantages of digital systems.**

An **analog signal** varies continuously and can take any value in a range, such as the voltage from a microphone or a thermometer. A **digital signal** takes only a few fixed levels, usually two (HIGH and LOW, written 1 and 0), and changes between them in steps (see Plate 1.1 and Figure 1.1). To handle an analog quantity digitally, an ADC *samples* it at regular instants and *quantises* each sample to the nearest of 2ⁿ levels; an n-bit ADC over V volts has a step of V / 2ⁿ. For example, a 10-bit ADC over 0–5 V has a step of 5 / 1024 ≈ 4.9 mV.

| Point | Analog | Digital |
|---|---|---|
| Values | continuous | discrete (0 and 1) |
| Noise | accumulates, cannot be removed | removed by thresholding |
| Copying | quality loss each copy | exact copy |
| Circuits | amplifiers, filters | gates, flip-flops |
| Accuracy | limited by component tolerance | set by the number of bits |

Four advantages: (1) noise immunity, because a 0.2 V ripple does not change a decision; (2) exact storage and copying; (3) error detection and correction using parity or CRC; (4) easy integration into chips and programmability. A Fonepay QR payment shows all four: the amount is the same at the shop and in the bank.

**Q (5 marks). Define noise margin. For a TTL gate with V_OH(min) = 2.4 V, V_IH(min) = 2.0 V, V_OL(max) = 0.4 V and V_IL(max) = 0.8 V, find both noise margins and explain their meaning.**

A gate does not output an exact voltage. The manufacturer guarantees only that a HIGH output is *at least* V_OH(min) and a LOW output is *at most* V_OL(max). The next gate, in turn, promises to read any input of at least V_IH(min) as HIGH and at most V_IL(max) as LOW. The **noise margin** is the extra unwanted voltage that a signal can pick up on the wire between the two gates and still be read correctly (Figure 1.2).

- High-state noise margin: NM_H = V_OH(min) − V_IH(min) = 2.4 − 2.0 = **0.4 V**.
- Low-state noise margin: NM_L = V_IL(max) − V_OL(max) = 0.8 − 0.4 = **0.4 V**.

So a HIGH can drop by 0.4 V (for instance because of crosstalk from a neighbouring wire) and a LOW can rise by 0.4 V without an error. The voltage zone between 0.8 V and 2.0 V is the **forbidden (undefined) region**: a signal there may be read as 0 or 1, so a correct design never leaves a signal in it except while switching. A larger noise margin means a more robust circuit; CMOS gates have larger margins (about 30 % of the supply on each side) than TTL, which is one reason they dominate today.

**Q (10 marks). Explain the digital waveform and the clock: rise time, fall time, propagation delay, period, frequency, duty cycle, and the setup and hold times. Compare TTL and CMOS logic families.**

*Introduction.* A digital system is driven by a **clock**, a periodic pulse train that tells every flip-flop when to sample its input. All timing in the computer, from the CPU to memory, is a multiple of this clock.

*The ideal and real waveform.* An ideal clock is a perfect square wave (Figure 1.3). A real pulse takes time to change level. The **rise time** t_r is the time to go from 10 % to 90 % of the amplitude, and the **fall time** t_f is the reverse. The **propagation delay** t_pd is the time between a change at a gate input and the resulting change at the output; it limits how fast the circuit can run.

*Clock parameters.*

1. **Period T**: time of one full cycle.
2. **Frequency f = 1 / T**: cycles per second (Hz). T = 20 ns means f = 50 MHz.
3. **Duty cycle = t_high / T × 100 %**: a 6 ns high time in a 20 ns period is 30 %.
4. **Rising edge (0 → 1)** and **falling edge (1 → 0)**: the *active* edge is the one that triggers the flip-flop.
5. **Setup time t_su**: the input data must be stable for this long *before* the active edge.
6. **Hold time t_h**: the data must stay stable for this long *after* the edge.
7. **Minimum clock period**: T ≥ t_clk-to-Q + t_pd(logic) + t_su; if a path is too slow, the clock must be slowed down.
8. **Violations**: if setup or hold is violated, the flip-flop can become *metastable*, giving an undefined output for a short time or capturing the wrong bit.

*Comparison of logic families.*

| Property | TTL (74xx / 74LS) | CMOS (74HCxx / 4000) |
|---|---|---|
| Building element | bipolar transistors | MOSFETs |
| Supply voltage | 5 V (±5 %) | 2–6 V (HC), 3–15 V (4000) |
| Static power | milliwatts per gate | almost zero |
| Speed | fast (a few ns) | now equal or faster |
| Noise margin | about 0.4 V | about 30 % of supply |
| Fan-out | about 10 | very high (more than 50) |
| Present use | teaching, legacy | CPUs, memories, nearly all chips |

*Conclusion.* The clock sets the beat, the logic levels and noise margin keep the beat reliable, and the logic family decides power and speed. Every figure in this unit is applied in the later units when flip-flops and counters are built.

**Q (5 marks). Compare totem-pole, open-collector and tri-state outputs. Where is each used?**

The three differ in how the output stage drives the line.

| Point | Totem-pole | Open-collector | Tri-state |
|---|---|---|---|
| Output states | 0 and 1, both driven | 0 driven, 1 by external resistor | 0, 1 and Hi-Z |
| Extra part | none | pull-up resistor | enable input |
| Outputs joined? | never (contention) | yes, wired-AND | yes, if only one enabled |
| Speed of rising edge | fast | slower (set by R and C) | fast |
| Typical use | ordinary gates, single load | interrupt lines, I²C, LED and relay drivers | data and address buses |

*Conclusion.* Use totem-pole for point-to-point links, open-collector where several devices may pull one line low, and tri-state where many devices take turns putting data on a shared bus.

**Q (5 marks). A path of six gates (t_pHL = 7 ns, t_pLH = 11 ns) feeds a flip-flop with setup time 15 ns. Find the maximum clock frequency. A second design replaces the gates with ones that are 40 % faster; find the new frequency.**

Average delay = (7 + 11) / 2 = 9 ns, so six gates give 54 ns. Add the setup time: T_min = 54 + 15 = 69 ns, so f_max = 1 / 69 ns ≈ **14.5 MHz**.

With 40 % faster gates the delay per gate is 0.6 × 9 = 5.4 ns; six gates give 32.4 ns; T_min = 32.4 + 15 = 47.4 ns and f_max ≈ **21.1 MHz**. The speed-up is only 46 %, not 67 %, because the setup time of the flip-flop did not shrink. *Conclusion.* A clock is limited by the slowest path **plus** setup time, so speeding up only the gates has diminishing returns.
