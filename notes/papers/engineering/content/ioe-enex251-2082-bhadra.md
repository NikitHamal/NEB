---
file: NEBians-IOE-Past-Paper-Microprocessors-and-Microcontrollers-ENEX251-2082-Bhadra.pdf
subject: Microprocessors and Microcontrollers
level: BE · Year II / Part II
code: ENEX 251
year_bs: 2082 Bhadra
cal: BS
year_ad: 2025
stream: BEL
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular (New Course). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
Draw a block diagram of Harvard architecture. What are the major differences between Harvard architecture and Von Neumann's architecture? [[2+2]]

@q 2
a) Define instruction and instruction cycle. Explain different types of instruction used in 8085 microprocessors based on byte size. [[2+4]]

b) Write an assembly language program of the 8085 microprocessor to transfer ten 8-bit data stored in memory address starting at 8050H to memory table starting from 9050H if the data is less than 70H, else store 00H. [[6]]

@q 3
a) What do you mean by instruction pipelining? Explain segment registers and general-purpose registers of the 8086 microprocessor. [[1+5]]

b) Write an assembly language program of the 8086 microprocessor to input a string from keyboard, convert all characters into upper case and display each word in separate lines on a blank screen. [[6]]

@q 4
a) Design an address decoding circuit to interface one 4 KB RAM chip and one 2 KB ROM chip with the 8085 microprocessor consecutively starting from the memory location A000H. [[6]]

b) Show machine cycles involved during the execution of the instruction OUT 80H. Calculate the time required to execute such instruction, if the microprocessor is operating at 2 MHz clock frequency. [[5+1]]

@q 5
a) Draw the internal architecture of the 8051 microcontroller and explain briefly about its internal RAM organization. [[2+4]]

b) In 8051, what do you mean by special function registers? Write an assembly language program on 8051 to read an 8-bit temperature in Celsius from port 1 and to output the Fahrenheit temperature equivalent onto port 2. [[2+4]]

@q 6
Write short notes on: (Any Two) [[2×4]]

a) Interrupt processing in 8085

b) Assembling, linking and execution of 8086 microprocessor

c) Addressing modes of 8051 microcontroller

<!-- SOLUTIONS -->

@s 1
**Harvard architecture** keeps the program (instructions) and the data in two **separate memories**, each with its own address and data bus, so the CPU can fetch the next instruction while it reads or writes data in the same clock cycle.

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


| Basis | Harvard architecture | Von Neumann architecture |
|---|---|---|
| Memories | separate program memory and data memory | one memory for instructions and data |
| Buses | separate address and data buses for each memory | one shared address bus and data bus |
| Speed | instruction fetch and data access are **simultaneous**: faster, pipelining is easy | fetch and data access are sequential: the shared bus is the *von Neumann bottleneck* |
| Word width | program and data word sizes can differ (e.g. 14-bit program, 8-bit data in PIC) | the same width for both |
| Hardware | more complex and costlier (more pins and buses) | simple and cheaper |
| Program as data | a program cannot overwrite itself; the program memory is mostly ROM | programs can be modified like data (self-modifying code, loaders) |
| Examples | 8051, PIC, AVR, DSP chips | 8085, 8086, general-purpose PCs |

@s 2
**(a) Instruction and instruction cycle.** An **instruction** is a binary-coded command (an *opcode*, with an operand when needed) that tells the microprocessor to perform one basic operation such as data transfer, arithmetic, logic, branching or machine control. A **program** is a sequence of instructions.

The **instruction cycle** is the time needed to fetch an instruction from memory, decode it and execute it. It is made of one or more **machine cycles** (opcode fetch, memory read or write, I/O read or write), and each machine cycle consists of 3 to 6 **T-states** (clock periods): instruction cycle ⊃ machine cycles ⊃ T-states. The first machine cycle is always the opcode fetch.

**Types of 8085 instructions by byte size.**

| Type | Format | Examples | Machine cycles / T-states |
|---|---|---|---|
| 1-byte | opcode only (the operands are registers, or implied) | `MOV A,B`, `ADD C`, `INX H`, `CMA`, `HLT` | `MOV A,B`: 1 / 4 T; `MOV A,M`: 2 / 7 T |
| 2-byte | opcode + 8-bit data or 8-bit port address | `MVI A,32H`, `ADI 05H`, `IN 80H`, `OUT 80H` | `MVI A,32H`: 2 / 7 T; `IN 80H`: 3 / 10 T |
| 3-byte | opcode + 16-bit address or 16-bit data (low byte first) | `LDA 2050H`, `STA 3000H`, `LXI H,2050H`, `JMP 2000H`, `CALL 3000H` | `LDA`: 4 / 13 T; `LXI`: 3 / 10 T; `JMP`: 3 / 10 T |

Example: `LDA 2050H` is stored as three consecutive bytes `3A 50 20` (opcode 3AH, then the low byte 50H, then the high byte 20H).

**(b) Program.** HL points to the source, DE to the destination, C counts ten data. `CPI 70H` computes A − 70H: the carry flag is set exactly when A < 70H.

```asm
        LXI  H,8050H    ; HL = source pointer
        LXI  D,9050H    ; DE = destination pointer
        MVI  C,0AH      ; C = counter = 10
LOOP:   MOV  A,M        ; A = data byte
        CPI  70H        ; compare with 70H: CY = 1 if A < 70H
        JC   STORE      ; data < 70H: keep the data
        MVI  A,00H      ; data >= 70H: replace by 00H
STORE:  STAX D          ; [DE] = A
        INX  H          ; next source
        INX  D          ; next destination
        DCR  C
        JNZ  LOOP       ; repeat for 10 data
        HLT
```

*Check.* Data 05H, 6FH, 70H, 9AH, FFH, 00H give 05H, 6FH, 00H, 00H, 00H, 00H (70H is not less than 70H, so it is replaced). The program was run on an instruction-level simulator on random data to confirm this.

@s 3
**(a) Instruction pipelining.** Pipelining overlaps the stages of consecutive instructions, so that the next instruction is fetched while the present one is executed. This increases throughput. The 8086 has a two-stage pipeline: the BIU prefetches instruction bytes into a 6-byte queue while the EU executes the earlier ones.

```figure caption="Instruction pipelining: overlapping the fetch of instruction n+1 with the execution of instruction n (the 8086 does this with its BIU and EU)."
import numpy as _np, matplotlib.patches as mp
def box(ax,x,y,w,h,t,fc="white",ec=INK,fs=8,lw=1.2,ls="-"):
    ax.add_patch(mp.FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",fc=fc,ec=ec,lw=lw,ls=ls,zorder=3))
    ax.text(x,y,t,ha="center",va="center",fontsize=fs,zorder=4)
def arr(ax,a,b,c=None,rad=0.0,lw=1.2,sa=0,sb=0,style="-|>"):
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle=style,color=c or ACCENT,lw=lw,shrinkA=sa,shrinkB=sb,connectionstyle="arc3,rad=%s"%rad),zorder=2)
BLUE="#eaf3ff"; YEL="#fff4d6"; GRN="#e6f4ea"; RED="#fde8e8"
fig,(a,b)=plt.subplots(2,1,figsize=(7.4,3.6),sharex=True)
cols=[BLUE,YEL,GRN]
a.set_title("Without pipelining (fetch, then execute)",fontsize=8,loc="left")
for i in range(3):
    a.add_patch(mp.Rectangle((i*4,2-i),2,0.8,fc=BLUE,ec=INK)); a.text(i*4+1,2-i+0.4,"F%d"%(i+1),ha="center",va="center",fontsize=7)
    a.add_patch(mp.Rectangle((i*4+2,2-i),2,0.8,fc=YEL,ec=INK)); a.text(i*4+3,2-i+0.4,"E%d"%(i+1),ha="center",va="center",fontsize=7)
a.set_ylim(-0.3,3.2); a.set_yticks([]); a.text(12.2,0.4,"12 time units",fontsize=7,va="center")
b.set_title("With pipelining (fetch of the next instruction overlaps execution)",fontsize=8,loc="left")
for i in range(3):
    b.add_patch(mp.Rectangle((i*2,2-i),2,0.8,fc=BLUE,ec=INK)); b.text(i*2+1,2-i+0.4,"F%d"%(i+1),ha="center",va="center",fontsize=7)
    b.add_patch(mp.Rectangle((i*2+2,2-i),2,0.8,fc=YEL,ec=INK)); b.text(i*2+3,2-i+0.4,"E%d"%(i+1),ha="center",va="center",fontsize=7)
b.set_ylim(-0.3,3.2); b.set_yticks([]); b.set_xlim(0,14); b.text(8.2,0.4,"8 time units",fontsize=7,va="center"); b.set_xlabel("time (each box = 2 units)",fontsize=7)
for z in (a,b):
    for s in ("top","right","left"): z.spines[s].set_visible(False)
    z.tick_params(labelsize=6.5)
fig.tight_layout()
```


For 3 instructions with 2-unit fetch and execute, the sequential time is 12 units but the pipelined time is only 8 units. A jump flushes the queue (the pipeline is refilled), which is the limit of the gain.

**Segment registers (16 bit).** The 1 MB memory is divided into 64 KB segments; four registers hold the segment base addresses:

| Register | Segment | Used with |
|---|---|---|
| CS | code segment | IP (instruction fetch) |
| DS | data segment | BX, SI, DI, direct address (data) |
| SS | stack segment | SP, BP (stack) |
| ES | extra segment | DI (destination of string instructions) |

The physical address is $\text{segment} \times 10H + \text{offset}$. Example: CS = 2000H and IP = 0100H give $20000H + 0100H = 20100H$.

**General-purpose registers (16 bit, in the EU).**

| Register | Name | Special use |
|---|---|---|
| AX (AH, AL) | accumulator | arithmetic, I/O (IN/OUT), multiply and divide |
| BX (BH, BL) | base | holds an offset (base address) for memory addressing, XLAT |
| CX (CH, CL) | count | loop count (LOOP), shift/rotate count, string repeat |
| DX (DH, DL) | data | port address for IN/OUT, upper half of the multiply/divide result |

Pointer and index registers SP (stack pointer), BP (base pointer), SI (source index) and DI (destination index) are also usable as 16-bit data registers.

**(b) 8086 program.** DOS function 0AH reads the string; a loop converts the lower case letters 'a' to 'z' to capital letters by subtracting 20H (clearing bit 5); BIOS function 06H of INT 10H clears the screen and function 02H homes the cursor; then each word is displayed on its own line.

```asm
.MODEL SMALL
.STACK 100H
.DATA
  MSG1  DB 'Enter a string: $'
  NL    DB 0DH,0AH,'$'
  BUF   DB 80,?,80 DUP(0)     ; max length, actual length, characters
.CODE
MAIN PROC
        MOV  AX,@DATA
        MOV  DS,AX
        LEA  DX,MSG1
        MOV  AH,09H
        INT  21H            ; prompt
        LEA  DX,BUF
        MOV  AH,0AH
        INT  21H            ; read the string into BUF
        LEA  SI,BUF+2
        MOV  CL,BUF+1
        MOV  CH,0           ; CX = number of characters
        JCXZ CLRSCR         ; empty string: nothing to convert
UP:     MOV  AL,[SI]
        CMP  AL,'a'
        JB   NXT            ; below 'a': leave unchanged
        CMP  AL,'z'
        JA   NXT            ; above 'z': leave unchanged
        SUB  AL,20H         ; lower case -> upper case
        MOV  [SI],AL
NXT:    INC  SI
        LOOP UP             ; repeat for all characters
CLRSCR: MOV  AX,0600H       ; scroll the whole window up: blank screen
        MOV  BH,07H         ; normal attribute
        MOV  CX,0000H       ; top left corner (row 0, column 0)
        MOV  DX,184FH       ; bottom right corner (row 24, column 79)
        INT  10H
        MOV  AH,02H
        MOV  BH,00H         ; page 0
        MOV  DX,0000H       ; cursor to row 0, column 0
        INT  10H
        LEA  SI,BUF+2
        MOV  CL,BUF+1
        MOV  CH,0
        MOV  BL,0           ; BL = 1 while inside a word
NEXT:   JCXZ FIN            ; all characters displayed
        MOV  DL,[SI]
        INC  SI
        DEC  CX
        CMP  DL,' '
        JE   SPACE
        MOV  BL,1           ; inside a word
        MOV  AH,02H
        INT  21H            ; display the character
        JMP  NEXT
SPACE:  CMP  BL,0
        JE   NEXT           ; repeated spaces: ignore
        MOV  BL,0           ; the word has ended
        LEA  DX,NL
        MOV  AH,09H
        INT  21H            ; carriage return + line feed
        JMP  NEXT
FIN:    MOV  AH,4CH
        INT  21H            ; return to DOS
MAIN ENDP
END MAIN
```

*Sample run.* Input `learn free, grow far` gives a blank screen with

```text
LEARN
FREE,
GROW
FAR
```

(characters other than a to z, such as the comma, are kept unchanged).

@s 4
**(a) Address decoding design.**

*Step 1, sizes and ranges.* RAM 4 KB = $2^{12}$ bytes → 12 address lines A0 to A11; ROM 2 KB = $2^{11}$ bytes → 11 lines A0 to A10. The RAM starts at A000H and the ROM follows consecutively.

| Chip | Start | End | A15 A14 A13 A12 | A11 | Lines to the chip |
|---|---|---|---|---|---|
| RAM 4 KB | A000H | AFFFH | 1 0 1 0 | x | A0 to A11 |
| ROM 2 KB | B000H | B7FFH | 1 0 1 1 | 0 | A0 to A10 |

*Step 2, decoder.* A 74LS138 is used with select inputs C = A14, B = A13, A = A12 and enables G1 = A15 (must be 1), G2A = IO/M (must be 0, a memory cycle), G2B = ground.

- $A_{14}A_{13}A_{12} = 010$ → output $Y_2$ low for A000H to AFFFH → chip select of the **RAM**.
- $A_{14}A_{13}A_{12} = 011$ → output $Y_3$ low for B000H to BFFFH (4 KB), larger than the 2 KB ROM, so $\overline{CS}_{ROM} = Y_3 + A_{11}$ (low only when $Y_3 = 0$ and $A_{11} = 0$) selects B000H to B7FFH.

```figure caption="Address decoding for 4 KB RAM at A000H and 2 KB ROM at B000H with a 74LS138 (Y2 selects the RAM; Y3 OR A11 selects the ROM)."
import numpy as _np, matplotlib.patches as mp
def box(ax,x,y,w,h,t,fc="white",ec=INK,fs=8,lw=1.2,ls="-"):
    ax.add_patch(mp.FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",fc=fc,ec=ec,lw=lw,ls=ls,zorder=3))
    ax.text(x,y,t,ha="center",va="center",fontsize=fs,zorder=4)
def arr(ax,a,b,c=None,rad=0.0,lw=1.2,sa=0,sb=0,style="-|>"):
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle=style,color=c or ACCENT,lw=lw,shrinkA=sa,shrinkB=sb,connectionstyle="arc3,rad=%s"%rad),zorder=2)
BLUE="#eaf3ff"; YEL="#fff4d6"; GRN="#e6f4ea"; RED="#fde8e8"
fig,ax=plt.subplots(figsize=(7.4,4.4)); ax.axis("off"); ax.set_xlim(0,14.8); ax.set_ylim(0,8.9)
C1=('RAM', '4', 'A000H - AFFFH', 2, 'A0-A11, D0-D7, RD, WR', 0); C2=('ROM', '2', 'B000H - B7FFH', 3, 'A0-A10, D0-D7, RD', 1); G1='A15'; G2A='IO/M'; G2B='GND'
# address bus labels
ax.text(0.1,8.5,"8085 address bus",fontsize=8,weight="bold")
for n,y in [("A15",7.6),("A14",6.7),("A13",5.8),("A12",4.9)]:
    ax.text(0.2,y,n,fontsize=7.5,va="center"); ax.plot([1.0,2.5],[y,y],color=INK,lw=1)
box(ax,3.9,5.35,2.8,5.1,"74LS138\n3:8 decoder",fs=8,fc=YEL)
for lab,y in [("A",4.9),("B",5.8),("C",6.7)]: ax.text(2.6,y,lab,fontsize=7,va="center")
ax.text(3.9,8.15,"G1=%s   G2A=%s   G2B=%s"%(G1,G2A,G2B),fontsize=6.8,ha="center")
for k in range(8):
    y=7.55-0.62*k; ax.plot([5.3,6.0],[y,y],color=INK,lw=1); ax.text(5.05,y,"Y%d"%k,fontsize=6.2,ha="right",va="center")
def ypos(k): return 7.55-0.62*k
y1=ypos(C1[3]); box(ax,11.9,6.6,3.6,1.9,"%s\n%s KB\n%s"%(C1[0],C1[1],C1[2]),fs=7.5,fc=BLUE)
ax.plot([6.0,8.0,8.0,10.1],[y1,y1,6.1,6.1],color=ACCENT,lw=1.3); ax.text(10.15,6.1,"CS",fontsize=6.5,va="center",ha="left",color="#b00020",bbox=dict(fc="white",ec="none",pad=0.3))
ax.text(11.9,5.3,C1[4],fontsize=6.5,ha="center")
y2=ypos(C2[3]); box(ax,11.9,2.6,3.6,1.9,"%s\n%s KB\n%s"%(C2[0],C2[1],C2[2]),fs=7.5,fc=GRN)
ax.add_patch(mp.Polygon([(7.2,3.4),(7.2,2.0),(8.4,2.7)],fc="white",ec=INK,lw=1.2,zorder=3)); ax.text(7.55,2.7,"OR",fontsize=6.5,ha="center",va="center",zorder=4)
ax.plot([6.0,6.3,6.3,7.2],[y2,y2,3.1,3.1],color=ACCENT,lw=1.3)
ax.text(0.2,1.8,"A11",fontsize=7.5,va="center"); ax.plot([1.0,6.7,6.7,7.2],[1.8,1.8,2.3,2.3],color=INK,lw=1.2)
ax.text(5.2,1.95,"A11",fontsize=6.5)
ax.plot([8.4,9.0,9.0,10.1],[2.7,2.7,2.6,2.6],color=ACCENT,lw=1.3); ax.text(10.15,2.6,"CS",fontsize=6.5,va="center",color="#b00020",bbox=dict(fc="white",ec="none",pad=0.3))
ax.text(11.9,1.3,C2[4],fontsize=6.5,ha="center")
ax.text(7.4,0.35,"Low address lines (A0-A11 / A0-A10) go straight to the chips; the data bus D0-D7 connects every chip",fontsize=6.3,ha="center")
```


AD0 to AD7 are latched with a 74LS373 (ALE) to get A0 to A7. $\overline{RD}$ goes to the output enable of RAM and ROM and $\overline{WR}$ to the write enable of the RAM.

**(b) Machine cycles of `OUT 80H`.** `OUT 80H` (opcode D3H, 2 bytes) writes the accumulator to output port 80H: 3 machine cycles, 10 T-states.

| Machine cycle | T-states | IO/M | S1 S0 | What happens |
|---|---|---|---|---|
| 1. Opcode fetch (M1) | 4 | 0 | 1 1 | PC on the address bus, ALE = 1 in T1; RD low in T2, T3 reads the opcode D3H; T4 decodes |
| 2. Memory read (M2) | 3 | 0 | 1 0 | address PC + 1; the port address 80H is read into a temporary register |
| 3. I/O write (M3) | 3 | 1 | 0 1 | 80H on A15 to A8 and AD7 to AD0, then the accumulator content on AD7 to AD0; WR low in T2 and T3 writes it to the port |

```figure caption="Machine cycles and timing of OUT 80H: opcode fetch (4 T), memory read of the port address (3 T) and I/O write (3 T)."
import numpy as _np, matplotlib.patches as mp
def box(ax,x,y,w,h,t,fc="white",ec=INK,fs=8,lw=1.2,ls="-"):
    ax.add_patch(mp.FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",fc=fc,ec=ec,lw=lw,ls=ls,zorder=3))
    ax.text(x,y,t,ha="center",va="center",fontsize=fs,zorder=4)
def arr(ax,a,b,c=None,rad=0.0,lw=1.2,sa=0,sb=0,style="-|>"):
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle=style,color=c or ACCENT,lw=lw,shrinkA=sa,shrinkB=sb,connectionstyle="arc3,rad=%s"%rad),zorder=2)
BLUE="#eaf3ff"; YEL="#fff4d6"; GRN="#e6f4ea"; RED="#fde8e8"
fig,ax=plt.subplots(figsize=(7.4,4.4)); ax.set_xlim(0,10.9); ax.set_ylim(-0.4,8.6); ax.axis("off")
INSTR='OUT'; OPC='D3H'; THIRD='IO write'
ctrl="RD" if INSTR=="IN" else "WR"
# bands
for i,(n,l,c) in enumerate([("Opcode fetch (M1)",4,YEL),("Memory read (M2)",3,BLUE),(THIRD+" (M3)",3,GRN)]):
    x0=[0,4,7][i]; ax.add_patch(mp.Rectangle((x0+0.9,7.6),l,0.6,fc=c,ec=INK,lw=1,zorder=2)); ax.text(x0+0.9+l/2,7.9,n,ha="center",va="center",fontsize=7)
for t in range(10):
    ax.text(0.9+t+0.5,7.3,"T%d"%(t%4+1 if t<4 else (t-4+1 if t<7 else t-7+1)),fontsize=6.3,ha="center")
    ax.plot([0.9+t,0.9+t],[0.3,7.2],color="#cccccc",lw=0.6,zorder=0)
ax.plot([10.9,10.9],[0.3,7.2],color="#cccccc",lw=0.6,zorder=0)
rows={"CLK":6.4,"ALE":5.4,"IO/M":4.4,ctrl:3.4,"A15-A8":2.3,"AD7-AD0":1.0}
for n,y in rows.items(): ax.text(0.8,y+0.1,n if n not in("RD","WR") else n,fontsize=7.3,ha="right",va="center")
# clock
for t in range(10):
    ax.plot([0.9+t,0.9+t,0.9+t+0.5,0.9+t+0.5,0.9+t+1],[6.1,6.7,6.7,6.1,6.1],color=INK,lw=1)
# ALE high in T1 of each cycle
def pulse(y,spans,hi_low=True,base=0.0):
    pass
for s in (0,4,7):
    ax.plot([0.9+s,0.9+s,0.9+s+0.5,0.9+s+0.5],[5.1,5.7,5.7,5.1],color=INK,lw=1.3)
ax.plot([0.9,0.9],[5.1,5.1],color=INK); ax.plot([0.9+0.5,0.9+4],[5.1,5.1],color=INK,lw=1.3); ax.plot([0.9+4.5,0.9+7],[5.1,5.1],color=INK,lw=1.3); ax.plot([0.9+7.5,10.9],[5.1,5.1],color=INK,lw=1.3)
# IO/M: low for M1,M2 (0..7), high for M3
ax.plot([0.9,7.9],[4.1,4.1],color=INK,lw=1.3); ax.plot([7.9,7.9],[4.1,4.7],color=INK,lw=1.3); ax.plot([7.9,10.9],[4.7,4.7],color=INK,lw=1.3)
ax.text(5.4,4.2,"low (memory)",fontsize=6.3,ha="center",va="bottom",color="#555"); ax.text(9.4,4.8,"high (I/O)",fontsize=6.3,ha="center",va="bottom",color="#555")
# RD / WR active low in T2-T3 of each cycle (OF, MR); only M3 for OUT uses WR instead of RD
hi,lo=3.7,3.1
segs=[(1,3),(5,7),(8,10)]
if INSTR=="OUT": segs_rd=[(1,3),(5,7)]; segs_wr=[(8,10)]
else: segs_rd=segs; segs_wr=[]
ax.plot([0.9,10.9],[hi,hi],color="#bbbbbb",lw=0.5)
x=0.9; pts=[]
def lowpulses(spans,y0=hi,y1=lo):
    x=0.9; X=[x]; Y=[y0]
    for a,b in spans:
        X+= [0.9+a,0.9+a,0.9+b,0.9+b]; Y+=[y0,y1,y1,y0]
    X.append(10.9); Y.append(y0); return X,Y
if INSTR=="IN":
    X,Y=lowpulses(segs); ax.plot(X,Y,color=INK,lw=1.3)
else:
    X,Y=lowpulses(segs_wr); ax.plot(X,Y,color=INK,lw=1.3)
    ax.text(10.8,3.15,"WR low",fontsize=6.3,ha="right",va="top",color="#555")
    ax.text(3.0,3.2,"RD (low in T2-T3 of M1, M2)",fontsize=6.0,color="#999")
    X2,Y2=lowpulses(segs_rd,y0=hi,y1=lo); ax.plot(X2,Y2,color="#aaaaaa",lw=1.0,ls="--")
# buses
def bus(y,spans,h=0.55):
    for (a,b,t,c) in spans:
        ax.add_patch(mp.Rectangle((0.9+a,y),b-a,h,fc=c,ec=INK,lw=1,zorder=2)); ax.text(0.9+(a+b)/2,y+h/2,t,ha="center",va="center",fontsize=6.3,zorder=3)
bus(2.0,[(0,4,"PCH (PC high)",BLUE),(4,7,"PCH (PC+1 high)",BLUE),(7,10,"80H (port address)",GRN)])
bus(0.7,[(0,0.5,"PCL",YEL),(0.5,4,"opcode "+OPC,BLUE),(4,4.5,"PCL+1",YEL),(4.5,7,"data 80H (port no.)",BLUE),(7,7.5,"80H",GRN),(7.5,10,"data " + ("in from port to A" if INSTR=="IN" else "A out to port"),GRN)])
ax.text(5.9,-0.2,"10 T-states in 3 machine cycles",fontsize=8,ha="center",weight="bold")
```


*Time.* With a 2 MHz clock, one T-state is $T = 1/(2\times10^{6}) = 0.5\ \mu s$. The instruction needs 4 + 3 + 3 = 10 T-states:

$$t = 10 \times 0.5\ \mu s = 5\ \mu s.$$

@s 5
**(a) Architecture of the 8051.**

```figure caption="Internal architecture of the 8051 microcontroller: CPU, 4 KB ROM, 128-byte RAM, SFRs, two timers, interrupt control, serial port and four 8-bit I/O ports on one chip."
import numpy as _np, matplotlib.patches as mp
def box(ax,x,y,w,h,t,fc="white",ec=INK,fs=8,lw=1.2,ls="-"):
    ax.add_patch(mp.FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",fc=fc,ec=ec,lw=lw,ls=ls,zorder=3))
    ax.text(x,y,t,ha="center",va="center",fontsize=fs,zorder=4)
def arr(ax,a,b,c=None,rad=0.0,lw=1.2,sa=0,sb=0,style="-|>"):
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle=style,color=c or ACCENT,lw=lw,shrinkA=sa,shrinkB=sb,connectionstyle="arc3,rad=%s"%rad),zorder=2)
BLUE="#eaf3ff"; YEL="#fff4d6"; GRN="#e6f4ea"; RED="#fde8e8"
fig,ax=plt.subplots(figsize=(7.4,5.0)); ax.axis("off"); ax.set_xlim(0,15); ax.set_ylim(0,10)
box(ax,1.5,9.2,2.4,0.7,"On-chip\noscillator",fs=6.8,fc=YEL); box(ax,4.3,9.2,2.4,0.7,"External\ninterrupts",fs=6.5,fc=YEL)
box(ax,2.3,7.9,2.8,0.8,"Interrupt control",fs=7.2,fc=YEL); box(ax,5.4,7.9,2.8,0.8,"Timer 0 / Timer 1\n(T0, T1 pins)",fs=6.8,fc=GRN)
box(ax,2.0,6.5,2.4,1.0,"On-chip ROM\n4 KB program\nmemory",fs=6.5,fc=BLUE); box(ax,4.8,6.5,2.4,0.9,"On-chip RAM\n128 bytes",fs=6.8,fc=BLUE)
box(ax,7.6,6.5,2.4,0.9,"SFR block",fs=7,fc=BLUE)
box(ax,12.5,8.5,4.0,2.0,"CPU\nALU  Accumulator A  B reg\nPSW  SP  DPTR (DPH DPL)\nPC  instruction register\nTiming and control",fs=6.8,fc=YEL)
ax.plot([0.5,10.3],[5.1,5.1],color=INK,lw=3,solid_capstyle="butt"); ax.text(5.4,5.35,"8-bit internal data bus",fontsize=7,ha="center")
for x in (2.0,4.8,7.6): arr(ax,(x,6.05),(x,5.15),c=INK,style="<|-|>")
arr(ax,(2.3,7.5),(2.3,5.15),c=INK,style="<|-|>"); arr(ax,(5.4,7.5),(5.4,5.15),c=INK,style="<|-|>")
arr(ax,(10.5,8.0),(10.5,5.15),c=INK,style="<|-|>"); ax.plot([10.5,10.5,10.9],[8.0,8.0,8.0],color=INK,lw=1.2); ax.plot([10.5,11.4],[7.9,7.9],color=INK,lw=1.2)
for i,(n,x) in enumerate([("P0\nAD0-AD7",1.3),("P1",3.9),("P2\nA8-A15",6.2),("P3\nRD WR T0 T1\nINT0 INT1 TxD RxD",9.0)]):
    box(ax,x,3.6,2.0 if i<3 else 3.0,0.9,"I/O port "+n,fs=6.3,fc=GRN); arr(ax,(x,4.1),(x,5.1),c=INK,style="<|-|>"); arr(ax,(x,3.1),(x,2.2),c=ACCENT,style="<|-|>")
    ax.text(x,1.9,["8 pins","8 pins","8 pins","8 pins"][i],fontsize=6.5,ha="center")
box(ax,12.5,3.6,3.0,0.9,"Serial port\n(SBUF, SCON, TxD, RxD)",fs=6.5,fc=GRN); arr(ax,(11.0,3.6),(11.0,5.1),c=INK,style="<|-|>")
ax.plot([10.3,10.3,13.0,13.0],[5.1,5.1,5.1,5.1],color=INK,lw=3)
arr(ax,(12.5,7.4),(12.5,5.15),c=INK,style="<|-|>"); ax.plot([10.3,12.5],[5.1,5.1],color=INK,lw=3,solid_capstyle="butt")
ax.text(12.5,1.9,"TxD / RxD",fontsize=6.5,ha="center"); arr(ax,(12.5,3.1),(12.5,2.2),c=ACCENT,style="<|-|>")
ax.text(7.4,0.7,"40-pin DIP: Vcc, GND, RST, XTAL1, XTAL2, EA, PSEN, ALE",fontsize=6.8,ha="center")
```


The 8051 holds on one chip: an 8-bit CPU (ALU, accumulator A, B register, PSW, SP, 16-bit DPTR and PC), 4 KB of ROM, 128 bytes of RAM, two 16-bit timers/counters, five interrupt sources with two priority levels, a full-duplex serial port (UART) and four 8-bit I/O ports (P0 to P3, P0 and P2 doubling as the external address and data bus).

**Internal RAM organisation.**

```figure caption="Organisation of the 8051 internal memory: four register banks (00H-1FH), 16 bytes of bit-addressable RAM (20H-2FH), 80 bytes of scratch pad (30H-7FH) and the special function registers (80H-FFH)."
import numpy as _np, matplotlib.patches as mp
def box(ax,x,y,w,h,t,fc="white",ec=INK,fs=8,lw=1.2,ls="-"):
    ax.add_patch(mp.FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",fc=fc,ec=ec,lw=lw,ls=ls,zorder=3))
    ax.text(x,y,t,ha="center",va="center",fontsize=fs,zorder=4)
def arr(ax,a,b,c=None,rad=0.0,lw=1.2,sa=0,sb=0,style="-|>"):
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle=style,color=c or ACCENT,lw=lw,shrinkA=sa,shrinkB=sb,connectionstyle="arc3,rad=%s"%rad),zorder=2)
BLUE="#eaf3ff"; YEL="#fff4d6"; GRN="#e6f4ea"; RED="#fde8e8"
fig,ax=plt.subplots(figsize=(7.4,4.6)); ax.axis("off"); ax.set_xlim(0,14.4); ax.set_ylim(0,9.4)
def blk(x,y,w,h,t,fc,fs=7.2): ax.add_patch(mp.Rectangle((x,y),w,h,fc=fc,ec=INK,lw=1.2)); ax.text(x+w/2,y+h/2,t,ha="center",va="center",fontsize=fs)
ax.text(3.0,9.1,"Internal data memory (direct addresses)",ha="center",fontsize=8.2,weight="bold")
blk(2.0,7.2,4.0,1.5,"SFR (direct addressing only)\nP0 80H, SP 81H, DPL 82H, DPH 83H,\nTCON 88H, P1 90H, SCON 98H, P2 A0H,\nIE A8H, P3 B0H, IP B8H, PSW D0H, A E0H, B F0H",BLUE,6.2)
blk(2.0,3.7,4.0,3.5,"General purpose RAM\n(scratch pad, stack)\n30H - 7FH  (80 bytes)\nDirect or indirect",YEL)
blk(2.0,2.5,4.0,1.2,"Bit-addressable RAM\n20H - 2FH (128 bits, bit addr 00H-7FH)",GRN,6.8)
for i,(n,fc) in enumerate([("Bank 3: 18H-1FH (R0-R7)",RED),("Bank 2: 10H-17H",RED),("Bank 1: 08H-0FH",RED),("Bank 0: 00H-07H (default)",RED)]):
    blk(2.0,2.5-(i+1)*0.6,4.0,0.6,n,fc,6.5)
for y,t in [(8.7,"FFH"),(7.2,"80H"),(3.7,"30H"),(2.5,"20H"),(0.1,"00H")]: ax.text(1.8,y,t,ha="right",va="center",fontsize=7)
ax.text(1.8,6.9,"7FH",ha="right",va="center",fontsize=7); ax.text(1.8,3.4,"2FH",ha="right",va="center",fontsize=7)
ax.text(1.8,2.2,"1FH",ha="right",va="center",fontsize=7)
ax.text(9.9,8.6,"Register banks and PSW",ha="center",fontsize=8.2,weight="bold")
for i in range(8):
    ax.add_patch(mp.Rectangle((7.6+i*0.55,7.4),0.55,0.6,fc=BLUE if i<4 else YEL,ec=INK,lw=1)); ax.text(7.6+i*0.55+0.275,7.7,"R%d"%i,ha="center",va="center",fontsize=6.5)
ax.text(9.9,7.05,"bank select by PSW.4 (RS1) and PSW.3 (RS0)",ha="center",fontsize=6.8)
ax.text(9.9,6.4,"RS1 RS0  bank  address range",ha="center",fontsize=6.8,weight="bold")
for i,(a,b,c) in enumerate([("0 0","0","00H-07H"),("0 1","1","08H-0FH"),("1 0","2","10H-17H"),("1 1","3","18H-1FH")]): ax.text(9.9,5.9-i*0.5,"%s     %s     %s"%(a,b,c),ha="center",fontsize=6.8)
ax.text(9.9,3.5,"PSW:  CY AC F0 RS1 RS0 OV - P",ha="center",fontsize=7.2,family="monospace")
ax.text(9.9,2.8,"bit:    7  6  5   4   3  2 1 0",ha="center",fontsize=7.2,family="monospace")
```


- **00H to 1FH:** four register banks (R0 to R7 each). Bank selected by RS1, RS0 of the PSW; bank 0 after reset. The stack starts at 08H by default.
- **20H to 2FH:** 16 bytes = 128 **bit-addressable** bits, with bit addresses 00H to 7FH (used by SETB, CLR, CPL, JB, JNB).
- **30H to 7FH:** 80 bytes of general-purpose scratch-pad RAM (data and stack).
- **80H to FFH:** special function registers (not RAM): accessed with direct addressing.

**(b) Special function registers (SFR).** The SFRs are the registers that control and report on the on-chip peripherals and the CPU. They occupy the addresses 80H to FFH of the internal data space and are reached by direct addressing. Examples: A (E0H), B (F0H), PSW (D0H), SP (81H), DPTR (DPL 82H, DPH 83H), the ports P0 (80H), P1 (90H), P2 (A0H), P3 (B0H), timer registers TMOD (89H), TCON (88H), TH0/TL0 (8CH, 8AH), serial SCON (98H), SBUF (99H), interrupt IE (A8H), IP (B8H). Many SFRs (with an address divisible by 8) are also bit addressable.

**Program.** The Fahrenheit temperature is $F = \tfrac{9}{5}C + 32$. Writing $C = 5q + r$ ($q$ = quotient and $r$ = remainder of $C \div 5$) gives $\tfrac{9}{5}C = 9q + \lfloor 9r/5 \rfloor$ exactly, and every intermediate value fits in 8 bits. (Computing $9C$ first would overflow the byte for $C > 28$ and break the 8-bit `DIV AB`.)

```asm
        MOV  P1,#0FFH    ; make port 1 an input port (write 1s)
        MOV  A,P1        ; A = temperature in Celsius (0 to 123)
        MOV  B,#05H
        DIV  AB          ; A = q = C / 5, B = r = C mod 5
        MOV  R0,B        ; save r
        MOV  B,#09H
        MUL  AB          ; A = 9q
        MOV  R1,A        ; R1 = 9q
        MOV  A,R0        ; A = r
        MOV  B,#09H
        MUL  AB          ; A = 9r (at most 36)
        MOV  B,#05H
        DIV  AB          ; A = floor(9r / 5)
        ADD  A,R1        ; A = floor(9C / 5)
        ADD  A,#32       ; A = F
        MOV  P2,A        ; output the Fahrenheit value at port 2
        SJMP $
```

| C (port 1) | q, r | 9q | floor(9r/5) | F (port 2) |
|---|---|---|---|---|
| 0 | 0, 0 | 0 | 0 | 32 = 20H |
| 25 (19H) | 5, 0 | 45 | 0 | 77 = 4DH |
| 37 (25H) | 7, 2 | 63 | 3 | 98 = 62H (exact 98.6, truncated) |
| 100 (64H) | 20, 0 | 180 | 0 | 212 = D4H |

The program was run on an instruction-level simulator for every C from 0 to 123 and gave floor(9C/5) + 32 each time. The 8-bit output is valid up to C = 123 °C (F = 253); for larger C the result needs 9 bits.

@s 6
**(a) Interrupt processing in the 8085.** An interrupt is a hardware signal that makes the CPU suspend the program, run an **interrupt service routine (ISR)** and then resume. The 8085 has five interrupt inputs:

| Interrupt | Vector address | Type | Priority |
|---|---|---|---|
| TRAP | 0024H | non-maskable, level and edge triggered | 1 (highest) |
| RST 7.5 | 003CH | maskable, rising-edge (latched) | 2 |
| RST 6.5 | 0034H | maskable, level triggered | 3 |
| RST 5.5 | 002CH | maskable, level triggered | 4 |
| INTR | set by the device (RST n or CALL) | maskable, level triggered, **non-vectored** | 5 (lowest) |

*Sequence.* (1) The CPU finishes the present instruction and samples the interrupt lines. (2) If the interrupt is accepted (EI and not masked) the interrupt enable flip-flop is reset, so further maskable interrupts are disabled. (3) For INTR the CPU sends $\overline{INTA}$ and the device puts an instruction (e.g. RST 5 = EFH) on the data bus; for TRAP and RST x.5 the vector is built in. (4) The PC is pushed on the stack. (5) PC ← vector address and the ISR runs. (6) The ISR ends with `EI` and `RET`, which pops the old PC, and the main program continues.

*Masking.* `EI` and `DI` enable or disable all maskable interrupts. `SIM` (set interrupt mask) with the accumulator bits M7.5, M6.5, M5.5 (bits 2 to 0), MSE (bit 3, mask set enable) and R7.5 (bit 4, reset the RST 7.5 latch) masks individual interrupts; `RIM` reads the mask bits and the pending interrupts. Example, enabling only RST 6.5:

```asm
        MVI  A,0DH      ; MSE = 1, M7.5 = 1, M6.5 = 0, M5.5 = 1
        SIM             ; mask 7.5 and 5.5, leave 6.5 unmasked
        EI              ; enable the maskable interrupts
```

**(b) Assembling, linking and execution of an 8086 program.**

```figure caption="Assembling, linking and execution of an 8086 program: source file (.ASM) to object file (.OBJ) to executable (.EXE) to a running process."
import numpy as _np, matplotlib.patches as mp
def box(ax,x,y,w,h,t,fc="white",ec=INK,fs=8,lw=1.2,ls="-"):
    ax.add_patch(mp.FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",fc=fc,ec=ec,lw=lw,ls=ls,zorder=3))
    ax.text(x,y,t,ha="center",va="center",fontsize=fs,zorder=4)
def arr(ax,a,b,c=None,rad=0.0,lw=1.2,sa=0,sb=0,style="-|>"):
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle=style,color=c or ACCENT,lw=lw,shrinkA=sa,shrinkB=sb,connectionstyle="arc3,rad=%s"%rad),zorder=2)
BLUE="#eaf3ff"; YEL="#fff4d6"; GRN="#e6f4ea"; RED="#fde8e8"
fig,ax=plt.subplots(figsize=(7.4,2.6)); ax.axis("off"); ax.set_xlim(0,15.6); ax.set_ylim(0,5)
items=[(1.4,3.4,"Editor\n(source\nprogram)",BLUE),(4.3,3.4,"Assembler\nMASM / TASM",YEL),(7.2,3.4,"Linker\nLINK / TLINK",YEL),(10.1,3.4,"Loader\n(DOS / OS)",YEL),(13.0,3.4,"Run /\nDEBUG",GRN)]
for x,y,t,c in items: box(ax,x,y,2.2,1.4,t,fs=7,fc=c)
for x in (1.4,4.3,7.2,10.1): arr(ax,(x+1.1,3.4),(x+1.8,3.4),c=ACCENT)
for x,t in [(2.85,"prog.ASM"),(5.75,"prog.OBJ"),(8.65,"prog.EXE"),(11.55,"in memory")]: ax.text(x,4.35,t,ha="center",fontsize=6.8,color="#b00020")
box(ax,4.3,1.3,2.3,0.8,"prog.LST (listing)\nprog.CRF",fs=6.3,fc="white"); arr(ax,(4.3,2.7),(4.3,1.7),c=INK)
box(ax,7.2,1.3,2.3,0.8,"Library files\n+ other .OBJ",fs=6.3,fc="white"); arr(ax,(7.2,1.7),(7.2,2.7),c=INK)
box(ax,10.1,1.3,2.3,0.8,"PSP + segments\nCS:IP, SS:SP set",fs=6.3,fc="white"); arr(ax,(10.1,1.7),(10.1,2.7),c=INK)
box(ax,7.2,0.0,0.01,0.01,"",ec="white")
```


1. **Editing:** the source program is written in a text editor and saved as `prog.ASM`.
2. **Assembling:** the assembler (MASM, TASM) translates the mnemonics into machine code. It makes two passes: pass 1 builds the symbol table (labels with their offsets), pass 2 generates the code. The output is the **object file** `prog.OBJ` (relocatable code with unresolved addresses), plus an optional listing `prog.LST` (source, code and addresses) and a cross-reference file. Syntax errors are reported here.
3. **Linking:** the linker (LINK, TLINK) combines one or more object files and library routines, resolves the external references, assigns the segment addresses and produces the **executable** `prog.EXE` (and a map file).
4. **Loading and execution:** the DOS loader builds the Program Segment Prefix (PSP), loads the EXE into free memory, relocates the segment references, sets CS:IP (start address) and SS:SP and gives control to the program. The program runs until it returns to DOS with `INT 21H` function 4CH.
5. **Debugging:** DEBUG, CodeView or Turbo Debugger run the program step by step, show registers, flags and memory, so logic errors can be found and corrected (then steps 1 to 4 are repeated).

**(c) Addressing modes of the 8051.**

| Mode | Operand is | Example | Meaning |
|---|---|---|---|
| Immediate | a constant in the instruction (`#`) | `MOV A,#25H`  `MOV DPTR,#2000H` | A ← 25H; DPTR ← 2000H |
| Register | in R0 to R7 of the selected bank | `MOV A,R3`  `ADD A,R5` | A ← R3; A ← A + R5 |
| Direct | at the 8-bit internal RAM or SFR address in the instruction | `MOV A,30H`  `MOV P1,A` | A ← [30H]; port 1 ← A |
| Register indirect | at the address held in R0 or R1 (or DPTR for external data) | `MOV A,@R0`  `MOVX A,@DPTR` | A ← [R0]; A ← external [DPTR] |
| Indexed | at (base register + A) in the program memory | `MOVC A,@A+DPTR`  `MOVC A,@A+PC` | look-up tables: A ← code[DPTR + A] |
| Bit | a single bit (bit address or name) | `SETB P1.0`  `CLR C`  `JB 20H.3,L` | set P1.0; clear carry; jump if the bit is 1 |
| Implied | fixed by the opcode (A, carry, DPTR) | `CPL A`  `RL A`  `INC DPTR` | complement A; rotate A left |

Relative addressing is used by the jumps (`SJMP`, `JNC`, `DJNZ`): the signed 8-bit offset is added to the PC (range −128 to +127).
