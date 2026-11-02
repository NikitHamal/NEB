---
subject: Probability and Statistics
grade: BCA Semester 3
unit: 4
title: Probability
hours: 8
area: BCA 205 · Probability and Statistics · Unit 4
---

**Probability** measures how likely an event is, from 0 (impossible) to 1 (certain). It is the mathematics of uncertainty behind sampling, hashing, networks, randomised algorithms and machine learning.

::: key What this unit gives you
- Definitions of probability; the addition and multiplication laws; conditional probability and Bayes' rule.
- The binomial, Poisson and normal distributions with numerical problems.
- A table of standard normal values.
:::

## 4.1 Basic definitions

An **experiment** has several possible **outcomes**; the **sample space** S is the set of all outcomes; an **event** is a subset of S. Events are **mutually exclusive** (cannot occur together), **exhaustive** (together cover S), **independent** (one does not affect the other's probability).

**Classical definition:** P(A) = (number of outcomes favourable to A)/(total equally likely outcomes). **Empirical (relative frequency):** P(A) = lim (times A occurred)/(trials). Axioms: 0 ≤ P(A) ≤ 1; P(S) = 1; for mutually exclusive A, B, P(A ∪ B) = P(A) + P(B). Complement: P(Aᶜ) = 1 − P(A).

## 4.2 Two basic laws

**Addition law:** P(A ∪ B) = P(A) + P(B) − P(A ∩ B); for mutually exclusive events the last term is 0.

**Multiplication law:** P(A ∩ B) = P(A) · P(B | A); for **independent** events P(A ∩ B) = P(A)P(B).

::: example Worked example
Two fair dice are rolled. P(sum = 8) = 5/36 (the pairs 2+6, 3+5, 4+4, 5+3, 6+2). P(at least one six) = 1 − (5/6)² = 11/36. A card drawn from 52: P(king or heart) = 4/52 + 13/52 − 1/52 = **16/52**.
Bag with 5 red and 3 blue balls; two drawn **without replacement**: P(both red) = (5/8)(4/7) = **5/14**; with replacement it would be (5/8)² = 25/64.
:::

## 4.3 Conditional probability and Bayes' theorem

**Conditional probability** of A given that B has occurred: **P(A | B) = P(A ∩ B)/P(B)**, P(B) > 0. A and B are independent iff P(A | B) = P(A). **Bayes' theorem** reverses the conditioning: **P(A | B) = P(B | A)P(A)/P(B)**, with P(B) from the total probability law, P(B) = Σ P(B | Aᵢ)P(Aᵢ).

::: example Worked example: a diagnostic test
A bug-detection tool flags a module as buggy. 1% of modules are buggy; the tool flags 95% of buggy modules and falsely flags 5% of clean ones. P(flag) = 0.01 × 0.95 + 0.99 × 0.05 = 0.0095 + 0.0495 = 0.059. **P(buggy | flagged) = 0.0095/0.059 = 0.161**: only about 16% of flagged modules are actually buggy, because buggy modules are rare. Also, if P(A) = 0.5, P(B) = 0.4 and P(A ∩ B) = 0.2 then P(A | B) = 0.5 = P(A), so A and B are independent.
:::

## 4.4 Random variables and probability distributions

A **random variable** X assigns a number to each outcome. **Discrete** (counts) has a **probability mass function** p(x) with Σp(x) = 1; **continuous** (measurements) has a **density** f(x) with total area 1, and probabilities are areas. **Expected value** E(X) = Σx·p(x) (mean); **variance** Var(X) = E(X²) − [E(X)]².

### Binomial distribution

For n independent trials, each with success probability p: **P(X = x) = C(n, x) pˣ (1 − p)ⁿ⁻ˣ**, x = 0…n. **Mean = np, variance = npq** (q = 1 − p).

::: example Worked example
A packet is lost with probability 0.4; 5 packets are sent. P(exactly 2 lost) = C(5,2)(0.4)²(0.6)³ = 10 × 0.16 × 0.216 = **0.3456**. P(at least one lost) = 1 − 0.6⁵ = **0.9222**. Mean = 5 × 0.4 = 2.0, variance = 5 × 0.4 × 0.6 = 1.2.
:::

### Poisson distribution

Counts of rare events in a fixed interval with average rate λ: **P(X = x) = e^(−λ) λˣ / x!**; **mean = variance = λ**. It approximates the binomial when n is large and p small (λ = np).

::: example Worked example
A server receives on average 3 failures a day. P(exactly 2) = e⁻³·3²/2! = 0.0498 × 4.5 = **0.2240**. P(at most 2) = **0.4232**. P(at least one) = 1 − e⁻³ = **0.9502**.
:::

### Normal distribution

The bell curve, symmetric about the mean μ: f(x) = (1/(σ√(2π))) e^(−(x − μ)²/(2σ²)). Written X ~ N(μ, σ²). **Standardise:** **Z = (X − μ)/σ ~ N(0, 1)**, then use the standard normal table of Φ(z) = P(Z ≤ z). **Empirical rule:** P(μ − σ < X < μ + σ) = 0.6827, ±2σ: 0.9545, ±3σ: 0.9973. The total area is 1, the curve is symmetric so Φ(−z) = 1 − Φ(z), and mean = median = mode.

| z | 0 | 0.5 | 1.0 | 1.5 | 2.0 | 2.5 | 3.0 |
|---|---|---|---|---|---|---|---|
| Φ(z) | 0.5000 | 0.6915 | 0.8413 | 0.9332 | 0.9772 | 0.9938 | 0.9987 |

::: example Worked example: X ~ N(200, 20²)
**P(X > 230):** z = (230 − 200)/20 = 1.5; P = 1 − Φ(1.5) = 1 − 0.9332 = **0.0668**.
**P(180 < X < 240):** z from −1 to 2: Φ(2) − Φ(−1) = 0.9772 − 0.1587 = **0.8186**.
**P(X < 190):** z = −0.5; Φ(−0.5) = 1 − 0.6915 = **0.3085**.
**Top 10%:** z = 1.2816 → X = 200 + 1.2816 × 20 = **225.63**.
Normal approximation to the binomial (n large, np and nq > 5): X ≈ N(np, npq) with a continuity correction ±0.5.
:::

## Formula and fact sheet

- P(A ∪ B) = P(A) + P(B) − P(A ∩ B); P(A ∩ B) = P(A)P(B | A); P(A | B) = P(A ∩ B)/P(B).
- Bayes: P(A | B) = P(B | A)P(A)/P(B).
- Binomial: C(n, x)pˣqⁿ⁻ˣ; mean np, var npq. Poisson: e^(−λ)λˣ/x!; mean = var = λ.
- Normal: Z = (X − μ)/σ; ±1σ 68.27%, ±2σ 95.45%, ±3σ 99.73%.

## Chapter summary

- Probability follows the addition and multiplication laws; conditioning updates probabilities and Bayes' rule inverts them.
- Binomial models fixed trials, Poisson rare events, normal measurements, which are standardised to Z for table lookup.

## Practice

1. Two coins are tossed. Find the probability of at least one head.
2. A bag has 5 red and 3 blue balls. Two drawn without replacement: P(one of each colour)?
3. P(A) = 0.6, P(B) = 0.5, P(A ∪ B) = 0.8. Find P(A ∩ B) and P(A | B). Are A and B independent?
4. A fair coin is tossed 6 times. Find the probability of exactly 3 heads, and the mean and variance of the number of heads.
5. Calls arrive at 2 per minute (Poisson). P(no calls in a minute)?
6. X ~ N(50, 10²). Find P(40 < X < 65).
7. Marks are N(60, 15²). What fraction scores below 40? Above 90?
8. Explain independence vs mutual exclusivity.

::: note Answers and worked solutions
**1.** 1 − P(no heads) = 1 − 1/4 = **3/4**.
**2.** P(R then B) + P(B then R) = (5/8)(3/7) + (3/8)(5/7) = 15/56 + 15/56 = **15/28**.
**3.** P(A ∩ B) = 0.6 + 0.5 − 0.8 = **0.3**; P(A | B) = 0.3/0.5 = **0.6** = P(A), so they **are independent** (0.6 × 0.5 = 0.3).
**4.** C(6,3)/2⁶ = 20/64 = **0.3125**; mean = 3, variance = 6 × 0.25 = **1.5**.
**5.** e⁻² = **0.1353**.
**6.** z = −1 and 1.5: 0.9332 − 0.1587 = **0.7745**.
**7.** Below 40: z = −1.33, Φ = 0.0918 (**9.2%**). Above 90: z = 2, 1 − 0.9772 = **2.3%**.
**8.** Independent: occurrence of one does not change the probability of the other (P(A ∩ B) = P(A)P(B)). Mutually exclusive: cannot both occur (P(A ∩ B) = 0). Events with nonzero probabilities cannot be both.
:::
