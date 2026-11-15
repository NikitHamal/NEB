---
file: NEBians-IOE-Past-Paper-Microprocessor-ENEX201-2082-Chaitra.pdf
subject: Microprocessor
level: BE · Year II / Part I
code: ENEX201
year_bs: 2082 Chaitra
cal: BS
year_ad: 2026
stream: BEI, BCT
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular (New Course). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
Differentiate microprocessors and microcontrollers. Explain the bus organization of microprocessor with block diagram. [[3+3]]

@q 2
Define flags. Explain the flags associated with 8085 microprocessor. [[3]]

@q 3
Draw and explain the timing diagram of MVI M. Also calculate the total execution time. [[5+1]]

@q 4
Write a program for 8085 microprocessor to transfer eight-bit numbers from A000H to B000H if bit D6 is 1 and D2 is 0. Otherwise transfer data by complementing bit D1 and D5. Assume there are ten numbers. [[6]]

@q 5
Draw the internal architecture of 8086 microprocessor and explain each unit. How is physical address calculated in 8086 microprocessor? [[2+4+2]]

@q 6
What are directives in assembly language programming? Explain different assembler directives used in assembly language programming. [[1+4]]

@q 7
Write an assembly language program for 8086 that accepts string from the user and display each character in newline of a clear screen. Also display the total length of string. [[5]]

@q 8
Design an address decoding circuit to interface two 1K EPROM and one 2K RAM consecutively using 3 to 8 decoder starting memory location 1000H. [[6]]

@q 9
Define PPI. Explain the operating modes of Intel 8255A PPI. Explain how control word is made. [[1+3+2]]

@q 10
What is interrupt service routine? Explain different interrupt signals of 8085 microprocessor and how are they used. [[1+5]]

@q 11
Differentiate RISC and CISC processor architectures. [[3]]
<!-- SOLUTIONS -->

@s 1
**Microprocessor versus microcontroller.**

| Basis | Microprocessor | Microcontroller |
|---|---|---|
| Chip contains | CPU only (ALU, registers, control unit) | CPU + ROM + RAM + timers + serial port + I/O ports + interrupt logic on one chip |
| Memory and I/O | external chips must be added (address decoding, latches) | internal, little external hardware needed |
| System size and cost | larger board, higher cost | small, cheap, low power |
| Instruction set | many instructions for data-processing; few bit-handling instructions | many bit-addressable instructions and I/O oriented instructions |
| Use | general-purpose computers, flexible systems (PC) | dedicated, embedded applications (washing machine, remote, meter) |
| Speed / word size | high clock, large address space | lower clock, small memory |
| Example | 8085, 8086, Pentium | 8051, PIC16F877, AVR ATmega328 |

**Bus organization of a microprocessor.**

A **microprocessor-based system** has three blocks joined by three buses.

- **CPU (microprocessor):** fetches, decodes and executes instructions: ALU, registers, control unit.
- **Memory:** ROM / EPROM (monitor program, fixed data) and RAM (user programs, variable data, stack).
- **Input / output devices:** keyboard, display, ADC, sensors, printer, through interface chips (8255 PPI, 8251 USART, 8253 timer, 8259 PIC, 8257 DMA).

```figure caption="Organization of a microprocessor-based system: the CPU, memory and I/O devices are connected by the address, data and control buses."
import numpy as _np, matplotlib.patches as mp
def box(ax,x,y,w,h,t,fc="white",ec=INK,fs=8,lw=1.2,ls="-"):
    ax.add_patch(mp.FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",fc=fc,ec=ec,lw=lw,ls=ls,zorder=3))
    ax.text(x,y,t,ha="center",va="center",fontsize=fs,zorder=4)
def arr(ax,a,b,c=None,rad=0.0,lw=1.2,sa=0,sb=0,style="-|>"):
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle=style,color=c or ACCENT,lw=lw,shrinkA=sa,shrinkB=sb,connectionstyle="arc3,rad=%s"%rad),zorder=2)
BLUE="#eaf3ff"; YEL="#fff4d6"; GRN="#e6f4ea"; RED="#fde8e8"
fig,ax=plt.subplots(figsize=(7.4,3.8)); ax.axis("off"); ax.set_xlim(0,14.8); ax.set_ylim(0,7.6)
box(ax,2.0,5.2,3.2,1.8,"CPU\n(microprocessor)\nALU, registers,\ncontrol unit",fs=7.5,fc=YEL)
box(ax,7.4,6.4,3.0,1.0,"ROM / EPROM",fs=8,fc=GRN); box(ax,7.4,4.8,3.0,1.0,"RAM",fs=8,fc=GRN)
box(ax,12.6,6.4,3.4,1.0,"Input device\n(keyboard, switches)",fs=7,fc=BLUE); box(ax,12.6,4.8,3.4,1.0,"Output device\n(display, LEDs)",fs=7,fc=BLUE)
for y,t,c in [(2.9,"Address bus  (A15 - A0, unidirectional)","#c62828"),(2.0,"Data bus  (D7 - D0, bidirectional)","#1565c0"),(1.1,"Control bus  (RD, WR, IO/M, ALE, READY, INTR ...)","#2e7d32")]:
    ax.plot([0.4,14.4],[y,y],color=c,lw=2.4); ax.text(7.4,y+0.2,t,fontsize=7,ha="center",color=c)
for x in (2.0,7.4,12.6):
    for y in (2.9,2.0,1.1): ax.plot([x],[y],"o",color=INK,ms=3)
ax.plot([2.0,2.0],[4.3,1.1],color="#777",lw=1); ax.plot([7.4,7.4],[4.3,1.1],color="#777",lw=1); ax.plot([12.6,12.6],[4.3,1.1],color="#777",lw=1)
ax.text(7.4,7.2,"Memory",fontsize=8,ha="center",weight="bold"); ax.text(12.6,7.2,"I/O devices (via interface, e.g. 8255)",fontsize=7.5,ha="center",weight="bold")
```


**Bus organization (8085 as example).**

| Bus | Width | Direction | Purpose |
|---|---|---|---|
| Address bus | 16 lines A15-A0 (A15-A8 are dedicated, A7-A0 are multiplexed with the data bus) | unidirectional, CPU to memory / I/O | selects one of $2^{16}=64$ KB memory locations (or one of 256 I/O ports) |
| Data bus | 8 lines D7-D0 (AD7-AD0) | bidirectional | carries instructions and data between the CPU, memory and I/O |
| Control bus | RD, WR, IO/M, ALE, S0, S1, READY, HOLD, INTR, ... | mostly CPU outputs | timing and type of the transfer (memory or I/O, read or write) |

The low address byte shares the pins AD7-AD0 with the data (**multiplexing**). During T1 of every machine cycle ALE = 1 and the 74LS373 latch stores the low address byte; during T2-T3 the same pins carry data, so a 16-bit address and 8-bit data need only 8 + 8 + 8 = 24 pins instead of 32.

@s 2
A **flag** is a 1-bit flip-flop (a bit of the *flag register* or program status word) that records a condition produced by the last arithmetic or logical instruction. Flags are tested by conditional jump, call and return instructions, so that the program can take decisions.

The 8085 has five flags in the 8-bit flag register (D7 D6 - D4 - D2 - D0 = S Z x AC x P x CY; the x bits are undefined):

| Flag | Bit | Meaning (set to 1 when) | Example |
|---|---|---|---|
| **S** sign | D7 | the result is negative (bit D7 of the result is 1) | 05H - 08H = FDH, so S = 1 |
| **Z** zero | D6 | the result is zero | 05H - 05H = 00H, so Z = 1 |
| **AC** auxiliary carry | D4 | there is a carry from bit D3 to D4 (used by DAA, BCD arithmetic) | 08H + 09H = 11H, carry out of the low nibble, AC = 1 |
| **P** parity | D2 | the result has an even number of 1 bits (even parity) | 03H = 0000 0011, two 1s, P = 1 |
| **CY** carry | D0 | the operation produces a carry (addition) or a borrow (subtraction / compare) out of D7 | F0H + 20H = 110H, CY = 1 |

INR, DCR and INX / DCX do not affect CY (INX and DCX affect no flag at all); logical instructions (ANA, ORA, XRA) clear CY, and ANA sets AC.

@s 3
**MVI M, data** (opcode 36H, 2 bytes) loads the immediate byte into the memory location whose address is in the HL pair: $[HL]\leftarrow$ data. It needs **three machine cycles and 10 T-states**.

| Machine cycle | T-states | IO/M | What happens |
|---|---|---|---|
| 1. **Opcode fetch (M1)** | 4 | 0 (memory), S1 S0 = 1 1 | PC (PCH on A15-A8, PCL on AD7-AD0) is output, ALE = 1 in T1 latches PCL; $\overline{RD}$ low in T2-T3 reads the opcode 36H into the instruction register; PC is incremented; T4 decodes the opcode |
| 2. **Memory read (M2)** | 3 | 0, S1 S0 = 1 0 | address = PC; $\overline{RD}$ low in T2-T3 reads the second byte (the data) into a temporary register; PC is incremented |
| 3. **Memory write (M3)** | 3 | 0, S1 S0 = 0 1 | the address in HL (H on A15-A8, L on AD7-AD0, latched by ALE in T1) is output, the data from the temporary register is put on AD7-AD0 in T2 and $\overline{WR}$ goes low in T2-T3 to write the byte into memory |

```figure caption="Timing diagram of MVI M, data (opcode 36H): opcode fetch (4 T), memory read of the data byte (3 T) and memory write to the location addressed by HL (3 T) = 10 T-states."
import numpy as _np, matplotlib.patches as mp
def box(ax,x,y,w,h,t,fc="white",ec=INK,fs=8,lw=1.2,ls="-"):
    ax.add_patch(mp.FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",fc=fc,ec=ec,lw=lw,ls=ls,zorder=3))
    ax.text(x,y,t,ha="center",va="center",fontsize=fs,zorder=4)
def arr(ax,a,b,c=None,rad=0.0,lw=1.2,sa=0,sb=0,style="-|>"):
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle=style,color=c or ACCENT,lw=lw,shrinkA=sa,shrinkB=sb,connectionstyle="arc3,rad=%s"%rad),zorder=2)
BLUE="#eaf3ff"; YEL="#fff4d6"; GRN="#e6f4ea"; RED="#fde8e8"
fig,ax=plt.subplots(figsize=(7.4,4.4)); ax.set_xlim(0,10.9); ax.set_ylim(-0.4,8.6); ax.axis("off")
bands=[("Opcode fetch (M1)",0,4,YEL),("Memory read (M2)",4,3,BLUE),("Memory write (M3)",7,3,GRN)]
for n,x0,l,c in bands:
    ax.add_patch(mp.Rectangle((x0+0.9,7.6),l,0.6,fc=c,ec=INK,lw=1,zorder=2)); ax.text(x0+0.9+l/2,7.9,n,ha="center",va="center",fontsize=7)
lab=["T1","T2","T3","T4","T1","T2","T3","T1","T2","T3"]
for t in range(10):
    ax.text(0.9+t+0.5,7.3,lab[t],fontsize=6.3,ha="center"); ax.plot([0.9+t,0.9+t],[0.3,7.2],color="#cccccc",lw=0.6,zorder=0)
ax.plot([10.9,10.9],[0.3,7.2],color="#cccccc",lw=0.6,zorder=0)
for n,y in {"CLK":6.4,"ALE":5.4,"IO/M":4.4,"RD":3.4,"WR":2.6,"A15-A8":1.6,"AD7-AD0":0.4}.items(): ax.text(0.8,y+0.1,n,fontsize=7.3,ha="right",va="center")
for t in range(10): ax.plot([0.9+t,0.9+t,0.9+t+0.5,0.9+t+0.5,0.9+t+1],[6.1,6.7,6.7,6.1,6.1],color=INK,lw=1)
for s in (0,4,7): ax.plot([0.9+s,0.9+s,0.9+s+1,0.9+s+1],[5.1,5.7,5.7,5.1],color=INK,lw=1.3)
ax.plot([0.9,0.9+10],[5.1,5.1],color=INK,lw=1.0)
ax.plot([0.9,10.9],[4.1,4.1],color=INK,lw=1.3); ax.text(5.9,4.2,"IO/M = 0 (memory cycles)",fontsize=6.3,ha="center",va="bottom",color="#555")
def low(y,spans,hi=0.6):
    X=[0.9]; Y=[y+hi]
    for a,b in spans: X+=[0.9+a,0.9+a,0.9+b,0.9+b]; Y+=[y+hi,y,y,y+hi]
    X.append(10.9); Y.append(y+hi); ax.plot(X,Y,color=INK,lw=1.3)
low(3.0,[(1,3),(5,7)]); low(2.2,[(8,10)])
ax.text(8.4,3.45,"RD high",fontsize=6.3,ha="center",color="#555")
def bus(y,spans,h=0.55):
    for a,b,t,c in spans: ax.add_patch(mp.Rectangle((0.9+a,y),b-a,h,fc=c,ec=INK,lw=1,zorder=2)); ax.text(0.9+(a+b)/2,y+h/2,t,ha="center",va="center",fontsize=6.2,zorder=3)
bus(1.3,[(0,4,"PCH",BLUE),(4,7,"PCH (PC+1)",BLUE),(7,10,"H (address of M)",GRN)])
bus(0.1,[(0,0.5,"PCL",YEL),(0.5,4,"opcode 36H",BLUE),(4,4.5,"PCL+1",YEL),(4.5,7,"data byte",BLUE),(7,7.5,"L",GRN),(7.5,10,"data out",GRN)])
ax.text(5.9,-0.35,"10 T-states in 3 machine cycles",fontsize=8,ha="center",weight="bold")
```


At the start of every machine cycle ALE goes high for one T-state to latch the low address byte. IO/M stays low because only memory is accessed. RD is active only in M1 and M2; WR is active only in M3.

**Execution time.** Total states $=4+3+3=10$ T. One T-state is one clock period of the internal clock, $T=1/f$. For the clock frequency $f=3$ MHz,

$$\begin{gathered}T=\frac{1}{3\times10^{6}}=0.333\ \mu s \\ t=10\times0.333\ \mu s=\mathbf{3.33\ \mu s}.\end{gathered}$$

(For a 5 MHz clock it is $10\times0.2=2\ \mu s$; in general $t=10/f$.)

@s 4
**Algorithm.** For each of the 10 numbers: test bits D6 and D2 using the mask 44H (0100 0100); if the result is 40H (D6 = 1 and D2 = 0) copy the number unchanged; otherwise complement bits D1 and D5 with XRI 22H (0010 0010, because XOR with 1 complements a bit) and store at the destination. `MOV` does not affect the flags, so the Z flag from `CPI` can be used after reloading A.

```asm
        LXI  H, A000H     ; HL = source pointer
        LXI  D, B000H     ; DE = destination pointer
        MVI  C, 0AH       ; counter = 10 numbers
NEXT:   MOV  A, M         ; A = number
        MOV  B, A         ; keep a copy in B
        ANI  44H          ; isolate D6 and D2
        CPI  40H          ; D6 = 1 and D2 = 0 ?
        MOV  A, B         ; (flags unchanged) reload the number
        JZ   STORE        ; yes: transfer unchanged
        XRI  22H          ; no: complement D5 and D1
STORE:  STAX D            ; [DE] = A
        INX  H
        INX  D
        DCR  C
        JNZ  NEXT         ; repeat for 10 numbers
        HLT
```

*Check (program run on an 8085 simulator).* Sample source bytes 44H, 40H, 4CH, FFH, 00H, C4H, 04H, 46H, 7FH, 55H are copied as 66H (D6 = 1 but D2 = 1, so D5 and D1 complemented: 44H xor 22H), 40H (D6 = 1, D2 = 0: unchanged), 6EH, DDH, 22H, E6H, 26H, 64H, 5DH, 77H; every result matches the rule.

@s 5
The **8086** is a 16-bit microprocessor with a 20-bit address bus (1 MB memory), 16-bit data bus (AD0-AD15 multiplexed), 40-pin package and a 5 MHz to 10 MHz clock. It is divided into two independent units that work in parallel (**pipelining**: instruction fetch overlaps execution).

```figure caption="Internal block diagram of the 8086: the Bus Interface Unit (left) fetches instructions into the 6-byte queue and forms 20-bit addresses; the Execution Unit (right) decodes and executes them."
import numpy as _np, matplotlib.patches as mp
def box(ax,x,y,w,h,t,fc="white",ec=INK,fs=8,lw=1.2,ls="-"):
    ax.add_patch(mp.FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",fc=fc,ec=ec,lw=lw,ls=ls,zorder=3))
    ax.text(x,y,t,ha="center",va="center",fontsize=fs,zorder=4)
def arr(ax,a,b,c=None,rad=0.0,lw=1.2,sa=0,sb=0,style="-|>"):
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle=style,color=c or ACCENT,lw=lw,shrinkA=sa,shrinkB=sb,connectionstyle="arc3,rad=%s"%rad),zorder=2)
BLUE="#eaf3ff"; YEL="#fff4d6"; GRN="#e6f4ea"; RED="#fde8e8"
fig,ax=plt.subplots(figsize=(7.4,4.6)); ax.axis("off"); ax.set_xlim(0,14.8); ax.set_ylim(0,9.2)
ax.add_patch(mp.Rectangle((0.2,0.3),6.4,8.6,fc="#f6f9ff",ec=INK,lw=1.2,ls="--",zorder=1)); ax.text(3.4,8.6,"Bus Interface Unit (BIU)",ha="center",fontsize=9,weight="bold")
ax.add_patch(mp.Rectangle((8.2,0.3),6.4,8.6,fc="#fffaf0",ec=INK,lw=1.2,ls="--",zorder=1)); ax.text(11.4,8.6,"Execution Unit (EU)",ha="center",fontsize=9,weight="bold")
# BIU
for i,(n) in enumerate(["ES","CS","SS","DS"]): box(ax,1.0+i*1.1,7.5,1.0,0.6,n,fs=7.5,fc=BLUE)
box(ax,3.4,6.5,5.8,0.6,"Instruction pointer (IP)",fs=7.5,fc=BLUE)
box(ax,3.4,5.4,5.8,0.8,"Address adder\n(segment x 16 + offset = 20-bit address)",fs=6.3,fc=YEL)
box(ax,3.4,3.9,5.8,1.0,"Instruction queue\n6 bytes (FIFO): 1 | 2 | 3 | 4 | 5 | 6",fs=7,fc=GRN)
box(ax,3.4,2.2,5.8,0.9,"Bus control logic\n(address, data, control signals)",fs=7)
box(ax,3.4,0.8,5.8,0.0001,"",fs=1,ec="white")
# EU
box(ax,9.7,7.5,2.6,0.7,"Control circuitry",fs=7,fc=YEL); box(ax,12.9,7.5,2.6,0.7,"Instr. decoder",fs=7,fc=YEL)
for i,n in enumerate(["AX (AH AL)","BX (BH BL)","CX (CH CL)","DX (DH DL)"]): box(ax,9.7+(i%2)*3.2,6.0-(i//2)*0.85,3.0,0.65,n,fs=7,fc=BLUE)
for i,n in enumerate(["SP","BP","SI","DI"]): box(ax,9.0+i*1.35,3.9,1.2,0.6,n,fs=7.5,fc=BLUE)
box(ax,9.7,2.7,2.6,0.8,"ALU",fs=9,fc=YEL); box(ax,12.9,2.7,2.6,0.8,"Flag register",fs=7.5,fc=BLUE)
box(ax,11.4,1.2,5.8,0.6,"Temporary operand registers",fs=7,fc=GRN)
# connections
arr(ax,(6.6,5.4),(8.2,5.4),c=INK,style="<|-|>"); ax.text(7.4,5.7,"internal\nbus",fontsize=6.3,ha="center")
arr(ax,(3.4,3.4),(3.4,2.65),c=ACCENT,style="<|-|>"); arr(ax,(3.4,4.4+0.5),(3.4,5.05),c=ACCENT); arr(ax,(3.4,6.2),(3.4,5.75),c=ACCENT)
arr(ax,(6.3,3.9),(7.5,3.9),c=INK); ax.text(7.45,4.2,"to decoder",fontsize=6.3,ha="center")
arr(ax,(3.4,1.75),(3.4,0.62),c=INK,style="<|-|>"); ax.text(3.4,0.45,"system bus (A0-A19, D0-D15)",fontsize=7,ha="center")
arr(ax,(11.6,7.5),(11.0,7.5),c=INK,sa=0)
```


**Bus interface unit (BIU).** Fetches instructions, reads / writes data in memory and I/O, and calculates the 20-bit physical address.

- **Segment registers** CS, DS, SS, ES (16 bit each) hold the base addresses of the code, data, stack and extra segments.
- **Instruction pointer (IP)**, 16 bit: offset of the next instruction in the code segment.
- **Address adder:** forms the physical address.
- **Instruction queue:** 6-byte FIFO; the BIU pre-fetches up to six instruction bytes while the EU is busy, so the EU rarely waits for a fetch.
- **Bus control logic:** generates the address, data and control signals.

**Execution unit (EU).** Decodes and executes the instructions taken from the queue.

- **General-purpose registers** AX, BX, CX, DX (each splits into the 8-bit halves AH / AL, BH / BL, CH / CL, DH / DL). AX accumulator, BX base, CX count, DX data / I/O port address.
- **Pointer and index registers** SP, BP (stack), SI, DI (source and destination index).
- **ALU** (16 bit), **flag register** (9 flags used) and the **control unit** with the instruction decoder and timing logic.

**Physical address calculation.** Memory is divided into logical segments of at most 64 KB which start at addresses divisible by 16. The BIU shifts the 16-bit segment base left by 4 bits (multiplies by 16) and adds the 16-bit offset:

$$\text{Physical address}=\text{Segment}\times 10\text{H}+\text{Offset}.$$

For example, DS = 2000H and offset = 0050H give $20000\text{H}+0050\text{H}=\mathbf{20050H}$. For the next instruction CS = 4000H, IP = 1234H give 41234H.

@s 6
**Directives (pseudo-operations)** are statements of an assembly language program that are meant for the **assembler**, not for the CPU: they give instructions to the assembler about how to translate the program (define data, reserve memory, set the origin, define segments and procedures). They produce **no machine code** (opcode) themselves, whereas an instruction is converted to machine code and executed by the processor at run time.

**Assembler directives of the 8086 (MASM / TASM):**

| Directive | Purpose | Example |
|---|---|---|
| `DB`, `DW`, `DD`, `DQ`, `DT` | define byte, word, double word, quad word, ten bytes of data | `NUM DB 25H`; `ARR DW 1234H, 5678H` |
| `DUP` | repeat (reserve and initialise) | `BUF DB 10 DUP(0)` |
| `EQU` | give a constant a name (no memory used) | `COUNT EQU 10` |
| `SEGMENT` ... `ENDS` | begin / end a logical segment | `DATA SEGMENT` ... `DATA ENDS` |
| `ASSUME` | tell the assembler which segment is addressed by which segment register | `ASSUME CS:CODE, DS:DATA` |
| `PROC` ... `ENDP` | begin / end a procedure (NEAR or FAR) | `MAIN PROC FAR` |
| `ORG` | set the location counter (origin) | `ORG 100H` |
| `END` | end of the source file (and the start label) | `END START` |
| `OFFSET`, `PTR` | offset of a label; override the data type | `MOV BX, OFFSET ARR`; `MOV BYTE PTR [SI], 5` |
| `.MODEL`, `.STACK`, `.DATA`, `.CODE` | simplified segment definitions | `.MODEL SMALL`; `.STACK 100H` |
| `MACRO` ... `ENDM` | define a macro | `PRINT MACRO MSG` ... `ENDM` |
| `PUBLIC`, `EXTRN` | share names between separately assembled modules | `PUBLIC SUM` |
| `LABEL`, `EVEN`, `NAME`, `TITLE` | type a label, align on an even address, name the module, title of the listing | `EVEN` |

Example of a skeleton using the directives:

```asm
        .MODEL SMALL
        .STACK 100H
        .DATA
MSG     DB  'HELLO$'
        .CODE
MAIN    PROC
        MOV AX, @DATA
        MOV DS, AX
        ...
MAIN    ENDP
        END MAIN
```

@s 7
**Method.** DOS function 0AH (buffered keyboard input) reads the string into a buffer whose first byte is the maximum size, the second byte receives the **number of characters typed** (the length) and the characters follow. The screen is cleared with BIOS INT 10H, function 06H (scroll window with AL = 0). Each character is printed with function 02H, preceded by a carriage return and line feed (0DH, 0AH), so that every character appears on a new line. At the end the length is converted to decimal digits and displayed.

```asm
        .MODEL SMALL
        .STACK 100H
        .DATA
MSG1    DB  'Enter a string: $'
MSG2    DB  0DH, 0AH, 'Total length = $'
BUF     DB  50, ?, 50 DUP(0)     ; max 50 chars, count, characters
        .CODE
MAIN    PROC
        MOV  AX, @DATA
        MOV  DS, AX
        ; ---- clear the screen and home the cursor ----
        MOV  AX, 0600H           ; AH = 06 scroll up, AL = 0 clear all
        MOV  BH, 07H             ; normal attribute
        MOV  CX, 0000H           ; upper left (row 0, col 0)
        MOV  DX, 184FH           ; lower right (row 24, col 79)
        INT  10H
        MOV  AH, 02H             ; set cursor position
        MOV  BH, 00H
        MOV  DX, 0000H
        INT  10H
        ; ---- accept the string ----
        LEA  DX, MSG1
        MOV  AH, 09H
        INT  21H
        LEA  DX, BUF
        MOV  AH, 0AH
        INT  21H
        ; ---- display each character on a new line ----
        MOV  CL, [BUF+1]         ; CL = number of characters typed
        MOV  CH, 00H
        LEA  SI, BUF+2           ; SI -> first character
        JCXZ LEN                 ; empty string
NEXT:   MOV  AH, 02H
        MOV  DL, 0DH             ; carriage return
        INT  21H
        MOV  DL, 0AH             ; line feed
        INT  21H
        MOV  DL, [SI]            ; the character
        INT  21H
        INC  SI
        LOOP NEXT
        ; ---- display the total length (00 - 50) ----
LEN:    LEA  DX, MSG2
        MOV  AH, 09H
        INT  21H
        MOV  AL, [BUF+1]
        MOV  AH, 00H
        MOV  BL, 10
        DIV  BL                  ; AL = tens, AH = units
        MOV  BX, AX              ; BL = tens, BH = units
        CMP  BL, 0
        JE   UNITS               ; suppress a leading zero
        MOV  DL, BL
        ADD  DL, 30H
        MOV  AH, 02H
        INT  21H
UNITS:  MOV  DL, BH
        ADD  DL, 30H
        MOV  AH, 02H
        INT  21H
        MOV  AH, 4CH             ; exit to DOS
        INT  21H
MAIN    ENDP
        END  MAIN
```

*Example.* Input `HELLO` prints H, E, L, L, O each on its own line and then `Total length = 5`. The count comes from the second byte of the buffer, which DOS fills with the number of characters typed (the final carriage return is not counted).

@s 8
**Step 1: memory size and address lines.** A 1 KB chip has $2^{10}$ bytes, so it needs 10 address lines A0-A9 (A0-A9 go directly to the chip). A 2 KB chip has $2^{11}$ bytes and needs 11 lines A0-A10. The three chips are placed one after another from 1000H.

**Step 2: address map.**

| Chip | Start | End | A15 A14 A13 | A12 | A11 | A10 | Lines to chip |
|---|---|---|---|---|---|---|---|
| EPROM 1 (1 KB) | 1000H | 13FFH | 0 0 0 | 1 | 0 | 0 | A0-A9 |
| EPROM 2 (1 KB) | 1400H | 17FFH | 0 0 0 | 1 | 0 | 1 | A0-A9 |
| RAM (2 KB) | 1800H | 1FFFH | 0 0 0 | 1 | 1 | x | A0-A10 |

(1000H = 0001 0000 0000 0000, 13FFH = 0001 0011 1111 1111, 1400H = 0001 0100 0000 0000, 17FFH = 0001 0111 1111 1111, 1800H = 0001 1000 0000 0000, 1FFFH = 0001 1111 1111 1111.)

**Step 3: decoder connections.** A 74LS138 is used. Its select inputs are $C=A_{12}$, $B=A_{11}$, $A=A_{10}$. The enables are: G1 $=\overline{A_{15}+A_{14}+A_{13}}$ (a 3-input NOR gate, high when A15 = A14 = A13 = 0), G2A $=$ IO/M (must be 0, memory access), G2B = GND. Then

- $CBA=100$ gives $\overline{Y_4}=0$: addresses 1000H-13FFH, connected to the chip select of **EPROM 1**;
- $CBA=101$ gives $\overline{Y_5}=0$: 1400H-17FFH, to **EPROM 2**;
- the RAM occupies two 1 KB decoder blocks, $CBA=110$ (1800H-1BFFH) and $CBA=111$ (1C00H-1FFFH), so its chip select is the AND of $\overline{Y_6}$ and $\overline{Y_7}$ (low when either is low): $\overline{CS}_{RAM}=\overline{Y_6}\cdot\overline{Y_7}$, giving 1800H-1FFFH.

```figure caption="Address decoding with a 74LS138: Y4 selects EPROM 1 (1000H-13FFH), Y5 selects EPROM 2 (1400H-17FFH) and the AND of Y6 and Y7 selects the 2 KB RAM (1800H-1FFFH)."
import numpy as _np, matplotlib.patches as mp
def box(ax,x,y,w,h,t,fc="white",ec=INK,fs=8,lw=1.2,ls="-"):
    ax.add_patch(mp.FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",fc=fc,ec=ec,lw=lw,ls=ls,zorder=3))
    ax.text(x,y,t,ha="center",va="center",fontsize=fs,zorder=4)
def arr(ax,a,b,c=None,rad=0.0,lw=1.2,sa=0,sb=0,style="-|>"):
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle=style,color=c or ACCENT,lw=lw,shrinkA=sa,shrinkB=sb,connectionstyle="arc3,rad=%s"%rad),zorder=2)
BLUE="#eaf3ff"; YEL="#fff4d6"; GRN="#e6f4ea"; RED="#fde8e8"
TITLE='Address decoding: 2 x 1 KB EPROM and 1 x 2 KB RAM from 1000H'; SEL=[('C', 'A12'), ('B', 'A11'), ('A', 'A10')]; ENAB='G1 = NOR(A15, A14, A13)   G2A = IO/M   G2B = GND'; CHIPS=[('EPROM 1', '1K x 8', '1000H - 13FFH', [4], 'A0-A9, D0-D7, RD'), ('EPROM 2', '1K x 8', '1400H - 17FFH', [5], 'A0-A9, D0-D7, RD'), ('RAM', '2K x 8', '1800H - 1FFFH', [6, 7], 'A0-A10, D0-D7, RD, WR')]
fig,ax=plt.subplots(figsize=(7.4,4.4)); ax.axis("off"); ax.set_xlim(0,14.8); ax.set_ylim(0,9.0)
ax.text(0.1,8.7,TITLE,fontsize=8,weight="bold")
for k,(pin,lab) in enumerate(SEL):
    y=6.9-k*0.9; ax.text(0.2,y,lab,fontsize=7.5,va="center"); ax.plot([1.1,2.7],[y,y],color=INK,lw=1); ax.text(2.8,y,pin,fontsize=7,va="center")
box(ax,4.2,5.3,2.8,5.2,"74LS138\n3:8 decoder",fs=8,fc=YEL)
ax.text(4.2,8.25,ENAB,fontsize=6.0,ha="center",va="center")
def yp(k): return 7.4-0.62*k
for k in range(8):
    ax.plot([5.6,6.4],[yp(k),yp(k)],color=INK,lw=1); ax.text(5.5,yp(k),"Y%d"%k,fontsize=6,ha="right",va="center")
cy=[7.0,4.3,1.6][:len(CHIPS)] if len(CHIPS)<=3 else [7.0,4.8,2.6,0.6]
for (nm,sz,rg,ys,ln),y in zip(CHIPS,cy):
    box(ax,12.2,y,4.2,1.5,nm+" "+sz+"\n"+rg+"\n"+ln,fs=6.3,fc=GRN)
    if len(ys)==1:
        yy=yp(ys[0]); ax.plot([6.4,9.0,9.0,10.1],[yy,yy,y,y],color=ACCENT,lw=1.2)
    else:
        gx=8.3; ax.add_patch(mp.Rectangle((gx,y-0.35),0.9,0.7,fc="white",ec=INK,lw=1.1,zorder=3)); ax.text(gx+0.45,y,"AND",fontsize=6.5,ha="center",va="center",zorder=4)
        for j,k in enumerate(ys):
            yy=yp(k); ax.plot([6.4,7.7,7.7,gx],[yy,yy,y+0.18-0.36*j,y+0.18-0.36*j],color=ACCENT,lw=1.2)
        ax.plot([gx+0.9,10.1],[y,y],color=ACCENT,lw=1.2)
    ax.text(10.15,y+0.15,"CS",fontsize=6.5,color=ACCENT)
ax.text(7.4,0.15,"CS is active low; A0-A(n-1) of each chip are connected to the same address lines, D0-D7 to the data bus",fontsize=6.0,ha="center",color="#555")
```


The low address byte is demultiplexed with a 74LS373 latch (ALE). The EPROMs are read-only (output enable = $\overline{RD}$); the RAM uses $\overline{RD}$ and $\overline{WR}$. The data lines D0-D7 of all chips go to the data bus.

@s 9
The **8255A** is a **programmable peripheral interface (PPI)** (Intel, 40 pins): a general-purpose parallel I/O chip that connects a microprocessor to peripherals such as keyboards, displays, switches, LEDs and printers. It has **24 I/O lines** arranged as three 8-bit ports (A, B, C) whose function is selected by software (a control word).

```figure caption="Block diagram of the 8255A programmable peripheral interface: data bus buffer, read/write control, group A and group B control and the three 8-bit ports (port C is split into two 4-bit halves)."
import numpy as _np, matplotlib.patches as mp
def box(ax,x,y,w,h,t,fc="white",ec=INK,fs=8,lw=1.2,ls="-"):
    ax.add_patch(mp.FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",fc=fc,ec=ec,lw=lw,ls=ls,zorder=3))
    ax.text(x,y,t,ha="center",va="center",fontsize=fs,zorder=4)
def arr(ax,a,b,c=None,rad=0.0,lw=1.2,sa=0,sb=0,style="-|>"):
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle=style,color=c or ACCENT,lw=lw,shrinkA=sa,shrinkB=sb,connectionstyle="arc3,rad=%s"%rad),zorder=2)
BLUE="#eaf3ff"; YEL="#fff4d6"; GRN="#e6f4ea"; RED="#fde8e8"
fig,ax=plt.subplots(figsize=(7.4,4.6)); ax.axis("off"); ax.set_xlim(0,14.8); ax.set_ylim(0,9.4)
ax.add_patch(mp.Rectangle((3.0,0.5),8.2,8.4,fc="#fafcff",ec=INK,lw=1.4)); ax.text(7.1,8.55,"Intel 8255A PPI",ha="center",fontsize=9,weight="bold")
box(ax,4.9,7.2,3.0,1.0,"Data bus\nbuffer",fs=7.5,fc=BLUE); box(ax,4.9,5.4,3.0,1.2,"Read / Write\ncontrol logic",fs=7.5,fc=RED); box(ax,4.9,3.2,3.0,1.3,"Group A control\nGroup B control",fs=7.2,fc=YEL)
box(ax,9.2,7.4,2.6,0.8,"Group A\nPort A (8)",fs=7,fc=GRN); box(ax,9.2,6.0,2.6,0.8,"Group A\nPort C upper (PC7-4)",fs=6.3,fc=GRN)
box(ax,9.2,4.3,2.6,0.8,"Group B\nPort C lower (PC3-0)",fs=6.3,fc=GRN); box(ax,9.2,2.9,2.6,0.8,"Group B\nPort B (8)",fs=7,fc=GRN)
ax.text(0.2,7.2,"D7 - D0",fontsize=8,va="center"); arr(ax,(1.4,7.2),(3.3,7.2),c=INK,style="<|-|>")
for y,t in [(5.9,"RD"),(5.4,"WR"),(4.9,"A0, A1"),(4.4,"RESET"),(3.9,"CS")]:
    ax.text(0.2,y,t,fontsize=7.5,va="center"); arr(ax,(1.4,y),(3.3,y),c=INK)
for y,t in [(7.4,"PA7 - PA0"),(6.0,"PC7 - PC4"),(4.3,"PC3 - PC0"),(2.9,"PB7 - PB0")]:
    arr(ax,(10.5,y),(12.0,y),c=INK,style="<|-|>"); ax.text(12.1,y,t,fontsize=7.5,va="center")
ax.plot([6.4,7.9],[7.2,7.2],color="#777"); ax.plot([6.4,7.9],[3.2,3.2],color="#777"); ax.plot([7.9,7.9],[3.2,7.4],color="#777",lw=1.5)
ax.text(7.1,0.9,"Vcc  GND  (40-pin DIP, 24 programmable I/O lines)",fontsize=6.5,ha="center",color="#555")
```


**Blocks.**

- **Data bus buffer:** 8-bit bidirectional tri-state buffer D7-D0 that connects the 8255 to the system data bus (data and control word).
- **Read / write control logic:** with $\overline{RD}$, $\overline{WR}$, $\overline{CS}$, A1, A0 and RESET it selects a port or the control register. With A1 A0 = 00 / 01 / 10 / 11 the port A / port B / port C / control register is addressed.
- **Group A control** (port A and the upper half PC7-PC4) and **Group B control** (port B and the lower half PC3-PC0): these receive the control word and set the operating modes.
- **Ports:** port A (PA7-PA0) and port B (PB7-PB0) are 8-bit latched I/O ports; port C is split into the two nibbles PC7-PC4 and PC3-PC0 which may be used separately, as I/O or as handshake / control lines for ports A and B.

**Operating modes.**

1. **Mode 0, simple (basic) I/O.** Ports A, B, C-upper and C-lower can be independently input or output; the outputs are latched and the inputs are not latched. No handshaking: used for simple devices (switches, LEDs, 7-segment displays).
2. **Mode 1, strobed (handshake) I/O.** Ports A and B are I/O ports with handshake signals taken from port C (3 lines per port: STB, IBF, INTR for input; OBF, ACK, INTR for output); data are latched and interrupts can be generated. Used for printers and keyboards.
3. **Mode 2, bidirectional bus I/O.** Only **port A** (group A) works as a bidirectional 8-bit bus with five handshake lines from PC7-PC3 (INTR, STB, IBF, OBF, ACK); port B can then be in mode 0 or 1. Used to communicate with another computer / floppy controller.
4. **Bit set / reset (BSR) mode.** Any single bit of port C can be set or reset by a control word with D7 = 0; used to control individual lines or to enable / disable the interrupt flip-flops in mode 1 and 2.

**Control word (mode definition word), written to the control register (A1 A0 = 11).**

| Bit | D7 | D6 D5 | D4 | D3 | D2 | D1 | D0 |
|---|---|---|---|---|---|---|---|
| Meaning | 1 = mode set flag (0 = BSR) | group A mode: 00 = mode 0, 01 = mode 1, 1x = mode 2 | port A: 1 = input, 0 = output | port C upper: 1 = input, 0 = output | group B mode: 0 = mode 0, 1 = mode 1 | port B: 1 = input, 0 = output | port C lower: 1 = input, 0 = output |

*Example.* Port A as input, port B as output, port C (upper and lower) as output, all in mode 0: D7 D6 D5 D4 D3 D2 D1 D0 = 1 0 0 1 0 0 0 0 = **90H**. With the port addresses 80H-83H the program is `MVI A, 90H`, `OUT 83H` and then `IN 80H`, `OUT 81H` copy port A to port B. The **BSR word** has the form 0 x x x B2 B1 B0 S/R, e.g. `0000 0111` = 07H sets PC3 (B2B1B0 = 011, S = 1) and `0000 0110` = 06H resets it.

@s 10
**Interrupt.** An interrupt is a signal (hardware) or an instruction (software) that makes the processor suspend the program it is running, execute a special routine for the event and then return to the interrupted program. It replaces the slow *polling* of devices.

**Interrupt service routine (ISR).** The ISR is the subroutine that is executed in response to an interrupt (for example to read a key or serve a timer). It starts at a fixed address (the interrupt vector), should save the registers it uses (PUSH PSW, PUSH H ...), serve the device, restore the registers, enable the interrupts (EI) and finish with RET.

**Interrupts of the 8085.** Five hardware interrupts (plus eight software RST instructions):

| Interrupt | Pin | Trigger | Vector address | Priority | Maskable? |
|---|---|---|---|---|---|
| **TRAP** | 6 | rising edge **and** high level (must stay high until it is served) | 0024H | 1 (highest) | **No** (non-maskable); not affected by DI |
| **RST 7.5** | 7 | rising edge (latched internally, remembered until served or reset by SIM) | 003CH | 2 | yes (mask bit M7.5) |
| **RST 6.5** | 8 | high level | 0034H | 3 | yes (M6.5) |
| **RST 5.5** | 9 | high level | 002CH | 4 | yes (M5.5) |
| **INTR** | 10 | high level, sampled during the last T-state of each instruction | decided by the device: it puts an RST n opcode (vector $8n$) or CALL on the data bus in response to INTA | 5 (lowest) | yes (disabled by DI) |

TRAP, RST 7.5, RST 6.5 and RST 5.5 are **vectored** (the CPU itself jumps to a fixed address); INTR is **non-vectored** (the interrupting device supplies the address). The software interrupts RST 0 to RST 7 go to $8\times n$ (0000H, 0008H, 0010H, 0018H, 0020H, 0028H, 0030H, 0038H).

**How they are used (interrupt processing).**

1. The device raises the interrupt line; the interrupt flip-flop must be enabled with **EI** (all except TRAP are disabled after RESET or after an interrupt is accepted).
2. The CPU finishes the **current instruction**, then checks the interrupt lines in priority order.
3. The interrupt enable flip-flop is reset (further interrupts are disabled); for INTR the CPU sends the **INTA** pulse(s) and the device places RST n (or CALL address) on the data bus.
4. The CPU pushes the **PC** on the stack (so it can return) and loads the vector address into the PC.
5. The ISR runs; it ends with **EI** and **RET**, which pops the PC and returns to the interrupted instruction.

*Controlling them:* **EI** / **DI** enable / disable INTR and the RST interrupts; **SIM** (set interrupt mask) writes the mask bits M7.5, M6.5, M5.5, the mask-set enable MSE and resets the RST 7.5 latch (bits D2-D0 = masks, D3 = MSE, D4 = R7.5; D6, D7 for serial output); **RIM** (read interrupt mask) reads the masks (D2-D0), the interrupt-enable flag (D3), the pending interrupts (D6-D4) and the serial input bit SID (D7). Example: `MVI A, 0DH` (MSE = 1, M7.5 = 1, M6.5 = 0, M5.5 = 1), `SIM`, `EI` enables only RST 6.5.

@s 11
| Basis | RISC (reduced instruction set computer) | CISC (complex instruction set computer) |
|---|---|---|
| Instruction set | small and simple (about 30 - 100 instructions) | large and complex (hundreds of instructions) |
| Instruction length | fixed (e.g. 32 bit), easy to decode | variable length |
| Execution | most instructions in **one clock cycle** | multi-cycle; one instruction may take many cycles |
| Addressing modes | few (load / store only access memory) | many, memory operands in most instructions |
| Control unit | hard-wired (fast) | micro-programmed (slower, flexible) |
| Registers | large register file (32 or more) | few registers |
| Pipelining | easy and efficient | difficult |
| Code size / compiler | larger programs; the compiler does more work | compact programs; hardware does more work |
| Power / cost | low power, simpler chip | more transistors, higher power |
| Examples | ARM, MIPS, RISC-V, SPARC, PowerPC | Intel 8085 / 8086, x86, VAX, Motorola 68000 |
