---
subject: Probability and Statistics
grade: BCA Semester 3
unit: 6
title: Sample Survey Methods
hours: 10
area: BCA 205 · Probability and Statistics · Unit 6
---

This unit gives the **designs** for choosing a sample and the matching **estimators**, then the sampling distributions (z, t, χ²) used to make confidence statements. Every number below was recomputed by `bca/tools/check_stats.py`.

::: key What this unit gives you
- Simple random sampling with and without replacement; stratified, systematic, cluster, multistage and PPS sampling.
- Ratio and regression estimation; estimating the population total and its variance.
- Sampling distributions: z, t and χ² with confidence intervals and tests.
:::

## 6.1 Types of sampling

**Probability sampling:** simple random, stratified random, systematic, cluster, multistage, PPS. **Non-probability:** convenience, judgement (purposive), quota, snowball: no valid sampling-error estimate. Notation: population size N, sample size n, f = n/N, population mean Ȳ and variance S² = Σ(Yᵢ − Ȳ)²/(N − 1), sample mean ȳ and variance s².

## 6.2 Simple random sampling (SRS)

Every possible sample of size n has the same chance. Drawn **without replacement (SRSWOR)** by lottery or random numbers (a unit cannot appear twice) or **with replacement (SRSWR)** (a unit may repeat). Number of possible samples: C(N, n) for SRSWOR, Nⁿ for SRSWR.

| | SRSWOR | SRSWR |
|---|---|---|
| Estimate of mean | ȳ = Σy/n (unbiased) | ȳ |
| Variance of ȳ | (1 − f) S²/n | σ²/n = (N − 1)S²/(Nn) |
| Estimated | (1 − f) s²/n | s²/n |
| Estimate of total Y | Ŷ = Nȳ | Nȳ |
| Variance of total | N²(1 − f)s²/n | N²s²/n |

(1 − f) is the **finite population correction**; sampling without replacement is more precise.

::: example Worked example
A population of N = 200 students; an SRSWOR of n = 20 gives ȳ = 52 marks and s = 8. f = 0.1. Estimated Var(ȳ) = (1 − 0.1) × 64/20 = **2.88**, SE = **1.697**. 95% confidence interval for the mean: 52 ± 1.96 × 1.697 = **(48.67, 55.33)**. Estimated total marks Ŷ = 200 × 52 = **10,400**, SE(Ŷ) = 200 × 1.697 = **339.41**. With replacement the variance would be 64/20 = 3.2, larger than 2.88.
:::

## 6.3 Stratified random sampling

Divide the population into non-overlapping, **homogeneous strata** (by district, class, income band), then draw an SRS in each. Estimate: **ȳ_st = Σ W_h ȳ_h**, W_h = N_h/N. **Var(ȳ_st) = Σ W_h² (1 − f_h) s_h²/n_h.** It is more precise than SRS when strata are internally similar and differ from one another, guarantees representation of subgroups, and allows separate estimates per stratum.

**Allocation of n:** **proportional** n_h = n N_h/N; **equal**; **optimum/Neyman** n_h ∝ N_h S_h (larger or more variable strata get more; with different costs ∝ N_h S_h/√c_h).

::: example Worked example
Two strata: N₁ = 300 (ȳ₁ = 60, s₁ = 10), N₂ = 700 (ȳ₂ = 50, s₂ = 8); total n = 100, proportional allocation: n₁ = 30, n₂ = 70, W = 0.3 and 0.7. ȳ_st = 0.3 × 60 + 0.7 × 50 = **53**. f₁ = f₂ = 0.1. Var = 0.3² × 0.9 × 100/30 + 0.7² × 0.9 × 64/70 = 0.27 + 0.4032 = **0.6732**, SE = **0.8205**. An SRS of the same 100 would have variance about **0.8622**, so stratification cut the variance by **22%**. **Neyman allocation:** n₁ ∝ 300 × 10 = 3000, n₂ ∝ 700 × 8 = 5600 → n₁ = 100 × 3000/8600 = **34.9 ≈ 35**, n₂ = **65.1 ≈ 65**.
:::

## 6.4 Systematic sampling

Select every **k-th** unit after a random start: k = N/n (the sampling interval); choose a random start r from 1…k; the sample is r, r + k, r + 2k, …. Simple, spreads the sample evenly over an ordered list, no need for a full renumbering. **Danger:** if the list has a **periodic pattern** matching k (every 7th day of sales data) the sample is biased. Equivalent to SRS if the list is in random order.

::: example Worked example
N = 1,000, n = 50: k = 20. Random start 7 → units **7, 27, 47, 67, 87, …, 987**. If N is not a multiple of n, use the nearest integer k or a circular list.
:::

## 6.5 Cluster and multistage sampling

**Cluster sampling:** divide the population into **clusters** (villages, schools, wards), randomly select some clusters, and survey **all** units in them. Cheap and practical when no unit list exists and units are scattered. Clusters are internally *heterogeneous* ideally; the higher the similarity within clusters (intra-cluster correlation) the less precise it is than SRS of the same size. **Multistage sampling** samples in stages: districts → wards → households → persons; each stage uses SRS, systematic or PPS sampling. It needs a list only for chosen units at each stage, and is the standard design for national surveys such as the Nepal Living Standards Survey and Demographic and Health Survey.

## 6.6 Probability proportional to size (PPS) sampling

When clusters differ in size, selecting each with probability **proportional to its size** removes the bias of giving small villages the same chance as big ones. With p_i = M_i/ΣM, the unbiased **Hansen–Hurwitz estimator** for the total with n draws is **Ŷ = (1/n) Σ y_i/p_i**, and its variance is estimated from the spread of the y_i/p_i values.

::: example Worked example
Three villages have 100, 300 and 600 households (total 1,000), so p = 0.1, 0.3, 0.6. Two draws select village 2 (y = 900 persons) and village 3 (y = 1,500). Ŷ = ½(900/0.3 + 1,500/0.6) = ½(3,000 + 2,500) = **2,750** persons.
:::

## 6.7 Ratio and regression methods of estimation

If an **auxiliary variable x** correlated with y is known for the whole population (total X, mean X̄), it improves precision. **Ratio estimator:** R̂ = ȳ/x̄; **ȳ_R = R̂ X̄**, **Ŷ_R = R̂ X**. It is better than ȳ when y is roughly proportional to x (the line through the origin). **Regression estimator:** ȳ_lr = ȳ + b(X̄ − x̄), with b the sample regression coefficient of y on x; best when y is linearly related to x (with any intercept), and never worse than the ratio estimator in large samples. Both are slightly biased but precise.

::: example Worked example
N = 100 farms with total area X = 5,000 ha (X̄ = 50). A sample of n = 10 gives mean production ȳ = 30 and mean area x̄ = 48. R̂ = 30/48 = 0.625. Estimated mean production = 0.625 × 50 = **31.25**; total = 0.625 × 5,000 = **3,125**. The raw ȳ = 30 would underestimate because the sample happened to have below-average farms (48 < 50); the ratio estimator corrects this.
:::

Ratio and regression methods also apply **within strata** (separate or combined estimators). **Estimating the population total and its variance:** Ŷ = Nȳ under SRS; Ŷ_st = Σ N_h ȳ_h under stratification with Var(Ŷ_st) = Σ N_h²(1 − f_h)s_h²/n_h.

## 6.8 Sampling distributions: z, t and χ²

The **sampling distribution** of a statistic is its distribution over all possible samples. The **central limit theorem**: for large n the distribution of x̄ is approximately normal with mean μ and **standard error σ/√n**, whatever the population shape.

| Distribution | When used | Statistic |
|---|---|---|
| **z (standard normal)** | mean, σ known or n large (≥ 30); proportions | z = (x̄ − μ)/(σ/√n) |
| **Student's t** | mean, σ unknown, small n; df = n − 1 | t = (x̄ − μ)/(s/√n) |
| **χ² (chi-square)** | tests of independence/goodness of fit; variance | χ² = Σ(O − E)²/E; df depends on the test |

The t distribution is bell-shaped but heavier-tailed than z and approaches z as df grows. **Critical values (5% level):** z = 1.645 (one-tail), 1.96 (two-tail), 2.576 (1% two-tail); t two-tail 0.05: df 9 → 2.262, 14 → 2.145, 15 → 2.131, 19 → 2.093; χ² at 5%: df 1 → 3.841, 2 → 5.991, 3 → 7.815, 5 → 11.070.

::: example Worked example: confidence interval with t
A sample of n = 16 response times has mean 52.5 ms and s = 6. SE = 6/√16 = 1.5; df = 15, t₀.₀₂₅ = 2.1314. 95% CI = 52.5 ± 2.1314 × 1.5 = **(49.30, 55.70)** ms. Using z would give the narrower (49.56, 55.44), falsely overconfident for n = 16.
:::

::: example Worked example: z test
A system claims a mean load time of 50 s (σ = 10). A sample of n = 36 gives x̄ = 53. z = (53 − 50)/(10/√36) = 3/1.667 = **1.8**. Two-tailed p-value = **0.0719** > 0.05, so we do **not** reject the claim at 5% (|z| < 1.96).
:::

::: example Worked example: χ² test of independence
Preference for a language by gender: 30 men and 20 women choose Java, and 20 men and 30 women choose Python, observed [[30, 20], [20, 30]]. Totals are 50 per row and column, so each expected count is 25. χ² = Σ(O − E)²/E = 4 × 25/25 = **4.0**, df = (2 − 1)(2 − 1) = 1; critical value 3.841; p = 0.0455 → **reject independence at 5%**: preference appears related to gender in this sample.
Goodness of fit: a die rolled 60 times gives counts 8, 12, 9, 11, 10, 10; expected 10 each; χ² = (4 + 4 + 1 + 1 + 0 + 0)/10 = **1.0** < 11.07 (df 5): consistent with a fair die.
:::

## Formula and fact sheet

- SRSWOR: Var(ȳ) = (1 − f)s²/n; total Ŷ = Nȳ, Var = N²(1 − f)s²/n. SRSWR: s²/n.
- Stratified: ȳ_st = ΣW_hȳ_h; Var = ΣW_h²(1 − f_h)s_h²/n_h; Neyman n_h ∝ N_hS_h.
- Systematic: k = N/n, random start. PPS: Ŷ = (1/n)Σy_i/p_i. Ratio: ȳ_R = (ȳ/x̄)X̄.
- SE of mean σ/√n; z = 1.96 (95%); t with df n − 1; χ² = Σ(O − E)²/E, df = (r − 1)(c − 1).

## Chapter summary

- SRS is the baseline; stratification gains precision from homogeneous strata; systematic sampling is simple but pattern-sensitive; cluster and multistage designs cut cost; PPS handles unequal clusters.
- Ratio and regression estimators exploit an auxiliary variable.
- The CLT justifies z; t replaces z for small n with unknown σ; χ² tests counts.

## Practice

1. N = 500, an SRSWOR of 50 gives ȳ = 40 and s = 6. Find the estimated variance of ȳ, the 95% CI, and the estimated total with its SE.
2. Two strata of sizes 400 and 600 have s = 5 and 10. Find the Neyman allocation for n = 100.
3. Select a systematic sample of 8 from N = 80 with random start 5.
4. Differentiate stratified and cluster sampling.
5. A sample ȳ = 25 with x̄ = 20, population mean X̄ = 22. Find the ratio estimate.
6. n = 25, x̄ = 100, s = 15: 95% CI (t₀.₀₂₅ with 24 df = 2.064).
7. Test independence for [[40, 10], [20, 30]] at 5%.
8. When is t used instead of z?

::: note Answers and worked solutions
**1.** f = 0.1; Var = 0.9 × 36/50 = **0.648**, SE = 0.805; CI 40 ± 1.96 × 0.805 = **(38.42, 41.58)**; total 500 × 40 = **20,000**, SE = 500 × 0.805 = **402.5**.
**2.** N₁S₁ = 2,000; N₂S₂ = 6,000: n₁ = 100 × 2,000/8,000 = **25**, n₂ = **75**.
**3.** k = 10; units **5, 15, 25, 35, 45, 55, 65, 75**.
**4.** Stratified: sample *within every* homogeneous stratum, improves precision. Cluster: sample *whole* clusters, reduces cost, usually less precise.
**5.** R̂ = 25/20 = 1.25; estimate = 1.25 × 22 = **27.5**.
**6.** SE = 15/5 = 3; CI = 100 ± 2.064 × 3 = **(93.81, 106.19)**.
**7.** Row totals 50, 50; column totals 60, 40; expected: 30, 20 / 30, 20. χ² = (10²/30 + 10²/20) × 2 = (3.333 + 5) × 2 = **16.67** > 3.841 → **reject independence**.
**8.** When σ is unknown and the sample is small (n < 30), the data being roughly normal.
:::
