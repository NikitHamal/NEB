---
subject: Computer Science
grade: 11
unit: 2
title: Number System and Boolean Logic
hours: 11
---

Inside a computer there are only two voltages, so there are only two symbols:
0 and 1. Everything else — your name, a photograph, a song, this sentence — is a
pattern of those two symbols. This unit teaches you to move between the number
systems people use and the one machines use, to do arithmetic in binary, and then
to describe and simplify the switching circuits that carry out that arithmetic.
It is the most *mechanical* unit in the course: almost every mark is earned by
applying a procedure correctly, so practise until the procedures are automatic.

::: key What the examiner wants from this unit
Conversions and complement subtraction are guaranteed marks — show every step of
the division/multiplication and keep the digits in the right order. Logic gates
appear every year: know all seven **symbols**, **truth tables** and **Boolean
functions**. De Morgan's theorems are usually asked as "state and verify using a
truth table" — draw the full table, do not just assert the result.
:::

## 2.1 Decimal, Binary, Octal and Hexadecimal number systems and conversion

A **number system** is a way of writing numbers using a fixed set of symbols.
The number of distinct symbols is the **base** (or **radix**) $r$. All four
systems in the syllabus are **positional**: the value of a digit depends on where
it stands.

$$ N = d_{n-1}r^{\,n-1} + \cdots + d_1r^{1} + d_0r^{0}
+ d_{-1}r^{-1} + d_{-2}r^{-2} + \cdots $$

| System | Base | Digits used | Example | Where used |
|---|---|---|---|---|
| Decimal | 10 | 0–9 | $(725)_{10}$ | everyday human counting |
| Binary | 2 | 0, 1 | $(1011)_{2}$ | internal machine representation |
| Octal | 8 | 0–7 | $(736)_{8}$ | shorthand for binary (3 bits per digit) |
| Hexadecimal | 16 | 0–9, A–F | $(2AF)_{16}$ | memory addresses, colour codes, MAC addresses |

In hexadecimal A = 10, B = 11, C = 12, D = 13, E = 14, F = 15.

```figure caption="The three conversion methods. Everything reduces to positional expansion (to decimal), repeated division or multiplication (from decimal), and grouping of bits (between binary, octal and hexadecimal)."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.1,3.1))
GRN='#2e8b57'; RED='#A8271F'
def box(cx,cy,w,h,t,c,fs=8.8):
    ax.add_patch(FancyBboxPatch((cx-w/2,cy-h/2),w,h,
        boxstyle="round,pad=0.02,rounding_size=0.10",fc=c,ec=c,lw=1.2,alpha=0.16,zorder=2))
    ax.add_patch(FancyBboxPatch((cx-w/2,cy-h/2),w,h,
        boxstyle="round,pad=0.02,rounding_size=0.10",fc='none',ec=c,lw=1.2,zorder=3))
    ax.text(cx,cy,t,ha='center',va='center',fontsize=fs,color=INK,zorder=4)
def arw(p,q,c,ls='-'):
    ax.annotate('',xy=q,xytext=p,zorder=2,
        arrowprops=dict(arrowstyle='-|>',color=c,lw=1.3,linestyle=ls,
                        shrinkA=3,shrinkB=3,mutation_scale=11))
box(1.55,2.45,1.65,0.62,'DECIMAL',ACCENT,9.2)
box(1.55,0.35,1.65,0.62,'BINARY',RED,9.2)
box(4.45,1.95,1.40,0.56,'OCTAL',GRN)
box(4.45,0.35,1.40,0.56,'HEX',GRN)
arw((1.10,2.14),(1.10,0.66),ACCENT)
ax.text(0.95,1.40,'repeated ÷ (integer)\nrepeated × (fraction)',ha='right',va='center',
        fontsize=7.4,color=ACCENT)
arw((2.00,0.66),(2.00,2.14),RED)
ax.text(2.13,1.28,'positional expansion',rotation=90,ha='left',va='center',
        fontsize=7.0,color=RED)
arw((2.42,2.32),(3.74,2.06),GRN)
ax.text(3.10,2.42,'÷ 8  /  ÷ 16',ha='center',va='bottom',fontsize=7.4,color=GRN)
arw((2.52,0.62),(3.74,1.74),GRN)
ax.text(3.32,0.92,'group 3 bits',ha='left',va='center',fontsize=7.4,color=GRN)
arw((2.42,0.35),(3.74,0.35),GRN)
ax.text(3.08,0.48,'group 4 bits',ha='center',va='bottom',fontsize=7.4,color=GRN)
ax.text(4.45,-0.30,'octal ↔ hex: always\ngo through binary',ha='center',va='top',
        fontsize=7.8,color=MUTED)
ax.set_xlim(-1.35,5.60); ax.set_ylim(-1.05,3.05); ax.axis('off')
```

### Any base → decimal: positional expansion

Multiply each digit by the base raised to its position weight and add.

::: example Worked example 2.1 — to decimal
**Problem.** Convert $(110110)_2$, $(736)_8$ and $(2AF)_{16}$ to decimal.

**Solution.**

$$ (110110)_2 = 1(2^5)+1(2^4)+0(2^3)+1(2^2)+1(2^1)+0(2^0) = 32+16+4+2 = (54)_{10} $$

$$ (736)_8 = 7(8^2)+3(8^1)+6(8^0) = 448+24+6 = (478)_{10} $$

$$ (2AF)_{16} = 2(16^2)+10(16^1)+15(16^0) = 512+160+15 = (687)_{10} $$
:::

Fractions use negative powers: $(11011.101)_2 = 16+8+2+1 + \frac12 + \frac18
= 27.625$.

### Decimal → any base: repeated division and multiplication

For the **integer part**, divide repeatedly by the base and read the remainders
**bottom to top**. For the **fraction part**, multiply repeatedly by the base and
read the carried integers **top to bottom**.

::: example Worked example 2.2 — decimal to binary, octal and hex
**Problem.** Convert $(185)_{10}$ to binary, octal and hexadecimal.

**Solution.** Divide by 2:

| ÷2 | Quotient | Remainder |
|---|---|---|
| 185 | 92 | **1** |
| 92 | 46 | **0** |
| 46 | 23 | **0** |
| 23 | 11 | **1** |
| 11 | 5 | **1** |
| 5 | 2 | **1** |
| 2 | 1 | **0** |
| 1 | 0 | **1** |

Reading upwards, $(185)_{10} = (10111001)_2$.

Divide by 8: $185 \div 8 = 23$ r **1**; $23 \div 8 = 2$ r **7**; $2 \div 8 = 0$
r **2**. So $(185)_{10} = (271)_8$.

Divide by 16: $185 \div 16 = 11$ r **9**; $11 \div 16 = 0$ r **11 = B**. So
$(185)_{10} = (B9)_{16}$.

**Check:** $2(64)+7(8)+1 = 185$ ✓ and $11(16)+9 = 185$ ✓
:::

::: example Worked example 2.3 — a decimal fraction
**Problem.** Convert $(0.6875)_{10}$ to binary, and $(13.75)_{10}$ to binary.

**Solution.** Multiply the fraction by 2 each time and take the integer carried
out:

| Step | Product | Integer part |
|---|---|---|
| $0.6875\times2$ | 1.375 | **1** |
| $0.375\times2$ | 0.75 | **0** |
| $0.75\times2$ | 1.5 | **1** |
| $0.5\times2$ | 1.0 | **1** |

Reading **downwards**, $(0.6875)_{10} = (0.1011)_2$.

For $13.75$: integer $13 = (1101)_2$; fraction $0.75 \to 0.75\times2 = 1.5$
(**1**), $0.5\times2 = 1.0$ (**1**), so $0.75 = (0.11)_2$. Hence
$(13.75)_{10} = (1101.11)_2$.
:::

::: caution Read the remainders in the right direction
Integer remainders are read **bottom to top** (last remainder is the most
significant bit). Fraction carries are read **top to bottom**. Reversing either
one is the single commonest mistake in this chapter.
:::

### Binary ↔ octal ↔ hexadecimal: grouping

Because $8 = 2^3$ and $16 = 2^4$, each octal digit is exactly **3 bits** and each
hex digit exactly **4 bits**. Group from the **binary point outwards**, padding
with zeros at the ends.

| Binary | Octal | Binary | Hex | Binary | Hex |
|---|---|---|---|---|---|
| 000 | 0 | 0000 | 0 | 1000 | 8 |
| 001 | 1 | 0001 | 1 | 1001 | 9 |
| 010 | 2 | 0010 | 2 | 1010 | A |
| 011 | 3 | 0011 | 3 | 1011 | B |
| 100 | 4 | 0100 | 4 | 1100 | C |
| 101 | 5 | 0101 | 5 | 1101 | D |
| 110 | 6 | 0110 | 6 | 1110 | E |
| 111 | 7 | 0111 | 7 | 1111 | F |

::: example Worked example 2.4 — grouping in both directions
**Problem.** (a) Convert $(1010101111)_2$ to octal and hexadecimal.
(b) Convert $(753)_8$ to hexadecimal.

**Solution.**
(a) In threes from the right, padding the left: 001 010 101 111 → $(1257)_8$.
In fours from the right, padding the left: 0010 1010 1111 → 2, A, F →
$(2AF)_{16}$.

(b) Octal → binary, three bits each: 7 = 111, 5 = 101, 3 = 011, giving
111101011. Now regroup in fours from the right: 0001 1110 1011 →
1, E, B → $(1EB)_{16}$.

**Check:** $(753)_8 = 7(64)+5(8)+3 = 491$ and $(1EB)_{16} = 256+14(16)+11 = 491$ ✓
:::

::: tip Octal to hexadecimal
There is no direct rule. Always convert through binary: octal → binary (3 bits
per digit) → regroup in fours → hexadecimal. Trying to do it "directly" costs
marks.
:::

## 2.2 Binary addition and subtraction

Binary arithmetic follows exactly the same column rules as decimal, with only
two digits available.

| Addition | Result | Subtraction | Result |
|---|---|---|---|
| 0 + 0 | 0 | 0 − 0 | 0 |
| 0 + 1 | 1 | 1 − 0 | 1 |
| 1 + 0 | 1 | 1 − 1 | 0 |
| 1 + 1 | **0 carry 1** | 0 − 1 | **1 borrow 1** |
| 1 + 1 + 1 | **1 carry 1** | | |

::: example Worked example 2.5 — addition, subtraction, multiplication, division
**Problem.** Perform in binary: (a) $1011 + 1101$, (b) $11010 - 1011$,
(c) $1101 \times 101$, (d) $110110 \div 101$.

**Solution.**

(a) Add column by column from the right:

```text
   1111     <- carries
    1011    (11)
  + 1101    (13)
  -------
   11000    (24)
```

(b) Subtract, borrowing where needed:

```text
   11010    (26)
  - 01011   (11)
  --------
   01111    (15)
```

(c) Multiply exactly as in decimal — each partial product is either the
multiplicand or zero:

```text
      1101        (13)
    x  101        ( 5)
    --------
      1101
     0000
    1101
    --------
    1000001       (65)
```

(d) Long division:

```text
          1010        quotient = 1010 (10)
      ----------
 101 ) 110110
       101
       ---
        0111
         101
         ---
          0101 0
           101
           ---
             100    remainder = 100 (4)
```

Check: $54 = 5\times10 + 4$ ✓
:::

::: caution Borrowing in binary is "borrow 2, not 10"
When you borrow into a column in binary, the borrowed unit is worth **2**, so
$0-1$ becomes $2-1 = 1$ with a borrow carried leftwards. Students who borrow 10
get decimal-looking nonsense.
:::

## 2.3 One's and Two's complement methods of binary subtraction

Hardware has no subtractor. A computer subtracts by **adding the complement**,
so the same adder circuit does both operations. This is why complements matter.

::: definition One's and two's complement
The **1's complement** of a binary number is obtained by replacing every 0 with
1 and every 1 with 0 (bitwise inversion).

The **2's complement** is the 1's complement **plus 1**:
$$ \text{2's complement} = \text{1's complement} + 1 = 2^{n} - N $$
:::

For example, with 4 bits: $N = 0110$ → 1's complement $= 1001$ → 2's complement
$= 1010$.

### Subtraction by 1's complement

To compute $A - B$:

1. Take the 1's complement of $B$ (the subtrahend).
2. Add it to $A$.
3. If a **carry comes out of the leftmost column**, the answer is positive: add
   that carry back into the least significant bit (**end-around carry**). The
   result is the answer.
4. If there is **no carry out**, the answer is negative: take the 1's complement
   of the sum and put a minus sign in front.

::: example Worked example 2.6 — 1's complement subtraction
**Problem.** Using 1's complement in 4 bits, find (a) $1010 - 0110$ and
(b) $0110 - 1010$.

**Solution.**

(a) $1010 - 0110$ (i.e. $10 - 6$). 1's complement of 0110 = **1001**.

```text
     1010
   + 1001
   -------
   1 0011      carry out = 1  -> positive
       +1      end-around carry
   -------
     0100      = 4
```

Answer: $(0100)_2 = +4$ ✓

(b) $0110 - 1010$ (i.e. $6 - 10$). 1's complement of 1010 = **0101**.

```text
     0110
   + 0101
   -------
     1011      no carry out -> negative
```

Take the 1's complement of 1011, which is 0100, and attach a minus sign:
answer $= -(0100)_2 = -4$ ✓
:::

### Subtraction by 2's complement

1. Take the 2's complement of $B$.
2. Add it to $A$.
3. If there is a **carry out, discard it**; the result is positive.
4. If there is **no carry out**, the result is negative: take the 2's complement
   of the sum and put a minus sign in front.

::: example Worked example 2.7 — 2's complement subtraction
**Problem.** Using 2's complement, find (a) $1010 - 0110$ in 4 bits and
(b) $45 - 78$ in 8 bits.

**Solution.**

(a) 2's complement of 0110 = 1001 + 1 = **1010**.

```text
     1010
   + 1010
   -------
   1 0100      discard the carry out
   -------
     0100      = +4
```

(b) $45 = (00101101)_2$ and $78 = (01001110)_2$.
1's complement of 78 = 10110001, so the 2's complement is **10110010**.

```text
     00101101      (45)
   + 10110010      (2's complement of 78)
   -----------
     11011111      no carry out -> negative
```

The magnitude is the 2's complement of 11011111 = 00100000 + 1 = **00100001**
$= 33$. Therefore $45 - 78 = -33$ ✓
:::

| | 1's complement | 2's complement |
|---|---|---|
| How formed | invert all bits | invert all bits, then add 1 |
| Carry handling | **add** the end-around carry back | **discard** the carry |
| Representations of zero | two (0000 and 1111) | one (0000) |
| Range with $n$ bits | $-(2^{n-1}-1)$ to $+(2^{n-1}-1)$ | $-2^{n-1}$ to $+(2^{n-1}-1)$ |
| Used in practice | rare | **all modern computers** |

::: caution Both numbers must have the same number of bits
Before complementing, pad the shorter number with leading zeros so that both
operands have the same width. Complementing a 4-bit number and adding it to an
8-bit number gives a wrong answer every time.
:::

## 2.4 Introduction to Boolean algebra

**Boolean algebra** is the algebra of two-valued logic, published by the English
mathematician **George Boole** in *An Investigation of the Laws of Thought*
(1854). In 1938 **Claude Shannon** showed that it describes switching circuits
exactly — a switch is either on or off — and that insight is the foundation of
all digital design.

| Ordinary algebra | Boolean algebra |
|---|---|
| Variables take any real value | Variables take only 0 or 1 |
| Operations: $+,-,\times,\div$ | Operations: OR ($+$), AND ($\cdot$), NOT ($\bar{\ }$) |
| Subtraction and division exist | No subtraction, no division |
| $1+1 = 2$ | $1+1 = 1$ |
| No complement law | $A + \bar{A} = 1$, $A\cdot\bar{A} = 0$ |

Here $+$ means **OR** (read "A or B"), $\cdot$ means **AND** (read "A and B"),
and the bar means **NOT**. The 0 and 1 are not quantities; they are *logic
levels* — false/true, off/on, low/high voltage.

## 2.5 Boolean values, truth table, Boolean expression and Boolean function

- A **Boolean value** (logic value) is either **0** (false, low) or **1** (true,
  high).
- A **Boolean variable** is a symbol, such as $A$, that can hold only a Boolean
  value. A **literal** is a variable or its complement: $A$ and $\bar{A}$ are two
  literals.
- A **Boolean expression** is variables combined by AND, OR and NOT, for example
  $\bar{A}B + AC$.
- A **Boolean function** assigns an output value to every combination of its
  input variables, written $F(A,B,C) = \bar{A}B + AC$.
- A **truth table** lists the output for *every* input combination. With $n$
  input variables it has $2^{n}$ rows.

For $F(A,B,C) = \bar{A}B + AC$:

| A | B | C | $\bar{A}$ | $\bar{A}B$ | $AC$ | $F$ |
|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 1 | 0 | 0 | **0** |
| 0 | 0 | 1 | 1 | 0 | 0 | **0** |
| 0 | 1 | 0 | 1 | 1 | 0 | **1** |
| 0 | 1 | 1 | 1 | 1 | 0 | **1** |
| 1 | 0 | 0 | 0 | 0 | 0 | **0** |
| 1 | 0 | 1 | 0 | 0 | 1 | **1** |
| 1 | 1 | 0 | 0 | 0 | 0 | **0** |
| 1 | 1 | 1 | 0 | 0 | 1 | **1** |

::: definition SOP and POS
A **sum of products (SOP)** expression is an OR of AND terms, e.g.
$\bar{A}B + AC$. A **product of sums (POS)** expression is an AND of OR terms,
e.g. $(A+B)(\bar{A}+C)$.

A **minterm** is a product term containing every variable exactly once; for
three variables, row 5 (101) gives the minterm $A\bar{B}C$, written $m_5$. A
function can be written as the sum of the minterms of the rows where $F = 1$:
here $F = \sum m(2,3,5,7)$.
:::

## 2.6 Logic gates

::: definition Logic gate
A logic gate is an electronic circuit with one or more inputs and exactly one
output, which produces an output determined only by the present combination of
inputs according to a Boolean function.
:::

```figure caption="The seven logic gates in the standard distinctive-shape symbols. Note the flat back and round nose of AND, the curved back and pointed nose of OR, the extra back curve of XOR, and the inversion bubble on NOT, NAND, NOR and XNOR."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch, Circle
from matplotlib.transforms import Affine2D
K=0.2761
def _and():
    return Path([(0,-.5),(0,.5),(.5,.5),(.5+K,.5),(1,K),(1,0),(1,-K),(.5+K,-.5),
                 (.5,-.5),(0,-.5)],[1,2,2,4,4,4,4,4,4,79])
def _bk(b): return [(b,-.5),(b+.32,-.24),(b+.32,.24),(b,.5)]
def _or(b=0.0):
    return Path(_bk(b)+[(b+.44,.46),(b+.86,.30),(b+1.14,0),(b+.86,-.30),
                        (b+.44,-.46),(b,-.5)],[1,4,4,4,4,4,4,4,4,4])
def _bx(y,b=0.0):
    t=np.linspace(0,1,400)
    yy=(1-t)**3*(-.5)+3*(1-t)**2*t*(-.24)+3*(1-t)*t**2*.24+t**3*.5
    xx=(1-t)**3*b+3*(1-t)**2*t*(b+.32)+3*(1-t)*t**2*(b+.32)+t**3*b
    return float(np.interp(y,yy,xx))
def gate(ax,k,x,y,s=1.0,dy=.27,lw=1.5,bub=None):
    k=k.upper(); T=Affine2D().scale(s).translate(x,y)
    if k in('AND','NAND'): p,nose,a0,a1=_and(),1.0,0.,0.
    elif k in('OR','NOR'): p,nose,a0,a1=_or(),1.14,_bx(dy),_bx(-dy)
    elif k in('XOR','XNOR'): p,nose,a0,a1=_or(.17),1.31,_bx(dy,.17),_bx(-dy,.17)
    else: p,nose,a0,a1=Path([(0,-.5),(0,.5),(.88,0),(0,-.5)],[1,2,2,79]),.88,0.,0.
    ax.add_patch(PathPatch(p.transformed(T),fc='none',ec=INK,lw=lw,
                           joinstyle='round',zorder=3))
    if k in('XOR','XNOR'):
        ax.add_patch(PathPatch(Path(_bk(0.),[1,4,4,4]).transformed(T),
                     fc='none',ec=INK,lw=lw,zorder=3))
    inv = bub if bub is not None else (k in('NAND','NOR','XNOR','NOT'))
    if inv:
        ax.add_patch(Circle((x+(nose+.085)*s,y),.085*s,fc='white',ec=INK,lw=lw,zorder=4))
        out=(x+(nose+.17)*s,y)
    else: out=(x+nose*s,y)
    if k=='NOT': return (x,y),None,out
    return (x+a0*s,y+dy*s),(x+a1*s,y-dy*s),out
def wire(ax,*p,c=None):
    ax.plot([q[0] for q in p],[q[1] for q in p],color=c or INK,lw=1.2,zorder=2,
            solid_capstyle='round')
fig, ax = plt.subplots(figsize=(5.1,3.3))
items=[("AND",r"$A\cdot B$"),("OR",r"$A+B$"),("NOT",r"$\bar{A}$"),
       ("XOR",r"$A\oplus B$"),("NAND",r"$\overline{A\cdot B}$"),
       ("NOR",r"$\overline{A+B}$"),("XNOR",r"$\overline{A\oplus B}$")]
pos=[(0,3.1),(3.15,3.1),(6.30,3.1),(9.45,3.1),(0,0),(3.15,0),(6.30,0)]
for (k,lab),(x,y) in zip(items,pos):
    a,b,o=gate(ax,k,x,y,s=.92)
    ax.text(x+.6,y+1.02,k,ha="center",va="bottom",fontsize=9.2,color=INK,fontweight="bold")
    ax.text(x+.6,y-.95,lab,ha="center",va="top",fontsize=10,color=ACCENT)
    wire(ax,(a[0]-.55,a[1]),a)
    ax.text(a[0]-.66,a[1],"A",ha="right",va="center",fontsize=8.2,color=MUTED)
    if b is not None:
        wire(ax,(b[0]-.55,b[1]),b)
        ax.text(b[0]-.66,b[1],"B",ha="right",va="center",fontsize=8.2,color=MUTED)
    wire(ax,o,(o[0]+.5,o[1]))
ax.set_xlim(-1.35,11.6); ax.set_ylim(-1.7,4.6); ax.set_aspect("equal"); ax.axis("off")
```

| A | B | AND $A\cdot B$ | OR $A+B$ | NAND $\overline{A\cdot B}$ | NOR $\overline{A+B}$ | XOR $A\oplus B$ | XNOR $\overline{A\oplus B}$ |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 1 | 1 | 0 | 1 |
| 0 | 1 | 0 | 1 | 1 | 0 | 1 | 0 |
| 1 | 0 | 0 | 1 | 1 | 0 | 1 | 0 |
| 1 | 1 | 1 | 1 | 0 | 0 | 0 | 1 |

The NOT gate (inverter) has one input: $\bar{0} = 1$ and $\bar{1} = 0$.

In words: **AND** gives 1 only when *all* inputs are 1. **OR** gives 1 when *at
least one* input is 1. **XOR** gives 1 when the inputs are *different* — it is
the "odd number of 1s" detector. **XNOR** gives 1 when the inputs are the *same*,
so it is an equality detector. NAND and NOR are the inverses of AND and OR.

::: key NAND and NOR are universal gates
Every Boolean function can be built using **only NAND** gates, or **only NOR**
gates. For NAND: $\bar{A} = \overline{A\cdot A}$;
$A\cdot B = \overline{\overline{A\cdot B}}$ (a NAND followed by a NAND-inverter);
and $A+B = \overline{\bar{A}\cdot\bar{B}}$ (invert both inputs, then NAND). This
is why whole chips are manufactured from one repeated gate type.
:::

### Drawing a circuit from an expression

Work from the innermost operation outwards: complements first, then AND terms,
then the final OR.

```figure caption="Logic circuit for $F = A\cdot B + \bar{A}\cdot C$. The NOT gate produces $\bar{A}$, two AND gates form the product terms, and the OR gate sums them."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch, Circle
from matplotlib.transforms import Affine2D
K=0.2761
def _and():
    return Path([(0,-.5),(0,.5),(.5,.5),(.5+K,.5),(1,K),(1,0),(1,-K),(.5+K,-.5),
                 (.5,-.5),(0,-.5)],[1,2,2,4,4,4,4,4,4,79])
def _bk(b): return [(b,-.5),(b+.32,-.24),(b+.32,.24),(b,.5)]
def _or(b=0.0):
    return Path(_bk(b)+[(b+.44,.46),(b+.86,.30),(b+1.14,0),(b+.86,-.30),
                        (b+.44,-.46),(b,-.5)],[1,4,4,4,4,4,4,4,4,4])
def _bx(y,b=0.0):
    t=np.linspace(0,1,400)
    yy=(1-t)**3*(-.5)+3*(1-t)**2*t*(-.24)+3*(1-t)*t**2*.24+t**3*.5
    xx=(1-t)**3*b+3*(1-t)**2*t*(b+.32)+3*(1-t)*t**2*(b+.32)+t**3*b
    return float(np.interp(y,yy,xx))
def gate(ax,k,x,y,s=1.0,dy=.27,lw=1.5,bub=None):
    k=k.upper(); T=Affine2D().scale(s).translate(x,y)
    if k in('AND','NAND'): p,nose,a0,a1=_and(),1.0,0.,0.
    elif k in('OR','NOR'): p,nose,a0,a1=_or(),1.14,_bx(dy),_bx(-dy)
    elif k in('XOR','XNOR'): p,nose,a0,a1=_or(.17),1.31,_bx(dy,.17),_bx(-dy,.17)
    else: p,nose,a0,a1=Path([(0,-.5),(0,.5),(.88,0),(0,-.5)],[1,2,2,79]),.88,0.,0.
    ax.add_patch(PathPatch(p.transformed(T),fc='none',ec=INK,lw=lw,
                           joinstyle='round',zorder=3))
    if k in('XOR','XNOR'):
        ax.add_patch(PathPatch(Path(_bk(0.),[1,4,4,4]).transformed(T),
                     fc='none',ec=INK,lw=lw,zorder=3))
    inv = bub if bub is not None else (k in('NAND','NOR','XNOR','NOT'))
    if inv:
        ax.add_patch(Circle((x+(nose+.085)*s,y),.085*s,fc='white',ec=INK,lw=lw,zorder=4))
        out=(x+(nose+.17)*s,y)
    else: out=(x+nose*s,y)
    if k=='NOT': return (x,y),None,out
    return (x+a0*s,y+dy*s),(x+a1*s,y-dy*s),out
def inbub(ax,p,s=1.0):
    ax.add_patch(Circle((p[0]-.085*s,p[1]),.085*s,fc='white',ec=INK,lw=1.5,zorder=4))
    return (p[0]-.17*s,p[1])
def wire(ax,*p,c=None):
    ax.plot([q[0] for q in p],[q[1] for q in p],color=c or INK,lw=1.2,zorder=2,
            solid_capstyle='round')
def dot(ax,p):
    ax.plot([p[0]],[p[1]],'o',ms=3.2,color=INK,zorder=5)

fig, ax = plt.subplots(figsize=(5.1,3.0))
S=0.78
n_in,_,n_out = gate(ax,'NOT',1.55,0.85+0.27*S,S)
a1,a2,a_out  = gate(ax,'AND',3.15,2.55,S)
b1,b2,b_out  = gate(ax,'AND',3.15,0.85,S)
o1,o2,o_out  = gate(ax,'OR', 5.15,1.70,S)
XA, XB, XC, TOP = 0.30, 0.62, 0.94, 3.45
for x,lab,c in [(XA,'A',SERIES[0]),(XB,'B',SERIES[1]),(XC,'C',SERIES[2])]:
    ax.text(x,TOP+0.10,lab,ha='center',va='bottom',fontsize=9.4,color=c,fontweight='bold')
wire(ax,(XA,TOP),(XA,n_in[1]),n_in)
dot(ax,(XA,a1[1])); wire(ax,(XA,a1[1]),a1)
wire(ax,(XB,TOP),(XB,a2[1]),a2)
wire(ax,(XC,TOP),(XC,b2[1]),b2)
wire(ax,n_out,(2.72,n_out[1]),(2.72,b1[1]),b1)
ax.text(2.10,1.20,r'$\bar{A}$',ha='center',va='bottom',fontsize=10,color=MUTED)
wire(ax,a_out,(4.62,a_out[1]),(4.62,o1[1]),o1)
wire(ax,b_out,(4.62,b_out[1]),(4.62,o2[1]),o2)
ax.text(4.20,2.72,r'$A\cdot B$',ha='center',va='bottom',fontsize=9.4,color=MUTED)
ax.text(4.20,0.48,r'$\bar{A}\cdot C$',ha='center',va='top',fontsize=9.4,color=MUTED)
wire(ax,o_out,(o_out[0]+0.70,o_out[1]))
ax.text(o_out[0]+0.84,o_out[1],r'$F$',ha='left',va='center',fontsize=11,color=ACCENT)
ax.set_xlim(-0.10,7.20); ax.set_ylim(0.10,3.90); ax.set_aspect('equal'); ax.axis('off')
```

### Half adder and full adder

A **half adder** adds two single bits and produces a sum and a carry. Its two
outputs are exactly XOR and AND of the inputs.

$$ S = A \oplus B, \qquad C = A\cdot B $$

| A | B | Sum $S$ | Carry $C$ |
|---|---|---|---|
| 0 | 0 | 0 | 0 |
| 0 | 1 | 1 | 0 |
| 1 | 0 | 1 | 0 |
| 1 | 1 | 0 | 1 |

A half adder cannot be used for the second and later columns of an addition,
because it has nowhere to take the carry *in*. A **full adder** adds three bits —
$A$, $B$ and a carry-in $C_{in}$ — and is built from two half adders plus an OR
gate.

$$ S = A \oplus B \oplus C_{in}, \qquad
C_{out} = A\cdot B + (A \oplus B)\cdot C_{in} $$

| A | B | $C_{in}$ | Sum $S$ | $C_{out}$ |
|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 1 | 0 |
| 0 | 1 | 0 | 1 | 0 |
| 0 | 1 | 1 | 0 | 1 |
| 1 | 0 | 0 | 1 | 0 |
| 1 | 0 | 1 | 0 | 1 |
| 1 | 1 | 0 | 0 | 1 |
| 1 | 1 | 1 | 1 | 1 |

```figure caption="Half adder. The sum bit is the XOR of the two inputs and the carry bit is their AND."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch, Circle
from matplotlib.transforms import Affine2D
K=0.2761
def _and():
    return Path([(0,-.5),(0,.5),(.5,.5),(.5+K,.5),(1,K),(1,0),(1,-K),(.5+K,-.5),
                 (.5,-.5),(0,-.5)],[1,2,2,4,4,4,4,4,4,79])
def _bk(b): return [(b,-.5),(b+.32,-.24),(b+.32,.24),(b,.5)]
def _or(b=0.0):
    return Path(_bk(b)+[(b+.44,.46),(b+.86,.30),(b+1.14,0),(b+.86,-.30),
                        (b+.44,-.46),(b,-.5)],[1,4,4,4,4,4,4,4,4,4])
def _bx(y,b=0.0):
    t=np.linspace(0,1,400)
    yy=(1-t)**3*(-.5)+3*(1-t)**2*t*(-.24)+3*(1-t)*t**2*.24+t**3*.5
    xx=(1-t)**3*b+3*(1-t)**2*t*(b+.32)+3*(1-t)*t**2*(b+.32)+t**3*b
    return float(np.interp(y,yy,xx))
def gate(ax,k,x,y,s=1.0,dy=.27,lw=1.5,bub=None):
    k=k.upper(); T=Affine2D().scale(s).translate(x,y)
    if k in('AND','NAND'): p,nose,a0,a1=_and(),1.0,0.,0.
    elif k in('OR','NOR'): p,nose,a0,a1=_or(),1.14,_bx(dy),_bx(-dy)
    elif k in('XOR','XNOR'): p,nose,a0,a1=_or(.17),1.31,_bx(dy,.17),_bx(-dy,.17)
    else: p,nose,a0,a1=Path([(0,-.5),(0,.5),(.88,0),(0,-.5)],[1,2,2,79]),.88,0.,0.
    ax.add_patch(PathPatch(p.transformed(T),fc='none',ec=INK,lw=lw,
                           joinstyle='round',zorder=3))
    if k in('XOR','XNOR'):
        ax.add_patch(PathPatch(Path(_bk(0.),[1,4,4,4]).transformed(T),
                     fc='none',ec=INK,lw=lw,zorder=3))
    inv = bub if bub is not None else (k in('NAND','NOR','XNOR','NOT'))
    if inv:
        ax.add_patch(Circle((x+(nose+.085)*s,y),.085*s,fc='white',ec=INK,lw=lw,zorder=4))
        out=(x+(nose+.17)*s,y)
    else: out=(x+nose*s,y)
    if k=='NOT': return (x,y),None,out
    return (x+a0*s,y+dy*s),(x+a1*s,y-dy*s),out
def inbub(ax,p,s=1.0):
    ax.add_patch(Circle((p[0]-.085*s,p[1]),.085*s,fc='white',ec=INK,lw=1.5,zorder=4))
    return (p[0]-.17*s,p[1])
def wire(ax,*p,c=None):
    ax.plot([q[0] for q in p],[q[1] for q in p],color=c or INK,lw=1.2,zorder=2,
            solid_capstyle='round')
def dot(ax,p):
    ax.plot([p[0]],[p[1]],'o',ms=3.2,color=INK,zorder=5)

fig, ax = plt.subplots(figsize=(4.4,2.4))
S=0.70
x1,x2,xo = gate(ax,'XOR',0.90,1.55,S)
y1,y2,yo = gate(ax,'AND',0.90,0.45,S)
wire(ax,(-1.30,x1[1]),x1)
dot(ax,(-1.15,x1[1])); wire(ax,(-1.15,x1[1]),(-1.15,y2[1]),y2)
ax.text(-1.42,x1[1],'A',ha='right',va='center',fontsize=9.4,color=INK)
wire(ax,(-0.60,x2[1]),x2)
dot(ax,(-0.45,x2[1])); wire(ax,(-0.45,x2[1]),(-0.45,y1[1]),y1)
ax.text(-0.72,x2[1],'B',ha='right',va='center',fontsize=9.4,color=INK)
wire(ax,xo,(2.60,xo[1]))
ax.text(2.72,xo[1],r'$S = A\oplus B$',ha='left',va='center',fontsize=9.6,color=ACCENT)
wire(ax,yo,(2.60,yo[1]))
ax.text(2.72,yo[1],r'$C = A\cdot B$',ha='left',va='center',fontsize=9.6,color=ACCENT)
ax.set_xlim(-1.85,5.30); ax.set_ylim(-0.20,2.30); ax.set_aspect('equal'); ax.axis('off')
```

```figure caption="Full adder built from two half adders and an OR gate. The first XOR and AND form half adder 1; the second XOR and AND form half adder 2; the OR gate combines the two carries."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch, Circle
from matplotlib.transforms import Affine2D
K=0.2761
def _and():
    return Path([(0,-.5),(0,.5),(.5,.5),(.5+K,.5),(1,K),(1,0),(1,-K),(.5+K,-.5),
                 (.5,-.5),(0,-.5)],[1,2,2,4,4,4,4,4,4,79])
def _bk(b): return [(b,-.5),(b+.32,-.24),(b+.32,.24),(b,.5)]
def _or(b=0.0):
    return Path(_bk(b)+[(b+.44,.46),(b+.86,.30),(b+1.14,0),(b+.86,-.30),
                        (b+.44,-.46),(b,-.5)],[1,4,4,4,4,4,4,4,4,4])
def _bx(y,b=0.0):
    t=np.linspace(0,1,400)
    yy=(1-t)**3*(-.5)+3*(1-t)**2*t*(-.24)+3*(1-t)*t**2*.24+t**3*.5
    xx=(1-t)**3*b+3*(1-t)**2*t*(b+.32)+3*(1-t)*t**2*(b+.32)+t**3*b
    return float(np.interp(y,yy,xx))
def gate(ax,k,x,y,s=1.0,dy=.27,lw=1.5,bub=None):
    k=k.upper(); T=Affine2D().scale(s).translate(x,y)
    if k in('AND','NAND'): p,nose,a0,a1=_and(),1.0,0.,0.
    elif k in('OR','NOR'): p,nose,a0,a1=_or(),1.14,_bx(dy),_bx(-dy)
    elif k in('XOR','XNOR'): p,nose,a0,a1=_or(.17),1.31,_bx(dy,.17),_bx(-dy,.17)
    else: p,nose,a0,a1=Path([(0,-.5),(0,.5),(.88,0),(0,-.5)],[1,2,2,79]),.88,0.,0.
    ax.add_patch(PathPatch(p.transformed(T),fc='none',ec=INK,lw=lw,
                           joinstyle='round',zorder=3))
    if k in('XOR','XNOR'):
        ax.add_patch(PathPatch(Path(_bk(0.),[1,4,4,4]).transformed(T),
                     fc='none',ec=INK,lw=lw,zorder=3))
    inv = bub if bub is not None else (k in('NAND','NOR','XNOR','NOT'))
    if inv:
        ax.add_patch(Circle((x+(nose+.085)*s,y),.085*s,fc='white',ec=INK,lw=lw,zorder=4))
        out=(x+(nose+.17)*s,y)
    else: out=(x+nose*s,y)
    if k=='NOT': return (x,y),None,out
    return (x+a0*s,y+dy*s),(x+a1*s,y-dy*s),out
def inbub(ax,p,s=1.0):
    ax.add_patch(Circle((p[0]-.085*s,p[1]),.085*s,fc='white',ec=INK,lw=1.5,zorder=4))
    return (p[0]-.17*s,p[1])
def wire(ax,*p,c=None):
    ax.plot([q[0] for q in p],[q[1] for q in p],color=c or INK,lw=1.2,zorder=2,
            solid_capstyle='round')
def dot(ax,p):
    ax.plot([p[0]],[p[1]],'o',ms=3.2,color=INK,zorder=5)

fig, ax = plt.subplots(figsize=(5.1,2.9))
S=0.60
p1,p2,po = gate(ax,'XOR',0.80,3.00,S)     # A xor B
s1,s2,so = gate(ax,'AND',0.80,0.60-0.27*S,S)     # A . B
q1,q2,qo = gate(ax,'XOR',2.90,2.40,S)     # (A xor B) xor Cin  -> S
r1,r2,ro = gate(ax,'AND',2.90,1.30,S)     # Cin . (A xor B)
t1,t2,to = gate(ax,'OR', 4.30,0.60,S)     # Cout
# --- inputs A and B, nested taps, no crossings ---
wire(ax,(-1.30,p1[1]),p1)
dot(ax,(-1.15,p1[1])); wire(ax,(-1.15,p1[1]),(-1.15,s2[1]),s2)
ax.text(-1.42,p1[1],'A',ha='right',va='center',fontsize=9.2,color=INK)
wire(ax,(-0.60,p2[1]),p2)
dot(ax,(-0.45,p2[1])); wire(ax,(-0.45,p2[1]),(-0.45,s1[1]),s1)
ax.text(-0.72,p2[1],'B',ha='right',va='center',fontsize=9.2,color=INK)
# --- A xor B fans out to XOR2 top and AND2 bottom ---
wire(ax,po,(1.95,po[1]),(1.95,r2[1]),r2)
dot(ax,(1.95,q1[1])); wire(ax,(1.95,q1[1]),q1)
ax.text(1.92,3.08,r'$A\oplus B$',ha='center',va='bottom',fontsize=8.8,color=MUTED)
# --- Cin fans out to XOR2 bottom and AND2 top ---
wire(ax,(0.30,1.90),(2.35,1.90),(2.35,q2[1]),q2)
dot(ax,(2.35,1.90)); wire(ax,(2.35,1.90),(2.35,r1[1]),r1)
ax.text(0.20,1.90,r'$C_{in}$',ha='right',va='center',fontsize=9.2,color=INK)
# --- outputs ---
wire(ax,qo,(5.48,qo[1]))
ax.text(5.60,qo[1],r'$S$',ha='left',va='center',fontsize=10.5,color=ACCENT)
wire(ax,ro,(3.95,ro[1]),(3.95,t1[1]),t1)
wire(ax,so,t2)
wire(ax,to,(5.48,to[1]))
ax.text(5.60,to[1],r'$C_{out}$',ha='left',va='center',fontsize=10.5,color=ACCENT)
ax.set_xlim(-1.85,6.45); ax.set_ylim(0.00,3.60); ax.set_aspect('equal'); ax.axis('off')
```

## 2.7 Laws of Boolean algebra

| Name | OR form | AND form |
|---|---|---|
| Identity | $A + 0 = A$ | $A \cdot 1 = A$ |
| Null (dominance) | $A + 1 = 1$ | $A \cdot 0 = 0$ |
| Idempotent | $A + A = A$ | $A \cdot A = A$ |
| Complement | $A + \bar{A} = 1$ | $A \cdot \bar{A} = 0$ |
| Involution (double negation) | $\bar{\bar{A}} = A$ | — |
| Commutative | $A + B = B + A$ | $A\cdot B = B\cdot A$ |
| Associative | $A+(B+C) = (A+B)+C$ | $A(BC) = (AB)C$ |
| Distributive | $A(B+C) = AB + AC$ | $A + BC = (A+B)(A+C)$ |
| Absorption | $A + AB = A$ | $A(A+B) = A$ |
| Redundancy | $A + \bar{A}B = A + B$ | $A(\bar{A}+B) = AB$ |
| De Morgan | $\overline{A+B} = \bar{A}\cdot\bar{B}$ | $\overline{A\cdot B} = \bar{A}+\bar{B}$ |

Note the second distributive law, $A + BC = (A+B)(A+C)$. It has **no counterpart
in ordinary algebra** and is a favourite examination question.

::: memory De Morgan in one sentence
"**Break the bar, change the sign.**" Break the long overbar into two short ones
and swap AND with OR. $\overline{A+B+C} = \bar{A}\bar{B}\bar{C}$ and
$\overline{ABC} = \bar{A}+\bar{B}+\bar{C}$.
:::

```figure caption="De Morgan's theorems drawn as gates. A NAND gate is the same circuit as an OR gate with both inputs inverted; a NOR gate is the same as an AND gate with both inputs inverted."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch, Circle
from matplotlib.transforms import Affine2D
K=0.2761
def _and():
    return Path([(0,-.5),(0,.5),(.5,.5),(.5+K,.5),(1,K),(1,0),(1,-K),(.5+K,-.5),
                 (.5,-.5),(0,-.5)],[1,2,2,4,4,4,4,4,4,79])
def _bk(b): return [(b,-.5),(b+.32,-.24),(b+.32,.24),(b,.5)]
def _or(b=0.0):
    return Path(_bk(b)+[(b+.44,.46),(b+.86,.30),(b+1.14,0),(b+.86,-.30),
                        (b+.44,-.46),(b,-.5)],[1,4,4,4,4,4,4,4,4,4])
def _bx(y,b=0.0):
    t=np.linspace(0,1,400)
    yy=(1-t)**3*(-.5)+3*(1-t)**2*t*(-.24)+3*(1-t)*t**2*.24+t**3*.5
    xx=(1-t)**3*b+3*(1-t)**2*t*(b+.32)+3*(1-t)*t**2*(b+.32)+t**3*b
    return float(np.interp(y,yy,xx))
def gate(ax,k,x,y,s=1.0,dy=.27,lw=1.5,outbub=False,inbub=False):
    k=k.upper(); T=Affine2D().scale(s).translate(x,y)
    if k=='AND': p,nose,a0,a1=_and(),1.0,0.,0.
    else: p,nose,a0,a1=_or(),1.14,_bx(dy),_bx(-dy)
    ax.add_patch(PathPatch(p.transformed(T),fc='none',ec=INK,lw=lw,
                           joinstyle='round',zorder=3))
    if outbub:
        ax.add_patch(Circle((x+(nose+.085)*s,y),.085*s,fc='white',ec=INK,lw=lw,zorder=4))
        out=(x+(nose+.17)*s,y)
    else: out=(x+nose*s,y)
    A=(x+a0*s,y+dy*s); B=(x+a1*s,y-dy*s)
    if inbub:
        for P in (A,B):
            ax.add_patch(Circle((P[0]-.085*s,P[1]),.085*s,fc='white',ec=INK,lw=lw,zorder=4))
        A=(A[0]-.17*s,A[1]); B=(B[0]-.17*s,B[1])
    return A,B,out
def wire(ax,*p):
    ax.plot([q[0] for q in p],[q[1] for q in p],color=INK,lw=1.2,zorder=2,
            solid_capstyle='round')
def unit(x,y,k,ob,ib,lab,S=0.80):
    A,B,O = gate(ax,k,x,y,S,outbub=ob,inbub=ib)
    wire(ax,(A[0]-0.42,A[1]),A); wire(ax,(B[0]-0.42,B[1]),B)
    ax.text(A[0]-0.52,A[1],'A',ha='right',va='center',fontsize=8.4,color=MUTED)
    ax.text(B[0]-0.52,B[1],'B',ha='right',va='center',fontsize=8.4,color=MUTED)
    wire(ax,O,(O[0]+0.38,O[1]))
    ax.text(x+0.5,y-0.78,lab,ha='center',va='top',fontsize=9.6,color=ACCENT)
fig, ax = plt.subplots(figsize=(5.1,2.7))
unit(0.55,2.15,'AND',True,False,r'$\overline{A\cdot B}$')
ax.text(2.92,2.15,'=',ha='center',va='center',fontsize=12,color=INK)
unit(4.10,2.15,'OR',False,True,r'$\bar{A}+\bar{B}$')
unit(0.55,0.35,'OR',True,False,r'$\overline{A+B}$')
ax.text(2.92,0.35,'=',ha='center',va='center',fontsize=12,color=INK)
unit(4.10,0.35,'AND',False,True,r'$\bar{A}\cdot\bar{B}$')
ax.set_xlim(-0.35,6.25); ax.set_ylim(-0.75,2.95); ax.set_aspect('equal'); ax.axis('off')
```

### Simplification using the laws

::: example Worked example 2.8 — algebraic simplification
**Problem.** Simplify (a) $F = AB + A(B+C) + B(B+C)$ and
(b) $F = \bar{A}BC + A\bar{B}C + AB\bar{C} + ABC$.

**Solution.**

(a) Expand with the distributive law:

$$ F = AB + AB + AC + BB + BC $$

Using $BB = B$ (idempotent) and $AB + AB = AB$:

$$ F = AB + AC + B + BC = B(1 + A + C) + AC = B\cdot 1 + AC = B + AC $$

(b) Use $ABC = ABC + ABC + ABC$ (idempotent) so that $ABC$ can pair with each of
the other three terms:

$$ F = (\bar{A}BC + ABC) + (A\bar{B}C + ABC) + (AB\bar{C} + ABC) $$
$$ F = BC(\bar{A}+A) + AC(\bar{B}+B) + AB(\bar{C}+C) = BC + AC + AB $$

This is the **majority function**: it outputs 1 when at least two of the three
inputs are 1.
:::

::: example Worked example 2.9 — using De Morgan
**Problem.** Simplify $F = \overline{\overline{A}+\overline{B}} + \overline{A+B}$.

**Solution.** Apply De Morgan to each term:

$$ \overline{\bar{A}+\bar{B}} = \bar{\bar{A}}\cdot\bar{\bar{B}} = A\cdot B,
\qquad \overline{A+B} = \bar{A}\cdot\bar{B} $$

$$ F = AB + \bar{A}\bar{B} = \overline{A \oplus B} $$

So the circuit is simply an XNOR gate — an equality detector.
:::

### Simplification using Karnaugh maps

A **Karnaugh map** (K-map) is a truth table redrawn as a grid, with the rows and
columns labelled in **Gray code** order (00, 01, 11, 10) so that any two
neighbouring cells differ in exactly one variable. Then:

1. Write a 1 in every cell whose minterm is in the function.
2. Ring **rectangular groups** of 1s whose size is a power of two — 1, 2, 4, 8 —
   making each group as large as possible. Groups may overlap, and they wrap
   around the edges of the map.
3. For each group write the product of the variables that stay **constant**
   inside it; drop the variables that change.
4. OR the group terms together.

```figure caption="Three-variable K-map for $F = \sum m(1,2,3,5,7)$. The group of four (column pairs where $C=1$) gives $C$; the group of two gives $\bar{A}B$; so $F = C + \bar{A}B$."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
fig, ax = plt.subplots(figsize=(4.6,2.6))
RED='#A8271F'
cols=['00','01','11','10']; rows=['0','1']
mint=[[0,1,3,2],[4,5,7,6]]
ones={1,2,3,5,7}
W,H=0.95,0.80
for j,c in enumerate(cols):
    ax.text(0.30+W*(j+0.5),2*H+0.14,c,ha='center',va='bottom',fontsize=8.6,color=INK)
for i,r in enumerate(rows):
    ax.text(0.18,(1-i)*H+H/2,r,ha='right',va='center',fontsize=8.6,color=INK)
ax.text(0.22,2*H+0.16,'A',ha='right',va='bottom',fontsize=9.0,color=ACCENT,fontweight='bold')
ax.text(0.30+2*W,2*H+0.52,'BC',ha='center',va='bottom',fontsize=9.0,color=ACCENT,fontweight='bold')
for i in range(2):
    for j in range(4):
        x=0.30+W*j; y=(1-i)*H
        ax.add_patch(Rectangle((x,y),W,H,fc='none',ec=MUTED,lw=0.9))
        m=mint[i][j]
        ax.text(x+W/2,y+H/2,'1' if m in ones else '0',ha='center',va='center',
                fontsize=10.5,color=INK if m in ones else GRID)
        ax.text(x+0.07,y+H-0.07,'$m_{%d}$'%m,ha='left',va='top',fontsize=6.4,color=MUTED)
# group of four: columns 01 and 11 (C=1) across both rows
ax.add_patch(FancyBboxPatch((0.30+W*1+0.07,0.07),2*W-0.14,2*H-0.14,
    boxstyle="round,pad=0,rounding_size=0.22",fc='none',ec=ACCENT,lw=1.8,zorder=6))
ax.text(0.30+W*2,-0.08,'group of four: $C$',ha='center',va='top',fontsize=8.6,color=ACCENT)
# group of two: row A=0, columns 11 and 10 (m3, m2)
ax.add_patch(FancyBboxPatch((0.30+W*2+0.15,H+0.15),2*W-0.30,H-0.30,
    boxstyle="round,pad=0,rounding_size=0.18",fc='none',ec=RED,lw=1.8,ls=(0,(4,2)),zorder=6))
ax.text(0.30+4*W+0.12,H+H/2,'group of two:\n'+r'$\bar{A}B$',ha='left',va='center',fontsize=8.6,color=RED)
ax.text(0.30+2*W,-0.62,r'$F = C + \bar{A}B$',ha='center',va='top',fontsize=10.5,color=INK)
ax.set_xlim(-0.05,5.75); ax.set_ylim(-1.25,2.60); ax.set_aspect('equal'); ax.axis('off')
```

::: example Worked example 2.10 — four-variable K-map
**Problem.** Simplify $F(A,B,C,D) = \sum m(0,1,4,5,6,7,10,12,13,14,15)$.

**Solution.** Plot the map (see the figure). Three groups cover every 1:

- a group of **eight**: rows $AB = 01$ and $AB = 11$, i.e. every cell with
  $B = 1$ → term **$B$**;
- a group of **four**: the top-left $2\times2$ block, where $A = 0$ and $C = 0$
  → term **$\bar{A}\bar{C}$**;
- a group of **two**: $m_{10}$ and $m_{14}$, where $A=1$, $C=1$, $D=0$ → term
  **$AC\bar{D}$**.

$$ F = B + \bar{A}\bar{C} + AC\bar{D} $$

Verify one cell: $m_{11} = 1011$ is **not** in the list. Here $B=0$, $A=1$ so
$\bar{A}\bar{C}=0$, and $D=1$ so $AC\bar{D}=0$. The expression gives 0 ✓
:::

```figure caption="Four-variable K-map for $F = \sum m(0,1,4,5,6,7,10,12,13,14,15)$, with the groups of eight, four and two ringed. Overlapping is allowed and each group must be as large as possible."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
fig, ax = plt.subplots(figsize=(4.7,3.4))
RED='#A8271F'; GRN='#2e8b57'
cols=['00','01','11','10']; rows=['00','01','11','10']
mint=[[0,1,3,2],[4,5,7,6],[12,13,15,14],[8,9,11,10]]
ones={0,1,4,5,6,7,10,12,13,14,15}
W,H=0.82,0.72
X0,Y0=0.55,0.30
for j,c in enumerate(cols):
    ax.text(X0+W*(j+0.5),Y0+4*H+0.12,c,ha='center',va='bottom',fontsize=8.4,color=INK)
for i,r in enumerate(rows):
    ax.text(X0-0.10,Y0+(3-i)*H+H/2,r,ha='right',va='center',fontsize=8.4,color=INK)
ax.text(X0-0.10,Y0+4*H+0.14,'AB',ha='right',va='bottom',fontsize=9.0,color=ACCENT,fontweight='bold')
ax.text(X0+2*W,Y0+4*H+0.50,'CD',ha='center',va='bottom',fontsize=9.0,color=ACCENT,fontweight='bold')
for i in range(4):
    for j in range(4):
        x=X0+W*j; y=Y0+(3-i)*H
        ax.add_patch(Rectangle((x,y),W,H,fc='none',ec=MUTED,lw=0.9))
        m=mint[i][j]
        ax.text(x+W/2,y+H/2,'1' if m in ones else '0',ha='center',va='center',
                fontsize=10.0,color=INK if m in ones else GRID)
        ax.text(x+0.06,y+H-0.06,'$m_{%d}$'%m,ha='left',va='top',fontsize=6.2,color=MUTED)
# group of 8: rows AB=01 and AB=11  (i = 1 and 2)
ax.add_patch(FancyBboxPatch((X0+0.06,Y0+H+0.06),4*W-0.12,2*H-0.12,
    boxstyle="round,pad=0,rounding_size=0.20",fc='none',ec=ACCENT,lw=1.9,zorder=6))
ax.text(X0+4*W+0.12,Y0+2*H,'group of\neight: $B$',ha='left',va='center',fontsize=8.6,color=ACCENT)
# group of 4: A'C'  -> rows i=0,1 ; cols j=0,1
ax.add_patch(FancyBboxPatch((X0+0.16,Y0+2*H+0.16),2*W-0.32,2*H-0.32,
    boxstyle="round,pad=0,rounding_size=0.16",fc='none',ec=GRN,lw=1.9,ls=(0,(5,2)),zorder=7))
ax.text(X0+W,-0.08,r'group of four: $\bar{A}\bar{C}$',ha='center',va='top',
        fontsize=8.6,color=GRN)
# group of 2: m10 (row i=3, col j=3) and m14 (row i=2, col j=3)
ax.add_patch(FancyBboxPatch((X0+3*W+0.13,Y0+0.13),W-0.26,2*H-0.26,
    boxstyle="round,pad=0,rounding_size=0.14",fc='none',ec=RED,lw=1.9,ls=(0,(3,2)),zorder=7))
ax.text(X0+4*W+0.12,Y0+H*0.70,'group of\ntwo: '+r'$AC\bar{D}$',ha='left',va='center',fontsize=8.6,color=RED)
ax.text(X0+2*W,-0.62,r'$F = B + \bar{A}\bar{C} + AC\bar{D}$',ha='center',va='top',
        fontsize=10.5,color=INK)
ax.set_xlim(0.0,5.75); ax.set_ylim(-1.30,3.90); ax.set_aspect('equal'); ax.axis('off')
```

::: caution Gray code order, not binary order
The columns of a K-map are labelled 00, **01, 11, 10** — not 00, 01, 10, 11. If
you label them in ordinary binary order, adjacent cells no longer differ by one
variable and every grouping you make will be wrong.
:::

## 2.8 Verification of the laws of Boolean algebra using truth tables

To *verify* a law, build one column for the left-hand side and one for the
right-hand side, fill in every row, and show the two columns are identical.

**De Morgan's first theorem:** $\overline{A+B} = \bar{A}\cdot\bar{B}$

| A | B | $A+B$ | $\overline{A+B}$ | $\bar{A}$ | $\bar{B}$ | $\bar{A}\cdot\bar{B}$ |
|---|---|---|---|---|---|---|
| 0 | 0 | 0 | **1** | 1 | 1 | **1** |
| 0 | 1 | 1 | **0** | 1 | 0 | **0** |
| 1 | 0 | 1 | **0** | 0 | 1 | **0** |
| 1 | 1 | 1 | **0** | 0 | 0 | **0** |

Columns 4 and 7 agree in every row, so the theorem is proved.

**De Morgan's second theorem:** $\overline{A\cdot B} = \bar{A} + \bar{B}$

| A | B | $A\cdot B$ | $\overline{A\cdot B}$ | $\bar{A}$ | $\bar{B}$ | $\bar{A}+\bar{B}$ |
|---|---|---|---|---|---|---|
| 0 | 0 | 0 | **1** | 1 | 1 | **1** |
| 0 | 1 | 0 | **1** | 1 | 0 | **1** |
| 1 | 0 | 0 | **1** | 0 | 1 | **1** |
| 1 | 1 | 1 | **0** | 0 | 0 | **0** |

**Distributive law:** $A + BC = (A+B)(A+C)$

| A | B | C | $BC$ | $A+BC$ | $A+B$ | $A+C$ | $(A+B)(A+C)$ |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | **0** | 0 | 0 | **0** |
| 0 | 0 | 1 | 0 | **0** | 0 | 1 | **0** |
| 0 | 1 | 0 | 0 | **0** | 1 | 0 | **0** |
| 0 | 1 | 1 | 1 | **1** | 1 | 1 | **1** |
| 1 | 0 | 0 | 0 | **1** | 1 | 1 | **1** |
| 1 | 0 | 1 | 0 | **1** | 1 | 1 | **1** |
| 1 | 1 | 0 | 0 | **1** | 1 | 1 | **1** |
| 1 | 1 | 1 | 1 | **1** | 1 | 1 | **1** |

**Absorption law:** $A + AB = A$, and **redundancy:** $A + \bar{A}B = A + B$

| A | B | $AB$ | $A+AB$ | $\bar{A}B$ | $A+\bar{A}B$ | $A+B$ |
|---|---|---|---|---|---|---|
| 0 | 0 | 0 | **0** | 0 | **0** | **0** |
| 0 | 1 | 0 | **0** | 1 | **1** | **1** |
| 1 | 0 | 0 | **1** | 0 | **1** | **1** |
| 1 | 1 | 1 | **1** | 0 | **1** | **1** |

Column 4 equals column 1 (absorption); column 6 equals column 7 (redundancy).

::: tip Writing a truth-table proof in the exam
State the law in symbols first, then draw the table with **one column per
intermediate step**, and finish with the sentence "the columns for LHS and RHS
are identical for all input combinations, hence the law is verified." Examiners
award marks for the intermediate columns, so never jump straight to the answer.
:::

## Chapter summary

- A positional number in base $r$ has value $\sum d_i r^{i}$. To decimal: expand
  positionally. From decimal: divide repeatedly (integers, read **up**) or
  multiply repeatedly (fractions, read **down**).
- Binary ↔ octal groups **3 bits** per digit; binary ↔ hex groups **4 bits**.
  Octal ↔ hex must go through binary.
- Binary addition: $1+1 = 10$; subtraction borrows a **2**.
- 1's complement = invert all bits, and the **end-around carry is added back**.
  2's complement = 1's complement + 1, and the **carry is discarded**. No carry
  in either method means the answer is negative — recomplement and add a minus.
- Boolean algebra (Boole 1854, applied by Shannon 1938) uses only 0 and 1, with
  $+$ = OR, $\cdot$ = AND and a bar for NOT.
- Seven gates: AND, OR, NOT, NAND, NOR, XOR ("different"), XNOR ("same").
  NAND and NOR are **universal**.
- Half adder: $S = A\oplus B$, $C = A\cdot B$. Full adder:
  $S = A\oplus B\oplus C_{in}$, $C_{out} = AB + (A\oplus B)C_{in}$.
- Key laws: $A+\bar{A}=1$, $A\cdot\bar{A}=0$, $A+AB=A$, $A+\bar{A}B = A+B$,
  $A+BC = (A+B)(A+C)$, and De Morgan $\overline{A+B} = \bar{A}\bar{B}$,
  $\overline{AB} = \bar{A}+\bar{B}$.
- A K-map is labelled in **Gray code** (00, 01, 11, 10); ring the largest
  possible power-of-two groups, allow overlap and wrap-around, and keep only the
  variables that stay constant in a group.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. $(1011)_2$ in decimal is <span class="marks">[1]</span>
   (a) 9 (b) 11 (c) 13 (d) 15
2. The hexadecimal equivalent of $(11011110)_2$ is <span class="marks">[1]</span>
   (a) DE (b) ED (c) 9E (d) BE
3. The 2's complement of $(0101)_2$ is <span class="marks">[1]</span>
   (a) 1010 (b) 1011 (c) 0110 (d) 1101
4. Which gate gives output 1 only when its two inputs are different? <span class="marks">[1]</span>
   (a) AND (b) NOR (c) XOR (d) XNOR
5. According to De Morgan's theorem, $\overline{A\cdot B}$ equals <span class="marks">[1]</span>
   (a) $\bar{A}\cdot\bar{B}$ (b) $\bar{A}+\bar{B}$ (c) $A+B$ (d) $\overline{A+B}$
6. $A + \bar{A}B$ simplifies to <span class="marks">[1]</span>
   (a) $A$ (b) $B$ (c) $A+B$ (d) $AB$
7. Which pair of gates is called universal? <span class="marks">[1]</span>
   (a) AND and OR (b) NAND and NOR (c) XOR and XNOR (d) NOT and AND
8. The carry output of a half adder is <span class="marks">[1]</span>
   (a) $A \oplus B$ (b) $A + B$ (c) $A\cdot B$ (d) $\overline{A\cdot B}$

::: note Answers to Group A
**1.** (b) — $8+0+2+1 = 11$.
**2.** (a) — 1101 = D, 1110 = E.
**3.** (b) — 1's complement of 0101 is 1010; add 1 to get 1011.
**4.** (c) — XOR is the "difference" detector.
**5.** (b) — break the bar and change AND to OR.
**6.** (c) — redundancy law.
**7.** (b) — any function can be built from NAND alone or NOR alone.
**8.** (c) — the carry is generated only when both inputs are 1.
:::

**Group B — Short answer (5 marks each)**

1. Convert (a) $(347)_{10}$ to binary, octal and hexadecimal, and
   (b) $(10110111)_2$ to decimal, octal and hexadecimal. <span class="marks">[5]</span>
2. Perform the following binary operations: (a) $10110 + 1101$,
   (b) $110100 - 10111$, (c) $1011 \times 110$, (d) $100101 \div 111$. <span class="marks">[5]</span>
3. Subtract $(0111)_2$ from $(1101)_2$ using (a) the 1's complement method and
   (b) the 2's complement method. Show every step. <span class="marks">[5]</span>
4. State and verify De Morgan's two theorems using truth tables. <span class="marks">[5]</span>
5. Simplify $F = \bar{A}\bar{B}C + \bar{A}BC + A\bar{B}C + ABC$ using the laws of
   Boolean algebra, and draw the logic circuit of the simplified expression. <span class="marks">[5]</span>
6. Draw the logic symbol and write the truth table and Boolean function of the
   NAND, NOR, XOR and XNOR gates. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** (a) $347 \div 2$ repeatedly gives remainders 1,1,0,1,1,0,1,0,1 read
upwards: $(101011011)_2$. Grouping in threes: 101 011 011 → $(533)_8$. Grouping
in fours: 0001 0101 1011 → $(15B)_{16}$.
Check: $1(256)+5(16)+11 = 347$ ✓

(b) $(10110111)_2 = 128+32+16+4+2+1 = (183)_{10}$. In threes: 010 110 111 →
$(267)_8$. In fours: 1011 0111 → $(B7)_{16}$.

**2.** (a) $10110 + 1101 = 100011$ (22 + 13 = 35).
(b) $110100 - 10111 = 011101$ (52 − 23 = 29).
(c) $1011 \times 110 = 1000010$ (11 × 6 = 66).
(d) $100101 \div 111 = 101$ remainder $10$ (37 ÷ 7 = 5 remainder 2).

**3.** $(1101)_2 - (0111)_2$, i.e. $13 - 7 = 6$.
(a) 1's complement of 0111 = 1000. $1101 + 1000 = 1\,0101$. There is a carry
out, so add it back: $0101 + 1 = 0110 = 6$.
(b) 2's complement of 0111 = 1000 + 1 = 1001. $1101 + 1001 = 1\,0110$. Discard
the carry: $0110 = 6$ ✓

**5.** $F = C(\bar{A}\bar{B} + \bar{A}B + A\bar{B} + AB)
= C\left[\bar{A}(\bar{B}+B) + A(\bar{B}+B)\right] = C(\bar{A}+A) = C\cdot 1 = C$.
The "circuit" is a single wire from input $C$ to the output — all the gates can
be removed.
:::

**Group C — Long answer (8 marks each)**

1. (a) Convert $(2C5)_{16}$ to decimal, binary and octal. <span class="marks">[3]</span>
   (b) Using the 2's complement method in 8 bits, evaluate $58 - 91$ and verify
   your answer in decimal. <span class="marks">[5]</span>
2. (a) Define a logic gate. Draw the symbol and truth table of all seven basic
   gates. <span class="marks">[4]</span>
   (b) Draw the logic circuit of a **full adder** using two half adders and one
   OR gate, write its truth table, and derive the expressions for the sum and
   the carry. <span class="marks">[4]</span>
3. Simplify $F(A,B,C,D) = \sum m(0,1,2,3,8,9,10,11,13,15)$ using a Karnaugh map.
   Show the map, the groupings and the final simplified expression, and draw the
   resulting logic circuit. <span class="marks">[8]</span>

::: note Answers to Group C
**1. (a)** $(2C5)_{16} = 2(256) + 12(16) + 5 = 512 + 192 + 5 = (709)_{10}$.
Each hex digit is four bits: 2 = 0010, C = 1100, 5 = 0101, so
$(2C5)_{16} = (001011000101)_2$. Regroup the binary in threes from the right:
001 011 000 101 → $(1305)_8$. Check: $1(512)+3(64)+0+5 = 709$ ✓

**1. (b)** $58 = (00111010)_2$, $91 = (01011011)_2$. 1's complement of 91 is
10100100, so the 2's complement is **10100101**.
$00111010 + 10100101 = 11011111$, with **no carry out**, so the result is
negative. The 2's complement of 11011111 is $00100000 + 1 = 00100001 = 33$.
Therefore $58 - 91 = -33$ ✓

**3.** Plot the minterms on a four-variable map with rows $AB$ = 00, 01, 11, 10
and columns $CD$ = 00, 01, 11, 10.

- $m_0,m_1,m_2,m_3,m_8,m_9,m_{10},m_{11}$ form a group of **eight** — the two
  rows $AB=00$ and $AB=10$, which are adjacent by wrap-around. In all eight
  cells $B = 0$, so the term is $\bar{B}$.
- $m_9,m_{11},m_{13},m_{15}$ form a group of **four**: in all of them $A = 1$
  and $D = 1$, so the term is $AD$.

$$ F = \bar{B} + AD $$

Check $m_{13} = 1101$: $B=1$ so $\bar{B}=0$, but $A=1$ and $D=1$ so $AD=1$,
giving $F=1$ ✓ and $m_{12} = 1100$: $\bar{B}=0$ and $D=0$ so $F=0$, and 12 is
indeed not in the list ✓

The circuit is one NOT gate on $B$, one AND gate for $A$ and $D$, and one OR
gate combining them.
:::
