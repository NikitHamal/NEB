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

## 1.3 Pulses and the clock waveform

An ideal digital waveform is a square wave; a real one has a **rise time** t_r and **fall time** t_f, usually measured between 10 % and 90 % of the amplitude, and a **propagation delay** t_pd: the time from an input change to the output change.

For a periodic clock:

- **Period** T: the time of one complete cycle.
- **Frequency** f = 1 / T (hertz).
- **Duty cycle** = t_high / T × 100 %.

A 50 MHz clock has T = 1 / (50 × 10⁶) = 20 ns. A clock with a 6 ns high time in a 20 ns period has a 30 % duty cycle.

Edge terms matter for sequential circuits: the **positive (rising) edge** is the 0 → 1 transition, the **negative (falling) edge** is 1 → 0. A flip-flop triggered by an edge samples its input at that instant only. Two timing requirements follow: the data must be stable for a **setup time** before the edge and a **hold time** after it. If a path through gates takes longer than the clock period minus setup, the circuit fails; this is why there is a maximum clock frequency.

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

## Formula and fact sheet

- Step of an n-bit ADC = V_range / 2ⁿ.
- NM_H = V_OH(min) − V_IH(min); NM_L = V_IL(max) − V_OL(max).
- f = 1 / T; duty cycle = t_high / T.
- Positive logic: H = 1. Negative logic: H = 0. AND ↔ OR under logic inversion.
- TTL thresholds: 0.8 / 2.0 V in, 0.4 / 2.4 V out.

## Chapter summary

- Digital signals resist noise because they are decided by thresholds.
- Logic levels have guaranteed bands and a forbidden zone; noise margin measures the safety.
- Clocks are described by period, frequency, duty cycle and edges; setup and hold times limit speed.
- ICs range from SSI gates to ULSI processors; CMOS is the dominant family.

## Practice

1. List four advantages of digital over analog representation.
2. A TTL gate has V_OH(min) = 2.4 V, V_IH(min) = 2.0 V, V_OL(max) = 0.4 V, V_IL(max) = 0.8 V. Compute both noise margins.
3. A 12-bit ADC has a 0–3.3 V input range. What is its resolution in millivolts?
4. A clock runs at 25 MHz with a duty cycle of 40 %. Find the period and the high time.
5. Distinguish positive and negative logic. What does an AND gate become under negative logic?
6. What do setup and hold time mean, and what happens if they are violated?
7. Name the scale of integration of (a) a 7400 chip, (b) a 4-bit counter chip, (c) a modern CPU.

::: note Answers and worked solutions
**1.** Noise immunity; exact storage and copying; error detection and correction; easy large-scale integration; programmability.
**2.** NM_H = 2.4 − 2.0 = 0.4 V; NM_L = 0.8 − 0.4 = 0.4 V.
**3.** 3.3 / 4096 = 0.000806 V ≈ 0.81 mV.
**4.** T = 1 / 25 MHz = 40 ns; high time = 0.4 × 40 = 16 ns.
**5.** Positive logic takes the high voltage as 1; negative logic takes it as 0. A gate that is AND in positive logic is OR in negative logic.
**6.** Setup: the data must be stable for a minimum time before the active clock edge; hold: it must stay stable for a minimum time after. Violating them can leave the flip-flop in an undefined (metastable) state or capture the wrong value.
**7.** (a) SSI, (b) MSI, (c) ULSI (VLSI in older classification).
:::
