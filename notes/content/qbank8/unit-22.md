---
subject: Question Bank
grade: 8
unit: 22
title: "Optional Mathematics: Model Question Sets and Predicted Questions"
hours: 0
area: Optional Mathematics
---

This chapter does three jobs. It sets out the **pattern** of the 50-mark Optional Mathematics paper used throughout this bank and shows where each unit's marks come from; it gives **two complete model papers**, each of 50 marks and two hours, with a full solution to every question; and it closes with a **ranked list of practice priorities**, each with the reason it holds its place. Sit each model paper in one go, with a clock, before you look at the solutions.

::: caution What "predicted" means here, and what it does not
Optional Mathematics in grade 8 is set and marked by your own school, so no outsider knows your paper. The ranks in section 22.4 rest only on the paper's pattern and on the syllabus: a high rank means **practise this first**, never "this will come"; a low rank means "less likely to carry many marks", never "safe to skip". Every question in this chapter is an original practice item; none is copied from any school's paper.
:::

::: key The pattern: 50 marks in 2 hours
| Group | Questions | Marks each | Total | What it asks for |
|---|---|---|---|---|
| A | 10 | 1 | 10 | one-step recall or one substitution (multiple choice) |
| B | 10 | 2 | 20 | one short method, two or three lines |
| C | 5 | 4 | 20 | a full method: figure or table, formula, working, checked answer |
| **Total** | **25** | | **50** | 2 hours |

Groups B and C carry 40 of the 50 marks. A student who is quick in Group A but writes no working in B and C scores far less than one who is slow in A and shows every step in C.
:::

## 22.1 What the paper looks like

### Where the marks of each unit come from

The two model papers follow the same blueprint: every unit has one Group A item, the shorter units take one or two Group B questions, and the five Group C questions go to the units whose methods take a full page.

```figure caption="The blueprint of the model papers: marks per unit, split by group. Trigonometry (9 marks) and coordinate geometry (7) are the heaviest; vector, transformation and statistics each carry a 4-mark question."
fig, ax = plt.subplots(figsize=(5.2, 3.7))
units = ['1 Relation and Function', '2 Polynomials', '3 Sequence and Series', '4 Limit', '5 Matrix',
         '6 Coordinate Geometry', '7 Trigonometry', '8 Vector', '9 Transformation', '10 Statistics']
A = [1]*10; B = [4, 2, 2, 2, 4, 2, 4, 0, 0, 0]; C = [0, 0, 0, 0, 0, 4, 4, 4, 4, 4]
y = np.arange(10)[::-1]
ax.barh(y, A, color=MUTED, height=0.62, label='Group A')
ax.barh(y, B, left=A, color=ACCENT, height=0.62, label='Group B')
ax.barh(y, C, left=[a + b for a, b in zip(A, B)], color=SERIES[1], height=0.62, label='Group C')
for yi, a, b, c in zip(y, A, B, C):
    ax.text(a + b + c + 0.15, yi, str(a + b + c), va='center', fontsize=8.5)
ax.set_yticks(y); ax.set_yticklabels(units, fontsize=8)
ax.set_xlim(0, 11); ax.set_xticks(range(0, 11, 2)); ax.set_xlabel('marks', fontsize=8.5)
ax.legend(fontsize=8, frameon=False, loc='lower right')
ax.grid(axis='x', color=GRID, lw=0.6); ax.set_axisbelow(True)
ax.spines[['top', 'right', 'left']].set_visible(False); ax.tick_params(labelsize=8, length=0)
fig.tight_layout(pad=0.4)
```

| Unit | Group A | Group B | Group C | Marks |
|---|---|---|---|---|
| 1. Relation and Function | 1 | 2 questions | | 5 |
| 2. Polynomials | 1 | 1 question | | 3 |
| 3. Sequence and Series | 1 | 1 question | | 3 |
| 4. Limit | 1 | 1 question | | 3 |
| 5. Matrix | 1 | 2 questions | | 5 |
| 6. Coordinate Geometry | 1 | 1 question | 1 question | 7 |
| 7. Trigonometry | 1 | 2 questions | 1 question | 9 |
| 8. Vector | 1 | | 1 question | 5 |
| 9. Transformation | 1 | | 1 question | 5 |
| 10. Statistics | 1 | | 1 question | 5 |
| **Total** | **10** | **10 (20 marks)** | **5 (20 marks)** | **50** |

Your school may share the marks differently; the point of a blueprint is that **every unit appears**. Four chapters left unread cost at least four Group A marks and probably a long question as well.

::: tip A timing plan that fits the paper
Reading the paper: **5 minutes**. Group A: **15 minutes** (90 seconds an item at most). Group B: **40 minutes** (4 minutes a question). Group C: **50 minutes** (10 minutes a question). Checking: **10 minutes**. If a Group A item stalls, mark your best choice, put a dot beside it and come back at the end. Start Group C by the 60-minute mark, even if two Group B questions are left; return to them after Group C.
:::

## 22.2 Model Set 1

**Optional Mathematics — Class 8. Time: 2 hours. Full marks: 50.**
**Attempt all questions.**

### Question paper

**Group A — Choose the correct answer. $[10\times1=10]$**

1. If $n(A)=3$ and $n(B)=5$, the number of elements in $A\times B$ is
   (a) 8 (b) 15 (c) 2 (d) 125
2. The degree of the polynomial $5x^2y-3xy+7$ is
   (a) 2 (b) 3 (c) 5 (d) 1
3. The 10th term of $3, 7, 11, 15, \ldots$ is
   (a) 39 (b) 40 (c) 43 (d) 37
4. $\lim_{x\to1}(x^2+3x)$ is
   (a) 1 (b) 3 (c) 4 (d) 0
5. A square matrix whose elements off the leading diagonal are all zero is a
   (a) row matrix (b) diagonal matrix (c) zero matrix (d) column matrix
6. The slope of the line joining $(2,-1)$ and $(6,7)$ is
   (a) 2 (b) $\frac{1}{2}$ (c) 3 (d) $-2$
7. $\left(\frac{3\pi}{4}\right)^c$ in degrees is
   (a) $120^\circ$ (b) $135^\circ$ (c) $150^\circ$ (d) $270^\circ$
8. The magnitude of $\binom{5}{-12}$ is
   (a) 7 (b) 17 (c) 13 (d) 60
9. The image of $(-3,4)$ under rotation through $180^\circ$ about the origin is
   (a) $(3,-4)$ (b) $(-4,-3)$ (c) $(4,3)$ (d) $(3,4)$
10. The median of 7, 3, 9, 5, 11 is
    (a) 5 (b) 7 (c) 9 (d) 7.5

**Group B — Answer in short. $[10\times2=20]$**

1. Find $x$ and $y$ if $(x+y,\ 2)=(8,\ x-y)$.
2. If $f(x)=3x-2$ and $f(a)=13$, find $a$. Also find $f(-1)$.
3. Multiply $(x-4)(x^2+x+2)$.
4. Expand and evaluate $\sum_{k=1}^{5}(2k+1)$.
5. Evaluate $\lim_{x\to3}\frac{x^2-9}{x-3}$.
6. If $A=[(2,5),(-1,3)]$ and $B=[(4,-2),(6,1)]$, find $A+B$.
7. Find $x$ and $y$ if $[(x+2,\ 3),(4,\ 2y)]=[(7,\ 3),(4,\ 8)]$.
8. Find the mid-point of the line joining $(-3,7)$ and $(5,-1)$.
9. If $\tan\theta=\frac{5}{12}$ and $\theta$ is acute, find $\sin\theta$ and $\cos\theta$.
10. Find the value of $\sin60^\circ\cos30^\circ+\cos60^\circ\sin30^\circ$.

**Group C — Answer with working. $[5\times4=20]$**

1. The vertices of a triangle are $A(-1,2)$, $B(3,-1)$ and $C(6,3)$. (i) Show that the triangle is isosceles and right-angled. (ii) Find its area.
2. A ladder leans against a vertical wall. Its foot is 4 m from the wall and it makes an angle of $60^\circ$ with the ground. Draw a figure and find the length of the ladder and the height of the wall it reaches.
3. If $\vec{a}=\binom{2}{-1}$, $\vec{b}=\binom{1}{3}$ and $\vec{c}=\binom{-4}{2}$, find (i) $\vec{a}+\vec{b}$ and its magnitude (ii) $2\vec{a}-\vec{b}+\vec{c}$. (iii) Show that $\vec{c}$ is parallel to $\vec{a}$ and say whether they are like or unlike.
4. The triangle $P(1,2)$, $Q(4,2)$, $R(2,5)$ is (i) reflected in the $y$-axis, and (ii) rotated through $+90^\circ$ about the origin. Find both images, draw all three triangles on one graph, and show that $PQ=P'Q'$.
5. The marks of 50 students are: 0–10: 5, 10–20: 8, 20–30: 15, 30–40: 12, 40–50: 10. Find the mean and the mode.

### Solutions

::: note Group A — answers with reasons
**1.** (b) — $n(A\times B)=3\times5=15$.
**2.** (b) — the term $5x^2y$ has degree $2+1=3$.
**3.** (a) — $t_n=4n-1$, so $t_{10}=39$.
**4.** (c) — substitute: $1+3=4$.
**5.** (b) — that is the definition of a diagonal matrix.
**6.** (a) — $\frac{7+1}{6-2}=2$.
**7.** (b) — $\frac{3\times180^\circ}{4}=135^\circ$.
**8.** (c) — $\sqrt{25+144}=13$.
**9.** (a) — both signs change.
**10.** (b) — in order 3, 5, 7, 9, 11; the middle value is 7.
:::

::: note Group B — solutions
**1.** $x+y=8$ and $2=x-y$. Adding, $2x=10$, so $x=5$ and $y=3$.
**2.** $3a-2=13$, so $a=5$. $f(-1)=-3-2=-5$.
**3.** $x^3+x^2+2x-4x^2-4x-8=x^3-3x^2-2x-8$.
**4.** $3+5+7+9+11=35$.
**5.** $\frac{(x-3)(x+3)}{x-3}=x+3\rightarrow6$.
**6.** $A+B=[(2+4,\ 5-2),(-1+6,\ 3+1)]=[(6,3),(5,4)]$.
**7.** $x+2=7$ gives $x=5$; $2y=8$ gives $y=4$.
**8.** $\left(\frac{-3+5}{2},\frac{7-1}{2}\right)=(1,3)$.
**9.** $p=5$, $b=12$, $h=\sqrt{25+144}=13$: $\sin\theta=\frac{5}{13}$, $\cos\theta=\frac{12}{13}$.
**10.** $\frac{\sqrt{3}}{2}\cdot\frac{\sqrt{3}}{2}+\frac{1}{2}\cdot\frac{1}{2}=\frac{3}{4}+\frac{1}{4}=1$.
:::

::: note Group C — solutions
**1.** (i) $AB^2=4^2+(-3)^2=25$, $BC^2=3^2+4^2=25$, $AC^2=7^2+1^2=50$. So $AB=BC=5$ (isosceles) and $AB^2+BC^2=50=AC^2$, so the angle at $B$ is a right angle. (ii) Area $=\frac{1}{2}\times AB\times BC=\frac{1}{2}\times5\times5=12.5$ square units. Check: $\frac{1}{2}\left|-1(-1-3)+3(3-2)+6(2+1)\right|=\frac{1}{2}(4+3+18)=12.5$ ✓.
**2.** **Figure:** the wall vertical, the ground horizontal, the ladder as the hypotenuse; foot 4 m from the wall, angle $60^\circ$ at the foot. Length: $\cos60^\circ=\frac{4}{L}$, so $L=\frac{4}{\frac{1}{2}}=8$ m. Height: $\tan60^\circ=\frac{h}{4}$, so $h=4\sqrt{3}\approx6.93$ m. Check: $4^2+(4\sqrt{3})^2=16+48=64=8^2$ ✓.
**3.** (i) $\vec{a}+\vec{b}=\binom{3}{2}$, magnitude $\sqrt{9+4}=\sqrt{13}\approx3.61$. (ii) $2\vec{a}-\vec{b}+\vec{c}=\binom{4-1-4}{-2-3+2}=\binom{-1}{-3}$. (iii) $\vec{c}=\binom{-4}{2}=-2\binom{2}{-1}=-2\vec{a}$: parallel, and **unlike** because the scalar is negative.
**4.** (i) Reflection in the $y$-axis, $(x,y)\rightarrow(-x,y)$: $P'(-1,2)$, $Q'(-4,2)$, $R'(-2,5)$. (ii) Rotation $+90^\circ$, $(x,y)\rightarrow(-y,x)$: $P''(-2,1)$, $Q''(-2,4)$, $R''(-5,2)$. On the graph the object is in quadrant I and both images in quadrant II. $PQ=4-1=3$ and $P'Q'=|-4-(-1)|=3$, so $PQ=P'Q'$.
**5.** Mid-values 5, 15, 25, 35, 45; $\sum fm=25+120+375+420+450=1390$; $N=50$; mean $=\frac{1390}{50}=27.8$ marks. Modal class 20–30 with $L=20$, $f_1=15$, $f_0=8$, $f_2=12$, $i=10$: $M_o=20+\frac{15-8}{30-8-12}\times10=20+\frac{7}{10}\times10=27$ marks.
:::

::: caution Two Group C slips that this set is built to catch
In question 1 the right angle is at $B$, the vertex **opposite** the longest side $AC$, not at $A$. In question 5 the denominator of the mode formula is $2f_1-f_0-f_2=30-8-12$, not $f_1-f_0-f_2$. Both slips give answers that look reasonable; only the habit of writing the formula first prevents them.
:::

## 22.3 Model Set 2

**Optional Mathematics — Class 8. Time: 2 hours. Full marks: 50.**
**Attempt all questions.**

### Question paper

**Group A — Choose the correct answer. $[10\times1=10]$**

1. The inverse of the relation $\{(1,4),(2,5),(3,6)\}$ is
   (a) $\{(4,1),(5,2),(6,3)\}$ (b) $\{(1,4),(2,5),(3,6)\}$ (c) $\{(4,5),(5,6)\}$ (d) $\{(1,2),(4,5)\}$
2. Which of these is a cubic binomial?
   (a) $x^3+2x+1$ (b) $4x^3-5$ (c) $x^2-9$ (d) $7x^3$
3. $\sum_{k=1}^{4}2k$ is equal to
   (a) 8 (b) 10 (c) 20 (d) 16
4. The sequence $0.3, 0.33, 0.333, \ldots$ tends to
   (a) 0.3 (b) $\frac{1}{3}$ (c) 3 (d) 0
5. If $A=[(1,2),(3,4)]$, then $3A$ is
   (a) $[(3,6),(9,12)]$ (b) $[(3,2),(3,4)]$ (c) $[(4,5),(6,7)]$ (d) $[(1,6),(9,4)]$
6. The area of the triangle with vertices $(0,0)$, $(5,0)$ and $(0,6)$ is
   (a) 30 (b) 15 (c) 11 (d) 60
7. The value of $\sin^230^\circ+\cos^230^\circ$ is
   (a) 0 (b) $\frac{1}{2}$ (c) 1 (d) 2
8. If $\binom{3}{k}$ is parallel to $\binom{6}{8}$, then $k$ is
   (a) 4 (b) 3 (c) 6 (d) 2
9. Translation by $\binom{2}{-3}$ maps $(-1,5)$ to
   (a) $(1,2)$ (b) $(-3,8)$ (c) $(1,8)$ (d) $(-2,-15)$
10. The coefficient of range of 12, 20, 8, 32 is
    (a) 24 (b) 0.6 (c) 0.4 (d) 1.5

**Group B — Answer in short. $[10\times2=20]$**

1. If $A=\{2,3\}$ and $B=\{4,6\}$, write the relation $R=\{(x,y): x \text{ is a factor of } y\}$ from $A$ to $B$ as a set of ordered pairs.
2. State, with a reason, whether $\{(1,2),(2,3),(3,2),(4,5)\}$ is a function, and write its range.
3. Find $a$ and $b$ if $(a+b)x^2+(a-b)x=9x^2+3x$.
4. Find the general term and the 20th term of $7, 12, 17, 22, \ldots$.
5. Evaluate $\lim_{x\to2}\frac{x^2+3x-10}{x-2}$.
6. If $A=[(5,-1),(2,0)]$ and $B=[(1,3),(-2,4)]$, find $2A-B$.
7. Construct the $2\times3$ matrix $A=[a_{ij}]$ with $a_{ij}=3i-j$.
8. Find the equation of the line through $(1,4)$ and $(3,10)$ in the form $y=mx+c$.
9. Convert $67.5^\circ$ into grades and into radians.
10. Prove that $\sin\theta\sec\theta=\tan\theta$.

**Group C — Answer with working. $[5\times4=20]$**

1. $A$ is $(-2,3)$ and $B$ is $(8,-2)$. (i) Find the point $P$ that divides $AB$ internally in the ratio $3:2$. (ii) Find the equation of the line $AB$ in the form $y=mx+c$. (iii) Show that $P$ lies on this line.
2. (i) Prove that $(1-\cos^2\theta)(1+\cot^2\theta)=1$. (ii) Find the value of $\cos120^\circ+\sin150^\circ+\tan135^\circ$.
3. The points are $P(-1,-2)$, $Q(1,2)$ and $R(3,6)$. (i) Find $\overrightarrow{PQ}$ and $\overrightarrow{QR}$. (ii) Show that $P$, $Q$, $R$ are collinear and find $PQ:QR$. (iii) Find the unit vector in the direction of $\overrightarrow{PR}$.
4. The triangle $A(1,3)$, $B(2,1)$, $C(4,2)$ is rotated through $-90^\circ$ about the origin, and the image is then reflected in the $x$-axis. Find both images and describe what happens to the coordinates of a general point.
5. The weights (in kg) of 11 students are 38, 42, 35, 47, 40, 44, 39, 50, 36, 41, 45. Find the median, the first and third quartiles, the range and the coefficient of range.

### Solutions

::: note Group A — answers with reasons
**1.** (a) — swap the components of each pair.
**2.** (b) — highest power 3 and two terms.
**3.** (c) — $2+4+6+8=20$.
**4.** (b) — the gaps $\frac{1}{30}, \frac{1}{300}, \ldots$ to $\frac{1}{3}$ shrink to 0.
**5.** (a) — multiply every element by 3.
**6.** (b) — a right triangle with legs 5 and 6: $\frac{1}{2}\times5\times6=15$.
**7.** (c) — $\sin^2\theta+\cos^2\theta=1$ for every angle.
**8.** (a) — $3\times8-6k=0$ gives $k=4$.
**9.** (a) — $(-1+2,\ 5-3)$.
**10.** (b) — $L=32$, $S=8$: $\frac{24}{40}=0.6$.
:::

::: note Group B — solutions
**1.** 2 divides 4 and 6; 3 divides 6 but not 4. So $R=\{(2,4),(2,6),(3,6)\}$.
**2.** It **is** a function: the first components 1, 2, 3, 4 are all different, so each has exactly one image. Range $=\{2,3,5\}$.
**3.** $a+b=9$ and $a-b=3$, so $a=6$ and $b=3$.
**4.** The difference is 5 and each term is 2 more than $5n$: $t_n=5n+2$, so $t_{20}=102$.
**5.** $\frac{(x+5)(x-2)}{x-2}=x+5\rightarrow7$.
**6.** $2A=[(10,-2),(4,0)]$, so $2A-B=[(9,-5),(6,-4)]$.
**7.** $a_{11}=2$, $a_{12}=1$, $a_{13}=0$, $a_{21}=5$, $a_{22}=4$, $a_{23}=3$: $A=[(2,1,0),(5,4,3)]$.
**8.** $m=\frac{10-4}{3-1}=3$; $4=3(1)+c$ gives $c=1$. So $y=3x+1$. Check with $(3,10)$: $9+1=10$ ✓.
**9.** $67.5\times\frac{10}{9}=75^g$; $67.5\times\frac{\pi}{180}=\frac{3\pi}{8}$ radians.
**10.** LHS $=\sin\theta\times\frac{1}{\cos\theta}=\frac{\sin\theta}{\cos\theta}=\tan\theta=$ RHS.
:::

::: note Group C — solutions
**1.** (i) $P=\left(\frac{3(8)+2(-2)}{5},\ \frac{3(-2)+2(3)}{5}\right)=\left(\frac{20}{5},\frac{0}{5}\right)=(4,0)$. (ii) $m=\frac{-2-3}{8+2}=-\frac{1}{2}$; through $A$: $3=-\frac{1}{2}(-2)+c$, so $c=2$ and the line is $y=-\frac{1}{2}x+2$. (iii) At $x=4$: $y=-2+2=0$, so $P(4,0)$ lies on $AB$ ✓.
**2.** (i) LHS $=\sin^2\theta\times\mathrm{cosec}^2\theta=\sin^2\theta\times\frac{1}{\sin^2\theta}=1=$ RHS. (ii) $\cos120^\circ=-\cos60^\circ=-\frac{1}{2}$, $\sin150^\circ=\sin30^\circ=\frac{1}{2}$, $\tan135^\circ=-\tan45^\circ=-1$. The value is $-\frac{1}{2}+\frac{1}{2}-1=-1$.
**3.** (i) $\overrightarrow{PQ}=\binom{2}{4}$ and $\overrightarrow{QR}=\binom{2}{4}$. (ii) The vectors are equal, hence parallel, and share $Q$, so $P$, $Q$, $R$ are collinear; $PQ:QR=1:1$ ($Q$ is the mid-point of $PR$). (iii) $\overrightarrow{PR}=\binom{4}{8}$ with magnitude $\sqrt{80}=4\sqrt{5}$, so the unit vector is $\binom{\frac{1}{\sqrt{5}}}{\frac{2}{\sqrt{5}}}$.
**4.** $-90^\circ$, $(x,y)\rightarrow(y,-x)$: $A'(3,-1)$, $B'(1,-2)$, $C'(2,-4)$. Reflection in the $x$-axis: $A''(3,1)$, $B''(1,2)$, $C''(2,4)$. A general point goes $(x,y)\rightarrow(y,-x)\rightarrow(y,x)$: the coordinates are swapped (a reflection in the line $y=x$, met in grade 9).
**5.** In order: 35, 36, 38, 39, 40, 41, 42, 44, 45, 47, 50 ($n=11$). Median: 6th item $=41$ kg. $Q_1$: 3rd item $=38$ kg. $Q_3$: 9th item $=45$ kg. Range $=50-35=15$ kg; coefficient of range $=\frac{15}{85}=\frac{3}{17}\approx0.18$.
:::

## 22.4 Ranked practice priorities

The order below is a judgement from the pattern and the syllabus. **Tier A** is worth rehearsing until it is automatic; **Tier B** is the second pass; **Tier C** is a quick pass in the last week.

### Tier A — rehearse until automatic

| Rank | Topic and likely form | Marks | Why it ranks here |
|---|---|---|---|
| 1 | Height and distance with one angle of elevation or depression, with a labelled figure | 4 | Trigonometry is the heaviest unit, and this is its natural long question: figure, one ratio, one answer. |
| 2 | Mean (and mode) of grouped data from a frequency table | 4 | The statistics long question; a fixed table method that is easy to mark step by step. |
| 3 | Distance formula to classify a triangle or quadrilateral, with its area | 4 | Coordinate geometry carries 7 marks; one formula used three times, then the area formula. |
| 4 | Reflection, rotation or translation of a triangle, plotted on a graph | 4 | The transformation long question; four rules to know and a graph that checks itself. |
| 5 | Vectors: $\overrightarrow{AB}$, magnitude, sum, a parallel or collinear test | 4 | The vector long question; head minus tail and $x_1y_2=x_2y_1$ do most of the work. |
| 6 | Proving a trigonometric identity | 2 or 4 | Appears in Group B and as part of a long question; the method (one side, sin and cos) never changes. |

### Tier B — second pass

| Rank | Topic and likely form | Marks | Why it ranks here |
|---|---|---|---|
| 7 | Trigonometric ratios: all six from one ratio, standard values, and allied angles such as $120^\circ$, $135^\circ$, $210^\circ$, $-60^\circ$ | 1 or 2 | Trigonometry has two Group B slots; the standard-value table and the two-step allied-angle rule (name, then sign) answer most of them. |
| 8 | Degrees, grades and radians, including the angles of a triangle | 1 or 2 | Short conversions; the minutes-to-decimal step catches many students. |
| 9 | Matrices: constructing from a rule, addition, subtraction, scalar multiples, unknowns from equal matrices | 2 | Matrix has two Group B slots; every question is element-by-element arithmetic. |
| 10 | Equal ordered pairs, the Cartesian product, and relations with their domain, range and inverse | 1 or 2 | The first topic of the book and a favourite short question. |
| 11 | Functions: "is it a function?", values, pre-images, and $f(x)=ax+b$ from two values | 2 | A Group B regular; the reason must be stated in words. |
| 12 | Section formula, mid-point, points of trisection | 2 or 4 | Often the second part of a coordinate long question. |
| 13 | Slope of a line and $y=mx+c$ | 1 or 2 | One substitution each; remember to make $y$ the subject. |

### Tier C — a quick pass before the paper

| Rank | Topic and likely form | Marks | Why it ranks here |
|---|---|---|---|
| 14 | Limits: of a sequence, and of a $\frac{0}{0}$ form by factorising and cancelling | 1 or 2 | One method, usually one short question. |
| 15 | General term, "is it a term?", and sigma expansion | 1 or 2 | One Group B slot; the method of differences covers most forms. |
| 16 | Multiplying polynomials and equal polynomials | 1 or 2 | One Group B slot; check by substituting a number. |
| 17 | Median, quartiles, range and coefficient of range of individual data | 1 or 4 | May appear instead of grouped data in the statistics question. |
| 18 | Types of matrix and the symmetric-matrix condition | 1 | Mostly a Group A item; learn the table of definitions. |

```figure caption="Marks of each model set sorted by tier. Tier A carries most of Set 1 (22 marks) and Tier B most of Set 2 (21 marks); together Tiers A and B cover 39 and 36 of the 50 marks, so Tier C can never be skipped entirely."
fig, ax = plt.subplots(figsize=(5.0, 2.6))
tiers = ['Tier A (ranks 1–6)', 'Tier B (ranks 7–13)', 'Tier C (ranks 14–18)']
s1 = [22, 17, 11]; s2 = [15, 21, 14]
y = np.arange(3)[::-1]; h = 0.36
ax.barh(y + h/2, s1, height=h, color=ACCENT, label='Model Set 1')
ax.barh(y - h/2, s2, height=h, color=SERIES[3], label='Model Set 2')
for yi, a, b in zip(y, s1, s2):
    ax.text(a + 0.4, yi + h/2, str(a), va='center', fontsize=8.5)
    ax.text(b + 0.4, yi - h/2, str(b), va='center', fontsize=8.5)
ax.set_yticks(y); ax.set_yticklabels(tiers, fontsize=8.5)
ax.set_xlim(0, 30); ax.set_xlabel('marks (of 50)', fontsize=8.5)
ax.legend(fontsize=8, frameon=False, loc='lower right')
ax.grid(axis='x', color=GRID, lw=0.6); ax.set_axisbelow(True)
ax.spines[['top', 'right', 'left']].set_visible(False); ax.tick_params(labelsize=8, length=0)
fig.tight_layout(pad=0.4)
```

Each question of the two model sets has been placed under the rank it practises, and the marks added up by tier. The chart shows how the two sets differ, not a forecast of any school's paper: the five long questions of Set 1 are all Tier A topics, while Set 2 gives one long question to the section formula (Tier B) and one to individual-data statistics (Tier C).

::: tip The last week before the paper
Work down the table. For each rank do **five** questions from the matching unit of the subjective bank (chapter 21) and mark them yourself. Then sit Model Set 1 and Model Set 2 **under the clock, in one sitting each**, and mark them by method step. Finish with the facts lines of the objective bank (chapter 20) on the night before the paper.
:::

## 22.5 Two answers written the way the marker pays

::: example A 2-mark answer: state, substitute, answer
**Question.** Evaluate $\lim_{x\to2}\frac{x^2+3x-10}{x-2}$.

**Model answer.** (1) Substitution gives $\frac{0}{0}$, so factorise: $\frac{x^2+3x-10}{x-2}=\frac{(x+5)(x-2)}{x-2}=x+5$ for $x\neq2$. (2) Therefore $\lim_{x\to2}(x+5)=2+5=7$.

One mark for the factorising and cancelling, one for the limit. Writing only "7" risks both marks, because the marker cannot see whether you understood the $\frac{0}{0}$ form.
:::

::: example A 4-mark answer: the height-and-distance question
**Question.** From the top of a tower 30 m high, the angle of depression of a car on the road is $60^\circ$. Find the distance of the car from the foot of the tower.

**Model answer.**
(1) **Figure.** Tower $AB=30$ m, with $A$ at the top; car at $C$; the horizontal through $A$; the $60^\circ$ angle of depression at $A$, equal to $\angle ACB$ (alternate angles).
(2) **Ratio.** In the right triangle $ABC$, $\tan60^\circ=\frac{AB}{BC}$.
(3) **Substitute and solve.** $\sqrt{3}=\frac{30}{BC}$, so $BC=\frac{30}{\sqrt{3}}=10\sqrt{3}$.
(4) **Answer with unit.** $BC\approx10\times1.732=17.32$ m.

Four marks: one for the labelled figure, one for choosing $\tan$ with the correct sides, one for the working, one for the answer with its unit. A bare "17.32 m" with no figure earns at most one.
:::

## Chapter summary

- The paper is **10 + 20 + 20 = 50** marks in two hours: ten 1-mark objective items, ten 2-mark short questions and five 4-mark long questions.
- In the blueprint every unit has one Group A item; trigonometry (9 marks) and coordinate geometry (7) are the heaviest; vector, transformation and statistics each have a long question.
- A workable clock: 5 minutes reading, 15 for Group A, 40 for Group B, 50 for Group C, 10 for checking.
- Group A rewards recall; Groups B and C reward visible method, a figure or table where one helps, and a checked answer.
- The six topics worth rehearsing first: height and distance, grouped mean and mode, distance-and-area in coordinates, transformations on a graph, vector operations, and trigonometric identities.
- Both model papers are rehearsals built to the pattern, not forecasts: no one outside your school knows its paper.
