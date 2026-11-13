---
subject: Machine Learning
grade: BCA Semester 7 (Elective I)
unit: 2
title: Supervised Learning: Regression, Perceptron, Neural Networks, Decision Trees and SVM
hours: 11
area: BCA 405 · Machine Learning · Unit 2
---

In supervised learning a teacher supplies the right answer for every training example, and the program must generalise to new ones. This unit builds five learners in increasing power: linear regression, the perceptron, multi-layer neural networks, decision trees and support vector machines. For each we ask the same three questions: what is the model, how is it trained, and when does it fail.

::: key What this unit gives you
- Classification and regression problems, and the shape of a supervised learner.
- Linear regression: the best-fit line by the normal equation and by gradient descent.
- The perceptron, its learning rule and why it cannot learn XOR; multi-layer networks and back-propagation.
- Decision trees: entropy, information gain and the ID3 algorithm worked on the classic tennis data set.
- Support vector machines: the maximum-margin separator and its computation.
:::

## 2.1 Classification problems

A supervised learner receives training pairs $(x_1, y_1), \dots, (x_N, y_N)$ and returns a function $h$ with $h(x) \approx y$. If $y$ is a **category** (spam or not, digit 0 to 9, disease or healthy) the task is **classification**; if $y$ is a **number** (house price, rainfall) it is **regression**. A classifier with two classes is **binary**; with more, **multi-class**. A **decision boundary** is the surface where the predicted class changes. A problem is **linearly separable** if one straight line (plane in more dimensions) puts all examples of one class on one side.

## 2.2 Linear regression: predicting a numerical value

The model is a straight line $\hat y = w_0 + w_1 x$ (or $\hat y = \mathbf{w}^{T}\mathbf{x}$ with several features, a bias term included). The **best-fit line** minimises the **sum of squared errors** (the *least squares* criterion)

$$J(\mathbf{w}) = \frac{1}{2N}\sum_{i=1}^{N}\big(\hat y_i - y_i\big)^{2}.$$

**Closed form.** For one feature, with means $\bar x, \bar y$:

$$w_1 = \frac{\sum (x_i-\bar x)(y_i-\bar y)}{\sum (x_i-\bar x)^{2}}, \qquad w_0 = \bar y - w_1\bar x.$$

For many features the **normal equation** is $\mathbf{w} = (X^{T}X)^{-1}X^{T}\mathbf{y}$.

**Gradient descent.** When $X^TX$ is huge, repeat $\mathbf{w} \leftarrow \mathbf{w} - \alpha\,\nabla J(\mathbf{w})$ where $\alpha$ is the **learning rate**: too small is slow, too large overshoots and diverges. Standardise features first so that the steps are balanced.

::: example Study hours and marks
Hours studied $x$: 1, 2, 3, 4, 5. Marks $y$: 35, 45, 50, 62, 68. Then $\bar x=3$, $\bar y=52$; $\sum(x-\bar x)(y-\bar y) = (-2)(-17)+(-1)(-7)+0+(1)(10)+(2)(16) = 34+7+10+32 = 83$ and $\sum(x-\bar x)^2 = 10$. So $w_1 = 8.3$ and $w_0 = 52 - 24.9 = 27.1$. Predicted marks for 6 hours: $27.1 + 8.3\times 6 = 76.9$.
:::

```python
import numpy as np
x = np.array([1, 2, 3, 4, 5.0]); y = np.array([35, 45, 50, 62, 68.0])
X = np.column_stack([np.ones_like(x), x])
w = np.linalg.solve(X.T @ X, X.T @ y)
print("normal equation  w0 = %.2f  w1 = %.2f" % tuple(w))
xs = (x - x.mean()) / x.std()
a, b = 0.0, 0.0
for _ in range(2000):
    err = a + b * xs - y
    a -= 0.1 * err.mean(); b -= 0.1 * (err * xs).mean()
w1 = b / x.std(); w0 = a - w1 * x.mean()
print("gradient descent w0 = %.2f  w1 = %.2f" % (w0, w1))
print("prediction for 6 hours: %.1f" % (w[0] + w[1] * 6))
print("R^2 = %.3f" % (1 - ((X @ w - y) ** 2).sum() / ((y - y.mean()) ** 2).sum()))
```
```output
normal equation  w0 = 27.10  w1 = 8.30
gradient descent w0 = 27.10  w1 = 8.30
prediction for 6 hours: 76.9
R^2 = 0.987
```
**Assessing the fit.** $R^2 = 1 - SS_{res}/SS_{tot}$ is the fraction of variance explained. Beware **outliers** (one extreme point drags the line), **extrapolation** (the line is only trusted inside the range of the training $x$) and **over-fitting** with many features (add **regularisation** such as ridge, which adds $\lambda\|\mathbf{w}\|^{2}$ to the cost).

## 2.3 The perceptron

Rosenblatt's **perceptron** is the simplest neural unit: a weighted sum followed by a hard threshold.

$$z = \mathbf{w}\cdot\mathbf{x} + b, \qquad \hat y = \begin{cases} 1 & z \ge 0\\ 0 & z < 0.\end{cases}$$

**Learning rule.** Start with small weights. For each example, compute the prediction and update only if it is wrong:

$$\mathbf{w} \leftarrow \mathbf{w} + \eta\,(y - \hat y)\,\mathbf{x}, \qquad b \leftarrow b + \eta\,(y - \hat y).$$

If the output was too low ($y=1,\hat y=0$) the weights move towards $\mathbf{x}$; if too high they move away. **Perceptron convergence theorem:** if the classes are linearly separable, the rule finds a separating line in a finite number of updates.

```python
import numpy as np
def train(X, y, eta=0.1, epochs=50):
    w = np.zeros(X.shape[1]); b = 0.0
    for ep in range(epochs):
        errors = 0
        for xi, yi in zip(X, y):
            pred = 1 if xi @ w + b >= 0 else 0
            if pred != yi:
                w += eta * (yi - pred) * xi; b += eta * (yi - pred); errors += 1
        if errors == 0:
            return w, b, ep + 1
    return w, b, None
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
for name, y in (("AND", [0, 0, 0, 1]), ("OR", [0, 1, 1, 1]), ("XOR", [0, 1, 1, 0])):
    w, b, ep = train(X, np.array(y))
    print(name, "converged in", ep, "epochs, w =", np.round(w, 2), "b =", round(b, 2)) if ep else print(name, "did NOT converge in 50 epochs")
```
```output
AND converged in 4 epochs, w = [0.2 0.1] b = -0.2
OR converged in 4 epochs, w = [0.1 0.1] b = -0.1
XOR did NOT converge in 50 epochs
```
**The XOR limit.** XOR needs the outputs (0,1) and (1,0) to be 1 and (0,0), (1,1) to be 0. No single straight line separates these two pairs, so a single perceptron fails. Minsky and Papert's 1969 proof of this stalled the field. The cure is more layers.

```svgfig label="2.1" caption="Linear separability. AND (left) can be split by one line; XOR (right) cannot, because the two 1s lie on opposite corners. Filled dots are class 1 and hollow dots are class 0."
f = Fig(580, 230)
for k, (name, lab) in enumerate((("AND", (0, 0, 0, 1)), ("XOR", (0, 1, 1, 0)))):
    ax = Axes(f, 40 + k * 290, 30, 200, 160, (-0.4, 1.4), (-0.4, 1.4))
    ax.grid(1, 1)
    ax.axes("x1", "x2")
    for (px, py), l in zip(((0, 0), (0, 1), (1, 0), (1, 1)), lab):
        ax.pt(px, py, "", r=7, color=(NAVY if l else RED), hollow=(l == 0))
    f.text(140 + k * 290, 18, name, size=11, color=NAVY, bold=True)
    if k == 0:
        f.line(ax.X(0.3), ax.Y(1.4), ax.X(1.4), ax.Y(0.3), color=TEAL, sw=2)
        f.text(140, 212, "one line separates the classes", size=10, color=TEAL)
    else:
        f.text(430, 212, "no single line works", size=10, color=RED)
```

## 2.4 Learning neural network structures

A **multi-layer perceptron (MLP)** stacks layers: an **input layer** (one unit per feature), one or more **hidden layers** and an **output layer**. Units in one layer feed all units in the next (*fully connected, feed-forward*). Each unit uses a smooth **activation function** instead of a hard step so that gradients exist:

| Activation | Formula | Range | Use |
|---|---|---|---|
| Sigmoid | $\sigma(z)=1/(1+e^{-z})$ | (0, 1) | Output of binary classifiers |
| Tanh | $\tanh z$ | (−1, 1) | Hidden layers (older) |
| ReLU | $\max(0,z)$ | [0, ∞) | Hidden layers (modern default) |
| Softmax | $e^{z_k}/\sum_j e^{z_j}$ | probabilities summing to 1 | Multi-class output |

A hidden layer lets the network bend the decision boundary. The **universal approximation theorem** says one hidden layer with enough units can approximate any continuous function on a bounded region. For XOR, two hidden units suffice: one learns "x1 OR x2", the other "x1 AND x2", and the output combines them as "OR but not AND".

**Back-propagation** trains the weights in four repeating steps: (1) **forward pass**: compute every layer's output; (2) compute the **loss** (squared error or cross-entropy); (3) **backward pass**: apply the chain rule to find $\partial L/\partial w$ for every weight, working from the output layer back; (4) **update** $w \leftarrow w - \eta\,\partial L/\partial w$. For a sigmoid output unit with squared error, the output-layer error term is $\delta_o = (\hat y - y)\,\hat y(1-\hat y)$, and a hidden unit's term is $\delta_h = \hat h(1-\hat h)\sum_o w_{ho}\delta_o$.

```python
import numpy as np
rng = np.random.default_rng(1)
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], float); y = np.array([[0], [1], [1], [0]], float)
sig = lambda z: 1 / (1 + np.exp(-z))
W1 = rng.normal(0, 1, (2, 3)); b1 = np.zeros(3); W2 = rng.normal(0, 1, (3, 1)); b2 = np.zeros(1)
for epoch in range(8000):
    h = sig(X @ W1 + b1); out = sig(h @ W2 + b2)
    d2 = (out - y) * out * (1 - out)
    d1 = (d2 @ W2.T) * h * (1 - h)
    W2 -= 0.8 * h.T @ d2; b2 -= 0.8 * d2.sum(0)
    W1 -= 0.8 * X.T @ d1; b1 -= 0.8 * d1.sum(0)
    if epoch in (0, 1000, 8000 - 1):
        print("epoch", epoch, "loss", round(float(((out - y) ** 2).mean()), 4))
print("predictions:", np.round(out.ravel(), 2), "-> classes", (out.ravel() > 0.5).astype(int))
```
```output
epoch 0 loss 0.2596
epoch 1000 loss 0.0036
epoch 7999 loss 0.0002
predictions: [0.01 0.99 0.98 0.01] -> classes [0 1 1 0]
```
**Practical points.** Initialise weights randomly (equal weights make all hidden units identical). Too many hidden units over-fit: use **early stopping** (stop when validation loss starts to rise), **weight decay** and **dropout**. Standardise inputs. A network is a black box compared with a tree; explainability is a cost of its power.

## 2.5 Decision tree representation

A **decision tree** classifies by asking a sequence of questions. Each **internal node** tests one attribute, each **branch** is an outcome of the test, each **leaf** gives a class. Any path from the root to a leaf is an **if-then rule**; the tree is the disjunction of all paths that end at "yes". For the tennis problem below, one rule is: *if Outlook = Overcast then PlayTennis = Yes.*

**Appropriate problems for decision tree learning** (Mitchell): (1) instances are described by attribute-value pairs; (2) the target function has discrete output values; (3) disjunctive descriptions may be needed; (4) the training data may contain errors; (5) the training data may have missing attribute values.

## 2.6 The basic decision tree algorithm (ID3)

**ID3** builds the tree top-down and greedily. At each node it picks the attribute that best splits the examples, makes one branch per value, and repeats on each subset until the subset is pure or attributes run out.

**Entropy** measures the impurity of a set $S$ with class proportions $p_i$:

$$H(S) = -\sum_{i} p_i \log_2 p_i.$$

It is 0 for a pure set and 1 for a 50-50 binary set. **Information gain** is the expected reduction in entropy from splitting on attribute $A$:

$$\mathrm{Gain}(S,A) = H(S) - \sum_{v \in \mathrm{Values}(A)} \frac{|S_v|}{|S|}\,H(S_v).$$

::: example Mitchell's PlayTennis data (14 days: 9 Yes, 5 No)
$H(S) = -\tfrac{9}{14}\log_2\tfrac{9}{14} - \tfrac{5}{14}\log_2\tfrac{5}{14} = 0.940$. For Outlook: Sunny has 5 days (2 Yes, 3 No, entropy 0.971), Overcast 4 days (4 Yes, entropy 0), Rain 5 days (3 Yes, 2 No, entropy 0.971). So $\mathrm{Gain}(S,\text{Outlook}) = 0.940 - \tfrac{5}{14}(0.971) - \tfrac{4}{14}(0) - \tfrac{5}{14}(0.971) = 0.247$ (Mitchell rounds the entropies and quotes 0.246). The other gains are Humidity 0.152 (Mitchell quotes 0.151), Wind 0.048 and Temperature 0.029, so **Outlook** becomes the root.
:::

```python
from math import log2
from collections import Counter
D = [("Sunny","Hot","High","Weak","No"),("Sunny","Hot","High","Strong","No"),("Overcast","Hot","High","Weak","Yes"),
     ("Rain","Mild","High","Weak","Yes"),("Rain","Cool","Normal","Weak","Yes"),("Rain","Cool","Normal","Strong","No"),
     ("Overcast","Cool","Normal","Strong","Yes"),("Sunny","Mild","High","Weak","No"),("Sunny","Cool","Normal","Weak","Yes"),
     ("Rain","Mild","Normal","Weak","Yes"),("Sunny","Mild","Normal","Strong","Yes"),("Overcast","Mild","High","Strong","Yes"),
     ("Overcast","Hot","Normal","Weak","Yes"),("Rain","Mild","High","Strong","No")]
names = ["Outlook", "Temperature", "Humidity", "Wind"]
def H(rows):
    c = Counter(r[-1] for r in rows); n = len(rows)
    return -sum(v / n * log2(v / n) for v in c.values())
def gain(rows, a):
    parts = {}
    for r in rows: parts.setdefault(r[a], []).append(r)
    return H(rows) - sum(len(p) / len(rows) * H(p) for p in parts.values())
print("H(S) = %.3f" % H(D))
for i, n in enumerate(names): print("Gain(%s) = %.3f" % (n, gain(D, i)))
def id3(rows, attrs, depth=0):
    labels = {r[-1] for r in rows}
    if len(labels) == 1: print("  " * depth + "-> " + labels.pop()); return
    a = max(attrs, key=lambda i: gain(rows, i))
    for v in sorted({r[a] for r in rows}):
        print("  " * depth + names[a] + " = " + v)
        id3([r for r in rows if r[a] == v], [i for i in attrs if i != a], depth + 1)
id3(D, [0, 1, 2, 3])
```
```output
H(S) = 0.940
Gain(Outlook) = 0.247
Gain(Temperature) = 0.029
Gain(Humidity) = 0.152
Gain(Wind) = 0.048
Outlook = Overcast
  -> Yes
Outlook = Rain
  Wind = Strong
    -> No
  Wind = Weak
    -> Yes
Outlook = Sunny
  Humidity = High
    -> No
  Humidity = Normal
    -> Yes
```
**Learned tree.** Outlook = Overcast gives Yes; Outlook = Sunny is split by Humidity (High: No, Normal: Yes); Outlook = Rain is split by Wind (Weak: Yes, Strong: No). **Over-fitting** is controlled by *pruning*: stop early (limit depth, minimum samples) or grow fully and remove branches that do not help on validation data. ID3 prefers attributes with many values (an ID column has maximal gain); **C4.5** corrects this with the *gain ratio*. For numeric attributes the tree tests thresholds ($\text{Humidity} \le 75$).

```svgfig label="2.2" caption="The decision tree ID3 learns from the PlayTennis data. Outlook has the highest information gain and is the root; the Sunny and Rain branches are split further by Humidity and Wind."
f = Fig(580, 250)
f.box(220, 10, 140, 34, "Outlook", fill=NAVY, stroke=NAVY, color="#ffffff", bold=True, size=12)
f.box(30, 100, 130, 34, "Humidity", fill=BLUE, stroke=NAVY, bold=True)
f.box(225, 100, 130, 34, "Yes", fill=MINT, stroke=TEAL, bold=True)
f.box(420, 100, 130, 34, "Wind", fill=BLUE, stroke=NAVY, bold=True)
f.arrow([(250, 44), (110, 100)], color=SLATE, label="Sunny", lpos=0.4)
f.arrow([(290, 44), (290, 100)], color=SLATE, label="Overcast", lpos=0.5)
f.arrow([(330, 44), (470, 100)], color=SLATE, label="Rain", lpos=0.4)
for x, t, fill, stroke, lab in ((5, "No", ROSE, RED, "High"), (100, "Yes", MINT, TEAL, "Normal"), (395, "Yes", MINT, TEAL, "Weak"), (490, "No", ROSE, RED, "Strong")):
    f.box(x + 25, 190, 70, 34, t, fill=fill, stroke=stroke, bold=True)
    f.arrow([((95 if x < 300 else 485), 134), (x + 60, 190)], color=SLATE, label=lab, lpos=0.5)
```

## 2.7 Support vector machines

Many lines may separate two classes. The **support vector machine (SVM)** picks the one with the **maximum margin**: the widest street between the classes. A wide margin is less sensitive to small shifts in the data, so it generalises better (this ties back to the VC bound: a larger margin lowers the effective complexity).

### Separating data with maximum margin
For labels $y_i \in \{-1,+1\}$ the separator is $\mathbf{w}\cdot\mathbf{x}+b=0$. Scale $\mathbf{w}, b$ so that the closest points satisfy $y_i(\mathbf{w}\cdot\mathbf{x}_i + b) = 1$. These closest points are the **support vectors**. The two margin lines are $\mathbf{w}\cdot\mathbf{x}+b=\pm 1$, and the distance between them is

$$\text{margin} = \frac{2}{\|\mathbf{w}\|}.$$

### Finding the maximum margin
Maximising $2/\|\mathbf{w}\|$ is the same as solving the **optimisation problem**

$$\min_{\mathbf{w},b}\ \tfrac{1}{2}\|\mathbf{w}\|^{2} \quad\text{subject to}\quad y_i(\mathbf{w}\cdot\mathbf{x}_i + b)\ge 1 \ \text{ for all } i.$$

This is a convex quadratic program, so it has one global optimum. Its dual form depends on the data only through dot products $\mathbf{x}_i\cdot\mathbf{x}_j$, which allows the **kernel trick**: replace the dot product by a kernel $K(\mathbf{x},\mathbf{x}')$ (polynomial, RBF) to separate data that is not linearly separable in the original space. Only the support vectors have non-zero multipliers, so the final classifier is $\hat y=\operatorname{sign}\big(\sum_{i\in SV}\alpha_i y_i K(\mathbf{x}_i,\mathbf{x})+b\big)$. When classes overlap, the **soft margin** allows violations with penalty $C$: large $C$ punishes errors (narrow margin, risk of over-fitting), small $C$ tolerates them.

::: example Three points by hand
Positive class: (3,3) and (4,3); negative class: (1,1). The nearest opposite points are (3,3) and (1,1), so these are the support vectors. By symmetry $\mathbf{w}=(a,a)$. Then $6a+b=1$ and $2a+b=-1$ give $a=0.5$, $b=-2$, so $\mathbf{w}=(0.5,0.5)$, $\|\mathbf{w}\|=0.707$ and the margin is $2/0.707 = 2.83$. The point (4,3) gives $0.5(7)-2=1.5 \ge 1$, so it is correctly outside the margin and is not a support vector.
:::

```python
import numpy as np
P = np.array([[3, 3], [4, 3], [1, 1.0]]); y = np.array([1, 1, -1])
# solve w=(t,t): 6t+b=1, 2t+b=-1
t, b = np.linalg.solve([[6, 1], [2, 1]], [1, -1]); w = np.array([t, t])
print("w =", w, "b =", b, "margin = %.3f" % (2 / np.linalg.norm(w)))
print("y*(w.x+b) =", y * (P @ w + b))
print("support vectors are the points where this equals 1 ->", [tuple(p) for p, v in zip(P, y * (P @ w + b)) if abs(v - 1) < 1e-9])
```
```output
w = [0.5 0.5] b = -1.9999999999999998 margin = 2.828
y*(w.x+b) = [1.  1.5 1. ]
support vectors are the points where this equals 1 -> [(np.float64(3.0), np.float64(3.0)), (np.float64(1.0), np.float64(1.0))]
```

## 2.8 Summary and exercises

Regression fits a line by least squares; the perceptron learns linearly separable problems by error-driven updates; hidden layers and back-propagation overcome XOR; ID3 grows a tree by information gain; the SVM picks the maximum-margin separator defined by its support vectors, with kernels for non-linear boundaries.

1. Fit the least-squares line for the points (1,2), (2,3), (3,5), (4,4) and predict y at x = 5.
2. Explain gradient descent and the effect of too large a learning rate.
3. Train a perceptron by hand (η = 1, start w = (0,0), b = 0) on the OR function for one epoch, going through the inputs in the order 00, 01, 10, 11.
4. Why can a perceptron not learn XOR? How does a two-layer network solve it?
5. Compute the entropy of a set with 3 positive and 1 negative example.
6. Compute the information gain of splitting 10 examples (6 Yes, 4 No) into a branch with (4 Yes, 0 No) and a branch with (2 Yes, 4 No).
7. List the conditions in which decision-tree learning is appropriate and two ways to reduce over-fitting.
8. Define margin, support vector and soft margin. What does the parameter C control?
9. Find the maximum-margin line for the positive points (2,2) and (3,3) and the negative point (0,0).

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Fit a least-squares line to (1,2), (2,3), (3,5), (4,4) and predict y at x = 5.**

$\bar x = 2.5$, $\bar y = 3.5$. $\sum(x-\bar x)(y-\bar y) = (-1.5)(-1.5)+(-0.5)(-0.5)+(0.5)(1.5)+(1.5)(0.5) = 2.25+0.25+0.75+0.75 = 4$; $\sum(x-\bar x)^2 = 5$. So $w_1 = 0.8$ and $w_0 = 3.5 - 2 = 1.5$. The line is $\hat y = 1.5 + 0.8x$ and at $x=5$, $\hat y = 5.5$ (an extrapolation just beyond the data).

**Q2 (5 marks). Train a perceptron on OR for one epoch.**

Rule: $w \leftarrow w + (y-\hat y)x$, $b \leftarrow b + (y - \hat y)$, with $\hat y = 1$ if $z \ge 0$. Start $w=(0,0), b=0$.

| Input | z | ŷ | y | Update | New (w, b) |
|---|---|---|---|---|---|
| 00 | 0 | 1 | 0 | error −1: $w$ unchanged, $b$ −1 | (0,0), −1 |
| 01 | −1 | 0 | 1 | error +1: $w$ += (0,1), $b$ += 1 | (0,1), 0 |
| 10 | 0 | 1 | 1 | none | (0,1), 0 |
| 11 | 1 | 1 | 1 | none | (0,1), 0 |

After one epoch the weights are $(0,1)$ with $b=0$. Two more epochs are needed: the rule settles at $w=(1,1)$, $b=-1$, which classifies all four inputs correctly, as the convergence theorem promises for separable data.

**Q3 (5 marks). Information gain of a split.**

Parent (6 Yes, 4 No): $H = -0.6\log_2 0.6 - 0.4\log_2 0.4 = 0.971$. Branch 1 (4,0): $H=0$. Branch 2 (2,4): $H = -\tfrac13\log_2\tfrac13 - \tfrac23\log_2\tfrac23 = 0.918$. Weighted: $\tfrac{4}{10}(0) + \tfrac{6}{10}(0.918) = 0.551$. Gain $= 0.971 - 0.551 = 0.420$ bits.

**Q4 (10 marks). Explain the ID3 algorithm with an example.**

*Introduction.* ID3 builds a decision tree top-down by repeatedly choosing the attribute with the highest information gain.

*Body.* (1) Compute the entropy of the whole set $S$. (2) For each attribute compute $\mathrm{Gain}(S,A)$. (3) Place the best attribute at the node and create a branch for each value. (4) Send each example down its branch and recurse. (5) Stop when a subset is pure (leaf with its class), when no attributes remain (leaf with the majority class) or when the subset is empty (leaf with the parent's majority).

*Example.* On the PlayTennis data, $H(S)=0.940$ and the gains are Outlook 0.247, Humidity 0.152, Wind 0.048, Temperature 0.029, so Outlook is the root (Figure 2.2). The Overcast branch is pure (Yes); the Sunny branch is split on Humidity and the Rain branch on Wind, giving three levels and five leaves.

*Limits and fixes.* ID3 over-fits and prefers many-valued attributes; pruning and the gain ratio (C4.5) address these. *Conclusion:* ID3 gives readable if-then rules cheaply, suitable for attribute-value problems with discrete classes.

**Q5 (10 marks). Explain the support vector machine and the maximum margin.**

*Introduction.* An SVM is a linear classifier that chooses, among all separating lines, the one with the largest distance to the nearest training points.

*Body.* (1) Separator $\mathbf{w}\cdot\mathbf{x}+b=0$, labels ±1. (2) Scale so that the nearest points satisfy $y(\mathbf{w}\cdot\mathbf{x}+b)=1$; these are the support vectors. (3) Margin $=2/\|\mathbf{w}\|$. (4) Maximising margin is the convex problem $\min \tfrac12\|\mathbf{w}\|^2$ with $y_i(\mathbf{w}\cdot\mathbf{x}_i+b)\ge1$. (5) Only support vectors determine the result. (6) For non-separable data use a soft margin (parameter C) and kernels (polynomial, RBF) that implicitly map the data to a space where a line separates it.

*Example.* For positives (3,3), (4,3) and negative (1,1), the support vectors are (3,3) and (1,1), $\mathbf{w}=(0.5,0.5)$, $b=-2$ and the margin is 2.83 (Section 2.7). *Conclusion:* large margins generalise well and the kernel trick makes SVMs powerful on small and medium data sets.
