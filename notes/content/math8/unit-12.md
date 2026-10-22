---
subject: Mathematics
grade: 8
unit: 12
title: Equation and Graph
hours: 0
area: Compulsory Mathematics
---

An equation is a balance: whatever you do to one side you must do to the other.
A graph is a picture of every pair of values that keeps the balance. Putting the
two together turns algebra into something you can see — the point where two
lines cross *is* the solution of the two equations, and an inequality is simply
a region of the graph rather than a line.

::: key What this chapter asks of you
You should be able to solve a linear equation in one variable, solve two
simultaneous linear equations, plot the graph of a linear equation from a table
of values, and show an inequality on a number line and read a solution from a
graph.
:::

## 12.1 Linear equations in one variable

A **linear equation** has the variable to the first power only. Solving means
isolating the variable by doing the same thing to both sides.

**Method.**

1. Clear any fractions by multiplying every term by the LCM of the denominators.
2. Remove brackets by multiplying out.
3. Collect all the variable terms on one side and all the constants on the
   other.
4. Divide by the coefficient of the variable.
5. Check by substituting back.

::: example With brackets
**Problem.** Solve $3(x-2)+5=2x+4$.

**Solution.** Expand the bracket:

$$3x-6+5=2x+4\;\Longrightarrow\;3x-1=2x+4$$

Subtract $2x$ from both sides and add 1:

$$x=5$$

**Answer.** $x=5$.

**Check.** Left side: $3(5-2)+5=9+5=14$. Right side: $2(5)+4=14$ ✓.
:::

::: example With fractions
**Problem.** Solve $\frac{2x-1}{3}=\frac{x+2}{2}$.

**Solution.** Multiply both sides by the LCM 6:

$$2(2x-1)=3(x+2)\;\Longrightarrow\;4x-2=3x+6\;\Longrightarrow\;x=8$$

**Answer.** $x=8$.

**Check.** Left: $\frac{16-1}{3}=5$. Right: $\frac{10}{2}=5$ ✓.
:::

## 12.2 Simultaneous linear equations

Two equations in two unknowns are **simultaneous**; the solution is the pair of
values that satisfies both at once.

### 12.2.1 The elimination method

Make the coefficients of one variable equal in size, then add or subtract the
equations to remove it.

::: example Elimination by adding
**Problem.** Solve $x+y=10$ and $x-y=4$.

**Solution.** The coefficients of $y$ are $+1$ and $-1$, so adding eliminates
$y$:

$$2x=14\;\Longrightarrow\;x=7$$

Substituting into $x+y=10$ gives $7+y=10$, so $y=3$.

**Answer.** $x=7$, $y=3$.

**Check.** $7+3=10$ ✓ and $7-3=4$ ✓.
:::

::: example Elimination by scaling
**Problem.** Solve $2x+3y=13$ and $3x-2y=0$.

**Solution.** **Step 1 — make the $x$ coefficients equal.** Multiply the first
equation by 3 and the second by 2:

$$6x+9y=39,\qquad 6x-4y=0$$

**Step 2 — subtract.**

$$(6x+9y)-(6x-4y)=39-0\;\Longrightarrow\;13y=39\;\Longrightarrow\;y=3$$

**Step 3 — substitute.** From $3x-2y=0$: $3x=6$, so $x=2$.

**Answer.** $x=2$, $y=3$.

**Check.** $2(2)+3(3)=4+9=13$ ✓ and $3(2)-2(3)=0$ ✓.
:::

### 12.2.2 The substitution method

Make one variable the subject of one equation and put it into the other.

::: example Substitution
**Problem.** Solve $y=2x+1$ and $3x+y=11$.

**Solution.** $y$ is already the subject, so substitute:

$$3x+(2x+1)=11\;\Longrightarrow\;5x=10\;\Longrightarrow\;x=2$$

Then $y=2(2)+1=5$.

**Answer.** $x=2$, $y=5$.

**Check.** $5=2(2)+1$ ✓ and $3(2)+5=11$ ✓.
:::

::: example A word problem
**Problem.** The sum of two numbers is 25 and their difference is 7. Find the
numbers.

**Solution.** Let the numbers be $x$ and $y$, with $x>y$. Then

$$x+y=25,\qquad x-y=7$$

Adding: $2x=32$, so $x=16$; then $y=25-16=9$.

**Answer.** 16 and 9.

**Check.** $16+9=25$ ✓ and $16-9=7$ ✓.
:::

::: caution The commonest slip in elimination
When you subtract one equation from another, every term of the subtracted
equation changes sign. From $6x+9y=39$ minus $6x-4y=0$ you get $13y=39$, but
only if the second equation is read as $-(6x-4y)=-6x+4y$. Writing
$9y-4y=5y$ is the classic error. Subtract in brackets, every time.
:::

## 12.3 The graph of a linear equation

An equation such as $y=2x+1$ has **infinitely many** solutions — one for each
value of $x$. Plotting them all gives a straight line, and two points are enough
to fix it (a third is a check).

**Method.**

1. Make a table of values, choosing convenient values of $x$ (often $-1$, 0, 1,
   2).
2. Plot the points on graph paper.
3. Join them with a straight line and label it with its equation.

```figure caption="The graph of y = 2x + 1. The line crosses the y-axis at 1 — the value when x is 0 — and rises 2 units for every 1 unit across, which is the coefficient of x."
import numpy as np
fig, ax = plt.subplots(figsize=(4.6, 2.9))
x = np.array([-2, -1, 0, 1, 2, 3])
y = 2 * x + 1
ax.plot(x, y, color=ACCENT, lw=1.7)
ax.plot(x, y, "o", color=INK, ms=3.6)
ax.axhline(0, color=INK, lw=0.8)
ax.axvline(0, color=INK, lw=0.8)
ax.annotate("(0, 1)", xy=(0, 1), xytext=(-1.1, 2.4), fontsize=8, color=INK, arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.8))
ax.plot([0, 1, 1], [1, 1, 3], color=SERIES[1], lw=1.2, ls="--")
ax.text(0.5, 0.35, "across 1", fontsize=8, color=SERIES[1], ha="center")
ax.text(1.12, 1.8, "rise 2", fontsize=8, color=SERIES[1])
ax.set_xlim(-2.4, 3.4)
ax.set_ylim(-4, 7.5)
ax.set_xlabel("x", fontsize=9)
ax.set_ylabel("y", fontsize=9)
ax.tick_params(labelsize=8, length=0)
ax.spines[["top", "right"]].set_visible(False)
ax.grid(True, color=GRID, lw=0.6)
ax.set_axisbelow(True)
fig.tight_layout()
```

| Table for $y=2x+1$ | | | | |
|---|---|---|---|---|
| $x$ | $-1$ | 0 | 1 | 2 |
| $y$ | $-1$ | 1 | 3 | 5 |

::: example Solving simultaneous equations graphically
**Problem.** Draw the graphs of $x+y=6$ and $y=x-2$ on the same axes and read
off the solution.

**Solution.** **Table for $x+y=6$, that is $y=6-x$:** when $x=0$, $y=6$; when
$x=2$, $y=4$; when $x=6$, $y=0$. **Table for $y=x-2$:** when $x=0$, $y=-2$;
when $x=2$, $y=0$; when $x=6$, $y=4$.

Plot both lines. They cross at $(4,2)$.

**Answer.** $x=4$, $y=2$.

**Check.** $4+2=6$ ✓ and $2=4-2$ ✓. At the crossing point both equations hold,
which is exactly what the solution means.
:::

```figure caption="Graphical solution of $x+y=6$ and $x-y=2$ (that is $y=x-2$). The lines meet at (4, 2), so $x=4$, $y=2$."
fig, ax = plt.subplots(figsize=(4.4, 3.2))
xs = np.array([-1, 7])
ax.plot(xs, 6 - xs, color=ACCENT, lw=1.6)
ax.plot(xs, xs - 2, color=SERIES[1], lw=1.6)
for (px, py) in [(0, 6), (2, 4), (6, 0)]:
    ax.plot(px, py, "o", color=ACCENT, ms=4)
for (px, py) in [(0, -2), (2, 0), (6, 4)]:
    ax.plot(px, py, "s", color=SERIES[1], ms=4)
ax.plot(4, 2, "o", color=INK, ms=6)
ax.annotate("(4, 2)", xy=(4, 2), xytext=(4.2, 2.9), fontsize=9, color=INK, bbox=dict(fc="white", ec="none", pad=1.5))
ax.text(0.3, 6.6, "x + y = 6", fontsize=9, color=ACCENT)
ax.text(5.0, 5.4, "x − y = 2", fontsize=9, color=SERIES[1])
ax.axhline(0, color=INK, lw=0.8); ax.axvline(0, color=INK, lw=0.8)
ax.set_xlim(-1, 7); ax.set_ylim(-3, 7.5)
ax.set_xticks(range(-1, 8)); ax.set_yticks(range(-3, 8))
ax.tick_params(labelsize=7.5, length=0)
ax.grid(True, color=GRID, lw=0.6); ax.set_axisbelow(True)
ax.spines[["top", "right"]].set_visible(False)
```

::: example A word problem solved graphically
**Problem.** A father's present age is 10 years more than twice his daughter's
age. The difference between their ages is 25 years. Find their ages by the
graphical method.

**Solution.** Let the father be $x$ years and the daughter $y$ years.
$x=2y+10$ … (i) and $x-y=25$ … (ii).

| From (i), $x=2y+10$ | | | |
|---|---|---|---|
| $y$ | 0 | 5 | 15 |
| $x$ | 10 | 20 | 40 |

| From (ii), $x=y+25$ | | | |
|---|---|---|---|
| $y$ | 0 | 5 | 15 |
| $x$ | 25 | 30 | 40 |

Plotting both lines, they meet at the point where $y=15$, $x=40$.

**Answer.** Father 40 years, daughter 15 years.
**Check.** $2\times15+10=40$ ✓ and $40-15=25$ ✓.
:::

::: tip The graph is a check, not a substitute
Drawing a graph takes five minutes and gives the answer only as accurately as
your paper allows. Use the elimination or substitution method to get the exact
answer, and draw the graph to confirm that the two lines really do meet at that
point. The examiner is looking for both.
:::

## 12.4 Inequality and its graph

An **inequality** compares two expressions with $<$, $>$, $\le$ or $\ge$. It is
solved exactly like an equation, with one important exception.

::: caution Multiplying by a negative reverses the sign
From $-2x>6$ the solution is $x<-3$, **not** $x>-3$. Dividing by $-2$ flips the
inequality sign. This does not happen when you add or subtract, only when you
multiply or divide by a negative number.
:::

**Drawing the solution on a number line.**

- For $x<3$, draw an open circle at 3 and shade to the left.
- For $x\le3$, draw a filled circle at 3 and shade to the left.
- For $x\ge-1$, draw a filled circle at $-1$ and shade to the right.

::: example Solving and graphing an inequality
**Problem.** Solve $3x-5\le7$ and show the solution on a number line.

**Solution.** Add 5 to both sides: $3x\le12$. Divide by 3 (positive, so the
sign does not change): $x\le4$.

On the number line, put a **filled** circle at 4 and shade everything to the
left, including 4.

**Check.** Try $x=4$: $3(4)-5=7\le7$ ✓ (allowed, because of the $\le$ sign).
Try $x=5$: $15-5=10>7$ ✗, correctly outside the shaded region.
:::

::: example An inequality with a negative coefficient
**Problem.** Solve $5-2x<11$ and graph the solution.

**Solution.** Subtract 5: $-2x<6$. Divide by $-2$, reversing the sign:
$x>-3$.

On the number line, put an open circle at $-3$ and shade to the right.

**Check.** Try $x=0$: $5-0=5<11$ ✓, and 0 is inside the region.
Try $x=-4$: $5+8=13<11$ is false ✗, correctly excluded.
:::

## 12.5 Quadratic equations by factorisation

An equation such as $x-4=0$ is **linear** (highest power of $x$ is 1). An
equation in one variable whose highest power is 2, written
$ax^2+bx+c=0$ with $a\ne0$, is a **quadratic equation**. It usually has two
solutions, called its **roots**.

**Key fact.** If the product of two factors is zero, at least one of them is
zero: if $pq=0$ then $p=0$ or $q=0$.

**Method.** Bring everything to one side ($=0$), factorise, set each factor
equal to zero and solve.

::: example Solving quadratics
**Problem.** Solve (a) $x^2-6x+8=0$ (b) $4x^2-25=0$ (c) $x^2-3x=0$.

**Solution.**
(a) $x^2-4x-2x+8=0$ → $x(x-4)-2(x-4)=0$ → $(x-4)(x-2)=0$.
Either $x-4=0$, so $x=4$; or $x-2=0$, so $x=2$. **Roots: 4 and 2.**

(b) $(2x)^2-5^2=0$ → $(2x+5)(2x-5)=0$.
Either $2x+5=0$, so $x=-\frac52$; or $2x-5=0$, so $x=\frac52$. **$x=\pm2\frac12$.**

(c) $x(x-3)=0$, so $x=0$ or $x=3$.

**Check (a).** $4^2-6(4)+8=16-24+8=0$ ✓ and $2^2-12+8=0$ ✓.
:::

::: caution Do not divide by $x$
In $x^2-3x=0$, dividing both sides by $x$ gives only $x=3$ and loses the root
$x=0$. Factorise instead.
:::

::: example Forming a quadratic from its roots
**Problem.** Find the quadratic equation whose roots are 2 and 3.

**Solution.** $x=2$ gives $x-2=0$ and $x=3$ gives $x-3=0$. So

$(x-2)(x-3)=0$ → $x^2-3x-2x+6=0$ → $x^2-5x+6=0$.
:::

## Chapter summary

- Two simultaneous equations are solved graphically by plotting both lines; the
  point where they cross gives $x$ and $y$.
- A quadratic equation $ax^2+bx+c=0$ is solved by factorising and putting each
  factor equal to zero; roots $p$, $q$ give $(x-p)(x-q)=0$.

- A linear equation is solved by clearing fractions, expanding brackets,
  collecting like terms and dividing by the coefficient.
- Simultaneous equations are solved by elimination (make one coefficient match,
  then add or subtract) or substitution (make one variable the subject).
- A linear equation has infinitely many solutions, and its graph is a straight
  line; two points fix the line and a third checks it.
- The solution of two simultaneous equations is the coordinates of the point
  where their graphs cross.
- An inequality is solved like an equation, but multiplying or dividing by a
  negative number reverses the sign.
- On a number line, an open circle means the value is excluded and a filled
  circle means it is included.

## Practice questions

**Group A — Objective (1 mark each)**

1. The solution of $x+7=12$ is <span class="marks">[1]</span>
   (a) 5 (b) $-5$ (c) 19 (d) $-19$
2. If $2x=18$, then $x$ is <span class="marks">[1]</span>
   (a) 36 (b) 9 (c) 16 (d) $\frac{1}{9}$
3. The solution of $x+y=12$, $x-y=2$ is
   <span class="marks">[1]</span>
   (a) $x=7$, $y=5$ (b) $x=5$, $y=7$ (c) $x=6$, $y=6$ (d) $x=10$, $y=2$
4. The graph of $y=3x-2$ crosses the $y$-axis at
   <span class="marks">[1]</span>
   (a) $(0,-2)$ (b) $(-2,0)$ (c) $(0,3)$ (d) $(3,0)$
5. The solution of $-3x>9$ is <span class="marks">[1]</span>
   (a) $x>3$ (b) $x<-3$ (c) $x>-3$ (d) $x<3$
6. The point $(1,4)$ lies on the line <span class="marks">[1]</span>
   (a) $y=x+3$ (b) $y=2x-1$ (c) $y=3x+1$ (d) $y=4x-1$

::: note Answers to Group A
**1.** (a) — subtract 7 from both sides.
**2.** (b) — divide by 2.
**3.** (a) — adding gives $2x=14$, so $x=7$ and $y=5$.
**4.** (a) — put $x=0$.
**5.** (b) — dividing by $-3$ reverses the sign.
**6.** (a) — $1+3=4$ ✓.
:::

**Group B — Short answer (2 marks each)**

1. Solve $5x-3=2x+9$. <span class="marks">[2]</span>
2. Solve $x+y=15$, $x-y=3$. <span class="marks">[2]</span>
3. Solve $\frac{x}{3}+\frac{x}{4}=7$. <span class="marks">[2]</span>
4. Solve $2x+5\ge11$ and show the solution on a number line.
   <span class="marks">[2]</span>

::: note Answers to Group B
**1.** $3x=12$, so $x=4$.
**2.** Adding: $2x=18$, so $x=9$ and $y=6$.
**3.** Multiply by 12: $4x+3x=84$, so $7x=84$ and $x=12$.
**4.** $2x\ge6$, so $x\ge3$: a filled circle at 3 with the shading to the right.
:::

**Group C — Long answer (4 marks each)**

1. Solve $3x+2y=16$ and $2x-y=6$ by the elimination method, and check both
   equations. <span class="marks">[4]</span>
2. The sum of the ages of a father and his son is 48 years. In 6 years the
   father will be three times as old as the son. Find their present ages.
   <span class="marks">[4]</span>

::: note Answers to Group C
**1.** **Step 1 — make the $y$ coefficients match.** The second equation times 2
gives $4x-2y=12$.
**Step 2 — add** (the $y$ terms have opposite signs):
$$(3x+2y)+(4x-2y)=16+12\;\Longrightarrow\;7x=28\;\Longrightarrow\;x=4$$
**Step 3 — substitute** into $2x-y=6$: $8-y=6$, so $y=2$.
**Answer.** $x=4$, $y=2$.
**Check.** $3(4)+2(2)=12+4=16$ ✓ and $2(4)-2=6$ ✓.
**2.** Let the father's age be $f$ and the son's $s$ years.
$$f+s=48$$
In 6 years the father is $f+6$ and the son $s+6$, and
$f+6=3(s+6)$, that is $f=3s+12$. Substituting into the first equation:
$3s+12+s=48$, so $4s=36$ and $s=9$; then $f=48-9=39$.
**Answer.** The father is 39 and the son is 9.
**Check.** In 6 years they are 45 and 15, and $45=3\times15$ ✓.
:::

**Extra practice — textbook-style questions**

**1.** Solve graphically: $x+y=5$, $x-y=3$.
**2.** Solve: (a) $x^2+x-6=0$ (b) $9y^2-16=0$ (c) $2x^2-x=0$.
**3.** Find the quadratic equation whose roots are $-1$ and $2$.
**4.** There are cats and hens in a yard: 10 heads and 26 legs in all. How many of each?

::: note Extra practice — answers
**1.** For $y=5-x$: (0, 5), (5, 0); for $y=x-3$: (3, 0), (5, 2). The lines meet at $(4,1)$, so $x=4$, $y=1$. Check: $4+1=5$, $4-1=3$ ✓.
**2.** (a) $(x+3)(x-2)=0$, $x=-3$ or $2$. (b) $(3y+4)(3y-4)=0$, $y=\pm\frac43$. (c) $x(2x-1)=0$, $x=0$ or $\frac12$.
**3.** $(x+1)(x-2)=0$, i.e. $x^2-x-2=0$.
**4.** Cats $c$, hens $h$: $c+h=10$, $4c+2h=26$. Subtracting twice the first: $2c=6$, so $c=3$, $h=7$. Check: $12+14=26$ legs ✓.
:::

## Objective practice

**Choose the correct answer.** <span class="marks">[5×1=5]</span>

**1.** The solution of $4x - 9 = 2x + 7$ is
   (a) 4 (b) 8 (c) 16 (d) $-8$
**2.** The slope of the line $y = -2x + 5$ is
   (a) 5 (b) $-2$ (c) 2 (d) $-5$
**3.** The line $y = 3x - 6$ cuts the $y$-axis at
   (a) $(0,3)$ (b) $(0,-6)$ (c) $(2,0)$ (d) $(-6,0)$
**4.** If $\frac{x}{5} + 2 = 7$, then $x$ is
   (a) 15 (b) 20 (c) 25 (d) 45
**5.** The graph of $y = 4$ is a line that is
   (a) parallel to the $x$-axis (b) parallel to the $y$-axis (c) through the origin (d) slanting

::: note Objective practice — answers
**1.** (b) — $2x = 16$, so $x = 8$. **2.** (b) — the coefficient of $x$. **3.** (b) — put $x = 0$. **4.** (c) — $\frac{x}{5} = 5$, so $x = 25$. **5.** (a) — every point has $y = 4$, so it is horizontal.
:::
