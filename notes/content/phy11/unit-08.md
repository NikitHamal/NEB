---
subject: Physics
grade: 11
unit: 8
title: Elasticity
hours: 5
area: Mechanics
---

Every solid changes shape a little when you push or pull it. A bridge deck sags
under a loaded truck on the Prithvi Highway, a steel cable in a Trishuli
suspension bridge stretches, a rubber band grows longer. Elasticity asks two
questions: how much does a body deform under a given force, and does it come
back when the force is removed? The whole unit is built on two quantities —
**stress** (force per unit area) and **strain** (fractional change in size) —
and on the constants that link them.

::: key What the examiner wants
Group B nearly always carries one definition set (stress, strain, Hooke's law,
modulus) plus one numerical on Young modulus or stored energy. Group C favours
"define the three moduli and derive the energy stored in a stretched wire".
Master the four boxed formulas in the summary and you cover most of the marks.
:::

## 8.1 Hooke's law: force constant

When an external force acts on a body, its molecules are pulled apart from (or
pushed towards) their equilibrium separations. The inter-molecular forces then
act to restore the original spacing. The external force is called the
**deforming force**; the internal force that opposes it is the **restoring
force**. As long as the deformation is small, the two are equal in magnitude.

Robert Hooke stated the experimental law in 1678: for small deformations the
extension is proportional to the load.

::: definition Hooke's law
Within the elastic limit, the extension produced in a body is directly
proportional to the deforming force applied, the temperature remaining constant.

$$ F \propto x \qquad \Rightarrow \qquad F = kx $$
:::

The constant $k$ is the **force constant** (also called stiffness, or spring
constant for a spring). It is the force needed to produce unit extension:

$$ k = \frac{F}{x}, \qquad \text{unit: N m}^{-1}, \qquad \text{dimensions } [MT^{-2}] $$

```figure caption="Load–extension graph. The straight part obeys Hooke's law and its slope is the force constant $k$. Past the elastic limit the graph curves and the body no longer returns to its original length."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6,2.8))
x1 = np.linspace(0, 4.0, 120); F1 = 5.0*x1
x2 = np.linspace(4.0, 7.0, 120); F2 = 20 + 5.0*(x2-4) - 0.95*(x2-4)**2
ax.plot(x1, F1, color=ACCENT, lw=2.0, label="Hooke's law region")
ax.plot(x2, F2, color=SERIES[1], lw=2.0, ls='--', label='beyond elastic limit')
ax.plot([4.0],[20.0],'o',color=INK,ms=5)
ax.annotate('elastic limit', (4.0,20.0), textcoords='offset points', xytext=(-30,20),
            fontsize=9, color=INK,
            arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.0, mutation_scale=10))
ax.plot([1.0,2.8,2.8],[5.0,5.0,14.0], color=MUTED, lw=1.0, ls=':')
ax.annotate(r'slope $=k$', (1.9,5.0), textcoords='offset points', xytext=(-10,-17),
            color=MUTED, fontsize=9)
ax.set_xlabel('extension  $x$  (cm)'); ax.set_ylabel('load  $F$  (N)')
ax.set_xlim(0,7.5); ax.set_ylim(0,32)
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.5)
ax.legend(loc='lower right', fontsize=8.2)
```

The force constant is **not** a property of the material alone. For a wire of
length $L$ and area of cross-section $A$ made of a material of Young modulus $Y$
(section 8.3),

$$ k = \frac{YA}{L} $$

so a short thick wire is stiffer than a long thin one of the same metal. When
springs of constants $k_1$ and $k_2$ are joined **in series** the combination is
softer, $1/k = 1/k_1 + 1/k_2$; joined side by side **in parallel** it is stiffer,
$k = k_1 + k_2$.

::: example Worked example 8.1
**Problem.** A spring of natural length $20\ \text{cm}$ stretches to
$24\ \text{cm}$ when a load of $20\ \text{N}$ hangs from it. Find its force
constant and the length of the spring when the load is $35\ \text{N}$.

**Solution.** Extension $x = 24 - 20 = 4\ \text{cm} = 0.04\ \text{m}$.

$$ k = \frac{F}{x} = \frac{20}{0.04} = 500\ \text{N m}^{-1} $$

For $F = 35\ \text{N}$, $x = F/k = 35/500 = 0.07\ \text{m} = 7\ \text{cm}$, so the
spring is $20 + 7 = 27\ \text{cm}$ long (assuming the elastic limit is not
exceeded).
:::

## 8.2 Stress, Strain, Elasticity and plasticity

::: definition Stress and strain
**Stress** is the restoring force set up per unit area of cross-section of a
deformed body: $\ \text{stress} = F/A$. SI unit N m⁻² or pascal (Pa), dimensional
formula $[ML^{-1}T^{-2}]$.

**Strain** is the ratio of the change in a dimension to the original value of
that dimension. It is a pure number with no unit and no dimensions.
:::

Stress has the same dimensions as pressure, but the two are not the same thing:
pressure in a fluid always acts normal to a surface, while stress may act along
a surface (shear). There are three kinds of stress and a matching strain for
each.

| Stress | How the force acts | Strain produced | Modulus |
|---|---|---|---|
| Tensile / compressive (longitudinal) | normal to the end faces, along the length | $\text{longitudinal strain} = e/L$ | Young modulus $Y$ |
| Hydraulic (volume) | normal and equal on every face | $\text{volume strain} = \Delta V/V$ | Bulk modulus $B$ |
| Tangential (shear) | parallel to one face, the opposite face fixed | $\text{shear strain} = \theta = x/L$ | Shear modulus $\eta$ |

**Elasticity** is the property by which a body regains its original shape and
size after the deforming force is removed. **Plasticity** is the opposite
property: the body keeps the new shape. No real material is perfectly elastic or
perfectly plastic; a quartz fibre is the nearest to perfectly elastic and wet
clay or putty the nearest to perfectly plastic.

```figure caption="Stress–strain curve for a ductile metal such as mild steel. $P$ is the proportional limit, $E$ the elastic limit, $Y$ the yield point, $U$ the ultimate tensile stress and $B$ the breaking point."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,3.0))
ek = [0, 0.004, 0.005, 0.0062, 0.009, 0.014, 0.020, 0.032, 0.050,
      0.080, 0.110, 0.150, 0.175, 0.200, 0.220]
sk = [0, 240, 252, 260, 250, 248, 250, 283, 318, 358, 384, 400, 393, 372, 330]
e = np.linspace(0, 0.220, 500); s = np.interp(e, ek, sk)
ax.plot(e, s, color=ACCENT, lw=2.0)
# P, E and Y lie almost on top of one another, so they are called out with
# leader lines into the clear space beside the curve
call = [(0.004,240,'P',0.030,160), (0.005,252,'E',0.030,205),
        (0.0062,260,'Y',0.018,298)]
for x0,y0,lab,tx,ty in call:
    ax.plot([x0],[y0],'o',color=SERIES[1],ms=4.0,zorder=4)
    ax.annotate(lab,(x0,y0),xytext=(tx,ty),ha='left',va='center',
                color=INK,fontsize=9.5,
                arrowprops=dict(arrowstyle='-',color=MUTED,lw=0.7,
                                shrinkA=2,shrinkB=3))
for x0,y0,lab,off in [(0.150,400,'U',(-3,9)), (0.220,330,'B',(6,-2))]:
    ax.plot([x0],[y0],'o',color=SERIES[1],ms=4.5,zorder=4)
    ax.annotate(lab,(x0,y0),textcoords='offset points',xytext=off,
                color=INK,fontsize=9.5)
ax.plot([0,0.0045],[0,270], color=MUTED, lw=1.0, ls=':')
ax.annotate('slope $=Y$', (0.014,100), ha='left', va='center',
            color=MUTED, fontsize=9)
ax.set_xlabel('strain'); ax.set_ylabel('stress  (MPa)')
ax.set_xlim(0,0.245); ax.set_ylim(0,440)
ax.spines[['top','right']].set_visible(False); ax.grid(True, alpha=.5)
```
Reading the curve from the origin:

- **$O$ to $P$ — proportional limit.** Stress is proportional to strain; Hooke's
  law holds and the slope of this line is the Young modulus.
- **$P$ to $E$ — elastic limit.** The graph bends, so Hooke's law fails, but the
  wire still returns exactly to its original length when unloaded.
- **Beyond $E$ — permanent set.** Unloading now leaves the wire longer than it
  started. At the **yield point** $Y$ the wire begins to extend with almost no
  extra load.
- **$U$ — ultimate tensile stress**, the largest stress the material can take.
  After $U$ the wire develops a local neck, so the true area falls and the curve
  drops until the wire snaps at the **breaking point** $B$.

A material that stretches a great deal between $Y$ and $B$ (copper, mild steel,
gold) is **ductile**; one that breaks very soon after the elastic limit (glass,
cast iron, ceramic tile) is **brittle**.

::: caution Breaking stress and breaking force are different
**Breaking stress** depends only on the material. **Breaking force** =
breaking stress $\times$ area, so it depends on the thickness of the wire but
**not** on its length. A 10 m wire and a 1 m wire of the same metal and diameter
snap under exactly the same load.
:::

Two related effects are worth naming. **Elastic after-effect** is the delay some
materials (glass, rubber) show in returning to their original size. **Elastic
fatigue** is the loss of elastic strength when a body is subjected to repeated
cycles of stress — the reason a wire finally breaks after being bent back and
forth many times, and why bridges and aircraft parts are replaced long before
they look worn.

## 8.3 Elastic modulus: Young modulus, bulk modulus, shear modulus

::: definition Modulus of elasticity
Within the elastic limit, the modulus of elasticity of a material is the ratio
of the stress applied to the strain produced:
$\ \text{modulus} = \text{stress}/\text{strain}$. Because strain has no unit, a
modulus has the unit of stress, N m⁻² (Pa). A large modulus means a stiff
material.
:::

```figure caption="The three deformations. (a) tensile stress changes length, (b) hydraulic stress changes volume, (c) tangential stress changes shape through the angle $\theta$."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Arc
fig, axes = plt.subplots(1, 3, figsize=(5.2,2.4))
aw = dict(arrowstyle='-|>', color=SERIES[1], lw=1.5, mutation_scale=11)
# (a) tensile
ax = axes[0]
ax.add_patch(Rectangle((0.34,0.20),0.32,1.05, fill=False, ec=INK, lw=1.3))
ax.annotate('', xy=(0.50,1.72), xytext=(0.50,1.25), arrowprops=aw)
ax.annotate('', xy=(0.50,-0.27), xytext=(0.50,0.20), arrowprops=aw)
ax.text(0.50,1.82,'$F$',ha='center',fontsize=9.5,color=INK)
ax.text(0.50,-0.52,'$F$',ha='center',fontsize=9.5,color=INK)
ax.text(0.74,0.72,'$L$',ha='left',fontsize=9,color=MUTED)
ax.set_title('(a) tensile', fontsize=9, color=INK)
ax.set_xlim(-0.05,1.05); ax.set_ylim(-0.75,2.0)
# (b) hydraulic
ax = axes[1]
ax.add_patch(Rectangle((0.28,0.42),0.44,0.44, fill=False, ec=INK, lw=1.3))
for (xs,ys,xe,ye) in [(0.50,1.15,0.50,0.90),(0.50,0.13,0.50,0.38),
                      (0.00,0.64,0.24,0.64),(1.00,0.64,0.76,0.64)]:
    ax.annotate('', xy=(xe,ye), xytext=(xs,ys), arrowprops=aw)
ax.text(0.50,1.30,'$p$',ha='center',fontsize=9.5,color=INK)
ax.set_title('(b) hydraulic', fontsize=9, color=INK)
ax.set_xlim(-0.12,1.12); ax.set_ylim(-0.30,1.65)
# (c) shear
ax = axes[2]
ax.add_patch(Rectangle((0.20,0.20),0.52,0.52, fill=False, ec=MUTED, lw=1.0, ls=':'))
ax.add_patch(Polygon([[0.20,0.20],[0.72,0.20],[0.98,0.72],[0.46,0.72]],
                     closed=True, fill=False, ec=INK, lw=1.3))
ax.annotate('', xy=(1.22,0.72), xytext=(0.98,0.72), arrowprops=aw)
ax.text(1.25,0.70,'$F$',ha='left',fontsize=9.5,color=INK)
ax.add_patch(Arc((0.20,0.20), 0.56, 0.56, theta1=63.4, theta2=90.0,
                 color=SERIES[1], lw=0.9))
ax.text(0.42,0.44,r'$\theta$',ha='left',va='center',fontsize=9.5,color=SERIES[1])
# x is the sideways shift of the top face, not the width of the face
ax.plot([0.20,0.20],[0.72,0.90], color=MUTED, lw=0.7, ls=':')
ax.plot([0.46,0.46],[0.72,0.90], color=MUTED, lw=0.7, ls=':')
ax.annotate('', xy=(0.46,0.86), xytext=(0.20,0.86),
            arrowprops=dict(arrowstyle='<->',color=MUTED,lw=0.8,mutation_scale=8))
ax.text(0.33,0.92,'$x$',ha='center',va='bottom',fontsize=9,color=MUTED)
ax.set_title('(c) shear', fontsize=9, color=INK)
ax.set_xlim(0.05,1.45); ax.set_ylim(-0.15,1.15)
for ax in axes:
    ax.set_aspect('equal'); ax.set_anchor('N'); ax.axis('off')
```
### Young modulus

$$ Y = \frac{\text{longitudinal stress}}{\text{longitudinal strain}}
= \frac{F/A}{e/L} = \frac{FL}{Ae} $$

where $e$ is the extension of a wire of original length $L$ and area $A$ under a
load $F$. Rearranging gives $F = (YA/L)e$, which compared with $F = kx$ proves
the result $k = YA/L$ quoted in section 8.1. Only solids have a Young modulus,
because only a solid can be pulled into a wire.

::: example Worked example 8.2
**Problem.** A steel wire of length $2.0\ \text{m}$ and diameter $1.0\ \text{mm}$
carries a load of $50\ \text{N}$. Taking $Y = 2.0 \times 10^{11}\ \text{Pa}$,
find the stress, the strain and the extension.

**Solution.** Area of cross-section:

$$ A = \frac{\pi d^{2}}{4} = \frac{3.1416 \times (1.0\times10^{-3})^{2}}{4}
= 7.854\times10^{-7}\ \text{m}^{2} $$

$$ \text{stress} = \frac{F}{A} = \frac{50}{7.854\times10^{-7}}
= 6.37\times10^{7}\ \text{Pa} $$

$$ \text{strain} = \frac{\text{stress}}{Y} = \frac{6.37\times10^{7}}{2.0\times10^{11}}
= 3.18\times10^{-4} $$

$$ e = \text{strain}\times L = 3.18\times10^{-4}\times 2.0
= 6.37\times10^{-4}\ \text{m} = 0.64\ \text{mm} $$
:::

### Bulk modulus

If a uniform increase of pressure $p$ on all sides reduces a volume $V$ by
$\Delta V$, then

$$ B = -\frac{p}{\Delta V / V} = -\frac{pV}{\Delta V} $$

The minus sign is there because $\Delta V$ is negative when $p$ increases, so
that $B$ comes out positive. Solids, liquids **and** gases all have a bulk
modulus. Its reciprocal is the **compressibility**,
$K = 1/B$, measured in Pa⁻¹.

::: example Worked example 8.3
**Problem.** The pressure on $1.0\ \text{m}^{3}$ of water is increased by
$2.2\times10^{7}\ \text{Pa}$. If the bulk modulus of water is
$2.2\times10^{9}\ \text{Pa}$, find the change in volume and the compressibility
of water.

**Solution.**

$$ \Delta V = -\frac{pV}{B} = -\frac{2.2\times10^{7}\times 1.0}{2.2\times10^{9}}
= -1.0\times10^{-2}\ \text{m}^{3} $$

The volume falls by $0.010\ \text{m}^{3}$, i.e. by $1.0\ \%$ — water is very
nearly incompressible. The compressibility is

$$ K = \frac{1}{B} = \frac{1}{2.2\times10^{9}} = 4.55\times10^{-10}\ \text{Pa}^{-1} $$
:::

### Shear modulus (modulus of rigidity)

A tangential force $F$ on the top face of area $A$ of a block of height $L$
slides that face sideways by $x$, turning the vertical edges through a small
angle $\theta = x/L$ radians. Then

$$ \eta = \frac{\text{tangential stress}}{\text{shear strain}}
= \frac{F/A}{\theta} = \frac{FL}{Ax} $$

Only solids have a shear modulus: a liquid or a gas cannot sustain a tangential
stress — it simply flows. For most metals $\eta$ is roughly $Y/3$.

::: example Worked example 8.4
**Problem.** A rubber block of square face $10\ \text{cm}\times10\ \text{cm}$ and
height $5.0\ \text{cm}$ is fixed at the bottom. A tangential force of
$100\ \text{N}$ is applied to the top face. If
$\eta = 2.0\times10^{6}\ \text{Pa}$, find the shear strain and the sideways
displacement of the top face.

**Solution.** $A = 0.10\times0.10 = 1.0\times10^{-2}\ \text{m}^{2}$.

$$ \text{tangential stress} = \frac{100}{1.0\times10^{-2}} = 1.0\times10^{4}\ \text{Pa} $$
$$ \theta = \frac{\text{stress}}{\eta} = \frac{1.0\times10^{4}}{2.0\times10^{6}}
= 5.0\times10^{-3}\ \text{rad} $$
$$ x = \theta L = 5.0\times10^{-3}\times 0.050 = 2.5\times10^{-4}\ \text{m} = 0.25\ \text{mm} $$
:::

Approximate room-temperature values (1 GPa $= 10^{9}$ Pa):

| Material | $Y$ (GPa) | $B$ (GPa) | $\eta$ (GPa) | Poisson ratio $\sigma$ |
|---|---|---|---|---|
| Steel | 200 | 160 | 84 | 0.29 |
| Copper | 110 | 140 | 44 | 0.34 |
| Brass | 91 | 61 | 35 | 0.34 |
| Aluminium | 70 | 70 | 25 | 0.33 |
| Glass | 55 | 37 | 23 | 0.25 |
| Water | — | 2.2 | 0 | — |
| Rubber | 0.0005 – 0.05 | ≈ 2 | ≈ 0.0007 | ≈ 0.50 |

## 8.4 Poisson's ratio

A stretched wire does not only get longer — it also gets thinner. If a wire of
length $L$ and diameter $d$ stretches by $e$ and its diameter shrinks by
$\Delta d$, then

$$ \text{longitudinal strain} = \frac{e}{L}, \qquad
\text{lateral strain} = -\frac{\Delta d}{d} $$

::: definition Poisson's ratio
Poisson's ratio $\sigma$ is the ratio of the lateral strain to the longitudinal
strain, within the elastic limit:

$$ \sigma = -\ \frac{\text{lateral strain}}{\text{longitudinal strain}}
= \frac{\Delta d / d}{e / L} $$

It is a pure number with **no unit and no dimensions**, and it is a constant of
the material.
:::

Theory allows $\sigma$ to lie between $-1$ and $+0.5$. For all common materials
it is positive and lies between about $0.2$ and $0.4$; rubber is the extreme
case at nearly $0.5$. The upper bound has a simple physical meaning. For a wire
of volume $V = \pi r^{2}L$, small changes give

$$ \frac{\Delta V}{V} = \frac{2\Delta r}{r} + \frac{\Delta L}{L}
= (-2\sigma + 1)\frac{\Delta L}{L} = (1-2\sigma)\,\frac{e}{L} $$

If $\sigma = 0.5$ the volume does not change at all when the wire is stretched;
$\sigma$ larger than $0.5$ would mean the volume **shrinks** on stretching,
which no material does.

::: example Worked example 8.5
**Problem.** A wire of length $3.0\ \text{m}$ and diameter $2.0\ \text{mm}$ is
stretched by $1.5\ \text{mm}$. If Poisson's ratio for the material is $0.30$,
find the decrease in diameter and the fractional change in volume.

**Solution.**

$$ \text{longitudinal strain} = \frac{e}{L} = \frac{1.5\times10^{-3}}{3.0}
= 5.0\times10^{-4} $$
$$ \text{lateral strain} = \sigma \times 5.0\times10^{-4}
= 0.30\times5.0\times10^{-4} = 1.5\times10^{-4} $$
$$ \Delta d = 1.5\times10^{-4}\times 2.0\ \text{mm} = 3.0\times10^{-4}\ \text{mm} $$

So the diameter falls by $0.30\ \mu\text{m}$. The volume change is

$$ \frac{\Delta V}{V} = (1-2\sigma)\frac{e}{L}
= (1-0.60)\times5.0\times10^{-4} = 2.0\times10^{-4} $$

an increase of $0.02\ \%$.
:::

## 8.5 Elastic potential energy

Stretching a wire takes work, and that work is stored in the wire as **elastic
potential energy**. It is recovered when the wire is released — this is how a
catapult, a bow and a clock spring work.

::: derivation Energy stored in a stretched wire, $U = \frac{1}{2}Fe$
We start from the work done by the stretching force and reach the energy stored in the
wire, and then the energy stored in each cubic metre of it.

**Setting up.** A wire of original length $L$ and cross-section area $A$ is slowly
stretched. Let $x$ be the extension *so far*, and let $e$ be the final extension when
the full load $F$ is on. The wire obeys Hooke's law throughout.

**Step 1 — the force needed at extension $x$.** The definition of Young modulus,
$Y = \dfrac{F_x L}{A x}$, rearranged for the force, says that the force which holds the
wire at extension $x$ is

$$ F_x = \frac{YA}{L}\,x $$

This is the key point: the force is **not** constant. It grows as the wire stretches, so
we cannot just write work $=$ force $\times$ distance.

**Step 2 — take a stretch so small the force cannot change.** Let the wire stretch a
further tiny amount $dx$. Over such a small distance $F_x$ is effectively constant, so
the small work done is

$$ dW = F_x\,dx = \frac{YA}{L}\,x\,dx $$

**Step 3 — add up all the small bits.** Adding up infinitely many small pieces means
integrating, from no extension ($x = 0$) to the final extension ($x = e$):

$$ W = \int_{0}^{e} \frac{YA}{L}\,x\,dx $$

**Step 4 — take the constants outside.** $Y$, $A$ and $L$ do not change during the
stretch:

$$ W = \frac{YA}{L}\int_{0}^{e} x\,dx $$

**Step 5 — do the integral.** Using $\int x\,dx = x^{2}/2$:

$$ W = \frac{YA}{L}\left[\frac{x^{2}}{2}\right]_{0}^{e} $$

**Step 6 — put in the limits.** At $x = e$ we get $e^{2}/2$; at $x = 0$ we get $0$:

$$ W = \frac{YA}{L}\cdot\frac{e^{2}}{2} $$

**Step 7 — split one factor of $e$ off, ready for the next step:**

$$ W = \frac{1}{2}\left(\frac{YAe}{L}\right)e $$

**Step 8 — recognise the bracket.** Putting $x = e$ in Step 1 gives the final load,
$F = YAe/L$. So the bracket *is* $F$:

$$ W = \frac{1}{2}Fe $$

**Step 9 — the work is stored, not lost.** The stretching is slow and the wire stays
elastic, so all this work is stored as elastic potential energy $U$:

$$ U = \frac{1}{2}Fe = \frac{1}{2}\times\text{load}\times\text{extension} $$

---

**Now the energy per unit volume.**

**Step 10 — divide by the volume.** The wire's volume is $A \times L$:

$$ u = \frac{U}{AL} = \frac{\frac{1}{2}Fe}{AL} $$

**Step 11 — split the fraction so that $F$ pairs with $A$ and $e$ pairs with $L$:**

$$ u = \frac{1}{2}\cdot\frac{F}{A}\cdot\frac{e}{L} $$

**Step 12 — name the two factors.** $F/A$ is the stress and $e/L$ is the strain:

$$ u = \frac{1}{2}\times\text{stress}\times\text{strain} $$

**Step 13 — two other forms.** Since stress $= Y \times$ strain, we may replace either
factor. Writing $\varepsilon$ for the strain:

$$ u = \frac{1}{2}Y\varepsilon^{2} = \frac{1}{2}\cdot\frac{(\text{stress})^{2}}{Y} $$

**Result.**

$$ U = \frac{1}{2}Fe, \qquad u = \frac{1}{2}\times\text{stress}\times\text{strain} $$

**What it means.** The $\frac{1}{2}$ is the whole physical story: the force starts at zero
and ends at $F$, so on average only $F/2$ acted over the distance $e$. Graphically,
$U$ is the **area under the load–extension line** — a triangle of base $e$ and height $F$.
The second result says the energy stored in each cubic metre depends only on how hard the
material is squeezed and how much it gives, not on the size of the wire.

**Conditions used.** Hooke's law holds (we are below the elastic limit, so the graph is a
straight line), the load is applied slowly so nothing vibrates, and no energy is lost as
heat.
:::

::: tip The examiner is looking for
1. The statement that the force is variable, $F_x = (YA/L)x$ — full marks are rarely
   given without it.
2. The element of work $dW = F_x\,dx$.
3. The integral $\int_{0}^{e}(YA/L)x\,dx$ **with correct limits**.
4. The step that turns $YAe/L$ back into $F$, giving $U = \frac{1}{2}Fe$.
5. For the energy-density part: dividing by volume $AL$ and regrouping into
   $\frac{1}{2}\,\text{stress}\times\text{strain}$.
:::

```figure caption="Work done in stretching is the area under the load–extension line, $U = \frac{1}{2}Fe$. The shaded strip is $dW = F\,dx$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.4,2.7))
x = np.linspace(0, 5, 200); F = 4.0*x
ax.plot(x, F, color=ACCENT, lw=2.0)
ax.fill_between(x, 0, F, color=ACCENT, alpha=0.12)
xs = 2.6; w = 0.30
ax.fill_between([xs, xs+w], 0, [4.0*xs, 4.0*(xs+w)], color=SERIES[1], alpha=0.45)
ax.annotate('$dW = F\\,dx$', (xs+w/2, 4.0*xs), textcoords='offset points',
            xytext=(-18,26), fontsize=9, color=SERIES[1],
            arrowprops=dict(arrowstyle='-|>', color=SERIES[1], lw=1.0, mutation_scale=10))
ax.annotate(r'$U=\frac{1}{2}Fe$', (1.4, 2.4), fontsize=10, color=INK, ha='center')
ax.hlines(20, 0, 5, color=MUTED, lw=0.9, ls=':')
ax.vlines(5, 0, 20, color=MUTED, lw=0.9, ls=':')
ax.set_xlabel('extension'); ax.set_ylabel('load')
ax.set_xlim(0, 5.7); ax.set_ylim(0, 24)
ax.set_xticks([5]); ax.set_xticklabels(['$e$'])
ax.set_yticks([20]); ax.set_yticklabels(['$F$'])
ax.spines[['top','right']].set_visible(False)
```

::: caution The factor of one half
The energy is $\frac{1}{2}Fe$, **not** $Fe$. The load is built up gradually from
zero to $F$, so the *average* force during the stretch is $F/2$. If instead the
full load $F$ is hung on suddenly, it does work $Fe$ — twice the stored energy —
and the extra $\frac{1}{2}Fe$ appears as vibration and heat.
:::

::: example Worked example 8.6
**Problem.** A steel wire of length $4.0\ \text{m}$ and cross-sectional area
$2.0\ \text{mm}^{2}$ is stretched by $2.0\ \text{mm}$. Taking
$Y = 2.0\times10^{11}\ \text{Pa}$, find the load applied, the energy stored and
the energy stored per unit volume.

**Solution.** With $A = 2.0\times10^{-6}\ \text{m}^{2}$ and
$e = 2.0\times10^{-3}\ \text{m}$:

$$ F = \frac{YAe}{L}
= \frac{2.0\times10^{11}\times 2.0\times10^{-6}\times 2.0\times10^{-3}}{4.0}
= 200\ \text{N} $$

$$ U = \tfrac{1}{2}Fe = \tfrac{1}{2}\times200\times2.0\times10^{-3} = 0.20\ \text{J} $$

Volume $= AL = 2.0\times10^{-6}\times4.0 = 8.0\times10^{-6}\ \text{m}^{3}$, so

$$ u = \frac{0.20}{8.0\times10^{-6}} = 2.5\times10^{4}\ \text{J m}^{-3} $$
:::

## Chapter summary

- Hooke's law: within the elastic limit $F = kx$, where the force constant
  $k = F/x$ (N m⁻¹). For a wire $k = YA/L$, so $k$ depends on shape as well as
  material.
- Stress $= F/A$ (Pa, $[ML^{-1}T^{-2}]$); strain $=$ change ÷ original value
  (no unit). Modulus $=$ stress ÷ strain.
- The stress–strain curve runs: proportional limit $P$, elastic limit $E$, yield
  point $Y$, ultimate stress $U$, breaking point $B$. Ductile materials have a
  long $Y$–$B$ stretch; brittle ones break just after $E$.
- Young modulus $Y = FL/Ae$; bulk modulus $B = -pV/\Delta V$ with
  compressibility $K = 1/B$; shear modulus $\eta = F/(A\theta)$ with
  $\theta = x/L$. Only $B$ applies to liquids and gases.
- Poisson's ratio $\sigma = (\Delta d/d)\div(e/L)$; no unit, theoretical range
  $-1$ to $0.5$, real materials $0.2$–$0.4$. Also
  $\Delta V/V = (1-2\sigma)e/L$.
- Elastic potential energy $U = \frac{1}{2}Fe = \frac{1}{2}\dfrac{YAe^{2}}{L}$,
  and energy per unit volume $u = \frac{1}{2}\times$ stress $\times$ strain
  $= \frac{1}{2}Y\varepsilon^{2}$.
- Breaking force depends on the area of cross-section, never on the length.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The SI unit of stress is <span class="marks">[1]</span>
   (a) N m (b) N m⁻² (c) N m⁻¹ (d) it has no unit
2. Strain is <span class="marks">[1]</span>
   (a) measured in N m⁻² (b) measured in m (c) a pure number (d) measured in N
3. For a perfectly rigid body the Young modulus is <span class="marks">[1]</span>
   (a) zero (b) infinite (c) unity (d) negative
4. The theoretical limits of Poisson's ratio are <span class="marks">[1]</span>
   (a) 0 to 1 (b) $-1$ to $0.5$ (c) $-0.5$ to $1$ (d) 0 to 0.25
5. The energy stored per unit volume of a stretched wire equals <span class="marks">[1]</span>
   (a) stress × strain (b) ½ × stress × strain (c) stress ÷ strain (d) ½ × stress ÷ strain

::: note Answers to Group A
**1.** (b) — stress is force per unit area, N m⁻² = Pa.
**2.** (c) — it is a ratio of two lengths (or two volumes), so it has no unit.
**3.** (b) — a rigid body has zero strain, and $Y = \text{stress}/\text{strain} \to \infty$.
**4.** (b) — $\sigma$ larger than $0.5$ would make the volume fall on stretching.
**5.** (b) — the area under the stress–strain line is $\frac{1}{2}\times$ stress $\times$ strain.
:::

**Group B — Short answer (5 marks each)**

1. Define stress and strain and state their units. State Hooke's law and hence
   define modulus of elasticity. <span class="marks">[5]</span>
2. Draw a stress–strain curve for a ductile material and mark the proportional
   limit, elastic limit, yield point and breaking point. Distinguish between
   elasticity and plasticity. <span class="marks">[5]</span>
3. Define Young modulus. A steel wire $3.0\ \text{m}$ long with cross-sectional
   area $2.0\ \text{mm}^{2}$ stretches by $1.5\ \text{mm}$ under a load $W$. Find
   $W$, given $Y = 2.0\times10^{11}\ \text{Pa}$. <span class="marks">[5]</span>
4. Define bulk modulus and compressibility. The pressure on a sample of water is
   increased by $4.4\times10^{7}\ \text{Pa}$. Find the percentage decrease in its
   volume if $B = 2.2\times10^{9}\ \text{Pa}$. <span class="marks">[5]</span>
5. Show that the energy stored per unit volume of a stretched wire is
   $\frac{1}{2}\times$ stress $\times$ strain. A wire of volume
   $1.0\times10^{-6}\ \text{m}^{3}$ is stretched so that its strain is
   $1.0\times10^{-3}$. Find the energy stored if
   $Y = 2.0\times10^{11}\ \text{Pa}$. <span class="marks">[5]</span>

::: note Answers to Group B
**3.** $F = \dfrac{YAe}{L} = \dfrac{2.0\times10^{11}\times2.0\times10^{-6}\times1.5\times10^{-3}}{3.0} = 200\ \text{N}$.

**4.** $\dfrac{\Delta V}{V} = \dfrac{p}{B} = \dfrac{4.4\times10^{7}}{2.2\times10^{9}} = 0.020$, i.e. a decrease of $2.0\ \%$.

**5.** Outline: work done $= \int_0^e (YA/L)x\,dx = \frac{1}{2}Fe$; divide by volume
$AL$ to get $u = \frac{1}{2}(F/A)(e/L)$. Numerically
$U = \frac{1}{2}Y\varepsilon^{2}V = \frac{1}{2}\times2.0\times10^{11}\times(1.0\times10^{-3})^{2}\times1.0\times10^{-6} = 0.10\ \text{J}$.
:::

**Group C — Long answer (8 marks each)**

1. (a) Define the three elastic moduli and write the expression for each.
   <span class="marks">[3]</span>
   (b) Derive an expression for the elastic potential energy stored in a
   stretched wire and hence for the energy per unit volume.
   <span class="marks">[3]</span>
   (c) A wire of length $2.0\ \text{m}$ and area $1.0\ \text{mm}^{2}$ is
   stretched by $1.0\ \text{mm}$ with $Y = 1.1\times10^{11}\ \text{Pa}$. Find the
   energy stored. <span class="marks">[2]</span>
2. A copper wire and a steel wire, each $2.0\ \text{m}$ long and
   $1.0\ \text{mm}$ in diameter, are joined end to end and a force of
   $100\ \text{N}$ is applied to the free ends. Given
   $Y_{Cu} = 1.1\times10^{11}\ \text{Pa}$ and
   $Y_{St} = 2.0\times10^{11}\ \text{Pa}$, find the stress in each wire, the
   extension of each wire and the total extension. <span class="marks">[8]</span>

::: note Answers to Group C
**1.** (c) $F = YAe/L = (1.1\times10^{11}\times1.0\times10^{-6}\times1.0\times10^{-3})/2.0 = 55\ \text{N}$,
so $U = \frac{1}{2}Fe = \frac{1}{2}\times55\times1.0\times10^{-3} = 2.75\times10^{-2}\ \text{J}$.

**2.** The two wires are in series, so each carries the same force $100\ \text{N}$
and, having the same diameter, the same stress.

$A = \pi d^{2}/4 = 7.854\times10^{-7}\ \text{m}^{2}$, hence
stress $= 100/7.854\times10^{-7} = 1.273\times10^{8}\ \text{Pa}$ in both.

Copper: $e = \text{stress}\times L / Y = (1.273\times10^{8}\times2.0)/1.1\times10^{11} = 2.32\times10^{-3}\ \text{m} = 2.32\ \text{mm}$.

Steel: $e = (1.273\times10^{8}\times2.0)/2.0\times10^{11} = 1.27\times10^{-3}\ \text{m} = 1.27\ \text{mm}$.

Total extension $= 2.32 + 1.27 = 3.59\ \text{mm}$. The copper wire stretches
nearly twice as much because its Young modulus is about half that of steel.
:::
