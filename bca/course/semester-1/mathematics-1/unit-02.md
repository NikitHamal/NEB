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
- Recurrence relations (Hanoi, Fibonacci), convergence tests, telescoping sums and the method of differences.
- Series in computing and finance: loop counts, amortised doubling, annuities and EMI.
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

## 2.6 Recurrence relations: sequences defined by their predecessors

A **recurrence relation** gives each term from earlier ones, together with starting values. Programs are full of them: a `for` loop that updates `total = total * 2 + 1` is a recurrence, and so is the running time of every recursive function. A **closed form** is a formula for $a_{n}$ that needs no earlier term.

**First-order linear recurrence.** For $a_{n+1} = r\, a_{n} + d$ the terms are a GP plus a constant. If $r \ne 1$, look for the fixed value $L = \frac{d}{1 - r}$; then $a_{n} - L$ is a GP with ratio $r$, so $a_{n} = L + (a_{1} - L)\, r^{n-1}$. If $r = 1$ the sequence is an AP with difference $d$.

::: example Worked example: $a_{1} = 3$, $a_{n+1} = 2 a_{n} + 1$
The terms are $3, 7, 15, 31, 63, \dots$. Here $r = 2$, $d = 1$, $L = \frac{1}{1 - 2} = -1$, so $a_{n} = -1 + (3 + 1)\, 2^{n-1} = 2^{n+1} - 1$. Check: $a_{10} = 2^{11} - 1 = 2047$, and running the recurrence nine times from 3 gives the same value.
:::

**Tower of Hanoi.** To move $n$ discs you move $n - 1$ discs aside, move the largest, and move the $n - 1$ back, so $T_{n} = 2 T_{n-1} + 1$ with $T_{1} = 1$. This is the same recurrence with a different start: $T_{n} = 2^{n} - 1$. For 20 discs that is $1{,}048{,}575$ moves; at one move per second the task takes about 12 days.

**Fibonacci sequence.** $F_{1} = F_{2} = 1$ and $F_{n+2} = F_{n+1} + F_{n}$ give $1, 1, 2, 3, 5, 8, 13, 21, 34, 55, \dots$ with $F_{10} = 55$ and $F_{20} = 6765$. The ratio $\frac{F_{n+1}}{F_{n}}$ tends to the golden ratio $\varphi = \frac{1 + \sqrt{5}}{2} \approx 1.618034$ ($\frac{F_{21}}{F_{20}} = 1.618034$). The closed form is **Binet's formula**
$$F_{n} = \frac{\varphi^{n} - \psi^{n}}{\sqrt{5}}, \qquad \psi = \frac{1 - \sqrt{5}}{2}.$$
Since $|\psi| < 1$, $F_{n}$ is the integer nearest to $\frac{\varphi^{n}}{\sqrt{5}}$; for $n = 10$ this is $\frac{122.99}{2.236} = 55.0$. The naive recursive function `fib(n)` makes $2 F_{n} - 1$ calls, so its cost grows like $\varphi^{n}$, a GP, which is why memoisation matters.

## 2.7 Limits of sequences and convergence of series

A sequence $a_{n}$ **converges** to $L$ if $a_{n}$ gets and stays as close to $L$ as we like once $n$ is large; we write $\lim_{n \to \infty} a_{n} = L$. Otherwise it **diverges**. Standard limits:

- $\lim \frac{1}{n} = 0$, and $\lim \frac{n}{n + 1} = \lim \frac{1}{1 + 1/n} = 1$.
- $\lim r^{n} = 0$ if $|r| < 1$, and the terms grow without bound if $r > 1$. The sequence $(-1)^{n}$ oscillates and has no limit.
- $\lim \left( 1 + \frac{1}{n} \right)^{n} = e = 2.71828\dots$ (for $n = 1000$ the value is $2.716924$).
- A sequence that is **bounded and monotone** (always rising or always falling) converges.

An infinite series $\sum a_{k}$ **converges** when its partial sums $S_{n}$ converge. Three facts are used constantly.

1. **Divergence test.** If $a_{k}$ does not tend to 0, the series diverges. The converse is false: $a_{k} \to 0$ does not guarantee convergence.
2. **The harmonic series diverges.** $1 + \frac{1}{2} + \left( \frac{1}{3} + \frac{1}{4} \right) + \left( \frac{1}{5} + \dots + \frac{1}{8} \right) + \dots$: each bracket is at least $\frac{1}{2}$, so $H_{2^{k}} \ge 1 + \frac{k}{2}$ and the sum is unbounded, but very slowly: $H_{10} = 2.929$, $H_{100} = 5.187$, $H_{1000} = 7.485$.
3. **The $p$-series** $\sum \frac{1}{k^{p}}$ converges for $p > 1$ and diverges for $p \le 1$. For $p = 2$ the sum is $\frac{\pi^{2}}{6} = 1.644934$: $S_{10} = 1.549768$ and $S_{100} = 1.634984$.

**Comparison and ratio tests.** If $0 \le a_{k} \le b_{k}$ and $\sum b_{k}$ converges, so does $\sum a_{k}$. For the **ratio test** let $\rho = \lim \left| \frac{a_{k+1}}{a_{k}} \right|$: the series converges if $\rho < 1$, diverges if $\rho > 1$, and the test says nothing if $\rho = 1$.

::: example Worked example: ratio test
$\sum \frac{k}{2^{k}}$: $\frac{a_{k+1}}{a_{k}} = \frac{k + 1}{2 k} \to \frac{1}{2} < 1$, so it converges. Its sum is the arithmetico-geometric series with $x = \frac{1}{2}$, in the form $\frac{1}{2} \cdot \frac{1}{(1 - 1/2)^{2}} = 2$. For $\sum \frac{1}{k!}$: $\frac{a_{k+1}}{a_{k}} = \frac{1}{k + 1} \to 0$, so it converges, to $e = 2.71828\dots$ (the first 20 terms already agree to 12 places).
:::

```svgfig label="2.1" caption="Partial sums S_n for n = 1 to 20. The geometric series 1 + 1/2 + 1/4 + ... settles at 2, the series of 1/k^2 settles at 1.645 (dashed lines), while the harmonic series keeps rising without bound, although slowly."
f = Fig(560, 290)
ax = Axes(f, 60, 20, 450, 220, (0, 21), (0, 6))
ax.grid(5, 1)
ax.axes("", "")
H = 0.0
Z = 0.0
for k in range(1, 21):
    H += 1 / k
    Z += 1 / k ** 2
    ax.pt(k, 2 - 2 * 0.5 ** k, "", r=2.8, color=TEAL)
    ax.pt(k, Z, "", r=2.8, color=AMBER)
    ax.pt(k, H, "", r=2.8, color=RED)
ax.hline(2, color=TEAL)
ax.hline(1.645, color=AMBER)
f.text(520, 262, "n", size=11, color=SLATE, bold=True, anchor="start")
f.text(60, 274, "S_n", size=11, color=SLATE, bold=True, anchor="start")
ax.tag(14, 0.6, "1 + 1/2 + 1/4 + ... (limit 2)", size=10, color=TEAL, bold=True)
ax.tag(14, 2.6, "sum of 1/k^2 (limit 1.645)", size=10, color=AMBER, bold=True)
ax.tag(10, 4.3, "harmonic series (no limit)", size=10.5, color=RED, bold=True)
```

## 2.8 Telescoping sums and the method of differences

Many sums collapse when each term is written as a difference $a_{k} = b_{k} - b_{k+1}$: then $\sum_{k=1}^{n} a_{k} = b_{1} - b_{n+1}$, because every middle term cancels. Partial fractions are the usual way to create the difference.

$$\frac{1}{k (k + 1)} = \frac{1}{k} - \frac{1}{k + 1} \quad \Rightarrow \quad \sum_{k=1}^{n} \frac{1}{k (k + 1)} = 1 - \frac{1}{n + 1} = \frac{n}{n + 1}.$$
For $n = 99$ the sum is exactly $\frac{99}{100}$, and as $n \to \infty$ the infinite series converges to 1.

::: example Worked example: $\sum \frac{1}{k (k + 2)}$
$\frac{1}{k (k + 2)} = \frac{1}{2} \left( \frac{1}{k} - \frac{1}{k + 2} \right)$. Writing out the terms, only $1$ and $\frac{1}{2}$ survive at the start and $\frac{1}{n + 1}$, $\frac{1}{n + 2}$ at the end:
$$S_{n} = \frac{1}{2} \left( 1 + \frac{1}{2} - \frac{1}{n + 1} - \frac{1}{n + 2} \right) = \frac{3}{4} - \frac{1}{2} \left( \frac{1}{n + 1} + \frac{1}{n + 2} \right).$$
For $n = 10$: $\frac{3}{4} - \frac{1}{2} \left( \frac{1}{11} + \frac{1}{12} \right) = 0.6629$, and $S_{\infty} = \frac{3}{4}$.
:::

Two more patterns: rationalising, $\frac{1}{\sqrt{k} + \sqrt{k + 1}} = \sqrt{k + 1} - \sqrt{k}$, so $\sum_{k=1}^{99} \frac{1}{\sqrt{k} + \sqrt{k + 1}} = \sqrt{100} - 1 = 9$; and products of consecutive integers, using $k (k + 1) = \frac{k (k + 1) (k + 2) - (k - 1) k (k + 1)}{3}$, which gives
$$\sum_{k=1}^{n} k (k + 1) = \frac{n (n + 1) (n + 2)}{3}, \qquad \text{for } n = 10: \ \frac{10 \cdot 11 \cdot 12}{3} = 440.$$

**Method of differences for a polynomial sequence.** If the first differences of a sequence are not constant but the second differences are, then $a_{n}$ is a quadratic in $n$. Take $2, 5, 10, 17, 26, \dots$: first differences $3, 5, 7, 9$, second differences all 2. Write $a_{n} = A n^{2} + B n + C$ with $2 A = 2$, so $A = 1$; then $a_{1} = 2$ and $a_{2} = 5$ give $B = 0$, $C = 1$, and $a_{n} = n^{2} + 1$. Its sum is
$$\sum_{k=1}^{n} (k^{2} + 1) = \frac{n (n + 1) (2 n + 1)}{6} + n, \qquad \text{for } n = 10: \ 385 + 10 = 395.$$
For $3, 7, 13, 21, 31, \dots$ the second differences are 2 again and $a_{n} = n^{2} + n + 1$.

**Binomial sums.** Putting $x = 1$ in $(1 + x)^{n} = \sum \binom{n}{k} x^{k}$ gives $\sum_{k=0}^{n} \binom{n}{k} = 2^{n}$: a set of $n$ elements has $2^{n}$ subsets, and $n$ bits have $2^{n}$ patterns. For $n = 8$ the coefficients $1, 8, 28, 56, 70, 56, 28, 8, 1$ add to 256.

## 2.9 Series in computing and finance

**Loop counting.** The inner statement of `for i in 1..n: for j in i+1..n` runs $\sum_{i=1}^{n} (n - i) = \frac{n (n - 1)}{2}$ times; for $n = 8$ that is 28 pairs. Because $\frac{n (n - 1)}{2}$ grows like $n^{2}$, such an algorithm is called quadratic. A loop that halves its range each time stops after $\lceil \log_{2} n \rceil$ rounds: searching one million sorted records takes at most 20 comparisons.

**Amortised doubling.** A dynamic array that doubles its capacity when full copies $1 + 2 + 4 + \dots + 2^{9} = 2^{10} - 1 = 1023$ elements in total while 1024 elements are appended. The total copying work is less than the number of insertions, so each append costs a constant on average.

**Compound interest and depreciation** are GPs. A balance $P$ at rate $i$ per period is worth $P (1 + i)^{n}$ after $n$ periods. A machine bought for Rs 80,000 that loses 15 percent of its value each year is worth $80000 \times 0.85^{4} = \text{Rs } 41{,}760.50$ after four years.

**Regular savings (annuity).** Depositing $R$ at the end of each period, the future value is the GP sum
$$FV = R\, \frac{(1 + i)^{n} - 1}{i}.$$
Rs 1,000 a month for 12 months at 1 percent a month gives $1000 \times \frac{1.01^{12} - 1}{0.01} = \text{Rs } 12{,}682.50$.

**Loan instalment (EMI).** For a loan $P$ at rate $i$ per month repaid in $n$ equal instalments, the present values of the instalments form a GP that equals $P$, which gives
$$\text{EMI} = \frac{P\, i\, (1 + i)^{n}}{(1 + i)^{n} - 1}.$$
::: example Worked example: loan of Rs 500,000
Rate 12 percent a year is $i = 1$ percent a month, repaid over 5 years ($n = 60$). $(1.01)^{60} = 1.8167$, so EMI $= \frac{500000 \times 0.01 \times 1.8167}{0.8167} = \text{Rs } 11{,}122.22$. Total paid $= 60 \times 11122.22 = \text{Rs } 667{,}333$, so the interest is about Rs 167,333.
:::

**Repeating decimals** are infinite GPs: $0.\overline{45} = \frac{0.45}{1 - 0.01} = \frac{45}{99} = \frac{5}{11}$.

## Formula and fact sheet

- AP: $a_{n} = a + (n - 1) d$; $S_{n} = \frac{n}{2} [2 a + (n - 1) d]$. GP: $a_{n} = a r^{n-1}$; $S_{n} = \frac{a (r^{n} - 1)}{r - 1}$; $S_{\infty} = \frac{a}{1 - r}$.
- $\mathrm{AM} \ge \mathrm{GM} \ge \mathrm{HM}$, $\mathrm{GM}^{2} = \mathrm{AM} \cdot \mathrm{HM}$ (two numbers).
- Recurrence $a_{n+1} = r a_{n} + d$: $a_{n} = L + (a_{1} - L) r^{n-1}$, $L = \frac{d}{1 - r}$. Hanoi $T_{n} = 2^{n} - 1$. Fibonacci ratio $\to \varphi = 1.618$.
- Series: harmonic diverges; $\sum \frac{1}{k^{p}}$ converges iff $p > 1$; ratio test $\rho < 1$. Telescoping: $\sum (b_{k} - b_{k+1}) = b_{1} - b_{n+1}$.
- Finance: $FV = R \frac{(1 + i)^{n} - 1}{i}$, $\text{EMI} = \frac{P i (1 + i)^{n}}{(1 + i)^{n} - 1}$.
- $\sum k = \frac{n (n + 1)}{2}$, $\sum k^{2} = \frac{n (n + 1) (2 n + 1)}{6}$, $\sum k^{3} = (\sum k)^{2}$.

## Chapter summary

- An AP has a constant difference, a GP a constant ratio and an HP has reciprocals in AP.
- The infinite GP sum exists only for $|r| < 1$.
- The means obey $\mathrm{AM} \ge \mathrm{GM} \ge \mathrm{HM}$, and the sums of $k$, $k^{2}$, $k^{3}$ are standard tools for counting loop iterations.
- A recurrence is solved by finding its fixed value; telescoping and second differences turn awkward sums into closed forms; EMI and annuities are GP sums.

## Practice

1. Find $S_{20}$ of the AP $5, 8, 11, \dots$.
2. The 3rd term of an AP is 11 and the 8th is 26. Find $a$, $d$ and the 15th term.
3. Find the sum of the first 7 terms of $3, 6, 12, \dots$ and the sum to infinity of $9, 3, 1, \dots$.
4. Insert three geometric means between 2 and 32.
5. Prove that for $a, b > 0$, $a + b \ge 2 \sqrt{a b}$, and find the HM of 6 and 12.
6. Find $1^{2} + 2^{2} + \dots + 15^{2}$.
7. Sum $1 + 3 x + 5 x^{2} + \dots$ for $|x| < 1$ in closed form.
8. The 4th term of an HP is $\frac{1}{7}$ and the 7th is $\frac{1}{13}$. Find the 10th term.
9. Find $a_{n}$ in closed form for $a_{1} = 5$, $a_{n+1} = 3 a_{n} - 2$ and evaluate $a_{6}$.
10. How many moves does the Tower of Hanoi need for 10 discs? Use $T_{n} = 2 T_{n-1} + 1$ to show $T_{n} = 2^{n} - 1$.
11. Use Binet's formula to find $F_{12}$, and check with the recurrence.
12. Test the series $\sum \frac{3^{k}}{k!}$ for convergence with the ratio test.
13. Show that $\sum_{k=1}^{n} \frac{1}{k (k + 1) (k + 2)} = \frac{1}{4} - \frac{1}{2 (n + 1) (n + 2)}$ and find the infinite sum.
14. Find the $n$th term and the sum of $n$ terms of $4, 10, 18, 28, 40, \dots$ (use second differences).
15. Find $\sum_{k=1}^{20} \frac{1}{\sqrt{k + 1} + \sqrt{k}}$ (give the exact form first, then a decimal).
16. A dynamic array starts at capacity 1 and doubles when full. How many element copies happen while 2048 elements are appended one by one?
17. Rs 2,000 is deposited at the end of every month for 24 months at 1 percent a month. Find the future value.
18. A phone costing Rs 60,000 loses 20 percent of its value each year. After how many whole years is it worth less than Rs 25,000?
19. Find the EMI for a loan of Rs 300,000 at 12 percent a year (1 percent a month) over 36 months.
20. Does $\sum \frac{1}{\sqrt{k}}$ converge? Does $\sum \frac{1}{k^{3/2}}$? Give the reason in each case.

::: note Answers and worked solutions
**1.** $a = 5$, $d = 3$: $S_{20} = 10 (10 + 57) = $ **670**.

**2.** $a + 2 d = 11$, $a + 7 d = 26 \Rightarrow 5 d = 15$, $d = 3$, $a = 5$. $a_{15} = 5 + 14 \cdot 3 = $ **47**.

**3.** $S_{7} = 3 (2^{7} - 1) = $ **381**. $r = \frac{1}{3}$: $S_{\infty} = \frac{9}{2/3} = $ **13.5**.

**4.** $r^{4} = 16$, $r = 2$: **4, 8, 16** (the means between 2 and 32).

**5.** $(\sqrt{a} - \sqrt{b})^{2} \ge 0$ gives $a + b \ge 2 \sqrt{a b}$. $\mathrm{HM} = \frac{2 \cdot 72}{18} = $ **8**.

**6.** $\frac{15 \cdot 16 \cdot 31}{6} = $ **1240**.

**7.** $S - x S = 1 + 2 x + 2 x^{2} + \dots = 1 + \frac{2 x}{1 - x} = \frac{1 + x}{1 - x}$, so **$S = \frac{1 + x}{(1 - x)^{2}}$**.

**8.** Reciprocals are an AP: $7$ and $13$ are the 4th and 7th terms, so $3 d = 6$, $d = 2$; the 10th is $13 + 6 = 19$, so the term is **$\frac{1}{19}$**.

**9.** Fixed value $L = \frac{-2}{1 - 3} = 1$, so $a_{n} - 1 = (5 - 1) 3^{n-1}$ and **$a_{n} = 1 + 4 \cdot 3^{n-1}$**. $a_{6} = 1 + 4 \cdot 243 = $ **973** (the recurrence gives $5, 13, 37, 109, 325, 973$).

**10.** $T_{10} = 2^{10} - 1 = $ **1023**. Proof: $T_{n} + 1 = 2 (T_{n-1} + 1)$, so $T_{n} + 1$ is a GP with ratio 2 starting at $T_{1} + 1 = 2$, giving $T_{n} + 1 = 2^{n}$.

**11.** $\varphi^{12} = 321.997$, $\frac{321.997}{2.236068} = 144.0$, so **$F_{12} = 144$**. Recurrence: $55 + 89 = 144$.

**12.** $\frac{a_{k+1}}{a_{k}} = \frac{3^{k+1} / (k + 1)!}{3^{k} / k!} = \frac{3}{k + 1} \to 0 < 1$: **converges** (the sum is $e^{3} - 1$).

**13.** $\frac{1}{k (k + 1) (k + 2)} = \frac{1}{2} \left[ \frac{1}{k (k + 1)} - \frac{1}{(k + 1) (k + 2)} \right]$, which telescopes to $\frac{1}{2} \left[ \frac{1}{2} - \frac{1}{(n + 1) (n + 2)} \right]$. As $n \to \infty$ the sum is **$\frac{1}{4}$**.

**14.** First differences $6, 8, 10, 12$, second differences 2, so $A = 1$. $a_{1} = 4$, $a_{2} = 10$: $1 + B + C = 4$, $4 + 2 B + C = 10$, so $B = 3$, $C = 0$ and **$a_{n} = n^{2} + 3 n$** (check $a_{5} = 40$). $S_{n} = \frac{n (n + 1) (2 n + 1)}{6} + \frac{3 n (n + 1)}{2} = \frac{n (n + 1) (n + 5)}{3}$.

**15.** $\frac{1}{\sqrt{k + 1} + \sqrt{k}} = \sqrt{k + 1} - \sqrt{k}$, so the sum is $\sqrt{21} - 1 = $ **3.583**.

**16.** Copies happen at sizes $1, 2, 4, \dots, 1024$ (when the array holds 1, 2, ..., 1024 and the next element arrives), so the total is $2^{11} - 1 = $ **2047** copies, fewer than the 2048 appends.

**17.** $FV = 2000 \times \frac{1.01^{24} - 1}{0.01} = 2000 \times 26.9735 = $ **Rs 53,947** (to the nearest rupee).

**18.** Value after $t$ years $= 60000 \times 0.8^{t}$. $t = 4$: 24,576 (below 25,000); $t = 3$: 30,720. So after **4 years**.

**19.** $1.01^{36} = 1.43077$, EMI $= \frac{300000 \times 0.01 \times 1.43077}{0.43077} = $ **Rs 9,964.29**.

**20.** $\sum \frac{1}{\sqrt{k}} = \sum \frac{1}{k^{1/2}}$ is a $p$-series with $p = \frac{1}{2} \le 1$: **diverges**. $\sum \frac{1}{k^{3/2}}$ has $p = \frac{3}{2} > 1$: **converges**.
:::
