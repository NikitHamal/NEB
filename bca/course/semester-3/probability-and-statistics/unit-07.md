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

## 7.6 Pictures of ANOVA and experimental design

```svgfig label="7.1" caption="Splitting the variation (three teaching methods, five students each). Left: every mark is a dot; the red bars are the group means 86, 78 and 72 and the dashed line is the grand mean 78.67. The dots sit tightly around their own bar but the bars are far apart. Right: the total sum of squares 609.33 divides into SSB = 493.33 (between methods, 81%) and SSW = 116.00 (within, 19%)."
f = Fig(580, 225)
ax = Axes(f, 40, 22, 270, 160, (0.4, 3.6), (62, 94))
ax.grid(1, 8, labels=False); ax.axes("", "marks")
data = {1: [82, 85, 88, 90, 85], 2: [78, 74, 80, 76, 82], 3: [70, 75, 72, 68, 75]}
for g, ys in data.items():
    for i, y in enumerate(ys): ax.pt(g - 0.2 + i * 0.1, y, "", r=3.6, color=TEAL)
    m = sum(ys) / 5
    f.line(ax.X(g - 0.32), ax.Y(m), ax.X(g + 0.32), ax.Y(m), color=RED, sw=3)
    f.text(ax.X(g), ax.Y(62) + 13, "Method " + "ABC"[g - 1], size=10.5, color=SLATE, bold=True)
ax.hline(78.667, color=AMBER, dash=True, sw=1.6)
f.text(ax.X(0.45), ax.Y(78.667) + 13, "grand mean 78.67", size=10, color=AMBER, bold=True, anchor="start")
w = 230; x0 = 335
f.text(x0 + w / 2, 40, "SST = 609.33 (df 14)", size=11.5, color=NAVY, bold=True)
f.box(x0, 52, w * 0.8096, 40, "SSB = 493.33", fill="#bfdbfe", stroke=NAVY, bold=True, size=11)
f.box(x0 + w * 0.8096, 52, w * 0.1904, 40, "", fill="#fde68a", stroke=AMBER)
f.text(x0 + w * 0.8096 + w * 0.095, 110, "SSW 116.00", size=10.5, color=AMBER, bold=True)
f.text(x0 + w * 0.4, 112, "df 2", size=10.5, color=NAVY, bold=True); f.text(x0 + w / 2, 150, "MSB = 246.67,  MSW = 9.67", size=11, color=SLATE, bold=True)
f.text(x0 + w / 2, 172, "F = 246.67 / 9.67 = 25.52", size=12, color=RED, bold=True)
f.text(x0 + w / 2, 194, "(within df = 12)", size=10.5, color=SLATE, italic=True)
```

```svgfig label="7.2" caption="The F distribution with (2, 12) degrees of freedom. It is skewed right and never negative. The 5% critical value is 3.885; the shaded tail has area 0.05. The teaching-method experiment gave F = 25.52, far to the right of the critical value, so H₀ (equal means) is rejected with p ≈ 0.00005."
import math
f = Fig(580, 200)
B = math.gamma(1) * math.gamma(6) / math.gamma(7)
F = lambda x: (2 / 12) * (1 + 2 * x / 12) ** (-7) / B
ax = Axes(f, 60, 18, 460, 140, (0, 8), (0, 1.1))
ax.grid(1, 0.25, labels=False); ax.axes("F", "")
ax.area(F, 3.885, 8, fill="#fbbf24", opacity=0.85)
ax.curve(F, 0.02, 8, color=NAVY, sw=2.6)
for v in range(0, 9): f.text(ax.X(v), ax.Y(0) + 14, str(v), size=10.5, color=SLATE)
ax.vline(3.885, 0, 0.9, color=RED, dash=False, sw=1.8)
f.text(ax.X(3.885) + 6, ax.Y(0.88), "critical 3.885", size=11, color=RED, bold=True, anchor="start")
f.text(ax.X(5.4), ax.Y(0.12) - 8, "reject H₀ (5%)", size=11, color=AMBER, bold=True)
f.arrow([(ax.X(6.9), ax.Y(0.3)), (ax.X(7.95), ax.Y(0.3))], color=TEAL, sw=2)
f.text(ax.X(7.95), ax.Y(0.5), "observed F = 25.52 (off the scale)", size=10.5, color=TEAL, bold=True, anchor="end")
f.text(290, 192, "Large F means the between-group variation is large compared with the within-group noise.", size=10.5, color=SLATE, italic=True)
```

```svgfig label="7.3" caption="A randomised complete block layout: 3 varieties (V1, V2, V3) in 4 blocks (fields). Each block holds every variety exactly once, in random order, so soil differences between blocks can be measured (SSC) and removed from the error. Randomisation protects against bias, blocking removes a known source of variation, and replication (4 plots per variety) lets the error be estimated."
f = Fig(580, 200)
order = [["V2", "V1", "V3"], ["V1", "V3", "V2"], ["V3", "V2", "V1"], ["V2", "V3", "V1"]]
col = {"V1": ("#bfdbfe", NAVY), "V2": ("#fde68a", AMBER), "V3": ("#a7f3d0", TEAL)}
for b, plots in enumerate(order):
    x = 20 + b * 140
    f.text(x + 55, 18, f"Block {b + 1}", size=11.5, color=NAVY, bold=True)
    for i, v in enumerate(plots):
        f.box(x, 28 + i * 40, 110, 36, v, fill=col[v][0], stroke=col[v][1], bold=True, size=12.5)
f.text(290, 168, "Rows of the ANOVA table: varieties (df 2), blocks (df 3), error (df 6), total (df 11)", size=11, color=SLATE, bold=True)
f.text(290, 188, "Randomise inside each block; never put the same variety in the same corner of every block.", size=10.5, color=SLATE, italic=True)
```

```svgfig label="7.4" caption="Partition of the total sum of squares in a two-way design (worked example of Section 7.5): SST = 138.25 splits into varieties 104.00, blocks 32.25 and error 2.00. Taking blocks out of the error shrinks SSE to 2.00, which is why both F ratios (156.0 and 32.25) are so large."
f = Fig(580, 170)
f.box(205, 8, 170, 36, "SST = 138.25  (df 11)", fill=NAVY, color="#ffffff", bold=True, size=12)
for x, t, d, fl, st in [(40, "SSR = 104.00\ndf 2, MS 52.00\nF = 156.0", "varieties", "#bfdbfe", NAVY), (215, "SSC = 32.25\ndf 3, MS 10.75\nF = 32.25", "blocks", "#a7f3d0", TEAL), (390, "SSE = 2.00\ndf 6, MS 0.333", "error", "#fde68a", AMBER)]:
    f.box(x, 86, 150, 54, t, fill=fl, stroke=st, bold=True, size=11)
    f.text(x + 75, 76, d, size=11, color=st, bold=True)
    f.arrow([(290, 44), (290, 56), (x + 75, 56), (x + 75, 64)])
f.text(290, 160, "Critical F(0.05): varieties F(2, 6) = 5.143;  blocks F(3, 6) = 4.757;  both exceeded", size=10.5, color=SLATE, italic=True)
```

## 7.7 Eight uses of ANOVA and designed experiments

1. **Comparing many means with one test.** Three or more groups, such as three teaching methods, can be compared in a single test. Running several t tests would inflate the chance of a false alarm well above 5%. ANOVA keeps the overall error at the stated level.
2. **Choosing the best crop variety or fertiliser.** Agricultural stations in Nepal compare paddy or maize varieties on several plots and blocks. ANOVA shows whether the yield differences are real or just soil variation. The blocked design of Figure 7.3 makes the test far more sensitive.
3. **Comparing algorithms and systems.** A developer runs three sorting programs on four data sets and compares the times. The two-way table separates the algorithm effect from the data-set effect. This avoids blaming an algorithm for a hard data set.
4. **A/B/n testing of products.** When a company tests four versions of an app screen, one ANOVA tells whether any version differs. Only then is a follow-up test used to find which one. This is cheaper than testing each pair separately.
5. **Quality control across machines or shifts.** A factory compares the output weight of three machines and two shifts. A significant F points to the machine or shift that needs adjusting. Managers can then target the fault instead of retraining everyone.
6. **Medical and psychological trials.** Doses of a drug or kinds of therapy are compared on groups of patients. ANOVA tells whether the treatments differ before doctors study which one is best. Randomisation protects patients from biased allocation.
7. **Education research.** A college compares exam marks across teaching methods, batches or campuses. A significant F supports a change in method; a non-significant one saves money. Section 7.4 works exactly such an example.
8. **Feature and model selection in data science.** The F statistic is used to rank features by how well they separate classes, and to compare the fit of nested regression models. It also underlies the overall F test in regression output. Many software reports show an ANOVA table by default.

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

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). The response times (ms) of three servers, measured four times each, are S1: 14, 16, 15, 17; S2: 19, 21, 20, 22; S3: 12, 13, 15, 12. Construct the one-way ANOVA table and test at the 5% level whether the servers differ. (F(2, 9) = 4.256 at 5%.)**

*Introduction.* One-way ANOVA tests H₀: all group means are equal against H₁: at least one differs, by comparing variation between groups with variation within them (Figure 7.1).

*Means.* S1 = 62/4 = 15.5; S2 = 82/4 = 20.5; S3 = 52/4 = 13.0. N = 12 and the grand mean = 196/12 = 16.333.

*Sums of squares.* SSB = 4[(15.5 − 16.333)² + (20.5 − 16.333)² + (13 − 16.333)²] = 4(0.694 + 17.361 + 11.111) = **116.67**. SST = Σ(y − 16.333)² = **132.67**. SSW = 132.67 − 116.67 = **16.00**.

| Source | SS | df | MS | F |
|---|---|---|---|---|
| Between servers | 116.67 | 2 | 58.33 | **32.81** |
| Within (error) | 16.00 | 9 | 1.778 | |
| Total | 132.67 | 11 | | |

*Decision.* F = 58.33/1.778 = 32.81 is greater than F(2, 9) = 4.256, and the p-value is about 0.00007, so **reject H₀**.

*Conclusion.* The servers do not all have the same mean response time. ANOVA does not say which; a follow-up test (Tukey or least significant difference) would show that S2 is slowest and S3 fastest.

**Q2 (5 marks). State the assumptions of ANOVA and explain the three principles of experimental design: randomisation, replication and blocking.**

*Introduction.* The F test is valid only when the data come from a properly designed experiment and meet some conditions.

*Assumptions.*

1. **Independence:** observations are independent of each other.
2. **Normality:** the errors in each group are approximately normal.
3. **Equal variances:** every group has about the same spread (homogeneity).
4. **Additivity:** in the two-way model, row and column effects simply add up (no interaction).

*Three principles (Figure 7.3).*

1. **Randomisation:** treatments are assigned to plots or subjects by chance. It removes selection bias and makes the error terms independent.
2. **Replication:** each treatment is repeated on several units. This allows the error variance to be estimated and gives more precise means.
3. **Blocking (local control):** similar units are grouped into blocks and every treatment appears once in each block. This removes known variation such as soil or batch differences from the error.

*Example.* To compare three paddy varieties on four fields, plant each variety once in every field (blocking), choose positions at random (randomisation), and use all four fields (replication). *Conclusion.* A significant F is trustworthy only when these principles were followed.

**Q3 (10 marks). Explain two-way ANOVA (one observation per cell). The running times (seconds) of three algorithms on four data sets were: A1: 12, 15, 11, 14; A2: 18, 22, 17, 21; A3: 14, 17, 13, 16. Prepare the ANOVA table and test both effects at 5%. (F(2, 6) = 5.143, F(3, 6) = 4.757.)**

*Introduction.* **Two-way classification** studies two factors at once: here algorithms (rows, treatments) and data sets (columns, blocks). The model is y_ij = μ + α_i + β_j + ε_ij. The total variation is split into rows, columns and error, so block-to-block differences are removed from the error and the test of algorithms becomes sharper (Figure 7.4).

*Steps.*

1. Compute the grand total G and correction factor CF = G²/N.
2. SST = Σy² − CF; SSR = Σ(row totals)²/b − CF; SSC = Σ(column totals)²/a − CF.
3. SSE = SST − SSR − SSC, with df (a − 1)(b − 1).
4. Form the mean squares and the F ratios; compare with the critical values.

*Calculation.* Row totals: A1 = 52, A2 = 78, A3 = 60. Column totals: 44, 54, 41, 51. G = **190**, N = 12. CF = 190²/12 = **3008.33**. Σy² = 686 + 1538 + 910 = **3134**.

SST = 3134 − 3008.33 = **125.67**. SSR = (52² + 78² + 60²)/4 − CF = 3097 − 3008.33 = **88.67**. SSC = (44² + 54² + 41² + 51²)/3 − CF = 3044.67 − 3008.33 = **36.33**. SSE = 125.67 − 88.67 − 36.33 = **0.67**.

| Source | SS | df | MS | F | F(0.05) | Decision |
|---|---|---|---|---|---|---|
| Algorithms (rows) | 88.67 | 2 | 44.33 | **399.0** | 5.143 | reject H₀ |
| Data sets (columns) | 36.33 | 3 | 12.11 | **109.0** | 4.757 | reject H₀ |
| Error | 0.67 | 6 | 0.111 | | | |
| Total | 125.67 | 11 | | | | |

*One-way versus two-way (Table).*

| Point | One-way | Two-way (no replication) |
|---|---|---|
| Factors | one | two (treatment and block) |
| Error df | N − k | (a − 1)(b − 1) |
| Error size | includes block variation | block variation removed |
| F tests | one | two |
| Example | three teaching methods | three algorithms on four data sets |

*Interpretation.* Both F ratios far exceed their critical values: the algorithms differ in running time, and the data sets differ in difficulty too, so blocking was worthwhile. A2 (mean 19.5 s) is slowest and A1 (13.0 s) fastest.

*Conclusion.* Two-way ANOVA identified both effects with an error sum of squares of only 0.67. A follow-up multiple-comparison test would confirm which algorithm pairs differ; ANOVA alone says only that the means are not all equal.
