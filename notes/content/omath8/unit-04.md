---
subject: Optional Mathematics
grade: 8
unit: 4
title: Limit
hours: 0
---

Stand 4 metres from a wall and walk half of the remaining distance, again and again. You will be 2 m away, then 1 m, then 0.5 m, then 0.25 m, … . You get as close to the wall as you like, yet no single step puts you exactly on it. The wall is the **limit** of your positions. The idea of a limit, a value that a list of numbers or a changing quantity **approaches** without necessarily reaching, is one of the most powerful ideas in mathematics: it is how Archimedes found the value of $\pi$, how we know that $0.999\ldots$ equals 1, and later it becomes the foundation of calculus. This chapter builds the idea from sequences of numbers, from sequences of diagrams and from the values of functions, and then introduces the notation used to write it.

::: key What your examination asks from this chapter
Expect: (i) write the next terms of a sequence and state the number it **approaches**; (ii) say which of several sequences has a limit and which does not; (iii) find how many terms are needed for the terms to come within a given distance of the limit; (iv) a sequence of diagrams (polygons in a circle, shaded squares) and its limiting perimeter or area; (v) complete a **table of values** of $f(x)$ near $x=a$ and state the limit; (vi) explain the difference between the **value** $f(a)$ and the **limit** of $f(x)$ as $x\rightarrow a$; (vii) evaluate simple limits by substitution or by factorising and cancelling; (viii) read and write the notation $\lim_{x\to a}f(x)=l$.
:::

## 4.1 Concept of limit from sequences of numbers

Look at the sequence $\frac{1}{2}, \frac{2}{3}, \frac{3}{4}, \frac{4}{5}, \ldots$, whose general term is $t_n=\frac{n}{n+1}$. As decimals the terms are $0.5, 0.667, 0.75, 0.8, 0.833, 0.857, 0.875, \ldots$. They keep increasing, but they never pass 1. How close do they come?

| $n$ | 1 | 9 | 99 | 999 | 9999 |
|---|---|---|---|---|---|
| $t_n=\frac{n}{n+1}$ | 0.5 | 0.9 | 0.99 | 0.999 | 0.9999 |
| gap $1-t_n=\frac{1}{n+1}$ | 0.5 | 0.1 | 0.01 | 0.001 | 0.0001 |

The gap between the terms and 1 shrinks towards zero. Whatever small distance you choose, 0.01 or 0.000 001, the terms eventually come closer to 1 than that, and **stay** closer for ever after. We say that the sequence **tends to 1**, or that its **limit is 1**.

::: definition Limit of a sequence
A number $l$ is the **limit** of a sequence if the terms come **as close to $l$ as we wish** and **remain** that close for all later terms. We then say that the sequence **converges** (or tends) to $l$. A sequence that has no such number has **no limit**.
:::

Two points in this definition are easy to miss.

- **The limit need not be a term.** No term of $\frac{n}{n+1}$ equals 1, because the gap $\frac{1}{n+1}$ is never zero. The limit is a target, not a member of the list.
- **"Getting closer" is not enough.** The terms of $\frac{n}{n+1}$ also get closer to 2 at every step, but they never come within 1 unit of 2. The limit is the one number they get **arbitrarily** close to.

```figure caption="Terms of two sequences marked on number lines. Above, $t_n=\frac{n}{n+1}$ crowds towards 1 from the left. Below, $t_n=\frac{(-1)^{n+1}}{n}$ (1, $-\frac{1}{2}$, $\frac{1}{3}$, $-\frac{1}{4}$, …) closes in on 0 from both sides in turn."
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(5.0, 2.8))
for ax in (ax1, ax2):
    ax.set_ylim(-0.6, 0.9); ax.set_yticks([])
    for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=8)
ax1.set_xlim(0.4, 1.06)
ts = [n/(n + 1) for n in range(1, 41)]
ax1.plot(ts, [0]*len(ts), '|', color=ACCENT, ms=12, mew=1.4)
for n in range(1, 5):
    ax1.text(n/(n + 1), 0.42, f'{n}/{n + 1}', ha='center', fontsize=8, color=ACCENT)
ax1.plot([1], [0], 'o', color=SERIES[1], ms=6)
ax1.text(1.0, 0.42, 'limit 1', ha='center', fontsize=8, color=SERIES[1])
ax1.set_xticks([0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
ax2.set_xlim(-0.6, 1.1)
vals = [((-1)**(n + 1))/n for n in range(1, 31)]
ax2.plot(vals, [0]*len(vals), '|', color=SERIES[2], ms=12, mew=1.4)
for n, lab in [(1, '1'), (2, '−1/2'), (3, '1/3'), (4, '−1/4')]:
    ax2.text(((-1)**(n + 1))/n, 0.42, lab, ha='center', fontsize=8, color=SERIES[2])
ax2.plot([0], [0], 'o', color=SERIES[1], ms=6)
ax2.text(0.0, -0.55, 'limit 0', ha='center', fontsize=8, color=SERIES[1])
ax2.set_xticks([-0.5, 0, 0.5, 1.0])
fig.tight_layout(pad=0.5)
```

### Sequences with and without a limit

| Sequence | Behaviour | Limit |
|---|---|---|
| $0.9, 0.99, 0.999, \ldots$ | gap to 1 is $0.1, 0.01, 0.001, \ldots$ | 1 |
| $1, \frac{1}{2}, \frac{1}{4}, \frac{1}{8}, \ldots$ | halves each time | 0 |
| $2.1, 2.01, 2.001, \ldots$ | comes down towards 2 | 2 |
| $1, -\frac{1}{2}, \frac{1}{3}, -\frac{1}{4}, \ldots$ | jumps from side to side, but the jumps shrink | 0 |
| $5, 5, 5, \ldots$ | already at 5 | 5 |
| $1, 2, 3, 4, \ldots$ | grows without bound | none |
| $1, -1, 1, -1, \ldots$ | keeps jumping between two values | none |

A sequence like $1, 2, 3, \ldots$ is said to **tend to infinity**, written $\infty$. Infinity is not a number; the phrase only means "becomes larger than any number you name".

::: example How far along must we go?
**Problem.** For $t_n=\frac{n}{n+1}$, from which term onwards are all the terms within 0.01 of the limit 1?

**Solution.** The gap is $1-\frac{n}{n+1}=\frac{n+1-n}{n+1}=\frac{1}{n+1}$. We need
$$ \frac{1}{n+1}<0.01=\frac{1}{100}\quad\Longrightarrow\quad n+1>100\quad\Longrightarrow\quad n>99 $$
At $n=99$ the gap is exactly 0.01, not less. So **from the 100th term onwards** every term lies within 0.01 of 1. For a closer target, say 0.001, we would need $n>999$: the closer the target, the further along we must go, but there is always some term after which the terms stay that close.
:::

::: example Halving towards zero
**Problem.** The sequence $\frac{1}{2}, \frac{1}{4}, \frac{1}{8}, \ldots$ has $t_n=\frac{1}{2^n}$. State its limit and find the first term that is less than 0.001.

**Solution.** Each term is half of the one before, and the terms stay positive, so they shrink towards **0**. We need $\frac{1}{2^n}<\frac{1}{1000}$, that is $2^n>1000$. Since $2^9=512$ and $2^{10}=1024$, the first such term is the **10th**, $t_{10}=\frac{1}{1024}\approx0.000\,98$.
:::

::: example A recurring decimal as a limit
**Problem.** Show that the sequence $0.3, 0.33, 0.333, \ldots$ tends to $\frac{1}{3}$.

**Solution.** Compare each term with $\frac{1}{3}$:
$$ \frac{1}{3}-0.3=\frac{1}{30},\qquad \frac{1}{3}-0.33=\frac{1}{300},\qquad \frac{1}{3}-0.333=\frac{1}{3000} $$
Each extra digit divides the gap by 10, so the gap shrinks towards 0 and the limit is $\frac{1}{3}$. This is what the recurring decimal $0.\overline{3}$ means. In the same way $0.9, 0.99, 0.999, \ldots$ tends to 1, which is why $0.\overline{9}=1$.
:::

::: example Splitting the general term
**Problem.** Find the limit of the sequence with $t_n=\frac{2n+1}{n}$.

**Solution.** Divide each part of the numerator by $n$:
$$ t_n=\frac{2n}{n}+\frac{1}{n}=2+\frac{1}{n} $$
As $n$ grows, $\frac{1}{n}$ shrinks towards 0, so $t_n$ tends to $2+0=2$. The terms $3, 2.5, 2.333, 2.25, 2.2, \ldots$ come down towards 2 from above.
:::

::: caution A limit is not the last term
An infinite sequence has **no last term**, so the limit cannot be "the last one". And a sequence that is still far from settling, like $1, -1, 1, -1, \ldots$, has no limit at all, even though its terms never leave the interval from $-1$ to 1. Always ask: is there **one** number that the terms come as close to as I like, and stay close to?
:::

## 4.2 Concept of limit from sequences of diagrams

Limits also appear when a shape is changed step by step. Each step gives a number (a perimeter, an area) and the numbers form a sequence.

### Polygons inside a circle

Draw a circle of radius 1 and fit a regular polygon inside it, with every corner on the circle. With 6 sides the polygon is a hexagon whose sides are equal to the radius, so its perimeter is 6. Double the number of sides to 12, then 24, then 48: the polygon hugs the circle more and more closely.

| Number of sides | 4 | 6 | 12 | 24 | 48 | 96 |
|---|---|---|---|---|---|---|
| Perimeter | 5.6569 | 6.0000 | 6.2117 | 6.2653 | 6.2787 | 6.2821 |
| Area | 2.0000 | 2.5981 | 3.0000 | 3.1058 | 3.1326 | 3.1394 |

The perimeters approach the circumference $2\pi r=2\pi\approx6.2832$, and the areas approach the area of the circle, $\pi r^2=\pi\approx3.1416$. Around 250 BC the Greek mathematician **Archimedes** used polygons of 96 sides, inside and outside a circle, to prove that $\pi$ lies between $3\frac{10}{71}$ and $3\frac{1}{7}$. The circle is the **limit** of the polygons.

```figure caption="Regular polygons of 6, 12 and 24 sides inscribed in a circle of radius 1. As the number of sides doubles, the polygon's perimeter (6.000, 6.212, 6.265) approaches the circumference of the circle, $2\pi\approx6.283$."
fig, axs = plt.subplots(1, 3, figsize=(5.0, 2.3))
t = np.linspace(0, 2*np.pi, 300)
for ax, n in zip(axs, (6, 12, 24)):
    ax.plot(np.cos(t), np.sin(t), color=MUTED, lw=1.0)
    a = np.linspace(0, 2*np.pi, n + 1) + np.pi/2
    ax.fill(np.cos(a), np.sin(a), color='#cfe3f6', zorder=0)
    ax.plot(np.cos(a), np.sin(a), color=ACCENT, lw=1.4)
    ax.set_title(f'{n} sides', fontsize=9, pad=2)
    ax.text(0, -1.42, f'perimeter {2*n*np.sin(np.pi/n):.3f}', ha='center', fontsize=8)
    ax.set_xlim(-1.25, 1.25); ax.set_ylim(-1.65, 1.2); ax.set_aspect('equal'); ax.axis('off')
fig.tight_layout(pad=0.3)
```

### Shading half of what is left

Take a square of area 1. Shade half of it. Then shade half of the part that is still white, then half of what is still white, and so on. After each step the shaded area is

$$ \frac{1}{2},\quad \frac{1}{2}+\frac{1}{4}=\frac{3}{4},\quad \frac{3}{4}+\frac{1}{8}=\frac{7}{8},\quad \frac{15}{16},\quad \frac{31}{32},\ \ldots $$

After $n$ steps the white part is $\frac{1}{2^n}$, so the shaded part is $1-\frac{1}{2^n}$. The white part tends to 0 and the shaded area tends to **1**, the whole square, although some white always remains after any number of steps. This is the same as saying that the series $\frac{1}{2}+\frac{1}{4}+\frac{1}{8}+\cdots$ has the limit 1.

### A staircase under a slope

Inside a square of side 1, draw the diagonal from the bottom-left corner to the top-right corner. The triangle under the diagonal has area $\frac{1}{2}$. Now fit a staircase of $n$ equal steps under the diagonal. Its area is
$$ \frac{1}{n}\left(\frac{0}{n}+\frac{1}{n}+\cdots+\frac{n-1}{n}\right)=\frac{1}{n^2}\times\frac{(n-1)n}{2}=\frac{n-1}{2n} $$
using $1+2+\cdots+(n-1)=\frac{(n-1)n}{2}$ from the previous chapter. For 4 steps the area is 0.375, for 8 steps 0.4375, for 100 steps 0.495. As the steps get finer, the staircase area tends to $\frac{1}{2}$, the area of the triangle.

```figure caption="Two sequences of diagrams. Left: shading half of what is left; after five steps $\frac{31}{32}$ of the square is shaded, and the shaded area tends to 1. Right: a staircase of 8 steps under the diagonal of a unit square has area $\frac{7}{16}$; with more and finer steps the area tends to $\frac{1}{2}$."
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(5.0, 2.7))
shades = ['#1d6fb8', '#4a8fd0', '#78acdd', '#a6c9ea', '#cfe3f6']
x, y, w, h = 0.0, 0.0, 1.0, 1.0
labels = ['1/2', '1/4', '1/8', '1/16', '1/32']
for k in range(5):
    if k % 2 == 0:
        ax1.add_patch(Rectangle((x, y), w/2, h, fc=shades[k], ec='white', lw=1.0))
        cx, cy = x + w/4, y + h/2; x = x + w/2; w = w/2
    else:
        ax1.add_patch(Rectangle((x, y + h/2), w, h/2, fc=shades[k], ec='white', lw=1.0))
        cx, cy = x + w/2, y + 3*h/4; h = h/2
    if k < 3:
        ax1.text(cx, cy, labels[k], ha='center', va='center', fontsize=8.5, color='white' if k < 2 else INK)
ax1.add_patch(Rectangle((0, 0), 1, 1, fill=False, ec=INK, lw=1.2))
ax1.set_xlim(-0.05, 1.05); ax1.set_ylim(-0.05, 1.05); ax1.set_aspect('equal'); ax1.axis('off')
n = 8
ax2.add_patch(Rectangle((0, 0), 1, 1, fill=False, ec=INK, lw=1.2))
for k in range(n):
    ax2.add_patch(Rectangle((k/n, 0), 1/n, k/n, fc='#d5efdf', ec=SERIES[2], lw=0.8))
ax2.plot([0, 1], [0, 1], color=SERIES[1], lw=1.5)
ax2.text(0.3, 0.72, 'diagonal', fontsize=8.5, color=SERIES[1], rotation=45, ha='center', va='center')
ax2.text(0.72, 0.16, '8 steps', fontsize=8.5, color=INK, ha='center')
ax2.set_xlim(-0.05, 1.05); ax2.set_ylim(-0.05, 1.05); ax2.set_aspect('equal'); ax2.axis('off')
fig.tight_layout(pad=0.4)
```

::: example How many shading steps are needed?
**Problem.** In the shading process above, after how many steps is the white part of the square less than 1% of the square?

**Solution.** After $n$ steps the white part is $\frac{1}{2^n}$. We need $\frac{1}{2^n}<\frac{1}{100}$, that is $2^n>100$. Since $2^6=64$ and $2^7=128$, **7 steps** are needed. The shaded area is then $1-\frac{1}{128}=\frac{127}{128}\approx0.992$.
:::

::: example The perimeter limit for a real circle
**Problem.** A regular hexagon is drawn inside a circle of radius 5 cm. Find its perimeter. What do the perimeters of the inscribed 12-gon, 24-gon, 48-gon, … approach?

**Solution.** In a regular hexagon inside a circle each side equals the radius, so the perimeter is $6\times5=30$ cm. As the number of sides keeps doubling, the perimeters increase towards the circumference $2\pi r=2\times\pi\times5=10\pi\approx31.42$ cm. They never reach it, because a straight side is always a little shorter than the arc it cuts off.
:::

## 4.3 Value of a function and its limiting value

The same idea works for a function $f(x)$. Instead of letting $n$ grow, we let $x$ come closer and closer to a fixed number $a$, from both sides, and watch what happens to $f(x)$.

### When the limit equals the value

Take $f(x)=2x+1$ and let $x$ approach 3.

| $x$ | 2.9 | 2.99 | 2.999 | → 3 ← | 3.001 | 3.01 | 3.1 |
|---|---|---|---|---|---|---|---|
| $f(x)=2x+1$ | 6.8 | 6.98 | 6.998 | → 7 ← | 7.002 | 7.02 | 7.2 |

From the left and from the right, $f(x)$ approaches 7. The **limiting value** of $f(x)$ as $x$ approaches 3 is 7. The **value** of the function at 3 is $f(3)=2(3)+1=7$ as well. For a smooth, unbroken graph such as a straight line, the limit and the value agree.

### When there is no value but there is a limit

Now take
$$ f(x)=\frac{x^2-4}{x-2} $$
At $x=2$ the fraction becomes $\frac{4-4}{2-2}=\frac{0}{0}$, which has no meaning. So $f(2)$ is **not defined**. But near 2 the function behaves perfectly well:

| $x$ | 1.9 | 1.99 | 1.999 | → 2 ← | 2.001 | 2.01 | 2.1 |
|---|---|---|---|---|---|---|---|
| $f(x)$ | 3.9 | 3.99 | 3.999 | → 4 ← | 4.001 | 4.01 | 4.1 |

The values approach 4 from both sides. So the **limit is 4, although the value does not exist**. Factorising shows why: for every $x\neq2$,
$$ f(x)=\frac{(x-2)(x+2)}{x-2}=x+2 $$
so the graph is the straight line $y=x+2$ with a single point missing at $(2,4)$, a "hole".

### When the value and the limit are different

A function can also be defined piece by piece. Let $g(x)=x+1$ for every $x\neq1$, but $g(1)=5$. Near 1 the values of $g$ are close to $1+1=2$, so the limit as $x$ approaches 1 is **2**, while the value $g(1)$ is **5**. The graph is the line $y=x+1$ with a hole at $(1,2)$ and a lonely dot at $(1,5)$.

### When there is no limit

A car park charges Rs 20 for any time up to and including 2 hours, and Rs 40 for more than 2 hours (up to 4 hours). Let $F(t)$ be the fee for $t$ hours. Just before 2 hours the fee is Rs 20; just after, it is Rs 40. As $t$ approaches 2 from the left, $F(t)$ approaches 20; from the right it approaches 40. The two sides disagree, so $F(t)$ has **no limit** as $t$ approaches 2, even though the value $F(2)=20$ exists.

```figure caption="Limit and value compared. Left: $f(x)=\frac{x^2-4}{x-2}$ is the line $y=x+2$ with a hole at $(2,4)$; the limit at 2 is 4 but $f(2)$ is undefined. Middle: the limit at 1 is 2 but the value is 5. Right: a parking fee jumps from Rs 20 to Rs 40 at 2 hours, so the two sides disagree and there is no limit at 2."
fig, axs = plt.subplots(1, 3, figsize=(5.0, 2.6))
x = np.linspace(-0.2, 4.0, 100)
ax = axs[0]
ax.plot(x, x + 2, color=ACCENT, lw=1.6)
ax.plot([2], [4], 'o', mfc='white', mec=ACCENT, ms=6, mew=1.4)
ax.set_title('value undefined', fontsize=8.5, pad=3)
ax.set_xlim(-0.2, 4); ax.set_ylim(0, 6.6); ax.set_xticks([0, 2, 4]); ax.set_yticks([0, 2, 4, 6])
ax = axs[1]
x2 = np.linspace(-1.0, 3.0, 100)
ax.plot(x2, x2 + 1, color=ACCENT, lw=1.6)
ax.plot([1], [2], 'o', mfc='white', mec=ACCENT, ms=6, mew=1.4)
ax.plot([1], [5], 'o', color=SERIES[1], ms=6)
ax.set_title('value ≠ limit', fontsize=8.5, pad=3)
ax.set_xlim(-1, 3); ax.set_ylim(-0.2, 6.6); ax.set_xticks([-1, 1, 3]); ax.set_yticks([0, 2, 4, 6])
ax = axs[2]
ax.plot([0, 2], [20, 20], color=ACCENT, lw=2.0)
ax.plot([2, 4], [40, 40], color=ACCENT, lw=2.0)
ax.plot([2], [20], 'o', color=ACCENT, ms=6)
ax.plot([2], [40], 'o', mfc='white', mec=ACCENT, ms=6, mew=1.4)
ax.set_title('no limit at 2', fontsize=8.5, pad=3)
ax.set_xlim(0, 4.2); ax.set_ylim(0, 50); ax.set_xticks([0, 2, 4]); ax.set_yticks([0, 20, 40])
ax.set_xlabel('hours', fontsize=8); ax.set_ylabel('fee (Rs)', fontsize=8)
for ax in axs:
    ax.grid(True, color=GRID, lw=0.5); ax.set_axisbelow(True)
    ax.spines[['top', 'right']].set_visible(False); ax.tick_params(labelsize=7.5)
fig.tight_layout(pad=0.4)
```

::: key Value and limit are separate questions
| Question | How to answer it |
|---|---|
| What is the **value** $f(a)$? | put $x=a$ in the rule (it may be undefined) |
| What is the **limit** as $x$ approaches $a$? | look at $f(x)$ for $x$ **close to** $a$, on both sides, but never equal to $a$ |

The limit can exist when the value does not, the two can differ, and the value can exist when the limit does not. When they are equal, the graph has no break at $a$.
:::

::: example Completing a table of values
**Problem.** Complete the table for $f(x)=3x-1$ and state the limiting value of $f(x)$ as $x$ approaches 2. Is it equal to $f(2)$?

| $x$ | 1.9 | 1.99 | 2.01 | 2.1 |
|---|---|---|---|---|
| $f(x)$ | | | | |

**Solution.** $f(1.9)=5.7-1=4.7$, $f(1.99)=4.97$, $f(2.01)=5.03$, $f(2.1)=5.3$. From both sides the values approach **5**. The value is $f(2)=6-1=5$, so here the limit and the value are equal.
:::

## 4.4 Notation of limit

Saying "as $x$ comes closer and closer to 2, $f(x)$ comes closer and closer to 4" every time is long. Mathematics shortens it with an arrow and the word lim.

::: definition Limit notation
$x\rightarrow a$ is read "**$x$ tends to $a$**" or "$x$ approaches $a$". It means that $x$ takes values closer and closer to $a$, from either side, but **never equal to $a$**.

$$ \lim_{x\to a}f(x)=l $$
is read "**the limit of $f(x)$ as $x$ tends to $a$ is $l$**". It means that $f(x)$ can be made as close to $l$ as we wish by taking $x$ close enough to $a$.

For a sequence we write $\lim_{n\to\infty}t_n=l$, "the limit of $t_n$ as $n$ tends to infinity is $l$".
:::

| In words | In symbols |
|---|---|
| As $x$ approaches 3, $2x+1$ approaches 7 | $\lim_{x\to3}(2x+1)=7$ |
| As $x$ approaches 2, $\frac{x^2-4}{x-2}$ approaches 4 | $\lim_{x\to2}\frac{x^2-4}{x-2}=4$ |
| As $n$ increases without bound, $\frac{1}{n}$ approaches 0 | $\lim_{n\to\infty}\frac{1}{n}=0$ |
| As $n$ increases without bound, $\frac{n}{n+1}$ approaches 1 | $\lim_{n\to\infty}\frac{n}{n+1}=1$ |

### Approaching from one side

Sometimes we need to say from which side $x$ approaches $a$. We write $x\rightarrow a^-$ for values **less** than $a$ (from the left) and $x\rightarrow a^+$ for values **greater** than $a$ (from the right). For the parking fee,
$$ \lim_{t\to2^-}F(t)=20 \qquad\text{and}\qquad \lim_{t\to2^+}F(t)=40 $$
The limit $\lim_{t\to2}F(t)$ exists only when the left-hand and right-hand values agree, so here it does not exist.

### Finding simple limits

**Method 1: substitution.** For a polynomial, the graph has no breaks, so the limit is simply the value: put $x=a$.

**Method 2: factorise and cancel.** If substitution gives $\frac{0}{0}$, the numerator and denominator share a factor $(x-a)$. Factorise, cancel the common factor (allowed, because $x\neq a$), and then substitute.

::: example Limits by substitution
**Problem.** Evaluate (i) $\lim_{x\to2}(3x^2-1)$ (ii) $\lim_{x\to-1}(x^3+2x)$.

**Solution.** (i) $3(2)^2-1=12-1=11$. (ii) $(-1)^3+2(-1)=-1-2=-3$.
:::

::: example Limits of the form 0/0
**Problem.** Evaluate (i) $\lim_{x\to3}\frac{x^2-9}{x-3}$ (ii) $\lim_{x\to1}\frac{x^2+x-2}{x-1}$ (iii) $\lim_{x\to2}\frac{x^2-5x+6}{x-2}$.

**Solution.** Each gives $\frac{0}{0}$ on substitution, so factorise first.

(i) $\frac{(x-3)(x+3)}{x-3}=x+3$, so the limit is $3+3=6$.

(ii) $\frac{(x+2)(x-1)}{x-1}=x+2$, so the limit is $1+2=3$.

(iii) $\frac{(x-2)(x-3)}{x-2}=x-3$, so the limit is $2-3=-1$.

**Check (i) with a table.** At $x=2.99$: $\frac{8.9401-9}{-0.01}=5.99$; at $x=3.01$: $\frac{9.0601-9}{0.01}=6.01$. Both are close to 6 ✓.
:::

::: example Limits of sequences in the new notation
**Problem.** Find (i) $\lim_{n\to\infty}\frac{3}{n}$ (ii) $\lim_{n\to\infty}\frac{2n+1}{n}$ (iii) $\lim_{n\to\infty}\left(1-\frac{1}{2^n}\right)$.

**Solution.** (i) $\frac{3}{n}$ gets smaller without end: the limit is **0**.

(ii) $\frac{2n+1}{n}=2+\frac{1}{n}$, and $\frac{1}{n}$ tends to 0, so the limit is **2**.

(iii) $\frac{1}{2^n}$ tends to 0, so the limit is $1-0=$ **1**. This is the shaded area of the square in section 4.2.
:::

::: caution 0/0 is a signal, not an answer
When substitution gives $\frac{0}{0}$, the answer is **not** 0, not 1 and not "undefined". It tells you that a common factor is hiding. Cancel it and substitute again. Remember also that $x\rightarrow a$ never means $x=a$: that is exactly why cancelling the factor $(x-a)$ is allowed.
:::

::: tip Use a table to check any limit
Pick two values just below $a$ and two just above (such as 1.99, 1.999 and 2.001, 2.01). If both sides of the table settle on the same number, that number is the limit, and it should match your algebra. If the two sides settle on different numbers, there is no limit.
:::

::: note Activity — the halving walk
Work in pairs in the school ground. Mark a line 4 m from a wall (or a fixed post). One student walks half of the remaining distance to the wall at each step while the other records (1) the distance left and (2) the total distance walked. Continue for six steps. You should find the distances left are 2, 1, 0.5, 0.25, 0.125, 0.0625 m and the totals are 2, 3, 3.5, 3.75, 3.875, 3.9375 m. Write the limit of each sequence, and explain why no step ever lands exactly on the wall.
:::

## Chapter summary

- A sequence has **limit $l$** if its terms come as close to $l$ as we wish and stay that close; the limit need not be a term.
- $\frac{n}{n+1}\rightarrow1$, $\frac{1}{2^n}\rightarrow0$, $0.9, 0.99, \ldots\rightarrow1$; sequences such as $1, 2, 3, \ldots$ and $1, -1, 1, \ldots$ have no limit.
- Sequences of diagrams have limits too: inscribed polygons tend to the circle (perimeter $\rightarrow2\pi r$, area $\rightarrow\pi r^2$); shading half of what is left tends to the whole square.
- The **value** $f(a)$ is found by putting $x=a$; the **limit** comes from values of $x$ close to $a$ on both sides, never equal to $a$.
- The limit can exist without the value (a hole), the two can differ, or there can be no limit (a jump).
- Notation: $\lim_{x\to a}f(x)=l$; $\lim_{n\to\infty}t_n=l$; one-sided limits $x\rightarrow a^-$ and $x\rightarrow a^+$ must agree for the limit to exist.
- Polynomial limits: substitute. A $\frac{0}{0}$ form: factorise, cancel the common factor, then substitute.

## Practice questions

**Group A — Objective (1 mark each)**

1. The limit of the sequence $0.9, 0.99, 0.999, \ldots$ is <span class="marks">[1]</span>
   (a) 0.9 (b) 0.999 (c) 1 (d) 10
2. The sequence $1, \frac{1}{2}, \frac{1}{4}, \frac{1}{8}, \ldots$ approaches <span class="marks">[1]</span>
   (a) 1 (b) $\frac{1}{2}$ (c) 0 (d) $-1$
3. The sequence $\frac{1}{2}, \frac{2}{3}, \frac{3}{4}, \frac{4}{5}, \ldots$ tends to <span class="marks">[1]</span>
   (a) 0 (b) $\frac{1}{2}$ (c) 1 (d) 2
4. Which sequence has no limit? <span class="marks">[1]</span>
   (a) $1, \frac{1}{2}, \frac{1}{3}, \ldots$ (b) $1, -1, 1, -1, \ldots$ (c) $5, 5, 5, \ldots$ (d) $0.3, 0.33, 0.333, \ldots$
5. As the number of sides of a regular polygon inscribed in a circle of radius $r$ increases, its perimeter approaches <span class="marks">[1]</span>
   (a) $\pi r^2$ (b) $2\pi r$ (c) $4r$ (d) $6r$
6. "$x\rightarrow3$" means <span class="marks">[1]</span>
   (a) $x$ equals 3 (b) $x$ comes closer and closer to 3 (c) $x$ is greater than 3 (d) $x$ is at most 3
7. $\lim_{x\to2}(3x+4)$ equals <span class="marks">[1]</span>
   (a) 6 (b) 10 (c) 7 (d) 2
8. $\lim_{x\to3}\frac{x^2-9}{x-3}$ equals <span class="marks">[1]</span>
   (a) 0 (b) 3 (c) 6 (d) 9
9. For $f(x)=\frac{x^2-1}{x-1}$, the value $f(1)$ is <span class="marks">[1]</span>
   (a) 0 (b) 1 (c) 2 (d) not defined
10. $\lim_{n\to\infty}\frac{1}{n}$ equals <span class="marks">[1]</span>
    (a) 1 (b) 0 (c) $\infty$ (d) $n$
11. A square is shaded $\frac{1}{2}$, then $\frac{1}{2}+\frac{1}{4}$, then $\frac{1}{2}+\frac{1}{4}+\frac{1}{8}$, and so on. The shaded part approaches <span class="marks">[1]</span>
    (a) $\frac{1}{2}$ (b) $\frac{3}{4}$ (c) 1 (d) 2
12. The limit of $0.3, 0.33, 0.333, \ldots$ is <span class="marks">[1]</span>
    (a) 0.3 (b) $\frac{1}{3}$ (c) 3 (d) 0.4

::: note Answers to Group A
**1.** (c) — the gaps to 1 are $0.1, 0.01, 0.001, \ldots$, which shrink to 0.
**2.** (c) — halving positive numbers again and again brings them towards 0.
**3.** (c) — the gap $1-\frac{n}{n+1}=\frac{1}{n+1}$ tends to 0.
**4.** (b) — it keeps jumping between $1$ and $-1$ and never settles.
**5.** (b) — the polygons tend to the circle, whose circumference is $2\pi r$.
**6.** (b) — $x$ approaches 3 but is never equal to 3.
**7.** (b) — substitute: $3(2)+4=10$.
**8.** (c) — $\frac{(x-3)(x+3)}{x-3}=x+3\rightarrow6$.
**9.** (d) — substitution gives $\frac{0}{0}$, which has no value.
**10.** (b) — $\frac{1}{n}$ becomes as small as we like.
**11.** (c) — the white part $\frac{1}{2^n}$ tends to 0.
**12.** (b) — the gaps $\frac{1}{30}, \frac{1}{300}, \ldots$ tend to 0, so the limit is $\frac{1}{3}$.
:::

**Group B — Short answer (2 marks each)**

1. Write the next three terms of $\frac{1}{2}, \frac{3}{4}, \frac{7}{8}, \frac{15}{16}, \ldots$ and state the limit of the sequence. <span class="marks">[2]</span>
2. Find the limit of the sequence $t_n=\frac{2n+1}{n}$ by writing $t_n=2+\frac{1}{n}$. <span class="marks">[2]</span>
3. Complete a table of $f(x)=3x-1$ for $x=1.9, 1.99, 2.01, 2.1$ and state $\lim_{x\to2}f(x)$. <span class="marks">[2]</span>
4. Evaluate $\lim_{x\to-1}(x^2+3x+5)$. <span class="marks">[2]</span>
5. Evaluate $\lim_{x\to4}\frac{x^2-16}{x-4}$. <span class="marks">[2]</span>
6. Evaluate $\lim_{x\to1}\frac{x^2+2x-3}{x-1}$. <span class="marks">[2]</span>
7. For $f(x)=\frac{x^2-4}{x-2}$, explain the difference between $f(2)$ and $\lim_{x\to2}f(x)$. <span class="marks">[2]</span>
8. From which term onwards are the terms of $\frac{n}{n+1}$ within 0.001 of 1? <span class="marks">[2]</span>
9. Write in limit notation: "as $n$ increases without bound, $\frac{3}{n}$ gets closer and closer to 0". <span class="marks">[2]</span>
10. A regular hexagon is inscribed in a circle of radius 5 cm. Find its perimeter, and state what the perimeters of inscribed polygons of 12, 24, 48, … sides approach. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** The $n$th term is $\frac{2^n-1}{2^n}$, so the next terms are $\frac{31}{32}$, $\frac{63}{64}$, $\frac{127}{128}$. The gap to 1 is $\frac{1}{2^n}$, which tends to 0, so the limit is **1**.
**2.** $t_n=2+\frac{1}{n}$; as $n\rightarrow\infty$, $\frac{1}{n}\rightarrow0$, so $\lim_{n\to\infty}t_n=2$.
**3.** $f(1.9)=4.7$, $f(1.99)=4.97$, $f(2.01)=5.03$, $f(2.1)=5.3$. Both sides approach 5, so $\lim_{x\to2}f(x)=5$.
**4.** A polynomial: substitute. $1-3+5=3$.
**5.** $\frac{(x-4)(x+4)}{x-4}=x+4$, so the limit is $8$.
**6.** $\frac{(x+3)(x-1)}{x-1}=x+3$, so the limit is $4$.
**7.** $f(2)=\frac{0}{0}$ is **not defined**: the function has no value at 2. But for $x\neq2$, $f(x)=x+2$, so values of $x$ near 2 give $f(x)$ near 4: $\lim_{x\to2}f(x)=4$. The graph is the line $y=x+2$ with a hole at $(2,4)$.
**8.** The gap is $\frac{1}{n+1}$. We need $\frac{1}{n+1}<\frac{1}{1000}$, so $n+1>1000$ and $n>999$. From the **1000th term** onwards.
**9.** $\lim_{n\to\infty}\frac{3}{n}=0$.
**10.** Each side equals the radius, so the perimeter is $6\times5=30$ cm. The perimeters approach the circumference $2\pi\times5=10\pi\approx31.42$ cm.
:::

**Group C — Long answer (4 marks each)**

1. For $t_n=\frac{n}{n+1}$: (i) write the first six terms as decimals correct to 3 places; (ii) find the gap $1-t_n$ for $n=9$, 99 and 999; (iii) state the limit; (iv) explain whether any term equals the limit. <span class="marks">[4]</span>
2. A square of area 1 is shaded in steps: half of it, then half of what is left white, and so on. (i) Write the shaded areas after 1, 2, 3, 4 and 5 steps. (ii) Write the white area after $n$ steps. (iii) State the limit of the shaded area. (iv) After how many steps is the white area first less than 0.01? <span class="marks">[4]</span>
3. Let $f(x)=\frac{x^2-5x+6}{x-2}$. (i) Show that $f(2)$ is not defined. (ii) Make a table of $f(x)$ for $x=1.9, 1.99, 1.999, 2.001, 2.01, 2.1$. (iii) Find $\lim_{x\to2}f(x)$ by factorising. (iv) Describe the graph of $f$. <span class="marks">[4]</span>
4. A car park charges Rs 20 for up to and including 2 hours and Rs 40 for more than 2 hours, up to 4 hours. Let $F(t)$ be the fee for $t$ hours. (i) Find $F(1.5)$, $F(2)$ and $F(2.5)$. (ii) What does $F(t)$ approach as $t\rightarrow2^-$ and as $t\rightarrow2^+$? (iii) Does $\lim_{t\to2}F(t)$ exist? Give a reason. <span class="marks">[4]</span>
5. Evaluate: (i) $\lim_{x\to2}(x^3-2x+1)$ (ii) $\lim_{x\to5}\frac{x^2-25}{x-5}$ (iii) $\lim_{x\to-3}\frac{x^2+5x+6}{x+3}$ (iv) $\lim_{n\to\infty}\frac{3n+2}{n}$. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** (i) $0.5, 0.667, 0.75, 0.8, 0.833, 0.857$. (ii) $1-t_n=\frac{1}{n+1}$, giving $0.1$, $0.01$ and $0.001$. (iii) The gap tends to 0, so $\lim_{n\to\infty}\frac{n}{n+1}=1$. (iv) No term equals 1, because the gap $\frac{1}{n+1}$ is positive for every $n$. The limit is approached but never reached.
**2.** (i) $\frac{1}{2}, \frac{3}{4}, \frac{7}{8}, \frac{15}{16}, \frac{31}{32}$, that is $0.5, 0.75, 0.875, 0.9375, 0.96875$. (ii) White area $=\frac{1}{2^n}$. (iii) $\frac{1}{2^n}\rightarrow0$, so the shaded area $1-\frac{1}{2^n}\rightarrow1$. (iv) $\frac{1}{2^n}<\frac{1}{100}$ needs $2^n>100$; $2^6=64$ is too small and $2^7=128$ works, so after **7 steps**.
**3.** (i) $f(2)=\frac{4-10+6}{0}=\frac{0}{0}$, which is not defined. (ii) $-1.1, -1.01, -1.001, -0.999, -0.99, -0.9$. (iii) $x^2-5x+6=(x-2)(x-3)$, so for $x\neq2$, $f(x)=x-3$ and $\lim_{x\to2}f(x)=2-3=-1$, which agrees with the table. (iv) The graph is the straight line $y=x-3$ with a hole at the point $(2,-1)$.
**4.** (i) $F(1.5)=20$, $F(2)=20$ (up to and including 2 hours), $F(2.5)=40$. (ii) As $t\rightarrow2^-$, $F(t)\rightarrow20$; as $t\rightarrow2^+$, $F(t)\rightarrow40$. (iii) No. The left-hand and right-hand values approach different numbers, so there is no single number that $F(t)$ approaches; the limit does not exist, even though $F(2)=20$ exists.
**5.** (i) Substitute: $8-4+1=5$. (ii) $\frac{(x-5)(x+5)}{x-5}=x+5\rightarrow10$. (iii) $\frac{(x+2)(x+3)}{x+3}=x+2\rightarrow-3+2=-1$. (iv) $\frac{3n+2}{n}=3+\frac{2}{n}\rightarrow3$.
:::
