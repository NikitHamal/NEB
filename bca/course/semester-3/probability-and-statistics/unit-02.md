---
subject: Probability and Statistics
grade: BCA Semester 3
unit: 2
title: Descriptive Statistics
hours: 6
area: BCA 205 · Probability and Statistics · Unit 2
---

Descriptive statistics condenses a mass of numbers into a few summary values. We need two kinds: a **central value** that says where the data sit, and a **measure of dispersion** that says how widely they spread. All values here were recomputed by `bca/tools/check_stats.py`.

::: key What this unit gives you
- Mean, median, partition values (quartiles, deciles, percentiles) and mode, for raw and grouped data.
- Range, quartile deviation, mean deviation, standard deviation, variance, coefficient of variation.
- Interpretation and choice of measure.
:::

## 2.1 Measures of central tendency

**Arithmetic mean:** x̄ = Σx / n. For a frequency table, x̄ = Σfx / Σf (with x the class midpoint). Properties: uses all values; the sum of deviations from the mean is zero (Σ(x − x̄) = 0); the sum of squared deviations is least about the mean; **sensitive to outliers**.

**Median:** the middle value of the ordered data; for n values it is the ((n + 1)/2)th item (average the two middle ones if n is even). Not affected by extreme values. For grouped data: **Median = L + ((n/2 − cf)/f) × h**, where L is the lower limit of the median class (the class containing the n/2th item), cf the cumulative frequency before it, f its frequency and h the class width.

**Mode:** the most frequent value. For grouped data: **Mode = L + (d₁/(d₁ + d₂)) × h**, with L the lower limit of the modal class, d₁ = f − f_previous, d₂ = f − f_next. A distribution may be unimodal, bimodal or have no mode. Empirical relation for moderately skewed data: mean − mode ≈ 3(mean − median).

**Partition values** divide the ordered data: **quartiles** Q₁, Q₂ (= median), Q₃ into 4 parts; **deciles** D₁…D₉ into 10; **percentiles** P₁…P₉₉ into 100. Position of Qᵢ = i(n + 1)/4 for raw data; for grouped data Qᵢ = L + ((i·n/4 − cf)/f) × h.

::: example Worked example: raw data
Marks of 10 students: 45, 52, 58, 61, 61, 67, 70, 74, 80, 92.
**Mean** = 660/10 = **66**. **Median:** n = 10, the 5th and 6th values are 61 and 67, so median = **64**. **Mode** = **61**. **Q₁:** position (n + 1)/4 = 2.75, between 52 and 58: 52 + 0.75 × 6 = **56.5**. **Q₃:** position 8.25, between 74 and 80: 74 + 0.25 × 6 = **75.5**.
:::

::: example Worked example: grouped data
| Class | 10–20 | 20–30 | 30–40 | 40–50 | 50–60 |
|---|---|---|---|---|---|
| Frequency f | 5 | 8 | 15 | 16 | 6 |
| Midpoint x | 15 | 25 | 35 | 45 | 55 |
| Cumulative f | 5 | 13 | 28 | 44 | 50 |

n = 50. **Mean** = Σfx/n = (75 + 200 + 525 + 720 + 330)/50 = 1850/50 = **37**.
**Median:** n/2 = 25 lies in the class 30–40 (cumulative 28): L = 30, cf = 13, f = 15, h = 10 → 30 + (25 − 13)/15 × 10 = **38**.
**Mode:** modal class 40–50 (f = 16): d₁ = 16 − 15 = 1, d₂ = 16 − 6 = 10 → 40 + 1/11 × 10 = **40.91**.
**Q₁:** n/4 = 12.5 in 20–30: 20 + (12.5 − 5)/8 × 10 = **29.375**. **Q₃:** 3n/4 = 37.5 in 40–50: 40 + (37.5 − 28)/16 × 10 = **45.94**.
:::

**Which average?** Mean for symmetric quantitative data and further calculation; median for skewed data or with outliers (incomes, house prices); mode for the most typical or for nominal data (the most common shoe size). For **positively skewed** data mean > median > mode; negatively skewed the reverse; symmetric, all equal.

## 2.2 Measures of dispersion

| Measure | Formula | Notes |
|---|---|---|
| **Range** | max − min | crude; depends on extremes. Coefficient = (max − min)/(max + min) |
| **Quartile deviation** | QD = (Q₃ − Q₁)/2 | uses the middle 50%; coefficient = (Q₃ − Q₁)/(Q₃ + Q₁) |
| **Mean deviation** | MD = Σ|x − x̄|/n (about the mean or median) | coefficient = MD/average |
| **Variance** | σ² = Σ(x − x̄)²/n (population); s² = Σ(x − x̄)²/(n − 1) (sample) | squared units |
| **Standard deviation** | σ = √σ² | same units as data; most used |
| **Coefficient of variation** | CV = (σ / x̄) × 100% | unitless; compares variability of different data sets |

Computational form: σ² = Σx²/n − x̄². Grouped: σ² = Σf(x − x̄)²/Σf. The sample version divides by n − 1 to give an **unbiased** estimate of the population variance.

::: example Worked example: dispersion of the 10 marks (x̄ = 66)
Range = 92 − 45 = **47**. QD = (75.5 − 56.5)/2 = **9.5** (coefficient 19/132 = 0.144). Absolute deviations from 66: 21, 14, 8, 5, 5, 1, 4, 8, 14, 26 sum to 106, so **MD = 10.6**. Squared deviations total **1704**: population variance = 170.4, **σ = 13.05**; sample variance = 1704/9 = 189.33, **s = 13.76**. **CV** = 13.05/66 × 100 = **19.78%**.
For the grouped data above (x̄ = 37): variance = Σf(x − 37)²/50 = **132**, σ = **11.49**, CV = **31.05%**. The grouped marks are relatively more variable (31%) than the 10 marks (20%), even though their means differ, which is what CV is for.
:::

**Standard deviation intuition:** for bell-shaped data about 68% of values lie within ±1σ of the mean, 95% within ±2σ, 99.7% within ±3σ (Unit 4). **Effect of change of origin and scale:** adding a constant to every value changes the mean but not σ; multiplying by c multiplies both the mean and σ by |c|.

**Skewness** (asymmetry) can be measured by Pearson's coefficient Sk = (mean − mode)/σ, or 3(mean − median)/σ; **kurtosis** describes peakedness.

## Formula and fact sheet

- x̄ = Σx/n; grouped Σfx/n. Median = L + ((n/2 − cf)/f)h. Mode = L + (d₁/(d₁ + d₂))h.
- Qᵢ at position i(n + 1)/4. Range, QD = (Q₃ − Q₁)/2, MD = Σ|x − x̄|/n.
- σ² = Σ(x − x̄)²/n = Σx²/n − x̄²; s² divides by n − 1. CV = σ/x̄ × 100.
- Mean − mode ≈ 3(mean − median). Σ(x − x̄) = 0.

## Chapter summary

- Mean, median and mode locate the centre; quartiles, deciles and percentiles split the data.
- Range, QD, MD, variance, standard deviation and CV measure spread; CV compares different data sets.
- The median resists outliers; the standard deviation is the standard measure of spread.

## Practice

1. Data: 4, 8, 6, 10, 12. Find the mean, median, population and sample standard deviation, and CV.
2. For the frequency distribution in 2.1 find D₆ (the 6th decile) and P₉₀.
3. Why is the median preferred for income data?
4. Two classes have means 70 and 55 with σ = 10 and 9. Which class is more consistent?
5. State the effect on the mean and standard deviation if every mark is increased by 5 and then doubled.
6. Prove Σ(x − x̄) = 0.
7. Compute the median of the data 3, 7, 7, 2, 9, 4.

::: note Answers and worked solutions
**1.** Mean 40/5 = **8**; ordered 4, 6, 8, 10, 12, median **8**. Squared deviations 16, 0, 4, 4, 16 = 40: population variance 8, σ = **2.83**; sample variance 10, s = **3.16**; CV = 2.83/8 × 100 = **35.4%**.
**2.** D₆: 6n/10 = 30 lies in 40–50 (cumulative 44; cf = 28): 40 + (30 − 28)/16 × 10 = **41.25**. P₉₀: 90n/100 = 45 lies in 50–60 (cf = 44, f = 6): 50 + (45 − 44)/6 × 10 = **51.67**.
**3.** A few very high incomes pull the mean upward; the median is unaffected by extremes.
**4.** CV₁ = 10/70 × 100 = 14.3%; CV₂ = 9/55 × 100 = 16.4%. The first class is **more consistent**.
**5.** +5: mean + 5, σ unchanged; then ×2: mean = 2(x̄ + 5), σ = 2σ.
**6.** Σ(x − x̄) = Σx − n·x̄ = Σx − Σx = 0.
**7.** Ordered 2, 3, 4, 7, 7, 9: middle values 4 and 7 → **5.5**.
:::
