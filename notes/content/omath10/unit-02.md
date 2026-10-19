---
subject: Optional Mathematics
grade: 10
unit: 2
title: Quadratic Equations and Graphs
hours: 0
area: Units
---

When a ball is thrown upward, a bridge cable hangs between two towers, or a farmer fences a rectangular field of fixed area, the mathematics behind the situation is a **quadratic**. A quadratic equation $ax^2+bx+c=0$ can be solved by factorisation or by a formula; its discriminant tells us in advance whether real solutions exist; and its graph, the **parabola**, shows the solutions as the points where the curve meets the $x$-axis. In this chapter we revise and extend these ideas, draw graphs of quadratic and cubic functions, and then solve a quadratic and a linear equation together, both by algebra and from a graph.

::: key What the SEE asks from this chapter
Typical questions are: (i) solve a quadratic equation by factorisation or by the formula; (ii) a word problem that leads to a quadratic equation; (iii) find the vertex, axis and intercepts of $y=ax^2+bx+c$ and **draw its graph** from a table; (iv) read the roots or the minimum/maximum value from a graph; (v) draw a cubic graph from a table; (vi) solve a quadratic and a linear equation, and find where a line meets a parabola. Always give a table of values and plot at least five points when asked to draw a graph.
:::

```photo id="omath10/golden-gate" caption="The cables of the Golden Gate Bridge hang in a curve very close to a parabola. The graph of a quadratic equation is an exact parabola, with one turning point and an axis of symmetry." width="100"
```

## 2.1 Quadratic equations: roots and their nature

::: definition Quadratic equation
An equation that can be written in the form $ax^2+bx+c=0$, where $a,\,b,\,c$ are real numbers and $a\neq 0$, is called a **quadratic equation** in $x$. The values of $x$ that satisfy it are its **roots** (or solutions).
:::

### Solving by factorisation

Split the middle term so that the expression becomes a product of two brackets. Then use the rule: if $PQ=0$, then $P=0$ or $Q=0$.

::: example Solving by factorisation
**Problem.** Solve (i) $x^2-5x+6=0$, (ii) $2x^2+5x-3=0$.

**Solution.** (i) $x^2-5x+6=x^2-2x-3x+6=x(x-2)-3(x-2)=(x-2)(x-3)$. So $x-2=0$ or $x-3=0$, giving $x=2$ or $x=3$.

(ii) We need two numbers with product $2\times(-3)=-6$ and sum $5$: these are $6$ and $-1$.
$$ 2x^2+6x-x-3=2x(x+3)-1(x+3)=(x+3)(2x-1) $$
So $x=-3$ or $x=\frac{1}{2}$.
:::

### Solving by the formula

When the expression does not factorise easily, use the quadratic formula. We first prove it by **completing the square**.

::: derivation Quadratic formula
We start from $ax^2+bx+c=0$ $(a\neq 0)$ and are heading for $x$ in terms of $a$, $b$, $c$.

**Step 1 — divide by $a$ so that the coefficient of $x^2$ is 1.**
$$ x^2+\frac{b}{a}x+\frac{c}{a}=0 $$

**Step 2 — move the constant to the right.**
$$ x^2+\frac{b}{a}x=-\frac{c}{a} $$

**Step 3 — add $\left(\frac{b}{2a}\right)^2$ to both sides.** This turns the left side into a perfect square:
$$ x^2+\frac{b}{a}x+\frac{b^2}{4a^2}=\frac{b^2}{4a^2}-\frac{c}{a} $$

**Step 4 — write the left side as a square and combine the right side.**
$$ \left(x+\frac{b}{2a}\right)^2=\frac{b^2-4ac}{4a^2} $$

**Step 5 — take the square root of both sides.**
$$ x+\frac{b}{2a}=\pm\frac{\sqrt{b^2-4ac}}{2a} $$

**Step 6 — move $\frac{b}{2a}$ to the right.**
$$ x=\frac{-b\pm\sqrt{b^2-4ac}}{2a} $$

**What it means.** Every quadratic equation has at most two roots, given by this one formula. The number under the root sign decides whether real roots exist.
:::

::: tip The examiner is looking for
(1) dividing by $a$, (2) adding $\left(\frac{b}{2a}\right)^2$ to **both** sides, (3) the perfect square on the left, (4) the $\pm$ sign in the final formula.
:::

::: key Quadratic formula and discriminant
$$ x=\frac{-b\pm\sqrt{D}}{2a},\qquad D=b^2-4ac $$

| Discriminant | Roots |
|---|---|
| $D>0$ | two real and different roots |
| $D=0$ | two real and equal roots, $x=-\frac{b}{2a}$ |
| $D<0$ | no real roots |

If $D$ is a perfect square (and $a,b,c$ are rational), the roots are rational.
:::

::: example Using the formula
**Problem.** Solve $x^2-4x-1=0$ and $2x^2-5x-3=0$ using the formula.

**Solution.** For $x^2-4x-1=0$: $a=1$, $b=-4$, $c=-1$. $D=16+4=20$.
$$ x=\frac{4\pm\sqrt{20}}{2}=\frac{4\pm 2\sqrt{5}}{2}=2\pm\sqrt{5} $$

For $2x^2-5x-3=0$: $a=2$, $b=-5$, $c=-3$. $D=25+24=49$.
$$ x=\frac{5\pm 7}{4}\;\Rightarrow\; x=3 \text{ or } x=-\frac{1}{2} $$
:::

::: example Equations that reduce to a quadratic
**Problem.** Solve (i) $\frac{x+1}{x-1}+\frac{x-1}{x+1}=\frac{5}{2}$, (ii) $x-\frac{3}{x}=2$.

**Solution.** (i) Multiply by the common denominator $2(x-1)(x+1)$:
$$ 2\left[(x+1)^2+(x-1)^2\right]=5(x^2-1) \;\Rightarrow\; 2(2x^2+2)=5x^2-5 \;\Rightarrow\; x^2=9 $$
So $x=\pm 3$. Neither makes a denominator zero, so both are valid.

(ii) Multiply by $x$ ($x\neq 0$): $x^2-3=2x$, so $x^2-2x-3=0$, $(x-3)(x+1)=0$ and $x=3$ or $x=-1$.
:::

### Nature of roots

::: example Finding an unknown from the nature of the roots
**Problem.** Find the values of $k$ for which $x^2+kx+9=0$ has equal roots. Find the nature of the roots of $3x^2-5x+2=0$.

**Solution.** For equal roots $D=0$: $k^2-4(1)(9)=0$, so $k^2=36$ and $k=\pm 6$.

For $3x^2-5x+2=0$: $D=25-24=1>0$ and $1$ is a perfect square, so the roots are **real, different and rational** ($x=1$ and $x=\frac{2}{3}$).
:::

### Sum and product of roots

If $\alpha$ and $\beta$ are the roots, the formula gives $\alpha+\beta=\frac{-b+\sqrt{D}}{2a}+\frac{-b-\sqrt{D}}{2a}=-\frac{b}{a}$ and $\alpha\beta=\frac{b^2-D}{4a^2}=\frac{4ac}{4a^2}=\frac{c}{a}$.

::: key Sum and product of roots
$$ \alpha+\beta=-\frac{b}{a},\qquad \alpha\beta=\frac{c}{a} $$
An equation with roots $\alpha,\beta$ is $x^2-(\alpha+\beta)x+\alpha\beta=0$.
:::

::: example Forming an equation
**Problem.** Find the sum and product of the roots of $3x^2+5x-2=0$. Form a quadratic equation whose roots are $3+\sqrt{2}$ and $3-\sqrt{2}$.

**Solution.** Sum $=-\frac{5}{3}$, product $=\frac{-2}{3}=-\frac{2}{3}$.

For the new equation: sum of roots $=(3+\sqrt{2})+(3-\sqrt{2})=6$; product $=3^2-(\sqrt{2})^2=9-2=7$. The equation is $x^2-6x+7=0$.
:::

::: caution Common mistakes
- Forgetting $a\neq 0$ and the $\pm$ sign, so only one root is found.
- Dividing both sides of $x^2=4x$ by $x$. This loses the root $x=0$. Write $x^2-4x=0$, $x(x-4)=0$.
- Writing the equation as $x^2+(\alpha+\beta)x+\alpha\beta=0$. The sign of the middle term is **minus**.
- Not checking roots in a word problem: a length or a number of children cannot be negative.
:::

::: example Completing the square and finding a missing coefficient
**Problem.** (i) Solve $x^2-6x+2=0$ by completing the square. (ii) One root of $2x^2+kx-6=0$ is 2. Find $k$ and the other root. (iii) The roots of $x^2-7x+k=0$ differ by 3. Find $k$.

**Solution.** (i) $x^2-6x=-2$. Add $\left(\frac{6}{2}\right)^2=9$ to both sides: $(x-3)^2=7$, so $x-3=\pm\sqrt{7}$ and $x=3\pm\sqrt{7}$.

(ii) Since 2 is a root: $2(4)+2k-6=0$, so $k=-1$. The equation is $2x^2-x-6=0$. The product of roots is $\frac{-6}{2}=-3$, so the other root is $\frac{-3}{2}=-\frac{3}{2}$. Check: $(2x+3)(x-2)=2x^2-x-6$ ✓.

(iii) Let the roots be $\alpha$ and $\alpha+3$. Sum: $2\alpha+3=7$, so $\alpha=2$ and the roots are 2 and 5. Product $=k=2\times 5=10$.
:::

::: example Equation with the variable in the denominator
**Problem.** Solve $x+\frac{1}{x}=\frac{5}{2}$.

**Solution.** Multiply by $2x$ ($x\neq 0$): $2x^2+2=5x$, so $2x^2-5x+2=0$ and $(2x-1)(x-2)=0$. Hence $x=\frac{1}{2}$ or $x=2$.
:::

::: example Word problems
**Problem.** (i) The product of two consecutive positive integers is 132. Find them. (ii) The length of a rectangle is 3 m more than its breadth and its area is 70 m². Find its length and breadth.

**Solution.** (i) Let the integers be $x$ and $x+1$: $x(x+1)=132$, so $x^2+x-132=0$, $(x+12)(x-11)=0$. Since $x>0$, $x=11$. The integers are **11 and 12**.

(ii) Let the breadth be $x$ m, so the length is $(x+3)$ m: $x(x+3)=70$, so $x^2+3x-70=0$, $(x+10)(x-7)=0$. A breadth cannot be negative, so $x=7$. Breadth **7 m**, length **10 m**.
:::

## 2.2 Graph of a quadratic function

The function $y=ax^2+bx+c$ $(a\neq 0)$ is a **quadratic function**. Its graph is a smooth U-shaped curve called a **parabola**.

::: key Features of the parabola $y=ax^2+bx+c$
- **Direction:** opens **upward** if $a>0$ (the vertex is a minimum); **downward** if $a<0$ (the vertex is a maximum).
- **Axis of symmetry:** the vertical line $x=-\frac{b}{2a}$.
- **Vertex:** $\left(-\frac{b}{2a},\ \frac{4ac-b^2}{4a}\right)$; find the $y$-value by substituting $x=-\frac{b}{2a}$ into the function.
- **$y$-intercept:** the point $(0,\,c)$.
- **$x$-intercepts:** the real roots of $ax^2+bx+c=0$. Two if $D>0$, one (the vertex touches the axis) if $D=0$, none if $D<0$.
- The larger $|a|$ is, the narrower the parabola.
:::

```figure caption="Graph of $y=x^2+2x-8$. The parabola opens upward ($a=1>0$), its axis is $x=-1$, vertex $(-1,-9)$, and it cuts the $x$-axis at $(-4,0)$ and $(2,0)$."
x = np.linspace(-5, 3, 200)
fig, ax = plt.subplots(figsize=(4.6, 3.3))
ax.plot(x, x**2 + 2*x - 8, color=ACCENT, lw=1.6)
ax.axvline(-1, color=MUTED, ls='--', lw=0.9)
ax.axhline(0, color=INK, lw=0.8)
ax.plot([-4, 2, -1, 0], [0, 0, -9, -8], 'o', color=SERIES[1], ms=4)
ax.text(-3.85, 1.4, '(-4, 0)', ha='left', fontsize=8)
ax.text(1.85, 1.4, '(2, 0)', ha='right', fontsize=8)
ax.text(-0.55, -10, 'vertex (-1, -9)', ha='left', va='center', fontsize=8)
ax.text(0.45, -8.3, '(0, -8)', ha='left', va='center', fontsize=8)
ax.text(-0.85, 5, 'axis x = -1', color=MUTED, ha='left', fontsize=8)
ax.set_xlim(-5.4, 3.8); ax.set_ylim(-11.2, 9)
ax.set_xlabel('x', fontsize=8.5); ax.set_ylabel('y', fontsize=8.5); ax.tick_params(labelsize=8)
ax.grid(color=GRID, lw=0.5); ax.spines[['top','right']].set_visible(False)
fig.tight_layout(pad=0.4)
```

### How to draw a parabola

1. Find the vertex $\left(-\frac{b}{2a},\,y\right)$ and the axis.
2. Make a table with the vertex in the **middle** and at least two $x$-values on each side.
3. Compute $y$ for each, plot the points and join them with a **smooth curve** (not straight segments).
4. Mark the axis, the vertex and the intercepts.

::: example Drawing $y=x^2+2x-8$
**Problem.** Draw the graph of $y=x^2+2x-8$. Write the equation of the axis and the vertex.

**Solution.** Here $a=1$, $b=2$, $c=-8$. Axis: $x=-\frac{2}{2}=-1$. At $x=-1$: $y=1-2-8=-9$. Vertex $(-1,-9)$.

| $x$ | $-4$ | $-3$ | $-2$ | $-1$ | $0$ | $1$ | $2$ |
|---|---|---|---|---|---|---|---|
| $y$ | $0$ | $-5$ | $-8$ | $-9$ | $-8$ | $-5$ | $0$ |

Plot the points and join them (Figure above). The roots of $x^2+2x-8=0$ are $x=-4$ and $x=2$, which are the $x$-intercepts; $y$-intercept is $-8$.
:::

::: example A downward parabola and its maximum value
**Problem.** For $y=-x^2+6x-5$ find the axis, the vertex, the $x$-intercepts and the maximum value of $y$.

**Solution.** $a=-1$, $b=6$, $c=-5$. Since $a<0$ the parabola opens downward and the vertex is a **maximum**.

Axis: $x=-\frac{6}{2(-1)}=3$. At $x=3$: $y=-9+18-5=4$. Vertex $(3,4)$; **maximum value $=4$**.

$x$-intercepts: $-x^2+6x-5=0\Rightarrow x^2-6x+5=0\Rightarrow(x-1)(x-5)=0$, so $x=1$ and $x=5$.
:::

```figure caption="Effect of the coefficient $a$ in $y=ax^2$. A larger positive $a$ makes the parabola narrower, a fraction makes it wider, and a negative $a$ turns it upside down."
x = np.linspace(-2, 2, 200)
fig, ax = plt.subplots(figsize=(4.4, 3.0))
for a_, c_, lb in [(2, SERIES[3], 'y = 2x²'), (1, ACCENT, 'y = x²'), (0.5, SERIES[2], 'y = 0.5x²'), (-1, SERIES[1], 'y = -x²')]:
    ax.plot(x, a_*x**2, color=c_, lw=1.5, label=lb)
ax.axhline(0, color=INK, lw=0.7); ax.axvline(0, color=INK, lw=0.7)
ax.set_xlim(-2.2, 2.2); ax.set_ylim(-5, 13)
ax.legend(fontsize=7.5, frameon=False, loc='upper center', ncol=2)
ax.tick_params(labelsize=8); ax.grid(color=GRID, lw=0.5)
ax.spines[['top','right']].set_visible(False)
fig.tight_layout(pad=0.4)
```

::: example The three possibilities for the $x$-intercepts
**Problem.** Without drawing, say how many times each parabola meets the $x$-axis: (i) $y=x^2-4x+4$, (ii) $y=x^2+2x+3$, (iii) $y=x^2-5x+6$.

**Solution.** Use $D=b^2-4ac$.

(i) $D=16-16=0$: the vertex $(2,0)$ **touches** the $x$-axis. One intercept.

(ii) $D=4-12=-8<0$: the parabola does not meet the axis. Its vertex is $(-1,2)$, above the axis, and it opens upward. No intercept.

(iii) $D=25-24=1>0$: two intercepts, $x=2$ and $x=3$.
:::

::: example Finding the equation from the intercepts
**Problem.** A parabola cuts the $x$-axis at $x=1$ and $x=3$ and passes through $(0,6)$. Find its equation and its vertex.

**Solution.** The roots are 1 and 3, so $y=a(x-1)(x-3)$. At $(0,6)$: $6=a(-1)(-3)=3a$, so $a=2$.

$$ y=2(x-1)(x-3)=2x^2-8x+6. $$

Axis: $x=\frac{1+3}{2}=2$. At $x=2$: $y=2(1)(-1)=-2$. Vertex $(2,-2)$.
:::

::: example Reading roots and minimum from the graph
**Problem.** From the graph of $y=x^2-2x-3$ find the roots of $x^2-2x-3=0$, the minimum value of $y$ and the range of $x$ for which $y<0$.

**Solution.** Axis $x=1$; at $x=1$, $y=1-2-3=-4$. Vertex $(1,-4)$.

| $x$ | $-2$ | $-1$ | $0$ | $1$ | $2$ | $3$ | $4$ |
|---|---|---|---|---|---|---|---|
| $y$ | $5$ | $0$ | $-3$ | $-4$ | $-3$ | $0$ | $5$ |

The curve cuts the $x$-axis at $x=-1$ and $x=3$, so the roots are $-1$ and $3$. The minimum value is $-4$. The curve lies below the $x$-axis for $-1<x<3$, so $y<0$ there.
:::

## 2.3 Graph of a cubic function

::: definition Cubic function
A function of the form $y=ax^3+bx^2+cx+d$, where $a\neq 0$, is a **cubic function**. Its graph has a smooth wavy shape and meets the $x$-axis at one, two or three points.
:::

The simplest cubics are $y=ax^3$. Because $(-x)^3=-x^3$, the graph is **symmetric about the origin**: if $(p,q)$ lies on it, so does $(-p,-q)$.

| $x$ | $-2$ | $-1$ | $0$ | $1$ | $2$ |
|---|---|---|---|---|---|
| $y=x^3$ | $-8$ | $-1$ | $0$ | $1$ | $8$ |
| $y=2x^3$ | $-16$ | $-2$ | $0$ | $2$ | $16$ |
| $y=-x^3$ | $8$ | $1$ | $0$ | $-1$ | $-8$ |

::: key Shape of $y=ax^3$
- If $a>0$ the curve rises from left to right, passing through the **3rd quadrant, the origin and the 1st quadrant**.
- If $a<0$ it falls from left to right, passing through the **2nd quadrant, the origin and the 4th quadrant**.
- A larger $|a|$ gives a steeper curve.
:::

```figure caption="Graphs of $y=x^3$, $y=2x^3$ and $y=-x^3$. All pass through the origin; the sign of $a$ decides whether the curve rises or falls."
x = np.linspace(-2, 2, 200)
fig, ax = plt.subplots(figsize=(4.4, 3.2))
ax.plot(x, x**3, color=ACCENT, lw=1.5, label='y = x³')
ax.plot(x, 2*x**3, color=SERIES[3], lw=1.5, label='y = 2x³')
ax.plot(x, -x**3, color=SERIES[1], lw=1.5, label='y = -x³')
ax.axhline(0, color=INK, lw=0.7); ax.axvline(0, color=INK, lw=0.7)
ax.set_xlim(-2.2, 2.2); ax.set_ylim(-10, 10)
ax.legend(fontsize=7.5, frameon=False, loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=3)
ax.tick_params(labelsize=8); ax.grid(color=GRID, lw=0.5)
ax.spines[['top','right']].set_visible(False)
fig.tight_layout(pad=0.4)
```

::: example Graph of a cubic with three roots
**Problem.** Draw the graph of $y=x^3-4x$ for $-3\leq x\leq 3$ and write its roots.

**Solution.** Factorise: $x^3-4x=x(x-2)(x+2)$, so $y=0$ at $x=-2,\ 0,\ 2$.

| $x$ | $-3$ | $-2$ | $-1$ | $0$ | $1$ | $2$ | $3$ |
|---|---|---|---|---|---|---|---|
| $y$ | $-15$ | $0$ | $3$ | $0$ | $-3$ | $0$ | $15$ |

The curve comes up from the 3rd quadrant, crosses the axis at $-2$, rises to a peak between $-2$ and $0$, falls through the origin to a trough between $0$ and $2$, crosses at $2$ and rises again. The graph meets the $x$-axis at three points, so $x^3-4x=0$ has three roots: $-2,\ 0,\ 2$.
:::

```figure caption="Graph of $y=x^3-4x$. It meets the $x$-axis at three points, $x=-2,\ 0,\ 2$."
x = np.linspace(-3, 3, 300)
fig, ax = plt.subplots(figsize=(4.4, 3.0))
ax.plot(x, x**3 - 4*x, color=ACCENT, lw=1.6)
ax.plot([-2, 0, 2], [0, 0, 0], 'o', color=SERIES[1], ms=4)
ax.plot([-3, -2, -1, 1, 2, 3], [-15, 0, 3, -3, 0, 15], '.', color=INK, ms=3)
ax.axhline(0, color=INK, lw=0.7); ax.axvline(0, color=INK, lw=0.7)
ax.text(-2.1, 3.5, '(-2, 0)', ha='right', fontsize=8)
ax.text(2.1, -3.5, '(2, 0)', ha='left', fontsize=8)
ax.text(0.2, 3.2, '(0, 0)', ha='left', fontsize=8)
ax.set_xlim(-3.4, 3.4); ax.set_ylim(-17, 17)
ax.set_xlabel('x', fontsize=8.5); ax.set_ylabel('y', fontsize=8.5); ax.tick_params(labelsize=8)
ax.grid(color=GRID, lw=0.5); ax.spines[['top','right']].set_visible(False)
fig.tight_layout(pad=0.4)
```

::: caution Common mistakes in graph drawing
- Joining the plotted points with straight lines. A parabola and a cubic are **smooth curves**.
- Choosing $x$-values only on one side of the vertex. The table should be centred on the axis of symmetry.
- Using different scales on the two axes without labelling them, or forgetting to label the axes and the curve.
- Drawing a cubic through the origin when $d\neq 0$. The $y$-intercept of $ax^3+bx^2+cx+d$ is $(0,d)$.
:::

## 2.4 Solving a quadratic and a linear equation together

Two equations, one quadratic and one linear, can have **two common solutions**, **one**, or **none**. Algebraically, substitute the linear expression into the quadratic and solve. Graphically, the solutions are the points where the **line cuts the parabola**.

::: example Solving by substitution
**Problem.** Solve $y=x^2-5x+6$ and $y=2$ simultaneously, and verify with the graph.

**Solution.** At a common point both $y$-values are equal:
$$ x^2-5x+6=2 \;\Rightarrow\; x^2-5x+4=0 \;\Rightarrow\; (x-1)(x-4)=0 $$
So $x=1$ or $x=4$, and $y=2$ in both. The solutions are $(1,2)$ and $(4,2)$.

Graph: the vertex of the parabola is at $x=\frac{5}{2}$, $y=\frac{25}{4}-\frac{25}{2}+6=-\frac{1}{4}$, so $\left(2.5,\,-0.25\right)$. The horizontal line $y=2$ lies above the vertex and cuts the parabola at two points.
:::

```figure caption="The parabola $y=x^2-5x+6$ and the line $y=2$ meet at $(1,2)$ and $(4,2)$, the solutions of $x^2-5x+4=0$."
x = np.linspace(-0.5, 5.5, 300)
fig, ax = plt.subplots(figsize=(4.6, 3.1))
ax.plot(x, x**2 - 5*x + 6, color=ACCENT, lw=1.6)
ax.axhline(2, color=SERIES[1], lw=1.3)
ax.axhline(0, color=INK, lw=0.7); ax.axvline(0, color=INK, lw=0.7)
ax.plot([1, 4], [2, 2], 'o', color=INK, ms=4)
ax.plot([2.5], [-0.25], 'o', color=SERIES[2], ms=4)
ax.text(0.9, 1.0, '(1, 2)', ha='right', fontsize=8)
ax.text(4.1, 1.0, '(4, 2)', ha='left', fontsize=8)
ax.text(2.5, -1.1, 'vertex (2.5, -0.25)', ha='center', fontsize=8)
ax.text(5.95, 1.3, 'y = 2', color=SERIES[1], ha='right', fontsize=8)
ax.set_xlim(-0.8, 6); ax.set_ylim(-2, 10)
ax.set_xlabel('x', fontsize=8.5); ax.set_ylabel('y', fontsize=8.5); ax.tick_params(labelsize=8)
ax.grid(color=GRID, lw=0.5); ax.spines[['top','right']].set_visible(False)
fig.tight_layout(pad=0.4)
```

::: key How many common points?
Substitute the line into the parabola to get a quadratic in $x$ and find its discriminant $D$.

| $D$ | Line and parabola |
|---|---|
| $D>0$ | meet at two points |
| $D=0$ | **touch** at one point (the line is a tangent) |
| $D<0$ | do not meet |
:::

::: example A line that meets the parabola
**Problem.** Find the common solutions of $y=x^2-4$ and $y=x-2$.

**Solution.** $x^2-4=x-2\Rightarrow x^2-x-2=0\Rightarrow(x-2)(x+1)=0$. If $x=2$ then $y=0$; if $x=-1$ then $y=-3$. Common points: $(2,0)$ and $(-1,-3)$.
:::

::: example When the line touches the parabola
**Problem.** For what value of $m$ does the line $y=2x+m$ touch the parabola $y=x^2+1$? Find the point of contact.

**Solution.** $x^2+1=2x+m\Rightarrow x^2-2x+(1-m)=0$. For one common point $D=0$: $(-2)^2-4(1)(1-m)=4m=0$, so $m=0$.

Then $x^2-2x+1=(x-1)^2=0$, $x=1$, $y=2$. The line $y=2x$ touches the parabola at $(1,2)$.
:::

::: example Quadratic and linear simultaneous equations
**Problem.** Solve (i) $x+y=7$, $xy=12$; (ii) $x^2+y^2=25$, $y=x+1$.

**Solution.** (i) $y=7-x$. Then $x(7-x)=12\Rightarrow x^2-7x+12=0\Rightarrow(x-3)(x-4)=0$. If $x=3$, $y=4$; if $x=4$, $y=3$. Solutions $(3,4)$ and $(4,3)$.

(ii) Put $y=x+1$: $x^2+(x+1)^2=25\Rightarrow 2x^2+2x-24=0\Rightarrow x^2+x-12=0\Rightarrow(x+4)(x-3)=0$. If $x=3$, $y=4$; if $x=-4$, $y=-3$. Solutions $(3,4)$ and $(-4,-3)$.
:::

::: example Solving an equation graphically using a parabola
**Problem.** Using the graph of $y=x^2$, solve $x^2-x-6=0$. Using the graph of $y=x^2-2x-3$, find approximate solutions of $x^2-2x-4=0$.

**Solution.** (i) Write $x^2=x+6$. Draw $y=x^2$ and the line $y=x+6$. They meet where $x^2=x+6$: at $(-2,4)$ and $(3,9)$. So $x=-2$ or $x=3$. Check: $x^2-x-6=(x-3)(x+2)$ ✓.

(ii) $x^2-2x-4=0$ means $x^2-2x-3=1$. On the graph of $y=x^2-2x-3$ draw the line $y=1$. It cuts the curve at two points, at $x\approx-1.2$ and $x\approx 3.2$. (By the formula, $x=1\pm\sqrt{5}\approx-1.24,\ 3.24$.)
:::

::: example Does the line meet the parabola?
**Problem.** Show that the line $y=-2$ does not meet the parabola $y=x^2+2x+3$, and that $y=3$ meets it at two points.

**Solution.** For $y=-2$: $x^2+2x+3=-2\Rightarrow x^2+2x+5=0$, $D=4-20=-16<0$. No real solution, so the line does not meet the parabola. (The minimum value of the parabola is 2, so it never goes below $y=2$.)

For $y=3$: $x^2+2x=0\Rightarrow x(x+2)=0$. The points are $(0,3)$ and $(-2,3)$.
:::

## 2.5 Exercises of the SEE type

::: example Fencing a field
**Problem.** A rectangular garden has perimeter 34 m and area 60 m². Find its length and breadth.

**Solution.** Let the length be $x$ m. Half the perimeter is 17 m, so the breadth is $(17-x)$ m.
$$ x(17-x)=60 \;\Rightarrow\; x^2-17x+60=0 \;\Rightarrow\; (x-5)(x-12)=0 $$
So $x=5$ or $12$. The sides are **12 m and 5 m**.
:::

::: example Consecutive odd integers
**Problem.** The product of two consecutive positive odd integers is 143. Find them.

**Solution.** Let them be $x$ and $x+2$: $x(x+2)=143\Rightarrow x^2+2x-143=0\Rightarrow(x+13)(x-11)=0$. Since $x>0$, $x=11$. The integers are **11 and 13**.
:::

::: example Maximum height
**Problem.** A ball thrown up from the ground reaches height $h=20t-5t^2$ metres after $t$ seconds. Find the greatest height and when the ball returns to the ground.

**Solution.** The graph of $h$ against $t$ is a parabola opening downward ($a=-5$). Axis $t=-\frac{20}{2(-5)}=2$ s. At $t=2$: $h=40-20=20$ m. The greatest height is **20 m**.

On the ground $h=0$: $20t-5t^2=5t(4-t)=0$, so $t=0$ or $t=4$. The ball lands after **4 s**.
:::

::: example Two numbers
**Problem.** The sum of two numbers is 15 and the sum of their squares is 117. Find the numbers.

**Solution.** Let the numbers be $x$ and $15-x$.
$$ x^2+(15-x)^2=117 \;\Rightarrow\; 2x^2-30x+225=117 \;\Rightarrow\; x^2-15x+54=0 $$
$(x-6)(x-9)=0$, so the numbers are **6 and 9**. Check: $36+81=117$ ✓.
:::

::: example Right-angled triangle
**Problem.** The hypotenuse of a right-angled triangle is 13 cm. The other two sides differ by 7 cm. Find them.

**Solution.** Let the sides be $x$ and $x+7$. By Pythagoras: $x^2+(x+7)^2=169\Rightarrow 2x^2+14x-120=0\Rightarrow x^2+7x-60=0\Rightarrow(x+12)(x-5)=0$. Since $x>0$, $x=5$. The sides are **5 cm and 12 cm**.
:::

::: example Boat in a river
**Problem.** A boat takes 5 hours to go 24 km upstream and 24 km back downstream. The speed of the current is 2 km/h. Find the speed of the boat in still water.

**Solution.** Let the speed in still water be $v$ km/h. Upstream speed is $v-2$, downstream speed $v+2$.
$$ \frac{24}{v-2}+\frac{24}{v+2}=5 \;\Rightarrow\; 24(v+2)+24(v-2)=5(v^2-4) \;\Rightarrow\; 48v=5v^2-20 $$
So $5v^2-48v-20=0$. $D=2304+400=2704=52^2$, so $v=\frac{48\pm52}{10}$, giving $v=10$ or $v=-0.4$. Speed cannot be negative, so the speed in still water is **10 km/h**.

Check: $\frac{24}{8}+\frac{24}{12}=3+2=5$ ✓.
:::

## Chapter summary

- **Quadratic formula:** $x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}$, $D=b^2-4ac$. $D>0$: two real different roots; $D=0$: equal roots; $D<0$: no real roots.
- **Sum and product:** $\alpha+\beta=-\frac{b}{a}$, $\alpha\beta=\frac{c}{a}$; equation $x^2-(\alpha+\beta)x+\alpha\beta=0$.
- **Parabola** $y=ax^2+bx+c$: axis $x=-\frac{b}{2a}$; vertex found by substituting; $y$-intercept $c$; $x$-intercepts are the roots; opens up if $a>0$ (minimum), down if $a<0$ (maximum).
- **Cubic** $y=ax^3$: rises through quadrants 3, 1 if $a>0$; falls through quadrants 2, 4 if $a<0$; symmetric about the origin.
- To draw a graph: table centred on the vertex, plot, smooth curve, label axes and intercepts.
- **Line and parabola:** substitute to get a quadratic in $x$; $D>0$ two points, $D=0$ tangent, $D<0$ none.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The roots of $x^2-7x+12=0$ are <span class="marks">[1]</span>
   (a) 2, 6 (b) 3, 4 (c) $-3$, $-4$ (d) 1, 12
2. The roots of $x^2-6x+9=0$ are <span class="marks">[1]</span>
   (a) real and equal (b) real and different (c) imaginary (d) irrational
3. The vertex of $y=x^2-4x+3$ is <span class="marks">[1]</span>
   (a) $(2,1)$ (b) $(-2,-1)$ (c) $(2,-1)$ (d) $(4,3)$
4. The graph of $y=-x^3$ passes through the <span class="marks">[1]</span>
   (a) 1st and 3rd quadrants (b) 2nd and 4th quadrants (c) 1st and 2nd quadrants (d) 3rd and 4th quadrants
5. The sum of the roots of $2x^2-8x+3=0$ is <span class="marks">[1]</span>
   (a) 4 (b) $-4$ (c) $\frac{3}{2}$ (d) $-\frac{3}{2}$
6. The number of points common to $y=x^2$ and $y=-1$ is <span class="marks">[1]</span>
   (a) 0 (b) 1 (c) 2 (d) 3

::: note Answers to Group A
**1.** (b) — $(x-3)(x-4)=0$.
**2.** (a) — $D=36-36=0$.
**3.** (c) — axis $x=2$, $y=4-8+3=-1$.
**4.** (b) — $a<0$, so the curve passes through quadrants 2 and 4.
**5.** (a) — $-\frac{b}{a}=\frac{8}{2}=4$.
**6.** (a) — $x^2=-1$ has no real solution.
:::

**Group B — Short answer (2 marks each)**

1. Solve $x^2-9x+14=0$. <span class="marks">[2]</span>
2. Find the discriminant of $3x^2-5x+2=0$ and state the nature of its roots. <span class="marks">[2]</span>
3. Find the vertex and the axis of symmetry of $y=x^2-6x+5$. <span class="marks">[2]</span>
4. Find the sum and the product of the roots of $3x^2+5x-2=0$. <span class="marks">[2]</span>
5. Find the $x$-intercepts and the $y$-intercept of $y=x^2-5x+6$. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** $(x-2)(x-7)=0$, so $x=2$ or $7$.
**2.** $D=25-24=1>0$: roots are real and different (and rational).
**3.** Axis $x=3$; $y=9-18+5=-4$. Vertex $(3,-4)$, axis $x=3$.
**4.** Sum $=-\frac{5}{3}$, product $=-\frac{2}{3}$.
**5.** $(x-2)(x-3)=0$: $x$-intercepts $(2,0)$ and $(3,0)$. $y$-intercept $(0,6)$.
:::

**Group C — Short answer (3 marks each)**

1. Solve $2x^2-5x-3=0$ using the quadratic formula. <span class="marks">[3]</span>
2. Find the values of $k$ for which $x^2+kx+16=0$ has equal roots. <span class="marks">[3]</span>
3. Draw the graph of $y=x^2-2x-3$ for $-2\leq x\leq 4$. From it find the roots of $x^2-2x-3=0$ and the minimum value of $y$. <span class="marks">[3]</span>
4. Solve $y=x^2-3x$ and $y=2x-6$ and write the common points. <span class="marks">[3]</span>
5. Form a quadratic equation whose roots are $3+\sqrt{2}$ and $3-\sqrt{2}$. <span class="marks">[3]</span>

::: note Answers to Group C
**1.** $a=2$, $b=-5$, $c=-3$, $D=25+24=49$. $x=\frac{5\pm7}{4}$, so $x=3$ or $x=-\frac{1}{2}$.
**2.** $D=k^2-64=0$, so $k=\pm 8$.
**3.** Table: $x=-2,-1,0,1,2,3,4$ gives $y=5,0,-3,-4,-3,0,5$. Vertex $(1,-4)$. Roots $x=-1$ and $x=3$. Minimum value of $y$ is $-4$.
**4.** $x^2-3x=2x-6\Rightarrow x^2-5x+6=0\Rightarrow x=2$ or $3$. $y=2x-6$ gives $y=-2$ and $y=0$. Common points $(2,-2)$ and $(3,0)$.
**5.** Sum $=6$, product $=9-2=7$. The equation is $x^2-6x+7=0$.
:::

**Group D — Long answer (4 marks each)**

1. The product of two consecutive positive odd integers is 143. Find them. <span class="marks">[4]</span>
2. Solve $\frac{x+1}{x-1}+\frac{x-1}{x+1}=\frac{5}{2}$. <span class="marks">[4]</span>
3. The perimeter of a rectangular field is 34 m and its area is 60 m². Find its length and breadth. <span class="marks">[4]</span>
4. Solve $x^2+y^2=25$ and $y=x-1$. <span class="marks">[4]</span>
5. For what value of $m$ does the line $y=2x+m$ touch the parabola $y=x^2+1$? Find the point of contact. <span class="marks">[4]</span>

::: note Answers to Group D
**1.** Let the integers be $x$ and $x+2$. $x^2+2x-143=0\Rightarrow(x+13)(x-11)=0$. $x=11$. The integers are 11 and 13.
**2.** $2[(x+1)^2+(x-1)^2]=5(x^2-1)\Rightarrow 4x^2+4=5x^2-5\Rightarrow x^2=9$, so $x=\pm 3$.
**3.** Let the length be $x$ m; breadth $17-x$. $x(17-x)=60\Rightarrow x^2-17x+60=0\Rightarrow(x-5)(x-12)=0$. Length 12 m, breadth 5 m.
**4.** $x^2+(x-1)^2=25\Rightarrow 2x^2-2x-24=0\Rightarrow x^2-x-12=0\Rightarrow(x-4)(x+3)=0$. If $x=4$, $y=3$; if $x=-3$, $y=-4$. Solutions $(4,3)$ and $(-3,-4)$.
**5.** $x^2+1=2x+m\Rightarrow x^2-2x+1-m=0$. $D=4-4(1-m)=4m=0$, so $m=0$. Then $(x-1)^2=0$, $x=1$, $y=2$. The point of contact is $(1,2)$.
:::


## Retrieval practice and investigation

::: key Work before reading the key
Answer these short retrieval questions without consulting the chapter. Explain the reason, not only the result. These are revision checks, not a prediction of the examination paper.
:::

**1.** Solve x² − 5x + 6 = 0.

**2.** For x² + 4x + 4 = 0, how many distinct real roots exist?

**3.** Does x² + 1 = 0 have a real root?

::: note Reasoned key
**1.** x = 2 or 3, since (x − 2)(x − 3) = 0. Check: 4 − 10 + 6 = 0 and 9 − 15 + 6 = 0.

**2.** One: the discriminant is 4² − 4 × 1 × 4 = 0, and the repeated root is −2.

**3.** No. Every real square is nonnegative, so x² + 1 is at least 1.

:::

::: tip Investigation — Test the roots against the graph
Make a value table for y = x² − 5x + 6 at integer x from 0 to 5. Plot it, mark both intercepts, and compare the graph with (x − 2)(x − 3). Explain why the turning point lies between the roots.

Submit a one-page record: your method, working or evidence, conclusion, and one limitation. Exchange it with a classmate and check the reasoning against the chapter.
:::
