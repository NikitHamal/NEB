---
subject: Mathematics
grade: 8
title: Congruency and Similarity
unit: 15
hours: 0
area: Compulsory Mathematics
---

Two figures are **congruent** when they are exactly the same shape and the same
size, so that one can be placed on the other and fit perfectly. They are
**similar** when they are the same shape but not necessarily the same size, so
that one is an enlargement of the other. Both ideas are tests: given a few
measurements, they let you say that two triangles must match without measuring
everything.

::: key What this chapter asks of you
You should be able to state the five tests of congruence (SSS, SAS, ASA, AAS, RHS),
the conditions for two triangles to be similar, use corresponding parts of
congruent triangles in a proof, and use the ratio of areas and sides of similar
triangles.
:::

## 15.1 Congruent figures

Two figures are **congruent** if they have exactly the same shape and size.
When triangles $ABC$ and $PQR$ are congruent we write

$$\triangle ABC\cong\triangle PQR$$

and the order of the letters matters: it tells you which vertex matches which.
So $A$ matches $P$, $B$ matches $Q$ and $C$ matches $R$, and therefore
$AB=PQ$, $BC=QR$, $CA=RP$, and the corresponding angles are equal.

**Corresponding parts of congruent triangles are equal** — usually written
CPCTC, and used as the reason in every proof of this chapter.

::: caution The order of the letters is information
$\triangle ABC\cong\triangle PQR$ says $AB$ corresponds to $PQ$. If the
congruence is really with $\triangle QRP$, then $AB$ corresponds to $QR$ and the
statement is false as written. Examiners deduct for a wrong order even when the
figure is right.
:::

## 15.2 The tests of congruence

To prove two triangles congruent you need only three matched facts, and the
three must be in one of these five patterns.

| Test | What must match | Why it works |
|---|---|---|
| SSS | all three sides | only one triangle can be built from three given sides |
| SAS | two sides and the **included** angle | the angle fixes the shape between the sides |
| ASA | two angles and the side **between** them | the side and the two angles at its ends fix the triangle |
| AAS | two angles and a side **not** between them | the third angle is forced (angles add to 180°), so it becomes ASA |
| RHS | a right angle, the hypotenuse and one other side | in a right triangle the third side follows by Pythagoras |

```figure caption="The five tests of congruence. The thick blue sides and the red arcs are the parts that must be equal in the two triangles. In SAS the angle lies between the two sides; in ASA the side lies between the two angles; in AAS the side does not."
from matplotlib.patches import Arc
fig, axs = plt.subplots(2, 3, figsize=(5.2, 3.6))
A, B, C = np.array([0.0, 0.0]), np.array([3.0, 0.0]), np.array([1.1, 2.0])
R1, R2, R3 = np.array([0.0, 0.0]), np.array([3.0, 0.0]), np.array([0.0, 2.0])
def ang(ax, V, P, Q, r=0.45):
    a1 = np.degrees(np.arctan2(*(P - V)[::-1])); a2 = np.degrees(np.arctan2(*(Q - V)[::-1]))
    lo, hi = sorted([a1, a2])
    if hi - lo > 180: lo, hi = hi, lo + 360
    ax.add_patch(Arc(V, 2*r, 2*r, theta1=lo, theta2=hi, color=SERIES[1], lw=1.6))
def draw(ax, P, sides, angles, title, sub):
    X, Y, Z = P
    pts = {"a": (X, Y), "b": (Y, Z), "c": (Z, X)}
    for k, (u, v) in pts.items():
        ax.plot([u[0], v[0]], [u[1], v[1]], color=ACCENT if k in sides else MUTED, lw=2.6 if k in sides else 1.0)
    for V, P1, P2 in angles:
        ang(ax, V, P1, P2)
    ax.text(1.5, -0.55, title, ha="center", fontsize=9, color=INK, weight="bold")
    ax.text(1.5, -1.05, sub, ha="center", fontsize=7.5, color=MUTED)
    ax.set_xlim(-0.3, 3.3); ax.set_ylim(-1.3, 2.3); ax.set_aspect("equal"); ax.axis("off")
draw(axs[0, 0], (A, B, C), "abc", [], "SSS", "three sides")
draw(axs[0, 1], (A, B, C), "ac", [(A, B, C)], "SAS", "two sides, included angle")
draw(axs[0, 2], (A, B, C), "a", [(A, B, C), (B, A, C)], "ASA", "two angles, side between")
draw(axs[1, 0], (A, B, C), "b", [(A, B, C), (B, A, C)], "AAS", "two angles, side not between")
draw(axs[1, 1], (R1, R2, R3), "ab", [], "RHS", "right angle, hypotenuse, side")
axs[1, 1].plot([0, 0.3, 0.3], [0.3, 0.3, 0], color=SERIES[1], lw=1.2)
axs[1, 2].axis("off")
fig.tight_layout()
```

::: caution There is no SSA test
Two sides and a **non-included** angle do **not** fix a triangle: two different
triangles can often be drawn with the same two sides and the same angle
somewhere else. Congruence must be proved with SSS, SAS, ASA, AAS or RHS — never with
"SSA", which does not exist.
:::

::: example A congruence proof
**Problem.** In the figure, $AB=AC$ and $D$ is the midpoint of $BC$. Prove that
$\triangle ABD\cong\triangle ACD$, and hence that $AD$ is perpendicular to
$BC$.

**Solution.**

**Given.** $AB=AC$ and $BD=DC$ ($D$ is the midpoint).

**To prove.** $\triangle ABD\cong\triangle ACD$ and $\angle ADB=90°$.

**Proof.**

| Statement | Reason |
|---|---|
| $AB=AC$ | given |
| $BD=DC$ | $D$ is the midpoint of $BC$ |
| $AD=AD$ | common side |
| $\triangle ABD\cong\triangle ACD$ | SSS |
| $\angle ADB=\angle ADC$ | corresponding parts of congruent triangles |

Now $\angle ADB+\angle ADC=180°$, because $BDC$ is a straight line. Equal
angles adding to 180° are each 90°, so $\angle ADB=90°$ and therefore $AD\perp
BC$. ∎

**What it shows.** In an isosceles triangle the line from the apex to the
midpoint of the base is perpendicular to the base — and it also bisects the apex
angle, since it makes the two triangles congruent.
:::

::: example A proof using ASA
**Problem.** Two triangles have $\angle B=\angle Q$, $\angle C=\angle R$ and
$BC=QR$. Prove the triangles congruent.

**Solution.**

**Proof.** In a triangle the angles add to 180°, so

$$\angle A=180°-(\angle B+\angle C),\qquad
\angle P=180°-(\angle Q+\angle R)$$

Since $\angle B=\angle Q$ and $\angle C=\angle R$, it follows that
$\angle A=\angle P$. We now have $\angle B=\angle Q$, $BC=QR$ (the side between
them) and $\angle C=\angle R$. Therefore

$$\triangle ABC\cong\triangle QRP\quad\text{(ASA)}$$

**Note.** We never measured $\angle A$; it was forced by the angle sum. This is
why ASA works with only two angles.

**Check.** The equal side must be the one lying **between** the two equal
angles. Here $BC$ lies between angles $B$ and $C$ ✓.
:::

::: example Finding an unknown from congruent triangles
**Problem.** $\triangle ABC\cong\triangle XYZ$ with $AB=(1.5x-1.5)$ cm and
$XY=(x+0.5)$ cm. Find $x$ and the length of $AB$.

**Solution.** Corresponding sides of congruent triangles are equal, so
$1.5x-1.5=x+0.5$ → $0.5x=2$ → $x=4$.
$AB=1.5\times4-1.5=4.5$ cm (and $XY=4+0.5=4.5$ cm ✓).
:::

::: example A proof with a perpendicular bisector
**Problem.** In the figure, D is the midpoint of AB and $CD\perp AB$. Prove
that $\triangle ACD\cong\triangle BCD$.

**Solution.**

| Statement | Reason |
|---|---|
| $\angle ADC=\angle BDC=90°$ | $CD\perp AB$ (given) |
| $AD=BD$ | D is the midpoint of AB |
| $CD=CD$ | common side |
| $\triangle ACD\cong\triangle BCD$ | SAS (side $AD$, included right angle, side $CD$) |

So $AC=BC$ (corresponding sides of congruent triangles).
:::

## 15.3 Similar figures

Two figures are **similar** if they have the same shape, even if they differ in
size. One is an enlargement of the other by a fixed **scale factor**.

For two similar triangles:

- the three angles of one equal the three angles of the other, and
- the three pairs of corresponding sides are in the same ratio.

$$\frac{AB}{PQ}=\frac{BC}{QR}=\frac{CA}{RP}=k$$

where $k$ is the scale factor.

**Conditions for two triangles to be similar.**

| Condition | Meaning |
|---|---|
| AA (or AAA) | two angles of one equal two angles of the other; the third follows |
| SSS similarity | the three pairs of sides are in the same ratio |
| SAS similarity | two pairs of sides are in the same ratio and the included angles are equal |

```figure caption="Similar triangles: the same angles, and every side of the larger is 2 times the matching side of the smaller (3 → 6, 2 → 4). The ratio of corresponding sides is 1 : 2."
fig, ax = plt.subplots(figsize=(4.8, 2.6))
ax.plot([0, 3, 0, 0], [0, 0, 2, 0], color=ACCENT, lw=1.6)
ax.plot([4.5, 10.5, 4.5, 4.5], [0, 0, 4, 0], color=SERIES[1], lw=1.6)
ax.plot([0, 0.25, 0.25], [0.25, 0.25, 0], color=ACCENT, lw=0.9)
ax.plot([4.5, 4.8, 4.8], [0.3, 0.3, 0], color=SERIES[1], lw=0.9)
ax.text(1.5, -0.45, "3 cm", ha="center", fontsize=9, color=INK)
ax.text(-0.2, 1.0, "2 cm", ha="right", va="center", fontsize=9, color=INK)
ax.text(7.5, -0.45, "6 cm", ha="center", fontsize=9, color=INK)
ax.text(4.3, 2.0, "4 cm", ha="right", va="center", fontsize=9, color=INK)
ax.text(1.5, 2.6, "small", ha="center", fontsize=9, color=ACCENT)
ax.text(8.2, 2.6, "enlarged (scale factor 2)", ha="center", fontsize=9, color=SERIES[1])
ax.set_xlim(-1.3, 11); ax.set_ylim(-0.9, 4.3); ax.set_aspect("equal"); ax.axis("off")
```

::: example Similar triangles and a missing side
**Problem.** Triangles $ABC$ and $PQR$ are similar, with $AB=6$ cm, $BC=9$ cm
and $PQ=4$ cm. Find $QR$.

**Solution.** Corresponding sides are in the same ratio:

$$\frac{AB}{PQ}=\frac{BC}{QR}\;\Longrightarrow\;\frac64=\frac{9}{QR}$$

Cross-multiplying: $6\times QR=36$, so $QR=6$ cm.

**Answer.** 6 cm.

**Check.** The scale factor is $\frac{6}{4}=1.5$, and
$9\div1.5=6$ ✓ — the same answer from the other direction.
:::

::: example The area ratio
**Problem.** Two similar triangles have corresponding sides in the ratio
$2:5$. Find the ratio of their areas.

**Solution.** For similar figures, the ratio of areas is the **square** of the
ratio of corresponding sides:

$$\frac{\text{area}_1}{\text{area}_2}=\left(\frac25\right)^2=\frac{4}{25}$$

**Answer.** $4:25$.

**Note.** The enlarged triangle has sides 2.5 times as long but an area 6.25
times as large. This is why a map of twice the scale needs four times the paper,
and why a model house has far less surface than the house it copies.
:::

::: caution Similar is not congruent
Two triangles with sides 3, 4, 5 and 6, 8, 10 are **similar** but not congruent.
Every pair of congruent triangles is similar, but the reverse is false. Read the
question: "find the length" usually means similar, "prove equal" means congruent.
:::

::: example Using the angle sum to prove similarity
**Problem.** In triangles $ABC$ and $DEF$, $\angle A=50°$, $\angle B=70°$,
$\angle D=50°$ and $\angle E=70°$. Prove the triangles similar and write the
ratio of corresponding sides.

**Solution.** Two angles of the first equal two angles of the second:
$\angle A=\angle D$ and $\angle B=\angle E$. So

$$\triangle ABC\sim\triangle DEF\quad\text{(AA)}$$

The third angles are equal too:
$\angle C=\angle F=180-120=60°$. The ratio of corresponding sides is

$$\frac{AB}{DE}=\frac{BC}{EF}=\frac{CA}{FD}$$

**Check.** The matched order is A with D, B with E, C with F — because those are
the equal angles. Writing the correspondence in the wrong order gives wrong
ratios.
:::

## Chapter summary

- Congruent figures have the same shape **and** size; similar figures have the
  same shape at different sizes.
- The tests of congruence are **SSS, SAS, ASA, AAS and RHS**; there is no SSA
  test.
- The order of the letters in $\triangle ABC\cong\triangle PQR$ gives the
  correspondence, and corresponding parts of congruent triangles are equal.
- Two triangles are similar if two angles match (AA), or if the three pairs of
  sides are in the same ratio (SSS similarity), or if two pairs of sides are in
  the same ratio with equal included angles (SAS similarity).
- In similar triangles, corresponding sides are in the same ratio $k$ and areas
  are in the ratio $k^2$.

## Practice questions

**Group A — Objective (1 mark each)**

1. Two triangles are congruent if <span class="marks">[1]</span>
   (a) two angles are equal (b) all three sides are equal (c) they have the same
   area (d) they look alike
2. Which of these is **not** a test of congruence?
   <span class="marks">[1]</span>
   (a) SSS (b) SAS (c) SSA (d) RHS
3. In SAS the given angle must be <span class="marks">[1]</span>
   (a) any angle (b) the largest angle (c) between the two given sides
   (d) a right angle
4. If two triangles are similar with sides in the ratio $3:4$, the ratio of
   their areas is <span class="marks">[1]</span>
   (a) $3:4$ (b) $9:16$ (c) $6:8$ (d) $4:3$
5. Two triangles with all three angles equal are
   <span class="marks">[1]</span>
   (a) always congruent (b) always similar (c) never similar (d) equal in area
6. Congruent figures have <span class="marks">[1]</span>
   (a) the same shape only (b) the same size only (c) the same shape and size
   (d) the same area only

::: note Answers to Group A
**1.** (b) — that is the SSS test.
**2.** (c) — SSA does not determine a triangle uniquely.
**3.** (c) — the angle must be the included one.
**4.** (b) — the area ratio is the square of the side ratio.
**5.** (b) — equal angles give the same shape, hence similarity; sizes may differ.
**6.** (c) — same shape and same size.
:::

**Group B — Short answer (2 marks each)**

1. State the five tests of congruence, naming the parts each uses.
   <span class="marks">[2]</span>
2. $\triangle ABC\cong\triangle PQR$ with $AB=7$ cm, $BC=9$ cm and
   $\angle B=55°$. Write down the other measurements you can.
   <span class="marks">[2]</span>
3. Two similar triangles have corresponding sides 8 cm and 12 cm. Find the
   scale factor and the ratio of their areas. <span class="marks">[2]</span>
4. In two triangles $\angle A=\angle D=65°$ and $\angle B=\angle E=45°$. Prove
   the triangles similar and state the third pair of equal angles.
   <span class="marks">[2]</span>

::: note Answers to Group B
**1.** SSS — all three sides. SAS — two sides and the included angle. ASA — two
angles and the side between them. AAS — two angles and a side not between them.
RHS — the right angle, the hypotenuse and one
other side.
**2.** Because the order of the letters gives the correspondence, $P$ matches
$A$, $Q$ matches $B$ and $R$ matches $C$. So $PQ=AB=7$ cm, $QR=BC=9$ cm, and
$\angle Q=\angle B=55°$. We also know $RP=CA$, $\angle P=\angle A$ and
$\angle R=\angle C$ (with $\angle P+\angle R=180°-55°=125°$), although their
values are not given.
**3.** Scale factor $=\frac{12}{8}=1.5$; ratio of areas
$=\left(\frac{8}{12}\right)^2=\frac{64}{144}=\frac49$, that is $4:9$.
**4.** Two angles of one equal two angles of the other, so the triangles are
similar by AA. The third pair is
$\angle C=\angle F=180-(65+45)=70°$.
:::

**Group C — Long answer (4 marks each)**

1. In a quadrilateral $ABCD$, the diagonal $AC$ bisects both $\angle A$ and
   $\angle C$. Prove that $\triangle ABC\cong\triangle ADC$ and hence that
   $AB=AD$ and $CB=CD$. <span class="marks">[4]</span>
2. A vertical pole 2 m high casts a shadow 3 m long at the same time as a tower
   casts a shadow 21 m long. Using similar triangles, find the height of the
   tower, and state which angles you used. <span class="marks">[4]</span>

::: note Answers to Group C
**1. Given.** $\angle BAC=\angle DAC$ and $\angle BCA=\angle DCA$ (the diagonal
bisects both angles). **To prove.** $\triangle ABC\cong\triangle ADC$, so
$AB=AD$ and $CB=CD$.

| Statement | Reason |
|---|---|
| $\angle BAC=\angle DAC$ | given, $AC$ bisects $\angle A$ |
| $AC=AC$ | common side |
| $\angle BCA=\angle DCA$ | given, $AC$ bisects $\angle C$ |
| $\triangle ABC\cong\triangle ADC$ | ASA |
| $AB=AD$ and $CB=CD$ | corresponding parts of congruent triangles |

The side $AC$ used in the ASA test is the one lying between the two pairs of
equal angles ✓.
**2.** Let the sun's rays make the same angle with the ground for both objects,
so $\angle(\text{ray, ground})$ is equal; and both the pole and the tower stand
vertically, so each makes a right angle with the ground. The two triangles
therefore have two equal angles and are similar by AA.

$$\frac{\text{height of tower}}{\text{height of pole}}
=\frac{\text{shadow of tower}}{\text{shadow of pole}}$$

$$\frac{h}{2}=\frac{21}{3}=7\;\Longrightarrow\;h=14\ \text{m}$$

**Answer.** The tower is 14 m high. **Angles used.** The right angle at the base
of each object and the angle between the sun's ray and the ground — the AA
condition. **Check.** The scale factor of the shadows is
$21\div3=7$, so the heights must also be in the ratio $7:1$, and
$14=7\times2$ ✓.
:::

## Objective practice

**Choose the correct answer.** <span class="marks">[5×1=5]</span>

**1.** Which test does **not** prove two triangles congruent?
   (a) SSS (b) SAS (c) AAA (d) ASA
**2.** In two similar triangles the corresponding sides are
   (a) equal (b) proportional (c) perpendicular (d) unrelated
**3.** Triangles with sides $5, 12, 13$ cm and $10, 24, 26$ cm are
   (a) congruent (b) similar only (c) neither (d) equal in area
**4.** The RHS test applies to
   (a) all triangles (b) right-angled triangles (c) isosceles triangles (d) equilateral triangles
**5.** If two figures are congruent then they are
   (a) also similar (b) never similar (c) similar only if squares (d) equal in perimeter but not area

::: note Objective practice — answers
**1.** (c) — equal angles fix the shape, not the size. **2.** (b) — proportional. **3.** (b) — the ratio is $1:2$, so similar but not congruent. **4.** (b) — right angle, hypotenuse and one side. **5.** (a) — congruent figures are similar with ratio 1.
:::
