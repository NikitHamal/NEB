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

- **Product rule**: if a task has two independent stages with m and n outcomes, there are m·n ways in all.
- **Sum rule**: if a task can be done in m ways *or* n ways (never both), there are m + n ways.
- **Subtraction (inclusion–exclusion)**: if the cases overlap, subtract the overlap.

::: example Worked example
A password has 3 letters (A to Z) followed by 2 digits: 26³ × 10² = 17,576 × 100 = **1,757,600**. With no repeated letters: 26·25·24 × 100 = 1,560,000.
A binary string of length 8 starts with 1 or ends with 00: start 1: 2⁷ = 128; ends 00: 2⁶ = 64; both: 2⁵ = 32; total 128 + 64 − 32 = **160**.
:::

## 3.2 Permutations

A **permutation** is an ordered arrangement. The number of ways to arrange r of n distinct objects is

**P(n, r) = n!/(n − r)! = n(n − 1)…(n − r + 1)**, and all n objects: n!.

- **With repetition allowed** (r positions, n choices): nʳ.
- **With identical objects**: n!/(n₁! n₂! … nₖ!).
- **Circular arrangements** of n distinct objects: (n − 1)!.

::: example Worked example
Arrange the letters of **BANANA**: 6 letters with A three times and N twice: 6!/(3!·2!·1!) = 720/12 = **60**.
**Seating:** 5 people in a row: 5! = 120; around a round table: 4! = 24. Two particular people must sit together in a row: treat them as a block: 4! × 2! = **48**.
**Ranking:** the number of ways to award gold, silver and bronze among 10 runners = P(10, 3) = 10·9·8 = **720**.
:::

## 3.3 Combinations

A **combination** is an unordered selection: **C(n, r) = n!/(r!(n − r)!)**, written also (n choose r). Properties: C(n, r) = C(n, n − r); C(n, 0) = C(n, n) = 1; **Pascal's rule** C(n, r) = C(n − 1, r − 1) + C(n − 1, r).

- **Selection with repetition** (multisets of size r from n types): C(n + r − 1, r).
- Number of non-negative integer solutions of x₁ + … + xₙ = r: C(r + n − 1, n − 1) ("stars and bars").

::: example Worked example
A committee of 3 from 5 men and 4 women with **at least one woman**: all committees C(9, 3) = 84, minus all-men C(5, 3) = 10: **74**.
Choose exactly 2 men and 1 woman: C(5, 2)·C(4, 1) = 10 × 4 = **40**.
Non-negative solutions of x₁ + x₂ + x₃ = 10: C(12, 2) = **66**. With each xᵢ ≥ 1: set yᵢ = xᵢ − 1, y₁ + y₂ + y₃ = 7: C(9, 2) = **36**.
**Lottery:** choosing 6 numbers from 40: C(40, 6) = 3,838,380; the chance of a jackpot ticket is 1 in 3,838,380.
**Poker hands:** C(52, 5) = 2,598,960 five-card hands; four of a kind: 13 × 48 = 624, so probability 624/2,598,960 ≈ 0.00024.
:::

## 3.4 The binomial theorem

**(x + y)ⁿ = Σ C(n, k) xⁿ⁻ᵏ yᵏ**, for k = 0 to n. The coefficients form **Pascal's triangle**:

```text
n=0:            1
n=1:          1   1
n=2:        1   2   1
n=3:      1   3   3   1
n=4:    1   4   6   4   1
n=5:  1   5  10  10   5   1
```

Consequences: Σ C(n, k) = 2ⁿ (the number of subsets); Σ (−1)ᵏ C(n, k) = 0; the number of subsets of size k of an n-set is C(n, k).

::: example Worked example
Coefficient of x²y³ in (2x + y)⁵: C(5, 2)(2x)²y³ = 10 · 4 = **40**.
Expand (1 + x)⁴ = 1 + 4x + 6x² + 4x³ + x⁴.
The number of subsets of a 10-element set with an even number of elements is 2⁹ = **512**.
:::

## 3.5 Inclusion–exclusion and derangements

For sets A₁, …, Aₙ: |A₁ ∪ … ∪ Aₙ| = Σ|Aᵢ| − Σ|Aᵢ ∩ Aⱼ| + Σ|Aᵢ ∩ Aⱼ ∩ Aₖ| − …

::: example Worked example
How many integers 1 to 100 are divisible by 2, 3 or 5? |A₂| = 50, |A₃| = 33, |A₅| = 20; pairs: ⌊100/6⌋ = 16, ⌊100/10⌋ = 10, ⌊100/15⌋ = 6; triple ⌊100/30⌋ = 3. Total = 50 + 33 + 20 − 16 − 10 − 6 + 3 = **74**. So 26 numbers are divisible by none of them (the numbers coprime to 30: 1, 7, 11, 13, …, 97).
:::

A **derangement** is a permutation with no fixed point. **Dₙ = n! Σ (−1)ᵏ/k!** for k = 0 to n: D₁ = 0, D₂ = 1, D₃ = 2, D₄ = 9, D₅ = 44. If four people each put a hat in a pile and take one at random, the chance nobody gets their own is D₄/4! = 9/24 = 0.375. As n grows, Dₙ/n! → 1/e ≈ 0.368.

## 3.6 The pigeonhole principle

**Pigeonhole:** if n + 1 objects go into n boxes, some box has at least two. **Generalised:** if N objects go into k boxes, some box has at least ⌈N/k⌉ objects.

::: example Worked example
- In any group of 13 people, two share a birth month (13 > 12).
- Among 100 people, at least ⌈100/12⌉ = **9** share a birth month.
- Any 5 points in a unit square: two are within √2/2 ≈ 0.707 of each other (divide the square into 4 quarters of diagonal √2/2).
- Choose 6 numbers from {1,…,10}: two of them add up to 11 (pairs (1,10), (2,9), (3,8), (4,7), (5,6): five boxes, six numbers).
- **Hashing:** inserting 1,001 keys into a table of 1,000 slots guarantees a collision.
:::

## 3.7 Counting and probability

For equally likely outcomes, **P(E) = |E|/|S|**. Properties: 0 ≤ P ≤ 1; P(E′) = 1 − P(E); P(A ∪ B) = P(A) + P(B) − P(A ∩ B).

::: example Worked example
Two dice sum to 7: favourable (1,6), (2,5), (3,4), (4,3), (5,2), (6,1) = 6 of 36 = **1/6**.
**Birthday paradox:** the probability that at least two of n people share a birthday is 1 − (365·364…(365 − n + 1))/365ⁿ. For n = 23 it is **0.507**, over one half; for n = 50 it is 0.970.
**Complement trick:** probability a 4-digit PIN has at least one repeated digit = 1 − (10·9·8·7)/10⁴ = 1 − 0.504 = **0.496**.
:::

(*Probability and Statistics* in Semester III builds conditional probability, distributions and expectation on this base.)

## 3.8 Pascal's triangle: all the binomial coefficients in one picture

Every number in Pascal's triangle is the sum of the two numbers above it, and row n lists C(n, 0), C(n, 1), …, C(n, n) (Figure 3.1). This single rule explains the identity C(n, r) = C(n − 1, r − 1) + C(n − 1, r): to choose r people from n, either a fixed person is in (choose r − 1 more from n − 1) or out (choose all r from n − 1). Row sums are 2ⁿ, the number of subsets, and row n gives the coefficients in (a + b)ⁿ, so row 4 says (a + b)⁴ = a⁴ + 4a³b + 6a²b² + 4ab³ + b⁴.

```svgfig label="3.1" caption="Pascal's triangle for rows 0 to 6. Each entry is the sum of the two above it (shaded: 3 + 3 = 6 and 6 + 4 = 10). Row n gives C(n,r) and sums to 2^n; the highlighted middle of row 4 is C(4,2) = 6."
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

## 3.9 Eight uses of counting

1. **Passwords and security.** The number of passwords of length 8 over 62 symbols is 62⁸, about 2.2 × 10¹⁴. Counting shows why length beats complexity rules, and why PINs of four digits (10,000 possibilities) can be guessed quickly.
2. **Algorithm analysis.** The running time of a nested loop is a count of how many times the body executes. Counting subsets or permutations explains why brute force becomes impossible: 20! is about 2.4 × 10¹⁸.
3. **Probability and statistics.** Probability of an event is favourable outcomes divided by all outcomes, both found by counting. Lottery and card odds are combination counts.
4. **Network and route planning.** The number of ways to visit n towns is (n − 1)!/2 for a round trip. This is why the travelling-salesman problem, for delivery routes among Kathmandu valley shops, is hard.
5. **Database design.** The number of possible rows, keys or index combinations decides storage and speed. A composite key on three fields with 10, 20 and 30 values allows 6,000 distinct keys.
6. **Hashing and the pigeonhole principle.** With more keys than table slots, two keys must share a slot. It guarantees that every compression method has files it cannot shrink.
7. **Error-correcting codes.** Counting the strings within a given distance of a codeword shows how many errors a code can fix. QR codes use this to survive scratches.
8. **Scheduling and teams.** Counting committees (combinations) and timetables (permutations) tells whether a fair rotation exists. Exam-hall seat plans for TU examinations are permutation problems.

## Formula and fact sheet

- P(n, r) = n!/(n−r)!; C(n, r) = n!/(r!(n−r)!); with repetition: nʳ and C(n+r−1, r).
- Identical objects: n!/(n₁!…nₖ!). Circular: (n−1)!.
- (x + y)ⁿ = Σ C(n, k) xⁿ⁻ᵏ yᵏ; ΣC(n, k) = 2ⁿ.
- Inclusion–exclusion alternates signs. Dₙ = n!Σ(−1)ᵏ/k!.
- Pigeonhole: ⌈N/k⌉ in some box.
- P(E) = favourable/total for equally likely outcomes.

## Chapter summary

- Product and sum rules solve most counting problems; subtract overlaps with inclusion–exclusion.
- Order matters → permutations; order does not → combinations; repetition changes the formula.
- The binomial theorem links combinations to powers and subsets.
- The pigeonhole principle proves existence without finding the object.

## Practice

1. How many 4-digit numbers can be formed from 1–9 with no repeated digit? With repetition allowed?
2. In how many ways can the letters of MISSISSIPPI be arranged?
3. A committee of 4 is chosen from 6 men and 5 women with at least 2 women. How many ways?
4. Find the number of non-negative integer solutions of x + y + z + w = 12.
5. Find the coefficient of x⁴ in (1 + 2x)⁶ and of x³y² in (x + 3y)⁵.
6. How many integers from 1 to 200 are divisible by 4 or 6?
7. Find D₅ and the probability that a random permutation of 5 items is a derangement.
8. Assuming friendship is mutual, show that among any n ≥ 2 people, two have the same number of friends.
9. Eight friends sit around a circular table. How many arrangements if two of them refuse to sit together?
10. A fair coin is tossed 5 times. Find the probability of exactly 3 heads and of at least 1 head.

::: note Answers and worked solutions
**1.** No repetition: 9·8·7·6 = **3024**; with repetition: 9⁴ = **6561**.
**2.** 11 letters: M 1, I 4, S 4, P 2: 11!/(1!·4!·4!·2!) = 39,916,800/1,152 = **34,650**.
**3.** At least 2 women: 2W+2M: C(5,2)C(6,2) = 10·15 = 150; 3W+1M: C(5,3)·6 = 60; 4W: C(5,4) = 5. Total **215**. (Check: C(11,4) = 330 minus 0 women C(6,4) = 15 minus 1 woman 5·C(6,3) = 100 = 215 ✓.)
**4.** C(12 + 3, 3) = C(15, 3) = **455**.
**5.** (1 + 2x)⁶: C(6,4)·2⁴ = 15 · 16 = **240**. (x + 3y)⁵: C(5,2)·1·3² = 10 · 9 = **90**.
**6.** |div by 4| = 50, |div by 6| = 33, |div by 12| = 16: 50 + 33 − 16 = **67**.
**7.** D₅ = 120(1 − 1 + 1/2 − 1/6 + 1/24 − 1/120) = 60 − 20 + 5 − 1 = **44**; probability 44/120 = **0.367**.
**8.** The number of friends of each person lies in 0…n−1, but 0 and n−1 cannot both occur (someone with n−1 friends is friends with everyone, so nobody has 0). So only n − 1 values are possible for n people; by pigeonhole two people have the same number of friends. ∎ (This holds for all n ≥ 2, including 6.)
**9.** Total circular arrangements (8 − 1)! = 5040; together: treat as a block: (7 − 1)! × 2 = 1440; apart = 5040 − 1440 = **3600**.
**10.** Exactly 3 heads: C(5, 3)/32 = 10/32 = **0.3125**; at least one head: 1 − 1/32 = **31/32 ≈ 0.969**.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). In how many distinct ways can the letters of the word KATHMANDU be arranged? In how many of them do the two A's come together?**

*Introduction.* When some objects repeat, permutations of n objects with repeats are n! divided by the factorial of each repeat count.

*Total arrangements.* KATHMANDU has 9 letters with A repeated twice and every other letter once, so the number is 9! ÷ 2! = 362,880 ÷ 2 = **181,440**.

*A's together.* Treat the two A's as one block. Then there are 8 objects (the block and 7 other letters), all different, so 8! = **40,320** arrangements. The two A's inside the block are identical, so no further factor is needed.

*Check of reasonableness.* 40,320 is a fraction 40,320 ÷ 181,440 = 2/9 of all arrangements, which agrees with the intuition that A's touch about two times in nine. *Conclusion.* There are 181,440 arrangements, of which 40,320 keep the A's together.

**Q2 (10 marks). State the rule of sum and product, permutations and combinations, the pigeonhole principle and inclusion–exclusion, with one worked example each.**

*Introduction.* Counting techniques answer "how many?" without listing. Five tools cover most questions.

*Tools and examples.*

1. **Rule of sum.** If one task can be done in m ways or another in n ways (not both), there are m + n ways. A student may choose one of 5 Java books or 4 C books: 9 ways.
2. **Rule of product.** Independent choices multiply. A PIN of 4 digits has 10⁴ = 10,000 possibilities.
3. **Permutations.** Ordered selection, P(n, r) = n! ÷ (n − r)!. Choosing a president, secretary and treasurer from 10 students: P(10, 3) = 720.
4. **Combinations.** Unordered selection, C(n, r) = n! ÷ (r!(n − r)!). A committee of 3 from 10: C(10, 3) = 120. Since each committee corresponds to 3! = 6 orderings, 720 ÷ 6 = 120.
5. **"At least one" by complement.** A committee of 3 from 5 men and 4 women with at least one woman: C(9, 3) − C(5, 3) = 84 − 10 = **74**.
6. **Pigeonhole principle.** If more than k × n objects go into n boxes, some box holds more than k. Among any 13 people, two share a birth month.
7. **Inclusion–exclusion.** |A ∪ B| = |A| + |B| − |A ∩ B|. Numbers from 1 to 100 divisible by 2 or 3: 50 + 33 − 16 = **67**.
8. **Derangements.** The number of permutations with no fixed point is Dₙ = n!(1 − 1/1! + 1/2! − … ± 1/n!); D₄ = 24 − 24 + 12 − 4 + 1 = **9**, so if four letters go into four envelopes at random, nine arrangements put every letter in a wrong envelope.

| Task | Formula | Example value |
|---|---|---|
| Ordered choice | P(n, r) | P(10, 3) = 720 |
| Unordered choice | C(n, r) | C(10, 3) = 120 |
| Row of Pascal | sum = 2ⁿ | row 4 sums to 16 |
| Union | \|A\| + \|B\| − \|A ∩ B\| | 67 |
| Derangement | D₄ | 9 |

*Conclusion.* Product, permutation, combination, pigeonhole and inclusion–exclusion solve nearly every counting question; the skill lies in deciding whether order matters and whether the cases overlap.
