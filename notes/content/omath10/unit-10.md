---
subject: Optional Mathematics
grade: 10
unit: 10
title: Continuity
hours: 0
area: Units
---

A river flows without a break; the number of students in a class jumps from 40 to 41 with nothing in between. Mathematics calls the first kind of change **continuous** and the second **discontinuous**. To make this precise we need one idea: the **limit** of a function — the value that $f(x)$ gets closer and closer to as $x$ approaches a point. This chapter builds that idea from tables of values, uses it to test continuity at a point, and prepares you for the calculus you will meet in Grade 11.

::: key What the SEE asks from this chapter
Expect (i) the limit of a function from a table of values or by simple algebra; (ii) a graph of a function and a decision, with a reason, on whether it is continuous at a point; (iii) the test for a **piecewise** function: compare the **left-hand limit**, the **right-hand limit** and the value $f(a)$; (iv) the value of $k$ that makes a function continuous. The test is always three numbers: $\lim_{x\to a^-}f(x)$, $\lim_{x\to a^+}f(x)$ and $f(a)$.
:::

## 10.1 Limit of a function: left-hand and right-hand limits

### The idea of a limit

Inscribe a regular polygon in a circle. As the number of sides $n$ increases without end ($n\to\infty$), the polygon becomes more and more like the circle. We say the **limit** of the polygon is the circle.

For a function the idea is the same. Take $f(x)=x^2$ and let $x$ come close to $2$ from **below** and from **above**.

| $x$ (from the left) | $1.9$ | $1.99$ | $1.999$ | | $x$ (from the right) | $2.1$ | $2.01$ | $2.001$ |
|---|---|---|---|---|---|---|---|---|
| $f(x)=x^2$ | $3.61$ | $3.9601$ | $3.996001$ | | $f(x)=x^2$ | $4.41$ | $4.0401$ | $4.004001$ |

As $x$ approaches $2$ from the left (written $x\to2^-$), $f(x)$ approaches $4$. As $x$ approaches $2$ from the right ($x\to2^+$), $f(x)$ also approaches $4$.

::: definition Left-hand limit, right-hand limit and limit
- The **left-hand limit** $\displaystyle\lim_{x\to a^-}f(x)=L_1$ is the value $f(x)$ approaches as $x$ approaches $a$ through values **less** than $a$.
- The **right-hand limit** $\displaystyle\lim_{x\to a^+}f(x)=L_2$ is the value $f(x)$ approaches as $x$ approaches $a$ through values **greater** than $a$.
- The **limit** $\displaystyle\lim_{x\to a}f(x)=L$ **exists** only if $L_1=L_2=L$.
:::

::: key The limit does not need the value at the point
The limit describes what happens **near** $a$, not **at** $a$. The function may even be undefined at $a$, as in the next example. That is exactly why limits are useful.
:::

### A limit where the function is undefined

Let $f(x)=\dfrac{x^2-1}{x-1}$. At $x=1$ the function is $\dfrac00$, which has no value. Look at points near $1$:

| $x$ | $0.9$ | $0.99$ | $0.999$ | $1.001$ | $1.01$ | $1.1$ |
|---|---|---|---|---|---|---|
| $f(x)$ | $1.9$ | $1.99$ | $1.999$ | $2.001$ | $2.01$ | $2.1$ |

Both sides approach $2$, so $\displaystyle\lim_{x\to1}\dfrac{x^2-1}{x-1}=2$ even though $f(1)$ does not exist. The reason is visible after factorising: for $x\neq 1$,

$$ \frac{x^2-1}{x-1}=\frac{(x-1)(x+1)}{x-1}=x+1 $$

The graph is the straight line $y=x+1$ with a **hole** at $(1,2)$.

```figure caption="The graph of $f(x)=\dfrac{x^2-1}{x-1}$ is the line $y=x+1$ with a hole at $(1,2)$. The limit as $x\to1$ is 2, but $f(1)$ does not exist."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.2, 3.0))
x = np.linspace(-1, 3, 100)
ax.plot(x, x+1, color=ACCENT, lw=1.7)
ax.plot([1], [2], 'o', mfc='white', mec=ACCENT, ms=7, mew=1.6, zorder=5)
ax.annotate('', xy=(0.9, 1.9), xytext=(0.2, 1.2), arrowprops=dict(arrowstyle='->', color=SERIES[1], lw=1.2))
ax.annotate('', xy=(1.1, 2.1), xytext=(1.8, 2.8), arrowprops=dict(arrowstyle='->', color=SERIES[1], lw=1.2))
ax.text(1.12, 1.55, 'hole at (1, 2)', fontsize=8.5)
ax.text(0.0, 2.6, 'from the left', fontsize=8, color=SERIES[1])
ax.text(1.95, 2.55, 'from the right', fontsize=8, color=SERIES[1])
ax.axhline(0, color=MUTED, lw=0.7); ax.axvline(0, color=MUTED, lw=0.7)
ax.set_xlim(-1, 3.2); ax.set_ylim(-0.3, 4.2)
ax.grid(color=GRID, lw=0.5); ax.spines[['top','right']].set_visible(False)
fig.tight_layout(pad=0.4)
```

### Finding limits by algebra

Tables show the idea but take time. In an exam you may use these rules (the limit of a sum, difference, product and quotient is the sum, difference, product and quotient of the limits, provided the denominator's limit is not zero):

::: key Methods for $\displaystyle\lim_{x\to a}f(x)$
1. **Substitute** $x=a$. For a polynomial, or any expression that stays defined at $a$, this gives the limit.
2. If you get $\dfrac00$, **factorise** the numerator and denominator, cancel the common factor $(x-a)$, then substitute.
3. Check one-sided limits when the function is defined by different formulas on the two sides of $a$.
:::

::: example Limit by substitution
**Problem.** Find $\displaystyle\lim_{x\to2}(3x^2-5x+4)$.

**Solution.** The expression is a polynomial, so substitute: $3(4)-5(2)+4=12-10+4=6$.
:::

::: example Limit by factorising
**Problem.** Find $\displaystyle\lim_{x\to3}\dfrac{x^2-9}{x-3}$.

**Solution.** Substituting $x=3$ gives $\dfrac00$. Factorise: $\dfrac{x^2-9}{x-3}=\dfrac{(x-3)(x+3)}{x-3}=x+3$ for $x\neq 3$. Therefore

$$ \lim_{x\to3}\frac{x^2-9}{x-3}=3+3=6 $$

(Table check: $f(2.99)=5.99$ and $f(3.01)=6.01$.)
:::

::: example A harder factorisation
**Problem.** Find $\displaystyle\lim_{x\to2}\dfrac{x^2-5x+6}{x-2}$.

**Solution.** $x^2-5x+6=(x-2)(x-3)$, so for $x\neq 2$ the fraction is $x-3$. The limit is $2-3=-1$.
:::

::: example One-sided limits of a piecewise function
**Problem.** Let $f(x)=3x+5$ for $x<1$ and $f(x)=9x-1$ for $x\geq 1$. Find $\displaystyle\lim_{x\to1^-}f(x)$ and $\displaystyle\lim_{x\to1^+}f(x)$.

**Solution.** For $x$ just below $1$ the formula is $3x+5$: the left-hand limit is $3(1)+5=8$.

For $x$ just above $1$ the formula is $9x-1$: the right-hand limit is $9(1)-1=8$.

Both are $8$, so $\displaystyle\lim_{x\to1}f(x)=8$.
:::

::: caution Do not cancel without factorising
In $\dfrac{x^2-9}{x-3}$ you may cancel $(x-3)$ only **after** writing $x^2-9=(x-3)(x+3)$. Also, $\dfrac00$ does **not** mean the limit is $0$ or "does not exist": it means more work is needed.
:::

## 10.2 Continuity and discontinuity on the number line and in graphs

### On the number line

Think of a line with no gaps. Between **any** two real numbers there is another real number, so the set of **real numbers $\mathbb{R}$** is continuous. Other familiar sets are not.

| Set | Is there always an element between two elements? | Continuous? |
|---|---|---|
| Natural numbers $\{1,2,3,\dots\}$ | No — nothing between $4$ and $5$ | No |
| Whole numbers $\{0,1,2,\dots\}$ | No | No |
| Integers | No — nothing between $-2$ and $-1$ | No |
| Rational numbers (fractions) | Yes, but irrational numbers such as $\sqrt{2}$ are missing | No (has gaps) |
| Irrational numbers | Rational numbers are missing between them | No |
| **Real numbers** | **Yes — no gaps** | **Yes** |

The same difference appears in everyday life: the height of a plant, the weight of a person, or the water level of a river changes **continuously** (it takes every value in between); the number of students present or the number of goals scored changes in **steps**, with nothing in between.

```figure caption="Top: the natural numbers are separate points with gaps. Bottom: the real numbers fill the whole line with no gaps."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6, 2.2))
ax.plot([0, 8], [1, 1], color=MUTED, lw=0.8)
ax.plot(range(1, 8), [1]*7, 'o', color=ACCENT, ms=6)
ax.text(0, 1.28, 'Natural numbers: separate points', fontsize=8.5)
for k in range(1, 8):
    ax.text(k, 0.7, str(k), fontsize=8, ha='center')
ax.plot([0.2, 7.8], [-0.5, -0.5], color=ACCENT, lw=3)
ax.text(0, -0.2, 'Real numbers: no gaps', fontsize=8.5)
ax.text(0.2, -0.9, '−∞ ← … → +∞', fontsize=8, color=MUTED)
ax.set_xlim(-0.3, 8.2); ax.set_ylim(-1.1, 1.7); ax.axis('off')
fig.tight_layout(pad=0.3)
```

### In graphs

Look at the graph of a function around a point $x=c$.

::: definition Continuous at a point (graph description)
A function is **continuous at $x=c$** if its graph has no **break, jump, gap or hole** at $x=c$ — you could draw through that point without lifting your pencil. Otherwise it is **discontinuous** at $x=c$.
:::

```figure caption="Four graphs near $x=0$. (a) continuous; (b) a hole: $f(0)$ is missing; (c) a jump: the two sides do not meet; (d) a break to infinity, as in $1/x$. (b), (c) and (d) are discontinuous at $x=0$."
import numpy as np, matplotlib.pyplot as plt
fig, axs = plt.subplots(1, 4, figsize=(5.0, 2.2))
x1 = np.linspace(-2, 2, 100)
axs[0].plot(x1, x1**2*0.6+0.4, color=ACCENT, lw=1.6); axs[0].set_title('(a) continuous', fontsize=7.5)
x2 = np.linspace(-2, 2, 100); x2 = x2[np.abs(x2) > 0.03]
axs[1].plot(x2, 0.5*x2+1, color=ACCENT, lw=1.6)
axs[1].plot([0], [1], 'o', mfc='white', mec=ACCENT, ms=5, mew=1.4); axs[1].set_title('(b) hole', fontsize=7.5)
xl = np.linspace(-2, 0, 50); xr = np.linspace(0, 2, 50)
axs[2].plot(xl, 0.5*xl+0.8, color=ACCENT, lw=1.6)
axs[2].plot([0], [0.8], 'o', mfc='white', mec=ACCENT, ms=5, mew=1.4)
axs[2].plot(xr, 0.5*xr+2, color=ACCENT, lw=1.6)
axs[2].plot([0], [2], 'o', color=ACCENT, ms=5); axs[2].set_title('(c) jump', fontsize=7.5)
xa = np.linspace(-2, -0.25, 60); xb = np.linspace(0.25, 2, 60)
axs[3].plot(xa, 1/xa, color=ACCENT, lw=1.6); axs[3].plot(xb, 1/xb, color=ACCENT, lw=1.6)
axs[3].set_ylim(-4, 4); axs[3].set_title('(d) break', fontsize=7.5)
for a in axs:
    a.axhline(0, color=MUTED, lw=0.6); a.axvline(0, color=MUTED, lw=0.6)
    a.set_xticks([]); a.set_yticks([]); a.spines[:].set_visible(False)
axs[0].set_ylim(-0.5, 3); axs[1].set_ylim(-0.5, 3); axs[2].set_ylim(-0.5, 3.2)
fig.tight_layout(pad=0.3)
```

::: example Reading continuity from a graph
**Problem.** The graph of $y=\sin x$ is drawn for $-180^\circ<x<360^\circ$. Is it continuous at $x=-90^\circ$ and at $x=180^\circ$?

**Solution.** The sine graph is one smooth curve with no break, jump, gap or hole anywhere in this interval. It can be drawn without lifting the pencil, so it is continuous at $x=-90^\circ$ (where $\sin x=-1$) and at $x=180^\circ$ (where $\sin x=0$).
:::

::: example Straight lines with a gap
**Problem.** Draw the graph of $f(x)=x$ for $-3\leq  x<0$ and $f(x)=x+2$ for $0\leq  x\leq 3$ and decide whether it is continuous at $x=0$.

**Solution.** The left part ends at $(0,0)$ — but that point is **not** drawn from the right side. The right part starts at $(0,2)$. The two pieces do not meet: there is a **jump** from $0$ to $2$. Hence $f$ is **discontinuous** at $x=0$.
:::

## 10.3 Continuity of a function at a point

Graphs show the idea, but exams want numbers. Put the three observations together.

::: key Test for continuity at $x=a$
A function $f$ is **continuous at $x=a$** if all three hold:

1. $f(a)$ is **defined**;
2. $\displaystyle\lim_{x\to a^-}f(x)$ and $\displaystyle\lim_{x\to a^+}f(x)$ **exist and are equal**;
3. this common limit **equals** $f(a)$.

$$ \lim_{x\to a^-}f(x)=\lim_{x\to a^+}f(x)=f(a) $$

If any one fails, $f$ is **discontinuous** at $a$.
:::

Polynomials ($3x+2$, $x^2-4x+1$, …) are continuous at every real number, because the limit is always found by substitution. Trouble appears only for **piecewise functions** (different formulas on the two sides of $a$) and for **fractions** whose denominator is zero at $a$.

::: example Piecewise function: continuous
**Problem.** Examine the continuity of $f(x)=3x+5$ for $x<1$, $f(x)=9x-1$ for $x\geq 1$ at $x=1$.

**Solution.** $f(1)=9(1)-1=8$ (the formula for $x\geq 1$ applies at $x=1$).

Left-hand limit: $\displaystyle\lim_{x\to1^-}(3x+5)=8$. Right-hand limit: $\displaystyle\lim_{x\to1^+}(9x-1)=8$.

$\lim_{x\to1^-}f(x)=\lim_{x\to1^+}f(x)=f(1)=8$, so $f$ is **continuous** at $x=1$.
:::

::: example Piecewise function: a jump
**Problem.** Examine the continuity of $f(x)=x+3$ for $x<1$ and $f(x)=2x$ for $x\geq 1$ at $x=1$.

**Solution.** $f(1)=2(1)=2$.

Left-hand limit: $\displaystyle\lim_{x\to1^-}(x+3)=4$. Right-hand limit: $\displaystyle\lim_{x\to1^+}2x=2$.

The two limits are different ($4\neq 2$), so the limit does not exist and $f$ is **discontinuous** at $x=1$ (a jump of $2$).
:::

```figure caption="Left: $f(x)=3x+5$ ($x<1$), $9x-1$ ($x\geq 1$) is continuous at $x=1$ — the pieces meet at $(1,8)$. Right: $f(x)=x+3$ ($x<1$), $2x$ ($x\geq 1$) jumps from 4 to 2."
import numpy as np, matplotlib.pyplot as plt
fig, (a1, a2) = plt.subplots(1, 2, figsize=(5.0, 2.5))
xl = np.linspace(0, 1, 30); xr = np.linspace(1, 1.6, 30)
a1.plot(xl, 3*xl+5, color=ACCENT, lw=1.7); a1.plot(xr, 9*xr-1, color=ACCENT, lw=1.7)
a1.plot([1], [8], 'o', color=INK, ms=5); a1.text(0.2, 11.2, 'continuous at x = 1', fontsize=8)
a1.text(1.03, 7.0, '(1, 8)', fontsize=8)
a1.set_xlim(0, 1.7); a1.set_ylim(4, 14)
xl = np.linspace(0, 1, 30); xr = np.linspace(1, 2, 30)
a2.plot(xl, xl+3, color=ACCENT, lw=1.7); a2.plot(xr, 2*xr, color=ACCENT, lw=1.7)
a2.plot([1], [4], 'o', mfc='white', mec=ACCENT, ms=6, mew=1.5); a2.plot([1], [2], 'o', color=ACCENT, ms=6)
a2.plot([1, 1], [2, 4], color=SERIES[1], lw=1, ls='--')
a2.text(0.05, 5.3, 'jump at x = 1', fontsize=8)
a2.text(1.07, 3.0, '4 → 2', fontsize=8, color=SERIES[1])
a2.set_xlim(0, 2.1); a2.set_ylim(0, 6)
for a in (a1, a2):
    a.grid(color=GRID, lw=0.5); a.spines[['top', 'right']].set_visible(False)
fig.tight_layout(pad=0.4)
```

::: example A hole: limit exists but the value is wrong
**Problem.** $f(x)=\dfrac{x^2-4}{x-2}$ for $x\neq 2$ and $f(2)=3$. Is $f$ continuous at $x=2$?

**Solution.** For $x\neq 2$, $f(x)=\dfrac{(x-2)(x+2)}{x-2}=x+2$, so both one-sided limits at $2$ equal $4$.

But $f(2)=3\neq 4$. The limit is not equal to the value, so $f$ is **discontinuous** at $x=2$.

*If we redefine $f(2)=4$* the function becomes continuous: this kind of discontinuity can be "repaired".
:::

::: example A function undefined at the point
**Problem.** Is $f(x)=\dfrac{x^2-1}{x-1}$ continuous at $x=1$? At $x=2$?

**Solution.** At $x=1$: $f(1)=\dfrac00$ is **undefined**, so condition 1 fails. $f$ is discontinuous at $x=1$ (the limit is $2$ but there is no value).

At $x=2$: $f(2)=\dfrac{4-1}{2-1}=3$; $\lim_{x\to2^-}f(x)=\lim_{x\to2^+}f(x)=2+1=3$. All three agree, so $f$ is **continuous** at $x=2$.
:::

::: example Finding $k$ for continuity
**Problem.** Find $k$ so that $f(x)=3x+k$ for $x<2$ and $f(x)=x^2+1$ for $x\geq 2$ is continuous at $x=2$.

**Solution.** $f(2)=4+1=5$. Right-hand limit $=5$. Left-hand limit $=3(2)+k=6+k$.

Continuity needs $6+k=5$, so $k=-1$.
:::

::: example Value that fills the hole
**Problem.** Find $k$ if $f(x)=\dfrac{x^2-9}{x-3}$ for $x\neq 3$ and $f(3)=k$ is continuous at $x=3$.

**Solution.** For $x\neq 3$, $f(x)=x+3$, so $\lim_{x\to3}f(x)=6$. Continuity needs $f(3)=6$, so $k=6$.
:::

::: example Another piecewise check
**Problem.** $f(x)=x$ for $x<0$, $f(0)=0$ and $f(x)=x^2$ for $x>0$. Is $f$ continuous at $x=0$?

**Solution.** Left-hand limit $=0$, right-hand limit $=0^2=0$, $f(0)=0$. All three equal $0$: $f$ is **continuous** at $x=0$.
:::

::: example Division by zero
**Problem.** Is $f(x)=\dfrac{1}{x-2}$ continuous at $x=2$?

**Solution.** $f(2)=\dfrac10$ is undefined. Also, just left of $2$ the values are huge and negative ($f(1.99)=-100$), just right of $2$ they are huge and positive ($f(2.01)=100$). The one-sided limits do not approach a number, so $f$ is **discontinuous** at $x=2$ (a break). It is continuous at every other real number.
:::

::: tip The examiner is looking for
Three separate lines: left-hand limit, right-hand limit, value of the function. Then a comparison and a conclusion in words: "Since $\lim_{x\to a^-}f(x)=\lim_{x\to a^+}f(x)=f(a)$, $f$ is continuous at $x=a$." For a table question, show at least two values on each side.
:::

## 10.4 Exercises of the SEE type

### Method for any question

1. **Limit:** substitute; if $\dfrac00$, factorise and cancel; if the formula changes at the point, find left and right limits separately.
2. **Continuity at $x=a$:** find $f(a)$; find the left-hand limit with the formula for $x<a$; find the right-hand limit with the formula for $x>a$.
3. Compare the three values and state the conclusion.
4. **Find $k$:** set the left limit, right limit and $f(a)$ equal and solve.
5. From a graph: look for a break, jump, gap or hole.

## Chapter summary

- $\displaystyle\lim_{x\to a^-}f(x)$ is the left-hand limit; $\displaystyle\lim_{x\to a^+}f(x)$ the right-hand limit. The limit exists only if they are equal.
- The limit depends on values **near** $a$, not on $f(a)$ itself.
- To find a limit: substitute; if $\dfrac00$, factorise and cancel.
- The real number line is continuous (no gaps); natural numbers, integers and rational numbers are not.
- A graph is continuous at $x=c$ if it has no break, jump, gap or hole there.
- $f$ is continuous at $x=a$ if $\lim_{x\to a^-}f(x)=\lim_{x\to a^+}f(x)=f(a)$.
- Polynomials are continuous everywhere; piecewise functions and fractions need checking at the joining point or where the denominator is zero.
- To find $k$: equate the left limit, right limit and $f(a)$.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. $\displaystyle\lim_{x\to2}(x+5)$ is <span class="marks">[1]</span>
   (a) $2$ (b) $5$ (c) $7$ (d) $10$
2. The set that is continuous on the number line is <span class="marks">[1]</span>
   (a) natural numbers (b) integers (c) rational numbers (d) real numbers
3. $f$ is continuous at $x=a$ if <span class="marks">[1]</span>
   (a) $f(a)$ exists (b) $\lim_{x\to a}f(x)$ exists (c) $\lim_{x\to a^-}f(x)=\lim_{x\to a^+}f(x)=f(a)$ (d) $f(a)=0$
4. $\displaystyle\lim_{x\to4}\dfrac{x^2-16}{x-4}=$ <span class="marks">[1]</span>
   (a) $0$ (b) $4$ (c) $8$ (d) does not exist
5. A graph with a "jump" at $x=c$ is <span class="marks">[1]</span>
   (a) continuous (b) discontinuous (c) a straight line (d) always zero

::: note Answers to Group A
**1.** (c) — substitute: $2+5=7$.
**2.** (d) — only the real line has no gaps.
**3.** (c) — all three conditions are needed.
**4.** (c) — $\frac{(x-4)(x+4)}{x-4}=x+4\to8$.
**5.** (b) — a jump is a break in the graph.
:::

**Group B — Short answer (2 marks each)**

1. If $f(x)=3x+2$, find $f(2.001)$ and $f(1.999)$ and write $\lim_{x\to2}f(x)$. <span class="marks">[2]</span>
2. Find $\displaystyle\lim_{x\to5}\dfrac{x^2-25}{x-5}$. <span class="marks">[2]</span>
3. Name one example each of continuous and discontinuous change from daily life. <span class="marks">[2]</span>
4. Is $f(x)=x^2+1$ continuous at $x=3$? Give a reason. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** $f(2.001)=8.003$, $f(1.999)=7.997$; both approach $8$, so $\lim_{x\to2}f(x)=8$.
**2.** $\frac{(x-5)(x+5)}{x-5}=x+5\to10$.
**3.** Continuous: the height of a growing plant. Discontinuous: the number of students present (changes in whole-number steps).
**4.** Yes — it is a polynomial; left limit $=$ right limit $=f(3)=10$.
:::

**Group C — Short answer (3 marks each)**

1. Examine the continuity of $f(x)=2x+1$ for $x<2$ and $f(x)=x+3$ for $x\geq 2$ at $x=2$. <span class="marks">[3]</span>
2. Find $k$ if $f(x)=kx+3$ for $x<1$ and $f(x)=5-x$ for $x\geq 1$ is continuous at $x=1$. <span class="marks">[3]</span>
3. Find $\displaystyle\lim_{x\to-2}\dfrac{x^2+5x+6}{x+2}$. <span class="marks">[3]</span>
4. For $f(x)=\dfrac{x^2-1}{x-1}$ ($x\neq 1$), $f(1)=3$, test continuity at $x=1$. <span class="marks">[3]</span>

::: note Answers to Group C
**1.** $f(2)=2+3=5$. Left limit $=2(2)+1=5$. Right limit $=2+3=5$. All equal $5$: continuous at $x=2$.
**2.** $f(1)=5-1=4$; right limit $=4$; left limit $=k+3$. So $k+3=4$, $k=1$.
**3.** $x^2+5x+6=(x+2)(x+3)$; the fraction is $x+3$ for $x\neq -2$; limit $=-2+3=1$.
**4.** For $x\neq 1$, $f(x)=x+1$, so both limits are $2$; but $f(1)=3\neq 2$. Discontinuous at $x=1$.
:::

**Group D — Long answer (4 marks each)**

1. Examine the continuity of $f(x)=x^2$ for $x<0$, $f(0)=1$ and $f(x)=2x$ for $x>0$ at $x=0$, giving a reason. <span class="marks">[4]</span>
2. Find the values of $\displaystyle\lim_{x\to3^-}f(x)$ and $\displaystyle\lim_{x\to3^+}f(x)$ for $f(x)=\dfrac{x^2-9}{x-3}$ (using $x=2.99$, $2.999$, $3.01$, $3.001$) and decide whether $f$ is continuous at $x=3$. <span class="marks">[4]</span>
3. Find $k$ so that $f(x)=\dfrac{x^2-x-6}{x-3}$ for $x\neq 3$ and $f(3)=k$ is continuous at $x=3$. Then state whether $f$ is continuous at $x=-1$. <span class="marks">[4]</span>
4. A taxi charges Rs 50 for the first kilometre and Rs 30 for each further kilometre or part of a kilometre. Draw the graph for $0<x\leq 4$ of $f(x)=50$ for $0<x\leq 1$, $80$ for $1<x\leq 2$, $110$ for $2<x\leq 3$, $140$ for $3<x\leq 4$ and state where it is discontinuous. <span class="marks">[4]</span>

::: note Answers to Group D
**1.** Left limit $=0^2=0$. Right limit $=2(0)=0$. But $f(0)=1\neq 0$. The limit exists (equal to $0$) but differs from $f(0)$, so $f$ is discontinuous at $x=0$.
**2.** $f(2.99)=5.99$, $f(2.999)=5.999$ so the left limit is $6$; $f(3.01)=6.01$, $f(3.001)=6.001$ so the right limit is $6$. But $f(3)=\frac00$ is undefined, so $f$ is **not continuous** at $x=3$.
**3.** $x^2-x-6=(x-3)(x+2)$, so $f(x)=x+2$ for $x\neq 3$ and the limit at $3$ is $5$. Continuity needs $k=5$. At $x=-1$: $f(-1)=1$ and both limits are $1$, so $f$ is continuous at $x=-1$.
**4.** The graph is a staircase of four horizontal segments. At $x=1$: left value $50$, right limit $80$ (jump of $30$); at $x=2$: jump from $80$ to $110$; at $x=3$: jump from $110$ to $140$. It is discontinuous at $x=1$, $2$ and $3$ and continuous elsewhere.
:::

