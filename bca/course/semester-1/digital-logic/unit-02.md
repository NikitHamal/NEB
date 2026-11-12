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

```svgfig label="2.1" caption="Decimal to binary: repeated division by 2 for the integer part (remainders read upward) and repeated multiplication by 2 for the fraction (carries read downward). 156.6875 = 10011100.1011."
f = Fig(760, 270)
f.text(170, 16, "Integer 156: divide by 2", size=11, color=NAVY, bold=True)
q = 156; y = 34
for k in range(8):
    f.box(60, y, 90, 24, f"{q} ÷ 2 = {q // 2}", fill=SOFT, stroke="#cbd5e1", size=10.5)
    f.box(160, y, 70, 24, f"rem {q % 2}", fill="#d1fae5" if q % 2 else "#fee2e2", stroke=TEAL if q % 2 else RED, size=10.5, bold=True)
    q //= 2; y += 28
f.arrow([(250, 244), (250, 40)], color=AMBER, sw=2)
f.text(262, 140, "read\nupward", size=10, color=AMBER, bold=True, anchor="start")
f.text(560, 16, "Fraction 0.6875: multiply by 2", size=11, color=NAVY, bold=True)
v = 0.6875; y = 34
for k in range(4):
    r = v * 2; d = int(r)
    f.box(440, y, 130, 24, f"{v:.4f} × 2 = {r:.4f}", fill=SOFT, stroke="#cbd5e1", size=10.5)
    f.box(580, y, 70, 24, f"bit {d}", fill="#d1fae5" if d else "#fee2e2", stroke=TEAL if d else RED, size=10.5, bold=True)
    v = r - d; y += 28
f.arrow([(670, 40), (670, 140)], color=AMBER, sw=2)
f.text(682, 90, "read\ndownward", size=10, color=AMBER, bold=True, anchor="start")
f.box(440, 170, 300, 34, "156.6875  =  10011100.1011", fill=NAVY, stroke=NAVY, color="#ffffff", size=13, bold=True)
f.text(590, 226, "check: 128+16+8+4 = 156 and 0.5+0.125+0.0625 = 0.6875", size=9.5, color=SLATE)
```

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

```svgfig label="2.2" caption="The 4-bit two's complement ring. Counting up past 0111 (+7) wraps to 1000 (-8). The sign bit is the leftmost bit; negation is invert-and-add-1."
import math
f = Fig(760, 330)
cx, cy, R = 200, 165, 120
f.circle(cx, cy, R, fill="#ffffff", stroke="#cbd5e1", sw=1.5, label="")
for n in range(16):
    a = math.radians(-90 + n * 22.5); x, y = cx + R * math.cos(a), cy + R * math.sin(a)
    val = n if n < 8 else n - 16
    f.circle(x, y, 17, fill="#d1fae5" if val >= 0 else "#fee2e2", stroke=TEAL if val >= 0 else RED, label=f"{val:+d}" if val else "0", size=9.5, color=NAVY)
    lx, ly = cx + (R + 44) * math.cos(a), cy + (R + 44) * math.sin(a)
    f.text(lx, ly + 3, format(n, "04b"), size=8.5, color=SLATE, bold=True)
f.text(cx, cy - 6, "4-bit", size=11, color=NAVY, bold=True); f.text(cx, cy + 10, "two's complement", size=10, color=NAVY, bold=True)
f.box(440, 30, 300, 28, "Range of n bits: −2ⁿ⁻¹ to +2ⁿ⁻¹ − 1", fill=NAVY, stroke=NAVY, color="#ffffff", size=11.5, bold=True)
rows = [("Sign-magnitude", "−7 to +7", "two zeros"), ("One's complement", "−7 to +7", "two zeros"), ("Two's complement", "−8 to +7", "one zero")]
for i, (a, b, c) in enumerate(rows):
    y = 72 + i * 32
    f.box(440, y, 130, 26, a, fill=SOFT, stroke="#cbd5e1", size=10, bold=True); f.box(574, y, 80, 26, b, fill=SOFT, stroke="#cbd5e1", size=10); f.box(658, y, 82, 26, c, fill=SAND if i < 2 else "#d1fae5", stroke=AMBER if i < 2 else TEAL, size=10)
f.box(440, 190, 300, 100, "", fill=SOFT, stroke="#cbd5e1")
f.text(590, 212, "Example: −5 in 4 bits", size=11, color=NAVY, bold=True)
f.text(590, 236, "+5 = 0101", size=11, color=SLATE); f.text(590, 256, "invert → 1010,  add 1 → 1011", size=11, color=SLATE); f.text(590, 276, "1011 = −8 + 2 + 1 = −5  ✓", size=11, color=TEAL, bold=True)
```

## 2.4 Floating-point (IEEE-754 single precision)

32 bits: 1 sign bit **S**, 8-bit exponent **E** (bias 127), 23-bit fraction **F**. For normal numbers value = (−1)ˢ × 1.F × 2^(E−127).

Encode 10.5: 10.5 = 1010.1₂ = 1.0101₂ × 2³. S = 0. E = 3 + 127 = 130 = 10000010. F = 0101 followed by zeros. Bits: 0 10000010 01010000000000000000000 = **0x41280000**. Special values: E = 0 with F = 0 is zero; E = 255 with F = 0 is ±infinity; E = 255 with F ≠ 0 is NaN. Double precision uses 11 exponent bits (bias 1023) and 52 fraction bits.

```svgfig label="2.3" caption="IEEE-754 single precision: 1 sign bit, 8 exponent bits (bias 127) and 23 fraction bits. Worked example: 0.15625 = 1.01₂ × 2⁻³ is stored as 0x3E200000."
f = Fig(760, 250)
f.box(30, 40, 60, 40, "S", fill=RED, stroke=RED, color="#ffffff", size=14, bold=True)
f.box(90, 40, 240, 40, "Exponent (8 bits)", fill=AMBER, stroke=AMBER, color="#ffffff", size=13, bold=True)
f.box(330, 40, 400, 40, "Fraction / mantissa (23 bits)", fill=TEAL, stroke=TEAL, color="#ffffff", size=13, bold=True)
f.text(60, 30, "bit 31", size=9.5, color=SLATE); f.text(300, 30, "bits 30 – 23", size=9.5, color=SLATE); f.text(640, 30, "bits 22 – 0", size=9.5, color=SLATE)
f.box(30, 90, 60, 34, "0", fill="#fee2e2", stroke=RED, size=14, bold=True)
f.box(90, 90, 240, 34, "0 1 1 1 1 1 0 0", fill="#fef3c7", stroke=AMBER, size=14, bold=True)
f.box(330, 90, 400, 34, "0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0", fill="#ccfbf1", stroke=TEAL, size=11.5, bold=True)
f.text(60, 146, "+", size=11, color=RED, bold=True); f.text(210, 146, "124 − 127 = −3", size=11, color=AMBER, bold=True); f.text(530, 146, "1.01₂ (hidden leading 1) = 1.25", size=11, color=TEAL, bold=True)
f.box(30, 166, 700, 62, "", fill=SOFT, stroke="#cbd5e1")
f.text(380, 188, "value = (−1)ˢ × 1.fraction × 2^(exponent − 127)", size=12, color=NAVY, bold=True)
f.text(380, 210, "= (+1) × 1.25 × 2⁻³ = 0.15625   →   hex 3E 20 00 00", size=11.5, color=SLATE)
```

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

```photogrid label="2.1" cols="2" ratio="1.5" caption="Binary codes made visible. (a) A real LED display: each digit is driven by a BCD-to-seven-segment decoder such as the 7447. (b) The seven segments a-g; the BCD code 0101 lights a, c, d, f, g to show the digit 5."
@ photo id="bca103/seg7" cap="Seven-segment LED digits (the colon separates hours and minutes)"
fit 1.5
call 0.50 0.93 0.20 0.70 "One digit = 7 LED segments"
@ svg cap="Segments a-g and the BCD input for digit 5"
f = Fig(300, 200)
def seg(x, y, w, h, name, on):
    f.box(x, y, w, h, name, fill=RED if on else "#e5e7eb", stroke="#9ca3af", color="#ffffff" if on else SLATE, size=9, bold=True, r=4)
on = dict(a=1, b=0, c=1, d=1, e=0, f=1, g=1)
seg(70, 10, 70, 16, "a", on["a"]); seg(70, 86, 70, 16, "g", on["g"]); seg(70, 162, 70, 16, "d", on["d"])
seg(48, 32, 16, 50, "f", on["f"]); seg(146, 32, 16, 50, "b", on["b"]); seg(48, 108, 16, 50, "e", on["e"]); seg(146, 108, 16, 50, "c", on["c"])
f.text(235, 70, "BCD input", size=10, color=NAVY, bold=True); f.text(235, 92, "D C B A", size=11, color=SLATE, bold=True); f.text(235, 114, "0 1 0 1", size=14, color=TEAL, bold=True)
f.text(235, 140, "digit 5", size=10, color=NAVY, bold=True)
```
```photogrid label="2.2" cols="2" ratio="1.4" caption="Codes you could hold in your hand. (a) A Teletype Model 33, the machine on which the 7-bit ASCII code was first used widely in the 1960s. (b) Real punched paper tapes: each row of holes is one character, with the holes standing for the 1 bits of its code."
@ photo id="bca103/asr33" cap="Teletype Model 33: keyboard, printer and tape punch in one machine"
fit 1.4
focus 0.5 0.5
@ photo id="bca103/tape8" cap="Paper tape: a row of up to 8 holes per character, plus the small sprocket holes"
fit 1.4
focus 0.5 0.5
```

```svgfig label="2.4" caption="The word NEB as it would be punched on 8-level paper tape: seven ASCII bits plus an even-parity bit. Codes and parity were computed in code; a lost or extra hole makes the count of 1s odd, which exposes the error."
word = "NEB"
rows = []
for ch in word:
    c = ord(ch); ones = bin(c).count("1"); par = ones & 1
    rows.append((ch, c, par, (par << 7) | c))
assert [(r[0], r[1], r[2]) for r in rows] == [("N", 78, 0), ("E", 69, 1), ("B", 66, 0)]
assert all(bin(r[3]).count("1") % 2 == 0 for r in rows)
f = Fig(760, 250)
f.text(380, 16, "Eight-level tape: one row per character, holes = 1 (most significant bit at the top, parity bit P)", size=11, color=NAVY, bold=True)
f.text(40, 40, "P  b6 b5 b4 b3 b2 b1 b0", size=10.5, color=NAVY, bold=True, anchor="start")
f.text(300, 40, "Char   Code   1s   Parity bit", size=10.5, color=NAVY, bold=True, anchor="start")
for i, (ch, c, par, byte) in enumerate(rows):
    y = 56 + i * 56
    f.box(30, y, 230, 46, "", fill=SAND, stroke=AMBER, r=4)
    for k in range(8):
        v = (byte >> (7 - k)) & 1
        f.circle(46 + k * 28, y + 23, 9 if v else 3, fill="#1e293b" if v else "#cbd5e1", stroke="#1e293b", sw=1, label="")
    f.text(300, y + 23, f"'{ch}'   {c:>3} = {c:07b}   {bin(c).count('1')}   {par}", size=11, color=SLATE, bold=True, anchor="start", vmid=True)
f.box(520, 56, 224, 158, "", fill=BLUE, stroke=NAVY)
f.text(632, 78, "Even parity", size=11, color=NAVY, bold=True)
for j, t in enumerate(["Total number of 1 bits in each", "row is always even: N has 4,", "E has 3 + parity 1 = 4, B has 2.", "If a hole is missed, the row has", "an odd count and the reader", "knows the character is wrong."]):
    f.text(632, 102 + j * 18, t, size=10.5, color=SLATE)
```

```photogrid label="2.3" cols="2" ratio="1.3" caption="Why shaft encoders use Gray code. (a) A rotary encoder: a shaft position is read as a binary pattern from a coded disc. (b) For a 3-bit disc, the worst reading error while the disc moves from one sector to the next, if the bits do not all change at exactly the same instant, computed for every transition: plain binary can be off by 3 positions, Gray code by 0."
@ photo id="bca103/encoder" cap="Rotary encoder: the coded disc sits inside the case"
fit 1.3
focus 0.5 0.5
@ svg cap="Worst misread at each of the 8 sector boundaries"
def gray(n): return n ^ (n >> 1)
def ungray(g):
    n = 0
    while g: n ^= g; g >>= 1
    return n
def worst(code, dec, a, b):
    ca, cb = code(a), code(b); diff = ca ^ cb; bitsl = [i for i in range(3) if diff >> i & 1]; w = 0
    for m in range(1 << len(bitsl)):
        r = ca
        for j, bi in enumerate(bitsl):
            if m >> j & 1: r ^= 1 << bi
        v = dec(r); w = max(w, min(abs(v - a), abs(v - b)))
    return w
ident = lambda x: x
tr = [(i, (i + 1) % 8) for i in range(8)]
wb = [worst(ident, ident, a, b) for a, b in tr]; wg = [worst(gray, ungray, a, b) for a, b in tr]
assert max(wb) == 3 and max(wg) == 0 and wb[3] == 3 and wb[0] == 0
f = Fig(400, 300)
f.text(200, 16, "Worst error in sector positions", size=11, color=NAVY, bold=True)
for i, ((a, b), x, g) in enumerate(zip(tr, wb, wg)):
    y = 34 + i * 30
    f.text(10, y + 10, f"{a} to {b}", size=10, color=SLATE, bold=True, anchor="start", vmid=True)
    f.box(60, y, max(x * 60, 3), 11, "", fill=ROSE, stroke=RED, r=2); f.text(66 + x * 60, y + 6, f"binary {x}", size=9.5, color=RED, bold=True, anchor="start", vmid=True)
    f.box(60, y + 13, 3, 11, "", fill=MINT, stroke=TEAL, r=1); f.text(70, y + 19, f"Gray {g}", size=9.5, color=TEAL, bold=True, anchor="start", vmid=True)
f.text(200, 288, "3 to 4 changes all three bits (011 to 100).", size=10, color=SLATE)
```

```photogrid label="2.4" cols="2" ratio="1.4" caption="Decimal digits in hardware. (a) Nixie tubes, the glowing-digit displays of the 1960s calculators; each tube is driven by a BCD decoder that lights one of ten digits. (b) Bits needed to store the same number in BCD and in pure binary, computed for four values."
@ photo id="bca103/nixie" cap="Nixie tubes: one tube per decimal digit, driven from 4-bit BCD"
fit 1.4
focus 0.5 0.5
@ svg cap="BCD costs more bits than binary"
vals = [99, 2025, 9999999, 999999999]
bits = [(v, 4 * len(str(v)), v.bit_length()) for v in vals]
assert bits == [(99, 8, 7), (2025, 16, 11), (9999999, 28, 24), (999999999, 36, 30)]
assert format(2025, "04d") == "2025" and " ".join(f"{int(d):04b}" for d in "2025") == "0010 0000 0010 0101"
f = Fig(400, 290)
f.text(200, 16, "Bits needed", size=11, color=NAVY, bold=True)
for i, (v, b, n) in enumerate(bits):
    y = 36 + i * 56
    f.text(10, y + 8, f"{v:,}", size=11, color=NAVY, bold=True, anchor="start")
    f.box(10, y + 14, b / 36 * 300, 16, "", fill=SAND, stroke=AMBER, r=3); f.text(16 + b / 36 * 300, y + 22, f"BCD {b}", size=10, color=AMBER, bold=True, anchor="start", vmid=True)
    f.box(10, y + 33, n / 36 * 300, 16, "", fill=MINT, stroke=TEAL, r=3); f.text(16 + n / 36 * 300, y + 41, f"binary {n}", size=10, color=TEAL, bold=True, anchor="start", vmid=True)
f.text(200, 266, "2025 in BCD = 0010 0000 0010 0101 (16 bits); in binary 11111101001 (11 bits).", size=9.5, color=SLATE)
assert format(2025, "b") == "11111101001"
```

```photogrid label="2.5" cols="2" ratio="1.5" caption="A code that checks itself. (a) An EAN-13 barcode on a packet: the last digit is a check digit that lets the scanner detect a misread. (b) The check digit of the number printed under that barcode, 4620017455554, recalculated with alternating weights 1 and 3: the last digit must come out as 4."
@ photo id="bca103/ean13" cap="EAN-13 barcode: 12 data digits and 1 check digit"
fit 1.5
focus 0.5 0.5
@ svg cap="Check digit = (10 - weighted sum mod 10) mod 10"
d = [int(c) for c in "462001745555"]
wsum = sum(x * (1 if i % 2 == 0 else 3) for i, x in enumerate(d)); chk = (10 - wsum % 10) % 10
assert wsum == 86 and chk == 4
bad = d[:]; bad[5], bad[6] = bad[6], bad[5]
wb2 = sum(x * (1 if i % 2 == 0 else 3) for i, x in enumerate(bad)); chk2 = (10 - wb2 % 10) % 10
assert chk2 != chk
f = Fig(400, 270)
f.text(200, 16, "Barcode number 462001745555-?", size=11, color=NAVY, bold=True)
for i, x in enumerate(d):
    wgt = 1 if i % 2 == 0 else 3
    f.box(8 + i * 31, 30, 28, 28, str(x), fill=BLUE, stroke=NAVY, size=11, bold=True)
    f.text(22 + i * 31, 74, f"x{wgt}", size=10, color=AMBER, bold=True)
f.box(8 + 12 * 31, 30, 28, 28, "?", fill=MINT, stroke=TEAL, size=11, bold=True)
f.text(200, 108, f"Weighted sum = {wsum}", size=11, color=SLATE, bold=True)
f.text(200, 130, f"{wsum} mod 10 = {wsum % 10}, so check digit = 10 - {wsum % 10} = {chk}", size=11, color=SLATE, bold=True)
f.box(40, 150, 320, 52, "", fill=MINT, stroke=TEAL)
f.text(200, 168, f"Valid number: 4620017455554 (check digit {chk})", size=10.5, color=TEAL, bold=True)
f.text(200, 188, "A scanner repeats this sum and rejects a mismatch.", size=10.5, color=SLATE)
f.text(200, 222, f"Swap two neighbours ({d[5]} and {d[6]}): the check digit would be {chk2},", size=10, color=RED)
f.text(200, 240, f"not {chk}, so that mistake is caught.", size=10, color=RED)
```

```svgfig label="2.5" caption="Hamming (7,4) in action, simulated for the data 1011. A single flipped bit is located by the three parity checks and repaired; a double error is repaired wrongly. All 7 single errors and all 21 double errors were tried."
import itertools
def enc(d1, d2, d3, d4):
    p1, p2, p3 = d1 ^ d2 ^ d4, d1 ^ d3 ^ d4, d2 ^ d3 ^ d4
    return [p1, p2, d1, p3, d2, d3, d4]
def syn(c): return (c[0] ^ c[2] ^ c[4] ^ c[6]) | ((c[1] ^ c[2] ^ c[5] ^ c[6]) << 1) | ((c[3] ^ c[4] ^ c[5] ^ c[6]) << 2)
def fix(c):
    s = syn(c); c = c[:]
    if s: c[s - 1] ^= 1
    return c
cw = enc(1, 0, 1, 1)
assert "".join(map(str, cw)) == "0110011" and syn(cw) == 0
ok1 = 0
for i in range(7):
    r = cw[:]; r[i] ^= 1
    ok1 += fix(r) == cw
ok2 = 0
for i, j in itertools.combinations(range(7), 2):
    r = cw[:]; r[i] ^= 1; r[j] ^= 1
    ok2 += fix(r) == cw
assert ok1 == 7 and ok2 == 0
r = cw[:]; r[4] ^= 1
assert syn(r) == 5 and fix(r) == cw
f = Fig(760, 270)
f.text(380, 16, "Positions 1 to 7: p1 p2 d1 p3 d2 d3 d4   (parity bits at 1, 2 and 4)", size=11, color=NAVY, bold=True)
labels = ["p1", "p2", "d1", "p3", "d2", "d3", "d4"]
def row(y, bits, title, hl=None, col=NAVY, fl=BLUE):
    f.text(10, y + 15, title, size=10.5, color=col, bold=True, anchor="start", vmid=True)
    for k in range(7):
        h = hl == k
        f.box(210 + k * 46, y, 40, 30, str(bits[k]), fill=ROSE if h else fl, stroke=RED if h else col, size=12, bold=True)
for k, l in enumerate(labels): f.text(230 + k * 46, 46, l, size=10, color=SLATE, bold=True)
row(54, cw, "1. Sent codeword", None, TEAL, MINT)
row(94, r, "2. Received (position 5 flipped)", 4, RED, ROSE)
row(134, fix(r), "3. After correction", None, TEAL, MINT)
f.box(540, 54, 210, 110, "", fill=SAND, stroke=AMBER)
f.text(645, 76, "Syndrome s3 s2 s1 = 101", size=10.5, color=AMBER, bold=True)
for j, t in enumerate(["= 5 in binary, so the error", "is at position 5: flip it back.", "s1 checks 1,3,5,7; s2 checks 2,3,6,7;", "s3 checks 4,5,6,7."]):
    f.text(645, 98 + j * 16, t, size=10, color=SLATE)
f.text(380, 196, "Single errors repaired: 7 of 7.     Double errors repaired: 0 of 21 (they are 'fixed' to a wrong word).", size=11, color=NAVY, bold=True)
f.text(380, 218, "Minimum distance 3 can correct 1 error or detect 2, not both: an extra overall parity bit (SECDED) is used in ECC memory.", size=10.5, color=SLATE)
f.text(380, 238, "Server RAM in banks and data centres uses this idea so that a cosmic-ray bit flip does not corrupt a record.", size=10.5, color=SLATE)
```

## 2.6 Why computers use binary and codes: eight reasons

1. **Two states are easy to build.** A transistor is either off or on, and a capacitor either holds charge or does not. Building a reliable ten-level device would be far harder. This is why every chip, from a calculator to the Nepal Rastra Bank server, is built on two states.
2. **Two states are easy to read correctly.** With only two levels the receiver needs one threshold, so the noise margin is large. A signal that has drifted a little is still read right. Ten levels in the same 5 V range would leave only 0.5 V between levels.
3. **Boolean algebra fits binary exactly.** The AND, OR and NOT operations of Boolean algebra map directly onto 1 and 0. Every arithmetic or decision circuit can therefore be written as an equation and then simplified. This is the base of Unit 3.
4. **Arithmetic is simple.** Binary addition has only four cases, and with two's complement the same adder also subtracts. A CPU needs no separate subtractor. This saves silicon and power.
5. **Hexadecimal makes bits readable.** One hex digit stands for exactly four bits, so 1111 0000 becomes F0. Memory dumps, MAC addresses and colour codes such as #DC143C (crimson, the colour of the Nepali flag) are written in hex. Conversion needs no calculation.
6. **Codes carry meaning.** ASCII and Unicode map characters to numbers, so Nepali text in Devanagari can be stored as code points. BCD keeps decimal digits separate for calculators and meters. Gray code changes one bit at a time, which prevents errors in position encoders.
7. **Codes detect errors.** A parity bit added to a byte makes the count of 1s even (or odd), so any single flipped bit is noticed. CRC and Hamming codes go further. Mobile networks and memory chips use them all the time.
8. **Floating point covers a huge range.** IEEE-754 stores a number as sign, exponent and fraction, so one 32-bit word can hold values from about 10⁻³⁸ to 10³⁸. It is the format used in spreadsheets, games and scientific code. The price is limited precision, about seven decimal digits for single precision.

### 2.6.1 Eight codes you meet every day in Nepal

1. **Unicode and UTF-8.** Every letter of Devanagari, such as न (U+0928), has a code point, and UTF-8 stores it in 3 bytes. This is why a Nepali SMS or a Facebook post in Nepali shows correctly on any phone. Older fonts such as Preeti used ASCII codes and displayed garbage on other systems.
2. **ASCII.** English letters and digits use 7-bit ASCII, for example A = 65. Programs written in C, Java and Python use it for strings and file names. It began on teleprinters like the one in Plate 2.2.
3. **BCD.** The digits on a digital weighing scale, a petrol pump or an electricity meter are driven from BCD, one 4-bit group per decimal digit. BCD avoids rounding of decimal fractions, which matters for money. It costs more bits than binary (Plate 2.4).
4. **Gray code.** Rotary encoders in lifts, machine tools and mouse wheels use Gray code so that one step changes one bit only. This prevents wild misreadings at sector edges (Plate 2.3). Karnaugh maps also use the Gray order.
5. **Parity bit.** Serial lines and older memory use a parity bit so that a single flipped bit is noticed. The sender makes the number of 1s even and the receiver checks it (Figure 2.4). It cannot find two errors together.
6. **Hamming code.** ECC memory in servers, for example those running the banking systems of Kathmandu, corrects a single bit error by itself (Figure 2.5). The check bits are placed at the power-of-two positions. A flipped bit costs no data and no downtime.
7. **Barcodes.** The EAN-13 code on a packet of noodles carries 12 digits and a check digit, and the till looks up the price from it (Plate 2.5). A wrongly scanned digit fails the check and the scanner beeps again. Libraries use the same method for ISBN numbers.
8. **QR codes.** The Fonepay QR code on a shop counter holds the merchant data and uses Reed-Solomon error correction so that it can be read even when partly torn or dirty. It is a two-dimensional cousin of the barcode. The phone camera decodes it in a fraction of a second.

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

## Model answers: medium (5 marks) and long (10 marks) questions

**Q (5 marks). Explain subtraction using two's complement. Subtract 5 from 7 in 4-bit binary and state how overflow is detected.**

To compute A − B, a computer does not use a subtractor. It takes the **two's complement** of B and **adds** it to A, so a single adder circuit handles both operations. The two's complement of B is obtained in two steps: invert every bit of B (one's complement), then add 1. The reason is that −B = 2ⁿ − B in an n-bit system, and adding 2ⁿ only produces a carry that falls outside the word (Figure 2.2).

Worked example, 7 − 5 in 4 bits:

1. 7 = 0111 and 5 = 0101.
2. Invert 5: 1010. Add 1: 1011 (this is −5).
3. Add: 0111 + 1011 = 1 0010.
4. Discard the carry-out of the fourth bit. The result 0010 = **2**, which is correct.

If the carry-out is 1 and the answer is non-negative, it is discarded; if there is no carry-out, the answer is negative and is already in two's complement form. **Overflow** occurs when two numbers of the same sign are added and the result has the opposite sign, for example 0101 + 0100 = 1001 (5 + 4 gives −7 in 4 bits). Equivalently, overflow is flagged when the carry into the sign bit is different from the carry out of the sign bit. The range of an n-bit two's complement word is −2ⁿ⁻¹ to +2ⁿ⁻¹ − 1, so 4 bits cover −8 to +7.

**Q (5 marks). What is BCD? Add 27 and 38 in BCD, showing the correction step, and compare BCD with pure binary.**

**BCD (binary-coded decimal)** represents each decimal digit by its own 4-bit binary code (8-4-2-1 weights); only 0000 to 1001 are valid, and 1010 to 1111 are unused. So 27 is stored as 0010 0111 and not as 11011. This keeps decimal digits separate, which is why calculators, digital meters and the seven-segment display in Plate 2.1 use it: a 7447 decoder turns one BCD digit directly into the segment pattern.

**BCD addition, 27 + 38:**

| Step | Low digit | High digit |
|---|---|---|
| Operands | 0111 (7) + 1000 (8) | 0010 (2) + 0011 (3) |
| Binary sum | 1111 (15, invalid) | 0010 + 0011 + carry 1 = 0110 |
| Correction | add 0110 → 1 0101, carry 1 | no correction (0110 is valid) |
| Result digit | 0101 (5) | 0110 (6) |

The answer is 0110 0101 = **65**, which is correct. The rule: if a digit sum is greater than 9 or produces a carry, add 0110 (6) to skip the six unused codes.

| Point | BCD | Pure binary |
|---|---|---|
| Bits for 99 | 8 (1001 1001) | 7 (1100011) |
| Arithmetic | needs correction | direct |
| Conversion to display | trivial | needs a divider |
| Use | meters, clocks, finance | general computing |

**Q (10 marks). Explain the common binary codes (BCD, excess-3, Gray, ASCII) and error-detecting parity codes with examples. Compare them in a table.**

*Introduction.* A **code** is an agreed way to represent numbers, letters or positions as groups of bits. Choosing the right code makes circuits simpler or data safer. A digital system uses several codes at once: pure binary inside the ALU, ASCII or Unicode for text, BCD for a display and parity for transmission.

*1. BCD (8-4-2-1).* Each decimal digit has a 4-bit code, 0 to 9 as 0000 to 1001; 93 is 1001 0011. It is easy to display (Plate 2.1) but needs correction (+0110) in arithmetic.

*2. Excess-3.* The BCD code plus 3: digit 0 is 0011 and digit 9 is 1100. It is *self-complementing*, because inverting every bit of a code gives the code of the 9's complement (the code for 2 is 0101 and the code for 7 is 1010). This makes decimal subtraction simple in old machines.

*3. Gray code.* Successive values differ in exactly **one** bit: 000, 001, 011, 010, 110, 111, 101, 100. It is used in rotary position encoders and Karnaugh maps, because when a sensor passes from one position to the next only one bit can be wrong at a time. Binary to Gray: keep the first bit, then XOR each bit with the bit before it. For binary 1011, Gray = 1, 1⊕0, 0⊕1, 1⊕1 = **1110**. Gray to binary: keep the first bit, then XOR each Gray bit with the previous *binary* bit.

*4. ASCII and Unicode.* ASCII gives each character a 7-bit code: 'A' = 65 = 0x41 = 1000001, 'a' = 97 (differs from 'A' by bit 5, value 32), '0' = 48 = 0x30. Unicode (UTF-8) extends this to every script; the Devanagari letter 'न' is U+0928. A Nepali website and a phone message both rely on Unicode.

*5. Parity.* A parity bit is added so that the number of 1s is even (even parity) or odd. The data 1011001 has four 1s, so the even-parity bit is 0 and the odd-parity bit is 1. A receiver recounts the 1s; one flipped bit makes the parity wrong and the error is detected. Parity cannot detect two flipped bits and cannot locate the error; **Hamming codes** add several parity bits at positions 1, 2, 4, 8, ... so that they can both locate and correct a single-bit error.

*Comparison.*

| Code | Bits | Main property | Use |
|---|---|---|---|
| BCD | 4 per digit | decimal digits stay separate | clocks, meters, displays |
| Excess-3 | 4 per digit | self-complementing | old decimal arithmetic |
| Gray | n | one bit changes per step | encoders, K-maps |
| ASCII | 7 (8 with parity) | letters and symbols | text, files |
| Parity | data + 1 | detects odd number of errors | memory, serial links |

*Conclusion.* No single code is best. Each code trades extra bits or extra logic for convenience, speed or safety, and a designer picks the code that suits the job.

**Q (5 marks). What is Gray code? Convert binary 1011 to Gray code and state why it is used in shaft encoders.**

**Gray code** is a binary code in which two consecutive numbers differ in **exactly one bit**. It is also called a reflected binary code and is not a weighted code.

**Binary to Gray.** Keep the most significant bit; every other Gray bit is the XOR of the binary bit with the bit on its left. For 1011: G3 = 1; G2 = 1 ⊕ 0 = 1; G1 = 0 ⊕ 1 = 1; G0 = 1 ⊕ 1 = 0, so **Gray = 1110**. Back to binary: B3 = 1; B2 = 1 ⊕ 1 = 0; B1 = 0 ⊕ 1 = 1; B0 = 1 ⊕ 0 = 1, giving 1011 again.

| Decimal | Binary | Gray |
|---|---|---|
| 3 | 011 | 010 |
| 4 | 100 | 110 |
| 5 | 101 | 111 |

**Why in encoders.** In pure binary the step from 3 (011) to 4 (100) changes all three bits, and the sensors never switch at exactly the same instant, so the reader may see 111 (7) or 000 (0). Plate 2.3 computed the worst error as 3 positions for binary and 0 for Gray, because Gray changes one bit and so can only show the old or the new position. Uses: rotary encoders in lifts and robots, Karnaugh maps and digital-to-analog converters.

**Q (10 marks). Explain the common binary codes (BCD, excess-3, Gray, ASCII) and the error-detecting and error-correcting codes (parity and Hamming).**

**Introduction.** A **code** represents numbers, letters or other information by groups of bits. Codes are chosen for ease of conversion, for safety against errors or for universal exchange of text (Plates 2.2 to 2.5).

**A. Numeric codes**

1. **BCD (8421):** each decimal digit has its own 4-bit group, so 2025 = 0010 0000 0010 0101. It is easy to display (Nixie tubes, seven-segment displays) but needs more bits than binary: 16 bits against 11 for 2025.
2. **Excess-3:** BCD plus 3, so 47 = 0111 1010. It is self-complementing: the 9's complement is found by inverting each bit, which simplified old decimal adders.
3. **Gray code:** one bit changes between successive numbers; used in shaft encoders and K-maps (Plate 2.3).

**B. Alphanumeric codes**

4. **ASCII:** a 7-bit code for 128 characters; A = 65, a = 97, 0 = 48. On 8-level tape the eighth bit is a parity bit (Figure 2.4).
5. **Unicode/UTF-8:** assigns a number to every character of every script; Devanagari letters take 3 bytes in UTF-8.

**C. Error codes**

6. **Parity:** one extra bit makes the count of 1s even or odd. It detects any odd number of errors, but cannot locate or correct them, and misses two errors together.
7. **Hamming (7,4):** three parity bits at positions 1, 2 and 4 protect four data bits. The three checks give a syndrome that is the position of the wrong bit (Figure 2.5): all 7 single errors were corrected, but double errors are not.
8. **Check digits:** EAN-13 and ISBN add one digit computed with weights 1 and 3; a swap or misread digit makes the check fail (Plate 2.5).

| Code | Bits per symbol | Property | Use |
|---|---|---|---|
| BCD | 4 per digit | direct decimal | meters, displays |
| Excess-3 | 4 per digit | self-complementing | old adders |
| Gray | n | one-bit change | encoders, K-maps |
| ASCII | 7 | text | files, terminals |
| Parity | +1 | detects odd errors | serial ports |
| Hamming (7,4) | 7 for 4 data | corrects 1 error | ECC memory |

**Conclusion.** No single code serves all needs. BCD suits decimal displays, Gray suits mechanical sensors, ASCII and Unicode serve text, and parity, Hamming and check digits protect data. A designer chooses the code that makes the hardware simplest and the data safest.
