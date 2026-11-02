---
subject: Mathematics I
grade: BCA Semester 1
unit: 2
title: Limits and Continuity
area: BCA 104 · Mathematics I · Unit 2
---

A **limit** describes what a function approaches near a point, even if it never reaches it. Limits are the foundation of both the derivative (a limit of slopes) and the integral (a limit of sums), and continuity is the property that makes functions well-behaved enough for calculus.

::: key What this unit gives you
- The meaning of lim f(x) as x → a, one-sided limits, and limits at infinity.
- The limit laws and every standard technique: factoring, rationalising, standard limits, squeeze.
- Continuity, the three types of discontinuity, and the Intermediate Value Theorem.
:::

## 2.1 The idea of a limit

We write **lim (x→a) f(x) = L** if f(x) can be made as close to L as we like by taking x close enough to a (but x ≠ a). The value f(a) itself is irrelevant to the limit.

Take f(x) = (x² − 1)/(x − 1). It is undefined at 1, but for x ≠ 1 it equals x + 1. As x → 1 the values approach 2, so the limit is 2: f(0.9) = 1.9, f(0.99) = 1.99, f(1.01) = 2.01.

**One-sided limits.** lim (x→a⁺) approaches from the right, lim (x→a⁻) from the left. **The limit exists iff both one-sided limits exist and are equal.**

::: example Worked example: a limit that does not exist
f(x) = |x|/x. For x > 0, f = 1; for x < 0, f = −1. The right limit at 0 is 1, the left limit is −1, so **lim (x→0) |x|/x does not exist**.
:::

**Limit laws.** If the limits of f and g exist: the limit of a sum, difference, product and constant multiple is the sum, difference, product and multiple of the limits; the limit of a quotient is the quotient of limits if the denominator's limit ≠ 0; lim [f(x)]ⁿ = [lim f(x)]ⁿ. For polynomials and most standard functions, **direct substitution** works: lim (x→a) P(x) = P(a).

## 2.2 Techniques for finding limits

When substitution gives **0/0** (an indeterminate form), rewrite the expression.

**(1) Factor and cancel.**

::: example Worked example
lim (x→3) (x² − 9)/(x − 3) = lim (x + 3) = **6**.
lim (x→2) (x³ − 8)/(x² − 4) = lim (x − 2)(x² + 2x + 4) / ((x − 2)(x + 2)) = (4 + 4 + 4)/4 = **3**.
:::

**(2) Rationalise** (multiply by the conjugate).

::: example Worked example
lim (x→0) (√(x + 4) − 2)/x. Multiply top and bottom by (√(x + 4) + 2): numerator becomes (x + 4) − 4 = x, so the expression is x / (x(√(x + 4) + 2)) = 1/(√(x + 4) + 2) → 1/4. Answer **1/4**.
:::

**(3) Standard limits** (x in radians):

| Limit | Value |
|---|---|
| lim (x→0) sin x / x | 1 |
| lim (x→0) (1 − cos x)/x² | 1/2 |
| lim (x→0) tan x / x | 1 |
| lim (x→0) (eˣ − 1)/x | 1 |
| lim (x→0) ln(1 + x)/x | 1 |
| lim (x→0) (aˣ − 1)/x | ln a |
| lim (x→0) (1 + x)^(1/x) = lim (x→∞) (1 + 1/x)ˣ | e |
| lim (x→a) (xⁿ − aⁿ)/(x − a) | n aⁿ⁻¹ |

::: example Worked example: using the standard limits
**(a)** lim (x→0) sin 5x / 3x = (5/3) · lim sin 5x/5x = **5/3**.
**(b)** lim (x→0) (e^{3x} − 1)/x = 3 · lim (e^{3x} − 1)/(3x) = **3**.
**(c)** lim (x→∞) (1 + 2/x)ˣ: put t = x/2, then (1 + 1/t)^{2t} → e². Answer **e²**.
**(d)** lim (x→0) (1 − cos x)/x² = lim 2 sin²(x/2)/x² = 2 · (1/2)² · lim (sin(x/2)/(x/2))² = **1/2**.
**(e)** lim (x→0) (tan 2x − sin 2x)/x³: tan 2x − sin 2x = tan 2x (1 − cos 2x), so the quotient is [tan 2x / x] · [(1 − cos 2x)/x²] → 2 · (4 · 1/2) = **4**.
:::

**(4) Squeeze theorem.** If g(x) ≤ f(x) ≤ h(x) near a and g and h both → L, then f → L. Example: |x sin(1/x)| ≤ |x| → 0, so lim (x→0) x sin(1/x) = 0.

## 2.3 Limits at infinity and infinite limits

For rational functions divide numerator and denominator by the highest power of x in the denominator.

::: example Worked example
lim (x→∞) (3x² + 2x)/(5x² − 1) = lim (3 + 2/x)/(5 − 1/x²) = **3/5**.
lim (x→∞) (2x + 1)/(x² + 3) = 0 (degree of top < degree of bottom).
lim (x→∞) (x³ + 1)/(x² + 1) = ∞ (degree of top > bottom).
:::

For differences of square roots, rationalise:

::: example Worked example
lim (x→∞) (√(x² + x) − x) = lim x/(√(x² + x) + x) = lim 1/(√(1 + 1/x) + 1) = **1/2**.
:::

The line y = L is a **horizontal asymptote** if f(x) → L as x → ±∞; x = a is a **vertical asymptote** if f(x) → ±∞ as x → a from one side. For f(x) = 1/(x − 2): vertical asymptote x = 2, horizontal asymptote y = 0. The five other indeterminate forms are ∞/∞, ∞ − ∞, 0·∞, 1^∞ and 0⁰ (Unit 4 handles them with L'Hôpital's rule).

## 2.4 Continuity

f is **continuous at a** if three things hold: (1) f(a) is defined, (2) lim (x→a) f(x) exists, (3) the limit equals f(a). Polynomials, sin, cos, eˣ are continuous everywhere; rational functions and tan, ln, √ are continuous on their domains. Sums, products, quotients (denominator ≠ 0) and compositions of continuous functions are continuous.

**Types of discontinuity**

| Type | Description | Example at x = 0 or 1 |
|---|---|---|
| Removable | limit exists but ≠ f(a) or f(a) undefined | (x² − 1)/(x − 1) at 1 |
| Jump | left and right limits exist but differ | ⌊x⌋ at integers; \|x\|/x at 0 |
| Infinite | function blows up | 1/x at 0 |

::: example Worked example: choose k to make f continuous
f(x) = (x² − 1)/(x − 1) for x ≠ 1 and f(1) = k. The limit at 1 is 2, so f is continuous only if **k = 2**.
:::

::: example Worked example: piecewise continuity
f(x) = ax + 1 for x ≤ 2; f(x) = x² − a for x > 2. Left limit at 2 = 2a + 1; right limit = 4 − a. Continuity needs 2a + 1 = 4 − a, so 3a = 3, **a = 1**.
:::

**Intermediate Value Theorem (IVT).** If f is continuous on [a, b] and N lies between f(a) and f(b), then f(c) = N for some c in (a, b). It proves a root exists: f(x) = x³ + x − 1 has f(0) = −1 < 0 and f(1) = 1 > 0, so there is a root in (0, 1). Halving the interval repeatedly (the **bisection method**, studied in Numerical Methods) finds it: f(0.5) = −0.375 < 0, so the root is in (0.5, 1); f(0.75) = 0.172 > 0, so it is in (0.5, 0.75).

## Formula and fact sheet

- lim sin x/x = 1, lim (1 − cos x)/x² = 1/2, lim (eˣ − 1)/x = 1, lim ln(1 + x)/x = 1, lim (1 + 1/x)ˣ = e, lim (aˣ − 1)/x = ln a.
- lim (xⁿ − aⁿ)/(x − a) = n aⁿ⁻¹.
- Rational at ∞: compare degrees (equal → ratio of leading coefficients; top smaller → 0).
- Continuity at a: f(a) defined, limit exists, limit = f(a).
- Limit exists ⇔ left limit = right limit.
- IVT: continuous on [a, b] takes every value between f(a) and f(b).

## Chapter summary

- A limit describes the approached value and ignores the value at the point; both one-sided limits must agree.
- For 0/0, factor, rationalise or use a standard limit; for x → ∞ divide by the highest power.
- Continuity means the graph can be drawn without lifting the pen; the three kinds of break are removable, jump and infinite.
- The IVT guarantees roots of continuous functions between sign changes.

## Practice

1. Evaluate (a) lim (x→2) (x² − 5x + 6)/(x − 2), (b) lim (x→0) (√(1 + x) − 1)/x, (c) lim (x→1) (x⁴ − 1)/(x − 1).
2. Evaluate (a) lim (x→0) sin 7x / sin 3x, (b) lim (x→0) (1 − cos 4x)/x², (c) lim (x→0) (e^{2x} − 1)/(sin 3x).
3. Evaluate (a) lim (x→∞) (4x³ − x)/(2x³ + 5), (b) lim (x→∞) (1 + 3/x)^{x}, (c) lim (x→∞) (√(x² + 3x) − x).
4. Does lim (x→0) |x|/x exist? What about lim (x→2) |x − 2|/(x − 2)?
5. Find a so that f(x) = (sin 3x)/x (x ≠ 0), f(0) = a is continuous at 0.
6. Find k if f(x) = kx + 2 (x < 1), f(x) = 3x² − k (x ≥ 1) is continuous.
7. Classify the discontinuities of f(x) = (x² − 4)/(x² − 3x + 2).
8. Show that x⁵ − 3x + 1 = 0 has a root in (0, 1).
9. Using the squeeze theorem find lim (x→∞) (sin x)/x.
10. Find the asymptotes of f(x) = (2x² + 1)/(x² − 1).

::: note Answers and worked solutions
**1.** (a) (x − 2)(x − 3)/(x − 2) → **−1**. (b) rationalise: x/(x(√(1 + x) + 1)) → **1/2**. (c) n aⁿ⁻¹ with n = 4, a = 1: **4**.
**2.** (a) (sin 7x/7x)(3x/sin 3x)(7/3) → **7/3**. (b) 1 − cos 4x = 2 sin² 2x, so 2·4 = **8** (2 sin²2x / x² = 2·(sin 2x / x)² → 2·4). (c) (e^{2x} − 1)/x → 2 and sin 3x / x → 3, so **2/3**.
**3.** (a) **2**. (b) **e³**. (c) multiply by conjugate: 3x/(√(x² + 3x) + x) → **3/2**.
**4.** The first does not exist (left −1, right +1). The second does not exist for the same reason (left −1, right +1).
**5.** The limit is 3, so **a = 3**.
**6.** Left limit at 1: k + 2; right: 3 − k. k + 2 = 3 − k ⇒ **k = 1/2**.
**7.** f = (x − 2)(x + 2)/((x − 1)(x − 2)). At x = 2: limit 4/1 = 4 exists, so a **removable** discontinuity. At x = 1: denominator → 0, numerator → −3, so an **infinite** discontinuity (vertical asymptote x = 1).
**8.** f(0) = 1 > 0, f(1) = −1 < 0, f is continuous, so by the IVT there is a root in (0, 1).
**9.** −1/x ≤ sin x / x ≤ 1/x and both bounds → 0, so the limit is **0**.
**10.** Vertical: x = 1 and x = −1. Horizontal: limit as x → ±∞ is 2, so **y = 2**.
:::
