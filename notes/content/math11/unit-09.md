---
subject: Mathematics
grade: 11
unit: 9
title: Inverse Circular Functions
hours: 6
area: Trigonometry
---

The sine function turns an angle into a ratio. This unit runs the machine
backwards: given the ratio, find the angle. Because $\sin\theta$ repeats every
$2\pi$, "the angle whose sine is $1/2$" has infinitely many answers, so before we
can speak of *the* inverse we must cut the domain down to a piece on which the
function is one-to-one. That single idea — **restrict, then invert** — controls
every domain, range and identity in this chapter.

::: key What the exam asks
Three question types cover almost everything: (i) state or evaluate a **principal
value**, (ii) **prove an identity** such as
$\tan^{-1}x+\tan^{-1}y=\tan^{-1}\frac{x+y}{1-xy}$, and (iii) **solve an equation**
in inverse functions. Every proof is worth marks line by line, so write the
substitution ("let $\tan^{-1}x = A$") explicitly.
:::

## 9.1 Definition, domain and range of inverse circular functions

### Why a restriction is needed

A function has an inverse only if it is **one-to-one** (each output comes from
exactly one input). Over its natural domain $\mathbb{R}$ the sine function is not
one-to-one: the horizontal line $y = 1/2$ cuts $y=\sin x$ infinitely often. But on
the single branch $-\pi/2 \le x \le \pi/2$ the sine rises steadily from $-1$ to
$+1$ and meets every horizontal line $y=k$, $-1\le k\le 1$, exactly once. That
branch is called the **principal branch**.

```figure caption="$y=\sin x$ meets $y=\tfrac12$ infinitely often, but exactly once on the shaded principal branch $-\pi/2\le x\le\pi/2$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,2.7))
x = np.linspace(-2.2*np.pi, 2.2*np.pi, 1200)
ax.plot(x, np.sin(x), color=MUTED, lw=1.2)
xb = np.linspace(-np.pi/2, np.pi/2, 300)
ax.plot(xb, np.sin(xb), color=ACCENT, lw=2.6, zorder=4)
ax.axvspan(-np.pi/2, np.pi/2, color=ACCENT, alpha=0.10, zorder=0)
ax.axhline(0.5, color='#d9534f', lw=1.1, ls='--')
xs = np.array([np.pi/6, 5*np.pi/6, np.pi/6-2*np.pi, 5*np.pi/6-2*np.pi,
               np.pi/6+2*np.pi, 5*np.pi/6+2*np.pi])
xs = xs[np.abs(xs) < 2.2*np.pi]
ax.plot(xs, 0.5*np.ones_like(xs), 'o', color='#d9534f', ms=4.5, zorder=5)
ax.plot([np.pi/6],[0.5],'o',color=ACCENT, ms=6.5, zorder=6)
ax.annotate(r'$x=\pi/6$', (np.pi/6,0.5), textcoords='offset points',
            xytext=(30,-54), color=ACCENT, fontsize=9,
            arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.0, mutation_scale=9))
ax.annotate('y = 1/2', (2.05*np.pi, 0.5), textcoords='offset points',
            xytext=(-6,7), color='#d9534f', fontsize=9, ha='right')
ax.set_xticks([-2*np.pi,-np.pi,-np.pi/2,0,np.pi/2,np.pi,2*np.pi])
ax.set_xticklabels([r'$-2\pi$',r'$-\pi$',r'$-\frac{\pi}{2}$','0',
                    r'$\frac{\pi}{2}$',r'$\pi$',r'$2\pi$'])
ax.set_yticks([-1,0,1]); ax.set_ylim(-1.5,1.6)
ax.axhline(0, color=INK, lw=0.8)
ax.set_xlabel('$x$'); ax.set_ylabel('$y$')
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.35)
```

Restricting the domain to the principal branch makes the inverse a genuine
function. Its graph is the mirror image of the branch in the line $y=x$, because
reflecting in $y=x$ interchanges the roles of input and output.

::: definition Inverse sine
For $-1 \le x \le 1$, $\sin^{-1}x$ (read "arc sine $x$") is the **unique** angle
$y$ with $-\dfrac{\pi}{2} \le y \le \dfrac{\pi}{2}$ such that $\sin y = x$. That
unique value is called the **principal value**.
:::

```figure caption="The principal branch of $\sin$ (grey) reflected in $y=x$ (dotted) gives $y=\sin^{-1}x$ (blue): domain $[-1,1]$, range $[-\pi/2,\pi/2]$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.4,3.4))
t = np.linspace(-np.pi/2, np.pi/2, 400)
ax.plot(t, np.sin(t), color=MUTED, lw=1.8, label=r'$y=\sin x$ on $[-\pi/2,\pi/2]$')
ax.plot(np.sin(t), t, color=ACCENT, lw=2.4, label=r'$y=\sin^{-1}x$')
d = np.linspace(-1.75,1.75,10)
ax.plot(d, d, color=INK, lw=0.9, ls=':')
ax.annotate('y = x', (1.55,1.55), textcoords='offset points', xytext=(-4,4),
            color=INK, fontsize=8.5, ha='right')
ax.axhline(np.pi/2, color=GRID, lw=1.0); ax.axhline(-np.pi/2, color=GRID, lw=1.0)
ax.axvline(1, color=GRID, lw=1.0); ax.axvline(-1, color=GRID, lw=1.0)
ax.axhline(0, color=INK, lw=0.8); ax.axvline(0, color=INK, lw=0.8)
ax.set_xticks([-1,1]); ax.set_yticks([-np.pi/2,np.pi/2])
ax.set_yticklabels([r'$-\pi/2$',r'$\pi/2$'])
ax.set_xlim(-1.85,1.85); ax.set_ylim(-1.85,1.85); ax.set_aspect('equal')
ax.spines[['top','right']].set_visible(False)
ax.legend(loc='upper left', fontsize=8.2)
```

The same programme is carried out for the other five functions. For cosine the
chosen branch is $0 \le x \le \pi$ (on $[-\pi/2,\pi/2]$ the cosine is *not*
one-to-one, since $\cos(-x)=\cos x$). For tangent it is the open interval
$-\pi/2 < x < \pi/2$, on which $\tan x$ sweeps once through all of $\mathbb{R}$.

```figure caption="Principal branch of $\cos$ on $[0,\pi]$ and its reflection $y=\cos^{-1}x$, range $[0,\pi]$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.4,3.4))
x = np.linspace(-1.3*np.pi, 1.6*np.pi, 900)
ax.plot(x, np.cos(x), color=GRID, lw=1.1)
t = np.linspace(0, np.pi, 400)
ax.plot(t, np.cos(t), color=MUTED, lw=1.9, label=r'$y=\cos x,\ 0\leq x\leq\pi$')
ax.plot(np.cos(t), t, color=ACCENT, lw=2.4, label=r'$y=\cos^{-1}x$')
ax.axvspan(0, np.pi, color=ACCENT, alpha=0.07, zorder=0)
d = np.linspace(-1.2,3.4,10); ax.plot(d,d,color=INK,lw=0.9,ls=':')
ax.axhline(0, color=INK, lw=0.8); ax.axvline(0, color=INK, lw=0.8)
ax.set_xticks([-1,1,np.pi]); ax.set_xticklabels(['-1','1',r'$\pi$'])
ax.set_yticks([np.pi/2,np.pi]); ax.set_yticklabels([r'$\pi/2$',r'$\pi$'])
ax.set_xlim(-1.9,3.5); ax.set_ylim(-1.9,3.5); ax.set_aspect('equal')
ax.spines[['top','right']].set_visible(False)
ax.legend(loc='lower right', fontsize=8.2)
```

```figure caption="$y=\tan^{-1}x$ has domain $\mathbb{R}$ and range the open interval $(-\pi/2,\pi/2)$; the lines $y=\pm\pi/2$ are horizontal asymptotes."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,3.0))
t = np.linspace(-np.pi/2+0.02, np.pi/2-0.02, 600)
ax.plot(t, np.tan(t), color=MUTED, lw=1.7, label=r'$y=\tan x$ on $(-\pi/2,\pi/2)$')
ax.plot(np.tan(t), t, color=ACCENT, lw=2.4, label=r'$y=\tan^{-1}x$')
for s in (1,-1):
    ax.axhline(s*np.pi/2, color='#d9534f', lw=1.0, ls='--')
    ax.axvline(s*np.pi/2, color=GRID, lw=1.0, ls='--')
ax.annotate(r'$y=\pi/2$', (5.6,np.pi/2), textcoords='offset points',
            xytext=(-2,5), color='#d9534f', fontsize=8.6, ha='right')
ax.annotate(r'$y=-\pi/2$', (5.6,-np.pi/2), textcoords='offset points',
            xytext=(-2,-13), color='#d9534f', fontsize=8.6, ha='right')
d = np.linspace(-5,5,10); ax.plot(d,d,color=INK,lw=0.9,ls=':')
ax.axhline(0,color=INK,lw=0.8); ax.axvline(0,color=INK,lw=0.8)
ax.set_xlim(-6,6); ax.set_ylim(-4.2,4.2)
ax.set_yticks([-np.pi/2,0,np.pi/2]); ax.set_yticklabels([r'$-\pi/2$','0',r'$\pi/2$'])
ax.set_xlabel('$x$')
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.3)
ax.legend(loc='lower right', fontsize=8.2)
```

### The six inverse circular functions

| Function | Domain | Range (principal values) |
|---|---|---|
| $\sin^{-1}x$ | $-1 \le x \le 1$ | $-\frac{\pi}{2} \le y \le \frac{\pi}{2}$ |
| $\cos^{-1}x$ | $-1 \le x \le 1$ | $0 \le y \le \pi$ |
| $\tan^{-1}x$ | $x \in \mathbb{R}$ | $-\frac{\pi}{2} < y < \frac{\pi}{2}$ |
| $\cot^{-1}x$ | $x \in \mathbb{R}$ | $0 < y < \pi$ |
| $\sec^{-1}x$ | $|x| \ge 1$ | $0 \le y \le \pi$, $y \ne \frac{\pi}{2}$ |
| $\csc^{-1}x$ | $|x| \ge 1$ | $-\frac{\pi}{2} \le y \le \frac{\pi}{2}$, $y \ne 0$ |

Two patterns make this table easy to remember.

::: memory Ranges in two groups
- **Sine family** ($\sin^{-1}$, $\csc^{-1}$, $\tan^{-1}$): range centred on $0$,
  from $-\pi/2$ to $\pi/2$. Negative inputs give **negative** answers.
- **Cosine family** ($\cos^{-1}$, $\sec^{-1}$, $\cot^{-1}$): range from $0$ to
  $\pi$. Negative inputs give answers in the **second quadrant**.
:::

::: caution Three notation traps
1. $\sin^{-1}x$ is an **angle**, not $\dfrac{1}{\sin x}$. The reciprocal is
   $\csc x$. Write $(\sin x)^{-1}$ if you mean the reciprocal.
2. $\sin^{-1}x$ is undefined for $|x|>1$: "$\sin^{-1}2$" does not exist.
3. $\sin^{-1}(\sin x) = x$ **only** when $-\pi/2 \le x \le \pi/2$. Outside that
   interval you must first replace $x$ by an angle inside the range with the same
   sine.
:::

::: example Worked example 9.1 — principal values
**Problem.** Find the principal values of (a) $\sin^{-1}\left(-\frac{1}{2}\right)$,
(b) $\cos^{-1}\left(-\frac{\sqrt{3}}{2}\right)$, (c) $\tan^{-1}(-1)$,
(d) $\cot^{-1}(-1)$, (e) $\sec^{-1}(-2)$.

**Solution.**

(a) We need $y$ with $\sin y = -\frac12$ and $-\frac{\pi}{2}\le y\le\frac{\pi}{2}$.
Since $\sin\frac{\pi}{6}=\frac12$, oddness gives $\sin\left(-\frac{\pi}{6}\right)=-\frac12$.
So $\sin^{-1}\left(-\frac12\right) = -\dfrac{\pi}{6}$.

(b) Here $y$ must lie in $[0,\pi]$, so $y$ is in the **second** quadrant.
$\cos\frac{\pi}{6}=\frac{\sqrt{3}}{2}$, and $\cos\left(\pi-\frac{\pi}{6}\right)=-\frac{\sqrt{3}}{2}$.
Hence $\cos^{-1}\left(-\frac{\sqrt{3}}{2}\right) = \dfrac{5\pi}{6}$.

(c) $\tan^{-1}$ has range $\left(-\frac{\pi}{2},\frac{\pi}{2}\right)$ and
$\tan\left(-\frac{\pi}{4}\right)=-1$, so $\tan^{-1}(-1) = -\dfrac{\pi}{4}$.

(d) $\cot^{-1}$ has range $(0,\pi)$, so the answer is in the second quadrant:
$\cot\frac{3\pi}{4} = -1$, giving $\cot^{-1}(-1) = \dfrac{3\pi}{4}$.

(e) $\sec^{-1}(-2) = \cos^{-1}\left(-\frac12\right) = \dfrac{2\pi}{3}$.
:::

::: example Worked example 9.2 — domain of a composite
**Problem.** Find the domain of (a) $f(x) = \sin^{-1}(2x-1)$ and
(b) $g(x) = \cos^{-1}(3-2x)$.

**Solution.**

(a) The input of $\sin^{-1}$ must lie in $[-1,1]$:

$$ -1 \le 2x-1 \le 1 \;\Rightarrow\; 0 \le 2x \le 2 \;\Rightarrow\; 0 \le x \le 1 $$

Domain $= [0,1]$.

(b) Similarly $-1 \le 3-2x \le 1$. Subtract $3$: $-4 \le -2x \le -2$. Divide by
$-2$ and **reverse the inequalities**: $1 \le x \le 2$. Domain $=[1,2]$.
:::

::: example Worked example 9.3 — undoing a function outside its range
**Problem.** Evaluate (a) $\sin^{-1}\left(\sin\frac{5\pi}{6}\right)$,
(b) $\cos^{-1}\left(\cos\frac{7\pi}{6}\right)$,
(c) $\tan^{-1}\left(\tan\frac{3\pi}{4}\right)$.

**Solution.**

(a) $\frac{5\pi}{6} \notin \left[-\frac{\pi}{2},\frac{\pi}{2}\right]$, so we cannot
cancel. Instead $\sin\frac{5\pi}{6}=\sin\left(\pi-\frac{5\pi}{6}\right)=\sin\frac{\pi}{6}$,
and $\frac{\pi}{6}$ **is** in the range. Answer $\dfrac{\pi}{6}$.

(b) $\frac{7\pi}{6} \notin [0,\pi]$. Use $\cos\frac{7\pi}{6}=\cos\left(2\pi-\frac{7\pi}{6}\right)=\cos\frac{5\pi}{6}$,
and $\frac{5\pi}{6}\in[0,\pi]$. Answer $\dfrac{5\pi}{6}$.

(c) $\tan\frac{3\pi}{4} = \tan\left(\frac{3\pi}{4}-\pi\right) = \tan\left(-\frac{\pi}{4}\right)$,
and $-\frac{\pi}{4}$ is in the range. Answer $-\dfrac{\pi}{4}$.
:::

### The right-triangle picture

Almost every evaluation question becomes trivial with one sketch. If
$\theta = \sin^{-1}x$ with $0\le x\le 1$, draw a right triangle with hypotenuse
$1$ and opposite side $x$; Pythagoras gives the adjacent side $\sqrt{1-x^2}$, and
then **every** ratio of $\theta$ can be read off.

```figure caption="If $\theta=\sin^{-1}x$ then $\cos\theta=\sqrt{1-x^{2}}$ and $\tan\theta=x/\sqrt{1-x^{2}}$ — read straight off the triangle."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.2,2.5))
A=np.array([0,0]); B=np.array([3.0,0]); C=np.array([3.0,1.7])
ax.plot([A[0],B[0],C[0],A[0]],[A[1],B[1],C[1],A[1]], color=ACCENT, lw=2.0)
ax.plot([2.74,2.74,3.0],[0,0.26,0.26], color=MUTED, lw=1.0)
th = np.linspace(0, np.arctan2(1.7,3.0), 40)
ax.plot(0.72*np.cos(th), 0.72*np.sin(th), color='#d9534f', lw=1.2)
ax.annotate(r'$\theta$', (0.88,0.20), color='#d9534f', fontsize=11)
ax.annotate(r'$\sqrt{1-x^{2}}$', (1.5,-0.02), ha='center', va='top',
            color=INK, fontsize=10)
ax.annotate(r'$x$', (3.08,0.85), ha='left', va='center', color=INK, fontsize=11)
ax.annotate(r'$1$', (1.4,1.05), ha='center', va='bottom', color=INK, fontsize=11,
            rotation=29.5)
ax.set_xlim(-0.35,3.9); ax.set_ylim(-0.55,2.1); ax.set_aspect('equal')
ax.axis('off')
```

::: example Worked example 9.4 — evaluation by triangle
**Problem.** Evaluate (a) $\cos\left(\sin^{-1}\frac{3}{5}\right)$,
(b) $\tan\left(\sin^{-1}\frac{3}{5}+\cot^{-1}\frac{3}{2}\right)$.

**Solution.**

(a) Let $A = \sin^{-1}\frac35$, so $\sin A = \frac35$ with $A$ in the first
quadrant. Then $\cos A = \sqrt{1-\frac{9}{25}} = \frac45$ (positive, because
$A\in\left[0,\frac{\pi}{2}\right]$). So the value is $\dfrac{4}{5}$.

(b) With $A$ as above, $\tan A = \dfrac{3/5}{4/5} = \dfrac34$. Let
$B = \cot^{-1}\frac32$, so $\cot B = \frac32$ and $\tan B = \frac23$. Then

$$ \tan(A+B) = \frac{\tan A + \tan B}{1-\tan A\tan B} = \frac{\frac34+\frac23}{1-\frac34\cdot\frac23} = \frac{\frac{17}{12}}{\frac12} = \frac{17}{6} $$
:::

## 9.2 Formulae and identities of inverse circular functions

### Complementary pairs

::: derivation $\sin^{-1}x + \cos^{-1}x = \dfrac{\pi}{2}$
Let $\sin^{-1}x = \theta$. Then $\sin\theta = x$ and $-\dfrac{\pi}{2}\le\theta\le\dfrac{\pi}{2}$.

Using $\cos\left(\dfrac{\pi}{2}-\theta\right) = \sin\theta = x$,

$$ \cos\left(\frac{\pi}{2}-\theta\right) = x $$

Now check the range: from $-\frac{\pi}{2}\le\theta\le\frac{\pi}{2}$ we get
$0 \le \dfrac{\pi}{2}-\theta \le \pi$, which is exactly the range of $\cos^{-1}$.
Therefore $\dfrac{\pi}{2}-\theta$ **is** the principal value:

$$ \cos^{-1}x = \frac{\pi}{2}-\theta = \frac{\pi}{2}-\sin^{-1}x
\;\Longrightarrow\; \sin^{-1}x+\cos^{-1}x = \frac{\pi}{2} $$

The identical argument with $\tan/\cot$ and $\sec/\csc$ gives the other two.
:::

::: key The complementary identities
$$ \sin^{-1}x+\cos^{-1}x = \frac{\pi}{2}\quad (|x|\le 1) $$
$$ \tan^{-1}x+\cot^{-1}x = \frac{\pi}{2}\quad (x\in\mathbb{R}) $$
$$ \sec^{-1}x+\csc^{-1}x = \frac{\pi}{2}\quad (|x|\ge 1) $$
:::

```figure caption="$\sin^{-1}x$ and $\cos^{-1}x$ always add to the constant $\pi/2$ — the dashed sum is a horizontal line."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,2.8))
x = np.linspace(-1,1,400)
ax.plot(x, np.arcsin(x), color=ACCENT, lw=2.0, label=r'$\sin^{-1}x$')
ax.plot(x, np.arccos(x), color='#2e8b57', lw=2.0, label=r'$\cos^{-1}x$')
ax.plot(x, np.arcsin(x)+np.arccos(x), color='#d9534f', lw=1.8, ls='--',
        label=r'sum $=\pi/2$')
ax.axhline(0, color=INK, lw=0.8); ax.axvline(0, color=INK, lw=0.8)
ax.set_yticks([-np.pi/2,0,np.pi/2,np.pi])
ax.set_yticklabels([r'$-\pi/2$','0',r'$\pi/2$',r'$\pi$'])
ax.set_xticks([-1,-0.5,0,0.5,1])
ax.set_xlabel('$x$'); ax.set_ylim(-2.0,3.6); ax.set_xlim(-1.15,1.15)
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.35)
ax.legend(loc='upper right', fontsize=8.2, ncol=1)
```

### Negative arguments and reciprocals

| Sine family (odd) | Cosine family |
|---|---|
| $\sin^{-1}(-x) = -\sin^{-1}x$ | $\cos^{-1}(-x) = \pi-\cos^{-1}x$ |
| $\tan^{-1}(-x) = -\tan^{-1}x$ | $\cot^{-1}(-x) = \pi-\cot^{-1}x$ |
| $\csc^{-1}(-x) = -\csc^{-1}x$ | $\sec^{-1}(-x) = \pi-\sec^{-1}x$ |

And the reciprocal rules, valid for $x>0$:

$$ \sin^{-1}\frac{1}{x} = \csc^{-1}x, \qquad \cos^{-1}\frac{1}{x} = \sec^{-1}x,
\qquad \tan^{-1}\frac{1}{x} = \cot^{-1}x $$

### Addition formulae for $\tan^{-1}$

::: derivation $\tan^{-1}x+\tan^{-1}y$
Put $A = \tan^{-1}x$ and $B = \tan^{-1}y$, so $\tan A = x$, $\tan B = y$ and both
$A,B \in\left(-\frac{\pi}{2},\frac{\pi}{2}\right)$. By the compound-angle formula,

$$ \tan(A+B) = \frac{\tan A+\tan B}{1-\tan A\tan B} = \frac{x+y}{1-xy} $$

so $A+B$ is *an* angle whose tangent is $\dfrac{x+y}{1-xy}$. It is the **principal**
value only if $A+B$ itself lies in $\left(-\frac{\pi}{2},\frac{\pi}{2}\right)$, and
that happens exactly when $xy<1$. Hence

$$ \tan^{-1}x+\tan^{-1}y = \tan^{-1}\frac{x+y}{1-xy} \qquad (xy<1) $$

If $xy>1$ the sum has overshot the principal range by $\pi$, so a correction term
is needed:

$$ \tan^{-1}x+\tan^{-1}y = \pi+\tan^{-1}\frac{x+y}{1-xy}\quad (x>0,\,y>0,\,xy>1) $$
$$ \tan^{-1}x+\tan^{-1}y = -\pi+\tan^{-1}\frac{x+y}{1-xy}\quad (x<0,\,y<0,\,xy>1) $$

Replacing $y$ by $-y$ gives the subtraction rule
$\tan^{-1}x-\tan^{-1}y = \tan^{-1}\dfrac{x-y}{1+xy}$, valid when $xy>-1$.
:::

::: caution The $xy<1$ condition is worth marks
Writing $\tan^{-1}2+\tan^{-1}3 = \tan^{-1}\frac{5}{1-6} = \tan^{-1}(-1) = -\frac{\pi}{4}$
is wrong: two positive angles cannot add to a negative one. Here $xy = 6 > 1$, so
the answer is $\pi-\frac{\pi}{4} = \frac{3\pi}{4}$. **Always test $xy$ against 1.**
:::

The special case $y = 1/x$ shows the same effect starkly: for $x>0$ the sum is
$+\pi/2$, but for $x<0$ it is $-\pi/2$.

```figure caption="$\tan^{-1}x+\tan^{-1}(1/x)$ equals $\pi/2$ for $x>0$ and $-\pi/2$ for $x<0$: the naive formula ignores the jump at $x=0$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,2.6))
xp = np.linspace(0.02, 6, 400); xn = np.linspace(-6, -0.02, 400)
ax.plot(xp, np.arctan(xp)+np.arctan(1/xp), color=ACCENT, lw=2.4)
ax.plot(xn, np.arctan(xn)+np.arctan(1/xn), color=ACCENT, lw=2.4)
ax.plot([0],[np.pi/2],'o',mfc='white',mec=ACCENT,ms=5.5)
ax.plot([0],[-np.pi/2],'o',mfc='white',mec=ACCENT,ms=5.5)
ax.axhline(0, color=INK, lw=0.8); ax.axvline(0, color=MUTED, lw=0.8, ls=':')
ax.annotate(r'$+\pi/2$', (4.6,np.pi/2), textcoords='offset points', xytext=(0,7),
            color=ACCENT, fontsize=9.5)
ax.annotate(r'$-\pi/2$', (-4.6,-np.pi/2), textcoords='offset points', xytext=(0,-16),
            color=ACCENT, fontsize=9.5)
ax.set_yticks([-np.pi/2,0,np.pi/2]); ax.set_yticklabels([r'$-\pi/2$','0',r'$\pi/2$'])
ax.set_xlabel('$x$'); ax.set_ylim(-2.4,2.4)
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.3)
```

### Sums for $\sin^{-1}$ and $\cos^{-1}$, and the double-angle forms

::: key Standard identities
$$ \sin^{-1}x+\sin^{-1}y = \sin^{-1}\left(x\sqrt{1-y^{2}}+y\sqrt{1-x^{2}}\right) $$
$$ \cos^{-1}x+\cos^{-1}y = \cos^{-1}\left(xy-\sqrt{1-x^{2}}\sqrt{1-y^{2}}\right) $$
$$ 2\tan^{-1}x = \tan^{-1}\frac{2x}{1-x^{2}} = \sin^{-1}\frac{2x}{1+x^{2}} = \cos^{-1}\frac{1-x^{2}}{1+x^{2}} $$
$$ 2\sin^{-1}x = \sin^{-1}\left(2x\sqrt{1-x^{2}}\right), \qquad 2\cos^{-1}x = \cos^{-1}\left(2x^{2}-1\right) $$
Conversions for $0\le x\le 1$:
$$ \sin^{-1}x = \cos^{-1}\sqrt{1-x^{2}} = \tan^{-1}\frac{x}{\sqrt{1-x^{2}}} $$
:::

The $2\tan^{-1}x$ chain comes straight from the $t$-formulae with $t=\tan\theta$:
if $\theta=\tan^{-1}x$ then $\sin 2\theta = \dfrac{2x}{1+x^2}$ and
$\cos 2\theta = \dfrac{1-x^2}{1+x^2}$.

::: example Worked example 9.5
**Problem.** Prove that $\tan^{-1}\dfrac12+\tan^{-1}\dfrac13 = \dfrac{\pi}{4}$.

**Solution.** Here $x=\frac12$, $y=\frac13$, so $xy = \frac16 < 1$ and the plain
formula applies.

$$ \tan^{-1}\frac12+\tan^{-1}\frac13 = \tan^{-1}\frac{\frac12+\frac13}{1-\frac12\cdot\frac13}
= \tan^{-1}\frac{\frac56}{\frac56} = \tan^{-1}1 = \frac{\pi}{4} $$
:::

::: example Worked example 9.6
**Problem.** Prove that $\tan^{-1}1+\tan^{-1}2+\tan^{-1}3 = \pi$.

**Solution.** Take the last two first. With $x=2$, $y=3$ we have $xy=6>1$ and both
are positive, so the correction $+\pi$ is needed:

$$ \tan^{-1}2+\tan^{-1}3 = \pi+\tan^{-1}\frac{2+3}{1-6} = \pi+\tan^{-1}(-1)
= \pi-\frac{\pi}{4} = \frac{3\pi}{4} $$

Adding $\tan^{-1}1 = \dfrac{\pi}{4}$ gives $\dfrac{\pi}{4}+\dfrac{3\pi}{4} = \pi$.
:::

::: example Worked example 9.7
**Problem.** Show that $\tan^{-1}\dfrac12+\tan^{-1}\dfrac15+\tan^{-1}\dfrac18 = \dfrac{\pi}{4}$.

**Solution.** Combine the first two ($xy = \frac{1}{10} < 1$):

$$ \tan^{-1}\frac12+\tan^{-1}\frac15 = \tan^{-1}\frac{\frac12+\frac15}{1-\frac{1}{10}}
= \tan^{-1}\frac{\frac{7}{10}}{\frac{9}{10}} = \tan^{-1}\frac79 $$

Now add $\tan^{-1}\frac18$ (product $\frac{7}{72}<1$):

$$ \tan^{-1}\frac79+\tan^{-1}\frac18 = \tan^{-1}\frac{\frac79+\frac18}{1-\frac{7}{72}}
= \tan^{-1}\frac{\frac{56+9}{72}}{\frac{65}{72}} = \tan^{-1}1 = \frac{\pi}{4} $$
:::

::: example Worked example 9.8
**Problem.** Prove that $\sin^{-1}\dfrac35+\sin^{-1}\dfrac{8}{17} = \sin^{-1}\dfrac{77}{85}$.

**Solution.** Let $A=\sin^{-1}\frac35$ and $B=\sin^{-1}\frac{8}{17}$, both in the
first quadrant. Then $\cos A = \sqrt{1-\frac{9}{25}} = \frac45$ and
$\cos B = \sqrt{1-\frac{64}{289}} = \frac{15}{17}$.

$$ \sin(A+B) = \sin A\cos B+\cos A\sin B = \frac35\cdot\frac{15}{17}+\frac45\cdot\frac{8}{17}
= \frac{45+32}{85} = \frac{77}{85} $$

Since $\sin A = \frac35 < \frac{1}{\sqrt{2}}$ and $\sin B = \frac{8}{17}<\frac{1}{\sqrt{2}}$,
both $A$ and $B$ are less than $\frac{\pi}{4}$, so $A+B<\frac{\pi}{2}$ and $A+B$ is
a principal value. Hence $A+B = \sin^{-1}\dfrac{77}{85}$.
:::

::: example Worked example 9.9
**Problem.** Prove that $\cos^{-1}\dfrac45+\cos^{-1}\dfrac{12}{13} = \cos^{-1}\dfrac{33}{65}$.

**Solution.** Let $A=\cos^{-1}\frac45$, $B=\cos^{-1}\frac{12}{13}$; then
$\sin A = \frac35$ and $\sin B = \frac{5}{13}$ (both positive, first quadrant).

$$ \cos(A+B) = \cos A\cos B-\sin A\sin B = \frac45\cdot\frac{12}{13}-\frac35\cdot\frac{5}{13}
= \frac{48-15}{65} = \frac{33}{65} $$

$A+B$ is a sum of two first-quadrant angles with $\cos(A+B)>0$, so
$0<A+B<\frac{\pi}{2}\subset[0,\pi]$, and therefore $A+B = \cos^{-1}\dfrac{33}{65}$.
:::

::: example Worked example 9.10
**Problem.** Show that $2\tan^{-1}\dfrac13 = \tan^{-1}\dfrac34$, and evaluate
$\sin\left(2\tan^{-1}\frac13\right)$ and $\cos\left(2\sin^{-1}\frac35\right)$.

**Solution.** With $x=\frac13$ (so $|x|<1$):

$$ 2\tan^{-1}\frac13 = \tan^{-1}\frac{2\cdot\frac13}{1-\frac19}
= \tan^{-1}\frac{\frac23}{\frac89} = \tan^{-1}\frac34 $$

Next, $\sin\left(2\tan^{-1}x\right) = \dfrac{2x}{1+x^{2}}
= \dfrac{2/3}{1+1/9} = \dfrac{2/3}{10/9} = \dfrac35$.

Finally, if $\theta=\sin^{-1}\frac35$ then $\cos 2\theta = 1-2\sin^{2}\theta
= 1-2\cdot\frac{9}{25} = \dfrac{7}{25}$.
:::

::: example Worked example 9.11 — solving an equation
**Problem.** Solve $\tan^{-1}2x+\tan^{-1}3x = \dfrac{\pi}{4}$.

**Solution.** Assume first that $(2x)(3x) = 6x^{2} < 1$, so the plain formula holds:

$$ \tan^{-1}\frac{2x+3x}{1-6x^{2}} = \frac{\pi}{4}
\;\Rightarrow\; \frac{5x}{1-6x^{2}} = \tan\frac{\pi}{4} = 1 $$

$$ 5x = 1-6x^{2} \;\Rightarrow\; 6x^{2}+5x-1 = 0 \;\Rightarrow\; (6x-1)(x+1)=0 $$

so $x = \frac16$ or $x = -1$.

**Check.** $x=\frac16$: $6x^{2} = \frac16 < 1$ and
$\tan^{-1}\frac13+\tan^{-1}\frac12 = \frac{\pi}{4}$ by Example 9.5 — valid.
$x=-1$: then $\tan^{-1}(-2)+\tan^{-1}(-3)$ is a sum of two negative angles, which
cannot equal $+\frac{\pi}{4}$ — reject.

$$ \boxed{x = \tfrac16} $$
:::

::: example Worked example 9.12 — solving with the complementary identity
**Problem.** Solve (a) $\cos^{-1}x-\sin^{-1}x = \dfrac{\pi}{6}$ and
(b) $\sin^{-1}(1-x)-2\sin^{-1}x = \dfrac{\pi}{2}$.

**Solution.**

(a) Add the known identity $\sin^{-1}x+\cos^{-1}x = \frac{\pi}{2}$ to the given
equation:

$$ 2\cos^{-1}x = \frac{\pi}{2}+\frac{\pi}{6} = \frac{2\pi}{3}
\;\Rightarrow\; \cos^{-1}x = \frac{\pi}{3} \;\Rightarrow\; x = \cos\frac{\pi}{3} = \frac12 $$

(b) Write $\sin^{-1}x = \theta$, so $x=\sin\theta$ and the equation becomes
$\sin^{-1}(1-x) = \frac{\pi}{2}+2\theta$. Taking sine of both sides,

$$ 1-x = \sin\left(\frac{\pi}{2}+2\theta\right) = \cos 2\theta = 1-2\sin^{2}\theta = 1-2x^{2} $$

so $2x^{2} = x$, i.e. $x(2x-1) = 0$, giving $x=0$ or $x=\frac12$.

**Check.** $x=0$: LHS $=\sin^{-1}1-0 = \frac{\pi}{2}$ — valid.
$x=\frac12$: LHS $=\sin^{-1}\frac12-2\sin^{-1}\frac12 = -\frac{\pi}{6}\ne\frac{\pi}{2}$ — reject.
Hence $x=0$.
:::

::: tip Always verify the root
Taking $\sin$ or $\tan$ of both sides can create extra roots, because those
functions are many-to-one. Substituting each root back into the *original*
equation is part of the solution, and examiners award a mark for it.
:::

## Chapter summary

- Inverse circular functions exist only after the domain is restricted to a
  one-to-one principal branch; the graph of the inverse is the reflection of that
  branch in $y=x$.
- Ranges: $\sin^{-1}, \csc^{-1} \in\left[-\frac{\pi}{2},\frac{\pi}{2}\right]$;
  $\tan^{-1}\in\left(-\frac{\pi}{2},\frac{\pi}{2}\right)$;
  $\cos^{-1}, \sec^{-1}\in[0,\pi]$; $\cot^{-1}\in(0,\pi)$.
- $\sin^{-1}x+\cos^{-1}x = \tan^{-1}x+\cot^{-1}x = \sec^{-1}x+\csc^{-1}x = \frac{\pi}{2}$.
- $\sin^{-1}(-x)=-\sin^{-1}x$ and $\tan^{-1}(-x)=-\tan^{-1}x$, but
  $\cos^{-1}(-x)=\pi-\cos^{-1}x$ and $\cot^{-1}(-x)=\pi-\cot^{-1}x$.
- $\tan^{-1}x+\tan^{-1}y = \tan^{-1}\frac{x+y}{1-xy}$ if $xy<1$; add $\pi$ if
  $x,y>0$ with $xy>1$ and subtract $\pi$ if $x,y<0$ with $xy>1$.
- $\sin^{-1}x+\sin^{-1}y = \sin^{-1}\left(x\sqrt{1-y^2}+y\sqrt{1-x^2}\right)$ and
  $\cos^{-1}x+\cos^{-1}y = \cos^{-1}\left(xy-\sqrt{1-x^2}\sqrt{1-y^2}\right)$.
- $2\tan^{-1}x = \tan^{-1}\frac{2x}{1-x^2} = \sin^{-1}\frac{2x}{1+x^2} = \cos^{-1}\frac{1-x^2}{1+x^2}$.
- $\sin^{-1}(\sin x)=x$ only for $x\in\left[-\frac{\pi}{2},\frac{\pi}{2}\right]$;
  otherwise shift the angle into the range first.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The range of $\cos^{-1}x$ is <span class="marks">[1]</span>
   (a) $\left[-\frac{\pi}{2},\frac{\pi}{2}\right]$ (b) $[0,\pi]$ (c) $(0,\pi)$ (d) $\mathbb{R}$
2. The principal value of $\sin^{-1}\left(-\frac{\sqrt{3}}{2}\right)$ is <span class="marks">[1]</span>
   (a) $\frac{4\pi}{3}$ (b) $\frac{2\pi}{3}$ (c) $-\frac{\pi}{3}$ (d) $-\frac{\pi}{6}$
3. The domain of $\sin^{-1}(3x)$ is <span class="marks">[1]</span>
   (a) $[-1,1]$ (b) $\left[-\frac13,\frac13\right]$ (c) $[-3,3]$ (d) $\mathbb{R}$
4. $\tan^{-1}x+\cot^{-1}x$ equals <span class="marks">[1]</span>
   (a) $0$ (b) $\frac{\pi}{4}$ (c) $\frac{\pi}{2}$ (d) $\pi$
5. $\cos^{-1}\left(\cos\frac{5\pi}{3}\right)$ equals <span class="marks">[1]</span>
   (a) $\frac{5\pi}{3}$ (b) $\frac{\pi}{3}$ (c) $-\frac{\pi}{3}$ (d) $\frac{2\pi}{3}$
6. $\tan^{-1}2+\tan^{-1}3$ equals <span class="marks">[1]</span>
   (a) $\frac{\pi}{4}$ (b) $\frac{3\pi}{4}$ (c) $-\frac{\pi}{4}$ (d) $\frac{\pi}{2}$

::: note Answers to Group A
**1.** (b) — the principal branch of $\cos$ is $[0,\pi]$.
**2.** (c) — $\sin^{-1}$ is odd and $\sin\frac{\pi}{3} = \frac{\sqrt{3}}{2}$.
**3.** (b) — need $-1\le 3x\le 1$.
**4.** (c) — complementary identity.
**5.** (b) — $\cos\frac{5\pi}{3} = \cos\left(2\pi-\frac{5\pi}{3}\right)=\cos\frac{\pi}{3}$, and $\frac{\pi}{3}\in[0,\pi]$.
**6.** (b) — $xy=6>1$ with both positive, so the value is $\pi+\tan^{-1}\frac{5}{-5}=\pi-\frac{\pi}{4}=\frac{3\pi}{4}$.
:::

**Group B — Short answer (5 marks each)**

1. Define the inverse sine function and state the domain and range of all six
   inverse circular functions. <span class="marks">[5]</span>
2. Prove that $\sin^{-1}x+\cos^{-1}x = \dfrac{\pi}{2}$ for $|x|\le 1$. <span class="marks">[5]</span>
3. Prove that $\tan^{-1}\dfrac{1}{3}+\tan^{-1}\dfrac{1}{5}+\tan^{-1}\dfrac{1}{7}+\tan^{-1}\dfrac{1}{8} = \dfrac{\pi}{4}$. <span class="marks">[5]</span>
4. Evaluate $\sin\left(\cos^{-1}\dfrac{4}{5}+\tan^{-1}\dfrac{5}{12}\right)$. <span class="marks">[5]</span>
5. Solve $\tan^{-1}(x+1)+\tan^{-1}(x-1) = \tan^{-1}\dfrac{8}{31}$. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** $\sin^{-1}x$ is the unique $y\in\left[-\frac{\pi}{2},\frac{\pi}{2}\right]$
with $\sin y = x$, defined for $-1\le x\le 1$. The full table is the one in §9.1:
$\sin^{-1},\csc^{-1}$ have range $\left[-\frac{\pi}{2},\frac{\pi}{2}\right]$
(excluding $0$ for $\csc^{-1}$), $\tan^{-1}$ has $\left(-\frac{\pi}{2},\frac{\pi}{2}\right)$,
$\cos^{-1},\sec^{-1}$ have $[0,\pi]$ (excluding $\frac{\pi}{2}$ for $\sec^{-1}$),
and $\cot^{-1}$ has $(0,\pi)$. Domains: $[-1,1]$ for $\sin^{-1},\cos^{-1}$;
$|x|\ge 1$ for $\sec^{-1},\csc^{-1}$; $\mathbb{R}$ for $\tan^{-1},\cot^{-1}$.

**2.** Let $\sin^{-1}x=\theta$, so $\sin\theta=x$ and $-\frac{\pi}{2}\le\theta\le\frac{\pi}{2}$.
Then $\cos\left(\frac{\pi}{2}-\theta\right)=\sin\theta=x$. Since
$0\le\frac{\pi}{2}-\theta\le\pi$, the angle $\frac{\pi}{2}-\theta$ lies in the range
of $\cos^{-1}$, so $\cos^{-1}x = \frac{\pi}{2}-\theta = \frac{\pi}{2}-\sin^{-1}x$,
which rearranges to the result.

**3.** Pair them off. First pair ($xy=\frac{1}{15}<1$):
$\tan^{-1}\frac13+\tan^{-1}\frac15 = \tan^{-1}\dfrac{\frac13+\frac15}{1-\frac{1}{15}}
= \tan^{-1}\dfrac{8/15}{14/15} = \tan^{-1}\frac47$.
Second pair ($xy=\frac{1}{56}<1$):
$\tan^{-1}\frac17+\tan^{-1}\frac18 = \tan^{-1}\dfrac{\frac17+\frac18}{1-\frac{1}{56}}
= \tan^{-1}\dfrac{15/56}{55/56} = \tan^{-1}\frac{3}{11}$.
Now combine ($xy = \frac{12}{77}<1$):
$\tan^{-1}\frac47+\tan^{-1}\frac{3}{11} = \tan^{-1}\dfrac{\frac47+\frac{3}{11}}{1-\frac{12}{77}}
= \tan^{-1}\dfrac{65/77}{65/77} = \tan^{-1}1 = \frac{\pi}{4}$.

**4.** Let $A=\cos^{-1}\frac45$, so $\sin A=\frac35$, $\cos A=\frac45$. Let
$B=\tan^{-1}\frac{5}{12}$, so $\sin B=\frac{5}{13}$, $\cos B=\frac{12}{13}$ (from the
$5,12,13$ triangle). Then
$\sin(A+B)=\sin A\cos B+\cos A\sin B = \frac35\cdot\frac{12}{13}+\frac45\cdot\frac{5}{13}
= \dfrac{36+20}{65} = \dfrac{56}{65}$.

**5.** Product $(x+1)(x-1) = x^{2}-1$. Assuming $x^2-1<1$,
$\tan^{-1}\dfrac{(x+1)+(x-1)}{1-(x^{2}-1)} = \tan^{-1}\dfrac{8}{31}$, so
$\dfrac{2x}{2-x^{2}} = \dfrac{8}{31}$. Cross-multiplying:
$62x = 16-8x^{2}$, i.e. $8x^{2}+62x-16=0$, or $4x^{2}+31x-8=0$.
Factorising, $(4x-1)(x+8)=0$, so $x=\frac14$ or $x=-8$.
Check: $x=\frac14$ gives $x^2-1 = -\frac{15}{16}<1$ and a small positive
left-hand side — valid. $x=-8$ makes the left side negative while
$\tan^{-1}\frac{8}{31}>0$ — reject. Hence $x=\dfrac14$.
:::

**Group C — Long answer (8 marks each)**

1. (a) Explain why the sine function must be restricted before it can be
   inverted, and sketch $y=\sin^{-1}x$ stating its domain and range. <span class="marks">[3]</span>
   (b) Prove that $\tan^{-1}x+\tan^{-1}y = \tan^{-1}\dfrac{x+y}{1-xy}$ when
   $xy<1$, and state the modification needed when $xy>1$. <span class="marks">[3]</span>
   (c) Hence prove $\tan^{-1}1+\tan^{-1}2+\tan^{-1}3 = \pi$. <span class="marks">[2]</span>
2. (a) Prove that $2\tan^{-1}x = \sin^{-1}\dfrac{2x}{1+x^{2}}$ for $|x|\le 1$. <span class="marks">[4]</span>
   (b) Solve $\sin^{-1}\dfrac{5}{x}+\sin^{-1}\dfrac{12}{x} = \dfrac{\pi}{2}$. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** (a) $\sin x$ is many-to-one on $\mathbb{R}$ (the line $y=k$ cuts it
infinitely often), so no inverse function exists. On the principal branch
$\left[-\frac{\pi}{2},\frac{\pi}{2}\right]$ the sine is strictly increasing from
$-1$ to $1$, hence one-to-one and onto $[-1,1]$. Reflecting that branch in $y=x$
gives $y=\sin^{-1}x$, with domain $[-1,1]$ and range
$\left[-\frac{\pi}{2},\frac{\pi}{2}\right]$ (Figure 2).

(b) Let $A=\tan^{-1}x$, $B=\tan^{-1}y$. Then $\tan(A+B) = \dfrac{x+y}{1-xy}$. The
sum $A+B$ lies in $\left(-\frac{\pi}{2},\frac{\pi}{2}\right)$ precisely when
$xy<1$, in which case $A+B$ is the principal value and equals
$\tan^{-1}\frac{x+y}{1-xy}$. If $xy>1$ with $x,y>0$ then
$A+B\in\left(\frac{\pi}{2},\pi\right)$, so $A+B = \pi+\tan^{-1}\frac{x+y}{1-xy}$;
with $x,y<0$ the correction is $-\pi$.

(c) $\tan^{-1}2+\tan^{-1}3$: $xy=6>1$ and both positive, so it equals
$\pi+\tan^{-1}\frac{5}{-5} = \pi-\frac{\pi}{4} = \frac{3\pi}{4}$. Adding
$\tan^{-1}1=\frac{\pi}{4}$ gives $\pi$.

**2.** (a) Let $\theta = \tan^{-1}x$, so $\tan\theta = x$ and
$-\frac{\pi}{4}\le\theta\le\frac{\pi}{4}$ when $|x|\le 1$. Then
$\sin 2\theta = \dfrac{2\tan\theta}{1+\tan^{2}\theta} = \dfrac{2x}{1+x^{2}}$.
Because $-\frac{\pi}{2}\le 2\theta\le\frac{\pi}{2}$, the angle $2\theta$ lies in the
range of $\sin^{-1}$, so $2\theta = \sin^{-1}\dfrac{2x}{1+x^{2}}$, i.e.
$2\tan^{-1}x = \sin^{-1}\dfrac{2x}{1+x^{2}}$.

(b) Rewrite as $\sin^{-1}\frac{5}{x} = \frac{\pi}{2}-\sin^{-1}\frac{12}{x}
= \cos^{-1}\frac{12}{x}$. Taking sine,
$\dfrac{5}{x} = \sin\left(\cos^{-1}\frac{12}{x}\right) = \sqrt{1-\dfrac{144}{x^{2}}}
= \dfrac{\sqrt{x^{2}-144}}{|x|}$.
For $x>0$ this gives $5 = \sqrt{x^{2}-144}$, so $x^{2} = 169$ and $x = 13$.
Check: $\sin^{-1}\frac{5}{13}+\sin^{-1}\frac{12}{13}$ — the two angles of a
$5,12,13$ right triangle — add to $\frac{\pi}{2}$. Valid. ($x=-13$ makes both
terms negative, so it is rejected.) Hence $x=13$.
:::
