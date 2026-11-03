---
subject: Discrete Structure
grade: BCA Semester 2
unit: 4
title: Induction, Recursion and Recurrence Relations
area: BCA 151 · Discrete Structure · Unit 4
---

A loop and a recursive function both compute by repeating. Induction proves that such repeated processes are correct; recurrence relations describe how their cost grows. This unit gives you the tools to prove statements for all integers and to solve the recurrences that arise from algorithms.

::: key What this unit gives you
- Mathematical induction (weak and strong), with six proof patterns.
- Recursive definitions and structural induction.
- Linear recurrences: homogeneous and non-homogeneous, with closed forms.
- Divide-and-conquer recurrences and the master theorem.
:::

## 4.1 Mathematical induction

To prove P(n) for all integers n ≥ n₀:

1. **Base case**: prove P(n₀).
2. **Inductive step**: assume P(k) (the **inductive hypothesis**) for an arbitrary k ≥ n₀ and prove P(k + 1).

Then P(n) holds for all n ≥ n₀, like dominoes: the first falls, and each one knocks over the next.

::: example Worked example: sum of the first n integers
Claim: 1 + 2 + … + n = n(n + 1)/2.
*Base:* n = 1: LHS 1, RHS 1·2/2 = 1 ✓.
*Step:* assume 1 + … + k = k(k + 1)/2. Then 1 + … + k + (k + 1) = k(k + 1)/2 + (k + 1) = (k + 1)(k/2 + 1) = (k + 1)(k + 2)/2, which is the formula for n = k + 1. ∎
:::

::: example Worked example: divisibility
Claim: 8ⁿ − 1 is divisible by 7 for n ≥ 1.
*Base:* 8 − 1 = 7 ✓. *Step:* assume 8ᵏ − 1 = 7m. Then 8ᵏ⁺¹ − 1 = 8·8ᵏ − 1 = 8(7m + 1) − 1 = 56m + 7 = 7(8m + 1). ∎
:::

::: example Worked example: an inequality
Claim: 2ⁿ > n² for n ≥ 5.
*Base:* 32 > 25 ✓. *Step:* assume 2ᵏ > k² with k ≥ 5. Then 2ᵏ⁺¹ = 2·2ᵏ > 2k² = k² + k² ≥ k² + 5k > k² + 2k + 1 = (k + 1)² (since k² ≥ 5k and 5k > 2k + 1). ∎
:::

::: example Worked example: sum of odd numbers and a geometric sum
1 + 3 + … + (2n − 1) = n²: base 1 = 1; step: k² + (2k + 1) = (k + 1)². ∎ 
Geometric: 1 + r + … + rⁿ = (rⁿ⁺¹ − 1)/(r − 1) (r ≠ 1): step: (rᵏ⁺¹ − 1)/(r − 1) + rᵏ⁺¹ = (rᵏ⁺¹ − 1 + rᵏ⁺²− rᵏ⁺¹)/(r − 1) = (rᵏ⁺² − 1)/(r − 1). ∎
:::

**Strong induction.** Assume P(j) for **all** j with n₀ ≤ j ≤ k, and prove P(k + 1). Example: every integer n ≥ 2 is a product of primes. If n is prime, done; otherwise n = ab with 2 ≤ a, b < n, and by hypothesis each is a product of primes, so n is too. ∎ Another: any postage of 12 cents or more can be made with 4-cent and 5-cent stamps (base cases 12, 13, 14, 15; for k + 1 ≥ 16 use k − 3, add one 4-cent stamp).

**Common mistakes:** forgetting the base case; assuming what must be proved; using a step that only works for some k; "proving" false statements (all horses are the same colour fails at k = 1 → 2).

## 4.2 Recursive definitions

A **recursive definition** has a **base** and a **recursive rule**.

- Factorial: 0! = 1, (n + 1)! = (n + 1)·n!.
- Fibonacci: F₀ = 0, F₁ = 1, Fₙ = Fₙ₋₁ + Fₙ₋₂ → 0, 1, 1, 2, 3, 5, 8, 13, 21, …
- Sets: the set of strings over {0, 1} with no "00"; well-formed formulas; binary trees (a tree is empty or a root with two subtrees).

**Structural induction** proves properties of recursively defined objects: show the base objects have it, and that each construction rule preserves it. Example: a full binary tree with i internal nodes has i + 1 leaves (base: a single leaf has 0 internal and 1 leaf; joining two trees with i₁, i₂ internal nodes under a new root gives i₁ + i₂ + 1 internal and (i₁ + 1) + (i₂ + 1) = i + 1 leaves).

**Recursion in code.** Every recursive function has a base case and a step that moves toward it:

```c
long fact(int n) { return n <= 1 ? 1 : n * fact(n - 1); }
int fib(int n)   { return n < 2 ? n : fib(n - 1) + fib(n - 2); } /* exponential time */
```

The inductive proof that `fact(n)` returns n! mirrors the code. The naïve `fib` takes about φⁿ calls (φ ≈ 1.618); memoisation reduces it to linear.

## 4.3 Linear recurrence relations

A **recurrence relation** gives aₙ in terms of earlier terms. A **linear homogeneous recurrence of order k with constant coefficients**: aₙ = c₁aₙ₋₁ + … + cₖaₙ₋ₖ.

**Method.** Try aₙ = rⁿ: the **characteristic equation** rᵏ = c₁rᵏ⁻¹ + … + cₖ.

| Roots | General solution (order 2) |
|---|---|
| distinct r₁ ≠ r₂ | aₙ = A r₁ⁿ + B r₂ⁿ |
| repeated r | aₙ = (A + Bn) rⁿ |

Use the initial conditions to find A and B.

::: example Worked example: distinct roots
aₙ = 5aₙ₋₁ − 6aₙ₋₂, a₀ = 1, a₁ = 0. Characteristic r² − 5r + 6 = 0 ⇒ r = 2, 3. aₙ = A·2ⁿ + B·3ⁿ; a₀: A + B = 1; a₁: 2A + 3B = 0 ⇒ B = −2, A = 3. **aₙ = 3·2ⁿ − 2·3ⁿ**. Check: a₂ = 5·0 − 6·1 = −6 and 3·4 − 2·9 = −6 ✓.
:::

::: example Worked example: Fibonacci closed form
r² = r + 1 ⇒ r = (1 ± √5)/2 = φ, ψ. With F₀ = 0, F₁ = 1: **Fₙ = (φⁿ − ψⁿ)/√5** (Binet). F₁₀ = 55.
:::

::: example Worked example: repeated root
aₙ = 4aₙ₋₁ − 4aₙ₋₂, a₀ = 1, a₁ = 3. (r − 2)² = 0 ⇒ aₙ = (A + Bn)2ⁿ; a₀: A = 1; a₁: 2(1 + B) = 3 ⇒ B = 1/2. **aₙ = (1 + n/2)2ⁿ**. Check a₂ = 4·3 − 4·1 = 8 and (1 + 1)·4 = 8 ✓.
:::

**Non-homogeneous** aₙ = (homogeneous part) + f(n): the solution is aₙ = (homogeneous solution) + (one particular solution). For constant f, try a constant; for f(n) = n, try pn + q. Example: aₙ = 2aₙ₋₁ + 1, a₀ = 0: particular aₙ = −1 (since −1 = −2 + 1), homogeneous A·2ⁿ; a₀ = A − 1 = 0 ⇒ **aₙ = 2ⁿ − 1**.

**Modelling.** *Tower of Hanoi:* moving n discs needs Tₙ = 2Tₙ₋₁ + 1, T₁ = 1 ⇒ **Tₙ = 2ⁿ − 1**: 10 discs take 1023 moves; 64 discs take about 1.8 × 10¹⁹. *Compound interest:* Bₙ = 1.05Bₙ₋₁ + 1000 (a yearly deposit). *Bit strings with no two consecutive 0s:* sₙ = sₙ₋₁ + sₙ₋₂, s₁ = 2, s₂ = 3 → 2, 3, 5, 8, 13 (a Fibonacci shift: s₅ = 13). *Counting regions:* n lines in a plane (general position) give Rₙ = Rₙ₋₁ + n, R₀ = 1 ⇒ Rₙ = 1 + n(n + 1)/2.

## 4.4 Divide-and-conquer recurrences

Algorithms that split a problem of size n into **a** subproblems of size n/b plus f(n) extra work satisfy **T(n) = aT(n/b) + f(n)**.

**Master theorem** (for f(n) = Θ(nᵈ)): compare d with log_b a.

| Case | Condition | T(n) |
|---|---|---|
| 1 | d < log_b a | Θ(n^{log_b a}) |
| 2 | d = log_b a | Θ(nᵈ log n) |
| 3 | d > log_b a | Θ(nᵈ) |

| Algorithm | Recurrence | log_b a vs d | Result |
|---|---|---|---|
| Binary search | T(n) = T(n/2) + 1 | log₂1 = 0 = d | Θ(log n) |
| Merge sort | T(n) = 2T(n/2) + n | 1 = 1 | Θ(n log n) |
| Sum or maximum of an array by halving | T(n) = 2T(n/2) + 1 | 1 > 0 | Θ(n) |
| Karatsuba multiplication | T(n) = 3T(n/2) + n | log₂3 ≈ 1.585 > 1 | Θ(n^1.585) |
| Strassen | T(n) = 7T(n/2) + n² | log₂7 ≈ 2.807 > 2 | Θ(n^2.807) |
| Naïve recursive Fibonacci | T(n) = T(n−1) + T(n−2) + 1 | not of this form | Θ(φⁿ) |

::: example Worked example: unrolling merge sort
T(n) = 2T(n/2) + n with n = 2ᵏ: T(n) = 2(2T(n/4) + n/2) + n = 4T(n/4) + 2n = … = 2ᵏT(1) + kn = n·T(1) + n log₂ n. For T(1) = 0: T(n) = n log₂ n. For n = 1024 that is 10,240 comparisons-ish, versus about 10⁶ for an n² method.
:::

## 4.5 The recursion tree of merge sort

A divide-and-conquer recurrence such as T(n) = 2T(n/2) + n can be read from a picture (Figure 4.1). Sorting 8 items splits them into two halves of 4, then four of 2, then eight of 1: that is 3 splits, so the tree has log₂ 8 + 1 = 4 levels. At every level the merging work adds up to n = 8 (each item is touched once), so the total is n per level × (log₂ n + 1) levels, about **n log n**. The same drawing explains why merge sort beats bubble sort (n²) for large n: for n = 1,000,000 it is roughly 20 million steps against a million million.

```svgfig label="4.1" caption="Recursion tree for T(n) = 2T(n/2) + n with n = 8. Each level does n = 8 units of merge work; there are log2(8) + 1 = 4 levels, so the total is about n log n. Leaves are single items, which need no sorting."
f = Fig(580, 230)
lv = [(1, 8), (2, 4), (4, 2), (8, 1)]
for d, (cnt, size) in enumerate(lv):
    y = 20 + d * 50
    w = 540 / cnt
    for i in range(cnt):
        x = 20 + i * w + w / 2
        bw = min(70, w - 8)
        f.box(x - bw / 2, y, bw, 28, f"size {size}" if bw > 50 else str(size), fill=[BLUE, SOFT, "#fde68a", "#bbf7d0"][d], stroke=NAVY, size=10 if bw > 50 else 10, color=NAVY)
        if d < 3:
            for j in (0, 1):
                nx = 20 + (2 * i + j) * (w / 2) + w / 4
                f.line(x, y + 28, nx, y + 50, color=SLATE, sw=1.1)
    f.text(570, y + 14, f"work {cnt} x {size} = 8", size=9.5, color=TEAL, anchor="end", bold=True, vmid=True) if d == 0 else None
f.text(290, 222, "4 levels x 8 units per level = 32 = 8 x log2(8) + 8: order n log n", size=10.5, color=NAVY, bold=True)
```

## 4.6 Eight uses of induction and recursion

1. **Proving programs correct.** A loop invariant is proved by induction on the number of iterations: true before the loop, preserved by each pass. This is how binary search and sorting routines are certified.
2. **Recursive programs.** Factorial, Fibonacci, tree traversal and directory walking are recursive definitions turned into code. Each has a base case and a step that moves toward it, exactly as an induction proof does.
3. **Divide and conquer.** Merge sort, quicksort and fast multiplication split a problem and combine the answers. Their running times are solved from recurrences like Figure 4.1.
4. **Algorithm cost.** The recurrence H(n) = 2H(n − 1) + 1 of the Tower of Hanoi gives 2ⁿ − 1 moves, so 10 disks need 1,023 moves and 64 disks are hopeless. Recurrences predict whether a method will finish in a lifetime.
5. **Data structures.** A binary tree, a linked list and a nested folder are recursive structures: each is either empty or a root with smaller copies. Their algorithms are naturally recursive.
6. **Growth models.** Compound interest on a deposit, population growth and loan balances satisfy a_n = r·a_(n−1) + d. Solving the recurrence gives a formula for any month. Banks in Nepal compute EMIs this way.
7. **Dynamic programming.** Shortest paths, edit distance and knapsack problems build the answer for size n from stored answers for smaller sizes. Spell-checkers and DNA matching use it.
8. **Language and grammars.** Programming-language syntax is defined recursively (an expression is a number or an expression plus an expression). Compilers parse by recursion and check properties by structural induction.

## Formula and fact sheet

- Induction: base case + (P(k) ⇒ P(k + 1)). Strong induction assumes all earlier cases.
- Σi = n(n+1)/2; Σ(2i−1) = n²; Σrⁱ = (rⁿ⁺¹ − 1)/(r − 1).
- Characteristic equation: distinct roots → A r₁ⁿ + B r₂ⁿ; repeated → (A + Bn)rⁿ.
- Hanoi Tₙ = 2ⁿ − 1; Fibonacci Fₙ = (φⁿ − ψⁿ)/√5.
- Master theorem: compare d with log_b a.

## Chapter summary

- Induction proves infinitely many statements with two finite checks; strong induction is the right tool when the step needs several earlier cases.
- Recursive definitions give structures and programs; structural induction proves their properties.
- Linear recurrences are solved through the characteristic equation; non-homogeneous ones add a particular solution.
- The master theorem gives the cost of divide-and-conquer algorithms at a glance.

## Practice

1. Prove by induction: 1² + 2² + … + n² = n(n + 1)(2n + 1)/6.
2. Prove: 3 divides n³ − n for all n ≥ 1 (induction, or factorisation).
3. Prove: 2ⁿ ≥ n + 1 for all n ≥ 0.
4. Solve aₙ = 3aₙ₋₁ − 2aₙ₋₂ with a₀ = 2, a₁ = 3.
5. Solve aₙ = 6aₙ₋₁ − 9aₙ₋₂, a₀ = 1, a₁ = 6.
6. Solve aₙ = 2aₙ₋₁ + 3, a₀ = 1.
7. How many bit strings of length 6 have no two consecutive 1s?
8. Apply the master theorem to T(n) = 4T(n/2) + n, T(n) = 2T(n/2) + n², T(n) = 9T(n/3) + n².
9. Prove that every integer ≥ 14 can be written as 3a + 8b (non-negative a, b) by strong induction.
10. Find the number of moves for the Tower of Hanoi with 6 discs and write the recursive algorithm.

::: note Answers and worked solutions
**1.** Base n = 1: 1 = 1·2·3/6 ✓. Step: k(k+1)(2k+1)/6 + (k+1)² = (k+1)[k(2k+1) + 6(k+1)]/6 = (k+1)(2k² + 7k + 6)/6 = (k+1)(k+2)(2k+3)/6 ✓. ∎
**2.** n³ − n = (n − 1)n(n + 1), a product of three consecutive integers, so one is divisible by 3. Induction: (k+1)³ − (k+1) = (k³ − k) + 3(k² + k). ∎
**3.** Base 1 ≥ 1. Step: 2ᵏ⁺¹ = 2·2ᵏ ≥ 2(k + 1) = 2k + 2 ≥ k + 2. ∎
**4.** r² − 3r + 2 = 0 ⇒ r = 1, 2. aₙ = A + B·2ⁿ; A + B = 2; A + 2B = 3 ⇒ B = 1, A = 1: **aₙ = 1 + 2ⁿ**. (a₂ = 9 − 4 = 5 = 1 + 4 ✓)
**5.** (r − 3)² = 0 ⇒ aₙ = (A + Bn)3ⁿ; A = 1; 3(1 + B) = 6 ⇒ B = 1: **aₙ = (1 + n)3ⁿ**. (a₂ = 36 − 9 = 27 = 3·9 ✓)
**6.** Particular: a = 2a + 3 ⇒ a = −3. aₙ = A·2ⁿ − 3; a₀ = A − 3 = 1 ⇒ A = 4: **aₙ = 4·2ⁿ − 3 = 2ⁿ⁺² − 3**. (a₁ = 5 ✓)
**7.** sₙ = sₙ₋₁ + sₙ₋₂ with s₁ = 2, s₂ = 3: 2, 3, 5, 8, 13, **21** for n = 6.
**8.** 4T(n/2) + n: log₂4 = 2 > 1 ⇒ Θ(n²). 2T(n/2) + n²: log₂2 = 1 < 2 ⇒ Θ(n²). 9T(n/3) + n²: log₃9 = 2 = d ⇒ Θ(n² log n).
**9.** Base: 14 = 3·2 + 8, 15 = 3·5, 16 = 8·2. Step: for k + 1 ≥ 17, k − 2 ≥ 15 can be written as 3a + 8b by hypothesis; add one 3 to get k + 1. ∎
**10.** Tₙ = 2ⁿ − 1 = 63 moves. `hanoi(n, from, to, via)`: if n = 0 return; hanoi(n−1, from, via, to); move disc n from → to; hanoi(n−1, via, to, from).
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Prove by mathematical induction that 1 + 3 + 5 + … + (2n − 1) = n² for all n ≥ 1.**

*Introduction.* Induction proves a statement P(n) for every integer n ≥ 1 in two steps: a base case and an inductive step.

*Base case.* For n = 1 the left side is 1 and the right side is 1² = 1, so P(1) is true.

*Inductive hypothesis.* Assume P(k) holds for some k ≥ 1: 1 + 3 + … + (2k − 1) = k².

*Inductive step.* Add the next odd number 2(k + 1) − 1 = 2k + 1 to both sides: 1 + 3 + … + (2k − 1) + (2k + 1) = k² + 2k + 1 = (k + 1)². This is P(k + 1).

*Conclusion.* P(1) is true and P(k) implies P(k + 1), so by the principle of mathematical induction P(n) holds for all n ≥ 1. Check: n = 4 gives 1 + 3 + 5 + 7 = 16 = 4².

**Q2 (10 marks). Solve the recurrence a(n) = 5a(n − 1) − 6a(n − 2) with a(0) = 1, a(1) = 4, and explain how divide-and-conquer recurrences and the Tower of Hanoi recurrence are solved.**

*Introduction.* A recurrence relation defines each term from earlier terms. Linear recurrences with constant coefficients are solved by the characteristic equation.

*Linear recurrence.*

1. **Characteristic equation.** Try a(n) = rⁿ: r² = 5r − 6, so r² − 5r + 6 = 0.
2. **Roots.** (r − 2)(r − 3) = 0 gives r = 2 and r = 3, distinct.
3. **General solution.** a(n) = A·2ⁿ + B·3ⁿ.
4. **Initial conditions.** a(0) = A + B = 1 and a(1) = 2A + 3B = 4. Subtracting twice the first equation from the second gives B = 2, so A = −1.
5. **Answer.** a(n) = 2·3ⁿ − 2ⁿ. Check: a(2) = 5·4 − 6·1 = 14 and 2·9 − 4 = 14; a(3) = 5·14 − 6·4 = 46 and 2·27 − 8 = 46.

*Other recurrences.*

6. **Tower of Hanoi.** H(n) = 2H(n − 1) + 1 with H(0) = 0 gives H(n) = 2ⁿ − 1; with 10 disks, 1,023 moves.
7. **Divide and conquer.** T(n) = 2T(n/2) + n (merge sort). Expand the recursion tree (Figure 4.1): log₂ n levels, n work each, so T(n) = Θ(n log n).
8. **Repeated roots.** If the characteristic equation has a double root r, the solution is (A + Bn)rⁿ.

| Recurrence | Solution | Use |
|---|---|---|
| a(n) = 5a(n−1) − 6a(n−2) | 2·3ⁿ − 2ⁿ | linear, distinct roots |
| H(n) = 2H(n−1) + 1 | 2ⁿ − 1 | Tower of Hanoi |
| T(n) = 2T(n/2) + n | Θ(n log n) | merge sort |

*Conclusion.* The characteristic equation solves constant-coefficient recurrences exactly; recursion trees give the order of growth of divide-and-conquer algorithms.
