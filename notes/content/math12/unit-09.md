---
subject: Mathematics
grade: 12
unit: 9
title: Product of Vectors
hours: 12
area: Vectors
---

Grade 11 gave you everything about vectors except how to multiply them. This unit
supplies the two products, and they are different animals. The **scalar product**
returns a number measuring how much two vectors point the same way — the tool for
angles, perpendicularity and work. The **vector product** returns a third vector,
at right angles to both, whose length is an area — the tool for areas,
perpendicular directions and moments. With both in hand, most of the trigonometry
of Units 6 and 7 can be proved again in two lines.

::: key What the exam wants
Group A asks you to **evaluate**: a dot product, a cross product, an angle, an
area. Group B asks you to **apply**: an angle, a projection, a unit vector
perpendicular to two given vectors, the area of a triangle, the moment of a force.
Group C asks you to **prove**: the cosine law, the sine law, the projection law,
$\cos(A \pm B)$, $\sin(A \pm B)$ and short geometry theorems. Learn those as
proofs — every line of the working carries a mark.
:::

## 9.1 Scalar (dot) product; angle between two vectors

Unit 14 of Grade 11 stated the scalar product and used it. We now start again from
the definition and prove the results, as a Grade 12 paper requires.

::: definition Scalar (dot) product
Let $\vec{a}$ and $\vec{b}$ be two non-zero vectors and let $\theta$ be the angle
between them, measured with both vectors drawn from a common point, so that
$0^{\circ} \leq \theta \leq 180^{\circ}$. Their **scalar product** is

$$ \vec{a}\cdot\vec{b} = |\vec{a}|\,|\vec{b}|\cos\theta $$

The answer is a **scalar**. If either vector is $\vec{0}$ the product is $0$.
:::

Two points are worth saying out loud. First, $\theta$ is the angle **between the
vectors when they start from the same point**: given $\vec{AB}$ and $\vec{BC}$,
the angle between them is *not* the interior angle $B$, so move one vector until
both tails meet. Second, since $\cos\theta$ changes sign at $90^{\circ}$, the sign
of $\vec{a}\cdot\vec{b}$ alone tells you whether the angle is acute, right or
obtuse.

Applying the definition to $\hat{i}$, $\hat{j}$, $\hat{k}$ gives a table worth
memorising: a base vector makes $0^{\circ}$ with itself, $90^{\circ}$ with the
other two.

| $\cdot$ | $\hat{i}$ | $\hat{j}$ | $\hat{k}$ |
|---|---|---|---|
| $\hat{i}$ | $1$ | $0$ | $0$ |
| $\hat{j}$ | $0$ | $1$ | $0$ |
| $\hat{k}$ | $0$ | $0$ | $1$ |

So $\hat{i}\cdot\hat{i} = \hat{j}\cdot\hat{j} = \hat{k}\cdot\hat{k} = 1$ (each is a
unit vector, $\cos 0^{\circ} = 1$) and
$\hat{i}\cdot\hat{j} = \hat{j}\cdot\hat{k} = \hat{k}\cdot\hat{i} = 0$
(perpendicular, $\cos 90^{\circ} = 0$).

### The component form, and why it agrees with the definition

Almost every calculation uses components rather than
$|\vec{a}||\vec{b}|\cos\theta$, so the two forms must be shown to agree. The
bridge is the cosine law of Unit 6.

::: derivation The component form of the scalar product
We start from the geometric definition $\vec{a}\cdot\vec{b} = |\vec{a}||\vec{b}|\cos\theta$
and finish with a formula that needs no angle at all, only the components.

**Setting up.** Draw both vectors from one point $O$: let $\vec{OA} = \vec{a}$ and
$\vec{OB} = \vec{b}$, with

$$ \vec{a} = a_1\hat{i} + a_2\hat{j} + a_3\hat{k}, \quad \vec{b} = b_1\hat{i} + b_2\hat{j} + b_3\hat{k} $$

Let $\theta = \angle AOB$. The sides meeting at $O$ are $OA = |\vec{a}|$ and
$OB = |\vec{b}|$, and the third side is $\vec{AB} = \vec{b} - \vec{a}$ (head
minus tail), so $AB = |\vec{b} - \vec{a}|$.

**Step 1 — apply the cosine law to triangle $OAB$.** The angle $\theta$ sits
between the two known sides, and $AB$ is opposite it:

$$ AB^{2} = OA^{2} + OB^{2} - 2\,OA \cdot OB\cos\theta $$

In vector language that is

$$ |\vec{b} - \vec{a}|^{2} = |\vec{a}|^{2} + |\vec{b}|^{2} - 2|\vec{a}||\vec{b}|\cos\theta $$

**Step 2 — write the left-hand side in components.** The vector
$\vec{b} - \vec{a}$ has components $b_1 - a_1$, $b_2 - a_2$, $b_3 - a_3$, so

$$ |\vec{b}-\vec{a}|^{2} = (b_1-a_1)^{2} + (b_2-a_2)^{2} + (b_3-a_3)^{2} $$

**Step 3 — expand every bracket.** Each square gives three terms:

$$ = (a_1^{2}+a_2^{2}+a_3^{2}) + (b_1^{2}+b_2^{2}+b_3^{2}) - 2(a_1b_1+a_2b_2+a_3b_3) $$

**Step 4 — recognise the first two brackets.** They are exactly the squared
magnitudes:

$$ |\vec{b}-\vec{a}|^{2} = |\vec{a}|^{2} + |\vec{b}|^{2} - 2(a_1b_1+a_2b_2+a_3b_3) $$

**Step 5 — compare with Step 1.** The two expressions for
$|\vec{b}-\vec{a}|^{2}$ must be equal. Cancel $|\vec{a}|^{2}+|\vec{b}|^{2}$ from
both sides and divide by $-2$:

$$ |\vec{a}||\vec{b}|\cos\theta = a_1b_1 + a_2b_2 + a_3b_3 $$

**Result.** The left side is $\vec{a}\cdot\vec{b}$, so

$$ \vec{a}\cdot\vec{b} = a_1b_1 + a_2b_2 + a_3b_3 $$

**What it means.** Multiply matching components and add. No angle, no square
roots, no drawing — which is why this is the form you compute with.

**Conditions used.** Only that $\hat{i},\hat{j},\hat{k}$ are mutually
perpendicular unit vectors, so that the distance formula
$|\vec{r}|^{2} = x^{2}+y^{2}+z^{2}$ holds. For plane vectors drop the third
component.
:::

::: tip The examiner is looking for
Four marks, four steps: the cosine law for triangle $OAB$ with
$\vec{AB} = \vec{b}-\vec{a}$; $|\vec{b}-\vec{a}|^{2}$ expanded in components; the
magnitudes identified; the comparison. Never skip the expansion — that is the step
being tested.
:::

### The angle between two vectors

Reading the two forms as one equation and solving for $\cos\theta$ gives the
single most used formula of the unit.

::: key Angle, and the test for perpendicularity
$$ \cos\theta = \frac{\vec{a}\cdot\vec{b}}{|\vec{a}|\,|\vec{b}|} = \frac{a_1b_1+a_2b_2+a_3b_3}{\sqrt{a_1^{2}+a_2^{2}+a_3^{2}}\;\sqrt{b_1^{2}+b_2^{2}+b_3^{2}}} $$

For non-zero $\vec{a}$ and $\vec{b}$,

$$ \vec{a} \perp \vec{b} \; \Leftrightarrow \; \theta = 90^{\circ} \; \Leftrightarrow \; \vec{a}\cdot\vec{b} = 0 $$

and $\vec{a}$, $\vec{b}$ are parallel exactly when $\vec{a}\cdot\vec{b} = \pm|\vec{a}||\vec{b}|$
($+$ for the same sense, $-$ for opposite senses).
:::

::: example Worked example 9.1
**Problem.** Find the angle between $\vec{a} = 2\hat{i}+2\hat{j}-\hat{k}$ and
$\vec{b} = 6\hat{i}-3\hat{j}+2\hat{k}$.

**Solution.** Take the scalar product in components:

$$ \vec{a}\cdot\vec{b} = (2)(6) + (2)(-3) + (-1)(2) = 12 - 6 - 2 = 4 $$

Now the two magnitudes:

$$ |\vec{a}| = \sqrt{4+4+1} = \sqrt{9} = 3, \qquad |\vec{b}| = \sqrt{36+9+4} = \sqrt{49} = 7 $$

$$ \cos\theta = \frac{4}{(3)(7)} = \frac{4}{21} = 0.1905 $$

$$ \theta = \cos^{-1}(0.1905) = 79.02^{\circ} $$

The scalar product is positive, so the angle had to come out acute. ✔
:::

::: example Worked example 9.2
**Problem.** Show that the triangle with vertices $A(2,1,1)$, $B(2,2,3)$ and
$C(4,4,2)$ is right-angled, and find its other two angles.

**Solution.** The angle of the triangle at $B$ is the angle between the vectors
$\vec{BA}$ and $\vec{BC}$ — both must start at $B$:

$$ \vec{BA} = \vec{a}-\vec{b} = -\hat{j}-2\hat{k}, \qquad \vec{BC} = \vec{c}-\vec{b} = 2\hat{i}+2\hat{j}-\hat{k} $$

$$ \vec{BA}\cdot\vec{BC} = (0)(2) + (-1)(2) + (-2)(-1) = 0 - 2 + 2 = 0 $$

A zero scalar product between two non-zero vectors means they are perpendicular,
so $\angle B = 90^{\circ}$ and the triangle is right-angled at $B$.

For the angle at $A$, use $\vec{AB} = \hat{j}+2\hat{k}$ and
$\vec{AC} = 2\hat{i}+3\hat{j}+\hat{k}$:

$$ \vec{AB}\cdot\vec{AC} = 0 + 3 + 2 = 5, \quad |\vec{AB}| = \sqrt{5}, \quad |\vec{AC}| = \sqrt{14} $$

$$ \cos A = \frac{5}{\sqrt{5}\sqrt{14}} = \frac{5}{\sqrt{70}} = 0.5976 $$

so $A = 53.30^{\circ}$. The third angle needs no new work:
$C = 180^{\circ} - 90^{\circ} - 53.30^{\circ} = 36.70^{\circ}$.

Check by Pythagoras: $AB^{2}+BC^{2} = 5 + 9 = 14 = AC^{2}$. ✔
:::

::: caution The angle at a vertex needs both tails at that vertex
For the angle at $A$ use $\vec{AB}$ and $\vec{AC}$, never $\vec{BA}$ and
$\vec{AC}$: reversing one vector reverses the sign and hands you $180^{\circ}-A$.
In Worked example 9.2, $\vec{BA}\cdot\vec{AC} = -5$ gives $126.70^{\circ}$, the
supplement of the correct $53.30^{\circ}$. Draw the arrows before you multiply.
:::

## 9.2 Geometric interpretation and properties of scalar product

### The scalar product is a length times a shadow

Group $|\vec{a}||\vec{b}|\cos\theta$ as $|\vec{a}| \times \left(|\vec{b}|\cos\theta\right)$.
The bracket is the **shadow** $\vec{b}$ casts on the line of $\vec{a}$ when light
falls at right angles to it. Drop a perpendicular from the head of $\vec{b}$ onto
that line, meeting it at $M$: then $OM$ is the **projection** of $\vec{b}$ on
$\vec{a}$.

::: definition Projection of one vector on another
The **scalar projection** (or component) of $\vec{b}$ along $\vec{a}$ is

$$ |\vec{b}|\cos\theta = \frac{\vec{a}\cdot\vec{b}}{|\vec{a}|} = \vec{b}\cdot\hat{a} $$

The **vector projection** of $\vec{b}$ on $\vec{a}$ is that number times the unit
vector $\hat{a}$:

$$ \vec{b}_{\parallel} = \left(\frac{\vec{a}\cdot\vec{b}}{|\vec{a}|^{2}}\right)\vec{a} $$

The scalar projection is signed: negative when $\theta$ is obtuse, because the
shadow then falls on the *backward* extension of $\vec{a}$.
:::

```figure caption="The scalar product as a length times a shadow, $\vec{a}\cdot\vec{b} = |\vec{a}|\,(|\vec{b}|\cos\theta)$. (a) Acute $\theta$: the shadow $OM$ falls along $\vec{a}$, so the projection and $\vec{a}\cdot\vec{b}$ are positive. (b) Obtuse $\theta$: the foot $M$ lands on the backward extension of $\vec{a}$, so both are negative."
import numpy as np, matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 2, figsize=(5.2, 2.7))
def arrow(ax, p, q, c=INK, lw=2.0, ls='-', ms=13):
    ax.annotate('', xy=q, xytext=p, arrowprops=dict(arrowstyle='-|>', color=c, lw=lw,
                linestyle=ls, shrinkA=0, shrinkB=0, mutation_scale=ms))
O = np.array([0.0, 0.0])
a = np.array([2.9, 0.0])
for k, ax in enumerate(axes):
    b = np.array([1.75, 1.60]) if k == 0 else np.array([-1.35, 1.60])
    foot = np.array([b[0], 0.0])
    # line of a, extended backwards in panel (b)
    ax.plot([-2.0 if k else -0.55, 3.35], [0, 0], color=GRID, lw=1.0,
            ls=(0, (4, 3)), zorder=0)
    arrow(ax, O, a, ACCENT)
    arrow(ax, O, b, SERIES[2])
    ax.plot([b[0], foot[0]], [b[1], foot[1]], color=MUTED, lw=1.0, ls=(0, (3, 2)))
    # right-angle mark at the foot
    s = 0.17
    sgn = 1.0 if k == 0 else -1.0
    ax.plot([foot[0] - sgn * s, foot[0] - sgn * s, foot[0]], [0, s, s],
            color=MUTED, lw=0.8)
    # projection bar
    col = SERIES[1] if k == 0 else SERIES[4]
    ax.plot([0, foot[0]], [-0.40, -0.40], color=col, lw=3.0, solid_capstyle='butt')
    ax.plot([foot[0], foot[0]], [-0.46, 0.0], color=MUTED, lw=0.7, ls=':')
    ax.plot([0, 0], [-0.46, 0.0], color=MUTED, lw=0.7, ls=':')
    # angle arc
    th = np.linspace(0, np.arctan2(b[1], b[0]), 60)
    ax.plot(0.60 * np.cos(th), 0.60 * np.sin(th), color=INK, lw=0.9)
    ax.annotate('$\\theta$', (0.72, 0.26) if k == 0 else (-0.30, 0.74),
                color=INK, fontsize=10.5)
    ax.annotate('$\\vec{a}$', (2.45, 0.0), textcoords='offset points',
                xytext=(0, 7), color=ACCENT, fontsize=11)
    ax.annotate('$\\vec{b}$', b / 2, textcoords='offset points',
                xytext=(9, -1) if k == 0 else (-13, -10), color=SERIES[2], fontsize=11)
    ax.annotate('$M$', foot, textcoords='offset points',
                xytext=(4, 6) if k == 0 else (-11, 6), color=INK, fontsize=9.5)
    ax.plot([foot[0]], [0], 'o', color=INK, ms=3.2)
    ax.plot([0], [0], 'o', color=INK, ms=3.6)
    ax.annotate('$O$', O, textcoords='offset points',
                xytext=(-5, 7) if k else (-11, 4), color=INK, fontsize=9.5)
    if k == 0:
        ax.annotate('$OM = |\\vec{b}|\\cos\\theta > 0$', (foot[0] / 2, -0.40),
                    textcoords='offset points', xytext=(0, -15), color=col,
                    fontsize=9.3, ha='center')
        ax.set_title('(a) acute angle', fontsize=9.5)
        ax.set_xlim(-1.40, 4.20); ax.set_ylim(-1.15, 2.15)
    else:
        ax.annotate('$OM = |\\vec{b}|\\cos\\theta < 0$', (foot[0] / 2, -0.40),
                    textcoords='offset points', xytext=(-6, -15), color=col,
                    fontsize=9.3, ha='center')
        ax.set_title('(b) obtuse angle', fontsize=9.5)
        ax.set_xlim(-2.13, 3.47); ax.set_ylim(-1.15, 2.15)
    ax.set_aspect('equal'); ax.axis('off')
fig.subplots_adjust(wspace=0.05)
```

::: example Worked example 9.3
**Problem.** For $\vec{a} = \hat{i}+3\hat{j}+2\hat{k}$ and
$\vec{b} = 3\hat{i}+2\hat{j}+6\hat{k}$ find (a) the scalar projection of $\vec{a}$
on $\vec{b}$, (b) the vector projection of $\vec{a}$ on $\vec{b}$, (c) the angle
between them.

**Solution.** One scalar product serves all three parts:

$$ \vec{a}\cdot\vec{b} = (1)(3) + (3)(2) + (2)(6) = 3 + 6 + 12 = 21 $$

$$ |\vec{a}| = \sqrt{1+9+4} = \sqrt{14}, \qquad |\vec{b}| = \sqrt{9+4+36} = \sqrt{49} = 7 $$

(a) Divide by the magnitude of the vector you are projecting **onto**:

$$ \text{projection of } \vec{a} \text{ on } \vec{b} = \frac{\vec{a}\cdot\vec{b}}{|\vec{b}|} = \frac{21}{7} = 3 \text{ units} $$

(b) Multiply that length by the unit vector $\hat{b} = \vec{b}/7$:

$$ \vec{a}_{\parallel} = 3\left(\frac{3\hat{i}+2\hat{j}+6\hat{k}}{7}\right) = \frac{9}{7}\hat{i} + \frac{6}{7}\hat{j} + \frac{18}{7}\hat{k} $$

(c) For the angle, divide by **both** magnitudes:

$$ \cos\theta = \frac{21}{\sqrt{14}\times 7} = \frac{3}{\sqrt{14}} = 0.8018 $$

so $\theta = 36.70^{\circ}$.
:::

::: caution Projection on $\vec{b}$ divides by $|\vec{b}|$ only
Dividing by $|\vec{a}||\vec{b}|$ gives $\cos\theta$, a pure number; dividing by
$|\vec{b}|$ alone gives a **length**. Remember the word order: "projection **of**
$\vec{a}$ **on** $\vec{b}$" divides by the magnitude of the vector after "on".
:::

### Algebraic properties, with proofs

::: key Properties of the scalar product
For all vectors $\vec{a},\vec{b},\vec{c}$ and every scalar $m$:

1. **Commutative:** $\vec{a}\cdot\vec{b} = \vec{b}\cdot\vec{a}$
2. **Square:** $\vec{a}\cdot\vec{a} = |\vec{a}|^{2}$, often written $\vec{a}^{2}$
3. **Scalars pull out:** $(m\vec{a})\cdot\vec{b} = m(\vec{a}\cdot\vec{b}) = \vec{a}\cdot(m\vec{b})$
4. **Distributive:** $\vec{a}\cdot(\vec{b}+\vec{c}) = \vec{a}\cdot\vec{b} + \vec{a}\cdot\vec{c}$
5. **Perpendicularity:** $\vec{a}\cdot\vec{b} = 0 \Leftrightarrow \vec{a} \perp \vec{b}$ (non-zero vectors)
6. **Expansion:** $|\vec{a}\pm\vec{b}|^{2} = |\vec{a}|^{2} \pm 2\,\vec{a}\cdot\vec{b} + |\vec{b}|^{2}$
7. **Bound:** $|\vec{a}\cdot\vec{b}| \leq |\vec{a}||\vec{b}|$, with equality only when the vectors are parallel
:::

The proofs are short, and NEB asks for them.

**1. Commutative.** The angle between $\vec{a}$ and $\vec{b}$ is the same angle as
between $\vec{b}$ and $\vec{a}$, and multiplication of numbers is commutative:

$$ \vec{a}\cdot\vec{b} = |\vec{a}||\vec{b}|\cos\theta = |\vec{b}||\vec{a}|\cos\theta = \vec{b}\cdot\vec{a} $$

**2. Square of a vector.** A vector makes an angle $0^{\circ}$ with itself, and
$\cos 0^{\circ} = 1$:

$$ \vec{a}\cdot\vec{a} = |\vec{a}||\vec{a}|\cos 0^{\circ} = |\vec{a}|^{2} $$

This is the identity that turns every length question into a scalar product
question. In components it reads $a_1^{2}+a_2^{2}+a_3^{2}$, the distance formula.

**3. Scalars.** Take $m > 0$ first. Multiplying $\vec{a}$ by $m$ multiplies its
length by $m$ and leaves its direction alone, so $\theta$ does not change:

$$ (m\vec{a})\cdot\vec{b} = |m\vec{a}||\vec{b}|\cos\theta = m|\vec{a}||\vec{b}|\cos\theta = m(\vec{a}\cdot\vec{b}) $$

If $m < 0$, then $|m\vec{a}| = -m|\vec{a}|$ and the direction of $m\vec{a}$ is
reversed, so the angle becomes $180^{\circ}-\theta$ and the cosine changes sign:

$$ (m\vec{a})\cdot\vec{b} = (-m|\vec{a}|)|\vec{b}|(-\cos\theta) = m(\vec{a}\cdot\vec{b}) $$

Both signs give the same rule, and $m = 0$ makes both sides zero.

**5. Perpendicularity.** If $\vec{a}$ and $\vec{b}$ are non-zero then
$|\vec{a}||\vec{b}| \ne 0$, so $\vec{a}\cdot\vec{b} = 0$ forces $\cos\theta = 0$,
i.e. $\theta = 90^{\circ}$. Running the argument backwards,
$\theta = 90^{\circ}$ gives $\cos\theta = 0$ and the product vanishes.

**6. Expansion.** Use property 2 on $\vec{a}\pm\vec{b}$, then expand by
distributivity and collect the two middle terms with commutativity:

$$ |\vec{a}+\vec{b}|^{2} = (\vec{a}+\vec{b})\cdot(\vec{a}+\vec{b}) = \vec{a}\cdot\vec{a} + 2\,\vec{a}\cdot\vec{b} + \vec{b}\cdot\vec{b} $$

Replacing $\vec{b}$ by $-\vec{b}$ gives the minus version. These two lines do the
work in most Group B problems about $|\vec{a}+\vec{b}|$.

**7. Bound.** Since $-1 \leq \cos\theta \leq 1$,

$$ |\vec{a}\cdot\vec{b}| = |\vec{a}||\vec{b}|\,|\cos\theta| \leq |\vec{a}||\vec{b}| $$

and $|\cos\theta| = 1$ only for $\theta = 0^{\circ}$ or $180^{\circ}$, that is,
only for parallel vectors.

Property 4 is the one that needs a picture rather than algebra.

::: derivation The distributive law, $\vec{a}\cdot(\vec{b}+\vec{c}) = \vec{a}\cdot\vec{b} + \vec{a}\cdot\vec{c}$
We start from the fact that projections add along a line, and finish with the rule
that lets you multiply out brackets of vectors.

**Setting up.** Let $\hat{a}$ be the unit vector along $\vec{a}$. Draw
$\vec{OP} = \vec{b}$ and $\vec{PQ} = \vec{c}$ head to tail, so
$\vec{OQ} = \vec{b}+\vec{c}$. Drop perpendiculars from $O$, $P$, $Q$ onto the
line through $O$ along $\hat{a}$; call the feet $O$, $P'$, $Q'$.

**Step 1 — name the three shadows.** By definition $OP' = \vec{b}\cdot\hat{a}$,
$P'Q' = \vec{c}\cdot\hat{a}$ and $OQ' = (\vec{b}+\vec{c})\cdot\hat{a}$, each a
**signed** length along $\hat{a}$.

**Step 2 — signed lengths on one line add.** The points $O$, $P'$, $Q'$ all lie on
one straight line, and for signed lengths on a line

$$ OQ' = OP' + P'Q' $$

whatever order the three points fall in — the only geometric fact used, and the
reason projections carry a sign.

**Step 3 — substitute the names from Step 1.**

$$ (\vec{b}+\vec{c})\cdot\hat{a} = \vec{b}\cdot\hat{a} + \vec{c}\cdot\hat{a} $$

**Step 4 — restore the length of $\vec{a}$.** Multiply through by the number
$|\vec{a}|$ and use $\vec{a} = |\vec{a}|\hat{a}$ with property 3:

$$ (\vec{b}+\vec{c})\cdot\vec{a} = \vec{b}\cdot\vec{a} + \vec{c}\cdot\vec{a} $$

**Step 5 — turn each product round** using the commutative law:

$$ \vec{a}\cdot(\vec{b}+\vec{c}) = \vec{a}\cdot\vec{b} + \vec{a}\cdot\vec{c} $$

**Result.** Brackets of vectors may be multiplied out exactly as in ordinary
algebra, provided every product is a dot product.

**What it means.** This is the property that makes vector proofs possible:
$(\vec{a}+\vec{b})\cdot(\vec{a}-\vec{b})$, $|\vec{a}+\vec{b}|^{2}$ and every
expansion in §9.3 depend on it.

**Conditions.** None beyond the definition of projection; the law holds for all
vectors, including the zero vector.
:::

::: example Worked example 9.4
**Problem.** If $|\vec{a}| = 3$, $|\vec{b}| = 4$ and $|\vec{a}+\vec{b}| = 5$, find
$\vec{a}\cdot\vec{b}$, the angle between the vectors, and $|\vec{a}-\vec{b}|$.

**Solution.** Square the given magnitude of the sum and expand (property 6):

$$ |\vec{a}+\vec{b}|^{2} = |\vec{a}|^{2} + 2\,\vec{a}\cdot\vec{b} + |\vec{b}|^{2} $$

$$ 25 = 9 + 2\,\vec{a}\cdot\vec{b} + 16 \; \Longrightarrow \; 2\,\vec{a}\cdot\vec{b} = 0 $$

So $\vec{a}\cdot\vec{b} = 0$, and since neither vector is zero the angle is
$\theta = 90^{\circ}$.

For the difference, use the minus version of the same expansion:

$$ |\vec{a}-\vec{b}|^{2} = 9 - 0 + 16 = 25 \; \Longrightarrow \; |\vec{a}-\vec{b}| = 5 $$

The two diagonals are equal, as they must be for a rectangle — and $3,4,5$ is
exactly the Pythagorean triple you should have expected.
:::

### Work done by a force

The scalar product was invented for this.

::: definition Work as a scalar product
If a constant force $\vec{F}$ acts on a body while its displacement is $\vec{d}$,
the **work done** is

$$ W = \vec{F}\cdot\vec{d} = |\vec{F}||\vec{d}|\cos\theta $$

where $\theta$ is the angle between force and displacement. Work is a scalar, in
joules (J) for $\vec{F}$ in newtons and $\vec{d}$ in metres.
:::

Only the part of the force **along** the displacement does work — the projection
idea of §9.2. A force at right angles to the motion, such as the string tension on
a whirling stone, does zero work because $\cos 90^{\circ} = 0$.

::: example Worked example 9.5
**Problem.** A force $\vec{F} = 4\hat{i}+\hat{j}-3\hat{k}$ newton moves a particle
from $A(1,-2,3)$ to $B(5,-1,2)$, distances in metres. Find the work done and the
angle between the force and the displacement.

**Solution.** The displacement is head minus tail:

$$ \vec{d} = \vec{AB} = (5-1)\hat{i} + (-1+2)\hat{j} + (2-3)\hat{k} = 4\hat{i}+\hat{j}-\hat{k} $$

$$ W = \vec{F}\cdot\vec{d} = (4)(4) + (1)(1) + (-3)(-1) = 16 + 1 + 3 = 20 \text{ J} $$

For the angle, $|\vec{F}| = \sqrt{16+1+9} = \sqrt{26}$ and
$|\vec{d}| = \sqrt{16+1+1} = \sqrt{18}$, so

$$ \cos\theta = \frac{20}{\sqrt{26}\sqrt{18}} = \frac{20}{21.633} = 0.9245 $$

giving $\theta = 22.38^{\circ}$. The work is positive because the force has a
component along the motion.
:::

::: caution You cannot cancel a vector
From $\vec{a}\cdot\vec{b} = \vec{a}\cdot\vec{c}$ it does **not** follow that
$\vec{b} = \vec{c}$, only that $\vec{a}\perp(\vec{b}-\vec{c})$. There is no
division by a vector, so never write $\vec{b} = (\vec{a}\cdot\vec{c})/\vec{a}$.
Nor does $\vec{a}\cdot\vec{b} = 0$ force either vector to be $\vec{0}$.
:::

## 9.3 Applications of scalar product in geometry and trigonometry

The method never changes: **name the sides as vectors, write the one relation they
satisfy, and dot both sides with something useful.**

For a triangle $ABC$ the standard naming is

$$ \vec{BC} = \vec{a}, \qquad \vec{CA} = \vec{b}, \qquad \vec{AB} = \vec{c} $$

taken **in order round the triangle**, so that by the triangle law

$$ \vec{a} + \vec{b} + \vec{c} = \vec{0} $$

and the side lengths are $a = |\vec{a}| = BC$, $b = |\vec{b}| = CA$,
$c = |\vec{c}| = AB$, as in Unit 6.

Care is needed with the angles. $\vec{b}$ and $\vec{c}$ do **not** make the angle
$A$: $\vec{c} = \vec{AB}$ leaves $A$ while $\vec{b} = \vec{CA}$ *arrives* at $A$.
Reversing $\vec{b}$ gives $\vec{AC}$, which does. So the angle between $\vec{b}$
and $\vec{c}$ is $180^{\circ}-A$, and

$$ \vec{b}\cdot\vec{c} = bc\cos(180^{\circ}-A) = -\,bc\cos A $$

The same argument at the other two vertices gives
$\vec{c}\cdot\vec{a} = -ca\cos B$ and $\vec{a}\cdot\vec{b} = -ab\cos C$. Those three
lines are the engine of everything in this section.

```figure caption="(a) The sides of a triangle as vectors taken in order: $\vec{a}+\vec{b}+\vec{c} = \vec{0}$. The arrow $\vec{b}$ arrives at $A$ while $\vec{c}$ leaves it, which is why the angle between them is $180^{\circ}-A$. (b) Two unit vectors at angles $A$ and $B$ to the $x$-axis: the angle between them is $A-B$, and their components are the sines and cosines of $A$ and $B$."
import numpy as np, matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 2, figsize=(5.2, 2.6))
def arrow(ax, p, q, c=INK, lw=2.0, ls='-', ms=13):
    ax.annotate('', xy=q, xytext=p, arrowprops=dict(arrowstyle='-|>', color=c, lw=lw,
                linestyle=ls, shrinkA=0, shrinkB=0, mutation_scale=ms))
def arc(ax, cen, r, t0, t1, c=INK):
    while t1 - t0 > np.pi: t1 -= 2 * np.pi
    while t1 - t0 < -np.pi: t1 += 2 * np.pi
    t = np.linspace(t0, t1, 60)
    ax.plot(cen[0] + r * np.cos(t), cen[1] + r * np.sin(t), color=c, lw=0.9)
    return (t0 + t1) / 2

# ---- (a) triangle with sides as vectors
ax = axes[0]
Av = np.array([0.15, 1.95]); Bv = np.array([-0.85, 0.0]); Cv = np.array([2.65, 0.15])
arrow(ax, Bv, Cv, ACCENT)          # a = BC
arrow(ax, Cv, Av, SERIES[2])       # b = CA
arrow(ax, Av, Bv, SERIES[1])       # c = AB
ax.annotate('$\\vec{a}$', (Bv + Cv) / 2, textcoords='offset points', xytext=(-2, -14),
            color=ACCENT, fontsize=11, ha='center')
ax.annotate('$\\vec{b}$', (Cv + Av) / 2, textcoords='offset points', xytext=(12, 3),
            color=SERIES[2], fontsize=11, ha='center')
ax.annotate('$\\vec{c}$', (Av + Bv) / 2, textcoords='offset points', xytext=(-13, 0),
            color=SERIES[1], fontsize=11, ha='center')
for P, lab, off in [(Av, '$A$', (0, 9)), (Bv, '$B$', (-12, -6)), (Cv, '$C$', (7, -5))]:
    ax.plot([P[0]], [P[1]], 'o', color=INK, ms=3.6)
    ax.annotate(lab, P, textcoords='offset points', xytext=off, color=INK, fontsize=9.8)
def ang_at(V, P, Q):
    return np.arctan2(P[1] - V[1], P[0] - V[0]), np.arctan2(Q[1] - V[1], Q[0] - V[0])
for V, P1, P2, lab, rr in [(Av, Bv, Cv, '$A$', 0.66), (Bv, Cv, Av, '$B$', 0.70),
                           (Cv, Av, Bv, '$C$', 0.70)]:
    tm = arc(ax, V, 0.46, *ang_at(V, P1, P2))
    ax.annotate(lab, V + rr * np.array([np.cos(tm), np.sin(tm)]),
                color=MUTED, fontsize=9.2, ha='center', va='center')
ax.set_title('(a) sides taken in order', fontsize=9.5)
ax.set_xlim(-1.5, 3.3); ax.set_ylim(-0.75, 2.6)

# ---- (b) two unit vectors at angles A and B
ax = axes[1]
O = np.array([0.0, 0.0]); Adeg, Bdeg = 66.0, 24.0
A_, B_ = np.radians(Adeg), np.radians(Bdeg)
P = np.array([np.cos(A_), np.sin(A_)]); Q = np.array([np.cos(B_), np.sin(B_)])
t = np.linspace(0, np.pi / 2, 80)
ax.plot(np.cos(t), np.sin(t), color=GRID, lw=1.1)
ax.plot([0, 1.24], [0, 0], color=MUTED, lw=0.9)
ax.plot([0, 0], [0, 1.18], color=MUTED, lw=0.9)
arrow(ax, O, P, SERIES[2], 2.0); arrow(ax, O, Q, ACCENT, 2.0)
arc(ax, O, 0.36, 0, B_, INK); arc(ax, O, 0.52, B_, A_, SERIES[1])
ax.annotate('$B$', 0.30 * np.array([np.cos(B_ / 2), np.sin(B_ / 2)]),
            textcoords='offset points', xytext=(7, -3), color=INK, fontsize=9.5)
ax.annotate('$A-B$', 0.78 * np.array([np.cos((A_ + B_) / 2), np.sin((A_ + B_) / 2)]),
            color=SERIES[1], fontsize=9.3, ha='center', va='center')
ax.annotate('$P(\\cos A,\\ \\sin A)$', P, textcoords='offset points', xytext=(-2, 8),
            color=SERIES[2], fontsize=9.0, ha='left')
ax.annotate('$Q(\\cos B,\\ \\sin B)$', Q, textcoords='offset points', xytext=(6, -2),
            color=ACCENT, fontsize=9.0, ha='left')
ax.annotate('$O$', O, textcoords='offset points', xytext=(-11, -4), color=INK, fontsize=9.5)
ax.annotate('unit circle', (0.05, 1.18), color=MUTED, fontsize=8.6, ha='left')
ax.set_title('(b) angles measured from $Ox$', fontsize=9.5)
ax.set_xlim(-0.30, 2.15); ax.set_ylim(-0.30, 1.55)
for ax in axes:
    ax.set_aspect('equal'); ax.axis('off')
fig.subplots_adjust(wspace=0.06)
```

::: derivation The cosine law, $a^{2} = b^{2}+c^{2}-2bc\cos A$
We start from $\vec{a}+\vec{b}+\vec{c} = \vec{0}$ and reach the cosine law of Unit 6
in four lines.

**Setting up.** In triangle $ABC$ put $\vec{a} = \vec{BC}$, $\vec{b} = \vec{CA}$,
$\vec{c} = \vec{AB}$, so that $\vec{a}+\vec{b}+\vec{c} = \vec{0}$.

**Step 1 — isolate the side you want.** Move the other two vectors across:

$$ \vec{a} = -(\vec{b}+\vec{c}) $$

**Step 2 — square by dotting with itself.** Property 2 says
$\vec{a}\cdot\vec{a} = |\vec{a}|^{2} = a^{2}$, and the two minus signs cancel:

$$ a^{2} = (\vec{b}+\vec{c})\cdot(\vec{b}+\vec{c}) $$

**Step 3 — multiply out**, using the distributive and commutative laws:

$$ a^{2} = \vec{b}\cdot\vec{b} + 2\,\vec{b}\cdot\vec{c} + \vec{c}\cdot\vec{c} = b^{2} + c^{2} + 2\,\vec{b}\cdot\vec{c} $$

**Step 4 — put in the angle.** As shown above,
$\vec{b}\cdot\vec{c} = -bc\cos A$, so

$$ a^{2} = b^{2} + c^{2} - 2bc\cos A $$

**Result.** The cosine law. The other two forms follow by starting from
$\vec{b} = -(\vec{c}+\vec{a})$ and $\vec{c} = -(\vec{a}+\vec{b})$:

$$ b^{2} = c^{2}+a^{2}-2ca\cos B, \qquad c^{2} = a^{2}+b^{2}-2ab\cos C $$

**What it means.** The extra term $-2bc\cos A$ is the correction to Pythagoras
when the angle at $A$ is not a right angle. Put $A = 90^{\circ}$ and it vanishes.

**Conditions.** None. Only the triangle law and the algebra of the scalar product
are used, so obtuse triangles are covered too (there $\cos A < 0$).
:::

::: note Is this argument circular?
In §9.1 the cosine law proved the component form; here the scalar product proves
the cosine law. That is not circular: this proof uses only the **definition**
$\vec{a}\cdot\vec{b} = |\vec{a}||\vec{b}|\cos\theta$ and the **distributive
law**, and §9.2 proved the distributive law from projections alone.
:::

::: derivation The projection law, $a = b\cos C + c\cos B$
We start from the same relation and this time dot it with one of the sides.

**Setting up.** Again $\vec{a}+\vec{b}+\vec{c} = \vec{0}$ in triangle $ABC$.

**Step 1 — dot the whole relation with $\vec{a}$.** Anything dotted with $\vec{0}$
is $0$:

$$ \vec{a}\cdot(\vec{a}+\vec{b}+\vec{c}) = \vec{a}\cdot\vec{0} = 0 $$

**Step 2 — distribute.**

$$ \vec{a}\cdot\vec{a} + \vec{a}\cdot\vec{b} + \vec{a}\cdot\vec{c} = 0 $$

**Step 3 — name each term.** The first is $a^{2}$; the other two use the angle
rules above, $\vec{a}\cdot\vec{b} = -ab\cos C$ and $\vec{c}\cdot\vec{a} = -ca\cos B$:

$$ a^{2} - ab\cos C - ca\cos B = 0 $$

**Step 4 — divide by $a$** (a side length, so $a \ne 0$):

$$ a = b\cos C + c\cos B $$

**Result.** With the other two choices of dotting vector,

$$ b = c\cos A + a\cos C, \qquad c = a\cos B + b\cos A $$

**What it means.** Each side is the sum of the projections of the other two onto
it — the shadow picture of §9.2, read along $BC$.

**Conditions.** Only that $ABC$ is a genuine triangle.
:::

::: tip The examiner is looking for
Both proofs start with the *same* first line, $\vec{a}+\vec{b}+\vec{c}=\vec{0}$;
the cosine law then **squares**, the projection law **dots with one side**. State
$\vec{b}\cdot\vec{c} = -bc\cos A$ and say why the minus sign is there — that line
is usually worth a mark.
:::

### Geometry theorems in three lines

```figure caption="(a) A rhombus: $|\vec{a}| = |\vec{b}|$, and the diagonals $\vec{a}+\vec{b}$ and $\vec{a}-\vec{b}$ satisfy $(\vec{a}+\vec{b})\cdot(\vec{a}-\vec{b}) = 0$, so they cross at right angles. (b) The angle in a semicircle: with $O$ the centre, $\vec{OA} = -\vec{r}$ and $\vec{OB} = \vec{r}$, and $\vec{PA}\cdot\vec{PB} = 0$ for every position of $P$ on the circle."
import numpy as np, matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 2, figsize=(5.2, 2.7))
def arrow(ax, p, q, c=INK, lw=1.9, ls='-', ms=12):
    ax.annotate('', xy=q, xytext=p, arrowprops=dict(arrowstyle='-|>', color=c, lw=lw,
                linestyle=ls, shrinkA=0, shrinkB=0, mutation_scale=ms))
def rightangle(ax, V, P, Q, s=0.17, c=MUTED):
    u = (P - V) / np.linalg.norm(P - V); v = (Q - V) / np.linalg.norm(Q - V)
    pts = np.array([V + s * u, V + s * u + s * v, V + s * v])
    ax.plot(pts[:, 0], pts[:, 1], color=c, lw=0.85)

# ---- (a) rhombus
ax = axes[0]
O = np.array([0.0, 0.0]); a = np.array([1.95, -0.42]); b = np.array([1.30, 1.52])
b = b / np.linalg.norm(b) * np.linalg.norm(a)
C = a + b
for p, q in [(O, a), (a, C), (C, b), (b, O)]:
    ax.plot([p[0], q[0]], [p[1], q[1]], color=MUTED, lw=1.1)
arrow(ax, O, C, SERIES[1], 2.0)
arrow(ax, b, a, SERIES[4], 1.7)
arrow(ax, O, a, ACCENT); arrow(ax, O, b, SERIES[2])
M = C / 2
rightangle(ax, M, C, a, 0.20, INK)
ax.annotate('$\\vec{a}$', (O + a) / 2, textcoords='offset points', xytext=(-2, -14),
            color=ACCENT, fontsize=10.5, ha='center')
ax.annotate('$\\vec{b}$', (O + b) / 2, textcoords='offset points', xytext=(-16, 1),
            color=SERIES[2], fontsize=10.5)
ax.annotate('$\\vec{a}+\\vec{b}$', C, textcoords='offset points', xytext=(4, 4),
            color=SERIES[1], fontsize=10)
ax.annotate('$\\vec{a}-\\vec{b}$', (0.72 * a + 0.28 * b), textcoords='offset points',
            xytext=(12, 8), color=SERIES[4], fontsize=10)
for P, lab, off in [(O, '$O$', (-12, -5)), (a, '$A$', (5, -6)), (b, '$B$', (-9, 6)),
                    (C, '$C$', (0, 0))]:
    if lab != '$C$':
        ax.plot([P[0]], [P[1]], 'o', color=INK, ms=3.4)
        ax.annotate(lab, P, textcoords='offset points', xytext=off, color=INK, fontsize=9.5)
ax.set_title('(a) diagonals of a rhombus', fontsize=9.5)
ax.set_xlim(-0.95, 4.15); ax.set_ylim(-1.15, 2.40)

# ---- (b) angle in a semicircle
ax = axes[1]
R = 1.45; O = np.array([0.0, 0.0])
t = np.linspace(0, 2 * np.pi, 240)
ax.plot(R * np.cos(t), R * np.sin(t), color=GRID, lw=1.2)
A_ = np.array([-R, 0.0]); B_ = np.array([R, 0.0])
ang = np.radians(62); Pp = R * np.array([np.cos(ang), np.sin(ang)])
ax.plot([A_[0], B_[0]], [A_[1], B_[1]], color=MUTED, lw=1.1)
ax.plot([A_[0], Pp[0]], [A_[1], Pp[1]], color=ACCENT, lw=1.6)
ax.plot([B_[0], Pp[0]], [B_[1], Pp[1]], color=SERIES[2], lw=1.6)
arrow(ax, O, Pp, SERIES[4], 1.5)
arrow(ax, O, B_, SERIES[1], 1.5)
rightangle(ax, Pp, A_, B_, 0.30, INK)
ax.annotate('$\\vec{p}$', (O + Pp) / 2, textcoords='offset points', xytext=(-21, -3),
            color=SERIES[4], fontsize=10.5)
ax.annotate('$\\vec{r}$', (O + B_) / 2, textcoords='offset points', xytext=(-2, -14),
            color=SERIES[1], fontsize=10.5, ha='center')
for P, lab, off in [(A_, '$A$', (-13, -4)), (B_, '$B$', (6, -4)), (Pp, '$P$', (2, 8)),
                    (O, '$O$', (-4, -13))]:
    ax.plot([P[0]], [P[1]], 'o', color=INK, ms=3.6)
    ax.annotate(lab, P, textcoords='offset points', xytext=off, color=INK, fontsize=9.5)
bis = (A_ - Pp) / np.linalg.norm(A_ - Pp) + (B_ - Pp) / np.linalg.norm(B_ - Pp)
bis = bis / np.linalg.norm(bis)
ax.annotate('$90^{\\circ}$', Pp + 0.74 * bis, color=INK, fontsize=8.8,
            ha='center', va='center')
ax.set_title('(b) angle in a semicircle', fontsize=9.5)
ax.set_xlim(-2.55, 2.55); ax.set_ylim(-1.88, 1.67)
for ax in axes:
    ax.set_aspect('equal'); ax.axis('off')
fig.subplots_adjust(wspace=0.06)
```

::: example Worked example 9.6
**Problem.** $OACB$ is a parallelogram with $\vec{OA} = \vec{a}$ and
$\vec{OB} = \vec{b}$. Prove that (a) the diagonals are perpendicular if and only if
$OACB$ is a rhombus, and (b) the diagonals are equal in length if and only if
$OACB$ is a rectangle.

**Solution.** The two diagonals are

$$ \vec{OC} = \vec{a}+\vec{b}, \qquad \vec{BA} = \vec{a}-\vec{b} $$

(a) Take their scalar product and expand:

$$ (\vec{a}+\vec{b})\cdot(\vec{a}-\vec{b}) = \vec{a}\cdot\vec{a} - \vec{a}\cdot\vec{b} + \vec{b}\cdot\vec{a} - \vec{b}\cdot\vec{b} $$

The middle two terms cancel because the scalar product is commutative, leaving

$$ (\vec{a}+\vec{b})\cdot(\vec{a}-\vec{b}) = |\vec{a}|^{2} - |\vec{b}|^{2} $$

So the diagonals are perpendicular $\Leftrightarrow$ this is zero
$\Leftrightarrow |\vec{a}| = |\vec{b}|$ $\Leftrightarrow$ the adjacent sides are
equal $\Leftrightarrow$ the parallelogram is a rhombus.

(b) Now compare the squares of the two diagonal lengths:

$$ |\vec{a}+\vec{b}|^{2} = |\vec{a}|^{2} + 2\,\vec{a}\cdot\vec{b} + |\vec{b}|^{2} $$

$$ |\vec{a}-\vec{b}|^{2} = |\vec{a}|^{2} - 2\,\vec{a}\cdot\vec{b} + |\vec{b}|^{2} $$

Subtracting, $|\vec{a}+\vec{b}|^{2} - |\vec{a}-\vec{b}|^{2} = 4\,\vec{a}\cdot\vec{b}$.
The diagonals are equal $\Leftrightarrow$ this difference is zero
$\Leftrightarrow \vec{a}\cdot\vec{b} = 0 \Leftrightarrow \vec{a} \perp \vec{b}$
$\Leftrightarrow$ the parallelogram is a rectangle.
:::

::: derivation The angle in a semicircle is a right angle
We start with a circle and one point on it and finish with a right angle.

**Setting up.** Let $O$ be the centre of a circle of radius $r$, $AB$ a diameter,
and take $O$ as origin with $\vec{OB} = \vec{r}$. Since $O$ is the midpoint of
$AB$, $\vec{OA} = -\vec{r}$. Let $P$ be any point of the circle, $\vec{OP} = \vec{p}$.

**Step 1 — write down the one fact you are given.** $A$, $B$ and $P$ all lie on
the circle, so all three are at distance $r$ from $O$:

$$ |\vec{p}| = |\vec{r}| = r $$

**Step 2 — form the two vectors that meet at $P$** (head minus tail):

$$ \vec{PA} = -\vec{r} - \vec{p}, \qquad \vec{PB} = \vec{r} - \vec{p} $$

**Step 3 — dot them.** Take a factor $-1$ out of $\vec{PA}$ first, so that the
brackets are a difference of two squares:

$$ \vec{PA}\cdot\vec{PB} = -(\vec{r}+\vec{p})\cdot(\vec{r}-\vec{p}) $$

**Step 4 — expand.** The cross terms cancel as in Worked example 9.6:

$$ \vec{PA}\cdot\vec{PB} = -\left(|\vec{r}|^{2} - |\vec{p}|^{2}\right) $$

**Step 5 — use Step 1.** Both magnitudes equal $r$:

$$ \vec{PA}\cdot\vec{PB} = -(r^{2}-r^{2}) = 0 $$

**Result.** $\vec{PA}$ and $\vec{PB}$ are non-zero and their scalar product is
zero, so $\vec{PA} \perp \vec{PB}$, i.e. $\angle APB = 90^{\circ}$.

**What it means.** $\vec{p}$ cancelled, so the result holds wherever $P$ sits:
every point of the semicircle sees the diameter at a right angle.

**Conditions.** $AB$ must be a **diameter** — that is what gives
$\vec{OA} = -\vec{OB}$. For any other chord the cross terms survive.
:::

### Compound angles by scalar product

The addition formulas of trigonometry fall straight out of the two expressions for
one scalar product. This is a favourite Group C question.

::: derivation $\cos(A-B)$ and $\cos(A+B)$ from the scalar product
We start with two unit vectors and finish with the cosine addition formulas.

**Setting up.** In the $xy$-plane let $\vec{OP}$ and $\vec{OQ}$ be **unit** vectors
making angles $A$ and $B$ with the positive $x$-axis, with $A > B$, as in the
figure above. Resolving each into components,

$$ \vec{OP} = \cos A\,\hat{i} + \sin A\,\hat{j}, \qquad \vec{OQ} = \cos B\,\hat{i} + \sin B\,\hat{j} $$

Both are unit vectors, and the angle between them is $A-B$.

**Step 1 — the scalar product from the definition.** With
$|\vec{OP}| = |\vec{OQ}| = 1$ and angle $A-B$:

$$ \vec{OP}\cdot\vec{OQ} = (1)(1)\cos(A-B) = \cos(A-B) $$

**Step 2 — the same scalar product in components.** Multiply matching components
and add:

$$ \vec{OP}\cdot\vec{OQ} = \cos A\cos B + \sin A\sin B $$

**Step 3 — the two answers must agree.**

$$ \cos(A-B) = \cos A\cos B + \sin A\sin B $$

**Step 4 — get the other formula for free.** Replace $B$ by $-B$ throughout, and
use $\cos(-B) = \cos B$, $\sin(-B) = -\sin B$:

$$ \cos(A+B) = \cos A\cos B - \sin A\sin B $$

**Result.** Both cosine addition formulas, from one scalar product.

**What it means.** The formula says the scalar product does not care which axes
you use: rotating both unit vectors together changes $A$ and $B$ but not $A-B$.

**Conditions.** None, once both angles are measured from the same axis. The
results hold for all $A$ and $B$, because $(\cos\theta, \sin\theta)$ is the unit
vector in every quadrant.
:::

::: example Worked example 9.7
**Problem.** Use the scalar product of two suitable unit vectors to find the exact
value of $\cos 15^{\circ}$.

**Solution.** Write $15^{\circ} = 45^{\circ}-30^{\circ}$ and take unit vectors at
$45^{\circ}$ and $30^{\circ}$ to the $x$-axis:

$$ \vec{OP} = \frac{1}{\sqrt{2}}\hat{i} + \frac{1}{\sqrt{2}}\hat{j}, \qquad \vec{OQ} = \frac{\sqrt{3}}{2}\hat{i} + \frac{1}{2}\hat{j} $$

The angle between them is $15^{\circ}$ and both have magnitude $1$, so
$\vec{OP}\cdot\vec{OQ} = \cos 15^{\circ}$. In components,

$$ \vec{OP}\cdot\vec{OQ} = \frac{1}{\sqrt{2}}\cdot\frac{\sqrt{3}}{2} + \frac{1}{\sqrt{2}}\cdot\frac{1}{2} = \frac{\sqrt{3}+1}{2\sqrt{2}} $$

Rationalise by multiplying top and bottom by $\sqrt{2}$:

$$ \cos 15^{\circ} = \frac{\sqrt{6}+\sqrt{2}}{4} = \frac{2.449 + 1.414}{4} = 0.9659 $$

which agrees with the tables. ✔
:::

## 9.4 Vector (cross) product; geometrical interpretation and properties

The scalar product throws away all direction information. Often the direction is
what you need — the normal to a plane, the axis of a turning effect. That calls
for a product whose answer is a **vector**.

::: definition Vector (cross) product
Let $\vec{a}$ and $\vec{b}$ be non-zero, non-parallel vectors with angle $\theta$
between them, $0^{\circ} < \theta < 180^{\circ}$. Their **vector product** is

$$ \vec{a}\times\vec{b} = |\vec{a}|\,|\vec{b}|\sin\theta\;\hat{n} $$

where $\hat{n}$ is the unit vector **perpendicular to both**, in the sense given
by the **right-hand rule**: curl your right fingers from $\vec{a}$ towards
$\vec{b}$ through $\theta$, and the thumb points along $\hat{n}$.

If $\vec{a}$ and $\vec{b}$ are parallel or either is $\vec{0}$, then
$\vec{a}\times\vec{b} = \vec{0}$.
:::

Since $\sin\theta \geq 0$ on $0^{\circ}$ to $180^{\circ}$, the factor
$|\vec{a}||\vec{b}|\sin\theta$ is never negative: it is the magnitude
$|\vec{a}\times\vec{b}|$, and all the directional information sits in $\hat{n}$.

```figure caption="(a) The right-hand rule. $\vec{a}$ and $\vec{b}$ lie in the shaded plane; turning $\vec{a}$ into $\vec{b}$ sends $\vec{a}\times\vec{b}$ out of the plane one way and $\vec{b}\times\vec{a}$ the other, so $\vec{b}\times\vec{a} = -(\vec{a}\times\vec{b})$. (b) The cycle $\hat{i} \to \hat{j} \to \hat{k} \to \hat{i}$: two base vectors read in the arrow direction give the third with a plus sign, against the arrow with a minus sign."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon, FancyArrowPatch
fig, axes = plt.subplots(1, 2, figsize=(5.2, 2.9))
def arrow(ax, p, q, c=INK, lw=2.0, ls='-', ms=13):
    ax.annotate('', xy=q, xytext=p, arrowprops=dict(arrowstyle='-|>', color=c, lw=lw,
                linestyle=ls, shrinkA=0, shrinkB=0, mutation_scale=ms))

# ---- (a) right-hand rule
ax = axes[0]
plane = np.array([[-1.55, -0.62], [1.70, -1.05], [2.30, 0.10], [-0.95, 0.52]])
ax.add_patch(Polygon(plane, closed=True, facecolor=GRID, edgecolor='#b9c0cc',
                     lw=0.9, alpha=0.9, zorder=0))
O = np.array([0.0, 0.0])
a = np.array([1.60, -0.52]); b = np.array([-0.72, 0.30])
arrow(ax, O, a, ACCENT); arrow(ax, O, b, SERIES[2])
arrow(ax, O, np.array([0.0, 1.60]), SERIES[1], 2.2, ms=14)
arrow(ax, O, np.array([0.0, -1.42]), SERIES[4], 1.6, ls=(0, (4, 2)), ms=12)
ax.annotate('$\\vec{a}$', a, textcoords='offset points', xytext=(4, -6),
            color=ACCENT, fontsize=10.5)
ax.annotate('$\\vec{b}$', b, textcoords='offset points', xytext=(-16, 1),
            color=SERIES[2], fontsize=10.5)
ax.annotate('$\\vec{a}\\times\\vec{b}$', (0.0, 1.60), textcoords='offset points',
            xytext=(4, 1), color=SERIES[1], fontsize=10.5)
ax.annotate('$\\vec{b}\\times\\vec{a}$', (0.0, -1.42), textcoords='offset points',
            xytext=(5, -6), color=SERIES[4], fontsize=10.5)
ax.add_patch(FancyArrowPatch((1.02, -0.02), (-0.30, 0.44), connectionstyle='arc3,rad=0.45',
                             arrowstyle='-|>', mutation_scale=10, color=MUTED, lw=1.0))
ax.annotate('turn $\\vec{a}$\ninto $\\vec{b}$', (1.62, 0.95), color=MUTED, fontsize=8.4,
            ha='center', va='center')
sq = 0.15
ax.plot([0, sq, sq], [sq, sq, 0], color=MUTED, lw=0.8)
ax.plot([0], [0], 'o', color=INK, ms=3.6)
ax.annotate('$O$', O, textcoords='offset points', xytext=(-12, -4), color=INK, fontsize=9.5)
ax.set_title('(a) right-hand rule', fontsize=9.5)
ax.set_xlim(-2.0, 2.6); ax.set_ylim(-1.85, 2.15)

# ---- (b) the i, j, k cycle
ax = axes[1]
R = 1.02
labs = ['$\\hat{i}$', '$\\hat{j}$', '$\\hat{k}$']
angs = np.radians([90, -30, 210])
pos = [R * np.array([np.cos(t), np.sin(t)]) for t in angs]
for t0, t1 in [(90, -30), (-30, -150), (-150, -270)]:
    tt = np.radians(np.linspace(t0 - 16, t1 + 16, 40))
    ax.plot(R * np.cos(tt), R * np.sin(tt), color=ACCENT, lw=1.4)
    e0 = R * np.array([np.cos(tt[-2]), np.sin(tt[-2])])
    e1 = R * np.array([np.cos(tt[-1]), np.sin(tt[-1])])
    arrow(ax, e0, e1, ACCENT, 1.4, ms=12)
for p, lab in zip(pos, labs):
    ax.text(p[0] * 1.30, p[1] * 1.30, lab, fontsize=12.5, color=INK,
            ha='center', va='center')
ax.text(0, 0.06, 'with the\narrows: $+$', fontsize=8.6, color=SERIES[2],
        ha='center', va='center')
ax.text(0, -0.52, 'against: $-$', fontsize=8.6, color=SERIES[1],
        ha='center', va='center')
ax.set_title('(b) the $\\hat{i},\\hat{j},\\hat{k}$ cycle', fontsize=9.5)
ax.set_xlim(-2.30, 2.30); ax.set_ylim(-1.85, 2.15)
for ax in axes:
    ax.set_aspect('equal'); ax.axis('off')
fig.subplots_adjust(wspace=0.04)
```

Applying the definition to the base vectors gives the results every calculation
rests on. Distinct base vectors are perpendicular, so $\sin 90^{\circ} = 1$ and
the product has magnitude $1$; the right-hand rule picks the sign.

$$ \hat{i}\times\hat{i} = \hat{j}\times\hat{j} = \hat{k}\times\hat{k} = \vec{0} $$

$$ \hat{i}\times\hat{j} = \hat{k}, \qquad \hat{j}\times\hat{k} = \hat{i}, \qquad \hat{k}\times\hat{i} = \hat{j} $$

$$ \hat{j}\times\hat{i} = -\hat{k}, \qquad \hat{k}\times\hat{j} = -\hat{i}, \qquad \hat{i}\times\hat{k} = -\hat{j} $$

::: memory The cycle
Write $\hat{i}, \hat{j}, \hat{k}$ round a circle in that order, as in the figure.
Reading **with** the arrows — $ij$, $jk$, $ki$ — the product is the remaining
letter with a **plus**. Reading **against** the arrows — $ji$, $kj$, $ik$ — it is
the remaining letter with a **minus**. Nothing else needs memorising; a base vector
crossed with itself is $\vec{0}$.
:::

### Properties, with proofs

::: key Properties of the vector product
1. **Anti-commutative:** $\vec{b}\times\vec{a} = -(\vec{a}\times\vec{b})$
2. **Self product:** $\vec{a}\times\vec{a} = \vec{0}$
3. **Parallel test:** for non-zero vectors, $\vec{a}\times\vec{b} = \vec{0} \Leftrightarrow \vec{a} \parallel \vec{b}$
4. **Scalars pull out:** $(m\vec{a})\times\vec{b} = m(\vec{a}\times\vec{b}) = \vec{a}\times(m\vec{b})$
5. **Distributive:** $\vec{a}\times(\vec{b}+\vec{c}) = \vec{a}\times\vec{b} + \vec{a}\times\vec{c}$
6. **Not associative:** in general $\vec{a}\times(\vec{b}\times\vec{c}) \ne (\vec{a}\times\vec{b})\times\vec{c}$
7. **Magnitude:** $|\vec{a}\times\vec{b}| = |\vec{a}||\vec{b}|\sin\theta$, so $\sin\theta = \dfrac{|\vec{a}\times\vec{b}|}{|\vec{a}||\vec{b}|}$
8. **Lagrange's identity:** $|\vec{a}\times\vec{b}|^{2} = |\vec{a}|^{2}|\vec{b}|^{2} - (\vec{a}\cdot\vec{b})^{2}$
:::

**1. Anti-commutativity.** The magnitude is unchanged, because
$|\vec{b}||\vec{a}|\sin\theta = |\vec{a}||\vec{b}|\sin\theta$ and $\theta$ is the
same angle. Only the direction changes: turning $\vec{b}$ into $\vec{a}$ instead of
$\vec{a}$ into $\vec{b}$ reverses the sense of the right-hand rule, so $\hat{n}$
becomes $-\hat{n}$. Same length, opposite direction:

$$ \vec{b}\times\vec{a} = -(\vec{a}\times\vec{b}) $$

This is the single biggest difference from the scalar product, and the commonest
source of sign errors. **Order matters.**

**2 and 3. Parallel vectors.** A vector makes an angle $0^{\circ}$ with itself, and
$\sin 0^{\circ} = 0$, so $\vec{a}\times\vec{a} = \vec{0}$. More generally if
$\vec{a}$ and $\vec{b}$ are parallel then $\theta = 0^{\circ}$ (same sense) or
$180^{\circ}$ (opposite sense), and $\sin\theta = 0$ either way. Conversely, if
neither vector is $\vec{0}$ and $|\vec{a}||\vec{b}|\sin\theta = 0$ then
$\sin\theta = 0$, so $\theta$ is $0^{\circ}$ or $180^{\circ}$ and the vectors are
parallel. This is the cross-product test for parallelism, and it is neater than
comparing ratios of components because it never divides by zero.

**4. Scalars.** For $m > 0$ neither the angle nor $\hat{n}$ changes and the
magnitude is multiplied by $m$. For $m < 0$ the direction of $m\vec{a}$ reverses, so
the angle becomes $180^{\circ}-\theta$ — but $\sin(180^{\circ}-\theta) = \sin\theta$,
so the magnitude picks up only the factor $|m| = -m$, while $\hat{n}$ reverses.
The two sign changes give $m$ overall.

**5. Distributivity** holds, and is what makes the determinant formula below work.
Its proof is longer than the syllabus requires — NEB quotes it — but you may use it
freely.

**6. No associativity.** One counterexample settles it. On the left,
$\hat{i}\times\hat{j} = \hat{k}$, so

$$ \hat{i}\times(\hat{i}\times\hat{j}) = \hat{i}\times\hat{k} = -\hat{j} $$

On the right, $\hat{i}\times\hat{i} = \vec{0}$, so

$$ (\hat{i}\times\hat{i})\times\hat{j} = \vec{0}\times\hat{j} = \vec{0} $$

and $-\hat{j} \ne \vec{0}$. **Never move the brackets in a cross product.**

**8. Lagrange's identity.** Start from the magnitude and use
$\sin^{2}\theta = 1-\cos^{2}\theta$:

$$ |\vec{a}\times\vec{b}|^{2} = |\vec{a}|^{2}|\vec{b}|^{2}\sin^{2}\theta = |\vec{a}|^{2}|\vec{b}|^{2}\left(1-\cos^{2}\theta\right) $$

$$ = |\vec{a}|^{2}|\vec{b}|^{2} - \left(|\vec{a}||\vec{b}|\cos\theta\right)^{2} = |\vec{a}|^{2}|\vec{b}|^{2} - (\vec{a}\cdot\vec{b})^{2} $$

This identity links the two products, and it is the quickest way to get one of
$|\vec{a}\times\vec{b}|$ and $\vec{a}\cdot\vec{b}$ from the other.

### The determinant form

::: derivation The vector product in components
We start from the definition and the base-vector products, and finish with the
$3\times3$ determinant you actually compute with.

**Setting up.** Let
$\vec{a} = a_1\hat{i}+a_2\hat{j}+a_3\hat{k}$ and
$\vec{b} = b_1\hat{i}+b_2\hat{j}+b_3\hat{k}$.

**Step 1 — multiply out using distributivity.** Every term of $\vec{a}$ crosses
every term of $\vec{b}$, giving nine products. Written out, and pulling the scalar
coefficients through by property 4:

$$ \vec{a}\times\vec{b} = a_1b_1(\hat{i}\times\hat{i}) + a_1b_2(\hat{i}\times\hat{j}) + a_1b_3(\hat{i}\times\hat{k}) $$

$$ + \; a_2b_1(\hat{j}\times\hat{i}) + a_2b_2(\hat{j}\times\hat{j}) + a_2b_3(\hat{j}\times\hat{k}) $$

$$ + \; a_3b_1(\hat{k}\times\hat{i}) + a_3b_2(\hat{k}\times\hat{j}) + a_3b_3(\hat{k}\times\hat{k}) $$

**Step 2 — kill the three diagonal terms.** Each of
$\hat{i}\times\hat{i}$, $\hat{j}\times\hat{j}$, $\hat{k}\times\hat{k}$ is $\vec{0}$,
so the terms in $a_1b_1$, $a_2b_2$, $a_3b_3$ disappear.

**Step 3 — replace the six survivors** using the cycle:

$$ \vec{a}\times\vec{b} = a_1b_2\hat{k} - a_1b_3\hat{j} - a_2b_1\hat{k} + a_2b_3\hat{i} + a_3b_1\hat{j} - a_3b_2\hat{i} $$

**Step 4 — collect the $\hat{i}$, $\hat{j}$ and $\hat{k}$ terms separately.**

$$ \vec{a}\times\vec{b} = (a_2b_3-a_3b_2)\hat{i} + (a_3b_1-a_1b_3)\hat{j} + (a_1b_2-a_2b_1)\hat{k} $$

**Result.** Those three brackets are exactly the three $2\times2$ minors of a
$3\times3$ array whose first row is $\hat{i},\hat{j},\hat{k}$, whose second row is
the components of $\vec{a}$ and whose third row is the components of $\vec{b}$ —
the determinant shown in the figure below.

**What it means.** The middle component carries a minus sign when you expand the
determinant, which is why $a_3b_1$ comes *before* $a_1b_3$ in the
$\hat{j}$ bracket. Writing the second bracket as $a_1b_3 - a_3b_1$ is the single
commonest error in the whole unit.

**Conditions.** Right-handed axes, i.e. $\hat{i}\times\hat{j} = +\hat{k}$. Every
sign in the answer depends on that convention.
:::

```figure caption="The determinant form of the vector product. Expand along the first row: the $\hat{j}$ term carries a minus sign, so its bracket is $a_3b_1-a_1b_3$."
fig = mateq(["$\\vec{a}\\times\\vec{b} =$",
             ("det", [["$\\hat{i}$", "$\\hat{j}$", "$\\hat{k}$"],
                      ["$a_1$", "$a_2$", "$a_3$"],
                      ["$b_1$", "$b_2$", "$b_3$"]])],
            fontsize=13.5, colw=0.62, scale=0.78)
```

::: memory Expanding the determinant by hand
Cover the $\hat{i}$ column: what is left is $a_2b_3-a_3b_2$ — that is the $\hat{i}$
component. Cover the $\hat{j}$ column: what is left is $a_1b_3-a_3b_1$, and you
**change its sign**. Cover the $\hat{k}$ column: what is left is $a_1b_2-a_2b_1$.
Cover, cross-multiply, subtract; minus in the middle.
:::

### Geometrical interpretation: $|\vec{a}\times\vec{b}|$ is an area

::: derivation The magnitude of $\vec{a}\times\vec{b}$ is the area of the parallelogram on $\vec{a}$ and $\vec{b}$
We start from the elementary formula "area $=$ base $\times$ height" and finish with
the cross product.

**Setting up.** Let $OACB$ be the parallelogram with $\vec{OA} = \vec{a}$ and
$\vec{OB} = \vec{b}$, and let $\theta = \angle AOB$ be the angle between them. Take
$OA$ as the base. Drop a perpendicular from $B$ to the line $OA$, meeting it at
$N$, so $BN$ is the height.

**Step 1 — the base.** By definition, base $= OA = |\vec{a}|$.

**Step 2 — the height.** In the right triangle $ONB$ the hypotenuse is
$OB = |\vec{b}|$ and the angle at $O$ is $\theta$, so the side opposite $\theta$ is

$$ BN = OB\sin\theta = |\vec{b}|\sin\theta $$

**Step 3 — multiply.**

$$ \text{area} = \text{base}\times\text{height} = |\vec{a}|\,|\vec{b}|\sin\theta $$

**Step 4 — recognise the right-hand side.** That is precisely the magnitude of the
vector product:

$$ \text{area of parallelogram} = |\vec{a}\times\vec{b}| $$

**Step 5 — halve it for the triangle.** The diagonal $AB$ cuts the parallelogram
into two congruent triangles, so

$$ \text{area of triangle } OAB = \tfrac{1}{2}|\vec{a}\times\vec{b}| $$

**What it means.** The cross product is an area *with an orientation*: its length
is how big the parallelogram is, and its direction is the normal to the plane the
parallelogram lies in. When $\vec{a}$ and $\vec{b}$ are parallel the parallelogram
collapses to a line, area zero — which is property 3 again.

**Conditions.** $\theta$ must be the angle between the vectors drawn from the
common vertex $O$. If the question gives you three vertices, form two vectors from
the *same* vertex first.
:::

```figure caption="$|\vec{a}\times\vec{b}| = |\vec{a}|\,|\vec{b}|\sin\theta$ is the area of the parallelogram $OACB$: base $|\vec{a}|$ times height $BN = |\vec{b}|\sin\theta$. The diagonal $AB$ halves it, so the shaded triangle has area $\frac{1}{2}|\vec{a}\times\vec{b}|$."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon
fig, ax = plt.subplots(figsize=(4.8, 2.8))
O = np.array([0.0, 0.0]); a = np.array([3.10, 0.0]); b = np.array([1.05, 1.55])
C = a + b; N = np.array([b[0], 0.0])
ax.add_patch(Polygon(np.array([O, a, b]), closed=True, facecolor=ACCENT,
                     alpha=0.13, edgecolor='none', zorder=0))
for p, q in [(O, a), (a, C), (C, b), (b, O)]:
    ax.plot([p[0], q[0]], [p[1], q[1]], color=MUTED, lw=1.1)
ax.plot([O[0], b[0]], [O[1], b[1]], color=SERIES[2], lw=2.0)
ax.plot([O[0], a[0]], [O[1], a[1]], color=ACCENT, lw=2.2)
ax.plot([a[0], b[0]], [a[1], b[1]], color=ACCENT, lw=1.1, ls=(0, (4, 2)))
ax.plot([b[0], N[0]], [b[1], N[1]], color=SERIES[1], lw=1.5, ls=(0, (3, 2)))
s = 0.16
ax.plot([N[0] - s, N[0] - s, N[0]], [0, s, s], color=MUTED, lw=0.8)
th = np.linspace(0, np.arctan2(b[1], b[0]), 60)
ax.plot(0.52 * np.cos(th), 0.52 * np.sin(th), color=INK, lw=0.9)
ax.annotate('$\\theta$', (0.62, 0.26), color=INK, fontsize=10.5)
ax.annotate('$\\vec{a}$', (2.30, 0.0), textcoords='offset points', xytext=(0, -14),
            color=ACCENT, fontsize=11, ha='center')
ax.annotate('$\\vec{b}$', b / 2, textcoords='offset points', xytext=(-16, 0),
            color=SERIES[2], fontsize=11)
ax.annotate('$|\\vec{b}|\\sin\\theta$', (b[0], b[1] / 2), textcoords='offset points',
            xytext=(7, 0), color=SERIES[1], fontsize=9.4)
ax.annotate('$\\frac{1}{2}|\\vec{a}\\times\\vec{b}|$', (1.82, 0.40),
            color=ACCENT, fontsize=10.0, ha='center', va='center')
for P, lab, off in [(O, '$O$', (-12, -5)), (a, '$A$', (5, -4)), (b, '$B$', (-11, 5)),
                    (C, '$C$', (5, 2)), (N, '$N$', (-3, -13))]:
    ax.plot([P[0]], [P[1]], 'o', color=INK, ms=3.4)
    ax.annotate(lab, P, textcoords='offset points', xytext=off, color=INK, fontsize=9.5)
ax.set_xlim(-0.8, 4.8); ax.set_ylim(-0.85, 1.95)
ax.set_aspect('equal'); ax.axis('off')
```

::: example Worked example 9.8
**Problem.** If $\vec{a} = 2\hat{i}+\hat{j}+3\hat{k}$ and
$\vec{b} = 3\hat{i}+5\hat{j}-2\hat{k}$, find $\vec{a}\times\vec{b}$ and
$|\vec{a}\times\vec{b}|$. Verify that $\vec{a}\times\vec{b}$ is perpendicular to
$\vec{a}$.

**Solution.** Expand the determinant with $\vec{a}$ in the second row and $\vec{b}$
in the third. Cover the $\hat{i}$ column:

$$ \hat{i}\text{-part} = (1)(-2) - (3)(5) = -2 - 15 = -17 $$

Cover the $\hat{j}$ column and **change the sign**:

$$ \hat{j}\text{-part} = -\left[(2)(-2) - (3)(3)\right] = -(-4-9) = 13 $$

Cover the $\hat{k}$ column:

$$ \hat{k}\text{-part} = (2)(5) - (1)(3) = 10 - 3 = 7 $$

$$ \vec{a}\times\vec{b} = -17\hat{i} + 13\hat{j} + 7\hat{k} $$

$$ |\vec{a}\times\vec{b}| = \sqrt{289+169+49} = \sqrt{507} = 13\sqrt{3} = 22.52 $$

Check the perpendicularity with a scalar product:

$$ \vec{a}\cdot(\vec{a}\times\vec{b}) = (2)(-17) + (1)(13) + (3)(7) = -34+13+21 = 0 $$ 

✔ As it must be, since $\vec{a}\times\vec{b}$ is normal to the plane of $\vec{a}$
and $\vec{b}$.
:::

::: example Worked example 9.9
**Problem.** Find a unit vector perpendicular to both
$\vec{a} = \hat{i}+2\hat{j}+2\hat{k}$ and $\vec{b} = 2\hat{i}+\hat{j}-2\hat{k}$.

**Solution.** Any vector perpendicular to both is parallel to
$\vec{a}\times\vec{b}$, so compute that first:

$$ \hat{i}\text{-part} = (2)(-2)-(2)(1) = -6, \qquad \hat{j}\text{-part} = -\left[(1)(-2)-(2)(2)\right] = 6 $$

$$ \hat{k}\text{-part} = (1)(1)-(2)(2) = -3 $$

$$ \vec{a}\times\vec{b} = -6\hat{i}+6\hat{j}-3\hat{k}, \qquad |\vec{a}\times\vec{b}| = \sqrt{36+36+9} = \sqrt{81} = 9 $$

Divide by the magnitude:

$$ \hat{n} = \frac{-6\hat{i}+6\hat{j}-3\hat{k}}{9} = -\frac{2}{3}\hat{i} + \frac{2}{3}\hat{j} - \frac{1}{3}\hat{k} $$

Since $-\hat{n}$ works too, the full answer is $\pm\hat{n}$. Note also
$\vec{a}\cdot\vec{b} = 2+2-4 = 0$: the vectors are perpendicular, so
$|\vec{a}\times\vec{b}| = |\vec{a}||\vec{b}| = 9$, as found. ✔
:::

::: example Worked example 9.10
**Problem.** For $\vec{a} = 3\hat{i}-\hat{j}+2\hat{k}$ and
$\vec{b} = 2\hat{i}+\hat{j}-\hat{k}$, find the angle between the vectors using
(a) the scalar product, (b) the vector product, and check that the two agree.

**Solution.** Both products first.

$$ \vec{a}\cdot\vec{b} = 6 - 1 - 2 = 3 $$

$$ \vec{a}\times\vec{b} = \left[(-1)(-1)-(2)(1)\right]\hat{i} - \left[(3)(-1)-(2)(2)\right]\hat{j} + \left[(3)(1)-(-1)(2)\right]\hat{k} $$

$$ \vec{a}\times\vec{b} = -\hat{i}+7\hat{j}+5\hat{k}, \qquad |\vec{a}\times\vec{b}| = \sqrt{1+49+25} = \sqrt{75} = 5\sqrt{3} $$

Also $|\vec{a}| = \sqrt{14}$ and $|\vec{b}| = \sqrt{6}$, so
$|\vec{a}||\vec{b}| = \sqrt{84}$.

(a) $\cos\theta = \dfrac{3}{\sqrt{84}} = 0.3273$, giving $\theta = 70.89^{\circ}$.

(b) $\sin\theta = \dfrac{5\sqrt{3}}{\sqrt{84}} = \dfrac{8.660}{9.165} = 0.9449$,
giving $\theta = 70.89^{\circ}$ (taking the acute value, which is right because
$\cos\theta > 0$).

Dividing one by the other avoids the magnitudes altogether:

$$ \tan\theta = \frac{|\vec{a}\times\vec{b}|}{\vec{a}\cdot\vec{b}} = \frac{5\sqrt{3}}{3} = 2.887 \; \Rightarrow \; \theta = 70.89^{\circ} $$ 

✔ All three routes agree.
:::

::: example Worked example 9.11
**Problem.** If $|\vec{a}| = 5$, $|\vec{b}| = 13$ and $|\vec{a}\times\vec{b}| = 25$,
find $\vec{a}\cdot\vec{b}$ and the angle between the vectors.

**Solution.** Use Lagrange's identity rather than looking for the vectors
themselves:

$$ (\vec{a}\cdot\vec{b})^{2} = |\vec{a}|^{2}|\vec{b}|^{2} - |\vec{a}\times\vec{b}|^{2} = (25)(169) - 625 $$

$$ (\vec{a}\cdot\vec{b})^{2} = 4225 - 625 = 3600 \; \Longrightarrow \; \vec{a}\cdot\vec{b} = \pm 60 $$

Both signs are possible, because the data fixes $\sin\theta$ but not the quadrant:

$$ \sin\theta = \frac{25}{(5)(13)} = \frac{5}{13} = 0.3846 $$

so $\theta = 22.62^{\circ}$ (which gives $\vec{a}\cdot\vec{b} = +60$) or
$\theta = 180^{\circ}-22.62^{\circ} = 157.38^{\circ}$ (which gives $-60$).
:::

::: caution The two products are not interchangeable
$\vec{a}\cdot\vec{b}$ is a **number**; $\vec{a}\times\vec{b}$ is a **vector**. So
$\vec{a}\cdot\vec{b} = 3\hat{i}$ is meaningless, and so is
$\vec{a}\times\vec{b} = 12$. Watch two more traps: $\vec{a}\times\vec{b} = \vec{0}$
means *parallel*, not perpendicular (that is the dot product); and
$\vec{a}\times\vec{b} = \vec{a}\times\vec{c}$ does **not** give $\vec{b} = \vec{c}$ —
only that $\vec{b}-\vec{c}$ is parallel to $\vec{a}$.
:::

## 9.5 Applications of vector product in geometry and trigonometry

Everything here follows from two proved facts: $|\vec{a}\times\vec{b}|$ is an
area, and the product vanishes exactly when the vectors are parallel.

### Areas

::: key Areas from a vector product
For a parallelogram with adjacent sides $\vec{a}$ and $\vec{b}$:

$$ \text{area} = |\vec{a}\times\vec{b}| $$

For a triangle $ABC$, take two sides **from the same vertex**:

$$ \text{area} = \tfrac{1}{2}\left|\vec{AB}\times\vec{AC}\right| $$

For a parallelogram whose **diagonals** are $\vec{d_1}$ and $\vec{d_2}$:

$$ \text{area} = \tfrac{1}{2}\left|\vec{d_1}\times\vec{d_2}\right| $$
:::

The third needs a one-line proof. With sides $\vec{p}$, $\vec{q}$ the diagonals
are $\vec{d_1} = \vec{p}+\vec{q}$ and $\vec{d_2} = \vec{q}-\vec{p}$, so by
distributivity

$$ \vec{d_1}\times\vec{d_2} = \vec{p}\times\vec{q} - \vec{p}\times\vec{p} + \vec{q}\times\vec{q} - \vec{q}\times\vec{p} $$

The two self-products are $\vec{0}$, and $-\vec{q}\times\vec{p} = +\vec{p}\times\vec{q}$
by anti-commutativity, so $\vec{d_1}\times\vec{d_2} = 2(\vec{p}\times\vec{q})$.
Taking magnitudes and halving gives the area $|\vec{p}\times\vec{q}|$ as claimed.

::: example Worked example 9.12
**Problem.** Find the area of the triangle with vertices $A(1,1,1)$, $B(1,2,3)$ and
$C(2,3,1)$.

**Solution.** Build two sides from the same vertex, $A$:

$$ \vec{AB} = (1-1)\hat{i} + (2-1)\hat{j} + (3-1)\hat{k} = \hat{j}+2\hat{k} $$

$$ \vec{AC} = (2-1)\hat{i} + (3-1)\hat{j} + (1-1)\hat{k} = \hat{i}+2\hat{j} $$

Cross them, with components $(0,1,2)$ and $(1,2,0)$:

$$ \hat{i}\text{-part} = (1)(0)-(2)(2) = -4, \qquad \hat{j}\text{-part} = -\left[(0)(0)-(2)(1)\right] = 2 $$

$$ \hat{k}\text{-part} = (0)(2)-(1)(1) = -1 $$

$$ \vec{AB}\times\vec{AC} = -4\hat{i}+2\hat{j}-\hat{k}, \qquad \left|\vec{AB}\times\vec{AC}\right| = \sqrt{16+4+1} = \sqrt{21} $$

$$ \text{area} = \tfrac{1}{2}\sqrt{21} = 2.29\ \text{square units} $$
:::

::: example Worked example 9.13
**Problem.** The diagonals of a parallelogram are $3\hat{i}+\hat{j}-2\hat{k}$ and
$\hat{i}-3\hat{j}+4\hat{k}$. Find its area.

**Solution.** Use $\text{area} = \tfrac{1}{2}|\vec{d_1}\times\vec{d_2}|$ with
$(3,1,-2)$ and $(1,-3,4)$:

$$ \hat{i}\text{-part} = (1)(4)-(-2)(-3) = 4-6 = -2 $$

$$ \hat{j}\text{-part} = -\left[(3)(4)-(-2)(1)\right] = -(12+2) = -14 $$

$$ \hat{k}\text{-part} = (3)(-3)-(1)(1) = -9-1 = -10 $$

$$ \vec{d_1}\times\vec{d_2} = -2\hat{i}-14\hat{j}-10\hat{k} $$

$$ \left|\vec{d_1}\times\vec{d_2}\right| = \sqrt{4+196+100} = \sqrt{300} = 10\sqrt{3} $$

$$ \text{area} = \tfrac{1}{2}\left(10\sqrt{3}\right) = 5\sqrt{3} = 8.66\ \text{square units} $$

Had you forgotten the $\tfrac{1}{2}$ you would have doubled the answer — that
factor is what distinguishes diagonals from sides.
:::

### Collinear points and parallel lines

Three points $A$, $B$, $C$ are collinear exactly when $\vec{AB}$ and $\vec{AC}$
are parallel, so by property 3 the test is a single cross product:

$$ A,\,B,\,C \text{ collinear} \; \Leftrightarrow \; \vec{AB}\times\vec{AC} = \vec{0} $$

Geometrically, triangle $ABC$ has zero area. The same product tests two lines for
parallelism: their directions satisfy $\vec{d_1}\times\vec{d_2} = \vec{0}$.

::: example Worked example 9.14
**Problem.** Show that the points $A(3,-2,4)$, $B(1,1,1)$ and $C(-1,4,-2)$ are
collinear.

**Solution.**

$$ \vec{AB} = (1-3, \; 1+2, \; 1-4) = (-2,\,3,\,-3) $$

$$ \vec{AC} = (-1-3, \; 4+2, \; -2-4) = (-4,\,6,\,-6) $$

$$ \hat{i}\text{-part} = (3)(-6)-(-3)(6) = -18+18 = 0 $$

$$ \hat{j}\text{-part} = -\left[(-2)(-6)-(-3)(-4)\right] = -(12-12) = 0 $$

$$ \hat{k}\text{-part} = (-2)(6)-(3)(-4) = -12+12 = 0 $$

So $\vec{AB}\times\vec{AC} = \vec{0}$: the vectors are parallel and share $A$,
so the points are collinear. ✔ Indeed $\vec{AC} = 2\vec{AB}$, so $B$ is the
midpoint of $AC$.
:::

### The sine law

::: derivation The sine law by vector product
We start from the closed triangle relation and finish with
$\dfrac{a}{\sin A} = \dfrac{b}{\sin B} = \dfrac{c}{\sin C}$.

**Setting up.** As in §9.3, take the sides of triangle $ABC$ as vectors in order:
$\vec{a} = \vec{BC}$, $\vec{b} = \vec{CA}$, $\vec{c} = \vec{AB}$, with
$a = |\vec{a}|$, $b = |\vec{b}|$, $c = |\vec{c}|$. Going once round the triangle
returns you to the start, so

$$ \vec{a}+\vec{b}+\vec{c} = \vec{0} $$

**Step 1 — substitute for $\vec{a}$ in $\vec{a}\times\vec{b}$.** From the relation,
$\vec{a} = -\vec{b}-\vec{c}$, so

$$ \vec{a}\times\vec{b} = (-\vec{b}-\vec{c})\times\vec{b} = -(\vec{b}\times\vec{b}) - (\vec{c}\times\vec{b}) $$

**Step 2 — simplify the two terms.** $\vec{b}\times\vec{b} = \vec{0}$, and
$-(\vec{c}\times\vec{b}) = \vec{b}\times\vec{c}$ by anti-commutativity. Hence

$$ \vec{a}\times\vec{b} = \vec{b}\times\vec{c} $$

**Step 3 — repeat with $\vec{b} = -\vec{c}-\vec{a}$.** The same two moves give
$\vec{b}\times\vec{c} = \vec{c}\times\vec{a}$, so all three products are equal:

$$ \vec{a}\times\vec{b} = \vec{b}\times\vec{c} = \vec{c}\times\vec{a} $$

**Step 4 — take magnitudes.** Drawn tail to tail, $\vec{a}$ and $\vec{b}$ make an
angle $180^{\circ}-C$ (see Figure 2a), and $\sin(180^{\circ}-C) = \sin C$, so
$|\vec{a}\times\vec{b}| = ab\sin C$. The same reasoning gives
$|\vec{b}\times\vec{c}| = bc\sin A$ and $|\vec{c}\times\vec{a}| = ca\sin B$.
Therefore

$$ ab\sin C = bc\sin A = ca\sin B $$

**Step 5 — divide right through by $abc$.** Every side is positive, so this is
legal:

$$ \frac{\sin C}{c} = \frac{\sin A}{a} = \frac{\sin B}{b} $$

**Result.** Inverting,

$$ \frac{a}{\sin A} = \frac{b}{\sin B} = \frac{c}{\sin C} $$

**What it means.** The three equal cross products are the three ways of writing
twice the area of the triangle; the sine law just says the area does not care which
pair of sides you compute it from.

**Conditions.** A genuine triangle, so none of $a$, $b$, $c$ is zero. Note where
the sine law comes from compared with the cosine law: cross product versus dot
product, area versus length.
:::

::: tip The examiner is looking for
For the sine law: write $\vec{a}+\vec{b}+\vec{c} = \vec{0}$, cross with one side,
show the three products are equal, take magnitudes using
$\sin(180^{\circ}-C) = \sin C$, divide by $abc$. Marks are lost almost every year
for using $\sin C$ without explaining the $180^{\circ}-C$; write that line down.
:::

### Moment of a force

::: definition Moment (torque) of a force
If a force $\vec{F}$ acts at a point $P$ whose position vector relative to a point
$O$ is $\vec{r} = \vec{OP}$, the **moment** of $\vec{F}$ about $O$ is

$$ \vec{M} = \vec{r}\times\vec{F} $$

Its magnitude is $|\vec{M}| = |\vec{r}||\vec{F}|\sin\theta = |\vec{F}|\,d$,
with $d = |\vec{r}|\sin\theta$ the perpendicular distance from $O$ to the line of
action. Its direction, by the right-hand rule, is the axis of turning. Unit:
newton metre (N m).
:::

$|\vec{M}| = |\vec{F}|d$ is the "force times perpendicular distance" rule of
elementary mechanics, with the cross product supplying the axis as well. A door
turns easily at the handle because $d$ is large; pushing along the line of the
hinge does nothing, since then $\vec{r}\times\vec{F} = \vec{0}$.

```figure caption="The moment of $\vec{F}$ about $O$. Only the perpendicular distance $d = |\vec{r}|\sin\theta$ from $O$ to the line of action matters, so $|\vec{M}| = |\vec{r}||\vec{F}|\sin\theta = |\vec{F}|\,d$. Sliding $\vec{F}$ along its line of action changes $\vec{r}$ but not the moment."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
fig, ax = plt.subplots(figsize=(5.0, 3.1))
def arrow(ax, p, q, c=INK, lw=2.0, ls='-', ms=13):
    ax.annotate('', xy=q, xytext=p, arrowprops=dict(arrowstyle='-|>', color=c, lw=lw,
                linestyle=ls, shrinkA=0, shrinkB=0, mutation_scale=ms))
O = np.array([0.0, 0.0]); P = np.array([2.60, 0.90])
u = np.array([0.5, np.sqrt(3) / 2])
N = P - float(P @ u) * u
ax.plot(*zip(N - 0.35 * u, P + 1.70 * u), color=MUTED, lw=0.9, ls=(0, (4, 2)))
ax.plot(*zip(P, P + 1.05 * (P / np.linalg.norm(P))), color=MUTED, lw=0.8, ls=(0, (1, 2)))
arrow(ax, O, P, ACCENT)
arrow(ax, P, P + 1.25 * u, SERIES[2], 2.2)
ax.plot(*zip(O, N), color=SERIES[1], lw=1.6, ls=(0, (3, 2)))
s = 0.17
n1 = (O - N) / np.linalg.norm(O - N)
ax.plot(*zip(N + s * n1, N + s * n1 + s * u, N + s * u), color=MUTED, lw=0.8)
t0 = np.degrees(np.arctan2(P[1], P[0])); t1 = np.degrees(np.arctan2(u[1], u[0]))
tt = np.radians(np.linspace(t0, t1, 60))
ax.plot(P[0] + 0.62 * np.cos(tt), P[1] + 0.62 * np.sin(tt), color=INK, lw=0.9)
ax.annotate('$\\theta$', (P[0] + 0.62, P[1] + 0.34), color=INK, fontsize=10.5)
ax.annotate('$\\vec{r}$', P / 2, textcoords='offset points', xytext=(2, -15),
            color=ACCENT, fontsize=11, ha='center')
ax.annotate('$\\vec{F}$', P + 1.25 * u, textcoords='offset points', xytext=(6, 0),
            color=SERIES[2], fontsize=11)
perp = np.array([-0.5, -np.sqrt(3) / 2])
ax.annotate('$d = |\\vec{r}|\\sin\\theta$', N / 2 + 0.26 * perp,
            color=SERIES[1], fontsize=9.4, ha='center', va='top')
ax.annotate('line of action', P + 1.70 * u, textcoords='offset points', xytext=(-6, 8),
            color=MUTED, fontsize=8.6, ha='right')
ax.add_patch(FancyArrowPatch((-0.72, -0.30), (-0.72, 0.42),
                             connectionstyle='arc3,rad=0.55', arrowstyle='-|>',
                             mutation_scale=11, color=SERIES[4], lw=1.2))
ax.annotate('$\\vec{M} = \\vec{r}\\times\\vec{F}$\nout of the page', (-1.05, 0.68),
            color=SERIES[4], fontsize=8.8, ha='center')
for Q, lab, off in [(O, '$O$', (-13, -6)), (P, '$P$', (3, -13)), (N, '$N$', (5, -6))]:
    ax.plot([Q[0]], [Q[1]], 'o', color=INK, ms=3.6)
    ax.annotate(lab, Q, textcoords='offset points', xytext=off, color=INK, fontsize=9.5)
ax.set_xlim(-1.95, 4.15); ax.set_ylim(-1.55, 2.45)
ax.set_aspect('equal'); ax.axis('off')
```

::: example Worked example 9.15
**Problem.** A force $\vec{F} = \hat{i}+2\hat{j}-2\hat{k}$ newtons acts at the point
$P(3,2,2)$. Find the moment of $\vec{F}$ about the origin, its magnitude, and the
perpendicular distance from the origin to the line of action of $\vec{F}$.

**Solution.** Here $\vec{r} = \vec{OP} = 3\hat{i}+2\hat{j}+2\hat{k}$, with
components $(3,2,2)$ and $(1,2,-2)$:

$$ \hat{i}\text{-part} = (2)(-2)-(2)(2) = -4-4 = -8 $$

$$ \hat{j}\text{-part} = -\left[(3)(-2)-(2)(1)\right] = -(-6-2) = 8 $$

$$ \hat{k}\text{-part} = (3)(2)-(2)(1) = 6-2 = 4 $$

$$ \vec{M} = \vec{r}\times\vec{F} = -8\hat{i}+8\hat{j}+4\hat{k} $$

$$ |\vec{M}| = \sqrt{64+64+16} = \sqrt{144} = 12\ \text{N m} $$

For the distance use $|\vec{M}| = |\vec{F}|d$, with
$|\vec{F}| = \sqrt{1+4+4} = 3$ N:

$$ d = \frac{|\vec{M}|}{|\vec{F}|} = \frac{12}{3} = 4\ \text{m} $$
:::

### Compound angles by vector product

In §9.3 the scalar product gave $\cos(A\pm B)$. The same two unit vectors, crossed
instead of dotted, give the sine formulas.

::: derivation $\sin(A-B)$ and $\sin(A+B)$ from the vector product
We start from two unit vectors in the $xy$-plane and finish with the sine
compound-angle formulas.

**Setting up.** Work in the plane $z = 0$, with $A > B$ both acute. Let $\vec{OP}$
and $\vec{OQ}$ be unit vectors making angles $A$ and $B$ with the positive
$x$-axis (Figure 2b), so

$$ \vec{OP} = \cos A\,\hat{i} + \sin A\,\hat{j}, \qquad \vec{OQ} = \cos B\,\hat{i} + \sin B\,\hat{j} $$

**Step 1 — cross them in components,** taking $\vec{OQ}\times\vec{OP}$ with
components $(\cos B, \sin B, 0)$ and $(\cos A, \sin A, 0)$. The $\hat{i}$ and
$\hat{j}$ parts each contain a factor $0$ and vanish, leaving only the $\hat{k}$
part:

$$ \vec{OQ}\times\vec{OP} = \left(\cos B\sin A - \sin B\cos A\right)\hat{k} $$

**Step 2 — cross them from the definition.** Both vectors are unit vectors, the
angle from $\vec{OQ}$ to $\vec{OP}$ is $A-B$, and turning $\vec{OQ}$ towards
$\vec{OP}$ is anticlockwise, so the right-hand rule gives $+\hat{k}$:

$$ \vec{OQ}\times\vec{OP} = (1)(1)\sin(A-B)\,\hat{k} $$

**Step 3 — compare the coefficients of $\hat{k}$.** Two expressions for the same
vector must agree component by component:

$$ \sin(A-B) = \sin A\cos B - \cos A\sin B $$

**Step 4 — replace $B$ by $-B$.** Since $\cos(-B) = \cos B$ and
$\sin(-B) = -\sin B$,

$$ \sin(A+B) = \sin A\cos B + \cos A\sin B $$

**Result.** Both sine compound-angle formulas, from one cross product.

**What it means.** The area of the parallelogram on two unit vectors is the sine of
the angle between them. Reading that area in components is the whole proof.

**Conditions.** The derivation as written assumes $A > B$ so that $A-B$ is the
actual (positive) angle between the vectors; the identity itself holds for all $A$
and $B$, as the general theory of trigonometric functions shows.
:::

::: example Worked example 9.16
**Problem.** Use the vector product to evaluate $\sin 75^{\circ}$ exactly.

**Solution.** Take $A = 45^{\circ}$, $B = 30^{\circ}$ and use the sum formula
derived above, which is $\sin(A+B) = \sin A\cos B + \cos A\sin B$:

$$ \sin 75^{\circ} = \sin 45^{\circ}\cos 30^{\circ} + \cos 45^{\circ}\sin 30^{\circ} $$

$$ = \left(\frac{1}{\sqrt{2}}\right)\left(\frac{\sqrt{3}}{2}\right) + \left(\frac{1}{\sqrt{2}}\right)\left(\frac{1}{2}\right) = \frac{\sqrt{3}+1}{2\sqrt{2}} $$

Rationalising by multiplying top and bottom by $\sqrt{2}$:

$$ \sin 75^{\circ} = \frac{\sqrt{6}+\sqrt{2}}{4} = 0.9659 $$

Compare Worked example 9.7: $\cos 15^{\circ}$ has the same value, as it must, since
$\cos 15^{\circ} = \sin(90^{\circ}-15^{\circ}) = \sin 75^{\circ}$. ✔
:::

::: caution Do not mix up the two compound-angle routes
$\cos(A\pm B)$ comes from the **dot** product (a number equals a number);
$\sin(A\pm B)$ comes from the **cross** product (the $\hat{k}$ components must
match). If a question says "using vector methods, prove
$\sin(A+B) = \dots$", a dot-product proof earns nothing.
:::

## Chapter summary

- **Scalar product:** $\vec{a}\cdot\vec{b} = |\vec{a}||\vec{b}|\cos\theta
  = a_1b_1+a_2b_2+a_3b_3$, a **number**. The two forms agree by the cosine law
  applied to the triangle on $\vec{a}$, $\vec{b}$ and $\vec{b}-\vec{a}$.
- **Angle and perpendicularity:**
  $\cos\theta = \dfrac{\vec{a}\cdot\vec{b}}{|\vec{a}||\vec{b}|}$; for non-zero
  vectors $\vec{a}\perp\vec{b} \Leftrightarrow \vec{a}\cdot\vec{b} = 0$. Also
  $\vec{a}\cdot\vec{a} = |\vec{a}|^{2}$, $\hat{i}\cdot\hat{i} = 1$,
  $\hat{i}\cdot\hat{j} = 0$.
- **Properties of $\cdot$:** commutative, distributive over addition,
  $(m\vec{a})\cdot\vec{b} = m(\vec{a}\cdot\vec{b})$, and
  $|\vec{a}\cdot\vec{b}| \leq |\vec{a}||\vec{b}|$. You may **not** cancel a
  vector factor.
- **Projection:** the scalar projection of $\vec{b}$ on $\vec{a}$ is
  $\dfrac{\vec{a}\cdot\vec{b}}{|\vec{a}|}$ (signed), and the vector projection is
  $\dfrac{\vec{a}\cdot\vec{b}}{|\vec{a}|^{2}}\vec{a}$. Work done is
  $W = \vec{F}\cdot\vec{d}$.
- **Dot-product geometry:** cosine law $a^{2} = b^{2}+c^{2}-2bc\cos A$;
  projection law $a = b\cos C + c\cos B$; $\cos(A\pm B) = \cos A\cos B \mp \sin A\sin B$;
  diagonals of a rhombus are perpendicular because
  $(\vec{a}+\vec{b})\cdot(\vec{a}-\vec{b}) = |\vec{a}|^{2}-|\vec{b}|^{2}$; the angle
  in a semicircle is $90^{\circ}$.
- **Vector product:** $\vec{a}\times\vec{b} = |\vec{a}||\vec{b}|\sin\theta\,\hat{n}$
  with $\hat{n}$ given by the right-hand rule — a **vector**. In components it is
  the $3\times3$ determinant with first row $\hat{i},\hat{j},\hat{k}$, i.e.
  $(a_2b_3-a_3b_2)\hat{i}+(a_3b_1-a_1b_3)\hat{j}+(a_1b_2-a_2b_1)\hat{k}$.
- **Properties of $\times$:** anti-commutative
  $\vec{b}\times\vec{a} = -(\vec{a}\times\vec{b})$; $\vec{a}\times\vec{a} = \vec{0}$;
  distributive; **not** associative; $\hat{i}\times\hat{j} = \hat{k}$ round the
  cycle; and $\vec{a}\times\vec{b} = \vec{0} \Leftrightarrow \vec{a}\parallel\vec{b}$
  for non-zero vectors.
- **Areas and Lagrange:** $|\vec{a}\times\vec{b}|$ is the area of the parallelogram
  on $\vec{a},\vec{b}$; a triangle is
  $\tfrac{1}{2}|\vec{AB}\times\vec{AC}|$; a parallelogram from its diagonals is
  $\tfrac{1}{2}|\vec{d_1}\times\vec{d_2}|$; and
  $|\vec{a}\times\vec{b}|^{2}+(\vec{a}\cdot\vec{b})^{2} = |\vec{a}|^{2}|\vec{b}|^{2}$.
- **Cross-product geometry:** sine law
  $\dfrac{a}{\sin A} = \dfrac{b}{\sin B} = \dfrac{c}{\sin C}$ from
  $\vec{a}\times\vec{b} = \vec{b}\times\vec{c} = \vec{c}\times\vec{a}$;
  $\sin(A\pm B) = \sin A\cos B \pm \cos A\sin B$; collinearity of $A,B,C$ from
  $\vec{AB}\times\vec{AC} = \vec{0}$; moment $\vec{M} = \vec{r}\times\vec{F}$ with
  $|\vec{M}| = |\vec{F}|d$.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The value of $\hat{i}\cdot\hat{j} + \hat{j}\cdot\hat{k} + \hat{k}\cdot\hat{i}$ is <span class="marks">[1]</span>
   (a) $0$ (b) $1$ (c) $3$ (d) $-1$
2. $\hat{j}\times\hat{k}$ equals <span class="marks">[1]</span>
   (a) $\hat{i}$ (b) $-\hat{i}$ (c) $\hat{k}$ (d) $\vec{0}$
3. If $|\vec{a}| = 3$, $|\vec{b}| = 4$ and the angle between them is $60^{\circ}$, then $\vec{a}\cdot\vec{b}$ is <span class="marks">[1]</span>
   (a) $6$ (b) $12$ (c) $6\sqrt{3}$ (d) $\dfrac{1}{2}$
4. The angle between $2\hat{i}+3\hat{j}+\hat{k}$ and $\hat{i}-\hat{j}+\hat{k}$ is <span class="marks">[1]</span>
   (a) $0^{\circ}$ (b) $45^{\circ}$ (c) $60^{\circ}$ (d) $90^{\circ}$
5. $|\vec{a}\times\vec{b}|^{2} + (\vec{a}\cdot\vec{b})^{2}$ equals <span class="marks">[1]</span>
   (a) $|\vec{a}|^{2}+|\vec{b}|^{2}$ (b) $|\vec{a}|^{2}|\vec{b}|^{2}$ (c) $2|\vec{a}||\vec{b}|$ (d) $0$
6. For non-zero vectors, $\vec{a}\times\vec{b} = \vec{0}$ means that $\vec{a}$ and $\vec{b}$ are <span class="marks">[1]</span>
   (a) perpendicular (b) parallel (c) equal (d) unit vectors
7. If the diagonals of a parallelogram are $\vec{d_1}$ and $\vec{d_2}$, its area is <span class="marks">[1]</span>
   (a) $|\vec{d_1}\times\vec{d_2}|$ (b) $\dfrac{1}{2}|\vec{d_1}\times\vec{d_2}|$ (c) $\vec{d_1}\cdot\vec{d_2}$ (d) $2|\vec{d_1}\times\vec{d_2}|$
8. If $\hat{a}$ and $\hat{b}$ are unit vectors inclined at $60^{\circ}$, then $|\hat{a}-\hat{b}|$ is <span class="marks">[1]</span>
   (a) $1$ (b) $\sqrt{2}$ (c) $\sqrt{3}$ (d) $2$
9. The projection of $2\hat{i}-\hat{j}+\hat{k}$ on $\hat{i}+2\hat{j}-2\hat{k}$ is <span class="marks">[1]</span>
   (a) $-\dfrac{2}{3}$ (b) $\dfrac{2}{3}$ (c) $-2$ (d) $\dfrac{2}{\sqrt{6}}$
10. A force $2\hat{i}+3\hat{j}-\hat{k}$ newtons moves a body through a displacement $\hat{i}+\hat{j}+\hat{k}$ metres. The work done is <span class="marks">[1]</span>
    (a) $2$ J (b) $4$ J (c) $6$ J (d) $-4$ J

::: note Answers to Group A
**1.** (a) — every term is the dot product of two *different* base vectors, and
each of those is $0$.

**2.** (a) — reading $\hat{j}\to\hat{k}$ with the arrows of the cycle gives the
remaining letter with a plus sign.

**3.** (a) — $\vec{a}\cdot\vec{b} = (3)(4)\cos 60^{\circ} = 12\left(\tfrac12\right) = 6$.

**4.** (d) — the dot product is $2-3+1 = 0$, and neither vector is $\vec{0}$.

**5.** (b) — this is Lagrange's identity,
$|\vec{a}|^{2}|\vec{b}|^{2}\left(\sin^{2}\theta+\cos^{2}\theta\right)$.

**6.** (b) — $\sin\theta = 0$, so $\theta = 0^{\circ}$ or $180^{\circ}$.

**7.** (b) — $\vec{d_1}\times\vec{d_2} = 2(\vec{p}\times\vec{q})$ for sides
$\vec{p},\vec{q}$, so the area is half the diagonal product.

**8.** (a) — $|\hat{a}-\hat{b}|^{2} = 1+1-2\cos 60^{\circ} = 1$.

**9.** (a) — the dot product is $2-2-2 = -2$ and the second vector has magnitude
$3$, so the projection is $-\tfrac{2}{3}$. It is negative because the angle is
obtuse.

**10.** (b) — $W = \vec{F}\cdot\vec{d} = 2+3-1 = 4$ J.
:::

**Group B — Short answer (5 marks each)**

1. Find the angle between the vectors $\hat{i}-2\hat{j}+3\hat{k}$ and
   $3\hat{i}-2\hat{j}+\hat{k}$. <span class="marks">[5]</span>
2. Prove by vector method that the diagonals of a rhombus bisect each other at
   right angles. <span class="marks">[5]</span>
3. Find the value of $\lambda$ for which $\lambda\hat{i}+2\hat{j}+\hat{k}$ is
   perpendicular to $4\hat{i}-9\hat{j}+2\hat{k}$, and state the magnitude of the
   first vector for that $\lambda$. <span class="marks">[5]</span>
4. If $|\vec{a}| = 5$, $|\vec{b}| = 4$ and $\vec{a}\cdot\vec{b} = 10$, find the
   angle between $\vec{a}$ and $\vec{b}$, and the values of $|\vec{a}+\vec{b}|$
   and $|\vec{a}-\vec{b}|$. <span class="marks">[5]</span>
5. Find a unit vector perpendicular to both $2\hat{i}-6\hat{j}-3\hat{k}$ and
   $4\hat{i}+3\hat{j}-\hat{k}$. <span class="marks">[5]</span>
6. Find the area of the triangle whose vertices are $A(1,1,2)$, $B(2,3,5)$ and
   $C(1,5,5)$. <span class="marks">[5]</span>
7. A force $\vec{F} = 2\hat{i}-\hat{j}+2\hat{k}$ newtons acts at the point
   $A(1,3,4)$. Find its moment about $B(1,2,2)$ and the perpendicular distance
   from $B$ to the line of action of $\vec{F}$. <span class="marks">[5]</span>
8. Find the scalar and the vector projection of $\vec{a} = \hat{i}-2\hat{j}+\hat{k}$
   on $\vec{b} = 2\hat{i}-\hat{j}+2\hat{k}$, and the angle between
   them. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Dot the two vectors and find both magnitudes.

$$ \vec{a}\cdot\vec{b} = (1)(3)+(-2)(-2)+(3)(1) = 3+4+3 = 10 $$

$$ |\vec{a}| = \sqrt{1+4+9} = \sqrt{14}, \qquad |\vec{b}| = \sqrt{9+4+1} = \sqrt{14} $$

$$ \cos\theta = \frac{10}{\sqrt{14}\sqrt{14}} = \frac{10}{14} = \frac{5}{7} = 0.7143 $$

$$ \theta = \cos^{-1}(0.7143) = 44.42^{\circ} $$

**2.** Let the rhombus be $OACB$ with $\vec{OA} = \vec{a}$ and $\vec{OB} = \vec{b}$.
All four sides are equal, so $|\vec{a}| = |\vec{b}|$.

*Bisection.* $\vec{OC} = \vec{a}+\vec{b}$, so the midpoint of $OC$ has position
vector $\tfrac{1}{2}(\vec{a}+\vec{b})$. The midpoint of $AB$ has position vector
$\tfrac{1}{2}(\vec{a}+\vec{b})$ as well. The two midpoints coincide, so the
diagonals bisect each other.

*Right angles.* The diagonals are $\vec{OC} = \vec{a}+\vec{b}$ and
$\vec{AB} = \vec{b}-\vec{a}$. Then

$$ (\vec{a}+\vec{b})\cdot(\vec{b}-\vec{a}) = \vec{a}\cdot\vec{b} - \vec{a}\cdot\vec{a} + \vec{b}\cdot\vec{b} - \vec{b}\cdot\vec{a} $$

$$ = |\vec{b}|^{2} - |\vec{a}|^{2} = 0 \qquad \text{since } |\vec{a}| = |\vec{b}| $$

Neither diagonal is $\vec{0}$, so they are perpendicular.

**3.** Perpendicular means the dot product vanishes:

$$ (\lambda)(4) + (2)(-9) + (1)(2) = 0 $$

$$ 4\lambda - 18 + 2 = 0 \; \Longrightarrow \; 4\lambda = 16 \; \Longrightarrow \; \lambda = 4 $$

With $\lambda = 4$ the first vector is $4\hat{i}+2\hat{j}+\hat{k}$, so

$$ |\vec{a}| = \sqrt{16+4+1} = \sqrt{21} = 4.58 $$

**4.** From the definition of the scalar product,

$$ \cos\theta = \frac{\vec{a}\cdot\vec{b}}{|\vec{a}||\vec{b}|} = \frac{10}{(5)(4)} = \frac{1}{2} \; \Longrightarrow \; \theta = 60^{\circ} $$

For the sums, square and expand:

$$ |\vec{a}+\vec{b}|^{2} = |\vec{a}|^{2} + 2\vec{a}\cdot\vec{b} + |\vec{b}|^{2} = 25+20+16 = 61 $$

$$ |\vec{a}+\vec{b}| = \sqrt{61} = 7.81 $$

$$ |\vec{a}-\vec{b}|^{2} = 25-20+16 = 21 \; \Longrightarrow \; |\vec{a}-\vec{b}| = \sqrt{21} = 4.58 $$

**5.** A vector perpendicular to both is $\vec{a}\times\vec{b}$, with components
$(2,-6,-3)$ and $(4,3,-1)$:

$$ \hat{i}\text{-part} = (-6)(-1)-(-3)(3) = 6+9 = 15 $$

$$ \hat{j}\text{-part} = -\left[(2)(-1)-(-3)(4)\right] = -(-2+12) = -10 $$

$$ \hat{k}\text{-part} = (2)(3)-(-6)(4) = 6+24 = 30 $$

$$ \vec{a}\times\vec{b} = 15\hat{i}-10\hat{j}+30\hat{k}, \quad |\vec{a}\times\vec{b}| = \sqrt{225+100+900} = 35 $$

$$ \hat{n} = \pm\frac{15\hat{i}-10\hat{j}+30\hat{k}}{35} = \pm\left(\frac{3}{7}\hat{i}-\frac{2}{7}\hat{j}+\frac{6}{7}\hat{k}\right) $$

**6.** Take two sides from $A$: $\vec{AB} = \hat{i}+2\hat{j}+3\hat{k}$ and
$\vec{AC} = 4\hat{j}+3\hat{k}$, i.e. components $(1,2,3)$ and $(0,4,3)$.

$$ \hat{i}\text{-part} = (2)(3)-(3)(4) = 6-12 = -6 $$

$$ \hat{j}\text{-part} = -\left[(1)(3)-(3)(0)\right] = -3 $$

$$ \hat{k}\text{-part} = (1)(4)-(2)(0) = 4 $$

$$ \left|\vec{AB}\times\vec{AC}\right| = \sqrt{36+9+16} = \sqrt{61} $$

$$ \text{area} = \tfrac{1}{2}\sqrt{61} = 3.91\ \text{square units} $$

**7.** The position vector of $A$ relative to $B$ is

$$ \vec{r} = \vec{BA} = (1-1)\hat{i}+(3-2)\hat{j}+(4-2)\hat{k} = \hat{j}+2\hat{k} $$

With components $(0,1,2)$ and $(2,-1,2)$:

$$ \hat{i}\text{-part} = (1)(2)-(2)(-1) = 4, \qquad \hat{j}\text{-part} = -\left[(0)(2)-(2)(2)\right] = 4 $$

$$ \hat{k}\text{-part} = (0)(-1)-(1)(2) = -2 $$

$$ \vec{M} = 4\hat{i}+4\hat{j}-2\hat{k}, \qquad |\vec{M}| = \sqrt{16+16+4} = 6\ \text{N m} $$

Since $|\vec{F}| = \sqrt{4+1+4} = 3$ N,

$$ d = \frac{|\vec{M}|}{|\vec{F}|} = \frac{6}{3} = 2\ \text{m} $$

**8.** First the dot product and the magnitude of $\vec{b}$:

$$ \vec{a}\cdot\vec{b} = (1)(2)+(-2)(-1)+(1)(2) = 2+2+2 = 6, \qquad |\vec{b}| = \sqrt{4+1+4} = 3 $$

Scalar projection of $\vec{a}$ on $\vec{b}$:

$$ \frac{\vec{a}\cdot\vec{b}}{|\vec{b}|} = \frac{6}{3} = 2 $$

Vector projection:

$$ \frac{\vec{a}\cdot\vec{b}}{|\vec{b}|^{2}}\,\vec{b} = \frac{6}{9}\left(2\hat{i}-\hat{j}+2\hat{k}\right) = \frac{4}{3}\hat{i} - \frac{2}{3}\hat{j} + \frac{4}{3}\hat{k} $$

For the angle, $|\vec{a}| = \sqrt{1+4+1} = \sqrt{6}$, so

$$ \cos\theta = \frac{6}{3\sqrt{6}} = \frac{2}{\sqrt{6}} = 0.8165 \; \Longrightarrow \; \theta = 35.26^{\circ} $$
:::

**Group C — Long answer (8 marks each)**

1. (a) Define the scalar product of two vectors and prove by vector method that
   $a^{2} = b^{2}+c^{2}-2bc\cos A$ in any triangle $ABC$. <span class="marks">[6]</span>
   (b) Hence find the largest angle of the triangle whose sides are $3$, $5$ and
   $7$ units. <span class="marks">[2]</span>
2. (a) Prove by vector method that
   $\sin(A-B) = \sin A\cos B - \cos A\sin B$. <span class="marks">[6]</span>
   (b) Hence evaluate $\sin 15^{\circ}$ in surd form. <span class="marks">[2]</span>
3. (a) Prove by vector method the sine law
   $\dfrac{a}{\sin A} = \dfrac{b}{\sin B} = \dfrac{c}{\sin C}$ for any triangle
   $ABC$. <span class="marks">[6]</span>
   (b) In a triangle, $A = 30^{\circ}$, $B = 45^{\circ}$ and $a = 10$ cm. Find
   $b$. <span class="marks">[2]</span>
4. For the points $A(1,1,1)$, $B(0,1,3)$ and $C(3,5,5)$, find (a) the area of
   triangle $ABC$, (b) a unit vector perpendicular to the plane $ABC$, and (c) the
   angle $\angle BAC$. Verify your area using
   $\tfrac{1}{2}\,bc\sin A$. <span class="marks">[8]</span>

::: note Answers to Group C
**1. (a)** The scalar product of $\vec{a}$ and $\vec{b}$ is
$\vec{a}\cdot\vec{b} = |\vec{a}||\vec{b}|\cos\theta$, where $\theta$ is the angle
between them when they are drawn from a common point; the answer is a real number.

In triangle $ABC$ put $\vec{AB} = \vec{c}$ and $\vec{AC} = \vec{b}$, both drawn
from $A$, so the angle between them is $A$ and

$$ \vec{b}\cdot\vec{c} = bc\cos A $$

By the triangle law, $\vec{BC} = \vec{AC}-\vec{AB} = \vec{b}-\vec{c}$. Square it
with the dot product:

$$ a^{2} = \left|\vec{b}-\vec{c}\right|^{2} = (\vec{b}-\vec{c})\cdot(\vec{b}-\vec{c}) $$

Expand by the distributive law:

$$ a^{2} = \vec{b}\cdot\vec{b} - \vec{b}\cdot\vec{c} - \vec{c}\cdot\vec{b} + \vec{c}\cdot\vec{c} $$

The scalar product is commutative, so the middle terms combine:

$$ a^{2} = |\vec{b}|^{2} + |\vec{c}|^{2} - 2\,\vec{b}\cdot\vec{c} $$

Substituting $\vec{b}\cdot\vec{c} = bc\cos A$:

$$ a^{2} = b^{2}+c^{2}-2bc\cos A $$

**(b)** The largest angle faces the longest side, $7$. Put $a = 7$, $b = 3$,
$c = 5$:

$$ \cos A = \frac{b^{2}+c^{2}-a^{2}}{2bc} = \frac{9+25-49}{2(3)(5)} = \frac{-15}{30} = -\frac{1}{2} $$

$$ A = 120^{\circ} $$

**2. (a)** Work in the plane $z = 0$ with $A > B$. Let $\vec{OP}$ and $\vec{OQ}$
be unit vectors making angles $A$ and $B$ with the positive $x$-axis:

$$ \vec{OP} = \cos A\,\hat{i}+\sin A\,\hat{j}, \qquad \vec{OQ} = \cos B\,\hat{i}+\sin B\,\hat{j} $$

Cross them in components, taking $\vec{OQ}\times\vec{OP}$ with
$(\cos B, \sin B, 0)$ and $(\cos A, \sin A, 0)$. The $\hat{i}$ and $\hat{j}$ parts
both contain a factor $0$, so

$$ \vec{OQ}\times\vec{OP} = \left(\cos B\sin A - \sin B\cos A\right)\hat{k} $$

Now use the definition: both are unit vectors, the angle from $\vec{OQ}$ to
$\vec{OP}$ is $A-B$, and the turn is anticlockwise, so $\hat{n} = +\hat{k}$:

$$ \vec{OQ}\times\vec{OP} = (1)(1)\sin(A-B)\,\hat{k} $$

Comparing the coefficients of $\hat{k}$ in the two expressions:

$$ \sin(A-B) = \sin A\cos B - \cos A\sin B $$

**(b)** Take $A = 45^{\circ}$ and $B = 30^{\circ}$:

$$ \sin 15^{\circ} = \sin 45^{\circ}\cos 30^{\circ} - \cos 45^{\circ}\sin 30^{\circ} $$

$$ = \left(\frac{1}{\sqrt{2}}\right)\left(\frac{\sqrt{3}}{2}\right) - \left(\frac{1}{\sqrt{2}}\right)\left(\frac{1}{2}\right) = \frac{\sqrt{3}-1}{2\sqrt{2}} = \frac{\sqrt{6}-\sqrt{2}}{4} $$

which is $0.2588$.

**3. (a)** Take the sides of triangle $ABC$ as vectors in order:
$\vec{a} = \vec{BC}$, $\vec{b} = \vec{CA}$, $\vec{c} = \vec{AB}$. Going once round
the triangle returns to the start, so

$$ \vec{a}+\vec{b}+\vec{c} = \vec{0} $$

Substitute $\vec{a} = -\vec{b}-\vec{c}$ into $\vec{a}\times\vec{b}$:

$$ \vec{a}\times\vec{b} = (-\vec{b}-\vec{c})\times\vec{b} = -(\vec{b}\times\vec{b}) - (\vec{c}\times\vec{b}) $$

Now $\vec{b}\times\vec{b} = \vec{0}$ and $-(\vec{c}\times\vec{b}) = \vec{b}\times\vec{c}$,
so $\vec{a}\times\vec{b} = \vec{b}\times\vec{c}$. Repeating with
$\vec{b} = -\vec{c}-\vec{a}$ gives $\vec{b}\times\vec{c} = \vec{c}\times\vec{a}$, so

$$ \vec{a}\times\vec{b} = \vec{b}\times\vec{c} = \vec{c}\times\vec{a} $$

Take magnitudes. Tail to tail, $\vec{a}$ and $\vec{b}$ are inclined at
$180^{\circ}-C$ and $\sin(180^{\circ}-C) = \sin C$, so
$|\vec{a}\times\vec{b}| = ab\sin C$, and likewise for the others. Hence

$$ ab\sin C = bc\sin A = ca\sin B $$

Dividing throughout by $abc$, which is non-zero:

$$ \frac{\sin C}{c} = \frac{\sin A}{a} = \frac{\sin B}{b} \quad\Longrightarrow\quad \frac{a}{\sin A} = \frac{b}{\sin B} = \frac{c}{\sin C} $$

**(b)** Using the sine law with $a = 10$, $A = 30^{\circ}$, $B = 45^{\circ}$:

$$ b = \frac{a\sin B}{\sin A} = \frac{10\sin 45^{\circ}}{\sin 30^{\circ}} = \frac{10(0.7071)}{0.5} = 14.14\ \text{cm} $$

Exactly, $b = 10\sqrt{2}$ cm.

**4.** Build both sides from $A$:

$$ \vec{AB} = (0-1,\; 1-1,\; 3-1) = (-1,\,0,\,2) $$

$$ \vec{AC} = (3-1,\; 5-1,\; 5-1) = (2,\,4,\,4) $$

**(a)** Cross them:

$$ \hat{i}\text{-part} = (0)(4)-(2)(4) = -8, \qquad \hat{j}\text{-part} = -\left[(-1)(4)-(2)(2)\right] = 8 $$

$$ \hat{k}\text{-part} = (-1)(4)-(0)(2) = -4 $$

$$ \vec{AB}\times\vec{AC} = -8\hat{i}+8\hat{j}-4\hat{k}, \qquad \left|\vec{AB}\times\vec{AC}\right| = \sqrt{64+64+16} = 12 $$

$$ \text{area} = \tfrac{1}{2}(12) = 6\ \text{square units} $$

**(b)** The cross product is normal to the plane, so a unit normal is

$$ \hat{n} = \pm\frac{-8\hat{i}+8\hat{j}-4\hat{k}}{12} = \pm\left(-\frac{2}{3}\hat{i}+\frac{2}{3}\hat{j}-\frac{1}{3}\hat{k}\right) $$

**(c)** For the angle at $A$ use the scalar product of the same two vectors:

$$ \vec{AB}\cdot\vec{AC} = (-1)(2)+(0)(4)+(2)(4) = -2+0+8 = 6 $$

$$ \left|\vec{AB}\right| = \sqrt{1+0+4} = \sqrt{5}, \qquad \left|\vec{AC}\right| = \sqrt{4+16+16} = 6 $$

$$ \cos A = \frac{6}{6\sqrt{5}} = \frac{1}{\sqrt{5}} = 0.4472 \; \Longrightarrow \; \angle BAC = 63.43^{\circ} $$

*Check.* With $c = |\vec{AB}| = \sqrt{5}$, $b = |\vec{AC}| = 6$ and
$\sin 63.43^{\circ} = 0.8944$,

$$ \tfrac{1}{2}bc\sin A = \tfrac{1}{2}(6)(2.2361)(0.8944) = 6.00 $$ 

✔ in agreement with part (a).
:::
