---
subject: Mathematics
grade: 12
unit: 3
title: Complex Numbers
hours: 8
area: Algebra
---

A complex number $z = x + iy$ has two parts, so it needs two pieces of
information to pin it down. Writing it as $x + iy$ answers "how far right, how
far up". Writing it in **polar form** answers "how far from the origin, and in
which direction" — and that second description turns multiplication into
addition of angles. Once that is seen, De Moivre's theorem makes powers and
roots of complex numbers as easy as multiplying angles by $n$, and Euler's
formula ties the whole subject to the exponential series of Unit 2.

::: key What the exam asks
Convert between $x + iy$ and $r(\cos\theta + i\sin\theta)$ with the **correct
quadrant** for $\theta$; use De Moivre to compute a high power such as
$(1+i)^{10}$; find the $n$ $n^{\text{th}}$ roots of a complex number and mark
them on an Argand diagram; prove and apply the properties of the cube roots of
unity $1, \omega, \omega^{2}$; and state Euler's formula $e^{i\theta} =
\cos\theta + i\sin\theta$.
:::

## 3.1 Polar form of a complex number

Plot $z = x + iy$ as the point $(x, y)$. This picture is the **Argand diagram**:
the horizontal axis is the real axis, the vertical axis is the imaginary axis.

::: definition Modulus and argument
For $z = x + iy$ with $z \neq 0$:

- The **modulus** $r = |z| = \sqrt{x^{2} + y^{2}}$ is the distance $OP$ from the
  origin. It is real and positive.
- The **argument** (or **amplitude**) $\theta = \arg z$ is the angle $POX$
  measured from the positive real axis, anticlockwise positive.

The argument is only fixed up to multiples of $2\pi$. The value in
$-\pi < \theta \leq \pi$ is the **principal argument**, and "the" argument
always means this one unless the question says otherwise.
:::

```figure caption="Argand diagram for $z = 3 + 4i$: the modulus $r = 5$ is the distance from $O$, and the argument $\theta = 53.13^{\circ}$ is measured anticlockwise from the positive real axis. The conjugate $\overline{z} = 3 - 4i$ is the mirror image in the real axis, with the same modulus and argument $-\theta$."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Arc
fig, ax = plt.subplots(figsize=(4.4,4.0))
x0, y0 = 3.0, 4.0
ax.axhline(0, color=INK, lw=0.9)
ax.axvline(0, color=INK, lw=0.9)
ax.plot([0,x0],[0,y0], color=ACCENT, lw=1.8, zorder=3)
ax.plot([x0],[y0], 'o', color=ACCENT, ms=6, zorder=4)
ax.plot([0,x0],[0,-y0], color=SERIES[2], lw=1.4, ls='--', zorder=3)
ax.plot([x0],[-y0], 'o', color=SERIES[2], ms=6, zorder=4)
ax.plot([x0,x0],[0,y0], ls=':', color=MUTED, lw=1.0)
ax.plot([0,x0],[y0,y0], ls=':', color=MUTED, lw=1.0)
ax.add_patch(Arc((0,0), 2.4, 2.4, theta1=0, theta2=53.13,
                 color=SERIES[4], lw=1.3))
ax.text(1.42, 0.44, r'$\theta$', color=SERIES[4], fontsize=11)
ax.text(3.22, 4.18, r'$P(3,\,4) \rightarrow z = 3+4i$', color=ACCENT, fontsize=8.6)
ax.text(3.22, -4.42, r'$\overline{z} = 3-4i$', color=SERIES[2], fontsize=8.6)
ax.text(1.28, 2.30, r'$r = 5$', color=ACCENT, fontsize=9.0, rotation=53)
ax.text(0.16, 4.20, r'$y = r\sin\theta = 4$', color=MUTED, fontsize=8.2)
ax.text(3.10, 1.30, r'$x = r\cos\theta$', color=MUTED, fontsize=8.2, rotation=90)
ax.text(5.35, 0.22, 'Re', color=INK, fontsize=8.6)
ax.text(0.14, 5.30, 'Im', color=INK, fontsize=8.6)
ax.text(-0.42, -0.42, r'$O$', color=INK, fontsize=9.0)
ax.set_xlim(-1.5, 5.8); ax.set_ylim(-5.2, 5.6)
ax.set_aspect('equal')
ax.axis('off')
```

From the right-angled triangle in the figure, $x = r\cos\theta$ and
$y = r\sin\theta$. Substituting these into $z = x + iy$ gives the polar form.

::: key Polar (modulus–argument) form
$$ z = x + iy = r(\cos\theta + i\sin\theta) $$
$$ r = |z| = \sqrt{x^{2}+y^{2}}, \qquad \tan\theta = \frac{y}{x} $$
Reverse direction: $x = r\cos\theta$, $y = r\sin\theta$.
:::

::: caution $\tan^{-1}(y/x)$ alone gives the wrong quadrant
A calculator returns $\tan^{-1}$ between $-90^{\circ}$ and $90^{\circ}$, so it
cannot tell $-1-i$ from $1+i$. **Always plot the point first.** Let
$\alpha = \tan^{-1}\left(\dfrac{y}{x}\right)$ taken as a positive acute angle.
Then:

| Position of $(x, y)$ | Signs | Principal argument $\theta$ |
|---|---|---|
| First quadrant | $x>0,\ y>0$ | $\alpha$ |
| Second quadrant | $x<0,\ y>0$ | $\pi - \alpha$ |
| Third quadrant | $x<0,\ y<0$ | $-(\pi - \alpha)$ |
| Fourth quadrant | $x>0,\ y<0$ | $-\alpha$ |

On the axes, read the argument straight off the picture: $\arg(5) = 0$,
$\arg(3i) = \pi/2$, $\arg(-2) = \pi$, $\arg(-4i) = -\pi/2$.
:::

::: example Worked example 3.1
**Problem.** Express in polar form, using principal arguments: (a) $1 + i\sqrt{3}$
(b) $-1 + i$ (c) $-\sqrt{3} - i$ (d) $1 - i$.

**Solution.** In each case find $r$, find the acute angle $\alpha$, then fix the
quadrant.

(a) $r = \sqrt{1 + 3} = 2$; $\tan\alpha = \sqrt{3}/1$ so $\alpha = 60^{\circ}$.
The point $(1, \sqrt{3})$ is in the first quadrant, so $\theta = 60^{\circ}$:

$$ 1 + i\sqrt{3} = 2\left(\cos 60^{\circ} + i\sin 60^{\circ}\right) $$

(b) $r = \sqrt{1+1} = \sqrt{2}$; $\tan\alpha = 1/1$ so $\alpha = 45^{\circ}$. The
point $(-1, 1)$ is in the second quadrant, so
$\theta = 180^{\circ} - 45^{\circ} = 135^{\circ}$:

$$ -1 + i = \sqrt{2}\left(\cos 135^{\circ} + i\sin 135^{\circ}\right) $$

(c) $r = \sqrt{3+1} = 2$; $\tan\alpha = 1/\sqrt{3}$ so $\alpha = 30^{\circ}$. The
point $(-\sqrt{3}, -1)$ is in the third quadrant, so
$\theta = -(180^{\circ} - 30^{\circ}) = -150^{\circ}$:

$$ -\sqrt{3} - i = 2\left[\cos(-150^{\circ}) + i\sin(-150^{\circ})\right] $$

(d) $r = \sqrt{2}$, $\alpha = 45^{\circ}$, fourth quadrant, so
$\theta = -45^{\circ}$:

$$ 1 - i = \sqrt{2}\left[\cos(-45^{\circ}) + i\sin(-45^{\circ})\right] $$

Check (c): $2\cos(-150^{\circ}) = 2(-\sqrt{3}/2) = -\sqrt{3}$ and
$2\sin(-150^{\circ}) = 2(-1/2) = -1$. Correct.
:::

### Multiplication and division in polar form

::: derivation Product and quotient of two complex numbers in polar form
Let $z_{1} = r_{1}(\cos\theta_{1} + i\sin\theta_{1})$ and
$z_{2} = r_{2}(\cos\theta_{2} + i\sin\theta_{2})$. Multiply:

$$ z_{1}z_{2} = r_{1}r_{2}\left(\cos\theta_{1} + i\sin\theta_{1}\right)
\left(\cos\theta_{2} + i\sin\theta_{2}\right) $$

Expand the bracket and use $i^{2} = -1$:

$$ = r_{1}r_{2}\left[\left(\cos\theta_{1}\cos\theta_{2}
- \sin\theta_{1}\sin\theta_{2}\right)
+ i\left(\sin\theta_{1}\cos\theta_{2} + \cos\theta_{1}\sin\theta_{2}\right)\right] $$

The two brackets are exactly the compound-angle formulas for
$\cos(\theta_{1}+\theta_{2})$ and $\sin(\theta_{1}+\theta_{2})$, so

$$ z_{1}z_{2} = r_{1}r_{2}\left[\cos(\theta_{1}+\theta_{2})
+ i\sin(\theta_{1}+\theta_{2})\right] $$

For the quotient, multiply numerator and denominator by
$\cos\theta_{2} - i\sin\theta_{2}$; the denominator becomes
$\cos^{2}\theta_{2} + \sin^{2}\theta_{2} = 1$, and the same compound-angle step
with $-\theta_{2}$ gives

$$ \frac{z_{1}}{z_{2}} = \frac{r_{1}}{r_{2}}
\left[\cos(\theta_{1}-\theta_{2}) + i\sin(\theta_{1}-\theta_{2})\right] $$

In words: **multiply the moduli, add the arguments; divide the moduli, subtract
the arguments.** $\blacksquare$
:::

```figure caption="Multiplying is rotating and scaling. With $z_{1} = 2(\cos 30^{\circ} + i\sin 30^{\circ})$ and $z_{2} = 1.5(\cos 45^{\circ} + i\sin 45^{\circ})$, the product has modulus $2 \times 1.5 = 3$ and argument $30^{\circ} + 45^{\circ} = 75^{\circ}$."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Arc
fig, ax = plt.subplots(figsize=(4.6,3.3))
th = np.linspace(0, 2*np.pi, 300)
ax.plot(np.cos(th), np.sin(th), color=GRID, lw=1.0)
ax.axhline(0, color=INK, lw=0.9); ax.axvline(0, color=INK, lw=0.9)
def vec(r, d, col, lab, dx, dy, fs=8.4):
    a = np.radians(d)
    ax.annotate('', xy=(r*np.cos(a), r*np.sin(a)), xytext=(0,0),
                arrowprops=dict(arrowstyle='-|>', color=col, lw=1.6,
                                shrinkA=0, shrinkB=0))
    ax.text(r*np.cos(a)+dx, r*np.sin(a)+dy, lab, color=col, fontsize=fs)
vec(2, 30, SERIES[0], r'$z_1$  (r=2, 30$^{\circ}$)', 0.06, -0.30)
vec(1.5, 45, SERIES[1], r'$z_2$  (r=1.5, 45$^{\circ}$)', -0.60, 0.20)
vec(3, 75, SERIES[4], r'$z_1z_2$  (r=3, 75$^{\circ}$)', -0.30, 0.22)
ax.add_patch(Arc((0,0), 1.1, 1.1, theta1=30, theta2=75, color=MUTED, lw=1.1,
                 ls='--'))
ax.text(-1.55, 0.80, 'turn by 45$^{\\circ}$', color=MUTED, fontsize=7.8)
ax.text(1.02, -0.30, 'unit circle', color=MUTED, fontsize=7.6)
ax.set_xlim(-1.7, 3.3); ax.set_ylim(-1.3, 3.5)
ax.set_aspect('equal'); ax.axis('off')
```

::: example Worked example 3.2
**Problem.** Find the modulus and principal argument of
$z = \dfrac{1+i}{1 - i\sqrt{3}}$, and write $z$ in polar form.

**Solution.** Do the numerator and denominator separately.

Numerator: $|1+i| = \sqrt{2}$, $\arg(1+i) = 45^{\circ}$ (first quadrant).

Denominator: $|1 - i\sqrt{3}| = \sqrt{1+3} = 2$; $\alpha = 60^{\circ}$ and
$(1, -\sqrt{3})$ is in the fourth quadrant, so $\arg = -60^{\circ}$.

Divide the moduli and subtract the arguments:

$$ |z| = \frac{\sqrt{2}}{2} = \frac{1}{\sqrt{2}}, \qquad
\arg z = 45^{\circ} - (-60^{\circ}) = 105^{\circ} $$

Since $105^{\circ}$ lies in $(-180^{\circ}, 180^{\circ}]$ it is already the
principal value, and $105^{\circ} = \dfrac{7\pi}{12}$. Hence

$$ z = \frac{1}{\sqrt{2}}\left(\cos 105^{\circ} + i\sin 105^{\circ}\right) $$
:::

::: tip Useful modulus facts
$|z_{1}z_{2}| = |z_{1}||z_{2}|$, $\left|\dfrac{z_{1}}{z_{2}}\right| =
\dfrac{|z_{1}|}{|z_{2}|}$, $|z^{n}| = |z|^{n}$ and
$z\overline{z} = |z|^{2}$. These let you find a modulus without ever
rationalising the fraction.
:::

## 3.2 De Moivre's theorem and its application to roots

::: key De Moivre's theorem
For every $n$,
$$ \left(\cos\theta + i\sin\theta\right)^{n} = \cos n\theta + i\sin n\theta $$
and more generally
$$ \left[r(\cos\theta + i\sin\theta)\right]^{n}
= r^{n}\left(\cos n\theta + i\sin n\theta\right) $$
If $n$ is an integer the right side is the only value; if $n$ is a rational
$p/q$ in lowest terms, the left side has $q$ values.
:::

::: derivation De Moivre's theorem
**Case 1: $n$ a positive integer — induction.** Let $P(n)$ be the statement
$(\cos\theta + i\sin\theta)^{n} = \cos n\theta + i\sin n\theta$.

*Base step.* $P(1)$ reads $\cos\theta + i\sin\theta = \cos\theta + i\sin\theta$,
which is true.

*Inductive step.* Assume $P(k)$ holds, i.e.
$(\cos\theta + i\sin\theta)^{k} = \cos k\theta + i\sin k\theta$. Multiply both
sides by $(\cos\theta + i\sin\theta)$:

$$ \left(\cos\theta + i\sin\theta\right)^{k+1}
= \left(\cos k\theta + i\sin k\theta\right)\left(\cos\theta + i\sin\theta\right) $$

By the product rule of §3.1 (moduli $1$, arguments $k\theta$ and $\theta$), the
right side is $\cos(k\theta + \theta) + i\sin(k\theta+\theta)$, that is

$$ = \cos(k+1)\theta + i\sin(k+1)\theta $$

which is $P(k+1)$. Since $P(1)$ is true and $P(k) \Rightarrow P(k+1)$, by
induction $P(n)$ is true for all positive integers $n$.

**Case 2: $n = 0$.** Both sides equal $1$.

**Case 3: $n$ a negative integer,** say $n = -m$ with $m > 0$. Then

$$ \left(\cos\theta+i\sin\theta\right)^{-m}
= \frac{1}{\cos m\theta + i\sin m\theta} $$

Multiply top and bottom by $\cos m\theta - i\sin m\theta$; the denominator
becomes $\cos^{2}m\theta + \sin^{2}m\theta = 1$, so

$$ = \cos m\theta - i\sin m\theta = \cos(-m\theta) + i\sin(-m\theta) $$

using $\cos(-A) = \cos A$, $\sin(-A) = -\sin A$. So the theorem holds for
$n = -m$ too.

**Case 4: $n = p/q$ rational.** Put
$w = \cos\dfrac{\theta}{q} + i\sin\dfrac{\theta}{q}$. By Case 1,
$w^{q} = \cos\theta + i\sin\theta$, so $w$ is one $q^{\text{th}}$ root of
$\cos\theta + i\sin\theta$; raising $w$ to the power $p$ gives
$\cos\dfrac{p\theta}{q} + i\sin\dfrac{p\theta}{q}$ as **one** of the values of
$(\cos\theta+i\sin\theta)^{p/q}$. $\blacksquare$
:::

```figure caption="De Moivre's theorem geometrically: each power of $z$ turns the point through a further $\theta$ and multiplies its distance from $O$ by $r$. Here $z = 1.18(\cos 32^{\circ} + i\sin 32^{\circ})$, so $z^{4}$ sits at angle $128^{\circ}$ and radius $1.18^{4} = 1.94$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,3.2))
r0, d0 = 1.18, 32.0
ax.axhline(0, color=INK, lw=0.9); ax.axvline(0, color=INK, lw=0.9)
t = np.linspace(0, 2*np.pi, 300)
ax.plot(np.cos(t), np.sin(t), color=GRID, lw=1.0)
ts = np.linspace(0, np.radians(d0*4), 400)
ax.plot(r0**(np.degrees(ts)/d0)*np.cos(ts), r0**(np.degrees(ts)/d0)*np.sin(ts),
        color=MUTED, lw=0.9, ls=':')
for k in range(1, 5):
    a = np.radians(d0*k); r = r0**k
    x, y = r*np.cos(a), r*np.sin(a)
    ax.annotate('', xy=(x,y), xytext=(0,0),
                arrowprops=dict(arrowstyle='-|>', color=SERIES[k-1], lw=1.4,
                                shrinkA=0, shrinkB=0))
    lab = '$z$' if k == 1 else '$z^{%d}$' % k
    ax.text(x + (0.10 if x > -0.4 else -0.34), y + 0.13, lab,
            color=SERIES[k-1], fontsize=9.0)
ax.text(0.98, -0.28, 'unit circle', color=MUTED, fontsize=7.6)
ax.text(-2.15, -0.95, 'each step:\nangle $+32^{\\circ}$, radius $\\times 1.18$',
        color=INK, fontsize=8.0)
ax.set_xlim(-2.25, 1.9); ax.set_ylim(-1.5, 2.1)
ax.set_aspect('equal'); ax.axis('off')
```

::: example Worked example 3.3
**Problem.** Evaluate $(1+i)^{10}$.

**Solution.** Expanding by the binomial theorem would take eleven terms. Use
polar form instead: $|1+i| = \sqrt{2}$ and $\arg(1+i) = 45^{\circ}$, so

$$ 1 + i = \sqrt{2}\left(\cos 45^{\circ} + i\sin 45^{\circ}\right) $$

Apply De Moivre with $n = 10$:

$$ (1+i)^{10} = \left(\sqrt{2}\right)^{10}
\left(\cos 450^{\circ} + i\sin 450^{\circ}\right) $$

Now $\left(\sqrt{2}\right)^{10} = 2^{5} = 32$, and
$450^{\circ} = 360^{\circ} + 90^{\circ}$, so
$\cos 450^{\circ} = \cos 90^{\circ} = 0$ and $\sin 450^{\circ} = 1$:

$$ (1+i)^{10} = 32(0 + i) = 32i $$
:::

::: example Worked example 3.4
**Problem.** Show that $\left(\sqrt{3} + i\right)^{7} = -64\left(\sqrt{3}+i\right)$.

**Solution.** $|\sqrt{3}+i| = \sqrt{3+1} = 2$ and
$\tan\alpha = 1/\sqrt{3}$, first quadrant, so $\arg = 30^{\circ}$:

$$ \sqrt{3} + i = 2\left(\cos 30^{\circ} + i\sin 30^{\circ}\right) $$

$$ \left(\sqrt{3}+i\right)^{7} = 2^{7}\left(\cos 210^{\circ} + i\sin 210^{\circ}\right)
= 128\left(-\frac{\sqrt{3}}{2} - \frac{i}{2}\right) $$

$$ = -64\sqrt{3} - 64i = -64\left(\sqrt{3} + i\right) $$

as required. (Note $210^{\circ}$ is in the third quadrant, where both cosine and
sine are negative — a sign slip here is the commonest lost mark.)
:::

::: example Worked example 3.5
**Problem.** Use De Moivre's theorem to prove
$\cos 3\theta = 4\cos^{3}\theta - 3\cos\theta$ and
$\sin 3\theta = 3\sin\theta - 4\sin^{3}\theta$.

**Solution.** By De Moivre with $n = 3$:

$$ \cos 3\theta + i\sin 3\theta = \left(\cos\theta + i\sin\theta\right)^{3} $$

Expand the right side by the binomial theorem, writing $c = \cos\theta$,
$s = \sin\theta$:

$$ = c^{3} + 3c^{2}(is) + 3c(is)^{2} + (is)^{3}
= c^{3} + 3ic^{2}s - 3cs^{2} - is^{3} $$

using $i^{2} = -1$, $i^{3} = -i$. Group real and imaginary parts:

$$ \cos 3\theta + i\sin 3\theta
= \left(c^{3} - 3cs^{2}\right) + i\left(3c^{2}s - s^{3}\right) $$

Two complex numbers are equal only if their real parts and imaginary parts match
separately, so

$$ \cos 3\theta = c^{3} - 3cs^{2} = c^{3} - 3c\left(1-c^{2}\right)
= 4c^{3} - 3c $$

$$ \sin 3\theta = 3c^{2}s - s^{3} = 3\left(1-s^{2}\right)s - s^{3}
= 3s - 4s^{3} $$

where $s^{2} = 1 - c^{2}$ and $c^{2} = 1 - s^{2}$ were used to remove the
unwanted letter. $\blacksquare$
:::

### Application to roots

::: derivation The $n$ $n^{\text{th}}$ roots of a complex number
To solve $w^{n} = z$ where $z = r(\cos\theta + i\sin\theta)$, first note that
adding $2k\pi$ to the argument does not change $z$ at all:

$$ z = r\left[\cos(\theta + 2k\pi) + i\sin(\theta+2k\pi)\right],
\qquad k \in \mathbb{Z} $$

This is the whole trick: the *same* number has infinitely many arguments, and
taking the $n^{\text{th}}$ root divides each of them by $n$, which spreads them
apart. Applying De Moivre with index $1/n$,

$$ w = z^{1/n} = r^{1/n}\left[\cos\frac{\theta+2k\pi}{n}
+ i\sin\frac{\theta+2k\pi}{n}\right] $$

Every root has the same modulus $r^{1/n}$ (the real positive $n^{\text{th}}$
root of $r$), and the arguments differ by $\dfrac{2\pi}{n}$ as $k$ increases by
$1$. After $n$ steps the argument has grown by $2\pi$ and we are back at the
first root, so exactly

$$ k = 0, 1, 2, \ldots, n-1 $$

give **$n$ distinct roots**. Because they share a modulus and are equally
spaced in angle, they lie on a circle of radius $r^{1/n}$ at the vertices of a
**regular $n$-gon**. $\blacksquare$
:::

::: example Worked example 3.6
**Problem.** Find the cube roots of $8i$ and show them on an Argand diagram.

**Solution.** Write $8i$ in polar form: $|8i| = 8$ and the point $(0, 8)$ is on
the positive imaginary axis, so $\arg(8i) = 90^{\circ}$. Including the general
argument,

$$ 8i = 8\left[\cos\left(90^{\circ} + 360^{\circ}k\right)
+ i\sin\left(90^{\circ}+360^{\circ}k\right)\right] $$

Take the cube root, so the modulus becomes $8^{1/3} = 2$ and each argument is
divided by $3$:

$$ (8i)^{1/3} = 2\left[\cos\frac{90^{\circ}+360^{\circ}k}{3}
+ i\sin\frac{90^{\circ}+360^{\circ}k}{3}\right],\qquad k = 0, 1, 2 $$

The three arguments are $30^{\circ}$, $150^{\circ}$ and $270^{\circ}$ — spaced
$120^{\circ}$ apart, as expected:

$$ k=0:\quad 2\left(\cos 30^{\circ} + i\sin 30^{\circ}\right)
= 2\left(\frac{\sqrt{3}}{2} + \frac{i}{2}\right) = \sqrt{3} + i $$

$$ k=1:\quad 2\left(\cos 150^{\circ} + i\sin 150^{\circ}\right)
= 2\left(-\frac{\sqrt{3}}{2} + \frac{i}{2}\right) = -\sqrt{3} + i $$

$$ k=2:\quad 2\left(\cos 270^{\circ} + i\sin 270^{\circ}\right)
= 2(0 - i) = -2i $$

**Check.** $\left(\sqrt{3}+i\right)^{3} = 2^{3}\left(\cos 90^{\circ} +
i\sin 90^{\circ}\right) = 8i$. Also the three roots sum to
$(\sqrt{3} - \sqrt{3} + 0) + i(1 + 1 - 2) = 0$, which it must be, since the
coefficient of $w^{2}$ in $w^{3} - 8i = 0$ is zero.
:::

```figure caption="The three cube roots of $8i$: all at distance $8^{1/3} = 2$ from $O$, at arguments $30^{\circ}$, $150^{\circ}$ and $270^{\circ}$ — the vertices of an equilateral triangle."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.2,3.4))
t = np.linspace(0, 2*np.pi, 400)
ax.plot(2*np.cos(t), 2*np.sin(t), color=GRID, lw=1.1)
ax.axhline(0, color=INK, lw=0.9); ax.axvline(0, color=INK, lw=0.9)
degs = [30, 150, 270]
labs = [r'$\sqrt{3}+i$', r'$-\sqrt{3}+i$', r'$-2i$']
offs = [(0.18, 0.14), (-1.28, 0.14), (0.16, -0.30)]
pts = []
for d, lab, off in zip(degs, labs, offs):
    a = np.radians(d); x, y = 2*np.cos(a), 2*np.sin(a)
    pts.append((x, y))
    ax.plot([0, x], [0, y], color=MUTED, lw=0.9, ls=':')
    ax.plot([x], [y], 'o', color=ACCENT, ms=7, zorder=4)
    ax.text(x+off[0], y+off[1], lab, color=ACCENT, fontsize=9.0)
    ox, oy = {30: (0.04, -0.30), 150: (-0.10, 0.14), 270: (0.14, 0.10)}[d]
    ax.text(x*0.55+ox, y*0.55+oy, '%d$^{\\circ}$' % d, color=MUTED,
            fontsize=7.6)
pts.append(pts[0])
ax.plot([p[0] for p in pts], [p[1] for p in pts], color=SERIES[3], lw=1.2)
ax.text(-2.55, 2.30, 'radius $= 2$', color=MUTED, fontsize=8.0)
ax.set_xlim(-2.7, 2.7); ax.set_ylim(-2.6, 2.6)
ax.set_aspect('equal'); ax.axis('off')
```

::: example Worked example 3.7
**Problem.** Solve $z^{4} + 16 = 0$.

**Solution.** The equation is $z^{4} = -16$. Now $|-16| = 16$ and
$\arg(-16) = 180^{\circ}$, so

$$ z^{4} = 16\left[\cos\left(180^{\circ}+360^{\circ}k\right)
+ i\sin\left(180^{\circ}+360^{\circ}k\right)\right] $$

$$ z = 16^{1/4}\left[\cos\frac{180^{\circ}+360^{\circ}k}{4}
+ i\sin\frac{180^{\circ}+360^{\circ}k}{4}\right],\qquad k = 0,1,2,3 $$

Here $16^{1/4} = 2$ and the arguments are $45^{\circ}, 135^{\circ},
225^{\circ}, 315^{\circ}$, each $90^{\circ}$ apart. Since
$\cos 45^{\circ} = \sin 45^{\circ} = 1/\sqrt{2}$, every root has both coordinates
of size $2/\sqrt{2} = \sqrt{2}$:

$$ z = \sqrt{2} + i\sqrt{2},\quad -\sqrt{2} + i\sqrt{2},\quad
-\sqrt{2} - i\sqrt{2},\quad \sqrt{2} - i\sqrt{2} $$

That is $z = \pm\sqrt{2} \pm i\sqrt{2}$, the four vertices of a square of
circumradius $2$. **Check:** $(\sqrt{2}+i\sqrt{2})^{2} = 2 + 4i + 2i^{2} = 4i$, and
$(4i)^{2} = -16$.
:::

### The $n^{\text{th}}$ roots of unity

Putting $z = 1$, so $r = 1$ and $\theta = 0$, gives the roots of $w^{n} = 1$:

::: key $n^{\text{th}}$ roots of unity
$$ w_{k} = \cos\frac{2k\pi}{n} + i\sin\frac{2k\pi}{n},
\qquad k = 0, 1, \ldots, n-1 $$
Writing $w = \cos\dfrac{2\pi}{n} + i\sin\dfrac{2\pi}{n}$, the roots are
$1, w, w^{2}, \ldots, w^{n-1}$: all on the **unit circle**, at the vertices of a
regular $n$-gon with one vertex at $1$.

- Their **sum is $0$** (for $n \geq 2$).
- Their **product is $(-1)^{n+1}$**.
:::

::: derivation Sum and product of the $n^{\text{th}}$ roots of unity
The roots are the solutions of $w^{n} - 1 = 0$, so

$$ w^{n} - 1 = (w - w_{0})(w - w_{1})\cdots(w - w_{n-1}) $$

Comparing the coefficient of $w^{n-1}$ on both sides: on the left it is $0$, on
the right it is $-(w_{0} + w_{1} + \cdots + w_{n-1})$. Hence the sum of the
roots is $0$.

Comparing constant terms: the left side gives $-1$, the right side gives
$(-1)^{n}w_{0}w_{1}\cdots w_{n-1}$. So the product is
$\dfrac{-1}{(-1)^{n}} = (-1)^{n+1}$.

The sum can also be seen as a geometric series: with
$w = \cos\dfrac{2\pi}{n} + i\sin\dfrac{2\pi}{n} \neq 1$,

$$ 1 + w + w^{2} + \cdots + w^{n-1} = \frac{w^{n}-1}{w-1} = \frac{0}{w-1} = 0 $$

since $w^{n} = \cos 2\pi + i\sin 2\pi = 1$. $\blacksquare$
:::

```figure caption="The $n^{\text{th}}$ roots of unity for $n = 3, 4, 5, 6$. All lie on the unit circle at spacing $360^{\circ}/n$, starting at $1$, so they form a regular $n$-gon; their vectors add head-to-tail to zero."
import numpy as np, matplotlib.pyplot as plt
fig, axes = plt.subplots(2, 2, figsize=(4.8,4.4))
t = np.linspace(0, 2*np.pi, 400)
for ax, n, col in zip(axes.ravel(), [3,4,5,6], [SERIES[0],SERIES[1],SERIES[2],SERIES[3]]):
    ax.plot(np.cos(t), np.sin(t), color=GRID, lw=1.0)
    ax.axhline(0, color=INK, lw=0.7); ax.axvline(0, color=INK, lw=0.7)
    a = 2*np.pi*np.arange(n)/n
    xs, ys = np.cos(a), np.sin(a)
    ax.fill(xs, ys, color=col, alpha=0.13)
    ax.plot(np.append(xs, xs[0]), np.append(ys, ys[0]), color=col, lw=1.3)
    ax.plot(xs, ys, 'o', color=col, ms=5, zorder=4)
    ax.text(1.12, -0.02, '1', color=INK, fontsize=8.0, va='center')
    ax.set_title('$n = %d$   (spacing $%d^{\\circ}$)' % (n, 360//n),
                 fontsize=8.4, color=INK, pad=3)
    ax.set_xlim(-1.45, 1.45); ax.set_ylim(-1.45, 1.45)
    ax.set_aspect('equal'); ax.axis('off')
fig.subplots_adjust(hspace=0.16, wspace=0.02)
```

::: example Worked example 3.8
**Problem.** Find the five fifth roots of $32$ and show that their sum is zero.

**Solution.** $32$ is real and positive, so $|32| = 32$ and $\arg 32 = 0$:

$$ z = 32^{1/5}\left[\cos\frac{0 + 360^{\circ}k}{5}
+ i\sin\frac{0+360^{\circ}k}{5}\right],\qquad k = 0,1,2,3,4 $$

Since $32^{1/5} = 2$ and $360^{\circ}/5 = 72^{\circ}$, the roots are

$$ z = 2\left(\cos 72^{\circ}k + i\sin 72^{\circ}k\right),
\qquad k = 0,1,2,3,4 $$

that is $2$, $2(\cos 72^{\circ} + i\sin 72^{\circ})$,
$2(\cos 144^{\circ} + i\sin 144^{\circ})$,
$2(\cos 216^{\circ} + i\sin 216^{\circ})$ and
$2(\cos 288^{\circ} + i\sin 288^{\circ})$ — five points on a circle of radius
$2$, forming a regular pentagon.

Every root is $2w^{k}$ where $w = \cos 72^{\circ} + i\sin 72^{\circ}$ is a
fifth root of unity, so the sum is

$$ 2\left(1 + w + w^{2} + w^{3} + w^{4}\right) = 2 \cdot \frac{w^{5}-1}{w-1} = 0 $$

because $w^{5} = \cos 360^{\circ} + i\sin 360^{\circ} = 1$. Numerically the
roots are $2$, $0.618 \pm 1.902i$ and $-1.618 \pm 1.176i$, and
$2 + 2(0.618) + 2(-1.618) = 0$ — the imaginary parts cancel in conjugate pairs.
:::

## 3.3 Properties of cube roots of unity

Put $n = 3$ in the work above, or simply factorise:

::: derivation The cube roots of unity
Solve $z^{3} = 1$, i.e. $z^{3} - 1 = 0$. Factorising the difference of cubes,

$$ (z-1)\left(z^{2}+z+1\right) = 0 $$

So either $z = 1$, or $z^{2}+z+1 = 0$, which by the quadratic formula gives

$$ z = \frac{-1 \pm \sqrt{1-4}}{2} = \frac{-1 \pm i\sqrt{3}}{2} $$

The three cube roots of unity are therefore

$$ 1, \qquad \omega = \frac{-1+i\sqrt{3}}{2}, \qquad
\omega^{2} = \frac{-1-i\sqrt{3}}{2} $$

To see that the third root really is the square of the second:

$$ \left(\frac{-1+i\sqrt{3}}{2}\right)^{2} = \frac{1 - 2i\sqrt{3} + 3i^{2}}{4}
= \frac{-2-2i\sqrt{3}}{4} = \frac{-1-i\sqrt{3}}{2} $$

Each has modulus $\sqrt{\frac14 + \frac34} = 1$, and their arguments are
$0^{\circ}$, $120^{\circ}$ and $-120^{\circ}$. $\blacksquare$
:::

::: key Properties of the cube roots of unity
If $\omega$ is a complex (non-real) cube root of unity, then

1. $\omega^{3} = 1$, and generally $\omega^{3m} = 1$ for any integer $m$ — so
   reduce any index **modulo 3**.
2. $1 + \omega + \omega^{2} = 0$ (sum of the roots of $z^{3}-1=0$). Hence
   $1 + \omega = -\omega^{2}$, $1 + \omega^{2} = -\omega$ and
   $\omega + \omega^{2} = -1$.
3. $\omega$ and $\omega^{2}$ are conjugates, and
   $\omega \cdot \omega^{2} = \omega^{3} = 1$, so
   $\omega^{2} = \dfrac{1}{\omega} = \overline{\omega}$.
4. The three roots are the vertices of an equilateral triangle inscribed in the
   unit circle.
5. $a^{3}+b^{3}+c^{3}-3abc
   = (a+b+c)\left(a+b\omega+c\omega^{2}\right)\left(a+b\omega^{2}+c\omega\right)$.
:::

```figure caption="The cube roots of unity. Left: $1$, $\omega$ and $\omega^{2}$ on the unit circle at $0^{\circ}$, $120^{\circ}$ and $240^{\circ}$, forming an equilateral triangle. Right: the same three vectors laid head to tail close up exactly, which is what $1 + \omega + \omega^{2} = 0$ means."
import numpy as np, matplotlib.pyplot as plt
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(5.0,2.7))
t = np.linspace(0, 2*np.pi, 400)
ax1.plot(np.cos(t), np.sin(t), color=GRID, lw=1.0)
ax1.axhline(0, color=INK, lw=0.7); ax1.axvline(0, color=INK, lw=0.7)
a = np.radians([0, 120, 240]); xs, ys = np.cos(a), np.sin(a)
ax1.fill(xs, ys, color=ACCENT, alpha=0.12)
ax1.plot(np.append(xs, xs[0]), np.append(ys, ys[0]), color=ACCENT, lw=1.3)
ax1.plot(xs, ys, 'o', color=ACCENT, ms=6, zorder=4)
for x, y, lab, off in zip(xs, ys, ['$1$', r'$\omega$', r'$\omega^{2}$'],
                          [(0.12,-0.16), (-0.12,0.16), (-0.12,-0.34)]):
    ax1.text(x+off[0], y+off[1], lab, color=ACCENT, fontsize=9.5)
ax1.text(-1.35, -1.32, '$120^{\\circ}$ apart', color=MUTED, fontsize=7.8)
ax1.set_xlim(-1.5, 1.5); ax1.set_ylim(-1.5, 1.5)
ax1.set_aspect('equal'); ax1.axis('off')
px, py = 0.0, 0.0
cols = [SERIES[0], SERIES[1], SERIES[2]]
labs = ['$1$', r'$\omega$', r'$\omega^{2}$']
for k in range(3):
    ang = np.radians(120*k)
    nx, ny = px + np.cos(ang), py + np.sin(ang)
    ax2.annotate('', xy=(nx, ny), xytext=(px, py),
                 arrowprops=dict(arrowstyle='-|>', color=cols[k], lw=1.7,
                                 shrinkA=0, shrinkB=0))
    ax2.text((px+nx)/2 + (0.06 if k != 2 else -0.30),
             (py+ny)/2 + (0.12 if k == 0 else -0.06), labs[k],
             color=cols[k], fontsize=9.5)
    px, py = nx, ny
ax2.plot([0], [0], 'o', color=INK, ms=5)
ax2.text(0.02, -0.24, 'start = finish', color=INK, fontsize=8.0)
ax2.text(-0.55, 1.02, '$1+\\omega+\\omega^{2}=0$', color=INK, fontsize=9.0)
ax2.set_xlim(-0.85, 1.35); ax2.set_ylim(-0.45, 1.35)
ax2.set_aspect('equal'); ax2.axis('off')
```

::: example Worked example 3.9
**Problem.** If $\omega$ is a complex cube root of unity, find the value of
$\omega^{100} + \omega^{200} + \omega^{300}$.

**Solution.** Reduce each index modulo $3$, using $\omega^{3} = 1$.

$100 = 3(33) + 1$, so $\omega^{100} = \left(\omega^{3}\right)^{33}\omega
= 1^{33}\omega = \omega$.

$200 = 3(66)+2$, so $\omega^{200} = \left(\omega^{3}\right)^{66}\omega^{2}
= \omega^{2}$.

$300 = 3(100)$, so $\omega^{300} = \left(\omega^{3}\right)^{100} = 1$.

Adding, and using property 2:

$$ \omega^{100}+\omega^{200}+\omega^{300} = \omega + \omega^{2} + 1 = 0 $$
:::

::: example Worked example 3.10
**Problem.** Prove that $\left(1 + \omega - \omega^{2}\right)^{3}
+ \left(1 - \omega + \omega^{2}\right)^{3} = -16$.

**Solution.** Use $1 + \omega + \omega^{2} = 0$ to simplify each bracket before
cubing — never expand the cube directly.

From $1+\omega+\omega^{2} = 0$ we get $1 + \omega = -\omega^{2}$, so

$$ 1 + \omega - \omega^{2} = \left(1+\omega\right) - \omega^{2}
= -\omega^{2} - \omega^{2} = -2\omega^{2} $$

Similarly $1 + \omega^{2} = -\omega$, so

$$ 1 - \omega + \omega^{2} = \left(1+\omega^{2}\right) - \omega
= -\omega - \omega = -2\omega $$

Now cube both:

$$ \left(-2\omega^{2}\right)^{3} = -8\omega^{6} = -8\left(\omega^{3}\right)^{2}
= -8 $$

$$ \left(-2\omega\right)^{3} = -8\omega^{3} = -8 $$

Adding, the required value is $-8 + (-8) = -16$. $\blacksquare$
:::

::: example Worked example 3.11
**Problem.** Show that
$a^{3}+b^{3}+c^{3}-3abc
= (a+b+c)\left(a+b\omega+c\omega^{2}\right)\left(a+b\omega^{2}+c\omega\right)$,
and hence evaluate the right side when $a=1$, $b=2$, $c=3$.

**Solution.** Multiply the last two factors first. Expanding term by term:

$$ \left(a+b\omega+c\omega^{2}\right)\left(a+b\omega^{2}+c\omega\right)
= a^{2} + ab\omega^{2} + ac\omega + ab\omega + b^{2}\omega^{3} + bc\omega^{2}
+ ac\omega^{2} + bc\omega^{4} + c^{2}\omega^{3} $$

Use $\omega^{3} = 1$ and $\omega^{4} = \omega$, then collect the $\omega$ and
$\omega^{2}$ terms:

$$ = a^{2}+b^{2}+c^{2} + \left(ac + ab + bc\right)\omega
+ \left(ab + bc + ac\right)\omega^{2} $$

$$ = a^{2}+b^{2}+c^{2} + \left(ab+bc+ca\right)\left(\omega + \omega^{2}\right) $$

Since $\omega+\omega^{2} = -1$, this is $a^{2}+b^{2}+c^{2}-ab-bc-ca$. Therefore
the product of all three factors is

$$ (a+b+c)\left(a^{2}+b^{2}+c^{2}-ab-bc-ca\right) = a^{3}+b^{3}+c^{3}-3abc $$

which is the standard identity. For $a=1$, $b=2$, $c=3$:

$$ a^{3}+b^{3}+c^{3}-3abc = 1 + 8 + 27 - 3(6) = 36 - 18 = 18 $$

(As a check, $a+b+c = 6$ and the other two factors multiply to
$1+4+9-2-6-3 = 3$, and $6 \times 3 = 18$.)
:::

## 3.4 Euler's formula

In Unit 2 the exponential series $e^{x} = 1 + x + \dfrac{x^{2}}{2!} +
\dfrac{x^{3}}{3!} + \cdots$ was established for every real $x$. It also holds
when the exponent is imaginary, and the result is remarkable.

::: derivation Euler's formula
Put $x = i\theta$ in the exponential series:

$$ e^{i\theta} = 1 + i\theta + \frac{(i\theta)^{2}}{2!}
+ \frac{(i\theta)^{3}}{3!} + \frac{(i\theta)^{4}}{4!} + \cdots $$

The powers of $i$ cycle $i, -1, -i, 1$:

$$ = 1 + i\theta - \frac{\theta^{2}}{2!} - \frac{i\theta^{3}}{3!}
+ \frac{\theta^{4}}{4!} + \frac{i\theta^{5}}{5!} - \cdots $$

Separate the terms without $i$ from the terms with $i$:

$$ = \left(1 - \frac{\theta^{2}}{2!} + \frac{\theta^{4}}{4!} - \cdots\right)
+ i\left(\theta - \frac{\theta^{3}}{3!} + \frac{\theta^{5}}{5!}
- \cdots\right) $$

The first bracket is the series for $\cos\theta$ and the second is the series
for $\sin\theta$. Hence

$$ e^{i\theta} = \cos\theta + i\sin\theta $$

Replacing $\theta$ by $-\theta$ gives $e^{-i\theta} = \cos\theta -
i\sin\theta$. $\blacksquare$
:::

::: key Euler's formula and exponential form
$$ e^{i\theta} = \cos\theta + i\sin\theta, \qquad
e^{-i\theta} = \cos\theta - i\sin\theta $$
$$ z = r(\cos\theta+i\sin\theta) = re^{i\theta} $$
$$ \cos\theta = \frac{e^{i\theta}+e^{-i\theta}}{2}, \qquad
\sin\theta = \frac{e^{i\theta}-e^{-i\theta}}{2i} $$
De Moivre's theorem is now just the index law
$\left(e^{i\theta}\right)^{n} = e^{in\theta}$. Putting $\theta = \pi$ gives
**Euler's identity** $e^{i\pi} + 1 = 0$, which links $e$, $i$, $\pi$, $1$ and
$0$ in one equation.
:::

```figure caption="Euler's formula on the unit circle: $e^{i\theta}$ is the point at angle $\theta$, so its horizontal shadow is $\cos\theta$ and its vertical shadow is $\sin\theta$. Quarter-turns give $e^{i\pi/2} = i$, $e^{i\pi} = -1$ and $e^{3i\pi/2} = -i$."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Arc
fig, ax = plt.subplots(figsize=(4.6,3.2))
t = np.linspace(0, 2*np.pi, 400)
ax.plot(np.cos(t), np.sin(t), color=ACCENT, lw=1.3)
ax.axhline(0, color=INK, lw=0.9); ax.axvline(0, color=INK, lw=0.9)
d = 58.0; a = np.radians(d); x, y = np.cos(a), np.sin(a)
ax.annotate('', xy=(x,y), xytext=(0,0),
            arrowprops=dict(arrowstyle='-|>', color=SERIES[0], lw=1.7,
                            shrinkA=0, shrinkB=0))
ax.plot([x,x],[0,y], ls=':', color=MUTED, lw=1.1)
ax.plot([0,x],[y,y], ls=':', color=MUTED, lw=1.1)
ax.plot([x],[y], 'o', color=SERIES[0], ms=6, zorder=4)
ax.text(x+0.06, y+0.10, r'$e^{i\theta}$', color=SERIES[0], fontsize=10)
ax.add_patch(Arc((0,0), 0.56, 0.56, theta1=0, theta2=d, color=SERIES[4], lw=1.2))
ax.text(0.31, 0.10, r'$\theta$', color=SERIES[4], fontsize=10)
ax.text(x/2-0.10, -0.20, r'$\cos\theta$', color=MUTED, fontsize=8.4)
ax.text(x+0.09, y/2-0.05, r'$\sin\theta$', color=MUTED, fontsize=8.4)
for xx, yy, lab, off in [(1,0,'$e^{i0}=1$',(0.08,-0.20)),
                         (0,1,'$e^{i\\pi/2}=i$',(0.10,0.10)),
                         (-1,0,'$e^{i\\pi}=-1$',(-0.30,-0.24)),
                         (0,-1,'$e^{3i\\pi/2}=-i$',(0.10,-0.22))]:
    ax.plot([xx],[yy], 'o', color=INK, ms=4, zorder=4)
    ax.text(xx+off[0], yy+off[1], lab, color=INK, fontsize=8.2)
ax.set_xlim(-1.75, 1.75); ax.set_ylim(-1.45, 1.40)
ax.set_aspect('equal'); ax.axis('off')
```

::: example Worked example 3.12
**Problem.** Express $1+i$ in the exponential form $re^{i\theta}$, and use it to
find $(1+i)^{10}$.

**Solution.** From Worked example 3.3, $r = \sqrt{2}$ and
$\theta = \pi/4$, so

$$ 1 + i = \sqrt{2}\,e^{i\pi/4} $$

Raise to the tenth power using the index laws:

$$ (1+i)^{10} = \left(\sqrt{2}\right)^{10}e^{10i\pi/4} = 32\,e^{5i\pi/2} $$

Reduce the angle: $\dfrac{5\pi}{2} = 2\pi + \dfrac{\pi}{2}$, and $e^{2\pi i} = 1$,
so $e^{5i\pi/2} = e^{i\pi/2} = i$. Hence

$$ (1+i)^{10} = 32i $$

the same answer as before, with less writing — this is why physicists and
engineers keep complex numbers in exponential form.
:::

::: example Worked example 3.13
**Problem.** Use Euler's formula to prove
$\cos^{3}\theta = \dfrac{3\cos\theta + \cos 3\theta}{4}$.

**Solution.** Start from $2\cos\theta = e^{i\theta} + e^{-i\theta}$ and cube
both sides:

$$ 8\cos^{3}\theta = \left(e^{i\theta}+e^{-i\theta}\right)^{3} $$

Expand by the binomial theorem, with $a = e^{i\theta}$, $b = e^{-i\theta}$, and
note that $ab = e^{i\theta}e^{-i\theta} = e^{0} = 1$:

$$ = e^{3i\theta} + 3e^{2i\theta}e^{-i\theta} + 3e^{i\theta}e^{-2i\theta}
+ e^{-3i\theta} $$

$$ = \left(e^{3i\theta} + e^{-3i\theta}\right)
+ 3\left(e^{i\theta} + e^{-i\theta}\right) $$

Each bracket is twice a cosine, by Euler's formula:

$$ 8\cos^{3}\theta = 2\cos 3\theta + 3(2\cos\theta)
= 2\cos 3\theta + 6\cos\theta $$

Divide by $8$:

$$ \cos^{3}\theta = \frac{2\cos 3\theta + 6\cos\theta}{8}
= \frac{3\cos\theta + \cos 3\theta}{4} $$

**Check** at $\theta = 0$: left side $1$, right side $(3+1)/4 = 1$.
$\blacksquare$
:::

::: example Worked example 3.14
**Problem.** If $x + \dfrac{1}{x} = 2\cos\theta$, prove that
$x^{n} + \dfrac{1}{x^{n}} = 2\cos n\theta$.

**Solution.** Multiply through by $x$ to get the quadratic
$x^{2} - 2x\cos\theta + 1 = 0$, so

$$ x = \frac{2\cos\theta \pm \sqrt{4\cos^{2}\theta - 4}}{2}
= \cos\theta \pm \sqrt{\cos^{2}\theta - 1} $$

Now $\cos^{2}\theta - 1 = -\sin^{2}\theta$, and
$\sqrt{-\sin^{2}\theta} = i\sin\theta$, so

$$ x = \cos\theta \pm i\sin\theta = e^{\pm i\theta} $$

Take $x = e^{i\theta}$ (the other sign only swaps the two terms below). Then by
De Moivre, $x^{n} = e^{in\theta} = \cos n\theta + i\sin n\theta$ and

$$ \frac{1}{x^{n}} = e^{-in\theta} = \cos n\theta - i\sin n\theta $$

Adding, the imaginary parts cancel:

$$ x^{n} + \frac{1}{x^{n}} = 2\cos n\theta $$

$\blacksquare$ (The companion result, from subtracting, is
$x^{n} - \dfrac{1}{x^{n}} = 2i\sin n\theta$.)
:::

## Chapter summary

- Polar form: $z = r(\cos\theta + i\sin\theta)$ with $r = |z| =
  \sqrt{x^{2}+y^{2}}$ and $\tan\theta = y/x$; fix $\theta$ from the **quadrant**
  of $(x, y)$, principal value in $-\pi < \theta \leq \pi$.
- Multiply: moduli multiply, arguments add. Divide: moduli divide, arguments
  subtract.
- De Moivre: $\left[r(\cos\theta+i\sin\theta)\right]^{n} = r^{n}(\cos n\theta +
  i\sin n\theta)$, proved by induction for positive integers and extended to
  negative and rational indices.
- Equating real and imaginary parts in
  $(\cos\theta+i\sin\theta)^{n} = \cos n\theta + i\sin n\theta$ gives the
  multiple-angle formulas, e.g. $\cos 3\theta = 4\cos^{3}\theta - 3\cos\theta$.
- $n^{\text{th}}$ roots: $z^{1/n} = r^{1/n}\left[\cos\dfrac{\theta+2k\pi}{n}
  + i\sin\dfrac{\theta+2k\pi}{n}\right]$, $k = 0, 1, \ldots, n-1$ — exactly $n$
  roots, equally spaced on a circle of radius $r^{1/n}$, forming a regular
  $n$-gon.
- $n^{\text{th}}$ roots of unity: $1, w, \ldots, w^{n-1}$ with
  $w = \cos\dfrac{2\pi}{n} + i\sin\dfrac{2\pi}{n}$; sum $= 0$, product
  $= (-1)^{n+1}$.
- Cube roots of unity: $1, \omega = \dfrac{-1+i\sqrt{3}}{2},
  \omega^{2} = \dfrac{-1-i\sqrt{3}}{2}$ with $\omega^{3}=1$ and
  $1+\omega+\omega^{2}=0$; reduce indices modulo $3$.
- Euler: $e^{i\theta} = \cos\theta+i\sin\theta$, $z = re^{i\theta}$,
  $e^{i\pi}+1=0$, $\cos\theta = \dfrac{e^{i\theta}+e^{-i\theta}}{2}$.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The modulus of $1 - i\sqrt{3}$ is <span class="marks">[1]</span>
   (a) $1$ (b) $2$ (c) $4$ (d) $\sqrt{2}$
2. The principal argument of $-1-i$ is <span class="marks">[1]</span>
   (a) $\dfrac{\pi}{4}$ (b) $\dfrac{3\pi}{4}$ (c) $-\dfrac{3\pi}{4}$ (d) $\dfrac{5\pi}{4}$
3. The value of $i^{2026}$ is <span class="marks">[1]</span>
   (a) $1$ (b) $-1$ (c) $i$ (d) $-i$
4. If $\omega$ is a complex cube root of unity, then $\omega^{4} + \omega^{2} + 1$ equals <span class="marks">[1]</span>
   (a) $0$ (b) $1$ (c) $\omega$ (d) $3$
5. The number of distinct fifth roots of $-32$ is <span class="marks">[1]</span>
   (a) $1$ (b) $2$ (c) $5$ (d) infinitely many
6. $e^{i\pi/2}$ equals <span class="marks">[1]</span>
   (a) $1$ (b) $-1$ (c) $i$ (d) $-i$

::: note Answers to Group A
**1.** (b) — $\sqrt{1^{2}+(\sqrt{3})^{2}} = \sqrt{4} = 2$.

**2.** (c) — $(-1,-1)$ is in the third quadrant with $\alpha = \pi/4$, so
$\theta = -(\pi - \pi/4) = -3\pi/4$.

**3.** (b) — $2026 = 4(506) + 2$, so $i^{2026} = i^{2} = -1$.

**4.** (a) — $\omega^{4} = \omega^{3}\omega = \omega$, so the sum is
$1 + \omega + \omega^{2} = 0$.

**5.** (c) — a non-zero complex number has exactly $n$ distinct
$n^{\text{th}}$ roots.

**6.** (c) — $e^{i\pi/2} = \cos 90^{\circ} + i\sin 90^{\circ} = i$.
:::

**Group B — Short answer (5 marks each)**

1. Express $-1 + i\sqrt{3}$ in polar form and hence evaluate
   $\left(-1+i\sqrt{3}\right)^{5}$. <span class="marks">[5]</span>
2. State De Moivre's theorem and prove it for a positive integral index.
   <span class="marks">[5]</span>
3. Find the modulus and principal argument of
   $\dfrac{1+i}{1-i}$, and write it in exponential form.
   <span class="marks">[5]</span>
4. Solve $z^{3} = -1$, giving the roots in the form $x+iy$, and show that they
   lie at the vertices of an equilateral triangle. <span class="marks">[5]</span>
5. If $1, \omega, \omega^{2}$ are the cube roots of unity, prove that
   $(1+\omega)\left(1+\omega^{2}\right)\left(1+\omega^{4}\right)
   \left(1+\omega^{8}\right) = 1$. <span class="marks">[5]</span>
6. Using De Moivre's theorem, prove that
   $\sin 3\theta = 3\sin\theta - 4\sin^{3}\theta$. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** $r = \sqrt{(-1)^{2}+(\sqrt{3})^{2}} = 2$; $\tan\alpha = \sqrt{3}/1$ gives
$\alpha = 60^{\circ}$, and $(-1, \sqrt{3})$ is in the second quadrant, so
$\theta = 180^{\circ}-60^{\circ} = 120^{\circ}$:
$-1+i\sqrt{3} = 2\left(\cos 120^{\circ} + i\sin 120^{\circ}\right)$.
By De Moivre,
$\left(-1+i\sqrt{3}\right)^{5} = 2^{5}\left(\cos 600^{\circ} + i\sin 600^{\circ}\right)$.
Since $600^{\circ} = 360^{\circ}+240^{\circ}$, use $240^{\circ}$:
$\cos 240^{\circ} = -\tfrac12$, $\sin 240^{\circ} = -\tfrac{\sqrt{3}}{2}$. So the
value is $32\left(-\tfrac12 - \tfrac{\sqrt{3}}{2}i\right) = -16 - 16\sqrt{3}\,i$.

**2.** Statement: for a positive integer $n$,
$(\cos\theta+i\sin\theta)^{n} = \cos n\theta + i\sin n\theta$. Proof by
induction: $P(1)$ is an identity. Assuming
$(\cos\theta+i\sin\theta)^{k} = \cos k\theta + i\sin k\theta$ and multiplying by
$(\cos\theta+i\sin\theta)$ gives
$(\cos k\theta\cos\theta - \sin k\theta\sin\theta)
+ i(\sin k\theta\cos\theta + \cos k\theta\sin\theta)
= \cos(k+1)\theta + i\sin(k+1)\theta$, using the compound-angle formulas. So
$P(k) \Rightarrow P(k+1)$ and the result holds for all positive integers $n$.

**3.** $|1+i| = \sqrt{2}$ with argument $45^{\circ}$; $|1-i| = \sqrt{2}$ with
argument $-45^{\circ}$. Dividing, the modulus is $\sqrt{2}/\sqrt{2} = 1$ and the
argument is $45^{\circ}-(-45^{\circ}) = 90^{\circ} = \pi/2$. Hence
$\dfrac{1+i}{1-i} = 1 \cdot e^{i\pi/2} = i$, which the direct calculation
$\dfrac{(1+i)^{2}}{(1-i)(1+i)} = \dfrac{2i}{2} = i$ confirms.

**4.** $-1 = 1\left[\cos(180^{\circ}+360^{\circ}k) +
i\sin(180^{\circ}+360^{\circ}k)\right]$, so
$z = \cos\dfrac{180^{\circ}+360^{\circ}k}{3} + i\sin\dfrac{180^{\circ}+360^{\circ}k}{3}$
for $k = 0,1,2$: arguments $60^{\circ}, 180^{\circ}, 300^{\circ}$. The roots are
$\tfrac12 + \tfrac{\sqrt{3}}{2}i$, $-1$, and $\tfrac12 - \tfrac{\sqrt{3}}{2}i$. All
have modulus $1$ and their arguments differ by $120^{\circ}$, so they are
equally spaced on the unit circle — the vertices of an equilateral triangle.

**5.** Reduce the indices modulo $3$: $\omega^{4} = \omega$ and
$\omega^{8} = \omega^{6}\omega^{2} = \omega^{2}$. The product becomes
$\left[(1+\omega)(1+\omega^{2})\right]^{2}$. Since $1+\omega = -\omega^{2}$ and
$1+\omega^{2} = -\omega$, we get
$(1+\omega)(1+\omega^{2}) = \omega^{3} = 1$, so the product is $1^{2} = 1$.

**6.** By De Moivre,
$\cos 3\theta + i\sin 3\theta = (\cos\theta+i\sin\theta)^{3}$. Expanding with
$c = \cos\theta$, $s = \sin\theta$:
$c^{3} + 3ic^{2}s - 3cs^{2} - is^{3}$. Equating imaginary parts,
$\sin 3\theta = 3c^{2}s - s^{3} = 3(1-s^{2})s - s^{3} = 3\sin\theta - 4\sin^{3}\theta$.
:::

**Group C — Long answer (8 marks each)**

1. State De Moivre's theorem and prove it for a positive integral index. Hence
   find the five fifth roots of $32$, and show that they are the vertices of a
   regular pentagon inscribed in a circle of radius $2$.
   <span class="marks">[8]</span>
2. Derive the general expression for the $n$ $n^{\text{th}}$ roots of unity.
   Prove that their sum is zero and their product is $(-1)^{n+1}$, and verify
   both results for $n = 6$. <span class="marks">[8]</span>
3. Find the cube roots of unity from $z^{3}-1 = 0$ and prove that
   $1+\omega+\omega^{2} = 0$. Hence prove that
   $(1+\omega)^{3} - \left(1+\omega^{2}\right)^{3} = 0$ and that
   $a^{3}+b^{3}+c^{3}-3abc
   = (a+b+c)\left(a+b\omega+c\omega^{2}\right)\left(a+b\omega^{2}+c\omega\right)$.
   <span class="marks">[8]</span>

::: note Answers to Group C
**1.** *Statement and proof:* as in Group B question 2 — state
$(\cos\theta+i\sin\theta)^{n} = \cos n\theta+i\sin n\theta$, verify $P(1)$,
assume $P(k)$, multiply by $(\cos\theta+i\sin\theta)$ and use the
compound-angle formulas to reach $P(k+1)$; conclude by induction.

*Fifth roots of 32:* $32 = 32\left[\cos(0+360^{\circ}k) +
i\sin(0+360^{\circ}k)\right]$, so
$z = 32^{1/5}\left[\cos\dfrac{360^{\circ}k}{5} + i\sin\dfrac{360^{\circ}k}{5}\right]$
with $k = 0,1,2,3,4$. As $32^{1/5} = 2$, the roots are
$2\left(\cos 72^{\circ}k + i\sin 72^{\circ}k\right)$, i.e. $2$,
$2(\cos 72^{\circ}+i\sin 72^{\circ}) \approx 0.618 + 1.902i$,
$2(\cos 144^{\circ}+i\sin 144^{\circ}) \approx -1.618+1.176i$,
$2(\cos 216^{\circ}+i\sin 216^{\circ}) \approx -1.618-1.176i$ and
$2(\cos 288^{\circ}+i\sin 288^{\circ}) \approx 0.618-1.902i$.

*Pentagon:* every root has modulus $2$, so all five lie on the circle
$|z| = 2$; consecutive arguments differ by exactly $72^{\circ} = 360^{\circ}/5$,
so the chords joining them are equal and the five points are the vertices of a
regular pentagon of circumradius $2$.

**2.** *Derivation:* $1 = \cos(0 + 2k\pi) + i\sin(0+2k\pi)$ for every integer
$k$, so by De Moivre with index $1/n$,
$w_{k} = \cos\dfrac{2k\pi}{n} + i\sin\dfrac{2k\pi}{n}$. Increasing $k$ by $n$
increases the argument by $2\pi$ and repeats a root, so $k = 0,1,\ldots,n-1$
give all $n$ distinct roots, and $w_{k} = w^{k}$ where
$w = \cos\dfrac{2\pi}{n}+i\sin\dfrac{2\pi}{n}$.

*Sum:* $1 + w + \cdots + w^{n-1} = \dfrac{w^{n}-1}{w-1} = 0$ because
$w^{n} = \cos 2\pi + i\sin 2\pi = 1$ while $w \neq 1$ for $n \geq 2$.

*Product:* $1 \cdot w \cdot w^{2}\cdots w^{n-1} = w^{0+1+\cdots+(n-1)}
= w^{n(n-1)/2}
= \left(\cos\dfrac{2\pi}{n}+i\sin\dfrac{2\pi}{n}\right)^{n(n-1)/2}
= \cos(n-1)\pi + i\sin(n-1)\pi = (-1)^{n-1} = (-1)^{n+1}$.

*Check $n = 6$:* the roots are $\pm 1$, $\pm\tfrac12 \pm \tfrac{\sqrt{3}}{2}i$,
i.e. $1, \tfrac12+\tfrac{\sqrt{3}}{2}i, -\tfrac12+\tfrac{\sqrt{3}}{2}i, -1,
-\tfrac12-\tfrac{\sqrt{3}}{2}i, \tfrac12-\tfrac{\sqrt{3}}{2}i$. Their sum is
$(1 + \tfrac12 - \tfrac12 - 1 - \tfrac12 + \tfrac12) + i(\tfrac{\sqrt{3}}{2}
+\tfrac{\sqrt{3}}{2}-\tfrac{\sqrt{3}}{2}-\tfrac{\sqrt{3}}{2}) = 0$. For the product,
pair conjugates: $\left(\tfrac12+\tfrac{\sqrt{3}}{2}i\right)
\left(\tfrac12-\tfrac{\sqrt{3}}{2}i\right) = \tfrac14+\tfrac34 = 1$ and likewise
$\left(-\tfrac12+\tfrac{\sqrt{3}}{2}i\right)\left(-\tfrac12-\tfrac{\sqrt{3}}{2}i\right) = 1$,
so the product is $1 \times (-1) \times 1 \times 1 = -1 = (-1)^{7}$. Both
results check.

**3.** *Cube roots:* $z^{3}-1 = (z-1)(z^{2}+z+1) = 0$ gives $z = 1$ or
$z = \dfrac{-1\pm i\sqrt{3}}{2}$. Writing
$\omega = \dfrac{-1+i\sqrt{3}}{2}$, direct squaring gives
$\omega^{2} = \dfrac{-1-i\sqrt{3}}{2}$, so the three roots are
$1, \omega, \omega^{2}$.

*Sum:* $\omega$ and $\omega^{2}$ satisfy $z^{2}+z+1 = 0$, so
$\omega^{2}+\omega+1 = 0$, i.e. $1+\omega+\omega^{2} = 0$. (Equivalently,
$\tfrac{-1+i\sqrt{3}}{2}+\tfrac{-1-i\sqrt{3}}{2} = -1$, and adding $1$ gives $0$.)

*First identity:* $1+\omega = -\omega^{2}$ and $1+\omega^{2} = -\omega$, so
$(1+\omega)^{3} = -\omega^{6} = -\left(\omega^{3}\right)^{2} = -1$ and
$\left(1+\omega^{2}\right)^{3} = -\omega^{3} = -1$. Their difference is
$-1-(-1) = 0$.

*Factorisation:* multiply the last two brackets and use $\omega^{3}=1$,
$\omega^{4}=\omega$:
$\left(a+b\omega+c\omega^{2}\right)\left(a+b\omega^{2}+c\omega\right)
= a^{2}+b^{2}+c^{2}+(ab+bc+ca)\left(\omega+\omega^{2}\right)
= a^{2}+b^{2}+c^{2}-ab-bc-ca$, since $\omega+\omega^{2} = -1$. Multiplying by
$(a+b+c)$ and using the standard identity
$(a+b+c)\left(a^{2}+b^{2}+c^{2}-ab-bc-ca\right) = a^{3}+b^{3}+c^{3}-3abc$
completes the proof.
:::
