---
subject: Microprocessor and Computer Architecture
grade: BCA Semester 2
unit: 5
title: Central Processing Unit and Computer Arithmetic
area: BCA 152 · Microprocessor and Computer Architecture · Unit 5
---

The CPU is the part that runs programs. This unit covers how a general CPU organises its registers and stack, how instructions are formatted and addressed, the families of instructions, program control and interrupts, the RISC/CISC debate, and the arithmetic the ALU performs — including Booth's multiplication, division and floating point.

::: key What this unit gives you
- General register organisation and the control word; stack organisation.
- Instruction formats (zero-, one-, two-, three-address) and addressing modes.
- Data-transfer, arithmetic, logic and shift instructions; program control, status bits, subroutines, interrupts.
- RISC versus CISC.
- Computer arithmetic: signed addition and subtraction, overflow, Booth's algorithm, restoring division, IEEE 754 floating point.
:::

## 5.1 General register organisation

A CPU with several registers avoids slow memory accesses. In the textbook design, **seven registers R1–R7** feed two multiplexers (MUX A and MUX B) which select the two ALU operands; the ALU output goes back through a decoder to the destination register.

```
  R1 … R7 ──► MUX A ─┐
                     ├──► ALU ──► (result) ──► destination register (via decoder)
  R1 … R7 ──► MUX B ─┘            OPR selects the operation
```

A **control word** specifies one micro-operation by selecting the three register fields and the operation:

| Field | Bits | Chooses |
|---|---|---|
| **SELA** | 3 | source register for ALU input A (000 = external input) |
| **SELB** | 3 | source register for ALU input B |
| **SELD** | 3 | destination register to load (000 = none) |
| **OPR** | 5 | the ALU operation |

| OPR | Operation | Symbol |
|---|---|---|
| 00000 | transfer A | TSFA |
| 00001 | increment A | INCA |
| 00010 | A + B | ADD |
| 00101 | A − B | SUB |
| 00110 | decrement A | DECA |
| 01000 | A ∧ B | AND |
| 01010 | A ∨ B | OR |
| 01100 | A ⊕ B | XOR |
| 01110 | complement A | COMA |
| 10000 | shift right A | SHRA |
| 11000 | shift left A | SHLA |

::: example Worked example: R1 ← R2 + R3
SELA = 010 (R2), SELB = 011 (R3), SELD = 001 (R1), OPR = 00010 (ADD): the 14-bit control word is `010 011 001 00010`. After one clock the sum sits in R1. A whole instruction is a sequence of such control words.
:::

## 5.2 Stack organisation

A **stack** is a LIFO store. A **register stack** uses a bank of registers with a **stack pointer SP**; a **memory stack** uses a region of RAM with SP in a CPU register (as on the 8085). Push and pop (memory stack growing toward lower addresses):

```
PUSH:  SP ← SP − 1 ;  M[SP] ← DR
POP :  DR ← M[SP] ;  SP ← SP + 1
```

A register stack adds **FULL** and **EMPTY** flags (stack-overflow and underflow checks) and works on `SP ← SP ± 1` with a 6-bit pointer for 64 words. Stacks matter for **subroutine calls**, **interrupts** (saving PC), **expression evaluation** and **recursion**.

### Reverse Polish notation

Stack machines evaluate **postfix** expressions with no brackets or precedence rules: `A * B + C * D` becomes `A B * C D * +`. Evaluate left to right: push operands; on an operator, pop two, apply, push the result.

::: example Worked example: evaluating (3 + 4) × (6 − 2)
Postfix: `3 4 + 6 2 − ×`. Push 3, push 4; `+` → pop 4, 3 → push 7. Push 6, push 2; `−` → pop 2, 6 → push 4. `×` → pop 4, 7 → push **28**. A stack-organised CPU gets zero-address instructions: `PUSH 3, PUSH 4, ADD, PUSH 6, PUSH 2, SUB, MUL`.
:::

## 5.3 Instruction formats

An instruction has an **opcode field**, one or more **operand/address fields** and a **mode field**. The number of addresses determines the style:

| Format | Example: X = (A + B) × (C + D) | Notes |
|---|---|---|
| **Three-address** | `ADD R1,A,B` · `ADD R2,C,D` · `MUL X,R1,R2` | shortest programs, long instructions |
| **Two-address** | `MOV R1,A` · `ADD R1,B` · `MOV R2,C` · `ADD R2,D` · `MUL R1,R2` · `MOV X,R1` | most common (x86-style); destination also a source |
| **One-address** | `LOAD A` · `ADD B` · `STORE T` · `LOAD C` · `ADD D` · `MUL T` · `STORE X` | accumulator machines (8085, basic computer) |
| **Zero-address** | `PUSH A, PUSH B, ADD, PUSH C, PUSH D, ADD, MUL, POP X` | stack machines |

More address fields ⇒ fewer instructions but more bits per instruction and more memory accesses per instruction.

## 5.4 Addressing modes

An **addressing mode** is the rule for finding an operand's **effective address (EA)** from the instruction's address field. Why modes exist: to give programmers pointers, loops over arrays, relocatable code and shorter instructions.

| Mode | Operand location / EA | Typical use |
|---|---|---|
| **Implied** | named by the opcode (accumulator, stack top) | `CMA`, zero-address stack ops |
| **Immediate** | the operand is in the instruction | constants (`MVI A,05H`) |
| **Register** | operand in a register | speed |
| **Register indirect** | EA = register contents | pointers (`MOV A,M`) |
| **Autoincrement / autodecrement** | register indirect, then register ± 1 | stepping through arrays, stack |
| **Direct (absolute)** | EA = address field | global variables |
| **Indirect** | EA = M[address field] | pointers in memory |
| **Relative** | EA = PC + address field | branches, position-independent code |
| **Indexed** | EA = index register + address field | array elements |
| **Base register** | EA = base register + address field | relocation of programs, segments |

::: example Worked example: effective addresses
Instruction at address 200, address field = 500, with PC = 201 (already incremented), index register XR = 100, R1 = 400, M[500] = 800, M[400] = 700, M[800] = 300.

| Mode | EA | Operand |
|---|---|---|
| Direct | 500 | M[500] = 800 |
| Immediate | — | 500 |
| Indirect | M[500] = 800 | M[800] = 300 |
| Relative | 201 + 500 = 701 | M[701] |
| Indexed | 500 + 100 = 600 | M[600] |
| Register | — | R1 = 400 |
| Register indirect | R1 = 400 | M[400] = 700 |
| Autoincrement | R1 = 400 (then R1 ← 401) | M[400] = 700 |
:::

## 5.5 Data transfer and manipulation

### Data-transfer instructions
Move data without changing it: **LOAD** (memory → register), **STORE** (register → memory), **MOVE** (register → register), **EXCHANGE**, **PUSH**, **POP**, **INPUT**, **OUTPUT**.

### Arithmetic instructions
**INC, DEC, ADD, SUB, MUL, DIV, ADDC (add with carry), SUBB (subtract with borrow), NEG** (two's complement).

### Logical and bit-manipulation instructions
**CLR, COM, AND, OR, XOR, CLRC, SETC, COMC** (carry), and bit tricks built from them:

- **Clear selected bits**: AND with a mask that has 0 in those positions (`1011 0110 AND 1111 0000 = 1011 0000`).
- **Set selected bits**: OR with a mask having 1s there.
- **Complement selected bits**: XOR with 1s there.

### Shift instructions

| Shift | Meaning | Fill |
|---|---|---|
| **Logical right/left** | slide all bits | 0 enters |
| **Arithmetic right** | divides a signed number by 2 | **sign bit is replicated** |
| **Arithmetic left** | multiplies by 2 | 0 enters; overflow if the sign changes |
| **Rotate** | circular | the bit that leaves re-enters |
| **Rotate through carry** | circular with carry as the 9th bit | CY enters |

Example: arithmetic right shift of 1110 0100 (−28) gives 1111 0010 (−14); a logical right shift would give 0111 0010 (+114).

## 5.6 Program control

**Program-control instructions** change the PC: `BR` (branch), `JMP`, conditional branches (`BZ`, `BNZ`, `BC`, `BNC`, `BP`, `BM`, `BV`), `CALL`, `RET`, compare and test (`CMP`, `TST`).

### Status bit conditions

The **status register (flags)** records ALU outcomes: **C** carry, **S** sign, **Z** zero, **V** overflow. Conditional branches test them. After comparing A and B (A − B):

| Condition | Test |
|---|---|
| A = B | Z = 1 |
| A ≠ B | Z = 0 |
| A > B (unsigned) | C = 0 and Z = 0 |
| A < B (unsigned) | C = 1 |
| A < B (signed) | S ⊕ V = 1 |
| A ≥ B (signed) | S ⊕ V = 0 |

### Subroutine call and return
`CALL` pushes the return address and loads the PC with the subroutine's address; `RET` pops it. The stack allows nested and recursive calls, unlike the basic computer's BSA (Unit 3).

### Program interrupt

An interrupt is a transfer of control forced by an event, not by the program. The CPU completes the current instruction, saves the PC and status on the stack, loads the service-routine address, and `RET`urns (`IRET`) afterwards.

| Type | Source | Examples |
|---|---|---|
| **External interrupt** | outside hardware | I/O device ready, timer, power failure, operator key |
| **Internal (trap)** | inside the CPU, caused by the running program | divide by zero, overflow, illegal opcode, protection violation, page fault |
| **Software interrupt** | a deliberate instruction | system calls (`INT`, `SVC`, `RST n`) |

Interrupts can be **vectored** (the device supplies the address) or **non-vectored** (fixed address), and prioritised (Unit 6).

## 5.7 RISC and CISC

| | **CISC** (complex instruction set) | **RISC** (reduced instruction set) |
|---|---|---|
| Instructions | many (100–300+), powerful, variable length | few (≈ 50–100), simple, **fixed length** |
| Cycles per instruction | many, varying | mostly **1 cycle** |
| Memory access | many instruction types access memory | only **LOAD and STORE** access memory (**load/store architecture**) |
| Addressing modes | many | few |
| Registers | few | **large register file** |
| Control unit | microprogrammed | **hardwired** |
| Pipelining | harder | easy and efficient |
| Compiler | simple (instructions close to HLL) | does more work |
| Code size | small | larger |
| Examples | VAX, Intel x86, Motorola 68000 | ARM, MIPS, RISC-V, SPARC, PowerPC |

Neither is simply "better": modern x86 chips translate CISC instructions into RISC-like micro-ops internally, and ARM dominates phones for power efficiency.

## 5.8 Computer arithmetic

### Signed integers and addition/subtraction

- **Sign-magnitude**: sign bit + magnitude; two zeros; awkward addition.
- **1's complement**: invert bits; two zeros.
- **2's complement** (used everywhere): −x = x′ + 1; single zero; range of n bits −2ⁿ⁻¹ … 2ⁿ⁻¹ − 1 (8 bits: −128 … 127). Add and subtract use the **same adder**: A − B = A + (B′ + 1).

**Overflow** (result outside the range) happens only when two numbers of the same sign give a result of the opposite sign. Detect it as **V = carry into the sign bit XOR carry out of the sign bit**. Example (8 bits): 0111 1111 + 0000 0001 = 1000 0000 (127 + 1 = −128): carry into MSB = 1, carry out = 0 ⇒ V = 1, overflow.

### Multiplication — shift-and-add

Multiply by adding the multiplicand once per 1-bit of the multiplier, shifted. Hardware keeps **A** (accumulator, initially 0), **Q** (multiplier), **M** (multiplicand) and a counter. For each bit of Q: if Q₀ = 1, A ← A + M; then shift A, Q right together. After n steps AQ holds the 2n-bit product (for unsigned numbers).

### Booth's algorithm (signed, two's complement)

Booth's method handles negative numbers without special cases and skips runs of 1s. It keeps an extra bit **Q₋₁** (initially 0) and looks at the pair **(Q₀, Q₋₁)** at each step:

| Q₀ Q₋₁ | Action before the shift |
|---|---|
| 00 or 11 | none |
| 10 (start of a run of 1s) | **A ← A − M** |
| 01 (end of a run of 1s) | **A ← A + M** |

Then **arithmetic shift right** the combined A, Q, Q₋₁ (the sign bit of A is kept). Repeat for n bits; the product is in AQ.

::: example Worked example: (−9) × (−13) with 5-bit Booth
M = −9 = 10111, Q = −13 = 10011, A = 00000, Q₋₁ = 0. (The values were generated and checked by the verifier script.)

| Step | Q₀Q₋₁ | Operation | A | Q | Q₋₁ |
|---|---|---|---|---|---|
| start | | | 00000 | 10011 | 0 |
| 1 | 10 | A ← A − M = 01001, shift | 00100 | 11001 | 1 |
| 2 | 11 | shift | 00010 | 01100 | 1 |
| 3 | 01 | A ← A + M = 11001, shift | 11100 | 10110 | 0 |
| 4 | 00 | shift | 11110 | 01011 | 0 |
| 5 | 10 | A ← A − M = 00111, shift | 00011 | 10101 | 1 |

Product = AQ = 00011 10101 = 0001110101₂ = **117**. ✔ ((−9) × (−13) = 117.)
:::

::: example Worked example: 7 × 3 with 4-bit Booth
M = 0111, Q = 0011, A = 0000, Q₋₁ = 0.

| Step | Q₀Q₋₁ | Operation | A | Q | Q₋₁ |
|---|---|---|---|---|---|
| 1 | 10 | A ← A − M = 1001, shift | 1100 | 1001 | 1 |
| 2 | 11 | shift | 1110 | 0100 | 1 |
| 3 | 01 | A ← A + M = 0101, shift | 0010 | 1010 | 0 |
| 4 | 00 | shift | 0001 | 0101 | 0 |

Product = 0001 0101₂ = **21** ✔ (verified by the script).
:::

### Division

**Restoring division** (unsigned): A = 0, Q = dividend, M = divisor. Repeat n times: shift A,Q left one bit; A ← A − M; if A < 0, **restore** (A ← A + M) and set Q₀ = 0, else set Q₀ = 1. At the end Q is the quotient and A the remainder. **Non-restoring** division avoids the restore step by adding M in the next cycle when A went negative.

::: example Worked example: 13 ÷ 3 (4 bits)
A = 0000, Q = 1101, M = 0011.

| Step | After shift | A − M | Action | A | Q |
|---|---|---|---|---|---|
| 1 | A = 0001 | negative | restore, q = 0 | 0001 | 1010 |
| 2 | A = 0011 | 0000 | q = 1 | 0000 | 0101 |
| 3 | A = 0000 | negative | restore, q = 0 | 0000 | 1010 |
| 4 | A = 0001 | negative | restore, q = 0 | 0001 | 0100 |

Quotient Q = 0100 = **4**, remainder A = 0001 = **1** ✔ (3 × 4 + 1 = 13).
:::

### Floating-point numbers (IEEE 754)

A floating-point number is ±1.f × 2ᵉ. **Single precision (32 bit)**: 1 sign bit, 8-bit **biased exponent** (bias 127), 23-bit fraction (the leading 1 is implicit). **Double precision (64 bit)**: 1 + 11 (bias 1023) + 52.

::: example Worked example: encoding 12.375
12.375 = 1100.011₂ = 1.100011 × 2³. Sign 0; exponent 3 + 127 = 130 = 10000010; fraction 10001100000000000000000. Hex **41460000**. Check: −5.75 = −101.11₂ = −1.0111 × 2² → sign 1, exponent 129 = 10000001, fraction 0111… ⇒ **C0B80000**. Decoding 3F400000: sign 0, exponent 01111110 = 126 → 2⁻¹, fraction .1 ⇒ 1.1₂ × 2⁻¹ = 1.5 × 0.5 = **0.75**. (All verified by script.)
:::

**Floating-point addition/subtraction** needs four steps: (1) **align** the exponents by shifting the smaller number's mantissa right; (2) **add or subtract** the mantissas; (3) **normalise** the result (shift so it is 1.f again, adjusting the exponent); (4) **round** and check for overflow/underflow. Example 0.5 + 0.375: 0.5 = 1.0 × 2⁻¹, 0.375 = 1.1 × 2⁻²; align: 0.11 × 2⁻¹; add: 1.0 + 0.11 = 1.11 × 2⁻¹ = **0.875**. **Multiplication**: multiply mantissas, add exponents (subtract one bias), normalise; **division**: divide mantissas, subtract exponents.

## Formula and fact sheet

- 2's complement: −x = x′ + 1; n-bit range −2ⁿ⁻¹ … 2ⁿ⁻¹ − 1; overflow V = C_in(MSB) ⊕ C_out(MSB).
- Booth: look at Q₀Q₋₁: 10 → A − M, 01 → A + M, 00/11 → shift only; arithmetic right shift; n steps.
- Restoring division: shift left, A − M, restore if negative, Q₀ = 1/0.
- IEEE single: value = (−1)ˢ × 1.f × 2^(e−127); double bias 1023.
- EA: indexed = base + index; relative = PC + offset; indirect = M[address].
- Instructions needed for X = (A+B)(C+D): 3-address 3, 2-address 6, 1-address 7, 0-address 8.

## Chapter summary

- A register-organised CPU selects ALU operands with two multiplexers and a control word SELA/SELB/SELD/OPR.
- A stack gives LIFO storage, supports calls and interrupts, and evaluates postfix expressions.
- Instruction formats range from three-address to zero-address; addressing modes locate operands flexibly.
- Program control uses flags C, S, Z, V; subroutine calls and interrupts save the return state on the stack.
- RISC: simple, fixed-length, load/store, hardwired, pipeline-friendly; CISC: complex, microprogrammed.
- The ALU adds/subtracts with 2's complement, multiplies with shift-and-add or Booth, divides by restoring/non-restoring, and handles reals as IEEE 754 floating point.

## Practice

1. Write the control word for R4 ← R5 − R6 in the seven-register CPU.
2. Convert A × B + C × D − E to postfix and evaluate it for A = 2, B = 3, C = 4, D = 5, E = 6.
3. Write programs for X = (A + B) × (C − D) in three-, two-, one- and zero-address styles.
4. Explain any six addressing modes with the effective address calculation.
5. Differentiate between RISC and CISC.
6. Perform (−6) × 5 with 5-bit Booth's algorithm.
7. Divide 13 by 3 by the restoring method (4 bits).
8. Represent −5.75 in IEEE 754 single precision.
9. Add 0110 0111 and 0101 1001 (8-bit two's complement) and detect overflow.
10. Distinguish external, internal and software interrupts with examples.

::: note Answers and worked solutions
**1.** SELA = 101 (R5), SELB = 110 (R6), SELD = 100 (R4), OPR = 00101 (SUB): `101 110 100 00101`.
**2.** `A B * C D * + E −`. 2·3 = 6; 4·5 = 20; 6 + 20 = 26; 26 − 6 = **20**.
**3.** 3-address: `SUB R1,C,D · ADD R2,A,B · MUL X,R2,R1`. 2-address: `MOV R1,A · ADD R1,B · MOV R2,C · SUB R2,D · MUL R1,R2 · MOV X,R1`. 1-address: `LOAD C · SUB D · STORE T · LOAD A · ADD B · MUL T · STORE X`. 0-address: `PUSH A · PUSH B · ADD · PUSH C · PUSH D · SUB · MUL · POP X`.
**4.** See the table in 5.4: e.g. indexed EA = XR + address field; relative EA = PC + offset; indirect EA = M[address]; register indirect EA = R.
**5.** See 5.7: RISC = few fixed-length, load/store, hardwired, big register file; CISC = many variable-length, microprogrammed.
**6.** M = −6 = 11010, Q = 5 = 00101. Following the Booth steps (Q₀Q₋₁ = 10 → A − M; 01 → A + M) gives AQ = 1111100010₂ = **−30** (checked by the verifier).
**7.** The table in 5.8 gives quotient 4, remainder 1.
**8.** −5.75 = −1.0111 × 2² → **C0B80000** (1 10000001 01110000000000000000000).
**9.** 0110 0111 (103) + 0101 1001 (89) = 1100 0000 (−64 as signed). Carry into MSB = 1, carry out = 0 ⇒ V = 1, **overflow** (the true sum 192 > 127).
**10.** External: I/O device ready, timer. Internal (trap): divide by zero, overflow, illegal opcode, page fault. Software: system call `INT n`, `RST n`.
:::
