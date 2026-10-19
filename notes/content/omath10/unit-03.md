---
subject: Optional Mathematics
grade: 10
unit: 3
title: Matrices and Determinants
hours: 0
area: Units
---

A shopkeeper who sells pens, copies and bags in two shops keeps the prices in a table of rows and columns. Such a rectangular table of numbers is a **matrix**. Matrices let us handle many numbers as one object, and they give us a clean way to solve simultaneous equations. In this chapter we attach a single number, the **determinant**, to every square matrix; use it to decide whether the matrix has an **inverse**; find that inverse for a $2\times2$ matrix; and then solve pairs of linear equations in two ways: by the **matrix method** ($X=A^{-1}B$) and by **Cramer's rule**.

::: key What the SEE asks from this chapter
Expect: (i) find the determinant of a $2\times2$ matrix and find the unknown that makes it zero (singular); (ii) find the inverse of a $2\times2$ matrix and **verify** $AA^{-1}=I$; (iii) solve two equations by the **matrix method**; (iv) solve two equations by **Cramer's rule**; (v) a word problem (prices, ages, numbers) that you must first turn into two equations. Show every step: the determinant, the inverse, the product.
:::

## 3.1 Determinant of a matrix

### A quick review

A matrix of $m$ rows and $n$ columns has **order** $m\times n$. A matrix with equal numbers of rows and columns is a **square matrix**. In this chapter we write a $2\times2$ matrix by listing its rows, for example $A=[(3,5),(2,4)]$ means row 1 is $3,\ 5$ and row 2 is $2,\ 4$. The **identity matrix** of order 2 is $I=[(1,0),(0,1)]$; multiplying by $I$ leaves any $2\times2$ matrix unchanged.

To multiply two matrices, take **row of the first times column of the second**: multiply matching entries and add. The product $AB$ exists when the number of columns of $A$ equals the number of rows of $B$.

```figure caption="Product of two $2\times2$ matrices. Entry $(1,1)$ is $1\times0+2\times2=4$; entry $(1,2)$ is $1\times1+2\times3=7$; entry $(2,1)$ is $3\times0+4\times2=8$; entry $(2,2)$ is $3\times1+4\times3=15$."
fig = mateq([[["$1$","$2$"],["$3$","$4$"]], "$\\times$", [["$0$","$1$"],["$2$","$3$"]], "$=$", [["$4$","$7$"],["$8$","$15$"]]])
```

Remember that $AB\neq BA$ in general.

::: definition Determinant of a 2×2 matrix
The **determinant** of a square matrix is a single number attached to it. For $A=[(a,b),(c,d)]$ it is written $|A|$ or $\det A$ and defined by
$$ |A|=ad-bc $$
(the product of the **leading diagonal** minus the product of the other diagonal). A matrix whose determinant is zero is called **singular**; otherwise it is **non-singular**.
:::

```figure caption="The determinant of $A=[(a,b),(c,d)]$ is $ad-bc$: multiply down the leading diagonal, subtract the product along the other diagonal."
fig = mateq(["$|A|=$", ("det", [["$a$","$b$"],["$c$","$d$"]]), "$=ad-bc$"])
```

::: example Value of a determinant
**Problem.** Find the determinant of (i) $A=[(3,5),(2,4)]$, (ii) $B=[(2,-1),(4,-2)]$. Which is singular?

**Solution.** (i) $|A|=3\times4-5\times2=12-10=2$.

(ii) $|B|=2\times(-2)-(-1)\times4=-4+4=0$. So $B$ is **singular**; $A$ is non-singular.
:::

::: example Finding an unknown from a determinant
**Problem.** Find $x$ if the matrix $[(x,2),(3,x+1)]$ is singular.

**Solution.** Its determinant is $x(x+1)-2\times3=x^2+x-6$. For a singular matrix this is 0:
$$ x^2+x-6=0\;\Rightarrow\;(x+3)(x-2)=0\;\Rightarrow\;x=-3\ \text{or}\ x=2. $$
:::

::: key Useful properties of 2×2 determinants
- $|AB|=|A|\,|B|$ (the determinant of a product is the product of the determinants).
- $|kA|=k^2|A|$ for a $2\times2$ matrix: multiplying **every** entry by $k$ multiplies the determinant by $k^2$.
- $|I|=1$.
:::

::: example Checking the properties
**Problem.** Let $A=[(1,2),(3,4)]$ and $B=[(0,1),(2,3)]$. Verify that $|AB|=|A||B|$ and find $|3A|$.

**Solution.** $|A|=4-6=-2$ and $|B|=0-2=-2$, so $|A||B|=4$.

From the figure above, $AB=[(4,7),(8,15)]$ and $|AB|=4\times15-7\times8=60-56=4$. ✓

$3A=[(3,6),(9,12)]$, so $|3A|=36-54=-18=3^2\times(-2)$. ✓
:::

::: example Matrix equation
**Problem.** If $A=[(1,2),(3,4)]$, show that $A^2-5A-2I=O$, where $O$ is the zero matrix.

**Solution.** $A^2=A\times A$: entry $(1,1)=1+6=7$, $(1,2)=2+8=10$, $(2,1)=3+12=15$, $(2,2)=6+16=22$. So $A^2=[(7,10),(15,22)]$.

$5A=[(5,10),(15,20)]$ and $2I=[(2,0),(0,2)]$.

$A^2-5A=[(2,0),(0,2)]$, so $A^2-5A-2I=[(0,0),(0,0)]=O$. ✓
:::

::: caution Common mistakes
- Computing $|A|=ad+bc$ or $ac-bd$. The rule is $ad-bc$: leading diagonal first.
- Writing $|kA|=k|A|$. For a $2\times2$ matrix it is $k^2|A|$.
- Multiplying matrices entry by entry. It is **row times column**.
- Saying "the matrix is zero" when the determinant is zero. The matrix is merely **singular**.
:::

::: example Adding, scalar multiples and the order of multiplication
**Problem.** Let $A=[(2,1),(3,4)]$ and $B=[(1,0),(2,5)]$. Find $A+B$, $3A$, $AB$ and $BA$. Is $AB=BA$?

**Solution.** Add or scale entry by entry: $A+B=[(3,1),(5,9)]$ and $3A=[(6,3),(9,12)]$.

$AB$: entry $(1,1)=2(1)+1(2)=4$; $(1,2)=2(0)+1(5)=5$; $(2,1)=3(1)+4(2)=11$; $(2,2)=3(0)+4(5)=20$. So $AB=[(4,5),(11,20)]$.

$BA$: entry $(1,1)=1(2)+0(3)=2$; $(1,2)=1(1)+0(4)=1$; $(2,1)=2(2)+5(3)=19$; $(2,2)=2(1)+5(4)=22$. So $BA=[(2,1),(19,22)]$.

Clearly $AB\neq BA$: **matrix multiplication is not commutative**.
:::

::: example Equal matrices and a determinant condition
**Problem.** (i) Find $x$ and $y$ if $[(x+y,\,2),(3,\,x-y)]=[(5,\,2),(3,\,1)]$. (ii) Find $x$ if the determinant of $[(x,2),(3,4)]$ is 10.

**Solution.** (i) Equal matrices have equal entries: $x+y=5$ and $x-y=1$. Adding: $2x=6$, $x=3$, and $y=2$.

(ii) $4x-2\times3=10\Rightarrow4x=16\Rightarrow x=4$.
:::

## 3.2 Inverse of a matrix

For numbers, $a\times\frac{1}{a}=1$. For matrices, if a square matrix $A$ has a matrix $B$ with $AB=BA=I$, then $B$ is the **inverse** of $A$ and is written $A^{-1}$.

::: derivation Inverse of a 2×2 matrix
We start from $A=[(a,b),(c,d)]$ and are heading for a formula for $A^{-1}$.

**Step 1 — build a helper matrix.** Swap the leading-diagonal entries and change the signs of the other two: $B=[(d,-b),(-c,a)]$.

**Step 2 — multiply $A$ by $B$.**
- Entry $(1,1)$: $ad+b(-c)=ad-bc$.
- Entry $(1,2)$: $a(-b)+ba=0$.
- Entry $(2,1)$: $cd+d(-c)=0$.
- Entry $(2,2)$: $c(-b)+da=ad-bc$.

So $AB=[(ad-bc,\,0),(0,\,ad-bc)]=(ad-bc)\,I=|A|\,I$.

**Step 3 — divide by $|A|$** (this needs $|A|\neq0$): $A\left(\frac{1}{|A|}B\right)=I$. The matrix in brackets is the inverse.

**Result.**
$$ A^{-1}=\frac{1}{ad-bc}\,[(d,-b),(-c,a)] $$

**What it means.** The inverse exists **only if** $ad-bc\neq0$, that is, only if $A$ is non-singular. A singular matrix has no inverse.
:::

```figure caption="Inverse of a $2\times2$ matrix: interchange $a$ and $d$, change the signs of $b$ and $c$, divide by the determinant."
fig = mateq(["$A^{-1}=$", "$\\frac{1}{ad-bc}$", [["$d$","$-b$"],["$-c$","$a$"]]])
```

::: tip The examiner is looking for
(1) the determinant $|A|$ found first, (2) the statement $|A|\neq0$, (3) the swap-and-negate matrix, (4) the factor $\frac{1}{|A|}$ in front, (5) a check by multiplying $AA^{-1}=I$.
:::

::: example Finding and verifying an inverse
**Problem.** Find the inverse of $A=[(4,3),(3,2)]$ and verify that $AA^{-1}=I$.

**Solution.** $|A|=4\times2-3\times3=8-9=-1\neq0$, so $A^{-1}$ exists.
$$ A^{-1}=\frac{1}{-1}\,[(2,-3),(-3,4)]=[(-2,3),(3,-4)] $$

Verification: entry $(1,1)=4(-2)+3(3)=1$, $(1,2)=4(3)+3(-4)=0$, $(2,1)=3(-2)+2(3)=0$, $(2,2)=3(3)+2(-4)=1$.
:::

```figure caption="Verification that $A^{-1}$ is correct for $A=[(4,3),(3,2)]$: the product $AA^{-1}$ is the identity matrix."
fig = mateq([[["$4$","$3$"],["$3$","$2$"]], "$\\times$", [["$-2$","$3$"],["$3$","$-4$"]], "$=$", [["$1$","$0$"],["$0$","$1$"]]])
```

::: example Another inverse
**Problem.** Find the inverse of $P=[(2,5),(1,3)]$. For what value of $k$ is $Q=[(k,3),(2,6)]$ without an inverse?

**Solution.** $|P|=6-5=1$, so $P^{-1}=\frac{1}{1}[(3,-5),(-1,2)]=[(3,-5),(-1,2)]$.

$Q$ has no inverse when $|Q|=0$: $6k-6=0$, so $k=1$.
:::

::: key Properties of the inverse
- $AA^{-1}=A^{-1}A=I$.
- $|A^{-1}|=\frac{1}{|A|}$.
- $(AB)^{-1}=B^{-1}A^{-1}$ (the order **reverses**).
:::

::: example Inverse of a product
**Problem.** For $A=[(2,1),(1,1)]$ and $B=[(1,2),(1,3)]$ verify that $(AB)^{-1}=B^{-1}A^{-1}$.

**Solution.** $|A|=1$, $A^{-1}=[(1,-1),(-1,2)]$. $|B|=1$, $B^{-1}=[(3,-2),(-1,1)]$.

$AB=[(2+1,\,4+3),(1+1,\,2+3)]=[(3,7),(2,5)]$, $|AB|=15-14=1$, so $(AB)^{-1}=[(5,-7),(-2,3)]$.

$B^{-1}A^{-1}=[(3,-2),(-1,1)]\times[(1,-1),(-1,2)]$: entry $(1,1)=3+2=5$, $(1,2)=-3-4=-7$, $(2,1)=-1-1=-2$, $(2,2)=1+2=3$. So $B^{-1}A^{-1}=[(5,-7),(-2,3)]=(AB)^{-1}$. ✓
:::

::: example A matrix equation AX = B
**Problem.** If $A=[(2,1),(5,3)]$ and $B=[(1,2),(3,4)]$, find the matrix $X$ such that $AX=B$.

**Solution.** Multiply both sides **on the left** by $A^{-1}$: $X=A^{-1}B$. $|A|=6-5=1$, so $A^{-1}=[(3,-1),(-5,2)]$.

$X=[(3,-1),(-5,2)]\times[(1,2),(3,4)]$: entry $(1,1)=3-3=0$, $(1,2)=6-4=2$, $(2,1)=-5+6=1$, $(2,2)=-10+8=-2$. So $X=[(0,2),(1,-2)]$.

Check: $AX$: $(1,1)=0+1=1$, $(1,2)=4-2=2$, $(2,1)=0+3=3$, $(2,2)=10-6=4$. ✓
:::

## 3.3 Solving linear equations by the matrix method

A pair of linear equations
$$ a_1x+b_1y=c_1,\qquad a_2x+b_2y=c_2 $$
can be written as one matrix equation $AX=B$, with $A=[(a_1,b_1),(a_2,b_2)]$ (the coefficient matrix), $X$ the column of unknowns $x,\ y$ and $B$ the column of constants $c_1,\ c_2$.

```figure caption="The equations $2x+y=5$ and $5x+3y=13$ written as $AX=B$."
fig = mateq([[["$2$","$1$"],["$5$","$3$"]], [["$x$"],["$y$"]], "$=$", [["$5$"],["$13$"]]])
```

If $|A|\neq0$, multiply both sides by $A^{-1}$ on the left. Since $A^{-1}A=I$ and $IX=X$:

::: key Matrix method
$$ AX=B \;\Rightarrow\; X=A^{-1}B $$
Steps: (1) write the equations in the form $a_1x+b_1y=c_1$; (2) form $A$ and $B$; (3) find $|A|$ and $A^{-1}$; (4) multiply $A^{-1}B$; (5) read $x$ and $y$; (6) check in the original equations.
:::

::: example Solving by the matrix method
**Problem.** Solve $2x+y=5$, $5x+3y=13$ by the matrix method.

**Solution.** $A=[(2,1),(5,3)]$ and $B$ has entries $5,\ 13$. $|A|=6-5=1$, so $A^{-1}=[(3,-1),(-5,2)]$.

$$ x=3(5)+(-1)(13)=15-13=2,\qquad y=(-5)(5)+2(13)=-25+26=1 $$

So $x=2$, $y=1$. Check: $2(2)+1=5$ ✓ and $5(2)+3(1)=13$ ✓.
:::

::: example A second matrix-method problem
**Problem.** Solve $3x+2y=8$, $4x+3y=11$ by the matrix method.

**Solution.** $|A|=9-8=1$ and $A^{-1}=[(3,-2),(-4,3)]$.

$x=3(8)-2(11)=24-22=2$ and $y=-4(8)+3(11)=-32+33=1$. So $(x,y)=(2,1)$.
:::

::: example Pens and copies
**Problem.** Three pens and two copies cost Rs 70. Two pens and five copies cost Rs 65. Find the price of a pen and of a copy by the matrix method.

**Solution.** Let a pen cost Rs $x$ and a copy Rs $y$: $3x+2y=70$, $2x+5y=65$.

$A=[(3,2),(2,5)]$, $|A|=15-4=11$, $A^{-1}=\frac{1}{11}[(5,-2),(-2,3)]$.

$$ x=\frac{5(70)-2(65)}{11}=\frac{350-130}{11}=20,\qquad y=\frac{-2(70)+3(65)}{11}=\frac{-140+195}{11}=5 $$

A pen costs **Rs 20** and a copy costs **Rs 5**. Check: $3(20)+2(5)=70$ ✓; $2(20)+5(5)=65$ ✓.
:::

### When the matrix method fails

If $|A|=0$, $A^{-1}$ does not exist and the method cannot be used. Then the two lines are parallel or the same line.

```figure caption="Three possibilities for two linear equations: (left) $|A|\neq0$, the lines meet at exactly one point; (middle) $|A|=0$ and the equations contradict, the lines are parallel, no solution; (right) $|A|=0$ and the equations are the same line, infinitely many solutions."
x = np.linspace(-1, 5, 50)
fig, axs = plt.subplots(1, 3, figsize=(4.8, 2.3), sharey=True)
axs[0].plot(x, 5 - x, color=ACCENT); axs[0].plot(x, x - 1, color=SERIES[1]); axs[0].plot([3], [2], 'ko', ms=4)
axs[0].set_title('one solution', fontsize=8)
axs[1].plot(x, 3 - x, color=ACCENT); axs[1].plot(x, 4 - x, color=SERIES[1]); axs[1].set_title('none', fontsize=8)
axs[2].plot(x, 3 - x, color=ACCENT, lw=3); axs[2].plot(x, 3 - x, color=SERIES[1], lw=1, ls='--'); axs[2].set_title('infinitely many', fontsize=8)
for a in axs:
    a.set_xlim(-1, 5); a.set_ylim(-2, 6); a.axhline(0, color=INK, lw=0.6); a.axvline(0, color=INK, lw=0.6)
    a.tick_params(labelsize=6.5); a.grid(color=GRID, lw=0.4); a.spines[['top','right']].set_visible(False)
fig.tight_layout(pad=0.3)
```

::: example Equations with no solution and with many solutions
**Problem.** Examine $x+2y=3$, $2x+4y=7$ and also $x+2y=3$, $2x+4y=6$.

**Solution.** In both cases $|A|=1\times4-2\times2=0$, so there is no inverse.

First system: doubling the first equation gives $2x+4y=6$, which contradicts $2x+4y=7$. **No solution.**

Second system: $2x+4y=6$ is just the first equation doubled. The equations are the same line: **infinitely many solutions**, for example $(1,1)$ and $(3,0)$.
:::

::: example Matrix method with a negative solution
**Problem.** Solve $2x+3y=3$ and $3x+5y=4$ by the matrix method.

**Solution.** $A=[(2,3),(3,5)]$, $|A|=10-9=1$, $A^{-1}=[(5,-3),(-3,2)]$. The constants are $3$ and $4$.

$$ x=5(3)-3(4)=15-12=3,\qquad y=-3(3)+2(4)=-9+8=-1 $$

Check: $2(3)+3(-1)=3$ ✓; $3(3)+5(-1)=4$ ✓. A solution may be negative; do not worry.
:::

::: example Solving a matrix equation directly
**Problem.** If $A=[(2,3),(1,2)]$, show that $A^2-4A+I=O$ and use it to find $A^{-1}$.

**Solution.** $A^2$: $(1,1)=4+3=7$, $(1,2)=6+6=12$, $(2,1)=2+2=4$, $(2,2)=3+4=7$. So $A^2=[(7,12),(4,7)]$. $4A=[(8,12),(4,8)]$.

$A^2-4A+I=[(7-8+1,\ 12-12+0),(4-4+0,\ 7-8+1)]=O$. ✓

Multiply $A^2-4A+I=O$ by $A^{-1}$: $A-4I+A^{-1}=O$, so $A^{-1}=4I-A=[(4-2,\,-3),(-1,\,4-2)]=[(2,-3),(-1,2)]$.

Check with the formula: $|A|=4-3=1$, $A^{-1}=[(2,-3),(-1,2)]$. ✓
:::

## 3.4 Cramer's rule

Cramer's rule solves the same equations directly with determinants, without finding an inverse.

::: derivation Cramer's rule for two equations
We start from $a_1x+b_1y=c_1$ and $a_2x+b_2y=c_2$ and are heading for $x$ and $y$ in terms of determinants.

**Step 1 — eliminate $y$.** Multiply the first equation by $b_2$ and the second by $b_1$:
$$ a_1b_2x+b_1b_2y=c_1b_2,\qquad a_2b_1x+b_1b_2y=c_2b_1 $$

**Step 2 — subtract.**
$$ (a_1b_2-a_2b_1)\,x=c_1b_2-c_2b_1 $$

**Step 3 — divide**, if $a_1b_2-a_2b_1\neq0$:
$$ x=\frac{c_1b_2-c_2b_1}{a_1b_2-a_2b_1} $$

**Step 4 — eliminate $x$ the same way** (multiply by $a_2$ and $a_1$, subtract):
$$ y=\frac{a_1c_2-a_2c_1}{a_1b_2-a_2b_1} $$

**Result.** Each numerator and denominator is a $2\times2$ determinant: the denominator is $D=|(a_1,b_1),(a_2,b_2)|$; the numerator of $x$ is $D_x=|(c_1,b_1),(c_2,b_2)|$ (the $x$-column replaced by the constants); the numerator of $y$ is $D_y=|(a_1,c_1),(a_2,c_2)|$.
:::

::: key Cramer's rule
For $a_1x+b_1y=c_1$ and $a_2x+b_2y=c_2$:
$$ D=a_1b_2-a_2b_1,\quad D_x=c_1b_2-c_2b_1,\quad D_y=a_1c_2-a_2c_1 $$
$$ x=\frac{D_x}{D},\qquad y=\frac{D_y}{D}\qquad(D\neq0) $$
- $D\neq0$: unique solution.
- $D=0$ and $D_x\neq0$ or $D_y\neq0$: **no solution**.
- $D=D_x=D_y=0$: infinitely many solutions.
:::

```figure caption="Cramer's rule: $D_x$ is $D$ with its first column replaced by the constants $c_1,c_2$; $D_y$ is $D$ with its second column replaced."
fig = mateq(["$D_x=$", ("det", [["$c_1$","$b_1$"],["$c_2$","$b_2$"]]), "$D_y=$", ("det", [["$a_1$","$c_1$"],["$a_2$","$c_2$"]])])
```

::: example Solving by Cramer's rule
**Problem.** Solve $3x+4y=10$, $2x-y=3$ by Cramer's rule.

**Solution.** $D=3(-1)-2(4)=-3-8=-11$.

$D_x=10(-1)-3(4)=-10-12=-22$. $D_y=3(3)-2(10)=9-20=-11$.

$$ x=\frac{-22}{-11}=2,\qquad y=\frac{-11}{-11}=1 $$

Check: $3(2)+4(1)=10$ ✓; $2(2)-1=3$ ✓.
:::

::: example Equations that must be rearranged first
**Problem.** Solve $2(x-1)=y$ and $3(x-1)=4y$ by Cramer's rule.

**Solution.** Write in the form $ax+by=c$: $2x-y=2$ and $3x-4y=3$.

$D=2(-4)-3(-1)=-8+3=-5$. $D_x=2(-4)-3(-1)=-5$. $D_y=2(3)-3(2)=0$.

$x=\frac{-5}{-5}=1$, $y=\frac{0}{-5}=0$. The solution is $(1,0)$.
:::

::: example Equations with fractions
**Problem.** Solve $\frac{x}{2}+\frac{y}{3}=3$ and $\frac{x}{4}-\frac{y}{3}=0$.

**Solution.** Clear fractions: multiply the first by 6 and the second by 12: $3x+2y=18$ and $3x-4y=0$.

$D=3(-4)-3(2)=-18$. $D_x=18(-4)-0(2)=-72$. $D_y=3(0)-3(18)=-54$.

$x=\frac{-72}{-18}=4$, $y=\frac{-54}{-18}=3$. Check: $\frac{4}{2}+\frac{3}{3}=2+1=3$ ✓; $\frac{4}{4}-\frac{3}{3}=0$ ✓.
:::

::: example When is there no unique solution?
**Problem.** For what value of $k$ do $3x+ky=5$ and $6x+4y=7$ have no unique solution? Do they then have no solution or many?

**Solution.** $D=3(4)-6k=12-6k$. No unique solution when $D=0$, so $k=2$.

For $k=2$: the first equation is $3x+2y=5$; doubling it gives $6x+4y=10\neq7$. The equations contradict each other, so there is **no solution**.
:::

::: caution Common mistakes
- Replacing the wrong column: $D_x$ replaces the **$x$-column** (first), $D_y$ the **second** column.
- Not writing the equations as $ax+by=c$ first, so the constants land on the wrong side.
- Forgetting to check $D\neq0$ before dividing.
- In the matrix method, multiplying $BA^{-1}$ instead of $A^{-1}B$. The inverse goes on the **left**.
:::

::: example Cramer's rule with $D=0$
**Problem.** Use Cramer's rule to examine (i) $2x+3y=5,\ 4x+6y=10$ and (ii) $2x+3y=5,\ 4x+6y=11$.

**Solution.** In both, $D=2(6)-4(3)=0$.

(i) $D_x=5(6)-10(3)=0$ and $D_y=2(10)-4(5)=0$. All three vanish: the second equation is twice the first, so there are **infinitely many solutions**.

(ii) $D_x=5(6)-11(3)=-3\neq0$. With $D=0$ and $D_x\neq0$ there is **no solution**.
:::

::: key Which method to use?
| Method | Best when | Needs |
|---|---|---|
| Elimination or substitution | numbers are small and easy | nothing special |
| Matrix method $X=A^{-1}B$ | the question says "by the matrix method" | $A^{-1}$ must exist ($|A|\neq0$) |
| Cramer's rule | the question says "by Cramer's rule" or you want each unknown separately | $D\neq0$ |

Follow the method named in the question: the marks are for the method.
:::

## 3.5 Exercises of the SEE type

::: example Prices of rice and dal
**Problem.** Two kg of rice and three kg of lentils cost Rs 650. Three kg of rice and one kg of lentils cost Rs 450. Find the price per kg of each by Cramer's rule.

**Solution.** Let rice be Rs $x$/kg and lentils Rs $y$/kg: $2x+3y=650$ and $3x+y=450$.

$D=2(1)-3(3)=-7$. $D_x=650(1)-450(3)=650-1350=-700$. $D_y=2(450)-3(650)=900-1950=-1050$.

$x=\frac{-700}{-7}=100$, $y=\frac{-1050}{-7}=150$. Rice is **Rs 100/kg** and lentils **Rs 150/kg**.
:::

::: example Two numbers
**Problem.** The sum of two numbers is 12 and their difference is 4. Find the numbers by the matrix method.

**Solution.** $x+y=12$, $x-y=4$. $A=[(1,1),(1,-1)]$, $|A|=-1-1=-2$, $A^{-1}=\frac{1}{-2}[(-1,-1),(-1,1)]=[(\frac{1}{2},\frac{1}{2}),(\frac{1}{2},-\frac{1}{2})]$.

$x=\frac{1}{2}(12)+\frac{1}{2}(4)=8$, $y=\frac{1}{2}(12)-\frac{1}{2}(4)=4$. The numbers are **8 and 4**.
:::

::: example Ages
**Problem.** The sum of the ages of a mother and her daughter is 50 years, and the mother is 4 times as old as her daughter. Find their ages by Cramer's rule.

**Solution.** Let the mother be $x$ years and the daughter $y$ years: $x+y=50$ and $x-4y=0$.

$D=1(-4)-1(1)=-5$. $D_x=50(-4)-0(1)=-200$. $D_y=1(0)-1(50)=-50$.

$x=\frac{-200}{-5}=40$, $y=\frac{-50}{-5}=10$. The mother is **40** and the daughter **10**.
:::

::: example Tickets
**Problem.** Three adult tickets and two child tickets cost Rs 1,100. Two adult tickets and three child tickets cost Rs 900. Find the price of each ticket by Cramer's rule.

**Solution.** Let an adult ticket be Rs $a$ and a child ticket Rs $c$: $3a+2c=1100$ and $2a+3c=900$.

$D=3(3)-2(2)=5$. $D_a=1100(3)-900(2)=3300-1800=1500$. $D_c=3(900)-2(1100)=2700-2200=500$.

$a=\frac{1500}{5}=300$ and $c=\frac{500}{5}=100$. An adult ticket costs **Rs 300** and a child ticket **Rs 100**.
:::

::: example Two numbers by the matrix method
**Problem.** The sum of two numbers is 18, and twice the first plus three times the second is 44. Find the numbers by the matrix method.

**Solution.** $x+y=18$ and $2x+3y=44$. $A=[(1,1),(2,3)]$, $|A|=3-2=1$, $A^{-1}=[(3,-1),(-2,1)]$.

$x=3(18)-1(44)=54-44=10$ and $y=-2(18)+1(44)=-36+44=8$. The numbers are **10 and 8**. Check: $10+8=18$ ✓; $20+24=44$ ✓.
:::

::: example Which matrices are singular?
**Problem.** For which value of $k$ does $[(k+1,\,3),(2,\,k)]$ have no inverse? Then find the inverse of the matrix when $k=3$.

**Solution.** The determinant is $k(k+1)-6=k^2+k-6=(k+3)(k-2)$. There is no inverse when $k=-3$ or $k=2$.

For $k=3$ the matrix is $[(4,3),(2,3)]$ with determinant $12-6=6$, so the inverse is $\frac{1}{6}[(3,-3),(-2,4)]$.
:::

## Chapter summary

- **Determinant:** $|A|=ad-bc$ for $A=[(a,b),(c,d)]$. $A$ is singular if $|A|=0$. $|AB|=|A||B|$, $|kA|=k^2|A|$.
- **Inverse:** $A^{-1}=\frac{1}{ad-bc}[(d,-b),(-c,a)]$, exists only if $|A|\neq0$. $AA^{-1}=A^{-1}A=I$; $(AB)^{-1}=B^{-1}A^{-1}$; $|A^{-1}|=\frac{1}{|A|}$.
- **Matrix method:** $AX=B\Rightarrow X=A^{-1}B$ (inverse on the left); needs $|A|\neq0$.
- **Cramer's rule:** $x=\frac{D_x}{D}$, $y=\frac{D_y}{D}$ with $D=a_1b_2-a_2b_1$, $D_x=c_1b_2-c_2b_1$, $D_y=a_1c_2-a_2c_1$.
- $D\neq0$: one solution; $D=0$ with $D_x\neq0$: none; $D=D_x=D_y=0$: infinitely many.
- Write the equations as $ax+by=c$ before forming any matrix or determinant, and always check the answer.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The determinant of $[(4,3),(2,5)]$ is <span class="marks">[1]</span>
   (a) 26 (b) 14 (c) $-14$ (d) 20
2. The matrix $[(2,3),(4,6)]$ is <span class="marks">[1]</span>
   (a) an identity matrix (b) singular (c) non-singular (d) a zero matrix
3. If $|A|=4$, then $|A^{-1}|$ is <span class="marks">[1]</span>
   (a) 4 (b) $-4$ (c) $\frac{1}{4}$ (d) $-\frac{1}{4}$
4. The matrix $[(k,2),(3,6)]$ is singular when $k$ equals <span class="marks">[1]</span>
   (a) 1 (b) 2 (c) 3 (d) 6
5. In Cramer's rule, $x$ equals <span class="marks">[1]</span>
   (a) $\frac{D}{D_x}$ (b) $\frac{D_x}{D}$ (c) $\frac{D_y}{D}$ (d) $D_xD$
6. The equations $x+y=2$ and $2x+2y=5$ have <span class="marks">[1]</span>
   (a) one solution (b) two solutions (c) no solution (d) infinitely many solutions

::: note Answers to Group A
**1.** (b) — $4\times5-3\times2=14$.
**2.** (b) — $2\times6-3\times4=0$.
**3.** (c) — $|A^{-1}|=\frac{1}{|A|}$.
**4.** (a) — $6k-6=0$.
**5.** (b) — $x=D_x/D$.
**6.** (c) — $D=0$ and doubling the first gives $2x+2y=4\neq5$.
:::

**Group B — Short answer (2 marks each)**

1. Find the determinant of $[(7,3),(5,2)]$. <span class="marks">[2]</span>
2. Find $x$ if $[(x,2),(3,x+1)]$ is singular. <span class="marks">[2]</span>
3. Find the inverse of $A=[(2,5),(1,3)]$. <span class="marks">[2]</span>
4. Solve $x+y=5$, $x-y=1$ by Cramer's rule. <span class="marks">[2]</span>
5. If $A=[(1,2),(3,4)]$, find $|2A|$. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** $7\times2-3\times5=-1$.
**2.** $x(x+1)-6=0\Rightarrow(x+3)(x-2)=0$, so $x=-3$ or $2$.
**3.** $|A|=1$; $A^{-1}=[(3,-5),(-1,2)]$.
**4.** $D=-1-1=-2$, $D_x=-5-1=-6$, $D_y=1-5=-4$. $x=3$, $y=2$.
**5.** $|A|=-2$, so $|2A|=2^2\times(-2)=-8$.
:::

**Group C — Short answer (3 marks each)**

1. Find the inverse of $A=[(4,3),(3,2)]$ and verify that $AA^{-1}=I$. <span class="marks">[3]</span>
2. Solve $2x+y=5$ and $5x+3y=13$ by the matrix method. <span class="marks">[3]</span>
3. Solve $3x+4y=10$ and $2x-y=3$ by Cramer's rule. <span class="marks">[3]</span>
4. For what value of $k$ do $3x+ky=5$ and $6x+4y=7$ have no solution? <span class="marks">[3]</span>
5. If $A=[(1,2),(3,4)]$, show that $A^2-5A-2I=O$. <span class="marks">[3]</span>

::: note Answers to Group C
**1.** $|A|=8-9=-1$. $A^{-1}=\frac{1}{-1}[(2,-3),(-3,4)]=[(-2,3),(3,-4)]$. $AA^{-1}$ entries: $4(-2)+3(3)=1$; $4(3)+3(-4)=0$; $3(-2)+2(3)=0$; $3(3)+2(-4)=1$. So $AA^{-1}=I$.
**2.** $|A|=1$, $A^{-1}=[(3,-1),(-5,2)]$. $x=15-13=2$, $y=-25+26=1$.
**3.** $D=-11$, $D_x=-22$, $D_y=-11$. $x=2$, $y=1$.
**4.** $D=12-6k=0\Rightarrow k=2$. Then $3x+2y=5$ doubled gives $6x+4y=10\neq7$: no solution.
**5.** $A^2=[(7,10),(15,22)]$, $5A=[(5,10),(15,20)]$, $2I=[(2,0),(0,2)]$. $A^2-5A-2I=O$.
:::

**Group D — Long answer (4 marks each)**

1. Solve $3x+2y=8$ and $4x+3y=11$ by the matrix method. <span class="marks">[4]</span>
2. If $A=[(2,1),(5,3)]$ and $B=[(1,2),(3,4)]$, find the matrix $X$ such that $AX=B$. <span class="marks">[4]</span>
3. Two kg of rice and three kg of lentils cost Rs 650, and three kg of rice and one kg of lentils cost Rs 450. Find the price per kg of each by Cramer's rule. <span class="marks">[4]</span>
4. For $A=[(2,1),(1,1)]$ and $B=[(1,2),(1,3)]$ verify that $(AB)^{-1}=B^{-1}A^{-1}$. <span class="marks">[4]</span>
5. Solve $\frac{x}{2}+\frac{y}{3}=3$ and $\frac{x}{4}-\frac{y}{3}=0$ by Cramer's rule. <span class="marks">[4]</span>

::: note Answers to Group D
**1.** $|A|=9-8=1$; $A^{-1}=[(3,-2),(-4,3)]$. $x=3(8)-2(11)=2$, $y=-4(8)+3(11)=1$. $(x,y)=(2,1)$.
**2.** $X=A^{-1}B$ with $A^{-1}=[(3,-1),(-5,2)]$. $X=[(0,2),(1,-2)]$ (entries: $3-3=0$, $6-4=2$, $-5+6=1$, $-10+8=-2$).
**3.** $2x+3y=650$, $3x+y=450$. $D=-7$, $D_x=-700$, $D_y=-1050$. Rice Rs 100/kg, lentils Rs 150/kg.
**4.** $A^{-1}=[(1,-1),(-1,2)]$, $B^{-1}=[(3,-2),(-1,1)]$, $AB=[(3,7),(2,5)]$, $(AB)^{-1}=[(5,-7),(-2,3)]$; $B^{-1}A^{-1}=[(5,-7),(-2,3)]$. Equal.
**5.** $3x+2y=18$, $3x-4y=0$. $D=-18$, $D_x=-72$, $D_y=-54$. $x=4$, $y=3$.
:::


## Retrieval practice and investigation

::: key Work before reading the key
Answer these short retrieval questions without consulting the chapter. Explain the reason, not only the result. These are revision checks, not a prediction of the examination paper.
:::

**1.** Find the determinant of the matrix with rows (2, 1), (1, 1).

**2.** Can the matrix with rows (1, 2), (2, 4) have an inverse?

**3.** Is matrix multiplication always commutative?

::: note Reasoned key
**1.** 2 × 1 − 1 × 1 = 1. A nonzero determinant means the inverse exists.

**2.** No. Its determinant is 4 − 4 = 0; its second row is twice its first row.

**3.** No. Even when both products exist, AB need not equal BA. Check entries, not only the matrix order.

:::

::: tip Investigation — Check an inverse by multiplication
Use the matrix with rows (2, 1) and (1, 1). Calculate its determinant and inverse, then multiply in both orders to obtain the identity. Swap its rows and explain the determinant's sign change.

Submit a one-page record: your method, working or evidence, conclusion, and one limitation. Exchange it with a classmate and check the reasoning against the chapter.
:::
