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
{{B:vn}}

@s 2
{{B:addr85}}

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
{{B:arch86}}

**Flags in the 8086.**

{{B:flags86}}

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
{{B:ppi}}

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

{{FIG:decH}}

The latch 74LS373 (ALE) separates the low address byte. ROM and EPROM need only $\overline{RD}$ (output enable); the RAM needs $\overline{RD}$ and $\overline{WR}$. D0-D7 of all chips join the data bus.

@s 8
{{B:intr85}}

@s 9
{{B:risc}}

@s 10
{{B:accreg}}
