---
subject: Mathematics
grade: BCA
unit: 1
title: Numbers, HCF and LCM, Ratio, Percentage and Average
hours: 5
area: Arithmetic
---

Arithmetic is the cheapest part of the BCA paper to score in. About 8–10 of the 50 mathematics questions are pure arithmetic, and this chapter covers the half of it that the paper asks most often: number properties, HCF and LCM, ratio, percentage and average. None of it needs more than Class 8 mathematics. What the paper tests is speed. A student who knows the fraction–percentage table and the few shortcuts below answers each question in under 40 seconds, and that saved time pays for the harder coordinate-geometry and calculus questions later in the paper.

::: key What the paper asks from this chapter
- **Number properties**: divisibility tests, primes, even/odd results, remainders. The Dean's Office model asks "which expression is always even" and "sum of first five primes".
- **HCF and LCM**: the product rule $\text{HCF}\times\text{LCM}=a\times b$, and the three word-problem types (greatest divisor, least multiple, bells together).
- **Ratio and proportion**: dividing a quantity, chaining ratios ($a:b$ and $b:c$), and age problems.
- **Percentage**: successive change $a+b+\frac{ab}{100}$, and "percent more / percent less" (always on the base).
- **Average**: replacing a member, adding a group, weighted mean.
:::

## 1.1 Integers, primes, divisibility, remainders, even and odd results

**Divisibility tests.**

| By | Test |
|---|---|
| 2, 5, 10 | last digit even; 0 or 5; 0 |
| 3, 9 | digit sum divisible by 3, 9 |
| 4, 8 | last two, last three digits divisible by 4, 8 |
| 6 | divisible by both 2 and 3 |
| 11 | (sum of odd-place digits) − (sum of even-place digits) is 0 or a multiple of 11 |

**Primes.** A prime has exactly two factors. The primes up to 50 are 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47. Two is the only even prime and 1 is neither prime nor composite. To test a number up to 120, divide by 2, 3, 5, 7 only. If none divides it, it is prime. The usual traps are $51=3\times17$, $57=3\times19$, $87=3\times29$, $91=7\times13$.

**Number of factors.** If $N=p^a q^b r^c$ then the number of factors is $(a+1)(b+1)(c+1)$. For $36=2^2\cdot3^2$ that is $3\times3=9$.

**Division statement.** $N=dq+r$ with $0\le r<d$. If a number leaves remainder 7 on division by 10, it leaves remainder $7-5=2$ on division by 5, because 5 divides 10.

**Even and odd results.**

| Expression | Always |
|---|---|
| $n(n+1)$ | even (one of two consecutive integers is even) |
| $n^2+n$, $n^2-n$ | even |
| $n^3-n=(n-1)n(n+1)$ | divisible by 6 |
| $n^2+1$ | even only if $n$ is odd |
| odd + odd, even + even | even |
| odd × odd | odd |

::: caution Traps
$n(n+2)$ is even only when $n$ is even, and $n^2+1$ is not always even. The question says "must be", so one counter-example kills an option.
:::

## 1.2 HCF and LCM and their word problems

- **Product rule.** For two numbers, $\text{HCF}\times\text{LCM}=a\times b$. Given any three of the four quantities, the fourth follows.
- **Fractions.** $\text{HCF}\left(\frac{a}{b},\frac{c}{d}\right)=\frac{\text{HCF}(a,c)}{\text{LCM}(b,d)}$ and $\text{LCM}=\frac{\text{LCM}(a,c)}{\text{HCF}(b,d)}$ (fractions in lowest terms).
- **Greatest number that divides $a$, $b$, $c$ leaving remainders $r_1,r_2,r_3$** is the HCF of $(a-r_1),(b-r_2),(c-r_3)$.
- **Least number that leaves remainder $r$ on division by $x,y,z$** is $\text{LCM}(x,y,z)+r$.
- **Bells, lights, runners** that repeat every $x,y,z$ units meet again after $\text{LCM}(x,y,z)$.
- **Co-prime numbers** have HCF 1, so their LCM is their product.

::: example Two numbers from HCF and LCM
**Problem.** The HCF of two numbers is 8 and their LCM is 240. One number is 48. Find the other.

**Solution.** Other $=\dfrac{8\times240}{48}=40$.
:::

## 1.3 Ratio, proportion, variation and ages

- $a:b=c:d$ means $ad=bc$. The mean proportional of $a$ and $b$ is $\sqrt{ab}$.
- **Chain a ratio.** From $a:b=2:3$ and $b:c=4:5$, make $b$ equal in both: $a:b=8:12$, $b:c=12:15$, so $a:b:c=8:12:15$.
- **Dividing $N$ in the ratio $p:q$**: the shares are $\frac{p}{p+q}N$ and $\frac{q}{p+q}N$.
- **Direct variation**: $y/x$ constant. **Inverse variation**: $xy$ constant (more men, fewer days).
- **Age problems**: let the present ages be $ax$ and $bx$ if they are in ratio $a:b$; the difference between ages never changes, so a difference of 8 years equals $(b-a)$ parts.

## 1.4 Percentage and successive change

- $x\%$ of $y$ equals $y\%$ of $x$. "Per cent" is "per hundred", so $x\% = \frac{x}{100}$.
- **Learn this table**: $\frac{1}{2}=50\%$, $\frac{1}{3}=33\frac{1}{3}\%$, $\frac{1}{4}=25\%$, $\frac{1}{5}=20\%$, $\frac{1}{6}=16\frac{2}{3}\%$, $\frac{1}{8}=12.5\%$, $\frac{1}{9}=11\frac{1}{9}\%$, $\frac{1}{10}=10\%$, $\frac{1}{12}=8\frac{1}{3}\%$.
- **Successive change** of $a\%$ then $b\%$ is a net $a+b+\frac{ab}{100}$ per cent (use a minus sign for a fall). A 20 % rise followed by a 20 % fall: $20-20-4=-4\%$.
- **Percent more / less.** If $A$ is $r\%$ more than $B$, then $B$ is $\frac{100r}{100+r}\%$ less than $A$. (25 % more gives 20 % less.)
- **Keeping expenditure fixed** after a price rise of $r\%$ needs a cut in consumption of $\frac{100r}{100+r}\%$.
- **Population / depreciation**: $P\left(1\pm\frac{r}{100}\right)^n$.

::: tip Fast method
Convert percent to a multiplier. +15 % is ×1.15, −20 % is ×0.8. For successive changes multiply the multipliers.
:::

## 1.5 Averages and weighted averages

- $\text{Average}=\dfrac{\text{sum}}{\text{number of items}}$, so sum $=$ average $\times$ number.
- The average of the first $n$ natural numbers is $\frac{n+1}{2}$; of any evenly spaced list it is the middle value (or the mean of the first and last).
- **A member leaves or joins**: work with totals. Removed value $=$ old total $-$ new total.
- **Weighted mean** of groups with sizes $n_1,n_2$ and averages $A_1,A_2$ is $\frac{n_1A_1+n_2A_2}{n_1+n_2}$.
- Adding a value equal to the current average leaves the average unchanged.

::: example A teacher joins the class
**Problem.** The average age of 20 students is 15 years. When the teacher is included, the average becomes 16. Find the teacher's age.

**Solution.** New total $=21\times16=336$, old total $=20\times15=300$. Teacher $=336-300=36$ years.
:::

## Formula and fact sheet

| Topic | Result |
|---|---|
| HCF × LCM | $= a\times b$ (two numbers only) |
| Least number with remainder $r$ | $\text{LCM}+r$ |
| Number of factors | $(a+1)(b+1)\cdots$ |
| Successive change | $a+b+\frac{ab}{100}$ |
| $r\%$ more ⇒ less by | $\frac{100r}{100+r}\%$ |
| Weighted mean | $\frac{n_1A_1+n_2A_2}{n_1+n_2}$ |
| Average of $1,\dots,n$ | $\frac{n+1}{2}$ |

## Chapter summary

- Check divisibility by digit sums and last digits before dividing; primes up to 120 need testing by 2, 3, 5, 7 only.
- $n(n+1)$ is always even; $n^3-n$ is always a multiple of 6.
- HCF × LCM equals the product of the two numbers, and of no other count of numbers.
- "Greatest divisor" means HCF of the differences from the remainders; "least number" means LCM plus the remainder.
- Chain ratios by matching the common term, then divide in parts.
- Percentage change is always on the base the question names; successive changes multiply.
- A 25 % rise is undone by a 20 % fall, not a 25 % fall.
- For averages, deal in totals, not in averages.

## Practice questions

**Set A — Recall (20 questions)**

1. The sum of the first five prime numbers is
   (a) 18 (b) 25 (c) 26 (d) 28
2. Which number is divisible by 9?
   (a) 4,321 (b) 5,238 (c) 7,415 (d) 6,073
3. The HCF of 36 and 48 is
   (a) 12 (b) 6 (c) 18 (d) 24
4. The LCM of 12, 15 and 20 is
   (a) 30 (b) 120 (c) 60 (d) 180
5. The product of two numbers is 2,160 and their HCF is 12. Their LCM is
   (a) 144 (b) 180 (c) 240 (d) 360
6. 12.5 % of 640 is
   (a) 64 (b) 72 (c) 90 (d) 80
7. If $a:b=2:3$ and $b:c=4:5$, then $a:c$ is
   (a) 6:15 (b) 2:5 (c) 8:15 (d) 4:5
8. The average of the first ten natural numbers is
   (a) 5.5 (b) 5 (c) 6 (d) 6.5
9. A number leaves remainder 7 when divided by 10. The remainder on division by 5 is
   (a) 0 (b) 1 (c) 3 (d) 2
10. Which of the following is a prime number?
    (a) 51 (b) 53 (c) 57 (d) 91
11. The number of factors of 36 is
    (a) 6 (b) 8 (c) 9 (d) 12
12. 0.375 expressed as a percentage is
    (a) 37.5 % (b) 3.75 % (c) 33.3 % (d) 0.375 %
13. If $n$ is an integer, which expression must be even?
    (a) $n+1$ (b) $n^2+1$ (c) $n(n+2)$ (d) $n(n+1)$
14. The only even prime number is
    (a) 0 (b) 1 (c) 2 (d) 4
15. 200 increased by 15 % is
    (a) 215 (b) 230 (c) 245 (d) 300
16. When Rs 56 is divided in the ratio 3 : 4, the larger share is
    (a) Rs 32 (b) Rs 24 (c) Rs 28 (d) Rs 36
17. The average of five numbers is 20. Their sum is
    (a) 25 (b) 80 (c) 120 (d) 100
18. $\frac{1}{8}$ expressed as a percentage is
    (a) 8 % (b) 12.5 % (c) 15 % (d) 18 %
19. Which number is divisible by 4?
    (a) 3,214 (b) 5,102 (c) 7,316 (d) 9,018
20. The LCM of the co-prime numbers 7 and 9 is
    (a) 63 (b) 1 (c) 16 (d) 126

::: note Answers and explanations — Set A
**1.** (d) — 2 + 3 + 5 + 7 + 11 = 28. Option (b) 25 is what you get after dropping 2.
**2.** (b) — digit sum of 5,238 is 18, a multiple of 9. The others give 10, 17 and 16.
**3.** (a) — 36 = 2²·3², 48 = 2⁴·3, so the HCF is 2²·3 = 12. 6 is a common divisor but not the greatest.
**4.** (c) — 12 = 2²·3, 15 = 3·5, 20 = 2²·5, so LCM = 2²·3·5 = 60.
**5.** (b) — LCM = 2160 ÷ 12 = 180.
**6.** (d) — 12.5 % = 1/8, and 640 ÷ 8 = 80.
**7.** (c) — make b equal: 2:3 = 8:12 and 4:5 = 12:15, so a:c = 8:15.
**8.** (a) — (1 + 10)/2 = 5.5.
**9.** (d) — N = 10q + 7 = 5(2q + 1) + 2, remainder 2.
**10.** (b) — 53 has no divisor among 2, 3, 5, 7. 51 = 3×17, 57 = 3×19, 91 = 7×13.
**11.** (c) — 36 = 2²·3², so (2+1)(2+1) = 9.
**12.** (a) — 0.375 = 3/8 = 37.5 %. Multiply a decimal by 100.
**13.** (d) — n(n+1) is a product of consecutive integers. n(n+2) is odd when n is odd.
**14.** (c) — every other even number has 2 as a factor besides 1 and itself.
**15.** (b) — 200 × 1.15 = 230.
**16.** (a) — 56 ÷ 7 = 8 per part, 4 × 8 = 32.
**17.** (d) — sum = average × number = 20 × 5 = 100.
**18.** (b) — 100 ÷ 8 = 12.5.
**19.** (c) — the last two digits 16 are divisible by 4. 14, 02 and 18 are not.
**20.** (a) — co-prime numbers have LCM equal to their product, 63.
:::

**Set B — Understanding (12 questions)**

1. The HCF of two numbers is 8 and their LCM is 240. If one number is 48, the other is
   (a) 30 (b) 36 (c) 40 (d) 80
2. The greatest number that divides 62, 132 and 237 leaving remainders 2, 6 and 5 respectively is
   (a) 2 (b) 4 (c) 6 (d) 12
3. The least number which leaves remainder 5 when divided by 6, 8 and 12 is
   (a) 24 (b) 25 (c) 48 (d) 29
4. Rs 1,750 is shared among A, B, C so that A:B = 2:3 and B:C = 4:5. C receives
   (a) Rs 700 (b) Rs 750 (c) Rs 800 (d) Rs 600
5. A price is raised by 20 % and then reduced by 20 %. The net effect is
   (a) no change (b) 4 % increase (c) 4 % decrease (d) 2 % decrease
6. A town of 20,000 people grows by 10 % every year. After two years its population is
   (a) 24,200 (b) 24,000 (c) 22,000 (d) 24,400
7. The average of five numbers is 27. When one is removed the average of the rest is 25. The removed number is
   (a) 30 (b) 32 (c) 37 (d) 35
8. The average age of 20 students is 15 years. Including the teacher, it is 16. The teacher is
   (a) 31 years (b) 36 years (c) 41 years (d) 46 years
9. A father is three times as old as his son. After 10 years he will be twice as old. The son's present age is
   (a) 10 years (b) 12 years (c) 15 years (d) 20 years
10. A is 25 % more than B. B is less than A by
    (a) 25 % (b) 12.5 % (c) 33⅓ % (d) 20 %
11. If 35 % of a number is 84, the number is
    (a) 210 (b) 235 (c) 240 (d) 294
12. Three numbers are in the ratio 1:2:3 and the sum of their squares is 504. The largest number is
    (a) 12 (b) 18 (c) 24 (d) 36

::: note Answers and explanations — Set B
**1.** (c) — other = (8 × 240) ÷ 48 = 40.
**2.** (a) — HCF of 60, 126, 232: 60 = 2²·3·5, 126 = 2·3²·7, 232 = 2³·29, so only 2 is common.
**3.** (d) — LCM(6, 8, 12) = 24, and 24 + 5 = 29. The LCM alone (24) leaves remainder 0.
**4.** (b) — A:B:C = 8:12:15, total 35 parts, 1750 ÷ 35 = 50, C = 15 × 50 = 750.
**5.** (c) — 20 − 20 − (20×20)/100 = −4 %. The common error is "no change".
**6.** (a) — 20,000 × 1.1 × 1.1 = 24,200. Simple growth would give 24,000.
**7.** (d) — removed = 5×27 − 4×25 = 135 − 100 = 35.
**8.** (b) — 21 × 16 − 20 × 15 = 336 − 300 = 36.
**9.** (a) — 3S + 10 = 2(S + 10) gives S = 10, father 30.
**10.** (d) — A = 125, B = 100, so B is 25/125 = 20 % less than A.
**11.** (c) — 84 ÷ 0.35 = 240.
**12.** (b) — numbers k, 2k, 3k: 14k² = 504, k = 6, largest 18.
:::

**Set C — Application (10 questions)**

1. Three bells ring at intervals of 12, 18 and 30 seconds and ring together at 9:00:00. They next ring together at
   (a) 9:02 (b) 9:03 (c) 9:04 (d) 9:06
2. The price of rice rises by 25 %. To keep the monthly spending unchanged, consumption must fall by
   (a) 25 % (b) 15 % (c) 12.5 % (d) 20 %
3. In a two-candidate election the winner gets 55 % of the votes and wins by 2,000 votes. The total number of votes is
   (a) 20,000 (b) 22,000 (c) 18,000 (d) 25,000
4. The mean mark of 30 students is 60 and of 20 other students is 75. The mean of all 50 is
   (a) 65 (b) 67.5 (c) 66 (d) 68
5. Two ages are in the ratio 3:5 and the elder is 8 years older. The younger is
   (a) 9 years (b) 12 years (c) 15 years (d) 18 years
6. How many numbers from 1 to 100 are divisible by both 4 and 6?
   (a) 6 (b) 7 (c) 9 (d) 8
7. Two numbers have HCF 6 and LCM 180, and their sum is 66. The larger number is
   (a) 30 (b) 32 (c) 36 (d) 40
8. A number is increased by 20 % and the result is decreased by 25 %, giving 270. The number is
   (a) 300 (b) 320 (c) 250 (d) 280
9. The remainder when $2^{10}$ is divided by 7 is
   (a) 1 (b) 4 (c) 3 (d) 2
10. The average of seven consecutive integers is 20. The largest is
    (a) 22 (b) 23 (c) 24 (d) 26

::: note Answers and explanations — Set C
**1.** (b) — LCM(12, 18, 30) = 180 s = 3 min.
**2.** (d) — 100 × 25/125 = 20 %. Cutting by 25 % would leave spending below the old value.
**3.** (a) — winner − loser = 55 % − 45 % = 10 % of the total = 2,000, so total = 20,000.
**4.** (c) — (30×60 + 20×75) ÷ 50 = 3300 ÷ 50 = 66. The simple mean 67.5 ignores the group sizes.
**5.** (b) — 5 − 3 = 2 parts = 8, one part = 4, younger = 12.
**6.** (d) — LCM(4, 6) = 12 and 12, 24, …, 96 gives 8 multiples.
**7.** (c) — numbers are 6a, 6b with ab = 30 and a + b = 11, so a, b = 5, 6 and the numbers are 30, 36.
**8.** (a) — x × 1.2 × 0.75 = 0.9x = 270, so x = 300.
**9.** (d) — 2³ = 8 ≡ 1 (mod 7), so 2¹⁰ = (2³)³ · 2 ≡ 2.
**10.** (b) — the middle (fourth) number is 20, so the seven are 17 to 23.
:::
