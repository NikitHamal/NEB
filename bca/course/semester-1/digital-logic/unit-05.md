---
subject: Digital Logic
grade: BCA Semester 1
unit: 5
title: Sequential Logic Design: State Machines
hours: 6
area: BCA 103 · Digital Logic · Unit 5
---

Counters follow a fixed sequence. A general **sequential machine** (finite-state machine, FSM) also reacts to *inputs*: a vending machine, a traffic light, a protocol detector, a CPU control unit. This unit shows how to turn a verbal description into a state diagram, a minimal state table and a circuit.

::: key What this unit gives you
- The Moore and Mealy models and their timing difference.
- State diagrams, state tables, state reduction by partitioning, state assignment.
- The full design procedure, demonstrated on a "101" sequence detector.
:::

## 5.1 Models of sequential machines

A synchronous sequential circuit has **inputs** x, a block of **flip-flops** holding the present **state**, **combinational logic** computing the next state from (state, input), and output logic.

- **Moore machine**: outputs depend **only on the present state**. Output is written inside the state circle (`S2/1`). Outputs change right after a clock edge and are glitch-free.
- **Mealy machine**: outputs depend on the **state and the present input**; they are written on the transition arrow (`x/z`). Usually needs fewer states, but outputs can change in the middle of a clock period when the input changes.

A Mealy machine and its equivalent Moore machine produce the same sequence, though the Mealy output appears one clock earlier.

```photogrid label="5.1" cols="2" ratio="1.3" caption="A finite state machine you can walk through. (a) Turnstiles at a station gate: each one is either locked or unlocked. (b) The same gate as a one-flip-flop machine, run on a stream of ten events: a coin sets the state to Unlocked, a push through an unlocked gate returns it to Locked, and a push against a locked gate does nothing."
@ photo id="bca103/turnstile" cap="Turnstile gate: two states, Locked and Unlocked"
fit 1.3
focus 0.5 0.4
call 0.5 0.9 0.35 0.45 "arm blocks you when Locked"
@ svg cap="Q+ = coin + Q.push' on the stream C P P C C P - P C P"
ev = "CPPCCP-PCP"; q = 0; log = []; passes = blocked = wasted = 0
for e in ev:
    c, p = e == "C", e == "P"
    if p and q: passes += 1
    if p and not q: blocked += 1
    if c and q: wasted += 1
    q = int(c or (q and not p)); log.append((e, q))
assert [s for _, s in log] == [1, 0, 0, 1, 1, 0, 0, 0, 1, 0] and (passes, blocked, wasted) == (3, 2, 1)
name = {"C": "coin", "P": "push", "-": "idle"}
f = Fig(400, 322)
f.text(10, 16, "Event", size=10.5, color=NAVY, bold=True, anchor="start"); f.text(110, 16, "State after", size=10.5, color=NAVY, bold=True, anchor="start"); f.text(235, 16, "Result", size=10.5, color=NAVY, bold=True, anchor="start")
q = 0
for i, (e, s) in enumerate(log):
    y = 26 + i * 26
    res = "person passes" if (e == "P" and q) else "blocked" if e == "P" else "coin wasted" if (e == "C" and q) else "unlocked" if e == "C" else "-"
    f.box(6, y, 388, 22, "", fill=MINT if s else SOFT, stroke=TEAL if s else "#94a3b8", r=4, sw=1)
    f.text(14, y + 11, f"{i + 1}. {name[e]}", size=10.5, color=SLATE, bold=True, anchor="start", vmid=True)
    f.text(110, y + 11, f"Q = {s}  ({'Unlocked' if s else 'Locked'})", size=10.5, color=SLATE, anchor="start", vmid=True)
    f.text(235, y + 11, res, size=10.5, color=RED if res in ("blocked", "coin wasted") else TEAL, bold=True, anchor="start", vmid=True)
    q = s
f.text(200, 304, f"Totals: {passes} people passed, {blocked} blocked, {wasted} coin wasted.", size=10.5, color=NAVY, bold=True)
```

## 5.2 Design procedure

1. Understand the specification; draw the **state diagram**.
2. Form the **state table** (present state, input → next state, output).
3. **Reduce** the states (merge equivalent states).
4. **Assign** binary codes (n flip-flops for up to 2ⁿ states); any assignment works but affects the logic cost.
5. Choose the flip-flop type; build the **excitation table**.
6. **Simplify** next-state and output equations with K-maps (unused codes are don't-cares).
7. Draw the circuit; confirm unused states do not trap the machine.

## 5.3 State reduction by partitioning

Two states are **equivalent** if, for every input sequence, they give the same outputs. Partition method: put states with identical outputs in one block, then split any block whose members go to different blocks for some input; repeat until nothing splits.

::: example Worked example: Moore machine with four states
| State | Output | next, x = 0 | next, x = 1 |
|---|---|---|---|
| A | 0 | B | C |
| B | 0 | A | D |
| C | 1 | A | C |
| D | 1 | A | C |

P₁ by output: {A, B}, {C, D}. For input 0, A→B and B→A both land in block 1, and C→A, D→A land in block 1. For input 1, A→C and B→D both land in block 2, and C→C, D→C both land in block 2. No block splits, so A ≡ B and C ≡ D: **the four-state machine reduces to two states.**
:::

Fewer states can mean fewer flip-flops and gates, but the benefit is largest on machines drawn without care.

## 5.4 Worked design: a "101" sequence detector (Mealy, overlapping)

**Specification.** One serial input x per clock. The output z is 1 exactly when the last three bits received were 1, 0, 1. Overlap allowed: the stream 10101 gives two detections.

**States.** S₀ = nothing useful seen; S₁ = last bit was 1; S₂ = last two bits were 10.

| Present | x = 0: next / z | x = 1: next / z |
|---|---|---|
| S₀ | S₀ / 0 | S₁ / 0 |
| S₁ | S₂ / 0 | S₁ / 0 |
| S₂ | S₀ / 0 | S₁ / 1 |

(From S₂ a 1 completes 101, so z = 1 and, because the final 1 can start a new 101, the next state is S₁.)

**Assignment.** Q₁Q₀: S₀ = 00, S₁ = 01, S₂ = 10; code 11 unused (don't-care). Use D flip-flops (D = next state).

| Q₁ Q₀ x | D₁ | D₀ | z |
|---|---|---|---|
| 0 0 0 | 0 | 0 | 0 |
| 0 0 1 | 0 | 1 | 0 |
| 0 1 0 | 1 | 0 | 0 |
| 0 1 1 | 0 | 1 | 0 |
| 1 0 0 | 0 | 0 | 0 |
| 1 0 1 | 0 | 1 | 1 |
| 1 1 x | X | X | X |

K-maps with the don't-cares give **D₁ = Q₀x', D₀ = x, z = Q₁x.**

**Test.** Input 1 0 1 0 1 1 0 1 gives states S₁, S₂, S₁, S₂, S₁, S₁, S₂, S₁ and outputs **0 0 1 0 1 0 0 1**: detections after the 3rd, 5th and 8th bits, each completing 101 (bits 1–3, 3–5, 6–8).

**Using JK or T flip-flops** changes only step 5: fill J, K (or T) columns from the excitation table of Unit 4 for each present → next pair, then simplify as before.

```svgfig label="5.1" caption="State diagram of the overlapping 101 sequence detector (Mealy). Arc labels are x/z: input bit / output bit. S0 = nothing useful seen, S1 = last bit was 1, S2 = last two bits were 10. The only arc with z = 1 is S2 to S1 on input 1."
f = Fig(760, 290)
for name, cx, sub in (("S0", 120, "00"), ("S1", 340, "01"), ("S2", 560, "10")):
    f.circle(cx, 140, 32, fill=SOFT, stroke=NAVY, label=name, size=14, color=NAVY)
    f.text(cx, 192, "Q1Q0 = " + sub, size=9.5, color=SLATE)
f.arrow([(152, 130), (308, 130)], color=SLATE, sw=1.8, label="1/0", lpos=(230, 118))
f.arrow([(372, 130), (528, 130)], color=SLATE, sw=1.8, label="0/0", lpos=(450, 118))
f.arrow([(528, 152), (372, 152)], color=RED, sw=2.2, label="1/1  (detected)", lpos=(450, 170))
f.arrow([(560, 172), (560, 250), (120, 250), (120, 172)], color=SLATE, sw=1.8, label="0/0", lpos=(340, 242))
f.arrow([(104, 110), (104, 70), (136, 70), (136, 108)], color=SLATE, sw=1.8, label="0/0", lpos=(120, 60))
f.arrow([(324, 110), (324, 70), (356, 70), (356, 108)], color=SLATE, sw=1.8, label="1/0", lpos=(340, 60))
f.arrow([(30, 140), (86, 140)], color=TEAL, sw=2, label="start", lpos=(40, 128))
f.box(630, 90, 120, 100, "", fill=SOFT, stroke="#cbd5e1")
f.text(690, 110, "Input 10101", size=10, color=NAVY, bold=True); f.text(690, 130, "S0 S1 S2 S1 S2 S1", size=9, color=SLATE)
f.text(690, 150, "z = 0 0 1 0 1", size=10, color=RED, bold=True); f.text(690, 170, "two detections", size=9.5, color=SLATE)
```

```svgfig label="5.2" caption="Mealy against Moore on the same input stream 1 0 1 0 1 1 0 1 for the overlapping 101 detector, simulated clock by clock. The Mealy machine needs 3 states and answers in the same clock cycle as the last input bit; the Moore machine needs 4 states and its output appears one cycle later."
mealy = {("S0", 0): ("S0", 0), ("S0", 1): ("S1", 0), ("S1", 0): ("S2", 0), ("S1", 1): ("S1", 0), ("S2", 0): ("S0", 0), ("S2", 1): ("S1", 1)}
moore = {("A", 0): "A", ("A", 1): "B", ("B", 0): "C", ("B", 1): "B", ("C", 0): "A", ("C", 1): "D", ("D", 0): "C", ("D", 1): "B"}
x = [1, 0, 1, 0, 1, 1, 0, 1]
s, zm, sm = "S0", [], []
for b in x:
    s, z = mealy[(s, b)]; zm.append(z); sm.append(s)
t, zo, so = "A", [0], ["A"]
for b in x:
    t = moore[(t, b)]; zo.append(1 if t == "D" else 0); so.append(t)
assert zm == [0, 0, 1, 0, 1, 0, 0, 1] and zo == [0, 0, 0, 1, 0, 1, 0, 0, 1]
assert zo[1:] == zm and sum(zm) == sum(zo) == 3
f = Fig(760, 270)
f.text(380, 16, "Input stream x and the two outputs (1 = pattern 101 just completed)", size=11.5, color=NAVY, bold=True)
cx = lambda k: 150 + k * 66
f.text(10, 50, "Cycle", size=10.5, color=NAVY, bold=True, anchor="start", vmid=True)
f.text(10, 78, "Input x", size=10.5, color=NAVY, bold=True, anchor="start", vmid=True)
f.text(10, 110, "Mealy state", size=10.5, color=AMBER, bold=True, anchor="start", vmid=True)
f.text(10, 138, "Mealy z", size=10.5, color=AMBER, bold=True, anchor="start", vmid=True)
f.text(10, 176, "Moore state", size=10.5, color=TEAL, bold=True, anchor="start", vmid=True)
f.text(10, 204, "Moore z", size=10.5, color=TEAL, bold=True, anchor="start", vmid=True)
for k in range(9):
    f.text(cx(k) + 24, 50, str(k + 1), size=10.5, color=SLATE, bold=True, vmid=True)
    if k < 8:
        f.box(cx(k), 64, 48, 26, str(x[k]), fill=BLUE, stroke=NAVY, size=11, bold=True)
        f.box(cx(k), 96, 48, 26, sm[k], fill=SAND, stroke=AMBER, size=10.5)
        f.box(cx(k), 124, 48, 26, str(zm[k]), fill=ROSE if zm[k] else SOFT, stroke=RED if zm[k] else "#94a3b8", size=11, bold=True)
    f.box(cx(k), 162, 48, 26, so[k], fill=MINT, stroke=TEAL, size=10.5)
    f.box(cx(k), 190, 48, 26, str(zo[k]), fill=ROSE if zo[k] else SOFT, stroke=RED if zo[k] else "#94a3b8", size=11, bold=True)
f.text(380, 242, "Moore z lags Mealy z by one clock because it depends only on the state reached after the bit.", size=10.5, color=SLATE, bold=True)
f.text(380, 260, "Both find the same 3 patterns (cycles 3, 5 and 8 for Mealy), but Moore needs one more state and flip-flop code.", size=10.5, color=SLATE)
```

```photogrid label="5.2" cols="2" ratio="1.0" caption="How big is the memory of a machine? (a) A lift call button: behind the panel a state machine remembers floor and direction. (b) The number of flip-flops k = ceil(log2 N) needed for N states, computed for six machines, with the unused codes that become don't-cares."
@ photo id="bca103/liftpanel" cap="Lift controller: the state is the floor and the direction of travel"
fit 1.2
focus 0.5 0.5
@ svg cap="States N, flip-flops k, unused codes 2^k - N"
import math
ms = [("Turnstile", 2), ("101 detector, Mealy", 3), ("101 detector, Moore", 4), ("3-phase signal G-Y-R", 3), ("Lift, 3 floors x (idle, up, down)", 9), ("MOD-60 clock counter", 60)]
rows = [(n, N, math.ceil(math.log2(N)), 2 ** math.ceil(math.log2(N)) - N) for n, N in ms]
assert [r[2:] for r in rows] == [(1, 0), (2, 1), (2, 0), (2, 1), (4, 7), (6, 4)]
f = Fig(400, 340)
f.text(8, 16, "Machine", size=10.5, color=NAVY, bold=True, anchor="start")
for x, h in ((220, "N"), (258, "k"), (300, "Unused")): f.text(x, 16, h, size=10.5, color=NAVY, bold=True, anchor="start")
for i, (n, N, k, u) in enumerate(rows):
    y = 28 + i * 50
    f.box(4, y, 392, 44, "", fill=BLUE if i % 2 == 0 else SOFT, stroke="#cbd5e1", r=4, sw=1)
    f.text(10, y + 16, n, size=10.5, color=SLATE, bold=True, anchor="start", vmid=True)
    f.text(220, y + 16, str(N), size=10.5, color=SLATE, anchor="start", vmid=True)
    f.text(258, y + 16, str(k), size=10.5, color=TEAL, bold=True, anchor="start", vmid=True)
    f.text(300, y + 16, str(u), size=10.5, color=SLATE, anchor="start", vmid=True)
    for j in range(k): f.box(10 + j * 22, y + 26, 18, 12, "", fill=MINT, stroke=TEAL, r=2)
f.text(200, 332, "Each green square is one flip-flop.", size=10, color=SLATE)
```

## 5.5 Counter design as a special case

A counter is an FSM with no inputs. The mod-3 JK design in Unit 4 and the Gray counter D₁ = Q₀, D₀ = Q₁' follow the same seven steps. For the Gray counter 00 → 01 → 11 → 10 → 00: next Q₁ sequence is 0, 1, 1, 0 and next Q₀ is 1, 1, 0, 0 for the present states 00, 01, 11, 10, which reads directly as D₁ = Q₀ and D₀ = Q₁'.

**Lock-out.** If an unused state (like 11 above) leads to another unused state forever, the counter is stuck after a power glitch. Design every unused state to enter the main sequence, as the MOD-3 design does.

## 5.6 Eight applications of finite state machines

1. **Traffic signals.** A signal controller is a Moore machine whose states are the lamp patterns, such as green, yellow and red. A timer or a sensor gives the input that moves it to the next state. The signals at a busy junction in Kathmandu run on this idea.
2. **Lifts.** The state is the present floor and the direction of travel, and the inputs are the buttons pressed (Plate 5.2). The machine decides to stop, open the door or move on. Every modern lift in a Nepali building uses a controller of this kind.
3. **Turnstiles and ticket gates.** The two-state machine of Plate 5.1 lets one person through for each coin or ticket. Stadium gates, parking barriers and airport boarding gates follow the same rule. The same pattern is used for any lock that opens once and then closes again.
4. **Vending and coin machines.** The state records the money inserted so far, and the output releases the item when the total is enough. Each coin is an input event. Ticket machines and prepaid payphones were built this way.
5. **ATM and keypad locks.** An ATM moves through card inserted, PIN entry, amount selection and cash dispensing. A wrong PIN three times sends it to a blocked state. A digital door lock with a secret code is a sequence detector like the 101 detector.
6. **Pattern matching in software.** The compilers of C and Java use a state machine to recognise words and numbers in the source code. Search tools and virus scanners match text using state machines too. The 101 detector of Section 5.4 is the smallest example.
7. **Communication protocols.** TCP, which carries every web page, is defined as a state machine with states such as LISTEN, SYN-SENT and ESTABLISHED. Each packet that arrives is an input. A protocol bug is often a missing arrow in the state diagram.
8. **Household appliances.** A washing machine moves through fill, wash, rinse and spin, and a microwave oven through set, cook and beep. Each step ends by a timer or a sensor. Because the machine has few states, the controller chip is cheap.

## 5.7 Laboratory works in the TU practical syllabus

The course has 2 practical hours a week. The six prescribed laboratory works are summarised here, so that the theory of Units 3 to 5 is linked to the bench. For each lab: **aim, parts, procedure, expected result and viva questions.** Use a 5 V supply, a breadboard and a logic probe or LEDs with 330-ohm resistors.

| Lab | Title | Where the theory is |
|---|---|---|
| 1 | Gates using active and passive elements | Section 3.9 |
| 2 | Half adder and full adder | Section 3.4 |
| 3 | 16:1 multiplexer | Sections 3.5 and 3.8 |
| 4 | 1:16 demultiplexer | Sections 3.5 and 3.8 |
| 5 | Digital watch using counters | Sections 4.2, 4.4 and 5.5 |
| 6 | Shift registers | Section 4.3 |

### Lab 2: half adder and full adder
*Parts:* 7486 (XOR), 7408 (AND), 7432 (OR), LEDs. *Procedure:* wire S = A XOR B and C = AB for the half adder; then use two half adders and an OR gate for the full adder. Apply all eight combinations of A, B, Cin and record Sum and Cout. *Expected:* the truth table has Sum = 1 for an odd number of ones, Cout = 1 for two or more ones. *Viva:* why does a full adder need three inputs? How is a ripple-carry adder formed from it?

### Lab 3: 16:1 multiplexer
*Parts:* 74153 (dual 4-to-1 MUX) or 74151 (8-to-1), 74150 (16-to-1) if available. *Procedure:* with 74150, set the data inputs to a known pattern (for example, alternate 0 and 1) with DIP switches, count through select codes 0000 to 1111 and observe the output (74150 gives the *inverted* data, so add an inverter). Without 74150, use the tree of Figure 3.5. *Expected:* the output equals the data input whose number is on the select lines. *Viva:* how many MUX chips are needed for a 64-to-1 MUX? (Answer: 16 + 4 + 1 = 21 4-to-1 MUXes, or 8 + 1 = 9 8-to-1 MUXes.)

### Lab 4: 1:16 demultiplexer
*Parts:* 74154 4-to-16 decoder/DEMUX, LEDs with resistors. *Procedure:* put the data bit on one enable pin (G1 low, data on G2), select lines S3 S2 S1 S0 on the address inputs. Output lines are active low, so the addressed LED *lights when the data bit is 0*. *Expected:* only the addressed output follows the data; others stay high. *Viva:* difference between a decoder and a DEMUX.

### Lab 5: digital watch using counters
*Aim:* count seconds, minutes and hours from a 1 Hz clock. *Parts:* a 555 timer or a 32.768 kHz crystal with a CD4060 divider for the 1 Hz clock; 7490 or 74192 counters; 7447 decoders; common-anode seven-segment displays.

1. **Clock.** A 555 astable with R1 = 1 kilo-ohm, R2 = 68 kilo-ohm and C = 10 microfarad gives f = 1.44 / ((R1 + 2 R2) C) = 1.44 / (137 kilo-ohm x 10 microfarad), about 1.05 Hz. A crystal of 32 768 Hz divided by 2¹⁵ gives exactly 1 Hz and is much more accurate.
2. **Seconds.** A mod-10 counter (units) followed by a mod-6 counter (tens): 10 x 6 = 60. The carry of the units drives the tens counter; when the tens counter reaches 6 (0110), it resets itself to 0 and sends a carry to the minutes.
3. **Minutes.** Another mod-60 chain, clocked by the seconds carry.
4. **Hours.** A mod-24 counter (or mod-12): reset to 00 when the count reaches 24 (the tens digit 2 and units digit 4).
5. **Display.** Each BCD digit goes to a 7447 and a seven-segment display.

*Expected:* the display counts 00:00:00 to 23:59:59 and rolls over. *Viva:* how do you get a mod-60 counter from a mod-10 and mod-6 counter? Why is a crystal clock more accurate than the 555?

### Lab 6: shift registers
*Parts:* 7495 or 74194 universal shift register, switches, LEDs. *Procedure:* (a) *serial in, serial out*: apply serial data with one clock pulse per bit and watch it move; (b) *serial in, parallel out*: after four clocks read all four outputs; (c) *parallel in, serial out*: load with the load line, then clock; (d) *parallel in, parallel out*; (e) *shift right and shift left* with the mode input. *Expected:* a 4-bit register takes 4 clock pulses to move a bit through. *Viva:* how can a shift register multiply or divide by 2? What is a ring or Johnson counter built from a shift register?

::: note Safety and good practice for all labs
Switch the supply off while wiring. Never connect an IC output directly to ground or +5 V. Use a series resistor with every LED. Do not leave CMOS inputs floating. Always draw the circuit and the truth table in the record before the bench work.
:::

## Formula and fact sheet

- Moore: z = f(state). Mealy: z = f(state, input).
- n flip-flops → at most 2ⁿ states. Unused codes are don't-cares.
- Partition: group by output, split by next-state blocks, repeat.
- Overlapping "101" detector: D₁ = Q₀x', D₀ = x, z = Q₁x (codes 00/01/10).
- Excitation tables convert state changes into flip-flop inputs.

## Chapter summary

- An FSM is a state register plus next-state and output logic.
- Mealy outputs react to the input directly; Moore outputs change only with the state.
- State reduction and sensible assignment shrink the circuit.
- Always check the unused states and test the design with a sample input stream.

## Practice

1. Differentiate Moore and Mealy machines with one example each.
2. How many flip-flops are needed for a machine with 9 states? With 4 states after reduction?
3. Reduce the following Moore machine: states A(0): 0→B, 1→A; B(0): 0→A, 1→B; C(1): 0→C, 1→A. State whether any states merge.
4. Modify the "101" detector so that overlap is **not** allowed (after a detection restart from S₀). Give the changed row and re-derive z.
5. Design a "11" detector (output 1 when the last two bits are 11, overlapping) with D flip-flops; give D and z.
6. For the detector designed in the text, give the output for the input 1 1 0 1 0 1.
7. Why must unused states be considered in the design?

::: note Answers and worked solutions
**1.** Moore: output depends on state only, such as a traffic light controller whose lamp colour is a function of the state. Mealy: output depends on state and input, such as the "101" detector whose output is 1 only while the final 1 is present.
**2.** 9 states → ⌈log₂ 9⌉ = 4 flip-flops; 4 states → 2.
**3.** Outputs: A and B give 0, C gives 1. Partition P₁ = {A, B}, {C}. For x = 0: A→B, B→A (both block 1). For x = 1: A→A, B→B (both block 1). No split: A ≡ B. C is alone. The machine reduces to two states, {A, B} and C. (C is also unreachable from A and B, so it could be removed entirely.)
**4.** From S₂ with x = 1 the output is 1 and the next state is S₀ instead of S₁. The z equation is the same (z = Q₁x); D₀ changes to D₀ = x·Q₁' (the S₂ → S₀ move no longer sets Q₀), while D₁ = Q₀x' is unchanged.
**5.** States: S₀ (no 1 just seen), S₁ (last bit was 1). S₀: x = 0 → S₀/0, x = 1 → S₁/0. S₁: x = 0 → S₀/0, x = 1 → S₁/1. With Q = 0 for S₀ and 1 for S₁: D = x and z = Qx.
**6.** The machine goes S₀→S₁ (x=1, z0), S₁→S₁ (x=1, z0), S₁→S₂ (x=0, z0), S₂→S₁ (x=1, z1), S₁→S₂ (x=0, z0), S₂→S₁ (x=1, z1). Output 0 0 0 1 0 1.
**7.** A glitch, noise or power-up can put the flip-flops in an unused code. If its transitions are not defined, the machine may never return to the intended sequence (lock-out).
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q (5 marks). Distinguish between Mealy and Moore machines with a block diagram description and one example each.**

A **sequential machine** has a memory (flip-flops holding the present state) and combinational logic that computes the next state and the output. The two models differ only in how the output is formed.

| Point | Mealy machine | Moore machine |
|---|---|---|
| Output depends on | present state **and** present input | present state **only** |
| Output written on | the transition arc (x/z) | inside the state circle |
| Response | can change in the same clock period as the input | changes only after the clock edge |
| Number of states | usually fewer | usually more (about one extra) |
| Glitches | input noise may reach the output | outputs are clean, synchronous |
| Example | the 101 detector in Figure 5.1 | a traffic-light controller |

In a Mealy machine, Z = g(Q, X) and Q⁺ = f(Q, X); in a Moore machine, Z = g(Q) and Q⁺ = f(Q, X). For example, in the 101 detector of Figure 5.1 the output z = Q₁·x depends on the input, so it is Mealy. In a Moore version the detector needs a fourth state S3 = "101 seen" with output 1 written inside the state, and the output appears one clock later. A traffic-light controller (red, green, amber) is naturally Moore, because each light depends only on the state it is in. Moore outputs are glitch-free, while Mealy machines react faster and need fewer flip-flops.

**Q (10 marks). Design an overlapping "101" sequence detector as a Mealy machine using D flip-flops. Show the specification, state diagram, state table, assignment, excitation equations and the circuit.**

*Specification.* One serial bit x is applied per clock. The output z must be 1 exactly when the last three bits received are 1, 0, 1. Overlap is allowed, so the stream 10101 gives two detections.

*Step 1: states and diagram.* Three states record how much of the pattern has been seen: S0 (nothing useful), S1 (last bit 1) and S2 (last two bits 10). Figure 5.1 shows the arcs: from S0, 0 stays and 1 goes to S1; from S1, 1 stays and 0 goes to S2; from S2, 0 returns to S0 and 1 completes the pattern, so z = 1, and the new 1 may begin another 101 so the next state is S1.

*Step 2: state table.*

| Present | x = 0: next / z | x = 1: next / z |
|---|---|---|
| S0 | S0 / 0 | S1 / 0 |
| S1 | S2 / 0 | S1 / 0 |
| S2 | S0 / 0 | S1 / 1 |

*Step 3: state reduction.* Partitioning by output puts S0, S1 and S2 in one block for x = 0 (all give z = 0) but separates S2 for x = 1 (z = 1); the next-state tests then separate S0 from S1, so all three states are distinguishable and no reduction is possible.

*Step 4: assignment.* Two flip-flops are needed (⌈log₂3⌉ = 2): S0 = 00, S1 = 01, S2 = 10; the code 11 never occurs and is a don't-care.

*Step 5: excitation and output equations.* For D flip-flops D = Q⁺. D₁ = 1 only when the next state is S2, which happens from S1 with x = 0, so **D₁ = Q₀·x'**. D₀ = 1 when the next state is S1, which happens for x = 1 from every state, so **D₀ = x**. The output is 1 only in S2 with x = 1: **z = Q₁·x**.

*Step 6: circuit.* Two D flip-flops with a common clock; one AND gate with inputs Q₀ and x' for D₁; D₀ is connected directly to x; one AND gate with inputs Q₁ and x gives z. The total is two flip-flops, two AND gates and one inverter.

*Step 7: check with 10101.* S0 → S1 → S2 → S1 (z = 1) → S2 → S1 (z = 1), giving z = 0, 0, 1, 0, 1, which matches the specification.

*Conclusion.* The procedure (specification, diagram, table, reduction, assignment, equations, circuit) is the same for every sequential design; a counter is the special case in which the next state does not depend on the input.

**Q (5 marks). How many flip-flops are needed for a sequential machine? What is state assignment?**

A machine with **N states** needs **k flip-flops** where 2ᵏ ≥ N, that is k = ⌈log₂ N⌉. Each state gets a different k-bit code, and this choice is called **state assignment**. Plate 5.2 lists real examples: a turnstile has 2 states and needs 1 flip-flop, the Mealy 101 detector has 3 states and needs 2, a lift with 3 floors and three movement modes has 9 states and needs 4.

1. **Count the states** from the state diagram after state reduction, because fewer states can mean fewer flip-flops.
2. **Find k** from 2ᵏ ≥ N.
3. **Assign codes.** Any assignment works, but good ones give simpler equations: states that follow one another should differ in few bits.
4. **Treat the unused codes as don't-cares** on the Karnaugh maps; the 101 detector has code 11 unused, which makes the equations shorter.

| Machine | N | k | Unused codes |
|---|---|---|---|
| Turnstile | 2 | 1 | 0 |
| 101 Mealy | 3 | 2 | 1 |
| 101 Moore | 4 | 2 | 0 |
| 3 floors × (idle, up, down) | 9 | 4 | 7 |

**Example.** For the 101 detector with S₀ = 00, S₁ = 01 and S₂ = 10, the code 11 never occurs, so it is marked X in the next-state maps. Figure 5.2 shows that the Moore version needs one more state (4 instead of 3), although both use 2 flip-flops here.

**Q (10 marks). Design a turnstile controller using a D flip-flop. Verify it with a sequence of events.**

**Introduction.** A turnstile (Plate 5.1) has an arm that is **Locked** until a coin is inserted and then **Unlocked** until one person pushes through. It is a good example of a sequential machine because its behaviour depends on its history. We design it as a **Moore machine**, since the output "arm free" depends only on the state.

**Step 1: specification.** Inputs: C = coin inserted, P = push on the arm. In each clock cycle at most one of them is 1. Output U = 1 when the arm is free.

**Step 2: states.** L (Locked, U = 0) and U (Unlocked, U = 1). Two states need k = 1 flip-flop; assign L = 0 and U = 1, so Q is the output itself.

**Step 3: state table.**

| Present Q | C P | Next Q⁺ | Meaning |
|---|---|---|---|
| 0 (L) | 0 0 | 0 | stay locked |
| 0 (L) | 0 1 | 0 | push is blocked |
| 0 (L) | 1 0 | 1 | coin unlocks |
| 1 (U) | 0 0 | 1 | stay unlocked |
| 1 (U) | 0 1 | 0 | person passes, lock again |
| 1 (U) | 1 0 | 1 | extra coin is wasted |

**Step 4: equation.** The next state is 1 when a coin arrives or when the gate is unlocked and nobody pushes, so **D = Q⁺ = C + Q·P′**. The case C = P = 1 never occurs and is a don't-care.

**Step 5: circuit.** One D flip-flop, one NOT gate (P′), one AND gate (Q·P′) and one OR gate (C + Q·P′). Output U = Q. A clear input sets Q = 0 at power-up so that the gate starts Locked.

**Step 6: verification.** The events C P P C C P idle P C P give the states 1, 0, 0, 1, 1, 0, 0, 0, 1, 0 (Plate 5.1). Three persons passed, two pushes were blocked and one coin was wasted, which is exactly what the specification demands.

| Part | Choice |
|---|---|
| Machine type | Moore |
| Number of states | 2 |
| Flip-flops | 1 D flip-flop |
| Gates | NOT, AND, OR |
| Equation | D = C + Q·P′ |

**Conclusion.** The same procedure of specification, states, table, equation, circuit and verification works for a machine of any size. Only the number of flip-flops and the size of the Karnaugh maps grow. A designer must always check the don't-care input combinations and give the machine a safe starting state.
