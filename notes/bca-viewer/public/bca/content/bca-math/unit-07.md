---
subject: Mathematics
grade: BCA
unit: 7
title: Permutation, Combination, Probability and Statistics
hours: 1
area: Algebra
---

One question in the paper, but it can come from any of four topics: counting, probability, central tendency or spread. Learn the nPr/nCr formulas, the dice-and-cards facts, and the three averages. The single question is usually the easiest in the paper if you know the vocabulary.

::: key What the paper asks from this chapter
- **Counting**: $n!$, ${}^nP_r$, ${}^nC_r$, words with repeated letters, "together" problems, circular arrangements.
- **Probability**: favourable ÷ total, addition rule, independent events, dice, coins and cards.
- **Statistics**: mean, median, mode, the mean–median–mode relation, and standard deviation.
:::

## 7.1 Fundamental principle, permutations and combinations

- **Multiplication principle**: $m$ ways then $n$ ways gives $mn$.
- ${}^nP_r=\frac{n!}{(n-r)!}$, ${}^nC_r=\frac{n!}{r!(n-r)!}$, ${}^nC_r={}^nC_{n-r}$, $0!=1$, ${}^nC_0=1$.
- Letters of a word with repeats: $\frac{n!}{p!\,q!\cdots}$ (BANANA: $\frac{6!}{3!\,2!}=60$).
- Two objects **together**: treat as one block, then multiply by $2!$. Circular arrangements of $n$: $(n-1)!$.
- "At least one" is easiest as total minus none.

## 7.2 Probability of events

- $P(E)=\frac{\text{favourable}}{\text{total}}$, $0\le P\le1$, $P(E)+P(E')=1$.
- $P(A\cup B)=P(A)+P(B)-P(A\cap B)$. Independent: $P(A\cap B)=P(A)P(B)$.
- **Facts**: coin 2 outcomes; die 6; two dice 36 (sum 7 in 6 ways); pack of 52 cards = 26 red + 26 black, 13 per suit, 12 face cards, 4 aces; 3 coins have 8 outcomes.

## 7.3 Mean, median, mode and dispersion

- Mean $=\frac{\sum x}{n}$; median is the middle value of the ordered data (mean of the two middle values if $n$ is even); mode is the most frequent value.
- Empirical relation: $\text{mode}=3\,\text{median}-2\,\text{mean}$.
- Range $=$ max − min. Variance $=\frac{\sum(x-\bar{x})^2}{n}$, SD $=\sqrt{\text{variance}}$.
- Adding a constant to every value shifts the mean but **leaves SD unchanged**; multiplying by $k$ multiplies the mean and SD by $k$.

## Formula and fact sheet

| Item | Result |
|---|---|
| ${}^nP_r$, ${}^nC_r$ | $\frac{n!}{(n-r)!}$, $\frac{n!}{r!(n-r)!}$ |
| Repeats | $\frac{n!}{p!q!}$ |
| $P(A\cup B)$ | $P(A)+P(B)-P(A\cap B)$ |
| Mode | $3\,\text{median}-2\,\text{mean}$ |

## Chapter summary

- Order matters: permutation. Order does not matter: combination.
- Divide by factorials of repeated letters.
- Subtract from the total for "at least one".
- Independent events multiply; overlapping events subtract the intersection.
- SD ignores a constant shift.

## Practice questions

**Set A — Recall (20 questions)**

1. The value of $5!$ is
   (a) 24 (b) 60 (c) 120 (d) 720
2. The value of ${}^5P_2$ is
   (a) 10 (b) 25 (c) 15 (d) 20
3. The value of ${}^5C_2$ is
   (a) 10 (b) 20 (c) 5 (d) 25
4. The probability of getting a head on a fair coin is
   (a) 1 (b) $\frac{1}{2}$ (c) $\frac{1}{4}$ (d) 0
5. The probability of a sure event is
   (a) 0 (b) $\frac{1}{2}$ (c) 2 (d) 1
6. The number of face cards in a pack of 52 is
   (a) 4 (b) 16 (c) 12 (d) 13
7. The median of 3, 5, 7, 9, 11 is
   (a) 5 (b) 7 (c) 9 (d) 35
8. The mean of 2, 4, 6, 8, 10 is
   (a) 6 (b) 5 (c) 8 (d) 30
9. The mode of 2, 3, 3, 4, 5, 3, 6 is
   (a) 2 (b) 4 (c) 5 (d) 3
10. ${}^nC_0$ equals
    (a) 0 (b) $n$ (c) 1 (d) $n!$
11. The number of arrangements of the letters of MAT is
    (a) 6 (b) 3 (c) 9 (d) 12
12. $P(A)+P(A')$ equals
    (a) 0 (b) 1 (c) $\frac{1}{2}$ (d) $P(A)$
13. The probability of getting a 6 when a die is thrown is
    (a) $\frac{1}{3}$ (b) $\frac{1}{2}$ (c) $\frac{1}{6}$ (d) 6
14. The number of outcomes when three coins are tossed is
    (a) 3 (b) 6 (c) 9 (d) 8
15. The value of $0!$ is
    (a) 1 (b) 0 (c) undefined (d) infinite
16. The standard deviation is the square root of the
    (a) mean (b) variance (c) range (d) mode
17. The range of 4, 9, 15, 20 is
    (a) 20 (b) 5 (c) 16 (d) 11
18. The value of ${}^{10}C_8$ is
    (a) 90 (b) 80 (c) 10 (d) 45
19. The number of circular arrangements of $n$ distinct objects is
    (a) $(n-1)!$ (b) $n!$ (c) $\frac{n!}{2}$ (d) $2n$
20. The probability of drawing a red card from a standard pack is
    (a) $\frac{1}{4}$ (b) $\frac{1}{2}$ (c) $\frac{1}{13}$ (d) $\frac{3}{4}$

::: note Answers and explanations — Set A
**1.** (c) — 5·4·3·2·1 = 120.
**2.** (d) — 5 × 4 = 20.
**3.** (a) — 20 / 2 = 10; (b) is the permutation.
**4.** (b) — one favourable of two.
**5.** (d) — a sure event has probability 1.
**6.** (c) — J, Q, K in four suits.
**7.** (b) — the middle value.
**8.** (a) — 30 / 5 = 6.
**9.** (d) — 3 occurs three times.
**10.** (c) — one way to choose nothing.
**11.** (a) — 3! = 6.
**12.** (b) — complementary events.
**13.** (c) — one of six faces.
**14.** (d) — 2³ = 8.
**15.** (a) — by definition.
**16.** (b) — SD = √variance.
**17.** (c) — 20 − 4.
**18.** (d) — ¹⁰C₈ = ¹⁰C₂ = 45.
**19.** (a) — fix one object, arrange the rest.
**20.** (b) — 26 of 52.
:::

**Set B — Understanding (12 questions)**

1. The number of distinct arrangements of the letters of BANANA is
   (a) 720 (b) 120 (c) 30 (d) 60
2. A committee of 3 is chosen from 8 people. The number of ways is
   (a) 56 (b) 336 (c) 24 (d) 28
3. Two dice are thrown. The probability that the sum is 7 is
   (a) $\frac{1}{12}$ (b) $\frac{1}{36}$ (c) $\frac{1}{6}$ (d) $\frac{1}{3}$
4. For independent events with $P(A)=0.4$ and $P(B)=0.5$, $P(A\cap B)$ is
   (a) 0.9 (b) 0.2 (c) 0.1 (d) 0.45
5. If $P(A)=0.5$, $P(B)=0.4$ and $P(A\cap B)=0.2$, then $P(A\cup B)$ is
   (a) 0.7 (b) 0.9 (c) 0.1 (d) 0.2
6. The mean of five numbers is 12. A sixth number 18 is added. The new mean is
   (a) 12 (b) 12.5 (c) 14 (d) 13
7. If the median is 20 and the mean is 18, the mode by the empirical relation is
   (a) 22 (b) 26 (c) 24 (d) 21
8. Every value in a data set is increased by 5. The standard deviation
   (a) increases by 5 (b) is unchanged (c) doubles (d) becomes zero
9. The number of words that can be formed by rearranging all letters of MATH is
   (a) 12 (b) 16 (c) 6 (d) 24
10. The probability of two heads in two tosses of a fair coin is
    (a) $\frac{1}{4}$ (b) $\frac{1}{2}$ (c) $\frac{1}{3}$ (d) $\frac{3}{4}$
11. Five people stand in a row with two particular people always together. The number of arrangements is
    (a) 24 (b) 48 (c) 72 (d) 120
12. The standard deviation of 2, 4, 4, 4, 5, 5, 7, 9 is
    (a) 1 (b) 4 (c) 2 (d) 5

::: note Answers and explanations — Set B
**1.** (d) — 6!/(3!·2!) = 60.
**2.** (a) — ⁸C₃ = 56; order does not matter.
**3.** (c) — six of 36 outcomes.
**4.** (b) — 0.4 × 0.5.
**5.** (a) — 0.5 + 0.4 − 0.2.
**6.** (d) — (60 + 18)/6 = 13.
**7.** (c) — 3(20) − 2(18) = 24.
**8.** (b) — a shift does not change spread.
**9.** (d) — 4! = 24.
**10.** (a) — (1/2)(1/2).
**11.** (b) — block of two: 2 × 4! = 48.
**12.** (c) — mean 5, squared deviations total 32, variance 4, SD 2.
:::

**Set C — Application (8 questions)**

1. The number of 3-digit numbers that can be formed from the digits 1 to 5 without repetition is
   (a) 60 (b) 125 (c) 10 (d) 15
2. Two cards are drawn from a pack of 52. The probability that both are aces is
   (a) $\frac{1}{169}$ (b) $\frac{1}{26}$ (c) $\frac{1}{221}$ (d) $\frac{1}{13}$
3. A committee of 3 is chosen from 4 men and 3 women with at least one woman. The number of ways is
   (a) 35 (b) 30 (c) 34 (d) 31
4. The probability of at least one head in three tosses of a fair coin is
   (a) $\frac{3}{8}$ (b) $\frac{7}{8}$ (c) $\frac{1}{8}$ (d) $\frac{1}{2}$
5. The variance of 40, 50, 60, 70, 80 is
   (a) 200 (b) 100 (c) 50 (d) 14
6. If ${}^nC_2=28$, then $n$ is
   (a) 6 (b) 7 (c) 9 (d) 8
7. If ${}^nP_2=42$, then $n$ is
   (a) 6 (b) 7 (c) 8 (d) 9
8. A number is chosen at random from 1 to 20. The probability that it is a multiple of 3 or 5 is
   (a) $\frac{1}{2}$ (b) $\frac{2}{5}$ (c) $\frac{9}{20}$ (d) $\frac{11}{20}$

::: note Answers and explanations — Set C
**1.** (a) — ⁵P₃ = 5·4·3 = 60.
**2.** (c) — (4·3)/(52·51) = 1/221.
**3.** (d) — total ⁷C₃ = 35 minus all-men ⁴C₃ = 4.
**4.** (b) — 1 − (1/2)³.
**5.** (a) — mean 60, squared deviations 1000, divided by 5.
**6.** (d) — 8·7/2 = 28.
**7.** (b) — 7·6 = 42.
**8.** (c) — 6 + 4 − 1 (15 counted twice) = 9 of 20.
:::
