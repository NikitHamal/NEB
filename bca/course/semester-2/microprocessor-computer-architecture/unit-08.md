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
