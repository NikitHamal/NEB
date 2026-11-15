---
file: NEBians-IOE-Past-Paper-Computer-Organization-and-Architecture-ENEX253-2082-Bhadra.pdf
subject: Computer Organization and Architecture
level: BE · Year II / Part II
code: ENEX 253
year_bs: 2082 Bhadra
cal: BS
year_ad: 2025
stream: BEI
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular (New Course). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
Comparison between computer architecture and computer organization. Explain CPI, MIPS rate, MFLOPS rate and Amdahl's law. [[4+4]]

@q 2
How effective address is calculated in different types of addressing modes? Explain with an example. [[8]]

@q 3
Differentiate between hardwired control unit and microprogrammed control unit. Describe address sequencing with the help of block diagram. [[4+4]]

@q 4
Explain associative cache mapping technique with suitable example. Describe the Least Recently Used (LRU) replacement algorithm with case example of miss and hit. [[5+5]]

@q 5
Write down the flowchart of Booth's Multiplication algorithm. Multiply $7 \times -5 = -35$ using Booth's Multiplication algorithm. [[5+5]]

@q 6
Formulate 4 segment instruction pipeline with branching and interrupts. [[5]]

@q 7
Comparison between Programmed I/O, Interrupt-Driven I/O and Direct Memory Access (DMA). [[5]]

@q 8
Explain about how multicore processors improve the hardware performance with respect to parallelism and power consumption. [[6]]

<!-- SOLUTIONS -->

@s 1
**Computer architecture and computer organization.**

| Basis | Computer architecture | Computer organization |
|---|---|---|
| Meaning | the attributes of the system **visible to the programmer**: what the computer does | how the features are **implemented**: the operational units and their interconnection |
| Concerned with | instruction set, data types, number of registers, addressing modes, I/O mechanism, memory addressing | control signals, interfaces between computer and peripherals, memory technology, ALU and bus design |
| Question answered | "what"? (logical view) | "how"? (physical view) |
| Level | design of the specification | realisation of the specification |
| Example | a multiply instruction exists | multiplier hardware or repeated addition |

One architecture (for example x86) can have many organizations, and software written for it runs on all of them.

**CPI (cycles per instruction).** The average number of clock cycles per instruction: for a program with $I_c$ instructions, $I_i$ of type $i$ with $CPI_i$ cycles,

$$CPI = \frac{\sum_i CPI_i \times I_i}{I_c}$$

and the CPU time is $T = I_c \times CPI \times \tau = \dfrac{I_c \times CPI}{f}$ ($\tau$ = clock period, $f$ = clock rate).

**MIPS rate** (millions of instructions per second):

$$\text{MIPS} = \frac{I_c}{T \times 10^{6}} = \frac{f}{CPI \times 10^{6}}$$

**MFLOPS rate** (millions of floating-point operations per second):

$$\text{MFLOPS} = \frac{\text{number of floating-point operations}}{T \times 10^{6}}$$

MIPS depends on the instruction set (not comparable between different architectures); MFLOPS is better for scientific work but also depends on which operations are counted as floating point.

**Example.** A 500 MHz processor runs this instruction mix:

| Type | Fraction | CPI |
|---|---|---|
| ALU | 0.45 | 1 |
| Load | 0.25 | 2 |
| Store | 0.15 | 2 |
| Branch | 0.15 | 3 |

$$CPI = 0.45(1) + 0.25(2) + 0.15(2) + 0.15(3) = 1.7$$

$$\text{MIPS} = \frac{500 \times 10^{6}}{1.7 \times 10^{6}} = 294.1$$

For a program of $10^{9}$ instructions, $T = 10^{9} \times 1.7 / (500 \times 10^{6}) = 3.4$ s.

**Amdahl's law.** If a fraction $f$ of the execution time is speeded up by a factor $k$ and the rest is unchanged, the overall speed-up is

$$\begin{gathered}\text{Speed-up} = \frac{1}{(1 - f) + \dfrac{f}{k}} \\ \text{limit as } k \to \infty:\ \frac{1}{1 - f}\end{gathered}$$

Example: $f = 0.8$, $k = 4$ gives $\dfrac{1}{0.2 + 0.2} = 2.5$ and the upper limit is $1/0.2 = 5$. The law shows that the part that cannot be improved (the serial part) limits the gain from faster hardware or more processors, so make the common case fast.

@s 2
**Effective address (EA)** is the actual memory address of the operand, computed from the address field of the instruction and the addressing mode: the mode field tells the control unit how to turn the instruction's address field into the operand. The common modes are given below, with a worked example: the instruction is stored at address 200 (its address field 500 is at 201), so after fetching PC = 202; register R1 = 400, index register XR = 100, with memory contents M[399] = 450, M[400] = 700, M[500] = 800, M[600] = 900, M[702] = 325, M[800] = 300.

| Mode | Effective address (EA) | Value loaded (instruction at 200, address field 500, R1 = 400, XR = 100, PC = 202 after the fetch) |
|---|---|---|
| Implied | operand is implied by the opcode (accumulator, stack top) | e.g. `CMA`, `PUSH`: no address |
| Immediate | no EA; the operand is in the instruction | operand = 500 |
| Register direct | operand is in register R1 | 400 |
| Register indirect | $EA = (R1) = 400$ | M[400] = 700 |
| Autoincrement | $EA = (R1)$, then $R1 \leftarrow R1 + 1$ | EA = 400: 700, R1 becomes 401 |
| Autodecrement | $R1 \leftarrow R1 - 1$, then $EA = (R1)$ | EA = 399: 450 |
| Direct (absolute) | $EA = \text{address field} = 500$ | M[500] = 800 |
| Indirect | $EA = M[\text{address field}] = M[500] = 800$ | M[800] = 300 |
| Relative | $EA = PC + \text{address field} = 202 + 500 = 702$ | M[702] = 325 |
| Indexed | $EA = XR + \text{address field} = 100 + 500 = 600$ | M[600] = 900 |
| Base register | $EA = BR + \text{address field}$ (BR holds the segment start; here 400 + 500 = 900) | M[900] |

Uses: immediate for constants; direct for simple variables; indirect for pointers and jump tables; register for speed; register indirect, autoincrement and autodecrement for arrays, stacks and pointer walking; relative for position-independent branches; indexed for array elements ($XR$ is incremented to step through an array); base register for relocation of programs (segment start in BR).

@s 3
**Function of the control unit.** The control unit is the part of the processor that directs the operation of everything else. For each instruction it (1) fetches the instruction and decodes the opcode, (2) generates, in the correct order and at the correct clock pulse, the **control signals** (register load enables, ALU function select, memory read/write, bus gating, I/O strobes) that open the data paths for each micro-operation, (3) sequences the instruction cycle (fetch, decode, execute, interrupt), and (4) responds to external signals such as interrupts, reset and bus requests, using the flags of the status register for conditional operations.

```figure caption="Left: hardwired control unit (logic gates decode the instruction register, timing signals and flags). Right: microprogrammed control unit (the control word is read from the control memory)."
import numpy as _np, matplotlib.patches as mp
def box(ax,x,y,w,h,t,fc="white",ec=INK,fs=8,lw=1.2,ls="-"):
    ax.add_patch(mp.FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",fc=fc,ec=ec,lw=lw,ls=ls,zorder=3))
    ax.text(x,y,t,ha="center",va="center",fontsize=fs,zorder=4)
def arr(ax,a,b,c=None,rad=0.0,lw=1.2,sa=0,sb=0,style="-|>"):
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle=style,color=c or ACCENT,lw=lw,shrinkA=sa,shrinkB=sb,connectionstyle="arc3,rad=%s"%rad),zorder=2)
fig,(a,b)=plt.subplots(1,2,figsize=(7.2,3.0))
for z in (a,b): z.axis("off"); z.set_xlim(-0.3,5.2); z.set_ylim(-3.6,1.6)
a.set_title("Hardwired",fontsize=8); box(a,0.9,0.9,1.5,0.6,"Instruction\nregister",fs=6.5,fc="#eaf3ff"); box(a,0.9,-0.3,1.5,0.6,"Decoder",fs=7); box(a,3.9,0.9,1.5,0.6,"Clock +\ntiming counter",fs=6.5,fc="#eaf3ff"); box(a,3.9,-0.3,1.5,0.6,"Flags / status",fs=6.5,fc="#eaf3ff")
box(a,2.4,-1.8,3.6,0.8,"Combinational control logic\n(gates, flip-flops)",fs=7,fc="#fff4d6")
for x,y in [(0.9,0.6),(0.9,-0.6)]: arr(a,(x,y),(x+0.4 if y>0 else 1.4,-1.4 if y<0 else -0.0),c=ACCENT)
arr(a,(3.9,0.6),(3.4,-1.4),c=ACCENT); arr(a,(3.9,-0.6),(3.9,-1.4),c=ACCENT); arr(a,(2.4,-2.2),(2.4,-3.1),c=ACCENT); a.text(2.4,-3.35,"control signals",fontsize=7,ha="center")
b.set_title("Microprogrammed",fontsize=8); box(b,0.9,0.9,1.5,0.6,"Instruction\nregister",fs=6.5,fc="#eaf3ff"); box(b,0.9,-0.4,1.5,0.7,"Sequencer\n(next address)",fs=6.5); box(b,3.2,-0.4,1.5,0.7,"Control address\nregister (CAR)",fs=6.3,fc="#fff4d6")
box(b,3.2,-1.7,1.5,0.7,"Control memory\n(microprogram)",fs=6.5,fc="#fff4d6"); box(b,3.2,-2.9,1.5,0.6,"Control data\nregister",fs=6.5,fc="#fff4d6")
arr(b,(0.9,0.6),(0.9,-0.05),c=ACCENT); arr(b,(1.65,-0.4),(2.45,-0.4),c=ACCENT); arr(b,(3.2,-0.75),(3.2,-1.3),c=ACCENT); arr(b,(3.2,-2.05),(3.2,-2.6),c=ACCENT)
arr(b,(3.95,-2.9),(4.9,-2.9),c=ACCENT); b.text(4.6,-3.3,"control word",fontsize=6.5,ha="center"); arr(b,(3.95,-1.7),(4.5,-1.7),c=INK,style="-"); b.plot([4.5,4.5],[-1.7,-0.4],color=INK,lw=1); arr(b,(4.5,-0.4),(3.95,-0.4),c=INK,style="-")
b.text(5.1,-1.0,"status",fontsize=6.5,rotation=90,va="center")
```

| Basis | Hardwired control unit | Microprogrammed control unit |
|---|---|---|
| Implementation | fixed logic circuit of gates, decoders, flip-flops and counters | control words (microinstructions) stored in a control memory (ROM) |
| Design | complex state tables and logic minimisation | writing a microprogram, like a program |
| Speed | **faster** (no memory access, only gate delays) | slower (a control memory read per microinstruction) |
| Flexibility | hard to change or extend, redesign of hardware | easy to modify, correct or add instructions by changing the microprogram |
| Cost / area | cheaper for small instruction sets | costlier ROM and sequencing hardware, but the cost is spread over a big instruction set |
| Instruction set | RISC processors | CISC processors (complex instructions) |
| Debugging | difficult | easier, emulation is possible |
| Example | MIPS, ARM cores | IBM 360, 8086, VAX |


**Address sequencing.** The microinstructions of a microprogram are stored in groups called **routines** in the control memory, and the control unit must supply the address of the next microinstruction after every clock pulse. Address sequencing handles: (1) **incrementing** the control address register CAR for the next microinstruction in a routine; (2) **unconditional or conditional branching** to the address given in the branch field of the microinstruction, conditional on a status bit (zero, carry, sign) chosen by the branch logic; (3) **mapping** from the opcode of the instruction register to the starting address of its routine (for example the fetch routine has a fixed address, and the opcode $0100$ may map to address $0100\,0000$ by placing 0 in front and two 0s behind); (4) **subroutine call and return** with the subroutine register SBR (microroutines shared by several instructions, such as effective-address calculation).

```figure caption="Address sequencing in a microprogrammed control unit: the control address register (CAR) gets its next value from the incrementer, a branch address field, the mapping logic (opcode) or the subroutine register."
import numpy as _np, matplotlib.patches as mp
def box(ax,x,y,w,h,t,fc="white",ec=INK,fs=8,lw=1.2,ls="-"):
    ax.add_patch(mp.FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",fc=fc,ec=ec,lw=lw,ls=ls,zorder=3))
    ax.text(x,y,t,ha="center",va="center",fontsize=fs,zorder=4)
def arr(ax,a,b,c=None,rad=0.0,lw=1.2,sa=0,sb=0,style="-|>"):
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle=style,color=c or ACCENT,lw=lw,shrinkA=sa,shrinkB=sb,connectionstyle="arc3,rad=%s"%rad),zorder=2)
fig,ax=plt.subplots(figsize=(7.4,3.2)); ax.axis("off"); ax.set_xlim(-0.4, 11.6); ax.set_ylim(-0.1, 4.3)
box(ax,0.9,3.2,1.9,0.7,"Instruction\nregister (opcode)",fs=6.5,fc="#eaf3ff"); box(ax,0.9,1.7,1.9,0.7,"Mapping logic",fs=7)
box(ax,3.9,0.5,1.9,0.7,"Branch logic\n(status bits)",fs=6.5); box(ax,3.9,2.1,1.9,0.7,"Multiplexers\n(select next address)",fs=6.3,fc="#fff4d6")
box(ax,6.9,2.1,1.9,0.7,"Control address\nregister (CAR)",fs=6.3,fc="#fff4d6"); box(ax,6.9,0.5,1.9,0.7,"Incrementer",fs=7); box(ax,6.9,3.7,1.9,0.7,"Subroutine\nregister (SBR)",fs=6.3)
box(ax,9.9,2.1,1.9,0.7,"Control memory\n(ROM)",fs=6.5,fc="#fff4d6"); box(ax,9.9,0.5,1.9,0.7,"Control data\nregister",fs=6.5,fc="#fff4d6")
arr(ax,(0.9,2.85),(0.9,2.05),c=ACCENT); arr(ax,(1.85,1.7),(2.95,2.0),c=ACCENT); arr(ax,(4.85,2.1),(5.95,2.1),c=ACCENT); arr(ax,(7.85,2.1),(8.95,2.1),c=ACCENT)
arr(ax,(9.9,1.75),(9.9,0.85),c=ACCENT); arr(ax,(6.9,1.75),(6.9,0.85),c=INK); arr(ax,(5.95,0.5),(4.85,0.5),c=INK,style="-");
arr(ax,(6.0,0.6),(4.5,1.75),c=INK,rad=0.0); arr(ax,(3.9,0.85),(3.9,1.75),c=ACCENT); arr(ax,(6.9,3.35),(4.5,2.45),c=INK); arr(ax,(6.9,2.45),(6.9,3.35),c=INK,rad=-0.4)
ax.text(11.0,1.2,"branch address field",fontsize=6.5,ha="center",color="#b00020"); ax.text(11.0,0.15,"from the control word",fontsize=6.0,ha="center")
```

The multiplexers choose the next address from four sources according to the mode bits of the microinstruction: CAR + 1, the branch address field (if the condition of the branch logic is true), the output of the mapping logic, or SBR (return). After the fetch routine the mapping logic loads the first address of the execute routine, and the last microinstruction of every routine branches back to the fetch routine at address 0.

@s 4
**Associative (fully associative) cache mapping.** A main-memory block can be placed in **any line** of the cache. The memory address is split only into a **tag** (the block number) and the word offset, $\text{Address} = \text{Tag} \,|\, \text{Word}$. To look up a word, the tag is compared **simultaneously with the tags of all cache lines** using an associative memory (content-addressable memory); a match is a hit and the word offset selects the word, otherwise it is a miss and a block is fetched, replacing a line chosen by a replacement algorithm when the cache is full.

*Advantage:* most flexible, no conflict misses, best hit ratio. *Disadvantage:* expensive and slow comparators for all the tags, and a replacement algorithm is needed.

**Address example.** Main memory 64 K words (16-bit address), block of 8 words, so offset = 3 bits and tag = 13 bits (8 K blocks); a cache of 32 lines holds any 32 of them. (Set associative mapping is the compromise: the block is placed in any line of one fixed set, address = tag, set, word.)

**LRU replacement.** On a miss with a full cache, remove the block that has **not been used for the longest time**. It is based on the principle of temporal locality (recently used blocks are likely to be used again). Implementation: a counter or an age value per line (updated on every reference, hit or miss), a stack of block numbers with the most recent on top, or a bit matrix; every **hit** moves the block to the most-recently-used position, and a **miss** evicts the least-recently-used block.

**Example.** Fully associative cache with 4 lines, reference string of block numbers 1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5 (oldest, i.e. least recently used, is listed first):

| Reference | Set | Result | Evicted | Contents after the reference (oldest first) |
|---|---|---|---|---|
| 1 | - | **miss** | - | [1] |
| 2 | - | **miss** | - | [1, 2] |
| 3 | - | **miss** | - | [1, 2, 3] |
| 4 | - | **miss** | - | [1, 2, 3, 4] |
| 1 | - | hit | - | [2, 3, 4, 1] |
| 2 | - | hit | - | [3, 4, 1, 2] |
| 5 | - | **miss** | 3 | [4, 1, 2, 5] |
| 1 | - | hit | - | [4, 2, 5, 1] |
| 2 | - | hit | - | [4, 5, 1, 2] |
| 3 | - | **miss** | 4 | [5, 1, 2, 3] |
| 4 | - | **miss** | 5 | [1, 2, 3, 4] |
| 5 | - | **miss** | 1 | [2, 3, 4, 5] |

$$\boxed{\,\text{LRU: } 4 \text{ hits and } 8 \text{ misses}\ \ (\text{hit ratio } 4/12)\,}$$

Examples: reference 1 (5th) is a **hit**, because blocks 1, 2, 3, 4 are all in the cache, and it makes 1 the most recent; reference 5 (7th) is a **miss**: the cache is full, so the least recently used block 3 is evicted; the last references 3, 4 and 5 are misses because LRU had just evicted exactly those blocks (a cyclic reference pattern is bad for LRU). LRU gives fewer misses than FIFO for programs with locality and has no Belady's anomaly, but costs more hardware. On the 20-reference string 7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1 with 3 frames LRU gives 12 faults (FIFO 15).

@s 5
**Flowchart of Booth's algorithm:**

**Booth's algorithm** multiplies two signed numbers in two's complement. It scans the multiplier bits in pairs $Q_0 Q_{-1}$ ($Q_{-1}$ is an extra bit appended on the right, initially 0): pair $10$ marks the **start of a run of 1s** (subtract the multiplicand, $A \leftarrow A - M$), pair $01$ marks the **end of a run of 1s** (add, $A \leftarrow A + M$), and $00$ or $11$ means no operation. After each step the register $A, Q, Q_{-1}$ is **arithmetic-shifted right** by one bit (the sign bit of $A$ is copied). After $n$ cycles the $2n$-bit product is in $A{:}Q$.

```figure caption="Flowchart of Booth's multiplication algorithm (A = accumulator, Q = multiplier, Q-1 = extra bit, M = multiplicand, SC = sequence counter)."
import numpy as _np, matplotlib.patches as mp
def box(ax,x,y,w,h,t,fc="white",ec=INK,fs=8,lw=1.2,ls="-"):
    ax.add_patch(mp.FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",fc=fc,ec=ec,lw=lw,ls=ls,zorder=3))
    ax.text(x,y,t,ha="center",va="center",fontsize=fs,zorder=4)
def arr(ax,a,b,c=None,rad=0.0,lw=1.2,sa=0,sb=0,style="-|>"):
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle=style,color=c or ACCENT,lw=lw,shrinkA=sa,shrinkB=sb,connectionstyle="arc3,rad=%s"%rad),zorder=2)
fig,ax=plt.subplots(figsize=(4.6,6.2)); ax.axis("off"); ax.set_xlim(-5.4, 5.4); ax.set_ylim(-2.4, 7.8)
box(ax,0,7.2,2.6,0.6,"Start",fs=7.5,fc="#eaf3ff")
box(ax,0,6.1,3.6,0.7,"A = 0,  Q-1 = 0,  SC = n\nM = multiplicand, Q = multiplier",fs=6.5)
ax.add_patch(mp.Polygon([(0,5.35),(1.6,4.5),(0,3.65),(-1.6,4.5)],fc="#fff4d6",ec=INK,lw=1.2,zorder=3)); ax.text(0,4.5,"Q0 Q-1 ?",ha="center",va="center",fontsize=7.5,zorder=4)
box(ax,-3.6,3.0,2.6,0.7,"A = A - M\n(Q0 Q-1 = 10)",fs=6.5); box(ax,3.6,3.0,2.6,0.7,"A = A + M\n(Q0 Q-1 = 01)",fs=6.5)
box(ax,0,2.0,4.4,0.7,"Arithmetic shift right A, Q, Q-1\n(sign bit of A is kept)",fs=6.5,fc="#eaf3ff"); box(ax,0,1.0,2.6,0.6,"SC = SC - 1",fs=7)
ax.add_patch(mp.Polygon([(0,0.45),(1.3,-0.2),(0,-0.85),(-1.3,-0.2)],fc="#fff4d6",ec=INK,lw=1.2,zorder=3)); ax.text(0,-0.2,"SC = 0 ?",ha="center",va="center",fontsize=7.5,zorder=4)
box(ax,0,-1.8,3.6,0.6,"Product = A : Q  (2n bits)   End",fs=7,fc="#eaf3ff")
arr(ax,(0,6.9),(0,6.45)); arr(ax,(0,5.75),(0,5.35)); arr(ax,(-1.6,4.5),(-3.6,3.35),rad=0.0); arr(ax,(1.6,4.5),(3.6,3.35)); ax.text(-3.3,4.2,"10",fontsize=7,color="#b00020"); ax.text(3.3,4.2,"01",fontsize=7,color="#b00020")
arr(ax,(0,3.65),(0,2.35)); ax.text(0.1,3.2,"00 or 11",fontsize=6.5,color="#b00020")
arr(ax,(-3.6,2.65),(-1.6,2.1)); arr(ax,(3.6,2.65),(1.6,2.1)); arr(ax,(0,1.65),(0,1.3)); arr(ax,(0,0.7),(0,0.45)); arr(ax,(0,-0.85),(0,-1.5)); ax.text(0.1,-1.15,"yes",fontsize=7,color="#b00020")
arr(ax,(-1.3,-0.2),(-4.9,-0.2),c=INK,style="-"); ax.plot([-4.9,-4.9],[-0.2,4.5],color=INK,lw=1.2); arr(ax,(-4.9,4.5),(-1.6,4.5),c=INK); ax.text(-3.0,0.05,"no",fontsize=7,color="#b00020")
ax.set_xlim(-5.4,5.4); ax.set_ylim(-2.4,7.8)
```

```figure caption="Hardware for Booth's algorithm: the adder/subtractor adds or subtracts the multiplicand register BR to the accumulator AC; AC, QR and Q-1 shift right together."
import numpy as _np, matplotlib.patches as mp
def box(ax,x,y,w,h,t,fc="white",ec=INK,fs=8,lw=1.2,ls="-"):
    ax.add_patch(mp.FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",fc=fc,ec=ec,lw=lw,ls=ls,zorder=3))
    ax.text(x,y,t,ha="center",va="center",fontsize=fs,zorder=4)
def arr(ax,a,b,c=None,rad=0.0,lw=1.2,sa=0,sb=0,style="-|>"):
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle=style,color=c or ACCENT,lw=lw,shrinkA=sa,shrinkB=sb,connectionstyle="arc3,rad=%s"%rad),zorder=2)
fig,ax=plt.subplots(figsize=(5.2,3.0)); ax.axis("off"); ax.set_xlim(-2.2, 6.6); ax.set_ylim(-0.3, 4.1)
box(ax,0,3.5,2.0,0.7,"BR (multiplicand)",fs=7,fc="#eaf3ff"); box(ax,0,2.2,2.6,0.7,"Parallel adder /\nsubtractor",fs=7,fc="#fff4d6")
box(ax,0,0.8,2.0,0.7,"AC (accumulator)",fs=7,fc="#eaf3ff"); box(ax,3.4,0.8,2.0,0.7,"QR (multiplier)",fs=7,fc="#eaf3ff"); box(ax,5.5,0.8,0.7,0.7,"Q-1",fs=7,fc="#eaf3ff")
box(ax,5.0,3.0,2.6,0.8,"Control logic\nQn Qn+1 = 10: subtract\n01: add, 00 / 11: none",fs=5.8,fc="#fff4d6"); box(ax,5.0,2.0,1.7,0.5,"Sequence counter",fs=6.3)
arr(ax,(0,3.15),(0,2.55)); arr(ax,(0,1.85),(0,1.15),c=ACCENT); arr(ax,(0,1.15),(0,1.85),c=INK,rad=0.0)
ax.plot([-1.6,-1.6],[0.8,2.2],color=INK,lw=1); arr(ax,(-1.6,2.2),(-1.3,2.2),c=INK); arr(ax,(-1.0,0.8),(-1.6,0.8),c=INK,style="-")
arr(ax,(2.4,0.8),(1.0,0.8),c=INK,style="-"); arr(ax,(4.4,0.8),(5.1,0.8),c=ACCENT); arr(ax,(1.0,0.45),(2.4,0.45),c=ACCENT); ax.text(2.4,0.1,"shift right (AC, QR, Q-1)",fontsize=6.5,ha="center",color="#b00020")
arr(ax,(5.0,2.6),(5.0,2.3),c=INK); arr(ax,(3.8,3.0),(1.4,2.35),c=ACCENT); ax.text(3.0,2.95,"add / sub",fontsize=6.3,color="#b00020"); arr(ax,(3.4,1.15),(4.2,2.6),c=INK); arr(ax,(5.5,1.15),(5.3,2.6),c=INK)
```

**Multiplication of $7 \times (-5)$ = -35:**

Multiplicand $M = 7 = 0111$, multiplier $Q = -5 = 1011$ (4-bit two's complement), $-M = 1001$.

| Cycle | $Q_0 Q_{-1}$ | Operation | A after add/subtract | A after shift | Q after shift | $Q_{-1}$ |
|---|---|---|---|---|---|---|
| 0 (initial) | - | - | - | 0000 | 1011 | 0 |
| 1 | 10 | A = A - M | 1001 | 1100 | 1101 | 1 |
| 2 | 11 | no change | 1100 | 1110 | 0110 | 1 |
| 3 | 01 | A = A + M | 0101 | 0010 | 1011 | 0 |
| 4 | 10 | A = A - M | 1011 | 1101 | 1101 | 1 |

Product = A:Q = $11011101$ (8 bits). Its sign bit is 1, so it is negative: two's complement gives $-35$.


@s 6
**Four-segment instruction pipeline.** The instruction cycle is divided into four segments that work on four different instructions at the same time:

1. **FI**: fetch the instruction from memory;
2. **DA**: decode the instruction and calculate the effective address;
3. **FO**: fetch the operand from memory;
4. **EX**: execute the instruction (and store the result).

```figure caption="Four-segment instruction pipeline with branch and interrupt handling: FI fetch, DA decode and address calculation, FO operand fetch, EX execute. A taken branch or an interrupt empties the pipe and reloads the PC."
import numpy as _np, matplotlib.patches as mp
def box(ax,x,y,w,h,t,fc="white",ec=INK,fs=8,lw=1.2,ls="-"):
    ax.add_patch(mp.FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",fc=fc,ec=ec,lw=lw,ls=ls,zorder=3))
    ax.text(x,y,t,ha="center",va="center",fontsize=fs,zorder=4)
def arr(ax,a,b,c=None,rad=0.0,lw=1.2,sa=0,sb=0,style="-|>"):
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle=style,color=c or ACCENT,lw=lw,shrinkA=sa,shrinkB=sb,connectionstyle="arc3,rad=%s"%rad),zorder=2)
fig,ax=plt.subplots(figsize=(4.6,6.2)); ax.axis("off"); ax.set_xlim(-3.0, 6.4); ax.set_ylim(-0.2, 9.4)
box(ax,0,8.6,3.4,0.7,"Segment 1:  FI  Fetch instruction\nfrom memory",fs=6.8,fc="#eaf3ff"); box(ax,0,7.1,3.4,0.7,"Segment 2:  DA  Decode instruction and\ncalculate effective address",fs=6.5,fc="#eaf3ff")
ax.add_patch(mp.Polygon([(0,6.2),(1.1,5.65),(0,5.1),(-1.1,5.65)],fc="#fff4d6",ec=INK,lw=1.2,zorder=3)); ax.text(0,5.65,"Branch?",ha="center",va="center",fontsize=7,zorder=4)
box(ax,0,4.1,3.4,0.7,"Segment 3:  FO  Fetch operand\nfrom memory",fs=6.8,fc="#eaf3ff"); box(ax,0,2.9,3.4,0.7,"Segment 4:  EX  Execute instruction",fs=6.8,fc="#eaf3ff")
ax.add_patch(mp.Polygon([(0,2.2),(1.3,1.65),(0,1.1),(-1.3,1.65)],fc="#fff4d6",ec=INK,lw=1.2,zorder=3)); ax.text(0,1.65,"Interrupt?",ha="center",va="center",fontsize=7,zorder=4)
box(ax,4.2,5.65,2.8,0.9,"Update PC\nEmpty the pipe",fs=6.8,fc="#ffe4e4"); box(ax,4.2,1.65,3.4,1.0,"Interrupt handling\nUpdate PC, empty the pipe",fs=6.5,fc="#ffe4e4")
arr(ax,(0,8.25),(0,7.45)); arr(ax,(0,6.75),(0,6.2)); arr(ax,(0,5.1),(0,4.45)); arr(ax,(0,3.75),(0,3.25)); arr(ax,(0,2.55),(0,2.2)); ax.text(0.1,4.85,"no",fontsize=7,color="#b00020")
arr(ax,(1.1,5.65),(2.8,5.65)); ax.text(1.6,5.8,"yes",fontsize=7,color="#b00020"); arr(ax,(1.3,1.65),(2.5,1.65)); ax.text(1.5,1.8,"yes",fontsize=7,color="#b00020")
ax.plot([5.6,5.6],[5.65,9.0],color=INK,lw=1.2); ax.plot([5.6,1.7],[9.0,9.0],color=INK,lw=1.2); arr(ax,(1.7,9.0),(1.7,8.9),c=INK); arr(ax,(1.7,9.0),(1.7,8.75),c=INK,rad=0.0)
arr(ax,(4.2,1.15),(4.2,0.2),c=INK,style="-"); ax.plot([4.2,-2.4,-2.4],[0.2,0.2,8.6],color=INK,lw=1.2); arr(ax,(-2.4,8.6),(-1.7,8.6),c=INK)
ax.text(0,0.55,"no: fetch the next instruction",fontsize=6.5,ha="center",color="#b00020")
```

**Branching.** When the decoder (segment 2) finds a branch instruction, the instructions already fetched after it are wrong if the branch is taken: the pipe is **emptied** and the PC is updated with the branch address after the effective address is calculated, then FI restarts from the target; the instructions after the branch must not be allowed to reach FO and EX, so branch instructions cost extra clock cycles. **Interrupts.** An interrupt is recognised at the end of the execute segment of the current instruction: the instructions in the pipe behind it are discarded, the return address is saved and the PC is loaded with the interrupt routine address (the pipe is emptied as for a branch).

**Timing diagram** (instruction 3 is a branch to instruction 15; $\blacksquare$ marks a discarded step):

| Cycle | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| Instr. 1 | FI | DA | FO | EX | | | | | | |
| Instr. 2 | | FI | DA | FO | EX | | | | | |
| Instr. 3 (branch) | | | FI | DA | FO | EX | | | | |
| Instr. 4 | | | | FI | $\blacksquare$ | | | | | |
| Instr. 5 | | | | | $\blacksquare$ | | | | | |
| Instr. 15 | | | | | | FI | DA | FO | EX | |
| Instr. 16 | | | | | | | FI | DA | FO | EX |

In a non-pipelined machine each instruction needs 4 cycles. For $n$ instructions with no branches the pipeline needs $k + n - 1 = n + 3$ cycles, giving a speed-up of $\dfrac{4n}{n + 3} \to 4$; every taken branch or interrupt wastes about $k - 1 = 3$ cycles, which is why branch prediction, delayed branch and a branch target buffer are used.

@s 7
**Programmed I/O.** The CPU starts the transfer and then **busy-waits** (polls the device status) for every byte or word; data goes device, CPU register, memory, so the CPU is occupied for the whole transfer.

**Interrupt-driven I/O.** The CPU starts the operation and continues with other work; the device interrupts when it is ready, and the CPU runs an interrupt service routine that moves one word. There is no busy waiting, but the CPU still moves every word and pays the overhead of saving and restoring the context at each interrupt (a big transfer needs thousands of interrupts).

**DMA (direct memory access).** A DMA controller with an address register, a word-count register and a control register moves the whole block directly between the device and memory over the system bus, taking the bus by **cycle stealing** (one word at a time) or **burst mode**.

```figure caption="DMA transfer: the processor programs the DMA controller, which then moves data between the I/O device and memory by cycle stealing or burst, and interrupts the CPU only at the end."
import numpy as _np, matplotlib.patches as mp
def box(ax,x,y,w,h,t,fc="white",ec=INK,fs=8,lw=1.2,ls="-"):
    ax.add_patch(mp.FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",fc=fc,ec=ec,lw=lw,ls=ls,zorder=3))
    ax.text(x,y,t,ha="center",va="center",fontsize=fs,zorder=4)
def arr(ax,a,b,c=None,rad=0.0,lw=1.2,sa=0,sb=0,style="-|>"):
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle=style,color=c or ACCENT,lw=lw,shrinkA=sa,shrinkB=sb,connectionstyle="arc3,rad=%s"%rad),zorder=2)
fig,ax=plt.subplots(figsize=(7.0,2.7)); ax.axis("off"); ax.set_xlim(-0.6, 11.0); ax.set_ylim(-0.4, 4.4)
box(ax,0.8,2.6,1.7,0.9,"CPU",fs=8,fc="#eaf3ff"); box(ax,3.9,2.6,1.9,0.9,"DMA controller\n(address, count,\ncontrol registers)",fs=6,fc="#fff4d6"); box(ax,7.1,2.6,1.7,0.9,"Memory",fs=8,fc="#eaf3ff"); box(ax,3.9,0.5,1.7,0.8,"I/O device",fs=8,fc="#eaf3ff")
ax.plot([-0.2,8.4],[4.0,4.0],color=INK,lw=2); ax.text(8.5,4.0,"address / data / control bus",fontsize=6.3,va="center")
for x in (0.8,3.9,7.1): ax.plot([x,x],[3.05,4.0],color=INK,lw=1.2)
arr(ax,(1.65,2.75),(2.95,2.75),c=ACCENT); ax.text(2.3,2.95,"program",fontsize=6.2,ha="center")
arr(ax,(2.95,2.4),(1.65,2.4),c="#b00020"); ax.text(2.3,2.05,"interrupt (done)",fontsize=6,ha="center",color="#b00020")
arr(ax,(3.9,1.7),(3.9,0.95),c=INK,style="<|-|>"); ax.text(4.1,1.35,"DMA req/ack",fontsize=6,color="#b00020")
ax.text(1.4,3.55,"HOLD / HLDA",fontsize=6,color="#b00020"); ax.text(5.5,0.5,"data moves directly between device and memory",fontsize=6.3,va="center")
```

Sequence: (1) the CPU writes the memory address, word count and direction into the DMA controller and continues; (2) the device raises DMA request; the controller asks for the bus with HOLD; (3) the CPU grants (HLDA) at the end of a bus cycle and the controller drives the address bus and moves a word for each request, incrementing the address and decrementing the count; (4) when the count reaches zero the controller interrupts the CPU **once**.

| Basis | Programmed I/O | Interrupt-driven I/O | DMA |
|---|---|---|---|
| Who moves the data | CPU, one word at a time | CPU, one word per interrupt | DMA controller, whole block |
| CPU involvement | continuous (busy waiting) | at each word (interrupt overhead) | only to start and at the end |
| CPU utilisation | very poor | moderate | best |
| Hardware | simplest | interrupt controller | DMA controller |
| Transfer rate | low | medium (limited by the interrupt latency) | high |
| Suitable for | slow devices, small data | slow or irregular devices | disks, network, graphics, bulk data |

Thus DMA overcomes the problems of the two other methods: it removes the CPU's busy-waiting of programmed I/O and the per-word interrupt and context-switch overhead of interrupt-driven I/O, so the CPU is free for computing while large blocks are transferred at bus speed.


@s 8
**Multicore processors and hardware performance.** The performance of a single core was raised for decades by higher clock frequency and deeper instruction-level parallelism, but both ran into the **power wall** (dynamic power $P = C V^{2} f$ with the supply voltage $V$ having to rise with $f$, so power grows roughly as $f^{3}$), the memory wall and the limited instruction-level parallelism in programs. A multicore processor puts several simpler cores on one chip instead.

**Parallelism.** Each core executes its own thread, so the chip does several streams of instructions at the same time: *thread-level parallelism* (and *data-level parallelism* with SIMD units in each core). With $N$ cores the ideal throughput is $N$ times that of one core; the real gain follows Amdahl's law, $\text{Speed-up} = 1/\big((1 - f) + f/N\big)$ ($f = 0.9$, $N = 4$ gives $3.08$). Shared L2/L3 caches, fast on-chip interconnects (bus, ring, mesh) and cache-coherence hardware (MESI) let the cores share data with short latency, much shorter than between separate chips. Combined with hardware multithreading (SMT) each core also hides memory latency.

**Power consumption.** Dynamic power is $P \propto C V^{2} f$ and, since $V$ scales almost in proportion to $f$, $P \propto f^{3}$. Instead of one core at frequency $f$, use two cores at $0.8 f$ each (with a correspondingly lower voltage):

$$\begin{gathered}\text{Performance} = 2 \times 0.8 = 1.6 \quad (\text{ideal, parallel workload}) \\ \text{Power} = 2 \times 0.8^{3} = 1.02\end{gathered}$$

so about 60 percent more performance for nearly the same power; or for the same performance as one core ($2 \times 0.5 = 1$) the power is only $2 \times 0.5^{3} = 0.25$, one quarter. Cores that are idle can be switched off (**power gating**) or slowed down (**DVFS**, dynamic voltage and frequency scaling), and a chip can mix big and little cores (heterogeneous multicore) to match power to the workload. The simpler cores also use less area per core and dissipate heat over a larger area, so cooling is easier.

| Single fast core | Multicore |
|---|---|
| performance only by clock speed and ILP; power rises about as $f^{3}$ | performance by the number of cores; power rises about linearly with cores |
| hot spot, limited by the power wall | heat spread, power gating and DVFS per core |
| one thread at a time (plus ILP) | many threads and processes at once |

Limits: the serial part of a program (Amdahl), memory bandwidth shared between cores, cache-coherence traffic and synchronisation, and the "dark silicon" problem (not all cores can run at full speed at the same time within the power budget).
