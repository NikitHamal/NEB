---
subject: Mathematics
grade: 8
title: Bearing and Scale Drawing
unit: 20
hours: 0
area: Compulsory Mathematics
---

A bearing is a way of writing a direction as a single number, so that there is
no argument about what "north-east" means. A scale drawing is a way of putting
several such directions and distances on one sheet of paper, to scale. Together
they are the mathematics of a trekking route, a flight path and a surveyor's
notebook.

::: key What this chapter asks of you
You should be able to write and read a three-figure bearing, find the back
bearing, draw a scale drawing from a description of distances and bearings, and
measure a distance or a bearing from a drawing.
:::

## 20.1 Bearing

A **bearing** is the angle measured **clockwise from north**, written with three
figures. So 060° means 60° clockwise from north, and 275° means 275° clockwise
from north.

Because a bearing is measured from north and is always positive, it carries the
direction without any words.

| Direction | Bearing | Why |
|---|---|---|
| North | 000° | at the start of the turn |
| East | 090° | a quarter turn clockwise |
| South | 180° | a half turn |
| West | 270° | three quarters |
| North-east | 045° | halfway between north and east |
| South-west | 225° | halfway between south and west |

Three figures are written even for small angles: north is **000°**, not 0°, and
8° is **008°**. Writing three figures is a convention that stops 8° being
confused with 80°.

::: definition Bearing
A **bearing** is the angle, measured clockwise from the north line, from one
point to another. It is always given in three figures, from 000° to 360°.
:::

::: example Reading directions as bearings
**Problem.** Write as bearings: (a) due west, (b) 30° east of north, (c) 40°
west of south.

**Solution.** (a) West is three quarters of a turn clockwise from north, so
**270°**.

(b) 30° east of north means starting at north and turning 30° towards the east,
i.e. clockwise: **030°**.

(c) From south, turning towards the west means turning further clockwise. South
is 180°, and 40° more gives **220°**.

**Check.** (c) is between south (180°) and west (270°), which is right for a
south-westerly direction ✓. If you had measured anticlockwise from south you
would have written 140°, which points south-east — the opposite side.
:::

### 20.1.1 Back bearing

The **back bearing** is the bearing from the second point back to the first. It
is found by adding 180° if the bearing is less than 180°, and subtracting 180°
if it is more.

$$\text{back bearing}=\text{bearing}\pm180°$$

**Why ±180°?** Let the bearing of S from R be $\theta$. The north lines at R
and S are parallel and RS is a transversal, so the angles $\angle N_1RS$ and
$\angle N_2SR$ are co-interior and add to 180°. Measuring clockwise from north
at S, the bearing of R from S is $360°-\angle N_2SR=360°-(180°-\theta)=\theta+180°$
(subtract 360° if this is more than 360°).

::: example Back bearing
**Problem.** A village $B$ is on a bearing of 065° from village $A$. Find the
bearing of $A$ from $B$.

**Solution.** 065° is less than 180°, so add 180°:

$$065°+180°=245°$$

**Answer.** 245°.

**Check.** The two directions must point exactly opposite each other, and 245°
is 180° round from 065° ✓. The distances are the same in both directions, so
only the direction changes.
:::

::: example A bearing greater than 180°
**Problem.** $Q$ is on a bearing of 300° from $P$. Find the bearing of $P$ from
$Q$.

**Solution.** 300° is more than 180°, so subtract 180°:
$300-180=120°$.

**Answer.** 120°.

**Check.** $120+180=300$ ✓. The rule works in both directions.
:::

## 20.2 Scale drawing

A **scale drawing** is a drawing in which every length on the paper is a fixed
fraction of the real length. The fraction is the **scale**, written as a ratio
such as $1:50\,000$ ("1 cm on the paper represents 50 000 cm on the ground") or
in words such as "1 cm to 1 km".

$$\text{scale}=\frac{\text{drawing length}}{\text{real length}}$$

Keep one unit throughout: convert the real distance to the same unit as the
drawing before dividing.

| Real distance | Scale | Drawing length |
|---|---|---|
| 5 km | 1 cm to 1 km | 5 cm |
| 2 500 m | 1 cm to 500 m | 5 cm |
| 60 km | $1:1\,000\,000$ | 6 cm |

::: example Converting a distance to a drawing length
**Problem.** The distance between two towns is 24 km. On a map of scale
$1:400\,000$, how far apart are they?

**Solution.** The scale means 1 cm on the map is 400 000 cm on the ground.

$$400\,000\text{ cm}=4\text{ km}$$

So 1 cm represents 4 km, and 24 km is represented by

$$\frac{24}{4}=6\text{ cm}$$

**Answer.** 6 cm.

**Check.** $6\ \text{cm}\times400\,000=2\,400\,000$ cm $=24$ km ✓.
:::

### 20.2.1 Drawing a route from bearings

**Method.**

1. Choose a scale that will fit the page, and write it on the drawing.
2. Mark the starting point and draw a north line through it.
3. Measure the first bearing clockwise from the north line with a protractor,
   and draw the first leg to the correct scaled length.
4. At the end of that leg, draw a NEW north line (parallel to the first) and
   measure the next bearing from it. Every leg gets its own north line.
5. Join the finishing point to the start to find the direct distance and its
   bearing.

::: caution The north line must be redrawn at every point
A bearing is measured from north **at the point you are standing on**. At each
new point the north line is a fresh parallel line, not the same line carried
along. Measuring the second bearing from the first north line gives a route that
curves away from the truth by whatever angle the first leg turned through.
:::

::: example A two-leg route
**Problem.** A plane flies 200 km on a bearing of 060° and then 150 km on a
bearing of 150°. Using a scale of 1 cm to 50 km, draw the route, and measure the
distance and the bearing of the finishing point from the start.

**Solution.** **Scale.** 1 cm to 50 km, so 200 km is 4 cm and 150 km is 3 cm.

**Drawing.** Mark the start $S$ and a north line. Measure 60° clockwise and draw
$SA=4$ cm. At $A$ draw a fresh north line, measure 150° clockwise from it and
draw $AB=3$ cm. Join $B$ back to $S$.

**Measuring.** $SB$ measures about 5.0 cm, and the bearing of $B$ from $S$
(measured clockwise from the north line at $S$) is about 097°. In real terms,
$5.0\times50=250$ km.

**Answer.** About 250 km on a bearing of about 097° from the start.

**Check.** The two legs turn through $150°-60°=90°$, so the triangle $SAB$ has
a right angle at $A$. By Pythagoras,
$SB=\sqrt{200^2+150^2}=\sqrt{62\,500}=250$ km ✓. The bearing 097° lies between
060° and 150°, as it must.
:::

```figure caption="Scale drawing of the two-leg flight (1 cm to 50 km): SA = 4 cm on 060°, then AB = 3 cm on 150° measured from a new north line at A. SB measures 5 cm (250 km) on a bearing of about 097°."
fig, ax = plt.subplots(figsize=(4.6, 3.0))
from matplotlib.patches import Arc
S = np.array([0.0, 0.0]); A = S + 4 * np.array([np.sin(np.radians(60)), np.cos(np.radians(60))])
B = A + 3 * np.array([np.sin(np.radians(150)), np.cos(np.radians(150))])
for P in (S, A):
    ax.annotate("", xy=(P[0], P[1] + 1.3), xytext=(P[0], P[1]), arrowprops=dict(arrowstyle="->", color=MUTED, lw=1))
    ax.text(P[0] - 0.1, P[1] + 1.4, "N", fontsize=8.5, color=MUTED)
ax.plot([S[0], A[0]], [S[1], A[1]], color=ACCENT, lw=1.6)
ax.plot([A[0], B[0]], [A[1], B[1]], color=SERIES[1], lw=1.6)
ax.plot([S[0], B[0]], [S[1], B[1]], color=INK, lw=1.2, ls="--")
ax.add_patch(Arc(S, 1.2, 1.2, theta1=30, theta2=90, color=ACCENT, lw=1))
ax.add_patch(Arc(A, 1.0, 1.0, theta1=-60, theta2=90, color=SERIES[1], lw=1))
ax.text(0.25, 0.75, "60°", fontsize=8.5, color=ACCENT)
ax.text(A[0] + 0.55, A[1] + 0.05, "150°", fontsize=8.5, color=SERIES[1])
for P, t, off in [(S, "S", (-0.35, -0.2)), (A, "A", (-0.35, 0.05)), (B, "B", (0.1, -0.3))]:
    ax.text(P[0] + off[0], P[1] + off[1], t, fontsize=10, color=INK)
ax.text(1.4, 1.35, "4 cm", fontsize=8.5, color=ACCENT, rotation=30)
ax.text(4.4, 0.9, "3 cm", fontsize=8.5, color=SERIES[1])
ax.text(2.2, -0.55, "5 cm", fontsize=8.5, color=INK)
ax.set_xlim(-0.8, 6.0); ax.set_ylim(-0.9, 3.6); ax.set_aspect("equal"); ax.axis("off")
```

::: tip Measuring is a skill, and examiners know the tolerance
In a scale-drawing question, an answer within about 1° or 2° of the true bearing
and within a millimetre or two of the true length is accepted. What is marked is
whether the north lines are drawn, whether the protractor was used at the right
point, and whether the scale is stated. Write the scale on the drawing; it is
worth a mark on its own.
:::

## 20.3 Bearings on the compass rose

A bearing is always measured **clockwise from north** and written with
**three figures**: $045°$, not $45°$.

```figure caption="The compass rose with the four cardinal and four intercardinal bearings. The back bearing of any direction differs by 180 degrees."
import math
fig, ax = plt.subplots(figsize=(4.0, 3.8))
pts = [("N  000°", 0), ("NE  045°", 45), ("E  090°", 90), ("SE  135°", 135),
       ("S  180°", 180), ("SW  225°", 225), ("W  270°", 270),
       ("NW  315°", 315)]
for lab, b in pts:
    a = math.radians(90 - b)
    x, y = 0.5 + 0.36 * math.cos(a), 0.5 + 0.36 * math.sin(a)
    ax.annotate("", xy=(x, y), xytext=(0.5, 0.5),
                arrowprops=dict(arrowstyle="-|>", color=SERIES[b // 45 % 6],
                                lw=1.3))
    ax.text(0.5 + 0.455 * math.cos(a), 0.5 + 0.455 * math.sin(a), lab,
            ha="center", va="center", color=INK, fontsize=7.6)
ax.add_patch(matplotlib.patches.Circle((0.5, 0.5), 0.36, facecolor="none",
                                       edgecolor=GRID, linewidth=1.0))
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_aspect("equal")
ax.axis("off")
```

| Idea | Rule | Example |
|---|---|---|
| Bearing | clockwise from north, three figures | due east $= 090°$ |
| Back bearing | add $180°$ (subtract if the sum exceeds $360°$) | bearing $070° \to$ back bearing $250°$ |
| Scale as a ratio | $1 : n$ means 1 unit on the map is $n$ units on the ground | $1 : 50{,}000$ |
| Map to ground | ground $=$ map length $\times n$ | 4 cm on $1:25{,}000 = 1$ km |
| Ground to map | map $=$ ground length $\div n$ | 3 km on $1:50{,}000 = 6$ cm |

::: example Bearing and back bearing
**Question.** A village B lies on a bearing of $130°$ from A. What is the
bearing of A from B?

**Answer.** Back bearing $= 130° + 180° = \textbf{310°}$.
(If the first bearing had been more than $180°$, we would subtract instead: the
back bearing of $250°$ is $250° - 180° = 070°$.)
:::

::: example Scale drawing
**Question.** On a map of scale $1:40{,}000$, two towns are 6.5 cm apart. Find
the real distance in kilometres. How far apart would they be on a $1:25{,}000$
map?

**Answer.** Real distance $= 6.5 \times 40{,}000 = 260{,}000$ cm $= \textbf{2.6
km}$.
On the $1:25{,}000$ map: $\frac{260000}{25000} = \textbf{10.4 cm}$ — a larger
scale gives a bigger picture of the same ground.
:::

::: note Activity — map your route to school
Pace out the route from your home to school, counting paces for each straight
stretch and noting the bearing at each turn with a compass (or a compass app).
Then draw the route to a scale of 1 cm to 50 m, marking each bearing.
**Check:** measure the straight-line distance on your drawing and convert it
back to metres. How does it compare with the distance you actually walk?
:::

## Chapter summary

- A bearing is measured clockwise from north and written in three figures, from
  000° to 360°.
- North 000°, east 090°, south 180°, west 270°.
- The back bearing is the bearing ± 180°: add 180° if the bearing is under 180°,
  subtract 180° if it is over.
- $\text{scale}=\frac{\text{drawing length}}{\text{real length}}$, and one unit
  must be used throughout.
- In a scale drawing a fresh north line is drawn at every point before the next
  bearing is measured.
- State the scale on the drawing; it earns a mark and it makes the drawing
  readable.

## Practice questions

**Group A — Objective (1 mark each)**

1. The bearing of east is <span class="marks">[1]</span>
   (a) 000° (b) 090° (c) 180° (d) 270°
2. The bearing of north-west is <span class="marks">[1]</span>
   (a) 045° (b) 135° (c) 225° (d) 315°
3. Bearings are measured from <span class="marks">[1]</span>
   (a) east, clockwise (b) north, clockwise (c) north, anticlockwise
   (d) south, clockwise
4. The back bearing of 070° is <span class="marks">[1]</span>
   (a) 110° (b) 250° (c) 290° (d) 160°
5. On a scale of 1 cm to 2 km, 10 km is drawn as
   <span class="marks">[1]</span>
   (a) 2 cm (b) 5 cm (c) 10 cm (d) 20 cm
6. A bearing of 8° should be written as <span class="marks">[1]</span>
   (a) 8° (b) 080° (c) 008° (d) 800°

::: note Answers to Group A
**1.** (b) — a quarter turn clockwise from north.
**2.** (d) — north-west is halfway between north (000°) and west (270°), so 315°.
**3.** (b) — from north, clockwise.
**4.** (b) — $70+180=250$.
**5.** (b) — $10\div2=5$.
**6.** (c) — three figures.
:::

**Group B — Short answer (2 marks each)**

1. Write the bearings of south-east and of 25° west of north.
   <span class="marks">[2]</span>
2. The bearing of $B$ from $A$ is 130°. Find the bearing of $A$ from $B$.
   <span class="marks">[2]</span>
3. On a map of scale $1:200\,000$, two places are 7 cm apart. Find the real
   distance in kilometres. <span class="marks">[2]</span>
4. A walker goes 6 km north and then 8 km east. Find his distance and bearing
   from the start. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** South-east is 135°; 25° west of north is $360-25=335°$.
**2.** $130+180=310°$.
**3.** $7\times200\,000=1\,400\,000$ cm $=14$ km.
**4.** The two legs are at right angles, so distance $=\sqrt{6^2+8^2}=10$ km.
From a scale drawing (say 1 cm to 1 km), the protractor gives a bearing of
about 053°.
:::

**Group C — Long answer (4 marks each)**

1. A ship sails 120 km on a bearing of 090° and then 160 km on a bearing of
   180°. Using a scale of 1 cm to 20 km, draw the route and find the distance
   and bearing of the ship's final position from its starting point.
   <span class="marks">[4]</span>
2. Madhav walks 5 km on a bearing of 030° from A to B, then 3 km on a bearing
   of 140° from B to C, and then returns straight to A. Make a scale drawing
   (1 cm to 1 km), and find the distance CA and the bearing of A from C.
   <span class="marks">[4]</span>

::: note Answers to Group C
**1.** **Scale.** 1 cm to 20 km, so 120 km is 6 cm and 160 km is 8 cm.
**Drawing.** From the start $S$ draw a north line, turn 090° (due east) and draw
$SA=6$ cm. At $A$ draw a fresh north line, turn 180° (due south) and draw
$AB=8$ cm. Join $B$ to $S$.
**Distance.** The angle at $A$ is 90°, so $SB=\sqrt{6^2+8^2}=10$ cm on the
drawing, i.e. $10\times20=200$ km.
**Bearing.** The protractor at $S$ gives about 143°.
**Check.** B is east and south of S, so its bearing must lie between 090° and
180° ✓.
**2.** **Scale.** 5 km → 5 cm, 3 km → 3 cm. Draw the north line at A, turn 030°
and draw AB = 5 cm; at B draw a new north line, turn 140° and draw BC = 3 cm;
join CA.
**Measurements.** CA ≈ 4.9 cm, so the actual distance is about 4.9 km. At C
draw a north line; the bearing of A from C measures about 245°.
**Check.** A lies to the south-west of C, so the bearing must be between 180°
and 270° ✓; and CA must be less than $5+3=8$ km ✓.
:::

**Extra practice**

**Group B (2 marks)**

**11.** Write the bearing of due south-west and its back bearing.
**12.** On a $1:20{,}000$ map, how long is a 3 km road?

**Group C (4 marks)**

**13.** A boat sails 8 km on a bearing of $090°$, then 6 km on a bearing of $000°$.
    Draw a rough sketch, and find its distance from the starting point.

::: note Extra practice — answers
**11.** South-west $= 225°$; back bearing $= 225° - 180° = 045°$.
**12.** $3$ km $= 300{,}000$ cm; map length $= \frac{300000}{20000} = 15$ cm.
**13.** The two legs are at right angles (east then north), so the path forms a
right-angled triangle with legs 8 km and 6 km.
Distance $= \sqrt{8^2 + 6^2} = \sqrt{64 + 36} = \sqrt{100} = \textbf{10 km}$
from the start.
:::

## Objective practice

**Choose the correct answer.** <span class="marks">[5×1=5]</span>

**1.** The bearing of due north is written as
   (a) $0°$ (b) $000°$ (c) $360°$ only (d) $090°$
**2.** The back bearing of $065°$ is
   (a) $115°$ (b) $245°$ (c) $295°$ (d) $025°$
**3.** On a map of scale $1:50{,}000$, 4 cm represents
   (a) 200 m (b) 2 km (c) 20 km (d) 50 km
**4.** A bearing is always measured
   (a) anticlockwise from north (b) clockwise from north (c) clockwise from east (d) from the nearest road
**5.** A distance of 7.5 km on a $1:25{,}000$ map is
   (a) 3 cm (b) 15 cm (c) 30 cm (d) 75 cm

::: note Objective practice — answers
**1.** (b) — bearings use three figures. **2.** (b) — $065° + 180° = 245°$. **3.** (b) — $4 \times 50{,}000 = 200{,}000$ cm $= 2$ km. **4.** (b) — clockwise from north. **5.** (c) — $750{,}000 \div 25{,}000 = 30$ cm.
:::
