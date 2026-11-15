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

{{B:mpsys}}

*Working.* To execute a program the CPU puts the address of the next instruction on the address bus, the control bus carries the memory-read command, and the instruction comes back over the data bus. After decoding, the CPU reads or writes data in the same way (for memory or for an I/O device selected by IO/M). Address decoding logic converts the upper address lines into chip-select signals of the memory and interface chips.

@s 2
{{B:arch85}}

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
{{B:addr86}}

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
{{B:dma}}

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

{{FIG:decK}}

The AD7-AD0 lines are demultiplexed with the 74LS373 latch (ALE). The EPROM output enable is $\overline{RD}$; the RAMs use $\overline{RD}$ and $\overline{WR}$ (so the memory is read or written only when IO/M = 0). The D0-D7 pins of all chips are common and the decoder outputs $Y_4$-$Y_7$ stay free for further memory.

@s 8
{{B:memio}}

@s 9
{{B:intr85}}

@s 10
{{B:flynn}}
