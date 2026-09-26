---
subject: Mathematics
grade: 12
unit: 11
title: Probability
hours: 4
area: Statistics and Probability
---

In Grade 11 you handled **independent** events, where what happens first tells
you nothing about what happens next. Real problems are rarely so obliging: draw a
card and do not replace it, and the second draw has changed. This unit deals with
those **dependent** cases and with the tool that measures them — **conditional
probability**, the probability of an event *given* that another event has already
happened. From it follow the multiplication theorem for dependent events, Bayes'
theorem for working backwards from an observed effect to its likely cause, and
the binomial distribution for repeated trials.

::: key What the exam asks
Almost every question is: *drawing without replacement*, *"given that …"*,
*a two-way table*, or *Bayes with two or three causes*. Draw a **tree diagram**
first — multiply along a branch, add across branches. Keep answers as fractions
in lowest terms unless the question uses decimals.
:::

## 11.1 Dependent cases

::: definition Independent and dependent events
Two events $A$ and $B$ are **independent** if the occurrence of one does not
change the probability of the other, that is $P(A \cap B) = P(A)\,P(B)$.
Otherwise they are **dependent**, and then

$$ P(A \cap B) = P(A)\cdot P(B \mid A) $$

where $P(B \mid A)$ is the probability of $B$ *after $A$ has happened*.
:::

The classic generator of dependence is **drawing without replacement**. A bag
holds $5$ red and $3$ black balls. The first ball drawn is red with probability
$\frac58$. If that ball is *not* put back, only $7$ balls remain, $4$ of them
red, so the second ball is red with probability $\frac47$ — the first draw has
changed the second. With replacement the probability would have stayed $\frac58$
and the draws would be independent.

| | Without replacement | With replacement |
|---|---|---|
| Total changes? | yes, $n \to n-1$ | no |
| Events are | dependent | independent |
| $P(\text{2 reds})$ from 5R, 3B | $\frac58 \times \frac47 = \frac{5}{14}$ | $\frac58 \times \frac58 = \frac{25}{64}$ |

::: key Multiplication theorem for dependent events
For two events,
$$ P(A \cap B) = P(A)\,P(B \mid A) = P(B)\,P(A \mid B) $$
For three, chain it:
$$ P(A \cap B \cap C) = P(A)\,P(B\mid A)\,P(C \mid A \cap B) $$
On a tree diagram this is simply "multiply the probabilities along the branch".
:::

```figure caption="Two balls drawn one after another, without replacement, from a bag of 5 red and 3 black. The second-stage probabilities have denominator $7$, not $8$ — that is what 'dependent' means. Multiply along a branch, then add the branches you want."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0, 3.2))
def node(x, y, label, col=INK):
    ax.text(x, y, label, ha='center', va='center', fontsize=10.0, color=col,
            bbox=dict(boxstyle='circle,pad=0.30', fc='white', ec=col, lw=1.0))
def branch(x1, y1, x2, y2, lab, col=MUTED):
    ax.annotate('', xy=(x2-0.10, y2), xytext=(x1+0.10, y1),
                arrowprops=dict(arrowstyle='->', color=col, lw=1.1))
    ax.text((x1+x2)/2, (y1+y2)/2 + 0.16, lab, ha='center', fontsize=9.0, color=col)
node(0.15, 2.0, 'S')
node(1.55, 3.0, 'R', '#d9534f'); node(1.55, 1.0, 'B', INK)
branch(0.15, 2.0, 1.55, 3.0, '5/8', '#d9534f')
branch(0.15, 2.0, 1.55, 1.0, '3/8', INK)
node(3.05, 3.7, 'R', '#d9534f'); node(3.05, 2.4, 'B', INK)
node(3.05, 1.6, 'R', '#d9534f'); node(3.05, 0.3, 'B', INK)
branch(1.55, 3.0, 3.05, 3.7, '4/7', '#d9534f')
branch(1.55, 3.0, 3.05, 2.4, '3/7', INK)
branch(1.55, 1.0, 3.05, 1.6, '5/7', '#d9534f')
branch(1.55, 1.0, 3.05, 0.3, '2/7', INK)
for y, txt in [(3.7, 'RR :  5/8 × 4/7 = 20/56'), (2.4, 'RB :  5/8 × 3/7 = 15/56'),
               (1.6, 'BR :  3/8 × 5/7 = 15/56'), (0.3, 'BB :  3/8 × 2/7 =  6/56')]:
    ax.text(3.42, y, txt, va='center', fontsize=9.0, color=INK)
ax.text(3.42, -0.55, 'total  =  56/56  =  1', va='center', fontsize=9.0, color=MUTED)
ax.text(0.15, 0.95, 'bag:\n5 R, 3 B', ha='center', fontsize=8.6, color=MUTED)
ax.set_xlim(-0.35, 6.4); ax.set_ylim(-0.95, 4.3)
ax.axis('off')
```

::: example Worked example 11.1
**Problem.** Two cards are drawn one after another from a well-shuffled pack of
$52$ cards, without replacement. Find the probability that (a) both are kings,
(b) the first is a king and the second is a queen, (c) all three are aces when
three cards are drawn.

**Solution.** Let $K_1$ be "first card is a king", $K_2$ "second card is a king".

**(a)** $P(K_1) = \dfrac{4}{52}$. Given a king has gone, $51$ cards remain of
which $3$ are kings, so $P(K_2 \mid K_1) = \dfrac{3}{51}$.

$$ P(K_1 \cap K_2) = \frac{4}{52}\times\frac{3}{51} = \frac{12}{2652}
= \frac{1}{221} $$

**(b)** Removing a king leaves all $4$ queens among $51$ cards:

$$ P = \frac{4}{52}\times\frac{4}{51} = \frac{16}{2652} = \frac{4}{663} $$

**(c)** Chain the multiplication theorem three times:

$$ P = \frac{4}{52}\times\frac{3}{51}\times\frac{2}{50} = \frac{24}{132\,600}
= \frac{1}{5525} $$
:::

::: example Worked example 11.2
**Problem.** A bag contains $5$ red and $3$ black balls. Two balls are drawn at
random one after the other. Find the probability that (a) both are red,
(b) one is red and the other black, (c) at least one is black — first without
replacement, then with replacement.

**Solution.** *Without replacement* (dependent), reading the tree diagram above:

$$ P(\text{both red}) = \frac58 \times \frac47 = \frac{20}{56} = \frac{5}{14} $$

$$ P(\text{one of each}) = P(RB) + P(BR) = \frac{15}{56} + \frac{15}{56}
= \frac{30}{56} = \frac{15}{28} $$

$$ P(\text{at least one black}) = 1 - P(\text{both red}) = 1 - \frac{5}{14}
= \frac{9}{14} $$

*With replacement* (independent), every draw sees $5$ red out of $8$:

$$ P(\text{both red}) = \frac58 \times \frac58 = \frac{25}{64}, \qquad
P(\text{one of each}) = 2 \times \frac58 \times \frac38 = \frac{30}{64}
= \frac{15}{32} $$

$$ P(\text{at least one black}) = 1 - \frac{25}{64} = \frac{39}{64} $$

Both red is more likely *with* replacement, because the bag is never depleted of
red balls.
:::

::: caution "At least one" means subtract from 1
Never add up the cases "exactly one" and "exactly two" if a complement will do.
$P(\text{at least one black}) = 1 - P(\text{no black})$ is one line; listing
cases is four and invites an error.
:::

## 11.2 Conditional probability (without proof)

::: definition Conditional probability
The probability of $A$ given that $B$ has already occurred is

$$ P(A \mid B) = \frac{P(A \cap B)}{P(B)}, \qquad P(B) \ne 0 $$

Equivalently $P(A \cap B) = P(B)\,P(A \mid B)$. The result is quoted without
proof; it is really a change of sample space.
:::

The idea behind the formula is worth one sentence: once you know $B$ has
happened, the outcomes outside $B$ are dead. $B$ becomes the new sample space,
and the only part of $A$ still alive is $A \cap B$. So we compare $A \cap B$ with
$B$ instead of with $S$ — and dividing by $P(B)$ is exactly that comparison.

```figure caption="Conditioning is shrinking the sample space. On the left, $A$ is measured against the whole of $S$. On the right, $B$ has happened, so $B$ is the new sample space and only the shaded overlap $A \cap B$ counts: $P(A \mid B) = P(A \cap B)/P(B)$."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
fig, (a1, a2) = plt.subplots(1, 2, figsize=(5.2, 2.6))
for ax, shrink in ((a1, False), (a2, True)):
    ax.add_patch(Rectangle((0, 0), 4.0, 3.0, fc='none', ec=INK, lw=1.1))
    ax.text(0.16, 2.72, 'S', fontsize=9.6, color=INK)
    cA = Circle((1.55, 1.5), 0.95, fc=ACCENT, ec=ACCENT, lw=1.2, alpha=0.18)
    cB = Circle((2.55, 1.5), 0.95, fc='#d9534f', ec='#d9534f', lw=1.2, alpha=0.18)
    if shrink:
        ax.add_patch(Rectangle((0, 0), 4.0, 3.0, fc=MUTED, ec='none', alpha=0.22))
        cB.set_alpha(0.30)
    ax.add_patch(cA); ax.add_patch(cB)
    ax.text(1.05, 1.45, 'A', fontsize=10.0, color=ACCENT)
    ax.text(2.92, 1.45, 'B', fontsize=10.0, color='#d9534f')
    if shrink:
        half = np.arccos(0.5/0.95)
        t1 = np.linspace(-half, half, 200)
        lx = np.concatenate([1.55 + 0.95*np.cos(t1), 2.55 - 0.95*np.cos(t1[::-1])])
        ly = np.concatenate([1.5 + 0.95*np.sin(t1), 1.5 + 0.95*np.sin(t1[::-1])])
        ax.fill(lx, ly, color='#2e8b57', ec='#2e8b57', lw=1.0, alpha=0.55)
        ax.text(2.05, 0.30, 'A ∩ B', ha='center', fontsize=9.0, color='#2e8b57')
    ax.set_xlim(-0.1, 4.1); ax.set_ylim(-0.6, 3.2)
    ax.set_aspect('equal'); ax.axis('off')
a1.set_title('P(A) = area of A ÷ area of S', fontsize=8.8, pad=2)
a2.set_title('P(A | B) = A ∩ B ÷ B', fontsize=8.8, pad=2)
fig.tight_layout(pad=0.4)
```

::: example Worked example 11.3
**Problem.** For two events $A$ and $B$, $P(A) = \frac12$, $P(B) = \frac35$ and
$P(A \cup B) = \frac45$. Find $P(A \cap B)$, $P(A \mid B)$ and $P(B \mid A)$, and
state whether $A$ and $B$ are independent.

**Solution.** From the addition theorem,
$P(A \cup B) = P(A) + P(B) - P(A \cap B)$:

$$ \frac45 = \frac12 + \frac35 - P(A \cap B)
\;\Longrightarrow\; P(A \cap B) = \frac12 + \frac35 - \frac45 = \frac{5 + 6 - 8}{10}
= \frac{3}{10} $$

$$ P(A \mid B) = \frac{P(A \cap B)}{P(B)} = \frac{3/10}{3/5}
= \frac{3}{10}\times\frac53 = \frac12, \qquad
P(B \mid A) = \frac{3/10}{1/2} = \frac35 $$

Since $P(A \mid B) = \frac12 = P(A)$, knowing $B$ tells us nothing about $A$:
the events are **independent**. (The same conclusion from
$P(A)P(B) = \frac12 \times \frac35 = \frac{3}{10} = P(A \cap B)$.)
:::

::: example Worked example 11.4
**Problem.** Of $100$ students of a Kathmandu college, $60$ are boys. In the last
examination $45$ of the boys and $35$ of the girls passed. A student is picked at
random. Find (a) $P(\text{pass})$, (b) $P(\text{pass} \mid \text{girl})$,
(c) $P(\text{girl} \mid \text{pass})$.

**Solution.** Put the data in a two-way table first — always.

| | Passed | Failed | Total |
|---|---|---|---|
| Boys | 45 | 15 | **60** |
| Girls | 35 | 5 | **40** |
| **Total** | **80** | **20** | **100** |

**(a)** $P(\text{pass}) = \dfrac{80}{100} = \dfrac45$.

**(b)** Conditioning on "girl" means working inside the girls' row only:

$$ P(\text{pass} \mid \text{girl}) = \frac{P(\text{pass} \cap \text{girl})}{P(\text{girl})}
= \frac{35/100}{40/100} = \frac{35}{40} = \frac78 $$

**(c)** Now the pass *column* is the sample space:

$$ P(\text{girl} \mid \text{pass}) = \frac{35/100}{80/100} = \frac{35}{80}
= \frac{7}{16} $$

Note that $P(\text{pass}\mid\text{girl}) \ne P(\text{girl}\mid\text{pass})$ —
they answer different questions.
:::

::: example Worked example 11.5
**Problem.** Two dice are thrown. Find (a) the probability that both show odd
numbers given that the sum is $6$, (b) the probability that the sum is $6$ given
that both show odd numbers.

**Solution.** The sample space has $36$ equally likely outcomes.

**(a)** Let $B$ = "sum is $6$" $= \{(1,5),(2,4),(3,3),(4,2),(5,1)\}$, so
$n(B) = 5$. Of these, the ones with both odd are $(1,5),(3,3),(5,1)$, so
$n(A \cap B) = 3$:

$$ P(A \mid B) = \frac{n(A \cap B)}{n(B)} = \frac{3}{5} $$

**(b)** Let $A$ = "both odd". Each die is odd with probability $\frac12$, so
$n(A) = 3 \times 3 = 9$:

$$ P(B \mid A) = \frac{n(A \cap B)}{n(A)} = \frac{3}{9} = \frac13 $$

The same three favourable outcomes, two different denominators — because the
condition names the sample space.
:::

```figure caption="The $36$ outcomes of two dice. The five circled cells are the event $B$ (sum $= 6$); the nine shaded cells are the event $A$ (both odd); three cells are in both. $P(A \mid B) = 3/5$ counts along the circled anti-diagonal only, while $P(B \mid A) = 3/9$ counts inside the shaded block only — same numerator, different sample space."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
fig, ax = plt.subplots(figsize=(4.4, 3.4))
for i in range(1, 7):
    for j in range(1, 7):
        both_odd = (i % 2 == 1) and (j % 2 == 1)
        fc = '#1d6fb8' if both_odd else 'white'
        al = 0.20 if both_odd else 1.0
        ax.add_patch(Rectangle((i-0.5, j-0.5), 1, 1, fc=fc, ec=GRID, lw=0.8, alpha=al))
        if i + j == 6:
            ax.add_patch(Circle((i, j), 0.36, fc='none', ec='#d9534f', lw=1.6))
        col = '#2e8b57' if (both_odd and i + j == 6) else INK
        ax.text(i, j, str(i+j), ha='center', va='center', fontsize=8.4, color=col)
ax.set_xticks(range(1, 7)); ax.set_yticks(range(1, 7))
ax.set_xlabel('first die', fontsize=9.0); ax.set_ylabel('second die', fontsize=9.0)
ax.set_xlim(0.4, 6.6); ax.set_ylim(0.4, 6.6)
ax.set_aspect('equal')
ax.tick_params(length=0, labelsize=8.4)
ax.spines[['top','right','left','bottom']].set_visible(False)
ax.text(3.5, 7.0, 'shaded: both odd (9 cells)     circled: sum = 6 (5 cells)',
        ha='center', fontsize=8.4, color=MUTED)
fig.tight_layout(pad=0.4)
```

::: example Worked example 11.6
**Problem.** A problem in mathematics is given to three students whose chances of
solving it are $\frac12$, $\frac13$ and $\frac14$, independently. Find the
probability that (a) the problem is solved, (b) exactly one of them solves it.

**Solution.** The probabilities of *failing* are $\frac12$, $\frac23$,
$\frac34$.

**(a)** $P(\text{solved}) = 1 - P(\text{all three fail})$:

$$ P = 1 - \frac12 \times \frac23 \times \frac34 = 1 - \frac{6}{24} = 1 - \frac14
= \frac34 $$

**(b)** Exactly one solves it — three mutually exclusive cases:

$$ P = \frac12\cdot\frac23\cdot\frac34 + \frac12\cdot\frac13\cdot\frac34
+ \frac12\cdot\frac23\cdot\frac14
= \frac{6}{24} + \frac{3}{24} + \frac{2}{24} = \frac{11}{24} $$
:::

## 11.3 Bayes' theorem: reasoning backwards

Conditional probability usually runs forwards: *given the cause, how likely is the
effect?* Bayes' theorem runs the other way: *given the effect, how likely is each
cause?* A bulb is defective — which machine made it? A test is positive — is the
patient really ill?

Suppose the events $E_1, E_2, \ldots, E_n$ are **mutually exclusive and
exhaustive**: exactly one of them must happen. They cut the sample space into
pieces, and any event $A$ is cut into the corresponding slices.

::: key Total probability and Bayes' theorem
**Law of total probability.** Adding the slices of $A$,

$$ P(A) = P(E_1)P(A \mid E_1) + P(E_2)P(A \mid E_2) + \cdots + P(E_n)P(A \mid E_n) $$

**Bayes' theorem.** For any one cause $E_i$,

$$ P(E_i \mid A) = \frac{P(E_i)\,P(A \mid E_i)}{\sum_{k} P(E_k)\,P(A \mid E_k)} $$

In words: *that branch, divided by all the branches that end in $A$.*
:::

```figure caption="Bayes' theorem as a Venn diagram. The causes $E_1$, $E_2$, $E_3$ are mutually exclusive and exhaustive, so the event $A$ (green) is chopped into the three slices $A \cap E_1$, $A \cap E_2$, $A \cap E_3$. $P(A)$ is the sum of the slices; $P(E_2 \mid A)$ is the middle slice divided by that sum."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Ellipse
fig, ax = plt.subplots(figsize=(5.0, 2.8))
W, H = 6.0, 3.0
cols = ['#1d6fb8', '#b8860b', '#6a5acd']
edges = [0.0, 2.1, 4.0, 6.0]
for i in range(3):
    ax.add_patch(Rectangle((edges[i], 0), edges[i+1]-edges[i], H,
                           fc=cols[i], ec=INK, lw=1.0, alpha=0.14))
    ax.text((edges[i]+edges[i+1])/2, 2.62, 'E$_%d$' % (i+1),
            ha='center', fontsize=10.2, color=cols[i])
ell = Ellipse((3.0, 1.15), 4.6, 1.5, fc='#2e8b57', ec='#2e8b57', lw=1.3, alpha=0.30)
ax.add_patch(ell)
ax.text(3.0, 1.15, 'A', ha='center', va='center', fontsize=11.0, color='#2e8b57')
for xv in (2.1, 4.0):
    ax.plot([xv, xv], [0, H], color=INK, lw=1.0)
ax.text(1.25, 0.62, 'A∩E$_1$', ha='center', fontsize=8.4, color=INK)
ax.text(3.05, 0.62, 'A∩E$_2$', ha='center', fontsize=8.4, color=INK)
ax.text(4.78, 0.62, 'A∩E$_3$', ha='center', fontsize=8.4, color=INK)
ax.add_patch(Rectangle((0, 0), W, H, fc='none', ec=INK, lw=1.3))
ax.text(0.12, 3.12, 'S', fontsize=9.8, color=INK)
ax.text(3.0, -0.52, 'P(A) = P(A∩E$_1$) + P(A∩E$_2$) + P(A∩E$_3$)',
        ha='center', fontsize=9.0, color=MUTED)
ax.set_xlim(-0.2, 6.2); ax.set_ylim(-0.9, 3.5)
ax.set_aspect('equal'); ax.axis('off')
```

::: example Worked example 11.7
**Problem.** Bag A contains $3$ white and $2$ red balls; bag B contains $2$ white
and $4$ red balls. A bag is chosen at random and one ball is drawn from it.
(a) Find the probability that the ball is white. (b) If the ball drawn is white,
what is the probability that it came from bag A?

**Solution.** Let $E_1$ = "bag A chosen", $E_2$ = "bag B chosen", $W$ = "the ball
is white". Then $P(E_1) = P(E_2) = \frac12$ and

$$ P(W \mid E_1) = \frac35, \qquad P(W \mid E_2) = \frac26 = \frac13 $$

**(a)** By the law of total probability,

$$ P(W) = \frac12\times\frac35 + \frac12\times\frac13
= \frac{3}{10} + \frac16 = \frac{9 + 5}{30} = \frac{14}{30} = \frac{7}{15} $$

**(b)** By Bayes' theorem,

$$ P(E_1 \mid W) = \frac{P(E_1)P(W\mid E_1)}{P(W)}
= \frac{3/10}{7/15} = \frac{3}{10}\times\frac{15}{7} = \frac{9}{14} $$

So a white ball is about $64\%$ likely to have come from bag A — sensible, since
bag A is the whiter bag.
:::

::: example Worked example 11.8
**Problem.** In a factory, machine A produces $60\%$ of the bulbs and machine B
the rest. $2\%$ of A's bulbs and $3\%$ of B's are defective. A bulb picked at
random from the day's output is found defective. What is the probability that it
was made by machine A?

**Solution.** $P(A) = 0.6$, $P(B) = 0.4$, $P(D\mid A) = 0.02$,
$P(D \mid B) = 0.03$.

$$ P(D) = (0.6)(0.02) + (0.4)(0.03) = 0.012 + 0.012 = 0.024 $$

$$ P(A \mid D) = \frac{(0.6)(0.02)}{0.024} = \frac{0.012}{0.024} = \frac12 $$

Although machine A makes more bulbs, its lower defect rate exactly cancels the
advantage: a defective bulb is equally likely to have come from either machine.
:::

::: example Worked example 11.9
**Problem.** A disease affects $1\%$ of a population. A screening test is
positive for $99\%$ of the people who have the disease, but also for $2\%$ of the
people who do not. A randomly chosen person tests positive. What is the
probability that he actually has the disease?

**Solution.** Let $D$ = "has the disease", $+$ = "tests positive". Then
$P(D) = 0.01$, $P(D') = 0.99$, $P(+\mid D) = 0.99$, $P(+ \mid D') = 0.02$.

$$ P(+) = (0.01)(0.99) + (0.99)(0.02) = 0.0099 + 0.0198 = 0.0297 $$

$$ P(D \mid +) = \frac{0.0099}{0.0297} = \frac{1}{3} $$

Only $1$ in $3$. The test is accurate, but the disease is so rare that the
$2\%$ of false positives drawn from the huge healthy group outnumber the true
positives two to one. This is why screening results are always confirmed by a
second test.
:::

::: caution $P(A \mid B)$ and $P(B \mid A)$ are different numbers
Worked example 11.9 is the standard trap: $P(+\mid D) = 0.99$ but
$P(D \mid +) = 0.33$. Read the question twice and identify which event is the
*condition* — it is the one that has already happened.
:::

## 11.4 Repeated trials: the binomial distribution

A **Bernoulli trial** is an experiment with just two outcomes, success (with
probability $p$) and failure (with probability $q = 1 - p$). Repeat it $n$ times
independently — toss a coin $6$ times, inspect $10$ bulbs — and the number of
successes $X$ follows the **binomial distribution**.

::: key Binomial probability
$$ P(X = r) = {}^nC_r\, p^{r} q^{\,n-r}, \qquad r = 0, 1, 2, \ldots, n,
\qquad q = 1-p $$

${}^nC_r$ counts the orders in which the $r$ successes can fall, $p^{r}$ pays for
the successes and $q^{n-r}$ for the failures. The terms are exactly those of the
expansion of $(q + p)^{n}$, which is why they add to $1$.

Mean $= np$, variance $= npq$, standard deviation $= \sqrt{npq}$.
:::

```figure caption="The binomial distribution for $n = 8$ trials. With $p = 0.2$ successes are rare and the bars pile up on the left; $p = 0.5$ is symmetric about the mean $np = 4$; $p = 0.8$ is the mirror image of $p = 0.2$. In each case the bar heights add to 1 and the dashed line marks the mean $np$."
import numpy as np, matplotlib.pyplot as plt
from math import comb
fig, axes = plt.subplots(1, 3, figsize=(5.2, 2.5), sharey=True)
n = 8
for ax, p, c in zip(axes, [0.2, 0.5, 0.8], ['#1d6fb8', '#2e8b57', '#d9534f']):
    r = np.arange(n+1)
    pr = np.array([comb(n, k)*p**k*(1-p)**(n-k) for k in r])
    ax.bar(r, pr, color=c, alpha=0.80, width=0.72)
    ax.axvline(n*p, color=MUTED, ls='--', lw=1.0)
    ax.set_title('p = %.1f   (np = %.1f)' % (p, n*p), fontsize=8.6, pad=3)
    ax.set_xlabel('number of successes r', fontsize=8.2)
    ax.set_xticks([0, 2, 4, 6, 8])
    ax.spines[['top','right']].set_visible(False)
    ax.grid(True, axis='y', alpha=.4)
axes[0].set_ylabel('P(X = r)', fontsize=8.6)
axes[0].set_ylim(0, 0.36)
fig.tight_layout(pad=0.4)
```

::: example Worked example 11.10
**Problem.** A fair coin is tossed $5$ times. Find the probability of getting
(a) exactly $3$ heads, (b) at least $3$ heads, (c) the mean number of heads.

**Solution.** Each toss is a Bernoulli trial with $p = q = \frac12$, $n = 5$.

**(a)** $$ P(X = 3) = {}^5C_3\left(\frac12\right)^{3}\left(\frac12\right)^{2}
= 10 \times \frac{1}{32} = \frac{10}{32} = \frac{5}{16} $$

**(b)** $$ P(X \ge 3) = P(3) + P(4) + P(5)
= \frac{10 + 5 + 1}{32} = \frac{16}{32} = \frac12 $$

(Which had to be $\frac12$, by the symmetry of the fair coin.)

**(c)** Mean $= np = 5 \times \frac12 = 2.5$ heads.
:::

::: example Worked example 11.11
**Problem.** A die is thrown $4$ times. Find the probability of getting
(a) exactly two sixes, (b) at least one six. Also find the mean and variance of
the number of sixes.

**Solution.** "Success" = a six, so $p = \frac16$, $q = \frac56$, $n = 4$.

**(a)** $$ P(X = 2) = {}^4C_2\left(\frac16\right)^{2}\left(\frac56\right)^{2}
= 6 \times \frac{1}{36}\times\frac{25}{36} = \frac{150}{1296} = \frac{25}{216} $$

**(b)** $$ P(X \ge 1) = 1 - P(X = 0) = 1 - \left(\frac56\right)^{4}
= 1 - \frac{625}{1296} = \frac{671}{1296} \approx 0.518 $$

Mean $= np = 4 \times \frac16 = \dfrac23$; variance
$= npq = 4 \times \dfrac16 \times \dfrac56 = \dfrac{5}{9}$.
:::

## Chapter summary

- Events are **dependent** when one changes the probability of the other; drawing
  without replacement is the standard example.
- Multiplication theorem: $P(A \cap B) = P(A)P(B \mid A) = P(B)P(A\mid B)$, and
  $P(A\cap B\cap C) = P(A)P(B\mid A)P(C\mid A\cap B)$. Independent means
  $P(A \cap B) = P(A)P(B)$.
- Conditional probability: $P(A \mid B) = \dfrac{P(A\cap B)}{P(B)}$, i.e. $B$
  becomes the new sample space.
- On a **tree diagram**: multiply along a branch, add across branches; all
  branch probabilities from one node add to $1$.
- "At least one" $= 1 -$ "none".
- Total probability:
  $P(A) = \sum_k P(E_k)P(A \mid E_k)$ over a set of mutually exclusive and
  exhaustive causes.
- Bayes' theorem:
  $P(E_i \mid A) = \dfrac{P(E_i)P(A\mid E_i)}{\sum_k P(E_k)P(A\mid E_k)}$ — one
  branch over all the branches.
- Binomial: $P(X = r) = {}^nC_r p^{r}q^{\,n-r}$, mean $np$, variance $npq$.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. If $P(A) = \frac12$ and $P(B \mid A) = \frac13$, then $P(A \cap B)$ is <span class="marks">[1]</span>
   (a) $\frac16$ (b) $\frac13$ (c) $\frac23$ (d) $\frac56$
2. A bag has $3$ red and $5$ black balls. Two are drawn without replacement. Given
   that the first is black, the probability that the second is black is <span class="marks">[1]</span>
   (a) $\frac58$ (b) $\frac47$ (c) $\frac57$ (d) $\frac12$
3. If $P(B) = 0.5$ and $P(A \cap B) = 0.32$, then $P(A \mid B)$ is <span class="marks">[1]</span>
   (a) $0.16$ (b) $0.32$ (c) $0.64$ (d) $0.82$
4. Two cards are drawn without replacement from a pack of $52$. The probability
   that both are aces is <span class="marks">[1]</span>
   (a) $\frac{1}{169}$ (b) $\frac{1}{221}$ (c) $\frac{1}{13}$ (d) $\frac{4}{663}$
5. For a binomial distribution with $n = 5$ and $p = \frac12$, $P(X = 5)$ is <span class="marks">[1]</span>
   (a) $\frac{1}{32}$ (b) $\frac{5}{32}$ (c) $\frac12$ (d) $\frac{5}{16}$
6. $A$ and $B$ are independent with $P(A) = 0.3$, $P(B) = 0.4$. Then
   $P(A \cup B)$ is <span class="marks">[1]</span>
   (a) $0.12$ (b) $0.58$ (c) $0.70$ (d) $0.82$

::: note Answers to Group A
**1.** (a) — $P(A\cap B) = P(A)P(B\mid A) = \frac12\times\frac13 = \frac16$.

**2.** (b) — after one black is removed, $4$ blacks remain among $7$ balls.

**3.** (c) — $0.32 \div 0.5 = 0.64$.

**4.** (b) — $\frac{4}{52}\times\frac{3}{51} = \frac{1}{221}$.

**5.** (a) — $\left(\frac12\right)^{5} = \frac{1}{32}$.

**6.** (b) — $0.3 + 0.4 - (0.3)(0.4) = 0.7 - 0.12 = 0.58$.
:::

**Group B — Short answer (5 marks each)**

1. A bag contains $6$ white and $4$ black balls. Two balls are drawn at random one
   after the other without replacement. Find the probability that (a) both are
   white, (b) one is white and the other black, (c) at least one is black. <span class="marks">[5]</span>
2. Define conditional probability. If $P(A) = 0.6$, $P(B) = 0.5$ and
   $P(A \cap B) = 0.3$, find $P(A\mid B)$ and $P(B \mid A)$ and determine whether
   $A$ and $B$ are independent. <span class="marks">[5]</span>
3. Two dice are thrown together. Find the probability that the sum is $6$, given
   that both dice show odd numbers. Also find the probability that both show odd
   numbers, given that the sum is $6$. <span class="marks">[5]</span>
4. The probabilities that Ramesh, Sita and Gita solve a problem are $\frac12$,
   $\frac13$ and $\frac14$ respectively, and they work independently. Find the
   probability that the problem is solved and the probability that exactly one of
   them solves it. <span class="marks">[5]</span>
5. A die is thrown $5$ times. Find the probability of getting exactly two sixes,
   and state the mean number of sixes. <span class="marks">[5]</span>
6. Three cards are drawn one by one without replacement from a well-shuffled
   pack. Find the probability that all three are hearts. Would the answer be
   larger or smaller with replacement, and why? <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Without replacement the second draw has denominator $9$.

(a) $P(WW) = \dfrac{6}{10}\times\dfrac59 = \dfrac{30}{90} = \dfrac13$.

(b) $P(\text{one of each}) = P(WB) + P(BW)
= \dfrac{6}{10}\cdot\dfrac49 + \dfrac{4}{10}\cdot\dfrac69 = \dfrac{24+24}{90}
= \dfrac{48}{90} = \dfrac{8}{15}$.

(c) $P(\text{at least one black}) = 1 - P(WW) = 1 - \dfrac13 = \dfrac23$.

(Check: $\frac13 + \frac{8}{15} + P(BB) = 1$ gives
$P(BB) = \frac{2}{15} = \frac{4}{10}\cdot\frac39$ ✓.)

**2.** $P(A\mid B)$ is the probability that $A$ occurs given that $B$ has already
occurred, defined by $P(A \mid B) = P(A\cap B)/P(B)$ for $P(B) \ne 0$.

$$ P(A \mid B) = \frac{0.3}{0.5} = 0.6, \qquad P(B\mid A) = \frac{0.3}{0.6} = 0.5 $$

Since $P(A\mid B) = 0.6 = P(A)$ (equivalently
$P(A)P(B) = 0.6\times0.5 = 0.3 = P(A\cap B)$), the events are **independent**.

**3.** Let $A$ = "both odd", $B$ = "sum is $6$". Out of $36$ outcomes,
$n(A) = 3\times3 = 9$ and $B = \{(1,5),(2,4),(3,3),(4,2),(5,1)\}$ so $n(B) = 5$.
The outcomes in both are $(1,5), (3,3), (5,1)$, so $n(A\cap B) = 3$.

$$ P(B \mid A) = \frac{n(A\cap B)}{n(A)} = \frac39 = \frac13, \qquad
P(A \mid B) = \frac{n(A \cap B)}{n(B)} = \frac35 $$

**4.** Failure probabilities are $\frac12, \frac23, \frac34$.

$$ P(\text{solved}) = 1 - \frac12\cdot\frac23\cdot\frac34 = 1 - \frac14 = \frac34 $$

$$ P(\text{exactly one}) = \frac12\cdot\frac23\cdot\frac34
+ \frac12\cdot\frac13\cdot\frac34 + \frac12\cdot\frac23\cdot\frac14
= \frac{6+3+2}{24} = \frac{11}{24} $$

**5.** Binomial with $n = 5$, $p = \frac16$, $q = \frac56$:

$$ P(X = 2) = {}^5C_2\left(\frac16\right)^{2}\left(\frac56\right)^{3}
= 10 \times \frac{1}{36}\times\frac{125}{216} = \frac{1250}{7776}
= \frac{625}{3888} \approx 0.161 $$

Mean $= np = 5 \times \frac16 = \frac56 \approx 0.83$ sixes.

**6.** There are $13$ hearts in $52$ cards, and each draw removes one card:

$$ P = \frac{13}{52}\times\frac{12}{51}\times\frac{11}{50}
= \frac{1716}{132\,600} = \frac{11}{850} \approx 0.0129 $$

With replacement the probability would be
$\left(\frac14\right)^{3} = \frac{1}{64} \approx 0.0156$, which is **larger**:
replacing each heart keeps the proportion of hearts at $\frac14$ instead of
letting it fall to $\frac{12}{51}$ and then $\frac{11}{50}$.
:::

**Group C — Long answer (8 marks each)**

1. (a) State the multiplication theorem of probability for dependent events and
   explain, with a tree diagram, how it is used for two draws without
   replacement. <span class="marks">[3]</span>
   (b) An urn contains $4$ white and $6$ black balls. Two balls are drawn one
   after the other without replacement. Find the probability that (i) both are
   black, (ii) the second is black, (iii) the first is black given that the second
   is black. <span class="marks">[5]</span>
2. (a) State Bayes' theorem. <span class="marks">[2]</span>
   (b) In a factory, machines A, B and C produce $50\%$, $30\%$ and $20\%$ of the
   items, and $3\%$, $4\%$ and $5\%$ of their outputs respectively are defective.
   An item drawn at random is found to be defective. Find the probability that it
   was produced by each of the three machines, and say which machine is the most
   likely source. <span class="marks">[6]</span>

::: note Answers to Group C
**1.** (a) For dependent events,
$P(A\cap B) = P(A)\cdot P(B \mid A)$: the probability that both happen is the
probability of the first times the probability of the second *computed in the
reduced situation left behind by the first*. On a tree diagram the first stage
carries $P(A)$ and $P(A')$, and each second-stage branch carries a conditional
probability with a denominator one smaller than at the first stage (see the tree
in §11.1). Multiplying along a branch gives the probability of that pair of
outcomes; adding the branches that satisfy the requirement gives the answer.

(b) Total $10$ balls: $4$ white ($W$), $6$ black ($B$).

(i) $P(B_1 \cap B_2) = \dfrac{6}{10}\times\dfrac59 = \dfrac{30}{90} = \dfrac13$.

(ii) The second ball is black either after a black or after a white:

$$ P(B_2) = \frac{6}{10}\cdot\frac59 + \frac{4}{10}\cdot\frac69
= \frac{30}{90} + \frac{24}{90} = \frac{54}{90} = \frac35 $$

(Equal to $P(B_1)$ — before you look at the first ball, every position in the
shuffled row is alike.)

(iii) By the definition of conditional probability,

$$ P(B_1 \mid B_2) = \frac{P(B_1 \cap B_2)}{P(B_2)} = \frac{1/3}{3/5}
= \frac13\times\frac53 = \frac59 $$

**2.** (a) If $E_1, E_2, \ldots, E_n$ are mutually exclusive and exhaustive
events with $P(E_i) > 0$, and $A$ is any event with $P(A) > 0$, then

$$ P(E_i \mid A) = \frac{P(E_i)\,P(A\mid E_i)}{\sum_{k=1}^{n} P(E_k)\,P(A \mid E_k)} $$

(b) $P(A) = 0.5$, $P(B) = 0.3$, $P(C) = 0.2$ and
$P(D\mid A) = 0.03$, $P(D \mid B) = 0.04$, $P(D\mid C) = 0.05$.

| Machine | $P(E_i)$ | $P(D\mid E_i)$ | product |
|---|---|---|---|
| A | 0.50 | 0.03 | 0.015 |
| B | 0.30 | 0.04 | 0.012 |
| C | 0.20 | 0.05 | 0.010 |
| | | **$P(D)$** | **0.037** |

$$ P(A \mid D) = \frac{0.015}{0.037} = \frac{15}{37} \approx 0.405 $$
$$ P(B \mid D) = \frac{0.012}{0.037} = \frac{12}{37} \approx 0.324 $$
$$ P(C \mid D) = \frac{0.010}{0.037} = \frac{10}{37} \approx 0.270 $$

The three posterior probabilities add to $1$, as they must. Machine **A** is the
most likely source of a defective item — not because it is the least reliable (it
is the most reliable) but because it makes half of everything.
:::
