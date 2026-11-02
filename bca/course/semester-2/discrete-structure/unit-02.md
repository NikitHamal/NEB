---
subject: Discrete Structure
grade: BCA Semester 2
unit: 2
title: Sets, Relations and Functions
area: BCA 151 · Discrete Structure · Unit 2
---

Sets, relations and functions are the vocabulary of data: a table is a relation, a database query is a set operation, a hash is a function. This unit defines them precisely and shows how to count and classify them.

::: key What this unit gives you
- Set notation, operations, identities, Venn diagrams and inclusion–exclusion.
- Relations: properties, representations, closures, equivalence relations and partial orders.
- Functions: one-to-one, onto, composition, inverse, and counting functions.
- Cardinality: finite, countable and uncountable sets.
:::

## 2.1 Sets and their operations

A **set** is an unordered collection of distinct objects. Notation: roster {1, 2, 3}; builder {x | x is even and x < 10}. ∅ is the empty set; **U** the universal set; |A| the cardinality; x ∈ A membership; A ⊆ B subset; A ⊂ B proper subset.

| Operation | Definition |
|---|---|
| Union A ∪ B | in A or B |
| Intersection A ∩ B | in both |
| Difference A − B | in A but not B |
| Complement A′ | in U but not A |
| Symmetric difference A ⊕ B | in exactly one: (A − B) ∪ (B − A) |
| Cartesian product A × B | all ordered pairs (a, b); \|A × B\| = \|A\|·\|B\| |
| Power set P(A) | the set of all subsets; \|P(A)\| = 2^{\|A\|} |

**Set identities** mirror logic: A ∪ (B ∩ C) = (A ∪ B) ∩ (A ∪ C); (A ∪ B)′ = A′ ∩ B′ (De Morgan); A ∪ A′ = U; A ∩ A′ = ∅; A − B = A ∩ B′. Prove equality by showing each side is a subset of the other, or by a membership table.

**Inclusion–exclusion.** |A ∪ B| = |A| + |B| − |A ∩ B|; |A ∪ B ∪ C| = |A| + |B| + |C| − |A∩B| − |A∩C| − |B∩C| + |A∩B∩C|.

::: example Worked example
In a class of 60, 35 study Java, 28 study Python and 10 study both. Either = 35 + 28 − 10 = 53, so **7** study neither; Java only = 25; Python only = 18.
**Power set:** P({a, b, c}) has 2³ = 8 elements: ∅, {a}, {b}, {c}, {a,b}, {a,c}, {b,c}, {a,b,c}.
**Bit-string view:** a subset of an n-element set is an n-bit string, so union is bitwise OR, intersection bitwise AND, and complement bitwise NOT. This is how sets are stored in machine words.
:::

## 2.2 Relations

A **relation** R from A to B is a subset of A × B; "a R b" means (a, b) ∈ R. A relation on A is a subset of A × A. A relation can be shown as a set of pairs, a **matrix** (1 if related), or a **digraph**.

**Properties of a relation R on A**

| Property | Meaning |
|---|---|
| Reflexive | (a, a) ∈ R for all a |
| Irreflexive | (a, a) ∉ R for all a |
| Symmetric | (a, b) ∈ R ⇒ (b, a) ∈ R |
| Antisymmetric | (a, b) and (b, a) ∈ R ⇒ a = b |
| Transitive | (a, b), (b, c) ∈ R ⇒ (a, c) ∈ R |

An **equivalence relation** is reflexive, symmetric and transitive; it partitions A into **equivalence classes**. A **partial order** is reflexive, antisymmetric and transitive; (A, ≤) is a **poset**, drawn as a **Hasse diagram** (omit loops and implied edges).

::: example Worked example
On {1, 2, 3}: R = {(1,1), (2,2), (3,3), (1,2), (2,1)} is reflexive, symmetric and transitive: an equivalence relation with classes {1, 2} and {3}.
"Divides" on {1, 2, 3, 4, 6, 12} is a partial order; its Hasse diagram has 1 at the bottom, then 2 and 3, then 4 and 6, and 12 at the top. 1 is the minimum, 12 the maximum; 4 and 6 are incomparable.
**Congruence mod 3** on ℤ (a ~ b iff 3 | a − b) is an equivalence with three classes: [0] = {…, −3, 0, 3, …}, [1], [2].
:::

**Counting relations.** On an n-element set there are 2^{n²} relations; 2^{n² − n} reflexive ones; 2^{n(n+1)/2} symmetric ones. For n = 3: 512, 64 and 64.

**Composition and closures.** R∘S = {(a, c) | ∃b: (a, b) ∈ S, (b, c) ∈ R} (order convention varies; here S is applied first). In matrix form it is the Boolean matrix product. The **reflexive**, **symmetric** and **transitive closures** are the smallest relations containing R with that property.

::: example Worked example: transitive closure
R = {(1,2), (2,3), (3,4)} on {1, 2, 3, 4}. Add (1,3) from (1,2),(2,3); (2,4) from (2,3),(3,4); then (1,4) from (1,3),(3,4). Closure = {(1,2), (2,3), (3,4), (1,3), (2,4), (1,4)}. **Warshall's algorithm** does this in O(n³): for each k, i, j, set M[i][j] |= M[i][k] & M[k][j].
:::

**Databases:** a relational table is a relation; a join is a composition-like operation; a primary key makes the relation a function from key to row.

## 2.3 Functions

A **function** f: A → B assigns each a ∈ A exactly one f(a) ∈ B. Domain A, codomain B, range = set of actual outputs.

| Type | Meaning | Test |
|---|---|---|
| **Injective** (one-to-one) | f(a) = f(a′) ⇒ a = a′ | no output hit twice |
| **Surjective** (onto) | every b has some a | range = codomain |
| **Bijective** | both | invertible |

**Composition** (g∘f)(x) = g(f(x)); composition of bijections is a bijection; a bijection has an inverse f⁻¹ with f⁻¹∘f = id.

::: example Worked example
f(x) = 2x + 1 on ℤ → ℤ is injective but not onto (even numbers are never reached). g(x) = x² on ℝ is neither (g(2) = g(−2); −1 is never reached); on [0, ∞) → [0, ∞) it is a bijection.
**Counting functions** from an m-set A to an n-set B: total nᵐ; injective n!/(n − m)! (needs m ≤ n); bijections n! (m = n); **onto** by inclusion–exclusion: for m = 4, n = 3: 3⁴ − 3·2⁴ + 3·1⁴ = 81 − 48 + 3 = **36**.
**Pigeonhole principle:** a function from a set of more than k elements to a set of k elements cannot be injective, so some two elements share an image. Among 13 people, two share a birth month.
**Hash functions** are not injective (collisions are certain when keys outnumber slots), which is the pigeonhole principle at work.
:::

Special functions: **floor** ⌊x⌋, **ceiling** ⌈x⌉, **mod**, **characteristic function** of a set, **recursive functions** (Unit 4). Growth of functions (big-O) uses these: n log n ≪ n² ≪ 2ⁿ ≪ n!.

## 2.4 Cardinality and countability

Two sets have the same cardinality if a bijection exists between them. A set is **countable** if it is finite or has the same size as ℕ. ℤ is countable (list 0, 1, −1, 2, −2, …); ℚ is countable; the set of all finite strings over a finite alphabet is countable (so the set of all programs is countable). **ℝ is uncountable** (Cantor's diagonal argument): any list of reals in (0,1) misses the number whose nth digit differs from the nth digit of the nth number. Consequence: there are more functions ℕ → {0,1} than programs, so some functions are **not computable**.

## Formula and fact sheet

- |P(A)| = 2ⁿ; |A × B| = |A||B|; |A ∪ B| = |A| + |B| − |A ∩ B|.
- Equivalence = reflexive + symmetric + transitive (partitions); partial order = reflexive + antisymmetric + transitive.
- Relations on n-set: 2^{n²}; reflexive 2^{n²−n}; symmetric 2^{n(n+1)/2}.
- Functions A → B: |B|^{|A|}; injective n!/(n−m)!; onto by inclusion–exclusion.
- Pigeonhole: n + 1 objects in n boxes ⇒ a box with two.
- ℕ, ℤ, ℚ countable; ℝ uncountable.

## Chapter summary

- Sets and bit strings: union, intersection and complement are the logical operators applied to membership.
- Relations capture structure (equivalence → partitions, order → posets); closures add forced pairs.
- Functions classified as injective, surjective, bijective; counting uses powers, falling factorials and inclusion–exclusion.
- Cardinality separates countable from uncountable infinities, with consequences for computability.

## Practice

1. If A = {1, 2, 3, 4}, B = {3, 4, 5}, U = {1,…,6}, find A ∪ B, A ∩ B, A − B, B′, A ⊕ B, |P(A)|, |A × B|.
2. Of 100 students 70 like cricket, 55 like football and 25 like neither. How many like both?
3. Prove (A ∪ B)′ = A′ ∩ B′.
4. Test the relation R on ℤ: a R b iff a − b is even; classify and give the classes.
5. Is "divides" on positive integers an equivalence relation? A partial order?
6. Find the transitive closure of {(a, b), (b, c), (c, a)} on {a, b, c}.
7. How many reflexive and symmetric relations on a 4-element set?
8. Classify f(x) = x³ on ℝ → ℝ and f(n) = n mod 5 on ℤ → {0,…,4}.
9. Count the functions from a 3-set to a 5-set, and the injective ones.
10. Show that the set of positive rationals is countable (describe the listing).

::: note Answers and worked solutions
**1.** A ∪ B = {1,2,3,4,5}; A ∩ B = {3,4}; A − B = {1,2}; B′ = {1,2,6}; A ⊕ B = {1,2,5}; |P(A)| = 16; |A × B| = 12.
**2.** Likes at least one = 100 − 25 = 75 = 70 + 55 − both ⇒ both = **50**.
**3.** x ∈ (A ∪ B)′ ⇔ ¬(x ∈ A ∨ x ∈ B) ⇔ x ∉ A ∧ x ∉ B ⇔ x ∈ A′ ∩ B′. ∎
**4.** Reflexive (0 is even), symmetric, transitive (even + even = even): an **equivalence** with two classes: the evens and the odds.
**5.** Not symmetric (2 | 4, 4 ∤ 2), so not an equivalence. It is reflexive, antisymmetric and transitive: a **partial order**.
**6.** The closure is all nine pairs of {a, b, c}²: a→b→c→a lets every element reach every element, including itself.
**7.** Reflexive: diagonal pairs forced (4). Symmetric on the 6 off-diagonal pairs: 2⁶ = **64** relations that are both.
**8.** x³ is a **bijection** on ℝ. n mod 5 is **onto** but not injective.
**9.** 5³ = **125**; injective: 5·4·3 = **60**.
**10.** Arrange p/q in a grid by numerator p and denominator q; walk the diagonals p + q = 2, 3, 4, … skipping fractions not in lowest terms; every positive rational appears exactly once, giving a bijection with ℕ.
:::
