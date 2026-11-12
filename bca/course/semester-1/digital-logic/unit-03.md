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

```svgfig label="3.1" caption="Standard logic-gate symbols with their Boolean expressions. A small circle (bubble) on an output means inversion; XOR adds a second curved line on the input side."
import math
f = Fig(760, 300)
def bez(p0, c, p1, n=10):
    return [((1-t)**2*p0[0]+2*(1-t)*t*c[0]+t*t*p1[0], (1-t)**2*p0[1]+2*(1-t)*t*c[1]+t*t*p1[1]) for t in [i/n for i in range(n+1)]]
def gate(kind, ox, oy, expr):
    x, y = ox + 60, oy + 30; ins = [y + 10, y + 30]
    if kind == "NOT": ins = [y + 20]
    if kind in ("AND", "NAND"):
        pts = [(x, y), (x + 28, y)] + [(x + 28 + 20 * math.sin(math.radians(a)), y + 20 - 20 * math.cos(math.radians(a))) for a in range(0, 181, 15)] + [(x, y + 40)]
        tip = x + 48
    elif kind == "NOT":
        pts = [(x, y), (x, y + 40), (x + 40, y + 20)]; tip = x + 40
    else:
        pts = bez((x, y), (x + 34, y), (x + 54, y + 20)) + bez((x + 54, y + 20), (x + 34, y + 40), (x, y + 40))[1:] + bez((x, y + 40), (x + 14, y + 20), (x, y))[1:]
        tip = x + 54
    f.poly(pts, fill=SOFT, stroke=NAVY, sw=1.8)
    if kind in ("XOR",):
        f.poly(bez((x - 8, y), (x + 6, y + 20), (x - 8, y + 40)), fill="none", stroke=NAVY, sw=1.8)
    bub = kind in ("NAND", "NOR", "NOT")
    if bub: f.circle(tip + 4, y + 20, 4, fill="#ffffff", stroke=NAVY, label="")
    for yy in ins: f.line(x - 24, yy, x - (8 if kind == "XOR" else 0) + (2 if kind in ("OR", "NOR") else 0), yy, color=NAVY, sw=1.6)
    f.line(tip + (8 if bub else 0), y + 20, tip + 34, y + 20, color=NAVY, sw=1.6)
    f.text(ox + 120, oy + 90, kind, size=11.5, color=NAVY, bold=True); f.text(ox + 120, oy + 108, expr, size=10.5, color=SLATE)
gate("AND", 0, 0, "F = A·B"); gate("OR", 250, 0, "F = A + B"); gate("NOT", 500, 0, "F = A'")
gate("NAND", 0, 140, "F = (A·B)'"); gate("NOR", 250, 140, "F = (A + B)'"); gate("XOR", 500, 140, "F = A ⊕ B")
```

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

```svgfig label="3.2" caption="Four-variable Karnaugh map for F = Σm(0, 1, 2, 5, 8, 9, 10). Teal: B'C' (wraps top-bottom); red: B'D' (four corners); navy: A'C'D. Result F = B'C' + B'D' + A'C'D."
f = Fig(760, 300)
rows = ["00", "01", "11", "10"]; cols = ["00", "01", "11", "10"]
ones = {0, 1, 2, 5, 8, 9, 10}; x0, y0, w = 150, 50, 64
f.text(x0 - 60, y0 - 22, "AB \\ CD", size=10.5, color=NAVY, bold=True)
for j, c in enumerate(cols): f.text(x0 + j * w + w / 2, y0 - 10, c, size=11, color=NAVY, bold=True)
for i, r in enumerate(rows):
    f.text(x0 - 28, y0 + i * w + w / 2 + 4, r, size=11, color=NAVY, bold=True)
    for j, c in enumerate(cols):
        m = int(r[0] + r[1] + c[0] + c[1], 2)
        f.box(x0 + j * w, y0 + i * w, w, w, "1" if m in ones else "0", fill="#ffffff", stroke="#cbd5e1", size=16, bold=m in ones, color=NAVY if m in ones else "#9ca3af")
        f.text(x0 + j * w + 8, y0 + i * w + 12, f"m{m}", size=8, color=SLATE, anchor="start")
def g(r1, c1, r2, c2, col, pad):
    f.box(x0 + c1 * w + pad, y0 + r1 * w + pad, (c2 - c1 + 1) * w - 2 * pad, (r2 - r1 + 1) * w - 2 * pad, "", fill="none", stroke=col, r=14)
g(0, 0, 0, 1, TEAL, 4); g(3, 0, 3, 1, TEAL, 4)
for r in (0, 3):
    for c in (0, 3): g(r, c, r, c, RED, 9)
g(0, 1, 1, 1, NAVY, 14)
f.box(470, 50, 270, 34, "F = B'C' + B'D' + A'C'D", fill=NAVY, stroke=NAVY, color="#ffffff", size=13, bold=True)
for i, (t, c) in enumerate([("B'C': m0, m1, m8, m9 (4 cells, wraps vertically)", TEAL), ("B'D': m0, m2, m8, m10 (4 corners)", RED), ("A'C'D: m1, m5 (2 cells)", NAVY)]):
    f.circle(484, 112 + i * 30, 7, fill=c, stroke=c, label=""); f.text(500, 116 + i * 30, t, size=10.5, color=SLATE, anchor="start")
f.text(470, 222, "Rule: groups of 1, 2, 4, 8, 16 ones; make each", size=10.5, color=SLATE, anchor="start")
f.text(470, 240, "group as large as possible; the edges wrap round;", size=10.5, color=SLATE, anchor="start")
f.text(470, 258, "every 1 must be covered; overlaps are allowed.", size=10.5, color=SLATE, anchor="start")
```

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

```svgfig label="3.3" caption="A full adder built from two half adders and an OR gate. Sum = A xor B xor Cin; Cout = AB + Cin(A xor B)."
f = Fig(760, 250)
f.box(120, 40, 120, 60, "Half adder 1\nXOR + AND", fill=SOFT, stroke=NAVY, size=11, bold=True)
f.box(360, 90, 120, 60, "Half adder 2\nXOR + AND", fill=SOFT, stroke=NAVY, size=11, bold=True)
f.box(570, 130, 80, 44, "OR", fill=SAND, stroke=AMBER, size=13, bold=True)
f.text(40, 58, "A", size=13, color=NAVY, bold=True); f.text(40, 86, "B", size=13, color=NAVY, bold=True); f.text(300, 190, "Cin", size=13, color=NAVY, bold=True)
f.arrow([(52, 54), (120, 54)], color=SLATE); f.arrow([(52, 82), (120, 82)], color=SLATE)
f.arrow([(240, 56), (300, 56), (300, 104), (360, 104)], color=SLATE, label="S1", lpos=(280, 48))
f.arrow([(330, 184), (330, 136), (360, 136)], color=SLATE)
f.arrow([(240, 88), (270, 88), (270, 220), (610, 220), (610, 174)], color=SLATE, label="C1", lpos=(440, 212))
f.arrow([(480, 104), (700, 104)], color=TEAL, sw=2, label="Sum", lpos=(690, 94))
f.arrow([(480, 136), (570, 144)], color=SLATE, label="C2", lpos=(525, 128))
f.arrow([(650, 152), (710, 152)], color=RED, sw=2, label="Cout", lpos=(715, 142))
```

## 3.5 Encoders, decoders, multiplexers

**Decoder (n → 2ⁿ).** Exactly one output goes active for each input code, so each output is a minterm of the inputs. A 3-to-8 decoder (74138) has three inputs, eight outputs and enable inputs; any function of three variables is the OR of the right decoder outputs. Decoders drive memory chip-select lines and **BCD-to-seven-segment** displays. A 4-to-16 decoder can be built from two 3-to-8 decoders using the extra input as the enable selector.

**Encoder (2ⁿ → n).** The reverse: 8 inputs, 3-bit output giving the number of the active input. A plain encoder fails if two inputs are active together; a **priority encoder** outputs the code of the highest-priority active input and has a valid flag. Octal-to-binary encoder: A₂ = D₄ + D₅ + D₆ + D₇, A₁ = D₂ + D₃ + D₆ + D₇, A₀ = D₁ + D₃ + D₅ + D₇.

**Multiplexer (MUX).** A data selector: 2ⁿ data inputs, n select lines, one output. A 4-to-1 MUX has Y = S₁'S₀'I₀ + S₁'S₀I₁ + S₁S₀'I₂ + S₁S₀I₃. **MUX as a function generator**: a 2ⁿ-to-1 MUX implements any function of n variables by connecting the variables to the selects and tying data inputs to 0, 1 or to the other variable. Example: F(A,B) = A ⊕ B on a 4-to-1 MUX with S₁ = A and S₀ = B: I₀ = 0, I₁ = 1, I₂ = 1, I₃ = 0. A 2ⁿ⁻¹-to-1 MUX can implement an n-variable function by using the last variable as data input. MUX trees expand width (a 16-to-1 MUX from five 4-to-1 MUXes).

**Demultiplexer (DEMUX).** One input routed to one of 2ⁿ outputs chosen by the select lines; a decoder with its enable input used as data is a DEMUX.

**Magnitude comparator.** For two bits, A = B when XNOR is 1; A > B when AB' = 1; A < B when A'B = 1. A 4-bit comparator (7485) compares from the most significant bit down and produces A>B, A=B, A<B.

**Parity generator and checker.** An even-parity bit for 4 data bits is P = D₃ ⊕ D₂ ⊕ D₁ ⊕ D₀. The checker XORs all received bits (data and parity); output 1 means an error.

## 3.6 Basic ideas of programmable logic

Instead of wiring gates by hand, a **PLD** contains a grid that can be programmed. A **PROM** has a fixed AND array (a full decoder) and a programmable OR array; a **PAL** has a programmable AND array and fixed OR array; a **PLA** has both arrays programmable. FPGAs generalise the idea with thousands of programmable lookup tables. A ROM is a combinational circuit: its address is the input, its stored word is the output.

```photogrid label="3.1" cols="2" ratio="1.55" caption="Where gate circuits are built and tested. (a) A solderless breadboard: the five holes of each short column are joined underneath, and the long rails carry power. (b) A logic analyzer, an instrument that records many digital lines at once so that timing faults can be seen."
@ photo id="bca103/breadboard" cap="Solderless breadboard (400 tie points)"
fit 1.55
mark 0.52 0.60 "1"
mark 0.30 0.80 "2"
mark 0.82 0.42 "3"
key 1 Rows of five joined holes: place the IC across the centre gap
key 2 Power rails (red +, blue -)
key 3 Centre gap separating the two halves
@ photo id="bca103/logican" cap="HP 1653B logic analyzer"
fit 1.55
call 0.30 0.90 0.28 0.62 "Screen: waveforms of each line"
call 0.72 0.10 0.70 0.45 "Keypad and rotary knob"
```

### PROM, EPROM, PAL and PLA in detail

Every programmable logic device (PLD) is built from the same two blocks: an **AND array** that forms product terms from the inputs and their complements, and an **OR array** that adds product terms to make each output. The devices differ in *which array the designer may program*.

| Device | AND array | OR array | Typical use |
|---|---|---|---|
| **PROM** (programmable read-only memory) | Fixed: a full decoder, one line for every minterm | Programmable | Look-up tables, microcode, small memories; any function of n inputs needs 2ⁿ words |
| **EPROM** (erasable PROM) | Fixed decoder | Programmable and erasable with ultraviolet light through a quartz window | Prototype firmware that is erased and rewritten under UV light for about 20 minutes |
| **PAL** (programmable array logic) | Programmable | Fixed (each output sums a fixed number of product terms) | Cheap, fast glue logic; the most common PLD |
| **PLA** (programmable logic array) | Programmable | Programmable | Flexible: a product term can be shared between several outputs |

**PROM as a function generator.** A PROM with 3 address inputs has 8 words. Writing the truth table of a function into the words *is* the implementation. Example: a full adder with inputs A, B, Cin and outputs Sum and Cout needs an 8 × 2 PROM whose content is the truth table:

| A B Cin | Word (Cout Sum) |
|---|---|
| 000 | 00 |
| 001 | 01 |
| 010 | 01 |
| 011 | 10 |
| 100 | 01 |
| 101 | 10 |
| 110 | 10 |
| 111 | 11 |

The PROM is simple but wasteful: if an input is added, the number of words doubles, even if the function needs few product terms. For the same reason, 16-input functions are never done in a PROM.

**EPROM, EEPROM and flash.** The EPROM stores a bit as charge on a floating gate. A programming voltage places the charge; ultraviolet light gives the electrons enough energy to leak away, which erases the whole chip. **EEPROM** erases electrically, one byte at a time, and **flash** erases in blocks, which is why it is used in pen drives, SSDs, phones and the BIOS chips of laptops. Programmable-ROM types differ in *how they are erased*, not in the logic they implement.

**PAL.** Each output of a PAL has its own fixed group of product terms (for example, two or four). A PAL16L8 has 16 inputs and 8 outputs. If a function needs more terms than one output provides, the designer chains an output back as an input. PALs are fast because the fixed OR array is short, and they are cheap to make.

**PLA.** Both arrays are programmable, so a product term such as A·B' can be *shared* by several outputs. A PLA implements a set of functions with fewer product terms than separate gates. Compared with a PROM, a PLA does not have to include every minterm; compared with a PAL, it allows sharing but is slower and costs more.

**Reading a PLD diagram.** A cross (×) at a crossing means a fuse is intact, i.e. the input is connected to that product line. A dot means a fixed connection. A missing mark means a blown fuse (no connection). A product line with all fuses intact is always 0 (because A·A' = 0), a standard shorthand.

**Example: sharing in a PLA.** Implement F1 = A·B + A'·C and F2 = A·B + B·C. The product term A·B is used by both outputs. A PLA needs product terms {A·B, A'·C, B·C}, three in total; a PAL with fixed OR gates would need A·B twice, four product terms in total.

```svgfig label="3.4" caption="Block structure of a PROM. The decoder (a fixed AND array) turns each 3-bit address into one active word line; programmable links in the OR array connect word lines to outputs. A PAL swaps the roles, with the AND array programmable and the OR array fixed."
f = Fig(580, 210)
f.box(10, 70, 80, 70, "Inputs\nA B C", fill=SAND, stroke=AMBER, size=11, bold=True)
f.box(150, 40, 130, 130, "Fixed AND array\n(3-to-8 decoder)\n\nm0 ... m7", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.box(350, 40, 130, 130, "Programmable\nOR array\n(fuse links)", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(515, 70, 60, 70, "Outputs\nD0 D1", fill=ROSE, stroke=RED, size=10.5, bold=True)
f.arrow([(90, 105), (150, 105)], color=SLATE)
f.arrow([(280, 105), (350, 105)], color=SLATE)
f.text(315, 94, "8 lines", size=9.5, color=SLATE)
f.arrow([(480, 105), (515, 105)], color=SLATE)
```

## 3.7 Implementing logic functions with multiplexers and decoders

The TU syllabus asks for *implementation of logical functions using multiplexers*. A MUX and a decoder are both **universal function generators**: with the right wiring, one chip replaces a whole sum-of-products circuit.

### Method A: a 2ⁿ-to-1 MUX for an n-variable function

Connect the n variables to the select lines and wire each data input to 0 or 1 according to the truth table. This is a table look-up. Example: F(A, B, C) = Σm(1, 2, 6, 7) with an 8-to-1 MUX has inputs I1 = I2 = I6 = I7 = 1 and all other data inputs 0.

### Method B: a 2ⁿ⁻¹-to-1 MUX for an n-variable function (the "folding" method)

Use n − 1 variables as the select lines and let the last variable (or its complement, 0 or 1) feed the data inputs. For the same F = Σm(1, 2, 6, 7), use A and B as select lines and C as the data variable:

| Select A B | Minterms in this pair | F in terms of C | Data input |
|---|---|---|---|
| 0 0 | m0 (C = 0) gives 0, m1 (C = 1) gives 1 | F = C | I0 = C |
| 0 1 | m2 (C = 0) gives 1, m3 (C = 1) gives 0 | F = C' | I1 = C' |
| 1 0 | m4 gives 0, m5 gives 0 | F = 0 | I2 = 0 |
| 1 1 | m6 gives 1, m7 gives 1 | F = 1 | I3 = 1 |

So a **4-to-1 MUX with I0 = C, I1 = C', I2 = 0, I3 = 1** realises a 3-variable function with one inverter. The rule for each pair of minterms (C = 0, C = 1) is: both 0 gives 0; both 1 gives 1; only the C = 1 minterm gives C; only the C = 0 minterm gives C'.

::: example Step by step: F(A, B, C, D) = Σm(1, 3, 4, 11, 12, 13, 14, 15) with an 8-to-1 MUX
Use A, B, C as select lines and D as the data variable. Write the truth table in pairs (D = 0, D = 1):

| ABC | Minterms | Which are in F | Data input |
|---|---|---|---|
| 000 | m0, m1 | m1 only | I0 = D |
| 001 | m2, m3 | m3 only | I1 = D |
| 010 | m4, m5 | m4 only | I2 = D' |
| 011 | m6, m7 | none | I3 = 0 |
| 100 | m8, m9 | none | I4 = 0 |
| 101 | m10, m11 | m11 only | I5 = D |
| 110 | m12, m13 | both | I6 = 1 |
| 111 | m14, m15 | both | I7 = 1 |

One 8-to-1 MUX and one inverter replace a four-variable gate network. Check: with ABC = 010 and D = 0, I2 = D' = 1, so F = 1, which is m4 (0100). Correct.
:::

### Method C: a decoder with OR (or NAND) gates

A decoder produces every minterm; the OR gate collects the ones the function needs. For the full adder with inputs A, B, Cin on a 3-to-8 decoder:

- **Sum** = Σm(1, 2, 4, 7) = OR of outputs Y1, Y2, Y4, Y7
- **Carry out** = Σm(3, 5, 6, 7) = OR of outputs Y3, Y5, Y6, Y7

A real 74138 decoder has *active-low* outputs, so a **NAND gate** is used instead of an OR (De Morgan: the NAND of active-low lines is the OR of active-high lines). That is why the standard 74138 full adder uses two 4-input NAND gates.

| Technique | Chip count for a 3-variable function | Remarks |
|---|---|---|
| Gates (SOP) | Several ANDs, one OR, inverters | Smallest for simple functions |
| 8-to-1 MUX | One MUX | Direct truth-table mapping |
| 4-to-1 MUX with a variable | One MUX and at most one inverter | Needs the data-variable folding |
| 3-to-8 decoder and NAND | One decoder and one NAND per output | Best when several functions share the same inputs |

## 3.8 Building a 16-to-1 multiplexer and a 1-to-16 demultiplexer

The prescribed laboratory work asks for a 16:1 MUX and a 1:16 DEMUX. Commercial parts exist (74150 is a 16-to-1 MUX; 74154 is a 4-to-16 decoder that works as a 1-to-16 DEMUX) but the lab also teaches how to **build large from small**.

**16-to-1 MUX from 4-to-1 MUXes.** Use four 4-to-1 MUXes in the first stage and one in the second stage:

1. The 16 data inputs I0 to I15 are divided into four groups of four. Each group feeds one first-stage MUX.
2. All four first-stage MUXes share the same select lines S1 S0, the *low* two bits of the 4-bit select.
3. The four first-stage outputs feed a second-stage 4-to-1 MUX whose select lines are S3 S2, the *high* two bits.

Check: to select I11 (binary 1011), S3 S2 = 10 selects the third group (I8 to I11) and S1 S0 = 11 picks its fourth member. Total: 5 MUX chips, 20 data pins.

**1-to-16 DEMUX from a 4-to-16 decoder.** A decoder with an enable input acts as a DEMUX: the data bit goes to the enable input and the four select lines go to the decoder inputs. Only the addressed output follows the data; all other outputs stay inactive. (The 74154 has two active-low enable inputs G1 and G2. Tie one low and apply the data bit to the other.)

**1-to-16 DEMUX from 1-to-4 DEMUXes (tree).** Use one 1-to-4 DEMUX in the first stage (select S3 S2) and four 1-to-4 DEMUXes in the second stage (select S1 S0). Again five chips.

```svgfig label="3.5" caption="A 16-to-1 multiplexer built from five 4-to-1 multiplexers. The four first-stage MUXes share select lines S1 S0; the second-stage MUX uses S3 S2. The same tree, reversed, gives a 1-to-16 demultiplexer."
f = Fig(580, 270)
for i in range(4):
    y = 8 + i * 64
    f.box(10, y, 90, 50, "I%d to I%d" % (i * 4, i * 4 + 3), fill=SAND, stroke=AMBER, size=10, bold=True)
    f.box(170, y, 110, 50, "4-to-1 MUX\n(S1 S0)", fill=BLUE, stroke=NAVY, size=10, bold=True)
    f.arrow([(100, y + 25), (170, y + 25)], color=SLATE)
    f.arrow([(280, y + 25), (360, 135)], color=SLATE)
f.box(360, 105, 110, 60, "4-to-1 MUX\n(S3 S2)", fill=MINT, stroke=TEAL, size=10, bold=True)
f.box(515, 115, 55, 40, "Y", fill=ROSE, stroke=RED, size=12, bold=True)
f.arrow([(470, 135), (515, 135)], color=SLATE)
```

## 3.9 Logic gates built from passive and active elements

The first laboratory work is *gates using active and passive elements*. **Passive** elements (resistors and diodes in this context) only pass or drop signals; **active** elements (transistors, and the transistors inside ICs) can amplify and restore a signal. Building gates from them shows what a gate IC contains and why ICs are used in practice.

**Assumptions for the circuits below:** supply 5 V, logic 0 = about 0 V, logic 1 = about 5 V, silicon diode forward drop 0.7 V.

| Gate | Parts | How it works | Output levels |
|---|---|---|---|
| **AND (diode)** | Two diodes with cathodes at the inputs, anodes joined to the output; a resistor from the output to +5 V | If any input is 0 V, its diode conducts and pulls the output down to the input level plus 0.7 V; only when both inputs are at 5 V do both diodes stay off and the resistor lifts the output to 5 V | Low about 0.7 V, high about 5 V |
| **OR (diode)** | Two diodes with anodes at the inputs, cathodes joined to the output; a resistor from the output to ground | The higher input conducts and drives the output to the input level minus 0.7 V; with both inputs at 0 V the resistor holds the output at 0 V | Low 0 V, high about 4.3 V |
| **NOT (transistor)** | An NPN transistor with an emitter at ground, a base resistor (10 kilo-ohm) and a collector resistor (1 kilo-ohm) to +5 V | A high input drives the base current, the transistor saturates and the output drops to about 0.2 V; a low input leaves the transistor cut off and the resistor pulls the output to 5 V | Low about 0.2 V, high about 5 V |

Combining the two kinds of elements gives the next two gates.

| Gate | Parts | How it works | Output levels |
|---|---|---|---|
| **NAND (DTL)** | Diode AND followed by the transistor inverter | AND at the input followed by inversion restores the level | Low about 0.2 V, high about 5 V |
| **NOR (RTL)** | Two transistors in parallel with a common collector resistor; one base resistor per input | Either input high saturates its transistor and pulls the output low | Low about 0.2 V, high about 5 V |

**Worked check of the inverter.** With the input at 5 V the base current is (5 − 0.7) / 10 kilo-ohm = 0.43 mA. The collector current is limited by the resistor: (5 − 0.2) / 1 kilo-ohm = 4.8 mA. A transistor with a current gain of 100 would need only 0.048 mA of base current to carry 4.8 mA, so the 0.43 mA overdrives it. It is saturated, and the output sits at about 0.2 V, a clean logic 0.

**Why the passive gates are not used alone.**

1. *Level degradation.* A diode gate loses 0.7 V at each stage. After a few gates a "high" is no longer recognised as high.
2. *No gain and no fan-out.* The passive gate cannot drive many following gates. The transistor restores the level and supplies current.
3. *Slow and power hungry.* Resistors are slow to charge the load capacitance and waste power.

The fix is to combine them: diode input, transistor output (DTL), then replace the diodes by a multi-emitter transistor (**TTL**, the 74xx family), and finally complementary pairs of MOSFETs (**CMOS**, the 74HC family and every modern processor).

::: note Laboratory procedure: verify the diode AND, diode OR and transistor NOT
1. Build the circuit on a breadboard with the supply at 5 V.
2. Connect each input in turn to 0 V and 5 V; measure the output with a multimeter and enter it in a truth table.
3. Compare the measured levels with the table above. Differences of 0.1 to 0.3 V are normal.
4. Cascade two diode gates and observe how the high level falls, which shows level degradation.
5. Replace the circuit with a 7408, 7432 and 7404 and note that the output is now always a clean 0 V or 5 V.
:::

## 3.10 Where combinational circuits are used: eight applications

1. **Adders inside every CPU.** The ALU is built around full adders chained together. They do addition, and with two's complement they also do subtraction and address calculation. Every spreadsheet total on a Nepali college server passes through such adders.
2. **Decoders for memory and I/O selection.** A decoder turns an address such as 1011 into a single active line. This selects exactly one memory chip or one device. Without it the CPU could not talk to RAM and the keyboard separately.
3. **Multiplexers for data routing.** A MUX picks one of many inputs and sends it on one line. Telephone exchanges, the input selector of a TV and the data paths in a CPU use it. A 4-to-1 MUX can also generate any 2-variable function.
4. **Encoders for keyboards and interrupts.** A priority encoder gives the binary number of the highest-priority active input. A keypad of an ATM and an interrupt controller both use it. If two keys are pressed together, the encoder picks the more important one.
5. **Seven-segment display drivers.** A BCD-to-seven-segment decoder (such as the 7447) lights the right segments for a digit. Electronic meters, queue-token boards in a bank and digital clocks show numbers in this way.
6. **Comparators for decisions.** A magnitude comparator tells whether A is greater than, equal to or smaller than B. A thermostat, a password check and a "sort" instruction all depend on it. A 4-bit comparator such as the 7485 can be cascaded for more bits.
7. **Parity generators and checkers.** An XOR tree creates the parity bit on sending and re-checks it on receiving. Memory modules and serial communication use this to spot a flipped bit. The circuit is simple and fast.
8. **Programmable logic (PLA, PAL, FPGA).** A designer can place a whole sum-of-products design in one programmable chip instead of many gates. This saves board space and allows a later change. University labs use FPGAs to test new processor designs.

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
11. How many bits must a PROM have to implement three functions of four variables? Why is this wasteful?
12. Differentiate PROM, EPROM, PAL and PLA in a table.
13. Implement F(A,B,C) = Σm(0, 2, 3, 5) with a 4-to-1 MUX that uses A and B as select lines.
14. Show how five 4-to-1 MUXes make a 16-to-1 MUX and trace the path of input I13.
15. Implement the full-adder outputs with a 74138 decoder and NAND gates.
16. Why is a purely diode-resistor gate unsuitable for cascading? How does a transistor help?

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
**11.** 16 words x 3 bits = 48 bits. It is wasteful because a PROM contains every minterm; adding one input doubles the size even when the function has only a few product terms.
**12.** PROM: fixed AND (decoder), programmable OR. EPROM: a PROM erased with ultraviolet light. PAL: programmable AND, fixed OR. PLA: both arrays programmable, so product terms can be shared.
**13.** Pairs (C = 0, C = 1): AB = 00 has m0 only, so I0 = C'; AB = 01 has m2 and m3, so I1 = 1; AB = 10 has m5 only, so I2 = C; AB = 11 has none, so I3 = 0.
**14.** Four first-stage 4-to-1 MUXes take I0 to I3, I4 to I7, I8 to I11 and I12 to I15 with S1 S0 shared; the second-stage MUX picks one of the four outputs with S3 S2. I13 = 1101: S3 S2 = 11 picks the fourth group, S1 S0 = 01 picks the second member of it.
**15.** Sum = NAND(Y1', Y2', Y4', Y7') = Y1 + Y2 + Y4 + Y7 and Cout = NAND(Y3', Y5', Y6', Y7'), where Yk' are the active-low decoder outputs of the 74138 with A, B, Cin on the three inputs.
**16.** A diode gate loses about 0.7 V per stage and cannot supply current to many loads, so levels degrade as gates are cascaded. A transistor amplifies and restores the level to a clean 0 or 5 V.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q (5 marks). What are PROM, PAL and PLA? Show how a PROM implements a full adder.**

A programmable logic device contains an AND array and an OR array. In a **PROM** the AND array is fixed (a decoder that produces every minterm) and the OR array is programmable. In a **PAL** the AND array is programmable and the OR array fixed. In a **PLA** both are programmable, so a product term can be shared by several outputs. An **EPROM** is a PROM that can be erased with ultraviolet light and reprogrammed.

*Full adder.* A full adder has three inputs (A, B, Cin) and two outputs (Sum, Cout), so a PROM with 8 words and 2 bits is used. Word 000 holds 00, words 001, 010 and 100 hold 01, words 011, 101 and 110 hold 10, and word 111 holds 11 (Cout Sum). Applying A, B and Cin as the address reads out the correct sum and carry: the truth table is stored in memory.

**Q (5 marks). Implement F(A, B, C, D) = Σm(1, 3, 4, 11, 12, 13, 14, 15) using an 8-to-1 multiplexer.**

Take A, B and C as select lines and D as the data variable. The minterm pairs (D = 0, D = 1) are (0,1), (2,3), (4,5), (6,7), (8,9), (10,11), (12,13), (14,15). For each pair: only m1 is present, so I0 = D; only m3 is present, so I1 = D; only m4 (D = 0) is present, so I2 = D'; none for I3 and I4, so both are 0; only m11 is present, so I5 = D; both of m12, m13 and both of m14, m15 are present, so I6 = I7 = 1. The circuit needs one 8-to-1 MUX and one inverter.

**Q (5 marks). Simplify F(A, B, C, D) = Σm(0, 1, 2, 5, 8, 9, 10) using a Karnaugh map and draw the resulting circuit in words.**

A **Karnaugh map** is a Gray-coded grid in which neighbouring cells differ in one variable, so two adjacent 1s can be merged and one variable disappears. For four variables the grid has 16 cells, with rows AB and columns CD ordered 00, 01, 11, 10 (Figure 3.2). The 1s are placed at m0, m1, m2, m5, m8, m9 and m10.

Grouping (powers of 2, as large as possible, edges wrap round):

1. **Group of four m0, m1, m8, m9**: A and D change, B = 0 and C = 0 stay fixed, so the term is **B'C'**.
2. **Group of four m0, m2, m8, m10** (the four corners): A and C change, B = 0 and D = 0 stay, giving **B'D'**.
3. **Group of two m1, m5**: B changes, A = 0, C = 0, D = 1 stay, giving **A'C'D**.

So **F = B'C' + B'D' + A'C'D**. All seven 1s are covered. The original expression needs seven four-literal minterms (28 literals); the simplified one needs three terms with 7 literals. The circuit is two-level AND–OR: two 2-input ANDs and one 3-input AND feed one 3-input OR. Using NAND gates only, each AND and the OR are replaced by NAND (NAND–NAND form), which needs just one chip type.

**Q (5 marks). Explain the 4-to-1 multiplexer and show how it implements an XOR gate.**

A **multiplexer (MUX)** selects one of several data inputs and passes it to a single output under the control of select lines. A 4-to-1 MUX has four data inputs I0–I3, two select lines S1 S0 and one output Y.

| S1 | S0 | Y |
|---|---|---|
| 0 | 0 | I0 |
| 0 | 1 | I1 |
| 1 | 0 | I2 |
| 1 | 1 | I3 |

Boolean expression: **Y = S1'S0'·I0 + S1'S0·I1 + S1S0'·I2 + S1S0·I3**. Internally it is a 2-to-4 decoder whose outputs are ANDed with the data inputs and ORed together.

**As a function generator**: connect the variables to the select lines and tie each data input to 0, 1 or a variable. For F = A ⊕ B take S1 = A and S0 = B. The truth table of XOR is 0, 1, 1, 0 for AB = 00, 01, 10, 11, so tie I0 = 0, I1 = 1, I2 = 1, I3 = 0. A 2ⁿ-to-1 MUX can therefore realise any n-variable function with no extra gates, which is why a MUX is the basic cell of FPGA look-up tables.

**Q (10 marks). Design a full adder from its truth table. Show how four full adders make a 4-bit ripple-carry adder, and compare it with a carry-lookahead adder.**

*Introduction.* Addition is the most used arithmetic operation in a computer. A **half adder** adds two bits and cannot accept a carry from a lower stage, so it can only be used for the least significant bit. A **full adder** adds A, B and a carry-in C_in.

*Truth table and equations.* The outputs for ABC_in = 000 to 111 are Sum = 0, 1, 1, 0, 1, 0, 0, 1 and C_out = 0, 0, 0, 1, 0, 1, 1, 1 (see the table in 3.4). From the K-map:

- **Sum = A ⊕ B ⊕ C_in** (1 when an odd number of inputs are 1).
- **C_out = AB + BC_in + AC_in**, which equals AB + C_in(A ⊕ B).

*Circuit.* Figure 3.3 shows two half adders and one OR: the first half adder gives S1 = A ⊕ B and C1 = AB; the second adds S1 and C_in to give Sum and C2 = C_in·S1; and C_out = C1 + C2. In all this needs two XOR, two AND and one OR gate.

*Ripple-carry adder.* Connect C_out of stage i to C_in of stage i+1 for four stages, with C_in of stage 0 = 0 (or 1 for subtraction). Adding 0111 + 0101 gives 1100 with carry 0. The adder is cheap and regular but slow: the carry must pass through every stage, so the delay is about n × (two gate delays). At 64 bits this limits the clock.

*Carry-lookahead adder.* It computes carries directly from generate G = AB and propagate P = A ⊕ B: C1 = G0 + P0C0, C2 = G1 + P1G0 + P1P0C0, and so on. Every carry is ready after two or three gate delays, whatever n is.

| Point | Ripple-carry | Carry-lookahead |
|---|---|---|
| Carry delay | grows with n | nearly constant |
| Gates needed | fewest | more (extra lookahead logic) |
| Speed | slow | fast |
| Use | small or cheap circuits | CPUs, ALUs |
| Chip example | two 7482 | 74283 (4-bit) with 74182 |

*Conclusion.* The full adder follows directly from its truth table and a K-map. Chaining it gives a multi-bit adder, and the speed problem of the carry is solved by lookahead logic at the cost of more gates.
