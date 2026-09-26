---
subject: Mathematics
grade: 11
unit: 10
title: Trigonometric Equations and General Values
hours: 6
area: Trigonometry
---

An equation such as $2\sin\theta = 1$ is unlike a polynomial equation: because
$\sin\theta$ repeats every $2\pi$, it has infinitely many roots. The task is
therefore not to find *a* root but to write **all** roots in one compact formula —
the **general value** of $\theta$. This unit gives the three master formulae that
do that, and the standard techniques for reducing any exam equation to one of the
three basic forms $\sin\theta=\sin\alpha$, $\cos\theta=\cos\alpha$ or
$\tan\theta=\tan\alpha$.

::: key The shape of every answer
Every solution ends in one of three patterns:
$\theta = n\pi+(-1)^{n}\alpha$, $\theta = 2n\pi\pm\alpha$, or
$\theta = n\pi+\alpha$, where $n \in \mathbb{Z}$. Getting to that pattern is the
work; writing "$n\in\mathbb{Z}$" at the end is a mark.
:::

## 10.1 Solution of trigonometric equations

### Roots, principal value and general value

::: definition Trigonometric equation
An equation involving trigonometric ratios of an unknown angle that is true only
for particular values of that angle is a **trigonometric equation**. A value of
the angle satisfying it is a **root** or **solution**. The numerically smallest
root is the **principal solution**; the formula covering all roots is the
**general solution** (or general value).
:::

An *identity* such as $\sin^{2}\theta+\cos^{2}\theta=1$ holds for every $\theta$;
an *equation* such as $\sin\theta = \frac{1}{2}$ holds only for some. Do not
confuse the two.

### Deciding the quadrant

The first step in every problem is to find one angle $\alpha$ — usually an angle
from the standard table — and then to decide **which quadrants** can contain
solutions. The sign of the ratio settles it.

```figure caption="Signs of the ratios by quadrant. Read anticlockwise: All, Sine, Tangent, Cosine are the ratios that are positive."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.2,3.2))
th = np.linspace(0,2*np.pi,400)
ax.plot(np.cos(th), np.sin(th), color=MUTED, lw=1.3)
ax.axhline(0, color=INK, lw=1.0); ax.axvline(0, color=INK, lw=1.0)
lab = [(0.55,0.55,'I','All +'), (-0.55,0.55,'II','sin, cosec +'),
       (-0.55,-0.55,'III','tan, cot +'), (0.55,-0.55,'IV','cos, sec +')]
for x,y,q,s in lab:
    ax.text(x, y+0.13, q, ha='center', fontsize=11, color=ACCENT, weight='bold')
    ax.text(x, y-0.13, s, ha='center', fontsize=8.6, color=INK)
for x,y,t,ha,va in [(1.16,0.07,'0','left','bottom'),(0.07,1.16,'π/2','left','bottom'),
                    (-1.16,0.07,'π','right','bottom'),(0.07,-1.16,'3π/2','left','top')]:
    ax.text(x,y,t,fontsize=8.5,color=MUTED,ha=ha,va=va)
a = np.linspace(0.06, 1.05, 40)
ax.plot(0.26*np.cos(a), 0.26*np.sin(a), color='#d9534f', lw=1.2)
ax.annotate('', xy=(0.26*np.cos(1.05),0.26*np.sin(1.05)),
            xytext=(0.26*np.cos(0.92),0.26*np.sin(0.92)),
            arrowprops=dict(arrowstyle='-|>', color='#d9534f', lw=1.2, mutation_scale=9))
ax.text(0.33,0.10,r'$\theta$',fontsize=10,color='#d9534f')
ax.set_xlim(-1.45,1.45); ax.set_ylim(-1.42,1.42); ax.set_aspect('equal')
ax.axis('off')
```

::: memory "All Silver Tea Cups"
Quadrant I **A**ll positive, II **S**ine (and cosec), III **T**angent (and cot),
IV **C**osine (and sec). Anything not listed is negative in that quadrant.
:::

::: example Worked example 10.1 — solutions in a given interval
**Problem.** Solve $2\sin\theta+1 = 0$ for $0 \le \theta < 2\pi$.

**Solution.** Rearranging, $\sin\theta = -\dfrac12$.

The related acute angle is $\alpha$ with $\sin\alpha = \frac12$, i.e.
$\alpha = \dfrac{\pi}{6}$.

Since $\sin\theta$ is **negative**, $\theta$ lies in quadrant III or IV.

$$ \text{quadrant III: } \theta = \pi+\frac{\pi}{6} = \frac{7\pi}{6},
\qquad \text{quadrant IV: } \theta = 2\pi-\frac{\pi}{6} = \frac{11\pi}{6} $$

So $\theta = \dfrac{7\pi}{6}, \dfrac{11\pi}{6}$. (The principal solution, the
numerically smallest root, is $-\dfrac{\pi}{6}$.)
:::

```figure caption="$\sin\theta=-\tfrac12$ on $[0,2\pi)$: exactly two roots, one in each of quadrants III and IV."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,2.6))
t = np.linspace(0, 2*np.pi, 600)
ax.plot(t, np.sin(t), color=ACCENT, lw=2.0)
ax.axhline(-0.5, color='#d9534f', lw=1.2, ls='--')
r = [7*np.pi/6, 11*np.pi/6]
ax.plot(r, [-0.5,-0.5], 'o', color='#d9534f', ms=6, zorder=5)
for v, lb in zip(r, [r'$\frac{7\pi}{6}$', r'$\frac{11\pi}{6}$']):
    ax.vlines(v, -0.5, 0, color=MUTED, lw=0.9, ls=':')
    ax.annotate(lb, (v,-0.5), textcoords='offset points', xytext=(0,-28),
                ha='center', color='#d9534f', fontsize=10)
ax.annotate(r'$y=-\frac{1}{2}$', (0,-0.5), textcoords='offset points',
            xytext=(6,8), ha='left', color='#d9534f', fontsize=9)
ax.axhline(0, color=INK, lw=0.9)
ax.set_xticks([0,np.pi/2,np.pi,3*np.pi/2,2*np.pi])
ax.set_xticklabels(['0',r'$\pi/2$',r'$\pi$',r'$3\pi/2$',r'$2\pi$'])
ax.set_ylim(-1.55,1.2); ax.set_xlim(0,2*np.pi)
ax.set_xlabel(r'$\theta$'); ax.set_ylabel(r'$\sin\theta$')
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.35)
```

### The four standard techniques

| If the equation… | do this |
|---|---|
| is quadratic in one ratio | factorise, then solve each factor |
| mixes $\sin^{2}$ and $\cos$ (or $\cos^{2}$ and $\sin$) | use $\sin^{2}\theta = 1-\cos^{2}\theta$ to get one ratio only |
| is $a\cos\theta+b\sin\theta=c$ | write it as $r\cos(\theta-\alpha)=c$ with $r=\sqrt{a^{2}+b^{2}}$ |
| is a sum of sines or cosines | use the sum-to-product formulae and factorise |

::: caution Never divide by a trigonometric factor
From $\sin\theta\cos\theta = \sin\theta$ do **not** cancel $\sin\theta$ — that
throws away every root with $\sin\theta = 0$. Move everything to one side and
factorise: $\sin\theta(\cos\theta-1)=0$.
:::

::: example Worked example 10.2 — quadratic in one ratio
**Problem.** Solve $2\cos^{2}\theta-3\cos\theta+1 = 0$.

**Solution.** Put $c = \cos\theta$, so $2c^{2}-3c+1=0$, i.e. $(2c-1)(c-1)=0$.

Hence $\cos\theta = \dfrac12$ or $\cos\theta = 1$.

$\cos\theta = \frac12 = \cos\frac{\pi}{3}$ gives $\theta = 2n\pi\pm\dfrac{\pi}{3}$.

$\cos\theta = 1 = \cos 0$ gives $\theta = 2n\pi$.

(The general-value formulae used here are proved in §10.2.)
:::

::: example Worked example 10.3 — reduce to a single ratio
**Problem.** Solve $2\sin^{2}\theta+\sqrt{3}\cos\theta+1 = 0$.

**Solution.** Replace $\sin^{2}\theta$ by $1-\cos^{2}\theta$:

$$ 2(1-\cos^{2}\theta)+\sqrt{3}\cos\theta+1 = 0
\;\Rightarrow\; 2\cos^{2}\theta-\sqrt{3}\cos\theta-3 = 0 $$

With $c=\cos\theta$, the quadratic formula gives

$$ c = \frac{\sqrt{3}\pm\sqrt{3+24}}{4} = \frac{\sqrt{3}\pm 3\sqrt{3}}{4} $$

so $c = \sqrt{3}$ (impossible, since $|\cos\theta|\le 1$) or
$c = -\dfrac{2\sqrt{3}}{4} = -\dfrac{\sqrt{3}}{2}$.

Now $\cos\theta = -\frac{\sqrt{3}}{2} = \cos\frac{5\pi}{6}$, so
$\theta = 2n\pi\pm\dfrac{5\pi}{6}$.
:::

::: example Worked example 10.4 — reciprocal ratios
**Problem.** Solve $\tan\theta+\cot\theta = 2$.

**Solution.** Write $\cot\theta = \dfrac{1}{\tan\theta}$ and put $t=\tan\theta$
(note $t\ne 0$):

$$ t+\frac1t = 2 \;\Rightarrow\; t^{2}-2t+1 = 0 \;\Rightarrow\; (t-1)^{2}=0 $$

So $\tan\theta = 1 = \tan\dfrac{\pi}{4}$, giving $\theta = n\pi+\dfrac{\pi}{4}$.
:::

## 10.2 General values

### The three master formulae

::: derivation $\sin\theta = \sin\alpha \Rightarrow \theta = n\pi+(-1)^{n}\alpha$
Move everything to one side and use the sum-to-product identity
$\sin C-\sin D = 2\cos\frac{C+D}{2}\sin\frac{C-D}{2}$:

$$ \sin\theta-\sin\alpha = 0 \;\Rightarrow\;
2\cos\frac{\theta+\alpha}{2}\,\sin\frac{\theta-\alpha}{2} = 0 $$

A product is zero when a factor is zero, so either

$$ \cos\frac{\theta+\alpha}{2} = 0 \;\Rightarrow\; \frac{\theta+\alpha}{2} = (2m+1)\frac{\pi}{2}
\;\Rightarrow\; \theta = (2m+1)\pi-\alpha $$

or

$$ \sin\frac{\theta-\alpha}{2} = 0 \;\Rightarrow\; \frac{\theta-\alpha}{2} = m\pi
\;\Rightarrow\; \theta = 2m\pi+\alpha $$

The first family is "odd multiple of $\pi$, minus $\alpha$"; the second is "even
multiple of $\pi$, plus $\alpha$". Both are captured by the single formula

$$ \theta = n\pi+(-1)^{n}\alpha, \qquad n\in\mathbb{Z} $$

because $(-1)^{n}=+1$ for even $n$ and $-1$ for odd $n$.
:::

::: derivation $\cos\theta = \cos\alpha$ and $\tan\theta=\tan\alpha$
**Cosine.** Using $\cos C-\cos D = -2\sin\frac{C+D}{2}\sin\frac{C-D}{2}$,

$$ \cos\theta-\cos\alpha = 0 \;\Rightarrow\;
-2\sin\frac{\theta+\alpha}{2}\,\sin\frac{\theta-\alpha}{2} = 0 $$

giving $\frac{\theta+\alpha}{2} = m\pi$ or $\frac{\theta-\alpha}{2} = m\pi$, i.e.
$\theta = 2m\pi-\alpha$ or $\theta = 2m\pi+\alpha$. Together,

$$ \theta = 2n\pi\pm\alpha, \qquad n\in\mathbb{Z} $$

**Tangent.** $\tan\theta = \tan\alpha$ means
$\dfrac{\sin\theta}{\cos\theta} = \dfrac{\sin\alpha}{\cos\alpha}$, so
$\sin\theta\cos\alpha-\cos\theta\sin\alpha = 0$, that is $\sin(\theta-\alpha)=0$.
Hence $\theta-\alpha = n\pi$ and

$$ \theta = n\pi+\alpha, \qquad n\in\mathbb{Z} $$
:::

::: key General values — the complete list
$$ \sin\theta = \sin\alpha \;\Rightarrow\; \theta = n\pi+(-1)^{n}\alpha $$
$$ \cos\theta = \cos\alpha \;\Rightarrow\; \theta = 2n\pi\pm\alpha $$
$$ \tan\theta = \tan\alpha \;\Rightarrow\; \theta = n\pi+\alpha $$
Squared forms (all three give the same pattern):
$$ \sin^{2}\theta=\sin^{2}\alpha,\ \ \cos^{2}\theta=\cos^{2}\alpha,\ \ \tan^{2}\theta=\tan^{2}\alpha
\;\Rightarrow\; \theta = n\pi\pm\alpha $$
Special zero cases:
$$ \sin\theta=0 \Rightarrow \theta=n\pi; \qquad \cos\theta=0 \Rightarrow \theta=(2n+1)\frac{\pi}{2};
\qquad \tan\theta=0 \Rightarrow \theta=n\pi $$
In every case $n$ is an integer.
:::

```figure caption="$\sin\theta=\tfrac12$: the crossings come in pairs, and $\theta=n\pi+(-1)^{n}\pi/6$ picks out every one of them."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.2,2.8))
t = np.linspace(-2.1*np.pi, 3.1*np.pi, 1400)
ax.plot(t, np.sin(t), color=ACCENT, lw=1.8)
ax.axhline(0.5, color='#d9534f', lw=1.2, ls='--')
ns = np.arange(-2, 4)
xs = ns*np.pi + (-1.0)**ns * (np.pi/6)
keep = (xs > -2.1*np.pi) & (xs < 3.1*np.pi)
ax.plot(xs[keep], 0.5*np.ones(keep.sum()), 'o', color='#d9534f', ms=5.5, zorder=5)
for n, x in zip(ns[keep], xs[keep]):
    ax.annotate(f'n={n}', (x,0.5), textcoords='offset points', xytext=(0,-42),
                ha='center', color=MUTED, fontsize=8.5)
ax.annotate(r'$\theta=n\pi+(-1)^{n}\frac{\pi}{6}$', (0.5, -1.30),
            ha='center', color=INK, fontsize=10.5)
ax.axhline(0, color=INK, lw=0.9)
ax.set_xticks([-2*np.pi,-np.pi,0,np.pi,2*np.pi,3*np.pi])
ax.set_xticklabels([r'$-2\pi$',r'$-\pi$','0',r'$\pi$',r'$2\pi$',r'$3\pi$'])
ax.set_ylim(-1.75,1.35); ax.set_xlim(-2.15*np.pi, 3.15*np.pi)
ax.set_xlabel(r'$\theta$')
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.3)
```

Notice the geometry behind each formula. For the sine the two roots in a period
are *reflections in the vertical line* $\theta = \pi/2$, which is why the sign
alternates. For the cosine they are reflections in the $\theta$-axis direction —
that is, they come as the symmetric pair $\pm\alpha$ about each multiple of
$2\pi$.

```figure caption="$\cos\theta=\tfrac12$: the roots sit symmetrically at $\pm\pi/3$ about every multiple of $2\pi$, giving $\theta=2n\pi\pm\pi/3$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.2,2.6))
t = np.linspace(-2.2*np.pi, 2.2*np.pi, 1200)
ax.plot(t, np.cos(t), color=ACCENT, lw=1.8)
ax.axhline(0.5, color='#d9534f', lw=1.2, ls='--')
xs = []
for n in (-1,0,1):
    xs += [2*n*np.pi+np.pi/3, 2*n*np.pi-np.pi/3]
xs = np.array([x for x in xs if abs(x) < 2.2*np.pi])
ax.plot(xs, 0.5*np.ones_like(xs), 'o', color='#d9534f', ms=5.5, zorder=5)
for n in (-1,0,1):
    c = 2*n*np.pi
    if abs(c) < 2.2*np.pi:
        ax.vlines(c, 0.5, 1.0, color=MUTED, lw=0.9, ls=':')
        ax.annotate(f'{2*n}π' if n else '0', (c,1.02), ha='center',
                    va='bottom', color=MUTED, fontsize=8.5)
        ax.annotate('', xy=(c+np.pi/3,0.62), xytext=(c,0.62),
                    arrowprops=dict(arrowstyle='<->', color=MUTED, lw=0.9,
                                    mutation_scale=7))
        ax.text(c+np.pi/6, 0.66, 'π/3', ha='center', va='bottom',
                color=MUTED, fontsize=7.5)
ax.annotate(r'$\theta=2n\pi\pm\frac{\pi}{3}$', (0,-1.42), ha='center',
            color=INK, fontsize=10.5)
ax.axhline(0, color=INK, lw=0.9)
ax.set_xticks([-2*np.pi,-np.pi,0,np.pi,2*np.pi])
ax.set_xticklabels([r'$-2\pi$',r'$-\pi$','0',r'$\pi$',r'$2\pi$'])
ax.set_ylim(-1.85,1.5); ax.set_xlim(-2.25*np.pi, 2.25*np.pi)
ax.set_xlabel(r'$\theta$')
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.3)
```

```figure caption="$\tan\theta=1$ has period $\pi$, so its roots are spaced $\pi$ apart: $\theta=n\pi+\pi/4$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,2.6))
for k in (-2,-1,0,1):
    t = np.linspace(k*np.pi-np.pi/2+0.04, k*np.pi+np.pi/2-0.04, 300)
    ax.plot(t, np.tan(t), color=ACCENT, lw=1.8)
    ax.axvline(k*np.pi+np.pi/2, color=GRID, lw=1.0, ls='--')
ax.axhline(1, color='#d9534f', lw=1.2, ls='--')
xs = np.array([k*np.pi+np.pi/4 for k in (-2,-1,0,1)])
ax.plot(xs, np.ones_like(xs), 'o', color='#d9534f', ms=5.5, zorder=5)
for k, x in zip((-2,-1,0,1), xs):
    ax.annotate(f'n={k}', (x,1), textcoords='offset points', xytext=(0,-46),
                ha='center', color=MUTED, fontsize=8.5)
ax.axhline(0, color=INK, lw=0.9)
ax.set_xticks([-2*np.pi,-np.pi,0,np.pi])
ax.set_xticklabels([r'$-2\pi$',r'$-\pi$','0',r'$\pi$'])
ax.set_ylim(-4,4); ax.set_xlim(-2*np.pi-0.3, np.pi+1.9)
ax.set_xlabel(r'$\theta$'); ax.set_ylabel(r'$\tan\theta$')
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.3)
```

::: tip Match the pattern to the function, not to the question
If the last line you reach is a **sine** equation use $n\pi+(-1)^n\alpha$, if it
is a **cosine** equation use $2n\pi\pm\alpha$, if **tangent** use $n\pi+\alpha$.
Converting a sine equation into a cosine one (or the reverse) is allowed and often
tidier, but then you must use the matching formula.
:::

::: example Worked example 10.5 — the three basic forms
**Problem.** Find the general values of $\theta$ if (a) $\sin\theta = \frac{\sqrt{3}}{2}$,
(b) $\cos\theta = -\frac{1}{\sqrt{2}}$, (c) $\tan\theta = -\sqrt{3}$.

**Solution.**

(a) $\frac{\sqrt{3}}{2} = \sin\frac{\pi}{3}$, so $\theta = n\pi+(-1)^{n}\dfrac{\pi}{3}$.

(b) The cosine is negative, so take $\alpha$ in the second quadrant:
$-\frac{1}{\sqrt{2}} = \cos\left(\pi-\frac{\pi}{4}\right) = \cos\frac{3\pi}{4}$.
Hence $\theta = 2n\pi\pm\dfrac{3\pi}{4}$.

(c) $\tan\frac{\pi}{3} = \sqrt{3}$ and tangent is odd, so
$-\sqrt{3} = \tan\left(-\frac{\pi}{3}\right)$ and
$\theta = n\pi-\dfrac{\pi}{3}$.
:::

::: example Worked example 10.6 — squared form
**Problem.** Solve $4\sin^{2}\theta = 3$.

**Solution.** $\sin^{2}\theta = \dfrac34 = \left(\dfrac{\sqrt{3}}{2}\right)^{2} = \sin^{2}\dfrac{\pi}{3}$.

For a squared equation both signs of the ratio are allowed, so the two families
$n\pi+(-1)^n\frac{\pi}{3}$ and $n\pi-(-1)^n\frac{\pi}{3}$ merge into

$$ \theta = n\pi\pm\frac{\pi}{3}, \qquad n\in\mathbb{Z} $$
:::

### Equations of the form $a\cos\theta+b\sin\theta = c$

Divide nothing; instead set $a = r\cos\alpha$ and $b = r\sin\alpha$, so that
$r = \sqrt{a^{2}+b^{2}}$ and $\tan\alpha = b/a$. Then

$$ a\cos\theta+b\sin\theta = r(\cos\alpha\cos\theta+\sin\alpha\sin\theta) = r\cos(\theta-\alpha) $$

and the equation becomes $\cos(\theta-\alpha) = c/r$. A solution exists only if
$|c| \le r = \sqrt{a^{2}+b^{2}}$.

::: example Worked example 10.7
**Problem.** Solve $\sqrt{3}\cos\theta+\sin\theta = 1$.

**Solution.** Here $a=\sqrt{3}$, $b=1$, so $r = \sqrt{3+1} = 2$ and
$\tan\alpha = \dfrac{1}{\sqrt{3}}$, giving $\alpha = \dfrac{\pi}{6}$
(both $a$ and $b$ positive, so $\alpha$ is in quadrant I). The equation becomes

$$ 2\cos\left(\theta-\frac{\pi}{6}\right) = 1
\;\Rightarrow\; \cos\left(\theta-\frac{\pi}{6}\right) = \frac12 = \cos\frac{\pi}{3} $$

$$ \theta-\frac{\pi}{6} = 2n\pi\pm\frac{\pi}{3}
\;\Rightarrow\; \theta = 2n\pi+\frac{\pi}{6}\pm\frac{\pi}{3} $$

Taking the two signs separately,

$$ \theta = 2n\pi+\frac{\pi}{2} \qquad\text{or}\qquad \theta = 2n\pi-\frac{\pi}{6} $$

**Check.** $\theta=\frac{\pi}{2}$: $\sqrt{3}(0)+1 = 1$ ✓.
$\theta=-\frac{\pi}{6}$: $\sqrt{3}\cdot\frac{\sqrt{3}}{2}+\left(-\frac12\right) = \frac32-\frac12 = 1$ ✓.
:::

```figure caption="$\sqrt{3}\cos\theta+\sin\theta$ is the single wave $2\cos(\theta-\pi/6)$ of amplitude 2; the line $y=1$ cuts it twice per period."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.2,2.7))
t = np.linspace(-2.2*np.pi, 2.2*np.pi, 1200)
ax.plot(t, np.sqrt(3)*np.cos(t), color=GRID, lw=1.2, label=r'$\sqrt{3}\cos\theta$')
ax.plot(t, np.sin(t), color=MUTED, lw=1.0, ls=':', label=r'$\sin\theta$')
ax.plot(t, np.sqrt(3)*np.cos(t)+np.sin(t), color=ACCENT, lw=2.2,
        label=r'$2\cos(\theta-\pi/6)$')
ax.axhline(1, color='#d9534f', lw=1.2, ls='--')
xs = []
for n in (-1,0,1):
    xs += [2*n*np.pi+np.pi/2, 2*n*np.pi-np.pi/6]
xs = np.array([x for x in xs if abs(x) < 2.2*np.pi])
ax.plot(xs, np.ones_like(xs), 'o', color='#d9534f', ms=5.5, zorder=6)
ax.annotate('y = 1', (np.pi,1), textcoords='offset points', xytext=(0,7),
            ha='center', color='#d9534f', fontsize=9)
ax.axhline(0, color=INK, lw=0.9)
ax.set_xticks([-2*np.pi,-np.pi,0,np.pi,2*np.pi])
ax.set_xticklabels([r'$-2\pi$',r'$-\pi$','0',r'$\pi$',r'$2\pi$'])
ax.set_ylim(-2.6,3.4); ax.set_xlim(-2.25*np.pi,2.25*np.pi)
ax.set_xlabel(r'$\theta$')
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.3)
ax.legend(loc='upper center', ncol=3, fontsize=8.0, columnspacing=1.0)
```

### Sums of sines and cosines

::: example Worked example 10.8
**Problem.** Solve $\sin\theta+\sin 3\theta+\sin 5\theta = 0$.

**Solution.** Group the outer two and use
$\sin C+\sin D = 2\sin\frac{C+D}{2}\cos\frac{C-D}{2}$:

$$ \sin\theta+\sin 5\theta = 2\sin 3\theta\cos 2\theta $$

so the equation becomes

$$ 2\sin 3\theta\cos 2\theta+\sin 3\theta = 0
\;\Rightarrow\; \sin 3\theta\,(2\cos 2\theta+1) = 0 $$

**Either** $\sin 3\theta = 0 \Rightarrow 3\theta = n\pi \Rightarrow \theta = \dfrac{n\pi}{3}$,

**or** $\cos 2\theta = -\dfrac12 = \cos\dfrac{2\pi}{3}
\Rightarrow 2\theta = 2n\pi\pm\dfrac{2\pi}{3} \Rightarrow \theta = n\pi\pm\dfrac{\pi}{3}$.
:::

::: example Worked example 10.9
**Problem.** Solve $\cos\theta+\cos 2\theta+\cos 3\theta = 0$.

**Solution.** Group the first and third:
$\cos\theta+\cos 3\theta = 2\cos 2\theta\cos\theta$. Hence

$$ 2\cos 2\theta\cos\theta+\cos 2\theta = 0
\;\Rightarrow\; \cos 2\theta\,(2\cos\theta+1) = 0 $$

**Either** $\cos 2\theta = 0 \Rightarrow 2\theta = (2n+1)\dfrac{\pi}{2}
\Rightarrow \theta = (2n+1)\dfrac{\pi}{4}$,

**or** $\cos\theta = -\dfrac12 = \cos\dfrac{2\pi}{3} \Rightarrow \theta = 2n\pi\pm\dfrac{2\pi}{3}$.
:::

::: example Worked example 10.10 — sine equals cosine
**Problem.** Solve $\sin 2\theta = \cos 3\theta$.

**Solution.** Convert the sine into a cosine using
$\sin x = \cos\left(\frac{\pi}{2}-x\right)$:

$$ \cos\left(\frac{\pi}{2}-2\theta\right) = \cos 3\theta $$

By the cosine rule for general values, $3\theta = 2n\pi\pm\left(\dfrac{\pi}{2}-2\theta\right)$.

**Plus sign:** $3\theta = 2n\pi+\dfrac{\pi}{2}-2\theta \Rightarrow 5\theta = 2n\pi+\dfrac{\pi}{2}
\Rightarrow \theta = \dfrac{(4n+1)\pi}{10}$.

**Minus sign:** $3\theta = 2n\pi-\dfrac{\pi}{2}+2\theta \Rightarrow \theta = 2n\pi-\dfrac{\pi}{2}$.

**Check.** $n=0$ in the first family gives $\theta = \frac{\pi}{10}$:
$\sin\frac{\pi}{5} = 0.5878$ and $\cos\frac{3\pi}{10} = 0.5878$ ✓.
:::

::: example Worked example 10.11
**Problem.** Solve $\tan\theta+\tan 2\theta+\tan 3\theta = \tan\theta\,\tan 2\theta\,\tan 3\theta$.

**Solution.** Collect the $\tan 3\theta$ terms:

$$ \tan\theta+\tan 2\theta = \tan 3\theta\,(\tan\theta\tan 2\theta-1)
= -\tan 3\theta\,(1-\tan\theta\tan 2\theta) $$

Provided $1-\tan\theta\tan 2\theta \ne 0$, divide by it:

$$ \frac{\tan\theta+\tan 2\theta}{1-\tan\theta\tan 2\theta} = -\tan 3\theta $$

The left side is $\tan(\theta+2\theta) = \tan 3\theta$, so
$\tan 3\theta = -\tan 3\theta$, i.e. $2\tan 3\theta = 0$.

Hence $\tan 3\theta = 0 \Rightarrow 3\theta = n\pi \Rightarrow \theta = \dfrac{n\pi}{3}$.

**Check.** $\theta = \frac{\pi}{3}$: $\tan\frac{\pi}{3}+\tan\frac{2\pi}{3}+\tan\pi = \sqrt{3}-\sqrt{3}+0 = 0$,
and the product is also $0$ ✓.
:::

::: example Worked example 10.12 — factorise, never cancel
**Problem.** Solve $\sin 2\theta = \sin\theta$.

**Solution.** Write $\sin 2\theta = 2\sin\theta\cos\theta$ and bring everything to
one side:

$$ 2\sin\theta\cos\theta-\sin\theta = 0 \;\Rightarrow\; \sin\theta\,(2\cos\theta-1) = 0 $$

**Either** $\sin\theta = 0 \Rightarrow \theta = n\pi$,
**or** $\cos\theta = \dfrac12 \Rightarrow \theta = 2n\pi\pm\dfrac{\pi}{3}$.

Cancelling $\sin\theta$ at the start would have lost the entire family
$\theta = n\pi$ — a guaranteed loss of marks.
:::

## Chapter summary

- A trigonometric equation has infinitely many roots; the answer required is the
  **general value**, with $n\in\mathbb{Z}$ stated.
- $\sin\theta=\sin\alpha \Rightarrow \theta = n\pi+(-1)^{n}\alpha$;
  $\cos\theta=\cos\alpha \Rightarrow \theta = 2n\pi\pm\alpha$;
  $\tan\theta=\tan\alpha \Rightarrow \theta = n\pi+\alpha$.
- Squared equations $\sin^{2}\theta=\sin^{2}\alpha$ (and the $\cos^2$, $\tan^2$
  versions) all give $\theta = n\pi\pm\alpha$.
- Zero cases: $\sin\theta=0 \Rightarrow \theta=n\pi$;
  $\cos\theta=0 \Rightarrow \theta=(2n+1)\frac{\pi}{2}$;
  $\tan\theta=0 \Rightarrow \theta=n\pi$.
- Quadratics in one ratio: factorise. Mixed $\sin^{2}$/$\cos$: substitute
  $\sin^{2}\theta = 1-\cos^{2}\theta$. Sums of sines or cosines: use
  sum-to-product, then factorise.
- $a\cos\theta+b\sin\theta = c$ becomes $r\cos(\theta-\alpha)=c$ with
  $r=\sqrt{a^{2}+b^{2}}$, $\tan\alpha = b/a$; solvable only if $|c|\le r$.
- Never cancel a common trigonometric factor — factorise and set each factor to
  zero. Always reject roots that need $|\sin\theta|>1$ or $|\cos\theta|>1$.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The general solution of $\cos\theta = 0$ is <span class="marks">[1]</span>
   (a) $n\pi$ (b) $2n\pi$ (c) $(2n+1)\frac{\pi}{2}$ (d) $n\pi+\frac{\pi}{4}$
2. If $\tan\theta = \tan\alpha$ then $\theta$ equals <span class="marks">[1]</span>
   (a) $2n\pi\pm\alpha$ (b) $n\pi+\alpha$ (c) $n\pi+(-1)^{n}\alpha$ (d) $2n\pi+\alpha$
3. The number of roots of $\sin\theta = \frac{1}{2}$ in $[0,2\pi)$ is <span class="marks">[1]</span>
   (a) 1 (b) 2 (c) 3 (d) infinitely many
4. The equation $3\cos\theta+4\sin\theta = 6$ has <span class="marks">[1]</span>
   (a) two roots (b) one root (c) no root (d) infinitely many roots
5. The general solution of $\tan^{2}\theta = 1$ is <span class="marks">[1]</span>
   (a) $n\pi+\frac{\pi}{4}$ (b) $n\pi\pm\frac{\pi}{4}$ (c) $2n\pi\pm\frac{\pi}{4}$ (d) $n\pi$
6. The principal solution of $\sin\theta = -\frac{1}{\sqrt{2}}$ is <span class="marks">[1]</span>
   (a) $\frac{5\pi}{4}$ (b) $\frac{7\pi}{4}$ (c) $-\frac{\pi}{4}$ (d) $\frac{3\pi}{4}$

::: note Answers to Group A
**1.** (c) — the cosine vanishes at every odd multiple of $\frac{\pi}{2}$.
**2.** (b) — tangent has period $\pi$.
**3.** (b) — $\frac{\pi}{6}$ and $\frac{5\pi}{6}$; one root per half-period in $[0,2\pi)$.
**4.** (c) — $r=\sqrt{9+16}=5$ and $6>5$, so no solution exists.
**5.** (b) — squared equations give $\theta = n\pi\pm\alpha$ with $\alpha = \frac{\pi}{4}$.
**6.** (c) — the numerically smallest root; $\sin\left(-\frac{\pi}{4}\right) = -\frac{1}{\sqrt{2}}$.
:::

**Group B — Short answer (5 marks each)**

1. Prove that if $\sin\theta = \sin\alpha$ then $\theta = n\pi+(-1)^{n}\alpha$,
   $n\in\mathbb{Z}$. <span class="marks">[5]</span>
2. Solve $2\cos^{2}\theta+\sin\theta-1 = 0$. <span class="marks">[5]</span>
3. Solve $\cos\theta+\cos 3\theta = 2\cos 2\theta$. <span class="marks">[5]</span>
4. Solve $\cos\theta-\sqrt{3}\sin\theta = 1$. <span class="marks">[5]</span>
5. Find all values of $\theta$ in $0^{\circ}\le\theta\le 360^{\circ}$ satisfying
   $\tan\theta+\sqrt{3} = 0$. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** $\sin\theta-\sin\alpha = 2\cos\frac{\theta+\alpha}{2}\sin\frac{\theta-\alpha}{2} = 0$.
Either $\cos\frac{\theta+\alpha}{2}=0$, giving $\frac{\theta+\alpha}{2}=(2m+1)\frac{\pi}{2}$
and so $\theta = (2m+1)\pi-\alpha$; or $\sin\frac{\theta-\alpha}{2}=0$, giving
$\frac{\theta-\alpha}{2}=m\pi$ and so $\theta = 2m\pi+\alpha$. The first family is
$\theta = (\text{odd }n)\pi-\alpha$ and the second $\theta = (\text{even }n)\pi+\alpha$,
both of which are $\theta = n\pi+(-1)^{n}\alpha$.

**2.** Substitute $\cos^{2}\theta = 1-\sin^{2}\theta$:
$2-2\sin^{2}\theta+\sin\theta-1=0$, i.e. $2\sin^{2}\theta-\sin\theta-1=0$.
Factorising, $(2\sin\theta+1)(\sin\theta-1)=0$.
If $\sin\theta = 1 = \sin\frac{\pi}{2}$ then $\theta = n\pi+(-1)^{n}\frac{\pi}{2}$.
If $\sin\theta = -\frac12 = \sin\left(-\frac{\pi}{6}\right)$ then
$\theta = n\pi+(-1)^{n}\left(-\frac{\pi}{6}\right) = n\pi-(-1)^{n}\frac{\pi}{6}$.

**3.** $\cos\theta+\cos 3\theta = 2\cos 2\theta\cos\theta$, so the equation is
$2\cos 2\theta\cos\theta = 2\cos 2\theta$, i.e. $2\cos 2\theta(\cos\theta-1)=0$.
Either $\cos 2\theta = 0 \Rightarrow 2\theta = (2n+1)\frac{\pi}{2} \Rightarrow
\theta = (2n+1)\frac{\pi}{4}$; or $\cos\theta = 1 \Rightarrow \theta = 2n\pi$.

**4.** $r = \sqrt{1^{2}+(-\sqrt{3})^{2}} = 2$, and with $a=1$, $b=-\sqrt{3}$ we have
$\tan\alpha = -\sqrt{3}$ with $\cos\alpha>0$, so $\alpha = -\frac{\pi}{3}$. Then
$2\cos\left(\theta+\frac{\pi}{3}\right) = 1$, i.e.
$\cos\left(\theta+\frac{\pi}{3}\right) = \frac12 = \cos\frac{\pi}{3}$.
So $\theta+\frac{\pi}{3} = 2n\pi\pm\frac{\pi}{3}$, giving
$\theta = 2n\pi$ or $\theta = 2n\pi-\frac{2\pi}{3}$.
Check $\theta = -\frac{2\pi}{3}$: $\cos = -\frac12$, $\sin = -\frac{\sqrt{3}}{2}$,
so LHS $= -\frac12+\frac{3}{2} = 1$ ✓.

**5.** $\tan\theta = -\sqrt{3} = \tan(-60^{\circ})$, so the general value is
$\theta = n\cdot 180^{\circ}-60^{\circ}$. Taking $n=1$ and $n=2$ gives the values in
range: $\theta = 120^{\circ}$ and $\theta = 300^{\circ}$. (Tangent is negative in
quadrants II and IV, which is exactly where these lie.)
:::

**Group C — Long answer (8 marks each)**

1. (a) Derive the general solution of $\cos\theta = \cos\alpha$. <span class="marks">[4]</span>
   (b) Hence solve $\cos\theta+\cos 2\theta+\cos 3\theta = 0$. <span class="marks">[4]</span>
2. (a) Show that $a\cos\theta+b\sin\theta$ can be written as $r\cos(\theta-\alpha)$
   and state the condition for $a\cos\theta+b\sin\theta = c$ to be solvable. <span class="marks">[3]</span>
   (b) Solve $\sin\theta+\sin 2\theta+\sin 3\theta = 0$. <span class="marks">[5]</span>

::: note Answers to Group C
**1.** (a) $\cos\theta-\cos\alpha = -2\sin\frac{\theta+\alpha}{2}\sin\frac{\theta-\alpha}{2} = 0$.
So $\sin\frac{\theta+\alpha}{2}=0$, giving $\frac{\theta+\alpha}{2}=m\pi$ and
$\theta = 2m\pi-\alpha$; or $\sin\frac{\theta-\alpha}{2}=0$, giving
$\theta = 2m\pi+\alpha$. Combining the two, $\theta = 2n\pi\pm\alpha$, $n\in\mathbb{Z}$.

(b) $\cos\theta+\cos 3\theta = 2\cos 2\theta\cos\theta$, so the equation is
$\cos 2\theta(2\cos\theta+1)=0$.
Either $\cos 2\theta = 0 \Rightarrow \theta = (2n+1)\frac{\pi}{4}$,
or $\cos\theta = -\frac12 = \cos\frac{2\pi}{3} \Rightarrow \theta = 2n\pi\pm\frac{2\pi}{3}$.

**2.** (a) Choose $r>0$ and $\alpha$ with $a = r\cos\alpha$ and $b = r\sin\alpha$.
Squaring and adding, $a^{2}+b^{2} = r^{2}$, so $r=\sqrt{a^{2}+b^{2}}$; dividing,
$\tan\alpha = b/a$. Then
$a\cos\theta+b\sin\theta = r(\cos\alpha\cos\theta+\sin\alpha\sin\theta) = r\cos(\theta-\alpha)$.
Since $|\cos(\theta-\alpha)|\le 1$, the equation $r\cos(\theta-\alpha)=c$ has a
solution only when $|c|\le\sqrt{a^{2}+b^{2}}$.

(b) $\sin\theta+\sin 3\theta = 2\sin 2\theta\cos\theta$, so
$2\sin 2\theta\cos\theta+\sin 2\theta = 0$, i.e. $\sin 2\theta(2\cos\theta+1)=0$.
Either $\sin 2\theta = 0 \Rightarrow 2\theta = n\pi \Rightarrow \theta = \frac{n\pi}{2}$,
or $\cos\theta = -\frac12 \Rightarrow \theta = 2n\pi\pm\frac{2\pi}{3}$.
Check $\theta = \frac{\pi}{2}$: $1+0-1 = 0$ ✓; check $\theta = \frac{2\pi}{3}$:
$\frac{\sqrt{3}}{2}-\frac{\sqrt{3}}{2}+0 = 0$ ✓.
:::
