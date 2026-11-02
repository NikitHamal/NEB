---
subject: Discrete Structure
grade: BCA Semester 2
unit: 1
title: Logic and Proof Techniques
area: BCA 151 · Discrete Structure · Unit 1
---

Discrete mathematics is the mathematics of countable, separate things: statements, sets, integers, graphs, strings. It is the language in which algorithms are specified and proved correct. This unit begins with logic, the grammar of every proof and every `if` statement you will write.

::: key What this unit gives you
- Propositions, connectives, truth tables, equivalences, tautologies.
- Normal forms and the algebra of logic.
- Predicates and quantifiers, with negation rules.
- Rules of inference and the standard proof techniques.
:::

## 1.1 Propositions and connectives

A **proposition** is a declarative sentence that is either true or false, never both. "Kathmandu is the capital of Nepal" is a proposition (true); "x + 2 = 5" is not (until x is given); "Close the door" is not.

| Connective | Symbol | Read | True when |
|---|---|---|---|
| Negation | ¬p | not p | p is false |
| Conjunction | p ∧ q | p and q | both true |
| Disjunction | p ∨ q | p or q (inclusive) | at least one true |
| Exclusive or | p ⊕ q | p xor q | exactly one true |
| Implication | p → q | if p then q | false only when p is true and q is false |
| Biconditional | p ↔ q | p iff q | p and q have the same value |

**Implication** surprises beginners: "If it rains, I carry an umbrella" is not broken when it does not rain, so p → q is true whenever p is false. Related forms of p → q:

- **Converse** q → p, **inverse** ¬p → ¬q, **contrapositive** ¬q → ¬p.
- The contrapositive is *equivalent* to the original; the converse and inverse are equivalent to each other but not to it.

Truth table of the main connectives (T/F):

| p | q | p ∧ q | p ∨ q | p ⊕ q | p → q | p ↔ q |
|---|---|---|---|---|---|---|
| T | T | T | T | F | T | T |
| T | F | F | T | T | F | F |
| F | T | F | T | T | T | F |
| F | F | F | F | F | T | T |

A formula with n variables has **2ⁿ** rows. **Precedence:** ¬, then ∧, then ∨, then →, then ↔.

## 1.2 Tautologies and equivalences

A **tautology** is always true; a **contradiction** is always false; otherwise a **contingency**. Two formulas are **logically equivalent** (≡) if they have identical truth tables.

| Law | Equivalence |
|---|---|
| Implication | p → q ≡ ¬p ∨ q |
| Contrapositive | p → q ≡ ¬q → ¬p |
| Biconditional | p ↔ q ≡ (p → q) ∧ (q → p) |
| De Morgan | ¬(p ∧ q) ≡ ¬p ∨ ¬q; ¬(p ∨ q) ≡ ¬p ∧ ¬q |
| Double negation | ¬¬p ≡ p |
| Distributive | p ∧ (q ∨ r) ≡ (p ∧ q) ∨ (p ∧ r); p ∨ (q ∧ r) ≡ (p ∨ q) ∧ (p ∨ r) |
| Absorption | p ∨ (p ∧ q) ≡ p; p ∧ (p ∨ q) ≡ p |
| Negation of → | ¬(p → q) ≡ p ∧ ¬q |
| Commutative, associative, idempotent, identity, domination | as in Boolean algebra |

::: example Worked example: prove an equivalence by laws
Show ¬(p ∨ (¬p ∧ q)) ≡ ¬p ∧ ¬q.
¬(p ∨ (¬p ∧ q)) ≡ ¬p ∧ ¬(¬p ∧ q) (De Morgan) ≡ ¬p ∧ (p ∨ ¬q) (De Morgan, double negation) ≡ (¬p ∧ p) ∨ (¬p ∧ ¬q) (distributive) ≡ F ∨ (¬p ∧ ¬q) ≡ **¬p ∧ ¬q**. ∎
:::

::: example Worked example: is it a tautology?
(p → q) ∧ (q → r) → (p → r) (hypothetical syllogism). The formula can be false only if the antecedent is true and p → r is false, i.e. p = T, r = F. Then p → q true forces q = T, and q → r with q = T, r = F is false, contradicting the antecedent. So it is never false: a **tautology**.
:::

**Normal forms.** A **DNF** (disjunctive normal form) is an OR of ANDs of literals; a **CNF** is an AND of ORs. Every formula has both (read the T rows for DNF, the F rows for CNF), which is the same canonical SOP/POS idea from Digital Logic. For p → q: DNF = ¬p ∨ q (already). For p ⊕ q: DNF (p ∧ ¬q) ∨ (¬p ∧ q), CNF (p ∨ q) ∧ (¬p ∨ ¬q).

**Counting formulas.** There are 2^(2ⁿ) distinct truth functions of n variables: 4 for one variable, 16 for two, 256 for three. **Satisfiability (SAT)**: is there an assignment making the formula true? It is the first problem proven NP-complete, which is why logic matters for complexity.

## 1.3 Predicates and quantifiers

A **predicate** P(x) becomes a proposition when x is given a value or **quantified** over a **domain**.

- **Universal:** ∀x P(x), "for all x, P(x)".
- **Existential:** ∃x P(x), "there exists x such that P(x)".
- **Negation:** ¬∀x P(x) ≡ ∃x ¬P(x); ¬∃x P(x) ≡ ∀x ¬P(x).

**Order matters.** Over the integers, ∀x ∃y (x + y = 0) is true (take y = −x) but ∃y ∀x (x + y = 0) is false (no single y works for all x).

::: example Worked example: translating English
"Every student who studies passes": ∀x (S(x) ∧ T(x) → P(x)) where S = is a student, T = studies, P = passes.
"Some student failed": ∃x (S(x) ∧ ¬P(x)).
Negation of "every student passes": ∃x (S(x) ∧ ¬P(x)), "some student fails".
Note: with ∀ use →; with ∃ use ∧. Writing ∀x (S(x) ∧ P(x)) would say that *everything* is a passing student.
:::

**Nested quantifiers in computing:** "Every array has a maximum" is ∀A ∃m (m ∈ A ∧ ∀a ∈ A, a ≤ m); the limit definition ∀ε>0 ∃δ>0 (…) is the same pattern. In loops, `for all` is a loop that stops at the first counterexample; `exists` stops at the first witness.

## 1.4 Rules of inference

An **argument** is valid if whenever all the premises are true the conclusion is true.

| Rule | Form |
|---|---|
| Modus ponens | p, p → q ⊢ q |
| Modus tollens | ¬q, p → q ⊢ ¬p |
| Hypothetical syllogism | p → q, q → r ⊢ p → r |
| Disjunctive syllogism | p ∨ q, ¬p ⊢ q |
| Addition | p ⊢ p ∨ q |
| Simplification | p ∧ q ⊢ p |
| Conjunction | p, q ⊢ p ∧ q |
| Resolution | p ∨ q, ¬p ∨ r ⊢ q ∨ r |
| Universal instantiation | ∀x P(x) ⊢ P(c) |
| Existential generalisation | P(c) ⊢ ∃x P(x) |

::: example Worked example: a valid argument
Premises: (1) If the server is down then the website is not reachable. (2) The website is reachable. (3) If the router fails then the server is down. Conclude: the router has not failed.
Let s = server down, w = reachable, r = router fails. (1) s → ¬w; (2) w; (3) r → s. From (1) and (2) by modus tollens: ¬s. From (3) and ¬s by modus tollens: **¬r**. ∎
:::

**Fallacies.** *Affirming the conclusion*: p → q, q ⊢ p is **invalid** (the wet road does not prove it rained). *Denying the hypothesis*: p → q, ¬p ⊢ ¬q is **invalid**.

## 1.5 Proof techniques

| Technique | Idea | Template |
|---|---|---|
| **Direct** | assume p, derive q | "Let n be even; n = 2k; n² = 4k² = 2(2k²), so even." |
| **Contrapositive** | prove ¬q → ¬p | to prove "n² even ⇒ n even", show n odd ⇒ n² odd |
| **Contradiction** | assume the negation, reach an impossibility | √2 irrational |
| **Cases** | split into exhaustive cases | |x| ≥ 0 by x ≥ 0 and x < 0 |
| **Existence** | constructive (exhibit) or non-constructive | |
| **Counterexample** | one example disproves a ∀ claim | "n² + n + 41 is prime for all n" fails at n = 40 |
| **Induction** | base case + step | Unit 4 |

::: example Worked example: √2 is irrational (contradiction)
Suppose √2 = a/b in lowest terms (a, b integers with no common factor). Then a² = 2b², so a² is even, so a is even (contrapositive: odd² is odd). Write a = 2c: 4c² = 2b², so b² = 2c², so b is even. Both a and b are even, contradicting lowest terms. Hence √2 is irrational. ∎
:::

::: example Worked example: contrapositive
Claim: if 3n + 2 is odd then n is odd. Contrapositive: if n is even then 3n + 2 is even. n = 2k ⇒ 3n + 2 = 6k + 2 = 2(3k + 1), even. ∎
:::

::: example Worked example: counterexample
Claim: for every integer n, n² + n + 41 is prime. n = 40 gives 40² + 40 + 41 = 1681 = 41², which is composite. The claim is **false**.
:::

## Formula and fact sheet

- 2ⁿ rows for n variables; 2^(2ⁿ) truth functions.
- p → q ≡ ¬p ∨ q ≡ ¬q → ¬p; ¬(p → q) ≡ p ∧ ¬q.
- De Morgan for connectives and quantifiers.
- ∀ pairs with →, ∃ pairs with ∧; quantifier order matters.
- Valid: modus ponens, tollens, syllogisms, resolution. Invalid: affirming the consequent, denying the antecedent.
- Proofs: direct, contrapositive, contradiction, cases, counterexample, induction.

## Chapter summary

- Propositions combine through connectives; the truth table decides equivalence, tautology or contradiction.
- Quantifiers extend logic to properties of many objects; negation swaps ∀ and ∃.
- Valid arguments chain inference rules; invalid ones commit fallacies.
- Proof techniques are templates; choose by the shape of the statement.

## Practice

1. Construct the truth table of (p → q) ∧ (¬q ∨ r) and decide whether it is a tautology.
2. Show p → (q → r) ≡ (p ∧ q) → r using laws.
3. Write the converse, inverse and contrapositive of "If a number is divisible by 6 then it is divisible by 3".
4. Write the DNF and CNF of p ↔ q.
5. Express with quantifiers: "Every program has a bug" and "Some program has no bug"; negate the first.
6. Is ∀x ∃y (y > x) true over ℕ? Is ∃y ∀x (y > x)?
7. Test the validity: p → q, q → r, ¬r ⊢ ¬p.
8. Prove by contradiction that there is no largest prime.
9. Prove or disprove: the sum of two irrational numbers is irrational.
10. How many different truth functions of 3 variables exist?

::: note Answers and worked solutions
**1.** Evaluating (p → q) ∧ (¬q ∨ r) row by row (p q r): TTT = T, TTF = F, TFT = F, TFF = F, FTT = T, FTF = F, FFT = T, FFF = T. It is true in 4 of the 8 rows, so it is **not a tautology** (a contingency).
**2.** p → (q → r) ≡ ¬p ∨ (¬q ∨ r) ≡ (¬p ∨ ¬q) ∨ r ≡ ¬(p ∧ q) ∨ r ≡ (p ∧ q) → r. ∎
**3.** Converse: if divisible by 3 then divisible by 6 (false: 9). Inverse: if not divisible by 6 then not divisible by 3 (false: 9). Contrapositive: if not divisible by 3 then not divisible by 6 (true).
**4.** DNF: (p ∧ q) ∨ (¬p ∧ ¬q). CNF: (¬p ∨ q) ∧ (p ∨ ¬q).
**5.** ∀x (Program(x) → ∃b Bug(b, x)); ∃x (Program(x) ∧ ¬∃b Bug(b, x)); negation of the first is the second.
**6.** ∀x ∃y (y > x) is **true** (y = x + 1). ∃y ∀x (y > x) is **false** (take x = y).
**7.** From q → r and ¬r: ¬q (modus tollens). From p → q and ¬q: ¬p (modus tollens). **Valid.**
**8.** Suppose p₁ … pₖ are all the primes. N = p₁p₂…pₖ + 1 is not divisible by any pᵢ (remainder 1), so N has a prime factor not in the list, a contradiction. ∎
**9.** **False**: √2 and −√2 are irrational but their sum is 0, rational.
**10.** 2^(2³) = 2⁸ = **256**.
:::
