---
subject: Mathematics
grade: 11
unit: 20
title: Computational Methods
hours: 12
area: Computational Methods OR Mechanics
---

Most equations you meet outside the textbook cannot be solved by a formula, and most
integrals cannot be evaluated by anti-differentiation. Computational methods give up
on exact answers and instead build a sequence of numbers that closes in on the true
value, stopping when the answer is accurate enough for the job. This unit is the
first place in your course where "accurate enough" is made precise. Note that the
CDC syllabus offers **Mechanics (Unit 21) as the alternative** to this unit for the
same 12 hours; you study one of the two, and Mechanics is covered in the next
chapter.

::: key What the examiner asks for
Four things, and they repeat almost unchanged every year: bisect an interval to find
a root to a stated number of decimal places, run Newton-Raphson for three or four
iterations from a given starting value, apply the trapezoidal rule with a given
number of sub-intervals, and apply Simpson's rule to the same kind of integral.
**Set the work out as a table.** Marks are awarded for the ordinate table and for
the substitution into the formula, not only for the final number. Keep at least six
decimal places in the working and round only at the very end.
:::

## 20.1 Roots of algebraic and transcendental equations: bisection method

An **algebraic equation** is one built from powers of $x$, such as $x^{3}-x-1=0$. A
**transcendental equation** involves trigonometric, exponential or logarithmic
functions, such as $\cos x = x$ or $xe^{x} = 1$. A number $\alpha$ with
$f(\alpha)=0$ is a **root** of $f(x)=0$. Beyond the quadratic (and the rarely used
cubic) formula there is no algebraic recipe for the roots, so we locate them
numerically.

### Locating a root

Every method starts by trapping the root inside an interval.

::: key Location (intermediate value) theorem
If $f$ is continuous on $[a,b]$ and $f(a)$ and $f(b)$ have **opposite signs** —
that is, $f(a)\cdot f(b) < 0$ — then $f(x)=0$ has at least one root between $a$
and $b$.
:::

To find such an interval, tabulate $f$ at convenient integers and look for a change
of sign. For $f(x) = x^{3}-x-1$:

| $x$ | 0 | 1 | 2 |
|---|---|---|---|
| $f(x)$ | $-1$ | $-1$ | $+5$ |

The sign changes between $x=1$ and $x=2$, so a root lies in $[1,2]$.

```figure caption="Bracketing a root. Since $f(1) = -1$ and $f(2) = +5$ have opposite signs, the continuous curve $y = x^3-x-1$ must cross the axis somewhere in $[1,2]$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.4,2.8))
f = lambda t: t**3 - t - 1
x = np.linspace(0.75, 2.1, 300)
ax.plot(x, f(x), color=ACCENT, lw=2, zorder=4)
ax.axhline(0, color=MUTED, lw=1.0)
ax.plot([1],[f(1)],'o',color='#d9534f',ms=5,zorder=6)
ax.plot([2],[f(2)],'o',color='#2e8b57',ms=5,zorder=6)
ax.annotate('$f(1)=-1$',(1,f(1)),xytext=(0.79,-0.42),color='#a8271f',fontsize=9,
            ha='left',
            arrowprops=dict(arrowstyle='-', color='#a8271f', lw=0.8))
ax.annotate('$f(2)=+5$',(2,f(2)),textcoords='offset points',xytext=(-58,4),
            color='#1b5e3a',fontsize=9)
r = 1.3247179572
ax.plot([r],[0],'o',color=INK,ms=4.5,zorder=6)
ax.annotate(r'$\alpha \approx 1.3247$',(r,0),xytext=(1.44,0.62),color=INK,fontsize=9,
            ha='left',
            arrowprops=dict(arrowstyle='-|>',color=INK,lw=0.9,mutation_scale=9))
ax.plot([1,2],[-1.55,-1.55],color=INK,lw=1.4)
for p in (1,2):
    ax.plot([p,p],[-1.68,-1.42],color=INK,lw=1.4)
ax.annotate('sign change over this interval',(1.5,-1.95),color=INK,fontsize=8.4,ha='center')
ax.set_xlim(0.72,2.15); ax.set_ylim(-2.35,5.4)
ax.set_xlabel('$x$'); ax.set_ylabel('$f(x) = x^3-x-1$')
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.35)
```

### The method

::: definition Bisection method
Given $[a,b]$ with $f(a)\,f(b)<0$, repeat:

1. Compute the midpoint $c = \frac{a+b}{2}$ and the value $f(c)$.
2. If $f(c) = 0$, then $c$ is the root — stop.
3. If $f(a)\,f(c) < 0$, the root lies in $[a,c]$: replace $b$ by $c$.
   Otherwise the root lies in $[c,b]$: replace $a$ by $c$.

Each pass halves the interval containing the root.
:::

Because the root always stays inside the current interval, the midpoint after $n$
steps differs from the true root by at most half the current interval width:

$$ |x_{n} - \alpha| \le \frac{b-a}{2^{n}} $$

This is the great virtue of bisection — it **cannot fail**, and it tells you in
advance how many steps you need. To guarantee an error below $\varepsilon$, solve

$$ \frac{b-a}{2^{n}} < \varepsilon \;\Longrightarrow\; n > \frac{\ln\frac{b-a}{\varepsilon}}{\ln 2} $$

```figure caption="Bisection in action on $x^3-x-1=0$. Each bar is the interval still known to contain the root; its midpoint becomes the next approximation, and the bar halves every time."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,3.1))
f = lambda t: t**3 - t - 1
x = np.linspace(0.95, 2.05, 300)
ax.plot(x, f(x), color=ACCENT, lw=1.8, zorder=4)
ax.axhline(0, color=MUTED, lw=1.0)
a, b = 1.0, 2.0
levels = [-0.7, -1.1, -1.5, -1.9]
for k, yy in enumerate(levels):
    c = (a+b)/2
    ax.plot([a,b],[yy,yy], color=SERIES[k], lw=2.2)
    for p in (a,b):
        ax.plot([p,p],[yy-0.09,yy+0.09], color=SERIES[k], lw=2.2)
    ax.plot([c],[yy],'o',color=SERIES[k],ms=4.5)
    ax.plot([c,c],[yy,0.0], color=SERIES[k], lw=0.8, ls=':')
    ax.annotate(f'$x_{k+1}={c:.4f}$',(b,yy),textcoords='offset points',
                xytext=(6,-3),color=SERIES[k],fontsize=8.2)
    if f(a)*f(c) < 0: b = c
    else: a = c
r = 1.3247179572
ax.plot([r],[0],'*',color=INK,ms=9,zorder=7)
ax.annotate(r'$\alpha = 1.3247$',(r,0),textcoords='offset points',xytext=(-18,14),
            color=INK,fontsize=8.6)
ax.set_xlim(0.92,2.35); ax.set_ylim(-2.25,5.3)
ax.set_xlabel('$x$'); ax.set_ylabel('$f(x)$')
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.3)
```

::: example Worked example 20.1
**Problem.** Find a root of $x^{3}-x-1=0$ correct to three decimal places by the
bisection method.

**Solution.** Let $f(x) = x^{3}-x-1$. Since $f(1) = -1 < 0$ and $f(2) = 5 > 0$, a
root lies in $[1,2]$. To be sure of three decimal places we need the error below
$0.0005$; since $\frac{1}{2^{n}} < 0.0005$ needs $n > \frac{\ln 2000}{\ln 2} = 10.97$,
eleven iterations will certainly do. Tabulating:

| $n$ | $a$ | $b$ | $c=\frac{a+b}{2}$ | $f(c)$ | sign | error bound |
|---|---|---|---|---|---|---|
| 1 | 1.000000 | 2.000000 | 1.500000 | $+0.875000$ | + | 0.500000 |
| 2 | 1.000000 | 1.500000 | 1.250000 | $-0.296875$ | $-$ | 0.250000 |
| 3 | 1.250000 | 1.500000 | 1.375000 | $+0.224609$ | + | 0.125000 |
| 4 | 1.250000 | 1.375000 | 1.312500 | $-0.051514$ | $-$ | 0.062500 |
| 5 | 1.312500 | 1.375000 | 1.343750 | $+0.082611$ | + | 0.031250 |
| 6 | 1.312500 | 1.343750 | 1.328125 | $+0.014576$ | + | 0.015625 |
| 7 | 1.312500 | 1.328125 | 1.320313 | $-0.018711$ | $-$ | 0.007813 |
| 8 | 1.320313 | 1.328125 | 1.324219 | $-0.002128$ | $-$ | 0.003906 |
| 9 | 1.324219 | 1.328125 | 1.326172 | $+0.006209$ | + | 0.001953 |
| 10 | 1.324219 | 1.326172 | 1.325195 | $+0.002037$ | + | 0.000977 |
| 11 | 1.324219 | 1.325195 | 1.324707 | $-0.000047$ | $-$ | 0.000488 |

The last error bound is $0.000488 < 0.0005$, so the root is

$$ \alpha \approx 1.325 \quad \text{(to 3 decimal places)} $$

The true root is $1.3247180$, so the actual error is about $0.00001$ — better than
the guarantee, as usually happens.
:::

::: example Worked example 20.2
**Problem.** Find the root of $x^{3}-2x-5=0$ lying between $2$ and $3$, correct to
two decimal places.

**Solution.** $f(2) = 8-4-5 = -1 < 0$ and $f(3) = 27-6-5 = 16 > 0$, so the root is
in $[2,3]$. For two decimal places we need the error below $0.005$, and
$\frac{1}{2^{n}} < 0.005$ needs $n > 7.6$, so eight iterations suffice.

| $n$ | $a$ | $b$ | $c$ | $f(c)$ | error bound |
|---|---|---|---|---|---|
| 1 | 2.000000 | 3.000000 | 2.500000 | $+5.625000$ | 0.500000 |
| 2 | 2.000000 | 2.500000 | 2.250000 | $+1.890625$ | 0.250000 |
| 3 | 2.000000 | 2.250000 | 2.125000 | $+0.345703$ | 0.125000 |
| 4 | 2.000000 | 2.125000 | 2.062500 | $-0.351318$ | 0.062500 |
| 5 | 2.062500 | 2.125000 | 2.093750 | $-0.008942$ | 0.031250 |
| 6 | 2.093750 | 2.125000 | 2.109375 | $+0.166836$ | 0.015625 |
| 7 | 2.093750 | 2.109375 | 2.101563 | $+0.078562$ | 0.007813 |
| 8 | 2.093750 | 2.101563 | 2.097656 | $+0.034714$ | 0.003906 |

Hence $\alpha \approx 2.10$ to two decimal places. (The true root is $2.0945515$;
continuing to eleven iterations would give $2.095$ to three places.)
:::

::: example Worked example 20.3 — a transcendental equation
**Problem.** Solve $\cos x = x$ (with $x$ in radians) correct to two decimal
places, by bisection.

**Solution.** Write it as $f(x) = \cos x - x = 0$. Then $f(0) = 1 > 0$ and
$f(1) = \cos 1 - 1 = 0.5403 - 1 = -0.4597 < 0$, so a root lies in $[0,1]$.

| $n$ | $a$ | $b$ | $c$ | $f(c) = \cos c - c$ | error bound |
|---|---|---|---|---|---|
| 1 | 0.000000 | 1.000000 | 0.500000 | $+0.377583$ | 0.500000 |
| 2 | 0.500000 | 1.000000 | 0.750000 | $-0.018311$ | 0.250000 |
| 3 | 0.500000 | 0.750000 | 0.625000 | $+0.185963$ | 0.125000 |
| 4 | 0.625000 | 0.750000 | 0.687500 | $+0.085335$ | 0.062500 |
| 5 | 0.687500 | 0.750000 | 0.718750 | $+0.033879$ | 0.031250 |
| 6 | 0.718750 | 0.750000 | 0.734375 | $+0.007875$ | 0.015625 |
| 7 | 0.734375 | 0.750000 | 0.742188 | $-0.005196$ | 0.007813 |
| 8 | 0.734375 | 0.742188 | 0.738281 | $+0.001345$ | 0.003906 |

So $\alpha \approx 0.74$ to two decimal places (the true value is $0.7390851$).
:::

::: caution Radians, not degrees
In every calculus and numerical-methods question the trigonometric functions take
**radians**. If your calculator is in degree mode, $\cos 0.5$ reads as $0.99996$
instead of $0.87758$ and every row of the table is wrong. Check the mode before you
begin, and sanity-check with $\cos 1 = 0.5403$.
:::

## 20.2 Roots by Newton-Raphson method

Bisection is safe but slow: each step buys only one bit of accuracy. Newton-Raphson
uses the gradient as well as the value of $f$, and converges dramatically faster.

::: derivation The Newton-Raphson formula
Let $x_{n}$ be an approximation to the root and let $h$ be the correction needed, so
that $f(x_{n}+h) = 0$. Expanding by Taylor's theorem and keeping only the first two
terms (valid when $h$ is small),

$$ f(x_{n}+h) \approx f(x_{n}) + h\,f'(x_{n}) = 0 $$

$$ \Longrightarrow \quad h \approx -\frac{f(x_{n})}{f'(x_{n})} $$

so the improved approximation $x_{n+1} = x_{n}+h$ is

$$ x_{n+1} = x_{n} - \frac{f(x_{n})}{f'(x_{n})}, \qquad n = 0,1,2,\ldots $$
:::

Geometrically, $x_{n+1}$ is the point where the **tangent** to $y=f(x)$ at
$(x_{n}, f(x_{n}))$ meets the $x$-axis. Replacing the curve by its tangent is a good
approximation near the root, so each new point lands much closer than the last.

```figure caption="Newton-Raphson on $f(x)=x^3-x-1$ starting from $x_0 = 1.9$. Each dashed tangent meets the axis at the next approximation, and the points close in rapidly on the root."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,3.0))
f  = lambda t: t**3 - t - 1
df = lambda t: 3*t**2 - 1
x = np.linspace(1.15, 2.05, 300)
ax.plot(x, f(x), color=ACCENT, lw=2, zorder=5)
ax.axhline(0, color=MUTED, lw=1.0)
xs = 1.9
for k in range(3):
    xn = xs - f(xs)/df(xs)
    tt = np.array([min(xs,xn)-0.06, max(xs,xn)+0.06])
    ax.plot(tt, f(xs)+df(xs)*(tt-xs), color=SERIES[k+1], lw=1.1, ls=(0,(4,2)))
    ax.plot([xs],[f(xs)],'o',color=SERIES[k+1],ms=4.5,zorder=6)
    ax.plot([xs,xs],[0,f(xs)],color=SERIES[k+1],lw=0.7,ls=':')
    ax.annotate(f'$x_{k}$',(xs,0),textcoords='offset points',
                xytext=(-3,-14 if k<2 else 8),color=SERIES[k+1],fontsize=9)
    xs = xn
ax.plot([xs],[0],'*',color=INK,ms=9,zorder=7)
ax.annotate('$x_3$',(xs,0),textcoords='offset points',xytext=(-20,13),color=INK,fontsize=9)
ax.annotate('tangent at $(x_0,f(x_0))$\ncuts the axis at $x_1$',(1.20,4.45),
            color=MUTED,fontsize=8.3)
ax.set_xlim(1.12,2.08); ax.set_ylim(-1.3,6.0)
ax.set_xlabel('$x$'); ax.set_ylabel('$f(x)$')
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.3)
```

::: example Worked example 20.4
**Problem.** Use the Newton-Raphson method to find a root of $x^{3}-x-1=0$
correct to five decimal places, taking $x_{0} = 1.5$.

**Solution.** Here $f(x) = x^{3}-x-1$ and $f'(x) = 3x^{2}-1$, so the iteration is

$$ x_{n+1} = x_{n} - \frac{x_{n}^{3}-x_{n}-1}{3x_{n}^{2}-1} $$

| $n$ | $x_{n}$ | $f(x_{n})$ | $f'(x_{n})$ | $x_{n+1}$ |
|---|---|---|---|---|
| 0 | 1.50000000 | $+0.87500000$ | 5.75000000 | 1.34782609 |
| 1 | 1.34782609 | $+0.10068217$ | 4.44990548 | 1.32520040 |
| 2 | 1.32520040 | $+0.00205836$ | 4.26846829 | 1.32471817 |
| 3 | 1.32471817 | $+0.00000092$ | 4.26463472 | 1.32471796 |

Two successive values agree to five decimal places, so

$$ \alpha \approx 1.32472 $$

Compare with Worked example 20.1: bisection needed eleven steps for three decimal
places; Newton-Raphson has produced eight correct places in four.
:::

::: tip Simplify the iteration formula before you compute
Algebra first saves arithmetic. For $f(x) = x^{3}-x-1$,
$$ x_{n+1} = x_n - \frac{x_n^3-x_n-1}{3x_n^2-1} = \frac{3x_n^3-x_n-x_n^3+x_n+1}{3x_n^2-1}
 = \frac{2x_{n}^{3}+1}{3x_{n}^{2}-1} $$
which is one keystroke sequence per row instead of three.
:::

### Newton-Raphson for roots and reciprocals

Setting $f(x) = x^{2}-N$ gives $x_{n+1} = \frac{1}{2}\left(x_{n}+\frac{N}{x_{n}}\right)$,
the classical square-root algorithm; $f(x) = x^{3}-N$ gives
$x_{n+1} = \frac{1}{3}\left(2x_{n}+\frac{N}{x_{n}^{2}}\right)$. These are how
calculators actually compute roots.

::: example Worked example 20.5
**Problem.** Compute $\sqrt{13}$ correct to six decimal places, taking
$x_{0}=3.5$.

**Solution.** Let $f(x) = x^{2}-13$, so $f'(x) = 2x$ and

$$ x_{n+1} = x_{n} - \frac{x_{n}^{2}-13}{2x_{n}} = \frac{1}{2}\left(x_{n}+\frac{13}{x_{n}}\right) $$

| $n$ | $x_{n}$ | $f(x_{n}) = x_n^2-13$ | $x_{n+1}$ |
|---|---|---|---|
| 0 | 3.50000000 | $-0.75000000$ | 3.60714286 |
| 1 | 3.60714286 | $+0.01147959$ | 3.60555163 |
| 2 | 3.60555163 | $+0.00000253$ | 3.60555128 |

Hence $\sqrt{13} \approx 3.605551$ to six decimal places.
:::

::: example Worked example 20.6
**Problem.** Find $\sqrt[3]{30}$ correct to five decimal places, taking
$x_{0} = 3$.

**Solution.** Let $f(x) = x^{3}-30$, $f'(x) = 3x^{2}$:

$$ x_{n+1} = x_{n} - \frac{x_{n}^{3}-30}{3x_{n}^{2}} = \frac{2x_{n}^{3}+30}{3x_{n}^{2}} $$

| $n$ | $x_{n}$ | $f(x_{n})$ | $f'(x_{n})$ | $x_{n+1}$ |
|---|---|---|---|---|
| 0 | 3.00000000 | $-3.00000000$ | 27.00000000 | 3.11111111 |
| 1 | 3.11111111 | $+0.11248285$ | 29.03703704 | 3.10723734 |
| 2 | 3.10723734 | $+0.00014000$ | 28.96477165 | 3.10723251 |

So $\sqrt[3]{30} \approx 3.10723$. Check: $3.10723^{3} = 29.99999$.
:::

::: example Worked example 20.7 — a transcendental equation
**Problem.** Find the root of $\cos x = x$ correct to six decimal places by the
Newton-Raphson method, taking $x_{0} = \frac{\pi}{4} = 0.7854$ radians.

**Solution.** With $f(x) = \cos x - x$ we get $f'(x) = -\sin x - 1$, so

$$ x_{n+1} = x_{n} - \frac{\cos x_{n} - x_{n}}{-\sin x_{n} - 1}
 = x_{n} + \frac{\cos x_{n}-x_{n}}{\sin x_{n}+1} $$

| $n$ | $x_{n}$ | $f(x_{n})$ | $f'(x_{n})$ | $x_{n+1}$ |
|---|---|---|---|---|
| 0 | 0.78540000 | $-0.07829452$ | $-1.70710808$ | 0.73953617 |
| 1 | 0.73953617 | $-0.00075493$ | $-1.67394531$ | 0.73908518 |
| 2 | 0.73908518 | $-0.00000008$ | $-1.67361206$ | 0.73908513 |

Hence $\alpha \approx 0.739085$. Bisection in Worked example 20.3 needed eight
iterations to reach two decimal places; here three iterations give eight.
:::

::: example Worked example 20.8
**Problem.** Solve $x\log_{10}x = 1.2$ correct to four decimal places, taking
$x_{0} = 2.5$.

**Solution.** Let $f(x) = x\log_{10}x - 1.2$. Since
$\log_{10}x = \frac{\ln x}{\ln 10}$, the product rule gives

$$ f'(x) = \log_{10}x + \frac{1}{\ln 10} = \log_{10}x + 0.4342945 $$

| $n$ | $x_{n}$ | $f(x_{n})$ | $f'(x_{n})$ | $x_{n+1}$ |
|---|---|---|---|---|
| 0 | 2.50000000 | $-0.20514998$ | 0.83223449 | 2.74650502 |
| 1 | 2.74650502 | $+0.00511256$ | 0.87307488 | 2.74064921 |
| 2 | 2.74064921 | $+0.00000271$ | 0.87214793 | 2.74064610 |

Hence $x \approx 2.7406$ to four decimal places.
:::

### How fast, and when it fails

Newton-Raphson converges **quadratically**: near a simple root the error is roughly
squared at each step, so the number of correct decimal places doubles every
iteration. That is why three or four rows are normally enough, and why you should
carry eight decimals in the working.

```figure caption="Error $|x_n - \alpha|$ against iteration number for $x^3-x-1=0$ on a logarithmic scale. Bisection gains a fixed amount per step; Newton-Raphson accelerates."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.4,2.7))
f  = lambda t: t**3 - t - 1
df = lambda t: 3*t**2 - 1
r = 1.3247179572447458
a, b = 1.0, 2.0; be = []
for k in range(14):
    c = (a+b)/2; be.append(abs(c-r))
    if f(a)*f(c) < 0: b = c
    else: a = c
x = 1.5; ne = []
for k in range(6):
    ne.append(max(abs(x-r), 1e-17)); x = x - f(x)/df(x)
ax.semilogy(range(1,15), be, 'o-', color=ACCENT, lw=1.5, ms=4, label='bisection')
ax.semilogy(range(1,7), ne, 's-', color='#d9534f', lw=1.5, ms=4, label='Newton-Raphson')
ax.axhline(1e-6, color=MUTED, lw=0.9, ls=':')
ax.annotate('6-decimal accuracy',(9.0,1.6e-6),color=MUTED,fontsize=8)
ax.set_xlabel('iteration $n$'); ax.set_ylabel('error $|x_n - \\alpha|$')
ax.set_ylim(1e-16, 1); ax.legend(fontsize=8.2)
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.35, which='major')
```

The price of the speed is that Newton-Raphson can fail. It breaks down if
$f'(x_{n}) = 0$ (the tangent is horizontal and never meets the axis), it can be
thrown far away if the starting value is poor, and it can fall into a cycle.

```figure caption="Failure of Newton-Raphson on $f(x)=x^3-2x+2$ with $x_0 = 0$. The tangents send the iteration to $x_1 = 1$ and straight back to $x_2 = 0$, so it cycles for ever."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.4,2.8))
f  = lambda t: t**3 - 2*t + 2
df = lambda t: 3*t**2 - 2
x = np.linspace(-2.3, 1.7, 300)
ax.plot(x, f(x), color=ACCENT, lw=2, zorder=5)
ax.axhline(0, color=MUTED, lw=1.0)
for x0, col in [(0.0, '#d9534f'), (1.0, '#b8860b')]:
    x1 = x0 - f(x0)/df(x0)
    tt = np.array([min(x0,x1)-0.35, max(x0,x1)+0.35])
    ax.plot(tt, f(x0)+df(x0)*(tt-x0), color=col, lw=1.1, ls=(0,(4,2)))
    ax.plot([x0],[f(x0)],'o',color=col,ms=4.5,zorder=6)
ax.annotate('$x_0=0$',(0,0),textcoords='offset points',xytext=(-6,-15),color='#a8271f',fontsize=9)
ax.annotate('$x_1=1$',(1,0),textcoords='offset points',xytext=(8,6),color='#8a6508',fontsize=9)
ax.annotate('', xy=(1,0.35), xytext=(0,0.35),
            arrowprops=dict(arrowstyle='<|-|>', color='#d9534f', lw=1.2, mutation_scale=10))
ax.text(-1.0, 4.15, 'the tangents send $x_0 \\to x_1 \\to x_2 = x_0$:\nthe iteration cycles and never converges',
        color='#a8271f', fontsize=8.3, ha='center', va='top')
ax.plot([-1.7693],[0],'*',color=INK,ms=9,zorder=7)
ax.annotate('the real root is here',(-1.7693,0),textcoords='offset points',
            xytext=(4,-22),color=INK,fontsize=8.3)
ax.set_xlim(-2.35,1.75); ax.set_ylim(-1.1,4.35)
ax.set_xlabel('$x$'); ax.set_ylabel('$f(x) = x^3-2x+2$')
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.3)
```

| | Bisection | Newton-Raphson |
|---|---|---|
| Needs | an interval with a sign change | one starting value and $f'(x)$ |
| Always converges? | yes | no |
| Speed | slow (linear) | fast (quadratic) |
| Error known in advance? | yes, $\frac{b-a}{2^{n}}$ | no |
| Stop when | interval $<$ tolerance | two successive values agree |

::: tip Choosing a starting value
Take $x_{0}$ to be the end of the bracketing interval at which $f$ and $f''$ have
the **same sign** — in practice, the end where the curve is steeper. A common exam
instruction is simply "take $x_{0}$ = 1.5"; use what you are given. If two
successive iterates start moving apart, stop and restart from a better $x_{0}$.
:::

## 20.3 Numerical integration: trapezoidal rule

When an integrand has no elementary anti-derivative — $\sqrt{1+x^{3}}$,
$e^{-x^{2}}$, $\frac{\sin x}{x}$ — or when $f$ is known only as a table of measured
values, we approximate the area directly.

Divide $[a,b]$ into $n$ equal strips of width $h = \frac{b-a}{n}$ with ordinates

$$ y_{0}=f(a),\ y_{1}=f(a+h),\ y_{2}=f(a+2h),\ \ldots,\ y_{n}=f(b) $$

The trapezoidal rule replaces the curve over each strip by the **chord** joining its
two endpoints, so each strip becomes a trapezium of area
$\frac{h}{2}(y_{r}+y_{r+1})$. Adding all $n$ of them, every interior ordinate is
counted twice.

::: key Trapezoidal rule
$$ \int_{a}^{b}f(x)\,dx \approx \frac{h}{2}\left[(y_{0}+y_{n}) + 2(y_{1}+y_{2}+\cdots+y_{n-1})\right] $$
"half the width times (first + last + twice all the rest)". Any number of strips
$n \ge 1$ may be used.

**Error bound:** $|E_{T}| \le \frac{(b-a)h^{2}}{12}\,M_{2}$, where $M_{2}$ is the
greatest value of $|f''(x)|$ on $[a,b]$. The error is proportional to $h^{2}$, so
halving $h$ divides the error by about four.
:::

::: example Worked example 20.9
**Problem.** Evaluate $\int_{1}^{2}\frac{dx}{x}$ by the trapezoidal rule with
five sub-intervals, correct to six decimal places, and estimate the error.

**Solution.** Here $a=1$, $b=2$, $n=5$, so $h = \frac{2-1}{5} = 0.2$.

| $r$ | $x_{r}$ | $y_{r} = 1/x_{r}$ | end / interior |
|---|---|---|---|
| 0 | 1.0 | 1.000000 | end |
| 1 | 1.2 | 0.833333 | interior |
| 2 | 1.4 | 0.714286 | interior |
| 3 | 1.6 | 0.625000 | interior |
| 4 | 1.8 | 0.555556 | interior |
| 5 | 2.0 | 0.500000 | end |

Ends: $y_{0}+y_{5} = 1.500000$. Interiors:
$y_{1}+y_{2}+y_{3}+y_{4} = 2.728175$. Therefore

$$ T = \frac{0.2}{2}\left[1.500000 + 2(2.728175)\right] = 0.1 \times 6.956349
 = 0.695635 $$

**Error estimate.** $f(x) = x^{-1}$ gives $f''(x) = \frac{2}{x^{3}}$, whose greatest
value on $[1,2]$ is $M_{2} = 2$ (at $x=1$). So

$$ |E_{T}| \le \frac{(2-1)(0.2)^{2}}{12}\times 2 = \frac{0.04\times 2}{12}
 = 0.006667 $$

The exact value is $\ln 2 = 0.693147$, so the actual error is $0.002488$ —
comfortably inside the bound, as it must be.
:::

::: example Worked example 20.10
**Problem.** Use the trapezoidal rule with six sub-intervals to evaluate
$\int_{0}^{1}\frac{dx}{1+x^{2}}$ to six decimal places, and compare with the exact
value.

**Solution.** $h = \frac{1-0}{6} = \frac{1}{6} = 0.166667$.

| $r$ | $x_{r}$ | $y_{r} = \frac{1}{1+x_{r}^{2}}$ |
|---|---|---|
| 0 | 0.000000 | 1.000000 |
| 1 | 0.166667 | 0.972973 |
| 2 | 0.333333 | 0.900000 |
| 3 | 0.500000 | 0.800000 |
| 4 | 0.666667 | 0.692308 |
| 5 | 0.833333 | 0.590164 |
| 6 | 1.000000 | 0.500000 |

Ends: $1.500000$. Interiors: $0.972973+0.900000+0.800000+0.692308+0.590164
= 3.955445$. Hence

$$ T = \frac{0.166667}{2}\left[1.500000 + 2(3.955445)\right]
 = 0.083333 \times 9.410890 = 0.784241 $$

The exact value is $\left[\tan^{-1}x\right]_{0}^{1} = \frac{\pi}{4} = 0.785398$, so
the error is $0.001157$.
:::

::: caution The trapezoidal rule is biased, not random
For a curve that is concave up (like $y = 1/x$) every chord lies **above** the
curve, so the trapezoidal rule always **overestimates** the integral. For a
concave-down curve it always underestimates. Do not expect errors to cancel — they
accumulate in one direction, which is exactly why Simpson's rule is worth the extra
work.
:::

## 20.4 Numerical integration: Simpson's rule

Instead of joining the endpoints of each strip by a straight line, Simpson's rule
fits a **parabola** through three consecutive points. A parabola bends, so it tracks
a curve far better than a chord does.

```figure caption="Left: the trapezoidal rule joins the ordinates by chords, which lie above the concave-up curve $y=1/x$. Right: Simpson's rule fits a parabola through three ordinates, and it hugs the curve almost exactly."
import numpy as np, matplotlib.pyplot as plt
f = lambda t: 1.0/t
fig, axes = plt.subplots(1, 2, figsize=(5.2,2.6), sharey=True)
x = np.linspace(0.92, 3.1, 300)
xs = np.array([1.0, 2.0, 3.0]); ys = f(xs)
for ax, mode in zip(axes, ['trap', 'simp']):
    if mode == 'trap':
        for i in range(2):
            ax.fill_between([xs[i], xs[i+1]], [0,0], [ys[i], ys[i+1]],
                            color=ACCENT, alpha=0.18)
            ax.plot([xs[i], xs[i+1]], [ys[i], ys[i+1]], color=ACCENT, lw=1.6)
        ax.set_title('trapezoidal rule ($n=2$)', fontsize=9)
        ax.annotate('chord lies above\nthe curve', (2.25,0.72), color=ACCENT, fontsize=8.2)
    else:
        c = np.polyfit(xs, ys, 2)
        xp = np.linspace(1.0, 3.0, 200); yp = np.polyval(c, xp)
        ax.fill_between(xp, 0, yp, color='#2e8b57', alpha=0.18)
        ax.plot(xp, yp, color='#2e8b57', lw=1.6)
        ax.set_title("Simpson's rule ($n=2$)", fontsize=9)
        ax.annotate('parabola hugs\nthe curve', (2.25,0.72), color='#2e8b57', fontsize=8.2)
    ax.plot(x, f(x), color='#d9534f', lw=1.9, zorder=5)
    for xv, yv in zip(xs, ys):
        ax.plot([xv,xv],[0,yv], color=MUTED, lw=0.8, ls=':')
        ax.plot([xv],[yv],'o',color=INK,ms=3.4,zorder=6)
    ax.set_xticks(list(xs)); ax.set_xticklabels(['$x_0$','$x_1$','$x_2$'])
    ax.set_xlim(0.9,3.15); ax.set_ylim(0,1.18)
    ax.set_xlabel('$x$')
    ax.spines[['top','right']].set_visible(False)
axes[0].set_ylabel('$y=1/x$')
fig.tight_layout()
```

Because three points are needed for one parabola, the strips are consumed in pairs,
so **$n$ must be even**. Over the pair $[x_{0},x_{2}]$ the area under the fitted
parabola works out to $\frac{h}{3}(y_{0}+4y_{1}+y_{2})$; adding all such pairs gives
the alternating pattern of coefficients $4,2,4,2,\ldots,4$.

::: key Simpson's one-third rule
For an **even** number $n$ of sub-intervals of width $h = \frac{b-a}{n}$,

$$ \int_{a}^{b}f(x)\,dx \approx \frac{h}{3}\left[(y_{0}+y_{n})
 + 4(y_{1}+y_{3}+y_{5}+\cdots) + 2(y_{2}+y_{4}+\cdots)\right] $$

"one third of the width times (first + last + 4 times the odd ordinates + 2 times
the even ordinates)".

**Error bound:** $|E_{S}| \le \frac{(b-a)h^{4}}{180}\,M_{4}$, where $M_{4}$ is the
greatest value of $|f^{(4)}(x)|$ on $[a,b]$. The error goes like $h^{4}$, so halving
$h$ divides it by about sixteen.
:::

::: memory Which ordinates get 4 and which get 2
| Ordinate | $y_0$ | $y_1$ | $y_2$ | $y_3$ | $y_4$ | ... | $y_n$ |
|---|---|---|---|---|---|---|---|
| Coefficient | 1 | 4 | 2 | 4 | 2 | ... | 1 |

**Odd subscript $\to$ 4, even subscript $\to$ 2**, with the two end ordinates always
1. Check your coefficients add to $3n$ before multiplying: for $n=4$ they are
$1+4+2+4+1 = 12 = 3\times 4$.
:::

::: example Worked example 20.11
**Problem.** Evaluate $\int_{1}^{2}\frac{dx}{x}$ by Simpson's rule with four
sub-intervals, estimate the error, and hence give a value of $\ln 2$.

**Solution.** $h = \frac{2-1}{4} = 0.25$.

| $r$ | $x_{r}$ | $y_{r}=1/x_{r}$ | coefficient |
|---|---|---|---|
| 0 | 1.00 | 1.000000 | 1 |
| 1 | 1.25 | 0.800000 | 4 |
| 2 | 1.50 | 0.666667 | 2 |
| 3 | 1.75 | 0.571429 | 4 |
| 4 | 2.00 | 0.500000 | 1 |

Ends: $y_{0}+y_{4} = 1.500000$. Odd: $y_{1}+y_{3} = 1.371429$. Even:
$y_{2} = 0.666667$. Therefore

$$ S = \frac{0.25}{3}\left[1.500000 + 4(1.371429) + 2(0.666667)\right] $$

$$ = 0.083333 \times \left[1.500000 + 5.485714 + 1.333333\right]
 = 0.083333 \times 8.319048 = 0.693254 $$

**Error estimate.** $f(x) = x^{-1}$ gives $f^{(4)}(x) = \frac{24}{x^{5}}$, so
$M_{4} = 24$ at $x = 1$ and

$$ |E_{S}| \le \frac{(2-1)(0.25)^{4}}{180}\times 24 = \frac{0.00390625\times 24}{180}
 = 0.000521 $$

So $\ln 2 \approx 0.6933$, correct to three decimal places (the true value is
$0.693147$, an actual error of only $0.000107$). The trapezoidal rule in Worked
example 20.9 used *more* ordinates and was twenty times less accurate.
:::

::: example Worked example 20.12
**Problem.** Use Simpson's rule with six sub-intervals on
$\int_{0}^{1}\frac{dx}{1+x^{2}}$ to estimate $\pi$ correct to five decimal places.

**Solution.** Take the ordinate table from Worked example 20.10, with
$h = 0.166667$.

| $r$ | $x_{r}$ | $y_{r}$ | coefficient |
|---|---|---|---|
| 0 | 0.000000 | 1.000000 | 1 |
| 1 | 0.166667 | 0.972973 | 4 |
| 2 | 0.333333 | 0.900000 | 2 |
| 3 | 0.500000 | 0.800000 | 4 |
| 4 | 0.666667 | 0.692308 | 2 |
| 5 | 0.833333 | 0.590164 | 4 |
| 6 | 1.000000 | 0.500000 | 1 |

Ends: $1.500000$. Odd: $0.972973+0.800000+0.590164 = 2.363137$. Even:
$0.900000+0.692308 = 1.592308$.

$$ S = \frac{0.166667}{3}\left[1.500000 + 4(2.363137) + 2(1.592308)\right] $$

$$ = 0.055556\left[1.500000 + 9.452548 + 3.184616\right]
 = 0.055556 \times 14.137164 = 0.785398 $$

Since $\int_{0}^{1}\frac{dx}{1+x^{2}} = \frac{\pi}{4}$,

$$ \pi \approx 4 \times 0.785398 = 3.14159 $$

which is correct to all five decimal places shown.
:::

::: example Worked example 20.13
**Problem.** Evaluate $\int_{0}^{\pi/2}\sin x\,dx$ by (a) the trapezoidal rule and
(b) Simpson's rule, each with four sub-intervals, and compare with the exact value.

**Solution.** $h = \frac{\pi/2 - 0}{4} = \frac{\pi}{8} = 0.392699$ radians.

| $r$ | $x_{r}$ | $y_{r} = \sin x_{r}$ |
|---|---|---|
| 0 | 0.000000 | 0.000000 |
| 1 | 0.392699 | 0.382683 |
| 2 | 0.785398 | 0.707107 |
| 3 | 1.178097 | 0.923880 |
| 4 | 1.570796 | 1.000000 |

(a) Ends $= 1.000000$; interiors $= 0.382683+0.707107+0.923880 = 2.013670$:

$$ T = \frac{0.392699}{2}\left[1.000000 + 2(2.013670)\right]
 = 0.196350 \times 5.027340 = 0.987116 $$

(b) Odd $= 0.382683+0.923880 = 1.306563$; even $= 0.707107$:

$$ S = \frac{0.392699}{3}\left[1.000000 + 4(1.306563) + 2(0.707107)\right]
 = 0.130900 \times 7.640466 = 1.000135 $$

The exact value is $\left[-\cos x\right]_{0}^{\pi/2} = 1$. The trapezoidal error is
$0.012884$; Simpson's error is $0.000135$, about a hundred times smaller from the
same five ordinates.
:::

::: example Worked example 20.14 — Simpson's three-eighths rule
**Problem.** Evaluate $\int_{0}^{6}\frac{dx}{1+x}$ using Simpson's three-eighths
rule with six sub-intervals.

**Solution.** When $n$ is a multiple of three, fitting a cubic through four points
at a time gives

$$ \int_{a}^{b}f\,dx \approx \frac{3h}{8}\left[(y_{0}+y_{n})
 + 3(\text{ordinates whose subscript is not a multiple of }3)
 + 2(\text{the rest})\right] $$

Here $h = \frac{6-0}{6} = 1$.

| $r$ | $x_{r}$ | $y_{r} = \frac{1}{1+x_{r}}$ | coefficient |
|---|---|---|---|
| 0 | 0 | 1.000000 | 1 |
| 1 | 1 | 0.500000 | 3 |
| 2 | 2 | 0.333333 | 3 |
| 3 | 3 | 0.250000 | 2 |
| 4 | 4 | 0.200000 | 3 |
| 5 | 5 | 0.166667 | 3 |
| 6 | 6 | 0.142857 | 1 |

$$ S_{3/8} = \frac{3(1)}{8}\left[1.142857 + 3(1.200000) + 2(0.250000)\right]
 = 0.375 \times 5.242857 = 1.966071 $$

The exact value is $\ln 7 = 1.945910$. (For comparison, the one-third rule on the
same ordinates gives $1.958730$ and the trapezoidal rule gives $2.021429$: with a
strip width as coarse as $h=1$, none of them is very accurate.)
:::

```figure caption="Error against number of strips for $\int_1^2 dx/x$, on logarithmic axes. The trapezoidal error falls like $h^2$ and Simpson's like $h^4$, so the Simpson line is four times steeper."
import numpy as np, matplotlib.pyplot as plt
f = lambda t: 1.0/t
exact = np.log(2.0)
ns = np.array([2,4,8,16,32,64])
te, se = [], []
for n in ns:
    h = 1.0/n
    y = f(1.0 + h*np.arange(n+1))
    T = h/2*(y[0]+y[-1]+2*y[1:-1].sum())
    S = h/3*(y[0]+y[-1]+4*y[1:-1:2].sum()+2*y[2:-1:2].sum())
    te.append(abs(T-exact)); se.append(abs(S-exact))
ax = plt.subplots(figsize=(4.4,2.7))[1]; fig = ax.figure
ax.loglog(ns, te, 'o-', color=ACCENT, lw=1.5, ms=4, label='trapezoidal ($\\propto h^2$)')
ax.loglog(ns, se, 's-', color='#2e8b57', lw=1.5, ms=4, label="Simpson ($\\propto h^4$)")
ax.set_xlabel('number of strips $n$'); ax.set_ylabel('absolute error')
ax.set_xticks(list(ns)); ax.set_xticklabels([str(v) for v in ns])
ax.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
ax.legend(fontsize=8.2)
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.35, which='major')
```

| | Trapezoidal rule | Simpson's one-third rule |
|---|---|---|
| Curve replaced by | straight chords | parabolic arcs |
| Restriction on $n$ | none | must be even |
| Coefficients | $1,2,2,\ldots,2,1$ | $1,4,2,4,\ldots,4,1$ |
| Multiplier | $\frac{h}{2}$ | $\frac{h}{3}$ |
| Error | $\propto h^{2}$ | $\propto h^{4}$ |
| Exact for | linear $f$ | cubic $f$ and below |

::: tip Marks come from the table
Set out an ordinate table with a coefficient column every time, even when you can
see the answer. Write $h$, the ordinates to six decimals, the three sub-totals
(ends, odds, evens) and only then the substitution. If you slip on one ordinate you
still earn the method marks. A last check: all coefficients in Simpson's rule sum to
$3n$, and in the trapezoidal rule to $2n$.
:::

## 20.5 Extension: linear programming by the graphical method

Optimising a linear quantity subject to linear constraints is the other classical
computational method of school mathematics, and it uses the same "compute, tabulate,
compare" discipline. A **linear programming problem** asks you to maximise or
minimise an **objective function** $Z = ax+by$ subject to linear inequalities called
**constraints**, together with the non-negativity conditions $x \ge 0$, $y \ge 0$.

Each inequality shades a half-plane; their intersection is the **feasible region**.
Because $Z$ is linear, its level curves $ax+by = k$ form a family of parallel lines,
and sliding that line across the feasible region shows that the optimum is always
reached at a **corner point** (vertex) of the region. So the method is: draw the
region, find its vertices, evaluate $Z$ at each, and pick the best.

```figure caption="Feasible region for maximising $Z = 4x+3y$ subject to $x+y \le 8$, $2x+y \le 10$, $x,y \ge 0$. The dashed iso-profit lines $Z = 8, 16, 26$ move outwards until the last one touches the region at the corner $B(2,6)$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6,3.1))
x = np.linspace(0, 8.5, 200)
ax.plot(x, 8-x, color=ACCENT, lw=1.8, label='$x+y=8$')
ax.plot(x, 10-2*x, color='#d9534f', lw=1.8, label='$2x+y=10$')
verts = np.array([[0,0],[5,0],[2,6],[0,8]])
ax.fill(verts[:,0], verts[:,1], color='#2e8b57', alpha=0.18, zorder=1)
for (px,py),lab in zip(verts, ['$O(0,0)$','$C(5,0)$','$B(2,6)$','$A(0,8)$']):
    ax.plot([px],[py],'o',color=INK,ms=4.5,zorder=6)
    ax.annotate(lab,(px,py),textcoords='offset points',xytext=(6,5),color=INK,fontsize=8.4)
for Z, st, lx in [(8,(0,(3,2)),1.2),(16,(0,(3,2)),3.0),(26,'solid',5.1)]:
    ax.plot(x, (Z-4*x)/3.0, color='#6a5acd', lw=1.2, ls=st)
    ax.annotate(f'$Z={Z}$',(lx,(Z-4*lx)/3.0),textcoords='offset points',xytext=(3,4),
                color='#6a5acd',fontsize=8)
ax.set_xlim(-0.4,7.2); ax.set_ylim(-0.6,9.6)
ax.set_xlabel('$x$'); ax.set_ylabel('$y$')
ax.legend(fontsize=8.2, loc='upper right')
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.35)
```

::: example Worked example 20.15
**Problem.** Maximise $Z = 4x+3y$ subject to $x+y \le 8$, $2x+y \le 10$,
$x \ge 0$, $y \ge 0$.

**Solution.** Draw the boundary lines. $x+y=8$ passes through $(8,0)$ and $(0,8)$;
$2x+y=10$ passes through $(5,0)$ and $(0,10)$. Testing the origin in each
inequality gives $0 \le 8$ and $0 \le 10$, both true, so the feasible region is the
side of each line containing the origin.

The two lines meet where $x+y=8$ and $2x+y=10$; subtracting, $x=2$, so $y=6$. The
vertices of the region are $O(0,0)$, $C(5,0)$, $B(2,6)$ and $A(0,8)$. Evaluate the
objective function at each:

| Vertex | $(x,y)$ | $Z = 4x+3y$ |
|---|---|---|
| $O$ | $(0,0)$ | $0$ |
| $C$ | $(5,0)$ | $20$ |
| $B$ | $(2,6)$ | $\mathbf{26}$ |
| $A$ | $(0,8)$ | $24$ |

The maximum is $Z = 26$, attained at $x = 2$, $y = 6$.
:::

## Chapter summary

- A root of $f(x)=0$ is bracketed whenever $f(a)\,f(b) < 0$ and $f$ is continuous on
  $[a,b]$.
- **Bisection:** repeatedly take $c = \frac{a+b}{2}$ and keep the half in which the
  sign change lies. It always converges, and $|x_{n}-\alpha| \le \frac{b-a}{2^{n}}$,
  so $n > \frac{\ln((b-a)/\varepsilon)}{\ln 2}$ iterations guarantee accuracy
  $\varepsilon$.
- **Newton-Raphson:** $x_{n+1} = x_{n} - \frac{f(x_{n})}{f'(x_{n})}$, obtained by
  replacing the curve with its tangent. Convergence is quadratic (correct digits
  double each step) but is not guaranteed; it fails when $f'(x_{n})$ is zero or the
  start is poor.
- Special cases: $x_{n+1} = \frac12\left(x_{n}+\frac{N}{x_{n}}\right)$ for
  $\sqrt{N}$, and $x_{n+1} = \frac{1}{3}\left(2x_{n}+\frac{N}{x_{n}^{2}}\right)$ for
  $\sqrt[3]{N}$.
- **Trapezoidal rule** with $h = \frac{b-a}{n}$:
  $\int_{a}^{b}f\,dx \approx \frac{h}{2}\left[(y_{0}+y_{n})+2(y_{1}+\cdots+y_{n-1})\right]$,
  with $|E_{T}| \le \frac{(b-a)h^{2}}{12}M_{2}$. Any $n$ is allowed.
- **Simpson's one-third rule** ($n$ even):
  $\int_{a}^{b}f\,dx \approx \frac{h}{3}\left[(y_{0}+y_{n})+4(\text{odd }y)+2(\text{even }y)\right]$,
  with $|E_{S}| \le \frac{(b-a)h^{4}}{180}M_{4}$. Simpson's three-eighths rule uses
  $\frac{3h}{8}$ with coefficients $1,3,3,2,3,3,\ldots,1$ and needs $n$ a multiple
  of three.
- Simpson's rule is exact for any cubic; the trapezoidal rule is exact only for a
  straight line and always errs to the same side of a curve of fixed concavity.
- In a linear programming problem the optimum of $Z = ax+by$ occurs at a corner of
  the feasible region, so evaluate $Z$ at every vertex and compare.
- Round only at the end, keep six decimals throughout, and always state the accuracy
  claimed and the error estimate when the question asks for one.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The bisection method can be started on $[a,b]$ only if <span class="marks">[1]</span>
   (a) $f(a) = f(b)$ (b) $f(a)\,f(b) < 0$ (c) $f(a)\,f(b) > 0$ (d) $f'(a)=0$
2. After $n$ bisections of $[a,b]$ the error in the midpoint is at most <span class="marks">[1]</span>
   (a) $\frac{b-a}{n}$ (b) $\frac{b-a}{2n}$ (c) $\frac{b-a}{2^{n}}$ (d) $\frac{b-a}{n^{2}}$
3. The Newton-Raphson iteration formula is <span class="marks">[1]</span>
   (a) $x_{n+1}=x_{n}+\frac{f(x_{n})}{f'(x_{n})}$ (b) $x_{n+1}=x_{n}-\frac{f(x_{n})}{f'(x_{n})}$ (c) $x_{n+1}=x_{n}-\frac{f'(x_{n})}{f(x_{n})}$ (d) $x_{n+1}=\frac{x_{n}}{f'(x_{n})}$
4. Newton-Raphson fails at $x_{n}$ when <span class="marks">[1]</span>
   (a) $f(x_{n})=0$ (b) $f'(x_{n})=0$ (c) $x_{n}>0$ (d) $f''(x_{n})=0$
5. In Simpson's one-third rule the number of sub-intervals must be <span class="marks">[1]</span>
   (a) odd (b) even (c) a multiple of 3 (d) a prime
6. In the trapezoidal rule the multiplier outside the bracket is <span class="marks">[1]</span>
   (a) $h$ (b) $\frac{h}{2}$ (c) $\frac{h}{3}$ (d) $\frac{3h}{8}$
7. Simpson's one-third rule integrates exactly every polynomial of degree at most <span class="marks">[1]</span>
   (a) 1 (b) 2 (c) 3 (d) 4
8. Which equation is transcendental? <span class="marks">[1]</span>
   (a) $x^{5}-3x+1=0$ (b) $2x^{2}-7=0$ (c) $xe^{x}-1=0$ (d) $x^{3}=8$
9. Using $f(x)=x^{2}-5$ with $x_{0}=2$, the first Newton-Raphson iterate is <span class="marks">[1]</span>
   (a) $2.2500$ (b) $2.2361$ (c) $2.5000$ (d) $2.0000$
10. The error of the trapezoidal rule is proportional to <span class="marks">[1]</span>
    (a) $h$ (b) $h^{2}$ (c) $h^{3}$ (d) $h^{4}$
11. In a linear programming problem the optimal value of the objective function
    occurs <span class="marks">[1]</span>
    (a) at the origin always (b) at a corner point of the feasible region (c) at the centre of the region (d) outside the region

::: note Answers to Group A
**1.** (b) — opposite signs guarantee a crossing by the location theorem.

**2.** (c) — the interval halves every step, so its width is $\frac{b-a}{2^{n}}$.

**3.** (b) — subtract $\frac{f}{f'}$; this is the tangent meeting the $x$-axis.

**4.** (b) — a zero derivative means a horizontal tangent, which never meets the
axis, and the formula divides by zero.

**5.** (b) — strips are used in pairs, one parabola per pair.

**6.** (b) — each trapezium has area $\frac{h}{2}(y_r+y_{r+1})$.

**7.** (c) — the cubic terms cancel in the error analysis, so Simpson's rule is
exact for cubics.

**8.** (c) — it contains $e^{x}$; the others are polynomial equations.

**9.** (a) — $x_1 = 2 - \frac{4-5}{4} = 2.25$.

**10.** (b) — $|E_T| \le \frac{(b-a)h^{2}}{12}M_2$.

**11.** (b) — the level lines of a linear $Z$ are parallel, so the extreme is pushed
to a vertex.
:::

**Group B — Short answer (5 marks each)**

1. Show that the equation $x^{3}-x-1=0$ has a root between $1$ and $2$, and find it
   correct to one decimal place by the bisection method. <span class="marks">[5]</span>
2. Find a root of $xe^{x} = 1$ correct to two decimal places using the bisection
   method on $[0,1]$. <span class="marks">[5]</span>
3. Derive the Newton-Raphson iteration formula from Taylor's theorem, and state two
   circumstances in which it fails. <span class="marks">[5]</span>
4. Use the Newton-Raphson method with $x_{0}=2$ to find the root of
   $x^{3}-2x-5=0$ correct to five decimal places. <span class="marks">[5]</span>
5. Evaluate $\int_{0}^{1}e^{x}dx$ by the trapezoidal rule with four sub-intervals
   and compare with the exact value. <span class="marks">[5]</span>
6. Evaluate $\int_{1}^{2}\ln x\,dx$ by Simpson's rule with four sub-intervals,
   giving your answer to five decimal places. <span class="marks">[5]</span>
7. Show that Simpson's rule gives the exact value of $\int_{0}^{2}x^{3}dx$ with
   $n=4$, and explain why. <span class="marks">[5]</span>
8. Use $x_{n+1} = \frac{1}{5}\left(4x_{n}+\frac{32}{x_{n}^{4}}\right)$, obtained
   from Newton-Raphson applied to $x^{5}-32=0$, with $x_{0}=2.1$ to compute
   $\sqrt[5]{32}$ to five decimal places. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** $f(1) = 1-1-1 = -1 < 0$ and $f(2) = 8-2-1 = 5 > 0$, so by the location
theorem a root lies in $[1,2]$. Bisecting:

| $n$ | $a$ | $b$ | $c$ | $f(c)$ |
|---|---|---|---|---|
| 1 | 1.0000 | 2.0000 | 1.5000 | $+0.8750$ |
| 2 | 1.0000 | 1.5000 | 1.2500 | $-0.2969$ |
| 3 | 1.2500 | 1.5000 | 1.3750 | $+0.2246$ |
| 4 | 1.2500 | 1.3750 | 1.3125 | $-0.0515$ |
| 5 | 1.3125 | 1.3750 | 1.3438 | $+0.0826$ |
| 6 | 1.3125 | 1.3438 | 1.3281 | $+0.0146$ |
| 7 | 1.3125 | 1.3281 | 1.3203 | $-0.0187$ |

The error bound is now $\frac{1}{2^{7}} = 0.0078 < 0.05$, so $\alpha \approx 1.3$
to one decimal place.

**2.** Let $f(x) = xe^{x}-1$. Then $f(0) = -1 < 0$ and
$f(1) = e-1 = 1.7183 > 0$, so a root lies in $[0,1]$.

| $n$ | $a$ | $b$ | $c$ | $f(c) = ce^{c}-1$ |
|---|---|---|---|---|
| 1 | 0.0000 | 1.0000 | 0.5000 | $-0.1756$ |
| 2 | 0.5000 | 1.0000 | 0.7500 | $+0.5878$ |
| 3 | 0.5000 | 0.7500 | 0.6250 | $+0.1677$ |
| 4 | 0.5000 | 0.6250 | 0.5625 | $-0.0128$ |
| 5 | 0.5625 | 0.6250 | 0.5938 | $+0.0751$ |
| 6 | 0.5625 | 0.5938 | 0.5781 | $+0.0306$ |
| 7 | 0.5625 | 0.5781 | 0.5703 | $+0.0088$ |
| 8 | 0.5625 | 0.5703 | 0.5664 | $-0.0020$ |

The bound is $\frac{1}{2^{8}} = 0.0039 < 0.005$, so $\alpha \approx 0.57$ to two
decimal places (true value $0.567143$).

**3.** Let $x_{n}$ approximate the root and let $h$ satisfy $f(x_{n}+h) = 0$. By
Taylor's theorem, $f(x_{n}+h) = f(x_{n}) + hf'(x_{n}) + \ldots$; neglecting the
terms in $h^{2}$ and higher because $h$ is small,
$$ f(x_{n}) + hf'(x_{n}) \approx 0 \;\Longrightarrow\; h \approx -\frac{f(x_{n})}{f'(x_{n})} $$
so $x_{n+1} = x_{n} - \frac{f(x_{n})}{f'(x_{n})}$. It fails (i) when
$f'(x_{n}) = 0$, since the tangent is then parallel to the $x$-axis and the formula
divides by zero, and (ii) when the starting value is far from the root, in which
case the iterates may diverge or cycle (for example $x^{3}-2x+2=0$ with $x_{0}=0$
oscillates between $0$ and $1$).

**4.** $f(x) = x^{3}-2x-5$, $f'(x) = 3x^{2}-2$, so
$x_{n+1} = \frac{2x_{n}^{3}+5}{3x_{n}^{2}-2}$.

| $n$ | $x_{n}$ | $f(x_{n})$ | $f'(x_{n})$ | $x_{n+1}$ |
|---|---|---|---|---|
| 0 | 2.00000000 | $-1.00000000$ | 10.00000000 | 2.10000000 |
| 1 | 2.10000000 | $+0.06100000$ | 11.23000000 | 2.09456812 |
| 2 | 2.09456812 | $+0.00018572$ | 11.16164684 | 2.09455148 |

Hence $\alpha \approx 2.09455$.

**5.** $h = 0.25$; ordinates $y_r = e^{x_r}$:

| $r$ | $x_{r}$ | $y_{r}$ |
|---|---|---|
| 0 | 0.00 | 1.000000 |
| 1 | 0.25 | 1.284025 |
| 2 | 0.50 | 1.648721 |
| 3 | 0.75 | 2.117000 |
| 4 | 1.00 | 2.718282 |

Ends $= 3.718282$; interiors $= 5.049746$. So
$$ T = \frac{0.25}{2}\left[3.718282 + 2(5.049746)\right] = 0.125 \times 13.817774
 = 1.727222 $$
The exact value is $\left[e^{x}\right]_{0}^{1} = e-1 = 1.718282$, so the
trapezoidal rule overestimates by $0.008940$ — as expected, since $y=e^{x}$ is
concave up.

**6.** $h = 0.25$; ordinates $y_r = \ln x_r$:

| $r$ | $x_{r}$ | $y_{r}$ | coefficient |
|---|---|---|---|
| 0 | 1.00 | 0.000000 | 1 |
| 1 | 1.25 | 0.223144 | 4 |
| 2 | 1.50 | 0.405465 | 2 |
| 3 | 1.75 | 0.559616 | 4 |
| 4 | 2.00 | 0.693147 | 1 |

Ends $= 0.693147$; odd $= 0.782760$; even $= 0.405465$.
$$ S = \frac{0.25}{3}\left[0.693147 + 4(0.782760) + 2(0.405465)\right]
 = 0.083333 \times 4.635117 = 0.386260 $$
So $\int_{1}^{2}\ln x\,dx \approx 0.38626$ (exact value $2\ln 2 - 1 = 0.386294$).

**7.** With $a=0$, $b=2$, $n=4$ we get $h = 0.5$ and ordinates
$y = 0,\ 0.125,\ 1,\ 3.375,\ 8$. Ends $= 8$; odd $= 0.125+3.375 = 3.5$;
even $= 1$.
$$ S = \frac{0.5}{3}\left[8 + 4(3.5) + 2(1)\right] = \frac{0.5}{3}\times 24
 = 4.000000 $$
The exact value is $\left[\frac{x^{4}}{4}\right]_{0}^{2} = 4$. They agree because
Simpson's error term involves the fourth derivative, and $f^{(4)}(x) = 0$ for a
cubic, so the rule is exact for every polynomial of degree three or less.

**8.** With $x_{0}=2.1$:

| $n$ | $x_{n}$ | $x_{n+1} = \frac{1}{5}\left(4x_{n}+\frac{32}{x_{n}^{4}}\right)$ |
|---|---|---|
| 0 | 2.10000000 | 2.00908099 |
| 1 | 2.00908099 | 2.00008172 |
| 2 | 2.00008172 | 2.00000001 |

So $\sqrt[5]{32} \approx 2.00000$, which is right, since $2^{5} = 32$.
:::

**Group C — Long answer (8 marks each)**

1. (a) State the location theorem and use it to show that $\cos x = x$ has a root
   between $0$ and $1$ radian. <span class="marks">[2]</span>
   (b) Find that root correct to two decimal places by the bisection method, showing
   the error bound at each stage. <span class="marks">[6]</span>
2. (a) Derive the trapezoidal rule for $n$ sub-intervals. <span class="marks">[3]</span>
   (b) Hence evaluate $\int_{0}^{1}\sqrt{1+x^{3}}\,dx$ with four sub-intervals, and
   also apply Simpson's rule to the same ordinates. State which answer you trust
   more and why. <span class="marks">[5]</span>
3. (a) Obtain the Newton-Raphson formula for $\sqrt{N}$ and use it to find
   $\sqrt{13}$ correct to six decimal places starting from $x_{0}=3.5$. <span class="marks">[5]</span>
   (b) Compare the bisection and Newton-Raphson methods under the headings
   *reliability*, *speed* and *information required*. <span class="marks">[3]</span>
4. A cottage industry in Bhaktapur makes two products. Maximise $Z = 4x+3y$
   subject to $x+y \le 8$, $2x+y \le 10$, $x \ge 0$, $y \ge 0$, by the graphical
   method, listing all corner points and the value of $Z$ at each. <span class="marks">[8]</span>

::: note Answers to Group C
**1. (a)** *Location theorem:* if $f$ is continuous on $[a,b]$ and
$f(a)\,f(b) < 0$, then $f(x) = 0$ has at least one root in $(a,b)$. Put
$f(x) = \cos x - x$, which is continuous. Then $f(0) = 1 - 0 = +1$ and
$f(1) = 0.540302 - 1 = -0.459698$. The signs are opposite, so a root lies in
$(0,1)$.

**(b)**

| $n$ | $a$ | $b$ | $c$ | $f(c)$ | error bound $\frac{1}{2^{n}}$ |
|---|---|---|---|---|---|
| 1 | 0.000000 | 1.000000 | 0.500000 | $+0.377583$ | 0.500000 |
| 2 | 0.500000 | 1.000000 | 0.750000 | $-0.018311$ | 0.250000 |
| 3 | 0.500000 | 0.750000 | 0.625000 | $+0.185963$ | 0.125000 |
| 4 | 0.625000 | 0.750000 | 0.687500 | $+0.085335$ | 0.062500 |
| 5 | 0.687500 | 0.750000 | 0.718750 | $+0.033879$ | 0.031250 |
| 6 | 0.718750 | 0.750000 | 0.734375 | $+0.007875$ | 0.015625 |
| 7 | 0.734375 | 0.750000 | 0.742188 | $-0.005196$ | 0.007813 |
| 8 | 0.734375 | 0.742188 | 0.738281 | $+0.001345$ | 0.003906 |

The bound $0.003906$ is below $0.005$, so the root is $0.74$ correct to two decimal
places.

**2. (a)** Divide $[a,b]$ into $n$ strips of width $h = \frac{b-a}{n}$ with
ordinates $y_{0},y_{1},\ldots,y_{n}$. Replacing the curve over the $r$-th strip by
the chord makes it a trapezium of parallel sides $y_{r}$ and $y_{r+1}$ and width
$h$, so its area is $\frac{h}{2}(y_{r}+y_{r+1})$. Summing from $r=0$ to $n-1$, each
interior ordinate appears in two trapezia and each end ordinate in one:
$$ \int_{a}^{b}f(x)dx \approx \frac{h}{2}\left[(y_{0}+y_{n})
 + 2(y_{1}+y_{2}+\cdots+y_{n-1})\right] $$

**(b)** $h = 0.25$ and $y_r = \sqrt{1+x_r^{3}}$:

| $r$ | $x_{r}$ | $y_{r}$ |
|---|---|---|
| 0 | 0.00 | 1.000000 |
| 1 | 0.25 | 1.007782 |
| 2 | 0.50 | 1.060660 |
| 3 | 0.75 | 1.192424 |
| 4 | 1.00 | 1.414214 |

Trapezoidal: ends $= 2.414214$, interiors $= 3.260866$, so
$$ T = \frac{0.25}{2}\left[2.414214 + 2(3.260866)\right] = 0.125 \times 8.935946
 = 1.116993 $$
Simpson: odd $= 1.007782+1.192424 = 2.200206$, even $= 1.060660$, so
$$ S = \frac{0.25}{3}\left[2.414214 + 4(2.200206) + 2(1.060660)\right]
 = 0.083333 \times 13.336158 = 1.111363 $$
Simpson's value is the more reliable, because its error is of order $h^{4}$ against
$h^{2}$ for the trapezoidal rule. (The true value is $1.111448$, so Simpson is out
by $0.000085$ and the trapezoidal rule by $0.005545$.)

**3. (a)** Put $f(x) = x^{2}-N$, so $f'(x) = 2x$. Then
$$ x_{n+1} = x_{n} - \frac{x_{n}^{2}-N}{2x_{n}}
 = \frac{2x_{n}^{2}-x_{n}^{2}+N}{2x_{n}} = \frac{1}{2}\left(x_{n}+\frac{N}{x_{n}}\right) $$
With $N=13$ and $x_{0}=3.5$:

| $n$ | $x_{n}$ | $x_{n+1}$ |
|---|---|---|
| 0 | 3.50000000 | 3.60714286 |
| 1 | 3.60714286 | 3.60555163 |
| 2 | 3.60555163 | 3.60555128 |

Hence $\sqrt{13} \approx 3.605551$.

**(b)** *Reliability:* bisection always converges provided the initial interval
brackets a root; Newton-Raphson may diverge or cycle. *Speed:* bisection gains
about one binary digit per iteration (linear convergence), whereas Newton-Raphson
roughly doubles the number of correct digits each iteration (quadratic
convergence), so it typically needs three or four steps against ten or more.
*Information required:* bisection needs only values of $f$ and a sign change;
Newton-Raphson needs the derivative $f'$ and a good starting value, but no
bracketing interval.

**4.** Draw $x+y=8$ through $(8,0)$ and $(0,8)$, and $2x+y=10$ through $(5,0)$ and
$(0,10)$. Substituting the origin into each constraint gives $0 \le 8$ and
$0 \le 10$, both true, so the feasible region lies on the origin side of both
lines, in the first quadrant. Solving the two boundary equations simultaneously:
subtracting $x+y=8$ from $2x+y=10$ gives $x=2$, hence $y=6$. The corner points are
therefore $O(0,0)$, $C(5,0)$, $B(2,6)$ and $A(0,8)$.

| Corner point | $Z = 4x+3y$ |
|---|---|
| $O(0,0)$ | $0$ |
| $C(5,0)$ | $20 + 0 = 20$ |
| $B(2,6)$ | $8 + 18 = 26$ |
| $A(0,8)$ | $0 + 24 = 24$ |

The feasible region is a closed bounded polygon, so the maximum is attained at a
corner. The greatest value is $Z = 26$, at $x = 2$ and $y = 6$.
:::
