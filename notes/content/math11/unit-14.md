---
subject: Mathematics
grade: 11
unit: 14
title: Vectors
hours: 12
area: Vectors
---

A vector is a quantity that needs a direction as well as a size before it means
anything. Once you can add vectors, resolve them into components and write one
vector in terms of others, a large part of coordinate geometry and mechanics
becomes ordinary algebra. This unit builds that algebra: collinearity,
coplanarity, linear combinations, linear dependence, and the scalar product that
measures the angle between two vectors.

::: key What this unit is really testing
Almost every vector question reduces to one of three sentences. "Two vectors are
parallel" means $\vec{a} = k\vec{b}$. "Three vectors are coplanar" means one is a
linear combination of the other two. "Two vectors are perpendicular" means
$\vec{a}\cdot\vec{b} = 0$. Learn to recognise which sentence a question is asking
you to write down, and the working is short.
:::

## 14.1 Collinear and non-collinear vectors

### Notation, magnitude and unit vectors

A **scalar** has magnitude only (mass, time, temperature). A **vector** has
magnitude and direction (displacement, velocity, force). A vector is drawn as a
directed line segment: the length of the segment is the magnitude, the arrowhead
gives the direction. The vector from $A$ to $B$ is written $\vec{AB}$, or by a
single letter $\vec{a}$. Its magnitude is $|\vec{AB}|$ or $|\vec{a}|$, a
non-negative scalar.

| Type of vector | Meaning |
|---|---|
| Zero (null) vector $\vec{0}$ | magnitude $0$, direction undefined |
| Unit vector $\hat{a}$ | magnitude exactly $1$ |
| Equal vectors | same magnitude **and** same direction |
| Negative vector $-\vec{a}$ | same magnitude, opposite direction |
| Like vectors | parallel, same sense |
| Unlike vectors | parallel, opposite sense |
| Position vector | vector from a fixed origin $O$ to a point |

In space we fix three mutually perpendicular unit vectors $\hat{i}$, $\hat{j}$,
$\hat{k}$ along $OX$, $OY$, $OZ$. Every vector can then be written in
**component form**:

$$ \vec{r} = x\hat{i} + y\hat{j} + z\hat{k}, \qquad |\vec{r}| = \sqrt{x^{2} + y^{2} + z^{2}} $$

```figure caption="The base unit vectors $\hat{i},\hat{j},\hat{k}$ and the position vector $\vec{OP} = 2\hat{i}+3\hat{j}+4\hat{k}$ of the point $P(2,3,4)$. The dashed lines show how the three components build up the vector."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.4,3.2))
def P(x,y,z): return (y-0.55*x, z-0.42*x)
def arrow(a,b,c=INK,lw=1.6,ls='-',ms=11):
    ax.annotate('', xy=b, xytext=a, arrowprops=dict(arrowstyle='-|>',color=c,lw=lw,
        linestyle=ls, shrinkA=0, shrinkB=0, mutation_scale=ms))
O=P(0,0,0)
arrow(O,P(3.4,0,0),MUTED,1.0); arrow(O,P(0,4.4,0),MUTED,1.0); arrow(O,P(0,0,5.0),MUTED,1.0)
ax.annotate('$X$',P(3.6,0,0),fontsize=9.5,color=MUTED,ha='center',va='top')
ax.annotate('$Y$',P(0,4.6,0),fontsize=9.5,color=MUTED,ha='left',va='center')
ax.annotate('$Z$',P(0,0,5.2),fontsize=9.5,color=MUTED,ha='center',va='bottom')
arrow(O,P(1,0,0),SERIES[2],2.1); arrow(O,P(0,1,0),SERIES[2],2.1); arrow(O,P(0,0,1),SERIES[2],2.1)
ax.annotate('$\\hat{i}$',P(1.05,0,0),fontsize=10,color=SERIES[2],ha='right',va='top')
ax.annotate('$\\hat{j}$',P(0,1.05,0),fontsize=10,color=SERIES[2],ha='left',va='top')
ax.annotate('$\\hat{k}$',P(0,0,1.05),fontsize=10,color=SERIES[2],ha='right',va='bottom')
arrow(O,P(2,3,4),ACCENT,2.0,ms=13)
ax.annotate('$\\vec{r}$',(np.array(P(2,3,4))+np.array(O))/2,fontsize=11,color=ACCENT,
            ha='right',va='bottom')
for a,b in [((0,0,0),(2,0,0)),((2,0,0),(2,3,0)),((2,3,0),(2,3,4)),((0,0,0),(2,3,0))]:
    p1,p2=P(*a),P(*b); ax.plot([p1[0],p2[0]],[p1[1],p2[1]],color=MUTED,lw=0.9,ls=(0,(3,2)))
p=P(2,3,4); ax.plot([p[0]],[p[1]],'o',color=ACCENT,ms=5)
ax.annotate('$P(2,3,4)$',p,textcoords='offset points',xytext=(5,2),fontsize=9.5,color=INK)
ax.annotate('$O$',O,textcoords='offset points',xytext=(-4,-9),fontsize=9.5,color=INK)
ax.set_xlim(-2.4,5.3); ax.set_ylim(-1.7,5.6); ax.set_aspect('equal'); ax.axis('off')
```

::: definition Unit vector and direction cosines
The unit vector along $\vec{a}$ is
$$ \hat{a} = \frac{\vec{a}}{|\vec{a}|} $$
If $\vec{a} = x\hat{i}+y\hat{j}+z\hat{k}$ makes angles $\alpha,\beta,\gamma$ with the
axes, its **direction cosines** are $l = x/|\vec{a}|$, $m = y/|\vec{a}|$,
$n = z/|\vec{a}|$, and they satisfy $l^{2}+m^{2}+n^{2} = 1$.
:::

::: example Worked example 14.1
**Problem.** For $\vec{a} = 2\hat{i} - 3\hat{j} + 6\hat{k}$, find $|\vec{a}|$, the
unit vector along $\vec{a}$, and its direction cosines.

**Solution.** Magnitude first, from the components:

$$ |\vec{a}| = \sqrt{2^{2} + (-3)^{2} + 6^{2}} = \sqrt{4 + 9 + 36} = \sqrt{49} = 7 $$

Divide the vector by its magnitude to get the unit vector:

$$ \hat{a} = \frac{2\hat{i} - 3\hat{j} + 6\hat{k}}{7} = \frac{2}{7}\hat{i} - \frac{3}{7}\hat{j} + \frac{6}{7}\hat{k} $$

The components of $\hat{a}$ *are* the direction cosines, so
$l = 2/7$, $m = -3/7$, $n = 6/7$. Check:
$\frac{4}{49} + \frac{9}{49} + \frac{36}{49} = \frac{49}{49} = 1$. ✔
:::

### Adding vectors: triangle and parallelogram laws

Vectors are added head to tail, not by adding magnitudes.

::: key The two laws of addition
**Triangle law.** If two vectors are represented by two sides of a triangle taken
in order, their sum is represented by the third side taken in the opposite order:
$\vec{AB} + \vec{BC} = \vec{AC}$.

**Parallelogram law.** If two vectors act at a point and are represented by two
adjacent sides of a parallelogram, their sum is the diagonal through that point.
:::

```figure caption="(a) Triangle law: $\vec{AB} + \vec{BC} = \vec{AC}$, head to tail. (b) Parallelogram law: with both vectors from the same point $O$, the resultant is the diagonal $\vec{OC}$, and $\vec{OD}-\vec{OA}$ is the other diagonal."
import numpy as np, matplotlib.pyplot as plt
fig, axes = plt.subplots(1,2,figsize=(5.1,2.5))
def arrow(ax,a,b,c=INK,lw=1.7,ls='-'):
    ax.annotate('', xy=b, xytext=a, arrowprops=dict(arrowstyle='-|>',color=c,lw=lw,
        linestyle=ls, shrinkA=0, shrinkB=0, mutation_scale=12))
ax=axes[0]
A=np.array([0,0]); B=np.array([2.4,1.35]); C=np.array([3.9,0.1])
arrow(ax,A,B,ACCENT,2.0); arrow(ax,B,C,SERIES[2],2.0); arrow(ax,A,C,SERIES[1],2.2)
ax.annotate('$\\vec{a}$',(A+B)/2,textcoords='offset points',xytext=(-14,2),color=ACCENT,fontsize=10)
ax.annotate('$\\vec{b}$',(B+C)/2,textcoords='offset points',xytext=(6,4),color=SERIES[2],fontsize=10)
ax.annotate('$\\vec{a}+\\vec{b}$',(A+C)/2,textcoords='offset points',xytext=(-12,-14),
            color=SERIES[1],fontsize=10)
for p,lab,off in [(A,'$A$',(-10,-4)),(B,'$B$',(-2,6)),(C,'$C$',(5,-2))]:
    ax.plot([p[0]],[p[1]],'o',color=INK,ms=3.4)
    ax.annotate(lab,p,textcoords='offset points',xytext=off,color=INK,fontsize=9.5)
ax.set_title('(a) triangle law',fontsize=9.5)
ax.set_xlim(-0.7,4.7); ax.set_ylim(-0.8,2.0)
ax=axes[1]
O=np.array([0,0]); a=np.array([2.7,0.15]); b=np.array([1.15,1.6]); c=a+b
ax.plot([a[0],c[0]],[a[1],c[1]],color=MUTED,lw=1.0,ls=(0,(3,2)))
ax.plot([b[0],c[0]],[b[1],c[1]],color=MUTED,lw=1.0,ls=(0,(3,2)))
arrow(ax,O,a,ACCENT,2.0); arrow(ax,O,b,SERIES[2],2.0); arrow(ax,O,c,SERIES[1],2.2)
arrow(ax,b,a,SERIES[4],1.5,ls=(0,(4,2)))
ax.annotate('$\\vec{a}$',(O+a)/2,textcoords='offset points',xytext=(-4,-13),color=ACCENT,fontsize=10)
ax.annotate('$\\vec{b}$',(O+b)/2,textcoords='offset points',xytext=(-17,-2),color=SERIES[2],fontsize=10)
ax.annotate('$\\vec{a}+\\vec{b}$',(O+c)/2,textcoords='offset points',xytext=(2,7),
            color=SERIES[1],fontsize=10)
ax.annotate('$\\vec{a}-\\vec{b}$',(a+b)/2,textcoords='offset points',xytext=(-6,-16),
            color=SERIES[4],fontsize=9.5)
ax.annotate('$\\theta$',(0.62,0.30),color=INK,fontsize=10)
th=np.linspace(np.arctan2(a[1],a[0]),np.arctan2(b[1],b[0]),40)
ax.plot(0.52*np.cos(th),0.52*np.sin(th),color=INK,lw=0.9)
for p,lab,off in [(O,'$O$',(-11,-5)),(a,'$A$',(4,-6)),(b,'$D$',(-11,2)),(c,'$C$',(4,2))]:
    ax.plot([p[0]],[p[1]],'o',color=INK,ms=3.4)
    ax.annotate(lab,p,textcoords='offset points',xytext=off,color=INK,fontsize=9.5)
ax.set_title('(b) parallelogram law',fontsize=9.5)
ax.set_xlim(-0.8,4.4); ax.set_ylim(-0.7,2.3)
for ax in axes: ax.set_aspect('equal'); ax.axis('off')
```

::: derivation Magnitude and direction of the resultant
Let $|\vec{a}| = a$, $|\vec{b}| = b$ and let $\theta$ be the angle between them, as
in the parallelogram figure. Drop a perpendicular from $C$ to the line $OA$
extended, meeting it at $N$. In the right triangle $ANC$,
$AN = b\cos\theta$ and $CN = b\sin\theta$.

Apply Pythagoras to the right triangle $ONC$:

$$ R^{2} = ON^{2} + CN^{2} = (a + b\cos\theta)^{2} + (b\sin\theta)^{2} $$

Expanding and using $\cos^{2}\theta + \sin^{2}\theta = 1$:

$$ R^{2} = a^{2} + 2ab\cos\theta + b^{2}\cos^{2}\theta + b^{2}\sin^{2}\theta = a^{2} + b^{2} + 2ab\cos\theta $$

$$ R = \sqrt{a^{2} + b^{2} + 2ab\cos\theta} $$

If the resultant makes an angle $\alpha$ with $\vec{a}$, then from the same
triangle $\tan\alpha = CN/ON$, so

$$ \tan\alpha = \frac{b\sin\theta}{a + b\cos\theta} $$
:::

::: example Worked example 14.2
**Problem.** Two vectors of magnitudes $5$ and $3$ units act at a point with
$60^{\circ}$ between them. Find the magnitude of their resultant and the angle it
makes with the larger vector.

**Solution.** Here $a = 5$, $b = 3$, $\theta = 60^{\circ}$, so
$\cos 60^{\circ} = 0.5$ and $\sin 60^{\circ} = 0.8660$.

$$ R = \sqrt{5^{2} + 3^{2} + 2(5)(3)(0.5)} = \sqrt{25 + 9 + 15} = \sqrt{49} = 7 \text{ units} $$

For the direction,

$$ \tan\alpha = \frac{3(0.8660)}{5 + 3(0.5)} = \frac{2.598}{6.5} = 0.3997 $$

so $\alpha = \tan^{-1}(0.3997) = 21.79^{\circ}$ from the $5$-unit vector.
:::

::: caution Magnitudes do not add
$|\vec{a}+\vec{b}| = |\vec{a}| + |\vec{b}|$ only when the two vectors are like
parallel vectors ($\theta = 0^{\circ}$). In general
$|\vec{a}+\vec{b}| \leq |\vec{a}| + |\vec{b}|$. Writing $5 + 3 = 8$ for the example
above instead of $7$ is the single commonest slip in this chapter.
:::

### Position vectors

Fix an origin $O$. The **position vector** of a point $A$ is $\vec{OA}$, usually
written $\vec{a}$. For any two points $A$ and $B$, the triangle law on
$O$, $A$, $B$ gives $\vec{OA} + \vec{AB} = \vec{OB}$, so

$$ \vec{AB} = \vec{OB} - \vec{OA} = \vec{b} - \vec{a} $$

In words: **the vector joining two points is the position vector of the head minus
the position vector of the tail.** Everything else in this chapter is built on
this one line.

```figure caption="Position vectors. $\vec{AB} = \vec{b} - \vec{a}$: head minus tail. The distance $AB$ is the magnitude $|\vec{b}-\vec{a}|$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.2,2.6))
O=np.array([0,0]); a=np.array([1.15,1.75]); b=np.array([3.5,0.55])
def arrow(p,q,c=INK,lw=1.8,ls='-'):
    ax.annotate('', xy=q, xytext=p, arrowprops=dict(arrowstyle='-|>',color=c,lw=lw,
        linestyle=ls, shrinkA=0, shrinkB=0, mutation_scale=12))
arrow(O,a,ACCENT); arrow(O,b,SERIES[2]); arrow(a,b,SERIES[1],2.1)
arrow(O,b-a,MUTED,1.3,ls=(0,(4,2)))
ax.annotate('$\\vec{a}$',(O+a)/2,textcoords='offset points',xytext=(-16,0),color=ACCENT,fontsize=10.5)
ax.annotate('$\\vec{b}$',(O+b)/2,textcoords='offset points',xytext=(-4,-14),color=SERIES[2],fontsize=10.5)
ax.annotate('$\\vec{b}-\\vec{a}$',(a+b)/2,textcoords='offset points',xytext=(2,7),
            color=SERIES[1],fontsize=10.5)
ax.annotate('same vector,\nmoved to $O$',(b-a)/2,textcoords='offset points',xytext=(-8,-26),
            color=MUTED,fontsize=8.4,ha='center')
for p,lab,off in [(O,'$O$',(-12,-5)),(a,'$A$',(-4,6)),(b,'$B$',(5,0))]:
    ax.plot([p[0]],[p[1]],'o',color=INK,ms=3.6)
    ax.annotate(lab,p,textcoords='offset points',xytext=off,color=INK,fontsize=9.5)
ax.set_xlim(-0.9,4.3); ax.set_ylim(-1.5,2.3); ax.set_aspect('equal'); ax.axis('off')
```

### Collinear and non-collinear vectors

::: definition Collinear and non-collinear vectors
Two or more vectors are **collinear** (or parallel) if they lie along the same line
or along parallel lines, so that each is a scalar multiple of the other. Vectors
that are not collinear are **non-collinear**.
$$ \vec{a} \parallel \vec{b} \Leftrightarrow \vec{a} = k\vec{b} \text{ for some scalar } k \ne 0 $$
:::

The scalar $k$ carries the information: $k > 0$ means like vectors (same sense),
$k < 0$ means unlike vectors, and $|k|$ is the ratio of the magnitudes.

In component form, $\vec{a} = a_1\hat{i}+a_2\hat{j}+a_3\hat{k}$ and
$\vec{b} = b_1\hat{i}+b_2\hat{j}+b_3\hat{k}$ are collinear when their components are
proportional:

$$ \frac{a_1}{b_1} = \frac{a_2}{b_2} = \frac{a_3}{b_3} $$

**Collinear points.** Three points $A$, $B$, $C$ are collinear if the vectors
$\vec{AB}$ and $\vec{BC}$ are collinear, i.e. $\vec{BC} = k\,\vec{AB}$. Because
they share the point $B$, the two parallel segments must lie on one straight line.

```figure caption="(a) $\vec{BC} = \tfrac{3}{2}\vec{AB}$, so $A$, $B$, $C$ are collinear. (b) $\vec{BC}$ is not a multiple of $\vec{AB}$: the points are non-collinear and form a triangle."
import numpy as np, matplotlib.pyplot as plt
fig, axes = plt.subplots(1,2,figsize=(5.1,2.3))
def arrow(ax,p,q,c=INK,lw=1.9):
    ax.annotate('', xy=q, xytext=p, arrowprops=dict(arrowstyle='-|>',color=c,lw=lw,
        shrinkA=0, shrinkB=0, mutation_scale=12))
ax=axes[0]
A=np.array([0,0]); B=np.array([1.5,0.85]); C=B+1.5*(B-A)
ax.plot([A[0],C[0]+0.35],[A[1],C[1]+0.20],color=GRID,lw=6,zorder=0)
arrow(ax,A,B,ACCENT); arrow(ax,B,C,SERIES[1])
ax.annotate('$\\vec{AB}$',(A+B)/2,textcoords='offset points',xytext=(-2,-16),color=ACCENT,fontsize=9.5)
ax.annotate('$\\vec{BC}$',(B+C)/2,textcoords='offset points',xytext=(-2,-16),color=SERIES[1],fontsize=9.5)
for p,lab in [(A,'$A$'),(B,'$B$'),(C,'$C$')]:
    ax.plot([p[0]],[p[1]],'o',color=INK,ms=4)
    ax.annotate(lab,p,textcoords='offset points',xytext=(-3,7),color=INK,fontsize=9.5)
ax.set_title('(a) collinear',fontsize=9.5); ax.set_xlim(-0.5,4.4); ax.set_ylim(-0.9,2.5)
ax=axes[1]
A=np.array([0,0]); B=np.array([1.7,0.3]); C=np.array([2.4,1.9])
arrow(ax,A,B,ACCENT); arrow(ax,B,C,SERIES[1])
ax.plot([C[0],A[0]],[C[1],A[1]],color=MUTED,lw=1.0,ls=(0,(3,2)))
ax.annotate('$\\vec{AB}$',(A+B)/2,textcoords='offset points',xytext=(-2,-16),color=ACCENT,fontsize=9.5)
ax.annotate('$\\vec{BC}$',(B+C)/2,textcoords='offset points',xytext=(6,-4),color=SERIES[1],fontsize=9.5)
for p,lab,off in [(A,'$A$',(-11,-4)),(B,'$B$',(2,-12)),(C,'$C$',(-3,7))]:
    ax.plot([p[0]],[p[1]],'o',color=INK,ms=4)
    ax.annotate(lab,p,textcoords='offset points',xytext=off,color=INK,fontsize=9.5)
ax.set_title('(b) non-collinear',fontsize=9.5); ax.set_xlim(-0.6,3.3); ax.set_ylim(-0.9,2.5)
for ax in axes: ax.set_aspect('equal'); ax.axis('off')
```

::: example Worked example 14.3
**Problem.** Show that the points $A(2,-1,3)$, $B(4,3,-1)$ and $C(7,9,-7)$ are
collinear.

**Solution.** Write the position vectors and take differences (head minus tail).

$$ \vec{AB} = \vec{b} - \vec{a} = (4-2)\hat{i} + (3+1)\hat{j} + (-1-3)\hat{k} = 2\hat{i} + 4\hat{j} - 4\hat{k} $$

$$ \vec{BC} = \vec{c} - \vec{b} = (7-4)\hat{i} + (9-3)\hat{j} + (-7+1)\hat{k} = 3\hat{i} + 6\hat{j} - 6\hat{k} $$

Now test whether one is a scalar multiple of the other:

$$ \vec{BC} = \frac{3}{2}\left(2\hat{i} + 4\hat{j} - 4\hat{k}\right) = \frac{3}{2}\vec{AB} $$

So $\vec{BC}$ is collinear with $\vec{AB}$, and since both contain the point $B$,
the three points lie on one straight line. Hence $A$, $B$, $C$ are collinear, and
$BC : AB = 3 : 2$.
:::

### The section formula

::: derivation Section formula — internal division
Let $P$ divide the join of $A$ and $B$ internally in the ratio $m:n$, so that
$AP : PB = m : n$. Then $\vec{AP}$ and $\vec{PB}$ point the same way, and

$$ n\,\vec{AP} = m\,\vec{PB} $$

Writing each as head minus tail with position vectors $\vec{a}$, $\vec{b}$, $\vec{r}$:

$$ n(\vec{r} - \vec{a}) = m(\vec{b} - \vec{r}) $$

$$ n\vec{r} + m\vec{r} = m\vec{b} + n\vec{a} \;\Longrightarrow\; \vec{r} = \frac{m\vec{b} + n\vec{a}}{m + n} $$

For **external** division the ratio is $AP:PB = m:(-n)$, so replace $n$ by $-n$:

$$ \vec{r} = \frac{m\vec{b} - n\vec{a}}{m - n} $$

Putting $m = n = 1$ in the internal formula gives the **midpoint**:
$\vec{r} = \dfrac{\vec{a}+\vec{b}}{2}$.
:::

```figure caption="Section formula. $P$ divides $AB$ internally in $m:n$ and $Q$ divides it externally in the same ratio; both position vectors are measured from $O$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,2.7))
O=np.array([0,0]); A=np.array([1.0,1.9]); B=np.array([4.3,1.1])
m,n=3,1
Pt=(m*B+n*A)/(m+n); Q=(m*B-n*A)/(m-n)
ax.plot([A[0],Q[0]],[A[1],Q[1]],color=GRID,lw=5,zorder=0)
def arrow(p,q,c=INK,lw=1.5,ls='-',ms=11):
    ax.annotate('', xy=q, xytext=p, arrowprops=dict(arrowstyle='-|>',color=c,lw=lw,
        linestyle=ls, shrinkA=0, shrinkB=0, mutation_scale=ms))
arrow(O,A,ACCENT,1.5); arrow(O,B,SERIES[2],1.5); arrow(O,Pt,SERIES[1],2.0)
ax.annotate('$\\vec{a}$',(O+A)/2,textcoords='offset points',xytext=(-14,0),color=ACCENT,fontsize=10)
ax.annotate('$\\vec{b}$',(O+B)/2,textcoords='offset points',xytext=(0,-14),color=SERIES[2],fontsize=10)
ax.annotate('$\\vec{r}$',(O+Pt)/2,textcoords='offset points',xytext=(-3,7),color=SERIES[1],fontsize=10)
for p,lab,off in [(O,'$O$',(-12,-5)),(A,'$A$',(-6,7)),(B,'$B$',(-2,8)),
                  (Pt,'$P$',(-3,8)),(Q,'$Q$',(3,6))]:
    ax.plot([p[0]],[p[1]],'o',color=INK,ms=4.2)
    ax.annotate(lab,p,textcoords='offset points',xytext=off,color=INK,fontsize=9.5)
ax.annotate('$m$',(A+Pt)/2,textcoords='offset points',xytext=(-2,-13),color=MUTED,fontsize=9)
ax.annotate('$n$',(Pt+B)/2,textcoords='offset points',xytext=(-2,-13),color=MUTED,fontsize=9)
ax.annotate('external\ndivision',Q,textcoords='offset points',xytext=(-6,-30),
            color=MUTED,fontsize=8.4,ha='center')
ax.set_xlim(-0.8,6.6); ax.set_ylim(-1.3,2.9); ax.set_aspect('equal'); ax.axis('off')
```

::: example Worked example 14.4
**Problem.** Find the position vector of the point that divides the join of
$A(1,2,3)$ and $B(6,7,8)$ in the ratio $2:3$ (a) internally, (b) externally.

**Solution.** Here $\vec{a} = \hat{i}+2\hat{j}+3\hat{k}$,
$\vec{b} = 6\hat{i}+7\hat{j}+8\hat{k}$, $m = 2$, $n = 3$.

(a) Internal division:

$$ \vec{r} = \frac{m\vec{b} + n\vec{a}}{m+n} = \frac{2(6\hat{i}+7\hat{j}+8\hat{k}) + 3(\hat{i}+2\hat{j}+3\hat{k})}{5} $$

$$ \vec{r} = \frac{(12+3)\hat{i} + (14+6)\hat{j} + (16+9)\hat{k}}{5} = \frac{15\hat{i}+20\hat{j}+25\hat{k}}{5} = 3\hat{i}+4\hat{j}+5\hat{k} $$

so the point is $(3,4,5)$.

(b) External division: replace $+n$ by $-n$ and $m+n$ by $m-n = -1$:

$$ \vec{r} = \frac{2(6\hat{i}+7\hat{j}+8\hat{k}) - 3(\hat{i}+2\hat{j}+3\hat{k})}{2-3} = \frac{9\hat{i}+8\hat{j}+7\hat{k}}{-1} = -9\hat{i}-8\hat{j}-7\hat{k} $$

so the point is $(-9,-8,-7)$. Note that it lies outside the segment $AB$, on the
side of $A$, as it must when $m < n$.
:::

::: tip Which position vector gets which coefficient
In $\vec{r} = \dfrac{m\vec{b}+n\vec{a}}{m+n}$ the coefficient of $\vec{b}$ is $m$ —
the part of the ratio **furthest** from $B$. Swapping $m$ and $n$ is the usual
error. Check your answer: the point must lie between $A$ and $B$ for internal
division.
:::

::: example Worked example 14.5
**Problem.** $P$, $Q$, $R$, $S$ are the midpoints of the sides $AB$, $BC$, $CD$,
$DA$ of a quadrilateral $ABCD$. Prove by vectors that $PQRS$ is a parallelogram.

**Solution.** Take any origin $O$ and let the position vectors of $A,B,C,D$ be
$\vec{a},\vec{b},\vec{c},\vec{d}$. By the midpoint formula,

$$ \vec{p} = \frac{\vec{a}+\vec{b}}{2}, \quad \vec{q} = \frac{\vec{b}+\vec{c}}{2}, \quad \vec{r} = \frac{\vec{c}+\vec{d}}{2}, \quad \vec{s} = \frac{\vec{d}+\vec{a}}{2} $$

Now compute two opposite sides, head minus tail:

$$ \vec{PQ} = \vec{q} - \vec{p} = \frac{\vec{b}+\vec{c}}{2} - \frac{\vec{a}+\vec{b}}{2} = \frac{\vec{c}-\vec{a}}{2} $$

$$ \vec{SR} = \vec{r} - \vec{s} = \frac{\vec{c}+\vec{d}}{2} - \frac{\vec{d}+\vec{a}}{2} = \frac{\vec{c}-\vec{a}}{2} $$

So $\vec{PQ} = \vec{SR}$: the sides $PQ$ and $SR$ are equal in length and parallel.
A quadrilateral with one pair of opposite sides equal and parallel is a
parallelogram. Hence $PQRS$ is a parallelogram, and each of its sides is half the
diagonal $AC$ or $BD$ of the original quadrilateral.
:::

## 14.2 Coplanar and non-coplanar vectors

::: definition Coplanar and non-coplanar vectors
Vectors are **coplanar** if, when drawn from a common point, they all lie in one
plane. Otherwise they are **non-coplanar**.
:::

Two facts settle most questions:

- **Any two vectors are always coplanar.** Drawn from a common point, two lines
  always determine a plane. You need at least *three* vectors before
  non-coplanarity is even possible.
- **Three vectors $\vec{a}$, $\vec{b}$, $\vec{c}$ (with $\vec{a}$, $\vec{b}$
  non-collinear) are coplanar if and only if** $\vec{c}$ can be written as
  $$ \vec{c} = x\vec{a} + y\vec{b} $$
  for some scalars $x$, $y$.

The reason is short. If $\vec{c} = x\vec{a}+y\vec{b}$, then $\vec{c}$ is built
entirely out of steps taken along $\vec{a}$ and $\vec{b}$, and every such step
stays in the plane of $\vec{a}$ and $\vec{b}$. Conversely, if $\vec{c}$ lies in
that plane, complete a parallelogram in the plane with sides along $\vec{a}$ and
$\vec{b}$ and diagonal $\vec{c}$; the side lengths give $x$ and $y$.

```figure caption="(a) $\vec{c}$ lies in the plane of $\vec{a}$ and $\vec{b}$, so $\vec{c} = x\vec{a}+y\vec{b}$ and the three are coplanar. (b) $\vec{c}$ sticks out of the plane: no choice of $x,y$ can reach it, so the three are non-coplanar."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Polygon
fig, axes = plt.subplots(1,2,figsize=(5.1,2.5))
def arrow(ax,p,q,c=INK,lw=1.9,ls='-'):
    ax.annotate('', xy=q, xytext=p, arrowprops=dict(arrowstyle='-|>',color=c,lw=lw,
        linestyle=ls, shrinkA=0, shrinkB=0, mutation_scale=12))
plane=np.array([[-1.35,-0.75],[2.3,-1.25],[3.15,0.5],[-0.5,1.0]])
O=np.array([0,0])
for k,ax in enumerate(axes):
    ax.add_patch(Polygon(plane,closed=True,facecolor=GRID,edgecolor='#b9c0cc',
                         lw=0.9,alpha=0.85,zorder=0))
    a=np.array([1.85,-0.35]); b=np.array([0.55,0.72])
    arrow(ax,O,a,ACCENT); arrow(ax,O,b,SERIES[2])
    ax.annotate('$\\vec{a}$',a,textcoords='offset points',xytext=(3,-7),color=ACCENT,fontsize=10)
    ax.annotate('$\\vec{b}$',b,textcoords='offset points',xytext=(-13,2),color=SERIES[2],fontsize=10)
    if k==0:
        c=0.95*a+1.25*b
        arrow(ax,O,c,SERIES[1],2.1)
        ax.plot([0.95*a[0],c[0]],[0.95*a[1],c[1]],color=MUTED,lw=0.9,ls=(0,(3,2)))
        ax.plot([1.25*b[0],c[0]],[1.25*b[1],c[1]],color=MUTED,lw=0.9,ls=(0,(3,2)))
        ax.annotate('$\\vec{c}=x\\vec{a}+y\\vec{b}$',c,textcoords='offset points',
                    xytext=(-2,12),color=SERIES[1],fontsize=9.5,ha='center')
        ax.set_title('(a) coplanar',fontsize=9.5)
    else:
        c=np.array([1.25,2.15])
        arrow(ax,O,c,SERIES[1],2.1)
        ax.plot([c[0],1.5],[c[1],0.05],color=MUTED,lw=0.9,ls=(0,(3,2)))
        ax.plot([1.5],[0.05],'x',color=MUTED,ms=5)
        ax.annotate('$\\vec{c}$',c,textcoords='offset points',xytext=(3,2),
                    color=SERIES[1],fontsize=10)
        ax.annotate('out of\nthe plane',(1.9,1.45),color=MUTED,fontsize=8.4,ha='left')
        ax.set_title('(b) non-coplanar',fontsize=9.5)
    ax.plot([0],[0],'o',color=INK,ms=3.6)
    ax.annotate('$O$',O,textcoords='offset points',xytext=(-11,-3),color=INK,fontsize=9.5)
    ax.set_xlim(-1.6,3.5); ax.set_ylim(-1.5,2.7); ax.set_aspect('equal'); ax.axis('off')
```

A consequence worth remembering: **any three points are always coplanar** (three
points determine a plane), so "prove these points are coplanar" only becomes a
real question for **four** points $A,B,C,D$ — and then the test is whether
$\vec{AD}$ is a linear combination of $\vec{AB}$ and $\vec{AC}$.

::: example Worked example 14.6
**Problem.** Show that the vectors $\vec{a} = \hat{i}+2\hat{j}-\hat{k}$,
$\vec{b} = 2\hat{i}-\hat{j}+3\hat{k}$ and $\vec{c} = 4\hat{i}+3\hat{j}+\hat{k}$ are
coplanar, and find the scalars involved.

**Solution.** $\vec{a}$ and $\vec{b}$ are not parallel (their components are not
proportional: $1/2 \ne 2/(-1)$), so we test whether $\vec{c} = x\vec{a} + y\vec{b}$.

Comparing components of $\hat{i}$, $\hat{j}$, $\hat{k}$ gives three equations:

$$ x + 2y = 4, \qquad 2x - y = 3, \qquad -x + 3y = 1 $$

Solve the first two. From the first, $x = 4 - 2y$; substituting into the second,

$$ 2(4-2y) - y = 3 \;\Rightarrow\; 8 - 5y = 3 \;\Rightarrow\; y = 1, \quad x = 2 $$

These values must also satisfy the third equation, and they do:
$-2 + 3(1) = 1$. ✔

Since $\vec{c} = 2\vec{a} + \vec{b}$, the vector $\vec{c}$ lies in the plane of
$\vec{a}$ and $\vec{b}$. The three vectors are coplanar.
:::

::: caution Check the third equation
Three components give three equations but there are only two unknowns. Solving two
of them always produces *some* $x$ and $y$; the vectors are coplanar **only if
those values also satisfy the third equation**. Skipping that check turns a proof
into a guess.
:::

::: example Worked example 14.7
**Problem.** Find the value of $\lambda$ for which the vectors
$\vec{a} = \hat{i}+2\hat{j}+3\hat{k}$, $\vec{b} = 2\hat{i}-\hat{j}+4\hat{k}$ and
$\vec{c} = 3\hat{i}+\lambda\hat{j}+7\hat{k}$ are coplanar.

**Solution.** Coplanar means $\vec{c} = x\vec{a} + y\vec{b}$. Comparing components:

$$ x + 2y = 3, \qquad 2x - y = \lambda, \qquad 3x + 4y = 7 $$

Use the two equations that do **not** contain $\lambda$. From the first,
$x = 3 - 2y$, so

$$ 3(3-2y) + 4y = 7 \;\Rightarrow\; 9 - 2y = 7 \;\Rightarrow\; y = 1, \quad x = 1 $$

Substituting into the remaining equation gives
$\lambda = 2(1) - 1 = 1$.

So $\lambda = 1$, and then $\vec{c} = \vec{a} + \vec{b}$ — which you can check
directly: $(1+2)\hat{i}+(2-1)\hat{j}+(3+4)\hat{k} = 3\hat{i}+\hat{j}+7\hat{k}$. ✔
:::

## 14.3 Linear combination of vectors

::: definition Linear combination
If $\vec{a}_1, \vec{a}_2, \ldots, \vec{a}_n$ are vectors and
$c_1, c_2, \ldots, c_n$ are scalars, the vector
$$ \vec{r} = c_1\vec{a}_1 + c_2\vec{a}_2 + \cdots + c_n\vec{a}_n $$
is called a **linear combination** of $\vec{a}_1, \ldots, \vec{a}_n$ with
coefficients $c_1,\ldots,c_n$.
:::

The whole of component form is one example: $\vec{r} = x\hat{i}+y\hat{j}+z\hat{k}$
is a linear combination of $\hat{i}$, $\hat{j}$, $\hat{k}$.

```figure caption="Every vector $\vec{r}$ in the plane of two non-collinear vectors $\vec{a},\vec{b}$ is a linear combination $\vec{r}=x\vec{a}+y\vec{b}$: here $\vec{r} = 2\vec{a} + \tfrac{3}{2}\vec{b}$, read off the grid of parallels."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6,3.0))
a=np.array([1.55,-0.40]); b=np.array([0.60,1.05])
for i in range(-1,5):
    p0=i*a-1.2*b; p1=i*a+3.0*b
    ax.plot([p0[0],p1[0]],[p0[1],p1[1]],color=GRID,lw=0.8,zorder=0)
for j in range(-1,4):
    p0=j*b-0.6*a; p1=j*b+3.6*a
    ax.plot([p0[0],p1[0]],[p0[1],p1[1]],color=GRID,lw=0.8,zorder=0)
def arrow(p,q,c=INK,lw=1.9,ls='-',ms=12):
    ax.annotate('', xy=q, xytext=p, arrowprops=dict(arrowstyle='-|>',color=c,lw=lw,
        linestyle=ls, shrinkA=0, shrinkB=0, mutation_scale=ms))
O=np.array([0,0]); r=2*a+1.5*b
arrow(O,a,ACCENT,2.2); arrow(O,b,SERIES[2],2.2)
arrow(O,2*a,ACCENT,1.2,ls=(0,(4,2)),ms=10)
arrow(2*a,r,SERIES[2],1.2,ls=(0,(4,2)),ms=10)
arrow(O,r,SERIES[1],2.3,ms=14)
ax.annotate('$\\vec{a}$',a/2,textcoords='offset points',xytext=(-2,-14),color=ACCENT,fontsize=10.5)
ax.annotate('$\\vec{b}$',b/2,textcoords='offset points',xytext=(-16,-2),color=SERIES[2],fontsize=10.5)
ax.annotate('$2\\vec{a}$',2*a,textcoords='offset points',xytext=(2,-13),color=ACCENT,fontsize=9.5)
ax.annotate('$\\frac{3}{2}\\vec{b}$',(2*a+r)/2,textcoords='offset points',xytext=(7,-4),
            color=SERIES[2],fontsize=9.5)
ax.annotate('$\\vec{r}=2\\vec{a}+\\frac{3}{2}\\vec{b}$',r,textcoords='offset points',
            xytext=(-30,9),color=SERIES[1],fontsize=10)
ax.plot([0],[0],'o',color=INK,ms=3.6)
ax.annotate('$O$',O,textcoords='offset points',xytext=(-11,-4),color=INK,fontsize=9.5)
ax.set_xlim(-1.3,4.6); ax.set_ylim(-1.5,2.6); ax.set_aspect('equal'); ax.axis('off')
```

::: derivation Uniqueness of the coefficients
Let $\vec{a}$ and $\vec{b}$ be non-collinear, and suppose the same vector
$\vec{r}$ can be written in two ways,

$$ \vec{r} = x_1\vec{a} + y_1\vec{b} = x_2\vec{a} + y_2\vec{b} $$

Subtracting,

$$ (x_1-x_2)\vec{a} + (y_1-y_2)\vec{b} = \vec{0} $$

If $x_1 \ne x_2$ we could divide by $(x_1-x_2)$ and get

$$ \vec{a} = -\frac{y_1-y_2}{x_1-x_2}\,\vec{b} $$

which says $\vec{a}$ is a scalar multiple of $\vec{b}$ — i.e. they are collinear,
contradicting our assumption. Hence $x_1 = x_2$, and then $(y_1-y_2)\vec{b} = \vec{0}$
with $\vec{b} \ne \vec{0}$ forces $y_1 = y_2$.

**Conclusion.** Two non-collinear vectors form a **basis** for their plane: every
vector in the plane is a linear combination of them in exactly one way. Likewise
three non-coplanar vectors form a basis for space.
:::

::: example Worked example 14.8
**Problem.** Express $\vec{c} = 8\hat{i}+7\hat{j}$ as a linear combination of
$\vec{a} = 2\hat{i}+3\hat{j}$ and $\vec{b} = \hat{i}-\hat{j}$.

**Solution.** Let $\vec{c} = x\vec{a} + y\vec{b}$. Then

$$ 8\hat{i}+7\hat{j} = x(2\hat{i}+3\hat{j}) + y(\hat{i}-\hat{j}) = (2x+y)\hat{i} + (3x-y)\hat{j} $$

Equate the coefficients of $\hat{i}$ and of $\hat{j}$ separately:

$$ 2x + y = 8, \qquad 3x - y = 7 $$

Adding the two equations eliminates $y$: $5x = 15$, so $x = 3$, and then
$y = 8 - 2(3) = 2$.

$$ \vec{c} = 3\vec{a} + 2\vec{b} $$

Check: $3(2\hat{i}+3\hat{j}) + 2(\hat{i}-\hat{j}) = 8\hat{i}+7\hat{j}$. ✔
Because $\vec{a}$ and $\vec{b}$ are non-collinear, this is the *only* possible
answer.
:::

## 14.4 Linearly dependent and independent vectors

::: definition Linear dependence and independence
The vectors $\vec{a}_1,\ldots,\vec{a}_n$ are **linearly dependent** if there exist
scalars $c_1,\ldots,c_n$, **not all zero**, such that
$$ c_1\vec{a}_1 + c_2\vec{a}_2 + \cdots + c_n\vec{a}_n = \vec{0} $$
If the only way to make the sum $\vec{0}$ is $c_1 = c_2 = \cdots = c_n = 0$, the
vectors are **linearly independent**.
:::

The definition looks abstract but says something concrete: a dependent set has at
least one vector that is redundant, because it can be built from the others. If
$c_1 \ne 0$, divide through by $c_1$:

$$ \vec{a}_1 = -\frac{c_2}{c_1}\vec{a}_2 - \cdots - \frac{c_n}{c_1}\vec{a}_n $$

This links the idea straight back to the last two sections:

| Number of vectors | Linearly dependent means | Linearly independent means |
|---|---|---|
| 2 | collinear (parallel) | non-collinear |
| 3 | coplanar | non-coplanar |
| 4 or more in space | always dependent | impossible |
| any set containing $\vec{0}$ | always dependent | — |

::: key The working method
To test $\vec{a},\vec{b},\vec{c}$ for independence, set
$x\vec{a}+y\vec{b}+z\vec{c} = \vec{0}$, compare the $\hat{i}$, $\hat{j}$, $\hat{k}$
components to get three homogeneous equations, and solve. If the only solution is
$x=y=z=0$, the vectors are independent; if a non-zero solution exists, they are
dependent and that solution is the relation between them.
:::

::: example Worked example 14.9
**Problem.** Show that $\vec{a} = \hat{i}+\hat{j}$, $\vec{b} = \hat{j}+\hat{k}$ and
$\vec{c} = \hat{k}+\hat{i}$ are linearly independent.

**Solution.** Suppose $x\vec{a} + y\vec{b} + z\vec{c} = \vec{0}$. Collecting terms,

$$ (x+z)\hat{i} + (x+y)\hat{j} + (y+z)\hat{k} = \vec{0} $$

Since $\hat{i},\hat{j},\hat{k}$ are themselves independent, each bracket is zero:

$$ x + z = 0, \qquad x + y = 0, \qquad y + z = 0 $$

Add all three equations: $2(x+y+z) = 0$, so $x+y+z = 0$. Subtracting each of the
three equations from this in turn,

$$ y = 0, \qquad z = 0, \qquad x = 0 $$

The only solution is the trivial one, so the three vectors are linearly
independent — equivalently, they are non-coplanar, and they form a basis of space.
:::

::: example Worked example 14.10
**Problem.** Show that $\vec{a} = \hat{i}+2\hat{j}-\hat{k}$,
$\vec{b} = 3\hat{i}-\hat{j}+2\hat{k}$ and $\vec{c} = 5\hat{i}+3\hat{j}$ are linearly
dependent, and write down the relation connecting them.

**Solution.** Try to build $\vec{c}$ from the other two: let
$\vec{c} = x\vec{a}+y\vec{b}$. Comparing components,

$$ x + 3y = 5, \qquad 2x - y = 3, \qquad -x + 2y = 0 $$

From the third equation, $x = 2y$. Substituting into the first,
$2y + 3y = 5$, so $y = 1$ and $x = 2$. Check the second equation:
$2(2) - 1 = 3$. ✔

Therefore $\vec{c} = 2\vec{a} + \vec{b}$, i.e.

$$ 2\vec{a} + \vec{b} - \vec{c} = \vec{0} $$

The coefficients $2, 1, -1$ are not all zero, so the three vectors are linearly
dependent (and hence coplanar).
:::

## 14.5 The scalar product and the angle between two vectors

The three tests above are all about *parallelism*. To measure **angles** — and in
particular perpendicularity — we need one more operation.

::: definition Scalar (dot) product
For vectors $\vec{a}$, $\vec{b}$ with angle $\theta$ ($0 \leq \theta \leq 180^{\circ}$)
between them,
$$ \vec{a}\cdot\vec{b} = |\vec{a}|\,|\vec{b}|\cos\theta $$
The result is a **scalar**, not a vector.
:::

Applying this to the base vectors, $\hat{i}\cdot\hat{i} = \hat{j}\cdot\hat{j} = \hat{k}\cdot\hat{k} = 1$
(angle $0^{\circ}$) and $\hat{i}\cdot\hat{j} = \hat{j}\cdot\hat{k} = \hat{k}\cdot\hat{i} = 0$
(angle $90^{\circ}$). Expanding
$(a_1\hat{i}+a_2\hat{j}+a_3\hat{k})\cdot(b_1\hat{i}+b_2\hat{j}+b_3\hat{k})$ term by
term, all the cross terms vanish and

$$ \vec{a}\cdot\vec{b} = a_1b_1 + a_2b_2 + a_3b_3 $$

Putting the two expressions together gives the working formula for the angle:

::: key Standard results for the dot product
$$ \cos\theta = \frac{\vec{a}\cdot\vec{b}}{|\vec{a}|\,|\vec{b}|} = \frac{a_1b_1+a_2b_2+a_3b_3}{\sqrt{a_1^{2}+a_2^{2}+a_3^{2}}\,\sqrt{b_1^{2}+b_2^{2}+b_3^{2}}} $$
- $\vec{a}\cdot\vec{b} = \vec{b}\cdot\vec{a}$ (commutative) and
  $\vec{a}\cdot(\vec{b}+\vec{c}) = \vec{a}\cdot\vec{b} + \vec{a}\cdot\vec{c}$ (distributive).
- $\vec{a}\cdot\vec{a} = |\vec{a}|^{2}$.
- $\vec{a} \perp \vec{b} \Leftrightarrow \vec{a}\cdot\vec{b} = 0$ (for non-zero vectors).
- Projection of $\vec{b}$ on $\vec{a}$ is $\dfrac{\vec{a}\cdot\vec{b}}{|\vec{a}|} = \vec{b}\cdot\hat{a}$.
:::

```figure caption="The scalar product as a projection: $\vec{a}\cdot\vec{b} = |\vec{a}|\,(|\vec{b}|\cos\theta)$, the length of $\vec{a}$ times the length of the shadow of $\vec{b}$ on $\vec{a}$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6,2.6))
O=np.array([0,0]); a=np.array([3.7,0.0]); b=np.array([1.95,1.75])
ah=a/np.linalg.norm(a); foot=(b@ah)*ah
def arrow(p,q,c=INK,lw=2.0,ls='-',ms=13):
    ax.annotate('', xy=q, xytext=p, arrowprops=dict(arrowstyle='-|>',color=c,lw=lw,
        linestyle=ls, shrinkA=0, shrinkB=0, mutation_scale=ms))
arrow(O,a,ACCENT); arrow(O,b,SERIES[2])
ax.plot([b[0],foot[0]],[b[1],foot[1]],color=MUTED,lw=1.0,ls=(0,(3,2)))
ax.plot([0,foot[0]],[-0.34,-0.34],color=SERIES[1],lw=2.6,solid_capstyle='butt')
ax.plot([foot[0],foot[0]],[-0.40,foot[1]+0.02],color=MUTED,lw=0.7,ls=':')
sq=0.16
ax.plot([foot[0]-sq,foot[0]-sq,foot[0]],[0,sq,sq],color=MUTED,lw=0.8)
th=np.linspace(0,np.arctan2(b[1],b[0]),40)
ax.plot(0.62*np.cos(th),0.62*np.sin(th),color=INK,lw=0.9)
ax.annotate('$\\theta$',(0.76,0.24),color=INK,fontsize=10.5)
ax.annotate('$\\vec{a}$',(2.8,0.0),textcoords='offset points',xytext=(0,7),color=ACCENT,fontsize=11)
ax.annotate('$\\vec{b}$',b/2,textcoords='offset points',xytext=(-15,3),color=SERIES[2],fontsize=11)
ax.annotate('projection $=|\\vec{b}|\\cos\\theta$',(foot[0]/2,-0.34),textcoords='offset points',
            xytext=(0,-15),color=SERIES[1],fontsize=9.5,ha='center')
ax.plot([0],[0],'o',color=INK,ms=3.6)
ax.annotate('$O$',O,textcoords='offset points',xytext=(-11,-2),color=INK,fontsize=9.5)
ax.set_xlim(-0.7,4.2); ax.set_ylim(-1.15,2.2); ax.set_aspect('equal'); ax.axis('off')
```

::: example Worked example 14.11
**Problem.** Find the angle between $\vec{a} = \hat{i}+\hat{j}$ and
$\vec{b} = \hat{i}+\hat{k}$.

**Solution.** In components $\vec{a} = (1,1,0)$ and $\vec{b} = (1,0,1)$, so

$$ \vec{a}\cdot\vec{b} = (1)(1) + (1)(0) + (0)(1) = 1 $$

$$ |\vec{a}| = \sqrt{1+1+0} = \sqrt{2}, \qquad |\vec{b}| = \sqrt{1+0+1} = \sqrt{2} $$

$$ \cos\theta = \frac{1}{\sqrt{2}\cdot\sqrt{2}} = \frac{1}{2} $$

Hence $\theta = 60^{\circ}$.
:::

::: example Worked example 14.12
**Problem.** (a) Find the projection of $\vec{b} = 2\hat{i}+3\hat{j}+2\hat{k}$ on
$\vec{a} = \hat{i}+2\hat{j}+2\hat{k}$. (b) Find $\lambda$ if
$2\hat{i}+\lambda\hat{j}+\hat{k}$ is perpendicular to $\hat{i}-2\hat{j}+3\hat{k}$.

**Solution.**

(a) $\vec{a}\cdot\vec{b} = (1)(2)+(2)(3)+(2)(2) = 2+6+4 = 12$ and
$|\vec{a}| = \sqrt{1+4+4} = 3$, so

$$ \text{projection} = \frac{\vec{a}\cdot\vec{b}}{|\vec{a}|} = \frac{12}{3} = 4 \text{ units} $$

(b) Perpendicular means the dot product is zero:

$$ (2)(1) + (\lambda)(-2) + (1)(3) = 0 \;\Rightarrow\; 2 - 2\lambda + 3 = 0 \;\Rightarrow\; \lambda = \frac{5}{2} $$
:::

::: derivation The diagonals of a rhombus are perpendicular
Let $OABC$ be a rhombus with $\vec{OA} = \vec{a}$ and $\vec{OC} = \vec{b}$. All
sides are equal, so $|\vec{a}| = |\vec{b}|$.

The diagonals are $\vec{OB} = \vec{a}+\vec{b}$ and $\vec{CA} = \vec{a}-\vec{b}$.
Take their dot product and expand using the distributive law:

$$ (\vec{a}+\vec{b})\cdot(\vec{a}-\vec{b}) = \vec{a}\cdot\vec{a} - \vec{a}\cdot\vec{b} + \vec{b}\cdot\vec{a} - \vec{b}\cdot\vec{b} $$

The two middle terms cancel because the dot product is commutative, leaving

$$ = |\vec{a}|^{2} - |\vec{b}|^{2} = 0 \qquad (\text{since } |\vec{a}| = |\vec{b}|) $$

A zero dot product between two non-zero vectors means they are perpendicular.
Hence the diagonals of a rhombus cut at right angles. (The same calculation run
backwards shows that if the diagonals of a parallelogram are perpendicular, it
must be a rhombus.)
:::

## Chapter summary

- A vector needs magnitude and direction; in components
  $\vec{r} = x\hat{i}+y\hat{j}+z\hat{k}$ with $|\vec{r}| = \sqrt{x^{2}+y^{2}+z^{2}}$,
  unit vector $\hat{r} = \vec{r}/|\vec{r}|$, and direction cosines satisfying
  $l^{2}+m^{2}+n^{2} = 1$.
- Triangle law: $\vec{AB}+\vec{BC} = \vec{AC}$. For two vectors at angle $\theta$,
  $R = \sqrt{a^{2}+b^{2}+2ab\cos\theta}$ and $\tan\alpha = \dfrac{b\sin\theta}{a+b\cos\theta}$.
- $\vec{AB} = \vec{b}-\vec{a}$ (head minus tail) — the key to every proof.
- Collinear: $\vec{a} = k\vec{b}$; points $A,B,C$ collinear if $\vec{BC} = k\,\vec{AB}$.
- Section formula: internal $\vec{r} = \dfrac{m\vec{b}+n\vec{a}}{m+n}$, external
  $\vec{r} = \dfrac{m\vec{b}-n\vec{a}}{m-n}$, midpoint $\dfrac{\vec{a}+\vec{b}}{2}$.
- Coplanar: $\vec{c} = x\vec{a}+y\vec{b}$; two non-collinear vectors span a plane and
  three non-coplanar vectors span space, with **unique** coefficients.
- Linearly dependent means $c_1\vec{a}_1+\cdots+c_n\vec{a}_n = \vec{0}$ with the
  $c_i$ not all zero. Two vectors: dependent $=$ collinear. Three: dependent $=$ coplanar.
- $\vec{a}\cdot\vec{b} = |\vec{a}||\vec{b}|\cos\theta = a_1b_1+a_2b_2+a_3b_3$;
  $\vec{a}\cdot\vec{b} = 0 \Leftrightarrow$ perpendicular; projection of $\vec{b}$ on $\vec{a}$
  is $\vec{a}\cdot\vec{b}/|\vec{a}|$.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. Two non-zero vectors $\vec{a}$ and $\vec{b}$ are collinear if <span class="marks">[1]</span>
   (a) $\vec{a}\cdot\vec{b} = 0$ (b) $\vec{a} = k\vec{b}$ (c) $|\vec{a}| = |\vec{b}|$ (d) $\vec{a}+\vec{b} = \vec{0}$
2. The position vector of the midpoint of the join of $A(\vec{a})$ and $B(\vec{b})$ is <span class="marks">[1]</span>
   (a) $\vec{b}-\vec{a}$ (b) $\dfrac{\vec{a}+\vec{b}}{2}$ (c) $\dfrac{\vec{b}-\vec{a}}{2}$ (d) $\vec{a}+\vec{b}$
3. The vectors $\hat{i}+\hat{j}$, $\hat{j}+\hat{k}$, $\hat{k}+\hat{i}$ are <span class="marks">[1]</span>
   (a) collinear (b) coplanar (c) linearly dependent (d) linearly independent
4. A unit vector along $3\hat{i}-4\hat{j}$ is <span class="marks">[1]</span>
   (a) $\dfrac{3\hat{i}-4\hat{j}}{5}$ (b) $\dfrac{3\hat{i}-4\hat{j}}{7}$ (c) $3\hat{i}-4\hat{j}$ (d) $\dfrac{3\hat{i}-4\hat{j}}{25}$
5. If $\vec{a}\cdot\vec{b} = 0$ and neither vector is $\vec{0}$, then the angle between them is <span class="marks">[1]</span>
   (a) $0^{\circ}$ (b) $45^{\circ}$ (c) $90^{\circ}$ (d) $180^{\circ}$
6. Any four vectors in three-dimensional space are <span class="marks">[1]</span>
   (a) always linearly independent (b) always linearly dependent (c) always collinear (d) never coplanar

::: note Answers to Group A
**1.** (b) — parallel vectors are scalar multiples of one another.
**2.** (b) — put $m = n = 1$ in the section formula.
**3.** (d) — Worked example 14.9 showed the only solution of $x\vec{a}+y\vec{b}+z\vec{c}=\vec{0}$ is $x=y=z=0$.
**4.** (a) — $|3\hat{i}-4\hat{j}| = \sqrt{9+16} = 5$, and $\hat{a} = \vec{a}/|\vec{a}|$.
**5.** (c) — $\cos\theta = 0$ gives $\theta = 90^{\circ}$.
**6.** (b) — space has dimension 3, so three vectors at most can be independent; a fourth is always a combination of the others.
:::

**Group B — Short answer (5 marks each)**

1. Define collinear vectors. Prove that the points $A(-2,3,5)$, $B(1,2,3)$ and
   $C(7,0,-1)$ are collinear, and find the ratio $AB:BC$. <span class="marks">[5]</span>
2. Find the position vector of the point $P$ which divides the join of
   $A(2,-1,4)$ and $B(7,4,-1)$ internally in the ratio $3:2$. <span class="marks">[5]</span>
3. Express $\vec{c} = 7\hat{i}+4\hat{j}$ as a linear combination of
   $\vec{a} = \hat{i}+2\hat{j}$ and $\vec{b} = 2\hat{i}-\hat{j}$, and explain why the
   answer is unique. <span class="marks">[5]</span>
4. Show that the vectors $\hat{i}-2\hat{j}+3\hat{k}$, $-2\hat{i}+3\hat{j}-4\hat{k}$ and
   $\hat{i}-3\hat{j}+5\hat{k}$ are coplanar. <span class="marks">[5]</span>
5. If $\vec{a} = 2\hat{i}+\lambda\hat{j}+\hat{k}$ is perpendicular to
   $\vec{b} = \hat{i}-2\hat{j}+3\hat{k}$, find $\lambda$. Hence find the projection of
   $\vec{b}$ on $\hat{i}-2\hat{j}+2\hat{k}$. <span class="marks">[5]</span>
6. Two vectors of magnitudes $7$ and $8$ units act at a point at $60^{\circ}$ to each
   other. Find the magnitude of the resultant and the angle it makes with the
   $8$-unit vector. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Collinear vectors lie on the same or parallel lines, so each is a scalar
multiple of the other. Here
$\vec{AB} = (1+2)\hat{i}+(2-3)\hat{j}+(3-5)\hat{k} = 3\hat{i}-\hat{j}-2\hat{k}$ and
$\vec{BC} = (7-1)\hat{i}+(0-2)\hat{j}+(-1-3)\hat{k} = 6\hat{i}-2\hat{j}-4\hat{k}$.
Since $\vec{BC} = 2\,\vec{AB}$, the vectors are collinear; they share $B$, so
$A$, $B$, $C$ lie on one line. Also $AB:BC = 1:2$.

**2.** With $m = 3$, $n = 2$:
$\vec{r} = \dfrac{3(7\hat{i}+4\hat{j}-\hat{k}) + 2(2\hat{i}-\hat{j}+4\hat{k})}{5}
= \dfrac{(21+4)\hat{i}+(12-2)\hat{j}+(-3+8)\hat{k}}{5} = \dfrac{25\hat{i}+10\hat{j}+5\hat{k}}{5}
= 5\hat{i}+2\hat{j}+\hat{k}$, i.e. $P(5,2,1)$. It lies between $A$ and $B$, as required.

**3.** Let $\vec{c} = x\vec{a}+y\vec{b}$. Then $x+2y = 7$ and $2x-y = 4$. From the
second, $y = 2x-4$; substituting, $x + 4x - 8 = 7$, so $5x = 15$, $x = 3$ and
$y = 2$. Hence $\vec{c} = 3\vec{a}+2\vec{b}$ (check:
$3\hat{i}+6\hat{j}+4\hat{i}-2\hat{j} = 7\hat{i}+4\hat{j}$ ✔). It is unique because
$\vec{a}$ and $\vec{b}$ are non-collinear, so they form a basis of the plane
(uniqueness proof in §14.3).

**4.** Let $\vec{c} = x\vec{a}+y\vec{b}$ with $\vec{a} = (1,-2,3)$,
$\vec{b} = (-2,3,-4)$, $\vec{c} = (1,-3,5)$. The equations are
$x-2y = 1$, $-2x+3y = -3$, $3x-4y = 5$. From the first, $x = 1+2y$; the second
gives $-2-4y+3y = -3$, so $y = 1$ and $x = 3$. The third is satisfied:
$3(3)-4(1) = 5$ ✔. Therefore $\vec{c} = 3\vec{a}+\vec{b}$ and the vectors are coplanar.

**5.** Perpendicularity gives $2(1)+\lambda(-2)+1(3) = 0$, so $5 = 2\lambda$ and
$\lambda = 5/2$. For the projection, $\vec{b}\cdot(\hat{i}-2\hat{j}+2\hat{k})
= 1+4+6 = 11$ and $|\hat{i}-2\hat{j}+2\hat{k}| = \sqrt{1+4+4} = 3$, so the
projection is $11/3 = 3.67$ units.

**6.** $R = \sqrt{8^{2}+7^{2}+2(8)(7)\cos 60^{\circ}} = \sqrt{64+49+56} = \sqrt{169} = 13$ units.
Measuring $\alpha$ from the $8$-unit vector,
$\tan\alpha = \dfrac{7\sin 60^{\circ}}{8+7\cos 60^{\circ}} = \dfrac{6.062}{11.5} = 0.5272$,
so $\alpha = 27.80^{\circ}$.
:::

**Group C — Long answer (8 marks each)**

1. (a) State and prove the section formula for the internal division of a line
   segment in the ratio $m:n$, and deduce the midpoint formula. <span class="marks">[4]</span>
   (b) Find the points dividing the join of $A(1,-2,3)$ and $B(4,7,-6)$ in the
   ratio $2:1$ internally and externally. <span class="marks">[4]</span>
2. (a) Define a linear combination of vectors, and linearly dependent and
   linearly independent vectors. <span class="marks">[3]</span>
   (b) Show that $\hat{i}+\hat{j}$, $\hat{j}+\hat{k}$ and $\hat{k}+\hat{i}$ are
   linearly independent, and express $3\hat{i}+5\hat{j}+4\hat{k}$ as a linear
   combination of them. <span class="marks">[5]</span>
3. (a) Prove by vector methods that the diagonals of a parallelogram bisect each
   other. <span class="marks">[4]</span>
   (b) Prove by vector methods that the line joining the midpoints of two sides of
   a triangle is parallel to the third side and half its length. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** (a) See the derivation in §14.1: from $AP:PB = m:n$ we get
$n\,\vec{AP} = m\,\vec{PB}$, i.e. $n(\vec{r}-\vec{a}) = m(\vec{b}-\vec{r})$, which
rearranges to $\vec{r} = \dfrac{m\vec{b}+n\vec{a}}{m+n}$. Putting $m = n = 1$ gives
the midpoint $\dfrac{\vec{a}+\vec{b}}{2}$.

(b) With $\vec{a} = \hat{i}-2\hat{j}+3\hat{k}$, $\vec{b} = 4\hat{i}+7\hat{j}-6\hat{k}$,
$m = 2$, $n = 1$:

Internal: $\vec{r} = \dfrac{2\vec{b}+\vec{a}}{3} = \dfrac{(8+1)\hat{i}+(14-2)\hat{j}+(-12+3)\hat{k}}{3}
= \dfrac{9\hat{i}+12\hat{j}-9\hat{k}}{3} = 3\hat{i}+4\hat{j}-3\hat{k}$, i.e. $(3,4,-3)$.

External: $\vec{r} = \dfrac{2\vec{b}-\vec{a}}{2-1} = (8-1)\hat{i}+(14+2)\hat{j}+(-12-3)\hat{k}
= 7\hat{i}+16\hat{j}-15\hat{k}$, i.e. $(7,16,-15)$.

**2.** (a) Definitions as in §14.3 and §14.4.

(b) Independence: from $x(\hat{i}+\hat{j})+y(\hat{j}+\hat{k})+z(\hat{k}+\hat{i}) = \vec{0}$
we get $x+z = 0$, $x+y = 0$, $y+z = 0$. Adding gives $x+y+z = 0$, and subtracting
each equation in turn gives $y = 0$, $z = 0$, $x = 0$. Only the trivial solution
exists, so the vectors are linearly independent.

For the combination, let $x(\hat{i}+\hat{j})+y(\hat{j}+\hat{k})+z(\hat{k}+\hat{i})
= 3\hat{i}+5\hat{j}+4\hat{k}$. Then

$$ x+z = 3, \qquad x+y = 5, \qquad y+z = 4 $$

Adding, $2(x+y+z) = 12$, so $x+y+z = 6$. Subtracting each equation from this:
$y = 6-3 = 3$, $z = 6-5 = 1$, $x = 6-4 = 2$. Hence
$3\hat{i}+5\hat{j}+4\hat{k} = 2(\hat{i}+\hat{j}) + 3(\hat{j}+\hat{k}) + (\hat{k}+\hat{i})$,
which checks out componentwise.

**3.** (a) Let $OACB$ be a parallelogram with $\vec{OA} = \vec{a}$,
$\vec{OB} = \vec{b}$, so $\vec{OC} = \vec{a}+\vec{b}$. The midpoint of the diagonal
$OC$ has position vector $\dfrac{\vec{a}+\vec{b}}{2}$. The midpoint of the other
diagonal $AB$ has position vector $\dfrac{\vec{a}+\vec{b}}{2}$ as well. The two
midpoints coincide, so each diagonal bisects the other.

(b) In triangle $OAB$ let $\vec{OA} = \vec{a}$, $\vec{OB} = \vec{b}$, and let $M$,
$N$ be the midpoints of $OA$ and $OB$, so $\vec{m} = \vec{a}/2$ and
$\vec{n} = \vec{b}/2$. Then

$$ \vec{MN} = \vec{n}-\vec{m} = \frac{\vec{b}-\vec{a}}{2} = \frac{1}{2}\vec{AB} $$

Since $\vec{MN}$ is a scalar multiple of $\vec{AB}$, the two are parallel, and
taking magnitudes, $MN = \frac{1}{2}AB$.
:::
