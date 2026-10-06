---
subject: Question Bank
grade: 10
unit: 18
title: "Optional Mathematics: Unit-wise Subjective Question Bank"
hours: 0
area: Optional Mathematics
---

This chapter gives one fully worked, multi-step practice problem for each of the 12 Optional Mathematics units. The questions make students show the reasoning that a one-line answer hides: choosing a formula, setting up an equation, checking a condition, and stating a conclusion. All items are original practice questions, not claims about any past examination.

::: key Mark your method as well as your answer
In the CDC 2082 grid, a within-content-area question may combine subparts and cognitive levels. In your own solution, write the formula or theorem first, substitute carefully, and finish with a clear statement. For a graph or construction, include labelled axes or points and show the important steps.
:::

::: caution Check restrictions before solving
A denominator cannot be zero, a length cannot be negative, and a square-root sign denotes the non-negative root unless the problem says otherwise. State these restrictions when they affect the answer.
:::

## 18.1 Sequence and Series

1. An arithmetic sequence begins $4,7,10,\ldots$. Find its 20th term and the sum of its first 20 terms. <span class="marks">[5]</span>

::: note Worked solution
Here $a=4$, $d=7-4=3$ and $n=20$.

$$t_{20}=a+(20-1)d=4+19(3)=61. $$

Then

$$S_{20}=\frac{20}{2}[2(4)+19(3)]=10(8+57)=650.$$

The 20th term is **61**, and the sum is **650**.
:::

## 18.2 Quadratic Equations and Graphs

2. For $y=x^2-5x+6$, find the zeros, the $y$-intercept, the coordinates of the vertex, and the axis of symmetry. State whether the parabola opens upward or downward. <span class="marks">[5]</span>

::: note Worked solution
Factor the quadratic: $y=(x-2)(x-3)$. The zeros are $x=2$ and $x=3$, so the graph crosses the $x$-axis at $(2,0)$ and $(3,0)$. At $x=0$, $y=6$, so the $y$-intercept is $(0,6)$. The axis is halfway between the zeros: $x=\frac{2+3}{2}=\frac52$. Substituting, $y=(\frac52)^2-5(\frac52)+6=\frac{25}{4}-\frac{50}{4}+\frac{24}{4}=-\frac14$. Thus the vertex is $(\frac52,-\frac14)$. Since the coefficient of $x^2$ is positive, the parabola opens upward.
:::

## 18.3 Matrices and Determinants

3. Solve $2x+y=7$ and $x-y=2$ using the inverse-matrix method. <span class="marks">[5]</span>

::: note Worked solution
Write the system as $AX=B$, where the rows of $A$ are $(2,1)$ and $(1,-1)$, $X=(x,y)^T$, and $B=(7,2)^T$. The determinant is $|A|=2(-1)-1(1)=-3$, so the inverse exists. The inverse has first row $(1/3,1/3)$ and second row $(1/3,-2/3)$. Multiplying by $B=(7,2)^T$ gives $x=(7+2)/3=3$ and $y=(7-4)/3=1$. Check: $2(3)+1=7$ and $3-1=2$.
:::

## 18.4 Trigonometry: Multiple, Submultiple and Transformation Formulae

4. Using a double-angle identity, find the exact value of $\sin60^\circ$ from $\sin30^\circ$ and $\cos30^\circ$. <span class="marks">[4]</span>

::: note Worked solution
Use $\sin2A=2\sin A\cos A$. Put $A=30^\circ$, so $2A=60^\circ$:

$$\sin60^\circ=2\sin30^\circ\cos30^\circ=2\left(\frac12\right)\left(\frac{\sqrt{3}}{2}\right)=\frac{\sqrt{3}}{2}.$$

This agrees with the special-angle value. Notice that the formula doubles the angle; it does not square the sine.
:::

## 18.5 Trigonometric Equations and Height and Distance

5. Solve $2\sin^2\theta-1=0$ for $0^\circ≤\theta<360^\circ$. <span class="marks">[5]</span>

::: note Worked solution
Rearrange: $\sin^2\theta=\frac12$, so $\sin\theta=\pm\frac{1}{\sqrt{2}}$. The reference angle is $45^\circ$. Sine is positive in quadrants I and II and negative in III and IV. Hence

$$\theta=45^\circ,\;135^\circ,\;225^\circ,\;315^\circ.$$

These are all the solutions in the required interval. The endpoint $360^\circ$ is excluded and would not be a solution in any case.
:::

## 18.6 Angle between Two Lines and Pair of Straight Lines

6. Find the equation of the line through $(2,3)$ perpendicular to $3x+2y-5=0$. <span class="marks">[4]</span>

::: note Worked solution
First write the given line in slope form: $2y=-3x+5$, so its slope is $-3/2$. A perpendicular line has slope $2/3$, the negative reciprocal. Using point-slope form through $(2,3)$,

$$y-3=\frac23(x-2).$$

Multiply by 3 and simplify: $3y-9=2x-4$, so the required line is **$2x-3y+5=0$**. Substituting $(2,3)$ gives $4-9+5=0$, confirming that it passes through the point.
:::

## 18.7 Conic Sections and Circle

7. Find the equation, centre, and radius of the circle through $(0,0)$, $(6,0)$, and $(0,8)$. <span class="marks">[5]</span>

::: note Worked solution
Use the general circle equation $x^2+y^2+Dx+Ey+F=0$. Substituting $(0,0)$ gives $F=0$. Substituting $(6,0)$ gives $36+6D=0$, so $D=-6$. Substituting $(0,8)$ gives $64+8E=0$, so $E=-8$. Thus

$$x^2+y^2-6x-8y=0.$$

Complete squares: $(x-3)^2+(y-4)^2=25$. The centre is **$(3,4)$** and the radius is **5**.
:::

## 18.8 Vector

8. Points $A=(1,2)$ and $B=(7,8)$ are joined by a vector. Find $\overrightarrow{AB}$ and its magnitude. Point $P$ divides $AB$ internally in the ratio $AP:PB=2:1$. Find $P$. <span class="marks">[5]</span>

::: note Worked solution
Subtract the coordinates of $A$ from those of $B$:

$$\overrightarrow{AB}=(7-1,8-2)=(6,6),\qquad |\overrightarrow{AB}|=\sqrt{6^2+6^2}=6\sqrt{2}.$$

For an internal division in ratio $AP:PB=2:1$, the section formula weights the endpoints oppositely:

$$P=\left(\frac{1(1)+2(7)}{3},\frac{1(2)+2(8)}{3}\right)=(5,6).$$

Check: $P-A=(4,4)$ and $B-P=(2,2)$, so $AP:PB=4\sqrt{2}:2\sqrt{2}=2:1$.
:::

## 18.9 Linear Programming and Transformation

9. Maximise $Z=3x+2y$ subject to $x+y≤6$, $x≤4$, $y≤5$, $x≥0$, and $y≥0$. <span class="marks">[5]</span>

::: note Worked solution
The feasible-region corner points are $(0,0)$, $(4,0)$, $(4,2)$, $(1,5)$ and $(0,5)$. Evaluate the objective at each:

| Corner | $(0,0)$ | $(4,0)$ | $(4,2)$ | $(1,5)$ | $(0,5)$ |
|---|---:|---:|---:|---:|---:|
| $Z=3x+2y$ | 0 | 12 | 16 | 13 | 10 |

The greatest value is 16 at $(4,2)$. Therefore $Z_{\max}=16$.
:::

## 18.10 Continuity

10. Define $f(x)=\frac{x^2-9}{x-3}$ for $x\ne3$ and $f(3)=k$. Find $k$ so that $f$ is continuous at $x=3$. <span class="marks">[4]</span>

::: note Worked solution
For $x\ne3$, factor and cancel:

$$f(x)=\frac{(x-3)(x+3)}{x-3}=x+3.$$

So $\lim_{x\to3}f(x)=6$. For continuity, this limit must equal the assigned value $f(3)=k$. Hence **$k=6$**. The cancellation is valid for the limit because it is taken for $x$ near 3 but not equal to 3.
:::

## 18.11 Statistics: Measures of Dispersion

11. Find the mean, population variance, and population standard deviation of $2,4,4,6$. <span class="marks">[5]</span>

::: note Worked solution
The mean is $\bar{x}=(2+4+4+6)/4=4$. Deviations from the mean are $-2,0,0,2$; their squares are $4,0,0,4$. Thus

$$\sigma^2=\frac{4+0+0+4}{4}=2,\qquad \sigma=\sqrt{2}.$$

The population variance is **2**, and the population standard deviation is **$\sqrt{2}\approx1.414$**. The denominator is $N=4$ because the question asks for population measures.
:::

## 18.12 Functions and Polynomials

12. Find the remainder when $f(x)=x^3-3x+2$ is divided by $x-2$. Then factorise $f(x)$ completely. <span class="marks">[5]</span>

::: note Worked solution
By the remainder theorem, the remainder on division by $x-2$ is $f(2)$:

$$f(2)=2^3-3(2)+2=8-6+2=4.$$

To factorise, test simple integer roots: $f(1)=1-3+2=0$ and $f(-2)=-8+6+2=0$. Since $x=1$ is a repeated root, divide or expand to obtain

$$x^3-3x+2=(x-1)^2(x+2).$$

The remainder is **4**, and the complete factorisation is **$(x-1)^2(x+2)$**.
:::
