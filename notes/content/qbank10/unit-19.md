---
subject: Question Bank
grade: 10
unit: 19
title: "Optional Mathematics: Model Question Sets and Predicted Questions"
hours: 0
area: Optional Mathematics
---

This chapter offers two complete, original practice papers for Grade 10 Optional Mathematics, followed by worked answers. The format follows the Curriculum Development Centre's 2082 specification grid for Grades 9–10 Optional Mathematics. A ranked practice list at the end helps you revise without pretending anyone can know the future paper.

::: key Current paper structure (CDC 2082)
**Full marks: 75 · Time: 3 hours.** Group A has 11 objective items worth 1 mark each (11 marks). Questions 2–13 are within-content-area questions worth 40 marks in total. Questions 14–17 are cross-content-area questions worth 6 marks each (24 marks). The grid's content areas are Algebra, Trigonometry, Geometry, Vector, Statistics, and Limit and Continuity. The official document is titled *Specification Grid and Model Question: Grade 9 and 10 Optional Mathematics*, decided on 2082/04/16; see the [CDC publication page](https://moecdc.gov.np/content/10/specification-schedule-and-sample-questions--class-9/).
:::

::: caution What "predicted" means
The priority list below is a revision guide based on the syllabus and the published grid—not a prediction of the questions the examination board will choose. Both papers are original practice material, not reproduced past questions. Check the latest CDC or school notice before an examination, because specifications can change.
:::

## 19.1 How the 75 marks are allocated

| Part | Questions | Marks | Total |
|---|---:|---:|---:|
| Group A: objective | 11 items | 1 each | 11 |
| Within content area | 12 questions | 40 in total | 40 |
| Cross content area | 4 questions | 6 each | 24 |
| **Total** | **17 questions** |  | **75** |

The CDC table assigns three within-area questions each to Algebra, Trigonometry, and Geometry, and one each to Vector, Statistics, and Limit and Continuity. The two papers below retain that subject-area structure and include four cross-area applications.

::: tip Recall the split | अङ्क बाँडफाँट सम्झनुहोस्
**English:** 11 marks are objective; 40 are within a content area; 24 combine areas. **नेपाली:** ११ अङ्क वस्तुगत, ४० अङ्क विषयक्षेत्रभित्रका, र २४ अङ्क दुई वा बढी क्षेत्र जोड्ने प्रश्नका हुन्। Add them before starting: $11+40+24=75$.
:::

```figure caption="How the Optional Mathematics paper distributes its 75 marks."
import matplotlib.pyplot as plt
labels = ["Objective", "Within-area", "Cross-area"]
values = [11, 40, 24]
ys = [2, 1, 0]
fig, ax = plt.subplots(figsize=(4.6, 2.5))
ax.barh(ys, values, height=0.56, color=[SERIES[0], SERIES[2], SERIES[4]])
for y, value in zip(ys, values):
    ax.text(value + 0.6, y, str(value), va="center", color=INK, fontweight="bold")
ax.set_yticks(ys); ax.set_yticklabels(labels)
ax.set_xlim(0, 46); ax.set_xlabel("Marks out of 75")
ax.tick_params(axis="both", length=0)
ax.spines[["top", "right", "left"]].set_visible(False)
ax.xaxis.grid(True, color=GRID, linewidth=0.6); ax.set_axisbelow(True)
fig.tight_layout()
```

## 19.2 Model Question Set 1

**Time: 3 hours. Full marks: 75. Attempt all questions.**

### Group A — Objective questions (11 × 1 = 11)

1. The 10th term of $5,8,11,\ldots$ is <span class="marks">[1]</span>
   (a) 29 (b) 30 (c) 32 (d) 35
2. The roots of $x^2-5x+6=0$ are <span class="marks">[1]</span>
   (a) 1 and 6 (b) 2 and 3 (c) -2 and -3 (d) 3 and 5
3. A $2\times2$ matrix has first row $(2,1)$ and second row $(5,3)$. Its determinant is <span class="marks">[1]</span>
   (a) -1 (b) 1 (c) 6 (d) 11
4. $\sin60^\circ$ equals <span class="marks">[1]</span>
   (a) $\frac12$ (b) $\frac{\sqrt{3}}{2}$ (c) 1 (d) 0
5. $\tan45^\circ$ equals <span class="marks">[1]</span>
   (a) 0 (b) $\frac12$ (c) 1 (d) $\sqrt{3}$
6. The slope of the line through $(1,2)$ and $(3,6)$ is <span class="marks">[1]</span>
   (a) 1 (b) 2 (c) 3 (d) 4
7. A circle with centre at the origin and radius 5 has equation <span class="marks">[1]</span>
   (a) $x+y=5$ (b) $x^2+y^2=5$ (c) $x^2+y^2=25$ (d) $x^2-y^2=25$
8. The magnitude of vector $(3,4)$ is <span class="marks">[1]</span>
   (a) 1 (b) 5 (c) 7 (d) 12
9. The dot product of $(1,2)$ and $(2,-1)$ is <span class="marks">[1]</span>
   (a) -4 (b) 0 (c) 2 (d) 4
10. The mean of $2,4,6,8$ is <span class="marks">[1]</span>
   (a) 4 (b) 5 (c) 6 (d) 20
11. $\lim_{x\to2}\frac{x^2-4}{x-2}$ is <span class="marks">[1]</span>
   (a) 0 (b) 2 (c) 4 (d) does not exist

### Within-content-area questions (40 marks)

**2. Algebra.** An arithmetic sequence begins $3,7,11,\ldots$. (a) Find its 20th term. (b) Find the sum of its first 20 terms. <span class="marks">[2+2]</span>

**3. Algebra.** Solve $2x+y=8$ and $x-y=1$ by the matrix method. <span class="marks">[1+2+1]</span>

**4. Algebra.** For $y=x^2-6x+5$, find (a) the zeros, (b) the axis and vertex, and (c) the direction in which the graph opens. <span class="marks">[1+2+1]</span>

**5. Trigonometry.** If $\sin A=\frac35$ and $A$ is acute, find $\cos A$ and $\sin2A$. <span class="marks">[1+2]</span>

**6. Trigonometry.** Solve $2\sin\theta=\sqrt{2}$ for $0^\circ≤\theta<360^\circ$. <span class="marks">[1+2]</span>

**7. Trigonometry.** A student stands $30$ m from the foot of a vertical tower. The angle of elevation of its top is $60^\circ$. Find the tower's height. <span class="marks">[1+1+1]</span>

**8. Geometry.** Find the equation of the line parallel to $2x-3y+6=0$ that passes through $(2,1)$. Show how you use the given point. <span class="marks">[1+3]</span>

**9. Geometry.** Find the equation, centre, and radius of the circle through $(0,0)$, $(4,0)$, and $(0,6)$. <span class="marks">[2+2]</span>

**10. Geometry.** Triangle $PQR$ has vertices $P(1,1)$, $Q(4,1)$, and $R(1,3)$. It is translated by vector $(2,-1)$. (a) Find the image vertices. (b) Name the transformation. (c) Find the area of the image triangle. <span class="marks">[2+1+1]</span>

**11. Vector.** For $\vec a=(3,4)$ and $\vec b=(4,-3)$, find $\vec a\cdot\vec b$ and state the angle between the vectors. <span class="marks">[1+1]</span>

**12. Statistics.** Find the mean and population variance of $2,4,6,8$. <span class="marks">[1+1]</span>

**13. Limit and Continuity.** (a) Find $\lim_{x\to3}\frac{x^2-9}{x-3}$. (b) If $f(x)=\frac{x^2-9}{x-3}$ for $x\ne3$ and $f(3)=k$, find $k$ for continuity at 3. <span class="marks">[2+1]</span>

### Cross-content-area questions (4 × 6 = 24)

**14. Algebra and Geometry.** A rectangular garden has length 4 m more than its width and area 77 m². A path 1 m wide is added outside all four sides. (a) Form and solve a quadratic equation to find the garden's dimensions. (b) Find the area of the path. (c) Find the paving cost at Rs 50 per m². <span class="marks">[2+2+2]</span>

**15. Trigonometry and Geometry.** A sector has radius 7 cm and central angle $60^\circ$. (a) Convert the angle to radians. (b) Find the arc length. (c) Find the area of the sector. <span class="marks">[1+2+3]</span>

**16. Functions and Statistics.** For $f(x)=3x-2$, list the values when $x=1,2,3,4,5$. Find their mean and population standard deviation. <span class="marks">[2+1+3]</span>

**17. Vector and Transformation.** Points $P(2,1)$, $Q(5,1)$, and $R(2,4)$ form a triangle. Rotate it $90^\circ$ anticlockwise about the origin. (a) Find the image coordinates. (b) Find the vector $\overrightarrow{P'Q'}$. (c) Find the area of the image triangle and compare it with the original. <span class="marks">[3+1+2]</span>

### Answers and worked solutions — Set 1

::: note Group A answer key
**1.** (c) — $t_{10}=5+9(3)=32$.
**2.** (b) — $(x-2)(x-3)=0$.
**3.** (b) — $2(3)-1(5)=1$.
**4.** (b) — the exact special-angle value is $\sqrt{3}/2$.
**5.** (c) — $\tan45^\circ=1$.
**6.** (b) — slope $=(6-2)/(3-1)=2$.
**7.** (c) — $x^2+y^2=r^2=25$.
**8.** (b) — $\sqrt{3^2+4^2}=5$.
**9.** (b) — $1(2)+2(-1)=0$.
**10.** (b) — $(2+4+6+8)/4=5$.
**11.** (c) — cancel $x-2$ for $x\ne2$; the limit is 4.
:::

::: note Questions 2 to 4
**2.** Here $a=3$, $d=4$. $t_{20}=3+19(4)=79$. Then $S_{20}=\frac{20}{2}[2(3)+19(4)]=10(82)=820$.

**3.** The coefficient matrix has rows $(2,1)$ and $(1,-1)$ and determinant $-3$. Its inverse has rows $(1/3,1/3)$ and $(1/3,-2/3)$. Multiplying by $(8,1)^T$ gives $x=(8+1)/3=3$ and $y=(8-2)/3=2$. Check in both equations: $6+2=8$ and $3-2=1$.

**4.** $x^2-6x+5=(x-1)(x-5)$, so the zeros are 1 and 5. The axis is midway, $x=3$. At $x=3$, $y=9-18+5=-4$, so the vertex is $(3,-4)$. The positive coefficient of $x^2$ means the parabola opens upward.
:::

::: note Questions 5 to 7
**5.** Since $A$ is acute, $\cos A=\sqrt{1-\sin^2 A}=\sqrt{1-9/25}=4/5$. Then $\sin2A=2\sin A\cos A=2(3/5)(4/5)=24/25$.

**6.** $\sin\theta=\sqrt{2}/2$. The reference angle is $45^\circ$; sine is positive in quadrants I and II. In $0^\circ≤\theta<360^\circ$, $\theta=45^\circ,135^\circ$.

**7.** Let the height be $h$. $\tan60^\circ=h/30$, so $h=30\sqrt{3}$ m (about 51.96 m).
:::

::: note Questions 8 to 10
**8.** Parallel lines have the same coefficients of $x$ and $y$, so write $2x-3y+c=0$. Substitute $(2,1)$: $4-3+c=0$, giving $c=-1$. The line is **$2x-3y-1=0$**.

**9.** Let the equation be $x^2+y^2+Dx+Ey+F=0$. The origin gives $F=0$; $(4,0)$ gives $16+4D=0$, so $D=-4$; $(0,6)$ gives $36+6E=0$, so $E=-6$. Thus $x^2+y^2-4x-6y=0$, or $(x-2)^2+(y-3)^2=13$. Centre $(2,3)$, radius $\sqrt{13}$.

**10.** Add $(2,-1)$ to each point: $P'(3,0)$, $Q'(6,0)$, $R'(3,2)$. This is a translation. The image is a right triangle with perpendicular legs 3 and 2, so its area is $\frac12(3)(2)=3$ square units.
:::

::: note Questions 11 to 13
**11.** $\vec a\cdot\vec b=3(4)+4(-3)=0$. Both vectors are non-zero, so they are **perpendicular** and the angle is $90^\circ$.

**12.** Mean $\bar x=(2+4+6+8)/4=5$. Squared deviations sum to $9+1+1+9=20$, so population variance is $20/4=5$.

**13.** (a) Factor: $(x^2-9)/(x-3)=x+3$ for $x\ne3$, so the limit is **6**. (b) Continuity requires $f(3)$ to equal the limit; hence **$k=6$**.
:::

::: note Questions 14 to 17
**14.** Let the width be $x$ m; length is $x+4$. $x(x+4)=77$, so $x^2+4x-77=0=(x+11)(x-7)$. Reject $x=-11$ because a length is positive. Width $=7$ m and length $=11$ m. The outer dimensions are $9$ m by $13$ m; path area $=9(13)-7(11)=117-77=40$ m². Cost $=40(50)=\text{Rs 2,000}$.

**15.** $60^\circ=\pi/3$ radians. Arc length $s=r\theta=7\pi/3$ cm (about 7.33 cm). Sector area $=\frac12r^2\theta=\frac12(49)(\pi/3)=49\pi/6$ cm² (about 25.66 cm²).

**16.** The outputs are $1,4,7,10,13$. Their mean is $35/5=7$. Squared deviations are $36,9,0,9,36$, with sum 90. Population variance is $90/5=18$, so standard deviation is $\sqrt{18}=3\sqrt{2}$ (about 4.24).

**17.** A $90^\circ$ anticlockwise rotation maps $(x,y)$ to $(-y,x)$. Thus $P'(-1,2)$, $Q'(-1,5)$, $R'(-4,2)$. $\overrightarrow{P'Q'}=(0,3)$. The image is a right triangle with legs 3 and 3, area $\frac12(3)(3)=4.5$ square units, equal to the original area $\frac12(3)(3)=4.5$.
:::

## 19.3 Model Question Set 2

**Time: 3 hours. Full marks: 75. Attempt all questions.**

### Group A — Objective questions (11 × 1 = 11)

1. The sum of the first four terms of $2,6,18,\ldots$ is <span class="marks">[1]</span>
   (a) 54 (b) 72 (c) 80 (d) 108
2. The discriminant of $x^2+4x+4=0$ is <span class="marks">[1]</span>
   (a) 0 (b) 4 (c) 8 (d) 16
3. A $2\times2$ matrix has first row $(1,2)$ and second row $(3,4)$. Its determinant is <span class="marks">[1]</span>
   (a) -2 (b) 2 (c) 10 (d) 14
4. $\cos120^\circ$ equals <span class="marks">[1]</span>
   (a) $\frac12$ (b) $-\frac12$ (c) $\frac{\sqrt{3}}{2}$ (d) 0
5. The solutions of $\sin\theta=\frac12$ in $0^\circ≤\theta<360^\circ$ are <span class="marks">[1]</span>
   (a) $30^\circ,150^\circ$ (b) $30^\circ,330^\circ$ (c) $60^\circ,120^\circ$ (d) $45^\circ,135^\circ$
6. The slope of $2x+y-7=0$ is <span class="marks">[1]</span>
   (a) 2 (b) -2 (c) $\frac12$ (d) $-\frac12$
7. The equation of a circle with centre $(3,-2)$ and radius 4 is <span class="marks">[1]</span>
   (a) $(x+3)^2+(y-2)^2=16$ (b) $(x-3)^2+(y+2)^2=16$ (c) $(x-3)^2+(y-2)^2=4$ (d) $x^2+y^2=16$
8. The vector from $(1,1)$ to $(4,5)$ is <span class="marks">[1]</span>
   (a) $(5,6)$ (b) $(3,4)$ (c) $(4,5)$ (d) $(2,3)$
9. $(2,1)\cdot(1,-2)$ equals <span class="marks">[1]</span>
   (a) -4 (b) 0 (c) 2 (d) 4
10. The range of $4,8,9,11$ is <span class="marks">[1]</span>
   (a) 3 (b) 7 (c) 8 (d) 11
11. $\lim_{x\to1}\frac{x^3-1}{x-1}$ is <span class="marks">[1]</span>
   (a) 1 (b) 2 (c) 3 (d) does not exist

### Within-content-area questions (40 marks)

**2. Algebra.** A geometric sequence begins $3,6,12,\ldots$. (a) Find its 8th term. (b) Find the sum of its first 8 terms. <span class="marks">[2+2]</span>

**3. Algebra.** Solve $3x+y=11$ and $x+y=5$ by a suitable algebraic or matrix method. Show your working. <span class="marks">[2+2]</span>

**4. Algebra.** For $y=x^2-4x-5$, find (a) the zeros, (b) the axis and vertex, and (c) the $y$-intercept. <span class="marks">[2+1+1]</span>

**5. Trigonometry.** If $\theta$ is acute, simplify $\sqrt{1-\sin^2\theta}$ in terms of a trigonometric ratio. <span class="marks">[1+2]</span>

**6. Trigonometry.** Solve $\cos\theta=\frac12$ for $0^\circ≤\theta<360^\circ$. <span class="marks">[1+2]</span>

**7. Trigonometry.** A building casts a horizontal shadow $20\sqrt{3}$ m long. If the Sun's elevation is $30^\circ$, find the building's height. <span class="marks">[1+1+1]</span>

**8. Geometry.** Find the equation of the line parallel to $x+2y-4=0$ that passes through $(2,0)$. <span class="marks">[1+3]</span>

**9. Geometry.** A circle has diameter endpoints $(2,0)$ and $(8,0)$. Find its centre, radius, and equation in general form. <span class="marks">[1+1+2]</span>

**10. Geometry.** An ellipse is given by $\frac{x^2}{25}+\frac{y^2}{9}=1$. Find its centre, the lengths of its major and minor axes, its foci, and its eccentricity. <span class="marks">[1+1+1+1]</span>

**11. Vector.** For $\vec a=(2,-1)$ and $\vec b=(3,4)$, find the dot product and state whether the angle between them is acute, right, or obtuse. <span class="marks">[1+1]</span>

**12. Statistics.** Find the population standard deviation of $1,3,5,7,9$. <span class="marks">[2]</span>

**13. Limit and Continuity.** Let $f(x)=\frac{x^3-8}{x-2}$ for $x\ne2$. (a) Find $\lim_{x\to2}f(x)$. (b) What value of $f(2)$ makes $f$ continuous at 2? <span class="marks">[2+1]</span>

### Cross-content-area questions (4 × 6 = 24)

**14. Algebra and Geometry.** A triangular panel has base $x$ m and perpendicular height $(x+2)$ m. Its area is 40 m². (a) Form the quadratic equation. (b) Solve it and select the physically meaningful base. (c) Find the height and hypotenuse if the panel is a right triangle. <span class="marks">[2+2+2]</span>

**15. Trigonometry and Geometry.** A 10 m ladder rests against a vertical wall and makes an angle of $60^\circ$ with the horizontal ground. Find (a) the height reached on the wall and (b) the horizontal distance from the wall to the foot of the ladder. <span class="marks">[3+3]</span>

**16. Functions and Statistics.** Evaluate $f(x)=x^2-2$ for $x=-2,-1,0,1,2$. From the resulting data, find (a) the mean, (b) the range, and (c) the population variance. <span class="marks">[2+1+3]</span>

**17. Algebra and Geometry (Linear Programming).** A workshop makes products A and B. Let $x$ and $y$ be their daily quantities. Each A uses 1 machine-hour and each B uses 1 machine-hour; at most 8 machine-hours are available. Production is limited to $x≤5$ and $y≤6$, with $x,y≥0$. If the contribution is Rs 4 per A and Rs 3 per B, (a) write the objective function and constraints, (b) list the feasible-region corner points, and (c) find the maximum contribution. <span class="marks">[2+2+2]</span>

### Answers and worked solutions — Set 2

::: note Group A answer key
**1.** (c) — $2+6+18+54=80$.
**2.** (a) — $D=4^2-4(1)(4)=0$.
**3.** (a) — $1(4)-2(3)=-2$.
**4.** (b) — cosine is negative in quadrant II; $\cos120^\circ=-1/2$.
**5.** (a) — sine is positive in quadrants I and II with reference angle $30^\circ$.
**6.** (b) — $y=-2x+7$.
**7.** (b) — use $(x-h)^2+(y-k)^2=r^2$ with $(h,k)=(3,-2)$.
**8.** (b) — subtract $(1,1)$ from $(4,5)$.
**9.** (b) — $2(1)+1(-2)=0$.
**10.** (b) — $11-4=7$.
**11.** (c) — cancel $x-1$; $x^2+x+1$ tends to 3.
:::

::: note Questions 2 to 4
**2.** Here $a=3$, $r=2$. $t_8=3(2^7)=384$. $S_8=3(2^8-1)/(2-1)=3(255)=765$.

**3.** Subtract the second equation from the first: $2x=6$, so $x=3$. Then $3+y=5$, so $y=2$. Check: $3(3)+2=11$ and $3+2=5$.

**4.** $x^2-4x-5=(x-5)(x+1)$, so the zeros are 5 and -1. The axis is their midpoint, $x=2$. At $x=2$, $y=4-8-5=-9$, so the vertex is $(2,-9)$. At $x=0$, $y=-5$, so the $y$-intercept is $(0,-5)$.
:::

::: note Questions 5 to 7
**5.** By $1-\sin^2\theta=\cos^2\theta$, $\sqrt{1-\sin^2\theta}=|\cos\theta|$. Since $\theta$ is acute, cosine is positive, so the answer is **$\cos\theta$**.

**6.** Cosine is positive in quadrants I and IV and has reference angle $60^\circ$. Thus $\theta=60^\circ,300^\circ$.

**7.** Let the height be $h$. $\tan30^\circ=h/(20\sqrt{3})$; hence $h=20\sqrt{3}(1/\sqrt{3})=20\text{ m}$.
:::

::: note Questions 8 to 10
**8.** A parallel line has form $x+2y+c=0$. Substitute $(2,0)$: $2+c=0$, so $c=-2$. Required equation: **$x+2y-2=0$**.

**9.** The midpoint of the diameter endpoints is $(5,0)$, the centre. The diameter is 6, so the radius is 3. Equation: $(x-5)^2+y^2=9$, or **$x^2+y^2-10x+16=0$**.

**10.** Centre $(0,0)$. Semi-major axis $a=5$ and semi-minor axis $b=3$, so the axis lengths are 10 and 6. $c^2=a^2-b^2=25-9=16$, so the foci are $(\pm4,0)$. Eccentricity $e=c/a=4/5$.
:::

::: note Questions 11 to 13
**11.** $\vec a\cdot\vec b=2(3)+(-1)(4)=2>0$. Therefore the angle is **acute**.

**12.** Mean $=5$. Squared deviations are $16,4,0,4,16$, summing to 40. Variance $=40/5=8$, so population standard deviation is **$\sqrt{8}=2\sqrt{2}$**.

**13.** Factor $x^3-8=(x-2)(x^2+2x+4)$. Therefore the limit is $2^2+2(2)+4=12$. Continuity requires **$f(2)=12$**.
:::

::: note Questions 14 to 17
**14.** $\frac12x(x+2)=40$, so $x^2+2x-80=0=(x+10)(x-8)$. Reject $x=-10$ because a length is positive; base $x=8$ m and height $x+2=10$ m. The hypotenuse is $\sqrt{8^2+10^2}=\sqrt{164}=2\sqrt{41}$ m.

**15.** The ladder is the hypotenuse. Height $=10\sin60^\circ=5\sqrt{3}\text{ m}$ (about 8.66 m). Horizontal distance $=10\cos60^\circ=5$ m. Check: $(5\sqrt{3})^2+5^2=75+25=100=10^2$.

**16.** Values are $2,-1,-2,-1,2$. Mean $=(2-1-2-1+2)/5=0$. Range $=2-(-2)=4$. Squared deviations sum to $4+1+4+1+4=14$, so population variance is **$14/5$**.

**17.** Maximise $Z=4x+3y$ subject to $x+y≤8$, $x≤5$, $y≤6$, $x,y≥0$. Corner points are $(0,0)$, $(5,0)$, $(5,3)$, $(2,6)$ and $(0,6)$. Their $Z$ values are 0, 20, 29, 26 and 18, respectively. The maximum contribution is **Rs 29** at $(x,y)=(5,3)$.
:::

## 19.4 Revision priorities

1. **Algebra:** factorisation, quadratic roots and graphs, matrices, and sequence/series formulae. Practise showing the condition that lets you reject an impossible root.
2. **Trigonometry:** exact ratios, identities, equation solutions over a stated interval, and labelled height-and-distance diagrams.
3. **Geometry:** slope and line equations, circles by completing squares, conic parameters, and transformations on coordinate pairs.
4. **Vector:** component form, magnitude, dot product, and the geometric meaning of a zero dot product.
5. **Statistics:** state whether the problem asks for population or sample measures, then use the correct denominator.
6. **Limit and Continuity:** factor before substituting, compare one-sided limits when necessary, and set the function value equal to the limit only when continuity is required.

Treat this order as a way to organise revision, not a promise about what will appear on an examination paper.
