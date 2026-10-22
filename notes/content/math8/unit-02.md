---
subject: Mathematics
grade: 8
unit: 2
title: Whole Numbers
hours: 0
area: Compulsory Mathematics
---

The number system you use every day has ten digits, 0 to 9, and we call it
**decimal** or base ten. Nothing is special about ten; it is only the number of
fingers people happen to have. A computer uses two digits because a switch is
either off or on, and a clock has used twelves and sixties for as long as anyone
can remember. This chapter shows how to write the same quantity in different
bases and how to do arithmetic in them.

::: key What this chapter asks of you
You should be able to explain what a place value means in any base, convert a
binary or quinary number into decimal and back, convert between any two bases
through decimal, and add, subtract and multiply numbers in base 2 and base 5.
:::

## 2.1 Place value in the decimal system

In the decimal system the value of a digit depends on its position. Moving one
place to the left multiplies the value by 10.

$$4725=4\times10^3+7\times10^2+2\times10^1+5\times10^0$$

Every base works the same way with a different multiplier. In **base 2**
(binary) only the digits 0 and 1 are allowed, and each place is worth twice the
one on its right. In **base 5** (quinary) only 0–4 are allowed.

| Base | Allowed digits | Place values |
|---|---|---|
| 10 | 0–9 | $\dots,10^3,10^2,10^1,10^0$ |
| 5 | 0–4 | $\dots,5^3,5^2,5^1,5^0$ |
| 2 | 0, 1 | $\dots,2^3,2^2,2^1,2^0$ |

| Power | 2 to that power | 5 to that power |
|---|---|---|
| $2^0,5^0$ | 1 | 1 |
| $2^1,5^1$ | 2 | 5 |
| $2^2,5^2$ | 4 | 25 |
| $2^3,5^3$ | 8 | 125 |
| $2^4,5^4$ | 16 | 625 |
| $2^5,5^5$ | 32 | 3125 |
| $2^6$ | 64 | — |
| $2^7$ | 128 | — |
| $2^8$ | 256 | — |
| $2^9$ | 512 | — |

The decimal system is also called the **Hindu–Arabic numeration system**. The
**binary** system is used in computers and electric circuits, where a switch has
only two states: ON (1) and OFF (0).

::: key Showing the base
A number in another base carries its base as a small subscript (suffix):
$(1011)_2$ or $1011_2$ is binary, $(243)_5$ or $243_5$ is quinary. A number with
no suffix is decimal. A digit 2, 3 or 4 can never appear in a binary number, and
5–9 never in a quinary number — so $(1021)_2$ and $(375)_5$ are impossible.
:::

### 2.1.1 Expanded form in powers of 2 and of 5

To express a decimal number **as powers of 2**, break it into the largest
powers of 2 that fit; for **powers of 5**, use 125, 25, 5, 1.

::: example Expressing a number in powers of 2 and 5
**Problem.** Express 43 in powers of 2 and 59 in powers of 5.

**Solution.**
$43=32+8+2+1$

$=1\times2^5+0\times2^4+1\times2^3+0\times2^2+1\times2^1+1\times2^0$

So $43=(101011)_2$.

$59=2\times25+1\times5+4$

$=2\times5^2+1\times5^1+4\times5^0$

So $59=(214)_5$.
:::

::: caution Do not skip the zero places
In the expansion of 43 there is no 16 and no 4, but $0\times2^4$ and
$0\times2^2$ must still be written. If you drop them, the binary number
becomes $1111_2=15$, which is wrong.
:::

## 2.2 Conversion from another base to decimal

**Rule.** Expand the number by place values and add.

::: example Binary to decimal
**Problem.** Convert $(1101)_2$ into decimal.

**Solution.** Write the place values under the digits:

$$(1101)_2=1\times2^3+1\times2^2+0\times2^1+1\times2^0$$

$$=8+4+0+1=13$$

**Answer.** $(1101)_2=(13)_{10}$.

**Check.** Count upwards in binary and see where it lands:
1, 10, 11, 100, 101, 110, 111, 1000, 1001, 1010, 1011, 1100, 1101 — that is the
13th number, counting the first as 1 in decimal. Agrees.
:::

::: example Quinary to decimal
**Problem.** Convert $(342)_5$ into decimal.

**Solution.**

$$(342)_5=3\times5^2+4\times5^1+2\times5^0=75+20+2=97$$

**Answer.** $(342)_5=(97)_{10}$.

**Check.** The largest power used is $5^2=25$, and $3\times25=75$; the remainder
$97-75=22$ is $4\times5+2$, which is the last two digits ✓.
:::

## 2.3 Conversion from decimal to another base

**Rule.** Divide repeatedly by the base and read the remainders **from the
bottom upwards**.

```figure caption="Converting 45 into base 5 by repeated division. Each remainder is written on the right; the remainders are read from the bottom up, so $45=(140)_5$."
fig, ax = plt.subplots(figsize=(4.6, 2.8))
ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
rows = [("5", "45", ""), ("5", "9", "0"), ("5", "1", "4"), ("", "0", "1")]
for i, (d, q, r) in enumerate(rows):
    y = 5.0 - i * 1.15
    ax.text(1.0, y, d, ha="center", va="center", fontsize=11, color=INK)
    ax.text(2.4, y, q, ha="center", va="center", fontsize=11, color=INK)
    if r:
        ax.text(3.9, y, r, ha="center", va="center", fontsize=11, color=ACCENT, weight="bold")
    if d:
        ax.plot([1.45, 1.45], [y - 0.45, y + 0.45], color=INK, lw=1.0)
        ax.plot([1.45, 3.2], [y - 0.55, y - 0.55], color=INK, lw=1.0)
ax.text(3.9, 5.75, "remainder", ha="center", fontsize=8, color=MUTED)
ax.annotate("", xy=(4.6, 3.85), xytext=(4.6, 1.55),
            arrowprops=dict(arrowstyle="->", color=ACCENT, lw=1.4))
ax.text(5.0, 2.7, "read upwards", fontsize=9, color=ACCENT, va="center")
ax.text(5.0, 1.1, "$45=(140)_5$", fontsize=11, color=INK)
ax.text(5.0, 0.35, "check: 1×25 + 4×5 + 0 = 45", fontsize=8.5, color=MUTED)
```

::: example Decimal to binary
**Problem.** Convert $(45)_{10}$ into binary.

**Solution.** Divide by 2 and record each remainder.

| Division | Remainder |
|---|---|
| 45 ÷ 2 = 22 | 1 |
| 22 ÷ 2 = 11 | 0 |
| 11 ÷ 2 = 5 | 1 |
| 5 ÷ 2 = 2 | 1 |
| 2 ÷ 2 = 1 | 0 |
| 1 ÷ 2 = 0 | 1 |

Reading the remainders from the bottom upwards:

$$(45)_{10}=(101101)_2$$

**Check.** $32+0+8+4+0+1=45$ ✓.
:::

::: example Decimal to base 5
**Problem.** Convert $(323)_{10}$ into base 5.

**Solution.**

| Division | Remainder |
|---|---|
| 323 ÷ 5 = 64 | 3 |
| 64 ÷ 5 = 12 | 4 |
| 12 ÷ 5 = 2 | 2 |
| 2 ÷ 5 = 0 | 2 |

So $(323)_{10}=(2243)_5$.

**Check.** $2\times125+2\times25+4\times5+3=250+50+20+3=323$ ✓.
:::

::: caution The remainder on the last line
At the last division the quotient becomes 0, and the number you divided (1, or
2, or whatever is left) is itself the final remainder. Leaving it out is the
commonest error in base conversion. The number of digits is the number of
divisions, counting that last line.
:::

## 2.4 Conversion between two non-decimal bases

To change from one base to another, go through decimal. The two steps are
"expand" and then "divide".

::: example Base 2 to base 5
**Problem.** Convert $(10110)_2$ into base 5.

**Solution.** **Step 1: to decimal.**

$$(10110)_2=16+0+4+2+0=22$$

**Step 2: to base 5.** Divide 22 by 5: $22\div5=4$ remainder 2, then
$4\div5=0$ remainder 4. Reading upwards, $(22)_{10}=(42)_5$.

**Answer.** $(10110)_2=(42)_5$.

**Check.** $4\times5+2=22$ ✓, which matches the decimal value found in step 1.
:::

### 2.4.1 Comparing numbers written in different bases

Numbers in different bases cannot be compared digit by digit. Convert both to
decimal first.

::: example Which is larger?
**Problem.** Which of $(110011)_2$ and $(144)_5$ is larger? Find their
difference.

**Solution.**
$(110011)_2=32+16+0+0+2+1=51$

$(144)_5=1\times25+4\times5+4=25+20+4=49$

Since $51>49$, $(110011)_2$ is larger. Difference $=51-49=2$.
:::

::: example Quinary to binary
**Problem.** Convert $(43)_5$ into binary.

**Solution.** **Step 1:** $(43)_5=4\times5+3=23$.

**Step 2:** $23\div2=11$ r 1, $11\div2=5$ r 1, $5\div2=2$ r 1,
$2\div2=1$ r 0, $1\div2=0$ r 1. Reading upwards, $23=(10111)_2$.

**Answer.** $(43)_5=(10111)_2$. Check: $16+4+2+1=23$ ✓.
:::

## 2.5 Arithmetic in other bases

Add, subtract and multiply exactly as in decimal, but carry and borrow with the
base instead of with ten.

- In base 2, $1+1=10$: write 0 and carry 1.
- In base 5, $4+3=12$: write 2 and carry 1, because 7 is 1 five and 2 units.

::: example Addition in base 2
**Problem.** Add $(1011)_2$ and $(1101)_2$.

**Solution.** Write them one under the other and add column by column from the
right.

| Position | Work | Written | Carry |
|---|---|---|---|
| units | $1+1=2=(10)_2$ | 0 | 1 |
| twos | $1+0+1=2=(10)_2$ | 0 | 1 |
| fours | $0+1+1=2=(10)_2$ | 0 | 1 |
| eights | $1+1+1=3=(11)_2$ | 1 | 1 |
| sixteens | carry only | 1 | 0 |

So $(1011)_2+(1101)_2=(11000)_2$.

**Check in decimal.** $1011_2=11$ and $1101_2=13$; $11+13=24$, and
$11000_2=16+8=24$ ✓.
:::

::: example Subtraction in base 5
**Problem.** Subtract $(213)_5$ from $(402)_5$.

**Solution.** Work column by column from the right. Borrowing 1 from the next
place gives **5** (not 10) to the place on its right.

- **Units:** $2-3$ is not possible. The fives digit is 0, so first borrow 1 from
  the twenty-fives place: $4\to3$, and the fives place becomes 5. Now borrow 1
  from the fives place: $5\to4$, and the units become $2+5=7$. $7-3=4$.
- **Fives:** $4-1=3$.
- **Twenty-fives:** $3-2=1$.

So $(402)_5-(213)_5=(134)_5$.

**Check in decimal.** $402_5=4\times25+0+2=102$ and $213_5=2\times25+5+3=58$;
$102-58=44$. And $134_5=25+15+4=44$ ✓.
:::

::: example Multiplication in base 5
**Problem.** Multiply $(23)_5$ by $(4)_5$.

**Solution.** $3\times4=12$; in base 5, $12=2\times5+2$, so write 2 and carry 2.
Then $2\times4=8$, plus the carry 2 gives 10; in base 5, $10=2\times5+0$, so
write 0 and carry 2. The final carry is 2.

So $(23)_5\times(4)_5=(202)_5$.

**Check in decimal.** $23_5=13$ and $4_5=4$; $13\times4=52$. And
$202_5=2\times25+0+2=52$ ✓.
:::

::: tip The decimal check is your safety net
Every base conversion and every base calculation can be checked by converting to
decimal, doing the arithmetic there, and converting back. In an examination it
costs thirty seconds and it catches a slipped carry, which is where nearly all
the marks are lost in this chapter.
:::

## 2.6 Properties of whole numbers at a glance

| Property | Addition | Multiplication |
|---|---|---|
| Closure | $a + b$ is a whole number | $a \times b$ is a whole number |
| Commutative | $a + b = b + a$ | $a \times b = b \times a$ |
| Associative | $(a+b)+c = a+(b+c)$ | $(ab)c = a(bc)$ |
| Identity | $a + 0 = a$ | $a \times 1 = a$ |
| Distributive | — | $a(b+c) = ab + ac$ |

Subtraction and division are **not** closed on whole numbers: $3 - 5$ and
$3 \div 5$ both leave the set.

```figure caption="The distributive property as areas. A rectangle of width a and length (b + c) can be split into two rectangles, so a(b + c) = ab + ac."
fig, ax = plt.subplots(figsize=(4.7, 2.3))
ax.add_patch(matplotlib.patches.Rectangle((0.05, 0.2), 0.35, 0.5,
             facecolor=SERIES[0], alpha=0.75, edgecolor="white", linewidth=1.4))
ax.add_patch(matplotlib.patches.Rectangle((0.40, 0.2), 0.25, 0.5,
             facecolor=SERIES[2], alpha=0.75, edgecolor="white", linewidth=1.4))
ax.text(0.225, 0.45, "$a \\times b$", ha="center", va="center", color="white",
        fontsize=11)
ax.text(0.525, 0.45, "$a \\times c$", ha="center", va="center", color="white",
        fontsize=11)
ax.text(0.02, 0.45, "$a$", ha="right", va="center", color=INK, fontsize=10)
ax.text(0.225, 0.76, "$b$", ha="center", color=INK, fontsize=10)
ax.text(0.525, 0.76, "$c$", ha="center", color=INK, fontsize=10)
ax.text(0.80, 0.45, "$a(b+c)$\n$= ab + ac$", ha="center", va="center",
        color=INK, fontsize=9.5)
ax.set_xlim(0, 1)
ax.set_ylim(0.1, 0.9)
ax.axis("off")
```

::: example Using the properties to calculate quickly
**Question.** Evaluate mentally, naming the property used:
(i) $47 \times 25 \times 4$ (ii) $98 \times 7$ (iii) $36 + 58 + 64$

**Answer.**
(i) Associative: $47 \times (25 \times 4) = 47 \times 100 = \textbf{4700}$.
(ii) Distributive: $(100 - 2) \times 7 = 700 - 14 = \textbf{686}$.
(iii) Commutative and associative: $(36 + 64) + 58 = 100 + 58 = \textbf{158}$.
:::

::: note Activity — the mental-maths minute
In pairs, time each other for one minute on ten products such as
$25 \times 16$, $99 \times 8$, $48 + 37 + 52$. After the first round, discuss
which property made each one quick, then repeat. Nearly every pair improves on
the second attempt — the gain comes from choosing the property, not from
calculating faster.
:::

## Chapter summary

- A number in base $b$ uses only the digits $0$ to $b-1$, and each place is
  worth $b$ times the place on its right.
- To convert **to** decimal, expand by place values and add.
- To convert **from** decimal, divide repeatedly by the base and read the
  remainders from the bottom upwards.
- To convert between two other bases, go through decimal in two steps.
- To compare numbers in different bases, change both to decimal first.
- In base 2: $1+1=10$, and the place values are 1, 2, 4, 8, 16, …
- In base 5: $4+1=10$, and the place values are 1, 5, 25, 125, …
- Add, subtract and multiply as in decimal but carry and borrow with the base.
- Always check a base calculation by converting to decimal.

## Practice questions

**Group A — Objective (1 mark each)**

1. The decimal value of $(1101)_2$ is <span class="marks">[1]</span>
   (a) 11 (b) 13 (c) 15 (d) 26
2. The number of digits allowed in base 5 is <span class="marks">[1]</span>
   (a) 4 (b) 5 (c) 6 (d) 10
3. $(25)_{10}$ in binary is <span class="marks">[1]</span>
   (a) 11001 (b) 10101 (c) 11010 (d) 10011
4. The place value of the third digit from the right in base 5 is
   <span class="marks">[1]</span>
   (a) 5 (b) 10 (c) 25 (d) 125
5. $(1000)_2$ in decimal is <span class="marks">[1]</span>
   (a) 4 (b) 8 (c) 16 (d) 1000
6. $1+1$ in binary is written as <span class="marks">[1]</span>
   (a) 2 (b) 10 (c) 11 (d) 0

::: note Answers to Group A
**1.** (b) — $8+4+0+1=13$.
**2.** (b) — 0, 1, 2, 3 and 4 are the only digits used.
**3.** (a) — $16+8+1=25$.
**4.** (c) — $5^2=25$.
**5.** (b) — $2^3=8$.
**6.** (b) — two is written as 1 two and 0 units.
:::

**Group B — Short answer (2 marks each)**

1. Convert $(101101)_2$ into decimal. <span class="marks">[2]</span>
2. Convert $(243)_5$ into decimal. <span class="marks">[2]</span>
3. Convert $(100)_{10}$ into binary and into base 5.
   <span class="marks">[2]</span>
4. Add $(1101)_2$ and $(1011)_2$. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** $32+0+8+4+0+1=45$.
**2.** $2\times25+4\times5+3=50+20+3=73$.
**3.** In binary: $64+32+4=100$, so $(1100100)_2$. In base 5:
$100=4\times25$, so $(400)_5$.
**4.** $1101_2=13$ and $1011_2=11$; the sum is 24, which is $(11000)_2$.
:::

**Group C — Long answer (4 marks each)**

1. Convert $(4321)_5$ into decimal and then into binary, showing both steps.
   <span class="marks">[4]</span>
2. Perform $10101_2-1101_2$ and $34_5\times3_5$, and check each answer by
   converting to decimal. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** **To decimal.**
$4\times125+3\times25+2\times5+1=500+75+10+1=586$.
**To binary.** Divide 586 by 2 repeatedly: remainders 0, 1, 0, 1, 0, 0, 1, 0, 0,
1 read upwards give $1001001010_2$. Check:
$512+64+8+2=586$ ✓.
**2.** $10101_2=21$ and $1101_2=13$, so the difference is 8, which is $(1000)_2$.
For the product, $34_5=3\times5+4=19$ and $3_5=3$, so the product is 57.
Converting 57 into base 5: $57\div5=11$ r 2, $11\div5=2$ r 1, $2\div5=0$ r 2,
so $(212)_5$. Check: $2\times25+1\times5+2=57$ ✓.
:::

**Extra practice — textbook-style questions**

**1.** State the number system: (a) $(10011)_2$ (b) 350 (c) $(4023)_5$.
**2.** Write 546 in expanded form using powers of 10.
**3.** Express 25 as powers of 2 and as powers of 5.
**4.** Convert $(512)_{10}$ and $(7521)_{10}$ into the quinary system.
**5.** Convert $(142013)_5$ into decimal.
**6.** Which of $(1101)_2$ and $(24)_5$ is larger? Find their difference.
**7.** Convert $(10101)_2$ into quinary and $(144)_5$ into binary.

::: note Extra practice — answers
**1.** (a) binary (b) decimal (c) quinary.
**2.** $546=5\times10^2+4\times10^1+6\times10^0$.
**3.** $25=16+8+1=1\times2^4+1\times2^3+0\times2^2+0\times2^1+1\times2^0=(11001)_2$; $25=1\times5^2+0\times5^1+0\times5^0=(100)_5$.
**4.** $512\div5=102$ r 2, $102\div5=20$ r 2, $20\div5=4$ r 0, $4\div5=0$ r 4, so $512=(4022)_5$. Similarly $7521=(220041)_5$ (remainders 1, 4, 0, 0, 2, 2 read upwards). Check: $2\times3125+2\times625+0+0+4\times5+1=6250+1250+20+1=7521$ ✓.
**5.** $1\times3125+4\times625+2\times125+0\times25+1\times5+3=3125+2500+250+0+5+3=5883$.
**6.** $(1101)_2=13$, $(24)_5=14$; $(24)_5$ is larger by 1.
**7.** $(10101)_2=21=4\times5+1=(41)_5$. $(144)_5=49=32+16+1=(110001)_2$.
:::

## Objective practice

**Choose the correct answer.** <span class="marks">[5×1=5]</span>

**1.** The smallest whole number is
   (a) $-1$ (b) 0 (c) 1 (d) there is none
**2.** $17\times(10+3)=170+51$ illustrates the
   (a) commutative property (b) associative property (c) distributive property (d) identity property
**3.** Which operation is **not** closed on whole numbers?
   (a) addition (b) multiplication (c) subtraction (d) none
**4.** The identity element for multiplication is
   (a) 0 (b) 1 (c) $-1$ (d) 10
**5.** $125\times8\times7$ is quickest as
   (a) $(125\times8)\times7$ (b) $125\times(8\times7)$ (c) $8\times(125\times7)$ (d) any order is equally quick

::: note Objective practice — answers
**1.** (b) — whole numbers start at 0. **2.** (c) — distributive over addition. **3.** (c) — $3-5$ leaves the set. **4.** (b) — 1. **5.** (a) — $125\times8=1000$ first.
:::
