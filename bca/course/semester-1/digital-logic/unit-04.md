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
