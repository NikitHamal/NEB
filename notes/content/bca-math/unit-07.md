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

```photogrid label="7.1" cols="3" ratio="1.0" caption="Probability began with gambling. (a) Blaise Pascal (1623-1662), who with Fermat founded probability theory in letters of 1654 about a dice game, and whose triangle of binomial coefficients appears in Fig 7.1. (b) and (c) Dice: each face of a fair die has probability 1/6, and two dice give 6 x 6 = 36 equally likely outcomes."
@ photo id="bcamath/pascal" cap="Blaise Pascal, co-founder of probability"
focus 0.5 0.3
@ photo id="bcamath/dice" cap="Four dice: each face 1/6"
focus 0.5 0.5
@ photo id="bcamath/dice2" cap="Two dice: 36 outcomes"
focus 0.5 0.5
```

```svgfig label="7.1" caption="Pascal's triangle computed with math.comb. Each entry is the sum of the two above it and equals C(n, r): C(5, 2) = 10 (highlighted) is the number of ways to choose 2 from 5, and every row adds to 2^n. Right: P(5, 3) = 60 ordered arrangements but C(5, 3) = 10 groups, because each group of 3 can be arranged in 3! = 6 ways; the letters of BANANA give 6!/(3! x 2!) = 60 words."
import math
for n in range(9):
    assert sum(math.comb(n, r) for r in range(n + 1)) == 2 ** n
assert math.comb(5, 2) == 10 and math.perm(5, 3) == 60 and math.comb(5, 3) == 10 and 60 // math.factorial(3) == 10
assert math.factorial(6) // (math.factorial(3) * math.factorial(2)) == 60 and math.comb(10, 3) == math.comb(10, 7) == 120
f = Fig(780, 320)
for n in range(9):
    for r in range(n + 1):
        x = 240 + (r - n / 2) * 40; y = 24 + n * 32
        hi = (n, r) == (5, 2)
        f.circle(x, y, 15, fill=("#fde68a" if hi else "#dbeafe"), stroke=(RED if hi else NAVY), label=str(math.comb(n, r)), size=(10 if math.comb(n, r) > 9 else 11), color=NAVY, bold=True)
    f.text(10, y + 4, "n=%d" % n, size=10, color=SLATE, anchor="start")
    f.text(440, y + 4, "= %d" % 2 ** n, size=10, color=TEAL, bold=True, anchor="start")
f.text(465, 12, "row sum 2^n", size=10, color=TEAL, bold=True, anchor="start")
f.text(620, 26, "Order matters or not?", size=11.5, color=NAVY, bold=True)
for j, (t, c) in enumerate([("P(n, r) = n! / (n - r)!", NAVY), ("C(n, r) = n! / (r! (n - r)!)", NAVY), ("P(5, 3) = 5 x 4 x 3 = 60 (ordered)", SLATE), ("C(5, 3) = 60 / 3! = 10 (groups)", SLATE), ("C(10, 3) = C(10, 7) = 120", TEAL), ("BANANA: 6!/(3! 2!) = 60 words", RED), ("circle of n people: (n - 1)!", SLATE), ("5 people in a row: 5! = 120", SLATE)]):
    f.text(520, 62 + j * 30, t, size=10.5, color=c, anchor="start", bold=(c in (NAVY, RED)))
```

## 7.2 Probability of events

- $P(E)=\frac{\text{favourable}}{\text{total}}$, $0\le P\le1$, $P(E)+P(E')=1$.
- $P(A\cup B)=P(A)+P(B)-P(A\cap B)$. Independent: $P(A\cap B)=P(A)P(B)$.
- **Facts**: coin 2 outcomes; die 6; two dice 36 (sum 7 in 6 ways); pack of 52 cards = 26 red + 26 black, 13 per suit, 12 face cards, 4 aces; 3 coins have 8 outcomes.

```svgfig label="7.2" caption="The sample space of two dice, counted by the cell. Of 36 equally likely pairs, 6 sum to 7 (probability 1/6), 6 give a double (1/6), and 6 sum to 10 or more (1/6); the sum 7 is the most likely and 2 or 12 the least (1/36). Bars on the right show the number of ways to make each sum from 2 to 12: 1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1."
from fractions import Fraction as F
pairs = [(a, b) for a in range(1, 7) for b in range(1, 7)]
s7 = [p for p in pairs if sum(p) == 7]; dbl = [p for p in pairs if p[0] == p[1]]; ge10 = [p for p in pairs if sum(p) >= 10]
assert len(pairs) == 36 and len(s7) == len(dbl) == len(ge10) == 6 and F(len(s7), 36) == F(1, 6)
ways = [len([p for p in pairs if sum(p) == s]) for s in range(2, 13)]; assert ways == [1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1]
f = Fig(780, 320); c = 38
f.text(150, 18, "die 2 down, die 1 across; sum 7 in gold, doubles ringed", size=10.5, color=NAVY, bold=True)
for a in range(1, 7):
    f.text(20 + a * c, 44, str(a), size=11, color=SLATE, bold=True); f.text(20, 44 + a * c - 8 + 18, str(a), size=11, color=SLATE, bold=True)
for (a, b) in pairs:
    x = 36 + (a - 1) * c + c / 2 - c / 2 + 6; y = 52 + (b - 1) * c
    col = "#fde68a" if a + b == 7 else ("#fecaca" if a + b >= 10 else "#dbeafe")
    f.box(x, y, c - 3, c - 3, str(a + b), fill=col, stroke=(RED if a == b else "#cbd5e1"), size=11, bold=True, color=NAVY, r=2)
f.text(150, 298, "red tint: sum 10 or more (6);  red ring: doubles (6)", size=10.5, color=SLATE)
f.text(580, 24, "Ways to make each sum", size=11.5, color=NAVY, bold=True)
for i, w in enumerate(ways):
    y = 40 + i * 24
    f.text(420, y + 9, "sum %d" % (i + 2), size=10, color=SLATE, anchor="end", vmid=True)
    f.box(430, y, w * 40, 19, str(w), fill=("#fde68a" if w == 6 else "#bfdbfe"), stroke=NAVY, size=10, bold=True, r=2)
f.text(580, 312, "P(sum = 7) = 6/36 = 1/6", size=11, color=RED, bold=True)
```

```svgfig label="7.3" caption="Probability rules on a pack of 52 cards. 13 are hearts, 4 are kings, and 1 card (the king of hearts) is both. P(heart or king) = 13/52 + 4/52 - 1/52 = 16/52 = 4/13. Because P(heart and king) = 1/52 = (1/4) x (1/13), being a heart and being a king are independent. The complement rule gives P(not a heart) = 1 - 1/4 = 3/4."
from fractions import Fraction as F
H, K, HK = F(13, 52), F(4, 52), F(1, 52)
assert H + K - HK == F(16, 52) == F(4, 13) and HK == H * K and 1 - H == F(3, 4) and HK / K == H
f = Fig(780, 320)
f.box(20, 20, 420, 280, "", fill="#f8fafc", stroke=SLATE, r=4); f.text(40, 40, "52 cards", size=11, color=SLATE, bold=True, anchor="start")
f.raw('<circle cx="170" cy="160" r="100" fill="#ef4444" fill-opacity="0.22" stroke="#b91c1c" stroke-width="2"/>')
f.raw('<circle cx="270" cy="160" r="70" fill="#2563eb" fill-opacity="0.22" stroke="#1e3a8a" stroke-width="2"/>')
f.text(130, 150, "12", size=18, color=RED, bold=True); f.text(130, 176, "hearts only", size=10.5, color=RED)
f.text(220, 150, "1", size=18, color=NAVY, bold=True); f.text(220, 172, "K of", size=10, color=NAVY); f.text(220, 186, "hearts", size=10, color=NAVY)
f.text(300, 150, "3", size=18, color=NAVY, bold=True); f.text(300, 176, "other kings", size=10.5, color=NAVY)
f.text(385, 280, "36 other cards", size=11, color=SLATE, bold=True)
f.text(120, 262, "hearts: 13", size=11, color=RED, bold=True); f.text(310, 238, "kings: 4", size=11, color=NAVY, bold=True)
f.text(600, 30, "Rules checked with fractions", size=11.5, color=NAVY, bold=True)
for j, (t, c) in enumerate([("P(heart) = 13/52 = 1/4", RED), ("P(king) = 4/52 = 1/13", NAVY), ("P(heart or king) = 13/52 + 4/52 - 1/52", SLATE), ("= 16/52 = 4/13", TEAL), ("P(heart and king) = 1/52", SLATE), ("= (1/4)(1/13): independent", TEAL), ("P(king | heart) = (1/52)/(13/52) = 1/13", SLATE), ("P(not heart) = 1 - 1/4 = 3/4", SLATE), ("mutually exclusive: P(A and B) = 0", RED)]):
    f.text(465, 64 + j * 28, t, size=10.5, color=c, anchor="start", bold=(c in (TEAL, RED)))
```

## 7.3 Mean, median, mode and dispersion

- Mean $=\frac{\sum x}{n}$; median is the middle value of the ordered data (mean of the two middle values if $n$ is even); mode is the most frequent value.
- Empirical relation: $\text{mode}=3\,\text{median}-2\,\text{mean}$.
- Range $=$ max − min. Variance $=\frac{\sum(x-\bar{x})^2}{n}$, SD $=\sqrt{\text{variance}}$.
- Adding a constant to every value shifts the mean but **leaves SD unchanged**; multiplying by $k$ multiplies the mean and SD by $k$.

```svgfig label="7.4" caption="Mean, median, mode and spread for the marks 4, 5, 5, 6, 7, 8, 8, 8, 9, 10, computed in the cell. Mean = 70/10 = 7, median = (7 + 8)/2 = 7.5, mode = 8, variance = 34/10 = 3.4 and standard deviation = 1.84. Replace the 10 by an outlier 40: the mean jumps to 10 but the median stays 7.5, so the median resists outliers."
import statistics as st, math
d = [4, 5, 5, 6, 7, 8, 8, 8, 9, 10]
m = sum(d) / len(d); md = st.median(d); mo = st.mode(d); var = sum((x - m) ** 2 for x in d) / len(d); sd = math.sqrt(var)
assert (m, md, mo) == (7.0, 7.5, 8) and round(var, 2) == 3.4 and round(sd, 2) == 1.84
d2 = d[:-1] + [40]; assert sum(d2) / 10 == 10.0 and st.median(d2) == 7.5
f = Fig(780, 320)
X = lambda v: 40 + v * 33
f.line(X(0), 200, X(11), 200, color=SLATE, sw=1.6)
for v in range(0, 12): f.line(X(v), 195, X(v), 205, color=SLATE, sw=1.2); f.text(X(v), 222, str(v), size=10.5, color=SLATE)
cnt = {}
for v in d: cnt[v] = cnt.get(v, 0) + 1; f.circle(X(v), 190 - cnt[v] * 22, 9, fill=("#fde68a" if v == 8 else "#bfdbfe"), stroke=NAVY)
f.line(X(m), 60, X(m), 200, color=RED, sw=1.8, dash=True); f.text(X(m) - 4, 56, "mean 7", size=11, color=RED, bold=True, anchor="end")
f.line(X(md), 80, X(md), 200, color=TEAL, sw=1.8, dash=True); f.text(X(md) + 4, 76, "median 7.5", size=11, color=TEAL, bold=True, anchor="start")
f.text(X(8), 108, "mode 8", size=11, color=AMBER, bold=True, anchor="start")
f.text(200, 24, "Dot plot of ten marks", size=11.5, color=NAVY, bold=True)
f.text(200, 262, "variance = 34 / 10 = 3.4, SD = 1.84 (square root of 3.4)", size=11, color=NAVY, bold=True)
f.text(200, 288, "sum of squared deviations: 9+4+4+1+0+1+1+1+4+9 = 34", size=10.5, color=SLATE)
f.text(600, 30, "With an outlier (10 becomes 40)", size=11.5, color=NAVY, bold=True)
for j, (t, c) in enumerate([("old mean 7", SLATE), ("new mean 10  (jumps by 3)", RED), ("old median 7.5", SLATE), ("new median 7.5  (unchanged)", TEAL), ("mode stays 8", SLATE), ("Mean uses every value;", NAVY), ("the median uses only the middle.", NAVY), ("Add 5 to every mark: mean +5, SD same", SLATE), ("Multiply by 2: mean x2, SD x2", SLATE)]):
    f.text(470, 64 + j * 27, t, size=10.5, color=c, anchor="start", bold=(c in (RED, TEAL)))
```

```svgfig label="7.5" caption="Counting outcomes of five coin tosses. The number of ways to get k heads is C(5, k) = 1, 5, 10, 10, 5, 1 out of 2^5 = 32 outcomes (row 5 of Pascal's triangle). So P(exactly 2 heads) = 10/32 = 5/16 and P(at least 3 heads) = (10 + 5 + 1)/32 = 1/2. This is the binomial distribution with n = 5 and p = 1/2."
import math
from fractions import Fraction as F
w = [math.comb(5, k) for k in range(6)]; assert w == [1, 5, 10, 10, 5, 1] and sum(w) == 32
assert F(w[2], 32) == F(5, 16) and F(sum(w[3:]), 32) == F(1, 2) and F(1, 32) == F(w[0], 32)
f = Fig(780, 300)
for k in range(6):
    x = 40 + k * 70; h = 14 + w[k] * 15
    f.box(x, 230 - h, 56, h, str(w[k]), fill=("#bbf7d0" if k >= 3 else "#bfdbfe"), stroke=NAVY, size=12, bold=True, r=2)
    f.text(x + 28, 252, "%d heads" % k, size=10.5, color=SLATE, bold=True); f.text(x + 28, 270, "%d/32" % w[k], size=10, color=NAVY)
f.text(220, 22, "Ways to get k heads in 5 tosses", size=11.5, color=NAVY, bold=True)
f.text(620, 60, "P(exactly 2 heads) = 10/32 = 5/16", size=11, color=NAVY, bold=True)
f.text(620, 96, "P(at least 3 heads) = 16/32 = 1/2", size=11, color=TEAL, bold=True)
f.text(620, 132, "P(no head) = 1/32", size=11, color=SLATE, bold=True)
f.text(620, 168, "P(at least one head) = 1 - 1/32 = 31/32", size=11, color=RED, bold=True)
f.text(620, 214, "Use the complement for 'at least one'", size=10.5, color=SLATE)
```

## 7.4 Eight traps in counting, probability and statistics

These questions are short but unforgiving, because one wrong rule changes the answer completely. The eight traps below are the usual cause, and each is tested in the figures above.

1. **"And" multiplies, "or" adds.** If a girl can choose from 3 shirts and 4 skirts, there are $3\times4=12$ outfits. If she picks either a shirt or a skirt, there are $3+4=7$ choices. The fundamental principle works only when the choices are independent stages.
2. **Order matters for permutations only.** Choosing a president and a secretary from 5 is $P(5,2)=20$, but choosing a committee of 2 is $C(5,2)=10$ (Fig 7.1). Use the formulas $P(n,r)=\frac{n!}{(n-r)!}$ and $C(n,r)=\frac{P(n,r)}{r!}$, and remember $C(n,r)=C(n,n-r)$.
3. **Repeated letters need division.** The word BANANA has 6 letters with A three times and N twice, so the arrangements are $\frac{6!}{3!\,2!}=60$, not 720. For people around a round table the count is $(n-1)!$, because rotations are the same. Always check for repeats before writing $n!$.
4. **Treat "together" as a block, and subtract for "never together".** If two particular people must sit together in a row of 5, glue them: $4!\times2!=48$. If they must not sit together, the count is $5!-48=72$. For numbers made from digits, the first digit cannot be 0.
5. **A probability lies between 0 and 1.** The sample space of two dice has $6\times6=36$ outcomes, not 12, and three coin tosses have $2^3=8$ outcomes (Fig 7.2). Use $P(A')=1-P(A)$. An answer such as $\frac{7}{6}$ is always wrong.
6. **Add the overlap back out.** $P(A\cup B)=P(A)+P(B)-P(A\cap B)$, as in the card example $\frac{13}{52}+\frac4{52}-\frac1{52}=\frac4{13}$ (Fig 7.3). Mutually exclusive events have $P(A\cap B)=0$, so the last term vanishes. For "at least one", compute $1-P(\text{none})$.
7. **Independent is not the same as mutually exclusive.** Independent events satisfy $P(A\cap B)=P(A)P(B)$, while mutually exclusive events cannot happen together. Drawing two cards without replacement makes the draws dependent, so the second probability changes. Conditional probability is $P(A|B)=\frac{P(A\cap B)}{P(B)}$.
8. **Sort first, and know what an outlier does.** The median is the middle value of the sorted list, or the average of the two middle values when $n$ is even (Fig 7.4). One extreme value moves the mean a lot but the median not at all. The variance is the mean of squared deviations, $\sigma=\sqrt{\text{variance}}$, adding a constant to every mark leaves the SD unchanged, and multiplying by $k$ multiplies it by $k$.

### 7.4.1 Worked checks

**Q. A committee of 3 is chosen from 5 men and 4 women. In how many ways does it contain at least one woman?**

**Answer.** Total committees $=C(9,3)=84$. Committees with no woman $=C(5,3)=10$. So at least one woman: $84-10=74$. Using the complement avoids three separate cases.

**Q. Two dice are thrown. Find the probability that the sum is 7 or the dice show a double.**

**Answer.** Sum 7 has 6 outcomes and doubles have 6, but no double sums to 7 (an odd total), so the overlap is 0. $P=\frac{6+6}{36}=\frac13$. Fig 7.2 shows both sets of cells.

**Q. For the marks 4, 5, 5, 6, 7, 8, 8, 8, 9, 10 find the mean, median, mode and standard deviation.**

**Answer.** Mean $=\frac{70}{10}=7$. The median is the average of the 5th and 6th values, $\frac{7+8}{2}=7.5$. The mode is 8. The squared deviations add to 34, so the variance is 3.4 and $\sigma=\sqrt{3.4}=1.84$.

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
