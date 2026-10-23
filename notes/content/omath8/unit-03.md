---
subject: Optional Mathematics
grade: 8
unit: 3
title: Sequence and Series
hours: 0
---

The Saturdays of a month fall on dates such as 3, 10, 17, 24 and 31. A child who saves Rs 10 more every week saves Rs 10, 20, 30, 40, … . A sheet of paper folded again and again has 1, 2, 4, 8, 16, … layers. Each of these is a list of numbers made by a rule, and the rule lets us find any number in the list without writing out all the numbers before it. Such a list is a **sequence**, and the sum of its numbers is a **series**. In this chapter you will learn what a sequence is, how to find its terms from a rule and its rule from its terms, and how to write long sums in a short form with the sigma sign $\Sigma$.

::: key What your examination asks from this chapter
Expect: (i) write the first few terms from a general term $t_n$; (ii) find the next terms and the **general term** of a given sequence, by differences or ratios; (iii) find a particular term, such as $t_{20}$, or decide **which term** a number is, or whether it is a term at all; (iv) a pattern problem (matchsticks, seats, savings) turned into a sequence; (v) **expand** a sigma expression and find its value; (vi) write a given series in **sigma notation**. Show the rule you found and check it against the given terms.
:::

## 3.1 Sequence: meaning, terms and the general term

::: definition Sequence and terms
A **sequence** is a list of numbers written in a definite order, according to a rule. Each number in the list is a **term**. The terms are named by their positions:
$$ t_1,\ t_2,\ t_3,\ \ldots,\ t_n,\ \ldots $$
where $t_1$ is the first term, $t_2$ the second term, and $t_n$ (read "$t$ sub $n$") the $n$th term.
:::

In the sequence $5, 10, 15, 20, \ldots$ we have $t_1=5$, $t_2=10$, $t_3=15$ and $t_4=20$. The number written small below $t$ is the **position** of the term; the term itself is the **value** at that position. Keep the two apart: in this sequence the 4th term is 20.

### Finite and infinite sequences

A sequence that stops is **finite**; one that goes on for ever is **infinite**. Three dots at the end, "…", show that the sequence continues.

| Sequence | Type | Reason |
|---|---|---|
| 3, 10, 17, 24, 31 (Saturdays of a month) | finite | it has exactly 5 terms |
| 5, 10, 15, 20, … (multiples of 5) | infinite | there is no last multiple of 5 |
| 1, 2, 4, 8, …, 1024 | finite | it stops at 1024 |
| 1, $\frac{1}{2}$, $\frac{1}{3}$, $\frac{1}{4}$, … | infinite | the dots show it never ends |

### The general term

The **general term** (or $n$th term) $t_n$ is a formula in $n$ that gives the term in any position. For the multiples of 5, $t_n=5n$: the 1st term is $5\times1=5$, the 7th term is $5\times7=35$, and the 100th term is $500$. Once we know $t_n$, we never need to count along the list.

A sequence is really a **function** whose domain is the set of natural numbers $\{1,2,3,\ldots\}$: it sends each position $n$ to the term $t_n$. This is why the graph of a sequence is a set of separate dots, one above each whole number, and not a joined-up line.

Many sequences come from patterns of dots. Counting the dots in each picture of a growing pattern gives a sequence, and the shape of the pattern often shows the rule.

```figure caption="Sequences from dot patterns. Square numbers 1, 4, 9, 16 have general term $t_n=n^2$. Triangular numbers 1, 3, 6, 10 have general term $t_n=\frac{n(n+1)}{2}$, because two equal triangles fit together into an $n$ by $n+1$ rectangle."
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(5.0, 3.4))
for ax in (ax1, ax2):
    ax.set_xlim(-0.6, 17.2); ax.set_aspect('equal'); ax.axis('off')
ax1.set_ylim(-1.7, 4.2); ax2.set_ylim(-1.7, 4.2)
x0 = 0.0
for n in range(1, 5):
    for i in range(n):
        for j in range(n):
            ax1.plot(x0 + j*0.8, i*0.8, 'o', color=ACCENT, ms=5.5)
    ax1.text(x0 + (n - 1)*0.4, -1.15, 't' + '₀₁₂₃₄'[n] + f' = {n*n}', ha='center', fontsize=8.5)
    x0 += n*0.8 + 1.4
ax1.text(16.9, 1.2, 'square\nnumbers', ha='right', va='center', fontsize=8.5, color=ACCENT)
x0 = 0.0
for n in range(1, 5):
    for i in range(n):
        for j in range(i + 1):
            ax2.plot(x0 + j*0.8, (n - 1 - i)*0.8, 'o', color=SERIES[1], ms=5.5)
    ax2.text(x0 + (n - 1)*0.4, -1.15, 't' + '₀₁₂₃₄'[n] + f' = {n*(n+1)//2}', ha='center', fontsize=8.5)
    x0 += n*0.8 + 1.4
ax2.text(16.9, 1.2, 'triangular\nnumbers', ha='right', va='center', fontsize=8.5, color=SERIES[1])
fig.tight_layout(pad=0.3)
```

::: example First terms from a general term
**Problem.** Write the first four terms of the sequence whose general term is $t_n=3n-1$. Find also the 25th term.

**Solution.** Put $n=1, 2, 3, 4$:
$$ t_1=3(1)-1=2,\quad t_2=3(2)-1=5,\quad t_3=8,\quad t_4=11 $$
The sequence is $2, 5, 8, 11, \ldots$ and $t_{25}=3(25)-1=74$.
:::

## 3.2 Finding terms and the rule of a sequence

### From the rule to the terms

Any formula in $n$ produces a sequence. The table shows some common shapes of general term and the sequences they make.

| General term $t_n$ | $t_1$ | $t_2$ | $t_3$ | $t_4$ | What happens |
|---|---|---|---|---|---|
| $3n+1$ | 4 | 7 | 10 | 13 | goes up by 3 each time |
| $n^2+1$ | 2 | 5 | 10 | 17 | gaps grow: 3, 5, 7 |
| $2^n$ | 2 | 4 | 8 | 16 | doubles each time |
| $\frac{n}{n+1}$ | $\frac{1}{2}$ | $\frac{2}{3}$ | $\frac{3}{4}$ | $\frac{4}{5}$ | creeps up towards 1 |
| $(-1)^n\,2n$ | $-2$ | 4 | $-6$ | 8 | signs alternate |

The factor $(-1)^n$ is $-1$ when $n$ is odd and $+1$ when $n$ is even, so it makes the signs alternate. Use $(-1)^{n+1}$ instead if the first term is to be positive.

### Two kinds of rule

A sequence can be described in two ways.

| Kind of rule | What it says | Example for $2, 5, 8, 11, \ldots$ |
|---|---|---|
| **Term-to-term** rule | how to get the next term from the one before | "start at 2 and add 3 each time": $t_1=2$, $t_{n+1}=t_n+3$ |
| **Position-to-term** rule (general term) | how to get a term straight from its position | $t_n=3n-1$ |

The term-to-term rule is easy to see but slow to use: to reach the 100th term you must take 99 steps. The general term jumps there at once: $t_{100}=299$. That is why examinations ask for $t_n$.

Some famous sequences are known mainly by a term-to-term rule. In the **Fibonacci sequence** $1, 1, 2, 3, 5, 8, 13, \ldots$ every term after the second is the sum of the two terms before it: $t_{n+2}=t_{n+1}+t_n$. The numbers of spirals on a sunflower head or a pine cone are usually Fibonacci numbers.

::: example A sequence from a term-to-term rule
**Problem.** A sequence is defined by $t_1=2$ and $t_{n+1}=3t_n-1$. Write its first six terms.

**Solution.** Each term is "three times the previous term, minus 1":
$$ t_2=3(2)-1=5,\quad t_3=3(5)-1=14,\quad t_4=3(14)-1=41 $$
$$ t_5=3(41)-1=122,\quad t_6=3(122)-1=365 $$
The sequence is $2, 5, 14, 41, 122, 365, \ldots$.
:::

::: example A term far along the list
**Problem.** If $t_n=2n^2-3$, find $t_1$, $t_2$, $t_3$ and $t_{10}$.

**Solution.** $t_1=2-3=-1$, $t_2=8-3=5$, $t_3=18-3=15$ and $t_{10}=2(100)-3=197$. We reached the 10th term without writing the 4th to the 9th.
:::

### From the terms to the rule: the method of differences

To find the rule, subtract each term from the next. The pattern of these **differences** tells you the kind of rule.

**1. The first differences are all equal.** If the gap is always $d$, the sequence is called an **arithmetic sequence**, and its general term has the form $t_n=dn+c$. To find $c$, compare with the multiples of $d$.

For $4, 7, 10, 13, \ldots$ the gap is 3, so compare with the multiples of 3:

| $n$ | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| $3n$ | 3 | 6 | 9 | 12 |
| term | 4 | 7 | 10 | 13 |

Each term is 1 more than $3n$, so $t_n=3n+1$. The same idea gives the formula $t_n=a+(n-1)d$, where $a$ is the first term: here $4+(n-1)3=3n+1$.

**2. The ratios are all equal.** If each term is the previous one multiplied by the same number $r$, the sequence is a **geometric sequence** and $t_n=a\times r^{n-1}$. For $3, 6, 12, 24, \ldots$ we have $a=3$ and $r=2$, so $t_n=3\times2^{n-1}$.

**3. The first differences change but the second differences are equal.** Then the rule contains $n^2$. If the second difference is 2, compare the terms with $n^2$; if it is $2a$, compare them with $an^2$.

::: example A rule from second differences
**Problem.** Find the general term of $2, 5, 10, 17, 26, \ldots$ and its 12th term.

**Solution.** First differences: $3, 5, 7, 9$. Second differences: $2, 2, 2$. Equal second differences of 2 mean that the rule starts with $n^2$. Compare:

| $n$ | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| $n^2$ | 1 | 4 | 9 | 16 | 25 |
| term | 2 | 5 | 10 | 17 | 26 |

Every term is $n^2+1$. So $t_n=n^2+1$ and $t_{12}=144+1=145$.
:::

::: example When the leftover is not constant
**Problem.** Find the general term of $3, 8, 15, 24, 35, \ldots$.

**Solution.** First differences $5, 7, 9, 11$; second differences all 2, so compare with $n^2$:

| $n$ | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| term $-\ n^2$ | $3-1=2$ | $8-4=4$ | $15-9=6$ | $24-16=8$ | $35-25=10$ |

The leftover $2, 4, 6, 8, 10$ is $2n$. So $t_n=n^2+2n$. Check: $t_4=16+8=24$ ✓.
:::

::: example Fractions and alternating signs
**Problem.** Find the general term of (i) $1, -\frac{1}{2}, \frac{1}{3}, -\frac{1}{4}, \ldots$ (ii) $\frac{1}{3}, \frac{1}{9}, \frac{1}{27}, \frac{1}{81}, \ldots$ (iii) $\frac{2}{3}, \frac{4}{5}, \frac{6}{7}, \frac{8}{9}, \ldots$

**Solution.** Look at the sign, the numerator and the denominator separately.

(i) The numerators are all 1, the denominators are $1, 2, 3, 4$, i.e. $n$, and the signs go $+, -, +, -$, which is $(-1)^{n+1}$. So $t_n=\frac{(-1)^{n+1}}{n}$.

(ii) The denominators $3, 9, 27, 81$ are $3^1, 3^2, 3^3, 3^4$. So $t_n=\frac{1}{3^n}$.

(iii) The numerators $2, 4, 6, 8$ are $2n$ and the denominators $3, 5, 7, 9$ are $2n+1$. So $t_n=\frac{2n}{2n+1}$. Check: $t_4=\frac{8}{9}$ ✓.
:::

```figure caption="The graph of a sequence is a set of separate dots. An arithmetic sequence ($t_n=3n+1$) lies on a straight line; a rule with $n^2$ ($t_n=n^2+1$) bends upwards; a geometric sequence ($t_n=3\times2^{n-1}$) shoots up fastest of all."
fig, ax = plt.subplots(figsize=(4.8, 2.9))
n = np.arange(1, 7)
ax.plot(n, 3*n + 1, 'o', color=ACCENT, ms=5)
ax.plot(n, n**2 + 1, 's', color=SERIES[2], ms=5)
ax.plot(n, 3*2.0**(n - 1), '^', color=SERIES[1], ms=5.5)
ax.text(6.25, 19, '3n + 1', color=ACCENT, fontsize=8.5, va='center')
ax.text(6.25, 37, 'n² + 1', color=SERIES[2], fontsize=8.5, va='center')
ax.text(5.25, 92, '3 × 2ⁿ⁻¹', color=SERIES[1], fontsize=8.5, va='center', ha='right')
ax.set_xlim(0.5, 7.3); ax.set_ylim(0, 105)
ax.set_xticks(n); ax.set_xlabel('position n', fontsize=8.5); ax.set_ylabel('term t(n)', fontsize=8.5)
ax.tick_params(labelsize=8)
ax.grid(True, color=GRID, lw=0.6); ax.set_axisbelow(True)
ax.spines[['top', 'right']].set_visible(False)
fig.tight_layout(pad=0.4)
```

### Is a number a term, and which term is it?

Once $t_n$ is known, set $t_n$ equal to the number and solve for $n$. If $n$ comes out as a **natural number**, the number is a term and $n$ is its position. If $n$ is a fraction or negative, the number is not a term.

::: example Which term, and is it a term at all?
**Problem.** For the sequence $4, 7, 10, 13, \ldots$: (i) which term is 100? (ii) Is 150 a term?

**Solution.** We found $t_n=3n+1$.

(i) $3n+1=100$ gives $3n=99$ and $n=33$. So 100 is the **33rd term**.

(ii) $3n+1=150$ gives $3n=149$ and $n=49\frac{2}{3}$. There is no $49\frac{2}{3}$th position, so **150 is not a term**. (The 49th term is 148 and the 50th is 151; 150 falls between them.)
:::

::: caution Position and value are different numbers
In "which term is 100?", 100 is a **value** and the answer, 33, is a **position**. Writing "$t_{100}$" for this question computes the 100th term, 301, which answers a different question. Read the question twice: "find $t_{20}$" gives a value; "which term is 62?" gives a position.
:::

### Patterns that turn into sequences

```figure caption="Squares in a row made of matchsticks. One square needs 4 sticks, and each new square needs only 3 more because it shares a side, so the numbers of sticks are 4, 7, 10, … with $t_n=3n+1$."
fig, ax = plt.subplots(figsize=(5.0, 2.4))
ax.set_xlim(-0.3, 12.6); ax.set_ylim(-1.4, 1.5); ax.set_aspect('equal'); ax.axis('off')
x0 = 0.0
for n, sticks in [(1, 4), (2, 7), (3, 10)]:
    for k in range(n + 1):
        ax.plot([x0 + k, x0 + k], [0.06, 0.94], color='#b5651d', lw=2.6, solid_capstyle='round')
    for k in range(n):
        ax.plot([x0 + k + 0.06, x0 + k + 0.94], [0, 0], color='#b5651d', lw=2.6, solid_capstyle='round')
        ax.plot([x0 + k + 0.06, x0 + k + 0.94], [1, 1], color='#b5651d', lw=2.6, solid_capstyle='round')
    ax.text(x0 + n/2, -0.45, f'{n} square' + ('s' if n > 1 else ''), ha='center', fontsize=8.5)
    ax.text(x0 + n/2, -0.95, f'{sticks} sticks', ha='center', fontsize=8.5, color=ACCENT)
    x0 += n + 1.9
ax.text(x0 - 0.4, 0.5, '…  n squares: 3n + 1 sticks', ha='left', va='center', fontsize=8.5, color=ACCENT)
ax.set_xlim(-0.3, x0 + 4.4)
fig.tight_layout(pad=0.3)
```

::: example Matchstick squares
**Problem.** Using the pattern above, find (i) the number of sticks for 25 squares, (ii) the number of squares that can be made with exactly 100 sticks.

**Solution.** The sticks form $4, 7, 10, \ldots$, with $t_n=3n+1$.

(i) $t_{25}=3(25)+1=76$ sticks.

(ii) $3n+1=100$ gives $n=33$. So 100 sticks make **33 squares**.
:::

::: example Seats in a hall
**Problem.** The first row of a school hall in Biratnagar has 20 seats, and every row has 2 more seats than the row in front of it. Find the general term and the number of seats in the 15th row.

**Solution.** The rows have $20, 22, 24, \ldots$ seats; the difference is 2. Comparing with $2n$ ($2, 4, 6, \ldots$), every term is 18 more, so $t_n=2n+18$. In the 15th row there are $t_{15}=30+18=48$ seats.
:::

::: tip A rule must fit every given term
Having found $t_n$, test it on **all** the terms you were given, not just the first. The rule $t_n=2n$ fits the first two terms of $2, 4, 8, 16$ but fails at the third ($2\times3=6\neq8$); the right rule is $t_n=2^n$. Writing the check line also earns the marker's confidence.
:::

## 3.3 Series and the sigma (Σ) notation

When the terms of a sequence are **added**, we get a **series**. The sequence $2, 4, 6, 8, 10$ gives the series $2+4+6+8+10$, whose value is 30. A series made from a finite sequence is a **finite series**; one made from an infinite sequence, such as $1+\frac{1}{2}+\frac{1}{4}+\cdots$, is an **infinite series**.

::: definition Series and the sum of n terms
A **series** is the sum of the terms of a sequence. The sum of the first $n$ terms is written $S_n$:
$$ S_n=t_1+t_2+t_3+\cdots+t_n $$
:::

An infinite series cannot be added term by term to the end, because there is no end. But its **partial sums** $S_1, S_2, S_3, \ldots$ can still be worked out. For $\frac{1}{2}+\frac{1}{4}+\frac{1}{8}+\frac{1}{16}+\cdots$ they are
$$ S_1=0.5,\quad S_2=0.75,\quad S_3=0.875,\quad S_4=0.9375,\quad S_5=0.96875,\ \ldots $$
Each partial sum is closer to 1, but none of them goes past 1. Saying exactly what such a sum "approaches" is the idea of a **limit**, the subject of the next chapter.

### The sigma notation

Writing $1+4+9+16+\cdots+400$ in full is slow. Mathematicians use the Greek capital letter **sigma**, $\Sigma$ (the Greek "S", for "sum"), to write such a sum in one short line:
$$ \sum_{k=1}^{20}k^2=1^2+2^2+3^2+\cdots+20^2 $$

::: key Reading a sigma expression
In $\sum_{k=1}^{n}t_k$:
- $k$ is the **index**; it takes the whole-number values from the bottom number to the top number, one at a time;
- $k=1$ (below) is the **lower limit** and $n$ (above) is the **upper limit**;
- $t_k$ is the general term; work it out for every value of $k$ and **add** the results.

The number of terms is upper limit $-$ lower limit $+1$. The letter used for the index does not matter: $\sum_{k=1}^{5}k^2$ and $\sum_{r=1}^{5}r^2$ are the same sum.
:::

::: example Expanding sigma expressions
**Problem.** Expand and evaluate: (i) $\sum_{k=1}^{4}(2k+1)$ (ii) $\sum_{k=1}^{5}k^2$ (iii) $\sum_{r=2}^{5}(r^2-r)$ (iv) $\sum_{k=1}^{6}(-1)^k\,k$.

**Solution.**

(i) $k=1,2,3,4$ give $3, 5, 7, 9$, so the sum is $3+5+7+9=24$.

(ii) $1+4+9+16+25=55$.

(iii) Here $r$ starts at 2: $r=2,3,4,5$ give $2, 6, 12, 20$, so the sum is $40$. There are $5-2+1=4$ terms.

(iv) $-1+2-3+4-5+6=3$. The factor $(-1)^k$ makes the odd-numbered terms negative.
:::

### Writing a series in sigma notation

Three steps: (1) find the general term $t_k$; (2) find the value of $k$ for the first term (usually 1); (3) find the value of $k$ for the **last** term by solving $t_k=$ last term.

::: example From a series to sigma notation
**Problem.** Write in sigma notation: (i) $3+7+11+\cdots+39$ (ii) $\frac{1}{2}+\frac{2}{3}+\frac{3}{4}+\cdots+\frac{9}{10}$ (iii) $1+8+27+64+125$.

**Solution.** (i) The difference is 4, so $t_k=4k-1$ (check: $t_1=3$ ✓). For the last term, $4k-1=39$ gives $k=10$. So the series is $\sum_{k=1}^{10}(4k-1)$.

(ii) The $k$th term is $\frac{k}{k+1}$, and the last term $\frac{9}{10}$ has $k=9$: $\sum_{k=1}^{9}\frac{k}{k+1}$.

(iii) These are cubes $1^3, 2^3, \ldots, 5^3$: $\sum_{k=1}^{5}k^3$.
:::

### Rules for working with sigma

Because $\Sigma$ only means "add", the ordinary rules of addition give three useful rules:

| Rule | Example |
|---|---|
| $\sum_{k=1}^{n}c=nc$ (a constant added $n$ times) | $\sum_{k=1}^{10}2=20$ |
| $\sum_{k=1}^{n}c\,t_k=c\sum_{k=1}^{n}t_k$ | $\sum_{k=1}^{10}3k=3\sum_{k=1}^{10}k$ |
| $\sum_{k=1}^{n}(a_k+b_k)=\sum_{k=1}^{n}a_k+\sum_{k=1}^{n}b_k$ | $\sum(3k+2)=\sum3k+\sum2$ |

### Two famous sums

When the young Carl Friedrich Gauss was asked to add the numbers from 1 to 100, he paired the first with the last, the second with the second-last, and so on: $1+100$, $2+99$, $3+98$, … . Each pair makes 101, and there are 50 pairs, so the sum is $50\times101=5050$. The picture below shows the same idea for any $n$.

```figure caption="Left: two copies of the staircase $1+2+3+4+5$ fit together into a $5\times6$ rectangle, so $1+2+\cdots+5=\frac{5\times6}{2}=15$ and in general $\sum_{k=1}^{n}k=\frac{n(n+1)}{2}$. Right: the odd numbers 1, 3, 5, 7 are L-shaped layers that build a $4\times4$ square, so the sum of the first $n$ odd numbers is $n^2$."
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(5.0, 2.6))
for i in range(1, 6):
    for j in range(i):
        ax1.add_patch(Rectangle((i - 1, j), 1, 1, fc=ACCENT, ec='white', lw=1.2))
    for j in range(i, 6):
        ax1.add_patch(Rectangle((i - 1, j), 1, 1, fc='#cfe3f6', ec='white', lw=1.2))
ax1.text(2.5, -0.55, 'n = 5 columns', ha='center', fontsize=8)
ax1.text(-0.35, 3.0, 'n + 1 = 6', rotation=90, ha='center', va='center', fontsize=8)
ax1.set_xlim(-0.8, 5.3); ax1.set_ylim(-1.0, 6.3); ax1.set_aspect('equal'); ax1.axis('off')
cols = [ACCENT, SERIES[2], SERIES[3], SERIES[1]]
for m in range(4):
    for i in range(m + 1):
        for j in range(m + 1):
            if i == m or j == m:
                ax2.add_patch(Rectangle((i, j), 1, 1, fc=cols[m], ec='white', lw=1.2, alpha=0.9))
for m, lab in enumerate(['1', '3', '5', '7']):
    ax2.text(m + 0.5, m + 0.5, lab, ha='center', va='center', fontsize=9, color='white')
ax2.text(2.0, -0.55, '1 + 3 + 5 + 7 = 16 = 4²', ha='center', fontsize=8)
ax2.set_xlim(-0.4, 4.4); ax2.set_ylim(-1.0, 4.6); ax2.set_aspect('equal'); ax2.axis('off')
fig.tight_layout(pad=0.4)
```

::: key Sums worth remembering
$$ \sum_{k=1}^{n}k=1+2+\cdots+n=\frac{n(n+1)}{2} \qquad\qquad \sum_{k=1}^{n}(2k-1)=1+3+\cdots+(2n-1)=n^2 $$
:::

::: example Using the rules and the famous sums
**Problem.** Find (i) $\sum_{k=1}^{20}k$ (ii) $\sum_{k=1}^{10}(2k-1)$ (iii) $\sum_{k=1}^{10}(3k+2)$.

**Solution.** (i) $\frac{20\times21}{2}=210$.

(ii) This is the sum of the first 10 odd numbers, $10^2=100$.

(iii) Split the sum:
$$ \sum_{k=1}^{10}(3k+2)=3\sum_{k=1}^{10}k+\sum_{k=1}^{10}2=3\times55+10\times2=165+20=185 $$
**Check.** The terms are $5, 8, 11, \ldots, 32$; pairing first and last, $5+32=37$, five pairs: $5\times37=185$ ✓.
:::

### From the sums back to the terms

If we know the sum $S_n$ of the first $n$ terms for every $n$, we can recover each term: the $n$th term is what the $n$th step **adds**,
$$ t_n=S_n-S_{n-1}, \qquad t_1=S_1 $$

::: example Terms from a formula for the sum
**Problem.** The sum of the first $n$ terms of a series is $S_n=n^2+2n$. Find the first three terms and the general term.

**Solution.** $S_1=3$, $S_2=8$, $S_3=15$. So $t_1=3$, $t_2=8-3=5$, $t_3=15-8=7$. The terms go up by 2, so $t_n=2n+1$. Check: $S_3=3+5+7=15$ ✓.
:::

::: caution Count the terms from the limits
$\sum_{r=3}^{10}t_r$ has $10-3+1=8$ terms, not 10 and not 7. Students who start counting at the wrong value of the index get every later term wrong. Write out the first two and the last term before you add.
:::

::: note Project — a savings sequence
Plan to save Rs 5 in the first week, Rs 10 in the second, Rs 15 in the third and so on. (1) Write the sequence of weekly savings and its general term. (2) How much will you put aside in the 20th week? (3) Write the total for 20 weeks in sigma notation and find it with $\sum_{k=1}^{n}k=\frac{n(n+1)}{2}$. (4) Keep a real record for four weeks in your notebook and compare it with the plan. (Answers to check yourself: $t_n=5n$; Rs 100; $\sum_{k=1}^{20}5k=5\times210=$ Rs 1,050.)
:::

## Chapter summary

- A **sequence** is an ordered list made by a rule; its terms are $t_1, t_2, \ldots, t_n$. It is **finite** or **infinite**.
- The **general term** $t_n$ gives the term in position $n$; a sequence is a function on the natural numbers.
- Equal first differences $d$: **arithmetic**, $t_n=a+(n-1)d$. Equal ratios $r$: **geometric**, $t_n=ar^{n-1}$. Equal second differences: the rule contains $n^2$.
- To test whether a number is a term, solve $t_n=$ number; it is a term only if $n$ is a natural number.
- A **series** is the sum of the terms; $S_n=t_1+t_2+\cdots+t_n$ and $t_n=S_n-S_{n-1}$.
- $\sum_{k=1}^{n}t_k$ means "add $t_k$ for $k=1, 2, \ldots, n$"; the number of terms is upper $-$ lower $+1$.
- $\sum_{k=1}^{n}c=nc$, $\sum c\,t_k=c\sum t_k$, $\sum(a_k+b_k)=\sum a_k+\sum b_k$.
- $1+2+\cdots+n=\frac{n(n+1)}{2}$ and $1+3+5+\cdots+(2n-1)=n^2$.

## Practice questions

**Group A — Objective (1 mark each)**

1. The 5th term of the sequence with $t_n=2n+3$ is <span class="marks">[1]</span>
   (a) 10 (b) 13 (c) 11 (d) 8
2. The general term of $3, 6, 9, 12, \ldots$ is <span class="marks">[1]</span>
   (a) $n+3$ (b) $3n$ (c) $3n+3$ (d) $n^3$
3. The next term of $1, 4, 9, 16, \ldots$ is <span class="marks">[1]</span>
   (a) 20 (b) 25 (c) 24 (d) 32
4. The sequence of even numbers $2, 4, 6, \ldots$ is <span class="marks">[1]</span>
   (a) finite (b) infinite (c) a series (d) constant
5. The common difference of $20, 16, 12, 8, \ldots$ is <span class="marks">[1]</span>
   (a) 4 (b) $-4$ (c) 8 (d) 12
6. The next term of $2, 6, 18, 54, \ldots$ is <span class="marks">[1]</span>
   (a) 108 (b) 162 (c) 72 (d) 216
7. $\sum_{k=1}^{4}k$ equals <span class="marks">[1]</span>
   (a) 4 (b) 10 (c) 24 (d) 16
8. $2+4+6+8+10$ in sigma notation is <span class="marks">[1]</span>
   (a) $\sum_{k=1}^{5}2k$ (b) $\sum_{k=2}^{10}k$ (c) $\sum_{k=1}^{10}2k$ (d) $\sum_{k=1}^{5}(k+2)$
9. The number of terms in $\sum_{r=3}^{10}t_r$ is <span class="marks">[1]</span>
   (a) 7 (b) 8 (c) 10 (d) 13
10. If $t_n=(-1)^n$, then $t_3$ is <span class="marks">[1]</span>
    (a) 1 (b) $-1$ (c) 3 (d) $-3$
11. The sum of the first 10 natural numbers is <span class="marks">[1]</span>
    (a) 45 (b) 55 (c) 100 (d) 110
12. Which term of $5, 10, 15, \ldots$ is 60? <span class="marks">[1]</span>
    (a) 10th (b) 11th (c) 12th (d) 13th

::: note Answers to Group A
**1.** (b) — $t_5=2(5)+3=13$.
**2.** (b) — the multiples of 3: $t_n=3n$.
**3.** (b) — square numbers; the next is $5^2=25$.
**4.** (b) — there is no last even number.
**5.** (b) — each term is 4 less: $16-20=-4$.
**6.** (b) — each term is 3 times the one before: $54\times3=162$.
**7.** (b) — $1+2+3+4=10$.
**8.** (a) — the $k$th term is $2k$ and there are 5 terms.
**9.** (b) — $10-3+1=8$.
**10.** (b) — $(-1)^3=-1$.
**11.** (b) — $\frac{10\times11}{2}=55$.
**12.** (c) — $5n=60$ gives $n=12$.
:::

**Group B — Short answer (2 marks each)**

1. Write the first four terms of the sequence whose general term is $t_n=n^2-1$. <span class="marks">[2]</span>
2. Find the general term of $7, 11, 15, 19, \ldots$. <span class="marks">[2]</span>
3. Find the 20th term of $2, 5, 8, 11, \ldots$. <span class="marks">[2]</span>
4. Find the next two terms of $1, 3, 6, 10, 15, \ldots$ and state the rule. <span class="marks">[2]</span>
5. Is 75 a term of $4, 9, 14, 19, \ldots$? Give a reason. <span class="marks">[2]</span>
6. Expand and evaluate $\sum_{k=1}^{4}(3k-1)$. <span class="marks">[2]</span>
7. Write $1+8+27+64+125$ in sigma notation. <span class="marks">[2]</span>
8. Find the value of $\sum_{n=2}^{5}n^2$. <span class="marks">[2]</span>
9. If $t_n=\frac{n}{n+2}$, find $t_1$, $t_2$, $t_3$ and $t_{10}$. <span class="marks">[2]</span>
10. Write $\frac{1}{2}+\frac{1}{4}+\frac{1}{8}+\frac{1}{16}$ in sigma notation and find its value. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** $t_1=0$, $t_2=3$, $t_3=8$, $t_4=15$.
**2.** The difference is 4. Comparing with $4n$ ($4, 8, 12, 16$), each term is 3 more, so $t_n=4n+3$.
**3.** $t_n=3n-1$, so $t_{20}=60-1=59$.
**4.** The differences are $2, 3, 4, 5$, so the next differences are 6 and 7: the next terms are **21 and 28**. These are the triangular numbers, $t_n=\frac{n(n+1)}{2}$.
**5.** $t_n=5n-1$. Setting $5n-1=75$ gives $n=\frac{76}{5}=15.2$, which is not a natural number. So **75 is not a term** (the 15th term is 74 and the 16th is 79).
**6.** $2+5+8+11=26$.
**7.** The terms are $1^3, 2^3, \ldots, 5^3$, so the series is $\sum_{k=1}^{5}k^3$.
**8.** $4+9+16+25=54$.
**9.** $t_1=\frac{1}{3}$, $t_2=\frac{2}{4}=\frac{1}{2}$, $t_3=\frac{3}{5}$, $t_{10}=\frac{10}{12}=\frac{5}{6}$.
**10.** The $k$th term is $\frac{1}{2^k}$, so the series is $\sum_{k=1}^{4}\frac{1}{2^k}$. Its value is $\frac{8+4+2+1}{16}=\frac{15}{16}$.
:::

**Group C — Long answer (4 marks each)**

1. A row of $n$ squares made of matchsticks uses $4, 7, 10, \ldots$ sticks for $n=1, 2, 3, \ldots$. (i) Find the general term. (ii) How many sticks are needed for 30 squares? (iii) How many squares can be made with 151 sticks? <span class="marks">[4]</span>
2. Find the general term of $2, 6, 12, 20, 30, \ldots$ by the method of differences, find its 15th term, and find $\sum_{k=1}^{5}t_k$. <span class="marks">[4]</span>
3. (i) Expand $\sum_{k=1}^{6}(2k-1)$ and find its value. (ii) Show that the sum of the first $n$ odd numbers is $n^2$ for $n=1$ to 6, and draw the square-and-L picture for $n=4$. <span class="marks">[4]</span>
4. The first row of a hall has 20 seats and each row has 3 more seats than the row in front. (i) Write the sequence and its general term. (ii) How many seats are in the 12th row? (iii) Which row has 62 seats? (iv) Write the number of seats in the first 5 rows in sigma notation and find it. <span class="marks">[4]</span>
5. The general term of a sequence is $t_n=2^n-1$. (i) Write its first five terms. (ii) Write the series of these five terms in sigma notation and find $S_5$. (iii) Is 255 a term? If so, which one? <span class="marks">[4]</span>

::: note Answers to Group C
**1.** (i) The difference is 3; comparing with $3n$, each term is 1 more, so $t_n=3n+1$. (ii) $t_{30}=91$ sticks. (iii) $3n+1=151$ gives $3n=150$, so $n=50$ squares.
**2.** First differences $4, 6, 8, 10$; second differences 2, so compare with $n^2$: the leftovers $2-1=1$, $6-4=2$, $12-9=3$, $20-16=4$, $30-25=5$ are $n$. So $t_n=n^2+n$. Then $t_{15}=225+15=240$, and $\sum_{k=1}^{5}t_k=2+6+12+20+30=70$.
**3.** (i) $1+3+5+7+9+11=36$. (ii) Partial sums: $1=1^2$, $1+3=4=2^2$, $4+5=9=3^2$, $9+7=16=4^2$, $16+9=25=5^2$, $25+11=36=6^2$. For $n=4$ draw a $4\times4$ square of dots split into L-shaped layers of 1, 3, 5 and 7 dots: each new odd number wraps one L around the square before it, making the next square.
**4.** (i) $20, 23, 26, 29, \ldots$; the difference is 3, so $t_n=3n+17$. (ii) $t_{12}=36+17=53$ seats. (iii) $3n+17=62$ gives $3n=45$, so the **15th row**. (iv) $\sum_{k=1}^{5}(3k+17)=20+23+26+29+32=130$ seats.
**5.** (i) $1, 3, 7, 15, 31$. (ii) $\sum_{n=1}^{5}(2^n-1)=1+3+7+15+31$, so $S_5=57$. (iii) $2^n-1=255$ gives $2^n=256=2^8$, so $n=8$: 255 is the **8th term**.
:::
