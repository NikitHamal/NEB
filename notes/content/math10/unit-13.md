---
subject: Mathematics
grade: 10
unit: 13
title: Area of Triangles and Quadrilaterals
hours: 0
area: Compulsory Mathematics
---

In Chapter 5 you calculated areas with formulas. Here we ask a deeper question: **when do two figures have equal areas without measuring them?** The answer is a family of theorems about triangles and parallelograms standing on the same base and lying between the same parallel lines. These theorems explain why a triangle is exactly half of a parallelogram, why a median halves a triangle, and why a farmer can swap a crooked boundary for a straight one without changing the area of the field. In the SEE you must be able to **prove** the main theorems with a neat figure, and **use** them in numerical and "prove that" questions.

::: key What the SEE asks from this chapter
Expect: (i) **prove** that parallelograms on the same base and between the same parallels are equal in area (3–4 marks, figure required); (ii) **prove** that a triangle and a parallelogram on the same base and between the same parallels satisfy $\Delta=\frac{1}{2}\,\text{parallelogram}$; (iii) apply the theorems: "prove that the diagonals of a parallelogram divide it into four equal triangles", "a median divides a triangle into two equal parts", or find an area from a ratio; (iv) numerical problems with heights and bases. Write: **Given, To prove, Construction, Proof** and give a reason for every line.
:::

## 13.1 Area of Triangles and Quadrilaterals: concepts, formulas and worked problems

### Basic area formulas to remember

| Figure | Area |
|---|---|
| Rectangle | length $\times$ breadth |
| Parallelogram | base $\times$ perpendicular height |
| Triangle | $\frac{1}{2}\times$ base $\times$ height |
| Trapezium | $\frac{1}{2}(a+b)\,h$, where $a,b$ are the parallel sides |
| Rhombus | $\frac{1}{2}\times d_1\times d_2$ |
| Quadrilateral with diagonal $d$ and offsets $h_1,h_2$ | $\frac{1}{2}\,d\,(h_1+h_2)$ |

**Equal in area** is written $\text{area}(\Delta ABC)=\text{area}(\Delta PQR)$. Two figures can be equal in area without being congruent: a $12\times 5$ rectangle and a $10\times 6$ rectangle both have area 60 but have different shapes.

### Same base, between the same parallels

Two figures are **on the same base and between the same parallels** if they share a base line, and their opposite vertices (or sides) lie on a single line parallel to that base. Then the **perpendicular height is the same** for both — this is the whole secret of the theorems.

```figure caption="Parallelograms ABCD and ABEF stand on the same base AB and lie between the parallels AB and DF. Both have the height h."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon
fig, ax = plt.subplots(figsize=(4.8, 2.4))
A, B = (0, 0), (5, 0)
D, C = (1.2, 2), (6.2, 2)
F, E = (3.0, 2), (8.0, 2)
ax.add_patch(Polygon([A, B, C, D], fc='#dbeafe', ec=INK, lw=1.1))
ax.add_patch(Polygon([A, B, E, F], fc='none', ec='#dc2626', lw=1.1, ls='--'))
ax.plot([0, 8.6], [2, 2], color=MUTED, lw=0.8)
ax.plot([-0.6, 8.6], [0, 0], color=MUTED, lw=0.8)
ax.plot([3, 3], [0, 2], color=ACCENT, lw=1.0, ls=':')
ax.text(3.12, 1.0, 'h', fontsize=8.5, color=ACCENT)
for p, t, dx, dy in [(A, 'A', -0.3, -0.3), (B, 'B', 0.1, -0.35), (C, 'C', 0.05, 0.15), (D, 'D', -0.2, 0.15), (E, 'E', 0.1, 0.15), (F, 'F', -0.05, 0.15)]:
    ax.text(p[0] + dx, p[1] + dy, t, fontsize=9)
ax.set_xlim(-0.8, 9); ax.set_ylim(-0.7, 2.7); ax.set_aspect('equal'); ax.axis('off')
fig.tight_layout(pad=0.3)
```

### Theorem 1 — parallelograms on the same base

::: derivation Parallelograms on the same base and between the same parallels are equal in area
**Given.** Parallelograms $ABCD$ and $ABEF$ stand on the same base $AB$ and lie between the same parallels $AB$ and $DF$ (as in the figure above).

**To prove.** $\text{area}(\text{parallelogram }ABCD)=\text{area}(\text{parallelogram }ABEF)$.

**Proof.**

**Step 1 — compare the triangles $ADF$ and $BCE$.** $AD=BC$ (opposite sides of parallelogram $ABCD$) and $AF=BE$ (opposite sides of parallelogram $ABEF$). Also $DC=AB=FE$, so $DF=DC-FC=FE-FC=CE$. Hence $\Delta ADF\cong\Delta BCE$ by SSS, and $\text{area}(\Delta ADF)=\text{area}(\Delta BCE)$.

**Step 2 — add the same quadrilateral to each.** Let $ABCF$ be the quadrilateral common to both parallelograms. Then

$$ \text{area}(\text{parallelogram }ABCD)=\text{area}(ABCF)+\text{area}(\Delta ADF) $$

$$ \text{area}(\text{parallelogram }ABEF)=\text{area}(ABCF)+\text{area}(\Delta BCE) $$

**Step 3 — equals added to equals.** The triangles are equal in area, and $ABCF$ is common, so the two right-hand sides are equal.

**Result.** $\text{area}(\text{parallelogram }ABCD)=\text{area}(\text{parallelogram }ABEF)$. Proved.

**What it means.** Slide the top side of a parallelogram along the top parallel and the area does not change. Only the base and the **height** matter.
:::

::: example Same base, same height
**Problem.** A rectangle $ABEF$ has $AB=10$ cm and $BE=6$ cm. A parallelogram $ABCD$ is on the same base $AB$ and between the same parallels, with side $BC=8$ cm. Find the area of the parallelogram, and compare the perimeters.

**Solution.** Both figures are between the same parallels, so the height of the parallelogram is also 6 cm. Area $=10\times6=60\text{ cm}^2$ — equal to the rectangle.

Perimeters: rectangle $2(10+6)=32$ cm; parallelogram $2(10+8)=36$ cm. Equal area but unequal perimeters: of all parallelograms on the same base and between the same parallels, **the rectangle has the least perimeter**.
:::

::: example Finding a second height
**Problem.** In parallelogram $ABCD$, $AB=15$ cm, $AD=10$ cm and the perpendicular distance between $AB$ and $DC$ is 8 cm. Find the distance between $AD$ and $BC$.

**Solution.** Area $=\text{base}\times\text{height}=15\times8=120\text{ cm}^2$. Using $AD$ as base, $10\times h=120$ gives $h=12$ cm.
:::

### Theorem 2 — triangle and parallelogram

```figure caption="Triangle ABE and parallelogram ABCD stand on the same base AB and lie between the same parallels AB and DC; the diagonal AC of the parallelogram splits it into two equal triangles."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon
fig, ax = plt.subplots(figsize=(4.8, 2.4))
A, B, C, D = (0, 0), (5, 0), (6.2, 2), (1.2, 2)
P = (3.6, 2)
ax.add_patch(Polygon([A, B, C, D], fc='#dbeafe', ec=INK, lw=1.1))
ax.add_patch(Polygon([A, B, P], fc='#fde68a', ec=INK, lw=1.1))
ax.plot([0.2, 7.0], [2, 2], color=MUTED, lw=0.8)
ax.plot([-0.6, 7.0], [0, 0], color=MUTED, lw=0.8)
for p, t, dx, dy in [(A, 'A', -0.3, -0.3), (B, 'B', 0.1, -0.35), (C, 'C', 0.1, 0.12), (D, 'D', -0.3, 0.12), (P, 'P', -0.05, 0.15)]:
    ax.text(p[0] + dx, p[1] + dy, t, fontsize=9)
ax.text(3.0, 0.6, 'Δ APB', fontsize=8.5, ha='center')
ax.set_xlim(-0.8, 7.2); ax.set_ylim(-0.7, 2.7); ax.set_aspect('equal'); ax.axis('off')
fig.tight_layout(pad=0.3)
```

::: derivation A triangle on the same base as a parallelogram is half of it
**Given.** Parallelogram $ABCD$ and triangle $ABP$ are on the same base $AB$ and between the same parallels $AB$ and $DC$ ($P$ lies on $DC$).

**To prove.** $\text{area}(\Delta ABP)=\frac{1}{2}\,\text{area}(\text{parallelogram }ABCD)$.

**Construction.** Join $AC$.

**Proof.**

**Step 1 — the diagonal halves the parallelogram.** A diagonal of a parallelogram divides it into two congruent triangles, so

$$ \text{area}(\Delta ABC)=\frac{1}{2}\,\text{area}(\text{parallelogram }ABCD) $$

**Step 2 — triangles on the same base and between the same parallels.** $\Delta ABC$ and $\Delta ABP$ have the same base $AB$ and the same height (the distance between $AB$ and $DC$), so $\text{area}(\Delta ABP)=\text{area}(\Delta ABC)$. (This is Theorem 3 below; here the result follows directly from $\frac{1}{2}\times AB\times h$ for both.)

**Result.** $\text{area}(\Delta ABP)=\frac{1}{2}\,\text{area}(\text{parallelogram }ABCD)$. Proved.

**What it means.** The area of a triangle is half the area of the parallelogram with the same base and height: $\frac{1}{2}\times\text{base}\times\text{height}$ — the familiar triangle formula, now proved.
:::

::: key The theorems to learn
1. **Parallelograms** on the same base and between the same parallels are equal in area.
2. A **triangle** on the same base as a parallelogram, and between the same parallels, has **half** its area.
3. **Triangles** on the same base and between the same parallels are equal in area.
4. Triangles on equal bases and between the same parallels are equal in area.
5. A **median** of a triangle divides it into two triangles of equal area.
6. The diagonals of a parallelogram divide it into **four triangles of equal area**.
:::

### Theorem 3 — triangles on the same base

```figure caption="Triangles ABC, ABD and ABE have the same base AB and their vertices lie on the line l parallel to AB: all three have equal area."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon
fig, ax = plt.subplots(figsize=(4.8, 2.3))
A, B = (1.5, 0), (5.5, 0)
tops = [(-0.2, 2), (3.2, 2), (7.2, 2)]
cols = ['#dbeafe', '#dcfce7', '#fde68a']
for P, c in zip(tops, cols):
    ax.add_patch(Polygon([A, B, P], fc='none', ec=INK, lw=1.0))
ax.add_patch(Polygon([A, B, tops[1]], fc='#dcfce7', ec=INK, lw=1.1))
ax.plot([-0.8, 8.2], [2, 2], color=ACCENT, lw=1.0)
ax.plot([-0.8, 8.2], [0, 0], color=MUTED, lw=0.8)
ax.text(8.3, 2.0, 'l', fontsize=9, color=ACCENT, va='center')
ax.text(1.2, -0.35, 'A', fontsize=9); ax.text(5.6, -0.35, 'B', fontsize=9)
for P, t in zip(tops, 'CDE'):
    ax.text(P[0] - 0.1, 2.15, t, fontsize=9)
ax.annotate('', xy=(3.2, 0.02), xytext=(3.2, 1.98), arrowprops=dict(arrowstyle='<->', color=ACCENT, lw=0.9))
ax.text(3.35, 1.0, 'h', fontsize=8.5, color=ACCENT)
ax.set_xlim(-0.9, 8.8); ax.set_ylim(-0.7, 2.7); ax.set_aspect('equal'); ax.axis('off')
fig.tight_layout(pad=0.3)
```

::: derivation Triangles on the same base and between the same parallels are equal
**Given.** Triangles $ABC$ and $ABD$ on the same base $AB$, with $C$ and $D$ on a line $l\parallel AB$.

**To prove.** $\text{area}(\Delta ABC)=\text{area}(\Delta ABD)$.

**Construction.** Through $A$ draw $AE\parallel BC$ and through $B$ draw $BF\parallel AD$, so that $E$ and $F$ lie on $l$ (as parallelograms $ABCE$ and $ABFD$ are formed).

**Proof.**

**Step 1.** $\text{parallelogram }ABCE$ and $\text{parallelogram }ABFD$ are on the same base $AB$ and between the same parallels, so by Theorem 1 their areas are equal.

**Step 2.** The diagonal $AC$ halves $\text{parallelogram }ABCE$: $\text{area}(\Delta ABC)=\frac{1}{2}\text{area}(\text{parallelogram }ABCE)$. The diagonal $BD$ halves $\text{parallelogram }ABFD$: $\text{area}(\Delta ABD)=\frac{1}{2}\text{area}(\text{parallelogram }ABFD)$.

**Result.** Halves of equal areas are equal, so $\text{area}(\Delta ABC)=\text{area}(\Delta ABD)$. Proved.

**What it means.** A triangle's area does not change when the apex slides along a line parallel to the base — as the figure shows, $C$, $D$ and $E$ give the same area.
:::

::: example Triangles with a moving apex
**Problem.** The base $BC=10$ cm and the apex $A$ of $\Delta ABC$ moves along a line parallel to $BC$ at a distance of 6 cm. Find the area for every position of $A$.

**Solution.** The height is always 6 cm, so $\text{area}=\frac{1}{2}\times10\times6=30\text{ cm}^2$ for every position.
:::

::: example A median halves the triangle
**Problem.** $AD$ is a median of $\Delta ABC$ with $\text{area}(\Delta ABC)=60\text{ cm}^2$. Find the area of $\Delta ABD$. Prove your answer.

**Solution.** $D$ is the midpoint of $BC$, so $BD=DC$. $\Delta ABD$ and $\Delta ADC$ have equal bases $BD=DC$ and the **same height** from $A$ to $BC$, so their areas are equal. Each has area $\frac{60}{2}=30\text{ cm}^2$.
:::

::: example Midpoints twice
**Problem.** $D$ is the midpoint of $BC$ in $\Delta ABC$ and $E$ is the midpoint of $AD$. If $\text{area}(\Delta ABC)=72\text{ cm}^2$, find $\text{area}(\Delta BED)$.

**Solution.** $AD$ is a median, so $\text{area}(\Delta ABD)=36$. In $\Delta ABD$, $BE$ is a median ($E$ is the midpoint of $AD$), so $\text{area}(\Delta BED)=\frac{36}{2}=18\text{ cm}^2$.
:::

::: example Ratio of bases
**Problem.** $D$ lies on $BC$ with $BD:DC=2:3$. If $\text{area}(\Delta ABC)=75\text{ cm}^2$, find the areas of $\Delta ABD$ and $\Delta ADC$.

**Solution.** The two triangles have the same height from $A$, so their areas are in the ratio of their bases, $2:3$. Hence

$$ \text{area}(\Delta ABD)=\frac{2}{5}\times75=30\text{ cm}^2,\qquad \text{area}(\Delta ADC)=\frac{3}{5}\times75=45\text{ cm}^2 $$
:::

### Using the theorems

::: example Point on the opposite side
**Problem.** $ABCD$ is a parallelogram with area $90\text{ cm}^2$ and $P$ is any point on $DC$. Find the area of $\Delta APB$.

**Solution.** $\Delta APB$ and the parallelogram are on the same base $AB$ and between the same parallels $AB$ and $DC$, so $\text{area}(\Delta APB)=\frac{1}{2}\times90=45\text{ cm}^2$, wherever $P$ is on $DC$.
:::

::: derivation The diagonals of a parallelogram make four equal triangles
**Given.** $ABCD$ is a parallelogram; the diagonals $AC$ and $BD$ meet at $O$.

**To prove.** $\text{area}(\Delta AOB)=\text{area}(\Delta BOC)=\text{area}(\Delta COD)=\text{area}(\Delta DOA)$.

**Proof.**

**Step 1.** The diagonals of a parallelogram bisect each other, so $AO=OC$ and $BO=OD$.

**Step 2.** In $\Delta ABC$, $BO$ is a median (as $AO=OC$), so $\text{area}(\Delta AOB)=\text{area}(\Delta BOC)$. In $\Delta BCD$, $CO$ is a median, so $\text{area}(\Delta BOC)=\text{area}(\Delta COD)$. In $\Delta CDA$, $DO$ is a median, so $\text{area}(\Delta COD)=\text{area}(\Delta DOA)$.

**Result.** All four triangles are equal in area, each equal to $\frac{1}{4}\text{area}(\text{parallelogram }ABCD)$. Proved.
:::

```figure caption="In a trapezium ABCD (AB ∥ DC) the diagonals meet at O. Triangles ADC and BDC have the same base DC and height, so ΔAOD and ΔBOC are equal in area."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon
fig, ax = plt.subplots(figsize=(4.6, 2.6))
A, B, C, D = (0, 0), (6, 0), (4.5, 2.4), (1.5, 2.4)
O = (3.0, 1.6) if False else None
# intersection of AC and BD
def inter(p1, p2, p3, p4):
    x1, y1 = p1; x2, y2 = p2; x3, y3 = p3; x4, y4 = p4
    d = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
    t = ((x1-x3)*(y3-y4) - (y1-y3)*(x3-x4)) / d
    return (x1 + t*(x2-x1), y1 + t*(y2-y1))
O = inter(A, C, B, D)
ax.add_patch(Polygon([A, B, C, D], fc='#f1f5f9', ec=INK, lw=1.1))
ax.add_patch(Polygon([A, O, D], fc='#bfdbfe', ec=INK, lw=0.9))
ax.add_patch(Polygon([B, O, C], fc='#bfdbfe', ec=INK, lw=0.9))
ax.plot([A[0], C[0]], [A[1], C[1]], color=INK, lw=1.0)
ax.plot([B[0], D[0]], [B[1], D[1]], color=INK, lw=1.0)
for p, t, dx, dy in [(A, 'A', -0.3, -0.35), (B, 'B', 0.1, -0.35), (C, 'C', 0.1, 0.1), (D, 'D', -0.3, 0.1), (O, 'O', 0.12, -0.05)]:
    ax.text(p[0] + dx, p[1] + dy, t, fontsize=9)
ax.text(1.55, 1.55, 'x', fontsize=8.5, ha='center'); ax.text(4.45, 1.55, 'x', fontsize=8.5, ha='center')
ax.set_xlim(-0.8, 6.8); ax.set_ylim(-0.8, 3.0); ax.set_aspect('equal'); ax.axis('off')
fig.tight_layout(pad=0.3)
```

::: example Trapezium: numbers
**Problem.** In trapezium $ABCD$, $AB\parallel DC$, $AB=12$ cm, $DC=6$ cm and the height is 4 cm. The diagonals meet at $O$. Find the area of the trapezium, show that $\text{area}(\Delta AOD)=\text{area}(\Delta BOC)$ and find all four areas.

**Solution.** Trapezium area $=\frac{1}{2}(12+6)\times4=36\text{ cm}^2$.

$\Delta ADC$ and $\Delta BDC$ have the same base $DC=6$ and the same height 4, so each has area $\frac{1}{2}\times6\times4=12\text{ cm}^2$. Subtracting the common part $\Delta DOC$ from both, $\text{area}(\Delta AOD)=\text{area}(\Delta BOC)$.

Since $\Delta AOB\sim\Delta COD$ with ratio of sides $12:6=2:1$, $AO:OC=2:1$. So $\Delta ABC$ (area $\frac{1}{2}\times12\times4=24$) splits as $\Delta AOB=16$ and $\Delta BOC=8$; $\Delta ADC$ (area 12) splits as $\Delta AOD=8$ and $\Delta COD=4$. Check: $16+8+8+4=36$ ✓.
:::

::: example Area of a quadrilateral with a diagonal
**Problem.** In quadrilateral $ABCD$ the diagonal $AC=20$ cm, and the perpendiculars from $B$ and $D$ to $AC$ are 6 cm and 9 cm. Find its area.

**Solution.** $\text{Area}=\frac{1}{2}\times AC\times(h_1+h_2)=\frac{1}{2}\times20\times(6+9)=150\text{ cm}^2$.
:::

::: example Heron and the height
**Problem.** A triangle has sides 13 cm, 14 cm, 15 cm. Find its area and the height on the side of 14 cm. A second triangle on the same base lies between the same parallels; what is its area?

**Solution.** $s=\frac{13+14+15}{2}=21$. Area $=\sqrt{21\times8\times7\times6}=\sqrt{7056}=84\text{ cm}^2$. Height on 14 cm: $\frac{2\times84}{14}=12$ cm. A triangle on the same base between the same parallels has the same area: $84\text{ cm}^2$.
:::

::: caution Common mistakes
- Using the **slant side** instead of the perpendicular height in $\text{base}\times\text{height}$.
- Forgetting to say "between the same parallels" — the reason is half the marks of a proof.
- Claiming triangles are *congruent* when you only know they are *equal in area*.
- In a proof, leaving out *Given, To prove, Construction*. Draw a clear figure with all letters.
- Writing $\text{area}(\Delta ABC)=\text{area}(\Delta ABD)$ without naming the common base and the parallels.
:::

## 13.2 Exercises of the SEE type

### Method for any question

1. Draw a neat figure; mark equal sides and parallel lines.
2. For a proof: **Given – To prove – Construction – Proof**; one reason per line.
3. Identify the common base and the parallels — the height is then the same.
4. For a numerical question: area $=\text{base}\times\text{height}$ (parallelogram) or $\frac{1}{2}\times\text{base}\times\text{height}$ (triangle), then use ratios of bases or equal heights.
5. End with the stated conclusion ("Proved") or a sentence with units.

::: example SEE type: numerical
**Problem.** In the figure $ABCD$ is a parallelogram, $E$ is a point on $BC$ and $\text{area}(\Delta AED)=40\text{ cm}^2$. Find the area of $\text{parallelogram }ABCD$ and of $\Delta ABE+\Delta DCE$.

**Solution.** $\Delta AED$ and $\text{parallelogram }ABCD$ are on the same base $AD$ and between the same parallels $AD$ and $BC$, so $\text{area}(\text{parallelogram }ABCD)=2\times40=80\text{ cm}^2$. The remaining part is $80-40=40\text{ cm}^2$, so $\text{area}(\Delta ABE)+\text{area}(\Delta DCE)=40\text{ cm}^2$.
:::

::: example SEE type: prove
**Problem.** Prove that a median of a triangle divides it into two triangles of equal area.

**Solution.** *Given:* $AD$ is a median of $\Delta ABC$, so $BD=DC$. *To prove:* $\text{area}(\Delta ABD)=\text{area}(\Delta ADC)$. *Construction:* draw $AM\perp BC$. *Proof:* $\text{area}(\Delta ABD)=\frac{1}{2}\times BD\times AM$ and $\text{area}(\Delta ADC)=\frac{1}{2}\times DC\times AM$. Since $BD=DC$, the areas are equal. Proved.
:::

::: example SEE type: parallelogram and its centre
**Problem.** $ABCD$ is a parallelogram with area $64\text{ cm}^2$ and diagonals meeting at $O$. Find $\text{area}(\Delta AOB)$ and $\text{area}(\Delta AOB)+\text{area}(\Delta COD)$.

**Solution.** Each of the four triangles has area $\frac{64}{4}=16\text{ cm}^2$, and the sum of two opposite ones is $32\text{ cm}^2$.
:::

## Chapter summary

- Parallelograms on the same base and between the same parallels have equal area.
- A triangle on the same base as a parallelogram and between the same parallels has half its area.
- Triangles on the same base (or equal bases) and between the same parallels are equal in area.
- A median divides a triangle into two triangles of equal area; triangles with the same height have areas in the ratio of their bases.
- The diagonals of a parallelogram divide it into four triangles of equal area.
- Formulas: parallelogram $bh$; triangle $\frac{1}{2}bh$; trapezium $\frac{1}{2}(a+b)h$; rhombus $\frac{1}{2}d_1d_2$; quadrilateral $\frac{1}{2}d(h_1+h_2)$.
- A proof always has Given, To prove, Construction, Proof with a reason for each step.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. A triangle and a parallelogram on the same base and between the same parallels: the area of the triangle is <span class="marks">[1]</span>
   (a) equal (b) half (c) double (d) one third of the parallelogram
2. A median of a triangle divides it into two triangles which are <span class="marks">[1]</span>
   (a) congruent (b) similar (c) equal in area (d) in the ratio 1:2
3. The diagonals of a parallelogram divide it into how many equal-area triangles? <span class="marks">[1]</span>
   (a) 2 (b) 3 (c) 4 (d) 6
4. A parallelogram has base 9 cm and height 4 cm. Its area is <span class="marks">[1]</span>
   (a) 18 cm² (b) 26 cm² (c) 36 cm² (d) 13 cm²
5. Triangles on the same base and between the same parallels are <span class="marks">[1]</span>
   (a) congruent (b) equal in area (c) similar (d) isosceles

::: note Answers to Group A
**1.** (b) — Theorem 2.
**2.** (c) — equal bases, same height.
**3.** (c) — four.
**4.** (c) — $9\times4=36$.
**5.** (b) — same base, same height.
:::

**Group B — Short answer (2 marks each)**

1. A parallelogram has area $48\text{ cm}^2$. Find the area of a triangle on the same base and between the same parallels. <span class="marks">[2]</span>
2. $D$ is the midpoint of $BC$ in $\Delta ABC$ of area $50\text{ cm}^2$. Find $\text{area}(\Delta ABD)$. <span class="marks">[2]</span>
3. A parallelogram has sides 12 cm and 8 cm and the height on the 12 cm side is 5 cm. Find the height on the 8 cm side. <span class="marks">[2]</span>
4. The area of a rhombus is $96\text{ cm}^2$ and one diagonal is 16 cm. Find the other diagonal. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** $\frac{1}{2}\times48=24\text{ cm}^2$.
**2.** $25\text{ cm}^2$.
**3.** Area $=12\times5=60$; $8h=60$ so $h=7.5$ cm.
**4.** $\frac{1}{2}\times16\times d_2=96$ so $d_2=12$ cm.
:::

**Group C — Short answer (3 marks each)**

1. Prove that triangles on the same base and between the same parallels are equal in area. <span class="marks">[3]</span>
2. $ABCD$ is a parallelogram of area $64\text{ cm}^2$ and $P$ is a point on $DC$. Find $\text{area}(\Delta APB)$ and give a reason. <span class="marks">[3]</span>
3. $D$ lies on $BC$ with $BD:DC=3:5$ and $\text{area}(\Delta ABC)=96\text{ cm}^2$. Find the area of $\Delta ABD$. <span class="marks">[3]</span>
4. In quadrilateral $ABCD$ the diagonal $AC=16$ cm and the perpendiculars to it from $B$ and $D$ are 5 cm and 7 cm. Find its area. <span class="marks">[3]</span>

::: note Answers to Group C
**1.** See Theorem 3: complete the parallelograms $ABCE$ and $ABFD$; they are equal (Theorem 1), and the triangles are their halves.
**2.** $32\text{ cm}^2$ — same base $AB$, same parallels, triangle is half the parallelogram.
**3.** Same height, so area in ratio of bases: $\frac{3}{8}\times96=36\text{ cm}^2$.
**4.** $\frac{1}{2}\times16\times(5+7)=96\text{ cm}^2$.
:::

**Group D — Long answer (4 marks each)**

1. Prove that parallelograms on the same base and between the same parallels are equal in area. <span class="marks">[4]</span>
2. Prove that the diagonals of a parallelogram divide it into four triangles of equal area. <span class="marks">[4]</span>
3. In trapezium $ABCD$, $AB\parallel DC$, $AB=12$ cm, $DC=6$ cm and the height is 4 cm. Find its area and the areas of the four triangles formed by the diagonals. <span class="marks">[4]</span>
4. $D$ is the midpoint of $BC$ and $E$ is the midpoint of $AD$ in $\Delta ABC$ of area $72\text{ cm}^2$. Find the area of $\Delta BED$ and the total area of $\Delta ABE$ and $\Delta ACE$. <span class="marks">[4]</span>

::: note Answers to Group D
**1.** See Theorem 1 (congruent triangles $ADF$ and $BCE$, then subtract from the same whole).
**2.** See the derivation: $O$ is the midpoint of both diagonals, so each of the four triangles is half of a triangle with a median; each has area $\frac{1}{4}$ of the parallelogram.
**3.** Area $36\text{ cm}^2$; triangles $AOB=16$, $BOC=8$, $COD=4$, $DOA=8$ ($\text{cm}^2$).
**4.** $AD$ is a median, so $\text{area}(\Delta ABD)=\text{area}(\Delta ACD)=36$. $BE$ is a median of $\Delta ABD$, so $\text{area}(\Delta BED)=18\text{ cm}^2$. $CE$ is a median of $\Delta ACD$ and $\Delta ABE=\frac{1}{2}\Delta ABD=18$, $\Delta ACE=\frac{1}{2}\Delta ACD=18$, so together $36\text{ cm}^2$.
:::
