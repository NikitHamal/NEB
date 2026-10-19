---
subject: Optional Mathematics
grade: 10
unit: 4
title: Trigonometry: Multiple, Submultiple and Transformation Formulas
hours: 0
area: Units
---

In Grade 9 you learnt how to find $\sin(A+B)$ and $\cos(A-B)$ from the ratios of $A$ and $B$. Those **compound-angle formulas** are the seed of this whole chapter. Put $B=A$ and you get the ratios of the **double angle** $2A$ and the **triple angle** $3A$ (the *multiple angles*). Put $A$ for $\frac{A}{2}$ and you can go backwards, from $A$ to the **half angle** $\frac{A}{2}$ (a *submultiple angle*). Finally, adding or subtracting two sines or cosines can be turned into a product, and a product into a sum (the **transformation formulas**). With these tools you can find exact values such as $\sin15^\circ$ and $\tan22.5^\circ$ and prove many identities.

::: key What the SEE asks from this chapter
Typical questions: (i) find $\sin2A,\ \cos2A,\ \tan2A$ from one given ratio; (ii) find the ratios of $\theta$ when a ratio of $\frac{\theta}{2}$ is given; (iii) **prove** an identity using $2A$, $3A$, $\frac{A}{2}$ formulas; (iv) express a sum as a product or a product as a sum; (v) find the exact value of a product such as $\cos20^\circ\cos40^\circ\cos80^\circ$. In a proof, work on the **left side** only, show each step, and finish on the right side.
:::

## 4.1 Compound angles: a quick review

For any angles $A$ and $B$:

| | |
|---|---|
| $\sin(A+B)=\sin A\cos B+\cos A\sin B$ | $\sin(A-B)=\sin A\cos B-\cos A\sin B$ |
| $\cos(A+B)=\cos A\cos B-\sin A\sin B$ | $\cos(A-B)=\cos A\cos B+\sin A\sin B$ |
| $\tan(A+B)=\frac{\tan A+\tan B}{1-\tan A\tan B}$ | $\tan(A-B)=\frac{\tan A-\tan B}{1+\tan A\tan B}$ |

Memory aid: the **sine** formula keeps the sign of the angle and **mixes** (sin cos + cos sin); the **cosine** formula **repeats** (cos cos, sin sin) and gives the **opposite** sign.

Standard values:

| Angle | $0^\circ$ | $30^\circ$ | $45^\circ$ | $60^\circ$ | $90^\circ$ |
|---|---|---|---|---|---|
| $\sin$ | $0$ | $\frac{1}{2}$ | $\frac{1}{\sqrt{2}}$ | $\frac{\sqrt{3}}{2}$ | $1$ |
| $\cos$ | $1$ | $\frac{\sqrt{3}}{2}$ | $\frac{1}{\sqrt{2}}$ | $\frac{1}{2}$ | $0$ |
| $\tan$ | $0$ | $\frac{1}{\sqrt{3}}$ | $1$ | $\sqrt{3}$ | not defined |

::: example Exact values from compound angles
**Problem.** Find the exact values of $\sin75^\circ$ and $\tan105^\circ$.

**Solution.** $\sin75^\circ=\sin(45^\circ+30^\circ)=\sin45^\circ\cos30^\circ+\cos45^\circ\sin30^\circ$
$$ =\frac{1}{\sqrt{2}}\cdot\frac{\sqrt{3}}{2}+\frac{1}{\sqrt{2}}\cdot\frac{1}{2}=\frac{\sqrt{3}+1}{2\sqrt{2}}=\frac{\sqrt{6}+\sqrt{2}}{4}. $$

$\tan105^\circ=\tan(60^\circ+45^\circ)=\frac{\sqrt{3}+1}{1-\sqrt{3}\cdot1}=\frac{\sqrt{3}+1}{1-\sqrt{3}}$. Multiply top and bottom by $(1+\sqrt{3})$: $\frac{(\sqrt{3}+1)^2}{1-3}=\frac{4+2\sqrt{3}}{-2}=-(2+\sqrt{3})$.
:::

::: example Ratios of $A+B$ from given ratios
**Problem.** If $\sin A=\frac{3}{5}$ and $\cos B=\frac{5}{13}$ with $A$ and $B$ acute, find $\sin(A+B)$, $\cos(A+B)$ and $\sin(A-B)$.

**Solution.** Using $\sin^2+\cos^2=1$: $\cos A=\sqrt{1-\frac{9}{25}}=\frac{4}{5}$ and $\sin B=\sqrt{1-\frac{25}{169}}=\frac{12}{13}$.

$\sin(A+B)=\frac{3}{5}\cdot\frac{5}{13}+\frac{4}{5}\cdot\frac{12}{13}=\frac{15+48}{65}=\frac{63}{65}$.

$\cos(A+B)=\frac{4}{5}\cdot\frac{5}{13}-\frac{3}{5}\cdot\frac{12}{13}=\frac{20-36}{65}=-\frac{16}{65}$.

$\sin(A-B)=\frac{3}{5}\cdot\frac{5}{13}-\frac{4}{5}\cdot\frac{12}{13}=\frac{15-48}{65}=-\frac{33}{65}$.
:::

::: example Two identities from the compound formulas
**Problem.** Prove that (i) $\sin(A+B)\sin(A-B)=\sin^2A-\sin^2B$; (ii) if $\tan A=\frac{1}{2}$ and $\tan B=\frac{1}{3}$ then $A+B=45^\circ$.

**Solution.** (i) $\sin(A+B)\sin(A-B)=(\sin A\cos B)^2-(\cos A\sin B)^2=\sin^2A(1-\sin^2B)-(1-\sin^2A)\sin^2B$
$=\sin^2A-\sin^2A\sin^2B-\sin^2B+\sin^2A\sin^2B=\sin^2A-\sin^2B$.

(ii) $\tan(A+B)=\frac{\frac{1}{2}+\frac{1}{3}}{1-\frac{1}{2}\cdot\frac{1}{3}}=\frac{\frac{5}{6}}{\frac{5}{6}}=1$. Since $A,B$ are acute, $A+B=45^\circ$.
:::

::: example More compound-angle problems
**Problem.** Prove that (i) $\cos(A+B)\cos(A-B)=\cos^2A-\sin^2B$; (ii) $\tan(45^\circ+A)=\frac{1+\tan A}{1-\tan A}$. Hence find $\tan15^\circ$.

**Solution.** (i) $\cos(A+B)\cos(A-B)=(\cos A\cos B)^2-(\sin A\sin B)^2=\cos^2A(1-\sin^2B)-(1-\cos^2A)\sin^2B=\cos^2A-\sin^2B$.

(ii) $\tan(45^\circ+A)=\frac{\tan45^\circ+\tan A}{1-\tan45^\circ\tan A}=\frac{1+\tan A}{1-\tan A}$.

For $\tan15^\circ=\tan(45^\circ-30^\circ)=\frac{1-\tan30^\circ}{1+\tan30^\circ}=\frac{1-\frac{1}{\sqrt{3}}}{1+\frac{1}{\sqrt{3}}}=\frac{\sqrt{3}-1}{\sqrt{3}+1}=\frac{(\sqrt{3}-1)^2}{2}=2-\sqrt{3}$.
:::

## 4.2 Multiple angles $2A$ and $3A$

A **multiple angle** of $A$ is $2A,\ 3A,\ 4A,\ \ldots$ Putting $B=A$ in the compound formulas gives the double-angle formulas.

::: derivation Double-angle formulas
We start from the compound-angle formulas with $B=A$.

**Step 1 — sine.**
$$ \sin2A=\sin(A+A)=\sin A\cos A+\cos A\sin A=2\sin A\cos A $$

**Step 2 — cosine.**
$$ \cos2A=\cos(A+A)=\cos A\cos A-\sin A\sin A=\cos^2A-\sin^2A $$

**Step 3 — two more forms of $\cos2A$.** Replace $\sin^2A$ by $1-\cos^2A$, or $\cos^2A$ by $1-\sin^2A$:
$$ \cos2A=\cos^2A-(1-\cos^2A)=2\cos^2A-1 $$
$$ \cos2A=(1-\sin^2A)-\sin^2A=1-2\sin^2A $$

**Step 4 — tangent.**
$$ \tan2A=\frac{\tan A+\tan A}{1-\tan A\tan A}=\frac{2\tan A}{1-\tan^2A} $$

**Step 5 — in terms of $t=\tan A$.** Divide $2\sin A\cos A$ by $1=\sin^2A+\cos^2A$, then divide top and bottom by $\cos^2A$:
$$ \sin2A=\frac{2\sin A\cos A}{\sin^2A+\cos^2A}=\frac{2\tan A}{1+\tan^2A},\qquad \cos2A=\frac{\cos^2A-\sin^2A}{\sin^2A+\cos^2A}=\frac{1-\tan^2A}{1+\tan^2A} $$

**What it means.** The double angle can be found from **any one** ratio of $A$. Which form of $\cos2A$ to use depends on what is given: use $1-2\sin^2A$ if $\sin A$ is known, $2\cos^2A-1$ if $\cos A$ is known.
:::

::: key Double-angle formulas
$$ \sin2A=2\sin A\cos A=\frac{2\tan A}{1+\tan^2A} $$
$$ \cos2A=\cos^2A-\sin^2A=2\cos^2A-1=1-2\sin^2A=\frac{1-\tan^2A}{1+\tan^2A} $$
$$ \tan2A=\frac{2\tan A}{1-\tan^2A} $$
Also: $1+\cos2A=2\cos^2A$ and $1-\cos2A=2\sin^2A$.
:::

```figure caption="If $\sin A=\frac{3}{5}$, the point $P$ on a circle of radius 25 is $(20,15)$. Doubling the angle moves the point to $Q=(7,24)$, so $\sin2A=\frac{24}{25}$ and $\cos2A=\frac{7}{25}$."
from matplotlib.patches import Arc
fig, ax = plt.subplots(figsize=(4.4, 3.7))
R = 25
t = np.linspace(0, np.pi/2, 100)
ax.plot(R*np.cos(t), R*np.sin(t), color=MUTED, lw=0.9)
P = (20, 15); Q = (7, 24)
for pt, c in [(P, ACCENT), (Q, SERIES[1])]:
    ax.plot([0, pt[0]], [0, pt[1]], color=c, lw=1.6)
    ax.plot([pt[0], pt[0]], [0, pt[1]], color=c, lw=1.0, ls='--')
ax.plot([0, 26], [0, 0], color=INK, lw=0.9)
ax.add_patch(Arc((0, 0), 10, 10, theta1=0, theta2=36.87, color=ACCENT, lw=1))
ax.add_patch(Arc((0, 0), 16, 16, theta1=0, theta2=73.74, color=SERIES[1], lw=1))
ax.text(5.6, 1.0, 'A', color=ACCENT, fontsize=8.5)
ax.text(2.2, 4.6, '2A', color=SERIES[1], fontsize=8.5)
ax.text(21.0, 15.4, 'P (20, 15)', color=ACCENT, fontsize=8)
ax.text(7.8, 24.6, 'Q (7, 24)', color=SERIES[1], fontsize=8)
ax.text(2.4, 14.5, '25', color=SERIES[1], fontsize=8, ha='right')
ax.text(20.5, 7, '15', color=ACCENT, fontsize=8, ha='left')
ax.text(7.6, 17, '24', color=SERIES[1], fontsize=8, ha='left')
ax.text(7, -2.4, '7', color=SERIES[1], fontsize=8, ha='center')
ax.text(20, -2.4, '20', color=ACCENT, fontsize=8, ha='center')
ax.set_xlim(-3, 28); ax.set_ylim(-4, 28); ax.set_aspect('equal'); ax.axis('off')
fig.tight_layout(pad=0.3)
```

::: example Ratios of $2A$ from a given ratio
**Problem.** If $\sin A=\frac{3}{5}$ and $A$ is acute, find $\sin2A$, $\cos2A$ and $\tan2A$.

**Solution.** $\cos A=\sqrt{1-\frac{9}{25}}=\frac{4}{5}$.

$\sin2A=2\sin A\cos A=2\cdot\frac{3}{5}\cdot\frac{4}{5}=\frac{24}{25}$.

$\cos2A=1-2\sin^2A=1-2\cdot\frac{9}{25}=\frac{7}{25}$.

$\tan2A=\frac{\sin2A}{\cos2A}=\frac{24}{7}$.
:::

::: example $\tan 2A$ and $\cos2\theta$ from a tangent
**Problem.** (i) If $\tan A=\frac{3}{4}$, find $\tan2A$. (ii) If $\tan\theta=\frac{1}{3}$, find $\cos2\theta$.

**Solution.** (i) $\tan2A=\frac{2\cdot\frac{3}{4}}{1-\frac{9}{16}}=\frac{\frac{3}{2}}{\frac{7}{16}}=\frac{3}{2}\cdot\frac{16}{7}=\frac{24}{7}$.

(ii) $\cos2\theta=\frac{1-\tan^2\theta}{1+\tan^2\theta}=\frac{1-\frac{1}{9}}{1+\frac{1}{9}}=\frac{\frac{8}{9}}{\frac{10}{9}}=\frac{4}{5}$.
:::

::: example Proving identities with $2A$
**Problem.** Prove that (i) $\frac{1-\cos2A}{\sin2A}=\tan A$; (ii) $(\sin A+\cos A)^2=1+\sin2A$.

**Solution.** (i) LHS $=\frac{2\sin^2A}{2\sin A\cos A}=\frac{\sin A}{\cos A}=\tan A=$ RHS.

(ii) LHS $=\sin^2A+2\sin A\cos A+\cos^2A=1+\sin2A=$ RHS.
:::

::: example A longer proof
**Problem.** Prove that $\frac{\cos A+\sin A}{\cos A-\sin A}-\frac{\cos A-\sin A}{\cos A+\sin A}=2\tan2A$.

**Solution.** Put over a common denominator:
$$ \text{LHS}=\frac{(\cos A+\sin A)^2-(\cos A-\sin A)^2}{(\cos A-\sin A)(\cos A+\sin A)}=\frac{4\sin A\cos A}{\cos^2A-\sin^2A}=\frac{2\sin2A}{\cos2A}=2\tan2A. $$
:::

::: example Double angle in a quadrant, and a sum of sine and cosine
**Problem.** (i) If $\cos A=-\frac{5}{13}$ and $A$ lies in the second quadrant, find $\sin2A$ and $\cos2A$. (ii) If $\sin A+\cos A=\frac{1}{2}$, find $\sin2A$. (iii) If $\cos2A=\frac{7}{25}$ and $A$ is acute, find $\sin A$.

**Solution.** (i) In the second quadrant $\sin A>0$: $\sin A=\sqrt{1-\frac{25}{169}}=\frac{12}{13}$.
$\sin2A=2\cdot\frac{12}{13}\cdot\left(-\frac{5}{13}\right)=-\frac{120}{169}$ and $\cos2A=2\cos^2A-1=\frac{50}{169}-1=-\frac{119}{169}$.
Check: $(-120)^2+(-119)^2=14400+14161=28561=169^2$, so $\sin^22A+\cos^22A=1$ ✓.

(ii) Square both sides: $\sin^2A+2\sin A\cos A+\cos^2A=\frac{1}{4}$, so $1+\sin2A=\frac{1}{4}$ and $\sin2A=-\frac{3}{4}$.

(iii) $1-2\sin^2A=\frac{7}{25}\Rightarrow\sin^2A=\frac{9}{25}$, so $\sin A=\frac{3}{5}$ (acute).
:::

::: example More identities with $2A$
**Problem.** Prove that (i) $\cos^4A-\sin^4A=\cos2A$; (ii) $\tan A+\cot A=\frac{2}{\sin2A}$; (iii) $\frac{\sin2A}{1-\cos2A}=\cot A$.

**Solution.** (i) $\cos^4A-\sin^4A=(\cos^2A-\sin^2A)(\cos^2A+\sin^2A)=\cos2A\cdot1=\cos2A$.

(ii) $\tan A+\cot A=\frac{\sin^2A+\cos^2A}{\sin A\cos A}=\frac{1}{\sin A\cos A}=\frac{2}{2\sin A\cos A}=\frac{2}{\sin2A}$.

(iii) $\frac{2\sin A\cos A}{2\sin^2A}=\frac{\cos A}{\sin A}=\cot A$.
:::

### Triple angle

::: derivation Formulas for $\sin3A$ and $\cos3A$
We start from $3A=2A+A$ and use the compound and double-angle formulas.

**Step 1 — sine.**
$$ \sin3A=\sin2A\cos A+\cos2A\sin A=2\sin A\cos^2A+(1-2\sin^2A)\sin A $$

**Step 2 — write $\cos^2A$ as $1-\sin^2A$.**
$$ \sin3A=2\sin A(1-\sin^2A)+\sin A-2\sin^3A=2\sin A-2\sin^3A+\sin A-2\sin^3A $$

**Step 3 — collect terms.**
$$ \sin3A=3\sin A-4\sin^3A $$

**Step 4 — cosine.**
$$ \cos3A=\cos2A\cos A-\sin2A\sin A=(2\cos^2A-1)\cos A-2\sin^2A\cos A $$

**Step 5 — write $\sin^2A$ as $1-\cos^2A$.**
$$ \cos3A=2\cos^3A-\cos A-2\cos A(1-\cos^2A)=4\cos^3A-3\cos A $$

**What it means.** The triple angle needs only the **single** ratio of $A$. Check with $A=30^\circ$: $3\sin30^\circ-4\sin^330^\circ=\frac{3}{2}-\frac{1}{2}=1=\sin90^\circ$. ✓
:::

::: key Triple-angle formulas
$$ \sin3A=3\sin A-4\sin^3A,\qquad \cos3A=4\cos^3A-3\cos A,\qquad \tan3A=\frac{3\tan A-\tan^3A}{1-3\tan^2A} $$
:::

::: example Using the triple-angle formulas
**Problem.** (i) If $\cos A=\frac{1}{2}$, find $\cos3A$. (ii) If $\tan A=\frac{1}{2}$, find $\tan3A$. (iii) Prove that $\sin3A=4\sin A\sin(60^\circ-A)\sin(60^\circ+A)$.

**Solution.** (i) $\cos3A=4\left(\frac{1}{2}\right)^3-3\cdot\frac{1}{2}=\frac{1}{2}-\frac{3}{2}=-1$. (Here $A=60^\circ$ and $\cos180^\circ=-1$. ✓)

(ii) $\tan3A=\frac{3\cdot\frac{1}{2}-\frac{1}{8}}{1-3\cdot\frac{1}{4}}=\frac{\frac{11}{8}}{\frac{1}{4}}=\frac{11}{2}$.

(iii) First, $\sin(60^\circ-A)\sin(60^\circ+A)=\sin^260^\circ-\sin^2A=\frac{3}{4}-\sin^2A$ (by the identity proved in 4.1). So
$$ 4\sin A\left(\frac{3}{4}-\sin^2A\right)=3\sin A-4\sin^3A=\sin3A. $$
:::

::: caution Common mistakes
- Writing $\sin2A=2\sin A$ or $\cos2A=2\cos A$. Doubling the angle does **not** double the ratio. Test with $A=30^\circ$: $\sin60^\circ=0.866\neq2\sin30^\circ=1$.
- Writing $\cos2A=\cos^2A+\sin^2A$. That equals 1. The correct form has a **minus** sign.
- Using $\sin3A=3\sin A-4\sin A^3$ or forgetting that $\sin^3A$ means $(\sin A)^3$.
- Choosing the wrong form of $\cos2A$ and getting a long calculation: match the form to the given ratio.
:::

## 4.3 Submultiple angles $\frac{A}{2}$

A **submultiple angle** of $A$ is $\frac{A}{2},\ \frac{A}{3},\ \ldots$ Replace $A$ by $\frac{A}{2}$ in the double-angle formulas.

::: derivation Half-angle formulas
We start from the double-angle formulas written for the angle $\frac{A}{2}$ (so $2\times\frac{A}{2}=A$).

**Step 1 — sine.**
$$ \sin A=2\sin\frac{A}{2}\cos\frac{A}{2} $$

**Step 2 — cosine, two forms.**
$$ \cos A=1-2\sin^2\frac{A}{2} \qquad\text{and}\qquad \cos A=2\cos^2\frac{A}{2}-1 $$

**Step 3 — solve for the squares.**
$$ \sin^2\frac{A}{2}=\frac{1-\cos A}{2},\qquad \cos^2\frac{A}{2}=\frac{1+\cos A}{2} $$

**Step 4 — divide.**
$$ \tan^2\frac{A}{2}=\frac{1-\cos A}{1+\cos A} $$

**Step 5 — a form without a square root.** Multiply top and bottom of $\tan\frac{A}{2}=\frac{\sin\frac{A}{2}}{\cos\frac{A}{2}}$ by $2\cos\frac{A}{2}$ (or by $2\sin\frac{A}{2}$):
$$ \tan\frac{A}{2}=\frac{\sin A}{1+\cos A}=\frac{1-\cos A}{\sin A} $$

**What it means.** The sign of the root ($\pm$) is decided by the **quadrant of $\frac{A}{2}$**, not of $A$. For acute $\frac{A}{2}$ all three ratios are positive.
:::

```figure caption="Right triangle for $t=\tan\frac{A}{2}$ (here $t=\frac{1}{2}$). The sides $2t$, $1-t^2$ and $1+t^2$ give $\sin A=\frac{2t}{1+t^2}=\frac{4}{5}$, $\cos A=\frac{1-t^2}{1+t^2}=\frac{3}{5}$ and $\tan A=\frac{2t}{1-t^2}=\frac{4}{3}$."
fig, ax = plt.subplots(figsize=(4.4, 2.8))
ax.plot([0, 3, 3, 0], [0, 0, 4, 0], color=INK, lw=1.3)
ax.text(1.5, -0.4, '$1-t^2$ (= 3/4)', ha='center', va='top', fontsize=8.5)
ax.text(3.15, 2.0, '$2t$ (= 1)', ha='left', va='center', fontsize=8.5)
ax.text(1.3, 2.35, '$1+t^2$ (= 5/4)', ha='right', va='bottom', rotation=53, rotation_mode='anchor', fontsize=8.5)
from matplotlib.patches import Arc, Rectangle
ax.add_patch(Arc((0, 0), 1.6, 1.6, theta1=0, theta2=53.13, color=ACCENT, lw=1.2))
ax.text(1.0, 0.28, 'A', color=ACCENT, fontsize=9)
ax.add_patch(Rectangle((2.75, 0), 0.25, 0.25, fill=False, ec=INK, lw=0.8))
ax.set_xlim(-0.4, 5.3); ax.set_ylim(-1.1, 4.5); ax.set_aspect('equal'); ax.axis('off')
fig.tight_layout(pad=0.3)
```

::: key Half-angle formulas
$$ \sin A=2\sin\frac{A}{2}\cos\frac{A}{2},\qquad \cos A=\cos^2\frac{A}{2}-\sin^2\frac{A}{2}=2\cos^2\frac{A}{2}-1=1-2\sin^2\frac{A}{2} $$
$$ \tan A=\frac{2\tan\frac{A}{2}}{1-\tan^2\frac{A}{2}},\qquad \sin A=\frac{2\tan\frac{A}{2}}{1+\tan^2\frac{A}{2}},\qquad \cos A=\frac{1-\tan^2\frac{A}{2}}{1+\tan^2\frac{A}{2}} $$
$$ 2\sin^2\frac{A}{2}=1-\cos A,\qquad 2\cos^2\frac{A}{2}=1+\cos A $$
For the third part: $\sin A=3\sin\frac{A}{3}-4\sin^3\frac{A}{3}$ and $\cos A=4\cos^3\frac{A}{3}-3\cos\frac{A}{3}$.
:::

::: example Ratios of $\theta$ from a ratio of $\frac{\theta}{2}$
**Problem.** (i) If $\cos\frac{\theta}{2}=\frac{4}{5}$ ($\frac{\theta}{2}$ acute), find $\sin\theta$, $\cos\theta$, $\tan\theta$. (ii) If $\tan\frac{\theta}{2}=\frac{4}{3}$, find $\sin\theta$, $\cos\theta$. (iii) If $\sin\frac{\theta}{2}=\frac{1}{\sqrt{2}}$, find $\cos\theta$.

**Solution.** (i) $\sin\frac{\theta}{2}=\sqrt{1-\frac{16}{25}}=\frac{3}{5}$.
$\sin\theta=2\cdot\frac{3}{5}\cdot\frac{4}{5}=\frac{24}{25}$; $\cos\theta=2\cos^2\frac{\theta}{2}-1=\frac{32}{25}-1=\frac{7}{25}$; $\tan\theta=\frac{24}{7}$.

(ii) With $t=\frac{4}{3}$: $1+t^2=\frac{25}{9}$. $\sin\theta=\frac{2t}{1+t^2}=\frac{\frac{8}{3}}{\frac{25}{9}}=\frac{24}{25}$. $\cos\theta=\frac{1-t^2}{1+t^2}=\frac{-\frac{7}{9}}{\frac{25}{9}}=-\frac{7}{25}$. (So $\theta$ is in the second quadrant; $\tan\theta=-\frac{24}{7}$.)

(iii) $\cos\theta=1-2\sin^2\frac{\theta}{2}=1-2\cdot\frac{1}{2}=0$. (Here $\frac{\theta}{2}=45^\circ$, $\theta=90^\circ$. ✓)
:::

::: example Exact values from half angles
**Problem.** Find the exact values of $\sin15^\circ$ and $\tan22.5^\circ$.

**Solution.** $\sin^215^\circ=\frac{1-\cos30^\circ}{2}=\frac{1-\frac{\sqrt{3}}{2}}{2}=\frac{2-\sqrt{3}}{4}$, so $\sin15^\circ=\frac{\sqrt{2-\sqrt{3}}}{2}=\frac{\sqrt{6}-\sqrt{2}}{4}$. (This matches the compound-angle value from $\sin(45^\circ-30^\circ)$.)

$\tan22.5^\circ=\frac{\sin45^\circ}{1+\cos45^\circ}=\frac{\frac{1}{\sqrt{2}}}{1+\frac{1}{\sqrt{2}}}=\frac{1}{\sqrt{2}+1}=\sqrt{2}-1$.
:::

::: example Proving identities with half angles
**Problem.** Prove that (i) $\frac{1-\cos\theta}{1+\cos\theta}=\tan^2\frac{\theta}{2}$; (ii) $\frac{\sin\theta}{1+\cos\theta}=\tan\frac{\theta}{2}$; (iii) $\sqrt{\frac{1-\cos\theta}{2}}\cdot\sqrt{\frac{1+\cos\theta}{2}}=\frac{\sin\theta}{2}$ (for $0<\theta<180^\circ$).

**Solution.** (i) LHS $=\frac{2\sin^2\frac{\theta}{2}}{2\cos^2\frac{\theta}{2}}=\tan^2\frac{\theta}{2}$.

(ii) LHS $=\frac{2\sin\frac{\theta}{2}\cos\frac{\theta}{2}}{2\cos^2\frac{\theta}{2}}=\tan\frac{\theta}{2}$.

(iii) LHS $=\sqrt{\frac{1-\cos^2\theta}{4}}=\frac{\sin\theta}{2}$.
:::

::: example Half-angle ratios from $\cos\theta$, and a proof
**Problem.** (i) If $\cos\theta=\frac{7}{25}$ ($\theta$ acute), find $\sin\frac{\theta}{2}$ and $\cos\frac{\theta}{2}$. (ii) Prove that $\tan\left(45^\circ+\frac{\theta}{2}\right)=\sec\theta+\tan\theta$. (iii) Prove that $\frac{\sin\theta}{1-\cos\theta}=\cot\frac{\theta}{2}$.

**Solution.** (i) $\sin^2\frac{\theta}{2}=\frac{1-\frac{7}{25}}{2}=\frac{9}{25}$, so $\sin\frac{\theta}{2}=\frac{3}{5}$. $\cos^2\frac{\theta}{2}=\frac{1+\frac{7}{25}}{2}=\frac{16}{25}$, so $\cos\frac{\theta}{2}=\frac{4}{5}$ (both positive since $\frac{\theta}{2}$ is acute).

(ii) Let $t=\tan\frac{\theta}{2}$. Then $\tan\left(45^\circ+\frac{\theta}{2}\right)=\frac{1+t}{1-t}=\frac{(1+t)^2}{(1-t)(1+t)}=\frac{1+t^2}{1-t^2}+\frac{2t}{1-t^2}=\sec\theta+\tan\theta$, using $\cos\theta=\frac{1-t^2}{1+t^2}$ and $\tan\theta=\frac{2t}{1-t^2}$.

(iii) $\frac{\sin\theta}{1-\cos\theta}=\frac{2\sin\frac{\theta}{2}\cos\frac{\theta}{2}}{2\sin^2\frac{\theta}{2}}=\frac{\cos\frac{\theta}{2}}{\sin\frac{\theta}{2}}=\cot\frac{\theta}{2}$.
:::

## 4.4 Transformation formulas: sums, differences and products

::: derivation Product to sum
We start from the four compound-angle formulas for sine and cosine.

**Step 1 — add the two sine formulas.**
$$ \sin(A+B)+\sin(A-B)=2\sin A\cos B $$

**Step 2 — subtract them.**
$$ \sin(A+B)-\sin(A-B)=2\cos A\sin B $$

**Step 3 — add the two cosine formulas.**
$$ \cos(A+B)+\cos(A-B)=2\cos A\cos B $$

**Step 4 — subtract them (second minus first).**
$$ \cos(A-B)-\cos(A+B)=2\sin A\sin B $$

**Step 5 — sum to product.** Put $A+B=C$ and $A-B=D$, so $A=\frac{C+D}{2}$ and $B=\frac{C-D}{2}$. Steps 1 to 4 become the formulas below.

**What it means.** A product of two ratios turns into a sum or difference of single ratios (easier to add or integrate), and a sum or difference turns into a product (easier to factorise and simplify).
:::

::: key Transformation formulas
**Product to sum**
$$ 2\sin A\cos B=\sin(A+B)+\sin(A-B) \qquad 2\cos A\sin B=\sin(A+B)-\sin(A-B) $$
$$ 2\cos A\cos B=\cos(A+B)+\cos(A-B) \qquad 2\sin A\sin B=\cos(A-B)-\cos(A+B) $$

**Sum to product**
$$ \sin C+\sin D=2\sin\frac{C+D}{2}\cos\frac{C-D}{2} \qquad \sin C-\sin D=2\cos\frac{C+D}{2}\sin\frac{C-D}{2} $$
$$ \cos C+\cos D=2\cos\frac{C+D}{2}\cos\frac{C-D}{2} \qquad \cos C-\cos D=-2\sin\frac{C+D}{2}\sin\frac{C-D}{2} $$
:::

```figure caption="Sum to product: $\sin5x+\sin3x=2\sin4x\cos x$. The fast wave $\sin4x$ is shaped by the slow envelope $\pm2\cos x$ (dashed)."
x = np.linspace(0, 2*np.pi, 600)
fig, ax = plt.subplots(figsize=(4.8, 2.6))
ax.plot(x, np.sin(5*x) + np.sin(3*x), color=ACCENT, lw=1.3, label='sin 5x + sin 3x')
ax.plot(x, 2*np.cos(x), color=SERIES[1], lw=1.0, ls='--')
ax.plot(x, -2*np.cos(x), color=SERIES[1], lw=1.0, ls='--')
ax.axhline(0, color=INK, lw=0.6)
ax.set_xlim(0, 2*np.pi); ax.set_ylim(-2.7, 2.7)
ax.set_xticks([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi]); ax.set_xticklabels(['0', '90°', '180°', '270°', '360°'])
ax.text(0.2, 2.35, 'envelope  ±2 cos x', color=SERIES[1], fontsize=8)
ax.text(np.pi*1.25, -2.4, '= 2 sin 4x cos x', color=ACCENT, fontsize=8)
ax.tick_params(labelsize=8); ax.grid(color=GRID, lw=0.5); ax.spines[['top','right']].set_visible(False)
fig.tight_layout(pad=0.4)
```

::: tip The examiner is looking for
(1) writing which of the four product-to-sum formulas you start from, (2) choosing $C$ and $D$ so that $\frac{C+D}{2}$ and $\frac{C-D}{2}$ are nice angles, (3) the **minus** sign in $\cos C-\cos D$, (4) a simplified final value.
:::

::: example Sum or difference to product
**Problem.** Find the exact values of (i) $\sin75^\circ+\sin15^\circ$, (ii) $\cos15^\circ-\cos75^\circ$.

**Solution.** (i) $\sin75^\circ+\sin15^\circ=2\sin\frac{75^\circ+15^\circ}{2}\cos\frac{75^\circ-15^\circ}{2}=2\sin45^\circ\cos30^\circ=2\cdot\frac{1}{\sqrt{2}}\cdot\frac{\sqrt{3}}{2}=\frac{\sqrt{3}}{\sqrt{2}}=\frac{\sqrt{6}}{2}$.

(ii) $\cos15^\circ-\cos75^\circ=-2\sin\frac{15^\circ+75^\circ}{2}\sin\frac{15^\circ-75^\circ}{2}=-2\sin45^\circ\sin(-30^\circ)=2\cdot\frac{1}{\sqrt{2}}\cdot\frac{1}{2}=\frac{1}{\sqrt{2}}$.
:::

::: example Product to sum
**Problem.** Express as a sum or difference: (i) $2\sin5\theta\cos2\theta$, (ii) $2\cos7\theta\cos3\theta$, (iii) $\sin75^\circ\sin15^\circ$ (and evaluate).

**Solution.** (i) $2\sin5\theta\cos2\theta=\sin7\theta+\sin3\theta$.

(ii) $2\cos7\theta\cos3\theta=\cos10\theta+\cos4\theta$.

(iii) $\sin75^\circ\sin15^\circ=\frac{1}{2}\left[\cos60^\circ-\cos90^\circ\right]=\frac{1}{2}\left[\frac{1}{2}-0\right]=\frac{1}{4}$.
:::

::: example Proving an identity
**Problem.** Prove that $\frac{\sin5A+\sin3A}{\cos5A+\cos3A}=\tan4A$.

**Solution.** $\sin5A+\sin3A=2\sin4A\cos A$ and $\cos5A+\cos3A=2\cos4A\cos A$. So
$$ \text{LHS}=\frac{2\sin4A\cos A}{2\cos4A\cos A}=\tan4A. $$
:::

::: example Value of a product of sines and cosines
**Problem.** Show that (i) $\cos20^\circ\cos40^\circ\cos80^\circ=\frac{1}{8}$; (ii) $\sin20^\circ\sin40^\circ\sin80^\circ=\frac{\sqrt{3}}{8}$.

**Solution.** (i) Let $P=\cos20^\circ\cos40^\circ\cos80^\circ$. Multiply and divide by $2\sin20^\circ$ and use $2\sin\theta\cos\theta=\sin2\theta$ repeatedly:
$$ P=\frac{2\sin20^\circ\cos20^\circ\cos40^\circ\cos80^\circ}{2\sin20^\circ}=\frac{\sin40^\circ\cos40^\circ\cos80^\circ}{2\sin20^\circ}=\frac{\sin80^\circ\cos80^\circ}{4\sin20^\circ}=\frac{\sin160^\circ}{8\sin20^\circ}. $$
Since $\sin160^\circ=\sin20^\circ$, $P=\frac{1}{8}$.

(ii) Use $\sin3A=4\sin A\sin(60^\circ-A)\sin(60^\circ+A)$ from 4.2 with $A=20^\circ$: $\sin60^\circ=4\sin20^\circ\sin40^\circ\sin80^\circ$. So the product is $\frac{\sin60^\circ}{4}=\frac{\sqrt{3}}{8}$.
:::

::: example Two more transformation proofs
**Problem.** Prove that (i) $\frac{\sin3A-\sin A}{\cos3A+\cos A}=\tan A$; (ii) $\frac{\cos A-\cos3A}{\sin3A-\sin A}=\tan2A$; (iii) $\cos105^\circ+\cos15^\circ=\frac{1}{\sqrt{2}}$.

**Solution.** (i) $\sin3A-\sin A=2\cos2A\sin A$ and $\cos3A+\cos A=2\cos2A\cos A$. The ratio is $\frac{\sin A}{\cos A}=\tan A$.

(ii) $\cos A-\cos3A=-2\sin2A\sin(-A)=2\sin2A\sin A$ and $\sin3A-\sin A=2\cos2A\sin A$. The ratio is $\frac{\sin2A}{\cos2A}=\tan2A$.

(iii) $\cos105^\circ+\cos15^\circ=2\cos60^\circ\cos45^\circ=2\cdot\frac{1}{2}\cdot\frac{1}{\sqrt{2}}=\frac{1}{\sqrt{2}}$.
:::

## 4.5 Exercises of the SEE type

::: example Sum of sines to a product, then a value
**Problem.** Prove that $\sin A+\sin3A+\sin5A=\sin3A\,(1+2\cos2A)$.

**Solution.** $\sin A+\sin5A=2\sin3A\cos2A$. So LHS $=2\sin3A\cos2A+\sin3A=\sin3A(2\cos2A+1)$ $=\sin3A\,(1+2\cos2A)$ = RHS.
:::

::: example Combining the formulas
**Problem.** Prove that $\cos4A=8\cos^4A-8\cos^2A+1$.

**Solution.** $\cos4A=\cos2(2A)=2\cos^22A-1$. Now $\cos2A=2\cos^2A-1$, so
$$ \cos4A=2(2\cos^2A-1)^2-1=2(4\cos^4A-4\cos^2A+1)-1 $$
$$ \cos4A=8\cos^4A-8\cos^2A+1. $$
:::

::: example A sum that collapses
**Problem.** Prove that $\cos A+\cos(120^\circ-A)+\cos(120^\circ+A)=0$.

**Solution.** $\cos(120^\circ-A)+\cos(120^\circ+A)=2\cos120^\circ\cos A=2\left(-\frac{1}{2}\right)\cos A=-\cos A$. So the sum is $\cos A-\cos A=0$.
:::

::: example Another special product
**Problem.** Find the value of $\sin10^\circ\sin50^\circ\sin70^\circ$.

**Solution.** Write $50^\circ=60^\circ-10^\circ$ and $70^\circ=60^\circ+10^\circ$. Then $\sin10^\circ\sin(60^\circ-10^\circ)\sin(60^\circ+10^\circ)=\frac{\sin30^\circ}{4}=\frac{1/2}{4}=\frac{1}{8}$, by $\sin3A=4\sin A\sin(60^\circ-A)\sin(60^\circ+A)$ with $A=10^\circ$.
:::

## Chapter summary

- **Compound angles:** $\sin(A\pm B)=\sin A\cos B\pm\cos A\sin B$; $\cos(A\pm B)=\cos A\cos B\mp\sin A\sin B$; $\tan(A\pm B)=\frac{\tan A\pm\tan B}{1\mp\tan A\tan B}$.
- **Double angle:** $\sin2A=2\sin A\cos A=\frac{2\tan A}{1+\tan^2A}$; $\cos2A=\cos^2A-\sin^2A=2\cos^2A-1=1-2\sin^2A=\frac{1-\tan^2A}{1+\tan^2A}$; $\tan2A=\frac{2\tan A}{1-\tan^2A}$.
- **Triple angle:** $\sin3A=3\sin A-4\sin^3A$; $\cos3A=4\cos^3A-3\cos A$; $\tan3A=\frac{3\tan A-\tan^3A}{1-3\tan^2A}$.
- **Half angle:** $\sin^2\frac{A}{2}=\frac{1-\cos A}{2}$; $\cos^2\frac{A}{2}=\frac{1+\cos A}{2}$; $\tan\frac{A}{2}=\frac{\sin A}{1+\cos A}=\frac{1-\cos A}{\sin A}$. Sign from the quadrant of $\frac{A}{2}$.
- **Product to sum:** $2\sin A\cos B=\sin(A+B)+\sin(A-B)$; $2\cos A\cos B=\cos(A+B)+\cos(A-B)$; $2\sin A\sin B=\cos(A-B)-\cos(A+B)$.
- **Sum to product:** $\sin C+\sin D=2\sin\frac{C+D}{2}\cos\frac{C-D}{2}$; $\cos C+\cos D=2\cos\frac{C+D}{2}\cos\frac{C-D}{2}$; $\cos C-\cos D=-2\sin\frac{C+D}{2}\sin\frac{C-D}{2}$.
- Special products: $\cos20^\circ\cos40^\circ\cos80^\circ=\frac{1}{8}$; $\sin20^\circ\sin40^\circ\sin80^\circ=\frac{\sqrt{3}}{8}$.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The value of $\sin75^\circ$ is <span class="marks">[1]</span>
   (a) $\frac{\sqrt{6}-\sqrt{2}}{4}$ (b) $\frac{\sqrt{6}+\sqrt{2}}{4}$ (c) $\frac{\sqrt{3}+1}{2}$ (d) $\frac{\sqrt{3}}{2}$
2. If $\sin A=\frac{3}{5}$, then $\cos2A$ is <span class="marks">[1]</span>
   (a) $\frac{24}{25}$ (b) $\frac{16}{25}$ (c) $\frac{7}{25}$ (d) $\frac{9}{25}$
3. Which of these is **not** equal to $\cos2A$? <span class="marks">[1]</span>
   (a) $\cos^2A-\sin^2A$ (b) $2\cos^2A-1$ (c) $1-2\sin^2A$ (d) $2\sin^2A-1$
4. $\sin^2\frac{A}{2}$ equals <span class="marks">[1]</span>
   (a) $\frac{1+\cos A}{2}$ (b) $\frac{1-\cos A}{2}$ (c) $\frac{1-\sin A}{2}$ (d) $1-\cos A$
5. $2\sin A\cos B$ equals <span class="marks">[1]</span>
   (a) $\sin(A+B)+\sin(A-B)$ (b) $\sin(A+B)-\sin(A-B)$ (c) $\cos(A+B)+\cos(A-B)$ (d) $\cos(A-B)-\cos(A+B)$
6. The value of $\tan22.5^\circ$ is <span class="marks">[1]</span>
   (a) $\sqrt{2}+1$ (b) $\sqrt{2}-1$ (c) $\frac{1}{\sqrt{2}}$ (d) $\frac{\sqrt{3}}{3}$

::: note Answers to Group A
**1.** (b) — $\sin(45^\circ+30^\circ)=\frac{\sqrt{6}+\sqrt{2}}{4}$.
**2.** (c) — $1-2\cdot\frac{9}{25}=\frac{7}{25}$.
**3.** (d) — $1-2\sin^2A$ is the correct form; $2\sin^2A-1=-\cos2A$.
**4.** (b) — from $\cos A=1-2\sin^2\frac{A}{2}$.
**5.** (a) — add the two sine compound formulas.
**6.** (b) — $\tan22.5^\circ=\frac{\sin45^\circ}{1+\cos45^\circ}=\sqrt{2}-1$.
:::

**Group B — Short answer (2 marks each)**

1. Find the exact value of $\sin15^\circ$ using a compound-angle formula. <span class="marks">[2]</span>
2. If $\tan A=\frac{3}{4}$, find $\tan2A$. <span class="marks">[2]</span>
3. Prove that $\frac{\sin2A}{1+\cos2A}=\tan A$. <span class="marks">[2]</span>
4. Express $2\sin5\theta\cos2\theta$ as a sum. <span class="marks">[2]</span>
5. Find the value of $\sin75^\circ+\sin15^\circ$. <span class="marks">[2]</span>

::: note Answers to Group B
**1.** $\sin(45^\circ-30^\circ)=\frac{1}{\sqrt{2}}\cdot\frac{\sqrt{3}}{2}-\frac{1}{\sqrt{2}}\cdot\frac{1}{2}=\frac{\sqrt{3}-1}{2\sqrt{2}}=\frac{\sqrt{6}-\sqrt{2}}{4}$.
**2.** $\tan2A=\frac{2\cdot\frac{3}{4}}{1-\frac{9}{16}}=\frac{24}{7}$.
**3.** LHS $=\frac{2\sin A\cos A}{2\cos^2A}=\tan A$.
**4.** $2\sin5\theta\cos2\theta=\sin7\theta+\sin3\theta$.
**5.** $2\sin45^\circ\cos30^\circ=2\cdot\frac{1}{\sqrt{2}}\cdot\frac{\sqrt{3}}{2}=\frac{\sqrt{6}}{2}$.
:::

**Group C — Short answer (3 marks each)**

1. If $\sin A=\frac{3}{5}$ and $A$ is acute, find $\sin2A$, $\cos2A$ and $\tan2A$. <span class="marks">[3]</span>
2. If $\cos\frac{\theta}{2}=\frac{4}{5}$ ($\frac{\theta}{2}$ acute), find $\sin\theta$ and $\cos\theta$. <span class="marks">[3]</span>
3. Prove that $\frac{\sin5A+\sin3A}{\cos5A+\cos3A}=\tan4A$. <span class="marks">[3]</span>
4. Prove that $\sin3A=4\sin A\sin(60^\circ-A)\sin(60^\circ+A)$. <span class="marks">[3]</span>
5. Find the value of $\cos15^\circ-\cos75^\circ$. <span class="marks">[3]</span>

::: note Answers to Group C
**1.** $\cos A=\frac{4}{5}$. $\sin2A=2\cdot\frac{3}{5}\cdot\frac{4}{5}=\frac{24}{25}$; $\cos2A=1-2\cdot\frac{9}{25}=\frac{7}{25}$; $\tan2A=\frac{24}{7}$.
**2.** $\sin\frac{\theta}{2}=\frac{3}{5}$. $\sin\theta=2\cdot\frac{3}{5}\cdot\frac{4}{5}=\frac{24}{25}$; $\cos\theta=2\cdot\frac{16}{25}-1=\frac{7}{25}$.
**3.** $\sin5A+\sin3A=2\sin4A\cos A$; $\cos5A+\cos3A=2\cos4A\cos A$; the ratio is $\tan4A$.
**4.** $\sin(60^\circ-A)\sin(60^\circ+A)=\sin^260^\circ-\sin^2A=\frac{3}{4}-\sin^2A$. Then $4\sin A(\frac{3}{4}-\sin^2A)=3\sin A-4\sin^3A=\sin3A$.
**5.** $-2\sin45^\circ\sin(-30^\circ)=2\cdot\frac{1}{\sqrt{2}}\cdot\frac{1}{2}=\frac{1}{\sqrt{2}}=\frac{\sqrt{2}}{2}$.
:::

**Group D — Long answer (4 marks each)**

1. Prove that $\frac{\cos A+\sin A}{\cos A-\sin A}-\frac{\cos A-\sin A}{\cos A+\sin A}=2\tan2A$. <span class="marks">[4]</span>
2. Prove that $\cos20^\circ\cos40^\circ\cos80^\circ=\frac{1}{8}$. <span class="marks">[4]</span>
3. If $\tan A=\frac{1}{2}$ and $\tan B=\frac{1}{3}$, show that $A+B=45^\circ$ and find $\tan2A$. <span class="marks">[4]</span>
4. If $\tan\frac{\theta}{2}=\frac{4}{3}$, find $\sin\theta$, $\cos\theta$ and $\tan\theta$. <span class="marks">[4]</span>
5. Prove that $\sin20^\circ\sin40^\circ\sin80^\circ=\frac{\sqrt{3}}{8}$. <span class="marks">[4]</span>

::: note Answers to Group D
**1.** LHS $=\frac{(\cos A+\sin A)^2-(\cos A-\sin A)^2}{\cos^2A-\sin^2A}=\frac{4\sin A\cos A}{\cos2A}=\frac{2\sin2A}{\cos2A}=2\tan2A$.
**2.** $P=\frac{2\sin20^\circ\cos20^\circ\cos40^\circ\cos80^\circ}{2\sin20^\circ}=\frac{\sin40^\circ\cos40^\circ\cos80^\circ}{2\sin20^\circ}=\frac{\sin80^\circ\cos80^\circ}{4\sin20^\circ}=\frac{\sin160^\circ}{8\sin20^\circ}=\frac{1}{8}$.
**3.** $\tan(A+B)=\frac{\frac{1}{2}+\frac{1}{3}}{1-\frac{1}{6}}=1$, so $A+B=45^\circ$. $\tan2A=\frac{1}{1-\frac{1}{4}}=\frac{4}{3}$.
**4.** $t=\frac{4}{3}$, $1+t^2=\frac{25}{9}$. $\sin\theta=\frac{8/3}{25/9}=\frac{24}{25}$; $\cos\theta=\frac{1-16/9}{25/9}=-\frac{7}{25}$; $\tan\theta=-\frac{24}{7}$.
**5.** From $\sin3A=4\sin A\sin(60^\circ-A)\sin(60^\circ+A)$ with $A=20^\circ$: $\sin60^\circ=4\sin20^\circ\sin40^\circ\sin80^\circ$, so the product is $\frac{\sqrt{3}/2}{4}=\frac{\sqrt{3}}{8}$.
:::


## Retrieval practice and investigation

::: key Work before reading the key
Answer these short retrieval questions without consulting the chapter. Explain the reason, not only the result. These are revision checks, not a prediction of the examination paper.
:::

**1.** Evaluate sin 2A when A = 30°.

**2.** Is sin(A + B) equal to sin A + sin B?

**3.** Evaluate cos 2A at A = 45°.

::: note Reasoned key
**1.** sin 60° = √3/2; also 2 sin 30° cos 30° = 2 × 1/2 × √3/2 = √3/2.

**2.** No. At A = B = 30°, the left side is √3/2 but the right side is 1.

**3.** 0. Each form agrees: cos²45° − sin²45° = 1/2 − 1/2 = 0.

:::

::: tip Investigation — Verify a transformation formula
Choose A = 30° and B = 45°. Evaluate sin(A + B) directly and through sin A cos B + cos A sin B. Keep exact surd values until the last step. Repeat with A − B and explain the sign change.

Submit a one-page record: your method, working or evidence, conclusion, and one limitation. Exchange it with a classmate and check the reasoning against the chapter.
:::
