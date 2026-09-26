---
subject: Mathematics
grade: 11
unit: 16
title: Probability
hours: 6
area: Statistics and Probability
---

Probability is the mathematics of uncertainty: it attaches a number between $0$
and $1$ to an event, measuring how likely that event is. The whole subject rests
on carefully counting the possible outcomes of an experiment, and then on two
laws — one for "or", one for "and" — that let you build complicated probabilities
out of simple ones.

::: key What the exam wants
Nearly every question is one of three kinds: *count the favourable cases* and
divide (mathematical definition), *use the addition law* when the question says
"or", or *use the multiplication law* when it says "and" / "both" / "one after
another". The hard part is never the arithmetic — it is deciding whether the
events are mutually exclusive, and whether they are independent.
:::

## 16.1 Independent cases

Before any formula, the vocabulary. A **random experiment** is one whose result
cannot be predicted in advance, although all its possible results are known — for
example tossing a coin or rolling a die. One performance of the experiment is a
**trial**, each possible result is an **outcome** or a **case**, the set of all
outcomes is the **sample space** $S$, and any subset of $S$ is an **event**.

For a single roll of a die, $S = \{1,2,3,4,5,6\}$ with $n(S) = 6$; the event "an
even number appears" is $A = \{2,4,6\}$ with $n(A) = 3$.

```figure caption="The sample space for rolling two dice: $n(S) = 36$ equally likely ordered pairs. The shaded diagonal is the event 'the sum is $8$', with $5$ favourable cases, so $P = 5/36$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.4,3.3))
for i in range(1,7):
    for j in range(1,7):
        hit = (i+j==8)
        ax.add_patch(plt.Rectangle((j-0.5,i-0.5),1,1,
                     facecolor=(SERIES[1] if hit else '#ffffff'),
                     alpha=(0.28 if hit else 1.0),
                     edgecolor=GRID,lw=0.8,zorder=0))
        ax.text(j,i,f'{i+j}',ha='center',va='center',fontsize=7.6,
                color=(SERIES[1] if hit else MUTED),
                fontweight=('bold' if hit else 'normal'))
ax.set_xticks(range(1,7)); ax.set_yticks(range(1,7))
ax.set_xlabel('score on the second die'); ax.set_ylabel('score on the first die')
ax.set_xlim(0.5,6.5); ax.set_ylim(0.5,6.5); ax.set_aspect('equal')
ax.spines[['top','right']].set_visible(False)
ax.tick_params(length=0)
```

::: definition The kinds of cases
For a random experiment:

- **Exhaustive cases**: all the possible outcomes taken together. Rolling a die
  has $6$ exhaustive cases; rolling two dice has $6\times6 = 36$.
- **Favourable cases** for an event $A$: the outcomes in which $A$ happens.
- **Equally likely cases**: no outcome has any preference over another (a fair
  coin, an unbiased die).
- **Mutually exclusive (disjoint) cases**: two events that cannot happen in the
  same trial — $A \cap B = \varnothing$.
- **Independent cases**: two events such that the occurrence of one does **not**
  affect the probability of the other.
- **Complementary event** $\bar{A}$: the event that $A$ does not happen.
:::

Independence is a statement about two *different* experiments or stages, or about
sampling **with** replacement. Drawing a card, replacing it, and drawing again
gives two independent draws; drawing two cards without replacement does not,
because the first draw changes what is left in the pack.

::: caution Mutually exclusive $\ne$ independent
These two words describe opposite situations and students swap them constantly.
Mutually exclusive events **cannot occur together**, so if one happens the other
certainly does not — that is the strongest possible *dependence*. Independent
events, by contrast, can happily occur together; knowing about one simply tells
you nothing about the other. In symbols: mutually exclusive means
$P(A \cap B) = 0$; independent means $P(A\cap B) = P(A)P(B)$.
:::

::: example Worked example 16.1
**Problem.** Two coins are tossed together. (a) Write the sample space and
$n(S)$. (b) List the favourable cases for $A$ = "exactly one head" and
$B$ = "at least one tail". (c) Are $A$ and $B$ mutually exclusive?

**Solution.**

(a) Each coin can fall $H$ or $T$, so $S = \{HH, HT, TH, TT\}$ and $n(S) = 4$.
All four are equally likely.

(b) $A = \{HT, TH\}$, so $n(A) = 2$. $B = \{HT, TH, TT\}$, so $n(B) = 3$.

(c) $A \cap B = \{HT, TH\} \ne \varnothing$, so the two events **can** occur
together (for instance the outcome $HT$). They are **not** mutually exclusive.
:::

## 16.2 Mathematical and empirical definition of probability

::: definition Mathematical (classical) definition
If a random experiment has $n$ exhaustive, mutually exclusive and **equally
likely** cases, of which $m$ are favourable to an event $A$, then
$$ P(A) = \frac{\text{number of favourable cases}}{\text{total number of cases}} = \frac{m}{n} = \frac{n(A)}{n(S)} $$
:::

Three consequences follow immediately:

- $0 \leq P(A) \leq 1$; $P(A) = 0$ for an impossible event and $P(A) = 1$ for a
  certain event.
- The probability that $A$ does not happen is
  $P(\bar{A}) = \dfrac{n-m}{n} = 1 - P(A)$.
- **Odds.** The odds in favour of $A$ are $m : (n-m)$ and the odds against $A$ are
  $(n-m) : m$. If the odds in favour are $a:b$ then $P(A) = \dfrac{a}{a+b}$.

::: caution "Equally likely" is a condition, not a decoration
The classical formula is only valid when the cases are equally likely. "It either
rains tomorrow or it does not, so $P(\text{rain}) = 1/2$" is wrong, because those
two cases are not equally likely. For such situations we need the empirical
definition below.
:::

::: definition Empirical (statistical) definition
If an experiment is repeated $n$ times under identical conditions and the event
$A$ occurs $m$ times, the **empirical probability** of $A$ is the limit of the
relative frequency:
$$ P(A) = \lim_{n \to \infty}\frac{m}{n} $$
In practice $m/n$ for a large $n$ is taken as an estimate of $P(A)$.
:::

```figure caption="Empirical probability at work: the proportion of heads in a simulated run of coin tosses. It jumps about for small $n$ but settles towards the mathematical value $0.5$ as $n$ grows — this stabilising is what the definition means by the limit."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.9,2.8))
rng=np.random.default_rng(11)
n=2000
for c,alp in [(ACCENT,1.0),(SERIES[2],0.75),(SERIES[3],0.6)]:
    tosses=rng.integers(0,2,n)
    prop=np.cumsum(tosses)/np.arange(1,n+1)
    ax.plot(np.arange(1,n+1),prop,color=c,lw=1.2,alpha=alp)
ax.axhline(0.5,color=SERIES[1],lw=1.5,ls=(0,(4,2)))
ax.annotate('$P(\\mathrm{head}) = 0.5$',(1700,0.56),color=SERIES[1],fontsize=9.0,ha='right')
ax.set_xscale('log')
ax.set_xlabel('number of tosses  $n$  (log scale)')
ax.set_ylabel('proportion of heads  $m/n$')
ax.set_ylim(-0.03,1.03); ax.set_xlim(1,n)
ax.spines[['top','right']].set_visible(False); ax.grid(alpha=0.45)
```

::: example Worked example 16.2
**Problem.** Two fair dice are rolled together. Find the probability that
(a) the sum is $8$, (b) the sum is at least $10$, (c) a doublet appears.

**Solution.** Each die has $6$ faces, so $n(S) = 6\times6 = 36$ equally likely
ordered pairs (see the grid above).

(a) Sum $8$: $(2,6),(3,5),(4,4),(5,3),(6,2)$ — that is $5$ cases.

$$ P(\text{sum } 8) = \frac{5}{36} $$

(b) Sum at least $10$ means sum $= 10, 11$ or $12$:
$(4,6),(5,5),(6,4)$; $(5,6),(6,5)$; $(6,6)$ — that is $3+2+1 = 6$ cases.

$$ P(\text{sum} \geq 10) = \frac{6}{36} = \frac{1}{6} $$

(c) A doublet is $(1,1),(2,2),\ldots,(6,6)$ — $6$ cases.

$$ P(\text{doublet}) = \frac{6}{36} = \frac{1}{6} $$
:::

::: example Worked example 16.3
**Problem.** One card is drawn at random from a well-shuffled pack of $52$ playing
cards. Find the probability that it is (a) a king, (b) a face card, (c) not a
spade. Also state the odds against drawing a king.

**Solution.** $n(S) = 52$ and every card is equally likely.

(a) There are $4$ kings: $P(K) = \dfrac{4}{52} = \dfrac{1}{13}$.

(b) Face cards are the jack, queen and king of each of the $4$ suits, so
$4\times3 = 12$ cards: $P(F) = \dfrac{12}{52} = \dfrac{3}{13}$.

(c) There are $13$ spades, so using the complement,

$$ P(\text{not a spade}) = 1 - \frac{13}{52} = 1 - \frac{1}{4} = \frac{3}{4} $$

Odds against a king $=$ (unfavourable) : (favourable) $= 48 : 4 = 12 : 1$.
:::

::: example Worked example 16.4
**Problem.** (a) In a quality check on $1000$ bulbs made at a factory in Balaju,
$25$ were found defective. Estimate the probability that a bulb picked at random
from the day's production is defective. (b) The odds in favour of a football team
winning a match are $3:5$. Find the probability that it wins, and the probability
that it does not.

**Solution.**

(a) This is an empirical probability, from observed frequencies:

$$ P(\text{defective}) = \frac{m}{n} = \frac{25}{1000} = 0.025 $$

so about $2.5\%$ of the production is expected to be defective.

(b) Odds in favour $a:b = 3:5$ means $3$ favourable cases to $5$ unfavourable, a
total of $8$:

$$ P(\text{win}) = \frac{3}{3+5} = \frac{3}{8}, \qquad P(\text{not win}) = 1 - \frac{3}{8} = \frac{5}{8} $$
:::

## 16.3 Two basic laws of probability

### The addition law — for "or"

::: key Addition law (stated without proof)
For any two events $A$ and $B$ of the same sample space,
$$ P(A \cup B) = P(A) + P(B) - P(A \cap B) $$
If $A$ and $B$ are **mutually exclusive** then $A \cap B = \varnothing$, so
$P(A\cap B) = 0$ and the law reduces to
$$ P(A \cup B) = P(A) + P(B) $$
For three events,
$P(A\cup B\cup C) = P(A)+P(B)+P(C)-P(A\cap B)-P(B\cap C)-P(C\cap A)+P(A\cap B\cap C)$.
:::

The subtraction is easy to see on a Venn diagram: adding $P(A)$ and $P(B)$ counts
the overlap twice, so it must be removed once.

```figure caption="(a) Mutually exclusive events: no overlap, so $P(A\cup B)=P(A)+P(B)$. (b) Overlapping events: adding the two circles counts the shaded region $A\cap B$ twice, so it must be subtracted once."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
fig, axes = plt.subplots(1,2,figsize=(5.1,2.5))
for k,ax in enumerate(axes):
    ax.add_patch(Rectangle((0,0),6,3.4,facecolor='#f4f6f9',edgecolor=MUTED,lw=1.0))
    ax.annotate('$S$',(0.22,3.06),color=MUTED,fontsize=9.5)
    if k==0:
        c1=Circle((1.75,1.65),1.05,facecolor=ACCENT,alpha=0.20,edgecolor=ACCENT,lw=1.4)
        c2=Circle((4.25,1.65),1.05,facecolor=SERIES[2],alpha=0.20,edgecolor=SERIES[2],lw=1.4)
        ax.add_patch(c1); ax.add_patch(c2)
        ax.annotate('$A$',(1.75,1.55),color=ACCENT,fontsize=11,ha='center')
        ax.annotate('$B$',(4.25,1.55),color=SERIES[2],fontsize=11,ha='center')
        ax.annotate('$A\\cap B=\\varnothing$',(3.0,0.32),color=INK,fontsize=9.0,ha='center')
        ax.set_title('(a) mutually exclusive',fontsize=9.2)
    else:
        c1=Circle((2.35,1.75),1.25,facecolor=ACCENT,alpha=0.20,edgecolor=ACCENT,lw=1.4)
        c2=Circle((3.75,1.75),1.25,facecolor=SERIES[2],alpha=0.20,edgecolor=SERIES[2],lw=1.4)
        ax.add_patch(c1); ax.add_patch(c2)
        r=1.25; d=(3.75-2.35)/2.0; a=np.arccos(d/r)
        t1=np.linspace(-a,a,120)
        t2=np.linspace(np.pi-a,np.pi+a,120)
        xs=list(2.35+r*np.cos(t1))+list(3.75+r*np.cos(t2[::-1]))
        ys=list(1.75+r*np.sin(t1))+list(1.75+r*np.sin(t2[::-1]))
        ax.fill(xs,ys,color=SERIES[1],alpha=0.30,lw=0)
        ax.annotate('$A$',(1.60,1.65),color=ACCENT,fontsize=11,ha='center')
        ax.annotate('$B$',(4.50,1.65),color=SERIES[2],fontsize=11,ha='center')
        ax.annotate('$A\\cap B$',(3.05,1.65),color=SERIES[1],fontsize=9.0,ha='center')
        ax.set_title('(b) not mutually exclusive',fontsize=9.2)
    ax.set_xlim(-0.15,6.15); ax.set_ylim(-0.15,3.55)
    ax.set_aspect('equal'); ax.axis('off')
```

::: example Worked example 16.5
**Problem.** A card is drawn from a pack of $52$. Find the probability that it is
(a) a king or a queen, (b) a king or a heart.

**Solution.**

(a) A card cannot be a king *and* a queen at once, so these events are mutually
exclusive:

$$ P(K \cup Q) = P(K) + P(Q) = \frac{4}{52} + \frac{4}{52} = \frac{8}{52} = \frac{2}{13} $$

(b) A card **can** be both a king and a heart — the king of hearts — so the events
are not mutually exclusive and the overlap must be subtracted:

$$ P(K \cup H) = P(K) + P(H) - P(K \cap H) = \frac{4}{52} + \frac{13}{52} - \frac{1}{52} = \frac{16}{52} = \frac{4}{13} $$
:::

::: example Worked example 16.6
**Problem.** In a class of $60$ students, $35$ play football, $30$ play cricket
and $15$ play both. A student is chosen at random. Find the probability that the
student (a) plays at least one of the two games, (b) plays neither, (c) plays
football only.

**Solution.** Let $F$ and $C$ be the two events. Then $P(F) = 35/60$,
$P(C) = 30/60$, $P(F\cap C) = 15/60$.

(a) By the addition law,

$$ P(F\cup C) = \frac{35}{60} + \frac{30}{60} - \frac{15}{60} = \frac{50}{60} = \frac{5}{6} $$

(b) "Neither" is the complement of "at least one":

$$ P(\overline{F\cup C}) = 1 - \frac{5}{6} = \frac{1}{6} $$

(c) Football only means $F$ but not $C$: $35 - 15 = 20$ students, so
$P = \dfrac{20}{60} = \dfrac{1}{3}$.
:::

```figure caption="The class of Worked example 16.6 as a Venn diagram. Filling the overlap first ($15$) and then subtracting is the safe way to do every survey question; the four regions must add to $60$."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
fig, ax = plt.subplots(figsize=(4.4,2.7))
ax.add_patch(Rectangle((0,0),6.4,4.1,facecolor='#f4f6f9',edgecolor=MUTED,lw=1.0))
ax.add_patch(Circle((2.5,1.95),1.35,facecolor=ACCENT,alpha=0.18,edgecolor=ACCENT,lw=1.4))
ax.add_patch(Circle((3.9,1.95),1.35,facecolor=SERIES[2],alpha=0.18,edgecolor=SERIES[2],lw=1.4))
ax.annotate('$S$: 60 students',(0.18,3.74),color=MUTED,fontsize=9.0)
ax.annotate('football $F$',(1.85,3.42),color=ACCENT,fontsize=9.0,ha='center')
ax.annotate('cricket $C$',(4.75,3.42),color=SERIES[2],fontsize=9.0,ha='center')
ax.annotate('20',(1.95,1.90),color=ACCENT,fontsize=12,ha='center')
ax.annotate('15',(3.20,1.90),color=SERIES[1],fontsize=12,ha='center')
ax.annotate('15',(4.45,1.90),color=SERIES[2],fontsize=12,ha='center')
ax.annotate('10',(0.75,0.55),color=MUTED,fontsize=12,ha='center')
ax.annotate('neither game',(0.95,0.18),color=MUTED,fontsize=8.0,ha='center')
ax.set_xlim(-0.2,6.6); ax.set_ylim(-0.25,4.35); ax.set_aspect('equal'); ax.axis('off')
```

### The multiplication law — for "and"

::: key Multiplication law (stated without proof)
For any two events,
$$ P(A \cap B) = P(A)\cdot P(B|A) = P(B)\cdot P(A|B) $$
where $P(B|A)$ is the **conditional probability** of $B$ given that $A$ has already
happened. If $A$ and $B$ are **independent** then $P(B|A) = P(B)$ and the law
reduces to
$$ P(A \cap B) = P(A)\cdot P(B) $$
Rearranging the first form gives the working formula for conditional probability:
$$ P(B|A) = \frac{P(A\cap B)}{P(A)}, \qquad P(A) \ne 0 $$
:::

::: memory Translating the words
| The question says | You need |
|---|---|
| "or", "at least one of" | addition law |
| "and", "both", "in succession" | multiplication law |
| "with replacement", "two different people" | independent: multiply the plain probabilities |
| "without replacement", "one after another from the same box" | dependent: the second probability changes |
| "at least one" | often easiest as $1 - P(\text{none})$ |
:::

```figure caption="Tree diagram for drawing two balls, without replacement, from a bag of $5$ red and $3$ black. The second-stage probabilities have denominator $7$, not $8$ — that is what 'dependent' means. Multiply along a branch; add the branches you want."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,2.9))
def branch(p0,p1,lab,c,lo):
    ax.annotate('',xy=p1,xytext=p0,arrowprops=dict(arrowstyle='-',color=c,lw=1.5))
    m=((p0[0]+p1[0])/2,(p0[1]+p1[1])/2)
    ax.annotate(lab,m,textcoords='offset points',xytext=lo,color=c,fontsize=8.6,ha='center')
O=(0.15,1.55)
R=(1.75,2.45); B=(1.75,0.65)
branch(O,R,'$5/8$',ACCENT,(-2,10)); branch(O,B,'$3/8$',SERIES[2],(-2,-13))
ends=[(R,(3.55,3.00),'$4/7$',ACCENT,'RR',  '$\\frac{5}{8}\\cdot\\frac{4}{7}=\\frac{5}{14}$'),
      (R,(3.55,1.95),'$3/7$',SERIES[2],'RB','$\\frac{5}{8}\\cdot\\frac{3}{7}=\\frac{15}{56}$'),
      (B,(3.55,1.10),'$5/7$',ACCENT,'BR',  '$\\frac{3}{8}\\cdot\\frac{5}{7}=\\frac{15}{56}$'),
      (B,(3.55,0.10),'$2/7$',SERIES[2],'BB','$\\frac{3}{8}\\cdot\\frac{2}{7}=\\frac{3}{28}$')]
for p0,p1,lab,c,name,val in ends:
    branch(p0,p1,lab,c,(-2,8) if p1[1]>p0[1] else (-2,-12))
    ax.annotate(name,p1,textcoords='offset points',xytext=(6,0),color=INK,
                fontsize=9.2,va='center',fontweight='bold')
    ax.annotate(val,p1,textcoords='offset points',xytext=(28,0),color=MUTED,
                fontsize=8.6,va='center')
for p,lab,c in [(O,'start',INK),(R,'R',ACCENT),(B,'B',SERIES[2])]:
    ax.plot([p[0]],[p[1]],'o',color=c,ms=5)
    ax.annotate(lab,p,textcoords='offset points',xytext=(-4,0),color=c,
                fontsize=9.2,ha='right',va='center')
ax.annotate('1st draw',(1.75,3.42),color=MUTED,fontsize=8.4,ha='center')
ax.annotate('2nd draw',(3.55,3.42),color=MUTED,fontsize=8.4,ha='center')
ax.set_xlim(-0.75,5.9); ax.set_ylim(-0.35,3.65); ax.axis('off')
```

::: example Worked example 16.7
**Problem.** A bag contains $5$ red and $3$ black balls. Two balls are drawn one
after another **without replacement**. Find the probability that (a) both are red,
(b) both are black, (c) one is of each colour.

**Solution.** The draws are dependent: after the first ball is taken out only $7$
balls remain.

(a) $P(\text{red first}) = \dfrac{5}{8}$, and then $4$ red remain out of $7$:

$$ P(RR) = \frac{5}{8}\times\frac{4}{7} = \frac{20}{56} = \frac{5}{14} $$

(b) $P(BB) = \dfrac{3}{8}\times\dfrac{2}{7} = \dfrac{6}{56} = \dfrac{3}{28}$

(c) "One of each" happens two ways, $RB$ or $BR$, and these are mutually
exclusive, so add them:

$$ P(RB) + P(BR) = \frac{5}{8}\cdot\frac{3}{7} + \frac{3}{8}\cdot\frac{5}{7} = \frac{15}{56} + \frac{15}{56} = \frac{30}{56} = \frac{15}{28} $$

Check: $\dfrac{5}{14} + \dfrac{3}{28} + \dfrac{15}{28} = \dfrac{10 + 3 + 15}{28} = 1$ ✔
:::

::: example Worked example 16.8
**Problem.** The probability that Sita solves a problem is $\frac{1}{2}$ and that
Gopal solves it is $\frac{1}{3}$. They try independently. Find the probability
that (a) both solve it, (b) neither solves it, (c) the problem is solved,
(d) exactly one of them solves it.

**Solution.** Let $A$ and $B$ be the events that Sita and Gopal solve it. They are
independent, so $P(\bar{A}) = \frac{1}{2}$ and $P(\bar{B}) = \frac{2}{3}$.

(a) $P(A\cap B) = P(A)P(B) = \dfrac{1}{2}\times\dfrac{1}{3} = \dfrac{1}{6}$

(b) $P(\bar{A}\cap\bar{B}) = \dfrac{1}{2}\times\dfrac{2}{3} = \dfrac{1}{3}$

(c) "Solved" means at least one succeeds — the complement of (b):

$$ P(A\cup B) = 1 - \frac{1}{3} = \frac{2}{3} $$

(The addition law gives the same thing:
$\frac{1}{2}+\frac{1}{3}-\frac{1}{6} = \frac{2}{3}$ ✔)

(d) Exactly one means ($A$ and not $B$) or (not $A$ and $B$):

$$ P = \frac{1}{2}\cdot\frac{2}{3} + \frac{1}{2}\cdot\frac{1}{3} = \frac{1}{3} + \frac{1}{6} = \frac{1}{2} $$
:::

::: tip "At least one" is almost always a complement
For $n$ independent events, $P(\text{at least one occurs}) = 1 - P(\text{none occurs})$.
Listing all the ways of getting "at least one" wastes time and loses marks to
arithmetic slips; one subtraction does the whole job.
:::

::: example Worked example 16.9
**Problem.** A fair coin is tossed three times. Find the probability of getting
at least one head.

**Solution.** The tosses are independent and $P(\text{tail}) = \frac{1}{2}$ each
time, so

$$ P(\text{no head}) = P(TTT) = \frac{1}{2}\times\frac{1}{2}\times\frac{1}{2} = \frac{1}{8} $$

$$ P(\text{at least one head}) = 1 - \frac{1}{8} = \frac{7}{8} $$

(Counting directly, $n(S) = 2^{3} = 8$ and only $TTT$ has no head — the same $7/8$.)
:::

::: example Worked example 16.10
**Problem.** The result of an examination in a school of $100$ students is:

| | Passed | Failed | Total |
|---|---|---|---|
| Boys | 45 | 15 | 60 |
| Girls | 35 | 5 | 40 |
| **Total** | **80** | **20** | **100** |

A student is chosen at random. Find (a) $P(\text{pass})$, (b) the probability that
the student passed given that she is a girl, (c) are "being a girl" and "passing"
independent?

**Solution.**

(a) $P(\text{pass}) = \dfrac{80}{100} = 0.8$

(b) Restrict attention to the $40$ girls, of whom $35$ passed:

$$ P(\text{pass}\,|\,\text{girl}) = \frac{n(\text{pass} \cap \text{girl})}{n(\text{girl})} = \frac{35}{40} = \frac{7}{8} = 0.875 $$

The same answer from the formula:
$P(\text{pass}|\text{girl}) = \dfrac{P(\text{pass}\cap\text{girl})}{P(\text{girl})}
= \dfrac{35/100}{40/100} = \dfrac{35}{40}$.

(c) Independence would require $P(\text{pass}|\text{girl}) = P(\text{pass})$. Here
$0.875 \ne 0.8$, so the two events are **not** independent: being a girl in this
school raises the chance of passing.
:::

```figure caption="Tree diagram for a two-stage experiment: pick one of two bags at random, then draw a ball. Multiply along each path, then add the two paths that give a white ball: $P(W) = \frac{3}{10}+\frac{1}{6} = \frac{7}{15}$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,2.7))
def branch(p0,p1,lab,c,lo):
    ax.annotate('',xy=p1,xytext=p0,arrowprops=dict(arrowstyle='-',color=c,lw=1.5))
    m=((p0[0]+p1[0])/2,(p0[1]+p1[1])/2)
    ax.annotate(lab,m,textcoords='offset points',xytext=lo,color=c,fontsize=8.6,ha='center')
O=(0.15,1.45); I=(1.70,2.45); II=(1.70,0.45)
branch(O,I,'$1/2$',INK,(-2,10)); branch(O,II,'$1/2$',INK,(-2,-13))
paths=[(I,(3.35,3.05),'$3/5$',ACCENT,'white','$\\frac{1}{2}\\cdot\\frac{3}{5}=\\frac{3}{10}$'),
       (I,(3.35,2.05),'$2/5$',MUTED,'black','$\\frac{1}{2}\\cdot\\frac{2}{5}=\\frac{1}{5}$'),
       (II,(3.35,0.90),'$2/6$',ACCENT,'white','$\\frac{1}{2}\\cdot\\frac{2}{6}=\\frac{1}{6}$'),
       (II,(3.35,-0.10),'$4/6$',MUTED,'black','$\\frac{1}{2}\\cdot\\frac{4}{6}=\\frac{1}{3}$')]
for p0,p1,lab,c,name,val in paths:
    branch(p0,p1,lab,c,(-2,8) if p1[1]>p0[1] else (-2,-12))
    ax.annotate(name,p1,textcoords='offset points',xytext=(6,0),color=c,fontsize=8.8,va='center')
    ax.annotate(val,p1,textcoords='offset points',xytext=(36,0),color=INK,fontsize=8.6,va='center')
for p,lab,c,off in [(O,'start',INK,(-6,0)),(I,'Bag I\n3W, 2B',ACCENT,(-24,17)),
                    (II,'Bag II\n2W, 4B',SERIES[2],(-24,-17))]:
    ax.plot([p[0]],[p[1]],'o',color=c,ms=5)
    ax.annotate(lab,p,textcoords='offset points',xytext=off,color=c,fontsize=8.6,
                ha=('right' if p is O else 'center'),va='center')
ax.set_xlim(-1.1,5.9); ax.set_ylim(-0.75,3.55); ax.axis('off')
```

::: example Worked example 16.11
**Problem.** Bag I contains $3$ white and $2$ black balls; bag II contains $2$
white and $4$ black balls. A bag is chosen at random and one ball is drawn from
it. Find the probability that the ball is white.

**Solution.** Each bag is equally likely, so $P(\text{I}) = P(\text{II}) = \frac{1}{2}$.
Use the multiplication law along each path and then add the paths (they are
mutually exclusive).

$$ P(\text{I and white}) = \frac{1}{2}\times\frac{3}{5} = \frac{3}{10} $$

$$ P(\text{II and white}) = \frac{1}{2}\times\frac{2}{6} = \frac{1}{6} $$

$$ P(\text{white}) = \frac{3}{10} + \frac{1}{6} = \frac{9}{30} + \frac{5}{30} = \frac{14}{30} = \frac{7}{15} $$
:::

::: example Worked example 16.12
**Problem.** $A$ and $B$ are independent events with $P(A) = 0.4$ and
$P(B) = 0.5$. Find (a) $P(A\cap B)$, (b) $P(A\cup B)$, (c) $P(A|B)$.

**Solution.**

(a) Independence lets us multiply: $P(A\cap B) = 0.4\times0.5 = 0.2$.

(b) By the addition law,

$$ P(A\cup B) = 0.4 + 0.5 - 0.2 = 0.7 $$

(c) $P(A|B) = \dfrac{P(A\cap B)}{P(B)} = \dfrac{0.2}{0.5} = 0.4 = P(A)$ — exactly what
independence means: knowing $B$ happened does not change the chance of $A$.
:::

## Chapter summary

- A random experiment has a sample space $S$; an event is a subset of $S$.
  Cases may be exhaustive, equally likely, mutually exclusive
  ($A\cap B = \varnothing$) or independent (one does not affect the other).
- Mathematical definition: $P(A) = \dfrac{n(A)}{n(S)} = \dfrac{m}{n}$, valid only
  for equally likely cases. $0 \leq P(A) \leq 1$ and $P(\bar{A}) = 1 - P(A)$.
- Empirical definition: $P(A) = \lim_{n\to\infty} \dfrac{m}{n}$, the limiting
  relative frequency in repeated trials.
- Odds in favour $a:b$ $\Longleftrightarrow$ $P(A) = \dfrac{a}{a+b}$.
- Addition law: $P(A\cup B) = P(A)+P(B)-P(A\cap B)$; for mutually exclusive events
  $P(A\cup B) = P(A)+P(B)$.
- Multiplication law: $P(A\cap B) = P(A)P(B|A)$; for independent events
  $P(A\cap B) = P(A)P(B)$. Conditional probability
  $P(B|A) = \dfrac{P(A\cap B)}{P(A)}$.
- For two dice $n(S) = 36$; for $n$ coins $n(S) = 2^{n}$; for a pack of cards
  $n(S) = 52$ with $4$ suits of $13$, $12$ face cards and $26$ red.
- "At least one" $= 1 - P(\text{none})$. Draw a tree for multi-stage problems:
  multiply along a branch, add across branches.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The probability of a sure event is <span class="marks">[1]</span>
   (a) $0$ (b) $0.5$ (c) $1$ (d) $\infty$
2. Two dice are thrown. The probability that the sum is $7$ is <span class="marks">[1]</span>
   (a) $\dfrac{1}{12}$ (b) $\dfrac{1}{6}$ (c) $\dfrac{5}{36}$ (d) $\dfrac{7}{36}$
3. If $A$ and $B$ are independent, then $P(A\cap B)$ equals <span class="marks">[1]</span>
   (a) $P(A)+P(B)$ (b) $P(A)\,P(B)$ (c) $0$ (d) $P(A)-P(B)$
4. If the odds in favour of an event are $4:3$, its probability is <span class="marks">[1]</span>
   (a) $\dfrac{4}{3}$ (b) $\dfrac{3}{7}$ (c) $\dfrac{4}{7}$ (d) $\dfrac{3}{4}$
5. For mutually exclusive events $A$ and $B$, $P(A\cup B)$ equals <span class="marks">[1]</span>
   (a) $P(A)P(B)$ (b) $P(A)+P(B)$ (c) $P(A)+P(B)-P(A)P(B)$ (d) $1$
6. A card is drawn from a well-shuffled pack. The probability that it is a face
   card is <span class="marks">[1]</span>
   (a) $\dfrac{1}{13}$ (b) $\dfrac{3}{13}$ (c) $\dfrac{1}{4}$ (d) $\dfrac{4}{13}$

::: note Answers to Group A
**1.** (c) — a sure event contains every outcome, so $m = n$.
**2.** (b) — the $6$ pairs $(1,6),\ldots,(6,1)$ out of $36$ give $6/36 = 1/6$.
**3.** (b) — that is the definition of independence.
**4.** (c) — $P = a/(a+b) = 4/7$.
**5.** (b) — the overlap term $P(A\cap B)$ is zero.
**6.** (b) — $12$ face cards out of $52$ gives $3/13$.
:::

**Group B — Short answer (5 marks each)**

1. Define the mathematical and the empirical definitions of probability, giving
   one example of each, and state why the mathematical definition fails for the
   event "it will rain in Pokhara tomorrow". <span class="marks">[5]</span>
2. Two fair dice are thrown together. Find the probability that (a) the sum is
   $9$, (b) the sum is at most $4$, (c) both numbers are even. <span class="marks">[5]</span>
3. A bag contains $4$ white, $5$ black and $3$ red balls. Two balls are drawn at
   random without replacement. Find the probability that (a) both are white,
   (b) one is white and one is black, (c) neither is red. <span class="marks">[5]</span>
4. $A$ and $B$ are independent events with $P(A) = 0.3$ and $P(B) = 0.6$. Find
   $P(A\cup B)$, the probability that exactly one of them occurs, and the
   probability that neither occurs. <span class="marks">[5]</span>
5. A card is drawn at random from a pack of $52$ cards. Find the probability that
   it is an ace or a red card. State clearly whether the two events are mutually
   exclusive. <span class="marks">[5]</span>
6. In a class of $40$ students, $25$ like mathematics, $20$ like science and $10$
   like both. Find the probability that a student chosen at random likes (a) at
   least one subject, (b) neither, (c) mathematics only. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Mathematical (classical): $P(A) = m/n$, the ratio of favourable to total
equally likely cases — e.g. $P(\text{head}) = 1/2$ for a fair coin. Empirical:
$P(A) = \lim_{n\to\infty} m/n$, the limiting relative frequency in repeated trials
— e.g. if $25$ of $1000$ bulbs are defective, $P \approx 0.025$. The mathematical
definition fails for rain because the two cases "rain" and "no rain" are **not
equally likely**, so dividing by $2$ has no justification; only past records
(an empirical estimate) can give a number.

**2.** $n(S) = 36$.
(a) Sum $9$: $(3,6),(4,5),(5,4),(6,3)$ — $4$ cases, so $P = 4/36 = 1/9$.
(b) Sum at most $4$: $(1,1),(1,2),(2,1),(1,3),(3,1),(2,2)$ — $6$ cases, so
$P = 6/36 = 1/6$.
(c) Both even: each die has $3$ even faces, so $3\times3 = 9$ cases and
$P = 9/36 = 1/4$.

**3.** Total $= 12$ balls, drawn without replacement.
(a) $P(WW) = \dfrac{4}{12}\times\dfrac{3}{11} = \dfrac{12}{132} = \dfrac{1}{11}$.
(b) One white one black, in either order:
$2\times\dfrac{4}{12}\times\dfrac{5}{11} = \dfrac{40}{132} = \dfrac{10}{33}$.
(c) Neither red means both come from the $9$ non-red balls:
$\dfrac{9}{12}\times\dfrac{8}{11} = \dfrac{72}{132} = \dfrac{6}{11}$.

**4.** $P(A\cap B) = 0.3\times0.6 = 0.18$, so
$P(A\cup B) = 0.3+0.6-0.18 = 0.72$.
Exactly one: $P(A)P(\bar{B}) + P(\bar{A})P(B) = 0.3(0.4) + 0.7(0.6) = 0.12+0.42 = 0.54$.
Neither: $P(\bar{A})P(\bar{B}) = 0.7\times0.4 = 0.28$ (which also equals
$1 - 0.72$ ✔).

**5.** A card can be both an ace and red (the ace of hearts, the ace of diamonds),
so the events are **not** mutually exclusive.
$P(\text{ace} \cup \text{red}) = \dfrac{4}{52} + \dfrac{26}{52} - \dfrac{2}{52}
= \dfrac{28}{52} = \dfrac{7}{13}$.

**6.** With $M$ and $S$ the two events, $n(M) = 25$, $n(S) = 20$, $n(M\cap S) = 10$.
(a) $n(M\cup S) = 25+20-10 = 35$, so $P = 35/40 = 7/8$.
(b) Neither $= 1 - 7/8 = 1/8$ (i.e. $5$ students).
(c) Mathematics only $= 25-10 = 15$ students, so $P = 15/40 = 3/8$.
:::

**Group C — Long answer (8 marks each)**

1. (a) State the addition law of probability for two events and illustrate it with
   a Venn diagram, writing down the special form for mutually exclusive
   events. <span class="marks">[3]</span>
   (b) A box contains $6$ red and $4$ blue balls. Three balls are drawn one after
   another without replacement. Find the probability that (i) all three are red,
   (ii) at least one is blue. <span class="marks">[5]</span>
2. (a) State the multiplication law of probability, and explain the difference
   between independent and dependent events with one example of each. <span class="marks">[3]</span>
   (b) Three students $A$, $B$, $C$ try to solve a problem independently with
   probabilities $\frac{1}{2}$, $\frac{1}{3}$ and $\frac{1}{4}$. Find the
   probability that (i) none of them solves it, (ii) the problem is solved,
   (iii) exactly one of them solves it. <span class="marks">[5]</span>

::: note Answers to Group C
**1.** (a) $P(A\cup B) = P(A)+P(B)-P(A\cap B)$. On a Venn diagram the two circles
overlap in $A\cap B$; adding the two circles counts that overlap twice, so it is
subtracted once. If the events are mutually exclusive the circles are disjoint,
$P(A\cap B) = 0$, and $P(A\cup B) = P(A)+P(B)$.

(b) There are $10$ balls, and the draws are dependent.

(i) $P(\text{all red}) = \dfrac{6}{10}\times\dfrac{5}{9}\times\dfrac{4}{8}
= \dfrac{120}{720} = \dfrac{1}{6}$

(ii) "At least one blue" is the complement of "all red":

$$ P(\text{at least one blue}) = 1 - \frac{1}{6} = \frac{5}{6} $$

**2.** (a) $P(A\cap B) = P(A)\,P(B|A)$; if the events are independent this becomes
$P(A\cap B) = P(A)P(B)$. Independent: two tosses of a coin — the first result does
not change the second. Dependent: two cards drawn from a pack without
replacement — the first draw changes the composition of the pack, so
$P(\text{second is an ace})$ depends on what the first card was.

(b) The three are independent, with
$P(\bar{A}) = \frac{1}{2}$, $P(\bar{B}) = \frac{2}{3}$, $P(\bar{C}) = \frac{3}{4}$.

(i) $P(\text{none}) = \dfrac{1}{2}\times\dfrac{2}{3}\times\dfrac{3}{4} = \dfrac{6}{24} = \dfrac{1}{4}$

(ii) $P(\text{solved}) = 1 - P(\text{none}) = 1 - \dfrac{1}{4} = \dfrac{3}{4}$

(iii) Exactly one means $A$ only, or $B$ only, or $C$ only:

$$ \frac{1}{2}\cdot\frac{2}{3}\cdot\frac{3}{4} + \frac{1}{2}\cdot\frac{1}{3}\cdot\frac{3}{4} + \frac{1}{2}\cdot\frac{2}{3}\cdot\frac{1}{4} = \frac{6}{24} + \frac{3}{24} + \frac{2}{24} = \frac{11}{24} $$
:::
