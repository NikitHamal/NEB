---
subject: Mental Agility Test
grade: CEE
unit: 4
title: Spatial Relation and Abstract Reasoning
hours: 5
area: Mental Agility Test
---

The last block of the Mental Agility Test — **5 of the 20 questions** — is the only one
asked in pictures. MEC calls it spatial relation / abstract reasoning, and its two
official sample questions show the range: *which 3D shape can be made from this 2D
net?* and *which shape completes this sequence?* Around them sit the other standard
picture types: dice, mirror and water images, folded and punched paper, hidden
(embedded) figures and counting figures. These questions reward a fixed routine more
than talent: for nets, find the opposite faces first; for images, decide what is
swapped; for paper, unfold one fold at a time; for series, follow one element at a time. In the
practice sets the figure comes first; read it fully before the question.

::: key What the paper asks from this chapter
- **Nets**: in a straight line of three squares the first and third are opposite; at the
  two ends of a Z the end squares are opposite. Opposite faces are never seen together.
- **Which cube?** Around any face, the neighbours keep the clockwise order they have in
  the net.
- **Dice**: a face seen together with X is not opposite X; on a standard die opposite
  faces add to 7.
- **Painted cube** cut into $n^3$ small cubes: 8 with three faces painted, $12(n-2)$ with
  two, $6(n-2)^2$ with one, $(n-2)^3$ with none.
- **Mirror image**: left and right swap (the order of letters reverses); **water
  image**: top and bottom swap (the order stays).
- **Paper folding**: every hole is reflected in every fold line; k folds in half give
  $2^k$ holes from one punch.
- **Counting**: count systematically — by corners or by sizes — or use the formula for
  the standard figure.
- **Series and matrices**: track each element (position, rotation, number, shading)
  separately; each must follow its own rule.
:::

## 4.1 Nets, cubes and dice

### Faces, edges and corners

A cube has **6 faces, 12 edges and 8 corners** (vertices). Each face shares an edge with
4 faces and is **opposite** exactly one. Three faces meet at every corner, so a picture
of a cube shows three faces that are pairwise adjacent — **two opposite faces can never
be seen together**.

### Nets

A **net** is a flat pattern of six squares that folds into a cube. There are exactly
**11** of them. Learn to see the opposite pairs at once:

1. **Line of three.** In a straight row (or column) of three squares, the first and the
   third are opposite.
2. **Z rule.** When four squares form a Z or S (two squares, a step, two squares), the
   two end squares are opposite.
3. Squares that share an edge in the net are always adjacent on the cube.

```figure caption="The 11 nets of a cube. Squares of the same colour become opposite faces when the net is folded: in a straight line of three, the first and third are opposite; at the two ends of a Z (or S) shape the end squares are opposite."
fig, axs = plt.subplots(3, 4, figsize=(5.2, 3.7))
nets = [[(0,0),(1,0),(1,1),(1,2),(1,3),(2,0)], [(0,0),(1,0),(1,1),(1,2),(1,3),(2,1)],
        [(0,0),(1,0),(1,1),(1,2),(1,3),(2,2)], [(0,0),(1,0),(1,1),(1,2),(1,3),(2,3)],
        [(0,1),(1,0),(1,1),(1,2),(1,3),(2,1)], [(0,1),(1,0),(1,1),(1,2),(1,3),(2,2)],
        [(0,0),(0,1),(1,1),(1,2),(1,3),(2,1)], [(0,0),(0,1),(1,1),(1,2),(1,3),(2,2)],
        [(0,0),(0,1),(1,1),(1,2),(1,3),(2,3)], [(0,0),(0,1),(1,1),(1,2),(2,2),(2,3)],
        [(0,0),(0,1),(0,2),(1,2),(1,3),(1,4)]]
cols = [[0,1,2,1,2,0]]*6 + [[0,1,2,0,2,1]]*3 + [[0,1,2,0,1,2]] + [[0,1,0,2,1,2]]
pal = ['#bcd4ee', '#f3c4c4', '#c6e6cf']
for k, ax in enumerate(axs.flat):
    ax.set_aspect('equal'); ax.axis('off')
    ax.set_xlim(-0.3, 5.3); ax.set_ylim(-2.45, 1.15)
    if k == 11:
        ax.text(2.5, -0.6, 'same colour\n= opposite\nfaces', ha='center', va='center', fontsize=8.6, color=MUTED)
        continue
    for (r, c), ci in zip(nets[k], cols[k]):
        ax.add_patch(Rectangle((c, -r), 1, 1, fc=pal[ci], ec=INK, lw=0.9))
fig.subplots_adjust(wspace=0.08, hspace=0.12)
```

A pattern is **not** a net if it has four squares in a 2 × 2 block, five or more in a
straight line, or if the rules above give some face two different opposites.

### Which cube can be made from the net?

Check the options in this order:

1. **Opposite faces.** Find the three opposite pairs from the net. Any option that shows
   two opposite faces together is wrong — this alone settles most questions.
2. **Order round a face.** Look at the top face of the option and find it in the net.
   Looking at the top face from outside, its four neighbours keep the order they have
   round it in the net. In a drawing that shows the top, the left-front and the
   right-front faces, the right face comes just **before** the left face when you go
   clockwise round the top face.

A neighbour that is not joined to the top square in the net can still be placed: fold
the joined neighbours down first and see where the next square lands.

::: example Opposite faces from a net
**Problem.** In a cross-shaped net the middle row is P, Q, R, S, with T above Q and U
below Q. Which face is opposite Q, and which is opposite T?

**Solution.** The middle row is a line of four: P–R are opposite (first and third of
P, Q, R) and Q–S are opposite (first and third of Q, R, S). The column T, Q, U is a line
of three, so **T is opposite U**. Opposite Q is **S**.
:::

### Dice

A die is a cube with the numbers 1 to 6 on its faces. On a **standard die** opposite
faces add up to 7: 1–6, 2–5, 3–4. When a question shows several positions of one die,
do not assume it is standard — work from the pictures:

1. Every number seen **together with** X in any picture is adjacent to X.
2. X has four neighbours; the one number never seen with X is **opposite** it.
3. If that leaves two candidates, look for a picture that links them to faces already
   placed.

::: example Two positions of a die
**Problem.** One position of a die shows 1 on top with 2 and 3 on the sides; another
shows 1 on top with 4 and 6 on the sides. Which number is opposite 1?

**Solution.** 1 is seen with 2, 3, 4 and 6 — its four neighbours. The only number
left is **5**, which is opposite 1. (This die is not standard.)
:::

### The painted cube

A cube painted on all its faces is cut into $n \times n \times n$ equal small cubes.
Where a small cube sits decides how many painted faces it has:

| Position | Painted faces | Number of small cubes | n = 3 | n = 4 | n = 5 |
|---|---|---|---|---|---|
| Corner | 3 | 8 | 8 | 8 | 8 |
| Edge (not corner) | 2 | $12(n - 2)$ | 12 | 24 | 36 |
| Face (not edge) | 1 | $6(n - 2)^2$ | 6 | 24 | 54 |
| Inside | 0 | $(n - 2)^3$ | 1 | 8 | 27 |
| Total | | $n^3$ | 27 | 64 | 125 |

::: example A cuboid
**Problem.** A painted cuboid 4 cm × 3 cm × 2 cm is cut into 1 cm cubes. How many cubes
have exactly two painted faces?

**Solution.** Two-face cubes lie on the edges, not at the corners. A cuboid has 4 edges
of each length: 4 × (4 − 2) + 4 × (3 − 2) + 4 × (2 − 2) = 8 + 4 + 0 = **12**. (Check:
8 corner cubes + 12 + 4 one-face cubes = 24 cubes in all.)
:::

::: caution Do not count the corners twice
A corner cube touches three faces and three edges. In the "two faces painted" count it
must be left out: an edge of 4 small cubes has only 4 − 2 = 2 two-face cubes.
:::

## 4.2 Mirror and water images

A **mirror image** is the reflection in a mirror held upright beside the object: left
and right are interchanged, top and bottom are not. A word's letters come in the reverse
order, and each letter is itself flipped. A **water image** is the reflection in a
horizontal surface below the object: top and bottom are interchanged, left and right
are not — the letters keep their order but each is upside down.

```figure caption="A word, its mirror image (mirror held to the right: left and right swap, so the letter order reverses and every letter is flipped) and its water image (mirror below: top and bottom swap, the order stays)."
from matplotlib.textpath import TextPath
from matplotlib.patches import PathPatch
from matplotlib.font_manager import FontProperties
import matplotlib.transforms as mtr
FP = FontProperties(family='DejaVu Sans', weight='bold')
def glyphs(ax, x0, y0, seq, h=0.5, step=0.42, color=INK):
    """seq: list of (char, flip_lr, flip_ud); each glyph centred in its own slot"""
    for i, (ch, fx, fy) in enumerate(seq):
        p = TextPath((0, 0), ch, size=1, prop=FP)
        e = p.get_extents()
        cx, cy = (e.x0 + e.x1)/2, (e.y0 + e.y1)/2
        k = h/0.73
        t = (mtr.Affine2D().translate(-cx, -cy).scale(-k if fx else k, -k if fy else k)
             .translate(x0 + i*step, y0) + ax.transData)
        ax.add_patch(PathPatch(p, transform=t, fc=color, ec='none'))
fig, ax = plt.subplots(figsize=(5.0, 2.5))
w = 'NEPAL'
glyphs(ax, 0.3, 2.0, [(c, False, False) for c in w])
glyphs(ax, 2.95, 2.0, [(c, True, False) for c in reversed(w)])
ax.plot([2.6, 2.6], [1.6, 2.4], ls='--', color=ACCENT, lw=1.3)
ax.text(2.6, 2.55, 'mirror', ha='center', va='bottom', fontsize=8.4, color=ACCENT)
ax.plot([0.0, 2.2], [1.25, 1.25], ls='--', color=SERIES[2], lw=1.3)
ax.text(2.25, 1.25, 'water surface', ha='left', va='center', fontsize=8.4, color=SERIES[2])
glyphs(ax, 0.3, 0.85, [(c, False, True) for c in w])
ax.text(0.95, 2.62, 'object', ha='center', va='bottom', fontsize=8.4, color=MUTED)
ax.text(3.65, 1.6, 'mirror image', ha='center', va='top', fontsize=8.4, color=MUTED)
ax.text(0.95, 0.42, 'water image', ha='center', va='top', fontsize=8.4, color=MUTED)
ax.set_xlim(-0.1, 4.9); ax.set_ylim(0.2, 2.85); ax.set_aspect('equal'); ax.axis('off')
```

| Capital letters that look the same | Letters |
|---|---|
| in a mirror (vertical line of symmetry) | A, H, I, M, O, T, U, V, W, X, Y |
| in water (horizontal line of symmetry) | B, C, D, E, H, I, K, O, X |
| in both | H, I, O, X |

A word looks the same in a mirror only if every letter is in the first row **and** the
word reads the same backwards: MOM, WOW, TOOT (TOY is not — it becomes YOT). A word
looks the same in water if every letter is in the second row, because the order does
not change: BOX, HIDE, DECIDE.

**Clocks.** For a clock seen in a mirror beside it, real time = 11:60 − time seen
(Unit 3). A mirror followed by a water image is the same as turning the figure through
180°.

::: example Picking the mirror image
**Problem.** How do you choose the mirror image of a word from four options?

**Solution.** Check two things. (1) Order: the last letter of the word must come first.
(2) Shape: an asymmetric letter (such as N, P, G, L) must be flipped. The two classic
wrong options each fail one test: the word written backwards with normal letters, and
the word in the right order with each letter flipped. A third wrong option is usually the
water image (letters upside down).
:::

## 4.3 Paper folding and cutting

A sheet is folded one or more times, and a hole (or a cut) is made through all the
layers. When it is unfolded:

1. **Count.** Each fold in half doubles the layers: one punch through k folds in half
   gives $2^k$ holes.
2. **Place.** Unfold in reverse order. Each time, every hole is reflected in the fold
   line being opened — the same distance on the other side of the line.
3. **Shape.** A cut on a fold line opens into a symmetric shape: a half-circle cut on the
   fold opens into a full circle.

```figure caption="Folding and punching. The square is folded left onto right, then top onto bottom, and one hole is punched through all four layers. Unfolding reflects the hole in each fold line in turn: 1 hole, then 2, then 4."
fig, axs = plt.subplots(1, 5, figsize=(5.2, 2.3))
def paper(ax, x0, y0, w, h):
    ax.add_patch(Rectangle((x0, y0), w, h, fc='#fbf6e9', ec=INK, lw=1.2))
def hole(ax, x, y):
    ax.add_patch(Circle((x, y), 0.06, fc=INK, ec=INK))
for ax in axs:
    ax.set_xlim(-0.12, 1.12); ax.set_ylim(-0.4, 1.12); ax.set_aspect('equal'); ax.axis('off')
paper(axs[0], 0, 0, 1, 1); axs[0].plot([0.5, 0.5], [0, 1], ls='--', color=ACCENT, lw=1.2)
axs[0].annotate('', xy=(0.78, 0.55), xytext=(0.22, 0.55), arrowprops=dict(arrowstyle='-|>', color=SERIES[1], lw=1.3, connectionstyle='arc3,rad=-0.5'))
paper(axs[1], 0.5, 0, 0.5, 1); axs[1].plot([0.5, 1], [0.5, 0.5], ls='--', color=ACCENT, lw=1.2)
axs[1].annotate('', xy=(0.75, 0.25), xytext=(0.75, 0.8), arrowprops=dict(arrowstyle='-|>', color=SERIES[1], lw=1.3, connectionstyle='arc3,rad=-0.5'))
paper(axs[2], 0.5, 0, 0.5, 0.5); hole(axs[2], 0.85, 0.15)
paper(axs[3], 0.5, 0, 0.5, 1); hole(axs[3], 0.85, 0.15); hole(axs[3], 0.85, 0.85)
paper(axs[4], 0, 0, 1, 1)
for x, y in [(0.85, 0.15), (0.85, 0.85), (0.15, 0.15), (0.15, 0.85)]:
    hole(axs[4], x, y)
for ax, t in zip(axs, ['fold 1', 'fold 2', 'punch', 'open fold 2', 'open fold 1']):
    ax.text(0.5, -0.24, t, ha='center', va='center', fontsize=8.4, color=MUTED)
fig.subplots_adjust(wspace=0.12)
```

::: example Unfold one fold at a time
**Problem.** A square sheet is folded left onto right and then top onto bottom, and one
hole is punched near the outer corner of the folded square (the corner that was the
bottom-right corner of the sheet). Where are the holes on the opened sheet?

**Solution.** Open the second fold first: the hole is reflected in the horizontal fold
line, giving two holes one above the other. Open the first fold: both are reflected in
the vertical fold line. **Four holes, one near each corner of the sheet** (figure above).
Had the hole been punched near the inner corner of the folded square, the four holes
would sit round the centre of the sheet instead.
:::

::: caution A hole is reflected, not copied
A hole near the right edge of the folded paper reappears near the *left* edge after
opening a vertical fold — not in the same place on the other half. And a diagonal fold
reflects in that diagonal: a hole near the bottom edge reappears near the left edge.
:::

## 4.4 Embedded figures and counting figures

### Embedded (hidden) figures

The given figure X is hidden in one of the options, with the **same size, the same
shape and the same way up** — not rotated, not reflected. Find the most unusual part of X
(an odd angle, a short tail, a small closed shape), look for it in each option, and then
check every line of X against the option. Options that contain X turned over, rotated,
stretched or with one line moved are the standard distractors.

### Counting figures

Count with a system, never by eye:

- **Label the points** and list the figures by their corners.
- **Count by size**: smallest pieces first, then figures made of two pieces, three, …
- **Use a formula** for a standard figure.

| Figure | Count |
|---|---|
| Triangle with n lines from the top corner to the base | $(n + 1)(n + 2)/2$ triangles |
| The same with h lines across, parallel to the base (base included) | h × $(n + 1)(n + 2)/2$ |
| Square with both diagonals | 8 triangles |
| Square with both diagonals and both mid-lines | 16 triangles |
| n × n grid of squares | $1^2 + 2^2 + \dots + n^2$ squares (3 × 3: 14; 4 × 4: 30) |
| m × n grid | $\frac{m(m+1)}{2} \times \frac{n(n+1)}{2}$ rectangles (2 × 2: 9; 3 × 3: 36) |

```figure caption="Counting triangles. Every triangle in this figure has A as its top corner and two of the five base points B, P, Q, R, C as its other corners, so the count is the number of ways of choosing 2 points from 5."
fig, ax = plt.subplots(figsize=(4.2, 2.4))
A = (2.0, 2.0); base = [(0.0, 0.0), (0.8, 0.0), (1.7, 0.0), (2.7, 0.0), (4.0, 0.0)]
names = ['B', 'P', 'Q', 'R', 'C']
ax.plot([base[0][0], base[-1][0]], [0, 0], color=INK, lw=1.4)
for (x, y), n in zip(base, names):
    ax.plot([A[0], x], [A[1], y], color=INK, lw=1.4)
    ax.text(x, -0.18, n, ha='center', va='top', fontsize=10, fontweight='bold')
ax.text(A[0], A[1] + 0.12, 'A', ha='center', va='bottom', fontsize=10, fontweight='bold')
ax.set_xlim(-0.4, 4.4); ax.set_ylim(-0.6, 2.5); ax.set_aspect('equal'); ax.axis('off')
```

::: example Counting triangles
**Problem.** How many triangles are there in the figure above?

**Solution.** Every triangle has A as one corner and two of the base points B, P, Q, R,
C as the others. Choosing 2 points out of 5 gives 5 × 4/2 = **10** triangles. (By
sizes: 4 single pieces, 3 made of two, 2 of three, 1 of four: 4 + 3 + 2 + 1 = 10.)
:::

## 4.5 Figure series, analogies and matrices

### Series

A figure series changes by a fixed rule from one step to the next. The elements that
change are few:

| Element | Typical rule |
|---|---|
| Position | moves one corner (or 45°, 90°) clockwise or anticlockwise each step |
| Rotation | turns through 45°, 90° or 180° each step |
| Number | one more (or one fewer) dot, line or side each step |
| Shading | alternates, or moves round the parts of the figure |
| Size | grows or shrinks each step |

**Method.** Follow one element across all the steps and write its rule; then the next
element. For each rule, cross out the options that break it. Usually one element removes
two options and a second element removes the third.

```figure caption="A figure series with two moving parts. The dot moves one corner clockwise each step; the arrow turns 90° anticlockwise each step. Step 5 (shaded) follows from tracking each part separately."
fig, axs = plt.subplots(1, 5, figsize=(5.2, 2.2))
corners = [(0.15, 0.85), (0.85, 0.85), (0.85, 0.15), (0.15, 0.15)]
dirs = [90, 180, 270, 0]
for k, ax in enumerate(axs):
    ax.set_xlim(-0.05, 1.05); ax.set_ylim(-0.32, 1.05); ax.set_aspect('equal'); ax.axis('off')
    ax.add_patch(Rectangle((0, 0), 1, 1, fc='#fde9c8' if k == 4 else 'white', ec=INK, lw=1.2))
    cx, cy = corners[k % 4]
    ax.add_patch(Circle((cx, cy), 0.08, fc=INK, ec=INK))
    a = np.radians(dirs[k % 4])
    ax.annotate('', xy=(0.5 + 0.27*np.cos(a), 0.5 + 0.27*np.sin(a)), xytext=(0.5 - 0.27*np.cos(a), 0.5 - 0.27*np.sin(a)),
                arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.8, mutation_scale=12))
    ax.text(0.5, -0.18, 'step %d' % (k + 1), ha='center', va='center', fontsize=8.4, color=MUTED)
fig.subplots_adjust(wspace=0.15)
```

::: example Two elements at once
**Problem.** In the series above (steps 1 to 4), what does step 5 look like?

**Solution.** The dot visits the corners top-left → top-right → bottom-right →
bottom-left: clockwise, one corner per step, so step 5 is top-left again. The arrow
points up → left → down → right: 90° anticlockwise each step, so step 5 points up.
Step 5: **dot at top-left, arrow up** (shaded).
:::

### Analogies

Figure 1 : figure 2 :: figure 3 : ? — find what was done to figure 1 to give figure 2
(rotated 90° clockwise, reflected, shading reversed, a line added, the inner and outer
shapes swapped) and do exactly that to figure 3. With rotations, check the direction: a
rotation by 90° clockwise and a reflection can look alike for a shape with symmetry,
so test a shape with no symmetry.

### Matrices

In a 3 × 3 matrix each row (and often each column) follows the same rule. Common rules:

- each row contains one of each of three shapes (a Latin square);
- a count increases along the row (1, 2, 3 dots);
- the third figure is the first two laid on top of each other, or keeps only the lines
  that are not common to both.

Find the rule in the two complete rows, check it on the columns, then apply it to the
row with the gap.

::: tip Eliminate, then confirm
In figure questions, the fastest route is elimination: test one feature at a time and
cross out options. Once one option is left, confirm it against *all* the rules — the
setters build a distractor that is right in every feature but one.
:::

## Formula and fact sheet

| Topic | Fact |
|---|---|
| Cube | 6 faces, 12 edges, 8 corners; each face has 4 neighbours and 1 opposite |
| Nets | 11 nets; line of three → ends opposite; Z shape → ends opposite |
| Not a net | a 2 × 2 block, 5 in a row, or a face with two opposites |
| Which cube | opposite faces never together; neighbours keep their clockwise order round a face |
| Standard die | opposite faces add to 7: 1–6, 2–5, 3–4 |
| Die from views | a face seen with X is adjacent; the one never seen with X is opposite |
| Painted cube ($n^3$ pieces) | 3 faces: 8; 2 faces: $12(n-2)$; 1 face: $6(n-2)^2$; none: $(n-2)^3$ |
| Painted cuboid | two-face cubes: 4 × [(a − 2) + (b − 2) + (c − 2)] |
| Mirror image | left–right swap; letter order reverses; A H I M O T U V W X Y unchanged |
| Water image | top–bottom swap; order unchanged; B C D E H I K O X unchanged |
| Mirror + water | = rotation through 180° |
| Mirror clock | real time = 11:60 − time seen |
| Paper folding | k folds in half → $2^k$ holes; unfold in reverse, reflect in each fold line |
| Triangles | n lines from the apex: $(n+1)(n+2)/2$; × h with h cross lines |
| Squares in n × n grid | $1^2 + 2^2 + \dots + n^2$ |
| Rectangles in m × n grid | $\frac{m(m+1)}{2} \times \frac{n(n+1)}{2}$ |
| Series | track position, rotation, number, shading, size — one at a time |

## Chapter summary

- Spatial relation / abstract reasoning carries 5 of the 20 MAT questions; the MEC
  samples are a net → cube question and a figure-sequence question.
- Nets: find the opposite pairs (line of three, Z rule); options showing two opposite
  faces together are wrong; the remaining ones are decided by the clockwise order of the
  neighbours round a face.
- Dice: faces seen together are adjacent; the face never seen with X is opposite X; a
  standard die has opposite faces adding to 7.
- Painted cubes: 8, $12(n-2)$, $6(n-2)^2$, $(n-2)^3$ for three, two, one and no painted
  faces.
- Mirror image swaps left and right (reversed order, flipped letters); water image swaps
  top and bottom (same order).
- Folded paper: $2^k$ holes from k folds; unfold in reverse, reflecting every hole in each
  fold line.
- Count figures systematically, by corners or by sizes, or with the standard formulas.
- Series, analogies and matrices: follow one element at a time and eliminate options.

## Practice questions

**Set A — Recall (25 questions)**

1. In a standard die the numbers on opposite faces add up to 7. Which number is opposite 3?
   (a) 4 (b) 1 (c) 6 (d) 5
2. How many faces of a cube share an edge with any one face?
   (a) 2 (b) 3 (c) 4 (d) 5

```figure caption="For Set A, questions 3 and 4: a net of a cube."
from matplotlib.patches import Polygon as Pg
X_ = np.array([0.866, -0.5]); Y_ = np.array([0.866, 0.5]); Z_ = np.array([0.0, 1.0])
def sym(ax, o, u, v, name, lw=1.5):
    o = np.asarray(o, float); u = np.asarray(u, float); v = np.asarray(v, float)
    M = lambda s, t: o + s*u + t*v
    th = np.linspace(0, 2*np.pi, 64)
    circ = lambda r: [M(0.5 + r*np.cos(a), 0.5 + r*np.sin(a)) for a in th]
    if name == 'dot':
        ax.add_patch(Pg(circ(0.17), closed=True, fc=INK, ec=INK, lw=0.8))
    elif name == 'ring':
        ax.add_patch(Pg(circ(0.27), closed=True, fc='none', ec=INK, lw=lw))
    elif name == 'bullseye':
        ax.add_patch(Pg(circ(0.3), closed=True, fc='none', ec=INK, lw=lw))
        ax.add_patch(Pg(circ(0.1), closed=True, fc=INK, ec=INK, lw=0.8))
    elif name in ('black', 'grey'):
        ax.add_patch(Pg([M(0, 0), M(1, 0), M(1, 1), M(0, 1)], closed=True,
                        fc=INK if name == 'black' else '#a3abb6', ec=INK, lw=1.2))
def iso(ax, ox, oy, s, top, front, right, num=False):
    O = np.array([ox, oy], float)
    sh = ['#eef1f5', 'white', '#dde3ea'] if num else ['white', 'white', 'white']
    for o, u, v, fc, lab in [(O + s*Z_, s*X_, s*Y_, sh[0], top), (O, s*X_, s*Z_, sh[1], front),
                             (O + s*X_, s*Y_, s*Z_, sh[2], right)]:
        ax.add_patch(Pg([o, o + u, o + u + v, o + v], closed=True, fc=fc, ec=INK, lw=1.2))
        if num:
            c = o + 0.5*u + 0.5*v
            ax.text(c[0], c[1], str(lab), ha='center', va='center', fontsize=11, fontweight='bold')
        else:
            sym(ax, o, u, v, lab)
def net(ax, cells, ox, oy, s, labels=None, syms=None, fc='white'):
    for k, (r, c) in enumerate(cells):
        x, y = ox + c*s, oy - r*s
        ax.add_patch(Rectangle((x, y), s, s, fc=fc, ec=INK, lw=1.2))
        if syms:
            sym(ax, (x, y), (s, 0), (0, s), syms[k])
        if labels:
            ax.text(x + s/2, y + s/2, labels[k], ha='center', va='center', fontsize=11, fontweight='bold')
fig, ax = plt.subplots(figsize=(4.0, 2.4))
net(ax, [(0,1),(1,0),(1,1),(1,2),(1,3),(2,1)], 0, 1.6, 0.8, labels=list('ABCDEF'))
ax.set_xlim(-0.8, 4.0); ax.set_ylim(-0.1, 2.5); ax.set_aspect('equal'); ax.axis('off')
```

3. In the figure above, which face is opposite face A when the net is folded into a cube?
   (a) C (b) F (c) D (d) E
4. In the same net, which face is opposite face B?
   (a) D (b) E (c) F (d) A
5. How many different nets does a cube have?
   (a) 6 (b) 8 (c) 10 (d) 11
6. How many edges does a cube have?
   (a) 6 (b) 8 (c) 12 (d) 24
7. A cube painted on all its faces is cut into 27 equal small cubes. How many small cubes have exactly two painted faces?
   (a) 8 (b) 12 (c) 6 (d) 1
8. In the same 27 small cubes, how many have no painted face?
   (a) 1 (b) 0 (c) 6 (d) 8

```figure caption="For Set A, question 9: two positions of the same die (the numbers are printed upright; only which faces touch matters)."
from matplotlib.patches import Polygon as Pg
X_ = np.array([0.866, -0.5]); Y_ = np.array([0.866, 0.5]); Z_ = np.array([0.0, 1.0])
def sym(ax, o, u, v, name, lw=1.5):
    o = np.asarray(o, float); u = np.asarray(u, float); v = np.asarray(v, float)
    M = lambda s, t: o + s*u + t*v
    th = np.linspace(0, 2*np.pi, 64)
    circ = lambda r: [M(0.5 + r*np.cos(a), 0.5 + r*np.sin(a)) for a in th]
    if name == 'dot':
        ax.add_patch(Pg(circ(0.17), closed=True, fc=INK, ec=INK, lw=0.8))
    elif name == 'ring':
        ax.add_patch(Pg(circ(0.27), closed=True, fc='none', ec=INK, lw=lw))
    elif name == 'bullseye':
        ax.add_patch(Pg(circ(0.3), closed=True, fc='none', ec=INK, lw=lw))
        ax.add_patch(Pg(circ(0.1), closed=True, fc=INK, ec=INK, lw=0.8))
    elif name in ('black', 'grey'):
        ax.add_patch(Pg([M(0, 0), M(1, 0), M(1, 1), M(0, 1)], closed=True,
                        fc=INK if name == 'black' else '#a3abb6', ec=INK, lw=1.2))
def iso(ax, ox, oy, s, top, front, right, num=False):
    O = np.array([ox, oy], float)
    sh = ['#eef1f5', 'white', '#dde3ea'] if num else ['white', 'white', 'white']
    for o, u, v, fc, lab in [(O + s*Z_, s*X_, s*Y_, sh[0], top), (O, s*X_, s*Z_, sh[1], front),
                             (O + s*X_, s*Y_, s*Z_, sh[2], right)]:
        ax.add_patch(Pg([o, o + u, o + u + v, o + v], closed=True, fc=fc, ec=INK, lw=1.2))
        if num:
            c = o + 0.5*u + 0.5*v
            ax.text(c[0], c[1], str(lab), ha='center', va='center', fontsize=11, fontweight='bold')
        else:
            sym(ax, o, u, v, lab)
def net(ax, cells, ox, oy, s, labels=None, syms=None, fc='white'):
    for k, (r, c) in enumerate(cells):
        x, y = ox + c*s, oy - r*s
        ax.add_patch(Rectangle((x, y), s, s, fc=fc, ec=INK, lw=1.2))
        if syms:
            sym(ax, (x, y), (s, 0), (0, s), syms[k])
        if labels:
            ax.text(x + s/2, y + s/2, labels[k], ha='center', va='center', fontsize=11, fontweight='bold')
fig, ax = plt.subplots(figsize=(4.0, 2.3))
iso(ax, 0.0, 0.0, 1.0, 2, 1, 4, num=True)
iso(ax, 2.6, 0.0, 1.0, 2, 5, 3, num=True)
ax.text(0.87, -0.75, '(i)', ha='center', va='center', fontsize=9.5)
ax.text(3.47, -0.75, '(ii)', ha='center', va='center', fontsize=9.5)
ax.set_xlim(-0.4, 4.7); ax.set_ylim(-0.95, 1.6); ax.set_aspect('equal'); ax.axis('off')
```

9. In the figure above, which number is opposite 2?
   (a) 3 (b) 5 (c) 6 (d) 1
10. A cube painted on all its faces is cut into 64 equal small cubes. How many small cubes have exactly one painted face?
   (a) 16 (b) 24 (c) 32 (d) 8
11. On a standard die (opposite faces add up to 7), which three numbers can be seen together at one corner?
   (a) 1, 6, 2 (b) 2, 5, 3 (c) 3, 4, 1 (d) 1, 2, 3
12. Which word looks exactly the same in a mirror held upright beside it?
   (a) DAD (b) MOM (c) NUN (d) POP
13. Which word looks exactly the same in its water image?
   (a) MAT (b) TOY (c) BOX (d) WAX
14. Which capital letter does NOT look the same in a mirror held upright beside it?
   (a) A (b) H (c) T (d) N

```figure caption="For Set A, question 15: the word LOGIC with a mirror held to its right, and four images."
from matplotlib.textpath import TextPath
from matplotlib.patches import PathPatch
from matplotlib.font_manager import FontProperties
import matplotlib.transforms as mtr
FP = FontProperties(family='DejaVu Sans', weight='bold')
def glyphs(ax, x0, y0, seq, h=0.5, step=0.42, color=INK):
    """seq: list of (char, flip_lr, flip_ud); each glyph centred in its own slot"""
    for i, (ch, fx, fy) in enumerate(seq):
        p = TextPath((0, 0), ch, size=1, prop=FP)
        e = p.get_extents()
        cx, cy = (e.x0 + e.x1)/2, (e.y0 + e.y1)/2
        k = h/0.73
        t = (mtr.Affine2D().translate(-cx, -cy).scale(-k if fx else k, -k if fy else k)
             .translate(x0 + i*step, y0) + ax.transData)
        ax.add_patch(PathPatch(p, transform=t, fc=color, ec='none'))
def optlabel(ax, x, y, t):
    ax.text(x, y, t, ha='center', va='center', fontsize=10, fontweight='bold', color=INK)
fig, ax = plt.subplots(figsize=(5.0, 2.3))
w = 'LOGIC'
glyphs(ax, 0.4, 2.0, [(c, False, False) for c in w])
ax.plot([2.45, 2.45], [1.65, 2.35], ls='--', color=ACCENT, lw=1.3)
ax.text(2.6, 2.0, 'mirror', ha='left', va='center', fontsize=8.6, color=ACCENT)
opts = [[(c, True, False) for c in reversed(w)], [(c, False, False) for c in reversed(w)],
        [(c, True, False) for c in w], [(c, False, True) for c in w]]
for k, seq in enumerate(opts):
    x0 = 0.4 + 2.55*(k % 2); y0 = 1.0 - 0.75*(k // 2)
    optlabel(ax, x0 - 0.35, y0, '(%s)' % 'abcd'[k])
    glyphs(ax, x0 + 0.05, y0, seq, h=0.42, step=0.36)
ax.set_xlim(-0.2, 5.0); ax.set_ylim(-0.0, 2.45); ax.set_aspect('equal'); ax.axis('off')
```

15. In the figure above, which option is the mirror image of the word?
   (a) image a (b) image b (c) image c (d) image d
16. In the water image of a figure,
   (a) left and right are interchanged (b) top and bottom are interchanged (c) both are interchanged (d) the figure turns through 90°

```figure caption="For Set A, question 17: which figure comes next in the series?"
def optlabel(ax, x, y, t):
    ax.text(x, y, t, ha='center', va='center', fontsize=10, fontweight='bold', color=INK)
fig, ax = plt.subplots(figsize=(5.0, 2.4))
def cell(x, y, ang, fc='white', q=False):
    ax.add_patch(Rectangle((x, y), 1, 1, fc=fc, ec=INK, lw=1.2))
    if q:
        ax.text(x + 0.5, y + 0.5, '?', ha='center', va='center', fontsize=14, fontweight='bold'); return
    a = np.radians(90 - ang)
    ax.annotate('', xy=(x + 0.5 + 0.36*np.cos(a), y + 0.5 + 0.36*np.sin(a)),
                xytext=(x + 0.5 - 0.36*np.cos(a), y + 0.5 - 0.36*np.sin(a)),
                arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.8, mutation_scale=13))
for k, ang in enumerate([0, 45, 90, 135]):
    cell(0.2 + 1.2*k, 1.6, ang)
cell(0.2 + 4.8, 1.6, 0, fc='#fde9c8', q=True)
for k, (lab, ang) in enumerate([('(a)', 225), ('(b)', 180), ('(c)', 0), ('(d)', 135)]):
    cell(0.8 + 1.4*k, 0.0, ang)
    optlabel(ax, 1.3 + 1.4*k, -0.25, lab)
ax.set_xlim(0.0, 6.4); ax.set_ylim(-0.5, 2.75); ax.set_aspect('equal'); ax.axis('off')
```

17. In the figure above, which option comes next in the series?
   (a) figure a (b) figure b (c) figure c (d) figure d
18. A sheet of paper is folded in half, then in half again, and one hole is punched through all the layers. How many holes are there when it is unfolded?
   (a) 2 (b) 3 (c) 4 (d) 8
19. How many squares of all sizes are there in a 3 × 3 grid of squares?
   (a) 9 (b) 10 (c) 13 (d) 14

```figure caption="For Set A, question 20: a square sheet is folded once along the dashed line (left half onto the right half) and one hole is punched."
def optlabel(ax, x, y, t):
    ax.text(x, y, t, ha='center', va='center', fontsize=10, fontweight='bold', color=INK)
fig, ax = plt.subplots(figsize=(5.0, 2.6))
def sheet(x, y, w, h, fc='#fbf6e9'):
    ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=INK, lw=1.2))
def hole(x, y):
    ax.add_patch(Circle((x, y), 0.065, fc=INK, ec=INK))
sheet(0.3, 1.5, 1, 1); ax.plot([0.8, 0.8], [1.5, 2.5], ls='--', color=ACCENT, lw=1.2)
ax.annotate('', xy=(1.08, 2.05), xytext=(0.52, 2.05), arrowprops=dict(arrowstyle='-|>', color=SERIES[1], lw=1.3, connectionstyle='arc3,rad=-0.5'))
sheet(2.4, 1.5, 0.5, 1); hole(2.4 + 0.25, 1.5 + 0.65)
ax.text(2.0, 2.0, '→', ha='center', va='center', fontsize=13)
opts = [[(0.25, 0.65), (0.75, 0.65)], [(0.75, 0.65), (0.75, 0.35)], [(0.75, 0.65)], [(0.25, 0.35), (0.75, 0.65)]]
for k, hs in enumerate(opts):
    x0 = 0.3 + 1.45*k
    sheet(x0, 0.0, 1, 1)
    for hx, hy in hs:
        hole(x0 + hx, hy)
    optlabel(ax, x0 + 0.5, -0.25, '(%s)' % 'abcd'[k])
ax.set_xlim(0.1, 6.0); ax.set_ylim(-0.5, 2.7); ax.set_aspect('equal'); ax.axis('off')
```

20. In the figure above, which option shows the sheet when it is unfolded?
   (a) sheet a (b) sheet b (c) sheet c (d) sheet d
21. How many rectangles of all sizes (squares included) are there in a 2 × 2 grid of squares?
   (a) 4 (b) 5 (c) 8 (d) 9
22. A square has both its diagonals drawn. How many triangles are there in the figure?
   (a) 4 (b) 6 (c) 8 (d) 10

```figure caption="For Set A, question 23: count the triangles."
fig, ax = plt.subplots(figsize=(4.0, 2.3))
A = (1.5, 2.0)
for x in [0.0, 1.0, 2.0, 3.0]:
    ax.plot([A[0], x], [A[1], 0], color=INK, lw=1.4)
ax.plot([0, 3], [0, 0], color=INK, lw=1.4)
ax.set_xlim(-0.6, 3.6); ax.set_ylim(-0.2, 2.2); ax.set_aspect('equal'); ax.axis('off')
```

23. How many triangles are there in the figure above?
   (a) 3 (b) 5 (c) 6 (d) 4
24. A cube of side 4 cm is cut into cubes of side 1 cm. How many small cubes are obtained?
   (a) 16 (b) 64 (c) 32 (d) 48
25. A cube painted on all its faces is cut into 27 equal small cubes. How many small cubes have three painted faces?
   (a) 8 (b) 4 (c) 12 (d) 6

::: note Answers and explanations — Set A
**1.** (a) — 3 + 4 = 7.
**2.** (c) — A face has four edges and shares each with one neighbour; only the opposite face is not a neighbour.
**3.** (b) — A, C, F are a column of three: the first and third, A and F, are opposite.
**4.** (a) — B, C, D are a row of three, so B and D are opposite (and C is opposite E).
**5.** (d) — There are exactly 11 nets of a cube.
**6.** (c) — 4 edges round the top, 4 round the bottom and 4 upright: 12.
**7.** (b) — n = 3: 12(n − 2) = 12. One middle cube on each of the 12 edges.
**8.** (a) — (n − 2)³ = 1: only the centre cube is hidden from every face.
**9.** (c) — 2 is seen with 1 and 4 in (i) and with 5 and 3 in (ii): its four neighbours are 1, 3, 4, 5. The number never seen with 2 is 6, so 6 is opposite 2.
**10.** (b) — n = 4: 6(n − 2)² = 6 × 4 = 24 (the 2 × 2 centre of each face).
**11.** (d) — Faces at a corner are pairwise adjacent, so no two may add to 7. Each other option contains an opposite pair (1–6, 2–5, 3–4).
**12.** (b) — In a mirror the letter order reverses and each letter is flipped. MOM reads the same backwards and M and O are symmetric left to right. D, N and P are not.
**13.** (c) — The water image keeps the order but turns each letter upside down; B, O and X are symmetric top to bottom. M, A, T, Y and W are not.
**14.** (d) — A, H and T have a vertical line of symmetry; N does not (its mirror image is И).
**15.** (a) — The mirror image reverses the order (C first) and flips every letter. (b) only reverses the order, (c) only flips the letters, (d) is the water image.
**16.** (b) — A horizontal mirror below the figure interchanges top and bottom only.
**17.** (b) — The arrow turns 45° clockwise each step: up, up-right, right, down-right, so next is down.
**18.** (c) — Two folds in half give 2² = 4 layers, so one punch makes 4 holes.
**19.** (d) — 9 small squares + 4 squares of side 2 + 1 of side 3 = 14.
**20.** (a) — The hole is reflected in the fold line: the same height, the same distance on the left of the fold. Option (b) reflects it in a horizontal line instead; (c) forgets the second layer.
**21.** (d) — (2 × 3/2) × (2 × 3/2) = 3 × 3 = 9: 4 small squares, 2 + 2 two-square rectangles and the whole square.
**22.** (c) — 4 small triangles and 4 made of two small ones (each half of the square): 8.
**23.** (c) — Two lines from the top corner divide the base into 3 parts: the triangles are chosen by 2 of the 4 base points, (2 + 1)(2 + 2)/2 = 6.
**24.** (b) — 4 × 4 × 4 = 64.
**25.** (a) — The three-face cubes are the 8 corners, for any n ≥ 2.
:::

**Set B — Understanding (15 questions)**

```figure caption="For Set B, question 1: a net of a cube (dot, black, ring, grey, bullseye and blank faces) and four cubes."
from matplotlib.patches import Polygon as Pg
X_ = np.array([0.866, -0.5]); Y_ = np.array([0.866, 0.5]); Z_ = np.array([0.0, 1.0])
def sym(ax, o, u, v, name, lw=1.5):
    o = np.asarray(o, float); u = np.asarray(u, float); v = np.asarray(v, float)
    M = lambda s, t: o + s*u + t*v
    th = np.linspace(0, 2*np.pi, 64)
    circ = lambda r: [M(0.5 + r*np.cos(a), 0.5 + r*np.sin(a)) for a in th]
    if name == 'dot':
        ax.add_patch(Pg(circ(0.17), closed=True, fc=INK, ec=INK, lw=0.8))
    elif name == 'ring':
        ax.add_patch(Pg(circ(0.27), closed=True, fc='none', ec=INK, lw=lw))
    elif name == 'bullseye':
        ax.add_patch(Pg(circ(0.3), closed=True, fc='none', ec=INK, lw=lw))
        ax.add_patch(Pg(circ(0.1), closed=True, fc=INK, ec=INK, lw=0.8))
    elif name in ('black', 'grey'):
        ax.add_patch(Pg([M(0, 0), M(1, 0), M(1, 1), M(0, 1)], closed=True,
                        fc=INK if name == 'black' else '#a3abb6', ec=INK, lw=1.2))
def iso(ax, ox, oy, s, top, front, right, num=False):
    O = np.array([ox, oy], float)
    sh = ['#eef1f5', 'white', '#dde3ea'] if num else ['white', 'white', 'white']
    for o, u, v, fc, lab in [(O + s*Z_, s*X_, s*Y_, sh[0], top), (O, s*X_, s*Z_, sh[1], front),
                             (O + s*X_, s*Y_, s*Z_, sh[2], right)]:
        ax.add_patch(Pg([o, o + u, o + u + v, o + v], closed=True, fc=fc, ec=INK, lw=1.2))
        if num:
            c = o + 0.5*u + 0.5*v
            ax.text(c[0], c[1], str(lab), ha='center', va='center', fontsize=11, fontweight='bold')
        else:
            sym(ax, o, u, v, lab)
def net(ax, cells, ox, oy, s, labels=None, syms=None, fc='white'):
    for k, (r, c) in enumerate(cells):
        x, y = ox + c*s, oy - r*s
        ax.add_patch(Rectangle((x, y), s, s, fc=fc, ec=INK, lw=1.2))
        if syms:
            sym(ax, (x, y), (s, 0), (0, s), syms[k])
        if labels:
            ax.text(x + s/2, y + s/2, labels[k], ha='center', va='center', fontsize=11, fontweight='bold')
def optlabel(ax, x, y, t):
    ax.text(x, y, t, ha='center', va='center', fontsize=10, fontweight='bold', color=INK)
fig, ax = plt.subplots(figsize=(5.2, 3.3))
net(ax, [(0,0),(0,1),(1,1),(1,2),(1,3),(2,2)], 0.9, 3.4, 0.62, syms=['dot', 'black', 'ring', 'grey', 'bullseye', 'blank'])
opts = [('dot', 'ring', 'grey'), ('ring', 'bullseye', 'black'), ('black', 'ring', 'grey'), ('blank', 'grey', 'black')]
for k, (t, f, r) in enumerate(opts):
    x0 = 0.15 + 1.65*k
    iso(ax, x0, 0.4, 0.75, t, f, r)
    optlabel(ax, x0 + 0.65, -0.25, '(%s)' % 'abcd'[k])
ax.set_xlim(0.0, 6.9); ax.set_ylim(-0.5, 4.1); ax.set_aspect('equal'); ax.axis('off')
```

1. In the figure above, which cube can be made from the net?
   (a) cube a (b) cube b (c) cube c (d) cube d

```figure caption="For Set B, question 2: three positions of the same die (numbers printed upright)."
from matplotlib.patches import Polygon as Pg
X_ = np.array([0.866, -0.5]); Y_ = np.array([0.866, 0.5]); Z_ = np.array([0.0, 1.0])
def sym(ax, o, u, v, name, lw=1.5):
    o = np.asarray(o, float); u = np.asarray(u, float); v = np.asarray(v, float)
    M = lambda s, t: o + s*u + t*v
    th = np.linspace(0, 2*np.pi, 64)
    circ = lambda r: [M(0.5 + r*np.cos(a), 0.5 + r*np.sin(a)) for a in th]
    if name == 'dot':
        ax.add_patch(Pg(circ(0.17), closed=True, fc=INK, ec=INK, lw=0.8))
    elif name == 'ring':
        ax.add_patch(Pg(circ(0.27), closed=True, fc='none', ec=INK, lw=lw))
    elif name == 'bullseye':
        ax.add_patch(Pg(circ(0.3), closed=True, fc='none', ec=INK, lw=lw))
        ax.add_patch(Pg(circ(0.1), closed=True, fc=INK, ec=INK, lw=0.8))
    elif name in ('black', 'grey'):
        ax.add_patch(Pg([M(0, 0), M(1, 0), M(1, 1), M(0, 1)], closed=True,
                        fc=INK if name == 'black' else '#a3abb6', ec=INK, lw=1.2))
def iso(ax, ox, oy, s, top, front, right, num=False):
    O = np.array([ox, oy], float)
    sh = ['#eef1f5', 'white', '#dde3ea'] if num else ['white', 'white', 'white']
    for o, u, v, fc, lab in [(O + s*Z_, s*X_, s*Y_, sh[0], top), (O, s*X_, s*Z_, sh[1], front),
                             (O + s*X_, s*Y_, s*Z_, sh[2], right)]:
        ax.add_patch(Pg([o, o + u, o + u + v, o + v], closed=True, fc=fc, ec=INK, lw=1.2))
        if num:
            c = o + 0.5*u + 0.5*v
            ax.text(c[0], c[1], str(lab), ha='center', va='center', fontsize=11, fontweight='bold')
        else:
            sym(ax, o, u, v, lab)
def net(ax, cells, ox, oy, s, labels=None, syms=None, fc='white'):
    for k, (r, c) in enumerate(cells):
        x, y = ox + c*s, oy - r*s
        ax.add_patch(Rectangle((x, y), s, s, fc=fc, ec=INK, lw=1.2))
        if syms:
            sym(ax, (x, y), (s, 0), (0, s), syms[k])
        if labels:
            ax.text(x + s/2, y + s/2, labels[k], ha='center', va='center', fontsize=11, fontweight='bold')
fig, ax = plt.subplots(figsize=(4.8, 2.3))
for k, (t, f, r) in enumerate([(3, 2, 4), (1, 3, 4), (6, 4, 2)]):
    iso(ax, 2.4*k, 0.0, 1.0, t, f, r, num=True)
    ax.text(2.4*k + 0.87, -0.75, '(%s)' % ['i', 'ii', 'iii'][k], ha='center', va='center', fontsize=9.5)
ax.set_xlim(-0.3, 6.8); ax.set_ylim(-0.95, 1.6); ax.set_aspect('equal'); ax.axis('off')
```

2. In the figure above, which number is opposite 4?
   (a) 1 (b) 5 (c) 6 (d) 2

```figure caption="For Set B, question 3: four arrangements of six squares."
from matplotlib.patches import Polygon as Pg
X_ = np.array([0.866, -0.5]); Y_ = np.array([0.866, 0.5]); Z_ = np.array([0.0, 1.0])
def sym(ax, o, u, v, name, lw=1.5):
    o = np.asarray(o, float); u = np.asarray(u, float); v = np.asarray(v, float)
    M = lambda s, t: o + s*u + t*v
    th = np.linspace(0, 2*np.pi, 64)
    circ = lambda r: [M(0.5 + r*np.cos(a), 0.5 + r*np.sin(a)) for a in th]
    if name == 'dot':
        ax.add_patch(Pg(circ(0.17), closed=True, fc=INK, ec=INK, lw=0.8))
    elif name == 'ring':
        ax.add_patch(Pg(circ(0.27), closed=True, fc='none', ec=INK, lw=lw))
    elif name == 'bullseye':
        ax.add_patch(Pg(circ(0.3), closed=True, fc='none', ec=INK, lw=lw))
        ax.add_patch(Pg(circ(0.1), closed=True, fc=INK, ec=INK, lw=0.8))
    elif name in ('black', 'grey'):
        ax.add_patch(Pg([M(0, 0), M(1, 0), M(1, 1), M(0, 1)], closed=True,
                        fc=INK if name == 'black' else '#a3abb6', ec=INK, lw=1.2))
def iso(ax, ox, oy, s, top, front, right, num=False):
    O = np.array([ox, oy], float)
    sh = ['#eef1f5', 'white', '#dde3ea'] if num else ['white', 'white', 'white']
    for o, u, v, fc, lab in [(O + s*Z_, s*X_, s*Y_, sh[0], top), (O, s*X_, s*Z_, sh[1], front),
                             (O + s*X_, s*Y_, s*Z_, sh[2], right)]:
        ax.add_patch(Pg([o, o + u, o + u + v, o + v], closed=True, fc=fc, ec=INK, lw=1.2))
        if num:
            c = o + 0.5*u + 0.5*v
            ax.text(c[0], c[1], str(lab), ha='center', va='center', fontsize=11, fontweight='bold')
        else:
            sym(ax, o, u, v, lab)
def net(ax, cells, ox, oy, s, labels=None, syms=None, fc='white'):
    for k, (r, c) in enumerate(cells):
        x, y = ox + c*s, oy - r*s
        ax.add_patch(Rectangle((x, y), s, s, fc=fc, ec=INK, lw=1.2))
        if syms:
            sym(ax, (x, y), (s, 0), (0, s), syms[k])
        if labels:
            ax.text(x + s/2, y + s/2, labels[k], ha='center', va='center', fontsize=11, fontweight='bold')
def optlabel(ax, x, y, t):
    ax.text(x, y, t, ha='center', va='center', fontsize=10, fontweight='bold', color=INK)
fig, ax = plt.subplots(figsize=(5.2, 2.2))
shapes = [[(0,0),(0,1),(0,2),(1,2),(1,3),(2,3)], [(0,1),(1,0),(1,1),(1,2),(1,3),(2,1)],
          [(0,0),(0,1),(1,1),(1,2),(2,2),(2,3)], [(0,0),(0,1),(1,1),(1,2),(1,3),(2,3)]]
for k, cells in enumerate(shapes):
    x0 = 0.1 + 1.55*k
    net(ax, cells, x0, 1.0, 0.33, fc='#eef1f5')
    optlabel(ax, x0 + 0.66, 0.05, '(%s)' % 'abcd'[k])
ax.set_xlim(0.0, 6.3); ax.set_ylim(-0.15, 1.45); ax.set_aspect('equal'); ax.axis('off')
```

3. In the figure above, which arrangement can NOT be folded into a cube?
   (a) shape a (b) shape b (c) shape c (d) shape d
4. A cube painted on all its faces is cut into 64 equal small cubes. How many small cubes have no painted face?
   (a) 16 (b) 4 (c) 24 (d) 8
5. A cube painted on all its faces is cut into 125 equal small cubes. How many small cubes have exactly two painted faces?
   (a) 24 (b) 36 (c) 48 (d) 54
6. A cube painted on all its faces is cut into 64 equal small cubes. How many small cubes have at least one painted face?
   (a) 56 (b) 48 (c) 60 (d) 8

```figure caption="For Set B, question 7: the word PALPA above a water surface, and four images."
from matplotlib.textpath import TextPath
from matplotlib.patches import PathPatch
from matplotlib.font_manager import FontProperties
import matplotlib.transforms as mtr
FP = FontProperties(family='DejaVu Sans', weight='bold')
def glyphs(ax, x0, y0, seq, h=0.5, step=0.42, color=INK):
    """seq: list of (char, flip_lr, flip_ud); each glyph centred in its own slot"""
    for i, (ch, fx, fy) in enumerate(seq):
        p = TextPath((0, 0), ch, size=1, prop=FP)
        e = p.get_extents()
        cx, cy = (e.x0 + e.x1)/2, (e.y0 + e.y1)/2
        k = h/0.73
        t = (mtr.Affine2D().translate(-cx, -cy).scale(-k if fx else k, -k if fy else k)
             .translate(x0 + i*step, y0) + ax.transData)
        ax.add_patch(PathPatch(p, transform=t, fc=color, ec='none'))
def optlabel(ax, x, y, t):
    ax.text(x, y, t, ha='center', va='center', fontsize=10, fontweight='bold', color=INK)
fig, ax = plt.subplots(figsize=(5.0, 2.4))
w = 'PALPA'
glyphs(ax, 0.4, 2.15, [(c, False, False) for c in w])
ax.plot([0.1, 2.3], [1.75, 1.75], ls='--', color=SERIES[2], lw=1.3)
ax.text(2.4, 1.75, 'water surface', ha='left', va='center', fontsize=8.6, color=SERIES[2])
opts = [[(c, True, False) for c in reversed(w)], [(c, False, True) for c in reversed(w)],
        [(c, True, True) for c in reversed(w)], [(c, False, True) for c in w]]
for k, seq in enumerate(opts):
    x0 = 0.4 + 2.55*(k % 2); y0 = 1.1 - 0.75*(k // 2)
    optlabel(ax, x0 - 0.35, y0, '(%s)' % 'abcd'[k])
    glyphs(ax, x0 + 0.05, y0, seq, h=0.42, step=0.36)
ax.set_xlim(-0.2, 5.0); ax.set_ylim(0.05, 2.6); ax.set_aspect('equal'); ax.axis('off')
```

7. In the figure above, which option is the water image of the word?
   (a) image a (b) image b (c) image c (d) image d

```figure caption="For Set B, question 8: a square sheet is folded top half onto bottom half, then left half onto right half, and one hole is punched."
def optlabel(ax, x, y, t):
    ax.text(x, y, t, ha='center', va='center', fontsize=10, fontweight='bold', color=INK)
fig, ax = plt.subplots(figsize=(5.0, 2.7))
def sheet(x, y, w, h, fc='#fbf6e9'):
    ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=INK, lw=1.2))
def hole(x, y):
    ax.add_patch(Circle((x, y), 0.06, fc=INK, ec=INK))
sheet(0.3, 1.55, 1, 1); ax.plot([0.3, 1.3], [2.05, 2.05], ls='--', color=ACCENT, lw=1.2)
ax.annotate('', xy=(0.8, 1.78), xytext=(0.8, 2.33), arrowprops=dict(arrowstyle='-|>', color=SERIES[1], lw=1.3, connectionstyle='arc3,rad=-0.5'))
ax.text(1.65, 1.8, '→', ha='center', va='center', fontsize=13)
sheet(2.0, 1.55, 1, 0.5); ax.plot([2.5, 2.5], [1.55, 2.05], ls='--', color=ACCENT, lw=1.2)
ax.annotate('', xy=(2.78, 1.8), xytext=(2.22, 1.8), arrowprops=dict(arrowstyle='-|>', color=SERIES[1], lw=1.3, connectionstyle='arc3,rad=-0.5'))
ax.text(3.35, 1.8, '→', ha='center', va='center', fontsize=13)
sheet(3.7, 1.55, 0.5, 0.5); hole(3.7 + 0.25, 1.55 + 0.1)
opts = [[(0.75, 0.1), (0.25, 0.1)], [(0.75, 0.1), (0.25, 0.1), (0.75, 0.9), (0.25, 0.9)],
        [(0.9, 0.25), (0.1, 0.25), (0.9, 0.75), (0.1, 0.75)], [(0.75, 0.1), (0.25, 0.1), (0.75, 0.9)]]
for k, hs in enumerate(opts):
    x0 = 0.3 + 1.45*k
    sheet(x0, 0.0, 1, 1)
    for hx, hy in hs:
        hole(x0 + hx, hy)
    optlabel(ax, x0 + 0.5, -0.25, '(%s)' % 'abcd'[k])
ax.set_xlim(0.1, 6.0); ax.set_ylim(-0.5, 2.75); ax.set_aspect('equal'); ax.axis('off')
```

8. In the figure above, which option shows the sheet when it is unfolded?
   (a) sheet a (b) sheet b (c) sheet c (d) sheet d

```figure caption="For Set B, question 9: which figure comes next in the series?"
def optlabel(ax, x, y, t):
    ax.text(x, y, t, ha='center', va='center', fontsize=10, fontweight='bold', color=INK)
fig, ax = plt.subplots(figsize=(5.0, 2.5))
def cell(x, y, n, corner, fc='white', q=False):
    ax.add_patch(Rectangle((x, y), 1, 1, fc=fc, ec=INK, lw=1.2))
    if q:
        ax.text(x + 0.5, y + 0.5, '?', ha='center', va='center', fontsize=14, fontweight='bold'); return
    tri = {'TL': [(0, 1), (0.4, 1), (0, 0.6)], 'TR': [(1, 1), (0.6, 1), (1, 0.6)],
           'BR': [(1, 0), (0.6, 0), (1, 0.4)], 'BL': [(0, 0), (0.4, 0), (0, 0.4)]}[corner]
    ax.add_patch(Polygon([(x + a, y + b) for a, b in tri], closed=True, fc=MUTED, ec=INK, lw=0.8))
    pos = [(0.5, 0.5), (0.3, 0.3), (0.7, 0.7), (0.3, 0.7), (0.7, 0.3), (0.5, 0.18)]
    pos = {1: [(0.5, 0.5)], 2: [(0.38, 0.5), (0.62, 0.5)], 3: [(0.3, 0.5), (0.5, 0.5), (0.7, 0.5)],
           4: [(0.38, 0.38), (0.62, 0.38), (0.38, 0.62), (0.62, 0.62)],
           5: [(0.3, 0.38), (0.5, 0.38), (0.7, 0.38), (0.4, 0.62), (0.6, 0.62)],
           6: [(0.3, 0.38), (0.5, 0.38), (0.7, 0.38), (0.3, 0.62), (0.5, 0.62), (0.7, 0.62)]}[n]
    for px, py in pos:
        ax.add_patch(Circle((x + px, y + py), 0.06, fc=INK, ec=INK))
seq = [(1, 'TL'), (2, 'TR'), (3, 'BR'), (4, 'BL')]
for k, (n, c) in enumerate(seq):
    cell(0.2 + 1.2*k, 1.6, n, c)
cell(0.2 + 4.8, 1.6, 0, 'TL', fc='#fde9c8', q=True)
for k, (n, c) in enumerate([(5, 'BL'), (4, 'TL'), (6, 'TR'), (5, 'TL')]):
    cell(0.8 + 1.4*k, 0.0, n, c)
    optlabel(ax, 1.3 + 1.4*k, -0.25, '(%s)' % 'abcd'[k])
ax.set_xlim(0.0, 6.4); ax.set_ylim(-0.5, 2.75); ax.set_aspect('equal'); ax.axis('off')
```

9. In the figure above, which option comes next in the series?
   (a) figure a (b) figure b (c) figure c (d) figure d

```figure caption="For Set B, question 10: the first figure is related to the second in the same way as the third is related to which option?"
def optlabel(ax, x, y, t):
    ax.text(x, y, t, ha='center', va='center', fontsize=10, fontweight='bold', color=INK)
fig, ax = plt.subplots(figsize=(5.0, 2.6))
FLAG = [[(-0.3, -0.8), (-0.3, 0.8)], [(-0.3, 0.8), (0.6, 0.55), (-0.3, 0.3)]]
EF = [[(-0.4, -0.8), (-0.4, 0.8), (0.5, 0.8)], [(-0.4, 0.05), (0.3, 0.05)]]
def tf(shape, m):
    return [[(m[0]*x + m[1]*y, m[2]*x + m[3]*y) for x, y in line] for line in shape]
CW, CCW, MIR, R180, ID = (0, 1, -1, 0), (0, -1, 1, 0), (-1, 0, 0, 1), (-1, 0, 0, -1), (1, 0, 0, 1)
def draw(shape, x, y, fc='white'):
    ax.add_patch(Rectangle((x, y), 1, 1, fc=fc, ec=MUTED, lw=1.0))
    for line in shape:
        xs = [x + 0.5 + 0.4*a for a, b in line]; ys = [y + 0.5 + 0.4*b for a, b in line]
        ax.plot(xs, ys, color=INK, lw=2.0, solid_capstyle='round', solid_joinstyle='round')
draw(tf(FLAG, ID), 0.3, 1.6); ax.text(1.55, 2.1, ':', ha='center', va='center', fontsize=14)
draw(tf(FLAG, CW), 1.8, 1.6); ax.text(3.15, 2.1, '::', ha='center', va='center', fontsize=14)
draw(tf(EF, ID), 3.5, 1.6); ax.text(4.75, 2.1, ':', ha='center', va='center', fontsize=14)
ax.add_patch(Rectangle((5.0, 1.6), 1, 1, fc='#fde9c8', ec=MUTED, lw=1.0))
ax.text(5.5, 2.1, '?', ha='center', va='center', fontsize=14, fontweight='bold')
for k, m in enumerate([CCW, MIR, CW, R180]):
    draw(tf(EF, m), 0.8 + 1.4*k, 0.0)
    optlabel(ax, 1.3 + 1.4*k, -0.25, '(%s)' % 'abcd'[k])
ax.set_xlim(0.1, 6.3); ax.set_ylim(-0.5, 2.75); ax.set_aspect('equal'); ax.axis('off')
```

10. In the figure above, which option completes the analogy?
   (a) figure a (b) figure b (c) figure c (d) figure d

```figure caption="For Set B, question 11: count the triangles."
fig, ax = plt.subplots(figsize=(4.0, 2.3))
A = (1.5, 2.0)
for x in [0.0, 1.0, 2.0, 3.0]:
    ax.plot([A[0], x], [A[1], 0], color=INK, lw=1.4)
ax.plot([0, 3], [0, 0], color=INK, lw=1.4)
ax.plot([0.75, 2.25], [1.0, 1.0], color=INK, lw=1.4)
ax.set_xlim(-0.6, 3.6); ax.set_ylim(-0.2, 2.2); ax.set_aspect('equal'); ax.axis('off')
```

11. How many triangles are there in the figure above?
   (a) 9 (b) 10 (c) 12 (d) 6
12. How many squares of all sizes are there in a 4 × 4 grid of squares?
   (a) 30 (b) 16 (c) 25 (d) 20
13. How many rectangles of all sizes (squares included) are there in a 3 × 3 grid of squares?
   (a) 14 (b) 36 (c) 9 (d) 30
14. On a standard die, 2 and 3 are on two neighbouring faces. Which number can be on a face that touches both of them?
   (a) 4 (b) 5 (c) 6 (d) 3
15. In a mirror held beside a wall clock, the clock appears to show 2:30. What is the actual time?
   (a) 9:30 (b) 10:30 (c) 9:00 (d) 8:30

::: note Answers and explanations — Set B
**1.** (c) — Opposite pairs from the net: ring–bullseye (row of three), dot–grey (ends of the Z dot, black, ring, grey) and black–blank (ends of the Z black, ring, grey, blank). (a) shows dot with grey, (b) ring with bullseye and (d) black with blank — each shows an opposite pair. In (c), with black on top, the ring folds down in front and the grey square, joined to the ring's right edge, comes round to the right.
**2.** (b) — 4 is seen with 3 and 2 in (i), with 1 and 3 in (ii) and with 6 and 2 in (iii): its neighbours are 1, 2, 3, 6. The number never seen with 4 is 5.
**3.** (a) — In shape (a) the top row is a line of three, so its first and third squares are opposite; the third square, the next two and the last one form a Z, so the same third square is also opposite the last square. A face cannot have two opposites, so (a) cannot fold. (b), (c) and (d) are among the 11 nets.
**4.** (d) — n = 4: (n − 2)³ = 2³ = 8 hidden cubes.
**5.** (b) — n = 5: 12(n − 2) = 12 × 3 = 36.
**6.** (a) — All 64 minus the 8 unpainted inner cubes: 56.
**7.** (d) — A water image keeps the letters in the same order and turns each upside down. (a) is the mirror image, (c) the figure turned through 180°, and (b) also reverses the order.
**8.** (b) — The packet is the bottom-right quarter, and the hole is near its bottom edge, midway across. Opening the second fold reflects it in the vertical centre line (a second hole near the bottom edge); opening the first reflects both in the horizontal centre line (two holes near the top edge). (c) puts the holes near the side edges instead; (a) and (d) leave out holes.
**9.** (d) — The dots increase by one (1, 2, 3, 4 → 5) and the shaded corner moves clockwise (top-left, top-right, bottom-right, bottom-left → top-left). Only (d) has five dots and the top-left corner.
**10.** (c) — The flag is turned through 90° clockwise. Turning the F through 90° clockwise puts its upright stroke along the top, with both bars hanging down. (a) is turned anticlockwise and (b) is a mirror image.
**11.** (c) — Two lines from the top corner make (2 + 1)(2 + 2)/2 = 6 triangles on the base; the cross line makes another 6 above it: 2 × 6 = 12.
**12.** (a) — 16 + 9 + 4 + 1 = 30.
**13.** (b) — (3 × 4/2) × (3 × 4/2) = 6 × 6 = 36. 14 counts only the squares.
**14.** (c) — The faces touching both 2 and 3 are those opposite neither: not 5 (opposite 2) and not 4 (opposite 3). So 1 or 6; of the options only 6.
**15.** (a) — 11:60 − 2:30 = 9:30.
:::

**Set C — Application (10 questions)**

```figure caption="For Set C, question 1: a net of a cube (ring, dot, bullseye, black, grey and blank faces) and four cubes."
from matplotlib.patches import Polygon as Pg
X_ = np.array([0.866, -0.5]); Y_ = np.array([0.866, 0.5]); Z_ = np.array([0.0, 1.0])
def sym(ax, o, u, v, name, lw=1.5):
    o = np.asarray(o, float); u = np.asarray(u, float); v = np.asarray(v, float)
    M = lambda s, t: o + s*u + t*v
    th = np.linspace(0, 2*np.pi, 64)
    circ = lambda r: [M(0.5 + r*np.cos(a), 0.5 + r*np.sin(a)) for a in th]
    if name == 'dot':
        ax.add_patch(Pg(circ(0.17), closed=True, fc=INK, ec=INK, lw=0.8))
    elif name == 'ring':
        ax.add_patch(Pg(circ(0.27), closed=True, fc='none', ec=INK, lw=lw))
    elif name == 'bullseye':
        ax.add_patch(Pg(circ(0.3), closed=True, fc='none', ec=INK, lw=lw))
        ax.add_patch(Pg(circ(0.1), closed=True, fc=INK, ec=INK, lw=0.8))
    elif name in ('black', 'grey'):
        ax.add_patch(Pg([M(0, 0), M(1, 0), M(1, 1), M(0, 1)], closed=True,
                        fc=INK if name == 'black' else '#a3abb6', ec=INK, lw=1.2))
def iso(ax, ox, oy, s, top, front, right, num=False):
    O = np.array([ox, oy], float)
    sh = ['#eef1f5', 'white', '#dde3ea'] if num else ['white', 'white', 'white']
    for o, u, v, fc, lab in [(O + s*Z_, s*X_, s*Y_, sh[0], top), (O, s*X_, s*Z_, sh[1], front),
                             (O + s*X_, s*Y_, s*Z_, sh[2], right)]:
        ax.add_patch(Pg([o, o + u, o + u + v, o + v], closed=True, fc=fc, ec=INK, lw=1.2))
        if num:
            c = o + 0.5*u + 0.5*v
            ax.text(c[0], c[1], str(lab), ha='center', va='center', fontsize=11, fontweight='bold')
        else:
            sym(ax, o, u, v, lab)
def net(ax, cells, ox, oy, s, labels=None, syms=None, fc='white'):
    for k, (r, c) in enumerate(cells):
        x, y = ox + c*s, oy - r*s
        ax.add_patch(Rectangle((x, y), s, s, fc=fc, ec=INK, lw=1.2))
        if syms:
            sym(ax, (x, y), (s, 0), (0, s), syms[k])
        if labels:
            ax.text(x + s/2, y + s/2, labels[k], ha='center', va='center', fontsize=11, fontweight='bold')
def optlabel(ax, x, y, t):
    ax.text(x, y, t, ha='center', va='center', fontsize=10, fontweight='bold', color=INK)
fig, ax = plt.subplots(figsize=(5.2, 3.3))
net(ax, [(0,0),(0,1),(1,1),(1,2),(2,2),(2,3)], 1.3, 3.4, 0.62, syms=['ring', 'dot', 'bullseye', 'black', 'grey', 'blank'])
opts = [('bullseye', 'black', 'grey'), ('dot', 'bullseye', 'ring'), ('bullseye', 'dot', 'black'), ('bullseye', 'grey', 'black')]
for k, (t, f, r) in enumerate(opts):
    x0 = 0.15 + 1.65*k
    iso(ax, x0, 0.4, 0.75, t, f, r)
    optlabel(ax, x0 + 0.65, -0.25, '(%s)' % 'abcd'[k])
ax.set_xlim(0.0, 6.9); ax.set_ylim(-0.5, 4.1); ax.set_aspect('equal'); ax.axis('off')
```

1. In the figure above, which cube can be made from the net?
   (a) cube a (b) cube b (c) cube c (d) cube d

```figure caption="For Set C, question 2: the square is folded along its diagonal (top-right half onto bottom-left half), then the triangle is folded in half along the dashed line, and one hole is punched."
def optlabel(ax, x, y, t):
    ax.text(x, y, t, ha='center', va='center', fontsize=10, fontweight='bold', color=INK)
fig, ax = plt.subplots(figsize=(5.0, 2.7))
def tri(P, fc='#fbf6e9'):
    ax.add_patch(Polygon(P, closed=True, fc=fc, ec=INK, lw=1.2))
def hole(x, y):
    ax.add_patch(Circle((x, y), 0.055, fc=INK, ec=INK))
ox, oy = 0.3, 1.55
tri([(ox, oy), (ox + 1, oy), (ox + 1, oy + 1), (ox, oy + 1)])
ax.plot([ox, ox + 1], [oy + 1, oy], ls='--', color=ACCENT, lw=1.2)
ax.annotate('', xy=(ox + 0.32, oy + 0.32), xytext=(ox + 0.85, oy + 0.85), arrowprops=dict(arrowstyle='-|>', color=SERIES[1], lw=1.3, connectionstyle='arc3,rad=0.45'))
ax.text(1.65, 2.05, '→', ha='center', va='center', fontsize=13)
ox = 2.0
tri([(ox, oy), (ox + 1, oy), (ox, oy + 1)])
ax.plot([ox, ox + 0.5], [oy, oy + 0.5], ls='--', color=ACCENT, lw=1.2)
ax.annotate('', xy=(ox + 0.42, oy + 0.16), xytext=(ox + 0.14, oy + 0.62), arrowprops=dict(arrowstyle='-|>', color=SERIES[1], lw=1.3, connectionstyle='arc3,rad=0.45'))
ax.text(3.35, 2.05, '→', ha='center', va='center', fontsize=13)
ox = 3.7
tri([(ox, oy), (ox + 1, oy), (ox + 0.5, oy + 0.5)]); hole(ox + 0.6, oy + 0.15)
opts = [[(0.6, 0.15), (0.15, 0.6)], [(0.6, 0.15), (0.4, 0.15), (0.6, 0.85), (0.4, 0.85)],
        [(0.6, 0.15), (0.15, 0.6), (0.85, 0.4), (0.4, 0.85)], [(0.6, 0.15), (0.15, 0.6), (0.6, 0.85), (0.85, 0.6)]]
for k, hs in enumerate(opts):
    x0 = 0.3 + 1.45*k
    tri([(x0, 0), (x0 + 1, 0), (x0 + 1, 1), (x0, 1)])
    for hx, hy in hs:
        hole(x0 + hx, hy)
    optlabel(ax, x0 + 0.5, -0.25, '(%s)' % 'abcd'[k])
ax.set_xlim(0.1, 6.0); ax.set_ylim(-0.5, 2.75); ax.set_aspect('equal'); ax.axis('off')
```

2. In the figure above, which option shows the sheet when it is unfolded?
   (a) sheet a (b) sheet b (c) sheet c (d) sheet d

```figure caption="For Set C, question 3: which option completes the matrix?"
def optlabel(ax, x, y, t):
    ax.text(x, y, t, ha='center', va='center', fontsize=10, fontweight='bold', color=INK)
fig, ax = plt.subplots(figsize=(5.0, 3.4))
def shape(x, y, kind, n, s=0.9):
    cx, cy = x + s/2, y + s/2 + 0.07
    if kind == 'circle':
        ax.add_patch(Circle((cx, cy), 0.3, fc='white', ec=INK, lw=1.4))
    elif kind == 'square':
        ax.add_patch(Rectangle((cx - 0.28, cy - 0.28), 0.56, 0.56, fc='white', ec=INK, lw=1.4))
    else:
        ax.add_patch(Polygon([(cx - 0.32, cy - 0.24), (cx + 0.32, cy - 0.24), (cx, cy + 0.32)], closed=True, fc='white', ec=INK, lw=1.4))
    xs = {1: [0.0], 2: [-0.09, 0.09], 3: [-0.12, 0.0, 0.12]}[n]
    for dx in xs:
        ax.add_patch(Circle((cx + dx, cy - 0.06), 0.035, fc=INK, ec=INK))
grid = [['circle', 'square', 'triangle'], ['square', 'triangle', 'circle'], ['triangle', 'circle', None]]
for r in range(3):
    for c in range(3):
        x, y = 0.2 + 0.9*c, 2.2 - 0.9*r
        ax.add_patch(Rectangle((x, y), 0.9, 0.9, fc='#fde9c8' if grid[r][c] is None else 'white', ec=MUTED, lw=1.0))
        if grid[r][c] is None:
            ax.text(x + 0.45, y + 0.45, '?', ha='center', va='center', fontsize=14, fontweight='bold')
        else:
            shape(x, y, grid[r][c], c + 1)
for k, (kind, n) in enumerate([('square', 3), ('triangle', 3), ('square', 2), ('circle', 3)]):
    x, y = 3.3 + 1.0*(k % 2), 2.2 - 1.2*(k // 2)
    ax.add_patch(Rectangle((x, y), 0.9, 0.9, fc='white', ec=MUTED, lw=1.0))
    shape(x, y, kind, n)
    optlabel(ax, x + 0.45, y - 0.15, '(%s)' % 'abcd'[k])
ax.set_xlim(0.1, 5.4); ax.set_ylim(0.3, 3.2); ax.set_aspect('equal'); ax.axis('off')
```

3. In the figure above, which option replaces the question mark?
   (a) figure a (b) figure b (c) figure c (d) figure d

```figure caption="For Set C, question 4: in which option is figure X hidden, with the same size and the same way up?"
def optlabel(ax, x, y, t):
    ax.text(x, y, t, ha='center', va='center', fontsize=10, fontweight='bold', color=INK)
fig, ax = plt.subplots(figsize=(5.0, 2.6))
s = 0.55
def tree_s(x, y, h, flip=False, stem=True, sx=0.5):
    d = -1 if flip else 1
    ax.plot([x - s/2, x + s/2, x, x - s/2], [y, y, y + d*h, y], color=INK, lw=1.4)
    if stem:
        ax.plot([x - s/2 + sx*s, x - s/2 + sx*s], [y, y - d*0.22], color=INK, lw=1.4)
tree_s(0.9, 1.85, 0.44)
ax.text(0.3, 2.0, 'X', ha='center', va='center', fontsize=11, fontweight='bold')
for k in range(4):
    x0 = 0.25 + 1.5*k
    ax.add_patch(Rectangle((x0, 0.0), 1.3, 1.3, fc='none', ec=INK, lw=1.4))
    ax.plot([x0, x0 + 1.3], [0.65, 0.65], color=INK, lw=1.4)
    optlabel(ax, x0 + 0.65, -0.25, '(%s)' % 'abcd'[k])
X = [0.25 + 1.5*k + 0.65 for k in range(4)]
tree_s(X[0], 0.65, 0.44, flip=True)
tree_s(X[1], 0.65, 0.44)
tree_s(X[2], 0.65, 0.44, sx=0.18)
tree_s(X[3], 0.65, 0.6)
ax.set_xlim(0.0, 6.4); ax.set_ylim(-0.5, 2.6); ax.set_aspect('equal'); ax.axis('off')
```

4. In the figure above, in which option is figure X embedded?
   (a) figure a (b) figure b (c) figure c (d) figure d

```figure caption="For Set C, question 5: count the triangles. The four inner slanting lines join the midpoints of the sides."
fig, ax = plt.subplots(figsize=(4.0, 2.4))
ax.add_patch(Rectangle((0, 0), 2, 2, fc='none', ec=INK, lw=1.4))
ax.plot([0, 2], [0, 2], color=INK, lw=1.4); ax.plot([0, 2], [2, 0], color=INK, lw=1.4)
ax.plot([1, 2, 1, 0, 1], [0, 1, 2, 1, 0], color=INK, lw=1.4)
ax.set_xlim(-0.9, 2.9); ax.set_ylim(-0.15, 2.15); ax.set_aspect('equal'); ax.axis('off')
```

5. How many triangles are there in the figure above?
   (a) 16 (b) 12 (c) 24 (d) 20
6. A 4 × 4 × 4 cube is painted on two opposite faces only and then cut into 64 unit cubes. How many unit cubes have no paint at all?
   (a) 16 (b) 32 (c) 48 (d) 8
7. A cuboid 5 cm × 4 cm × 3 cm is painted on all its faces and cut into 1 cm cubes. How many cubes have exactly two painted faces?
   (a) 22 (b) 12 (c) 24 (d) 36
8. A painted cube is cut into equal small cubes, and exactly 8 of the small cubes have no paint. How many small cubes have exactly one painted face?
   (a) 24 (b) 8 (c) 48 (d) 36
9. A word is reflected in an upright mirror, and that image is then reflected in a horizontal mirror below it. Compared with the original word, the final image is
   (a) turned through 90° clockwise (b) turned through 180° (c) turned through 90° anticlockwise (d) unchanged
10. A cube painted blue on all its faces is cut into 8 equal small cubes. How many faces of the small cubes, in all, are unpainted?
   (a) 8 (b) 16 (c) 24 (d) 48

::: note Answers and explanations — Set C
**1.** (d) — Opposite pairs (Z rule): ring–black, dot–grey, bullseye–blank; no option shows a pair, so fold. Put the bullseye on top: the dot folds to the back and black to the right; grey, joined to the lower edge of black, comes round to the front; the ring goes to the left. So with the bullseye on top, grey is in front and black on the right: (d). (a) swaps them (a mirror image). In (c), with the bullseye on top and the dot in front, the right face would be the ring, not black. In (b), with the dot on top and the bullseye in front, the right face would be black, not the ring.
**2.** (c) — The hole is near the bottom edge, a little right of its middle. Opening the second fold reflects it in the line from the bottom-left corner to the centre: a second hole near the left edge, a little above its middle. Opening the diagonal fold reflects both in the other diagonal: holes near the right edge (a little below its middle) and near the top edge (a little left of its middle) — a "pinwheel" of four holes, symmetric about both diagonals. (d) is symmetric about one diagonal only, (b) about the mid-lines instead of the diagonals, and (a) has only two holes although the punch went through four layers.
**3.** (a) — Each row contains one circle, one square and one triangle, so the gap is a square; the dots go 1, 2, 3 along every row, so it has 3 dots.
**4.** (b) — (b) has the triangle the same way up, the same size, with the short line hanging from the middle of its base. (a) is upside down, in (c) the short line is not at the middle, and in (d) the triangle is taller.
**5.** (d) — The square with its two diagonals already holds 8 triangles (4 quarters and 4 halves). The inner lines cut off a triangle at each corner, and the diagonal splits it into two small ones: 3 triangles per corner, 12 in all. The four pieces inside the inner square are squares, not triangles. Total 8 + 12 = 20.
**6.** (b) — The two painted faces each hold 16 cubes, so 32 cubes have paint and 64 − 32 = 32 have none.
**7.** (c) — Two-face cubes lie on the 12 edges, corners left out: 4 × (5 − 2) + 4 × (4 − 2) + 4 × (3 − 2) = 12 + 8 + 4 = 24. (22 is the number with one painted face.)
**8.** (a) — (n − 2)³ = 8 gives n = 4. One-face cubes: 6(n − 2)² = 6 × 4 = 24.
**9.** (b) — The mirror swaps left and right, the water image swaps top and bottom; doing both is a half-turn (180°).
**10.** (c) — Each of the 8 small cubes is a corner cube with 3 painted and 3 unpainted faces: 8 × 3 = 24.
:::
