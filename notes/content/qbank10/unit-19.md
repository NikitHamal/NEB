---
subject: Question Bank
grade: 10
unit: 19
title: "Optional Mathematics: Model Question Sets and Predicted Questions"
hours: 0
area: Optional Mathematics
---

This chapter does three jobs. It sets out the **specification grid** of the SEE
Optional Mathematics paper and shows what each group is really testing; it gives
**two complete model papers**, each of 75 marks and three hours, to the exact CDC
pattern, with a full solution to every question; and it closes with a **ranked
order of practice priorities**, each rank carrying the reason it holds that
place.

::: caution What "predicted" means here, and what it does not
Nobody outside the examination board knows next year's questions. Every rank in
section 19.4 rests on two public facts only: the **specification grid** (how
many questions of each kind and marks), and the **syllabus** (what may be asked).
A high rank means *practise this first*, never *this will come*. A low rank means
*less likely*, never *safe to skip*. None of the questions below is copied from
a past paper; all of them are original practice items built to the published
pattern.
:::

::: key The grid: 75 marks in 3 hours
| Group | Questions | Marks each | Total | What it asks for |
|---|---|---|---|---|
| A | 10 | 1 | 10 | one-line recall or a single substitution |
| B | 8 | 2 | 16 | one short method, two or three lines |
| C | 11 | 3 | 33 | a full short-answer method |
| D | 4 | 4 | 16 | a longer method, a proof, or a two-triangle problem |
| **Total** | **33** | | **75** | |

Groups C and D together are **49 of the 75 marks**. A student who is slow in
Group A but fluent in C and D scores far higher than the reverse.
:::

## 19.1 What the grid implies

### 19.1.1 Marks by group

```figure caption="Marks against time for the four groups. Group A is 13% of the marks and about 6% of the time; Group C alone is 44% of the marks, so it deserves roughly half the paper's three hours."
import matplotlib.pyplot as plt
groups = ["A", "B", "C", "D"]
marks = [10, 16, 33, 16]
share = [13.3, 21.3, 44.0, 21.3]
fig, ax = plt.subplots(figsize=(4.6, 2.6))
ax.bar(groups, marks, color=[MUTED, MUTED, ACCENT, SERIES[1]], width=0.55)
for i, (m, s) in enumerate(zip(marks, share)):
    ax.text(i, m + 0.8, "%d\n%.0f%%" % (m, s), ha="center", fontsize=8, color=INK)
ax.set_ylim(0, 40)
ax.set_ylabel("marks out of 75", fontsize=8)
ax.tick_params(labelsize=9, length=0)
ax.spines[["top", "right"]].set_visible(False)
ax.yaxis.grid(True, color=GRID, lw=0.6)
ax.set_axisbelow(True)
fig.tight_layout()
```

### 19.1.2 The twelve units and where they normally appear

| Unit | Usual home | Note |
|---|---|---|
| 1. Sequence and series | A, B or C | AP and GP formulas pay for themselves in Group A |
| 2. Quadratic equations and graphs | B or C | roots, nature, vertex, line meets curve |
| 3. Matrices and determinants | B or C | almost always a system of two equations |
| 4. Trigonometry: multiple and submultiple | B or C | proofs of identities sit here |
| 5. Conditional identities, equations, height and distance | C or D | one height-and-distance question is close to certain |
| 6. Angle between two lines, pair of lines | A or B | slope conditions |
| 7. Conic sections and circle | B or C | find the circle, or centre and radius |
| 8. Vector | A, B or C | dot product, perpendicularity, collinearity |
| 9. Linear programming and transformation | C or D | maximise an objective at a corner |
| 10. Continuity | A or B | limit by cancelling a factor |
| 11. Statistics: dispersion | C or D | SD, quartile deviation, coefficient of variation |
| 12. Functions and polynomials | B, C or D | remainder, factor, inverse, composite |

### 19.1.3 The thinking levels

| Level | Approximate marks | What it looks like |
|---|---|---|
| Knowledge | 15 | state a formula, name a transformation, write a centre |
| Understanding | 20 | explain why a line and a curve meet twice; compare consistencies |
| Application | 25 | solve a system, find a height, maximise a profit |
| Higher ability | 15 | prove an identity, complete a two-triangle problem, justify a corner |

::: tip Timing plan that fits the grid
Group A: **10 minutes**. Group B: 8 items at 3 minutes, **24 minutes**. Group C:
11 items at 4 minutes, **44 minutes**. Group D: 4 items at 6 minutes,
**24 minutes**. That is 102 minutes of writing, leaving **18 minutes** to check
— and the check is where the last five marks live. Never let a Group A item take
more than 90 seconds: mark it and come back.
:::

## 19.2 Model Set 1

**Optional Mathematics — Class 10. Time: 3 hours. Full marks: 75.**
**Attempt all questions.**

### Question paper

**Group A — Choose the correct answer. $[10\times1=10]$**

1. If the arithmetic mean and the geometric mean of two positive numbers are
   equal, then the numbers
   (a) are equal (b) are unequal (c) are reciprocals (d) are both zero
2. The 7th term of 3, 7, 11, ... is
   (a) 27 (b) 31 (c) 35 (d) 39
3. $\cos2A$ equals
   (a) $2\cos A$ (b) $\cos^2A-\sin^2A$ (c) $1-2\cos^2A$ (d) $2\sin A\cos A$
4. If $\tan A=1$ and $A$ is acute, then $A$ is
   (a) $30°$ (b) $45°$ (c) $60°$ (d) $90°$
5. The centre of the circle $x^2+y^2-6x+4y+9=0$ is
   (a) $(3,-2)$ (b) $(-3,2)$ (c) $(6,-4)$ (d) $(3,2)$
6. If $\vec a=\hat i+2\hat j$ and $\vec b=2\hat i-\hat j$, then $\vec a\cdot\vec b$ is
   (a) 4 (b) 0 (c) $-4$ (d) 5
7. The 5th term of 2, 6, 18, ... is
   (a) 54 (b) 108 (c) 162 (d) 486
8. A quadratic equation has equal roots when its discriminant is
   (a) positive (b) negative (c) zero (d) one
9. The maximum of $z=2x+3y$ subject to $x+y\le 4$, $x\ge 0$, $y\ge 0$ is
   (a) 8 (b) 10 (c) 12 (d) 14
10. The standard deviation of 5, 5, 5, 5 is
   (a) 0 (b) 1 (c) 5 (d) 25

**Group B — Answer in short. $[8\times2=16]$**

1. Find the 12th term of the arithmetic sequence 4, 9, 14, ...
2. Find the sum of the first 20 terms of 3, 7, 11, ...
3. Solve $x^2-5x-6=0$.
4. Find the value of $k$ for which $x^2+4x+k=0$ has equal roots.
5. Find the inverse of the matrix with rows $(1,2)$ and $(3,7)$.
6. If $\sin A=\frac45$ and $A$ is acute, find $\cos2A$.
7. Find the angle between two lines whose slopes are 2 and $-\frac12$.
8. Find the radius of the circle $x^2+y^2-2x+4y-4=0$.

**Group C — Answer with working. $[11\times3=33]$**

1. Insert three arithmetic means between 4 and 20.
2. Find the sum of the geometric series $3+9+27+\dots+2187$.
3. Solve by the matrix method: $3x+2y=12$, $2x-y=1$.
4. Prove that $\frac{1+\cos2A}{\sin2A}=\cot A$.
5. Prove that $\sin3A=3\sin A-4\sin^3A$.
6. A kite string 100 m long makes an angle of $30°$ with the ground. Find the
   height of the kite.
7. Find the equation of the circle with centre $(3,-2)$ that passes through
   $(1,1)$.
8. Find the angle between $\vec a=3\hat i+4\hat j$ and $\vec b=4\hat i-3\hat j$.
9. Find the image of $(2,5)$ under the transformation with matrix rows $(1,2)$
   and $(3,4)$.
10. Evaluate $\lim_{x\to1}\frac{x^3-1}{x-1}$.
11. Find the standard deviation of 6, 8, 10, 12, 14.

**Group D — Answer in detail. $[4\times4=16]$**

1. The third term of a geometric sequence is 12 and the sixth is 96. Find the
   sequence and the sum of its first six terms.
2. In a triangle, prove that
   $\sin2A+\sin2B+\sin2C=4\sin A\sin B\sin C$.
3. From the top of a 30 m cliff the angles of depression of two boats on the
   same side are $30°$ and $45°$. Find the distance between the boats.
4. Solve $x^2+y^2=25$ and $y=x+1$ simultaneously.

### Solutions

::: note Group A — answers with reasons
**1.** (a) — AM $=$ GM forces $(\sqrt{a}-\sqrt{b})^2=0$, so $a=b$.
**2.** (a) — $t_7=a+6d=3+6\times4=27$; the exponent is $7-1$, not 7.
**3.** (b) — that is the definition; (c) is the wrong sign, (d) is $\sin2A$.
**4.** (b) — $\tan45°=1$.
**5.** (a) — $g=-3$, $f=2$, centre $(-g,-f)=(3,-2)$.
**6.** (b) — $1\times2+2\times(-1)=0$.
**7.** (c) — $2\times3^4=162$.
**8.** (c) — $D=0$ gives the two roots the same value.
**9.** (c) — corners $(0,0)$, $(4,0)$, $(0,4)$ give 0, 8, 12; the largest is 12.
**10.** (a) — every observation equals the mean, so there is no spread.
:::

::: caution Two Group A items above reward a habit, not knowledge
Item 2 asks for the **7th** term, so the multiplier is $3^{7-1}$ for a GP and
$6d$ for an AP — six steps from the first term, not seven. Item 3 offers both
$(b)$ $\cos^2A-\sin^2A$ and $(c)$ $1-2\cos^2A$; only the first is the standard
form, the second has the sign wrong. In both cases the whole method is:
**write the formula, put the numbers in, and only then look at the options.**
Choosing by eye is how marks disappear from a 13% group.
:::

::: note Group B — solutions
**1.** $4+11\times5=59$.
**2.** $S_{20}=\frac{20}{2}\{6+19\times4\}=10\times82=820$.
**3.** $(x-6)(x+1)=0$, so $x=6$ or $x=-1$.
**4.** $D=16-4k=0$, so $k=4$.
**5.** $|A|=7-6=1$, and the inverse has rows $(7,-2)$ and $(-3,1)$.
**6.** $\cos A=\frac35$, so $\cos2A=1-2\left(\frac45\right)^2=1-\frac{32}{25}
   =-\frac{7}{25}$.
**7.** The product of the slopes is $2\times\left(-\frac12\right)=-1$, so the
   angle is $90°$.
**8.** $\sqrt{g^2+f^2-c}=\sqrt{1+4+4}=3$.
:::

::: note Group C — solutions
**1.** Between 4 and 20 there are four equal gaps totalling 16, so $d=4$ and the
   means are **8, 12, 16**.
**2.** The last term is $3\times3^{6}=2187$, so the series has 7 terms and
   $S_7=\frac{3(3^7-1)}{3-1}=\frac{3\times2186}{2}=3279$.
**3.** $|A|=3(-1)-2(2)=-7$; $x=\frac{12(-1)-2(1)}{-7}=\frac{-14}{-7}=2$ and
   $y=\frac{3(1)-2(12)}{-7}=\frac{-21}{-7}=3$. Check: $6+6=12$ ✓ and
   $4-3=1$ ✓.
**4.** $1+\cos2A=2\cos^2A$ and $\sin2A=2\sin A\cos A$, so the left side is
   $\frac{2\cos^2A}{2\sin A\cos A}=\frac{\cos A}{\sin A}=\cot A$.
**5.** $\sin3A=\sin(2A+A)=\sin2A\cos A+\cos2A\sin A
   =2\sin A\cos^2A+(1-2\sin^2A)\sin A
   =2\sin A(1-\sin^2A)+\sin A-2\sin^3A=3\sin A-4\sin^3A$.
**6.** $\sin30°=\frac{1}{2}=\frac{h}{100}$, so $h=50$ m.
**7.** Radius
   $r=\sqrt{(3-1)^2+(-2-1)^2}=\sqrt{4+9}=\sqrt{13}$, so
   $(x-3)^2+(y+2)^2=13$, that is $x^2+y^2-6x+4y=0$. Check the given point:
   $1+1-6+4=0$ ✓.
**8.** $\vec a\cdot\vec b=12-12=0$, so the angle is $90°$.
**9.** $(1\times2+2\times5,\;3\times2+4\times5)=(12,26)$.
**10.** Cancel: $\frac{(x-1)(x^2+x+1)}{x-1}=x^2+x+1\to3$.
**11.** Mean $=10$; deviations $-4,-2,0,2,4$; sum of squares $=40$; variance
    $=8$; $\sigma=2\sqrt{2}\approx2.83$.
:::

::: note Group D — solutions
**1.** $r^3=\frac{96}{12}=8$, so $r=2$ and $a=\frac{12}{2^2}=3$. The sequence is
   **3, 6, 12, 24, ...** and
   $S_6=\frac{3(2^6-1)}{2-1}=3\times63=189$.
**2.** $C=180°-(A+B)$, so $2C=360°-2(A+B)$ and
   $\sin2C=-\sin2(A+B)$. Then
   $\sin2A+\sin2B=2\sin(A+B)\cos(A-B)$, so the left side is
   $2\sin(A+B)\cos(A-B)-2\sin(A+B)\cos(A+B)
   =2\sin(A+B)\{\cos(A-B)-\cos(A+B)\}$. Now
   $\cos(A-B)-\cos(A+B)=2\sin A\sin B$, and
   $\sin(A+B)=\sin(180°-C)=\sin C$. The product is
   $2\cdot2\sin A\sin B\sin C=4\sin A\sin B\sin C$.
**3.** Let the boats be at horizontal distances $d_1$ and $d_2$ from the foot of
   the cliff. A depression of $45°$ means $\tan45°=\frac{30}{d_1}$, so
   $d_1=30$ m; a depression of $30°$ means $\tan30°=\frac{30}{d_2}$, so
   $d_2=\frac{30}{\tan30°}=30\sqrt{3}\approx51.96$ m. The boats are
   $d_2-d_1=30\sqrt{3}-30=30(\sqrt{3}-1)\approx21.96$ m apart. Check: the nearer boat
   is at 30 m, the same as the cliff height, which is exactly what a $45°$
   depression requires ✓.
**4.** Substitute $y=x+1$ into $x^2+y^2=25$:
   $x^2+(x+1)^2=25$, so $2x^2+2x+1=25$, giving $x^2+x-12=0$. Then
   $(x+4)(x-3)=0$, so $x=3$ or $x=-4$. With $y=x+1$: $(3,4)$ and $(-4,-3)$.
   Check both: $9+16=25$ ✓ and $16+9=25$ ✓. The line cuts the circle twice, in
   the first and the third quadrant.
:::

## 19.3 Model Set 2

**Optional Mathematics — Class 10. Time: 3 hours. Full marks: 75.**
**Attempt all questions.**

### Question paper

**Group A — Choose the correct answer. $[10\times1=10]$**

1. The common difference of 11, 7, 3, ... is
   (a) 4 (b) $-4$ (c) 7 (d) 11
2. The geometric mean of 2 and 18 is
   (a) 6 (b) 10 (c) 20 (d) 36
3. The roots of $x^2-9=0$ are
   (a) equal (b) imaginary (c) real and unequal (d) zero
4. The determinant of the matrix with rows $(4,1)$ and $(2,3)$ is
   (a) 10 (b) 14 (c) 12 (d) 2
5. $\sin2A$ equals
   (a) $2\sin A$ (b) $2\sin A\cos A$ (c) $\sin A\cos A$ (d) $1-2\sin^2A$
6. The slope of the line $2x+3y=6$ is
   (a) $\frac23$ (b) $-\frac23$ (c) $\frac32$ (d) $-\frac32$
7. The eccentricity of a hyperbola is
   (a) 0 (b) 1 (c) less than 1 (d) greater than 1
8. The magnitude of $5\hat i-12\hat j$ is
   (a) 7 (b) 13 (c) 17 (d) 60
9. $\lim_{x\to0}\frac{\sin x}{x}$ is
   (a) 0 (b) 1 (c) $\infty$ (d) not defined
10. The coefficient of variation is expressed as
   (a) a number (b) a percentage of the mean (c) a squared deviation
   (d) a range

**Group B — Answer in short. $[8\times2=16]$**

1. Find the 10th term of 5, 8, 11, ...
2. Find the sum of the first 15 natural numbers.
3. Find the value of $m$ for which $2x^2+mx+8=0$ has equal roots.
4. If the matrix has rows $(3,k)$ and $(2,4)$, find $k$ for which it has no
   inverse.
5. If $\tan A=\frac12$, find $\tan2A$.
6. Find the general solution of $\cos\theta=\frac12$.
7. Find the centre and radius of $x^2+y^2+4x-6y+4=0$.
8. If $\vec a=2\hat i+\hat j$ and $\vec b=\hat i-2\hat j$, find
   $\vec a\cdot\vec b$.

**Group C — Answer with working. $[11\times3=33]$**

1. Which term of 7, 12, 17, ... is 102?
2. Insert two geometric means between 3 and 81.
3. Solve by Cramer's rule: $2x+3y=13$, $x+2y=8$.
4. Prove that $\frac{1-\cos2A}{\sin2A}=\tan A$.
5. Prove that $\cos^2A+\cos^2(60°+A)+\cos^2(60°-A)=\frac32$.
6. A tower is 45 m high. Find the angle of elevation of its top from a point
   45 m from its foot.
7. Find the equation of the circle on the segment joining $(2,3)$ and $(6,7)$ as
   diameter.
8. Show that the points $A(1,3)$, $B(3,7)$ and $C(5,11)$ are collinear using
   vectors.
9. Find the image of $(-1,4)$ under the matrix with rows $(0,-1)$ and $(1,0)$,
   and name the transformation.
10. Find the value of $k$ that makes $f$ continuous at $x=2$, where
    $f(x)=\frac{x^2-4}{x-2}$ for $x\ne2$ and $f(2)=k$.
11. The mean of five observations is 20 and their standard deviation is 4. Find
    the coefficient of variation.

**Group D — Answer in detail. $[4\times4=16]$**

1. Two positive numbers have arithmetic mean 13 and geometric mean 12. Find the
   numbers.
2. Prove that $\tan A+\tan B+\tan C=\tan A\tan B\tan C$ when
   $A+B+C=180°$.
3. The angle of elevation of the top of a tower from a point on the ground is
   $30°$. Walking 40 m nearer, the elevation becomes $60°$. Find the height.
4. Find the values of $p$ for which the line $y=px+1$ touches the circle
   $x^2+y^2=4$.

### Solutions

::: note Group A — answers with reasons
**1.** (b) — $7-11=-4$.
**2.** (a) — $\sqrt{2\times18}=\sqrt{36}=6$.
**3.** (c) — $x^2-9=(x-3)(x+3)$, so $x=\pm3$: real and unequal.
**4.** (a) — $4\times3-1\times2=10$.
**5.** (b) — the double-angle formula for sine.
**6.** (b) — rearranged, $y=-\frac23x+2$.
**7.** (d) — an ellipse is below 1, a parabola exactly 1, a hyperbola above 1.
**8.** (b) — $\sqrt{25+144}=13$.
**9.** (b) — the standard limit.
**10.** (b) — the coefficient of variation is a percentage of the mean.
:::

::: note Group B — solutions
**1.** $5+9\times3=32$.
**2.** $S_{15}=\frac{15\times16}{2}=120$.
**3.** $D=m^2-4\times2\times8=0$, so $m^2=64$ and $m=\pm8$.
**4.** No inverse means $12-2k=0$, so $k=6$.
**5.** $\tan2A=\frac{2\times\frac12}{1-\frac14}=\frac{1}{\frac34}=\frac43$.
**6.** $\cos\theta=\frac12$ has the principal value $60°$, so
   $\theta=2n\pi\pm\frac{\pi}{3}$, or in degrees
   $\theta=360°n\pm60°$.
**7.** $g=2$, $f=-3$, so the centre is $(-2,3)$ and
   $r=\sqrt{4+9-4}=3$.
**8.** $2\times1+1\times(-2)=0$.
:::

::: note Group C — solutions
**1.** $102=7+(n-1)5$, so $n-1=19$ and it is the **20th** term.
**2.** With two means between 3 and 81 there are three equal ratios, so
   $r^3=\frac{81}{3}=27$ and $r=3$. The means are $3r=9$ and $3r^2=27$, and
   $81=3r^3$ checks ✓.
**3.** $D=2(2)-3(1)=1$; $D_x=13(2)-3(8)=26-24=2$, so $x=2$; and
   $D_y=2(8)-1(13)=16-13=3$, so $y=3$. Check: $4+9=13$ ✓ and $2+6=8$ ✓.
**4.** $1-\cos2A=2\sin^2A$, so the left side is
   $\frac{2\sin^2A}{2\sin A\cos A}=\frac{\sin A}{\cos A}=\tan A$.
**5.** Write $\cos^2x=\frac{1+\cos2x}{2}$ for each of the three terms. The left
   side becomes
   $\frac32+\frac12\{\cos2A+\cos(120°+2A)+\cos(120°-2A)\}$. The pair formula
   gives $\cos(120°+2A)+\cos(120°-2A)=2\cos120°\cos2A=-\cos2A$, so the bracket
   cancels to zero and the left side is $\frac32$.
**6.** $\tan\theta=\frac{45}{45}=1$, so the elevation is $45°$.
**7.** The centre is the midpoint $(4,5)$ and
   $r=\frac12\sqrt{(6-2)^2+(7-3)^2}=\frac12\sqrt{32}=2\sqrt{2}$, so
   $(x-4)^2+(y-5)^2=8$.
**8.** $\overrightarrow{AB}=2\hat i+4\hat j$ and
   $\overrightarrow{BC}=2\hat i+4\hat j$. The two are equal, hence parallel, and
   they share the point $B$; so the three points lie on one line. (The slope
   check agrees: $A$ to $C$ has slope $\frac{11-3}{5-1}=2$.)
**9.** $(0\times(-1)+(-1)\times4,\;1\times(-1)+0\times4)=(-4,-1)$. The matrix
   sends $(1,0)$ to $(0,1)$, so it rotates a point through $90°$ anticlockwise
   about the origin: a **rotation**.
**10.** Cancelling gives $x+2\to4$, so $k=4$.
**11.** $\frac{\sigma}{\bar x}\times100=\frac{4}{20}\times100=20\%$.
:::

::: note Group D — solutions
**1.** $a+b=26$ and $ab=144$; the roots of $t^2-26t+144=0$ are
   $t=\frac{26\pm\sqrt{676-576}}{2}=\frac{26\pm10}{2}=18$ and $8$. The numbers
   are **18 and 8**. Check: $\frac{18+8}{2}=13$ ✓ and $\sqrt{144}=12$ ✓.
**2.** $A+B=180°-C$, so $\tan(A+B)=-\tan C$. Also
   $\tan(A+B)=\frac{\tan A+\tan B}{1-\tan A\tan B}$. Cross-multiplying,
   $\tan A+\tan B=-\tan C+\tan A\tan B\tan C$; adding $\tan C$ to both sides
   gives the identity.
**3.** Let $h$ be the height and $x$ the distance from the nearer point to the
   foot. From the nearer point, $\tan60°=\frac{h}{x}$, so $x=\frac{h}{\sqrt{3}}$.
   From the farther point, $\tan30°=\frac{h}{x+40}$, so $x+40=h\sqrt{3}$.
   Substituting: $\frac{h}{\sqrt{3}}+40=h\sqrt{3}$, so
   $40=h\left(\sqrt{3}-\frac{1}{\sqrt{3}}\right)=\frac{2h}{\sqrt{3}}$, giving
   $h=20\sqrt{3}\approx34.64$ m. Check: $x=20$ m and $x+40=60$ m;
   $\frac{34.64}{60}=0.577=\tan30°$ ✓.
**4.** Substitute the line into the circle:
   $x^2+(px+1)^2=4$, so $(1+p^2)x^2+2px-3=0$. Touching means exactly one
   solution, so the discriminant is zero:
   $4p^2-4(1+p^2)(-3)=0$, that is $4p^2+12+12p^2=0$ and $16p^2=-12$. That has
   no real solution, so **no real value of $p$** makes the line touch the
   circle. Check why: the line $y=px+1$ always passes through $(0,1)$, which is
   inside the circle of radius 2, so it must cut the circle twice for every
   real $p$ — a line through an interior point can never be a tangent. The
   algebra and the picture agree.
:::

## 19.4 Ranked practice priorities

The order below is a judgement from the grid and the syllabus. Rank 1 means
"rehearse this until it is automatic"; a low rank means "less likely to be
asked", never "skip it".

| Rank | Item | Why it ranks here |
|---|---|---|
| 1 | A system of two linear equations by matrix or Cramer's rule | Unit 3 has a guaranteed group B or C slot and the method never changes |
| 2 | An arithmetic or geometric sequence problem | Unit 1 is the easiest C-mark in the paper and appears in A and B too |
| 3 | Height and distance with one or two triangles | Unit 5 contains both a C item and, often, the D item; the method is three lines |
| 4 | Trigonometric identity proof using $\sin2A$, $\cos2A$ or the sum-to-product rules | Unit 4 supplies a C and frequently a D question |
| 5 | Circle: centre, radius, equation through given points | Unit 7 is a dependable B or C slot with a fixed recipe |
| 6 | Vectors: dot product, perpendicularity, collinearity | Unit 8 appears in all four groups in different years |
| 7 | Standard deviation or coefficient of variation of a small set | Unit 11 gives a C or D question with a fixed table method |
| 8 | Linear programming: maximise an objective at a corner | Unit 9's longer item is almost always the same shape |
| 9 | Remainder and factor theorem, inverse function, composite | Unit 12 questions are short and heavily practised |
| 10 | Limit by cancelling a common factor | Unit 10 is usually a single A or B item |
| 11 | Angle between two lines; perpendicularity condition | Unit 6 supplies mostly one-mark items |
| 12 | Graph of a quadratic and its vertex | Unit 2's graph item appears only when a graph question is set |

```figure caption="The four content blocks that carry most of the paper, as a share of the 75 marks. Rehearsing the top four ranks covers roughly two-thirds of the paper before a single low-rank topic is touched."
import matplotlib.pyplot as plt
labels = ["Algebra and\nsequences", "Trigonometry", "Geometry and\nvectors", "Statistics and\nmodelling"]
vals = [22, 16, 21, 16]
fig, ax = plt.subplots(figsize=(4.7, 2.5))
ax.bar(labels, vals, color=[ACCENT, SERIES[1], SERIES[2], SERIES[3]], width=0.6)
for i, v in enumerate(vals):
    ax.text(i, v + 0.5, str(v), ha="center", fontsize=9, color=INK)
ax.set_ylim(0, 26)
ax.set_ylabel("marks", fontsize=8)
ax.tick_params(labelsize=7.5, length=0)
ax.spines[["top", "right"]].set_visible(False)
ax.yaxis.grid(True, color=GRID, lw=0.6)
ax.set_axisbelow(True)
fig.tight_layout()
```

::: tip The last week before the paper
Work top-down through the table. For each rank, do **five** items from the
matching section of the unit-wise bank and mark them yourself against the
solutions. Five clean items in a topic is enough to make the method automatic;
ten is wasted time you could spend on the next rank. Then sit both model papers
in 19.2 and 19.3 **under the clock, in one sitting each**, and mark them by
method step.
:::

## 19.5 Three answers written the way the marker pays for them

Reading a solution is not the same as writing one. The three answers below take
a question of each of the three scored lengths and lay the working out in the
order that collects the method marks. The open circles on the figure mark the
point in each answer where the marker's pen comes down.

```figure caption="Where the marks sit inside a 2-mark, a 3-mark and a 4-mark answer. The final answer line is one mark of the three in a Group C item; the other two are earned before it."
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.7, 2.5))
rows = ["2 marks", "3 marks", "4 marks"]
setup = [0.5, 0.5, 0.5]
method = [0.5, 1.5, 2.0]
result = [1.0, 1.0, 1.5]
y = [2, 1, 0]
ax.barh(y, setup, height=0.5, color=MUTED, label="reading the question and setting up")
ax.barh(y, method, left=setup, height=0.5, color=ACCENT, label="visible method, one line per step")
ax.barh(y, result, left=[a + b for a, b in zip(setup, method)], height=0.5,
        color=SERIES[1], label="answer with units and a check")
for i, lbl in enumerate(rows):
    ax.text(0.08, y[i] - 0.42, lbl, fontsize=8, color=INK)
ax.set_xlim(0, 4.6); ax.set_yticks([])
ax.set_xlabel("marks earned", fontsize=8)
ax.tick_params(labelsize=8, length=0)
ax.legend(fontsize=7.5, frameon=False, loc="lower right")
ax.spines[["top", "right", "left"]].set_visible(False)
ax.xaxis.grid(True, color=GRID, lw=0.6)
ax.set_axisbelow(True)
fig.tight_layout()
```

::: example A 2-mark answer: state and substitute
**Question.** Find the value of $k$ for which $2x^2+kx+8=0$ has equal roots.

**Model answer.**
(1) A quadratic has equal roots when its discriminant is zero: $b^2-4ac=0$.
(2) Here $a=2$, $b=k$, $c=8$, so $k^2-4(2)(8)=0$, giving $k^2=64$ and
$k=\pm8$.

Two lines, two marks: one for the condition, one for the value. Note that the
answer is not $8$ but $\pm8$ — both signs satisfy the condition, and a marker
looking for "both values" will deduct for one.
:::

::: example A 3-mark answer: the matrix method laid out
**Question.** Solve by the matrix method: $3x+2y=12$, $2x-y=1$.

**Model answer.**
(1) In the form $AX=B$, the coefficient matrix has rows $(3,2)$ and $(2,-1)$.
Its determinant is $|A|=3(-1)-2(2)=-7$, which is not zero, so the inverse
exists.
(2) The inverse is $-\frac17$ times the matrix with rows $(-1,-2)$ and $(-2,3)$.
(3) Then

$$x=\frac{(-1)(12)+(-2)(1)}{-7}=\frac{-14}{-7}=2,\qquad
y=\frac{(-2)(12)+(3)(1)}{-7}=\frac{-21}{-7}=3$$

**Check.** $3(2)+2(3)=12$ ✓ and $2(2)-3=1$ ✓, so $x=2$, $y=3$.

Three marks: one for the determinant and the inverse, one for the
multiplication with the signs carried, one for the answer. The check line costs
four seconds and protects all three.
:::

::: example A 4-mark answer: the two-triangle problem
**Question.** The angle of elevation of the top of a tower from a point on the
ground is $30°$. Walking 40 m nearer, the elevation becomes $60°$. Find the
height of the tower.

**Model answer.**
(1) **Draw and name.** Let the height be $h$ and let $x$ be the horizontal
distance from the nearer point to the foot of the tower. The farther point is
then $x+40$ from the foot.
(2) **Write the two tangents.** From the nearer point,
$\tan60°=\frac{h}{x}$, so $x=\frac{h}{\sqrt{3}}$. From the farther point,
$\tan30°=\frac{h}{x+40}$, so $x+40=h\sqrt{3}$.
(3) **Eliminate $x$.** Substituting, $\frac{h}{\sqrt{3}}+40=h\sqrt{3}$, so
$40=h\sqrt{3}-\frac{h}{\sqrt{3}}=\frac{2h}{\sqrt{3}}$, giving
$h=20\sqrt{3}$.
(4) **Answer and check.** $h\approx34.64$ m. Check: $x=20$ m, so the farther
point is 60 m away and $\frac{34.64}{60}=0.577=\tan30°$ ✓.

Four marks: one for the diagram and the naming, one for each tangent equation,
one for the elimination, one for the value with a check. A bare "34.64 m" with
no diagram earns at most one.
:::


## Chapter summary

- The Optional Mathematics paper is **10 + 16 + 33 + 16 = 75** marks in three
  hours. Groups C and D alone carry 49 of those marks.
- A realistic clock is 10 minutes for Group A, 24 for B, 44 for C, 24 for D and
  18 minutes to check. A Group A item that stalls past 90 seconds is marked and
  left.
- Group A rewards formula recall; Group B rewards one short method; Groups C
  and D reward a complete, visible method with the answer substituted back.
- The five ranks worth rehearsing first are: a two-equation linear system, a
  sequence problem, height and distance, a trigonometric identity and the
  circle work.
- Both model papers are original practice items built to the CDC grid. They are
  a rehearsal, not a forecast: no one outside the board knows the paper.
