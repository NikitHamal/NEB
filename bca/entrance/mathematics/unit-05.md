---
subject: Mathematics
grade: BCA
unit: 5
title: Sequences and Series
hours: 2
area: Algebra
---

Two questions a year come from sequences, and the Dean's Office model had a seven-day "1 paisa, 2 paisa, 4 paisa" savings problem. The question is almost always one of five things: the $n$th term of an AP or GP, a sum, an AM or GM, a "which term is", or a sum to infinity. Memorise the formulas below and each takes under a minute.

::: key What the paper asks from this chapter
- **AP**: $a_n=a+(n-1)d$, $S_n=\frac{n}{2}[2a+(n-1)d]$, three numbers in AP, insert means.
- **GP**: $a_n=ar^{n-1}$, $S_n=\frac{a(r^n-1)}{r-1}$, $S_\infty=\frac{a}{1-r}$.
- **Special sums**: $\sum n$, $\sum n^2$, $\sum n^3$, odd and even numbers.
- **Means**: $AM=\frac{a+b}{2}$, $GM=\sqrt{ab}$, and $AM\ge GM$.
:::

## 5.1 Arithmetic progression

- $a_n=a+(n-1)d$; number of terms $n=\frac{l-a}{d}+1$.
- $S_n=\frac{n}{2}[2a+(n-1)d]=\frac{n}{2}(a+l)$.
- $a,b,c$ in AP $\iff 2b=a+c$. For three numbers in AP write $a-d,a,a+d$ (sum $=3a$).
- To insert $m$ means between $a$ and $b$: $d=\frac{b-a}{m+1}$.
- If $S_n$ is given, $a_n=S_n-S_{n-1}$ and $a_1=S_1$.

## 5.2 Geometric progression

- $a_n=ar^{n-1}$, $r=\frac{a_2}{a_1}$. $S_n=\frac{a(r^n-1)}{r-1}$ for $r\ne1$; for $|r|<1$, $S_\infty=\frac{a}{1-r}$.
- $a,b,c$ in GP $\iff b^2=ac$. Three numbers in GP: $\frac{a}{r},a,ar$ (product $=a^3$).
- Recurring decimal: $0.\overline{6}=\frac{0.6}{1-0.1}=\frac{2}{3}$.
- **Harmonic progression**: the reciprocals of its terms form an AP.

## 5.3 Special sums and mixed problems

| Sum | Value |
|---|---|
| $1+2+\dots+n$ | $\frac{n(n+1)}{2}$ |
| $1+3+5+\dots$ ($n$ odd numbers) | $n^2$ |
| $2+4+\dots+2n$ | $n(n+1)$ |
| $1^2+2^2+\dots+n^2$ | $\frac{n(n+1)(2n+1)}{6}$ |
| $1^3+2^3+\dots+n^3$ | $\left[\frac{n(n+1)}{2}\right]^2$ |

::: example Doubling savings
**Problem.** You save 1 paisa on day 1, 2 on day 2, 4 on day 3, and so on. Total for a week?

**Solution.** GP with $a=1$, $r=2$, $n=7$: $S=\frac{2^7-1}{2-1}=127$ paisa.
:::

## Formula and fact sheet

| Item | AP | GP |
|---|---|---|
| $n$th term | $a+(n-1)d$ | $ar^{n-1}$ |
| Sum | $\frac{n}{2}[2a+(n-1)d]$ | $\frac{a(r^n-1)}{r-1}$ |
| Condition | $2b=a+c$ | $b^2=ac$ |
| Mean | $\frac{a+b}{2}$ | $\sqrt{ab}$ |

## Chapter summary

- Count terms first: $n=\frac{l-a}{d}+1$.
- $S_n$ for AP is $n$ times the average of first and last.
- Use $\frac{a}{r},a,ar$ for three GP numbers and $a-d,a,a+d$ for AP.
- $S_\infty$ exists only when $|r|<1$.
- $a_n=S_n-S_{n-1}$ recovers terms from sums.
- $AM\ge GM$, with equality only when the numbers are equal.

## Practice questions

**Set A — Recall (20 questions)**

1. The 10th term of the AP 2, 5, 8, … is
   (a) 27 (b) 30 (c) 32 (d) 29
2. The sum of the first 20 natural numbers is
   (a) 210 (b) 200 (c) 420 (d) 190
3. The 5th term of the GP 3, 6, 12, … is
   (a) 24 (b) 96 (c) 48 (d) 45
4. The arithmetic mean of 4 and 16 is
   (a) 8 (b) 10 (c) 12 (d) 20
5. The geometric mean of 4 and 16 is
   (a) 10 (b) 12 (c) 6 (d) 8
6. The sum $1+2+4+8+16+32+64$ is
   (a) 64 (b) 128 (c) 127 (d) 126
7. The sum of the first $n$ odd numbers is
   (a) $n^2$ (b) $n(n+1)$ (c) $\frac{n(n+1)}{2}$ (d) $2n$
8. The sum to infinity of $1+\frac{1}{2}+\frac{1}{4}+\cdots$ is
   (a) 1 (b) 2 (c) $\frac{3}{2}$ (d) infinite
9. If $a,b,c$ are in AP, then
   (a) $b^2=ac$ (b) $b=a+c$ (c) $2b=a+c$ (d) $b=ac$
10. The common ratio of 2, $-6$, 18, … is
    (a) 3 (b) $-2$ (c) 4 (d) $-3$
11. The sum of the first 10 even natural numbers is
    (a) 100 (b) 110 (c) 55 (d) 120
12. $1^3+2^3+3^3$ equals
    (a) 36 (b) 14 (c) 6 (d) 27
13. The common difference of 7, 4, 1, … is
    (a) 3 (b) 11 (c) $-4$ (d) $-3$
14. $1^2+2^2+3^2+4^2+5^2$ equals
    (a) 15 (b) 225 (c) 55 (d) 50
15. In a harmonic progression the reciprocals of the terms form
    (a) an AP (b) a GP (c) an HP (d) a constant sequence
16. The number of terms in the AP 5, 9, 13, …, 41 is
    (a) 9 (b) 10 (c) 11 (d) 12
17. The 3rd term of the GP with first term 2 and ratio 3 is
    (a) 12 (b) 9 (c) 18 (d) 54
18. The sum of the first $n$ natural numbers is
    (a) $n^2$ (b) $n(n+1)$ (c) $\frac{n(n-1)}{2}$ (d) $\frac{n(n+1)}{2}$
19. The sum to infinity of the GP 3, 1, $\frac{1}{3}$, … is
    (a) $\frac{9}{2}$ (b) 4 (c) 6 (d) 9
20. Which of the following is a GP?
    (a) 1, 3, 5, 7 (b) 3, 9, 27, 81 (c) 2, 4, 6, 8 (d) 1, 4, 9, 16

::: note Answers and explanations — Set A
**1.** (d) — 2 + 9 × 3 = 29.
**2.** (a) — 20 × 21 / 2 = 210.
**3.** (c) — 3 × 2⁴ = 48.
**4.** (b) — (4 + 16)/2 = 10.
**5.** (d) — √(4 × 16) = 8; GM is below AM.
**6.** (c) — (2⁷ − 1)/(2 − 1) = 127.
**7.** (a) — 1 + 3 + 5 + … = n².
**8.** (b) — a/(1 − r) = 1/(1/2) = 2.
**9.** (c) — the middle term is the average of its neighbours; (a) is for a GP.
**10.** (d) — 18 / (−6) = −3.
**11.** (b) — n(n + 1) = 10 × 11 = 110.
**12.** (a) — 1 + 8 + 27 = 36 = (1 + 2 + 3)².
**13.** (d) — 4 − 7 = −3.
**14.** (c) — 5 × 6 × 11 / 6 = 55.
**15.** (a) — that is the definition of an HP.
**16.** (b) — (41 − 5)/4 + 1 = 10.
**17.** (c) — 2 × 3² = 18.
**18.** (d) — n(n + 1)/2; (b) is the sum of even numbers.
**19.** (a) — 3 / (1 − 1/3) = 9/2.
**20.** (b) — constant ratio 3.
:::

**Set B — Understanding (12 questions)**

1. The sum of the first 10 terms of the AP 3, 7, 11, … is
   (a) 200 (b) 210 (c) 220 (d) 190
2. Which term of the AP 3, 8, 13, … is 78?
   (a) 14th (b) 15th (c) 17th (d) 16th
3. Three numbers in AP have sum 27. The middle number is
   (a) 9 (b) 8 (c) 10 (d) 12
4. Three numbers in GP have product 216. The middle number is
   (a) 8 (b) 12 (c) 6 (d) 9
5. A GP has first term 5 and fifth term 80, with positive ratio. The ratio is
   (a) 3 (b) 2 (c) 4 (d) 16
6. The sum $1+3+9+27+81+243$ is
   (a) 364 (b) 243 (c) 363 (d) 729
7. The first term of an AP is 3 and the sum of its first 5 terms is 35. The common difference is
   (a) 4 (b) 3 (c) 1 (d) 2
8. The sum of all multiples of 3 between 1 and 50 is
   (a) 400 (b) 425 (c) 408 (d) 416
9. The sum $2+4+6+\cdots+100$ is
   (a) 2,550 (b) 5,050 (c) 2,500 (d) 5,100
10. The sum to infinity of $0.6+0.06+0.006+\cdots$ is
    (a) 0.6 (b) 0.7 (c) 1 (d) $\frac{2}{3}$
11. For what $n$ is $1+2+\cdots+n=55$?
    (a) 9 (b) 11 (c) 10 (d) 12
12. If three arithmetic means are inserted between 4 and 20, the second mean is
    (a) 10 (b) 12 (c) 14 (d) 16

::: note Answers and explanations — Set B
**1.** (b) — 5(6 + 36) = 210.
**2.** (d) — 3 + (n − 1)5 = 78 gives n = 16.
**3.** (a) — sum = 3 × middle, so 27/3 = 9.
**4.** (c) — (a/r)(a)(ar) = a³ = 216, a = 6.
**5.** (b) — r⁴ = 16, so r = 2.
**6.** (a) — (3⁶ − 1)/2 = 364.
**7.** (d) — (5/2)(6 + 4d) = 35 gives d = 2.
**8.** (c) — 3, 6, …, 48 is 16 terms; 16(3 + 48)/2 = 408.
**9.** (a) — 50 × 51 = 2,550; 5,050 is the sum of 1 to 100.
**10.** (d) — 0.6/(1 − 0.1) = 2/3.
**11.** (c) — 10 × 11/2 = 55.
**12.** (b) — d = 16/4 = 4, so the means are 8, 12, 16.
:::

**Set C — Application (8 questions)**

1. A man saves Rs 100 in the first month and Rs 20 more each month than the month before. His total saving in 12 months is
   (a) Rs 2,400 (b) Rs 2,640 (c) Rs 2,520 (d) Rs 2,280
2. If the sum of the first $n$ terms of an AP is $3n^2+2n$, its common difference is
   (a) 6 (b) 5 (c) 3 (d) 11
3. A GP has first term 1 and common ratio 3. Its 5th term is
   (a) 27 (b) 64 (c) 243 (d) 81
4. Three numbers in GP have sum 14 and product 64. The largest is
   (a) 6 (b) 8 (c) 10 (d) 12
5. The sum $1^2+2^2+\cdots+10^2$ is
   (a) 3,025 (b) 55 (c) 385 (d) 100
6. The sum $1^3+2^3+\cdots+10^3$ is
   (a) 385 (b) 55 (c) 2,025 (d) 3,025
7. The sum of the AP 25, 22, 19, …, 1 is
   (a) 117 (b) 126 (c) 108 (d) 130
8. If $x$, $x+2$, $x+8$ are in GP, then $x$ is
   (a) 2 (b) 1 (c) 4 (d) 3

::: note Answers and explanations — Set C
**1.** (c) — (12/2)(200 + 11 × 20) = 6 × 420 = 2,520.
**2.** (a) — a₁ = 5, a₂ = 16 − 5 = 11, so d = 6.
**3.** (d) — 1 × 3⁴ = 81; (c) is the 6th term.
**4.** (b) — numbers 2, 4, 8: sum 14, product 64.
**5.** (c) — 10 × 11 × 21 / 6 = 385.
**6.** (d) — (55)² = 3,025.
**7.** (a) — 9 terms; 9 × (25 + 1)/2 = 117.
**8.** (b) — (x + 2)² = x(x + 8) gives 4x + 4 = 8x, x = 1.
:::
