---
file: NEBians-IOE-Past-Paper-Microprocessors-and-Microcontrollers-ENEX251-2083-Baishakh.pdf
subject: Microprocessors and Microcontrollers
level: BE · Year II / Part II
code: ENEX 251
year_bs: 2083 Baishakh
cal: BS
year_ad: 2026
stream: BEL
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Back (New Course). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
Compare the Hardwired Control Unit and the Microprogrammed Control Unit, highlighting their advantages and limitations. [[4]]

@q 2
a) Describe the different types of branching instructions supported by the 8085 microprocessor. Explain each with suitable examples. [[6]]

b) Write an 8085 program to calculate the sum of numbers from 1 to n, where n is a byte stored in memory address 8050H. Display the sum at output port 41H. [[6]]

@q 3
a) Describe the functions and components of the Bus Interface Unit (BIU) and Execution Unit (EU) in the 8086 microprocessor. [[6]]

b) Write an assembly language program for the 8086 microprocessor to read a string, display each word of the string on a separate line, count the number of words present in the string, and display the word count. [[6]]

@q 4
a) Differentiate between synchronous bus and asynchronous bus. Design an address decoding circuit to interface: 4 KB ROM and 2 KB RAM. The starting address is 4000H. Use a suitable decoder. [[2+4]]

b) Show the machine cycles involved during execution of the instruction IN 80H. Calculate the time required to execute the instruction if the microprocessor is operating at a 4 MHz clock frequency. [[5+1]]

@q 5
a) Draw the internal architecture of the 8051 microcontroller and explain briefly its internal RAM organization. [[2+4]]

b) Write an assembly language program on 8051 to add ten bytes stored in the internal RAM. Assume that the starting location of the data block is 40H, the sum is a 16-bit result, and the final result is stored in registers R2 and R3 of register bank 0, with the LSB in R2 and the MSB in R3. [[6]]

@q 6
Write short notes on: (Any Two) [[2×4]]

a) Microprocessor vs Microcontroller

b) Addressing modes of 8085

c) Flag register of 8086 microprocessor

<!-- SOLUTIONS -->

@s 1
**Control unit.** The control unit generates the control signals (register loads, ALU function, memory and I/O strobes) that carry out each instruction. It can be built in two ways.

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
| Speed | **faster**, only gate delays | slower, one control-memory read per microinstruction |
| Design effort | complex: state tables, logic minimisation | simple: write a microprogram like a program |
| Flexibility | hard to modify or extend, the hardware must be redesigned | easy to modify, add or correct instructions by changing the ROM |
| Instruction set | small and regular (RISC style, e.g. MIPS) | large and complex (CISC style, e.g. 8086, VAX) |
| Chip area and cost | less control store, but irregular layout | needs a control memory; regular layout, easier to test |
| Errors | an error needs a redesign | an error is fixed by changing a microinstruction |

**Advantages and limitations.**

- *Hardwired:* **advantage**: very high speed, no memory access; compact for small instruction sets; **limitation**: inflexible, long design time, hard to debug, grows unmanageable for a complex instruction set.
- *Microprogrammed:* **advantage**: systematic, flexible, a new instruction or an emulation of another machine is only a new routine, cheap to debug; **limitation**: slower because every microinstruction is fetched from the control memory, the extra control store costs area and power.

@s 2
**(a) Branching instructions of the 8085.** A branching instruction changes the normal sequential flow by loading a new address into the program counter. There are three groups, and each of them has an unconditional and a conditional form. The flags tested are **Z, CY, S, P**.

| Group | Unconditional | Conditional (test a flag) | Action |
|---|---|---|---|
| Jump (3 bytes) | `JMP addr` | `JC` `JNC` `JZ` `JNZ` `JP` `JM` `JPE` `JPO` | PC ← addr (if the condition is true) |
| Call (3 bytes) | `CALL addr` | `CC` `CNC` `CZ` `CNZ` `CP` `CM` `CPE` `CPO` | push PC (return address) on the stack, PC ← addr |
| Return (1 byte) | `RET` | `RC` `RNC` `RZ` `RNZ` `RP` `RM` `RPE` `RPO` | pop the return address from the stack into PC |
| Restart (1 byte) | `RST 0` to `RST 7` | none | a 1-byte call to the address 8 × n |
| Jump indirect | `PCHL` | none | PC ← HL |

Conditions: C = carry set (CY = 1), NC = CY = 0, Z = result zero, NZ = not zero, P = plus (S = 0), M = minus (S = 1), PE = parity even (P = 1), PO = parity odd (P = 0).

*Examples.*

1. **Unconditional jump.** `JMP 2050H` loads PC with 2050H, so the next instruction executed is the one at 2050H (10 T-states).
2. **Conditional jump.** `JNZ LOOP` jumps to LOOP only when the Z flag is 0 (10 T if taken, 7 T if not). Used for loops: `DCR C` then `JNZ LOOP`.
3. **Call and return.** `CALL 3000H` at address 2000H pushes the return address 2003H (high byte first) on the stack and sets PC = 3000H; the subroutine ends with `RET`, which pops 2003H back into PC (18 T for CALL, 10 T for RET). `CZ 3000H` calls only if Z = 1 (18 T or 9 T), `RNC` returns only if CY = 0 (12 T or 6 T).
4. **Restart.** `RST 5` is a call to 0028H (5 × 8 = 40 = 28H), 12 T-states. Used by the hardware interrupts (RST 5.5 is at 002CH).
5. **PCHL.** If HL = 2400H then `PCHL` makes PC = 2400H (a computed jump, 6 T).

**(b) Sum of 1 to n.** The sum is $S = 1 + 2 + \dots + n = \dfrac{n(n+1)}{2}$. Algorithm: A ← 0; C ← n; repeat {A ← A + C; C ← C − 1} until C = 0; output A.

```asm
        LDA  8050H      ; A = n
        MOV  C,A        ; C = counter = n
        MVI  A,00H      ; A = sum = 0
LOOP:   ADD  C          ; sum = sum + C
        DCR  C          ; C = C - 1 (sets Z)
        JNZ  LOOP       ; repeat until C = 0
        OUT  41H        ; display the sum at port 41H
        HLT
```

*Check (n = 5):* A = 5, 9, 12, 14, 15 → output 0FH = 15 = 5·6/2. The program was run on an instruction-level simulator for every n from 1 to 22 and gave $n(n+1)/2$ each time.

**Limitation and improved version.** A byte holds at most 255, so the 8-bit program is right only for n ≤ 22 (n = 23 gives 276). For any n in 0 to 255 (maximum sum 255·256/2 = 32 640 = 7F80H) use a 16-bit sum in HL and a 16-bit counter DE, also handling n = 0 (the plain loop would run 256 times):

```asm
        LXI  H,0000H    ; HL = sum
        LDA  8050H
        MOV  E,A        ; DE = counter (E = n, D = 0)
        MVI  D,00H
        ORA  A
        JZ   DONE
LOOP:   DAD  D          ; HL = HL + DE
        DCX  D          ; DE = DE - 1
        MOV  A,D
        ORA  E          ; Z = 1 when DE = 0
        JNZ  LOOP
DONE:   MOV  A,L
        OUT  41H        ; low byte at 41H
        MOV  A,H
        OUT  42H        ; high byte at 42H
        HLT
```

@s 3
**(a) BIU and EU of the 8086.** The 8086 is split into two units that work in parallel; this overlap of instruction fetch and execution is a two-stage **pipeline**.

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


**Bus Interface Unit (BIU).** Interfaces the processor with memory and I/O: it fetches instructions, reads operands and writes results. Its components and functions:

| Component | Function |
|---|---|
| Segment registers CS, DS, SS, ES (16 bit) | hold the base (segment) addresses of the code, data, stack and extra segments |
| Instruction pointer IP | offset of the next instruction in the code segment (not directly accessible) |
| Address adder | forms the 20-bit physical address: segment × 16 + offset (so 1 MB can be addressed) |
| Instruction queue (6 bytes, FIFO) | prefetches instruction bytes while the EU is busy; as soon as 2 bytes are free the BIU fetches the next word, so the EU seldom waits |
| Bus control logic | generates the address, data and control signals (ALE, RD, WR, M/IO, DT/R, DEN, BHE) for the system bus |

**Execution Unit (EU).** Decodes and executes instructions taken from the queue; it has no connection to the system bus (it asks the BIU for any memory or I/O access).

| Component | Function |
|---|---|
| Control circuitry and instruction decoder | decodes the opcode from the queue and generates the control signals |
| ALU (16 bit) | arithmetic and logic operations |
| General registers AX, BX, CX, DX | data registers, each also two 8-bit halves (AH/AL, ...); AX accumulator, BX base, CX count, DX data/port |
| Pointer and index registers SP, BP, SI, DI | stack pointer, base pointer, source and destination index (offsets) |
| Flag register | 9 flags: CF, PF, AF, ZF, SF, OF (status) and TF, IF, DF (control) |
| Temporary registers | hold operands of the ALU |

On a jump or call the queue is flushed and refilled from the new address.

**(b) 8086 program: words on separate lines and word count.** The program reads the string with DOS function 0AH (buffered keyboard input), scans it character by character and treats a run of non-space characters as one word. Each character of a word is displayed with function 02H; at the end of a word (a space) a new line is printed. A flag in BL tells whether the scan is inside a word, and BH counts the words. Finally the count is converted to decimal and displayed.

```asm
.MODEL SMALL
.STACK 100H
.DATA
  MSG1  DB 'Enter a string: $'
  MSG2  DB 'Word count = $'
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
        INT  21H            ; read the string
        LEA  DX,NL
        MOV  AH,09H
        INT  21H            ; new line after the Enter key
        LEA  SI,BUF+2       ; SI -> first character
        MOV  CL,BUF+1       ; CL = number of characters read
        MOV  CH,0           ; CX = count
        MOV  BX,0           ; BL = in-word flag (0), BH = word count (0)
NEXT:   CMP  CX,0
        JE   ENDSTR         ; all characters processed
        MOV  DL,[SI]        ; DL = current character
        INC  SI
        DEC  CX
        CMP  DL,' '
        JE   SPACE
        CMP  BL,0           ; non-space: already inside a word?
        JNE  SHOW
        MOV  BL,1           ; a new word starts
        INC  BH             ; word count + 1
SHOW:   MOV  AH,02H
        INT  21H            ; display the character in DL
        JMP  NEXT
SPACE:  CMP  BL,0
        JE   NEXT           ; extra space between words: ignore
        MOV  BL,0           ; the word has ended
        LEA  DX,NL
        MOV  AH,09H
        INT  21H            ; next word on a new line
        JMP  NEXT
ENDSTR: CMP  BL,0
        JE   COUNT          ; string ended with a space: line already ended
        LEA  DX,NL
        MOV  AH,09H
        INT  21H            ; end the last word
COUNT:  LEA  DX,MSG2
        MOV  AH,09H
        INT  21H
        MOV  AL,BH
        MOV  AH,0
        MOV  BL,10
        DIV  BL             ; AL = tens, AH = units
        MOV  CX,AX          ; CL = tens, CH = units
        MOV  DL,CL
        CMP  DL,0
        JE   UNITS          ; no leading zero
        ADD  DL,30H
        MOV  AH,02H
        INT  21H
UNITS:  MOV  DL,CH
        ADD  DL,30H
        MOV  AH,02H
        INT  21H            ; display the units digit
        MOV  AH,4CH
        INT  21H            ; return to DOS
MAIN ENDP
END MAIN
```

*Sample run.* Input `Nepal is  beautiful` (two spaces after *is*):

```text
Enter a string: Nepal is  beautiful
Nepal
is
beautiful
Word count = 3
```

A string of at most 80 characters has at most 40 words, so the count has at most two decimal digits, which the conversion by `DIV BL` handles. Only the space is used as a word separator (a tab could be added with one more `CMP DL,09H`).

@s 4
**(a) Synchronous and asynchronous bus.**

| Basis | Synchronous bus | Asynchronous bus |
|---|---|---|
| Timing | all transfers are timed by a common **clock** on the bus | no common clock; a **handshake** (request / acknowledge, e.g. MSYN and SSYN) controls each transfer |
| Speed | fixed by the slowest device, all devices must run at the bus clock | each transfer runs at the speed of the two devices; mixing fast and slow devices is easy |
| Hardware | simple, cheap interface | more complex control logic |
| Length | short buses (clock skew) | can be longer |
| Example | the 8085 / 8086 system bus, PCI | SCSI, the 8085 with the READY or wait-state logic, Multibus |

**Address-decoding design.**

*Step 1, sizes and ranges.* ROM 4 KB = $2^{12}$ bytes needs 12 address lines (A0 to A11); RAM 2 KB = $2^{11}$ bytes needs 11 lines (A0 to A10). The ROM starts at 4000H and the RAM follows it.

| Chip | Start | End | A15 A14 A13 A12 | A11 | Lines to the chip |
|---|---|---|---|---|---|
| ROM 4 KB | 4000H | 4FFFH | 0 1 0 0 | x | A0 to A11 |
| RAM 2 KB | 5000H | 57FFH | 0 1 0 1 | 0 | A0 to A10 |

*Step 2, decoder.* A 74LS138 (3 to 8 decoder) is used. Its select inputs are C = A14, B = A13, A = A12; its enables are G1 = +5 V (always on), G2A = A15 (must be 0) and G2B = IO/M (must be 0, a memory access). Then

- $Y_4$ goes low for $A_{14}A_{13}A_{12} = 100$, that is 4000H to 4FFFH: it is connected to the chip select of the **ROM**;
- $Y_5$ goes low for 101, that is 5000H to 5FFFH (4 KB): this is more than the 2 KB RAM, so $Y_5$ is OR-ed with A11: $\overline{CS}_{RAM} = Y_5 + A_{11}$, which is low only when $Y_5 = 0$ and $A_{11} = 0$, i.e. 5000H to 57FFH.

```figure caption="Address decoding for 4 KB ROM at 4000H and 2 KB RAM at 5000H with a 74LS138 (Y4 selects the ROM; Y5 OR A11 selects the RAM)."
import numpy as _np, matplotlib.patches as mp
def box(ax,x,y,w,h,t,fc="white",ec=INK,fs=8,lw=1.2,ls="-"):
    ax.add_patch(mp.FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",fc=fc,ec=ec,lw=lw,ls=ls,zorder=3))
    ax.text(x,y,t,ha="center",va="center",fontsize=fs,zorder=4)
def arr(ax,a,b,c=None,rad=0.0,lw=1.2,sa=0,sb=0,style="-|>"):
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle=style,color=c or ACCENT,lw=lw,shrinkA=sa,shrinkB=sb,connectionstyle="arc3,rad=%s"%rad),zorder=2)
BLUE="#eaf3ff"; YEL="#fff4d6"; GRN="#e6f4ea"; RED="#fde8e8"
fig,ax=plt.subplots(figsize=(7.4,4.4)); ax.axis("off"); ax.set_xlim(0,14.8); ax.set_ylim(0,8.9)
C1=('ROM', '4', '4000H - 4FFFH', 4, 'A0-A11, D0-D7, RD', 0); C2=('RAM', '2', '5000H - 57FFH', 5, 'A0-A10, D0-D7, RD, WR', 1); G1='+5V'; G2A='A15'; G2B='IO/M'
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


The low address lines AD0 to AD7 are demultiplexed with a 74LS373 latch controlled by ALE. The ROM output enable is driven by $\overline{RD}$, the RAM by $\overline{RD}$ and $\overline{WR}$. The block 5800H to 5FFFH and the rest of the space is unused (it can be given to other devices).

**(b) Machine cycles of `IN 80H`.** The instruction `IN 80H` (opcode DBH, 2 bytes) copies the byte from input port 80H to the accumulator. It needs **three machine cycles** and 10 T-states.

| Machine cycle | T-states | IO/M | Status S1 S0 | What happens |
|---|---|---|---|---|
| 1. Opcode fetch (M1) | 4 | 0 | 1 1 | PC is placed on the address bus, ALE = 1 in T1; RD low in T2 and T3 reads the opcode DBH into the instruction register; T4 decodes it |
| 2. Memory read (M2) | 3 | 0 | 1 0 | address PC + 1; the second byte (port address 80H) is read into a temporary register |
| 3. I/O read (M3) | 3 | 1 | 1 0 | the port address 80H is placed on A15 to A8 **and** AD7 to AD0; RD low in T2 and T3 reads the data from the port into the accumulator |

```figure caption="Machine cycles and timing of IN 80H: opcode fetch (4 T), memory read of the port address (3 T) and I/O read (3 T)."
import numpy as _np, matplotlib.patches as mp
def box(ax,x,y,w,h,t,fc="white",ec=INK,fs=8,lw=1.2,ls="-"):
    ax.add_patch(mp.FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",fc=fc,ec=ec,lw=lw,ls=ls,zorder=3))
    ax.text(x,y,t,ha="center",va="center",fontsize=fs,zorder=4)
def arr(ax,a,b,c=None,rad=0.0,lw=1.2,sa=0,sb=0,style="-|>"):
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle=style,color=c or ACCENT,lw=lw,shrinkA=sa,shrinkB=sb,connectionstyle="arc3,rad=%s"%rad),zorder=2)
BLUE="#eaf3ff"; YEL="#fff4d6"; GRN="#e6f4ea"; RED="#fde8e8"
fig,ax=plt.subplots(figsize=(7.4,4.4)); ax.set_xlim(0,10.9); ax.set_ylim(-0.4,8.6); ax.axis("off")
INSTR='IN'; OPC='DBH'; THIRD='IO read'
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


*Time.* Total states = 4 + 3 + 3 = 10 T. With the processor clock at 4 MHz, one T-state is $T = 1/f = 1/(4\times 10^{6}) = 0.25\ \mu s$, so

$$t = 10 \times 0.25\ \mu s = 2.5\ \mu s.$$

(If 4 MHz is the crystal frequency, the 8085 divides it by two, the internal clock is 2 MHz, and the time would be 5 µs.)

@s 5
**(a) Architecture of the 8051.** The 8051 is an 8-bit microcontroller: CPU, program ROM, data RAM, timers, interrupt logic, serial port and I/O ports on one chip.

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


- **CPU:** 8-bit ALU, accumulator A, B register (multiply and divide), PSW (flags CY, AC, F0, RS1, RS0, OV, P), stack pointer SP (8 bit, default 07H), data pointer DPTR (16 bit), program counter PC (16 bit).
- **Memory:** 4 KB on-chip ROM (code, up to 64 KB external), 128 bytes on-chip RAM (up to 64 KB external data), special function registers.
- **Timers:** two 16-bit timer/counters T0 and T1. **Serial port:** full-duplex UART (SBUF, SCON). **Interrupts:** five sources (INT0, INT1, T0, T1, serial), two priority levels.
- **I/O:** four 8-bit ports P0 to P3 (32 lines); P0 and P2 also form the multiplexed external address/data bus; P3 has alternate functions.

**Internal RAM organisation.** The 128-byte internal RAM (addresses 00H to 7FH) is divided in three areas; the SFRs occupy 80H to FFH.

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


1. **Register banks, 00H to 1FH (32 bytes):** four banks of eight registers R0 to R7; the active bank is selected by the bits RS1 and RS0 of the PSW (after reset bank 0 is selected, 00H to 07H). The stack also starts here, at 08H, by default.
2. **Bit-addressable area, 20H to 2FH (16 bytes = 128 bits):** every bit has an address 00H to 7FH, so single bits can be set, cleared or tested with SETB, CLR, JB (the byte 20H holds bits 00H to 07H, ... 2FH holds 78H to 7FH).
3. **General-purpose (scratch-pad) area, 30H to 7FH (80 bytes):** byte-addressable; used for data and for the stack.
4. **SFRs, 80H to FFH:** accessed by direct addressing only (the upper 128 bytes of the 8052 are RAM reached by indirect addressing).

**(b) 8051 program: sum of ten bytes.** Pointer R0 = 40H, counter R7 = 10, sum R3:R2 = 0. For each byte: A = R2 + byte; R2 = A; if a carry is generated then R3 is incremented.

```asm
        MOV  R0,#40H     ; R0 = pointer to the data block
        MOV  R7,#0AH     ; R7 = counter = 10
        MOV  R2,#00H     ; R2 = LSB of the sum
        MOV  R3,#00H     ; R3 = MSB of the sum
AGAIN:  MOV  A,R2
        ADD  A,@R0       ; A = LSB + data byte
        MOV  R2,A
        JNC  SKIP        ; no carry: nothing to add to the MSB
        INC  R3          ; carry: MSB = MSB + 1
SKIP:   INC  R0          ; next byte
        DJNZ R7,AGAIN    ; repeat 10 times
        SJMP $           ; stop (R3:R2 = sum)
```

*Check.* The routine was run on an 8051 instruction simulator with 50 random data blocks and R3:R2 always equalled the sum; the largest possible sum is ten bytes of FFH: $10 \times 255 = 2550 = 09F6H$, so R3 = 09H and R2 = F6H.

@s 6
**(a) Microprocessor vs microcontroller.**

| Basis | Microprocessor (8085, 8086) | Microcontroller (8051) |
|---|---|---|
| Chip content | CPU only; memory, I/O and timers are external chips | CPU, RAM, ROM, I/O ports, timers, serial port on one chip |
| Application | general purpose (PCs, computation); the program is changed | dedicated, embedded (washing machine, remote, meters) |
| Memory and I/O | large external memory; many external chips | small on-chip memory; few external parts |
| Instruction set | many addressing modes, mostly memory-oriented | many bit-handling, I/O-oriented instructions |
| Cost and size | the system costs more and is bigger | a low-cost, small, low-power system |
| Speed (clock) | high (MHz to GHz) | lower (12 to 40 MHz) |
| Bit operations | few | many (bit-addressable RAM and SFRs) |
| Power saving | usually none built in | idle and power-down modes |

**(b) Addressing modes of the 8085.** The way the operand is specified. There are five modes.

| Mode | Operand is | Example | Meaning |
|---|---|---|---|
| Immediate | in the instruction itself | `MVI A,32H`  `LXI H,2050H` | A ← 32H; HL ← 2050H |
| Register | in a register | `MOV A,B`  `ADD C` | A ← B; A ← A + C |
| Direct | at the 16-bit (or 8-bit I/O) address in the instruction | `LDA 2050H`  `STA 3000H`  `IN 80H` | A ← [2050H]; [3000H] ← A; A ← port 80H |
| Register indirect | at the address held in a register pair | `MOV A,M`  `LDAX B`  `STAX D` | A ← [HL]; A ← [BC]; [DE] ← A |
| Implied (implicit) | the operand is fixed by the opcode (usually A) | `CMA`  `RAL`  `STC` | A ← NOT A; rotate A left; CY ← 1 |

**(c) Flag register of the 8086.** A 16-bit register of which nine bits are flags.

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
| CF carry | status | carry out of (or borrow into) the MSB of the result |
| PF parity | status | 1 if the low byte of the result has an even number of 1s |
| AF auxiliary carry | status | carry from bit 3 to bit 4 (used by BCD adjust DAA, DAS) |
| ZF zero | status | 1 if the result is zero |
| SF sign | status | copy of the MSB of the result (1 = negative) |
| OF overflow | status | signed overflow (result outside the range of the destination) |
| TF trap | control | 1 = single-step mode (an interrupt after each instruction) |
| IF interrupt enable | control | 1 = the maskable INTR is accepted (STI / CLI) |
| DF direction | control | 0 = string instructions auto-increment SI, DI; 1 = auto-decrement (CLD / STD) |

Example: `MOV AL,7FH` then `ADD AL,01H` gives AL = 80H with SF = 1, OF = 1 (positive + positive = negative), ZF = 0, CF = 0, PF = 0 (one 1 bit), AF = 1.
