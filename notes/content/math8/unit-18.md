---
subject: Mathematics
grade: 8
unit: 18
title: Tessellation
hours: 0
area: Compulsory Mathematics
---

Tessellation is the covering of a surface with shapes, without gaps and without
overlaps. It is the mathematics behind tiled floors, brick walls, honeycomb and
much of the decoration on Nepali temples and *dhunge dhara* spouts. The
surprising result of the chapter is that only three regular polygons can do the
job on their own, and the reason is a single angle sum.

::: key What this chapter asks of you
You should be able to explain what a tessellation is, decide which regular
polygons tessellate and prove it with angles, describe a semi-regular
tessellation, and identify the symmetry used in a tiling.
:::

## 18.1 Tessellation

A **tessellation**, or tiling, is a pattern of shapes that covers a plane
completely with no gaps and no overlapping.

The condition is simple. At every vertex where the shapes meet, the angles that
come together must fill a full turn:

$$\text{sum of the angles at each vertex}=360°$$

And each shape that is not at the edge of the pattern must fit its neighbour
exactly, so its sides must match. That is all that is needed.

| Kind of tessellation | What it uses |
|---|---|
| Regular | one kind of regular polygon repeated |
| Semi-regular (Archimedean) | two or more kinds of regular polygon, arranged the same way at every vertex |
| Irregular | polygonal tiles that are not regular, often chosen so that copies interlock |
| Monohedral | one tile shape used throughout, transformed by translation, rotation and reflection |

## 18.2 Which regular polygons tessellate?

At each vertex, $k$ copies of a regular polygon with interior angle $\theta$
must fit, so

$$k\theta=360°$$

We already know the interior angle of a regular $n$-gon:
$\theta=\frac{(n-2)180°}{n}$.

| Polygon | $n$ | Interior angle | Can it fill 360°? |
|---|---|---|---|
| Equilateral triangle | 3 | 60° | yes — six fit: $6\times60=360$ |
| Square | 4 | 90° | yes — four fit: $4\times90=360$ |
| Regular pentagon | 5 | 108° | no — $3\times108=324$, $4\times108=432$ |
| Regular hexagon | 6 | 120° | yes — three fit: $3\times120=360$ |
| Regular octagon | 8 | 135° | no — $2\times135=270$, $3\times135=405$ |

So exactly **three** regular polygons tessellate on their own: the equilateral
triangle, the square and the regular hexagon. The reason each time is that the
interior angle divides 360° exactly.

```figure caption="Three regular tessellations. Six triangles, four squares or three hexagons meet at every vertex, and in each case the angles add to exactly 360°."
fig, ax = plt.subplots(figsize=(5.1, 2.7))
ax.set_xlim(0, 12)
ax.set_ylim(0, 6.4)
ax.axis("off")
# triangles
s = 1.0
for row in range(3):
    for col in range(4):
        y = 1.2 + row * (s * 0.866)
        x = 0.4 + col * s + (row % 2) * s / 2
        up = (row + col) % 2 == 0
        if up:
            ax.add_patch(plt.Polygon([(x, y), (x + s, y), (x + s / 2, y + s * 0.866)],
                                     fill=True, fc=ACCENT, alpha=0.16, ec=ACCENT, lw=0.8))
        else:
            ax.add_patch(plt.Polygon([(x, y + s * 0.866), (x + s, y + s * 0.866),
                                      (x + s / 2, y)], fill=True, fc=ACCENT,
                                     alpha=0.16, ec=ACCENT, lw=0.8))
ax.text(2.2, 5.6, "triangle  6 x 60 = 360", ha="center", fontsize=6.6, color=INK)
# squares
for row in range(3):
    for col in range(3):
        ax.add_patch(plt.Rectangle((5.4 + col * 0.85, 1.2 + row * 0.85), 0.85, 0.85,
                                   fc=SERIES[1], alpha=0.16, ec=SERIES[1], lw=0.8))
ax.text(6.65, 5.6, "square  4 x 90 = 360", ha="center", fontsize=6.6, color=INK)
# hexagons
import numpy as np
R = 0.62
for cx, cy in [(9.9, 2.1), (10.98, 2.1), (9.36, 3.17), (10.44, 3.17), (11.52, 3.17),
               (9.9, 4.24), (10.98, 4.24)]:
    if cx > 12.1:
        continue
    pts = [(cx + R * np.cos(t), cy + R * np.sin(t))
           for t in np.linspace(0, 2 * np.pi, 7)]
    ax.add_patch(plt.Polygon(pts, fill=True, fc=SERIES[2], alpha=0.16,
                             ec=SERIES[2], lw=0.8))
ax.text(10.4, 5.6, "hexagon  3 x 120 = 360", ha="center", fontsize=6.6, color=INK)
fig.tight_layout()
```

::: example Does a regular octagon tessellate?
**Problem.** A regular octagon has an interior angle of 135°. Show that it
cannot tessellate on its own.

**Solution.** At a vertex we should need $k$ octagons with

$$k\times135°=360°\qquad\Rightarrow\qquad k=\frac{360}{135}=2\frac23$$

But $k$ must be a whole number, because a whole number of tiles must meet at the
vertex. $2\frac23$ is impossible.

Checking the nearest whole numbers: $2\times135=270°$ leaves a gap of 90°, and
$3\times135=405°$ overlaps by 45°.

**Answer.** A regular octagon cannot tessellate alone. It **can** be used in a
semi-regular tessellation together with a square: $135+135+90=360°$, so two
octagons and one square meet at every vertex.

**Check.** $135+135+90=360$ ✓, which is exactly the condition.
:::

::: example Testing three polygons together
**Problem.** Can one regular triangle, one regular hexagon and one square meet
at a vertex without a gap?

**Solution.** The angles are 60°, 120° and 90°. Their sum is

$$60+120+90=270°$$

which is less than 360°, so there is a gap of 90° at the vertex. If another
square is added, the total becomes $270+90=360°$ ✓.

**Answer.** Three tiles alone leave a gap; a triangle, a hexagon and two squares
($60+120+90+90$) fit exactly.

**Check.** $60+120+90+90=360$ ✓.
:::

::: caution The angles must fit exactly, not approximately
A pattern with a tiny gap or a tiny overlap is not a tessellation. This is why
the test is arithmetic and not artistic: the angles at a vertex must add to
**exactly** 360°. A sketch that "looks about right" proves nothing.
:::

## 18.3 Semi-regular tessellations

In a **semi-regular tessellation** two or more kinds of regular polygon are used,
and the arrangement of tiles round every vertex is the same. There are exactly
eight of them.

| Vertex arrangement | Angles | Sum |
|---|---|---|
| 3.3.3.3.6 | $4\times60+120$ | 360 |
| 3.3.3.4.4 | $3\times60+2\times90$ | 360 |
| 3.3.4.3.4 | $60+60+90+60+90$ | 360 |
| 3.4.6.4 | $60+90+120+90$ | 360 |
| 3.6.3.6 | $60+120+60+120$ | 360 |
| 3.12.12 | $60+150+150$ | 360 |
| 4.6.12 | $90+120+150$ | 360 |
| 4.8.8 | $90+135+135$ | 360 |

The notation lists the number of sides of the tiles met, in order, going round
the vertex. So **4.8.8** means a square, an octagon and an octagon.

::: tip Read the notation like a recipe
In 4.8.8, the numbers are the sides of the polygons in order round one vertex.
Adding the interior angles of those polygons must give 360°:
$90+135+135=360$ ✓. Use that as the check for any vertex arrangement you meet.
:::

## 18.4 Symmetry in tessellation

Tessellations are built from the three transformations you already know.

| Transformation | What it does in a tiling |
|---|---|
| Translation | slides the tile to the next position; the commonest in brick and tile patterns |
| Reflection | mirrors the tile across a line, giving a pattern with a mirror symmetry |
| Rotation | turns the tile about a vertex; hexagonal tilings have 6-fold rotation about each vertex |
| Glide reflection | a reflection followed by a slide — found in brick walls and many *mandala* borders |

A tiling is **periodic** if a translation by some fixed distance brings the
pattern onto itself. Every tiling in this chapter is periodic.

## Chapter summary

- A tessellation covers a plane with no gaps and no overlaps; at every vertex the
  angles add to exactly 360°.
- Exactly three regular polygons tessellate alone: the equilateral triangle
  ($6\times60°$), the square ($4\times90°$) and the regular hexagon
  ($3\times120°$).
- A polygon tessellates alone only if its interior angle divides 360° exactly.
- Regular pentagons and octagons cannot tessellate alone; an octagon can be used
  with a square ($135+135+90=360$).
- In semi-regular tessellations the same arrangement of two or more regular
  polygons occurs at every vertex, written as a list such as 4.8.8.
- Tilings use translation, reflection, rotation and glide reflection, and a
  periodic tiling repeats by translation.

## Practice questions

**Group A — Objective (1 mark each)**

1. At a vertex of a tessellation the angles add up to
   <span class="marks">[1]</span>
   (a) 90° (b) 180° (c) 270° (d) 360°
2. The interior angle of a regular hexagon is <span class="marks">[1]</span>
   (a) 60° (b) 90° (c) 108° (d) 120°
3. Which regular polygon does **not** tessellate on its own?
   <span class="marks">[1]</span>
   (a) triangle (b) square (c) pentagon (d) hexagon
4. The number of squares meeting at a vertex in a square tessellation is
   <span class="marks">[1]</span>
   (a) 3 (b) 4 (c) 5 (d) 6
5. 4.8.8 means that at a vertex there are
   <span class="marks">[1]</span>
   (a) two squares and an octagon (b) a square and two octagons
   (c) four squares and an octagon (d) eight squares
6. The interior angle of a regular octagon is
   <span class="marks">[1]</span>
   (a) 120° (b) 135° (c) 144° (d) 150°

::: note Answers to Group A
**1.** (d) — a full turn, else there is a gap or an overlap.
**2.** (d) — $\frac{(6-2)180}{6}=120$.
**3.** (c) — $108°$ does not divide 360°.
**4.** (b) — $360\div90=4$.
**5.** (b) — the order is one square then two octagons.
**6.** (b) — $\frac{(8-2)180}{8}=135$.
:::

**Group B — Short answer (2 marks each)**

1. Show that an equilateral triangle tessellates and state how many meet at a
   vertex. <span class="marks">[2]</span>
2. Why does a regular pentagon fail to tessellate?
   <span class="marks">[2]</span>
3. What is a semi-regular tessellation? Give one example of a vertex
   arrangement. <span class="marks">[2]</span>
4. Name the transformation that turns one brick in a wall into the next, and
   the one that makes a mirror pattern.<span class="marks">[2]</span>
:::

::: note Answers to Group B
**1.** The interior angle of an equilateral triangle is 60°, and
$360\div60=6$, so six triangles meet at each vertex and the angles add to
$6\times60=360°$ ✓.
**2.** The interior angle of a regular pentagon is 108°.
$360\div108=3\frac13$, which is not a whole number; three pentagons give 324°
and leave a 36° gap, while four overlap. So a pentagon cannot fill the vertex.
**3.** A tessellation using two or more kinds of regular polygon, in the same
arrangement at every vertex. Example: 4.8.8, where one square and two octagons
meet, $90+135+135=360°$.
**4.** One brick to the next is a **translation** (a glide reflection also
occurs in a normal brick wall, because alternate courses are offset). A mirror
pattern is a **reflection**.
:::

**Group C — Long answer (4 marks each)**

1. For each of the regular triangle, square, hexagon and octagon, calculate the
   interior angle, and decide whether it tessellates alone. Show the arithmetic
   in a table and explain the rule you used. <span class="marks">[4]</span>
2. Design a semi-regular tessellation using squares and equilateral triangles.
   Show by angle arithmetic that the arrangement works at every vertex, draw a
   patch of it, and describe the symmetry of the pattern.
   <span class="marks">[4]</span>

::: note Answers to Group C
**1.**

| Polygon | Interior angle | $360\div\theta$ | Tessellates alone? |
|---|---|---|---|
| Triangle | 60° | 6 | yes |
| Square | 90° | 4 | yes |
| Hexagon | 120° | 3 | yes |
| Octagon | 135° | $2\frac23$ | no |

**Rule.** A regular polygon tessellates on its own exactly when
$\frac{360°}{\text{interior angle}}$ is a whole number, because a whole number
of identical tiles has to meet at each vertex — there can be no part of a tile.
**2.** **Angle arithmetic.** Three triangles and two squares:
$3\times60+2\times90=180+180=360°$ ✓. So the arrangement 3.3.3.4.4 works at every
vertex.
**Patch.** Draw a row of squares; on each square side draw an equilateral
triangle pointing outward from alternate sides, and the triangles between
neighbouring squares fit together in pairs to leave no gap. Check one vertex:
three triangle angles (180°) plus two square angles (180°) fill the point ✓.
**Symmetry.** The pattern has translation symmetry in both directions (it
repeats every two squares across and every two rows up), and rotations of order
2 about the midpoints of shared edges. It has no mirror line through every
vertex, because the triangle-and-square order runs the same way round each
vertex — which is exactly what "semi-regular" requires.
:::
