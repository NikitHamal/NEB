---
subject: Mathematics
grade: 11
unit: 2
title: Real Numbers
hours: 4
area: Algebra
---

Every number you will use this year — every coordinate, every limit, every root — is a
real number. This short unit pins down what that means: how the real numbers fill a
straight line with no gaps, how to name a stretch of that line (an interval), and how to
measure distance along it (absolute value). Intervals and absolute values then reappear
constantly as domains, ranges and error bounds, so the notation must become automatic.

::: key What the exam asks for
Expect one Group A mark on interval notation or on $|x|$, and a Group B question that is
almost always one of three things: convert a recurring decimal to a fraction, represent a
surd such as $\sqrt{5}$ on the number line by construction, or solve an absolute-value
equation or inequality and show the answer as an interval.
:::

## 2.1 Geometric representation of real numbers

The number systems are built up in stages, each containing the one before it.

| Symbol | Name | Description | Examples |
|---|---|---|---|
| $\mathbb{N}$ | Natural numbers | counting numbers | $1, 2, 3, \dots$ |
| $\mathbb{W}$ | Whole numbers | $\mathbb{N}$ together with $0$ | $0, 1, 2, \dots$ |
| $\mathbb{Z}$ | Integers | whole numbers and their negatives | $\dots, -2, -1, 0, 1, \dots$ |
| $\mathbb{Q}$ | Rational numbers | $p/q$ with $p, q \in \mathbb{Z}$, $q \ne 0$ | $\frac{3}{4}, -5, 0.25, 0.\overline{3}$ |
| $\mathbb{Q}^c$ | Irrational numbers | reals that are **not** of the form $p/q$ | $\sqrt{2}, \sqrt[3]{7}, \pi, e$ |
| $\mathbb{R}$ | Real numbers | $\mathbb{Q} \cup \mathbb{Q}^c$ | all of the above |

So $\mathbb{N} \subset \mathbb{W} \subset \mathbb{Z} \subset \mathbb{Q} \subset \mathbb{R}$,
and $\mathbb{Q} \cap \mathbb{Q}^c = \emptyset$.

```figure caption="The real number system. Each region contains the one inside it; the irrationals $\mathbb{Q}^c$ are everything in $\mathbb{R}$ outside $\mathbb{Q}$."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.0,3.0))
boxes = [((0.10,0.10),9.80,4.90,'#f3f6fa'),
         ((0.45,0.45),6.05,4.20,'#e7eff8'),
         ((0.80,0.80),4.00,2.95,'#d8e6f4'),
         ((1.15,1.40),2.35,1.50,'#c4d9ef')]
for (x,y),w,h,c in boxes:
    ax.add_patch(FancyBboxPatch((x,y), w, h, boxstyle='round,pad=0.06',
                                fc=c, ec=MUTED, lw=0.9))
ax.text(1.35, 2.58, '$\\mathbb{N}$', fontsize=11, color=INK)
ax.text(2.33, 1.95, '1, 2, 3, ...', fontsize=8.6, color=INK, ha='center')
ax.text(1.00, 3.42, '$\\mathbb{Z}$', fontsize=11, color=INK)
ax.text(2.95, 1.05, '..., -2, -1, 0', fontsize=8.6, color=INK, ha='center')
ax.text(0.66, 4.20, '$\\mathbb{Q}$', fontsize=11, color=INK)
ax.text(5.60, 2.55, '$\\frac{3}{4}$,  $-\\frac{7}{2}$,', fontsize=9, color=INK, ha='center')
ax.text(5.60, 1.55, '$0.25$,  $0.\\overline{3}$', fontsize=9, color=INK, ha='center')
ax.text(9.40, 4.62, '$\\mathbb{R}$', fontsize=11, color=INK)
ax.text(8.15, 3.20, '$\\mathbb{Q}^c$  (irrational)', fontsize=9, color=INK, ha='center')
ax.text(8.15, 2.35, '$\\sqrt{2}$,  $\\pi$,  $e$,', fontsize=9.5, color=INK, ha='center')
ax.text(8.15, 1.55, '$\\sqrt[3]{7}$,  $0.1010010001...$'.replace('0.1010010001...','0.101001...'),
        fontsize=9.5, color=INK, ha='center')
ax.set_xlim(-0.05,10.05); ax.set_ylim(-0.05,5.25); ax.axis('off')
```

::: key Decimal test for rationality
A real number is **rational** exactly when its decimal expansion **terminates**
($0.375$) or **recurs** ($0.\overline{36} = 0.363636\dots$). It is **irrational** exactly
when the expansion is non-terminating and non-recurring ($\pi = 3.14159265\dots$).
:::

### The number line

Choose a point $O$ on a straight line to be $0$ and a point one unit to its right to be
$1$. Every real number then corresponds to exactly one point of the line, and every point
corresponds to exactly one real number. This **one-to-one correspondence** is what makes
the real line a *line*: it has no gaps. (The rationals alone leave gaps — there is no
rational point at the diagonal of a unit square.)

```figure caption="The real line. Rational and irrational points are interleaved; between any two distinct reals lie infinitely many of each kind."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,2.2))
ax.annotate('', xy=(4.2,0), xytext=(-3.2,0),
            arrowprops=dict(arrowstyle='<|-|>', color=INK, lw=1.3, mutation_scale=12))
for k in range(-3,5):
    ax.plot([k,k],[-0.07,0.07], color=INK, lw=1.0)
    ax.text(k, -0.30, str(k), fontsize=8.4, color=MUTED, ha='center')
pts = [(-2.0,'$-2$',ACCENT), (-1.5,'$-\\frac{3}{2}$',ACCENT), (0.5,'$\\frac{1}{2}$',ACCENT),
       (np.sqrt(2),'$\\sqrt{2}$',SERIES[1]), (np.pi,'$\\pi$',SERIES[1])]
for x,lab,c in pts:
    ax.plot([x],[0],'o',color=c,ms=5.5, zorder=4)
    ax.text(x, 0.22, lab, fontsize=9.5, color=c, ha='center')
ax.text(-3.1, 0.62, 'blue: rational    red: irrational', fontsize=8.2, color=MUTED)
ax.set_xlim(-3.5,4.5); ax.set_ylim(-0.55,0.95); ax.axis('off')
```

::: key Density of $\mathbb{Q}$ and $\mathbb{Q}^c$
Between any two distinct real numbers $a < b$ there is a rational number and also an
irrational number — hence infinitely many of each. A quick recipe: the mean
$\frac{a+b}{2}$ gives a rational between two rationals, and $a + \frac{b-a}{\sqrt{2}}$
gives an irrational between them.
:::

### Representing a surd on the number line

Irrational numbers of the form $\sqrt{n}$ can be located **exactly** with ruler and
compasses, using Pythagoras' theorem.

::: derivation Locating $\sqrt{2}$ and $\sqrt{3}$
**Step 1.** Draw the number line and mark $O$ at $0$ and $A$ at $1$.

**Step 2.** At $A$ erect $AB \perp OA$ with $AB = 1$ unit. Then by Pythagoras in the
right triangle $OAB$,

$$ OB = \sqrt{OA^{2} + AB^{2}} = \sqrt{1^{2} + 1^{2}} = \sqrt{2} $$

**Step 3.** With centre $O$ and radius $OB$, draw an arc cutting the number line at $P$.
Then $OP = \sqrt{2}$, so $P$ represents $\sqrt{2}$.

**Step 4.** Repeat: at $P$ erect $PQ \perp OP$ with $PQ = 1$. Then
$OQ = \sqrt{(\sqrt{2})^{2} + 1^{2}} = \sqrt{3}$, and an arc of radius $OQ$ cuts the line
at the point representing $\sqrt{3}$.

Continuing gives $\sqrt{4}, \sqrt{5}, \dots$ — this chain is called the *spiral of
Theodorus*. $\blacksquare$
:::

```figure caption="Constructing $\sqrt{2}$ and $\sqrt{3}$ on the number line. Each right triangle adds one to the square of the hypotenuse."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Arc
fig, ax = plt.subplots(figsize=(5.0,2.8))
r2, r3 = np.sqrt(2), np.sqrt(3)
ax.annotate('', xy=(2.65,0), xytext=(-0.55,0),
            arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.2, mutation_scale=11))
for k,lab in [(0,'O'),(1,'A')]:
    ax.plot([k],[0],'o',color=INK,ms=4)
    ax.text(k,-0.26,lab,fontsize=9,color=INK,ha='center')
ax.plot([1,1],[0,1], color=MUTED, lw=1.2)
ax.plot([0,1],[0,1], color=ACCENT, lw=1.6)
ax.text(1.05,1.02,'B',fontsize=9,color=INK)
ax.text(0.38,0.62,'$\\sqrt{2}$',fontsize=9.5,color=ACCENT)
ax.text(1.07,0.70,'1',fontsize=8.6,color=MUTED)
ax.text(0.50,-0.26,'1',fontsize=8.6,color=MUTED, ha='center')
ax.plot([r2,r2],[0,1], color=MUTED, lw=1.2)
ax.plot([0,r2],[0,1], color=SERIES[2], lw=1.6)
ax.text(r2+0.05,1.02,'Q',fontsize=9,color=INK)
ax.text(0.72,0.21,'$\\sqrt{3}$',fontsize=9.5,color=SERIES[2])
ax.text(r2+0.06,0.62,'1',fontsize=8.6,color=MUTED)
ax.add_patch(Arc((0,0), 2*r2, 2*r2, theta1=0, theta2=45, ec=ACCENT, lw=1.0, ls=(0,(3,2))))
ax.add_patch(Arc((0,0), 2*r3, 2*r3, theta1=0, theta2=30, ec=SERIES[2], lw=1.0, ls=(0,(3,2))))
for v,lab,c in [(r2,'$\\sqrt{2}$',ACCENT),(r3,'$\\sqrt{3}$',SERIES[2])]:
    ax.plot([v],[0],'o',color=c,ms=5)
    ax.text(v,-0.30,lab,fontsize=9.5,color=c,ha='center')
ax.text(2.0,-0.30,'2',fontsize=8.4,color=MUTED,ha='center')
ax.plot([2],[0],'|',color=MUTED,ms=7)
ax.set_xlim(-0.65,2.75); ax.set_ylim(-0.50,1.35)
ax.set_aspect('equal'); ax.axis('off')
```

::: example Worked example 2.1
**Problem.** Express $0.\overline{36}$ and $0.4\overline{7}$ as fractions in lowest terms.

**Solution.** **(a)** Let $x = 0.363636\dots$ Two digits repeat, so multiply by $10^2$:

$$ 100x = 36.363636\dots $$

Subtracting the first line from the second cancels the whole repeating tail:

$$ 100x - x = 36 \;\Rightarrow\; 99x = 36 \;\Rightarrow\; x = \frac{36}{99} = \frac{4}{11} $$

**(b)** Let $x = 0.4777\dots$ Here one digit repeats but only after one non-repeating
digit, so use two multipliers:

$$ 10x = 4.777\dots, \qquad 100x = 47.777\dots $$
$$ 100x - 10x = 43 \;\Rightarrow\; 90x = 43 \;\Rightarrow\; x = \frac{43}{90} $$

*Check:* $4 \div 11 = 0.3636\dots$ and $43 \div 90 = 0.4777\dots$ Both correct.
:::

::: derivation $\sqrt{2}$ is irrational (proof by contradiction)
Suppose, for contradiction, that $\sqrt{2}$ is rational. Then $\sqrt{2} = p/q$ where $p, q$
are integers with $q \ne 0$ and the fraction is in **lowest terms**, so $p$ and $q$ have
no common factor.

Squaring: $2 = p^{2}/q^{2}$, hence

$$ p^{2} = 2q^{2} $$

So $p^2$ is even, and therefore $p$ is even (the square of an odd number is odd). Write
$p = 2m$. Substituting,

$$ (2m)^{2} = 2q^{2} \;\Rightarrow\; 4m^{2} = 2q^{2} \;\Rightarrow\; q^{2} = 2m^{2} $$

So $q^2$ is even, hence $q$ is even. But then $p$ and $q$ are both even, contradicting
"no common factor". The assumption must be false, so $\sqrt{2}$ is irrational.
$\blacksquare$
:::

::: example Worked example 2.2
**Problem.** Insert one rational and one irrational number between $\frac{1}{3}$ and
$\frac{1}{2}$.

**Solution.** In decimals, $\frac{1}{3} = 0.3333\dots$ and $\frac{1}{2} = 0.5$.

**Rational:** take the mean,
$\frac{1}{2}\left(\frac{1}{3} + \frac{1}{2}\right) = \frac{1}{2} \cdot \frac{5}{6} = \frac{5}{12} = 0.41\overline{6}$,
which lies between them.

**Irrational:** any non-terminating, non-recurring decimal starting $0.4$ will do, for
example $0.401001000100001\dots$ (the number of zeros grows each time, so the expansion
never repeats). It satisfies $0.3333 < 0.4010\dots < 0.5$.
:::

## 2.2 Interval

::: definition Interval
An **interval** is a set of real numbers containing every number between any two of its
members — geometrically, an unbroken piece of the number line. A **square bracket**
includes the endpoint; a **round bracket** excludes it. $\infty$ and $-\infty$ are not
numbers, so they always take a round bracket.
:::

| Interval | Set-builder form | Name | Endpoints |
|---|---|---|---|
| $(a, b)$ | $\{x \in \mathbb{R} : a < x < b\}$ | open | neither included |
| $[a, b]$ | $\{x \in \mathbb{R} : a \le x \le b\}$ | closed | both included |
| $[a, b)$ | $\{x \in \mathbb{R} : a \le x < b\}$ | half-open (right-open) | $a$ only |
| $(a, b]$ | $\{x \in \mathbb{R} : a < x \le b\}$ | half-open (left-open) | $b$ only |
| $(a, \infty)$ | $\{x \in \mathbb{R} : x > a\}$ | open, unbounded above | none |
| $[a, \infty)$ | $\{x \in \mathbb{R} : x \ge a\}$ | closed, unbounded above | $a$ |
| $(-\infty, b]$ | $\{x \in \mathbb{R} : x \le b\}$ | closed, unbounded below | $b$ |
| $(-\infty, \infty)$ | $\mathbb{R}$ | the whole line | none |

The **length** of a bounded interval with endpoints $a < b$ is $b - a$, regardless of
which endpoints are included.

```figure caption="The six interval types on the number line. A hollow dot excludes the endpoint, a solid dot includes it."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,3.4))
a, b = 1.0, 4.0
rows = [('$[a, b]$',  True,  True,  None),
        ('$(a, b)$',  False, False, None),
        ('$[a, b)$',  True,  False, None),
        ('$(a, b]$',  False, True,  None),
        ('$[a, \\infty)$', True, None, 'right'),
        ('$(-\\infty, b]$', None, True, 'left')]
for i, (lab, la, lb, ray) in enumerate(rows):
    y = -i * 1.0
    ax.annotate('', xy=(5.6, y), xytext=(-0.6, y),
                arrowprops=dict(arrowstyle='<|-|>', color=GRID, lw=1.0, mutation_scale=9))
    if ray == 'right':
        ax.plot([a, 5.3], [y, y], color=ACCENT, lw=3.0, solid_capstyle='butt')
    elif ray == 'left':
        ax.plot([-0.3, b], [y, y], color=ACCENT, lw=3.0, solid_capstyle='butt')
    else:
        ax.plot([a, b], [y, y], color=ACCENT, lw=3.0, solid_capstyle='butt')
    for x, inc in [(a, la), (b, lb)]:
        if inc is None:
            continue
        ax.plot([x], [y], 'o', ms=7.0, mec=ACCENT, mew=1.5,
                mfc=(ACCENT if inc else 'white'), zorder=5)
    ax.text(-1.15, y, lab, fontsize=9.5, color=INK, ha='right', va='center')
    if la is not None:
        ax.text(a, y - 0.36, '$a$', fontsize=8.6, color=MUTED, ha='center')
    if lb is not None:
        ax.text(b, y - 0.36, '$b$', fontsize=8.6, color=MUTED, ha='center')
ax.set_xlim(-3.3, 5.9); ax.set_ylim(-5.6, 0.55); ax.axis('off')
```

Intervals can be combined like any other sets. The intersection of two intervals is the
overlap; the union is a single interval only if they meet or touch.

::: definition Neighbourhood
For $a \in \mathbb{R}$ and $\delta > 0$, the open interval $(a-\delta,\ a+\delta)$ is
called the **$\delta$-neighbourhood** of $a$. It is exactly the set
$\{x : |x - a| < \delta\}$. Removing $a$ itself gives the *deleted* neighbourhood, used
when defining limits in Unit 17.
:::

::: example Worked example 2.3
**Problem.** Write in interval notation: (a) $-3 < x \le 4$, (b) $x > 5$,
(c) all real $x$ except $x = 2$.

**Solution.**

(a) Left endpoint excluded, right included: $(-3, 4]$.

(b) Unbounded above, $5$ excluded: $(5, \infty)$.

(c) The line with one point removed is two rays:
$(-\infty, 2) \cup (2, \infty)$, also written $\mathbb{R} - \{2\}$. This is **not** a
single interval, because it is not unbroken.
:::

::: example Worked example 2.4
**Problem.** If $A = (-3, 4]$ and $B = [1, 7)$, find $A \cap B$, $A \cup B$ and $A - B$.

**Solution.** Draw both on one line and read off.

**$A \cap B$:** $x$ must satisfy $-3 < x \le 4$ **and** $1 \le x < 7$. The binding
conditions are $x \ge 1$ (from $B$) and $x \le 4$ (from $A$), so

$$ A \cap B = [1, 4] $$

**$A \cup B$:** the two intervals overlap, so the union is one interval running from the
smaller left endpoint to the larger right endpoint, keeping each endpoint's own bracket:

$$ A \cup B = (-3, 7) $$

**$A - B$:** the part of $A$ with $x < 1$, i.e. $A - B = (-3, 1)$.
:::

::: example Worked example 2.5
**Problem.** Solve $2x - 5 < 7$ and $3x + 1 \ge -8$ simultaneously, and write the
solution as an interval.

**Solution.** Solve each inequality separately.

$$ 2x - 5 < 7 \;\Rightarrow\; 2x < 12 \;\Rightarrow\; x < 6 $$
$$ 3x + 1 \ge -8 \;\Rightarrow\; 3x \ge -9 \;\Rightarrow\; x \ge -3 $$

Both must hold, so we intersect: $-3 \le x < 6$, that is $[-3, 6)$.
:::

::: caution Multiplying an inequality by a negative number
Multiplying or dividing an inequality by a **negative** number reverses the sign:
from $-2x < 6$ we get $x > -3$, not $x < -3$. Adding, subtracting, and multiplying by a
positive number leave the direction unchanged.
:::

## 2.3 Absolute value

::: definition Absolute value (modulus)
For $x \in \mathbb{R}$,

$$ |x| = x \ \text{ if } x \ge 0, \qquad |x| = -x \ \text{ if } x < 0 $$

Equivalently $|x| = \sqrt{x^{2}}$, the **non-negative** square root. Geometrically $|x|$
is the distance of the point $x$ from the origin, and $|x - y|$ is the distance between
the points $x$ and $y$.
:::

::: key Properties of the absolute value
For all real $a, b$:

- $|a| \ge 0$, and $|a| = 0$ only when $a = 0$
- $|-a| = |a|$ and $|a|^{2} = a^{2}$
- $|ab| = |a|\,|b|$ and $|a/b| = |a|/|b|$ for $b \ne 0$
- $-|a| \le a \le |a|$
- **Triangle inequality:** $|a + b| \le |a| + |b|$
- $| \,|a| - |b|\, | \le |a - b|$ (the reverse triangle inequality)
:::

::: key Solving with absolute values (let $k > 0$)
| Statement | Equivalent to | As an interval |
|---|---|---|
| $|x| = k$ | $x = k$ or $x = -k$ | two points |
| $|x| < k$ | $-k < x < k$ | $(-k, k)$ |
| $|x| \le k$ | $-k \le x \le k$ | $[-k, k]$ |
| $|x| > k$ | $x < -k$ or $x > k$ | $(-\infty, -k) \cup (k, \infty)$ |
| $|x - a| < \delta$ | $a - \delta < x < a + \delta$ | $(a-\delta,\ a+\delta)$ |

Read the last line as "$x$ is within $\delta$ of $a$". *Less than* gives **one** interval;
*greater than* gives **two**.
:::

```figure caption="Graphs of $y = |x|$, $y = |x-2|$ and $y = |x| - 2$. The V is shifted right by 2 and down by 2 respectively; the corner is where the inside expression is zero."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,2.8))
x = np.linspace(-4, 5, 600)
ax.plot(x, np.abs(x), color=ACCENT, lw=1.9, label='$y = |x|$')
ax.plot(x, np.abs(x-2), color=SERIES[1], lw=1.7, ls='--', label='$y = |x-2|$')
ax.plot(x, np.abs(x)-2, color=SERIES[2], lw=1.7, ls=':', label='$y = |x|-2$')
for px, py, c in [(0,0,ACCENT), (2,0,SERIES[1]), (0,-2,SERIES[2])]:
    ax.plot([px],[py],'o',color=c,ms=4.5, zorder=5)
ax.axhline(0, color=MUTED, lw=0.8); ax.axvline(0, color=MUTED, lw=0.8)
ax.set_xlabel('$x$'); ax.set_ylabel('$y$')
ax.set_xlim(-4,5); ax.set_ylim(-2.6,4.6)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.45); ax.legend(loc='upper center', ncol=3, fontsize=8.0, columnspacing=1.0)
```

::: derivation The triangle inequality $|a+b| \le |a| + |b|$
For any real $a$ we know $-|a| \le a \le |a|$, and likewise $-|b| \le b \le |b|$.

Adding the two chains of inequalities term by term,

$$ -\left(|a| + |b|\right) \le a + b \le |a| + |b| $$

Now apply the rule "$|X| \le k$ is the same as $-k \le X \le k$", with $X = a+b$ and
$k = |a| + |b|$:

$$ |a + b| \le |a| + |b| $$

Equality holds exactly when $a$ and $b$ have the same sign (or one is zero).
$\blacksquare$
:::

::: example Worked example 2.6
**Problem.** Solve $|2x - 5| = 7$.

**Solution.** $|X| = 7$ means $X = 7$ or $X = -7$, so

$$ 2x - 5 = 7 \;\Rightarrow\; 2x = 12 \;\Rightarrow\; x = 6 $$
$$ 2x - 5 = -7 \;\Rightarrow\; 2x = -2 \;\Rightarrow\; x = -1 $$

*Check:* $|2(6)-5| = |7| = 7$ and $|2(-1)-5| = |-7| = 7$. Solution set $\{-1, 6\}$.
:::

::: example Worked example 2.7
**Problem.** Solve $|3x + 2| \le 8$ and write the answer in interval notation.

**Solution.** $|X| \le 8$ means $-8 \le X \le 8$:

$$ -8 \le 3x + 2 \le 8 $$

Subtract $2$ throughout:

$$ -10 \le 3x \le 6 $$

Divide by $3$ (positive, so no sign change):

$$ -\frac{10}{3} \le x \le 2 $$

The solution set is $\left[-\frac{10}{3},\ 2\right]$.
:::

::: example Worked example 2.8
**Problem.** Solve $|x - 4| > 3$ and interpret the answer geometrically.

**Solution.** $|X| > 3$ means $X > 3$ or $X < -3$:

$$ x - 4 > 3 \;\Rightarrow\; x > 7 \qquad\text{or}\qquad x - 4 < -3 \;\Rightarrow\; x < 1 $$

Solution set $(-\infty, 1) \cup (7, \infty)$.

**Geometrically:** $|x-4|$ is the distance from $x$ to $4$, so we want all points more
than $3$ units from $4$ — everything outside the interval $[1, 7]$, as found.
:::

```figure caption="Solving $|x-3| < 2$ graphically: the V-graph lies below the line $y=2$ exactly for $1 < x < 5$, i.e. within 2 units of 3."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6,2.8))
x = np.linspace(-1, 7, 600); y = np.abs(x-3)
ax.plot(x, y, color=ACCENT, lw=1.9, label='$y = |x-3|$')
ax.axhline(2, color=SERIES[1], lw=1.4, ls='--', label='$y = 2$')
ax.fill_between(x, y, 2, where=(y < 2), color=ACCENT, alpha=0.16)
for px in (1, 5):
    ax.plot([px],[2],'o', mfc='white', mec=SERIES[1], mew=1.5, ms=6.5, zorder=5)
    ax.plot([px,px],[0,2], color=MUTED, lw=0.8, ls=':')
ax.plot([1,5],[0,0], color=SERIES[2], lw=3.2, solid_capstyle='butt', zorder=4)
ax.text(3, 0.28, 'solution  $1 < x < 5$', fontsize=8.6, color=SERIES[2], ha='center')
ax.set_xticks([-1,0,1,2,3,4,5,6,7])
ax.set_xlabel('$x$'); ax.set_ylabel('$y$')
ax.set_xlim(-1,7); ax.set_ylim(0,4.4)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.45); ax.legend(loc='upper center', ncol=2, fontsize=8.2)
```

::: example Worked example 2.9
**Problem.** Solve $|2x - 1| = |x + 4|$.

**Solution.** $|A| = |B|$ means $A = B$ or $A = -B$.

**Case 1:** $2x - 1 = x + 4 \Rightarrow x = 5$.

**Case 2:** $2x - 1 = -(x + 4) \Rightarrow 2x - 1 = -x - 4 \Rightarrow 3x = -3 \Rightarrow x = -1$.

*Check:* at $x = 5$, $|9| = |9|$ ✓; at $x = -1$, $|-3| = 3$ and $|3| = 3$ ✓.
Solution set $\{-1, 5\}$.

(An alternative is to square both sides: $(2x-1)^2 = (x+4)^2$ gives
$3x^{2} - 12x - 15 = 0$, i.e. $x^{2} - 4x - 5 = 0$, $(x-5)(x+1) = 0$ — the same roots.)
:::

::: example Worked example 2.10
**Problem.** Solve $|x - 1| + |x - 3| = 4$.

**Solution.** Two modulus signs, so split the line at the points where each inside
expression changes sign: $x = 1$ and $x = 3$. That gives three cases.

**Case 1: $x < 1$.** Here $x-1 < 0$ and $x-3 < 0$, so both moduli flip sign:

$$ (1-x) + (3-x) = 4 \;\Rightarrow\; 4 - 2x = 4 \;\Rightarrow\; x = 0 $$

Since $0 < 1$, this is valid.

**Case 2: $1 \le x < 3$.** Here $x - 1 \ge 0$ but $x - 3 < 0$:

$$ (x-1) + (3-x) = 2 $$

This is $2$, never $4$, so there is **no** solution in this interval.

**Case 3: $x \ge 3$.** Both are non-negative:

$$ (x-1) + (x-3) = 4 \;\Rightarrow\; 2x - 4 = 4 \;\Rightarrow\; x = 4 $$

Since $4 \ge 3$, this is valid. The solution set is $\{0, 4\}$.

*Geometric reading:* $|x-1| + |x-3|$ is the total distance from $x$ to the points $1$ and
$3$. Between them that total is always $2$ (the gap); outside, it grows.
:::

```figure caption="$y = |x-1| + |x-3|$. The graph is flat at height 2 between the corners, so $y = 4$ has exactly two solutions, $x = 0$ and $x = 4$; $y = 2$ has infinitely many and $y = 1$ has none."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6,2.8))
x = np.linspace(-2, 6, 800); y = np.abs(x-1) + np.abs(x-3)
ax.plot(x, y, color=ACCENT, lw=1.9, label='$y = |x-1|+|x-3|$')
ax.axhline(4, color=SERIES[1], lw=1.3, ls='--', label='$y = 4$')
for px in (0, 4):
    ax.plot([px],[4],'o',color=SERIES[1],ms=5.5, zorder=5)
    ax.annotate(f'$x = {px}$', (px,4), textcoords='offset points',
                xytext=(-20 if px == 0 else 20, -4), fontsize=8.6,
                color=SERIES[1], ha='center')
ax.plot([1,3],[2,2], color=SERIES[2], lw=3.0, solid_capstyle='butt', zorder=4)
ax.annotate('flat: value $= 2$', (2,2), textcoords='offset points', xytext=(0,-16),
            fontsize=8.4, color=SERIES[2], ha='center')
ax.set_xticks([-2,-1,0,1,2,3,4,5,6])
ax.set_xlabel('$x$'); ax.set_ylabel('$y$')
ax.set_xlim(-2,6); ax.set_ylim(0,7.4)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.45); ax.legend(loc='upper center', ncol=2, fontsize=8.0)
```

::: example Worked example 2.11
**Problem.** Express $\{x : |x - 3| < 2\}$ as an interval, and write the interval
$(-1, 7)$ in the form $|x - a| < \delta$.

**Solution.** **(a)** $|x-3| < 2$ means $-2 < x - 3 < 2$, so $1 < x < 5$, i.e. $(1, 5)$.

**(b)** Reverse the process. The midpoint of $(-1, 7)$ is

$$ a = \frac{-1 + 7}{2} = 3, \qquad \delta = \frac{7 - (-1)}{2} = 4 $$

so $(-1, 7) = \{x : |x - 3| < 4\}$.
:::

::: caution $\sqrt{x^{2}} = |x|$, not $x$
$\sqrt{(-5)^{2}} = \sqrt{25} = 5 = |-5|$, not $-5$. The radical sign always denotes the
non-negative root. Similarly, $|x| = k$ has **two** solutions whenever $k > 0$, and
**none** when $k < 0$ — an equation such as $|3x-1| = -4$ has no solution at all.
:::

## Chapter summary

- $\mathbb{N} \subset \mathbb{W} \subset \mathbb{Z} \subset \mathbb{Q} \subset \mathbb{R}$;
  a real number is rational iff its decimal terminates or recurs.
- Each real number corresponds to exactly one point of the number line and conversely;
  $\sqrt{n}$ is located exactly by a Pythagorean construction.
- Between any two distinct reals there are infinitely many rationals and infinitely many
  irrationals.
- $(a,b)$ excludes endpoints, $[a,b]$ includes them; $\infty$ always takes a round
  bracket; the length of either is $b-a$.
- $|x| = x$ for $x \ge 0$ and $-x$ for $x < 0$; $|x| = \sqrt{x^{2}}$; $|x-y|$ is the
  distance from $x$ to $y$.
- $|x| < k \Leftrightarrow -k < x < k$ (one interval);
  $|x| > k \Leftrightarrow x < -k$ or $x > k$ (two intervals).
- Triangle inequality $|a+b| \le |a|+|b|$; a sum of two moduli is solved by splitting the
  line at the zeros of each inside expression.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. Which of the following is irrational? <span class="marks">[1]</span>
   (a) $\sqrt{16}$ (b) $0.\overline{27}$ (c) $\sqrt{7}$ (d) $\frac{22}{7}$
2. The set $\{x \in \mathbb{R} : -2 \le x < 5\}$ in interval notation is <span class="marks">[1]</span>
   (a) $(-2, 5)$ (b) $[-2, 5)$ (c) $(-2, 5]$ (d) $[-2, 5]$
3. $|x| < 3$ is equivalent to <span class="marks">[1]</span>
   (a) $x < 3$ (b) $x > -3$ (c) $-3 < x < 3$ (d) $x < -3$ or $x > 3$
4. $\sqrt{(-9)^{2}}$ equals <span class="marks">[1]</span>
   (a) $-9$ (b) $9$ (c) $\pm 9$ (d) $81$
5. The solution set of $|x| = -2$ is <span class="marks">[1]</span>
   (a) $\{2, -2\}$ (b) $\{-2\}$ (c) $\emptyset$ (d) $\mathbb{R}$
6. $(-\infty, 3] \cap (0, 5)$ equals <span class="marks">[1]</span>
   (a) $(0, 3]$ (b) $[0, 3)$ (c) $(0, 5)$ (d) $(-\infty, 5)$
7. The decimal $0.\overline{5}$ as a fraction is <span class="marks">[1]</span>
   (a) $\frac{1}{2}$ (b) $\frac{5}{9}$ (c) $\frac{5}{99}$ (d) $\frac{1}{5}$

::: note Answers to Group A
**1.** (c) — $\sqrt{16}=4$ is an integer, $0.\overline{27}$ recurs, $\frac{22}{7}$ is a ratio of integers; only $\sqrt{7}$ is a non-perfect-square surd.

**2.** (b) — $-2$ is included (square bracket), $5$ is not (round bracket).

**3.** (c) — "$|x|$ less than $k$" always collapses to the single interval $-k < x < k$.

**4.** (b) — $\sqrt{x^2} = |x|$, and $|-9| = 9$.

**5.** (c) — an absolute value is never negative, so no $x$ works.

**6.** (a) — need $x \le 3$ and $0 < x < 5$; the binding conditions are $x>0$ and $x \le 3$.

**7.** (b) — $x = 0.555\dots$, $10x = 5.555\dots$, $9x = 5$, $x = \frac{5}{9}$.
:::

**Group B — Short answer (5 marks each)**

1. Define rational and irrational numbers. Express $0.\overline{4}$ and $1.2\overline{3}$
   as fractions in lowest terms. <span class="marks">[5]</span>
2. Represent $\sqrt{5}$ on the number line by an exact geometric construction, justifying
   each step. <span class="marks">[5]</span>
3. Write in interval notation and represent on a number line: (i) $-2 \le x < 3$,
   (ii) $x > 5$, (iii) $|x| \le 4$. Also find $(-5, 2] \cap [0, 6)$. <span class="marks">[5]</span>
4. Solve $|3x - 2| < 4$ and express the solution as an interval. <span class="marks">[5]</span>
5. Solve the pair $|x - 2| \le 3$ and $|x + 1| > 1$ simultaneously. <span class="marks">[5]</span>
6. If $|x - 5| < 0.01$, find the interval containing $x$ and hence an upper bound for
   $|2x - 10|$. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** A **rational** number can be written $p/q$ with $p, q \in \mathbb{Z}$, $q \ne 0$;
its decimal terminates or recurs. An **irrational** number cannot be so written; its
decimal neither terminates nor recurs.

$x = 0.444\dots$, so $10x = 4.444\dots$ and $10x - x = 4$, giving $9x = 4$ and
$x = \frac{4}{9}$.

$x = 1.2333\dots$, so $10x = 12.333\dots$ and $100x = 123.333\dots$ Subtracting,
$90x = 111$, so $x = \frac{111}{90} = \frac{37}{30}$. *Check:* $37 \div 30 = 1.2333\dots$ ✓

**2.** Mark $O$ at $0$ and $A$ at $2$ on the number line. At $A$ erect $AB \perp OA$ with
$AB = 1$ unit. By Pythagoras,

$$ OB = \sqrt{OA^{2} + AB^{2}} = \sqrt{2^{2} + 1^{2}} = \sqrt{5} $$

With centre $O$ and radius $OB$, draw an arc meeting the number line at $P$ on the
positive side. Then $OP = OB = \sqrt{5}$ (radii of the same arc), so $P$ represents
$\sqrt{5} \approx 2.236$ — between $2$ and $3$, as expected since $4 < 5 < 9$.

**3.** (i) $[-2, 3)$: solid dot at $-2$, hollow at $3$, segment shaded between.
(ii) $(5, \infty)$: hollow dot at $5$, shading to the right.
(iii) $|x| \le 4$ means $-4 \le x \le 4$, i.e. $[-4, 4]$: solid dots at both ends.

For the intersection, $x$ must satisfy $-5 < x \le 2$ and $0 \le x < 6$. The binding
conditions are $x \ge 0$ and $x \le 2$, so $(-5, 2] \cap [0, 6) = [0, 2]$.

**4.** $|3x-2| < 4$ means $-4 < 3x - 2 < 4$. Adding $2$: $-2 < 3x < 6$. Dividing by $3$:

$$ -\frac{2}{3} < x < 2 $$

Solution set $\left(-\frac{2}{3},\ 2\right)$.

**5.** First inequality: $|x-2| \le 3 \Rightarrow -3 \le x-2 \le 3 \Rightarrow -1 \le x \le 5$,
i.e. $[-1, 5]$.

Second: $|x+1| > 1 \Rightarrow x+1 > 1$ or $x+1 < -1 \Rightarrow x > 0$ or $x < -2$,
i.e. $(-\infty,-2) \cup (0,\infty)$.

Intersecting: $[-1,5]$ has no points below $-2$, so only the piece $x > 0$ survives,
giving $(0, 5]$.

**6.** $|x-5| < 0.01$ means $-0.01 < x - 5 < 0.01$, so

$$ 4.99 < x < 5.01, \qquad \text{i.e. } x \in (4.99,\ 5.01) $$

Then $|2x - 10| = |2(x-5)| = 2|x-5| < 2(0.01) = 0.02$. So $|2x-10| < 0.02$.
:::

**Group C — Long answer (8 marks each)**

1. (a) Prove that $\sqrt{3}$ is irrational. <span class="marks">[4]</span>
   (b) Solve $|2x + 1| \ge 5$, write the solution in interval notation and show it on a
   number line. <span class="marks">[4]</span>
2. (a) State and prove the triangle inequality $|a+b| \le |a| + |b|$. <span class="marks">[4]</span>
   (b) Solve $|x - 2| + |x + 1| = 5$. <span class="marks">[4]</span>

::: note Answers to Group C
**1. (a)** Suppose $\sqrt{3} = p/q$ in lowest terms, $p, q \in \mathbb{Z}$, $q \ne 0$.
Squaring gives $p^{2} = 3q^{2}$, so $3 \mid p^{2}$, and since $3$ is prime, $3 \mid p$.
Write $p = 3m$. Then $9m^{2} = 3q^{2}$, so $q^{2} = 3m^{2}$, hence $3 \mid q^{2}$ and
$3 \mid q$. Now $3$ divides both $p$ and $q$, contradicting "lowest terms". Therefore
$\sqrt{3}$ is irrational.

**1. (b)** $|X| \ge 5$ means $X \ge 5$ or $X \le -5$:

$$ 2x + 1 \ge 5 \;\Rightarrow\; 2x \ge 4 \;\Rightarrow\; x \ge 2 $$
$$ 2x + 1 \le -5 \;\Rightarrow\; 2x \le -6 \;\Rightarrow\; x \le -3 $$

Solution set $(-\infty, -3] \cup [2, \infty)$. On the number line: a solid dot at $-3$
with shading to the left, a solid dot at $2$ with shading to the right, and the open gap
$(-3, 2)$ left unshaded.

**2. (a)** *Statement:* for all real $a, b$, $|a+b| \le |a| + |b|$.

*Proof.* Since $-|a| \le a \le |a|$ and $-|b| \le b \le |b|$, adding gives

$$ -(|a| + |b|) \le a + b \le |a| + |b| $$

A number $X$ satisfying $-k \le X \le k$ (with $k \ge 0$) satisfies $|X| \le k$. Taking
$X = a+b$ and $k = |a|+|b|$ gives $|a+b| \le |a| + |b|$. Equality occurs when $a$ and $b$
have the same sign or one of them is zero.

**2. (b)** The inside expressions vanish at $x = 2$ and $x = -1$, so split there.

**Case 1: $x < -1$.** Both are negative:
$(2 - x) + (-x - 1) = 5 \Rightarrow 1 - 2x = 5 \Rightarrow x = -2$. Valid, as $-2 < -1$.

**Case 2: $-1 \le x < 2$.** Then $|x-2| = 2-x$ and $|x+1| = x+1$:
$(2-x) + (x+1) = 3 \ne 5$, so no solution here.

**Case 3: $x \ge 2$.** Both are non-negative:
$(x-2) + (x+1) = 5 \Rightarrow 2x - 1 = 5 \Rightarrow x = 3$. Valid, as $3 \ge 2$.

Solution set $\{-2, 3\}$. *Check:* at $x=-2$, $|-4| + |-1| = 4+1 = 5$ ✓; at $x=3$,
$|1| + |4| = 1+4 = 5$ ✓.
:::
