---
subject: Digital Logic
grade: BCA Semester 1
unit: 3
title: Combinational Logic Design: Gates, Boolean Algebra, K-Maps and Standard Circuits
hours: 16
area: BCA 103 · Digital Logic · Unit 3
---

A **combinational circuit** is one whose outputs depend only on its present inputs; it has no memory. Adders, comparators, decoders and multiplexers are all combinational, and together they form the arithmetic and data-path logic of a CPU. This is the largest unit of the subject and the one with the most exam marks.

::: key What this unit gives you
- The seven gates, their truth tables, and NAND/NOR as universal gates.
- Boolean algebra: postulates, theorems, De Morgan; SOP/POS and canonical forms.
- Karnaugh maps (2 to 4 variables) with don't-cares.
- Half and full adders and subtractors; parallel adder.
- Encoders, decoders, multiplexers, demultiplexers, comparators, parity circuits, and a note on programmable logic.
:::

## 3.1 Logic gates

| Gate | Symbol (expression) | Output is 1 when | Truth table (A B → F) |
|---|---|---|---|
| NOT | F = A' | input is 0 | 0→1, 1→0 |
| AND | F = A·B | both inputs 1 | 00→0, 01→0, 10→0, 11→1 |
| OR | F = A + B | at least one input 1 | 00→0, 01→1, 10→1, 11→1 |
| NAND | F = (A·B)' | not both 1 | 00→1, 01→1, 10→1, 11→0 |
| NOR | F = (A + B)' | both 0 | 00→1, 01→0, 10→0, 11→0 |
| XOR | F = A ⊕ B = A'B + AB' | inputs differ | 00→0, 01→1, 10→1, 11→0 |
| XNOR | F = (A ⊕ B)' = AB + A'B' | inputs equal | 00→1, 01→0, 10→0, 11→1 |

XOR of several inputs is 1 when an **odd** number of inputs are 1, which is why XOR trees generate parity. XNOR is the one-bit equality comparator.

**Universal gates.** NAND alone (and NOR alone) can build every other gate:

| Want | With NAND | With NOR |
|---|---|---|
| NOT A | NAND(A, A) | NOR(A, A) |
| A·B | NOT(NAND(A,B)) | NOR(A', B') |
| A + B | NAND(A', B') | NOT(NOR(A,B)) |

Any SOP expression becomes a **two-level NAND–NAND** circuit directly: replace every AND and OR with NAND (bubbles cancel by De Morgan). Any POS becomes NOR–NOR.

## 3.2 Boolean algebra

Variables take values 0 or 1. Operations: `+` (OR), `·` (AND), `'` (NOT).

| Law | AND form | OR form |
|---|---|---|
| Identity | A·1 = A | A + 0 = A |
| Null (dominance) | A·0 = 0 | A + 1 = 1 |
| Idempotent | A·A = A | A + A = A |
| Complement | A·A' = 0 | A + A' = 1 |
| Involution | (A')' = A | |
| Commutative | AB = BA | A + B = B + A |
| Associative | (AB)C = A(BC) | (A+B)+C = A+(B+C) |
| Distributive | A(B + C) = AB + AC | A + BC = (A+B)(A+C) |
| Absorption | A(A + B) = A | A + AB = A |
| Redundancy | A(A' + B) = AB | A + A'B = A + B |
| Consensus | (A+B)(A'+C)(B+C) = (A+B)(A'+C) | AB + A'C + BC = AB + A'C |
| **De Morgan** | (A + B)' = A'B' | (AB)' = A' + B' |

**Duality**: swap AND↔OR and 0↔1 in a true identity and you get another true identity. **De Morgan** extends to any number of variables: (A + B + C)' = A'B'C'.

::: example Worked example: simplify F = AB + A'C + BC
By the consensus theorem the term BC is redundant: F = AB + A'C. Proof: BC = BC(A + A') = ABC + A'BC, and each of those is absorbed into AB and A'C.
:::

::: example Worked example: simplify F = (A + B)(A + C)
Distributive law (OR form): F = A + BC.
:::

**Standard forms.** A **minterm** is an AND of all variables, each complemented or not, equal to 1 for exactly one input row; **maxterm** is an OR of all variables, equal to 0 for exactly one row. For three variables, row *i* of the truth table gives minterm mᵢ (e.g. m₃ = A'BC, since 011) and maxterm Mᵢ = (mᵢ)'.

- **Canonical SOP** = sum of the minterms where F = 1: F = Σm(…).
- **Canonical POS** = product of the maxterms where F = 0: F = ΠM(…).
- The minterm indices of F and the maxterm indices of F are complementary sets.

Example: F(A,B,C) is 1 for 1, 4, 5, 7. Then F = Σm(1,4,5,7) = A'B'C + AB'C' + AB'C + ABC, and F = ΠM(0,2,3,6).

## 3.3 Simplification with Karnaugh maps

A **K-map** arranges the truth table in a grid in which adjacent cells differ by exactly one variable (Gray-code order 00, 01, 11, 10 along each axis), so that grouping adjacent 1s applies the rule AB + AB' = A visually.

**Rules**

1. Mark 1s for SOP (use 0s for POS).
2. Form groups of 1, 2, 4, 8, 16 adjacent cells (a power of two), rectangles only; the map **wraps around** top-to-bottom and left-to-right, and the four corners are adjacent.
3. Use the **fewest, largest** groups that cover every 1; overlap is allowed.
4. Each group gives one product term: keep the variables that do not change inside the group. Larger group → fewer literals.
5. **Don't-care** cells (X) may be included in a group if they enlarge it, and are otherwise ignored.
6. Prime implicant: a group that cannot be enlarged. **Essential** prime implicant: the only group covering some 1; it must be chosen.

**Two-variable and three-variable layout** (rows A, columns BC in Gray order 00, 01, 11, 10):

```text
      BC  00  01  11  10
   A=0 |  m0  m1  m3  m2
   A=1 |  m4  m5  m7  m6
```

**Four-variable example.** F(A,B,C,D) = Σm(0, 1, 2, 5, 8, 9, 10). Layout (rows AB, columns CD in Gray order):

```text
       CD  00  01  11  10
   AB=00 |  1   1   0   1
   AB=01 |  0   1   0   0
   AB=11 |  0   0   0   0
   AB=10 |  1   1   0   1
```

Groups: the four cells m0, m1, m8, m9 (columns 00 and 01 in rows 00 and 10, wrapping vertically) form B'C'; the four cells m0, m2, m8, m10 (the four corners) form B'D'; m1 and m5 (column 01, rows 00 and 01) form A'C'D. So **F = B'C' + B'D' + A'C'D**.

**POS from the map**: group the 0s, write each group as a sum of the variables that stay constant but *complemented*, and multiply the sums. **Don't-care example.** F = Σm(1, 3, 7, 11, 15) + d(0, 2, 5). Cells 0, 1, 2, 3 form the group A'B' (using the X cells 0 and 2 to complete it), and cells 3, 7, 11, 15 form CD. Every required 1 is covered, so **F = A'B' + CD**; the X cell 5 is simply left out.

## 3.4 Arithmetic circuits

**Half adder** adds two bits: Sum = A ⊕ B, Carry = A·B.

**Full adder** adds A, B and carry-in C_in: Sum = A ⊕ B ⊕ C_in; C_out = AB + C_in(A ⊕ B). It can be built from two half adders and an OR gate.

| A B Cin | Sum | Cout |
|---|---|---|
| 0 0 0 | 0 | 0 |
| 0 0 1 | 1 | 0 |
| 0 1 0 | 1 | 0 |
| 0 1 1 | 0 | 1 |
| 1 0 0 | 1 | 0 |
| 1 0 1 | 0 | 1 |
| 1 1 0 | 0 | 1 |
| 1 1 1 | 1 | 1 |

**Half subtractor**: Difference = A ⊕ B, Borrow = A'B. **Full subtractor**: D = A ⊕ B ⊕ B_in, B_out = A'B + (A ⊕ B)' B_in.

**Parallel (ripple-carry) adder.** Chain n full adders, each carry-out feeding the next carry-in. It is simple but slow: the carry must ripple through all stages, so the delay is about n × (carry delay). A **carry-lookahead adder** computes carries in parallel from *generate* G = AB and *propagate* P = A ⊕ B, with C₁ = G₀ + P₀C₀, C₂ = G₁ + P₁G₀ + P₁P₀C₀, and so on. **Adder-subtractor**: XOR each B input with a control M and feed M as the first carry-in; M = 0 adds, M = 1 computes A + B' + 1 = A − B. Overflow is C_n ⊕ C_(n−1). A 4-bit chip is the 7483; BCD addition needs a correction of +6.

## 3.5 Encoders, decoders, multiplexers

**Decoder (n → 2ⁿ).** Exactly one output goes active for each input code, so each output is a minterm of the inputs. A 3-to-8 decoder (74138) has three inputs, eight outputs and enable inputs; any function of three variables is the OR of the right decoder outputs. Decoders drive memory chip-select lines and **BCD-to-seven-segment** displays. A 4-to-16 decoder can be built from two 3-to-8 decoders using the extra input as the enable selector.

**Encoder (2ⁿ → n).** The reverse: 8 inputs, 3-bit output giving the number of the active input. A plain encoder fails if two inputs are active together; a **priority encoder** outputs the code of the highest-priority active input and has a valid flag. Octal-to-binary encoder: A₂ = D₄ + D₅ + D₆ + D₇, A₁ = D₂ + D₃ + D₆ + D₇, A₀ = D₁ + D₃ + D₅ + D₇.

**Multiplexer (MUX).** A data selector: 2ⁿ data inputs, n select lines, one output. A 4-to-1 MUX has Y = S₁'S₀'I₀ + S₁'S₀I₁ + S₁S₀'I₂ + S₁S₀I₃. **MUX as a function generator**: a 2ⁿ-to-1 MUX implements any function of n variables by connecting the variables to the selects and tying data inputs to 0, 1 or to the other variable. Example: F(A,B) = A ⊕ B on a 4-to-1 MUX with S₁ = A and S₀ = B: I₀ = 0, I₁ = 1, I₂ = 1, I₃ = 0. A 2ⁿ⁻¹-to-1 MUX can implement an n-variable function by using the last variable as data input. MUX trees expand width (a 16-to-1 MUX from five 4-to-1 MUXes).

**Demultiplexer (DEMUX).** One input routed to one of 2ⁿ outputs chosen by the select lines; a decoder with its enable input used as data is a DEMUX.

**Magnitude comparator.** For two bits, A = B when XNOR is 1; A > B when AB' = 1; A < B when A'B = 1. A 4-bit comparator (7485) compares from the most significant bit down and produces A>B, A=B, A<B.

**Parity generator and checker.** An even-parity bit for 4 data bits is P = D₃ ⊕ D₂ ⊕ D₁ ⊕ D₀. The checker XORs all received bits (data and parity); output 1 means an error.

## 3.6 Basic ideas of programmable logic

Instead of wiring gates by hand, a **PLD** contains a grid that can be programmed. A **PROM** has a fixed AND array (a full decoder) and a programmable OR array; a **PAL** has a programmable AND array and fixed OR array; a **PLA** has both arrays programmable. FPGAs generalise the idea with thousands of programmable lookup tables. A ROM is a combinational circuit: its address is the input, its stored word is the output.

## Formula and fact sheet

- Half adder: S = A⊕B, C = AB. Full adder: S = A⊕B⊕Cin, Cout = AB + Cin(A⊕B).
- De Morgan: (A+B)' = A'B'; (AB)' = A'+B'. Consensus: AB + A'C + BC = AB + A'C.
- Minterm index from row; ΣF and ΠF use complementary index sets.
- K-map groups: powers of two, wrap-around, fewest and largest; X cells optional.
- n-to-2ⁿ decoder yields minterms; 2ⁿ-to-1 MUX implements any n-variable function.
- NAND–NAND = SOP; NOR–NOR = POS. A − B = A + B' + 1.

## Chapter summary

- Gates → Boolean algebra → minimal expressions (K-map) → standard building blocks.
- NAND and NOR alone are enough for any circuit.
- Adders chain into n-bit arithmetic; the same adder subtracts with XORs on B.
- Decoders, encoders, multiplexers and demultiplexers route data; any function is one MUX or decoder plus gates.

## Practice

1. Simplify F = AB + A'C + BC and F = A + A'B + A'B'C.
2. Prove (A + B)(A' + C) = AC + A'B using Boolean laws.
3. Express F(A,B,C) = Σm(1, 4, 5, 7) in POS form and write the simplified SOP.
4. Simplify F(A,B,C,D) = Σm(0, 2, 5, 7, 8, 10, 13, 15).
5. Simplify F(A,B,C,D) = Σm(1, 3, 7, 11, 15) + d(0, 2, 5).
6. Realise XOR using only NAND gates and state how many are needed.
7. Design a full adder from two half adders and one OR gate; give the equations.
8. Implement F(A,B,C) = Σm(1, 2, 4, 7) using an 8-to-1 MUX and then using a 4-to-1 MUX.
9. Design a 2-bit magnitude comparator (A₁A₀ vs B₁B₀) in terms of its outputs.
10. How many 3-to-8 decoders make a 5-to-32 decoder?

::: note Answers and worked solutions
**1.** AB + A'C + BC = AB + A'C (consensus). A + A'B = A + B; so A + A'B + A'B'C = A + B + A'B'C = A + B + B'C = A + B + C. Final **F = A + B + C**.
**2.** Expand: AA' + AC + A'B + BC = 0 + AC + A'B + BC. By consensus BC is redundant, leaving AC + A'B.
**3.** F = 0 for 0, 2, 3, 6, so F = ΠM(0, 2, 3, 6) = (A+B+C)(A+B'+C)(A+B'+C')(A'+B'+C). On the K-map the 1s are cells 1, 4, 5, 7. Cell 1 is covered only by {1, 5} = B'C, cell 4 only by {4, 5} = AB', cell 7 only by {5, 7} = AC. All three groups are essential, so **F = AB' + AC + B'C**.
**4.** The 1s are 0, 2, 8, 10 (the four corners: B'D') and 5, 7, 13, 15 (the middle block: BD). **F = B'D' + BD** (the XNOR of B and D).
**5.** With the X cells: cells 0, 1, 2, 3 (A'B') and 3, 7, 11, 15 (CD) cover all the required 1s: **F = A'B' + CD**.
**6.** With N = NAND(A, B): F = NAND(NAND(A, N), NAND(B, N)). Four NAND gates.
**7.** HA₁: S₁ = A ⊕ B, C₁ = AB. HA₂: Sum = S₁ ⊕ Cin, C₂ = S₁·Cin. Cout = C₁ + C₂.
**8.** 8-to-1 MUX: select lines A, B, C; I₁ = I₂ = I₄ = I₇ = 1 and the others 0. 4-to-1 MUX: S₁ = A, S₀ = B; for AB = 00 (minterms 0, 1) F = C → I₀ = C; for AB = 01 (2, 3) F = C' → I₁ = C'; for AB = 10 (4, 5) F = C' → I₂ = C'; for AB = 11 (6, 7) F = C → I₃ = C.
**9.** A = B: (A₁ ⊙ B₁)(A₀ ⊙ B₀). A > B: A₁B₁' + (A₁ ⊙ B₁)A₀B₀'. A < B: A₁'B₁ + (A₁ ⊙ B₁)A₀'B₀.
**10.** Four 3-to-8 decoders give the 32 outputs. The two most significant input bits go to one 2-to-4 decoder whose four outputs enable one 3-to-8 decoder each; the low three input bits go to all four. That is four 3-to-8 decoders plus one 2-to-4 decoder.
:::
