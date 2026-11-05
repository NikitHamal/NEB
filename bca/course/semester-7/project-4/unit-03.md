---
subject: Project IV
grade: BCA Semester 7
unit: 3
title: Modelling: Logistic Regression from Scratch, Evaluation and Fairness
area: BCA 404 · Project IV · Unit 3
---

This is the unit examiners wait for. With clean data and a locked test set, we now build the model, but the point of a good capstone is not to find the fanciest algorithm. It is to show that the student **understands** the model, **measures** it honestly against baselines, and **checks it for harm**. We write logistic regression from scratch in about ten lines of NumPy, so there is no black box to hide behind.

::: key What this unit gives you
- How logistic regression turns features into a probability, and how gradient descent learns the weights.
- A training log showing the loss falling, and what the learned weights mean (and do not mean).
- Choosing a **threshold** on the validation set, then the single test-set report with the confusion matrix, precision, recall, F1, AUC and precision at the top.
- A 5-fold cross-validation and a **group-fairness check** with a bootstrap interval, so a small gap is not over-read.
:::

## 3.1 Logistic regression in plain words

Linear regression predicts a number. **Logistic regression** predicts a probability that an example belongs to class 1 (here, "will fail"). It works in two steps.

1. Compute a **score**: z = b + w₁x₁ + w₂x₂ + … where each x is a scaled feature and each w is a weight. A negative weight for attendance means that higher attendance lowers the score.
2. Pass the score through the **sigmoid** function, p = 1 ÷ (1 + e^(−z)), which squashes any number into the range 0 to 1.

Learning means finding the weights that make the predicted p close to the true 0/1 labels. The measure of how far off the model is called **log loss**; it is large when the model is confidently wrong. **Gradient descent** repeats a simple loop: compute the predictions, find the error (p − y), nudge each weight a little in the direction that reduces the loss, and repeat.

```svgfig label="3.1" caption="Logistic regression as a picture. Five scaled features are multiplied by weights and added to a bias to give a score; the sigmoid turns the score into a probability; a threshold turns the probability into a flag. Gradient descent adjusts the weights so the loss falls."
f = Fig(580, 230)
names = ["attendance", "internal", "assignment", "prev GPA", "commute"]
for i, nm in enumerate(names):
    y0 = 18 + i * 40
    f.box(8, y0, 92, 28, nm, fill=BLUE, stroke=NAVY, size=10.5, color=NAVY)
    f.arrow([(100, y0 + 14), (190, 108)], color=SLATE, sw=1.1)
    f.text(148, y0 + 3 + (108 - y0) * 0.35, f"w{i+1}", size=9, color=TEAL)
f.circle(215, 108, 28, fill=SOFT, stroke=TEAL, label="score\nz", size=10.5, color=NAVY)
f.arrow([(243, 108), (300, 108)], color=NAVY)
f.box(300, 78, 90, 60, "sigmoid\np = 1/(1+e^-z)", fill=SOFT, stroke=AMBER, size=10, color=NAVY)
f.arrow([(390, 108), (440, 108)], color=NAVY)
f.box(440, 78, 126, 60, "threshold t\nflag if p >= t", fill=BLUE, stroke=RED, size=10.5, color=NAVY)
f.text(340, 170, "loss = how wrong p is", size=10, color=NAVY)
f.arrow([(340, 178), (340, 205), (215, 205), (215, 140)], color=RED, dash=True)
f.text(280, 220, "gradient descent: nudge weights", size=10, color=RED)
```

## 3.2 Training the model and reading the weights

The script prepares the same split as Unit 2, scales with training means only (as Section 2.6 demanded), trains for 400 steps and prints the loss at five moments.

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
y = risk.astype(int)
rs = np.random.default_rng(11)
tr, va, te = [], [], []
for cls in (0, 1):
    idx = rs.permutation(np.where(y == cls)[0])
    a, b = int(0.6 * len(idx)), int(0.8 * len(idx))
    tr += list(idx[:a]); va += list(idx[a:b]); te += list(idx[b:])
tr, va, te = map(np.array, (tr, va, te))
mu, sd = X[tr].mean(axis=0), X[tr].std(axis=0)
Z = (X - mu) / sd
def sigmoid(t): return 1 / (1 + np.exp(-t))
def fit(Z, y, lr=0.2, steps=400, l2=0.0, log=None):
    w = np.zeros(Z.shape[1]); b = 0.0
    for i in range(steps):
        p = sigmoid(Z @ w + b); g = p - y
        if log is not None and i in log:
            loss = -np.mean(y * np.log(p + 1e-12) + (1 - y) * np.log(1 - p + 1e-12))
            print(f"step {i:3d}  loss {loss:.4f}")
        w -= lr * (Z.T @ g / len(y) + l2 * w); b -= lr * g.mean()
    return w, b
def auc(score, label):
    order = np.argsort(score)
    ranks = np.empty(len(score)); ranks[order] = np.arange(1, len(score) + 1)
    pos = label == 1
    return (ranks[pos].sum() - pos.sum() * (pos.sum() + 1) / 2) / (pos.sum() * (~pos).sum())
names = ["attendance", "internal", "assignment", "prev_gpa", "commute"]
w, b = fit(Z[tr], y[tr], log={0, 10, 50, 100, 399})
print("weights:", {k: round(float(v), 3) for k, v in zip(names, w)}, "bias", round(float(b), 3))
for nm, part in (("train", tr), ("valid", va)):
    print(f"{nm} AUC {auc(Z[part] @ w + b, y[part]):.3f}")
```
```output
step   0  loss 0.6931
step  10  loss 0.4924
step  50  loss 0.3713
step 100  loss 0.3499
step 399  loss 0.3399
weights: {'attendance': -0.729, 'internal': -1.191, 'assignment': 0.113, 'prev_gpa': -0.774, 'commute': -0.141} bias -2.054
train AUC 0.876
valid AUC 0.743
```

*Reading the output.* The loss starts at 0.6931 (that is ln 2, the loss of a model that always says 50 percent) and falls quickly to 0.4924 by step 10, then flattens at 0.3399. A flattening curve means the weights have **converged**, so more steps would not help. The training AUC is 0.876 and the validation AUC is **0.743**. The gap is a warning sign of mild over-fitting, made noisier by the fact that the validation set holds only 28 failing students. A student must report both numbers and not only the better one.

*Reading the weights.* Internal marks (−1.191), previous GPA (−0.774) and attendance (−0.729) push the score down, as expected. Notice that **assignment has a small positive weight (+0.113)**, which seems to say that submitting more assignments *raises* the risk. That is not a discovery; assignment submission is correlated with internal marks and attendance, so once those are in the model, its leftover weight is noise. **Weights of correlated features must never be read one at a time as causes.** A report that says "assignments increase failure" would be laughed at in a viva.

```svgfig label="3.2" caption="Learning curve from the training log: log loss against gradient-descent step. The curve starts at ln 2 = 0.693, drops fast and flattens near 0.34. Stop training when the curve is flat, not when the score looks pretty."
f = Fig(580, 230)
ax = Axes(f, 70, 30, 480, 150, (0, 400), (0.3, 0.7))
ax.grid(100, 0.1).axes("", "")
f.text(70, 16, "log loss", size=11, color=SLATE, italic=True, anchor="start")
f.text(310, 216, "gradient-descent step", size=11, color=SLATE, italic=True)
pts = [(0, 0.6931), (10, 0.4924), (50, 0.3713), (100, 0.3499), (399, 0.3399)]
for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
    f.line(ax.X(x0), ax.Y(y0), ax.X(x1), ax.Y(y1), color=RED, sw=2.4)
for x, yv in pts:
    ax.pt(x, yv, "", color=RED)
ax.tag(95, 0.66, "start: 0.6931 (ln 2)", size=10, color=NAVY)
ax.tag(92, 0.5, "0.4924 at step 10", size=10, color=NAVY)
ax.tag(310, 0.385, "0.3399 at step 399", size=10, color=NAVY)
```

## 3.3 Choosing a threshold and reporting the test set once

The model outputs a probability, but a teacher needs a yes or no. The **threshold** t decides: flag a student if p ≥ t. A low threshold flags many students (high recall, many false alarms); a high one flags few (high precision, many misses). The right balance depends on the college's capacity, so the threshold is a **policy choice** and is tuned on the **validation** set, never on the test set.

The script sweeps six thresholds on the validation set, picks the one with the best F1 score (the harmonic mean of precision and recall), and only then opens the test set once.

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
y = risk.astype(int)
rs = np.random.default_rng(11)
tr, va, te = [], [], []
for cls in (0, 1):
    idx = rs.permutation(np.where(y == cls)[0])
    a, b = int(0.6 * len(idx)), int(0.8 * len(idx))
    tr += list(idx[:a]); va += list(idx[a:b]); te += list(idx[b:])
tr, va, te = map(np.array, (tr, va, te))
mu, sd = X[tr].mean(axis=0), X[tr].std(axis=0)
Z = (X - mu) / sd
def sigmoid(t): return 1 / (1 + np.exp(-t))
def fit(Z, y, lr=0.2, steps=400, l2=0.0, log=None):
    w = np.zeros(Z.shape[1]); b = 0.0
    for i in range(steps):
        p = sigmoid(Z @ w + b); g = p - y
        if log is not None and i in log:
            loss = -np.mean(y * np.log(p + 1e-12) + (1 - y) * np.log(1 - p + 1e-12))
            print(f"step {i:3d}  loss {loss:.4f}")
        w -= lr * (Z.T @ g / len(y) + l2 * w); b -= lr * g.mean()
    return w, b
def auc(score, label):
    order = np.argsort(score)
    ranks = np.empty(len(score)); ranks[order] = np.arange(1, len(score) + 1)
    pos = label == 1
    return (ranks[pos].sum() - pos.sum() * (pos.sum() + 1) / 2) / (pos.sum() * (~pos).sum())
w, b = fit(Z[tr], y[tr])
def metrics(pred, label):
    tp = int(((pred == 1) & (label == 1)).sum()); fp = int(((pred == 1) & (label == 0)).sum())
    fn = int(((pred == 0) & (label == 1)).sum()); tn = int(((pred == 0) & (label == 0)).sum())
    pr = tp / (tp + fp) if tp + fp else 0.0; rc = tp / (tp + fn)
    f1 = 2 * pr * rc / (pr + rc) if pr + rc else 0.0
    return tp, fp, fn, tn, pr, rc, f1
pv = sigmoid(Z[va] @ w + b)
print("threshold sweep on VALIDATION set")
best = None
for t in (0.15, 0.20, 0.25, 0.30, 0.40, 0.50):
    tp, fp, fn, tn, pr, rc, f1 = metrics((pv >= t).astype(int), y[va])
    print(f"  t={t:.2f} flagged {tp+fp:3d} precision {pr:.2f} recall {rc:.2f} F1 {f1:.2f}")
    if best is None or f1 > best[1]: best = (t, f1)
t = best[0]
print("chosen threshold (best validation F1):", t)
pt = sigmoid(Z[te] @ w + b)
tp, fp, fn, tn, pr, rc, f1 = metrics((pt >= t).astype(int), y[te])
print(f"TEST confusion: TP {tp} FP {fp} FN {fn} TN {tn}")
print(f"TEST accuracy {(tp+tn)/len(te):.3f} precision {pr:.2f} recall {rc:.2f} F1 {f1:.2f} AUC {auc(pt, y[te]):.3f}")
top = np.argsort(-pt)[:12]
print(f"precision at top 12 (10% of test): {y[te][top].mean():.2f}")
base = metrics((Z[te][:, 0] * sd[0] + mu[0] < 70).astype(int), y[te])
print(f"TEST attendance<70 rule: precision {base[4]:.2f} recall {base[5]:.2f}; do-nothing accuracy {1 - y[te].mean():.3f}")
```
```output
threshold sweep on VALIDATION set
  t=0.15 flagged  50 precision 0.40 recall 0.71 F1 0.51
  t=0.20 flagged  46 precision 0.41 recall 0.68 F1 0.51
  t=0.25 flagged  42 precision 0.40 recall 0.61 F1 0.49
  t=0.30 flagged  36 precision 0.44 recall 0.57 F1 0.50
  t=0.40 flagged  30 precision 0.50 recall 0.54 F1 0.52
  t=0.50 flagged  19 precision 0.53 recall 0.36 F1 0.43
chosen threshold (best validation F1): 0.4
TEST confusion: TP 15 FP 11 FN 13 TN 82
TEST accuracy 0.802 precision 0.58 recall 0.54 F1 0.56 AUC 0.791
precision at top 12 (10% of test): 0.83
TEST attendance<70 rule: precision 0.43 recall 0.46; do-nothing accuracy 0.769
```

*Reading the output.* On the validation set, lowering the threshold raises recall (0.71 at t = 0.15) but cuts precision (0.40); raising it does the opposite. The F1 scores are all close (0.43 to 0.52), so the choice is not sharp: **t = 0.40** has the best F1 (0.52) and is chosen. The test set is then opened once: TP 15, FP 11, FN 13, TN 82. That gives accuracy 0.802, precision 0.58, recall 0.54, F1 0.56 and AUC 0.791. Of the 12 students ranked highest, 10 really fail (**precision at top 12 = 0.83**), which meets objective O3 (at least 60 percent).

| Method on the test set (121 students, 28 fail) | Accuracy | Precision | Recall |
|---|---|---|---|
| Do nothing | 76.9% | undefined | 0% |
| Attendance below 70 rule (TP 13, FP 17, FN 15) | 73.6% | 0.43 | 0.46 |
| Logistic regression, t = 0.40 | 80.2% | 0.58 | 0.54 |

The model beats both baselines, but **honestly it is a modest win**: it still misses 13 of 28 failing students. A report that says "the model finds just over half of failing students and two-thirds of its flags are right in the top ranks, which is better than the attendance rule" is believable. A report that says "the model is 80 percent accurate" is not.

```svgfig label="3.3" caption="Confusion matrix on the test set at threshold 0.40. The 15 true positives are students correctly flagged; the 13 false negatives are failing students the model missed, which is the costly error; the 11 false positives are false alarms that waste teacher time."
f = Fig(580, 230)
f.text(300, 18, "Predicted", size=11, color=NAVY, bold=True)
f.text(200, 40, "flagged", size=10.5, color=NAVY); f.text(410, 40, "not flagged", size=10.5, color=NAVY)
f.text(46, 98, "fails", size=10.5, color=NAVY); f.text(46, 178, "passes", size=10.5, color=NAVY)
f.text(18, 138, "Actual", size=11, color=NAVY, bold=True)
f.box(100, 50, 200, 80, "TP = 15\ncorrectly flagged", fill="#bbf7d0", stroke=TEAL, size=12, color=NAVY)
f.box(310, 50, 200, 80, "FN = 13\nMISSED (costly)", fill="#fecaca", stroke=RED, size=12, color=NAVY)
f.box(100, 140, 200, 80, "FP = 11\nfalse alarm", fill="#fde68a", stroke=AMBER, size=12, color=NAVY)
f.box(310, 140, 200, 80, "TN = 82\ncorrectly left alone", fill="#bbf7d0", stroke=TEAL, size=12, color=NAVY)
f.text(550, 90, "recall", size=10, color=NAVY); f.text(550, 104, "15/28", size=10, color=NAVY)
f.text(550, 180, "precision", size=10, color=NAVY); f.text(550, 194, "15/26", size=10, color=NAVY)
```

```svgfig label="3.4" caption="Precision-recall trade-off on the validation set as the threshold rises from 0.15 to 0.50. Recall (red) falls steadily while precision (blue) creeps up, then both settle; the chosen point t = 0.40 balances them. Moving the threshold is a policy decision about teacher time."
f = Fig(580, 230)
ax = Axes(f, 70, 30, 480, 150, (0.1, 0.55), (0.3, 0.8))
ax.grid(0.1, 0.1).axes("", "")
f.text(70, 16, "score", size=11, color=SLATE, italic=True, anchor="start")
f.text(310, 216, "threshold t", size=11, color=SLATE, italic=True)
T = [0.15, 0.20, 0.25, 0.30, 0.40, 0.50]
P = [0.40, 0.41, 0.40, 0.44, 0.50, 0.53]
R = [0.71, 0.68, 0.61, 0.57, 0.54, 0.36]
for a, b2, col in ((P, None, NAVY), (R, None, RED)):
    for i in range(len(T) - 1):
        f.line(ax.X(T[i]), ax.Y(a[i]), ax.X(T[i + 1]), ax.Y(a[i + 1]), color=col, sw=2.4)
    for i in range(len(T)):
        ax.pt(T[i], a[i], "", color=col)
ax.vline(0.40, color=AMBER)
ax.tag(0.40, 0.77, "chosen t = 0.40", size=10, color=NAVY)
ax.tag(0.2, 0.75, "recall", size=10.5, color=RED, bold=True)
ax.tag(0.2, 0.36, "precision", size=10.5, color=NAVY, bold=True)
```

## 3.4 Cross-validation and a group-fairness check

One test set of 121 students with only 28 failures gives a **noisy** score: a few different students would change the recall by several points. **K-fold cross-validation** reduces the noise. The 600 students are cut into five stratified folds; the model is trained on four and scored on the fifth, five times, so every student is predicted once by a model that never saw them (an **out-of-fold** prediction).

Those out-of-fold predictions also let us check **fairness** with a larger sample. The simulator labels each student as living inside the Kathmandu Valley or outside it. SikshyaSignal never uses that column as a feature, but a model can still treat groups differently through related features such as commute. We compare, for each group, the share flagged, the **recall** (failing students found) and the **false-alarm rate** (passing students wrongly flagged). A **bootstrap** (resampling the 600 students 1,000 times with replacement) gives an interval for the recall gap, so a small gap is not over-read.

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
y = risk.astype(int)
rs = np.random.default_rng(11)
tr, va, te = [], [], []
for cls in (0, 1):
    idx = rs.permutation(np.where(y == cls)[0])
    a, b = int(0.6 * len(idx)), int(0.8 * len(idx))
    tr += list(idx[:a]); va += list(idx[a:b]); te += list(idx[b:])
tr, va, te = map(np.array, (tr, va, te))
mu, sd = X[tr].mean(axis=0), X[tr].std(axis=0)
Z = (X - mu) / sd
def sigmoid(t): return 1 / (1 + np.exp(-t))
def fit(Z, y, lr=0.2, steps=400, l2=0.0, log=None):
    w = np.zeros(Z.shape[1]); b = 0.0
    for i in range(steps):
        p = sigmoid(Z @ w + b); g = p - y
        if log is not None and i in log:
            loss = -np.mean(y * np.log(p + 1e-12) + (1 - y) * np.log(1 - p + 1e-12))
            print(f"step {i:3d}  loss {loss:.4f}")
        w -= lr * (Z.T @ g / len(y) + l2 * w); b -= lr * g.mean()
    return w, b
def auc(score, label):
    order = np.argsort(score)
    ranks = np.empty(len(score)); ranks[order] = np.arange(1, len(score) + 1)
    pos = label == 1
    return (ranks[pos].sum() - pos.sum() * (pos.sum() + 1) / 2) / (pos.sum() * (~pos).sum())
k = 5
rk = np.random.default_rng(3)
fold = np.empty(n, dtype=int)
for cls in (0, 1):
    idx = rk.permutation(np.where(y == cls)[0]); fold[idx] = np.arange(len(idx)) % k
oof = np.zeros(n); aucs = []
for f in range(k):
    trn, tst = fold != f, fold == f
    m_, s_ = X[trn].mean(axis=0), X[trn].std(axis=0)
    w_, b_ = fit((X[trn] - m_) / s_, y[trn])
    oof[tst] = sigmoid(((X[tst] - m_) / s_) @ w_ + b_)
    aucs.append(auc(oof[tst], y[tst]))
print("5-fold AUC per fold:", np.round(aucs, 3), " mean", round(float(np.mean(aucs)), 3), " sd", round(float(np.std(aucs)), 3))
t = 0.25
flag = oof >= t
print(f"all 600 out-of-fold at t={t}: flagged {flag.sum()}, precision {y[flag].mean():.2f}, recall {flag[y == 1].mean():.2f}")
print("group           n  fail%  flagged%  recall  false-alarm%")
for nm, g in (("valley", valley), ("outside valley", ~valley)):
    fl = flag[g]; yy = y[g]
    print(f"{nm:14s} {g.sum():3d}  {yy.mean():5.1%}  {fl.mean():7.1%}  {fl[yy == 1].mean():6.2f}  {fl[yy == 0].mean():11.1%}")
rb = np.random.default_rng(9)
gaps = []
for _ in range(1000):
    i = rb.integers(0, n, n); g, fl, yy = valley[i], flag[i], y[i]
    gaps.append(fl[g & (yy == 1)].mean() - fl[~g & (yy == 1)].mean())
obs = flag[valley & (y == 1)].mean() - flag[~valley & (y == 1)].mean()
lo, hi = np.percentile(gaps, [2.5, 97.5])
print(f"recall gap (valley - outside) {obs:+.3f}, 95% bootstrap interval [{lo:+.3f}, {hi:+.3f}]")
```
```output
5-fold AUC per fold: [0.85  0.837 0.819 0.831 0.814]  mean 0.83  sd 0.013
all 600 out-of-fold at t=0.25: flagged 212, precision 0.47, recall 0.72
group           n  fail%  flagged%  recall  false-alarm%
valley         362  22.7%    34.8%    0.71        24.3%
outside valley 238  23.5%    36.1%    0.75        24.2%
recall gap (valley - outside) -0.043, 95% bootstrap interval [-0.196, +0.116]
```

*Reading the output.* The five fold AUCs run from 0.814 to 0.850 with mean **0.830** and standard deviation 0.013, so the model's ranking quality is stable and the single-split AUC (0.791) was a little unlucky. At threshold 0.25 the model flags 212 of the 600 students with precision 0.47 and recall 0.72; a lower threshold raises recall at the cost of more flags. For the two groups, the failing rates are almost equal (22.7 and 23.5 percent), the flagged shares are 34.8 and 36.1 percent, recall is 0.71 and 0.75, and false alarms are 24.3 and 24.2 percent. The recall gap is **−0.043 with a 95 percent bootstrap interval of −0.196 to +0.116**. Because the interval comfortably includes zero, the data show **no evidence of a gap**, but it is also too wide to prove there is none.

An honest fairness paragraph says four things: which groups were checked, which measures were compared, what the numbers were, and what was **not** checked (gender, caste or ethnicity, disability, language, and any group too small to count). It also says that the simulated data cannot reveal biases that real records would contain, for example if teachers in one campus mark attendance more strictly.

## 3.5 Eight ways a model can mislead, and the cure

1. **Reporting accuracy only.** With 23 percent failures, doing nothing scores 76.9 percent on the test set. Always show the baseline, confusion matrix, precision and recall. Choose the metric that matches the cost of the error.
2. **Tuning on the test set.** Choosing the threshold, features or learning rate by looking at test scores turns the test set into a second validation set. Tune on validation or inside cross-validation, then report the test once.
3. **One lucky split.** With only 28 failures in the test set, the score can swing by several points. Use cross-validation, report the mean and spread, and say how many positives each score rests on.
4. **Reading weights as causes.** The positive weight on assignment shows how correlated features share the work. Describe weights as associations inside this model only, and never as advice to students.
5. **Ignoring calibration of the threshold.** A threshold of 0.5 is only a default. The right value depends on how many students teachers can meet. State the capacity and show the precision and recall at that cut.
6. **Over-fitting.** A big gap between training AUC (0.876) and validation AUC (0.743) means the model memorised noise. Use fewer features, add L2 regularisation (the `l2` option in the fit function) or collect more data.
7. **Ignoring groups.** A model with good overall recall can be much worse for a smaller group. Compute recall and false alarms per group, add a bootstrap interval, and be open about groups you could not check.
8. **Treating the output as a verdict.** A risk score is a reason to talk to a student, not a label to store or a reason to penalise. Keep a human in the loop, let students see and challenge what is recorded, and review the model every term.

```photogrid label="3.1" cols="2" ratio="1.1" caption="The logistic curve and the cost of a threshold. (a) Pierre-Francois Verhulst (1804-1849), who introduced the logistic curve in 1845 to describe a population that grows and then levels off. (b) Logistic regression turns any score z into a probability 1 / (1 + e^-z): -4 gives 0.018, -2 gives 0.119, 0 gives 0.500, 2 gives 0.881 and 4 gives 0.982. A simulated test set of 400 cases with 76 true positives (seeded random numbers, not real data) was then scored and cut at three thresholds. At 0.3 the model catches 75 of 76 positives (recall 0.987) but raises 160 false alarms (precision 0.319); at 0.5 it finds 66 with 29 false alarms (precision 0.695, recall 0.868); at 0.7 it raises only 2 false alarms (precision 0.935) but misses 47 (recall 0.382). The threshold is a business choice: a screening test wants high recall, an automatic loan rejection wants high precision."
@ photo id="bcapj/verhulst" cap="Pierre-Francois Verhulst (1804-1849)"
fit 1.1
focus 0.5 0.3
@ svg cap="Sigmoid, and precision/recall at three thresholds"
import numpy as np, math
sg = lambda z: 1 / (1 + math.exp(-z))
assert [round(sg(z), 4) for z in (-4, -2, 0, 2, 4)] == [0.018, 0.1192, 0.5, 0.8808, 0.982]
rng = np.random.default_rng(2081); n = 400
y = (rng.random(n) < 0.2).astype(int); s = np.clip(rng.normal(0.30 + 0.35 * y, 0.16), 0.01, 0.99)
rows = []
for th in (0.3, 0.5, 0.7):
    p = s >= th; tp = int((p & (y == 1)).sum()); fp = int((p & (y == 0)).sum()); fn = int((~p & (y == 1)).sum())
    rows.append((th, tp, fp, fn, tp / (tp + fp), tp / (tp + fn)))
assert [(r[1], r[2], r[3]) for r in rows] == [(75, 160, 1), (66, 29, 10), (29, 2, 47)] and int(y.sum()) == 76
assert [round(r[4], 3) for r in rows] == [0.319, 0.695, 0.935] and [round(r[5], 3) for r in rows] == [0.987, 0.868, 0.382]
f = Fig(300, 240)
f.text(150, 12, "p = 1 / (1 + e^-z)", size=10.5, color=NAVY, bold=True)
X = lambda z: 30 + (z + 6) / 12 * 250; Y = lambda p: 100 - p * 70
f.line(30, Y(0), 280, Y(0), color=SLATE, sw=1); f.line(30, Y(1), 280, Y(1), color="#e2e8f0", sw=1)
f.line(X(0), Y(0), X(0), Y(1), color="#e2e8f0", sw=1)
zs = [-6 + i * 0.3 for i in range(41)]
for a, b in zip(zs, zs[1:]): f.line(X(a), Y(sg(a)), X(b), Y(sg(b)), color="#1d6fb8", sw=2.2)
for z in (-4, -2, 0, 2, 4): f.circle(X(z), Y(sg(z)), 3, fill=RED, stroke=RED, sw=1)
f.text(22, Y(1), "1", size=10.5, color=SLATE, anchor="end", vmid=True); f.text(22, Y(0), "0", size=10.5, color=SLATE, anchor="end", vmid=True)
f.text(150, 118, "z (score)", size=10.5, color=SLATE)
for j, h in ((52, "cut"), (110, "TP/FP/FN"), (196, "prec."), (250, "recall")): f.text(j, 138, h, size=10.5, color=NAVY, bold=True)
for i, (th, tp, fp, fn, pr, rc) in enumerate(rows):
    yy = 160 + i * 22
    f.text(52, yy, f"{th}", size=10.5, color=NAVY, bold=True)
    f.text(110, yy, f"{tp}/{fp}/{fn}", size=10.5, color=SLATE)
    f.text(196, yy, f"{pr:.3f}", size=10.5, color="#0f766e" if pr > .9 else NAVY, bold=True)
    f.text(250, yy, f"{rc:.3f}", size=10.5, color="#0f766e" if rc > .9 else "#b91c1c" if rc < .5 else NAVY, bold=True)
f.text(150, 232, "76 true positives in 400 cases (simulated)", size=10.5, color=SLATE)
```

## Formula and fact sheet

| Item | Formula or fact |
|---|---|
| Sigmoid | p = 1 ÷ (1 + e^(−z)) |
| Score | z = b + w₁x₁ + … + wₖxₖ |
| Log loss | −mean[y ln p + (1 − y) ln(1 − p)]; starts at ln 2 = 0.693 for p = 0.5 |
| Gradient step | w ← w − lr × (Zᵀ(p − y) ÷ m); b ← b − lr × mean(p − y) |
| Precision, recall | TP ÷ (TP + FP); TP ÷ (TP + FN) |
| F1 | 2PR ÷ (P + R) |
| k-fold CV | train on k − 1 folds, test on the other, repeat k times |
| Bootstrap | resample with replacement many times to get an interval |

## Chapter summary

- Logistic regression turns a weighted score into a **probability** with the sigmoid; gradient descent learns the weights by reducing log loss.
- Read the loss curve and **both** training and validation scores; a large gap signals over-fitting.
- Weights of correlated features are **associations, not causes**.
- Tune the **threshold** on validation, then report the test set **once** with the confusion matrix, precision, recall, F1, AUC and precision at the top, next to the baselines.
- Use **cross-validation** for a steadier estimate and a **bootstrap interval** to judge group gaps.
- A fairness paragraph states the groups checked, the numbers and, just as important, what was not checked.

## Practice

1. Write the sigmoid function and say what it does to a score of 0.
2. Why does the training log start at a loss of 0.6931?
3. What does it mean when the loss curve flattens?
4. In Section 3.2 the training AUC is 0.876 and the validation AUC is 0.743. What does the gap suggest and how can it be reduced?
5. Why is the positive weight on assignment not evidence that assignments cause failure?
6. Explain why raising the threshold increases precision but lowers recall.
7. From TP = 15, FP = 11, FN = 13, TN = 82, compute accuracy, precision, recall and F1.
8. The model scores 80.2 percent accuracy and the do-nothing baseline 76.9 percent. Why is the 3.3-point gap a weak argument on its own?
9. Describe how 5-fold stratified cross-validation works and why it is steadier than one split.
10. The recall gap between two groups is −0.043 with a bootstrap interval of −0.196 to +0.116. What can and cannot be concluded?

::: note Answers and worked solutions
**1.** p = 1 ÷ (1 + e^(−z)). For z = 0 it gives p = 0.5, the point of complete uncertainty.
**2.** With all weights zero the model says p = 0.5 for everyone and the loss is −ln 0.5 = 0.6931.
**3.** The weights have converged; further steps give almost no improvement.
**4.** The model fits the training data better than new data, a mild over-fit; use fewer features, L2 regularisation or more data. The small validation set (28 failures) also adds noise.
**5.** Assignment is correlated with internal marks and attendance, so its small leftover weight is not a separate cause.
**6.** A higher threshold flags only students with very high scores, who are more often really failing (precision up), but many failing students with medium scores are not flagged (recall down).
**7.** Accuracy (15 + 82) ÷ 121 = 0.802; precision 15 ÷ 26 = 0.577; recall 15 ÷ 28 = 0.536; F1 = 2 × 0.577 × 0.536 ÷ (0.577 + 0.536) = 0.556.
**8.** Accuracy rewards the large passing class; the baseline already gets 76.9 percent with recall 0, so the right evidence is precision and recall, where the model reaches 0.58 and 0.54.
**9.** Cut the data into five stratified folds, train on four and score on the fifth, rotate five times, then average. Every student is scored by a model that never saw them, so the average rests on all 600 students.
**10.** The data show no evidence of a recall gap, since the interval includes zero. They cannot prove the groups are treated equally: the interval allows a gap of about 12 to 20 points either way.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain how logistic regression classifies an example and how its weights are learned. Use the early-warning example.**

*Introduction.* Logistic regression is a simple, widely used classifier that outputs the probability that an example belongs to class 1. In SikshyaSignal class 1 means "will fail at least one subject".

*How it classifies.*

1. Each student's features (attendance, internal marks, assignment rate, previous GPA, commute) are scaled to z-scores.
2. The model computes a score z = b + w₁x₁ + … + w₅x₅, where the weights show how strongly each feature pushes the score up or down.
3. The sigmoid p = 1 ÷ (1 + e^(−z)) converts the score into a probability between 0 and 1.
4. A threshold, chosen on the validation set (0.40 here), turns the probability into a flag.

*How the weights are learned.* Start with all weights at zero (loss 0.6931). Repeat 400 times: predict p for every training student, find the error p − y, and move each weight a small step in the direction that lowers the log loss. The loss fell from 0.6931 to 0.3399 and flattened, so training had converged (Figure 3.2).

*Example.* Internal marks received the largest negative weight (−1.191), so a student with low internal marks gets a high score and a high risk.

*Conclusion.* The model is easy to explain, quick to train and gives probabilities that can be ranked, which suits a teacher who wants a list of whom to meet first.

**Q2 (5 marks). Define the confusion matrix, precision, recall and F1. Compute them for the SikshyaSignal test result and explain which matters more.**

*Introduction.* Accuracy hides the difference between the two kinds of error, so a classifier is reported with a confusion matrix and the measures derived from it.

*Definitions.*

| Term | Meaning | SikshyaSignal test value |
|---|---|---|
| TP | failing student flagged | 15 |
| FP | passing student flagged (false alarm) | 11 |
| FN | failing student missed | 13 |
| TN | passing student not flagged | 82 |
| Precision | TP ÷ (TP + FP) | 15 ÷ 26 = 0.58 |
| Recall | TP ÷ (TP + FN) | 15 ÷ 28 = 0.54 |
| F1 | 2PR ÷ (P + R) | 0.56 |

*Which matters more.* Missing a failing student (FN) costs the student a chance of help, so **recall** is usually weighted heavily. But teachers can meet only a limited number of students, so too many false alarms (low **precision**) waste the scarce resource and make teachers ignore the list. The balance is set by choosing the threshold, and by looking at precision in the top ranks (here 0.83 for the top 12).

*Comparison.* The attendance rule scored precision 0.43 and recall 0.46, so the model is better on both, and the do-nothing baseline has recall 0.

*Conclusion.* A report that shows the matrix, both measures and the baselines lets the examiner judge the model without trusting a single number.

**Q3 (10 marks). Describe how a classification model should be evaluated honestly in a final-year project. Cover baselines, splitting, threshold choice, metrics, cross-validation and fairness, using the early-warning example.**

*Introduction.* Building a model is easy; showing that it works is hard. An honest evaluation protects both the student and the people the model will affect. SikshyaSignal's evaluation follows seven steps.

*1. Baselines first.* Compute the do-nothing baseline (76.9 percent accuracy, recall 0) and a simple rule (attendance below 70: precision 0.43, recall 0.46). The model must beat these on the measures that matter.

*2. A clean split.* Use a stratified 60/20/20 split with a fixed seed; fit scaling on the training rows only. The test set stays locked.

*3. Threshold on validation.* Sweep thresholds on the validation set and choose t = 0.40 for the best F1. Explain that this is a policy decision linked to teacher capacity.

*4. One look at the test set.* Report TP 15, FP 11, FN 13, TN 82; accuracy 0.802, precision 0.58, recall 0.54, F1 0.56, AUC 0.791 and precision of 0.83 in the top 12.

*5. Check stability.* Five-fold cross-validation gave AUCs from 0.814 to 0.850 (mean 0.830, sd 0.013), so the ranking is stable. Also report the training–validation gap (0.876 against 0.743) as a sign of mild over-fitting.

*6. Fairness check.* Compare the two campus groups with out-of-fold predictions: recall 0.71 against 0.75 and false alarms 24.3 against 24.2 percent. The recall gap of −0.043 has a 95 percent bootstrap interval of −0.196 to +0.116, so no gap is shown but none is ruled out. State the groups not checked.

*7. Limits and human review.* Say that the data is simulated, that weights are associations and not causes, and that the output is advice to a teacher, never a punishment.

| Step | Evidence in the report |
|---|---|
| Baselines | accuracy, precision, recall of do-nothing and rule |
| Split | rows and failing rate per part |
| Threshold | validation sweep table |
| Test result | confusion matrix and measures, once |
| Stability | fold AUCs, train–validation gap |
| Fairness | group table with interval |

*Conclusion.* An evaluation chapter that follows these steps may show only a modest improvement, but it will be believed. Honest modest results with clear limits are rated above inflated numbers that cannot survive a single question from the panel.
