---
subject: Digital Logic
grade: BCA Semester 1
unit: 2
title: Number Systems, Binary Arithmetic and Codes
hours: 5
area: BCA 103 · Digital Logic · Unit 2
---

A computer stores everything (numbers, text, pictures) as groups of bits. This unit teaches how numbers are written in base 2, 8 and 16, how negative and fractional numbers are stored, how arithmetic works on them, and how codes (BCD, Gray, ASCII, parity, Hamming) represent and protect information.

::: key What this unit gives you
- Conversions between decimal, binary, octal and hexadecimal, including fractions.
- Signed numbers: sign-magnitude, 1's complement, 2's complement; overflow.
- Binary addition and subtraction using complements.
- IEEE-754 single-precision floating point.
- BCD, Excess-3, Gray, ASCII/Unicode, parity and the Hamming code.
:::

## 2.1 Positional number systems and conversions

A number in base *r* with digits dₙ…d₁d₀ . d₋₁d₋₂… has value Σ dᵢ × rⁱ.

| System | Base | Digits |
|---|---|---|
| Binary | 2 | 0, 1 |
| Octal | 8 | 0–7 |
| Decimal | 10 | 0–9 |
| Hexadecimal | 16 | 0–9, A(10), B(11), C(12), D(13), E(14), F(15) |

**To decimal**: multiply each digit by its place value and add. 1011.011₂ = 8 + 2 + 1 + 0.25 + 0.125 = **11.375**. 2F₁₆ = 2×16 + 15 = 47.

**From decimal, integer part**: divide repeatedly by the base; the remainders read **bottom to top** are the digits. For 156 → binary: 156 ÷ 2 = 78 r 0, 39 r 0, 19 r 1, 9 r 1, 4 r 1, 2 r 0, 1 r 0, 0 r 1 → **10011100₂**.

**From decimal, fractional part**: multiply repeatedly by the base; the integer parts read **top to bottom** are the digits. 0.625 × 2 = 1.25 → 1; 0.25 × 2 = 0.5 → 0; 0.5 × 2 = 1.0 → 1; so 0.625 = **0.101₂**. Some fractions never terminate: 0.1₁₀ = 0.000110011…₂, which is why 0.1 is inexact in a `float`.

**Binary ↔ octal ↔ hex by grouping.** Group bits in threes (octal) or fours (hex) from the binary point outwards, padding with zeros. 10011100₂ = 010 011 100 = **234₈**; = 1001 1100 = **9C₁₆**. 3A7₁₆ = 0011 1010 0111₂. Hex is the programmer's shorthand: 1 byte = 2 hex digits.

| Dec | Bin | Oct | Hex | | Dec | Bin | Oct | Hex |
|---|---|---|---|---|---|---|---|---|
| 0 | 0000 | 0 | 0 | | 8 | 1000 | 10 | 8 |
| 1 | 0001 | 1 | 1 | | 9 | 1001 | 11 | 9 |
| 2 | 0010 | 2 | 2 | | 10 | 1010 | 12 | A |
| 3 | 0011 | 3 | 3 | | 11 | 1011 | 13 | B |
| 4 | 0100 | 4 | 4 | | 12 | 1100 | 14 | C |
| 5 | 0101 | 5 | 5 | | 13 | 1101 | 15 | D |
| 6 | 0110 | 6 | 6 | | 14 | 1110 | 16 | E |
| 7 | 0111 | 7 | 7 | | 15 | 1111 | 17 | F |

**Range**: n bits hold 2ⁿ patterns. Unsigned: 0 to 2ⁿ − 1 (8 bits: 0–255).

## 2.2 Binary arithmetic

Addition rules: 0+0 = 0, 0+1 = 1, 1+0 = 1, 1+1 = 10 (sum 0, carry 1), 1+1+1 = 11 (sum 1, carry 1). Example: 1011 + 0110 = 10001 (11 + 6 = 17). Multiplication is shift-and-add; division is shift-and-subtract.

**Complements.** For an n-digit number N in base r:

- **(r−1)'s complement** = (rⁿ − 1) − N. For binary this is the **1's complement**: flip every bit.
- **r's complement** = rⁿ − N = (r−1)'s complement + 1. In binary: the **2's complement**: flip every bit and add 1.

## 2.3 Signed numbers

| Scheme | −25 in 8 bits | Range (n bits) | Zeros | Notes |
|---|---|---|---|---|
| Sign-magnitude | 10011001 | −(2ⁿ⁻¹−1) … +(2ⁿ⁻¹−1) | two (+0, −0) | easy to read; awkward arithmetic |
| 1's complement | 11100110 | same | two | end-around carry needed |
| **2's complement** | **11100111** | −2ⁿ⁻¹ … 2ⁿ⁻¹−1 | one | used by every real CPU |

In 2's complement the most significant bit has weight −2ⁿ⁻¹. For 8 bits the range is −128 … +127 (one more negative than positive). To read a negative pattern, complement and add 1 again: 11100111 → 00011000 + 1 = 00011001 = 25.

**Subtraction with 2's complement**: A − B = A + (2's complement of B), ignoring the final carry out. For 45 − 29 in 8 bits: 45 = 00101101; 29 = 00011101; −29 = 11100011. Sum: 00101101 + 11100011 = 1 00010000; discard the carry: 00010000 = **16**. ✔

**Overflow** occurs when adding two numbers of the *same sign* gives a result of the *opposite* sign (equivalently, the carry into the sign bit differs from the carry out). 100 + 50 in 8 bits: 01100100 + 00110010 = 10010110 = −106, which is wrong, so overflow. Adding numbers of opposite sign can never overflow.

## 2.4 Floating-point (IEEE-754 single precision)

32 bits: 1 sign bit **S**, 8-bit exponent **E** (bias 127), 23-bit fraction **F**. For normal numbers value = (−1)ˢ × 1.F × 2^(E−127).

Encode 10.5: 10.5 = 1010.1₂ = 1.0101₂ × 2³. S = 0. E = 3 + 127 = 130 = 10000010. F = 0101 followed by zeros. Bits: 0 10000010 01010000000000000000000 = **0x41280000**. Special values: E = 0 with F = 0 is zero; E = 255 with F = 0 is ±infinity; E = 255 with F ≠ 0 is NaN. Double precision uses 11 exponent bits (bias 1023) and 52 fraction bits.

## 2.5 Binary codes

**BCD (8421).** Each decimal digit is written as its own 4-bit binary group: 259 = 0010 0101 1001. The patterns 1010–1111 are invalid. BCD wastes states but converts easily to a decimal display. In BCD addition, if a digit sum exceeds 9 (or carries out), add 0110 (6) to correct it.

**Excess-3** = BCD + 3, a self-complementing code: 47 → (4+3)(7+3) = 0111 1010.

**Gray code** changes only **one bit** between consecutive numbers, which prevents false readings in shaft encoders and K-maps. Binary → Gray: keep the MSB, then XOR each bit with the bit to its left: 1011 → 1, 1⊕0 = 1, 0⊕1 = 1, 1⊕1 = 0 → **1110**. Gray → binary: keep the MSB; each next binary bit = previous binary bit XOR current Gray bit.

| Dec | Binary | Gray | Excess-3 |
|---|---|---|---|
| 0 | 0000 | 0000 | 0011 |
| 1 | 0001 | 0001 | 0100 |
| 2 | 0010 | 0011 | 0101 |
| 3 | 0011 | 0010 | 0110 |
| 4 | 0100 | 0110 | 0111 |
| 5 | 0101 | 0111 | 1000 |

**Alphanumeric codes.** *ASCII* is a 7-bit code (128 characters): `'A'` = 65 = 1000001, `'a'` = 97, `'0'` = 48; control codes 0–31. Extended ASCII uses 8 bits. *Unicode* (UTF-8, UTF-16) covers every script including Devanagari (Nepali) with code points such as U+0905 अ.

**Error detection: parity.** Add one bit so the total number of 1s is even (even parity) or odd. It detects any odd number of bit errors but cannot locate or correct, and misses two-bit errors. Parity generators and checkers are XOR trees.

**Error correction: the Hamming (7,4) code.** Four data bits d₁d₂d₃d₄ are placed at positions 3, 5, 6, 7; parity bits p₁, p₂, p₄ sit at positions 1, 2, 4, each covering the positions whose index has that bit set (p₁: 1,3,5,7; p₂: 2,3,6,7; p₄: 4,5,6,7), with even parity. Data 1011 → p₁ = d₁⊕d₂⊕d₄ = 1⊕0⊕1 = 0; p₂ = d₁⊕d₃⊕d₄ = 1⊕1⊕1 = 1; p₄ = d₂⊕d₃⊕d₄ = 0⊕1⊕1 = 0. Codeword (positions 1–7) = **0110011**. At the receiver recompute the three parity checks; the 3-bit result (c₄c₂c₁) is the *position* of a single flipped bit (000 means no error). Minimum Hamming distance 3: detects two errors, corrects one.

## Formula and fact sheet

- Value = Σ dᵢ rⁱ. Integer to base r: repeated division (remainders upward). Fraction: repeated multiplication (integers downward).
- Binary → hex: groups of 4; → octal: groups of 3.
- 2's complement = invert + 1. Range −2ⁿ⁻¹ … 2ⁿ⁻¹ − 1. Subtract by adding the 2's complement.
- Overflow: same-sign operands, opposite-sign result.
- IEEE single: 1 + 8 + 23 bits, bias 127. Double: 1 + 11 + 52, bias 1023.
- Gray: g = b ⊕ (b >> 1). Excess-3 = BCD + 3. ASCII 'A' = 65, 'a' = 97, '0' = 48.
- Hamming (7,4): parity at 1, 2, 4; syndrome gives the error position.

## Chapter summary

- Any base converts through the place-value rule; hex and octal are compact binary.
- 2's complement lets one adder do addition and subtraction; watch for overflow.
- Floating-point splits a number into sign, biased exponent and fraction.
- Codes serve different goals: BCD for decimal displays, Gray for one-bit change, ASCII for text, parity and Hamming for error control.

## Practice

1. Convert 156₁₀ to binary, octal and hexadecimal.
2. Convert 1011.011₂ to decimal and 0.625₁₀ to binary.
3. Convert 3A7₁₆ to binary and to octal.
4. Write −25 in 8-bit sign-magnitude, 1's complement and 2's complement.
5. Compute 45 − 29 in 8-bit 2's complement and state the carry.
6. Add 01100100 and 00110010 (8-bit signed). Is there overflow? Why?
7. Encode 10.5 in IEEE-754 single precision (hex).
8. Write 259 in BCD and 47 in Excess-3.
9. Convert binary 1011 to Gray code.
10. Compute the Hamming (7,4) codeword for data 1011 and decode 0110111 (one error).

::: note Answers and worked solutions
**1.** 10011100₂ = 234₈ = 9C₁₆ (128 + 16 + 8 + 4 = 156).
**2.** 8 + 2 + 1 + 0.25 + 0.125 = 11.375; 0.625 = 0.101₂.
**3.** 3A7₁₆ = 0011 1010 0111₂; regrouped in threes from the right: 001 110 100 111 = 1647₈.
**4.** 25 = 00011001. Sign-magnitude 10011001; 1's complement 11100110; 2's complement 11100111.
**5.** 00101101 + 11100011 = 1 00010000: result 00010000 = 16 and the carry out of 1 is discarded.
**6.** Sum 10010110, which reads as −106 although 100 + 50 = 150. Overflow: two positive operands gave a negative result (150 is beyond +127).
**7.** 0x41280000 (S = 0, E = 10000010, F = 0101…).
**8.** 259 → 0010 0101 1001; 47 → 0111 1010 in Excess-3.
**9.** 1110.
**10.** Codeword 0110011. For the received word 0110111 the bits at positions 1–7 are 0, 1, 1, 0, 1, 1, 1. Check p₁ (positions 1, 3, 5, 7): 0⊕1⊕1⊕1 = 1. Check p₂ (positions 2, 3, 6, 7): 1⊕1⊕1⊕1 = 0. Check p₄ (positions 4, 5, 6, 7): 0⊕1⊕1⊕1 = 1. The syndrome c₄c₂c₁ = 101 = 5, so bit 5 is wrong. Flipping it gives 0110011, whose data bits (positions 3, 5, 6, 7) are 1011.
:::
