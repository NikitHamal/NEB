---
subject: Optional Mathematics
grade: 10
unit: 1
title: Sequence and Series
hours: 0
area: Units
---

A bank adds the same interest to a deposit every month. A bacterium divides into two, then four, then eight. A staircase has steps that rise by equal amounts. All three situations produce a list of numbers that follows a pattern. A list that follows a rule is a **sequence**; when its terms are added, we get a **series**. This chapter studies the two most important patterns, the **arithmetic** pattern (add the same number each time) and the **geometric** pattern (multiply by the same number each time). You will learn to find any term, to insert means between two numbers, and to add up many terms without writing them all out.

::: key What the SEE asks from this chapter
Expect a 3- or 4-mark question on this chapter almost every year. The common types are: (i) find a term or the number of terms of an AP or GP; (ii) find a term from two given terms; (iii) **insert** arithmetic or geometric means; (iv) three numbers in AP or GP with a given sum and product; (v) the sum of $n$ terms; (vi) a real-life problem on savings, salary or growth. Write the formula first, then substitute. Marks are given for the formula, the substitution and the answer.
:::

```photo id="omath10/sunflower" caption="The seeds in a sunflower head spiral in two directions, and the two counts are consecutive Fibonacci numbers. A sequence is a rule that produces a list; nature uses this particular one." width="84"
```

## 1.1 Arithmetic sequence and the nth term

A **sequence** is a list of numbers written in a definite order, each number being called a **term**. We write the terms $t_1, t_2, t_3, \ldots, t_n, \ldots$ (the symbol $t_n$ is read "the $n$th term").

::: definition Arithmetic sequence (AP)
A sequence in which the **difference between any term and the term before it is always the same** is called an **arithmetic sequence** or **arithmetic progression (AP)**. This constant difference is the **common difference** $d$.
:::

For example, $5, 8, 11, 14, \ldots$ is an AP with first term $a=5$ and $d=8-5=3$. The sequence $20, 17, 14, 11, \ldots$ is an AP with $d=-3$ (decreasing). A sequence such as $1, 4, 9, 16, \ldots$ is **not** an AP because the differences $3, 5, 7$ are not equal.

```figure caption="The terms of an AP lie on a straight line. Here $5, 8, 11, \ldots$ rises by $d=3$ at each step, and $20, 17, 14, \ldots$ falls by $d=-3$."
n = np.arange(1, 8)
fig, ax = plt.subplots(figsize=(4.6, 2.6))
ax.plot(n, 5 + 3*(n-1), 'o-', color=ACCENT, ms=4, lw=1.2)
ax.plot(n, 20 - 3*(n-1), 's-', color=SERIES[1], ms=4, lw=1.2)
ax.text(7.15, 23, 'd = 3', color=ACCENT, fontsize=8.5, va='center')
ax.text(7.15, 2, 'd = -3', color=SERIES[1], fontsize=8.5, va='center')
ax.set_xlim(0.6, 8.4); ax.set_ylim(-1, 26)
ax.set_xlabel('term number n', fontsize=8.5); ax.set_ylabel('term t(n)', fontsize=8.5)
ax.set_xticks(n); ax.tick_params(labelsize=8)
ax.grid(color=GRID, lw=0.5); ax.spines[['top','right']].set_visible(False)
fig.tight_layout(pad=0.4)
```

### The general term

Let the first term be $a$ and the common difference $d$. Then

$$ t_1=a,\quad t_2=a+d,\quad t_3=a+2d,\quad t_4=a+3d,\ \ldots $$

The coefficient of $d$ is always **one less than the term number**. So the $n$th term is $a+(n-1)d$.

::: key General term of an AP
$$ t_n = a+(n-1)d $$
where $a$ is the first term, $d$ the common difference and $n$ the number of the term. If $l$ is the last term of an AP with $n$ terms, then $l=a+(n-1)d$, so the number of terms is $n=\frac{l-a}{d}+1$.
:::

::: example Finding a term and the position of a term
**Problem.** For the AP $5, 8, 11, \ldots$ find (i) the 20th term, (ii) which term is 101.

**Solution.** Here $a=5$ and $d=8-5=3$.

(i) $t_{20}=a+19d=5+19\times 3=5+57=62$.

(ii) Let $t_n=101$. Then $5+(n-1)\times 3=101$, so $(n-1)\times 3=96$, $n-1=32$ and $n=33$. So 101 is the **33rd term**.
:::

::: example Terms from two given terms
**Problem.** In an AP the 4th term is 14 and the 9th term is 29. Find the AP and its 15th term.

**Solution.** $t_4=a+3d=14$ …… (i) and $t_9=a+8d=29$ …… (ii).

Subtract (i) from (ii): $5d=15$, so $d=3$. From (i), $a=14-9=5$. The AP is $5, 8, 11, 14, \ldots$ and

$$ t_{15}=a+14d=5+14\times 3=47. $$
:::

::: example Is a number a term?
**Problem.** Is 150 a term of the AP $7, 12, 17, \ldots$ ? Find the number of terms in the AP $3, 7, 11, \ldots, 95$.

**Solution.** For $7, 12, 17, \ldots$: $a=7$, $d=5$. If $t_n=150$ then $7+5(n-1)=150$, so $n-1=\frac{143}{5}=28.6$. Since $n$ must be a whole number, **150 is not a term**.

For $3, 7, 11, \ldots, 95$: $a=3$, $d=4$, $l=95$.

$$ n=\frac{l-a}{d}+1=\frac{95-3}{4}+1=23+1=24 \text{ terms.} $$
:::

### Three numbers in AP

When three numbers are in AP and their sum is given, take them as $a-d,\ a,\ a+d$. The middle one is $a$, and the $d$'s cancel when we add.

::: example Sum and product of three numbers in AP
**Problem.** Three numbers are in AP. Their sum is 21 and their product is 315. Find them.

**Solution.** Let the numbers be $a-d,\ a,\ a+d$.

Sum: $(a-d)+a+(a+d)=3a=21$, so $a=7$.

Product: $(a-d)\,a\,(a+d)=a(a^2-d^2)=315$. Putting $a=7$: $7(49-d^2)=315$, so $49-d^2=45$ and $d^2=4$, $d=\pm 2$.

For $d=2$ the numbers are $5, 7, 9$; for $d=-2$ they are $9, 7, 5$. The three numbers are **5, 7, 9**.
:::

::: caution Common mistakes
- Using $t_n=a+nd$. The correct rule is $a+(n-1)d$: the first term has **no** $d$ added.
- Taking $d=t_1-t_2$. Always subtract the earlier term from the later: $d=t_2-t_1$.
- For three numbers in AP, taking them as $a, a+d, a+2d$ when the sum is given. It works but makes the algebra longer; use $a-d, a, a+d$.
:::

### Real-life use

::: example A rising salary
**Problem.** A clerk in Pokhara starts on a monthly salary of Rs 20,000, and her salary rises by Rs 1,500 each year. What will her monthly salary be in the 8th year?

**Solution.** The yearly salaries form an AP with $a=20{,}000$ and $d=1{,}500$.

$$ t_8=a+7d=20000+7\times 1500=20000+10500=\text{Rs } 30{,}500. $$
:::

## 1.2 Arithmetic mean

If three numbers $a, A, b$ are in AP, the middle number $A$ is the **arithmetic mean** of $a$ and $b$. In an AP, $A-a=b-A$, so $2A=a+b$.

::: key Arithmetic mean of two numbers
$$ A=\frac{a+b}{2} $$
The AM of two numbers is exactly halfway between them.
:::

### Inserting several arithmetic means

To **insert $n$ arithmetic means** between $a$ and $b$ means to put $n$ numbers between them so that all $n+2$ numbers form an AP. The sequence is

$$ a,\ A_1,\ A_2,\ \ldots,\ A_n,\ b $$

It has $n+2$ terms, with first term $a$ and last term $b$. The last term is the $(n+2)$th, so $b=a+(n+1)d$.

::: key Common difference when inserting $n$ means
$$ d=\frac{b-a}{n+1} $$
Then $A_1=a+d,\ A_2=a+2d,\ \ldots,\ A_n=a+nd$.
:::

::: example Inserting arithmetic means
**Problem.** Insert four arithmetic means between 3 and 18.

**Solution.** Here $a=3$, $b=18$, $n=4$.

$$ d=\frac{b-a}{n+1}=\frac{18-3}{5}=3. $$

The means are $3+3,\ 3+6,\ 3+9,\ 3+12$, that is **6, 9, 12, 15**. The full AP is $3, 6, 9, 12, 15, 18$.
:::

::: example Sum of the means
**Problem.** Five arithmetic means are inserted between 7 and 25. Find their sum.

**Solution.** $d=\frac{25-7}{6}=3$. The means are $10, 13, 16, 19, 22$ and their sum is $80$.

Shortcut: the sum of $n$ arithmetic means between $a$ and $b$ is $n\times\frac{a+b}{2}$. Here $5\times\frac{7+25}{2}=5\times 16=80$. ✓
:::

::: example Means between a negative and a positive number
**Problem.** Insert three arithmetic means between $-2$ and $10$.

**Solution.** $d=\frac{10-(-2)}{4}=\frac{12}{4}=3$. The means are $-2+3,\ -2+6,\ -2+9$, that is **1, 4, 7**.
:::

::: example Finding the numbers from their mean
**Problem.** The arithmetic mean of two numbers is 13 and one of them is 7. Find the other number. Then insert two arithmetic means between the two numbers.

**Solution.** $\frac{7+b}{2}=13$, so $7+b=26$ and $b=19$. Now insert two means between 7 and 19: $d=\frac{19-7}{3}=4$, so the means are $11$ and $15$.
:::

## 1.3 Sum of an arithmetic series

Adding the terms of a sequence gives a **series**. The sum of the first $n$ terms of an AP is called an **arithmetic series** and is written $S_n$.

::: derivation Sum of the first n terms of an AP
We start from the AP with first term $a$, common difference $d$ and $n$ terms. We are heading for a formula for $S_n$.

**Setting up.** The last term is $l=a+(n-1)d$.

**Step 1 — write the sum forwards.**
$$ S_n=a+(a+d)+(a+2d)+\cdots+(l-2d)+(l-d)+l $$

**Step 2 — write the same sum backwards.**
$$ S_n=l+(l-d)+(l-2d)+\cdots+(a+2d)+(a+d)+a $$

**Step 3 — add the two lines, pair by pair.** Each pair adds up to $a+l$, and there are $n$ pairs:
$$ 2S_n=(a+l)+(a+l)+\cdots+(a+l)=n(a+l) $$

**Step 4 — divide by 2.**
$$ S_n=\frac{n}{2}(a+l) $$

**Step 5 — put $l=a+(n-1)d$.**
$$ S_n=\frac{n}{2}\left[2a+(n-1)d\right] $$

**What it means.** The sum is the number of terms times the **average** of the first and last term. It works for any AP, including decreasing ones.
:::

::: tip The examiner is looking for
(1) writing the series forwards and backwards, (2) adding to get $n(a+l)$, (3) dividing by 2, (4) substituting $l=a+(n-1)d$ to reach the second form.
:::

::: key Sum of an AP
$$ S_n=\frac{n}{2}\left[2a+(n-1)d\right]=\frac{n}{2}(a+l) $$
Use the first form when you know $a$ and $d$; use the second when you know the last term $l$. Also $t_n=S_n-S_{n-1}$.
:::

```figure caption="Why $S_n=\frac{n}{2}(a+l)$: two copies of the series $1+2+3+4+5$ (dark and light bars) fit together into a rectangle $5\times 6$, so $S_5=\frac{5\times 6}{2}=15$."
fig, ax = plt.subplots(figsize=(4.4, 2.6))
for i in range(1, 6):
    ax.bar(i, i, width=0.9, color=ACCENT, ec='white', alpha=0.9)
    ax.bar(i, 6 - i, bottom=i, width=0.9, color='#bfdbfe', ec='white')
    ax.text(i, i/2, str(i), ha='center', va='center', color='white', fontsize=8.5)
    ax.text(i, i + (6 - i)/2, str(6 - i), ha='center', va='center', color=INK, fontsize=8.5)
ax.annotate('', xy=(5.65, 6), xytext=(5.65, 0), arrowprops=dict(arrowstyle='<->', color=MUTED, lw=0.9))
ax.text(5.85, 3, 'a + l = 6', rotation=90, va='center', fontsize=8.5)
ax.set_xlim(0.4, 6.2); ax.set_ylim(0, 6.6); ax.set_xticks(range(1, 6)); ax.set_yticks([])
ax.set_xlabel('term number', fontsize=8.5); ax.tick_params(labelsize=8)
ax.spines[['top','right','left']].set_visible(False)
fig.tight_layout(pad=0.4)
```

### Three special sums

Take $a=1$ and $d=1$ (natural numbers), $a=2,\ d=2$ (even numbers) and $a=1,\ d=2$ (odd numbers) in $S_n=\frac{n}{2}[2a+(n-1)d]$:

| Series | Sum of first $n$ terms | Check with $n=10$ |
|---|---|---|
| $1+2+3+\cdots+n$ | $\frac{n(n+1)}{2}$ | $55$ |
| $2+4+6+\cdots+2n$ | $n(n+1)$ | $110$ |
| $1+3+5+\cdots+(2n-1)$ | $n^2$ | $100$ |

::: example Sum of an AP when a, d and n are known
**Problem.** Find the sum of the first 20 terms of $3+7+11+\cdots$.

**Solution.** $a=3$, $d=4$, $n=20$.

$$ S_{20}=\frac{20}{2}\left[2\times 3+19\times 4\right]=10\,(6+76)=10\times 82=820. $$
:::

::: example Sum when the last term is known
**Problem.** Find the sum of $5+8+11+\cdots+80$.

**Solution.** $a=5$, $d=3$, $l=80$. First find $n$:

$$ n=\frac{l-a}{d}+1=\frac{80-5}{3}+1=26. $$

$$ S_{26}=\frac{n}{2}(a+l)=\frac{26}{2}(5+80)=13\times 85=1105. $$
:::

::: example Sum of multiples
**Problem.** Find the sum of all multiples of 3 between 1 and 100.

**Solution.** The multiples are $3, 6, 9, \ldots, 99$. Here $a=3$, $d=3$, $l=99$, so $n=\frac{99-3}{3}+1=33$.

$$ S_{33}=\frac{33}{2}(3+99)=\frac{33}{2}\times 102=33\times 51=1683. $$
:::

::: example Two answers for the number of terms
**Problem.** How many terms of the AP $24, 21, 18, \ldots$ must be taken so that the sum is 78? Explain the double answer.

**Solution.** $a=24$, $d=-3$, $S_n=78$.

$$ \frac{n}{2}\left[48+(n-1)(-3)\right]=78 \;\Rightarrow\; n(51-3n)=156 \;\Rightarrow\; 3n^2-51n+156=0 $$

Divide by 3: $n^2-17n+52=0$, so $(n-4)(n-13)=0$ and $n=4$ or $n=13$.

Both are correct. The terms are $24, 21, 18, 15, 12, 9, 6, 3, 0, -3, -6, -9, -12$. The first 4 terms add up to $24+21+18+15=78$. The terms $t_5$ to $t_{13}$ add up to $12+9+6+3+0-3-6-9-12=0$, so 13 terms also give 78.
:::

::: example From the sum to the sequence
**Problem.** The sum of the first $n$ terms of a series is $S_n=3n^2+2n$. Find the first term, the common difference and the $n$th term.

**Solution.** $t_1=S_1=3+2=5$. $S_2=3(4)+4=16$, so $t_2=S_2-S_1=16-5=11$. Then $d=11-5=6$.

For the $n$th term: $t_n=S_n-S_{n-1}=3n^2+2n-\left[3(n-1)^2+2(n-1)\right]=3n^2+2n-3n^2+6n-3-2n+2=6n-1$.

Check: $t_1=6-1=5$ ✓, $t_2=12-1=11$ ✓.
:::

::: example Monthly savings
**Problem.** Ram saves Rs 100 in the first month and increases his saving by Rs 50 every month. How much does he save in the 12th month, and how much in the whole year?

**Solution.** $a=100$, $d=50$, $n=12$.

$t_{12}=a+11d=100+550=\text{Rs } 650$.

$S_{12}=\frac{12}{2}\left[2\times 100+11\times 50\right]=6\times 750=\text{Rs } 4{,}500$.
:::

## 1.4 Geometric sequence and the nth term

::: definition Geometric sequence (GP)
A sequence in which **each term is obtained by multiplying the previous term by the same non-zero number** is called a **geometric sequence** or **geometric progression (GP)**. The constant multiplier is the **common ratio** $r=\frac{t_2}{t_1}=\frac{t_3}{t_2}=\cdots$.
:::

For example $3, 6, 12, 24, \ldots$ has $a=3$ and $r=2$. The sequence $27, 9, 3, 1, \ldots$ has $r=\frac{1}{3}$. The sequence $2, -6, 18, -54, \ldots$ has $r=-3$; its terms alternate in sign.

```figure caption="The terms of a GP climb faster and faster: $3, 6, 12, 24, \ldots$ ($r=2$), compared with the AP $3, 6, 9, 12, \ldots$ ($d=3$)."
n = np.arange(1, 8)
fig, ax = plt.subplots(figsize=(4.6, 2.6))
ax.plot(n, 3*2.0**(n-1), 'o-', color=ACCENT, ms=4, lw=1.2)
ax.plot(n, 3 + 3*(n-1), 's-', color=SERIES[1], ms=4, lw=1.2)
ax.text(5.7, 150, 'GP, r = 2', color=ACCENT, fontsize=8.5, ha='right')
ax.text(6.4, 38, 'AP, d = 3', color=SERIES[1], fontsize=8.5, ha='center')
ax.set_xlim(0.6, 7.4); ax.set_ylim(0, 210)
ax.set_xlabel('term number n', fontsize=8.5); ax.set_ylabel('term t(n)', fontsize=8.5)
ax.set_xticks(n); ax.tick_params(labelsize=8)
ax.grid(color=GRID, lw=0.5); ax.spines[['top','right']].set_visible(False)
fig.tight_layout(pad=0.4)
```

### The general term

With first term $a$ and common ratio $r$:

$$ t_1=a,\quad t_2=ar,\quad t_3=ar^2,\quad t_4=ar^3,\ \ldots $$

The power of $r$ is **one less than the term number**.

::: key General term of a GP
$$ t_n=ar^{\,n-1} $$
where $a$ is the first term, $r$ the common ratio. If the last term of an $n$-term GP is $l$, then $l=ar^{n-1}$.
:::

::: example Term and position in a GP
**Problem.** For the GP $3, 6, 12, \ldots$ find the 8th term and the position of 768.

**Solution.** $a=3$, $r=2$.

$t_8=ar^7=3\times 2^7=3\times 128=384$.

If $t_n=768$: $3\times 2^{n-1}=768$, so $2^{n-1}=256=2^8$. Hence $n-1=8$ and $n=9$.
:::

::: example Terms from two given terms
**Problem.** The 4th term of a GP is 24 and the 7th term is 192. Find the GP and its 10th term.

**Solution.** $ar^3=24$ …… (i) and $ar^6=192$ …… (ii).

Divide (ii) by (i): $r^3=\frac{192}{24}=8$, so $r=2$. From (i): $a\times 8=24$, so $a=3$.

The GP is $3, 6, 12, 24, \ldots$ and $t_{10}=3\times 2^9=3\times 512=1536$.
:::

::: example Number of terms
**Problem.** How many terms are there in the GP $2, 6, 18, \ldots, 1458$?

**Solution.** $a=2$, $r=3$, $l=1458$. From $l=ar^{n-1}$: $3^{n-1}=\frac{1458}{2}=729=3^6$. So $n-1=6$ and $n=7$.
:::

### Three numbers in GP

When three numbers are in GP and their **product** is given, take them as $\frac{a}{r},\ a,\ ar$. The $r$'s cancel when we multiply.

::: example Sum and product of three numbers in GP
**Problem.** Three numbers are in GP. Their sum is 21 and their product is 216. Find the numbers.

**Solution.** Let the numbers be $\frac{a}{r},\ a,\ ar$.

Product: $\frac{a}{r}\times a\times ar=a^3=216$, so $a=6$.

Sum: $\frac{6}{r}+6+6r=21$. Multiply by $r$: $6+6r+6r^2=21r$, so $6r^2-15r+6=0$, that is $2r^2-5r+2=0$.

$(2r-1)(r-2)=0$, so $r=2$ or $r=\frac{1}{2}$. For $r=2$ the numbers are $3, 6, 12$; for $r=\frac{1}{2}$ they are $12, 6, 3$. The numbers are **3, 6, 12**.
:::

::: caution Common mistakes
- Writing $t_n=(ar)^{n-1}$ or $ar^n$. The correct form is $ar^{n-1}$; $r$ is raised to $n-1$ and **only** $r$.
- Taking $r=t_1\div t_2$. The ratio is the **later** term divided by the **earlier** one.
- Forgetting the negative ratio. In $2, -6, 18, \ldots$ the ratio is $-3$, not $3$.
:::

::: example Bacteria in a culture
**Problem.** A culture has 500 bacteria, and the number doubles every hour. How many bacteria are there after 6 hours?

**Solution.** The counts $500, 1000, 2000, \ldots$ form a GP with $a=500$, $r=2$. After 6 hours we need the 7th term (the 1st term is the count at hour 0):

$$ t_7=500\times 2^6=500\times 64=32{,}000. $$
:::

## 1.5 Geometric mean

If three positive numbers $a, G, b$ are in GP, then $G$ is the **geometric mean** of $a$ and $b$. In a GP, $\frac{G}{a}=\frac{b}{G}$, so $G^2=ab$.

::: key Geometric mean of two numbers
$$ G=\sqrt{ab} \qquad (a,\,b \text{ positive}) $$
The AM, GM and the numbers are related by $A\geq G$, and $A^2-G^2=\left(\frac{a-b}{2}\right)^2$.
:::

### Inserting several geometric means

To insert $n$ geometric means between $a$ and $b$, make $a, G_1, G_2, \ldots, G_n, b$ a GP. It has $n+2$ terms, and the last term is the $(n+2)$th, so $b=ar^{n+1}$.

::: key Common ratio when inserting $n$ means
$$ r=\left(\frac{b}{a}\right)^{\frac{1}{n+1}} $$
Then $G_1=ar,\ G_2=ar^2,\ \ldots,\ G_n=ar^n$. The product of the $n$ means is $G^n$ where $G=\sqrt{ab}$.
:::

::: example Inserting geometric means
**Problem.** Insert three geometric means between 2 and 32.

**Solution.** $a=2$, $b=32$, $n=3$. $r^4=\frac{32}{2}=16$, so $r=2$.

The means are $2\times 2,\ 2\times 4,\ 2\times 8$, that is **4, 8, 16**. The GP is $2, 4, 8, 16, 32$. Check the product of the means: $4\times 8\times 16=512=8^3$, and $\sqrt{2\times 32}=8$. ✓
:::

::: example Four geometric means
**Problem.** Insert four geometric means between 3 and 729.

**Solution.** $r^5=\frac{729}{3}=243=3^5$, so $r=3$. The means are $9, 27, 81, 243$.
:::

::: example AM and GM of the same pair
**Problem.** Find the AM and GM of 4 and 16, and the difference between them.

**Solution.** $A=\frac{4+16}{2}=10$ and $G=\sqrt{4\times 16}=\sqrt{64}=8$. The difference is $A-G=2$, and $A>G$, as always for two unequal positive numbers.
:::

```figure caption="AM and GM of $a=4$ and $b=16$. On a diameter of length $a+b$, the radius is the AM (10) and the perpendicular at the join of $a$ and $b$ meets the semicircle at height $\sqrt{ab}$, the GM (8)."
a_, b_ = 4.0, 16.0
R = (a_ + b_)/2
fig, ax = plt.subplots(figsize=(4.6, 2.7))
t = np.linspace(0, np.pi, 200)
ax.plot(R + R*np.cos(t), R*np.sin(t), color=INK, lw=1.2)
ax.plot([0, a_ + b_], [0, 0], color=INK, lw=1.2)
ax.plot([a_, a_], [0, np.sqrt(a_*b_)], color=ACCENT, lw=1.6)
ax.plot([R, R], [0, R], color=SERIES[1], lw=1.4, ls='--')
ax.plot([a_], [0], 'o', color=INK, ms=3)
ax.text(a_ - 0.4, np.sqrt(a_*b_)/2, 'GM = 8', color=ACCENT, ha='right', va='center', fontsize=8.5)
ax.text(R + 0.4, R/2, 'AM = 10', color=SERIES[1], ha='left', va='center', fontsize=8.5)
ax.text(a_/2, -1.3, 'a = 4', ha='center', fontsize=8.5)
ax.text(a_ + b_/2, -1.3, 'b = 16', ha='center', fontsize=8.5)
ax.set_xlim(-1, 21); ax.set_ylim(-2.5, 11.5); ax.set_aspect('equal'); ax.axis('off')
fig.tight_layout(pad=0.3)
```

::: example Finding the numbers from their AM and GM
**Problem.** The AM and GM of two positive numbers are 5 and 4. Find the numbers.

**Solution.** $\frac{a+b}{2}=5$ gives $a+b=10$; $\sqrt{ab}=4$ gives $ab=16$. The numbers are the roots of $x^2-10x+16=0$, i.e. $(x-2)(x-8)=0$. They are **2 and 8**.
:::

## 1.6 Sum of a geometric series

::: derivation Sum of the first n terms of a GP
We start from the GP with first term $a$, common ratio $r$ and $n$ terms. We are heading for a formula for $S_n$.

**Step 1 — write the sum.**
$$ S_n=a+ar+ar^2+\cdots+ar^{n-1} \qquad (\mathrm{i}) $$

**Step 2 — multiply both sides by $r$.** Every term moves one place to the right:
$$ rS_n=ar+ar^2+ar^3+\cdots+ar^{n-1}+ar^n \qquad (\mathrm{ii}) $$

**Step 3 — subtract (ii) from (i).** All the middle terms cancel:
$$ S_n-rS_n=a-ar^n $$

**Step 4 — factorise both sides.**
$$ S_n(1-r)=a(1-r^n) $$

**Step 5 — divide by $1-r$** (needs $r\neq 1$):
$$ S_n=\frac{a(1-r^n)}{1-r} $$

**What it means.** Multiplying by $-1$ top and bottom gives the equivalent form $S_n=\frac{a(r^n-1)}{r-1}$. Use this form when $r>1$ so that both numerator and denominator are positive. If $r=1$ all terms equal $a$ and $S_n=na$.
:::

::: tip The examiner is looking for
(1) writing $S_n$ and $rS_n$, (2) subtracting to cancel the middle terms, (3) factorising to get $S_n(1-r)=a(1-r^n)$, (4) the final formula.
:::

::: key Sum of a GP
$$ S_n=\frac{a(r^n-1)}{r-1}\ \ (r>1) \qquad S_n=\frac{a(1-r^n)}{1-r}\ \ (r<1) \qquad S_n=na\ \ (r=1) $$
When the last term $l$ is known, $S_n=\frac{lr-a}{r-1}$.
:::

::: example Sum of a GP, r greater than 1
**Problem.** Find the sum of the first 6 terms of $2+6+18+\cdots$.

**Solution.** $a=2$, $r=3$, $n=6$.

$$ S_6=\frac{a(r^6-1)}{r-1}=\frac{2(729-1)}{3-1}=\frac{2\times 728}{2}=728. $$
:::

::: example Sum of a GP, r less than 1
**Problem.** Find the sum of the first 8 terms of $1+\frac{1}{2}+\frac{1}{4}+\cdots$.

**Solution.** $a=1$, $r=\frac{1}{2}$, $n=8$.

$$ S_8=\frac{1-\left(\frac{1}{2}\right)^8}{1-\frac{1}{2}}=2\left(1-\frac{1}{256}\right)=2\times\frac{255}{256}=\frac{255}{128}. $$
:::

::: example Number of terms from the sum
**Problem.** How many terms of $3+6+12+\cdots$ add up to 381?

**Solution.** $a=3$, $r=2$.

$$ \frac{3(2^n-1)}{2-1}=381 \;\Rightarrow\; 2^n-1=127 \;\Rightarrow\; 2^n=128=2^7. $$

So $n=7$.
:::

::: example Using two sums
**Problem.** In a GP with positive common ratio, the sum of the first two terms is 12 and the sum of the first four terms is 60. Find the first term, the common ratio and the sum of the first six terms.

**Solution.** $S_2=a(1+r)=12$. Also $S_4=a(1+r)(1+r^2)=S_2(1+r^2)$, so $60=12(1+r^2)$, giving $1+r^2=5$, $r^2=4$ and $r=2$ (positive).

Then $a(1+2)=12$, so $a=4$. The GP is $4, 8, 16, 32, \ldots$ and

$$ S_6=\frac{4(2^6-1)}{2-1}=4\times 63=252. $$
:::

::: example Doubling every day
**Problem.** A girl saves Re 1 on day 1, Rs 2 on day 2, Rs 4 on day 3 and so on, doubling every day. How much has she saved in all after 15 days?

**Solution.** $a=1$, $r=2$, $n=15$.

$$ S_{15}=\frac{1\times(2^{15}-1)}{2-1}=32768-1=\text{Rs } 32{,}767. $$
:::

::: example A rumour spreads
**Problem.** One student tells a rumour to 3 friends. Each of them tells 3 new friends, and so on. Counting the first student, how many people know the rumour after 4 such rounds?

**Solution.** The number of people who hear in each round is $1, 3, 9, 27, 81$, a GP with $a=1$, $r=3$ and 5 terms.

$$ S_5=\frac{3^5-1}{3-1}=\frac{242}{2}=121 \text{ people.} $$
:::

## 1.7 Exercises of the SEE type

These problems mix both patterns, the way the SEE does.

::: example AP changed into a GP
**Problem.** Three numbers in AP have sum 15. If 1, 4 and 19 are added to them respectively, the new numbers are in GP. Find the numbers.

**Solution.** Let the numbers be $a-d,\ a,\ a+d$. Their sum is $3a=15$, so $a=5$.

The new numbers are $(5-d)+1=6-d$, then $5+4=9$, then $(5+d)+19=24+d$. For a GP the middle term squared equals the product of the others:

$$ 9^2=(6-d)(24+d) \;\Rightarrow\; 81=144-18d-d^2 \;\Rightarrow\; d^2+18d-63=0. $$

$(d-3)(d+21)=0$, so $d=3$ or $d=-21$.

For $d=3$ the numbers are **2, 5, 8** (new GP: $3, 9, 27$). For $d=-21$ they are $26, 5, -16$ (new GP: $27, 9, 3$). Both satisfy the conditions.
:::

::: example Bounce of a ball
**Problem.** A ball is dropped from a height of 64 m. Each time it bounces back to half the previous height. How high does it rise after the 6th bounce, and what total distance has it travelled up to the moment of hitting the ground for the 4th time?

**Solution.** The rebound heights $32, 16, 8, 4, 2, 1, \ldots$ form a GP with $a=32$, $r=\frac{1}{2}$. After the 6th bounce: $t_6=32\left(\frac{1}{2}\right)^5=1$ m.

By the 4th landing the ball has fallen 64 m, then risen and fallen 32, 16 and 8 m on the first three rebounds. Total $=64+2(32+16+8)=64+112=176$ m.
:::

::: example Seats in a hall
**Problem.** An auditorium has 20 seats in the first row, and each next row has 2 more seats than the one before. There are 15 rows. Find the number of seats in the last row and in the whole hall.

**Solution.** AP with $a=20$, $d=2$, $n=15$.

$l=t_{15}=20+14\times 2=48$ seats.

$S_{15}=\frac{15}{2}(20+48)=\frac{15}{2}\times 68=510$ seats.
:::

::: example Compound growth as a GP
**Problem.** Rs 10,000 is invested at 10% compound interest per year. The amount after 1 year, 2 years, 3 years, … forms a GP. Find the first three terms and the amount after 5 years.

**Solution.** Each year the amount is multiplied by $1.1$. The amounts are $11000,\ 12100,\ 13310,\ \ldots$ with $a=11000$ and $r=1.1$.

After 5 years: $t_5=11000\times 1.1^4=11000\times 1.4641=\text{Rs } 16{,}105.10$. (Equivalent to $10000\times 1.1^5$.)
:::

## Chapter summary

- **AP:** $t_n=a+(n-1)d$ with $d=t_2-t_1$; three numbers in AP: $a-d,\ a,\ a+d$.
- **AM:** $A=\frac{a+b}{2}$; to insert $n$ means, $d=\frac{b-a}{n+1}$.
- **Sum of an AP:** $S_n=\frac{n}{2}[2a+(n-1)d]=\frac{n}{2}(a+l)$; $t_n=S_n-S_{n-1}$. Sums of the first $n$ natural, even and odd numbers: $\frac{n(n+1)}{2}$, $n(n+1)$, $n^2$.
- **GP:** $t_n=ar^{n-1}$ with $r=\frac{t_2}{t_1}$; three numbers in GP: $\frac{a}{r},\ a,\ ar$.
- **GM:** $G=\sqrt{ab}$; to insert $n$ means, $r=\left(\frac{b}{a}\right)^{\frac{1}{n+1}}$; $A\geq G$.
- **Sum of a GP:** $S_n=\frac{a(r^n-1)}{r-1}$ for $r>1$ and $\frac{a(1-r^n)}{1-r}$ for $r<1$; $S_n=na$ for $r=1$.
- Inserting $n$ means gives $n+2$ terms in all, with $b$ as the $(n+2)$th term.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The 10th term of the AP $2, 5, 8, \ldots$ is <span class="marks">[1]</span>
   (a) 27 (b) 29 (c) 32 (d) 30
2. The arithmetic mean between 7 and 19 is <span class="marks">[1]</span>
   (a) 12 (b) 26 (c) 13 (d) 14
3. The geometric mean between 4 and 25 is <span class="marks">[1]</span>
   (a) 10 (b) 14.5 (c) 12 (d) 100
4. The sum of the first 20 natural numbers is <span class="marks">[1]</span>
   (a) 200 (b) 210 (c) 400 (d) 420
5. The 5th term of the GP $2, 6, 18, \ldots$ is <span class="marks">[1]</span>
   (a) 54 (b) 108 (c) 162 (d) 486
6. The common ratio of the GP $27, 9, 3, \ldots$ is <span class="marks">[1]</span>
   (a) 3 (b) $\frac{1}{3}$ (c) $-3$ (d) $-\frac{1}{3}$
7. The sum of the first 10 odd numbers is <span class="marks">[1]</span>
   (a) 55 (b) 90 (c) 100 (d) 110

::: note Answers to Group A
**1.** (b) — $t_{10}=2+9\times 3=29$.
**2.** (c) — $\frac{7+19}{2}=13$.
**3.** (a) — $\sqrt{4\times 25}=\sqrt{100}=10$.
**4.** (b) — $\frac{20\times 21}{2}=210$.
**5.** (c) — $2\times 3^4=162$.
**6.** (b) — $\frac{9}{27}=\frac{1}{3}$.
**7.** (c) — the sum of the first $n$ odd numbers is $n^2=100$.
:::

**Group B — Short answer (2 marks each)**

1. Find the 25th term of the AP $4, 9, 14, \ldots$ <span class="marks">[2]</span>
2. Insert three arithmetic means between 5 and 21. <span class="marks">[2]</span>
3. Find the sum of $4+8+12+\cdots+40$. <span class="marks">[2]</span>
4. Find the 6th term of the GP $3, 6, 12, \ldots$ <span class="marks">[2]</span>
5. Insert one geometric mean between 5 and 20. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** $a=4$, $d=5$: $t_{25}=4+24\times 5=124$.
**2.** $d=\frac{21-5}{4}=4$. The means are $9, 13, 17$.
**3.** $a=4$, $d=4$, $l=40$, so $n=10$. $S_{10}=\frac{10}{2}(4+40)=220$.
**4.** $t_6=3\times 2^5=96$.
**5.** $G=\sqrt{5\times 20}=\sqrt{100}=10$.
:::

**Group C — Short answer (3 marks each)**

1. In an AP the 3rd term is 12 and the 8th term is 37. Find the first term, the common difference and the 20th term. <span class="marks">[3]</span>
2. How many terms of the AP $5, 9, 13, \ldots$ must be added to make 275? <span class="marks">[3]</span>
3. In a GP the 2nd term is 6 and the 5th term is 48. Find the GP and its 8th term. <span class="marks">[3]</span>
4. Find the sum of the first 7 terms of $1+3+9+\cdots$ <span class="marks">[3]</span>
5. The AM and GM of two positive numbers are 17 and 15. Find the numbers. <span class="marks">[3]</span>

::: note Answers to Group C
**1.** $a+2d=12$ and $a+7d=37$. Subtract: $5d=25$, $d=5$, $a=2$. $t_{20}=2+19\times 5=97$.
**2.** $a=5$, $d=4$. $\frac{n}{2}[10+4(n-1)]=275$, so $n(2n+3)=275$, i.e. $2n^2+3n-275=0$. $(n-11)(2n+25)=0$, so $n=11$ (the negative root is rejected).
**3.** $ar=6$, $ar^4=48$, so $r^3=8$, $r=2$, $a=3$. The GP is $3, 6, 12, \ldots$ and $t_8=3\times 2^7=384$.
**4.** $a=1$, $r=3$: $S_7=\frac{3^7-1}{3-1}=\frac{2186}{2}=1093$.
**5.** $a+b=34$, $ab=225$. The numbers are the roots of $x^2-34x+225=0$, i.e. $(x-9)(x-25)=0$. They are 9 and 25.
:::

**Group D — Long answer (4 marks each)**

1. Three numbers in AP have sum 27 and product 693. Find the numbers. <span class="marks">[4]</span>
2. The sum of the first $n$ terms of an AP is $2n^2+3n$. Find the first term, the common difference and the 10th term. <span class="marks">[4]</span>
3. Three numbers in GP have sum 39 and product 729. Find them. <span class="marks">[4]</span>
4. A worker earns Rs 12,000 in the first month and her monthly pay rises by Rs 500 each month. Find her pay in the 12th month and her total earnings in 12 months. <span class="marks">[4]</span>
5. Insert four geometric means between 3 and 96 and find the sum of all six terms of the GP. <span class="marks">[4]</span>

::: note Answers to Group D
**1.** Let the numbers be $a-d,\ a,\ a+d$. Sum $=3a=27$, so $a=9$. Product: $9(81-d^2)=693$, so $81-d^2=77$, $d^2=4$, $d=\pm 2$. The numbers are **7, 9, 11**.
**2.** $t_1=S_1=2+3=5$. $S_2=8+6=14$, so $t_2=9$ and $d=4$. $t_n=S_n-S_{n-1}=4n+1$, so $t_{10}=41$.
**3.** Let the numbers be $\frac{a}{r},\ a,\ ar$. Product $=a^3=729$, so $a=9$. Sum: $\frac{9}{r}+9+9r=39$, so $9r^2-30r+9=0$, i.e. $3r^2-10r+3=0$, $(3r-1)(r-3)=0$. The numbers are **3, 9, 27**.
**4.** $a=12000$, $d=500$. $t_{12}=12000+11\times 500=\text{Rs } 17{,}500$. $S_{12}=\frac{12}{2}[24000+11\times 500]=6\times 29500=\text{Rs } 1{,}77{,}000$.
**5.** $r^5=\frac{96}{3}=32$, so $r=2$. The means are $6, 12, 24, 48$. The GP is $3, 6, 12, 24, 48, 96$ with sum $\frac{3(2^6-1)}{2-1}=189$.
:::


## Retrieval practice and investigation

::: key Work before reading the key
Answer these short retrieval questions without consulting the chapter. Explain the reason, not only the result. These are revision checks, not a prediction of the examination paper.
:::

**1.** The fifth term of 3, 7, 11, … is?

**2.** For 3, 6, 12, … find the fifth term.

**3.** If the common difference is zero, must every term be zero?

::: note Reasoned key
**1.** 19: a₅ = 3 + (5 − 1) × 4. The multiplier is four intervals, not five.

**2.** 48: a₅ = 3 × 2⁴. Adding the ratio instead of multiplying would describe a different sequence.

**3.** No. All terms equal the first term; 5, 5, 5, … is an arithmetic sequence with difference zero.

:::

::: tip Investigation — Build two growth patterns
Write the first six terms of 3, 7, 11, … and 3, 6, 12, …. Plot term number against term. Compare a constant difference with a constant ratio. Predict the tenth term before calculating it.

Submit a one-page record: your method, working or evidence, conclusion, and one limitation. Exchange it with a classmate and check the reasoning against the chapter.
:::
