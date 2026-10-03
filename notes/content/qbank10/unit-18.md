---
subject: Question Bank
grade: 10
unit: 18
title: "Optional Mathematics: Unit-wise Subjective Question Bank"
hours: 0
area: Optional Mathematics
---

Group A is ten single marks. The other **65 marks** of the Optional Mathematics
paper come from Groups B, C and D, and here the marks are won by *method*, not
by recall: a 3-mark item is looking for three visible steps, and a 4-mark item
for four or five. This chapter works through the twelve units of the syllabus in
that order, giving each one a fully worked model question plus a graded set of
two-, three- and four-mark questions with complete solutions.

::: key How to use this bank
Read the worked model at the head of each unit first, then close the book and
write the questions out. Mark yourself against the solutions **by method
step**, not by final answer: in the real paper a right answer with no working
loses most of the method marks, and a wrong slip carried through correct working
keeps them. Two-mark items should take two minutes, three-mark items four
minutes, four-mark items six minutes.
:::

::: caution Practice items, not past questions
Every question below is an original **practice** item written to the CDC
pattern. None is claimed to have appeared in a particular year's paper. All
numerical answers were recomputed independently before being written down, and
each one is followed by the check that proves it.
:::

```figure caption="Where the 75 marks sit and how long each group should take. The three-mark group is nearly half the paper, which is why a practised four-minute rhythm for 3-mark items matters more than speed in Group A."
import matplotlib.pyplot as plt
groups = ["A (10 x 1)", "B (8 x 2)", "C (11 x 3)", "D (4 x 4)"]
marks = [10, 16, 33, 16]
minutes = [10, 24, 88, 40]
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(5.0, 2.6))
ax1.bar(range(4), marks, color=[INK, MUTED, ACCENT, SERIES[1]], width=0.6)
ax1.set_xticks(range(4)); ax1.set_xticklabels(["A", "B", "C", "D"], fontsize=8)
ax1.set_ylabel("marks", fontsize=8)
ax1.set_title("marks (of 75)", fontsize=8.5, color=INK)
ax2.bar(range(4), minutes, color=[INK, MUTED, ACCENT, SERIES[1]], width=0.6)
ax2.set_xticks(range(4)); ax2.set_xticklabels(["A", "B", "C", "D"], fontsize=8)
ax2.set_ylabel("minutes", fontsize=8)
ax2.set_title("time (of 180 min)", fontsize=8.5, color=INK)
for ax in (ax1, ax2):
    ax.tick_params(labelsize=8, length=0)
    ax.spines[["top", "right"]].set_visible(False)
    ax.yaxis.grid(True, color=GRID, lw=0.6)
    ax.set_axisbelow(True)
fig.tight_layout()
```

## 18.1 Sequence and Series

::: example Model question: the arithmetic mean and the geometric mean
**Problem.** The arithmetic mean of two positive numbers is 10 and their
geometric mean is 8. Find the numbers, and find the sum to infinity of the
geometric sequence they begin.

**Solution.** Write the numbers as $a$ and $b$. The arithmetic mean gives
$\frac{a+b}{2}=10$, so $a+b=20$; the geometric mean gives $\sqrt{ab}=8$, so
$ab=64$. A pair of numbers whose sum and product are known are the roots of
$t^2-20t+64=0$. Factorising, $(t-16)(t-4)=0$, so the numbers are **16 and 4**.

The geometric sequence 16, 4, 1, ... has first term $a=16$ and common ratio
$r=\frac{4}{16}=\frac14$. Since $|r|<1$ the sum to infinity is

$$S_\infty=\frac{a}{1-r}=\frac{16}{1-\frac14}=\frac{16}{\frac34}=\frac{64}{3}
=21\frac13\approx21.33$$

**Check.** The partial sums must climb towards $21\frac13$: the first four terms
already give $16+4+1+0.25=21.25$, and everything left over is less than
$0.09$. So $21.33$ is right.
:::

1. Find the 15th term of the arithmetic sequence 7, 11, 15, ... <span class="marks">[2]</span>
2. Which term of the sequence 5, 9, 13, ... is 81? <span class="marks">[2]</span>
3. Insert four arithmetic means between 3 and 23. <span class="marks">[3]</span>
4. Find the sum of the first 25 terms of 4, 9, 14, ... <span class="marks">[3]</span>
5. The third term of a geometric sequence is 24 and the sixth is 192. Find the
   sequence and the sum of its first 8 terms. <span class="marks">[4]</span>
6. Two positive numbers have arithmetic mean 12 and geometric mean
   $6\sqrt{2}$. Find the numbers. <span class="marks">[4]</span>

::: note Solutions to 18.1
**1.** $a=7$, $d=4$, so $t_{15}=7+14\times4=63$.
**2.** $81=5+(n-1)4$, so $n-1=19$ and the term is the **20th**.
**3.** The five gaps between 3 and 23 total 20, so each gap is $d=4$: the means
   are **7, 11, 15, 19**.
**4.** $a=4$, $d=5$, $S_{25}=\frac{25}{2}\{8+24\times5\}=\frac{25}{2}\times128=1600$.
**5.** $\frac{t_6}{t_3}=r^3=\frac{192}{24}=8$, so $r=2$ and $a=\frac{24}{4}=6$; the
   sequence is **6, 12, 24, ...** and
   $S_8=\frac{6(2^8-1)}{2-1}=6\times255=1530$.
**6.** $a+b=24$ and $ab=(6\sqrt{2})^2=72$; the roots of $t^2-24t+72=0$ are
   $t=\frac{24\pm\sqrt{576-288}}{2}=\frac{24\pm\sqrt{288}}{2}=\frac{24\pm12\sqrt{2}}{2}
   =12\pm6\sqrt{2}$. The numbers are $12+6\sqrt{2}$ and $12-6\sqrt{2}$; check the
   product: $(12)^2-(6\sqrt{2})^2=144-72=72$.
:::

## 18.2 Quadratic Equations and Graphs

::: example Model question: where a line meets a parabola
**Problem.** Solve the pair of equations $y=x^2-3x+2$ and $y=x+2$
simultaneously, and state what the two solutions mean on the graph.

**Solution.** Both expressions equal $y$, so equate them:

$$x^2-3x+2=x+2\;\Longrightarrow\;x^2-4x=0\;\Longrightarrow\;x(x-4)=0$$

so $x=0$ or $x=4$. Substituting back into the line $y=x+2$: at $x=0$, $y=2$; at
$x=4$, $y=6$. The solutions are therefore $(0,2)$ and $(4,6)$.

**What it means.** Each solution is a point where the straight line and the
parabola cross, so the line cuts the curve in two places. The number of
crossings is decided by the discriminant of the combined quadratic: here
$x^2-4x=0$ has $D=16>0$, so two real intersections, agreeing with the algebra.

**Check.** At $x=4$ the parabola gives $16-12+2=6$ and the line gives 6. At
$x=0$ both give 2.
:::

1. Solve $x^2-7x+12=0$. <span class="marks">[2]</span>
2. Find the value of $k$ for which $2x^2+kx+8=0$ has equal roots.
   <span class="marks">[2]</span>
3. If $\alpha$ and $\beta$ are the roots of $2x^2-5x+3=0$, find
   $\frac{\alpha}{\beta}+\frac{\beta}{\alpha}$. <span class="marks">[3]</span>
4. Solve $x^2+2x-8=0$ and state the coordinates of the vertex and the equation
   of the line of symmetry of the graph. <span class="marks">[3]</span>
5. For what values of $p$ does $x^2+px+9=0$ have (i) equal roots, (ii) no real
   roots? <span class="marks">[4]</span>
6. The sum of a number and its reciprocal is $\frac{10}{3}$. Find the number.
   <span class="marks">[4]</span>

::: note Solutions to 18.2
**1.** $(x-3)(x-4)=0$, so $x=3$ or $x=4$.
**2.** Equal roots need $D=0$: $k^2-4\times2\times8=0$, so $k^2=64$ and
   $k=\pm8$.
**3.** $\alpha+\beta=\frac52$ and $\alpha\beta=\frac32$, so
   $\frac{\alpha^2+\beta^2}{\alpha\beta}
   =\frac{(\alpha+\beta)^2-2\alpha\beta}{\alpha\beta}
   =\frac{\frac{25}{4}-3}{\frac32}=\frac{\frac{13}{4}}{\frac32}=\frac{13}{6}$.
**4.** $(x+4)(x-2)=0$ gives roots $x=-4$ and $x=2$; the line of symmetry is the
   midpoint, $x=-1$, and the vertex is $(-1,\,-9)$ because
   $1-2-8=-9$.
**5.** $D=p^2-36$. (i) $D=0$ when $p=\pm6$. (ii) $D<0$ when $p^2<36$, that is
   $-6<p<6$.
**6.** $x+\frac1x=\frac{10}{3}$ gives $3x^2-10x+3=0$, so
   $(3x-1)(x-3)=0$ and the number is **3** (or $\frac13$, its reciprocal —
   the two answers are the same pair).
:::

## 18.3 Matrices and Determinants

```figure caption="The inverse of a $2\times2$ matrix, written out. The determinant divides every entry, so the inverse exists only when the determinant is not zero."
fig = mateq(["$A^{-1} =$", "$\\frac{1}{ad-bc}$", [["$d$", "$-b$"], ["$-c$", "$a$"]]])
```

::: example Model question: the matrix method end to end
**Problem.** Solve $2x+3y=13$ and $x+2y=8$ by the matrix method, and check the
answer in both equations.

**Solution.** Write the system as $AX=B$, where $A$ has rows $(2,3)$ and $(1,2)$,
$X$ is the column of unknowns and $B$ is the column $(13,8)$. The determinant of
$A$ is $|A|=2\times2-3\times1=4-3=1$, which is not zero, so the inverse exists:
$A^{-1}=\frac{1}{1}$ times the matrix with rows $(2,-3)$ and $(-1,2)$. Then

$$X=A^{-1}B\;\Longrightarrow\;x=2\times13-3\times8=26-24=2$$

$$y=-1\times13+2\times8=-13+16=3$$

**Check.** $2(2)+3(3)=4+9=13$ and $2+2(3)=8$. Both hold, so $x=2$, $y=3$.
:::

1. If $A$ has rows $(2,5)$ and $(1,3)$, find $|A|$ and $A^{-1}$.
   <span class="marks">[2]</span>
2. Solve by Cramer's rule: $3x+2y=7$, $2x-y=0$. <span class="marks">[2]</span>
3. If $A$ has rows $(1,2)$, $(3,4)$ and $B$ has rows $(2,1)$, $(1,3)$, find $AB$
   and verify that $|AB|=|A||B|$. <span class="marks">[3]</span>
4. Solve by the matrix method: $x+y=5$, $2x-y=1$. <span class="marks">[3]</span>
5. Find the value of $k$ for which the matrix with rows $(k,3)$ and $(4,6)$ has
   no inverse. <span class="marks">[4]</span>
6. A shop sells pens at Rs 15 and copies at Rs 40. Ramesh bought 7 items and
   paid Rs 205. Set the problem up as a matrix equation and solve it.
   <span class="marks">[4]</span>

::: note Solutions to 18.3
**1.** $|A|=6-5=1$; $A^{-1}$ has rows $(3,-5)$ and $(-1,2)$.
**2.** $D=3(-1)-2(2)=-7$; $D_x=7(-1)-2(0)=-7$, so $x=1$; $D_y=3(0)-2(7)=-14$,
   so $y=2$. Check: $3+4=7$ and $2-2=0$.
**3.** $AB$ has rows $(1\times2+2\times1,\;1\times1+2\times3)=(4,7)$ and
   $(3\times2+4\times1,\;3\times1+4\times3)=(10,15)$. Then
   $|AB|=4\times15-7\times10=60-70=-10$, while
   $|A|=4-6=-2$, $|B|=6-1=5$ and $(-2)(5)=-10$. They agree.
**4.** $|A|=1(-1)-1(2)=-3$; the inverse is $-\frac13$ times the matrix with rows
   $(-1,-1)$ and $(-2,1)$, that is rows $\left(\frac13,\frac13\right)$ and
   $\left(\frac23,-\frac13\right)$. Then
   $x=\frac13(5)+\frac13(1)=2$ and $y=\frac23(5)-\frac13(1)=3$. Check:
   $2+3=5$ ✓ and $2(2)-3=1$ ✓.
**5.** No inverse means $|A|=0$: $6k-12=0$, so $k=2$.
**6.** With $p$ pens and $c$ copies, rows $(1,1)$ and $(15,40)$ acting on the
   column $(p,c)$ give the column $(7,205)$. $|A|=40-15=25$; then
   $p=\frac{40\times7-1\times205}{25}=\frac{280-205}{25}=3$ and
   $c=\frac{1\times205-15\times7}{25}=\frac{100}{25}=4$. Check:
   $3+4=7$ items and $3(15)+4(40)=45+160=205$.
:::

::: caution Check both unknowns in both equations
A matrix solution has three places to slip: the sign of the determinant, the
order of the two rows of the inverse, and the order of the multiplication. All
three leave an answer that looks completely reasonable. The cure is thirty
seconds long and always works: **substitute both unknowns back into both
original equations.** In question 4 above, the row order decides whether
$y$ comes out as $3$ or $-3$; only the substitution tells you which.
:::

## 18.4 Trigonometry: Multiple, Submultiple and Transformation Formulas

::: example Model question: an exact value from a compound angle
**Problem.** Find the exact value of $\sin15°$ and use it to find $\sin75°$.

**Solution.** Write $15°=45°-30°$ and use
$\sin(A-B)=\sin A\cos B-\cos A\sin B$:

$$\sin15°=\sin45°\cos30°-\cos45°\sin30°
=\frac{\sqrt{2}}{2}\cdot\frac{\sqrt{3}}{2}-\frac{\sqrt{2}}{2}\cdot\frac12
=\frac{\sqrt{6}-\sqrt{2}}{4}$$

For $\sin75°$ write $75°=45°+30°$:
$\sin75°=\frac{\sqrt{6}+\sqrt{2}}{4}$.

**Check.** $\frac{\sqrt{6}-\sqrt{2}}{4}\approx\frac{2.449-1.414}{4}=0.259$, and
$\sin15°=0.2588$. For 75° the value is about $0.966$, and $\sin75°=0.9659$. Both
hold to three places.
:::

1. If $\sin A=\frac{5}{13}$ and $A$ is acute, find $\cos2A$.
   <span class="marks">[2]</span>
2. If $\tan A=\frac13$, find $\tan2A$. <span class="marks">[2]</span>
3. Prove that $\frac{\sin2A}{1+\cos2A}=\tan A$. <span class="marks">[3]</span>
4. Prove that $\cos20°+\cos100°+\cos140°=0$. <span class="marks">[3]</span>
5. Prove that $\cos^2A+\cos^2(60°+A)+\cos^2(60°-A)=\frac32$.
   <span class="marks">[4]</span>
6. If $\sin A=\frac{3}{5}$ and $\sin B=\frac{5}{13}$, with $A$ and $B$ both
   acute, find $\sin(A+B)$. <span class="marks">[4]</span>

::: note Solutions to 18.4
**1.** $\cos2A=1-2\sin^2A=1-2\cdot\frac{25}{169}=1-\frac{50}{169}=\frac{119}{169}$.
**2.** $\tan2A=\frac{2\tan A}{1-\tan^2A}=\frac{\frac23}{1-\frac19}
   =\frac{\frac23}{\frac89}=\frac34$.
**3.** Take the left side: $\frac{2\sin A\cos A}{1+2\cos^2A-1}
   =\frac{2\sin A\cos A}{2\cos^2A}=\frac{\sin A}{\cos A}=\tan A$. Done.
**4.** $\cos20°+\cos100°=2\cos60°\cos40°=\cos40°$, and then
   $\cos40°+\cos140°=2\cos90°\cos50°=0$ because $\cos90°=0$.
**5.** Use $\cos^2x=\frac{1+\cos2x}{2}$ three times. The left side becomes
   $\frac32+\frac12\{\cos2A+\cos(120°+2A)+\cos(120°-2A)\}$. The bracket is
   $\cos2A+2\cos120°\cos2A=\cos2A-\cos2A=0$, since
   $\cos120°=-\frac12$. So the left side is $\frac32$.
**6.** $\cos A=\frac45$ and $\cos B=\frac{12}{13}$. Then
   $\sin(A+B)=\frac35\cdot\frac{12}{13}+\frac45\cdot\frac{5}{13}
   =\frac{36}{65}+\frac{20}{65}=\frac{56}{65}\approx0.862$. Since
   $A\approx36.87°$ and $B\approx22.62°$, the sum is about $59.5°$, and
   $\sin59.5°\approx0.862$. Holds.
:::

## 18.5 Conditional Identities, Trigonometric Equations and Height and Distance

::: example Model question: two angles of elevation
**Problem.** The angle of elevation of the top of a tower from a point on the
ground is $30°$. After walking 60 m straight towards the tower the elevation
becomes $60°$. Find the height of the tower.

**Solution.** Let $h$ be the height and let $x$ be the horizontal distance from
the second position to the foot of the tower. From the second position,
$\tan60°=\frac{h}{x}$, so $x=\frac{h}{\sqrt{3}}$. From the first position,
$\tan30°=\frac{h}{x+60}$, so $x+60=h\sqrt{3}$. Substituting $x$:

$$\frac{h}{\sqrt{3}}+60=h\sqrt{3}\;\Longrightarrow\;60=h\sqrt{3}-\frac{h}{\sqrt{3}}
=h\cdot\frac{3-1}{\sqrt{3}}=\frac{2h}{\sqrt{3}}$$

so $h=\frac{60\sqrt{3}}{2}=30\sqrt{3}\approx51.96$ m.

**Check.** With $h=30\sqrt{3}$, $x=\frac{30\sqrt{3}}{\sqrt{3}}=30$ m and
$x+60=90$ m. Then $\frac{h}{90}=\frac{51.96}{90}=0.577=\tan30°$ ✓ and
$\frac{h}{30}=1.732=\tan60°$ ✓. The tower is about **51.96 m** high.
:::

1. Find the general solution of $2\sin\theta=1$. <span class="marks">[2]</span>
2. A pole 12 m high casts a shadow $12\sqrt{3}$ m long. Find the elevation of the
   sun. <span class="marks">[2]</span>
3. In a triangle, prove that $\tan A+\tan B+\tan C=\tan A\tan B\tan C$.
   <span class="marks">[3]</span>
4. Prove that $\cos^2A+\cos^2B+\cos^2C+2\cos A\cos B\cos C=1$ when
   $A+B+C=180°$. <span class="marks">[4]</span>
5. From the top of a 20 m building the angle of elevation of the top of a tower
   is $30°$ and the angle of depression of its foot is $45°$. Find the height of
   the tower. <span class="marks">[4]</span>

::: note Solutions to 18.5
**1.** $\sin\theta=\frac12$ has the principal value $\theta=\frac{\pi}{6}$, so
   $\theta=n\pi+(-1)^n\frac{\pi}{6}$ for integral $n$.
**2.** $\tan\theta=\frac{12}{12\sqrt{3}}=\frac{1}{\sqrt{3}}$, so the elevation is
   $30°$.
**3.** $A+B=180°-C$, so
   $\tan(A+B)=-\tan C$. But
   $\tan(A+B)=\frac{\tan A+\tan B}{1-\tan A\tan B}$. Cross-multiplying:
   $\tan A+\tan B=-\tan C(1-\tan A\tan B)
   =-\tan C+\tan A\tan B\tan C$. Adding $\tan C$ to both sides gives the
   identity.
**4.** Put $c=\cos A\cos B$ and $s=\sin A\sin B$. Since $C=180°-(A+B)$ we have
   $\cos C=-\cos(A+B)=-c+s$, and
   $\cos^2C=(c-s)^2=c^2-2cs+s^2$. Also
   $2\cos A\cos B\cos C=2c(-c+s)=-2c^2+2cs$. Adding the left side:

   $$\cos^2A+\cos^2B+(c^2-2cs+s^2)+(-2c^2+2cs)
   =\cos^2A+\cos^2B-c^2+s^2$$

   Now $c^2=\cos^2A\cos^2B$ and $s^2=\sin^2A\sin^2B$, so
   $\cos^2A-c^2=\cos^2A(1-\cos^2B)=\cos^2A\sin^2B$. The expression becomes
   $\cos^2A\sin^2B+\cos^2B+\sin^2A\sin^2B
   =\sin^2B(\cos^2A+\sin^2A)+\cos^2B=\sin^2B+\cos^2B=1$. Done.
**5.** The depression of the foot is $45°$, so the horizontal distance from the
   building to the tower equals the building's height, 20 m. From the same top,
   the elevation of the tower top is $30°$ over that 20 m, so the tower stands
   $20\tan30°=\frac{20}{\sqrt{3}}\approx11.55$ m above the building's top. Height
   $=20+11.55\approx31.55$ m. Check: the angle from the ground point at 45°
   gives exactly 20 m to the building's top ✓.
:::

## 18.6 Angle between Two Lines and Pair of Straight Lines

::: example Model question: the angle between a pair of lines
**Problem.** Show that $6x^2+5xy-6y^2=0$ represents a pair of straight lines
through the origin, find them, and show that they are perpendicular.

**Solution.** The left side factorises as $(3x-2y)(2x+3y)$, since
$6x^2+9xy-4xy-6y^2=6x^2+5xy-6y^2$. Setting each factor to zero gives the two
lines $y=\frac32x$ and $y=-\frac23x$.

Both pass through the origin, so the equation is a pair of straight lines
through the origin. Their slopes multiply to $\frac32\times\left(-\frac23\right)=-1$,
so the lines are perpendicular. This agrees with the coefficient test: for
$ax^2+2hxy+by^2=0$ the lines are perpendicular exactly when $a+b=0$, and here
$6+(-6)=0$.

**Check.** Take a point on the first line, $(2,3)$: $6(4)+5(6)-6(9)=24+30-54=0$ ✓.
Take $(3,-2)$ on the second: $54-30-24=0$ ✓.
:::

1. Find the slope of the line joining $(2,3)$ and $(4,7)$. <span class="marks">[2]</span>
2. Find the angle between the lines whose slopes are $\sqrt{3}$ and
   $\frac{1}{\sqrt{3}}$. <span class="marks">[2]</span>
3. Show that the lines $2x-3y+5=0$ and $3x+2y-7=0$ are perpendicular.
   <span class="marks">[3]</span>
4. Find the angle between the pair of lines $2x^2-5xy+2y^2=0$.
   <span class="marks">[3]</span>
5. Find the separate equations of the lines represented by
   $x^2-4xy+3y^2=0$, and the angle between them.
   <span class="marks">[4]</span>

::: note Solutions to 18.6
**1.** $m=\frac{7-3}{4-2}=2$.
**2.** $\tan\theta=\left|\frac{\sqrt{3}-\frac{1}{\sqrt{3}}}{1+1}\right|
   =\frac{\frac{2}{\sqrt{3}}}{2}=\frac{1}{\sqrt{3}}$, so $\theta=30°$.
**3.** The slopes are $\frac23$ and $-\frac32$; their product is $-1$, so the
   lines are perpendicular.
**4.** Factorise: $(2x-y)(x-2y)=0$, so the slopes are 2 and $\frac12$. Then
   $\tan\theta=\left|\frac{2-\frac12}{1+1}\right|=\frac34$, so
   $\theta=\tan^{-1}\frac34\approx36.87°$.
**5.** $(x-y)(x-3y)=0$, so the lines are $y=x$ and $y=3x$. Then
   $\tan\theta=\left|\frac{1-3}{1+3}\right|=\frac12$, so
   $\theta\approx26.57°$.
:::

## 18.7 Conic Sections and Circle

::: example Model question: the circle through three points
**Problem.** Find the equation, centre and radius of the circle through
$(0,0)$, $(1,0)$ and $(0,1)$.

**Solution.** Let the circle be
$x^2+y^2+2gx+2fy+c=0$. Putting $(0,0)$ gives $c=0$. Putting $(1,0)$ gives
$1+2g=0$, so $g=-\frac12$. Putting $(0,1)$ gives $1+2f=0$, so $f=-\frac12$.
The equation is therefore

$$x^2+y^2-x-y=0$$

The centre is $(-g,-f)=\left(\frac12,\frac12\right)$ and the radius is
$\sqrt{g^2+f^2-c}=\sqrt{\frac14+\frac14}=\frac{1}{\sqrt{2}}\approx0.707$.

**Check.** The distance from the centre $\left(\frac12,\frac12\right)$ to
$(0,0)$ is $\sqrt{\frac14+\frac14}=0.707$ ✓; to $(1,0)$ it is
$\sqrt{\frac14+\frac14}=0.707$ ✓. All three points lie on the same circle.
:::

1. Find the centre and radius of $x^2+y^2-4x+6y-12=0$. <span class="marks">[2]</span>
2. Write the equation of the circle with centre $(2,-3)$ and radius 5.
   <span class="marks">[2]</span>
3. Find the equation of the circle on the line joining $A(1,2)$ and $B(5,6)$ as
   diameter. <span class="marks">[3]</span>
4. Show that $x^2+y^2-2x-4y+5=0$ represents a single point, and find it.
   <span class="marks">[3]</span>
5. Find the equation of the circle passing through the origin with centre
   $(3,-4)$, and find its radius. <span class="marks">[4]</span>

::: note Solutions to 18.7
**1.** $g=-2$, $f=3$, so the centre is $(2,-3)$ and the radius is
   $\sqrt{4+9+12}=5$.
**2.** $(x-2)^2+(y+3)^2=25$, that is
   $x^2+y^2-4x+6y-12=0$.
**3.** The centre is the midpoint $(3,4)$ and
   $r=\frac12\sqrt{(5-1)^2+(6-2)^2}=\frac12\sqrt{32}=2\sqrt{2}$, so
   $(x-3)^2+(y-4)^2=8$.
**4.** $g=-1$, $f=-2$, $c=5$; then
   $r^2=g^2+f^2-c=1+4-5=0$. A radius of zero means the circle has collapsed to
   its centre, $(1,2)$.
**5.** The radius is the distance from $(3,-4)$ to the origin,
   $\sqrt{9+16}=5$. The equation is $(x-3)^2+(y+4)^2=25$, that is
   $x^2+y^2-6x+8y=0$. Check: putting the origin gives $0=0$ ✓.
:::

## 18.8 Vector

::: example Model question: proving an angle and a collinearity
**Problem.** (a) Find the angle between $\vec a=\hat i+\hat j$ and
$\vec b=\hat i$. (b) Show that $A(1,2)$, $B(3,6)$ and $C(4,8)$ are collinear.

**Solution.** (a) $\vec a\cdot\vec b=1\times1+1\times0=1$, $|\vec a|=\sqrt{2}$ and
$|\vec b|=1$, so $\cos\theta=\frac{1}{\sqrt{2}}$ and $\theta=45°$.

(b)
$\overrightarrow{AB}=(3-1)\hat i+(6-2)\hat j=2\hat i+4\hat j$ and
$\overrightarrow{BC}=(4-3)\hat i+(8-6)\hat j=\hat i+2\hat j$. Since
$\overrightarrow{AB}=2\,\overrightarrow{BC}$, the two vectors are parallel, and
they share the point $B$. Two parallel segments with a common point lie on one
straight line, so the three points are collinear.

**Check.** The line through $A(1,2)$ and $B(3,6)$ has slope
$\frac{6-2}{3-1}=2$, and at $x=4$ it gives $y=2+2(4-1)=8$, which is $C$. ✓
:::

1. If $\vec a=3\hat i-2\hat j$ and $\vec b=\hat i+5\hat j$, find
   $\vec a\cdot\vec b$. <span class="marks">[2]</span>
2. Find $x$ if $2\hat i+3\hat j$ and $x\hat i+6\hat j$ are parallel.
   <span class="marks">[2]</span>
3. Find the angle between $\vec a=2\hat i+2\hat j$ and
   $\vec b=2\hat i-2\hat j$. <span class="marks">[3]</span>
4. Prove that $(\vec a+\vec b)\cdot(\vec a-\vec b)=|\vec a|^2-|\vec b|^2$ in
   component form. <span class="marks">[3]</span>
5. The position vectors of $A$ and $B$ are $2\hat i+\hat j$ and
   $6\hat i+5\hat j$. Find the position vector of the point that divides $AB$
   internally in the ratio $1:3$. <span class="marks">[4]</span>

::: note Solutions to 18.8
**1.** $3(1)+(-2)(5)=3-10=-7$.
**2.** Parallel needs $\frac{2}{x}=\frac{3}{6}$, so $x=4$.
**3.** $\vec a\cdot\vec b=4-4=0$, and neither vector is zero, so the angle is
   $90°$.
**4.** With $\vec a=(a_1,a_2)$ and $\vec b=(b_1,b_2)$, the left side is
   $(a_1+b_1)(a_1-b_1)+(a_2+b_2)(a_2-b_2)
   =a_1^2-b_1^2+a_2^2-b_2^2=|\vec a|^2-|\vec b|^2$. Done.
**5.** The point is $\frac{1\vec b+3\vec a}{1+3}
   =\frac{(6\hat i+5\hat j)+3(2\hat i+\hat j)}{4}
   =\frac{12\hat i+8\hat j}{4}=3\hat i+2\hat j$.
   Check: it lies on $AB$ since $A(2,1)$, $P(3,2)$, $B(6,5)$ all have slope 1.
:::

## 18.9 Linear Programming and Transformation

::: example Model question: a maximum at a corner
**Problem.** Maximise $z=5x+4y$ subject to $x+y\leq 8$, $2x+y\leq 10$, $x\geq 0$,
$y\geq 0$.

**Solution.** Draw the two constraint lines and shade the region that satisfies
all four inequalities. Its corners are where the boundary lines meet:

- $(0,0)$ from the two axes;
- $(5,0)$ where $2x+y=10$ meets the $x$-axis;
- $(0,8)$ where $x+y=8$ meets the $y$-axis;
- $(2,6)$ where $x+y=8$ and $2x+y=10$ meet (subtracting gives $x=2$, then
  $y=6$).

Evaluate $z$ at each corner:

$$z(0,0)=0,\quad z(5,0)=25,\quad z(0,8)=32,\quad z(2,6)=10+24=34$$

The largest value is $z=34$, at $x=2$, $y=6$.

**Check.** Both constraints hold at $(2,6)$: $2+6=8\leq 8$ ✓ and
$4+6=10\leq 10$ ✓. Moving anywhere inside the region from that corner reduces
$z$, because both constraint boundaries are active there.
:::

1. Find the image of the point $(2,-3)$ under the transformation with matrix
   rows $(0,1)$ and $(1,0)$. <span class="marks">[2]</span>
2. Find the image of $(4,1)$ under the matrix with rows $(2,0)$ and $(0,3)$,
   and name the transformation. <span class="marks">[2]</span>
3. Maximise $z=3x+2y$ subject to $x+y\leq 4$, $x\geq 0$, $y\geq 0$.
   <span class="marks">[3]</span>
4. A point $P$ is 3 cm from the centre of an inversion circle of radius 6 cm.
   Find $OP'$ and say where $P'$ lies. <span class="marks">[3]</span>
5. A workshop makes chairs and tables. Each chair needs 2 hours of carpentry and
   earns Rs 300; each table needs 3 hours and earns Rs 500. Only 30 carpenter
   hours are available and at most 12 pieces can be stored. How many of each
   maximise the earning? <span class="marks">[4]</span>

::: note Solutions to 18.9
**1.** $(0\times2+1\times(-3),\;1\times2+0\times(-3))=(-3,2)$.
**2.** $(2\times4,\;3\times1)=(8,3)$; the transformation is an enlargement
   (stretch) of factor 2 along $x$ and 3 along $y$.
**3.** Corners $(0,0)$, $(4,0)$, $(0,4)$; $z$ values 0, 12, 8. Maximum
   $z=12$ at $(4,0)$.
**4.** $OP\cdot OP'=k^2$ gives $OP'=\frac{36}{3}=12$ cm, on the ray $OP$ but
   beyond the circle, on the far side of the inversion circle.
**5.** Let $x$ chairs and $y$ tables. Maximise $z=300x+500y$ subject to
   $2x+3y\leq 30$ and $x+y\leq12$. Corners: $(0,0)$; $(12,0)$ from $x+y=12$;
   $(0,10)$ from $2x+3y=30$; and the intersection of the two lines, where
   $y=12-x$ gives $2x+36-3x=30$, so $x=6$, $y=6$. Values:
   $z(12,0)=3600$, $z(0,10)=5000$, $z(6,6)=1800+3000=4800$. The best is
   **10 tables and no chairs**, earning Rs 5000. Check:
   $2(0)+3(10)=30$ hours ✓ and $0+10\leq12$ ✓.
:::

```figure caption="The feasible region of a two-variable linear programme is always a convex polygon, and the best value of a linear objective always sits on one of its corners — no need to search the interior."
import matplotlib.pyplot as plt
import numpy as np
fig, ax = plt.subplots(figsize=(4.6, 2.9))
x = np.linspace(0, 11, 200)
ax.plot(x, 10 - 2*x, color=ACCENT, lw=1.6)
ax.plot(x, 8 - x, color=SERIES[1], lw=1.6)
ax.fill([0, 5, 2, 0], [0, 0, 6, 8], color=ACCENT, alpha=0.13)
ax.plot([0, 5, 2, 0], [0, 0, 6, 8], "o", color=INK, ms=4)
for px, py, name in [(0, 0, "(0,0)"), (5, 0, "(5,0)"), (2, 6, "(2,6)"), (0, 8, "(0,8)")]:
    ax.annotate(name, (px, py), xytext=(px + 0.25, py + 0.35), fontsize=8, color=INK)
ax.text(4.6, 1.1, "$2x+y=10$", fontsize=8, color=ACCENT)
ax.text(0.25, 7.3, "$x+y=8$", fontsize=8, color=SERIES[1])
ax.set_xlim(-0.4, 6.5); ax.set_ylim(-0.6, 9.5)
ax.set_xlabel("x", fontsize=9); ax.set_ylabel("y", fontsize=9)
ax.tick_params(labelsize=8, length=0)
ax.spines[["top", "right"]].set_visible(False)
ax.grid(True, color=GRID, lw=0.6)
ax.set_axisbelow(True)
fig.tight_layout()
```

## 18.10 Continuity

::: example Model question: removing a gap
**Problem.** The function $f(x)=\frac{x^2-4}{x-2}$ is not defined at $x=2$.
Find $\lim_{x\to2}f(x)$, say what kind of discontinuity this is, and give the
value that would make the function continuous there.

**Solution.** Factorise the numerator: $x^2-4=(x-2)(x+2)$. For every $x\ne2$,
the factor $x-2$ cancels and

$$f(x)=x+2$$

so $\lim_{x\to2}f(x)=4$. The limit exists and is finite, but $f(2)$ is
undefined, so the graph is the line $y=x+2$ with a single missing point at
$(2,4)$. That is a **removable discontinuity**. Defining $f(2)=4$ fills the
hole and makes the function continuous at $x=2$.

**Check.** Take $x=1.999$: $\frac{3.996-4}{-0.001}=\frac{-0.004}{-0.001}=4$ ✓;
take $x=2.001$: $\frac{0.004}{0.001}=4$ ✓. Both sides approach 4.
:::

1. Evaluate $\lim_{x\to2}\frac{x^2-4}{x-2}$. <span class="marks">[2]</span>
2. Evaluate $\lim_{x\to0}\frac{3x^2+2x}{x}$. <span class="marks">[2]</span>
3. Test the continuity of $f(x)=\frac{x^2-1}{x-1}$ at $x=1$, and say what kind
   of discontinuity it has. <span class="marks">[3]</span>
4. Find $k$ so that $f$ is continuous at $x=3$, where
   $f(x)=\frac{x^2-9}{x-3}$ for $x\ne3$ and $f(3)=k$.
   <span class="marks">[3]</span>
5. A function is defined by $f(x)=2x+1$ for $x<1$, $f(x)=5$ for $x=1$ and
   $f(x)=3x-1$ for $x>1$. Show that it has a jump discontinuity at $x=1$, and
   draw the two one-sided limits. <span class="marks">[4]</span>

::: note Solutions to 18.10
**1.** Cancel: $x+2\to4$.
**2.** Divide by $x$: $3x+2\to2$.
**3.** Cancelling gives $x+1$, so the limit at $x=1$ is 2, but $f(1)$ is
   undefined: a **removable** discontinuity.
**4.** $\frac{(x-3)(x+3)}{x-3}=x+3\to6$, so $k=6$.
**5.** As $x\to1^-$, $f\to2(1)+1=3$; as $x\to1^+$, $f\to3(1)-1=2$; and
   $f(1)=5$. The left limit (3), the right limit (2) and the value (5) are
   three different numbers, so the graph jumps at $x=1$. It is a jump
   discontinuity, and it cannot be repaired by changing $f$ at one point alone.
:::

## 18.11 Statistics: Measures of Dispersion

::: example Model question: which player is more consistent?
**Problem.** In ten matches a batsman scores a mean of 45 with a standard
deviation of 9; a second batsman has a mean of 30 with a standard deviation of
3. Which batsman is more consistent?

**Solution.** Consistency means small spread **relative to the size of the
scores**, which is what the coefficient of variation measures:

$$\text{CV}=\frac{\sigma}{\bar x}\times100\%$$

For the first batsman, $\text{CV}=\frac{9}{45}\times100=20\%$. For the second,
$\text{CV}=\frac{3}{30}\times100=10\%$. The second batsman has the smaller
coefficient of variation, so **the second batsman is more consistent**, even
though his scores are lower.

**Check.** The comparison is fair because both CVs are percentages of their own
means. Comparing the raw standard deviations (9 against 3) would have said the
same thing here, but it would mislead whenever the means differ a lot — which is
exactly why the coefficient exists.
:::

1. Find the range and the mean deviation from the mean of 3, 5, 7, 9.
   <span class="marks">[2]</span>
2. Find the standard deviation of 4, 8, 10, 12, 16. <span class="marks">[2]</span>
3. For a distribution the mean is 25 and the standard deviation is 5. Find the
   coefficient of variation. <span class="marks">[3]</span>
4. If $Q_1=18$ and $Q_3=42$, find the quartile deviation and its coefficient.
   <span class="marks">[3]</span>
5. The marks of two students in five tests are: A — 60, 64, 58, 66, 62;
   B — 48, 52, 50, 54, 51. Compare their consistency using the coefficient of
   variation. <span class="marks">[4]</span>

::: note Solutions to 18.11
**1.** Range $=9-3=6$. Mean $=6$, deviations are $-3,-1,1,3$, so the mean
   deviation is $\frac{3+1+1+3}{4}=2$.
**2.** Mean $=10$; deviations $-6,-2,0,2,6$; sum of squares
   $=36+4+0+4+36=80$; variance $=\frac{80}{5}=16$; $\sigma=4$.
**3.** $\frac{5}{25}\times100=20\%$.
**4.** Quartile deviation $=\frac{42-18}{2}=12$; its coefficient is
   $\frac{Q_3-Q_1}{Q_3+Q_1}=\frac{24}{60}=0.4$.
**5.** A: mean $=\frac{310}{5}=62$, deviations $-2,2,-4,4,0$, sum of squares
   $=40$, variance $=8$, $\sigma_A=\sqrt{8}\approx2.83$, CV
   $=\frac{2.83}{62}\times100\approx4.56\%$. B: mean $=51$, deviations
   $-3,1,-1,3,0$, sum of squares $=20$, variance $=4$, $\sigma_B=2$, CV
   $=\frac{2}{51}\times100\approx3.92\%$. B has the smaller CV, so **B is more
   consistent**.
:::

## 18.12 Functions and Polynomials

::: example Model question: an inverse function and its check
**Problem.** The function $f(x)=\frac{2x+1}{x-2}$ is defined for $x\ne2$. Find
$f^{-1}(x)$ and verify that $f(f^{-1}(x))=x$.

**Solution.** Put $y=\frac{2x+1}{x-2}$ and solve for $x$. Multiply both sides by
$x-2$: $y(x-2)=2x+1$, so $xy-2y=2x+1$. Gather the $x$ terms:
$x(y-2)=1+2y$, giving

$$f^{-1}(x)=\frac{1+2x}{x-2}$$

**Verify.** $f(f^{-1}(x))
=\frac{2\cdot\frac{1+2x}{x-2}+1}{\frac{1+2x}{x-2}-2}$. Multiply top and bottom
by $x-2$: the top becomes $2(1+2x)+(x-2)=4x+2+x-2=5x$, and the bottom becomes
$(1+2x)-2(x-2)=1+2x-2x+4=5$. The ratio is $x$, as required.

**Check with a number.** $f(0)=\frac{1}{-2}=-0.5$, and
$f^{-1}(-0.5)=\frac{1-1}{-2.5}=0$ ✓.
:::

1. If $f(x)=x^2-3x+2$, find $f(-1)$. <span class="marks">[2]</span>
2. Find the domain of $f(x)=\sqrt{x-3}$. <span class="marks">[2]</span>
3. If $f(x)=2x+1$ and $g(x)=x^2$, find $(f\circ g)(x)$ and $(g\circ f)(x)$.
   <span class="marks">[3]</span>
4. Find the remainder when $x^4-3x^2+2$ is divided by $x+2$.
   <span class="marks">[3]</span>
5. Factorise $x^3-6x^2+11x-6$ completely using the factor theorem.
   <span class="marks">[4]</span>
6. If $f(x)=\frac{3x-1}{2}$, find $f^{-1}(x)$ and verify that
   $f(f^{-1}(5))=5$. <span class="marks">[4]</span>

::: note Solutions to 18.12
**1.** $1+3+2=6$.
**2.** The expression under the root must not be negative, so $x\geq3$; the
   domain is $[3,\infty)$.
**3.** $(f\circ g)(x)=f(x^2)=2x^2+1$ and $(g\circ f)(x)=(2x+1)^2$.
**4.** By the remainder theorem the remainder is $f(-2)=16-12+2=6$.
**5.** Try $x=1$: $1-6+11-6=0$, so $x-1$ is a factor. Dividing,
   $x^3-6x^2+11x-6=(x-1)(x^2-5x+6)=(x-1)(x-2)(x-3)$.
**6.** Put $y=\frac{3x-1}{2}$; then $2y=3x-1$ and $x=\frac{2y+1}{3}$, so
   $f^{-1}(x)=\frac{2x+1}{3}$. Check: $f^{-1}(5)=\frac{11}{3}$ and
   $f\left(\frac{11}{3}\right)=\frac{11-1}{2}=5$ ✓.
:::

## Chapter summary

- **Sequences:** $t_n=a+(n-1)d$, $S_n=\frac n2\{2a+(n-1)d\}$; $t_n=ar^{n-1}$,
  $S_n=\frac{a(r^n-1)}{r-1}$; a pair of numbers with known sum $S$ and product
  $P$ are the roots of $t^2-St+P=0$.
- **Quadratics:** $D=b^2-4ac$ decides the nature of the roots; vertex at
  $x=-\frac{b}{2a}$; a line meets a parabola as many times as the combined
  quadratic has real roots.
- **Matrices:** the inverse of a 2-row matrix needs a non-zero determinant; the
  matrix method and Cramer's rule give the same answer, and $|AB|=|A||B|$.
- **Trigonometry:** $\sin(A\pm B)$, $\cos(A\pm B)$, the three forms of $\cos2A$,
  $\tan2A$, $\sin3A$, $\cos3A$, and the sum-to-product formulas are the whole
  toolkit.
- **Height and distance:** always draw the two right triangles, write
  $\tan$ for each, and eliminate the distance you do not know.
- **Lines:** $\tan\theta=\left|\frac{m_1-m_2}{1+m_1m_2}\right|$; for
  $ax^2+2hxy+by^2=0$ the lines are perpendicular when $a+b=0$.
- **Circle:** $x^2+y^2+2gx+2fy+c=0$ has centre $(-g,-f)$ and radius
  $\sqrt{g^2+f^2-c}$; the circle on a diameter has the midpoint as centre.
- **Vectors:** $\vec a\cdot\vec b=a_1b_1+a_2b_2$; parallelism is checked with
  the cross-product-like condition $a_1b_2-a_2b_1=0$.
- **Linear programming:** the optimum is always at a corner of the feasible
  region; an inversion satisfies $OP\cdot OP'=k^2$.
- **Continuity:** continuous means the two one-sided limits equal the value;
  equal limits with a different value is removable, unequal limits is a jump.
- **Statistics:** $\sigma=\sqrt{\frac{\sum(x-\bar x)^2}{n}}$,
  CV $=\frac{\sigma}{\bar x}\times100\%$, and consistency is judged on the
  coefficient of variation, never on the standard deviation alone.
- **Polynomials:** remainder $=f(a)$ on division by $x-a$; $x-a$ is a factor
  exactly when $f(a)=0$.
