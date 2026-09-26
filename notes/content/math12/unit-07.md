---
subject: Mathematics
grade: 12
unit: 7
title: Solution of Triangles
hours: 4
area: Trigonometry
---

Unit 6 built the tools; this unit uses them. To **solve** a triangle is to find
all six parts — three sides and three angles — from the three that are given.
Which law you reach for depends entirely on *which* three you were given, and
there are only four patterns. Three of them have exactly one answer. The fourth,
two sides and a non-included angle, may have two answers, one, or none at all,
and knowing why is worth several marks every year.

::: key What the exam asks
"Solve the triangle in which …" — identify the pattern (SSS, SAS, ASA/AAS, SSA),
use the law that matches, and quote angles to the nearest minute. Always finish
with the check $A+B+C = 180^{\circ}$ and "largest angle faces the largest side".
Applications are height-and-distance problems: draw the figure first, mark every
given, then solve the triangle inside it.
:::

## 7.1 Solution of triangles (simple cases)

Three parts fix a triangle provided at least one of them is a side. (Three angles
do not: AAA gives the *shape* but not the *size*, since every similar triangle
has the same angles.) That leaves four data patterns.

| Given | Name | First step | Answers |
|---|---|---|---|
| three sides | SSS | cosine law, or half angle law | exactly one |
| two sides and the angle **between** them | SAS | cosine law, or tangent law | exactly one |
| one side and two angles | ASA / AAS | third angle, then sine law | exactly one |
| two sides and an angle **not** between them | SSA | sine law | $0$, $1$ or $2$ |

```figure caption="The four patterns. Blue marks the given parts; the label names the law that starts the solution."
import numpy as np
fig, axs = plt.subplots(1, 4, figsize=(5.2,2.3))
P = {'A': np.array([0.35,1.95]), 'B': np.array([0.0,0.0]), 'C': np.array([1.75,0.0])}
def draw(ax, sides, angles, title):
    V = [P['A'],P['B'],P['C']]
    seg = {'a':(P['B'],P['C']), 'b':(P['C'],P['A']), 'c':(P['A'],P['B'])}
    for k,(U,W) in seg.items():
        col = ACCENT if k in sides else GRID
        ax.plot([U[0],W[0]],[U[1],W[1]], color=col, lw=2.4 if k in sides else 1.4)
    for k in angles:
        Q = P[k]
        ax.plot(Q[0], Q[1], 'o', color=ACCENT, ms=6)
    for k,(dx,dy) in (('A',(0.0,0.26)),('B',(-0.22,-0.24)),('C',(0.2,-0.24))):
        ax.text(P[k][0]+dx, P[k][1]+dy, k, fontsize=9, color=INK, ha='center', va='center')
    ax.set_title(title, fontsize=8.4, color=INK, pad=4)
    ax.set_aspect('equal'); ax.axis('off')
    ax.set_xlim(-0.6, 2.3); ax.set_ylim(-0.6, 2.5)
draw(axs[0], 'abc', '',    'SSS\ncosine law')
draw(axs[1], 'ac',  'B',   'SAS\ncosine law')
draw(axs[2], 'a',   'BC',  'ASA\nsine law')
draw(axs[3], 'ab',  'A',   'SSA\nambiguous')
fig.subplots_adjust(wspace=0.45)
```

### Case 1 — three sides (SSS)

Use the cosine law for one angle, then either the cosine law again or the sine
law for a second, and subtract from $180^{\circ}$ for the third. If logarithm
tables are being used, or if an angle is close to $90^{\circ}$ (where the cosine
changes slowly and reading it back is inaccurate), the half angle law is safer.

::: example 7.1 SSS by the cosine law
**Problem.** Solve the triangle $a = 5$ cm, $b = 7$ cm, $c = 8$ cm.

**Solution.**

$$ \cos A = \frac{b^{2}+c^{2}-a^{2}}{2bc} = \frac{49+64-25}{2 \times 7 \times 8}
 = \frac{88}{112} = 0.7857 \ \Rightarrow\ A = 38^{\circ}13' $$

$$ \cos B = \frac{c^{2}+a^{2}-b^{2}}{2ca} = \frac{64+25-49}{2 \times 8 \times 5}
 = \frac{40}{80} = \frac12 \ \Rightarrow\ B = 60^{\circ} $$

$$ C = 180^{\circ} - 38^{\circ}13' - 60^{\circ} = 81^{\circ}47' $$

**Check.** The largest angle $C$ faces the largest side $c = 8$ ✓, and
$\cos C = \frac{25+49-64}{2 \times 5 \times 7} = \frac{10}{70} = 0.1429$, which
is indeed $\cos 81^{\circ}47'$. ✓
:::

::: example 7.2 The same triangle by the half angle law
**Problem.** Solve $a = 5$, $b = 7$, $c = 8$ using half angles, and find the area.

**Solution.** $s = \frac{5+7+8}{2} = 10$, so $s-a = 5$, $s-b = 3$, $s-c = 2$.

$$ \tan\frac{A}{2} = \sqrt{\frac{(s-b)(s-c)}{s(s-a)}}
 = \sqrt{\frac{3 \times 2}{10 \times 5}} = \sqrt{0.12} = 0.3464 $$

so $\frac{A}{2} = 19^{\circ}6'$ and $A = 38^{\circ}13'$ — as before.

$$ \tan\frac{B}{2} = \sqrt{\frac{(s-c)(s-a)}{s(s-b)}}
 = \sqrt{\frac{2 \times 5}{10 \times 3}} = \frac{1}{\sqrt{3}}
 \ \Rightarrow\ \frac{B}{2} = 30^{\circ},\ B = 60^{\circ} $$

$C = 81^{\circ}47'$. Area, by Heron,

$$ \Delta = \sqrt{s(s-a)(s-b)(s-c)} = \sqrt{10 \times 5 \times 3 \times 2}
 = \sqrt{300} = 10\sqrt{3} = 17.32\ \text{cm}^{2} $$

**Check.** $\frac12 ca\sin B = \frac12(8)(5)\sin 60^{\circ} = 20(0.8660)
= 17.32$ ✓.
:::

### Case 2 — two sides and the included angle (SAS)

The cosine law gives the third side at once; the sine law (or another cosine)
then gives a second angle. The tangent law gives both unknown angles without ever
finding the third side, which is why it was the standard method before
calculators.

::: example 7.3 SAS by the cosine law
**Problem.** Solve the triangle $a = 3$ cm, $c = 2$ cm, $B = 60^{\circ}$.

**Solution.** $B$ lies between $a$ and $c$, so

$$ b^{2} = a^{2}+c^{2}-2ac\cos B = 9 + 4 - 2(3)(2)\left(\tfrac12\right)
 = 13 - 6 = 7,\qquad b = \sqrt{7} = 2.646\ \text{cm} $$

$$ \cos A = \frac{b^{2}+c^{2}-a^{2}}{2bc} = \frac{7+4-9}{2(2.646)(2)}
 = \frac{2}{10.583} = 0.1890 \ \Rightarrow\ A = 79^{\circ}6' $$

$$ C = 180^{\circ} - 60^{\circ} - 79^{\circ}6' = 40^{\circ}54' $$

**Check.** $a = 3$ is the largest side and $A = 79^{\circ}6'$ is the largest
angle ✓.
:::

::: example 7.4 The same triangle by the tangent law
**Problem.** Solve $a = 3$, $c = 2$, $B = 60^{\circ}$ by Napier's analogy.

**Solution.** The unknown angles are $A$ and $C$, and

$$ \frac{A+C}{2} = 90^{\circ} - \frac{B}{2} = 90^{\circ}-30^{\circ} = 60^{\circ} $$

$$ \tan\frac{A-C}{2} = \frac{a-c}{a+c}\cot\frac{B}{2}
 = \frac{3-2}{3+2}\cot 30^{\circ} = \frac{1.7321}{5} = 0.3464 $$

$$ \frac{A-C}{2} = 19^{\circ}6' $$

Adding and subtracting:

$$ A = 60^{\circ}+19^{\circ}6' = 79^{\circ}6',\qquad
   C = 60^{\circ}-19^{\circ}6' = 40^{\circ}54' $$

Then $b = \frac{a\sin B}{\sin A} = \frac{3(0.8660)}{0.9822} = 2.646$ cm —
the same triangle as Example 7.3.
:::

### Case 3 — one side and two angles (ASA or AAS)

Subtract to get the third angle, then use the sine law twice. This case is never
ambiguous: the two angles fix the shape and the one side fixes the size.

::: example 7.5 ASA
**Problem.** Solve the triangle $A = 60^{\circ}$, $C = 75^{\circ}$, $b = 10$ cm,
and find its area.

**Solution.** $B = 180^{\circ}-60^{\circ}-75^{\circ} = 45^{\circ}$.

$$ a = \frac{b\sin A}{\sin B} = \frac{10\sin 60^{\circ}}{\sin 45^{\circ}}
 = \frac{10(0.8660)}{0.7071} = 12.25\ \text{cm}\ \ (= 5\sqrt{6}) $$

$$ c = \frac{b\sin C}{\sin B} = \frac{10\sin 75^{\circ}}{\sin 45^{\circ}}
 = \frac{10(0.9659)}{0.7071} = 13.66\ \text{cm} $$

$$ \Delta = \tfrac12 ab\sin C = \tfrac12(12.25)(10)(0.9659) = 59.15\ \text{cm}^{2} $$

**Check.** Sides increase in the same order as their opposite angles:
$b = 10 < a = 12.25 < c = 13.66$ for $45^{\circ} < 60^{\circ} < 75^{\circ}$ ✓.
:::

### Case 4 — two sides and a non-included angle (SSA): the ambiguous case

Suppose $a$, $b$ and $A$ are given. The sine law gives
$\sin B = \frac{b\sin A}{a}$ — but $\sin B$ does not determine $B$: both $B$ and
$180^{\circ}-B$ have the same sine. Geometrically, the side $a$ is a compass arc
swung from $C$, and an arc can cut the base line twice, once, or not at all.

```figure caption="Ambiguous case: $a = 20$, $b = 30$, $A = 30^{\circ}$. The arc of radius $20$ centred at $C$ meets the base at two points, giving $B = 48^{\circ}35'$ or $131^{\circ}25'$."
import numpy as np
fig, ax = plt.subplots(figsize=(5.0,2.9))
A0 = np.array([0.0,0.0]); C = np.array([25.98,15.0])
B1 = np.array([12.752,0.0]); B2 = np.array([39.210,0.0])
th = np.linspace(np.radians(190), np.radians(350), 200)
ax.plot(C[0]+20*np.cos(th), C[1]+20*np.sin(th), color=GRID, lw=1.1)
ax.plot([0,46],[0,0], color=MUTED, lw=1.0)
ax.plot([A0[0],C[0]],[A0[1],C[1]], color=INK, lw=1.8)
ax.plot([C[0],B1[0]],[C[1],B1[1]], color=ACCENT, lw=1.8)
ax.plot([C[0],B2[0]],[C[1],B2[1]], color=SERIES[2], lw=1.8)
ax.plot([C[0],C[0]],[C[1],0.0], color=MUTED, lw=1.0, ls=':')
ax.plot([25.2,25.2,25.98],[0,0.8,0.8], color=MUTED, lw=0.8)
ax.text(25.2, 7.5, 'b sin A = 15', color=MUTED, fontsize=8.6, ha='center',
        va='center', rotation=90)
ax.text(9.5, 8.8, '$b = 30$', color=INK, fontsize=10)
ax.text(13.6, 4.6, '$a = 20$', color=ACCENT, fontsize=10)
ax.text(34.5, 9.0, '$a = 20$', color=SERIES[2], fontsize=10)
ax.text(3.2, 1.2, '$30^{\\circ}$', color=INK, fontsize=9)
for P,lab,dy in ((A0,'A',-2.6),(B1,'$B_1$',-3.0),(B2,'$B_2$',-3.0),(C,'C',1.6)):
    ax.plot(P[0],P[1],'o',color=INK,ms=4)
    ax.text(P[0], P[1]+dy, lab, fontsize=10.5, color=INK, ha='center', va='center')
ax.set_aspect('equal'); ax.axis('off')
ax.set_xlim(-2.5, 48.0); ax.set_ylim(-5.5, 19.0)
```

Compare $a$ with the altitude $b\sin A$ from $C$ to the base, which is the
shortest possible distance from $C$ to the line.

```figure caption="The four possibilities when $a$, $b$ and $A$ are given (with $A$ acute in the first three)."
import numpy as np
fig, axs = plt.subplots(2, 2, figsize=(5.0,3.4))
A0 = np.array([0.0,0.0]); C = np.array([25.98,15.0]); h = 15.0
cases = [(11.0, 'a < b sin A : no triangle', '#d9534f'),
         (15.0, 'a = b sin A : one (right-angled)', ACCENT),
         (20.0, 'b sin A < a < b : two triangles', ACCENT),
         (34.0, 'a ' + chr(8805) + ' b : one triangle', ACCENT)]
for ax,(r,lab,col) in zip(axs.ravel(), cases):
    th = np.linspace(np.radians(185), np.radians(355), 200)
    ax.plot(C[0]+r*np.cos(th), C[1]+r*np.sin(th), color=GRID, lw=1.0)
    ax.plot([-4,62],[0,0], color=MUTED, lw=0.9)
    ax.plot([A0[0],C[0]],[A0[1],C[1]], color=INK, lw=1.5)
    ax.plot([C[0],C[0]],[C[1],0.0], color=MUTED, lw=0.8, ls=':')
    if r >= h:
        d = np.sqrt(r*r - h*h)
        xs = [C[0]+d] if r >= 30 else [C[0]-d, C[0]+d]
        for x in xs:
            ax.plot([C[0],x],[C[1],0.0], color=col, lw=1.6)
            ax.plot(x, 0, 'o', color=col, ms=3.5)
    ax.plot(A0[0],A0[1],'o',color=INK,ms=3.5); ax.plot(C[0],C[1],'o',color=INK,ms=3.5)
    ax.set_title(lab, fontsize=7.8, color=col, pad=3)
    ax.set_aspect('equal'); ax.axis('off')
    ax.set_xlim(-6, 64); ax.set_ylim(-4, 19)
fig.subplots_adjust(hspace=0.02, wspace=0.05)
```

::: key The SSA test (with $A$ acute)
Compute $h = b\sin A$. Then

- $a < h$: **no** triangle ($\sin B > 1$);
- $a = h$: **one** triangle, right-angled at $B$;
- $h < a < b$: **two** triangles, $B$ and $180^{\circ}-B$;
- $a \ge b$: **one** triangle (the obtuse option is rejected).

If $A$ is obtuse there is one triangle when $a > b$ and none otherwise.
:::

::: example 7.6 Two triangles
**Problem.** In a triangle $a = 20$ cm, $b = 30$ cm and $A = 30^{\circ}$. Solve it.

**Solution.** $h = b\sin A = 30(0.5) = 15$, and $15 < 20 < 30$, so **two**
triangles exist. By the sine law,

$$ \sin B = \frac{b\sin A}{a} = \frac{30 \times 0.5}{20} = 0.75 $$

$$ B_1 = 48^{\circ}35' \qquad\text{or}\qquad B_2 = 180^{\circ}-48^{\circ}35'
 = 131^{\circ}25' $$

Both are admissible because $A + B < 180^{\circ}$ in each case.

*First triangle:* $C_1 = 180^{\circ}-30^{\circ}-48^{\circ}35' = 101^{\circ}25'$, so

$$ c_1 = \frac{a\sin C_1}{\sin A} = \frac{20(0.9803)}{0.5} = 39.21\ \text{cm} $$

*Second triangle:* $C_2 = 180^{\circ}-30^{\circ}-131^{\circ}25' = 18^{\circ}35'$, so

$$ c_2 = \frac{20(0.3189)}{0.5} = 12.75\ \text{cm} $$

**Check.** In the figure above, $AB_1 = 12.75$ and $AB_2 = 39.21$, and
$25.98 \pm 13.23$ gives exactly those two feet. ✓
:::

::: example 7.7 No triangle
**Problem.** Can a triangle have $a = 10$ cm, $b = 30$ cm and $A = 30^{\circ}$?

**Solution.** $\sin B = \frac{b\sin A}{a} = \frac{30 \times 0.5}{10} = 1.5$.
No angle has a sine greater than $1$, so **no such triangle exists**.
Equivalently $h = b\sin A = 15 > 10 = a$: the side $a$ is too short to reach the
base line. ∎
:::

::: example 7.8 One triangle
**Problem.** Solve $a = 40$ cm, $b = 30$ cm, $A = 30^{\circ}$.

**Solution.** Here $a > b$, so only one triangle exists.

$$ \sin B = \frac{30 \times 0.5}{40} = 0.375 \ \Rightarrow\ B = 22^{\circ}1' $$

The second value $157^{\circ}59'$ is rejected: it would make
$A+B = 187^{\circ}59' > 180^{\circ}$. (Equivalently, $b < a$ forces $B < A$, so
$B$ cannot be obtuse.)

$$ C = 180^{\circ}-30^{\circ}-22^{\circ}1' = 127^{\circ}59' $$

$$ c = \frac{a\sin C}{\sin A} = \frac{40(0.7883)}{0.5} = 63.06\ \text{cm} $$
:::

::: caution Do not throw away the obtuse root too soon
When the sine law gives $\sin B = k$, write **both** $B$ and $180^{\circ}-B$, then
test each: keep it only if $A+B < 180^{\circ}$. Students lose marks for silently
taking the calculator's answer. Conversely, if the given angle is opposite the
**larger** side, the obtuse root is always impossible — say so, do not just drop it.
:::

## 7.2 Heights and distances

Every height-and-distance problem is a triangle with one known side (a measured
baseline) and two known angles, so Case 3 solves it. Draw the figure, mark the
angles of elevation from the horizontal, and name the triangle you intend to use.

```figure caption="Angle of elevation $30^{\circ}$ at $P$; after walking $40$ m to $Q$ it is $60^{\circ}$. Drawn to scale: $h = 20\sqrt{3} = 34.64$ m."
import numpy as np
fig, ax = plt.subplots(figsize=(5.0,2.7))
P = np.array([0.0,0.0]); Q = np.array([40.0,0.0]); T = np.array([60.0,0.0])
S = np.array([60.0,34.641])
ax.plot([-4,68],[0,0], color=MUTED, lw=1.1)
ax.plot([T[0],S[0]],[T[1],S[1]], color=INK, lw=2.2)
ax.plot([P[0],S[0]],[P[1],S[1]], color=ACCENT, lw=1.4, ls='--')
ax.plot([Q[0],S[0]],[Q[1],S[1]], color=ACCENT, lw=1.4)
ax.plot([57.6,57.6,60],[0,2.4,2.4], color=MUTED, lw=0.9)
ax.text(6.0, 1.3, '$30^{\\circ}$', color=ACCENT, fontsize=9)
ax.text(43.0, 1.3, '$60^{\\circ}$', color=ACCENT, fontsize=9)
ax.text(20.0, -3.4, '$40$ m', color=INK, fontsize=9.5, ha='center')
ax.text(50.0, -3.4, '$20$ m', color=MUTED, fontsize=9.5, ha='center')
ax.text(61.5, 17.0, '$h$', color=INK, fontsize=11)
for x,lab in ((0,'P'),(40,'Q'),(60,'T')):
    ax.plot(x,0,'o',color=INK,ms=4)
    ax.text(x, -6.2, lab, fontsize=10.5, color=INK, ha='center')
ax.text(60.0, 37.0, 'S', fontsize=10.5, color=INK, ha='center')
ax.set_aspect('equal'); ax.axis('off')
ax.set_xlim(-6, 72); ax.set_ylim(-8.5, 41)
```

::: example 7.9 Height of a tower
**Problem.** From a point $P$ on level ground the angle of elevation of the top
of a tower is $30^{\circ}$. Walking $40$ m towards the tower to a point $Q$, the
elevation becomes $60^{\circ}$. Find the height of the tower.

**Solution.** Let $S$ be the top and $T$ the foot. In triangle $PQS$:

- $\angle SPQ = 30^{\circ}$;
- $\angle SQT = 60^{\circ}$ is an **exterior** angle of triangle $PQS$ at $Q$,
  so $\angle PQS = 180^{\circ}-60^{\circ} = 120^{\circ}$;
- hence $\angle PSQ = 180^{\circ}-30^{\circ}-120^{\circ} = 30^{\circ}$.

Triangle $PQS$ therefore has two equal angles, so $QS = PQ = 40$ m. Now in the
right triangle $QTS$,

$$ h = ST = QS\sin 60^{\circ} = 40 \times \frac{\sqrt{3}}{2} = 20\sqrt{3}
 = 34.64\ \text{m} $$

**Check.** $QT = h\cot 60^{\circ} = 20$ m and $PT = h\cot 30^{\circ} = 60$ m, and
$PT - QT = 40$ m ✓.
:::

```figure caption="Width of a river: the baseline $AB = 100$ m is measured along one bank and the angles to the tree at $C$ are read at $A$ and $B$."
import numpy as np
fig, ax = plt.subplots(figsize=(5.0,2.8))
A = np.array([0.0,0.0]); B = np.array([100.0,0.0]); C = np.array([36.603,63.397])
ax.fill_between([-12,112],[0,0],[63.397,63.397], color=GRID, alpha=0.35)
ax.plot([-12,112],[0,0], color=MUTED, lw=1.4)
ax.plot([-12,112],[63.397,63.397], color=MUTED, lw=1.4)
ax.plot([A[0],B[0]],[A[1],B[1]], color=INK, lw=2.0)
ax.plot([A[0],C[0]],[A[1],C[1]], color=ACCENT, lw=1.6)
ax.plot([B[0],C[0]],[B[1],C[1]], color=ACCENT, lw=1.6)
ax.plot([C[0],C[0]],[C[1],0.0], color=MUTED, lw=1.0, ls=':')
ax.plot([33.6,33.6,36.6],[0,3.0,3.0], color=MUTED, lw=0.8)
ax.text(11.0, 4.0, '$60^{\\circ}$', color=ACCENT, fontsize=9)
ax.text(84.0, 4.0, '$45^{\\circ}$', color=ACCENT, fontsize=9)
ax.text(50.0, -7.5, '$AB = 100$ m', color=INK, fontsize=9.5, ha='center')
ax.text(58.0, 21.0, 'width $= 63.4$ m', color=MUTED, fontsize=9, ha='center')
ax.text(12.0, 28.0, '$b$', color=ACCENT, fontsize=10)
ax.text(76.0, 33.0, '$a$', color=ACCENT, fontsize=10)
for P,lab,dy in ((A,'A',-5.5),(B,'B',-5.5),(C,'C',5.0)):
    ax.plot(P[0],P[1],'o',color=INK,ms=4)
    ax.text(P[0], P[1]+dy, lab, fontsize=10.5, color=INK, ha='center')
ax.set_aspect('equal'); ax.axis('off')
ax.set_xlim(-14, 114); ax.set_ylim(-11, 72)
```

::: example 7.10 Width of a river
**Problem.** $A$ and $B$ are two points $100$ m apart on one straight bank of a
river. A tree $C$ stands on the opposite bank. It is found that
$\angle CAB = 60^{\circ}$ and $\angle CBA = 45^{\circ}$. Find $AC$, $BC$ and the
width of the river.

**Solution.** $\angle ACB = 180^{\circ}-60^{\circ}-45^{\circ} = 75^{\circ}$
(Case 3, ASA). By the sine law, with $c = AB = 100$,

$$ AC = \frac{c\sin B}{\sin C} = \frac{100\sin 45^{\circ}}{\sin 75^{\circ}}
 = \frac{100(0.7071)}{0.9659} = 73.21\ \text{m} $$

$$ BC = \frac{c\sin A}{\sin C} = \frac{100(0.8660)}{0.9659} = 89.66\ \text{m} $$

The width is the perpendicular distance from $C$ to the bank $AB$:

$$ \text{width} = AC\sin 60^{\circ} = 73.21 \times 0.8660 = 63.40\ \text{m} $$

**Check.** The same width from the other triangle:
$BC\sin 45^{\circ} = 89.66(0.7071) = 63.40$ m ✓.
:::

::: example 7.11 Area of a field
**Problem.** A triangular field in Chitwan has sides $120$ m, $170$ m and
$250$ m. Find its area in square metres and in ropani
($1$ ropani $= 508.72$ m²).

**Solution.** $s = \frac{120+170+250}{2} = 270$ m, so $s-a = 150$, $s-b = 100$,
$s-c = 20$.

$$ \Delta = \sqrt{270 \times 150 \times 100 \times 20} = \sqrt{81\,000\,000}
 = 9000\ \text{m}^{2} $$

$$ \frac{9000}{508.72} = 17.69\ \text{ropani} $$

**Check.** The field is nearly degenerate ($120+170 = 290$, only $40$ m more than
$250$), so a small area for such long sides is exactly what we expect. ✓
:::

::: example 7.12 A two-bearing problem
**Problem.** Two roads leave a junction $J$ at an angle of $60^{\circ}$. A cyclist
rides $3$ km along one and a walker $2$ km along the other. How far apart are
they, and what angle does the line joining them make with the cyclist's road?

**Solution.** This is SAS with the $60^{\circ}$ angle included, exactly the
triangle of Example 7.3 measured in kilometres: $a = 3$, $c = 2$, $B = 60^{\circ}$.

$$ b^{2} = 9+4-2(3)(2)\left(\tfrac12\right) = 7,\qquad b = 2.65\ \text{km} $$

The required angle is the one at the cyclist's end, opposite the walker's
distance $c = 2$:

$$ \cos C = \frac{a^{2}+b^{2}-c^{2}}{2ab} = \frac{9+7-4}{2(3)(2.646)} = 0.7559
 \ \Rightarrow\ C = 40^{\circ}54' $$

So they are $2.65$ km apart, and the joining line makes $40^{\circ}54'$ with the
cyclist's road.
:::

::: tip Marking points in a solution
State the case (SSS, SAS, …) in words before computing — it shows the examiner
you chose the law deliberately. Keep five figures during the work and round only
at the end. Give angles in degrees and minutes ($1^{\circ} = 60'$): $0.5^{\circ}$
is $30'$, not $50'$.
:::

## Chapter summary

- Three parts solve a triangle if at least one is a side; AAA gives shape only.
- **SSS:** cosine law $\cos A = \frac{b^{2}+c^{2}-a^{2}}{2bc}$, or half angles
  $\tan\frac{A}{2} = \sqrt{\frac{(s-b)(s-c)}{s(s-a)}}$.
- **SAS:** $a^{2} = b^{2}+c^{2}-2bc\cos A$; or Napier,
  $\tan\frac{A-B}{2} = \frac{a-b}{a+b}\cot\frac{C}{2}$ with
  $\frac{A+B}{2} = 90^{\circ}-\frac{C}{2}$.
- **ASA/AAS:** third angle first, then $\frac{a}{\sin A} = \frac{b}{\sin B}$.
- **SSA is ambiguous:** with $h = b\sin A$ and $A$ acute — none if $a<h$, one
  (right-angled) if $a = h$, two if $h<a<b$, one if $a \ge b$.
- Area: $\Delta = \frac12 ab\sin C = \sqrt{s(s-a)(s-b)(s-c)}$.
- Heights and distances: draw the figure, use the exterior-angle trick to find
  the angle at the near point, then solve the triangle on the baseline.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. To solve a triangle given its three sides you should start with <span class="marks">[1]</span>
   (a) the sine law (b) the cosine law (c) the projection law (d) the angle sum
2. A triangle can **not** be solved from <span class="marks">[1]</span>
   (a) SSS (b) SAS (c) AAA (d) ASA
3. If $a = 20$, $b = 30$, $A = 30^{\circ}$, the number of possible triangles is <span class="marks">[1]</span>
   (a) $0$ (b) $1$ (c) $2$ (d) infinitely many
4. In a triangle $b = 4$, $c = 5$ and $A = 60^{\circ}$; then $a$ equals <span class="marks">[1]</span>
   (a) $\sqrt{21}$ (b) $\sqrt{41}$ (c) $\sqrt{61}$ (d) $9$
5. If $\sin B = 0.8$ and $b < a$, then $B$ is <span class="marks">[1]</span>
   (a) $53^{\circ}8'$ only (b) $126^{\circ}52'$ only (c) either (d) neither
6. From the top of a tower $h$ m high the angle of depression of a point on the
   ground is $45^{\circ}$; the point is at a distance <span class="marks">[1]</span>
   (a) $\frac{h}{2}$ (b) $h$ (c) $h\sqrt{3}$ (d) $2h$

::: note Answers to Group A
**1.** (b) — the sine law would need an angle, which SSS does not give.

**2.** (c) — AAA fixes only the shape; all similar triangles share it.

**3.** (c) — $h = b\sin A = 15$ and $15 < 20 < 30$, the two-triangle case.

**4.** (a) — $a^{2} = 16+25-2(4)(5)\left(\frac12\right) = 21$.

**5.** (a) — $b < a$ gives $B < A$, so $B$ cannot be obtuse.

**6.** (b) — $\tan 45^{\circ} = h/d = 1$, so $d = h$.
:::

**Group B — Short answer (5 marks each)**

1. Solve the triangle $a = 5$ cm, $b = 7$ cm, $c = 8$ cm and find its area.
   <span class="marks">[5]</span>
2. Solve the triangle in which $a = 3$ cm, $c = 2$ cm and $B = 60^{\circ}$, using
   the tangent law for the angles. <span class="marks">[5]</span>
3. Solve the triangle $A = 60^{\circ}$, $C = 75^{\circ}$, $b = 10$ cm.
   <span class="marks">[5]</span>
4. Show that no triangle exists with $a = 10$ cm, $b = 30$ cm, $A = 30^{\circ}$,
   but that exactly one exists with $a = 40$ cm, $b = 30$ cm, $A = 30^{\circ}$;
   solve the second. <span class="marks">[5]</span>
5. The angle of elevation of the top of a tower from a point on level ground is
   $30^{\circ}$; on walking $40$ m towards the tower it becomes $60^{\circ}$.
   Find the height of the tower. <span class="marks">[5]</span>
6. A triangular plot has sides $120$ m, $170$ m and $250$ m. Find its area and
   the radius of its circumcircle. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** $\cos A = \frac{49+64-25}{112} = 0.7857$, so $A = 38^{\circ}13'$;
$\cos B = \frac{64+25-49}{80} = 0.5$, so $B = 60^{\circ}$; and
$C = 81^{\circ}47'$. With $s = 10$,
$\Delta = \sqrt{10 \times 5 \times 3 \times 2} = 10\sqrt{3} = 17.32$ cm².

**2.** $\frac{A+C}{2} = 90^{\circ}-30^{\circ} = 60^{\circ}$ and
$\tan\frac{A-C}{2} = \frac{3-2}{3+2}\cot 30^{\circ} = \frac{1.7321}{5}
= 0.3464$, so $\frac{A-C}{2} = 19^{\circ}6'$. Hence $A = 79^{\circ}6'$,
$C = 40^{\circ}54'$, and
$b = \frac{a\sin B}{\sin A} = \frac{3(0.8660)}{0.9822} = 2.65$ cm
$(= \sqrt{7})$.

**3.** $B = 45^{\circ}$;
$a = \frac{10\sin 60^{\circ}}{\sin 45^{\circ}} = 12.25$ cm;
$c = \frac{10\sin 75^{\circ}}{\sin 45^{\circ}} = 13.66$ cm.
(Area, if wanted: $\frac12 ab\sin C = 59.15$ cm².)

**4.** First: $\sin B = \frac{30 \times 0.5}{10} = 1.5 > 1$, impossible, so no
triangle. Second: $a = 40 > b = 30$, so exactly one. $\sin B
= \frac{30 \times 0.5}{40} = 0.375$ gives $B = 22^{\circ}1'$ (the obtuse root
$157^{\circ}59'$ fails $A+B<180^{\circ}$). Then $C = 127^{\circ}59'$ and
$c = \frac{40\sin C}{\sin 30^{\circ}} = \frac{40(0.7883)}{0.5} = 63.06$ cm.

**5.** With $P$, $Q$ the two points and $S$ the top: $\angle SPQ = 30^{\circ}$,
$\angle PQS = 180^{\circ}-60^{\circ} = 120^{\circ}$, so
$\angle PSQ = 30^{\circ}$ and the triangle $PQS$ is isosceles with
$QS = PQ = 40$ m. Then $h = QS\sin 60^{\circ} = 40\left(\frac{\sqrt{3}}{2}\right)
= 20\sqrt{3} = 34.64$ m.

**6.** $s = 270$ m; $\Delta = \sqrt{270 \times 150 \times 100 \times 20}
= 9000$ m². Then
$R = \frac{abc}{4\Delta} = \frac{120 \times 170 \times 250}{4 \times 9000}
= \frac{5\,100\,000}{36\,000} = 141.67$ m.
:::

**Group C — Long answer (8 marks each)**

1. Explain what is meant by solving a triangle and list the four cases of given
   data. Solve the triangle $a = 20$ cm, $b = 30$ cm, $A = 30^{\circ}$
   completely, explaining why it has two solutions, and state the condition for
   each of the other possibilities. <span class="marks">[8]</span>
2. Derive the tangent law $\tan\frac{A-B}{2} = \frac{a-b}{a+b}\cot\frac{C}{2}$
   and use it to solve the triangle $a = 9$ cm, $b = 7$ cm, $C = 60^{\circ}$.
   Find the area of that triangle. <span class="marks">[8]</span>
3. $A$ and $B$ are points $100$ m apart on a straight bank of a river and $C$ is
   a tree on the opposite bank, with $\angle CAB = 60^{\circ}$ and
   $\angle CBA = 45^{\circ}$. Find $AC$, $BC$, the width of the river and the
   area of triangle $ABC$. <span class="marks">[8]</span>

::: note Answers to Group C
**1.** *Solving* a triangle means finding all six parts from three given ones,
at least one of which must be a side. The four cases are SSS and SAS (cosine or
tangent law), ASA/AAS (angle sum, then sine law) and SSA (sine law, possibly
ambiguous).
Here $h = b\sin A = 30 \times 0.5 = 15$ and $15 < a = 20 < b = 30$, which is the
two-triangle case: the arc of radius $a$ centred at $C$ cuts the base twice.
$\sin B = \frac{b\sin A}{a} = 0.75$, so $B = 48^{\circ}35'$ or $131^{\circ}25'$,
and both satisfy $A+B < 180^{\circ}$.
*First:* $C = 101^{\circ}25'$, $c = \frac{20\sin C}{\sin 30^{\circ}}
= \frac{20(0.9803)}{0.5} = 39.21$ cm.
*Second:* $C = 18^{\circ}35'$, $c = \frac{20(0.3189)}{0.5} = 12.75$ cm.
Other possibilities (for acute $A$): $a < h$ gives no triangle, $a = h$ gives one
right-angled triangle, and $a \ge b$ gives exactly one triangle.

**2.** *Derivation.* By the sine law $a = 2R\sin A$, $b = 2R\sin B$, so
$$ \frac{a-b}{a+b} = \frac{\sin A-\sin B}{\sin A+\sin B}
= \frac{2\cos\frac{A+B}{2}\sin\frac{A-B}{2}}{2\sin\frac{A+B}{2}\cos\frac{A-B}{2}}
= \cot\frac{A+B}{2}\tan\frac{A-B}{2} $$
and since $\frac{A+B}{2} = 90^{\circ}-\frac{C}{2}$,
$\cot\frac{A+B}{2} = \tan\frac{C}{2}$, giving
$\tan\frac{A-B}{2} = \frac{a-b}{a+b}\cot\frac{C}{2}$.
*Application.* $\frac{A+B}{2} = 60^{\circ}$ and
$\tan\frac{A-B}{2} = \frac{2}{16}\cot 30^{\circ} = 0.2165$, so
$\frac{A-B}{2} = 12^{\circ}13'$, $A = 72^{\circ}13'$, $B = 47^{\circ}47'$.
Third side: $c^{2} = 81+49-2(9)(7)\left(\frac12\right) = 67$, $c = 8.19$ cm.
Area: $\Delta = \frac12 ab\sin C = \frac12(9)(7)(0.8660) = 27.28$ cm².

**3.** $\angle ACB = 180^{\circ}-60^{\circ}-45^{\circ} = 75^{\circ}$, so with
$AB = c = 100$ m the sine law gives
$$ AC = \frac{100\sin 45^{\circ}}{\sin 75^{\circ}} = 73.21\ \text{m},\qquad
BC = \frac{100\sin 60^{\circ}}{\sin 75^{\circ}} = 89.66\ \text{m} $$
Width $= AC\sin 60^{\circ} = 73.21(0.8660) = 63.40$ m (check:
$BC\sin 45^{\circ} = 63.40$ m ✓).
Area $= \frac12 \times AB \times \text{width} = \frac12(100)(63.40)
= 3170$ m², and equally $\frac12(AC)(BC)\sin 75^{\circ}
= \frac12(73.21)(89.66)(0.9659) = 3170$ m².
:::
