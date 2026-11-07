---
subject: Probability and Statistics
grade: BCA Semester 3
unit: 4
title: Probability
hours: 8
area: BCA 205 · Probability and Statistics · Unit 4
---

**Probability** measures how likely an event is, from 0 (impossible) to 1 (certain). It is the mathematics of uncertainty behind sampling, hashing, networks, randomised algorithms and machine learning.

::: key What this unit gives you
- Definitions of probability; the addition and multiplication laws; conditional probability and Bayes' rule.
- The binomial, Poisson and normal distributions with numerical problems.
- A table of standard normal values.
:::

## 4.1 Basic definitions

An **experiment** has several possible **outcomes**; the **sample space** S is the set of all outcomes; an **event** is a subset of S. Events are **mutually exclusive** (cannot occur together), **exhaustive** (together cover S), **independent** (one does not affect the other's probability).

**Classical definition:** $P (A)$ = (number of outcomes favourable to $A ) / ( \mathrm{total}$ equally likely outcomes). **Empirical (relative frequency):** $P (A) = \lim$ (times A occurred)/(trials). Axioms: $0 \leq P (A) \leq 1 ;\  P (S) = 1$; for mutually exclusive $A ,\  B ,\  P (A \cup B) = P (A) + P (B)$. Complement: $P (A^{c}) = 1 - P (A)$.

## 4.2 Two basic laws

**Addition law:** $P (A \cup B) = P (A) + P (B) - P (A \cap B)$; for mutually exclusive events the last term is 0.

**Multiplication law:** $P (A \cap B) = P (A) \cdot P ( B$ | A); for **independent** events $P (A \cap B) = P (A) P (B)$.

::: example Worked example
Two fair dice are rolled. $P (\mathrm{sum} = 8) = \frac{5}{36}$ (the pairs $2 + 6 ,\  3 + 5 ,\  4 + 4 ,\  5 + 3 ,\  6 + 2$). $P ( a t$ least one six) = $1 - \left( \frac{5}{6} \right)^{2} = \frac{11}{36}$. A card drawn from 52: $P ( \mathrm{king}$ or heart) = $\frac{4}{52} + \frac{13}{52} - \frac{1}{52}$ = **$\frac{16}{52}$**.

Bag with 5 red and 3 blue balls; two drawn **without replacement**: $P ( \mathrm{both}$ red) = $\left( \frac{5}{8} \right) \left( \frac{4}{7} \right)$ = **$\frac{5}{14}$**; with replacement it would be $\left( \frac{5}{8} \right)^{2} = \frac{25}{64}$.
:::

## 4.3 Conditional probability and Bayes' theorem

**Conditional probability** of A given that B has occurred: **$P ( A$ | $B ) = \frac{P (A \cap B)}{P} ( B$)**, $P (B) > 0$. A and B are independent iff $P ( A$ | $B ) = P ( A$). **Bayes' theorem** reverses the conditioning: **$P ( A$ | $B ) = P ( B$ | $A ) \frac{P (A)}{P} ( B$)**, with $P (B)$ from the total probability law, $P (B) = \sum P ( B$ | $A_{i} ) P ( A_{i}$).

::: example Worked example: a diagnostic test
A bug-detection tool flags a module as buggy. 1% of modules are buggy; the tool flags 95% of buggy modules and falsely flags 5% of clean ones. $P (\mathrm{flag}) = 0.01 \times 0.95 + 0.99 \times 0.05 = 0.0095 + 0.0495 = 0.059$. **$P ( \mathrm{buggy}$ | flagged) = $0.0095 / 0.059 = 0.161$**: only about 16% of flagged modules are actually buggy, because buggy modules are rare. Also, if $P (A) = 0.5 ,\  P (B) = 0.4$ and $P (A \cap B) = 0.2$ then $P ( A$ | $B ) = 0.5 = P ( A$), so A and B are independent.
:::

## 4.4 Random variables and probability distributions

A **random variable** X assigns a number to each outcome. **Discrete** (counts) has a **probability mass function** $p (x)$ with $\sum p (x) = 1$; **continuous** (measurements) has a **density** $f (x)$ with total area 1, and probabilities are areas. **Expected value** $E (X) = \sum x \cdot p (x)$ (mean); **variance** Var(X) = $E (X^{2}) - [E (X)]^{2}$.

### Binomial distribution

For *n* independent trials, each with success probability *p*: **$P (X = x) = C (n ,\  x) p^{x} (1 - p)^{n-x}$**, $x = 0 \ldots n$. **Mean = $n p$, variance = $n p q$** $(q = 1 - p)$.

::: example Worked example
A packet is lost with probability 0.4; 5 packets are sent. $P ( \mathrm{exactly}$ 2 lost) = $C (5 ,\  2) (0.4)^{2} (0.6)^{3} = 10 \times 0.16 \times 0.216$ = **0.3456**. $P ( a t$ least one lost) = $1 - 0.6^{5}$ = **0.9222**. Mean = $5 \times 0.4 = 2.0$, variance = $5 \times 0.4 \times 0.6 = 1.2$.
:::

### Poisson distribution

Counts of rare events in a fixed interval with average rate *λ*: **$P (X = x) = \frac{e^{- \lambda} \lambda^{x}}{x !}$**; **mean = variance = *λ***. It approximates the binomial when *n* is large and *p* small $(\lambda = n p)$.

::: example Worked example
A server receives on average 3 failures a day. $P (\mathrm{exactly} 2) = e^{-3} \cdot \frac{3^{2}}{2 !} = 0.0498 \times 4.5$ = **0.2240**. $P ( a t$ most 2) = **0.4232**. $P ( a t$ least one) = $1 - e^{-3}$ = **0.9502**.
:::

### Normal distribution

The bell curve, symmetric about the mean *μ*: $f (x) = \left( \frac{1}{\sigma \sqrt{2 \pi}} \right) e^{- \frac{(x - \mu)^{2}}{(2 \sigma^{2})}}$. Written X ~ $N (\mu ,\  \sigma^{2})$. **Standardise:** **$Z = \frac{X - \mu}{\sigma}$ ~ $N ( 0$, 1)**, then use the standard normal table of $\Phi (z) = P (Z \leq z)$. **Empirical rule:** $P (\mu - \sigma < X < \mu + \sigma) = 0.6827 ,\  \pm 2 \sigma$: $0.9545 ,\  \pm 3 \sigma$: 0.9973. The total area is 1, the curve is symmetric so $\Phi (- z) = 1 - \Phi (z)$, and mean = median = mode.

| *z* | 0 | 0.5 | 1.0 | 1.5 | 2.0 | 2.5 | 3.0 |
|---|---|---|---|---|---|---|---|
| $\Phi (z)$ | 0.5000 | 0.6915 | 0.8413 | 0.9332 | 0.9772 | 0.9938 | 0.9987 |

::: example Worked example: X ~ N(200, 20²)
**$P (X > 230)$:** $z = \frac{230 - 200}{20} = 1.5 ;\  P = 1 - \Phi (1.5) = 1 - 0.9332$ = **0.0668**.

**$P (180 < X < 240)$:** *z* from −1 to 2: $\Phi (2) - \Phi (- 1) = 0.9772 - 0.1587$ = **0.8186**.

**$P (X < 190)$:** $z = - 0.5 ;\  \Phi (- 0.5) = 1 - 0.6915$ = **0.3085**.

**Top 10%:** $z = 1.2816 \to X = 200 + 1.2816 \times 20$ = **225.63**.

Normal approximation to the binomial (*n* large, $n p$ and $n q > 5$): $X \approx N (n p ,\  n p q)$ with a continuity correction $\pm 0.5$.
:::

## 4.5 Pictures of probability

```svgfig label="4.1" caption="Bayes' theorem as a tree of natural frequencies. Out of 10,000 modules, 100 are buggy and 9,900 are clean. The tool flags 95 of the buggy and 495 of the clean ones, so 590 modules are flagged but only 95 of them are really buggy: $P ( \mathrm{buggy}$ | flagged) = 95/590 = 0.161."
f = Fig(580, 235)
f.box(8, 92, 110, 44, "10,000\nmodules", fill=NAVY, color="#ffffff", bold=True, size=12)
f.box(190, 22, 110, 40, "Buggy\n100", fill=ROSE, stroke=RED, bold=True)
f.box(190, 168, 110, 40, "Clean\n9,900", fill=MINT, stroke=TEAL, bold=True)
f.arrow([(118, 105), (154, 105), (154, 42), (190, 42)]); f.arrow([(118, 123), (154, 123), (154, 188), (190, 188)])
f.text(130, 78, "1%", size=11, color=RED, bold=True); f.text(130, 170, "99%", size=11, color=TEAL, bold=True)
f.box(370, 6, 120, 34, "Flagged 95", fill=AMBER, color="#ffffff", stroke=AMBER, bold=True)
f.box(370, 46, 120, 34, "Missed 5", fill=SOFT, stroke=SLATE)
f.box(370, 150, 120, 34, "False alarm 495", fill=AMBER, color="#ffffff", stroke=AMBER, bold=True)
f.box(370, 190, 120, 34, "Correct 9,405", fill=SOFT, stroke=SLATE)
f.arrow([(300, 38), (334, 38), (334, 23), (370, 23)]); f.arrow([(300, 46), (334, 46), (334, 63), (370, 63)])
f.arrow([(300, 184), (334, 184), (334, 167), (370, 167)]); f.arrow([(300, 192), (334, 192), (334, 207), (370, 207)])
f.text(338, 14, "95%", size=10.5, color=SLATE, bold=True); f.text(338, 80, "5%", size=10.5, color=SLATE, bold=True)
f.text(338, 158, "5%", size=10.5, color=SLATE, bold=True); f.text(338, 222, "95%", size=10.5, color=SLATE, bold=True)
f.text(535, 78, "Flagged:", size=11, color=AMBER, bold=True); f.text(535, 96, "95 + 495", size=11, color=AMBER, bold=True)
f.text(535, 114, "= 590", size=11, color=AMBER, bold=True)
f.text(535, 140, "95/590", size=11.5, color=NAVY, bold=True); f.text(535, 158, "= 0.161", size=11.5, color=NAVY, bold=True)
```

```photogrid label="4.1" cols="2" ratio="1.0" caption="Why the bell curve appears. (a) A Galton board: each bead bounces left or right at every peg, so the final slot is a binomial count, and the heap of beads at the bottom forms a bell shape. (b) The normal curve and the empirical rule: 68.27% of the area lies within one *σ* of the mean, 95.45% within two and 99.73% within three."
@ photo id="bca205/galton" cap="Galton board (quincunx), Matemateca, University of São Paulo"
fit 1.0
focus 0.5 0.62
@ svg cap="The 68-95-99.7 rule"
import math
f = Fig(300, 300)
ax = Axes(f, 14, 40, 272, 190, (-3.5, 3.5), (0, 0.45))
N = lambda z: math.exp(-z * z / 2) / math.sqrt(2 * math.pi)
ax.area(N, -3, 3, fill="#dbeafe", opacity=1); ax.area(N, -2, 2, fill="#93c5fd", opacity=1); ax.area(N, -1, 1, fill="#3b82f6", opacity=1)
ax.curve(N, -3.5, 3.5, color=NAVY, sw=2.4)
f.line(ax.X(-3.5), ax.Y(0), ax.X(3.5), ax.Y(0), color=SLATE, sw=1.2)
for z in range(-3, 4): f.text(ax.X(z), ax.Y(0) + 15, f"{z}σ" if z else "μ", size=12.5, color=SLATE, bold=True)
f.text(150, 112, "68.27%", size=13, color="#ffffff", bold=True)
f.text(150, 24, "95.45% within ±2σ", size=13, color=NAVY, bold=True); f.text(150, 262, "99.73% within ±3σ", size=13, color=NAVY, bold=True)
```

```svgfig label="4.2" caption="Two discrete distributions drawn from the worked examples. (a) Binomial $n = 5 ,\  p = 0.4$ (packet loss): the most likely count is 2 (0.3456), mean 2.0. (b) Poisson with $\lambda = 3$ (server failures per day): $P (2) = 0.2240$ and $P (3) = 0.2240$ are tied for the highest bar. Bar heights are probabilities and each set adds to 1."
import math
f = Fig(580, 210)
def bars(x0, vals, color, title, xl):
    ax = Axes(f, x0, 28, 240, 135, (-0.5, len(vals) - 0.5), (0, 0.4))
    ax.grid(1, 0.1, labels=False)
    for i, v in enumerate(vals):
        f.raw(f'<rect x="{ax.X(i - 0.35)}" y="{ax.Y(v)}" width="{round(ax.X(i + 0.35) - ax.X(i - 0.35), 2)}" height="{round(ax.Y(0) - ax.Y(v), 2)}" fill="{color}" stroke="{NAVY}" stroke-width="1"/>')
        f.text(ax.X(i), ax.Y(0) + 13, str(i), size=10.5, color=SLATE)
        f.text(ax.X(i), ax.Y(v) - 5, f"{v:.3f}", size=8.5, color=NAVY, bold=True)
    f.text(x0 + 120, 14, title, size=11.5, color=NAVY, bold=True); f.text(x0 + 120, 190, xl, size=10.5, color=SLATE, italic=True)
bars(24, [math.comb(5, k) * 0.4 ** k * 0.6 ** (5 - k) for k in range(6)], "#bfdbfe", "(a) Binomial n = 5, p = 0.4", "x = packets lost")
bars(312, [math.exp(-3) * 3 ** k / math.factorial(k) for k in range(9)], "#fde68a", "(b) Poisson λ = 3", "x = failures in a day")
```

```svgfig label="4.3" caption="Areas under $N (200 ,\  20^{2})$. Left: $P (X > 230)$ is the right tail beyond $z = 1.5$, area 0.0668. Right: $P (180 < X < 240)$ is the area between $z = - 1$ and $z = 2$, which is $0.9772 - 0.1587 = 0.8186$. Probability for a continuous variable is always an area."
import math
f = Fig(580, 200)
N = lambda x: math.exp(-(x - 200) ** 2 / 800) / (20 * math.sqrt(2 * math.pi))
for k, (a, b, t) in enumerate([(230, 270, "P(X > 230) = 0.0668"), (180, 240, "P(180 < X < 240) = 0.8186")]):
    ax = Axes(f, 18 + k * 290, 34, 255, 125, (140, 260), (0, 0.022))
    ax.area(N, a, min(b, 260), fill="#fbbf24", opacity=0.8)
    ax.curve(N, 140, 260, color=NAVY, sw=2.4)
    f.line(ax.X(140), ax.Y(0), ax.X(260), ax.Y(0), color=SLATE, sw=1.2)
    for v in (160, 200, 240): f.text(ax.X(v), ax.Y(0) + 14, str(v), size=10.5, color=SLATE)
    f.text(145 + k * 290, 18, t, size=11.5, color=NAVY, bold=True)
f.text(290, 192, "z = (x − 200)/20:   230 → 1.5,   180 → −1,   240 → 2", size=10.5, color=SLATE, italic=True)
```

## 4.6 Eight uses of probability and distributions

1. **Risk and uncertainty in software.** Probability turns "it may fail" into a number such as 0.4% per day. A team can then compare the cost of failure with the cost of prevention. Nepali digital-payment systems such as Fonepay plan their servers around such numbers.
2. **Spam and fraud filters.** Bayes' theorem updates the chance that a message is spam after seeing words such as "lottery". The same idea flags suspicious card or wallet transactions. As Figure 4.1 shows, a low base rate keeps many alarms false.
3. **Reliability and packet loss.** The binomial distribution gives the chance that exactly *k* of *n* packets are lost. Network engineers use it to size retransmission and buffer settings. A video call over a weak mobile link is exactly this problem.
4. **Counting rare events.** The Poisson distribution models failures, arrivals of calls or accidents per period. A bank branch in Butwal uses it to decide how many counters to open at peak hour. Too few counters make queues; too many waste salaries.
5. **Measurement errors and natural variation.** Heights, marks, weights and manufacturing sizes follow the normal curve. With only the mean and *σ* one can state what share lies above or below any value. Exam boards use this for grading on a curve.
6. **Quality control limits.** A factory fixes control limits at $\mu \pm 3 \sigma$ because 99.73% of normal output falls inside them. A point outside signals that the process has shifted. This is the basis of Six Sigma programmes.
7. **Insurance and finance.** Insurers price a policy from the probability of a claim and its expected size. Banks estimate the chance a borrower defaults. Both rely on expected value $E (X)$ and variance from this unit.
8. **Machine learning and simulation.** Classifiers output probabilities, and many algorithms assume normal errors. Monte Carlo simulation draws random numbers from these distributions to test designs before they are built. Games, weather models and network studies all use this.

```photogrid label="4.2" cols="2" ratio="1.2" caption="The same test, two very different meanings. (a) A rapid antigen test cassette: a second line means positive, but how much that line proves depends on how many people are infected. (b) With a test that finds 90 per cent of the sick and wrongly flags 10 per cent of the healthy, 1,000 people are tested in two settings. In mass screening with 1 per cent infected, 10 are sick and 9 test positive, but 99 of the 990 healthy also test positive, so only 8.3 per cent of positives are really sick. In a clinic where 20 per cent are infected, 180 of 200 sick and 80 of 800 healthy test positive, and 69.2 per cent of positives are sick. A simulation of 200,000 people (fixed seed) gave 8.2 and 68.6 per cent, matching Bayes' theorem; the percentages are illustrative, not those of a real kit."
@ photo id="bcamath/rapidtest" cap="A rapid test cassette: one line or two"
fit 1.2
focus 0.5 0.5
@ svg cap="1,000 people tested twice: base rate matters"
import random
sens, fpr = 0.90, 0.10
def tree(prev, n=1000):
    sick = round(n * prev)
    tp = round(sick * sens)
    fp = round((n - sick) * fpr)
    return sick, tp, fp, tp / (tp + fp)
a = tree(0.01)
b = tree(0.20)
assert a[:3] == (10, 9, 99) and b[:3] == (200, 180, 80)
random.seed(2081)
def sim(prev, N=200000):
    tp = fp = 0
    for _ in range(N):
        s = random.random() < prev
        pos = random.random() < (sens if s else fpr)
        if pos:
            tp += s
            fp += (not s)
    return tp / (tp + fp)
sa, sb = sim(0.01), sim(0.20)
assert abs(sa - a[3]) < 0.01 and abs(sb - b[3]) < 0.01
facts = dict(ppv1=round(a[3] * 100, 1), ppv2=round(b[3] * 100, 1), s1=round(sa * 100, 1), s2=round(sb * 100, 1))
f = Fig(300, 236)
f.text(150, 12, "sensitivity 90%, false positive rate 10%", size=10.5, color=NAVY, bold=True)
for k, (t, prev, title) in enumerate([(a, 1, "Mass screening: 1% infected"), (b, 20, "Clinic: 20% infected")]):
    y = 26 + k * 100
    f.text(150, y + 4, title, size=10.5, color=NAVY, bold=True)
    f.box(100, y + 12, 100, 20, "1,000 people", fill=BLUE, stroke=NAVY, size=10.5, bold=True, r=3, sw=1)
    f.box(20, y + 44, 110, 20, "%d sick" % t[0], fill="#fecaca", stroke=RED, size=10.5, r=3, sw=1)
    f.box(170, y + 44, 110, 20, "%d healthy" % (1000 - t[0]), fill="#bbf7d0", stroke=TEAL, size=10.5, r=3, sw=1)
    f.arrow([(130, y + 32), (75, y + 44)], color=SLATE)
    f.arrow([(170, y + 32), (225, y + 44)], color=SLATE)
    f.text(75, y + 78, "%d test positive" % t[1], size=10.5, color=RED, bold=True)
    f.text(225, y + 78, "%d test positive" % t[2], size=10.5, color=TEAL, bold=True)
    f.text(150, y + 92, "true among positives: %.1f%%" % (t[3] * 100), size=10.5, color=NAVY, bold=True)
```

## Formula and fact sheet

- $P (A \cup B) = P (A) + P (B) - P (A \cap B) ;\  P (A \cap B) = P (A) P ( B$ | $A ) ;\  P ( A$ | $B ) = \frac{P (A \cap B)}{P} ( B$).
- Bayes: $P ( A$ | $B ) = P ( B$ | $A ) \frac{P (A)}{P} ( B$).
- Binomial: $C (n ,\  x) p^{x} q^{n-x}$; mean $n p ,\  v a r n p q$. Poisson: $\frac{e^{- \lambda} \lambda^{x}}{x}$!; mean = $v a r = \lambda$.
- Normal: $Z = \frac{X - \mu}{\sigma} ;\  \pm 1 \sigma$ 68.27%, $\pm 2 \sigma$ 95.45%, $\pm 3 \sigma$ 99.73%.

## Chapter summary

- Probability follows the addition and multiplication laws; conditioning updates probabilities and Bayes' rule inverts them.
- Binomial models fixed trials, Poisson rare events, normal measurements, which are standardised to Z for table lookup.

## Practice

1. Two coins are tossed. Find the probability of at least one head.
2. A bag has 5 red and 3 blue balls. Two drawn without replacement: $P ( \mathrm{one}$ of each colour)?
3. $P (A) = 0.6 ,\  P (B) = 0.5 ,\  P (A \cup B) = 0.8$. Find $P (A \cap B)$ and $P ( A$ | B). Are A and B independent?
4. A fair coin is tossed 6 times. Find the probability of exactly 3 heads, and the mean and variance of the number of heads.
5. Calls arrive at 2 per minute (Poisson). $P ( n o$ calls in a minute)?
6. X ~ $N (50 ,\  10^{2})$. Find $P (40 < X < 65)$.
7. Marks are $N (60 ,\  15^{2})$. What fraction scores below 40? Above 90?
8. Explain independence $v s$ mutual exclusivity.

::: note Answers and worked solutions
**1.** $1 - P ( n o$ heads) = $1 - \frac{1}{4}$ = **$\frac{3}{4}$**.

**2.** $P ( R$ then $B ) + P ( B$ then $R ) = \left( \frac{5}{8} \right) \left( \frac{3}{7} \right) + \left( \frac{3}{8} \right) \left( \frac{5}{7} \right) = \frac{15}{56} + \frac{15}{56}$ = **$\frac{15}{28}$**.

**3.** $P (A \cap B) = 0.6 + 0.5 - 0.8$ = **0.3**; $P ( A$ | $B ) = 0.3 / 0.5$ = **0.6** = $P (A)$, so they **are independent** $(0.6 \times 0.5 = 0.3)$.

**4.** $\frac{C (6 ,\  3)}{2^{6}} = \frac{20}{64}$ = **0.3125**; mean = 3, variance = $6 \times 0.25$ = **1.5**.

**5.** $e^{-2}$ = **0.1353**.

**6.** $z = - 1$ and 1.5: $0.9332 - 0.1587$ = **0.7745**.

**7.** Below 40: $z = - 1.33 ,\  \Phi = 0.0918$ (**9.2%**). Above 90: $z = 2 ,\  1 - 0.9772$ = **2.3%**.

**8.** Independent: occurrence of one does not change the probability of the other $(P (A \cap B) = P (A) P (B))$. Mutually exclusive: cannot both occur $(P (A \cap B) = 0)$. Events with nonzero probabilities cannot be both.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Machine A makes 60% of the chips in a factory and machine B makes 40%. 2% of A's chips and 5% of B's chips are defective. A chip chosen at random is defective. Find the probability that it came from A.**

*Introduction.* This is a reversed-conditioning problem, so we use **Bayes' theorem**: $P ( A$ | $D ) = P ( D$ | $A ) \frac{P (A)}{P} ( D$), where $P (D)$ comes from the law of total probability.

*Given.* $P (A) = 0.60 ,\  P (B) = 0.40 ,\  P ( D$ | $A ) = 0.02 ,\  P ( D$ | $B ) = 0.05$.

*Total probability of a defect.* $P (D) = P ( D$ | $A ) P (A) + P ( D$ | $B ) P (B) = 0.02 \times 0.60 + 0.05 \times 0.40 = 0.012 + 0.020$ = **0.032**.

*Bayes.* $P ( A$ | $D ) = 0.012 / 0.032$ = **0.375**. Then $P ( B$ | $D ) = 0.020 / 0.032 = 0.625$, and the two add up to 1 as they must.

*Interpretation.* Machine A produces more chips, but machine B is far worse, so a defective chip is more likely to be from B (62.5%) than A (37.5%). *Conclusion.* The prior share of production (60%) is updated to 37.5% after we learn the chip is defective; that is the meaning of a posterior probability.

**Q2 (5 marks). The response time of a server is normally distributed with mean 120 ms and standard deviation 15 ms. Find (a) $P (X > 150)$, (b) $P (100 < X < 140)$, (c) the response time that 95% of requests beat.**

*Introduction.* For X ~ $N (\mu ,\  \sigma^{2})$ we standardise with $Z = \frac{X - \mu}{\sigma}$ and read $\Phi (z)$ from the standard normal table (Figure 4.3).

$\ast (a)$ Slow responses.* $z = \frac{150 - 120}{15} = 2.0$. $P (X > 150) = 1 - \Phi (2.0) = 1 - 0.9772$ = **0.0228**, so about 2.3% of requests are slower than 150 ms.

$\ast (b)$ Between 100 and $140 . \ast z_{1} = \frac{100 - 120}{15} = - 1.33$ and $z_{2} = + 1.33$. $P = \Phi (1.33) - \Phi (- 1.33) = 2 \Phi (1.33) - 1 \approx 2 \times 0.9088 - 1$ ≈ **0.818** (more exact $z = 1.3333$ gives 0.8176). About 82% of requests fall in this band.

$\ast (c)$ The 95th percentile.* We need *z* with $\Phi (z) = 0.95$, which is $z = 1.645$. $x = 120 + 1.645 \times 15$ = **144.7 ms**. So 95% of requests finish within about 145 ms.

*Conclusion.* The tail beyond two standard deviations is small (2.3%), and an engineer would set the timeout alarm near 145 ms to catch only the slowest 5%.

**Q3 (10 marks). Explain the binomial and Poisson distributions with their conditions, mean and variance. A batch has a 10% defect rate and 10 items are inspected. Find $P (X = 2)$ and $P (X \leq 1)$ using the binomial, then compare with the Poisson approximation.**

*Introduction.* A **random variable** assigns a number to each outcome of an experiment. Two of the most useful discrete distributions are the **binomial** (counts of successes in fixed trials) and the **Poisson** (counts of rare events in an interval). Figure 4.2 shows both.

*Binomial distribution $B (n ,\  p) . \ast$

1. **Conditions:** a fixed number *n* of trials; each trial has two outcomes (success or failure); constant success probability *p*; trials independent.
2. **Formula:** $P (X = x) = C (n ,\  x) p^{x} q^{n-x}$, with $q = 1 - p$ and $x = 0 ,\  1 ,\  \ldots ,\  n$.
3. **Mean = $n p$, variance = $n p q$.**
4. **Shape:** symmetric if $p = 0.5$, skewed otherwise.

*Poisson distribution $P (\lambda) . \ast$

1. **Conditions:** events occur singly, at a constant average rate *λ* per interval, independently of each other.
2. **Formula:** $P (X = x) = \frac{e^{- \lambda} \lambda^{x}}{x !}$, with $x = 0 ,\  1 ,\  2 ,\  \ldots$
3. **Mean = variance = *λ*.**
4. **Link:** it approximates $B (n ,\  p)$ when *n* is large and *p* is small, with $\lambda = n p$.

*Calculation (binomial, $n = 10 ,\  p = 0.1 ) . \ast P (X = 2) = C (10 ,\  2) (0.1)^{2} (0.9)^{8} = 45 \times 0.01 \times 0.4305$ = **0.1937**. $P (X = 0) = 0.9^{10} = 0.3487$ and $P (X = 1) = 10 \times 0.1 \times 0.9^{9} = 0.3874$, so **$P (X \leq 1) = 0.7361$**. Mean = $n p = 1.0$ and variance = $n p q = 0.9$.

*Poisson approximation $(\lambda = n p = 1) . \ast P (X = 2) = e^{-1} \times \frac{1^{2}}{2 !}$ = **0.1839**. $P (X = 0) = P (X = 1) = e^{-1} = 0.3679$, so $P (X \leq 1)$ = **0.7358**.

*Comparison of the two answers (Table).*

| Quantity | Binomial (exact) | Poisson $(\lambda = 1)$ |
|---|---|---|
| $P (X = 2)$ | 0.1937 | 0.1839 |
| $P (X \leq 1)$ | 0.7361 | 0.7358 |
| Mean | 1.0 | 1.0 |
| Variance | 0.9 | 1.0 |

*Binomial versus Poisson (Table).*

| Point | Binomial | Poisson |
|---|---|---|
| Trials | fixed *n* | no fixed *n*, an interval |
| Possible values | 0 to *n* | 0, 1, 2, … without limit |
| Parameters | *n* and *p* | *λ* only |
| Mean and variance | $n p$ and $n p q$ | both *λ* |
| Typical use | defects in a sample, lost packets | calls per minute, failures per day |

*Conclusion.* The Poisson answer is close to the exact binomial one (0.7358 against 0.7361 for $P (X \leq 1)$), so for rare events the simpler Poisson model is a good substitute. The small gap in $P (X = 2)$ shows the approximation improves as *n* grows and *p* shrinks.
