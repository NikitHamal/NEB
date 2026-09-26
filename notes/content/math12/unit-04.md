---
subject: Mathematics
grade: 12
unit: 4
title: Sequence and Series
hours: 8
area: Algebra
---

In Grade 11 you summed arithmetic, geometric and harmonic progressions. This unit
sums the three series that are not progressions at all but turn up everywhere:
$1+2+\cdots+n$, the squares $1^2+2^2+\cdots+n^2$ and the cubes
$1^3+2^3+\cdots+n^3$. With these three results and the sigma rules you can total
any series whose $n^{\text{th}}$ term is a polynomial in $n$. The unit then gives
you **mathematical induction**, the proof method that settles "is this formula
true for *every* $n$?", and closes with the two infinite series that define $e$
and the natural logarithm.

::: key What the exam asks
Three shapes cover nearly every question. **(i)** "Find the sum to $n$ terms of
$1\cdot 2 + 2\cdot 3 + \cdots$" — write the $n^{\text{th}}$ term, split it with
sigma rules, substitute the three standard sums. **(ii)** "Prove by induction
that …" — the three-step layout is worth marks on its own, so never skip the
basis step. **(iii)** "Sum the series $1 + \frac{1}{2!} + \frac{1}{3!} + \cdots$"
— recognise it as $e^x$ or $\log(1+x)$ with a particular $x$.
:::

## 4.1 Sum of first n natural numbers

### Sigma notation

The symbol $\sum$ (capital sigma) is shorthand for "add up". The statement

$$ \sum_{k=1}^{n} t_k = t_1 + t_2 + t_3 + \cdots + t_n $$

is read "the sum of $t_k$ as $k$ runs from $1$ to $n$". The letter $k$ is a
**dummy**: $\sum_{k=1}^{5} k^2$ and $\sum_{r=1}^{5} r^2$ are the same number, $55$.

Two rules follow straight from the fact that addition can be reordered, and both
are used in every question in this unit.

::: key The two sigma rules
$$ \sum_{k=1}^{n} (a_k \pm b_k) = \sum_{k=1}^{n} a_k \pm \sum_{k=1}^{n} b_k
\qquad\text{and}\qquad \sum_{k=1}^{n} c\,a_k = c\sum_{k=1}^{n} a_k $$
A constant comes out in front; a constant on its own gives
$\sum_{k=1}^{n} c = nc$. There is **no** rule for a product:
$\sum a_k b_k \ne \left(\sum a_k\right)\left(\sum b_k\right)$.
:::

### The sum itself

::: derivation $\sum_{k=1}^{n} k = \frac{n(n+1)}{2}$
Write the sum forwards, then backwards underneath it:

$$ S = 1 + 2 + 3 + \cdots + (n-1) + n $$
$$ S = n + (n-1) + (n-2) + \cdots + 2 + 1 $$

Add the two lines column by column. Every column gives the same total $n+1$, and
there are $n$ columns, so

$$ 2S = n(n+1) \quad\Longrightarrow\quad \sum_{k=1}^{n} k = \frac{n(n+1)}{2} $$

This is also the arithmetic-series formula $S_n = \frac{n}{2}(a+l)$ with $a=1$
and $l=n$; the numbers $\frac{n(n+1)}{2}$ are called **triangular numbers**
because $1, 3, 6, 10, \ldots$ dots stack into triangles.
:::

The pairing argument is exactly what the picture below shows: two copies of the
triangle of dots, one turned upside down, interlock into a full rectangle.

```figure caption="Two triangular stacks of $n=6$ rows interlock into a $6 \times 7$ rectangle, so each triangle holds $\frac{6 \times 7}{2} = 21$ dots. This is the pairing proof drawn."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,2.6))
n = 6
for i in range(1, n+1):
    for j in range(i):
        ax.plot([j], [n-i], 'o', color=ACCENT, ms=6.5)
    for j in range(i, n+1):
        ax.plot([j], [n-i], 'o', color='#d9534f', ms=6.5, alpha=0.75, mfc='none', mew=1.4)
ax.annotate('1 + 2 + $\\cdots$ + 6 = 21 dots', (-0.4, -1.25), color=ACCENT, fontsize=9.2, ha='left')
ax.annotate('the same 21, turned upside down', (-0.4, -2.15), color='#d9534f', fontsize=9.2, ha='left')
ax.annotate('', xy=(-0.55, 5.35), xytext=(-0.55, -0.35),
            arrowprops=dict(arrowstyle='<|-|>', color=MUTED, lw=0.9, mutation_scale=7))
ax.text(-0.95, 2.5, '$n = 6$', rotation=90, va='center', ha='center', fontsize=9.2, color=MUTED)
ax.annotate('', xy=(-0.15, 5.9), xytext=(6.15, 5.9),
            arrowprops=dict(arrowstyle='<|-|>', color=MUTED, lw=0.9, mutation_scale=7))
ax.text(3.0, 6.25, '$n + 1 = 7$', ha='center', fontsize=9.2, color=MUTED)
ax.set_xlim(-1.35, 7.2); ax.set_ylim(-2.7, 6.7)
ax.set_aspect('equal'); ax.axis('off')
```

::: example Worked example 4.1
**Problem.** Find (a) $51 + 52 + 53 + \cdots + 100$ and (b) the sum of the first
$n$ odd natural numbers.

**Solution.** (a) Subtract the shorter sum from the longer one:

$$ \sum_{k=51}^{100} k = \sum_{k=1}^{100} k - \sum_{k=1}^{50} k
= \frac{100(101)}{2} - \frac{50(51)}{2} = 5050 - 1275 = 3775 $$

(b) The $k^{\text{th}}$ odd number is $2k-1$, so

$$ \sum_{k=1}^{n} (2k-1) = 2\sum_{k=1}^{n} k - \sum_{k=1}^{n} 1
= 2 \cdot \frac{n(n+1)}{2} - n = n^2 + n - n = n^2 $$

The first $n$ odd numbers always add to $n^2$. Check with $n=4$:
$1+3+5+7 = 16 = 4^2$.
:::

::: example Worked example 4.2
**Problem.** How many consecutive natural numbers, starting from $1$, add up to
$465$?

**Solution.** Solve $\dfrac{n(n+1)}{2} = 465$, i.e. $n^2 + n - 930 = 0$:

$$ n = \frac{-1 \pm \sqrt{1 + 3720}}{2} = \frac{-1 \pm 61}{2} = 30 \text{ or } -31 $$

A count of terms cannot be negative, so $n = 30$. Check:
$\frac{30 \times 31}{2} = 465$.
:::

::: caution Reject the negative root, and never round
$n$ counts terms, so it must be a positive **whole** number. If the quadratic
gives no positive integer root, the correct answer is "no such $n$ exists" — not
the nearest integer.
:::

## 4.2 Sum of squares and cubes of first n natural numbers

Both results come from the same trick: find an expression whose *difference*
between consecutive values is the term you want, then add the differences so that
almost everything cancels. This is called **telescoping**.

::: derivation $\sum_{k=1}^{n} k^{2} = \frac{n(n+1)(2n+1)}{6}$
Start from the identity $(k+1)^3 - k^3 = 3k^2 + 3k + 1$. Write it out for
$k = 1, 2, \ldots, n$ and add all $n$ lines. On the left the terms cancel in pairs
— $2^3$ cancels with $-2^3$, $3^3$ with $-3^3$, and so on — leaving only the last
and the first:

$$ (n+1)^3 - 1 = 3\sum_{k=1}^{n} k^{2} + 3\sum_{k=1}^{n} k + \sum_{k=1}^{n} 1 $$

Substitute the two sums we already know:

$$ n^3 + 3n^2 + 3n = 3\sum k^{2} + \frac{3n(n+1)}{2} + n $$

$$ 3\sum k^{2} = n^3 + 3n^2 + 2n - \frac{3n(n+1)}{2}
= \frac{2n^3 + 6n^2 + 4n - 3n^2 - 3n}{2} = \frac{2n^3 + 3n^2 + n}{2} $$

$$ \sum_{k=1}^{n} k^{2} = \frac{n(2n^2 + 3n + 1)}{6} = \frac{n(n+1)(2n+1)}{6} $$
:::

::: derivation $\sum_{k=1}^{n} k^{3} = \frac{n^{2}(n+1)^{2}}{4}$
Use the next identity up, $(k+1)^4 - k^4 = 4k^3 + 6k^2 + 4k + 1$. Adding for
$k = 1$ to $n$ telescopes the left side to $(n+1)^4 - 1$:

$$ (n+1)^4 - 1 = 4\sum k^{3} + 6\sum k^{2} + 4\sum k + n $$

$$ 4\sum k^{3} = (n+1)^4 - 1 - n(n+1)(2n+1) - 2n(n+1) - n $$

Now $(n+1)^4 - 1 - n = (n+1)^4 - (n+1) = (n+1)\left[(n+1)^3 - 1\right]
= (n+1)(n^3 + 3n^2 + 3n)= n(n+1)(n^2+3n+3)$, so taking out $n(n+1)$ throughout,

$$ 4\sum k^{3} = n(n+1)\left[n^2 + 3n + 3 - (2n+1) - 2\right] = n(n+1)\left[n^2 + n\right] $$

$$ \sum_{k=1}^{n} k^{3} = \frac{n(n+1)\cdot n(n+1)}{4} = \frac{n^{2}(n+1)^{2}}{4}
= \left[\frac{n(n+1)}{2}\right]^{2} = \left(\sum_{k=1}^{n} k\right)^{2} $$
:::

That last line is worth remembering on its own: **the sum of the first $n$ cubes
is the square of the sum of the first $n$ natural numbers.** It has a pretty
picture. Draw squares of side $1, 3, 6, 10, \ldots$ (the triangular numbers) one
inside the other; the L-shaped strip added at stage $k$ has area
$T_k^2 - T_{k-1}^2 = k^3$.

```figure caption="Nested squares of sides $T_k = 1, 3, 6, 10$. The L-shaped layer added at stage $k$ has area $k^{3}$, so the whole $10 \times 10$ square gives $1^{3}+2^{3}+3^{3}+4^{3} = 10^{2} = 100$."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(4.4,3.2))
T = [0, 1, 3, 6, 10]
cols = ['#1d6fb8', '#d9534f', '#2e8b57', '#b8860b']
for k in range(4, 0, -1):
    ax.add_patch(Rectangle((0,0), T[k], T[k], facecolor=cols[k-1], alpha=0.32,
                           edgecolor=INK, lw=1.0))
labs = ['$2^{3}=8$', '$3^{3}=27$', '$4^{3}=64$']
pos = [(2.1,2.1), (4.4,4.4), (8.0,8.0)]
for k in range(3):
    ax.text(pos[k][0], pos[k][1], labs[k], ha='center', va='center',
            fontsize=9.4, color=INK)
ax.annotate('$1^{3}=1$', (0.55, 0.15), (3.3, -1.45), fontsize=9.4, color=INK,
            va='center', ha='center',
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.8))
for k in range(1,5):
    ax.annotate(f'$T_{k}={T[k]}$', (T[k], -0.45), ha='center', va='top',
                fontsize=8.4, color=MUTED)
ax.annotate('side $= 1+2+3+4 = 10$', (5.0, 10.55), ha='center', fontsize=9.2, color=INK)
ax.set_xlim(-0.6, 11.2); ax.set_ylim(-2.3, 11.5)
ax.set_aspect('equal'); ax.axis('off')
```

::: key The three standard sums
$$ \sum_{k=1}^{n} k = \frac{n(n+1)}{2}, \qquad
\sum_{k=1}^{n} k^{2} = \frac{n(n+1)(2n+1)}{6}, \qquad
\sum_{k=1}^{n} k^{3} = \frac{n^{2}(n+1)^{2}}{4} $$
Memorise the denominators $2$, $6$, $4$ — they are the commonest thing to get
wrong under pressure.
:::

### The method for any series with a polynomial term

To sum a series such as $1\cdot 2 + 2\cdot 3 + 3\cdot 4 + \cdots$:

1. Write down the $n^{\text{th}}$ term $t_k$ as a polynomial in $k$.
2. Apply $\sum$ and split it with the sigma rules.
3. Substitute the three standard sums.
4. Factorise the answer, then **test it on $n=1$ or $n=2$**.

::: example Worked example 4.3
**Problem.** Find (a) $1^2 + 2^2 + \cdots + 20^2$ and (b) $1^3 + 2^3 + \cdots + 15^3$.

**Solution.** (a) With $n = 20$,

$$ \sum_{k=1}^{20} k^{2} = \frac{20(21)(41)}{6} = \frac{17220}{6} = 2870 $$

(b) With $n = 15$,

$$ \sum_{k=1}^{15} k^{3} = \frac{15^{2}(16)^{2}}{4} = \frac{225 \times 256}{4}
= 225 \times 64 = 14400 $$

(Equivalently $\left[\frac{15\times 16}{2}\right]^2 = 120^2 = 14400$.)
:::

::: example Worked example 4.4
**Problem.** Find the sum to $n$ terms of $1\cdot 2 + 2\cdot 3 + 3\cdot 4 + \cdots$
and hence the sum of the first $20$ terms.

**Solution.** The $k^{\text{th}}$ term is $t_k = k(k+1) = k^2 + k$, so

$$ S_n = \sum_{k=1}^{n}(k^2 + k) = \frac{n(n+1)(2n+1)}{6} + \frac{n(n+1)}{2} $$

Take out $\dfrac{n(n+1)}{6}$:

$$ S_n = \frac{n(n+1)}{6}\left[(2n+1) + 3\right] = \frac{n(n+1)(2n+4)}{6}
= \frac{n(n+1)(n+2)}{3} $$

*Test:* $n=2$ gives $\frac{2(3)(4)}{3} = 8 = 1\cdot 2 + 2\cdot 3$. Correct.

For $n = 20$: $S_{20} = \dfrac{20(21)(22)}{3} = \dfrac{9240}{3} = 3080$.
:::

::: example Worked example 4.5
**Problem.** Find the sum of the squares of the first $n$ odd natural numbers,
$1^2 + 3^2 + 5^2 + \cdots + (2n-1)^2$, and evaluate it for $n = 10$.

**Solution.** The $k^{\text{th}}$ odd number is $2k-1$, so
$t_k = (2k-1)^2 = 4k^2 - 4k + 1$ and

$$ S_n = 4\sum k^2 - 4\sum k + \sum 1
= \frac{4n(n+1)(2n+1)}{6} - \frac{4n(n+1)}{2} + n $$

$$ = \frac{2n(n+1)(2n+1)}{3} - 2n(n+1) + n
= \frac{2n(n+1)(2n+1) - 6n(n+1) + 3n}{3} $$

Take out $n$: the bracket is $2(n+1)(2n+1) - 6(n+1) + 3 = 4n^2 + 6n + 2 - 6n - 6 + 3
= 4n^2 - 1$, so

$$ S_n = \frac{n(4n^2-1)}{3} = \frac{n(2n-1)(2n+1)}{3} $$

*Test:* $n=2$ gives $\frac{2(3)(5)}{3} = 10 = 1 + 9$. Correct.

For $n = 10$: $S_{10} = \dfrac{10(19)(21)}{3} = \dfrac{3990}{3} = 1330$.
:::

::: example Worked example 4.6
**Problem.** Find the sum to $n$ terms of the series
$1\cdot 3 + 2\cdot 4 + 3\cdot 5 + \cdots$, and its value for $n = 12$.

**Solution.** The factors differ by $2$, so $t_k = k(k+2) = k^2 + 2k$:

$$ S_n = \frac{n(n+1)(2n+1)}{6} + 2\cdot\frac{n(n+1)}{2}
= \frac{n(n+1)}{6}\left[(2n+1) + 6\right] = \frac{n(n+1)(2n+7)}{6} $$

*Test:* $n=2$ gives $\frac{2(3)(11)}{6} = 11 = 3 + 8$. Correct.

For $n = 12$: $S_{12} = \dfrac{12(13)(31)}{6} = 2 \times 13 \times 31 = 806$.
:::

::: example Worked example 4.7
**Problem.** Find $11^3 + 12^3 + \cdots + 20^3$.

**Solution.** Subtract two standard sums:

$$ \sum_{k=11}^{20} k^{3} = \sum_{k=1}^{20} k^{3} - \sum_{k=1}^{10} k^{3}
= \left[\frac{20 \times 21}{2}\right]^{2} - \left[\frac{10 \times 11}{2}\right]^{2} $$

$$ = 210^{2} - 55^{2} = 44100 - 3025 = 41075 $$
:::

::: tip Always subtract, never re-derive
For a sum that starts part-way along ($\sum_{k=m}^{n}$), use
$\sum_{k=1}^{n} - \sum_{k=1}^{m-1}$. Note the $m-1$: if you subtract
$\sum_{k=1}^{m}$ you have thrown away the term you were asked to keep.
:::

## 4.3 Principle of mathematical induction

A formula checked for $n = 1, 2, 3$ may still fail at $n = 40$. Induction is the
method that proves a statement for **all** natural numbers at once, using a
domino argument: knock over the first domino, and make sure each domino knocks
over the next.

::: definition Principle of mathematical induction
Let $P(n)$ be a statement about the natural number $n$. If

1. **(Basis)** $P(1)$ is true, and
2. **(Inductive step)** for every $k \in \mathbb{N}$, the truth of $P(k)$ forces
   the truth of $P(k+1)$,

then $P(n)$ is true for every natural number $n$.
:::

```figure caption="Induction as a row of dominoes. The basis step topples $P(1)$; the inductive step guarantees each domino topples the next, so every $P(n)$ falls. Removing either step leaves the row standing."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.transforms as mtransforms
fig, ax = plt.subplots(figsize=(5.0,2.4))
labels = ['$P(1)$','$P(2)$','$P(3)$','$P(k)$','$P(k{+}1)$','']
angles  = [-58, -42, -26, -10, 0, 0]
for i in range(6):
    x = 1.35*i
    tr = mtransforms.Affine2D().rotate_deg_around(x, 0, angles[i]) + ax.transData
    col = ACCENT if i < 3 else '#2e8b57' if i < 5 else MUTED
    ax.add_patch(Rectangle((x-0.22, 0), 0.44, 1.55, facecolor=col, alpha=0.30,
                           edgecolor=INK, lw=1.0, transform=tr))
    if labels[i]:
        ax.text(x + 0.30, 1.85, labels[i], ha='center', fontsize=9.0, color=INK)
ax.plot([-0.8, 7.9], [0, 0], color=INK, lw=1.1)
ax.annotate('basis step:\npush this one', (0.0, -0.40), (0.0, -1.35), ha='center',
            fontsize=8.8, color=ACCENT,
            arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.0, mutation_scale=9))
ax.annotate('inductive step: $P(k) \\Rightarrow P(k+1)$', (4.05, -0.40), (5.0, -1.35),
            ha='center', fontsize=8.8, color='#2e8b57',
            arrowprops=dict(arrowstyle='-|>', color='#2e8b57', lw=1.0, mutation_scale=9))
ax.text(7.55, 0.95, '$\\cdots$', fontsize=12, color=MUTED)
ax.set_xlim(-1.1, 8.3); ax.set_ylim(-1.9, 2.45)
ax.set_aspect('equal'); ax.axis('off')
```

::: memory The four lines every induction proof must contain
1. "Let $P(n)$ be the statement …"
2. "**Basis.** For $n=1$, LHS $=$ … $=$ RHS, so $P(1)$ is true."
3. "**Assume** $P(k)$ is true, i.e. …" (the *inductive hypothesis* — say the word)
4. "**Then** … $=$ the formula with $k+1$ in place of $k$, so $P(k+1)$ is true.
   Hence by the principle of mathematical induction $P(n)$ holds for all
   $n \in \mathbb{N}$."
:::

::: example Worked example 4.8
**Problem.** Prove by induction that
$1^{3} + 2^{3} + \cdots + n^{3} = \dfrac{n^{2}(n+1)^{2}}{4}$ for all
$n \in \mathbb{N}$.

**Solution.** Let $P(n)$ be that statement.

**Basis.** For $n = 1$: LHS $= 1^3 = 1$ and RHS $= \dfrac{1 \times 4}{4} = 1$.
So $P(1)$ is true.

**Inductive step.** Assume $P(k)$ is true:

$$ 1^{3} + 2^{3} + \cdots + k^{3} = \frac{k^{2}(k+1)^{2}}{4} $$

Add the next term $(k+1)^{3}$ to both sides:

$$ 1^{3} + \cdots + k^{3} + (k+1)^{3} = \frac{k^{2}(k+1)^{2}}{4} + (k+1)^{3} $$

$$ = \frac{(k+1)^{2}\left[k^{2} + 4(k+1)\right]}{4}
= \frac{(k+1)^{2}\left(k^{2}+4k+4\right)}{4} = \frac{(k+1)^{2}(k+2)^{2}}{4} $$

which is exactly the formula with $k+1$ in place of $n$. So $P(k)$ true forces
$P(k+1)$ true.

Hence by the principle of mathematical induction the formula holds for all
$n \in \mathbb{N}$.
:::

::: example Worked example 4.9
**Problem.** Prove by induction that $3^{2n} - 1$ is divisible by $8$ for every
$n \in \mathbb{N}$.

**Solution.** Let $P(n)$: "$3^{2n} - 1$ is divisible by $8$".

**Basis.** $n=1$: $3^{2} - 1 = 8$, which is divisible by $8$. True.

**Inductive step.** Assume $P(k)$: $3^{2k} - 1 = 8m$ for some integer $m$, so
$3^{2k} = 8m + 1$. Then

$$ 3^{2(k+1)} - 1 = 3^{2k}\cdot 3^{2} - 1 = 9(8m+1) - 1 = 72m + 8 = 8(9m + 1) $$

Since $9m+1$ is an integer, $3^{2(k+1)} - 1$ is divisible by $8$, i.e. $P(k+1)$
is true. By induction $8 \mid 3^{2n}-1$ for all $n$.
:::

::: example Worked example 4.10
**Problem.** Prove by induction that
$\dfrac{1}{1\cdot 2} + \dfrac{1}{2\cdot 3} + \cdots + \dfrac{1}{n(n+1)}
= \dfrac{n}{n+1}$.

**Solution.** Let $P(n)$ be the statement.

**Basis.** $n=1$: LHS $= \dfrac{1}{2}$, RHS $= \dfrac{1}{2}$. True.

**Inductive step.** Assume the sum to $k$ terms is $\dfrac{k}{k+1}$. Adding the
$(k+1)^{\text{th}}$ term $\dfrac{1}{(k+1)(k+2)}$:

$$ \frac{k}{k+1} + \frac{1}{(k+1)(k+2)} = \frac{k(k+2) + 1}{(k+1)(k+2)}
= \frac{k^{2}+2k+1}{(k+1)(k+2)} $$

$$ = \frac{(k+1)^{2}}{(k+1)(k+2)} = \frac{k+1}{k+2} $$

which is the formula with $n = k+1$. Hence $P(n)$ is true for all $n$ by
induction.
:::

::: caution The inductive step is not "substitute $k+1$ and check"
You must *use* the hypothesis. Start from the left side for $k+1$, split off the
last term, replace the first $k$ terms by the assumed formula, and then do
algebra. A proof that merely rewrites the right-hand side with $k+1$ everywhere
scores zero, and a proof with no basis step scores at most half.
:::

## 4.4 Exponential and logarithmic series

The two series below are named in Unit 2 as standard results; here they are
derived and used, because every "sum the series" question in this unit is one of
them in disguise.

::: derivation Euler's number: $e = 1 + \frac{1}{1!} + \frac{1}{2!} + \cdots$
By definition $e = \lim_{n\to\infty}\left(1 + \frac{1}{n}\right)^{n}$. Expand by
the binomial theorem for a positive integral index:

$$ \left(1+\frac{1}{n}\right)^{n} = 1 + n\cdot\frac{1}{n}
+ \frac{n(n-1)}{2!}\cdot\frac{1}{n^{2}}
+ \frac{n(n-1)(n-2)}{3!}\cdot\frac{1}{n^{3}} + \cdots $$

Divide each numerator by the powers of $n$ underneath it:

$$ = 1 + 1 + \frac{1}{2!}\left(1-\frac{1}{n}\right)
+ \frac{1}{3!}\left(1-\frac{1}{n}\right)\left(1-\frac{2}{n}\right) + \cdots $$

As $n \to \infty$ every $\frac{r}{n} \to 0$, so each bracket tends to $1$:

$$ e = 1 + \frac{1}{1!} + \frac{1}{2!} + \frac{1}{3!} + \cdots = 2.718281828\ldots $$

The terms shrink faster than any GP, so the series converges very fast: five
terms already give $2.7083$.
:::

::: derivation The exponential series $e^{x}$ and $a^{x}$
Replace $\frac1n$ by $\frac{x}{n}$ in the same limit, $e^{x} = \lim_{n\to\infty}
\left(1+\frac{x}{n}\right)^{n}$, and expand:

$$ \left(1+\frac{x}{n}\right)^{n} = 1 + x + \frac{x^{2}}{2!}\left(1-\frac{1}{n}\right)
+ \frac{x^{3}}{3!}\left(1-\frac{1}{n}\right)\left(1-\frac{2}{n}\right) + \cdots $$

Letting $n \to \infty$,

$$ e^{x} = 1 + \frac{x}{1!} + \frac{x^{2}}{2!} + \frac{x^{3}}{3!} + \cdots
= \sum_{r=0}^{\infty} \frac{x^{r}}{r!} \qquad \text{for every real } x $$

For any base $a > 0$ write $a = e^{\log a}$, so $a^{x} = e^{x\log a}$ and

$$ a^{x} = 1 + \frac{x\log a}{1!} + \frac{(x\log a)^{2}}{2!}
+ \frac{(x\log a)^{3}}{3!} + \cdots $$

where $\log$ means the natural logarithm, to base $e$. Putting $x = -1$ in the
exponential series gives $e^{-1} = 1 - 1 + \frac{1}{2!} - \frac{1}{3!} + \cdots$,
which is how the "alternating factorial" series are recognised.
:::

::: derivation The logarithmic series $\log(1+x)$
Expand $(1+x)^{n}$ in two different ways and compare the coefficients of $n$.

*First way* — the binomial series:

$$ (1+x)^{n} = 1 + nx + \frac{n(n-1)}{2!}x^{2} + \frac{n(n-1)(n-2)}{3!}x^{3} + \cdots $$

Multiply out each numerator and keep only the terms in the **first** power of
$n$: from $nx$ we get $x$; from $\frac{n^{2}-n}{2}x^{2}$ we get $-\frac{x^{2}}{2}$;
from $\frac{n^{3}-3n^{2}+2n}{6}x^{3}$ we get $+\frac{x^{3}}{3}$, and so on. So the
coefficient of $n$ is

$$ x - \frac{x^{2}}{2} + \frac{x^{3}}{3} - \frac{x^{4}}{4} + \cdots $$

*Second way* — write $(1+x)^{n} = e^{\,n\log(1+x)}$ and use the exponential
series:

$$ (1+x)^{n} = 1 + n\log(1+x) + \frac{n^{2}\log^{2}(1+x)}{2!} + \cdots $$

Here the coefficient of $n$ is $\log(1+x)$. The two expansions are the same
function of $n$, so their coefficients of $n$ must agree:

$$ \log(1+x) = x - \frac{x^{2}}{2} + \frac{x^{3}}{3} - \frac{x^{4}}{4} + \cdots,
\qquad -1 < x \le 1 $$

Replacing $x$ by $-x$ gives
$\log(1-x) = -x - \frac{x^{2}}{2} - \frac{x^{3}}{3} - \cdots$, and subtracting,

$$ \log\frac{1+x}{1-x} = 2\left(x + \frac{x^{3}}{3} + \frac{x^{5}}{5} + \cdots\right) $$
:::

::: key Where each series is valid
$$ e^{x} = \sum_{r=0}^{\infty}\frac{x^{r}}{r!} \ \text{ for all } x, \qquad
\log(1+x) = \sum_{r=1}^{\infty}\frac{(-1)^{r-1}x^{r}}{r} \ \text{ for } -1 < x \le 1 $$
Put $x = 1$ in the log series and you get $\log 2 = 1 - \frac12 + \frac13 - \cdots$;
put $x = -1$ and the terms become $-1 - \frac12 - \frac13 - \cdots$, which has no
sum. That is why the condition $x > -1$ must be stated.
:::

The exponential series converges because its terms carry a factorial in the
denominator: each new term is the previous one multiplied by $x/r$, a factor that
eventually becomes tiny. Laying the terms end to end on a line, the pieces pack
into a finite length.

```figure caption="Left: the terms of $1+1+\frac{1}{2!}+\frac{1}{3!}+\cdots$ laid end to end fill an interval of length $e$ and never pass it. Right: the partial sums climb to $e = 2.7183$ within four terms."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(5.2,2.5))
import math
terms = [1/math.factorial(r) for r in range(9)]
cols = ['#1d6fb8','#d9534f','#2e8b57','#b8860b','#6a5acd','#008b8b']
x0 = 0.0
for r, t in enumerate(terms):
    ax1.add_patch(Rectangle((x0, 0), t, 0.55, facecolor=cols[r % 6], alpha=0.35,
                            edgecolor=INK, lw=0.7))
    if r < 4:
        ax1.text(x0 + t/2, 0.70, ['$1$','$1$','$\\frac{1}{2!}$','$\\frac{1}{3!}$'][r],
                 ha='center', fontsize=8.6, color=INK)
    x0 += t
ax1.axvline(math.e, color=INK, lw=1.2, ls='--')
ax1.annotate('', xy=(0, -0.22), xytext=(math.e, -0.22),
             arrowprops=dict(arrowstyle='<|-|>', color=MUTED, lw=0.9, mutation_scale=7))
ax1.text(math.e/2, -0.50, 'total length $= e$', ha='center', fontsize=9.0, color=INK)
ax1.set_xlim(-0.12, 3.05); ax1.set_ylim(-0.72, 1.05)
ax1.axis('off')
ns = np.arange(1, 9)
S = np.cumsum(terms)[:8]
ax2.plot(ns, S, 'o-', color=ACCENT, ms=4.0)
ax2.axhline(math.e, color='#d9534f', lw=1.0, ls='--')
ax2.text(4.4, math.e - 0.24, '$e = 2.7183$', color='#d9534f', fontsize=9.0)
ax2.set_xlabel('terms used'); ax2.set_ylabel('partial sum')
ax2.set_ylim(0.9, 3.0); ax2.set_xlim(0.6, 8.4)
ax2.spines[['top','right']].set_visible(False)
ax2.grid(True, alpha=.5)
```

Truncating the exponential series gives polynomials that hug $e^{x}$ over a wider
and wider range as more terms are kept.

```figure caption="Partial sums of $e^{x}$. One term is a line, two a parabola; by six terms the polynomial is indistinguishable from $e^{x}$ on $-2 \le x \le 2$."
import numpy as np, matplotlib.pyplot as plt
import math
fig, ax = plt.subplots(figsize=(4.8,2.8))
x = np.linspace(-2.4, 2.2, 400)
ax.plot(x, np.exp(x), color=INK, lw=2.0, label='$e^{x}$')
for m, c in [(2, '#d9534f'), (3, '#b8860b'), (6, '#2e8b57')]:
    y = sum(x**r/math.factorial(r) for r in range(m))
    ax.plot(x, y, lw=1.3, ls='--', color=c, label=f'{m} terms')
ax.set_xlabel('$x$'); ax.set_ylabel('value')
ax.set_ylim(-1.5, 8.0); ax.set_xlim(-2.4, 2.2)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.5); ax.legend(loc='upper left', fontsize=8.0)
```

```figure caption="Partial sums of $\log(1+x) = x - \frac{x^{2}}{2} + \frac{x^{3}}{3} - \cdots$ for $x = 1$ (they close in on $\log 2 = 0.6931$, slowly and from both sides) and for $x = -1.2$, where the terms grow and the series has no sum."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.9,2.8))
r = np.arange(1, 15)
for xv, c, lab in [(1.0, ACCENT, '$x=1$'), (0.5, '#2e8b57', '$x=0.5$'),
                   (-1.2, '#d9534f', '$x=-1.2$')]:
    S = np.cumsum([(-1)**(k-1)*xv**k/k for k in r])
    ax.plot(r, S, 'o-', color=c, ms=3.4, label=lab)
ax.axhline(np.log(2), color=ACCENT, lw=0.9, ls='--', alpha=0.8)
ax.axhline(np.log(1.5), color='#2e8b57', lw=0.9, ls='--', alpha=0.8)
ax.text(7.6, 1.16, '$\\log 2 = 0.6931$', color=ACCENT, fontsize=8.8)
ax.text(2.0, 0.02, '$\\log 1.5 = 0.4055$', color='#2e8b57', fontsize=8.8)
ax.text(4.6, -2.3, 'no sum when x ≤ -1', color='#d9534f', fontsize=8.8)
ax.set_xlabel('number of terms'); ax.set_ylabel('partial sum')
ax.set_xlim(0.5, 14.5); ax.set_ylim(-3.0, 1.55)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.5); ax.legend(loc='lower right', fontsize=8.0)
```

::: example Worked example 4.11
**Problem.** Sum the series $1 + \dfrac{1}{2!} + \dfrac{1}{3!} + \dfrac{1}{4!}
+ \cdots$ and the series
$\dfrac{1}{1!} + \dfrac{1}{3!} + \dfrac{1}{5!} + \cdots$

**Solution.** *First series.* The exponential series with $x = 1$ is
$e = 1 + \frac{1}{1!} + \frac{1}{2!} + \frac{1}{3!} + \cdots$. Our series is that
one without the leading $1$ (since $\frac{1}{1!} = 1$ is the given first term):

$$ 1 + \frac{1}{2!} + \frac{1}{3!} + \cdots = e - 1 = 1.71828 $$

*Second series.* Write both $x = 1$ and $x = -1$:

$$ e = 1 + \frac{1}{1!} + \frac{1}{2!} + \frac{1}{3!} + \cdots $$
$$ e^{-1} = 1 - \frac{1}{1!} + \frac{1}{2!} - \frac{1}{3!} + \cdots $$

**Subtracting** kills all the even-power terms and doubles the odd ones:

$$ e - e^{-1} = 2\left(\frac{1}{1!} + \frac{1}{3!} + \frac{1}{5!} + \cdots\right)
\;\Longrightarrow\; \text{sum} = \frac{e - e^{-1}}{2} = \frac{e^{2}-1}{2e} $$

Numerically $\frac{2.71828 - 0.36788}{2} = 1.17520$.
:::

::: example Worked example 4.12
**Problem.** Show that $\dfrac{1}{1!} + \dfrac{2}{2!} + \dfrac{3}{3!} + \cdots = e$.

**Solution.** Look at the general term and cancel:

$$ t_r = \frac{r}{r!} = \frac{r}{r\,(r-1)!} = \frac{1}{(r-1)!} $$

So the series is

$$ \sum_{r=1}^{\infty}\frac{1}{(r-1)!} = \frac{1}{0!} + \frac{1}{1!} + \frac{1}{2!}
+ \cdots = e $$

using $0! = 1$. The whole method is "simplify the general term until a factorial
series appears".
:::

::: example Worked example 4.13
**Problem.** Using $\log\dfrac{1+x}{1-x} = 2\left(x + \dfrac{x^{3}}{3}
+ \dfrac{x^{5}}{5} + \cdots\right)$, find $\log 1.2$ correct to four decimal
places.

**Solution.** Choose $x$ so that $\dfrac{1+x}{1-x} = 1.2 = \dfrac{6}{5}$:

$$ 5(1+x) = 6(1-x) \;\Longrightarrow\; 5 + 5x = 6 - 6x \;\Longrightarrow\;
x = \frac{1}{11} $$

Since $|x|$ is small the series converges quickly:

$$ \log 1.2 = 2\left(\frac{1}{11} + \frac{1}{3(11)^{3}} + \frac{1}{5(11)^{5}}
+ \cdots\right) $$

$$ = 2\left(0.0909091 + 0.0002502 + 0.0000012\right) = 2(0.0911605) = 0.18232 $$

So $\log 1.2 \approx 0.1823$. (Using the plain series $\log(1+x)$ with $x = 0.2$
would need six terms for the same accuracy.)
:::

::: caution $\log$ here means $\log_e$
In this unit $\log x$ always means the natural logarithm $\ln x$. Every series
above is wrong by a factor of $\log_{10} e = 0.4343$ if you read it as a base-10
logarithm.
:::

## Chapter summary

- $\sum_{k=1}^{n} k = \dfrac{n(n+1)}{2}$,
  $\sum_{k=1}^{n} k^{2} = \dfrac{n(n+1)(2n+1)}{6}$,
  $\sum_{k=1}^{n} k^{3} = \dfrac{n^{2}(n+1)^{2}}{4} = \left(\sum k\right)^{2}$.
- Sigma is linear: $\sum(a_k \pm b_k) = \sum a_k \pm \sum b_k$ and
  $\sum c\,a_k = c\sum a_k$, with $\sum_{k=1}^{n} c = nc$.
- To sum a series, write $t_k$ as a polynomial in $k$, split with the sigma
  rules, substitute the three standard sums, factorise, then test on $n = 1$.
- For a part-sum, $\sum_{k=m}^{n} = \sum_{k=1}^{n} - \sum_{k=1}^{m-1}$.
- Induction: state $P(n)$; prove $P(1)$; assume $P(k)$; **use the assumption** to
  prove $P(k+1)$; conclude for all $n \in \mathbb{N}$.
- $e = 1 + \frac{1}{1!} + \frac{1}{2!} + \cdots = 2.71828$ and
  $e^{x} = \sum_{r\ge 0} \frac{x^{r}}{r!}$ for every real $x$; $a^{x} = e^{x\log a}$.
- $e + e^{-1} = 2\left(1 + \frac{1}{2!} + \frac{1}{4!} + \cdots\right)$ and
  $e - e^{-1} = 2\left(\frac{1}{1!} + \frac{1}{3!} + \cdots\right)$.
- $\log(1+x) = x - \frac{x^{2}}{2} + \frac{x^{3}}{3} - \cdots$ for
  $-1 < x \le 1$, and
  $\log\frac{1+x}{1-x} = 2\left(x + \frac{x^{3}}{3} + \frac{x^{5}}{5} + \cdots\right)$.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. $\sum_{k=1}^{n} k^{2}$ equals <span class="marks">[1]</span>
   (a) $\frac{n(n+1)}{2}$ (b) $\frac{n(n+1)(2n+1)}{6}$ (c) $\frac{n^{2}(n+1)^{2}}{4}$ (d) $\frac{n(n+1)(n+2)}{3}$
2. The value of $1^{3} + 2^{3} + \cdots + 10^{3}$ is <span class="marks">[1]</span>
   (a) $385$ (b) $2025$ (c) $3025$ (d) $5050$
3. In a proof by induction, the step that is proved first is <span class="marks">[1]</span>
   (a) $P(k+1)$ (b) $P(k)$ (c) $P(1)$ (d) $P(n)$ for all $n$
4. The sum $1 + \frac{1}{1!} + \frac{1}{2!} + \frac{1}{3!} + \cdots$ equals <span class="marks">[1]</span>
   (a) $e$ (b) $e - 1$ (c) $e + 1$ (d) $e^{-1}$
5. The series $x - \frac{x^{2}}{2} + \frac{x^{3}}{3} - \cdots$ is valid for <span class="marks">[1]</span>
   (a) all $x$ (b) $x > 0$ (c) $-1 < x \le 1$ (d) $|x| > 1$
6. If $\sum_{k=1}^{n} k = 210$, then $n$ is <span class="marks">[1]</span>
   (a) $19$ (b) $20$ (c) $21$ (d) $22$

::: note Answers to Group A
**1.** (b) — the standard sum of squares; the denominator is $6$.

**2.** (c) — $\left[\frac{10 \times 11}{2}\right]^{2} = 55^{2} = 3025$.

**3.** (c) — the basis step; without it the chain has nothing to start from.

**4.** (c) — the series for $e$ is $1 + \frac{1}{1!} + \frac{1}{2!} + \cdots$, and
this one has an extra leading $1$, so the sum is $1 + e$.

**5.** (c) — at $x = -1$ the terms become $-1 - \frac12 - \frac13 - \cdots$, which
has no sum.

**6.** (b) — $\frac{n(n+1)}{2} = 210$ gives $n^{2}+n-420 = 0$, $(n-20)(n+21)=0$,
so $n = 20$.
:::

**Group B — Short answer (5 marks each)**

1. Prove that $\sum_{k=1}^{n} k^{2} = \dfrac{n(n+1)(2n+1)}{6}$ and hence find
   $11^{2} + 12^{2} + \cdots + 30^{2}$. <span class="marks">[5]</span>
2. Find the sum to $n$ terms of $1\cdot 2\cdot 3 + 2\cdot 3\cdot 4 + 3\cdot 4\cdot 5
   + \cdots$ and evaluate it for $n = 10$. <span class="marks">[5]</span>
3. Find the sum of the cubes of the first $n$ odd natural numbers,
   $1^{3} + 3^{3} + \cdots + (2n-1)^{3}$, and evaluate it for $n = 10$. <span class="marks">[5]</span>
4. Prove by mathematical induction that $n(n+1)(n+2)$ is divisible by $6$ for
   every natural number $n$. <span class="marks">[5]</span>
5. Prove by mathematical induction that
   $1 + 4 + 7 + \cdots + (3n-2) = \dfrac{n(3n-1)}{2}$. <span class="marks">[5]</span>
6. Sum the series $1 + \dfrac{1}{2!} + \dfrac{1}{4!} + \dfrac{1}{6!} + \cdots$ <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Add the identity $(k+1)^{3} - k^{3} = 3k^{2} + 3k + 1$ for
$k = 1, \ldots, n$. The left side telescopes to $(n+1)^{3} - 1$, so

$$ n^{3} + 3n^{2} + 3n = 3\sum k^{2} + \frac{3n(n+1)}{2} + n $$

which rearranges to $\sum k^{2} = \frac{n(n+1)(2n+1)}{6}$ (full working in §4.2).

Then

$$ \sum_{k=11}^{30} k^{2} = \frac{30(31)(61)}{6} - \frac{10(11)(21)}{6}
= 9455 - 385 = 9070 $$

**2.** $t_k = k(k+1)(k+2) = k^{3} + 3k^{2} + 2k$, so

$$ S_n = \frac{n^{2}(n+1)^{2}}{4} + \frac{3n(n+1)(2n+1)}{6} + 2\cdot\frac{n(n+1)}{2} $$

Take out $\dfrac{n(n+1)}{4}$:

$$ S_n = \frac{n(n+1)}{4}\left[n(n+1) + 2(2n+1) + 4\right]
= \frac{n(n+1)(n^{2}+5n+6)}{4} = \frac{n(n+1)(n+2)(n+3)}{4} $$

Test $n=1$: $\frac{1(2)(3)(4)}{4} = 6 = 1\cdot 2\cdot 3$. Correct. For $n = 10$:
$S_{10} = \frac{10(11)(12)(13)}{4} = \frac{17160}{4} = 4290$.

**3.** $t_k = (2k-1)^{3} = 8k^{3} - 12k^{2} + 6k - 1$, so

$$ S_n = 8\cdot\frac{n^{2}(n+1)^{2}}{4} - 12\cdot\frac{n(n+1)(2n+1)}{6}
+ 6\cdot\frac{n(n+1)}{2} - n $$

$$ = 2n^{2}(n+1)^{2} - 2n(n+1)(2n+1) + 3n(n+1) - n $$

Take out $n$ and expand the bracket:
$2n(n+1)^{2} - 2(n+1)(2n+1) + 3(n+1) - 1
= 2n^{3}+4n^{2}+2n - 4n^{2}-6n-2 + 3n+3-1 = 2n^{3} - n$. Hence

$$ S_n = n\left(2n^{3} - n\right) = n^{2}\left(2n^{2}-1\right) $$

Test $n = 2$: $4(8-1) = 28 = 1 + 27$. Correct. For $n = 10$:
$S_{10} = 100(199) = 19900$.

**4.** Let $P(n)$: "$6 \mid n(n+1)(n+2)$".

*Basis:* $n=1$ gives $1\cdot 2\cdot 3 = 6$, divisible by $6$.

*Step:* assume $k(k+1)(k+2) = 6m$ for an integer $m$. Then

$$ (k+1)(k+2)(k+3) = k(k+1)(k+2) + 3(k+1)(k+2) = 6m + 3(k+1)(k+2) $$

Of the two consecutive integers $k+1$, $k+2$ one is even, so $(k+1)(k+2) = 2p$
for an integer $p$ and $3(k+1)(k+2) = 6p$. Hence the total is $6(m+p)$, divisible
by $6$. By induction the result holds for all $n$.

**5.** Let $P(n)$: $1 + 4 + \cdots + (3n-2) = \frac{n(3n-1)}{2}$.

*Basis:* $n=1$: LHS $=1$, RHS $=\frac{1(2)}{2} = 1$. True.

*Step:* assume the sum to $k$ terms is $\frac{k(3k-1)}{2}$. The next term is
$3(k+1)-2 = 3k+1$, so

$$ \frac{k(3k-1)}{2} + (3k+1) = \frac{3k^{2}-k+6k+2}{2} = \frac{3k^{2}+5k+2}{2}
= \frac{(k+1)(3k+2)}{2} $$

and $3k+2 = 3(k+1)-1$, so this is the formula with $n = k+1$. Hence true for all
$n$ by induction.

**6.** Add the series for $e$ and $e^{-1}$:

$$ e + e^{-1} = 2\left(1 + \frac{1}{2!} + \frac{1}{4!} + \cdots\right) $$

because the odd-power terms cancel. Therefore

$$ 1 + \frac{1}{2!} + \frac{1}{4!} + \cdots = \frac{e + e^{-1}}{2}
= \frac{e^{2}+1}{2e} = \frac{2.71828 + 0.36788}{2} = 1.54308 $$
:::

**Group C — Long answer (8 marks each)**

1. (a) Prove that $1^{3} + 2^{3} + \cdots + n^{3} = \left[\frac{n(n+1)}{2}\right]^{2}$
   by telescoping $(k+1)^{4} - k^{4}$. <span class="marks">[4]</span>
   (b) Find the sum to $n$ terms of the series whose $n^{\text{th}}$ term is
   $n(n+1)(2n+1)$, and check your formula for $n = 2$. <span class="marks">[4]</span>
2. (a) State the principle of mathematical induction and use it to prove that
   $2^{n} > n$ for every natural number $n$. <span class="marks">[4]</span>
   (b) Prove by induction that $\frac{1}{1\cdot 3} + \frac{1}{3\cdot 5}
   + \cdots + \frac{1}{(2n-1)(2n+1)} = \frac{n}{2n+1}$. <span class="marks">[4]</span>
3. (a) Derive the exponential series for $e^{x}$ from
   $e^{x} = \lim_{n\to\infty}\left(1+\frac{x}{n}\right)^{n}$. <span class="marks">[4]</span>
   (b) Prove that $\log\frac{1+x}{1-x} = 2\left(x + \frac{x^{3}}{3}
   + \frac{x^{5}}{5} + \cdots\right)$ and use it to compute $\log 1.1$ correct to
   four decimal places. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** (a) $(k+1)^{4} - k^{4} = 4k^{3} + 6k^{2} + 4k + 1$. Summing for
$k = 1, \ldots, n$ telescopes the left side to $(n+1)^{4} - 1$:

$$ (n+1)^{4} - 1 = 4\sum k^{3} + n(n+1)(2n+1) + 2n(n+1) + n $$

Since $(n+1)^{4} - 1 - n = n(n+1)(n^{2}+3n+3)$,

$$ 4\sum k^{3} = n(n+1)\left[n^{2}+3n+3 - (2n+1) - 2\right] = n(n+1)\cdot n(n+1) $$

so $\sum k^{3} = \frac{n^{2}(n+1)^{2}}{4} = \left[\frac{n(n+1)}{2}\right]^{2}$.

(b) $t_k = k(k+1)(2k+1) = 2k^{3} + 3k^{2} + k$, so

$$ S_n = \frac{2n^{2}(n+1)^{2}}{4} + \frac{3n(n+1)(2n+1)}{6} + \frac{n(n+1)}{2} $$

$$ = \frac{n(n+1)}{2}\left[n(n+1) + (2n+1) + 1\right] = \frac{n(n+1)(n^{2}+3n+2)}{2} $$

$$ = \frac{n(n+1)^{2}(n+2)}{2} $$

Check $n = 2$: formula gives $\frac{2(9)(4)}{2} = 36$; direct sum is
$1\cdot2\cdot3 + 2\cdot3\cdot5 = 6 + 30 = 36$. Correct.

**2.** (a) *Statement:* if $P(1)$ is true and $P(k) \Rightarrow P(k+1)$ for every
$k \in \mathbb{N}$, then $P(n)$ is true for all $n \in \mathbb{N}$.

Let $P(n)$: $2^{n} > n$. *Basis:* $2^{1} = 2 > 1$. True.
*Step:* assume $2^{k} > k$. Then

$$ 2^{k+1} = 2\cdot 2^{k} > 2k = k + k \ge k + 1 $$

since $k \ge 1$. So $2^{k+1} > k+1$, i.e. $P(k+1)$ holds, and the result follows
for all $n$ by induction.

(b) *Basis:* $n=1$: LHS $= \frac{1}{1\cdot 3} = \frac13$ and RHS
$= \frac{1}{3}$. True.

*Step:* assume the sum to $k$ terms is $\frac{k}{2k+1}$. Add the next term
$\frac{1}{(2k+1)(2k+3)}$:

$$ \frac{k}{2k+1} + \frac{1}{(2k+1)(2k+3)} = \frac{k(2k+3)+1}{(2k+1)(2k+3)}
= \frac{2k^{2}+3k+1}{(2k+1)(2k+3)} $$

$$ = \frac{(2k+1)(k+1)}{(2k+1)(2k+3)} = \frac{k+1}{2(k+1)+1} $$

which is the formula with $n = k+1$. Hence it holds for all $n$.

**3.** (a) Expand $\left(1+\frac{x}{n}\right)^{n}$ by the binomial theorem:

$$ 1 + n\cdot\frac{x}{n} + \frac{n(n-1)}{2!}\cdot\frac{x^{2}}{n^{2}}
+ \frac{n(n-1)(n-2)}{3!}\cdot\frac{x^{3}}{n^{3}} + \cdots $$

$$ = 1 + x + \frac{x^{2}}{2!}\left(1-\frac{1}{n}\right)
+ \frac{x^{3}}{3!}\left(1-\frac{1}{n}\right)\left(1-\frac{2}{n}\right) + \cdots $$

As $n \to \infty$ each bracket $\to 1$, so
$e^{x} = 1 + \frac{x}{1!} + \frac{x^{2}}{2!} + \frac{x^{3}}{3!} + \cdots$

(b) From the logarithmic series,
$\log(1+x) = x - \frac{x^{2}}{2} + \frac{x^{3}}{3} - \cdots$ and, replacing $x$ by
$-x$, $\log(1-x) = -x - \frac{x^{2}}{2} - \frac{x^{3}}{3} - \cdots$. Subtracting,
the even powers cancel and the odd ones double:

$$ \log\frac{1+x}{1-x} = \log(1+x) - \log(1-x)
= 2\left(x + \frac{x^{3}}{3} + \frac{x^{5}}{5} + \cdots\right) $$

For $\log 1.1$ put $\frac{1+x}{1-x} = \frac{11}{10}$, i.e. $10+10x = 11-11x$, so
$x = \frac{1}{21}$:

$$ \log 1.1 = 2\left(\frac{1}{21} + \frac{1}{3(21)^{3}} + \cdots\right)
= 2\left(0.0476190 + 0.0000360\right) = 0.09531 $$

So $\log 1.1 \approx 0.0953$.
:::
