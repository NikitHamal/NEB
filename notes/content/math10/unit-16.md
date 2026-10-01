---
subject: Mathematics
grade: 10
unit: 16
title: Trigonometry
hours: 0
area: Compulsory Mathematics
---

How tall is a tower you cannot climb? How wide is a river you cannot cross? Surveyors, pilots, architects and mountaineers answer these questions without measuring the distance directly: they measure an **angle** and one length, and use **trigonometry** — the study of the relationship between the sides and the angles of a right-angled triangle. This chapter defines the three basic ratios **sine, cosine and tangent**, finds their exact values for $30^\circ$, $45^\circ$ and $60^\circ$, shows how the ratios of complementary angles are linked, proves the key identities, and then applies everything to **heights and distances**.

::: key What the SEE asks from this chapter
Expect: (i) find all trigonometric ratios from one given ratio (e.g. $\sin\theta=\frac{5}{13}$); (ii) evaluate expressions with the standard values of $30^\circ,45^\circ,60^\circ$; (iii) **prove an identity** such as $(\sec\theta-\tan\theta)(\sec\theta+\tan\theta)=1$; (iv) use complementary angles ($\sin 25^\circ=\cos65^\circ$); (v) a word problem on a tower, ladder or cliff using the angle of **elevation** or **depression**. Draw a clear figure, mark the right angle and the angle, and write the ratio you use.
:::

## 16.1 Trigonometry: concepts, formulas and worked problems

### The right-angled triangle and its sides

In a right-angled triangle, the side opposite the right angle is the **hypotenuse** (the longest side). For an acute angle $\theta$, the side facing $\theta$ is the **opposite** (perpendicular, $p$) and the side touching $\theta$ (other than the hypotenuse) is the **adjacent** (base, $b$). The names of the two shorter sides change if you move to the other acute angle, but the hypotenuse never changes.

```figure caption="The sides of a right-angled triangle relative to the angle θ: hypotenuse h, opposite p and adjacent b."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Arc, Rectangle
fig, ax = plt.subplots(figsize=(4.4, 2.6))
A = np.array([0, 0.]); B = np.array([4, 0.]); C = np.array([4, 2.6])
ax.add_patch(Polygon([A, B, C], fc='#dbeafe', ec=INK, lw=1.3))
ax.add_patch(Rectangle((3.75, 0), 0.25, 0.25, fc='none', ec=INK, lw=0.9))
ax.add_patch(Arc(A, 1.6, 1.6, theta1=0, theta2=33, color='#dc2626', lw=1.1))
ax.text(1.0, 0.18, 'θ', fontsize=10, color='#dc2626')
ax.text(2.0, -0.4, 'adjacent  b', fontsize=9, ha='center')
ax.text(4.12, 1.3, 'opposite  p', fontsize=9, va='center')
ax.text(1.6, 1.45, 'hypotenuse  h', fontsize=9, rotation=33, ha='center')
ax.set_xlim(-0.4, 5.6); ax.set_ylim(-0.8, 3.1); ax.set_aspect('equal'); ax.axis('off')
fig.tight_layout(pad=0.3)
```

::: key The three ratios
$$ \sin\theta=\frac{\text{opposite}}{\text{hypotenuse}}=\frac{p}{h} \qquad \cos\theta=\frac{\text{adjacent}}{\text{hypotenuse}}=\frac{b}{h} \qquad \tan\theta=\frac{\text{opposite}}{\text{adjacent}}=\frac{p}{b} $$

Their reciprocals are
$$ \csc\theta=\frac{h}{p} \qquad \sec\theta=\frac{h}{b} \qquad \cot\theta=\frac{b}{p} $$

A memory aid: **SOH – CAH – TOA** (Sine = Opposite/Hypotenuse, Cosine = Adjacent/Hypotenuse, Tangent = Opposite/Adjacent). Also $\tan\theta=\frac{\sin\theta}{\cos\theta}$.
:::

Because similar triangles have the same shape, the ratio depends only on the angle, not on the size of the triangle. The values of $\sin\theta$ and $\cos\theta$ are never greater than 1 for an acute angle; $\tan\theta$ can be any positive number.

::: example Ratios from a 3-4-5 triangle
**Problem.** A right-angled triangle has sides 3 cm, 4 cm and 5 cm. Find the three ratios for the angle $\theta$ opposite the side 3 cm.

**Solution.** Opposite $=3$, adjacent $=4$, hypotenuse $=5$.

$$ \sin\theta=\frac{3}{5},\qquad \cos\theta=\frac{4}{5},\qquad \tan\theta=\frac{3}{4} $$

Check: $\sin^2\theta+\cos^2\theta=\frac{9}{25}+\frac{16}{25}=1$ ✓.
:::

::: example All ratios from one ratio
**Problem.** If $\sin\theta=\frac{5}{13}$, find $\cos\theta$, $\tan\theta$ and $\sec\theta$.

**Solution.** Draw a right triangle with opposite $=5$ and hypotenuse $=13$. By Pythagoras the adjacent side is $\sqrt{13^2-5^2}=\sqrt{144}=12$. Then

$$ \cos\theta=\frac{12}{13},\qquad \tan\theta=\frac{5}{12},\qquad \sec\theta=\frac{13}{12} $$
:::

::: example From the tangent
**Problem.** If $\tan\theta=\frac{3}{4}$, find $\sin\theta$ and $\cos\theta$.

**Solution.** Opposite $=3$, adjacent $=4$, so the hypotenuse is $\sqrt{9+16}=5$. $\sin\theta=\frac{3}{5}$ and $\cos\theta=\frac{4}{5}$. (This is the 3-4-5 triangle: $\theta\approx36.9^\circ$.)
:::

### Ratios of $30^\circ$, $45^\circ$ and $60^\circ$

::: derivation Exact values for 45°, 30° and 60°
We read the ratios off two special triangles.

**Step 1 — the isosceles right triangle.** Take a right-angled triangle with the two equal sides 1, so the angles are $45^\circ,45^\circ,90^\circ$. By Pythagoras the hypotenuse is $\sqrt{1^2+1^2}=\sqrt{2}$. For $45^\circ$:

$$ \sin45^\circ=\frac{1}{\sqrt{2}}\qquad \cos45^\circ=\frac{1}{\sqrt{2}}\qquad \tan45^\circ=1 $$

**Step 2 — the half-equilateral triangle.** Take an equilateral triangle of side 2 and draw an altitude. It bisects the base and the apex angle, giving a right-angled triangle with angles $30^\circ,60^\circ,90^\circ$, hypotenuse 2, short side 1 and altitude $\sqrt{2^2-1^2}=\sqrt{3}$.

**Step 3 — read the ratios.** The side opposite $30^\circ$ is 1, the side opposite $60^\circ$ is $\sqrt{3}$:

$$ \sin30^\circ=\frac{1}{2}\quad\cos30^\circ=\frac{\sqrt{3}}{2}\quad\tan30^\circ=\frac{1}{\sqrt{3}} $$

$$ \sin60^\circ=\frac{\sqrt{3}}{2}\quad\cos60^\circ=\frac{1}{2}\quad\tan60^\circ=\sqrt{3} $$

**What it means.** These nine values are exact and must be memorised.
:::

```figure caption="The two special triangles that give the exact ratios: the 45°–45°–90° triangle with sides 1, 1, √2 and the 30°–60°–90° triangle with sides 1, √3, 2."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(5.0, 2.6))
ax1.add_patch(Polygon([(0, 0), (2, 0), (2, 2)], fc='#dbeafe', ec=INK, lw=1.2))
ax1.text(1.0, -0.3, '1', ha='center', fontsize=9); ax1.text(2.15, 1.0, '1', fontsize=9, va='center')
ax1.text(0.8, 1.15, '√2', fontsize=9, rotation=45, ha='center')
ax1.text(0.35, 0.1, '45°', fontsize=8, color='#dc2626'); ax1.text(1.35, 1.55, '45°', fontsize=8, color='#dc2626')
ax1.set_xlim(-0.4, 2.7); ax1.set_ylim(-0.7, 2.4); ax1.set_aspect('equal'); ax1.axis('off')
s3 = np.sqrt(3)
ax2.add_patch(Polygon([(0, 0), (1, 0), (1, s3)], fc='#dcfce7', ec=INK, lw=1.2))
ax2.text(0.5, -0.3, '1', ha='center', fontsize=9); ax2.text(1.12, s3 / 2, '√3', fontsize=9, va='center')
ax2.text(0.28, 1.0, '2', fontsize=9, rotation=60, ha='center')
ax2.text(0.3, 0.1, '60°', fontsize=8, color='#dc2626'); ax2.text(0.55, 1.3, '30°', fontsize=8, color='#dc2626')
ax2.set_xlim(-0.5, 1.8); ax2.set_ylim(-0.7, 2.2); ax2.set_aspect('equal'); ax2.axis('off')
fig.tight_layout(pad=0.3)
```

::: key Table of standard values
| $\theta$ | $30^\circ$ | $45^\circ$ | $60^\circ$ |
|---|---|---|---|
| $\sin\theta$ | $\frac{1}{2}$ | $\frac{1}{\sqrt{2}}$ | $\frac{\sqrt{3}}{2}$ |
| $\cos\theta$ | $\frac{\sqrt{3}}{2}$ | $\frac{1}{\sqrt{2}}$ | $\frac{1}{2}$ |
| $\tan\theta$ | $\frac{1}{\sqrt{3}}$ | $1$ | $\sqrt{3}$ |

Memory trick: the sines are $\frac{\sqrt{1}}{2},\frac{\sqrt{2}}{2},\frac{\sqrt{3}}{2}$ for $30^\circ,45^\circ,60^\circ$; the cosines are the sines in reverse.
:::

::: example Evaluate
**Problem.** Find the value of $\sin30^\circ\cos60^\circ+\cos30^\circ\sin60^\circ$.

**Solution.** $\frac{1}{2}\times\frac{1}{2}+\frac{\sqrt{3}}{2}\times\frac{\sqrt{3}}{2}=\frac{1}{4}+\frac{3}{4}=1$.
:::

::: example Evaluate with squares
**Problem.** Find $4\sin^260^\circ-3\tan^230^\circ$.

**Solution.** $\sin^260^\circ=\left(\frac{\sqrt{3}}{2}\right)^2=\frac{3}{4}$ and $\tan^230^\circ=\left(\frac{1}{\sqrt{3}}\right)^2=\frac{1}{3}$. So $4\times\frac{3}{4}-3\times\frac{1}{3}=3-1=2$.
:::

::: example Evaluate: a mixed expression
**Problem.** Simplify $\frac{\tan60^\circ-\tan30^\circ}{1+\tan60^\circ\tan30^\circ}$.

**Solution.** $\tan60^\circ\tan30^\circ=\sqrt{3}\times\frac{1}{\sqrt{3}}=1$, so the denominator is $2$. The numerator is $\sqrt{3}-\frac{1}{\sqrt{3}}=\frac{3-1}{\sqrt{3}}=\frac{2}{\sqrt{3}}$. The result is $\frac{2/\sqrt{3}}{2}=\frac{1}{\sqrt{3}}=\tan30^\circ$.
:::

::: example Finding the angle
**Problem.** Find the acute angle $\theta$ if (a) $2\sin\theta=1$, (b) $\tan\theta=\sqrt{3}$, (c) $2\cos^2\theta-1=0$.

**Solution.** (a) $\sin\theta=\frac{1}{2}$, so $\theta=30^\circ$. (b) $\theta=60^\circ$. (c) $\cos^2\theta=\frac{1}{2}$, $\cos\theta=\frac{1}{\sqrt{2}}$, so $\theta=45^\circ$.
:::

### Complementary angles

Two angles are **complementary** if they add up to $90^\circ$. In a right-angled triangle the two acute angles $\theta$ and $90^\circ-\theta$ are complementary, and the side opposite one is the side adjacent to the other. So:

::: key Complementary-angle relations
$$ \sin(90^\circ-\theta)=\cos\theta \qquad \cos(90^\circ-\theta)=\sin\theta \qquad \tan(90^\circ-\theta)=\cot\theta $$

For example $\sin25^\circ=\cos65^\circ$ and $\tan15^\circ\times\tan75^\circ=\tan15^\circ\times\cot15^\circ=1$.
:::

::: example Complementary angles
**Problem.** Evaluate (a) $\frac{\sin25^\circ}{\cos65^\circ}$, (b) $\tan15^\circ\tan75^\circ$, (c) $\cos20^\circ-\sin70^\circ$.

**Solution.** (a) $\cos65^\circ=\sin25^\circ$, so the ratio is $1$. (b) $\tan75^\circ=\cot15^\circ$, so the product is $1$. (c) $\sin70^\circ=\cos20^\circ$, so the difference is $0$.
:::

### Identities

::: derivation The Pythagorean identities
**Setting up.** Take a right-angled triangle with opposite $p$, adjacent $b$ and hypotenuse $h$ for the angle $\theta$.

**Step 1 — Pythagoras.** $p^2+b^2=h^2$.

**Step 2 — divide by $h^2$.**

$$ \left(\frac{p}{h}\right)^2+\left(\frac{b}{h}\right)^2=1 \;\Rightarrow\; \sin^2\theta+\cos^2\theta=1 $$

**Step 3 — divide Step 1 by $b^2$.**

$$ \left(\frac{p}{b}\right)^2+1=\left(\frac{h}{b}\right)^2 \;\Rightarrow\; 1+\tan^2\theta=\sec^2\theta $$

**Step 4 — divide Step 1 by $p^2$.**

$$ 1+\left(\frac{b}{p}\right)^2=\left(\frac{h}{p}\right)^2 \;\Rightarrow\; 1+\cot^2\theta=\csc^2\theta $$

**What it means.** These hold for every angle, so we can replace $\sin^2\theta+\cos^2\theta$ by 1, and so on, in any proof.
:::

::: key Identities to learn
$$ \sin^2\theta+\cos^2\theta=1 \qquad 1+\tan^2\theta=\sec^2\theta \qquad 1+\cot^2\theta=\csc^2\theta $$
$$ \tan\theta=\frac{\sin\theta}{\cos\theta}\qquad \cot\theta=\frac{\cos\theta}{\sin\theta} \qquad \sin\theta\csc\theta=\cos\theta\sec\theta=\tan\theta\cot\theta=1 $$
:::

::: example Prove an identity
**Problem.** Prove that $(1-\sin^2\theta)\sec^2\theta=1$.

**Solution.** $1-\sin^2\theta=\cos^2\theta$. So LHS $=\cos^2\theta\times\frac{1}{\cos^2\theta}=1=$ RHS. Proved.
:::

::: example Prove with two brackets
**Problem.** Prove that $(\sec\theta-\tan\theta)(\sec\theta+\tan\theta)=1$.

**Solution.** Use $(a-b)(a+b)=a^2-b^2$: LHS $=\sec^2\theta-\tan^2\theta=1$ (from $1+\tan^2\theta=\sec^2\theta$) $=$ RHS. Proved.
:::

::: example Prove with fractions
**Problem.** Prove that $\frac{\sin\theta}{1+\cos\theta}+\frac{1+\cos\theta}{\sin\theta}=2\csc\theta$.

**Solution.** Combine over the common denominator $\sin\theta(1+\cos\theta)$:

$$ \text{LHS}=\frac{\sin^2\theta+(1+\cos\theta)^2}{\sin\theta(1+\cos\theta)} $$

Expand the numerator: $\sin^2\theta+1+2\cos\theta+\cos^2\theta=2+2\cos\theta=2(1+\cos\theta)$. So

$$ \text{LHS}=\frac{2(1+\cos\theta)}{\sin\theta(1+\cos\theta)}=\frac{2}{\sin\theta}=2\csc\theta=\text{RHS} $$

Proved.
:::

::: example Prove with a difference of fourth powers
**Problem.** Prove that $\sin^4\theta-\cos^4\theta=\sin^2\theta-\cos^2\theta$.

**Solution.** LHS $=(\sin^2\theta-\cos^2\theta)(\sin^2\theta+\cos^2\theta)=(\sin^2\theta-\cos^2\theta)\times1=$ RHS. Proved.
:::

::: example Prove with two fractions
**Problem.** Prove that $\frac{1}{1+\sin\theta}+\frac{1}{1-\sin\theta}=2\sec^2\theta$.

**Solution.** LHS $=\frac{(1-\sin\theta)+(1+\sin\theta)}{(1+\sin\theta)(1-\sin\theta)}=\frac{2}{1-\sin^2\theta}=\frac{2}{\cos^2\theta}=2\sec^2\theta$. Proved.
:::

::: example Evaluate using an identity
**Problem.** If $\sin\theta+\cos\theta=\sqrt{2}$, find $\sin\theta\cos\theta$.

**Solution.** Square both sides: $\sin^2\theta+2\sin\theta\cos\theta+\cos^2\theta=2$, so $1+2\sin\theta\cos\theta=2$ and $\sin\theta\cos\theta=\frac{1}{2}$.
:::

::: caution Common mistakes
- $\sin^2\theta$ means $(\sin\theta)^2$, not $\sin(\theta^2)$.
- $\sin(A+B)\ne\sin A+\sin B$. For instance $\sin30^\circ+\sin60^\circ\ne\sin90^\circ$.
- Mixing up opposite and adjacent: they depend on **which angle** you are using.
- Calculator in the wrong mode — keep it in **degrees**.
- In an identity proof, do not move terms across the "=" sign; simplify one side until it equals the other.
:::

```figure caption="Graphs of sin θ, cos θ and tan θ for 0° ≤ θ ≤ 80°: sine rises from 0, cosine falls from 1 and they cross at 45°; tangent keeps rising."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6, 3.0))
x = np.linspace(0, 80, 200)
r = np.radians(x)
ax.plot(x, np.sin(r), color=ACCENT, lw=1.7, label='sin θ')
ax.plot(x, np.cos(r), color='#dc2626', lw=1.7, label='cos θ')
ax.plot(x, np.tan(r), color='#16a34a', lw=1.7, label='tan θ')
ax.plot([45], [np.sin(np.radians(45))], 'o', color=INK, ms=3.5)
ax.text(46, 0.55, '45°: 0.707', fontsize=8)
ax.set_xlim(0, 80); ax.set_ylim(0, 2.2)
ax.set_xlabel('θ (degrees)', fontsize=8.5)
ax.tick_params(labelsize=8); ax.grid(color=GRID, lw=0.5)
ax.legend(fontsize=8, frameon=False, loc='upper left')
fig.tight_layout(pad=0.4)
```

### Heights and distances

When you look **up** at an object, the angle between your horizontal line of sight and the line to the object is the **angle of elevation**. When you look **down**, it is the **angle of depression**. The angle of depression of an object from a point equals the angle of elevation of that point from the object (alternate angles).

```figure caption="A tower of height h seen from a point 30 m away at an angle of elevation 60°: tan 60° = h / 30, so h = 30√3 ≈ 51.96 m."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Arc, Rectangle
fig, ax = plt.subplots(figsize=(4.6, 3.0))
h = 30 * np.sqrt(3)
ax.plot([-5, 40], [0, 0], color=INK, lw=1.2)
ax.add_patch(Rectangle((30, 0), 3, h, fc='#e2e8f0', ec=INK, lw=1.1))
ax.plot([0, 30], [0, h], color=ACCENT, lw=1.2)
ax.plot([0, 30], [0, 0], color=INK, lw=0.8)
ax.add_patch(Arc((0, 0), 18, 18, theta1=0, theta2=60, color='#dc2626', lw=1.1))
ax.text(11, 3.2, '60°', fontsize=9, color='#dc2626')
ax.text(15, -6, '30 m', fontsize=9, ha='center')
ax.text(34, h / 2, 'h', fontsize=10, va='center')
ax.text(-1, 4, 'P', fontsize=9)
ax.set_xlim(-6, 42); ax.set_ylim(-10, 62); ax.set_aspect('equal'); ax.axis('off')
fig.tight_layout(pad=0.3)
```

::: key How to solve height-and-distance problems
1. Draw a figure: a vertical line (tower), a horizontal ground line, and the line of sight; mark the right angle and the angle of elevation or depression.
2. Decide which two sides are involved: opposite and adjacent → **tan**; opposite and hypotenuse → **sin**; adjacent and hypotenuse → **cos**.
3. Write the equation, solve for the unknown, and state the answer with units.
4. Use $\sqrt{3}\approx1.732$ and $\sqrt{2}\approx1.414$ unless told otherwise.
:::

::: example Height of a tower
**Problem.** The angle of elevation of the top of a tower from a point 30 m from its foot on level ground is $60^\circ$. Find the height of the tower.

**Solution.** $\tan60^\circ=\frac{h}{30}$, so $h=30\sqrt{3}=30\times1.732=51.96$ m.
:::

::: example Ladder against a wall
**Problem.** A 10 m ladder makes an angle of $60^\circ$ with the ground. How high up the wall does it reach, and how far is its foot from the wall?

**Solution.** Height $=10\sin60^\circ=10\times\frac{\sqrt{3}}{2}=5\sqrt{3}=8.66$ m. Distance from wall $=10\cos60^\circ=5$ m. Check: $5^2+(5\sqrt{3})^2=25+75=100$ ✓.
:::

::: example Shadow
**Problem.** A pole 6 m high casts a shadow on level ground when the Sun's elevation is $45^\circ$. Find the length of the shadow.

**Solution.** $\tan45^\circ=\frac{6}{\text{shadow}}$ and $\tan45^\circ=1$, so the shadow is 6 m long.
:::

::: example Tower at a given distance
**Problem.** The angle of elevation of the top of a tower from a point 50 m from its foot is $30^\circ$. Find the height of the tower.

**Solution.** $\tan30^\circ=\frac{h}{50}$, $h=\frac{50}{\sqrt{3}}=28.87$ m.
:::

::: example Angle of depression
**Problem.** From the top of a cliff 40 m high, the angle of depression of a boat on the sea is $30^\circ$. Find the distance of the boat from the foot of the cliff.

**Solution.** The angle of elevation of the top from the boat is also $30^\circ$. $\tan30^\circ=\frac{40}{d}$, so $d=\frac{40}{\tan30^\circ}=40\sqrt{3}=69.28$ m.
:::

::: example A kite string
**Problem.** A kite is flying at the end of a 100 m string, which makes an angle of $60^\circ$ with the ground. Find the height of the kite (assume the string is straight).

**Solution.** Height $=100\sin60^\circ=50\sqrt{3}=86.6$ m.
:::

```figure caption="Two observation points: from P the top of the tower is at elevation 30°; after walking 20 m towards the tower to Q the elevation is 45°."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Arc, Rectangle
fig, ax = plt.subplots(figsize=(4.8, 2.8))
h = 20 / (np.sqrt(3) - 1)
xq = h
xp = h * np.sqrt(3)
ax.plot([-5, xp + 22], [0, 0], color=INK, lw=1.2)
ax.add_patch(Rectangle((xp + xq - xq - 0, 0), 0, 0))
# tower at x = 0 (place P on the right)
X = lambda d: xp - d
ax.add_patch(Rectangle((-1.5, 0), 3, h, fc='#e2e8f0', ec=INK, lw=1.1))
ax.plot([xp, 0], [0, h], color=ACCENT, lw=1.1)
ax.plot([xq, 0], [0, h], color='#dc2626', lw=1.1)
ax.add_patch(Arc((xp, 0), 22, 22, theta1=180 - 30, theta2=180, color=ACCENT, lw=1.0))
ax.add_patch(Arc((xq, 0), 16, 16, theta1=180 - 45, theta2=180, color='#dc2626', lw=1.0))
ax.text(xp - 14, 2.3, '30°', fontsize=8.5, color=ACCENT)
ax.text(xq - 9.5, 2.2, '45°', fontsize=8.5, color='#dc2626')
ax.annotate('', xy=(xq, -4), xytext=(xp, -4), arrowprops=dict(arrowstyle='<->', color=INK, lw=0.9))
ax.text(xp + 1, 1, 'P', fontsize=9); ax.text(xq + 1, 1, 'Q', fontsize=9)
ax.text((xp + xq) / 2, -9, '20 m', fontsize=8.5, ha='center')
ax.text(-5, h / 2, 'h', fontsize=10)
ax.set_xlim(-8, xp + 8); ax.set_ylim(-13, h + 6); ax.set_aspect('equal'); ax.axis('off')
fig.tight_layout(pad=0.3)
```

::: example Two angles of elevation
**Problem.** From a point $P$ on level ground the angle of elevation of the top of a tower is $30^\circ$. After walking 20 m towards the tower to $Q$ the angle of elevation is $45^\circ$. Find the height of the tower.

**Solution.** Let the height be $h$ and let the distance from $Q$ to the foot be $x$. From $Q$: $\tan45^\circ=\frac{h}{x}$, so $x=h$. From $P$ (distance $x+20$): $\tan30^\circ=\frac{h}{x+20}$, so

$$ \frac{1}{\sqrt{3}}=\frac{h}{h+20} \;\Rightarrow\; h+20=\sqrt{3}\,h \;\Rightarrow\; h=\frac{20}{\sqrt{3}-1}=\frac{20(\sqrt{3}+1)}{2}=10(\sqrt{3}+1) $$

So $h=10\times2.732=27.32$ m.

**Check.** From $P$ the distance is $47.32$ m and $\tan30^\circ\times47.32=27.32$ ✓.
:::

::: example Solving a right triangle
**Problem.** In right-angled $\Delta ABC$, $\angle B=90^\circ$, $\angle A=30^\circ$ and $AC=8$ cm. Find $BC$ and $AB$.

**Solution.** $BC=AC\sin30^\circ=8\times\frac{1}{2}=4$ cm and $AB=AC\cos30^\circ=8\times\frac{\sqrt{3}}{2}=4\sqrt{3}=6.93$ cm.
:::

## 16.2 Exercises of the SEE type

### Method for any question

1. For a "find the ratios" question, draw the triangle, find the third side by Pythagoras, then read each ratio.
2. For an "evaluate" question, replace each ratio by its exact value and simplify step by step.
3. For an identity, start with the more complicated side; use $\sin^2\theta+\cos^2\theta=1$, change everything to $\sin$ and $\cos$, combine fractions.
4. For heights and distances, draw a labelled figure first.
5. Write a final sentence with units; keep $\sqrt{3}$ exact until the last line.

::: example SEE type: ratios
**Problem.** If $\cos\theta=\frac{8}{17}$, find $\sin\theta$ and $\tan\theta$.

**Solution.** Adjacent $=8$, hypotenuse $=17$; opposite $=\sqrt{17^2-8^2}=\sqrt{225}=15$. Hence $\sin\theta=\frac{15}{17}$ and $\tan\theta=\frac{15}{8}$.
:::

::: example SEE type: evaluate
**Problem.** Find the value of $\frac{\sin^245^\circ+\cos^245^\circ+\tan 45^\circ}{\sin60^\circ\cos30^\circ-\cos60^\circ\sin30^\circ}$.

**Solution.** Numerator: $\frac{1}{2}+\frac{1}{2}+1=2$. Denominator: $\frac{\sqrt{3}}{2}\cdot\frac{\sqrt{3}}{2}-\frac{1}{2}\cdot\frac{1}{2}=\frac{3}{4}-\frac{1}{4}=\frac{1}{2}$. The value is $2\div\frac{1}{2}=4$.
:::

::: example SEE type: prove
**Problem.** Prove that $\frac{\cos\theta}{1-\sin\theta}=\frac{1+\sin\theta}{\cos\theta}$.

**Solution.** Multiply the numerator and the denominator of the LHS by $(1+\sin\theta)$:

$$ \text{LHS}=\frac{\cos\theta(1+\sin\theta)}{(1-\sin\theta)(1+\sin\theta)}=\frac{\cos\theta(1+\sin\theta)}{1-\sin^2\theta}=\frac{\cos\theta(1+\sin\theta)}{\cos^2\theta}=\frac{1+\sin\theta}{\cos\theta} $$

Proved.
:::

::: example SEE type: tower and flagstaff
**Problem.** From a point on the ground 20 m from the foot of a building, the angles of elevation of the bottom and the top of a flagstaff on the roof are $30^\circ$ and $45^\circ$. Find the height of the building and the length of the flagstaff.

**Solution.** Building: $20\tan30^\circ=\frac{20}{\sqrt{3}}=11.55$ m. Building plus flagstaff: $20\tan45^\circ=20$ m. Flagstaff $=20-11.55=8.45$ m.
:::

## Chapter summary

- $\sin\theta=\frac{p}{h}$, $\cos\theta=\frac{b}{h}$, $\tan\theta=\frac{p}{b}=\frac{\sin\theta}{\cos\theta}$; reciprocals $\csc,\sec,\cot$. Memory aid SOH-CAH-TOA.
- Standard values for $30^\circ,45^\circ,60^\circ$ come from the triangles with sides $1,1,\sqrt{2}$ and $1,\sqrt{3},2$.
- Complementary angles: $\sin(90^\circ-\theta)=\cos\theta$, $\cos(90^\circ-\theta)=\sin\theta$, $\tan(90^\circ-\theta)=\cot\theta$.
- Identities: $\sin^2\theta+\cos^2\theta=1$; $1+\tan^2\theta=\sec^2\theta$; $1+\cot^2\theta=\csc^2\theta$.
- For one given ratio, draw the triangle and find the third side with Pythagoras.
- Angle of elevation = angle of depression (alternate angles); use $\tan$ for height and ground distance, $\sin$ for height and slant length.
- Prove identities by simplifying one side only.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. $\sin30^\circ$ equals <span class="marks">[1]</span>
   (a) $\frac{\sqrt{3}}{2}$ (b) $\frac{1}{2}$ (c) $1$ (d) $\frac{1}{\sqrt{2}}$
2. $\sin^2\theta+\cos^2\theta=$ <span class="marks">[1]</span>
   (a) 0 (b) $\tan\theta$ (c) 1 (d) $2$
3. $\tan45^\circ=$ <span class="marks">[1]</span>
   (a) 0 (b) $\sqrt{3}$ (c) $\frac{1}{\sqrt{3}}$ (d) 1
4. $\cos60^\circ$ equals <span class="marks">[1]</span>
   (a) $\sin30^\circ$ (b) $\sin60^\circ$ (c) $\tan30^\circ$ (d) $1$
5. $\tan\theta$ equals <span class="marks">[1]</span>
   (a) $\frac{\cos\theta}{\sin\theta}$ (b) $\frac{\sin\theta}{\cos\theta}$ (c) $\sin\theta\cos\theta$ (d) $\frac{1}{\sin\theta}$

::: note Answers to Group A
**1.** (b).
**2.** (c).
**3.** (d).
**4.** (a) — complementary: $\cos60^\circ=\sin30^\circ=\frac{1}{2}$.
**5.** (b).
:::

**Group B — Short answer (2 marks each)**

1. If $\sin\theta=\frac{3}{5}$ find $\cos\theta$. <span class="marks">[2]</span>
2. Evaluate $\sin30^\circ\cos60^\circ+\cos30^\circ\sin60^\circ$. <span class="marks">[2]</span>
3. Evaluate $\tan15^\circ\tan75^\circ$. <span class="marks">[2]</span>
4. A 10 m ladder makes $60^\circ$ with the ground. Find the height it reaches. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** $\cos\theta=\frac{4}{5}$.
**2.** $\frac{1}{4}+\frac{3}{4}=1$.
**3.** $\tan75^\circ=\cot15^\circ$; product $=1$.
**4.** $10\sin60^\circ=5\sqrt{3}\approx8.66$ m.
:::

**Group C — Short answer (3 marks each)**

1. If $\tan\theta=\frac{3}{4}$, find $\sin\theta$ and $\cos\theta$. <span class="marks">[3]</span>
2. Find the value of $4\sin^260^\circ-3\tan^230^\circ$. <span class="marks">[3]</span>
3. Prove that $(\sec\theta-\tan\theta)(\sec\theta+\tan\theta)=1$. <span class="marks">[3]</span>
4. The angle of elevation of the top of a tower from a point 30 m from its foot is $60^\circ$. Find the height. <span class="marks">[3]</span>

::: note Answers to Group C
**1.** $\sin\theta=\frac{3}{5}$, $\cos\theta=\frac{4}{5}$.
**2.** $3-1=2$.
**3.** LHS $=\sec^2\theta-\tan^2\theta=1$.
**4.** $30\sqrt{3}\approx51.96$ m.
:::

**Group D — Long answer (4 marks each)**

1. Prove that $\frac{\sin\theta}{1+\cos\theta}+\frac{1+\cos\theta}{\sin\theta}=2\csc\theta$. <span class="marks">[4]</span>
2. From a point on level ground the angle of elevation of the top of a tower is $30^\circ$; after walking 20 m towards the tower it is $45^\circ$. Find the height of the tower. <span class="marks">[4]</span>
3. From the top of a 40 m cliff the angle of depression of a boat is $30^\circ$. Find the distance of the boat from the foot of the cliff. <span class="marks">[4]</span>
4. Prove that $\frac{1}{1+\sin\theta}+\frac{1}{1-\sin\theta}=2\sec^2\theta$ and find its value for $\theta=30^\circ$. <span class="marks">[4]</span>

::: note Answers to Group D
**1.** See the worked example: the sum is $\frac{2(1+\cos\theta)}{\sin\theta(1+\cos\theta)}=2\csc\theta$.
**2.** $h=10(\sqrt{3}+1)\approx27.32$ m.
**3.** $40\sqrt{3}\approx69.28$ m.
**4.** LHS $=\frac{2}{1-\sin^2\theta}=2\sec^2\theta$. For $\theta=30^\circ$: $2\times\frac{4}{3}=\frac{8}{3}$ (since $\sec^230^\circ=\frac{4}{3}$); directly, $\frac{1}{1.5}+\frac{1}{0.5}=\frac{2}{3}+2=\frac{8}{3}$ ✓.
:::
