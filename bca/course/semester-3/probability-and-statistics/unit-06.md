---
subject: Probability and Statistics
grade: BCA Semester 3
unit: 6
title: Sample Survey Methods
hours: 10
area: BCA 205 · Probability and Statistics · Unit 6
---

This unit gives the **designs** for choosing a sample and the matching **estimators**, then the sampling distributions $(z ,\  t ,\  \chi^{2})$ used to make confidence statements. Every number below was recomputed by `bca/tools/check_stats.py`.

::: key What this unit gives you
- Simple random sampling with and without replacement; stratified, systematic, cluster, multistage and PPS sampling.
- Ratio and regression estimation; estimating the population total and its variance.
- Sampling distributions: $z ,\  t$ and $\chi^{2}$ with confidence intervals and tests.
:::

## 6.1 Types of sampling

**Probability sampling:** simple random, stratified random, systematic, cluster, multistage, PPS. **Non-probability:** convenience, judgement (purposive), quota, snowball: no valid sampling-error estimate. Notation: population size N, sample size $n ,\  f = \frac{n}{N}$, population mean Ȳ and variance S² = Σ(Yᵢ − Ȳ)²/(N − 1), sample mean ȳ and variance $s^{2}$.

## 6.2 Simple random sampling (SRS)

Every possible sample of size *n* has the same chance. Drawn **without replacement (SRSWOR)** by lottery or random numbers (a unit cannot appear twice) or **with replacement (SRSWR)** (a unit may repeat). Number of possible samples: $C (N ,\  n)$ for SRSWOR, $N^{n}$ for SRSWR.

|  | SRSWOR | SRSWR |
|---|---|---|
| Estimate of mean | ȳ = $\frac{\sum y}{n}$ (unbiased) | ȳ |
| Variance of ȳ | $\frac{(1 - f) S^{2}}{n}$ | $\frac{\sigma^{2}}{n} = \frac{(N - 1) S^{2}}{N n}$ |
| Estimated | $\frac{(1 - f) s^{2}}{n}$ | $\frac{s^{2}}{n}$ |
| Estimate of total Y | Ŷ = Nȳ | Nȳ |
| Variance of total | $\frac{N^{2} (1 - f) s^{2}}{n}$ | $\frac{N^{2} s^{2}}{n}$ |

$(1 - f)$ is the **finite population correction**; sampling without replacement is more precise.

::: example Worked example
A population of $N = 200$ students; an SRSWOR of $n = 20$ gives ȳ = 52 marks and $s = 8$. $f = 0.1$. Estimated Var(ȳ) = $(1 - 0.1) \times \frac{64}{20}$ = **2.88**, SE = **1.697**. 95% confidence interval for the mean: $52 \pm 1.96 \times 1.697$ = **(48.67, 55.33)**. Estimated total marks Ŷ = $200 \times 52$ = **10,400**, SE(Ŷ) = $200 \times 1.697$ = **339.41**. With replacement the variance would be $\frac{64}{20} = 3.2$, larger than 2.88.
:::

## 6.3 Stratified random sampling

Divide the population into non-overlapping, **homogeneous strata** (by district, class, income band), then draw an SRS in each. Estimate: **ȳ_st = Σ W_h ȳ_h**, $W_{h} = \frac{N_{h}}{N}$. **Var(ȳ_st) = Σ W_h² (1 − f_h) s_h²/n_h.** It is more precise than SRS when strata are internally similar and differ from one another, guarantees representation of subgroups, and allows separate estimates per stratum.

**Allocation of *n*:** **proportional** $n_{h} = \frac{n N_{h}}{N}$; **equal**; **optimum/Neyman** $n_{h} \propto N_{h} S_{h}$ (larger or more variable strata get more; with different costs ∝ $\frac{N_{h} S_{h}}{\sqrt{c_{h}}}$).

::: example Worked example
Two strata: N₁ = 300 (ȳ₁ = 60, s₁ = 10), N₂ = 700 (ȳ₂ = 50, s₂ = 8); total $n = 100$, proportional allocation: $n_{1} = 30 ,\  n_{2} = 70 ,\  W = 0.3$ and 0.7. ȳ_st = 0.3 × 60 + 0.7 × 50 = **53**. $f_{1} = f_{2} = 0.1$. Var = $0.3^{2} \times 0.9$ × 100/30 + $0.7^{2} \times 0.9 \times \frac{64}{70} = 0.27 + 0.4032$ = **0.6732**, SE = **0.8205**. An SRS of the same 100 would have variance about **0.8622**, so stratification cut the variance by **22%**. **Neyman allocation:** $n_{1} \propto 300 \times 10 = 3000 ,\  n_{2} \propto 700 \times 8 = 5600 \to n_{1} = 100$ × 3000/8600 = **$34.9 \approx 35$**, $n_{2}$ = **$65.1 \approx 65$**.
:::

## 6.4 Systematic sampling

Select every **k-th** unit after a random start: $k = \frac{N}{n}$ (the sampling interval); choose a random start *r* from $1 \ldots k$; the sample is $r ,\  r + k ,\  r + 2 k ,\  \ldots$. Simple, spreads the sample evenly over an ordered list, no need for a full renumbering. **Danger:** if the list has a **periodic pattern** matching *k* (every 7th day of sales data) the sample is biased. Equivalent to SRS if the list is in random order.

::: example Worked example
N = 1,000, $n = 50$: $k = 20$. Random start 7 → units **7, 27, 47, 67, 87, …, 987**. If N is not a multiple of *n*, use the nearest integer *k* or a circular list.
:::

## 6.5 Cluster and multistage sampling

**Cluster sampling:** divide the population into **clusters** (villages, schools, wards), randomly select some clusters, and survey **all** units in them. Cheap and practical when no unit list exists and units are scattered. Clusters are internally *heterogeneous* ideally; the higher the similarity within clusters (intra-cluster correlation) the less precise it is than SRS of the same size. **Multistage sampling** samples in stages: districts → wards → households → persons; each stage uses SRS, systematic or PPS sampling. It needs a list only for chosen units at each stage, and is the standard design for national surveys such as the Nepal Living Standards Survey and Demographic and Health Survey.

## 6.6 Probability proportional to size (PPS) sampling

When clusters differ in size, selecting each with probability **proportional to its size** removes the bias of giving small villages the same chance as big ones. With $p_{i} = \frac{M_{i}}{\sum M}$, the unbiased **Hansen–Hurwitz estimator** for the total with *n* draws is **Ŷ = $\frac{\left( \frac{1}{n} \right) \sum y_{i}}{p_{i}}$**, and its variance is estimated from the spread of the $\frac{y_{i}}{p_{i}}$ values.

::: example Worked example
Three villages have 100, 300 and 600 households (total 1,000), so $p = 0.1 ,\  0.3 ,\  0.6$. Two draws select village 2 ($y = 900$ persons) and village 3 (*y* = 1,500). Ŷ = $\frac{1}{2} ( 900 / 0.3$ + 1,500/0.6) = $\frac{1}{2} ( 3 ,\  000$ + 2,500) = **2,750** persons.
:::

## 6.7 Ratio and regression methods of estimation

If an **auxiliary variable *x*** correlated with *y* is known for the whole population (total X, mean $\bar{X}$), it improves precision. **Ratio estimator:** R̂ = ȳ/x̄; **ȳ_R = R̂ $\bar{X}$**, **Ŷ_R = R̂ X**. It is better than ȳ when *y* is roughly proportional to *x* (the line through the origin). **Regression estimator:** ȳ_lr = ȳ + $b (\bar{X} - \bar{x})$, with *b* the sample regression coefficient of *y* on *x*; best when *y* is linearly related to *x* (with any intercept), and never worse than the ratio estimator in large samples. Both are slightly biased but precise.

::: example Worked example
$N = 100$ farms with total area X = 5,000 $h a (\bar{X} = 50)$. A sample of $n = 10$ gives mean production ȳ = 30 and mean area $\bar{x} = 48$. R̂ = $\frac{30}{48} = 0.625$. Estimated mean production = $0.625 \times 50$ = **31.25**; total = 0.625 × 5,000 = **3,125**. The raw ȳ = 30 would underestimate because the sample happened to have below-average farms $(48 < 50)$; the ratio estimator corrects this.
:::

Ratio and regression methods also apply **within strata** (separate or combined estimators). **Estimating the population total and its variance:** Ŷ = Nȳ under SRS; Ŷ_st = Σ N_h ȳ_h under stratification with Var(Ŷ_st) = Σ N_h²(1 − f_h)s_h²/n_h.

## 6.8 Sampling distributions: z, t and χ²

The **sampling distribution** of a statistic is its distribution over all possible samples. The **central limit theorem**: for large *n* the distribution of $\bar{x}$ is approximately normal with mean *μ* and **standard error $\frac{\sigma}{\sqrt{n}}$**, whatever the population shape.

| Distribution | When used | Statistic |
|---|---|---|
| ***z* (standard normal)** | mean, *σ* known or *n* large $(\geq 30)$; proportions | $z = \frac{\bar{x} - \mu}{\frac{\sigma}{\sqrt{n}}}$ |
| **Student's *t*** | mean, *σ* unknown, small *n*; df = $n - 1$ | $t = \frac{\bar{x} - \mu}{\frac{s}{\sqrt{n}}}$ |
| **$\chi^{2}$ (chi-square)** | tests of independence/goodness of fit; variance | $\chi^{2} = \frac{\sum (O - E)^{2}}{E}$; df depends on the test |

The *t* distribution is bell-shaped but heavier-tailed than *z* and approaches *z* as df grows. **Critical values (5% level):** $z = 1.645$ (one-tail), 1.96 (two-tail), 2.576 (1% two-tail); *t* two-tail 0.05: df $9 \to 2.262 ,\  14 \to 2.145 ,\  15 \to 2.131 ,\  19 \to 2.093 ;\  \chi^{2}$ at 5%: df $1 \to 3.841 ,\  2 \to 5.991 ,\  3 \to 7.815 ,\  5 \to 11.070$.

::: example Worked example: confidence interval with t
A sample of $n = 16$ response times has mean 52.5 ms and $s = 6$. $S E = \frac{6}{\sqrt{16}} = 1.5$; df = 15, t₀.₀₂₅ = 2.1314. 95% $C I = 52.5 \pm 2.1314 \times 1.5$ = **(49.30, 55.70)** ms. Using *z* would give the narrower (49.56, 55.44), falsely overconfident for $n = 16$.
:::

::: example Worked example: z test
A system claims a mean load time of 50 $s (\sigma = 10)$. A sample of $n = 36$ gives $\bar{x} = 53$. $z = \frac{53 - 50}{\frac{10}{\sqrt{36}}} = 3 / 1.667$ = **1.8**. Two-tailed p-value = **0.0719** > 0.05, so we do **not** reject the claim at 5% $(|z| < 1.96)$.
:::

::: example Worked example: χ² test of independence
Preference for a language by gender: 30 men and 20 women choose Java, and 20 men and 30 women choose Python, observed $\begin{bmatrix} 30 & 20 \\ 20 & 30 \end{bmatrix}$. Totals are 50 per row and column, so each expected count is 25. $\chi^{2} = \frac{\sum (O - E)^{2}}{E} = 4 \times \frac{25}{25}$ = **4.0**, df = $(2 - 1) (2 - 1) = 1$; critical value $3.841 ;\  p = 0.0455$ → **reject independence at 5%**: preference appears related to gender in this sample.

Goodness of fit: a die rolled 60 times gives counts 8, 12, 9, 11, 10, 10; expected 10 each; $\chi^{2} = \frac{4 + 4 + 1 + 1 + 0 + 0}{10}$ = **1.0** < 11.07 (df 5): consistent with a fair die.
:::

## 6.9 Pictures of sampling designs and sampling distributions

```svgfig label="6.1" caption="Four ways to draw 20 units from a population of 100 shown as a $10 \times 10$ grid (red = selected). (a) Simple random: any 20 positions, no pattern. (b) Stratified: the grid is split into three strata (rows 1-3, 4-7, 8-10) and a random share is drawn from each, here in proportion 6, 8, 6. (c) Systematic: every 5th unit after a random start of 3. (d) Cluster: four whole columns (clusters) are chosen and every unit in them is surveyed."
f = Fig(580, 225)
srs = {(1, 2), (4, 0), (7, 1), (2, 5), (9, 4), (5, 3), (0, 8), (3, 9), (6, 7), (8, 6), (1, 6), (4, 4), (7, 9), (9, 0), (2, 1), (5, 8), (8, 3), (0, 4), (6, 2), (3, 6)}
strat = {(r, c) for r, c in [(0, 1), (0, 6), (1, 3), (1, 8), (2, 0), (2, 5), (3, 2), (3, 7), (4, 4), (4, 9), (5, 1), (5, 6), (6, 3), (6, 8), (7, 5), (8, 0), (8, 4), (8, 7), (9, 2), (9, 9)]}
syst = {((i - 1) // 10, (i - 1) % 10) for i in range(3, 101, 5)}
clus = {(r, c) for c in (1, 4, 6, 8) for r in range(10)}
cs = 12.5
for k, (t, sel, strata) in enumerate([("(a) simple random", srs, False), ("(b) stratified", strat, True), ("(c) systematic", syst, False), ("(d) cluster", clus, False)]):
    x0 = 14 + k * 144
    for r in range(10):
        for c in range(10):
            on = (r, c) in sel
            f.circle(x0 + c * cs + 6, 30 + r * cs + 6, 4.4 if on else 3.2, fill=RED if on else "#cbd5e1", stroke=RED if on else "#cbd5e1", sw=0.8)
    if strata:
        f.line(x0, 30 + 3 * cs, x0 + 10 * cs, 30 + 3 * cs, color=NAVY, sw=1.6, dash=True); f.line(x0, 30 + 7 * cs, x0 + 10 * cs, 30 + 7 * cs, color=NAVY, sw=1.6, dash=True)
    f.text(x0 + 63, 16, t, size=11, color=NAVY, bold=True)
f.text(290, 196, "Stratified and cluster designs use the structure of the population; simple random and systematic ignore it.", size=10.5, color=SLATE, italic=True)
f.text(290, 212, "Stratify when groups are internally alike; cluster when groups are internally mixed and travel is costly.", size=10.5, color=SLATE, italic=True)
```

```photogrid label="6.1" cols="3" ratio="1.0" caption="Student's *t*. (a) William Sealy Gosset (1876-1937), brewer and statistician, working at the Guinness brewery in Dublin where he needed to judge barley and beer from very small samples. (b) The plaque in the Guinness Storehouse recognises the 't test' he published in 1908 under the pen name Student. (c) With few degrees of freedom the *t* curve has heavier tails than the normal curve, so its critical values are larger."
@ photo id="bca205/gosset" cap="W. S. Gosset, 1908"
fit 1.0
focus 0.5 0.3
@ photo id="bca205/guinness" cap="Gosset plaque, Guinness Storehouse, Dublin"
fit 1.0
focus 0.5 0.4
@ svg cap="t (df = 3, red) versus normal (blue)"
import math
f = Fig(300, 300)
ax = Axes(f, 14, 40, 272, 190, (-4, 4), (0, 0.45))
N = lambda z: math.exp(-z * z / 2) / math.sqrt(2 * math.pi)
T = lambda x, v=3: math.gamma((v + 1) / 2) / (math.sqrt(v * math.pi) * math.gamma(v / 2)) * (1 + x * x / v) ** (-(v + 1) / 2)
ax.curve(N, -4, 4, color=NAVY, sw=2.4); ax.curve(T, -4, 4, color=RED, sw=2.4)
f.line(ax.X(-4), ax.Y(0), ax.X(4), ax.Y(0), color=SLATE, sw=1.2)
for z in (-2, 0, 2): f.text(ax.X(z), ax.Y(0) + 15, str(z), size=12.5, color=SLATE)
f.text(150, 22, "t has fatter tails", size=13, color=RED, bold=True)
f.text(150, 262, "two-tail 5%: z = 1.96, t₃ = 3.18", size=12.5, color=SLATE, bold=True)
```

```svgfig label="6.2" caption="The central limit theorem in pictures. If individual values have spread $\sigma ( n = 1$, wide curve), the mean of *n* values has spread $\frac{\sigma}{\sqrt{n}}$: it is already much narrower for $n = 4$ and very narrow for $n = 25$. Sampling distributions of the mean are approximately normal for large *n* whatever the shape of the population, and larger samples give more precise estimates."
import math
f = Fig(580, 200)
ax = Axes(f, 60, 18, 460, 140, (-3, 3), (0, 2.2))
for s, c, t in [(1.0, SLATE, "n = 1, SE = σ"), (0.5, TEAL, "n = 4, SE = σ/2"), (0.2, RED, "n = 25, SE = σ/5")]:
    ax.curve(lambda x, s=s: math.exp(-x * x / (2 * s * s)) / (s * math.sqrt(2 * math.pi)), -3, 3, color=c, sw=2.4)
f.line(ax.X(-3), ax.Y(0), ax.X(3), ax.Y(0), color=SLATE, sw=1.2)
f.text(ax.X(0), ax.Y(0) + 14, "μ", size=11.5, color=SLATE, bold=True)
for x, y, t, c in [(ax.X(1.45), ax.Y(0.2), "n = 1, SE = σ", SLATE), (ax.X(1.1), ax.Y(0.6), "n = 4, SE = σ/2", TEAL), (ax.X(0.6), ax.Y(1.7), "n = 25, SE = σ/5", RED)]:
    f.text(x, y, t, size=11, color=c, bold=True, anchor="start")
f.text(290, 192, "Precision grows with √n: to halve the standard error you need four times the sample.", size=10.5, color=SLATE, italic=True)
```

```svgfig label="6.3" caption="The chi-square test as a picture. For 3 degrees of freedom the curve is skewed right; the 5% critical value is 7.815. If the computed $\chi^{2} = \frac{\sum (O - E)^{2}}{E}$ falls in the shaded tail the observed counts are too far from the expected ones and the hypothesis is rejected. The goodness-of-fit value 1.0 (die, 5 df, critical 11.07) is nowhere near its tail."
import math
f = Fig(580, 200)
C = lambda x, k=3: x ** (k / 2 - 1) * math.exp(-x / 2) / (2 ** (k / 2) * math.gamma(k / 2))
ax = Axes(f, 60, 18, 460, 140, (0, 14), (0, 0.3))
ax.grid(2, 0.1, labels=False); ax.axes("χ²", "")
ax.area(C, 7.815, 14, fill="#fbbf24", opacity=0.85)
ax.curve(C, 0.05, 14, color=NAVY, sw=2.6)
for v in range(0, 15, 2): f.text(ax.X(v), ax.Y(0) + 14, str(v), size=10.5, color=SLATE)
ax.vline(7.815, 0, 0.17, color=RED, dash=False, sw=1.8)
f.text(ax.X(7.815) + 5, ax.Y(0.17) + 4, "critical 7.815", size=11, color=RED, bold=True, anchor="start")
f.text(ax.X(11.2), ax.Y(0.05), "reject H₀ (area 5%)", size=11, color=AMBER, bold=True)
f.text(ax.X(2.5), ax.Y(0.25), "do not reject", size=11, color=TEAL, bold=True)
f.text(290, 192, "Fixed rule: χ² > critical value means reject; otherwise the data are consistent with the hypothesis.", size=10.5, color=SLATE, italic=True)
```

## 6.10 Eight sampling designs and tools, and what each is used for

1. **Simple random sampling.** Every unit has the same chance, like drawing lots, so the estimate is unbiased and easy to analyse. It suits a small, well-listed population such as 200 students of one batch. It is the baseline against which other designs are compared.
2. **Stratified sampling.** The population is split into alike groups (strata) such as Terai, hill and mountain, and each is sampled separately. This guarantees that every group is represented and often gives a smaller variance than simple random sampling. A national household survey in Nepal is naturally stratified by ecological region.
3. **Systematic sampling.** Pick a random start and then every k-th unit, such as every 20th voter on a list. It is quick, spreads the sample evenly and needs no random-number table. It fails if the list repeats with the same period as *k*, for example a weekly pattern with $k = 7$.
4. **Cluster and multistage sampling.** Whole villages, wards or schools are chosen at random and then units inside them are surveyed. It cuts travel cost enormously when no list of individuals exists. The price is a larger error, because people in one ward resemble each other.
5. **PPS sampling.** Big clusters are given a bigger chance of selection, in proportion to size. A village with 600 households is then six times more likely to be drawn than one with 100. The estimator divides each total by its selection probability to stay unbiased.
6. **Ratio and regression estimation.** When an easy-to-know variable such as farm area is correlated with the target, say production, it sharpens the estimate. The ratio estimator uses the known population total of the helper variable. It gave 31.25 instead of 30 in the worked example of Section 6.7.
7. **The *z* and *t* distributions.** They give confidence intervals and tests for a mean. Use *z* when *σ* is known or *n* is large, and *t* when *σ* is unknown and *n* is small, as Gosset showed. A software tester comparing the load times of 12 pages uses *t*.
8. **The chi-square test.** It compares observed counts with expected counts. A college can test whether language preference differs by gender, or whether a die or random-number generator is fair. The decision rule is the shaded tail of Figure 6.3.

## Formula and fact sheet

- SRSWOR: Var(ȳ) = $\frac{(1 - f) s^{2}}{n}$; total Ŷ = Nȳ, Var = $\frac{N^{2} (1 - f) s^{2}}{n}$. SRSWR: $\frac{s^{2}}{n}$.
- Stratified: ȳ_st = ΣW_hȳ_h; Var = $\frac{\sum W_{h}^{2} (1 - f_{h}) s_{h}^{2}}{n_{h}}$; Neyman $n_{h} \propto N_{h} S_{h}$.
- Systematic: $k = \frac{N}{n}$, random start. PPS: Ŷ = $\frac{\left( \frac{1}{n} \right) \sum y_{i}}{p_{i}}$. Ratio: ȳ_R = (ȳ/x̄)X̄.
- SE of mean $\frac{\sigma}{\sqrt{n}} ;\  z = 1.96$ (95%); *t* with df $n - 1 ;\  \chi^{2} = \frac{\sum (O - E)^{2}}{E}$, df = $(r - 1) (c - 1)$.

## Chapter summary

- SRS is the baseline; stratification gains precision from homogeneous strata; systematic sampling is simple but pattern-sensitive; cluster and multistage designs cut cost; PPS handles unequal clusters.
- Ratio and regression estimators exploit an auxiliary variable.
- The CLT justifies $z ;\  t$ replaces *z* for small *n* with unknown $\sigma ;\  \chi^{2}$ tests counts.

## Practice

1. $N = 500$, an SRSWOR of 50 gives ȳ = 40 and $s = 6$. Find the estimated variance of ȳ, the 95% CI, and the estimated total with its SE.
2. Two strata of sizes 400 and 600 have $s = 5$ and 10. Find the Neyman allocation for $n = 100$.
3. Select a systematic sample of 8 from $N = 80$ with random start 5.
4. Differentiate stratified and cluster sampling.
5. A sample ȳ = 25 with $\bar{x} = 20$, population mean $\bar{X} = 22$. Find the ratio estimate.
6. $n = 25 ,\  \bar{x} = 100 ,\  s = 15$: 95% CI (t₀.₀₂₅ with 24 df = 2.064).
7. Test independence for $\begin{bmatrix} 40 & 10 \\ 20 & 30 \end{bmatrix}$ at 5%.
8. When is *t* used instead of *z*?

::: note Answers and worked solutions
**1.** $f = 0.1$; Var = $0.9 \times \frac{36}{50}$ = **0.648**, $S E = 0.805 ;\  C I 40 \pm 1.96 \times 0.805$ = **(38.42, 41.58)**; total $500 \times 40$ = **20,000**, $S E = 500 \times 0.805$ = **402.5**.

**2.** $N_{1} S_{1}$ = 2,000; $N_{2} S_{2}$ = 6,000: $n_{1} = 100$ × 2,000/8,000 = **25**, $n_{2}$ = **75**.

**3.** $k = 10$; units **5, 15, 25, 35, 45, 55, 65, 75**.

**4.** Stratified: sample *within every* homogeneous stratum, improves precision. Cluster: sample *whole* clusters, reduces cost, usually less precise.

**5.** R̂ = $\frac{25}{20} = 1.25$; estimate = $1.25 \times 22$ = **27.5**.

**6.** $S E = \frac{15}{5} = 3 ;\  C I = 100 \pm 2.064 \times 3$ = **(93.81, 106.19)**.

**7.** Row totals 50, 50; column totals 60, 40; expected: $30 ,\  \frac{20}{30} ,\  20$. $\chi^{2} = (10^{2} / 30 + 10^{2} / 20) \times 2 = (3.333 + 5) \times 2$ = **16.67** > 3.841 → **reject independence**.

**8.** When *σ* is unknown and the sample is small $(n < 30)$, the data being roughly normal.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). A population has $N = 800$ students. A simple random sample without replacement of $n = 40$ gives mean marks ȳ = 65 and $s = 10$. Estimate the variance and standard error of the mean, a 95% confidence interval, and the population total with its standard error.**

*Introduction.* Under SRSWOR the sample mean is an unbiased estimate of the population mean and its variance includes the finite population correction $(1 - f)$, where $f = \frac{n}{N}$.

*Sampling fraction.* *f* = 40/800 = 0.05, so $1 - f = 0.95$.

*Variance and SE.* Est. Var(ȳ) = $\frac{(1 - f) s^{2}}{n} = 0.95$ × 100/40 = **2.375**, so SE(ȳ) = $\sqrt{2.375}$ = **1.541**.

*Confidence interval.* ȳ ± 1.96 $S E = 65 \pm 1.96 \times 1.541 = 65 \pm 3.02$, that is **(61.98, 68.02)**.

*Total.* Ŷ = Nȳ = $800 \times 65$ = **52,000**. SE(Ŷ) = N × SE(ȳ) = $800 \times 1.541$ = **1,232.9**.

*Interpretation and conclusion.* We are 95% confident the true mean mark lies between about 62 and 68. Without the correction the SE would be 1.581, a little too large, so ignoring $(1 - f)$ overstates the uncertainty. The estimates are valid only if the 40 students were truly chosen at random from a complete list (Figure 6.1a).

**Q2 (5 marks). A population has two strata: $N_{1} = 600$ with $s_{1} = 4$ and $N_{2} = 400$ with $s_{2} = 12$. Allocate a sample of $n = 50$ by (a) proportional and (b) Neyman allocation, and compare the variances.**

*Introduction.* Stratified sampling draws a separate random sample from each stratum. The allocation decides how many units come from each.

$\ast (a)$ Proportional allocation* $n_{h} = \frac{n N_{h}}{N}$. $n_{1} = 50$ × 600/1000 = **30** and $n_{2} = 50$ × 400/1000 = **20**.

$\ast (b)$ Neyman (optimum) allocation* $n_{h} \propto N_{h} S_{h}$. $N_{1} S_{1}$ = 2,400 and $N_{2} S_{2}$ = 4,800, total 7,200. $n_{1} = 50$ × 2400/7200 = 16.7 ≈ **17**; $n_{2} = 50$ × 4800/7200 = 33.3 ≈ **33**.

*Variance of the stratified mean* Var = $\frac{\sum W_{h}^{2} (1 - f_{h}) s_{h}^{2}}{n_{h}}$ with $W_{1} = 0.6$ and $W_{2} = 0.4$.

| Allocation | $n_{1} ,\  n_{2}$ | Var(ȳ_st) | SE |
|---|---|---|---|
| Proportional | 30, 20 | 1.2768 | 1.130 |
| Neyman | 17, 33 | 0.9698 | 0.985 |

*Conclusion.* Neyman allocation gives a **24% smaller variance** because it samples more heavily from the highly variable stratum 2. It is the best design when the strata differ strongly in variability; proportional allocation is simpler and nearly as good when they do not.

**Q3 (10 marks). Explain the $z ,\  t$ and chi-square distributions with their uses. A sample of 9 response times has mean 52 ms and $s = 6$ ms. Test $H_{0}$: $\mu = 48$ ms against $H_{1}$: $\mu \neq 48$ ms at the 5% level and give a 95% confidence interval. Compare with a z-test.**

*Introduction.* The **sampling distribution** of a statistic is its distribution over all possible samples. By the **central limit theorem** the sample mean is approximately normal with standard error $\frac{\sigma}{\sqrt{n}}$ for large *n* (Figure 6.2). Three families are used for inference.

*The three distributions (Table).*

| Distribution | Use | Statistic | Shape |
|---|---|---|---|
| *z* (standard normal) | mean with known *σ* or $n \geq 30$; proportions | $z = \frac{\bar{x} - \mu}{\frac{\sigma}{\sqrt{n}}}$ | symmetric bell |
| Student's *t* | mean, *σ* unknown, small *n*; df = $n - 1$ | $t = \frac{\bar{x} - \mu}{\frac{s}{\sqrt{n}}}$ | symmetric, heavier tails |
| $\chi^{2}$ | goodness of fit, independence, variance | $\chi^{2} = \frac{\sum (O - E)^{2}}{E}$ | skewed right, df-dependent |

*Key points.* The *t* curve approaches the normal as df grows (Plate $6.1 ) ;\  \chi^{2}$ is never negative and its decision tail is on the right (Figure 6.3).

*Hypothesis test (t-test).*

1. **Hypotheses:** $H_{0}$: $\mu = 48 ;\  H_{1}$: $\mu \neq 48$ (two-tailed).
2. **Statistic:** $S E = \frac{6}{\sqrt{9}} = 2$. $t = \frac{52 - 48}{2}$ = **2.0**, with df = 8.
3. **Critical value:** t₀.₀₂₅ with 8 df = **2.306**.
4. **Decision:** $|2.0| < 2.306$, so we **do not reject $H_{0}$**. The two-tailed p-value is 0.0805, greater than 0.05.

*Confidence interval.* $52 \pm 2.306 \times 2 = 52 \pm 4.61$, that is **(47.39, 56.61)**. The value 48 lies inside, which agrees with the test.

*Comparison with $z . \ast$ If *σ* were wrongly taken as 6 (known), $z = 2.0$ and the critical value is 1.96, so the same data would **reject** $H_{0} (p = 0.0455)$. The z-test is too eager with only 9 observations because it ignores the extra uncertainty of estimating *σ*; that is exactly why Gosset invented the *t* distribution.

*Conclusion.* With a small sample and unknown *σ*, use *t*. Here the evidence (52 ms against 48 ms) is suggestive but not statistically significant at the 5% level; a larger sample would be needed to settle it.
