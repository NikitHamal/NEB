---
subject: Mathematics
grade: 10
unit: 8
title: Highest Common Factor and Lowest Common Multiple
hours: 0
area: Compulsory Mathematics
---

The **highest common factor (HCF)** is the biggest thing that divides every given expression; the **lowest common multiple (LCM)** is the smallest thing that every given expression divides. You already know both for numbers. In Grade 10 the same two ideas are applied to **algebraic expressions** — and they are needed in the next chapters, because adding or simplifying algebraic fractions means finding a common denominator, which is an LCM. The key skill throughout is **factorisation**: once each expression is written as a product of factors, the HCF and LCM can be read off almost without calculation.

::: key What the SEE asks from this chapter
The usual questions: (i) find the **HCF and LCM of two or three expressions** after factorising (3 or 4 marks); (ii) use $\text{HCF}\times\text{LCM}=$ product of the two expressions to **find the missing expression**; (iii) a small word problem on numbers (bells, ropes, tiles). Factorise every expression completely first, and write the final answer **in factor form**.
:::

## 8.1 Highest Common Factor and Lowest Common Multiple: concepts, formulas and worked problems

### Revision with numbers

A **factor** divides exactly. A **multiple** is what you get by multiplying. The factors of 12 are 1, 2, 3, 4, 6, 12; the multiples of 12 are 12, 24, 36, … A **prime** number has exactly two factors, 1 and itself.

::: definition HCF and LCM
- The **HCF** (or GCD, greatest common divisor) of given numbers is the **greatest** number that divides each of them exactly.
- The **LCM** of given numbers is the **least** number that is exactly divisible by each of them.
:::

Prime factorisation gives both at once.

::: key Reading HCF and LCM from prime factors
Write each number as a product of prime powers.

- **HCF** $=$ product of the primes that are **common to all**, each with its **lowest** power.
- **LCM** $=$ product of **all** the primes that appear, each with its **highest** power.
:::

```figure caption="Prime factor tree of 360. Splitting each number until only primes remain gives 360 = 2³ × 3² × 5."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.2, 2.8))
def node(x, y, s, prime=False):
    ax.text(x, y, s, ha='center', va='center', fontsize=9.5, fontweight='bold' if prime else 'normal',
            color=ACCENT if prime else INK,
            bbox=dict(boxstyle='circle,pad=0.25', fc='#dbeafe' if prime else 'white', ec=ACCENT if prime else MUTED, lw=1.0))
def edge(x1, y1, x2, y2):
    ax.plot([x1, x2], [y1 - 0.18, y2 + 0.18], color=MUTED, lw=1.0, zorder=0)
node(0, 5, '360')
node(-1.2, 4, '2', True); node(1.2, 4, '180')
node(0.0, 3, '2', True); node(2.4, 3, '90')
node(1.2, 2, '2', True); node(3.6, 2, '45')
node(2.4, 1, '3', True); node(4.8, 1, '15')
node(3.6, 0, '3', True); node(6.0, 0, '5', True)
for a, b in [((0,5),(-1.2,4)), ((0,5),(1.2,4)), ((1.2,4),(0,3)), ((1.2,4),(2.4,3)), ((2.4,3),(1.2,2)), ((2.4,3),(3.6,2)),
             ((3.6,2),(2.4,1)), ((3.6,2),(4.8,1)), ((4.8,1),(3.6,0)), ((4.8,1),(6.0,0))]:
    edge(a[0], a[1], b[0], b[1])
ax.text(3.3, 4.2, '360 = 2 × 2 × 2 × 3 × 3 × 5\n      = 2³ × 3² × 5', fontsize=8.5, ha='left', va='center')
ax.set_xlim(-2.2, 7.0); ax.set_ylim(-0.8, 5.7); ax.axis('off')
```

::: example HCF and LCM of three numbers
**Problem.** Find the HCF and LCM of 24, 36 and 60.

**Solution.** Prime factorisation:

$24=2^3\times 3$, $\quad 36=2^2\times 3^2$, $\quad 60=2^2\times 3\times 5$.

Common primes: 2 and 3. Lowest powers: $2^2$ and $3^1$, so

$$ \text{HCF}=2^2\times 3=12 $$

All primes: 2, 3, 5. Highest powers: $2^3$, $3^2$, $5^1$, so

$$ \text{LCM}=2^3\times 3^2\times 5=360 $$
:::

```figure caption="Prime factors of 24 and 36 in two overlapping circles. The overlap (2 × 2 × 3) multiplies to the HCF 12; everything together (the whole picture) multiplies to the LCM 72."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle
fig, ax = plt.subplots(figsize=(4.4, 2.6))
ax.add_patch(Circle((-0.8, 0), 1.45, fc=SERIES[0], alpha=0.16, ec=INK, lw=1.1))
ax.add_patch(Circle((0.8, 0), 1.45, fc=SERIES[1], alpha=0.16, ec=INK, lw=1.1))
ax.text(-1.55, 0, '2', fontsize=11, ha='center', va='center', fontweight='bold')
ax.text(-0.3, 0.35, '2', fontsize=11, ha='center', va='center', fontweight='bold')
ax.text(0.3, 0.35, '2', fontsize=11, ha='center', va='center', fontweight='bold')
ax.text(0, -0.35, '3', fontsize=11, ha='center', va='center', fontweight='bold')
ax.text(1.55, 0, '3', fontsize=11, ha='center', va='center', fontweight='bold')
ax.text(-1.5, 1.7, '24 = 2 × 2 × 2 × 3', fontsize=8.5, ha='center')
ax.text(1.5, 1.7, '36 = 2 × 2 × 3 × 3', fontsize=8.5, ha='center')
ax.text(0, -1.7, 'HCF = 2 × 2 × 3 = 12', fontsize=8.5, ha='center')
ax.text(0, -2.1, 'LCM = 2 × 2 × 2 × 3 × 3 = 72', fontsize=8.5, ha='center')
ax.set_xlim(-3.3, 3.3); ax.set_ylim(-2.4, 2.1); ax.set_aspect('equal'); ax.axis('off')
```

::: key Two numbers: HCF × LCM = product
For any two numbers $a$ and $b$: $\text{HCF}(a,b)\times\text{LCM}(a,b)=a\times b$.

Check with 24 and 36: HCF $=12$, LCM $=72$, and $12\times 72=864=24\times 36$ ✓.
:::

::: example Euclid's division method
**Problem.** Find the HCF of 252 and 198 by long division.

**Solution.** Divide the larger by the smaller, then divide the divisor by the remainder, and continue until the remainder is zero. The last divisor is the HCF.

$$ 252=198\times 1+54 $$
$$ 198=54\times 3+36 $$
$$ 54=36\times 1+18 $$
$$ 36=18\times 2+0 $$

The HCF is **18**.
:::

::: example Word problem: HCF
**Problem.** Three ropes of lengths 36 m, 48 m and 60 m are to be cut into pieces of **equal length**, as long as possible. Find the length of each piece and the number of pieces.

**Solution.** The longest equal piece is the **HCF** of 36, 48 and 60. $36=2^2\times 3^2$, $48=2^4\times 3$, $60=2^2\times 3\times 5$, so

$$ \text{HCF}=2^2\times 3=12\text{ m} $$

Number of pieces $=\dfrac{36}{12}+\dfrac{48}{12}+\dfrac{60}{12}=3+4+5=12$.
:::

```figure caption="Three bells ring every 12, 15 and 20 minutes starting together. The first time all three ring together again is at the LCM, 60 minutes."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8, 2.4))
for yi, (step, col, name) in enumerate([(12, SERIES[0], 'every 12 min'), (15, SERIES[1], 'every 15 min'), (20, SERIES[2], 'every 20 min')]):
    y = 3 - yi
    ts = np.arange(0, 61, step)
    ax.plot(ts, [y]*len(ts), 'o', color=col, ms=6)
    ax.text(-3, y, name, ha='right', va='center', fontsize=8)
ax.axvline(60, color=INK, lw=1.2, ls='--')
ax.text(57, 3.75, 'all ring together\nLCM = 60', ha='right', va='bottom', fontsize=8)
ax.set_xlim(-24, 68); ax.set_ylim(0.4, 4.9)
ax.set_yticks([]); ax.set_xticks(range(0, 61, 10))
ax.set_xlabel('minutes after the start', fontsize=8.5)
ax.spines[['top','right','left']].set_visible(False)
ax.grid(axis='x', color=GRID, lw=0.5); ax.set_axisbelow(True)
```

::: example Word problem: LCM
**Problem.** Three bells ring at intervals of 18, 24 and 30 minutes. They ring together at 6:00 a.m. When will they next ring together?

**Solution.** The bells ring together after the **LCM** of 18, 24 and 30 minutes.

$18=2\times 3^2$, $24=2^3\times 3$, $30=2\times 3\times 5$, so

$$ \text{LCM}=2^3\times 3^2\times 5=360\text{ minutes}=6\text{ hours} $$

They next ring together at **12:00 noon**.
:::

::: tip HCF or LCM?
Ask: *am I cutting or splitting into the biggest equal parts?* — **HCF** (largest tile, longest rope, most students per group). *Am I waiting for events to coincide, or finding the smallest number that all will divide?* — **LCM** (bells, traffic lights, common denominator).
:::

::: example Largest square tile
**Problem.** A hall is 8 m 40 cm long and 5 m 25 cm wide. It is to be paved with identical square tiles, as large as possible, with no cutting. Find the side of each tile and the number of tiles.

**Solution.** Change to centimetres: length $=840$ cm, width $=525$ cm. The largest square tile has side $=\text{HCF}(840,525)$.

$$ 840=525\times 1+315 \qquad 525=315\times 1+210 $$
$$ 315=210\times 1+105 \qquad 210=105\times 2+0 $$

HCF $=105$ cm. Tiles along the length $=\dfrac{840}{105}=8$; along the width $=\dfrac{525}{105}=5$.

Number of tiles $=8\times 5=40$.
:::

::: example Number leaving a remainder
**Problem.** Find the smallest number which, when divided by 12, 15 and 20, leaves a remainder 5 each time.

**Solution.** A number that is exactly divisible by 12, 15 and 20 is a multiple of their LCM. $12=2^2\times 3$, $15=3\times 5$, $20=2^2\times 5$, so LCM $=2^2\times 3\times 5=60$.

The required number is the LCM plus the remainder: $60+5=65$.

Check: $65=12\times 5+5$, $65=15\times 4+5$, $65=20\times 3+5$ ✓.
:::

### Factorisation: the toolkit

To find the HCF and LCM of expressions, each must first be broken into factors that cannot be broken further. These are the types you need.

| Type | Rule | Example |
|---|---|---|
| Common factor | take out the common factor | $6x^2-6=6(x^2-1)$ |
| Grouping | group in pairs, take out common factors | $ax+ay+bx+by=(a+b)(x+y)$ |
| Difference of squares | $a^2-b^2=(a+b)(a-b)$ | $x^2-9=(x+3)(x-3)$ |
| Perfect square | $a^2\pm 2ab+b^2=(a\pm b)^2$ | $x^2+4x+4=(x+2)^2$ |
| Trinomial $x^2+px+q$ | find two numbers with sum $p$ and product $q$ | $x^2-5x+6=(x-2)(x-3)$ |
| Trinomial $ax^2+bx+c$ | split $b$ into two numbers whose product is $ac$ | $2x^2+7x+3=(2x+1)(x+3)$ |
| Sum / difference of cubes | $a^3\pm b^3=(a\pm b)(a^2\mp ab+b^2)$ | $x^3+8=(x+2)(x^2-2x+4)$ |

::: example Splitting the middle term
**Problem.** Factorise $2x^2+7x+3$.

**Solution.** Here $a\cdot c=2\times 3=6$. We need two numbers with product 6 and sum 7: they are 6 and 1.

$$ 2x^2+7x+3=2x^2+6x+x+3=2x(x+3)+1(x+3)=(2x+1)(x+3) $$

Check: $(2x+1)(x+3)=2x^2+6x+x+3=2x^2+7x+3$ ✓.
:::

::: caution Factorisation mistakes
- Stopping early: $x^4-16=(x^2-4)(x^2+4)$ is not finished, since $x^2-4=(x-2)(x+2)$ factorises further.
- Treating $x^2+y^2$ as factorisable. It does not factorise over real numbers.
- Forgetting the numerical factor: $6x^2-6=6(x-1)(x+1)$, not $(x-1)(x+1)$.
- Sign errors: $x^2-x-6=(x-3)(x+2)$ since the numbers with product $-6$ and sum $-1$ are $-3$ and $+2$.
:::

### HCF and LCM of algebraic expressions

::: key Method for expressions
1. **Factorise** each expression completely.
2. **HCF** $=$ product of the factors **common to all** the expressions (with the **lowest** power), including the HCF of the numerical coefficients.
3. **LCM** $=$ product of **all** the different factors (with the **highest** power), including the LCM of the numerical coefficients.
4. Leave the answer in factor form (multiplying out is optional unless asked).
:::

```figure caption="Factors of x²−5x+6 and x²−9. The shared factor (x−3) is the HCF; all three different factors multiplied together give the LCM."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle
fig, ax = plt.subplots(figsize=(4.6, 2.6))
ax.add_patch(Circle((-0.8, 0), 1.45, fc=SERIES[0], alpha=0.16, ec=INK, lw=1.1))
ax.add_patch(Circle((0.8, 0), 1.45, fc=SERIES[1], alpha=0.16, ec=INK, lw=1.1))
ax.text(-1.55, 0, '(x − 2)', fontsize=9, ha='center', va='center')
ax.text(0, 0, '(x − 3)', fontsize=9, ha='center', va='center', fontweight='bold')
ax.text(1.55, 0, '(x + 3)', fontsize=9, ha='center', va='center')
ax.text(-1.5, 1.7, 'x² − 5x + 6', fontsize=8.5, ha='center')
ax.text(1.5, 1.7, 'x² − 9', fontsize=8.5, ha='center')
ax.text(0, -1.7, 'HCF = (x − 3)', fontsize=8.5, ha='center')
ax.text(0, -2.1, 'LCM = (x − 2)(x − 3)(x + 3)', fontsize=8.5, ha='center')
ax.set_xlim(-3.3, 3.3); ax.set_ylim(-2.4, 2.1); ax.set_aspect('equal'); ax.axis('off')
```

::: example Two quadratics
**Problem.** Find the HCF and LCM of $x^2-5x+6$ and $x^2-9$.

**Solution.** Factorise:

$x^2-5x+6=(x-2)(x-3)$ and $x^2-9=(x-3)(x+3)$.

Common factor: $(x-3)$.

$$ \text{HCF}=x-3 $$
$$ \text{LCM}=(x-2)(x-3)(x+3) $$
:::

::: example Monomials with coefficients
**Problem.** Find the HCF and LCM of $12a^3b^2$, $18a^2b^3c$ and $30ab^4c^2$.

**Solution.** Numerical parts: $\text{HCF}(12,18,30)=6$ and $\text{LCM}(12,18,30)=180$.

| Letter | Powers in the three terms | Lowest (HCF) | Highest (LCM) |
|---|---|---|---|
| $a$ | $3,\ 2,\ 1$ | $a^1$ | $a^3$ |
| $b$ | $2,\ 3,\ 4$ | $b^2$ | $b^4$ |
| $c$ | $0,\ 1,\ 2$ | none ($c^0$) | $c^2$ |

$$ \text{HCF}=6ab^2 \qquad \text{LCM}=180a^3b^4c^2 $$

A letter that is missing from even one term (like $c$ in the first term) does not appear in the HCF.
:::

::: example Cubes and squares
**Problem.** Find the HCF and LCM of $a^3-b^3$ and $a^2-b^2$.

**Solution.** $a^3-b^3=(a-b)(a^2+ab+b^2)$ and $a^2-b^2=(a-b)(a+b)$.

$$ \text{HCF}=a-b \qquad \text{LCM}=(a-b)(a+b)(a^2+ab+b^2) $$
:::

::: example Three expressions with numerical factors
**Problem.** Find the HCF and LCM of $6x^2-6$, $9x^2+9x-18$ and $3x^2+6x+3$.

**Solution.** Factorise:

$6x^2-6=6(x^2-1)=6(x-1)(x+1)$.

$9x^2+9x-18=9(x^2+x-2)=9(x-1)(x+2)$.

$3x^2+6x+3=3(x^2+2x+1)=3(x+1)^2$.

Numerical parts: $\text{HCF}(6,9,3)=3$ and $\text{LCM}(6,9,3)=18$.

Algebraic factors: $(x-1)$ is not in the third; $(x+1)$ is not in the second; $(x+2)$ is only in the second. There is **no algebraic factor common to all three**.

$$ \text{HCF}=3 $$
$$ \text{LCM}=18(x-1)(x+1)^2(x+2) $$

(Highest power of $(x+1)$ is 2, from the third expression.)
:::

::: example Cubes, squares and perfect squares
**Problem.** Find the HCF and LCM of $x^3+8$, $x^2-4$ and $x^2+4x+4$.

**Solution.** $x^3+8=(x+2)(x^2-2x+4)$, $x^2-4=(x-2)(x+2)$, $x^2+4x+4=(x+2)^2$.

Common to all three: $(x+2)$, lowest power 1.

$$ \text{HCF}=x+2 $$
$$ \text{LCM}=(x+2)^2(x-2)(x^2-2x+4) $$
:::

::: example Factorising by grouping first
**Problem.** Find the HCF and LCM of $ax+ay+bx+by$ and $ax-ay+bx-by$.

**Solution.** $ax+ay+bx+by=a(x+y)+b(x+y)=(a+b)(x+y)$.

$ax-ay+bx-by=a(x-y)+b(x-y)=(a+b)(x-y)$.

$$ \text{HCF}=a+b \qquad \text{LCM}=(a+b)(x+y)(x-y) $$
:::

### The relation between HCF, LCM and the expressions

::: derivation HCF × LCM = product of the two expressions
We show that for two expressions $A$ and $B$, the HCF and LCM multiply back to $A\times B$. This lets us find a missing expression.

**Setting up.** Let $H$ be the HCF of $A$ and $B$. Then we can write

$$ A=H\times p, \qquad B=H\times q $$

where $p$ and $q$ have **no common factor** (we have taken out everything shared).

**Step 1 — the LCM.** The LCM must contain all of $A$ and all of $B$ with nothing repeated. The shared part $H$ appears once, plus the leftover parts $p$ and $q$:

$$ L=H\times p\times q $$

**Step 2 — multiply HCF by LCM.**

$$ H\times L=H\times(H\times p\times q)=(H\times p)\times(H\times q) $$

**Step 3 — recognise $A$ and $B$.**

$$ H\times L=A\times B $$

**Result.** $\text{HCF}\times\text{LCM}=A\times B$ (true for **two** expressions only, not for three).

**What it means.** If you know any three of $A$, $B$, HCF and LCM you can find the fourth: $B=\dfrac{\text{HCF}\times\text{LCM}}{A}$.
:::

::: example Verifying the relation
**Problem.** For $p=x^2+3x+2$ and $q=x^2-1$ find the HCF and LCM and verify that $\text{HCF}\times\text{LCM}=p\times q$.

**Solution.** $p=(x+1)(x+2)$ and $q=(x-1)(x+1)$.

HCF $=x+1$; LCM $=(x+1)(x+2)(x-1)=x^3+2x^2-x-2$.

HCF $\times$ LCM $=(x+1)(x^3+2x^2-x-2)=x^4+3x^3+x^2-3x-2$.

$p\times q=(x^2+3x+2)(x^2-1)=x^4+3x^3+2x^2-x^2-3x-2=x^4+3x^3+x^2-3x-2$.

The two results are the same. ✓
:::

::: example Finding the missing expression
**Problem.** The HCF of two expressions is $x+2$ and their LCM is $x^3+3x^2-4x-12$. If one expression is $x^2-4$, find the other.

**Solution.** $\text{LCM}=x^3+3x^2-4x-12=x^2(x+3)-4(x+3)=(x+3)(x^2-4)=(x+3)(x-2)(x+2)$.

Other expression $=\dfrac{\text{HCF}\times\text{LCM}}{\text{given expression}}=\dfrac{(x+2)(x+3)(x-2)(x+2)}{(x-2)(x+2)}=(x+2)(x+3)$.

Other expression $=x^2+5x+6$.

Check: HCF of $(x-2)(x+2)$ and $(x+2)(x+3)$ is $x+2$ ✓; LCM is $(x-2)(x+2)(x+3)$ ✓.
:::

::: example Trinomials with leading coefficient
**Problem.** Find the HCF and LCM of $2x^2+7x+3$ and $2x^2-x-1$.

**Solution.** $2x^2+7x+3=(2x+1)(x+3)$ and $2x^2-x-1=(2x+1)(x-1)$.

$$ \text{HCF}=2x+1 \qquad \text{LCM}=(2x+1)(x+3)(x-1) $$
:::

## 8.2 Exercises of the SEE type

### Method

1. Factorise every expression **completely**. Take out numerical factors too.
2. Underline factors common to **all** expressions: their lowest powers multiply to the HCF.
3. List every different factor at its highest power: the product is the LCM.
4. For two expressions, check with $\text{HCF}\times\text{LCM}=A\times B$ if the question asks you to verify.
5. To find a missing expression: $B=\dfrac{\text{HCF}\times\text{LCM}}{A}$.
6. Word problems: cutting into equal pieces $\Rightarrow$ HCF; events together again $\Rightarrow$ LCM.

## Chapter summary

- HCF $=$ common factors at lowest powers; LCM $=$ all factors at highest powers (include the numerical parts).
- For two numbers or expressions: $\text{HCF}\times\text{LCM}=A\times B$. Not valid for three.
- Factorisation toolkit: common factor, grouping, $a^2-b^2$, perfect squares, $x^2+px+q$, $ax^2+bx+c$, $a^3\pm b^3$.
- $a^3+b^3=(a+b)(a^2-ab+b^2)$ and $a^3-b^3=(a-b)(a^2+ab+b^2)$.
- Euclid's method: divide, then divide the divisor by the remainder, until the remainder is 0; the last divisor is the HCF.
- Missing expression: $B=\dfrac{\text{HCF}\times\text{LCM}}{A}$.
- A letter missing from any one term is not in the HCF.
- Word problems: HCF for equal cutting; LCM for common times.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The HCF of 12 and 18 is <span class="marks">[1]</span>
   (a) 3 (b) 6 (c) 36 (d) 2
2. The LCM of 4 and 6 is <span class="marks">[1]</span>
   (a) 24 (b) 2 (c) 12 (d) 10
3. The HCF of $x^2-9$ and $x-3$ is <span class="marks">[1]</span>
   (a) $x+3$ (b) $x-3$ (c) $x^2-9$ (d) 1
4. The HCF of two expressions is 3, their LCM is 60 and one expression is 12. The other is <span class="marks">[1]</span>
   (a) 5 (b) 15 (c) 20 (d) 30
5. The LCM of $a^2b$ and $ab^2$ is <span class="marks">[1]</span>
   (a) $ab$ (b) $a^2b$ (c) $a^2b^2$ (d) $a^3b^3$

::: note Answers to Group A
**1.** (b) — $12=2^2\cdot 3$, $18=2\cdot 3^2$, HCF $=2\cdot 3=6$.
**2.** (c) — $4=2^2$, $6=2\cdot 3$, LCM $=2^2\cdot 3=12$.
**3.** (b) — $x^2-9=(x-3)(x+3)$, so $(x-3)$ is common.
**4.** (b) — $\frac{3\times 60}{12}=15$.
**5.** (c) — highest powers: $a^2$ and $b^2$.
:::

**Group B — Short answer (2 marks each)**

1. Find the HCF and LCM of $12a^2b$ and $18ab^2$. <span class="marks">[2]</span>
2. Factorise $x^2-7x+12$. <span class="marks">[2]</span>
3. Find the HCF of $x^2-4$ and $x^2+4x+4$. <span class="marks">[2]</span>
4. Find the HCF of 36 and 48 by the division method. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** HCF of coefficients $=6$, LCM $=36$. $a$: lowest 1, highest 2; $b$: lowest 1, highest 2. HCF $=6ab$; LCM $=36a^2b^2$.
**2.** Numbers with product 12 and sum $-7$: $-3$ and $-4$. $x^2-7x+12=(x-3)(x-4)$.
**3.** $x^2-4=(x-2)(x+2)$ and $x^2+4x+4=(x+2)^2$. HCF $=x+2$.
**4.** $48=36\times 1+12$; $36=12\times 3+0$. HCF $=12$.
:::

**Group C — Short answer (3 marks each)**

1. Find the HCF and LCM of $x^2-x-6$ and $x^2-9$. <span class="marks">[3]</span>
2. Find the HCF and LCM of $2x^2+7x+3$ and $2x^2-x-1$. <span class="marks">[3]</span>
3. Three bells ring at intervals of 18, 24 and 30 minutes. They ring together at 6:00 a.m. When will they ring together next? <span class="marks">[3]</span>
4. Find the HCF and LCM of $a^3-b^3$ and $a^2-b^2$. <span class="marks">[3]</span>

::: note Answers to Group C
**1.** $x^2-x-6=(x-3)(x+2)$ and $x^2-9=(x-3)(x+3)$. HCF $=x-3$. LCM $=(x-3)(x+2)(x+3)$.
**2.** $(2x+1)(x+3)$ and $(2x+1)(x-1)$. HCF $=2x+1$; LCM $=(2x+1)(x+3)(x-1)$.
**3.** LCM of 18, 24, 30: $18=2\cdot 3^2$, $24=2^3\cdot 3$, $30=2\cdot 3\cdot 5$, so LCM $=2^3\cdot 3^2\cdot 5=360$ min $=6$ hours. Next together at 12:00 noon.
**4.** $(a-b)(a^2+ab+b^2)$ and $(a-b)(a+b)$. HCF $=a-b$; LCM $=(a-b)(a+b)(a^2+ab+b^2)$.
:::

**Group D — Long answer (4 marks each)**

1. Find the HCF and LCM of $6x^2-6$, $9x^2+9x-18$ and $3x^2+6x+3$. <span class="marks">[4]</span>
2. The HCF of two expressions is $x+1$ and their LCM is $x^3+2x^2-x-2$. If one expression is $x^2+3x+2$, find the other, and verify that $\text{HCF}\times\text{LCM}=$ product of the expressions. <span class="marks">[4]</span>
3. Find the HCF and LCM of $x^3+8$, $x^2-4$ and $x^2+4x+4$. <span class="marks">[4]</span>
4. Find the HCF and LCM of $ax+ay+bx+by$ and $ax-ay+bx-by$. <span class="marks">[4]</span>

::: note Answers to Group D
**1.** $6(x-1)(x+1)$, $9(x-1)(x+2)$, $3(x+1)^2$. Numerical HCF $=3$, LCM $=18$. No algebraic factor common to all three. HCF $=3$. LCM $=18(x-1)(x+1)^2(x+2)$.
**2.** $x^3+2x^2-x-2=x^2(x+2)-(x+2)=(x+2)(x^2-1)=(x+2)(x-1)(x+1)$. Other $=\frac{(x+1)(x+2)(x-1)(x+1)}{(x+1)(x+2)}=(x+1)(x-1)=x^2-1$. Verification: HCF $\times$ LCM $=x^4+3x^3+x^2-3x-2$ and $(x^2+3x+2)(x^2-1)=x^4+3x^3+x^2-3x-2$ ✓.
**3.** $(x+2)(x^2-2x+4)$, $(x-2)(x+2)$, $(x+2)^2$. HCF $=x+2$; LCM $=(x+2)^2(x-2)(x^2-2x+4)$.
**4.** $(a+b)(x+y)$ and $(a+b)(x-y)$. HCF $=a+b$; LCM $=(a+b)(x+y)(x-y)$.
:::
