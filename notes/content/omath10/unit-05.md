---
subject: Optional Mathematics
grade: 10
unit: 5
title: Conditional Identities, Trigonometric Equations and Height and Distance
hours: 0
area: Units
---

This chapter puts the trigonometry of Chapter 4 to work in three ways. First, when the angles of a triangle satisfy $A+B+C=180^\circ$, a whole family of **conditional identities** becomes true, and you learn to prove them. Second, you learn to **solve trigonometric equations**, finding every angle in a given range that makes an equation true. Third, you use right-angled triangles and trigonometric ratios to find heights and distances that cannot be measured directly: the height of a tower, the width of a river, the distance of a boat from a cliff. This is the part of the course where trigonometry becomes surveying.

::: key What the SEE asks from this chapter
Expect: (i) prove an identity for angles of a triangle ($A+B+C=180^\circ$), such as $\tan A+\tan B+\tan C=\tan A\tan B\tan C$; (ii) solve an equation such as $2\sin^2\theta-\sin\theta-1=0$ for $0^\circ\leq\theta\leq360^\circ$ (give **all** solutions in the range); (iii) a height-and-distance problem with a **figure**, using $\tan\theta$ and often $\tan30^\circ=\frac{1}{\sqrt{3}}$, $\tan60^\circ=\sqrt{3}$. Draw a clear, labelled diagram first; it earns marks on its own.
:::

## 5.1 Conditional trigonometric identities

An identity is true for **all** angles. A **conditional identity** is true only when the angles satisfy a stated condition. The most common condition is that $A$, $B$, $C$ are the angles of a triangle: $A+B+C=180^\circ$.

::: key The conditions behind every proof
If $A+B+C=180^\circ$ then $A+B=180^\circ-C$ and $\frac{A+B}{2}=90^\circ-\frac{C}{2}$. Hence

| | |
|---|---|
| $\sin(A+B)=\sin C$ | $\cos(A+B)=-\cos C$ |
| $\tan(A+B)=-\tan C$ | $\sin\frac{A+B}{2}=\cos\frac{C}{2}$ |
| $\cos\frac{A+B}{2}=\sin\frac{C}{2}$ | $\sin2C=-\sin(2A+2B)$ |

**Method:** (1) group two of the angles, say $A$ and $B$; (2) use sum-to-product on them; (3) replace $A+B$ by $180^\circ-C$ using the table; (4) factor out the common ratio of $C$ and use sum-to-product or product-to-sum again.
:::

::: derivation If $A+B+C=180^\circ$, then $\sin2A+\sin2B+\sin2C=4\sin A\sin B\sin C$
We start from the left side and group the first two terms.

**Step 1 — sum to product on $\sin2A+\sin2B$.**
$$ \sin2A+\sin2B=2\sin(A+B)\cos(A-B) $$

**Step 2 — use $\sin(A+B)=\sin C$.**
$$ \sin2A+\sin2B=2\sin C\cos(A-B) $$

**Step 3 — double angle on the third term.**
$$ \sin2C=2\sin C\cos C $$

**Step 4 — add and factor out $2\sin C$.**
$$ \text{LHS}=2\sin C\left[\cos(A-B)+\cos C\right] $$

**Step 5 — use $\cos C=-\cos(A+B)$.**
$$ \text{LHS}=2\sin C\left[\cos(A-B)-\cos(A+B)\right] $$

**Step 6 — product formula** $\cos(A-B)-\cos(A+B)=2\sin A\sin B$:
$$ \text{LHS}=2\sin C\cdot2\sin A\sin B=4\sin A\sin B\sin C=\text{RHS} $$

**What it means.** The identity holds only for a triangle. Check with the equilateral triangle $A=B=C=60^\circ$: LHS $=3\sin120^\circ=\frac{3\sqrt{3}}{2}$ and RHS $=4\left(\frac{\sqrt{3}}{2}\right)^3=\frac{3\sqrt{3}}{2}$. ✓
:::

::: derivation If $A+B+C=180^\circ$, then $\tan A+\tan B+\tan C=\tan A\tan B\tan C$
We start from $A+B=180^\circ-C$.

**Step 1 — take the tangent of both sides.**
$$ \tan(A+B)=\tan(180^\circ-C)=-\tan C $$

**Step 2 — expand $\tan(A+B)$.**
$$ \frac{\tan A+\tan B}{1-\tan A\tan B}=-\tan C $$

**Step 3 — cross-multiply.**
$$ \tan A+\tan B=-\tan C+\tan A\tan B\tan C $$

**Step 4 — bring $\tan C$ to the left.**
$$ \tan A+\tan B+\tan C=\tan A\tan B\tan C $$

**What it means.** In a triangle, the sum and the product of the three tangents are equal. (It needs no right angle: if one angle is $90^\circ$ its tangent is undefined, so the statement is for non-right triangles.) Check: $A=B=C=60^\circ$ gives $3\sqrt{3}=(\sqrt{3})^3=3\sqrt{3}$. ✓
:::

::: derivation If $A+B+C=180^\circ$, then $\sin A+\sin B+\sin C=4\cos\frac{A}{2}\cos\frac{B}{2}\cos\frac{C}{2}$
We group $A$ and $B$ and use half-angles for $C$.

**Step 1 — sum to product.**
$$ \sin A+\sin B=2\sin\frac{A+B}{2}\cos\frac{A-B}{2}=2\cos\frac{C}{2}\cos\frac{A-B}{2} $$

**Step 2 — double-angle on $\sin C$.**
$$ \sin C=2\sin\frac{C}{2}\cos\frac{C}{2} $$

**Step 3 — add and factor out $2\cos\frac{C}{2}$.**
$$ \text{LHS}=2\cos\frac{C}{2}\left[\cos\frac{A-B}{2}+\sin\frac{C}{2}\right] $$

**Step 4 — use $\sin\frac{C}{2}=\cos\frac{A+B}{2}$.**
$$ \text{LHS}=2\cos\frac{C}{2}\left[\cos\frac{A-B}{2}+\cos\frac{A+B}{2}\right] $$

**Step 5 — sum to product again:** $\cos\frac{A-B}{2}+\cos\frac{A+B}{2}=2\cos\frac{A}{2}\cos\frac{B}{2}$, so
$$ \text{LHS}=4\cos\frac{A}{2}\cos\frac{B}{2}\cos\frac{C}{2}=\text{RHS} $$
:::

::: tip The examiner is looking for
(1) the condition $A+B+C=180^\circ$ written down and used, (2) grouping two angles and using sum-to-product, (3) the replacement such as $\sin(A+B)=\sin C$, (4) the common factor taken out, (5) stopping when the left side **equals** the right side.
:::

::: example Two more triangle identities
**Problem.** If $A+B+C=180^\circ$ prove that (i) $\cos2A+\cos2B+\cos2C=-1-4\cos A\cos B\cos C$; (ii) $\cos A+\cos B+\cos C=1+4\sin\frac{A}{2}\sin\frac{B}{2}\sin\frac{C}{2}$.

**Solution.** (i) $\cos2A+\cos2B=2\cos(A+B)\cos(A-B)=-2\cos C\cos(A-B)$. Also $\cos2C=2\cos^2C-1$. So
$$ \text{LHS}=-2\cos C\cos(A-B)+2\cos^2C-1=2\cos C\left[\cos C-\cos(A-B)\right]-1. $$
Put $\cos C=-\cos(A+B)$: $\cos C-\cos(A-B)=-\left[\cos(A+B)+\cos(A-B)\right]=-2\cos A\cos B$. Hence LHS $=-4\cos A\cos B\cos C-1$.

(ii) $\cos A+\cos B=2\cos\frac{A+B}{2}\cos\frac{A-B}{2}=2\sin\frac{C}{2}\cos\frac{A-B}{2}$, and $\cos C=1-2\sin^2\frac{C}{2}$. So
$$ \text{LHS}=1+2\sin\frac{C}{2}\left[\cos\frac{A-B}{2}-\sin\frac{C}{2}\right]=1+2\sin\frac{C}{2}\left[\cos\frac{A-B}{2}-\cos\frac{A+B}{2}\right]. $$
Since $\cos\frac{A-B}{2}-\cos\frac{A+B}{2}=2\sin\frac{A}{2}\sin\frac{B}{2}$, LHS $=1+4\sin\frac{A}{2}\sin\frac{B}{2}\sin\frac{C}{2}$.
:::

::: example Squares of sines
**Problem.** If $A+B+C=180^\circ$ prove that $\sin^2A+\sin^2B+\sin^2C=2+2\cos A\cos B\cos C$.

**Solution.** $\sin^2A+\sin^2B=1-\frac{\cos2A+\cos2B}{2}$ (since $\sin^2\theta=\frac{1-\cos2\theta}{2}$). From part (i) above, $\cos2A+\cos2B=-2\cos C\cos(A-B)$, so
$$ \sin^2A+\sin^2B=1+\cos C\cos(A-B). $$
Add $\sin^2C=1-\cos^2C$: LHS $=2+\cos C\left[\cos(A-B)-\cos C\right]$. With $\cos C=-\cos(A+B)$: $\cos(A-B)+\cos(A+B)=2\cos A\cos B$, so LHS $=2+\cos C\cdot2\cos A\cos B=2+2\cos A\cos B\cos C$.
:::

::: example Angles adding to $90^\circ$
**Problem.** If $A+B+C=90^\circ$, prove that $\tan A\tan B+\tan B\tan C+\tan C\tan A=1$.

**Solution.** $A+B=90^\circ-C$, so $\tan(A+B)=\cot C=\frac{1}{\tan C}$:
$$ \frac{\tan A+\tan B}{1-\tan A\tan B}=\frac{1}{\tan C} \;\Rightarrow\; \tan C(\tan A+\tan B)=1-\tan A\tan B. $$
Hence $\tan A\tan C+\tan B\tan C+\tan A\tan B=1$.
:::

::: caution Common mistakes
- Using the condition in a problem where it is not given. $\sin2A+\sin2B+\sin2C=4\sin A\sin B\sin C$ is **false** for general angles.
- Writing $\cos(A+B)=\cos C$. Because $A+B=180^\circ-C$, $\cos(A+B)=-\cos C$; only the **sine** keeps its sign.
- Proving by assuming the result and working on both sides at once. Work on one side and arrive at the other.
- Using $A+B+C=90^\circ$ and $180^\circ$ conditions interchangeably.
:::

## 5.2 Trigonometric equations

A **trigonometric equation** is true only for certain angles. To **solve** it means to find all angles in the stated range. Always read the range: $0^\circ\leq\theta\leq90^\circ$ gives one answer, while $0^\circ\leq\theta\leq360^\circ$ often gives two or more.

### Principal value and the other angle

Find the **acute angle** $\alpha$ (the **principal value**) from the positive value of the ratio, then use the quadrant rule (**A**ll, **S**ine, **T**an, **C**os: the letter shows which ratio is positive in the quadrants 1, 2, 3, 4).

| Equation | Solutions in $0^\circ\leq\theta\leq360^\circ$ |
|---|---|
| $\sin\theta=+k$ | $\alpha$ and $180^\circ-\alpha$ |
| $\sin\theta=-k$ | $180^\circ+\alpha$ and $360^\circ-\alpha$ |
| $\cos\theta=+k$ | $\alpha$ and $360^\circ-\alpha$ |
| $\cos\theta=-k$ | $180^\circ-\alpha$ and $180^\circ+\alpha$ |
| $\tan\theta=+k$ | $\alpha$ and $180^\circ+\alpha$ |
| $\tan\theta=-k$ | $180^\circ-\alpha$ and $360^\circ-\alpha$ |

```figure caption="The solutions are the points where the graph meets a horizontal line. Left: $\sin\theta=\frac{1}{2}$ in $0^\circ\leq\theta\leq360^\circ$ gives $30^\circ$ and $150^\circ$. Right: $\cos\theta=-\frac{1}{2}$ gives $120^\circ$ and $240^\circ$."
x = np.linspace(0, 360, 400)
fig, (a1, a2) = plt.subplots(1, 2, figsize=(4.8, 2.5), sharey=True)
a1.plot(x, np.sin(np.radians(x)), color=ACCENT, lw=1.4); a1.axhline(0.5, color=SERIES[1], lw=1.1)
a1.plot([30, 150], [0.5, 0.5], 'o', color=INK, ms=4)
a1.set_title('y = sin θ,  line y = 1/2', fontsize=7.5)
a2.plot(x, np.cos(np.radians(x)), color=ACCENT, lw=1.4); a2.axhline(-0.5, color=SERIES[1], lw=1.1)
a2.plot([120, 240], [-0.5, -0.5], 'o', color=INK, ms=4)
a2.set_title('y = cos θ,  line y = -1/2', fontsize=7.5)
for a, pts in ((a1, (30, 150)), (a2, (120, 240))):
    a.axhline(0, color=INK, lw=0.6); a.set_xlim(0, 360); a.set_ylim(-1.35, 1.35)
    a.set_xticks([0, 90, 180, 270, 360]); a.tick_params(labelsize=6.5); a.grid(color=GRID, lw=0.4)
    a.spines[['top','right']].set_visible(False)
a1.text(30, 0.72, '30°', ha='center', fontsize=7); a1.text(150, 0.72, '150°', ha='center', fontsize=7)
a2.text(120, -1.25, '120°', ha='center', fontsize=7); a2.text(240, -1.25, '240°', ha='center', fontsize=7)
fig.tight_layout(pad=0.3)
```

::: example Basic equations
**Problem.** Solve for $0^\circ\leq\theta\leq360^\circ$: (i) $2\sin\theta-1=0$; (ii) $2\cos\theta+1=0$; (iii) $\sqrt{3}\tan\theta=1$.

**Solution.** (i) $\sin\theta=\frac{1}{2}$. The principal value is $30^\circ$, and sine is positive in quadrants 1 and 2: $\theta=30^\circ$ or $180^\circ-30^\circ=150^\circ$.

(ii) $\cos\theta=-\frac{1}{2}$. The principal value is $60^\circ$. Cosine is negative in quadrants 2 and 3: $\theta=180^\circ-60^\circ=120^\circ$ or $180^\circ+60^\circ=240^\circ$.

(iii) $\tan\theta=\frac{1}{\sqrt{3}}$, principal value $30^\circ$. Tangent is positive in quadrants 1 and 3: $\theta=30^\circ$ or $180^\circ+30^\circ=210^\circ$.
:::

::: example Equations with a square
**Problem.** Solve $4\sin^2\theta=\tan^260^\circ$ for $0^\circ\leq\theta\leq180^\circ$.

**Solution.** $\tan^260^\circ=3$, so $\sin^2\theta=\frac{3}{4}$ and $\sin\theta=\pm\frac{\sqrt{3}}{2}$. In $0^\circ\leq\theta\leq180^\circ$ sine is never negative, so $\sin\theta=\frac{\sqrt{3}}{2}$: $\theta=60^\circ$ or $120^\circ$.

(For $0^\circ\leq\theta\leq360^\circ$ the negative value would add $240^\circ$ and $300^\circ$.)
:::

### Quadratic in one ratio

When the equation contains one ratio in a quadratic form, treat that ratio as the unknown, factorise, and solve each factor. Reject any value outside $-1\leq\sin\theta\leq1$ (or the cosine range).

::: example Quadratic in $\sin\theta$
**Problem.** Solve $2\sin^2\theta-\sin\theta-1=0$ for $0^\circ\leq\theta\leq360^\circ$.

**Solution.** Let $s=\sin\theta$: $2s^2-s-1=(2s+1)(s-1)=0$, so $s=-\frac{1}{2}$ or $s=1$.

$\sin\theta=1$: $\theta=90^\circ$.

$\sin\theta=-\frac{1}{2}$: principal value $30^\circ$; sine is negative in quadrants 3 and 4: $\theta=180^\circ+30^\circ=210^\circ$ or $360^\circ-30^\circ=330^\circ$.

Solutions: $\theta=90^\circ,\ 210^\circ,\ 330^\circ$.
:::

### Using identities first

If two different ratios appear, use an identity ($\cos2\theta$, $\sin^2\theta+\cos^2\theta=1$, $\csc\theta=\frac{1}{\sin\theta}$) to make **one** ratio.

::: example Using $\cos2\theta$
**Problem.** Solve $\cos2\theta=\sin\theta$ for $0^\circ\leq\theta\leq360^\circ$.

**Solution.** Use $\cos2\theta=1-2\sin^2\theta$: $1-2\sin^2\theta=\sin\theta$, so $2\sin^2\theta+\sin\theta-1=0$, $(2\sin\theta-1)(\sin\theta+1)=0$.

$\sin\theta=\frac{1}{2}$: $\theta=30^\circ,\ 150^\circ$. $\sin\theta=-1$: $\theta=270^\circ$.

Solutions: $30^\circ,\ 150^\circ,\ 270^\circ$.
:::

::: example Mixed ratios
**Problem.** Solve $2\cos^2\theta+3\sin\theta=3$ for $0^\circ\leq\theta\leq360^\circ$.

**Solution.** Replace $\cos^2\theta=1-\sin^2\theta$: $2-2\sin^2\theta+3\sin\theta=3$, so $2\sin^2\theta-3\sin\theta+1=0$, $(2\sin\theta-1)(\sin\theta-1)=0$.

$\sin\theta=\frac{1}{2}$: $30^\circ,\ 150^\circ$. $\sin\theta=1$: $90^\circ$. Solutions: $30^\circ,\ 90^\circ,\ 150^\circ$.
:::

::: example Do not divide by a ratio
**Problem.** Solve $\sin2\theta=\sin\theta$ for $0^\circ\leq\theta\leq180^\circ$.

**Solution.** $2\sin\theta\cos\theta=\sin\theta\Rightarrow\sin\theta\,(2\cos\theta-1)=0$.

$\sin\theta=0$: $\theta=0^\circ,\ 180^\circ$. $\cos\theta=\frac{1}{2}$: $\theta=60^\circ$.

Solutions: $0^\circ,\ 60^\circ,\ 180^\circ$. Dividing by $\sin\theta$ would have lost $0^\circ$ and $180^\circ$.
:::

::: example Cosecant equation
**Problem.** Solve $\csc\theta-2\sin\theta=1$ for $0^\circ\leq\theta\leq180^\circ$.

**Solution.** $\frac{1}{\sin\theta}-2\sin\theta=1\Rightarrow1-2\sin^2\theta=\sin\theta\Rightarrow2\sin^2\theta+\sin\theta-1=0$, i.e. $(2\sin\theta-1)(\sin\theta+1)=0$.

$\sin\theta=\frac{1}{2}$: $30^\circ,\ 150^\circ$. $\sin\theta=-1$ gives $270^\circ$, outside the range.

Solutions: $\theta=30^\circ,\ 150^\circ$.
:::

::: caution Common mistakes
- Giving only the principal value when the range allows more. Always check the other quadrant.
- Dividing both sides by $\sin\theta$ (or $\cos\theta$): this loses the solutions of $\sin\theta=0$. Factorise instead.
- Accepting $\sin\theta=2$ or $\cos\theta=-1.5$. Sine and cosine lie between $-1$ and $1$.
- Forgetting to check the stated range, for example giving $210^\circ$ when the range is $0^\circ$ to $180^\circ$.
:::

::: example Equations in $\tan\theta$ and $\cos\theta$
**Problem.** Solve for $0^\circ\leq\theta\leq360^\circ$: (i) $3\tan^2\theta=1$; (ii) $2\cos^2\theta-3\cos\theta+1=0$.

**Solution.** (i) $\tan^2\theta=\frac{1}{3}$, so $\tan\theta=\pm\frac{1}{\sqrt{3}}$. For $+\frac{1}{\sqrt{3}}$: $30^\circ,\ 210^\circ$. For $-\frac{1}{\sqrt{3}}$: $180^\circ-30^\circ=150^\circ$ and $360^\circ-30^\circ=330^\circ$. Solutions: $30^\circ,\ 150^\circ,\ 210^\circ,\ 330^\circ$.

(ii) $(2\cos\theta-1)(\cos\theta-1)=0$. $\cos\theta=\frac{1}{2}$: $\theta=60^\circ,\ 300^\circ$. $\cos\theta=1$: $\theta=0^\circ,\ 360^\circ$. Solutions: $0^\circ,\ 60^\circ,\ 300^\circ,\ 360^\circ$.
:::

## 5.3 Height and distance

Heights of towers, trees, hills and the width of rivers can be found **without climbing or crossing**, by measuring an angle and a distance on level ground and using a right-angled triangle.

::: definition Angles of elevation and depression
The **angle of elevation** of an object is the angle between the horizontal line through the observer's eye and the line of sight, when the object is **above** the horizontal. The **angle of depression** is the angle between the horizontal and the line of sight, when the object is **below** the horizontal.
:::

```figure caption="Angle of elevation $\theta$ (object $P$ above the observer's horizontal) and angle of depression $\alpha$ (object $Q$ below it). The angle of depression of $Q$ from $O$ equals the angle of elevation of $O$ from $Q$ (alternate angles)."
from matplotlib.patches import Arc
fig, ax = plt.subplots(figsize=(4.6, 2.9))
ax.plot([0, 10], [0, 0], color=INK, lw=1.0, ls='--')
ax.plot([0, 8], [0, 3.6], color=ACCENT, lw=1.5)
ax.plot([0, 8], [0, -2.8], color=SERIES[1], lw=1.5)
ax.add_patch(Arc((0, 0), 4.4, 4.4, theta1=0, theta2=24.2, color=ACCENT, lw=1.1))
ax.add_patch(Arc((0, 0), 4.4, 4.4, theta1=-19.3, theta2=0, color=SERIES[1], lw=1.1))
ax.text(2.9, 0.72, 'θ', color=ACCENT, fontsize=9)
ax.text(2.9, -0.95, 'α', color=SERIES[1], fontsize=9)
ax.plot([0], [0], 'ko', ms=4)
ax.text(-0.3, 0.4, 'O (observer)', ha='right', fontsize=8)
ax.text(8.2, 3.6, 'P (above)', va='center', fontsize=8)
ax.text(8.2, -2.8, 'Q (below)', va='center', fontsize=8)
ax.text(10.2, 0, 'horizontal', va='center', fontsize=8, color=MUTED)
ax.set_xlim(-3.2, 12.4); ax.set_ylim(-3.6, 4.4); ax.set_aspect('equal'); ax.axis('off')
fig.tight_layout(pad=0.3)
```

::: key Working rules
In a right-angled triangle with angle $\theta$:
$$ \sin\theta=\frac{\text{opposite}}{\text{hypotenuse}},\quad \cos\theta=\frac{\text{adjacent}}{\text{hypotenuse}},\quad \tan\theta=\frac{\text{opposite}}{\text{adjacent}} $$
- For height $h$ and horizontal distance $d$: $\tan\theta=\frac{h}{d}$, so $h=d\tan\theta$.
- Always draw the figure, mark the right angle, mark the angles of elevation or depression from the **horizontal**, and label the unknown.
- Useful: $\tan30^\circ=\frac{1}{\sqrt{3}}$, $\tan45^\circ=1$, $\tan60^\circ=\sqrt{3}$, with $\sqrt{3}\approx1.732$.
:::

::: example Height of a tower
**Problem.** From a point 50 m from the foot of a tower, the angle of elevation of the top of the tower is $60^\circ$. Find the height of the tower.

**Solution.** $\tan60^\circ=\frac{h}{50}$, so $h=50\sqrt{3}\approx50\times1.732=86.6$ m.
:::

::: example Angle of depression
**Problem.** From the top of a cliff 60 m high, the angle of depression of a boat is $30^\circ$. How far is the boat from the foot of the cliff?

**Solution.** The angle of elevation of the top of the cliff from the boat is also $30^\circ$ (alternate angles). Let the distance be $d$: $\tan30^\circ=\frac{60}{d}$, so $d=\frac{60}{\tan30^\circ}=60\sqrt{3}\approx103.9$ m.
:::

::: example Ladder
**Problem.** A 10 m ladder leans against a wall and makes an angle of $60^\circ$ with the ground. How high does it reach and how far is its foot from the wall?

**Solution.** The ladder is the hypotenuse. Height $=10\sin60^\circ=10\cdot\frac{\sqrt{3}}{2}=5\sqrt{3}\approx8.66$ m. Distance of the foot $=10\cos60^\circ=5$ m.
:::

::: example Two positions
**Problem.** The angle of elevation of the top of a tower from a point $A$ on the ground is $30^\circ$. On moving 100 m **towards** the tower to a point $B$, the angle of elevation is $60^\circ$. Find the height of the tower and the original distance $AC$ from its foot $C$.

**Solution.** Let the height be $h$ and $BC=x$. In triangle $BCT$: $\tan60^\circ=\frac{h}{x}\Rightarrow x=\frac{h}{\sqrt{3}}$. In triangle $ACT$: $\tan30^\circ=\frac{h}{x+100}\Rightarrow x+100=h\sqrt{3}$.

Substituting $x=\frac{h}{\sqrt{3}}$: $\frac{h}{\sqrt{3}}+100=h\sqrt{3}\Rightarrow100=h\sqrt{3}-\frac{h}{\sqrt{3}}=\frac{3h-h}{\sqrt{3}}=\frac{2h}{\sqrt{3}}$.

So $h=50\sqrt{3}\approx86.6$ m. Then $x=\frac{h}{\sqrt{3}}=50$ m and $AC=x+100=150$ m.

Check: $\tan30^\circ=\frac{86.6}{150}=0.577$ ✓.
:::

```figure caption="Two-position problem: the angle of elevation is $30^\circ$ from $A$ and $60^\circ$ from $B$ with $AB=100$ m. The tower is $50\sqrt{3}\approx86.6$ m high and $BC=50$ m, $AC=150$ m."
from matplotlib.patches import Arc, Rectangle
fig, ax = plt.subplots(figsize=(4.8, 2.6))
h = 50*np.sqrt(3)
ax.plot([0, 165], [0, 0], color=INK, lw=1.0)
ax.plot([0, 0], [0, h], color=INK, lw=2.2)
ax.plot([0, 150], [h, 0], color=SERIES[1], lw=1.2)
ax.plot([0, 50], [h, 0], color=ACCENT, lw=1.2)
ax.add_patch(Arc((150, 0), 40, 40, theta1=150, theta2=180, color=SERIES[1], lw=1))
ax.add_patch(Arc((50, 0), 28, 28, theta1=120, theta2=180, color=ACCENT, lw=1))
ax.add_patch(Rectangle((0, 0), 7, 7, fill=False, ec=INK, lw=0.7))
ax.text(117, 8, '30°', color=SERIES[1], fontsize=8, ha='center')
ax.text(64, 12, '60°', color=ACCENT, fontsize=8, ha='left')
ax.text(-5, h/2, 'h', ha='right', va='center', fontsize=9)
ax.text(-3, -9, 'C', ha='right', fontsize=8.5); ax.text(50, -9, 'B', ha='center', fontsize=8.5); ax.text(150, -9, 'A', ha='center', fontsize=8.5)
ax.text(-3, h + 3, 'T', ha='right', fontsize=8.5)
ax.text(100, -16, 'AB = 100 m', ha='center', fontsize=8)
ax.set_xlim(-18, 170); ax.set_ylim(-24, 100); ax.set_aspect('equal'); ax.axis('off')
fig.tight_layout(pad=0.3)
```

::: example Two buildings
**Problem.** From the top of a 30 m tower, the angles of depression of the **base** and the **top** of a nearby building are $60^\circ$ and $30^\circ$. Find the height of the building and its distance from the tower.

**Solution.** Let the horizontal distance be $d$. Base: $\tan60^\circ=\frac{30}{d}\Rightarrow d=\frac{30}{\sqrt{3}}=10\sqrt{3}\approx17.32$ m.

The top of the building is $d\tan30^\circ=10\sqrt{3}\times\frac{1}{\sqrt{3}}=10$ m below the top of the tower. So the building is $30-10=20$ m high.
:::

```figure caption="From the top $T$ of a 30 m tower the angles of depression of the base and top of a building are $60^\circ$ and $30^\circ$. The building is 20 m high and $10\sqrt{3}\approx17.3$ m away."
from matplotlib.patches import Arc, Rectangle
fig, ax = plt.subplots(figsize=(4.6, 2.9))
d = 10*np.sqrt(3)
ax.plot([-4, 30], [0, 0], color=INK, lw=1.0)
ax.add_patch(Rectangle((-4, 0), 4, 30, fc='#dbeafe', ec=INK, lw=1.0))
ax.add_patch(Rectangle((d, 0), 5, 20, fc='#e5e7eb', ec=INK, lw=1.0))
ax.plot([0, 24], [30, 30], color=MUTED, lw=0.9, ls='--')
ax.plot([0, d], [30, 0], color=SERIES[1], lw=1.2)
ax.plot([0, d], [30, 20], color=ACCENT, lw=1.2)
ax.add_patch(Arc((0, 30), 14, 14, theta1=-60, theta2=0, color=SERIES[1], lw=1))
ax.add_patch(Arc((0, 30), 22, 22, theta1=-30, theta2=0, color=ACCENT, lw=1))
ax.text(5.4, 23.3, '60°', color=SERIES[1], fontsize=8)
ax.text(13.5, 27.6, '30°', color=ACCENT, fontsize=8)
ax.text(-2, 15, '30 m', ha='center', va='center', fontsize=8, rotation=90)
ax.text(d + 2.5, 8, '20 m', ha='center', va='center', fontsize=8, rotation=90)
ax.text(d/2, -3.5, 'd = 10√3 m', ha='center', va='top', fontsize=8)
ax.text(-1, 32.5, 'T', ha='center', fontsize=8.5)
ax.set_xlim(-6, 27); ax.set_ylim(-8, 36); ax.set_aspect('equal'); ax.axis('off')
fig.tight_layout(pad=0.3)
```

::: example Flagstaff on a tower
**Problem.** A flagstaff stands on top of a tower. From a point 40 m from the foot of the tower the angles of elevation of the top of the tower and of the top of the flagstaff are $45^\circ$ and $60^\circ$. Find the height of the flagstaff.

**Solution.** Tower: $\tan45^\circ=\frac{h_1}{40}\Rightarrow h_1=40$ m. Tower plus flagstaff: $\tan60^\circ=\frac{h_1+x}{40}\Rightarrow h_1+x=40\sqrt{3}$.

Flagstaff $x=40\sqrt{3}-40=40(\sqrt{3}-1)=40(0.732)\approx29.3$ m.
:::

::: example A kite
**Problem.** A kite is flying at the end of a 80 m string that is taut and makes an angle of $30^\circ$ with the horizontal ground. Find the height of the kite above the ground (ignore the sag of the string).

**Solution.** The string is the hypotenuse: height $=80\sin30^\circ=80\times\frac{1}{2}=40$ m.
:::

::: example Angle of elevation changes from $30^\circ$ to $45^\circ$
**Problem.** A student walks 20 m towards the foot of a pole. The angle of elevation of the top changes from $30^\circ$ to $45^\circ$. Find the height of the pole.

**Solution.** Let the height be $h$ and the final distance from the foot $x$. $\tan45^\circ=\frac{h}{x}\Rightarrow x=h$. $\tan30^\circ=\frac{h}{x+20}\Rightarrow x+20=h\sqrt{3}$.

So $h+20=h\sqrt{3}\Rightarrow20=h(\sqrt{3}-1)\Rightarrow h=\frac{20}{\sqrt{3}-1}=\frac{20(\sqrt{3}+1)}{2}=10(\sqrt{3}+1)\approx27.3$ m.
:::

::: example An aeroplane
**Problem.** An aeroplane flying 3000 m above level ground passes directly over a point $P$. Two points $A$ and $B$ on the ground on opposite sides of $P$ are seen from the plane with angles of depression $30^\circ$ and $60^\circ$. Find the distance $AB$.

**Solution.** $PA=\frac{3000}{\tan30^\circ}=3000\sqrt{3}\approx5196$ m and $PB=\frac{3000}{\tan60^\circ}=\frac{3000}{\sqrt{3}}=1000\sqrt{3}\approx1732$ m. On opposite sides, $AB=PA+PB=3000\sqrt{3}+1000\sqrt{3}=4000\sqrt{3}\approx6928$ m.
:::

## 5.4 Exercises of the SEE type

::: example A river
**Problem.** A tree stands on one bank of a river. From a point directly opposite the tree on the other bank, the angle of elevation of the top of the tree is $60^\circ$. From a point 30 m further back, in line, it is $30^\circ$. Find the height of the tree and the width of the river.

**Solution.** Let height $=h$ and width $=w$. $\tan60^\circ=\frac{h}{w}\Rightarrow w=\frac{h}{\sqrt{3}}$. $\tan30^\circ=\frac{h}{w+30}\Rightarrow w+30=h\sqrt{3}$.

$\frac{h}{\sqrt{3}}+30=h\sqrt{3}\Rightarrow30=\frac{2h}{\sqrt{3}}\Rightarrow h=15\sqrt{3}\approx25.98$ m. Then $w=\frac{h}{\sqrt{3}}=15$ m.

The tree is about **26 m** high and the river is **15 m** wide.
:::

::: example Shadow
**Problem.** The shadow of a vertical pole on level ground is $\sqrt{3}$ times its height. Find the angle of elevation of the sun.

**Solution.** $\tan\theta=\frac{\text{height}}{\text{shadow}}=\frac{1}{\sqrt{3}}$, so $\theta=30^\circ$.
:::

::: example An identity and an equation together
**Problem.** (i) In a triangle $ABC$, prove that $\sin A+\sin B+\sin C=4\cos\frac{A}{2}\cos\frac{B}{2}\cos\frac{C}{2}$ and verify it for $A=B=C=60^\circ$. (ii) Solve $\sin\theta+\cos\theta=1$ for $0^\circ\leq\theta\leq360^\circ$.

**Solution.** (i) The proof is in 5.1. Check: LHS $=3\sin60^\circ=\frac{3\sqrt{3}}{2}$; RHS $=4\cos^330^\circ=4\left(\frac{\sqrt{3}}{2}\right)^3=\frac{3\sqrt{3}}{2}$. ✓

(ii) Square both sides: $\sin^2\theta+2\sin\theta\cos\theta+\cos^2\theta=1\Rightarrow\sin2\theta=0\Rightarrow\theta=0^\circ,\ 90^\circ,\ 180^\circ,\ 270^\circ,\ 360^\circ$. Squaring can add false roots, so test each in the original equation: $\theta=0^\circ$: $0+1=1$ ✓; $90^\circ$: $1+0=1$ ✓; $180^\circ$: $0-1=-1$ ✗; $270^\circ$: $-1+0=-1$ ✗; $360^\circ$: $0+1=1$ ✓.

Solutions: $\theta=0^\circ,\ 90^\circ,\ 360^\circ$.
:::

## Chapter summary

- **Triangle conditions** ($A+B+C=180^\circ$): $\sin(A+B)=\sin C$, $\cos(A+B)=-\cos C$, $\tan(A+B)=-\tan C$, $\sin\frac{A+B}{2}=\cos\frac{C}{2}$.
- **Identities:** $\sin2A+\sin2B+\sin2C=4\sin A\sin B\sin C$; $\tan A+\tan B+\tan C=\tan A\tan B\tan C$; $\sin A+\sin B+\sin C=4\cos\frac{A}{2}\cos\frac{B}{2}\cos\frac{C}{2}$; $\cos A+\cos B+\cos C=1+4\sin\frac{A}{2}\sin\frac{B}{2}\sin\frac{C}{2}$; $\cos2A+\cos2B+\cos2C=-1-4\cos A\cos B\cos C$.
- If $A+B+C=90^\circ$: $\tan A\tan B+\tan B\tan C+\tan C\tan A=1$.
- **Equations:** find the principal value $\alpha$, then use quadrants: $\sin\theta=k$: $\alpha,\ 180^\circ-\alpha$; $\cos\theta=k$: $\alpha,\ 360^\circ-\alpha$; $\tan\theta=k$: $\alpha,\ 180^\circ+\alpha$ (for positive $k$). Factorise, never divide by a ratio, and respect the range.
- **Height and distance:** $\tan\theta=\frac{h}{d}$; angle of depression from a point equals the angle of elevation of that point from below (alternate angles). Draw the figure first.
- Two-position problems: write two equations with the same height $h$ and solve; $\tan30^\circ=\frac{1}{\sqrt{3}}$, $\tan60^\circ=\sqrt{3}$.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. If $A+B+C=180^\circ$, then $\cos(A+B)$ equals <span class="marks">[1]</span>
   (a) $\cos C$ (b) $-\cos C$ (c) $\sin C$ (d) $-\sin C$
2. If $A+B+C=180^\circ$, then $\tan A+\tan B+\tan C$ equals <span class="marks">[1]</span>
   (a) $\tan A\tan B\tan C$ (b) 0 (c) 1 (d) $\tan A\tan B+\tan B\tan C$
3. The solutions of $2\sin\theta-1=0$ for $0^\circ\leq\theta\leq360^\circ$ are <span class="marks">[1]</span>
   (a) $30^\circ,\ 330^\circ$ (b) $30^\circ,\ 150^\circ$ (c) $60^\circ,\ 120^\circ$ (d) $30^\circ,\ 210^\circ$
4. If $\tan\theta=\frac{1}{\sqrt{3}}$ and $0^\circ\leq\theta\leq90^\circ$, then $\theta$ is <span class="marks">[1]</span>
   (a) $30^\circ$ (b) $45^\circ$ (c) $60^\circ$ (d) $90^\circ$
5. The angle of elevation of the top of a tower from a point 20 m from its foot is $45^\circ$. The height is <span class="marks">[1]</span>
   (a) 10 m (b) 20 m (c) $20\sqrt{3}$ m (d) $\frac{20}{\sqrt{3}}$ m
6. The angle of depression of an object from an observer equals <span class="marks">[1]</span>
   (a) the angle of elevation of the observer from the object (b) $90^\circ$ minus that angle (c) twice that angle (d) none of these

::: note Answers to Group A
**1.** (b) — $A+B=180^\circ-C$.
**2.** (a) — the conditional identity.
**3.** (b) — $\sin\theta=\frac{1}{2}$ in quadrants 1 and 2.
**4.** (a) — $\tan30^\circ=\frac{1}{\sqrt{3}}$.
**5.** (b) — $\tan45^\circ=1$, so $h=20$ m.
**6.** (a) — alternate angles are equal.
:::

**Group B — Short answer (2 marks each)**

1. If $A+B+C=180^\circ$, show that $\sin(A+B)=\sin C$ and $\cos(A+B)=-\cos C$. <span class="marks">[2]</span>
2. Solve $2\cos\theta+1=0$ for $0^\circ\leq\theta\leq360^\circ$. <span class="marks">[2]</span>
3. Solve $\sqrt{3}\tan\theta=1$ for $0^\circ\leq\theta\leq360^\circ$. <span class="marks">[2]</span>
4. A 10 m ladder makes an angle of $60^\circ$ with the ground. How high does it reach? <span class="marks">[2]</span>
5. From the top of a 60 m cliff, the angle of depression of a boat is $30^\circ$. Find its distance from the foot of the cliff. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** $A+B=180^\circ-C$; $\sin(180^\circ-C)=\sin C$ and $\cos(180^\circ-C)=-\cos C$.
**2.** $\cos\theta=-\frac{1}{2}$: $\theta=120^\circ$ or $240^\circ$.
**3.** $\tan\theta=\frac{1}{\sqrt{3}}$: $\theta=30^\circ$ or $210^\circ$.
**4.** $10\sin60^\circ=5\sqrt{3}\approx8.66$ m.
**5.** $d=\frac{60}{\tan30^\circ}=60\sqrt{3}\approx103.9$ m.
:::

**Group C — Short answer (3 marks each)**

1. If $A+B+C=180^\circ$, prove that $\tan A+\tan B+\tan C=\tan A\tan B\tan C$. <span class="marks">[3]</span>
2. Solve $2\sin^2\theta-\sin\theta-1=0$ for $0^\circ\leq\theta\leq360^\circ$. <span class="marks">[3]</span>
3. Solve $\cos2\theta=\sin\theta$ for $0^\circ\leq\theta\leq360^\circ$. <span class="marks">[3]</span>
4. From a point 50 m from the foot of a tower, the angle of elevation of its top is $60^\circ$. Find the height of the tower. <span class="marks">[3]</span>
5. From a point 40 m from the foot of a tower, the angles of elevation of the tower top and of the top of a flagstaff on it are $45^\circ$ and $60^\circ$. Find the height of the flagstaff. <span class="marks">[3]</span>

::: note Answers to Group C
**1.** $\tan(A+B)=-\tan C\Rightarrow\frac{\tan A+\tan B}{1-\tan A\tan B}=-\tan C\Rightarrow\tan A+\tan B=-\tan C+\tan A\tan B\tan C$, so the sum equals the product.
**2.** $(2\sin\theta+1)(\sin\theta-1)=0$: $\sin\theta=1\Rightarrow90^\circ$; $\sin\theta=-\frac{1}{2}\Rightarrow210^\circ,\ 330^\circ$. Solutions $90^\circ,\ 210^\circ,\ 330^\circ$.
**3.** $1-2\sin^2\theta=\sin\theta\Rightarrow(2\sin\theta-1)(\sin\theta+1)=0$: $30^\circ,\ 150^\circ,\ 270^\circ$.
**4.** $h=50\tan60^\circ=50\sqrt{3}\approx86.6$ m.
**5.** Tower $=40\tan45^\circ=40$ m; tower plus staff $=40\tan60^\circ=40\sqrt{3}$ m. Flagstaff $=40(\sqrt{3}-1)\approx29.3$ m.
:::

**Group D — Long answer (4 marks each)**

1. If $A+B+C=180^\circ$, prove that $\sin2A+\sin2B+\sin2C=4\sin A\sin B\sin C$. <span class="marks">[4]</span>
2. If $A+B+C=180^\circ$, prove that $\sin A+\sin B+\sin C=4\cos\frac{A}{2}\cos\frac{B}{2}\cos\frac{C}{2}$. <span class="marks">[4]</span>
3. The angle of elevation of the top of a tower from a point $A$ is $30^\circ$. On moving 100 m towards the tower it becomes $60^\circ$. Find the height of the tower. <span class="marks">[4]</span>
4. From the top of a 30 m tower, the angles of depression of the base and the top of a building are $60^\circ$ and $30^\circ$. Find the height of the building. <span class="marks">[4]</span>
5. Solve $2\cos^2\theta+3\sin\theta=3$ for $0^\circ\leq\theta\leq360^\circ$. <span class="marks">[4]</span>

::: note Answers to Group D
**1.** $\sin2A+\sin2B=2\sin(A+B)\cos(A-B)=2\sin C\cos(A-B)$. $\sin2C=2\sin C\cos C$. LHS $=2\sin C[\cos(A-B)+\cos C]=2\sin C[\cos(A-B)-\cos(A+B)]=2\sin C\cdot2\sin A\sin B=4\sin A\sin B\sin C$.
**2.** $\sin A+\sin B=2\cos\frac{C}{2}\cos\frac{A-B}{2}$; $\sin C=2\sin\frac{C}{2}\cos\frac{C}{2}$. LHS $=2\cos\frac{C}{2}[\cos\frac{A-B}{2}+\cos\frac{A+B}{2}]=2\cos\frac{C}{2}\cdot2\cos\frac{A}{2}\cos\frac{B}{2}=4\cos\frac{A}{2}\cos\frac{B}{2}\cos\frac{C}{2}$.
**3.** Let $BC=x$, height $h$. $x=\frac{h}{\sqrt{3}}$ and $x+100=h\sqrt{3}$. So $\frac{2h}{\sqrt{3}}=100$, $h=50\sqrt{3}\approx86.6$ m.
**4.** Distance $d=\frac{30}{\tan60^\circ}=10\sqrt{3}$. Drop to the building top $=d\tan30^\circ=10$ m. Height of building $=30-10=20$ m.
**5.** $2-2\sin^2\theta+3\sin\theta=3\Rightarrow(2\sin\theta-1)(\sin\theta-1)=0$. $\sin\theta=\frac{1}{2}$: $30^\circ,\ 150^\circ$; $\sin\theta=1$: $90^\circ$. Solutions $30^\circ,\ 90^\circ,\ 150^\circ$.
:::
