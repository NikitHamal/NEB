# Probability and Statistics — BCA 205 (Semester III, 3 credits)

Old code CAST202 (2074 curriculum: 3 h theory, 1 h tutorial, 1 h practical per week; 7 units, 45 hours).

| Unit | Title | Hours |
|---|---|---|
| 1 | Introduction to Statistics | 3 |
| 2 | Descriptive Statistics | 6 |
| 3 | Correlation and Regression Analysis | 6 |
| 4 | Probability (laws, conditional, binomial, Poisson, normal) | 8 |
| 5 | Sample Survey | 6 |
| 6 | Sample Survey Methods (SRS, stratified, systematic, cluster, multistage, PPS, ratio/regression, t, χ², z) | 10 |
| 7 | Design of Experiment (ANOVA) | 6 |

## Verification

`bca/tools/check_stats.py` (and `check_stats41.py` for the session 41 sections) recomputes every numerical example (mean/median/quartiles, grouped statistics, r and the regression lines, binomial/Poisson/normal probabilities, Bayes, sample sizes, SRS/stratified/ratio estimates, t, z and χ² results, both ANOVA tables) with Python's `statistics`, NumPy and SciPy, and the book quotes the printed values. Practice answers were worked by hand and re-checked with the same script. The SPSS laboratory in the syllabus is not reproduced; Excel and Python equivalents are mentioned where relevant.

## Source and honesty

Unit titles, topics and hours are the TU **CAST202** syllabus as reproduced on notebahadur.com (see `bca/SOURCES.md`); the revised BCA 205 PDF was not retrievable. The syllabus lists unit 6's "sampling distributions (t, χ², z)" inside the survey-methods unit and it is kept there. The syllabus contains "Ratio and regression method of estimation under simple and stratified random sampling": the stratified (separate/combined) ratio estimators are mentioned but not derived.

## Session 41 additions (78 -> 98 pages)

2.5 geometric, harmonic and weighted means; 2.6 moments, skewness, kurtosis, Chebyshev (Fig 2.4). 3.5 r-squared, standard error of estimate, probable error, t test of r (Fig 3.3); 3.6 partial and multiple correlation, Simpson's paradox. 4.7 expectation, variance rules, joint tables, covariance; 4.8 hypergeometric, geometric, uniform, exponential, normal approximation with continuity correction, CLT (Figs 4.4, 4.5). 6.11 hypothesis testing in full: errors, power, one-sample, two-sample, paired, F and proportion tests (Fig 6.4). 7.7 Latin square design with a worked ANOVA, comparison of CRD/RBD/LSD, least significant difference (Fig 7.5). Every unit gained practice items with worked answers. All numbers are recomputed by `check_stats41.py`; constants in the examples are illustrative.

## Layout notes from the PDF QA

98 pages, fails=0, 16 warnings (6.2 pt photo credits).
