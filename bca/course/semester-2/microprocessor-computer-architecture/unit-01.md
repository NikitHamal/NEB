---
subject: Microprocessor and Computer Architecture
grade: BCA Semester 2
unit: 1
title: Microprocessors and the Intel 8085
area: BCA 152 · Microprocessor and Computer Architecture · Unit 1
---

A microprocessor is a whole CPU on one chip. This unit builds the vocabulary — bus, register, ALU, flag, machine cycle — on the classic **Intel 8085**, a processor small enough to understand completely. Everything later in the book (control units, pipelines, caches) is this same machine made faster.

::: key What this unit gives you
- What a microprocessor is and how a microprocessor system is wired: CPU, memory, I/O and the three buses.
- The architecture of the 8085: registers, ALU, flags, timing and control, interrupts, pins.
- Instruction cycle, machine cycle and T-state, with the timing of the common cycles.
- A first look at the 8086 and why it was a step forward.
:::

## 1.1 What a microprocessor is

A **microprocessor** is a programmable integrated circuit that fetches instructions from memory, decodes them and executes them. Its three jobs: **arithmetic and logic** (the ALU), **temporary storage** (registers) and **control** (sequencing every step with timing signals). A **microcomputer** adds memory and I/O around it; a **microcontroller** puts CPU, memory and I/O on one chip (a washing-machine controller, an Arduino's ATmega).

| Word size | Meaning | Examples |
|---|---|---|
| 4-bit | 4 data lines | Intel 4004 (1971) |
| 8-bit | 8 data lines, 16 address lines (64 KB) | 8080, **8085**, Z80, 6502 |
| 16-bit | 16 data lines, 20 address lines (1 MB) | 8086, 8088 |
| 32/64-bit | modern PCs and phones | Pentium, Core, ARM |

The **word length** is the number of bits the ALU handles at once; it is also normally the width of the data bus.

## 1.2 A microprocessor system and its buses

A microprocessor system has four blocks joined by **three buses**:

1. **CPU** — the 8085 itself.
2. **Memory** — ROM (program that must survive power-off) and RAM (data and programs being run).
3. **Input/output devices** — keyboard, display, sensors, via interface chips.
4. **Buses** — groups of wires shared by all blocks.

| Bus | Direction | Carries | 8085 width |
|---|---|---|---|
| **Address bus** | one-way, CPU → others | the location (memory cell or I/O port) being accessed | 16 lines → 2¹⁶ = 65,536 locations (64 KB) |
| **Data bus** | two-way | the data or instruction being transferred | 8 lines → one byte at a time |
| **Control bus** | mixed | timing and command signals: RD', WR', IO/M', ALE, READY… | several lines |

To read a byte: the CPU puts the address on the address bus, activates the **memory-read** control signal, the addressed device places its byte on the data bus, and the CPU latches it. A write is the same with the CPU supplying the data. The CPU is the **bus master**; memory and I/O are slaves.

## 1.3 The 8085 at a glance

The 8085 (Intel, 1976) is an **8-bit** processor in a **40-pin** package, needing a single **+5 V** supply. Features:

- 8-bit data bus; **16-bit address bus** → 64 KB of memory; separate 256 I/O ports.
- On-chip **clock generator**: a 6 MHz crystal gives an internal 3 MHz clock (the 8085A-2 runs at 5 MHz).
- **Five hardware interrupts** plus eight software interrupts (RST n).
- **Serial** input and output lines (SID, SOD).
- 74 instructions, 246 opcodes; multiplexed address/data lines to save pins.

### Functional blocks

| Block | Role |
|---|---|
| **ALU** | add, subtract, AND, OR, XOR, compare, rotate, increment, decrement; its inputs are the accumulator and a temporary register |
| **Accumulator (A)** | 8-bit register holding one operand and receiving the result |
| **Temporary register** | holds the second operand during an ALU operation; not programmer-visible |
| **Flag register** | five condition flags set by ALU results |
| **General registers** B, C, D, E, H, L | 8-bit, usable singly or as pairs BC, DE, HL |
| **W, Z** | internal temporary registers used by CALL, XCHG and similar; not programmer-visible |
| **Program counter PC** | 16-bit; address of the next instruction; incremented after each fetch |
| **Stack pointer SP** | 16-bit; address of the top of the stack in memory |
| **Instruction register and decoder** | holds the opcode just fetched and decodes it |
| **Timing and control unit** | generates all control signals in step with the clock |
| **Interrupt control**, **serial I/O control** | handle INTR/TRAP/RST lines and SID/SOD |
| **Address buffer, data/address buffer** | drive A8–A15 and the multiplexed AD0–AD7 |

### The programmer's model

```
 A  (accumulator, 8)        Flags: S Z - AC - P - CY
 B   C    ← pair BC          PC  (16)   next instruction
 D   E    ← pair DE          SP  (16)   top of stack
 H   L    ← pair HL (also acts as the memory pointer "M")
```

**M** is not a physical register: it means "the memory byte addressed by HL". `MOV A,M` copies that byte into A. Many instructions can use M in place of a register, which is how the 8085 walks through arrays.

## 1.4 The flag register

An 8-bit register of which five bits are used. After most arithmetic and logic instructions the flags describe the result.

| Flag | Bit | Set (1) when |
|---|---|---|
| **S** Sign | D7 | bit 7 of the result is 1 (negative in two's complement) |
| **Z** Zero | D6 | the result is 0 |
| **AC** Auxiliary carry | D4 | carry from bit 3 to bit 4 (used by DAA for BCD) |
| **P** Parity | D2 | the result has an **even** number of 1 bits |
| **CY** Carry | D0 | carry out of bit 7 on addition, or borrow on subtraction; also set/cleared by rotate and compare |

Bits D5, D3 and D1 are unused. Flags let programs make decisions: `JZ`, `JNC`, `JM` and the other conditional jumps test them. Note that INR and DCR change S, Z, AC, P but **not CY**, and that data-transfer instructions (MOV, MVI, LDA…) change **no** flags.

::: example Worked example: flags after addition
**9BH + 75H.** 1001 1011 + 0111 0101 = 1 0001 0000. Result = **10H**, so: CY = 1 (carry out of bit 7), Z = 0, S = 0 (bit 7 of 10H is 0), P = 0 (one 1-bit → odd), AC = 1 (low nibbles B + 5 = 10H carries).
**3EH + 42H** = 80H: S = 1, CY = 0, Z = 0, P = 0 (one 1 bit); the signed overflow (positive + positive = negative) is *not* flagged separately on the 8085 — you must notice S changing sign yourself.
**05H − 05H** = 00H: Z = 1, CY = 0 (no borrow), P = 1 (zero 1-bits is even).
**CPI 09H with A = 05H:** A − 09H would borrow, so CY = 1, Z = 0, and A stays 05H (compare does not store the result).
:::

## 1.5 Pins and signal groups

You are expected to know the groups, not memorise all 40 pin numbers.

| Group | Pins | Meaning |
|---|---|---|
| Address bus | **A8–A15** | the high-order byte of the address, output only |
| Multiplexed bus | **AD0–AD7** | low-order address byte *and* the data byte, at different times |
| **ALE** | 1 | Address Latch Enable: pulses high at the start of each machine cycle so an external latch (74LS373) can capture AD0–AD7 as A0–A7 |
| Status/control | **IO/M'**, **S0, S1**, **RD'**, **WR'** | tell whether the cycle is memory or I/O, and read or write; RD' and WR' are active low |
| Interrupts | **TRAP, RST 7.5, 6.5, 5.5, INTR, INTA'** | request lines and the acknowledge output |
| DMA | **HOLD, HLDA** | a DMA controller asks the CPU to release the buses; the CPU acknowledges |
| Wait | **READY** | a slow device pulls it low to make the CPU insert wait states |
| Reset | **RESET IN', RESET OUT** | RESET IN' low sets PC = 0000H |
| Serial | **SID, SOD** | serial input and output data |
| Clock | **X1, X2, CLK OUT** | crystal in; system clock out for peripherals |
| Power | **Vcc (+5 V), Vss (ground)** | |

::: key Why multiplex?
A 40-pin package cannot hold 16 address pins, 8 data pins and all the control pins. The 8085 therefore sends A0–A7 on AD0–AD7 first (with ALE high), then the same pins carry data. A latch holds the low address byte so that the address stays valid while the pins turn into data lines. Demultiplexing = one 74LS373 latch enabled by ALE.
:::

## 1.6 Instruction cycle, machine cycle, T-state

- **T-state**: one period of the processor clock — the smallest unit of timing. At 3 MHz, T = 1/3 µs = **0.333 µs**.
- **Machine cycle (M-cycle)**: one complete bus operation — opcode fetch, memory read, memory write, I/O read, I/O write, interrupt acknowledge — made of 3 to 6 T-states.
- **Instruction cycle**: everything needed to fetch and execute one instruction — one to five machine cycles.

```
Instruction cycle  = M1 (opcode fetch) + M2 + M3 …
Machine cycle      = T1 + T2 + T3 (+ T4 + T5 + T6)
```

### The machine cycles and their status lines

| Machine cycle | IO/M' | S1 | S0 | T-states |
|---|---|---|---|---|
| Opcode fetch | 0 | 1 | 1 | 4 (6 for a few, e.g. PUSH, CALL, RST) |
| Memory read | 0 | 1 | 0 | 3 |
| Memory write | 0 | 0 | 1 | 3 |
| I/O read (IN) | 1 | 1 | 0 | 3 |
| I/O write (OUT) | 1 | 0 | 1 | 3 |
| Interrupt acknowledge | 1 | 1 | 1 | 3 |

### Inside the opcode fetch cycle (4 T-states)

- **T1**: the CPU puts the PC on the address bus (high byte on A8–A15, low byte on AD0–AD7); **ALE = 1** so the latch captures the low byte. PC is incremented.
- **T2**: **RD'** goes low; the memory begins to respond.
- **T3**: the opcode appears on AD0–AD7 and is loaded into the instruction register; RD' goes high.
- **T4**: the opcode is decoded; the ALU works if the instruction needs no further memory access.

For a memory read or write cycle, T1 outputs the address (ALE high), T2 asserts RD' or WR', T3 completes the transfer.

### Counting machine cycles and T-states

| Instruction | Bytes | Machine cycles | T-states | Why |
|---|---|---|---|---|
| `MOV B,C` | 1 | 1 | 4 | opcode fetch only |
| `MVI B,32H` | 2 | 2 | 7 | fetch (4) + read operand (3) |
| `LXI H,2050H` | 3 | 3 | 10 | fetch + read low byte + read high byte |
| `MOV A,M` | 1 | 2 | 7 | fetch + read memory at HL |
| `ADD M` | 1 | 2 | 7 | fetch + read memory |
| `INR M` | 1 | 3 | 10 | fetch + read + write back |
| `LDA 2050H` | 3 | 4 | 13 | fetch + 2 address bytes + data read |
| `STA 2050H` | 3 | 4 | 13 | fetch + 2 address bytes + data write |
| `PUSH B` | 1 | 3 | 12 | 6-T fetch + 2 stack writes (3 + 3) |
| `CALL addr` | 3 | 5 | 18 | 6-T fetch + 2 reads + 2 stack writes |
| `OUT 80H` | 2 | 3 | 10 | fetch + read port address + I/O write |

::: example Worked example: execution time
How long does `LXI H,2050H ; MOV A,M ; INX H ; ADD M ; STA 2052H ; HLT` take on a 3 MHz 8085?
T-states: 10 + 7 + 6 + 7 + 13 + 5 = **48 T** (checked by running the sequence on the book's 8085 simulator, `tools/check_mpca.py`). Time = 48 × 0.333 µs = **16 µs**.
:::

## 1.7 Interrupts (introduction)

An **interrupt** makes the CPU pause the running program, run a service routine, and return.

| Interrupt | Type | Priority | Vector (service address) | Maskable? |
|---|---|---|---|---|
| **TRAP** | hardware, edge **and** level | 1 (highest) | 0024H | **no** |
| **RST 7.5** | hardware, edge-triggered | 2 | 003CH | yes (SIM) |
| **RST 6.5** | hardware, level | 3 | 0034H | yes |
| **RST 5.5** | hardware, level | 4 | 002CH | yes |
| **INTR** | hardware, level; device supplies an RST opcode | 5 (lowest) | 8 × n for RST n | yes (EI/DI) |

Software interrupts **RST 0–7** are one-byte instructions that call address 8 × n (RST 1 → 0008H). `EI` enables and `DI` disables the maskable interrupts; SIM sets individual masks and RIM reads the interrupt status. Unit 6 returns to interrupts in I/O organisation.

## 1.8 A first look at the 8086

The 8086 (1978) is a **16-bit** processor with a 16-bit data bus and a **20-bit address bus** (1 MB). Its main ideas:

- **Two units working in parallel**: the **Bus Interface Unit (BIU)** fetches instructions into a 6-byte queue and handles addresses; the **Execution Unit (EU)** executes. Fetching overlaps with executing — the earliest form of pipelining in the family (Unit 7).
- **Segmented memory**: a 20-bit physical address is built from a 16-bit segment register and a 16-bit offset: **physical = segment × 16 + offset**. For 2000:0150 → 20000H + 0150H = **20150H**.
- Registers: AX, BX, CX, DX (each splits into high/low bytes), SP, BP, SI, DI, four segment registers CS, DS, SS, ES, instruction pointer IP and a 16-bit flag register (adds overflow, direction, interrupt, trap, tracing flags).
- Hardware multiply and divide, string instructions, a larger instruction set.

| | 8085 | 8086 |
|---|---|---|
| Data bus | 8-bit | 16-bit |
| Address bus | 16 lines (64 KB) | 20 lines (1 MB) |
| Pipelining | none | 6-byte prefetch queue |
| Multiply/divide | none (software) | MUL, DIV instructions |
| Memory model | flat 64 KB | segmented |

## Formula and fact sheet

- Address lines n → 2ⁿ locations: 16 lines = 64 KB, 20 lines = 1 MB.
- T = 1/f; at 3 MHz T = 0.333 µs. Execution time = (total T-states) × T.
- Opcode fetch = 4 T (6 T for PUSH/CALL/RST); memory/I/O read or write = 3 T.
- Flags: S (D7), Z (D6), AC (D4), P (D2), CY (D0). MOV/MVI/LDA/STA/jumps change no flags.
- Interrupt priority: TRAP > RST 7.5 > RST 6.5 > RST 5.5 > INTR. Vectors 0024H, 003CH, 0034H, 002CH.
- 8086 physical address = segment × 16 + offset.

## Chapter summary

- A microprocessor is a CPU on a chip; a system joins CPU, memory and I/O with address, data and control buses.
- The 8085 has an accumulator, six general registers (pairs BC, DE, HL; M = byte at HL), PC, SP and five flags S, Z, AC, P, CY.
- AD0–AD7 are multiplexed; ALE and a latch separate the low address byte from the data.
- An instruction cycle consists of machine cycles (opcode fetch plus reads/writes), each of 3–6 T-states.
- Five hardware interrupts with fixed priority and eight software RSTs.
- The 8086 adds a wider bus, a prefetch queue (BIU/EU), segmentation and hardware multiply/divide.

## Practice

1. Define microprocessor, microcomputer and microcontroller.
2. Name the three buses of a microprocessor system, their direction and the 8085 width of each.
3. Why are AD0–AD7 multiplexed? Describe the role of ALE and the 74LS373.
4. List the five flags of the 8085 and say when each is set.
5. Find the flags after 7FH + 01H and after 80H + 80H.
6. Differentiate between T-state, machine cycle and instruction cycle.
7. How many T-states and machine cycles does `LDA 2050H` need? Show each cycle.
8. Compute the time taken by `MVI A,05H ; ADD B ; STA 3000H ; HLT` on a 3 MHz 8085.
9. List the 8085 interrupts in order of priority with their vector addresses.
10. Calculate the 8086 physical address for CS = 1A00H, IP = 0250H, and state two advantages of the 8086 over the 8085.

::: note Answers and worked solutions
**1.** A microprocessor is a CPU on one chip; a microcomputer is a microprocessor with memory and I/O; a microcontroller has CPU, memory and I/O on a single chip.
**2.** Address (one-way, 16 lines), data (two-way, 8 lines), control (several lines, mixed direction).
**3.** To fit in 40 pins. ALE goes high at T1, the latch captures AD0–AD7 as A0–A7, then the pins carry data while the latch keeps the address stable.
**4.** S (result negative), Z (result zero), AC (carry from bit 3), P (even parity), CY (carry/borrow).
**5.** 7FH + 01H = 80H: S = 1, Z = 0, CY = 0, AC = 1 (F + 1 carries), P = 0. 80H + 80H = 100H → result 00H: S = 0, Z = 1, CY = 1, AC = 0, P = 1.
**6.** T-state = one clock period; machine cycle = one bus operation (3–6 T); instruction cycle = all machine cycles of one instruction.
**7.** 13 T, 4 machine cycles: opcode fetch (4), memory read low address byte (3), memory read high address byte (3), memory read data (3).
**8.** 7 + 4 + 13 + 5 = 29 T × 0.333 µs = **9.67 µs**.
**9.** TRAP (0024H) > RST 7.5 (003CH) > RST 6.5 (0034H) > RST 5.5 (002CH) > INTR (8n via RST n).
**10.** 1A00H × 16 = 1A000H; + 0250H = **1A250H**. Advantages: 1 MB addressing; 16-bit data bus/prefetch queue; hardware multiply/divide.
:::
