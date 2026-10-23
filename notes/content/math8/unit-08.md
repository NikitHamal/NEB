---
subject: Mathematics
grade: 8
unit: 8
title: Area and Volume
hours: 0
area: Compulsory Mathematics
---

Mensuration is arithmetic done with a ruler. A farmer measures a field in
*bigha*, a mason orders sand by the cubic metre, and a painter buys tin by the
square metre — all three are using the formulas in this chapter. The work is to
know which formula fits the shape, to keep the units consistent, and to remember
that an area is measured in square units and a volume in cubic units.

::: key What this chapter asks of you
You should be able to find the area of a triangle, a parallelogram, a rhombus
and a trapezium, find the area and the circumference of a circle and the area of
a sector, and find the curved surface area, total surface area and volume of a
cylinder.
:::

## 8.1 Area of triangles

For a triangle with base $b$ and perpendicular height $h$:

$$\text{Area}=\frac12\times b\times h$$

The height must be **perpendicular** to the base you choose. A triangle has
three possible base-height pairs, and all three give the same area.

A right-angled triangle is half of a rectangle (cut along a diagonal), so its
area is $\frac12\times$ base $\times$ perpendicular. Any triangle can be cut by
its height into two right-angled triangles, which is why $\frac12bh$ works for
every triangle.

::: example Area of a right-angled triangle
**Problem.** A triangle has sides 6 m, 8 m and 10 m. Show that it is
right-angled, find its area, and find the height drawn to the 10 m side.

**Solution.** $6^2+8^2=36+64=100=10^2$, so by the converse of Pythagoras'
theorem the angle between the 6 m and 8 m sides is $90°$.

$$\text{Area}=\frac12\times6\times8=24\ \text{m}^2$$

Taking 10 m as the base: $\frac12\times10\times h=24$, so $h=4.8$ m.

**Answer.** 24 m²; height on the longest side 4.8 m.
:::

### 8.1.1 Equilateral and isosceles triangles

::: derivation Area of an equilateral triangle of side $a$
In equilateral $\triangle ABC$ draw $AD\perp BC$. AD bisects BC, so
$BD=DC=\frac a2$.

**Step 1 — Pythagoras in $\triangle ADC$.**
$AD^2=AC^2-DC^2=a^2-\frac{a^2}{4}=\frac{3a^2}{4}$

**Step 2 — take the square root.** $AD=\frac{\sqrt{3}}{2}a$

**Step 3 — use $\frac12bh$.**
Area $=\frac12\times a\times\frac{\sqrt{3}}{2}a$

**Result.**

$$\text{Area of equilateral triangle}=\frac{\sqrt{3}}{4}a^2$$
:::

::: derivation Area of an isosceles triangle (equal sides $a$, base $b$)
Draw $AD\perp BC$; it bisects the base, so $DC=\frac b2$.

$AD^2=a^2-\frac{b^2}{4}=\frac{4a^2-b^2}{4}$, so
$AD=\frac{\sqrt{4a^2-b^2}}{2}$.

Area $=\frac12\times b\times\frac{\sqrt{4a^2-b^2}}{2}$, which gives

$$\text{Area of isosceles triangle}=\frac{b}{4}\sqrt{4a^2-b^2}$$
:::

::: example Equilateral and isosceles triangles
**Problem.** Find the area of (a) an equilateral triangle of side 6 cm,
(b) an isosceles triangle with equal sides 13 cm and base 10 cm.

**Solution.**
(a) Area $=\frac{\sqrt{3}}{4}\times6^2=\frac{\sqrt{3}}{4}\times36=9\sqrt{3}\approx15.59$ cm².

(b) Area $=\frac{10}{4}\sqrt{4\times13^2-10^2}=\frac{10}{4}\sqrt{676-100}$

$=\frac{10}{4}\sqrt{576}=\frac{10}{4}\times24=60$ cm².

**Check (b).** Height $=\sqrt{13^2-5^2}=12$ cm, and $\frac12\times10\times12=60$ ✓.
:::

::: caution The height is not a side
In a triangle with sides 5 m, 4 m and 3 m, the area is **not**
$\frac12\times5\times4$. The 4 m side is not perpendicular to the 5 m side.
Draw the triangle, identify the right angle, and use the two sides that form it:
here 4 and 3 give $\frac12\times4\times3=6$ m². Substituting a sloping side for
the height is the classic mensuration error.
:::

## 8.2 Area of quadrilaterals

| Shape | Diagram | Area |
|---|---|---|
| Rectangle | length $l$, breadth $b$ | $l\times b$ |
| Square | side $a$ | $a^2$ |
| Parallelogram | base $b$, height $h$ | $b\times h$ |
| Rhombus | diagonals $d_1$, $d_2$ | $\frac12 d_1 d_2$ |
| Trapezium | parallel sides $a$, $b$, height $h$ | $\frac12(a+b)h$ |
| Kite | diagonals $d_1$, $d_2$ | $\frac12 d_1 d_2$ |

```figure caption="Base b and perpendicular height h in three shapes. The height is always measured at right angles to the base, never along a slanting side."
fig, ax = plt.subplots(figsize=(5.2, 2.4))
def shape(xs, ys, c):
    ax.plot(xs + [xs[0]], ys + [ys[0]], color=c, lw=1.6)
# triangle
shape([0, 3, 1.9], [0, 0, 2.2], ACCENT)
ax.plot([1.9, 1.9], [0, 2.2], color=MUTED, ls="--", lw=0.9)
ax.text(2.0, 0.9, "h", fontsize=9, color=INK)
ax.text(1.5, -0.45, "b", fontsize=9, ha="center", color=INK)
ax.text(1.5, -1.05, "triangle: ½bh", fontsize=9, ha="center", color=ACCENT)
# parallelogram
shape([3.8, 6.6, 7.6, 4.8], [0, 0, 2.2, 2.2], SERIES[1])
ax.plot([4.8, 4.8], [0, 2.2], color=MUTED, ls="--", lw=0.9)
ax.text(4.9, 0.9, "h", fontsize=9, color=INK)
ax.text(5.2, -0.45, "b", fontsize=9, ha="center", color=INK)
ax.text(5.6, -1.05, "parallelogram: bh", fontsize=9, ha="center", color=SERIES[1])
# trapezium
shape([8.4, 11.8, 11.0, 9.2], [0, 0, 2.2, 2.2], SERIES[2])
ax.plot([9.2, 9.2], [0, 2.2], color=MUTED, ls="--", lw=0.9)
ax.text(9.3, 0.9, "h", fontsize=9, color=INK)
ax.text(10.1, -0.45, "b", fontsize=9, ha="center", color=INK)
ax.text(10.1, 2.4, "a", fontsize=9, ha="center", color=INK)
ax.text(10.1, -1.05, "trapezium: ½(a+b)h", fontsize=9, ha="center", color=SERIES[2])
ax.set_xlim(-0.3, 12.1); ax.set_ylim(-1.4, 2.8); ax.set_aspect("equal"); ax.axis("off")
```

::: example A trapezium and a rhombus
**Problem.** (a) A trapezium has parallel sides 12 m and 8 m and a distance of
5 m between them. Find its area. (b) A rhombus has diagonals 16 cm and 12 cm.
Find its area and the length of one side.

**Solution.** (a)

$$\text{Area}=\frac12(a+b)h=\frac12(12+8)\times5
=\frac12\times20\times5=50\ \text{m}^2$$

(b)

$$\text{Area}=\frac12 d_1d_2=\frac12\times16\times12=96\ \text{cm}^2$$

The diagonals of a rhombus bisect each other at right angles, so each side is
the hypotenuse of a right triangle with legs 8 cm and 6 cm:

$$\text{side}=\sqrt{8^2+6^2}=\sqrt{100}=10\ \text{cm}$$

**Answer.** (a) 50 m². (b) area 96 cm², side 10 cm.

**Check.** (b) The four sides are equal at 10 cm, so the perimeter is 40 cm; and
$\frac12\times16\times12=96$ ✓.
:::

### 8.2.1 Any quadrilateral: a diagonal and two heights

A diagonal $d$ cuts any quadrilateral into two triangles. If the
perpendiculars from the other two vertices to the diagonal are $h_1$ and $h_2$,

$$\text{Area}=\frac12dh_1+\frac12dh_2=\frac12d(h_1+h_2)$$

The rhombus formula $\frac12d_1d_2$ is the special case where $h_1+h_2=d_2$.

::: example Quadrilateral and parallelogram
**Problem.** (a) In quadrilateral PQRS the diagonal PR $=12$ cm, and the
perpendiculars from Q and S to PR are 5 cm and 4 cm. Find its area.
(b) A parallelogram has area 120 cm² and base 15 cm. Find its height.

**Solution.**
(a) Area $=\frac12\times12\times(5+4)=6\times9=54$ cm².

(b) $b\times h=120$, so $15h=120$ and $h=8$ cm.
:::

::: example Area excluding a part
**Problem.** A rectangular park 120 m × 110 m contains a volleyball court
18 m × 9 m. Find the area of the park excluding the court.

**Solution.** Park $=120\times110=13\,200$ m². Court $=18\times9=162$ m².
Remaining area $=13\,200-162=13\,038$ m².
:::

## 8.3 Area and circumference of a circle

For a circle of radius $r$:

$$\text{Circumference}=2\pi r=\pi d,\qquad \text{Area}=\pi r^2$$

Take $\pi=\frac{22}{7}$ unless a question says otherwise.

| Part | Meaning | Formula |
|---|---|---|
| Diameter | the chord through the centre | $d=2r$ |
| Sector | the region between two radii and an arc | area $=\frac{\theta}{360°}\times\pi r^2$ |
| Arc | the curved length of a sector | length $=\frac{\theta}{360°}\times2\pi r$ |
| Semicircle | half the circle | area $=\frac12\pi r^2$ |

::: derivation Why the area of a circle is $\pi r^2$
Cut a circle of radius $r$ into many equal sectors (16, 32, …) and arrange them
head-to-tail. They form a shape that is almost a parallelogram (a rectangle,
if the pieces are very thin).

- Its height is the radius, $r$.
- Its base is half the circumference: $\frac12\times2\pi r=\pi r$.

So area $=$ base $\times$ height $=\pi r\times r=\pi r^2$. Since $r=\frac d2$,
area $=\frac{\pi d^2}{4}$ as well.
:::

::: example Radius from the area
**Problem.** The area of a circle is 5544 cm². Find its radius
($\pi=\frac{22}{7}$).

**Solution.** $\frac{22}{7}r^2=5544$, so $r^2=\frac{5544\times7}{22}=1764$ and
$r=\sqrt{1764}=42$ cm.
:::

::: example Shaded region — square and quarter circles
**Problem.** ABCD is a square of side 14 cm. At each corner a quarter circle of
radius 7 cm is cut out. Find the area of the remaining (shaded) part
($\pi=\frac{22}{7}$).

**Solution.** Square $=14\times14=196$ cm².
Four quarter circles of radius 7 cm make one full circle:
$\frac{22}{7}\times7\times7=154$ cm².
Shaded area $=196-154=42$ cm².
:::

```figure caption="Square of side 14 cm with a quarter circle of radius 7 cm at each corner. The four quarters together make one circle of area 154 cm², so the shaded part is 196 − 154 = 42 cm²."
from matplotlib.patches import Rectangle, Wedge
fig, ax = plt.subplots(figsize=(4.2, 3.0))
ax.add_patch(Rectangle((0, 0), 14, 14, fc=ACCENT, alpha=0.30, ec=INK, lw=1.2))
for (cx, cy, t1) in [(0, 0, 0), (14, 0, 90), (14, 14, 180), (0, 14, 270)]:
    ax.add_patch(Wedge((cx, cy), 7, t1, t1 + 90, fc="white", ec=INK, lw=1.0))
for (x, y, t) in [(-1.0, -1.0, "A"), (14.3, -1.0, "B"), (14.3, 14.3, "C"), (-1.0, 14.3, "D")]:
    ax.text(x, y, t, fontsize=10, color=INK)
ax.text(7, -1.8, "14 cm", ha="center", fontsize=9, color=INK)
ax.plot([0, 4.95], [0, 4.95], color=SERIES[1], lw=1.0)
ax.text(3.2, 1.6, "7 cm", fontsize=8.5, color=SERIES[1])
ax.text(7, 7, "shaded", ha="center", va="center", fontsize=9, color=INK)
ax.set_xlim(-2, 16); ax.set_ylim(-2.6, 15.6); ax.set_aspect("equal"); ax.axis("off")
```

::: example A circle and a sector
**Problem.** A circle has radius 7 cm. Find its circumference and area. Then
find the area of a sector of the same circle that subtends 90° at the centre.

**Solution.** Circumference $=2\times\frac{22}{7}\times7=44$ cm.

$$\text{Area}=\frac{22}{7}\times7^2=154\ \text{cm}^2$$

Sector:

$$\text{Area}=\frac{90}{360}\times154=\frac14\times154=38.5\ \text{cm}^2$$

**Answer.** 44 cm; 154 cm²; the quarter sector is 38.5 cm².

**Check.** The sector is a quarter of the circle, and
$\frac{154}{4}=38.5$ ✓.
:::

::: example A circular path
**Problem.** A circular garden of radius 14 m has a path 1 m wide all round it,
outside the garden. Find the area of the path.

**Solution.** The path is the ring between two circles: the inner radius is
14 m and the outer radius is $14+1=15$ m.

$$\text{Area}=\pi(15^2-14^2)=\frac{22}{7}(225-196)=\frac{22}{7}\times29
\approx91.14\ \text{m}^2$$

**Answer.** About 91.14 m².

**Check.** The whole outer circle is $\frac{22}{7}\times225=707.14$ m² and the
garden is $\frac{22}{7}\times196=616$ m²; the difference is 91.14 m² ✓. Always
subtract the two circles rather than multiplying the circumference by the width,
which would overestimate.
:::

## 8.4 Surface area and volume of a cylinder

A **cylinder** has two circular ends and one curved surface. Think of a tin of
ghee or a water tank.

| Quantity | Formula |
|---|---|
| Curved (lateral) surface area | $2\pi rh$ |
| Total surface area | $2\pi r(r+h)$ |
| Volume | $\pi r^2h$ |

where $r$ is the radius of the base and $h$ the height. The volume of any prism
is $\text{area of base}\times\text{height}$, which is where $\pi r^2h$ comes
from: the base is a circle.

```figure caption="Unrolling a cylinder. The curved surface flattens into a rectangle whose width is the circumference of the base, 2πr, and whose height is h."
fig, ax = plt.subplots(figsize=(5.0, 2.5))
ax.set_xlim(0, 10)
ax.set_ylim(0, 5.2)
ax.axis("off")
ax.add_patch(Ellipse((1.6, 3.9), 2.6, 0.7, fill=False, ec=INK, lw=1.2))
ax.add_patch(Ellipse((1.6, 1.1), 2.6, 0.7, fill=False, ec=INK, lw=1.2))
ax.plot([0.3, 0.3], [1.1, 3.9], color=INK, lw=1.2)
ax.plot([2.9, 2.9], [1.1, 3.9], color=INK, lw=1.2)
ax.annotate("", xy=(0.05, 3.9), xytext=(0.05, 1.1),
            arrowprops=dict(arrowstyle="<->", color=ACCENT, lw=1.0))
ax.text(0.0, 2.5, "h", ha="right", va="center", fontsize=7.5, color=ACCENT)
ax.text(1.6, 0.35, "base radius r", ha="center", fontsize=6.4, color=MUTED)
ax.annotate("", xy=(4.0, 2.5), xytext=(3.3, 2.5),
            arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.1))
ax.add_patch(plt.Rectangle((4.4, 1.1), 5.2, 2.8, fill=False, ec=SERIES[1], lw=1.3))
ax.annotate("", xy=(4.4, 0.7), xytext=(9.6, 0.7),
            arrowprops=dict(arrowstyle="<->", color=SERIES[1], lw=1.0))
ax.text(7.0, 0.3, "2πr (the circumference)", ha="center", fontsize=6.6,
        color=SERIES[1])
ax.text(9.75, 2.5, "h", ha="left", va="center", fontsize=7.5, color=SERIES[1])
ax.text(7.0, 4.35, "curved area = 2πrh", ha="center", fontsize=7.0, color=INK)
fig.tight_layout()
```

::: example A water tank
**Problem.** A cylindrical water tank has a radius of 70 cm and a height of
1.5 m. Find its volume in litres and the area of sheet metal needed to make it
(with a closed top).

**Solution.** Keep the units consistent: $r=70$ cm $=0.7$ m, $h=1.5$ m.

$$\text{Volume}=\pi r^2h=\frac{22}{7}\times0.7^2\times1.5
=\frac{22}{7}\times0.49\times1.5=2.31\ \text{m}^3$$

Since 1 m³ $=1000$ litres, the volume is **2,310 litres**.

$$\text{Total surface area}=2\pi r(r+h)=\frac{44}{7}\times0.7\times(0.7+1.5)
=4.4\times2.2=9.68\ \text{m}^2$$

**Answer.** 2,310 litres; about 9.68 m² of sheet.

**Check.** The base area is $1.54$ m² and the height is 1.5 m, so
$1.54\times1.5=2.31$ m³ ✓.
:::

::: caution Square units and cubic units
An area is in m² and a volume in m³. Multiplying a length by an area gives a
volume; adding a length to an area is meaningless and always wrong. Before
substituting, write every length in the **same** unit — mixing centimetres with
metres is the second commonest error in mensuration.
:::

## 8.5 Choosing the right formula

Most lost marks in mensuration come from reaching for the wrong formula, not
from arithmetic. Decide three things first: **flat or solid**, **which
shape**, **which quantity**.

```figure caption="A decision path for mensuration questions. Answer the three questions in order and the formula is fixed before any number is written."
fig, ax = flow([("Flat or solid?", "area or volume"),
                ("Which shape?", "rectangle, circle, cuboid, cylinder"),
                ("Which quantity?", "perimeter, area, surface, volume"),
                ("Units?", "cm², m³, litres")],
               note="1 m³ = 1000 litres; 1 m² = 10,000 cm²")
```

| Shape | Perimeter / circumference | Area | Volume | Surface area |
|---|---|---|---|---|
| Rectangle | $2(l+b)$ | $lb$ | — | — |
| Square | $4l$ | $l^2$ | — | — |
| Triangle | sum of sides | $\frac{1}{2}bh$ | — | — |
| Circle | $2\pi r$ | $\pi r^2$ | — | — |
| Cuboid | — | — | $lbh$ | $2(lb+bh+lh)$ |
| Cube | — | — | $l^3$ | $6l^2$ |
| Cylinder | — | — | $\pi r^2h$ | curved $2\pi rh$; total $2\pi r(r+h)$ |

::: example Walls, floor and cost in one question
**Question.** A hall is 12 m long, 9 m wide and 4 m high. It has two doors of
2 m × 1.2 m and four windows of 1.5 m × 1 m. Find (i) the area of the four
walls to be painted (ii) the cost of painting at Rs 95 per m².

**Answer.**
(i) Four walls $= 2h(l+b) = 2 \times 4 \times (12+9) = 168$ m².
Openings $= 2(2 \times 1.2) + 4(1.5 \times 1) = 4.8 + 6 = 10.8$ m².
Area to paint $= 168 - 10.8 = \textbf{157.2 m}^2$.
(ii) Cost $= 157.2 \times 95 = \textbf{Rs 14,934}$.
:::

::: example From volume to litres
**Question.** A cylindrical tank of diameter 1.4 m and height 1.5 m is filled
to three-quarters of its height. How many litres does it hold? Take
$\pi = \frac{22}{7}$.

**Answer.** $r = 0.7$ m; filled height $= \frac{3}{4} \times 1.5 = 1.125$ m.
$V = \pi r^2 h = \frac{22}{7} \times 0.49 \times 1.125 = 1.7325$ m³.
$1$ m³ $= 1000$ litres, so the tank holds **1,732.5 litres**.
:::

::: note Activity — measure your classroom
In groups, measure the length, breadth and height of your classroom, and the
size of every door and window. Work out (a) the floor area, (b) the area of
the four walls less the openings, (c) the volume of air in the room. Then find
the cost of painting the walls at the local rate, and compare the groups'
answers — differences will come from measurement, not from the formula.
:::

## Chapter summary

- Triangle: $\frac12 bh$; equilateral $\frac{\sqrt{3}}{4}a^2$; isosceles
  $\frac b4\sqrt{4a^2-b^2}$.
- Any quadrilateral with diagonal $d$ and offsets $h_1,h_2$: $\frac12d(h_1+h_2)$.
- Shaded area $=$ whole figure $-$ unshaded part.
- Rectangle $lb$; square $a^2$; parallelogram $bh$; rhombus and kite
  $\frac12 d_1d_2$; trapezium $\frac12(a+b)h$.
- Circle: circumference $2\pi r$, area $\pi r^2$; sector area
  $\frac{\theta}{360°}\pi r^2$; arc length $\frac{\theta}{360°}2\pi r$.
- Cylinder: curved surface $2\pi rh$, total surface $2\pi r(r+h)$, volume
  $\pi r^2h$.
- A ring or path is the difference of two circles, not a circumference times a
  width.
- Areas are in square units and volumes in cubic units, and all lengths must be
  in the same unit.

## Practice questions

**Group A — Objective (1 mark each)**

1. The area of a triangle with base 12 cm and height 5 cm is
   <span class="marks">[1]</span>
   (a) 17 cm² (b) 30 cm² (c) 60 cm² (d) 34 cm²
2. The area of a rhombus with diagonals 8 cm and 6 cm is
   <span class="marks">[1]</span>
   (a) 24 cm² (b) 48 cm² (c) 14 cm² (d) 12 cm²
3. The area of a trapezium with parallel sides 10 m and 6 m and height 4 m is
   <span class="marks">[1]</span>
   (a) 32 m² (b) 64 m² (c) 240 m² (d) 40 m²
4. The circumference of a circle of radius 7 cm is
   <span class="marks">[1]</span>
   (a) 22 cm (b) 44 cm (c) 154 cm (d) 49 cm
5. The volume of a cylinder of radius 3 cm and height 10 cm is
   (take $\pi=3.14$) <span class="marks">[1]</span>
   (a) 282.6 cm³ (b) 94.2 cm³ (c) 30 cm³ (d) 188.4 cm³
6. 1 m³ in litres is <span class="marks">[1]</span>
   (a) 10 (b) 100 (c) 1000 (d) 10000

::: note Answers to Group A
**1.** (b) — $\frac12\times12\times5=30$.
**2.** (a) — $\frac12\times8\times6=24$.
**3.** (a) — $\frac12(10+6)\times4=32$.
**4.** (b) — $2\times\frac{22}{7}\times7=44$.
**5.** (a) — $3.14\times9\times10=282.6$.
**6.** (c) — one cubic metre is 1000 litres.
:::

**Group B — Short answer (2 marks each)**

1. Find the area of a triangle whose base is 16 m and height 9 m.
   <span class="marks">[2]</span>
2. Find the area of a circle of diameter 28 cm.
   <span class="marks">[2]</span>
3. Find the curved surface area and the volume of a cylinder of radius 7 cm and
   height 10 cm. <span class="marks">[2]</span>
4. A trapezium has area 84 cm² and parallel sides 10 cm and 14 cm. Find the
   distance between them. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** $\frac12\times16\times9=72$ m².
**2.** $r=14$ cm, so area $=\frac{22}{7}\times196=616$ cm².
**3.** Curved surface $=2\times\frac{22}{7}\times7\times10=440$ cm²; volume
$=\frac{22}{7}\times49\times10=1540$ cm³.
**4.** $\frac12(10+14)h=84$, so $12h=84$ and $h=7$ cm.
:::

**Group C — Long answer (4 marks each)**

1. A rectangular field is 60 m long and 40 m wide. A circular pond of radius 7 m
   is dug inside it. Find the area of the field that remains, and the length of
   fencing needed around the whole field. <span class="marks">[4]</span>
2. A cylindrical tank of radius 1.4 m and height 2 m is full of water. Find its
   volume in litres. If water is drawn off at 20 litres a minute, how long will
   the tank take to empty? <span class="marks">[4]</span>

::: note Answers to Group C
**1.** **Area of the field.** $60\times40=2400$ m². **Area of the pond.**
$\frac{22}{7}\times7^2=154$ m². **Remaining area.** $2400-154=2246$ m².
**Fencing.** The fence runs round the rectangle, so its length is the perimeter:
$2(60+40)=200$ m.
**Check.** The pond takes up 154 m² out of 2400 m², about 6.4 %, so the remaining
area must be a little under 2400 ✓.
**2.** **Volume.** $\pi r^2h=\frac{22}{7}\times1.4^2\times2
=\frac{22}{7}\times1.96\times2=12.32$ m³. Since 1 m³ $=1000$ litres, the tank
holds **12,320 litres**. **Time.** At 20 litres a minute,
$\frac{12\,320}{20}=616$ minutes, that is **10 hours 16 minutes**.
**Check.** 616 minutes is about 10.3 hours; at 20 litres a minute the tank loses
1200 litres an hour, and $12\,320\div1200=10.27$ hours ✓.
:::

**Extra practice**

**Group B (2 marks)**

**14.** Find the total surface area of a cuboid 8 cm × 5 cm × 3 cm.
**15.** The circumference of a circle is 88 cm. Find its radius
    ($\pi = \frac{22}{7}$).

**Group C (4 marks)**

**16.** A room 6 m × 5 m × 3.5 m is to be carpeted on the floor at Rs 450 per m²
    and painted on the four walls at Rs 110 per m², with one door
    2 m × 1 m. Find the total cost.

::: note Extra practice — answers
**14.** $2(lb + bh + lh) = 2(40 + 15 + 24) = 158$ cm².
**15.** $2\pi r = 88 \Rightarrow r = \frac{88 \times 7}{2 \times 22} = 14$ cm.
**16.** Floor $= 30$ m²; carpet $= 30 \times 450 = $ Rs 13,500.
Walls $= 2 \times 3.5 \times (6+5) = 77$ m²; less the door $2$ m² gives
75 m²; paint $= 75 \times 110 = $ Rs 8,250.
**Total $=$ Rs 21,750.**
:::

## Objective practice

**Choose the correct answer.** <span class="marks">[5×1=5]</span>

**1.** The area of a circle of radius 7 cm ($\pi=\frac{22}{7}$) is
   (a) 44 cm² (b) 154 cm² (c) 49 cm² (d) 22 cm²
**2.** The volume of a cuboid 5 cm × 4 cm × 3 cm is
   (a) 12 cm³ (b) 60 cm³ (c) 94 cm³ (d) 47 cm³
**3.** 1 m³ equals
   (a) 100 litres (b) 1000 litres (c) 10 litres (d) 10,000 litres
**4.** The area of the four walls of a room is
   (a) $lb$ (b) $2h(l+b)$ (c) $2(lb+bh+lh)$ (d) $lbh$
**5.** If the radius of a circle is doubled, its area becomes
   (a) double (b) three times (c) four times (d) unchanged

::: note Objective practice — answers
**1.** (b) — $\frac{22}{7}\times49=154$ cm². **2.** (b) — $5\times4\times3=60$ cm³. **3.** (b) — 1000 litres. **4.** (b) — $2h(l+b)$. **5.** (c) — area varies as the square of the radius.
:::
