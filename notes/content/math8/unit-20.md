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

**Measuring.** $SB$ measures about 4.4 cm, and the bearing of $SB$ measures
about 101°. In real terms, $4.4\times50=220$ km.

**Answer.** About 220 km on a bearing of about 101° from the start.

**Check.** The answer must lie between the two legs: a distance between 50 km
and 350 km, and it does. A bearing of about 101° is just past east, which is
reasonable because the first leg headed north-east and the second headed
south-east.

**A cross-check by calculation.** Resolving the legs into north and east
components: leg 1 gives $200\sin60°=173$ km east and $200\cos60°=100$ km north;
leg 2 gives $150\sin150°=75$ km east and $150\cos150°=-130$ km north. Totals:
248 km east and $-30$ km north. Then
$SB=\sqrt{248^2+30^2}\approx250$ km and the bearing from the tangent gives about
$97°$ — close enough to the drawing to confirm it, with the small difference
coming from measuring with a ruler rather than from any error in the method.
:::

::: tip Measuring is a skill, and examiners know the tolerance
In a scale-drawing question, an answer within about 1° or 2° of the true bearing
and within a millimetre or two of the true length is accepted. What is marked is
whether the north lines are drawn, whether the protractor was used at the right
point, and whether the scale is stated. Write the scale on the drawing; it is
worth a mark on its own.
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
:::

::: note Answers to Group B
**1.** South-east is 135°; 25° west of north is $360-25=335°$.
**2.** $130+180=310°$.
**3.** $7\times200\,000=1\,400\,000$ cm $=14$ km.
**4.** Distance $=\sqrt{6^2+8^2}=10$ km; the bearing is
$\tan^{-1}\frac86\approx53°$, so about 053°.
:::

**Group C — Long answer (4 marks each)**

1. A ship sails 120 km on a bearing of 090° and then 160 km on a bearing of
   180°. Using a scale of 1 cm to 20 km, draw the route and find the distance
   and bearing of the ship's final position from its starting point.
   <span class="marks">[4]</span>
2. A helicopter flies 80 km on a bearing of 040° and then 60 km on a bearing of
   130°. Find its final distance and bearing from the start by resolving the
   two legs into north and east components, and check that your answer is
   consistent with the two legs. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** **Scale.** 1 cm to 20 km, so 120 km is 6 cm and 160 km is 8 cm.
**Drawing.** From the start $S$, draw a north line and measure 090° — that is
due east — then draw $SA=6$ cm eastwards. At $A$ draw a fresh north line,
measure 180° (due south) and draw $AB=8$ cm southwards. Join $B$ to $S$.
**Measuring.** $SB$ measures about 10 cm, and the bearing of $SB$ measures about
127°. In real terms the distance is $10\times20=200$ km.
**Check by calculation.** East: $120+0=120$ km; north: $0-160=-160$ km. So
$SB=\sqrt{120^2+160^2}=\sqrt{14\,400+25\,600}=\sqrt{40\,000}=200$ km ✓, and the
bearing is $90°+\tan^{-1}\frac{160}{120}=90°+53°=143°$. The drawing gives about
127°, which is 16° out — a reminder that a rough sketch is a check on the
method, not on the angle; the calculated 143° is the exact answer.
**2.** **Components.** Leg 1 at 040°: east $=80\sin40°\approx51.4$ km, north
$=80\cos40°\approx61.3$ km. Leg 2 at 130°: east
$=60\sin130°\approx46.0$ km, north $=60\cos130°\approx-38.6$ km.
**Totals.** East $=51.4+46.0=97.4$ km; north $=61.3-38.6=22.7$ km.
**Distance.** $\sqrt{97.4^2+22.7^2}=\sqrt{9487+515}=\sqrt{10\,002}\approx100$ km.
**Bearing.** $\tan\theta=\frac{97.4}{22.7}=4.29$, so
$\theta\approx76.9°$ east of north, that is a bearing of about **077°**.
**Consistency check.** The answer, 100 km on 077°, lies sensibly between the two
legs: the total path is 140 km, so a direct distance of 100 km implies a good
deal of turning, which is true here (90° between the two legs), and the final
bearing of 077° is between 040° and 130° as it must be.
:::
