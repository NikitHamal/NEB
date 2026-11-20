---
subject: Computer Science
grade: 8
unit: 15
title: Number System
hours: 0
area: Number System, Graphics and Multimedia
---

You count with ten digits because people first counted on ten fingers. A
computer has no fingers: inside it, every tiny switch is either off or on, so
it counts with only two digits, 0 and 1. This lesson teaches the four number
systems used in computing — decimal, binary, octal and hexadecimal — how to
change a number from one system to another, and how a computer's memory is
measured in bits and bytes. You met base 2 and base 5 in Mathematics; the same
ideas work here. Almost every mark in this lesson is earned by following a
procedure step by step, so practise until the steps are automatic.

::: key What the examination asks from this lesson
In a 50-mark school paper this lesson usually gives **one or two objective
questions** (the base of a system, its symbols, a quick conversion, a memory
unit), **two short questions** (one or two conversions, or a memory-unit
calculation) and often a **long question** made of four conversions
[1+1+1+1]. Marks are given for the **working**, not only the answer: the
division table with its remainders, the expansion with place values, or the
groups of bits. Every answer must carry its **base**, as in $(101101)_2$.
Grade 9 starts its number-system unit with exactly these conversions.
:::

## 15.1 Number systems: decimal, binary, octal and hexadecimal

::: definition Number system and base
A **number system** is a way of writing numbers with a fixed set of symbols
(digits) and rules. The **base** (or **radix**) of a number system is the
number of different digits it uses. The largest digit of a system is always
one less than its base.
:::

All four systems in this lesson are **positional**: the value of a digit depends
on its **position** (place) in the number. The place at the right end is worth
1; every place to the left is worth **base times** the place on its right.

**Decimal (base 10).** Ten digits, 0 to 9. The places are worth 1, 10, 100,
1000 and so on, the powers of 10:

$$(4725)_{10} = 4\times10^3 + 7\times10^2 + 2\times10^1 + 5\times10^0 = 4000 + 700 + 20 + 5$$

**Binary (base 2).** Only two digits, 0 and 1. The places are worth 1, 2, 4, 8,
16, 32, 64, 128 … — each place is double the one on its right. A binary digit
is called a **bit**. Example: $(110111)_2$.

**Octal (base 8).** Eight digits, 0 to 7. The places are worth 1, 8, 64, 512,
4096 … Example: $(375)_8$. The digits 8 and 9 do not exist in octal.

**Hexadecimal (base 16).** Sixteen symbols: the digits 0 to 9 and the letters A
to F, where **A = 10, B = 11, C = 12, D = 13, E = 14 and F = 15**. The places are
worth 1, 16, 256, 4096 … Example: $(\mathrm{8F5})_{16}$. "Hex" is the short name.

To show which system a number belongs to, write its **base as a small number
after it**: $(101)_2$ is binary and means five, while $(101)_{10}$ is the
ordinary one hundred and one. A number written with no base is taken to be
decimal.

| System | Base | Digits used | Largest digit | Place values (right to left) | Example |
|---|---|---|---|---|---|
| Binary | 2 | 0, 1 | 1 | 1, 2, 4, 8, 16, 32 … | $(10110)_2$ |
| Octal | 8 | 0 to 7 | 7 | 1, 8, 64, 512 … | $(207)_8$ |
| Decimal | 10 | 0 to 9 | 9 | 1, 10, 100, 1000 … | $(719)_{10}$ |
| Hexadecimal | 16 | 0 to 9, A to F | F (= 15) | 1, 16, 256, 4096 … | $(\mathrm{AC4})_{16}$ |

```figure caption="The same number, forty-five, written in the four systems. Each digit sits in a box with its place value below it; multiplying each digit by its place value and adding always gives 45. In binary the shaded boxes are the 1s."
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(5.0, 3.1))
ax.set_xlim(0, 10); ax.set_ylim(0, 6.2); ax.axis("off")
rows = [("binary (base 2)", "101101", [32, 16, 8, 4, 2, 1], "= 32 + 8 + 4 + 1 = 45"),
        ("octal (base 8)", "55", [8, 1], "= 5×8 + 5×1 = 45"),
        ("decimal (base 10)", "45", [10, 1], "= 4×10 + 5×1 = 45"),
        ("hexadecimal (base 16)", "2D", [16, 1], "= 2×16 + 13×1 = 45")]
w = 0.52
for i, (name, digits, pv, s) in enumerate(rows):
    y = 5.0 - i * 1.45
    ax.text(0.0, y + 0.25, name, fontsize=7.8, color=INK, fontweight="bold", va="center")
    ax.text(0.0, y - 0.22, "place values", fontsize=7.0, color=MUTED, va="center")
    x0 = 3.4
    for k, (d, p) in enumerate(zip(digits, pv)):
        x = x0 + k * (w + 0.06)
        ax.add_patch(Rectangle((x, y), w, 0.5, fc="#e8f1fb" if d != "0" else "white", ec=ACCENT, lw=1.0))
        ax.text(x + w / 2, y + 0.25, d, ha="center", va="center", fontsize=9.5, color=INK, fontweight="bold")
        ax.text(x + w / 2, y - 0.22, str(p), ha="center", va="center", fontsize=7.0, color=MUTED)
    ax.text(x0 + 6 * (w + 0.06) + 0.15, y + 0.25, s, fontsize=8.0, color=INK, va="center")
```

### Why computers use binary

A computer is built from millions of tiny electronic switches called
transistors, and each one is either **off** or **on**. Two states are easy to
make, easy to tell apart and hard to confuse even when a signal is weak: a low
voltage stands for 0 and a high voltage for 1. The same two-state idea stores
data everywhere in computing — a spot magnetised one way or the other on a hard
disk, a pit or no pit on a DVD, a charge or no charge in a pen drive, light off
or on in an optical fibre. Ten clearly different voltages would be far harder
to build and to read reliably. So all data inside a computer — numbers, letters,
pictures, sound — is stored as patterns of bits.

### Why octal and hexadecimal are used

Long strings of 0s and 1s are hard for people to read and easy to copy wrongly.
Because $8 = 2^3$ and $16 = 2^4$, **one octal digit stands for exactly three
bits** and **one hexadecimal digit for exactly four bits**, so they are short,
exact ways of writing binary. You will meet hexadecimal often:

- **colour codes** in web pages (Lesson 10): `#FF0000` is pure red — FF of red,
  00 of green, 00 of blue;
- **MAC addresses** of network cards (Lesson 14), such as `3C-52-82-9A-7F-10`;
- **memory addresses** and error codes shown by programs.

Octal is used less today; you may see it in the file permissions of Linux, such
as `755`.

| Decimal | Binary | Octal | Hexadecimal |
|---|---|---|---|
| 0 | 0 | 0 | 0 |
| 1 | 1 | 1 | 1 |
| 2 | 10 | 2 | 2 |
| 3 | 11 | 3 | 3 |
| 4 | 100 | 4 | 4 |
| 5 | 101 | 5 | 5 |
| 6 | 110 | 6 | 6 |
| 7 | 111 | 7 | 7 |
| 8 | 1000 | 10 | 8 |
| 9 | 1001 | 11 | 9 |
| 10 | 1010 | 12 | A |
| 11 | 1011 | 13 | B |
| 12 | 1100 | 14 | C |
| 13 | 1101 | 15 | D |
| 14 | 1110 | 16 | E |
| 15 | 1111 | 17 | F |
| 16 | 10000 | 20 | 10 |

Look down the table: in each system, when the largest digit is used up, the
count goes back to 0 and a 1 is carried to the next place — after 1 in binary,
after 7 in octal, after 9 in decimal and after F in hexadecimal.

::: memory Two things to learn by heart
**Binary place values** double from the right: 1, 2, 4, 8, 16, 32, 64, 128, 256,
512, 1024. **Hexadecimal letters:** A = 10, B = 11, C = 12, D = 13, E = 14,
F = 15. With these two lines and the table above, every conversion in this
lesson becomes simple arithmetic.
:::

::: caution Do not read binary as decimal
$(101)_2$ is not "one hundred and one"; read it digit by digit, "one zero one,
base two", and remember it means five. And a digit can never equal or exceed
its base: "$(28)_8$" and "$(102)_2$" are not numbers at all, because octal has
no digit 8 and binary has no digit 2.
:::

```photogrid label="15.H" cols="4" ratio="1.25" caption="People have always counted with a base. (a) A soroban, a Japanese abacus: each rod is one place of a decimal number. (b) Roman numerals on an alarm clock: I, V and X, a system without place value and without zero. (c) An old Nepali banknote with its number written in Devanagari numerals; our everyday decimal system is also written in many scripts. (d) A binary clock on a railway station, where lit lamps stand for 1 and dark ones for 0: a computer counts in base 2."
@ photo id="cs8/num-soroban" cap="(a) Soroban: decimal places"
@ photo id="cs8/num-roman-clock" cap="(b) Roman numerals"
@ photo id="cs8/num-nepali-note" cap="(c) Devanagari numerals"
@ photo id="cs8/num-binary-clock" cap="(d) A binary clock"
```

## 15.2 Converting decimal numbers to binary, octal and hexadecimal

To change a decimal number into another base, use **repeated division by the
new base**:

1. Divide the decimal number by the base (2, 8 or 16). Write the quotient below
   it and the remainder at the side.
2. Divide that quotient by the base again, and write the new quotient and
   remainder.
3. Repeat until the quotient becomes **0**.
4. Write the remainders from the **bottom to the top**. This is the answer.

Each division by the base splits off the last digit of the number in that base,
just as dividing 4725 by 10 leaves the remainder 5, its last digit. So the
**first remainder is the rightmost digit** and the **last remainder is the
leftmost digit** — which is why the remainders are read upwards.

::: example Worked example 15.1 — decimal to binary
**Problem.** Convert $(45)_{10}$ into binary.

**Solution.** Divide by 2 again and again, writing each remainder.

| Divide by 2 | Quotient | Remainder |
|---|---|---|
| 45 ÷ 2 | 22 | 1 |
| 22 ÷ 2 | 11 | 0 |
| 11 ÷ 2 | 5 | 1 |
| 5 ÷ 2 | 2 | 1 |
| 2 ÷ 2 | 1 | 0 |
| 1 ÷ 2 | 0 | 1 |

The quotient is now 0, so stop. Reading the remainders from the bottom up:
$(45)_{10} = (101101)_2$.

**Check.** $32 + 8 + 4 + 1 = 45$ ✓
:::

```figure caption="Converting 156 by repeated division in the short ladder form. Write the base on the left, each quotient under the number, and each remainder on the right; stop when the quotient is 0, then read the remainders upwards, as the arrows show. In base 16 the remainder 12 is written as the digit C."
fig, axs = plt.subplots(1, 3, figsize=(5.0, 3.3), gridspec_kw=dict(width_ratios=[1.25, 1, 1]))
D = "0123456789ABCDEF"
TOP = 9 * 0.62
for ax, b in zip(axs, (2, 8, 16)):
    rows = []
    m = 156
    while m > 0:
        rows.append((m, m % b)); m //= b
    rows.append((0, None))
    ax.set_xlim(0, 4.3); ax.set_ylim(-1.75, TOP + 0.5); ax.axis("off")
    for i, (q, r) in enumerate(rows):
        y = TOP - i * 0.62
        if r is not None:
            ax.text(0.45, y, str(b), ha="center", va="center", fontsize=8.6, color=INK)
            ax.plot([0.85, 0.85], [y - 0.27, y + 0.27], color=INK, lw=0.9)
            ax.plot([0.85, 2.3], [y - 0.3, y - 0.3], color=INK, lw=0.9)
        ax.text(1.58, y, str(q), ha="center", va="center", fontsize=8.6, color=INK)
        if r is not None:
            ax.text(2.7, y, D[r] if r < 10 else f"{r} = {D[r]}", ha="left", va="center", fontsize=8.6,
                    color=SERIES[1], fontweight="bold")
    ax.text(2.7, TOP + 0.5, "remainder", fontsize=6.9, color=MUTED, ha="left", va="center")
    ax.annotate("", xy=(4.15, TOP - 0.05), xytext=(4.15, TOP - (len(rows) - 2) * 0.62 + 0.05),
                arrowprops=dict(arrowstyle="-|>", color=SERIES[1], lw=1.1))
    s = "".join(D[r] for q, r in reversed(rows) if r is not None)
    ax.text(2.0, -0.7, f"divide by {b}", ha="center", va="center", fontsize=7.8, color=INK, fontweight="bold")
    ax.text(2.0, -1.35, f"$(156)_{{10}} = (\\mathrm{{{s}}})_{{{b}}}$", ha="center", va="center", fontsize=9.0, color=INK)
fig.subplots_adjust(wspace=0.05)
```

::: example Worked example 15.2 — one number, three bases
**Problem.** Convert $(156)_{10}$ into binary, octal and hexadecimal.

**Solution.** The three ladders are drawn in the figure above.

*Binary.* 156 ÷ 2 = 78 r 0; 78 ÷ 2 = 39 r 0; 39 ÷ 2 = 19 r 1; 19 ÷ 2 = 9 r 1;
9 ÷ 2 = 4 r 1; 4 ÷ 2 = 2 r 0; 2 ÷ 2 = 1 r 0; 1 ÷ 2 = 0 r 1. Reading upwards,
$(156)_{10} = (10011100)_2$.

*Octal.* 156 ÷ 8 = 19 r 4; 19 ÷ 8 = 2 r 3; 2 ÷ 8 = 0 r 2. Reading upwards,
$(156)_{10} = (234)_8$.

*Hexadecimal.* 156 ÷ 16 = 9 r 12; 9 ÷ 16 = 0 r 9. The remainder 12 is written
C, so $(156)_{10} = (\mathrm{9C})_{16}$.

**Check.** $128 + 16 + 8 + 4 = 156$ ✓; $2\times64 + 3\times8 + 4 = 156$ ✓;
$9\times16 + 12 = 156$ ✓
:::

::: example Worked example 15.3 — decimal to octal
**Problem.** Convert $(500)_{10}$ into octal.

**Solution.**

| Divide by 8 | Quotient | Remainder |
|---|---|---|
| 500 ÷ 8 | 62 | 4 |
| 62 ÷ 8 | 7 | 6 |
| 7 ÷ 8 | 0 | 7 |

Reading upwards: $(500)_{10} = (764)_8$.

**Check.** $7\times64 + 6\times8 + 4 = 448 + 48 + 4 = 500$ ✓
:::

::: example Worked example 15.4 — decimal to hexadecimal
**Problem.** Convert $(2024)_{10}$ into hexadecimal.

**Solution.**

| Divide by 16 | Quotient | Remainder | Hex digit |
|---|---|---|---|
| 2024 ÷ 16 | 126 | 8 | 8 |
| 126 ÷ 16 | 7 | 14 | E |
| 7 ÷ 16 | 0 | 7 | 7 |

Reading upwards: $(2024)_{10} = (\mathrm{7E8})_{16}$.

**Check.** $7\times256 + 14\times16 + 8 = 1792 + 224 + 8 = 2024$ ✓
:::

::: caution Three slips that cost marks
(1) Reading the remainders **downwards**. For 156 the remainders from top to
bottom are 0, 0, 1, 1, 1, 0, 0, 1; read downwards they give 00111001, which is
57, not the correct 10011100. Always read **from the bottom up**. (The
remainders of 45 happen to read the same both ways, so 45 is no test.)
(2) Forgetting the **last remainder**: when the quotient becomes 0, the number
you divided (often 1) is itself the last remainder. (3) Writing a
remainder of 10 to 15 as two digits in hexadecimal: 14 must be written **E**,
not "14", or the answer becomes a different number.
:::

::: tip Check every conversion
Convert your answer back to decimal by the method of section 15.3. It takes
thirty seconds and catches nearly every error. For binary there is also a quick
test: an **odd** number always ends in 1 and an **even** number in 0.
:::

### A second method for binary: subtracting place values

For binary there is a quick method that also checks the division method. Write
the place values 1, 2, 4, 8, 16, 32, 64, 128 … Take the **largest place value
that fits** into the number, write 1 under it and subtract; repeat with what is
left; write 0 under every place value that is not used.

::: example Worked example 15.5 — the parts of an IP address
**Problem.** Every part of an IPv4 address such as 192.168.1.10 (Lesson 14) is
stored in one byte. Convert (a) 200, (b) 192 and (c) 168 into 8-bit binary by
subtracting place values.

**Solution.** The place values of a byte are 128, 64, 32, 16, 8, 4, 2, 1.

(a) 200 − 128 = 72; 72 − 64 = 8; 8 − 8 = 0. The places 128, 64 and 8 are used:

| Place value | 128 | 64 | 32 | 16 | 8 | 4 | 2 | 1 |
|---|---|---|---|---|---|---|---|---|
| Bit | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 0 |

So $(200)_{10} = (11001000)_2$.

(b) 192 − 128 = 64; 64 − 64 = 0. Places 128 and 64:
$(192)_{10} = (11000000)_2$.

(c) 168 − 128 = 40; 40 − 32 = 8; 8 − 8 = 0. Places 128, 32 and 8:
$(168)_{10} = (10101000)_2$.

**Check.** Dividing 168 by 2 repeatedly gives the remainders 0, 0, 0, 1, 0, 1,
0, 1, which read upwards are 10101000 ✓
:::

## 15.3 Converting binary, octal and hexadecimal numbers to decimal

To change a number from any base into decimal, use **positional expansion**:

1. Write the **place value** under each digit, starting with 1 at the right and
   multiplying by the base for each place to the left. (The place values are
   the powers of the base: $\text{base}^0, \text{base}^1, \text{base}^2$ …)
2. Multiply each digit by its place value. In hexadecimal, change the letters A
   to F into 10 to 15 first.
3. Add the products. The sum is the number in decimal.

These are the place values you will need most often:

| Power | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Base 2 | 1 | 2 | 4 | 8 | 16 | 32 | 64 | 128 | 256 | 512 | 1024 |
| Base 8 | 1 | 8 | 64 | 512 | 4096 | | | | | | |
| Base 16 | 1 | 16 | 256 | 4096 | 65536 | | | | | | |

::: example Worked example 15.6 — binary to decimal by expansion
**Problem.** Convert $(110101)_2$ into decimal.

**Solution.** The rightmost digit has power 0; there are six digits, so the
leftmost has power 5.

$$(110101)_2 = 1\times2^5 + 1\times2^4 + 0\times2^3 + 1\times2^2 + 0\times2^1 + 1\times2^0$$

$$= 32 + 16 + 0 + 4 + 0 + 1 = (53)_{10}$$

**Check.** 53 is odd and the binary number ends in 1 ✓
:::

::: example Worked example 15.7 — binary to decimal with a place-value table
**Problem.** Convert $(10011011)_2$ into decimal.

**Solution.** Write the place values above the bits and add the place values
that have a 1 under them.

| Place value | 128 | 64 | 32 | 16 | 8 | 4 | 2 | 1 |
|---|---|---|---|---|---|---|---|---|
| Bit | 1 | 0 | 0 | 1 | 1 | 0 | 1 | 1 |

$128 + 16 + 8 + 2 + 1 = 155$, so $(10011011)_2 = (155)_{10}$.
:::

::: example Worked example 15.8 — octal to decimal
**Problem.** Convert $(1572)_8$ into decimal.

**Solution.**

$$(1572)_8 = 1\times8^3 + 5\times8^2 + 7\times8^1 + 2\times8^0$$

$$= 1\times512 + 5\times64 + 7\times8 + 2\times1 = 512 + 320 + 56 + 2 = (890)_{10}$$
:::

::: example Worked example 15.9 — hexadecimal to decimal
**Problem.** Convert $(\mathrm{3AF})_{16}$ into decimal.

**Solution.** Replace the letters first: A = 10 and F = 15.

$$(\mathrm{3AF})_{16} = 3\times16^2 + 10\times16^1 + 15\times16^0$$

$$= 3\times256 + 10\times16 + 15\times1 = 768 + 160 + 15 = (943)_{10}$$
:::

::: example Worked example 15.10 — a four-digit hexadecimal number
**Problem.** Convert $(\mathrm{BEAD})_{16}$ into decimal.

**Solution.** B = 11, E = 14, A = 10, D = 13, and the place values are 4096,
256, 16 and 1.

| Digit | B = 11 | E = 14 | A = 10 | D = 13 |
|---|---|---|---|---|
| Place value | 4096 | 256 | 16 | 1 |
| Product | 45056 | 3584 | 160 | 13 |

$45056 + 3584 + 160 + 13 = 48813$, so $(\mathrm{BEAD})_{16} = (48813)_{10}$.
:::

::: example Worked example 15.11 — reading a colour code
**Problem.** In a web page (Lesson 10) the colour orange is written `#FFA500`.
The six hex digits are three pairs, giving the amounts of red, green and blue
light, each from 0 to 255. Find the three amounts in decimal.

**Solution.** Red = $(\mathrm{FF})_{16} = 15\times16 + 15 = 255$.
Green = $(\mathrm{A5})_{16} = 10\times16 + 5 = 165$.
Blue = $(00)_{16} = 0$.

So `#FFA500` means red 255, green 165, blue 0: full red with some green, which
the eye sees as orange.
:::

::: caution The powers start at 0
The rightmost digit is multiplied by $\text{base}^0 = 1$, not by the base. A
student who starts with $2^1$ for $(110101)_2$ gets 106, exactly double the
right answer. Count the digits first: a number with $n$ digits has its leftmost
digit multiplied by $\text{base}^{\,n-1}$.
:::

## 15.4 Converting between binary, octal and hexadecimal

Since $8 = 2^3$, every octal digit is exactly **3 bits**; since $16 = 2^4$,
every hexadecimal digit is exactly **4 bits**. So these conversions need no
division at all — only grouping, using the two tables below.

| Octal digit | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| 3 bits | 000 | 001 | 010 | 011 | 100 | 101 | 110 | 111 |

| Hex digit | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| 4 bits | 0000 | 0001 | 0010 | 0011 | 0100 | 0101 | 0110 | 0111 |
| **Hex digit** | **8** | **9** | **A** | **B** | **C** | **D** | **E** | **F** |
| **4 bits** | **1000** | **1001** | **1010** | **1011** | **1100** | **1101** | **1110** | **1111** |

Why does grouping work? Look at the place values of binary in threes from the
right: 1, 2, 4 | 8, 16, 32 | 64, 128, 256. Each group of three is worth 1, 8 or
64 times the same pattern 1, 2, 4 — and 1, 8 and 64 are exactly the place
values of octal. So each group of three bits, read as a number from 0 to 7, is
one octal digit in the right place. In the same way, groups of four bits are
worth 1, 16, 256 … times a number from 0 to 15: the hexadecimal digits.

**Binary to octal.** Starting from the **right**, cut the bits into groups of
three. If the last group on the left is short, add 0s on its left. Write the
octal digit for each group.

**Binary to hexadecimal.** The same, with groups of **four**.

```figure caption="Grouping the bits of $(1101011010)_2$. Groups are always made from the right; the red 0s are added on the left only to fill the last group. Each group of three bits gives one octal digit, and each group of four gives one hexadecimal digit."
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(5.0, 2.9))
ax.set_xlim(0, 10); ax.set_ylim(0, 6.0); ax.axis("off")
bits = "1101011010"
def row(y, group, pad_to, title, digits, result):
    padded = bits.rjust(pad_to, "0")
    npad = pad_to - len(bits)
    w = 0.5
    x0 = 5.0 - pad_to * w / 2
    ax.text(0.0, y + 1.25, title, fontsize=7.8, color=INK, fontweight="bold", va="center")
    for k, b in enumerate(padded):
        x = x0 + k * w
        pad = k < npad
        ax.add_patch(Rectangle((x, y + 0.45), w - 0.04, 0.5, fc="#fde8e7" if pad else "#e8f1fb",
                               ec=SERIES[1] if pad else ACCENT, lw=0.9))
        ax.text(x + (w - 0.04) / 2, y + 0.7, b, ha="center", va="center", fontsize=9,
                color=SERIES[1] if pad else INK, fontweight="bold")
    for g in range(pad_to // group):
        xa = x0 + g * group * w + 0.03
        xb = x0 + (g + 1) * group * w - 0.07
        ax.plot([xa, xa, xb, xb], [y + 0.35, y + 0.25, y + 0.25, y + 0.35], color=INK, lw=0.9)
        ax.text((xa + xb) / 2, y - 0.1, digits[g], ha="center", va="center", fontsize=9.5, color=SERIES[2],
                fontweight="bold")
    ax.text(x0 + pad_to * w + 0.35, y + 0.2, result, fontsize=9, color=INK, va="center")
row(3.4, 3, 12, "In threes from the right → octal (8 = 2³)", "1532", "$= (1532)_8$")
row(0.4, 4, 12, "In fours from the right → hexadecimal (16 = 2⁴)", "35A", "$= (\\mathrm{35A})_{16}$")
ax.text(10.0, 5.6, "red 0 = zero added on the left", fontsize=7.0, color=SERIES[1], ha="right", va="center")
```

::: example Worked example 15.12 — binary to octal and hexadecimal
**Problem.** Convert $(1101011010)_2$ into octal and into hexadecimal.

**Solution.** *Octal:* groups of three from the right are 1 | 101 | 011 | 010.
Fill the last group: 001 | 101 | 011 | 010 → 1, 5, 3, 2. So
$(1101011010)_2 = (1532)_8$.

*Hexadecimal:* groups of four from the right are 11 | 0101 | 1010. Fill the
last group: 0011 | 0101 | 1010 → 3, 5, A. So
$(1101011010)_2 = (\mathrm{35A})_{16}$.

**Check.** The binary number is $512 + 256 + 64 + 16 + 8 + 2 = 858$;
$(1532)_8 = 512 + 320 + 24 + 2 = 858$ ✓ and
$(\mathrm{35A})_{16} = 768 + 80 + 10 = 858$ ✓
:::

**Octal to binary.** Replace **each** octal digit by its **three** bits, keeping
any 0s inside a group. **Hexadecimal to binary.** Replace each hex digit by its
**four** bits. Zeros at the far left of the final answer may be dropped.

::: example Worked example 15.13 — octal to binary
**Problem.** Convert $(5274)_8$ into binary.

**Solution.**

| Octal digit | 5 | 2 | 7 | 4 |
|---|---|---|---|---|
| 3 bits | 101 | 010 | 111 | 100 |

Joining the groups: $(5274)_8 = (101010111100)_2$. Note that 2 is written
**010**, not 10: dropping that 0 would shift every bit after it.
:::

::: example Worked example 15.14 — hexadecimal to binary
**Problem.** Convert (a) $(\mathrm{9C4})_{16}$ and (b) $(\mathrm{2F})_{16}$ into binary.

**Solution.** (a) 9 = 1001, C = 1100, 4 = 0100, so
$(\mathrm{9C4})_{16} = (100111000100)_2$.

(b) 2 = 0010, F = 1111, giving 00101111. The two 0s at the far left can be
dropped: $(\mathrm{2F})_{16} = (101111)_2$.

**Check (b).** $(\mathrm{2F})_{16} = 2\times16 + 15 = 47$ and
$(101111)_2 = 32 + 8 + 4 + 2 + 1 = 47$ ✓
:::

::: example Worked example 15.15 — a MAC address in binary
**Problem.** A network card has the MAC address `3C-52-82-9A-7F-10` (Lesson 14).
(a) How many bits long is the address? (b) Write the pairs 3C and 9A in binary
and in decimal.

**Solution.** (a) There are 12 hexadecimal digits and each is 4 bits, so the
address has 12 × 4 = **48 bits** (6 bytes, one byte per pair).

(b) 3C: 3 = 0011 and C = 1100, so $(\mathrm{3C})_{16} = (00111100)_2$, which is
32 + 16 + 8 + 4 = **60**. 9A: 9 = 1001 and A = 1010, so
$(\mathrm{9A})_{16} = (10011010)_2$, which is 128 + 16 + 8 + 2 = **154**
(check: 9 × 16 + 10 = 154 ✓).
:::

**Octal to hexadecimal, and back.** There is no direct rule, because 8 and 16
are not powers of each other. Go **through binary**: write each octal digit as
3 bits, then regroup the bits in fours from the right (or the reverse).

::: example Worked example 15.16 — octal to hexadecimal
**Problem.** Convert $(745)_8$ into hexadecimal.

**Solution.** *Step 1 — octal to binary:* 7 = 111, 4 = 100, 5 = 101, so
$(745)_8 = (111100101)_2$.

*Step 2 — regroup in fours from the right:* 1 | 1110 | 0101 → 0001 | 1110 | 0101
→ 1, E, 5.

So $(745)_8 = (\mathrm{1E5})_{16}$.

**Check.** $(745)_8 = 7\times64 + 4\times8 + 5 = 485$ and
$(\mathrm{1E5})_{16} = 256 + 14\times16 + 5 = 485$ ✓
:::

::: example Worked example 15.17 — hexadecimal to octal
**Problem.** Convert $(\mathrm{B6})_{16}$ into octal.

**Solution.** *Step 1 — hex to binary:* B = 1011, 6 = 0110, so
$(\mathrm{B6})_{16} = (10110110)_2$.

*Step 2 — regroup in threes from the right:* 10 | 110 | 110 → 010 | 110 | 110
→ 2, 6, 6.

So $(\mathrm{B6})_{16} = (266)_8$.

**Check.** $(\mathrm{B6})_{16} = 11\times16 + 6 = 182$ and
$(266)_8 = 2\times64 + 6\times8 + 6 = 182$ ✓
:::

::: caution Group from the right, never from the left
Grouping $(1101011010)_2$ in threes from the **left** gives 110 | 101 | 101 | 0,
which leads to the wrong answer 6550. The groups must start at the **right**
end, where the place worth 1 is; the extra 0s go only at the **left**.
:::

```figure caption="Which method to use for each conversion. Between decimal and the other three systems, divide (going down) or multiply by place values and add (going up); between binary and octal or hexadecimal, regroup the bits; between octal and hexadecimal, pass through binary."
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.0, 3.0))
ax.set_xlim(0, 10); ax.set_ylim(0, 6.0); ax.axis("off")
def box(x, y, t, c, w=2.3):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - 0.38), w, 0.76, boxstyle="round,pad=0.03,rounding_size=0.15",
                                fc=c, ec="none", alpha=0.92))
    ax.text(x, y, t, ha="center", va="center", fontsize=8.4, color="white", fontweight="bold")
def arr(p, q, c, style="-|>"):
    ax.annotate("", xy=q, xytext=p, arrowprops=dict(arrowstyle=style, color=c, lw=1.3, shrinkA=1, shrinkB=1))
box(5.0, 4.55, "DECIMAL", SERIES[0], 2.6)
box(1.5, 1.6, "OCTAL", SERIES[2])
box(5.0, 1.6, "BINARY", SERIES[1])
box(8.5, 1.6, "HEXADECIMAL", SERIES[3])
for x in (1.5, 5.0, 8.5):
    dx = (x - 5.0) * 0.12
    arr((4.75 + dx, 4.15), (x - 0.25, 2.02), SERIES[0])
    arr((x + 0.25, 2.02), (5.25 + dx, 4.15), SERIES[1])
ax.text(0.0, 5.75, "blue ↓  divide by 2, 8 or 16; read the remainders upwards", fontsize=7.2, color=SERIES[0], va="center")
ax.text(0.0, 5.35, "red ↑  multiply each digit by its place value; add", fontsize=7.2, color=SERIES[1], va="center")
arr((2.7, 1.6), (3.8, 1.6), SERIES[2], "<|-|>")
arr((6.2, 1.6), (7.3, 1.6), SERIES[3], "<|-|>")
ax.text(3.25, 0.92, "3 bits =\n1 octal digit", ha="center", va="center", fontsize=7.0, color=SERIES[2])
ax.text(6.75, 0.92, "4 bits =\n1 hex digit", ha="center", va="center", fontsize=7.0, color="#8a6508")
ax.text(5.0, 0.2, "octal ↔ hexadecimal: always go through binary", ha="center", va="center", fontsize=7.2, color=INK)
```

::: note Activity 15.1 — check your answers with the computer
Open the **Calculator** on a Windows computer and choose **Programmer** from its
menu. Type a decimal number such as 156: the calculator shows it at once in
HEX, DEC, OCT and BIN. Click HEX, OCT or BIN to type a number in that base
instead. Do five conversions from this lesson by hand first, then check each
one on the calculator. (Phones have similar "programmer calculator" apps.)
:::

::: note The same in Python
The grade 9–10 course uses Python, which has these conversions built in.
`bin()`, `oct()` and `hex()` change a decimal number, adding the prefixes `0b`,
`0o` and `0x`; `int(text, base)` changes a number written in another base back
to decimal.

```python
print(bin(45))
print(oct(500))
print(hex(2024))
print(int("110101", 2))
print(int("1572", 8))
print(int("3AF", 16))
print(format(156, "b"), format(156, "o"), format(156, "X"))
```

```text
0b101101
0o764
0x7e8
53
890
943
10011100 234 9C
```
:::

## 15.5 Bits, bytes and the units of memory

::: definition Bit, nibble and byte
A **bit** (*b*inary dig*it*) is a single 0 or 1 — the smallest unit of data in a
computer. A group of **4 bits** is a **nibble**. A group of **8 bits** is a
**byte**, the basic unit in which memory and storage are measured.
:::

One byte stores one character in the ASCII code used by English text: the
letter A is the number 65, stored as the byte 01000001. So the word NEPAL needs
5 bytes, which is 40 bits. Nepali letters are not in ASCII; they are stored in
**Unicode**, and in UTF-8, the form used on the web, a Devanagari character such as
क takes 3 bytes. The word नेपाल is stored as five characters (न, े, प, ा, ल),
so it takes 15 bytes. With $n$ bits a computer can make $2^n$ different
patterns: one byte (8 bits) has $2^8 = 256$ patterns, the numbers 0 to 255. The
largest byte, $(11111111)_2$, is 255, which is $(377)_8$ and $(\mathrm{FF})_{16}$ —
the FF of a colour code. The number of bits a processor handles at one time is
called its **word length**: a "64-bit processor" works on 64 bits at once.

Bigger units are made by multiplying by **1024**, not 1000, because computers
count in powers of 2, and $2^{10} = 1024$ is the power of 2 nearest to a
thousand.

| Unit | Symbol | Equal to | In bytes |
|---|---|---|---|
| Bit | b | a single 0 or 1 | — |
| Nibble | — | 4 bits | half a byte |
| Byte | B | 8 bits | 1 |
| Kilobyte | KB | 1024 bytes | $2^{10}$ = 1,024 |
| Megabyte | MB | 1024 KB | $2^{20}$ = 1,048,576 |
| Gigabyte | GB | 1024 MB | $2^{30}$ = 1,073,741,824 |
| Terabyte | TB | 1024 GB | $2^{40}$ |
| Petabyte | PB | 1024 TB | $2^{50}$ |
| Exabyte | EB | 1024 PB | $2^{60}$ |
| Zettabyte | ZB | 1024 EB | $2^{70}$ |
| Yottabyte | YB | 1024 ZB | $2^{80}$ |

```figure caption="The ladder of memory units. From the byte upwards each unit is 1024 times the one below it. The grey notes give a feel for each size."
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.0, 4.4))
ax.set_xlim(0, 10); ax.set_ylim(-0.1, 11.1); ax.axis("off")
units = [("bit", "a single 0 or 1"), ("nibble", "= 4 bits"), ("byte (B)", "= 8 bits"),
         ("kilobyte (KB)", "= 1024 bytes"), ("megabyte (MB)", "= 1024 KB"), ("gigabyte (GB)", "= 1024 MB"),
         ("terabyte (TB)", "= 1024 GB"), ("petabyte (PB)", "= 1024 TB"), ("exabyte (EB)", "= 1024 PB"),
         ("zettabyte (ZB)", "= 1024 EB"), ("yottabyte (YB)", "= 1024 ZB")]
examples = {2: "one letter, such as A", 3: "a short text message: under 1 KB", 4: "a phone photo: about 3 MB",
            5: "a two-hour film: about 2 GB", 6: "a laptop's hard disk: about 1 TB",
            7: "a large data centre: many PB", 9: "EB, ZB and YB measure the data of"}
for i, (u, rel) in enumerate(units):
    col = SERIES[0] if i < 3 else (SERIES[2] if i < 7 else SERIES[4])
    ax.add_patch(FancyBboxPatch((0.1, i + 0.12), 2.7, 0.72, boxstyle="round,pad=0.02,rounding_size=0.12",
                                fc=col, ec="none", alpha=0.9))
    ax.text(1.45, i + 0.48, u, ha="center", va="center", fontsize=7.8, color="white", fontweight="bold")
    ax.text(3.05, i + 0.48, rel, ha="left", va="center", fontsize=7.6, color=INK)
    if i in examples:
        ax.text(5.6, i + 0.48, examples[i], ha="left", va="center", fontsize=7.2, color=MUTED)
ax.text(5.6, 9.05, "whole countries and of the Internet", ha="left", va="center", fontsize=7.2, color=MUTED)
```

::: note Why a "1 TB" disk shows about 931 GB
Makers of hard disks and pen drives, and network speeds (Lesson 14), use the
decimal meaning: 1 KB = 1000 bytes, 1 GB = 1,000,000,000 bytes and 1 TB =
1,000,000,000,000 bytes. A computer divides by 1024 at each step, so a "1 TB"
disk appears as $10^{12} \div 1024^3 \approx 931$ GB. Nothing is missing; the
two numbers use different units. Scientists now write KiB, MiB and GiB for the
1024 units, and you may see these in some programs. For computer memory, **1 KB = 1024 bytes**.
:::

::: example Worked example 15.18 — changing memory units
**Problem.** Convert (a) 5 bytes into bits; (b) 3 KB into bytes; (c) 2 MB into
bytes; (d) 4096 MB into GB; (e) 3 GB into KB.

**Solution.** Going to a smaller unit, multiply; going to a larger unit,
divide.

(a) 5 bytes = 5 × 8 = **40 bits**.

(b) 3 KB = 3 × 1024 = **3,072 bytes**.

(c) 2 MB = 2 × 1024 KB = 2,048 KB = 2,048 × 1024 = **2,097,152 bytes**.

(d) 4096 MB = 4096 ÷ 1024 = **4 GB**.

(e) 3 GB = 3 × 1024 MB = 3,072 MB = 3,072 × 1024 = **3,145,728 KB**.
:::

::: example Worked example 15.19 — how many photos will fit?
**Problem.** Sushma's phone takes photos of 4 MB each. How many photos can a
64 GB memory card hold? (Ignore the space taken by the card's own system
files.)

**Solution.** 64 GB = 64 × 1024 MB = 65,536 MB.

Number of photos = 65,536 ÷ 4 = **16,384 photos**.
:::

::: example Worked example 15.20 — the size of a typed essay
**Problem.** An essay has 2,000 words. On average a word, with the space after
it, takes 6 characters. Find its size in bytes and in KB, taking 1 byte per
character.

**Solution.** Characters = 2,000 × 6 = 12,000, so the size is **12,000 bytes**.
In KB: 12,000 ÷ 1024 ≈ **11.7 KB**. A whole essay is smaller than one photo, which
is why text messages and emails are so quick to send.
:::

::: example Worked example 15.21 — how many bits are needed?
**Problem.** (a) What is the largest number that can be written with 10 bits?
(b) How many bits are needed to write 1000 in binary? (c) And 5000?

**Solution.** $n$ bits make $2^n$ patterns, the numbers from 0 to $2^n - 1$.

(a) $2^{10} - 1 = 1024 - 1 = 1023$, which is ten 1s: $(1111111111)_2$.

(b) $2^9 = 512$ is less than 1000, but $2^{10} = 1024$ is more, so 1000 needs
**10 bits**. Indeed $(1000)_{10} = (1111101000)_2$, which has 10 digits.

(c) $2^{12} = 4096$ is less than 5000 and $2^{13} = 8192$ is more, so 5000 needs
**13 bits**: $(5000)_{10} = (1001110001000)_2$.
:::

::: note Activity 15.2 — binary cards
Cut five cards. On their fronts draw 16, 8, 4, 2 and 1 dots, and lay them in a
row with 16 on the left. A card turned face up means 1 and face down means 0.
(1) Show 9: only the 8 and the 1 are up, so 9 = 01001. (2) Show 21, 30 and 31.
(3) What is the largest number five cards can show, and how many different
numbers (counting 0) can they make? (Answer: 31, and 32 numbers, because
$2^5 = 32$.) (4) Add a sixth card: how many dots must it have?
:::

## Chapter summary

- A **number system** writes numbers with a fixed set of digits; its **base**
  (radix) is the number of digits, and the largest digit is base − 1. Binary
  (2: 0, 1), octal (8: 0–7), decimal (10: 0–9), hexadecimal (16: 0–9, A–F with
  A = 10 … F = 15). Always write the base: $(101)_2$.
- All four are **positional**: place values are powers of the base, starting
  with $\text{base}^0 = 1$ at the right.
- Computers use **binary** because their switches have two states (off/on);
  octal (3 bits per digit) and hexadecimal (4 bits per digit) are short ways of
  writing binary — hex is used for colour codes and MAC addresses.
- **Decimal → any base:** divide by the base until the quotient is 0; read the
  remainders **from the bottom up**; write 10–15 as A–F.
- **Any base → decimal:** multiply each digit by its place value and add.
- **Binary → octal / hex:** group bits in **threes / fours from the right**,
  padding 0s on the left. **Octal / hex → binary:** write 3 / 4 bits for each
  digit. **Octal ↔ hex:** go through binary.
- **Memory:** bit; nibble = 4 bits; byte = 8 bits; KB, MB, GB, TB, PB, EB, ZB,
  YB, each **1024** times the one before. Disk makers and network speeds use
  1000.

## Practice questions

**Group A — Objective (1 mark each)**

1. The base of the hexadecimal number system is <span class="marks">[1]</span>
   (a) 2 (b) 8 (c) 10 (d) 16
2. Which digit is not used in the octal system? <span class="marks">[1]</span>
   (a) 0 (b) 5 (c) 7 (d) 8
3. $(1011)_2$ in decimal is <span class="marks">[1]</span>
   (a) 11 (b) 13 (c) 9 (d) 1011
4. $(25)_{10}$ in binary is <span class="marks">[1]</span>
   (a) 11001 (b) 10011 (c) 11010 (d) 10101
5. In hexadecimal, the symbol D stands for <span class="marks">[1]</span>
   (a) 11 (b) 12 (c) 13 (d) 14
6. How many bits make one byte? <span class="marks">[1]</span>
   (a) 4 (b) 8 (c) 16 (d) 1024
7. 1 KB is equal to <span class="marks">[1]</span>
   (a) 1000 bits (b) 1024 bits (c) 1024 bytes (d) 1000 MB
8. $(17)_8$ in decimal is <span class="marks">[1]</span>
   (a) 15 (b) 17 (c) 23 (d) 7
9. The binary equivalent of $(\mathrm{A})_{16}$ is <span class="marks">[1]</span>
   (a) 1010 (b) 1100 (c) 1001 (d) 1110
10. To convert a binary number into octal, its bits are grouped in <span class="marks">[1]</span>
    (a) twos (b) threes (c) fours (d) eights
11. Which of these units is the largest? <span class="marks">[1]</span>
    (a) TB (b) PB (c) GB (d) EB
12. $(64)_8$ in binary is <span class="marks">[1]</span>
    (a) 110100 (b) 1101111 (c) 1110001 (d) 11000101
13. $(\mathrm{FF})_{16}$ in decimal is <span class="marks">[1]</span>
    (a) 225 (b) 255 (c) 256 (d) 1515
14. A nibble is <span class="marks">[1]</span>
    (a) 2 bits (b) 4 bits (c) 8 bits (d) 16 bits

::: note Answers to Group A
**1.** (d) — hexadecimal uses 16 symbols, 0–9 and A–F.
**2.** (d) — octal digits run from 0 to 7.
**3.** (a) — 8 + 0 + 2 + 1 = 11.
**4.** (a) — 25 = 16 + 8 + 1, so the bits for 16, 8 and 1 are 1: 11001.
**5.** (c) — A = 10, B = 11, C = 12, D = 13.
**6.** (b) — a byte is 8 bits.
**7.** (c) — 1 KB = 1024 bytes ($2^{10}$).
**8.** (a) — 1 × 8 + 7 = 15.
**9.** (a) — A = 10 = 8 + 2 = 1010.
**10.** (b) — $8 = 2^3$, so each octal digit is 3 bits.
**11.** (d) — the order is GB, TB, PB, EB.
**12.** (a) — 6 = 110 and 4 = 100, giving 110100.
**13.** (b) — 15 × 16 + 15 = 255.
**14.** (b) — a nibble is half a byte, 4 bits.
:::

**Group B — Short answer (2 marks each)**

1. What is a number system? Define base (radix) with one example. <span class="marks">[2]</span>
2. Why do computers use the binary number system? <span class="marks">[2]</span>
3. Convert $(89)_{10}$ into binary. <span class="marks">[2]</span>
4. Convert $(11100110)_2$ into decimal. <span class="marks">[2]</span>
5. Convert $(726)_8$ into decimal. <span class="marks">[2]</span>
6. Convert $(1000)_{10}$ into hexadecimal. <span class="marks">[2]</span>
7. Convert $(\mathrm{2C9})_{16}$ into decimal. <span class="marks">[2]</span>
8. Convert $(1011101)_2$ into octal and hexadecimal. <span class="marks">[2]</span>
9. Convert 3 MB into KB and into bytes. <span class="marks">[2]</span>
10. Convert $(352)_8$ into hexadecimal. <span class="marks">[2]</span>
11. How many bits are there in 2 KB? Show the working. <span class="marks">[2]</span>
12. Find the decimal value of $(\mathrm{FFF})_{16}$, the largest three-digit hexadecimal number. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** A number system is a way of writing numbers with a fixed set of digits
and rules. Its base (radix) is the number of different digits it uses: binary
has base 2 (digits 0 and 1), and decimal has base 10 (digits 0 to 9).

**2.** A computer is made of electronic switches that have only two states, off
and on, which are easy to make and to tell apart; they are written as 0 and 1.
Storage also uses two states (magnetised one way or the other, charge or no
charge), so all data is stored and processed as binary digits.

**3.** 89 ÷ 2 = 44 r 1; 44 ÷ 2 = 22 r 0; 22 ÷ 2 = 11 r 0; 11 ÷ 2 = 5 r 1;
5 ÷ 2 = 2 r 1; 2 ÷ 2 = 1 r 0; 1 ÷ 2 = 0 r 1. Reading upwards,
$(89)_{10} = (1011001)_2$. Check: 64 + 16 + 8 + 1 = 89.

**4.** Place values 128, 64, 32, 16, 8, 4, 2, 1 over the bits 1 1 1 0 0 1 1 0:
128 + 64 + 32 + 4 + 2 = **230**, so $(11100110)_2 = (230)_{10}$.

**5.** $(726)_8 = 7\times8^2 + 2\times8^1 + 6\times8^0 = 448 + 16 + 6 = (470)_{10}$.

**6.** 1000 ÷ 16 = 62 r 8; 62 ÷ 16 = 3 r 14 (E); 3 ÷ 16 = 0 r 3. Reading upwards,
$(1000)_{10} = (\mathrm{3E8})_{16}$. Check: 3 × 256 + 14 × 16 + 8 = 1000.

**7.** C = 12, so $(\mathrm{2C9})_{16} = 2\times256 + 12\times16 + 9 = 512 + 192 + 9 = (713)_{10}$.

**8.** Octal: 1 | 011 | 101 → 001 | 011 | 101 → $(135)_8$. Hexadecimal:
101 | 1101 → 0101 | 1101 → 5, D → $(\mathrm{5D})_{16}$. Check: the binary number is
64 + 16 + 8 + 4 + 1 = 93, and 64 + 24 + 5 = 93, 80 + 13 = 93.

**9.** 3 MB = 3 × 1024 = **3,072 KB**; 3,072 × 1024 = **3,145,728 bytes**.

**10.** Through binary: 3 = 011, 5 = 101, 2 = 010, so $(352)_8 = (11101010)_2$.
In fours from the right: 1110 | 1010 → E, A. So $(352)_8 = (\mathrm{EA})_{16}$.
Check: 3 × 64 + 5 × 8 + 2 = 234 and 14 × 16 + 10 = 234.

**11.** 2 KB = 2 × 1024 = 2,048 bytes, and each byte is 8 bits, so
2,048 × 8 = **16,384 bits**.

**12.** F = 15, so $(\mathrm{FFF})_{16} = 15\times256 + 15\times16 + 15 = 3840 + 240 + 15 = (4095)_{10}$.
(This is $16^3 - 1$, one less than $(1000)_{16}$.)
:::

**Group C — Long answer (4 marks each)**

1. Convert as indicated: (a) $(175)_{10}$ into binary (b) $(1101101)_2$ into decimal (c) $(634)_8$ into decimal (d) $(\mathrm{4D})_{16}$ into binary. <span class="marks">[1+1+1+1]</span>
2. Convert $(420)_{10}$ into binary, octal and hexadecimal, and check one of your answers by converting it back. <span class="marks">[4]</span>
3. Why is each octal digit worth exactly 3 bits and each hexadecimal digit exactly 4 bits? Convert $(\mathrm{A7F})_{16}$ into octal through binary. <span class="marks">[1+3]</span>
4. (a) Write the units of memory from the bit to the yottabyte in order, with the relation between each pair. (b) A 32 GB memory card stores songs of 4 MB each. How many songs can it hold? (c) Why does a "1 TB" hard disk show only about 931 GB on a computer? <span class="marks">[2+1+1]</span>
5. Compare the binary, octal, decimal and hexadecimal systems in a table (base, digits, largest digit, one use). Write $(100)_{10}$ in each of the other three systems. <span class="marks">[2+2]</span>

::: note Answers to Group C
**1.** (a) 175 ÷ 2 = 87 r 1; 87 ÷ 2 = 43 r 1; 43 ÷ 2 = 21 r 1; 21 ÷ 2 = 10 r 1;
10 ÷ 2 = 5 r 0; 5 ÷ 2 = 2 r 1; 2 ÷ 2 = 1 r 0; 1 ÷ 2 = 0 r 1. Reading upwards,
$(175)_{10} = (10101111)_2$ (check: 128 + 32 + 8 + 4 + 2 + 1 = 175).
(b) $(1101101)_2 = 64 + 32 + 0 + 8 + 4 + 0 + 1 = (109)_{10}$.
(c) $(634)_8 = 6\times64 + 3\times8 + 4 = 384 + 24 + 4 = (412)_{10}$.
(d) 4 = 0100 and D = 1101, giving 01001101; dropping the leading 0,
$(\mathrm{4D})_{16} = (1001101)_2$.

**2.** *Binary:* 420 ÷ 2 = 210 r 0; 210 ÷ 2 = 105 r 0; 105 ÷ 2 = 52 r 1;
52 ÷ 2 = 26 r 0; 26 ÷ 2 = 13 r 0; 13 ÷ 2 = 6 r 1; 6 ÷ 2 = 3 r 0; 3 ÷ 2 = 1 r 1;
1 ÷ 2 = 0 r 1. Reading upwards, $(420)_{10} = (110100100)_2$.
*Octal:* 420 ÷ 8 = 52 r 4; 52 ÷ 8 = 6 r 4; 6 ÷ 8 = 0 r 6, so
$(420)_{10} = (644)_8$.
*Hexadecimal:* 420 ÷ 16 = 26 r 4; 26 ÷ 16 = 1 r 10 (A); 1 ÷ 16 = 0 r 1, so
$(420)_{10} = (\mathrm{1A4})_{16}$.
*Check:* $(644)_8 = 6\times64 + 4\times8 + 4 = 384 + 32 + 4 = 420$ ✓ (also
$(\mathrm{1A4})_{16} = 256 + 160 + 4 = 420$ and $256 + 128 + 32 + 4 = 420$).

**3.** $8 = 2^3$, so three bits make exactly the eight patterns 000 to 111, one
for each octal digit; $16 = 2^4$, so four bits make exactly the sixteen patterns
0000 to 1111, one for each hex digit (1 mark).
*Step 1 — hex to binary:* A = 1010, 7 = 0111, F = 1111, so
$(\mathrm{A7F})_{16} = (101001111111)_2$.
*Step 2 — regroup in threes from the right:* 101 | 001 | 111 | 111 → 5, 1, 7, 7.
So $(\mathrm{A7F})_{16} = (5177)_8$.
*Check:* $10\times256 + 7\times16 + 15 = 2687$ and
$5\times512 + 1\times64 + 7\times8 + 7 = 2687$ ✓

**4.** (a) 1 nibble = 4 bits; 1 byte = 8 bits; 1 KB = 1024 bytes; 1 MB = 1024 KB;
1 GB = 1024 MB; 1 TB = 1024 GB; 1 PB = 1024 TB; 1 EB = 1024 PB; 1 ZB = 1024 EB;
1 YB = 1024 ZB.
(b) 32 GB = 32 × 1024 = 32,768 MB; 32,768 ÷ 4 = **8,192 songs**.
(c) Disk makers count 1 TB as 1,000,000,000,000 bytes (powers of 1000), but
the computer divides by 1024 three times to show GB:
$10^{12} \div 1024^3 \approx 931$ GB. The disk is not smaller; the two figures
use different units.

**5.**

| System | Base | Digits | Largest digit | One use |
|---|---|---|---|---|
| Binary | 2 | 0, 1 | 1 | all data inside a computer |
| Octal | 8 | 0–7 | 7 | short form of binary; Linux file permissions |
| Decimal | 10 | 0–9 | 9 | everyday counting by people |
| Hexadecimal | 16 | 0–9, A–F | F (15) | colour codes, MAC addresses |

$(100)_{10}$: 100 ÷ 2 gives the remainders 0, 0, 1, 0, 0, 1, 1 (quotients 50,
25, 12, 6, 3, 1, 0), so $(100)_{10} = (1100100)_2$; 100 ÷ 8 = 12 r 4,
12 ÷ 8 = 1 r 4, 1 ÷ 8 = 0 r 1, so $(100)_{10} = (144)_8$; 100 ÷ 16 = 6 r 4,
6 ÷ 16 = 0 r 6, so $(100)_{10} = (64)_{16}$. Check: 64 + 32 + 4 = 100;
64 + 32 + 4 = 100; 6 × 16 + 4 = 100.
:::

**Group D — Extended answers (10 marks each, for deeper revision)**

1. Explain decimal, binary, octal and hexadecimal number systems. Why does a computer use binary? <span class="marks">[10]</span>
2. Convert numbers between decimal, binary, octal and hexadecimal with full working. <span class="marks">[10]</span>
3. Explain the units of computer memory and convert between binary, octal and hexadecimal directly. <span class="marks">[10]</span>

### Model answer D1: number systems (10 marks)

**Introduction.** A **number system** is a way of writing numbers using a fixed set of digits. The number of different digits is called the **base** (or radix). The value of a digit depends on its place, which is **positional value**: in 345 the 3 means 3 × 10² (Plate 15.H).

| System | Base | Digits used | Example | Where used |
|---|---|---|---|---|
| Decimal | 10 | 0 to 9 | 156 | Daily life |
| Binary | 2 | 0, 1 | 10011100 | Inside the computer |
| Octal | 8 | 0 to 7 | 234 | Short form of binary |
| Hexadecimal | 16 | 0 to 9 and A to F | 9C | Colours, memory addresses |

In hexadecimal, A = 10, B = 11, C = 12, D = 13, E = 14 and F = 15.

**The same number in four systems.** Decimal 156 = binary 10011100 = octal 234 = hexadecimal 9C.

**Why does a computer use binary?**

1. A computer is made of switches and transistors that have two states: on (1) and off (0).
2. Two states are easy and cheap to build and are very reliable, because a small change in voltage does not confuse 0 with 1.
3. Binary matches Boolean logic (true and false), the basis of all calculation in a computer.
4. Any data, such as text, picture and sound, can be stored as a string of 0s and 1s.

**Why octal and hexadecimal?** Long binary numbers are hard to read and to write without mistakes. One octal digit stands for 3 bits and one hexadecimal digit for 4 bits, so they are a short form of binary.

**Conclusion.** Humans use the decimal system, the computer uses binary, and octal and hexadecimal are convenient short forms of binary.

### Model answer D2: conversions with working (10 marks)

**Introduction.** To convert from decimal, we divide again and again by the new base and read the remainders upwards. To convert to decimal, we multiply each digit by its place value and add.

**(a) Decimal 156 to binary.**

| Divide | Quotient | Remainder |
|---|---|---|
| 156 ÷ 2 | 78 | 0 |
| 78 ÷ 2 | 39 | 0 |
| 39 ÷ 2 | 19 | 1 |
| 19 ÷ 2 | 9 | 1 |
| 9 ÷ 2 | 4 | 1 |
| 4 ÷ 2 | 2 | 0 |
| 2 ÷ 2 | 1 | 0 |
| 1 ÷ 2 | 0 | 1 |

Reading the remainders from the bottom up: **(156)₁₀ = (10011100)₂**.

**(b) Decimal 156 to octal and hexadecimal.** 156 ÷ 8 = 19 remainder 4; 19 ÷ 8 = 2 remainder 3; 2 ÷ 8 = 0 remainder 2. So **(156)₁₀ = (234)₈**. Again, 156 ÷ 16 = 9 remainder 12 (C); 9 ÷ 16 = 0 remainder 9. So **(156)₁₀ = (9C)₁₆**.

**(c) Binary 1101011 to decimal.** 1×2⁶ + 1×2⁵ + 0×2⁴ + 1×2³ + 0×2² + 1×2¹ + 1×2⁰ = 64 + 32 + 0 + 8 + 0 + 2 + 1 = **107**.

**(d) Octal 725 to decimal.** 7×8² + 2×8¹ + 5×8⁰ = 448 + 16 + 5 = **469**.

**(e) Hexadecimal 2F5 to decimal.** 2×16² + 15×16¹ + 5×16⁰ = 512 + 240 + 5 = **757**.

**(f) Decimal 45 to binary.** 45 ÷ 2 = 22 r 1; 22 ÷ 2 = 11 r 0; 11 ÷ 2 = 5 r 1; 5 ÷ 2 = 2 r 1; 2 ÷ 2 = 1 r 0; 1 ÷ 2 = 0 r 1. Upwards: **101101**. Check: 32 + 8 + 4 + 1 = 45.

**Conclusion.** Division by the base and reading the remainders upwards gives the converted number, and multiplying by place values brings it back to decimal. Always check the answer by converting back.

### Model answer D3: units of memory and direct conversion (10 marks)

**Introduction.** A **bit** (binary digit) is the smallest unit of data, 0 or 1. A **byte** is a group of 8 bits and can store one character. Memory is measured in bytes.

| Unit | Short | Size |
|---|---|---|
| Bit | b | 0 or 1 |
| Nibble | | 4 bits |
| Byte | B | 8 bits |
| Kilobyte | KB | 1024 bytes |
| Megabyte | MB | 1024 KB |
| Gigabyte | GB | 1024 MB |
| Terabyte | TB | 1024 GB |

**Example.** A 4 GB pen drive holds 4 × 1024 = 4096 MB. If a photo is 3 MB, about 4096 ÷ 3 = 1365 photos fit in it. A 3 MB photo is 3 × 1024 = 3072 KB.

**Binary to octal (group in 3 bits from the right).** Convert 101110011: group 101 | 110 | 011 = 5, 6, 3, so **(101110011)₂ = (563)₈**.

**Binary to hexadecimal (group in 4 bits from the right).** The same number: 1 | 0111 | 0011, padding the left as 0001 | 0111 | 0011 = 1, 7, 3, so **(101110011)₂ = (173)₁₆**.

**Hexadecimal to binary (write 4 bits for each digit).** B7: B = 1011, 7 = 0111, so **(B7)₁₆ = (10110111)₂**, which is 183 in decimal.

**Octal to binary (write 3 bits for each digit).** 234 → 010 | 011 | 100, so **(234)₈ = (10011100)₂**.

| Binary | Octal | Hexadecimal |
|---|---|---|
| 101110011 | 563 | 173 |
| 11110000 | 360 | F0 |
| 10110111 | 267 | B7 |

**Binary addition rules.** 0 + 0 = 0, 0 + 1 = 1, 1 + 0 = 1, 1 + 1 = 10 (0 carry 1), and 1 + 1 + 1 = 11. For example, 1101 (13) + 0111 (7) = 10100 (20).

**Conclusion.** Memory is counted in powers of 1024, and the grouping of 3 or 4 bits gives a quick path between binary, octal and hexadecimal.
