---
subject: Mathematics
grade: 8
title: Lines and Angles
unit: 13
hours: 0
area: Compulsory Mathematics
---

Two straight lines that never meet, a transversal that cuts them, and the eight
angles that appear: that picture contains almost every angle fact you will need
in geometry. The whole chapter is really one idea — when a transversal crosses
parallel lines, four angles come out equal in one way and four in another, and
recognising which is which settles a question in one line.

::: key What this chapter asks of you
You should be able to name and use complementary, supplementary, adjacent and
vertically opposite angles, state the conditions for two lines to be parallel,
and find unknown angles using corresponding angles, alternate angles and
co-interior angles.
:::

## 13.1 Points, lines and angles

| Term | Meaning |
|---|---|
| Point | a position with no size, named with a capital letter |
| Line | a straight path that extends for ever in both directions |
| Line segment | a part of a line with two end points |
| Ray | a part of a line with one end point |
| Angle | the figure formed by two rays with a common end point, the vertex |

An angle is measured in **degrees**, from 0° to 360°, using a protractor. Angles
are named by three letters with the vertex in the middle, as in $\angle ABC$.

| Kind of angle | Size |
|---|---|
| Acute | between 0° and 90° |
| Right | exactly 90° |
| Obtuse | between 90° and 180° |
| Straight | exactly 180° |
| Reflex | between 180° and 360° |

## 13.2 Pairs of angles

| Pair | Relation | Example |
|---|---|---|
| Complementary | they add to 90° | 35° and 55° |
| Supplementary | they add to 180° | 110° and 70° |
| Adjacent | they share a vertex and a common arm, without overlapping | the two angles on either side of a line |
| Vertically opposite | they are formed by two intersecting lines, and they are equal | the two angles opposite each other at a crossing |
| Linear pair | two adjacent angles that together make a straight line; they add to 180° | the two angles on one side of a straight line |

```figure caption="Two straight lines crossing. The four angles round the point add to 360°, and the two pairs of vertically opposite angles are equal to each other."
fig, ax = plt.subplots(figsize=(4.7, 2.8))
ax.set_xlim(0, 10)
ax.set_ylim(0, 6.2)
ax.axis("off")
ax.plot([0.6, 9.4], [3.1, 3.1], color=INK, lw=1.6)
ax.plot([3.0, 7.0], [0.8, 5.4], color=INK, lw=1.6)
ax.plot([4.8], [3.1], "o", color=INK, ms=4)
ax.text(4.65, 2.65, "O", fontsize=7.5, color=INK)
ax.text(2.0, 3.45, "a", fontsize=8, color=ACCENT)
ax.text(6.9, 2.6, "b", fontsize=8, color=SERIES[1])
ax.text(2.15, 2.65, "b", fontsize=8, color=SERIES[1])
ax.text(6.85, 3.45, "a", fontsize=8, color=ACCENT)
ax.text(3.6, 4.5, "the angles marked a", ha="center", fontsize=6.4, color=ACCENT)
ax.text(3.6, 1.75, "are vertically opposite and equal", ha="center", fontsize=6.4,
        color=MUTED)
fig.tight_layout()
```

::: example Complementary and supplementary angles
**Problem.** Two angles are supplementary. One of them is 40° more than the
other. Find both.

**Solution.** Let the smaller be $x$; then the larger is $x+40$. Because they are
supplementary,

$$x+(x+40)=180\;\Longrightarrow\;2x=140\;\Longrightarrow\;x=70$$

**Answer.** 70° and 110°.

**Check.** $70+110=180$ ✓ and $110-70=40$ ✓.
:::

::: example Vertically opposite angles
**Problem.** Two straight lines cross. One of the four angles is 65°. Find the
other three, giving a reason for each.

**Solution.** The angle vertically opposite 65° is also **65°** (vertically
opposite angles are equal). Each of the other two is supplementary to 65°, so
each is $180-65=115°$; and they are equal to each other because they are
vertically opposite.

**Answer.** 65°, 115°, 115°.

**Check.** $65+115+65+115=360$ ✓, which is the angle sum round a point.
:::

::: caution Angles on a straight line add to 180°, not to the "big" angle
In a figure with three angles on one side of a straight line, the equation is
$x+2x+3x=180$, not 360. The 360° belongs to the angles round a **point**. Read
whether the arms close a full turn or only a half turn before you add.
:::

## 13.3 Parallel lines and a transversal

A **transversal** is a line that cuts two or more other lines. When it cuts two
**parallel** lines, eight angles are formed, and they fall into three named
pairs.

```figure caption="A transversal cutting two parallel lines. Every acute angle in the figure equals every other acute angle, and every obtuse angle equals every other obtuse angle — that is the whole content of the three rules."
fig, ax = plt.subplots(figsize=(4.9, 2.9))
ax.set_xlim(0, 10)
ax.set_ylim(0, 6.2)
ax.axis("off")
ax.plot([0.6, 9.4], [4.1, 4.1], color=INK, lw=1.6)
ax.plot([0.6, 9.4], [1.5, 1.5], color=INK, lw=1.6)
ax.plot([2.6, 7.4], [0.4, 5.6], color=ACCENT, lw=1.4)
ax.annotate("", xy=(9.3, 4.1), xytext=(8.7, 4.1),
            arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.0))
ax.annotate("", xy=(9.3, 1.5), xytext=(8.7, 1.5),
            arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.0))
ax.text(3.3, 4.45, "1", fontsize=7.5, color=INK)
ax.text(4.1, 3.6, "2", fontsize=7.5, color=INK)
ax.text(3.3, 1.85, "3", fontsize=7.5, color=INK)
ax.text(4.1, 1.05, "4", fontsize=7.5, color=INK)
ax.text(5.5, 4.45, "a", fontsize=7.5, color=SERIES[1])
ax.text(6.4, 3.6, "b", fontsize=7.5, color=SERIES[1])
ax.text(5.5, 1.85, "c", fontsize=7.5, color=SERIES[2])
ax.text(6.4, 1.05, "d", fontsize=7.5, color=SERIES[2])
ax.text(0.7, 5.35, "corresponding: 1 and a, 2 and b, 3 and c, 4 and d", fontsize=6.2,
        color=SERIES[1])
ax.text(0.7, 0.1, "alternate: 2 and c, 4 and a;  co-interior: 2 and a, 4 and c",
        fontsize=6.2, color=SERIES[2])
fig.tight_layout()
```

| Pair | Position | Relation |
|---|---|---|
| Corresponding angles | same side of the transversal, same side of their own line (the "F" shape) | equal |
| Alternate angles | opposite sides of the transversal, between the two lines (the "Z" shape) | equal |
| Co-interior angles | same side of the transversal, between the two lines (the "C" shape) | supplementary, adding to 180° |

**Conditions for two lines to be parallel.** Two lines are parallel if

- a pair of corresponding angles is equal, or
- a pair of alternate angles is equal, or
- a pair of co-interior angles adds to 180°.

::: example Finding angles with a transversal
**Problem.** In the figure above, angle 1 is 120°. Find angles 2, 3, 4, a, b, c
and d, giving a reason for each.

**Solution.**

| Angle | Value | Reason |
|---|---|---|
| 2 | 60° | angles 1 and 2 form a linear pair on a straight line |
| 3 | 120° | vertically opposite to angle 1 |
| 4 | 60° | vertically opposite to angle 2 |
| a | 120° | corresponding to angle 1 |
| b | 60° | corresponding to angle 2 (or vertically opposite to $a$) |
| c | 120° | alternate to angle 1 |
| d | 60° | corresponding to angle 4 |

**Check.** Angle 2 and angle $a$ are co-interior: $60+120=180$ ✓. All the acute
angles are 60° and all the obtuse ones 120°, which is exactly what parallel
lines force.
:::

::: example Two unknowns
**Problem.** Two parallel lines are cut by a transversal. A pair of co-interior
angles are $3x$ and $2x+20$. Find $x$ and the size of each angle.

**Solution.** Co-interior angles are supplementary:

$$3x+(2x+20)=180\;\Longrightarrow\;5x=160\;\Longrightarrow\;x=32$$

The angles are $3(32)=96°$ and $2(32)+20=84°$.

**Answer.** $x=32$; the angles are 96° and 84°.

**Check.** $96+84=180$ ✓, as co-interior angles must.
:::

::: example Testing for parallel lines
**Problem.** A transversal cuts two lines. A pair of alternate angles are 75°
and 78°. Are the two lines parallel? Give a reason.

**Solution.** Alternate angles are equal only when the lines are parallel. Here
$75°\ne78°$, so the alternate angles are not equal.

**Answer.** The lines are **not** parallel; they meet on the side where the
angles open out. The test for parallel lines is exactly the equality of such a
pair.
:::

::: caution Which pair is it?
Students often use a co-interior pair as if it must be equal. The shapes are the
reminder: **F** (corresponding) means equal and the two angles are on the same
side of both lines; **Z** (alternate) means equal and the angles are on opposite
sides of the transversal; **C** (co-interior) means they add up to 180°. Sketch
the letter next to the angle before you decide.
:::

## 13.5 Reasons are the marks

In a geometry answer the number is worth one mark; the **reason** is worth the
rest. Every statement should carry the name of the rule that justifies it.

| Statement | Reason to write |
|---|---|
| $\angle a = \angle b$ | vertically opposite angles |
| $\angle a + \angle b = 180°$ | angles on a straight line (linear pair) |
| $\angle a = \angle b$ (parallel lines) | corresponding angles |
| $\angle a = \angle b$ (parallel lines, opposite sides) | alternate angles |
| $\angle a + \angle b = 180°$ (parallel lines, same side) | co-interior angles |
| $\angle A + \angle B + \angle C = 180°$ | angle sum of a triangle |
| exterior $=$ sum of two opposite interior | exterior angle property |

```figure caption="Two parallel lines cut by a transversal: the eight angles form just two sizes. Name which rule you are using and the marks follow."
fig, ax = plt.subplots(figsize=(4.8, 2.9))
ax.plot([0.07, 0.93], [0.70, 0.70], color=INK, linewidth=1.6)
ax.plot([0.07, 0.93], [0.28, 0.28], color=INK, linewidth=1.6)
ax.plot([0.22, 0.74], [0.14, 0.86], color=SERIES[1], linewidth=1.6)
pts = {"a": (0.47, 0.78), "b": (0.63, 0.78), "c": (0.44, 0.62),
       "d": (0.60, 0.62), "e": (0.31, 0.36), "f": (0.47, 0.36),
       "g": (0.28, 0.20), "h": (0.44, 0.20)}
for lab, (x, y) in pts.items():
    ax.text(x, y, lab, ha="center", va="center", color=SERIES[0], fontsize=9.5)
ax.text(0.5, 0.045, "equal angles: a = d = e = h   and   b = c = f = g",
        ha="center", color=MUTED, fontsize=8)
ax.set_xlim(0, 1)
ax.set_ylim(0, 0.95)
ax.axis("off")
```

::: example A four-mark angle chase, written for marks
**Question.** Two parallel lines are cut by a transversal. One angle is
$116°$. Find the other seven, with reasons.

**Answer.**
Vertically opposite to $116°$: $\textbf{116°}$ — *vertically opposite angles*.
On the straight line with it: $180° - 116° = \textbf{64°}$ — *linear pair*;
and its vertically opposite is $\textbf{64°}$.
On the second parallel line, the corresponding angle is $\textbf{116°}$ —
*corresponding angles*; its vertically opposite is $\textbf{116°}$.
The remaining two are $\textbf{64°}$ each — *co-interior with $116°$*
($116° + 64° = 180°$) and *vertically opposite*.
:::

::: note Activity — the angle hunt
Find five real examples of parallel lines cut by a transversal in or near
the school: the lines of a football pitch, a ladder against a wall, railings,
the bars of a window grille, a zebra crossing. Sketch each, measure two
angles with a protractor, and name the rule that connects them.
:::

## Chapter summary

- Complementary angles add to 90°; supplementary angles add to 180°; angles
  round a point add to 360°.
- Vertically opposite angles are equal; angles in a linear pair are
  supplementary.
- When a transversal cuts two **parallel** lines: corresponding angles are equal,
  alternate angles are equal, and co-interior angles add to 180°.
- Two lines are parallel if any one of those three conditions holds.
- Remember the shapes: F for corresponding, Z for alternate, C for co-interior.

## Practice questions

**Group A — Objective (1 mark each)**

1. The complement of 40° is <span class="marks">[1]</span>
   (a) 40° (b) 50° (c) 140° (d) 60°
2. The supplement of 125° is <span class="marks">[1]</span>
   (a) 55° (b) 65° (c) 235° (d) 45°
3. An angle of 100° is <span class="marks">[1]</span>
   (a) acute (b) right (c) obtuse (d) reflex
4. Vertically opposite angles are <span class="marks">[1]</span>
   (a) supplementary (b) complementary (c) equal (d) always 90°
5. When a transversal cuts two parallel lines, alternate angles are
   <span class="marks">[1]</span>
   (a) equal (b) supplementary (c) complementary (d) unequal
6. Co-interior angles add up to <span class="marks">[1]</span>
   (a) 90° (b) 180° (c) 270° (d) 360°

::: note Answers to Group A
**1.** (b) — $90-40=50$.
**2.** (a) — $180-125=55$.
**3.** (c) — between 90° and 180°.
**4.** (c) — equal.
**5.** (a) — equal, and that is the test for parallel lines.
**6.** (b) — 180°.
:::

**Group B — Short answer (2 marks each)**

1. Two angles are complementary and one is four times the other. Find both.
   <span class="marks">[2]</span>
2. Two straight lines intersect and one angle is 42°. Find the other three.
   <span class="marks">[2]</span>
3. A transversal cuts two parallel lines. A pair of corresponding angles are
   $2x+10$ and $70$. Find $x$. <span class="marks">[2]</span>
4. State whether the lines are parallel: a pair of co-interior angles measure
   110° and 60°. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** $x+4x=90$, so $5x=90$ and $x=18°$; the angles are 18° and 72°.
**2.** 42° (vertically opposite), 138° and 138° (each supplementary to 42°).
**3.** $2x+10=70$, so $2x=60$ and $x=30$.
**4.** $110+60=170\ne180$, so they are **not** parallel.
:::

**Group C — Long answer (4 marks each)**

1. Two parallel lines are cut by a transversal. One of the co-interior angles is
   $4x-15$ and the other is $2x+45$. Find the value of $x$ and the size of every
   angle in the figure. <span class="marks">[4]</span>
2. In the figure, angle 1 and angle 5 are corresponding angles and angle 1 is
   $70°$. Find angles 2, 3, 4, 5, 6, 7 and 8, stating the reason for each, and
   verify that the sum of the angles round the two vertices is 360° each.
   <span class="marks">[4]</span>

::: note Answers to Group C
**1.** Co-interior angles are supplementary:
$$(4x-15)+(2x+45)=180 \;\Longrightarrow\; 6x+30=180$$

$$6x=150 \;\Longrightarrow\; x=25$$
The angles are $4(25)-15=85°$ and $2(25)+45=95°$. Every acute angle in the
figure is $85°$ and every obtuse angle is $95°$, because corresponding and
alternate angles are equal and each angle is supplementary to the one beside it.
**Check.** $85+95=180$ ✓, and round either vertex
$85+95+85+95=360$ ✓.
**2.** With angle 1 $=70°$: **angle 2** $=110°$ (linear pair with 1);
**angle 3** $=70°$ (vertically opposite to 1); **angle 4** $=110°$ (vertically
opposite to 2); **angle 5** $=70°$ (corresponding to angle 1); **angle 6**
$=110°$ (linear pair with 5, or corresponding to 2); **angle 7** $=70°$
(vertically opposite to 5); **angle 8** $=110°$ (vertically opposite to 6).
**Check.** At the upper vertex: $70+110+70+110=360$ ✓. At the lower vertex:
$70+110+70+110=360$ ✓. Every acute angle in the figure is 70° and every obtuse
one is 110°, which is exactly what two parallel lines force: angles 1 and 3 are
vertically opposite, 1 and 5 are corresponding, 3 and 5 are vertically opposite
again, and each of 2, 4, 6, 8 is the supplement of one of them.
:::

**Extra practice**

**Group B (2 marks)**

**14.** Two angles of a triangle are $42°$ and $78°$. Find the third angle and the
    exterior angle at that vertex.
**15.** Find each exterior angle of a regular polygon of 12 sides.

**Group C (4 marks)**

**16.** In a parallelogram $PQRS$, $\angle P = 72°$. Find the other three angles
    with reasons.

::: note Extra practice — answers
**14.** Third angle $= 180° - 120° = 60°$; exterior angle $= 180° - 60° = 120°$
(which equals $42° + 78°$, the exterior angle property).
**15.** $\frac{360°}{12} = 30°$.
**16.** $\angle R = \angle P = 72°$ — *opposite angles of a parallelogram are
equal*. $\angle Q = 180° - 72° = 108°$ — *co-interior angles between the
parallel sides are supplementary*. $\angle S = \angle Q = 108°$ — *opposite
angles*. Check: $72 + 108 + 72 + 108 = 360°$.
:::
