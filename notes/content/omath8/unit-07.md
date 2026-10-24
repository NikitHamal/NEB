---
subject: Optional Mathematics
grade: 8
unit: 7
title: Trigonometry
hours: 0
---

How tall is the Dharahara, a tree in the school ground, or a hill across the river? You cannot climb up with a measuring tape, but you can stand some distance away, measure that distance along the ground, and measure the angle up to the top. **Trigonometry** (from Greek *trigonon*, triangle, and *metron*, measure) is the mathematics that turns such an angle and a distance into a height. It rests on a simple fact: in right-angled triangles with the same angle, the ratios of the sides are always the same. This chapter first explains three ways of measuring angles, then defines the six trigonometric ratios, proves the identities that connect them, finds their exact values for the standard angles, extends them to angles such as $120^\circ$ and $-30^\circ$, and finally uses them to find heights and distances.

::: key What your examination asks from this chapter
Expect: (i) converting an angle between **degrees, grades and radians**, often for the angles of a triangle; (ii) finding all six **trigonometric ratios** from one ratio or from the sides of a right triangle; (iii) **proving an identity** such as $\tan\theta+\cot\theta=\sec\theta\,\mathrm{cosec}\,\theta$; (iv) evaluating expressions with the values at $0^\circ$, $30^\circ$, $45^\circ$, $60^\circ$, $90^\circ$, or finding an acute angle from an equation; (v) ratios of angles such as $120^\circ$, $135^\circ$, $210^\circ$, $-60^\circ$ using **allied angles**; (vi) one **height and distance** problem with a single angle of elevation or depression, with a labelled figure. Marks are given for the figure, the ratio chosen, the substitution and the answer with its unit.
:::

## 7.1 Measurement of angles: sexagesimal, centesimal and circular (radian) systems

An **angle** is formed when a ray turns about its end point from a starting position (the **initial side**) to a final position (the **terminal side**). The amount of turning is the size of the angle. Turning **anticlockwise** gives a **positive** angle; turning **clockwise** gives a **negative** angle. One complete turn brings the ray back to where it started, and a quarter of a complete turn is a **right angle**.

There are three systems of measuring angles. They differ only in how they divide the right angle.

### Sexagesimal (British) system

The right angle is divided into 90 equal parts called **degrees** ($^\circ$), each degree into 60 **minutes** ($'$) and each minute into 60 **seconds** ($''$). The name comes from the Latin for sixty.
$$ 1 \text{ right angle}=90^\circ,\qquad 1^\circ=60',\qquad 1'=60'' $$

### Centesimal (French) system

The right angle is divided into 100 equal parts called **grades** ($^g$), each grade into 100 **centesimal minutes** ($^c$) and each of these into 100 **centesimal seconds** ($^{cc}$). The name comes from the Latin for hundred.
$$ 1 \text{ right angle}=100^g,\qquad 1^g=100^c,\qquad 1^c=100^{cc} $$

### Circular system and the radian

::: definition Radian
A **radian** is the angle subtended at the centre of a circle by an arc whose length is **equal to the radius**. It is written $1^c$ (or 1 rad).
:::

```figure caption="Left: an arc of length $r$ on a circle of radius $r$ subtends one radian, about $57.3^\circ$, at the centre. Right: one right angle in the three systems, $90^\circ=100^g=\left(\frac{\pi}{2}\right)^c$."
from matplotlib.patches import Arc, Wedge
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(5.0, 2.7))
t = np.linspace(0, 2*np.pi, 300)
ax1.plot(np.cos(t), np.sin(t), color=MUTED, lw=1.0)
ax1.add_patch(Wedge((0, 0), 1.0, 0, np.degrees(1.0), fc='#cfe3f6', ec='none'))
ax1.plot([0, 1], [0, 0], color=INK, lw=1.4)
ax1.plot([0, np.cos(1.0)], [0, np.sin(1.0)], color=INK, lw=1.4)
ta = np.linspace(0, 1.0, 60)
ax1.plot(np.cos(ta), np.sin(ta), color=SERIES[1], lw=2.4)
ax1.text(0.5, -0.13, 'r', ha='center', fontsize=9.5)
ax1.text(0.18, 0.42, 'r', ha='center', fontsize=9.5)
ax1.text(1.04, 0.5, 'arc = r', fontsize=9, color=SERIES[1])
ax1.add_patch(Arc((0, 0), 0.5, 0.5, theta1=0, theta2=np.degrees(1.0), color=INK, lw=1.0))
ax1.text(0.3, 0.1, '1ᶜ', fontsize=9)
ax1.set_xlim(-1.15, 1.75); ax1.set_ylim(-1.15, 1.15); ax1.set_aspect('equal'); ax1.axis('off')
ax2.plot([0, 1.3], [0, 0], color=INK, lw=1.4); ax2.plot([0, 0], [0, 1.3], color=INK, lw=1.4)
ax2.add_patch(Rectangle((0, 0), 0.14, 0.14, fill=False, ec=INK, lw=0.9))
ax2.add_patch(Arc((0, 0), 1.2, 1.2, theta1=0, theta2=90, color=ACCENT, lw=1.6))
ax2.text(0.62, 0.95, '90°', fontsize=10, color=ACCENT)
ax2.text(0.62, 0.72, '= 100ᵍ', fontsize=10, color=SERIES[2])
ax2.text(0.62, 0.49, '= (π/2)ᶜ', fontsize=10, color=SERIES[1])
ax2.set_xlim(-0.2, 1.8); ax2.set_ylim(-0.2, 1.45); ax2.set_aspect('equal'); ax2.axis('off')
fig.tight_layout(pad=0.4)
```

The circumference of a circle is $2\pi r$, so it contains $2\pi$ arcs of length $r$. A complete turn is therefore $2\pi$ radians, a half turn is $\pi$ radians, and a right angle is $\frac{\pi}{2}$ radians:
$$ \pi^c=180^\circ,\qquad 1^c=\frac{180^\circ}{\pi}\approx57.3^\circ\approx57^\circ17'45'',\qquad 1^\circ=\frac{\pi}{180}\ \text{radian}\approx0.01745^c $$
A radian is the same size for every circle, because doubling the radius doubles the arc as well. That is why scientists prefer it.

::: key Converting between the systems
All three systems agree that a right angle is $90^\circ=100^g=\frac{\pi}{2}$ radians. So if an angle is $D$ degrees, $G$ grades and $R$ radians,
$$ \frac{D}{90}=\frac{G}{100}=\frac{2R}{\pi} $$
In practice: $1^\circ=\frac{10}{9}$ grades, $1^g=\frac{9}{10}$ degree $=0.9^\circ$, and $\pi^c=180^\circ=200^g$.
:::

::: example Degrees and grades
**Problem.** Convert (i) $24^\circ18'$ into grades; (ii) $75^g$ into degrees and minutes; (iii) $50^g25^c$ into degrees, minutes and seconds.

**Solution.** (i) First make the minutes a decimal: $18'=\frac{18}{60}=0.3^\circ$, so $24^\circ18'=24.3^\circ$. Then $G=\frac{10}{9}\times24.3=27^g$.

(ii) $D=\frac{9}{10}\times75=67.5^\circ$, and $0.5^\circ=30'$. So $75^g=67^\circ30'$.

(iii) $25^c=\frac{25}{100}=0.25^g$, so the angle is $50.25^g$. Then $D=0.9\times50.25=45.225^\circ$. The decimal part $0.225^\circ=0.225\times60'=13.5'=13'30''$. So $50^g25^c=45^\circ13'30''$.
:::

::: example Degrees and radians
**Problem.** Convert (i) $135^\circ$ into radians; (ii) $\left(\frac{3\pi}{5}\right)^c$ into degrees and grades.

**Solution.** (i) Multiply by $\frac{\pi}{180}$: $135\times\frac{\pi}{180}=\frac{3\pi}{4}$ radians.

(ii) Replace $\pi$ by $180^\circ$: $\frac{3\times180^\circ}{5}=108^\circ$. Since $\pi^c=200^g$, the same angle is $\frac{3\times200}{5}=120^g$.
:::

::: example Angles of a triangle in mixed units
**Problem.** Two angles of a triangle are $60^\circ$ and $50^g$. Find the third angle in degrees and in radians.

**Solution.** Change everything to degrees first: $50^g=0.9\times50=45^\circ$. The angles of a triangle add to $180^\circ$, so the third angle is $180^\circ-60^\circ-45^\circ=75^\circ$. In radians, $75\times\frac{\pi}{180}=\frac{5\pi}{12}$.
:::

### Length of an arc

The definition of a radian gives a quick formula: an angle of $\theta$ radians at the centre cuts off an arc $\theta$ times as long as the radius,
$$ l=r\theta \qquad (\theta \text{ in radians}) $$
A bicycle wheel of radius 35 cm that turns through 2 radians rolls $35\times2=70$ cm along the road. A pendulum 50 cm long whose bob moves along an arc of 10 cm swings through $\theta=\frac{10}{50}=0.2$ radian, about $11.5^\circ$.

::: caution Change minutes to a decimal before converting
$24^\circ18'$ is $24.3^\circ$, **not** $24.18^\circ$, because a degree has 60 minutes, not 100. Only centesimal minutes are hundredths: $50^g25^c$ really is $50.25^g$. Mixing the two is the commonest error in conversion questions.
:::

## 7.2 Trigonometric ratios of an acute angle

Take a right-angled triangle and fix one of its acute angles, $\theta$. The three sides are named by their position relative to $\theta$:

- the **hypotenuse** $h$ is the longest side, opposite the right angle;
- the **perpendicular** $p$ is the side **opposite** $\theta$;
- the **base** $b$ is the side **next to** $\theta$ (other than the hypotenuse).

```figure caption="Naming the sides for the angle $\theta$ at $A$: the perpendicular $p$ is opposite $\theta$, the base $b$ is next to it and the hypotenuse $h$ is opposite the right angle. For the other acute angle, at $C$, the perpendicular and the base change places."
from matplotlib.patches import Arc
fig, ax = plt.subplots(figsize=(4.6, 2.9))
A, B, C = (0.0, 0.0), (4.0, 0.0), (4.0, 3.0)
ax.fill([A[0], B[0], C[0]], [A[1], B[1], C[1]], color='#eef4fb')
ax.plot([A[0], B[0], C[0], A[0]], [A[1], B[1], C[1], A[1]], color=INK, lw=1.6)
ax.add_patch(Rectangle((B[0] - 0.25, 0), 0.25, 0.25, fill=False, ec=INK, lw=0.9))
ax.add_patch(Arc(A, 1.3, 1.3, theta1=0, theta2=np.degrees(np.arctan2(3, 4)), color=SERIES[1], lw=1.4))
ax.text(0.8, 0.2, 'θ', fontsize=11, color=SERIES[1])
ax.text(A[0] - 0.15, A[1] - 0.1, 'A', fontsize=10, ha='right'); ax.text(B[0] + 0.12, B[1] - 0.1, 'B', fontsize=10)
ax.text(C[0] + 0.12, C[1] + 0.05, 'C', fontsize=10)
ax.text(2.0, -0.38, 'base  b', ha='center', fontsize=9.5, color=SERIES[2])
ax.text(4.15, 1.5, 'perpendicular  p', va='center', fontsize=9.5, color=ACCENT)
ax.text(1.7, 1.75, 'hypotenuse  h', ha='center', fontsize=9.5, rotation=36.87, color=INK)
ax.set_xlim(-0.6, 6.8); ax.set_ylim(-0.7, 3.4); ax.set_aspect('equal'); ax.axis('off')
fig.tight_layout(pad=0.3)
```

::: definition The six trigonometric ratios
For an acute angle $\theta$ of a right-angled triangle with perpendicular $p$, base $b$ and hypotenuse $h$:
$$ \sin\theta=\frac{p}{h},\qquad \cos\theta=\frac{b}{h},\qquad \tan\theta=\frac{p}{b} $$
$$ \mathrm{cosec}\,\theta=\frac{h}{p},\qquad \sec\theta=\frac{h}{b},\qquad \cot\theta=\frac{b}{p} $$
They are read sine, cosine, tangent, cosecant, secant and cotangent of $\theta$.
:::

::: memory Some People Have Curly Brown Hair Through Proper Brushing
**S**ome **P**eople **H**ave: $\sin=\frac{p}{h}$. **C**urly **B**rown **H**air: $\cos=\frac{b}{h}$. **T**hrough **P**roper **B**rushing: $\tan=\frac{p}{b}$. The other three are the same fractions turned upside down.
:::

### Why the ratios depend only on the angle

Any two right-angled triangles with the same acute angle $\theta$ are **similar** (their angles are $90^\circ$, $\theta$ and $90^\circ-\theta$). In similar triangles corresponding sides are in proportion, so $\frac{p}{h}$, $\frac{b}{h}$ and $\frac{p}{b}$ come out the same however large the triangle is drawn. The ratios belong to the **angle**, not to the particular triangle. That is what makes it possible to measure a tall tower with a small triangle drawn in a notebook.

### Reciprocal and quotient relations

Straight from the definitions:
$$ \mathrm{cosec}\,\theta=\frac{1}{\sin\theta},\qquad \sec\theta=\frac{1}{\cos\theta},\qquad \cot\theta=\frac{1}{\tan\theta} $$
$$ \tan\theta=\frac{\sin\theta}{\cos\theta},\qquad \cot\theta=\frac{\cos\theta}{\sin\theta} $$
(For example, $\frac{\sin\theta}{\cos\theta}=\frac{p/h}{b/h}=\frac{p}{b}=\tan\theta$.)

::: example Six ratios from the sides
**Problem.** In triangle $ABC$, $\angle B=90^\circ$, $AB=5$ cm, $BC=12$ cm and $AC=13$ cm. Find the six trigonometric ratios of $\angle A$, and $\sin C$, $\cos C$, $\tan C$.

**Solution.** For $\angle A$: the side opposite is $p=BC=12$, the side next to it is $b=AB=5$, and $h=AC=13$.
$$ \sin A=\frac{12}{13},\ \ \cos A=\frac{5}{13},\ \ \tan A=\frac{12}{5},\ \ \mathrm{cosec}\,A=\frac{13}{12},\ \ \sec A=\frac{13}{5},\ \ \cot A=\frac{5}{12} $$
For $\angle C$ the roles change: $p=AB=5$ and $b=BC=12$. So $\sin C=\frac{5}{13}$, $\cos C=\frac{12}{13}$ and $\tan C=\frac{5}{12}$. Notice that $\sin C=\cos A$: the two acute angles add to $90^\circ$.
:::

::: example All the ratios from one ratio
**Problem.** If $\sin\theta=\frac{3}{5}$, find the other five ratios of the acute angle $\theta$.

**Solution.** $\sin\theta=\frac{p}{h}=\frac{3}{5}$, so take $p=3$ and $h=5$. By Pythagoras' theorem,
$$ b=\sqrt{h^2-p^2}=\sqrt{25-9}=\sqrt{16}=4 $$
So $\cos\theta=\frac{4}{5}$, $\tan\theta=\frac{3}{4}$, $\mathrm{cosec}\,\theta=\frac{5}{3}$, $\sec\theta=\frac{5}{4}$ and $\cot\theta=\frac{4}{3}$.
:::

::: example From a tangent to the sine and cosine
**Problem.** If $\tan\theta=\frac{8}{15}$, find $\sin\theta$ and $\cos\theta$. If the hypotenuse of a right triangle is 10 cm and $\cos\theta=0.8$, find its other two sides.

**Solution.** $\tan\theta=\frac{p}{b}=\frac{8}{15}$; then $h=\sqrt{64+225}=\sqrt{289}=17$. So $\sin\theta=\frac{8}{17}$ and $\cos\theta=\frac{15}{17}$.

For the second part, $\cos\theta=\frac{b}{h}$ gives $b=10\times0.8=8$ cm, and then $p=\sqrt{100-64}=6$ cm.
:::

::: caution The perpendicular is opposite the angle you are using
"Perpendicular" here does not mean "the vertical side in the picture". It means the side **opposite the chosen angle**. In the example above, $BC$ is the perpendicular for $\angle A$ but the base for $\angle C$. Mark the angle first, then name $p$, $b$ and $h$.
:::

## 7.3 Trigonometric identities and their conversions

An **identity** is an equation that is true for **every** value of the angle, like $(a+b)^2=a^2+2ab+b^2$ in algebra. Three identities follow from Pythagoras' theorem $p^2+b^2=h^2$.

::: derivation The three fundamental identities
We start from $p^2+b^2=h^2$ in a right triangle with acute angle $\theta$.

**Step 1 — divide every term by $h^2$.**
$$ \frac{p^2}{h^2}+\frac{b^2}{h^2}=1\ \Rightarrow\ \left(\frac{p}{h}\right)^2+\left(\frac{b}{h}\right)^2=1\ \Rightarrow\ \sin^2\theta+\cos^2\theta=1 $$

**Step 2 — divide $p^2+b^2=h^2$ by $b^2$ instead.**
$$ \frac{p^2}{b^2}+1=\frac{h^2}{b^2}\ \Rightarrow\ \tan^2\theta+1=\sec^2\theta $$

**Step 3 — divide by $p^2$.**
$$ 1+\frac{b^2}{p^2}=\frac{h^2}{p^2}\ \Rightarrow\ 1+\cot^2\theta=\mathrm{cosec}^2\theta $$

**What it means.** $\sin^2\theta$ means $(\sin\theta)^2$. These three identities, with their rearrangements, are the main tools for proving every other identity in this chapter.
:::

::: key Identities to know by heart
| Identity | Useful rearrangements |
|---|---|
| $\sin^2\theta+\cos^2\theta=1$ | $\sin^2\theta=1-\cos^2\theta$, $\ \cos^2\theta=1-\sin^2\theta$ |
| $1+\tan^2\theta=\sec^2\theta$ | $\sec^2\theta-\tan^2\theta=1$, $\ (\sec\theta-\tan\theta)(\sec\theta+\tan\theta)=1$ |
| $1+\cot^2\theta=\mathrm{cosec}^2\theta$ | $\mathrm{cosec}^2\theta-\cot^2\theta=1$ |
| $\tan\theta=\frac{\sin\theta}{\cos\theta}$, $\cot\theta=\frac{\cos\theta}{\sin\theta}$ | $\mathrm{cosec}\,\theta=\frac{1}{\sin\theta}$, $\sec\theta=\frac{1}{\cos\theta}$, $\cot\theta=\frac{1}{\tan\theta}$ |
:::

### Conversions: one ratio in terms of another

Every ratio can be written in terms of any one of the others. The easy way is to draw a triangle. To write everything in terms of $\sin\theta$, take $p=\sin\theta$ and $h=1$; then $b=\sqrt{1-\sin^2\theta}$. To write everything in terms of $\tan\theta$, take $p=\tan\theta$ and $b=1$; then $h=\sqrt{1+\tan^2\theta}$.

| Ratio | in terms of $\sin\theta$ | in terms of $\tan\theta$ |
|---|---|---|
| $\sin\theta$ | $\sin\theta$ | $\frac{\tan\theta}{\sqrt{1+\tan^2\theta}}$ |
| $\cos\theta$ | $\sqrt{1-\sin^2\theta}$ | $\frac{1}{\sqrt{1+\tan^2\theta}}$ |
| $\tan\theta$ | $\frac{\sin\theta}{\sqrt{1-\sin^2\theta}}$ | $\tan\theta$ |
| $\mathrm{cosec}\,\theta$ | $\frac{1}{\sin\theta}$ | $\frac{\sqrt{1+\tan^2\theta}}{\tan\theta}$ |
| $\sec\theta$ | $\frac{1}{\sqrt{1-\sin^2\theta}}$ | $\sqrt{1+\tan^2\theta}$ |
| $\cot\theta$ | $\frac{\sqrt{1-\sin^2\theta}}{\sin\theta}$ | $\frac{1}{\tan\theta}$ |

### Proving identities

To prove an identity, start from **one side** (usually the more complicated one) and change it, step by step, into the other side. Never move terms across the equals sign as if solving an equation: you are showing that two expressions are the same, not finding $\theta$. Useful moves are: change everything into $\sin$ and $\cos$; use $\sin^2\theta+\cos^2\theta=1$; factorise; and add fractions over a common denominator.

::: example Three short proofs
**Problem.** Prove that (i) $(1-\sin^2\theta)\sec^2\theta=1$ (ii) $\sin\theta\cot\theta=\cos\theta$ (iii) $(1+\tan^2\theta)\cos^2\theta=1$.

**Solution.** (i) LHS $=(1-\sin^2\theta)\sec^2\theta=\cos^2\theta\times\frac{1}{\cos^2\theta}=1=$ RHS.

(ii) LHS $=\sin\theta\times\frac{\cos\theta}{\sin\theta}=\cos\theta=$ RHS.

(iii) LHS $=\sec^2\theta\times\cos^2\theta=\frac{1}{\cos^2\theta}\times\cos^2\theta=1=$ RHS.
:::

::: example Changing into sine and cosine
**Problem.** Prove that $\tan\theta+\cot\theta=\sec\theta\,\mathrm{cosec}\,\theta$.

**Solution.**
$$ \text{LHS}=\frac{\sin\theta}{\cos\theta}+\frac{\cos\theta}{\sin\theta}=\frac{\sin^2\theta+\cos^2\theta}{\sin\theta\cos\theta}=\frac{1}{\sin\theta\cos\theta} $$
$$ =\frac{1}{\cos\theta}\times\frac{1}{\sin\theta}=\sec\theta\,\mathrm{cosec}\,\theta=\text{RHS} $$
:::

::: example Factorising and fractions
**Problem.** Prove that (i) $\sin^4\theta-\cos^4\theta=\sin^2\theta-\cos^2\theta$ (ii) $\frac{1}{1+\sin\theta}+\frac{1}{1-\sin\theta}=2\sec^2\theta$ (iii) $(1-\cos\theta)(1+\cos\theta)(1+\cot^2\theta)=1$.

**Solution.** (i) Use $a^2-b^2=(a+b)(a-b)$ with $a=\sin^2\theta$, $b=\cos^2\theta$:
$$ \text{LHS}=(\sin^2\theta+\cos^2\theta)(\sin^2\theta-\cos^2\theta)=1\times(\sin^2\theta-\cos^2\theta)=\text{RHS} $$
(ii) Add the fractions:
$$ \text{LHS}=\frac{(1-\sin\theta)+(1+\sin\theta)}{(1+\sin\theta)(1-\sin\theta)}=\frac{2}{1-\sin^2\theta}=\frac{2}{\cos^2\theta}=2\sec^2\theta=\text{RHS} $$
(iii) $(1-\cos\theta)(1+\cos\theta)=1-\cos^2\theta=\sin^2\theta$ and $1+\cot^2\theta=\mathrm{cosec}^2\theta$, so
$$ \text{LHS}=\sin^2\theta\times\frac{1}{\sin^2\theta}=1=\text{RHS} $$
:::

::: tip The examiner is looking for
(1) "LHS =" written at the start, so the marker knows which side you began from; (2) one change per line, with the identity used visible; (3) "= RHS" at the end. A proof that works on both sides at once and meets in the middle is accepted, but it must be set out as two separate chains.
:::

## 7.4 Values of trigonometric ratios of 0°, 30°, 45°, 60° and 90°

For most angles the ratios are long decimals found with a calculator. For five special angles we can find them **exactly** from simple triangles.

### 45°

Cut a square of side 1 along a diagonal. Each half is a right triangle with two angles of $45^\circ$, legs 1 and 1, and hypotenuse $\sqrt{1^2+1^2}=\sqrt{2}$.
$$ \sin45^\circ=\frac{1}{\sqrt{2}},\qquad \cos45^\circ=\frac{1}{\sqrt{2}},\qquad \tan45^\circ=\frac{1}{1}=1 $$

### 30° and 60°

Take an equilateral triangle of side 2 and drop a perpendicular from the top vertex. It bisects the base and the top angle, giving a right triangle with angles $30^\circ$, $60^\circ$, $90^\circ$, hypotenuse 2, short side 1, and height $\sqrt{2^2-1^2}=\sqrt{3}$.

```figure caption="Exact values come from two triangles. Left: half of a unit square has angles of $45^\circ$ and sides $1, 1, \sqrt{2}$. Right: half of an equilateral triangle of side 2 has angles $30^\circ$ and $60^\circ$ and sides $1, \sqrt{3}, 2$."
from matplotlib.patches import Arc
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(5.0, 2.7))
ax1.plot([0, 2, 2, 0], [0, 0, 2, 0], color=INK, lw=1.5)
ax1.add_patch(Rectangle((1.82, 0), 0.18, 0.18, fill=False, ec=INK, lw=0.9))
ax1.add_patch(Arc((0, 0), 0.8, 0.8, theta1=0, theta2=45, color=SERIES[1], lw=1.3))
ax1.text(0.48, 0.12, '45°', fontsize=8.5, color=SERIES[1])
ax1.add_patch(Arc((2, 2), 0.8, 0.8, theta1=225, theta2=270, color=SERIES[1], lw=1.3))
ax1.text(1.7, 1.3, '45°', fontsize=8.5, color=SERIES[1])
ax1.text(1.0, -0.3, '1', ha='center', fontsize=10); ax1.text(2.12, 1.0, '1', va='center', fontsize=10)
ax1.text(0.82, 1.15, '√2', ha='center', fontsize=10)
ax1.set_xlim(-0.3, 2.6); ax1.set_ylim(-0.5, 2.3); ax1.set_aspect('equal'); ax1.axis('off')
h = np.sqrt(3)
ax2.plot([0, 2, 1, 0], [0, 0, h, 0], color=MUTED, lw=1.0, ls='--')
ax2.plot([1, 2, 1, 1], [0, 0, h, 0], color=INK, lw=1.6)
ax2.fill([1, 2, 1], [0, 0, h], color='#eef4fb')
ax2.add_patch(Rectangle((1, 0), 0.15, 0.15, fill=False, ec=INK, lw=0.9))
ax2.add_patch(Arc((2, 0), 0.6, 0.6, theta1=120, theta2=180, color=SERIES[1], lw=1.3))
ax2.text(1.55, 0.12, '60°', fontsize=8.5, color=SERIES[1])
ax2.add_patch(Arc((1, h), 0.7, 0.7, theta1=270, theta2=300, color=SERIES[2], lw=1.3))
ax2.text(1.06, h - 0.62, '30°', fontsize=8.5, color=SERIES[2])
ax2.text(1.5, -0.3, '1', ha='center', fontsize=10); ax2.text(0.8, 0.85, '√3', ha='center', fontsize=10)
ax2.text(1.66, 1.0, '2', fontsize=10)
ax2.set_xlim(-0.2, 2.4); ax2.set_ylim(-0.5, 2.0); ax2.set_aspect('equal'); ax2.axis('off')
fig.tight_layout(pad=0.4)
```

For the $30^\circ$ angle at the top, $p=1$, $b=\sqrt{3}$, $h=2$; for the $60^\circ$ angle at the base, $p=\sqrt{3}$, $b=1$, $h=2$:
$$ \sin30^\circ=\frac{1}{2},\qquad \cos30^\circ=\frac{\sqrt{3}}{2},\qquad \tan30^\circ=\frac{1}{\sqrt{3}} $$
$$ \sin60^\circ=\frac{\sqrt{3}}{2},\qquad \cos60^\circ=\frac{1}{2},\qquad \tan60^\circ=\sqrt{3} $$

### 0° and 90°

Imagine a right triangle with hypotenuse 1 and let its angle $\theta$ shrink towards $0^\circ$: the perpendicular shrinks to 0 and the base grows to 1. So $\sin0^\circ=0$, $\cos0^\circ=1$ and $\tan0^\circ=0$. Now let $\theta$ grow towards $90^\circ$: the perpendicular grows to 1 and the base shrinks to 0. So $\sin90^\circ=1$ and $\cos90^\circ=0$, while $\tan90^\circ=\frac{1}{0}$ is **not defined**. (This is the limit idea of chapter 4 at work.)

::: key Table of standard values
| $\theta$ | $0^\circ$ | $30^\circ$ | $45^\circ$ | $60^\circ$ | $90^\circ$ |
|---|---|---|---|---|---|
| $\sin\theta$ | 0 | $\frac{1}{2}$ | $\frac{1}{\sqrt{2}}$ | $\frac{\sqrt{3}}{2}$ | 1 |
| $\cos\theta$ | 1 | $\frac{\sqrt{3}}{2}$ | $\frac{1}{\sqrt{2}}$ | $\frac{1}{2}$ | 0 |
| $\tan\theta$ | 0 | $\frac{1}{\sqrt{3}}$ | 1 | $\sqrt{3}$ | not defined |
| $\mathrm{cosec}\,\theta$ | not defined | 2 | $\sqrt{2}$ | $\frac{2}{\sqrt{3}}$ | 1 |
| $\sec\theta$ | 1 | $\frac{2}{\sqrt{3}}$ | $\sqrt{2}$ | 2 | not defined |
| $\cot\theta$ | not defined | $\sqrt{3}$ | 1 | $\frac{1}{\sqrt{3}}$ | 0 |
:::

::: memory The square-root pattern
Write $\sqrt{0}, \sqrt{1}, \sqrt{2}, \sqrt{3}, \sqrt{4}$ and divide each by 2: you get $\sin0^\circ, \sin30^\circ, \sin45^\circ, \sin60^\circ, \sin90^\circ$, that is $0, \frac{1}{2}, \frac{1}{\sqrt{2}}, \frac{\sqrt{3}}{2}, 1$. The cosines are the same list **backwards**. Then $\tan=\frac{\sin}{\cos}$.
:::

::: example Evaluating with standard values
**Problem.** Find the value of (i) $\sin30^\circ\cos60^\circ+\cos30^\circ\sin60^\circ$ (ii) $\tan^260^\circ+2\tan^245^\circ$ (iii) $\frac{1-\tan^230^\circ}{1+\tan^230^\circ}$ (iv) $4\sin^230^\circ+3\tan^230^\circ-8\sin45^\circ\cos45^\circ$.

**Solution.** (i) $\frac{1}{2}\cdot\frac{1}{2}+\frac{\sqrt{3}}{2}\cdot\frac{\sqrt{3}}{2}=\frac{1}{4}+\frac{3}{4}=1$.

(ii) $(\sqrt{3})^2+2(1)^2=3+2=5$.

(iii) $\tan^230^\circ=\frac{1}{3}$, so the value is $\frac{1-\frac{1}{3}}{1+\frac{1}{3}}=\frac{\frac{2}{3}}{\frac{4}{3}}=\frac{1}{2}$, which equals $\cos60^\circ$.

(iv) $4\cdot\frac{1}{4}+3\cdot\frac{1}{3}-8\cdot\frac{1}{\sqrt{2}}\cdot\frac{1}{\sqrt{2}}=1+1-4=-2$.
:::

::: example Finding the angle
**Problem.** Find the acute angle $\theta$ if (i) $2\sin\theta=\sqrt{3}$ (ii) $\sqrt{3}\tan\theta=1$ (iii) $2\cos^2\theta=1$.

**Solution.** (i) $\sin\theta=\frac{\sqrt{3}}{2}=\sin60^\circ$, so $\theta=60^\circ$.

(ii) $\tan\theta=\frac{1}{\sqrt{3}}=\tan30^\circ$, so $\theta=30^\circ$.

(iii) $\cos^2\theta=\frac{1}{2}$, so $\cos\theta=\frac{1}{\sqrt{2}}$ (positive, as $\theta$ is acute) and $\theta=45^\circ$.
:::

::: caution sin²30° is not sin 30²
$\sin^230^\circ$ means $(\sin30^\circ)^2=\frac{1}{4}$. It does not mean $\sin900^\circ$ or $\sin(30^\circ)\times2$. And $\sin(30^\circ+60^\circ)=\sin90^\circ=1$ is **not** $\sin30^\circ+\sin60^\circ=\frac{1+\sqrt{3}}{2}$: a trigonometric ratio does not split over addition.
:::

## 7.5 Trigonometric ratios of (90° ± θ), (180° ± θ) and (−θ)

### Ratios of any angle

A right triangle can only hold acute angles. To give $120^\circ$ or $-30^\circ$ a sine, we use coordinates. Let the terminal side of an angle $\theta$ (measured from the positive $x$-axis) pass through a point $P(x,y)$, and let $r=OP=\sqrt{x^2+y^2}$. Define
$$ \sin\theta=\frac{y}{r},\qquad \cos\theta=\frac{x}{r},\qquad \tan\theta=\frac{y}{x} $$
and the other three as their reciprocals. For an acute angle, $y$ is the perpendicular, $x$ the base and $r$ the hypotenuse, so these agree with section 7.2. For larger angles, $x$ or $y$ may be negative, and the ratios take the signs of $x$ and $y$.

```figure caption="Signs of the ratios in the four quadrants. $r$ is always positive, so $\sin\theta=\frac{y}{r}$ has the sign of $y$ and $\cos\theta=\frac{x}{r}$ the sign of $x$. Only the ratios named in a quadrant (and their reciprocals) are positive there: All, Sin, Tan, Cos."
from matplotlib.patches import Arc
fig, ax = plt.subplots(figsize=(4.4, 3.4))
t = np.linspace(0, 2*np.pi, 300)
ax.plot(np.cos(t), np.sin(t), color=GRID, lw=1.2)
ax.axhline(0, color=INK, lw=0.9); ax.axvline(0, color=INK, lw=0.9)
th = np.radians(40)
P = (np.cos(th), np.sin(th))
ax.plot([0, P[0]], [0, P[1]], color=ACCENT, lw=1.6)
ax.plot([P[0], P[0]], [0, P[1]], color=ACCENT, lw=1.0, ls='--')
ax.plot(P[0], P[1], 'o', color=ACCENT, ms=4.5)
ax.text(P[0] + 0.04, P[1] + 0.05, 'P(x, y)', fontsize=8.5, color=ACCENT)
ax.text(0.33, 0.37, 'r', fontsize=9, color=ACCENT)
ax.add_patch(Arc((0, 0), 0.4, 0.4, theta1=0, theta2=40, color=INK, lw=1.0))
ax.text(0.24, 0.05, 'θ', fontsize=9)
for (x, y), lab, sub, c in [((1.25, 1.0), 'I : All', 'x +, y +', SERIES[2]), ((-1.25, 1.0), 'II : Sin', 'x −, y +', SERIES[1]),
                            ((-1.25, -0.9), 'III : Tan', 'x −, y −', SERIES[3]), ((1.25, -0.9), 'IV : Cos', 'x +, y −', SERIES[4])]:
    ax.text(x, y, lab, fontsize=9, color=c, ha='center')
    ax.text(x, y - 0.17, sub, fontsize=8, color=MUTED, ha='center')
ax.text(1.12, -0.12, 'x', fontsize=9, color=MUTED); ax.text(0.05, 1.08, 'y', fontsize=9, color=MUTED)
ax.set_xlim(-1.75, 1.75); ax.set_ylim(-1.15, 1.2); ax.set_aspect('equal'); ax.axis('off')
fig.tight_layout(pad=0.3)
```

::: memory All Silver Tea Cups
Going anticlockwise from the first quadrant: **A**ll ratios are positive in the first, **S**ine in the second, **T**angent in the third and **C**osine in the fourth (each with its reciprocal). "**A**ll **S**ilver **T**ea **C**ups" (ASTC).
:::

### How the allied angles arise

Let $\theta$ be acute and $P(x,y)$ a point on its terminal side, so $\sin\theta=\frac{y}{r}$ and $\cos\theta=\frac{x}{r}$. Each allied angle comes from moving $P$ by a reflection or a rotation that keeps its distance $r$ from $O$ (you will meet these transformations again in chapter 9).

```figure caption="The point $P(x,y)$ on the terminal side of $\theta$ and its images. Reflection in the $x$-axis gives $(x,-y)$ for $-\theta$; reflection in the $y$-axis gives $(-x,y)$ for $180^\circ-\theta$; a half turn gives $(-x,-y)$ for $180^\circ+\theta$; a quarter turn anticlockwise gives $(-y,x)$ for $90^\circ+\theta$."
fig, ax = plt.subplots(figsize=(4.6, 3.6))
t = np.linspace(0, 2*np.pi, 300)
ax.plot(np.cos(t), np.sin(t), color=GRID, lw=1.2)
ax.axhline(0, color=INK, lw=0.9); ax.axvline(0, color=INK, lw=0.9)
th = np.radians(28); x, y = np.cos(th), np.sin(th)
pts = [((x, y), 'P(x, y) : θ', INK, (0.05, 0.04), 'left'), ((x, -y), '(x, −y) : −θ', SERIES[1], (0.05, -0.12), 'left'),
       ((-x, y), '(−x, y) : 180° − θ', SERIES[2], (-0.05, 0.04), 'right'), ((-x, -y), '(−x, −y) : 180° + θ', SERIES[3], (-0.05, -0.12), 'right'),
       ((-y, x), '(−y, x) : 90° + θ', ACCENT, (-0.05, 0.06), 'right')]
for (px, py), lab, c, (dx, dy), ha in pts:
    ax.plot([0, px], [0, py], color=c, lw=1.3)
    ax.plot(px, py, 'o', color=c, ms=4.5)
    ax.text(px + dx, py + dy, lab, fontsize=8, color=c, ha=ha)
ax.set_xlim(-1.75, 1.75); ax.set_ylim(-1.15, 1.15); ax.set_aspect('equal'); ax.axis('off')
fig.tight_layout(pad=0.3)
```

Reading the ratios from the new coordinates (with the same $r$) gives every rule at once:

| Angle | New point | sin | cos | tan |
|---|---|---|---|---|
| $-\theta$ | $(x,-y)$ | $-\sin\theta$ | $\cos\theta$ | $-\tan\theta$ |
| $90^\circ-\theta$ | $(y,x)$ | $\cos\theta$ | $\sin\theta$ | $\cot\theta$ |
| $90^\circ+\theta$ | $(-y,x)$ | $\cos\theta$ | $-\sin\theta$ | $-\cot\theta$ |
| $180^\circ-\theta$ | $(-x,y)$ | $\sin\theta$ | $-\cos\theta$ | $-\tan\theta$ |
| $180^\circ+\theta$ | $(-x,-y)$ | $-\sin\theta$ | $-\cos\theta$ | $\tan\theta$ |

For example, for $90^\circ+\theta$ the new point is $(-y,x)$, so $\sin(90^\circ+\theta)=\frac{x}{r}=\cos\theta$ and $\cos(90^\circ+\theta)=\frac{-y}{r}=-\sin\theta$. For $90^\circ-\theta$, the two acute angles of one right triangle are $\theta$ and $90^\circ-\theta$, so the perpendicular of one is the base of the other: the sine of one is the cosine of the other.

::: key The two-step rule for allied angles
**Step 1 — the name.** With $90^\circ\pm\theta$ the ratio **changes** to its partner ($\sin\leftrightarrow\cos$, $\tan\leftrightarrow\cot$, $\mathrm{cosec}\leftrightarrow\sec$). With $180^\circ\pm\theta$ or $-\theta$ the name **stays the same**.

**Step 2 — the sign.** Treat $\theta$ as a small acute angle, find the quadrant of the whole angle, and use ASTC to decide whether the original ratio is positive or negative there.

Example: $\cos(90^\circ+\theta)$. The name changes to $\sin$; $90^\circ+\theta$ is in quadrant II, where cosine is negative. So $\cos(90^\circ+\theta)=-\sin\theta$.
:::

::: example Ratios of larger angles
**Problem.** Find the values of $\sin120^\circ$, $\cos135^\circ$, $\tan150^\circ$, $\sin210^\circ$, $\cos240^\circ$ and $\tan225^\circ$.

**Solution.** Write each angle as $180^\circ\pm$ (a standard angle):

$\sin120^\circ=\sin(180^\circ-60^\circ)=\sin60^\circ=\frac{\sqrt{3}}{2}$ (quadrant II, sine positive).

$\cos135^\circ=\cos(180^\circ-45^\circ)=-\cos45^\circ=-\frac{1}{\sqrt{2}}$.

$\tan150^\circ=\tan(180^\circ-30^\circ)=-\tan30^\circ=-\frac{1}{\sqrt{3}}$.

$\sin210^\circ=\sin(180^\circ+30^\circ)=-\sin30^\circ=-\frac{1}{2}$ (quadrant III, sine negative).

$\cos240^\circ=\cos(180^\circ+60^\circ)=-\cos60^\circ=-\frac{1}{2}$.

$\tan225^\circ=\tan(180^\circ+45^\circ)=\tan45^\circ=1$ (quadrant III, tangent positive).

**Check one another way.** $\sin120^\circ=\sin(90^\circ+30^\circ)=\cos30^\circ=\frac{\sqrt{3}}{2}$, the same.
:::

::: example Negative angles
**Problem.** Find $\cos(-60^\circ)$, $\sin(-45^\circ)$ and $\tan(-30^\circ)$.

**Solution.** $\cos(-60^\circ)=\cos60^\circ=\frac{1}{2}$; $\sin(-45^\circ)=-\sin45^\circ=-\frac{1}{\sqrt{2}}$; $\tan(-30^\circ)=-\tan30^\circ=-\frac{1}{\sqrt{3}}$. Turning clockwise into quadrant IV, only the cosine stays positive.
:::

::: example Simplifying with allied angles
**Problem.** (i) Evaluate $\sin150^\circ+\cos120^\circ-\tan135^\circ$. (ii) Show that $\sin(90^\circ+\theta)\cos(180^\circ-\theta)+\cos(90^\circ+\theta)\sin(180^\circ-\theta)=-1$.

**Solution.** (i) $\sin150^\circ=\sin30^\circ=\frac{1}{2}$, $\cos120^\circ=-\cos60^\circ=-\frac{1}{2}$, $\tan135^\circ=-\tan45^\circ=-1$. So the value is $\frac{1}{2}-\frac{1}{2}-(-1)=1$.

(ii) Replace each ratio:
$$ \text{LHS}=\cos\theta\,(-\cos\theta)+(-\sin\theta)\sin\theta=-(\cos^2\theta+\sin^2\theta)=-1=\text{RHS} $$
:::

## 7.6 Height and distance with one angle of elevation or depression

### Angles of elevation and depression

When you look at an object, the straight line from your eye to the object is the **line of sight**. The angle is always measured from the **horizontal line** through your eye.

::: definition Angle of elevation and angle of depression
If the object is **above** the horizontal through the eye, the angle between the line of sight and the horizontal is the **angle of elevation**. If the object is **below** it, the angle between the horizontal and the line of sight is the **angle of depression**.
:::

```figure caption="Left: looking up from $A$ at the top $T$ of a tower, the angle of elevation is measured up from the horizontal $AB$. Right: looking down from the top $C$ of a cliff at a boat $D$, the angle of depression is measured down from the horizontal through $C$; it equals the angle of elevation of $C$ from $D$, because the two horizontals are parallel (alternate angles)."
from matplotlib.patches import Arc
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(5.0, 2.7))
A, B, T = (0, 0), (3.2, 0), (3.2, 2.4)
ax1.plot([A[0], B[0]], [0, 0], color=INK, lw=1.2)
ax1.plot([B[0], T[0]], [0, T[1]], color=INK, lw=2.4)
ax1.plot([A[0], T[0]], [0, T[1]], color=ACCENT, lw=1.3, ls='--')
ax1.add_patch(Arc(A, 1.3, 1.3, theta1=0, theta2=np.degrees(np.arctan2(2.4, 3.2)), color=SERIES[1], lw=1.3))
ax1.text(0.72, 0.16, 'θ', fontsize=10, color=SERIES[1])
ax1.text(0.9, 1.15, 'line of sight', fontsize=8, color=ACCENT, rotation=36.9)
ax1.text(1.6, -0.35, 'horizontal distance', ha='center', fontsize=8)
ax1.text(3.35, 1.2, 'height', fontsize=8, va='center')
for p, lab, dx in [(A, 'A', -0.2), (B, 'B', 0.12), (T, 'T', 0.12)]:
    ax1.text(p[0] + dx, p[1] - 0.05 if p != T else p[1], lab, fontsize=9)
ax1.set_title('angle of elevation', fontsize=8.5, pad=3)
ax1.set_xlim(-0.4, 4.6); ax1.set_ylim(-0.6, 2.8); ax1.set_aspect('equal'); ax1.axis('off')
C, F, D = (0, 2.4), (0, 0), (3.2, 0)
ax2.plot([0, 0], [0, 2.4], color=INK, lw=2.4)
ax2.plot([0, 3.6], [0, 0], color=INK, lw=1.2)
ax2.plot([0, 3.6], [2.4, 2.4], color=MUTED, lw=1.0, ls=':')
ax2.plot([C[0], D[0]], [C[1], D[1]], color=ACCENT, lw=1.3, ls='--')
ang = np.degrees(np.arctan2(2.4, 3.2))
ax2.add_patch(Arc(C, 1.3, 1.3, theta1=-ang, theta2=0, color=SERIES[1], lw=1.3))
ax2.text(0.72, 2.12, 'θ', fontsize=10, color=SERIES[1])
ax2.add_patch(Arc(D, 1.3, 1.3, theta1=180 - ang, theta2=180, color=SERIES[1], lw=1.3))
ax2.text(2.38, 0.12, 'θ', fontsize=10, color=SERIES[1])
ax2.text(1.8, 2.52, 'horizontal', fontsize=8, color=MUTED, ha='center')
ax2.text(-0.2, 2.4, 'C', fontsize=9, ha='right'); ax2.text(-0.2, -0.05, 'F', fontsize=9, ha='right'); ax2.text(3.25, -0.3, 'D', fontsize=9)
ax2.set_title('angle of depression', fontsize=8.5, pad=3)
ax2.set_xlim(-0.6, 4.0); ax2.set_ylim(-0.6, 2.8); ax2.set_aspect('equal'); ax2.axis('off')
fig.tight_layout(pad=0.4)
```

### The method

1. **Draw** a neat figure: the object, the observer, the horizontal line, the line of sight, the right angle, and the given angle.
2. **Name** the unknown side (usually $h$ for height or $x$ for distance).
3. **Choose the ratio** that connects the known side and the unknown side with the given angle: $\tan$ when both are the legs (height and horizontal distance), $\sin$ or $\cos$ when the hypotenuse (a ladder, a string, a line of sight) is involved.
4. **Substitute** the standard value and solve. Use $\sqrt{3}\approx1.732$ and $\sqrt{2}\approx1.414$ for a decimal answer, and write the unit.

::: example Height of a tower
**Problem.** The angle of elevation of the top of a tower from a point 30 m from its foot is $60^\circ$. Find the height of the tower.

**Solution.** Let the height be $h$ m. In the right triangle, the height is opposite the $60^\circ$ angle and the 30 m distance is next to it, so use $\tan$:
$$ \tan60^\circ=\frac{h}{30}\ \Rightarrow\ h=30\tan60^\circ=30\sqrt{3}\approx30\times1.732=51.96 \text{ m} $$
:::

::: example A ladder and a kite string
**Problem.** (i) A ladder 10 m long rests against a wall and makes an angle of $60^\circ$ with the ground. How high up the wall does it reach, and how far is its foot from the wall? (ii) A kite is flying on a string 100 m long that makes an angle of $30^\circ$ with the ground. How high is the kite?

**Solution.** (i) The ladder is the hypotenuse. Height: $\sin60^\circ=\frac{h}{10}$, so $h=10\times\frac{\sqrt{3}}{2}=5\sqrt{3}\approx8.66$ m. Distance of the foot: $\cos60^\circ=\frac{d}{10}$, so $d=10\times\frac{1}{2}=5$ m.

(ii) The string is the hypotenuse and the height is opposite $30^\circ$: $h=100\sin30^\circ=100\times\frac{1}{2}=50$ m.
:::

::: example From a shadow to the sun's elevation
**Problem.** A vertical pole 12 m high casts a shadow $12\sqrt{3}$ m long on level ground. Find the angle of elevation of the sun.

**Solution.** The pole and its shadow are the two legs of a right triangle, with the sun's rays as the hypotenuse:
$$ \tan\theta=\frac{12}{12\sqrt{3}}=\frac{1}{\sqrt{3}}\ \Rightarrow\ \theta=30^\circ $$
When the shadow is exactly as long as the pole, $\tan\theta=1$ and the sun is at $45^\circ$.
:::

::: example An angle of depression
**Problem.** From the top of a cliff 45 m high, the angle of depression of a boat on the lake is $30^\circ$. Find the distance of the boat from the foot of the cliff, and the length of the line of sight.

**Solution.** The angle of depression at the top equals the angle of elevation at the boat (alternate angles), so the angle at the boat is $30^\circ$. Let the distance be $x$ m:
$$ \tan30^\circ=\frac{45}{x}\ \Rightarrow\ x=\frac{45}{\tan30^\circ}=45\sqrt{3}\approx77.94 \text{ m} $$
Line of sight: $\sin30^\circ=\frac{45}{l}$, so $l=\frac{45}{\frac{1}{2}}=90$ m.
:::

::: example Remember the observer's height
**Problem.** A boy whose eyes are 1.5 m above the ground stands 20 m from a flagpole. The angle of elevation of the top of the pole from his eyes is $45^\circ$. Find the height of the pole.

**Solution.** The angle is measured from the horizontal through his **eyes**, 1.5 m above the ground. The part of the pole above eye level is $h_1$, with $\tan45^\circ=\frac{h_1}{20}$, so $h_1=20$ m. The height of the pole is $20+1.5=21.5$ m.
:::

::: caution Depression is measured from the horizontal, not from the vertical
The angle of depression is the angle **between the horizontal line and the line of sight**. It is not the angle between the cliff and the line of sight. In a depression problem, put the given angle at the observer against the horizontal, then transfer it to the object on the ground as an alternate angle. A wrong placement turns $30^\circ$ into $60^\circ$ and gives the wrong side.
:::

::: note Project — make a clinometer and measure the school building
A **clinometer** measures angles of elevation. Tape a drinking straw along the straight edge of a protractor, and hang a small stone on a thread from the centre of the protractor. Look at the top of the school building (or a tall tree) through the straw. The thread hangs vertically; the angle between the thread and the $90^\circ$ mark is the angle of elevation. (1) Measure your distance from the foot of the building with a tape, and your eye height. (2) Draw the figure and find the height with $\tan$. (3) Repeat from a second distance. Do your two answers agree? Which errors could explain the difference? (Never look at the sun through the straw.)
:::

## Chapter summary

- Right angle $=90^\circ=100^g=\left(\frac{\pi}{2}\right)^c$; $1^\circ=60'$, $1'=60''$; $1^g=100^c$, $1^c=100^{cc}$; $\pi^c=180^\circ=200^g$; $\frac{D}{90}=\frac{G}{100}=\frac{2R}{\pi}$; arc $l=r\theta$.
- $\sin\theta=\frac{p}{h}$, $\cos\theta=\frac{b}{h}$, $\tan\theta=\frac{p}{b}$; cosec, sec and cot are their reciprocals; $\tan\theta=\frac{\sin\theta}{\cos\theta}$.
- $\sin^2\theta+\cos^2\theta=1$, $1+\tan^2\theta=\sec^2\theta$, $1+\cot^2\theta=\mathrm{cosec}^2\theta$; prove identities from one side, one change per line.
- $\sin0^\circ, \sin30^\circ, \sin45^\circ, \sin60^\circ, \sin90^\circ=0, \frac{1}{2}, \frac{1}{\sqrt{2}}, \frac{\sqrt{3}}{2}, 1$; cosines in reverse order; $\tan45^\circ=1$, $\tan60^\circ=\sqrt{3}$, $\tan90^\circ$ not defined.
- Signs by quadrant: All, Sin, Tan, Cos.
- $\sin(-\theta)=-\sin\theta$, $\cos(-\theta)=\cos\theta$; with $90^\circ\pm\theta$ the ratio changes to its partner, with $180^\circ\pm\theta$ it keeps its name; the sign comes from the quadrant.
- Elevation and depression are measured from the horizontal; the depression from $A$ to $B$ equals the elevation from $B$ to $A$. Use $\tan$ for height and distance, $\sin$ or $\cos$ with a hypotenuse, and add the observer's eye height.

## Practice questions

**Group A — Objective (1 mark each)**

1. One right angle in the centesimal system is <span class="marks">[1]</span>
   (a) $90^g$ (b) $100^g$ (c) $60^g$ (d) $180^g$
2. $\pi^c$ is equal to <span class="marks">[1]</span>
   (a) $90^\circ$ (b) $180^\circ$ (c) $360^\circ$ (d) $57.3^\circ$
3. $45^\circ$ expressed in grades is <span class="marks">[1]</span>
   (a) $40^g$ (b) $45^g$ (c) $50^g$ (d) $60^g$
4. In a right-angled triangle, $\sin\theta$ is <span class="marks">[1]</span>
   (a) $\frac{b}{h}$ (b) $\frac{p}{h}$ (c) $\frac{p}{b}$ (d) $\frac{h}{p}$
5. If $\tan\theta=\frac{3}{4}$, then $\cot\theta$ is <span class="marks">[1]</span>
   (a) $\frac{4}{3}$ (b) $\frac{3}{5}$ (c) $\frac{4}{5}$ (d) $\frac{5}{3}$
6. $\sin^2\theta+\cos^2\theta$ is equal to <span class="marks">[1]</span>
   (a) 0 (b) 1 (c) 2 (d) $\tan^2\theta$
7. $\sec^2\theta-\tan^2\theta$ is equal to <span class="marks">[1]</span>
   (a) 0 (b) $-1$ (c) 1 (d) $\cot^2\theta$
8. The value of $\sin30^\circ+\cos60^\circ$ is <span class="marks">[1]</span>
   (a) $\frac{1}{2}$ (b) 1 (c) $\sqrt{3}$ (d) 0
9. $\tan45^\circ$ is equal to <span class="marks">[1]</span>
   (a) 0 (b) $\frac{1}{\sqrt{3}}$ (c) 1 (d) $\sqrt{3}$
10. $\sin(90^\circ-\theta)$ is equal to <span class="marks">[1]</span>
    (a) $\sin\theta$ (b) $-\cos\theta$ (c) $\cos\theta$ (d) $-\sin\theta$
11. $\cos(180^\circ-\theta)$ is equal to <span class="marks">[1]</span>
    (a) $\cos\theta$ (b) $-\cos\theta$ (c) $\sin\theta$ (d) $-\sin\theta$
12. When the shadow of a pole is equal to its height, the angle of elevation of the sun is <span class="marks">[1]</span>
    (a) $30^\circ$ (b) $45^\circ$ (c) $60^\circ$ (d) $90^\circ$

::: note Answers to Group A
**1.** (b) — the centesimal system divides the right angle into 100 grades.
**2.** (b) — half a turn is $\pi$ radians and $180^\circ$.
**3.** (c) — $45\times\frac{10}{9}=50^g$.
**4.** (b) — perpendicular over hypotenuse.
**5.** (a) — $\cot\theta=\frac{1}{\tan\theta}$.
**6.** (b) — the fundamental identity.
**7.** (c) — from $1+\tan^2\theta=\sec^2\theta$.
**8.** (b) — $\frac{1}{2}+\frac{1}{2}=1$.
**9.** (c) — in the half-square triangle the legs are equal.
**10.** (c) — complementary angles: sine of one is cosine of the other.
**11.** (b) — $180^\circ-\theta$ is in quadrant II, where cosine is negative.
**12.** (b) — $\tan\theta=1$, so $\theta=45^\circ$.
:::

**Group B — Short answer (2 marks each)**

1. Convert $67^\circ30'$ into grades. <span class="marks">[2]</span>
2. Convert $\left(\frac{3\pi}{5}\right)^c$ into degrees and into grades. <span class="marks">[2]</span>
3. Two angles of a triangle are $60^\circ$ and $50^g$. Find the third angle in radians. <span class="marks">[2]</span>
4. If $\sin\theta=\frac{5}{13}$ and $\theta$ is acute, find $\cos\theta$ and $\tan\theta$. <span class="marks">[2]</span>
5. Prove that $(1-\sin^2\theta)\sec^2\theta=1$. <span class="marks">[2]</span>
6. Prove that $\tan\theta+\cot\theta=\sec\theta\,\mathrm{cosec}\,\theta$. <span class="marks">[2]</span>
7. Find the value of $\tan^260^\circ+2\tan^245^\circ$. <span class="marks">[2]</span>
8. Find the values of $\sin120^\circ$ and $\cos135^\circ$. <span class="marks">[2]</span>
9. Find the acute angle $\theta$ if $2\cos\theta=1$. <span class="marks">[2]</span>
10. A ladder 10 m long makes an angle of $60^\circ$ with the ground. How high up the wall does it reach? <span class="marks">[2]</span>

::: note Answers to Group B
**1.** $30'=0.5^\circ$, so the angle is $67.5^\circ$, and $67.5\times\frac{10}{9}=75^g$.
**2.** $\frac{3\times180^\circ}{5}=108^\circ$ and $\frac{3\times200^g}{5}=120^g$.
**3.** $50^g=45^\circ$, so the third angle is $180^\circ-60^\circ-45^\circ=75^\circ=75\times\frac{\pi}{180}=\frac{5\pi}{12}$ radians.
**4.** $p=5$, $h=13$, $b=\sqrt{169-25}=12$. So $\cos\theta=\frac{12}{13}$ and $\tan\theta=\frac{5}{12}$.
**5.** LHS $=\cos^2\theta\times\frac{1}{\cos^2\theta}=1=$ RHS.
**6.** LHS $=\frac{\sin\theta}{\cos\theta}+\frac{\cos\theta}{\sin\theta}=\frac{\sin^2\theta+\cos^2\theta}{\sin\theta\cos\theta}=\frac{1}{\sin\theta\cos\theta}=\sec\theta\,\mathrm{cosec}\,\theta=$ RHS.
**7.** $(\sqrt{3})^2+2(1)^2=3+2=5$.
**8.** $\sin120^\circ=\sin(180^\circ-60^\circ)=\sin60^\circ=\frac{\sqrt{3}}{2}$; $\cos135^\circ=\cos(180^\circ-45^\circ)=-\cos45^\circ=-\frac{1}{\sqrt{2}}$.
**9.** $\cos\theta=\frac{1}{2}=\cos60^\circ$, so $\theta=60^\circ$.
**10.** $\sin60^\circ=\frac{h}{10}$, so $h=10\times\frac{\sqrt{3}}{2}=5\sqrt{3}\approx8.66$ m.
:::

**Group C — Long answer (4 marks each)**

1. (i) Define one radian. (ii) Show that $\pi^c=180^\circ$. (iii) Express $1^c$ in degrees, minutes and seconds (to the nearest second). (iv) The angles of a triangle are in the ratio $2:3:5$. Find them in degrees, in grades and in radians. <span class="marks">[4]</span>
2. If $\tan\theta=\frac{8}{15}$, find the other trigonometric ratios of the acute angle $\theta$ and verify that $\sin^2\theta+\cos^2\theta=1$ and $\sec^2\theta-\tan^2\theta=1$. <span class="marks">[4]</span>
3. Prove that (i) $\frac{1}{1+\sin\theta}+\frac{1}{1-\sin\theta}=2\sec^2\theta$ (ii) $(\sec\theta-\tan\theta)(\sec\theta+\tan\theta)=1$. <span class="marks">[4]</span>
4. (i) Evaluate $4\sin^230^\circ+3\tan^230^\circ-8\sin45^\circ\cos45^\circ$. (ii) Evaluate $\sin150^\circ+\cos120^\circ-\tan135^\circ$. (iii) Show that $\sin(90^\circ+\theta)\cos(180^\circ-\theta)+\cos(90^\circ+\theta)\sin(180^\circ-\theta)=-1$. <span class="marks">[4]</span>
5. From the top of a cliff 45 m high, the angle of depression of a boat is $30^\circ$. (i) Draw a labelled figure. (ii) Find the distance of the boat from the foot of the cliff. (iii) Find the length of the line of sight from the top of the cliff to the boat. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** (i) One radian is the angle subtended at the centre of a circle by an arc equal in length to the radius. (ii) The circumference $2\pi r$ contains $2\pi$ arcs of length $r$, so a full turn is $2\pi$ radians; a full turn is also $360^\circ$, so $2\pi^c=360^\circ$ and $\pi^c=180^\circ$. (iii) $1^c=\frac{180^\circ}{\pi}\approx57.2958^\circ$; $0.2958^\circ\times60=17.75'$ and $0.75'\times60=45''$, so $1^c\approx57^\circ17'45''$. (iv) The parts are $2+3+5=10$, so the angles are $\frac{2}{10}\times180^\circ=36^\circ$, $54^\circ$ and $90^\circ$; in grades $40^g$, $60^g$, $100^g$; in radians $\frac{\pi}{5}$, $\frac{3\pi}{10}$, $\frac{\pi}{2}$.
**2.** $p=8$, $b=15$, $h=\sqrt{64+225}=17$. So $\sin\theta=\frac{8}{17}$, $\cos\theta=\frac{15}{17}$, $\mathrm{cosec}\,\theta=\frac{17}{8}$, $\sec\theta=\frac{17}{15}$, $\cot\theta=\frac{15}{8}$. Check: $\sin^2\theta+\cos^2\theta=\frac{64}{289}+\frac{225}{289}=\frac{289}{289}=1$ ✓; $\sec^2\theta-\tan^2\theta=\frac{289}{225}-\frac{64}{225}=\frac{225}{225}=1$ ✓.
**3.** (i) LHS $=\frac{(1-\sin\theta)+(1+\sin\theta)}{(1+\sin\theta)(1-\sin\theta)}=\frac{2}{1-\sin^2\theta}=\frac{2}{\cos^2\theta}=2\sec^2\theta=$ RHS. (ii) LHS $=\sec^2\theta-\tan^2\theta$ (difference of two squares) $=1=$ RHS, using $1+\tan^2\theta=\sec^2\theta$.
**4.** (i) $4\left(\frac{1}{2}\right)^2+3\left(\frac{1}{\sqrt{3}}\right)^2-8\cdot\frac{1}{\sqrt{2}}\cdot\frac{1}{\sqrt{2}}=1+1-4=-2$. (ii) $\frac{1}{2}+\left(-\frac{1}{2}\right)-(-1)=1$. (iii) LHS $=\cos\theta(-\cos\theta)+(-\sin\theta)(\sin\theta)=-(\cos^2\theta+\sin^2\theta)=-1=$ RHS.
**5.** (i) A vertical line $CF$ of 45 m for the cliff, a horizontal line through $C$, the boat $D$ on the ground level with $F$, and the line of sight $CD$; the $30^\circ$ angle between the horizontal and $CD$ at $C$, and an equal $30^\circ$ at $D$ (alternate angles). (ii) $\tan30^\circ=\frac{45}{FD}$, so $FD=45\sqrt{3}\approx77.94$ m. (iii) $\sin30^\circ=\frac{45}{CD}$, so $CD=90$ m. Check: $45^2+77.94^2\approx2025+6075=8100=90^2$ ✓.
:::
