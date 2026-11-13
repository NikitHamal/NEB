---
subject: Probability and Statistics
grade: BCA Semester 3
unit: 7
title: Design of Experiment
hours: 6
area: BCA 205 · Probability and Statistics · Unit 7
---

An **experiment** deliberately changes conditions to see their effect (three teaching methods, four server configurations, two web page layouts). **Analysis of variance (ANOVA)** compares the means of **three or more** groups at once, which repeated *t* tests cannot do safely, since each extra test inflates the chance of a false alarm.

::: key What this unit gives you
- The idea of ANOVA, the F statistic and its distribution.
- The linear model, one-way and two-way classification (fixed effects), with worked ANOVA tables.
:::

## 7.1 Concept of analysis of variance

The total variation in the data is split into **variation between groups** (explained by the treatment) and **variation within groups** (random error). If treatment means really differ, the between-group variation is large relative to the within-group variation. **Null hypothesis $H_{0}$:** all treatment means are equal; **$H_{1}$:** at least one differs. **Assumptions:** independent observations, normally distributed errors, equal variances. **Basic design principles:** **randomisation** (random assignment of units to treatments), **replication** (several units per treatment, to estimate error) and **blocking/local control** (group similar units to remove a nuisance factor).

## 7.2 The F statistic and its distribution

**F = (variance estimate between)/(variance estimate within) = $\frac{M S_{b} \mathrm{etween}}{M S_{w} \mathrm{ithin}}$**, a ratio of two mean squares (each a sum of squares divided by its degrees of freedom). Under $H_{0}$ it follows the **F distribution** with $(d f_{1} ,\  d f_{2})$ degrees of freedom: positively skewed, always ≥ 0, with the shape set by the two df. Reject $H_{0}$ if F exceeds the critical value $F (\alpha ;\  d f_{1} ,\  d f_{2})$ (right-tail test). **Critical values $(\alpha = 0.05)$:** $F (2 ,\  12) = 3.885 ;\  F (2 ,\  6) = 5.143 ;\  F (3 ,\  6) = 4.757$.

## 7.3 The linear model

**One-way:** $y_{i} j = \mu + \tau_{i} + \epsilon_{i} j$: observation *j* in treatment *i* = overall mean + treatment effect ($\sum \tau_{i} = 0$ in the fixed-effect model, where the treatments are the only ones of interest) + random error $\epsilon_{i} j$ ~ $N (0 ,\  \sigma^{2})$. **Two-way (one observation per cell, no interaction):** $y_{i} j = \mu + \alpha_{i} + \beta_{j} + \epsilon_{i} j$, with *α* the row (treatment) effects and *β* the column (block) effects.

## 7.4 One-way classification

*k* groups with $n_{i}$ observations each, total N. **Sums of squares:** SST = Σ(y − ȳ..)² (total), **SSB = Σ n_i(ȳ_i − ȳ..)²** (between treatments), **$\mathrm{SSW} = \mathrm{SST} - \mathrm{SSB}$** (within, error). Degrees of freedom: between $k - 1$; within $N - k$; total $N - 1$. Mean squares MSB = SSB/(k − 1), MSW = SSW/(N − $k ) ;\  F$ = MSB/MSW.

::: example Worked example: three teaching methods
Marks: Method A: 82, 85, 88, 90, 85 (mean 86); B: 78, 74, 80, 76, 82 (mean 78); C: 70, 75, 72, 68, 75 (mean 72). $N = 15$, grand mean = 78.667.

$\mathrm{SSB} = 5 (86 - 78.667)^{2} + 5 (78 - 78.667)^{2} + 5 (72 - 78.667)^{2} = 5 (53.78 + 0.444 + 44.44)$ = **493.33**. SST = **609.33**; $\mathrm{SSW} = 609.33 - 493.33$ = **116.00**.

| Source | SS | df | MS | F |

|---|---|---|---|---|

| Between methods | 493.33 | 2 | 246.67 | **25.52** |

| Within (error) | 116.00 | 12 | 9.67 |  |

| Total | 609.33 | 14 |  |  |

$F = 246.67 / 9.667 = 25.52 > F (2 ,\  12) = 3.885 (p \approx 0.00005)$: **reject $H_{0}$**: the methods do not all give the same mean marks. ANOVA only says that *some* means differ; a post-hoc test (Tukey, least significant difference) would say which.
:::

## 7.5 Two-way classification (one observation per cell)

Rows = a treatments (e.g. crop varieties), columns = *b* blocks (e.g. fields); one observation in each of the $a \times b$ cells, $N = a b$. With grand total G and correction factor **$C F = \frac{G^{2}}{N}$**: $\mathrm{SST} = \sum y^{2} - C F$; **$\mathrm{SSR} = \frac{\sum (\mathrm{row} \mathrm{totals})^{2}}{b} - C F$**; **$\mathrm{SSC} = \frac{\sum (\mathrm{column} \mathrm{totals})^{2}}{a} - C F$**; **$\mathrm{SSE} = \mathrm{SST} - \mathrm{SSR} - \mathrm{SSC}$**. Degrees of freedom: rows $a - 1$, columns $b - 1$, error $(a - 1) (b - 1)$, total $a b - 1$. $F_{r} \mathrm{ows}$ = MSR/MSE, $F_{c} \mathrm{ols}$ = MSC/MSE. Blocking removes the column variation from the error, making the treatment test more sensitive. With **$m > 1$ observations per cell** an **interaction** term (does the row effect depend on the column?) can also be tested, with error df ab(m − 1).

::: example Worked example: three varieties in four blocks
|  | B1 | B2 | B3 | B4 | Row total |

|---|---|---|---|---|---|

| V1 | 20 | 22 | 19 | 24 | 85 |

| V2 | 25 | 27 | 25 | 28 | 105 |

| V3 | 18 | 21 | 17 | 21 | 77 |

| Column total | 63 | 70 | 61 | 73 | **267** |

$C F = 267^{2} / 12$ = **5,940.75**. $\sum y^{2}$ = 6,079, so $\mathrm{SST} = 138.25$. $\mathrm{SSR} = \frac{(85^{2} + 105^{2} + 77^{2})}{4} - C F$ = 6,044.75 − 5,940.75 = **104.00**. $\mathrm{SSC} = \frac{(63^{2} + 70^{2} + 61^{2} + 73^{2})}{3} - C F$ = 5,973 − 5,940.75 = **32.25**. $\mathrm{SSE} = 138.25 - 104 - 32.25$ = **2.00**.

| Source | SS | df | MS | F | $F (0.05)$ |

|---|---|---|---|---|---|

| Varieties (rows) | 104.00 | 2 | 52.00 | **156.0** | 5.143 |

| Blocks (columns) | 32.25 | 3 | 10.75 | **32.25** | 4.757 |

| Error | 2.00 | 6 | 0.333 |  |  |

| Total | 138.25 | 11 |  |  |  |

Both F values exceed their critical values: varieties differ significantly, and the blocks differ too, so blocking was worthwhile.
:::

**Using software:** SPSS *Analyze → Compare Means → One-Way ANOVA* or *General Linear Model → Univariate*; Excel *Data Analysis → Anova: Single Factor / Two-Factor Without Replication*; Python `scipy.stats.f_oneway`.

## 7.6 Pictures of ANOVA and experimental design

```svgfig label="7.1" caption="Splitting the variation (three teaching methods, five students each). Left: every mark is a dot; the red bars are the group means 86, 78 and 72 and the dashed line is the grand mean 78.67. The dots sit tightly around their own bar but the bars are far apart. Right: the total sum of squares 609.33 divides into $\mathrm{SSB} = 493.33$ (between methods, 81%) and $\mathrm{SSW} = 116.00$ (within, 19%)."
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

```svgfig label="7.2" caption="The F distribution with (2, 12) degrees of freedom. It is skewed right and never negative. The 5% critical value is 3.885; the shaded tail has area 0.05. The teaching-method experiment gave $F = 25.52$, far to the right of the critical value, so $H_{0}$ (equal means) is rejected with $p \approx 0.00005$."
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

```svgfig label="7.4" caption="Partition of the total sum of squares in a two-way design (worked example of Section 7.5): $\mathrm{SST} = 138.25$ splits into varieties 104.00, blocks 32.25 and error 2.00. Taking blocks out of the error shrinks SSE to 2.00, which is why both F ratios (156.0 and 32.25) are so large."
f = Fig(580, 170)
f.box(205, 8, 170, 36, "SST = 138.25  (df 11)", fill=NAVY, color="#ffffff", bold=True, size=12)
for x, t, d, fl, st in [(40, "SSR = 104.00\ndf 2, MS 52.00\nF = 156.0", "varieties", "#bfdbfe", NAVY), (215, "SSC = 32.25\ndf 3, MS 10.75\nF = 32.25", "blocks", "#a7f3d0", TEAL), (390, "SSE = 2.00\ndf 6, MS 0.333", "error", "#fde68a", AMBER)]:
    f.box(x, 86, 150, 54, t, fill=fl, stroke=st, bold=True, size=11)
    f.text(x + 75, 76, d, size=11, color=st, bold=True)
    f.arrow([(290, 44), (290, 56), (x + 75, 56), (x + 75, 64)])
f.text(290, 160, "Critical F(0.05): varieties F(2, 6) = 5.143;  blocks F(3, 6) = 4.757;  both exceeded", size=10.5, color=SLATE, italic=True)
```

## 7.7 Eight uses of ANOVA and designed experiments

1. **Comparing many means with one test.** Three or more groups, such as three teaching methods, can be compared in a single test. Running several *t* tests would inflate the chance of a false alarm well above 5%. ANOVA keeps the overall error at the stated level.
2. **Choosing the best crop variety or fertiliser.** Agricultural stations in Nepal compare paddy or maize varieties on several plots and blocks. ANOVA shows whether the yield differences are real or just soil variation. The blocked design of Figure 7.3 makes the test far more sensitive.
3. **Comparing algorithms and systems.** A developer runs three sorting programs on four data sets and compares the times. The two-way table separates the algorithm effect from the data-set effect. This avoids blaming an algorithm for a hard data set.
4. **$\frac{\frac{A}{B}}{n}$ testing of products.** When a company tests four versions of an $a p p$ screen, one ANOVA tells whether any version differs. Only then is a follow-up test used to find which one. This is cheaper than testing each pair separately.
5. **Quality control across machines or shifts.** A factory compares the output weight of three machines and two shifts. A significant F points to the machine or shift that needs adjusting. Managers can then target the fault instead of retraining everyone.
6. **Medical and psychological trials.** Doses of a drug or kinds of therapy are compared on groups of patients. ANOVA tells whether the treatments differ before doctors study which one is best. Randomisation protects patients from biased allocation.
7. **Education research.** A college compares exam marks across teaching methods, batches or campuses. A significant F supports a change in method; a non-significant one saves money. Section 7.4 works exactly such an example.
8. **Feature and model selection in data science.** The F statistic is used to rank features by how well they separate classes, and to compare the fit of nested regression models. It also underlies the overall F test in regression output. Many software reports show an ANOVA table by default.

```photogrid label="7.1" cols="2" ratio="1.2" caption="Is the difference real or just chance? (a) Ronald Fisher (with W. S. Gosset, who wrote as 'Student'): Fisher worked at the Rothamsted agricultural station, invented analysis of variance and the F test in the 1920s and wrote Statistical Methods for Research Workers (1925). (b) Yields (quintals per hectare) from five plots each of three fertilisers: A 20, 22, 19, 24, 25; B 28, 30, 27, 31, 29; C 23, 25, 22, 26, 24. The group means are 22, 29 and 24 and the grand mean 25. Between groups $S S = 130$ (2 degrees of freedom, mean square 65.0); within groups $S S = 46$ (12 degrees of freedom, mean square $3.83 ) ;\  F = 65.0 / 3.83 = 16.96$. The 5 percent critical value is 3.89 and the p-value is 0.0003, so the fertilisers do not all give the same mean yield. The F value is checked against scipy."
@ photo id="bcamath/fisher" cap="Ronald Fisher with 'Student' (W. S. Gosset)"
fit 1.2
focus 0.5 0.4
@ svg cap="One-way ANOVA of three fertilisers, F = 16.96"
import numpy as np
from scipy import stats
G = {"A": [20, 22, 19, 24, 25], "B": [28, 30, 27, 31, 29], "C": [23, 25, 22, 26, 24]}
allv = sum(G.values(), []); gm = np.mean(allv)
ssb = sum(len(v) * (np.mean(v) - gm) ** 2 for v in G.values()); ssw = sum(((np.array(v) - np.mean(v)) ** 2).sum() for v in G.values())
msb = ssb / 2; msw = ssw / 12; F = msb / msw
res = stats.f_oneway(*G.values())
assert gm == 25 and ssb == 130 and ssw == 46 and abs(F - res.statistic) < 1e-9 and round(F, 2) == 16.96
assert round(res.pvalue, 4) == 0.0003 and round(stats.f.ppf(0.95, 2, 12), 2) == 3.89
f = Fig(300, 240)
Y = lambda v: 128 - (v - 18) / 14 * 100
f.line(30, 128, 280, 128, color=SLATE, sw=1.2); f.line(30, 128, 30, 24, color=SLATE, sw=1.2)
f.line(30, Y(25), 280, Y(25), color=SLATE, sw=1.2, dash=True); f.text(284, Y(25), "25", size=10.5, color=SLATE, anchor="end")
for k, (g, v) in enumerate(G.items()):
    cx = 75 + k * 80
    for j, val in enumerate(sorted(v)):
        f.circle(cx + (j - 2) * 6, Y(val), 4, fill=[BLUE, MINT, SAND][k], stroke=[NAVY, TEAL, AMBER][k], sw=1.4)
    f.line(cx - 28, Y(np.mean(v)), cx + 28, Y(np.mean(v)), color=RED, sw=2.4)
    f.text(cx, 144, f"{g}: mean {np.mean(v):.0f}", size=10.5, color=NAVY, bold=True)
f.text(150, 176, "SSB 130 (df 2, MS 65.0); SSW 46 (df 12, MS 3.83)", size=10.5, color=SLATE)
f.text(150, 198, "F = 65.0 / 3.83 = 16.96 > 3.89 (5% value)", size=10.5, color=RED, bold=True)
f.text(150, 220, "p = 0.0003: means are not all equal", size=10.5, color=NAVY, bold=True)
```

```photogrid label="7.2" cols="2" ratio="1.2" caption="Arranging a fair experiment. (a) Terraced rice fields in Nepal: soil, slope and water change from one strip to the next, so a fair field trial must stop the soil from favouring one variety. (b) A 4 *x* 4 Latin square puts four varieties A, B, C, D on 16 plots so that every variety appears exactly once in each row (soil strip) and once in each column (irrigation channel); the program verifies this for the square drawn, which was made by shuffling the rows and columns of a cyclic square with seed 2081. A Latin square removes two sources of variation, so the ANOVA has df = 3 for varieties, 3 for rows, 3 for columns and 6 for error (15 in total). There are exactly 576 Latin squares of order 4, which the figure counts by exhaustive search, and the actual layout should be chosen at random from them."
@ photo id="bcamath/ricefield" cap="Terraced rice fields in Nepal"
fit 1.2
focus 0.5 0.5
@ svg cap="A 4 x 4 Latin square for four rice varieties"
import itertools, random
base = [[(i + j) % 4 for j in range(4)] for i in range(4)]
rng = random.Random(2081); rows = list(range(4)); cols = list(range(4)); rng.shuffle(rows); rng.shuffle(cols)
L = [[base[r][c] for c in cols] for r in rows]
assert all(sorted(r) == [0, 1, 2, 3] for r in L) and all(sorted(c) == [0, 1, 2, 3] for c in zip(*L))
perms = list(itertools.permutations(range(4))); a1 = (0, 1, 2, 3); k = 0
for a2 in perms:
    if any(x == y for x, y in zip(a1, a2)): continue
    for a3 in perms:
        if any(x == z or y == z for x, y, z in zip(a1, a2, a3)): continue
        for a4 in perms:
            if any(x == w or y == w or z == w for x, y, z, w in zip(a1, a2, a3, a4)): continue
            k += 1
assert 24 * k == 576 and 3 + 3 + 3 + 6 == 15
f = Fig(300, 240)
fl = [BLUE, MINT, SAND, ROSE]; st = [NAVY, TEAL, AMBER, RED]
for i in range(4):
    for j in range(4):
        v = L[i][j]; f.box(20 + j * 38, 26 + i * 38, 36, 36, "ABCD"[v], fill=fl[v], stroke=st[v], size=13, bold=True, r=3)
for j in range(4): f.text(38 + j * 38, 16, f"col {j + 1}", size=10.5, color=SLATE)
f.text(184, 60, "rows = soil strips", size=10.5, color=SLATE, anchor="start")
f.text(184, 80, "columns = water", size=10.5, color=SLATE, anchor="start")
f.text(184, 110, "each of A-D", size=10.5, color=TEAL, bold=True, anchor="start")
f.text(184, 126, "once per row and", size=10.5, color=TEAL, bold=True, anchor="start")
f.text(184, 142, "once per column", size=10.5, color=TEAL, bold=True, anchor="start")
f.text(150, 200, "576 Latin squares of order 4 (counted)", size=10.5, color=NAVY, bold=True)
f.text(150, 220, "df: varieties 3, rows 3, columns 3, error 6", size=10.5, color=SLATE)
```

## 7.7 Latin square design and multiple comparisons

A **Latin square design (LSD)** controls *two* sources of nuisance variation at once. The *t* treatments are arranged in a $t \times t$ square so that every treatment appears **exactly once in each row and exactly once in each column**. Rows and columns are two blocking factors (for example servers and time slots, or soil gradient in two directions). It needs the same number of rows, columns and treatments, so it is practical for $t$ from about 3 to 8. **Randomisation:** choose a standard square, then shuffle the rows, the columns and the treatment labels at random.

**Linear model:** $y_{ijk} = \mu + \rho_i + \gamma_j + \tau_k + e_{ijk}$ (row, column and treatment effects plus error). The sum of squares splits into four parts:

$SS_T = SS_R + SS_C + SS_{Trt} + SS_E$, with degrees of freedom $t^2 - 1 = (t - 1) + (t - 1) + (t - 1) + (t - 1)(t - 2)$.

Computation: $CF = \frac{G^2}{t^2}$; $SS_T = \sum y^2 - CF$; $SS_R = \frac{\sum R_i^2}{t} - CF$; $SS_C = \frac{\sum C_j^2}{t} - CF$; $SS_{Trt} = \frac{\sum T_k^2}{t} - CF$; $SS_E$ by subtraction. The test for treatments is $F = \frac{MS_{Trt}}{MS_E}$ with $(t - 1)$ and $(t - 1)(t - 2)$ d.f.

::: example Worked example: four compression algorithms
Algorithms A, B, C, D are timed (ms) on four servers (rows) in four time slots (columns). Each algorithm runs once on each server and once in each slot.

| | Slot 1 | Slot 2 | Slot 3 | Slot 4 | Row total |
|---|---|---|---|---|---|
| Server 1 | A 39 | B 34 | C 35 | D 40 | 148 |
| Server 2 | B 37 | C 27 | D 38 | A 28 | 130 |
| Server 3 | C 28 | D 31 | A 31 | B 29 | 119 |
| Server 4 | D 36 | A 22 | B 31 | C 21 | 110 |
| Column total | 140 | 114 | 135 | 118 | 507 |

Treatment totals: A = 120, B = 131, C = 111, D = 145 (means 30.00, 32.75, 27.75, 36.25).
$CF = \frac{507^2}{16} = 16065.56$; $SS_T = 491.44$; $SS_R = 200.69$; $SS_C = 120.69$; $SS_{Trt} = 161.19$; $SS_E = 491.44 - 200.69 - 120.69 - 161.19 = 8.88$.

| Source | SS | d.f. | MS | *F* |
|---|---|---|---|---|
| Servers (rows) | 200.69 | 3 | 66.90 | 45.2 |
| Slots (columns) | 120.69 | 3 | 40.23 | 27.2 |
| Algorithms | 161.19 | 3 | 53.73 | **36.3** |
| Error | 8.88 | 6 | 1.479 | |
| Total | 491.44 | 15 | | |

The critical value is $F_{0.05}(3, 6) = 4.76$, so the algorithms differ significantly ($p = 0.0003$); servers and slots matter too, which is why blocking on both was worthwhile.
**What if we had ignored the blocks?** A one-way ANOVA on the same 16 numbers gives $F = 1.95$ with $p = 0.175$, which is **not** significant: the server and slot differences swamp the algorithm differences. The Latin square removed 321.4 of the 491.4 total variation from the error term (error mean square falls from about 22.3 to 1.48).
:::

```svgfig label="7.5" caption="The 4 by 4 Latin square of the worked example. Every algorithm (colour and letter) appears once in every row (server) and once in every column (time slot); the number is the measured time in milliseconds. Row and column totals are shown at the margins."
f = Fig(580, 245)
L = ["ABCD", "BCDA", "CDAB", "DABC"]
Y = [[39, 34, 35, 40], [37, 27, 38, 28], [28, 31, 31, 29], [36, 22, 31, 21]]
fills = {"A": "#bfdbfe", "B": "#fde68a", "C": "#bbf7d0", "D": "#fecaca"}
x0, y0, w, h = 150, 40, 70, 40
for j in range(4):
    f.text(x0 + j * w + w / 2, 30, "Slot %d" % (j + 1), size=11, color=NAVY, bold=True)
for i in range(4):
    f.text(x0 - 10, y0 + i * h + h / 2 + 4, "Server %d" % (i + 1), size=11, color=NAVY, bold=True, anchor="end")
    for j in range(4):
        k = L[i][j]
        f.box(x0 + j * w, y0 + i * h, w, h, fill=fills[k], stroke=NAVY, sw=1.4)
        f.text(x0 + j * w + w / 2, y0 + i * h + h / 2 + 5, "%s  %d" % (k, Y[i][j]), size=13, color=NAVY, bold=True)
for i, t in enumerate([148, 130, 119, 110]):
    f.text(x0 + 4 * w + 12, y0 + i * h + h / 2 + 4, str(t), size=11, color=SLATE, bold=True, anchor="start")
for j, t in enumerate([140, 114, 135, 118]):
    f.text(x0 + j * w + w / 2, y0 + 4 * h + 18, str(t), size=11, color=SLATE, bold=True)
f.text(x0 + 4 * w + 12, 30, "total", size=10.5, color=SLATE, anchor="start")
f.text(x0 - 10, y0 + 4 * h + 18, "total", size=10.5, color=SLATE, anchor="end")
f.text(290, 238, "A = blue, B = amber, C = green, D = red; each letter once per row and once per column", size=10.5, color=SLATE, italic=True)
```

**Comparing the three standard designs.**

| Feature | Completely randomised (CRD) | Randomised block (RBD) | Latin square (LSD) |
|---|---|---|---|
| Nuisance factors controlled | none | one (blocks) | two (rows and columns) |
| Error d.f. | $N - t$ | $(t - 1)(b - 1)$ | $(t - 1)(t - 2)$ |
| Best when | units are uniform | one clear source of variation | two crossed sources |
| Weakness | large error if units differ | block effect must not interact with treatments | needs $t$ rows = $t$ columns = $t$ treatments, few error d.f. for small $t$ |

**Multiple comparisons: the least significant difference (LSD) test.** A significant *F* says only that *some* means differ. The **least significant difference** is $\mathrm{LSD} = t_{\alpha/2,\ \mathrm{d.f.\ of\ error}} \sqrt{\frac{2\,MS_E}{r}}$ for means of $r$ observations each; two treatment means differ significantly if their gap exceeds it. In the example $t_{0.025, 6} = 2.447$ and $\mathrm{LSD} = 2.447\sqrt{\frac{2 \times 1.479}{4}} = $ **2.10 ms**. The gaps: C 27.75, A 30.00 (2.25), B 32.75 (2.75 from A), D 36.25 (3.50 from B); every adjacent gap exceeds 2.10, so all four means are pairwise different and **C is the fastest**. Apply LSD only after a significant *F*, and remember that with many comparisons the chance of at least one false alarm rises; Tukey's HSD or Bonferroni's $\alpha/m$ are the safer choices when there are many treatments.

## Formula and fact sheet

- F = MSB/MSW with $(k - 1 ,\  N - k)$ df; reject if $F > F_{c} \mathrm{ritical}$.
- One-way: SST = SSB + SSW; SSB = Σn_i(ȳ_i − ȳ)².
- Two-way: $C F = \frac{G^{2}}{N} ;\  \mathrm{SSR}$, SSC from totals; $\mathrm{SSE} = \mathrm{SST} - \mathrm{SSR} - \mathrm{SSC}$; error df $(a - 1) (b - 1)$.
- Principles: randomisation, replication, blocking.
- Latin square: $SS_T = SS_R + SS_C + SS_{Trt} + SS_E$; error d.f. $(t - 1)(t - 2)$; $F = \frac{MS_{Trt}}{MS_E}$.
- $\mathrm{LSD} = t_{\alpha/2}\sqrt{\frac{2\,MS_E}{r}}$ (use after a significant *F*).

## Chapter summary

- ANOVA compares several means by splitting total variation into between and within parts and testing their ratio with the F distribution.
- One-way ANOVA handles one factor; two-way ANOVA adds a blocking factor to reduce error.
- A significant F says means differ somewhere; follow-up tests locate the difference.
- A Latin square controls two nuisance factors with error d.f. $(t - 1)(t - 2)$; ignoring the blocks can hide a real treatment effect; the LSD test compares individual means after a significant *F*.

## Practice

1. Why can't we simply run several *t* tests to compare three means?
2. Samples A: 6, 8, 7; B: 9, 11, 10; C: 5, 4, 6. Construct the ANOVA table and test at 5% $(F (2 ,\  6) = 5.143)$.
3. State the assumptions of ANOVA.
4. Explain randomisation, replication and blocking.
5. In a two-way design with 4 rows and 5 columns, give the degrees of freedom of each source.
6. What does a significant F-ratio not tell you?
7. Explain the structure of a Latin square design, state its degrees of freedom for $t = 5$, and give one situation where it is preferable to a randomised block design.
8. For a $3 \times 3$ Latin square the totals are $SS_T = 96$, $SS_R = 12$, $SS_C = 18$, $SS_{Trt} = 60$. Complete the ANOVA table and test the treatments at 5% (critical $F(2, 2) = 19.0$).
9. In the compression example, find the 95% LSD if $MS_E = 1.479$, $r = 4$ and $t_{0.025, 6} = 2.447$, and say whether the means of A (30.00) and B (32.75) differ.

::: note Answers and worked solutions
**1.** Each test has a 5% chance of a false positive, so repeated testing inflates the overall error rate; ANOVA tests all means with one test.

**2.** Means 7, 10, 5; grand mean 7.333. $\mathrm{SSB} = 3 (0.111 + 7.111 + 5.444)$ = **38.0**; $\mathrm{SSW} = (1 + 1 + 0) + (1 + 1 + 0) + (1 + 1 + 0)$ = **6.0**; $\mathrm{SST} = 44$. $\mathrm{MSB} = 19 ,\  \mathrm{MSW} = 1$, **$F = 19.0$** > 5.143 → **reject $H_{0}$**; the means differ.

**3.** Independent observations, normal errors, equal variances across groups.

**4.** Randomisation: assign units to treatments by chance, avoiding bias. Replication: repeat each treatment to estimate error. Blocking: group similar units to remove an unwanted source of variation.

**5.** Rows 3, columns 4, error 12, total 19.

**6.** Which means differ, by how much, or whether the differences matter in practice.

**7.** A $5 \times 5$ square puts each of 5 treatments once in every row and column, so it blocks two factors at once. d.f.: treatments 4, rows 4, columns 4, error $(5 - 1)(5 - 2) = 12$, total 24. It is preferable when there are two crossed sources of variation, such as soil fertility changing both north-south and east-west, or machines and operators in an experiment.

**8.** $SS_E = 96 - 12 - 18 - 60 = 6$ with $(3 - 1)(3 - 2) = 2$ d.f., so $MS_E = 3$. $MS_{Trt} = \frac{60}{2} = 30$ and $F = \frac{30}{3} = $ **10**, which is less than 19.0: **do not reject** the equality of treatments. With only 2 error d.f. the test has little power, which is the weakness of small Latin squares.

**9.** $\mathrm{LSD} = 2.447\sqrt{\frac{2(1.479)}{4}} = 2.447 \times 0.860$ = **2.10**. The gap $32.75 - 30.00 = 2.75 > 2.10$, so **A and B differ significantly**.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). The response times (ms) of three servers, measured four times each, are S1: 14, 16, 15, 17; S2: 19, 21, 20, 22; S3: 12, 13, 15, 12. Construct the one-way ANOVA table and test at the 5% level whether the servers differ. ($F (2 ,\  9) = 4.256$ at 5%.)**

*Introduction.* One-way ANOVA tests $H_{0}$: all group means are equal against $H_{1}$: at least one differs, by comparing variation between groups with variation within them (Figure 7.1).

*Means.* S1 = $\frac{62}{4} = 15.5$; S2 = $\frac{82}{4} = 20.5$; S3 = $\frac{52}{4} = 13.0$. $N = 12$ and the grand mean = 196/12 = 16.333.

*Sums of squares.* SSB = 4[(15.5 − 16.333)² + (20.5 − 16.333)² + (13 − 16.333)²] = 4(0.694 + 17.361 + 11.111) = **116.67**. $\mathrm{SST} = \sum (y - 16.333)^{2}$ = **132.67**. $\mathrm{SSW} = 132.67 - 116.67$ = **16.00**.

| Source | SS | df | MS | F |
|---|---|---|---|---|
| Between servers | 116.67 | 2 | 58.33 | **32.81** |
| Within (error) | 16.00 | 9 | 1.778 |  |
| Total | 132.67 | 11 |  |  |

*Decision.* $F = 58.33 / 1.778 = 32.81$ is greater than $F (2 ,\  9) = 4.256$, and the p-value is about 0.00007, so **reject $H_{0}$**.

*Conclusion.* The servers do not all have the same mean response time. ANOVA does not say which; a follow-up test (Tukey or least significant difference) would show that S2 is slowest and S3 fastest.

**Q2 (5 marks). State the assumptions of ANOVA and explain the three principles of experimental design: randomisation, replication and blocking.**

*Introduction.* The F test is valid only when the data come from a properly designed experiment and meet some conditions.

*Assumptions.*

1. **Independence:** observations are independent of each other.
2. **Normality:** the errors in each group are approximately normal.
3. **Equal variances:** every group has about the same spread (homogeneity).
4. **Additivity:** in the two-way model, row and column effects simply add up (no interaction).

*Three principles (Figure $7.3 ) . \ast$

1. **Randomisation:** treatments are assigned to plots or subjects by chance. It removes selection bias and makes the error terms independent.
2. **Replication:** each treatment is repeated on several units. This allows the error variance to be estimated and gives more precise means.
3. **Blocking (local control):** similar units are grouped into blocks and every treatment appears once in each block. This removes known variation such as soil or batch differences from the error.

*Example.* To compare three paddy varieties on four fields, plant each variety once in every field (blocking), choose positions at random (randomisation), and use all four fields (replication). *Conclusion.* A significant F is trustworthy only when these principles were followed.

**Q3 (10 marks). Explain two-way ANOVA (one observation per cell). The running times (seconds) of three algorithms on four data sets were: A1: 12, 15, 11, 14; A2: 18, 22, 17, 21; A3: 14, 17, 13, 16. Prepare the ANOVA table and test both effects at 5%. ($F (2 ,\  6) = 5.143 ,\  F ( 3$, 6) = 4.757.)**

*Introduction.* **Two-way classification** studies two factors at once: here algorithms (rows, treatments) and data sets (columns, blocks). The model is $y_{i} j = \mu + \alpha_{i} + \beta_{j} + \epsilon_{i} j$. The total variation is split into rows, columns and error, so block-to-block differences are removed from the error and the test of algorithms becomes sharper (Figure 7.4).

*Steps.*

1. Compute the grand total G and correction factor $C F = \frac{G^{2}}{N}$.
2. $\mathrm{SST} = \sum y^{2} - C F ;\  \mathrm{SSR} = \frac{\sum (\mathrm{row} \mathrm{totals})^{2}}{b} - C F ;\  \mathrm{SSC} = \frac{\sum (\mathrm{column} \mathrm{totals})^{2}}{a} - C F$.
3. $\mathrm{SSE} = \mathrm{SST} - \mathrm{SSR} - \mathrm{SSC}$, with df $(a - 1) (b - 1)$.
4. Form the mean squares and the F ratios; compare with the critical values.

*Calculation.* Row totals: A1 = 52, A2 = 78, A3 = 60. Column totals: 44, 54, 41, 51. G = **190**, $N = 12$. $C F = 190^{2} / 12$ = **3008.33**. $\sum y^{2} = 686 + 1538 + 910$ = **3134**.

$\mathrm{SST} = 3134 - 3008.33$ = **125.67**. $\mathrm{SSR} = \frac{(52^{2} + 78^{2} + 60^{2})}{4} - C F = 3097 - 3008.33$ = **88.67**. $\mathrm{SSC} = \frac{(44^{2} + 54^{2} + 41^{2} + 51^{2})}{3} - C F = 3044.67 - 3008.33$ = **36.33**. $\mathrm{SSE} = 125.67 - 88.67 - 36.33$ = **0.67**.

| Source | SS | df | MS | F | $F (0.05)$ | Decision |
|---|---|---|---|---|---|---|
| Algorithms (rows) | 88.67 | 2 | 44.33 | **399.0** | 5.143 | reject $H_{0}$ |
| Data sets (columns) | 36.33 | 3 | 12.11 | **109.0** | 4.757 | reject $H_{0}$ |
| Error | 0.67 | 6 | 0.111 |  |  |  |
| Total | 125.67 | 11 |  |  |  |  |

*One-way versus two-way (Table).*

| Point | One-way | Two-way (no replication) |
|---|---|---|
| Factors | one | two (treatment and block) |
| Error df | $N - k$ | $(a - 1) (b - 1)$ |
| Error size | includes block variation | block variation removed |
| F tests | one | two |
| Example | three teaching methods | three algorithms on four data sets |

*Interpretation.* Both F ratios far exceed their critical values: the algorithms differ in running time, and the data sets differ in difficulty too, so blocking was worthwhile. A2 (mean 19.5 *s*) is slowest and A1 (13.0 *s*) fastest.

*Conclusion.* Two-way ANOVA identified both effects with an error sum of squares of only 0.67. A follow-up multiple-comparison test would confirm which algorithm pairs differ; ANOVA alone says only that the means are not all equal.
