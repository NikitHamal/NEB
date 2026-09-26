---
subject: Mathematics
grade: 12
unit: 1
title: Permutation and Combination
hours: 10
area: Algebra
---

Counting sounds like the easiest thing in mathematics until the list gets too
long to write out. How many different number plates can Bagmati Province issue?
In how many orders can eleven players bat? How many five-member committees can a
class of thirty form? This unit gives you machinery that answers such questions
without listing anything. Two ideas do all the work: a **permutation** counts
arrangements, where order matters, and a **combination** counts selections, where
order does not.

::: key What the exam asks
Every question reduces to one decision: *does order matter?* If it does, you are
counting permutations ($^{n}P_{r}$); if it does not, combinations ($^{n}C_{r}$).
Then ask whether the objects are all different, whether repetition is allowed,
and whether the arrangement is in a line or a circle. Group B items are usually
word-arrangements or committee selections with a restriction; Group C usually
asks you to derive $^{n}P_{r}$ or $^{n}C_{r}$ and then apply it.
:::

## 1.1 Basic principle of counting

Almost everything in this unit grows from two short rules.

::: definition The two counting principles
**Multiplication principle (the "AND" rule).** If one job can be done in $m$ ways
and, *after* it has been done, a second job can be done in $n$ ways, then the two
jobs can be done one after the other in $m \times n$ ways. This extends to any
number of jobs done in succession.

**Addition principle (the "OR" rule).** If one job can be done in $m$ ways and a
*different, mutually exclusive* job in $n$ ways, then exactly one of the two jobs
can be done in $m + n$ ways.
:::

The word that tells you which rule to use is the connective. "Choose a shirt
**and** a pair of trousers" multiplies. "Travel by bus **or** by plane" adds.

```figure caption="The multiplication principle drawn as a tree. Three ways to reach Pokhara, then two ways on to Jomsom, give $3 \times 2 = 6$ complete journeys — one for each path from root to leaf."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,2.9))
root = (0.0, 0.0)
mids = [(1.5, 1.7), (1.5, 0.0), (1.5, -1.7)]
mlab = ['bus', 'car', 'plane']
leaf = ['flight', 'jeep']
for hx, ht in [(0.0, 'Kathmandu'), (1.5, 'Pokhara'), (3.2, 'Jomsom')]:
    ax.text(hx, 2.45, ht, ha='center', fontsize=9.2, color=INK)
ax.plot([root[0]], [root[1]], 'o', color=INK, ms=6)
n = 0
for (mx, my), ml in zip(mids, mlab):
    ax.annotate('', xy=(mx, my), xytext=root,
                arrowprops=dict(arrowstyle='-', color=ACCENT, lw=1.1))
    ax.text((root[0]+mx)/2 - 0.08, (root[1]+my)/2 + 0.14, ml, ha='center',
            fontsize=8.4, color=ACCENT)
    ax.plot([mx], [my], 'o', color=INK, ms=5)
    for s, ll in zip((0.55, -0.55), leaf):
        lx, ly = 3.2, my + s
        ax.annotate('', xy=(lx, ly), xytext=(mx, my),
                    arrowprops=dict(arrowstyle='-', color='#2e8b57', lw=1.1))
        ax.plot([lx], [ly], 'o', color=INK, ms=4)
        n += 1
        ax.text(lx + 0.14, ly, f'{ll}  ({n})', ha='left', va='center',
                fontsize=8.4, color=INK)
ax.text(1.6, -3.05, '3 branches  $\\times$  2 branches each  =  6 routes',
        ha='center', fontsize=9.4, color=INK)
ax.set_xlim(-1.1, 4.9); ax.set_ylim(-3.5, 2.8)
ax.axis('off')
```

### Factorial notation

For a positive integer $n$, the product of all positive integers up to $n$ is
written $n!$ and read "$n$ factorial":

$$ n! = n(n-1)(n-2)\cdots 3 \cdot 2 \cdot 1, \qquad n! = n\,(n-1)! $$

So $5! = 120$ and $6! = 720$. Putting $n = 1$ in $n! = n(n-1)!$ gives
$1! = 1 \cdot 0!$, which forces

$$ 0! = 1 $$

This is a *definition made necessary by the formula*, not an accident; without it
$^{n}P_{n} = n!/0!$ would be meaningless.

::: example Worked example 1.1
**Problem.** A traveller can go from Kathmandu to Pokhara by $3$ bus services or
$2$ flights, and from Pokhara to Jomsom by $4$ jeeps. In how many ways can the
whole journey Kathmandu → Pokhara → Jomsom be made?

**Solution.** The first leg is "bus **or** flight", so the addition principle
gives $3 + 2 = 5$ ways. The first leg **and** then the second leg gives, by the
multiplication principle,

$$ 5 \times 4 = 20 \text{ ways} $$
:::

::: example Worked example 1.2
**Problem.** How many three-digit numbers can be formed from the digits
$1, 2, 3, 4, 5, 6$ if (a) repetition is allowed, (b) repetition is not allowed,
(c) repetition is not allowed and the number must be even?

**Solution.** Draw three boxes — hundreds, tens, units — and fill them.

(a) Each box can take any of the $6$ digits: $\;6 \times 6 \times 6 = 216$.

(b) Once a digit is used it is gone: $\;6 \times 5 \times 4 = 120$.

(c) Fill the **restricted box first**. The units digit must be $2$, $4$ or $6$,
so it has $3$ choices; the hundreds box then has $5$ digits left and the tens box
$4$:

$$ 3 \times 5 \times 4 = 60 $$

Note that we multiplied in the order hundreds $\times$ tens $\times$ units at the
end — the *order of filling* does not change the product, but filling the
restricted box first keeps the counts honest.
:::

::: caution Deal with the restriction first
If a question says "must end in $0$", "must begin with a vowel", or "a particular
person must sit at the head", fill that position **before** any free position. If
you fill the free positions first you will not know how many choices are left for
the restricted one.
:::

## 1.2 Permutation of objects all different

::: definition Permutation
A **permutation** of $r$ objects taken from $n$ distinct objects is an
*arrangement* of $r$ of them in a definite order. The number of such arrangements
is written $^{n}P_{r}$ (also $P(n,r)$), where $0 \le r \le n$.
:::

::: derivation $^{n}P_{r}$ from first principles
Think of $r$ empty boxes standing in a row, to be filled from $n$ distinct
objects with no object used twice.

- The **first** box can be filled in $n$ ways (any object).
- For each of those, the **second** box can be filled in $n-1$ ways, since one
  object has been used.
- The **third** box: $n-2$ ways. And so on.
- The $r^{\text{th}}$ box is the $r^{\text{th}}$ in the list
  $n, n-1, n-2, \ldots$, so it can be filled in $n-(r-1) = n-r+1$ ways.

By the multiplication principle, multiply the counts:

$$ ^{n}P_{r} = n(n-1)(n-2)\cdots(n-r+1) $$

There are exactly $r$ factors. Multiply and divide by $(n-r)!$ to close the
product into factorials:

$$ ^{n}P_{r} = \frac{n(n-1)\cdots(n-r+1)\times(n-r)(n-r-1)\cdots 1}{(n-r)!}
= \frac{n!}{(n-r)!} $$

Putting $r = n$ gives $^{n}P_{n} = n!/0! = n!$: **$n$ distinct objects can be
arranged among themselves in $n!$ ways.**
:::

```figure caption="Filling $r=4$ ordered boxes from $n$ distinct objects. Each box has one fewer choice than the box before it, and the product of the four counts is $^{n}P_{4}$."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(5.0,2.4))
labs = ['$n$', '$n-1$', '$n-2$', '$n-3$']
pos  = ['1st', '2nd', '3rd', '4th']
for i, (l, p) in enumerate(zip(labs, pos)):
    x = i * 1.25
    ax.add_patch(Rectangle((x, 0), 1.0, 0.72, facecolor='none',
                           edgecolor=INK, lw=1.2))
    ax.text(x + 0.5, 0.36, l, ha='center', va='center', fontsize=11.5, color=ACCENT)
    ax.text(x + 0.5, 0.92, p + ' place', ha='center', fontsize=8.6, color=MUTED)
    if i < 3:
        ax.text(x + 1.125, 0.36, '$\\times$', ha='center', va='center',
                fontsize=11, color=INK)
ax.annotate('', xy=(0.0, -0.30), xytext=(4.75, -0.30),
            arrowprops=dict(arrowstyle='<|-|>', color=MUTED, lw=0.9, mutation_scale=9))
ax.text(2.375, -0.64, 'one choice used up at every step', ha='center',
        fontsize=8.8, color=MUTED)
ax.text(2.375, -1.18, '$^{n}P_{4} = n(n-1)(n-2)(n-3) = \\frac{n!}{(n-4)!}$',
        ha='center', fontsize=12, color=INK)
ax.set_xlim(-0.25, 5.0); ax.set_ylim(-1.55, 1.35)
ax.axis('off')
```

::: key Permutation formulas worth memorising
$$ ^{n}P_{r} = \frac{n!}{(n-r)!}, \qquad ^{n}P_{n} = n!, \qquad ^{n}P_{0} = 1,
\qquad ^{n}P_{1} = n $$
Two useful consequences: $^{n}P_{r} = n \cdot {}^{n-1}P_{r-1}$ and
$^{n}P_{r} = {}^{n-1}P_{r} + r\cdot{}^{n-1}P_{r-1}$.
:::

::: example Worked example 1.3
**Problem.** (a) Find $n$ if $^{n}P_{4} = 20 \cdot {}^{n}P_{2}$.
(b) Find $r$ if $^{10}P_{r} = 720$.

**Solution.** (a) Write both sides as products, not factorials — the cancelling
is then obvious:

$$ n(n-1)(n-2)(n-3) = 20\,n(n-1) $$

Since $n \ge 4$, the factor $n(n-1)$ is non-zero and may be cancelled:

$$ (n-2)(n-3) = 20 \;\Longrightarrow\; n^{2} - 5n + 6 = 20
\;\Longrightarrow\; n^{2} - 5n - 14 = 0 $$

$$ (n-7)(n+2) = 0 \;\Longrightarrow\; n = 7 \text{ or } n = -2 $$

A number of objects cannot be negative, so $n = 7$.
**Check:** $^{7}P_{4} = 840$ and $20 \times {}^{7}P_{2} = 20 \times 42 = 840$. ✓

(b) $^{10}P_{r} = 10 \times 9 \times 8 \cdots$ Taking three factors gives
$10 \times 9 \times 8 = 720$, so $r = 3$.
:::

::: example Worked example 1.4
**Problem.** In how many ways can the letters of the word **TRIANGLE** be
arranged if (a) there is no restriction, (b) all the vowels come together,
(c) no two vowels are together?

**Solution.** TRIANGLE has $8$ different letters: consonants T, R, N, G, L
($5$ of them) and vowels I, A, E ($3$).

(a) Eight distinct letters: $\;8! = 40\,320$.

(b) Tie the three vowels into one block. There are now $5 + 1 = 6$ units to
arrange, in $6!$ ways, and the vowels inside the block can be ordered in $3!$
ways:

$$ 6! \times 3! = 720 \times 6 = 4320 $$

(c) Use the **gap method**. Arrange the $5$ consonants first: $5! = 120$ ways.
This creates $6$ gaps (before, between and after them):

$$ \_\,\text{T}\,\_\,\text{R}\,\_\,\text{N}\,\_\,\text{G}\,\_\,\text{L}\,\_ $$

Put the three vowels into three *different* gaps, which is an arrangement of $3$
vowels in $6$ places: $^{6}P_{3} = 6 \times 5 \times 4 = 120$ ways. Hence

$$ 5! \times {}^{6}P_{3} = 120 \times 120 = 14\,400 $$
:::

::: caution "Not all together" is not "no two together"
In TRIANGLE, arrangements with *no two* vowels adjacent number $14\,400$, while
arrangements in which the vowels are *not all three* together number
$40\,320 - 4320 = 36\,000$. Read the wording carefully: "together" glued as a
block, "no two together" needs the gap method.
:::

## 1.3 Permutation of objects not all different

If some objects are identical, swapping them produces no new arrangement, so the
count $n!$ over-counts.

::: derivation Arrangements of $n$ objects with repeats
Suppose $n$ objects contain $p$ alike of one kind, $q$ alike of a second kind,
$s$ alike of a third kind, and the rest all different. Let the required number of
distinct arrangements be $x$.

Take any one of these $x$ arrangements. If the $p$ identical objects were
*labelled* to make them distinguishable, they could be permuted among their own
$p$ places in $p!$ ways, and every one of those would then look different.
Similarly the $q$ alike give $q!$ and the $s$ alike give $s!$. So each of the $x$
arrangements would spread into $p!\,q!\,s!$ distinguishable ones.

But if every object were distinct the total would be exactly $n!$. Therefore

$$ x \times p!\,q!\,s! = n! \qquad\Longrightarrow\qquad x = \frac{n!}{p!\,q!\,s!} $$
:::

```figure caption="Why we divide. The $5! = 120$ orderings of L,E,V,E,L fall into $30$ clusters of $2!\times 2! = 4$ orderings that look identical once the labels are removed, so only $120/4 = 30$ arrangements are genuinely different."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(5.0,2.7))
rng = np.random.default_rng(3)
for c in range(30):
    cx, cy = (c % 10) * 1.0, -(c // 10) * 1.0
    ax.add_patch(Rectangle((cx - 0.40, cy - 0.40), 0.80, 0.80,
                           facecolor=ACCENT, alpha=0.10,
                           edgecolor=ACCENT, lw=0.7))
    for dx, dy in [(-0.17, 0.17), (0.17, 0.17), (-0.17, -0.17), (0.17, -0.17)]:
        ax.plot([cx + dx], [cy + dy], 'o', color=INK, ms=2.6)
ax.text(4.5, 1.05, '$5! = 120$ labelled orderings of  L$_1$ E$_1$ V E$_2$ L$_2$',
        ha='center', fontsize=9.6, color=INK)
ax.text(4.5, -3.05, '30 clusters $\\times$ 4 look-alikes in each cluster',
        ha='center', fontsize=9.4, color=MUTED)
ax.text(4.5, -3.95, '$\\frac{5!}{2!\\,2!} = 30$ distinct arrangements',
        ha='center', fontsize=11.5, color=INK)
ax.set_xlim(-1.0, 10.0); ax.set_ylim(-4.7, 1.5)
ax.set_aspect('equal'); ax.axis('off')
```

::: example Worked example 1.5
**Problem.** How many distinct arrangements can be made of the letters of the
word **KATHMANDU**? In how many of them are the three vowels together?

**Solution.** KATHMANDU has $9$ letters: K, A, T, H, M, A, N, D, U. Only A is
repeated, twice; every other letter appears once. So $n = 9$, $p = 2$:

$$ \frac{9!}{2!} = \frac{362\,880}{2} = 181\,440 $$

For the vowels A, A, U together, tie them into one block. The consonants K, T, H,
M, N, D ($6$ of them) plus the block make $7$ units, all different, giving $7!$
arrangements; inside the block the three letters A, A, U can be ordered in
$3!/2!$ ways because two of them are alike:

$$ 7! \times \frac{3!}{2!} = 5040 \times 3 = 15\,120 $$
:::

::: example Worked example 1.6
**Problem.** How many different arrangements are there of the letters of
**MISSISSIPPI**? In how many of them do no two I's come together?

**Solution.** Eleven letters: M ($1$), I ($4$), S ($4$), P ($2$).

$$ \frac{11!}{4!\,4!\,2!} = \frac{39\,916\,800}{24 \times 24 \times 2} = 34\,650 $$

For no two I's together, first arrange the other seven letters M, S, S, S, S, P,
P:

$$ \frac{7!}{4!\,2!} = \frac{5040}{48} = 105 \text{ ways} $$

These seven letters create $8$ gaps, and the four identical I's must occupy four
*different* gaps — a selection, not an arrangement, since the I's are alike:
$^{8}C_{4} = 70$. Hence

$$ 105 \times 70 = 7350 $$
:::

## 1.4 Circular permutation; permutation with repeated use of objects

### Arrangements round a circle

Around a round table there is no "first seat". Rotating everybody one place to
the left gives the same cyclic order, so each circular arrangement corresponds to
several linear ones.

::: derivation Circular permutations
Fix one person, say A, in any seat. This removes the rotational freedom, because
every arrangement of the circle can be rotated until A sits in that chosen seat,
and it can be done in exactly one way. The remaining $n-1$ people now fill $n-1$
distinct seats *relative to A*, which can be done in $(n-1)!$ ways. Hence

$$ \text{circular permutations of } n \text{ distinct objects} = (n-1)! $$

Equivalently: the $n!$ linear arrangements fall into groups of $n$ that are
rotations of one another, so the count is $n!/n = (n-1)!$.

If the circle may also be **turned over** — a garland of flowers, a necklace of
beads, a bracelet — then a clockwise arrangement and its mirror image are the
same object, and the count halves:

$$ \frac{(n-1)!}{2} \qquad (n \ge 3) $$
:::

```figure caption="Left: the four rotations of A, B, C, D are one circular arrangement, so $4!$ must be divided by $4$, leaving $3! = 6$. Right: for a garland the mirror image is the same object, so divide by $2$ again."
import numpy as np, matplotlib.pyplot as plt
fig, axs = plt.subplots(1, 2, figsize=(5.1,3.2))

def ring(ax, labels, R=0.62, start=90, cx=0.0, cy=0.0, col=INK):
    th = np.deg2rad(start) + np.arange(len(labels)) * 2*np.pi/len(labels)
    ax.plot(cx + R*np.cos(np.linspace(0, 2*np.pi, 200)),
            cy + R*np.sin(np.linspace(0, 2*np.pi, 200)),
            color=GRID, lw=1.0)
    for t, L in zip(th, labels):
        ax.plot([cx + R*np.cos(t)], [cy + R*np.sin(t)], 'o', color=col, ms=4.5)
        ax.text(cx + 1.48*R*np.cos(t), cy + 1.48*R*np.sin(t), L,
                ha='center', va='center', fontsize=9.2, color=col)

XL, YL = (-1.55, 4.95), (-5.6, 2.1)
S = 3.4
ax = axs[0]
L = ['A','B','C','D']
for k, (cx, cy) in enumerate([(0,0), (S,0), (0,-S), (S,-S)]):
    ring(ax, L[k:] + L[:k], cx=cx, cy=cy)
ax.annotate('', xy=(2.35,0), xytext=(1.05,0),
            arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.1))
ax.annotate('', xy=(S,-2.15), xytext=(S,-1.30),
            arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.1))
ax.annotate('', xy=(1.05,-S), xytext=(2.35,-S),
            arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.1))
ax.annotate('', xy=(0,-1.30), xytext=(0,-2.15),
            arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.1))
ax.text(1.7, 1.75, 'rotate = same arrangement', ha='center',
        fontsize=8.6, color=ACCENT)
ax.text(1.7, -5.05, '$4!/4 = 3! = 6$', ha='center', fontsize=10.5, color=INK)
ax.set_xlim(*XL); ax.set_ylim(*YL)
ax.set_aspect('equal'); ax.axis('off')

ax = axs[1]
ring(ax, ['A','B','C','D'], cx=0.0, cy=0.0)
ring(ax, ['A','D','C','B'], cx=S, cy=0.0)
ax.plot([S/2, S/2], [-1.35, 1.35], ls=(0,(4,3)), color=MUTED, lw=1.0)
ax.annotate('', xy=(S-1.05,-0.05), xytext=(1.05,-0.05),
            arrowprops=dict(arrowstyle='<|-|>', color='#d9534f', lw=1.1))
ax.text(1.7, 1.75, 'flip over = same garland', ha='center',
        fontsize=8.6, color='#d9534f')
ax.text(1.7, -1.95, '$(4-1)!/2 = 3$', ha='center', fontsize=10.5, color=INK)
ax.set_xlim(*XL); ax.set_ylim(*YL)
ax.set_aspect('equal'); ax.axis('off')
```

::: example Worked example 1.7
**Problem.** Eight friends sit at a round table. In how many ways can they sit if
(a) there is no restriction, (b) two particular friends sit together, (c) those
two never sit together? (d) In how many ways can $8$ different flowers be strung
into a garland?

**Solution.** (a) $\;(8-1)! = 7! = 5040$.

(b) Tie the two friends into one block. There are now $7$ units round the circle,
giving $(7-1)! = 6! = 720$ ways; the two inside the block can swap in $2!$ ways:

$$ 6! \times 2! = 720 \times 2 = 1440 $$

(c) "Never together" is everything else:
$\;5040 - 1440 = 3600$.

(d) A garland can be turned over, so

$$ \frac{(8-1)!}{2} = \frac{5040}{2} = 2520 $$
:::

### Permutations with repeated use of objects

Now allow each object to be used as often as we like.

::: derivation $n^{r}$ arrangements with unlimited repetition
There are $r$ places to fill and $n$ objects available. Because an object may be
used again, the number of choices does **not** shrink: each of the $r$ places can
be filled in $n$ ways independently. By the multiplication principle the number
of arrangements is

$$ \underline{n \times n \times \cdots \times n} \;=\; n^{r},
\qquad r \text{ factors} $$

Note the contrast with $^{n}P_{r}$: there the factors *decrease*, here they stay
at $n$ because nothing is used up.
:::

::: memory Which formula, when?
| Situation | Count |
|---|---|
| $r$ from $n$, order matters, no repetition | $^{n}P_{r} = \dfrac{n!}{(n-r)!}$ |
| $r$ from $n$, order matters, repetition allowed | $n^{r}$ |
| $r$ from $n$, order does not matter | $^{n}C_{r} = \dfrac{n!}{r!(n-r)!}$ |
| all $n$ in a row, $p$ and $q$ alike | $\dfrac{n!}{p!\,q!}$ |
| all $n$ round a circle | $(n-1)!$ |
| all $n$ in a garland or necklace | $\dfrac{(n-1)!}{2}$ |
:::

::: example Worked example 1.8
**Problem.** (a) How many four-digit numbers can be formed using the digits
$1$ to $9$ if a digit may be repeated? (b) In how many ways can $5$ letters be
posted into $3$ letter-boxes?

**Solution.** (a) Four places, $9$ choices for each, repetition allowed:

$$ 9^{4} = 6561 $$

(b) Ask the question from the side that makes the choices independent: *each
letter* must pick a box. Letter 1 has $3$ choices, letter 2 has $3$, and so on
for $5$ letters:

$$ 3^{5} = 243 $$

Not $5^{3}$ — a box may hold many letters, but a letter goes into exactly one
box, so the letters do the choosing.
:::

## 1.5 Combination of things all different

::: definition Combination
A **combination** of $r$ objects out of $n$ distinct objects is a *selection* of
$r$ of them in which order is irrelevant. The number of such selections is
written $^{n}C_{r}$, or $\binom{n}{r}$, with $0 \le r \le n$.
:::

::: derivation $^{n}C_{r}$ from first principles
Count the permutations $^{n}P_{r}$ in two stages instead of one.

**Stage 1.** Choose which $r$ objects to use. By definition this can be done in
$^{n}C_{r}$ ways.

**Stage 2.** Arrange the chosen $r$ objects among themselves. They are all
different, so this can be done in $r!$ ways.

Every arrangement of $r$ objects out of $n$ arises from exactly one selection
followed by exactly one ordering, so by the multiplication principle

$$ ^{n}C_{r} \times r! = {}^{n}P_{r} $$

Therefore

$$ ^{n}C_{r} = \frac{^{n}P_{r}}{r!} = \frac{n!}{r!\,(n-r)!}
= \frac{n(n-1)\cdots(n-r+1)}{r!} $$

The last form — $r$ factors on top, $r!$ underneath — is the one to compute with.
:::

```figure caption="$^{4}C_{2} \times 2! = {}^{4}P_{2}$: each of the $6$ selections from A, B, C, D opens into $2! = 2$ ordered arrangements, giving $12$ permutations in all."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(4.7,3.2))
pairs = [('A','B'), ('A','C'), ('A','D'), ('B','C'), ('B','D'), ('C','D')]
for i, (p, q) in enumerate(pairs):
    y = -i * 1.0
    ax.add_patch(Rectangle((0, y - 0.32), 1.15, 0.64, facecolor=ACCENT,
                           alpha=0.12, edgecolor=ACCENT, lw=0.8))
    ax.text(0.575, y, '{' + p + ', ' + q + '}', ha='center', va='center',
            fontsize=9.6, color=INK)
    for k, s in enumerate((p + q, q + p)):
        ax.annotate('', xy=(2.15, y + 0.30 - 0.60*k), xytext=(1.20, y),
                    arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=0.8))
        ax.text(2.28, y + 0.30 - 0.60*k, s, ha='left', va='center',
                fontsize=9.4, color='#2e8b57')
ax.text(0.575, 1.05, '$^{4}C_{2} = 6$ selections', ha='center',
        fontsize=9.8, color=ACCENT)
ax.text(2.55, 1.05, '$^{4}P_{2} = 12$ arrangements', ha='center',
        fontsize=9.8, color='#2e8b57')
ax.text(1.6, -6.05, 'selection $\\times$ ordering = arrangement:   '
        '$6 \\times 2! = 12$', ha='center', fontsize=9.8, color=INK)
ax.set_xlim(-0.35, 3.6); ax.set_ylim(-6.6, 1.5)
ax.axis('off')
```

::: example Worked example 1.9
**Problem.** A committee of $5$ is to be chosen from $7$ men and $4$ women. In
how many ways can this be done if the committee must contain (a) exactly
$2$ women, (b) at least $2$ women, (c) at most $1$ woman?

**Solution.** Order of selection is irrelevant, so use combinations.

(a) Choose $2$ of the $4$ women **and** $3$ of the $7$ men:

$$ ^{4}C_{2} \times {}^{7}C_{3} = 6 \times 35 = 210 $$

(b) "At least $2$" means $2$, $3$ or $4$ women — mutually exclusive cases, so
add:

$$ ^{4}C_{2}{}^{7}C_{3} + {}^{4}C_{3}{}^{7}C_{2} + {}^{4}C_{4}{}^{7}C_{1}
= 210 + 4(21) + 1(7) = 210 + 84 + 7 = 301 $$

(c) The total number of committees is $^{11}C_{5} = 462$, and "at most $1$ woman"
is the complement of "at least $2$":

$$ 462 - 301 = 161 $$

**Check directly:** $^{4}C_{0}{}^{7}C_{5} + {}^{4}C_{1}{}^{7}C_{4}
= 21 + 4(35) = 21 + 140 = 161$. ✓
:::

::: example Worked example 1.10
**Problem.** There are $12$ points in a plane, of which $5$ are collinear and no
other three are collinear. How many (a) straight lines and (b) triangles can be
drawn using these points? (c) How many diagonals has a regular $12$-gon?

**Solution.** (a) Any $2$ points give a line: $^{12}C_{2} = 66$. But the $5$
collinear points would give $^{5}C_{2} = 10$ lines, whereas in fact they all lie
on **one** line. Subtract the wrong ten and add back the one:

$$ 66 - 10 + 1 = 57 $$

(b) Any $3$ points give a triangle unless they are collinear:

$$ ^{12}C_{3} - {}^{5}C_{3} = 220 - 10 = 210 $$

(c) Joining $12$ vertices in pairs gives $^{12}C_{2} = 66$ segments, of which
$12$ are sides:

$$ 66 - 12 = 54 \text{ diagonals} $$
:::

## 1.6 Properties of combination

::: derivation The five standard properties
**(i) $^{n}C_{0} = {}^{n}C_{n} = 1$.**
$\;^{n}C_{0} = \dfrac{n!}{0!\,n!} = 1$ and $^{n}C_{n} = \dfrac{n!}{n!\,0!} = 1$.
There is exactly one way to choose nothing, and one way to choose everything.

**(ii) $^{n}C_{r} = {}^{n}C_{n-r}$.** Replace $r$ by $n-r$ in the formula:

$$ ^{n}C_{n-r} = \frac{n!}{(n-r)!\,\left[n-(n-r)\right]!}
= \frac{n!}{(n-r)!\,r!} = {}^{n}C_{r} $$

*Why it is obvious:* choosing $r$ objects to take is the same act as choosing the
$n-r$ objects to leave behind.

**(iii) If $^{n}C_{r} = {}^{n}C_{s}$ then $r = s$ or $r + s = n$.** By (ii),
$^{n}C_{s} = {}^{n}C_{n-s}$, and $^{n}C_{x}$ takes each value at most twice, so
either $r = s$ or $r = n - s$.

**(iv) Pascal's rule: $^{n}C_{r} + {}^{n}C_{r-1} = {}^{n+1}C_{r}$.**

$$ ^{n}C_{r} + {}^{n}C_{r-1} = \frac{n!}{r!\,(n-r)!} + \frac{n!}{(r-1)!\,(n-r+1)!} $$

Take out $n!$ and make the denominators match, using $r! = r(r-1)!$ and
$(n-r+1)! = (n-r+1)(n-r)!$:

$$ = \frac{n!}{(r-1)!\,(n-r)!}\left[\frac{1}{r} + \frac{1}{n-r+1}\right]
= \frac{n!}{(r-1)!\,(n-r)!}\cdot\frac{(n-r+1)+r}{r\,(n-r+1)} $$

$$ = \frac{n!\,(n+1)}{r!\,(n-r+1)!} = \frac{(n+1)!}{r!\,(n+1-r)!} = {}^{n+1}C_{r} $$

*Why it is obvious:* to choose $r$ from $n+1$ objects, either leave out a marked
object (then choose all $r$ from the other $n$: $^{n}C_{r}$ ways) or include it
(then choose $r-1$ from the other $n$: $^{n}C_{r-1}$ ways).

**(v) $r \cdot {}^{n}C_{r} = n \cdot {}^{n-1}C_{r-1}$.**

$$ r \cdot \frac{n!}{r!\,(n-r)!} = \frac{n!}{(r-1)!\,(n-r)!}
= n \cdot \frac{(n-1)!}{(r-1)!\,(n-r)!} = n \cdot {}^{n-1}C_{r-1} $$

*Why it is obvious:* both sides count "choose a committee of $r$ from $n$ people
and appoint one of them chairperson".
:::

A sixth property follows from Pascal's rule and is proved in Unit 2:
$\;^{n}C_{0} + {}^{n}C_{1} + \cdots + {}^{n}C_{n} = 2^{n}$, the total number of
subsets of a set of $n$ elements.

```figure caption="The values of $^{10}C_{r}$. The bars are symmetric about $r=5$ because $^{n}C_{r} = {}^{n}C_{n-r}$, and the largest value sits at the middle, $^{10}C_{5} = 252$."
import numpy as np, matplotlib.pyplot as plt
from math import comb
fig, ax = plt.subplots(figsize=(4.9,2.8))
r = np.arange(11)
v = np.array([comb(10, int(k)) for k in r])
cols = [ACCENT] * 11
cols[5] = '#d9534f'; cols[2] = cols[8] = '#2e8b57'
ax.bar(r, v, color=cols, alpha=0.88, width=0.68)
for k, val in zip(r, v):
    ax.text(k, val + 9, str(val), ha='center', fontsize=7.6, color=INK)
ax.text(-0.45, 352, '$^{10}C_{2} = {}^{10}C_{8} = 45$   (green pair):',
        ha='left', fontsize=9.0, color='#2e8b57')
ax.text(-0.45, 318, 'the bars are symmetric about $r=5$',
        ha='left', fontsize=8.8, color=MUTED)
ax.annotate('greatest at the middle', xy=(5.45, 258), xytext=(8.1, 292),
            ha='center', fontsize=8.8, color='#d9534f',
            arrowprops=dict(arrowstyle='-|>', color='#d9534f', lw=0.9))
ax.set_xlabel('$r$'); ax.set_ylabel('$^{10}C_{r}$')
ax.set_xticks(r); ax.set_ylim(0, 390); ax.set_yticks([0,50,100,150,200,250])
ax.spines[['top','right']].set_visible(False)
ax.grid(True, axis='y', alpha=.45)
```

::: example Worked example 1.11
**Problem.** If $^{n}C_{r-1} = 36$, $^{n}C_{r} = 84$ and $^{n}C_{r+1} = 126$,
find $n$ and $r$.

**Solution.** Take ratios, because consecutive combinations have a very simple
ratio:

$$ \frac{^{n}C_{r}}{^{n}C_{r-1}} = \frac{n!/[r!(n-r)!]}{n!/[(r-1)!(n-r+1)!]}
= \frac{n-r+1}{r} $$

So the first pair gives

$$ \frac{n-r+1}{r} = \frac{84}{36} = \frac{7}{3}
\;\Longrightarrow\; 3n - 3r + 3 = 7r \;\Longrightarrow\; 3n - 10r + 3 = 0 \quad (1) $$

The second pair, with $r$ replaced by $r+1$, gives

$$ \frac{n-r}{r+1} = \frac{126}{84} = \frac{3}{2}
\;\Longrightarrow\; 2n - 2r = 3r + 3 \;\Longrightarrow\; 2n - 5r - 3 = 0 \quad (2) $$

Multiply (2) by $2$ and subtract (1): $\;(4n - 10r - 6) - (3n - 10r + 3) = 0$,
so $n - 9 = 0$ and $n = 9$. Then from (2), $\;18 - 5r - 3 = 0$, giving $r = 3$.

**Check:** $^{9}C_{2} = 36$, $^{9}C_{3} = 84$, $^{9}C_{4} = 126$. ✓
:::

::: example Worked example 1.12
**Problem.** (a) If $^{2n}C_{3} : {}^{n}C_{2} = 44 : 3$, find $n$.
(b) If $^{n}C_{8} = {}^{n}C_{12}$, find $^{n}C_{17}$.

**Solution.** (a) Write both in the "$r$ factors over $r!$" form:

$$ \frac{^{2n}C_{3}}{^{n}C_{2}}
= \frac{\dfrac{2n(2n-1)(2n-2)}{3!}}{\dfrac{n(n-1)}{2!}}
= \frac{2n(2n-1)\cdot 2(n-1)}{6}\cdot\frac{2}{n(n-1)}
= \frac{4(2n-1)\cdot 2}{6} = \frac{4(2n-1)}{3} $$

Set this equal to $\dfrac{44}{3}$: $\;4(2n-1) = 44$, so $2n - 1 = 11$ and
$n = 6$.
**Check:** $^{12}C_{3} = 220$, $^{6}C_{2} = 15$, and $220:15 = 44:3$. ✓

(b) Since $8 \ne 12$, property (iii) forces $8 + 12 = n$, so $n = 20$. Then

$$ ^{20}C_{17} = {}^{20}C_{3} = \frac{20 \times 19 \times 18}{3 \times 2 \times 1}
= 1140 $$
:::

::: tip Never compute large factorials
$^{20}C_{3}$ is three numbers over $3!$, not $20!$ divided by two more
factorials. Always cancel first: with $^{n}C_{r}$, use the smaller of $r$ and
$n-r$, so compute $^{50}C_{48}$ as $^{50}C_{2} = 1225$.
:::

## Chapter summary

- Multiplication principle (AND): multiply the counts. Addition principle (OR):
  add them. A tree diagram makes which one applies visible.
- $n! = n(n-1)\cdots 1$ and $0! = 1$.
- Permutation (order matters):
  $^{n}P_{r} = n(n-1)\cdots(n-r+1) = \dfrac{n!}{(n-r)!}$, and $^{n}P_{n} = n!$.
- $n$ objects with $p$, $q$, $s$ alike arrange in $\dfrac{n!}{p!\,q!\,s!}$ ways.
- Round a circle: $(n-1)!$ arrangements; a garland or necklace, which can be
  flipped: $\dfrac{(n-1)!}{2}$.
- With unlimited repetition, $r$ places filled from $n$ objects: $n^{r}$.
- Combination (order irrelevant): $^{n}C_{r}\cdot r! = {}^{n}P_{r}$, so
  $^{n}C_{r} = \dfrac{n!}{r!\,(n-r)!}$.
- Properties: $^{n}C_{0} = {}^{n}C_{n} = 1$; $^{n}C_{r} = {}^{n}C_{n-r}$;
  $^{n}C_{r} = {}^{n}C_{s} \Rightarrow r = s$ or $r+s = n$;
  $^{n}C_{r} + {}^{n}C_{r-1} = {}^{n+1}C_{r}$;
  $r\,{}^{n}C_{r} = n\,{}^{n-1}C_{r-1}$; and $\sum_{r=0}^{n}{}^{n}C_{r} = 2^{n}$.
- Standard techniques: fill the restricted place first; tie objects together into
  a block for "together"; use the gap method for "no two together"; use the
  complement for "at least" and "never".

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The value of $^{8}P_{3}$ is <span class="marks">[1]</span>
   (a) $56$ (b) $168$ (c) $336$ (d) $6720$
2. The number of ways in which $6$ people can sit at a round table is <span class="marks">[1]</span>
   (a) $720$ (b) $360$ (c) $120$ (d) $60$
3. If $^{n}C_{9} = {}^{n}C_{7}$, then $n$ is <span class="marks">[1]</span>
   (a) $2$ (b) $9$ (c) $16$ (d) $63$
4. The number of distinct arrangements of the letters of the word **LEVEL** is <span class="marks">[1]</span>
   (a) $120$ (b) $60$ (c) $30$ (d) $20$
5. $^{n}C_{r} + {}^{n}C_{r-1}$ equals <span class="marks">[1]</span>
   (a) $^{n}C_{r+1}$ (b) $^{n+1}C_{r}$ (c) $^{n+1}C_{r-1}$ (d) $^{n-1}C_{r}$
6. The number of diagonals of a regular octagon is <span class="marks">[1]</span>
   (a) $16$ (b) $20$ (c) $28$ (d) $56$

::: note Answers to Group A
**1.** (c) — $^{8}P_{3} = 8 \times 7 \times 6 = 336$.

**2.** (c) — $(6-1)! = 5! = 120$.

**3.** (c) — $9 \ne 7$, so $n = 9 + 7 = 16$.

**4.** (c) — LEVEL has $5$ letters with L twice and E twice:
$5!/(2!\,2!) = 120/4 = 30$.

**5.** (b) — Pascal's rule.

**6.** (b) — $^{8}C_{2} - 8 = 28 - 8 = 20$.
:::

**Group B — Short answer (5 marks each)**

1. Derive the formula $^{n}P_{r} = \dfrac{n!}{(n-r)!}$ from the basic principle of
   counting, and hence find $n$ if $^{n}P_{3} = 12 \cdot {}^{n}P_{2}$. <span class="marks">[5]</span>
2. In how many ways can the letters of the word **EQUATION** be arranged so that
   all the vowels are together? In how many arrangements do no two vowels come
   together? <span class="marks">[5]</span>
3. In how many ways can $7$ boys and $3$ girls stand in a row so that no two
   girls stand next to each other? <span class="marks">[5]</span>
4. A cricket team of $11$ is to be chosen from $15$ players, of whom $5$ are
   bowlers. In how many ways can the team be chosen so that it contains exactly
   $4$ bowlers? <span class="marks">[5]</span>
5. Prove that $^{n}C_{r} + {}^{n}C_{r-1} = {}^{n+1}C_{r}$, and use it to evaluate
   $^{12}C_{5} + {}^{12}C_{4}$. <span class="marks">[5]</span>
6. How many numbers greater than $3000$ can be formed using the digits
   $1, 2, 3, 4, 5$ without repetition? <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Fill $r$ ordered places from $n$ distinct objects. The first place has $n$
choices, the second $n-1$, …, the $r^{\text{th}}$ has $n-r+1$. Multiplying,
$^{n}P_{r} = n(n-1)\cdots(n-r+1)$; multiplying top and bottom by $(n-r)!$ gives
$^{n}P_{r} = \dfrac{n!}{(n-r)!}$.

Now $n(n-1)(n-2) = 12\,n(n-1)$. Cancel $n(n-1) \ne 0$: $\;n - 2 = 12$, so
$n = 14$. Check: $^{14}P_{3} = 2184 = 12 \times 182 = 12\,{}^{14}P_{2}$. ✓

**2.** EQUATION has $8$ different letters, $5$ vowels (E, U, A, I, O) and $3$
consonants (Q, T, N).

*Vowels together:* tie them into one block, giving $3 + 1 = 4$ units:

$$ 4! \times 5! = 24 \times 120 = 2880 $$

*No two vowels together:* arrange the $3$ consonants in $3! = 6$ ways; they make
$4$ gaps, and $5$ vowels cannot fit into $4$ gaps without two sharing a gap.
Hence the number of such arrangements is $\mathbf{0}$ — it is impossible.

**3.** Arrange the $7$ boys: $7! = 5040$ ways. They create $8$ gaps, and the $3$
girls must go into $3$ different gaps, which can be done in
$^{8}P_{3} = 8 \times 7 \times 6 = 336$ ways. Total

$$ 5040 \times 336 = 1\,693\,440 $$

**4.** Exactly $4$ bowlers from $5$, and the remaining $7$ players from the
$10$ non-bowlers:

$$ ^{5}C_{4} \times {}^{10}C_{7} = 5 \times 120 = 600 $$

**5.** $^{n}C_{r} + {}^{n}C_{r-1} = \dfrac{n!}{r!(n-r)!} + \dfrac{n!}{(r-1)!(n-r+1)!}$.
Taking out $\dfrac{n!}{(r-1)!\,(n-r)!}$ leaves
$\left[\dfrac{1}{r} + \dfrac{1}{n-r+1}\right] = \dfrac{n+1}{r(n-r+1)}$, so the sum
is $\dfrac{(n+1)!}{r!\,(n+1-r)!} = {}^{n+1}C_{r}$.

Hence $^{12}C_{5} + {}^{12}C_{4} = {}^{13}C_{5} = \dfrac{13\cdot12\cdot11\cdot10\cdot9}{120} = 1287$.

**6.** The numbers may have $4$ or $5$ digits (any $5$-digit number made from
these digits exceeds $3000$).

*Four-digit numbers greater than $3000$:* the leading digit must be $3$, $4$ or
$5$ — that is $3$ choices — and the other three places are filled from the
remaining $4$ digits in $^{4}P_{3} = 24$ ways: $\;3 \times 24 = 72$.

*Five-digit numbers:* $5! = 120$, all of which exceed $3000$.

Total $= 72 + 120 = 192$.
:::

**Group C — Long answer (8 marks each)**

1. (a) Prove that $^{n}C_{r} = \dfrac{n!}{r!\,(n-r)!}$ by first showing that
   $^{n}P_{r} = {}^{n}C_{r} \times r!$. <span class="marks">[4]</span>
   (b) Out of $6$ teachers and $8$ students, a committee of $6$ is to be formed
   containing at least $2$ teachers. In how many ways can it be done? <span class="marks">[4]</span>
2. (a) Derive the number of circular permutations of $n$ distinct objects, and
   explain why the number for a garland is $\dfrac{(n-1)!}{2}$. <span class="marks">[4]</span>
   (b) In how many ways can $5$ men and $4$ women be seated at a round table so
   that no two women sit together? <span class="marks">[4]</span>
3. (a) How many arrangements can be made of the letters of the word
   **INDEPENDENCE**? In how many of these do all the vowels occur together? <span class="marks">[4]</span>
   (b) There are $10$ points in a plane, no three of which are collinear except
   $4$ which lie on one straight line. Find the number of straight lines and the
   number of triangles determined by these points. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** (a) An arrangement of $r$ objects chosen from $n$ can be made in two
stages: select the $r$ objects ($^{n}C_{r}$ ways, by definition), then order them
($r!$ ways, as they are all different). Every arrangement arises exactly once, so
$^{n}P_{r} = {}^{n}C_{r} \times r!$. Hence

$$ ^{n}C_{r} = \frac{^{n}P_{r}}{r!} = \frac{n!}{r!\,(n-r)!} $$

(b) "At least $2$ teachers" from $6$ teachers and $8$ students, committee of $6$.
Count by number of teachers $t = 2, 3, 4, 5, 6$:

| $t$ teachers | students $6-t$ | ways |
|---|---|---|
| $2$ | $4$ | $^{6}C_{2}{}^{8}C_{4} = 15 \times 70 = 1050$ |
| $3$ | $3$ | $^{6}C_{3}{}^{8}C_{3} = 20 \times 56 = 1120$ |
| $4$ | $2$ | $^{6}C_{4}{}^{8}C_{2} = 15 \times 28 = 420$ |
| $5$ | $1$ | $^{6}C_{5}{}^{8}C_{1} = 6 \times 8 = 48$ |
| $6$ | $0$ | $^{6}C_{6}{}^{8}C_{0} = 1$ |

Total $= 1050 + 1120 + 420 + 48 + 1 = 2639$.

**Check by complement:** $^{14}C_{6} = 3003$, and committees with $0$ or $1$
teacher number $^{8}C_{6} + {}^{6}C_{1}{}^{8}C_{5} = 28 + 6(56) = 364$;
$3003 - 364 = 2639$. ✓

**2.** (a) Fix one object in one seat; every circular arrangement can be rotated
into exactly one position with that object there, so nothing is lost or
double-counted. The other $n-1$ objects then fill $n-1$ distinguishable places in
$(n-1)!$ ways. Equivalently the $n!$ linear arrangements come in rotation-groups
of size $n$, giving $n!/n = (n-1)!$. A garland can be picked up and turned over,
so an arrangement and its mirror image are the same garland; the arrangements
therefore pair off and the count is $\dfrac{(n-1)!}{2}$.

(b) Seat the $5$ men round the table first: $(5-1)! = 4! = 24$ ways. This creates
$5$ gaps between neighbouring men, and the $4$ women must occupy $4$ different
gaps: $^{5}P_{4} = 5 \times 4 \times 3 \times 2 = 120$ ways. Total

$$ 24 \times 120 = 2880 $$

**3.** (a) INDEPENDENCE has $12$ letters: N appears $3$ times, E appears $4$
times, D twice, and I, P, C once each ($3+4+2+1+1+1 = 12$).

$$ \frac{12!}{3!\,4!\,2!} = \frac{479\,001\,600}{6 \times 24 \times 2} = 1\,663\,200 $$

The vowels are I, E, E, E, E ($5$ of them). Tie them into one block; the block
plus the $7$ consonants N, D, P, N, D, N, C make $8$ units, of which N occurs $3$
times and D twice:

$$ \frac{8!}{3!\,2!} \times \frac{5!}{4!} = \frac{40\,320}{12} \times 5
= 3360 \times 5 = 16\,800 $$

(b) *Lines.* $^{10}C_{2} = 45$ pairs, but the $4$ collinear points give
$^{4}C_{2} = 6$ pairs that all determine the same single line:

$$ 45 - 6 + 1 = 40 \text{ straight lines} $$

*Triangles.* $^{10}C_{3} = 120$ triples, minus the $^{4}C_{3} = 4$ collinear
triples which form no triangle:

$$ 120 - 4 = 116 \text{ triangles} $$
:::
