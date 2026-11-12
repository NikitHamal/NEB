---
subject: Mathematics I
grade: BCA Semester 1
unit: 2
title: Sequence and Series
area: BCA 104 · Mathematics I · Unit 2
---

A **sequence** is an ordered list of numbers; a **series** is the sum of its terms. They describe loop counts, running totals, compound interest, recursion and the cost of algorithms, so this unit is the mathematical language of "how does this grow?".

::: key What this unit gives you
- Arithmetic, geometric and harmonic sequences, their $n$th terms and sums.
- Finite and infinite geometric series, with the condition $|r| < 1$.
- The means AM, GM, HM and the inequality $\mathrm{AM} \ge \mathrm{GM} \ge \mathrm{HM}$.
- The sums $\sum n$, $\sum n^{2}$, $\sum n^{3}$ and the arithmetico-geometric series.
:::

## 2.1 Sequences and series

A sequence is a function from the natural numbers: $a_{1}, a_{2}, a_{3}, \dots$ with general term $a_{n}$. The series $S_{n} = a_{1} + a_{2} + \dots + a_{n}$ is the $n$th **partial sum**, and $a_{n} = S_{n} - S_{n-1}$. A sequence may be given by a formula ($a_{n} = n^{2}$) or by recursion ($a_{1} = 1$, $a_{n+1} = 2 a_{n}$).

## 2.2 Arithmetic progression (AP)

Each term exceeds the previous by a fixed **common difference** $d$.
$$a_{n} = a + (n - 1) d, \qquad S_{n} = \frac{n}{2} \left[ 2 a + (n - 1) d \right] = \frac{n}{2} (a + l),$$
where $l$ is the last term. Three numbers in AP can be written $a - d,\ a,\ a + d$. The middle term is the average of its neighbours.

::: example Worked example: AP
First term 3, common difference 4. Then $a_{10} = 3 + 9 \cdot 4 = 39$ and $S_{10} = \frac{10}{2} (3 + 39) = 210$. Which term equals 91? $3 + (n - 1) 4 = 91 \Rightarrow n = 23$.
:::

## 2.3 Geometric progression (GP)

Each term is the previous times a fixed **common ratio** $r$.
$$a_{n} = a r^{n-1}, \qquad S_{n} = \frac{a (r^{n} - 1)}{r - 1} \ (r \ne 1), \qquad S_{\infty} = \frac{a}{1 - r} \ (|r| < 1).$$
If $|r| \ge 1$ the infinite series does not converge to a finite sum.

::: example Worked example: GP
$a = 2$, $r = 3$: $S_{6} = \frac{2 (3^{6} - 1)}{2} = 728$. The series $8 + 4 + 2 + 1 + \dots$ has $r = \frac{1}{2}$ and $S_{\infty} = \frac{8}{1 - 1/2} = 16$. The recurring decimal $0.\overline{36} = \frac{36}{100} + \frac{36}{10000} + \dots = \frac{0.36}{1 - 0.01} = \frac{4}{11}$.
:::

**Computing link.** Binary halving search takes about $\log_{2} n$ steps; a loop that doubles its step has a GP of costs, and the total $1 + 2 + 4 + \dots + 2^{k} = 2^{k+1} - 1$ is the largest number storable in $k + 1$ bits.

## 2.4 Harmonic progression and the means

A sequence is a **harmonic progression (HP)** if the reciprocals of its terms are in AP: $\frac{1}{a}, \frac{1}{a+d}, \dots$. There is no simple sum formula, so questions on HP are solved by taking reciprocals.

For positive numbers $a$ and $b$:
$$\mathrm{AM} = \frac{a + b}{2}, \quad \mathrm{GM} = \sqrt{a b}, \quad \mathrm{HM} = \frac{2 a b}{a + b}, \qquad \mathrm{AM} \ge \mathrm{GM} \ge \mathrm{HM}, \quad \mathrm{GM}^{2} = \mathrm{AM} \cdot \mathrm{HM}.$$
Equality holds only when $a = b$. *Proof of AM $\ge$ GM:* $\frac{a + b}{2} - \sqrt{a b} = \frac{(\sqrt{a} - \sqrt{b})^{2}}{2} \ge 0$.

::: example Worked example: means of 4 and 9
$\mathrm{AM} = 6.5$, $\mathrm{GM} = 6$, $\mathrm{HM} = \frac{2 \cdot 36}{13} = 5.538$. Order $6.5 > 6 > 5.538$ and $6^{2} = 36 = 6.5 \times 5.538$. To insert $n$ arithmetic means between $a$ and $b$ use $d = \frac{b - a}{n + 1}$: two means between 3 and 12 are 6 and 9.
:::

## 2.5 Special sums and the arithmetico-geometric series

$$\sum_{k=1}^{n} k = \frac{n (n + 1)}{2}, \qquad \sum_{k=1}^{n} k^{2} = \frac{n (n + 1) (2 n + 1)}{6}, \qquad \sum_{k=1}^{n} k^{3} = \left[ \frac{n (n + 1)}{2} \right]^{2}.$$
For $n = 10$: $55$, $385$ and $3025$ ($= 55^{2}$). The first sum is the number of steps of the nested loop `for i in 1..n: for j in 1..i`; the second counts operations in some triple loops.

An **arithmetico-geometric series** has terms that are the product of an AP term and a GP term, $a b, (a + d) b r, (a + 2 d) b r^{2}, \dots$. Method: multiply $S$ by $r$, subtract, and sum the resulting GP. For $S = 1 + 2 x + 3 x^{2} + \dots$ ($|x| < 1$): $S - x S = 1 + x + x^{2} + \dots = \frac{1}{1 - x}$, so $S = \frac{1}{(1 - x)^{2}}$.

::: example Worked example: arithmetico-geometric series
$1 + \frac{2}{3} + \frac{3}{9} + \frac{4}{27} + \dots$ is $S$ with $x = \frac{1}{3}$, so $S = \frac{1}{(2/3)^{2}} = \frac{9}{4}$. A loan question: if Rs 1,000 grows by 10 percent a year, the value after 5 years is the GP term $1000 (1.1)^{5} = \mathrm{Rs}\ 1610.51$.
:::

**Sigma notation rules.** $\sum (a_{k} + b_{k}) = \sum a_{k} + \sum b_{k}$ and $\sum c\, a_{k} = c \sum a_{k}$. Use them with the special sums to evaluate $\sum_{k=1}^{n} (2 k^{2} + 3 k)$: $\frac{n (n + 1) (2 n + 1)}{3} + \frac{3 n (n + 1)}{2}$.

## Formula and fact sheet

- AP: $a_{n} = a + (n - 1) d$; $S_{n} = \frac{n}{2} [2 a + (n - 1) d]$. GP: $a_{n} = a r^{n-1}$; $S_{n} = \frac{a (r^{n} - 1)}{r - 1}$; $S_{\infty} = \frac{a}{1 - r}$.
- $\mathrm{AM} \ge \mathrm{GM} \ge \mathrm{HM}$, $\mathrm{GM}^{2} = \mathrm{AM} \cdot \mathrm{HM}$ (two numbers).
- $\sum k = \frac{n (n + 1)}{2}$, $\sum k^{2} = \frac{n (n + 1) (2 n + 1)}{6}$, $\sum k^{3} = (\sum k)^{2}$.

## Chapter summary

- An AP has a constant difference, a GP a constant ratio and an HP has reciprocals in AP.
- The infinite GP sum exists only for $|r| < 1$.
- The means obey $\mathrm{AM} \ge \mathrm{GM} \ge \mathrm{HM}$, and the sums of $k$, $k^{2}$, $k^{3}$ are standard tools for counting loop iterations.

## Practice

1. Find $S_{20}$ of the AP $5, 8, 11, \dots$.
2. The 3rd term of an AP is 11 and the 8th is 26. Find $a$, $d$ and the 15th term.
3. Find the sum of the first 7 terms of $3, 6, 12, \dots$ and the sum to infinity of $9, 3, 1, \dots$.
4. Insert three geometric means between 2 and 32.
5. Prove that for $a, b > 0$, $a + b \ge 2 \sqrt{a b}$, and find the HM of 6 and 12.
6. Find $1^{2} + 2^{2} + \dots + 15^{2}$.
7. Sum $1 + 3 x + 5 x^{2} + \dots$ for $|x| < 1$ in closed form.
8. The 4th term of an HP is $\frac{1}{7}$ and the 7th is $\frac{1}{13}$. Find the 10th term.

::: note Answers and worked solutions
**1.** $a = 5$, $d = 3$: $S_{20} = 10 (10 + 57) = $ **670**.

**2.** $a + 2 d = 11$, $a + 7 d = 26 \Rightarrow 5 d = 15$, $d = 3$, $a = 5$. $a_{15} = 5 + 14 \cdot 3 = $ **47**.

**3.** $S_{7} = 3 (2^{7} - 1) = $ **381**. $r = \frac{1}{3}$: $S_{\infty} = \frac{9}{2/3} = $ **13.5**.

**4.** $r^{4} = 16$, $r = 2$: **4, 8, 16** (the means between 2 and 32).

**5.** $(\sqrt{a} - \sqrt{b})^{2} \ge 0$ gives $a + b \ge 2 \sqrt{a b}$. $\mathrm{HM} = \frac{2 \cdot 72}{18} = $ **8**.

**6.** $\frac{15 \cdot 16 \cdot 31}{6} = $ **1240**.

**7.** $S - x S = 1 + 2 x + 2 x^{2} + \dots = 1 + \frac{2 x}{1 - x} = \frac{1 + x}{1 - x}$, so **$S = \frac{1 + x}{(1 - x)^{2}}$**.

**8.** Reciprocals are an AP: $7$ and $13$ are the 4th and 7th terms, so $3 d = 6$, $d = 2$; the 10th is $13 + 6 = 19$, so the term is **$\frac{1}{19}$**.
:::
