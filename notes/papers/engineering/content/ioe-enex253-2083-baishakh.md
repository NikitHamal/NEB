---
file: NEBians-IOE-Past-Paper-Computer-Organization-and-Architecture-ENEX253-2083-Baishakh.pdf
subject: Computer Organization and Architecture
level: BE · Year II / Part II
code: ENEX 253
year_bs: 2083 Baishakh
cal: BS
year_ad: 2026
stream: BEI
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Back (New Course). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
Describe the methods of bus arbitration. Explain the instruction cycle state diagram. [[4+4]]

@q 2
Write a code for $V = (M + N - O/P)\,/\,((Q - R) \times S/T)$ using three, two, one and zero address instruction. [[8]]

@q 3
Explain the function of control unit. Give the differences between hardwired control unit and microprogrammed control unit. [[4+4]]

@q 4
Explain set associative mapping technique with suitable example. Describe the First in First out (FIFO) page replacement algorithm with example. [[5+5]]

@q 5
Explain Booth's Multiplication algorithm with its hardware design implementation. Multiply $8 \times -6 = -48$ using Booth's Multiplication algorithm. [[5+5]]

@q 6
Explain the different types of pipeline hazards with example. [[5]]

@q 7
How does DMA overcome the problems of programmed I/O and interrupt-driven I/O in computer organization. [[5]]

@q 8
Explain about how multicore processors improve the software performance issues. [[6]]

<!-- SOLUTIONS -->

@s 1
**Bus arbitration** decides which of several bus masters (CPU, DMA controllers, I/O processors) may use the shared bus when more than one requests it. A bus master asserts a **bus request (BR)**, the arbiter answers with a **bus grant (BG)**, and the master holds the bus busy (BB) while it transfers. The methods are:

```figure caption="Bus arbitration schemes: (a) daisy chain, (b) polling, (c) independent request. BR = bus request, BG = bus grant, BB = bus busy."
import numpy as _np, matplotlib.patches as mp
def box(ax,x,y,w,h,t,fc="white",ec=INK,fs=8,lw=1.2,ls="-"):
    ax.add_patch(mp.FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",fc=fc,ec=ec,lw=lw,ls=ls,zorder=3))
    ax.text(x,y,t,ha="center",va="center",fontsize=fs,zorder=4)
def arr(ax,a,b,c=None,rad=0.0,lw=1.2,sa=0,sb=0,style="-|>"):
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle=style,color=c or ACCENT,lw=lw,shrinkA=sa,shrinkB=sb,connectionstyle="arc3,rad=%s"%rad),zorder=2)
fig,axs=plt.subplots(1,3,figsize=(7.4,2.9))
for a in axs: a.axis("off"); a.set_xlim(-0.2,4.4); a.set_ylim(-3.8,1.6)
def masters(a,n=3):
    for i in range(n): box(a,0.5+i*1.35,-2.6,1.05,0.7,"M%d"%(i+1),fs=7.5,fc="#fff4d6")
a=axs[0]; a.set_title("(a) Daisy chain",fontsize=7.5); box(a,2.1,0.9,2.0,0.7,"Bus arbiter",fs=7.5,fc="#eaf3ff"); masters(a)
arr(a,(1.2,0.55),(0.5,-2.2),c=ACCENT); a.text(0.15,-0.8,"BG",fontsize=6.5,color="#b00020")
for i in range(2): arr(a,(1.03+i*1.35,-2.6),(1.32+i*1.35,-2.6),c=ACCENT)
ax2=a; a.plot([3.2,3.2],[-2.2,0.55],color=INK,lw=1); a.text(3.3,-0.8,"BR (common)",fontsize=6,rotation=90,va="center"); a.plot([0.5+2*1.35,3.2],[-2.2,-2.2],color=INK,lw=1)
a.text(2.1,-3.5,"grant is passed along the chain",fontsize=6,ha="center")
a=axs[1]; a.set_title("(b) Polling",fontsize=7.5); box(a,2.1,0.9,2.0,0.7,"Arbiter + counter",fs=7,fc="#eaf3ff"); masters(a)
for i in range(3): arr(a,(1.6+i*0.25,0.55),(0.5+i*1.35,-2.2),c=ACCENT)
a.text(2.1,-1.3,"poll address lines",fontsize=6.5,ha="center",color="#b00020"); a.text(2.1,-3.5,"counter polls masters in turn",fontsize=6,ha="center")
a=axs[2]; a.set_title("(c) Independent request",fontsize=7.5); box(a,2.1,0.9,2.0,0.7,"Arbiter",fs=7.5,fc="#eaf3ff"); masters(a)
for i in range(3):
    x=0.5+i*1.35; arr(a,(x-0.2,-2.2),(1.5+i*0.45-0.1,0.55),c=INK); arr(a,(1.6+i*0.45,0.55),(x+0.2,-2.2),c=ACCENT)
a.text(2.1,-3.5,"separate BR/BG pair per master",fontsize=6,ha="center")
```

| Method | Principle | Advantage | Disadvantage |
|---|---|---|---|
| **Daisy chaining** (serial) | all masters share one request line; the grant line passes through the masters in series, so the master nearest to the arbiter has the highest priority and a requesting master absorbs the grant | few wires, simple, easy to add masters | fixed priority, a failure breaks the chain, slow grant propagation, far masters can starve |
| **Polling** (parallel polling by counter) | the controller puts a count on the poll lines; the master whose address matches and that is requesting takes the bus; the counter can start at 0 (fixed priority) or continue from the last winner (rotating, fair) | priority is programmable | needs $\lceil \log_2 n \rceil$ poll lines, slower |
| **Independent requests** (parallel) | every master has its own BR and BG pair; the arbiter has a priority encoder and grants the winner directly | fastest, flexible priority | many lines, more arbiter hardware |

Other schemes: **distributed arbitration by self-selection** (each device puts its identity on shared lines), **rotating priority (round robin)** and **fixed priority**.

**Instruction cycle.** To execute one instruction the processor repeats the cycle

1. **Instruction address calculation**: compute the address of the next instruction (add the length of the current one to the PC);
2. **Instruction fetch**: read the instruction from memory into the instruction register;
3. **Instruction operation decoding**: find the operation type and the operands;
4. **Operand address calculation**: find the effective address of each source operand (may involve indirect or indexed addressing);
5. **Operand fetch**: read the operand from memory or I/O;
6. **Data operation**: perform the arithmetic or logic operation;
7. **Operand address calculation** for the result and **operand store**: write the result to memory or I/O;
8. **Interrupt check**: if an interrupt is pending the processor saves its state and jumps to the interrupt routine, otherwise the next instruction begins.

```figure caption="Instruction cycle state diagram: each instruction passes through address calculation, fetch, decoding, operand address calculation, operand fetch, data operation and result store; the interrupt check follows and the cycle returns to the next instruction."
import numpy as _np, matplotlib.patches as mp
def box(ax,x,y,w,h,t,fc="white",ec=INK,fs=8,lw=1.2,ls="-"):
    ax.add_patch(mp.FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",fc=fc,ec=ec,lw=lw,ls=ls,zorder=3))
    ax.text(x,y,t,ha="center",va="center",fontsize=fs,zorder=4)
def arr(ax,a,b,c=None,rad=0.0,lw=1.2,sa=0,sb=0,style="-|>"):
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle=style,color=c or ACCENT,lw=lw,shrinkA=sa,shrinkB=sb,connectionstyle="arc3,rad=%s"%rad),zorder=2)
fig,ax=plt.subplots(figsize=(7.2,3.0)); ax.axis("off"); ax.set_xlim(-0.4, 11.4); ax.set_ylim(-0.6, 4.2)
B={"iac":(0.9,2.6,"Instruction\naddress\ncalculation"),"if":(3.2,2.6,"Instruction\nfetch"),"iod":(5.5,2.6,"Instruction\noperation\ndecoding"),"oac":(7.8,2.6,"Operand\naddress\ncalculation"),"of":(10.1,2.6,"Operand\nfetch"),
 "do":(10.1,0.6,"Data\noperation"),"oac2":(7.8,0.6,"Operand\naddress\ncalculation"),"os":(5.5,0.6,"Operand\nstore"),"int":(3.2,0.6,"Interrupt\ncheck")}
for k,(x,y,t) in B.items(): box(ax,x,y,1.8,0.95,t,fs=6.5,fc="#eaf3ff" if y>1 else "#fff4d6")
def L(a,b,pa,pb,**kw): arr(ax,pa,pb,**kw)
for a,b in [("iac","if"),("if","iod"),("iod","oac"),("oac","of")]: arr(ax,(B[a][0]+0.92,B[a][1]),(B[b][0]-0.92,B[b][1]))
arr(ax,(10.1,2.1),(10.1,1.1)); 
for a,b in [("do","oac2"),("oac2","os"),("os","int")]: arr(ax,(B[a][0]-0.92,B[a][1]),(B[b][0]+0.92,B[b][1]))
arr(ax,(0.9,1.1),(0.9,2.1)); ax.plot([0.9,3.2-0.92],[0.6,0.6],color=ACCENT,lw=1.2); ax.plot([0.9,0.9],[0.6,1.1],color=ACCENT,lw=1.2); arr(ax,(3.2-0.92,0.6),(0.9,0.6),style="-")
arr(ax,(10.0,3.1),(8.0,3.1),rad=0.45); ax.text(9.0,3.85,"multiple operands",fontsize=6.5,ha="center")
ax.text(1.0,1.65,"next instruction",fontsize=6.5,color="#b00020",ha="left");
ax.text(5.5,-0.3,"multiple results: store loops back to operand address calculation",fontsize=6.5,ha="center")
```

The loops of the diagram handle instructions with several source operands (back to operand address calculation) or several results. In the simple basic-computer view, the cycle is fetch ($T_0$: $AR \leftarrow PC$; $T_1$: $IR \leftarrow M[AR],\ PC \leftarrow PC + 1$), decode ($T_2$), indirect (if $I = 1$) and execute, with the interrupt flip-flop tested at the end.


@s 2
**Rules.** The expression is parsed as $V = \dfrac{M + N - O/P}{\big((Q - R) \times S\big)/T}$ (multiplication and division are left associative). Let T1, T2, T3 be temporary locations. Every program below was executed by computer on random values and gives the same $V$ as the formula.

**(a) Three-address instructions** (`OP dest, src1, src2`, 7 instructions):

```
DIV  T1, O, P        ; T1 = O / P
ADD  T2, M, N        ; T2 = M + N
SUB  T2, T2, T1      ; T2 = M + N - O/P
SUB  T3, Q, R        ; T3 = Q - R
MUL  T3, T3, S       ; T3 = (Q - R) * S
DIV  T3, T3, T       ; T3 = (Q - R) * S / T
DIV  V,  T2, T3      ; V  = T2 / T3
```

**(b) Two-address instructions** (`OP dest, src` with dest = dest OP src, 11 instructions; the first operand is overwritten, so MOV is needed to keep operands):

```
MOV  T1, O           ; T1 = O
DIV  T1, P           ; T1 = O / P
MOV  T2, M           ; T2 = M
ADD  T2, N           ; T2 = M + N
SUB  T2, T1          ; T2 = M + N - O/P
MOV  T3, Q           ; T3 = Q
SUB  T3, R           ; T3 = Q - R
MUL  T3, S           ; T3 = (Q - R) * S
DIV  T3, T           ; T3 = (Q - R) * S / T
DIV  T2, T3          ; T2 = V
MOV  V,  T2          ; V  = T2
```

**(c) One-address instructions** (all arithmetic uses the accumulator AC; 15 instructions):

```
LOAD  O              ; AC = O
DIV   P              ; AC = O / P
STORE T1             ; T1 = O / P
LOAD  M              ; AC = M
ADD   N              ; AC = M + N
SUB   T1             ; AC = M + N - O/P
STORE T2             ; T2 = numerator
LOAD  Q              ; AC = Q
SUB   R              ; AC = Q - R
MUL   S              ; AC = (Q - R) * S
DIV   T              ; AC = (Q - R) * S / T
STORE T3             ; T3 = denominator
LOAD  T2             ; AC = numerator
DIV   T3             ; AC = numerator / denominator
STORE V              ; V = AC
```

**(d) Zero-address (stack) instructions** (operands are on the top of the stack; only PUSH and POP name a memory address; the code is the postfix form $M\,N\,+\,O\,P\,/\,-\,Q\,R\,-\,S\,*\,T\,/\,/$; 16 instructions):

```
PUSH M     PUSH N     ADD                 ; (M + N)
PUSH O     PUSH P     DIV                 ; (O / P)
SUB                                       ; M + N - O/P
PUSH Q     PUSH R     SUB                 ; (Q - R)
PUSH S     MUL                            ; (Q - R) * S
PUSH T     DIV                            ; (Q - R) * S / T
DIV                                       ; numerator / denominator
POP  V
```

| Format | Instructions | Memory references for operands |
|---|---|---|
| Three-address | 7 | 3 per arithmetic instruction (shortest program, long instructions) |
| Two-address | 11 | 2 per instruction |
| One-address | 15 | 1 per instruction (accumulator) |
| Zero-address | 16 | none for ADD, SUB, MUL, DIV (stack), only PUSH / POP |

Fewer address fields make each instruction shorter but the program longer.

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


@s 4
**Set associative mapping.** The cache is divided into $S$ **sets** of $k$ lines each ($k$-way set associative). A main-memory block can go into **exactly one set** (set = block number mod $S$) but into **any of the $k$ lines** of that set. It is a compromise between direct mapping (fast, but conflict misses) and fully associative mapping (flexible, but an expensive comparison of all tags). The memory address is split into

$$\text{Address} = \underbrace{\text{Tag}}_{t\ \text{bits}} \ \Big|\ \underbrace{\text{Set index}}_{s\ \text{bits}} \ \Big|\ \underbrace{\text{Word offset}}_{w\ \text{bits}}$$

The set index selects a set, the tags of the $k$ lines of that set are compared in parallel with the tag of the address: a match is a **hit**, otherwise a **miss** (block fetched into a free line of the set or replacing one chosen by LRU, FIFO or random).

**Address example.** Main memory 1 M words (20-bit address), cache 4 K words, block 16 words, 4-way set associative. Offset $w = \log_2 16 = 4$ bits; number of lines $= 4096/16 = 256$; sets $S = 256/4 = 64$, so $s = 6$ bits; tag $t = 20 - 6 - 4 = 10$ bits.

**Trace example.** Cache of 8 lines, 2-way, so $S = 4$ sets (set = block mod 4), LRU inside a set; reference string of block numbers 0, 4, 0, 4, 8, 0, 1, 5, 1, 5 (blocks 0, 4, 8 all compete for set 0, blocks 1 and 5 for set 1):

| Reference | Set (block mod 4) | Result | Evicted | Contents after the reference (oldest first) |
|---|---|---|---|---|
| 0 | 0 | **miss** | - | set 0: [0] |
| 4 | 0 | **miss** | - | set 0: [0, 4] |
| 0 | 0 | hit | - | set 0: [4, 0] |
| 4 | 0 | hit | - | set 0: [0, 4] |
| 8 | 0 | **miss** | 0 | set 0: [4, 8] |
| 0 | 0 | **miss** | 4 | set 0: [8, 0] |
| 1 | 1 | **miss** | - | set 0: [8, 0]; set 1: [1] |
| 5 | 1 | **miss** | - | set 0: [8, 0]; set 1: [1, 5] |
| 1 | 1 | hit | - | set 0: [8, 0]; set 1: [5, 1] |
| 5 | 1 | hit | - | set 0: [8, 0]; set 1: [1, 5] |

Result: 4 hits and 6 misses (hit ratio $= 4/10$). With direct mapping blocks 0 and 4 would share one line and evict each other on every reference; the two ways of a set keep both blocks, which gives the hits on the repeated references.

**First-in first-out (FIFO) page replacement.** When a page fault occurs and all frames are full, the page that has been in memory **longest** (the oldest, kept in a queue) is replaced. It is simple (a queue pointer), but it can remove a heavily used page and shows **Belady's anomaly** (more frames can give more faults). Reference string 7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1 with 3 frames (the contents are listed oldest first):

| Reference | Set | Result | Evicted | Contents after the reference (oldest first) |
|---|---|---|---|---|
| 7 | - | **miss** | - | [7] |
| 0 | - | **miss** | - | [7, 0] |
| 1 | - | **miss** | - | [7, 0, 1] |
| 2 | - | **miss** | 7 | [0, 1, 2] |
| 0 | - | hit | - | [0, 1, 2] |
| 3 | - | **miss** | 0 | [1, 2, 3] |
| 0 | - | **miss** | 1 | [2, 3, 0] |
| 4 | - | **miss** | 2 | [3, 0, 4] |
| 2 | - | **miss** | 3 | [0, 4, 2] |
| 3 | - | **miss** | 0 | [4, 2, 3] |
| 0 | - | **miss** | 4 | [2, 3, 0] |
| 3 | - | hit | - | [2, 3, 0] |
| 2 | - | hit | - | [2, 3, 0] |
| 1 | - | **miss** | 2 | [3, 0, 1] |
| 2 | - | **miss** | 3 | [0, 1, 2] |
| 0 | - | hit | - | [0, 1, 2] |
| 1 | - | hit | - | [0, 1, 2] |
| 7 | - | **miss** | 0 | [1, 2, 7] |
| 0 | - | **miss** | 1 | [2, 7, 0] |
| 1 | - | **miss** | 2 | [7, 0, 1] |

$$\boxed{\,\text{FIFO: } 15 \text{ page faults, } 5 \text{ hits for 20 references}\,}$$

(LRU on the same string gives 12 faults, optimal replacement 9.)

@s 5
**Booth's algorithm** multiplies two signed numbers in two's complement. It scans the multiplier bits in pairs $Q_0 Q_{-1}$ ($Q_{-1}$ is an extra bit appended on the right, initially 0): pair $10$ marks the **start of a run of 1s** (subtract the multiplicand, $A \leftarrow A - M$), pair $01$ marks the **end of a run of 1s** (add, $A \leftarrow A + M$), and $00$ or $11$ means no operation. After each step the register $A, Q, Q_{-1}$ is **arithmetic-shifted right** by one bit (the sign bit of $A$ is copied). After $n$ cycles the $2n$-bit product is in $A{:}Q$.

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

**Multiplication of $8 \times (-6)$ = -48:**

Multiplicand $M = 8 = 01000$, multiplier $Q = -6 = 11010$ (5-bit two's complement), $-M = 11000$.

| Cycle | $Q_0 Q_{-1}$ | Operation | A after add/subtract | A after shift | Q after shift | $Q_{-1}$ |
|---|---|---|---|---|---|---|
| 0 (initial) | - | - | - | 00000 | 11010 | 0 |
| 1 | 00 | no change | 00000 | 00000 | 01101 | 0 |
| 2 | 10 | A = A - M | 11000 | 11100 | 00110 | 1 |
| 3 | 01 | A = A + M | 00100 | 00010 | 00011 | 0 |
| 4 | 10 | A = A - M | 11010 | 11101 | 00001 | 1 |
| 5 | 11 | no change | 11101 | 11110 | 10000 | 1 |

Product = A:Q = $1111010000$ (10 bits). Its sign bit is 1, so it is negative: two's complement gives $-48$.


@s 6
**Pipeline hazards** are situations that prevent the next instruction from entering the pipeline in its clock cycle and make the pipeline **stall**. There are three types.

**1. Structural hazards** arise from a resource conflict: two instructions need the same hardware in the same cycle (for example one memory port used for instruction fetch of $I_4$ and data access of $I_1$). Remedy: separate instruction and data caches (Harvard style), more functional units, or a stall.

**2. Data hazards** arise when an instruction depends on the result of an earlier instruction that is still in the pipeline:

- **RAW** (read after write, true dependence): `ADD R1,R2,R3` then `SUB R4,R1,R5`;
- **WAR** (write after read, anti-dependence) and **WAW** (write after write, output dependence): occur with out-of-order execution and are removed by register renaming.

```figure caption="Data hazard (RAW) between ADD R1,R2,R3 and SUB R4,R1,R5 in a 5-stage pipeline: top, without forwarding SUB stalls two cycles; bottom, with forwarding there is no stall."
import numpy as _np, matplotlib.patches as mp
def box(ax,x,y,w,h,t,fc="white",ec=INK,fs=8,lw=1.2,ls="-"):
    ax.add_patch(mp.FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",fc=fc,ec=ec,lw=lw,ls=ls,zorder=3))
    ax.text(x,y,t,ha="center",va="center",fontsize=fs,zorder=4)
def arr(ax,a,b,c=None,rad=0.0,lw=1.2,sa=0,sb=0,style="-|>"):
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle=style,color=c or ACCENT,lw=lw,shrinkA=sa,shrinkB=sb,connectionstyle="arc3,rad=%s"%rad),zorder=2)
fig,ax=plt.subplots(figsize=(7.0,3.3)); ax.axis("off"); ax.set_xlim(-3.6,9.4); ax.set_ylim(-5.4,1.4)
col={"IF":"#eaf3ff","ID":"#eaf3ff","EX":"#fff4d6","MEM":"#e8f6e8","WB":"#f3e8f6","stall":"#ffd6d6"}
def row(y,label,cells):
    ax.text(-0.2,y,label,ha="right",va="center",fontsize=7)
    for st,c in cells: box(ax,c,y,0.88,0.55,st,fc=col[st],fs=6.3)
for c in range(1,9): ax.text(c,1.0,str(c),ha="center",fontsize=6.5,color="#555")
ax.text(-0.2,1.0,"cycle",ha="right",fontsize=6.5,color="#555")
row(0.2,"ADD R1,R2,R3",[("IF",1),("ID",2),("EX",3),("MEM",4),("WB",5)])
row(-0.6,"SUB R4,R1,R5",[("IF",2),("ID",3),("stall",4),("ID",5),("EX",6),("MEM",7),("WB",8)])
ax.text(3.9,-1.15,"SUB reads R1 only in cycle 5 (after ADD writes it): 2 stall cycles",fontsize=6.5,ha="center",color="#b00020")
row(-2.6,"ADD R1,R2,R3",[("IF",1),("ID",2),("EX",3),("MEM",4),("WB",5)])
row(-3.4,"SUB R4,R1,R5",[("IF",2),("ID",3),("EX",4),("MEM",5),("WB",6)])
arr(ax,(3.3,-2.85),(4.0,-3.15),c="#b00020"); ax.text(5.6,-4.2,"forwarding path: EX/MEM result of ADD goes straight to the ALU input of SUB",fontsize=6.5,ha="center",color="#b00020")
```

Without forwarding the SUB must wait until ADD has written R1 (2 stall cycles); with **forwarding (bypassing)** the ALU output of the ADD is fed straight to the next instruction's ALU input and there is no stall. A load followed by a dependent instruction still needs one stall (**load-use hazard**). Other remedies: compiler instruction scheduling and hardware **interlocks** (stalls).

**3. Control (branch) hazards** arise from branches and jumps: the target is known only after the branch is decided, so the instructions fetched after it may be wrong. Example: with a branch decided in the 3rd stage, two fetched instructions are flushed (a penalty of 2 cycles per taken branch). Remedies: **pipeline flushing**, **predict-not-taken or branch prediction** (static or dynamic with a branch history table), **branch target buffer**, **delayed branch** (fill the delay slot with a useful instruction), early branch resolution in the decode stage.

**Effect on speed-up.** For $k$ stages and $n$ instructions the ideal speed-up is $\dfrac{nk}{k + n - 1} \to k$; with an average stall of $s$ cycles per instruction the speed-up falls to about $\dfrac{k}{1 + s}$.

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
**Multicore processors and software performance.** A multicore processor places two or more independent processing cores (each with its own registers and L1 caches, usually sharing L2/L3 cache and the memory interface) on one chip. Single-core clock speeds stopped rising because of the power and heat wall, so performance now comes from **parallelism**; the software side of the problem is:

1. **Thread-level and process-level parallelism.** Independent tasks, threads or processes run on different cores simultaneously, so an operating system running many programs, or a multithreaded program (web server, database, rendering, compilers), gets near-linear throughput gains up to the number of runnable threads.
2. **Speed-up is limited by the serial part (Amdahl's law).** If a fraction $f$ of the program can be parallelised over $N$ cores, $\text{Speed-up} = \dfrac{1}{(1 - f) + f/N}$. Example: $f = 0.8$, $N = 4$ gives $\dfrac{1}{0.2 + 0.2} = 2.5$; even with unlimited cores the limit is $1/(1 - f) = 5$. So software must be restructured to reduce the serial fraction (Gustafson: with a bigger problem size the parallel fraction grows).
3. **Software must be written for parallel hardware**: threads (POSIX threads, Java threads), OpenMP, task libraries, parallel loops and data-parallel frameworks. An old single-threaded program does not become faster by itself, although the cores still run other programs at the same time.
4. **Communication and synchronisation overhead**: locks, barriers and atomic operations serialise execution; shared data needs **cache coherence** (MESI), and false sharing or contention for the shared memory bus can cancel the gains. Good software partitions the data, reduces sharing and balances the load.
5. **Better responsiveness and isolation**: one core can run the user interface while another does background work; virtualisation gives each virtual machine its own cores.
6. **Power efficiency**: several slower cores give more total work per watt than one very fast core, so software can run longer on a battery.

Thus multicore processors improve the performance of software that exposes parallelism (multithreaded, multi-programmed, data-parallel), but the gain depends on the parallel fraction, load balance, synchronisation and memory behaviour of the program.
