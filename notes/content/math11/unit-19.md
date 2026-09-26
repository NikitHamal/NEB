---
subject: Mathematics
grade: 11
unit: 19
title: Anti-derivatives
hours: 16
area: Calculus
---

Differentiation takes a function and produces its rate of change. Anti-differentiation
runs the machine backwards: you are given the rate of change and must recover the
function. That single idea — reversing the derivative — turns out to compute areas,
volumes, distances travelled from a velocity, and the total from a rate. At 16 hours
this is the largest chapter of Grade 11 Mathematics, and it carries the most marks in
the calculus area of the paper.

::: key What the examiner asks for
Almost every question is of one of five kinds: *use a standard form*, *substitute*,
*integrate by parts*, *evaluate a definite integral (often using a property)*, or
*find an area*. Learn to recognise which of the five a question is, and the rest is
routine algebra. Marks are given per step — always write the substitution you are
making and the form you are reducing to.
:::

## 19.1 Basic (standard) integrals

### The anti-derivative

::: definition Anti-derivative and indefinite integral
A function $F(x)$ is an **anti-derivative** of $f(x)$ on an interval if
$F'(x) = f(x)$ for every $x$ in that interval. The collection of all
anti-derivatives of $f$ is written

$$ \int f(x)\,dx = F(x) + C $$

and is called the **indefinite integral** of $f$. Here $f(x)$ is the *integrand*,
$x$ is the *variable of integration*, $dx$ says which variable, and $C$ is the
**constant of integration**.
:::

Why a constant? Because $\frac{d}{dx}(C) = 0$, so if $F'(x) = f(x)$ then
$(F(x)+C)' = f(x)$ too. Two anti-derivatives of the same function can differ only
by a constant, so $F(x)+C$ is the complete answer, not just one answer.

Geometrically, the anti-derivatives of $f$ form a family of curves, each a vertical
translate of the others. At any fixed $x_0$ every curve in the family has the same
gradient $f(x_0)$.

```figure caption="The family $y = x^2 + C$: all the anti-derivatives of $f(x)=2x$. Every member has the same gradient at a given $x$, so the family is one curve slid up and down."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.4,2.9))
x = np.linspace(-2.2, 2.2, 300)
for C, c in zip([-2,-1,0,1,2], SERIES):
    ax.plot(x, x**2 + C, color=c, lw=1.5)
    ax.annotate(f'C = {C}', (2.2, 4.84+C), textcoords='offset points',
                xytext=(3,-3), color=c, fontsize=8)
x0 = 1.0
for C in [-2,0,2]:
    tt = np.array([x0-0.55, x0+0.55])
    ax.plot(tt, x0**2+C + 2*x0*(tt-x0), color=INK, lw=1.0, ls=(0,(3,2)))
    ax.plot([x0],[x0**2+C],'o',color=INK,ms=3.2)
ax.annotate('same slope $2x_0$\nat every $C$', (x0+0.55, 3.0+0.0),
            textcoords='offset points', xytext=(-104,14), color=INK, fontsize=8.4,
            arrowprops=dict(arrowstyle='-|>', color=INK, lw=0.9, mutation_scale=9))
ax.axhline(0, color=MUTED, lw=0.8); ax.axvline(0, color=MUTED, lw=0.8)
ax.set_xlim(-2.3, 3.0); ax.set_ylim(-2.6, 7.2)
ax.set_xlabel('$x$'); ax.set_ylabel('$y$')
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.4)
```

### Two rules that do all the splitting

$$ \int k\,f(x)\,dx = k\int f(x)\,dx \qquad \int [f(x) \pm g(x)]\,dx = \int f(x)\,dx \pm \int g(x)\,dx $$

There is **no** product rule and **no** quotient rule for integration. A product must
be turned into something integrable — by multiplying out, by a trigonometric
identity, by substitution, or by parts.

### The standard integrals

::: key Complete table of standard integrals
Every one of these is just a derivative read backwards. Add $+\,C$ to each.

| No. | Integral | Result |
|---|---|---|
| 1 | $\int x^n\,dx$ | $\frac{x^{n+1}}{n+1}$,  $n \neq -1$ |
| 2 | $\int \frac{dx}{x}$ | $\ln|x|$ |
| 3 | $\int e^{x}\,dx$ | $e^{x}$ |
| 4 | $\int a^{x}\,dx$ | $\frac{a^{x}}{\ln a}$,  $a>0,\ a \neq 1$ |
| 5 | $\int \sin x\,dx$ | $-\cos x$ |
| 6 | $\int \cos x\,dx$ | $\sin x$ |
| 7 | $\int \sec^{2} x\,dx$ | $\tan x$ |
| 8 | $\int \csc^{2} x\,dx$ | $-\cot x$ |
| 9 | $\int \sec x\tan x\,dx$ | $\sec x$ |
| 10 | $\int \csc x\cot x\,dx$ | $-\csc x$ |
| 11 | $\int \tan x\,dx$ | $\ln|\sec x|$ |
| 12 | $\int \cot x\,dx$ | $\ln|\sin x|$ |
| 13 | $\int \sec x\,dx$ | $\ln|\sec x + \tan x|$ |
| 14 | $\int \csc x\,dx$ | $\ln|\csc x - \cot x|$ |
| 15 | $\int \frac{dx}{\sqrt{a^{2}-x^{2}}}$ | $\sin^{-1}\frac{x}{a}$ |
| 16 | $\int \frac{dx}{a^{2}+x^{2}}$ | $\frac{1}{a}\tan^{-1}\frac{x}{a}$ |
| 17 | $\int \frac{dx}{x\sqrt{x^{2}-a^{2}}}$ | $\frac{1}{a}\sec^{-1}\frac{x}{a}$ |
| 18 | $\int \frac{dx}{x^{2}-a^{2}}$ | $\frac{1}{2a}\ln\frac{|x-a|}{|x+a|}$ |
| 19 | $\int \frac{dx}{a^{2}-x^{2}}$ | $\frac{1}{2a}\ln\frac{|a+x|}{|a-x|}$ |
| 20 | $\int \frac{dx}{\sqrt{x^{2}+a^{2}}}$ | $\ln|x+\sqrt{x^{2}+a^{2}}|$ |
| 21 | $\int \frac{dx}{\sqrt{x^{2}-a^{2}}}$ | $\ln|x+\sqrt{x^{2}-a^{2}}|$ |
| 22 | $\int \sqrt{a^{2}-x^{2}}\,dx$ | $\frac{x}{2}\sqrt{a^{2}-x^{2}} + \frac{a^{2}}{2}\sin^{-1}\frac{x}{a}$ |
| 23 | $\int \sqrt{x^{2}+a^{2}}\,dx$ | $\frac{x}{2}\sqrt{x^{2}+a^{2}} + \frac{a^{2}}{2}\ln|x+\sqrt{x^{2}+a^{2}}|$ |
| 24 | $\int \sqrt{x^{2}-a^{2}}\,dx$ | $\frac{x}{2}\sqrt{x^{2}-a^{2}} - \frac{a^{2}}{2}\ln|x+\sqrt{x^{2}-a^{2}}|$ |
| 25 | $\int \frac{f'(x)}{f(x)}\,dx$ | $\ln|f(x)|$ |
| 26 | $\int [f(x)]^{n}f'(x)\,dx$ | $\frac{[f(x)]^{n+1}}{n+1}$,  $n \neq -1$ |
| 27 | $\int e^{x}[f(x)+f'(x)]\,dx$ | $e^{x}f(x)$ |
:::

Two generalisations follow at once from the chain rule. For any constants $a \neq 0$
and $b$,

$$ \int f(ax+b)\,dx = \frac{1}{a}F(ax+b) + C \qquad \text{where } F'=f $$

so, for example, $\int \cos(3x+1)\,dx = \frac{1}{3}\sin(3x+1)+C$ and
$\int (2x-5)^{7}dx = \frac{(2x-5)^{8}}{16}+C$.

::: caution The "divide by the inner derivative" trick only works for linear inners
$\int (2x-5)^7 dx = \frac{(2x-5)^8}{16}+C$ is right because the inside is linear.
But $\int (x^2-5)^7 dx \neq \frac{(x^2-5)^8}{16x}$ — dividing by $2x$ is illegal,
because $2x$ is not a constant and cannot be moved through the integral sign.
:::

::: example Worked example 19.1
**Problem.** Evaluate $\int \left(3x^{4} - \frac{5}{x^{2}} + 2\sqrt{x} - 7\right)dx$.

**Solution.** Split the integral and write every term as a power of $x$:

$$ \int 3x^{4}dx - \int 5x^{-2}dx + \int 2x^{1/2}dx - \int 7\,dx $$

Apply rule 1 to each term ($n = 4,\,-2,\,\tfrac12,\,0$):

$$ = \frac{3x^{5}}{5} - 5\cdot\frac{x^{-1}}{-1} + 2\cdot\frac{x^{3/2}}{3/2} - 7x + C
 = \frac{3x^{5}}{5} + \frac{5}{x} + \frac{4}{3}x^{3/2} - 7x + C $$

**Check.** Differentiating gives back $3x^4 - 5x^{-2} + 2x^{1/2} - 7$. Always spend
five seconds on this check; it costs nothing and catches sign slips.
:::

::: example Worked example 19.2
**Problem.** Evaluate $\int \left(\sqrt{x} + \frac{1}{\sqrt{x}}\right)^{2}dx$.

**Solution.** There is no product rule, so **expand first**:

$$ \left(\sqrt{x}+\frac{1}{\sqrt{x}}\right)^{2} = x + 2 + \frac{1}{x} $$

Now every term is standard:

$$ \int\left(x+2+\frac{1}{x}\right)dx = \frac{x^{2}}{2} + 2x + \ln|x| + C $$
:::

::: example Worked example 19.3
**Problem.** Evaluate $\int \tan^{2}x\,dx$ and $\int \frac{dx}{1+\cos x}$.

**Solution.** Neither integrand is in the table, so convert with an identity.

(a) Using $\sec^2 x = 1 + \tan^2 x$, so $\tan^2 x = \sec^2 x - 1$:

$$ \int \tan^{2}x\,dx = \int(\sec^{2}x - 1)dx = \tan x - x + C $$

(b) Using $1+\cos x = 2\cos^{2}\frac{x}{2}$:

$$ \int \frac{dx}{2\cos^{2}(x/2)} = \frac{1}{2}\int \sec^{2}\frac{x}{2}\,dx
 = \frac{1}{2}\cdot\frac{\tan(x/2)}{1/2} + C = \tan\frac{x}{2} + C $$
:::

::: example Worked example 19.4
**Problem.** Evaluate $\int \left(e^{x} + 2^{x} + \frac{3}{1+x^{2}}\right)dx$.

**Solution.** Standard forms 3, 4 and 16 (with $a=1$):

$$ = e^{x} + \frac{2^{x}}{\ln 2} + 3\tan^{-1}x + C $$
:::

### Why integration is harder than differentiation

Differentiation is mechanical. Given any combination of the standard functions, the
product, quotient and chain rules will grind out the derivative in a finite number of
steps, and there is never any doubt about what to do next. Integration has no such
algorithm. There is no rule for the integral of a product, and there are perfectly
ordinary-looking functions — $e^{-x^{2}}$, $\frac{\sin x}{x}$, $\sqrt{1+x^{3}}$ —
whose anti-derivatives cannot be written down in terms of the functions you know at
all. So integration is a matter of **pattern recognition**: you learn a table of
standard forms, and you learn three or four manoeuvres (substitution, parts, partial
fractions, trigonometric identities) for pushing an unfamiliar integral into that
table. When you meet a new integral, the first question is never "what is the rule?"
but "which standard form is this trying to be?".

### Finding one particular anti-derivative

An indefinite integral gives the whole family $F(x)+C$. In an applied problem one
extra piece of information — the value of the function at one point, called an
**initial condition** or boundary condition — pins down $C$ and selects one member
of the family. This is the pattern for every "given the rate, find the quantity"
question in the paper.

::: example Worked example 19.5
**Problem.** A curve passes through the point $(1,4)$ and its gradient at every
point is $\frac{dy}{dx} = 3x^{2}-2x+1$. Find the equation of the curve.

**Solution.** Integrate the gradient to recover $y$:

$$ y = \int (3x^{2}-2x+1)\,dx = x^{3}-x^{2}+x+C $$

Now use the condition that the curve passes through $(1,4)$, so $y = 4$ when $x=1$:

$$ 4 = 1 - 1 + 1 + C \;\Longrightarrow\; C = 3 $$

Hence the curve is $y = x^{3}-x^{2}+x+3$. Only one curve of the family fits, because
only one vertical translate passes through the given point.
:::

::: example Worked example 19.6
**Problem.** A particle moves in a straight line with velocity
$v = 3t^{2}-4t+2$ (in m s⁻¹) at time $t$ seconds, and is at $s = 5$ m from the
origin when $t=0$. Find its displacement at $t = 3$ s.

**Solution.** Velocity is the rate of change of displacement, so displacement is the
anti-derivative of velocity:

$$ s = \int (3t^{2}-4t+2)\,dt = t^{3}-2t^{2}+2t + C $$

At $t=0$, $s=5$, so $C = 5$ and $s = t^{3}-2t^{2}+2t+5$. At $t = 3$ s,

$$ s = 27 - 18 + 6 + 5 = 20 \ \text{m} $$
:::

## 19.2 Integration by substitution

Substitution is the chain rule reversed. If $x = g(t)$ is a differentiable function
with $dx = g'(t)\,dt$, then

$$ \int f(x)\,dx = \int f(g(t))\,g'(t)\,dt $$

In practice you go the other way: you spot a function $u = g(x)$ inside the integrand
whose derivative $g'(x)$ is also present (up to a constant), put $du = g'(x)dx$, and
the integral collapses to a standard form in $u$.

::: tip How to choose the substitution
Look for the **inner function** of a composition — what is under a root, inside a
bracket raised to a power, in an exponent, or in a denominator. Call it $u$. The
substitution works if $du$ uses up the rest of the integrand apart from a constant.
:::

### The two workhorse forms

$$ \int \frac{f'(x)}{f(x)}\,dx = \ln|f(x)| + C \qquad
\int [f(x)]^{n}f'(x)\,dx = \frac{[f(x)]^{n+1}}{n+1}+C \ \ (n \neq -1) $$

::: example Worked example 19.7
**Problem.** Evaluate (a) $\int \frac{x\,dx}{x^{2}+1}$  (b) $\int x^{2}\sqrt{x^{3}+2}\ dx$.

**Solution.**

(a) Put $u = x^{2}+1$, so $du = 2x\,dx$, i.e. $x\,dx = \tfrac12 du$:

$$ \int\frac{x\,dx}{x^2+1} = \frac{1}{2}\int\frac{du}{u} = \frac{1}{2}\ln|u| + C
 = \frac{1}{2}\ln(x^{2}+1) + C $$

(The modulus can be dropped because $x^2+1 > 0$ always.)

(b) Put $u = x^{3}+2$, so $du = 3x^{2}dx$, i.e. $x^{2}dx = \tfrac13 du$:

$$ \frac{1}{3}\int u^{1/2}du = \frac{1}{3}\cdot\frac{u^{3/2}}{3/2}+C
 = \frac{2}{9}(x^{3}+2)^{3/2} + C $$
:::

::: example Worked example 19.8
**Problem.** Prove that $\int \tan x\,dx = \ln|\sec x| + C$, and evaluate
$\int \frac{e^{\sqrt{x}}}{\sqrt{x}}\,dx$.

**Solution.** $\int\tan x\,dx = \int\frac{\sin x}{\cos x}dx$. Put $u = \cos x$, so
$du = -\sin x\,dx$:

$$ \int\frac{\sin x}{\cos x}dx = -\int\frac{du}{u} = -\ln|u| + C
 = -\ln|\cos x| + C = \ln|\sec x| + C $$

For the second integral put $u = \sqrt{x}$, so $du = \frac{dx}{2\sqrt{x}}$, i.e.
$\frac{dx}{\sqrt{x}} = 2\,du$:

$$ \int \frac{e^{\sqrt{x}}}{\sqrt{x}}dx = 2\int e^{u}du = 2e^{u}+C = 2e^{\sqrt{x}}+C $$
:::

### A substitution that needs the inverse

Sometimes the substitution does not clear out the whole integrand in one stroke and
you must also express the leftover $x$ in terms of $u$. That is allowed, and it is
often the neatest route when a linear expression sits under a root.

::: example Worked example 19.9
**Problem.** Evaluate $\int \frac{x\,dx}{\sqrt{x+1}}$.

**Solution.** Put $u = x+1$, so $du = dx$ and, rearranging, $x = u-1$:

$$ \int\frac{(u-1)}{\sqrt{u}}du = \int\left(u^{1/2}-u^{-1/2}\right)du
 = \frac{2}{3}u^{3/2} - 2u^{1/2} + C $$

$$ = \frac{2}{3}(x+1)^{3/2} - 2\sqrt{x+1} + C $$
:::

::: derivation The integral of $\sec x$
This looks like a trick, but it is the standard NEB derivation and is worth
memorising. Multiply top and bottom by $\sec x + \tan x$:

$$ \int\sec x\,dx = \int\frac{\sec x(\sec x+\tan x)}{\sec x+\tan x}\,dx
 = \int\frac{\sec^{2}x + \sec x\tan x}{\sec x + \tan x}\,dx $$

The numerator is now exactly the derivative of the denominator, because
$\frac{d}{dx}(\sec x+\tan x) = \sec x\tan x + \sec^{2}x$. So by form 25,

$$ \int\sec x\,dx = \ln|\sec x + \tan x| + C $$

The same device with $\csc x - \cot x$ gives
$\int\csc x\,dx = \ln|\csc x - \cot x| + C$.
:::

### Deriving the standard forms 18, 16 and 15

These three appear in the table, but NEB regularly asks you to *derive* them.

::: derivation The forms $\frac{1}{x^2-a^2}$, $\frac{1}{a^2+x^2}$ and $\frac{1}{\sqrt{a^2-x^2}}$
**(i)** Split into partial fractions:
$\frac{1}{x^{2}-a^{2}} = \frac{1}{(x-a)(x+a)} = \frac{1}{2a}\left(\frac{1}{x-a}-\frac{1}{x+a}\right)$.
Integrating each term with form 25,

$$ \int\frac{dx}{x^{2}-a^{2}} = \frac{1}{2a}\left(\ln|x-a| - \ln|x+a|\right) + C
 = \frac{1}{2a}\ln\frac{|x-a|}{|x+a|} + C $$

**(ii)** Put $x = a\tan\theta$, so $dx = a\sec^{2}\theta\,d\theta$ and
$a^{2}+x^{2} = a^{2}\sec^{2}\theta$:

$$ \int\frac{a\sec^{2}\theta\,d\theta}{a^{2}\sec^{2}\theta} = \frac{1}{a}\int d\theta
 = \frac{\theta}{a}+C = \frac{1}{a}\tan^{-1}\frac{x}{a}+C $$

**(iii)** Put $x = a\sin\theta$, so $dx = a\cos\theta\,d\theta$ and
$\sqrt{a^{2}-x^{2}} = a\cos\theta$:

$$ \int\frac{a\cos\theta\,d\theta}{a\cos\theta} = \int d\theta = \theta + C
 = \sin^{-1}\frac{x}{a}+C $$
:::

The substitutions used in (ii) and (iii) are the **trigonometric substitutions**.
Choose them from the shape of the surd, and read the other sides off a right-angled
triangle when you have to convert back to $x$.

```figure caption="The three trigonometric substitutions. Draw the triangle, label two sides from the substitution, and the third side is the surd you need."
import numpy as np, matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 3, figsize=(5.2,2.0))
specs = [('$x=a\\sin\\theta$', '$a$', '$x$', '$\\sqrt{a^2-x^2}$'),
         ('$x=a\\tan\\theta$', '$\\sqrt{a^2+x^2}$', '$x$', '$a$'),
         ('$x=a\\sec\\theta$', '$x$', '$\\sqrt{x^2-a^2}$', '$a$')]
for ax,(sub,hyp,opp,adj) in zip(axes, specs):
    A,B,C = np.array([0,0]), np.array([3.2,0]), np.array([3.2,1.9])
    ax.plot([A[0],B[0],C[0],A[0]],[A[1],B[1],C[1],A[1]], color=INK, lw=1.5)
    ax.plot([B[0]-0.3,B[0]-0.3,B[0]],[B[1],B[1]+0.3,B[1]+0.3], color=MUTED, lw=0.9)
    th = np.linspace(0, np.arctan2(1.9,3.2), 40)
    ax.plot(0.75*np.cos(th), 0.75*np.sin(th), color='#d9534f', lw=1.1)
    ax.annotate(r'$\theta$', (0.95,0.20), color='#d9534f', fontsize=9.5)
    ax.annotate(hyp, (1.15,1.32), color=INK, fontsize=9, ha='center')
    ax.annotate(opp, (3.3,0.95), color=INK, fontsize=9, ha='left')
    ax.annotate(adj, (1.6,-0.05), color=INK, fontsize=9, ha='center', va='top')
    ax.set_title(sub, fontsize=9)
    ax.set_xlim(-0.35,4.6); ax.set_ylim(-0.8,2.6)
    ax.set_aspect('equal'); ax.axis('off')
fig.tight_layout()
```

| Expression in the integrand | Substitution | It becomes |
|---|---|---|
| $\sqrt{a^{2}-x^{2}}$ or $a^2-x^2$ | $x = a\sin\theta$ | $a\cos\theta$ |
| $\sqrt{a^{2}+x^{2}}$ or $a^2+x^2$ | $x = a\tan\theta$ | $a\sec\theta$ |
| $\sqrt{x^{2}-a^{2}}$ or $x^2-a^2$ | $x = a\sec\theta$ | $a\tan\theta$ |
| $\sqrt{\frac{a-x}{a+x}}$ | $x = a\cos 2\theta$ | $\tan\theta$ form |

::: example Worked example 19.10
**Problem.** Evaluate (a) $\int\frac{dx}{x^{2}-9}$  (b) $\int\frac{dx}{\sqrt{4-9x^{2}}}$.

**Solution.**

(a) This is form 18 with $a = 3$:

$$ \int\frac{dx}{x^{2}-9} = \frac{1}{2(3)}\ln\frac{|x-3|}{|x+3|} + C
 = \frac{1}{6}\ln\frac{|x-3|}{|x+3|} + C $$

(b) Take the $9$ out of the surd: $\sqrt{4-9x^{2}} = 3\sqrt{\frac{4}{9}-x^{2}}$, so
with $a = \frac{2}{3}$,

$$ \frac{1}{3}\int\frac{dx}{\sqrt{(2/3)^{2}-x^{2}}} = \frac{1}{3}\sin^{-1}\frac{x}{2/3}+C
 = \frac{1}{3}\sin^{-1}\frac{3x}{2} + C $$
:::

::: example Worked example 19.11
**Problem.** Evaluate $\int\sqrt{9-x^{2}}\,dx$ by trigonometric substitution.

**Solution.** Put $x = 3\sin\theta$, $dx = 3\cos\theta\,d\theta$; then
$\sqrt{9-x^{2}} = 3\cos\theta$.

$$ \int 3\cos\theta\cdot 3\cos\theta\,d\theta = 9\int\cos^{2}\theta\,d\theta
 = \frac{9}{2}\int(1+\cos 2\theta)\,d\theta $$

$$ = \frac{9}{2}\left(\theta + \frac{\sin 2\theta}{2}\right)+C
 = \frac{9}{2}\theta + \frac{9}{2}\sin\theta\cos\theta + C $$

Back-substitute using the first triangle: $\sin\theta = \frac{x}{3}$,
$\cos\theta = \frac{\sqrt{9-x^{2}}}{3}$, $\theta = \sin^{-1}\frac{x}{3}$:

$$ = \frac{9}{2}\sin^{-1}\frac{x}{3} + \frac{x}{2}\sqrt{9-x^{2}} + C $$

which is entry 22 of the table with $a = 3$.
:::

### Quadratics in the denominator: complete the square

Any $ax^{2}+bx+c$ can be written as $a\left[(x+\frac{b}{2a})^{2} + \frac{4ac-b^2}{4a^2}\right]$.
After the shift $u = x + \frac{b}{2a}$, the integral is one of forms 15, 16, 18, 19,
20 or 21.

::: example Worked example 19.12
**Problem.** Evaluate (a) $\int\frac{dx}{x^{2}+4x+13}$  (b) $\int\frac{dx}{\sqrt{x^{2}+6x+5}}$.

**Solution.**

(a) $x^{2}+4x+13 = (x+2)^{2}+9$. With $u = x+2$, $du = dx$, and $a = 3$ in form 16:

$$ \int\frac{du}{u^{2}+3^{2}} = \frac{1}{3}\tan^{-1}\frac{u}{3}+C
 = \frac{1}{3}\tan^{-1}\frac{x+2}{3}+C $$

(b) $x^{2}+6x+5 = (x+3)^{2}-4$. With $u = x+3$ and $a = 2$ in form 21:

$$ \int\frac{du}{\sqrt{u^{2}-2^{2}}} = \ln|u+\sqrt{u^{2}-4}|+C
 = \ln|x+3+\sqrt{x^{2}+6x+5}|+C $$
:::

### The form $\frac{px+q}{ax^{2}+bx+c}$

Write the numerator as **(a multiple of the derivative of the denominator) + (a constant)**:

$$ px+q = \lambda\,(2ax+b) + \mu $$

The $\lambda$ part integrates by form 25 to a logarithm; the $\mu$ part is handled by
completing the square as above. The same split works with the denominator under a
square root.

::: example Worked example 19.13
**Problem.** Evaluate $\int\frac{x+2}{x^{2}+2x+5}\,dx$.

**Solution.** The derivative of the denominator is $2x+2$. Write

$$ x+2 = \tfrac{1}{2}(2x+2) + 1 $$

so the integral splits as

$$ \frac{1}{2}\int\frac{2x+2}{x^{2}+2x+5}dx + \int\frac{dx}{x^{2}+2x+5} $$

The first is form 25; the second needs $x^{2}+2x+5 = (x+1)^{2}+4$:

$$ = \frac{1}{2}\ln(x^{2}+2x+5) + \frac{1}{2}\tan^{-1}\frac{x+1}{2} + C $$
:::

### Rational functions: partial fractions

If the integrand is $\frac{P(x)}{Q(x)}$ with $P,Q$ polynomials, first make it a
**proper** fraction (degree of $P$ less than degree of $Q$) by dividing out. Then
split $\frac{P}{Q}$ into partial fractions using the four denominator cases.

| Factor in $Q(x)$ | Contributes |
|---|---|
| distinct linear $(x-a)$ | $\frac{A}{x-a}$ |
| repeated linear $(x-a)^{k}$ | $\frac{A_1}{x-a}+\frac{A_2}{(x-a)^{2}}+\cdots+\frac{A_k}{(x-a)^{k}}$ |
| distinct quadratic $(x^{2}+px+q)$ | $\frac{Ax+B}{x^{2}+px+q}$ |
| repeated quadratic $(x^{2}+px+q)^{k}$ | $\frac{A_1x+B_1}{x^{2}+px+q}+\cdots+\frac{A_kx+B_k}{(x^{2}+px+q)^{k}}$ |

Partial fractions always work on a rational function, because every polynomial with
real coefficients factorises into linear factors and irreducible quadratic factors.
Those are precisely the two kinds of piece we know how to integrate: a linear
denominator gives a logarithm, and an irreducible quadratic gives a logarithm plus an
inverse tangent after completing the square. So a rational function can always, in
principle, be integrated — which is not true of most other families of functions.

::: example Worked example 19.14 — distinct linear factors
**Problem.** Evaluate $\int\frac{3x-1}{(x-1)(x-2)}\,dx$.

**Solution.** Write $\frac{3x-1}{(x-1)(x-2)} = \frac{A}{x-1}+\frac{B}{x-2}$, so

$$ 3x-1 = A(x-2) + B(x-1) $$

Put $x = 1$: $\ 2 = -A$, so $A = -2$. Put $x = 2$: $\ 5 = B$. Hence

$$ \int\left(\frac{-2}{x-1}+\frac{5}{x-2}\right)dx = -2\ln|x-1| + 5\ln|x-2| + C $$
:::

::: example Worked example 19.15 — a repeated linear factor
**Problem.** Evaluate $\int\frac{dx}{x(x+1)^{2}}$.

**Solution.** Set $\frac{1}{x(x+1)^{2}} = \frac{A}{x}+\frac{B}{x+1}+\frac{D}{(x+1)^{2}}$, so

$$ 1 = A(x+1)^{2} + Bx(x+1) + Dx $$

Put $x = 0$: $A = 1$. Put $x = -1$: $1 = -D$, so $D = -1$. Comparing coefficients of
$x^{2}$: $A + B = 0$, so $B = -1$. Therefore

$$ \int\left(\frac{1}{x}-\frac{1}{x+1}-\frac{1}{(x+1)^{2}}\right)dx
 = \ln|x| - \ln|x+1| + \frac{1}{x+1} + C $$
:::

::: example Worked example 19.16 — a non-repeated quadratic factor
**Problem.** Evaluate $\int\frac{dx}{(x+1)(x^{2}+1)}$.

**Solution.** Set $\frac{1}{(x+1)(x^{2}+1)} = \frac{A}{x+1}+\frac{Bx+D}{x^{2}+1}$, so

$$ 1 = A(x^{2}+1) + (Bx+D)(x+1) $$

Put $x = -1$: $1 = 2A$, so $A = \frac12$. Coefficient of $x^{2}$: $A+B = 0$, so
$B = -\frac12$. Constant term: $A + D = 1$, so $D = \frac12$. Hence

$$ \int\left(\frac{1/2}{x+1} + \frac{-\tfrac12 x + \tfrac12}{x^{2}+1}\right)dx
 = \frac{1}{2}\ln|x+1| - \frac{1}{4}\ln(x^{2}+1) + \frac{1}{2}\tan^{-1}x + C $$
:::

::: example Worked example 19.17 — a repeated quadratic factor
**Problem.** Evaluate $\int\frac{dx}{x(x^{2}+1)^{2}}$.

**Solution.** Set
$\frac{1}{x(x^{2}+1)^{2}} = \frac{A}{x}+\frac{Bx+D}{x^{2}+1}+\frac{Ex+F}{(x^{2}+1)^{2}}$, so

$$ 1 = A(x^{2}+1)^{2} + (Bx+D)\,x\,(x^{2}+1) + (Ex+F)\,x $$

Put $x = 0$: $A = 1$. Comparing coefficients: $x^{4}$ gives $A+B = 0$ so $B=-1$;
$x^{3}$ gives $D = 0$; $x^{2}$ gives $2A+B+E = 0$ so $E = -1$; $x^{1}$ gives
$D+F = 0$ so $F = 0$. The integral becomes

$$ \int\frac{dx}{x} - \int\frac{x\,dx}{x^{2}+1} - \int\frac{x\,dx}{(x^{2}+1)^{2}} $$

Each of the last two yields to $u = x^{2}+1$, $du = 2x\,dx$:

$$ = \ln|x| - \frac{1}{2}\ln(x^{2}+1) + \frac{1}{2(x^{2}+1)} + C $$
:::

::: caution An improper fraction must be divided first
$\int\frac{x^{2}+1}{x^{2}-1}dx$ cannot go straight to partial fractions — the top
and bottom have the same degree. Divide first:
$\frac{x^{2}+1}{x^{2}-1} = 1 + \frac{2}{x^{2}-1}$, giving
$x + \ln\frac{|x-1|}{|x+1|} + C$ by form 18 with $a=1$.
:::

## 19.3 Integration by parts

Integrate the product rule $\frac{d}{dx}(uv) = u\frac{dv}{dx} + v\frac{du}{dx}$
over $x$:

$$ uv = \int u\,\frac{dv}{dx}\,dx + \int v\,\frac{du}{dx}\,dx $$

Rearranging gives the rule.

::: key Integration by parts
$$ \int u\,\frac{dv}{dx}\,dx = uv - \int v\,\frac{du}{dx}\,dx $$
In the shorthand $\int u\,dv = uv - \int v\,du$: "integral of (first $\times$ second)
= first $\times$ integral of second $-$ integral of (derivative of first $\times$
integral of second)."
:::

The whole skill is choosing which factor is $u$ (to be differentiated) and which is
$dv$ (to be integrated). Choose $u$ to be whichever comes **first** in this list:

::: memory ILATE — the order for choosing $u$
| Letter | Type of function | Example |
|---|---|---|
| **I** | Inverse trigonometric | $\sin^{-1}x$, $\tan^{-1}x$ |
| **L** | Logarithmic | $\ln x$, $\log_{10}x$ |
| **A** | Algebraic | $x$, $x^{2}$, $3x-1$ |
| **T** | Trigonometric | $\sin x$, $\cos x$ |
| **E** | Exponential | $e^{x}$, $2^{x}$ |

The function earlier in ILATE becomes $u$; the other becomes $dv$. The reason is
simple: I and L get *simpler* when differentiated but are painful to integrate, while
T and E integrate as easily as they differentiate.
:::

::: example Worked example 19.18
**Problem.** Evaluate $\int x e^{x}\,dx$.

**Solution.** Algebraic (A) beats exponential (E), so $u = x$ and $dv = e^{x}dx$.
Then $du = dx$ and $v = e^{x}$.

$$ \int x e^{x}dx = x e^{x} - \int e^{x}\,dx = xe^{x} - e^{x} + C = (x-1)e^{x}+C $$

Had we chosen the other way round ($u = e^x$), the remaining integral would be
$\int \frac{x^2}{2}e^x dx$ — worse than what we started with. That is what ILATE
protects you from.
:::

::: example Worked example 19.19
**Problem.** Evaluate (a) $\int \ln x\,dx$  (b) $\int \tan^{-1}x\,dx$.

**Solution.** Both have only one visible factor; supply a second factor of $1$.

(a) $u = \ln x$ (L), $dv = 1\cdot dx$, so $du = \frac{dx}{x}$ and $v = x$:

$$ \int \ln x\,dx = x\ln x - \int x\cdot\frac{dx}{x} = x\ln x - x + C $$

(b) $u = \tan^{-1}x$ (I), $dv = dx$, so $du = \frac{dx}{1+x^{2}}$ and $v = x$:

$$ \int\tan^{-1}x\,dx = x\tan^{-1}x - \int\frac{x\,dx}{1+x^{2}}
 = x\tan^{-1}x - \frac{1}{2}\ln(1+x^{2}) + C $$
:::

::: example Worked example 19.20
**Problem.** Evaluate $\int x\ln x\,dx$.

**Solution.** L comes before A, so $u = \ln x$ and $dv = x\,dx$; then
$du = \frac{dx}{x}$ and $v = \frac{x^{2}}{2}$:

$$ \int x\ln x\,dx = \frac{x^{2}}{2}\ln x - \int\frac{x^{2}}{2}\cdot\frac{dx}{x}
 = \frac{x^{2}}{2}\ln x - \frac{1}{2}\int x\,dx = \frac{x^{2}}{2}\ln x - \frac{x^{2}}{4}+C $$
:::

### Repeated parts

If the algebraic factor is $x^{n}$, apply the rule $n$ times.

::: example Worked example 19.21 — parts applied twice
**Problem.** Evaluate $\int x^{2}e^{2x}dx$.

**Solution.** First application: $u = x^{2}$, $dv = e^{2x}dx$, $v = \frac{e^{2x}}{2}$:

$$ \int x^{2}e^{2x}dx = \frac{x^{2}e^{2x}}{2} - \int 2x\cdot\frac{e^{2x}}{2}dx
 = \frac{x^{2}e^{2x}}{2} - \int x e^{2x}dx $$

Second application on $\int xe^{2x}dx$ with $u = x$, $v = \frac{e^{2x}}{2}$:

$$ \int xe^{2x}dx = \frac{xe^{2x}}{2} - \int\frac{e^{2x}}{2}dx = \frac{xe^{2x}}{2} - \frac{e^{2x}}{4} $$

Putting the pieces together,

$$ \int x^{2}e^{2x}dx = \frac{x^{2}e^{2x}}{2} - \frac{xe^{2x}}{2} + \frac{e^{2x}}{4} + C
 = \frac{e^{2x}}{4}\left(2x^{2}-2x+1\right) + C $$
:::

::: example Worked example 19.22
**Problem.** Evaluate $\int x^{2}\sin x\,dx$.

**Solution.** A beats T, so $u = x^{2}$ and $dv = \sin x\,dx$, giving $v = -\cos x$:

$$ \int x^{2}\sin x\,dx = -x^{2}\cos x + 2\int x\cos x\,dx $$

Apply parts again to $\int x\cos x\,dx$ with $u = x$ and $v = \sin x$:

$$ \int x\cos x\,dx = x\sin x - \int\sin x\,dx = x\sin x + \cos x $$

Therefore

$$ \int x^{2}\sin x\,dx = -x^{2}\cos x + 2x\sin x + 2\cos x + C $$

Notice the pattern: each application lowers the power of $x$ by one, so a factor
$x^{n}$ needs exactly $n$ applications.
:::

### The $e^{x}[f(x)+f'(x)]$ form

Integration by parts produces one standard form so often that it is quicker to
recognise it than to derive it each time.

::: derivation Why $\int e^{x}[f(x)+f'(x)]dx = e^{x}f(x)+C$
Split the integral and apply parts to the first piece with $u = f(x)$,
$dv = e^{x}dx$:

$$ \int e^{x}f(x)\,dx = e^{x}f(x) - \int e^{x}f'(x)\,dx $$

Adding $\int e^{x}f'(x)dx$ to both sides,

$$ \int e^{x}\left[f(x)+f'(x)\right]dx = e^{x}f(x) + C $$

To use it, look for an expression of the form $e^x$ times (something plus its own
derivative). For example, in $\int e^{x}\left(\frac{1}{x}-\frac{1}{x^{2}}\right)dx$
take $f(x)=\frac1x$, since $f'(x) = -\frac{1}{x^{2}}$; the answer is
$\frac{e^{x}}{x}+C$.
:::

### The cyclic case

When both factors are of type T or E, two applications bring back the original
integral. Treat it as an unknown and solve for it algebraically.

::: example Worked example 19.23 — the cyclic trick
**Problem.** Evaluate $I = \int e^{x}\sin x\,dx$.

**Solution.** Take $u = \sin x$, $dv = e^{x}dx$:

$$ I = e^{x}\sin x - \int e^{x}\cos x\,dx $$

Apply parts again to the new integral, with $u = \cos x$, $dv = e^{x}dx$:

$$ \int e^{x}\cos x\,dx = e^{x}\cos x + \int e^{x}\sin x\,dx = e^{x}\cos x + I $$

Substituting back,

$$ I = e^{x}\sin x - e^{x}\cos x - I \;\Longrightarrow\; 2I = e^{x}(\sin x - \cos x) $$

$$ I = \frac{e^{x}}{2}(\sin x - \cos x) + C $$
:::

::: caution Keep the *same* choice of $u$ both times
In the cyclic case, if the second application swaps the roles (taking $u = e^x$
instead of the trigonometric factor) you simply undo the first step and get the
useless identity $I = I$. Stay consistent: trigonometric as $u$ both times, or
exponential as $u$ both times.
:::

A result worth memorising, which follows from the same trick:

$$ \int e^{ax}\sin bx\,dx = \frac{e^{ax}(a\sin bx - b\cos bx)}{a^{2}+b^{2}} + C $$

::: example Worked example 19.24
**Problem.** Evaluate $\int x\sec^{2}x\,dx$.

**Solution.** A before T, so $u = x$, $dv = \sec^{2}x\,dx$, giving $v = \tan x$:

$$ \int x\sec^{2}x\,dx = x\tan x - \int\tan x\,dx = x\tan x - \ln|\sec x| + C $$

which can also be written $x\tan x + \ln|\cos x| + C$.
:::

::: tip Deciding which method to use
Work down this list and stop at the first line that matches.

1. **Is it already a standard form?** Check the table, including forms 25, 26 and 27.
   Allow for a linear inner function $ax+b$ (divide by $a$ at the end).
2. **Can algebra or a trigonometric identity simplify it first?** Expand brackets,
   divide out an improper fraction, use $\sec^2 = 1+\tan^2$, $\sin^2 = \frac{1-\cos2x}{2}$,
   $2\sin A\cos B = \sin(A+B)+\sin(A-B)$.
3. **Is there an inner function whose derivative is also present?** Substitute.
   A surd $\sqrt{a^2 \pm x^2}$ or $\sqrt{x^2-a^2}$ asks for a trigonometric
   substitution; a quadratic denominator asks you to complete the square.
4. **Is it a quotient of polynomials?** Divide if improper, then partial fractions.
5. **Is it a product of two unrelated types of function?** Integrate by parts,
   choosing $u$ by ILATE.

If none of these fits, you have probably copied the question down wrongly.
:::

## 19.4 Definite integral

### Definition as the limit of a sum

Divide $[a,b]$ into $n$ equal sub-intervals of width $h = \frac{b-a}{n}$. On each
sub-interval build a rectangle whose height is the value of $f$ at the right-hand
end. The total rectangle area is $\sum_{r=1}^{n} f(a+rh)\,h$. As $n$ grows the
rectangles hug the curve better and better.

::: definition Definite integral
$$ \int_{a}^{b} f(x)\,dx = \lim_{n\to\infty} h\sum_{r=1}^{n} f(a+rh), \qquad h=\frac{b-a}{n} $$
$a$ is the **lower limit**, $b$ the **upper limit**. The result is a *number*, not a
family of functions, so no constant of integration appears.
:::

```figure caption="Rectangles approximating $\int_0^1 x^2 dx$. With $n=4$, $10$ and $40$ strips the total area falls towards the exact value $1/3$."
import numpy as np, matplotlib.pyplot as plt
f = lambda t: t**2
fig, axes = plt.subplots(1, 3, figsize=(5.2,2.3), sharey=True)
x = np.linspace(0, 1, 300)
for ax, n in zip(axes, [4, 10, 40]):
    h = 1.0/n
    xs = np.arange(n)*h
    ax.bar(xs, f(xs+h), width=h, align='edge', color=ACCENT, alpha=0.30,
           edgecolor=ACCENT, linewidth=0.5)
    ax.plot(x, f(x), color='#d9534f', lw=1.6, zorder=4)
    S = h*np.sum(f(xs+h))
    ax.set_title(f'n = {n},  S = {S:.4f}', fontsize=8.6)
    ax.set_xlim(0,1); ax.set_ylim(0,1.05)
    ax.set_xticks([0,1]); ax.set_xlabel('$x$')
    ax.spines[['top','right']].set_visible(False)
axes[0].set_yticks([0,1]); axes[0].set_ylabel('$y=x^2$')
fig.suptitle('$S \\to 1/3 = 0.3333$  as  $n \\to \\infty$', fontsize=9, y=1.05)
fig.tight_layout()
```

::: example Worked example 19.25 — from first principles
**Problem.** Evaluate $\int_{0}^{1}x^{2}dx$ as the limit of a sum.

**Solution.** Here $a=0$, $b=1$, $h = \frac{1}{n}$ and $f(x) = x^{2}$, so

$$ \int_0^1 x^2 dx = \lim_{n\to\infty} h\sum_{r=1}^{n}(rh)^{2}
 = \lim_{n\to\infty}\frac{1}{n^{3}}\sum_{r=1}^{n}r^{2} $$

Using $\sum_{r=1}^{n}r^{2} = \frac{n(n+1)(2n+1)}{6}$,

$$ = \lim_{n\to\infty}\frac{n(n+1)(2n+1)}{6n^{3}}
 = \lim_{n\to\infty}\frac{1}{6}\left(1+\frac{1}{n}\right)\left(2+\frac{1}{n}\right)
 = \frac{1\times 1\times 2}{6} = \frac{1}{3} $$
:::

The two kinds of integral are different objects and are marked differently, so keep
them apart.

| | Indefinite integral | Definite integral |
|---|---|---|
| Written | $\int f(x)\,dx$ | $\int_{a}^{b}f(x)\,dx$ |
| Result is | a family of functions | a single number |
| Constant $C$ | compulsory | cancels, so omitted |
| Means | all anti-derivatives of $f$ | signed area from $a$ to $b$ |
| On substituting | change back to $x$ at the end | change the limits instead |

### The fundamental theorem of calculus

Computing every definite integral from the definition would be unbearable. The
fundamental theorem converts it into an anti-derivative evaluation.

::: key Fundamental theorem of calculus
If $F$ is any anti-derivative of a continuous $f$ on $[a,b]$, then
$$ \int_{a}^{b}f(x)\,dx = \left[F(x)\right]_{a}^{b} = F(b) - F(a) $$
The constant of integration cancels: $(F(b)+C)-(F(a)+C) = F(b)-F(a)$, so you may
drop $C$ in a definite integral.
:::

::: derivation Why the fundamental theorem is true
Define the **area function** $A(x) = \int_{a}^{x}f(t)\,dt$, the signed area from the
fixed left end $a$ up to a movable right end $x$. Increasing $x$ by a small amount
$h$ adds a thin strip of width $h$ and height roughly $f(x)$, so
$A(x+h) - A(x) \approx f(x)\,h$. Dividing by $h$ and letting $h \to 0$,

$$ A'(x) = \lim_{h\to 0}\frac{A(x+h)-A(x)}{h} = f(x) $$

So the area function is itself an anti-derivative of $f$. If $F$ is any other
anti-derivative then $A(x) = F(x) + C$ for some constant. Putting $x = a$ gives
$0 = F(a)+C$, so $C = -F(a)$, and putting $x = b$ gives

$$ \int_{a}^{b}f(x)\,dx = A(b) = F(b) - F(a) $$

This is the link between the two halves of calculus: area (a limit of a sum) is
computed by anti-differentiation.
:::

Geometrically $\int_a^b f(x)\,dx$ is the **signed area** between the curve and the
$x$-axis from $x=a$ to $x=b$: the limit of the thin strips of height $f(x)$ and
width $dx$.

```figure caption="The definite integral $\int_a^b f(x)\,dx$ is the shaded area, built up from strips of area $f(x)\,dx$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6,2.9))
f = lambda t: 0.45*t**2 + 1.0
x = np.linspace(0, 5, 400)
a, b = 1.0, 4.0
xs = np.linspace(a, b, 200)
ax.fill_between(xs, 0, f(xs), color=ACCENT, alpha=0.16, zorder=1)
for p, lab in [(a,'$a$'), (b,'$b$')]:
    ax.vlines(p, 0, f(p), color=MUTED, lw=1.0, ls=':')
    ax.annotate(lab, (p,0), textcoords='offset points', xytext=(-3,-14),
                color=INK, fontsize=10)
ax.annotate(r'$A=\int_a^b f(x)\,dx$', (2.5, 1.6), color=INK, fontsize=11, ha='center')
xd = 3.3; ax.vlines(xd, 0, f(xd), color='#d9534f', lw=1.8, zorder=5)
ax.annotate('thin strip: height $f(x)$,\nwidth $dx$, area $f(x)\\,dx$',
            (xd, f(xd)), textcoords='offset points', xytext=(-118,30),
            color='#a8271f', fontsize=8.4,
            arrowprops=dict(arrowstyle='-|>', color='#a8271f', lw=1.0, mutation_scale=9))
ax.plot(x, f(x), color=ACCENT, lw=2, zorder=4)
ax.annotate('$y=f(x)$', (4.75, f(4.75)), textcoords='offset points', xytext=(-46,6),
            color=ACCENT, fontsize=9.5)
ax.set_xlim(0, 5.1); ax.set_ylim(0, 13)
ax.set_xticks([]); ax.set_yticks([])
ax.spines[['top','right']].set_visible(False)
```

::: caution A definite integral needs a continuous integrand
$\int_{-1}^{1}\frac{dx}{x^{2}}$ is **not** $\left[-\frac1x\right]_{-1}^{1} = -2$.
An area cannot be negative when the integrand $\frac{1}{x^2}$ is positive
everywhere, and the "answer" is meaningless because the integrand blows up at
$x=0$, which lies inside the interval. The fundamental theorem requires $f$ to be
continuous on the whole of $[a,b]$. Before writing down $F(b)-F(a)$, check that the
integrand has no infinity between the limits.
:::

### Properties of the definite integral

| # | Property | Note |
|---|---|---|
| P1 | $\int_{a}^{b}f(x)dx = -\int_{b}^{a}f(x)dx$ | swapping limits changes the sign |
| P2 | $\int_{a}^{a}f(x)dx = 0$ | zero width |
| P3 | $\int_{a}^{b}f(x)dx = \int_{a}^{c}f(x)dx + \int_{c}^{b}f(x)dx$ | split at any $c$ |
| P4 | $\int_{a}^{b}f(x)dx = \int_{a}^{b}f(t)dt$ | the variable is a dummy |
| P5 | $\int_{0}^{a}f(x)dx = \int_{0}^{a}f(a-x)dx$ | reflect in the midpoint |
| P6 | $\int_{a}^{b}f(x)dx = \int_{a}^{b}f(a+b-x)dx$ | general reflection |
| P7 | $\int_{-a}^{a}f(x)dx = 2\int_{0}^{a}f(x)dx$ if $f$ is even | $f(-x)=f(x)$ |
| P8 | $\int_{-a}^{a}f(x)dx = 0$ if $f$ is odd | $f(-x)=-f(x)$ |
| P9 | $\int_{0}^{2a}f(x)dx = \int_{0}^{a}f(x)dx + \int_{0}^{a}f(2a-x)dx$ | split at $a$, then P5 |

::: derivation Proofs of P5 and P7
**P5.** In $\int_0^a f(x)dx$ substitute $x = a-t$, so $dx = -dt$; when $x=0$, $t=a$,
and when $x=a$, $t=0$. Then

$$ \int_{0}^{a}f(x)dx = -\int_{a}^{0}f(a-t)\,dt = \int_{0}^{a}f(a-t)\,dt $$

and renaming the dummy variable $t$ back to $x$ (property P4) gives the result.

**P7 and P8.** Split at $0$ using P3:
$\int_{-a}^{a}f = \int_{-a}^{0}f + \int_{0}^{a}f$. In the first piece put $x = -t$,
$dx = -dt$, which turns it into $\int_{0}^{a}f(-t)\,dt$. So

$$ \int_{-a}^{a}f(x)dx = \int_{0}^{a}\left[f(-x)+f(x)\right]dx $$

If $f$ is even, $f(-x)=f(x)$ and the bracket is $2f(x)$, giving P7. If $f$ is odd,
$f(-x)=-f(x)$ and the bracket is zero, giving P8.
:::

::: example Worked example 19.26
**Problem.** Evaluate $\int_{0}^{\pi/2}\sin^{2}x\,dx$.

**Solution.** Powers of sine and cosine are always reduced with the double-angle
identity before integrating; $\sin^2 x$ is not a standard form but $\cos 2x$ is.
Using $\sin^{2}x = \frac{1-\cos 2x}{2}$,

$$ \int_{0}^{\pi/2}\frac{1-\cos 2x}{2}dx
 = \frac{1}{2}\left[x - \frac{\sin 2x}{2}\right]_{0}^{\pi/2} $$

$$ = \frac{1}{2}\left[\left(\frac{\pi}{2}-\frac{\sin\pi}{2}\right)-(0-0)\right]
 = \frac{\pi}{4} $$
:::

::: example Worked example 19.27
**Problem.** Evaluate (a) $\int_{0}^{1}xe^{x}dx$  (b) $\int_{1}^{e}\ln x\,dx$.

**Solution.** In a definite integral by parts, evaluate the $uv$ term at the limits
as you go: $\int_{a}^{b}u\,dv = \left[uv\right]_{a}^{b} - \int_{a}^{b}v\,du$.

(a) With $u = x$, $dv = e^{x}dx$:

$$ \int_{0}^{1}xe^{x}dx = \left[xe^{x}\right]_{0}^{1} - \int_{0}^{1}e^{x}dx
 = e - \left[e^{x}\right]_{0}^{1} = e - (e-1) = 1 $$

(b) With $u = \ln x$, $dv = dx$:

$$ \int_{1}^{e}\ln x\,dx = \left[x\ln x\right]_{1}^{e} - \int_{1}^{e}dx
 = (e\cdot 1 - 0) - (e-1) = 1 $$
:::

::: tip Spotting a P5/P6 question
If a definite integral over $[0,\frac{\pi}{2}]$ has $\sin$ and $\cos$ appearing
symmetrically, apply P5 with $a = \frac{\pi}{2}$ (which turns $\sin x$ into $\cos x$),
add the two versions, and the messy part cancels. The answer is usually
$\frac{\pi}{4}$.
:::

::: example Worked example 19.28
**Problem.** Evaluate $\int_{1}^{2}\left(x^{2}+\frac{1}{x^{2}}\right)dx$.

**Solution.**

$$ \int_{1}^{2}\left(x^{2}+x^{-2}\right)dx = \left[\frac{x^{3}}{3}-\frac{1}{x}\right]_{1}^{2} $$

$$ = \left(\frac{8}{3}-\frac{1}{2}\right)-\left(\frac{1}{3}-1\right)
 = \frac{13}{6} + \frac{2}{3} = \frac{17}{6} $$
:::

::: example Worked example 19.29 — substitution with limits
**Problem.** Evaluate $\int_{0}^{1}\frac{x\,dx}{x^{2}+1}$.

**Solution.** Put $u = x^{2}+1$, $du = 2x\,dx$. **Change the limits too:** when
$x=0$, $u=1$; when $x=1$, $u=2$.

$$ \int_{0}^{1}\frac{x\,dx}{x^{2}+1} = \frac{1}{2}\int_{1}^{2}\frac{du}{u}
 = \frac{1}{2}\left[\ln u\right]_{1}^{2} = \frac{1}{2}(\ln 2 - \ln 1) = \frac{1}{2}\ln 2 $$
:::

::: caution Changing the variable but not the limits
This is the single most common error in Group B. Either change the limits with the
variable (as above), or integrate back to $x$ first and then apply the original
limits. Never mix: $\frac12[\ln(x^2+1)]_1^2$ is wrong.
:::

::: example Worked example 19.30 — using a property
**Problem.** Evaluate $I = \int_{0}^{\pi/2}\frac{dx}{1+\tan x}$.

**Solution.** Write the integrand in terms of sine and cosine:

$$ I = \int_{0}^{\pi/2}\frac{\cos x}{\cos x + \sin x}\,dx $$

By P5 with $a = \frac{\pi}{2}$, replacing $x$ by $\frac{\pi}{2}-x$ turns $\cos x$
into $\sin x$ and $\sin x$ into $\cos x$:

$$ I = \int_{0}^{\pi/2}\frac{\sin x}{\sin x + \cos x}\,dx $$

Adding the two expressions for $I$,

$$ 2I = \int_{0}^{\pi/2}\frac{\cos x + \sin x}{\cos x + \sin x}\,dx
 = \int_{0}^{\pi/2}dx = \frac{\pi}{2} \;\Longrightarrow\; I = \frac{\pi}{4} $$
:::

::: example Worked example 19.31 — odd and even
**Problem.** Evaluate $\int_{-2}^{2}(x^{3}+x)\,dx$ and $\int_{-2}^{2}(x^{2}+1)\,dx$.

**Solution.** For the first, $f(-x) = -x^{3}-x = -f(x)$, so $f$ is **odd** and by P8
the integral is $0$ — the area below the axis on $[-2,0]$ exactly cancels the area
above it on $[0,2]$.

For the second, $f(-x) = x^{2}+1 = f(x)$, so $f$ is **even** and by P7

$$ \int_{-2}^{2}(x^{2}+1)dx = 2\int_{0}^{2}(x^{2}+1)dx
 = 2\left[\frac{x^{3}}{3}+x\right]_{0}^{2} = 2\left(\frac{8}{3}+2\right) = \frac{28}{3} $$
:::

## 19.5 Area under a curve; area between two curves

### Signed area and true area

The definite integral counts area **below** the $x$-axis as negative. That is exactly
what you want for a displacement, and exactly what you do *not* want when a question
asks for "the area of the region".

```figure caption="Signed area. On $[0,2]$ the curve $y=x^3-4x$ lies below the axis and contributes $-4$; on $[2,3]$ it lies above and contributes $+6.25$. The definite integral over $[0,3]$ is $2.25$, but the total area of the region is $10.25$ square units."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6,2.9))
f = lambda t: t**3 - 4*t
x = np.linspace(-0.25, 3.1, 400)
ax.plot(x, f(x), color=INK, lw=1.9, zorder=4)
x1 = np.linspace(0, 2, 200); x2 = np.linspace(2, 3, 200)
ax.fill_between(x1, 0, f(x1), color='#d9534f', alpha=0.30)
ax.fill_between(x2, 0, f(x2), color=ACCENT, alpha=0.30)
ax.axhline(0, color=MUTED, lw=1.0)
ax.annotate('below axis\n$\\int_0^2 = -4$', (1.1,-1.7), color='#a8271f',
            fontsize=8.6, ha='center')
ax.annotate('above axis\n$\\int_2^3 = +6.25$', (2.68,4.6), textcoords='offset points',
            xytext=(-86,44), color='#155a8a', fontsize=8.6, ha='center',
            arrowprops=dict(arrowstyle='-|>', color='#155a8a', lw=1.0, mutation_scale=9))
for p in (0,2,3):
    ax.plot([p],[0],'o',color=INK,ms=3.5,zorder=5)
    ax.annotate(f'${p}$',(p,0),textcoords='offset points',xytext=(-3,5 if p==2 else -13),
                color=INK,fontsize=9)
ax.set_xlim(-0.3,3.2); ax.set_ylim(-4.2,16)
ax.set_xlabel('$x$'); ax.set_ylabel('$y = x^3-4x$')
ax.set_yticks([-3,0,5,10,15])
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.35)
```

::: key Rule for areas
1. Find where the curve crosses the $x$-axis inside the interval.
2. Integrate **separately** over each piece.
3. Take the **modulus** of each piece, then add.

$$ \text{Area} = \int_{a}^{c}|f(x)|\,dx + \int_{c}^{b}|f(x)|\,dx $$
:::

### Area with respect to the $x$-axis

The area bounded by $y = f(x)$, the $x$-axis and the ordinates $x=a$, $x=b$ is

$$ A = \int_{a}^{b}y\,dx = \int_{a}^{b}f(x)\,dx \qquad (f \ge 0 \text{ on } [a,b]) $$

```figure caption="The region bounded by $y = 4-x^2$ and the two axes in the first quadrant. Its area is $\int_0^2 (4-x^2)\,dx = 16/3$ square units."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.2,2.8))
x = np.linspace(-0.6, 2.5, 400)
ax.plot(x, 4-x**2, color=ACCENT, lw=2, zorder=4)
xs = np.linspace(0, 2, 200)
ax.fill_between(xs, 0, 4-xs**2, color=ACCENT, alpha=0.20)
ax.axhline(0, color=MUTED, lw=0.9); ax.axvline(0, color=MUTED, lw=0.9)
ax.annotate('$A=\\int_0^2(4-x^2)\\,dx=\\frac{16}{3}$', (1.05,1.15), color=INK,
            fontsize=9, ha='center')
ax.plot([0,2],[4,0],'o',color=INK,ms=4,zorder=6)
ax.annotate('$(0,4)$',(0,4),textcoords='offset points',xytext=(7,2),color=INK,fontsize=9)
ax.annotate('$(2,0)$',(2,0),textcoords='offset points',xytext=(2,7),color=INK,fontsize=9)
ax.set_xlim(-0.7,2.6); ax.set_ylim(-1.2,5.0)
ax.set_xlabel('$x$'); ax.set_ylabel('$y$')
ax.set_xticks([0,1,2]); ax.set_yticks([0,2,4])
ax.spines[['top','right']].set_visible(False)
```

::: example Worked example 19.32
**Problem.** Find the area bounded by the parabola $y = 4x - x^{2}$ and the
$x$-axis.

**Solution.** The curve meets the axis where $4x - x^{2} = 0$, i.e. $x(4-x)=0$, so
at $x = 0$ and $x = 4$. Between these the parabola is above the axis, so

$$ A = \int_{0}^{4}(4x-x^{2})dx = \left[2x^{2}-\frac{x^{3}}{3}\right]_{0}^{4}
 = 32 - \frac{64}{3} = \frac{32}{3} \ \text{square units} $$
:::

::: example Worked example 19.33 — remembering the modulus
**Problem.** Find the area enclosed between the curve $y = x^{3}-4x$, the $x$-axis
and the lines $x = 0$ and $x = 3$.

**Solution.** The curve cuts the axis where $x(x^{2}-4)=0$, i.e. at $x = 0$ and
$x = 2$ inside the interval. Split there.

$$ \int_{0}^{2}(x^{3}-4x)dx = \left[\frac{x^{4}}{4}-2x^{2}\right]_{0}^{2} = 4-8 = -4 $$

$$ \int_{2}^{3}(x^{3}-4x)dx = \left[\frac{x^{4}}{4}-2x^{2}\right]_{2}^{3}
 = \left(\frac{81}{4}-18\right) - (4-8) = \frac{9}{4}+4 = \frac{25}{4} $$

Total area $= |-4| + \frac{25}{4} = 4 + 6.25 = 10.25$ square units. (The definite
integral $\int_0^3$ would give only $2.25$ — a different question with a different
answer.)
:::

### Area with respect to the $y$-axis

When the region is bounded by the $y$-axis and horizontal lines, use horizontal
strips of length $x$ and width $dy$:

$$ A = \int_{c}^{d}x\,dy $$

```figure caption="Horizontal strips. The region bounded by $x=y^2$, the $y$-axis and $y=1$, $y=3$ has area $\int_1^3 y^2\,dy = 26/3$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.2,3.0))
y = np.linspace(0, 3.35, 300)
ys = np.linspace(1, 3, 200)
ax.fill_betweenx(ys, 0, ys**2, color=ACCENT, alpha=0.18)
for yy in np.linspace(1.12, 2.9, 7):
    ax.plot([0, yy**2],[yy,yy], color=ACCENT, lw=0.7, alpha=0.5)
ax.plot(y**2, y, color=ACCENT, lw=2, zorder=4)
ax.axhline(0, color=MUTED, lw=0.9); ax.axvline(0, color=MUTED, lw=0.9)
for yy,lab in [(1,'$y=1$'),(3,'$y=3$')]:
    ax.hlines(yy, 0, yy**2, color=INK, lw=1.0, ls=':')
    ax.annotate(lab,(yy**2,yy),textcoords='offset points',xytext=(6,-3),
                color=INK,fontsize=9)
ax.annotate('$x=y^2$',(3.3**2,3.3),textcoords='offset points',xytext=(-52,2),
            color=ACCENT,fontsize=9.5)
ax.annotate('strip: length $x=y^2$,\nwidth $dy$',(6.2,1.35),color=INK,fontsize=8.2,
            ha='center')
ax.annotate('$A=\\int_1^3 y^2\\,dy=\\frac{26}{3}$',(6.2,0.35),color=INK,fontsize=9.5,ha='center')
ax.set_xlim(-0.8,12.6); ax.set_ylim(-0.35,3.6)
ax.set_xlabel('$x$'); ax.set_ylabel('$y$')
ax.set_yticks([0,1,2,3]); ax.set_xticks([0,3,6,9])
ax.spines[['top','right']].set_visible(False)
```

::: example Worked example 19.34
**Problem.** Find the area of the region bounded by the curve $x = y^{2}$, the
$y$-axis and the lines $y = 1$ and $y = 3$.

**Solution.** Horizontal strips run from the $y$-axis ($x=0$) out to $x = y^{2}$, so

$$ A = \int_{1}^{3}x\,dy = \int_{1}^{3}y^{2}dy = \left[\frac{y^{3}}{3}\right]_{1}^{3}
 = 9 - \frac{1}{3} = \frac{26}{3} \ \text{square units} $$
:::

### Area between two curves

If $y = f(x)$ lies above $y = g(x)$ on $[a,b]$, a vertical strip has height
$f(x)-g(x)$, so

$$ A = \int_{a}^{b}\left[f(x)-g(x)\right]dx $$

The limits $a$ and $b$ are the $x$-coordinates of the points of intersection, found
by solving $f(x) = g(x)$.

This formula does not care where the $x$-axis is. Even if part of the region lies
below the axis, the height of a strip is still (top curve) minus (bottom curve), and
the negative parts cancel correctly on their own. That is why you do **not** split
an "area between two curves" question at the $x$-axis — you split it only where the
two curves cross each other, because that is where "top" and "bottom" swap over.

```figure caption="Area between $y = 4-x^2$ and $y = x+2$. The curves meet at $(-2,0)$ and $(1,3)$, and the shaded area is $9/2$ square units."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.4,2.9))
x = np.linspace(-3.0, 2.4, 400)
ax.plot(x, 4-x**2, color=ACCENT, lw=2, zorder=4, label='$y=4-x^2$')
ax.plot(x, x+2, color='#d9534f', lw=2, zorder=4, label='$y=x+2$')
xs = np.linspace(-2, 1, 200)
ax.fill_between(xs, xs+2, 4-xs**2, color='#2e8b57', alpha=0.22, zorder=1)
for p in (-2.0, 1.0):
    ax.plot([p],[p+2],'o',color=INK,ms=4.5,zorder=6)
ax.annotate('$(-2,0)$',(-2,0),textcoords='offset points',xytext=(-54,14),color=INK,fontsize=8.8)
ax.annotate('$(1,3)$',(1,3),textcoords='offset points',xytext=(6,0),color=INK,fontsize=8.8)
xd=-0.5
ax.vlines(xd, xd+2, 4-xd**2, color=INK, lw=1.4)
ax.annotate('$(y_{top}-y_{bot})\\,dx$',(xd,xd+2),xytext=(-0.15,0.62),
            color=INK,fontsize=8.4,ha='center',
            arrowprops=dict(arrowstyle='-|>',color=INK,lw=0.9,mutation_scale=9))
ax.annotate('$A=\\frac{9}{2}$',(0.33,2.95),color='#1b5e3a',fontsize=10.5,ha='center')
ax.axhline(0, color=MUTED, lw=0.8)
ax.set_xlim(-3.1,2.5); ax.set_ylim(-3.0,5.0)
ax.set_xlabel('$x$'); ax.set_ylabel('$y$')
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.35)
ax.legend(loc='lower left', fontsize=8.4)
```

::: example Worked example 19.35
**Problem.** Find the area enclosed between the parabola $y = 4-x^{2}$ and the line
$y = x+2$.

**Solution.** The curves meet where $4-x^{2} = x+2$, i.e. $x^{2}+x-2 = 0$, i.e.
$(x+2)(x-1)=0$, so $x = -2$ and $x = 1$. Between these the parabola is the upper
curve, so

$$ A = \int_{-2}^{1}\left[(4-x^{2})-(x+2)\right]dx = \int_{-2}^{1}(2-x-x^{2})dx $$

$$ = \left[2x - \frac{x^{2}}{2} - \frac{x^{3}}{3}\right]_{-2}^{1}
 = \left(2-\frac12-\frac13\right) - \left(-4-2+\frac83\right) = \frac{7}{6} + \frac{10}{3}
 = \frac{9}{2} \ \text{square units} $$
:::

::: example Worked example 19.36
**Problem.** Find the area of the region bounded by the parabola $y^{2} = 4x$ and
the line $y = x$.

**Solution.** Solving $y^2 = 4x$ with $y = x$ gives $x^{2} = 4x$, so $x = 0$ or
$x = 4$. For $0 \le x \le 4$ the parabola $y = 2\sqrt{x}$ lies above the line, so

$$ A = \int_{0}^{4}\left(2\sqrt{x} - x\right)dx
 = \left[\frac{4}{3}x^{3/2} - \frac{x^{2}}{2}\right]_{0}^{4}
 = \frac{32}{3} - 8 = \frac{8}{3} \ \text{square units} $$
:::

::: example Worked example 19.37
**Problem.** Find the area of the region in the first quadrant bounded by the circle
$x^{2}+y^{2} = 9$ and the two axes, and hence state the area of the whole circle.

**Solution.** In the first quadrant $y = \sqrt{9-x^{2}}$, and the region runs from
$x=0$ to $x=3$:

$$ A = \int_{0}^{3}\sqrt{9-x^{2}}\,dx
 = \left[\frac{x}{2}\sqrt{9-x^{2}} + \frac{9}{2}\sin^{-1}\frac{x}{3}\right]_{0}^{3} $$

using entry 22 of the table with $a=3$. At $x=3$ the first term vanishes and
$\sin^{-1}1 = \frac{\pi}{2}$; at $x=0$ both terms vanish. So

$$ A = \frac{9}{2}\cdot\frac{\pi}{2} = \frac{9\pi}{4} \ \text{square units} $$

By symmetry the whole circle has area $4 \times \frac{9\pi}{4} = 9\pi$, which agrees
with $\pi r^{2}$ for $r = 3$. That agreement is a useful check on the method.
:::

::: example Worked example 19.38
**Problem.** Find the area enclosed between the curve $y = \sin x$ and the $x$-axis
from $x = 0$ to $x = 2\pi$.

**Solution.** The sine curve is above the axis on $[0,\pi]$ and below it on
$[\pi,2\pi]$, so the two pieces must be handled separately.

$$ \int_{0}^{\pi}\sin x\,dx = \left[-\cos x\right]_{0}^{\pi} = 1-(-1) = 2 $$

$$ \int_{\pi}^{2\pi}\sin x\,dx = \left[-\cos x\right]_{\pi}^{2\pi} = -1-1 = -2 $$

Total area $= |2| + |-2| = 4$ square units, although
$\int_{0}^{2\pi}\sin x\,dx = 0$. The integral being zero says the positive and
negative signed areas balance; it does not say there is no region.
:::

### Where areas are used

The area idea is the reason integration appears everywhere outside mathematics. If a
graph plots a *rate* against time, the area under it is the *total*: the area under
a velocity-time graph is the distance travelled, the area under a force-displacement
graph is the work done, the area under a current-time graph is the charge that has
flowed, and the area under a discharge-time graph for a river such as the Bagmati is
the total volume of water carried. In each case the units of the area are (units of
the $y$-axis) $\times$ (units of the $x$-axis), which is a quick way to check that
you have set up the right integral.

::: tip Which is "top"?
Substitute a single convenient $x$ strictly between the two intersection points into
both functions; the larger value is the top curve. One test point settles it —
never guess from a rough sketch alone.
:::

::: tip Always sketch first
An area question without a sketch is a guess. The sketch tells you three things the
algebra alone will not: which curve is on top, where the region actually closes up,
and whether the curve crosses the $x$-axis inside the interval so that the integral
must be split. A rough sketch showing the intercepts, the general shape and the
shaded region takes thirty seconds and is usually worth a mark of its own in
Group C. If the two curves cross *between* the stated limits, the upper curve
changes partway across, and you must split the integral at the crossing point and
add the moduli of the pieces — exactly as you do when a single curve crosses the
axis.
:::

## Chapter summary

- $\int f(x)dx = F(x)+C$ means $F'(x)=f(x)$. The constant $C$ is compulsory in an
  indefinite integral and cancels in a definite one.
- Integration is linear: constants come out, sums split. There is no product or
  quotient rule.
- Standard forms to know cold: $\int x^n dx = \frac{x^{n+1}}{n+1}$ $(n\neq-1)$,
  $\int\frac{dx}{x}=\ln|x|$, $\int\frac{dx}{a^2+x^2}=\frac1a\tan^{-1}\frac{x}{a}$,
  $\int\frac{dx}{\sqrt{a^2-x^2}}=\sin^{-1}\frac{x}{a}$,
  $\int\frac{dx}{x^2-a^2}=\frac{1}{2a}\ln\frac{|x-a|}{|x+a|}$.
- Substitution: $u=g(x)$, $du=g'(x)dx$. Two workhorses:
  $\int\frac{f'}{f}dx=\ln|f|+C$ and $\int f^n f'dx = \frac{f^{n+1}}{n+1}+C$.
  Surds $\sqrt{a^2-x^2}$, $\sqrt{a^2+x^2}$, $\sqrt{x^2-a^2}$ call for
  $x=a\sin\theta$, $a\tan\theta$, $a\sec\theta$.
- Quadratic denominators: complete the square; for $\frac{px+q}{ax^2+bx+c}$ write
  $px+q=\lambda(2ax+b)+\mu$. Rational functions: divide if improper, then split into
  partial fractions by the four denominator cases.
- By parts: $\int u\,dv = uv - \int v\,du$, choosing $u$ by **ILATE**. Apply twice
  for $x^2$ factors; for $\int e^{ax}\sin bx\,dx$ apply twice and solve for $I$.
- $\int_a^b f(x)dx = \lim_{n\to\infty}h\sum_{r=1}^{n}f(a+rh)$ with $h=\frac{b-a}{n}$,
  and equals $F(b)-F(a)$ by the fundamental theorem. Change the limits whenever you
  change the variable.
- Useful properties: $\int_0^a f(x)dx=\int_0^a f(a-x)dx$;
  $\int_{-a}^{a}f=2\int_0^a f$ for even $f$ and $0$ for odd $f$.
- Area under a curve is $\int_a^b y\,dx$ (or $\int_c^d x\,dy$ for horizontal
  strips); area between curves is $\int_a^b (y_{top}-y_{bot})dx$. Split at every
  crossing of the axis and take moduli before adding.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. $\int \frac{dx}{x}$ equals <span class="marks">[1]</span>
   (a) $-x^{-2}+C$ (b) $\ln|x|+C$ (c) $\frac{x^{0}}{0}+C$ (d) $x\ln x+C$
2. $\int_{0}^{\pi/2}\cos x\,dx$ equals <span class="marks">[1]</span>
   (a) $0$ (b) $\frac{1}{2}$ (c) $1$ (d) $\frac{\pi}{2}$
3. $\int \frac{dx}{4+x^{2}}$ equals <span class="marks">[1]</span>
   (a) $\tan^{-1}\frac{x}{2}+C$ (b) $\frac{1}{2}\tan^{-1}\frac{x}{2}+C$ (c) $\frac{1}{4}\tan^{-1}\frac{x}{4}+C$ (d) $\ln(4+x^{2})+C$
4. The area bounded by $y = x^{2}$, the $x$-axis and $x = 3$ is <span class="marks">[1]</span>
   (a) $3$ (b) $6$ (c) $9$ (d) $27$
5. $\int e^{x}(\sin x + \cos x)\,dx$ equals <span class="marks">[1]</span>
   (a) $e^{x}\cos x+C$ (b) $e^{x}\sin x+C$ (c) $e^{x}(\sin x-\cos x)+C$ (d) $2e^{x}\sin x+C$
6. $\int_{-1}^{1} x^{3}\,dx$ equals <span class="marks">[1]</span>
   (a) $\frac{1}{2}$ (b) $\frac{1}{4}$ (c) $2$ (d) $0$
7. In $\int x\ln x\,dx$, ILATE says $u$ should be <span class="marks">[1]</span>
   (a) $x$ (b) $\ln x$ (c) either (d) $x\ln x$
8. $\int \frac{2x}{x^{2}+5}\,dx$ equals <span class="marks">[1]</span>
   (a) $\ln(x^{2}+5)+C$ (b) $\frac{1}{2}\ln(x^{2}+5)+C$ (c) $2\tan^{-1}\frac{x}{5}+C$ (d) $\frac{x^{2}}{x^{2}+5}+C$
9. The value of $\int_{2}^{2}(x^{5}+7x)\,dx$ is <span class="marks">[1]</span>
   (a) $1$ (b) $0$ (c) $36$ (d) undefined
10. $\int \frac{dx}{\sqrt{9-x^{2}}}$ equals <span class="marks">[1]</span>
   (a) $\sin^{-1}\frac{x}{9}+C$ (b) $\frac{1}{3}\sin^{-1}\frac{x}{3}+C$ (c) $\sin^{-1}\frac{x}{3}+C$ (d) $\ln|x+\sqrt{9-x^{2}}|+C$
11. The area between $y = f(x)$ and $y = g(x)$ from $x=a$ to $x=b$, where $f \ge g$ throughout, is <span class="marks">[1]</span>
   (a) $\int_a^b [f(x)+g(x)]dx$ (b) $\int_a^b [f(x)-g(x)]dx$ (c) $\int_a^b f(x)g(x)dx$ (d) $\int_a^b \frac{f(x)}{g(x)}dx$

::: note Answers to Group A
**1.** (b) — rule 1 fails for $n=-1$; the derivative of $\ln|x|$ is $1/x$.

**2.** (c) — $[\sin x]_0^{\pi/2} = 1-0 = 1$.

**3.** (b) — form 16 with $a=2$ gives the factor $\frac1a = \frac12$.

**4.** (c) — $\int_0^3 x^2dx = [x^3/3]_0^3 = 9$.

**5.** (b) — form 27 with $f(x)=\sin x$, since $f'(x)=\cos x$.

**6.** (d) — $x^3$ is odd and the limits are symmetric, so by P8 the value is $0$.

**7.** (b) — L comes before A in ILATE.

**8.** (a) — the numerator is exactly the derivative of the denominator, so form 25
applies with no extra factor.

**9.** (b) — the limits are equal, so by P2 the integral is zero whatever the
integrand.

**10.** (c) — form 15 with $a=3$; there is no $\frac1a$ factor in the inverse sine
form.

**11.** (b) — a vertical strip has height (top curve) minus (bottom curve).
:::

**Group B — Short answer (5 marks each)**

1. Evaluate $\int \frac{x+1}{(x+2)(x+3)}\,dx$. <span class="marks">[5]</span>
2. Evaluate $\int x\cos x\,dx$ and state which factor you took as $u$ and why. <span class="marks">[5]</span>
3. Evaluate $\int \frac{dx}{x^{2}+6x+13}$. <span class="marks">[5]</span>
4. Show that $\int_{0}^{\pi/2}\frac{\sin x}{\sin x + \cos x}\,dx = \frac{\pi}{4}$. <span class="marks">[5]</span>
5. Find the area bounded by the curve $y = x^{2}$, the $x$-axis and the lines $x=1$ and $x=3$. <span class="marks">[5]</span>
6. Evaluate $\int e^{2x}\cos x\,dx$. <span class="marks">[5]</span>
7. Evaluate $\int \sqrt{4-x^{2}}\,dx$ using a trigonometric substitution. <span class="marks">[5]</span>
8. Evaluate $\int \sin^{-1}x\,dx$. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Put $\frac{x+1}{(x+2)(x+3)} = \frac{A}{x+2}+\frac{B}{x+3}$, so
$x+1 = A(x+3)+B(x+2)$. At $x=-2$: $-1 = A$. At $x=-3$: $-2 = -B$, so $B = 2$.
Hence the integral is
$$ \int\left(\frac{-1}{x+2}+\frac{2}{x+3}\right)dx = -\ln|x+2| + 2\ln|x+3| + C $$

**2.** A (algebraic) comes before T (trigonometric) in ILATE, so $u = x$ and
$dv = \cos x\,dx$, giving $du = dx$ and $v = \sin x$:
$$ \int x\cos x\,dx = x\sin x - \int\sin x\,dx = x\sin x + \cos x + C $$
Choosing $u=\cos x$ instead would leave $\int\frac{x^2}{2}\sin x\,dx$, which is worse.

**3.** Complete the square: $x^{2}+6x+13 = (x+3)^{2}+4$. With $u=x+3$ and $a=2$
in form 16,
$$ \int\frac{du}{u^{2}+2^{2}} = \frac{1}{2}\tan^{-1}\frac{u}{2}+C
 = \frac{1}{2}\tan^{-1}\frac{x+3}{2}+C $$

**4.** Let $I = \int_0^{\pi/2}\frac{\sin x}{\sin x+\cos x}dx$. By P5 with
$a=\frac{\pi}{2}$, replacing $x$ by $\frac{\pi}{2}-x$ swaps $\sin$ and $\cos$:
$I = \int_0^{\pi/2}\frac{\cos x}{\cos x+\sin x}dx$. Adding,
$$ 2I = \int_0^{\pi/2}\frac{\sin x+\cos x}{\sin x+\cos x}dx = \int_0^{\pi/2}dx = \frac{\pi}{2} $$
so $I = \frac{\pi}{4}$.

**5.** The curve is above the axis on $[1,3]$, so
$$ A = \int_1^3 x^2dx = \left[\frac{x^3}{3}\right]_1^3 = 9 - \frac13 = \frac{26}{3}
\ \text{square units} $$

**6.** Let $I = \int e^{2x}\cos x\,dx$. Take $u = \cos x$, $dv = e^{2x}dx$, so
$v = \frac{e^{2x}}{2}$:
$$ I = \frac{e^{2x}\cos x}{2} + \frac{1}{2}\int e^{2x}\sin x\,dx $$
Apply parts again to the new integral with $u = \sin x$:
$\int e^{2x}\sin x\,dx = \frac{e^{2x}\sin x}{2} - \frac{1}{2}I$. Substituting,
$$ I = \frac{e^{2x}\cos x}{2} + \frac{e^{2x}\sin x}{4} - \frac{I}{4}
 \;\Longrightarrow\; \frac{5I}{4} = \frac{e^{2x}(2\cos x + \sin x)}{4} $$
so $I = \frac{e^{2x}(2\cos x+\sin x)}{5}+C$.

**7.** Put $x = 2\sin\theta$, $dx = 2\cos\theta\,d\theta$, $\sqrt{4-x^2}=2\cos\theta$:
$$ \int 4\cos^{2}\theta\,d\theta = 2\int(1+\cos2\theta)d\theta
 = 2\theta + \sin2\theta + C = 2\theta + 2\sin\theta\cos\theta + C $$
Since $\sin\theta = \frac{x}{2}$ and $\cos\theta = \frac{\sqrt{4-x^{2}}}{2}$,
$$ \int\sqrt{4-x^{2}}\,dx = 2\sin^{-1}\frac{x}{2} + \frac{x}{2}\sqrt{4-x^{2}} + C $$

**8.** There is only one factor, so supply a second factor of $1$. By ILATE the
inverse trigonometric function is $u$: take $u = \sin^{-1}x$ and $dv = dx$, so
$du = \frac{dx}{\sqrt{1-x^{2}}}$ and $v = x$:
$$ \int\sin^{-1}x\,dx = x\sin^{-1}x - \int\frac{x\,dx}{\sqrt{1-x^{2}}} $$
For the remaining integral put $t = 1-x^{2}$, $dt = -2x\,dx$:
$$ \int\frac{x\,dx}{\sqrt{1-x^{2}}} = -\frac{1}{2}\int t^{-1/2}dt = -\sqrt{t}
 = -\sqrt{1-x^{2}} $$
Hence $\int\sin^{-1}x\,dx = x\sin^{-1}x + \sqrt{1-x^{2}} + C$.
:::

**Group C — Long answer (8 marks each)**

1. (a) Derive the formula for integration by parts from the product rule. <span class="marks">[3]</span>
   (b) Hence evaluate $\int x^{2}\ln x\,dx$. <span class="marks">[5]</span>
2. Evaluate $\int\frac{2x+1}{(x-1)(x^{2}+1)}\,dx$ by partial fractions, stating the
   form of the decomposition and justifying it. <span class="marks">[8]</span>
3. (a) Evaluate $\int_{1}^{3}(x^{2}+1)\,dx$ from first principles, as the limit of a
   sum. <span class="marks">[5]</span>
   (b) Verify your answer using the fundamental theorem of calculus. <span class="marks">[3]</span>
4. Find the area of the region enclosed by the parabola $y^{2}=4x$ and the line
   $y = 2x-4$. <span class="marks">[8]</span>
5. (a) Evaluate $\int_{0}^{\pi/2}x\sin x\,dx$. <span class="marks">[4]</span>
   (b) Find the area of the region bounded by the curve $y = 2x - x^{2}$ and the
   $x$-axis. <span class="marks">[4]</span>

::: note Answers to Group C
**1. (a)** From the product rule, $\frac{d}{dx}(uv) = u\frac{dv}{dx}+v\frac{du}{dx}$.
Integrating both sides with respect to $x$ gives
$uv = \int u\frac{dv}{dx}dx + \int v\frac{du}{dx}dx$, and rearranging,
$$ \int u\,\frac{dv}{dx}\,dx = uv - \int v\,\frac{du}{dx}\,dx $$

**(b)** By ILATE take $u = \ln x$ and $dv = x^{2}dx$, so $du = \frac{dx}{x}$ and
$v = \frac{x^{3}}{3}$:
$$ \int x^{2}\ln x\,dx = \frac{x^{3}}{3}\ln x - \int\frac{x^{3}}{3}\cdot\frac{dx}{x}
 = \frac{x^{3}}{3}\ln x - \frac{1}{3}\int x^{2}dx $$
$$ = \frac{x^{3}}{3}\ln x - \frac{x^{3}}{9} + C $$

**2.** The denominator has one distinct linear factor and one non-repeated
irreducible quadratic factor, so the decomposition is
$$ \frac{2x+1}{(x-1)(x^{2}+1)} = \frac{A}{x-1} + \frac{Bx+D}{x^{2}+1} $$
(a quadratic factor needs a *linear* numerator, because the numerator must be allowed
one degree less than the factor). Clearing denominators,
$$ 2x+1 = A(x^{2}+1) + (Bx+D)(x-1) $$
At $x=1$: $3 = 2A$, so $A = \frac32$. Coefficient of $x^{2}$: $A+B = 0$, so
$B = -\frac32$. Constant term: $A - D = 1$, so $D = \frac12$. Therefore
$$ I = \frac{3}{2}\int\frac{dx}{x-1} - \frac{3}{2}\int\frac{x\,dx}{x^{2}+1}
 + \frac{1}{2}\int\frac{dx}{x^{2}+1} $$
$$ = \frac{3}{2}\ln|x-1| - \frac{3}{4}\ln(x^{2}+1) + \frac{1}{2}\tan^{-1}x + C $$

**3. (a)** Here $a=1$, $b=3$, $h = \frac{2}{n}$ and $f(x) = x^{2}+1$, so
$f(1+rh) = (1+rh)^{2}+1 = 2 + 2rh + r^{2}h^{2}$ and
$$ \int_1^3 (x^2+1)dx = \lim_{n\to\infty} h\sum_{r=1}^{n}\left(2+2rh+r^{2}h^{2}\right) $$
$$ = \lim_{n\to\infty}\left[2nh + 2h^{2}\cdot\frac{n(n+1)}{2}
 + h^{3}\cdot\frac{n(n+1)(2n+1)}{6}\right] $$
With $h = 2/n$ this is
$$ \lim_{n\to\infty}\left[4 + \frac{4(n+1)}{n} + \frac{8}{6}\cdot\frac{(n+1)(2n+1)}{n^{2}}\right]
 = 4 + 4 + \frac{8}{6}(1)(2) = \frac{32}{3} $$

**(b)** $\int_1^3 (x^2+1)dx = \left[\frac{x^{3}}{3}+x\right]_1^3
= (9+3) - \left(\frac13+1\right) = 12 - \frac43 = \frac{32}{3}$. The two agree.

**4.** Solve the two equations together. From the line, $x = \frac{y+4}{2}$; from
the parabola, $x = \frac{y^{2}}{4}$. Equating,
$$ \frac{y^{2}}{4} = \frac{y+4}{2} \;\Longrightarrow\; y^{2}-2y-8 = 0
\;\Longrightarrow\; (y-4)(y+2) = 0 $$
so $y = -2$ and $y = 4$ (the points $(1,-2)$ and $(4,4)$). Horizontal strips are
easier here, because a vertical strip would change its lower boundary partway across.
For $-2 < y < 4$ the line lies to the right of the parabola, so
$$ A = \int_{-2}^{4}\left(\frac{y+4}{2} - \frac{y^{2}}{4}\right)dy
 = \left[\frac{y^{2}}{4} + 2y - \frac{y^{3}}{12}\right]_{-2}^{4} $$
$$ = \left(4 + 8 - \frac{64}{12}\right) - \left(1 - 4 + \frac{8}{12}\right)
 = \frac{20}{3} - \left(-\frac{7}{3}\right) = 9 \ \text{square units} $$

**5. (a)** By ILATE take $u = x$ and $dv = \sin x\,dx$, so $v = -\cos x$:
$$ \int_{0}^{\pi/2}x\sin x\,dx = \left[-x\cos x\right]_{0}^{\pi/2}
 + \int_{0}^{\pi/2}\cos x\,dx $$
The bracket is zero at both limits, since $\cos\frac{\pi}{2}=0$ and $x=0$ at the
lower limit. So the value is $\left[\sin x\right]_{0}^{\pi/2} = 1$.

**(b)** The curve meets the $x$-axis where $x(2-x)=0$, i.e. at $x=0$ and $x=2$, and
it lies above the axis between them. Hence
$$ A = \int_{0}^{2}(2x-x^{2})dx = \left[x^{2}-\frac{x^{3}}{3}\right]_{0}^{2}
 = 4 - \frac{8}{3} = \frac{4}{3} \ \text{square units} $$
:::
