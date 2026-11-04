---
subject: Artificial Intelligence
grade: BCA Semester 5
unit: 4
title: Learning
hours: 4
area: BCA 302 · Artificial Intelligence · Unit 4
---

Writing a rule for every email that might be spam is impossible; letting a program *look at ten thousand labelled emails* and work out the rules itself is routine. That is **machine learning**: improving performance on a task through experience. This unit covers the kinds of learning in the syllabus, then works through the three algorithms most often examined (decision trees, naive Bayes, nearest neighbours) with real numbers, and finishes with the genetic algorithm, which learns by evolution.

::: key What this unit gives you
- Concepts of machine learning: supervised, unsupervised; training, testing, overfitting, evaluation measures.
- Rote learning, learning by analogy, inductive learning, explanation-based learning.
- Decision trees (entropy and information gain), naive Bayes, k-nearest neighbours.
- Learning by evolution: the genetic algorithm.
:::

## 4.1 Concepts of machine learning

A program **learns** from experience E with respect to a task T and performance measure P if its performance at T, measured by P, improves with E (Mitchell). A spam filter's task T is classifying mail, P is accuracy, E is a set of mails labelled by users.

### Kinds of learning

- **Supervised learning**: the training data has inputs and the correct outputs (labels). **Classification** predicts a category (spam or not, digit 0–9); **regression** predicts a number (house price). Examples: decision trees, naive Bayes, k-NN, neural networks.
- **Unsupervised learning**: no labels; find structure: **clustering** (group similar customers), dimensionality reduction, association rules (people who buy A also buy B). Example: k-means.
- **Reinforcement learning**: an agent learns by trial and error from rewards (a game player, a robot).
- **Semi-supervised** learning uses a few labels and many unlabelled examples.

### Training, testing and overfitting

Data is split into a **training set** (fit the model), a **validation set** (choose settings) and a **test set** (final honest estimate). A model that fits the training data very well but does poorly on new data has **overfitted**: it memorised noise. A model too simple to capture the pattern **underfits**. More data, simpler models, regularisation, pruning and **cross-validation** (k folds, each used once for testing) all reduce overfitting.

### Evaluating a classifier

For a binary problem count true positives (TP), false positives (FP), false negatives (FN) and true negatives (TN).

| Measure | Formula | Meaning |
|---|---|---|
| Accuracy | (TP + TN) / total | fraction correct |
| Precision | TP / (TP + FP) | of those called positive, how many are |
| Recall (sensitivity) | TP / (TP + FN) | of the real positives, how many were found |
| F1 | 2 P R / (P + R) | harmonic mean of precision and recall |

With TP = 40, FP = 10, FN = 20 and TN = 130 (200 cases): accuracy 170/200 = **0.85**, precision 40/50 = **0.80**, recall 40/60 = **0.667**, F1 = **0.727**. Accuracy alone misleads when classes are imbalanced: a model that always says "not fraud" is 99.9 % accurate if fraud is 0.1 % of cases and catches none.

## 4.2 Forms of learning in the syllabus

- **Rote learning** stores every input–output pair and looks it up: simple memorisation (a cache; Samuel's checkers program stored board values). It gains speed, not generalisation.
- **Learning by analogy** solves a new problem by adapting the solution of a similar past problem (case-based reasoning): a help-desk system retrieves the nearest earlier case and adapts its fix. The k-NN method below is a simple version.
- **Inductive learning** generalises from examples to a rule that covers unseen cases (learn "is a bird" from many labelled animals). Induction is never certain: the rule can be falsified by one new case, and many rules fit the same data, so a **bias** (prefer simpler hypotheses, Occam's razor) is needed. Decision trees and neural networks are inductive learners.
- **Explanation-based learning (EBL)** uses background knowledge to explain *why* one example works and then generalises the explanation, so a single example can suffice. It needs a correct domain theory and gives speed-up (learning macro-rules).
- **Learning by evolution** (genetic algorithms) searches by simulating natural selection.

## 4.3 Decision trees

A **decision tree** classifies by asking a series of questions: each internal node tests an attribute, each branch is a value and each leaf is a class. The **ID3** algorithm grows the tree greedily, choosing at each node the attribute with the largest **information gain**.

**Entropy** measures impurity: H(S) = −Σ pᵢ log₂ pᵢ (0 for a pure set, 1 bit for a 50/50 binary split). **Information gain** of attribute A is Gain(S, A) = H(S) − Σ (|S_v|/|S|) H(S_v).

::: example PlayTennis
The standard 14-day data set: 9 days Yes and 5 days No, so H(S) = −(9/14) log₂(9/14) − (5/14) log₂(5/14) = **0.940**. The attributes are Outlook (Sunny, Overcast, Rain), Temperature, Humidity and Wind. Information gains:

| Attribute | Gain |
|---|---|
| Outlook | **0.247** |
| Humidity | 0.152 |
| Wind | 0.048 |
| Temperature | 0.029 |

Outlook has the highest gain, so it is the root. The Overcast branch is pure (always Yes, 4 days) and becomes a leaf; the Sunny branch is split by Humidity (High → No, Normal → Yes) and the Rain branch by Wind (Weak → Yes, Strong → No). **C4.5** improves on ID3 with the gain *ratio*, continuous attributes and pruning; **CART** uses the Gini index. Trees are easy to read but overfit unless they are pruned or combined into **random forests**.
:::

## 4.4 Naive Bayes

Naive Bayes classifies by Bayes' rule with a strong simplifying assumption: given the class, the attributes are **independent**. The class chosen is the one maximising **P(C) Π P(xᵢ | C)**. It is fast, needs little data and works well for text.

::: example PlayTennis again: Sunny, Cool, High, Strong
Priors: P(Yes) = 9/14, P(No) = 5/14. From the table:

| Attribute value | P(· | Yes) | P(· | No) |
|---|---|---|
| Outlook = Sunny | 2/9 | 3/5 |
| Temperature = Cool | 3/9 | 1/5 |
| Humidity = High | 3/9 | 4/5 |
| Wind = Strong | 3/9 | 3/5 |

Score(Yes) = 9/14 × 2/9 × 3/9 × 3/9 × 3/9 = **0.0053**. Score(No) = 5/14 × 3/5 × 1/5 × 4/5 × 3/5 = **0.0206**. Normalising: P(No | x) = 0.0206 / (0.0053 + 0.0206) = **0.795**, P(Yes | x) = 0.205. The prediction is **No** (do not play).
:::

### The zero-frequency problem and Laplace smoothing

If an attribute value never occurred with a class in training, its estimated probability is 0 and wipes out the whole product. **Laplace (add-one) smoothing** uses (count + 1) / (class total + number of possible values).

::: example A tiny spam filter
Training messages: spam: "buy cheap pills now", "cheap pills cheap"; ham: "meeting at noon", "lunch meeting now", "project report due". The vocabulary has 11 distinct words. Spam contains 7 words, ham 9 words. For the message "cheap pills": P(cheap | spam) = (3 + 1)/(7 + 11) = 4/18, P(pills | spam) = (2 + 1)/18 = 3/18 and P(spam) = 2/5, so the spam score is 2/5 × 4/18 × 3/18 = 0.0148. Neither word occurs in ham, so each gets (0 + 1)/(9 + 11) = 1/20 and the ham score is 3/5 × 1/20 × 1/20 = 0.0015. Normalised, P(spam | "cheap pills") = **0.908**. For "cheap meeting now" the two scores are 0.000549 (spam) and 0.00045 (ham), so P(spam) = **0.549**: a close call, since the message mixes spammy and hammy words.
:::

The program below recomputes these figures; without smoothing the ham score for "cheap pills" would have been exactly 0, which is the zero-frequency problem in action.

## 4.5 k-nearest neighbours

**k-NN** is a lazy, instance-based learner: to classify a point, find the k training points closest to it (usually Euclidean distance) and take a majority vote. No training phase; all work is at query time. Features must be **scaled** (otherwise income in rupees dominates age in years); k is chosen by validation (small k: noisy; large k: blurred boundaries; odd k avoids ties in two-class problems).

::: example
Training points: A at (1, 1) and (2, 1); B at (4, 4), (5, 4), (4, 5). Query q = (3, 3). Distances: to (4, 4) it is √2 = 1.414 (B); to (2, 1), (5, 4) and (4, 5) it is √5 = 2.236 (A, B, B); to (1, 1) it is √8 = 2.828 (A). With k = 1 the answer is B; with k = 5 (all points) the vote is 3 B to 2 A, again B.
:::

## 4.6 Clustering (unsupervised)

**k-means** groups n points into k clusters: pick k initial centres; assign each point to the nearest centre; move each centre to the mean of its points; repeat until nothing changes. It minimises within-cluster squared distance, depends on the initial centres (run several times), needs k in advance and finds round clusters. Hierarchical clustering builds a tree of merges (dendrogram).

## 4.7 Learning by evolution: genetic algorithms

A **genetic algorithm (GA)** keeps a **population** of candidate solutions (chromosomes, often bit strings) and improves it over **generations**:

1. **Initialise** a random population.
2. **Evaluate** the **fitness** of each individual.
3. **Select** parents with probability related to fitness (roulette wheel, tournament).
4. **Crossover**: swap parts of two parents (single-point: choose a cut and exchange tails) to make children.
5. **Mutation**: flip each bit with a small probability, preserving diversity.
6. **Replace** the population and repeat until the fitness is good enough or time runs out.

Crossover of 11100|011 and 00011|110 at the cut after bit 5 gives 11100110 and 00011011. GAs suit hard optimisation problems with a poorly understood landscape (timetables, circuit design, neural network structure). The **schema theorem** explains why short, fit building blocks multiply. Weaknesses: many fitness evaluations, no guarantee of the optimum, sensitive to the encoding.

## Practising the commands

The first program recomputes the entropy, the gains, the naive Bayes scores (with and without smoothing), the spam filter, k-NN distances and the evaluation measures.

```python
import math
data = [("Sunny","Hot","High","Weak","No"),("Sunny","Hot","High","Strong","No"),("Overcast","Hot","High","Weak","Yes"),("Rain","Mild","High","Weak","Yes"),("Rain","Cool","Normal","Weak","Yes"),("Rain","Cool","Normal","Strong","No"),("Overcast","Cool","Normal","Strong","Yes"),("Sunny","Mild","High","Weak","No"),("Sunny","Cool","Normal","Weak","Yes"),("Rain","Mild","Normal","Weak","Yes"),("Sunny","Mild","Normal","Strong","Yes"),("Overcast","Mild","High","Strong","Yes"),("Overcast","Hot","Normal","Weak","Yes"),("Rain","Mild","High","Strong","No")]
names = ["Outlook", "Temperature", "Humidity", "Wind"]
H = lambda ps: -sum(p * math.log2(p) for p in ps if p)
yes = sum(r[-1] == "Yes" for r in data); HS = H([yes / 14, 1 - yes / 14]); print("entropy %.3f" % HS)
for i, n in enumerate(names):
    g = HS
    for v in {r[i] for r in data}:
        sub = [r for r in data if r[i] == v]; y = sum(r[-1] == "Yes" for r in sub)
        g -= len(sub) / 14 * H([y / len(sub), 1 - y / len(sub)])
    print("gain", n, round(g, 3))
x = ("Sunny", "Cool", "High", "Strong"); sc = {}
for c, nc in (("Yes", 9), ("No", 5)):
    p = nc / 14
    for i, v in enumerate(x): p *= sum(1 for r in data if r[-1] == c and r[i] == v) / nc
    sc[c] = p
docs = [("buy cheap pills now", "spam"), ("cheap pills cheap", "spam"), ("meeting at noon", "ham"), ("lunch meeting now", "ham"), ("project report due", "ham")]
vocab = {w for d, _ in docs for w in d.split()}; print("vocabulary", len(vocab))
def spam(msg):
    out = {}
    for c in ("spam", "ham"):
        words = [w for d, k in docs if k == c for w in d.split()]; p = sum(k == c for _, k in docs) / len(docs)
        for w in msg.split(): p *= (words.count(w) + 1) / (len(words) + len(vocab))
        out[c] = p
    return {k: round(v, 5) for k, v in out.items()}, round(out["spam"] / sum(out.values()), 3)
pts = [((1, 1), "A"), ((2, 1), "A"), ((4, 4), "B"), ((5, 4), "B"), ((4, 5), "B")]
TP, FP, FN, TN = 40, 10, 20, 130; P_, R_ = TP / (TP + FP), TP / (TP + FN)
```
```output
entropy 0.940
gain Outlook 0.247
gain Temperature 0.029
gain Humidity 0.152
gain Wind 0.048
scores {'Yes': 0.0053, 'No': 0.0206} P(No|x) = 0.795
vocabulary 11
({'spam': 0.01481, 'ham': 0.0015}, 0.908)
({'spam': 0.00055, 'ham': 0.00045}, 0.549)
[(1.414, 'B'), (2.236, 'A'), (2.236, 'B'), (2.236, 'B'), (2.828, 'A')]
accuracy 0.85 precision 0.80 recall 0.667 F1 0.727
```
The second program is a small genetic algorithm that evolves a 12-bit string of all ones ("one-max"), with a fixed random seed so that the run is reproducible.

```python
import random
rnd = random.Random(4); N, L, GENS = 6, 12, 12
fit = lambda c: sum(c)
pop = [[rnd.randint(0, 1) for _ in range(L)] for _ in range(N)]
def pick(pop):
    a, b = rnd.sample(pop, 2); return a if fit(a) >= fit(b) else b
for g in range(GENS + 1):
    best = max(pop, key=fit); print("gen", g, "best fitness", fit(best), "mean %.2f" % (sum(map(fit, pop)) / N))
    if fit(best) == L: break
    new = [best[:]]
    while len(new) < N:
        p1, p2 = pick(pop), pick(pop); cut = rnd.randint(1, L - 1)
        child = p1[:cut] + p2[cut:]
        child = [b ^ 1 if rnd.random() < 0.05 else b for b in child]; new.append(child)
    pop = new
```
```output
gen 0 best fitness 8 mean 6.33
gen 1 best fitness 9 mean 7.00
gen 2 best fitness 9 mean 8.00
gen 3 best fitness 9 mean 8.67
gen 4 best fitness 10 mean 9.17
gen 5 best fitness 10 mean 8.83
gen 6 best fitness 10 mean 9.00
gen 7 best fitness 10 mean 8.50
gen 8 best fitness 10 mean 9.17
gen 9 best fitness 10 mean 9.00
gen 10 best fitness 10 mean 9.50
gen 11 best fitness 10 mean 9.50
gen 12 best fitness 11 mean 9.83
crossover example: 11100110 00011011
```
With only six individuals and twelve generations the run above reaches 11 of the 12 ones, not all 12: a GA is a stochastic search with no guarantee of the optimum within a fixed budget, and a larger population or more generations would be needed (the best individual is copied unchanged each generation, so the best fitness never falls).

## 4.8 Seeing the ideas: pioneers, flowers, evolution and the algorithms

Machine learning is easiest to remember when each algorithm is tied to a picture and to numbers you can check. Plate 4.1 shows the people and machines behind learning from experience. Plate 4.2 shows the three iris flowers of the most famous data set in the field. Plate 4.3 gives an everyday object for spam, clustering and the Overcast branch of the tennis tree. Plate 4.4 collects the natural and engineered examples behind genetic algorithms. The figures after the plates are computed in the figure code itself, so every number printed in a caption is the number the program produced.

```photogrid label="4.1" cols="4" ratio="1.0" caption="Four roots of learning from experience. (a) The operator console of an IBM 701 (CC BY 2.0): Arthur Samuel wrote a checkers program for this machine in the early 1950s that improved by playing against itself, and in 1959 he called the field machine learning. (b) Ronald Fisher as a young man (public domain), who in 1936 published the iris measurements used in Plate 4.2 to show that flowers can be classified from their petals. (c) A drawing of Pavlov's apparatus for conditioned reflexes (CC BY 4.0, Wellcome Collection): behaviour changes after a signal is repeatedly paired with a result. (d) Thorndike's puzzle box and a learning curve (public domain): a cat needs several hundred seconds to escape at first and under about 100 seconds after many trials, the trial-and-error pattern that reinforcement learning copies."
@ photo id="bca302/ibm701" cap="IBM 701 console: Samuel's checkers learner"
fit 1.0
focus 0.5 0.55
@ photo id="bca302/fisher" cap="Ronald Fisher: the iris data (1936)"
fit 1.0
focus 0.5 0.6
@ photo id="bca302/pavlov" cap="Pavlov's apparatus: learning by association"
fit 1.0
focus 0.35 0.5
@ photo id="bca302/puzzlebox" cap="Thorndike's puzzle box: trial and error"
fit 1.0
focus 0.5 0.5
```

```svgfig label="4.1" caption="The three kinds of learning. Supervised learning is given inputs with correct labels and learns the map from input to output (classification gives a category, regression a number). Unsupervised learning has no labels and finds structure such as clusters. Reinforcement learning has an agent act in a world and learn from a reward signal. Semi-supervised learning sits between the first two, with a few labels and many unlabelled examples."
f = Fig(580, 232)
cm = __import__("math")
cols = [("Supervised", 8, TEAL), ("Unsupervised", 198, AMBER), ("Reinforcement", 388, RED)]
for t, x, c in cols:
    f.box(x, 6, 184, 220, "", fill="#ffffff", stroke=c, r=8, sw=1.6)
    f.text(x + 92, 24, t, size=13, color=c, bold=True)
# supervised: labelled points with a boundary
import_pts = [(30, 70, 0), (48, 90, 0), (40, 108, 0), (66, 78, 0), (60, 100, 0), (120, 72, 1), (140, 92, 1), (128, 110, 1), (152, 76, 1), (104, 98, 1)]
for px, py, k in import_pts:
    f.circle(8 + px + 4, 36 + py - 50 + 10, 6, fill=MINT if k == 0 else SAND, stroke=TEAL if k == 0 else AMBER, sw=1.5)
f.line(8 + 92, 46, 8 + 80, 130, color=NAVY, sw=2, dash=True)
f.text(100, 142, "labels: spam / not spam", size=10, color=SLATE)
f.text(100, 164, "learn the map  x -> y", size=11, color=NAVY, bold=True)
f.text(100, 184, "classification: a category", size=10, color=SLATE)
f.text(100, 198, "regression: a number", size=10, color=SLATE)
f.text(100, 214, "tree, naive Bayes, k-NN", size=10, color=TEAL, bold=True)
# unsupervised: two blobs, no labels
rng = __import__("random").Random(4)
for cx, cy in [(250, 82), (330, 104)]:
    f.raw('<ellipse cx="%d" cy="%d" rx="42" ry="30" fill="none" stroke="#b45309" stroke-width="1.4" stroke-dasharray="5 3"/>' % (cx, cy))
    for _ in range(7):
        f.circle(round(cx + rng.uniform(-34, 34)), round(cy + rng.uniform(-22, 22)), 5, fill="#e2e8f0", stroke=SLATE, sw=1.3)
f.text(290, 142, "no labels at all", size=10, color=SLATE)
f.text(290, 164, "find the structure", size=11, color=NAVY, bold=True)
f.text(290, 184, "clusters, associations,", size=10, color=SLATE)
f.text(290, 198, "dimensionality reduction", size=10, color=SLATE)
f.text(290, 214, "k-means, hierarchical", size=10, color=AMBER, bold=True)
# reinforcement: agent / environment loop
f.box(412, 44, 60, 34, "agent", fill=MINT, stroke=TEAL, size=11, bold=True)
f.box(492, 44, 70, 34, "world", fill=SAND, stroke=AMBER, size=11, bold=True)
f.arrow([(472, 52), (492, 52)], color=NAVY, label="act", lpos=(482, 45), lsize=9.5)
f.arrow([(492, 72), (472, 72)], color=NAVY)
f.text(482, 92, "state, reward", size=9.5, color=RED, bold=True)
f.box(412, 104, 150, 26, "reward +1 / -1 after moves", fill=ROSE, stroke=RED, size=9.5)
f.text(480, 148, "learn by trial and error", size=11, color=NAVY, bold=True)
f.text(480, 168, "maximise the total reward", size=10, color=SLATE)
f.text(480, 184, "game player, robot, bidding", size=10, color=SLATE)
f.text(480, 214, "Q-learning, policy gradient", size=10, color=RED, bold=True)
```

```svgfig label="4.2" caption="The four forms of learning in the syllabus. Rote learning stores answers, analogy reuses the solution of a similar case, inductive learning generalises from many examples to a rule, and explanation-based learning explains why a single example works using a domain theory and turns the explanation into a general macro-rule. Each card gives a toy example, where it is used and its main limit."
f = Fig(580, 250)
cards = [("Rote learning", TEAL, MINT, "store every pair, look it up", "board 17 -> value 0.3\nboard 18 -> value -0.1", "Samuel's checkers; a cache", "speed, no generalising"),
         ("Learning by analogy", AMBER, SAND, "adapt the solution of a similar case", "new fault ~ case 212\nreuse its fix, then adjust", "help desk; k-NN", "needs a good similarity"),
         ("Inductive learning", NAVY, BLUE, "generalise from examples to a rule", "10 labelled birds\n-> rule: has feathers", "trees, neural nets", "never certain; needs bias"),
         ("Explanation-based", RED, ROSE, "explain WHY one example works", "1 example + domain theory\n-> a general macro-rule", "chess forks, planners", "needs a correct theory")]
for i, (t, c, fl, d1, ex, uses, lim) in enumerate(cards):
    x = 6 + (i % 2) * 288; y = 6 + (i // 2) * 124
    f.box(x, y, 280, 116, "", fill=fl, stroke=c, r=8, sw=1.6)
    f.text(x + 140, y + 17, t, size=12.5, color=c, bold=True)
    f.text(x + 140, y + 35, d1, size=10, color=SLATE)
    f.box(x + 40, y + 44, 200, 34, ex, fill="#ffffff", stroke=c, size=9.5, r=5, color=NAVY)
    f.text(x + 140, y + 94, "used in: " + uses, size=9.5, color=NAVY, bold=True)
    f.text(x + 140, y + 108, "limit: " + lim, size=9.5, color=SLATE)
```

```photogrid label="4.2" cols="3" ratio="1.0" caption="The three classes of Fisher's iris data. (a) A flower labelled Iris setosa (CC BY-SA 4.0). (b) Iris versicolor (CC BY-SA 4.0). (c) Iris virginica (CC BY-SA 2.0). Fisher measured 50 flowers of each species. The petal length separates setosa (about 1.0 to 1.9 cm) from the other two almost perfectly, while versicolor (about 3.0 to 5.1 cm) and virginica (about 4.5 to 6.9 cm) overlap, which is why a classifier makes mistakes only between those two. Figures 4.8 and 4.9 use 30 of the real measurements."
@ photo id="bca302/irisset" cap="Iris setosa: short petals, easy to separate"
fit 1.0
focus 0.5 0.55
@ photo id="bca302/irisver" cap="Iris versicolor: medium petals"
fit 1.0
focus 0.5 0.5
@ photo id="bca302/irisvir" cap="Iris virginica: long petals, overlaps versicolor"
fit 1.0
focus 0.5 0.5
```

```svgfig label="4.3" caption="Overfitting computed. Twelve noisy points were drawn from a sine curve (noise 0.25) and polynomials of degree 1 to 10 were fitted. The training error falls steadily from 0.362 at degree 1 to 0.042 at degree 10, but the error on 60 new points is smallest at degree 3 (0.311) and then grows: 0.478 at degree 4, 1.107 at degree 5 and 998.9 at degree 10. A model that memorises the 12 points is useless on new ones."
f = Fig(580, 284)
np = __import__("numpy")
rng = np.random.default_rng(3)
def truth(x): return np.sin(2 * np.pi * x)
xt = np.sort(rng.uniform(0, 1, 12)); yt = truth(xt) + rng.normal(0, 0.25, 12)
xs = rng.uniform(0, 1, 60); ys = truth(xs) + rng.normal(0, 0.25, 60)
fits = {d: np.polyfit(xt, yt, d) for d in range(1, 11)}
def rmse(d, x, y): return float(np.sqrt(np.mean((np.polyval(fits[d], x) - y) ** 2)))
tr = {d: rmse(d, xt, yt) for d in fits}; te = {d: rmse(d, xs, ys) for d in fits}
best = min(te, key=te.get)
assert tr[10] < tr[1] and te[10] > te[best] and te[1] > te[best]
f.text(150, 14, "three models, the same 12 points", size=11.5, color=NAVY, bold=True)
a = Axes(f, 30, 24, 250, 184, (0, 1), (-1.8, 1.8)); a.grid(0.25, 0.9).axes("x", "y")
a.curve(truth, color="#94a3b8", dash=True, sw=1.6)
a.curve(lambda x: float(np.polyval(fits[1], x)), color=AMBER, sw=2)
a.curve(lambda x: float(np.polyval(fits[3], x)), color=TEAL, sw=2.4)
a.curve(lambda x: float(np.polyval(fits[10], x)), color=RED, sw=2)
for x, y in zip(xt, yt): a.pt(float(x), float(y), r=3.6, color=NAVY)
f.text(150, 246, "degree 1 underfits", size=10, color=AMBER, bold=True)
f.text(150, 259, "degree 3 fits well", size=10, color=TEAL, bold=True)
f.text(150, 272, "degree 10 memorises noise", size=10, color=RED, bold=True)
f.text(430, 14, "error on training vs new data (RMSE)", size=11.5, color=NAVY, bold=True)
b = Axes(f, 330, 24, 236, 184, (0.5, 10.5), (0, 1.0)); b.grid(1, 0.25).axes("", "")
b.curve(lambda x: tr[min(10, max(1, round(x)))], 1, 10, color=TEAL, n=9, sw=2.4)
b.curve(lambda x: min(1.0, te[min(10, max(1, round(x)))]), 1, 10, color=RED, n=9, sw=2.4)
for d in range(1, 11): b.pt(d, tr[d], r=3, color=TEAL); b.pt(d, min(1.0, te[d]), r=3, color=RED)
b.vline(best, color=NAVY)
f.text(446, 246, "teal: training error keeps falling", size=10, color=TEAL, bold=True)
f.text(446, 259, "red: test error rises again (clipped at 1.0)", size=10, color=RED, bold=True)
f.text(446, 272, "best degree on test data: %d" % best, size=10, color=NAVY, bold=True)
```

```svgfig label="4.4" caption="Evaluation measures. Left: the confusion matrix of the worked example with 200 cases gives accuracy 0.85, precision 0.80, recall 0.667 and F1 0.727. Right: with 10 frauds in 10,000 payments, a model that always says not fraud is 99.90 percent accurate and catches nothing, while a real detector with 8 true positives and 40 false positives has accuracy 99.58 percent and recall 0.80. Accuracy alone hides the failure when classes are rare."
f = Fig(580, 250)
TP, FP, FN, TN = 40, 10, 20, 130
n = TP + FP + FN + TN
acc = (TP + TN) / n; pre = TP / (TP + FP); rec = TP / (TP + FN); f1 = 2 * pre * rec / (pre + rec)
assert (round(acc, 2), round(pre, 2), round(rec, 3), round(f1, 3)) == (0.85, 0.8, 0.667, 0.727)
f.text(130, 14, "confusion matrix (200 cases)", size=11.5, color=NAVY, bold=True)
f.text(130, 34, "predicted positive          predicted negative", size=9.5, color=SLATE, bold=True)
cells = [("TP = %d" % TP, "found", 40, 44, MINT, TEAL), ("FN = %d" % FN, "missed", 130, 44, ROSE, RED),
         ("FP = %d" % FP, "false alarm", 40, 114, SAND, AMBER), ("TN = %d" % TN, "correct no", 130, 114, BLUE, NAVY)]
for t, s, x, y, fl, c in cells:
    f.box(x, y, 86, 64, "", fill=fl, stroke=c, r=6, sw=1.6)
    f.text(x + 43, y + 26, t, size=13, color=c, bold=True)
    f.text(x + 43, y + 46, s, size=10, color=SLATE)
f.text(20, 108, "real +", size=9.5, color=SLATE, bold=True, anchor="middle")
f.text(20, 178, "real -", size=9.5, color=SLATE, bold=True, anchor="middle")
f.text(130, 196, "accuracy = (TP+TN)/N = %.2f" % acc, size=10.5, color=NAVY, bold=True)
f.text(130, 212, "precision = TP/(TP+FP) = %.2f" % pre, size=10.5, color=TEAL, bold=True)
f.text(130, 228, "recall = TP/(TP+FN) = %.3f" % rec, size=10.5, color=RED, bold=True)
f.text(130, 244, "F1 = 2PR/(P+R) = %.3f" % f1, size=10.5, color=AMBER, bold=True)
# imbalance: 1000 payments, 1 fraud
f.text(430, 14, "why accuracy misleads: 10,000 payments, 10 frauds", size=11.5, color=NAVY, bold=True)
N, P = 10000, 10
a_acc = (N - P) / N
b_tp, b_fp = 8, 40; b_fn = P - b_tp; b_tn = N - P - b_fp
b_acc = (b_tp + b_tn) / N; b_pre = b_tp / (b_tp + b_fp); b_rec = b_tp / P
rows = [("Model A: always says  'not fraud'", "accuracy %.2f %%" % (a_acc * 100), "recall 0 of 10 caught", AMBER, SAND),
        ("Model B: real detector (TP 8, FP 40)", "accuracy %.2f %%" % (b_acc * 100), "recall %d of 10 caught, precision %.2f" % (b_tp, b_pre), TEAL, MINT)]
for i, (t, a1, a2, c, fl) in enumerate(rows):
    y = 30 + i * 100
    f.box(300, y, 270, 90, "", fill=fl, stroke=c, r=8, sw=1.6)
    f.text(435, y + 18, t, size=10.5, color=c, bold=True)
    f.text(435, y + 42, a1, size=15, color=NAVY, bold=True)
    f.text(435, y + 62, a2, size=10.5, color=RED if i == 0 else TEAL, bold=True)
    f.text(435, y + 79, "lower accuracy, far more useful" if i == 1 else "99.90 % and useless", size=9.5, color=SLATE)
f.text(435, 238, "Use precision, recall and F1 when classes are rare.", size=10, color=NAVY, bold=True)
```

```photogrid label="4.3" cols="3" ratio="1.0" caption="Everyday objects for three ideas. (a) Shelves of canned Spam (CC BY-SA 4.0): a Monty Python sketch about the tinned meat gave unwanted e-mail its name, and the naive Bayes filter of Fig. 4.7 was one of the first defences against it. (b) A vegetable seller at Asan Bazaar, Kathmandu (CC BY-SA 4.0): the potatoes, garlic, onions and ginger form natural groups that nobody labelled, which is what clustering finds from the data alone. (c) An overcast sky (CC BY 4.0): in the PlayTennis data every one of the 4 Overcast days is a Yes, so the Overcast branch of the tree in Fig. 4.6 is a pure leaf."
@ photo id="bca302/spamtin" cap="Spam tins: the origin of the word"
fit 1.0
focus 0.5 0.55
@ photo id="bca302/asanveg" cap="Asan Bazaar: natural clusters"
fit 1.0
focus 0.4 0.4
@ photo id="bca302/overcast" cap="Overcast: a pure branch"
fit 1.0
focus 0.5 0.5
```

```svgfig label="4.5" caption="Entropy and information gain computed from the 14 PlayTennis rows. The curve is H(p), which is 0 for a pure set, 1 bit for an even mix, and 0.940 bits for 9 Yes and 5 No. The bars are the information gains of the four attributes: Outlook 0.247, Humidity 0.152, Wind 0.048 and Temperature 0.029, so Outlook is the root."
f = Fig(580, 262)
cm = __import__("math")
D = [("Sunny","Hot","High","Weak","No"),("Sunny","Hot","High","Strong","No"),("Overcast","Hot","High","Weak","Yes"),("Rain","Mild","High","Weak","Yes"),("Rain","Cool","Normal","Weak","Yes"),("Rain","Cool","Normal","Strong","No"),("Overcast","Cool","Normal","Strong","Yes"),("Sunny","Mild","High","Weak","No"),("Sunny","Cool","Normal","Weak","Yes"),("Rain","Mild","Normal","Weak","Yes"),("Sunny","Mild","Normal","Strong","Yes"),("Overcast","Mild","High","Strong","Yes"),("Overcast","Hot","Normal","Weak","Yes"),("Rain","Mild","High","Strong","No")]
def H(rows):
    n = len(rows); y = sum(1 for r in rows if r[-1] == "Yes")
    return -sum(p * cm.log2(p) for p in (y / n, (n - y) / n) if p > 0)
def gain(rows, a):
    g = H(rows)
    for v in set(r[a] for r in rows):
        s = [r for r in rows if r[a] == v]; g -= len(s) / len(rows) * H(s)
    return g
names = ["Outlook", "Temperature", "Humidity", "Wind"]
G = {names[a]: gain(D, a) for a in range(4)}
assert round(H(D), 3) == 0.940 and [round(G[k], 3) for k in names] == [0.247, 0.029, 0.152, 0.048]
f.text(140, 14, "entropy of a yes/no set", size=11.5, color=NAVY, bold=True)
a = Axes(f, 34, 24, 240, 170, (0, 1), (0, 1.1)); a.grid(0.25, 0.25).axes("p", "H")
a.curve(lambda p: -(p * cm.log2(p) + (1 - p) * cm.log2(1 - p)), 0.001, 0.999, color=TEAL, sw=2.6)
a.pt(9 / 14, H(D), "9 Yes, 5 No: %.3f" % H(D), color=RED, dx=10, dy=-4, anchor="start")
a.pt(0.5, 1.0, "50/50: 1 bit", color=NAVY, dx=-8, dy=-8, anchor="end")
a.pt(1.0, 0.0, "", color=AMBER, r=3); a.pt(0.0, 0.0, "pure: 0", color=AMBER, dx=8, dy=-8)
f.text(154, 232, "p = share of Yes; pure set = 0 bits, even mix = 1 bit", size=10, color=SLATE)
f.text(154, 247, "gain = entropy before - weighted entropy after", size=10, color=SLATE)
f.text(430, 14, "information gain of each attribute", size=11.5, color=NAVY, bold=True)
order = sorted(names, key=lambda k: -G[k])
for i, k in enumerate(order):
    y = 34 + i * 44
    f.text(300, y + 18, k, size=11, color=NAVY, bold=True, anchor="start")
    w = G[k] / 0.25 * 130
    f.box(386, y + 4, round(w), 24, "", fill=MINT if i == 0 else BLUE, stroke=TEAL if i == 0 else NAVY, r=4)
    f.text(386 + round(w) + 6, y + 17, "%.3f" % G[k], size=11, color=RED if i == 0 else SLATE, bold=True, anchor="start", vmid=True)
f.box(300, 212, 270, 36, "Outlook has the largest gain,\nso it becomes the root of the tree", fill=SAND, stroke=AMBER, size=10, r=6, color=NAVY, bold=True)
```

```svgfig label="4.6" caption="The decision tree produced by running ID3 on the 14 rows (the program checks the shape before drawing it). Outlook is the root with 9 Yes and 5 No. Overcast is a pure leaf of 4 Yes. Sunny (2 Yes, 3 No) is split by Humidity and Rain (3 Yes, 2 No) by Wind, and every leaf is then pure. The new day Sunny, Cool, High, Strong follows Sunny then High and is classified No."
f = Fig(580, 270)
D = [("Sunny","Hot","High","Weak","No"),("Sunny","Hot","High","Strong","No"),("Overcast","Hot","High","Weak","Yes"),("Rain","Mild","High","Weak","Yes"),("Rain","Cool","Normal","Weak","Yes"),("Rain","Cool","Normal","Strong","No"),("Overcast","Cool","Normal","Strong","Yes"),("Sunny","Mild","High","Weak","No"),("Sunny","Cool","Normal","Weak","Yes"),("Rain","Mild","Normal","Weak","Yes"),("Sunny","Mild","Normal","Strong","Yes"),("Overcast","Mild","High","Strong","Yes"),("Overcast","Hot","Normal","Weak","Yes"),("Rain","Mild","High","Strong","No")]
cm = __import__("math")
AT = ["Outlook", "Temperature", "Humidity", "Wind"]
def H(rows):
    n = len(rows); y = sum(1 for r in rows if r[-1] == "Yes")
    return -sum(p * cm.log2(p) for p in (y / n, (n - y) / n) if p > 0)
def gain(rows, a):
    return H(rows) - sum(len(s) / len(rows) * H(s) for v in set(r[a] for r in rows) for s in [[r for r in rows if r[a] == v]])
def id3(rows, avail):
    labs = set(r[-1] for r in rows)
    if len(labs) == 1: return labs.pop()
    a = max(avail, key=lambda i: gain(rows, i))
    return (AT[a], {v: id3([r for r in rows if r[a] == v], [i for i in avail if i != a]) for v in sorted(set(r[a] for r in rows))})
T = id3(D, [0, 1, 2, 3])
assert T[0] == "Outlook" and T[1]["Overcast"] == "Yes" and T[1]["Sunny"][0] == "Humidity" and T[1]["Rain"][0] == "Wind"
assert T[1]["Sunny"][1] == {"High": "No", "Normal": "Yes"} and T[1]["Rain"][1] == {"Strong": "No", "Weak": "Yes"}
def counts(rows): return "%dY %dN" % (sum(r[-1] == "Yes" for r in rows), sum(r[-1] == "No" for r in rows))
def node(x, y, t, sub, c=NAVY, fl=BLUE):
    f.box(x - 52, y, 104, 40, t + "\n" + sub, fill=fl, stroke=c, size=10.5, bold=True, r=8, color=NAVY)
def leaf(x, y, yes, sub):
    f.box(x - 38, y, 76, 36, ("PLAY" if yes else "STAY IN") + "\n" + sub, fill=MINT if yes else ROSE, stroke=TEAL if yes else RED, size=10, bold=True, r=18, color=NAVY)
node(290, 8, "Outlook", counts(D))
S = [r for r in D if r[0] == "Sunny"]; O = [r for r in D if r[0] == "Overcast"]; R = [r for r in D if r[0] == "Rain"]
node(110, 108, "Humidity", counts(S)); leaf(290, 112, True, counts(O)); node(470, 108, "Wind", counts(R))
f.arrow([(250, 48), (130, 108)], color=SLATE); f.text(168, 70, "Sunny", size=10.5, color=AMBER, bold=True)
f.arrow([(290, 48), (290, 112)], color=SLATE); f.text(318, 84, "Overcast", size=10.5, color=AMBER, bold=True)
f.arrow([(330, 48), (450, 108)], color=SLATE); f.text(430, 70, "Rain", size=10.5, color=AMBER, bold=True)
for x, sub, kids in [(110, S, T[1]["Sunny"][1]), (470, R, T[1]["Rain"][1])]:
    attr = 2 if x == 110 else 3
    for j, (v, lab) in enumerate(sorted(kids.items())):
        lx = x - 70 + j * 140
        rows = [r for r in sub if r[attr] == v]
        f.arrow([(x + (-14 if j == 0 else 14), 148), (lx, 196)], color=SLATE)
        f.text(lx + (-26 if j == 0 else 26), 168, v, size=10.5, color=AMBER, bold=True)
        leaf(lx, 198, lab == "Yes", counts(rows))
f.text(290, 252, "Classify (Sunny, Cool, High, Strong): Outlook = Sunny, Humidity = High -> STAY IN (No)", size=10.5, color=NAVY, bold=True)
```

```svgfig label="4.7" caption="Naive Bayes computed with exact fractions. Left: the table for Sunny, Cool, High, Strong multiplies down each column to give score Yes 0.0053 and score No 0.0206, so P(No) = 0.795. Right: the tiny spam filter with Laplace smoothing (vocabulary of 11 words) gives P(spam) = 0.908 for the message cheap pills and only 0.549 for cheap meeting now. Without the add-one rule the ham score of cheap pills would be exactly 0."
f = Fig(580, 312)
fr = __import__("fractions").Fraction
D = [("Sunny","Hot","High","Weak","No"),("Sunny","Hot","High","Strong","No"),("Overcast","Hot","High","Weak","Yes"),("Rain","Mild","High","Weak","Yes"),("Rain","Cool","Normal","Weak","Yes"),("Rain","Cool","Normal","Strong","No"),("Overcast","Cool","Normal","Strong","Yes"),("Sunny","Mild","High","Weak","No"),("Sunny","Cool","Normal","Weak","Yes"),("Rain","Mild","Normal","Weak","Yes"),("Sunny","Mild","Normal","Strong","Yes"),("Overcast","Mild","High","Strong","Yes"),("Overcast","Hot","Normal","Weak","Yes"),("Rain","Mild","High","Strong","No")]
q = [(0, "Sunny", "Outlook"), (1, "Cool", "Temperature"), (2, "High", "Humidity"), (3, "Strong", "Wind")]
Y = [r for r in D if r[-1] == "Yes"]; N = [r for r in D if r[-1] == "No"]
sy = fr(len(Y), 14); sn = fr(len(N), 14)
rows = []
for i, v, nm in q:
    rows.append((nm + " = " + v, fr(sum(r[i] == v for r in Y), len(Y)), fr(sum(r[i] == v for r in N), len(N))))
for r in rows: sy *= r[1]; sn *= r[2]
post_no = float(sn / (sy + sn))
assert (round(float(sy), 4), round(float(sn), 4), round(post_no, 3)) == (0.0053, 0.0206, 0.795)
f.text(140, 14, "playing tennis? Sunny, Cool, High, Strong", size=11, color=NAVY, bold=True)
f.text(112, 38, "evidence", size=10, color=SLATE, bold=True); f.text(188, 38, "Yes", size=10, color=TEAL, bold=True); f.text(250, 38, "No", size=10, color=RED, bold=True)
f.box(10, 44, 262, 28, "prior  P(class)", fill=SOFT, stroke="#94a3b8", size=10, r=4, anchor="start", color=NAVY)
f.text(188, 58, "9/14", size=11, color=TEAL, bold=True); f.text(250, 58, "5/14", size=11, color=RED, bold=True)
for i, (t, a, b) in enumerate(rows):
    y = 76 + i * 32
    f.box(10, y, 262, 28, t, fill=BLUE, stroke=NAVY, size=10, r=4, anchor="start", color=NAVY)
    f.text(188, y + 14, "%d/%d" % (a.numerator, a.denominator), size=11, color=TEAL, bold=True, vmid=True)
    f.text(250, y + 14, "%d/%d" % (b.numerator, b.denominator), size=11, color=RED, bold=True, vmid=True)
f.text(140, 214, "multiply down each column", size=10, color=SLATE)
mx = max(float(sy), float(sn))
for k, (nm, v, c, fl) in enumerate([("score Yes", float(sy), TEAL, MINT), ("score No", float(sn), RED, ROSE)]):
    y = 224 + k * 30
    f.text(10, y + 12, nm, size=10.5, color=c, bold=True, anchor="start", vmid=True)
    w = round(v / mx * 120)
    f.box(86, y, w, 22, "", fill=fl, stroke=c, r=4)
    f.text(86 + w + 6, y + 11, "%.4f" % v, size=11, color=NAVY, bold=True, anchor="start", vmid=True)
f.text(140, 292, "P(No | x) = %.3f  ->  do not play" % post_no, size=11.5, color=RED, bold=True)
# spam / Laplace
spam = ["buy cheap pills now", "cheap pills cheap"]; ham = ["meeting at noon", "lunch meeting now", "project report due"]
sw = " ".join(spam).split(); hw = " ".join(ham).split()
V = len(set(sw + hw))
def score(msg, docs, words, prior, k=1):
    p = prior
    for w in msg.split(): p *= (words.count(w) + k) / (len(words) + k * V)
    return p
out = []
for msg in ["cheap pills", "cheap meeting now"]:
    s = score(msg, spam, sw, 2 / 5); h = score(msg, ham, hw, 3 / 5)
    out.append((msg, s, h, s / (s + h)))
raw0 = 3 / 5 * (0 / 9) ** 2
assert V == 11 and round(out[0][3], 3) == 0.908 and round(out[1][3], 3) == 0.549
f.text(430, 14, "Laplace smoothing: a tiny spam filter", size=11, color=NAVY, bold=True)
f.box(296, 24, 276, 66, "vocabulary V = %d words\nspam: %d words, ham: %d words\nP(word | class) = (count + 1) / (words + V)\nwithout the +1, ham score of 'cheap pills' = %d" % (V, len(sw), len(hw), raw0), fill=SOFT, stroke="#94a3b8", size=9.5, r=6, color=NAVY)
for i, (m, s, h, p) in enumerate(out):
    y = 100 + i * 88
    f.box(296, y, 276, 80, "", fill=SAND if p > 0.8 else BLUE, stroke=AMBER if p > 0.8 else NAVY, r=8)
    f.text(434, y + 14, "message: '" + m + "'", size=10.5, color=NAVY, bold=True)
    f.text(434, y + 32, "spam score %.6f" % s, size=10, color=RED)
    f.text(434, y + 46, "ham score %.6f" % h, size=10, color=TEAL)
    f.text(434, y + 66, "P(spam | message) = %.3f" % p, size=12, color=RED if p > 0.8 else AMBER, bold=True)
f.text(434, 292, "a close call when words mix both classes", size=9.5, color=SLATE)
```

```photogrid label="4.4" cols="4" ratio="1.0" caption="Natural and engineered selection. (a) Charles Darwin (public domain), who described evolution by natural selection. (b) A peppered moth on bark (CC BY-SA 4.0): in sooty 19th-century Britain the dark form became common because predators found it harder to see, a fitness test applied by the environment. (c) Great Danes and Chihuahuas (CC BY 2.5): breeders select parents by a fitness of their own choosing, and a few hundred generations produce very different dogs. (d) The NASA ST5 X-band antenna (public domain, scale in cm): its crooked wire shape was found by an evolutionary algorithm and flew on a satellite, a genetic algorithm used in real engineering."
@ photo id="bca302/darwin" cap="Darwin: natural selection"
fit 1.0
focus 0.5 0.65
@ photo id="bca302/moth" cap="Peppered moth: camouflage as fitness"
fit 1.0
focus 0.5 0.5
@ photo id="bca302/dogs" cap="Selective breeding: Great Dane and Chihuahua"
fit 1.0
focus 0.5 0.5
@ photo id="bca302/st5" cap="ST5 antenna evolved by a program"
fit 1.0
focus 0.5 0.5
call 0.5 0.9 0.55 0.72 "evolved wire"
```

```svgfig label="4.8" caption="k-nearest neighbours on 30 real iris flowers (petal length and width in cm). The query (4.8, 1.6) has five nearest neighbours at distances 0.141, 0.141, 0.224, 0.224 and 0.424: three versicolor and two virginica, so the vote is versicolor. Leave-one-out accuracy on the 30 flowers is 28/30 for k = 1, 29/30 for k = 3, 28/30 for k = 5, 29/30 for k = 7 and 26/30 for k = 9, so a small odd k works best and a large k blurs the classes. The toy example of Section 4.5 is in the box."
f = Fig(580, 262)
cm = __import__("math")
S = {"setosa": [(1.3,0.2),(1.5,0.2),(1.4,0.1),(1.4,0.3),(1.0,0.2),(1.5,0.2),(1.5,0.1),(1.4,0.1),(1.3,0.2),(1.4,0.2)],
     "versicolor": [(4.9,1.5),(3.3,1.0),(4.0,1.0),(4.1,1.0),(4.9,1.5),(5.0,1.7),(3.9,1.2),(4.4,1.3),(4.0,1.2),(4.3,1.3)],
     "virginica": [(5.9,2.1),(6.3,1.8),(5.5,2.1),(6.7,2.2),(6.7,2.0),(4.9,1.8),(5.6,2.2),(5.5,1.8),(5.1,1.9),(5.2,2.0)]}
P = [(x, y, k) for k, v in S.items() for x, y in v]
def knn(q, k, pool):
    ds = sorted(pool, key=lambda p: cm.dist(q, p[:2]))[:k]
    votes = {}
    for p in ds: votes[p[2]] = votes.get(p[2], 0) + 1
    return max(votes, key=votes.get), ds
loo = {}
for k in (1, 3, 5, 7, 9):
    ok = 0
    for i, p in enumerate(P):
        pred, _ = knn(p[:2], k, P[:i] + P[i + 1:]); ok += pred == p[2]
    loo[k] = ok
q = (4.8, 1.6); lab, nb = knn(q, 5, P)
col = {"setosa": (MINT, TEAL), "versicolor": (SAND, AMBER), "virginica": (ROSE, RED)}
f.text(150, 14, "30 real iris flowers (petal, cm)", size=11.5, color=NAVY, bold=True)
a = Axes(f, 36, 24, 244, 190, (0.5, 7.5), (0, 2.8)); a.grid(1, 0.5).axes("length", "width")
for x, y, k in P: f.circle(a.X(x), a.Y(y), 4.6, fill=col[k][0], stroke=col[k][1], sw=1.6)
f.circle(a.X(q[0]), a.Y(q[1]), 6, fill="#ffffff", stroke=NAVY, sw=2.4)
r = max(cm.dist(q, p[:2]) for p in nb)
f.raw('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="none" stroke="#1e3a8a" stroke-width="1.4" stroke-dasharray="4 3"/>' % (a.X(q[0]), a.Y(q[1]), round(r / 7 * 244), round(r / 2.8 * 190)))
f.text(a.X(q[0]) - 8, a.Y(q[1]) - 12, "query", size=10, color=NAVY, bold=True, anchor="end")
for i, (k, (fl, c)) in enumerate(col.items()):
    f.circle(60 + i * 78, 232, 4.6, fill=fl, stroke=c, sw=1.6); f.text(68 + i * 78, 232, k, size=9.5, color=c, bold=True, anchor="start", vmid=True)
f.text(150, 252, "query (4.8, 1.6): the 5 nearest vote -> %s" % lab, size=10, color=NAVY, bold=True)
f.text(430, 14, "leave-one-out accuracy vs k (30 flowers)", size=11, color=NAVY, bold=True)
b = Axes(f, 330, 24, 236, 120, (0, 10), (0, 38)); b.grid(2, 10).axes("k", "")
for k, v in loo.items():
    f.box(b.X(k) - 12, b.Y(v), 24, round(b.Y(0) - b.Y(v)), "", fill=BLUE, stroke=NAVY, r=2)
    f.text(b.X(k), b.Y(v) - 8, "%d/30" % v, size=9.5, color=NAVY, bold=True)
f.box(300, 160, 272, 92, "Toy example (3, 3):\nA (1,1) (2,1)   B (4,4) (5,4) (4,5)\ndistances: 1.414 B, 2.236 A, 2.236 B,\n2.236 B, 2.828 A\nk = 1 -> B,  k = 5 -> 3 B vs 2 A -> B", fill=SOFT, stroke="#94a3b8", size=10, r=6, color=NAVY)
```

```svgfig label="4.9" caption="k-means with k = 3 on the same 30 flowers, computed. With a good start (one centre in each group) the sum of squared distances (SSE) falls 17.3, 7.2, 7.1 and the loop stops after 3 rounds, with the clusters following the three species closely. When all three starting centres lie inside the setosa group the SSE starts at 307.8 and ends at 20.43, almost three times worse, which shows that k-means can stop in a poor local minimum and should be run several times."
f = Fig(580, 282)
cm = __import__("math")
S = [(1.3,0.2),(1.5,0.2),(1.4,0.1),(1.4,0.3),(1.0,0.2),(1.5,0.2),(1.5,0.1),(1.4,0.1),(1.3,0.2),(1.4,0.2),
     (4.9,1.5),(3.3,1.0),(4.0,1.0),(4.1,1.0),(4.9,1.5),(5.0,1.7),(3.9,1.2),(4.4,1.3),(4.0,1.2),(4.3,1.3),
     (5.9,2.1),(6.3,1.8),(5.5,2.1),(6.7,2.2),(6.7,2.0),(4.9,1.8),(5.6,2.2),(5.5,1.8),(5.1,1.9),(5.2,2.0)]
def kmeans(C):
    hist = []
    C = list(C)
    for it in range(20):
        lab = [min(range(3), key=lambda j: cm.dist(p, C[j])) for p in S]
        sse = sum(cm.dist(p, C[l]) ** 2 for p, l in zip(S, lab))
        hist.append((list(C), lab, sse))
        newC = []
        for j in range(3):
            m = [p for p, l in zip(S, lab) if l == j]
            newC.append((sum(p[0] for p in m) / len(m), sum(p[1] for p in m) / len(m)) if m else C[j])
        if newC == C: break
        C = newC
    return hist
h1 = kmeans([(1.3, 0.2), (1.5, 0.2), (1.4, 0.1)])
h2 = kmeans([(1.0, 0.2), (4.0, 1.0), (6.7, 2.2)])
assert h1[-1][2] > 2.5 * h2[-1][2] and len(h2) >= 3
panels = [(0, "start: 3 chosen centres"), (1, "after update 1"), (len(h2) - 1, "converged")]
f.text(290, 14, "k-means with k = 3 on the same 30 flowers (good start)", size=11.5, color=NAVY, bold=True)
colr = [(MINT, TEAL), (SAND, AMBER), (ROSE, RED)]
for pi, (idx, title) in enumerate(panels):
    C, lab, sse = h2[idx]
    a = Axes(f, 30 + pi * 190, 36, 150, 120, (0.5, 7.5), (0, 2.8)); a.grid(2, 1, labels=False).axes("", "")
    for p, l in zip(S, lab): f.circle(a.X(p[0]), a.Y(p[1]), 3.6, fill=colr[l][0], stroke=colr[l][1], sw=1.4)
    for j, c in enumerate(C):
        x, y = a.X(c[0]), a.Y(c[1])
        f.raw('<path d="M%s %s l8 8 m-8 0 l8 -8" transform="translate(-4,-4)" stroke="%s" stroke-width="2.6" fill="none"/>' % (x, y, colr[j][1]))
    f.text(30 + pi * 190 + 75, 170, title, size=10.5, color=NAVY, bold=True)
    f.text(30 + pi * 190 + 75, 184, "SSE = %.2f" % sse, size=10, color=RED, bold=True)
f.text(290, 206, "SSE = sum of squared distances to the own centre; it never rises, so the loop must stop", size=10, color=SLATE)
f.box(30, 216, 250, 56, "same data, bad start (all three centres\ninside the setosa group):\nSSE per round " + ", ".join("%.1f" % x[2] for x in h1) + "\nends at SSE %.2f" % h1[-1][2], fill=ROSE, stroke=RED, size=9.5, r=6, color=NAVY)
f.box(300, 216, 270, 56, "good start: SSE per round " + ", ".join("%.1f" % x[2] for x in h2) + "\nends at SSE %.2f in %d rounds\nrun k-means several times, keep the lowest SSE" % (h2[-1][2], len(h2)), fill=MINT, stroke=TEAL, size=9.5, r=6, color=NAVY)
```

```svgfig label="4.10" caption="A genetic algorithm computed. Left: one generation by hand when maximising x squared on 5-bit strings gives fitness 169, 576, 64 and 361 (total 1170, mean 292.5), so the roulette shares are 14.4, 49.2, 5.5 and 30.9 percent, and crossing 11000 with 10011 after bit 2 gives children 11011 (729) and 10000 (256). Right: a seeded run on 30-bit strings (goal: all ones) with tournament selection, crossover, mutation and elitism starts with a best of 19 and a mean of 14.7 and reaches the maximum of 30 in generation 15, after about 480 fitness evaluations."
f = Fig(580, 290)
rnd = __import__("random")
# Part 1: roulette selection, f(x) = x^2 on 5-bit strings
pop = ["01101", "11000", "01000", "10011"]
fit = [int(c, 2) ** 2 for c in pop]; tot = sum(fit); pr = [v / tot for v in fit]
assert fit == [169, 576, 64, 361] and tot == 1170
f.text(150, 14, "one generation by hand: maximise x squared", size=11, color=NAVY, bold=True)
for j, t in enumerate(["string", "x", "f = x^2", "share"]):
    f.text([40, 92, 142, 214][j], 36, t, size=10, color=SLATE, bold=True)
for i, c in enumerate(pop):
    y = 44 + i * 26
    f.box(8, y, 276, 22, "", fill=BLUE if i != 1 else MINT, stroke=NAVY if i != 1 else TEAL, r=4)
    f.text(40, y + 11, c, size=11, color=NAVY, bold=True, vmid=True)
    f.text(92, y + 11, str(int(c, 2)), size=11, color=SLATE, vmid=True)
    f.text(142, y + 11, str(fit[i]), size=11, color=SLATE, vmid=True)
    f.text(214, y + 11, "%.1f %%" % (pr[i] * 100), size=11, color=RED if i == 1 else SLATE, bold=True, vmid=True)
f.text(146, 160, "total %d, mean %.1f, best %d" % (tot, tot / 4, max(fit)), size=10, color=NAVY, bold=True)
x0 = 8
for i, p in enumerate(pr):
    w = round(p * 276)
    f.box(x0, 172, w, 26, "", fill=[SAND, MINT, ROSE, BLUE][i], stroke=[AMBER, TEAL, RED, NAVY][i], r=2)
    f.text(x0 + w / 2, 185, "" if w < 24 else "%.0f%%" % (p * 100), size=9.5, color=NAVY, bold=True, vmid=True); x0 += w
f.text(146, 212, "roulette wheel: slice width = share of total fitness", size=9.5, color=SLATE)
a, b = "11000", "10011"; cut = 2
c1, c2 = a[:cut] + b[cut:], b[:cut] + a[cut:]
f.box(8, 222, 276, 58, "crossover after bit %d:\n%s | %s  x  %s | %s\nchildren %s (%d) and %s (%d)" % (cut, a[:cut], a[cut:], b[:cut], b[cut:], c1, int(c1, 2) ** 2, c2, int(c2, 2) ** 2), fill=SAND, stroke=AMBER, size=10, r=6, color=NAVY)
# Part 2: OneMax 30 bits
rg = rnd.Random(7); L = 30; N = 30
P = [[rg.randint(0, 1) for _ in range(L)] for _ in range(N)]
best, avg = [], []
for g in range(41):
    fs = [sum(x) for x in P]; best.append(max(fs)); avg.append(sum(fs) / N)
    new = [list(P[fs.index(max(fs))])]
    while len(new) < N:
        def tour():
            i, j = rg.randrange(N), rg.randrange(N); return P[i] if fs[i] >= fs[j] else P[j]
        p1, p2 = tour(), tour()
        if rg.random() < 0.9:
            c = rg.randrange(1, L); ch = p1[:c] + p2[c:]
        else: ch = p1[:]
        ch = [1 - b if rg.random() < 1 / L else b for b in ch]
        new.append(ch)
    P = new
hit = next((g for g, v in enumerate(best) if v == L), None)
f.text(430, 14, "a real run: 30 bits, 30 strings, goal = all ones", size=11, color=NAVY, bold=True)
ax = Axes(f, 330, 24, 236, 170, (0, 40), (10, 32)); ax.grid(10, 5).axes("generation", "ones")
ax.curve(lambda g: best[int(round(g))], 0, 40, color=RED, n=40, sw=2.4)
ax.curve(lambda g: avg[int(round(g))], 0, 40, color=TEAL, n=40, sw=2.4)
ax.hline(30, color=AMBER)
f.text(430, 222, "red: best string, teal: population mean", size=10, color=SLATE)
f.text(430, 238, "generation 0: best %d, mean %.1f" % (best[0], avg[0]), size=10.5, color=NAVY, bold=True)
f.text(430, 253, "generation %d: best %d (the maximum)" % (hit, best[hit]) if hit is not None else "best after 40 generations: %d" % best[-1], size=10.5, color=RED, bold=True)
f.text(430, 267, "about %d fitness evaluations in all" % (N * (hit + 1) if hit is not None else N * 41), size=10, color=SLATE)
f.text(430, 281, "tournament, crossover, mutation 1/30, elitism", size=10, color=SLATE)
```

```svgfig label="4.11" caption="Choosing a learning method. Start from the question: labelled data leads to supervised methods (a decision tree when the answer must be explained, naive Bayes or k-NN otherwise, regression for numbers); no labels leads to clustering; a reward signal leads to reinforcement learning; a huge search space with no gradient suggests a genetic algorithm. Whatever you choose, test on unseen cases."
f = Fig(580, 300)
def q(x, y, w, h, t, fl=SAND, c=AMBER): f.box(x, y, w, h, t, fill=fl, stroke=c, size=10, r=8, bold=True, color=NAVY)
def a(x1, y1, x2, y2, lab=None, lp=None): f.arrow([(x1, y1), (x2, y2)], color=SLATE, label=lab, lpos=lp, lsize=9.5)
q(180, 6, 220, 34, "Do you have labelled examples?")
q(40, 70, 150, 34, "predict a category\nor a number?")
q(400, 70, 160, 34, "find groups or\nunusual points?")
a(240, 40, 130, 70, "yes", (160, 52)); a(340, 40, 480, 70, "no", (430, 52))
q(0, 140, 100, 38, "category:\nexplain it?", BLUE, NAVY); q(150, 140, 100, 38, "number:\nregression", MINT, TEAL)
a(100, 104, 50, 140); a(130, 104, 200, 140)
q(0, 210, 100, 40, "yes: decision\ntree (ID3)", MINT, TEAL); q(106, 210, 100, 40, "no: naive Bayes\nfor text, k-NN", MINT, TEAL)
a(30, 178, 46, 210, "yes", (14, 194)); a(70, 178, 150, 210, "no", (126, 192))
q(212, 210, 116, 40, "linear fit, tree,\nneural network", MINT, TEAL); a(215, 178, 268, 210)
q(396, 140, 86, 38, "k-means,\nhierarchical", MINT, TEAL); q(490, 140, 86, 38, "learn from\nreward?", ROSE, RED)
a(450, 104, 439, 140); a(510, 104, 533, 140)
q(470, 210, 106, 40, "reinforcement\nlearning", ROSE, RED); a(533, 178, 523, 210, "yes", (545, 195))
q(280, 100, 100, 38, "or: huge search\nspace?", SAND, AMBER); q(340, 210, 110, 40, "genetic\nalgorithm", MINT, TEAL); a(330, 138, 395, 210, "yes", (378, 176))
f.text(290, 274, "Always: split the data, test on cases the model has not seen, report precision and recall.", size=10.5, color=NAVY, bold=True)
f.text(290, 290, "Start simple; add complexity only when the test result demands it.", size=10, color=SLATE)
```

### 4.8.1 Eight uses of machine learning in Nepal

1. **Spam and scam message filters.** Mobile companies such as Nepal Telecom and Ncell, and mail services, must stop unwanted offers and phishing links reaching users. A naive Bayes filter learns from messages that users mark as spam and multiplies the evidence of each word, as in Fig. 4.7. Laplace smoothing keeps a new word from forcing the score to zero. The filter needs regular retraining because scammers change their wording.
2. **Fraud detection in digital payments.** Wallets and banks such as eSewa, Khalti, Fonepay and ConnectIPS see very few fraudulent payments among millions of honest ones. As Fig. 4.4 shows, accuracy is a poor measure here, so the team watches recall (frauds caught) and precision (alarms that were real). A model is trained on past labelled cases and a human checks the alarms that are raised. Too many false alarms would block honest customers.
3. **Credit scoring for loans.** Banks and cooperatives decide on a loan using age, income, savings and repayment history. A decision tree (Fig. 4.6) is popular because the officer can read the path from the first question to the decision and explain it to the customer. The tree must be pruned and tested on new applicants so that it does not overfit (Fig. 4.3). The result supports the officer and does not replace judgement.
4. **Crop disease and yield prediction.** The Department of Agriculture and farm projects hold records of weather, soil, seed and past yields. A k-nearest-neighbour or tree model compares a new field with the most similar earlier fields, as in Fig. 4.8, and suggests a likely yield or a disease risk. Features such as rainfall and altitude must be scaled so that one does not dominate. A farmer should be told when the new field is unlike any earlier one.
5. **Rain and flood forecasting.** The Department of Hydrology and Meteorology records rainfall and river levels at many stations. A regression model learns the relation between upstream rain and later river height, and a classifier learns when a flood warning is needed. The model is tested on seasons it has not seen, because a model that fits only the past years has overfitted. Warnings should always be checked by a forecaster.
6. **Student progress and dropout alerts.** Schools and campuses that record attendance, marks and fees in systems such as Tribhuvan University and school EMIS records can train a tree to flag students at risk of dropping out. Its purpose is to let a teacher offer help early, not to label a child. The data must be checked for bias, for example against students from remote districts, and parents should know how the data is used.
7. **Customer groups for shops and telecom.** A retailer or a mobile company has thousands of customers and no labels for them. k-means groups customers by how much they spend, call or browse, as in Fig. 4.9, and each group gets a suitable offer, such as a data pack for heavy users. The number of groups k and the starting centres matter, so the analyst runs the method several times and keeps the lowest SSE.
8. **Timetables and delivery routes.** A college has to place hundreds of classes in rooms and periods without clashes, and a delivery firm has to plan routes through crowded streets. These are huge search problems with no simple formula. A genetic algorithm, as in Fig. 4.10, evolves many candidate plans, keeps the fit ones and mixes them by crossover. It gives a good plan quickly, though not a guaranteed best one.

## Formula and fact sheet

- Entropy H(S) = −Σ pᵢ log₂ pᵢ. Gain(S, A) = H(S) − Σ (|S_v| / |S|) H(S_v). ID3 picks the attribute with the highest gain.
- Naive Bayes: choose C maximising P(C) Π P(xᵢ | C); Laplace: (count + 1) / (n_C + |values|).
- Accuracy, precision = TP/(TP + FP), recall = TP/(TP + FN), F1 = 2PR/(P + R).
- k-NN: majority of the k nearest by distance; scale features.
- GA: selection, crossover, mutation, replacement.

## Chapter summary

- Machine learning improves a task from data: supervised (labelled), unsupervised (structure), reinforcement (rewards); evaluate on unseen data to detect overfitting.
- Rote learning memorises, analogy reuses similar cases, induction generalises, explanation-based learning generalises from one explained example.
- Decision trees split on the attribute with the highest information gain; naive Bayes multiplies class-conditional probabilities; k-NN votes among nearest neighbours.
- Genetic algorithms evolve a population with selection, crossover and mutation.

## Practice

1. Differentiate supervised, unsupervised and reinforcement learning with an example each.
2. What is overfitting and how can it be reduced?
3. Compute accuracy, precision, recall and F1 for TP = 40, FP = 10, FN = 20, TN = 130.
4. Explain rote learning, learning by analogy and explanation-based learning.
5. Compute the entropy of a set with 9 positive and 5 negative examples.
6. Why does ID3 choose Outlook as the root of PlayTennis? Give the gains.
7. Classify (Sunny, Cool, High, Strong) with naive Bayes and give the probabilities.
8. What is the zero-frequency problem and how does Laplace smoothing fix it?
9. Classify q = (3, 3) with 1-NN for the data in Section 4.5.
10. Describe the steps of a genetic algorithm and perform single-point crossover on 11100011 and 00011110 after bit 5.

::: note Answers and worked solutions
**1.** Supervised: spam classification from labelled mail. Unsupervised: grouping customers by purchases. Reinforcement: a robot learning to walk from rewards.
**2.** The model fits noise in the training data and generalises poorly. Reduce it with more data, simpler models, pruning or regularisation, and cross-validation to detect it.
**3.** Accuracy 0.85; precision 40/50 = 0.80; recall 40/60 = 0.667; F1 = 2 × 0.8 × 0.667 / (0.8 + 0.667) = 0.727.
**4.** Rote: store and recall answers. Analogy: adapt the solution of the most similar earlier case. EBL: explain why one example works using domain knowledge and generalise the explanation.
**5.** H = −(9/14) log₂(9/14) − (5/14) log₂(5/14) = 0.940 bits.
**6.** Gain(Outlook) = 0.247 is larger than Humidity 0.152, Wind 0.048 and Temperature 0.029.
**7.** Score(Yes) = 0.0053, Score(No) = 0.0206; P(No) = 0.795, P(Yes) = 0.205; the class is No.
**8.** An unseen value gives probability 0 and forces the whole product to 0; add-one smoothing gives it a small non-zero probability, (count + 1)/(n + |values|).
**9.** The nearest point is (4, 4) at distance 1.414, class B.
**10.** Initialise, evaluate fitness, select parents, crossover, mutate, replace, repeat. Crossover after bit 5: 11100|011 and 00011|110 give 11100110 and 00011011.
:::

## Model answers for Unit 4

**Q1. Define machine learning. Explain supervised, unsupervised and reinforcement learning with examples. (10 marks)**

**Introduction.** Machine learning is the study of programs that improve at a task through experience. In Mitchell's wording, a program learns from experience E with respect to a task T and a performance measure P if its performance at T, measured by P, improves with E. A spam filter has the task of classifying mail, the measure of accuracy and the experience of mails that users have labelled.

**Kinds of learning (Fig. 4.1).**

1. **Supervised learning** uses training data that has inputs and the correct outputs. The program learns the map from input to output. If the output is a category the task is *classification* (spam or not spam, a digit from 0 to 9); if it is a number the task is *regression* (the price of a house). Decision trees, naive Bayes, k-nearest neighbours and neural networks are examples.
2. **Unsupervised learning** has no labels. The program finds structure by itself: *clustering* groups similar customers, *association rules* find that buyers of tea also buy sugar, and dimensionality reduction compresses many features into few. k-means is the standard example.
3. **Reinforcement learning** places an agent in a world. It acts, receives a reward or a penalty, and learns by trial and error which actions give the largest total reward. Game players and robots that learn to walk are examples, and Thorndike's puzzle box in Plate 4.1 is the animal version.
4. **Semi-supervised learning** uses a few labelled examples and many unlabelled ones, which is useful when labelling is expensive.

| Point | Supervised | Unsupervised | Reinforcement |
|---|---|---|---|
| Data | inputs and labels | inputs only | states, actions, rewards |
| Goal | predict the label | find structure | maximise total reward |
| Feedback | correct answer | none | reward after actions |
| Example | spam filter | customer groups | game player |

**Evaluation.** Whatever the kind, the data is split into training, validation and test sets, and the final score is measured on the test set. A model that does well only on the training data has overfitted (Fig. 4.3).

**Conclusion.** The three kinds differ in the feedback they receive: the right answer, no answer, or a reward. The choice of method follows from what data is available (Fig. 4.11).

**Q2. What is overfitting? How can it be detected and reduced? (5 marks)**

A model **overfits** when it fits the training data very closely, including its random noise, and then performs badly on new data. It has memorised instead of generalising. The opposite fault is **underfitting**, where the model is too simple to capture the pattern.

**Evidence (Fig. 4.3).** Twelve noisy points from a sine curve were fitted with polynomials of degree 1 to 10. The training error fell steadily from 0.362 to 0.042, which looks like steady improvement. On 60 new points, however, the error was smallest at degree 3 (0.311) and then grew to 1.107 at degree 5 and 998.9 at degree 10. Degree 1 underfits (0.494) and degree 10 overfits.

**Detection.** Keep a test set that the model never sees during training; a large gap between training and test accuracy signals overfitting. **Cross-validation** divides the data into k folds and uses each fold once as the test set, so the estimate does not depend on one lucky split.

**Reduction.**
1. Collect more training data.
2. Choose a simpler model (lower degree, fewer attributes).
3. **Prune** a decision tree, or limit its depth.
4. Use **regularisation**, which penalises large weights.
5. Stop training early when the validation error starts to rise.

**Conclusion.** The aim of learning is good performance on unseen cases, so the model is judged on the test set and not on the training set.

**Q3. Define accuracy, precision, recall and F1. Compute them for TP = 40, FP = 10, FN = 20, TN = 130 and explain why accuracy can mislead. (5 marks)**

For a two-class problem count the true positives (TP), false positives (FP), false negatives (FN) and true negatives (TN), as in the confusion matrix of Fig. 4.4.

| Measure | Formula | Meaning |
|---|---|---|
| Accuracy | (TP + TN) / total | fraction of all cases correct |
| Precision | TP / (TP + FP) | of those called positive, how many are positive |
| Recall | TP / (TP + FN) | of the real positives, how many were found |
| F1 | 2PR / (P + R) | harmonic mean of precision and recall |

**Computation.** The total is 40 + 10 + 20 + 130 = 200. Accuracy = (40 + 130) / 200 = **0.85**. Precision = 40 / 50 = **0.80**. Recall = 40 / 60 = **0.667**. F1 = 2 × 0.80 × 0.667 / (0.80 + 0.667) = **0.727**.

**Why accuracy misleads.** Suppose 10 of 10,000 payments are fraudulent. A model that always says not fraud is right 9,990 times, an accuracy of 99.90 percent, and catches no fraud at all. A real detector with 8 true positives and 40 false positives has a lower accuracy of 99.58 percent but a recall of 0.80. When classes are rare, precision, recall and F1 describe the usefulness of the model better than accuracy.

**Q4. Explain the ID3 decision-tree algorithm. Build the tree for the PlayTennis data using entropy and information gain. (10 marks)**

**Introduction.** A decision tree classifies a case by asking a series of questions. Each internal node tests an attribute, each branch is one value of it and each leaf gives a class. **ID3** builds the tree greedily from the top, choosing at every node the attribute with the largest information gain.

**Measures.** Entropy measures impurity: H(S) = −Σ pᵢ log₂ pᵢ, which is 0 for a pure set and 1 bit for a 50/50 mix. The information gain of an attribute A is Gain(S, A) = H(S) − Σ (|S_v| / |S|) H(S_v), the drop in entropy after splitting on A (Fig. 4.5).

**Algorithm.**
1. If all examples at the node have the same class, make a leaf.
2. If there are no attributes left, make a leaf with the majority class.
3. Otherwise compute the gain of each remaining attribute and split on the best one.
4. Repeat for each branch with the examples that have that value.

**Worked example.** The 14 days have 9 Yes and 5 No, so H(S) = 0.940. The gains are Outlook 0.247, Humidity 0.152, Wind 0.048 and Temperature 0.029, so **Outlook is the root**. The Overcast branch has 4 Yes and no No, so it is a leaf (Yes). The Sunny branch (2 Yes, 3 No) has its best split on Humidity (High gives No, Normal gives Yes). The Rain branch (3 Yes, 2 No) is best split on Wind (Weak gives Yes, Strong gives No). Fig. 4.6 shows the tree. The day Sunny, Cool, High, Strong is classified **No**.

| Point | Decision tree |
|---|---|
| Strength | easy to read and explain; handles mixed data |
| Weakness | overfits; small data changes alter the tree |
| Remedy | pruning, or a random forest of many trees |
| Variants | C4.5 (gain ratio, continuous values), CART (Gini index) |

**Conclusion.** ID3 builds a short, readable tree by always taking the most informative question first. The tree should be pruned and tested on unseen data before it is trusted.

**Q5. Explain the naive Bayes classifier. Classify (Sunny, Cool, High, Strong) for PlayTennis and explain Laplace smoothing. (10 marks)**

**Introduction.** Naive Bayes applies Bayes' rule with the assumption that, given the class, the attributes are independent. It chooses the class C that maximises P(C) × Π P(xᵢ | C). The assumption is rarely exactly true, but the method is fast, needs little data and works well for text.

**Priors and likelihoods.** From the 14 days, P(Yes) = 9/14 and P(No) = 5/14. The likelihoods are given in Fig. 4.7:

| Evidence | P(· \| Yes) | P(· \| No) |
|---|---|---|
| Outlook = Sunny | 2/9 | 3/5 |
| Temperature = Cool | 3/9 | 1/5 |
| Humidity = High | 3/9 | 4/5 |
| Wind = Strong | 3/9 | 3/5 |

**Scores.** Score(Yes) = 9/14 × 2/9 × 3/9 × 3/9 × 3/9 = **0.0053**. Score(No) = 5/14 × 3/5 × 1/5 × 4/5 × 3/5 = **0.0206**. Dividing by the sum, P(No) = 0.0206 / 0.0259 = **0.795** and P(Yes) = 0.205. The prediction is **No**: do not play.

**The zero-frequency problem.** If a value never occurred with a class in training, its estimated probability is 0 and the whole product becomes 0, however strong the other evidence. **Laplace (add-one) smoothing** estimates P(word | class) = (count + 1) / (words in class + V), where V is the number of distinct words. In the spam example with V = 11, the message cheap pills gets a spam score of 0.0148 and a ham score of 0.0015, so P(spam) = **0.908**. Without smoothing the ham score would be 0 whatever the words were.

**Strengths and limits.** Naive Bayes trains in one pass over the data, so it is fast even for large text collections, and it gives a probability and not only a label. Its independence assumption is false when attributes are linked, for example the words New and Kathmandu, which can make the probabilities too extreme, although the ranking of classes is often still right. It should therefore be tested on unseen data like any other model.

**Conclusion.** Naive Bayes multiplies the evidence for each class and picks the larger score. Laplace smoothing is essential for text, where new words appear all the time.

**Q6. Describe the k-nearest-neighbour method. How is k chosen and why are features scaled? (5 marks)**

**k-NN** is a lazy, instance-based learner. It has no training phase: it stores all the examples and does its work when a query arrives. To classify a query it finds the k training points closest to it, usually by Euclidean distance, and takes a majority vote of their classes. For regression it averages their values.

**Example (Fig. 4.8).** On 30 real iris flowers the query (4.8, 1.6) has five nearest neighbours at distances 0.141, 0.141, 0.224, 0.224 and 0.424. Three are versicolor and two are virginica, so the answer is versicolor. In the toy example of Section 4.5 the point (3, 3) has nearest neighbour (4, 4) at distance 1.414, class B.

**Choosing k.** A small k gives a noisy boundary that follows single odd points; a large k blurs the classes together. For the 30 flowers the leave-one-out accuracy is 28/30 at k = 1, 29/30 at k = 3, 28/30 at k = 5, 29/30 at k = 7 and 26/30 at k = 9. So k is chosen by validation, and an odd k avoids ties in a two-class problem.

**Scaling.** Distance adds the differences of all features. If income is in rupees and age in years, the income difference swamps the age difference, so every feature is first scaled to a similar range, for example to 0 to 1.

**Conclusion.** k-NN is simple and needs no model, but it is slow for large data and sensitive to scaling and to irrelevant features.

**Q7. Explain the k-means clustering algorithm. What are its weaknesses? (5 marks)**

**Clustering** is unsupervised: it groups similar points without labels. **k-means** groups n points into k clusters.

**Algorithm.**
1. Choose k starting centres (random points, for example).
2. **Assign** every point to its nearest centre.
3. **Update** each centre to the mean of the points assigned to it.
4. Repeat steps 2 and 3 until no assignment changes.

The method minimises the sum of squared distances (SSE) of points to their own centre. SSE never rises from one round to the next, so the loop must stop.

**Example (Fig. 4.9).** On 30 iris flowers with k = 3 and one starting centre in each group, the SSE falls 17.3, 7.2, 7.1 and the loop stops after 3 rounds; the clusters follow the three species. With all three starting centres inside the setosa group the SSE ends at 20.43, almost three times worse.

**Weaknesses.**
- The result depends on the starting centres, so the method is run several times and the lowest SSE is kept.
- k must be chosen in advance.
- It finds round clusters of similar size and is disturbed by outliers.
- Features need scaling.

**Conclusion.** k-means is fast and simple, but its answer is only a local minimum and must be checked.

**Q8. Explain the genetic algorithm with its steps. Show one generation of an example. (10 marks)**

**Introduction.** A genetic algorithm (GA) is a search method that copies natural selection (Plate 4.4). It keeps a **population** of candidate solutions, each written as a chromosome such as a bit string, and improves the population over **generations**. It suits hard optimisation problems where the landscape is badly understood.

**Steps.**
1. **Initialise** a random population.
2. **Evaluate** the fitness of each individual with a fitness function.
3. **Select** parents with a chance that grows with fitness (roulette wheel or tournament).
4. **Crossover:** choose a cut point and swap the tails of two parents to make children.
5. **Mutation:** flip each bit with a small probability, which keeps variety in the population.
6. **Replace** the population (often keeping the best individual, called elitism) and repeat until the fitness is good enough or time runs out.

**Worked example (Fig. 4.10).** Maximise f(x) = x² for x from 0 to 31 with 5-bit strings. The population 01101, 11000, 01000 and 10011 has x values 13, 24, 8 and 19, fitness 169, 576, 64 and 361, a total of 1170 and a mean of 292.5. The roulette shares are 14.4, 49.2, 5.5 and 30.9 percent, so 11000 is most likely to be chosen. Crossing 11000 with 10011 after bit 2 gives 11011 (x = 27, fitness 729) and 10000 (fitness 256). A child of 729 is already better than any parent.

**A real run.** On 30-bit strings the best fitness rose from 19 to the maximum of 30 in generation 15 (about 480 evaluations).

| Point | Genetic algorithm |
|---|---|
| Strength | needs no gradient; handles huge, rough search spaces |
| Weakness | many fitness evaluations; no guarantee of the best answer |
| Sensitivity | depends on the encoding, population size and mutation rate |
| Uses | timetables, routes, circuit and antenna design |

**Conclusion.** A GA improves a population by selection, crossover and mutation. It gives good solutions to problems that are too large to search completely, such as the evolved antenna of Plate 4.4.

**Q9. Explain rote learning, learning by analogy, inductive learning and explanation-based learning. (5 marks)**

Fig. 4.2 summarises the four forms.

1. **Rote learning** stores every input and output pair and looks the answer up later. Samuel's checkers program stored the values of positions it had met, and a web cache stores pages. It gives speed but no ability to handle a new case.
2. **Learning by analogy** (case-based reasoning) solves a new problem by finding the most similar earlier case and adapting its solution. A help desk retrieves the nearest earlier fault and adjusts its fix. The k-NN method is a simple form, and the quality of the similarity measure decides the quality of the answer.
3. **Inductive learning** generalises from many examples to a rule that covers unseen cases, such as learning the rule for a bird from many labelled animals. Induction is never certain, because one new case can break the rule, and many rules fit the same data, so a bias such as Occam's razor (prefer the simpler rule) is needed. Decision trees and neural networks are inductive.
4. **Explanation-based learning (EBL)** uses background knowledge to explain why one example works, then generalises the explanation into a macro-rule. One example may be enough, but a correct domain theory is required.

**Conclusion.** The four forms differ in how much they generalise: rote none, analogy a little, induction a lot from many examples, and EBL a lot from one example plus knowledge.
