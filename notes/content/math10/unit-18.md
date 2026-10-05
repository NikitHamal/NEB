---
subject: Mathematics
grade: 10
unit: 18
title: Probability
hours: 0
area: Compulsory Mathematics
---

Will it rain tomorrow? Will the coin land heads? Will a ticket win the lottery? Probability is the branch of mathematics that measures **how likely** an event is, using a number from 0 (impossible) to 1 (certain). Insurance companies, weather forecasters, doctors and game designers all rely on it. In this chapter we build the idea from simple experiments with coins, dice, cards and bags of coloured balls; list **sample spaces** (using tables and **tree diagrams**); use the **addition rule** for "or" and the **multiplication rule** for "and"; and learn the difference between **mutually exclusive** and **independent** events, and between drawing **with** and **without replacement**.

::: key What the SEE asks from this chapter
Expect: (i) write the sample space and find a probability for coins, dice or cards (2–3 marks); (ii) a probability with the **complement** ("at least one", "not"); (iii) balls drawn from a bag **with or without replacement**, with a **tree diagram** (4 marks); (iv) a Venn-diagram or "like football / like cricket" problem using $P(A\cup B)=P(A)+P(B)-P(A\cap B)$; (v) an algebra question ("find $x$ if $P(\text{blue})=\frac{3}{5}$"). Always write the favourable outcomes, the total outcomes, and a fraction in lowest terms.
:::

```photo id="math10/dice" caption="A die. Each of the six faces has the same chance of landing face up, so the probability of any one face is 1/6 — the simplest equally likely sample space." width="80"
```

## 18.1 Probability: concepts, formulas and worked problems

### Key terms

| Term | Meaning | Example |
|---|---|---|
| Experiment (trial) | an action whose result is uncertain | tossing a coin, rolling a die |
| Outcome | one possible result of a trial | Head; 5 |
| Sample space $S$ | the set of **all** possible outcomes | die: $S=\{1,2,3,4,5,6\}$; $n(S)=6$ |
| Event $E$ | a subset of the sample space we are interested in | "even number" $=\{2,4,6\}$ |
| Equally likely | each outcome has the same chance | a fair coin or fair die |
| Complement $E'$ (not $E$) | the outcomes that are **not** in $E$ | not even $=\{1,3,5\}$ |

### The probability of an event

::: key Probability formula
For equally likely outcomes,
$$ P(E)=\frac{\text{number of favourable outcomes}}{\text{total number of outcomes}}=\frac{n(E)}{n(S)} $$

- $0\leq P(E)\leq1$; $P(E)=0$ for an impossible event, $P(E)=1$ for a certain event.
- $P(E)+P(E')=1$, so $P(E')=1-P(E)$.
- The sum of the probabilities of all the outcomes in the sample space is 1.
- **Expected number** of times $E$ occurs in $N$ trials $=N\times P(E)$.
:::

::: example Rolling a die
**Problem.** A fair die is rolled once. Find the probability of (a) an even number, (b) a prime number, (c) a number greater than 4, (d) a number that is not a multiple of 3.

**Solution.** $S=\{1,2,3,4,5,6\}$, $n(S)=6$.

(a) $\{2,4,6\}$: $P=\frac{3}{6}=\frac{1}{2}$.
(b) Primes $\{2,3,5\}$ (1 is not prime): $P=\frac{3}{6}=\frac{1}{2}$.
(c) $\{5,6\}$: $P=\frac{2}{6}=\frac{1}{3}$.
(d) Multiples of 3 are $\{3,6\}$, so "not a multiple of 3" has $\{1,2,4,5\}$: $P=\frac{4}{6}=\frac{2}{3}$, or $1-\frac{2}{6}=\frac{2}{3}$.
:::

::: example Tossing coins
**Problem.** Two fair coins are tossed. Write the sample space and find the probability of (a) two heads, (b) at least one head, (c) exactly one head.

**Solution.** $S=\{HH,HT,TH,TT\}$, so $n(S)=4$.

(a) $P(HH)=\frac{1}{4}$.
(b) At least one head: $\{HH,HT,TH\}$, $P=\frac{3}{4}$ (or $1-P(TT)=1-\frac{1}{4}$).
(c) $\{HT,TH\}$: $P=\frac{2}{4}=\frac{1}{2}$.
:::

::: example Three coins
**Problem.** Three coins are tossed. Find $P(\text{exactly two heads})$.

**Solution.** There are $2\times2\times2=8$ outcomes: HHH, HHT, HTH, HTT, THH, THT, TTH, TTT. Two heads: HHT, HTH, THH. $P=\frac{3}{8}$.
:::

### Two dice: the sample-space table

When two dice are rolled there are $6\times6=36$ equally likely outcomes. A grid shows them all at once.

```figure caption="The 36 outcomes of rolling two dice. The six cells shaded blue have sum 7, so P(sum 7) = 6/36 = 1/6; the six red cells have sum 10 or more, so P(sum ≥ 10) = 6/36 = 1/6."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(4.4, 3.4))
for a in range(1, 7):
    for b in range(1, 7):
        s = a + b
        fc = 'white'
        if s == 7: fc = '#bfdbfe'
        elif s >= 10: fc = '#fecaca'
        ax.add_patch(Rectangle((a - 0.5, b - 0.5), 1, 1, fc=fc, ec=GRID, lw=0.8))
        ax.text(a, b, str(s), ha='center', va='center', fontsize=8.5)
ax.set_xlim(0.5, 6.5); ax.set_ylim(0.5, 6.5)
ax.set_xticks(range(1, 7)); ax.set_yticks(range(1, 7))
ax.set_xlabel('first die', fontsize=8.5); ax.set_ylabel('second die', fontsize=8.5)
ax.tick_params(labelsize=8); ax.set_aspect('equal')
fig.tight_layout(pad=0.4)
```

::: example Sum on two dice
**Problem.** Two fair dice are rolled. Find the probability that (a) the sum is 7, (b) the sum is at least 10, (c) both dice show the same number, (d) the sum is 8.

**Solution.** $n(S)=36$.

(a) Pairs with sum 7: $(1,6),(2,5),(3,4),(4,3),(5,2),(6,1)$: 6 outcomes, $P=\frac{6}{36}=\frac{1}{6}$.
(b) Sum 10: $(4,6),(5,5),(6,4)$; sum 11: $(5,6),(6,5)$; sum 12: $(6,6)$. Total 6, $P=\frac{1}{6}$.
(c) Doubles: $(1,1),\dots,(6,6)$: 6 outcomes, $P=\frac{1}{6}$.
(d) $(2,6),(3,5),(4,4),(5,3),(6,2)$: 5 outcomes, $P=\frac{5}{36}$.
:::

### Playing cards

A standard pack has **52 cards**: 4 suits (spades ♠, clubs ♣ black; hearts ♥, diamonds ♦ red) of 13 cards each (A, 2–10, J, Q, K). The **face cards** are J, Q, K: 12 in all. There are 4 kings, 4 aces, 26 red cards and 26 black cards.

::: example One card
**Problem.** One card is drawn from a well-shuffled pack of 52. Find the probability of (a) a king, (b) a heart, (c) a red king, (d) a face card, (e) neither a king nor a queen.

**Solution.** $n(S)=52$.

(a) $\frac{4}{52}=\frac{1}{13}$. (b) $\frac{13}{52}=\frac{1}{4}$. (c) $\frac{2}{52}=\frac{1}{26}$. (d) $\frac{12}{52}=\frac{3}{13}$.
(e) Kings and queens number 8, so $P=\frac{52-8}{52}=\frac{44}{52}=\frac{11}{13}$.
:::

### Complementary events and "at least one"

::: example Using the complement
**Problem.** A bag has 5 red, 3 blue and 2 green balls. One ball is drawn. Find $P(\text{red})$, $P(\text{not red})$ and $P(\text{blue or green})$.

**Solution.** $n(S)=10$. $P(\text{red})=\frac{5}{10}=\frac{1}{2}$. $P(\text{not red})=1-\frac{1}{2}=\frac{1}{2}$. "Blue or green" is the same as "not red": $\frac{3+2}{10}=\frac{1}{2}$.
:::

::: example Finding an unknown number of objects
**Problem.** A bag has 4 red balls and $x$ blue balls. If $P(\text{blue})=\frac{3}{5}$, find $x$.

**Solution.** Total balls $=4+x$.

$$ \frac{x}{4+x}=\frac{3}{5} \;\Rightarrow\; 5x=3(4+x) \;\Rightarrow\; 5x=12+3x \;\Rightarrow\; x=6 $$

**Check.** $\frac{6}{10}=\frac{3}{5}$ ✓.
:::

::: example Expected number
**Problem.** The probability that it rains on a day in July is 0.3. On about how many of the 31 days of July would you expect rain? A fair coin is tossed 200 times: how many heads are expected?

**Solution.** Expected rainy days $=31\times0.3=9.3\approx9$ days. Expected heads $=200\times\frac{1}{2}=100$.
:::

### Addition rule for "or"

Two events are **mutually exclusive** if they cannot happen together (e.g. rolling a 2 and rolling a 5 on one die).

::: key Addition rule
For any two events $A$ and $B$:
$$ P(A\cup B)=P(A)+P(B)-P(A\cap B) $$
For **mutually exclusive** events $P(A\cap B)=0$, so $P(A\cup B)=P(A)+P(B)$.

$A\cup B$ means "$A$ **or** $B$ (or both)"; $A\cap B$ means "$A$ **and** $B$".
:::

```figure caption="Venn diagram of a class of 40: 25 like football (F), 20 like cricket (C) and 10 like both. 15 like football only, 10 cricket only, 5 like neither."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
fig, ax = plt.subplots(figsize=(4.6, 3.0))
ax.add_patch(Rectangle((0, 0), 10, 6.4, fc='white', ec=INK, lw=1.1))
ax.add_patch(Circle((3.8, 3.2), 2.3, fc='#bfdbfe', ec=ACCENT, lw=1.3, alpha=0.7))
ax.add_patch(Circle((6.2, 3.2), 2.3, fc='#fecaca', ec='#dc2626', lw=1.3, alpha=0.7))
ax.text(2.7, 3.2, '15', fontsize=11, ha='center', va='center')
ax.text(5.0, 3.2, '10', fontsize=11, ha='center', va='center')
ax.text(7.3, 3.2, '10', fontsize=11, ha='center', va='center')
ax.text(0.5, 0.35, '5 neither', fontsize=9)
ax.text(2.7, 5.9, 'F', fontsize=10, color=ACCENT, ha='center'); ax.text(7.3, 5.9, 'C', fontsize=10, color='#dc2626', ha='center')
ax.text(9.7, 6.0, 'n(S) = 40', fontsize=8, ha='right')
ax.set_xlim(-0.2, 10.2); ax.set_ylim(-0.2, 6.6); ax.set_aspect('equal'); ax.axis('off')
fig.tight_layout(pad=0.3)
```

::: example King or heart
**Problem.** One card is drawn from a pack. Find $P(\text{king or heart})$.

**Solution.** $P(K)=\frac{4}{52}$, $P(H)=\frac{13}{52}$ and $P(K\cap H)=\frac{1}{52}$ (the king of hearts). By the addition rule

$$ P(K\cup H)=\frac{4}{52}+\frac{13}{52}-\frac{1}{52}=\frac{16}{52}=\frac{4}{13} $$
:::

::: example Football and cricket
**Problem.** In a class of 40 students, 25 like football, 20 like cricket and 10 like both. A student is chosen at random. Find the probability that the student likes (a) football or cricket, (b) neither, (c) only cricket.

**Solution.** $n(S)=40$.

(a) $n(F\cup C)=25+20-10=35$, so $P=\frac{35}{40}=\frac{7}{8}$.
(b) $P(\text{neither})=1-\frac{7}{8}=\frac{1}{8}$ (that is 5 students).
(c) Only cricket: $20-10=10$ students, $P=\frac{10}{40}=\frac{1}{4}$.
:::

::: example Mutually exclusive
**Problem.** A die is rolled. Find $P(\text{a 2 or a 5})$ and $P(\text{an even number or a multiple of 3})$.

**Solution.** "2" and "5" are mutually exclusive: $\frac{1}{6}+\frac{1}{6}=\frac{1}{3}$. For the second, even $=\{2,4,6\}$, multiples of 3 $=\{3,6\}$; the overlap is $\{6\}$, so $P=\frac{3}{6}+\frac{2}{6}-\frac{1}{6}=\frac{4}{6}=\frac{2}{3}$ (the outcomes are $\{2,3,4,6\}$).
:::

### Independent events and the multiplication rule

Two events are **independent** if the occurrence of one does not change the probability of the other (a coin toss and a die roll, or two draws **with replacement**).

::: key Multiplication rule
For independent events $A$ and $B$:
$$ P(A\cap B)=P(A)\times P(B) $$

For dependent events (for example drawing **without replacement**) the second probability changes: $P(A\cap B)=P(A)\times P(B\text{ after }A)$.
:::

::: example Independent events
**Problem.** $P(A)=0.6$ and $P(B)=0.5$ for independent events. Find $P(A\cap B)$ and $P(A\cup B)$.

**Solution.** $P(A\cap B)=0.6\times0.5=0.3$. $P(A\cup B)=0.6+0.5-0.3=0.8$.
:::

::: example A coin and a die
**Problem.** A coin is tossed and a die is rolled. Find $P(\text{head and a 6})$.

**Solution.** The events are independent: $\frac{1}{2}\times\frac{1}{6}=\frac{1}{12}$. (Check: 12 equally likely outcomes, one is H6.)
:::

### Tree diagrams: drawing without replacement

A **tree diagram** shows each stage of an experiment as branches, with the probability written on each branch. Multiply along a path to get the probability of that outcome; add the paths that belong to the event.

```figure caption="Tree diagram: two balls drawn without replacement from a bag of 3 red (R) and 2 blue (B). The four path probabilities 3/10, 3/10, 3/10 and 1/10 add to 1."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8, 3.4))
def br(x1, y1, x2, y2, lab, ly=0.0):
    ax.plot([x1, x2], [y1, y2], color=INK, lw=1.1)
    ax.text((x1 + x2) / 2, (y1 + y2) / 2 + ly, lab, fontsize=8.5, ha='center', color=ACCENT,
            bbox=dict(fc='white', ec='none', pad=0.6))
O = (0.2, 3.0)
br(*O, 2.4, 4.6, '3/5', 0.0); br(*O, 2.4, 1.4, '2/5', 0.0)
br(2.6, 4.6, 5.0, 5.4, '2/4'); br(2.6, 4.6, 5.0, 3.8, '2/4')
br(2.6, 1.4, 5.0, 2.2, '3/4'); br(2.6, 1.4, 5.0, 0.6, '1/4')
for (x, y, t) in [(2.5, 4.6, 'R'), (2.5, 1.4, 'B'), (5.1, 5.4, 'R'), (5.1, 3.8, 'B'), (5.1, 2.2, 'R'), (5.1, 0.6, 'B')]:
    ax.text(x, y, t, fontsize=10, ha='center', va='center', fontweight='bold',
            bbox=dict(boxstyle='circle,pad=0.2', fc='#f1f5f9', ec=INK, lw=0.9))
for y, t in [(5.4, 'RR   3/5 × 2/4 = 3/10'), (3.8, 'RB   3/5 × 2/4 = 3/10'), (2.2, 'BR   2/5 × 3/4 = 3/10'), (0.6, 'BB   2/5 × 1/4 = 1/10')]:
    ax.text(5.5, y, t, fontsize=8.5, va='center')
ax.text(0.0, 5.9, '1st draw', fontsize=8.5, color=MUTED); ax.text(3.1, 5.9, '2nd draw', fontsize=8.5, color=MUTED)
ax.set_xlim(-0.2, 9.4); ax.set_ylim(0.0, 6.3); ax.axis('off')
fig.tight_layout(pad=0.3)
```

::: example Without replacement
**Problem.** A bag contains 3 red and 2 blue balls. Two balls are drawn one after another **without replacement**. Find the probability that (a) both are red, (b) both are the same colour, (c) at least one is blue.

**Solution.** Use the tree above.

(a) $P(RR)=\frac{3}{5}\times\frac{2}{4}=\frac{3}{10}$.
(b) $P(RR)+P(BB)=\frac{3}{10}+\frac{1}{10}=\frac{4}{10}=\frac{2}{5}$.
(c) At least one blue is the complement of "both red": $1-\frac{3}{10}=\frac{7}{10}$.
:::

::: example With replacement
**Problem.** A bag has 5 red, 3 blue and 2 green balls. Two balls are drawn, the first being **replaced** before the second is drawn. Find the probability that both are red.

**Solution.** With replacement the draws are independent and $P(\text{red})=\frac{5}{10}$ each time: $\frac{1}{2}\times\frac{1}{2}=\frac{1}{4}$.

**Without replacement:** $\frac{5}{10}\times\frac{4}{9}=\frac{20}{90}=\frac{2}{9}$. Notice the probability is smaller: after one red ball is removed, fewer red balls remain.
:::

::: example Different colours
**Problem.** From the same bag (5 red, 3 blue, 2 green) two balls are drawn without replacement. Find the probability that they are of different colours.

**Solution.** Find the probability that both have the **same** colour and subtract from 1.

$$ P(\text{same})=\frac{5}{10}\cdot\frac{4}{9}+\frac{3}{10}\cdot\frac{2}{9}+\frac{2}{10}\cdot\frac{1}{9}=\frac{20+6+2}{90}=\frac{28}{90}=\frac{14}{45} $$

$$ P(\text{different})=1-\frac{14}{45}=\frac{31}{45} $$
:::

::: example Same or different with a smaller bag
**Problem.** A bag has 4 red and 6 white balls. Two are drawn without replacement. Find $P(\text{same colour})$ and $P(\text{different colours})$.

**Solution.** $P(\text{RR})=\frac{4}{10}\times\frac{3}{9}=\frac{12}{90}$ and $P(\text{WW})=\frac{6}{10}\times\frac{5}{9}=\frac{30}{90}$. Same colour: $\frac{42}{90}=\frac{7}{15}$. Different: $1-\frac{7}{15}=\frac{8}{15}$.
:::

::: example Lottery tickets
**Problem.** A lottery has 100 tickets, 5 of which win a prize. Ali buys 2 tickets. Find the probability that he wins at least one prize.

**Solution.** $P(\text{no prize})=\frac{95}{100}\times\frac{94}{99}=\frac{8930}{9900}$. So $P(\text{at least one prize})=1-\frac{8930}{9900}=\frac{970}{9900}=\frac{97}{990}\approx0.098$.
:::

::: caution Common mistakes
- Writing the sample space incompletely: for two coins there are **four** outcomes (HT and TH are different), not three.
- Treating dice sums as equally likely: the sum 7 is much more likely than the sum 2 (6 ways against 1).
- Using the same probability for both draws **without replacement**; the denominator drops by 1.
- Adding probabilities for "and" or multiplying for "or": **and** means multiply (independent), **or** means add.
- Forgetting to subtract the overlap in $P(A\cup B)$ when the events are not mutually exclusive.
- Leaving the answer as "6 out of 36" — give a fraction in lowest terms ($\frac{1}{6}$) or a decimal.
:::

## 18.2 Exercises of the SEE type

### Method for any question

1. Decide the experiment and write the sample space (a list, a table or a tree). State $n(S)$.
2. Write the favourable outcomes and $n(E)$.
3. $P(E)=\frac{n(E)}{n(S)}$; reduce the fraction.
4. "At least one": use $1-P(\text{none})$.
5. For two stages, decide **with** or **without** replacement, draw a tree and multiply along branches.
6. Check that all branch probabilities in a tree add to 1.

::: example SEE type: dice and coins
**Problem.** A coin is tossed and a die is rolled together. Write the sample space and find (a) $P(\text{head and an even number})$, (b) $P(\text{tail and a number less than 3})$.

**Solution.** $S=\{H1,H2,H3,H4,H5,H6,T1,T2,T3,T4,T5,T6\}$, $n(S)=12$.

(a) H2, H4, H6: $P=\frac{3}{12}=\frac{1}{4}$.
(b) T1, T2: $P=\frac{2}{12}=\frac{1}{6}$.
:::

::: example SEE type: sums of two dice
**Problem.** Two dice are thrown. Find the probability that the sum is (a) less than 4, (b) a multiple of 5, (c) the numbers differ by 2.

**Solution.** $n(S)=36$.

(a) Sum 2: $(1,1)$; sum 3: $(1,2),(2,1)$. Total 3, $P=\frac{3}{36}=\frac{1}{12}$.
(b) Sum 5: $(1,4),(2,3),(3,2),(4,1)$ — 4; sum 10: $(4,6),(5,5),(6,4)$ — 3. Total 7, $P=\frac{7}{36}$.
(c) Pairs with $|a-b|=2$: $(1,3),(3,1),(2,4),(4,2),(3,5),(5,3),(4,6),(6,4)$ — 8, $P=\frac{8}{36}=\frac{2}{9}$.
:::

::: example SEE type: cards
**Problem.** A card is drawn at random from a pack of 52. Find the probability that it is (a) a black card, (b) an ace or a spade, (c) neither a heart nor a king.

**Solution.** (a) $\frac{26}{52}=\frac{1}{2}$. (b) Aces 4, spades 13, overlap 1: $\frac{4+13-1}{52}=\frac{16}{52}=\frac{4}{13}$. (c) Hearts or kings: $13+4-1=16$ cards, so neither $=\frac{52-16}{52}=\frac{36}{52}=\frac{9}{13}$.
:::

## Chapter summary

- $P(E)=\frac{n(E)}{n(S)}$ for equally likely outcomes; $0\leq P(E)\leq1$.
- Complement: $P(E')=1-P(E)$. "At least one" $=1-P(\text{none})$.
- Addition rule: $P(A\cup B)=P(A)+P(B)-P(A\cap B)$; for mutually exclusive events $P(A\cap B)=0$.
- Multiplication rule for independent events: $P(A\cap B)=P(A)\times P(B)$.
- Without replacement the second probability changes; use a tree diagram and multiply along each path.
- Two dice: 36 outcomes; two coins: 4; three coins: 8; pack of cards: 52.
- Expected frequency $=N\times P(E)$.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The probability of an impossible event is <span class="marks">[1]</span>
   (a) 0 (b) $\frac{1}{2}$ (c) 1 (d) $-1$
2. A fair die is rolled. $P(\text{an even number})$ is <span class="marks">[1]</span>
   (a) $\frac{1}{6}$ (b) $\frac{1}{3}$ (c) $\frac{1}{2}$ (d) $\frac{2}{3}$
3. $P(E)+P(E')$ equals <span class="marks">[1]</span>
   (a) 0 (b) $\frac{1}{2}$ (c) 1 (d) $P(E)$
4. The number of outcomes when two dice are rolled is <span class="marks">[1]</span>
   (a) 12 (b) 18 (c) 36 (d) 6
5. The probability of drawing a king from a pack of 52 cards is <span class="marks">[1]</span>
   (a) $\frac{1}{52}$ (b) $\frac{1}{13}$ (c) $\frac{1}{4}$ (d) $\frac{4}{13}$

::: note Answers to Group A
**1.** (a).
**2.** (c) — 3 of 6.
**3.** (c).
**4.** (c) — $6\times6$.
**5.** (b) — $\frac{4}{52}$.
:::

**Group B — Short answer (2 marks each)**

1. Two coins are tossed. Find the probability of at least one head. <span class="marks">[2]</span>
2. A die is rolled. Find $P(\text{a prime number})$. <span class="marks">[2]</span>
3. A bag has 5 red and 3 blue balls. Find $P(\text{blue})$. <span class="marks">[2]</span>
4. If $P(E)=0.35$, find $P(E')$. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** $\frac{3}{4}$.
**2.** Primes $\{2,3,5\}$: $\frac{3}{6}=\frac{1}{2}$.
**3.** $\frac{3}{8}$.
**4.** $1-0.35=0.65$.
:::

**Group C — Short answer (3 marks each)**

1. Two dice are thrown. Find the probability that the sum is 7. <span class="marks">[3]</span>
2. A card is drawn from a pack of 52. Find $P(\text{king or heart})$. <span class="marks">[3]</span>
3. A bag has 4 red balls and $x$ blue balls. If $P(\text{blue})=\frac{3}{5}$, find $x$. <span class="marks">[3]</span>
4. In a class of 40, 25 like football, 20 like cricket and 10 like both. Find $P(\text{neither})$. <span class="marks">[3]</span>

::: note Answers to Group C
**1.** $\frac{6}{36}=\frac{1}{6}$.
**2.** $\frac{4+13-1}{52}=\frac{4}{13}$.
**3.** $\frac{x}{4+x}=\frac{3}{5}$, $x=6$.
**4.** $1-\frac{35}{40}=\frac{1}{8}$.
:::

**Group D — Long answer (4 marks each)**

1. A bag contains 3 red and 2 blue balls. Two are drawn without replacement. Draw a tree diagram and find $P(\text{both red})$ and $P(\text{at least one blue})$. <span class="marks">[4]</span>
2. A bag has 5 red, 3 blue and 2 green balls. Two balls are drawn without replacement. Find the probability that both are red and the probability that they are of different colours. <span class="marks">[4]</span>
3. Two dice are thrown. Find the probability that the sum is at least 10, and the probability that the numbers on the two dice are equal. <span class="marks">[4]</span>
4. A bag has 4 red and 6 white balls. Two are drawn without replacement. Find $P(\text{same colour})$ and $P(\text{different colours})$. <span class="marks">[4]</span>

::: note Answers to Group D
**1.** $P(RR)=\frac{3}{5}\times\frac{2}{4}=\frac{3}{10}$; $P(\text{at least one blue})=1-\frac{3}{10}=\frac{7}{10}$.
**2.** $P(RR)=\frac{5}{10}\times\frac{4}{9}=\frac{2}{9}$; $P(\text{different})=1-\frac{14}{45}=\frac{31}{45}$.
**3.** $\frac{6}{36}=\frac{1}{6}$ and $\frac{6}{36}=\frac{1}{6}$.
**4.** $\frac{12}{90}+\frac{30}{90}=\frac{7}{15}$; different $=\frac{8}{15}$.
:::
