---
subject: Mathematics
grade: 10
unit: 5
title: Plane Surfaces
hours: 0
area: Compulsory Mathematics
---

A plane surface is any flat shape — the floor of a classroom, a triangular plot of land, a round garden, a ring-shaped running track. Finding its **perimeter** tells us how much fencing or boundary we need; finding its **area** tells us how much paint, tile, carpet or seed we need. This chapter collects the area and perimeter formulas for the triangle, the quadrilaterals and the circle, adds Heron's formula and the sector, and then applies everything to paths, rings and combined figures, with costs. The SEE tests whether you can break an unfamiliar figure into simple pieces.

::: key What the SEE asks from this chapter
Typical questions (3 or 4 marks): (i) area of a triangle by **Heron's formula**; (ii) area of a **path** around a rectangular or circular garden, with the cost; (iii) area and perimeter of a **combined figure** (rectangle plus semicircle); (iv) the number of **tiles** needed for a floor; (v) area of a **ring** or **sector**. Unless told otherwise use $\pi=\dfrac{22}{7}$. Every answer needs a unit: m, m², cm², Rs.
:::

## 5.1 Plane Surfaces: concepts, formulas and worked problems

### Perimeter and area: the difference

**Perimeter** is the length of the boundary — measured in cm, m, km. **Area** is the amount of surface inside the boundary — measured in cm², m². Fencing a field needs the perimeter; ploughing it needs the area.

| Figure | Perimeter | Area |
|---|---|---|
| Rectangle ($l$, $b$) | $2(l+b)$ | $lb$ |
| Square (side $a$) | $4a$ | $a^2$ |
| Triangle (base $b$, height $h$) | sum of the sides | $\dfrac12 bh$ |
| Parallelogram (base $b$, height $h$) | $2(a+b)$ | $bh$ |
| Rhombus (diagonals $d_1,d_2$; side $a$) | $4a$ | $\dfrac12 d_1d_2$ |
| Trapezium (parallel sides $a,b$; height $h$) | sum of the sides | $\dfrac12(a+b)h$ |
| Circle (radius $r$) | $2\pi r$ | $\pi r^2$ |

```figure caption="Height (dashed) is the perpendicular distance between the base and the opposite side or vertex; it is not the slanting side."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon
fig, axes = plt.subplots(1, 3, figsize=(5.0, 2.3))
def style(ax, xl, yl):
    ax.set_xlim(*xl); ax.set_ylim(*yl); ax.set_aspect('equal'); ax.axis('off')
ax = axes[0]
ax.add_patch(Polygon([(0,0),(6,0),(2,3.6)], fc='#dbeafe', ec=INK, lw=1.1))
ax.plot([2,2],[0,3.6], ls='--', color=ACCENT, lw=1)
ax.text(3,-0.7,'base b', ha='center', fontsize=8)
ax.text(2.2,1.7,'h', fontsize=8, color=ACCENT)
ax.set_title('Triangle', fontsize=8.5, pad=1)
style(ax, (-0.5,6.5), (-1.3,4.2))
ax = axes[1]
ax.add_patch(Polygon([(0,0),(5,0),(6.5,3.2),(1.5,3.2)], fc='#dcfce7', ec=INK, lw=1.1))
ax.plot([1.5,1.5],[0,3.2], ls='--', color=ACCENT, lw=1)
ax.text(2.5,-0.7,'base b', ha='center', fontsize=8)
ax.text(1.7,1.4,'h', fontsize=8, color=ACCENT)
ax.set_title('Parallelogram', fontsize=8.5, pad=1)
style(ax, (-0.5,7), (-1.3,4.2))
ax = axes[2]
ax.add_patch(Polygon([(0,0),(6,0),(4.6,3.2),(1.2,3.2)], fc='#fef3c7', ec=INK, lw=1.1))
ax.plot([1.2,1.2],[0,3.2], ls='--', color=ACCENT, lw=1)
ax.text(3,-0.7,'b', ha='center', fontsize=8)
ax.text(2.9,3.55,'a', ha='center', fontsize=8)
ax.text(1.4,1.4,'h', fontsize=8, color=ACCENT)
ax.set_title('Trapezium', fontsize=8.5, pad=1)
style(ax, (-0.5,6.5), (-1.3,4.4))
fig.tight_layout(pad=0.3)
```

::: example Rectangle: fencing and tiling
**Problem.** A rectangular room is 8 m long and 6 m wide. (a) Find its perimeter and area. (b) How many square tiles of side 40 cm are needed to cover the floor? (c) The field in front is 24 m by 18 m; find the cost of fencing it at Rs 150 per metre.

**Solution.** (a) Perimeter $=2(8+6)=28$ m. Area $=8\times 6=48$ m².

(b) Area of one tile $=0.4\times 0.4=0.16$ m². Number of tiles $=\dfrac{48}{0.16}=300$.

(c) Perimeter of field $=2(24+18)=84$ m. Cost $=84\times 150=\text{Rs } 12{,}600$.
:::

::: caution Units must match
Change all lengths to the same unit **before** you multiply. For tiles of 40 cm in a room measured in metres, write 40 cm as 0.4 m. Dividing 48 m² by 40 × 40 = 1600 gives nonsense because the units differ.
:::

### Triangles and Heron's formula

Area of a triangle $=\dfrac12\times\text{base}\times\text{height}$. If the height is not known but the three sides $a,b,c$ are, use **Heron's formula**.

::: key Heron's formula
Let the sides be $a$, $b$, $c$ and the **semi-perimeter** $s=\dfrac{a+b+c}{2}$. Then

$$ \text{Area}=\sqrt{s(s-a)(s-b)(s-c)} $$

Height on side $a$: $h_a=\dfrac{2\times\text{Area}}{a}$.

Equilateral triangle of side $a$: Area $=\dfrac{\sqrt{3}}{4}a^2$.
:::

::: example Heron's formula
**Problem.** Find the area of the triangle with sides 13 cm, 14 cm and 15 cm, and the height on the side of 14 cm.

**Solution.** $s=\dfrac{13+14+15}{2}=21$ cm.

$$ \text{Area}=\sqrt{21\times 8\times 7\times 6}=\sqrt{7056}=84\text{ cm}^2 $$

Here $s-a=21-13=8$, $s-b=21-14=7$ and $s-c=21-15=6$.

Height on 14 cm: $h=\dfrac{2\times 84}{14}=12$ cm.
:::

```figure caption="Triangle with sides 13, 14 and 15 cm. Heron's formula gives area 84 cm², and the height on the 14 cm side is 12 cm."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon
fig, ax = plt.subplots(figsize=(4.3, 2.7))
A, B, C = (0, 0), (14, 0), (5, 12)
ax.add_patch(Polygon([A, B, C], fc='#dbeafe', ec=INK, lw=1.2))
ax.plot([5, 5], [0, 12], ls='--', color=ACCENT, lw=1)
ax.plot([5, 5.9, 5.9], [0.9, 0.9, 0], color=ACCENT, lw=0.8)
ax.text(7, -1.3, '14 cm', ha='center', fontsize=8.5)
ax.text(1.5, 6.8, '13 cm', ha='center', fontsize=8.5, rotation=67)
ax.text(10.6, 7.0, '15 cm', ha='center', fontsize=8.5, rotation=-53)
ax.text(5.4, 5.5, 'h = 12', ha='left', fontsize=8.5, color=ACCENT)
ax.text(-0.3, -0.9, 'A', fontsize=9, ha='right'); ax.text(14.3, -0.9, 'B', fontsize=9)
ax.text(5, 12.5, 'C', fontsize=9, ha='center')
ax.set_xlim(-2, 16); ax.set_ylim(-2.5, 13.8); ax.set_aspect('equal'); ax.axis('off')
```

::: example Cost of a triangular plot
**Problem.** A triangular plot has sides 9 m, 40 m and 41 m. Find its area, and the cost of levelling it at Rs 500 per m².

**Solution.** $s=\dfrac{9+40+41}{2}=45$ m.

$$ \text{Area}=\sqrt{45\times 36\times 5\times 4}=\sqrt{32400}=180\text{ m}^2 $$

(Check: $9^2+40^2=81+1600=1681=41^2$, so it is right-angled and the area is $\frac12\times 9\times 40=180$ ✓.)

Cost $=180\times 500=\text{Rs } 90{,}000$.
:::

::: example Equilateral triangle
**Problem.** Find the area of an equilateral triangle of side 10 cm. (Take $\sqrt{3}=1.732$.)

**Solution.** Area $=\dfrac{\sqrt{3}}{4}\times 10^2=\dfrac{1.732\times 100}{4}=43.3\text{ cm}^2$.
:::

### Quadrilaterals

::: example Parallelogram and rhombus
**Problem.** (a) A parallelogram has base 15 cm and height 8 cm. Find its area. (b) The diagonals of a rhombus are 16 cm and 12 cm. Find its area, side and perimeter.

**Solution.** (a) Area $=bh=15\times 8=120\text{ cm}^2$.

(b) Area $=\dfrac12 d_1d_2=\dfrac12\times 16\times 12=96\text{ cm}^2$.

The diagonals of a rhombus bisect each other at right angles, so half-diagonals are 8 and 6 and the side is $\sqrt{8^2+6^2}=\sqrt{100}=10$ cm.

Perimeter $=4\times 10=40$ cm.
:::

::: example Trapezium
**Problem.** A field is in the shape of a trapezium with parallel sides 20 m and 12 m, the distance between them being 8 m. Find its area.

**Solution.** Area $=\dfrac12(20+12)\times 8=\dfrac12\times 32\times 8=128\text{ m}^2$.
:::

::: example Quadrilateral split by a diagonal
**Problem.** In quadrilateral $ABCD$, diagonal $AC=20$ cm, and the perpendiculars from $B$ and $D$ to $AC$ are 7 cm and 5 cm. Find the area.

**Solution.** The diagonal splits $ABCD$ into triangles $ABC$ and $ADC$ with the same base $AC$.

$$ \text{Area}=\tfrac12\times 20\times 7+\tfrac12\times 20\times 5=70+50=120\text{ cm}^2 $$

or $\dfrac12\times 20\times(7+5)=120$ cm².
:::

### The circle, semicircle and sector

::: key Circle formulas ($\pi=\frac{22}{7}$ unless told otherwise)
- Circumference $C=2\pi r=\pi d$; Area $A=\pi r^2$.
- Semicircle: area $\dfrac12\pi r^2$; perimeter $\pi r+2r$ (curved part plus the diameter).
- Sector with angle $\theta$: arc length $=\dfrac{\theta}{360}\times 2\pi r$; area $=\dfrac{\theta}{360}\times\pi r^2$.
:::

::: example Circle and semicircle
**Problem.** (a) Find the circumference and area of a circle of radius 7 cm. (b) Find the perimeter and area of a semicircle of radius 14 cm.

**Solution.** (a) $C=2\times\dfrac{22}{7}\times 7=44$ cm; $A=\dfrac{22}{7}\times 7^2=154\text{ cm}^2$.

(b) Curved part $=\pi r=\dfrac{22}{7}\times 14=44$ cm. Perimeter $=44+2\times 14=72$ cm.

Area $=\dfrac12\times\dfrac{22}{7}\times 14^2=\dfrac12\times\dfrac{22}{7}\times 196=308\text{ cm}^2$.
:::

```figure caption="A sector of angle θ is the fraction θ/360 of the whole circle: its arc and its area are the same fraction of the circumference and the area."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Wedge, Circle
fig, ax = plt.subplots(figsize=(4.0, 2.8))
ax.add_patch(Wedge((0,0), 1, 0, 60, fc='#dbeafe', ec=INK, lw=1.2))
ax.plot([0,1],[0,0], color=INK, lw=1.2)
ax.text(0.5, -0.1, 'r = 21 cm', ha='center', va='top', fontsize=8)
ax.text(-0.1, 0.1, 'θ = 60°', fontsize=8, ha='right', va='center')
ax.annotate('arc = 22 cm', xy=(0.88, 0.52), xytext=(1.12, 0.78), fontsize=8, arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.7))
ax.text(0.62, 0.3, 'area\n231 cm²', fontsize=7.5, ha='center', va='center')
ax.set_xlim(-0.8, 1.9); ax.set_ylim(-0.4, 1.1); ax.set_aspect('equal'); ax.axis('off')
```

::: example Arc length and area of a sector
**Problem.** Find the arc length and area of a sector of radius 21 cm and angle $60^\circ$.

**Solution.** Arc length $=\dfrac{60}{360}\times 2\times\dfrac{22}{7}\times 21=\dfrac16\times 132=22$ cm.

Area $=\dfrac{60}{360}\times\dfrac{22}{7}\times 21^2=\dfrac16\times 1386=231\text{ cm}^2$.
:::

::: example From circumference to area
**Problem.** The circumference of a circular pond is 88 m. Find its area. A square plot has the same perimeter; find its area and compare.

**Solution.** $2\pi r=88\Rightarrow r=\dfrac{88\times 7}{2\times 22}=14$ m.

Area of the pond $=\dfrac{22}{7}\times 14^2=616\text{ m}^2$.

Square plot: side $=\dfrac{88}{4}=22$ m, area $=22^2=484\text{ m}^2$.

For the same perimeter the circle encloses the larger area (616 m² against 484 m²).
:::

### Paths and rings

A **path** around a figure is the region between the figure and a larger, similar figure outside it (or a smaller one inside). Its area is always the **difference of two areas**.

::: key Path and ring
- Path outside a rectangle $l\times b$, width $w$: outer rectangle $(l+2w)\times(b+2w)$; path area $=(l+2w)(b+2w)-lb$.
- Path inside a rectangle, width $w$: inner rectangle $(l-2w)\times(b-2w)$; path area $=lb-(l-2w)(b-2w)$.
- Circular ring with outer radius $R$ and inner radius $r$: area $=\pi R^2-\pi r^2=\pi(R+r)(R-r)$.
- Circular path of width $w$ outside a circle of radius $r$: $R=r+w$.
:::

::: example Path inside a rectangle
**Problem.** A rectangular garden is 30 m long and 20 m wide. A path 2 m wide runs inside along the whole boundary. Find the area of the path and the cost of paving it at Rs 120 per m².

**Solution.** Garden: $30\times 20=600\text{ m}^2$.

Inner rectangle: $(30-2\times 2)\times(20-2\times 2)=26\times 16=416\text{ m}^2$.

Area of path $=600-416=184\text{ m}^2$.

Cost $=184\times 120=\text{Rs } 22{,}080$.
:::

::: example Path outside a rectangle
**Problem.** A park is 40 m by 30 m. A path 2 m wide is built outside it all round. Find the area of the path.

**Solution.** Outer rectangle $=(40+4)\times(30+4)=44\times 34=1496\text{ m}^2$.

Park $=40\times 30=1200\text{ m}^2$.

Area of path $=1496-1200=296\text{ m}^2$.
:::

```figure caption="A circular garden of radius 14 m with a 7 m wide path round it. The path is a ring with outer radius 21 m and inner radius 14 m."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle
fig, ax = plt.subplots(figsize=(4.0, 3.0))
ax.add_patch(Circle((0,0), 21, fc='#fde68a', ec=INK, lw=1.2))
ax.add_patch(Circle((0,0), 14, fc='#bbf7d0', ec=INK, lw=1.2))
ax.annotate('', xy=(14, 0), xytext=(0, 0), arrowprops=dict(arrowstyle='-|>', color=INK, lw=0.9))
ax.annotate('', xy=(21*np.cos(0.9), 21*np.sin(0.9)-0.0), xytext=(0, 0), arrowprops=dict(arrowstyle='-|>', color=INK, lw=0.9))
ax.text(7, -1.2, 'r = 14', ha='center', va='top', fontsize=8.5)
ax.text(14.0, 17.5, 'R = 21', ha='left', va='center', fontsize=8.5)
ax.text(0, -8.3, 'garden', ha='center', fontsize=8.5)
ax.text(-17.5, 0, 'path', ha='center', va='center', fontsize=8.5)
ax.set_xlim(-23, 30); ax.set_ylim(-23, 23); ax.set_aspect('equal'); ax.axis('off')
```

::: example Circular path
**Problem.** A circular garden has radius 14 m. A path 7 m wide is made all round outside it. Find the area of the path, the cost of paving it at Rs 450 per m², and the cost of fencing the outer edge at Rs 200 per metre.

**Solution.** Outer radius $R=14+7=21$ m, inner radius $r=14$ m.

Area of path $=\pi(R^2-r^2)=\dfrac{22}{7}(441-196)=\dfrac{22}{7}\times 245=770\text{ m}^2$.

Paving cost $=770\times 450=\text{Rs } 3{,}46{,}500$.

Outer circumference $=2\times\dfrac{22}{7}\times 21=132$ m. Fencing cost $=132\times 200=\text{Rs } 26{,}400$.
:::

::: example Ring
**Problem.** A circular ring-shaped track has outer radius 14 m and inner radius 7 m. Find its area.

**Solution.** Area $=\dfrac{22}{7}(14^2-7^2)=\dfrac{22}{7}\times 147=462\text{ m}^2$.
:::

### Combined figures

Split the figure into rectangles, triangles, semicircles; add (or subtract) the areas. For the **perimeter** include only the boundary that is outside — a side where two pieces join is **not** part of the boundary.

```figure caption="A hall plan: a rectangle 21 m by 14 m with a semicircle on one 14 m side. The joining 14 m line is not part of the boundary."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Wedge
fig, ax = plt.subplots(figsize=(4.4, 2.5))
ax.add_patch(Rectangle((0,0), 21, 14, fc='#dbeafe', ec=INK, lw=1.2))
ax.add_patch(Wedge((21, 7), 7, -90, 90, fc='#fde68a', ec=INK, lw=1.2))
ax.plot([21,21],[0,14], color=INK, lw=0.8, ls='--')
ax.text(10.5, 7, 'rectangle\n294 m²', ha='center', va='center', fontsize=8.5)
ax.text(29.5, 7, 'semicircle\n77 m²', ha='left', va='center', fontsize=8)
ax.text(10.5, -1.6, '21 m', ha='center', va='top', fontsize=8.5)
ax.text(-0.8, 7, '14 m', ha='right', va='center', fontsize=8.5)
ax.set_xlim(-4.5, 37); ax.set_ylim(-4.2, 15); ax.set_aspect('equal'); ax.axis('off')
```

::: example Rectangle with a semicircle
**Problem.** The figure shows a rectangle of length 21 m and breadth 14 m with a semicircle on one of the 14 m sides. Find the area and the perimeter, and the cost of painting the floor at Rs 20 per m².

**Solution.** Radius of semicircle $=\dfrac{14}{2}=7$ m.

Area of rectangle $=21\times 14=294\text{ m}^2$.

Area of semicircle $=\dfrac12\times\dfrac{22}{7}\times 7^2=77\text{ m}^2$.

Total area $=294+77=371\text{ m}^2$.

Perimeter $=21+21+14+\pi r$ where the curved part $=\dfrac{22}{7}\times 7=22$ m. The 14 m side where the semicircle joins is **not** counted.

Perimeter $=21+21+14+22=78$ m.

Cost $=371\times 20=\text{Rs } 7{,}420$.
:::

::: tip Strategy for a figure you have not seen
Draw it. Mark all given lengths. Split it into rectangles, triangles and circular pieces. Find each area, add or subtract. For the perimeter, trace along the outside edge only and list each piece of boundary once.
:::

::: caution Common mistakes
- Using the **slant side** instead of the perpendicular height of a parallelogram or trapezium.
- Taking the path width once instead of **twice** when the path is on both sides: outer length $=l+2w$, inner length $=l-2w$.
- Using the diameter in $\pi r^2$. Halve it first.
- Counting the joining line in the perimeter of a combined figure.
- Forgetting that $\frac12 bh$ needs the **perpendicular** height. In a right-angled triangle, use the two sides containing the right angle.
:::

## 5.2 Exercises of the SEE type

### Method

1. Sketch the figure and write the data in the same unit.
2. Choose the formula: triangle (use Heron if only the sides are given), quadrilateral, circle, sector.
3. For paths and rings: area $=$ (outer area) $-$ (inner area).
4. For combined figures: add areas, and list the outer boundary for the perimeter.
5. For cost: area (or perimeter) $\times$ rate per unit.
6. Give the unit of the answer (m, m², Rs).

## Chapter summary

- Rectangle $lb$, $2(l+b)$; square $a^2$, $4a$; triangle $\frac12bh$; parallelogram $bh$; rhombus $\frac12d_1d_2$; trapezium $\frac12(a+b)h$.
- Heron: $s=\frac{a+b+c}{2}$, Area $=\sqrt{s(s-a)(s-b)(s-c)}$; equilateral $\frac{\sqrt{3}}{4}a^2$.
- Circle: $C=2\pi r$, $A=\pi r^2$; semicircle perimeter $\pi r+2r$, area $\frac12\pi r^2$.
- Sector: arc $=\frac{\theta}{360}\times2\pi r$, area $=\frac{\theta}{360}\times\pi r^2$.
- Path or ring $=$ larger area $-$ smaller area; ring $=\pi(R^2-r^2)$.
- Path outside a rectangle adds $2w$ to each side; path inside subtracts $2w$.
- Combined figure: add areas; the joining line is not in the perimeter.
- Cost $=$ area (or length) $\times$ rate; number of tiles $=$ floor area $\div$ one tile.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The area of a triangle with base 10 cm and height 6 cm is <span class="marks">[1]</span>
   (a) 60 cm² (b) 30 cm² (c) 16 cm² (d) 15 cm²
2. The circumference of a circle of radius 7 cm ($\pi=\frac{22}{7}$) is <span class="marks">[1]</span>
   (a) 22 cm (b) 154 cm (c) 44 cm (d) 49 cm
3. The area of a trapezium with parallel sides 8 cm and 12 cm and height 5 cm is <span class="marks">[1]</span>
   (a) 50 cm² (b) 100 cm² (c) 40 cm² (d) 60 cm²
4. The area of a ring with outer radius 5 cm and inner radius 3 cm is <span class="marks">[1]</span>
   (a) $4\pi$ cm² (b) $8\pi$ cm² (c) $16\pi$ cm² (d) $34\pi$ cm²
5. The semi-perimeter of a triangle with sides 6 cm, 8 cm and 10 cm is <span class="marks">[1]</span>
   (a) 24 cm (b) 12 cm (c) 8 cm (d) 10 cm

::: note Answers to Group A
**1.** (b) — $\frac12\times 10\times 6=30$.
**2.** (c) — $2\times\frac{22}{7}\times 7=44$.
**3.** (a) — $\frac12(8+12)\times 5=50$.
**4.** (c) — $\pi(25-9)=16\pi$.
**5.** (b) — $\frac{6+8+10}{2}=12$.
:::

**Group B — Short answer (2 marks each)**

1. Find the area of a parallelogram with base 15 cm and height 8 cm. <span class="marks">[2]</span>
2. Find the area of a rhombus whose diagonals are 10 cm and 24 cm. <span class="marks">[2]</span>
3. Find the area of a circle of diameter 28 cm. <span class="marks">[2]</span>
4. Find the perimeter of a semicircle of radius 7 cm. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** $bh=15\times 8=120\text{ cm}^2$.
**2.** $\frac12\times 10\times 24=120\text{ cm}^2$.
**3.** $r=14$: $\frac{22}{7}\times 14^2=\frac{22}{7}\times 196=616\text{ cm}^2$.
**4.** $\pi r+2r=22+14=36$ cm.
:::

**Group C — Short answer (3 marks each)**

1. Find the area of a triangle with sides 17 cm, 25 cm and 28 cm. <span class="marks">[3]</span>
2. A park 40 m long and 30 m wide has a path 2 m wide built outside it. Find the area of the path and the cost of paving it at Rs 75 per m². <span class="marks">[3]</span>
3. Find the area of a circular ring of outer radius 14 cm and inner radius 7 cm. <span class="marks">[3]</span>
4. Find the arc length and the area of a sector of radius 14 cm and angle $90^\circ$. <span class="marks">[3]</span>

::: note Answers to Group C
**1.** $s=\frac{17+25+28}{2}=35$. Area $=\sqrt{35\times 18\times 10\times 7}=\sqrt{44100}=210\text{ cm}^2$.
**2.** Outer rectangle $44\times 34=1496$; park $=1200$; path $=296\text{ m}^2$. Cost $=296\times 75=\text{Rs } 22{,}200$.
**3.** $\frac{22}{7}(14^2-7^2)=\frac{22}{7}\times 147=462\text{ cm}^2$.
**4.** Arc $=\frac{90}{360}\times 2\times\frac{22}{7}\times 14=22$ cm. Area $=\frac14\times\frac{22}{7}\times 196=154\text{ cm}^2$.
:::

**Group D — Long answer (4 marks each)**

1. A field is a trapezium with parallel sides 60 m and 40 m, and the distance between them is 30 m. Find its area and the cost of ploughing it at Rs 12 per m². <span class="marks">[4]</span>
2. A rectangular hall 12 m by 9 m is to be covered with square tiles of side 30 cm. Find the number of tiles, and the cost at Rs 45 per tile. <span class="marks">[4]</span>
3. A circular garden of radius 14 m has a 7 m wide path outside it. Find the area of the path, the cost of paving it at Rs 450 per m², and the cost of fencing the outer boundary at Rs 200 per metre. <span class="marks">[4]</span>
4. A floor consists of a rectangle 21 m by 14 m with a semicircle on one 14 m side. Find its area and perimeter, and the cost of painting at Rs 20 per m². <span class="marks">[4]</span>

::: note Answers to Group D
**1.** Area $=\frac12(60+40)\times 30=1500\text{ m}^2$. Cost $=1500\times 12=\text{Rs } 18{,}000$.
**2.** Hall area $=12\times 9=108\text{ m}^2$. Tile area $=0.3\times 0.3=0.09\text{ m}^2$. Tiles $=\frac{108}{0.09}=1200$. Cost $=1200\times 45=\text{Rs } 54{,}000$.
**3.** $R=14+7=21$. Path $=\frac{22}{7}(441-196)=770\text{ m}^2$. Paving $=770\times 450=\text{Rs } 3{,}46{,}500$. Outer circumference $=2\times\frac{22}{7}\times 21=132$ m; fencing $=132\times 200=\text{Rs } 26{,}400$.
**4.** Rectangle $294$; semicircle $\frac12\times\frac{22}{7}\times 49=77$; area $=371\text{ m}^2$. Perimeter $=21+21+14+22=78$ m. Cost $=371\times 20=\text{Rs } 7{,}420$.
:::
