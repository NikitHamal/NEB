---
subject: Digital Logic
grade: BCA Semester 1
unit: 4
title: Flip-Flops, Counters and Registers
hours: 16
area: BCA 103 · Digital Logic · Unit 4
---

Combinational circuits forget. To remember a bit, to count, to hold a value while the next one arrives, you need **sequential** circuits: circuits whose output depends on the present input *and* on stored state. The storage element is the **flip-flop**, and registers and counters are flip-flops wired in useful patterns. Every register in a CPU is such a circuit.

::: key What this unit gives you
- Latches and the flip-flops SR, JK (and master-slave), D, T: characteristic equations, truth tables, excitation tables.
- Level vs edge triggering, preset/clear, and the race-around condition.
- Asynchronous (ripple) counters, modulus-N counters, ring and Johnson counters.
- Synchronous counters and their design with excitation tables.
- Shift registers (SISO, SIPO, PISO, PIPO), and applications: digital clock, frequency counter.
:::

## 4.1 Latches and flip-flops

A **latch** is a level-sensitive bistable element. The basic **SR latch** from two cross-coupled NOR gates has inputs Set and Reset: S = 1, R = 0 sets Q = 1; S = 0, R = 1 resets Q = 0; S = R = 0 holds; **S = R = 1 is forbidden** (both outputs 0, and the result is undefined when both return to 0). A NAND version has active-low inputs. A **gated (clocked) SR latch** responds only while the clock enable is high.

A **flip-flop** changes state only at a clock **edge**. Terms: Q is the present state, Q⁺ (or Q(t+1)) the next state.

| Type | Inputs | Characteristic equation | Behaviour |
|---|---|---|---|
| SR | S, R | Q⁺ = S + R'Q, with SR = 0 | S = 1 sets, R = 1 resets, 00 holds, 11 not allowed |
| **JK** | J, K | Q⁺ = JQ' + K'Q | 00 hold, 01 reset, 10 set, **11 toggle** |
| **D** | D | Q⁺ = D | copies D at the clock edge (a one-bit delay) |
| **T** | T | Q⁺ = T ⊕ Q | T = 0 hold, T = 1 toggle |

JK removes the SR forbidden state by making 11 mean toggle. A D flip-flop is a JK with K = J'. A T flip-flop is a JK with J = K = T, or a D flip-flop with D = T ⊕ Q.

**Excitation tables** answer "what must the inputs be to go from Q to Q⁺?" and are the key to counter design (X = don't-care):

| Q → Q⁺ | SR: S R | JK: J K | D | T |
|---|---|---|---|---|
| 0 → 0 | 0 X | 0 X | 0 | 0 |
| 0 → 1 | 1 0 | 1 X | 1 | 1 |
| 1 → 0 | 0 1 | X 1 | 0 | 1 |
| 1 → 1 | X 0 | X 0 | 1 | 0 |

**Triggering.** *Level triggering*: the output follows the inputs for the whole time the clock is high (or low); the circuit is "transparent". *Edge triggering*: the inputs are sampled only at the rising (or falling) edge, which makes behaviour predictable. Edge-triggered symbols have a small triangle on the clock input; a bubble means falling-edge or active-low.

**Race-around.** In a level-triggered JK with J = K = 1 the output toggles repeatedly during the whole clock-high interval whenever that interval exceeds the propagation delay, so the final state is uncertain. Remedies: **master-slave** construction (two latches on opposite clock phases, the master takes the input while clock is high and the slave updates when it falls), or edge-triggering, or a very narrow clock pulse.

**Asynchronous inputs.** **Preset** (set to 1) and **Clear** (reset to 0) act immediately, overriding the clock. They initialise counters and registers at power-up.

## 4.2 Counters

A **counter** is a sequential circuit that steps through a fixed sequence of states, one per clock pulse. **Modulus** (MOD) = number of distinct states. n flip-flops give at most 2ⁿ states, so MOD ≤ 2ⁿ.

### Asynchronous (ripple) counters

In a ripple counter the clock goes only to the first flip-flop; each following flip-flop is clocked by the output of the previous one. With T (toggle) flip-flops (JK with J = K = 1) that trigger on the falling edge, Q₀ toggles every clock pulse, Q₁ every two, Q₂ every four: a **binary up-counter**. Each stage divides the frequency by two, so an n-stage counter divides by 2ⁿ: a 4-stage ripple counter fed by 1 MHz gives 62.5 kHz at Q₃. Connecting each clock to the *complement* output Q' counts **down**.

Counting sequence of a 3-bit up counter (Q₂Q₁Q₀): 000, 001, 010, 011, 100, 101, 110, 111, 000, …

**Drawback.** The delay accumulates: the last output settles about n × t_pd after the clock. With t_pd = 20 ns and four stages the output is valid only after 80 ns, so the counter cannot run faster than about 1 / 80 ns = 12.5 MHz, and decoding the state can produce brief false values (*glitches*) while the ripple passes.

**Modulus-N counters by reset.** To count 0 … N − 1, use n = ⌈log₂ N⌉ flip-flops and add a NAND gate that detects the binary value N and drives the asynchronous clear (active low) of all flip-flops, forcing the count back to 0 immediately.

| MOD | Flip-flops | Detect and clear at | NAND inputs |
|---|---|---|---|
| 5 | 3 | 101 (5) | Q₂, Q₀ |
| 7 | 3 | 111 (7) | Q₂, Q₁, Q₀ |
| **10 (decade)** | 4 | 1010 (10) | Q₃, Q₁ |
| 11 | 4 | 1011 (11) | Q₃, Q₁, Q₀ |

The **decade (MOD-10) counter** counts 0000 to 1001 and clears on 1010, which is detected by Q₃ = Q₁ = 1 because no earlier state has both set. Its output is BCD, used for one digit of a display (the 7490 chip). The state 1010 exists for only a few nanoseconds.

### Ring and Johnson counters

A **ring counter** is a circular shift register of n D flip-flops with Q of the last fed back to D of the first; preset one stage to 1 and a single 1 circulates. It has **n states** with n flip-flops (one-hot) and needs no decoder: 1000 → 0100 → 0010 → 0001 → 1000. A **Johnson (twisted-ring) counter** feeds back Q' of the last stage, giving **2n states**: for 4 flip-flops 0000 → 1000 → 1100 → 1110 → 1111 → 0111 → 0011 → 0001 → 0000 (8 states). Each state is decoded with a 2-input gate.

### Synchronous counters

In a **synchronous counter** all flip-flops share one clock, so all outputs change together and the speed no longer depends on the number of stages. The price is extra gating. For a binary up-counter with T flip-flops: T₀ = 1, T₁ = Q₀, T₂ = Q₀Q₁, T₃ = Q₀Q₁Q₂; a stage toggles when all lower bits are 1. The maximum frequency is 1 / (t_pd of one flip-flop + one AND-gate delay).

**Design procedure** (shown fully in Unit 5): (1) state diagram; (2) number of flip-flops; (3) pick the flip-flop type; (4) write the state table with next states; (5) fill the excitation columns from the excitation table; (6) simplify each input with a K-map (unused states are don't-cares); (7) draw the circuit and check the unused states lead back into the sequence.

::: example Worked design: synchronous MOD-3 counter with JK flip-flops (00 → 01 → 10 → 00)
Two flip-flops, states Q₁Q₀. Unused state 11 is sent to 00 for self-starting.

| Q₁Q₀ | Next | J₁ K₁ | J₀ K₀ |
|---|---|---|---|
| 00 | 01 | 0 X | 1 X |
| 01 | 10 | 1 X | X 1 |
| 10 | 00 | X 1 | 0 X |
| 11 | 00 | X 1 | X 1 |

K-maps give **J₁ = Q₀, K₁ = 1, J₀ = Q₁', K₀ = 1.** Check from 01: J₁ = K₁ = 1 toggles Q₁ to 1; J₀ = Q₁' = 1 and K₀ = 1 toggle Q₀ to 0 → 10 ✔.
:::

**Applications.** *Frequency division and timing*: a **digital clock** uses a 32,768 Hz quartz crystal divided by a chain of 15 flip-flops (2¹⁵ = 32,768) to get exactly 1 Hz; the seconds then feed a MOD-10 and MOD-6 counter (00–59), then another MOD-10/MOD-6 pair for minutes, then a MOD-12 or MOD-24 counter for hours, each stage driving a BCD-to-seven-segment decoder. A **frequency counter** opens an AND gate for exactly one second and counts the input pulses that pass through; the count in that second is the frequency in Hz. Counters are also used as address generators, event counters and in timers.

```svgfig label="4.1" caption="A 3-bit asynchronous (ripple) up counter of three T flip-flops (T = 1). Each stage toggles when the previous output falls, so Q0 runs at f/2, Q1 at f/4 and Q2 at f/8; Q2 Q1 Q0 counts 000 to 111."
f = Fig(760, 340)
for i in range(3):
    x = 120 + i * 150
    f.box(x, 14, 90, 50, f"T-FF  Q{i}", fill=SOFT, stroke=NAVY, size=11, bold=True)
    f.arrow([(x - 30, 39), (x, 39)], color=SLATE)
    if i < 2: f.arrow([(x + 90, 24), (x + 120, 24), (x + 120, 39), (x + 150 - 30 + 30 - 30, 39)], color=SLATE)
f.text(60, 43, "CLK in", size=10.5, color=NAVY, bold=True)
def wave(y, init, toggles, label, col):
    f.text(48, y + 16, label, size=11, color=col, bold=True, anchor="end")
    lvl = init; x = 60
    for t in toggles + [700]:
        yy = y if lvl else y + 22
        f.line(x, yy, t, yy, color=col, sw=2.2)
        if t != 700:
            f.line(t, y, t, y + 22, color=col, sw=2.2); lvl ^= 1
        x = t
wave(100, 1, [100 + 40 * j for j in range(15)], "CLK", NAVY)
wave(146, 0, [100 + 80 * k for k in range(8)], "Q0", TEAL)
wave(192, 0, [100 + 80 * k for k in (1, 3, 5, 7)], "Q1", RED)
wave(238, 0, [100 + 80 * k for k in (3, 7)], "Q2", AMBER)
for c in range(8):
    f.text(80 if c == 0 else 60 + 80 * c, 292, format(c, "03b"), size=10.5, color=NAVY, bold=True)
f.text(48, 296, "count", size=10.5, color=NAVY, bold=True, anchor="end")
f.text(380, 326, "outputs change on the falling edge of the previous stage (ripple delay ignored here)", size=9.5, color=SLATE)
```

## 4.3 Registers

A **register** is a group of flip-flops holding a binary word, all sharing one clock; an n-bit register stores n bits. A **shift register** also moves the bits one position on each clock pulse. Four modes:

| Mode | Input | Output | Clock pulses to load 4 bits |
|---|---|---|---|
| **SISO** serial-in, serial-out | one bit at a time | one bit at a time | 4 to load, 4 more to read out: a delay line |
| **SIPO** serial-in, parallel-out | serial | all bits at once | 4 (serial-to-parallel conversion, e.g. receiver) |
| **PISO** parallel-in, serial-out | all bits at once (load line) | serial | 1 to load, 4 to send (parallel-to-serial, transmitter) |
| **PIPO** parallel-in, parallel-out | all bits | all bits | 1 (a storage register) |

Built from D flip-flops with each Q wired to the next D. Loading 1011 serially (first bit 1 entered first): after four clocks the register holds Q₃Q₂Q₁Q₀ = 1011 with the *first* bit at the far end. **Right shift** moves bits towards the LSB end (divides an unsigned number by 2); **left shift** doubles it. A **universal shift register** (74194) has a mode control to do hold, shift left, shift right and parallel load, and is built with a 4-to-1 MUX in front of every flip-flop.

Registers are used for temporary storage in the CPU, serial communication (UART), delay lines, sequence generation (ring and Johnson counters are shift registers with feedback), and arithmetic (shift-and-add multiplication).

```svgfig label="4.2" caption="A 4-bit serial-in serial-out shift register of D flip-flops. At every clock edge each bit moves one place to the right. The table shows the contents after each clock when the data 1, 0, 1, 1 is shifted in (first bit first)."
f = Fig(760, 250)
f.text(40, 50, "Serial in", size=10.5, color=NAVY, bold=True)
for i in range(4):
    x = 120 + i * 120
    f.box(x, 24, 70, 54, f"D-FF\nQ{i}", fill=SOFT, stroke=NAVY, size=11, bold=True)
    f.arrow([(x - 40 if i else x - 36, 51), (x, 51)], color=SLATE)
    f.line(x + 35, 78, x + 35, 96, color=SLATE)
f.arrow([(120 + 3 * 120 + 70, 51), (740, 51)], color=TEAL, label="Serial out", lpos=(716, 40))
f.line(110, 96, 560, 96, color=AMBER, sw=1.6); f.text(335, 112, "common clock", size=10, color=AMBER, bold=True)
rows = [("start", "0 0 0 0"), ("clock 1", "1 0 0 0"), ("clock 2", "0 1 0 0"), ("clock 3", "1 0 1 0"), ("clock 4", "1 1 0 1")]
f.text(210, 134, "Q0 Q1 Q2 Q3", size=10.5, color=NAVY, bold=True, anchor="start")
for i, (a, b) in enumerate(rows):
    y = 152 + i * 18
    f.text(120, y, a, size=10.5, color=SLATE, anchor="start"); f.text(210, y, b, size=10.5, color=TEAL if i else SLATE, bold=True, anchor="start")
f.box(420, 130, 310, 94, "", fill=SOFT, stroke="#cbd5e1")
f.text(575, 154, "Four clocks load four bits (serial to parallel).", size=10.5, color=NAVY, bold=True)
f.text(575, 176, "Four more clocks move them out", size=10.5, color=SLATE); f.text(575, 194, "(parallel to serial).", size=10.5, color=SLATE)
f.text(575, 214, "Delay = n clock periods for n bits.", size=10.5, color=SLATE)
```

## 4.4 Applications of flip-flops, counters and registers: eight uses

1. **Memory cells.** A flip-flop stores one bit as long as power is on. Registers inside a CPU and the cache memory are arrays of such cells. A 32-bit register is simply 32 flip-flops sharing one clock.
2. **Frequency division.** A T flip-flop halves the clock frequency, so n stages divide by 2ⁿ. A 32.768 kHz watch crystal passes through 15 stages to give exactly 1 Hz. The same idea gives slower clocks inside microcontrollers.
3. **Digital clocks and timers.** Counters count seconds, minutes and hours, and a decoder drives the display. The token board at a bank counter and the timer on a microwave oven are examples. A MOD-60 counter resets after 59.
4. **Event and frequency counters.** A counter can count pulses from a sensor in a fixed time. A factory in Hetauda counting bottles on a belt, or a meter measuring the speed of a motor, works in this way. The count is the reading.
5. **Serial-to-parallel conversion.** A shift register collects bits one by one from a wire and then offers them all together. USB, UART and Ethernet ports do this at high speed. Parallel-to-serial conversion works in the opposite direction.
6. **Delay lines and pipelines.** A shift register delays a signal by a known number of clock periods. Pipelined CPUs put registers between stages to hold each instruction while the next one starts. This raises the speed of the whole processor.
7. **Ring and Johnson counters for control.** A ring counter keeps one flip-flop at 1 and moves it around. It gives timing pulses that switch traffic lights or step a stepper motor in sequence. Johnson counters give 2n states from n flip-flops.
8. **Synchronisation and debouncing.** A D flip-flop samples an input at the clock edge, which turns a noisy or asynchronous signal into a clean one. Keyboard keys and push buttons need this because their contacts bounce. It also protects the CPU from signals that arrive at random times.

## Formula and fact sheet

- SR: Q⁺ = S + R'Q (SR = 0). JK: Q⁺ = JQ' + K'Q. D: Q⁺ = D. T: Q⁺ = T ⊕ Q.
- Excitation: JK 0→1 is "1X", 1→0 is "X1"; T = Q ⊕ Q⁺; D = Q⁺.
- n flip-flops: MOD ≤ 2ⁿ; ripple divides frequency by 2ⁿ.
- Ripple settling time ≈ n × t_pd; f_max ≈ 1 / (n × t_pd).
- Ring: n states; Johnson: 2n states.
- Reset to make MOD-N: NAND the outputs that are 1 in the binary value of N.
- Digital clock: 32,768 Hz / 2¹⁵ = 1 Hz.

## Chapter summary

- Flip-flops store one bit and change on a clock edge; JK toggles on 11, D delays, T toggles.
- Excitation tables turn a wanted state change into flip-flop inputs.
- Ripple counters are simple and slow; synchronous counters are fast and need design.
- Counters count and divide frequency; registers store and shift words.

## Practice

1. Write the characteristic equation and truth table of the JK flip-flop. How does it differ from SR?
2. What is the race-around condition and how is it removed?
3. Derive the T flip-flop from a JK flip-flop; derive a D flip-flop from a JK.
4. A 4-bit ripple counter uses flip-flops with t_pd = 25 ns. Find the maximum clock frequency (counter-settling basis) and the output frequency at Q₃ for a 4 MHz input.
5. Draw (describe) a MOD-10 ripple counter and give the state at which it is cleared.
6. What is the counting sequence of a 3-bit down counter?
7. List the 8 states of a 4-bit Johnson counter, starting at 0000.
8. Design a synchronous 2-bit counter that goes 00 → 01 → 11 → 10 → 00 with D flip-flops.
9. A 4-bit PISO register is clocked at 1 kHz. How long does it take to send out one loaded word?
10. How many flip-flops are needed for a MOD-60 counter, and how would you build it from decade counters?

::: note Answers and worked solutions
**1.** Q⁺ = JQ' + K'Q. J K = 00 → Q; 01 → 0; 10 → 1; 11 → Q'. SR has the forbidden input 11; JK uses it to toggle.
**2.** With J = K = 1 on a level-triggered clock, the output toggles repeatedly while the clock stays high (longer than t_pd), leaving the final state uncertain. Use a master-slave or edge-triggered flip-flop.
**3.** Tie J and K together: T flip-flop, Q⁺ = TQ' + T'Q = T ⊕ Q. For D: J = D, K = D', so Q⁺ = DQ' + DQ = D.
**4.** Settling time 4 × 25 = 100 ns → f_max ≈ 10 MHz. Q₃ output = 4 MHz / 16 = 250 kHz.
**5.** Four toggle flip-flops in ripple; NAND(Q₃, Q₁) drives the active-low clear; it clears at 1010 (decimal 10), so the stable states are 0000–1001.
**6.** 111, 110, 101, 100, 011, 010, 001, 000, then 111 again.
**7.** 0000, 1000, 1100, 1110, 1111, 0111, 0011, 0001.
**8.** The next Q₁ is 0, 1, 1, 0 for states 00, 01, 11, 10, so D₁ = Q₀. The next Q₀ is 1, 1, 0, 0, so D₀ = Q₁'. Check: 00 → 01 → 11 → 10 → 00 ✔.
**9.** At 1 kHz one clock period is 1 ms. One pulse loads the word and then four periods shift the four bits out, so the word is transmitted in 4 ms after a 1 ms load (5 ms in all).
**10.** A single binary counter for 60 states needs 6 flip-flops (2⁶ = 64 ≥ 60). The practical BCD build is a MOD-10 counter (4 flip-flops) cascaded with a MOD-6 counter (3 flip-flops), 7 in total: the MOD-10 carries into the MOD-6 every ten pulses, and both give BCD outputs for a two-digit display counting 00–59.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q (5 marks). Explain the JK flip-flop with its truth table and characteristic equation. How does it avoid the invalid state of the SR flip-flop? What is the race-around condition?**

A **JK flip-flop** is a clocked bistable circuit with two inputs J (set) and K (reset) and outputs Q and Q'. It is the most flexible flip-flop because every input combination has a defined result.

| J | K | Q⁺ (next state) | Action |
|---|---|---|---|
| 0 | 0 | Q | hold |
| 0 | 1 | 0 | reset |
| 1 | 0 | 1 | set |
| 1 | 1 | Q' | toggle |

Characteristic equation: **Q⁺ = JQ' + K'Q**. In an SR flip-flop the input S = R = 1 is forbidden, because both outputs would try to go to 0 and the final state is unpredictable. In the JK flip-flop the outputs are fed back to the input gates so that the combination J = K = 1 simply **toggles** the output. The invalid state is therefore turned into a useful function.

**Race-around.** In a *level-triggered* JK flip-flop with J = K = 1, the output toggles and, since the clock is still high, the new output feeds back and toggles it again, many times during one pulse; the final state is uncertain. It is cured by (1) using edge triggering, (2) a master–slave construction, or (3) making the clock pulse shorter than the propagation delay. With J = K = T the JK becomes a T flip-flop, and with K = J' it becomes a D flip-flop.

**Q (10 marks). Describe the 3-bit asynchronous (ripple) counter with its timing diagram. Compare asynchronous and synchronous counters.**

*Introduction.* A **counter** is a sequential circuit built from flip-flops that goes through a fixed sequence of states when clock pulses arrive. A counter with n flip-flops has at most 2ⁿ states; the number of states it uses is its **modulus** (MOD). A 3-bit binary counter is MOD-8.

*Construction.* Use three T flip-flops (JK with J = K = 1), as in Figure 4.1. The external clock drives only the first stage. The output Q0 of the first stage is the clock of the second, and Q1 is the clock of the third. Each flip-flop toggles on the **falling edge** of its own clock input.

*Operation.* Starting from 000: the first falling edge of CLK makes Q0 = 1 (001). The second makes Q0 = 0, and that falling edge toggles Q1, giving 010. The third gives 011, and the fourth takes Q0 and Q1 to 0 and toggles Q2, giving 100. The count continues to 111 and then returns to 000 on the eighth edge. Frequencies: Q0 = f/2, Q1 = f/4 and Q2 = f/8, so a counter is also a divider.

*Ripple delay and its limit.* Each stage waits for the previous one, so the delay of an n-bit ripple counter is n × t_pd. For a 3-stage counter with t_pd = 10 ns the final output settles after 30 ns, and the maximum clock is limited to about 1 / (n × t_pd). During the ripple the outputs pass through false states (for example 011 → 010 → 000 → 100), which may cause glitches in a decoder.

*Other counters.* **Down counter**: use Q' to clock the next stage. **MOD-N counter**: detect state N with a NAND gate and use it to clear all flip-flops asynchronously; for MOD-6 detect 110 (Q2 Q1) and clear.

| Point | Asynchronous (ripple) | Synchronous |
|---|---|---|
| Clock | only the first stage | all stages together |
| Delay | n × t_pd | one t_pd |
| Speed | slow | fast |
| Hardware | simplest | extra AND gates |
| False states | yes | no |
| Design | trivial | uses excitation tables |
| Use | frequency dividers | CPUs, high-speed counters |

*Conclusion.* The ripple counter is simple, cheap and good as a frequency divider; when speed matters, a synchronous counter is used because all flip-flops change at the same instant.
