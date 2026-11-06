---
subject: Microprocessor and Computer Architecture
grade: BCA Semester 2
unit: 8
title: Pipelining, Vector Processing and Multiprocessors
area: BCA 152 · Microprocessor and Computer Architecture · Unit 8
---

Once a single processor has been made as fast as clocks and gates allow, the way to go faster is to do *many things at once*. This unit covers **parallelism** at three levels: overlapping the stages of one instruction stream (**pipelining**), applying one operation to whole arrays (**vector processing**), and using several processors (**multiprocessors**).

::: key What this unit gives you
- Flynn's classification of parallel computers (SISD, SIMD, MISD, MIMD).
- Pipeline principle, space–time diagram, speed-up and efficiency with worked numbers.
- Arithmetic pipelines (floating-point addition) and the four-segment instruction pipeline.
- Hazards: structural, data (RAW/WAR/WAW) and control; branch handling.
- Vector processing and matrix multiplication; multiprocessor structure, interconnection, cache coherence, Amdahl's law.
:::

## 8.1 Parallel processing and Flynn's classification

**Parallel processing** means carrying out several computations at the same time. Levels: instruction level (pipelining, superscalar), data level (vector/SIMD), thread/task level (multi-core, multiprocessor), and job level (clusters).

**Flynn's classification** (1966) sorts machines by the number of **instruction streams** and **data streams**:

| Class | Instruction streams | Data streams | Example |
|---|---|---|---|
| **SISD** | single | single | the classic uniprocessor (8085, a simple CPU) |
| **SIMD** | single | multiple | array/vector processors, GPUs, SSE/AVX instructions |
| **MISD** | multiple | single | rare; fault-tolerant systems (e.g. space-shuttle flight computers), systolic arrays in some views |
| **MIMD** | multiple | multiple | multiprocessors and multicomputers: multi-core CPUs, clusters |

```
SISD:  IS → [CU → PU ⇄ MM]                 SIMD:  IS → CU ⇒ PU1, PU2, … PUn  (each with own data)
MIMD:  (IS1 → CU1 → PU1), (IS2 → CU2 → PU2) … sharing memory or messages
```

## 8.2 Pipelining

### The idea

A **pipeline** splits a task into **k stages** (segments) separated by registers, so that while one task is in stage 2, the next is already in stage 1 — like a car assembly line. Each stage takes **one clock period**; once the pipeline is **full**, one result emerges **every clock**.

### Space–time diagram (4 stages, 6 tasks)

```
clock →   1   2   3   4   5   6   7   8   9
stage 1  T1  T2  T3  T4  T5  T6
stage 2      T1  T2  T3  T4  T5  T6
stage 3          T1  T2  T3  T4  T5  T6
stage 4              T1  T2  T3  T4  T5  T6
```
The first task needs k = 4 clocks; each later task finishes one clock after the previous: 6 tasks need **k + n − 1 = 4 + 6 − 1 = 9** clocks.

### Speed-up, efficiency, throughput

For n tasks, k stages, clock period t_p, and a non-pipelined time per task of **n·k·t_p** (equal stage delays):

- Pipelined time = **(k + n − 1) · t_p**.
- **Speed-up S = n·k / (k + n − 1)**; as n → ∞, **S → k**.
- **Efficiency = S / k**; **Throughput = n / ((k + n − 1) t_p)**.

::: example Worked example: speed-up numbers
A 4-stage pipeline, 100 tasks, t_p = 10 ns. Non-pipelined: 100 × 4 × 10 = 4000 ns. Pipelined: (4 + 100 − 1) × 10 = **1030 ns**. S = 400/103 = **3.88**; efficiency = 3.88/4 = **0.97**. Another: k = 5, n = 20: pipelined 24 clocks vs 100 non-pipelined; S = 100/24 = **4.17**. Few tasks give poor speed-up (n = 1 gives S = 1) because the pipeline never fills; many tasks approach k. (All verified by script.)
:::

### Why real speed-up is below k
Stages are never perfectly balanced (the slowest stage sets the clock), the pipeline needs time to fill and drain, and **hazards** stall it.

## 8.3 Arithmetic pipeline

Arithmetic pipelines split operations such as floating-point addition into stages. A **four-segment floating-point add/subtract pipeline** for X = A × 2ᵃ and Y = B × 2ᵇ:

1. **Compare exponents** (subtract them; the larger exponent is kept).
2. **Align mantissas** (shift the one with the smaller exponent right by the difference).
3. **Add or subtract mantissas.**
4. **Normalise** the result (shift mantissa, adjust exponent) and round.

Registers separate the segments, so four different additions are in flight at once. Example of what the stages do: 0.5 + 0.375 — compare exponents (−1 vs −2, difference 1); align (0.375 → 0.011 × 2⁻¹ with a mantissa shift); add (1.0 + 0.11 = 1.11); normalise (already normalised) ⇒ 1.11 × 2⁻¹ = **0.875**.

## 8.4 Instruction pipeline

An **instruction pipeline** overlaps the phases of consecutive instructions. The textbook **four-segment pipeline**:

| Segment | Abbrev | Work |
|---|---|---|
| 1 | **FI** | Fetch the instruction from memory |
| 2 | **DA** | Decode it and calculate the effective address |
| 3 | **FO** | Fetch the operand from memory |
| 4 | **EX** | Execute and store the result |

Space–time diagram for instructions I1–I4 (no conflicts):

```
clock →  1   2   3   4   5   6   7
I1      FI  DA  FO  EX
I2          FI  DA  FO  EX
I3              FI  DA  FO  EX
I4                  FI  DA  FO  EX
```
Four instructions finish in 7 clocks instead of 16. Real CPUs have 5–20 stages (the classic RISC pipeline: IF, ID, EX, MEM, WB).

## 8.5 Pipeline hazards

A **hazard** is a condition that stops the next instruction from executing in its clock cycle.

| Hazard | Cause | Remedies |
|---|---|---|
| **Structural** | two instructions need the same hardware (e.g. one memory port for fetching an instruction and an operand) | duplicate resources; split instruction/data caches (Harvard style) |
| **Data** | an instruction needs a result that an earlier instruction has not yet produced | forwarding, stalls, instruction reordering |
| **Control (branch)** | a branch changes the PC, so the instructions already fetched may be wrong | prediction, delayed branch, branch target buffer |

### Data dependency

| Kind | Meaning | Example |
|---|---|---|
| **RAW** (read after write) — *true dependency* | I2 reads what I1 writes | `ADD R1,R2,R3` then `SUB R4,R1,R5` — SUB needs the R1 produced by ADD |
| **WAR** (write after read) — *anti-dependency* | I2 writes what I1 reads | rare in in-order pipes |
| **WAW** (write after write) — *output dependency* | both write the same register | out-of-order issue |

Ways to handle RAW:

- **Hardware interlock (stall)**: detect the dependency and insert **bubbles** until the result is ready.
- **Operand forwarding (bypassing)**: route the ALU result directly to the next instruction's input, without waiting for the register write — removes most stalls.
- **Delayed load** or **compiler scheduling**: the compiler inserts an independent instruction (or a NOP) in the gap.

::: example Worked example: effect of a RAW stall
Without forwarding, in a pipeline where the result is written in segment 4 and read in segment 2, `SUB` must wait two bubbles for the preceding `ADD`: if 10 instructions have one such dependency each, 10 extra clocks are lost; forwarding reduces this to 0 or 1 per dependency (a load followed immediately by its use still needs one stall). For a pipeline with CPI_ideal = 1 and 20 % of instructions followed by a one-cycle stall: CPI = 1 + 0.2 × 1 = **1.2**, giving 83 % of the ideal throughput.
:::

### Handling branch instructions

A conditional branch is resolved late (in EX), by which time the pipeline has already fetched the next sequential instructions. Techniques:

- **Prefetch both paths** — fetch the branch target and the fall-through into separate buffers; discard one when the branch resolves.
- **Branch target buffer (BTB)** — a small cache keyed by the branch address, storing the target (and prediction).
- **Branch prediction** — *static* (always not taken; backward branches taken) or *dynamic* (a 1- or 2-bit history counter per branch; loops are predicted well, ≥ 90 % accuracy in practice).
- **Loop buffer** — a small fast buffer holding a loop's instructions.
- **Delayed branch** — the compiler fills the slot(s) after the branch with useful instructions that execute whatever the outcome.

A mispredicted branch **flushes** the pipeline; the cost grows with pipeline depth. If 20 % of instructions are branches, 60 % of them taken, and a taken branch costs 2 extra cycles: CPI = 1 + 0.2 × 0.6 × 2 = **1.24**.

## 8.6 Vector processing

Scientific problems (weather, structural analysis, graphics, ML) apply the same operation to **arrays**. A **vector processor** has instructions that operate on whole vectors, e.g. `C(1:100) = A(1:100) + B(1:100)` in **one instruction** instead of a 100-iteration loop of fetch/decode/execute.

Benefits: fewer instruction fetches and decodes, no loop-control overhead, no branch hazards inside the vector, regular memory access that is easy to interleave and prefetch, and the arithmetic units are pipelined to produce one result per clock.

- **Vector registers** hold e.g. 64 elements; a **vector length register** says how many are used; a **mask register** selects which elements participate.
- **Memory interleaving**: m memory modules with consecutive addresses in different modules supply a word per cycle.
- **Vector operations**: vector + vector, vector × scalar, reductions (sum, max), gather/scatter.

### Matrix multiplication

C = A × B for n × n matrices needs **n³ multiplications and n²(n − 1) additions** (n = 2: 8 and 4). Each element Cᵢⱼ is an inner product of row *i* of A and column *j* of B, so it maps to a pipelined *multiply–accumulate* stream; with several pipelines, rows can be computed in parallel. **Systolic arrays** compute the product by passing A and B values through a grid of processing elements in lock-step — the basis of modern deep-learning accelerators.

```
for i in 1..n:  for j in 1..n:  C[i][j] = 0
   for k in 1..n:  C[i][j] += A[i][k] * B[k][j]      ← the inner loop becomes one vector op
```

**SIMD in everyday hardware:** Intel SSE/AVX and ARM NEON apply one instruction to 4–16 packed values; a GPU runs thousands of such lanes.

## 8.7 Multiprocessors

A **multiprocessor** is a computer with two or more CPUs sharing memory (a *tightly coupled* MIMD system); a **multicomputer** (cluster) has separate memories and communicates by messages (*loosely coupled*). Motivations: **throughput** (more jobs per second), **speed** for parallel tasks, **reliability** (graceful degradation if one CPU fails), **scalability**.

| | Shared-memory multiprocessor | Distributed-memory multicomputer |
|---|---|---|
| Memory | one address space | each node has its own |
| Communication | read/write shared variables | message passing |
| Scale | tens of CPUs | thousands of nodes |
| Examples | multi-core PC, SMP server | cluster, supercomputer |

**UMA** (uniform memory access): all CPUs reach memory in equal time (SMP). **NUMA**: local memory is faster than remote memory.

### Interconnection structures

| Structure | Idea | Pros / cons |
|---|---|---|
| **Common (time-shared) bus** | all CPUs and memories on one bus | cheap, simple; the bus is the bottleneck, one transfer at a time |
| **Multiport memory** | memory has a port per CPU | high bandwidth; many wires |
| **Crossbar switch** | a switch at every CPU–memory crossing | simultaneous non-conflicting transfers; cost grows as n² |
| **Multistage network (Omega)** | log₂ n stages of 2 × 2 switches | cost n log n; some blocking |
| **Hypercube** | 2ⁿ nodes, each linked to n neighbours | scalable; used in multicomputers |

Arbitration: fixed priority, rotating (round-robin) or daisy chain decides who gets the bus.

### Cache coherence

Each CPU has a private cache, so two caches may hold **different values of the same variable**. **Coherence** protocols keep them consistent:

- **Write-invalidate**: a write invalidates all other copies (the common approach).
- **Write-update (broadcast)**: a write updates all copies.
- **Snooping**: every cache watches (snoops) the shared bus. The **MESI** protocol labels each line **Modified, Exclusive, Shared, Invalid**.
- **Directory-based**: a directory records which caches hold each block (scales better than snooping).

### Amdahl's law and the limit of parallelism

If a fraction **P** of a program can be parallelised over **N** processors: **Speed-up = 1 / ((1 − P) + P/N)**.

::: example Worked example: Amdahl's law
P = 0.9, N = 4: S = 1/(0.1 + 0.9/4) = 1/0.325 = **3.08**. As N → ∞, S → 1/(1 − P) = **10**: no number of processors can speed this program more than tenfold, because the 10 % serial part remains. (Verified by script.)
:::

### Inter-process communication and synchronisation
Shared-memory multiprocessors need **mutual exclusion** (locks built with atomic *test-and-set* instructions), **semaphores**, and **barriers**. Message-passing machines use `send`/`receive`. Ordering of memory operations is defined by a **memory consistency model**.

## 8.8 Seeing the ideas: assembly lines, parallel machines, hazards, branch prediction and Amdahl's law

Parallelism is easiest to understand from a factory floor. The plate starts with a real assembly line (a pipeline you can see), then shows the real machines that appeared when designers copied the idea in silicon: a vector supercomputer, a data-parallel machine, a many-node cluster, a multi-core die and a crossbar switch. The figures then draw the timing that the words describe. Every number in them was computed by a short Python program.

```photogrid label="8.1" cols="4" ratio="1.0" caption="Parallel machines, from the idea to the hardware. (a) A Ford assembly line (public domain): each worker does one stage and the product moves on, exactly like a pipeline; once the line is full, one finished unit leaves per beat. (b) The Cray-1 (public domain), a vector processor of 1976 with eight 64-element vector registers. (c) A Connection Machine CM-2 (CC BY-SA 2.0): 65,536 one-bit processors all executing the same instruction, a SIMD machine. (d) A Blue Gene/Q cabinet of the Fermi supercomputer at CINECA (CC BY 2.0): thousands of nodes with their own memory joined by a network, a MIMD multicomputer."
@ photo id="bca152/assembly" cap="Assembly line = pipeline"
fit 1.0
focus 0.4 0.5
call 0.5 0.1 0.3 0.45 "stage"
@ photo id="bca152/cray1" cap="Cray-1 vector computer"
fit 1.0
focus 0.5 0.5
@ photo id="bca152/cm2" cap="Connection Machine CM-2"
fit 1.0
focus 0.5 0.5
@ photo id="bca152/fermi" cap="Blue Gene/Q cabinets"
fit 1.0
focus 0.6 0.5
```

```photogrid label="8.2" cols="2" ratio="1.5" caption="Parallel hardware inside a PC and in a switch. (a) The silicon die of an Intel Core i5-2500 at 40x magnification (CC BY-SA 2.0): four identical processor cores run side by side along the top and middle, the integrated graphics unit (a SIMD engine) fills the lower-left area, and the shared L3 cache sits beside the cores. This is a multiprocessor on one chip. (b) A crossbar telephone exchange (NTT, public domain): every incoming line can be connected to any outgoing line through a grid of crosspoints, the same idea as the crossbar interconnect of Fig. 8.8."
@ photo id="bca152/i5die" cap="Four-core die with graphics"
fit 1.5
focus 0.5 0.5
call 0.28 0.9 0.4 0.3 "core"
call 0.78 0.9 0.7 0.3 "core"
@ photo id="bca152/crossbar" cap="Crossbar exchange"
fit 1.5
focus 0.5 0.5
```

```svgfig label="8.1" caption="Flynn's four classes drawn as block diagrams. CU is a control unit, PU a processing unit, MM memory; IS is an instruction stream and DS a data stream. SISD: one CU drives one PU. SIMD: one CU broadcasts the same instruction to many PUs, each on its own data. MISD: several CUs act on one data stream passed along a chain (rare). MIMD: several independent CU-PU pairs, each with its own instructions and data."
f = Fig(580, 232)
def panel(x, title, fl, st):
    f.box(x, 4, 134, 24, title, fill=fl, stroke=st, size=11, bold=True, r=3)
panel(4, "SISD", SAND, AMBER)
panel(148, "SIMD", MINT, TEAL)
panel(292, "MISD", BLUE, NAVY)
panel(436, "MIMD", ROSE, RED)
# SISD
f.box(40, 44, 60, 28, "CU", fill=SAND, stroke=AMBER, size=10, bold=True, r=3)
f.box(40, 100, 60, 28, "PU", fill=BLUE, stroke=NAVY, size=10, bold=True, r=3)
f.box(40, 156, 60, 28, "MM", fill=MINT, stroke=TEAL, size=10, bold=True, r=3)
f.arrow([(70, 72), (70, 100)], color=AMBER)
f.arrow([(70, 128), (70, 156)], color=TEAL, both=True)
f.text(104, 88, "IS", size=9.5, color=AMBER, bold=True, anchor="start")
f.text(104, 142, "DS", size=9.5, color=TEAL, bold=True, anchor="start")
# SIMD
f.box(176, 44, 80, 28, "CU", fill=SAND, stroke=AMBER, size=10, bold=True, r=3)
for i in range(3):
    x = 152 + i * 44
    f.box(x, 100, 38, 28, "PU", fill=BLUE, stroke=NAVY, size=9.5, bold=True, r=3)
    f.box(x, 156, 38, 28, "MM", fill=MINT, stroke=TEAL, size=9.5, bold=True, r=3)
    f.arrow([(216, 72), (216, 86), (x + 19, 86), (x + 19, 100)], color=AMBER, sw=1.2)
    f.arrow([(x + 19, 128), (x + 19, 156)], color=TEAL, sw=1.2, both=True)
# MISD
f.box(300, 44, 56, 28, "CU1", fill=SAND, stroke=AMBER, size=10, bold=True, r=3)
f.box(366, 44, 56, 28, "CU2", fill=SAND, stroke=AMBER, size=10, bold=True, r=3)
f.box(300, 100, 56, 28, "PU1", fill=BLUE, stroke=NAVY, size=10, bold=True, r=3)
f.box(366, 100, 56, 28, "PU2", fill=BLUE, stroke=NAVY, size=10, bold=True, r=3)
f.box(320, 156, 82, 28, "MM", fill=MINT, stroke=TEAL, size=10, bold=True, r=3)
f.arrow([(328, 72), (328, 100)], color=AMBER)
f.arrow([(394, 72), (394, 100)], color=AMBER)
f.arrow([(356, 114), (366, 114)], color=TEAL)
f.arrow([(328, 128), (328, 142), (361, 142), (361, 156)], color=TEAL, sw=1.2)
# MIMD
for i in range(2):
    x = 448 + i * 66
    f.box(x, 44, 56, 28, "CU" + str(i + 1), fill=SAND, stroke=AMBER, size=10, bold=True, r=3)
    f.box(x, 100, 56, 28, "PU" + str(i + 1), fill=BLUE, stroke=NAVY, size=10, bold=True, r=3)
    f.arrow([(x + 28, 72), (x + 28, 100)], color=AMBER)
    f.arrow([(x + 28, 128), (x + 28, 142), (x + 28 if i == 0 else x + 28, 156)], color=TEAL, sw=1.2, both=True)
f.box(444, 156, 126, 28, "shared MM", fill=MINT, stroke=TEAL, size=10, bold=True, r=3)
for x, t in ((4, "one stream, one datum"), (148, "one stream, many data"), (292, "many streams, one datum"), (436, "many streams, many data")):
    f.text(x + 67, 204, t, size=9, color=SLATE, bold=True)
f.text(4, 224, "Examples: 8085 | GPU, AVX | flight computers | multi-core PC, cluster", size=9.5, color=SLATE, bold=True, anchor="start")
```

```svgfig label="8.2" caption="Space-time diagram of a four-stage pipeline processing six tasks. Each coloured cell is one task in one stage for one clock. Task T1 needs 4 clocks; each later task finishes one clock after the one before, so all six finish at clock 4 + 6 - 1 = 9. Without a pipeline the six tasks would take 6 x 4 = 24 clocks, a speed-up of 24 / 9 = 2.67. The empty triangles at the start and end are the fill and drain time."
f = Fig(580, 214)
cols = [BLUE, MINT, SAND, ROSE, BLUE, MINT]
sts = [NAVY, TEAL, AMBER, RED, NAVY, TEAL]
x0, w = 66, 36
f.text(8, 18, "clock", size=10, color=SLATE, bold=True, anchor="start")
for c in range(9):
    f.text(x0 + c * w + w / 2, 18, str(c + 1), size=10, color=SLATE, bold=True)
for s in range(4):
    y = 30 + s * 34
    f.text(8, y + 15, "stage " + str(s + 1), size=10, color=NAVY, bold=True, anchor="start", vmid=True)
    for t in range(6):
        c = s + t
        f.box(x0 + c * w + 1, y, w - 2, 30, "T" + str(t + 1), fill=cols[t], stroke=sts[t], size=10, bold=True, r=3)
f.line(x0 + 3 * w, 24, x0 + 3 * w, 170, color=AMBER, sw=1, dash=True)
f.line(x0 + 6 * w, 24, x0 + 6 * w, 170, color=AMBER, sw=1, dash=True)
f.text(x0 + 1.5 * w, 184, "fill", size=9.5, color=AMBER, bold=True)
f.text(x0 + 4.5 * w, 184, "full: 1 result per clock", size=9.5, color=AMBER, bold=True)
f.text(x0 + 7.5 * w, 184, "drain", size=9.5, color=AMBER, bold=True)
f.text(x0 + 4.5 * w, 204, "6 tasks: 9 clocks (k + n - 1) against 24 without a pipeline", size=10, color=NAVY, bold=True)
```

```svgfig label="8.3" caption="Speed-up of a four-stage pipeline grows with the number of tasks n but never reaches k = 4. S = n k / (k + n - 1): n = 1 gives 1.00, n = 2 gives 1.60, n = 4 gives 2.29, n = 8 gives 2.91, n = 16 gives 3.37 and n = 100 gives 3.88 (efficiency 0.97). A single task gets no benefit because the pipeline never fills."
f = Fig(580, 214)
base = 170
k = 4
ns = [1, 2, 4, 8, 16, 100]
for i, n in enumerate(ns):
    s = n * k / (k + n - 1)
    h = s * 36
    x = 50 + i * 82
    f.box(x, base - h, 56, h, "%.2f" % s, fill=MINT if n >= 16 else SAND, stroke=TEAL if n >= 16 else AMBER, size=11, bold=True, r=2)
    f.text(x + 28, base + 14, "n = " + str(n), size=10, color=NAVY, bold=True)
    f.text(x + 28, base + 28, "E = %.2f" % (s / k), size=9.5, color=SLATE, bold=True)
f.line(36, base - 4 * 36, 556, base - 4 * 36, color=RED, sw=1.4, dash=True)
f.text(36, base - 4 * 36 - 8, "limit S = k = 4", size=10, color=RED, bold=True, anchor="start")
f.line(36, base, 556, base, color=SLATE, sw=1.2)
```

```svgfig label="8.4" caption="The four-segment floating-point adder, tracing 0.5 + 0.375 = 0.875. The numbers are X = 1.0 x 2^-1 and Y = 1.1 x 2^-2 (binary mantissas). Segment 1 subtracts the exponents (difference 1). Segment 2 shifts the mantissa of Y one place right, giving 0.11 x 2^-1. Segment 3 adds the mantissas, 1.0 + 0.11 = 1.11. Segment 4 normalises: the result is already in the form 1.xx, so it stays 1.11 x 2^-1 = 1.75 x 0.5 = 0.875."
f = Fig(580, 200)
f.box(8, 4, 200, 26, "X = 0.5 = 1.0 x 2^-1", fill=SAND, stroke=AMBER, size=10, bold=True, r=3)
f.box(220, 4, 210, 26, "Y = 0.375 = 1.1 x 2^-2", fill=SAND, stroke=AMBER, size=10, bold=True, r=3)
steps = [("1  Compare\nexponents", "-1 and -2\ndifference = 1", BLUE, NAVY), ("2  Align\nmantissas", "1.1 x 2^-2\n= 0.11 x 2^-1", MINT, TEAL), ("3  Add\nmantissas", "1.0 + 0.11\n= 1.11", SAND, AMBER), ("4  Normalise\nand round", "1.11 x 2^-1\nno shift needed", ROSE, RED)]
for i, (t, d, fl, st) in enumerate(steps):
    x = 8 + i * 144
    f.box(x, 54, 128, 44, t, fill=fl, stroke=st, size=10.5, bold=True, r=4)
    f.box(x, 110, 128, 44, d, fill="#ffffff", stroke=st, size=10, bold=True, r=4, color=SLATE)
    if i < 3:
        f.arrow([(x + 128, 76), (x + 144, 76)], color=SLATE)
        f.box(x + 128, 62, 6, 28, "", fill=NAVY, stroke=NAVY, r=0)
f.arrow([(108, 30), (108, 54)], color=AMBER)
f.arrow([(325, 30), (325, 42), (140, 42), (140, 54)], color=AMBER, sw=1.2)
f.text(8, 176, "Result = 1.11 x 2^-1 = 0.875. Dark bars are the pipeline registers between segments.", size=10, color=NAVY, bold=True, anchor="start")
f.text(8, 192, "Four different additions can be in the four segments at the same moment.", size=10, color=SLATE, bold=True, anchor="start")
```

```svgfig label="8.5" caption="A read-after-write (RAW) hazard in a five-stage pipeline (IF, ID, EX, MEM, WB). Case A, no forwarding: SUB needs R1 from ADD, which is only written in cycle 5, so SUB waits two cycles (shaded) and finishes in cycle 8. Case B, with forwarding: the ALU result of ADD, ready at the end of cycle 3, is sent straight to the ALU input of SUB in cycle 4: no stall, SUB ends in cycle 6. Case C, load followed at once by its use: even with forwarding one stall is unavoidable because the data arrive only after MEM."
f = Fig(580, 262)
x0, w = 150, 52
names = ["IF", "ID", "EX", "MEM", "WB"]
def row(y, label, start, pre=0, mid=0):
    f.text(8, y + 10, label, size=9.5, color=NAVY, bold=True, anchor="start", vmid=True)
    c = start
    for i, n in enumerate(names):
        k = pre if i == 1 else (mid if i == 2 else 0)
        for s in range(k):
            f.box(x0 + (c - 1) * w + 1, y, w - 2, 20, "stall", fill=ROSE, stroke=RED, size=9, bold=True, r=2)
            c += 1
        f.box(x0 + (c - 1) * w + 1, y, w - 2, 20, n, fill=MINT if n != "EX" else SAND, stroke=TEAL if n != "EX" else AMBER, size=10, bold=True, r=2)
        c += 1
for c in range(8):
    f.text(x0 + c * w + w / 2, 10, str(c + 1), size=9.5, color=SLATE, bold=True)
f.text(8, 10, "cycle", size=9.5, color=SLATE, bold=True, anchor="start")
f.text(8, 38, "A  no forwarding", size=10, color=RED, bold=True, anchor="start")
row(46, "ADD R1,R2,R3", 1)
row(70, "SUB R4,R1,R5", 2, pre=2)
f.text(8, 108, "B  with forwarding", size=10, color=TEAL, bold=True, anchor="start")
row(116, "ADD R1,R2,R3", 1)
row(140, "SUB R4,R1,R5", 2)
f.arrow([(x0 + 2 * w + 26, 136), (x0 + 3 * w + 26, 140)], color=AMBER, sw=1.6)
f.text(8, 178, "C  load then use", size=10, color=AMBER, bold=True, anchor="start")
row(186, "LW  R1,0(R2)", 1)
row(210, "ADD R4,R1,R5", 2, mid=1)
f.text(8, 252, "A: SUB ends in cycle 8.   B: cycle 6.   C: one stall even with forwarding.", size=9.5, color=SLATE, bold=True, anchor="start")
```

```svgfig label="8.6" caption="Branches cost cycles. Top: cycles per instruction (CPI) for a program with 20 percent branches and a 2-cycle penalty for a wrong guess. Stalling on every branch gives 1 + 0.2 x 2 = 1.40. Predict not-taken with 60 percent of branches taken gives 1 + 0.2 x 0.6 x 2 = 1.24. A one-bit predictor that is right 80 percent of the time gives 1.08, and a two-bit predictor right 90 percent of the time gives 1.04. Bottom: the two-bit saturating counter; T moves right, N moves left, and two wrong guesses in a row are needed to change the prediction."
f = Fig(580, 268)
bars = [("stall every branch", 1.40, ROSE, RED), ("predict not taken", 1.24, SAND, AMBER), ("1-bit, 80% right", 1.08, MINT, TEAL), ("2-bit, 90% right", 1.04, MINT, TEAL), ("ideal", 1.00, BLUE, NAVY)]
for i, (n, v, fl, st) in enumerate(bars):
    y = 6 + i * 26
    f.text(8, y + 10, n, size=10, color=NAVY, bold=True, anchor="start", vmid=True)
    f.box(150, y, v * 250, 20, "", fill=fl, stroke=st, r=2)
    f.text(150 + v * 250 + 6, y + 10, "CPI %.2f" % v, size=10, color=st, bold=True, anchor="start", vmid=True)
labs = ["00", "01", "10", "11"]
nm = ["strongly\nnot taken", "weakly\nnot taken", "weakly\ntaken", "strongly\ntaken"]
for i in range(4):
    x = 90 + i * 130
    hi = i >= 2
    f.circle(x, 196, 18, fill=MINT if hi else SAND, stroke=TEAL if hi else AMBER, label=labs[i], size=11, color=TEAL if hi else AMBER)
    f.text(x, 232, nm[i].split("\n")[0], size=9, color=SLATE, bold=True)
    f.text(x, 244, nm[i].split("\n")[1], size=9, color=SLATE, bold=True)
    if i < 3:
        f.arrow([(x + 18, 188), (x + 112, 188)], color=TEAL, sw=1.3)
        f.arrow([(x + 112, 204), (x + 18, 204)], color=AMBER, sw=1.3)
f.text(155, 178, "T", size=10, color=TEAL, bold=True)
f.text(155, 222, "N", size=10, color=AMBER, bold=True)
f.text(8, 150, "predict NOT taken", size=9.5, color=AMBER, bold=True, anchor="start")
f.text(300, 150, "predict TAKEN", size=9.5, color=TEAL, bold=True, anchor="start")
f.text(8, 264, "Loop of 10 (taken 9 times, then exits): 1-bit counter misses 2 per loop, 2-bit counter misses 1.", size=9.5, color=NAVY, bold=True, anchor="start")
```

```svgfig label="8.7" caption="Top: adding two vectors of 64 numbers. A scalar machine that finishes each addition before starting the next needs 64 x 6 = 384 clocks for a six-stage adder; a vector instruction streams the 64 pairs through the same pipeline and finishes in 6 + 63 = 69 clocks, a speed-up of 5.6. Bottom: matrix multiplication as a stream of inner products. For two 2 x 2 matrices each result element needs two multiplications and one addition, so 8 multiplications and 4 additions in all (n^3 and n^2 (n - 1))."
f = Fig(580, 262)
f.text(8, 14, "scalar loop", size=10, color=NAVY, bold=True, anchor="start")
f.box(110, 4, 384 * 0.9, 20, "384 clocks", fill=ROSE, stroke=RED, size=10, bold=True, r=2)
f.text(8, 44, "vector add", size=10, color=NAVY, bold=True, anchor="start")
f.box(110, 34, 69 * 0.9, 20, "69", fill=MINT, stroke=TEAL, size=10, bold=True, r=2)
f.text(110 + 69 * 0.9 + 8, 44, "speed-up 384 / 69 = 5.6", size=10, color=TEAL, bold=True, anchor="start", vmid=True)
def mat(x, y, vals, fl, st, hl=None):
    for r in range(2):
        for c in range(2):
            h = hl is not None and (r, c) in hl
            f.box(x + c * 34, y + r * 30, 32, 28, str(vals[r][c]), fill=SAND if h else fl, stroke=AMBER if h else st, size=11, bold=True, r=3)
mat(24, 100, [[1, 2], [3, 4]], BLUE, NAVY, [(0, 0), (0, 1)])
f.text(100, 134, "x", size=16, color=SLATE, bold=True)
mat(120, 100, [[5, 6], [7, 8]], BLUE, NAVY, [(0, 0), (1, 0)])
f.text(196, 134, "=", size=16, color=SLATE, bold=True)
mat(216, 100, [[19, 22], [43, 50]], MINT, TEAL, [(0, 0)])
f.text(24, 84, "A (row 1 shaded)", size=9.5, color=SLATE, bold=True, anchor="start")
f.text(120, 84, "B (column 1)", size=9.5, color=SLATE, bold=True, anchor="start")
f.text(216, 84, "C = A x B", size=9.5, color=SLATE, bold=True, anchor="start")
f.text(300, 106, "C11 = 1 x 5 + 2 x 7 = 19", size=10, color=NAVY, bold=True, anchor="start")
f.text(300, 124, "C12 = 1 x 6 + 2 x 8 = 22", size=10, color=NAVY, bold=True, anchor="start")
f.text(300, 142, "C21 = 3 x 5 + 4 x 7 = 43", size=10, color=NAVY, bold=True, anchor="start")
f.text(300, 160, "C22 = 3 x 6 + 4 x 8 = 50", size=10, color=NAVY, bold=True, anchor="start")
f.box(24, 188, 290, 28, "n = 2: 8 multiplications, 4 additions", fill=SAND, stroke=AMBER, size=10.5, bold=True, r=3)
f.box(24, 224, 290, 28, "n = 3: 27 multiplications, 18 additions", fill=SAND, stroke=AMBER, size=10.5, bold=True, r=3)
f.text(330, 206, "each C element = one multiply-add stream", size=9.5, color=SLATE, bold=True, anchor="start")
f.text(330, 242, "= one vector instruction on a row and a column", size=9.5, color=SLATE, bold=True, anchor="start")
```

```svgfig label="8.8" caption="Left: a 4 x 4 crossbar. Four processors P0 to P3 are on the rows and four memory modules M0 to M3 are on the columns; a dot is a closed crosspoint. All four transfers (P0-M2, P1-M0, P2-M3, P3-M1) go on at the same time because no two share a row or a column. A single bus could carry only one. Right: the cost of connecting n processors to n memories. A crossbar needs n x n crosspoints, an Omega network only (n / 2) log2 n two-by-two switches."
f = Fig(580, 214)
f.text(8, 14, "4 x 4 crossbar", size=10, color=NAVY, bold=True, anchor="start")
conn = {0: 2, 1: 0, 2: 3, 3: 1}
for c in range(4):
    f.text(66 + c * 44, 30, "M" + str(c), size=10, color=TEAL, bold=True)
    f.line(66 + c * 44, 38, 66 + c * 44, 186, color="#94a3b8", sw=1.4)
for r in range(4):
    y = 62 + r * 38
    f.text(10, y, "P" + str(r), size=10, color=AMBER, bold=True, anchor="start", vmid=True)
    f.line(34, y, 214, y, color="#94a3b8", sw=1.4)
    f.circle(66 + conn[r] * 44, y, 6, fill=TEAL, stroke=TEAL)
f.text(124, 206, "4 transfers at once", size=9.5, color=TEAL, bold=True)
f.text(260, 14, "n processors and n memories", size=10, color=NAVY, bold=True, anchor="start")
hd = ["n", "bus", "crossbar", "Omega"]
xs = [260, 300, 360, 450]
ws = [40, 60, 90, 100]
for h, x, w in zip(hd, xs, ws):
    f.box(x, 24, w - 2, 24, h, fill=NAVY, stroke=NAVY, color="#ffffff", size=10, bold=True, r=2)
data = [(4, 16, 4), (8, 64, 12), (16, 256, 32), (64, 4096, 192)]
for i, (n, cb, om) in enumerate(data):
    y = 52 + i * 30
    vals = [str(n), "1 path", "{:,}".format(cb), str(om) + " switches"]
    fills = [BLUE, SAND, ROSE if cb > 1000 else SAND, MINT]
    strokes = [NAVY, AMBER, RED if cb > 1000 else AMBER, TEAL]
    for v, x, w, fl, st in zip(vals, xs, ws, fills, strokes):
        f.box(x, y, w - 2, 26, v, fill=fl, stroke=st, size=10, bold=True, r=2)
f.text(260, 190, "crossbar: n x n crosspoints", size=9.5, color=SLATE, bold=True, anchor="start")
f.text(260, 206, "Omega: (n / 2) x log2 n switches, some blocking", size=9.5, color=SLATE, bold=True, anchor="start")
```

```svgfig label="8.9" caption="A 3-cube (hypercube): 8 nodes labelled 000 to 111, each linked to the 3 nodes whose label differs in one bit, 12 links in all. A message from 000 to 111 needs 3 hops (the highlighted path flips one bit per hop: 000, 001, 011, 111). The diameter of an n-cube is n, so 2^n nodes are reached in only n hops, and each node needs only n links."
f = Fig(580, 214)
def pos(b):
    b2, b1, b0 = (b >> 2) & 1, (b >> 1) & 1, b & 1
    return (40 + b0 * 120 + b2 * 70, 176 - b1 * 100 - b2 * 46)
path = [0, 1, 3, 7]
pe = set()
for a, b in zip(path, path[1:]):
    pe.add((min(a, b), max(a, b)))
for a in range(8):
    for bit in (1, 2, 4):
        b = a ^ bit
        if a < b:
            x1, y1 = pos(a)
            x2, y2 = pos(b)
            on = (a, b) in pe
            f.line(x1, y1, x2, y2, color=AMBER if on else "#94a3b8", sw=3.2 if on else 1.6)
for a in range(8):
    x, y = pos(a)
    on = a in path
    f.circle(x, y, 17, fill=SAND if on else BLUE, stroke=AMBER if on else NAVY, label=format(a, "03b"), size=9.5, color=AMBER if on else NAVY)
f.box(330, 30, 240, 28, "8 nodes, 3 links per node, 12 links", fill=BLUE, stroke=NAVY, size=10.5, bold=True, r=3)
f.box(330, 70, 240, 28, "diameter 3: any node in at most 3 hops", fill=MINT, stroke=TEAL, size=10.5, bold=True, r=3)
f.box(330, 110, 240, 28, "route 000 to 111: flip one bit per hop", fill=SAND, stroke=AMBER, size=10.5, bold=True, r=3)
f.box(330, 150, 240, 28, "n = 6: 64 nodes, still only 6 hops", fill=BLUE, stroke=NAVY, size=10.5, bold=True, r=3)
```

```svgfig label="8.10" caption="Cache coherence with the MESI states for one variable X (value 5 in memory) shared by two processors. Step 1: A reads X and holds it Exclusive. Step 2: B reads it too and both copies become Shared. Step 3: A writes 7; the write-invalidate rule marks B's copy Invalid and A's line Modified, while memory still holds the stale 5. Step 4: B reads X again; A supplies the 7 and writes it back, and both copies end up Shared with memory updated."
f = Fig(580, 224)
heads = ["step and event", "cache A", "cache B", "memory X"]
xs = [8, 224, 324, 424]
ws = [214, 98, 98, 146]
for h, x, w in zip(heads, xs, ws):
    f.box(x, 4, w, 24, h, fill=NAVY, stroke=NAVY, color="#ffffff", size=10, bold=True, r=2)
col = {"M": (ROSE, RED), "E": (SAND, AMBER), "S": (MINT, TEAL), "I": (BLUE, NAVY)}
rows = [("0  start", "I", "I", "5"), ("1  A reads X", "E  X = 5", "I", "5"), ("2  B reads X", "S  X = 5", "S  X = 5", "5"), ("3  A writes X = 7", "M  X = 7", "I  (invalidated)", "5  (stale)"), ("4  B reads X", "S  X = 7", "S  X = 7", "7  (written back)")]
for i, (ev, a, b, m) in enumerate(rows):
    y = 34 + i * 34
    f.box(xs[0], y, ws[0], 30, ev, fill="#ffffff", stroke="#cbd5e1", size=10, bold=True, r=2, color=NAVY)
    for v, x, w in zip((a, b), xs[1:3], ws[1:3]):
        fl, st = col[v[0]]
        f.box(x, y, w, 30, v, fill=fl, stroke=st, size=9.5, bold=True, r=2)
    f.box(xs[3], y, ws[3], 30, m, fill="#ffffff", stroke=RED if "stale" in m else "#cbd5e1", size=10, bold=True, r=2, color=RED if "stale" in m else NAVY)
f.text(8, 214, "M modified, E exclusive, S shared, I invalid.", size=9.5, color=SLATE, bold=True, anchor="start")
```

```svgfig label="8.11" caption="Amdahl's law for three programs: the parallel fraction P is 0.5, 0.9 and 0.99. Speed-up = 1 / ((1 - P) + P / N). For P = 0.9: 1.82 on 2 processors, 3.08 on 4, 4.71 on 8, 6.40 on 16 and 8.77 on 64, and never more than 10. The serial part sets the ceiling: 1 / (1 - P) = 2, 10 and 100."
f = Fig(580, 232)
x0, x1, y0, y1 = 56, 500, 196, 18
ns = [1, 2, 4, 8, 16, 32, 64]
def X(i): return x0 + i * (x1 - x0) / 6
def Y(s): return y0 - s * (y0 - y1) / 40.0
for s in (10, 20, 30, 40):
    f.line(x0, Y(s), x1, Y(s), color="#e2e8f0", sw=1)
    f.text(x0 - 6, Y(s), str(s), size=9.5, color=SLATE, bold=True, anchor="end", vmid=True)
for i, n in enumerate(ns):
    f.text(X(i), y0 + 14, str(n), size=9.5, color=SLATE, bold=True)
f.text(x0 + (x1 - x0) / 2, y0 + 28, "number of processors N", size=9.5, color=SLATE, bold=True)
f.line(x0, y0, x1, y0, color=SLATE, sw=1.4)
f.line(x0, y0, x0, y1, color=SLATE, sw=1.4)
for P, col, lab in ((0.5, AMBER, "P = 0.5"), (0.9, TEAL, "P = 0.9"), (0.99, RED, "P = 0.99")):
    pts = [(X(i), Y(1 / ((1 - P) + P / n))) for i, n in enumerate(ns)]
    for (a, b), (c, d) in zip(pts, pts[1:]):
        f.line(a, b, c, d, color=col, sw=2.4)
    for (a, b) in pts:
        f.circle(a, b, 3, fill=col, stroke=col)
    f.text(x1 + 8, pts[-1][1], lab, size=10, color=col, bold=True, anchor="start", vmid=True)
f.text(x0 - 6, y1 - 6, "speed-up", size=9.5, color=SLATE, bold=True, anchor="start")
```

### 8.8.1 Eight uses of pipelining, vector and parallel processing in Nepal

1. **Every phone and laptop processor is pipelined.** The ARM cores in phones sold in New Road and the Intel or AMD chips in student laptops all overlap fetch, decode, execute and write-back. This is why a processor with a 2 GHz clock can finish close to two billion simple instructions each second. A pipeline is the main reason a cheap phone feels fast.
2. **Branch prediction in everyday programs.** Loops in a Python or Java program written in a TU lab end with a branch that is taken many times and then not taken. The two-bit predictor of Fig. 8.6 guesses this almost always right. Without it the pipeline would waste cycles on every loop and the same program would run noticeably slower.
3. **GPUs and SIMD instructions for video and games.** Decoding a YouTube video, playing an online game or applying a filter in a photo app runs the same operation on thousands of pixels. A GPU or an AVX or NEON instruction does this in lock-step. This is the SIMD class of Flynn's classification, and it is why a small graphics chip can beat a big CPU on pictures.
4. **Multi-core PCs and servers.** A quad-core PC in a college lab can run a browser, an IDE and a video call at the same time, each on its own core. A web server for a school or a university results portal handles many students at once in the same way. This is a MIMD multiprocessor on one chip, as in Plate 8.2.
5. **Weather and flood modelling.** Forecast models, such as those used by the Department of Hydrology and Meteorology and international partners for the Koshi and Narayani basins, divide the land into a grid and apply the same equations to every cell. This vector-style work runs well on clusters and supercomputers. More processors give a faster forecast, up to the limit of Amdahl's law.
6. **Cloud servers behind payments and e-government.** Services such as ConnectIPS, Fonepay and the Nagarik App run on cloud or data-centre servers with many cores. Thousands of users can be served at once because each request runs on a separate core or thread. The cores share memory, so cache coherence (Fig. 8.10) keeps their copies of the data consistent.
7. **Matrix work in AI and image processing.** Face matching for the e-passport, driving-licence or national ID systems, and the machine-learning models taught in BCA, spend most of their time multiplying matrices. This is the vector and systolic-array style of Fig. 8.7. Specialised hardware, such as a GPU, does this work many times faster than a plain CPU loop.
8. **Telecom and network equipment.** The routers and switches in Nepal Telecom, Ncell and ISP networks use multi-core network processors and crossbar-style switching fabrics. Each packet is handled on its own core while others are being forwarded. This lets one box carry the traffic of thousands of customers at the same time.

## Formula and fact sheet

- Flynn: SISD, SIMD, MISD, MIMD.
- Pipeline time = (k + n − 1) t_p; speed-up S = n k /(k + n − 1) → k; efficiency = S/k.
- Four-segment instruction pipeline: FI, DA, FO, EX. Hazards: structural, data (RAW/WAR/WAW), control.
- Branch CPI = 1 + (branch fraction) × (taken fraction) × (penalty).
- Matrix multiplication n × n: n³ multiplications, n²(n − 1) additions.
- Amdahl: S = 1/((1 − P) + P/N); limit 1/(1 − P).

## Chapter summary

- Flynn classifies computers by instruction and data streams; modern machines are mostly MIMD with SIMD units.
- A k-stage pipeline gives up to k-fold speed-up, reduced by fill time, unbalanced stages and hazards.
- Arithmetic pipelines segment operations like floating-point add; the four-segment instruction pipeline overlaps FI, DA, FO and EX.
- Structural, data and control hazards are handled by resources, forwarding/interlocks and branch prediction.
- Vector processors apply one operation to arrays, removing loop overhead; matrix multiplication is the model workload.
- Multiprocessors share memory over a bus, crossbar or network; caches need coherence protocols; Amdahl's law bounds the gain.

## Practice

1. Explain Flynn's classification with examples of each class.
2. A 5-stage pipeline processes 20 tasks at 5 ns per stage. Find the time, speed-up and efficiency.
3. Draw the space–time diagram of a four-segment instruction pipeline for 5 instructions and count the clocks.
4. Explain the four-segment floating-point pipeline and trace 0.5 + 0.375.
5. Describe structural, data and control hazards and how each is handled.
6. Explain operand forwarding with an example.
7. List four techniques for handling branch instructions.
8. What is vector processing? How many multiplications and additions does a 3 × 3 matrix product need?
9. Compare common bus, crossbar and multistage network interconnections.
10. What is cache coherence? Compute Amdahl speed-up for P = 0.8, N = 8.

::: note Answers and worked solutions
**1.** SISD — one CPU on one stream (8085); SIMD — one instruction on many data (GPU, AVX); MISD — many instructions on one data stream (rare, fault-tolerant); MIMD — independent CPUs (multi-core, cluster).
**2.** Pipelined: (5 + 20 − 1) × 5 = **120 ns**; non-pipelined: 20 × 5 × 5 = 500 ns; S = 500/120 = **4.17**; efficiency = 4.17/5 = **0.83**.
**3.** I1..I5 in a four-stage pipeline finish at clock 4 + 5 − 1 = **8** (each instruction starts one clock after the previous one).
**4.** Stages: compare exponents → align mantissas → add/subtract mantissas → normalise. 0.5 = 1.0 × 2⁻¹, 0.375 = 1.1 × 2⁻²; difference 1 → shift 0.375's mantissa right → 0.11 × 2⁻¹; add 1.0 + 0.11 = 1.11 × 2⁻¹ = 0.875.
**5.** Structural — resource conflict (add resources, separate caches); data — dependency on a pending result (forwarding, interlock, scheduling); control — a branch changes the PC (prediction, delayed branch, BTB).
**6.** Instead of waiting for `ADD R1,R2,R3` to write R1, the ALU output is fed straight back to the ALU input of the next instruction `SUB R4,R1,R5`, saving the stall cycles.
**7.** Prefetch both paths, branch target buffer, branch prediction, loop buffer, delayed branch.
**8.** One instruction operates on whole arrays (e.g. adds two 100-element vectors). 3 × 3: n³ = 27 multiplications and n²(n − 1) = 9 × 2 = 18 additions.
**9.** Bus: cheapest, one transfer at a time; crossbar: many simultaneous transfers, n² switches; multistage: n log n switches, some blocking.
**10.** Coherence = keeping the copies of a shared variable in different caches consistent (write-invalidate, snooping/MESI, directory). Amdahl: S = 1/(0.2 + 0.8/8) = 1/0.3 = **3.33**.
:::

## Model answers for Unit 8

**Q1. Explain Flynn's classification of parallel computers with a block diagram and an example of each class. (5 marks)**

Michael Flynn classified computers in 1966 by the number of **instruction streams** (IS) and **data streams** (DS) that they handle at the same time. An instruction stream is the sequence of instructions executed by a control unit (CU); a data stream is the sequence of operands handled by a processing unit (PU). Fig. 8.1 draws the four classes.

| Class | Instruction streams | Data streams | Example |
|---|---|---|---|
| **SISD** | one | one | classic uniprocessor such as the 8085 |
| **SIMD** | one | many | vector processor, GPU, AVX or NEON instructions, CM-2 |
| **MISD** | many | one | rare; fault-tolerant flight computers, some systolic arrays |
| **MIMD** | many | many | multi-core PC, SMP server, cluster, Blue Gene |

In **SISD** one CU fetches instructions one after another and drives one PU on one stream of data. In **SIMD** one CU broadcasts the same instruction to many PUs, each working on its own data, so one `ADD` adds many pairs of numbers. In **MISD** several CUs act on the same data stream as it passes along a chain; real examples are few. In **MIMD** every processor has its own CU and its own program and data; the processors may share memory (multiprocessor) or have private memory and exchange messages (multicomputer). A modern PC is MIMD across its cores and SIMD inside each core.

**Q2. What is pipelining? Derive the speed-up and efficiency of a k-stage pipeline and explain why the real speed-up is lower. (5 marks)**

**Pipelining** splits a task into k stages separated by registers, each stage taking one clock period t_p. While task 1 is in stage 2, task 2 is already in stage 1, like cars on an assembly line (Plate 8.1). Once the pipeline is full, one task finishes every clock.

For n tasks, the first needs k clocks and every later task needs one more, so the pipelined time is **(k + n − 1) t_p** (Fig. 8.2: 4 + 6 − 1 = 9 clocks). Without a pipeline the tasks take n k t_p. Therefore

- **Speed-up S = n k / (k + n − 1)**, which tends to k as n becomes large.
- **Efficiency = S / k**, the fraction of the stages kept busy.
- **Throughput = n / ((k + n − 1) t_p)**, tending to one result per clock.

For k = 4 and n = 100 the speed-up is 400 / 103 = 3.88 and the efficiency 0.97 (Fig. 8.3). For a single task S = 1.

The real speed-up is lower because (1) the pipeline needs k − 1 clocks to fill and drain, (2) stages are not equal in delay and the slowest one sets the clock, (3) registers between stages add delay, and (4) hazards force stalls: structural conflicts, data dependencies and branches.

**Q3. A five-stage pipeline with a stage delay of 4 ns executes 30 tasks. Find the time, speed-up, efficiency and throughput. (5 marks)**

Given k = 5, n = 30, t_p = 4 ns. The same method applies whatever the numbers are.

**Pipelined time.** The first task leaves after 5 clocks and the other 29 leave one per clock, so the number of clocks is k + n − 1 = 5 + 29 = 34. The time is 34 × 4 = **136 ns**.

**Non-pipelined time.** Each task passes all five stages one after another, so the time is n k t_p = 30 × 5 × 4 = **600 ns**.

**Speed-up.** S = 600 / 136 = **4.41**. This is the same as n k / (k + n − 1) = 150 / 34 = 4.41.

**Efficiency.** E = S / k = 4.41 / 5 = **0.882**, so the stages are busy 88.2% of the time.

**Throughput.** n / time = 30 / 136 ns = 0.2206 tasks per ns, which is about **220.6 million tasks per second**. The non-pipelined machine gives 30 / 600 = 50 million per second.

| Quantity | Pipelined | Not pipelined |
|---|---|---|
| Total time | 136 ns | 600 ns |
| Tasks per second | 220.6 million | 50 million |
| Speed-up | 4.41 | 1 |

If the number of tasks grew to 1000, the speed-up would rise to 5000 / 1004 = 4.98, close to the ideal limit of k = 5. This shows that a pipeline pays off for long, steady streams of work, which is why instruction pipelines are so successful.

**Q4. Explain the four-segment floating-point adder pipeline and trace 0.75 + 0.15625 through it. (5 marks)**

Floating-point addition cannot simply add the mantissas because the exponents may differ. The operation is split into four segments, with a register between each pair (Fig. 8.4):

1. **Compare exponents.** Subtract them; the larger one becomes the exponent of the result and the difference tells how far to shift.
2. **Align mantissas.** Shift the mantissa of the number with the smaller exponent to the right by the difference.
3. **Add or subtract the mantissas.**
4. **Normalise the result.** Shift it back to the form 1.xxx and adjust the exponent; round if needed.

**Trace.** X = 0.75 = 1.1 × 2⁻¹ and Y = 0.15625 = 1.01 × 2⁻³ (binary mantissas).

| Segment | Work | Result |
|---|---|---|
| 1 | exponents −1 and −3, difference 2 | exponent −1 kept |
| 2 | shift 1.01 right by 2 places | 0.0101 × 2⁻¹ |
| 3 | 1.1 + 0.0101 | 1.1101 × 2⁻¹ |
| 4 | already in form 1.xxx | 1.1101 × 2⁻¹ |

The result is 1.1101₂ × 2⁻¹ = 1.8125 × 0.5 = **0.90625**, which equals 0.75 + 0.15625. Because the segments are separated by registers, four different additions can be in the four segments at once, so after the pipeline fills a result is produced every clock. This is how vector processors and floating-point units deliver one sum per cycle.

**Q5. Explain the hazards that occur in an instruction pipeline and the methods used to reduce their effect, including branch handling. (10 marks)**

A **hazard** is a condition that prevents the next instruction from executing in its own clock cycle. The pipeline must then stall (insert **bubbles**) or take another action, and the speed-up falls.

**1. Structural hazards** occur when two instructions need the same hardware at the same time, for example one memory port used both for fetching an instruction and for loading an operand. The remedy is to duplicate the resource, such as separate instruction and data caches.

**2. Data hazards** occur when an instruction needs a result that an earlier one has not produced yet.

| Type | Meaning | Example |
|---|---|---|
| RAW (true dependency) | I2 reads what I1 writes | `ADD R1,R2,R3` then `SUB R4,R1,R5` |
| WAR (anti-dependency) | I2 writes what I1 reads | arises with out-of-order issue |
| WAW (output dependency) | both write the same register | arises with out-of-order issue |

In the five-stage pipeline of Fig. 8.5 the `SUB` must wait two cycles for the `ADD` result to be written. Remedies are a hardware **interlock** (stall), **operand forwarding** (the ALU output is sent straight to the next ALU input, removing the stall), and **compiler scheduling** (an independent instruction or a NOP is placed in the gap). A load followed at once by its use still needs one stall.

**3. Control (branch) hazards** occur because a branch changes the PC after the next instructions have already been fetched. Techniques:

- **Prefetch both paths** into separate buffers and discard one.
- **Branch target buffer (BTB):** a small cache holding the target address of recent branches.
- **Branch prediction:** static (not taken, or backward taken) or dynamic. A two-bit counter (Fig. 8.6) mispredicts a loop once per exit, 90% accuracy for a loop of 10.
- **Loop buffer** for small loops, and **delayed branch**, in which the compiler fills the slot after the branch with a useful instruction.

**Effect on CPI.** With 20% branches and a 2-cycle penalty, stalling on every branch gives CPI = 1 + 0.2 × 2 = 1.40, always-not-taken with 60% taken gives 1.24, and a 90% accurate predictor gives 1 + 0.2 × 0.1 × 2 = 1.04.

In conclusion, pipelines deliver close to one instruction per clock only when hazards are removed by duplicated hardware, forwarding and good prediction.

**Q6. What is vector processing? Why does it speed up scientific programs, and how many operations does matrix multiplication need? (5 marks)**

Scientific programs, such as weather models, structural analysis and graphics, apply the same operation to long arrays. A **vector processor** has instructions that operate on a whole vector, so `C(1:64) = A(1:64) + B(1:64)` is one instruction instead of a loop of 64 iterations. A Cray-1 had eight vector registers of 64 elements each (Plate 8.1).

The speed-up has several sources:

- **Fewer instruction fetches and decodes:** one instruction replaces 64 iterations.
- **No loop overhead and no branch hazards** inside the vector.
- **Pipelined arithmetic:** after a start-up of 6 clocks, the six-stage adder gives one sum per clock, so 64 additions take 6 + 63 = 69 clocks instead of 64 × 6 = 384, a speed-up of 5.6 (Fig. 8.7).
- **Interleaved memory** supplies one operand per clock because consecutive addresses lie in different modules.

**Matrix multiplication.** For n × n matrices, C = A × B needs **n³ multiplications and n²(n − 1) additions**. Each element C(i,j) is the inner product of row i of A and column j of B. For n = 2 this is 8 multiplications and 4 additions; for n = 3 it is 27 and 18. With A = [[1,2],[3,4]] and B = [[5,6],[7,8]], C = [[19,22],[43,50]]. Each inner product is a stream of multiply-add operations, so several pipelines can compute different rows at once. Systolic arrays and GPUs use this idea.

**Q7. What is a multiprocessor? Describe the interconnection structures and the cache coherence problem and its solutions. (10 marks)**

A **multiprocessor** is a computer with two or more CPUs that share one memory and run under one operating system, a *tightly coupled* MIMD system. A **multicomputer** or cluster has separate memories and exchanges messages. Multiprocessors give higher throughput, speed for parallel programs, graceful degradation if a CPU fails, and the ability to add processors.

**Interconnection structures.**

| Structure | Idea | Advantage | Limit |
|---|---|---|---|
| Common bus | all CPUs and memories on one bus | cheap and simple | only one transfer at a time |
| Multiport memory | one port per CPU on each memory | high bandwidth | many wires, complex memory |
| Crossbar | a switch at each CPU-memory crossing | many simultaneous transfers | n × n switches (4096 for n = 64) |
| Multistage (Omega) | log₂ n stages of 2 × 2 switches | (n / 2) log₂ n switches (192 for n = 64) | some blocking |
| Hypercube | 2ⁿ nodes, each linked to n neighbours | any node in n hops | wiring grows with n |

Fig. 8.8 shows a crossbar carrying four transfers at once, and Fig. 8.9 a 3-cube in which a message flips one address bit per hop. Arbitration (fixed priority, rotating priority or daisy chain) decides who gets a shared bus.

**Cache coherence.** Each CPU has a private cache, so two caches may hold different values of the same variable. If CPU A writes X = 7 and CPU B still holds X = 5, B reads stale data. Solutions:

1. **Write-invalidate:** a write removes all other copies; this is the common choice.
2. **Write-update (broadcast):** a write sends the new value to all copies.
3. **Snooping:** each cache watches the shared bus for writes. The **MESI** protocol labels each line Modified, Exclusive, Shared or Invalid (Fig. 8.10).
4. **Directory-based:** a directory records which caches hold each block, so only those are contacted; it scales to larger systems.

For example, with a shared bus every miss in any cache uses the same wires, so beyond a few cores a bus saturates and designers move to crossbars, rings or directory-based networks, as in server chips with dozens of cores. Programs also need **synchronisation** (locks built from atomic test-and-set, semaphores, barriers). In conclusion, the speed of a multiprocessor depends as much on the interconnect and coherence cost as on the number of CPUs, and Amdahl's law limits what extra CPUs can achieve.

**Q8. State Amdahl's law. A program is 95% parallelisable; find the speed-up on 8 and 64 processors and the upper limit. (5 marks)**

**Amdahl's law** says that if a fraction P of a program can be run in parallel on N processors and the rest, 1 − P, must run serially, the speed-up is

**S = 1 / ((1 − P) + P / N).**

The serial part does not shrink, so it sets a ceiling: as N grows, S tends to 1 / (1 − P).

For P = 0.95:

- **N = 8:** S = 1 / (0.05 + 0.95 / 8) = 1 / (0.05 + 0.11875) = 1 / 0.16875 = **5.93**.
- **N = 64:** S = 1 / (0.05 + 0.95 / 64) = 1 / (0.05 + 0.01484) = 1 / 0.06484 = **15.4**.
- **Limit (N → ∞):** S = 1 / 0.05 = **20**.

| Processors | Speed-up | Efficiency S / N |
|---|---|---|
| 1 | 1.00 | 100% |
| 8 | 5.93 | 74% |
| 64 | 15.4 | 24% |
| unlimited | 20 | → 0% |

The table shows that eight times more processors (from 8 to 64) gives only 2.6 times more speed. Fig. 8.11 compares three programs; a program with P = 0.5 can never run more than twice as fast. The lesson is that the serial fraction must be reduced as much as the processor count is raised.
