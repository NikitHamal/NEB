---
file: NEBians-IOE-Past-Paper-Microprocessor-ENEX201-2082-Kartik.pdf
subject: Microprocessor
level: BE · Year II / Part I
code: ENEX201
year_bs: 2082 Kartik
cal: BS
year_ad: 2025
stream: BCT, BEI
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Back (New Course). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
What is microprocessor? Explain briefly about the organization of a microprocessor based system. [[1+5]]

@q 2
Draw the internal architecture of 8085 microprocessor and explain briefly about its major components. [[8]]

@q 3
Write a program in 8085 to multiply two 8 bit binary numbers stored at 2050H and 2051H where multiplicand is at 2050H and multiplier is at 2051H. Store 16 bit result at memory location 2052H. [[6]]

@q 4
What is addressing mode? Explain briefly about different types of addressing mode used in 8086 with suitable example. [[2+6]]

@q 5
Write an Assembly language programming in 8086 to display, find the factorial of given number. (The given number is in location 2050H). [[6]]

@q 6
Explain in brief about 8257 with its block diagram. [[6]]

@q 7
Design an address decoding circuit to interface one 4Kx8 EPROM chip and two 2Kx8 RAM chip with 8085 microprocessor. [[6]]

@q 8
Differentiate between Memory mapped I/O and I/O mapped I/O. [[3]]

@q 9
What is an interrupt? Explain briefly about the features of different types of Hardware interrupts in 8085. [[2+5]]

@q 10
Explain briefly about Flynn's classification of multiprocessor computer architectures. [[4]]
<!-- SOLUTIONS -->

@s 1
A **microprocessor** is a programmable, multipurpose integrated circuit (a single VLSI chip) that contains the **central processing unit**: the arithmetic and logic unit, the registers and the control unit. It fetches instructions from memory, decodes them, executes them and communicates with memory and I/O devices through buses. It needs external memory and I/O to form a computer (examples: Intel 8085, 8086).

**Organization of a microprocessor-based system.**

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

*Working.* To execute a program the CPU puts the address of the next instruction on the address bus, the control bus carries the memory-read command, and the instruction comes back over the data bus. After decoding, the CPU reads or writes data in the same way (for memory or for an I/O device selected by IO/M). Address decoding logic converts the upper address lines into chip-select signals of the memory and interface chips.

@s 2
The 8085 is an 8-bit microprocessor with a 16-bit address bus (64 KB memory), a single +5 V supply and a 3 MHz clock (internal), made in NMOS technology with 6500 transistors in a 40-pin package.

```figure caption="Internal architecture of the 8085: registers (blue/green) on one internal data bus, the ALU, and the control section (red) that decodes instructions and produces timing, interrupt and serial I/O signals."
import numpy as _np, matplotlib.patches as mp
def box(ax,x,y,w,h,t,fc="white",ec=INK,fs=8,lw=1.2,ls="-"):
    ax.add_patch(mp.FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",fc=fc,ec=ec,lw=lw,ls=ls,zorder=3))
    ax.text(x,y,t,ha="center",va="center",fontsize=fs,zorder=4)
def arr(ax,a,b,c=None,rad=0.0,lw=1.2,sa=0,sb=0,style="-|>"):
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle=style,color=c or ACCENT,lw=lw,shrinkA=sa,shrinkB=sb,connectionstyle="arc3,rad=%s"%rad),zorder=2)
BLUE="#eaf3ff"; YEL="#fff4d6"; GRN="#e6f4ea"; RED="#fde8e8"
fig,ax=plt.subplots(figsize=(7.4,5.0)); ax.axis("off"); ax.set_xlim(0,14.8); ax.set_ylim(0,10)
ax.add_patch(mp.Rectangle((0.1,0.2),14.6,9.6,fc="#fafcff",ec=INK,lw=1.3,ls="--",zorder=1)); ax.text(7.4,9.45,"8085 microprocessor",ha="center",fontsize=9,weight="bold")
BX=7.3
ax.plot([BX,BX],[0.7,8.9],color=INK,lw=2.4,zorder=2); ax.text(BX,9.05,"internal 8-bit data bus",fontsize=6.5,ha="center")
def tie(x,y,fr=True): ax.plot([x,BX],[y,y],color="#777",lw=1.0,zorder=2)
box(ax,1.6,8.2,2.6,0.8,"Accumulator (8)",fs=7.2,fc=BLUE); tie(2.9,8.2)
box(ax,1.6,7.0,2.6,0.8,"Temporary register (8)",fs=7.0,fc=BLUE)
box(ax,1.6,5.8,2.6,0.8,"Flag register\nS Z AC P CY",fs=6.8,fc=BLUE)
box(ax,4.9,6.9,2.2,2.6,"ALU",fs=10,fc=YEL); ax.plot([4.9,4.9],[8.2,8.2]); tie(6.0,6.9)
ax.plot([2.9,3.8],[8.2,8.2],color="#777",lw=1); ax.plot([2.9,3.8],[7.0,7.0],color="#777",lw=1); ax.plot([2.9,3.8],[5.8,5.8],color="#777",lw=1)
for i,(a,b) in enumerate([("B","C"),("D","E"),("H","L"),("W","Z")]):
    y=4.5-i*0.85; box(ax,1.2,y,1.6,0.65,a,fs=8,fc=GRN); box(ax,2.9,y,1.6,0.65,b,fs=8,fc=GRN); tie(3.7,y)
box(ax,2.1,0.95,3.4,0.65,"Stack pointer SP (16)",fs=7,fc=GRN); tie(3.8,0.95)
box(ax,2.1,0.1+0.0001,0.0001,0.0001,"",fs=1,ec="white")
box(ax,9.4,8.3,2.4,0.8,"Instruction register (8)",fs=6.8,fc=RED); tie(8.2,8.3); ax.plot([8.2,BX],[8.3,8.3],color="#777",lw=1)
box(ax,9.4,7.2,2.4,0.8,"Instruction decoder\nand machine cycle\nencoder",fs=6.2,fc=RED)
box(ax,9.4,5.6,2.4,1.3,"Timing and control\nCLK  ALE  RD  WR\nIO/M  S0  S1  READY\nRESET IN / OUT",fs=6.2,fc=RED)
box(ax,9.4,3.9,2.4,1.3,"Interrupt control\nINTR  INTA  TRAP\nRST7.5  RST6.5\nRST5.5",fs=6.2,fc=RED)
box(ax,9.4,2.4,2.4,0.9,"Serial I/O control\nSID  SOD",fs=6.6,fc=RED)
box(ax,13.1,7.9,3.0,0.8,"Program counter (16)",fs=6.8,fc=GRN)
box(ax,13.1,6.6,3.0,0.8,"Incrementer / decrementer\naddress latch (16)",fs=6.2,fc=GRN)
box(ax,13.1,4.9,3.0,0.8,"Address buffer\nA15 - A8 (output)",fs=6.5,fc=BLUE)
box(ax,13.1,3.6,3.0,0.8,"Address / data buffer\nAD7 - AD0 (bidirectional)",fs=6.2,fc=BLUE)
for y in (7.9,6.6,4.9,3.6): ax.plot([BX,11.6],[y,y],color="#777",lw=1.0,zorder=1)
ax.plot([8.2,8.2],[8.3,7.2],color="#999",lw=0.8); ax.plot([9.4,9.4],[6.8,6.3],color="#999",lw=0.8)
ax.text(9.4,0.95,"8085 internal architecture",fontsize=6.6,ha="center",color="#555",style="italic")
```


**Major components**

1. **Arithmetic and logic unit (ALU).** Performs the 8-bit addition, subtraction, AND, OR, XOR, complement, rotate, increment and decrement. One operand is always the accumulator, the other comes from the temporary register; the result goes back to the accumulator and the flags are updated.
2. **Accumulator (A).** 8-bit register, the main data register of the ALU: it holds one operand before and the result after an operation, and is used for all I/O transfers (IN / OUT).
3. **Temporary register.** Hidden register that holds the second operand during the ALU operation (not accessible to the programmer).
4. **Flag register.** Five flip-flops: **S** (sign), **Z** (zero), **AC** (auxiliary carry), **P** (parity) and **CY** (carry), set or cleared after arithmetic and logic operations; used by conditional jumps.
5. **General purpose registers B, C, D, E, H, L.** Six 8-bit registers, usable singly or as the 16-bit pairs BC, DE, HL (HL also acts as the memory pointer M). W and Z are temporary registers used by the CPU itself for CALL, XCHG, etc.
6. **Program counter (PC), 16 bit.** Holds the address of the next instruction to be fetched; it is incremented after each fetch.
7. **Stack pointer (SP), 16 bit.** Points to the top of the stack in R/W memory (PUSH, POP, CALL, RET, interrupts).
8. **Instruction register and decoder.** The opcode fetched from memory is held in the instruction register (8 bit) and decoded; the decoder passes the result to the timing and control unit.
9. **Timing and control unit.** Generates the clock-synchronised control signals (ALE, RD, WR, IO/M, S0, S1) for the memory and I/O devices and manages the machine cycles.
10. **Interrupt control.** Five hardware interrupts: TRAP, RST 7.5, RST 6.5, RST 5.5, INTR (with INTA).
11. **Serial I/O control.** SID (serial input data) and SOD (serial output data) pins, used with the RIM and SIM instructions.
12. **Address buffer and address / data buffer.** Drive A15-A8 and the multiplexed AD7-AD0 pins; the address / data buffer is tri-stated (high impedance) during HOLD.
13. **Incrementer / decrementer address latch.** Increments or decrements PC, SP and the register pairs (INX, DCX) without using the ALU.

@s 3
**Method.** The 8085 has no multiply instruction, so the product is found by **repeated addition**: the multiplicand is added to a 16-bit sum as many times as the multiplier says. HL is used as the 16-bit accumulator (`DAD D` adds DE to HL), DE holds the multiplicand (16 bit, high byte 0) and C is the counter. $2050\text{H}\times2051\text{H}$ is at most $FFH\times FFH=FE01H$, which fits in 16 bits.

```asm
        LDA   2050H       ; A = multiplicand
        MOV   E, A
        MVI   D, 00H      ; DE = multiplicand (16 bit)
        LDA   2051H       ; A = multiplier
        MOV   C, A        ; C = counter
        LXI   H, 0000H    ; HL = product = 0
        MOV   A, C
        ORA   A           ; multiplier = 0 ?
        JZ    DONE        ; yes: product = 0
LOOP:   DAD   D           ; HL = HL + DE
        DCR   C
        JNZ   LOOP        ; repeat multiplier times
DONE:   SHLD  2052H       ; [2052H] = L (low byte), [2053H] = H (high byte)
        HLT
```

*Check (program run on an 8085 simulator).* $FFH\times FFH$ gives FE01H ([2052H] = 01H, [2053H] = FEH); $12\text{H}\times0\text{AH}$ gives 00B4H ($18\times10=180$); $A5\text{H}\times3C\text{H}$ gives 26ACH ($165\times60=9900$); a zero multiplicand or multiplier gives 0000H. All five test cases matched $a\times b$ exactly. The 16-bit result is stored with the low byte at 2052H and the high byte at 2053H.

*Example.* $2050\text{H}=05\text{H}$, $2051\text{H}=03\text{H}$: HL $=0005\to000A\to000F$ after 3 additions, so [2052H] = 0FH and [2053H] = 00H ($5\times3=15$).

@s 4
**Addressing mode:** the method by which an instruction specifies the location of its operand(s). The 8086 has the following modes (assume DS = 2000H, BX = 0100H, SI = 0010H, DI = 0020H, BP = 0200H).

| Mode | Operand location | Example | Effect |
|---|---|---|---|
| **Register** | in a register | `MOV AX, BX` | AX $\leftarrow$ BX |
| **Immediate** | in the instruction | `MOV AL, 5AH` | AL $\leftarrow$ 5AH |
| **Direct** | offset is a constant in the instruction | `MOV AX, [2050H]` | AX $\leftarrow$ word at 20000H + 2050H = 22050H |
| **Register indirect** | offset in BX, SI, DI (or BP) | `MOV AL, [BX]` | AL $\leftarrow$ byte at 20000H + 0100H = 20100H |
| **Based** | offset = BX or BP + displacement | `MOV AX, [BX+08H]` | AX $\leftarrow$ word at 20108H |
| **Indexed** | offset = SI or DI + displacement | `MOV AX, [SI+04H]` | AX $\leftarrow$ word at 20014H (array access) |
| **Based indexed** | offset = base (BX / BP) + index (SI / DI) [+ displacement] | `MOV AX, [BX+SI+02H]` | AX $\leftarrow$ word at 20000H + 0100H + 0010H + 2 = 20112H |
| **String** | implicit DS:SI (source), ES:DI (destination) | `MOVSB` | [ES:DI] $\leftarrow$ [DS:SI], then SI, DI step by $\pm1$ |
| **I/O port (direct / indirect)** | 8-bit port number or DX | `IN AL, 80H`; `OUT DX, AL` | port transfer |
| **Relative** | IP + signed 8 / 16 bit displacement (jumps, calls) | `JNZ LABEL` | IP $\leftarrow$ IP + disp |
| **Implied** | operand fixed by the opcode | `CLC`; `STD`; `CBW` | carry flag cleared, ... |

@s 5
**Method.** $n!=n(n-1)\cdots2\cdot1$ and $0!=1$. The number is read from the memory location 2050H (offset in DS) into CX, AX is initialised to 1 and `MUL CX` multiplies AX by CX in a loop that counts CX down to 1. With a 16-bit result the largest number that can be handled is $8!=40320$ (FFFFH = 65535; $9!=362880$ overflows). The factorial is stored at 2051H-2052H and is also **displayed** in decimal by repeated division by 10 (the remainders are pushed and popped to reverse their order).

```asm
        .MODEL SMALL
        .STACK 100H
        .DATA
MSG     DB  0DH, 0AH, 'Factorial = $'
        .CODE
MAIN    PROC
        MOV  AX, @DATA
        MOV  DS, AX
        MOV  BYTE PTR DS:[2050H], 5   ; test value (the given number n)
        MOV  SI, 2050H           ; SI -> location 2050H
        MOV  CL, [SI]            ; CL = n
        MOV  CH, 00H             ; CX = n
        MOV  AX, 0001H           ; result = 1
        JCXZ STORE               ; 0! = 1
FACT:   MUL  CX                  ; DX:AX = AX x CX
        LOOP FACT                ; CX = CX - 1, repeat while CX <> 0
STORE:  MOV  [SI+1], AX          ; store result at 2051H (low) - 2052H (high)
        ; ---- display AX in decimal ----
        LEA  DX, MSG
        PUSH AX
        MOV  AH, 09H
        INT  21H
        POP  AX
        MOV  BX, 10
        MOV  CX, 0
DIVL:   MOV  DX, 0
        DIV  BX                  ; AX = AX / 10, DX = remainder digit
        PUSH DX
        INC  CX
        CMP  AX, 0
        JNE  DIVL
SHOW:   POP  DX
        ADD  DL, 30H             ; to ASCII
        MOV  AH, 02H
        INT  21H
        LOOP SHOW
        MOV  AH, 4CH
        INT  21H
MAIN    ENDP
        END  MAIN
```

*Trace for n = 5.* CX = 5, AX = 1; MUL: AX = 5, CX = 4; AX = 20, CX = 3; AX = 60, CX = 2; AX = 120, CX = 1; AX = 120 x 1 = 120, CX = 0, loop ends. The result 0078H (120) is stored at 2051H (78H) and 2052H (00H), and `Factorial = 120` appears. Values $n=0,1,2,3,4,5,6,7,8$ give $1,1,2,6,24,120,720,5040,40320$.

@s 6
The **8257** is a programmable, **4-channel DMA (direct memory access) controller**. **DMA** transfers a block of data directly between an I/O device and memory **without the CPU** (the 8257 takes over the buses), so the transfer speed is limited only by the memory speed and no instruction fetch is needed for each byte.

```figure caption="Block diagram of the 8257 DMA controller: four channels with address and terminal-count registers, a priority resolver, read/write and control logic, and the data bus buffer. DRQ/DACK pins serve the I/O devices, HRQ/HLDA the CPU."
import numpy as _np, matplotlib.patches as mp
def box(ax,x,y,w,h,t,fc="white",ec=INK,fs=8,lw=1.2,ls="-"):
    ax.add_patch(mp.FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",fc=fc,ec=ec,lw=lw,ls=ls,zorder=3))
    ax.text(x,y,t,ha="center",va="center",fontsize=fs,zorder=4)
def arr(ax,a,b,c=None,rad=0.0,lw=1.2,sa=0,sb=0,style="-|>"):
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle=style,color=c or ACCENT,lw=lw,shrinkA=sa,shrinkB=sb,connectionstyle="arc3,rad=%s"%rad),zorder=2)
BLUE="#eaf3ff"; YEL="#fff4d6"; GRN="#e6f4ea"; RED="#fde8e8"
fig,ax=plt.subplots(figsize=(7.4,4.8)); ax.axis("off"); ax.set_xlim(0,14.8); ax.set_ylim(0,9.8)
ax.add_patch(mp.Rectangle((3.4,0.4),8.0,9.0,fc="#fafcff",ec=INK,lw=1.4)); ax.text(7.4,9.05,"Intel 8257 DMA controller",ha="center",fontsize=9,weight="bold")
box(ax,5.1,7.9,3.0,0.9,"Data bus buffer",fs=7.5,fc=BLUE); box(ax,5.1,6.4,3.0,1.0,"Read / write logic",fs=7.5,fc=RED); box(ax,5.1,4.5,3.0,1.6,"Control logic\n(mode set register,\nstatus register)",fs=7,fc=YEL)
box(ax,5.1,2.2,3.0,1.2,"Priority resolver",fs=7.5,fc=RED)
for i in range(4): box(ax,9.4,8.0-i*1.35,3.2,1.0,"Channel %d\nDMA address reg. (16)\nterminal count reg. (16)"%i,fs=5.9,fc=GRN)
for y,t in [(7.9,"D0 - D7"),(6.9,"IOR, IOW"),(6.0,"A0 - A3, CS"),(5.1,"RESET, CLK"),(4.2,"HRQ / HLDA"),(3.3,"READY"),(2.0,"DRQ0-3 in"),(1.2,"DACK0-3 out")]:
    ax.text(0.1,y,t,fontsize=7,va="center"); arr(ax,(1.9,y),(3.6,y),c=INK,style="<|-|>" if t.startswith("D0") else "-|>")
for y,t in [(8.0,"A0 - A7, A8 - A15"),(6.5,"MEMR, MEMW"),(5.0,"AEN, ADSTB"),(3.5,"TC, MARK")]:
    ax.text(14.7,y,t,fontsize=7,va="center",ha="right"); arr(ax,(11.5,y),(12.0,y),c=INK) if False else None
ax.text(7.4,0.7,"4 channels: 16-bit address + 14-bit count with 2 mode bits each",fontsize=6.5,ha="center",color="#555")
```


**Features and blocks.**

- Four independent channels (DRQ0-3 inputs, DACK0-3 outputs); each has a 16-bit **DMA address register** and a 14-bit **terminal count register** (plus 2 bits that choose read, write or verify), so a block of up to 16 KB can be moved.
- **Priority resolver:** fixed priority (channel 0 highest) or rotating priority.
- **Mode set register** (8 bit): enables the channels (EN0-EN3), rotating priority, extended write, TC stop and auto-load (channel 2 re-load from channel 3). **Status register:** terminal count flags TC0-TC3 and the update flag.
- **Data bus buffer** (D0-D7), **read / write logic** (IOR, IOW, and in the master mode MEMR, MEMW), **control logic** (HRQ, HLDA, READY, AEN, ADSTB, TC, MARK).
- **Slave mode** (the CPU programs the registers through A0-A3, $\overline{CS}$, $\overline{IOW}$) and **master mode** (the 8257 supplies A0-A15 and the memory and I/O control signals).

**Working.** (1) The peripheral raises DRQn. (2) The 8257 asks for the buses by HRQ; (3) the CPU completes the current machine cycle and answers with HLDA, floating its buses. (4) The 8257 sends DACKn to the device and places the memory address on A0-A15 (A0-A7 are latched with ADSTB); MEMR and IOW (or MEMW and IOR) move one byte. (5) The address register is incremented and the count is decremented; at terminal count TC is activated and the transfer stops. (6) HRQ is removed and the CPU continues. Transfer modes: single, block and demand.

@s 7
**Step 1: sizes.** The 4K x 8 EPROM has $2^{12}$ bytes: it needs 12 lines (A0-A11). Each 2K x 8 RAM has $2^{11}$ bytes: 11 lines (A0-A10). The starting address is not given, so the chips are assigned consecutively from 0000H.

| Chip | Start | End | A15 A14 | A13 | A12 | A11 | Lines to chip |
|---|---|---|---|---|---|---|---|
| EPROM 4 KB | 0000H | 0FFFH | 0 0 | 0 | 0 | x | A0-A11 |
| RAM 1 (2 KB) | 1000H | 17FFH | 0 0 | 0 | 1 | 0 | A0-A10 |
| RAM 2 (2 KB) | 1800H | 1FFFH | 0 0 | 0 | 1 | 1 | A0-A10 |

**Step 2: decoder.** A 74LS138 with $C=A_{13}$, $B=A_{12}$, $A=A_{11}$. Enables: G1 $=\overline{A_{15}+A_{14}}$ (2-input NOR, high when A15 = A14 = 0), G2A = IO/M (0 for memory), G2B = GND.

- $CBA=000$ and $001$ ($\overline{Y_0}$, $\overline{Y_1}$): 0000H-07FFH and 0800H-0FFFH, which together form the 4 KB EPROM, so $\overline{CS}_{EPROM}=\overline{Y_0}\cdot\overline{Y_1}$ (AND gate);
- $CBA=010$ ($\overline{Y_2}$): 1000H-17FFH: **RAM 1**;
- $CBA=011$ ($\overline{Y_3}$): 1800H-1FFFH: **RAM 2**.

```figure caption="Address decoding with a 74LS138: the AND of Y0 and Y1 selects the 4 KB EPROM (0000H-0FFFH), Y2 selects RAM 1 (1000H-17FFH) and Y3 selects RAM 2 (1800H-1FFFH)."
import numpy as _np, matplotlib.patches as mp
def box(ax,x,y,w,h,t,fc="white",ec=INK,fs=8,lw=1.2,ls="-"):
    ax.add_patch(mp.FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",fc=fc,ec=ec,lw=lw,ls=ls,zorder=3))
    ax.text(x,y,t,ha="center",va="center",fontsize=fs,zorder=4)
def arr(ax,a,b,c=None,rad=0.0,lw=1.2,sa=0,sb=0,style="-|>"):
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle=style,color=c or ACCENT,lw=lw,shrinkA=sa,shrinkB=sb,connectionstyle="arc3,rad=%s"%rad),zorder=2)
BLUE="#eaf3ff"; YEL="#fff4d6"; GRN="#e6f4ea"; RED="#fde8e8"
TITLE='Address decoding: 4K x 8 EPROM and 2 x 2K x 8 RAM (start 0000H)'; SEL=[('C', 'A13'), ('B', 'A12'), ('A', 'A11')]; ENAB='G1 = NOR(A15, A14)   G2A = IO/M   G2B = GND'; CHIPS=[('EPROM', '4K x 8', '0000H - 0FFFH', [0, 1], 'A0-A11, D0-D7, RD'), ('RAM 1', '2K x 8', '1000H - 17FFH', [2], 'A0-A10, D0-D7, RD, WR'), ('RAM 2', '2K x 8', '1800H - 1FFFH', [3], 'A0-A10, D0-D7, RD, WR')]
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


The AD7-AD0 lines are demultiplexed with the 74LS373 latch (ALE). The EPROM output enable is $\overline{RD}$; the RAMs use $\overline{RD}$ and $\overline{WR}$ (so the memory is read or written only when IO/M = 0). The D0-D7 pins of all chips are common and the decoder outputs $Y_4$-$Y_7$ stay free for further memory.

@s 8
| Basis | Memory-mapped I/O | I/O-mapped (isolated, standard) I/O |
|---|---|---|
| Address space | I/O devices share the 64 KB memory address space; they look like memory locations | separate I/O address space of 256 ports (8-bit port address) |
| Address lines | all 16 lines A15-A0 are decoded | only 8 lines A7-A0 are decoded |
| Instructions | any memory-reference instruction (MOV A, M; LDA; STA; ADD M; arithmetic and logic on I/O data) | only `IN` and `OUT` (data through the accumulator) |
| Control signals | MEMR and MEMW (IO/M = 0) | IOR and IOW (IO/M = 1) |
| Number of devices | many (up to 64 K minus memory) | limited to 256 input and 256 output ports |
| Memory space | reduces the memory available | full 64 KB for memory |
| Decoder | 16-bit address decoding, more hardware | 8-bit address decoding, simpler |
| Speed | slower for I/O data (more bytes per instruction: 3 bytes) | faster (2 byte instructions) |

@s 9
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

@s 10
**Flynn's classification** (1966) groups computers by the number of **instruction streams** and **data streams** that are processed simultaneously.

```figure caption="Flynn's classification: CU = control unit (instruction stream), PU = processing unit, with one or many data streams from memory."
import numpy as _np, matplotlib.patches as mp
def box(ax,x,y,w,h,t,fc="white",ec=INK,fs=8,lw=1.2,ls="-"):
    ax.add_patch(mp.FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",fc=fc,ec=ec,lw=lw,ls=ls,zorder=3))
    ax.text(x,y,t,ha="center",va="center",fontsize=fs,zorder=4)
def arr(ax,a,b,c=None,rad=0.0,lw=1.2,sa=0,sb=0,style="-|>"):
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle=style,color=c or ACCENT,lw=lw,shrinkA=sa,shrinkB=sb,connectionstyle="arc3,rad=%s"%rad),zorder=2)
BLUE="#eaf3ff"; YEL="#fff4d6"; GRN="#e6f4ea"; RED="#fde8e8"
fig,ax=plt.subplots(1,4,figsize=(7.4,2.6))
def panel(a,title,ncu,npu,nds,desc):
    a.set_xlim(0,6); a.set_ylim(0,6); a.axis("off"); a.set_title(title,fontsize=8)
    for i in range(ncu):
        y=5.0-i*(3.3/max(ncu,1)) if ncu>1 else 4.6
        a.add_patch(mp.Rectangle((0.2,y-0.35),1.1,0.7,fc="#fde8e8",ec=INK,lw=1)); a.text(0.75,y,"CU",ha="center",va="center",fontsize=6.5)
    for i in range(npu):
        y=5.0-i*(3.3/max(npu,1)) if npu>1 else 4.6
        a.add_patch(mp.Rectangle((2.3,y-0.35),1.1,0.7,fc="#fff4d6",ec=INK,lw=1)); a.text(2.85,y,"PU",ha="center",va="center",fontsize=6.5)
    if ncu==1 and npu>1:
        for i in range(npu):
            y=5.0-i*(3.3/npu); a.plot([1.3,2.3],[4.6,y],color=ACCENT,lw=0.9)
    elif ncu==npu:
        for i in range(ncu):
            y=5.0-i*(3.3/max(ncu,1)) if ncu>1 else 4.6; a.plot([1.3,2.3],[y,y],color=ACCENT,lw=0.9)
    else:
        for i in range(ncu):
            y=5.0-i*(3.3/ncu); a.plot([1.3,2.3],[y,4.6],color=ACCENT,lw=0.9)
    a.add_patch(mp.Rectangle((4.4,0.9),1.3,3.9,fc="#e6f4ea",ec=INK,lw=1)); a.text(5.05,2.85,"Memory\n(data)",ha="center",va="center",fontsize=6.3)
    for i in range(npu):
        y=5.0-i*(3.3/max(npu,1)) if npu>1 else 4.6; a.plot([3.4,4.4],[y,min(max(y,1.2),4.5)],color="#555",lw=0.9)
    a.text(3.0,0.3,desc,ha="center",fontsize=6.2)
panel(ax[0],"SISD",1,1,1,"1 instr. stream\n1 data stream")
panel(ax[1],"SIMD",1,3,3,"1 instr. stream\nmany data streams")
panel(ax[2],"MISD",3,1,1,"many instr. streams\n1 data stream")
panel(ax[3],"MIMD",3,3,3,"many instr. streams\nmany data streams")
plt.tight_layout()
```


| Class | Description | Example |
|---|---|---|
| **SISD** (single instruction, single data) | one control unit, one processing unit; instructions are executed one after another on one data item (the conventional von Neumann computer) | classic uniprocessor PC, 8085 / 8086 |
| **SIMD** (single instruction, multiple data) | one control unit broadcasts the same instruction to many processing elements, each working on its own data; ideal for vectors and matrices | array / vector processors, GPUs, MMX / SSE / AVX |
| **MISD** (multiple instruction, single data) | many processing units apply different instructions to the same data stream (rare, mostly theoretical; used in fault-tolerant systems) | systolic arrays, space-shuttle flight control computers |
| **MIMD** (multiple instruction, multiple data) | many processors, each with its own instructions and data; the most general and common parallel architecture; *tightly coupled* (shared memory, multiprocessors) or *loosely coupled* (distributed memory, clusters) | multi-core CPUs, supercomputers, computer clusters |
