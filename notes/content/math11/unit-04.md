---
subject: Mathematics
grade: 11
unit: 4
title: Curve Sketching
hours: 5
area: Algebra
---

Sketching a curve is not plotting fifty points and joining them. It is deducing the shape
from the equation: where the curve crosses the axes, whether it is symmetric, where it
rises and falls, and what happens far away or near a forbidden value. Four or five
deductions fix the picture, and the picture then answers questions about roots, ranges
and maxima at a glance. This unit builds the checklist and applies it to the five curves
the syllabus names.

::: key What the exam asks for
Group A takes a mark from parity (odd/even), period or an asymptote. Group B is almost
always "sketch this quadratic / this $\frac{1}{ax+b}$ / this $a\sin bx$, stating its
main features". Marks are awarded for the **stated features** — intercepts, vertex,
asymptotes, amplitude, period — not for the neatness of the curve, so always label them.
:::

## 4.1 Odd and even functions; periodicity

::: definition Even and odd functions
A function $f$ whose domain is symmetric about $0$ is

- **even** if $f(-x) = f(x)$ for every $x$ in the domain;
- **odd** if $f(-x) = -f(x)$ for every $x$ in the domain.

A function may be even, odd, or **neither**. The only function that is both is
$f(x) = 0$.
:::

To test parity, replace $x$ by $-x$ and simplify. If the result is the original
expression, it is even; if it is the original with every sign reversed, it is odd; if it
is neither, the function has no parity.

| Even | Odd | Neither |
|---|---|---|
| $x^{2},\ x^{4},\ x^{6}$ | $x,\ x^{3},\ x^{5}$ | $x^{2}+x$ |
| $\cos x,\ \sec x$ | $\sin x,\ \tan x,\ \csc x,\ \cot x$ | $x + \cos x$ |
| $|x|$ | $x\,|x|$ | $e^{x}$ |
| $\frac{1}{2}(e^{x}+e^{-x})$ | $\frac{1}{2}(e^{x}-e^{-x})$ | $\ln x$ (domain not symmetric) |

::: memory Parity arithmetic
- even $\pm$ even $=$ even; odd $\pm$ odd $=$ odd; even $\pm$ odd $=$ neither (in general)
- even $\times$ even $=$ even; odd $\times$ odd $=$ **even**; even $\times$ odd $=$ odd

A polynomial is even when **all** its powers are even, and odd when all are odd; a mixture
of even and odd powers gives neither. A non-zero constant term counts as an even power
($x^{0}$).
:::

```figure caption="Left: an even function, symmetric about the $y$-axis — reflect and the curve maps to itself. Right: an odd function, symmetric about the origin — rotate by $180^\circ$ and the curve maps to itself."
import numpy as np, matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 2, figsize=(5.2,2.7))
x = np.linspace(-2.1, 2.1, 500)
ax = axes[0]
ax.plot(x, x**4-3*x**2, color=ACCENT, lw=1.9)
for px in (1.5, -1.5):
    ax.plot([px],[px**4-3*px**2],'o',color=SERIES[1],ms=5, zorder=5)
ax.plot([-1.5,1.5],[1.5**4-3*1.5**2]*2, color=SERIES[1], lw=0.9, ls=(0,(3,2)))
ax.annotate('$f(-x)=f(x)$', (0,-1.6), fontsize=8.6, color=SERIES[1], ha='center')
ax.set_title('even:  $y = x^4-3x^2$', fontsize=9.2, pad=3)
ax.set_ylim(-3.2,3.2)
ax = axes[1]
ax.plot(x, x**3-3*x, color=ACCENT, lw=1.9)
for px in (1.0, -1.0):
    ax.plot([px],[px**3-3*px],'o',color=SERIES[1],ms=5, zorder=5)
ax.plot([-1,1],[2,-2], color=SERIES[1], lw=0.9, ls=(0,(3,2)))
ax.annotate('$f(-x)=-f(x)$', (0,-2.7), fontsize=8.6, color=SERIES[1], ha='center')
ax.set_title('odd:  $y = x^3-3x$', fontsize=9.2, pad=3)
ax.set_ylim(-3.4,3.4)
for ax in axes:
    ax.axhline(0, color=MUTED, lw=0.9); ax.axvline(0, color=MUTED, lw=0.9)
    ax.set_xlim(-2.1,2.1); ax.set_xlabel('$x$')
    ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.35)
fig.tight_layout()
```

::: example Worked example 4.1
**Problem.** Determine whether each function is even, odd or neither:
(a) $f(x) = x^{4} - 3x^{2} + 1$, (b) $g(x) = x^{3} - x$, (c) $h(x) = x^{2} + x$.

**Solution.**

**(a)** $f(-x) = (-x)^{4} - 3(-x)^{2} + 1 = x^{4} - 3x^{2} + 1 = f(x)$. **Even** — all
powers present ($4, 2, 0$) are even.

**(b)** $g(-x) = (-x)^{3} - (-x) = -x^{3} + x = -(x^{3}-x) = -g(x)$. **Odd** — all powers
($3, 1$) are odd.

**(c)** $h(-x) = (-x)^{2} + (-x) = x^{2} - x$. This is neither $h(x) = x^2+x$ nor
$-h(x) = -x^2-x$, so $h$ is **neither**. (It mixes an even power with an odd one.)
:::

::: example Worked example 4.2
**Problem.** Show that $f(x) = \dfrac{e^{x} + e^{-x}}{2}$ is even and
$g(x) = x\,|x|$ is odd.

**Solution.**

$$ f(-x) = \frac{e^{-x} + e^{-(-x)}}{2} = \frac{e^{-x} + e^{x}}{2} = f(x) $$

so $f$ is even. (This function is $\cosh x$, and its graph is the shape of a hanging
cable.)

For $g$, use $|-x| = |x|$:

$$ g(-x) = (-x)\,|-x| = -x\,|x| = -g(x) $$

so $g$ is odd.
:::

### Periodicity

::: definition Periodic function
A function $f$ is **periodic** if there is a positive number $T$ with

$$ f(x + T) = f(x) \quad \text{for every } x \text{ in the domain} $$

The smallest such $T$ is the **fundamental period** (usually just "the period"). The graph
of a periodic function repeats the same block of width $T$ forever.
:::

::: key Periods you must know
| Function | Period |
|---|---|
| $\sin x$, $\cos x$, $\csc x$, $\sec x$ | $2\pi$ |
| $\tan x$, $\cot x$ | $\pi$ |
| $a\sin bx$, $a\cos bx$ | $\dfrac{2\pi}{|b|}$ |
| $a\tan bx$ | $\dfrac{\pi}{|b|}$ |
| $\sin^{2}x$, $\cos^{2}x$ | $\pi$ |

The amplitude $a$ never changes the period; only the coefficient $b$ of $x$ does. A larger
$|b|$ squeezes the graph horizontally, giving a shorter period.
:::

```figure caption="$y = \sin x$ has period $2\pi$: the block between $0$ and $2\pi$ repeats forever. $y = \sin 2x$ repeats twice as fast, with period $\pi$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,2.7))
x = np.linspace(-2*np.pi, 3*np.pi, 900)
ax.plot(x, np.sin(x), color=ACCENT, lw=1.9, label='$y = \\sin x$')
ax.plot(x, np.sin(2*x), color=SERIES[1], lw=1.4, ls='--', label='$y = \\sin 2x$')
ax.axvspan(0, 2*np.pi, color=ACCENT, alpha=0.08)
ax.annotate('', xy=(2*np.pi,1.42), xytext=(0,1.42),
            arrowprops=dict(arrowstyle='<|-|>', color=ACCENT, lw=1.2, mutation_scale=10))
ax.text(np.pi, 1.52, 'one period $= 2\\pi$', fontsize=8.6, color=ACCENT, ha='center')
ax.annotate('', xy=(np.pi,-1.42), xytext=(0,-1.42),
            arrowprops=dict(arrowstyle='<|-|>', color=SERIES[1], lw=1.2, mutation_scale=10))
ax.text(np.pi/2, -1.80, 'period $= \\pi$', fontsize=8.6, color=SERIES[1], ha='center')
ax.set_xticks([-2*np.pi,-np.pi,0,np.pi,2*np.pi,3*np.pi])
ax.set_xticklabels(['$-2\\pi$','$-\\pi$','0','$\\pi$','$2\\pi$','$3\\pi$'])
ax.axhline(0, color=MUTED, lw=0.8)
ax.set_xlim(-2*np.pi,3*np.pi); ax.set_ylim(-2.2,2.9)
ax.set_xlabel('$x$'); ax.set_ylabel('$y$')
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.35)
ax.legend(loc='upper left', fontsize=8.0, ncol=1)
```

::: example Worked example 4.3
**Problem.** Find the period of (a) $\sin 3x$, (b) $\cos\frac{x}{2}$, (c) $\tan 4x$,
(d) $2 + 3\sin(\pi x)$.

**Solution.** Use period $= \frac{2\pi}{|b|}$ for sine and cosine, $\frac{\pi}{|b|}$ for
tangent.

**(a)** $b = 3$, so period $= \frac{2\pi}{3}$.

**(b)** $b = \frac{1}{2}$, so period $= \frac{2\pi}{1/2} = 4\pi$.

**(c)** Tangent: period $= \frac{\pi}{4}$.

**(d)** Adding $2$ shifts the graph up and multiplying by $3$ stretches it vertically;
neither affects the period. With $b = \pi$, period $= \frac{2\pi}{\pi} = 2$.
:::

## 4.2 Symmetry about origin, X-axis and Y-axis; monotonicity

Parity is a statement about *functions*. Symmetry is the same idea applied to any
*equation* in $x$ and $y$, including curves such as $y^{2} = 4x$ that are not functions.

::: key The three symmetry tests
Take the equation of the curve and substitute:

| Replace | Equation unchanged means | Example |
|---|---|---|
| $x$ by $-x$ | symmetric about the **$Y$-axis** | $y = x^{4} - 2x^{2}$ |
| $y$ by $-y$ | symmetric about the **$X$-axis** | $y^{2} = 4x$ |
| $x$ by $-x$ **and** $y$ by $-y$ | symmetric about the **origin** | $y = x^{3}$, $xy = 6$ |

If a curve has any two of these symmetries it automatically has the third. A curve
symmetric about the $X$-axis (other than a piece of the $x$-axis itself) is never the
graph of a function, since a vertical line meets it twice.
:::

```figure caption="Left: $y^2 = 4x$ is symmetric about the $X$-axis and fails the vertical line test. Right: $x^2+y^2=9$ has all three symmetries."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle
fig, axes = plt.subplots(1, 2, figsize=(5.0,2.6))
ax = axes[0]
y = np.linspace(-4.2, 4.2, 400)
ax.plot(y**2/4, y, color=ACCENT, lw=1.9)
ax.axvline(2.0, color=SERIES[1], lw=1.0, ls=(0,(4,3)))
for py in (np.sqrt(8), -np.sqrt(8)):
    ax.plot([2.0],[py],'o',color=SERIES[1],ms=4.5, zorder=5)
ax.text(2.55, 0.35, 'one $x$,\ntwo $y$', fontsize=8.0, color=SERIES[1])
ax.set_title('$y^2 = 4x$  ($X$-axis only)', fontsize=9.0, pad=3)
ax.set_xlim(-1.0,5.0); ax.set_ylim(-4.4,4.4)
ax = axes[1]
ax.add_patch(Circle((0,0), 3, fill=False, ec=ACCENT, lw=1.9))
ax.plot([-3.9,3.9],[0,0], color=SERIES[1], lw=0.9, ls=(0,(4,3)))
ax.plot([0,0],[-3.9,3.9], color=SERIES[1], lw=0.9, ls=(0,(4,3)))
for px,py in [(2.12,2.12),(-2.12,2.12),(2.12,-2.12),(-2.12,-2.12)]:
    ax.plot([px],[py],'o',color=SERIES[2],ms=4, zorder=5)
ax.set_title('$x^2+y^2=9$  (all three)', fontsize=9.0, pad=3)
ax.set_xlim(-4.2,4.2); ax.set_ylim(-4.2,4.2); ax.set_aspect('equal')
for ax in axes:
    ax.axhline(0, color=MUTED, lw=0.8); ax.axvline(0, color=MUTED, lw=0.8)
    ax.set_xlabel('$x$'); ax.spines[['top','right']].set_visible(False)
    ax.grid(True, alpha=.3)
fig.tight_layout()
```

::: example Worked example 4.4
**Problem.** Discuss the symmetry of (a) $y = x^{4} - 2x^{2}$, (b) $y^{2} = 8x$,
(c) $xy = 6$, (d) $x^{2} + y^{2} = 25$.

**Solution.**

**(a)** Replace $x$ by $-x$: $(-x)^4 - 2(-x)^2 = x^4 - 2x^2$, unchanged. Symmetric about
the **$Y$-axis** only. (Replacing $y$ by $-y$ gives $-y = x^4-2x^2$, a different curve.)

**(b)** Replace $y$ by $-y$: $(-y)^{2} = y^{2}$, unchanged. Symmetric about the
**$X$-axis** only — replacing $x$ by $-x$ gives $y^2 = -8x$, a different parabola.

**(c)** Replace $x$ by $-x$ and $y$ by $-y$: $(-x)(-y) = xy = 6$, unchanged. Symmetric
about the **origin** only.

**(d)** All three substitutions leave $x^2+y^2 = 25$ unchanged, so the circle is
symmetric about both axes **and** the origin — as expected.
:::

### Monotonicity

::: definition Increasing and decreasing
Let $f$ be defined on an interval $I$ and let $x_1, x_2 \in I$.

- $f$ is **strictly increasing** on $I$ if $x_1 < x_2 \Rightarrow f(x_1) < f(x_2)$.
- $f$ is **strictly decreasing** on $I$ if $x_1 < x_2 \Rightarrow f(x_1) > f(x_2)$.

A function that is one or the other throughout $I$ is called **monotonic** on $I$.
Monotonicity is always stated **on an interval**, never at a single point.
:::

The standard method is to take $x_1 < x_2$ and examine the sign of $f(x_2) - f(x_1)$. In
Unit 18 you will meet the quicker test: $f'(x) > 0$ on $I$ makes $f$ increasing there, and
$f'(x) < 0$ makes it decreasing.

```figure caption="Monotonic intervals. Left: $y=x^2$ decreases on $(-\infty,0]$ and increases on $[0,\infty)$. Right: $y=1/x$ decreases on each branch separately, but is not decreasing on its whole domain."
import numpy as np, matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 2, figsize=(5.0,2.7))
ax = axes[0]
xl = np.linspace(-2.6, 0, 300); xr = np.linspace(0, 2.6, 300)
ax.plot(xl, xl**2, color=SERIES[1], lw=2.0, label='decreasing')
ax.plot(xr, xr**2, color=ACCENT, lw=2.0, label='increasing')
ax.plot([0],[0],'o',color=INK,ms=4.5, zorder=5)
ax.set_title('$y = x^{2}$', fontsize=9.2, pad=3)
ax.set_xlim(-2.6,2.6); ax.set_ylim(-0.9,9.6)
ax.legend(loc='upper center', fontsize=7.8, ncol=2)
ax = axes[1]
for seg in (np.linspace(-3.0,-0.30,300), np.linspace(0.30,3.0,300)):
    ax.plot(seg, 1/seg, color=SERIES[1], lw=2.0)
ax.plot([-3.2,3.2],[0,0], color=MUTED, lw=0.9, ls=(0,(4,3)))
ax.plot([0,0],[-3.6,3.6], color=MUTED, lw=0.9, ls=(0,(4,3)))
ax.plot([-1,1],[-1,1],'o',color=INK,ms=4.5, zorder=6)
ax.annotate('$f(-1) = -1 < f(1) = 1$', (-1.55,2.35), fontsize=7.8, color=INK, ha='center')
ax.set_title('$y = 1/x$', fontsize=9.2, pad=3)
ax.set_xlim(-3.2,3.2); ax.set_ylim(-3.6,3.6)
for ax in axes:
    ax.axhline(0, color=MUTED, lw=0.8); ax.axvline(0, color=MUTED, lw=0.8)
    ax.set_xlabel('$x$'); ax.spines[['top','right']].set_visible(False)
    ax.grid(True, alpha=.35)
fig.tight_layout()
```

::: example Worked example 4.5
**Problem.** Show that $f(x) = 3x + 2$ is strictly increasing on $\mathbb{R}$, and that
$g(x) = -2x + 7$ is strictly decreasing on $\mathbb{R}$.

**Solution.** Let $x_1 < x_2$.

$$ f(x_2) - f(x_1) = (3x_2+2) - (3x_1+2) = 3(x_2 - x_1) $$

Since $x_2 - x_1 > 0$, this is positive, so $f(x_2) > f(x_1)$. Hence $f$ is strictly
increasing.

$$ g(x_2) - g(x_1) = (-2x_2+7) - (-2x_1+7) = -2(x_2-x_1) $$

Since $x_2 - x_1 > 0$, this is negative, so $g(x_2) < g(x_1)$ and $g$ is strictly
decreasing. In general $y = mx+c$ increases when $m > 0$ and decreases when $m < 0$.
:::

::: example Worked example 4.6
**Problem.** Show that $f(x) = x^{2}$ is decreasing on $(-\infty, 0]$ and increasing on
$[0, \infty)$.

**Solution.** For any $x_1 < x_2$,

$$ f(x_2) - f(x_1) = x_2^{2} - x_1^{2} = (x_2 - x_1)(x_2 + x_1) $$

The first factor $x_2 - x_1$ is positive. The sign therefore follows the sign of
$x_1 + x_2$.

- If $x_1 < x_2 \le 0$ then $x_1 + x_2 < 0$, so $f(x_2) < f(x_1)$: **decreasing**.
- If $0 \le x_1 < x_2$ then $x_1 + x_2 > 0$, so $f(x_2) > f(x_1)$: **increasing**.

So $x = 0$ is the turning point, which matches the vertex of the parabola.
:::

::: caution "Decreasing on each branch" is not "decreasing everywhere"
$f(x) = \frac{1}{x}$ is strictly decreasing on $(-\infty,0)$ and strictly decreasing on
$(0,\infty)$, but it is **not** decreasing on $\mathbb{R}-\{0\}$: taking $x_1 = -1$ and
$x_2 = 1$ gives $f(x_1) = -1 < 1 = f(x_2)$. Monotonicity may only be claimed on an
interval, and $\mathbb{R}-\{0\}$ is not one.
:::

## 4.3 Graphs of quadratic, cubic, rational function of form $1/(ax+b)$

::: memory The sketching checklist
1. **Domain** — which $x$ are allowed?
2. **Intercepts** — put $y = 0$ for $x$-intercepts, $x = 0$ for the $y$-intercept.
3. **Symmetry** — apply the three tests.
4. **Asymptotes** — vertical where a denominator vanishes; horizontal from the behaviour
   as $x \rightarrow \pm\infty$.
5. **Turning points / monotonic intervals**.
6. **End behaviour** — what happens as $x \rightarrow \pm\infty$.

Then plot the special points found and join them smoothly.
:::

### Quadratic

$y = ax^{2}+bx+c$ is a parabola with vertex at $x = -\frac{b}{2a}$ and axis of symmetry
$x = -\frac{b}{2a}$; it opens upward if $a > 0$ and downward if $a < 0$.

```figure caption="$y = 2x^2-8x+5$. Vertex $(2,-3)$, axis $x=2$ (dashed), $y$-intercept $5$, roots $2 \pm \frac{\sqrt{6}}{2} \approx 0.78$ and $3.22$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6,3.0))
x = np.linspace(-0.6, 4.6, 500)
ax.plot(x, 2*x**2-8*x+5, color=ACCENT, lw=2.0)
ax.axvline(2, color=SERIES[1], lw=1.0, ls=(0,(4,3)))
ax.plot([2],[-3],'o',color=SERIES[1],ms=6, zorder=6)
ax.annotate('vertex $(2,-3)$', (2,-3), textcoords='offset points', xytext=(8,-4),
            fontsize=8.4, color=SERIES[1])
ax.plot([0],[5],'o',color=SERIES[2],ms=5, zorder=6)
ax.annotate('$(0,5)$', (0,5), textcoords='offset points', xytext=(6,2),
            fontsize=8.4, color=SERIES[2])
r = np.sqrt(6)/2
for rx in (2-r, 2+r):
    ax.plot([rx],[0],'o',color=INK,ms=4.5, zorder=6)
ax.annotate('$2-\\frac{\\sqrt{6}}{2}$', (2-r,0), textcoords='offset points',
            xytext=(-38,6), fontsize=8.2, color=INK)
ax.annotate('$2+\\frac{\\sqrt{6}}{2}$', (2+r,0), textcoords='offset points',
            xytext=(4,6), fontsize=8.2, color=INK)
ax.text(2.06, 4.6, 'axis $x=2$', fontsize=8.2, color=SERIES[1])
ax.axhline(0, color=MUTED, lw=0.8); ax.axvline(0, color=MUTED, lw=0.8)
ax.set_xlabel('$x$'); ax.set_ylabel('$y$')
ax.set_xlim(-0.6,4.6); ax.set_ylim(-4.5,7.5)
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.4)
```

::: example Worked example 4.7
**Problem.** Sketch $y = 2x^{2} - 8x + 5$, stating the vertex, axis of symmetry,
intercepts, range and monotonic intervals.

**Solution.**

**Step 1 — shape.** $a = 2 > 0$, so the parabola opens upward.

**Step 2 — vertex.** $x = -\frac{b}{2a} = \frac{8}{4} = 2$, and

$$ y = 2(2)^{2} - 8(2) + 5 = 8 - 16 + 5 = -3 $$

Vertex $(2,-3)$; axis of symmetry $x = 2$.

**Step 3 — $y$-intercept.** $x = 0$ gives $y = 5$.

**Step 4 — $x$-intercepts.** Solve $2x^2-8x+5 = 0$ with the quadratic formula:

$$ x = \frac{8 \pm \sqrt{64 - 40}}{4} = \frac{8 \pm \sqrt{24}}{4} = 2 \pm \frac{\sqrt{6}}{2} $$

Numerically $x \approx 0.78$ and $x \approx 3.22$ (the discriminant $24 > 0$, so there are
two distinct roots).

**Step 5 — range and monotonicity.** The minimum value is $-3$, so the range is
$[-3, \infty)$. The curve decreases on $(-\infty, 2]$ and increases on $[2, \infty)$.
:::

### Cubic

A cubic $y = ax^{3}+bx^{2}+cx+d$ with $a > 0$ runs from $-\infty$ to $+\infty$; it has
either two turning points or none, and always at least one real root.

```figure caption="$y = x^3-3x^2+2x = x(x-1)(x-2)$: roots at $0, 1, 2$, local maximum near $(0.42,\ 0.38)$ and local minimum near $(1.58,\ -0.38)$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6,2.9))
x = np.linspace(-0.55, 2.55, 600)
ax.plot(x, x**3-3*x**2+2*x, color=ACCENT, lw=2.0)
for rx in (0,1,2):
    ax.plot([rx],[0],'o',color=SERIES[2],ms=5, zorder=6)
tp = [1-1/np.sqrt(3), 1+1/np.sqrt(3)]
for px, lab, off in [(tp[0],'local max',(-12,10)), (tp[1],'local min',(2,-16))]:
    py = px**3-3*px**2+2*px
    ax.plot([px],[py],'o',color=SERIES[1],ms=5.5, zorder=6)
    ax.annotate(lab, (px,py), textcoords='offset points', xytext=off,
                fontsize=8.4, color=SERIES[1])
ax.text(0.02,-0.30,'$0$',fontsize=8.4,color=SERIES[2])
ax.text(1.0,-0.42,'$1$',fontsize=8.4,color=SERIES[2],ha='center')
ax.text(2.0,-0.42,'$2$',fontsize=8.4,color=SERIES[2],ha='center')
ax.axhline(0, color=MUTED, lw=0.8); ax.axvline(0, color=MUTED, lw=0.8)
ax.set_xlabel('$x$'); ax.set_ylabel('$y$')
ax.set_xlim(-0.55,2.55); ax.set_ylim(-1.5,1.5)
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.4)
```

::: example Worked example 4.8
**Problem.** Sketch $y = x^{3} - 3x^{2} + 2x$, stating intercepts, symmetry, sign and end
behaviour.

**Solution.**

**Factorise.** $y = x(x^{2}-3x+2) = x(x-1)(x-2)$, so the $x$-intercepts are
$x = 0, 1, 2$. Putting $x = 0$ gives $y = 0$, so the curve passes through the origin.

**Symmetry.** $f(-x) = -x^3 - 3x^2 - 2x$, which equals neither $f(x)$ nor $-f(x)$, so
there is **no** symmetry about the axes or the origin.

**Sign.** Test one point in each interval cut off by the roots:

| Interval | test $x$ | $y$ | sign |
|---|---|---|---|
| $x < 0$ | $-1$ | $(-1)(-2)(-3) = -6$ | negative |
| $0 < x < 1$ | $0.5$ | $(0.5)(-0.5)(-1.5) = 0.375$ | positive |
| $1 < x < 2$ | $1.5$ | $(1.5)(0.5)(-0.5) = -0.375$ | negative |
| $x > 2$ | $3$ | $(3)(2)(1) = 6$ | positive |

**End behaviour.** As $x \rightarrow \infty$, $y \rightarrow \infty$; as
$x \rightarrow -\infty$, $y \rightarrow -\infty$.

So the curve rises from the bottom left, crosses at $0$, peaks, dips through $1$, bottoms
out, and rises through $2$ to the top right. The turning points are at
$x = 1 \pm \frac{1}{\sqrt{3}}$, i.e. $x \approx 0.42$ and $1.58$, where
$y \approx \pm 0.38$.
:::

### The rational function $y = \dfrac{1}{ax+b}$

::: key Features of $y = \dfrac{1}{ax+b}$  $(a \ne 0)$
- **Domain:** $\mathbb{R} - \left\{-\frac{b}{a}\right\}$.
- **Vertical asymptote:** $x = -\dfrac{b}{a}$, where the denominator vanishes. As $x$
  approaches it, $|y| \rightarrow \infty$.
- **Horizontal asymptote:** $y = 0$, since $\frac{1}{ax+b} \rightarrow 0$ as
  $x \rightarrow \pm\infty$.
- **No $x$-intercept** — a fraction with numerator $1$ is never zero. The $y$-intercept is
  $\frac{1}{b}$ (provided $b \ne 0$).
- **Two branches**, one on each side of the vertical asymptote. Each branch is strictly
  decreasing if $a > 0$ and strictly increasing if $a < 0$.
- **Range:** $\mathbb{R} - \{0\}$.
:::

```figure caption="$y = \dfrac{1}{2x-4}$. The dashed lines $x=2$ and $y=0$ are the asymptotes; the curve never touches them. The only intercept is $(0,-0.25)$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6,3.0))
left = np.linspace(-3.0, 1.90, 400); right = np.linspace(2.10, 7.0, 400)
for seg in (left, right):
    ax.plot(seg, 1/(2*seg-4), color=ACCENT, lw=2.0)
ax.axvline(2, color=SERIES[1], lw=1.2, ls=(0,(5,3)))
ax.axhline(0, color=SERIES[2], lw=1.2, ls=(0,(5,3)))
ax.text(2.35, -1.75, 'vertical\nasymptote $x = 2$', fontsize=8.2, color=SERIES[1])
ax.text(4.25, 0.55, 'horizontal\nasymptote $y = 0$', fontsize=8.2, color=SERIES[2])
ax.plot([0],[-0.25],'o',color=INK,ms=5, zorder=6)
ax.annotate('$(0,-0.25)$', (0,-0.25), textcoords='offset points', xytext=(-14,-16),
            fontsize=8.4, color=INK)
ax.axvline(0, color=MUTED, lw=0.8)
ax.set_xlabel('$x$'); ax.set_ylabel('$y$')
ax.set_xlim(-3.0,7.0); ax.set_ylim(-3.2,3.2)
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.4)
```

::: example Worked example 4.9
**Problem.** Sketch $y = \dfrac{1}{2x-4}$, giving the domain, asymptotes, intercepts,
range and monotonicity.

**Solution.**

**Domain.** $2x - 4 \ne 0$, so $x \ne 2$: domain $= \mathbb{R} - \{2\}$.

**Vertical asymptote.** $x = 2$. Approaching from the right ($x = 2.1$) gives
$y = \frac{1}{0.2} = 5$, large and positive; from the left ($x = 1.9$) gives
$y = \frac{1}{-0.2} = -5$, large and negative.

**Horizontal asymptote.** As $x \rightarrow \pm\infty$ the denominator grows without
bound, so $y \rightarrow 0$. The line $y = 0$ is a horizontal asymptote.

**Intercepts.** Setting $y = 0$ gives $1 = 0$, impossible — there is no $x$-intercept.
Setting $x = 0$ gives $y = \frac{1}{-4} = -0.25$.

**Range.** $y$ takes every value except $0$: range $= \mathbb{R} - \{0\}$.

**Monotonicity.** Writing $y = (2x-4)^{-1}$, an increase in $x$ increases $2x-4$; on each
branch the reciprocal then decreases. So the curve is strictly decreasing on
$(-\infty, 2)$ and strictly decreasing on $(2, \infty)$ — but not on the whole domain.
:::

::: caution A graph may cross a horizontal asymptote, never a vertical one
A vertical asymptote sits at an $x$ **excluded from the domain**, so the curve cannot
reach it. A horizontal asymptote only describes behaviour far away; some curves do cross
theirs closer in. For $y = \frac{1}{ax+b}$ neither is crossed.
:::

## 4.4 Graphs of $a\sin bx$, $a\cos bx$, $e^{x}$, $\ln x$

::: key $y = a\sin bx$ and $y = a\cos bx$
- **Amplitude** $= |a|$; the curve oscillates between $-|a|$ and $+|a|$, so the range is
  $[-|a|,\ |a|]$.
- **Period** $= \dfrac{2\pi}{|b|}$; the graph completes $|b|$ full waves in the interval
  of length $2\pi$.
- $a\sin bx$ starts at $0$ when $x = 0$ and its zeros are at $x = \frac{n\pi}{b}$.
- $a\cos bx$ starts at its **maximum** $a$ when $x = 0$ (for $a>0$), and its zeros are at
  $x = \frac{(2n+1)\pi}{2b}$.
- A negative $a$ turns the whole graph upside down.
:::

```figure caption="Left: $y = \sin x$ and $y = 3\sin 2x$ — tripled amplitude, halved period. Right: $y = 2\cos 3x$, amplitude 2 and period $2\pi/3$, starting at its maximum."
import numpy as np, matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 2, figsize=(5.2,2.7))
ax = axes[0]
x = np.linspace(0, 2*np.pi, 800)
ax.plot(x, np.sin(x), color=MUTED, lw=1.3, ls='--', label='$y=\\sin x$')
ax.plot(x, 3*np.sin(2*x), color=ACCENT, lw=1.9, label='$y=3\\sin 2x$')
ax.annotate('', xy=(np.pi/4,3), xytext=(np.pi/4,0),
            arrowprops=dict(arrowstyle='<|-|>', color=SERIES[1], lw=1.1, mutation_scale=9))
ax.text(np.pi/4+0.12, 1.5, 'amplitude 3', fontsize=8.0, color=SERIES[1])
ax.annotate('', xy=(np.pi,-3.5), xytext=(0,-3.5),
            arrowprops=dict(arrowstyle='<|-|>', color=SERIES[2], lw=1.1, mutation_scale=9))
ax.text(np.pi/2, -4.4, 'period $\\pi$', fontsize=8.0, color=SERIES[2], ha='center')
ax.set_xticks([0,np.pi/2,np.pi,3*np.pi/2,2*np.pi])
ax.set_xticklabels(['0','$\\pi/2$','$\\pi$','$3\\pi/2$','$2\\pi$'])
ax.set_ylim(-5.0,4.4); ax.set_xlim(0,2*np.pi)
ax.legend(loc='upper right', fontsize=7.6)
ax = axes[1]
ax.plot(x, 2*np.cos(3*x), color=SERIES[2], lw=1.9, label='$y=2\\cos 3x$')
ax.annotate('', xy=(2*np.pi/3,-2.6), xytext=(0,-2.6),
            arrowprops=dict(arrowstyle='<|-|>', color=SERIES[1], lw=1.1, mutation_scale=9))
ax.text(np.pi/3, -3.3, 'period $2\\pi/3$', fontsize=8.0, color=SERIES[1], ha='center')
ax.plot([0],[2],'o',color=SERIES[1],ms=4.5, zorder=6)
ax.set_xticks([0,2*np.pi/3,4*np.pi/3,2*np.pi])
ax.set_xticklabels(['0','$2\\pi/3$','$4\\pi/3$','$2\\pi$'])
ax.set_ylim(-3.8,3.2); ax.set_xlim(0,2*np.pi)
ax.legend(loc='upper right', fontsize=7.6)
for ax in axes:
    ax.axhline(0, color=MUTED, lw=0.8)
    ax.set_xlabel('$x$'); ax.spines[['top','right']].set_visible(False)
    ax.grid(True, alpha=.35)
fig.tight_layout()
```

::: example Worked example 4.10
**Problem.** Sketch $y = 3\sin 2x$ for $0 \le x \le 2\pi$, giving amplitude, period,
range, zeros and the coordinates of the maxima and minima.

**Solution.**

**Amplitude** $= |3| = 3$; **period** $= \frac{2\pi}{2} = \pi$; **range** $= [-3, 3]$.

**Zeros.** $3\sin 2x = 0$ when $2x = 0, \pi, 2\pi, 3\pi, 4\pi$, i.e.

$$ x = 0,\ \frac{\pi}{2},\ \pi,\ \frac{3\pi}{2},\ 2\pi $$

**Maxima.** $\sin 2x = 1$ when $2x = \frac{\pi}{2}, \frac{5\pi}{2}$, so
$x = \frac{\pi}{4}, \frac{5\pi}{4}$, giving the points
$\left(\frac{\pi}{4}, 3\right)$ and $\left(\frac{5\pi}{4}, 3\right)$.

**Minima.** $\sin 2x = -1$ when $2x = \frac{3\pi}{2}, \frac{7\pi}{2}$, so
$x = \frac{3\pi}{4}, \frac{7\pi}{4}$, giving
$\left(\frac{3\pi}{4}, -3\right)$ and $\left(\frac{7\pi}{4}, -3\right)$.

Two complete waves fit into $[0, 2\pi]$, as the period $\pi$ demands.
:::

::: example Worked example 4.11
**Problem.** Sketch $y = 2\cos 3x$ for $0 \le x \le 2\pi$, giving amplitude, period and
the first maximum and minimum.

**Solution.** Amplitude $= 2$, period $= \frac{2\pi}{3}$, range $= [-2, 2]$.

A cosine starts at its maximum: at $x = 0$, $y = 2\cos 0 = 2$.

The first minimum is where $3x = \pi$, i.e. $x = \frac{\pi}{3}$, giving $y = -2$.

Zeros occur where $3x = \frac{\pi}{2}, \frac{3\pi}{2}, \dots$, i.e.
$x = \frac{\pi}{6}, \frac{\pi}{2}, \frac{5\pi}{6}, \dots$

Since $2\pi \div \frac{2\pi}{3} = 3$, exactly **three** complete waves fit into
$[0, 2\pi]$.
:::

::: key $y = e^{x}$ and $y = \ln x$
| | $y = e^{x}$ | $y = \ln x$ |
|---|---|---|
| Domain | $\mathbb{R}$ | $(0, \infty)$ |
| Range | $(0, \infty)$ | $\mathbb{R}$ |
| Passes through | $(0,1)$ | $(1,0)$ |
| Asymptote | horizontal $y = 0$ (as $x \rightarrow -\infty$) | vertical $x = 0$ (as $x \rightarrow 0^{+}$) |
| Monotonicity | strictly increasing | strictly increasing |
| Symmetry | none | none |

$y = e^{-x}$ is the mirror image of $y = e^{x}$ in the $Y$-axis: it is strictly
decreasing, still passes through $(0,1)$, and still has $y = 0$ as an asymptote.
:::

```figure caption="$y = e^{x}$ (growth), $y = e^{-x}$ (decay) and $y = \ln x$. Dashed lines are the asymptotes $y=0$ and $x=0$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,2.9))
x = np.linspace(-3.0, 2.2, 400)
ax.plot(x, np.exp(x), color=ACCENT, lw=1.9, label='$y = e^{x}$')
ax.plot(x, np.exp(-x), color=SERIES[1], lw=1.7, ls='--', label='$y = e^{-x}$')
t = np.linspace(0.05, 5.0, 500)
ax.plot(t, np.log(t), color=SERIES[2], lw=1.9, label='$y = \\ln x$')
ax.axhline(0, color=MUTED, lw=1.1, ls=(0,(5,3)))
ax.axvline(0, color=MUTED, lw=1.1, ls=(0,(5,3)))
ax.plot([0],[1],'o',color=INK,ms=4.5, zorder=6)
ax.annotate('$(0,1)$', (0,1), textcoords='offset points', xytext=(-32,2),
            fontsize=8.2, color=INK)
ax.plot([1],[0],'o',color=SERIES[2],ms=4.5, zorder=6)
ax.annotate('$(1,0)$', (1,0), textcoords='offset points', xytext=(4,-13),
            fontsize=8.2, color=SERIES[2])
ax.set_xlabel('$x$'); ax.set_ylabel('$y$')
ax.set_xlim(-3.0,5.0); ax.set_ylim(-2.6,5.2)
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.4)
ax.legend(loc='upper right', fontsize=8.0)
```

::: example Worked example 4.12
**Problem.** Sketch $y = e^{x}$ and $y = \ln x$ on the same axes and state, for each, the
domain, range, intercept and asymptote. Hence say how many solutions $e^{x} = \ln x$ has.

**Solution.**

| | $e^{x}$ | $\ln x$ |
|---|---|---|
| Domain | $\mathbb{R}$ | $(0,\infty)$ |
| Range | $(0,\infty)$ | $\mathbb{R}$ |
| Intercept | $(0,1)$ on the $y$-axis | $(1,0)$ on the $x$-axis |
| Asymptote | $y = 0$ | $x = 0$ |

Both are increasing, and each is the reflection of the other in $y = x$.

For $x > 0$, $e^{x} > 1$ while $\ln x < x$; in fact $e^{x}$ lies entirely **above** the
line $y = x$ and $\ln x$ lies entirely **below** it. So the two curves never meet, and
$e^{x} = \ln x$ has **no** solution.
:::

## Chapter summary

- $f$ is even if $f(-x) = f(x)$ (graph symmetric about the $Y$-axis) and odd if
  $f(-x) = -f(x)$ (symmetric about the origin). odd $\times$ odd $=$ even.
- $f$ is periodic with period $T$ if $f(x+T) = f(x)$; $a\sin bx$ and $a\cos bx$ have
  period $\frac{2\pi}{|b|}$, and $a\tan bx$ has period $\frac{\pi}{|b|}$.
- Symmetry tests: $x \rightarrow -x$ unchanged gives $Y$-axis symmetry;
  $y \rightarrow -y$ gives $X$-axis symmetry; both together give origin symmetry.
- $f$ is increasing on $I$ if $x_1 < x_2 \Rightarrow f(x_1) < f(x_2)$; prove it from the
  sign of $f(x_2)-f(x_1)$. Monotonicity is claimed on an interval, never pointwise.
- Quadratic: vertex at $x = -\frac{b}{2a}$, opens up if $a>0$; number of $x$-intercepts
  from the discriminant $b^2-4ac$.
- $y = \frac{1}{ax+b}$: vertical asymptote $x = -\frac{b}{a}$, horizontal asymptote
  $y = 0$, $y$-intercept $\frac{1}{b}$, no $x$-intercept, two decreasing branches when
  $a>0$, range $\mathbb{R}-\{0\}$.
- $y = a\sin bx$: amplitude $|a|$, period $\frac{2\pi}{|b|}$, range $[-|a|,|a|]$;
  $a\cos bx$ is the same curve starting at its maximum.
- $e^{x}$: domain $\mathbb{R}$, range $(0,\infty)$, through $(0,1)$, asymptote $y=0$.
  $\ln x$: domain $(0,\infty)$, range $\mathbb{R}$, through $(1,0)$, asymptote $x=0$.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The function $f(x) = x^{3} + x$ is <span class="marks">[1]</span>
   (a) even (b) odd (c) neither (d) periodic
2. The period of $y = 5\cos 4x$ is <span class="marks">[1]</span>
   (a) $\frac{\pi}{2}$ (b) $\frac{\pi}{4}$ (c) $2\pi$ (d) $8\pi$
3. The curve $y^{2} = 4x$ is symmetric about <span class="marks">[1]</span>
   (a) the $Y$-axis (b) the $X$-axis (c) the origin only (d) both axes
4. The vertical asymptote of $y = \dfrac{1}{3x-6}$ is <span class="marks">[1]</span>
   (a) $x = 6$ (b) $x = -2$ (c) $x = 2$ (d) $y = 0$
5. The amplitude of $y = -4\sin 3x$ is <span class="marks">[1]</span>
   (a) $-4$ (b) $4$ (c) $3$ (d) $12$
6. The range of $y = e^{x}$ is <span class="marks">[1]</span>
   (a) $\mathbb{R}$ (b) $[0, \infty)$ (c) $(0, \infty)$ (d) $(-\infty, 0)$
7. The function $y = x^{2}$ is decreasing on <span class="marks">[1]</span>
   (a) $\mathbb{R}$ (b) $[0,\infty)$ (c) $(-\infty,0]$ (d) nowhere

::: note Answers to Group A
**1.** (b) — both powers, $3$ and $1$, are odd, so $f(-x) = -x^3-x = -f(x)$.

**2.** (a) — period $= \frac{2\pi}{|b|} = \frac{2\pi}{4} = \frac{\pi}{2}$; the amplitude $5$ is irrelevant.

**3.** (b) — replacing $y$ by $-y$ leaves $y^2 = 4x$ unchanged; replacing $x$ by $-x$ does not.

**4.** (c) — the denominator vanishes when $3x-6 = 0$, i.e. $x = 2$.

**5.** (b) — amplitude is $|a| = |-4| = 4$; the minus sign only flips the graph.

**6.** (c) — $e^{x}$ is always strictly positive and takes every positive value; $0$ itself is never attained.

**7.** (c) — to the left of the vertex the parabola falls; to the right it rises.
:::

**Group B — Short answer (5 marks each)**

1. Define even and odd functions. Test whether each of $f(x) = x^{4} - 3x^{2} + 2$,
   $g(x) = x^{3} + x$ and $h(x) = x^{3} + x^{2}$ is even, odd or neither. <span class="marks">[5]</span>
2. Find the period of (a) $\sin 4x$, (b) $\cos\frac{2x}{3}$, (c) $\tan 3x$,
   (d) $2\sin\frac{x}{3}$. <span class="marks">[5]</span>
3. Discuss the symmetry of (i) $y^{2} = 8x$, (ii) $x^{2}+y^{2} = 16$, (iii) $y = x^{5}-x$. <span class="marks">[5]</span>
4. Show from the definition that $f(x) = 5x - 3$ is strictly increasing on $\mathbb{R}$
   and that $g(x) = 4 - 3x$ is strictly decreasing on $\mathbb{R}$. <span class="marks">[5]</span>
5. Sketch $y = -2x^{2} + 4x + 6$, stating the vertex, axis of symmetry, intercepts and
   range. <span class="marks">[5]</span>
6. Sketch $y = \dfrac{1}{x+1}$, stating the domain, asymptotes, intercepts, range and
   monotonicity. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** $f$ is **even** if $f(-x) = f(x)$ for all $x$ in a domain symmetric about $0$, and
**odd** if $f(-x) = -f(x)$.

$f(-x) = x^{4} - 3x^{2} + 2 = f(x)$ — **even** (all powers $4, 2, 0$ are even).

$g(-x) = -x^{3} - x = -(x^3+x) = -g(x)$ — **odd** (all powers odd).

$h(-x) = -x^{3} + x^{2}$, which is neither $h(x) = x^3+x^2$ nor $-h(x) = -x^3-x^2$ —
**neither** (it mixes an odd and an even power).

**2.** (a) $\frac{2\pi}{4} = \frac{\pi}{2}$.

(b) $b = \frac{2}{3}$, so period $= \frac{2\pi}{2/3} = 3\pi$.

(c) Tangent: $\frac{\pi}{3}$.

(d) $b = \frac{1}{3}$, so period $= \frac{2\pi}{1/3} = 6\pi$ (the amplitude $2$ is
irrelevant).

**3.** (i) Replacing $y$ by $-y$: $(-y)^2 = 8x$ is the same equation, so the curve is
symmetric about the **$X$-axis**. Replacing $x$ by $-x$ gives $y^2 = -8x$, a different
curve, so there is no $Y$-axis symmetry (and hence none about the origin).

(ii) All three substitutions leave $x^2+y^2 = 16$ unchanged, so the circle is symmetric
about **both axes and the origin**.

(iii) $y = x^5 - x$. Replacing $x$ by $-x$ and $y$ by $-y$: $-y = -x^5 + x$, i.e.
$y = x^5 - x$, unchanged. Symmetric about the **origin** only (it is an odd function).

**4.** Let $x_1 < x_2$, so $x_2 - x_1 > 0$.

$$ f(x_2) - f(x_1) = (5x_2-3)-(5x_1-3) = 5(x_2-x_1) > 0 $$

so $f(x_1) < f(x_2)$ and $f$ is strictly increasing.

$$ g(x_2) - g(x_1) = (4-3x_2)-(4-3x_1) = -3(x_2-x_1) < 0 $$

so $g(x_1) > g(x_2)$ and $g$ is strictly decreasing.

**5.** $a = -2 < 0$, so the parabola opens **downward**.

Vertex: $x = -\frac{b}{2a} = -\frac{4}{-4} = 1$, and $y = -2(1)+4(1)+6 = 8$. Vertex
$(1, 8)$; axis of symmetry $x = 1$.

$x$-intercepts: $-2x^2+4x+6 = 0 \Rightarrow x^2-2x-3 = 0 \Rightarrow (x-3)(x+1) = 0$, so
$x = -1$ and $x = 3$. $y$-intercept: $x = 0$ gives $y = 6$.

Maximum value $8$, so the range is $(-\infty, 8]$. The curve increases on $(-\infty,1]$
and decreases on $[1,\infty)$.

**6.** Here $a = 1$, $b = 1$, so:

Domain $= \mathbb{R} - \{-1\}$. Vertical asymptote $x = -1$; horizontal asymptote
$y = 0$.

$y$-intercept: $x = 0$ gives $y = 1$. There is no $x$-intercept, since $\frac{1}{x+1}$ is
never zero.

Range $= \mathbb{R} - \{0\}$.

Since $a = 1 > 0$, the curve is strictly decreasing on $(-\infty,-1)$ and strictly
decreasing on $(-1,\infty)$ — two separate branches, the left one below the $x$-axis and
the right one above it.
:::

**Group C — Long answer (8 marks each)**

1. (a) Define even, odd and periodic functions, and prove that the product of two odd
   functions is even. <span class="marks">[3]</span>
   (b) Sketch $y = 3\cos 2x$ for $0 \le x \le 2\pi$, stating the amplitude, period, range
   and the coordinates of all maxima, minima and zeros in that interval. <span class="marks">[5]</span>
2. (a) Sketch $y = x^{3} - 3x^{2} + 2x$, showing the intercepts, the sign in each
   interval and the behaviour as $x \rightarrow \pm\infty$. <span class="marks">[4]</span>
   (b) Sketch $y = \dfrac{1}{2x-6}$, showing the asymptotes, the intercept and the
   monotonic intervals. <span class="marks">[4]</span>

::: note Answers to Group C
**1. (a)** $f$ is **even** if $f(-x) = f(x)$, **odd** if $f(-x) = -f(x)$, and
**periodic** with period $T > 0$ if $f(x+T) = f(x)$ for every $x$ in the domain, $T$ being
the smallest such number.

*Proof.* Let $f$ and $g$ both be odd and put $h(x) = f(x)\,g(x)$. Then

$$ h(-x) = f(-x)\,g(-x) = \left(-f(x)\right)\left(-g(x)\right) = f(x)\,g(x) = h(x) $$

so $h$ is even. (Example: $x \cdot x^{3} = x^{4}$, indeed even.)

**1. (b)** For $y = 3\cos 2x$: amplitude $= 3$, period $= \frac{2\pi}{2} = \pi$,
range $= [-3, 3]$.

**Maxima** ($\cos 2x = 1$): $2x = 0, 2\pi, 4\pi$, so $x = 0, \pi, 2\pi$, giving
$(0,3)$, $(\pi,3)$ and $(2\pi,3)$.

**Minima** ($\cos 2x = -1$): $2x = \pi, 3\pi$, so $x = \frac{\pi}{2}, \frac{3\pi}{2}$,
giving $\left(\frac{\pi}{2},-3\right)$ and $\left(\frac{3\pi}{2},-3\right)$.

**Zeros** ($\cos 2x = 0$): $2x = \frac{\pi}{2}, \frac{3\pi}{2}, \frac{5\pi}{2}, \frac{7\pi}{2}$,
so

$$ x = \frac{\pi}{4},\ \frac{3\pi}{4},\ \frac{5\pi}{4},\ \frac{7\pi}{4} $$

The sketch shows two complete cosine waves in $[0, 2\pi]$, starting and ending at the
maximum height $3$.

**2. (a)** $y = x(x-1)(x-2)$, so the $x$-intercepts are $0, 1, 2$ and the $y$-intercept is
$0$.

Sign: negative for $x<0$, positive for $0<x<1$, negative for $1<x<2$, positive for $x>2$
(test $x = -1, 0.5, 1.5, 3$ giving $-6, 0.375, -0.375, 6$).

As $x \rightarrow \infty$, $y \rightarrow \infty$; as $x \rightarrow -\infty$,
$y \rightarrow -\infty$. There is no symmetry. The turning points are at
$x = 1 \pm \frac{1}{\sqrt{3}}$ with $y \approx \pm 0.38$ — a local maximum near
$(0.42, 0.38)$ and a local minimum near $(1.58, -0.38)$.

**2. (b)** $y = \frac{1}{2x-6}$. The denominator vanishes at $2x - 6 = 0$, i.e. $x = 3$,
so:

- Domain $\mathbb{R}-\{3\}$; vertical asymptote $x = 3$.
- As $x \rightarrow \pm\infty$, $y \rightarrow 0$: horizontal asymptote $y = 0$.
- $y$-intercept: $x = 0$ gives $y = \frac{1}{-6} = -\frac{1}{6}$. No $x$-intercept.
- Range $\mathbb{R}-\{0\}$.
- Since $a = 2 > 0$, the curve is strictly decreasing on $(-\infty,3)$ and strictly
  decreasing on $(3,\infty)$.

The left branch lies below the $x$-axis, rising from just below $0$ and plunging to
$-\infty$ as $x \rightarrow 3^{-}$; the right branch comes down from $+\infty$ at
$x \rightarrow 3^{+}$ and approaches $0$ from above.
:::
