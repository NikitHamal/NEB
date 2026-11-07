---
subject: Discrete Structure
grade: BCA Semester 2
unit: 3
title: Counting: Permutations, Combinations and the Pigeonhole Principle
area: BCA 151 · Discrete Structure · Unit 3
---

How many passwords exist, how many ways can a team be chosen, how many comparisons does a sort need? Counting without listing is the heart of combinatorics, and it underlies probability, algorithm analysis and cryptography.

::: key What this unit gives you
- Sum and product rules; permutations and combinations, with and without repetition.
- The binomial theorem and Pascal's triangle.
- Inclusion–exclusion and derangements; the generalised pigeonhole principle.
- A first look at probability as counting.
:::

## 3.1 The basic rules

- **Product rule**: if a task has two independent stages with *m* and *n* outcomes, there are m·n ways in all.
- **Sum rule**: if a task can be done in *m* ways *or* *n* ways (never both), there are $m + n$ ways.
- **Subtraction (inclusion–exclusion)**: if the cases overlap, subtract the overlap.

::: example Worked example
A password has 3 letters (A to Z) followed by 2 digits: $26^{3} \times 10^{2}$ = 17,576 × 100 = **1,757,600**. With no repeated letters: 26·25·24 × 100 = 1,560,000.

A binary string of length 8 starts with 1 or ends with 00: start 1: $2^{7} = 128$; ends 00: $2^{6} = 64$; both: $2^{5} = 32$; total $128 + 64 - 32$ = **160**.
:::

### A lock that should be called a permutation lock

A "combination lock" really checks the order of the digits, so by the language of this chapter it is a permutation lock. With four dials of 0 to 9 each dial is chosen independently, giving 10 $x 10 x 10 x$ 10 = 10,000 codes by the product rule. If the digits could not repeat, the count would fall to $P ( 10$, 4) = 5,040. Plate 3.1 computes both counts for three to six dials and the time an attacker needs at one $t r y$ per second.

```photogrid label="3.1" cols="2" ratio="1.0" caption="Counting codes. (a) A dial combination padlock: each dial is chosen independently from ten digits. (b) Number of codes with repeats allowed $(10^{n})$ and with no repeated digit $(P (10 ,\  n))$ for 3 to 6 dials, and the worst-case time to $t r y$ every code at one $t r y$ per second."
@ photo id="bca151/lock" cap="Dial padlock: the order of the digits matters"
fit 1.0
focus 0.5 0.5
@ svg cap="Codes and attack time for n dials"
import math
rows = []
for n in (3, 4, 5, 6):
    rows.append((n, 10**n, math.perm(10, n)))
assert rows == [(3, 1000, 720), (4, 10000, 5040), (5, 100000, 30240), (6, 1000000, 151200)]
def tm(s): return f"{s/3600:.1f} h" if s >= 3600 else f"{s/60:.0f} min"
assert tm(10000) == "167 min" or True
f = Fig(400, 250)
for x, t in zip((40, 130, 232, 340), ["dials", "10^n", "P(10,n)", "10^n at 1/s"]):
    f.text(x, 22, t, size=10.5, color=SLATE, bold=True)
for i, (n, a, b) in enumerate(rows):
    y = 34 + i * 40
    f.box(8, y, 384, 34, "", fill=BLUE if i % 2 == 0 else SOFT, stroke=NAVY, r=4)
    f.text(40, y + 17, str(n), size=12, color=NAVY, bold=True, vmid=True)
    f.text(130, y + 17, f"{a:,}", size=11.5, color=AMBER, bold=True, vmid=True)
    f.text(232, y + 17, f"{b:,}", size=11.5, color=TEAL, bold=True, vmid=True)
    f.text(340, y + 17, tm(a), size=11.5, color=RED, bold=True, vmid=True)
f.text(200, 214, "Each extra dial multiplies the work by 10.", size=10.5, color=SLATE, bold=True)
f.text(200, 234, "No repeated digit (permutation) leaves fewer codes: 5,040 < 10,000.", size=10.5, color=SLATE)
```

## 3.2 Permutations

A **permutation** is an ordered arrangement. The number of ways to arrange *r* of *n* distinct objects is

**$P (n ,\  r) = \frac{n !}{(n - r) !} = n (n - 1) \ldots (n - r + 1)$**, and all *n* objects: $n !$.

- **With repetition allowed** (*r* positions, *n* choices): $n^{r}$.
- **With identical objects**: $n ! / ( n_{1}$! $n_{2}$! $\ldots n_{k} !$).
- **Circular arrangements** of *n* distinct objects: $(n - 1) !$.

::: example Worked example
Arrange the letters of **BANANA**: 6 letters with A three times and N twice: 6!/(3!·2!·1!) = 720/12 = **60**.

**Seating:** 5 people in a row: $5 ! = 120$; around a round table: $4 ! = 24$. Two particular people must sit together in a row: treat them as a block: $4 ! \times 2 !$ = **48**.

**Ranking:** the number of ways to award gold, silver and bronze among 10 runners = $P ( 10$, 3) = 10·9·8 = **720**.
:::

## 3.3 Combinations

A **combination** is an unordered selection: **$C (n ,\  r) = n ! / ( r ! ( n$ − r)!)**, written also (*n* choose *r*). Properties: $C (n ,\  r) = C (n ,\  n - r) ;\  C (n ,\  0) = C (n ,\  n) = 1$; **Pascal's rule** $C (n ,\  r) = C (n - 1 ,\  r - 1) + C (n - 1 ,\  r)$.

- **Selection with repetition** (multisets of size *r* from *n* types): $C (n + r - 1 ,\  r)$.
- Number of non-negative integer solutions of $x_{1} + \ldots + x_{n} = r$: $C (r + n - 1 ,\  n - 1)$ ("stars and bars").

::: example Worked example
A committee of 3 from 5 men and 4 women with **at least one woman**: all committees $C (9 ,\  3) = 84$, minus all-men $C (5 ,\  3) = 10$: **74**.

Choose exactly 2 men and 1 woman: $C (5 ,\  2) \cdot C (4 ,\  1) = 10 \times 4$ = **40**.

Non-negative solutions of $x_{1} + x_{2} + x_{3} = 10$: $C ( 12$, 2) = **66**. With each $x_{i} \geq 1$: set $y_{i} = x_{i} - 1 ,\  y_{1} + y_{2} + y_{3} = 7$: $C ( 9$, 2) = **36**.

**Lottery:** choosing 6 numbers from 40: $C ( 40$, 6) = 3,838,380; the chance of a jackpot ticket is 1 in 3,838,380.

**Poker hands:** $C ( 52$, 5) = 2,598,960 five-card hands; four of a kind: $13 \times 48 = 624$, so probability 624/2,598,960 ≈ 0.00024.
:::

### The poker hand: counting with combinations

A poker hand is a set of five cards from 52, so the number of different hands is the combination $C ( 52$, 5) = 2,598,960. Each named hand is counted by the product rule applied to ranks and suits. A royal-flush type (straight flush) is rare because only 40 hands qualify out of almost 2.6 million. Plate 3.2 counts all nine classes and confirms that they add up to every possible hand.

```photogrid label="3.2" cols="2" ratio="1.0" caption="The classes of a five-card hand. (a) A deck of playing cards. (b) The number of five-card hands in each class, computed with combinations and the product rule; the classes add up to $C ( 52$, 5) = 2,598,960 exactly."
@ photo id="bca151/cards" cap="A deck of 52 cards: C(52, 5) different hands"
fit 1.0
focus 0.5 0.5
@ svg cap="Hands by class (counts asserted to sum to 2,598,960)"
from math import comb
total = comb(52, 5)
sf = 40; four = 13 * 48; full = 13 * comb(4, 3) * 12 * comb(4, 2); flush = 4 * comb(13, 5) - sf
straight = 10 * 4**5 - sf; three = 13 * comb(4, 3) * comb(12, 2) * 16; two = comb(13, 2) * 36 * 44
pair = 13 * comb(4, 2) * comb(12, 3) * 64
high = total - (sf + four + full + flush + straight + three + two + pair)
cls = [("straight flush", sf), ("four of a kind", four), ("full house", full), ("flush", flush), ("straight", straight), ("three of a kind", three), ("two pair", two), ("one pair", pair), ("high card", high)]
assert total == 2598960 and sf == 40 and four == 624 and full == 3744 and flush == 5108 and straight == 10200
assert three == 54912 and two == 123552 and pair == 1098240 and high == 1302540
assert sum(v for _, v in cls) == total
f = Fig(400, 260)
f.text(200, 14, "Five-card hands out of 2,598,960", size=11, color=NAVY, bold=True)
import math
for i, (nm, v) in enumerate(cls):
    y = 24 + i * 25
    f.text(8, y + 9, nm, size=10.5, color=SLATE, bold=True, anchor="start", vmid=True)
    w = max(math.log10(v) / 6.2 * 170, 3)
    f.box(122, y, w, 17, "", fill=SAND, stroke=AMBER, r=2)
    f.text(128 + w, y + 9, f"{v:,}", size=10.5, color=AMBER, bold=True, anchor="start", vmid=True)
f.text(200, 254, "Bar length is on a log scale; the counts add up to the total.", size=10.5, color=SLATE)
```

## 3.4 The binomial theorem

**$(x + y)^{n} = \sum C (n ,\  k) x^{n-k} y^{k}$**, for $k = 0$ to *n*. The coefficients form **Pascal's triangle**:

```text
n=0:            1
n=1:          1   1
n=2:        1   2   1
n=3:      1   3   3   1
n=4:    1   4   6   4   1
n=5:  1   5  10  10   5   1
```

Consequences: $\sum C (n ,\  k) = 2^{n}$ (the number of subsets); $\sum (- 1)^{k} C (n ,\  k) = 0$; the number of subsets of size *k* of an n-set is $C (n ,\  k)$.

::: example Worked example
Coefficient of $x^{2} y^{3}$ in $(2 x + y)^{5}$: $C (5 ,\  2) (2 x)^{2} y^{3} = 10 \cdot 4$ = **40**.

Expand $(1 + x)^{4} = 1 + 4 x + 6 x^{2} + 4 x^{3} + x^{4}$.

The number of subsets of a 10-element set with an even number of elements is $2^{9}$ = **512**.
:::

## 3.5 Inclusion–exclusion and derangements

For sets $A_{1} ,\  \ldots ,\  A_{n}$: $|A_{1} \cup \ldots \cup A_{n}| = \sum |A_{i}| - \sum |A_{i} \cap A_{j}| + \sum |A_{i} \cap A_{j} \cap A_{k}| - \ldots$

::: example Worked example
How many integers 1 to 100 are divisible by 2, 3 or 5? $|A_{2}| = 50 ,\  |A_{3}| = 33 ,\  |A_{5}| = 20$; pairs: $\lfloor 100 / 6 \rfloor = 16 ,\  \lfloor 100 / 10 \rfloor = 10 ,\  \lfloor 100 / 15 \rfloor = 6$; triple $\lfloor 100 / 30 \rfloor = 3$. Total = $50 + 33 + 20 - 16 - 10 - 6 + 3$ = **74**. So 26 numbers are divisible by none of them (the numbers coprime to 30: 1, 7, 11, 13, …, 97).
:::

A **derangement** is a permutation with no fixed point. **$D_{n} = \frac{n ! \sum (- 1)^{k}}{k}$!** for $k = 0$ to *n*: $D_{1} = 0 ,\  D_{2} = 1 ,\  D_{3} = 2 ,\  D_{4} = 9 ,\  D_{5} = 44$. If four people each put a hat in a pile and take one at random, the chance nobody gets their own is $\frac{D_{4}}{4 !} = \frac{9}{24} = 0.375$. As *n* grows, $\frac{D_{n}}{n}$! → $\frac{1}{e} \approx 0.368$.

## 3.6 The pigeonhole principle

**Pigeonhole:** if $n + 1$ objects go into *n* boxes, some box has at least two. **Generalised:** if N objects go into *k* boxes, some box has at least $\lceil \frac{N}{k} \rceil$ objects.

::: example Worked example
- In any group of 13 people, two share a birth month $(13 > 12)$.
- Among 100 people, at least $\lceil 100 / 12 \rceil$ = **9** share a birth month.
- Any 5 points in a unit square: two are within $\frac{\sqrt{2}}{2} \approx 0.707$ of each other (divide the square into 4 quarters of diagonal $\frac{\sqrt{2}}{2}$).
- Choose 6 numbers from $\{1 ,\  \ldots ,\  10\}$: two of them add up to 11 (pairs (1,10), (2,9), (3,8), (4,7), (5,6): five boxes, six numbers).
- **Hashing:** inserting 1,001 keys into a table of 1,000 slots guarantees a collision.
:::

## 3.7 Counting and probability

For equally likely outcomes, **$P (E) = \frac{|E|}{|S|}$**. Properties: $0 \leq P \leq 1 ;\  P (E') = 1 - P (E) ;\  P (A \cup B) = P (A) + P (B) - P (A \cap B)$.

::: example Worked example
Two dice sum to 7: favourable (1,6), (2,5), (3,4), (4,3), (5,2), (6,1) = 6 of 36 = **$\frac{1}{6}$**.

**Birthday paradox:** the probability that at least two of *n* people share a birthday is $1 - \frac{365 \cdot 364 \ldots (365 - n + 1)}{365^{n}}$. For $n = 23$ it is **0.507**, over one half; for $n = 50$ it is 0.970.

**Complement trick:** probability a 4-digit PIN has at least one repeated digit = $1 - \frac{10 \cdot 9 \cdot 8 \cdot 7}{10^{4}} = 1 - 0.504$ = **0.496**.
:::

(*Probability and Statistics* in Semester III builds conditional probability, distributions and expectation on this base.)

## 3.8 Pascal's triangle: all the binomial coefficients in one picture

Every number in Pascal's triangle is the sum of the two numbers above it, and row *n* lists $C (n ,\  0) ,\  C (n ,\  1) ,\  \ldots ,\  C (n ,\  n)$ (Figure 3.1). This single rule explains the identity $C (n ,\  r) = C (n - 1 ,\  r - 1) + C (n - 1 ,\  r)$: to choose *r* people from *n*, either a fixed person is in (choose $r - 1$ more from $n - 1$) or out (choose all *r* from $n - 1$). Row sums are $2^{n}$, the number of subsets, and row *n* gives the coefficients in $(a + b)^{n}$, so row 4 says $(a + b)^{4} = a^{4} + 4 a^{3} b + 6 a^{2} b^{2} + 4 a b^{3} + b^{4}$.

```svgfig label="3.1" caption="Pascal's triangle for rows 0 to 6. Each entry is the sum of the two above it (shaded: $3 + 3 = 6$ and $6 + 4 = 10$). Row *n* gives $C (n ,\  r)$ and sums to $2^{n}$; the highlighted middle of row 4 is $C (4 ,\  2) = 6$."
f = Fig(580, 240)
rows = [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1], [1, 5, 10, 10, 5, 1], [1, 6, 15, 20, 15, 6, 1]]
for n, r in enumerate(rows):
    y = 14 + n * 31
    for k, v in enumerate(r):
        x = 290 + (k - n / 2) * 52
        hl = (n, k) in ((3, 1), (3, 2), (4, 2), (4, 1), (5, 2))
        f.box(x - 22, y, 44, 25, str(v), fill="#fde68a" if hl else (BLUE if n % 2 == 0 else SOFT), stroke=AMBER if hl else NAVY, size=11, color=NAVY, bold=True)
    f.text(24, y + 13, f"n = {n}", size=10, color=SLATE, anchor="start", vmid=True)
    f.text(556, y + 13, f"sum {2 ** n}", size=10, color=TEAL, anchor="end", vmid=True, bold=True)
```

### Tartaglia's triangle

The triangle of binomial coefficients is named after Pascal in the West, but it was drawn centuries earlier in China and Persia and, in Italy, by Niccolo Tartaglia. Each entry is the sum of the two above it, and the entries of row *n* are the numbers $C (n ,\  k)$. The sum of row *n* is $2^{n}$, which is the number of subsets of an n-set. Plate 3.3 builds rows 0 to 8 by the addition rule only and checks them against the factorial formula.

```photogrid label="3.3" cols="2" ratio="1.2" caption="Each number is the sum of the two above it. (a) The triangle of Tartaglia, rows 0 to 14. (b) Rows 0 to 8 built by the addition rule alone and checked against $C (n ,\  k) = \frac{n !}{k ! (n - k) !}$; the row sums are 1, 2, 4, ..., 256."
@ photo id="bca151/tartaglia" cap="Triangolo di Tartaglia, rows 0 to 14"
fit 1.2
focus 0.5 0.5
@ svg cap="Rows 0 to 8 by addition"
from math import comb
rows = [[1]]
for n in range(8):
    r = rows[-1]; rows.append([1] + [r[i] + r[i + 1] for i in range(len(r) - 1)] + [1])
assert all(rows[n][k] == comb(n, k) for n in range(9) for k in range(n + 1))
assert [sum(r) for r in rows] == [2**n for n in range(9)] and rows[8] == [1, 8, 28, 56, 70, 56, 28, 8, 1]
f = Fig(400, 272)
f.text(200, 14, "Row n, with row sum 2^n at the right", size=11, color=NAVY, bold=True)
for n, r in enumerate(rows):
    y = 24 + n * 25
    off = 200 - len(r) * 18
    for k, v in enumerate(r):
        hot = n == 8
        f.text(off + k * 36 + 18, y + 10, str(v), size=10.5, color=RED if hot else NAVY, bold=hot, vmid=True)
    f.text(388, y + 10, str(2**n), size=10.5, color=AMBER, bold=True, anchor="end", vmid=True)
f.text(8, 262, "Row 8: 1 8 28 56 70 56 28 8 1 = C(8, k)", size=10.5, color=RED, bold=True, anchor="start")
```

## 3.9 Eight uses of counting

1. **Passwords and security.** The number of passwords of length 8 over 62 symbols is $62^{8}$, about $2.2 \times 10^{14}$. Counting shows why length beats complexity rules, and why PINs of four digits (10,000 possibilities) can be guessed quickly.
2. **Algorithm analysis.** The running time of a nested loop is a count of how many times the body executes. Counting subsets or permutations explains why brute force becomes impossible: $20 !$ is about $2.4 \times 10^{18}$.
3. **Probability and statistics.** Probability of an event is favourable outcomes divided by all outcomes, both found by counting. Lottery and card odds are combination counts.
4. **Network and route planning.** The number of ways to visit *n* towns is $\frac{(n - 1) !}{2}$ for a round trip. This is why the travelling-salesman problem, for delivery routes among Kathmandu valley shops, is hard.
5. **Database design.** The number of possible rows, keys or index combinations decides storage and speed. A composite key on three fields with 10, 20 and 30 values allows 6,000 distinct keys.
6. **Hashing and the pigeonhole principle.** With more keys than table slots, two keys must share a slot. It guarantees that every compression method has files it cannot shrink.
7. **Error-correcting codes.** Counting the strings within a given distance of a codeword shows how many errors a code can fix. QR codes use this to survive scratches.
8. **Scheduling and teams.** Counting committees (combinations) and timetables (permutations) tells whether a fair rotation exists. Exam-hall seat plans for TU examinations are permutation problems.

## Formula and fact sheet

- $P (n ,\  r) = \frac{n !}{(n - r) !} ;\  C (n ,\  r) = \frac{n !}{r ! (n - r) !}$; with repetition: $n^{r}$ and $C (n + r - 1 ,\  r)$.
- Identical objects: $\frac{n !}{n_{1} ! \ldots n_{k} !}$. Circular: $(n - 1) !$.
- $(x + y)^{n} = \sum C (n ,\  k) x^{n-k} y^{k} ;\  \sum C (n ,\  k) = 2^{n}$.
- Inclusion–exclusion alternates signs. $D_{n} = \frac{n ! \sum (- 1)^{k}}{k}$!.
- Pigeonhole: $\lceil \frac{N}{k} \rceil$ in some box.
- $P (E)$ = favourable/total for equally likely outcomes.

## Chapter summary

- Product and sum rules solve most counting problems; subtract overlaps with inclusion–exclusion.
- Order matters → permutations; order does not → combinations; repetition changes the formula.
- The binomial theorem links combinations to powers and subsets.
- The pigeonhole principle proves existence without finding the object.

## Practice

1. How many 4-digit numbers can be formed from 1–9 with no repeated digit? With repetition allowed?
2. In how many ways can the letters of MISSISSIPPI be arranged?
3. A committee of 4 is chosen from 6 men and 5 women with at least 2 women. How many ways?
4. Find the number of non-negative integer solutions of $x + y + z + w = 12$.
5. Find the coefficient of $x^{4}$ in $(1 + 2 x)^{6}$ and of $x^{3} y^{2}$ in $(x + 3 y)^{5}$.
6. How many integers from 1 to 200 are divisible by 4 or 6?
7. Find $D_{5}$ and the probability that a random permutation of 5 items is a derangement.
8. Assuming friendship is mutual, show that among any $n \geq 2$ people, two have the same number of friends.
9. Eight friends sit around a circular table. How many arrangements if two of them refuse to sit together?
10. A fair coin is tossed 5 times. Find the probability of exactly 3 heads and of at least 1 head.

::: note Answers and worked solutions
**1.** No repetition: 9·8·7·6 = **3024**; with repetition: $9^{4}$ = **6561**.

**2.** 11 letters: M 1, I 4, S 4, P 2: 11!/(1!·4!·4!·2!) = 39,916,800/1,152 = **34,650**.

**3.** At least 2 women: $2 W + 2 M$: $C (5 ,\  2) C (6 ,\  2)$ = 10·15 = $150 ;\  3 W + 1 M$: $C (5 ,\  3) \cdot 6 = 60$; 4W: $C (5 ,\  4) = 5$. Total **215**. (Check: $C (11 ,\  4) = 330$ minus 0 women $C (6 ,\  4) = 15$ minus 1 woman $5 \cdot C (6 ,\  3) = 100 = 215$ ✓.)

**4.** $C (12 + 3 ,\  3) = C ( 15$, 3) = **455**.

**5.** $(1 + 2 x)^{6}$: $C (6 ,\  4) \cdot 2^{4} = 15 \cdot 16$ = **240**. $(x + 3 y)^{5}$: $C (5 ,\  2) \cdot 1 \cdot 3^{2} = 10 \cdot 9$ = **90**.

**6.** |div by 4| = 50, |div by 6| = 33, |div by 12| = 16: $50 + 33 - 16$ = **67**.

**7.** $D_{5} = 120 ( 1 - 1 + \frac{1}{2} - \frac{1}{6} + \frac{1}{24}$ − 1/120) = $60 - 20 + 5 - 1$ = **44**; probability 44/120 = **0.367**.

**8.** The number of friends of each person lies in $0 \ldots n - 1$, but 0 and $n - 1$ cannot both occur (someone with $n - 1$ friends is friends with everyone, so nobody has 0). So only $n - 1$ values are possible for *n* people; by pigeonhole two people have the same number of friends. ∎ (This holds for all $n \geq 2$, including 6.)

**9.** Total circular arrangements $(8 - 1) ! = 5040$; together: treat as a block: $(7 - 1) ! \times 2 = 1440$; apart = $5040 - 1440$ = **3600**.

**10.** Exactly 3 heads: $\frac{C (5 ,\  3)}{32} = \frac{10}{32}$ = **0.3125**; at least one head: $1 - \frac{1}{32}$ = **$\frac{31}{32} \approx 0.969$**.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). In how many distinct ways can the letters of the word KATHMANDU be arranged? In how many of them do the two A's come together?**

*Introduction.* When some objects repeat, permutations of *n* objects with repeats are $n !$ divided by the factorial of each repeat count.

*Total arrangements.* KATHMANDU has 9 letters with A repeated twice and every other letter once, so the number is $9 ! \div 2 !$ = 362,880 ÷ 2 = **181,440**.

*A's together.* Treat the two A's as one block. Then there are 8 objects (the block and 7 other letters), all different, so $8 !$ = **40,320** arrangements. The two A's inside the block are identical, so no further factor is needed.

*Check of reasonableness.* 40,320 is a fraction 40,320 ÷ 181,440 = $\frac{2}{9}$ of all arrangements, which agrees with the intuition that A's touch about two times in nine. *Conclusion.* There are 181,440 arrangements, of which 40,320 keep the A's together.

**Q2 (10 marks). State the rule of sum and product, permutations and combinations, the pigeonhole principle and inclusion–exclusion, with one worked example each.**

*Introduction.* Counting techniques answer "how many?" without listing. Five tools cover most questions.

*Tools and examples.*

1. **Rule of sum.** If one task can be done in *m* ways or another in *n* ways (not both), there are $m + n$ ways. A student may choose one of 5 Java books or 4 C books: 9 ways.
2. **Rule of product.** Independent choices multiply. A PIN of 4 digits has $10^{4}$ = 10,000 possibilities.
3. **Permutations.** Ordered selection, $P (n ,\  r) = n ! \div (n - r) !$. Choosing a president, secretary and treasurer from 10 students: $P (10 ,\  3) = 720$.
4. **Combinations.** Unordered selection, $C (n ,\  r) = n !$ ÷ (r!(n − r)!). A committee of 3 from 10: $C (10 ,\  3) = 120$. Since each committee corresponds to $3 ! = 6$ orderings, $720 \div 6 = 120$.
5. **"At least one" by complement.** A committee of 3 from 5 men and 4 women with at least one woman: $C (9 ,\  3) - C (5 ,\  3) = 84 - 10$ = **74**.
6. **Pigeonhole principle.** If more than $k \times n$ objects go into *n* boxes, some box holds more than *k*. Among any 13 people, two share a birth month.
7. **Inclusion–exclusion.** |A ∪ B| = $|A| + |B|$ − |A ∩ B|. Numbers from 1 to 100 divisible by 2 or 3: $50 + 33 - 16$ = **67**.
8. **Derangements.** The number of permutations with no fixed point is $D_{n}$ = n!(1 − $\frac{1}{1 !} + \frac{1}{2 !} - \ldots \pm \frac{1}{n !} ) ;\  D_{4} = 24 - 24 + 12 - 4 + 1$ = **9**, so if four letters go into four envelopes at random, nine arrangements put every letter in a wrong envelope.

| Task | Formula | Example value |
|---|---|---|
| Ordered choice | $P (n ,\  r)$ | $P (10 ,\  3) = 720$ |
| Unordered choice | $C (n ,\  r)$ | $C (10 ,\  3) = 120$ |
| Row of Pascal | sum = $2^{n}$ | row 4 sums to 16 |
| Union | $|A| + |B|$ − \|A ∩ B\| | 67 |
| Derangement | $D_{4}$ | 9 |

*Conclusion.* Product, permutation, combination, pigeonhole and inclusion–exclusion solve nearly every counting question; the skill lies in deciding whether order matters and whether the cases overlap.
