---
subject: Mathematics
grade: 10
unit: 7
title: Prism and Pyramid
hours: 0
area: Compulsory Mathematics
---

A room, a water tank, a tent, a roof, a Toblerone box and a temple spire are all prisms or pyramids. A **prism** has the same cross-section all along its length; a **pyramid** narrows from a flat base to a single point. This chapter gives the surface area and volume of the cuboid, cube, triangular and other prisms, the square pyramid, and — as a close relative — the cone. You will also learn to find the **slant height** from the height using Pythagoras, because almost every pyramid question needs it.

::: key What the SEE asks from this chapter
Typical 3- or 4-mark questions: (i) surface area and volume of a **triangular prism** or a prism with a trapezium base; (ii) area of the **four walls** of a room and the cost of painting; (iii) a **square pyramid** where the height is given and you must find the **slant height** (or the reverse) before finding the surface area and volume; (iv) volume of a pyramid and finding the missing height; (v) a **tent** (pyramid or cone) and the cloth needed. Unit conversions: 1 dm³ $=1$ litre, 1 m³ $=1000$ litres.
:::

```photo id="math10/pyramid" caption="The Great Pyramid of Cheops. A pyramid has one polygonal base and triangular faces that meet at a single apex; its volume is one third of the prism standing on the same base." width="96"
```

## 7.1 Prism and Pyramid: concepts, formulas and worked problems

### Prisms

::: definition Prism
A **prism** is a solid whose two ends are equal, parallel polygons (the **bases**) and whose side faces are rectangles (in a **right prism**). The prism is named after its base: triangular prism, rectangular prism (cuboid), hexagonal prism. The **height** (or length) $h$ of the prism is the distance between the two bases.
:::

The **lateral surface** is the sides only (not the bases). Because the side faces are rectangles of height $h$ whose widths are the sides of the base, they unroll into one big rectangle of length equal to the **perimeter of the base**.

::: key Right prism: three formulas
Let $P$ be the perimeter of the base, $A$ the area of the base and $h$ the height.

$$ \text{LSA}=P\times h \qquad \text{TSA}=P\times h+2A \qquad V=A\times h $$

- Lateral surface area (LSA) is also called the **area of the four walls** for a cuboid.
- Volume $=$ area of the cross-section $\times$ length.
:::

### Cuboid and cube

For a cuboid of length $l$, breadth $b$ and height $h$ the general formulas become:

| Solid | LSA | TSA | Volume | Diagonal |
|---|---|---|---|---|
| Cuboid | $2h(l+b)$ | $2(lb+bh+hl)$ | $lbh$ | $\sqrt{l^2+b^2+h^2}$ |
| Cube (side $a$) | $4a^2$ | $6a^2$ | $a^3$ | $a\sqrt{3}$ |

::: example Cuboid
**Problem.** A cuboid has length 12 cm, breadth 4 cm and height 3 cm. Find its lateral surface area, total surface area, volume and diagonal.

**Solution.** $\text{LSA}=2h(l+b)=2\times 3\times(12+4)=96\text{ cm}^2$.

$\text{TSA}=2(lb+bh+hl)=2(48+12+36)=192\text{ cm}^2$.

$V=lbh=12\times 4\times 3=144\text{ cm}^3$.

Diagonal $=\sqrt{12^2+4^2+3^2}=\sqrt{144+16+9}=\sqrt{169}=13$ cm.
:::

::: example Painting a room
**Problem.** A hall is 10 m long, 8 m wide and 4 m high. It has one door $2.5\text{ m}\times 1.2\text{ m}$ and two windows each $1.5\text{ m}\times 1\text{ m}$. Find the cost of painting the four walls at Rs 15 per m².

**Solution.** Area of four walls $=2h(l+b)=2\times 4\times(10+8)=144\text{ m}^2$.

Door $=2.5\times 1.2=3\text{ m}^2$; two windows $=2\times 1.5\times 1=3\text{ m}^2$. Total opening $=6\text{ m}^2$.

Area to be painted $=144-6=138\text{ m}^2$.

Cost $=138\times 15=\text{Rs } 2{,}070$.
:::

::: example Water tank
**Problem.** A rectangular water tank is 2.5 m long, 2 m wide and 1.2 m deep. How many litres does it hold? How much sheet metal is needed for the tank, if it is open at the top?

**Solution.** $V=2.5\times 2\times 1.2=6\text{ m}^3=6\times 1000=6000$ litres.

Open tank: base $+$ four walls $=lb+2h(l+b)=2.5\times 2+2\times 1.2\times(2.5+2)=5+10.8=15.8\text{ m}^2$.
:::

### Triangular and other prisms

```figure caption="A triangular prism whose base is a right-angled triangle with sides 6, 8 and 10 cm, and length 15 cm. Dashed edges are hidden."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon
fig, ax = plt.subplots(figsize=(4.6, 2.7))
A = np.array([0, 0.0]); B = np.array([5, 0.0]); C = np.array([0, 3.75]); d = np.array([5.5, 2.2])
ax.add_patch(Polygon([A, B, C], fc='#dbeafe', ec=INK, lw=1.3))
ax.add_patch(Polygon([B, B+d, C+d, C], fc='#c7e0fb', ec='none', alpha=0.6))
for P, Q in [(B, B+d), (C, C+d), (B+d, C+d)]:
    ax.plot([P[0], Q[0]], [P[1], Q[1]], color=INK, lw=1.3)
for P, Q in [(A, A+d), (A+d, B+d), (A+d, C+d)]:
    ax.plot([P[0], Q[0]], [P[1], Q[1]], color=INK, lw=1.0, ls='--')
ax.text(2.5, -0.35, '8 cm', ha='center', va='top', fontsize=8.5)
ax.text(-0.2, 1.9, '6 cm', ha='right', va='center', fontsize=8.5)
ax.text(2.9, 2.35, '10 cm', ha='left', va='bottom', fontsize=8.5, rotation=-37)
ax.text(B[0] + d[0]/2 + 0.45, B[1] + d[1]/2 - 0.3, 'h = 15 cm', ha='left', va='center', fontsize=8.5, color=ACCENT)
ax.set_xlim(-1.6, 11.8); ax.set_ylim(-1.0, 6.4); ax.set_aspect('equal'); ax.axis('off')
```

::: example Triangular prism
**Problem.** The base of a prism is a right-angled triangle with sides 6 cm, 8 cm and 10 cm. The length of the prism is 15 cm. Find its lateral surface area, total surface area and volume.

**Solution.** Perimeter of base $P=6+8+10=24$ cm.

Area of base $A=\dfrac12\times 6\times 8=24\text{ cm}^2$.

$\text{LSA}=P\times h=24\times 15=360\text{ cm}^2$.

$\text{TSA}=360+2\times 24=408\text{ cm}^2$.

$V=A\times h=24\times 15=360\text{ cm}^3$.
:::

```figure caption="Net of the triangular prism: three rectangles (one for each side of the triangle) in a row, with a triangle at each end. Not to scale."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon
fig, ax = plt.subplots(figsize=(4.4, 3.2))
x = 0
for w, lab, col in [(8, '8 × h', '#dcfce7'), (6, '6 × h', '#fef3c7'), (10, '10 × h', '#fce7f3')]:
    ax.add_patch(Rectangle((x, 8), w, 8, fc=col, ec=INK, lw=1.1))
    ax.text(x + w/2, 12, lab, ha='center', va='center', fontsize=9)
    x += w
ax.add_patch(Polygon([(8, 16), (14, 16), (8, 24)], fc='#dbeafe', ec=INK, lw=1.1))
ax.text(10.0, 18.0, 'base', ha='center', va='center', fontsize=8.5)
ax.add_patch(Polygon([(8, 8), (14, 8), (8, 0)], fc='#dbeafe', ec=INK, lw=1.1))
ax.text(10.0, 6.0, 'base', ha='center', va='center', fontsize=8.5)
ax.text(12, -1.2, 'side faces: P × h', ha='center', va='top', fontsize=8.5)
ax.set_xlim(-1, 25); ax.set_ylim(-3, 25); ax.set_aspect('equal'); ax.axis('off')
```

::: example Prism with a trapezium base
**Problem.** A water trough has a trapezium cross-section with parallel sides 10 dm and 6 dm, the distance between them 4 dm, and slanting sides 5 dm each. The trough is 20 dm long. Find its volume in litres and its total surface area.

**Solution.** Area of base $A=\dfrac12(10+6)\times 4=32\text{ dm}^2$.

Volume $=A\times h=32\times 20=640\text{ dm}^3=640$ litres (1 dm³ $=1$ litre).

Perimeter of base $=10+6+5+5=26$ dm, so $\text{LSA}=26\times 20=520\text{ dm}^2$.

$\text{TSA}=520+2\times 32=584\text{ dm}^2$.
:::

::: caution Common mistakes
- Using the **slant side** of a trapezium or triangle as the height in the area formula. The base area needs the perpendicular height.
- Adding the two bases to the **lateral** surface area. LSA is the sides only.
- Writing the volume in cm² or the area in cm³. Area is square units; volume is cubic units.
- For an open tank, counting the top face as well.
:::

### Pyramids

::: definition Pyramid
A **pyramid** has a polygon as its base and triangular side faces that meet at a point called the **apex** (vertex). In a **right regular pyramid** the base is a regular polygon and the apex is directly above its centre. Two lengths matter:

- the **height** $h$ — perpendicular distance from the apex to the base;
- the **slant height** $l$ — the height of one triangular face, from the apex to the middle of a base edge.
:::

::: key Square pyramid (base side $a$)
$$ l^2=h^2+\left(\frac a2\right)^2 $$
$$ \text{LSA}=\frac12\times\text{(perimeter of base)}\times l=\frac12\times 4a\times l=2al $$
$$ \text{TSA}=\text{LSA}+a^2 \qquad V=\frac13\times a^2\times h $$
:::

```figure caption="A square pyramid with height h, slant height l and half the base edge a/2. The right-angled triangle V–O–M gives l² = h² + (a/2)²."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon
fig, ax = plt.subplots(figsize=(4.4, 3.2))
A = np.array([0, 0.0]); B = np.array([5, 0.0]); C = np.array([6.6, 1.8]); D = np.array([1.6, 1.8])
O = (A + C)/2; V = O + np.array([0, 4.6]); M = (A + B)/2
ax.add_patch(Polygon([V, M, O], fc='#fde68a', ec='none', alpha=0.7))
ax.add_patch(Polygon([A, B, C, D], fc='none', ec='none'))
for P, Q in [(A, B), (B, C), (V, A), (V, B), (V, C)]:
    ax.plot([P[0], Q[0]], [P[1], Q[1]], color=INK, lw=1.3)
for P, Q in [(A, D), (D, C), (V, D)]:
    ax.plot([P[0], Q[0]], [P[1], Q[1]], color=INK, lw=1.0, ls='--')
ax.plot([V[0], O[0]], [V[1], O[1]], color=ACCENT, lw=1.2, ls='--')
ax.plot([V[0], M[0]], [V[1], M[1]], color=SERIES[1], lw=1.4)
ax.plot([O[0], M[0]], [O[1], M[1]], color=ACCENT, lw=1.0, ls='--')
ax.text(O[0] + 0.15, (V[1] + O[1])/2 + 0.3, 'h', color=ACCENT, fontsize=9, ha='left')
ax.text((V[0] + M[0])/2 - 0.2, (V[1] + M[1])/2 - 0.5, 'l', color=SERIES[1], fontsize=9, ha='right')
ax.text(M[0] + 0.95, M[1] + 0.3, 'a/2', color=ACCENT, fontsize=8.5, ha='left', va='center')
ax.text(4.0, -0.35, 'a', fontsize=9, ha='center', va='top')
ax.text(V[0], V[1] + 0.25, 'V', fontsize=9, ha='center')
ax.text(O[0] + 0.2, O[1] + 0.15, 'O', fontsize=8.5, ha='left')
ax.text(M[0] - 0.05, M[1] - 0.2, 'M', fontsize=8.5, ha='center', va='top')
ax.set_xlim(-1.5, 8.6); ax.set_ylim(-1.2, 6.8); ax.set_aspect('equal'); ax.axis('off')
```

::: derivation Why the volume of a pyramid is one third of base times height
We show the rule for a special pyramid, using a cube; the rule is the same for every pyramid with the same base area and height.

**Setting up.** Take a cube of side $a$. Join its centre $O$ to the 8 vertices. The cube is cut into **six** identical square pyramids, each with a face of the cube as its base and $O$ as its apex.

**Step 1 — volume of the cube.** $V_{\text{cube}}=a^3$.

**Step 2 — volume of each pyramid.** The six pyramids are equal, so

$$ V_{\text{pyramid}}=\frac{a^3}{6} $$

**Step 3 — the base and height of one of them.** Base area $=a^2$ and the height (from $O$ to the face) $=\dfrac a2$.

**Step 4 — compare.**

$$ \frac13\times\text{base}\times\text{height}=\frac13\times a^2\times\frac a2=\frac{a^3}{6} $$

**Result.** $V=\dfrac13\times(\text{area of base})\times(\text{height})$.

**What it means.** A pyramid is exactly one third of the prism with the same base and height: three pyramids fill that prism. (Likewise a cone is one third of the cylinder.)
:::

::: example Slant height, surface area and volume
**Problem.** A square pyramid has base side 10 cm and slant height 13 cm. Find its height, lateral surface area, total surface area and volume.

**Solution.** Half the base side $=5$ cm.

$$ h=\sqrt{l^2-\left(\frac a2\right)^2}=\sqrt{13^2-5^2}=\sqrt{169-25}=\sqrt{144}=12\text{ cm} $$

$\text{LSA}=2al=2\times 10\times 13=260\text{ cm}^2$.

$\text{TSA}=260+10^2=360\text{ cm}^2$.

$V=\dfrac13\times 10^2\times 12=400\text{ cm}^3$.
:::

::: example Height given, find slant height
**Problem.** A square pyramid has base side 16 cm and height 6 cm. Find the slant height, TSA and volume.

**Solution.** Half the side $=8$ cm.

$$ l=\sqrt{h^2+\left(\frac a2\right)^2}=\sqrt{6^2+8^2}=\sqrt{100}=10\text{ cm} $$

$\text{LSA}=2al=2\times 16\times 10=320\text{ cm}^2$; $\text{TSA}=320+16^2=576\text{ cm}^2$.

$V=\dfrac13\times 256\times 6=512\text{ cm}^3$.
:::

::: example Finding the height from the volume
**Problem.** The volume of a square pyramid is 1,125 cm³ and its base side is 15 cm. Find its height.

**Solution.** $V=\dfrac13a^2h$:

$$ 1125=\frac13\times 225\times h=75h \;\Rightarrow\; h=\frac{1125}{75}=15\text{ cm} $$
:::

::: example A tent
**Problem.** A tent is in the shape of a square pyramid with base side 6 m and height 4 m. Find the cloth needed for its four sides (the floor is not covered), the cost at Rs 120 per m², and the volume of air inside.

**Solution.** $l=\sqrt{4^2+3^2}=\sqrt{25}=5$ m.

Cloth $=\text{LSA}=2al=2\times 6\times 5=60\text{ m}^2$.

Cost $=60\times 120=\text{Rs } 7{,}200$.

Volume of air $=\dfrac13\times 6^2\times 4=48\text{ m}^3$.
:::

::: example Recasting a cube into pyramids
**Problem.** A metal cube of side 6 cm is melted and recast into square pyramids of base side 6 cm and height 6 cm. How many pyramids are made?

**Solution.** Volume of cube $=6^3=216\text{ cm}^3$. Volume of one pyramid $=\dfrac13\times 6^2\times 6=72\text{ cm}^3$.

Number $=\dfrac{216}{72}=3$ pyramids.
:::

### The cone: a round pyramid

A **right circular cone** has a circular base of radius $r$, height $h$ and **slant height** $l$ along the surface from the apex to the rim of the base.

::: key Cone formulas
$$ l^2=r^2+h^2 \qquad \text{CSA}=\pi rl \qquad \text{TSA}=\pi r(r+l) \qquad V=\frac13\pi r^2h $$
:::

```figure caption="A right circular cone with radius r, height h and slant height l. The right-angled triangle gives l² = r² + h²."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon
fig, ax = plt.subplots(figsize=(4.0, 3.0))
r, h = 3.0, 6.0
ax.add_patch(Polygon([(-r, 0), (r, 0), (0, h)], fc='#dbeafe', ec='none'))
ax.add_patch(Ellipse((0, 0), 2*r, 1.2, fc='#bfdbfe', ec=INK, lw=1.2))
ax.plot([-r, 0], [0, h], color=INK, lw=1.3); ax.plot([r, 0], [0, h], color=INK, lw=1.3)
ax.plot([0, 0], [0, h], color=ACCENT, lw=1.2, ls='--')
ax.plot([0, r], [0, 0], color=ACCENT, lw=1.2)
ax.text(r/2, 0.12, 'r', color=ACCENT, fontsize=9, ha='center', va='bottom')
ax.text(-0.2, h/2, 'h', color=ACCENT, fontsize=9, ha='right', va='center')
ax.text(r/2 + 0.45, h/2 + 0.2, 'l', fontsize=9, ha='left', va='center')
ax.set_xlim(-4.4, 4.4); ax.set_ylim(-1.4, 6.8); ax.set_aspect('equal'); ax.axis('off')
```

::: example Cone
**Problem.** A cone has radius 7 cm and height 24 cm. Find its slant height, curved surface area, total surface area and volume.

**Solution.** $l=\sqrt{r^2+h^2}=\sqrt{49+576}=\sqrt{625}=25$ cm.

$\text{CSA}=\pi rl=\dfrac{22}{7}\times 7\times 25=550\text{ cm}^2$.

$\text{TSA}=\pi r(r+l)=\dfrac{22}{7}\times 7\times 32=704\text{ cm}^2$.

$V=\dfrac13\pi r^2h=\dfrac13\times\dfrac{22}{7}\times 49\times 24=1232\text{ cm}^3$.
:::

::: tip Always draw the right-angled triangle
In a pyramid or a cone, the **height**, the **slant height** and the **half-base** (or radius) form a right-angled triangle with the slant height as hypotenuse. Sketch it and apply Pythagoras before anything else. The usual Pythagorean triples are $(3,4,5)$, $(5,12,13)$, $(8,15,17)$, $(7,24,25)$ and their multiples.
:::

## 7.2 Exercises of the SEE type

### Method

1. Identify the solid (prism, pyramid, cone). Draw it and mark every length.
2. Prism: find the base area $A$ and base perimeter $P$; then LSA $=Ph$, TSA $=Ph+2A$, $V=Ah$.
3. Pyramid or cone: find $l$ by Pythagoras from $h$ (or $h$ from $l$).
4. Use the formula; keep fractions such as $\frac13$ until the end.
5. For cost questions multiply the area by the rate; for capacity convert to litres.
6. Write each answer with the correct unit (square for area, cube for volume).

## Chapter summary

- Right prism: LSA $=Ph$, TSA $=Ph+2A$, $V=Ah$ ($P$ base perimeter, $A$ base area).
- Cuboid: LSA $=2h(l+b)$, TSA $=2(lb+bh+hl)$, $V=lbh$, diagonal $=\sqrt{l^2+b^2+h^2}$.
- Cube: TSA $=6a^2$, $V=a^3$.
- Square pyramid: $l^2=h^2+(\frac a2)^2$, LSA $=2al$, TSA $=2al+a^2$, $V=\frac13a^2h$.
- A pyramid is one third of the prism with the same base and height.
- Cone: $l^2=r^2+h^2$, CSA $=\pi rl$, TSA $=\pi r(r+l)$, $V=\frac13\pi r^2h$.
- 1 dm³ $=1$ litre; 1 m³ $=1000$ litres.
- The four walls of a room: $2h(l+b)$ minus the doors and windows.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The volume of a prism is <span class="marks">[1]</span>
   (a) perimeter of base $\times$ height (b) area of base $\times$ height (c) $\frac13\times$ area of base $\times$ height (d) $2\times$ area of base $\times$ height
2. The volume of a pyramid is <span class="marks">[1]</span>
   (a) base area $\times$ height (b) $\frac12\times$ base area $\times$ height (c) $\frac13\times$ base area $\times$ height (d) $\frac14\times$ base area $\times$ height
3. The area of the four walls of a room of length $l$, breadth $b$ and height $h$ is <span class="marks">[1]</span>
   (a) $lbh$ (b) $2(lb+bh+hl)$ (c) $2h(l+b)$ (d) $2lb$
4. The slant height of a square pyramid of base side 10 cm and height 12 cm is <span class="marks">[1]</span>
   (a) 11 cm (b) 13 cm (c) 15 cm (d) 22 cm
5. The total surface area of a cube of side 6 cm is <span class="marks">[1]</span>
   (a) 36 cm² (b) 144 cm² (c) 216 cm² (d) 72 cm²

::: note Answers to Group A
**1.** (b) — $V=A\times h$.
**2.** (c) — one third of the matching prism.
**3.** (c) — LSA of a cuboid.
**4.** (b) — $\sqrt{12^2+5^2}=13$.
**5.** (c) — $6\times 36=216$.
:::

**Group B — Short answer (2 marks each)**

1. Find the volume of a cuboid 10 cm by 6 cm by 4 cm. <span class="marks">[2]</span>
2. The base of a prism has area 24 cm² and the prism is 15 cm long. Find its volume. <span class="marks">[2]</span>
3. Find the volume of a square pyramid of base side 6 cm and height 4 cm. <span class="marks">[2]</span>
4. Find the slant height of a square pyramid of base side 24 cm and height 9 cm. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** $10\times 6\times 4=240\text{ cm}^3$.
**2.** $24\times 15=360\text{ cm}^3$.
**3.** $\frac13\times 36\times 4=48\text{ cm}^3$.
**4.** $l=\sqrt{9^2+12^2}=\sqrt{225}=15$ cm.
:::

**Group C — Short answer (3 marks each)**

1. A room is 8 m long, 6 m wide and 3 m high. Find the cost of whitewashing its four walls and ceiling at Rs 20 per m². <span class="marks">[3]</span>
2. A square pyramid has base side 10 cm and slant height 13 cm. Find its lateral and total surface areas. <span class="marks">[3]</span>
3. A square pyramid has a volume of 1,125 cm³ and a base side of 15 cm. Find its height. <span class="marks">[3]</span>
4. A cone has radius 7 cm and slant height 25 cm. Find its curved surface area, and its volume given that the height is 24 cm. <span class="marks">[3]</span>

::: note Answers to Group C
**1.** Four walls $=2\times 3\times(8+6)=84\text{ m}^2$; ceiling $=8\times 6=48\text{ m}^2$; total $=132\text{ m}^2$. Cost $=132\times 20=\text{Rs } 2{,}640$.
**2.** LSA $=2al=2\times 10\times 13=260\text{ cm}^2$; TSA $=260+100=360\text{ cm}^2$.
**3.** $1125=\frac13\times 225\times h=75h$, so $h=15$ cm.
**4.** CSA $=\pi rl=\frac{22}{7}\times 7\times 25=550\text{ cm}^2$. $V=\frac13\times\frac{22}{7}\times 49\times 24=1232\text{ cm}^3$.
:::

**Group D — Long answer (4 marks each)**

1. The base of a prism is a right-angled triangle with sides 5 cm, 12 cm and 13 cm. The prism is 20 cm long. Find its lateral surface area, total surface area and volume. <span class="marks">[4]</span>
2. A square pyramid has a base side of 16 cm and a height of 6 cm. Find its slant height, total surface area and volume. <span class="marks">[4]</span>
3. A tent is a square pyramid with base side 6 m and height 4 m. Find the cost of the cloth for its four sides at Rs 120 per m², and the volume of air inside. <span class="marks">[4]</span>
4. A trough has a trapezium cross-section with parallel sides 10 dm and 6 dm, height 4 dm and slant sides 5 dm. It is 20 dm long. Find its capacity in litres and its total surface area. <span class="marks">[4]</span>

::: note Answers to Group D
**1.** $P=5+12+13=30$ cm; $A=\frac12\times 5\times 12=30\text{ cm}^2$. LSA $=30\times 20=600\text{ cm}^2$; TSA $=600+60=660\text{ cm}^2$; $V=30\times 20=600\text{ cm}^3$.
**2.** $l=\sqrt{6^2+8^2}=10$ cm. LSA $=2\times 16\times 10=320$; TSA $=320+256=576\text{ cm}^2$. $V=\frac13\times 256\times 6=512\text{ cm}^3$.
**3.** $l=\sqrt{4^2+3^2}=5$ m. Cloth $=2\times 6\times 5=60\text{ m}^2$; cost $=60\times 120=\text{Rs } 7{,}200$. Air $=\frac13\times 36\times 4=48\text{ m}^3$.
**4.** $A=\frac12(10+6)\times 4=32\text{ dm}^2$; $V=32\times 20=640\text{ dm}^3=640$ litres. LSA $=(10+6+5+5)\times 20=520$; TSA $=520+64=584\text{ dm}^2$.
:::
