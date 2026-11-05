---
subject: Microprocessor and Computer Architecture
grade: BCA Semester 2
unit: 4
title: Microprogrammed and Hardwired Control
area: BCA 152 · Microprocessor and Computer Architecture · Unit 4
---

The control unit decides *which control signals fire at each clock tick*. There are two ways to build it: as a fixed circuit of gates (**hardwired**) or as a tiny stored program called a **microprogram** (**microprogrammed**). This unit shows both, builds a microprogram for the basic computer's fetch and ADD, and explains how a micro-sequencer picks the next microinstruction.

::: key What this unit gives you
- Micro-operations, microinstructions, microprograms; the role of control memory.
- Hardwired versus microprogrammed control, with trade-offs.
- Control memory, address sequencing, conditional branching, mapping, subroutines.
- The microinstruction format and symbolic/binary microprograms (FETCH and ADD).
- Design of the control unit: requirements, structure, and the micro-program sequencer.
- Control of the AC register and ALU organisation.
:::

## 4.1 Micro-operations and control signals

A **micro-operation** is one elementary register-level action done in one clock period — `AR ← PC`, `AC ← AC + DR`, `PC ← PC + 1`. An instruction is carried out by a sequence of micro-operations; a **control word** is the set of bits that enables exactly the micro-operations of one clock period. Micro-operations are of four kinds:

1. **Register-transfer** (`R1 ← R2`).
2. **Arithmetic** (add, subtract, increment, decrement, complement).
3. **Logic** (AND, OR, XOR, clear, complement).
4. **Shift** (logical, arithmetic, circular).

**Control signals** open the paths for these actions (select a bus source, load a register, set an ALU function, read or write memory).

## 4.2 Hardwired control

In a **hardwired** control unit the control functions are implemented directly as a **network of gates, decoders and flip-flops**. The basic computer of Unit 3 is hardwired: the sequence counter feeds a decoder giving T0–T15, the opcode feeds a decoder giving D0–D7, and each control signal is a Boolean expression such as `LD(AC) = D0T5 + D1T5 + D2T5 + …`.

Design steps: write down the micro-operations for every instruction; derive, for every control input, the Boolean function of timing, opcode and flag signals; minimise the logic; build the gates.

| | Advantages | Disadvantages |
|---|---|---|
| **Hardwired** | very fast — no memory lookup, only gate delays | hard to design for large instruction sets; changes mean redesign; inflexible |

## 4.3 Microprogrammed control

A **microprogrammed** control unit stores the control words in a special memory — the **control memory** (usually ROM; writable control stores exist too). Each word of control memory is a **microinstruction**, which specifies the micro-operations of one step plus how to find the next microinstruction. A sequence of microinstructions that implements one machine instruction is a **microprogram** (or routine). The microprograms for the whole instruction set together are the **firmware**.

Terms:

- **Microinstruction** — one word of control memory: control bits plus next-address information.
- **Microprogram** — the sequence of microinstructions for one machine instruction.
- **Micro-operation** — what a microinstruction causes to happen.
- **Control address register (CAR)** — holds the address of the microinstruction to be executed.
- **Control data register** (pipeline register) — holds the microinstruction being executed, letting the next one be fetched meanwhile.

| | Hardwired | Microprogrammed |
|---|---|---|
| Speed | faster | slower (a control-memory read per step) |
| Flexibility | fixed | change the microprogram, not the hardware |
| Design effort | grows steeply with instruction set | systematic, regular |
| Cost/complexity | cheaper for simple CPUs | better for complex instruction sets (CISC) |
| Typical use | RISC CPUs, simple processors | CISC processors (older x86), bug fixes by microcode update |
| Error repair | rewire | update the microcode |

Modern x86 chips combine both: a hardwired fast path for simple instructions and microcode for complex ones, and they can load **microcode updates** at boot.

## 4.4 The microprogrammed control unit

```
 external input (opcode, status)
        │
        ▼
 ┌─────────────┐   ┌──────────────┐   ┌──────────────────┐   ┌────────────────────┐
 │ next-address│──►│ control      │──►│ control memory   │──►│ control data       │──► control signals
 │ generator   │   │ address reg. │   │ (microprogram    │   │ register (pipeline)│    (to datapath)
 │ (sequencer) │   │ CAR          │   │  ROM)            │   │                    │
 └─────────────┘   └──────────────┘   └──────────────────┘   └────────────────────┘
        ▲                                                            │
        └──────── next-address information, condition bits ──────────┘
```

- The **control memory** holds the microprogram.
- The **CAR** supplies the address; the microinstruction is read into the control data register.
- The **next-address generator (micro-program sequencer)** computes the next CAR value from: the current CAR + 1, an address field in the microinstruction (branch), a **mapped** address from the machine opcode (start of a new routine), a return address from a **subroutine register (SBR)**, or a condition test.

### Address sequencing

How the next microinstruction is chosen:

| Mechanism | Next CAR |
|---|---|
| **Incrementing** | CAR + 1 (the default) |
| **Unconditional branch** | the AD field of the microinstruction |
| **Conditional branch** | AD if the tested condition (e.g. AC = 0, sign) is true, else CAR + 1 |
| **Mapping** | formed from the opcode in IR: bits `0 xxxx 00` — each opcode gets a 4-word block |
| **Subroutine call/return** | CALL: SBR ← CAR + 1, CAR ← AD; RET: CAR ← SBR |

::: key Mapping
A machine instruction's opcode must be converted into the *start address of its microprogram*. A simple map places the opcode in the middle of the CAR: with a 4-bit opcode, CAR = 0 + opcode + 00 (7 bits for a 128-word memory). Opcode 0000 → address 0, 0001 → 4, 0010 → 8, 0011 → 12: each routine gets 4 words. A routine longer than 4 words branches to a shared area.
:::

### Conditional branching

A **status-bit test** selects between a branch and the next sequential address. Condition inputs include the sign of AC, AC = 0, the carry E, the I (indirect) bit and the interrupt flag. The microinstruction names *which* condition to test; the sequencer multiplexer picks that bit and, if true, loads the branch address.

## 4.5 A microinstruction format (the Mano example)

A 20-bit microinstruction in a 128-word control memory (7-bit addresses, 128 × 20 = 2560 bits):

```
  3     3     3    2    2     7
┌─────┬─────┬─────┬────┬────┬────────┐
│ F1  │ F2  │ F3  │ CD │ BR │   AD   │
└─────┴─────┴─────┴────┴────┴────────┘
```

- **F1, F2, F3** (3 bits each): three micro-operation fields; each selects one of 7 micro-operations (000 = none). Three fields mean up to three micro-operations *in parallel* per microinstruction, as long as they use different hardware.
- **CD** (condition, 2 bits): 00 = always 1 (unconditional), 01 = indirect bit I, 10 = AC sign bit, 11 = AC = 0.
- **BR** (branch, 2 bits): 00 **JMP** (jump to AD if condition = 1, else CAR + 1), 01 **CALL** (same, but save return address), 10 **RET** (CAR ← SBR), 11 **MAP** (CAR ← mapped opcode).
- **AD** (address, 7 bits): the branch address.

The micro-operation tables (symbol = what it does):

| F1 | Symbol | Micro-operation | F2 | Symbol | Micro-operation | F3 | Symbol | Micro-operation |
|---|---|---|---|---|---|---|---|---|
| 000 | NOP | none | 000 | NOP | none | 000 | NOP | none |
| 001 | ADD | AC ← AC + DR | 001 | SUB | AC ← AC − DR | 001 | XOR | AC ← AC ⊕ DR |
| 010 | CLRAC | AC ← 0 | 010 | OR | AC ← AC ∨ DR | 010 | COM | AC ← AC′ |
| 011 | INCAC | AC ← AC + 1 | 011 | AND | AC ← AC ∧ DR | 011 | SHL | AC ← shl AC |
| 100 | DRTAC | AC ← DR | 100 | READ | DR ← M[AR] | 100 | SHR | AC ← shr AC |
| 101 | DRTAR | AR ← DR(0–10) | 101 | ACTDR | DR ← AC | 101 | INCPC | PC ← PC + 1 |
| 110 | PCTAR | AR ← PC | 110 | INCDR | DR ← DR + 1 | 110 | ARTPC | PC ← AR |
| 111 | WRITE | M[AR] ← DR | 111 | PCTDR | DR(0–10) ← PC | 111 | — | unused |

Two micro-operations that need *different* hardware can share one microinstruction by being placed in different fields — for example `READ` (F2) and `INCPC` (F3) in the fetch routine, or `ACTDR` and `DRTAC` together, which swaps AC and DR because both transfers use the old values in the same clock period.

## 4.6 Symbolic and binary microprograms

A **symbolic microprogram** is the readable, assembly-like form, listing for each microinstruction a label, the three micro-operations, the condition, the branch type and the address. It is translated by a **microprogram assembler** into the **binary microprogram** (the 20-bit words to burn into ROM).

### The fetch routine (always at address 64)

```
        ORG 64
FETCH:  PCTAR            U   JMP  NEXT     ; AR ← PC
        READ, INCPC      U   JMP  NEXT     ; DR ← M[AR], PC ← PC + 1
        DRTAR            U   MAP           ; AR ← DR(0–10), then map opcode → routine
```
Three microinstructions (the third needs no jump label: `MAP` loads CAR from the opcode). **U** means unconditional, **NEXT** means the following address.

### The ADD routine (opcode 0000 → address 0)

```
        ORG 0
ADD:    NOP              I   CALL INDRCT   ; if indirect (I = 1), call INDRCT
        READ             U   JMP  NEXT     ; DR ← M[AR]
        ADD              U   JMP  FETCH    ; AC ← AC + DR, go back to fetch

INDRCT: READ             U   JMP  NEXT     ; DR ← M[AR]
        DRTAR            U   RET           ; AR ← DR(0–10), return
```
Trace of `ADD` with direct addressing: the first microinstruction tests I (= 0, so no call), then READ loads the operand into DR, then ADD adds it to AC and jumps to FETCH (64). With indirect addressing the CALL goes to INDRCT, which reads the pointer, loads AR, and returns to the next word.

The **binary** form of one line, e.g. `ADD U JMP FETCH`: F1 = 001 (ADD), F2 = 000, F3 = 000, CD = 00 (U), BR = 00 (JMP), AD = 1000000 (64): `001 000 000 00 00 1000000`. The other routines follow the same pattern:

```
        ORG 4
BRANCH: NOP    S   JMP  OVER      ; S: branch if AC is negative…
        NOP    U   JMP  FETCH
OVER:   NOP    I   CALL INDRCT
        ARTPC  U   JMP  FETCH     ; PC ← AR

        ORG 8
STORE:  NOP    I   CALL INDRCT
        ACTDR  U   JMP  NEXT      ; DR ← AC
        WRITE  U   JMP  FETCH     ; M[AR] ← DR

        ORG 12
EXCHANGE: NOP  I   CALL INDRCT
        READ   U   JMP  NEXT
        ACTDR, DRTAC  U  JMP NEXT  ; swap AC and DR
        WRITE  U   JMP  FETCH
```
Four routines, four words each (addresses 0, 4, 8, 12) — exactly what the mapping `0 + opcode + 00` provides. The opcodes are ADD = 0000, BRANCH = 0001, STORE = 0010, EXCHANGE = 0011. In BRANCH the condition **S** (AC sign) makes the first microinstruction jump to OVER when AC is negative; otherwise the second one returns to FETCH, so the branch is taken only if AC < 0.

## 4.7 Design of the control unit

### Requirements

The control unit must (1) **sequence** the steps of the instruction cycle (fetch, decode, execute); (2) **generate the correct control signals** at the correct time; (3) **react to status** flags and interrupts; (4) **start the right routine** for each opcode. In a microprogrammed unit requirement (4) is the mapping logic and (2) is the control memory.

### Structure of the microprogrammed control unit

- **Control memory** (ROM, e.g. 128 × 20);
- **Control address register (CAR)**;
- **Control data register** (pipeline register) holding the current microinstruction so the next can be fetched during execution;
- **Sequencer** — the next-address logic: multiplexer choosing among CAR + 1, AD, mapped address, SBR; a **condition multiplexer** driven by CD; and an **incrementer**;
- **Decoders** turning the F1, F2, F3 fields into the actual control signals for the datapath.

The design effort of a microprogrammed unit is in writing the microcode, not in routing gates, which is why it scales to large instruction sets.

### The micro-program sequencer

A commercial sequencer (e.g. the AMD 2910) packages the address-selection logic: it holds the CAR, an incrementer, the SBR/stack for subroutines and loop counters, and a multiplexer with inputs "CAR + 1", "branch address", "stack/return" and "mapped". Its inputs are the **instruction field** (jump/call/return/map), the **condition test** (pass/fail) and the **branch address**; its output is the next CAR. A microprogrammed control unit is therefore: *sequencer + ROM + pipeline register*.

## 4.8 Control of the AC register and the ALU

Each register is built from flip-flops with **load**, **increment** and **clear** inputs. The AC register gets its input from the **ALU**, and its control signals come from the same Tᵢ·Dⱼ products:

```
r = D7 I′ T3   (register-reference)      p = D7 I T3   (input-output)

LD(AC)  = D0T5 + D1T5 + D2T5 + p·B11 + r·(B9 + B7 + B6)   ; AND, ADD, LDA, INP, CMA, CIR, CIL
INR(AC) = r·B5                                            ; INC
CLR(AC) = r·B11                                           ; CLA
```
Here B11, B9, B7, B6, B5 are the individual bits of the instruction (CLA = bit 11, CMA = bit 9, CIR = bit 7, CIL = bit 6, INC = bit 5 — compare the codes 7800, 7200, 7080, 7040, 7020 in Unit 3). The **ALU** is a combinational circuit with inputs AC, DR and INPR and outputs to AC. Its operations (add, AND, transfer DR, transfer INPR, complement, shift right, shift left) are selected by control signals from the control unit; E receives the carry-out. Shifts through E (CIR, CIL) are done in the AC register logic rather than the adder.

## Formula and fact sheet

- Control memory 128 × 20 → 2560 bits; microinstruction = F1 (3) + F2 (3) + F3 (3) + CD (2) + BR (2) + AD (7) = 20 bits.
- Mapping: CAR = 0 + opcode(4) + 00 ⇒ opcode n → address 4n.
- Fetch routine at address 64: PCTAR; READ, INCPC; DRTAR, MAP.
- BR: 00 JMP, 01 CALL, 10 RET, 11 MAP. CD: 00 always, 01 I, 10 AC sign, 11 AC = 0.
- Hardwired = fast, inflexible; microprogrammed = flexible, slower; RISC → hardwired; CISC → microcoded.

## Chapter summary

- A micro-operation is one register-level action; a microinstruction packs those of one clock period plus the next-address information; a microprogram is the routine for one machine instruction.
- Hardwired control uses gates, is fast and hard to change; microprogrammed control uses a control memory, is flexible and slower.
- The sequencer chooses the next address by increment, jump, conditional jump, opcode mapping, or subroutine return.
- Mano's 20-bit microinstruction has three micro-operation fields, a condition field, a branch field and a 7-bit address.
- FETCH is three microinstructions, and each machine instruction's routine ends by branching back to FETCH.

## Practice

1. Define micro-operation, microinstruction and microprogram.
2. Differentiate between hardwired and microprogrammed control with advantages of each.
3. Draw the block diagram of a microprogrammed control unit and describe each part.
4. List the ways in which the next microinstruction address can be selected.
5. What is mapping? Find the control-memory address of the routine for opcode 0011 in the Mano scheme.
6. Explain the microinstruction format F1 F2 F3 CD BR AD with sizes.
7. Write the symbolic microprogram for FETCH and explain every line.
8. Write the ADD routine and trace it for an indirect operand.
9. Why is a pipeline register used in the control unit?
10. What is the function of a microprogram sequencer?

::: note Answers and worked solutions
**1.** Micro-operation: a single register-transfer/arith/logic/shift action in one clock; microinstruction: a control-memory word specifying micro-operations of one step and the next address; microprogram: the sequence of microinstructions implementing a machine instruction.
**2.** See the table in section 4.3: hardwired is faster but inflexible and hard to design for big instruction sets; microprogrammed is regular, flexible and field-updatable but slower.
**3.** Sequencer → CAR → control memory → control data register → control signals, with condition/status inputs feeding the sequencer (diagram in 4.4).
**4.** Increment, unconditional branch, conditional branch, opcode mapping, subroutine call/return.
**5.** Mapping converts the opcode into the start address of its routine. Opcode 0011 → 0 0011 00 = 0001100₂ = **12**.
**6.** F1, F2, F3 = 3 bits each (three micro-operations); CD = 2 bits (condition); BR = 2 bits (branch type); AD = 7 bits (branch address): 20 bits in total.
**7.** PCTAR (AR ← PC); READ, INCPC (DR ← M[AR], PC ← PC + 1 in parallel); DRTAR + MAP (AR ← DR(0–10) and CAR ← mapped opcode). The routine always lives at address 64, and each machine instruction ends by jumping back to FETCH.
**8.** ADD: NOP with I CALL INDRCT; READ; ADD, JMP FETCH. If I = 1, the CALL saves CAR + 1 in SBR and enters INDRCT, which reads the pointer (READ), loads AR (DRTAR) and returns (RET) to the READ word; then READ fetches the operand, ADD adds, and control returns to FETCH.
**9.** It holds the current microinstruction while the next one is fetched from control memory, overlapping fetch and execution of microinstructions and shortening the clock period.
**10.** It selects the next control-memory address — CAR + 1, branch, mapped opcode, or return address — according to the instruction field and the condition tests.
:::
