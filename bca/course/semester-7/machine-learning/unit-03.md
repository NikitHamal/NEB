---
subject: Machine Learning
grade: BCA Semester 7 (Elective I)
unit: 3
title: Bayesian and Instance-Based Learning
hours: 11
area: BCA 405 · Machine Learning · Unit 3
---

A doctor tells you a test for a rare disease is "90 percent accurate" and yours is positive. Are you 90 percent likely to be ill? Almost certainly not, and the reason is **Bayes' rule**. This unit turns probability into a classifier: Bayes decision theory, naive Bayes, Bayesian belief networks, and then a very different idea, **k-nearest neighbour**, which learns nothing in advance and decides by looking at the most similar past examples.

::: key What this unit gives you
- Probability theory: conditional probability, independence, total probability and Bayes' rule.
- Bayes decision theory: minimum-error and minimum-risk classification.
- Naive Bayes with Laplace smoothing, worked on the tennis data and a spam example.
- Bayesian belief networks: structure, conditional probability tables and exact inference by enumeration.
- k-nearest neighbour: distance, the choice of k, weighting, and the curse of dimensionality.
:::

## 3.1 Probability theory and Bayes' rule

The **probability** of an event $A$ is a number $P(A)\in[0,1]$. The **conditional probability** of $A$ given $B$ is

$$P(A\mid B) = \frac{P(A\cap B)}{P(B)}, \qquad P(B)>0.$$

Events are **independent** when $P(A\cap B)=P(A)P(B)$, equivalently $P(A\mid B)=P(A)$. They are **conditionally independent** given $C$ if $P(A\cap B\mid C)=P(A\mid C)P(B\mid C)$. If $B_1,\dots,B_k$ partition the sample space, the **law of total probability** gives $P(A)=\sum_i P(A\mid B_i)P(B_i)$. Combining the product rule $P(A\cap B)=P(A\mid B)P(B)=P(B\mid A)P(A)$ gives **Bayes' rule**:

$$P(H\mid D) = \frac{P(D\mid H)\,P(H)}{P(D)}.$$

In learning, $H$ is a hypothesis (class), $D$ is the observed data. $P(H)$ is the **prior**, $P(D\mid H)$ the **likelihood**, $P(D)$ the **evidence** and $P(H\mid D)$ the **posterior**. Learning is updating belief from prior to posterior as data arrives.

::: example The rare-disease test
A disease affects 1 percent of people. The test detects it in 90 percent of ill people (sensitivity) and wrongly flags 5 percent of healthy people (false-positive rate). $P(+) = 0.9(0.01)+0.05(0.99) = 0.0585$, so $P(\text{ill}\mid +) = 0.009/0.0585 = 0.154$. Only about 15 percent of positives are truly ill, because healthy people are so many more. This is the **base-rate fallacy**.
:::

```python
prior, sens, fpr = 0.01, 0.90, 0.05
evidence = sens * prior + fpr * (1 - prior)
print("P(+) = %.4f" % evidence)
print("P(ill | +) = %.3f" % (sens * prior / evidence))
for p in (0.001, 0.01, 0.1, 0.5):
    print("prevalence %.3f -> posterior %.3f" % (p, sens * p / (sens * p + fpr * (1 - p))))
```
```output
P(+) = 0.0585
P(ill | +) = 0.154
prevalence 0.001 -> posterior 0.018
prevalence 0.010 -> posterior 0.154
prevalence 0.100 -> posterior 0.667
prevalence 0.500 -> posterior 0.947
```
## 3.2 Classifying with Bayes decision theory

Given features $\mathbf{x}$ and classes $\omega_1,\dots,\omega_c$, the **Bayes classifier** chooses the class with the largest posterior:

$$\hat\omega = \arg\max_k P(\omega_k\mid\mathbf{x}) = \arg\max_k\ p(\mathbf{x}\mid\omega_k)\,P(\omega_k),$$

(the evidence is the same for all classes and can be dropped). This **minimises the probability of error**, and no other classifier can have a lower error rate; that lowest rate is the **Bayes error**, the noise floor of Unit 1.

**Minimum risk.** Errors rarely cost the same. Let $\lambda(\alpha_i\mid\omega_j)$ be the loss of taking action $\alpha_i$ when the truth is $\omega_j$. The **conditional risk** of action $\alpha_i$ is $R(\alpha_i\mid\mathbf{x})=\sum_j\lambda(\alpha_i\mid\omega_j)P(\omega_j\mid\mathbf{x})$ and the decision is the action with the smallest risk.

::: example Loan decision with unequal costs
For an applicant $P(\text{good}\mid\mathbf{x})=0.7$ and $P(\text{bad}\mid\mathbf{x})=0.3$. Losses: approving a bad borrower costs Rs 100,000; rejecting a good borrower loses Rs 10,000 of interest; correct decisions cost 0. $R(\text{approve}) = 0.3(100{,}000)=30{,}000$ and $R(\text{reject}) = 0.7(10{,}000)=7{,}000$. Reject, even though "good" is more likely, because a bad loan is ten times costlier.
:::

## 3.3 Naive Bayes classifier

With many features, the likelihood $p(x_1,\dots,x_n\mid\omega)$ needs a table that grows exponentially. **Naive Bayes** assumes the features are **conditionally independent given the class**:

$$\hat\omega = \arg\max_k\ P(\omega_k)\prod_{i=1}^{n}P(x_i\mid\omega_k).$$

The assumption is almost never true, yet the classifier is often accurate because only the *ranking* of classes matters, not exact probabilities. It trains by counting, so it is fast and works with little data.

**Laplace smoothing.** If a value never appears with a class in the training data, its count is 0 and the whole product becomes 0. Add 1 to every count: $P(x_i=v\mid\omega)=\dfrac{n_{v,\omega}+1}{n_\omega+m}$ where $m$ is the number of possible values.

::: example Tennis: Outlook = Sunny, Temperature = Cool, Humidity = High, Wind = Strong
From the 14 days: $P(\text{Yes})=9/14$, $P(\text{No})=5/14$. For Yes: $P(\text{Sunny})=2/9$, $P(\text{Cool})=3/9$, $P(\text{High})=3/9$, $P(\text{Strong})=3/9$, giving $\tfrac{9}{14}\cdot\tfrac29\cdot\tfrac39\cdot\tfrac39\cdot\tfrac39 = 0.0053$. For No: $\tfrac5{14}\cdot\tfrac35\cdot\tfrac15\cdot\tfrac45\cdot\tfrac35 = 0.0206$. Normalising, $P(\text{No}) = 0.0206/(0.0206+0.0053) = 0.795$. Predict **No**.
:::

```python
from collections import Counter
D = [("Sunny","Hot","High","Weak","No"),("Sunny","Hot","High","Strong","No"),("Overcast","Hot","High","Weak","Yes"),
     ("Rain","Mild","High","Weak","Yes"),("Rain","Cool","Normal","Weak","Yes"),("Rain","Cool","Normal","Strong","No"),
     ("Overcast","Cool","Normal","Strong","Yes"),("Sunny","Mild","High","Weak","No"),("Sunny","Cool","Normal","Weak","Yes"),
     ("Rain","Mild","Normal","Weak","Yes"),("Sunny","Mild","Normal","Strong","Yes"),("Overcast","Mild","High","Strong","Yes"),
     ("Overcast","Hot","Normal","Weak","Yes"),("Rain","Mild","High","Strong","No")]
query = ("Sunny", "Cool", "High", "Strong")
classes = Counter(r[-1] for r in D)
score = {}
for c, nc in classes.items():
    p = nc / len(D)
    for i, v in enumerate(query):
        p *= sum(1 for r in D if r[-1] == c and r[i] == v) / nc
    score[c] = p
total = sum(score.values())
for c in score: print(c, "score %.4f  posterior %.3f" % (score[c], score[c] / total))
print("prediction:", max(score, key=score.get))
# Laplace-smoothed spam example: counts of words in 6 spam and 6 ham messages
spam = {"free": 4, "offer": 3, "meeting": 0}; ham = {"free": 1, "offer": 1, "meeting": 4}
for word in ("free", "meeting"):
    print(word, "P(w|spam) = %.3f  smoothed %.3f" % (spam[word] / 6, (spam[word] + 1) / (6 + 2)))
```
```output
No score 0.0206  posterior 0.795
Yes score 0.0053  posterior 0.205
prediction: No
free P(w|spam) = 0.667  smoothed 0.625
meeting P(w|spam) = 0.000  smoothed 0.125
```
For continuous features, **Gaussian naive Bayes** models each $P(x_i\mid\omega)$ by a normal density with the class mean and variance. **Text classification** (spam, sentiment) uses word counts (multinomial naive Bayes) and sums log-probabilities to avoid numerical underflow.

## 3.4 Bayesian belief networks

When full independence is too strong, a **Bayesian belief network** (Bayesian network) encodes *which* variables depend on which. It is a **directed acyclic graph**: each node is a random variable, an edge $A\to B$ means $A$ directly influences $B$, and each node has a **conditional probability table (CPT)** $P(\text{node}\mid\text{parents})$. The joint distribution factorises as

$$P(x_1,\dots,x_n) = \prod_{i=1}^{n}P\big(x_i\mid\mathrm{parents}(x_i)\big).$$

A network with $n$ binary variables needs $2^n-1$ numbers for the full joint but only $\sum 2^{|\text{parents}|}$ for its CPTs, a large saving for sparse graphs.

::: example The burglar alarm (Pearl; Russell and Norvig)
Burglary (B) and Earthquake (E) both cause the Alarm (A); Alarm causes John to call (J) and Mary to call (M). $P(B)=0.001$, $P(E)=0.002$. $P(A\mid B,E)$: 0.95 (B and E), 0.94 (B only), 0.29 (E only), 0.001 (neither). $P(J\mid A)=0.90$, $P(J\mid\neg A)=0.05$; $P(M\mid A)=0.70$, $P(M\mid\neg A)=0.01$. If both John and Mary call, what is the probability of a burglary?
:::

```svgfig label="3.1" caption="The burglar-alarm Bayesian network. Arrows run from causes to effects. Burglary and Earthquake are parents of Alarm; John and Mary each depend only on Alarm, so given the alarm they are independent of the burglary."
f = Fig(580, 230)
f.circle(150, 40, 30, fill=BLUE, stroke=NAVY, label="Burglary\nP=0.001", size=9)
f.circle(430, 40, 30, fill=BLUE, stroke=NAVY, label="Earthquake\nP=0.002", size=9)
f.circle(290, 120, 30, fill=ROSE, stroke=RED, label="Alarm", size=10)
f.circle(180, 200, 28, fill=MINT, stroke=TEAL, label="John\ncalls", size=9)
f.circle(400, 200, 28, fill=MINT, stroke=TEAL, label="Mary\ncalls", size=9)
f.arrow([(172, 62), (268, 100)], color=SLATE)
f.arrow([(408, 62), (312, 100)], color=SLATE)
f.arrow([(272, 146), (200, 178)], color=SLATE)
f.arrow([(308, 146), (380, 178)], color=SLATE)
```

**Exact inference by enumeration.** Sum the joint over the hidden variables: $P(B\mid j,m)=\alpha\sum_e\sum_a P(B)P(e)P(a\mid B,e)P(j\mid a)P(m\mid a)$, where $\alpha$ normalises.

```python
from itertools import product
PB, PE = 0.001, 0.002
PA = {(1, 1): 0.95, (1, 0): 0.94, (0, 1): 0.29, (0, 0): 0.001}
PJ = {1: 0.90, 0: 0.05}; PM = {1: 0.70, 0: 0.01}
def joint(b, e, a, j=1, m=1):
    p = (PB if b else 1 - PB) * (PE if e else 1 - PE)
    p *= PA[(b, e)] if a else 1 - PA[(b, e)]
    p *= PJ[a] if j else 1 - PJ[a]
    p *= PM[a] if m else 1 - PM[a]
    return p
num = sum(joint(1, e, a) for e, a in product((0, 1), repeat=2))
den = sum(joint(b, e, a) for b, e, a in product((0, 1), repeat=3))
print("P(Burglary | John and Mary call) = %.3f" % (num / den))
print("P(Alarm | John and Mary call)    = %.3f" % (sum(joint(b, e, 1) for b, e in product((0, 1), repeat=2)) / den))
```
```output
P(Burglary | John and Mary call) = 0.284
P(Alarm | John and Mary call)    = 0.761
```
The answer is about 0.284: even with two calls a burglary is less than 30 percent likely, because burglaries are so rare *a priori* and either call may be false. Networks can be built from expert knowledge or learned from data (structure search plus counting for the CPTs); exact inference is exponential in general, so large networks use approximations such as sampling.

## 3.5 K-nearest neighbour (k-NN)

**Instance-based** (memory-based, lazy) learners do no training: they store the examples and do the work at prediction time. **k-NN** classifies a query point by finding the $k$ stored examples closest to it and taking a **majority vote** of their labels (for regression, the *average* of their values).

**Algorithm.** (1) Choose $k$ and a distance. (2) Compute the distance from the query to every training example. (3) Select the $k$ smallest. (4) Vote (or average). The most common distance is **Euclidean**, $d(\mathbf{x},\mathbf{z})=\sqrt{\sum_i (x_i-z_i)^2}$; others are in Section 4.2.

**Choosing k.** $k=1$ follows every point, noise included (low bias, high variance, a jagged boundary); a very large $k$ over-smooths (high bias; in the extreme $k=N$ predicts the majority class everywhere). Use an odd $k$ for two classes to avoid ties, and pick it by **validation or cross-validation** (try $k=1,3,5,\dots$). A common starting point is $k\approx\sqrt N$.

**Weighted k-NN.** Let closer neighbours count more: weight $w_i = 1/d_i^{2}$, so a very near neighbour outvotes several distant ones.

In the example the weighted vote for $k=5$ is Blue (about 2.07 against 0.67 for Red) because G is so close, so weighting can overturn the plain vote.

**Scaling matters.** If income (in rupees) and age (in years) are both used, income dominates the distance. Standardise or min-max scale every feature first.

::: example Predict the class
Training points (x1, x2, class): A (1,1,Red), B (2,1,Red), C (2,2,Red), D (6,5,Blue), E (7,7,Blue), F (6,6,Blue), G (3,3,Blue). Query $q=(2.5,3.5)$. Distances: G 0.71, C 1.58, B 2.55, A 2.92, D 3.81, F 4.30, E 5.70. With $k=1$ the nearest is G, so **Blue**. With $k=3$ the neighbours are G (Blue), C (Red), B (Red): **Red** wins 2 to 1. With $k=5$ add A (Red) and D (Blue): 3 Red and 2 Blue, so **Red**. The answer changes with $k$, which is why $k$ is chosen by validation.
:::

```python
import numpy as np
from collections import Counter
P = np.array([[1,1],[2,1],[2,2],[6,5],[7,7],[6,6],[3,3.0]]); lab = ["Red","Red","Red","Blue","Blue","Blue","Blue"]
q = np.array([2.5, 3.5])
d = np.sqrt(((P - q) ** 2).sum(axis=1))
order = np.argsort(d)
print("distances:", {n: round(float(v), 2) for n, v in zip("ABCDEFG", d)})
for k in (1, 3, 5):
    votes = Counter(lab[i] for i in order[:k])
    print("k =", k, votes.most_common(), "->", votes.most_common(1)[0][0])
w = 1 / d[order[:5]] ** 2
print("weighted k=5 vote:", {c: round(float(sum(w[j] for j, i in enumerate(order[:5]) if lab[i] == c)), 3) for c in ("Red", "Blue")})
```
```output
distances: {'A': 2.92, 'B': 2.55, 'C': 1.58, 'D': 3.81, 'E': 5.7, 'F': 4.3, 'G': 0.71}
k = 1 [('Blue', 1)] -> Blue
k = 3 [('Red', 2), ('Blue', 1)] -> Red
k = 5 [('Red', 3), ('Blue', 2)] -> Red
weighted k=5 vote: {'Red': 0.671, 'Blue': 2.069}
```
```svgfig label="3.2" caption="k-NN on seven points. The query (amber) at (2.5, 3.5) is classified by its nearest neighbours. The dashed circle contains the k = 3 nearest points: one Blue and two Red, so the vote is Red. With k = 1 the nearest point is Blue."
f = Fig(580, 250)
ax = Axes(f, 60, 15, 330, 200, (0, 8), (0, 8))
ax.grid(1, 1)
ax.axes("x1", "x2")
for x, y, c in ((1,1,0),(2,1,0),(2,2,0),(6,5,1),(7,7,1),(6,6,1),(3,3,1)):
    ax.pt(x, y, "", r=6, color=(NAVY if c else RED))
ax.pt(2.5, 3.5, "", r=7, color=AMBER)
f.raw('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="%s" stroke-width="1.5" stroke-dasharray="5 4"/>' % (ax.X(2.5), ax.Y(3.5), ax.X(2.55) - ax.X(0), TEAL))
f.text(470, 70, "Red class", size=11, color=RED, bold=True)
f.text(470, 100, "Blue class", size=11, color=NAVY, bold=True)
f.text(470, 130, "Query (2.5, 3.5)", size=11, color=AMBER, bold=True)
f.text(470, 165, "k = 1 -> Blue", size=11, color=NAVY, bold=True)
f.text(470, 190, "k = 3 -> Red", size=11, color=RED, bold=True)
```

**The curse of dimensionality.** In many dimensions every point is almost equally far from every other, so "nearest" loses meaning, and the data needed grows exponentially. The program measures the gap between the nearest and the farthest of 500 random points:

```python
import numpy as np
rng = np.random.default_rng(0)
for dim in (2, 10, 100, 1000):
    X = rng.random((500, dim)); q = rng.random(dim)
    d = np.sqrt(((X - q) ** 2).sum(axis=1))
    print("dim %4d  nearest/farthest distance ratio = %.2f" % (dim, d.min() / d.max()))
```
```output
dim    2  nearest/farthest distance ratio = 0.02
dim   10  nearest/farthest distance ratio = 0.18
dim  100  nearest/farthest distance ratio = 0.74
dim 1000  nearest/farthest distance ratio = 0.90
```
**Strengths and weaknesses.**

| Strengths | Weaknesses |
|---|---|
| No training; new data is added at once | Slow prediction (distance to every example); needs indexing such as k-d trees |
| Handles non-linear boundaries naturally | Needs scaling and a sensible distance |
| Few assumptions; works for classification and regression | Hurt by irrelevant features and high dimensions; stores all data |

## 3.6 Maximum likelihood, MAP and Gaussian naive Bayes

Two ways to estimate a parameter $\theta$ from data $D$: **maximum likelihood (ML)** picks the $\theta$ that makes the data most probable, $\hat\theta_{ML}=\arg\max P(D\mid\theta)$; **maximum a posteriori (MAP)** also uses a prior, $\hat\theta_{MAP}=\arg\max P(D\mid\theta)P(\theta)$. For a coin with 3 heads in 3 tosses, ML says $P(\text{head})=1$ (absurd after three tosses); a prior that favours fair coins moves the MAP estimate towards 0.5. Laplace smoothing is exactly MAP with a uniform prior. With more data the likelihood dominates and the two agree.

For **continuous features** Gaussian naive Bayes models $P(x\mid\omega)$ as a normal density $\mathcal N(\mu_\omega,\sigma_\omega^2)$ whose mean and variance are estimated from each class.

```python
import numpy as np
from math import exp, pi, sqrt
small = np.array([158, 162, 165, 170, 172.0]); tall = np.array([176, 180, 183, 185, 190.0])   # heights (cm): shorter vs taller group
def pdf(x, v): m, s = v.mean(), v.std(ddof=1); return exp(-((x - m) ** 2) / (2 * s * s)) / (s * sqrt(2 * pi))
for h in (168, 174, 178):
    a, b = pdf(h, small) * 0.5, pdf(h, tall) * 0.5
    print("height %d: P(group A) = %.3f, P(group B) = %.3f -> %s" % (h, a / (a + b), b / (a + b), "A" if a > b else "B"))
print("ML estimate of P(head) after 3 heads in 3 tosses = 1.0; MAP with a Beta(5,5) prior = %.3f" % ((3 + 4) / (3 + 8)))
```
```output
height 168: P(group A) = 0.977, P(group B) = 0.023 -> A
height 174: P(group A) = 0.546, P(group B) = 0.454 -> A
height 178: P(group A) = 0.110, P(group B) = 0.890 -> B
ML estimate of P(head) after 3 heads in 3 tosses = 1.0; MAP with a Beta(5,5) prior = 0.636
```
The **MAP** value uses the prior pseudo-counts: with a Beta(5,5) prior (equivalent to 4 imaginary heads and 4 imaginary tails beyond the first), the estimate is $(3+4)/(3+8)=0.636$, much more sensible than 1.0.

## 3.7 Naive Bayes for text and the zero-frequency problem

Spam filtering is the classic naive Bayes application. A message is a bag of words; the **multinomial** model estimates $P(w\mid c)$ as the fraction of all word positions in class $c$ that hold word $w$, and scores a message by $\log P(c)+\sum_{w}\log P(w\mid c)$. Logarithms turn a product of many tiny numbers into a sum and prevent numerical underflow; the class with the larger score wins.

The trouble is a word never seen in one class during training. Its estimated probability is $0$, and a single zero multiplies the whole product to $0$, no matter how strongly the other words point to that class. **Laplace smoothing** (add-one) repairs this by adding $\alpha=1$ to every count and $\alpha V$ to the denominator, where $V$ is the vocabulary size:

$$P(w\mid c)=\frac{\text{count}(w,c)+\alpha}{\text{tokens}(c)+\alpha V}.$$

The program trains on seven tiny messages (three spam, four ham) and scores three new messages with $\alpha=0$ and with $\alpha=1$.

```python
import math
from collections import Counter
spam = ["win free prize now", "free recharge offer win", "claim prize free offer"]
ham = ["meeting at ten tomorrow", "send the notes tomorrow", "lab report due tomorrow", "free at ten for meeting"]
vocab = sorted({w for m in spam + ham for w in m.split()})
cs, ch = Counter(w for m in spam for w in m.split()), Counter(w for m in ham for w in m.split())
ns, nh = sum(cs.values()), sum(ch.values())
print("vocabulary size V = %d, spam tokens = %d, ham tokens = %d" % (len(vocab), ns, nh))
print("P(spam) = %d/7, P(ham) = %d/7" % (len(spam), len(ham)))
def logpost(msg, counts, n, prior, alpha):
    s = math.log(prior)
    for w in msg.split():
        p = (counts[w] + alpha) / (n + alpha * len(vocab))
        if p == 0: return float("-inf")
        s += math.log(p)
    return s
for msg in ("free prize tomorrow", "win free notes", "claim cash offer now"):
    for alpha in (0, 1):
        a = logpost(msg, cs, ns, 3 / 7, alpha); b = logpost(msg, ch, nh, 4 / 7, alpha)
        if a == b == float("-inf"): verdict, pr = "undefined", "both zero"
        else:
            verdict = "spam" if a > b else "ham"
            pr = "P(spam|msg) = %.3f" % (1 / (1 + math.exp(b - a))) if math.isfinite(a) and math.isfinite(b) else ("P(spam|msg) = %d" % (a > b))
        print("%-22s alpha=%d  log spam %8.3f  log ham %8.3f  -> %s (%s)" % (msg, alpha, a, b, verdict, pr))
```
```output
vocabulary size V = 18, spam tokens = 12, ham tokens = 17
P(spam) = 3/7, P(ham) = 4/7
free prize tomorrow    alpha=0  log spam     -inf  log ham     -inf  -> undefined (both zero)
free prize tomorrow    alpha=1  log spam   -8.566  log ham   -9.146  -> spam (P(spam|msg) = 0.641)
win free notes         alpha=0  log spam     -inf  log ham     -inf  -> undefined (both zero)
win free notes         alpha=1  log spam   -8.566  log ham   -9.839  -> spam (P(spam|msg) = 0.781)
claim cash offer now   alpha=0  log spam     -inf  log ham     -inf  -> undefined (both zero)
claim cash offer now   alpha=1  log spam  -11.967  log ham  -14.781  -> spam (P(spam|msg) = 0.943)
```

Without smoothing every test message is **undefined**: each contains one word that is missing from one class and another word that is missing from the other, so both scores are zero. With add-one smoothing the filter gives a decision with a calibrated-looking probability. Work the first message by hand: the spam class has 12 tokens and the vocabulary has 18 words, so $P(\text{free}\mid S)=4/30$, $P(\text{prize}\mid S)=3/30$, $P(\text{tomorrow}\mid S)=1/30$ and the score is $\ln(\tfrac37\cdot\tfrac{4\cdot3\cdot1}{30^3})=-8.566$. The ham class has 17 tokens, so the denominators are 35 and the score is $\ln(\tfrac47\cdot\tfrac{2\cdot1\cdot4}{35^3})=-9.146$. Spam wins by a factor $e^{0.58}=1.8$, which is a posterior of 0.641: honest uncertainty, since "free" occurs in both classes and "tomorrow" is a ham word.

::: tip Practical notes for naive Bayes text models
Lower-case and tokenise first; drop very frequent stop words if they carry no class information; use $\alpha$ between 0.1 and 1 chosen on validation data; store log probabilities, not probabilities; for long documents the independence assumption makes the posterior over-confident, but the **ranking** of classes is usually still right, which is all classification needs.
:::

## 3.8 Locally weighted regression and lazy learning

k-NN is a **lazy** learner: it stores the data and does the work only when a query arrives. Mitchell (chapter 8) generalises the idea to numeric targets with **locally weighted regression** (LWR). To predict at a query point $q$, fit a simple model, here a straight line, using **all** training points but weight each point by its closeness to $q$,

$$w_i=\exp\!\left(-\frac{(x_i-q)^2}{2\tau^2}\right),\qquad \boldsymbol\beta(q)=(A^{T}WA)^{-1}A^{T}Wy,$$

where $W$ is the diagonal matrix of the weights and $\tau$ is the **bandwidth**. A fresh line is fitted for every query, so the final prediction function can bend to follow the data even though each local model is a straight line. A small $\tau$ means a narrow neighbourhood (flexible, high variance); a large $\tau$ makes all weights almost equal and gives the ordinary global line (rigid, high bias). The bandwidth is therefore the bias-variance dial of Section 1.8.

The program fits 60 noisy points of $y=\sin x+0.3x$ and reports the error of a global line and of LWR with four bandwidths against the true curve.

```python
import numpy as np
rng = np.random.default_rng(5)
x = np.sort(rng.uniform(0, 6, 60)); true = lambda t: np.sin(t) + 0.3 * t
y = true(x) + rng.normal(0, 0.15, 60)
def lwr(q, tau):
    w = np.exp(-(x - q) ** 2 / (2 * tau ** 2))          # Gaussian weight of each training point
    A = np.c_[np.ones_like(x), x]
    beta = np.linalg.solve(A.T @ (w[:, None] * A), A.T @ (w * y))
    return beta[0] + beta[1] * q
grid = np.linspace(0.3, 5.7, 28)
glob = np.polyfit(x, y, 1)
rows = [("global straight line", np.polyval(glob, grid))]
for tau in (2.0, 0.6, 0.25, 0.05):
    rows.append(("LWR tau = %.2f" % tau, np.array([lwr(q, tau) for q in grid])))
print("method                  RMSE against the true curve")
for name, pred in rows:
    print("%-22s  %.3f" % (name, np.sqrt(np.mean((pred - true(grid)) ** 2))))
q = 3.0
for tau in (0.6,):
    w = np.exp(-(x - q) ** 2 / (2 * tau ** 2))
    print("query x = %.1f, tau = %.1f: effective points = %.1f of 60, prediction %.3f, truth %.3f" % (q, tau, w.sum() ** 2 / (w ** 2).sum(), lwr(q, tau), true(q)))
```
```output
method                  RMSE against the true curve
global straight line    0.390
LWR tau = 2.00          0.338
LWR tau = 0.60          0.126
LWR tau = 0.25          0.063
LWR tau = 0.05          2.233
query x = 3.0, tau = 0.6: effective points = 19.2 of 60, prediction 0.971, truth 1.041
```

The global line (RMSE 0.390) cannot follow the sine wave; $\tau=2$ is nearly as rigid (0.338). Bandwidths 0.6 and 0.25 follow the curve well (0.126 and 0.063). At $\tau=0.05$ the weights are almost zero for all but one or two points, the weighted fit is nearly singular and the error jumps to 2.233: the model has become pure variance. At the query $x=3$ with $\tau=0.6$ about 19 of the 60 points effectively take part. The price of lazy learning is clear: no model is built in advance, but every prediction costs a full pass over the data and a small linear solve.

::: definition Case-based reasoning (CBR)
**Case-based reasoning** extends instance-based learning to rich, non-numeric instances such as past help-desk tickets or legal cases. Its four steps are **retrieve** the most similar stored case, **reuse** its solution, **revise** the solution when it does not fit, and **retain** the corrected case for the future. A bank that approves a loan by finding the most similar previous applicants is doing CBR with a similarity measure instead of a model.
:::

## 3.9 Choosing k, distance weighting and the curse of dimensionality

Two design choices decide whether k-NN works. **The value of k:** a small $k$ follows noise (high variance), a large $k$ blurs the class boundary (high bias), and $k=n$ simply predicts the majority class. Choose $k$ by validation, preferably odd for two classes to avoid ties. **Distance weighting:** let a neighbour at distance $d$ vote with weight $1/d^2$ so that nearer neighbours count more.

The second danger is **dimension**. In high dimensions all points are almost equally far from each other, so "nearest" loses meaning, and a feature irrelevant to the label adds noise to every distance. The program measures leave-one-out accuracy on 120 overlapping points and then the relative gap between the farthest and the nearest of 500 random points as the number of dimensions grows.

```python
import numpy as np
rng = np.random.default_rng(3)
# (a) leave-one-out accuracy of k-NN on two overlapping classes, plain and distance-weighted vote
X = np.vstack([rng.normal(0, 1.0, (60, 2)), rng.normal(1.5, 1.0, (60, 2))]); y = np.r_[np.zeros(60, int), np.ones(60, int)]
D = np.sqrt(((X[:, None] - X[None]) ** 2).sum(-1)); np.fill_diagonal(D, np.inf)
order = np.argsort(D, axis=1)
print("k    plain vote   distance-weighted vote")
for k in (1, 3, 5, 9, 15, 31, 61):
    nn = order[:, :k]
    plain = (y[nn].mean(1) > 0.5).astype(int)
    wts = 1 / (np.take_along_axis(D, nn, 1) ** 2 + 1e-9)
    wtd = ((wts * y[nn]).sum(1) / wts.sum(1) > 0.5).astype(int)
    print("%-3d  %.3f        %.3f" % (k, (plain == y).mean(), (wtd == y).mean()))
# (b) distance concentration in high dimension: ratio (farthest - nearest) / nearest from a random query
print("dimension   (max - min) / min distance")
for d in (1, 2, 10, 100, 1000):
    P = rng.uniform(0, 1, (500, d)); q = rng.uniform(0, 1, d)
    dist = np.sqrt(((P - q) ** 2).sum(1))
    print("%-10d  %.2f" % (d, (dist.max() - dist.min()) / dist.min()))
```
```output
k    plain vote   distance-weighted vote
1    0.783        0.783
3    0.800        0.783
5    0.825        0.800
9    0.858        0.808
15   0.858        0.808
31   0.867        0.817
61   0.850        0.808
dimension   (max - min) / min distance
1           259.94
2           101.05
10          2.06
100         0.44
1000        0.12
```

Accuracy rises from 0.78 at $k=1$ to a plateau of about 0.86 for $k$ from 9 to 31 and drops slightly at $k=61$, the expected bias-variance shape. On this data the weighted vote was **not** better than the plain vote: weighting helps mostly when classes overlap little or neighbour distances differ a lot, so it must be tested, not assumed. The second table is the **curse of dimensionality**: the relative contrast $(d_{\max}-d_{\min})/d_{\min}$ collapses from about 260 in one dimension to 0.12 in 1000 dimensions, so the farthest point is only 12 percent farther than the nearest. Remedies are feature selection, dimensionality reduction (Section 4.7) and metrics learned from data.

## 3.10 Summary and exercises

Bayes' rule converts likelihood and prior into a posterior. The Bayes classifier picks the most probable class (minimum error) or the least risky action (minimum risk). Naive Bayes multiplies per-feature likelihoods under conditional independence and uses Laplace smoothing. A Bayesian network is a DAG with CPTs that factorises the joint distribution. k-NN votes among the k closest stored examples; the choice of k, the distance and feature scaling decide its quality.

1. A factory has two machines: M1 makes 60 percent of items with 2 percent defects, M2 makes 40 percent with 5 percent defects. A defective item is found; what is the probability it came from M2?
2. Define prior, likelihood, evidence and posterior with a spam example.
3. Why is naive Bayes called "naive"? Why does it often work anyway?
4. Using the PlayTennis counts, classify (Rain, Mild, Normal, Weak) with naive Bayes.
5. A word never appears in the spam training mails. Show how Laplace smoothing prevents a zero probability.
6. Draw a Bayesian network for Rain, Sprinkler and Wet-grass and write the factorisation of the joint distribution.
7. Classify the query (5,5) with k = 3 using the seven points of Section 3.5, and then repeat with k = 5.
8. What is the effect of k = 1 and of k = N? How do you select k?
9. Why must features be scaled for k-NN? Give an example.
10. Using the seven training messages of Section 3.7, classify "prize offer" with add-one smoothing and show the two scores.
11. Why does Laplace smoothing use $\alpha V$ in the denominator? Show that the smoothed probabilities of all words in a class sum to 1.
12. Explain locally weighted regression and the role of the bandwidth $\tau$.
13. Differentiate eager and lazy learners; give two examples of each and one drawback of lazy learning.
14. Describe the four steps of case-based reasoning with a help-desk example.
15. Describe the curse of dimensionality and two ways to reduce its effect on k-NN.

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Defective item: which machine?**

$P(D) = 0.6(0.02) + 0.4(0.05) = 0.012 + 0.020 = 0.032$. By Bayes' rule $P(M_2\mid D) = 0.020/0.032 = 0.625$. Although M2 makes fewer items, 62.5 percent of defects come from it because its defect rate is 2.5 times higher.

**Q2 (5 marks). Naive Bayes for (Rain, Mild, Normal, Weak).**

From the data: Yes (9 days): Rain 3/9, Mild 4/9, Normal 6/9, Weak 6/9. No (5 days): Rain 2/5, Mild 2/5, Normal 1/5, Weak 2/5. Score(Yes) $= \tfrac9{14}\cdot\tfrac39\cdot\tfrac49\cdot\tfrac69\cdot\tfrac69 = 0.0423$. Score(No) $= \tfrac5{14}\cdot\tfrac25\cdot\tfrac25\cdot\tfrac15\cdot\tfrac25 = 0.0046$. The class is **Yes** (posterior $0.0423/(0.0423+0.0046)\approx 0.90$).

**Q3 (5 marks). k-NN prediction for q = (5,5), k = 3.**

Distances: D (6,5) = 1.00, F (6,6) = 1.41, G (3,3) = 2.83, E (7,7) = 2.83, C (2,2) = 4.24. The three nearest are D (Blue), F (Blue) and then G or E (tie at 2.83, both Blue). All three are Blue, so the class is **Blue**.

**Q4 (10 marks). Explain Bayesian belief networks with an example.**

*Introduction.* A Bayesian network represents the joint distribution of many variables compactly by using the conditional independences among them.

*Body.* (1) Structure: a directed acyclic graph; an edge means direct influence. (2) Parameters: a conditional probability table for every node given its parents. (3) Factorisation: $P(x_1,\dots,x_n)=\prod P(x_i\mid\text{parents})$. (4) Inference: sum out hidden variables (enumeration), then normalise. (5) Saving: with $n$ binary variables the joint has $2^n-1$ free numbers, while the CPTs need only a few for sparse graphs.

*Example.* In the alarm network (Figure 3.1) the joint is $P(B)P(E)P(A\mid B,E)P(J\mid A)P(M\mid A)$ with 10 numbers instead of 31. Enumeration gives $P(B\mid J,M)=0.284$ and $P(A\mid J,M)=0.761$.

*Conclusion.* Bayesian networks combine expert knowledge and data, handle uncertainty and missing evidence, and explain which variables matter.

**Q5 (10 marks). Compare naive Bayes and k-NN.**

*Introduction.* Both are simple classifiers, but one is model-based and the other instance-based.

| Aspect | Naive Bayes | k-NN |
|---|---|---|
| Idea | Posterior from priors and per-feature likelihoods | Vote of the k most similar stored examples |
| Training | Counts (fast) | None (stores data) |
| Prediction | Very fast | Slow (distance to all examples) |
| Assumption | Features independent given the class | Similar inputs have similar labels |
| Data needs | Works with small data | Needs enough data near the query |
| Scaling | Not needed | Essential |
| Output | Class probabilities | Class (or vote share) |
| Weak point | Correlated features | Irrelevant features, high dimensions |

*Conclusion.* Use naive Bayes for text and fast baselines with little data, and k-NN when the boundary is irregular, the feature count is small and prediction speed is not critical.

**Q6 (5 marks). Classify "prize offer" with add-one smoothing.**

Spam has 12 tokens, ham 17, $V=18$. Counts: in spam prize = 2 and offer = 2; in ham both are 0. Spam score: $\ln\!\big(\tfrac37\cdot\tfrac{3}{30}\cdot\tfrac{3}{30}\big)=\ln(0.004286)=-5.45$. Ham score: $\ln\!\big(\tfrac47\cdot\tfrac{1}{35}\cdot\tfrac{1}{35}\big)=\ln(0.000467)=-7.67$. Spam is larger by a factor $e^{2.22}\approx9.2$, so the message is spam with posterior about 0.90.

**Q7 (5 marks). Why $\alpha V$ in the denominator.**

Adding $\alpha$ to each of the $V$ word counts adds $\alpha V$ to the total, so $\sum_w \frac{n_w+\alpha}{N+\alpha V}=\frac{N+\alpha V}{N+\alpha V}=1$: the smoothed estimates remain a probability distribution. It also guarantees that no word has probability 0.

**Q8 (5 marks). Eager versus lazy learners.**

An eager learner builds a global model during training and discards the data (decision trees, naive Bayes, neural networks, SVM); prediction is fast. A lazy learner postpones all work to query time and keeps the data (k-NN, locally weighted regression, case-based reasoning); it adapts to each query but every prediction needs the whole data set, so it is slow and memory hungry for large $N$ and is hurt by irrelevant features.

**Q9 (10 marks). Locally weighted regression.**

*Introduction.* LWR is a lazy method for numeric targets that fits a separate weighted linear model for every query.

*Method.* For a query $q$ compute $w_i=\exp(-(x_i-q)^2/2\tau^2)$, solve $\beta=(A^TWA)^{-1}A^TWy$, and predict $\beta_0+\beta_1q$. The local lines together form a curve that bends with the data.

*Role of $\tau$.* Small $\tau$: few points matter, the curve is flexible and noisy (in our test RMSE 2.233 at $\tau=0.05$). Large $\tau$: all weights similar, the result approaches one global line (0.390 for the global line against 0.063 at $\tau=0.25$). The best $\tau$ is chosen by validation, the bias-variance trade-off.

*Conclusion.* LWR fits non-linear data without choosing a global form, at the price of computation at every query.
