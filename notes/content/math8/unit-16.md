---
subject: Mathematics
grade: 8
unit: 16
title: Solid Objects
hours: 0
area: Compulsory Mathematics
---

A box, a milk carton, a pyramid-shaped temple roof: all are solids with flat
faces, and every one of them can be cut out of a sheet of paper using a **net**.
This chapter counts faces, edges and vertices, unfolds the solids into nets, and
then does the arithmetic that matters in a workshop — how much material is
needed to make the box, and how much it holds.

::: key What this chapter asks of you
You should be able to count and name the faces, edges and vertices of a prism
and a pyramid, draw a net of a cube, a cuboid and a triangular prism, find the
surface area of a cuboid, a cube and a triangular prism, and find the volume of
a prism and a pyramid.
:::

## 16.1 Prisms and pyramids

A **prism** has two identical parallel ends (its bases) joined by rectangular
side faces. A **pyramid** has one base and triangular side faces that meet at a
single point, the apex.

| Solid | Faces | Edges | Vertices |
|---|---|---|---|
| Cube (square prism with all edges equal) | 6 squares | 12 | 8 |
| Cuboid (rectangular prism) | 6 rectangles | 12 | 8 |
| Triangular prism | 5 (2 triangles, 3 rectangles) | 9 | 6 |
| Hexagonal prism | 8 (2 hexagons, 6 rectangles) | 18 | 12 |
| Square pyramid | 5 (1 square, 4 triangles) | 8 | 5 |
| Triangular pyramid (tetrahedron) | 4 triangles | 6 | 4 |

For any such solid, the counts obey **Euler's relation**:

$$F+V-E=2$$

Check it on the cube: $6+8-12=2$ ✓. On the square pyramid:
$5+5-8=2$ ✓.

```figure caption="A prism and a pyramid drawn side by side. In a prism the two ends are the same shape and the sides are rectangles; in a pyramid the sides are triangles meeting at one apex."
fig, ax = plt.subplots(figsize=(5.0, 2.6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 5.2)
ax.axis("off")
# triangular prism
ax.add_patch(plt.Polygon([(0.6, 0.8), (2.6, 0.8), (1.6, 2.4)], fill=False, ec=ACCENT, lw=1.3))
ax.add_patch(plt.Polygon([(1.6, 2.8), (3.6, 2.8), (2.6, 4.4)], fill=False, ec=ACCENT, lw=1.3))
for a, b in [((0.6, 0.8), (1.6, 2.8)), ((2.6, 0.8), (3.6, 2.8)), ((1.6, 2.4), (2.6, 4.4))]:
    ax.plot([a[0], b[0]], [a[1], b[1]], color=ACCENT, lw=1.3)
ax.text(2.1, 0.25, "triangular prism", ha="center", fontsize=6.8, color=ACCENT)
ax.text(4.6, 3.6, "faces 5\\nedges 9\\nvertices 6", ha="left", fontsize=6.0, color=MUTED)
# square pyramid
ax.add_patch(plt.Polygon([(6.0, 0.8), (9.0, 0.8), (9.8, 2.0), (6.8, 2.0)], fill=False,
                         ec=SERIES[1], lw=1.3))
ax.plot([6.0, 7.9], [0.8, 3.9], color=SERIES[1], lw=1.3)
ax.plot([9.0, 7.9], [0.8, 3.9], color=SERIES[1], lw=1.3)
ax.plot([9.8, 7.9], [2.0, 3.9], color=SERIES[1], lw=1.3)
ax.plot([6.8, 7.9], [2.0, 3.9], color=SERIES[1], lw=1.3)
ax.plot([7.9], [3.9], "o", color=INK, ms=3.5)
ax.text(7.9, 4.35, "apex", ha="center", fontsize=6.2, color=INK)
ax.text(7.9, 0.25, "square pyramid", ha="center", fontsize=6.8, color=SERIES[1])
ax.text(5.0, 5.0, "F + V - E = 2 for every one of them", ha="center", fontsize=6.6,
        color=MUTED)
fig.tight_layout()
```

::: example Counting on a prism
**Problem.** A prism has a base that is a regular octagon. How many faces, edges
and vertices does it have? Check with Euler's relation.

**Solution.** The two ends are octagons, and there is one rectangular face for
each of the eight sides. So

$$F=2+8=10$$

Each of the 8 base edges appears at each end, so there are 16 base edges, plus
the 8 side edges:

$$E=16+8=24$$

There are 8 vertices at each end:

$$V=16$$

**Check.** $F+V-E=10+16-24=2$ ✓.
:::

## 16.2 Nets

A **net** is a flat shape that folds up into a solid. Cutting a net out of card
and folding it is the quickest way to be sure you have the right one.

| Solid | Net |
|---|---|
| Cube | six squares in a cross; there are eleven different nets of a cube |
| Cuboid | six rectangles: two of each of the three sizes |
| Triangular prism | two triangles and three rectangles in a row |
| Square pyramid | one square with a triangle attached to each side |
| Cylinder | two circles and one rectangle whose width is the circumference |

```figure caption="A net of a cuboid. The four side rectangles stand in a row, and the two end rectangles attach top and bottom; folding on the dotted lines gives the box."
fig, ax = plt.subplots(figsize=(5.0, 2.6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 5.2)
ax.axis("off")
w, h, d = 1.5, 1.1, 0.9
x0, y0 = 2.0, 1.6
for i in range(4):
    ax.add_patch(plt.Rectangle((x0 + i * w, y0), w, h, fill=False, ec=ACCENT, lw=1.2))
ax.add_patch(plt.Rectangle((x0 + w, y0 + h), w, d, fill=False, ec=SERIES[1], lw=1.2))
ax.add_patch(plt.Rectangle((x0 + w, y0 - d), w, d, fill=False, ec=SERIES[1], lw=1.2))
ax.text(x0 + 2 * w, y0 + h + d + 0.25, "top", ha="center", fontsize=6.4, color=SERIES[1])
ax.text(x0 + 2 * w, y0 - d - 0.4, "bottom", ha="center", fontsize=6.4, color=SERIES[1])
ax.text(x0 + 2 * w, y0 + 0.45, "four side faces", ha="center", fontsize=6.6, color=ACCENT)
ax.text(5.0, 4.75, "fold on the dotted edges to make the box", ha="center",
        fontsize=6.5, color=MUTED)
fig.tight_layout()
```

::: caution A net must have exactly the right number of faces
Six squares will not make a cube unless they are joined in one of the eleven
correct arrangements. Two squares that overlap when folded, or a gap that cannot
close, both give a wrong net. Count the faces first (a cube needs 6, a cuboid 6,
a triangular prism 5), then check that the joins can actually fold.
:::

## 16.3 Surface area

The **surface area** is the total area of every face, and it is what you need to
know to buy paint, cloth or cardboard.

| Solid | Surface area |
|---|---|
| Cube of side $a$ | $6a^2$ |
| Cuboid $l\times b\times h$ | $2(lb+bh+hl)$ |
| Triangular prism (base triangle $b$, height $h_t$, length $L$) | $2\times\frac12 b h_t+(\text{perimeter of base})\times L$ |
| Square pyramid (base side $a$, slant height $l$) | $a^2+2al$ |
| Cylinder | $2\pi r(r+h)$ |

```figure caption="A cuboid opened out. The total surface area is the sum of the six rectangles: two of each of lb, bh and hl."
fig, ax = plt.subplots(figsize=(5.0, 2.5))
ax.set_xlim(0, 10)
ax.set_ylim(0, 5.0)
ax.axis("off")
ax.add_patch(plt.Rectangle((1.0, 1.2), 3.2, 2.0, fill=False, ec=ACCENT, lw=1.2))
ax.text(2.6, 2.2, "$l\\times b$", ha="center", va="center", fontsize=7.0, color=ACCENT)
ax.add_patch(plt.Rectangle((4.4, 1.2), 1.7, 2.0, fill=False, ec=SERIES[1], lw=1.2))
ax.text(5.25, 2.2, "$b\\times h$", ha="center", va="center", fontsize=6.6, color=SERIES[1])
ax.add_patch(plt.Rectangle((6.3, 1.2), 3.2, 2.0, fill=False, ec=ACCENT, lw=1.2))
ax.text(7.9, 2.2, "$l\\times b$", ha="center", va="center", fontsize=7.0, color=ACCENT)
ax.add_patch(plt.Rectangle((1.0, 3.4), 3.2, 1.0, fill=False, ec=SERIES[2], lw=1.2))
ax.text(2.6, 3.9, "$h\\times l$", ha="center", va="center", fontsize=6.6, color=SERIES[2])
ax.add_patch(plt.Rectangle((6.3, 3.4), 3.2, 1.0, fill=False, ec=SERIES[2], lw=1.2))
ax.text(7.9, 3.9, "$h\\times l$", ha="center", va="center", fontsize=6.6, color=SERIES[2])
ax.text(5.0, 0.5, "total = 2(lb + bh + hl)", ha="center", fontsize=7.4, color=INK)
fig.tight_layout()
```

::: example A cuboid box
**Problem.** A closed box measures 20 cm by 15 cm by 10 cm. Find its total
surface area and its volume.

**Solution.** Take $l=20$, $b=15$ and $h=10$ cm.

$$S=2(lb+bh+hl)=2(300+150+200)=2\times650=1300\ \text{cm}^2$$

$$V=lbh=20\times15\times10=3000\ \text{cm}^3$$

**Answer.** 1300 cm² of card; volume 3000 cm³.

**Check.** The six faces are two of 300 cm², two of 150 cm² and two of 200 cm²,
giving $600+300+400=1300$ ✓. The volume is the base area $300\times$ the height
$10=3000$ ✓.
:::

::: example A cube painted on the outside
**Problem.** A cube of side 12 cm is painted all over. Find the area painted, and
the volume.

**Solution.** $S=6a^2=6\times144=864$ cm².

$$V=a^3=12^3=1728\ \text{cm}^3$$

**Answer.** 864 cm²; 1728 cm³.

**Check.** Each face is $12\times12=144$ cm², and six of them give 864 ✓.
:::

## 16.4 Volume of a prism and a pyramid

$$\text{Volume of a prism}=\text{area of base}\times\text{height}$$

$$\text{Volume of a pyramid}=\frac13\times\text{area of base}\times\text{height}$$

The factor $\frac13$ is not a mystery: three pyramids of the same base and height
fill exactly one prism. A cube can be cut into three congruent square pyramids
with the same apex.

| Solid | Volume |
|---|---|
| Cube of side $a$ | $a^3$ |
| Cuboid $l\times b\times h$ | $lbh$ |
| Triangular prism (base $b$, triangle height $h_t$, length $L$) | $\frac12bh_t\times L$ |
| Square pyramid (base side $a$, height $h$) | $\frac13a^2h$ |
| Cylinder | $\pi r^2h$ |

::: example A triangular prism
**Problem.** A triangular prism has a base that is a right-angled triangle with
legs 6 cm and 8 cm, and a length of 15 cm. Find its volume and its total surface
area.

**Solution.** **Volume.** Area of the triangular base
$=\frac12\times6\times8=24$ cm², so

$$V=24\times15=360\ \text{cm}^3$$

**Surface area.** Two triangular ends: $2\times24=48$ cm². The hypotenuse is
$\sqrt{6^2+8^2}=10$ cm, so the perimeter of the base is $6+8+10=24$ cm and the
three rectangular faces total $24\times15=360$ cm².

$$S=48+360=408\ \text{cm}^2$$

**Answer.** Volume 360 cm³; surface area 408 cm².

**Check.** The two triangular ends are 48 of the 408; the three rectangles are
$6\times15=90$, $8\times15=120$ and $10\times15=150$, which add to 360 ✓.
:::

::: example A pyramid
**Problem.** A square pyramid has a base of side 10 m and a height of 12 m. Find
its volume.

**Solution.**

$$V=\frac13\times a^2\times h=\frac13\times100\times12=400\ \text{m}^3$$

**Answer.** 400 m³.

**Check.** The enclosing prism would have volume $100\times12=1200$ m³, and a
third of it is 400 ✓.
:::

::: caution Area, surface area and volume are three different things
The **area** of the triangular base is 24 cm². The **surface area** of the whole
prism is 408 cm². The **volume** is 360 cm³. Substituting a base area where a
surface area is wanted, or forgetting to multiply by the length, are the two
commonest errors here. Label each quantity with its unit as you work — cm² and
cm³ look different, and that is the point.
:::

## Chapter summary

- A prism has two identical parallel ends and rectangular sides; a pyramid has
  one base and triangular sides meeting at an apex.
- $F+V-E=2$ for every such solid.
- A net is a flat pattern that folds into the solid; a cube has eleven nets.
- Cube surface area $6a^2$, volume $a^3$; cuboid surface area
  $2(lb+bh+hl)$, volume $lbh$.
- Volume of a prism $=$ base area $\times$ length; volume of a pyramid
  $=\frac13\times$ base area $\times$ height.
- Surface area is in square units, volume in cubic units, and the two are never
  interchangeable.

## Practice questions

**Group A — Objective (1 mark each)**

1. The number of faces of a cuboid is <span class="marks">[1]</span>
   (a) 4 (b) 6 (c) 8 (d) 12
2. The number of vertices of a square pyramid is
   <span class="marks">[1]</span>
   (a) 4 (b) 5 (c) 6 (d) 8
3. Volume of a cuboid $5\times4\times3$ cm is <span class="marks">[1]</span>
   (a) 12 cm³ (b) 47 cm³ (c) 60 cm³ (d) 94 cm³
4. Total surface area of a cube of side 5 cm is
   <span class="marks">[1]</span>
   (a) 25 cm² (b) 125 cm² (c) 150 cm² (d) 30 cm²
5. The volume of a pyramid is that of a prism with the same base and height
   <span class="marks">[1]</span>
   (a) the same as (b) one half of (c) one third of (d) twice
6. In a triangular prism, the shape of the side faces is
   <span class="marks">[1]</span>
   (a) triangle (b) rectangle (c) square (d) circle

::: note Answers to Group A
**1.** (b) — six rectangular faces.
**2.** (b) — four at the base plus the apex.
**3.** (c) — $5\times4\times3=60$.
**4.** (c) — $6\times25=150$.
**5.** (c) — one third.
**6.** (b) — rectangles joining the two triangular ends.
:::

**Group B — Short answer (2 marks each)**

1. Write the number of faces, edges and vertices of a triangular prism, and
   check with Euler's relation. <span class="marks">[2]</span>
2. Find the volume and total surface area of a cuboid 8 cm by 5 cm by 4 cm.
   <span class="marks">[2]</span>
3. Find the volume of a square pyramid of base side 6 cm and height 10 cm.
   <span class="marks">[2]</span>
4. How much sheet metal is needed for a closed cube of side 25 cm, and what is
   its volume? <span class="marks">[2]</span>

::: note Answers to Group B
**1.** $F=5$, $E=9$, $V=6$; $F+V-E=5+6-9=2$ ✓.
**2.** $V=8\times5\times4=160$ cm³;
$S=2(40+20+32)=184$ cm².
**3.** $V=\frac13\times36\times10=120$ cm³.
**4.** $S=6\times625=3750$ cm²; $V=25^3=15\,625$ cm³.
:::

**Group C — Long answer (4 marks each)**

1. A closed box is 1.2 m long, 80 cm wide and 60 cm high. Find its volume in
   cubic metres and its total surface area in square metres. How much would it
   cost to paint the outside at Rs 120 per square metre?
   <span class="marks">[4]</span>
2. A water tank is in the shape of a cuboid 2 m by 1.5 m by 1 m. How many litres
   does it hold? If a bucket holds 15 litres, how many buckets fill the tank?
   <span class="marks">[4]</span>

::: note Answers to Group C
**1.** Convert everything to metres: $l=1.2$, $b=0.8$, $h=0.6$.
$$V=1.2\times0.8\times0.6=0.576\ \text{m}^3$$
$$S=2(1.2\times0.8+0.8\times0.6+0.6\times1.2)$$

$$=2(0.96+0.48+0.72)=2\times2.16=4.32\ \text{m}^2$$
Cost $=4.32\times120=\text{Rs }518.40$.
**Check.** The six faces are two of 0.96 m², two of 0.48 m² and two of 0.72 m²:
$1.92+0.96+1.44=4.32$ ✓.
**2.** $V=2\times1.5\times1=3$ m³. Since 1 m³ $=1000$ litres, the tank holds
**3000 litres**. Number of buckets $=3000\div15=200$.
**Check.** $200\times15=3000$ ✓.
:::

## Objective practice

**Choose the correct answer.** <span class="marks">[5×1=5]</span>

**1.** A cube has edges numbering
   (a) 6 (b) 8 (c) 12 (d) 16
**2.** Euler's relation for a solid is
   (a) $F + V - E = 2$ (b) $F + E - V = 2$ (c) $F - V + E = 2$ (d) $F + V + E = 2$
**3.** A triangular prism has faces numbering
   (a) 4 (b) 5 (c) 6 (d) 9
**4.** The volume of a cube of edge 6 cm is
   (a) 36 cm³ (b) 72 cm³ (c) 216 cm³ (d) 108 cm³
**5.** The total surface area of a cube of edge 5 cm is
   (a) 25 cm² (b) 125 cm² (c) 150 cm² (d) 100 cm²

::: note Objective practice — answers
**1.** (c) — 12 edges. **2.** (a) — $F + V - E = 2$. **3.** (b) — two triangles and three rectangles. **4.** (c) — $6^3 = 216$ cm³. **5.** (c) — $6 \times 5^2 = 150$ cm².
:::
