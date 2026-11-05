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
print("scores", {k: round(v, 4) for k, v in sc.items()}, "P(No|x) = %.3f" % (sc["No"] / sum(sc.values())))
docs = [("buy cheap pills now", "spam"), ("cheap pills cheap", "spam"), ("meeting at noon", "ham"), ("lunch meeting now", "ham"), ("project report due", "ham")]
vocab = {w for d, _ in docs for w in d.split()}; print("vocabulary", len(vocab))
def spam(msg):
    out = {}
    for c in ("spam", "ham"):
        words = [w for d, k in docs if k == c for w in d.split()]; p = sum(k == c for _, k in docs) / len(docs)
        for w in msg.split(): p *= (words.count(w) + 1) / (len(words) + len(vocab))
        out[c] = p
    return {k: round(v, 5) for k, v in out.items()}, round(out["spam"] / sum(out.values()), 3)
print(spam("cheap pills")); print(spam("cheap meeting now"))
pts = [((1, 1), "A"), ((2, 1), "A"), ((4, 4), "B"), ((5, 4), "B"), ((4, 5), "B")]
print([(round(math.dist((3, 3), p), 3), c) for p, c in sorted(pts, key=lambda t: math.dist((3, 3), t[0]))])
TP, FP, FN, TN = 40, 10, 20, 130; P_, R_ = TP / (TP + FP), TP / (TP + FN)
print("accuracy %.2f precision %.2f recall %.3f F1 %.3f" % ((TP + TN) / 200, P_, R_, 2 * P_ * R_ / (P_ + R_)))
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
print("crossover example:", "11100" + "110", "00011" + "011")
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
