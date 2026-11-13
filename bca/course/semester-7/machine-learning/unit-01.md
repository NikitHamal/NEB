---
subject: Machine Learning
grade: BCA Semester 7 (Elective I)
unit: 1
title: Introduction to Machine Learning and the Theory of Learning
hours: 10
area: BCA 405 · Machine Learning · Unit 1
---

A bank in Pokhara wants to decide, from a loan form, which applicants will repay. Writing rules by hand ("income above this, age below that") fails within a month because customers change and the rules interact in ways no officer can list. **Machine learning (ML)** takes the opposite route: show a program thousands of past forms with their outcomes and let it *find the rule itself*. This unit explains what that means, what the program can and cannot promise, and the vocabulary used in every later unit.

::: key What this unit gives you
- A short history of ML and the brain-neuron analogy that inspired neural networks.
- Tom Mitchell's definition of learning, the types of learning and the need for ML.
- The data and tools you will use, a statistics review, and the training, validation and test split.
- The theory of learning: feasibility, error and noise, training versus testing, the generalization bound, the approximation-generalization trade-off, bias and variance, and learning curves.
:::

## 1.1 History of machine learning

| Year | Event |
|---|---|
| 1943 | McCulloch and Pitts model a neuron as a threshold switch |
| 1950 | Alan Turing asks "Can machines think?" and proposes the imitation game |
| 1952 | Arthur Samuel writes a checkers program that improves by playing itself; he later coins the phrase "machine learning" (1959) |
| 1957 | Frank Rosenblatt builds the perceptron |
| 1969 | Minsky and Papert show a single perceptron cannot learn XOR; neural-network funding falls (the first "AI winter") |
| 1986 | Rumelhart, Hinton and Williams popularise back-propagation for multi-layer networks |
| 1995 | Cortes and Vapnik publish the support vector machine; Quinlan's decision trees (ID3 1986, C4.5 1993) are in wide use |
| 1997 | IBM Deep Blue beats the chess champion; Mitchell publishes the textbook used by this course |
| 2012 | A deep convolutional network wins the ImageNet contest by a large margin; deep learning takes off |
| 2017 onwards | Transformers lead to large language models |

The pattern is a cycle: an idea is promising, limited by data or computing power, set aside and then revived when both grow. Today's boom rests on three things that the 1960s lacked: huge labelled data sets, cheap parallel hardware (GPUs) and better training methods.

## 1.2 The brain-neuron learning system

A human brain has about 86 billion **neurons**. Each neuron receives electrical signals through its **dendrites**, adds them up in the cell body, and if the total crosses a threshold it fires a signal along its **axon** to other neurons through junctions called **synapses**. Learning changes the *strength* of synapses: connections used together get stronger (Hebb's rule, "cells that fire together wire together").

An artificial neuron copies this in four steps: multiply each input $x_i$ by a weight $w_i$ (synapse strength), add a bias $b$, sum, and pass the sum through an activation function (the firing rule). *Learning* means adjusting the weights from examples. The analogy is loose: real neurons are far more complex, but the idea of many simple units whose connection strengths are learned is the root of neural networks (Unit 2).

```svgfig label="1.1" caption="A biological neuron and its artificial counterpart. Dendrites correspond to the inputs, synaptic strengths to the weights, the cell body to the weighted sum and threshold, and the axon to the output."
f = Fig(580, 210)
f.text(145, 18, "Biological neuron", size=11, color=TEAL, bold=True)
f.circle(145, 105, 34, fill=MINT, stroke=TEAL, label="cell body\nsum + fire", size=9)
for i, y in enumerate((50, 105, 160)):
    f.arrow([(30, y), (111, 105)], color=TEAL)
f.text(36, 40, "dendrites", size=9.5, color=TEAL)
f.arrow([(179, 105), (270, 105)], color=TEAL)
f.text(226, 94, "axon", size=9.5, color=TEAL)
f.text(430, 18, "Artificial neuron", size=11, color=NAVY, bold=True)
for i, (y, t) in enumerate(((45, "x1"), (105, "x2"), (165, "x3"))):
    f.circle(330, y, 15, fill=BLUE, stroke=NAVY, label=t, size=10)
    f.arrow([(345, y), (404, 105)], color=NAVY, label="w%d" % (i + 1), lpos=(372, (y + 105) / 2 - 4 + (6 if y > 105 else 0)))
f.circle(430, 105, 28, fill=BLUE, stroke=NAVY, label="Σ + b", size=11)
f.box(470, 90, 50, 30, "f(z)", fill=ROSE, stroke=RED, size=11, bold=True)
f.arrow([(520, 105), (565, 105)], color=NAVY)
f.text(552, 94, "y", size=11, color=NAVY, bold=True)
```

## 1.3 Definition and types of learning

**Mitchell's definition (1997).** *A computer program is said to learn from experience E with respect to some class of tasks T and performance measure P, if its performance at tasks in T, as measured by P, improves with experience E.*

::: example Spam filter
T = classify an e-mail as spam or not spam. E = a collection of e-mails already labelled by users. P = the percentage of new e-mails classified correctly. If P rises as E grows, the filter is learning.
:::

| Type | Data given | Goal | Examples |
|---|---|---|---|
| **Supervised** | Inputs *with* correct outputs (labels) | Predict the label of new inputs. *Classification*: label is a category; *regression*: label is a number | Spam detection, house-price prediction |
| **Unsupervised** | Inputs only | Find structure: groups, patterns, compact descriptions | Customer segments, topic discovery, compression |
| **Semi-supervised** | A few labelled and many unlabelled inputs | Use the unlabelled data to do better than labels alone | Medical images where labelling is costly |
| **Reinforcement** | An agent acts and receives rewards | Learn a policy that maximises long-run reward | Game playing, robot control |

## 1.4 The need for machine learning

1. **Rules are too hard to write.** Nobody can list the rules that tell a handwritten 7 from a 1.
2. **The world changes.** A model retrained on new data adapts; a hand-written rule set needs an engineer.
3. **Scale and speed.** Millions of decisions a day (fraud checks on every mobile-wallet transaction) cannot be made by people.
4. **Personalisation.** A different recommendation for each user is impossible by hand.
5. **Discovery.** ML can find patterns humans did not suspect, for example in medical records.

ML is *not* the right tool when there is little data, when a simple rule is known and exact (a tax formula), or when every decision must be explained in full legal detail and no interpretable model is accurate enough.

## 1.5 Data and tools

**Data.** A data set is a table. Each row is an **example** (instance, sample); each column is a **feature** (attribute); for supervised learning one extra column is the **label** (target). Features can be numeric (age), categorical (district) or ordinal (grade A, B, C). Quality matters more than quantity: missing values, wrong labels, duplicated rows and *sampling bias* (data from one city only) all damage the result. The rule is **garbage in, garbage out**.

**Tools.** The practical stack for this course is free:

| Tool | Use |
|---|---|
| Python 3 | The language; readable and the ML standard |
| NumPy | Arrays and linear algebra (every program in this book uses it) |
| pandas | Loading and cleaning tables |
| matplotlib | Plots |
| scikit-learn | Ready-made algorithms for classification, regression, clustering, PCA and evaluation |
| Jupyter or Google Colab | Notebooks that mix code, results and notes; Colab needs only a browser |
| MATLAB / Octave | Alternative named in the TU syllabus laboratory work |

## 1.6 Review of statistics

For a sample $x_1, \dots, x_n$:

$$\bar{x} = \frac{1}{n}\sum_{i=1}^{n} x_i, \qquad s^{2} = \frac{1}{n-1}\sum_{i=1}^{n}(x_i - \bar{x})^{2}, \qquad s = \sqrt{s^{2}}.$$

- **Mean, median, mode** describe the centre; the median resists outliers.
- **Variance and standard deviation** describe spread. Using $n-1$ (Bessel's correction) makes the sample variance an unbiased estimate of the population variance.
- **Covariance and correlation** measure how two features move together: $\operatorname{cov}(x,y)=\frac{1}{n-1}\sum (x_i-\bar x)(y_i-\bar y)$ and $r = \operatorname{cov}(x,y)/(s_x s_y)$, with $-1 \le r \le 1$. Correlation is not causation.
- **Normal distribution.** About 68 percent of values lie within one standard deviation of the mean, 95 percent within two and 99.7 percent within three.
- **Standardisation (z-score)** $z=(x-\bar x)/s$ puts features on a common scale, which distance-based methods (Units 3 and 4) need.

## 1.7 Training, validation and test data

A model that is judged on the same data it learned from will look perfect even if it has only memorised. So the data is split:

| Set | Typical share | Purpose |
|---|---|---|
| **Training** | 60 to 70 percent | Fit the model's parameters |
| **Validation** | 15 to 20 percent | Compare models and tune hyper-parameters (tree depth, k in k-NN) |
| **Test** | 15 to 20 percent | Report final performance, used *once* at the end |

::: caution
If you keep adjusting the model until the test score looks good, the test set has become a second validation set and its score is optimistic (*data leakage*). When data is scarce, use **k-fold cross-validation**: split into k parts, train on k − 1 and validate on the remaining one, rotate, and average the k scores (Unit 5).
:::

## 1.8 Theory of learning

### Feasibility of learning
How can a program say anything about *unseen* data from a finite sample? The unknown target could do anything outside the sample. The answer is **probability**. If the examples are drawn independently from the same distribution that future data comes from, then the fraction of errors on a sample is close to the true error rate with high probability. **Hoeffding's inequality**: for a sample of $N$ independent examples, the sample error rate $E_{in}$ and the true error rate $E_{out}$ of one fixed hypothesis satisfy

$$P\left(|E_{in} - E_{out}| > \epsilon\right) \le 2 e^{-2\epsilon^{2} N}.$$

Learning is therefore *feasible*: the bound shrinks exponentially as $N$ grows. Note it covers one hypothesis chosen *before* seeing the data.

```python
import math
for N in (100, 500, 1000, 5000):
    print(N, "examples -> P(|Ein-Eout| > 0.05) <=", round(min(1, 2 * math.exp(-2 * 0.05**2 * N)), 4))
```
```output
100 examples -> P(|Ein-Eout| > 0.05) <= 1
500 examples -> P(|Ein-Eout| > 0.05) <= 0.1642
1000 examples -> P(|Ein-Eout| > 0.05) <= 0.0135
5000 examples -> P(|Ein-Eout| > 0.05) <= 0.0
```
### Error and noise
**Error** is a measure of how far a prediction is from the truth: for classification the *0-1 error* (wrong or right), for regression the *squared error* $(h(x)-y)^2$. **Noise** is the part of $y$ that no function of $x$ can predict: measurement errors, mislabels and hidden factors. With noise, the target is a *distribution* $P(y\mid x)$, not a function, and even the best model has some error. Do not chase noise: a model that reaches zero training error on noisy data has fitted the noise.

### Training versus testing, and the generalization bound
When the learner *chooses* the best of $M$ hypotheses, Hoeffding gets multiplied by $M$ (the union bound). For infinite hypothesis sets such as all lines, $M$ is replaced by a **growth function** $m_H(N)$, the number of different labellings the set can produce on $N$ points. The largest $N$ it can produce *all* $2^N$ labellings on is the **VC dimension** $d_{VC}$; lines in the plane have $d_{VC}=3$. The result is the **VC generalization bound**: with probability at least $1-\delta$,

$$E_{out} \le E_{in} + \sqrt{\frac{8}{N}\ln\frac{4\, m_H(2N)}{\delta}}, \qquad m_H(N) \le N^{d_{VC}} + 1.$$

Read it plainly: *test error ≤ training error + a penalty for model complexity*. The penalty rises with $d_{VC}$ and falls with $N$. A rough rule is to have at least $10\,d_{VC}$ examples.

### Approximation-generalization trade-off
A **richer** hypothesis set (higher degree polynomial, deeper tree) can approximate the target better, so $E_{in}$ falls, but the complexity penalty rises, so $E_{in}$ becomes a worse guide to $E_{out}$. A **simpler** set generalises reliably but may be unable to approximate the target. Learning is the search for the best compromise, as in the figure below.

### Bias and variance
For a fixed model class, imagine training it on many different data sets of the same size. The expected squared error at a point splits into three parts:

$$\mathbb{E}\big[(\hat f(x) - y)^2\big] = \underbrace{\big(\mathbb{E}[\hat f(x)] - f(x)\big)^2}_{\text{bias}^2} + \underbrace{\mathbb{E}\big[(\hat f(x) - \mathbb{E}[\hat f(x)])^2\big]}_{\text{variance}} + \underbrace{\sigma^{2}}_{\text{noise}}.$$

**Bias** is the error from a model too simple to capture the target (*under-fitting*). **Variance** is how much the fitted model changes with the training sample (*over-fitting*). The program fits polynomials of degree 1, 3 and 5 to many noisy samples of $\sin(\pi x)$ and measures both.

```python
import numpy as np
rng = np.random.default_rng(7)
xs = np.linspace(-0.9, 0.9, 200)
truth = np.sin(np.pi * xs)
print("degree  bias^2  variance")
for deg in (1, 3, 5):
    preds = []
    for _ in range(300):
        x = rng.uniform(-1, 1, 15)
        y = np.sin(np.pi * x) + rng.normal(0, 0.3, 15)
        preds.append(np.polyval(np.polyfit(x, y, deg), xs))
    preds = np.array(preds)
    bias2 = np.mean((preds.mean(axis=0) - truth) ** 2)
    var = np.mean(preds.var(axis=0))
    print(f"{deg:>6}  {bias2:6.3f}  {var:8.3f}")
```
```output
degree  bias^2  variance
     1   0.152     0.047
     3   0.003     0.033
     5   0.004     1.005
```
The straight line has high bias and low variance, the degree-5 curve has tiny bias and large variance, and degree 3 balances the two.

```svgfig label="1.2" caption="Under-fitting and over-fitting. Training error (blue) always falls as the model becomes more complex; validation error (red) falls and then rises. The best model is at the minimum of the validation curve, between high bias on the left and high variance on the right."
f = Fig(580, 240)
ax = Axes(f, 60, 20, 480, 170, (0, 10), (0, 10))
ax.axes("", "")
ax.curve(lambda c: 9 * math.exp(-0.38 * c) + 0.3, 0, 10, color=NAVY, label="training error", lx=7.3, ly=1.6)
ax.curve(lambda c: 9 * math.exp(-0.38 * c) + 0.3 + 0.06 * c ** 2 * 0.9 - 0.4, 0, 10, color=RED, label="validation error", lx=8.2, ly=7.8)
ax.vline(5.0, color=TEAL)
f.text(150, 205, "under-fitting\nhigh bias", size=10, color=SLATE)
f.text(300, 205, "best\ncomplexity", size=10, color=TEAL, bold=True)
f.text(470, 205, "over-fitting\nhigh variance", size=10, color=SLATE)
f.text(300, 235, "model complexity (degree, tree depth, number of neurons)", size=10, color=SLATE)
f.text(18, 105, "error", size=10, color=SLATE)
```

### Learning curves
A **learning curve** plots training and validation error against the *number of training examples*. With few examples the training error is low (easy to memorise) and the validation error high. As $N$ grows the two converge. If they converge to a **high** error, the model is biased: more data will not help, a richer model will. If a **large gap** remains, the model has high variance: more data, regularisation or a simpler model will help.

```python
import numpy as np
rng = np.random.default_rng(3)
def sample(n):
    x = rng.uniform(-1, 1, n)
    return x, np.sin(np.pi * x) + rng.normal(0, 0.3, n)
xv, yv = sample(2000)
print("  N   train-MSE  val-MSE   (degree 3)   |  train-MSE  val-MSE   (degree 5)")
for n in (15, 25, 50, 100, 400):
    row = []
    for deg in (3, 5):
        tr, va = [], []
        for _ in range(50):
            x, y = sample(n)
            c = np.polyfit(x, y, deg)
            tr.append(np.mean((np.polyval(c, x) - y) ** 2))
            va.append(np.mean((np.polyval(c, xv) - yv) ** 2))
        row += [np.mean(tr), np.mean(va)]
    print(f"{n:>4}   {row[0]:8.3f} {row[1]:8.3f}              |  {row[2]:8.3f} {row[3]:8.3f}")
```
```output
  N   train-MSE  val-MSE   (degree 3)   |  train-MSE  val-MSE   (degree 5)
  15      0.071    0.166              |     0.057    0.595
  25      0.075    0.117              |     0.069    0.315
  50      0.082    0.108              |     0.077    0.118
 100      0.091    0.103              |     0.084    0.099
 400      0.094    0.100              |     0.088    0.094
```
## 1.9 Regularisation and splitting data in practice

**Regularisation** fights over-fitting by penalising large weights. **Ridge regression** minimises $\sum (\hat y_i-y_i)^2+\lambda\sum w_j^{2}$: the larger $\lambda$ is, the smaller the weights and the smoother the model (more bias, less variance). **Lasso** uses $\lambda\sum|w_j|$, which drives some weights exactly to zero and so selects features. $\lambda$ is a **hyper-parameter**: it is chosen on the validation set, never on the training set. The program fits a degree-9 polynomial to 12 noisy points with several values of $\lambda$ and scores each on fresh data.

```python
import numpy as np
rng = np.random.default_rng(11)
def make(n):
    x = rng.uniform(-1, 1, n); return x, np.sin(np.pi * x) + rng.normal(0, 0.25, n)
xt, yt = make(12); xv, yv = make(400)
def feats(x): return np.vander(x, 10, increasing=True)
print("lambda      train-MSE  validation-MSE")
for lam in (0, 1e-6, 1e-3, 1e-1, 1, 10):
    A = feats(xt)
    w = np.linalg.solve(A.T @ A + lam * np.eye(10), A.T @ yt)
    print("%-10g  %8.3f  %12.3f" % (lam, np.mean((A @ w - yt) ** 2), np.mean((feats(xv) @ w - yv) ** 2)))
```
```output
lambda      train-MSE  validation-MSE
0              0.001        10.177
1e-06          0.003         0.485
0.001          0.005         0.106
0.1            0.019         0.180
1              0.057         0.333
10             0.107         0.465
```
With $\lambda=0$ the training error is almost zero but the validation error is high (over-fitting); a moderate $\lambda$ trades a little training error for a much better validation error; a very large $\lambda$ flattens the curve and the model under-fits. The same principle appears as **tree depth limits**, **early stopping** in networks and **the C parameter** of the SVM.

**Splitting in code.** Shuffle before splitting (data files are often sorted by class or date), fix the random seed so the experiment can be repeated, and keep the proportions of the classes (stratify). For time-ordered data split by time, training on the past and testing on the future, because a random split would let the model "see" the future.

```python
import numpy as np
rng = np.random.default_rng(0)
y = np.array([0] * 90 + [1] * 10)
idx = rng.permutation(len(y)); tr, va, te = idx[:60], idx[60:80], idx[80:]
print("sizes:", len(tr), len(va), len(te), "| positives in each part:", y[tr].sum(), y[va].sum(), y[te].sum())
```
```output
sizes: 60 20 20 | positives in each part: 5 4 1
```
## 1.10 Summary and exercises

ML is Mitchell's (T, P, E) definition made practical: supervised, unsupervised, semi-supervised and reinforcement learning. Data is split into training, validation and test sets. Learning is feasible because of Hoeffding-type bounds; the VC bound says test error is at most training error plus a complexity penalty; the error decomposes into bias, variance and noise; and learning curves diagnose which of the two to fix.

1. State Mitchell's definition and apply it to a face-unlock feature (identify T, P and E).
2. Differentiate supervised, unsupervised and reinforcement learning with one Nepali example each.
3. Why can a model with zero training error still be a poor model? Name the phenomenon.
4. Use Hoeffding's bound to find how many examples guarantee $|E_{in}-E_{out}| \le 0.05$ with probability at least 95 percent for one fixed hypothesis.
5. What is the VC dimension of a line in the plane and why does it matter?
6. Explain bias and variance, and say which a degree-1 polynomial fitted to a sine wave suffers from.
7. A learning curve shows training and validation errors both stuck at 0.40. Diagnose the problem and suggest two remedies.
8. Why must the test set be used only once?

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Define machine learning and explain its types.**

*Introduction.* Machine learning studies programs that improve at a task from experience. Mitchell: a program learns from experience E with respect to tasks T and measure P if its performance on T, measured by P, improves with E.

| Type | Data | Output |
|---|---|---|
| Supervised | Labelled examples | Classifier or regressor |
| Unsupervised | Unlabelled examples | Clusters or compact representation |
| Semi-supervised | Few labels, many unlabelled | Better model than labels alone |
| Reinforcement | Rewards from interaction | Policy |

*Example.* Predicting loan default from past loans is supervised classification; grouping customers by spending is unsupervised clustering. *Conclusion:* the type is chosen by what data and feedback are available.

**Q2 (5 marks). Hoeffding: find N for a given accuracy.**

*Method.* Set the bound $2e^{-2\epsilon^2 N} \le \delta$ and solve: $N \ge \dfrac{1}{2\epsilon^{2}}\ln\dfrac{2}{\delta}$. For $\epsilon = 0.05$ and $\delta = 0.05$: $N \ge \dfrac{1}{2(0.0025)}\ln 40 = 200 \times 3.689 = 737.8$, so **N = 738**. *Conclusion:* about 740 independent examples suffice for one pre-chosen hypothesis; choosing among many hypotheses needs more.

**Q3 (10 marks). Explain the bias-variance trade-off with the approximation-generalization trade-off and learning curves.**

*Introduction.* Every learner faces two goals: fit the training data (approximate the target) and perform well on new data (generalise). They conflict as model complexity grows.

*Body.* (1) The expected squared error equals bias² + variance + noise. (2) A simple model (degree 1) has high bias and low variance: it misses the shape but is stable across samples; the program in Section 1.8 shows high bias² for degree 1. (3) A complex model (degree 5) has low bias and high variance: it follows each sample's noise. (4) Training error always falls with complexity; validation error is U-shaped, so we pick the minimum (Figure 1.2). (5) The VC bound expresses the same idea: test error ≤ training error + penalty that grows with $d_{VC}$ and shrinks with N. (6) Learning curves diagnose which side we are on: both curves high and close means bias, remedy richer model or better features; a wide gap means variance, remedy more data, regularisation or a simpler model.

*Conclusion.* Choose the model class by validation error, collect more data when variance dominates, and add capacity when bias dominates; noise sets a floor that no model can beat.
