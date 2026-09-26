---
subject: Physics
grade: 11
unit: 19
title: Electric Charges
hours: 3
area: Electricity and Magnetism
---

Rub a plastic comb on dry hair in winter and it picks up small pieces of paper.
That small experiment contains the whole of this unit: charge can be separated,
it comes in two kinds, and charges exert forces on one another across empty
space. Everything in the rest of electricity — fields, potential, capacitors,
circuits — is built on the inverse-square force law we meet here.

::: key What this unit is really about
One law, $F = \dfrac{1}{4\pi\varepsilon_0}\dfrac{q_1q_2}{r^{2}}$, plus one
principle, superposition. Most Group B numericals are just these two applied to
two or three charges with careful attention to **direction**.
:::

## 19.1 Electric charges

::: definition Electric charge
Electric charge is the intrinsic property of matter because of which it
experiences and exerts electrostatic force. There are two kinds, called
**positive** and **negative** (the names are due to Benjamin Franklin).
Like charges repel; unlike charges attract.
:::

A neutral atom has equal numbers of protons and electrons. Charging a body means
**transferring electrons** — never protons, which are locked in the nucleus. A
body that has lost electrons is positively charged; one that has gained electrons
is negatively charged.

### Properties of charge

| Property | Statement |
|---|---|
| Quantisation | Charge exists only in integral multiples of the elementary charge: $q = \pm ne$, with $e = 1.6\times10^{-19}\ \text{C}$ and $n = 1,2,3,\dots$ |
| Conservation | The total charge of an isolated system never changes; charge can only be transferred, not created or destroyed |
| Additivity | Charge is a scalar; total charge is the **algebraic** sum of the individual charges |
| Invariance | The charge on a body does not change with its speed, unlike its mass |

The SI unit of charge is the **coulomb** (C): the charge carried past a point in
one second by a steady current of one ampere, so $1\ \text{C} = 1\ \text{A s}$.
One coulomb is an enormous charge — it corresponds to

$$ n = \frac{1}{1.6\times10^{-19}} = 6.25\times10^{18}\ \text{electrons} $$

which is why laboratory charges are usually quoted in microcoulombs
($1\ \mu\text{C} = 10^{-6}\ \text{C}$) or nanocoulombs.

### Conductors and insulators

| | Conductor | Insulator (dielectric) |
|---|---|---|
| Free electrons | many | practically none |
| Charge given to it | spreads over the whole outer surface | stays where it is put |
| Examples | metals, graphite, human body, earth, salt solutions | glass, dry wood, ebonite, plastic, dry air |

Three ways of charging a body: by **friction** (rubbing glass with silk, ebonite
with fur), by **conduction** (touching it with an already charged body — it gains
charge of the *same* sign), and by **induction** (§19.2 — it gains charge of the
*opposite* sign).

```figure caption="Gold-leaf electroscope. Charge given to the disc spreads down the rod to the leaves, which repel each other and diverge; the divergence measures the charge."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
fig, ax = plt.subplots(figsize=(4.2,3.6))

# glass vessel
ax.add_patch(Rectangle((-1.05,-1.95), 2.10, 2.55, facecolor='#eaf1f8',
                       edgecolor=INK, lw=1.6, zorder=1))
ax.annotate('glass\nvessel', (1.46, -0.36), ha='left', color=MUTED, fontsize=8.2)
ax.annotate('', xy=(1.07,-0.60), xytext=(1.42,-0.50),
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=0.9, mutation_scale=8))

# insulating stopper
ax.add_patch(Rectangle((-0.42, 0.60), 0.84, 0.26, facecolor='#d9c8a9',
                       edgecolor=INK, lw=1.3, zorder=3))
ax.annotate('insulating plug', (0.52, 0.72), ha='left', color=MUTED, fontsize=8.2)

# metal rod and disc
ax.plot([0,0], [-0.95, 1.30], color=INK, lw=3.4, zorder=4)
ax.add_patch(Rectangle((-0.62, 1.30), 1.24, 0.13, facecolor=MUTED,
                       edgecolor=INK, lw=1.3, zorder=5))
ax.annotate('metal disc (cap)', (0.70, 1.47), ha='center', color=INK, fontsize=8.4)
ax.annotate('metal rod', (-0.14, 0.20), ha='right', color=INK, fontsize=8.4)

# gold leaves, diverging
for sx in (-1, 1):
    ax.plot([0, sx*0.46], [-0.95, -1.72], color='#b8860b', lw=3.0, zorder=4)
ax.annotate('gold leaves', (1.18, -1.88), ha='left', color='#b8860b', fontsize=8.4)
ax.annotate('', xy=(0.50,-1.74), xytext=(1.12,-1.86),
            arrowprops=dict(arrowstyle='-|>', color='#b8860b', lw=0.9, mutation_scale=8))

# charge symbols
for x, y in [(-0.36,1.36),(-0.12,1.36),(0.12,1.36),(0.36,1.36),
             (-0.42,-1.30),(0.42,-1.30),(-0.58,-1.62),(0.58,-1.62)]:
    ax.annotate('+', (x,y), ha='center', va='center', color='#c0392b', fontsize=10.5,
                zorder=6)

# repulsion arrows
ax.annotate('', xy=(-0.80,-1.45), xytext=(-0.50,-1.45),
            arrowprops=dict(arrowstyle='-|>', color='#c0392b', lw=1.3, mutation_scale=10))
ax.annotate('', xy=(0.80,-1.45), xytext=(0.50,-1.45),
            arrowprops=dict(arrowstyle='-|>', color='#c0392b', lw=1.3, mutation_scale=10))

# earthed case
ax.plot([-1.05,-1.35],[-1.30,-1.30], color=MUTED, lw=1.2)
for k,w in enumerate([0.22,0.15,0.08]):
    ax.plot([-1.35-w/2,-1.35+w/2],[-1.42-0.09*k,-1.42-0.09*k], color=MUTED, lw=1.6)
ax.plot([-1.35,-1.35],[-1.30,-1.42], color=MUTED, lw=1.2)
ax.annotate('earthed\nmetal foil', (-1.52,-0.98), ha='center', color=MUTED, fontsize=7.8)

ax.set_xlim(-2.15, 2.30); ax.set_ylim(-2.25, 1.85)
ax.set_aspect('equal'); ax.axis('off')
```

::: example Worked example 19.1
**Problem.** A polythene rod acquires a charge of $-3.2\ \mu\text{C}$ when rubbed
with wool. (a) How many electrons has it gained? (b) What is the charge on the
wool? (c) By how much has the mass of the rod changed?
Take $e = 1.6\times10^{-19}\ \text{C}$ and $m_e = 9.1\times10^{-31}\ \text{kg}$.

**Solution.**

(a) By quantisation, $q = ne$, so

$$ n = \frac{q}{e} = \frac{3.2\times10^{-6}}{1.6\times10^{-19}} = 2\times10^{13}\ \text{electrons} $$

(b) By conservation of charge the wool must carry $+3.2\ \mu\text{C}$: the
electrons were transferred from the wool to the rod, nothing was created.

(c) The rod gains the mass of those electrons:

$$ \Delta m = n\,m_e = 2\times10^{13} \times 9.1\times10^{-31}
 = 1.82\times10^{-17}\ \text{kg} $$

— utterly unmeasurable, which is why we treat charging as a mass-free process.
:::

## 19.2 Charging by induction

A charged body can produce a charge in a neutral conductor **without touching
it**. The process is called electrostatic induction and it depends on the free
electrons of the conductor being able to move.

```figure caption="Charging a metal sphere positively by induction with a negatively charged rod. The sphere ends up with a charge opposite to that of the rod, and the rod itself loses nothing."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
fig, axs = plt.subplots(2, 2, figsize=(5.0,4.4))
axs = axs.ravel()

def sphere(ax, plus, minus, rod=True, earth=False):
    ax.add_patch(Circle((0,0), 1.0, facecolor='#eaf1f8', edgecolor=INK, lw=1.5))
    ax.plot([-0.24,0.24],[-1.02,-1.02], color=INK, lw=1.5)
    ax.add_patch(Rectangle((-0.17,-1.62), 0.34, 0.60, facecolor='#d9c8a9',
                           edgecolor=INK, lw=1.1))
    ax.plot([-0.62,0.62],[-1.62,-1.62], color=MUTED, lw=2.0)
    if rod:
        ax.add_patch(Rectangle((-2.70,-0.17), 1.10, 0.34, facecolor='#d9d9d9',
                               edgecolor=INK, lw=1.2))
        for k in range(4):
            ax.annotate('\u2212', (-2.52+0.28*k, 0.0), ha='center', va='center',
                        color=SERIES[0], fontsize=11)
    for th in plus:
        ax.annotate('+', (0.70*np.cos(th), 0.70*np.sin(th)), ha='center',
                    va='center', color='#c0392b', fontsize=11)
    for th in minus:
        ax.annotate('\u2212', (0.70*np.cos(th), 0.70*np.sin(th)), ha='center',
                    va='center', color=SERIES[0], fontsize=11)
    if earth:
        ax.plot([1.0,1.80],[0,0], color=MUTED, lw=1.3)
        ax.plot([1.80,1.80],[0,-0.60], color=MUTED, lw=1.3)
        for k,w in enumerate([0.40,0.27,0.14]):
            ax.plot([1.80-w/2,1.80+w/2],[-0.60-0.17*k]*2, color=MUTED, lw=1.8)
        ax.annotate('', xy=(1.72,-0.30), xytext=(1.20,-0.30),
                    arrowprops=dict(arrowstyle='-|>', color=SERIES[0], lw=1.2,
                                    mutation_scale=9))
    ax.set_xlim(-2.95, 2.45); ax.set_ylim(-3.25, 1.35)
    ax.set_aspect('equal'); ax.axis('off')

L = [np.pi*0.80, np.pi*1.0, np.pi*1.20]        # near (left) face
R = [np.pi*0.20, 0.0, -np.pi*0.20]             # far  (right) face

sphere(axs[0], L, R)
axs[0].annotate('1. rod brought near\nnear face $+$, far face $-$',
                (-0.25,-1.95), ha='center', va='top', fontsize=8.0, color=INK)
sphere(axs[1], L, [], earth=True)
axs[1].annotate('2. far side earthed\nelectrons run to earth',
                (-0.25,-1.95), ha='center', va='top', fontsize=8.0, color=INK)
sphere(axs[2], L, [])
axs[2].annotate('3. earth removed first,\nrod still in place',
                (-0.25,-1.95), ha='center', va='top', fontsize=8.0, color=INK)
sphere(axs[3], [np.pi*0.25, np.pi*0.75, np.pi*1.25, np.pi*1.75], [], rod=False)
axs[3].annotate('4. rod removed\n$+$ spreads uniformly',
                (-0.25,-1.95), ha='center', va='top', fontsize=8.0, color=INK)
fig.subplots_adjust(hspace=0.02, wspace=0.02)
```
The four steps, in the order the examiner wants them:

1. **Bring the charged rod near.** The free electrons of the sphere are repelled
   by the negative rod and collect on the far face, leaving the near face
   positive. The sphere as a whole is still neutral.
2. **Earth the sphere** (touch the far side, or connect it to earth). Electrons
   on the far face are pushed down to earth. The near-face positive charge stays,
   held by the attraction of the rod.
3. **Remove the earth connection first**, while the rod is still in place.
4. **Remove the rod.** The positive charge, no longer bound, spreads uniformly
   over the sphere.

::: caution Order matters
If you remove the rod *before* breaking the earth connection, electrons flow back
up from the earth and the sphere ends up neutral. In the examination you lose
marks for writing the steps in the wrong order.
:::

Three points to notice:

- The induced charge is **opposite in sign** to the inducing charge.
- The inducing body **loses no charge at all** — the same rod can charge any
  number of spheres.
- The magnitude of the induced charge is at most equal to the inducing charge.

Induction also explains why a charged comb attracts *neutral* bits of paper: the
comb induces an opposite charge on the near face of each piece and a like charge
on the far face. The near charge is closer, so by the inverse-square law the
attraction beats the repulsion and the paper jumps.

## 19.3 Coulomb's law — force between two point charges

Coulomb measured this force in 1785 with a torsion balance.

::: definition Coulomb's law
The force of attraction or repulsion between two stationary point charges is
directly proportional to the product of the magnitudes of the charges, inversely
proportional to the square of the distance between them, and acts along the line
joining them.

$$ F \propto \frac{q_1q_2}{r^{2}}
   \qquad\Longrightarrow\qquad F = k\,\frac{q_1q_2}{r^{2}} $$
:::

```figure caption="Coulomb forces are equal, opposite and directed along the line joining the charges — outwards for like charges, inwards for unlike charges."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle
fig, (a1, a2) = plt.subplots(2, 1, figsize=(5.0,2.7))

def pair(ax, s1, s2, outward, title):
    ax.plot([-1.3,1.3],[0,0], color=GRID, lw=1.0, ls=':')
    for x, s in ((-1.3,s1), (1.3,s2)):
        c = '#c0392b' if s=='+' else SERIES[0]
        ax.add_patch(Circle((x,0), 0.26, facecolor=c, alpha=0.18,
                            edgecolor=c, lw=1.3))
        ax.annotate(s, (x,0.02), ha='center', va='center', color=c, fontsize=13)
    ax.annotate('$q_1$', (-1.3,0.40), ha='center', color=INK, fontsize=9.2)
    ax.annotate('$q_2$', ( 1.3,0.40), ha='center', color=INK, fontsize=9.2)
    d = 1 if outward else -1
    ax.annotate('', xy=(-1.3-d*0.95, 0), xytext=(-1.3-d*0.30, 0),
                arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.9, mutation_scale=13))
    ax.annotate('', xy=( 1.3+d*0.95, 0), xytext=( 1.3+d*0.30, 0),
                arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.9, mutation_scale=13))
    xf1 = -1.3-d*0.62; xf2 = 1.3+d*0.62
    ax.annotate(r'$\vec{F}_{12}$', (xf1, 0.30), ha='center', color=INK, fontsize=9.2)
    ax.annotate(r'$\vec{F}_{21}$', (xf2, 0.30), ha='center', color=INK, fontsize=9.2)
    ax.annotate('', xy=(1.04,-0.46), xytext=(-1.04,-0.46),
                arrowprops=dict(arrowstyle='<|-|>', color=MUTED, lw=0.9, mutation_scale=8))
    ax.annotate('$r$', (0,-0.70), ha='center', color=MUTED, fontsize=9.2)
    ax.annotate(title, (0.0,0.86), ha='center', va='center', color=INK, fontsize=8.8)
    ax.set_xlim(-2.60, 2.60); ax.set_ylim(-0.95, 1.10)
    ax.set_aspect('equal'); ax.axis('off')

pair(a1, '+', '+', True,  'Like charges: repulsion')
pair(a2, '+', '\u2212', False, 'Unlike charges: attraction')
fig.subplots_adjust(hspace=0.05)
```

In SI units the constant is written $k = \dfrac{1}{4\pi\varepsilon_0}$, so

$$ F = \frac{1}{4\pi\varepsilon_0}\cdot\frac{q_1q_2}{r^{2}} $$

where $\varepsilon_0 = 8.85\times10^{-12}\ \text{C}^2\text{N}^{-1}\text{m}^{-2}$
is the **permittivity of free space** and

$$ k = \frac{1}{4\pi\varepsilon_0} = 9\times10^{9}\ \text{N m}^{2}\text{C}^{-2} $$

::: definition The coulomb, defined from Coulomb's law
One coulomb is that charge which, placed $1\ \text{m}$ from an equal charge in
vacuum, repels it with a force of $9\times10^{9}\ \text{N}$.
:::

**In a material medium** of relative permittivity (dielectric constant)
$\varepsilon_r$,

$$ F_{med} = \frac{1}{4\pi\varepsilon_0\varepsilon_r}\cdot\frac{q_1q_2}{r^{2}}
 = \frac{F_{vac}}{\varepsilon_r},
\qquad \varepsilon_r = \frac{F_{vac}}{F_{med}} $$

so a medium always **weakens** the force ($\varepsilon_r \ge 1$; for water
$\varepsilon_r \approx 80$).

**Vector form.** If $\hat{r}_{21}$ is the unit vector pointing from charge 1 to
charge 2, the force **on** $q_2$ **due to** $q_1$ is

$$ \vec{F}_{21} = \frac{1}{4\pi\varepsilon_0}\cdot\frac{q_1q_2}{r^{2}}\,\hat{r}_{21} $$

Substituting signed values of the charges automatically gives the right
direction: $q_1q_2 > 0$ (like charges) makes $\vec{F}_{21}$ point along
$\hat{r}_{21}$, i.e. away from $q_1$. Newton's third law holds:
$\vec{F}_{12} = -\vec{F}_{21}$.

| | Coulomb force | Gravitational force |
|---|---|---|
| Depends on | product of charges | product of masses |
| Distance dependence | $1/r^{2}$ | $1/r^{2}$ |
| Sign | attractive or repulsive | always attractive |
| Affected by medium | yes, reduced by $\varepsilon_r$ | no |
| Relative strength | about $10^{36}$ times stronger | very weak |

::: example Worked example 19.2
**Problem.** Two point charges of $+2\ \mu\text{C}$ and $-3\ \mu\text{C}$ are
placed $30\ \text{cm}$ apart in air. (a) Find the force between them. (b) What
would the force become if the charges were immersed in a liquid of dielectric
constant $4$ at the same separation?

**Solution.**

(a) $q_1 = 2\times10^{-6}\ \text{C}$, $q_2 = 3\times10^{-6}\ \text{C}$,
$r = 0.30\ \text{m}$.

$$ F = \frac{9\times10^{9}\times(2\times10^{-6})\times(3\times10^{-6})}{(0.30)^{2}}
 = \frac{9\times10^{9}\times 6\times10^{-12}}{0.09} $$

$$ F = \frac{5.4\times10^{-2}}{0.09} = 0.6\ \text{N} $$

Since the charges are unlike, the force is one of **attraction**.

(b) $F_{med} = F_{vac}/\varepsilon_r = 0.6/4 = 0.15\ \text{N}$, still attractive.
:::

::: example Worked example 19.3
**Problem.** Compare the electrostatic and gravitational forces between two
protons. Take $e = 1.6\times10^{-19}\ \text{C}$,
$m_p = 1.67\times10^{-27}\ \text{kg}$ and
$G = 6.67\times10^{-11}\ \text{N m}^{2}\text{kg}^{-2}$.

**Solution.** Both forces vary as $1/r^{2}$, so the separation cancels in the
ratio:

$$ \frac{F_e}{F_g} = \frac{k e^{2}/r^{2}}{G m_p^{2}/r^{2}} = \frac{k e^{2}}{G m_p^{2}} $$

Numerator: $9\times10^{9} \times (1.6\times10^{-19})^{2}
= 9\times10^{9} \times 2.56\times10^{-38} = 2.304\times10^{-28}$.

Denominator: $6.67\times10^{-11} \times (1.67\times10^{-27})^{2}
= 6.67\times10^{-11} \times 2.789\times10^{-54} = 1.860\times10^{-64}$.

$$ \frac{F_e}{F_g} = \frac{2.304\times10^{-28}}{1.860\times10^{-64}}
 \approx 1.24\times10^{36} $$

Gravity is utterly negligible inside an atom — which is why we ignore it in every
electrostatics problem.
:::

## 19.4 Force between multiple electric charges

::: definition Principle of superposition
The force exerted on a charge by another charge is **unaffected** by the presence
of any other charges. The resultant force on any one charge is therefore the
**vector sum** of the forces exerted on it by each of the other charges taken one
at a time:

$$ \vec{F}_1 = \vec{F}_{12} + \vec{F}_{13} + \cdots + \vec{F}_{1n} $$
:::

Written out for $n$ charges,

$$ \vec{F}_1 = \frac{q_1}{4\pi\varepsilon_0}\sum_{j=2}^{n}\frac{q_j}{r_{1j}^{2}}\,\hat{r}_{1j} $$

where $\hat{r}_{1j}$ is the unit vector pointing from $q_j$ towards $q_1$, in
keeping with the notation of §19.3. For two forces $F_a$ and $F_b$ with angle
$\theta$ between them, the parallelogram law gives

$$ F = \sqrt{F_a^{2} + F_b^{2} + 2F_aF_b\cos\theta} $$

```figure caption="Superposition. The two Coulomb forces on $q_1$ are combined by the parallelogram law; for three equal charges at the corners of an equilateral triangle the resultant is $\sqrt{3}F$ directed away from the centroid."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle
fig, ax = plt.subplots(figsize=(4.4,4.3))

A = np.array([0.0, 1.732]); B = np.array([-1.0, 0.0]); C = np.array([1.0, 0.0])

for P, lab, off in ((A,'$q_1$',(-0.34,-0.04)), (B,'$q_2$',(-0.30,-0.30)),
                    (C,'$q_3$',(0.30,-0.30))):
    ax.add_patch(Circle(P, 0.16, facecolor='#c0392b', alpha=0.20,
                        edgecolor='#c0392b', lw=1.3, zorder=4))
    ax.annotate('+', P, ha='center', va='center', color='#c0392b',
                fontsize=11, zorder=5)
    ax.annotate(lab, P+np.array(off), ha='center', color=INK, fontsize=9.2)

for P, Q in ((A,B), (A,C), (B,C)):
    ax.plot([P[0],Q[0]],[P[1],Q[1]], color=GRID, lw=1.1, ls=(0,(4,3)), zorder=1)
ax.annotate('$r$', (0.0,-0.28), ha='center', color=MUTED, fontsize=9.2)

L = 0.90
u12 = (A-B)/np.linalg.norm(A-B)        # force on q1 due to q2 : away from q2
u13 = (A-C)/np.linalg.norm(A-C)
F12 = A + L*u12
F13 = A + L*u13
R   = A + L*(u12+u13)

for tip, lab, off in ((F12, r'$\vec{F}_{12}$', ( 0.36,0.08)),
                      (F13, r'$\vec{F}_{13}$', (-0.36,0.08))):
    ax.annotate('', xy=tip, xytext=A,
                arrowprops=dict(arrowstyle='-|>', color=SERIES[0], lw=1.8,
                                shrinkA=0, shrinkB=0, mutation_scale=13))
    ax.annotate(lab, tip+np.array(off), ha='center', color=SERIES[0], fontsize=9.0)
ax.annotate('', xy=R, xytext=A,
            arrowprops=dict(arrowstyle='-|>', color='#c0392b', lw=2.1,
                            shrinkA=0, shrinkB=0, mutation_scale=14))
ax.annotate(r'$F=\sqrt{3}\,F_{12}$', R+np.array([0.10,0.16]), ha='center',
            color='#c0392b', fontsize=9.0)
ax.plot([F12[0],R[0]],[F12[1],R[1]], color=MUTED, lw=0.9, ls=(0,(3,2)), zorder=2)
ax.plot([F13[0],R[0]],[F13[1],R[1]], color=MUTED, lw=0.9, ls=(0,(3,2)), zorder=2)
th = np.linspace(np.pi/3, 2*np.pi/3, 60)
ax.plot(A[0]+0.52*np.cos(th), A[1]+0.52*np.sin(th), color=MUTED, lw=0.9)
ax.annotate(r'$60^\circ$', A+np.array([0.60,0.38]), ha='left',
            color=MUTED, fontsize=8.4)
ax.set_xlim(-2.05, 2.05); ax.set_ylim(-0.60, 3.75)
ax.set_aspect('equal'); ax.axis('off')
```

::: tip A reliable method for superposition numericals
1. Draw the charges and mark each force **on** the chosen charge with an arrow,
   using only the *signs* to decide the direction.
2. Compute each magnitude from $F = kq_1q_2/r^{2}$, ignoring signs.
3. Resolve into $x$ and $y$ components, add, then recombine with
   $F = \sqrt{F_x^{2}+F_y^{2}}$ and $\tan\alpha = F_y/F_x$.
:::

::: example Worked example 19.4
**Problem.** Three charges of $+2\ \mu\text{C}$ each are fixed at the corners of
an equilateral triangle of side $20\ \text{cm}$. Find the magnitude and direction
of the resultant force on any one of them.

**Solution.** Each pair gives the same magnitude of force, with
$q = 2\times10^{-6}\ \text{C}$ and $r = 0.20\ \text{m}$:

$$ F_{12} = F_{13} = \frac{9\times10^{9}\times(2\times10^{-6})^{2}}{(0.20)^{2}}
 = \frac{9\times10^{9}\times4\times10^{-12}}{0.04} $$

$$ = \frac{3.6\times10^{-2}}{0.04} = 0.9\ \text{N} $$

Both are repulsive, and the angle between them is $60^{\circ}$. By the
parallelogram law,

$$ F = \sqrt{F_{12}^{2}+F_{13}^{2}+2F_{12}F_{13}\cos 60^{\circ}}
 = F\sqrt{1+1+2(0.5)} = 0.9\sqrt{3} $$

$$ F = 1.56\ \text{N} $$

Because the two forces are equal, the resultant bisects the angle between them,
i.e. it points **directly away from the centroid** of the triangle.
:::

::: caution Never add Coulomb forces as numbers
Forces are vectors. Adding $0.9 + 0.9 = 1.8\ \text{N}$ in the example above is
the single commonest error in this chapter; the correct answer,
$0.9\sqrt{3} = 1.56\ \text{N}$, is smaller because the forces are $60^{\circ}$
apart.
:::

::: derivation Where the resultant force on a third charge is zero
We start from the condition that two Coulomb forces balance, and reach a general formula for the
position of the **null point** between two like charges.

**Setting up.** Charges $q_1$ and $q_2$ are fixed a distance $d$ apart, both of the same sign. A
test charge $q_0$ is placed on the line joining them, a distance $x$ from $q_1$ and so
$(d - x)$ from $q_2$.

**Step 1 — why the point must lie between them.** Only between the two charges do the two forces
on $q_0$ point in opposite directions. Outside, both push the same way and can never cancel. So
$0 < x < d$.

**Step 2 — write the two force magnitudes** from Coulomb's law:

$$ F_1 = \frac{kq_0q_1}{x^{2}}, \qquad F_2 = \frac{kq_0q_2}{(d-x)^{2}} $$

**Step 3 — set them equal.** They already point opposite ways, so equal magnitudes means zero
resultant:

$$ \frac{kq_0q_1}{x^{2}} = \frac{kq_0q_2}{(d-x)^{2}} $$

**Step 4 — cancel $k$ and $q_0$,** which appear on both sides. This is the key moment: the test
charge has vanished, so the answer cannot depend on its size or its sign.

$$ \frac{q_1}{x^{2}} = \frac{q_2}{(d-x)^{2}} $$

**Step 5 — cross-multiply:**

$$ q_1(d-x)^{2} = q_2 x^{2} $$

**Step 6 — divide both sides by $q_2 x^{2}$:**

$$ \frac{q_1}{q_2} = \frac{x^{2}}{(d-x)^{2}} $$

**Step 7 — take the positive square root.** We keep only the positive root because Step 1 tells
us $x$ and $(d-x)$ are both positive:

$$ \sqrt{\frac{q_1}{q_2}} = \frac{x}{d-x} $$

**Step 8 — write $\sqrt{q_1/q_2} = s$ for short, and cross-multiply:**

$$ x = s(d - x) = sd - sx $$

**Step 9 — collect the $x$ terms:**

$$ x + sx = sd $$

**Step 10 — take out $x$ and divide:**

$$ x = \frac{sd}{1+s} = \frac{d\sqrt{q_1}}{\sqrt{q_1}+\sqrt{q_2}} $$

**Result.**

$$ \frac{x}{d-x} = \sqrt{\frac{q_1}{q_2}}, \qquad
x = \frac{d\sqrt{q_1}}{\sqrt{q_1}+\sqrt{q_2}} $$

**What it means.** The distances are in the ratio of the **square roots** of the charges, not the
charges themselves. So the null point always lies **nearer the smaller charge** — it has to be
closer to make up for being weaker. And because $q_0$ cancelled in Step 4, the same point works
for any third charge, positive or negative, large or small.

**Conditions used.** Point charges, both of the **same sign**, and the test point on the straight
line joining them. If the two charges have opposite signs the null point lies outside the pair,
on the far side of the smaller charge, and Step 1 must be redone.
:::

::: example Worked example 19.5
**Problem.** Charges of $+9\ \mu\text{C}$ and $+4\ \mu\text{C}$ are fixed
$50\ \text{cm}$ apart. At what point on the line joining them is the resultant
force on a third charge zero?

**Solution.** Between the two charges the forces on a third charge are in
opposite directions, so the null point lies there. Let it be at a distance $x$
from the $9\ \mu\text{C}$ charge, so that it is $(0.50-x)$ from the
$4\ \mu\text{C}$ charge. For the magnitudes to be equal,

$$ \frac{kq_0(9\ \mu\text{C})}{x^{2}} = \frac{kq_0(4\ \mu\text{C})}{(0.50-x)^{2}} $$

$$ \frac{9}{x^{2}} = \frac{4}{(0.50-x)^{2}}
\;\Longrightarrow\; \frac{3}{x} = \frac{2}{0.50-x} $$

(taking positive square roots, since $0 < x < 0.50$)

$$ 3(0.50-x) = 2x \;\Rightarrow\; 1.5 = 5x \;\Rightarrow\; x = 0.30\ \text{m} $$

The null point is $30\ \text{cm}$ from the $9\ \mu\text{C}$ charge and
$20\ \text{cm}$ from the $4\ \mu\text{C}$ charge — nearer the smaller charge, as
it must be. Note the answer does not depend on the third charge at all.
:::

## Chapter summary

- Charge is quantised ($q = \pm ne$, $e = 1.6\times10^{-19}\ \text{C}$),
  conserved, additive and independent of speed. Charging transfers electrons only.
- $1\ \text{C} = 1\ \text{A s} = 6.25\times10^{18}$ electronic charges.
- Charging by induction gives a charge **opposite** to the inducing charge; the
  earth connection must be broken **before** the rod is taken away.
- Coulomb's law: $F = \dfrac{1}{4\pi\varepsilon_0}\dfrac{q_1q_2}{r^{2}}$ with
  $\dfrac{1}{4\pi\varepsilon_0} = 9\times10^{9}\ \text{N m}^{2}\text{C}^{-2}$ and
  $\varepsilon_0 = 8.85\times10^{-12}\ \text{C}^{2}\text{N}^{-1}\text{m}^{-2}$.
- In a medium the force is reduced: $F_{med} = F_{vac}/\varepsilon_r$.
- Vector form $\vec{F}_{21} = \dfrac{1}{4\pi\varepsilon_0}\dfrac{q_1q_2}{r^{2}}\hat{r}_{21}$;
  the forces obey Newton's third law.
- Superposition: the resultant force is the **vector** sum of the individual
  pairwise forces, $\vec{F}_1 = \sum_j \vec{F}_{1j}$; combine two forces with
  $F = \sqrt{F_a^{2}+F_b^{2}+2F_aF_b\cos\theta}$.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. Which of the following is **not** a property of electric charge? <span class="marks">[1]</span>
   (a) quantisation (b) conservation (c) additivity (d) variation with speed
2. The number of electronic charges in one coulomb is about <span class="marks">[1]</span>
   (a) $1.6\times10^{19}$ (b) $6.25\times10^{18}$ (c) $6.02\times10^{23}$ (d) $9\times10^{9}$
3. A body charged by induction acquires a charge <span class="marks">[1]</span>
   (a) of the same sign as the inducing charge (b) of the opposite sign
   (c) that is always zero (d) equal to twice the inducing charge
4. Two charges repel each other with a force $F$ in air. Placed at the same
   separation in a medium of dielectric constant $4$, the force becomes <span class="marks">[1]</span>
   (a) $4F$ (b) $F/2$ (c) $F/4$ (d) $F/16$
5. If the distance between two point charges is halved, the force between them <span class="marks">[1]</span>
   (a) is halved (b) is doubled (c) becomes four times (d) becomes one fourth

::: note Answers to Group A
**1.** (d) — charge is invariant; it is the *mass* that changes with speed.
**2.** (b) — $1/(1.6\times10^{-19}) = 6.25\times10^{18}$.
**3.** (b) — electrons are driven away or attracted, leaving the opposite charge behind.
**4.** (c) — $F_{med} = F_{vac}/\varepsilon_r$.
**5.** (c) — $F \propto 1/r^{2}$, so halving $r$ multiplies $F$ by $4$.
:::

**Group B — Short answer (5 marks each)**

1. State Coulomb's law and express it in vector form. Hence define the coulomb. <span class="marks">[5]</span>
2. Explain, with labelled diagrams, how a metal sphere standing on an insulating
   base can be given a positive charge by induction. Why must the earth
   connection be removed before the charging rod? <span class="marks">[5]</span>
3. Two point charges of $+5\ \mu\text{C}$ and $+10\ \mu\text{C}$ are placed
   $20\ \text{cm}$ apart in vacuum. Calculate the force between them, and state
   its nature. <span class="marks">[5]</span>
4. State the principle of quantisation and conservation of charge. How many
   electrons must be removed from a body to give it a charge of
   $+2\ \mu\text{C}$? <span class="marks">[5]</span>
5. Two identical metal spheres carrying charges of $+6\ \mu\text{C}$ and
   $-2\ \mu\text{C}$ are brought into contact and then separated to a distance of
   $10\ \text{cm}$. Find the force between them. <span class="marks">[5]</span>

::: note Answers to Group B
**3.** $F = \dfrac{9\times10^{9}\times5\times10^{-6}\times10\times10^{-6}}{(0.20)^{2}}
= \dfrac{9\times10^{9}\times5\times10^{-11}}{0.04} = \dfrac{0.45}{0.04} = 11.25\ \text{N}$,
repulsive (both charges positive).

**4.** $n = \dfrac{q}{e} = \dfrac{2\times10^{-6}}{1.6\times10^{-19}} = 1.25\times10^{13}$
electrons must be **removed**.

**5.** Identical spheres in contact share the total charge equally. Total
$= +6 - 2 = +4\ \mu\text{C}$, so each carries $+2\ \mu\text{C}$. Then

$$ F = \frac{9\times10^{9}\times(2\times10^{-6})^{2}}{(0.10)^{2}}
= \frac{3.6\times10^{-2}}{0.01} = 3.6\ \text{N} $$

repulsive, since both spheres are now positive.
:::

**Group C — Long answer (8 marks each)**

1. (a) State Coulomb's law, write it in vector form, and state the principle of
   superposition of electrostatic forces. <span class="marks">[4]</span>
   (b) Three point charges of $+3\ \mu\text{C}$ each are placed at the corners of
   an equilateral triangle of side $30\ \text{cm}$. Calculate the magnitude and
   direction of the resultant force on one of them. <span class="marks">[4]</span>
2. (a) What is meant by charging by induction? Describe, with diagrams, how two
   metal spheres in contact can be given equal and opposite charges in a single
   operation. <span class="marks">[4]</span>
   (b) Two point charges of $+9\ \mu\text{C}$ and $+4\ \mu\text{C}$ are fixed
   $50\ \text{cm}$ apart in air. Find the position on the line joining them at
   which a third charge would experience no resultant force, and explain why the
   answer does not depend on the size or sign of that third charge. <span class="marks">[4]</span>

::: note Answers to Group C
**1.(b)** With $q = 3\times10^{-6}\ \text{C}$ and $r = 0.30\ \text{m}$, each
pairwise force is

$$ F_1 = \frac{9\times10^{9}\times(3\times10^{-6})^{2}}{(0.30)^{2}}
= \frac{9\times10^{9}\times9\times10^{-12}}{0.09} = \frac{8.1\times10^{-2}}{0.09}
= 0.9\ \text{N} $$

The two forces on the chosen charge are each $0.9\ \text{N}$, repulsive, with
$60^{\circ}$ between them:

$$ F = \sqrt{0.9^{2}+0.9^{2}+2(0.9)(0.9)\cos 60^{\circ}} = 0.9\sqrt{3} = 1.56\ \text{N} $$

directed along the bisector, i.e. radially outward from the centroid of the
triangle.

**2.(a)** Outline: place the two spheres in contact on insulating stands; bring a
negatively charged rod near sphere A; electrons are repelled to sphere B;
**separate the spheres while the rod is still in position**; then remove the rod.
A is left positive and B negative, with equal magnitudes (charge is conserved, and
the pair was neutral to begin with).

**2.(b)** Let the null point be $x$ from the $9\ \mu\text{C}$ charge, on the line
between the two charges. Equating magnitudes,

$$ \frac{9}{x^{2}} = \frac{4}{(0.50-x)^{2}} \;\Rightarrow\; \frac{3}{x} = \frac{2}{0.50-x} $$

$$ 1.5 - 3x = 2x \;\Rightarrow\; x = 0.30\ \text{m} $$

The point lies $30\ \text{cm}$ from the $9\ \mu\text{C}$ charge (and $20\ \text{cm}$
from the $4\ \mu\text{C}$ charge). The test charge $q_0$ appears as a common
factor on both sides of the equation and cancels, so neither its magnitude nor its
sign affects the position of the null point.
:::
