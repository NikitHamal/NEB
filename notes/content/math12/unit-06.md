---
subject: Mathematics
grade: 12
unit: 6
title: Properties of a Triangle
hours: 8
area: Trigonometry
---

A triangle has six parts — three sides and three angles. Fix any three of them
(as long as one is a side) and the other three are decided. The formulae in this
unit are the dictionary that translates between the two halves: sides into
angles, angles into sides. The sine law, the cosine law, the tangent law, the
projection laws and the half-angle laws are all consequences of one picture, an
altitude dropped inside a triangle, and every one of them is derivable in a few
lines. Learn the derivations, not just the results — the board asks for them.

::: key What the exam asks
Three shapes of question. **(i)** "Prove the sine/cosine/tangent/projection/
half-angle law" — a straight 5- or 8-mark derivation. **(ii)** "In a triangle
$a = 13$, $b = 14$, $c = 15$, find $\cos A$, $\tan\frac{A}{2}$, the area, $R$,
$r$" — substitution, but you must pick the right formula. **(iii)** "Prove that
$a(b\cos C - c\cos B) = b^{2}-c^{2}$" — an identity. Turn everything into sides
(projection or cosine law) **or** everything into sines (sine law), never a
mixture.
:::

## 6.1 Sine law

Throughout the unit $ABC$ is a triangle with **standard notation**: the side
opposite vertex $A$ has length $a$, the side opposite $B$ is $b$, the side
opposite $C$ is $c$, and $A$, $B$, $C$ also denote the sizes of the angles, so
$A + B + C = 180^{\circ}$. Write $s = \frac{a+b+c}{2}$ for the **semi-perimeter**
and $\Delta$ for the area. A single triangle, $a = 13$, $b = 14$, $c = 15$, is
used as the running example in this chapter; its numbers are unusually clean.

```figure caption="Standard notation: the side facing angle $A$ is $a$. The running example has $a = 13$, $b = 14$, $c = 15$."
import numpy as np
from matplotlib.patches import Arc
fig, ax = plt.subplots(figsize=(4.6,3.2))
B = np.array([0.0,0.0]); C = np.array([13.0,0.0]); A = np.array([7.6154,12.9231])
T = np.array([A,B,C,A])
ax.plot(T[:,0], T[:,1], color=INK, lw=1.8)
for P,lab,dx,dy in ((A,'A',0.0,0.9),(B,'B',-0.9,-1.0),(C,'C',0.7,-1.0)):
    ax.plot(P[0], P[1], 'o', color=INK, ms=4.5)
    ax.text(P[0]+dx, P[1]+dy, lab, fontsize=12, color=INK, ha='center', va='center')
def side(P,Q,txt,off):
    M = (P+Q)/2.0; d = Q-P; n = np.array([-d[1], d[0]]); n = n/np.hypot(*n)
    ax.text(M[0]+off*n[0], M[1]+off*n[1], txt, fontsize=11, color=ACCENT,
            ha='center', va='center')
side(B,C,'$a = 13$',-1.5); side(C,A,'$b = 14$',-1.5); side(A,B,'$c = 15$',-1.6)
def arcat(P,Q,Rp,rad,lab):
    a1 = np.degrees(np.arctan2(*(Q-P)[::-1])); a2 = np.degrees(np.arctan2(*(Rp-P)[::-1]))
    if (a2-a1) % 360 > 180: a1, a2 = a2, a1
    ax.add_patch(Arc(P, 2*rad, 2*rad, theta1=a1, theta2=a2, color=MUTED, lw=1.2))
    m = np.radians(a1 + ((a2-a1) % 360)/2.0)
    ax.text(P[0]+1.65*rad*np.cos(m), P[1]+1.65*rad*np.sin(m), lab,
            fontsize=10.5, color=MUTED, ha='center', va='center')
arcat(B,A,C,2.2,'$B$'); arcat(C,A,B,2.2,'$C$'); arcat(A,B,C,2.4,'$A$')
ax.set_aspect('equal'); ax.axis('off')
ax.set_xlim(-2.6, 15.6); ax.set_ylim(-2.8, 14.8)
```

::: derivation The sine law
Drop the perpendicular $AD$ from $A$ onto $BC$, and call its length $h$.

In the right triangle $ABD$, the angle at $B$ is $B$ and the hypotenuse is
$AB = c$, so $h = c\sin B$. In the right triangle $ACD$, the angle at $C$ is $C$
and the hypotenuse is $AC = b$, so $h = b\sin C$. The two expressions are the
same length, hence

$$ c\sin B = b\sin C \quad\Longrightarrow\quad \frac{b}{\sin B} = \frac{c}{\sin C} $$

Repeating with the perpendicular from $B$ onto $CA$ gives
$\frac{a}{\sin A} = \frac{c}{\sin C}$. Combining,

$$ \frac{a}{\sin A} = \frac{b}{\sin B} = \frac{c}{\sin C} $$
:::

The common value of the three ratios is not an accident — it is the diameter of
the circle through $A$, $B$ and $C$ (the **circumcircle**, radius $R$).

::: derivation The common ratio equals $2R$
Draw the circumcircle, centre $O$, and the diameter $BA'$ through $B$. Then

1. $\angle BCA' = 90^{\circ}$, because an angle in a semicircle is a right angle.
2. $\angle BA'C = \angle BAC = A$, because angles in the same segment
   (standing on the chord $BC$) are equal.

In the right triangle $BCA'$, $\sin(\angle BA'C) = \dfrac{BC}{BA'}$, that is
$\sin A = \dfrac{a}{2R}$, so $\dfrac{a}{\sin A} = 2R$. Hence

$$ \frac{a}{\sin A} = \frac{b}{\sin B} = \frac{c}{\sin C} = 2R $$
:::

```figure caption="Why the common ratio is $2R$. The angle at $A'$ equals $A$, and $\angle BCA' = 90^{\circ}$, so $a = 2R\sin A$."
import numpy as np
fig, ax = plt.subplots(figsize=(4.4,3.3))
O = np.array([6.5,4.875]); R = 8.125
t = np.linspace(0, 2*np.pi, 400)
ax.plot(O[0]+R*np.cos(t), O[1]+R*np.sin(t), color=GRID, lw=1.3)
B = np.array([0.0,0.0]); C = np.array([13.0,0.0]); A = np.array([7.6154,12.9231])
Ap = 2*O - B
ax.plot([A[0],B[0],C[0],A[0]], [A[1],B[1],C[1],A[1]], color=INK, lw=1.7)
ax.plot([B[0],Ap[0]], [B[1],Ap[1]], color=ACCENT, lw=1.4, ls='--')
ax.plot([C[0],Ap[0]], [C[1],Ap[1]], color=ACCENT, lw=1.4)
ax.plot([O[0]],[O[1]], 'o', color=MUTED, ms=4)
ax.text(2.2, 3.2, '$2R$', color=ACCENT, fontsize=11)
for P,lab,dx,dy in ((A,'A',-0.2,1.0),(B,'B',-1.1,-0.5),(C,'C',0.9,-0.8),
                    (Ap,"$A'$",1.0,0.6),(O,'O',-0.9,0.4)):
    ax.plot(P[0],P[1],'o',color=INK,ms=4)
    ax.text(P[0]+dx, P[1]+dy, lab, fontsize=11.5, color=INK, ha='center', va='center')
ax.text(6.4, -1.4, '$a$', color=ACCENT, fontsize=11, ha='center')
ax.plot([12.3,12.3,13.0],[0.0,0.7,0.7], color=MUTED, lw=1.0)
ax.text(10.6, 1.15, '$90^{\\circ}$', color=MUTED, fontsize=9.5)
ax.set_aspect('equal'); ax.axis('off')
ax.set_xlim(-2.5, 16.5); ax.set_ylim(-3.0, 14.2)
```

::: key Sine law
$$ \frac{a}{\sin A} = \frac{b}{\sin B} = \frac{c}{\sin C} = 2R
\qquad\text{equivalently}\qquad a = 2R\sin A,\ \ b = 2R\sin B,\ \ c = 2R\sin C $$
Use it when you know **two angles and a side**, or **two sides and the angle
opposite one of them**. In an identity, $a = 2R\sin A$ is the switch that turns
every side into a sine and lets the $2R$ cancel.
:::

::: example 6.1 Two angles and a side
**Problem.** In triangle $ABC$, $A = 30^{\circ}$, $B = 45^{\circ}$ and
$a = 10$ cm. Find $b$ and $c$.

**Solution.**
$C = 180^{\circ} - 30^{\circ} - 45^{\circ} = 105^{\circ}$ — angle sum.

By the sine law $\dfrac{b}{\sin B} = \dfrac{a}{\sin A}$, so

$$ b = \frac{a\sin B}{\sin A} = \frac{10\sin 45^{\circ}}{\sin 30^{\circ}}
 = \frac{10 \times \frac{1}{\sqrt{2}}}{\frac{1}{2}} = 10\sqrt{2} = 14.14\ \text{cm} $$

For $c$, use $\sin 105^{\circ} = \sin(60^{\circ}+45^{\circ})
= \sin 60^{\circ}\cos 45^{\circ} + \cos 60^{\circ}\sin 45^{\circ}
= \frac{\sqrt{6}+\sqrt{2}}{4} = 0.9659$:

$$ c = \frac{a\sin C}{\sin A} = \frac{10 \times 0.9659}{0.5} = 19.32\ \text{cm} $$

**Check.** The largest side $c$ faces the largest angle $C$. ✓
:::

::: example 6.2 An identity done by the sine law
**Problem.** In any triangle prove that
$a(\sin B - \sin C) + b(\sin C - \sin A) + c(\sin A - \sin B) = 0$.

**Solution.** Put $a = 2R\sin A$, $b = 2R\sin B$, $c = 2R\sin C$ — the sine law
in the form that removes all the sides:

$$ \text{LHS} = 2R\big[\sin A(\sin B - \sin C) + \sin B(\sin C - \sin A)
+ \sin C(\sin A - \sin B)\big] $$

Expand inside the bracket:

$$ \sin A\sin B - \sin A\sin C + \sin B\sin C - \sin B\sin A
+ \sin C\sin A - \sin C\sin B $$

Each product appears twice with opposite signs, so the bracket is $0$, and
$\text{LHS} = 0$. ∎
:::

## 6.2 Cosine law

The sine law fails when you know all three sides, or two sides and the angle
*between* them: in both cases every equation it gives has two unknowns. The
cosine law covers exactly those cases.

::: derivation The cosine law
Drop the perpendicular $CD$ from $C$ onto $AB$, of length $h$, and let $D$ lie
on $AB$ with $AD = b\cos A$ (from right triangle $ACD$, hypotenuse $b$) and
$h = b\sin A$. Then $DB = c - b\cos A$.

Apply Pythagoras in right triangle $CDB$:

$$ a^{2} = h^{2} + DB^{2} = (b\sin A)^{2} + (c - b\cos A)^{2} $$
$$ a^{2} = b^{2}\sin^{2}A + c^{2} - 2bc\cos A + b^{2}\cos^{2}A $$

Now $b^{2}\sin^{2}A + b^{2}\cos^{2}A = b^{2}(\sin^{2}A + \cos^{2}A) = b^{2}$, so

$$ a^{2} = b^{2} + c^{2} - 2bc\cos A $$

If $A$ is obtuse, $D$ falls outside the segment $AB$ and $\cos A$ is negative;
the signed length $AD = b\cos A$ is then negative and every line above still
holds. Cycling the letters gives the other two forms.
:::

```figure caption="The altitude from $A$. Left: $h = c\sin B = b\sin C$ (sine law) and $BD = c\cos B$, $DC = b\cos C$ (projection law). Right: for an obtuse $B$ the foot $D$ falls outside, and $\cos B < 0$."
import numpy as np
fig, axs = plt.subplots(1, 2, figsize=(5.1,2.7))
ax = axs[0]
B = np.array([0.0,0.0]); C = np.array([13.0,0.0]); A = np.array([7.6154,12.9231])
D = np.array([A[0], 0.0])
ax.plot([A[0],B[0],C[0],A[0]], [A[1],B[1],C[1],A[1]], color=INK, lw=1.7)
ax.plot([A[0],D[0]], [A[1],D[1]], color=ACCENT, lw=1.4, ls='--')
ax.plot([D[0]-0.9,D[0]-0.9,D[0]],[0,0.9,0.9], color=MUTED, lw=0.9)
for P,lab,dx,dy in ((A,'A',0,1.3),(B,'B',-1.2,-1.3),(C,'C',1.0,-1.3),(D,'D',0.3,-1.6)):
    ax.text(P[0]+dx, P[1]+dy, lab, fontsize=11, color=INK, ha='center', va='center')
ax.text(A[0]+0.6, 6.0, '$h$', color=ACCENT, fontsize=11)
ax.text(3.4, -2.9, '$c\\cos B$', color=ACCENT, fontsize=9.5, ha='center')
ax.text(10.5, -2.9, '$b\\cos C$', color=ACCENT, fontsize=9.5, ha='center')
ax.text(2.6, 7.6, '$c$', color=MUTED, fontsize=10.5)
ax.text(11.4, 7.6, '$b$', color=MUTED, fontsize=10.5)
ax.set_aspect('equal'); ax.axis('off')
ax.set_xlim(-2.0, 15.5); ax.set_ylim(-4.6, 15.2)
ax = axs[1]
B2 = np.array([0.0,0.0]); C2 = np.array([13.0,0.0]); A2 = np.array([-4.0,9.0])
D2 = np.array([A2[0], 0.0])
ax.plot([A2[0],B2[0],C2[0],A2[0]], [A2[1],B2[1],C2[1],A2[1]], color=INK, lw=1.7)
ax.plot([A2[0],D2[0]], [A2[1],D2[1]], color=ACCENT, lw=1.4, ls='--')
ax.plot([D2[0],B2[0]], [0,0], color=ACCENT, lw=1.4, ls=':')
ax.plot([D2[0]+0.9,D2[0]+0.9,D2[0]],[0,0.9,0.9], color=MUTED, lw=0.9)
for P,lab,dx,dy in ((A2,'A',-0.4,1.4),(B2,'B',1.1,-1.5),(C2,'C',1.0,-1.5),(D2,'D',-0.4,-1.6)):
    ax.text(P[0]+dx, P[1]+dy, lab, fontsize=11, color=INK, ha='center', va='center')
ax.text(-2.4, -3.4, 'BD = -c cos B > 0', color='#d9534f', fontsize=8.6, ha='center')
ax.set_aspect('equal'); ax.axis('off')
ax.set_xlim(-6.5, 15.0); ax.set_ylim(-4.6, 15.2)
```

::: key Cosine law
$$ a^{2} = b^{2}+c^{2}-2bc\cos A,\qquad b^{2} = c^{2}+a^{2}-2ca\cos B,
\qquad c^{2} = a^{2}+b^{2}-2ab\cos C $$
Rearranged to give an angle from three sides:
$$ \cos A = \frac{b^{2}+c^{2}-a^{2}}{2bc},\qquad
\cos B = \frac{c^{2}+a^{2}-b^{2}}{2ca},\qquad
\cos C = \frac{a^{2}+b^{2}-c^{2}}{2ab} $$
:::

::: example 6.3 Three sides to an angle
**Problem.** In a triangle $a = 13$ cm, $b = 14$ cm, $c = 15$ cm. Find $A$ and
$\sin C$.

**Solution.**

$$ \cos A = \frac{b^{2}+c^{2}-a^{2}}{2bc} = \frac{196 + 225 - 169}{2 \times 14 \times 15}
 = \frac{252}{420} = \frac{3}{5} = 0.6 $$

so $A = \cos^{-1}0.6 = 53^{\circ}8'$ (to the nearest minute).

$$ \cos C = \frac{a^{2}+b^{2}-c^{2}}{2ab} = \frac{169+196-225}{2 \times 13 \times 14}
 = \frac{140}{364} = \frac{5}{13} $$

Since $C$ is an angle of a triangle, $\sin C > 0$, so

$$ \sin C = \sqrt{1 - \left(\tfrac{5}{13}\right)^{2}} = \sqrt{\tfrac{144}{169}}
 = \frac{12}{13} \quad (C = 67^{\circ}23') $$

**Check.** $B = 180^{\circ} - 53^{\circ}8' - 67^{\circ}23' = 59^{\circ}29'$, and
$\cos B = \frac{225+169-196}{2\times 15\times 13} = \frac{198}{390} = 0.5077$,
which does give $59^{\circ}29'$. ✓
:::

::: example 6.4 Two sides and the included angle
**Problem.** In triangle $ABC$, $b = 7$ cm, $c = 8$ cm and $A = 60^{\circ}$.
Find $a$.

**Solution.** The angle lies between the two known sides, so use the cosine law:

$$ a^{2} = b^{2}+c^{2}-2bc\cos A = 49 + 64 - 2(7)(8)\left(\tfrac{1}{2}\right)
 = 113 - 56 = 57 $$

$$ a = \sqrt{57} = 7.55\ \text{cm} $$

**Check.** $a$ lies between $|b-c| = 1$ and $b+c = 15$, and because
$A = 60^{\circ} < $ the other angles' likely sizes, $a$ is the middle side. ✓
:::

::: caution The sign of the cosine
$\cos A$ comes out **negative** exactly when $a^{2} > b^{2} + c^{2}$, i.e. when
$A$ is obtuse. Do not "lose" the minus sign: $\cos A = -0.5$ gives
$A = 120^{\circ}$, not $60^{\circ}$. At most one angle of a triangle can be
obtuse, and it is the one facing the longest side.
:::

## 6.3 Tangent law

Two sides and the angle between them leave the other two angles unknown. The
cosine law can find them one at a time; the tangent law (also called
**Napier's analogy**) finds them together, and needs only logarithm tables —
which is why it was invented.

::: derivation Tangent law
Start from the sine law in the form $a = 2R\sin A$, $b = 2R\sin B$:

$$ \frac{a-b}{a+b} = \frac{2R(\sin A - \sin B)}{2R(\sin A + \sin B)}
 = \frac{\sin A - \sin B}{\sin A + \sin B} $$

Apply the sum-to-product formulae
$\sin A - \sin B = 2\cos\frac{A+B}{2}\sin\frac{A-B}{2}$ and
$\sin A + \sin B = 2\sin\frac{A+B}{2}\cos\frac{A-B}{2}$:

$$ \frac{a-b}{a+b}
= \frac{2\cos\frac{A+B}{2}\sin\frac{A-B}{2}}{2\sin\frac{A+B}{2}\cos\frac{A-B}{2}}
= \cot\frac{A+B}{2}\,\tan\frac{A-B}{2} $$

Finally $A + B = 180^{\circ} - C$, so
$\frac{A+B}{2} = 90^{\circ} - \frac{C}{2}$ and
$\cot\frac{A+B}{2} = \tan\frac{C}{2}$. Therefore

$$ \tan\frac{A-B}{2} = \frac{a-b}{a+b}\cot\frac{C}{2} $$
:::

::: key Tangent law (Napier's analogy)
$$ \tan\frac{A-B}{2} = \frac{a-b}{a+b}\cot\frac{C}{2},\qquad
\tan\frac{B-C}{2} = \frac{b-c}{b+c}\cot\frac{A}{2},\qquad
\tan\frac{C-A}{2} = \frac{c-a}{c+a}\cot\frac{B}{2} $$
Given $a$, $b$ and $C$ it gives $\frac{A-B}{2}$; and $\frac{A+B}{2}
= 90^{\circ}-\frac{C}{2}$ is already known. Add and subtract to get $A$ and $B$.
:::

::: example 6.5 Two sides and the included angle, by the tangent law
**Problem.** In triangle $ABC$, $a = 9$, $b = 7$ and $C = 60^{\circ}$. Find $A$,
$B$ and $c$.

**Solution.** Half the known sum first:

$$ \frac{A+B}{2} = 90^{\circ} - \frac{C}{2} = 90^{\circ} - 30^{\circ} = 60^{\circ} $$

Now the tangent law, with $\cot 30^{\circ} = \sqrt{3}$:

$$ \tan\frac{A-B}{2} = \frac{a-b}{a+b}\cot\frac{C}{2}
 = \frac{9-7}{9+7}\sqrt{3} = \frac{2}{16}(1.7321) = 0.2165 $$

$$ \frac{A-B}{2} = \tan^{-1}0.2165 = 12^{\circ}13' $$

Add and subtract the two half-quantities:

$$ A = 60^{\circ} + 12^{\circ}13' = 72^{\circ}13',\qquad
   B = 60^{\circ} - 12^{\circ}13' = 47^{\circ}47' $$

For $c$, the cosine law: $c^{2} = 81 + 49 - 2(9)(7)\left(\frac12\right) = 67$, so
$c = \sqrt{67} = 8.19$.

**Check.** $A+B+C = 72^{\circ}13' + 47^{\circ}47' + 60^{\circ} = 180^{\circ}$ ✓,
and the largest side $a = 9$ faces the largest angle $A$. ✓
:::

## 6.4 Projection laws

Look again at the altitude figure. The base $BC$ is cut by the foot $D$ into two
pieces, and each piece is the **projection** of one of the other sides onto $BC$.

::: derivation Projection laws
With $AD \perp BC$: in right triangle $ABD$, $BD = c\cos B$; in right triangle
$ACD$, $DC = b\cos C$. Since $D$ lies between $B$ and $C$,

$$ a = BD + DC = c\cos B + b\cos C $$

If $B$ is obtuse, $D$ lies outside on the far side of $B$, so
$a = DC - DB = b\cos C - c\cos(180^{\circ}-B) = b\cos C + c\cos B$ again —
the formula is unchanged.

Purely algebraically, from the cosine law,

$$ b\cos C + c\cos B = b\cdot\frac{a^{2}+b^{2}-c^{2}}{2ab}
 + c\cdot\frac{c^{2}+a^{2}-b^{2}}{2ca}
 = \frac{(a^{2}+b^{2}-c^{2}) + (a^{2}+c^{2}-b^{2})}{2a} = \frac{2a^{2}}{2a} = a $$
:::

::: key Projection laws
$$ a = b\cos C + c\cos B,\qquad b = c\cos A + a\cos C,\qquad
   c = a\cos B + b\cos A $$
Each side equals the sum of the other two, each multiplied by the cosine of the
angle it is next to. These are the fastest tool for identities in which sides
and cosines are mixed.
:::

::: example 6.6 A projection identity
**Problem.** In any triangle prove that $a(b\cos C - c\cos B) = b^{2}-c^{2}$.

**Solution.** Replace both cosines using the cosine law:

$$ b\cos C = b\cdot\frac{a^{2}+b^{2}-c^{2}}{2ab} = \frac{a^{2}+b^{2}-c^{2}}{2a},
\qquad
c\cos B = c\cdot\frac{c^{2}+a^{2}-b^{2}}{2ca} = \frac{a^{2}+c^{2}-b^{2}}{2a} $$

Subtract:

$$ b\cos C - c\cos B
= \frac{(a^{2}+b^{2}-c^{2}) - (a^{2}+c^{2}-b^{2})}{2a}
= \frac{2b^{2}-2c^{2}}{2a} = \frac{b^{2}-c^{2}}{a} $$

Multiply by $a$: $a(b\cos C - c\cos B) = b^{2}-c^{2}$. ∎

**Check with the running triangle** ($a=13$, $b=14$, $c=15$):
$b\cos C = 14 \times \frac{5}{13} = 5.385$ and
$c\cos B = 15 \times 0.5077 = 7.615$, so
$13(5.385 - 7.615) = 13(-2.231) = -29$, while
$b^{2}-c^{2} = 196-225 = -29$. ✓
:::

::: example 6.7 A harder projection identity
**Problem.** Prove that $b\cos B + c\cos C = a\cos(B-C)$.

**Solution.** Turn the sides into sines with $b = 2R\sin B$, $c = 2R\sin C$:

$$ b\cos B + c\cos C = 2R(\sin B\cos B + \sin C\cos C)
 = R(\sin 2B + \sin 2C) $$

using $2\sin\theta\cos\theta = \sin 2\theta$. By the sum-to-product formula,

$$ \sin 2B + \sin 2C = 2\sin(B+C)\cos(B-C) $$

But $B + C = 180^{\circ} - A$, so $\sin(B+C) = \sin A$. Hence

$$ b\cos B + c\cos C = 2R\sin A\cos(B-C) = a\cos(B-C) $$

since $2R\sin A = a$. ∎
:::

## 6.5 Half angle laws

The cosine law gives $\cos A$, but many results (areas, radii, Heron's formula)
need $\sin\frac{A}{2}$, $\cos\frac{A}{2}$ or $\tan\frac{A}{2}$. All three come
out of the cosine law in one step each, and all three are written with the
semi-perimeter $s = \frac{a+b+c}{2}$. Note the useful rewritings
$b+c-a = 2(s-a)$, $c+a-b = 2(s-b)$, $a+b-c = 2(s-c)$.

::: derivation The half angle formulae
**Sine.** Use $1 - \cos A = 2\sin^{2}\frac{A}{2}$ and the cosine law:

$$ 2\sin^{2}\frac{A}{2} = 1 - \frac{b^{2}+c^{2}-a^{2}}{2bc}
 = \frac{2bc - b^{2} - c^{2} + a^{2}}{2bc} = \frac{a^{2}-(b-c)^{2}}{2bc} $$

Factorise the difference of squares:
$a^{2}-(b-c)^{2} = (a+b-c)(a-b+c) = 2(s-c)\cdot 2(s-b)$, so

$$ \sin^{2}\frac{A}{2} = \frac{(s-b)(s-c)}{bc}
\quad\Longrightarrow\quad
\sin\frac{A}{2} = \sqrt{\frac{(s-b)(s-c)}{bc}} $$

the positive root, because $0 < \frac{A}{2} < 90^{\circ}$.

**Cosine.** Use $1 + \cos A = 2\cos^{2}\frac{A}{2}$:

$$ 2\cos^{2}\frac{A}{2} = 1 + \frac{b^{2}+c^{2}-a^{2}}{2bc}
 = \frac{(b+c)^{2}-a^{2}}{2bc} = \frac{2s\cdot 2(s-a)}{2bc} $$

$$ \cos\frac{A}{2} = \sqrt{\frac{s(s-a)}{bc}} $$

**Tangent.** Divide the two results; the $bc$ cancels:

$$ \tan\frac{A}{2} = \sqrt{\frac{(s-b)(s-c)}{s(s-a)}} $$
:::

::: key Half angle laws
$$ \sin\frac{A}{2} = \sqrt{\frac{(s-b)(s-c)}{bc}},\qquad
\cos\frac{A}{2} = \sqrt{\frac{s(s-a)}{bc}},\qquad
\tan\frac{A}{2} = \sqrt{\frac{(s-b)(s-c)}{s(s-a)}} $$
with $s = \frac{a+b+c}{2}$; cycle $a \to b \to c \to a$ and $A \to B \to C \to A$
for the others. Every root is positive, because each half-angle is acute.
:::

::: caution $s - a$, not $a - s$
$s$ is **half** the perimeter, so $s - a$, $s - b$, $s - c$ are all positive and
add up to $s$. Writing $s = a+b+c$ is the single commonest slip in this unit and
it wrecks every number that follows. Always check: $(s-a)+(s-b)+(s-c) = s$.
:::

::: example 6.8 Half angles of the running triangle
**Problem.** For $a = 13$, $b = 14$, $c = 15$ find $\sin\frac{A}{2}$,
$\cos\frac{A}{2}$ and $\tan\frac{A}{2}$.

**Solution.** $s = \frac{13+14+15}{2} = 21$, so $s-a = 8$, $s-b = 7$, $s-c = 6$
(and $8+7+6 = 21 = s$ ✓).

$$ \sin\frac{A}{2} = \sqrt{\frac{(s-b)(s-c)}{bc}} = \sqrt{\frac{7 \times 6}{14 \times 15}}
 = \sqrt{\frac{42}{210}} = \sqrt{\frac{1}{5}} = 0.4472 $$

$$ \cos\frac{A}{2} = \sqrt{\frac{s(s-a)}{bc}} = \sqrt{\frac{21 \times 8}{210}}
 = \sqrt{\frac{4}{5}} = 0.8944 $$

$$ \tan\frac{A}{2} = \sqrt{\frac{(s-b)(s-c)}{s(s-a)}} = \sqrt{\frac{42}{168}}
 = \sqrt{\frac{1}{4}} = \frac{1}{2} $$

**Check.** $\frac{A}{2} = \tan^{-1}0.5 = 26^{\circ}34'$, so
$A = 53^{\circ}8'$ — the same $A$ as in Example 6.3. ✓
:::

::: example 6.9 All three angles from three sides
**Problem.** Find the angles of the triangle with sides $a = 3$, $b = 5$,
$c = 7$ cm.

**Solution.** $s = \frac{3+5+7}{2} = \frac{15}{2} = 7.5$, so
$s-a = 4.5$, $s-b = 2.5$, $s-c = 0.5$.

$$ \tan\frac{A}{2} = \sqrt{\frac{(s-b)(s-c)}{s(s-a)}}
= \sqrt{\frac{2.5 \times 0.5}{7.5 \times 4.5}} = \sqrt{\frac{1.25}{33.75}}
= \sqrt{0.03704} = 0.1925 $$

$\frac{A}{2} = 10^{\circ}54'$, so $A = 21^{\circ}47'$.

$$ \tan\frac{C}{2} = \sqrt{\frac{(s-a)(s-b)}{s(s-c)}}
= \sqrt{\frac{4.5 \times 2.5}{7.5 \times 0.5}} = \sqrt{3} = 1.7321 $$

$\frac{C}{2} = 60^{\circ}$, so $C = 120^{\circ}$.

$$ B = 180^{\circ} - 21^{\circ}47' - 120^{\circ} = 38^{\circ}13' $$

**Check.** $C$ is obtuse, and indeed $c^{2} = 49 > a^{2}+b^{2} = 34$. ✓
:::

::: tip Which law for which data
| You are given | Use |
|---|---|
| two angles and any side (AAS/ASA) | sine law |
| two sides and an opposite angle (SSA) | sine law — but watch for two answers |
| two sides and the included angle (SAS) | cosine law, or tangent law |
| three sides (SSS) | cosine law, or half angle law for the angles |
:::

## 6.6 Area of a triangle, and the radii $R$, $r$, $r_1$

::: derivation Area and Heron's formula
The altitude from $A$ has length $h = b\sin C$, and the base is $a$, so

$$ \Delta = \tfrac{1}{2}\,(\text{base})(\text{height}) = \tfrac{1}{2}ab\sin C $$

Now write $\sin A = 2\sin\frac{A}{2}\cos\frac{A}{2}$ and put in the half-angle
formulae:

$$ \sin A = 2\sqrt{\frac{(s-b)(s-c)}{bc}}\sqrt{\frac{s(s-a)}{bc}}
 = \frac{2}{bc}\sqrt{s(s-a)(s-b)(s-c)} $$

Therefore

$$ \Delta = \tfrac{1}{2}bc\sin A = \sqrt{s(s-a)(s-b)(s-c)} $$

which is **Heron's formula** — the area from the three sides alone.
:::

::: key Area, and the three kinds of radius
$$ \Delta = \tfrac{1}{2}bc\sin A = \tfrac{1}{2}ca\sin B = \tfrac{1}{2}ab\sin C
 = \sqrt{s(s-a)(s-b)(s-c)} $$
$$ R = \frac{abc}{4\Delta},\qquad r = \frac{\Delta}{s} = (s-a)\tan\frac{A}{2},
\qquad r_1 = \frac{\Delta}{s-a} = s\tan\frac{A}{2} $$
$R$ is the **circumradius** (circle through the vertices), $r$ the **inradius**
(circle touching all three sides from inside) and $r_1$, $r_2$, $r_3$ the
**exradii** — the circles touching one side and the other two produced.
:::

```figure caption="Circumcircle (radius $R$, centre $O$) and incircle (radius $r$, centre $I$) of the triangle $13$, $14$, $15$. The incircle cuts the sides into the lengths $s-a$, $s-b$, $s-c$."
import numpy as np
fig, ax = plt.subplots(figsize=(4.4,3.4))
B = np.array([0.0,0.0]); C = np.array([13.0,0.0]); A = np.array([7.6154,12.9231])
O = np.array([6.5,4.875]); R = 8.125
I = np.array([7.0,4.0]); r = 4.0
t = np.linspace(0,2*np.pi,400)
ax.plot(O[0]+R*np.cos(t), O[1]+R*np.sin(t), color=GRID, lw=1.3)
ax.plot(I[0]+r*np.cos(t), I[1]+r*np.sin(t), color=ACCENT, lw=1.3)
ax.plot([A[0],B[0],C[0],A[0]],[A[1],B[1],C[1],A[1]], color=INK, lw=1.7)
ax.plot([O[0],I[0]],[O[1],I[1]], ls='none')
ax.plot([O[0]],[O[1]],'o',color=MUTED,ms=4); ax.plot([I[0]],[I[1]],'o',color=ACCENT,ms=4)
ax.plot([O[0],O[0]+R*np.cos(np.radians(125))],[O[1],O[1]+R*np.sin(np.radians(125))],
        color=MUTED, lw=1.0, ls=':')
ax.plot([I[0],I[0]],[I[1],0.0], color=ACCENT, lw=1.0, ls=':')
ax.text(2.0, 9.6, '$R$', color=MUTED, fontsize=11)
ax.text(I[0]+0.35, 1.7, '$r$', color=ACCENT, fontsize=11)
ax.text(O[0]-2.0, O[1]-0.1, '$O$', color=MUTED, fontsize=10.5)
ax.text(I[0]+0.3, I[1]+0.5, '$I$', color=ACCENT, fontsize=10.5)
for P,lab,dx,dy in ((A,'A',0,1.0),(B,'B',-1.1,-0.9),(C,'C',1.0,-0.9)):
    ax.text(P[0]+dx,P[1]+dy,lab,fontsize=11,color=INK,ha='center',va='center')
ax.text(3.5,-1.5,'$s-b = 7$',color=ACCENT,fontsize=8.8,ha='center')
ax.text(10.4,-1.5,'$s-c = 6$',color=ACCENT,fontsize=8.8,ha='center')
ax.set_aspect('equal'); ax.axis('off')
ax.set_xlim(-2.6, 16.2); ax.set_ylim(-3.0, 14.4)
```

```figure caption="The three excircles of the same triangle: $r_1 = 10.5$ touches $BC$ itself, $r_2 = 12$ touches $CA$, $r_3 = 14$ touches $AB$, each from outside."
import numpy as np
fig, ax = plt.subplots(figsize=(4.7,4.3))
B = np.array([0.0,0.0]); C = np.array([13.0,0.0]); A = np.array([7.6154,12.9231])
t = np.linspace(0,2*np.pi,500)
ex = [((6.0,-10.5), 10.5, '$r_1$', (6.0,-19.0)),
      ((21.0,12.0), 12.0, '$r_2$', (26.5,20.5)),
      ((-8.0,14.0), 14.0, '$r_3$', (-15.0,24.0))]
cols = [ACCENT, SERIES[2], SERIES[3]]
for (ctr, rr, lab, lp), col in zip(ex, cols):
    ax.plot(ctr[0]+rr*np.cos(t), ctr[1]+rr*np.sin(t), color=col, lw=1.2)
    ax.plot([ctr[0]],[ctr[1]],'o',color=col,ms=4)
    ax.text(lp[0], lp[1], lab, color=col, fontsize=12, ha='center', va='center')
def full(P,Q):
    d = (Q-P)/np.hypot(*(Q-P))
    ax.plot([P[0]-30*d[0], P[0]+40*d[0]], [P[1]-30*d[1], P[1]+40*d[1]],
            color=GRID, lw=0.9)
full(B,C); full(A,B); full(A,C)
ax.plot(7.0+4.0*np.cos(t), 4.0+4.0*np.sin(t), color=MUTED, lw=1.0, ls='--')
ax.text(7.0, 4.0, '$r$', color=MUTED, fontsize=10, ha='center', va='center')
ax.plot([A[0],B[0],C[0],A[0]],[A[1],B[1],C[1],A[1]], color=INK, lw=2.0)
for P,lab,dx,dy in ((A,'A',0.5,2.0),(B,'B',-2.2,-1.5),(C,'C',2.0,-1.5)):
    ax.text(P[0]+dx,P[1]+dy,lab,fontsize=11,color=INK,ha='center',va='center')
ax.set_aspect('equal'); ax.axis('off')
ax.set_xlim(-24.0, 35.0); ax.set_ylim(-22.0, 29.0)
```

::: example 6.10 Area two ways
**Problem.** Find the area of the triangle $a = 13$, $b = 14$, $c = 15$, and
hence $\sin B$.

**Solution.** By Heron, with $s = 21$:

$$ \Delta = \sqrt{s(s-a)(s-b)(s-c)} = \sqrt{21 \times 8 \times 7 \times 6}
 = \sqrt{7056} = 84\ \text{cm}^{2} $$

Now use $\Delta = \frac{1}{2}ca\sin B$ backwards:

$$ \sin B = \frac{2\Delta}{ca} = \frac{2 \times 84}{15 \times 13}
 = \frac{168}{195} = 0.8615 $$

**Check.** $B = \sin^{-1}0.8615 = 59^{\circ}29'$, matching Example 6.3. ✓
:::

::: example 6.11 The five radii
**Problem.** For the same triangle find $R$, $r$, $r_1$, $r_2$, $r_3$.

**Solution.** From Example 6.10, $\Delta = 84$, $s = 21$, $s-a = 8$, $s-b = 7$,
$s-c = 6$.

$$ R = \frac{abc}{4\Delta} = \frac{13 \times 14 \times 15}{4 \times 84}
 = \frac{2730}{336} = 8.125\ \text{cm} $$

$$ r = \frac{\Delta}{s} = \frac{84}{21} = 4\ \text{cm} $$

$$ r_1 = \frac{\Delta}{s-a} = \frac{84}{8} = 10.5,\qquad
   r_2 = \frac{\Delta}{s-b} = \frac{84}{7} = 12,\qquad
   r_3 = \frac{\Delta}{s-c} = \frac{84}{6} = 14\ \text{cm} $$

**Check.** $r = (s-a)\tan\frac{A}{2} = 8 \times \frac12 = 4$ ✓ and
$r_1 = s\tan\frac{A}{2} = 21 \times \frac12 = 10.5$ ✓ (Example 6.8).
:::

::: example 6.12 $r = 4R\sin\frac{A}{2}\sin\frac{B}{2}\sin\frac{C}{2}$
**Problem.** Prove it.

**Solution.** Two ingredients. First, from $\Delta = \frac{1}{2}ab\sin C$ with
$a = 2R\sin A$, $b = 2R\sin B$:

$$ \Delta = \tfrac{1}{2}(2R\sin A)(2R\sin B)\sin C = 2R^{2}\sin A\sin B\sin C $$

Second, $s = \frac{a+b+c}{2} = R(\sin A + \sin B + \sin C)$, and the Grade 11
identity $\sin A + \sin B + \sin C = 4\cos\frac{A}{2}\cos\frac{B}{2}\cos\frac{C}{2}$
for angles of a triangle gives
$s = 4R\cos\frac{A}{2}\cos\frac{B}{2}\cos\frac{C}{2}$. Now divide, writing each
$\sin A$ as $2\sin\frac{A}{2}\cos\frac{A}{2}$:

$$ r = \frac{\Delta}{s}
 = \frac{2R^{2}\cdot 8\sin\frac{A}{2}\cos\frac{A}{2}\sin\frac{B}{2}\cos\frac{B}{2}
 \sin\frac{C}{2}\cos\frac{C}{2}}{4R\cos\frac{A}{2}\cos\frac{B}{2}\cos\frac{C}{2}}
 = 4R\sin\frac{A}{2}\sin\frac{B}{2}\sin\frac{C}{2} $$

**Check** ($13$, $14$, $15$): $4(8.125)(0.4472)(0.4961)(0.5547) = 4.00 = r$ ✓.
:::

::: example 6.13 $r_1 + r_2 + r_3 - r = 4R$
**Problem.** Prove it.

**Solution.** Write every radius as $\Delta$ over something:

$$ r_1 + r_2 + r_3 - r
= \Delta\left[\frac{1}{s-a} + \frac{1}{s-b} + \frac{1}{s-c} - \frac{1}{s}\right] $$

Pair the brackets cleverly. Since $(s-a)+(s-b) = 2s-a-b = c$,

$$ \frac{1}{s-a}+\frac{1}{s-b} = \frac{c}{(s-a)(s-b)},\qquad
\frac{1}{s-c}-\frac{1}{s} = \frac{s-(s-c)}{s(s-c)} = \frac{c}{s(s-c)} $$

Add these two:

$$ c\,\frac{s(s-c) + (s-a)(s-b)}{s(s-a)(s-b)(s-c)} = c\,\frac{s(s-c)+(s-a)(s-b)}{\Delta^{2}} $$

The numerator simplifies: $s(s-c)+(s-a)(s-b) = 2s^{2} - s(a+b+c) + ab
= 2s^{2}-2s^{2}+ab = ab$. Hence

$$ r_1+r_2+r_3-r = \Delta\cdot\frac{abc}{\Delta^{2}} = \frac{abc}{\Delta}
= 4\cdot\frac{abc}{4\Delta} = 4R $$

**Check:** $10.5 + 12 + 14 - 4 = 32.5 = 4 \times 8.125$ ✓.
:::

## Chapter summary

- Standard notation: $a$ faces $A$, $s = \frac{a+b+c}{2}$, area $\Delta$.
- **Sine law:** $\frac{a}{\sin A} = \frac{b}{\sin B} = \frac{c}{\sin C} = 2R$,
  so $a = 2R\sin A$ — the switch from sides to sines.
- **Cosine law:** $a^{2} = b^{2}+c^{2}-2bc\cos A$, i.e.
  $\cos A = \frac{b^{2}+c^{2}-a^{2}}{2bc}$; negative cosine means an obtuse angle.
- **Tangent law:** $\tan\frac{A-B}{2} = \frac{a-b}{a+b}\cot\frac{C}{2}$, with
  $\frac{A+B}{2} = 90^{\circ}-\frac{C}{2}$.
- **Projection laws:** $a = b\cos C + c\cos B$, and its two cyclic partners.
- **Half angle laws:** $\sin\frac{A}{2} = \sqrt{\frac{(s-b)(s-c)}{bc}}$,
  $\cos\frac{A}{2} = \sqrt{\frac{s(s-a)}{bc}}$,
  $\tan\frac{A}{2} = \sqrt{\frac{(s-b)(s-c)}{s(s-a)}}$.
- **Area:** $\Delta = \frac12 ab\sin C = \sqrt{s(s-a)(s-b)(s-c)}$ (Heron).
- **Radii:** $R = \frac{abc}{4\Delta}$, $r = \frac{\Delta}{s} = 4R\sin\frac{A}{2}
  \sin\frac{B}{2}\sin\frac{C}{2}$, $r_1 = \frac{\Delta}{s-a} = s\tan\frac{A}{2}$,
  and $r_1+r_2+r_3-r = 4R$.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. In any triangle $\dfrac{a}{\sin A}$ equals <span class="marks">[1]</span>
   (a) $R$ (b) $2R$ (c) $\frac{R}{2}$ (d) $4R$
2. $\cos A$ equals <span class="marks">[1]</span>
   (a) $\frac{b^{2}+c^{2}-a^{2}}{2bc}$ (b) $\frac{a^{2}+b^{2}-c^{2}}{2bc}$ (c) $\frac{b^{2}+c^{2}-a^{2}}{2ab}$ (d) $\frac{a^{2}-b^{2}-c^{2}}{2bc}$
3. $b\cos C + c\cos B$ equals <span class="marks">[1]</span>
   (a) $a$ (b) $b$ (c) $c$ (d) $2s$
4. $\tan\frac{A}{2}$ equals <span class="marks">[1]</span>
   (a) $\sqrt{\frac{s(s-a)}{(s-b)(s-c)}}$ (b) $\sqrt{\frac{(s-b)(s-c)}{s(s-a)}}$ (c) $\sqrt{\frac{(s-b)(s-c)}{bc}}$ (d) $\sqrt{\frac{s(s-a)}{bc}}$
5. The area of the triangle with sides $13$, $14$, $15$ cm is <span class="marks">[1]</span>
   (a) $84$ cm² (b) $42$ cm² (c) $168$ cm² (d) $21$ cm²
6. If $r = 4$ and $s = 21$ then $\Delta$ is <span class="marks">[1]</span>
   (a) $21$ (b) $84$ (c) $5.25$ (d) $336$

::: note Answers to Group A
**1.** (b) — the common ratio is the diameter of the circumcircle.

**2.** (a) — rearrange $a^{2} = b^{2}+c^{2}-2bc\cos A$; the denominator carries
the two sides **enclosing** $A$.

**3.** (a) — the projection law: the two projections onto $BC$ add to $BC = a$.

**4.** (b) — (c) and (d) are $\sin\frac{A}{2}$ and $\cos\frac{A}{2}$; their ratio
is (b).

**5.** (a) — $s = 21$ and $\sqrt{21 \times 8 \times 7 \times 6} = 84$.

**6.** (b) — $\Delta = rs = 4 \times 21 = 84$.
:::

**Group B — Short answer (5 marks each)**

1. In triangle $ABC$, $b = \sqrt{3}$ cm, $c = 1$ cm and $A = 30^{\circ}$. Find
   $a$, $B$ and $C$. <span class="marks">[5]</span>
2. Find the greatest angle of the triangle whose sides are $7$ cm, $8$ cm and
   $9$ cm. <span class="marks">[5]</span>
3. In any triangle $ABC$ prove that $a(b\cos C - c\cos B) = b^{2}-c^{2}$ and
   deduce that $c(a\cos B - b\cos A) = a^{2}-b^{2}$. <span class="marks">[5]</span>
4. In a triangle $a = 9$ cm, $b = 7$ cm and $C = 60^{\circ}$. Using the tangent
   law find $A$ and $B$, and then find $c$. <span class="marks">[5]</span>
5. If $a = 13$, $b = 14$, $c = 15$, find $\tan\frac{A}{2}$, $\tan\frac{B}{2}$,
   $\tan\frac{C}{2}$ and verify that
   $\tan\frac{A}{2}\tan\frac{B}{2} + \tan\frac{B}{2}\tan\frac{C}{2}
   + \tan\frac{C}{2}\tan\frac{A}{2} = 1$. <span class="marks">[5]</span>
6. For the triangle with sides $5$, $12$, $13$ cm find $\Delta$, $r$, $R$,
   $r_1$, $r_2$, $r_3$, and verify $r_1+r_2+r_3-r = 4R$. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Two sides and the included angle, so the cosine law:
$a^{2} = b^{2}+c^{2}-2bc\cos A = 3 + 1 - 2(\sqrt{3})(1)\left(\frac{\sqrt{3}}{2}\right)
= 4 - 3 = 1$, so $a = 1$ cm.
Then by the sine law $\sin B = \frac{b\sin A}{a}
= \frac{\sqrt{3} \times \frac12}{1} = \frac{\sqrt{3}}{2}$, giving $B = 60^{\circ}$ or
$120^{\circ}$. Since $b = \sqrt{3}$ is the **largest** side, $B$ is the largest
angle, so $B = 120^{\circ}$ and $C = 180^{\circ}-30^{\circ}-120^{\circ}
= 30^{\circ}$. (The triangle is isosceles with $a = c = 1$, which agrees with
$A = C = 30^{\circ}$.)

**2.** The greatest angle faces the greatest side, so it is the angle $C$
opposite $9$ cm. With $a = 7$, $b = 8$, $c = 9$:
$$ \cos C = \frac{a^{2}+b^{2}-c^{2}}{2ab} = \frac{49+64-81}{2 \times 7 \times 8}
= \frac{32}{112} = \frac{2}{7} = 0.2857 $$
so $C = \cos^{-1}0.2857 = 73^{\circ}24'$.

**3.** By the cosine law $b\cos C = \frac{a^{2}+b^{2}-c^{2}}{2a}$ and
$c\cos B = \frac{a^{2}+c^{2}-b^{2}}{2a}$. Subtracting,
$b\cos C - c\cos B = \frac{2b^{2}-2c^{2}}{2a} = \frac{b^{2}-c^{2}}{a}$, so
$a(b\cos C - c\cos B) = b^{2}-c^{2}$. The second result is the same statement
with the letters advanced one step, $a \to c$, $b \to a$, $c \to b$ (and
$A \to C$, $B \to A$, $C \to B$): $c(a\cos B - b\cos A) = a^{2}-b^{2}$.

**4.** $\frac{A+B}{2} = 90^{\circ}-\frac{C}{2} = 60^{\circ}$. By the tangent law
$$ \tan\frac{A-B}{2} = \frac{a-b}{a+b}\cot\frac{C}{2}
= \frac{2}{16}\cot 30^{\circ} = \frac{1.7321}{8} = 0.2165 $$
so $\frac{A-B}{2} = 12^{\circ}13'$. Then $A = 60^{\circ}+12^{\circ}13'
= 72^{\circ}13'$ and $B = 60^{\circ}-12^{\circ}13' = 47^{\circ}47'$.
By the cosine law $c^{2} = 81+49-2(9)(7)\left(\frac12\right) = 67$, so
$c = 8.19$ cm.

**5.** $s = 21$, $s-a = 8$, $s-b = 7$, $s-c = 6$.
$\tan\frac{A}{2} = \sqrt{\frac{7 \times 6}{21 \times 8}} = \sqrt{\frac14}
= \frac12$;
$\tan\frac{B}{2} = \sqrt{\frac{8 \times 6}{21 \times 7}} = \sqrt{\frac{48}{147}}
= \frac47$;
$\tan\frac{C}{2} = \sqrt{\frac{8 \times 7}{21 \times 6}} = \sqrt{\frac{56}{126}}
= \frac23$.
Then $\frac12 \cdot \frac47 + \frac47 \cdot \frac23 + \frac23 \cdot \frac12
= \frac27 + \frac{8}{21} + \frac13 = \frac{6+8+7}{21} = 1$ ✓.

**6.** $s = \frac{5+12+13}{2} = 15$; $s-a = 10$, $s-b = 3$, $s-c = 2$.
$\Delta = \sqrt{15 \times 10 \times 3 \times 2} = \sqrt{900} = 30$ cm²
(it is right-angled, and $\frac12 \times 5 \times 12 = 30$ ✓).
$r = \frac{\Delta}{s} = \frac{30}{15} = 2$ cm;
$R = \frac{abc}{4\Delta} = \frac{5 \times 12 \times 13}{120} = 6.5$ cm
(half the hypotenuse, as expected for a right angle).
$r_1 = \frac{30}{10} = 3$, $r_2 = \frac{30}{3} = 10$, $r_3 = \frac{30}{2} = 15$ cm.
Finally $r_1+r_2+r_3-r = 3+10+15-2 = 26 = 4 \times 6.5 = 4R$ ✓.
:::

**Group C — Long answer (8 marks each)**

1. State and prove the cosine law for a triangle. Hence find all three angles and
   the area of the triangle whose sides are $4$ cm, $5$ cm and $6$ cm.
   <span class="marks">[8]</span>
2. Prove that $\sin\frac{A}{2} = \sqrt{\frac{(s-b)(s-c)}{bc}}$ and
   $\cos\frac{A}{2} = \sqrt{\frac{s(s-a)}{bc}}$, and deduce Heron's formula
   $\Delta = \sqrt{s(s-a)(s-b)(s-c)}$. Use them on the triangle with sides
   $5$, $6$, $7$ cm. <span class="marks">[8]</span>
3. Prove that $r = 4R\sin\frac{A}{2}\sin\frac{B}{2}\sin\frac{C}{2}$ and
   $r_1 = 4R\sin\frac{A}{2}\cos\frac{B}{2}\cos\frac{C}{2}$, and verify both for
   the triangle $13$, $14$, $15$. <span class="marks">[8]</span>

::: note Answers to Group C
**1.** *Statement:* $a^{2} = b^{2}+c^{2}-2bc\cos A$ (and cyclically).
*Proof:* drop $CD \perp AB$. Then $AD = b\cos A$, $CD = b\sin A$ and
$DB = c - b\cos A$. Pythagoras in $\triangle CDB$ gives
$a^{2} = b^{2}\sin^{2}A + (c-b\cos A)^{2}
= b^{2}\sin^{2}A + b^{2}\cos^{2}A + c^{2} - 2bc\cos A = b^{2}+c^{2}-2bc\cos A$.
(If $A$ is obtuse, $D$ lies outside $AB$, $\cos A < 0$, and the same algebra
holds with the signed length $AD$.)
*Application*, $a = 4$, $b = 5$, $c = 6$:
$$ \cos A = \frac{25+36-16}{2 \times 5 \times 6} = \frac{45}{60} = 0.75
\Rightarrow A = 41^{\circ}25' $$
$$ \cos B = \frac{16+36-25}{2 \times 4 \times 6} = \frac{27}{48} = 0.5625
\Rightarrow B = 55^{\circ}46' $$
$$ C = 180^{\circ} - 41^{\circ}25' - 55^{\circ}46' = 82^{\circ}49' $$
Area: $s = 7.5$, so
$\Delta = \sqrt{7.5 \times 3.5 \times 2.5 \times 1.5} = \sqrt{98.4375}
= 9.92$ cm² $\left(= \frac{15\sqrt{7}}{4}\right)$.
Check with $\frac12 bc\sin A = \frac12(5)(6)(0.6614) = 9.92$ ✓.

**2.** From the cosine law, $1-\cos A = \frac{2bc - b^{2}-c^{2}+a^{2}}{2bc}
= \frac{a^{2}-(b-c)^{2}}{2bc} = \frac{(a+b-c)(a-b+c)}{2bc}
= \frac{2(s-c)\cdot 2(s-b)}{2bc}$. Since $1-\cos A = 2\sin^{2}\frac{A}{2}$,
$\sin^{2}\frac{A}{2} = \frac{(s-b)(s-c)}{bc}$, and the half angle is acute so the
root is positive. Similarly $1+\cos A = \frac{(b+c)^{2}-a^{2}}{2bc}
= \frac{2s \cdot 2(s-a)}{2bc} = 2\cos^{2}\frac{A}{2}$, giving
$\cos\frac{A}{2} = \sqrt{\frac{s(s-a)}{bc}}$.
Then $\sin A = 2\sin\frac{A}{2}\cos\frac{A}{2}
= \frac{2}{bc}\sqrt{s(s-a)(s-b)(s-c)}$ and
$\Delta = \frac12 bc\sin A = \sqrt{s(s-a)(s-b)(s-c)}$.
*Application*, $a=5$, $b=6$, $c=7$: $s = 9$, $s-a = 4$, $s-b = 3$, $s-c = 2$.
$\Delta = \sqrt{9 \times 4 \times 3 \times 2} = \sqrt{216} = 6\sqrt{6}
= 14.70$ cm².
$\tan\frac{A}{2} = \sqrt{\frac{3 \times 2}{9 \times 4}} = \sqrt{\frac16}
= 0.4082 \Rightarrow A = 44^{\circ}25'$;
$\tan\frac{B}{2} = \sqrt{\frac{4 \times 2}{9 \times 3}} = 0.5443
\Rightarrow B = 57^{\circ}7'$;
$C = 180^{\circ}-44^{\circ}25'-57^{\circ}7' = 78^{\circ}28'$.

**3.** Using $a = 2R\sin A$ etc., $\Delta = \frac12 ab\sin C
= 2R^{2}\sin A\sin B\sin C$, and
$s = R(\sin A+\sin B+\sin C) = 4R\cos\frac{A}{2}\cos\frac{B}{2}\cos\frac{C}{2}$.
Dividing and writing $\sin A = 2\sin\frac{A}{2}\cos\frac{A}{2}$ (and likewise for
$B$, $C$) cancels all three cosines:
$$ r = \frac{\Delta}{s} = 4R\sin\frac{A}{2}\sin\frac{B}{2}\sin\frac{C}{2} $$
For $r_1$ we need $s-a$. Now
$s - a = R(\sin B + \sin C - \sin A)$, and
$\sin B+\sin C = 2\cos\frac{A}{2}\cos\frac{B-C}{2}$ while
$\sin A = 2\sin\frac{A}{2}\cos\frac{A}{2} = 2\cos\frac{A}{2}\cos\frac{B+C}{2}$,
so
$$ s-a = 2R\cos\tfrac{A}{2}\left[\cos\tfrac{B-C}{2}-\cos\tfrac{B+C}{2}\right]
= 4R\cos\tfrac{A}{2}\sin\tfrac{B}{2}\sin\tfrac{C}{2} $$
Hence
$$ r_1 = \frac{\Delta}{s-a}
= \frac{2R^{2}\sin A\sin B\sin C}{4R\cos\frac{A}{2}\sin\frac{B}{2}\sin\frac{C}{2}}
= 4R\sin\tfrac{A}{2}\cos\tfrac{B}{2}\cos\tfrac{C}{2} $$
*Verification* ($13$, $14$, $15$; $R = 8.125$): $\sin\frac{A}{2} = 0.4472$,
$\sin\frac{B}{2} = 0.4961$, $\sin\frac{C}{2} = 0.5547$, $\cos\frac{B}{2} = 0.8682$,
$\cos\frac{C}{2} = 0.8321$.
$4R\sin\frac{A}{2}\sin\frac{B}{2}\sin\frac{C}{2} = 32.5 \times 0.1231 = 4.00 = r$ ✓
and $4R\sin\frac{A}{2}\cos\frac{B}{2}\cos\frac{C}{2} = 32.5 \times 0.3231
= 10.5 = r_1$ ✓.
:::
