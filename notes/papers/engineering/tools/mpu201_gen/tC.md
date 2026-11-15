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

{{B:mpmc}}

**Bus organization of a microprocessor.**

{{B:mpsys}}

@s 2
{{B:flags85}}

@s 3
**MVI M, data** (opcode 36H, 2 bytes) loads the immediate byte into the memory location whose address is in the HL pair: $[HL]\leftarrow$ data. It needs **three machine cycles and 10 T-states**.

| Machine cycle | T-states | IO/M | What happens |
|---|---|---|---|
| 1. **Opcode fetch (M1)** | 4 | 0 (memory), S1 S0 = 1 1 | PC (PCH on A15-A8, PCL on AD7-AD0) is output, ALE = 1 in T1 latches PCL; $\overline{RD}$ low in T2-T3 reads the opcode 36H into the instruction register; PC is incremented; T4 decodes the opcode |
| 2. **Memory read (M2)** | 3 | 0, S1 S0 = 1 0 | address = PC; $\overline{RD}$ low in T2-T3 reads the second byte (the data) into a temporary register; PC is incremented |
| 3. **Memory write (M3)** | 3 | 0, S1 S0 = 0 1 | the address in HL (H on A15-A8, L on AD7-AD0, latched by ALE in T1) is output, the data from the temporary register is put on AD7-AD0 in T2 and $\overline{WR}$ goes low in T2-T3 to write the byte into memory |

{{FIG:mvim}}

At the start of every machine cycle ALE goes high for one T-state to latch the low address byte. IO/M stays low because only memory is accessed. RD is active only in M1 and M2; WR is active only in M3.

**Execution time.** Total states $=4+3+3=10$ T. One T-state is one clock period of the internal clock, $T=1/f$. For the clock frequency $f=3$ MHz,

$$T=\frac{1}{3\times10^{6}}=0.333\ \mu s,\qquad t=10\times0.333\ \mu s=\mathbf{3.33\ \mu s}.$$

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
{{B:arch86}}

@s 6
{{B:directives}}

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

{{FIG:decC}}

The low address byte is demultiplexed with a 74LS373 latch (ALE). The EPROMs are read-only (output enable = $\overline{RD}$); the RAM uses $\overline{RD}$ and $\overline{WR}$. The data lines D0-D7 of all chips go to the data bus.

@s 9
{{B:ppi}}

@s 10
{{B:intr85}}

@s 11
{{B:risc}}
