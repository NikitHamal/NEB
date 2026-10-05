---
subject: Question Bank
grade: 10
unit: 18
title: "Optional Mathematics: Unit-wise Subjective Question Bank"
hours: 0
area: Optional Mathematics
---

The short questions in Optional Mathematics are not “small versions” of long questions. They test whether you can choose a representation: an AP table, a determinant, a labelled triangle, a coordinate graph, a frequency table or a feasible-region sketch. This bank gives a spread of board-style prompts and the full route to each answer.

::: key Marking discipline
Start every solution with the relevant formula, theorem, equation or labelled diagram. A correct final number with no visible route is fragile: a calculator slip can cost the whole answer, while clear steps usually retain method marks.
:::

## 18.1 Algebra, sequences and matrices

1. The 5th term of an AP is 18 and the 12th term is 46. Find the first term, common difference and sum of the first 20 terms. <span class="marks">[4]</span>
2. In a GP, the first term is 3 and the fourth term is 81. Find the common ratio and the sum of the first five terms. <span class="marks">[4]</span>
3. Solve $2x^2-7x+3=0$ and state the nature of its roots. <span class="marks">[3]</span>
4. Use the inverse-matrix method to solve $2x+y=7$ and $x-y=2$. <span class="marks">[4]</span>

::: note Solutions
**1.** Let first term $=a$ and common difference $=d$. $a+4d=18$ and $a+11d=46$. Subtracting gives $7d=28$, so $d=4$ and $a=2$. $S_{20}=\frac{20}{2}[2(2)+19(4)]=10(80)=$ **800**.

**2.** $ar^3=81$, so $3r^3=81$ and $r=3$. $S_5=\frac{3(3^5-1)}{3-1}=\frac{3(243-1)}2=$ **363**.

**3.** $2x^2-7x+3=(2x-1)(x-3)=0$. Hence **$x=\frac12,3$**. Also $D=(-7)^2-4(2)(3)=25>0$, so the roots are real and distinct.

**4.** Let the coefficient matrix have first row $(2,1)$ and second row $(1,-1)$. Its determinant is $2(-1)-1(1)=-3$, so the inverse exists. The inverse has rows $(\frac13,\frac13)$ and $(\frac13,-\frac23)$. Multiplying it by the constants $(7,2)$ gives $x=\frac73+\frac23=3$ and $y=\frac73-\frac43=1$. Therefore **$x=3,y=1$**.
:::

::: caution Matrix notation in the PDF
If your printed copy shows matrix entries as a row, write the same calculation in a bracketed two-by-two arrangement in your answer book. The mathematical method is unchanged: determinant first, then inverse, then multiplication.
:::

## 18.2 Trigonometry and coordinate geometry

5. Prove that $\frac{1-\cos2A}{\sin2A}=\tan A$, where both sides are defined. <span class="marks">[3]</span>
6. From a point 20 m from the foot of a tower, the angle of elevation of the top is $30^\circ$. Find the height of the tower. <span class="marks">[3]</span>
7. Find the acute angle between $3x-4y+7=0$ and $4x+3y-2=0$. <span class="marks">[3]</span>
8. Find the equation of the circle with centre $(2,-1)$ and passing through $(5,3)$. <span class="marks">[3]</span>
9. Show that vectors $\mathbf a=2\mathbf i-\mathbf j+2\mathbf k$ and $\mathbf b=\mathbf i+2\mathbf j$ are perpendicular. <span class="marks">[2]</span>

::: note Solutions
**5.** Use $1-\cos2A=2\sin^2A$ and $\sin2A=2\sin A\cos A$. Therefore $\frac{1-\cos2A}{\sin2A}=\frac{2\sin^2A}{2\sin A\cos A}=\frac{\sin A}{\cos A}=\tan A$. Proved.

**6.** Draw a right triangle, with height $h$ opposite $30^\circ$ and base 20 m. $\tan30^\circ=\frac h{20}$, so $\frac1{\sqrt3}=\frac h{20}$. Hence **$h=\frac{20}{\sqrt3}=\frac{20\sqrt3}{3}$ m**, about 11.55 m.

**7.** Slopes are $m_1=\frac34$ and $m_2=-\frac43$. Their product is $-1$; therefore the lines are perpendicular and the acute angle is **$90^\circ$**.

**8.** Radius squared is $(5-2)^2+(3+1)^2=9+16=25$. Thus the equation is **$(x-2)^2+(y+1)^2=25$**.

**9.** $\mathbf a\cdot\mathbf b=2(1)+(-1)(2)+2(0)=0$. Since both vectors are non-zero and their dot product is zero, they are **perpendicular**.
:::

## 18.3 Graphs, transformation and continuity

10. Sketch $y=x^2-4x+3$. State its vertex and intercepts. <span class="marks">[4]</span>
11. Maximise $Z=3x+2y$ subject to $x+y\le6$, $x\le4$, $y\le3$, $x\ge0$, $y\ge0$. <span class="marks">[4]</span>
12. Under the transformation rule $(x,y)\mapsto(-y,x)$, find the images of $A(2,1)$ and $B(-1,3)$. Name the transformation. <span class="marks">[3]</span>
13. A function has value $2x+k$ when $x<1$, value 5 when $x=1$, and value $x^2+1$ when $x>1$. Can any value of $k$ make it continuous at $x=1$? <span class="marks">[3]</span>

::: note Solutions
**10.** Factor: $y=(x-1)(x-3)$, so the $x$-intercepts are **$(1,0)$** and **$(3,0)$**. At $x=0$, $y=3$, so $y$-intercept is **$(0,3)$**. Axis is midway between roots, $x=2$; $y=4-8+3=-1$, so vertex is **$(2,-1)$**. The coefficient of $x^2$ is positive, so draw an upward-opening parabola through these points.

**11.** The feasible vertices are $(0,0),(4,0),(4,2),(3,3),(0,3)$. Values of $Z$ are 0, 12, 16, 15 and 6 respectively. Therefore the maximum is **$Z=16$ at $(4,2)$**.

**12.** The rule is $(x,y)\mapsto(-y,x)$. Thus $A'=$ **$(-1,2)$** and $B'=$ **$(-3,-1)$**. This is a rotation of **$90^\circ$ anticlockwise about the origin**.

**13.** Right limit $=1^2+1=2$. For continuity it must equal $f(1)=5$, but it does not. Therefore **no value of $k$** can make this function continuous at $x=1. This is exactly why both one-sided limits must be checked before solving for a parameter.
:::

## 18.4 Statistics and functions

14. For the values 2, 4, 6, 8, 10, find the mean, mean deviation about the mean and standard deviation. <span class="marks">[4]</span>
15. The marks of two students are: A: mean 60, standard deviation 6; B: mean 72, standard deviation 9. Who is more consistent? <span class="marks">[2]</span>
16. Find the domain and range of $f(x)=\frac1{x-2}$. <span class="marks">[2]</span>
17. Use the remainder theorem to find the remainder when $2x^3-3x^2+4x-5$ is divided by $x+1$. <span class="marks">[2]</span>
18. If $f(x)=2x-1$ and $g(x)=x^2$, find $(g\circ f)(3)$ and $(f\circ g)(3)$. Explain why they differ. <span class="marks">[3]</span>

::: note Solutions
**14.** Mean $=\frac{2+4+6+8+10}{5}=6$. Absolute deviations are 4, 2, 0, 2, 4; their sum is 12, so $MD=\frac{12}{5}=$ **2.4**. Squared deviations are 16, 4, 0, 4, 16; their sum is 40, so $\sigma=\sqrt{\frac{40}{5}}=\sqrt8=$ **$2\sqrt2$**, about 2.83.

**15.** $CV_A=\frac6{60}\times100=10\%$. $CV_B=\frac9{72}\times100=12.5\%$. Student **A** is more consistent because the coefficient of variation is smaller.

**16.** The denominator cannot be zero, so domain is **all real $x$ except 2**. The fraction can never be zero, so range is **all real $y$ except 0**.

**17.** For divisor $x+1=x-(-1)$, remainder is $f(-1)=2(-1)^3-3(-1)^2+4(-1)-5=-2-3-4-5=$ **$-14$**.

**18.** $f(3)=5$, then $g(5)=25$, so $(g\circ f)(3)=$ **25**. $g(3)=9$, then $f(9)=17$, so $(f\circ g)(3)=$ **17**. They differ because composition order matters; generally $g\circ f\ne f\circ g$.
:::

## Chapter summary

- Sequences: identify $a,d$ or $a,r$ before choosing a term or sum formula.
- Quadratics: factor if possible, then use the discriminant to state the nature of roots.
- Coordinate geometry: convert to slope or centre-radius form before interpreting a line or circle.
- Graphs: list intercepts, vertex/turning point, axis and opening direction before sketching.
- Linear programming: the answer is a point **and** the value of the objective function.
- Statistics: compare consistency using CV, not the standard deviation alone when means differ.
- Functions: treat domain restrictions and order of composition as part of the question, not a final afterthought.

## Practice questions

1. Find the equation of the line through $(2,5)$ perpendicular to $3x+4y-1=0$. <span class="marks">[3]</span>
2. A function has $f(x)=x^2-4$. Find $f^{-1}(5)$ as a set of possible inputs, and explain why the unrestricted function has no inverse function over all real numbers. <span class="marks">[3]</span>

::: note Answers
**1.** Given line has slope $-\frac34$, so a perpendicular slope is $\frac43$. $y-5=\frac43(x-2)$. Thus **$4x-3y+7=0$**.

**2.** $x^2-4=5\Rightarrow x^2=9$, so $f^{-1}(5)$ as inputs is **$\{-3,3\}$**. The unrestricted parabola is not one-one: $f(-3)=f(3)$, so it fails the horizontal-line test and cannot have an inverse function without restricting its domain.
:::
