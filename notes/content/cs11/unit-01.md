---
subject: Computer Science
grade: 11
unit: 1
title: Computer System
hours: 20
---

A computer is not one machine but a *system* — a set of parts, each doing one
job, wired together so that data flows from input, through processing, to output,
while instructions and results sit in memory. This unit takes the system apart:
first the history and the classification, then the architecture, then every
physical component you will be asked to name, compare and describe. At 20 teaching
hours it is the largest unit in Grade 11 Computer Science and it supplies more
exam marks than any other.

::: key What the examiner wants from this unit
Almost every question is one of four shapes: **define and list characteristics**,
**compare two things in a table**, **draw and explain the block diagram**, or a
small **numerical** on storage capacity or speed. Learn the block diagram until
you can draw it from memory, and memorise the storage-unit ladder.
:::

## 1.1 Definition, characteristics and application of computer

::: definition Computer
A computer is an electronic device that accepts data as input, processes it
according to a stored set of instructions (a program), stores the data and
results, and produces meaningful information as output.

The word comes from the Latin *computare*, "to calculate", but a modern computer
is a general-purpose **data processor**, not merely a calculator.
:::

The processing cycle is usually written as the **IPO cycle** — Input → Process →
Output — with **Storage** added as a fourth stage, giving **IPO-S**.

**Characteristics.**

| Characteristic | What it means |
|---|---|
| Speed | Operations are measured in millions or billions per second; internal events take nanoseconds |
| Accuracy | Errors come from wrong data or a wrong program, not from the machine — **GIGO**: Garbage In, Garbage Out |
| Diligence | It does not tire, get bored or lose concentration; the millionth calculation is as good as the first |
| Versatility | The same hardware runs a spreadsheet, a game and a weather model — only the program changes |
| Storage capacity | Terabytes of data can be held and retrieved in a fraction of a second |
| Automation | Once started, a program runs to completion without human help |
| Reliability | Consistent results over long periods with very low failure rates |
| No IQ / No feeling | It has no intelligence of its own; it obeys instructions literally |

**Applications.** Education (e-learning, NEB result publication), banking (ATMs,
mobile banking, cheque clearing), business (billing, inventory, payroll),
government (national ID, Loksewa and NEB result processing, land records),
health (CT and MRI imaging, hospital records), engineering (CAD/CAM),
communication (email, VoIP, social media), entertainment (games, animation),
science (weather forecasting by the Department of Hydrology and Meteorology,
earthquake modelling) and transport (online ticketing, air-traffic control).

## 1.2 Evolution of computer technology (generations)

Before electronics, calculation was mechanical: the **abacus** (about 3000 BC),
Napier's Bones (1617), Pascal's **Pascaline** (1642), Leibniz's stepped reckoner
(1671), Jacquard's punched-card loom (1801) and Charles **Babbage's** Difference
Engine (1822) and Analytical Engine (1833). Because the Analytical Engine already
had a mill, a store, input and output, Babbage is called the **Father of
Computer**, and **Ada Lovelace**, who wrote its algorithms, the first programmer.
Herman Hollerith's punched-card tabulator (1890) led to the company that became
IBM.

Electronic computers are grouped into five **generations**, each defined by the
switching technology it uses.

```figure caption="The five generations of computers: each is defined by the switching device inside it, and each step shrinks size and cost while raising speed."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.1,3.0))
gens = [("1st","1946-58","Vacuum\ntube","ENIAC\nUNIVAC-I"),
        ("2nd","1959-64","Transistor","IBM 1401\nCDC 1604"),
        ("3rd","1965-70","Integrated\ncircuit","IBM 360\nPDP-8"),
        ("4th","1971-now","Micro-\nprocessor","Intel 4004\nIBM PC"),
        ("5th","emerging","ULSI, AI,\nparallel","AI, quantum\nexascale")]
x = np.arange(5)*1.20
for i,(g,yr,tech,ex) in enumerate(gens):
    c = SERIES[i]
    ax.add_patch(FancyBboxPatch((x[i]-0.52,0.46),1.04,1.60,
        boxstyle="round,pad=0.02,rounding_size=0.06", fc=c, ec='none', alpha=0.12, zorder=1))
    ax.text(x[i],1.92,g,ha='center',va='top',fontsize=9.0,color=c,fontweight='bold')
    ax.text(x[i],1.60,yr,ha='center',va='top',fontsize=7.2,color=INK)
    ax.text(x[i],1.36,tech,ha='center',va='top',fontsize=7.6,color=c,fontweight='bold')
    ax.text(x[i],0.86,ex,ha='center',va='top',fontsize=6.8,color=MUTED)
    ax.plot([x[i]],[0.26],'o',ms=7,color=c,zorder=3)
ax.plot([x[0]-0.62,x[-1]+0.62],[0.26,0.26], color=MUTED, lw=1.3, zorder=1)
ax.annotate('', xy=(x[-1]+0.62,-0.16), xytext=(x[0]-0.62,-0.16),
    arrowprops=dict(arrowstyle='-|>',color=ACCENT,lw=1.3,mutation_scale=12))
ax.text(x[2],-0.28,'smaller  •  cheaper  •  faster  •  more reliable',
        ha='center',va='top',fontsize=7.8,color=ACCENT)
ax.set_xlim(x[0]-0.80, x[-1]+0.80); ax.set_ylim(-0.62,2.08); ax.axis('off')
ax.set_aspect('equal')
```

| Generation | Switching device | Memory | Language | Typical speed |
|---|---|---|---|---|
| First | Vacuum tube | Magnetic drum | Machine (binary) | milliseconds |
| Second | Transistor | Magnetic core | Assembly, early FORTRAN/COBOL | microseconds |
| Third | Integrated circuit (SSI/MSI) | Magnetic core, early semiconductor | High-level, OS with multiprogramming | nanoseconds |
| Fourth | Microprocessor (LSI/VLSI) | Semiconductor RAM | 3GL, 4GL, GUI | nanoseconds |
| Fifth | ULSI, parallel and AI processors | Very large semiconductor, optical | Natural language, AI | picoseconds |

The fourth generation begins with the **Intel 4004** (1971) — the first
microprocessor, a 4-bit chip of about 2,300 transistors clocked at roughly
740 kHz. The IBM PC of 1981 used the 16-bit Intel 8088.

::: memory Vacuum-Transistor-IC-Microprocessor-AI
"**V**ery **T**all **I**ndians **M**ake **A**rt" — Vacuum tube, Transistor,
Integrated circuit, Microprocessor, AI. The five generations in order.
:::

## 1.3 Measurement unit of processing speed and storage unit

**Speed.** Two different things are measured, and students mix them up.

| Quantity | Unit | Meaning |
|---|---|---|
| Clock frequency | hertz (Hz), MHz, GHz | clock pulses per second; $1\ \text{GHz} = 10^{9}$ cycles s⁻¹ |
| Cycle / access time | ms, μs, ns, ps | time for one cycle or one memory access |
| Instruction rate | MIPS | millions of instructions per second |
| Arithmetic rate | FLOPS, GFLOPS, TFLOPS, PFLOPS, EFLOPS | floating-point operations per second |

$$ 1\ \text{ms} = 10^{-3}\,\text{s},\quad 1\ \mu\text{s} = 10^{-6}\,\text{s},
\quad 1\ \text{ns} = 10^{-9}\,\text{s},\quad 1\ \text{ps} = 10^{-12}\,\text{s} $$

Clock period and frequency are reciprocals: $T = 1/f$. A 3.2 GHz processor has a
clock period of $1/(3.2\times10^{9}) = 0.3125$ ns.

**Storage.** The smallest unit is the **bit** (binary digit, 0 or 1). Four bits
make a **nibble**, eight bits a **byte** — one byte stores one character in ASCII.

::: memory The storage ladder
$$ 8\ \text{bit} = 1\ \text{byte},\qquad 1024\ \text{byte} = 1\ \text{KB} $$

KB → MB → GB → TB → PB → EB → ZB → YB, each step $\times 1024 = \times 2^{10}$.
"**K**ings **M**ake **G**ood **T**ea **P**ots **E**very **Z**ero **Y**ear."
(In 2022 the BIPM added two more: **RB** ronnabyte and **QB** quettabyte.)
:::

| Unit | Symbol | Binary value | Approximate size |
|---|---|---|---|
| Kilobyte | KB | $2^{10}$ = 1,024 B | half a page of text |
| Megabyte | MB | $2^{20}$ B | a 3-minute MP3 song ≈ 3 MB |
| Gigabyte | GB | $2^{30}$ B | a 2-hour HD film ≈ 4 GB |
| Terabyte | TB | $2^{40}$ B | a typical 2026 laptop hard disk |
| Petabyte | PB | $2^{50}$ B | a large national data centre |
| Exabyte | EB | $2^{60}$ B | global internet traffic in a few hours |

::: caution 1 GB on the box is not 1 GB in Windows
Disk makers use the decimal SI prefix, $1\ \text{GB} = 10^{9}$ bytes, while the
operating system reports binary units, $2^{30} = 1{,}073{,}741{,}824$ bytes. A
"500 GB" disk therefore shows as about 465 GB. The IEC names for the binary units
are **KiB, MiB, GiB** (kibibyte, mebibyte, gibibyte). In NEB answers use
$1\ \text{KB} = 1024\ \text{B}$ unless the question says otherwise.
:::

::: example Worked example 1.1
**Problem.** A 64 GB memory card is used in a camera that produces 6 MB photos
and 1080p video at 24 Mbps. (a) How many photos fit? (b) How many minutes of
video fit, if the card is empty? Take $1\ \text{GB}=1024\ \text{MB}$.

**Solution.**
(a) Capacity $= 64 \times 1024 = 65{,}536\ \text{MB}$.

$$ n = \frac{65536}{6} = 10{,}922.7 \Rightarrow 10{,}922\ \text{photos} $$

(b) Video rate $= 24\ \text{Mbps} = 24/8 = 3\ \text{MB s}^{-1}$.

$$ t = \frac{65536\ \text{MB}}{3\ \text{MB s}^{-1}} = 21{,}845\ \text{s}
= 364.1\ \text{minutes} \approx 6\ \text{hours} $$
:::

## 1.4 Super, Mainframe, Mini and Microcomputers

Digital computers are classified by size, processing power and cost.

| Type | Processing power | Users at once | Typical use | Example |
|---|---|---|---|---|
| Supercomputer | Fastest; measured in PFLOPS/EFLOPS | few, batch jobs | weather modelling, nuclear simulation, genome research | El Capitan, Frontier, Fugaku |
| Mainframe | Very high throughput, huge I/O | thousands of terminals | bank core systems, census, airline reservation | IBM z-series |
| Minicomputer (midrange) | Medium | tens to hundreds | departmental servers, process control | PDP-11, IBM AS/400 |
| Microcomputer | One microprocessor | usually one | desktop, laptop, tablet, smartphone | PC, MacBook, smartphone |

A **supercomputer** gets its speed from massive parallelism, not from one very
fast processor. As of the November 2025 TOP500 list, the fastest machine in the
world was **El Capitan** at Lawrence Livermore National Laboratory, USA, rated at
**1.809 exaFLOPS** (about $1.8\times10^{18}$ floating-point operations per
second) on the LINPACK benchmark, using more than 11 million processor cores.

A **mainframe** is optimised for *throughput and reliability* rather than raw
arithmetic: it moves enormous volumes of transactions with near-continuous
uptime, which is why banks and airlines still use them.

Microcomputers are further divided into **desktop, laptop, notebook, netbook,
tablet, palmtop/PDA, smartphone** and **workstation** (a high-end single-user
machine for CAD or video editing).

## 1.5 Mobile Computing and its Application

::: definition Mobile computing
Mobile computing is the use of portable computing devices that can transmit and
receive data over a wireless network while the user is moving, so that computing
is not tied to a fixed location.
:::

It rests on three legs: **mobile hardware** (smartphone, tablet, laptop,
wearable), **mobile software** (mobile OS and apps) and **mobile communication**
(Wi-Fi, Bluetooth, 4G LTE, 5G, NFC, GPS, satellite).

**Applications.** Mobile banking and digital wallets (eSewa, Khalti, ConnectIPS
and fonepay QR payments in Nepal); m-commerce; m-learning; telemedicine and
tele-consultation in remote districts; GPS navigation and ride hailing
(Pathao, InDrive); field data collection for the census and for disaster
response; agriculture advisories by SMS; and mobile ticketing.

**Advantages** — mobility, immediate access, location awareness, lower
infrastructure cost. **Limitations** — limited battery, small screen, weaker
processing and storage, dependence on network coverage, and greater security and
privacy risk.

## 1.6 Concept of computer architecture and organization

These two terms are examined together almost every year because they are easy to
confuse.

::: definition Architecture and organization
**Computer architecture** is the *functional behaviour* of a computer as seen by
a programmer — instruction set, data types, word length, addressing modes,
registers and I/O mechanisms. It answers **what** the machine does.

**Computer organization** is the *operational implementation* — the control
signals, the interfaces, the memory technology and how the units are physically
interconnected. It answers **how** it is built.
:::

| Architecture | Organization |
|---|---|
| Logical / functional view | Physical / implementation view |
| Visible to the programmer | Transparent to the programmer |
| Decided first, changes rarely | Decided later, changes with each model |
| Instruction set, word size, addressing modes | Control signals, bus widths, memory chips used |
| e.g. "the x86-64 instruction set" | e.g. "how L2 cache is wired in this particular CPU" |

Two classical architectures appear in the syllabus:

- **Von Neumann (stored-program) architecture** — one memory holds both
  instructions and data, and one bus carries both. Simple and cheap, but the
  single path between CPU and memory limits speed; this is the *von Neumann
  bottleneck*. Almost all general-purpose computers use it.
- **Harvard architecture** — separate memories and separate buses for
  instructions and data, so both can be fetched at once. Used in microcontrollers
  and in DSP chips, and inside modern CPUs at the cache level (separate
  instruction and data L1 caches — a "modified Harvard" design).

## 1.7 Components of computer system: input, output, processing, memory and storage

A computer system = **hardware + software + data + people (liveware) +
procedures**. The hardware is organised into five functional units.

```figure caption="Block diagram of a computer system. Solid blue arrows are data and instruction paths; dashed red arrows are control signals issued by the control unit."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.1,3.95))
RED = '#A8271F'
def box(x0,y0,x1,y1,label,fs=8.6,fc='none',ec=INK,lw=1.3,bold=False,alpha=1.0):
    ax.add_patch(FancyBboxPatch((x0,y0),x1-x0,y1-y0,
        boxstyle="round,pad=0.02,rounding_size=0.08", fc=fc, ec=ec, lw=lw,
        alpha=alpha, zorder=3))
    ax.text((x0+x1)/2,(y0+y1)/2,label,ha='center',va='center',fontsize=fs,
            color=INK, zorder=4, fontweight='bold' if bold else 'normal')
def arw(p,q,c=ACCENT,ls='-',lw=1.4,both=False):
    ax.annotate('', xy=q, xytext=p, zorder=2,
        arrowprops=dict(arrowstyle='<|-|>' if both else '-|>', color=c, lw=lw,
                        linestyle=ls, shrinkA=0, shrinkB=0, mutation_scale=11))
def rail(pts,c=RED,lw=1.15):
    ax.plot([p[0] for p in pts],[p[1] for p in pts],color=c,lw=lw,
            ls=(0,(4,2)),zorder=2,solid_capstyle='round')
DASH=(0,(4,2))
box(2.30,0.45,4.60,3.15,'', fc=ACCENT, ec=ACCENT, lw=1.1, alpha=0.07)
ax.text(2.30,3.22,'CPU',ha='left',va='bottom',fontsize=9.2,color=ACCENT,fontweight='bold')
box(2.45,2.35,4.45,3.00,'Control Unit (CU)',fs=8.4)
box(2.45,1.40,4.45,2.10,'Arithmetic & Logic\nUnit (ALU)',fs=8.0)
box(2.45,0.60,4.45,1.15,'Registers',fs=8.4)
box(0.35,1.40,1.75,2.10,'INPUT\nunit',bold=True)
box(5.45,1.40,6.85,2.10,'OUTPUT\nunit',bold=True)
box(2.30,3.62,4.60,4.20,'Primary memory\n(RAM / ROM)',fs=8.0)
box(2.30,-0.65,4.60,-0.07,'Secondary storage\n(HDD / SSD / optical)',fs=7.6)
# ---- data paths (blue) ----
arw((1.75,1.75),(2.45,1.75))
arw((4.45,1.75),(5.45,1.75))
arw((3.05,3.15),(3.05,3.62),both=True)
arw((3.05,0.45),(3.05,-0.07),both=True)
# ---- control paths (red dashed) ----
rail([(2.45,2.68),(1.05,2.68),(1.05,2.22)]); arw((1.05,2.22),(1.05,2.10),RED,DASH,1.15)
rail([(4.45,2.68),(6.15,2.68),(6.15,2.22)]); arw((6.15,2.22),(6.15,2.10),RED,DASH,1.15)
arw((3.85,3.00),(3.85,3.62),RED,DASH,1.15)
arw((3.85,2.35),(3.85,2.10),RED,DASH,1.15)
rail([(4.45,2.50),(4.95,2.50),(4.95,-0.36),(4.75,-0.36)])
arw((4.75,-0.36),(4.60,-0.36),RED,DASH,1.15)
rail([(2.45,2.50),(2.00,2.50),(2.00,0.88),(2.30,0.88)])
arw((2.30,0.88),(2.45,0.88),RED,DASH,1.15)
# ---- legend ----
ax.plot([0.35,0.95],[-1.10,-1.10],color=ACCENT,lw=1.4)
ax.text(1.05,-1.10,'data / instruction path',va='center',fontsize=7.8,color=INK)
ax.plot([3.55,4.15],[-1.10,-1.10],color=RED,lw=1.15,ls=DASH)
ax.text(4.25,-1.10,'control signal',va='center',fontsize=7.8,color=INK)
ax.set_xlim(-0.05,7.05); ax.set_ylim(-1.45,4.45)
ax.set_aspect('equal'); ax.axis('off')
```

1. **Input unit** — converts data from a human-readable form into binary and
   feeds it to the CPU.
2. **Central Processing Unit (CPU)** — the "brain". It contains:
   - the **Control Unit (CU)**, which fetches instructions, decodes them and
     generates the control signals that direct every other unit (it does not do
     any arithmetic itself);
   - the **Arithmetic and Logic Unit (ALU)**, which performs arithmetic (+, −,
     ×, ÷) and logic (AND, OR, NOT, comparison) operations;
   - **registers**, small very fast stores inside the CPU that hold the data
     being worked on right now.
3. **Memory unit (primary memory)** — holds the program and data currently in
   use; directly addressable by the CPU.
4. **Storage (secondary memory)** — keeps data permanently; not directly
   accessible by the CPU, data must be copied to RAM first.
5. **Output unit** — converts binary results back into human-readable form.

The CU and ALU together with registers form the CPU; the CPU and primary memory
together are sometimes called the **main unit** or system unit.

## 1.8 Microprocessor: basic concepts, clock speed, word length, components and functions

::: definition Microprocessor
A microprocessor is a single integrated-circuit chip that contains the complete
central processing unit — control unit, arithmetic and logic unit and registers —
of a computer. It is fabricated using VLSI/ULSI technology.
:::

**Components and their functions.**

| Component | Function |
|---|---|
| ALU | arithmetic and logical operations |
| Control unit | decodes instructions, generates timing and control signals |
| Register array | temporary high-speed storage (accumulator, PC, MAR, MDR/MBR, IR, general registers) |
| Clock / timing circuit | synchronises every operation |
| Cache (L1, L2, L3) | keeps recently used instructions and data close to the cores |
| Bus interface unit | connects the chip to the external address, data and control buses |

**Key registers.** Program Counter (PC) holds the address of the next
instruction; Memory Address Register (MAR) holds the address being accessed;
Memory Data Register (MDR) holds the word in transit; Instruction Register (IR)
holds the instruction being decoded; the Accumulator (A) holds ALU results.

**Clock speed** is the number of clock pulses per second, in MHz or GHz. Each
instruction takes a whole number of clock cycles, so — for one given design — a
higher clock means more instructions per second. Typical desktop processors in
2026 run at a base clock of 3–4 GHz with boost clocks above 5 GHz.

**Word length** is the number of bits the CPU can fetch, store and process as a
single unit — 8, 16, 32 or 64 bits on real machines. A longer word means more
precision, larger directly-addressable memory and greater speed. A 32-bit
processor can address $2^{32} = 4\ \text{GB}$ of memory; a 64-bit processor can
in principle address $2^{64}$ bytes, which is 16 exabytes.

::: example Worked example 1.2
**Problem.** A microprocessor has a clock speed of 2.5 GHz. An instruction needs
5 clock cycles. Find (a) the clock period, (b) the time to execute one
instruction, and (c) the number of instructions executed per second in MIPS.

**Solution.**
(a) $T = \dfrac{1}{f} = \dfrac{1}{2.5\times10^{9}} = 4\times10^{-10}\ \text{s} = 0.4\ \text{ns}$

(b) $t_{instr} = 5 \times 0.4\ \text{ns} = 2\ \text{ns}$

(c) Instructions per second $= \dfrac{1}{2\times10^{-9}} = 5\times10^{8}$, i.e.
$\dfrac{5\times10^{8}}{10^{6}} = 500\ \text{MIPS}$.
:::

::: caution Clock speed alone does not decide performance
A 2 GHz processor can beat a 3 GHz one if it has more cores, a wider word, a
bigger cache or a better instruction set. Never say "the higher the GHz, the
faster the computer" without adding "for processors of the same design".
:::

## 1.9 Bus System: data bus, address bus and control bus

::: definition Bus
A bus is a group of parallel conducting lines that carries bits between the
components of a computer. The number of lines is the **width** of the bus.
:::

```figure caption="The system bus. The address bus is unidirectional (CPU out only); the data bus is bidirectional; the control bus carries individual timing and command signals."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.1,3.0))
RED = '#A8271F'; GRN = '#2e8b57'
BOT = 2.45
for i,lbl in enumerate(['CPU','Main\nmemory','Input /\nOutput']):
    x0 = 0.30+i*1.85
    ax.add_patch(FancyBboxPatch((x0,BOT),1.45,0.85,
        boxstyle="round,pad=0.02,rounding_size=0.08", fc='none', ec=INK, lw=1.3, zorder=3))
    ax.text(x0+0.725,BOT+0.425,lbl,ha='center',va='center',fontsize=8.6,color=INK,zorder=4)
lanes = [(1.90,'Address bus',ACCENT,-0.30,'out'),
         (1.25,'Data bus',    GRN,   0.00,'bi'),
         (0.60,'Control bus', RED,   0.30,'out')]
for y,name,c,dx,kind in lanes:
    ax.plot([0.10,5.75],[y,y],color=c,lw=2.4,solid_capstyle='round',zorder=2)
    ax.text(5.88,y,name,va='center',fontsize=8.4,color=c)
    for i in range(3):
        cx = 0.30+i*1.85+0.725+dx
        if kind=='bi':
            style='<|-|>'
        else:
            style='-|>'
        if kind=='bi' or i==0:
            p,q = (cx,BOT),(cx,y)          # CPU drives out / data both ways
        else:
            p,q = (cx,y),(cx,BOT)          # into memory and I/O
        ax.annotate('', xy=q, xytext=p, zorder=4,
            arrowprops=dict(arrowstyle=style, color=c, lw=1.15,
                            shrinkA=0, shrinkB=0, mutation_scale=10))
ax.text(2.9,0.16,'$n$ address lines  ⇒  $2^{n}$ addressable locations',
        ha='center',va='top',fontsize=8.4,color=MUTED)
ax.set_xlim(0.0,7.7); ax.set_ylim(-0.30,3.45); ax.set_aspect('equal'); ax.axis('off')
```

| Bus | Direction | Carries | Width decides |
|---|---|---|---|
| **Address bus** | unidirectional (CPU → memory/IO) | the address of the location to be read or written | how much memory can be addressed: $2^{n}$ locations |
| **Data bus** | bidirectional | the actual data or instruction word | how many bits move per transfer (usually = word length) |
| **Control bus** | bidirectional (individual lines) | READ, WRITE, CLOCK, RESET, INTERRUPT, memory/IO select, bus request/grant | timing and coordination |

::: example Worked example 1.3
**Problem.** A processor has a 24-bit address bus and a 16-bit data bus. Find
(a) the maximum memory it can address, and (b) the total memory in bytes if each
addressable location stores one word.

**Solution.**
(a) Number of locations $= 2^{24} = 16{,}777{,}216 = 16\ \text{M}$ locations.

(b) Each word is 16 bits = 2 bytes, so

$$ 16\ \text{M} \times 2\ \text{B} = 32\ \text{MB} $$
:::

## 1.10 Primary memory: RAM, ROM, Cache, Buffer

**Primary (main) memory** is semiconductor memory that the CPU can address
directly. It is fast, expensive per byte, and small compared with storage.

```figure caption="The memory hierarchy. Moving down, capacity and cost per byte improve while speed falls by roughly a factor of ten at each step."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon
fig, ax = plt.subplots(figsize=(5.1,3.2))
levels = [("Registers","< 1 KB","0.3 ns"),
          ("L1 / L2 / L3 cache","32 KB - 64 MB","1-20 ns"),
          ("Main memory (RAM)","4 - 64 GB","50-90 ns"),
          ("SSD (flash)","256 GB - 8 TB","20-100 μs"),
          ("Hard disk / optical","1 - 36 TB","5-12 ms"),
          ("Tape, cloud archive","petabytes","seconds")]
n=len(levels); H=0.52; topw=1.05; botw=4.10
for i,(name,cap,spd) in enumerate(levels):
    y0 = (n-1-i)*H
    w0 = topw + (botw-topw)*(i/n); w1 = topw + (botw-topw)*((i+1)/n)
    ax.add_patch(Polygon([(-w0/2,y0+H),(w0/2,y0+H),(w1/2,y0),(-w1/2,y0)],
                 closed=True, fc=SERIES[i%6], ec='white', lw=1.1, alpha=0.22, zorder=2))
    ax.text(0,y0+H/2,name,ha='center',va='center',fontsize=8.2,color=INK,zorder=3)
    ax.text(botw/2+0.28,y0+H/2,cap,ha='left',va='center',fontsize=7.6,color=MUTED)
    ax.text(-botw/2-0.28,y0+H/2,spd,ha='right',va='center',fontsize=7.6,color=MUTED)
ax.text(-botw/2-0.28,n*H+0.10,'access time',ha='right',va='bottom',fontsize=7.8,color=INK)
ax.text( botw/2+0.28,n*H+0.10,'capacity',ha='left',va='bottom',fontsize=7.8,color=INK)
ax.annotate('',xy=(-4.55,0.05),xytext=(-4.55,n*H-0.05),
            arrowprops=dict(arrowstyle='-|>',color=ACCENT,lw=1.3,mutation_scale=11))
ax.text(-4.70,n*H/2,'slower',rotation=90,ha='right',va='center',fontsize=8.2,color=ACCENT)
ax.annotate('',xy=(4.55,0.05),xytext=(4.55,n*H-0.05),
            arrowprops=dict(arrowstyle='-|>',color='#2e8b57',lw=1.3,mutation_scale=11))
ax.text(4.70,n*H/2,'bigger, cheaper per byte',rotation=270,ha='left',va='center',
        fontsize=8.0,color='#2e8b57')
ax.set_xlim(-5.45,5.95); ax.set_ylim(-0.15,n*H+0.48); ax.axis('off')
```

**RAM (Random Access Memory)** is read/write, **volatile** (contents lost when
power goes off) and used as working memory. "Random access" means any location
takes the same time to reach, unlike tape.

| | SRAM | DRAM |
|---|---|---|
| Storage cell | flip-flop (4–6 transistors) | one transistor + one capacitor |
| Refresh needed | no | yes, thousands of times per second |
| Speed | very fast | slower |
| Cost and density | expensive, low density | cheap, high density |
| Power | higher (static) | lower per bit |
| Used as | cache memory | main memory |

DRAM has evolved SDRAM → DDR → DDR2 → DDR3 → DDR4 → **DDR5**, which is the
standard for new PCs in 2026 with module speeds commonly from 4800 to about
8000 MT/s.

**ROM (Read Only Memory)** is **non-volatile** and holds firmware — the BIOS/UEFI
that starts the machine (the **bootstrap** program), and the control programs of
embedded devices.

| ROM type | Written by | Erasable? |
|---|---|---|
| MROM (Masked ROM) | the manufacturer, during fabrication | no |
| PROM (Programmable ROM) | the user, once, with a PROM burner | no |
| EPROM (Erasable PROM) | the user | yes — ultraviolet light through a quartz window, whole chip |
| EEPROM (Electrically Erasable PROM) | the user | yes — electrically, byte by byte |
| Flash ROM | the user | yes — electrically, in blocks; fast; used for BIOS and pen drives |

**Cache memory** is a small, very fast SRAM between the CPU and main memory that
holds recently and frequently used instructions and data. When the CPU finds what
it wants in cache that is a **hit**, otherwise a **miss**. Levels: **L1** (on
each core, smallest, fastest), **L2** (per core, larger), **L3** (shared by all
cores). Cache works because of *locality of reference*.

**Buffer** is a temporary holding area in RAM (or inside a device) that
compensates for the difference in speed between two units — for example a print
buffer lets the CPU dump a document and carry on while the slow printer prints,
and a video buffer stores the next few seconds of a stream.

::: caution Cache is not buffer
Cache speeds up *repeated* access to the same data and is managed by hardware;
a buffer *matches speeds* between a fast and a slow device and is usually managed
by software. Both are temporary, but they solve different problems.
:::

## 1.11 Secondary Memory: Magnetic Disk, Flash Memory, Optical Disk, External Storage

Secondary memory is non-volatile, large, cheap per byte and **not** directly
addressable by the CPU.

```figure caption="Surface geometry of a magnetic (hard) disk: concentric tracks divided into sectors, and the read/write head on its access arm. Aligned tracks on all platters form a cylinder."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge, Rectangle
fig, ax = plt.subplots(figsize=(5.1,2.9))
# platter
cx,cy = 0.0,0.0
ax.add_patch(Circle((cx,cy),1.55,fc=GRID,ec=MUTED,lw=1.1,alpha=0.45,zorder=1))
for r in [1.40,1.18,0.96,0.74,0.52]:
    ax.add_patch(Circle((cx,cy),r,fc='none',ec=MUTED,lw=0.8,zorder=2))
ax.add_patch(Circle((cx,cy),0.30,fc='white',ec=MUTED,lw=1.0,zorder=3))
for a in range(0,360,30):
    t=np.radians(a)
    ax.plot([0.30*np.cos(t),1.55*np.cos(t)],[0.30*np.sin(t),1.55*np.sin(t)],
            color=MUTED,lw=0.6,zorder=2)
ax.add_patch(Wedge((cx,cy),1.18,60,90,width=0.22,fc=ACCENT,alpha=0.45,ec=ACCENT,lw=0.9,zorder=4))
ax.annotate('sector',xy=(0.45,0.95),xytext=(1.10,2.00),fontsize=8.3,color=ACCENT,
            arrowprops=dict(arrowstyle='-|>',color=ACCENT,lw=1.0,mutation_scale=9))
ax.annotate('track',xy=(-1.29,0.0),xytext=(-2.85,0.95),fontsize=8.3,color=INK,
            arrowprops=dict(arrowstyle='-|>',color=INK,lw=1.0,mutation_scale=9))
ax.annotate('spindle',xy=(0.0,-0.22),xytext=(-1.35,-1.95),fontsize=8.3,color=INK,
            arrowprops=dict(arrowstyle='-|>',color=INK,lw=1.0,mutation_scale=9))
# arm + head
ax.plot([3.05,0.55],[ -1.05,-0.55],color=INK,lw=2.4,solid_capstyle='round',zorder=5)
ax.add_patch(Circle((0.50,-0.54),0.11,fc='#A8271F',ec='#A8271F',zorder=6))
ax.annotate('read/write head',xy=(0.50,-0.54),xytext=(1.45,-1.95),fontsize=8.3,color='#A8271F',
            arrowprops=dict(arrowstyle='-|>',color='#A8271F',lw=1.0,mutation_scale=9))
ax.text(3.15,-1.05,'access\narm',fontsize=8.3,color=INK,va='center')
# side view
ax.plot([4.70,4.70],[-1.10,1.55],color=MUTED,lw=2.0)
for k,yy in enumerate([1.20,0.55,-0.10,-0.75]):
    ax.add_patch(Rectangle((3.95,yy),1.50,0.10,fc=GRID,ec=MUTED,lw=0.8))
ax.plot([5.22,5.22],[-0.75,1.30],color='#A8271F',lw=1.3,ls=(0,(3,2)))
ax.text(5.32,0.30,'cylinder',fontsize=8.3,color='#A8271F',va='center')
ax.text(4.70,1.80,'platters (side view)',fontsize=8.0,color=MUTED,ha='center')
ax.set_xlim(-3.3,6.6); ax.set_ylim(-2.35,2.35); ax.set_aspect('equal'); ax.axis('off')
```

**Magnetic disk.** A hard disk drive (HDD) stores bits as magnetised spots on
rotating aluminium or glass **platters** coated with magnetic material. Each
surface is divided into concentric **tracks**, each track into **sectors**
(traditionally 512 bytes, now usually 4096 bytes in Advanced Format). Tracks at
the same radius on all surfaces make a **cylinder**. Access time = seek time +
rotational latency + transfer time. Drives spin at 5400, 7200, 10000 or
15000 rpm. In 2026 desktop HDDs of 1–8 TB are ordinary and data-centre drives
using HAMR technology reach 30–36 TB, with 40 TB+ models shipping to hyperscale
customers. Magnetic tape is still used for cheap archival backup.

**Flash memory** is EEPROM-based solid-state storage with no moving parts: pen
drives, memory cards (SD, microSD) and **SSDs**. It is fast, silent, shock-proof
and low-power, but has a limited number of write cycles and costs more per
gigabyte than an HDD. Consumer SSDs run to 8 TB (M.2 NVMe); enterprise flash
drives of about 245 TB exist as of 2026.

**Optical disk.** Data is written as microscopic **pits** and **lands** along one
long spiral track, read by reflecting a laser beam off the surface.

| Disk | Laser | Capacity | Notes |
|---|---|---|---|
| CD-ROM / CD-R / CD-RW | infrared, 780 nm | 700 MB | audio and small data |
| DVD | red, 650 nm | 4.7 GB single layer, 8.5 GB dual layer | film, software |
| Blu-ray (BD) | blue-violet, 405 nm | 25 GB single layer, 50 GB dual layer | HD video |
| BDXL | blue-violet | 100 GB / 128 GB | archival |

**External storage devices** connect through a port rather than sitting inside
the case: external HDD and SSD (USB or Thunderbolt), pen drive, memory card,
network attached storage (NAS) and cloud storage (Google Drive, OneDrive).

```figure caption="Typical capacities of storage media, on a logarithmic scale — each grid step is a factor of ten. Figures are the common maximum for each medium as of 2026."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.1,2.9))
names = ['Floppy\n(1.44 MB)','CD\n(700 MB)','DVD-DL\n(8.5 GB)','Blu-ray\n(25 GB)',
         'BDXL\n(100 GB)','Pen drive\n(1 TB)','SSD M.2\n(8 TB)','HDD\n(36 TB)']
vals  = [1.44e6, 700e6, 8.5e9, 25e9, 100e9, 1e12, 8e12, 36e12]
cols  = [MUTED,MUTED,SERIES[0],SERIES[0],SERIES[0],SERIES[2],SERIES[2],SERIES[1]]
ax.bar(range(len(vals)), vals, color=cols, width=0.62, alpha=0.85)
ax.set_yscale('log')
ax.set_xticks(range(len(vals))); ax.set_xticklabels(names, fontsize=7.2)
ax.set_ylabel('capacity (bytes, log scale)')
ax.set_ylim(1e6, 3e14)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, axis='y', alpha=.55)
```

## 1.12 Input Devices

::: definition Input device
An input device is a peripheral that accepts data and instructions from the
outside world and converts them into the binary form the computer can process.
:::

| Device | How it works | Typical use |
|---|---|---|
| **Keyboard** | each key closes a switch; the keyboard controller sends a scan code | text entry; QWERTY layout, 104 keys |
| **Mouse** | optical sensor or ball tracks movement; pointing device | GUI pointing, drag and drop |
| **Scanner** | a light source and CCD/CIS sensor digitise a page into an image (measured in dpi) | copying documents and photographs |
| **Light pen** | a photodetector in a pen senses the screen and reports position | drawing directly on the screen, CAD |
| **OMR** (Optical Mark Reader) | detects the presence of pencil marks in fixed positions by reflected light | multiple-choice answer sheets, Loksewa and entrance exams |
| **OCR** (Optical Character Recognition) | software recognises the *shapes* of printed or written characters and converts them to editable text | digitising books and forms |
| **BCR** (Bar Code Reader) | a laser scans the bar pattern; reflected light gives a digit string (e.g. EAN-13) | supermarket billing, library, inventory |
| **MICR** (Magnetic Ink Character Recognition) | reads characters printed in magnetic ink in the E-13B font | bank cheque clearing, used by Nepali banks |
| **Touch screen** | resistive or capacitive layer detects the position of a finger | ATMs, smartphones, kiosks, POS |
| **Microphone** | a transducer turns sound pressure into an electrical signal, digitised by the sound card | voice input, recording, online class |
| **Digital camera / webcam** | a lens focuses light onto a CCD/CMOS sensor; resolution in megapixels | photographs, video conferencing |

Other input devices worth naming: joystick, trackball, graphics tablet,
biometric (fingerprint, iris) scanner, QR code reader, and sensors of all kinds.

::: caution OMR, OCR, MICR and BCR
OMR reads **marks** (is the bubble filled?), OCR reads **shapes of characters**,
MICR reads **magnetic ink characters**, BCR reads **bars**. Exam questions almost
always ask you to distinguish OMR from OCR — the key word is *mark* versus
*character*.
:::

## 1.13 Output Devices

Output is either **soft copy** (temporary — screen, sound) or **hard copy**
(permanent — paper).

**Monitor.** The Visual Display Unit. Quality is described by **resolution**
(pixels, e.g. HD 1366×768, Full HD 1920×1080, 4K UHD 3840×2160), **refresh rate**
(Hz), **dot pitch** and **colour depth**.

| | LCD | LED | OLED |
|---|---|---|---|
| Backlight | cold cathode fluorescent lamp (CCFL) | light-emitting diodes | none — each pixel emits its own light |
| Thickness | thicker | thin | thinnest |
| Power | moderate | lower | lowest for dark images |
| Contrast / black level | moderate | better | best (true black) |
| Cost | lower | moderate | highest |

Strictly, an "LED monitor" is an LCD panel with an LED backlight.

**Printers.** Divided into **impact** (the head strikes the paper through a
ribbon) and **non-impact**.

| | Dot matrix | Inkjet | Laser |
|---|---|---|---|
| Type | impact | non-impact | non-impact |
| Mechanism | 9 or 24 pins strike an inked ribbon | tiny nozzles spray liquid ink droplets | laser draws a charged image on a drum; toner is fused by heat |
| Quality | low (visible dots) | good, photo-quality | excellent, sharp text |
| Speed unit | characters per second (cps) | pages per minute (slow) | pages per minute (fast) |
| Noise | noisy | quiet | quiet |
| Running cost | very low | high (cartridges) | low per page |
| Best for | multi-part carbon bills, bank passbooks | photos, home use | offices, high volume |

Also: plotters (large engineering drawings), 3D printers, projectors (LCD/DLP).

**Speaker.** Converts the digital audio signal — after the sound card's
digital-to-analogue converter — into sound waves. Output is described by power
(watts) and frequency response; headphones and earphones are personal versions.

## 1.14 Hardware Interfaces: ports, slots and standards

::: definition Port
A port is a socket on the outside of the system unit through which a peripheral
is connected to the computer's bus. An **interface** is the complete set of
electrical, mechanical and logical rules for that connection.
:::

```figure caption="Common connectors on the back panel of a desktop computer, drawn to relative scale, with the shape by which each is recognised."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, Polygon, Circle
fig, ax = plt.subplots(figsize=(5.1,2.8))
def dsub(x,y,w,h,inset,ec=INK):
    """D-subminiature shell: wider at the top."""
    ax.add_patch(Polygon([(x+inset,y),(x+w-inset,y),(x+w,y+h),(x,y+h)],
                         closed=True, fc='none', ec=ec, lw=1.3))
def pins(x0,x1,y,n,ms=1.7):
    for i in range(n):
        ax.plot([x0+(x1-x0)*i/max(n-1,1)],[y],'o',ms=ms,color=MUTED)
def lab(x,y,t,c=INK,fs=7.6):
    ax.text(x,y,t,ha='center',va='top',fontsize=fs,color=c)
# --- row 1 ---
dsub(0.05,2.20,1.70,0.42,0.13); pins(0.25,1.55,2.50,13); pins(0.31,1.49,2.32,12)
lab(0.90,2.10,'Parallel  DB-25\n(IEEE 1284)')
dsub(2.30,2.20,0.78,0.42,0.06); pins(2.42,2.96,2.50,5); pins(2.48,2.90,2.32,4)
lab(2.69,2.10,'Serial  DB-9\n(RS-232)')
ax.add_patch(Rectangle((3.62,2.30),0.95,0.30,fc='none',ec=INK,lw=1.3))
ax.add_patch(Rectangle((3.68,2.47),0.55,0.08,fc=GRID,ec=MUTED,lw=0.7))
lab(4.10,2.18,'USB Type-A')
ax.add_patch(FancyBboxPatch((5.00,2.34),0.72,0.20,
             boxstyle="round,pad=0,rounding_size=0.10",fc='none',ec=INK,lw=1.3))
lab(5.36,2.20,'USB Type-C')
# --- row 2 ---
ax.add_patch(Polygon([(0.30,1.25),(1.25,1.25),(1.35,1.57),(0.20,1.57)],
                     closed=True,fc='none',ec=INK,lw=1.3))
ax.add_patch(Rectangle((0.36,1.42),0.83,0.08,fc=GRID,ec=MUTED,lw=0.7))
lab(0.78,1.15,'HDMI Type-A')
ax.add_patch(Polygon([(2.00,1.22),(2.70,1.22),(2.70,1.58),(2.52,1.58),(2.52,1.70),
                      (2.18,1.70),(2.18,1.58),(2.00,1.58)],closed=True,
                     fc='none',ec=INK,lw=1.3))
lab(2.35,1.12,'RJ-45 (LAN)')
dsub(3.30,1.22,0.90,0.40,0.08,ec=ACCENT)
pins(3.44,4.06,1.52,5,1.5); pins(3.48,4.02,1.40,5,1.5); pins(3.44,4.06,1.28,5,1.5)
lab(3.75,1.12,'VGA DB-15',ACCENT)
for xx,cc in [(4.85,'#2e8b57'),(5.25,SERIES[4]),(5.65,'#A8271F')]:
    ax.add_patch(Circle((xx,1.43),0.13,fc='none',ec=cc,lw=1.3))
lab(5.25,1.22,'3.5 mm audio jacks')
# --- expansion slots ---
ax.text(0.20,0.62,'Expansion slots on the motherboard:',fontsize=8.2,color=INK)
for x0,w,nm,c in [(0.25,0.55,'PCIe x1',MUTED),(1.20,1.35,'PCIe x4',SERIES[0]),
                  (2.80,2.35,'PCIe x16',ACCENT)]:
    ax.add_patch(Rectangle((x0,0.16),w,0.16,fc=c,ec=c,lw=1.0,alpha=0.30))
    ax.text(x0+w/2,0.06,nm,ha='center',va='top',fontsize=7.4,color=c)
ax.set_xlim(-0.05,6.15); ax.set_ylim(-0.30,2.95); ax.set_aspect('equal'); ax.axis('off')
```

| Interface | Transmission | Connector | Speed | Status |
|---|---|---|---|---|
| **Parallel port** | 8 bits side by side on 8 wires | DB-25 female | up to about 2.5 MB s⁻¹ (ECP) | obsolete; was used for printers |
| **Serial port** | 1 bit at a time on one wire | DB-9 (RS-232) | up to 115.2 kbps | obsolete; was used for modems, mice |
| **USB** | serial, differential pair, hot-swappable, supplies power | Type-A, Type-B, micro, **Type-C** | 1.1: 12 Mbps · 2.0: 480 Mbps · 3.2 Gen1: 5 Gbps · Gen2: 10 Gbps · Gen2×2: 20 Gbps · USB4: 40 Gbps · USB4 v2: **80 Gbps** | current standard |
| **HDMI** | digital video **and** audio on one cable | 19-pin Type-A | 1.4: 10.2 Gbps · 2.0: 18 Gbps · 2.1: 48 Gbps · **2.2: 96 Gbps** | current standard |
| **Expansion slot** | parallel/serial lanes into the system bus | ISA, PCI, AGP, **PCI Express** | PCIe 4.0 ×16 ≈ 32 GB s⁻¹; PCIe 5.0 ×16 ≈ 63 GB s⁻¹ | PCIe only |

Despite the name, a **parallel** port is *slower* than a modern serial port:
pushing eight bits simultaneously down eight long wires causes skew and
crosstalk, so parallel links cannot be clocked fast. Modern high-speed links
(USB, SATA, PCIe, HDMI) are all serial for exactly this reason.

USB Power Delivery now carries up to **240 W**, enough to charge a laptop over
the same cable that carries the data. HDMI version 2.2, released in June 2025,
raised the maximum bandwidth to 96 Gbps and requires the new **Ultra96** certified
cable; it supports up to 12K at 120 Hz.

**Expansion slots** are connectors on the motherboard into which add-on cards
(graphics, sound, network, capture) are plugged. The historical order is
ISA → PCI → AGP (graphics only) → **PCI Express**, which uses point-to-point
serial *lanes* (×1, ×4, ×8, ×16) instead of a shared parallel bus.

## Chapter summary

- A computer accepts input, processes it under a stored program, stores data and
  produces output: the **IPO-S** cycle. Its characteristics are speed, accuracy,
  diligence, versatility, storage, automation and reliability — with no IQ.
- Five generations: vacuum tube → transistor → IC → microprocessor → AI/ULSI.
  Babbage is the Father of Computer; the Intel 4004 (1971) began generation four.
- Speed units: Hz/MHz/GHz, MIPS, FLOPS; time units ms, μs, ns, ps with
  $T = 1/f$. Storage: 8 bits = 1 byte, and $1\ \text{KB} = 2^{10}$ bytes, each
  further step $\times 2^{10}$.
- Classification by power: supercomputer > mainframe > mini > microcomputer.
- **Architecture** = what the machine does (programmer's view); **organization**
  = how it is built (implementation).
- Block diagram: input → CPU (CU + ALU + registers) ↔ primary memory ↔ secondary
  storage → output, with control signals from the CU to every unit.
- An $n$-bit address bus addresses $2^{n}$ locations; the address bus is
  unidirectional, the data bus bidirectional, the control bus carries commands.
- RAM is volatile (SRAM = cache, DRAM = main memory); ROM is non-volatile
  (MROM, PROM, EPROM, EEPROM, Flash). Cache speeds repeat access; a buffer
  matches unequal speeds.
- Secondary storage: magnetic disk (tracks, sectors, cylinders), flash/SSD,
  optical (CD 700 MB, DVD 4.7 GB, BD 25 GB), external and cloud.
- Serial interfaces (USB, HDMI, PCIe) have replaced the old parallel and RS-232
  ports because long parallel links cannot be clocked fast.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. Which of the following is **not** a characteristic of a computer? <span class="marks">[1]</span>
   (a) Diligence (b) Versatility (c) Intelligence (d) Accuracy
2. The microprocessor that started the fourth generation of computers is <span class="marks">[1]</span>
   (a) Intel 8085 (b) Intel 4004 (c) Intel 8088 (d) Motorola 6800
3. If the address bus of a CPU is 20 bits wide, the maximum number of memory locations it can address is <span class="marks">[1]</span>
   (a) 20 (b) $2^{20}$ (c) $20^{2}$ (d) $2^{10}$
4. Which memory is *volatile*? <span class="marks">[1]</span>
   (a) ROM (b) EPROM (c) RAM (d) Flash memory
5. A device that reads characters printed in magnetic ink on a bank cheque is <span class="marks">[1]</span>
   (a) OMR (b) OCR (c) MICR (d) BCR
6. The capacity of a standard single-layer DVD is about <span class="marks">[1]</span>
   (a) 700 MB (b) 4.7 GB (c) 25 GB (d) 8.5 GB
7. Which port carries digital video and audio together on one cable? <span class="marks">[1]</span>
   (a) VGA (b) RS-232 (c) HDMI (d) IEEE 1284

::: note Answers to Group A
**1.** (c) — a computer has no IQ of its own; it only follows instructions.
**2.** (b) — the Intel 4004 (1971) was the first microprocessor.
**3.** (b) — an $n$-line address bus selects $2^{n}$ distinct addresses.
**4.** (c) — RAM loses its contents when power is removed.
**5.** (c) — MICR reads the E-13B magnetic ink characters on cheques.
**6.** (b) — DVD-5 single layer holds 4.7 GB; 8.5 GB is dual layer.
**7.** (c) — VGA is analogue video only; HDMI carries both digital video and audio.
:::

**Group B — Short answer (5 marks each)**

1. Define a computer. Explain any four characteristics of a computer with one
   example of each. <span class="marks">[5]</span>
2. Differentiate between computer architecture and computer organization with
   two examples of each. <span class="marks">[5]</span>
3. What is a bus? Describe the three types of bus in a computer system, stating
   the direction of each. <span class="marks">[5]</span>
4. Differentiate between RAM and ROM. Name and describe any three types of ROM. <span class="marks">[5]</span>
5. A computer has a 32-bit address bus and a 64-bit data bus. Its clock runs at
   4 GHz and one memory transfer takes 5 clock cycles. Find (a) the maximum
   addressable memory in GB if each location holds one byte, (b) the clock
   period, and (c) the peak transfer rate in GB s⁻¹. <span class="marks">[5]</span>
6. Distinguish between OMR, OCR and MICR, giving one application of each. <span class="marks">[5]</span>

::: note Answers to Group B
**3.** A bus is a set of parallel wires carrying bits between the units of a
computer. The **address bus** is unidirectional (CPU → memory/I/O) and carries
the address of the location being accessed; $n$ lines give $2^{n}$ locations.
The **data bus** is bidirectional and carries the actual data or instruction; its
width normally equals the word length. The **control bus** carries individual
timing and command signals (READ, WRITE, CLOCK, RESET, INTERRUPT) in both
directions.

**5.** (a) Locations $= 2^{32} = 4{,}294{,}967{,}296$; at one byte each that is
$2^{32}/2^{30} = 4\ \text{GB}$.
(b) $T = 1/(4\times10^{9}) = 0.25\ \text{ns}$.
(c) One transfer takes $5 \times 0.25 = 1.25\ \text{ns}$ and moves
64 bits = 8 bytes, so the rate is
$8/(1.25\times10^{-9}) = 6.4\times10^{9}\ \text{B s}^{-1} = 6.4\ \text{GB s}^{-1}$.

**6.** OMR senses whether a **mark** has been made in a fixed position by
measuring reflected light — used for MCQ answer sheets. OCR recognises the
**shape of printed or handwritten characters** and converts them to editable
text — used to digitise books and forms. MICR reads characters printed in
**magnetic ink** in the E-13B font — used for clearing bank cheques.
:::

**Group C — Long answer (8 marks each)**

1. Draw the block diagram of a computer system and explain the function of each
   unit. Clearly distinguish the data path from the control path, and state the
   function of the control unit, the ALU and the registers. <span class="marks">[8]</span>
2. (a) What is a microprocessor? Explain clock speed and word length, and state
   how each affects performance. <span class="marks">[4]</span>
   (b) A processor has a clock speed of 3.2 GHz, a 16-bit data bus and a 28-bit
   address bus. Calculate the clock period, the memory it can address in MB, and
   the number of instructions executed per second if each instruction takes
   8 clock cycles. <span class="marks">[4]</span>
3. Explain the memory hierarchy of a computer. Compare cache, primary memory and
   secondary memory on speed, cost, capacity and volatility, and explain with an
   example why cache memory improves performance. <span class="marks">[8]</span>

::: note Answer outline to Group C
**1.** Draw input unit → CPU → output unit with primary memory above the CPU and
secondary storage below. Inside the CPU show CU, ALU and registers. Solid arrows
= data and instructions; dashed arrows = control signals radiating from the CU to
input, memory, ALU and output. Then describe: input converts data to binary; the
CU fetches, decodes and issues control signals but performs no arithmetic; the
ALU performs arithmetic and logic; registers hold operands and results; primary
memory holds the running program; secondary storage keeps data permanently;
output converts binary back to human-readable form.

**2. (b)** $T = 1/(3.2\times10^{9}) = 0.3125\ \text{ns}$.
Addressable locations $= 2^{28} = 268{,}435{,}456$; at 16 bits = 2 bytes each,
total $= 2^{28}\times 2 = 2^{29}\ \text{B} = 512\ \text{MB}$.
One instruction takes $8 \times 0.3125 = 2.5\ \text{ns}$, so the rate is
$1/(2.5\times10^{-9}) = 4\times10^{8}$ instructions per second = **400 MIPS**.

**3.** Sketch the pyramid: registers, L1/L2/L3 cache, RAM, SSD, HDD, tape/cloud.
Going down, capacity and cost per byte improve but access time worsens by roughly
a factor of ten per level. Cache is small, fast, volatile SRAM; primary memory is
larger, slower, volatile DRAM; secondary memory is largest, slowest and
non-volatile. Cache works because of **locality of reference** — a loop executed
a million times is fetched into cache once and then read at cache speed, so a
90 % hit rate can cut the average access time of a 1 ns cache and a 60 ns RAM to
about $0.9(1) + 0.1(60) = 6.9\ \text{ns}$.
:::
