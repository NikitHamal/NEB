---
file: NEBians-IOE-Past-Paper-Microprocessors-ENEX201-2081-Chaitra.pdf
subject: Microprocessor
level: BE · Year II / Part I
code: ENEX201
year_bs: 2081 Chaitra
cal: BS
year_ad: 2025
stream: BEI, BCT
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular (New Course). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
Define stored program concept. Explain briefly about Von Neumann Architecture. [[2+4]]

@q 2
Define addressing mode. Explain briefly about different types of addressing mode used in 8085 with suitable example. [[2+5]]

@q 3
Write a program in 8085 to transfer 8-bit number from one table to other by setting bit D5 if the number is less than 50 H else transfer the number by resetting bit D6. [[6]]

@q 4
Explain 8086 microprocessor with its internal architecture. Explain flags in 8086 Microprocessor. [[6+3]]

@q 5
Write an Assembly language programming in 8086 to display "Programming is Fun" in screen. [[6]]

@q 6
Explain in brief about 8255A PPI with its block diagram. [[6]]

@q 7
Design an address decoding circuit to interface one 2K × 8 ROM chip, one 2K × 8 RAM chip and one 4K × 8 EPROM chip with 8085 microprocessor consecutively starting from the memory location A000H. [[6]]

@q 8
What is an interrupt? Explain about the interrupt processing in 8085. [[2+4]]

@q 9
Differentiate between RISC and CISC architecture. [[4]]

@q 10
Compare and contrast between accumulator based and register based architecture. [[4]]
<!-- SOLUTIONS -->

@s 1
**Stored program concept.** The program (instructions in binary) and the data it works on are stored together in the **same read / write memory**, and the CPU fetches the instructions from memory one by one (the *program counter* gives the address of the next instruction) and executes them. A different program is loaded just by changing the memory contents; no rewiring is needed (unlike the early ENIAC). Instructions are treated like data, so a program can be loaded, modified and even generate other programs (compilers, loaders).

**Von Neumann architecture.** Proposed by John von Neumann (1945), it is built on the stored-program concept. Components:

- **CPU:** control unit (fetches, decodes, sequences), ALU (arithmetic and logic), registers (accumulator, PC, IR, MAR, MDR).
- **One main memory** for instructions **and** data, addressed by location number.
- **Input / output units.**
- A **single bus system** (address, data and control) that links them.

Operation: the *fetch-decode-execute* cycle: (1) the PC is copied to MAR; (2) the instruction is read to the IR; (3) the PC is incremented; (4) the control unit decodes the instruction; (5) the operands are fetched and the ALU / the transfer is carried out and the result written back.

```figure caption="Block diagrams of the Von Neumann architecture (one memory and one bus) and the Harvard architecture (separate program and data memories with separate buses)."
import numpy as _np, matplotlib.patches as mp
def box(ax,x,y,w,h,t,fc="white",ec=INK,fs=8,lw=1.2,ls="-"):
    ax.add_patch(mp.FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",fc=fc,ec=ec,lw=lw,ls=ls,zorder=3))
    ax.text(x,y,t,ha="center",va="center",fontsize=fs,zorder=4)
def arr(ax,a,b,c=None,rad=0.0,lw=1.2,sa=0,sb=0,style="-|>"):
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle=style,color=c or ACCENT,lw=lw,shrinkA=sa,shrinkB=sb,connectionstyle="arc3,rad=%s"%rad),zorder=2)
BLUE="#eaf3ff"; YEL="#fff4d6"; GRN="#e6f4ea"; RED="#fde8e8"
fig,(a,b)=plt.subplots(1,2,figsize=(7.4,3.2))
for z in (a,b): z.axis("off"); z.set_xlim(0,7); z.set_ylim(0,6)
a.set_title("Von Neumann architecture",fontsize=8.5)
box(a,3.5,4.9,3.0,0.9,"CPU\n(control unit + ALU)",fs=7.5,fc=YEL); box(a,3.5,1.3,3.4,1.1,"Single memory\ninstructions + data",fs=7.5,fc=BLUE)
arr(a,(3.0,4.4),(3.0,1.9),c=ACCENT,style="<|-|>"); arr(a,(4.0,4.4),(4.0,1.9),c=ACCENT,style="<|-|>"); a.text(3.5,3.15,"one shared\naddress + data bus",ha="center",fontsize=6.5,bbox=dict(fc="white",ec="none",pad=0.5))
box(a,3.5,0.15,0.01,0.01,"",ec="white")
b.set_title("Harvard architecture",fontsize=8.5)
box(b,3.5,4.9,3.0,0.9,"CPU\n(control unit + ALU)",fs=7.5,fc=YEL); box(b,1.4,1.3,2.5,1.1,"Program\nmemory\n(instructions)",fs=7.2,fc=BLUE); box(b,5.6,1.3,2.5,1.1,"Data\nmemory",fs=7.5,fc=GRN)
arr(b,(2.5,4.45),(1.4,1.9),c=ACCENT,style="<|-|>"); arr(b,(4.5,4.45),(5.6,1.9),c=ACCENT,style="<|-|>"); b.text(1.2,3.3,"program bus",fontsize=6.5,rotation=55,ha="center"); b.text(5.9,3.3,"data bus",fontsize=6.5,rotation=-55,ha="center")
```


*Advantages:* simple, cheap, flexible (the split between program and data memory is free). *Disadvantage:* the **von Neumann bottleneck**: instruction and data share one bus, so they cannot be fetched at the same time (the Harvard architecture with separate memories and buses, used in the 8051 and DSPs, removes this).

@s 2
**Addressing mode:** the way in which the operand (data) of an instruction is specified or its location is found. The 8085 has five modes.

| Mode | How the operand is given | Example | Meaning |
|---|---|---|---|
| **Immediate** | the data is a part of the instruction | `MVI B, 32H`; `LXI H, 2050H` | B $\leftarrow$ 32H; HL $\leftarrow$ 2050H |
| **Register** | operand is in a register | `MOV A, B`; `ADD C` | A $\leftarrow$ B; A $\leftarrow$ A + C |
| **Direct** | the 16-bit (or 8-bit port) address of the operand is in the instruction | `LDA 2050H`; `STA 3000H`; `IN 80H` | A $\leftarrow$ [2050H]; [3000H] $\leftarrow$ A; A $\leftarrow$ port 80H |
| **Register indirect** | a register pair holds the memory address | `MOV A, M`; `LDAX B`; `STAX D` | A $\leftarrow$ [HL]; A $\leftarrow$ [BC]; [DE] $\leftarrow$ A |
| **Implied (implicit)** | the operand is implied by the opcode itself (usually A) | `CMA`; `RAL`; `STC`; `RRC` | complement A; rotate A left with carry |

@s 3
**Algorithm.** The table length is not given, so ten numbers are assumed (source table at 2000H, destination table at 3000H). For each number: compare it with 50H using `CPI 50H` (CY = 1 when the number is less than 50H). If it is **less than 50H**, **set bit D5** (`ORI 20H`); otherwise **reset bit D6** (`ANI BFH`, mask 1011 1111) and store the result in the other table.

```asm
        LXI  H, 2000H     ; HL = source table
        LXI  D, 3000H     ; DE = destination table
        MVI  C, 0AH       ; 10 numbers (assumed)
NEXT:   MOV  A, M         ; A = number
        CPI  50H          ; compare with 50H
        JC   SETD5        ; number < 50H  (CY = 1)
        ANI  BFH          ; number >= 50H: reset D6
        JMP  STORE
SETD5:  ORI  20H          ; number < 50H: set D5
STORE:  STAX D            ; store in the second table
        INX  H
        INX  D
        DCR  C
        JNZ  NEXT
        HLT
```

*Check (program run on an 8085 simulator).* Source 10H, 4FH, 50H, FFH, 7AH, 00H, 80H, C3H, 51H, 20H gives 30H, 6FH, 10H, BFH, 3AH, 20H, 80H, 83H, 11H, 20H: numbers below 50H (10H, 4FH, 00H, 20H) have D5 set (30H, 6FH, 20H, 20H) and the numbers $\ge$ 50H have D6 reset (50H to 10H, FFH to BFH, 7AH to 3AH, 80H unchanged because D6 is already 0, C3H to 83H, 51H to 11H).

@s 4
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

**Flags in the 8086.**

The 8086 flag register is 16 bits wide, of which nine bits are used: six **status (conditional) flags** that are set by the ALU after an operation and three **control flags** that are set or cleared by the programmer.

```figure caption="The 8086 flag register: six status flags set by the ALU and three control flags set by the programmer; seven bits are unused."
import numpy as _np, matplotlib.patches as mp
def box(ax,x,y,w,h,t,fc="white",ec=INK,fs=8,lw=1.2,ls="-"):
    ax.add_patch(mp.FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",fc=fc,ec=ec,lw=lw,ls=ls,zorder=3))
    ax.text(x,y,t,ha="center",va="center",fontsize=fs,zorder=4)
def arr(ax,a,b,c=None,rad=0.0,lw=1.2,sa=0,sb=0,style="-|>"):
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle=style,color=c or ACCENT,lw=lw,shrinkA=sa,shrinkB=sb,connectionstyle="arc3,rad=%s"%rad),zorder=2)
BLUE="#eaf3ff"; YEL="#fff4d6"; GRN="#e6f4ea"; RED="#fde8e8"
fig,ax=plt.subplots(figsize=(7.4,2.6)); ax.axis("off"); ax.set_xlim(-0.3,16.6); ax.set_ylim(-1.2,3.4)
names={11:"OF",10:"DF",9:"IF",8:"TF",7:"SF",6:"ZF",4:"AF",2:"PF",0:"CF"}
for b in range(16):
    x=15-b; k=b
    fc=YEL if k in (11,7,6,4,2,0) else (BLUE if k in (10,9,8) else "#eeeeee")
    ax.add_patch(mp.Rectangle((x,1.0),1,0.9,fc=fc,ec=INK,lw=1.2)); ax.text(x+0.5,1.45,names.get(k,"-"),ha="center",va="center",fontsize=8,weight="bold" if k in names else "normal")
    ax.text(x+0.5,2.15,str(k),ha="center",fontsize=6.8)
ax.text(8.0,-0.8,"yellow = status flags (CF PF AF ZF SF OF), blue = control flags (TF IF DF), grey = undefined",ha="center",fontsize=6.8)
ax.text(8.0,2.85,"8086 flag register (16 bits)",ha="center",fontsize=8.2,weight="bold")
```


| Flag | Type | Meaning |
|---|---|---|
| **CF** carry | status | carry out of the MSB in addition or borrow in subtraction |
| **PF** parity | status | 1 if the low byte of the result has an even number of 1s |
| **AF** auxiliary carry | status | carry from bit 3 to bit 4 (BCD operations) |
| **ZF** zero | status | 1 if the result is zero |
| **SF** sign | status | copy of the MSB of the result (1 means negative) |
| **OF** overflow | status | 1 if a signed result is out of range (e.g. 7FH + 01H in 8 bit) |
| **TF** trap | control | 1 puts the CPU in single-step mode (an interrupt after every instruction) |
| **IF** interrupt | control | 1 enables the maskable (INTR) interrupt (STI sets, CLI clears it) |
| **DF** direction | control | 0 auto-increments SI / DI in string instructions, 1 auto-decrements (CLD / STD) |

@s 5
**Method.** The message is stored in the data segment as a string terminated by `$`. DOS function 09H (INT 21H) displays a `$`-terminated string pointed to by DS:DX. The data segment register must first be loaded with the address of the data segment, and the program ends with function 4CH.

```asm
        .MODEL SMALL
        .STACK 100H
        .DATA
MSG     DB  'Programming is Fun$'    ; '$' marks the end of the string
        .CODE
MAIN    PROC
        MOV  AX, @DATA        ; initialise the data segment
        MOV  DS, AX
        LEA  DX, MSG          ; DS:DX -> message
        MOV  AH, 09H          ; DOS function: display string
        INT  21H
        MOV  AH, 4CH          ; DOS function: terminate program
        INT  21H
MAIN    ENDP
        END  MAIN
```

*Alternative (character by character with function 02H).*

```asm
        LEA  SI, MSG
AGAIN:  MOV  DL, [SI]
        CMP  DL, '$'
        JE   EXIT
        MOV  AH, 02H          ; display the character in DL
        INT  21H
        INC  SI
        JMP  AGAIN
EXIT:   MOV  AH, 4CH
        INT  21H
```

Output on the screen: `Programming is Fun`.

@s 6
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

@s 7
**Step 1: sizes.** 2K x 8 ROM: $2^{11}$ bytes, 11 lines A0-A10. 2K x 8 RAM: 11 lines A0-A10. 4K x 8 EPROM: $2^{12}$ bytes, 12 lines A0-A11. The chips are placed one after the other from A000H: ROM first (2 KB), RAM next (2 KB), the EPROM last (4 KB).

**Step 2: address map.**

| Chip | Start | End | A15 A14 | A13 | A12 | A11 | Lines to chip |
|---|---|---|---|---|---|---|---|
| ROM 2 KB | A000H | A7FFH | 1 0 | 1 | 0 | 0 | A0-A10 |
| RAM 2 KB | A800H | AFFFH | 1 0 | 1 | 0 | 1 | A0-A10 |
| EPROM 4 KB | B000H | BFFFH | 1 0 | 1 | 1 | x | A0-A11 |

(A000H = 1010 0000 0000 0000, A7FFH = 1010 0111 1111 1111, A800H = 1010 1000 0000 0000, AFFFH = 1010 1111 1111 1111, B000H = 1011 0000 0000 0000, BFFFH = 1011 1111 1111 1111.)

**Step 3: decoder.** A 74LS138 is used with $C=A_{13}$, $B=A_{12}$, $A=A_{11}$. The enables must make the decoder active only for A15 = 1, A14 = 0 and a memory access: G1 = A15 (active high), G2A = A14 (active low), G2B = IO/M (active low).

- $CBA=100$ ($\overline{Y_4}$): A000H-A7FFH, to the chip select of the **ROM**;
- $CBA=101$ ($\overline{Y_5}$): A800H-AFFFH, to the **RAM**;
- $CBA=110$ and $111$ ($\overline{Y_6}$, $\overline{Y_7}$): B000H-B7FFH and B800H-BFFFH together form the 4 KB **EPROM**, so $\overline{CS}_{EPROM}=\overline{Y_6}\cdot\overline{Y_7}$ (AND gate).

```figure caption="Address decoding with a 74LS138: Y4 selects the 2 KB ROM (A000H-A7FFH), Y5 the 2 KB RAM (A800H-AFFFH) and the AND of Y6 and Y7 the 4 KB EPROM (B000H-BFFFH)."
import numpy as _np, matplotlib.patches as mp
def box(ax,x,y,w,h,t,fc="white",ec=INK,fs=8,lw=1.2,ls="-"):
    ax.add_patch(mp.FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",fc=fc,ec=ec,lw=lw,ls=ls,zorder=3))
    ax.text(x,y,t,ha="center",va="center",fontsize=fs,zorder=4)
def arr(ax,a,b,c=None,rad=0.0,lw=1.2,sa=0,sb=0,style="-|>"):
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle=style,color=c or ACCENT,lw=lw,shrinkA=sa,shrinkB=sb,connectionstyle="arc3,rad=%s"%rad),zorder=2)
BLUE="#eaf3ff"; YEL="#fff4d6"; GRN="#e6f4ea"; RED="#fde8e8"
TITLE='Address decoding: 2K ROM, 2K RAM, 4K EPROM consecutively from A000H'; SEL=[('C', 'A13'), ('B', 'A12'), ('A', 'A11')]; ENAB='G1 = A15   G2A = A14   G2B = IO/M'; CHIPS=[('ROM', '2K x 8', 'A000H - A7FFH', [4], 'A0-A10, D0-D7, RD'), ('RAM', '2K x 8', 'A800H - AFFFH', [5], 'A0-A10, D0-D7, RD, WR'), ('EPROM', '4K x 8', 'B000H - BFFFH', [6, 7], 'A0-A11, D0-D7, RD')]
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


The latch 74LS373 (ALE) separates the low address byte. ROM and EPROM need only $\overline{RD}$ (output enable); the RAM needs $\overline{RD}$ and $\overline{WR}$. D0-D7 of all chips join the data bus.

@s 8
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

@s 9
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

@s 10
| Basis | Accumulator-based architecture | Register-based (general-register) architecture |
|---|---|---|
| Operands | one operand is always in the **accumulator** and the result is returned there; the other is a register or memory (e.g. 8085: `ADD B` means A $\leftarrow$ A + B) | any register may be the source and destination (e.g. 8086: `ADD BX, CX`; ARM: `ADD R1, R2, R3`) |
| Number of registers | few (one accumulator, a few helpers) | many general-purpose registers |
| Instruction | short, one-address (the accumulator is implied), so small code | longer (two or three register fields) |
| Data movement | much movement to and from the accumulator (a bottleneck) | fewer transfers, intermediate results stay in registers |
| Speed | slower for complex expressions (memory traffic) | faster; supports pipelining and compilers can optimise registers |
| Hardware | simple, cheap | more complex (register file, more buses, decoding) |
| Examples | 8080 / 8085, 6502, early computers (EDSAC) | 8086 / x86, MIPS, ARM, RISC-V |
