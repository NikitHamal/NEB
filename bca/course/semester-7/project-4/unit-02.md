---
subject: Project IV
grade: BCA Semester 7
unit: 2
title: Data: Collection, Cleaning, Features and Leakage
area: BCA 404 · Project IV · Unit 2
---

Experienced data scientists say that most of a project is spent on the data, and a capstone is no different. A weak model on honest, clean data beats a clever model on messy data, and the examiner will ask about the data before asking about the model. This unit follows SikshyaSignal's 600 students from the attendance register to a table of numbers that a model can learn from, and ends with the most dangerous mistake in the whole project, **data leakage**.

::: key What this unit gives you
- A **data sheet** that documents every column, its unit, valid range and source.
- The five common data faults (missing, impossible, duplicate, inconsistent, outlier) and an executed cleaning script.
- Feature scaling, derived features and a correlation check, with real printed numbers.
- A stratified train, validation and test split, and a leakage experiment that shows how a "perfect" model can be a cheat.
:::

## 2.1 Where the data comes from, and the data sheet

SikshyaSignal's imagined inputs come from three places inside the college: the **attendance register** (kept by each subject teacher), the **assignment log** (kept in the learning platform) and the **examination section** (internal marks and the previous semester's GPA). Using only data the college already holds, with the students told that it is used for support, is both simpler and more ethical than collecting anything new.

Before any code, write a **data sheet**. It is a table that lets a stranger understand every column.

| Column | Meaning | Unit | Valid range | Source | Known at week 6? |
|---|---|---|---|---|---|
| attendance | classes attended divided by classes held | % | 0 to 100 | attendance register | yes |
| internal | first internal exam mark | marks | 0 to 40 | examination section | yes |
| assignment | share of assignments submitted on time | % | 0 to 100 | learning platform | yes |
| prev_gpa | GPA of the previous level | points | 0 to 4 | examination section | yes |
| commute | travel time to college | minutes | 0 to 240 | admission form | yes |
| fails | failed at least one subject at the final | 0 or 1 | 0 or 1 | final result | **no: this is the label** |

The last column is the most important. **A feature may be used only if it would truly be known at the moment the prediction is made.** The label "fails" is known only after the final exam, so it can never be an input. Section 2.5 shows what goes wrong when this rule is broken.

## 2.2 Five data faults and a cleaning script

Real data is never clean on arrival. Five faults appear in almost every project.

| Fault | Example in SikshyaSignal | Usual treatment |
|---|---|---|
| Missing value | a teacher forgot to enter assignments for 30 students | impute (median) and add a "was missing" flag |
| Impossible value | attendance of 120 percent, a mark of −1 | treat as missing, then impute |
| Duplicate row | the same student exported twice | keep the first row per student id |
| Inconsistent units | GPA entered as 3.2 in one file and 80 percent in another | convert to one unit before merging |
| Outlier | a commute of 600 minutes | check with the source; keep if real, cap if a typing error |

The script below takes the clean simulated arrays and **deliberately damages them** (30 missing assignments, 18 missing GPAs, 6 impossible attendance values, 3 negative marks and 12 duplicate rows), then cleans them with the rules above. Because we know exactly what was broken, we can check that the cleaning found everything.

```python
import numpy as np
rng = np.random.default_rng(404)
n = 600
ability = rng.normal(0, 1, n)
attend = np.clip(78 + 4.5*ability + rng.normal(0, 10, n), 30, 100)
internal = np.clip(24 + 5*ability + 0.08*(attend-78) + rng.normal(0, 3.5, n), 0, 40)
assign = np.clip(80 + 6*ability + rng.normal(0, 14, n), 0, 100)
gpa = np.clip(2.9 + 0.45*ability + rng.normal(0, 0.3, n), 1.5, 4.0)
sid = np.arange(1, n + 1)
rng2 = np.random.default_rng(7)
cols = {"id": sid.copy(), "attend": attend.copy(), "internal": internal.copy(), "assign": assign.copy(), "gpa": gpa.copy()}
cols["assign"][rng2.choice(n, 30, replace=False)] = np.nan
cols["gpa"][rng2.choice(n, 18, replace=False)] = np.nan
cols["attend"][rng2.choice(n, 6, replace=False)] = 120.0
cols["internal"][rng2.choice(n, 3, replace=False)] = -1.0
dup = rng2.choice(n, 12, replace=False)
raw = {k: np.concatenate([v, v[dup]]) for k, v in cols.items()}
print("raw rows", len(raw["id"]), "unique ids", len(np.unique(raw["id"])))
print("missing assign", int(np.isnan(raw["assign"]).sum()), "missing gpa", int(np.isnan(raw["gpa"]).sum()))
print("attend > 100:", int((raw["attend"] > 100).sum()), " internal < 0:", int((raw["internal"] < 0).sum()))
_, first = np.unique(raw["id"], return_index=True)
clean = {k: v[np.sort(first)].copy() for k, v in raw.items()}
clean["attend"][clean["attend"] > 100] = np.nan
clean["internal"][clean["internal"] < 0] = np.nan
for k in ("attend", "internal", "assign", "gpa"):
    miss = np.isnan(clean[k])
    med = np.nanmedian(clean[k])
    clean[k + "_missing"] = miss.astype(int)
    clean[k][miss] = med
    print(f"{k:9s} imputed {int(miss.sum()):2d} with median {med:6.2f}")
print("clean rows", len(clean["id"]), "any NaN left:", any(np.isnan(clean[k]).any() for k in ("attend", "internal", "assign", "gpa")))
print("max attend", clean["attend"].max(), "min internal", round(float(clean["internal"].min()), 2))
```
```output
raw rows 612 unique ids 600
missing assign 31 missing gpa 18
attend > 100: 6  internal < 0: 3
attend    imputed  6 with median  78.52
internal  imputed  3 with median  23.34
assign    imputed 30 with median  79.46
gpa       imputed 18 with median   2.89
clean rows 600 any NaN left: False
max attend 100.0 min internal 1.43
```

*Reading the output.* The raw table has 612 rows but only 600 unique ids, so 12 rows are duplicates (the 31 missing assignments in the raw table include one duplicated row; after de-duplication the true count is 30). The checks find all 6 attendance values above 100 and all 3 negative marks. Median imputation fills 6 attendance, 3 internal, 30 assignment and 18 GPA values, leaving no missing value. Imputing with the **median** (not the mean) keeps one extreme student from pulling the fill value. The `_missing` flag columns are kept because *the fact that a value was missing* can itself be informative: a teacher who does not enter assignments may be teaching a class in trouble.

One caution: **compute the medians from the training rows only** and reuse them for validation and test rows. Section 2.4 explains why. Here the medians are computed on all rows to keep the demonstration short.

```photogrid label="2.1" cols="2" ratio="1.1" caption="Data cleaning is done in code, not by hand. (a) Python code on a monitor: every cleaning rule is a line that can be re-run, reviewed and defended, unlike an edit in a spreadsheet. (b) The cleaning flow used in the script: remove duplicates, mark impossible values missing, then impute and flag. Row counts match the printed output."
@ photo id="bca306/code" cap="Cleaning rules written as code"
fit 1.1
focus 0.5 0.5
call 0.5 0.8 0.5 0.6 "re-runnable rules"
@ svg cap="Cleaning flow with row counts"
f = Fig(300, 270)
f.box(20, 10, 260, 40, "Raw table: 612 rows", fill=BLUE, stroke=NAVY, size=12, color=NAVY)
f.box(20, 70, 260, 40, "Drop duplicate ids: 600 rows", fill=SOFT, stroke=TEAL, size=11.5, color=NAVY)
f.box(20, 130, 260, 40, "120% and -1 become missing", fill=SOFT, stroke=AMBER, size=11.5, color=NAVY)
f.box(20, 190, 260, 40, "Median fill + flag: 0 missing", fill=BLUE, stroke=RED, size=11.5, color=NAVY)
for y in (50, 110, 170):
    f.arrow([(150, y), (150, y + 20)], color=NAVY)
f.text(150, 252, "-12 rows, 57 values filled (9 were bad)", size=10.5, color=NAVY)
```

## 2.3 Features: scaling, derived columns and a correlation check

A **feature** is a number that describes one student in a form the model can use. Two steps matter most.

*Scaling.* Attendance runs 0 to 100, GPA only 0 to 4, commute 0 to 240. A learning method that adjusts weights step by step struggles when the columns have such different sizes. The standard cure is the **z-score**: subtract the column mean and divide by its standard deviation, so every column has mean 0 and standard deviation 1.

*Derived features.* Sometimes a combination says more than its parts. An "engagement" score that averages the z-scores of attendance and assignment submission is one example.

The correlation check below tells us which features carry a signal. Correlation with a 0/1 label (called point-biserial correlation) runs from −1 to +1; a negative value means that a higher feature value goes with a lower chance of failing.

```python
import numpy as np
rng = np.random.default_rng(404)
n = 600
ability = rng.normal(0, 1, n)
attend = np.clip(78 + 4.5*ability + rng.normal(0, 10, n), 30, 100)
internal = np.clip(24 + 5*ability + 0.08*(attend-78) + rng.normal(0, 3.5, n), 0, 40)
assign = np.clip(80 + 6*ability + rng.normal(0, 14, n), 0, 100)
gpa = np.clip(2.9 + 0.45*ability + rng.normal(0, 0.3, n), 1.5, 4.0)
commute = rng.gamma(2.0, 20, n)
valley = rng.random(n) < 0.6
z = -2.0 - 0.05*(attend-78) - 0.18*(internal-24) - 0.01*(assign-80) - 0.8*(gpa-2.9) + 0.006*(commute-40)
risk = rng.random(n) < 1/(1+np.exp(-z))
X = np.column_stack([attend, internal, assign, gpa, commute])
names = ["attendance", "internal", "assignment", "prev_gpa", "commute"]
Z = (X - X.mean(axis=0)) / X.std(axis=0)
print("z-score means (rounded):", np.round(Z.mean(axis=0), 3) + 0.0, " sds:", np.round(Z.std(axis=0), 3))
y = risk.astype(int)
for j, nm in enumerate(names):
    r = np.corrcoef(Z[:, j], y)[0, 1]
    print(f"corr({nm:10s}, fails) = {r:+.3f}")
eng = 0.5 * Z[:, 0] + 0.5 * Z[:, 2]
print(f"derived engagement score: corr with fails = {np.corrcoef(eng, y)[0, 1]:+.3f}")
```
```output
z-score means (rounded): [0. 0. 0. 0. 0.]  sds: [1. 1. 1. 1. 1.]
corr(attendance, fails) = -0.349
corr(internal  , fails) = -0.471
corr(assignment, fails) = -0.233
corr(prev_gpa  , fails) = -0.435
corr(commute   , fails) = -0.025
derived engagement score: corr with fails = -0.377
```

*Reading the output.* After scaling every mean prints as 0.0 and every standard deviation as 1.0. The strongest signals are internal marks (−0.471), previous GPA (−0.435) and attendance (−0.349); assignment submission is weaker (−0.233), and **commute time is almost useless** (−0.025). The derived engagement score (−0.377) is stronger than either of its two parts taken separately. A weak feature is not a failure. It is a finding: the report can say "commute time was tested and dropped because its correlation with failure was −0.025". Remember that correlation is not cause: low attendance may be a *symptom* of trouble at home, and the project must not blame the student for it.

```svgfig label="2.1" caption="Attendance histogram split by outcome (counts from the simulator). Students who fail (red) are concentrated between 60 and 90 percent, but passing students (blue) overlap them heavily. The overlap is why no single rule, including 'below 70', can separate the groups cleanly."
f = Fig(580, 230)
f.line(60, 180, 560, 180, color=SLATE)
f.line(60, 30, 60, 180, color=SLATE)
fail = [3, 20, 40, 47, 22, 6]
ok = [0, 9, 61, 151, 166, 75]
for i in range(6):
    x = 80 + i * 80
    h1 = ok[i] * 0.85; h2 = fail[i] * 0.85
    f.box(x, 180 - h1, 30, h1, "", fill=BLUE, stroke=NAVY)
    f.box(x + 32, 180 - h2, 30, h2, "", fill="#fecaca", stroke=RED)
    if ok[i]: f.text(x + 15, 180 - h1 - 7, str(ok[i]), size=9.5, color=NAVY)
    f.text(x + 47, 180 - h2 - 7, str(fail[i]), size=9.5, color=RED)
    f.text(x + 31, 198, f"{40 + 10*i}-{50 + 10*i}", size=10, color=NAVY)
f.text(310, 220, "attendance (%)", size=10.5, color=SLATE)
f.box(70, 34, 12, 12, "", fill=BLUE, stroke=NAVY); f.text(88, 40, "passes (462)", size=10, color=NAVY, anchor="start", vmid=True)
f.box(70, 54, 12, 12, "", fill="#fecaca", stroke=RED); f.text(88, 60, "fails (138)", size=10, color=NAVY, anchor="start", vmid=True)
```

## 2.4 Train, validation and test: three sets with three jobs

A model must be judged on students it has **never seen**. So the data is cut into three parts.

- **Training set** (60 percent): the model learns its weights here.
- **Validation set** (20 percent): used to compare settings such as the decision threshold or the learning rate.
- **Test set** (20 percent): locked away; used **once**, at the very end, to report the final score.

Because only 23 percent of students fail, a random cut could by chance put too few failing students in one part. A **stratified** split cuts each class separately so every part keeps the same failure rate. Any fitted preparation step (medians, means for z-scores) must be computed on the training part only and then applied to the others; otherwise information from the test set has quietly leaked into training.

```python
import numpy as np
rng = np.random.default_rng(404)
n = 600
ability = rng.normal(0, 1, n)
attend = np.clip(78 + 4.5*ability + rng.normal(0, 10, n), 30, 100)
internal = np.clip(24 + 5*ability + 0.08*(attend-78) + rng.normal(0, 3.5, n), 0, 40)
assign = np.clip(80 + 6*ability + rng.normal(0, 14, n), 0, 100)
gpa = np.clip(2.9 + 0.45*ability + rng.normal(0, 0.3, n), 1.5, 4.0)
commute = rng.gamma(2.0, 20, n)
valley = rng.random(n) < 0.6
z = -2.0 - 0.05*(attend-78) - 0.18*(internal-24) - 0.01*(assign-80) - 0.8*(gpa-2.9) + 0.006*(commute-40)
risk = rng.random(n) < 1/(1+np.exp(-z))
y = risk.astype(int)
# stratified 60/20/20 split
rs = np.random.default_rng(11)
tr, va, te = [], [], []
for cls in (0, 1):
    idx = rs.permutation(np.where(y == cls)[0])
    a, b = int(0.6 * len(idx)), int(0.8 * len(idx))
    tr += list(idx[:a]); va += list(idx[a:b]); te += list(idx[b:])
for nm, part in (("train", tr), ("valid", va), ("test", te)):
    print(f"{nm:5s} rows {len(part):3d}  at-risk {y[part].sum():3d}  rate {y[part].mean():.1%}")
print("overlap train/test:", len(set(tr) & set(te)))
```
```output
train rows 359  at-risk  82  rate 22.8%
valid rows 120  at-risk  28  rate 23.3%
test  rows 121  at-risk  28  rate 23.1%
overlap train/test: 0
```

```svgfig label="2.2" caption="Stratified split of the 600 students. Each part keeps about 23 percent failing students. The test set is locked away until the final report and is used exactly once."
f = Fig(580, 150)
f.box(10, 20, 340, 50, "Train: 359 rows, 82 fail (22.8%)", fill=BLUE, stroke=NAVY, size=11.5, color=NAVY)
f.box(354, 20, 112, 50, "Valid: 120\n28 fail (23.3%)", fill=SOFT, stroke=TEAL, size=10.5, color=NAVY)
f.box(470, 20, 100, 50, "Test: 121\n28 fail (23.1%)", fill="#fde68a", stroke=AMBER, size=10.5, color=NAVY)
f.text(180, 95, "learn the weights", size=10.5, color=NAVY)
f.text(410, 95, "tune settings", size=10.5, color=NAVY)
f.text(520, 95, "report once", size=10.5, color=RED, bold=True)
f.arrow([(520, 110), (520, 128)], color=RED)
f.text(520, 142, "locked until the end", size=9.5, color=RED)
```

## 2.5 Data leakage: when a perfect score is a warning

**Leakage** means that information from the future, or from the answer itself, has slipped into the features. The model then looks brilliant in the lab and fails in real use. It is the most common reason a student's "99 percent" result collapses at the defence.

Suppose someone adds a column `remedial_attended`: whether the student went to remedial classes. It looks harmless, but remedial classes are offered *after* students are identified as failing, so the column is largely a **consequence of the label**. The experiment below measures how well single columns rank students using the **AUC**: the probability that a randomly chosen failing student gets a higher risk score than a randomly chosen passing one (0.5 is a coin toss, 1.0 is perfect).

```python
import numpy as np
rng = np.random.default_rng(404)
n = 600
ability = rng.normal(0, 1, n)
attend = np.clip(78 + 4.5*ability + rng.normal(0, 10, n), 30, 100)
internal = np.clip(24 + 5*ability + 0.08*(attend-78) + rng.normal(0, 3.5, n), 0, 40)
assign = np.clip(80 + 6*ability + rng.normal(0, 14, n), 0, 100)
gpa = np.clip(2.9 + 0.45*ability + rng.normal(0, 0.3, n), 1.5, 4.0)
commute = rng.gamma(2.0, 20, n)
valley = rng.random(n) < 0.6
z = -2.0 - 0.05*(attend-78) - 0.18*(internal-24) - 0.01*(assign-80) - 0.8*(gpa-2.9) + 0.006*(commute-40)
risk = rng.random(n) < 1/(1+np.exp(-z))
def auc(score, label):
    order = np.argsort(score)
    ranks = np.empty(len(score)); ranks[order] = np.arange(1, len(score) + 1)
    pos = label == 1
    return (ranks[pos].sum() - pos.sum() * (pos.sum() + 1) / 2) / (pos.sum() * (~pos).sum())
y = risk.astype(int)
r3 = np.random.default_rng(5)
remedial = np.where(y == 1, r3.random(n) < 0.85, r3.random(n) < 0.04).astype(int)
print(f"AUC attendance alone (lower is riskier): {auc(-attend, y):.3f}")
print(f"AUC internal marks alone:                {auc(-internal, y):.3f}")
print(f"AUC remedial_attended (LEAKED):          {auc(remedial + 0.001*r3.random(n), y):.3f}")
print("remedial_attended among failing:", f"{remedial[y==1].mean():.0%}", " among passing:", f"{remedial[y==0].mean():.0%}")
```
```output
AUC attendance alone (lower is riskier): 0.730
AUC internal marks alone:                0.818
AUC remedial_attended (LEAKED):          0.930
remedial_attended among failing: 87%  among passing: 5%
```

*Reading the output.* Attendance alone ranks students with an AUC of 0.730 and internal marks with 0.818: honest, useful signals. The leaked column scores 0.930, better than either, but 87 percent of failing students and only 5 percent of passing students attended remedial classes, which tells us the column records the *response* to being flagged. In real use, at week 6, nobody has attended remedial classes yet, so the column would be empty and the model would collapse. **If one feature is suddenly far better than everything else, suspect leakage before celebrating.**

```svgfig label="2.3" caption="Timeline of the semester. Features must come from before the prediction point (week 6). Remedial attendance and the final result happen after it, so using them as inputs is leakage."
f = Fig(580, 200)
f.line(30, 100, 550, 100, color=NAVY, sw=2.5)
for x, lab, col in ((60, "week 1\nattendance\nstarts", NAVY), (200, "week 4\nassignments\nlogged", NAVY), (300, "week 6\ninternal exam\nPREDICT HERE", RED), (420, "weeks 7-8\nremedial\nclasses", AMBER), (520, "week 14\nfinal result\n= label", AMBER)):
    f.circle(x, 100, 6, fill=col if col == RED else BLUE, stroke=col, sw=2)
    f.text(x, 150, lab.split("\n")[0], size=10.5, color=col, bold=True)
    f.text(x, 166, lab.split("\n")[1], size=9.5, color=col)
    f.text(x, 180, lab.split("\n")[2], size=9.5, color=col, bold=(col == RED))
f.box(40, 30, 250, 30, "usable as features: known before week 6", fill=SOFT, stroke=TEAL, size=10.5, color=NAVY)
f.box(330, 30, 220, 30, "NOT usable: known only afterwards", fill="#fecaca", stroke=RED, size=10.5, color=NAVY)
f.arrow([(300, 94), (300, 62)], color=RED)
```

## 2.6 Eight data habits that examiners notice

1. **Keep the raw file untouched.** Never edit the original export; write all changes as code that produces a new cleaned file. Then anyone, including you after three months, can repeat the steps. Store the raw file read-only and note the date it was exported.
2. **Write the data sheet first.** Every column needs a meaning, unit, valid range and source. Doing this early exposes confusions such as GPA out of 4 versus percentage. A one-page sheet in the report earns marks and prevents mistakes.
3. **Count before and after.** Print row counts and missing counts at every step, as in Section 2.2. A cleaning step that silently removes 200 rows is a bug. Include the count table in the report.
4. **Impute with the training median.** Compute fill values from the training rows only and reuse them on the validation and test rows. Otherwise test-set information leaks into training. Add a missing-flag column so the model can learn from the gap itself.
5. **Scale inside the pipeline.** Fit the mean and standard deviation on training rows and apply them to new students at prediction time. The saved model must carry those numbers. If the service forgets them, every prediction is wrong without any error message.
6. **Test each feature for time.** Ask of every column: "would I know this on the prediction day?" Remove those that fail the test. Write the answer in the data sheet column used in Section 2.1.
7. **Split once and fix the seed.** Make the stratified split with a fixed random seed and save the row ids of each part. Never re-split after seeing results. Repeating the split until the score looks good is a form of cheating even if done innocently.
8. **Protect the people in the rows.** Remove names and phone numbers, replace roll numbers with random ids, and store the file where only the project team can read it. Under Nepal's Individual Privacy Act 2075 personal data needs care. The safest demo uses simulated data, as this book does.

```photogrid label="2.2" cols="2" ratio="1.2" caption="When a perfect score is a warning. (a) Students in an entrance examination: the paper is sealed until the start because knowing the answers in advance makes the result meaningless. (b) A simulated pass or fail table of 600 students (fixed seed) was split 360, 120 and 120. Guessing pass for everyone scores 54 per cent on the unseen test set, attendance alone 62 per cent and study hours alone 68 per cent: realistic, modest numbers for an honest model. A column holding the final-exam mark scores 99 per cent, but that mark is only known after the pass or fail decision, so it leaks the answer and the model would be useless on the day it is needed. When a student project reports almost 100 per cent, check every column for information that would not exist at prediction time."
@ photo id="bcapj/exam" cap="Students in an entrance examination: the test is sealed"
fit 1.2
focus 0.5 0.5
@ svg cap="Honest features vs a leaky one"
import numpy as np
rng = np.random.default_rng(2081)
n = 600
att = rng.normal(75, 12, n).clip(30, 100)
hrs = rng.normal(2.5, 1, n).clip(0, 6)
score = 0.5 * (att - 75) / 12 + 0.6 * (hrs - 2.5) + rng.normal(0, 1.0, n)
y = (score > -0.2).astype(int)
final = np.where(y == 1, rng.normal(58, 8, n), rng.normal(30, 8, n))
tr, va, te = slice(0, 360), slice(360, 480), slice(480, 600)
def stump(x, yy):
    best = (0, 0, 1)
    for t in np.unique(x):
        for s in (1, -1):
            a = np.mean((s * (x - t) > 0).astype(int) == yy)
            if a > best[0]:
                best = (a, t, s)
    return best
def test_acc(x):
    a, t, s = stump(x[tr], y[tr])
    return float(np.mean((s * (x[te] - t) > 0).astype(int) == y[te]))
base = float(max(np.mean(y[te]), 1 - np.mean(y[te])))
acc = [base, test_acc(att), test_acc(hrs), test_acc(final)]
assert acc[3] > 0.9 and acc[1] < 0.8 and acc[2] < 0.8
facts = dict(base=round(acc[0] * 100), att=round(acc[1] * 100), hrs=round(acc[2] * 100), leak=round(acc[3] * 100))
f = Fig(300, 236)
f.text(150, 12, "600 students: 360 train / 120 validate / 120 test", size=10.5, color=NAVY, bold=True)
f.box(6, 22, 180, 16, "train 360", fill=BLUE, stroke=NAVY, size=10.5, r=2, sw=1)
f.box(188, 22, 60, 16, "val 120", fill="#fde68a", stroke=AMBER, size=10.5, r=2, sw=1)
f.box(250, 22, 44, 16, "test", fill="#bbf7d0", stroke=TEAL, size=10.5, r=2, sw=1)
f.text(150, 58, "test accuracy of a one-feature rule", size=10.5, color=SLATE, bold=True)
names = ["always say pass", "attendance only", "study hours only", "final-exam mark"]
cols = ["#e5e7eb", BLUE, BLUE, "#fecaca"]
for i, (nm, a) in enumerate(zip(names, acc)):
    y0 = 68 + i * 30
    f.text(6, y0 + 11, nm, size=10.5, color=NAVY, bold=True, anchor="start", vmid=True)
    f.box(112, y0, a * 140, 22, "", fill=cols[i], stroke=SLATE, r=3, sw=1)
    f.text(118 + a * 140, y0 + 11, "%d%%" % round(a * 100), size=10.5, color=NAVY, bold=True, anchor="start", vmid=True)
f.text(150, 206, "final marks exist only AFTER the result", size=10.5, color=RED, bold=True)
f.text(150, 222, "a near-perfect score is a warning", size=10.5, color=RED, bold=True)
```

## Formula and fact sheet

| Item | Formula or fact |
|---|---|
| z-score | (x − mean) ÷ standard deviation |
| Median imputation | replace a missing value with the column's median from the training rows |
| Point-biserial correlation | Pearson correlation between a feature and a 0/1 label, from −1 to +1 |
| Stratified split | cut each class separately so every part keeps the same class rate |
| AUC | probability that a random positive outranks a random negative; 0.5 = chance |
| Leakage | a feature that is a consequence of the label or is unknown at prediction time |

## Chapter summary

- Document every column in a **data sheet**: meaning, unit, range, source and whether it is known at prediction time.
- Five faults appear in nearly all data: missing, impossible, duplicate, inconsistent and outlier values; clean them in code and print counts.
- **Scale** features with z-scores and check correlations; a weak feature is a finding, not a failure.
- Split into **train, validation and test** with stratification; use the test set once.
- A suspiciously good feature signals **leakage**: information that is not available when the prediction is made.
- Protect people: anonymise, limit access and say when data is simulated.

## Practice

1. Name the five common data faults and one treatment for each.
2. Why is the label never allowed as an input feature?
3. In Section 2.2 the raw table has 612 rows and 600 unique ids. How many duplicates are there, and how were they removed?
4. Why use the median rather than the mean to fill missing values?
5. After z-scoring, what are the mean and standard deviation of every column?
6. Commute time has a correlation of −0.025 with failure. What should the report do with it?
7. Why is a stratified split better than a plain random split for SikshyaSignal?
8. State the three jobs of the training, validation and test sets.
9. Explain why `remedial_attended` is leakage even though it is a real column in the college's records.
10. A model reports an AUC of 0.99 on the first run. List three checks you would make before trusting it.

::: note Answers and worked solutions
**1.** Missing (median fill + flag), impossible (mark missing then fill), duplicate (keep first per id), inconsistent units (convert), outlier (check source, cap if error).
**2.** The label is the answer; using it makes the problem trivial and the model useless on new students.
**3.** 612 − 600 = 12 duplicates; `np.unique` on ids gave the first position of each id and the other rows were dropped.
**4.** One extreme value shifts the mean but barely moves the median.
**5.** Mean 0 and standard deviation 1.
**6.** Report it as a tested and dropped feature, giving the correlation, rather than hiding it.
**7.** Only 23 percent fail, so a random cut could leave a part with too few failing students; stratification keeps 22.8, 23.3 and 23.1 percent.
**8.** Training: learn weights. Validation: choose settings. Test: one honest final score.
**9.** Remedial classes are offered after students are flagged as failing, so the column is a consequence of the outcome and is unknown on the prediction day.
**10.** Check for a leaked column, check that the test set was never used in tuning or imputation, and compare with the baseline and with a single-feature AUC.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Describe the common faults found in real datasets and explain how each was handled in the SikshyaSignal cleaning script.**

*Introduction.* Real data is collected by busy people from several systems, so it nearly always contains faults. A model trained on faulty data learns the faults. Cleaning must therefore be done in code, with counts printed, so that every change can be checked.

*The faults and the treatments.*

1. **Missing values.** Thirty assignment values and eighteen GPA values were empty. They were filled with the column median and a flag column recorded that the value had been missing.
2. **Impossible values.** Six attendance values of 120 percent and three negative internal marks break the valid range in the data sheet. They were first set to missing and then filled in the same way.
3. **Duplicate rows.** The raw table held 612 rows for 600 students. Keeping the first row for each student id removed the 12 duplicates.
4. **Inconsistent units.** If one file gave GPA out of 4 and another a percentage, they would be converted to one unit before the files are joined.
5. **Outliers.** A commute of several hundred minutes is checked with the source before it is kept or capped.

*Evidence.* The script prints the row count before and after (612 then 600) and ends by confirming that no missing value remains.

*Conclusion.* Median imputation, missing flags and printed counts make the cleaning transparent. The medians should be computed on the training rows only so that no test information leaks into the model.

**Q2 (5 marks). Explain the roles of training, validation and test sets and why the test set must be used only once.**

*Introduction.* A model's score on the data it learned from is always flattering. To estimate how it will behave on new students, the data is divided into three parts with three different jobs.

| Set | Share | Job |
|---|---|---|
| Training | 60% (359 rows) | the model adjusts its weights here |
| Validation | 20% (120 rows) | compare settings such as the decision threshold |
| Test | 20% (121 rows) | report the final, honest score |

*Stratification.* Because only 23 percent of students fail, each class was split separately. The failing rate is then 22.8, 23.3 and 23.1 percent in the three parts, so no part is unrepresentative. Figure 2.2 shows the cut.

*Why the test set is used once.* Every time the test score is looked at and the model is changed in response, some information from the test set enters the model. After ten rounds of this the test score is no longer an independent estimate; it has become another training score. Tuning therefore uses the validation set, and the test set is opened a single time for the final report.

*Conclusion.* Three sets give the student a clean way to choose and then to confirm. An examiner who asks "was the test set touched during tuning?" should hear a clear "no".

**Q3 (10 marks). Describe the complete data-preparation process for a machine-learning capstone. Use the early-warning example and discuss the data sheet, cleaning, scaling, feature checks, splitting and the danger of leakage.**

*Introduction.* Data preparation takes most of the time in a data project and decides the quality of the result. For SikshyaSignal it turns attendance registers, assignment logs and examination records into a table of 600 clean rows ready for a model.

*1. Data sheet.* List each column with meaning, unit, valid range, source and whether it is known at the prediction point (week 6). This exposes unit confusion early and gives the examiner a map of the data.

*2. Cleaning.* Print counts, remove the 12 duplicate rows, mark impossible values (attendance 120, marks below zero) as missing, and fill missing values with the training median while keeping a missing flag. Keep the raw file unchanged and perform all edits in code.

*3. Scaling.* Convert each feature to a z-score so that attendance (0 to 100) and GPA (0 to 4) have equal influence. Store the means and standard deviations, because the service must apply the same numbers to new students.

*4. Feature checks.* Correlate each feature with the label. Internal marks (−0.471), GPA (−0.435) and attendance (−0.349) are strong; commute (−0.025) is dropped and reported as such. A derived engagement score (−0.377) combines attendance and assignments. Remember that correlation is not causation.

*5. Splitting.* Make a stratified 60/20/20 split with a fixed seed and save the ids. Fit medians and scaling on the training part only, then apply them elsewhere.

*6. Leakage control.* For every column ask "would this be known at week 6?" The experiment with `remedial_attended` gave an AUC of 0.930, higher than honest features, because remedial classes follow the flagging. It is therefore excluded. Figure 2.3 shows the timeline.

*7. Privacy.* Use random ids, remove names, restrict access and state clearly that the demo data is simulated.

| Step | Output | Check printed |
|---|---|---|
| Data sheet | one table | every column documented |
| Cleaning | 600 rows, no missing | before and after counts |
| Scaling | z-score columns | mean 0, sd 1 |
| Split | 359, 120, 121 rows | class rate per part |
| Leakage test | features list | AUC of each single feature |

*Conclusion.* A careful preparation chapter, with printed evidence at every step, shows the panel that the later model scores can be trusted, and it is the best protection against the question "how do you know your data is right?".
