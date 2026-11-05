---
subject: Microprocessor and Computer Architecture
grade: BCA Semester 2
unit: 7
title: Memory Organisation
area: BCA 152 · Microprocessor and Computer Architecture · Unit 7
---

Processor speed has long outrun memory speed. The answer is a **hierarchy** of memories, each level small and fast near the CPU and large and slow far from it, managed so the whole behaves like a large, fast memory. This unit covers the hierarchy, RAM and ROM chips and their address maps, secondary storage, cache memory (mapping, replacement, writes), virtual memory (paging, page replacement), segmentation and protection.

::: key What this unit gives you
- The memory hierarchy and the locality principle.
- RAM and ROM chip types, chip-select decoding and memory address maps.
- Magnetic disk structure and access time.
- Cache memory: hit ratio, three mapping schemes, replacement, write policies, average access time.
- Virtual memory: pages, page tables, page faults, FIFO/LRU/optimal replacement (Belady's anomaly).
- Segmented page mapping and memory protection.
:::

## 7.1 The memory hierarchy

| Level | Technology | Size | Access time | Cost per bit |
|---|---|---|---|---|
| Registers | flip-flops in the CPU | hundreds of bytes | < 1 ns | highest |
| L1 cache | SRAM on the CPU chip | 32–64 KB | 1 ns | |
| L2/L3 cache | SRAM | 256 KB – 32 MB | 3–20 ns | |
| Main memory | DRAM | GBs | 50–100 ns | |
| Secondary | SSD / magnetic disk | 100 GB – TBs | 0.1 ms / 10 ms | |
| Archive | tape, optical | very large | seconds | lowest |

**Principle of locality** makes this effective: *temporal locality* (recently used items are likely to be used again soon — loops) and *spatial locality* (items near a used one are likely to be used soon — sequential code, arrays). The upper levels hold copies of the data most likely to be needed.

## 7.2 Primary memory: RAM and ROM

| Type | Meaning | Notes |
|---|---|---|
| **SRAM** | static RAM — flip-flop cells (6 transistors) | fast, no refresh, expensive, big per bit: **cache** |
| **DRAM** | dynamic RAM — one transistor + capacitor | slower, needs **periodic refresh** (every few ms), cheap and dense: **main memory** (SDRAM, DDR) |
| **ROM** | read-only memory | holds boot program; non-volatile |
| **PROM** | programmable once by the user | |
| **EPROM** | erasable by UV light, reprogrammable | quartz window |
| **EEPROM** | erasable electrically, byte by byte | settings storage |
| **Flash** | block-erasable EEPROM | SSDs, USB sticks, phone storage |

RAM is volatile (loses data at power-off); ROM is non-volatile.

### Memory chip organisation and chip select

A 128 × 8 RAM chip has 7 address lines (2⁷ = 128), 8 data lines, **chip-select (CS)** inputs and read/write lines. When CS is not active the chip's data lines are high-impedance, so many chips can share the bus.

A 2K × 8 chip needs **11** address lines; a 64 KB space needs **16**; building a 64 KB memory from 16K × 8 chips takes 4 chips and 2 address lines (A14, A15) to select among them via a 2-to-4 decoder.

### The memory address map

A **memory address map** is a table listing which chip responds to which range of addresses.

::: example Worked example: 512 B RAM + 512 B ROM
Use four 128 × 8 RAM chips and one 512 × 8 ROM chip in a 10-bit address space (1024 bytes). Address line 10 (counting from 1; the 10th line, A9) selects RAM (0) or ROM (1). Lines A8–A7 drive a 2-to-4 decoder choosing one of the four RAM chips; A6–A0 address within a RAM chip; A8–A0 address within the ROM.

| Component | A9 | A8 A7 | A6–A0 | Hex address range |
|---|---|---|---|---|
| RAM 1 | 0 | 00 | x | 0000 – 007F |
| RAM 2 | 0 | 01 | x | 0080 – 00FF |
| RAM 3 | 0 | 10 | x | 0100 – 017F |
| RAM 4 | 0 | 11 | x | 0180 – 01FF |
| ROM | 1 | xx | x | 0200 – 03FF |

(Range checks: four chips × 128 = 512 = 0x200, so RAM ends at 01FF and the 512-byte ROM occupies 0200–03FF — verified by the script.)
:::

## 7.3 Secondary memory: the magnetic disk

A hard disk has one or more **platters** coated with magnetic material, each surface served by a **read/write head** on an arm. Data are on concentric **tracks**; all tracks at the same arm position form a **cylinder**; each track is divided into **sectors** (commonly 512 bytes or 4 KB).

**Capacity = surfaces × cylinders (tracks per surface) × sectors per track × bytes per sector.**
Example: 8 surfaces × 1000 cylinders × 63 sectors × 512 B = **258,048,000 bytes** ≈ 258 MB.

**Access time = seek time + rotational latency + transfer time.**

- **Seek time**: moving the arm to the right cylinder (a few ms on average).
- **Rotational latency**: waiting for the sector to arrive under the head; on average **half a revolution**: at 7200 rpm, one revolution = 60/7200 s = 8.33 ms, so average latency = **4.17 ms**.
- **Transfer time**: sector size ÷ transfer rate (microseconds for one sector).

Disks are about 10⁵–10⁶ times slower than DRAM, which is why caching and virtual memory exist. SSDs have no moving parts (no seek or rotational latency) and use flash memory.

## 7.4 Cache memory

A **cache** is a small, fast memory between the CPU and main memory that holds copies of recently used blocks.

- **Hit**: the word is in the cache. **Miss**: it is not; the whole **block** (line, e.g. 16 or 64 bytes) is fetched from main memory.
- **Hit ratio h** = hits ÷ total accesses; miss ratio = 1 − h.
- **Average memory access time (AMAT) = h × t_cache + (1 − h) × (t_cache + t_memory)** = t_cache + (1 − h) × t_memory.

::: example Worked example: average access time
Cache access 10 ns, main memory 100 ns, hit ratio 0.9. AMAT = 0.9 × 10 + 0.1 × (10 + 100) = 9 + 11 = **20 ns**; without a cache each access costs 100 ns, so the cache gives a speed-up of 100/20 = **5**. A second case: cache 2 ns, memory 50 ns, h = 0.95: AMAT = 0.95 × 2 + 0.05 × 52 = 1.9 + 2.6 = **4.5 ns**. (Both verified by script.)
:::

### Mapping functions — where does a memory block go?

Memory is divided into blocks the size of a cache line. A **mapping function** decides which cache line may hold a given block. Each cache line stores a **tag** identifying which block it currently holds, plus a valid bit.

| Mapping | Rule | Address split | Pros / cons |
|---|---|---|---|
| **Direct** | block *j* → line (*j* mod number of lines) | tag · index · offset | simplest, fastest; **conflict misses** if two active blocks share a line |
| **Fully associative** | a block may go in **any** line | tag · offset | no conflicts; needs comparing the tag against **all** lines (expensive) |
| **Set associative** (k-way) | block *j* → set (*j* mod number of sets); any of k lines in the set | tag · set · offset | the practical compromise (2-, 4-, 8-way) |

::: example Worked example: direct-mapped address split
Main memory 64 KB (16-bit addresses), cache 1 KB, block (line) size 16 bytes. Offset = log₂16 = **4** bits. Number of lines = 1024/16 = 64 ⇒ index = **6** bits. Tag = 16 − 4 − 6 = **6** bits.
Address **A3C7** = 1010 0011 1100 0111: tag = 101000 (28H), index = 111100 (3CH = line 60), offset = 0111 (7). The byte is in cache line 60 if its tag equals 28H.
For a **4-way set-associative** cache of the same size: 64 lines ÷ 4 = **16 sets** ⇒ index 4 bits, tag 8 bits.
:::

### Replacement policies (associative caches)

When a set is full, which line is evicted? **LRU** (least recently used — best in practice, needs bookkeeping), **FIFO** (oldest in), **random**, **LFU** (least frequently used). A direct-mapped cache needs no policy.

### Write policies

| Policy | Operation | Notes |
|---|---|---|
| **Write-through** | write cache **and** main memory together | memory always up to date; slow unless a *write buffer* is used |
| **Write-back** | write the cache only; mark line **dirty**; write to memory when the line is evicted | far fewer memory writes; more complex (coherence in multi-core) |
| *Write-allocate / no-write-allocate* | on a write miss, load the block (or not) | usually write-back + write-allocate |

Cache **coherence** (several CPUs with private caches) is covered in Unit 8.

## 7.5 Virtual memory

**Virtual memory** gives each program the illusion of a very large, private, contiguous address space — bigger than physical memory — by keeping the program on disk and loading **pages** into RAM on demand.

- The CPU issues **virtual (logical) addresses**; the **memory-management unit (MMU)** translates them to **physical addresses**.
- Virtual space is divided into **pages** (typically 4 KB); physical memory into **frames** of the same size.
- A **page table** (per process) maps page numbers → frame numbers; each entry has a **valid/present bit** and protection bits.

```
 virtual address = [ page number | offset ]  ──► page table ──► [ frame number | offset ] = physical address
```

::: example Worked example: address translation
32-bit virtual address, 4 KB pages: offset = 12 bits, page number = 20 bits ⇒ 2²⁰ = 1,048,576 page-table entries; with 4-byte entries the page table is **4 MB** per process (hence multi-level page tables). Virtual address 0x00003A7C: page = 3, offset = A7C. If page-table[3] = frame 0x1B, the physical address = 0x1B·1000 + A7C = **0x0001BA7C**.
:::

### Page fault and demand paging

If the valid bit is 0 the access causes a **page fault** (a trap): the OS finds a free frame (or **evicts** a page), reads the page from disk, updates the page table and **restarts** the instruction. A page fault costs milliseconds, so the page-fault rate must be tiny: effective access time ≈ (1 − p) × t_mem + p × t_fault. A **TLB** (translation lookaside buffer, a small cache of page-table entries) avoids the extra memory access for the page table on most references.

### Page replacement algorithms

Reference string 7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2 with **3 frames** — page faults:

| Algorithm | Rule | Faults |
|---|---|---|
| **FIFO** | evict the page that has been in memory longest | **10** |
| **LRU** | evict the page unused for the longest time | **9** |
| **Optimal (OPT)** | evict the page that will not be used for the longest time in the future (unrealisable; the benchmark) | **7** |

(Counted by script.) **Belady's anomaly:** with FIFO, giving a process *more* frames can increase faults: the string 1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5 gives **9 faults with 3 frames but 10 with 4 frames**. LRU and OPT (stack algorithms) never show it.

**Thrashing** — when the total working sets exceed physical memory, processes spend most of their time page-faulting. The OS then reduces the number of active processes.

## 7.6 Memory management hardware

### Segmentation and segmented page mapping

A **segment** is a logical unit (code, data, stack) of variable size. A **segmented address** is (segment, offset); a **segment table** gives each segment's base and limit. Segmentation matches the programmer's view and eases sharing and protection, but suffers from **external fragmentation**. **Segmented-page mapping** combines both: a logical address is **segment · page · offset**; the segment table points to a page table for that segment, and paging removes external fragmentation. The Intel 386+ supports both.

### Memory protection

Protection prevents one program from reading or writing another's memory or the OS's:

- **Base and limit registers**: every address must lie in [base, base + limit); otherwise a trap.
- **Protection bits** per page or segment: read/write/execute, user/supervisor.
- **Privilege levels / rings** (kernel versus user mode): privileged instructions and I/O only in kernel mode.
- Access to a page with the wrong permission raises a protection fault (**segmentation fault** in Unix terms).

## Formula and fact sheet

- n address lines → 2ⁿ locations; chips needed = total size ÷ chip size.
- Disk capacity = surfaces × tracks × sectors × bytes; access = seek + rotational (½ revolution) + transfer; at 7200 rpm average latency 4.17 ms.
- AMAT = t_c + (1 − h) × t_m (= h·t_c + (1 − h)(t_c + t_m)).
- Direct-mapped split: offset = log₂(block size); index = log₂(lines); tag = address bits − index − offset. k-way: sets = lines ÷ k.
- Pages: offset = log₂(page size); page-table entries = 2^(page-number bits).
- FIFO may show Belady's anomaly; LRU and OPT do not.

## Chapter summary

- The hierarchy trades size, speed and cost; locality makes it work.
- SRAM for cache, DRAM for main memory, ROM family for non-volatile code; the address map and chip-select decode place chips in the address space.
- A disk's access time is dominated by seek and rotation.
- Caches map blocks by direct, fully associative or set-associative rules, replace by LRU/FIFO/random and write by write-through or write-back.
- Virtual memory pages programs on demand; page faults are handled by the OS using FIFO/LRU-like replacement; TLBs speed translation.
- Segmentation and segmented paging structure memory; base/limit registers and protection bits enforce isolation.

## Practice

1. Explain the memory hierarchy and the principle of locality.
2. Differentiate between SRAM and DRAM; between PROM, EPROM and EEPROM.
3. Design a memory address map for 1 KB RAM (four 256 × 8 chips) and 512 B ROM in an 11-bit address space.
4. A disk has 4 surfaces, 500 cylinders, 40 sectors per track and 1 KB sectors, rotating at 6000 rpm. Find its capacity and the average rotational latency.
5. A cache of 8 KB, 32-byte blocks, 24-bit addresses, direct-mapped: find offset, index, tag bits.
6. A system has cache time 5 ns, memory time 60 ns, hit ratio 0.92. Find the average access time and the speed-up.
7. Compare direct, associative and set-associative mapping.
8. Distinguish write-through and write-back.
9. For the string 1 2 3 2 4 1 5 2 1 2 3 4 with 3 frames, count page faults under FIFO and LRU.
10. Explain paging, page tables, page faults and the role of the TLB. What is memory protection?

::: note Answers and worked solutions
**1.** See 7.1: levels from registers to disk; locality (temporal and spatial) means the upper levels satisfy most accesses.
**2.** SRAM: flip-flop cells, fast, no refresh, used for cache; DRAM: capacitor cells, refresh needed, cheaper and denser, used for main memory. PROM: programmed once; EPROM: UV-erasable; EEPROM: electrically erasable per byte.
**3.** 1 KB RAM = 4 × 256 B ⇒ 8 address lines per chip; 512 B ROM needs 9 lines. In an 11-bit space (2 KB): A10 = 0 selects RAM, A10 = 1 ROM; A9–A8 → 2-to-4 decoder for the RAM chips; ranges RAM 000–0FF, 100–1FF, 200–2FF, 300–3FF; ROM 400–5FF.
**4.** Capacity = 4 × 500 × 40 × 1024 = **81,920,000 B**. 6000 rpm → 10 ms per revolution → latency **5 ms**.
**5.** Offset = 5 bits (32 B); lines = 8192/32 = 256 ⇒ index 8 bits; tag = 24 − 8 − 5 = **11** bits.
**6.** AMAT = 5 + 0.08 × 60 = **9.8 ns**; speed-up = 60/9.8 ≈ **6.1**.
**7.** Direct: one possible line, simple, conflict misses; associative: any line, no conflicts, costly comparators; set-associative: k lines per set, balanced.
**8.** Write-through updates cache and memory together; write-back updates only the cache and writes the dirty line back on eviction.
**9.** FIFO (frames after each fault): 1 F [1]; 2 F [1,2]; 3 F [1,2,3]; 2 H; 4 F [2,3,4]; 1 F [3,4,1]; 5 F [4,1,5]; 2 F [1,5,2]; 1 H; 2 H; 3 F [5,2,3]; 4 F [2,3,4] → **9 faults**. LRU: 1 F; 2 F; 3 F; 2 H; 4 F (evict 1) [3,2,4]; 1 F (evict 3) [2,4,1]; 5 F (evict 2) [4,1,5]; 2 F (evict 4) [1,5,2]; 1 H; 2 H; 3 F (evict 5) [1,2,3]; 4 F (evict 1) [2,3,4] → also **9 faults**. Both counts were checked by script; the two policies happen to tie on this string.
**10.** Pages/frames, per-process page table with valid bit; a page fault traps to the OS which loads the page; the TLB caches recent translations; memory protection uses base/limit registers and permission bits to confine each process.
:::
