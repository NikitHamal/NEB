---
subject: Operating Systems
grade: BCA Semester 4
unit: 6
title: Input/Output Device Management
hours: 4
area: BCA 251 · Operating Systems · Unit 6
---

Disks, keyboards, printers and network cards differ wildly in speed (a keyboard sends a few bytes a second, a disk hundreds of megabytes). The OS hides these differences behind a uniform interface and uses clever tricks (interrupts, DMA, buffering, disk scheduling) so that the CPU is not left waiting.

::: key What this unit gives you
- I/O hardware: devices, controllers, memory-mapped I/O, DMA.
- I/O software: goals, programmed I/O, interrupt-driven I/O, DMA I/O, and the software layers.
- Disk hardware and disk scheduling (FCFS, SSTF, SCAN, C-SCAN, LOOK, C-LOOK) with verified examples.
:::

## 6.1 Principles of I/O hardware

### I/O devices

| Class | Transfer unit | Examples |
|---|---|---|
| **Block devices** | fixed-size blocks, randomly addressable | hard disk, SSD, USB drive |
| **Character devices** | stream of bytes, no addressing | keyboard, mouse, serial port, printer |
| **Network devices** | packets | Ethernet, Wi-Fi |

Data rates range over about nine orders of magnitude: keyboard ≈ 10 B/s; Gigabit Ethernet ≈ 125 MB/s; NVMe SSD ≈ several GB/s.

### Device controllers

An I/O device has a mechanical part and an electronic part, the **controller** (adapter). The OS talks to the controller, not the device. For a disk, the controller reads the bit stream, assembles it into a block, checks the error-correcting code and puts the block in its own buffer. The controller has **registers** (command, status, data) which the CPU reads and writes.

### Addressing the controller: port-mapped and memory-mapped I/O

- **Separate I/O space**: each controller register has an I/O port number, accessed with special instructions (`IN`, `OUT` on x86).
- **Memory-mapped I/O**: the registers are mapped to *addresses in the normal memory space*, so ordinary `load` and `store` instructions (and C pointers) control devices. No special instructions, and the OS can use page protection to decide who may touch a device; the cost is that caching must be disabled for those addresses.

### Direct memory access (DMA)

Without DMA the CPU copies every byte between the controller and memory. A **DMA controller** moves a whole block by itself:

1. The CPU programs the DMA controller: memory address, byte count, direction, device.
2. The DMA controller requests the block from the device controller.
3. The device controller transfers data to memory over the bus. (*Cycle stealing*: DMA takes bus cycles when the CPU is not using them.)
4. On completion the device controller signals the DMA controller, which raises **one interrupt** to tell the CPU.

The CPU is therefore interrupted once per block instead of once per byte.

::: example Why DMA matters
Reading a 4 KB block with interrupt-driven byte transfer needs 4,096 interrupts. If each interrupt costs 2 µs of CPU time, the CPU spends 8.2 ms servicing the transfer. With DMA there is one interrupt (2 µs), a saving of 99.98 %.
:::

## 6.2 Principles of I/O software

### Goals

- **Device independence**: programs read a file whether it is on a disk or a USB drive.
- **Uniform naming**: a name is a string, not tied to hardware (`/dev/sda`, `D:`).
- **Error handling**: handle errors as close to the hardware as possible; hide transient errors from higher layers.
- **Synchronous (blocking) vs asynchronous (interrupt-driven)** transfers: programs prefer blocking calls, hardware is interrupt-driven.
- **Buffering**: store data temporarily to smooth speed differences.
- **Sharable vs dedicated devices**: a disk is shared; a printer is exclusive (spooling resolves this).

### Three ways to do I/O

| Method | How | CPU involvement | Good for |
|---|---|---|---|
| **Programmed I/O (polling)** | CPU loops reading the status register until ready, then copies each byte | 100 % busy during transfer | tiny embedded systems |
| **Interrupt-driven I/O** | CPU starts the device and does other work; device interrupts when a byte or block is ready | an interrupt per unit | slow character devices |
| **I/O using DMA** | DMA controller moves the block; one interrupt at the end | start + one interrupt | disks, network, bulk data |

::: example Programmed I/O on a printer
To print "ABC" the CPU copies the first character to the printer's data register, then busy-waits until the status register says "ready", copies the next one, and so on. In interrupt-driven I/O, the CPU copies one character, blocks the calling process (the scheduler runs something else) and the printer's "ready" interrupt wakes the process to send the next character.
:::

## 6.3 I/O software layers

I/O software is organised in four layers, from the hardware up:

| Layer | Job |
|---|---|
| 1. **Interrupt handlers** | save registers, find the source of the interrupt, run the handler, unblock the waiting driver, restore and return |
| 2. **Device drivers** | device-specific code that issues commands to the controller, supplied by the manufacturer, normally run in kernel mode |
| 3. **Device-independent I/O software** | uniform interface to drivers, naming, protection, buffering, block size, allocation of dedicated devices, error reporting |
| 4. **User-space I/O software** | library calls (`printf`, `read`) and spooling daemons |

A typical interrupt sequence: the device raises the interrupt; the CPU saves the program counter and PSW and jumps to the handler; the handler acknowledges the interrupt controller, runs, and signals the driver; the scheduler picks the next process.

**Buffering** schemes: none (the process waits on every transfer), single buffer, double buffer (fill one while the process drains the other), circular buffer. **Spooling** keeps a queue of print jobs on disk, and a daemon prints them one at a time, so processes need never hold the printer.

## 6.4 Disk hardware and disk scheduling

### Disk geometry

A magnetic disk has **platters** with **tracks** divided into **sectors**; the same track on all platters forms a **cylinder**. The disk arm moves the heads to a cylinder.

A disk access has three parts:

- **Seek time**: moving the arm to the right cylinder (several ms).
- **Rotational delay (latency)**: waiting for the sector to rotate under the head; average half a rotation.
- **Transfer time**: reading the data as it passes under the head.

::: example Access time of one 4 KB block
Disk: 7200 rpm, average seek 9 ms, transfer rate 100 MB/s. One rotation takes 60/7200 = 8.33 ms, so the average rotational latency is half of it, **4.17 ms**. Transfer of 4 KB = 4/1024 MB ÷ 100 MB/s = **0.039 ms**. Total ≈ 9 + 4.17 + 0.04 = **13.21 ms**. Seek and rotation dominate, which is why scheduling the arm (and reading in large chunks) pays. A track holding 400 sectors of 512 B turns 120 times per second, a media rate of 400 × 512 × 120 = **24.6 MB/s**.
:::

Seek time is the cost to minimise by ordering the requests. (SSDs have no arm, so these algorithms matter for hard disks; SSD schedulers mostly merge and batch requests.)

### Disk scheduling algorithms

Take a disk with cylinders 0–199, the head at **53**, and the queue of requests **98, 183, 37, 122, 14, 124, 65, 67**. We count the total head movement in cylinders. All results below were computed by `bca/tools/check_os.py`.

**FCFS.** Serve in arrival order: 53 → 98 → 183 → 37 → 122 → 14 → 124 → 65 → 67. Movement: 45 + 85 + 146 + 85 + 108 + 110 + 59 + 2 = **640** cylinders. Fair, but a lot of wild swinging.

**SSTF (shortest seek time first).** Always go to the nearest pending request: 53 → 65 → 67 → 37 → 14 → 98 → 122 → 124 → 183. Movement: 12 + 2 + 30 + 23 + 84 + 24 + 2 + 59 = **236**. A greedy choice like SJF; it can **starve** far-away requests when new nearby ones keep arriving.

**SCAN (elevator).** The arm sweeps in one direction, serving requests on the way, goes to the **end of the disk**, then reverses. Going up first: 53 → 65 → 67 → 98 → 122 → 124 → 183 → **199** → 37 → 14. Movement: (199 − 53) + (199 − 14) = 146 + 185 = **331**. If the arm instead started downwards: 53 → 37 → 14 → **0** → 65 → 67 → 98 → 122 → 124 → 183 gives 53 + 183 = **236**. The direction at the start matters, so the question must state it.

**LOOK.** Like SCAN but reverses at the *last request* rather than the disk end: 53 → 65 → 67 → 98 → 122 → 124 → 183 → 37 → 14 = (183 − 53) + (183 − 14) = 130 + 169 = **299**.

**C-SCAN (circular SCAN).** Sweeps in one direction only; at the end it jumps back to cylinder 0 without serving requests and starts again, giving more uniform waiting times. Path: 53 → 65 → 67 → 98 → 122 → 124 → 183 → 199 → 0 → 14 → 37. Counting the return jump, movement is 146 + 199 + 37 = **382**; if only the service sweeps are counted (the jump excluded) it is 146 + 37 = **183**. Always say whether the return is counted.

**C-LOOK.** C-SCAN that goes only as far as the last request: 53 → 65 → 67 → 98 → 122 → 124 → 183 → 14 → 37: (183 − 53) + (183 − 14) + (37 − 14) = 130 + 169 + 23 = **322** (with the return jump counted).

| Algorithm | Total movement | Comment |
|---|---|---|
| FCFS | 640 | fair, worst here |
| SSTF | 236 | good average, starvation risk |
| SCAN (up first) | 331 | no starvation |
| SCAN (down first) | 236 | direction changes the answer |
| LOOK (up first) | 299 | SCAN without useless travel |
| C-SCAN (jump counted) | 382 | uniform wait |
| C-LOOK (jump counted) | 322 | C-SCAN without useless travel |

::: note Choosing an algorithm
For light loads FCFS is acceptable; SSTF is a natural choice; under heavy load SCAN and C-SCAN are better because they cannot starve any request. Linux's historical elevators (deadline, CFQ, now mq-deadline and BFQ) are variants of these ideas.
:::

### Disk management and RAID in brief

Low-level formatting writes sectors with headers and ECC; the OS then **partitions** the disk and builds a file system. The **boot block** holds the bootstrap loader; bad blocks are remapped to spare sectors. **RAID** combines disks: RAID 0 stripes for speed (no redundancy), RAID 1 mirrors, RAID 5 stripes with distributed parity (survives one disk failure; usable capacity (n − 1)/n).

## Formula and fact sheet

- Access time = seek + rotational latency + transfer. Average latency = ½ × (60 / rpm) s.
- Transfer time = size / transfer rate. Media rate = sectors per track × sector size × rotations per second.
- FCFS, SSTF, SCAN, C-SCAN, LOOK, C-LOOK: total head movement in cylinders; state direction and whether jumps count.
- Programmed I/O = polling, interrupt-driven = per-unit interrupt, DMA = one interrupt per block.
- Layers: interrupt handlers → device drivers → device-independent software → user-space.

## Chapter summary

- Devices are block or character; each has a controller reached through ports or memory-mapped registers.
- DMA lets the controller move whole blocks and interrupt the CPU once.
- I/O software aims for device independence, uniform naming, buffering and error handling; it is layered (handler, driver, device-independent, user).
- Disk time is dominated by seek and rotation, so the arm is scheduled: SSTF is greedy, SCAN and C-SCAN sweep, LOOK variants save needless travel.

## Practice

1. Differentiate block and character devices with two examples each.
2. What is memory-mapped I/O? State one advantage and one disadvantage.
3. Explain how DMA transfers a block, and why it reduces CPU load.
4. Compare programmed, interrupt-driven and DMA I/O.
5. List the four layers of I/O software and what each does.
6. Disk at 5400 rpm, average seek 12 ms, transfer rate 80 MB/s. Find the average time to read one 8 KB block.
7. Head at 50 on a disk with cylinders 0–199; queue 82, 170, 43, 140, 24, 16, 190. Compute total head movement for FCFS, SSTF and SCAN (up first).
8. Why can SSTF starve requests, and how does SCAN avoid it?
9. What is spooling? Name a device where it is used.

::: note Answers and worked solutions
**1.** Block: hard disk, SSD (addressable fixed blocks). Character: keyboard, serial port (byte streams, no seek).
**2.** The device registers occupy part of the address space and are accessed with `load`/`store`. Advantages: no special I/O instructions, easy protection through memory management. Disadvantage: caching must be disabled for those addresses, and the bus must route addresses to memory or devices.
**3.** The CPU gives the DMA controller the memory address, count and direction; the controller moves the data over the bus without the CPU, then interrupts once. One interrupt per block instead of one per byte frees the CPU for other processes.
**4.** Programmed: CPU polls, 100 % busy. Interrupt-driven: CPU does other work, one interrupt per byte/word. DMA: one interrupt per block, best for large transfers.
**5.** Interrupt handlers (take the interrupt, wake the driver); device drivers (device-specific commands); device-independent software (naming, buffering, protection, errors); user-space (libraries, spooler).
**6.** One rotation = 60/5400 = 11.11 ms; average latency = 5.56 ms. Transfer = 8/1024 MB ÷ 80 MB/s = 0.098 ms. Total = 12 + 5.56 + 0.10 = **17.65 ms**.
**7.** FCFS: |50−82| + |82−170| + |170−43| + |43−140| + |140−24| + |24−16| + |16−190| = 32 + 88 + 127 + 97 + 116 + 8 + 174 = **642**. SSTF: 50 → 43 (7) → 24 (19) → 16 (8) → 82 (66) → 140 (58) → 170 (30) → 190 (20) = **208**. SCAN up: 50 → 82 → 140 → 170 → 190 → 199, then to 43, 24, 16: (199 − 50) + (199 − 16) = 149 + 183 = **332**.
**8.** If requests keep arriving near the head, the distant request is never the closest and waits indefinitely. SCAN guarantees that the arm eventually reaches every cylinder in a sweep, so every request waits at most about two sweeps.
**9.** Spooling stores output jobs in a disk queue and a daemon feeds the device one at a time, so no process holds a dedicated device. Used for printers.
:::
