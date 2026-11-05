---
subject: Microprocessor and Computer Architecture
grade: BCA Semester 2
unit: 6
title: Input–Output Organisation
area: BCA 152 · Microprocessor and Computer Architecture · Unit 6
---

A computer is useless if it cannot talk to the world. Devices are thousands of times slower than the CPU and speak different formats, so a computer needs **interfaces** and a strategy for transferring data. This unit covers the I/O interface, the three transfer methods (programmed, interrupt-driven, DMA), interrupt priority, and I/O processors.

::: key What this unit gives you
- The I/O bus and interface; memory-mapped versus isolated I/O.
- Asynchronous data transfer: strobe and handshaking.
- Programmed I/O, interrupt-initiated I/O, priority interrupts and the daisy chain.
- Direct memory access (DMA): controller, transfer modes, a worked timing example.
- I/O processors and serial communication protocols.
:::

## 6.1 The I/O interface

An **interface** sits between the CPU buses and a peripheral. Why it is needed: (1) peripherals are **electromechanical** with different signal levels and formats; (2) their **data rate** is much lower than the CPU's; (3) their **data formats and word lengths** differ; (4) the CPU must be able to select one among many devices.

```
        data bus    ┌────────────┐   data (device format)
 CPU ◄════════════► │  interface │ ◄════════════►  peripheral
 address bus ═════► │  (ports,   │ ◄── status / control ──►
 control bus (R/W)► │  registers)│
                    └────────────┘
```

An interface has **registers**: a **data register** (data in/out), a **status register** (ready/busy/error flags) and a **control register** (commands to the device), and a small **decoder** that recognises its own address.

### I/O bus and addressing

Two ways to give devices addresses:

| | **Isolated (I/O-mapped)** | **Memory-mapped** |
|---|---|---|
| Address space | separate; special IN/OUT instructions | shares the memory address space |
| Control line | separate I/O read/write signals | the ordinary memory read/write |
| Instructions | few (IN, OUT) | any memory instruction works on device registers |
| Memory used | none lost | some addresses lost to devices |
| Example | 8085 `IN`/`OUT`, x86 ports | ARM, MIPS, most microcontrollers |

## 6.2 Asynchronous data transfer

CPU and device have different clocks, so they must agree on *when* data is valid.

**Strobe control** — one control line from one side tells the other when the data is valid.

- *Source-initiated strobe*: the source places data on the bus, then pulses the strobe; the destination latches data on the strobe's edge. Weakness: the source cannot know whether the destination received it.
- *Destination-initiated strobe*: the destination pulses the strobe to request data; the source supplies it. Weakness: the destination cannot know the data is valid.

**Handshaking** fixes both weaknesses with **two** lines forming a request–acknowledge loop:

```
Source-initiated handshake:
  1. source puts data on the bus, then raises  DATA VALID
  2. destination accepts the data, raises       DATA ACCEPTED
  3. source drops DATA VALID, removes the data
  4. destination drops DATA ACCEPTED   → ready for the next transfer
```
Handshaking guarantees delivery whatever the relative speeds; it is used by parallel ports (Centronics) and the 8255's mode 1.

**Asynchronous serial transmission** sends characters one bit at a time with **start bit (0)**, 5–8 data bits (LSB first), an optional **parity** bit, and 1–2 **stop bits (1)**. The line idles at 1. At 9600 baud with 8N1 (one start, 8 data, no parity, one stop = 10 bits per character) the rate is 960 characters per second.

## 6.3 Modes of transfer

### 1. Programmed I/O (polling)

The CPU runs an I/O program that repeatedly **tests the device's status flag** until it is ready, then moves one word.

```
loop:  IN   status_port      ; read the status
       ANI  01H              ; ready bit?
       JZ   loop             ; not ready: keep polling (busy wait)
       IN   data_port        ; ready: read the byte
```
Simple, but the CPU is **tied up** doing nothing useful while it waits. Fine for fast devices or trivial systems.

### 2. Interrupt-initiated I/O

The CPU does other work; when the device is ready it **raises an interrupt**. The CPU finishes the current instruction, saves the PC (and flags), jumps to the **interrupt service routine (ISR)** at the vector address, transfers the data, restores the state and resumes.

| Programmed (polling) | Interrupt-driven |
|---|---|
| CPU checks the device repeatedly | device signals the CPU |
| CPU is busy-waiting | CPU free for other work |
| simple hardware | needs interrupt hardware and ISRs |
| response time depends on the polling loop | fast, but each word costs interrupt overhead |

Vectored interrupts: the device supplies the **vector address** (or an interrupt-type number) directly; **non-vectored**: the CPU jumps to a fixed address and then finds out who interrupted by polling.

### 3. Direct memory access (DMA)

For fast, bulk transfers (disk, network) even interrupts per byte are too slow. **DMA** lets a **DMA controller** move blocks directly between a device and memory without the CPU touching each word (Section 6.5).

## 6.4 Priority interrupts

With several devices, the system must decide *who is served first* and what to do if another interrupt arrives mid-service.

### Software polling
One common interrupt branches to a routine that **polls** each device's status in priority order. Simple, but the polling time makes the lowest-priority device slow.

### Daisy-chain (hardware) priority

Devices are connected in a **chain**; the interrupt-acknowledge signal enters the highest-priority device. Each device has a PI (priority-in) and PO (priority-out) line:

```
 CPU INTA ──► [Device 1] PI → PO ──► [Device 2] PI → PO ──► [Device 3] …
              (highest)                                      (lowest)
 A device that is requesting keeps PO = 0 (blocks the chain) and puts its vector on the bus;
 a device that is not requesting passes PI → PO.
```
Cheap and scalable, but the priorities are fixed by position and one failed device can break the chain.

### Parallel priority hardware
A **priority encoder** with an interrupt mask register: each device has a request line; a mask bit can disable it; the encoder outputs the vector of the highest-priority unmasked request. More flexible and faster than the daisy chain; masks allow selective disabling.

### The 8085 and the 8259
The 8085 has built-in priority (TRAP > RST 7.5 > 6.5 > 5.5 > INTR). For more devices, a programmable **8259 interrupt controller** accepts 8 request lines (cascadable to 64), prioritises them and supplies the vector to the CPU.

### Enabling, masking and nesting
Maskable interrupts can be disabled (`DI`, mask register); non-maskable ones (TRAP, power-fail) cannot. A **higher-priority** interrupt may interrupt a lower-priority ISR (nesting) provided the ISR saves state on the stack and re-enables interrupts.

## 6.5 Direct memory access

### Why DMA

Interrupt-driven transfer costs maybe 10–50 CPU cycles per word. A disk delivering 50 MB/s would swamp the CPU. With DMA the CPU sets up the transfer and is interrupted **once per block**.

### The DMA controller

Registers inside the DMA controller (e.g. Intel 8257/8237): an **address register** (memory address of the next transfer), a **word count register** (words remaining), a **control register** (direction, mode) and a status register.

### The DMA procedure

1. The CPU **programs** the DMA controller: memory start address, word count, direction (read from or write to the device), and starts it.
2. The device raises **DREQ** (DMA request) when it has data.
3. The controller asserts **HOLD** (bus request) to the CPU.
4. The CPU finishes its current *bus cycle*, releases the address, data and control buses (tri-states them), and replies **HLDA** (hold acknowledge).
5. The controller puts the memory address on the address bus and asserts the read/write strobes; the data goes **directly** between device and memory (the controller sends **DACK** to the device).
6. Address register ++, word count −−. Repeat steps 5–6 until the count is 0.
7. The controller drops HOLD; the CPU regains the bus; the controller raises an **interrupt** to say "block done".

### DMA transfer modes

| Mode | How it takes the bus | Effect |
|---|---|---|
| **Burst (block) mode** | keeps the bus for the whole block | fastest transfer; CPU stalled for the duration |
| **Cycle stealing** | takes the bus for **one cycle per word**, then returns it | CPU slowed slightly; smooth; the usual choice |
| **Transparent mode** | transfers only when the CPU is not using the bus | no CPU slowdown; slower transfer, complex hardware |

::: example Worked example: DMA versus interrupts
A device delivers 4 KB (4096 words) at 1 MB/s. In interrupt mode each word costs about 20 µs of CPU time for the ISR (save, move, restore): 4096 × 20 µs = **82 ms** of CPU time. With DMA in cycle-stealing mode, the CPU spends perhaps 20 µs to program the controller and 20 µs for the completion interrupt, and loses at most one memory cycle (say 0.5 µs) per word: 4096 × 0.5 µs = **2 ms** of bus time — a roughly 40× saving.
:::

### Memory-mapped I/O and DMA contention
When the DMA controller and the CPU both want the bus, the **bus arbiter** (or the HOLD/HLDA handshake) decides; DMA gets priority since the device cannot wait without losing data.

## 6.6 I/O processors and communication processors

An **input–output processor (IOP)** (a channel) is a processor with its **own instruction set** specialised for I/O. The CPU gives it only a high-level command ("read 50 blocks from device X into buffer Y"); the IOP fetches its own **channel program** from memory, transfers data, handles errors, formats and conversions, and interrupts the CPU when done. It extends DMA: DMA moves data, but the IOP also **decides** (control, code conversion, scatter/gather). Mainframes use channels; PCs use the chipset and bus-mastering adapters.

A **data communication processor** (front-end processor) connects a computer to a network or many terminals. It performs multiplexing, framing, error checking and protocol work, unburdening the CPU. Two classes of communication protocols are named in the syllabus:

| | **Character-oriented protocol** | **Bit-oriented protocol** |
|---|---|---|
| Unit | the **character** (control characters like SYN, STX, ETX, ACK, NAK) | a **frame** of arbitrary bits |
| Framing | special control characters mark start/end | a flag byte `01111110` marks start/end |
| Transparency | needs **character stuffing** (DLE) to send data resembling control characters | **bit stuffing**: insert a 0 after five consecutive 1s |
| Efficiency | lower, fixed alphabet | higher, any code |
| Examples | BISYNC (IBM binary synchronous) | **HDLC, SDLC**, PPP |

::: example Worked example: bit stuffing
Data `0110111111011` contains a run of six 1s. The sender inserts a 0 after every five consecutive 1s: `01101111101011` → the data becomes `01101111101011` (the inserted 0 sits after the first five 1s). The frame `01111110 · stuffed data · 01111110` can never confuse a data run with the flag. The receiver removes any 0 that follows five 1s.
:::

## Formula and fact sheet

- Asynchronous frame = 1 start + n data (+ parity) + 1–2 stop bits; chars/sec = baud ÷ bits per frame (9600/10 = 960).
- Polling wastes CPU; interrupts overlap I/O with computation; DMA bypasses the CPU for blocks.
- DMA handshake: DREQ → HOLD → HLDA → DACK; transfer; interrupt at the end.
- DMA modes: burst, cycle stealing, transparent.
- Daisy-chain: fixed priority by position (PI/PO). Parallel priority: encoder + mask register.
- 8085 interrupts: TRAP > RST 7.5 > RST 6.5 > RST 5.5 > INTR.

## Chapter summary

- An interface adapts the peripheral to the CPU through data, status and control registers; I/O is isolated or memory-mapped.
- Strobe and handshake coordinate data transfer between unsynchronised units; handshake confirms delivery.
- Programmed I/O polls; interrupt-driven I/O signals; DMA moves blocks with one interrupt at the end.
- Priority is resolved by software polling, daisy chain or a priority encoder; the 8259 extends the 8085's interrupt lines.
- IOPs run their own channel programs; communication processors offload character- and bit-oriented protocols.

## Practice

1. Why is an interface needed between the CPU and a peripheral? List the registers of a typical interface.
2. Compare memory-mapped and isolated I/O.
3. Explain source-initiated strobe and handshaking; why is handshaking better?
4. Compare programmed I/O and interrupt-driven I/O.
5. Explain the daisy-chain priority interrupt scheme with a diagram.
6. Describe the DMA transfer procedure, naming each signal.
7. Differentiate the three DMA transfer modes.
8. A serial line runs at 4800 baud with 1 start, 8 data, 1 parity and 2 stop bits. How many characters per second?
9. What is an I/O processor? How does it differ from DMA?
10. Differentiate character-oriented and bit-oriented protocols. Show bit stuffing of `0111110111111`.

::: note Answers and worked solutions
**1.** Different electrical/data formats, speed mismatch, word length differences, device selection. Registers: data, status, control.
**2.** See the table in 6.1: memory-mapped shares the address space and uses ordinary memory instructions; isolated uses a separate space and IN/OUT.
**3.** Source-initiated strobe: the source puts data on the bus then pulses a strobe. Handshaking adds an acknowledge from the destination, so each side knows the other's state — delivery is guaranteed whatever the speeds.
**4.** In programmed I/O the CPU polls the flag and is busy; in interrupt-driven I/O the device interrupts, so the CPU does useful work meanwhile.
**5.** Devices in series, PI/PO per device, nearest-to-CPU has the highest priority (diagram in 6.4).
**6.** CPU programs address/count → DREQ → HOLD → HLDA → DACK + transfers (address ++, count −−) → HOLD released → interrupt on completion.
**7.** Burst: whole block at once; cycle stealing: one word per stolen bus cycle; transparent: only when the CPU is not using the bus.
**8.** Bits per character = 1 + 8 + 1 + 2 = 12; 4800 / 12 = **400 characters per second**.
**9.** An IOP is a processor with its own I/O instruction set that runs channel programs from memory; DMA merely moves data between memory and a device, without making decisions.
**10.** Character-oriented: control characters (SYN, STX, ETX) frame data; bit-oriented: flag 01111110 frames data. Stuffing 0111110111111: the data is `0` `11111` `0` `11111` `1`. Insert a 0 after each group of five 1s → `0` `11111` `0` `0` `11111` `0` `1` = **011111001111101** (15 bits; the second group of five 1s is followed by a stuffed 0 before the final 1).
:::
