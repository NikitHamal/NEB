---
subject: Question Bank
grade: 10
unit: 17
title: "Optional Mathematics: Unit-wise Objective Question Bank"
hours: 0
area: Optional Mathematics
---

Optional Mathematics is the paper where a single mark costs the least work and
the most care. Group A of the SEE paper carries **ten one-mark items** and the
first item of almost every later group is also a one-line recall, so roughly a
quarter of the paper can be won or lost on formulas that take ten seconds each.
This chapter drills those items unit by unit, in multiple-choice form, so that
every answer can be checked instantly and every mistake has a name.

Each section opens with a **facts line** — the four to six results that the
items in that section actually use — then gives items, then gives a key with a
one-line reason. Work an item in under a minute; correct it in ten seconds; move
on.

::: key The shape of the paper (CDC grid, 2082)
| Group | Items | Marks each | Total | What it tests |
|---|---|---|---|---|
| A | 10 | 1 | 10 | direct recall, single step |
| B | 8 | 2 | 16 | one short method |
| C | 11 | 3 | 33 | a full short-answer method |
| D | 4 | 4 | 16 | longer method, proof or construction |
| **Total** | **33** | | **75** | 3 hours |

Group A is 13% of the paper but takes about 10 of the 180 minutes. It is also
the only group with no method marks to fall back on: an item is right or it is
zero.
:::

::: caution Practice items, not past questions
Every item below is an original **practice** item written to the CDC pattern.
None is claimed to have appeared in a particular year's paper. Every numerical
answer has been recomputed independently before it was written down.
:::

```figure caption="Where the 75 marks of the Optional Mathematics paper sit. Group A is ten single marks — small, cheap and the easiest place to lose marks through a slipped formula."
import matplotlib.pyplot as plt
labels = ["A  10 x 1", "B  8 x 2", "C  11 x 3", "D  4 x 4"]
vals = [10, 16, 33, 16]
fig, ax = plt.subplots(figsize=(4.6, 2.4))
bars = ax.barh([3, 2, 1, 0], vals, height=0.58,
               color=[INK, MUTED, ACCENT, SERIES[1]])
for y, v in zip([3, 2, 1, 0], vals):
    ax.text(v + 0.7, y, str(v), va="center", fontsize=9, color=INK)
ax.set_yticks([3, 2, 1, 0]); ax.set_yticklabels(labels, fontsize=9)
ax.set_xlim(0, 40)
ax.set_xlabel("Marks out of 75", fontsize=8)
ax.tick_params(labelsize=8, length=0)
ax.spines[["top", "right", "left"]].set_visible(False)
ax.xaxis.grid(True, color=GRID, lw=0.6)
ax.set_axisbelow(True)
fig.tight_layout()
```


```figure caption="Actual practice-question coverage in this chapter. Counts describe this book, not examination weightage or the probability of a question appearing."
fig, ax = barh_ranked(
    ["Sequence and Series", "Quadratic Equations and Graphs", "Matrices and Determinants", "Trigonometry: Multiple, Submultiple and Transformation Formulas", "Conditional Identities, Trigonometric Equations and Height and Distance", "Angle between Two Lines and Pair of Straight Lines", "Conic Sections and Circle", "Vector", "Linear Programming and Transformation", "Continuity", "Statistics: Measures of Dispersion", "Functions and Polynomials"],
    [8, 8, 8, 10, 8, 6, 8, 8, 8, 6, 8, 8], unit=" questions")
```


## 17.1 Sequence and Series

**Facts.** For an arithmetic sequence, $t_n=a+(n-1)d$ and
$S_n=\frac{n}{2}\{2a+(n-1)d\}$. For a geometric sequence,
$t_n=ar^{n-1}$ and $S_n=\frac{a(r^n-1)}{r-1}$ for $r\ne1$. The arithmetic mean of
two numbers is $\frac{a+b}{2}$, the geometric mean is $\sqrt{ab}$, and for
positive numbers AM $\geq$ GM with equality only when the numbers are equal.

1. The 10th term of the sequence 3, 7, 11, ... is <span class="marks">[1]</span>
   (a) 35 (b) 39 (c) 40 (d) 43
2. The number of terms in the sequence 5, 8, 11, ..., 47 is <span class="marks">[1]</span>
   (a) 13 (b) 14 (c) 15 (d) 16
3. Which term of the sequence 2, 5, 8, ... is 65? <span class="marks">[1]</span>
   (a) 20th (b) 21st (c) 22nd (d) 23rd
4. The sum of the first 20 natural numbers is <span class="marks">[1]</span>
   (a) 190 (b) 200 (c) 210 (d) 420
5. The geometric mean of 4 and 9 is <span class="marks">[1]</span>
   (a) 6 (b) 6.5 (c) 13 (d) 36
6. If $a$ and $b$ are two unequal positive numbers, then <span class="marks">[1]</span>
   (a) AM $>$ GM (b) AM $<$ GM (c) AM $=$ GM (d) AM $=$ 2 GM
7. The 5th term of the geometric sequence 3, 6, 12, ... is <span class="marks">[1]</span>
   (a) 24 (b) 36 (c) 48 (d) 96
8. The sum of 2 + 6 + 18 + ... + 1458 is <span class="marks">[1]</span>
   (a) 2186 (b) 2187 (c) 1458 (d) 729

::: note Answers to 17.1
**1.** (b) — $a=3$, $d=4$, $t_{10}=3+9\times4=39$.
**2.** (c) — $47=5+(n-1)3$, so $n-1=14$ and $n=15$.
**3.** (c) — $65=2+(n-1)3$, so $n-1=21$ and $n=22$.
**4.** (c) — $S_{20}=\frac{20\times21}{2}=210$.
**5.** (a) — $\sqrt{4\times9}=\sqrt{36}=6$.
**6.** (a) — $(\sqrt{a}-\sqrt{b})^2>0$ gives $\frac{a+b}{2}>\sqrt{ab}$.
**7.** (c) — $t_5=3\times2^{4}=48$.
**8.** (a) — the last term is $2\times3^{6}$, so $S_7=\frac{2(3^7-1)}{3-1}=2186$.
:::

## 17.2 Quadratic Equations and Graphs

**Facts.** For $ax^2+bx+c=0$ the roots are $\frac{-b\pm\sqrt{b^2-4ac}}{2a}$; the
discriminant $D=b^2-4ac$ decides the nature (real and unequal for $D>0$, equal
for $D=0$, imaginary for $D<0$); the sum of the roots is $-\frac{b}{a}$ and the
product is $\frac{c}{a}$. The graph of $y=ax^2+bx+c$ is a parabola opening up
when $a>0$, and its vertex is at $x=-\frac{b}{2a}$.

1. The discriminant of $2x^2-5x+3=0$ is <span class="marks">[1]</span>
   (a) 1 (b) −1 (c) 49 (d) 25
2. The roots of $x^2-5x+6=0$ are <span class="marks">[1]</span>
   (a) 1, 6 (b) 2, 3 (c) −2, −3 (d) −1, −6
3. If the roots of $x^2+kx+9=0$ are equal, then $k$ is <span class="marks">[1]</span>
   (a) 3 (b) 6 (c) 9 (d) 81
4. The sum and the product of the roots of $3x^2-7x+2=0$ are <span class="marks">[1]</span>
   (a) $\frac{7}{3}$ and $\frac{2}{3}$ (b) $-\frac{7}{3}$ and $\frac{2}{3}$
   (c) $\frac{7}{3}$ and $-\frac{2}{3}$ (d) $\frac{3}{7}$ and $\frac{3}{2}$
5. The graph of $y=x^2-4x+3$ cuts the $x$-axis at <span class="marks">[1]</span>
   (a) $x=1$ and $x=3$ (b) $x=-1$ and $x=-3$ (c) $x=0$ and $x=4$ (d) $x=2$ only
6. The line of symmetry of the parabola $y=x^2-6x+5$ is <span class="marks">[1]</span>
   (a) $x=3$ (b) $x=-3$ (c) $x=6$ (d) $y=3$
7. If one root of $x^2-7x+c=0$ is 2, then $c$ is <span class="marks">[1]</span>
   (a) 2 (b) 5 (c) 10 (d) 14
8. The roots of $x^2+4=0$ are <span class="marks">[1]</span>
   (a) real and equal (b) real and unequal (c) imaginary (d) zero

::: note Answers to 17.2
**1.** (a) — $25-4\times2\times3=25-24=1$.
**2.** (b) — $x^2-5x+6=(x-2)(x-3)$.
**3.** (b) — equal roots need $k^2=4\times9=36$, so $k=\pm6$; of the options, 6.
**4.** (a) — sum $=-\frac{b}{a}=\frac{7}{3}$, product $=\frac{c}{a}=\frac{2}{3}$.
**5.** (a) — $x^2-4x+3=(x-1)(x-3)$, so $y=0$ at $x=1$ and $x=3$.
**6.** (a) — $x=-\frac{b}{2a}=\frac{6}{2}=3$.
**7.** (c) — $2$ is a root, so $4-14+c=0$ and $c=10$.
**8.** (c) — $D=0-16=-16<0$, so the roots are imaginary ($x=\pm2i$).
:::

```figure caption="The same quadratic read three ways. $y=x^2-6x+5$ crosses the axis where the factors vanish, and its lowest point sits on the line of symmetry $x=3$."
import numpy as np
import matplotlib.pyplot as plt
x = np.linspace(-0.5, 6.5, 400)
y = x**2 - 6*x + 5
fig, ax = plt.subplots(figsize=(4.6, 2.9))
ax.plot(x, y, color=ACCENT, lw=1.8)
ax.axhline(0, color=INK, lw=0.8)
ax.plot([1, 5], [0, 0], "o", color=SERIES[1], ms=5)
ax.axvline(3, color=MUTED, lw=1.0, ls="--")
ax.annotate("roots $x=1, 5$", xy=(1, 0), xytext=(0.05, 4.2), fontsize=8, color=INK)
ax.annotate("vertex $(3,-4)$", xy=(3, -4), xytext=(3.3, -3.1), fontsize=8, color=INK)
ax.text(3.08, 5.6, "axis $x=3$", fontsize=8, color=MUTED)
ax.set_xlim(-0.5, 6.5); ax.set_ylim(-6, 8)
ax.set_xlabel("x", fontsize=9); ax.set_ylabel("y", fontsize=9)
ax.tick_params(labelsize=8, length=0)
ax.spines[["top", "right"]].set_visible(False)
ax.grid(True, color=GRID, lw=0.6)
ax.set_axisbelow(True)
fig.tight_layout()
```

## 17.3 Matrices and Determinants

**Facts.** A matrix with $m$ rows and $n$ columns has order $m\times n$; two
matrices can be added only when their orders match, and multiplied only when
the columns of the first equal the rows of the second. For a square matrix of
order 2 with rows $(a,b)$ and $(c,d)$, the determinant is $ad-bc$ — the leading
diagonal product minus the other one — and the inverse
$\frac{1}{ad-bc}$ times the matrix with rows $(d,-b)$ and $(-c,a)$ exists only
when $ad-bc\ne0$.

1. The order of the matrix with 3 rows and 4 columns is <span class="marks">[1]</span>
   (a) $3\times3$ (b) $4\times4$ (c) $3\times4$ (d) $4\times3$
2. The determinant of the matrix with first row 5, 2 and second row 3, 4 is
   <span class="marks">[1]</span>
   (a) 26 (b) 14 (c) 20 (d) 6
3. A square matrix has an inverse only when its determinant is
   <span class="marks">[1]</span>
   (a) zero (b) not zero (c) positive (d) one
4. If $A$ has order $2\times3$ and $B$ has order $3\times4$, then $AB$ has order
   <span class="marks">[1]</span>
   (a) $2\times4$ (b) $4\times2$ (c) $3\times3$ (d) not defined
5. The value of $x$ if the determinant with first row $x$, 3 and second row 4, 6
   equals 12 is <span class="marks">[1]</span>
   (a) 2 (b) 4 (c) 6 (d) 8
6. The determinant of the identity matrix of order 3 is <span class="marks">[1]</span>
   (a) 0 (b) 1 (c) 3 (d) 9
7. Which of these matrices is singular? <span class="marks">[1]</span>
   (a) first row 2, 1, second row 4, 3 (b) first row 3, 6, second row 1, 2
   (c) first row 1, 0, second row 0, 1 (d) first row 5, 2, second row 1, 4
8. In Cramer's rule the value of $y$ is <span class="marks">[1]</span>
   (a) $\frac{D_y}{D}$ (b) $\frac{D}{D_y}$ (c) $D_yD$ (d) $\frac{D_x}{D}$

::: note Answers to 17.3
**1.** (c) — rows first, then columns: $3\times4$.
**2.** (b) — $5\times4-2\times3=20-6=14$.
**3.** (b) — division by the determinant is impossible when it is zero.
**4.** (a) — the inner orders (3 and 3) cancel, leaving $2\times4$.
**5.** (b) — $6x-12=12$ gives $6x=24$ and $x=4$.
**6.** (b) — every identity matrix has determinant 1.
**7.** (b) — $3\times2-6\times1=0$.
**8.** (a) — $y=\frac{D_y}{D}$ when $D\ne0$.
:::

::: caution When the unknown is inside the matrix
An item of this shape asks for the **letter in the matrix**, not for the
determinant, and the two numbers are usually different. Item 5 is the model:
the determinant is given as 12 and the letter comes out as 4. Read which one
the question wants, then substitute your answer back — $6(4)-12=12$ — before
you mark the option.
:::

## 17.4 Trigonometry: Multiple, Submultiple and Transformation Formulas

**Facts.** $\sin2A=2\sin A\cos A$; $\cos2A=\cos^2A-\sin^2A=1-2\sin^2A=2\cos^2A-1$;
$\tan2A=\frac{2\tan A}{1-\tan^2A}$; $\sin3A=3\sin A-4\sin^3A$;
$\cos3A=4\cos^3A-3\cos A$; for submultiples
$\sin A=\frac{2\tan\frac{A}{2}}{1+\tan^2\frac{A}{2}}$ and
$\cos A=\frac{1-\tan^2\frac{A}{2}}{1+\tan^2\frac{A}{2}}$; and the transformation
formulas $\sin C+\sin D=2\sin\frac{C+D}{2}\cos\frac{C-D}{2}$,
$\sin C-\sin D=2\cos\frac{C+D}{2}\sin\frac{C-D}{2}$,
$\cos C+\cos D=2\cos\frac{C+D}{2}\cos\frac{C-D}{2}$,
$\cos C-\cos D=-2\sin\frac{C+D}{2}\sin\frac{C-D}{2}$.

1. If $\sin A=\frac{3}{5}$ and $A$ is acute, then $\sin2A$ is
   <span class="marks">[1]</span>
   (a) $\frac{6}{5}$ (b) $\frac{24}{25}$ (c) $\frac{7}{25}$ (d) $\frac{12}{25}$
2. The value of $2\sin15°\cos15°$ is <span class="marks">[1]</span>
   (a) $\frac{1}{2}$ (b) $\frac{\sqrt{3}}{2}$ (c) 1 (d) $\frac{\sqrt{3}}{4}$
3. $\cos2A$ in terms of $\sin A$ alone is <span class="marks">[1]</span>
   (a) $1+2\sin^2A$ (b) $1-2\sin^2A$ (c) $2\sin^2A-1$ (d) $2\sin A\cos A$
4. If $\tan A=\frac{1}{2}$, then $\tan2A$ is <span class="marks">[1]</span>
   (a) $\frac{3}{4}$ (b) $\frac{4}{3}$ (c) 1 (d) $\frac{1}{4}$
5. $\sin3A$ equals <span class="marks">[1]</span>
   (a) $3\sin A-4\sin^3A$ (b) $4\sin^3A-3\sin A$ (c) $3\sin A+4\sin^3A$
   (d) $3\sin^3A$
6. $\sin40°+\sin20°$ equals <span class="marks">[1]</span>
   (a) $\sin60°$ (b) $2\sin30°\cos10°$ (c) $\cos30°$ (d) $2\cos30°\cos10°$
7. $\cos40°-\cos20°$ equals <span class="marks">[1]</span>
   (a) $-2\sin30°\sin10°$ (b) $2\sin30°\sin10°$ (c) $-2\cos30°\cos10°$
   (d) $2\cos30°\sin10°$
8. The value of $\frac{\sin2A}{1+\cos2A}$ is <span class="marks">[1]</span>
   (a) $\tan A$ (b) $\cot A$ (c) $\tan2A$ (d) $\sec A$
9. $\cos^2A-\sin^2A$ equals <span class="marks">[1]</span>
   (a) $2\sin A$ (b) $\cos2A$ (c) $\sin2A$ (d) 1
10. If $\sin A=\cos A$ and $A$ is acute, then $2A$ is <span class="marks">[1]</span>
   (a) $45°$ (b) $60°$ (c) $90°$ (d) $180°$

::: note Answers to 17.4
**1.** (b) — $\cos A=\frac{4}{5}$, so $\sin2A=2\times\frac{3}{5}\times\frac{4}{5}=\frac{24}{25}$.
**2.** (a) — $2\sin15°\cos15°=\sin30°=\frac{1}{2}$.
**3.** (b) — from the three forms of $\cos2A$, the one with only $\sin A$ is $1-2\sin^2A$.
**4.** (b) — $\tan2A=\frac{2\times\frac{1}{2}}{1-\frac{1}{4}}=\frac{1}{\frac{3}{4}}=\frac{4}{3}$.
**5.** (a) — the standard identity; (b) is $-\sin3A$.
**6.** (b) — $2\sin30°\cos10°$, which is about 0.98, the value of $\sin40°+\sin20°$.
**7.** (a) — the minus form carries the negative sign: $-2\sin30°\sin10°\approx-0.174$.
**8.** (a) — $\frac{2\sin A\cos A}{2\cos^2A}=\tan A$.
**9.** (b) — that is the definition of $\cos2A$.
**10.** (c) — $A=45°$, so $2A=90°$.
:::

## 17.5 Conditional Identities, Trigonometric Equations and Height and Distance

**Facts.** Three conditional identities govern most items of this type: in a
triangle, $\sin2A+\sin2B+\sin2C=4\sin A\sin B\sin C$,
$\cos^2A+\cos^2B+\cos^2C=1-2\cos A\cos B\cos C$ and
$\tan A+\tan B+\tan C=\tan A\tan B\tan C$. A trigonometric equation is solved
by reducing it to a single ratio and writing the general value of the angle.

1. In any triangle, $\sin2A+\sin2B+\sin2C$ equals <span class="marks">[1]</span>
   (a) $4\cos A\cos B\cos C$ (b) $4\sin A\sin B\sin C$ (c) 0 (d) $2\sin A\sin B\sin C$
2. If $A+B+C=180°$, then $\tan A+\tan B+\tan C$ equals
   <span class="marks">[1]</span>
   (a) $\tan A\tan B\tan C$ (b) 0 (c) 1 (d) $\cot A\cot B\cot C$
3. If $\sin\theta=\frac{\sqrt{3}}{2}$ and $0°\leq\theta\leq90°$, then $\theta$ is
   <span class="marks">[1]</span>
   (a) $30°$ (b) $45°$ (c) $60°$ (d) $90°$
4. The general solution of $\tan\theta=1$ is <span class="marks">[1]</span>
   (a) $n\pi+\frac{\pi}{4}$ (b) $2n\pi+\frac{\pi}{4}$ (c) $n\pi-\frac{\pi}{4}$
   (d) $\frac{n\pi}{2}$
5. A pole 10 m high casts a shadow 10 m long. The elevation of the sun is
   <span class="marks">[1]</span>
   (a) $30°$ (b) $45°$ (c) $60°$ (d) $90°$
6. From a point 20 m from the foot of a tower the angle of elevation of the top
   is $45°$. The height of the tower is <span class="marks">[1]</span>
   (a) 10 m (b) 20 m (c) $20\sqrt{3}$ m (d) 40 m
7. The angle of depression is measured <span class="marks">[1]</span>
   (a) upward from the horizontal (b) downward from the horizontal
   (c) from the vertical (d) along the ground
8. If $\cos\theta=\frac{1}{2}$ and $\theta$ is acute, then $\theta$ is
   <span class="marks">[1]</span>
   (a) $30°$ (b) $45°$ (c) $60°$ (d) $120°$

::: note Answers to 17.5
**1.** (b) — $\sin2A+\sin2B+\sin2C=4\sin A\sin B\sin C$ in a triangle.
**2.** (a) — the tangent identity for a triangle sum: they are equal.
**3.** (c) — $\sin60°=\frac{\sqrt{3}}{2}$.
**4.** (a) — tangent has period $\pi$, so $\theta=n\pi+\frac{\pi}{4}$.
**5.** (b) — $\tan\theta=\frac{10}{10}=1$, so the elevation is $45°$.
**6.** (b) — $\tan45°=1$, so height $=$ distance $=20$ m.
**7.** (b) — the depression is the angle below the horizontal.
**8.** (c) — $\cos60°=\frac{1}{2}$; $120°$ has the same cosine but is obtuse.
:::

```figure caption="Why the elevation and the depression are the same angle. The two horizontal lines are parallel, so the two marked angles are alternate angles, whichever object you stand under."
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
fig, ax = plt.subplots(figsize=(4.6, 2.6))
ax.plot([0, 5], [0, 0], color=GRID, lw=1)
ax.plot([0, 5], [2.4, 2.4], color=GRID, lw=1)
ax.plot([0.6, 0.6], [0, 2.4], color=INK, lw=2)
ax.plot([0.6, 4.6], [2.4, 0], color=ACCENT, lw=1.6)
ax.plot([0.6, 4.6], [0, 0], color=SERIES[1], lw=1.4, ls=":")
ax.add_patch(Arc((0.6, 2.4), 1.1, 1.1, theta1=0, theta2=-30, color=SERIES[1], lw=1.2))
ax.add_patch(Arc((4.6, 0), 1.1, 1.1, theta1=150, theta2=180, color=SERIES[1], lw=1.2))
ax.text(1.35, 2.5, "depression", fontsize=8, color=SERIES[1])
ax.text(3.4, 0.12, "elevation", fontsize=8, color=SERIES[1])
ax.text(0.15, 1.15, "tower", fontsize=8, color=INK, rotation=90, va="center")
ax.text(2.4, 1.5, "line of sight", fontsize=8, color=ACCENT)
ax.set_xlim(0, 5.2); ax.set_ylim(-0.5, 3.0)
ax.axis("off")
fig.tight_layout()
```

## 17.6 Angle between Two Lines and Pair of Straight Lines

**Facts.** If two lines of slopes $m_1$ and $m_2$ meet at an angle
$\theta$, then $\tan\theta=\left|\frac{m_1-m_2}{1+m_1m_2}\right|$. The lines are
parallel when $m_1=m_2$ and perpendicular when $m_1m_2=-1$. A homogeneous
equation of the second degree $ax^2+2hxy+by^2=0$ represents a pair of straight
lines through the origin, and the angle between them satisfies
$\tan\theta=\left|\frac{2\sqrt{h^2-ab}}{a+b}\right|$, the lines being
perpendicular when $a+b=0$.

1. The slope of the line $3x+4y=12$ is <span class="marks">[1]</span>
   (a) $\frac{3}{4}$ (b) $-\frac{3}{4}$ (c) $\frac{4}{3}$ (d) $-\frac{4}{3}$
2. The lines $2x+3y=5$ and $4x+6y=7$ are <span class="marks">[1]</span>
   (a) perpendicular (b) parallel (c) coincident (d) intersecting at $45°$
3. If two lines of slopes $m_1$ and $m_2$ are perpendicular, then
   <span class="marks">[1]</span>
   (a) $m_1=m_2$ (b) $m_1m_2=1$ (c) $m_1m_2=-1$ (d) $m_1+m_2=0$
4. The angle between the lines $y=x$ and $y=\sqrt{3}x$ is
   <span class="marks">[1]</span>
   (a) $15°$ (b) $30°$ (c) $45°$ (d) $60°$
5. The equation $x^2-y^2=0$ represents <span class="marks">[1]</span>
   (a) a circle (b) a pair of perpendicular lines (c) a parabola
   (d) a single line
6. For the pair of lines $ax^2+2hxy+by^2=0$ to be perpendicular, we need
   <span class="marks">[1]</span>
   (a) $a=b$ (b) $a=-b$ (c) $h^2=ab$ (d) $h=0$

::: note Answers to 17.6
**1.** (b) — rearranging gives $y=-\frac{3}{4}x+3$.
**2.** (b) — the second equation is the first multiplied by 2, with a different
   constant, so the slopes match and the lines never meet.
**3.** (c) — perpendicular slopes multiply to $-1$.
**4.** (a) — slopes 1 and $\sqrt{3}$, so
   $\tan\theta=\frac{\sqrt{3}-1}{1+\sqrt{3}}=2-\sqrt{3}\approx0.268$, and
   $\tan15°=2-\sqrt{3}$, so $\theta=15°$.
**5.** (b) — $x^2-y^2=(x-y)(x+y)=0$ gives the lines $y=x$ and $y=-x$.
**6.** (b) — $a+b=0$ is the perpendicular condition.
:::

::: caution The two-minute habit that saves these marks
In item 4 the two slopes are $1$ and $1.732$, and the value $0.268$ that comes
out of the formula does not look like any angle on the page. The habit that
never fails is: **compute the number, then compare it with a value you already
know.** $\tan15°\approx0.27$ and $\tan30°\approx0.58$, so the angle is $15°$.
Carry that habit into every Group A item.
:::

## 17.7 Conic Sections and Circle

**Facts.** The circle with centre $(h,k)$ and radius $r$ has equation
$(x-h)^2+(y-k)^2=r^2$, and the general equation
$x^2+y^2+2gx+2fy+c=0$ has centre $(-g,-f)$ and radius
$\sqrt{g^2+f^2-c}$. A parabola has eccentricity 1, an ellipse less than 1 and a
hyperbola more than 1.

1. The centre of the circle $x^2+y^2-6x+4y-12=0$ is
   <span class="marks">[1]</span>
   (a) $(3,-2)$ (b) $(-3,2)$ (c) $(6,-4)$ (d) $(3,2)$
2. The radius of the circle in item 1 is <span class="marks">[1]</span>
   (a) 5 (b) 25 (c) 12 (d) 13
3. The equation of the circle with centre $(0,0)$ and radius 4 is
   <span class="marks">[1]</span>
   (a) $x^2+y^2=2$ (b) $x^2+y^2=4$ (c) $x^2+y^2=8$ (d) $x^2+y^2=16$
4. The eccentricity of a parabola is <span class="marks">[1]</span>
   (a) 0 (b) less than 1 (c) 1 (d) more than 1
5. The conic with eccentricity greater than 1 is <span class="marks">[1]</span>
   (a) circle (b) ellipse (c) parabola (d) hyperbola
6. The distance of the point $(3,4)$ from the origin is
   <span class="marks">[1]</span>
   (a) 5 (b) 7 (c) 12 (d) 25
7. If the circle $x^2+y^2+4x+2y+c=0$ passes through the origin, then $c$ is
   <span class="marks">[1]</span>
   (a) 0 (b) 4 (c) 2 (d) −4
8. The circle $x^2+y^2+2x+2y+2=0$ has <span class="marks">[1]</span>
   (a) radius 2 (b) radius $\sqrt{2}$ (c) no real circle (d) radius 0

::: note Answers to 17.7
**1.** (a) — compare with $x^2+y^2+2gx+2fy+c$: $g=-3$, $f=2$, centre $(-g,-f)=(3,-2)$.
**2.** (a) — $r=\sqrt{9+4+12}=\sqrt{25}=5$.
**3.** (d) — radius squared is 16.
**4.** (c) — every point of a parabola is equidistant from the focus and the
   directrix, so $e=1$.
**5.** (d) — an eccentricity greater than 1 gives a hyperbola.
**6.** (a) — $\sqrt{9+16}=5$.
**7.** (a) — putting $x=y=0$ leaves $c=0$.
**8.** (c) — $r^2=g^2+f^2-c=1+1-2=0$, so the "circle" is a single point.
:::

## 17.8 Vector

**Facts.** If $\vec a=a_1\hat i+a_2\hat j$ and $\vec b=b_1\hat i+b_2\hat j$,
then $\vec a\cdot\vec b=a_1b_1+a_2b_2=|\vec a||\vec b|\cos\theta$;
$\vec a$ and $\vec b$ are perpendicular when the dot product is zero and
parallel when $\frac{a_1}{b_1}=\frac{a_2}{b_2}$. The magnitude of
$\vec a$ is $\sqrt{a_1^2+a_2^2}$, and the position vector of the point dividing
$AB$ internally in the ratio $m:n$ is $\frac{m\vec b+n\vec a}{m+n}$.

1. If $\vec a=2\hat i+3\hat j$ and $\vec b=4\hat i-\hat j$, then
   $\vec a\cdot\vec b$ is <span class="marks">[1]</span>
   (a) 5 (b) 11 (c) 8 (d) −3
2. The magnitude of $\vec a=3\hat i+4\hat j$ is <span class="marks">[1]</span>
   (a) 5 (b) 7 (c) 12 (d) 25
3. The vectors $2\hat i+\hat j$ and $x\hat i+2\hat j$ are perpendicular when
   $x$ is <span class="marks">[1]</span>
   (a) 1 (b) −1 (c) 2 (d) −2
4. The unit vector along $3\hat i+4\hat j$ is
   <span class="marks">[1]</span>
   (a) $3\hat i+4\hat j$ (b) $\frac{3\hat i+4\hat j}{5}$
   (c) $\frac{3\hat i+4\hat j}{7}$ (d) $5(3\hat i+4\hat j)$
5. If $\vec a=2\hat i+\hat j$ and $\vec b=4\hat i+2\hat j$, the two vectors are
   <span class="marks">[1]</span>
   (a) parallel (b) perpendicular (c) equal (d) opposite
6. The position vector of the midpoint of $A(2,3)$ and $B(4,7)$ is
   <span class="marks">[1]</span>
   (a) $3\hat i+5\hat j$ (b) $6\hat i+10\hat j$ (c) $2\hat i+4\hat j$
   (d) $\hat i+2\hat j$
7. If $\vec a\cdot\vec b=0$ and neither vector is zero, the angle between them is
   <span class="marks">[1]</span>
   (a) $0°$ (b) $45°$ (c) $90°$ (d) $180°$
8. The value of $|\hat i+\hat j|$ is <span class="marks">[1]</span>
   (a) 1 (b) $\sqrt{2}$ (c) 2 (d) 0

::: note Answers to 17.8
**1.** (a) — $2\times4+3\times(-1)=8-3=5$.
**2.** (a) — $\sqrt{9+16}=5$.
**3.** (b) — $2x+2=0$ gives $x=-1$; check: $2(-1)+1(2)=0$.
**4.** (b) — divide by the magnitude 5.
**5.** (a) — $\vec b=2\vec a$, so they are parallel.
**6.** (a) — the midpoint is $(3,5)$.
**7.** (c) — $\cos\theta=0$, so $\theta=90°$.
**8.** (b) — $\sqrt{1+1}=\sqrt{2}$.
:::

::: caution The substitution habit
Every item in this chapter that asks for a letter has a "near miss" option
next to the right one, because that is how real papers are built. The cheap
insurance is the same every time: **find the value, then put it back into the
condition the question stated.** For item 3 that means checking that
$2(-1)+1(2)$ really is zero before you darken the bubble.
:::

## 17.9 Linear Programming and Transformation

**Facts.** A linear programming problem has an **objective function** to be
maximised or minimised, **constraints** written as linear inequalities, and a
**feasible region** that is always convex. The best value is attained at a
corner of that region. A transformation with matrix rows $(a,b)$ and $(c,d)$
sends the point $(x,y)$ to $(ax+by,\;cx+dy)$; an inversion transformation with
centre $O$ and radius $k$ sends $P$ to $P'$ on the same ray with
$OP\cdot OP'=k^2$.

1. In linear programming the objective function is <span class="marks">[1]</span>
   (a) a constraint (b) the quantity to be maximised or minimised
   (c) the feasible region (d) a corner point
2. The maximum of a linear objective over a feasible region is attained
   <span class="marks">[1]</span>
   (a) at the centre (b) at a corner point (c) anywhere (d) outside the region
3. The point $(2,3)$ under the identity transformation goes to
   <span class="marks">[1]</span>
   (a) $(3,2)$ (b) $(2,3)$ (c) $(-2,-3)$ (d) $(0,0)$
4. Under the transformation with matrix first row 0, −1 and second row 1, 0, the
   point $(3,4)$ goes to <span class="marks">[1]</span>
   (a) $(-4,3)$ (b) $(4,-3)$ (c) $(3,-4)$ (d) $(-3,4)$
5. In an inversion transformation with radius $k$, the product $OP\cdot OP'$
   equals <span class="marks">[1]</span>
   (a) $k$ (b) $k^2$ (c) $2k$ (d) 1
6. The region satisfying $x\geq0$, $y\geq0$ and $x+y\leq4$ is
   <span class="marks">[1]</span>
   (a) a triangle (b) a square (c) unbounded (d) a single point
7. The maximum of $z=x+y$ subject to $x\geq0$, $y\geq0$, $x+y\leq4$ is
   <span class="marks">[1]</span>
   (a) 0 (b) 2 (c) 4 (d) 8
8. A point on the inversion circle is <span class="marks">[1]</span>
   (a) moved onto itself (b) sent to the centre (c) sent to infinity
   (d) lost

::: note Answers to 17.9
**1.** (b) — the objective is what the problem asks you to maximise or minimise.
**2.** (b) — a linear function on a convex polygon peaks at a vertex.
**3.** (b) — the identity matrix leaves every point fixed.
**4.** (a) — $(0\times3+(-1)\times4,\;1\times3+0\times4)=(-4,3)$.
**5.** (b) — that product is the defining property, $OP\cdot OP'=k^2$.
**6.** (a) — the three lines close a right triangle with corners
   $(0,0)$, $(4,0)$, $(0,4)$.
**7.** (c) — $z$ is largest at $(4,0)$ or $(0,4)$, where $z=4$.
**8.** (a) — a point at distance $k$ from the centre satisfies
   $OP\cdot OP'=k^2$ with $OP'=k$, so it is its own image.
:::

## 17.10 Continuity

**Facts.** A function is continuous at $x=a$ when the left-hand limit, the
right-hand limit and the value of the function at $a$ are all the same number.
If the two one-sided limits differ, the gap is a **jump discontinuity**; if the
limit exists but $f(a)$ is different, the point is a **removable
discontinuity**.

1. A function $f$ is continuous at $x=a$ if <span class="marks">[1]</span>
   (a) $f(a)$ exists (b) the limit exists (c) the limit exists and equals $f(a)$
   (d) $f$ is increasing
2. The value of $\lim_{x\to2}(3x+1)$ is <span class="marks">[1]</span>
   (a) 5 (b) 6 (c) 7 (d) does not exist
3. The value of $\lim_{x\to0}\frac{\sin x}{x}$ is <span class="marks">[1]</span>
   (a) 0 (b) 1 (c) $\infty$ (d) does not exist
4. The function $f(x)=\frac{1}{x}$ is discontinuous at
   <span class="marks">[1]</span>
   (a) $x=0$ (b) $x=1$ (c) every $x$ (d) no point
5. If $\lim_{x\to a^-}f(x)=3$ and $\lim_{x\to a^+}f(x)=5$, then at $a$ the
   function has <span class="marks">[1]</span>
   (a) a removable discontinuity (b) a jump discontinuity (c) no discontinuity
   (d) a maximum
6. The value of $\lim_{x\to3}\frac{x^2-9}{x-3}$ is <span class="marks">[1]</span>
   (a) 0 (b) 3 (c) 6 (d) does not exist

::: note Answers to 17.10
**1.** (c) — continuity needs the limit and the value to agree.
**2.** (c) — $3\times2+1=7$, and a polynomial is continuous everywhere.
**3.** (b) — the standard limit is 1.
**4.** (a) — at $x=0$ the expression is undefined and grows without bound.
**5.** (b) — the one-sided limits differ, which is a jump.
**6.** (c) — cancel the factor: $\frac{(x-3)(x+3)}{x-3}=x+3\to6$.
:::

## 17.11 Statistics: Measures of Dispersion

**Facts.** For a set of $n$ observations with mean $\bar x$, the mean deviation
about the mean is $\frac{\sum|x-\bar x|}{n}$; the standard deviation is
$\sigma=\sqrt{\frac{\sum(x-\bar x)^2}{n}}$, the variance is $\sigma^2$, and the
coefficient of variation is $\frac{\sigma}{\bar x}\times100\%$. The quartile
deviation is $\frac{Q_3-Q_1}{2}$.

1. The range of 4, 9, 2, 7, 11 is <span class="marks">[1]</span>
   (a) 7 (b) 9 (c) 11 (d) 5
2. The mean of 2, 4, 6, 8, 10 is <span class="marks">[1]</span>
   (a) 5 (b) 6 (c) 7 (d) 30
3. The standard deviation of 2, 4, 6, 8, 10 is <span class="marks">[1]</span>
   (a) $\sqrt{8}$ (b) 8 (c) $\sqrt{40}$ (d) 2
4. If every observation is increased by 5, the standard deviation
   <span class="marks">[1]</span>
   (a) increases by 5 (b) is unchanged (c) is multiplied by 5 (d) doubles
5. The coefficient of variation is a measure of <span class="marks">[1]</span>
   (a) central tendency (b) relative dispersion (c) correlation (d) skewness
6. If $Q_1=20$ and $Q_3=40$, the quartile deviation is
   <span class="marks">[1]</span>
   (a) 10 (b) 20 (c) 30 (d) 60
7. For a distribution with mean 50 and standard deviation 5, the coefficient of
   variation is <span class="marks">[1]</span>
   (a) 5% (b) 10% (c) 25% (d) 50%
8. The standard deviation of a set in which every observation is equal is
   <span class="marks">[1]</span>
   (a) equal to the observation (b) 1 (c) 0 (d) undefined

::: note Answers to 17.11
**1.** (b) — $11-2=9$.
**2.** (b) — $\frac{30}{5}=6$.
**3.** (a) — deviations are $-4,-2,0,2,4$; $\frac{16+4+0+4+16}{5}=8$, so
   $\sigma=\sqrt{8}\approx2.83$.
**4.** (b) — adding a constant moves every point but not the spread.
**5.** (b) — it expresses the spread as a percentage of the mean.
**6.** (a) — $\frac{40-20}{2}=10$.
**7.** (b) — $\frac{5}{50}\times100=10\%$.
**8.** (c) — no observation departs from the mean.
:::

```figure caption="Two sets can share a mean and still be nothing alike. Both sets below average 6; the taller bars are the more variable one, and that is exactly what standard deviation reports."
import numpy as np
import matplotlib.pyplot as plt
x = np.arange(1, 7)
a = np.array([3, 4, 5, 6, 7, 8])
b = np.array([1, 4, 6, 5, 9, 7])
fig, ax = plt.subplots(figsize=(4.6, 2.5))
w = 0.38
ax.bar(x - w/2, a, w, color=ACCENT, label="SD 1.7")
ax.bar(x + w/2, b, w, color=SERIES[1], label="SD 2.7")
ax.axhline(6, color=INK, lw=1.0, ls="--")
ax.text(6.15, 6.15, "mean 6", fontsize=8, color=INK)
ax.set_xticks(x); ax.set_xlabel("observation number", fontsize=8)
ax.set_ylabel("value", fontsize=8)
ax.tick_params(labelsize=8, length=0)
ax.legend(fontsize=8, frameon=False, loc="upper left")
ax.spines[["top", "right"]].set_visible(False)
ax.yaxis.grid(True, color=GRID, lw=0.6)
ax.set_axisbelow(True)
fig.tight_layout()
```

## 17.12 Functions and Polynomials

**Facts.** A relation is a set of ordered pairs; a function sends each input to
exactly one output, which the vertical line test checks on a graph. For
$f(x)=ax^2+bx+c$ the remainder on division by $x-a$ is $f(a)$ (remainder
theorem), and $x-a$ is a factor exactly when $f(a)=0$ (factor theorem). For
$f:A\to B$ and $g:B\to C$, the composite is $(g\circ f)(x)=g(f(x))$, and $f$
has an inverse only when it is one-to-one and onto.

1. The domain of $f(x)=\frac{1}{x-2}$ is <span class="marks">[1]</span>
   (a) all real numbers (b) all real numbers except 2
   (c) all real numbers except 0 (d) $x>2$
2. If $f(x)=2x+3$, then $f(4)$ is <span class="marks">[1]</span>
   (a) 8 (b) 11 (c) 14 (d) 7
3. The remainder when $x^3-2x^2+4$ is divided by $x-2$ is
   <span class="marks">[1]</span>
   (a) 0 (b) 4 (c) 8 (d) 12
4. $x-1$ is a factor of $x^3-3x^2+2x$ because <span class="marks">[1]</span>
   (a) $f(1)=0$ (b) $f(1)=1$ (c) $f(0)=0$ (d) the degree is 3
5. If $f(x)=x+1$ and $g(x)=x^2$, then $(g\circ f)(2)$ is
   <span class="marks">[1]</span>
   (a) 5 (b) 9 (c) 3 (d) 4
6. If $f(x)=3x-2$, then $f^{-1}(x)$ is <span class="marks">[1]</span>
   (a) $\frac{x+2}{3}$ (b) $\frac{x-2}{3}$ (c) $3x+2$ (d) $\frac{1}{3x-2}$
7. A graph represents a function when no vertical line meets it
   <span class="marks">[1]</span>
   (a) at all (b) more than once (c) exactly once (d) below the axis
8. The function $f(x)=x^2$ on all real numbers is
   <span class="marks">[1]</span>
   (a) one-to-one (b) not one-to-one (c) constant (d) the identity

::: note Answers to 17.12
**1.** (b) — at $x=2$ the denominator is zero.
**2.** (b) — $2\times4+3=11$.
**3.** (b) — $f(2)=8-8+4=4$.
**4.** (a) — the factor theorem; indeed $1-3+2=0$.
**5.** (b) — $f(2)=3$, then $g(3)=9$.
**6.** (a) — solve $y=3x-2$ for $x=\frac{y+2}{3}$.
**7.** (b) — one crossing at most is the definition the test checks.
**8.** (b) — $f(2)=f(-2)=4$, so two inputs share an output.
:::

## Chapter summary

- **Sequences:** $t_n=a+(n-1)d$, $S_n=\frac n2\{2a+(n-1)d\}$, $t_n=ar^{n-1}$,
  $S_n=\frac{a(r^n-1)}{r-1}$; AM $=\frac{a+b}{2}$, GM $=\sqrt{ab}$, and
  AM $\geq$ GM.
- **Quadratic:** $D=b^2-4ac$ fixes the nature of the roots; sum of roots
  $=-\frac ba$, product $=\frac ca$; vertex at $x=-\frac{b}{2a}$.
- **Matrices:** order is rows $\times$ columns; a square matrix is invertible
  exactly when its determinant is not zero.
- **Trigonometry:** know $\sin2A$, the three forms of $\cos2A$, $\tan2A$,
  $\sin3A$, $\cos3A$, the four transformation formulas, and the four
  half-angle results.
- **Conditional identities:** in a triangle,
  $\tan A+\tan B+\tan C=\tan A\tan B\tan C$ and
  $\sin2A+\sin2B+\sin2C=4\sin A\sin B\sin C$.
- **Lines:** $\tan\theta=\left|\frac{m_1-m_2}{1+m_1m_2}\right|$; parallel means
  equal slopes, perpendicular means the slopes multiply to $-1$.
- **Circle:** centre $(-g,-f)$ and radius $\sqrt{g^2+f^2-c}$ for
  $x^2+y^2+2gx+2fy+c=0$.
- **Vectors:** $\vec a\cdot\vec b=a_1b_1+a_2b_2$; zero dot product means
  perpendicular.
- **Dispersion:** $\sigma=\sqrt{\frac{\sum(x-\bar x)^2}{n}}$,
  CV $=\frac{\sigma}{\bar x}\times100\%$, quartile deviation
  $=\frac{Q_3-Q_1}{2}$.
- **Polynomials:** remainder $=f(a)$ on division by $x-a$; $x-a$ is a factor
  exactly when $f(a)=0$.
