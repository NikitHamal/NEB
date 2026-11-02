---
subject: Discrete Structure
grade: BCA Semester 2
unit: 6
title: Number Theory, Modular Arithmetic and Algebraic Structures
area: BCA 151 · Discrete Structure · Unit 6
---

Number theory, once the purest branch of mathematics, now protects every online payment. This unit covers divisibility, the Euclidean algorithm, modular arithmetic and RSA, then introduces algebraic structures (groups) and the lattice and Boolean algebra viewpoint that unifies sets, logic and circuits.

::: key What this unit gives you
- Divisibility, primes, gcd/lcm, the Euclidean and extended Euclidean algorithms.
- Congruences, modular inverses, Fermat's theorem, the Chinese remainder theorem.
- Applications: hashing, check digits, Caesar cipher, and RSA with a worked toy example.
- Groups and other algebraic structures; Boolean algebra as a lattice.
:::

## 6.1 Divisibility, primes and gcd

a **divides** b (a | b) if b = ak for an integer k. **Division algorithm**: for integers a and d > 0 there are unique q and r with a = dq + r, 0 ≤ r < d. A **prime** has exactly two positive divisors (2, 3, 5, 7, 11, …). **Fundamental theorem of arithmetic**: every integer ≥ 2 factors uniquely into primes (up to order); 360 = 2³ · 3² · 5. There are infinitely many primes (Euclid, proved in Unit 1). To test whether n is prime, trial-divide by primes up to √n.

**gcd and lcm.** gcd(a, b) is the largest common divisor; **gcd(a, b) · lcm(a, b) = ab**. Using factorisations: gcd takes the minimum powers, lcm the maximum. a and b are **coprime** if gcd = 1.

**Euclidean algorithm**: gcd(a, b) = gcd(b, a mod b), stopping when the remainder is 0. It takes at most about 5 × (digits of the smaller number) steps, which is fast even for 300-digit numbers.

::: example Worked example: gcd and extended Euclid
gcd(252, 105): 252 = 2·105 + 42; 105 = 2·42 + 21; 42 = 2·21 + 0. **gcd = 21**; lcm = 252·105/21 = **1260**.
**Extended Euclid (Bézout):** work backwards: 21 = 105 − 2·42 = 105 − 2(252 − 2·105) = **5·105 − 2·252**. So 21 = 5·105 + (−2)·252, and the equation 105x + 252y = 21 has the solution (x, y) = (5, −2).
:::

A linear Diophantine equation ax + by = c has integer solutions iff gcd(a, b) | c. Example: 6x + 9y = 8 has none (gcd 3 does not divide 8); 6x + 9y = 12 does (x = −2, y = 2).

## 6.2 Modular arithmetic

**a ≡ b (mod m)** means m | (a − b), i.e. a and b leave the same remainder. Congruence is an equivalence relation with m classes (ℤₘ = {0, 1, …, m − 1}). It respects addition, subtraction and multiplication:

(a + b) mod m = ((a mod m) + (b mod m)) mod m; likewise for ×, so we can reduce at every step.

::: example Worked example
Last digit of 7²²²: powers of 7 mod 10 cycle 7, 9, 3, 1 (period 4). 222 mod 4 = 2, so the last digit is **9**.
2¹⁰⁰ mod 7: 2³ = 8 ≡ 1, so 2¹⁰⁰ = (2³)³³ · 2 ≡ **2**.
(123 × 456) mod 11: 123 ≡ 2, 456 ≡ 5 (456 − 451), so 10.
**Divisibility by 9:** a number ≡ its digit sum (mod 9); 7,842 has digit sum 21 ≡ 3, so 7,842 mod 9 = 3.
:::

**Modular inverse.** a has an inverse mod m iff gcd(a, m) = 1; it is found with extended Euclid. Then ax ≡ b (mod m) has the solution x ≡ a⁻¹b.

::: example Worked example
Inverse of 7 mod 26: 26 = 3·7 + 5; 7 = 1·5 + 2; 5 = 2·2 + 1. Back: 1 = 5 − 2·2 = 5 − 2(7 − 5) = 3·5 − 2·7 = 3(26 − 3·7) − 2·7 = 3·26 − 11·7. So 7⁻¹ ≡ −11 ≡ **15** (check: 7·15 = 105 = 4·26 + 1 ✓).
Solve 3x ≡ 4 (mod 7): 3⁻¹ = 5 (15 ≡ 1), so x ≡ 5·4 = 20 ≡ **6** (check 18 mod 7 = 4 ✓).
:::

**Fermat's little theorem**: if p is prime and p ∤ a, then **aᵖ⁻¹ ≡ 1 (mod p)**. **Euler's theorem**: if gcd(a, n) = 1 then a^{φ(n)} ≡ 1 (mod n), where φ(n) counts integers up to n coprime to n; φ(p) = p − 1, φ(pq) = (p − 1)(q − 1).

**Chinese remainder theorem (CRT)**: if the moduli are pairwise coprime, the system x ≡ aᵢ (mod mᵢ) has a unique solution modulo M = ∏mᵢ.

::: example Worked example: CRT
x ≡ 2 (mod 3), x ≡ 3 (mod 5), x ≡ 2 (mod 7). M = 105. Search x = 2 + 3t (t = 0,1,…) satisfying mod 5 = 3: x = 8 (8 mod 5 = 3). Now x = 8 + 15s with x ≡ 2 (mod 7): 8 ≡ 1, 15 ≡ 1, so 1 + s ≡ 2 ⇒ s = 1, x = **23**. Check: 23 mod 3 = 2, mod 5 = 3, mod 7 = 2 ✓. Solutions: 23 + 105k.
:::

## 6.3 Applications

- **Hashing**: h(k) = k mod m with m prime spreads keys well. Keys 123, 456, 789 with m = 11 give 2, 5, 8 (789 = 71·11 + 8).
- **Check digits**: ISBN-10 requires Σ (i × dᵢ) ≡ 0 (mod 11); a single wrong digit is always detected, since 11 is prime.
- **Pseudo-random numbers**: linear congruential generator Xₙ₊₁ = (aXₙ + c) mod m.
- **Caesar cipher**: E(x) = (x + 3) mod 26, D(y) = (y − 3) mod 26; "NEPAL" becomes "QHSDO". It is weak (26 keys); an **affine cipher** E(x) = (ax + b) mod 26 needs gcd(a, 26) = 1.
- **Fast modular exponentiation** (square and multiply) computes aᵏ mod m in O(log k) multiplications: 3¹³ mod 7: 3² = 2, 3⁴ = 4, 3⁸ = 16 ≡ 2; 13 = 8 + 4 + 1 ⇒ 2 · 4 · 3 = 24 ≡ **3**.

**RSA public-key cryptography.**

1. Choose primes p, q; n = pq; φ = (p − 1)(q − 1).
2. Choose e coprime to φ (public key (e, n)); compute d = e⁻¹ mod φ (private key).
3. Encrypt: c = mᵉ mod n. Decrypt: m = cᵈ mod n (correct by Euler's theorem since ed ≡ 1 mod φ).

::: example Worked example: a toy RSA
p = 61, q = 53 ⇒ n = 3233, φ = 60 · 52 = 3120. Take e = 17 (gcd(17, 3120) = 1). Then d = 17⁻¹ mod 3120 = **2753** (17 · 2753 = 46,801 = 15 · 3120 + 1 ✓).
Encrypt m = 65: c = 65¹⁷ mod 3233 = **2790**. Decrypt: 2790²⁷⁵³ mod 3233 = **65** ✓.
Security rests on the difficulty of factoring n; real keys use n of 2048 bits or more. Real systems also add padding (OAEP) and use RSA mainly to exchange a symmetric key. Quantum computers (Shor's algorithm) could break RSA, which motivates post-quantum cryptography.
:::

## 6.4 Algebraic structures

A **binary operation** on a set S takes two elements and returns an element of S (closure).

| Structure | Axioms |
|---|---|
| **Semigroup** | closed, associative |
| **Monoid** | semigroup with an identity |
| **Group** | monoid where every element has an inverse |
| **Abelian group** | commutative group |
| **Ring** | abelian group under +, monoid (or semigroup) under ×, × distributes over + |
| **Field** | commutative ring where every non-zero element has a multiplicative inverse |

Examples: (ℤ, +) is an abelian group; (ℕ, +) is a monoid; (ℤ, ×) is a monoid; (ℚ − {0}, ×) is a group; **ℤₚ with + and × is a field when p is prime** (that is why inverses mod a prime always exist); strings under concatenation form a monoid (identity: empty string); invertible n × n matrices under multiplication form a (non-abelian) group; the permutations of n objects form the symmetric group Sₙ of order n!.

::: example Worked example: the group ℤ₆ under +
Elements {0, …, 5}, identity 0, inverse of a is 6 − a (so 2⁻¹ = 4). Order 6. The element 1 **generates** the group (1, 2, 3, 4, 5, 0), so ℤ₆ is **cyclic**; 5 also generates it; 2 generates only {0, 2, 4}, a **subgroup** of order 3; {0, 3} is a subgroup of order 2. **Lagrange's theorem**: the order of a subgroup divides the order of the group (2 | 6, 3 | 6). The multiplicative set {1, 5} mod 6 is a group, but {1, 2, 3, 4, 5} mod 6 is not (2 has no inverse as gcd(2, 6) = 2); ℤ₇* = {1,…,6} is a group of order 6 under multiplication mod 7.
:::

A **homomorphism** preserves the operation: f(a ∗ b) = f(a) ⋆ f(b). Example: x ↦ x mod 3 from (ℤ, +) to (ℤ₃, +), and x ↦ eˣ from (ℝ, +) to (ℝ⁺, ×). **Applications:** error-correcting codes are built on finite fields (Reed–Solomon in QR codes, CDs); AES uses arithmetic in GF(2⁸); elliptic-curve cryptography uses a group of curve points.

## 6.5 Lattices and Boolean algebra

A **lattice** is a poset in which every two elements have a least upper bound (**join**, ∨) and a greatest lower bound (**meet**, ∧). Examples: (subsets of S, ⊆) with ∪ and ∩; (divisors of n, |) with lcm and gcd; (ℕ, ≤) with max and min.

A **Boolean algebra** is a complemented distributive lattice with 0 and 1. The two-element algebra {0, 1} is the algebra of switching circuits and of propositional logic; the power set of a set is another; **every finite Boolean algebra has 2ⁿ elements** and looks like subsets of an n-set. This is why the same laws (De Morgan, distributivity, absorption) hold in logic (Unit 1), sets (Unit 2) and digital circuits (the Digital Logic book): they are three views of one structure.

**Divisor lattice of 12**: elements {1, 2, 3, 4, 6, 12}; join of 4 and 6 = lcm = 12; meet = gcd = 2. It is *not* complemented (4 has no complement), so it is a lattice but not a Boolean algebra; the divisors of 30 (= 2·3·5) form one, with 8 = 2³ elements.

## Formula and fact sheet

- a = dq + r; gcd(a, b) = gcd(b, a mod b); gcd · lcm = ab; Bézout: gcd = ax + by.
- a ≡ b (mod m) ⇔ m | a − b; inverse exists iff gcd(a, m) = 1.
- Fermat: aᵖ⁻¹ ≡ 1 (mod p). Euler: a^φ(n) ≡ 1; φ(pq) = (p−1)(q−1).
- CRT: coprime moduli give a unique solution mod the product.
- RSA: n = pq, ed ≡ 1 (mod φ), c = mᵉ mod n, m = cᵈ mod n.
- Group: closure, associativity, identity, inverse. ℤₚ is a field for prime p. Lagrange: subgroup order divides group order.
- Finite Boolean algebra has 2ⁿ elements.

## Chapter summary

- The Euclidean algorithm computes gcds quickly and the extended version yields inverses.
- Modular arithmetic lets us compute with remainders; Fermat, Euler and the CRT are its workhorses.
- RSA turns the difficulty of factoring into public-key encryption.
- Groups, rings and fields classify structures by their axioms; Boolean algebras unify logic, sets and circuits.

## Practice

1. Find gcd(1071, 462) and express it as 1071x + 462y.
2. Find 5⁻¹ mod 17 and solve 5x ≡ 3 (mod 17).
3. Find the last two digits of 3¹⁰⁰ (hint: 3²⁰ mod 100).
4. Solve x ≡ 1 (mod 4), x ≡ 2 (mod 9) (use CRT).
5. Compute 7¹⁰⁰ mod 13 using Fermat's theorem.
6. In RSA with p = 5, q = 11, e = 7, find n, φ, d, the ciphertext of m = 8 and verify decryption.
7. Is (ℤ₈ − {0}, × mod 8) a group? Justify.
8. List all subgroups of (ℤ₁₂, +).
9. Show that the ISBN-10 check digit detects any single wrong digit.
10. Is the divisor lattice of 18 a Boolean algebra?

::: note Answers and worked solutions
**1.** 1071 = 2·462 + 147; 462 = 3·147 + 21; 147 = 7·21. **gcd = 21**. 21 = 462 − 3·147 = 462 − 3(1071 − 2·462) = 7·462 − 3·1071. So x = −3, y = 7.
**2.** 5 · 7 = 35 = 2·17 + 1, so 5⁻¹ = **7**. 5x ≡ 3 ⇒ x ≡ 7·3 = 21 ≡ **4** (check 20 mod 17 = 3 ✓).
**3.** 3⁴ = 81; 3²⁰ = 81⁵: 81² = 6561 ≡ 61; 81⁴ ≡ 61² = 3721 ≡ 21; 81⁵ ≡ 21·81 = 1701 ≡ 1. So 3²⁰ ≡ 1 (mod 100) and 3¹⁰⁰ ≡ **01**.
**4.** x = 1 + 4t ≡ 2 (mod 9) ⇒ 4t ≡ 1 ⇒ t ≡ 7 (4·7 = 28 ≡ 1) ⇒ x = 29. Solutions **x ≡ 29 (mod 36)** (29 mod 4 = 1, 29 mod 9 = 2 ✓).
**5.** 7¹² ≡ 1 (mod 13); 100 = 8·12 + 4; 7⁴ = 2401 = 184·13 + 9. So 7¹⁰⁰ ≡ **9**.
**6.** n = 55, φ = 40; d = 7⁻¹ mod 40 = 23 (7·23 = 161 = 4·40 + 1). c = 8⁷ mod 55: 8² = 64 ≡ 9; 8⁴ ≡ 81 ≡ 26; 8⁶ ≡ 26·9 = 234 ≡ 14; 8⁷ ≡ 112 ≡ **2**. Decrypt 2²³ mod 55: 2¹⁰ = 1024 ≡ 34; 2²⁰ ≡ 34² = 1156 ≡ 1; 2²³ ≡ 8 ✓.
**7.** **No**: 2, 4, 6 have no inverse (gcd with 8 is not 1) and 2·4 = 8 ≡ 0 is not in the set.
**8.** Subgroups of ℤ₁₂ correspond to divisors of 12: ⟨1⟩ (order 12), ⟨2⟩ = {0,2,4,6,8,10} (6), ⟨3⟩ = {0,3,6,9} (4), ⟨4⟩ = {0,4,8} (3), ⟨6⟩ = {0,6} (2), ⟨0⟩ = {0} (1): **six** subgroups.
**9.** If digit i (weight i) changes by δ ≠ 0 (|δ| ≤ 10), the weighted sum changes by iδ, which is not ≡ 0 (mod 11) because 11 is prime and divides neither i (1 to 10) nor δ.
**10.** 18 = 2 · 3² is not square-free (it has a repeated prime factor), so the divisor lattice (1, 2, 3, 6, 9, 18) is **not** a Boolean algebra (6 elements is not 2ⁿ).
:::
