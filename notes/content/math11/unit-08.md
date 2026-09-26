---
subject: Mathematics
grade: 11
unit: 8
title: Complex Numbers
hours: 4
area: Algebra
---

The equation $x^{2}+1 = 0$ has no real solution, because no real number squares to
a negative. Rather than stop there, mathematicians invented a new number whose
square is $-1$ and found that the resulting system — the **complex numbers** —
obeys all the usual rules of algebra, gives every quadratic two roots, and has a
clean picture as points of a plane. This unit sets up that arithmetic and that
picture.

::: key What the exam asks
Powers of $i$; add, subtract, multiply and divide complex numbers; plot $z$ on an
Argand diagram and find $|z|$ and $\arg z$; use the conjugate properties; and find
$\sqrt{a+ib}$ by the "let $\sqrt{a+ib} = x+iy$" method. Cube roots of unity appear
in Group B.
:::

## 8.1 Imaginary unit; algebra of complex numbers

::: definition The imaginary unit
$$ i = \sqrt{-1}, \qquad \text{so} \qquad i^{2} = -1 $$
A **complex number** is $z = a + ib$ where $a$, $b$ are real. $a = \mathrm{Re}(z)$ is
the **real part** and $b = \mathrm{Im}(z)$ is the **imaginary part** (note: $b$ itself
is real). If $b = 0$, $z$ is real; if $a = 0$ and $b \ne 0$, $z$ is **purely
imaginary**. The set of all complex numbers is $\mathbb{C}$.
:::

Two complex numbers are **equal** exactly when their real parts are equal *and*
their imaginary parts are equal:

$$ a + ib = c + id \Leftrightarrow a = c \ \text{ and } \ b = d $$

This single fact turns one complex equation into two real equations, and it is the
engine behind almost every problem in this chapter.

### Powers of $i$

$$ i^{1} = i, \quad i^{2} = -1, \quad i^{3} = i^{2}\cdot i = -i, \quad
i^{4} = \left(i^{2}\right)^{2} = 1 $$

After that the pattern repeats with period $4$, so $i^{n}$ depends only on the
remainder when $n$ is divided by $4$.

```figure caption="Multiplying by $i$ rotates a number a quarter-turn anticlockwise, so the powers of $i$ cycle with period 4."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6,3.2))
th = np.linspace(0, 2*np.pi, 300)
ax.plot(np.cos(th), np.sin(th), color=GRID, lw=1.2)
pts = [(1, 0, '$i^{4} = 1$', (1.32, -0.34), 'left'),
       (0, 1, '$i^{1} = i$', (0.14, 1.30), 'left'),
       (-1, 0, '$i^{2} = -1$', (-1.32, -0.34), 'right'),
       (0, -1, '$i^{3} = -i$', (0.14, -1.42), 'left')]
for x, y, lab, tp, ha in pts:
    ax.annotate('', xy=(x,y), xytext=(0,0),
                arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.6, mutation_scale=11))
    ax.plot([x],[y],'o',color=ACCENT,ms=5.5,zorder=5)
    ax.annotate(lab, tp, fontsize=9.4, color=INK, ha=ha)
R = 1.16
for k in range(4):
    a0 = k*np.pi/2 + 0.26; a1 = a0 + np.pi/2 - 0.52
    aa = np.linspace(a0, a1, 40)
    ax.plot(R*np.cos(aa), R*np.sin(aa), color='#d9534f', lw=1.0)
    ax.annotate('', xy=(R*np.cos(a1), R*np.sin(a1)),
                xytext=(R*np.cos(a1-0.06), R*np.sin(a1-0.06)),
                arrowprops=dict(arrowstyle='-|>', color='#d9534f', lw=1.0, mutation_scale=9))
ax.annotate(r'$\times i$', (1.00, 1.00), fontsize=9.6, color='#d9534f', ha='left')
ax.axhline(0, color=MUTED, lw=0.8); ax.axvline(0, color=MUTED, lw=0.8)
ax.set_xlim(-2.35, 2.35); ax.set_ylim(-1.75, 1.60)
ax.set_aspect('equal'); ax.axis('off')
```

::: example Worked example 8.1
**Problem.** Evaluate (a) $i^{2026}$, (b) $i^{-35}$.

**Solution.** (a) Divide the index by $4$: $2026 = 4 \times 506 + 2$, so

$$ i^{2026} = \left(i^{4}\right)^{506}\cdot i^{2} = 1^{506}\times(-1) = -1 $$

(b) $\;-35 = 4\times(-9) + 1$, so $i^{-35} = \left(i^{4}\right)^{-9}\cdot i^{1} = i$.

Alternatively $i^{-35} = \dfrac{1}{i^{35}}$; since $35 = 4\times 8 + 3$,
$i^{35} = i^{3} = -i$, and $\dfrac{1}{-i} = \dfrac{-1}{i}\cdot\dfrac{i}{i}
= \dfrac{-i}{-1} = i$. Same answer.
:::

### The four operations

Add and subtract componentwise; multiply as ordinary binomials and replace
$i^{2}$ by $-1$:

$$ (a+ib)+(c+id) = (a+c) + i(b+d) $$
$$ (a+ib)(c+id) = (ac-bd) + i(ad+bc) $$

Division is done by multiplying above and below by the **conjugate** of the
denominator, which makes the denominator real:

$$ \frac{a+ib}{c+id} = \frac{a+ib}{c+id}\times\frac{c-id}{c-id}
= \frac{(ac+bd) + i(bc-ad)}{c^{2}+d^{2}} $$

::: caution $\sqrt{a}\sqrt{b} = \sqrt{ab}$ fails for negatives
$\sqrt{-4}\times\sqrt{-9} = (2i)(3i) = 6i^{2} = -6$, **not** $\sqrt{36} = 6$.
Always convert each negative square root to $i$ form *first*, then multiply.
:::

::: example Worked example 8.2
**Problem.** Simplify $(3+4i)(2-5i)$.

**Solution.** Expand as usual:

$$ (3+4i)(2-5i) = 6 - 15i + 8i - 20i^{2} $$

Since $i^{2} = -1$, the last term is $-20(-1) = +20$:

$$ = (6+20) + (-15+8)i = 26 - 7i $$
:::

::: example Worked example 8.3
**Problem.** Express $\dfrac{2+3i}{3-4i}$ in the form $a+ib$.

**Solution.** Multiply numerator and denominator by $3+4i$, the conjugate of the
denominator:

$$ \frac{2+3i}{3-4i}\times\frac{3+4i}{3+4i}
= \frac{6+8i+9i+12i^{2}}{3^{2}+4^{2}} = \frac{6+17i-12}{25} $$

$$ = \frac{-6+17i}{25} = -\frac{6}{25} + \frac{17}{25}\,i $$

The denominator became $(3)^{2}+(4)^{2} = 25$ — a real number — because
$(c+id)(c-id) = c^{2}+d^{2}$.
:::

::: example Worked example 8.4
**Problem.** Find real $x$ and $y$ such that $(x+iy)(3-2i) = 13+13i$.

**Solution.** Expand the left side:

$$ (x+iy)(3-2i) = 3x - 2xi + 3yi - 2yi^{2} = (3x+2y) + i(3y-2x) $$

Equate real and imaginary parts with $13+13i$:

$$ 3x + 2y = 13, \qquad -2x + 3y = 13 $$

Multiply the first by $3$ and the second by $2$, then add:
$9x+6y = 39$ and $-4x+6y = 26$; subtracting gives $13x = 13$, so $x = 1$.
Then $3(1)+2y = 13$ gives $y = 5$.

$$ x = 1, \quad y = 5 $$

**Check.** $(1+5i)(3-2i) = 3-2i+15i-10i^{2} = 3+13i+10 = 13+13i$. Correct.
:::

## 8.2 Geometric representation

Because $z = a+ib$ is fixed by the *pair* of real numbers $(a, b)$, every complex
number is a point of a plane. That plane is the **Argand diagram**: the horizontal
axis carries the real part (the **real axis**), the vertical axis the imaginary
part (the **imaginary axis**).

::: definition Argand diagram, modulus, argument
$z = a+ib$ is plotted as the point $P(a, b)$, or as the vector $\vec{OP}$.

- **Modulus** $|z| = OP = \sqrt{a^{2}+b^{2}}$ — the distance from the origin.
- **Argument** $\arg z = \theta$, the angle $\vec{OP}$ makes with the positive
  real axis, measured anticlockwise. The value in $(-\pi, \pi]$ is the
  **principal argument**.
:::

```figure caption="The Argand diagram. $z = 3+4i$ is the point $(3,4)$; $|z| = 5$ is the length $OP$ and $\\theta = \\arg z$ is the marked angle. The conjugate $\\bar{z} = 3-4i$ is the mirror image in the real axis."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,3.2))
ax.plot([-1.6, 7.7], [0,0], color=INK, lw=1.0)
ax.plot([0,0], [-5.9, 6.2], color=INK, lw=1.0)
ax.annotate('', xy=(3,4), xytext=(0,0),
            arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=2.0, mutation_scale=12))
ax.annotate('', xy=(3,-4), xytext=(0,0),
            arrowprops=dict(arrowstyle='-|>', color='#2e8b57', lw=1.6, mutation_scale=11))
ax.plot([3,3],[0,4], color=MUTED, lw=0.9, ls=(0,(2,2)))
ax.plot([0,3],[4,4], color=MUTED, lw=0.9, ls=(0,(2,2)))
ax.plot([3],[4],'o',color=ACCENT,ms=6.5,zorder=5)
ax.plot([3],[-4],'o',color='#2e8b57',ms=6.5,zorder=5)
aa = np.linspace(0, np.arctan2(4,3), 60)
ax.plot(1.25*np.cos(aa), 1.25*np.sin(aa), color='#d9534f', lw=1.2)
ax.annotate(r'$\theta$', (1.50, 0.50), fontsize=10.5, color='#d9534f', ha='left')
ax.annotate('$P(3,4)$:  $z = 3+4i$', (3.30, 4.18), fontsize=9.4, color=ACCENT, ha='left')
ax.annotate(r'$\bar{z} = 3-4i$', (3.30, -4.20), fontsize=9.4, color='#2e8b57', ha='left')
ax.annotate('$|z| = 5$', (0.85, 2.55), fontsize=9.6, color=ACCENT, ha='right')
ax.annotate('$a = 3$', (1.5, -0.75), ha='center', fontsize=9.2, color=MUTED)
ax.annotate('$b = 4$', (3.20, 1.90), ha='left', fontsize=9.2, color=MUTED)
ax.annotate('real axis', (7.6, 0.35), ha='right', fontsize=9.2, color=MUTED)
ax.annotate('imaginary axis', (0.22, 5.65), ha='left', fontsize=9.2, color=MUTED)
ax.set_xlim(-1.8, 7.9); ax.set_ylim(-6.1, 6.4)
ax.set_aspect('equal'); ax.axis('off')
```

### Polar (modulus–argument) form

From the right triangle in the figure, $a = r\cos\theta$ and $b = r\sin\theta$
where $r = |z|$. Hence

::: key Polar form
$$ z = r\left(\cos\theta + i\sin\theta\right), \qquad
r = \sqrt{a^{2}+b^{2}}, \qquad \tan\theta = \frac{b}{a} $$
$\tan\theta = b/a$ alone does not fix $\theta$ — two angles a half-turn apart share
a tangent. **Always check which quadrant $(a,b)$ lies in** and adjust.
:::

| Quadrant of $(a,b)$ | Principal argument $\theta$, where $\tan\alpha = |b/a|$, $0 < \alpha < \pi/2$ |
|---|---|
| I ($a>0$, $b>0$) | $\theta = \alpha$ |
| II ($a<0$, $b>0$) | $\theta = \pi - \alpha$ |
| III ($a<0$, $b<0$) | $\theta = -(\pi - \alpha)$ |
| IV ($a>0$, $b<0$) | $\theta = -\alpha$ |

::: example Worked example 8.5
**Problem.** Express $z = -1 + i\sqrt{3}$ in polar form.

**Solution.** Here $a = -1$, $b = \sqrt{3}$.

$$ r = |z| = \sqrt{(-1)^{2}+\left(\sqrt{3}\right)^{2}} = \sqrt{1+3} = \sqrt{4} = 2 $$

$$ \alpha = \tan^{-1}\left(\frac{\sqrt{3}}{1}\right) = \tan^{-1}\sqrt{3}
= \frac{\pi}{3} $$

Since $a < 0$ and $b > 0$, the point lies in the **second quadrant**, so

$$ \theta = \pi - \frac{\pi}{3} = \frac{2\pi}{3} = 120^{\circ} $$

$$ z = 2\left(\cos\frac{2\pi}{3} + i\sin\frac{2\pi}{3}\right) $$

**Check.** $2\cos 120^{\circ} = 2(-\tfrac12) = -1$ and
$2\sin 120^{\circ} = 2\left(\tfrac{\sqrt{3}}{2}\right) = \sqrt{3}$. Correct.
:::

### Addition is vector addition

$z_1 + z_2$ is the diagonal of the parallelogram on $\vec{Oz_1}$ and
$\vec{Oz_2}$ — exactly the triangle law for vectors. One side of a triangle is
never longer than the other two together, which gives the **triangle inequality**

$$ |z_1 + z_2| \le |z_1| + |z_2| $$

```figure caption="Addition follows the parallelogram law: $(4+i)+(1+3i) = 5+4i$. The closing side is never longer than the two others added, which is the triangle inequality."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6,3.0))
z1 = (4,1); z2 = (1,3); zs = (5,4)
ax.axhline(0, color=INK, lw=1.0); ax.axvline(0, color=INK, lw=1.0)
for z, col, lab, off in ((z1, ACCENT, '$z_1 = 4+i$', (6,-12)),
                         (z2, '#2e8b57', '$z_2 = 1+3i$', (-6,8)),
                         (zs, '#d9534f', '$z_1+z_2 = 5+4i$', (6,4))):
    ax.annotate('', xy=z, xytext=(0,0),
                arrowprops=dict(arrowstyle='-|>', color=col, lw=1.8, mutation_scale=12))
    ax.plot([z[0]],[z[1]],'o',color=col,ms=5.5,zorder=5)
    ha = 'right' if off[0] < 0 else 'left'
    ax.annotate(lab, z, textcoords='offset points', xytext=off, fontsize=9.2,
                color=col, ha=ha)
ax.plot([z1[0],zs[0]],[z1[1],zs[1]], color=MUTED, lw=1.0, ls=(0,(3,2)))
ax.plot([z2[0],zs[0]],[z2[1],zs[1]], color=MUTED, lw=1.0, ls=(0,(3,2)))
ax.set_xlim(-0.9, 6.9); ax.set_ylim(-0.9, 5.2)
ax.set_aspect('equal'); ax.axis('off')
```

## 8.3 Modulus and conjugate with properties

::: definition Conjugate
The **conjugate** of $z = a+ib$ is $\bar{z} = a - ib$: the same point reflected in
the real axis. Reflecting twice returns you to the start, so
$\overline{\left(\bar{z}\right)} = z$.
:::

::: key Properties you may quote
For all $z, z_1, z_2 \in \mathbb{C}$:

| Conjugate | Modulus |
|---|---|
| $\overline{z_1 \pm z_2} = \bar{z_1} \pm \bar{z_2}$ | $|z_1 z_2| = |z_1||z_2|$ |
| $\overline{z_1 z_2} = \bar{z_1}\,\bar{z_2}$ | $|z_1/z_2| = \dfrac{|z_1|}{|z_2|}$ |
| $\overline{\left(\dfrac{z_1}{z_2}\right)} = \dfrac{\bar{z_1}}{\bar{z_2}}$ | $|z| = |\bar{z}| = |-z|$ |
| $z + \bar{z} = 2\,\mathrm{Re}(z)$ | $z\bar{z} = |z|^{2}$ |
| $z - \bar{z} = 2i\,\mathrm{Im}(z)$ | $|z_1+z_2| \le |z_1|+|z_2|$ |

$z$ is real $\Leftrightarrow z = \bar{z}$; $z$ is purely imaginary $\Leftrightarrow z = -\bar{z}$.
:::

::: derivation $z\bar{z} = |z|^{2}$, and the reason division works
With $z = a+ib$,

$$ z\bar{z} = (a+ib)(a-ib) = a^{2} - (ib)^{2} = a^{2} - i^{2}b^{2} = a^{2}+b^{2} $$

and $|z| = \sqrt{a^{2}+b^{2}}$, so $z\bar{z} = |z|^{2}$ — always a **non-negative
real number**. This is precisely why multiplying by the conjugate clears a complex
denominator, and it gives the reciprocal formula

$$ \frac{1}{z} = \frac{\bar{z}}{z\bar{z}} = \frac{\bar{z}}{|z|^{2}}
\qquad (z \ne 0) $$
:::

::: example Worked example 8.6
**Problem.** Verify that $|z_1 z_2| = |z_1||z_2|$ for $z_1 = 3+4i$ and
$z_2 = 1-2i$.

**Solution.**

$$ |z_1| = \sqrt{9+16} = 5, \qquad |z_2| = \sqrt{1+4} = \sqrt{5} $$

$$ z_1 z_2 = (3+4i)(1-2i) = 3 - 6i + 4i - 8i^{2} = 3 - 2i + 8 = 11 - 2i $$

$$ |z_1 z_2| = \sqrt{121+4} = \sqrt{125} = 5\sqrt{5} $$

And $|z_1||z_2| = 5\sqrt{5}$. The two agree.
:::

::: example Worked example 8.7
**Problem.** If $z = \dfrac{1+i}{1-i}$, find $z$, $|z|$ and $\arg z$.

**Solution.** Multiply above and below by $1+i$:

$$ z = \frac{1+i}{1-i}\times\frac{1+i}{1+i} = \frac{(1+i)^{2}}{1^{2}+1^{2}}
= \frac{1+2i+i^{2}}{2} = \frac{2i}{2} = i $$

So $z = i = 0 + 1i$, giving $|z| = \sqrt{0+1} = 1$ and, since the point $(0,1)$
lies on the positive imaginary axis, $\arg z = \dfrac{\pi}{2} = 90^{\circ}$.
:::

::: example Worked example 8.8
**Problem.** Evaluate $(1+i)^{8}$.

**Solution.** Square first and use the result repeatedly.

$$ (1+i)^{2} = 1 + 2i + i^{2} = 2i $$

$$ (1+i)^{8} = \left[(1+i)^{2}\right]^{4} = (2i)^{4} = 2^{4}i^{4} = 16 \times 1 = 16 $$

**Modulus check.** $|1+i| = \sqrt{2}$, so $|(1+i)^{8}| = \left(\sqrt{2}\right)^{8} = 16$,
matching the real answer $16$.
:::

### Cube roots of unity

Solving $z^{3} = 1$, i.e. $z^{3}-1 = (z-1)\left(z^{2}+z+1\right) = 0$, gives
$z = 1$ and the roots of $z^{2}+z+1 = 0$:

$$ z = \frac{-1 \pm \sqrt{1-4}}{2} = \frac{-1 \pm i\sqrt{3}}{2} $$

Write $\omega = \dfrac{-1+i\sqrt{3}}{2}$. Then the three cube roots of unity are
$1$, $\omega$, $\omega^{2}$.

::: key Cube roots of unity
$$ 1 + \omega + \omega^{2} = 0, \qquad \omega^{3} = 1 $$
Each has modulus $1$, and their arguments are $0^{\circ}$, $120^{\circ}$ and
$240^{\circ}$ — they sit at the corners of an equilateral triangle on the unit
circle. The first identity is just the coefficient relation for
$z^{2}+z+1 = 0$ together with the root $z = 1$.
:::

```figure caption="The cube roots of unity $1$, $\omega$, $\omega^{2}$ lie on the unit circle $120^{\circ}$ apart, forming an equilateral triangle. Being symmetric about the origin's directions, they add to zero."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.4,3.2))
th = np.linspace(0, 2*np.pi, 300)
ax.plot(np.cos(th), np.sin(th), color=GRID, lw=1.3)
ax.axhline(0, color=MUTED, lw=0.8); ax.axvline(0, color=MUTED, lw=0.8)
ang = [0, 2*np.pi/3, 4*np.pi/3]
labs = ['$1$', r'$\omega = -\frac{1}{2}+\frac{\sqrt{3}}{2}i$',
        r'$\omega^{2} = -\frac{1}{2}-\frac{\sqrt{3}}{2}i$']
offs = [(10,-14), (-6,10), (-6,-20)]
has = ['left', 'right', 'right']
cols = [ACCENT, '#d9534f', '#2e8b57']
P = [(np.cos(a), np.sin(a)) for a in ang]
tri = P + [P[0]]
ax.plot([p[0] for p in tri], [p[1] for p in tri], color=MUTED, lw=1.0, ls=(0,(3,2)))
for (x,y), lab, off, ha, col in zip(P, labs, offs, has, cols):
    ax.annotate('', xy=(x,y), xytext=(0,0),
                arrowprops=dict(arrowstyle='-|>', color=col, lw=1.6, mutation_scale=11))
    ax.plot([x],[y],'o',color=col,ms=6,zorder=5)
    ax.annotate(lab, (x,y), textcoords='offset points', xytext=off,
                fontsize=9.2, color=col, ha=ha)
aa = np.linspace(0, 2*np.pi/3, 50)
ax.plot(0.33*np.cos(aa), 0.33*np.sin(aa), color=INK, lw=0.9)
ax.annotate('$120^{\\circ}$', (0.30, 0.42), fontsize=9.0, color=INK)
ax.set_xlim(-2.35, 2.05); ax.set_ylim(-1.75, 1.60)
ax.set_aspect('equal'); ax.axis('off')
```

::: example Worked example 8.9
**Problem.** If $\omega$ is a complex cube root of unity, evaluate
$\left(1+\omega-\omega^{2}\right)^{2}$.

**Solution.** From $1+\omega+\omega^{2} = 0$ we get $1+\omega = -\omega^{2}$.
Substituting,

$$ 1+\omega-\omega^{2} = -\omega^{2}-\omega^{2} = -2\omega^{2} $$

$$ \left(1+\omega-\omega^{2}\right)^{2} = \left(-2\omega^{2}\right)^{2}
= 4\omega^{4} = 4\omega^{3}\cdot\omega = 4(1)\omega = 4\omega $$

With $\omega = \dfrac{-1+i\sqrt{3}}{2}$ this is $-2 + 2\sqrt{3}\,i$.
:::

## 8.4 Square root of a complex number

Every complex number has exactly two square roots, and they are negatives of each
other. To find them, use the equality of complex numbers.

::: derivation The method for $\sqrt{a+ib}$
Let $\sqrt{a+ib} = x+iy$ with $x$, $y$ real. Squaring,

$$ a + ib = (x+iy)^{2} = x^{2} - y^{2} + 2ixy $$

Equating real and imaginary parts gives two real equations:

$$ x^{2} - y^{2} = a \qquad\text{and}\qquad 2xy = b $$

Now use the identity $\left(x^{2}+y^{2}\right)^{2} = \left(x^{2}-y^{2}\right)^{2} + (2xy)^{2}$:

$$ x^{2}+y^{2} = \sqrt{a^{2}+b^{2}} \quad (\text{positive, since } x^{2}+y^{2} > 0) $$

Adding and subtracting this with $x^{2}-y^{2} = a$ gives $x^{2}$ and $y^{2}$, hence
$x$ and $y$. The sign of $2xy = b$ decides which sign pairing is allowed: if
$b > 0$, $x$ and $y$ have the **same** sign; if $b < 0$, **opposite** signs.
:::

::: tip A faster route in the exam
For small numbers, guess-and-fit is quicker: try $(x+iy)^{2} = a+ib$ with small
integer $x$, $y$ satisfying $2xy = b$. For $3+4i$, $2xy = 4$ means $xy = 2$, so
try $(2,1)$: $2^{2}-1^{2} = 3$. Done — the root is $\pm(2+i)$. Always state
**both** signs.
:::

::: example Worked example 8.10
**Problem.** Find the square roots of $3+4i$.

**Solution.** Let $\sqrt{3+4i} = x+iy$. Then

$$ x^{2}-y^{2} = 3, \qquad 2xy = 4 $$

$$ x^{2}+y^{2} = \sqrt{3^{2}+4^{2}} = \sqrt{25} = 5 $$

Adding to $x^{2}-y^{2} = 3$: $\;2x^{2} = 8$, so $x^{2} = 4$ and $x = \pm 2$.
Subtracting: $\;2y^{2} = 2$, so $y^{2} = 1$ and $y = \pm 1$.

Since $2xy = 4 > 0$, $x$ and $y$ take the **same** sign. Hence

$$ \sqrt{3+4i} = \pm(2+i) $$

**Check.** $(2+i)^{2} = 4 + 4i + i^{2} = 3+4i$. Correct.
:::

::: example Worked example 8.11
**Problem.** Find the square roots of $-15-8i$.

**Solution.** Let $\sqrt{-15-8i} = x+iy$. Then

$$ x^{2}-y^{2} = -15, \qquad 2xy = -8 $$

$$ x^{2}+y^{2} = \sqrt{(-15)^{2}+(-8)^{2}} = \sqrt{225+64} = \sqrt{289} = 17 $$

Adding: $2x^{2} = 2 \Rightarrow x = \pm 1$. Subtracting: $2y^{2} = 32
\Rightarrow y = \pm 4$.

Since $2xy = -8 < 0$, $x$ and $y$ take **opposite** signs:

$$ \sqrt{-15-8i} = \pm(1-4i) $$

**Check.** $(1-4i)^{2} = 1 - 8i + 16i^{2} = 1 - 8i - 16 = -15-8i$. Correct.
:::

::: example Worked example 8.12
**Problem.** Solve $x^{2} - 4x + 13 = 0$ over $\mathbb{C}$ and comment on the roots.

**Solution.** $D = 16 - 52 = -36 < 0$, so the roots are complex.

$$ x = \frac{4 \pm \sqrt{-36}}{2} = \frac{4 \pm 6i}{2} = 2 \pm 3i $$

The two roots $2+3i$ and $2-3i$ are conjugates — as they must be, because the
coefficients are real. Their sum is $4 = -b/a$ and their product is
$(2+3i)(2-3i) = 4+9 = 13 = c/a$, so the root–coefficient relations of Unit 7 hold
just as well in $\mathbb{C}$.
:::

## Chapter summary

- $i = \sqrt{-1}$, $i^{2} = -1$; powers of $i$ repeat with period $4$.
- $z = a+ib$; $a+ib = c+id$ exactly when $a = c$ and $b = d$.
- Divide by multiplying top and bottom by the conjugate of the denominator.
- Argand diagram: $z = a+ib$ is the point $(a,b)$; $|z| = \sqrt{a^{2}+b^{2}}$ and
  $\arg z = \theta$ with $\tan\theta = b/a$, fixed by the quadrant.
- Polar form $z = r(\cos\theta + i\sin\theta)$.
- $\bar{z} = a-ib$; $z\bar{z} = |z|^{2}$, $z+\bar{z} = 2\,\mathrm{Re}(z)$,
  $z-\bar{z} = 2i\,\mathrm{Im}(z)$, $\dfrac{1}{z} = \dfrac{\bar{z}}{|z|^{2}}$.
- $|z_1z_2| = |z_1||z_2|$, $|z_1/z_2| = \dfrac{|z_1|}{|z_2|}$,
  $|z_1+z_2| \le |z_1|+|z_2|$.
- Cube roots of unity: $1, \omega, \omega^{2}$ with $\omega^{3} = 1$ and
  $1+\omega+\omega^{2} = 0$.
- $\sqrt{a+ib} = x+iy$: solve $x^{2}-y^{2} = a$, $2xy = b$,
  $x^{2}+y^{2} = \sqrt{a^{2}+b^{2}}$; the sign of $b$ fixes the sign pairing.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The value of $i^{10}$ is <span class="marks">[1]</span>
   (a) $1$ (b) $-1$ (c) $i$ (d) $-i$
2. The modulus of $3+4i$ is <span class="marks">[1]</span>
   (a) $7$ (b) $5$ (c) $\sqrt{7}$ (d) $25$
3. The conjugate of $-2+5i$ is <span class="marks">[1]</span>
   (a) $2+5i$ (b) $-2-5i$ (c) $2-5i$ (d) $5-2i$
4. $z\bar{z}$ equals <span class="marks">[1]</span>
   (a) $|z|$ (b) $2\,\mathrm{Re}(z)$ (c) $|z|^{2}$ (d) $0$
5. If $\omega$ is a complex cube root of unity, then $1+\omega+\omega^{2}$ is <span class="marks">[1]</span>
   (a) $1$ (b) $0$ (c) $\omega$ (d) $3$
6. The argument of the complex number $-i$ is <span class="marks">[1]</span>
   (a) $0$ (b) $\dfrac{\pi}{2}$ (c) $-\dfrac{\pi}{2}$ (d) $\pi$

::: note Answers to Group A
**1.** (b) — $10 = 4(2)+2$, so $i^{10} = i^{2} = -1$.

**2.** (b) — $\sqrt{9+16} = 5$.

**3.** (b) — change the sign of the imaginary part only.

**4.** (c) — $(a+ib)(a-ib) = a^{2}+b^{2} = |z|^{2}$.

**5.** (b) — it is the sum of the roots-plus-one identity for $z^{3} = 1$.

**6.** (c) — $-i$ is the point $(0,-1)$, a quarter turn **clockwise**.
:::

**Group B — Short answer (5 marks each)**

1. Express $\dfrac{2+3i}{1-2i}$ in the form $a+ib$ and state its conjugate. <span class="marks">[5]</span>
2. Find the modulus and the principal argument of $z = -1-i$, and represent it on
   an Argand diagram. <span class="marks">[5]</span>
3. Find real $x$ and $y$ if $(x+iy)(2-i) = 7 + i$. <span class="marks">[5]</span>
4. Find the square roots of $-5+12i$. <span class="marks">[5]</span>
5. Show that $(2+3i)(2-3i) = |2+3i|^{2}$, and state the general property this
   illustrates. <span class="marks">[5]</span>
6. Find the square roots of $7+24i$. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Multiply by the conjugate $1+2i$:

$$ \frac{2+3i}{1-2i}\times\frac{1+2i}{1+2i} = \frac{2+4i+3i+6i^{2}}{1^{2}+2^{2}}
= \frac{2+7i-6}{5} = \frac{-4+7i}{5} $$

So $z = -\dfrac45 + \dfrac75 i$, and its conjugate is $-\dfrac45 - \dfrac75 i$.

**2.** $a = -1$, $b = -1$, so $|z| = \sqrt{1+1} = \sqrt{2}$.
$\alpha = \tan^{-1}\left(\dfrac{1}{1}\right) = \tan^{-1}1 = \dfrac{\pi}{4}$.
The point $(-1,-1)$ is in the **third quadrant**, so

$$ \arg z = -\left(\pi - \frac{\pi}{4}\right) = -\frac{3\pi}{4} = -135^{\circ} $$

On the Argand diagram, plot $(-1,-1)$: the vector points down-left at $45^{\circ}$
below the negative real axis, with length $\sqrt{2}$.

**3.** $(x+iy)(2-i) = 2x - xi + 2yi - yi^{2} = (2x+y) + i(2y-x)$. Equating parts,

$$ 2x + y = 7, \qquad -x + 2y = 1 $$

From the first, $y = 7-2x$. Substituting into the second,

$$ -x + 2(7-2x) = 1 \;\Longrightarrow\; -5x + 14 = 1 \;\Longrightarrow\; x = \frac{13}{5} $$

Then $y = 7 - \dfrac{26}{5} = \dfrac{9}{5}$.

$$ x = \frac{13}{5}, \qquad y = \frac{9}{5} $$

**Check.** $\left(\tfrac{13}{5}+\tfrac95 i\right)(2-i)
= \tfrac{26}{5} - \tfrac{13}{5}i + \tfrac{18}{5}i - \tfrac95 i^{2}
= \tfrac{26+9}{5} + \tfrac{5}{5}i = 7+i$. Correct.

**4.** Let $\sqrt{-5+12i} = x+iy$. Then $x^{2}-y^{2} = -5$ and $2xy = 12$, while

$$ x^{2}+y^{2} = \sqrt{25+144} = \sqrt{169} = 13 $$

Adding: $2x^{2} = 8 \Rightarrow x = \pm2$. Subtracting: $2y^{2} = 18
\Rightarrow y = \pm3$. As $2xy = 12 > 0$ the signs match, so

$$ \sqrt{-5+12i} = \pm(2+3i) \qquad\left[\text{check } (2+3i)^{2} = 4+12i-9 = -5+12i\right] $$

**5.** $(2+3i)(2-3i) = 4 - 6i + 6i - 9i^{2} = 4+9 = 13$, and
$|2+3i|^{2} = \left(\sqrt{4+9}\right)^{2} = 13$. They are equal.

This illustrates $z\bar{z} = |z|^{2}$: a complex number times its conjugate is the
square of its modulus, always a non-negative real number.

**6.** Let $\sqrt{7+24i} = x+iy$. Then $x^{2}-y^{2} = 7$, $2xy = 24$, and

$$ x^{2}+y^{2} = \sqrt{49+576} = \sqrt{625} = 25 $$

Adding: $2x^{2} = 32 \Rightarrow x = \pm4$. Subtracting: $2y^{2} = 18
\Rightarrow y = \pm3$. Since $2xy = 24 > 0$ the signs match:

$$ \sqrt{7+24i} = \pm(4+3i) \qquad\left[\text{check } (4+3i)^{2} = 16+24i-9 = 7+24i\right] $$
:::

**Group C — Long answer (8 marks each)**

1. (a) Define the modulus and the conjugate of a complex number. <span class="marks">[2]</span>
   (b) Prove that $z\bar{z} = |z|^{2}$ and that $|z_1z_2| = |z_1||z_2|$. <span class="marks">[4]</span>
   (c) Hence find $\dfrac{1}{3-2i}$ in the form $a+ib$. <span class="marks">[2]</span>
2. (a) Represent $z = 3+2i$ on an Argand diagram and find $|z|$ and $\arg z$. <span class="marks">[4]</span>
   (b) Express $z = -1+i\sqrt{3}$ in polar form and mark it, together with
   $\bar{z}$, on the same diagram. <span class="marks">[4]</span>
3. (a) Show that the cube roots of unity are $1$, $\omega$, $\omega^{2}$, where
   $\omega = \dfrac{-1+i\sqrt{3}}{2}$, and prove $1+\omega+\omega^{2} = 0$. <span class="marks">[4]</span>
   (b) Find the square roots of $-8-6i$. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** (a) For $z = a+ib$ ($a$, $b$ real), the modulus is
$|z| = \sqrt{a^{2}+b^{2}}$, the distance of the point $(a,b)$ from the origin; the
conjugate is $\bar{z} = a-ib$, the reflection of that point in the real axis.

(b) $z\bar{z} = (a+ib)(a-ib) = a^{2} - i^{2}b^{2} = a^{2}+b^{2} = |z|^{2}$.

For the product, let $z_1 = a+ib$ and $z_2 = c+id$. Then
$z_1z_2 = (ac-bd) + i(ad+bc)$, so

$$ |z_1z_2|^{2} = (ac-bd)^{2} + (ad+bc)^{2}
= a^{2}c^{2}+b^{2}d^{2}+a^{2}d^{2}+b^{2}c^{2} $$

$$ = \left(a^{2}+b^{2}\right)\left(c^{2}+d^{2}\right) = |z_1|^{2}|z_2|^{2} $$

Taking non-negative square roots, $|z_1z_2| = |z_1||z_2|$.

(c) $\dfrac{1}{3-2i} = \dfrac{\bar{z}}{|z|^{2}}$ with $z = 3-2i$, i.e.

$$ \frac{1}{3-2i} = \frac{3+2i}{9+4} = \frac{3}{13} + \frac{2}{13}\,i $$

**2.** (a) $z = 3+2i$ is the point $(3,2)$, in the first quadrant.

$$ |z| = \sqrt{9+4} = \sqrt{13} \approx 3.606 $$

$$ \arg z = \tan^{-1}\frac{2}{3} \approx 33.69^{\circ} \approx 0.588 \text{ rad} $$

(b) $z = -1+i\sqrt{3}$: $|z| = \sqrt{1+3} = 2$ and, since $(-1,\sqrt{3})$ is in the
second quadrant, $\arg z = \pi - \dfrac{\pi}{3} = \dfrac{2\pi}{3}$. Hence

$$ z = 2\left(\cos\frac{2\pi}{3} + i\sin\frac{2\pi}{3}\right) $$

$\bar{z} = -1-i\sqrt{3}$ is the reflection in the real axis: same modulus $2$, and
argument $-\dfrac{2\pi}{3}$.

**3.** (a) $z^{3} = 1 \Rightarrow z^{3}-1 = 0 \Rightarrow (z-1)\left(z^{2}+z+1\right) = 0$.
So either $z = 1$, or

$$ z = \frac{-1 \pm \sqrt{1-4}}{2} = \frac{-1 \pm i\sqrt{3}}{2} $$

Writing $\omega = \dfrac{-1+i\sqrt{3}}{2}$, a direct squaring gives
$\omega^{2} = \dfrac{-1-i\sqrt{3}}{2}$, which is the other root. So the three cube
roots are $1$, $\omega$, $\omega^{2}$.

Adding them: $1 + \dfrac{-1+i\sqrt{3}}{2} + \dfrac{-1-i\sqrt{3}}{2}
= 1 + \dfrac{-2}{2} = 0$. (Equivalently, $\omega$ and $\omega^{2}$ are the roots of
$z^{2}+z+1 = 0$, whose sum is $-1$.)

(b) Let $\sqrt{-8-6i} = x+iy$. Then $x^{2}-y^{2} = -8$, $2xy = -6$, and

$$ x^{2}+y^{2} = \sqrt{64+36} = \sqrt{100} = 10 $$

Adding: $2x^{2} = 2 \Rightarrow x = \pm1$. Subtracting: $2y^{2} = 18
\Rightarrow y = \pm3$. Since $2xy = -6 < 0$ the signs are opposite:

$$ \sqrt{-8-6i} = \pm(1-3i) $$

**Check.** $(1-3i)^{2} = 1 - 6i + 9i^{2} = 1 - 6i - 9 = -8-6i$. Correct.
:::
