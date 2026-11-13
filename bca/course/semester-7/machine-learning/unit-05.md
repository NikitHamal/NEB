---
subject: Machine Learning
grade: BCA Semester 7 (Elective I)
unit: 5
title: Measures for Performance Evaluation of ML Algorithms
hours: 8
area: BCA 405 · Machine Learning · Unit 5
---

A cancer-screening model reports "99 percent accuracy". If only 1 percent of patients have cancer, a program that says "healthy" to everybody scores exactly that, and misses every sick patient. Choosing the **right measure** is as important as choosing the algorithm. This unit gives the standard measures for classifiers (accuracy, the confusion matrix, costs, sensitivity and specificity, precision and recall, ROC curves), and the statistics (box plots, confidence intervals, cross-validation) that tell you whether a difference between two models is real.

::: key What this unit gives you
- Classification accuracy and the confusion matrix, and when accuracy misleads.
- Misclassification costs and cost-sensitive decisions.
- Sensitivity, specificity, precision, recall and the F1 score.
- The ROC curve, the area under it, and how to build it from scores.
- Box plots, confidence intervals and k-fold cross-validation, ending with a template for the course mini-project.
:::

## 5.1 Classification accuracy and the confusion matrix

A **confusion matrix** counts predictions against truth. For a binary problem with a *positive* class (the one we want to detect: disease, fraud, spam):

| | Predicted positive | Predicted negative |
|---|---|---|
| **Actual positive** | True positive (TP) | False negative (FN) |
| **Actual negative** | False positive (FP) | True negative (TN) |

$$\text{Accuracy}=\frac{TP+TN}{TP+TN+FP+FN}, \qquad \text{Error rate}=1-\text{Accuracy}.$$

For more than two classes the matrix is $c\times c$: the diagonal holds correct predictions and the off-diagonal cells show *which* classes are confused with which.

**When accuracy misleads.** With **class imbalance** accuracy rewards ignoring the rare class. A fraud detector on 10,000 transactions with 20 frauds that flags nothing has accuracy 99.8 percent and detects no fraud. Use the measures below, and always compare with a **baseline** such as "always predict the majority class".

## 5.2 Misclassification costs

The two errors rarely cost the same. A false negative in cancer screening (a missed cancer) is far worse than a false positive (an extra test). A **cost matrix** assigns a cost to every cell (correct predictions usually cost 0) and the **total cost** is $C=c_{FP}\cdot FP+c_{FN}\cdot FN$. The best model for the business is the one with the lowest cost, which may *not* be the most accurate. Two ways to build it in: train as usual and **move the decision threshold** (flag as positive when the probability exceeds $c_{FP}/(c_{FP}+c_{FN})$, from the minimum-risk rule of Unit 3), or give the costly class a higher weight during training.

## 5.3 Sensitivity, specificity, recall and precision

| Measure | Formula | Question it answers |
|---|---|---|
| **Sensitivity** = **recall** = true-positive rate (TPR) | $\dfrac{TP}{TP+FN}$ | Of all actual positives, how many did we catch? |
| **Specificity** = true-negative rate (TNR) | $\dfrac{TN}{TN+FP}$ | Of all actual negatives, how many did we correctly clear? |
| **Precision** (positive predictive value) | $\dfrac{TP}{TP+FP}$ | Of all that we flagged, how many were truly positive? |
| **False-positive rate** (FPR) | $\dfrac{FP}{FP+TN}=1-\text{specificity}$ | Of all actual negatives, how many did we wrongly flag? |
| **F1 score** | $\dfrac{2PR}{P+R}$ | Harmonic mean of precision $P$ and recall $R$ |

Recall and precision pull in opposite directions: flagging more cases raises recall and lowers precision. The **harmonic** mean punishes a big gap: precision 1.0 with recall 0.1 gives F1 = 0.18, not 0.55. Use *recall* when misses are costly (disease, fraud) and *precision* when false alarms are costly (spam filter blocking real mail).

::: example A screening test on 100 people (50 ill, 50 healthy)
TP = 40, FN = 10, FP = 5, TN = 45. Accuracy = 85/100 = 0.85. Sensitivity = 40/50 = 0.80. Specificity = 45/50 = 0.90. Precision = 40/45 = 0.889. F1 = 2(0.889)(0.80)/(0.889+0.80) = 0.842. If a missed case costs Rs 50 and a false alarm Rs 5: total cost = 10(50) + 5(5) = Rs 525, average Rs 5.25 per person.
:::

```python
def report(TP, FN, FP, TN, c_fn=50, c_fp=5):
    n = TP + FN + FP + TN
    P = TP / (TP + FP) if TP + FP else 0.0; R = TP / (TP + FN)
    print("accuracy %.3f | sensitivity %.3f | specificity %.3f | precision %.3f | F1 %.3f | cost %d"
          % ((TP + TN) / n, R, TN / (TN + FP), P, 2 * P * R / (P + R) if P + R else 0, c_fn * FN + c_fp * FP))
report(40, 10, 5, 45)
print("imbalanced: 10 ill in 1000, classifier always says healthy")
report(0, 10, 0, 990)
```
```output
accuracy 0.850 | sensitivity 0.800 | specificity 0.900 | precision 0.889 | F1 0.842 | cost 525
imbalanced: 10 ill in 1000, classifier always says healthy
accuracy 0.990 | sensitivity 0.000 | specificity 1.000 | precision 0.000 | F1 0.000 | cost 500
```
## 5.4 The ROC curve

Most classifiers output a **score** (probability) and a **threshold** turns it into a class. Moving the threshold trades sensitivity against specificity. The **ROC curve** (receiver operating characteristic) plots **TPR (y) against FPR (x)** for *every* threshold. The corner (0,1) is perfect; the diagonal is random guessing; a curve bowed towards the top-left is better. The **area under the curve (AUC)** summarises the curve in one number: 1.0 is perfect, 0.5 is random, and AUC equals the probability that a random positive receives a higher score than a random negative.

**Construction.** Sort examples by score from high to low, then start at (0,0) and move up one step for every positive and right one step for every negative.

::: example Ten scored examples
Positives have scores 0.95, 0.85, 0.70, 0.60, 0.45 and negatives 0.80, 0.55, 0.40, 0.30, 0.20. Sorted: 0.95(P), 0.85(P), 0.80(N), 0.70(P), 0.60(P), 0.55(N), 0.45(P), 0.40(N), 0.30(N), 0.20(N). Each positive step is $1/5=0.2$ up and each negative step $1/5=0.2$ right. Counting, for each positive, the negatives below it: 5, 5, 4, 4, 3, total 21 of 25 pairs, so AUC $=21/25=0.84$.
:::

```python
pos = [0.95, 0.85, 0.70, 0.60, 0.45]; neg = [0.80, 0.55, 0.40, 0.30, 0.20]
pts = [(0.0, 0.0)]; tp = fp = 0
for score, lab in sorted([(s, 1) for s in pos] + [(s, 0) for s in neg], reverse=True):
    tp += lab; fp += 1 - lab
    pts.append((fp / len(neg), tp / len(pos)))
print("ROC points (FPR, TPR):", pts)
auc = sum((x2 - x1) * (y1 + y2) / 2 for (x1, y1), (x2, y2) in zip(pts, pts[1:]))
pairs = sum(p > n for p in pos for n in neg)
print("AUC by trapezoids = %.2f, by pair counting = %d/25 = %.2f" % (auc, pairs, pairs / 25))
for th in (0.9, 0.65, 0.5, 0.35):
    tpr = sum(p >= th for p in pos) / 5; fpr = sum(n >= th for n in neg) / 5
    print("threshold %.2f -> TPR %.1f, FPR %.1f" % (th, tpr, fpr))
```
```output
ROC points (FPR, TPR): [(0.0, 0.0), (0.0, 0.2), (0.0, 0.4), (0.2, 0.4), (0.2, 0.6), (0.2, 0.8), (0.4, 0.8), (0.4, 1.0), (0.6, 1.0), (0.8, 1.0), (1.0, 1.0)]
AUC by trapezoids = 0.84, by pair counting = 21/25 = 0.84
threshold 0.90 -> TPR 0.2, FPR 0.0
threshold 0.65 -> TPR 0.6, FPR 0.2
threshold 0.50 -> TPR 0.8, FPR 0.4
threshold 0.35 -> TPR 1.0, FPR 0.6
```
```svgfig label="5.1" caption="ROC curve of the ten-example classifier (blue steps) against the random-guess diagonal (dashed). The area under the blue curve is 0.84. Lowering the threshold moves along the curve from (0,0) towards (1,1): sensitivity rises but so does the false-positive rate."
f = Fig(580, 270)
ax = Axes(f, 70, 15, 220, 220, (0, 1), (0, 1))
ax.grid(0.2, 0.2, xfmt=lambda v: "%.1f" % v, yfmt=lambda v: "%.1f" % v)
ax.axes("false-positive rate", "true-positive rate")
pos = [0.95, 0.85, 0.70, 0.60, 0.45]; neg = [0.80, 0.55, 0.40, 0.30, 0.20]
pts = [(0.0, 0.0)]; tp = fp = 0
for s, l in sorted([(s, 1) for s in pos] + [(s, 0) for s in neg], reverse=True):
    tp += l; fp += 1 - l
    pts.append((fp / 5, tp / 5))
f.line(ax.X(0), ax.Y(0), ax.X(1), ax.Y(1), color=SLATE, sw=1.4, dash=True)
for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
    f.line(ax.X(x1), ax.Y(y1), ax.X(x2), ax.Y(y2), color=NAVY, sw=2.6)
for x, y in pts:
    ax.pt(x, y, "", r=3.5, color=RED)
f.text(430, 70, "AUC = 0.84", size=12, color=NAVY, bold=True)
f.text(430, 100, "perfect: (0, 1)", size=10.5, color=TEAL)
f.text(430, 122, "random: diagonal, AUC 0.5", size=10.5, color=SLATE)
f.text(430, 144, "better curves bow to", size=10.5, color=SLATE)
f.text(430, 162, "the top-left corner", size=10.5, color=SLATE)
```

## 5.5 Regression measures

For numeric predictions, with errors $e_i=\hat y_i-y_i$: **MAE** $=\frac1N\sum|e_i|$ (average size of error, same units as $y$), **MSE** $=\frac1N\sum e_i^2$ and **RMSE** $=\sqrt{\text{MSE}}$ (punish big errors), and $R^2=1-\frac{\sum e_i^2}{\sum(y_i-\bar y)^2}$ (share of variance explained; 0 means no better than predicting the mean). RMSE is at least MAE; a large gap means a few big errors.

## 5.6 Box plots and variability of results

One accuracy number hides how much a model varies. Run the evaluation several times (different folds or random splits) and show the spread with a **box plot**, which draws the **five-number summary**: minimum, first quartile $Q_1$, median, third quartile $Q_3$ and maximum. The box covers $Q_1$ to $Q_3$ (the middle 50 percent), a line marks the median, and the **whiskers** extend to the most extreme values within $1.5\times\text{IQR}$ of the box, where $\text{IQR}=Q_3-Q_1$. Points beyond the whiskers are plotted individually as **outliers**.

```python
import numpy as np
A = np.array([0.82, 0.85, 0.84, 0.86, 0.83, 0.85, 0.87, 0.84, 0.83, 0.85])
B = np.array([0.80, 0.90, 0.78, 0.88, 0.82, 0.92, 0.75, 0.86, 0.89, 0.79])
for name, v in (("Model A", A), ("Model B", B)):
    q1, med, q3 = np.percentile(v, [25, 50, 75])
    print(name, "min %.3f Q1 %.4f median %.3f Q3 %.4f max %.3f | IQR %.4f | mean %.3f sd %.3f" % (v.min(), q1, med, q3, v.max(), q3 - q1, v.mean(), v.std(ddof=1)))
```
```output
Model A min 0.820 Q1 0.8325 median 0.845 Q3 0.8500 max 0.870 | IQR 0.0175 | mean 0.844 sd 0.015
Model B min 0.750 Q1 0.7925 median 0.840 Q3 0.8875 max 0.920 | IQR 0.0950 | mean 0.839 sd 0.058
```
```svgfig label="5.2" caption="Box plots of ten-fold accuracy for two models with almost the same mean. Model A is consistent (narrow box); Model B swings widely between folds (wide box), so its performance on a new data set is much less predictable."
f = Fig(580, 230)
ax = Axes(f, 70, 15, 300, 170, (0, 3), (0.70, 0.95))
ax.grid(1, 0.05, labels=False)
ax.axes("", "")
def pc(v, p):
    v = sorted(v); k = (len(v) - 1) * p / 100.0; i = int(k)
    return v[i] + (v[min(i + 1, len(v) - 1)] - v[i]) * (k - i)
data = {1: [0.82, 0.85, 0.84, 0.86, 0.83, 0.85, 0.87, 0.84, 0.83, 0.85], 2: [0.80, 0.90, 0.78, 0.88, 0.82, 0.92, 0.75, 0.86, 0.89, 0.79]}
for x, v in data.items():
    q1, md, q3 = pc(v, 25), pc(v, 50), pc(v, 75)
    col = TEAL if x == 1 else RED
    fill = MINT if x == 1 else ROSE
    f.line(ax.X(x), ax.Y(min(v)), ax.X(x), ax.Y(max(v)), color=col, sw=2)
    for y in (min(v), max(v)):
        f.line(ax.X(x - 0.15), ax.Y(y), ax.X(x + 0.15), ax.Y(y), color=col, sw=2)
    f.box(ax.X(x - 0.3), ax.Y(q3), ax.X(x + 0.3) - ax.X(x - 0.3), ax.Y(q1) - ax.Y(q3), "", fill=fill, stroke=col)
    f.line(ax.X(x - 0.3), ax.Y(md), ax.X(x + 0.3), ax.Y(md), color=col, sw=3)
    f.text(ax.X(x), 205, "Model " + "AB"[x - 1], size=11, color=col, bold=True)
for y in (0.70, 0.75, 0.80, 0.85, 0.90, 0.95):
    f.text(60, ax.Y(y) + 4, "%.2f" % y, size=9.5, color=SLATE, anchor="end")
f.text(450, 80, "box: Q1 to Q3", size=10.5, color=SLATE)
f.text(450, 102, "thick line: median", size=10.5, color=SLATE)
f.text(450, 124, "whiskers: min and max", size=10.5, color=SLATE)
```

## 5.7 Confidence intervals

A test accuracy of 0.85 on 100 cases is an *estimate* of the true accuracy. A **confidence interval** gives a range likely to contain the truth. Treat each test case as an independent success/failure with true accuracy $p$; the sample proportion $\hat p$ has standard error $\sqrt{\hat p(1-\hat p)/n}$ and the **95 percent confidence interval** (normal approximation, valid when $n\hat p$ and $n(1-\hat p)$ exceed about 10) is

$$\hat p \pm 1.96\sqrt{\frac{\hat p\,(1-\hat p)}{n}}.$$

For 90 percent use 1.645 and for 99 percent 2.576. For the mean of $k$ cross-validation scores use $\bar x\pm t\,s/\sqrt k$ with the $t$ value for $k-1$ degrees of freedom. Intervals that **overlap** heavily mean the data cannot show that one model is better; to *prove* a difference, use a paired test on the same folds.

```python
from math import sqrt
for n in (100, 400, 1000):
    p = 0.85; se = sqrt(p * (1 - p) / n)
    print("n = %4d  accuracy 0.85  95%% CI = [%.3f, %.3f]  (+/- %.3f)" % (n, p - 1.96 * se, p + 1.96 * se, 1.96 * se))
n_needed = (1.96 / 0.02) ** 2 * 0.85 * 0.15
print("test cases needed for +/- 0.02:", round(n_needed))
```
```output
n =  100  accuracy 0.85  95% CI = [0.780, 0.920]  (+/- 0.070)
n =  400  accuracy 0.85  95% CI = [0.815, 0.885]  (+/- 0.035)
n = 1000  accuracy 0.85  95% CI = [0.828, 0.872]  (+/- 0.022)
test cases needed for +/- 0.02: 1225
```
## 5.8 Cross-validation and fair evaluation

**k-fold cross-validation** splits the data into $k$ equal folds (usually $k=5$ or $10$). Each fold serves once as the validation set while the model is trained on the other $k-1$; the $k$ scores are averaged. All data is used for both training and validation, and the spread of the scores shows the variability. **Stratified** folds keep the class proportions in every fold, essential with imbalance; **leave-one-out** ($k=N$) is nearly unbiased but slow. Rules for fair evaluation: split *before* any scaling, feature selection or balancing (otherwise validation information leaks into training); never tune on the test set; report the baseline; report more than accuracy; and give the interval, not just a single number.

```python
import numpy as np
rng = np.random.default_rng(5)
X = np.r_[rng.normal(0, 1, (60, 2)), rng.normal(2, 1, (60, 2))]; y = np.r_[np.zeros(60), np.ones(60)]
idx = rng.permutation(120); folds = np.array_split(idx, 5); scores = []
for i in range(5):
    te = folds[i]; tr = np.concatenate([folds[j] for j in range(5) if j != i])
    c0 = X[tr][y[tr] == 0].mean(axis=0); c1 = X[tr][y[tr] == 1].mean(axis=0)
    pred = (np.linalg.norm(X[te] - c1, axis=1) < np.linalg.norm(X[te] - c0, axis=1)).astype(float)
    scores.append((pred == y[te]).mean())
print("fold accuracies:", np.round(scores, 3), "mean %.3f sd %.3f" % (np.mean(scores), np.std(scores, ddof=1)))
```
```output
fold accuracies: [1.    1.    0.875 0.917 0.875] mean 0.933 sd 0.063
```
## 5.9 Laboratory work and the mini-project

The syllabus requires laboratory work on every unit and a small project in Python or MATLAB. A sound template:

| Step | What to do | Unit |
|---|---|---|
| 1. Problem and data | State the task (for example, predict student pass/fail), collect or choose a data set, describe each feature | 1 |
| 2. Clean and explore | Handle missing values, plot distributions, check class balance | 1, 5 |
| 3. Split | Train, validation and test (or cross-validation) | 1 |
| 4. Baselines and models | Majority-class baseline, then two or three of: regression, tree, k-NN, naive Bayes, SVM, small neural network | 2, 3 |
| 5. Structure | Optionally cluster or reduce with PCA and plot | 4 |
| 6. Evaluate | Confusion matrix, precision, recall, F1, ROC and AUC, cross-validated mean with interval | 5 |
| 7. Report | Which model, why, what it cannot do, ethical concerns (bias, privacy) | all |

Suggested laboratory sequence: (1) statistics and plots with NumPy and matplotlib; (2) linear regression by the normal equation and gradient descent; (3) perceptron on AND, OR, XOR; (4) back-propagation on XOR; (5) ID3 on PlayTennis; (6) naive Bayes on text; (7) k-NN with different k; (8) k-means and hierarchical clustering; (9) PCA on a data set; (10) confusion matrix, ROC and cross-validation of all earlier models.

## 5.10 Summary and exercises

Accuracy hides class imbalance, so read the confusion matrix and use sensitivity, specificity, precision, recall and F1 as the problem demands; weight errors by their costs; the ROC curve and AUC show performance across all thresholds; box plots and confidence intervals show the variability of results; cross-validation with careful splitting gives a fair estimate.

1. A classifier gives TP = 30, FN = 20, FP = 10, TN = 140. Compute accuracy, sensitivity, specificity, precision and F1.
2. Why is accuracy a poor measure for fraud detection? Give a numerical example.
3. For the matrix in Question 1, with a missed case costing Rs 200 and a false alarm Rs 10, find the total cost.
4. Explain precision and recall and the trade-off between them. When is each more important?
5. Construct the ROC curve and AUC for positives 0.9, 0.7, 0.5 and negatives 0.8, 0.4, 0.3.
6. Compute the 95 percent confidence interval for an accuracy of 0.90 on 200 test cases.
7. Explain k-fold cross-validation and why stratification matters.
8. What does a box plot show? Interpret two box plots with equal medians but different box heights.
9. List the steps of a machine-learning mini-project.

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Measures for TP = 30, FN = 20, FP = 10, TN = 140 (n = 200).**

Accuracy $=170/200=0.85$. Sensitivity $=30/50=0.60$. Specificity $=140/150=0.933$. Precision $=30/40=0.75$. F1 $=2(0.75)(0.60)/(1.35)=0.667$. Cost with Rs 200 per miss and Rs 10 per false alarm: $20(200)+10(10)=$ Rs 4,100.

*Comment.* Accuracy looks good (0.85) but the model misses 40 percent of the positives; with costly misses, a lower threshold is justified.

**Q2 (5 marks). ROC and AUC for positives 0.9, 0.7, 0.5 and negatives 0.8, 0.4, 0.3.**

Sorted: 0.9(P), 0.8(N), 0.7(P), 0.5(P), 0.4(N), 0.3(N). Each P step is 1/3 up, each N step 1/3 right. Path: (0,0) → (0,1/3) → (1/3,1/3) → (1/3,2/3) → (1/3,1) → (2/3,1) → (1,1). Pairs with the positive higher: 0.9 beats all 3 negatives; 0.7 beats 0.4 and 0.3 (2); 0.5 beats 0.4 and 0.3 (2); total 7 of 9, so **AUC = 7/9 = 0.78**.

**Q3 (5 marks). 95 percent confidence interval for accuracy 0.90 with n = 200.**

$SE=\sqrt{0.9(0.1)/200}=\sqrt{0.00045}=0.0212$. Margin $=1.96\times0.0212=0.0416$. Interval $=[0.858,\,0.942]$. With only 50 cases the margin would be 0.083, which shows why small test sets give unreliable results.

**Q4 (10 marks). Explain the confusion matrix and the measures derived from it.**

*Introduction.* The confusion matrix tabulates actual against predicted classes and is the source of all classification measures.

*Body.* (1) Cells TP, FN, FP, TN. (2) Accuracy $(TP+TN)/n$, which fails under imbalance. (3) Sensitivity (recall) $TP/(TP+FN)$ and specificity $TN/(TN+FP)$. (4) Precision $TP/(TP+FP)$. (5) F1 $=2PR/(P+R)$. (6) Costs $c_{FP}FP+c_{FN}FN$.

*Example.* For TP = 40, FN = 10, FP = 5, TN = 45: accuracy 0.85, recall 0.80, specificity 0.90, precision 0.889, F1 0.842. For 10 ill people in 1,000, a model that predicts "healthy" for everyone has accuracy 0.99 but recall 0.

*Conclusion.* Report the full matrix and choose the measure that matches the cost of each error.

**Q5 (10 marks). Describe k-fold cross-validation and the construction and interpretation of the ROC curve.**

*Cross-validation.* Partition the data into $k$ folds; for each fold train on the other $k-1$ and test on it; average the $k$ scores and report the mean with its spread or interval. It uses all data for training and testing and reveals variability; stratification keeps class proportions; all preprocessing must be fitted inside each training fold.

*ROC.* A model gives scores; a threshold gives a class. Varying the threshold from high to low and plotting TPR against FPR traces the curve from (0,0) to (1,1). The diagonal is chance, the top-left corner is perfect, and the AUC (0.5 to 1) equals the probability that a random positive outranks a random negative. For the ten-example classifier of Section 5.4 the AUC is 0.84. The curve lets us choose a threshold to suit costs, and compare models independently of any one threshold.

*Conclusion.* Cross-validation gives a trustworthy estimate of how well the model generalises; the ROC curve shows how it behaves at every operating point.
