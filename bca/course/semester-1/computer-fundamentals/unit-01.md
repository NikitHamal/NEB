---
subject: Computer Fundamentals and Applications
grade: BCA Semester 1
unit: 1
title: Introduction to Computer System
hours: 16
area: BCA 101 · Computer Fundamentals and Applications · Unit 1
---

Every other subject in the BCA stands on this unit. Before you can write a program, design a database or secure a network you must know what a computer is made of, how it executes an instruction, where it keeps data and how it talks to the world. This unit covers all eleven topics of the Tribhuvan University syllabus for the first theory unit, in syllabus order.

::: key What this unit gives you
- What a computer is, its characteristics, and where it is used.
- The three classifications (size, purpose, data handled) and the five generations.
- The anatomy of a digital computer: CPU, memory, I/O, buses, and the stored-program idea.
- The memory hierarchy with real capacities and speeds, and how to compute with memory sizes.
- Input devices, output devices and the interfaces that connect them.
:::

## 1.1 Introduction to computer

A **computer** is an electronic device that accepts data, stores it, processes it according to a stored list of instructions (a program), and produces information. The cycle is **input → process → output**, with **storage** serving all three.

- **Data** are raw facts (`75`, `Sita`, `2082-05-14`). **Information** is data processed into a meaningful form ("Sita scored 75, the class average is 62").
- **Hardware** is the physical machine; **software** is the programs that run on it; **people-ware** (users, programmers, administrators) completes the system.

| Generation | Years (approx.) | Key technology | Examples / notes |
|---|---|---|---|
| First | 1940–1956 | vacuum tubes | ENIAC, UNIVAC I; huge, hot, machine language |
| Second | 1956–1963 | transistors | IBM 1401; assembly language, FORTRAN, COBOL |
| Third | 1964–1971 | integrated circuits (IC) | IBM System/360; operating systems, keyboards and monitors |
| Fourth | 1971–present | microprocessor (VLSI) | Intel 4004 (1971); personal computers, GUI |
| Fifth | present and developing | ULSI, parallel processing, AI | speech recognition, machine learning hardware |

## 1.2 Characteristics of a computer

| Characteristic | Meaning |
|---|---|
| Speed | billions of simple operations per second; a modern CPU runs at 3–5 GHz |
| Accuracy | errors come from wrong input or wrong programs, not from the arithmetic ("garbage in, garbage out") |
| Diligence | no tiredness or loss of concentration; the millionth repeat is as good as the first |
| Versatility | the same hardware does accounting, games, design, communication, depending on the program |
| Storage | large amounts of data kept and retrieved in milliseconds or less |
| Automation | once a program starts it runs without human intervention |
| No IQ | a computer does exactly what it is told; it cannot decide what to do on its own |

## 1.3 Applications of computers

Education (e-learning, simulation), business (billing, inventory, payroll), banking (ATMs, mobile banking, ConnectIPS), government (e-governance, citizenship and tax records), health (patient records, scanning, diagnosis support), science and engineering (simulation, weather forecasting), communication (email, video calls), entertainment, transport (airline and bus ticketing, traffic control), and agriculture (weather and market information).

## 1.4 Classification of computers

**By size and power**

| Type | Description | Example use |
|---|---|---|
| Supercomputer | thousands of processors, quadrillions of operations per second | weather and climate models, nuclear and genome simulation |
| Mainframe | very reliable, serves thousands of users and transactions | bank and airline transaction systems |
| Minicomputer (mid-range server) | between mainframe and PC; multiuser | departmental servers, manufacturing control |
| Microcomputer | single-chip CPU; desktop, laptop, tablet, smartphone | personal and office use |
| Embedded computer | a computer inside another device | washing machine, car engine control, router |

**By purpose:** *general-purpose* (can run any program: a PC) and *special-purpose* (built for one task: an ATM controller).

**By data handled**

| Type | Works on | Example |
|---|---|---|
| Analog | continuous physical quantities | speedometer, old thermometer |
| Digital | discrete values (binary 0 and 1) | PC, phone |
| Hybrid | both: analog input converted to digital for processing | ICU patient monitor, petrol pump |

## 1.5 Mobile computing

Mobile computing means using computing and communication while moving, through portable devices, wireless networks and software that works anywhere. Its three parts: **mobile hardware** (smartphone, tablet, laptop, wearable), **mobile communication** (Wi-Fi, 4G/5G, Bluetooth, GPS) and **mobile software** (apps and mobile operating systems such as Android and iOS).

Advantages: access anywhere (mobile banking, wallets such as eSewa and Khalti, maps), productivity and instant communication. Limitations: small screen and keyboard, limited battery life, variable signal quality, security risks (lost device, public Wi-Fi) and limited processing power compared with desktops.

## 1.6 Anatomy of a digital computer

A computer has five functional units.

1. **Input unit**: brings data in (keyboard, mouse, scanner).
2. **Central Processing Unit (CPU)**: the processor.
   - **ALU (Arithmetic Logic Unit)** does arithmetic (+, −, ×, ÷) and logical comparisons (AND, OR, NOT, <, =, >).
   - **CU (Control Unit)** fetches and decodes instructions and sends control signals; it does no calculation.
   - **Registers** are tiny, very fast storage inside the CPU: PC (program counter, address of the next instruction), IR (instruction register), MAR (memory address register), MDR (memory data register), accumulator and general-purpose registers.
3. **Memory unit**: holds programs and data (main memory, then secondary storage).
4. **Output unit**: presents results (monitor, printer, speaker).
5. **Buses**: the wires joining the units: the **address bus** (one-way, CPU → memory, carries the location), the **data bus** (two-way, carries the value) and the **control bus** (read/write, clock and interrupt signals).

::: definition Motherboard
The main circuit board that carries the CPU socket, memory slots, chipset, expansion slots and ports, and the buses that connect them.
:::

## 1.7 Computer architecture

**The stored-program (von Neumann) concept** (John von Neumann, 1945): instructions and data are held in the *same* memory as binary numbers. The CPU fetches instructions from memory one after another, so changing the program means changing memory, not rewiring the machine. **Harvard architecture** uses separate memories (and buses) for instructions and data; it is common in microcontrollers and inside the L1 cache of modern CPUs.

**The instruction cycle** repeats forever:

1. **Fetch**: the address in the PC goes to MAR; memory returns the instruction into MDR, then IR; the PC is incremented.
2. **Decode**: the control unit works out the operation and the operands.
3. **Execute**: the ALU or another unit performs it (a memory access or an I/O may be needed).
4. **Store** the result, then go back to step 1. An **interrupt** (a key press, a timer) can pause this cycle so the CPU can run a handler first.

**Performance** depends on clock speed, instructions per cycle, number of cores and the memory system.

- *Clock cycle time* = 1 / frequency.
- *CPU time* = (instruction count × cycles per instruction) / clock frequency.

::: example Worked example: CPU time
A program executes 2 × 10⁹ instructions at an average of 1.5 cycles per instruction on a 3 GHz CPU. Find the CPU time and the cycle time.

**Solution.** Cycle time = 1 / (3 × 10⁹ Hz) = 0.333 ns. CPU time = (2 × 10⁹ × 1.5) / (3 × 10⁹) = **1 second**.
:::

**Word size and addressing.** An address bus of *n* lines can select 2ⁿ locations. 16 lines → 65,536 locations (64 KiB with one byte per location); 32 lines → 4,294,967,296 locations (4 GiB), which is why 32-bit systems cannot use more than 4 GiB of RAM directly.

**RISC and CISC.** CISC (e.g. x86) has many complex, variable-length instructions; RISC (e.g. ARM, which powers most phones) has few simple, fixed-length instructions that are easy to pipeline.

## 1.8 Memory and its classification

**Units.** A bit is 0 or 1; 1 byte = 8 bits. In the binary convention, 1 KiB = 1024 B, 1 MiB = 1024 KiB, 1 GiB = 1024 MiB, 1 TiB = 1024 GiB. Disk makers use decimal (1 GB = 10⁹ B), so a "500 GB" drive shows about 465 GiB in the operating system. Most textbooks and examiners write KB/MB/GB for the 1024-based units; this book does the same unless it says otherwise.

**Memory hierarchy** (faster ↑ costlier ↑ smaller ↑ at the top):

| Level | Typical size | Typical access time | Volatile? |
|---|---|---|---|
| CPU registers | a few hundred bytes | under 1 ns | yes |
| Cache L1 / L2 / L3 (SRAM) | 32–64 KB per core / 256 KB–2 MB / 8–64 MB shared | about 1 / 4 / 15 ns | yes |
| Main memory (DRAM) | 4–64 GB | 50–100 ns | yes |
| SSD (flash) | 128 GB–4 TB | 0.05–0.1 ms | no |
| Hard disk (magnetic) | 500 GB–20 TB | 5–10 ms | no |
| Optical, tape (archive) | 25 GB–tens of TB | slow | no |

The hierarchy works because of **locality of reference**: a program tends to reuse recently used data (temporal) and nearby data (spatial), so a small fast cache serves most accesses.

**Primary memory**

- **RAM** (random access memory) is read–write and volatile. **SRAM** uses flip-flops (about six transistors per bit): fast, expensive, no refresh; used for cache. **DRAM** stores each bit as charge in a capacitor and must be refreshed thousands of times a second: slower, cheap, dense; used as main memory (DDR4, DDR5 are synchronous DRAM).
- **ROM** (read-only memory) is non-volatile and holds firmware (the BIOS/UEFI that starts the machine). Types: **MROM** (programmed at the factory), **PROM** (programmed once by the user), **EPROM** (erased by ultraviolet light), **EEPROM** (erased electrically, byte by byte), and **flash** (erased in blocks; the memory in USB sticks, SSDs and phones).

| | RAM | ROM |
|---|---|---|
| Volatility | volatile | non-volatile |
| Use | working memory | start-up firmware |
| Access | read and write | mostly read |

**Secondary memory** keeps data permanently. A **hard disk** stores bits on magnetised platters in tracks and sectors, read by a moving head; capacity is platters × surfaces × tracks × sectors × bytes per sector. An **SSD** has no moving parts (NAND flash), so it is faster, silent and shock-resistant. **Optical discs** (CD about 700 MB, DVD 4.7 GB, Blu-ray 25 GB per layer) are read by laser. **Magnetic tape** is sequential and used for cheap, long-term backup.

::: example Worked example: storage arithmetic
(a) How many 4 MB photographs fit on a 64 GB memory card? (b) A 1920 × 1080 screen uses 24 bits per pixel. How much memory holds one frame?

**Solution.** (a) 64 GB = 64 × 1024 MB = 65,536 MB; 65,536 / 4 = **16,384 photographs**. (b) Pixels = 1920 × 1080 = 2,073,600; bytes per pixel = 24/8 = 3; frame = 6,220,800 bytes ≈ **5.93 MB** (6,220,800 / 1,048,576).
:::

**Virtual memory** extends RAM using disk space; **ECC** RAM detects and corrects single-bit errors (servers); **buffering** and **caching** hide the speed gap between devices.

## 1.9 Input devices

An input device converts human or physical data into signals the computer understands.

| Group | Devices |
|---|---|
| Keyboard and pointing | keyboard, mouse, trackball, touchpad, touch screen, light pen, joystick, stylus and graphics tablet |
| Scanning and recognition | flatbed scanner, **barcode reader**, **QR/2-D code reader**, **OCR** (optical character recognition: printed text), **OMR** (optical mark recognition: exam answer sheets), **MICR** (magnetic ink characters on bank cheques), fingerprint, iris and face scanners |
| Audio and video | microphone, webcam, digital camera |
| Sensors | temperature, motion, GPS and accelerometer in phones |

::: caution OCR, OMR and MICR
OCR reads *characters*, OMR reads *marks in positions* (filled bubbles) and MICR reads *magnetic-ink characters* (cheque numbers). Examiners ask the difference.
:::

## 1.10 Output devices

| Type | Devices |
|---|---|
| Soft copy (screen) | CRT, LCD, LED, OLED monitors; projectors. Quality is set by **resolution** (pixels, e.g. 1920 × 1080), **refresh rate** (Hz) and **dot pitch** |
| Hard copy (paper) | **Impact printers** strike the paper (dot-matrix, line printer; can make carbon copies; noisy). **Non-impact printers**: **inkjet** sprays ink drops, **laser** uses a toner-and-drum electrostatic process, **thermal** heats special paper (receipts). Plotters draw large vector drawings; 3-D printers build objects |
| Audio | speakers, headphones |

Printer speed is quoted in **ppm** (pages per minute) or **cps** (characters per second); resolution in **dpi** (dots per inch).

## 1.11 Interfaces

An **interface** is the connection, electrical and logical, between two parts of a system. A **port** is the socket; the **protocol** is the agreed signalling.

| Interface | Type | Notes |
|---|---|---|
| USB (A, B, C) | serial | USB 2.0 up to 480 Mbit/s; USB 3.0 5 Gbit/s; USB 3.2 up to 20 Gbit/s; USB4 up to 40 Gbit/s; carries power; hot-pluggable; Type-C is the reversible connector |
| HDMI / DisplayPort | digital video and audio | monitors, TVs, projectors |
| SATA | serial | internal hard disks and SSDs (SATA III: 6 Gbit/s) |
| PCI Express and M.2 NVMe | serial lanes | graphics cards, fast SSDs |
| Ethernet (RJ-45) | network | wired LAN |
| Wi-Fi, Bluetooth, NFC | wireless | LAN, short-range devices, tap-to-pay |
| Audio jack, VGA (legacy), PS/2, parallel (legacy) | | older peripherals |

**Serial vs parallel transmission.** Parallel sends several bits at once on several wires (fast over short distances, but suffers skew and crosstalk); serial sends bits one after another on one wire pair and, at high clock rates, is now faster and cheaper (USB, SATA, PCIe). **Plug and Play** lets the OS detect and configure a new device automatically; **hot swapping** lets you connect it while the system is running. **Device drivers** are the software that lets the OS control a specific device.

## Formula and fact sheet

- 1 byte = 8 bits; 1 KiB = 1024 B; 1 MiB = 1024 KiB; 1 GiB = 1024 MiB; 1 TiB = 1024 GiB.
- Cycle time = 1 / f; CPU time = (instructions × CPI) / f.
- n address lines → 2ⁿ locations; frame size = width × height × bits per pixel / 8.
- Generations: vacuum tube → transistor → IC → microprocessor → ULSI/AI.
- Memory speed order: registers > cache > RAM > SSD > HDD > optical/tape.
- ALU computes, CU controls, registers hold, buses carry.
- SRAM (cache, flip-flop, fast) vs DRAM (main memory, capacitor, refresh).
- OCR = characters, OMR = marks, MICR = cheque ink, barcode = bars.
- Impact: dot-matrix; non-impact: inkjet, laser, thermal.

## Chapter summary

- A computer takes input, processes it under a stored program, stores data and produces output.
- Computers are classified by size, purpose and the kind of data they handle; five generations are marked by tube, transistor, IC, microprocessor and ULSI/AI.
- The CPU contains the ALU, control unit and registers; buses join CPU, memory and I/O.
- Instructions and data share one memory in the von Neumann design; the CPU repeats fetch–decode–execute–store.
- Memory is a hierarchy: speed and cost fall and capacity rises from registers to cache to RAM to disks and tape.
- RAM is volatile and read–write; ROM is non-volatile and holds start-up firmware; flash is erasable ROM.
- Input devices, output devices and interfaces (USB, HDMI, SATA, PCIe, wireless) connect the machine to the user.

## Practice

**A. Short questions**

1. Differentiate between data and information with an example.
2. List five characteristics of a computer.
3. Distinguish analog, digital and hybrid computers with one example of each.
4. State the functions of the ALU and the control unit.
5. What are registers? Name four.
6. Explain the fetch–decode–execute cycle.
7. Why is cache memory used?
8. Differentiate SRAM and DRAM.
9. Differentiate impact and non-impact printers with examples.
10. Differentiate OCR, OMR and MICR.

**B. Numerical problems**

11. A CPU at 2.5 GHz runs a program of 5 × 10⁹ instructions at 2 cycles per instruction. Find the execution time.
12. How many memory locations can a 20-bit address bus select? Express in KiB or MiB if each location holds one byte.
13. How many 700 MB files fit on a 1 TB disk (use 1 TB = 1024 × 1024 MB)?
14. An image is 800 × 600 pixels at 16 bits per pixel. Find its size in KB.

**C. Long questions**

15. Describe the anatomy of a digital computer with a block diagram description of its five units and three buses.
16. Explain the memory hierarchy and why it works.
17. Describe the classification of computers by size with examples.

::: note Answers and worked solutions
**1.** Data are raw facts such as `75`; information is processed data such as "average mark of the class is 62".
**2.** Speed, accuracy, diligence, versatility, storage (also automation).
**3.** Analog: speedometer; digital: laptop; hybrid: ICU monitor (analog body signals converted to digital processing).
**4.** ALU does arithmetic and logical operations; CU fetches, decodes and directs execution but computes nothing.
**5.** Very fast storage cells inside the CPU: PC, IR, MAR, MDR, accumulator.
**6.** See §1.7: fetch the instruction at the PC address, decode it, execute it, store the result, repeat.
**7.** Cache holds recently used data in fast SRAM close to the CPU, so most accesses avoid slow DRAM (locality of reference).
**8.** SRAM: flip-flops, fast, costly, no refresh, cache. DRAM: capacitors, slower, cheap, needs refresh, main memory.
**9.** Impact printers strike the paper (dot-matrix; can print carbon copies, noisy); non-impact use ink, toner or heat (inkjet, laser, thermal; quiet, better quality).
**10.** OCR reads printed characters, OMR reads filled marks (answer sheets), MICR reads magnetic-ink cheque characters.
**11.** Time = (5 × 10⁹ × 2) / (2.5 × 10⁹) = **4 s**.
**12.** 2²⁰ = 1,048,576 locations = **1 MiB**.
**13.** 1 TB = 1,048,576 MB; 1,048,576 / 700 = 1497.97, so **1497 files** (700 × 1498 = 1,048,600 would overflow the disk).
**14.** 800 × 600 = 480,000 pixels × 2 bytes = 960,000 bytes = 960,000 / 1024 = **937.5 KB**.
**15–17.** Model answers are in §1.6, §1.8 and §1.4 respectively; write the unit, the labelled list of parts and one example for each.
:::
