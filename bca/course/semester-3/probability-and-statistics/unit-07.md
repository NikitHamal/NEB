---
subject: Probability and Statistics
grade: BCA Semester 3
unit: 7
title: Design of Experiment
hours: 6
area: BCA 205 · Probability and Statistics · Unit 7
---

An **experiment** deliberately changes conditions to see their effect (three teaching methods, four server configurations, two web page layouts). **Analysis of variance (ANOVA)** compares the means of **three or more** groups at once, which repeated t tests cannot do safely, since each extra test inflates the chance of a false alarm.

::: key What this unit gives you
- The idea of ANOVA, the F statistic and its distribution.
- The linear model, one-way and two-way classification (fixed effects), with worked ANOVA tables.
:::

## 7.1 Concept of analysis of variance

The total variation in the data is split into **variation between groups** (explained by the treatment) and **variation within groups** (random error). If treatment means really differ, the between-group variation is large relative to the within-group variation. **Null hypothesis H₀:** all treatment means are equal; **H₁:** at least one differs. **Assumptions:** independent observations, normally distributed errors, equal variances. **Basic design principles:** **randomisation** (random assignment of units to treatments), **replication** (several units per treatment, to estimate error) and **blocking/local control** (group similar units to remove a nuisance factor).

## 7.2 The F statistic and its distribution

**F = (variance estimate between)/(variance estimate within) = MS_between/MS_within**, a ratio of two mean squares (each a sum of squares divided by its degrees of freedom). Under H₀ it follows the **F distribution** with (df₁, df₂) degrees of freedom: positively skewed, always ≥ 0, with the shape set by the two df. Reject H₀ if F exceeds the critical value F(α; df₁, df₂) (right-tail test). **Critical values (α = 0.05):** F(2, 12) = 3.885; F(2, 6) = 5.143; F(3, 6) = 4.757.

## 7.3 The linear model

**One-way:** y_ij = μ + τ_i + ε_ij: observation j in treatment i = overall mean + treatment effect (Στ_i = 0 in the fixed-effect model, where the treatments are the only ones of interest) + random error ε_ij ~ N(0, σ²). **Two-way (one observation per cell, no interaction):** y_ij = μ + α_i + β_j + ε_ij, with α the row (treatment) effects and β the column (block) effects.

## 7.4 One-way classification

k groups with n_i observations each, total N. **Sums of squares:** SST = Σ(y − ȳ..)² (total), **SSB = Σ n_i(ȳ_i − ȳ..)²** (between treatments), **SSW = SST − SSB** (within, error). Degrees of freedom: between k − 1; within N − k; total N − 1. Mean squares MSB = SSB/(k − 1), MSW = SSW/(N − k); F = MSB/MSW.

::: example Worked example: three teaching methods
Marks: Method A: 82, 85, 88, 90, 85 (mean 86); B: 78, 74, 80, 76, 82 (mean 78); C: 70, 75, 72, 68, 75 (mean 72). N = 15, grand mean = 78.667.
SSB = 5(86 − 78.667)² + 5(78 − 78.667)² + 5(72 − 78.667)² = 5(53.78 + 0.444 + 44.44) = **493.33**. SST = **609.33**; SSW = 609.33 − 493.33 = **116.00**.

| Source | SS | df | MS | F |
|---|---|---|---|---|
| Between methods | 493.33 | 2 | 246.67 | **25.52** |
| Within (error) | 116.00 | 12 | 9.67 | |
| Total | 609.33 | 14 | | |

F = 246.67/9.667 = 25.52 > F(2, 12) = 3.885 (p ≈ 0.00005): **reject H₀**: the methods do not all give the same mean marks. ANOVA only says that *some* means differ; a post-hoc test (Tukey, least significant difference) would say which.
:::

## 7.5 Two-way classification (one observation per cell)

Rows = a treatments (e.g. crop varieties), columns = b blocks (e.g. fields); one observation in each of the a × b cells, N = ab. With grand total G and correction factor **CF = G²/N**: SST = Σy² − CF; **SSR = Σ(row totals)²/b − CF**; **SSC = Σ(column totals)²/a − CF**; **SSE = SST − SSR − SSC**. Degrees of freedom: rows a − 1, columns b − 1, error (a − 1)(b − 1), total ab − 1. F_rows = MSR/MSE, F_cols = MSC/MSE. Blocking removes the column variation from the error, making the treatment test more sensitive. With **m > 1 observations per cell** an **interaction** term (does the row effect depend on the column?) can also be tested, with error df ab(m − 1).

::: example Worked example: three varieties in four blocks
| | B1 | B2 | B3 | B4 | Row total |
|---|---|---|---|---|---|
| V1 | 20 | 22 | 19 | 24 | 85 |
| V2 | 25 | 27 | 25 | 28 | 105 |
| V3 | 18 | 21 | 17 | 21 | 77 |
| Column total | 63 | 70 | 61 | 73 | **267** |

CF = 267²/12 = **5,940.75**. Σy² = 6,079, so SST = 138.25. SSR = (85² + 105² + 77²)/4 − CF = 6,044.75 − 5,940.75 = **104.00**. SSC = (63² + 70² + 61² + 73²)/3 − CF = 5,973 − 5,940.75 = **32.25**. SSE = 138.25 − 104 − 32.25 = **2.00**.

| Source | SS | df | MS | F | F(0.05) |
|---|---|---|---|---|---|
| Varieties (rows) | 104.00 | 2 | 52.00 | **156.0** | 5.143 |
| Blocks (columns) | 32.25 | 3 | 10.75 | **32.25** | 4.757 |
| Error | 2.00 | 6 | 0.333 | | |
| Total | 138.25 | 11 | | | |

Both F values exceed their critical values: varieties differ significantly, and the blocks differ too, so blocking was worthwhile.
:::

**Using software:** SPSS *Analyze → Compare Means → One-Way ANOVA* or *General Linear Model → Univariate*; Excel *Data Analysis → Anova: Single Factor / Two-Factor Without Replication*; Python `scipy.stats.f_oneway`.

## Formula and fact sheet

- F = MSB/MSW with (k − 1, N − k) df; reject if F > F_critical.
- One-way: SST = SSB + SSW; SSB = Σn_i(ȳ_i − ȳ)².
- Two-way: CF = G²/N; SSR, SSC from totals; SSE = SST − SSR − SSC; error df (a − 1)(b − 1).
- Principles: randomisation, replication, blocking.

## Chapter summary

- ANOVA compares several means by splitting total variation into between and within parts and testing their ratio with the F distribution.
- One-way ANOVA handles one factor; two-way ANOVA adds a blocking factor to reduce error.
- A significant F says means differ somewhere; follow-up tests locate the difference.

## Practice

1. Why can't we simply run several t tests to compare three means?
2. Samples A: 6, 8, 7; B: 9, 11, 10; C: 5, 4, 6. Construct the ANOVA table and test at 5% (F(2, 6) = 5.143).
3. State the assumptions of ANOVA.
4. Explain randomisation, replication and blocking.
5. In a two-way design with 4 rows and 5 columns, give the degrees of freedom of each source.
6. What does a significant F-ratio not tell you?

::: note Answers and worked solutions
**1.** Each test has a 5% chance of a false positive, so repeated testing inflates the overall error rate; ANOVA tests all means with one test.
**2.** Means 7, 10, 5; grand mean 7.333. SSB = 3(0.111 + 7.111 + 5.444) = **38.0**; SSW = (1 + 1 + 0) + (1 + 1 + 0) + (1 + 1 + 0) = **6.0**; SST = 44. MSB = 19, MSW = 1, **F = 19.0** > 5.143 → **reject H₀**; the means differ.
**3.** Independent observations, normal errors, equal variances across groups.
**4.** Randomisation: assign units to treatments by chance, avoiding bias. Replication: repeat each treatment to estimate error. Blocking: group similar units to remove an unwanted source of variation.
**5.** Rows 3, columns 4, error 12, total 19.
**6.** Which means differ, by how much, or whether the differences matter in practice.
:::
