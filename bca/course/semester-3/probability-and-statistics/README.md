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

`bca/tools/check_stats.py` recomputes every numerical example (mean/median/quartiles, grouped statistics, r and the regression lines, binomial/Poisson/normal probabilities, Bayes, sample sizes, SRS/stratified/ratio estimates, t, z and χ² results, both ANOVA tables) with Python's `statistics`, NumPy and SciPy, and the book quotes the printed values. Practice answers were worked by hand and re-checked with the same script. The SPSS laboratory in the syllabus is not reproduced; Excel and Python equivalents are mentioned where relevant.

## Source and honesty

Unit titles, topics and hours are the TU **CAST202** syllabus as reproduced on notebahadur.com (see `bca/SOURCES.md`); the revised BCA 205 PDF was not retrievable. The syllabus lists unit 6's "sampling distributions (t, χ², z)" inside the survey-methods unit and it is kept there. The syllabus contains "Ratio and regression method of estimation under simple and stratified random sampling": the stratified (separate/combined) ratio estimators are mentioned but not derived.

## Layout notes from the PDF QA

30 pages, 0 hard failures. Two near-empty-page warnings: p3 is the table-of-contents overflow and p10 is the last answers of a chapter spilling onto a new page before the next chapter begins.
