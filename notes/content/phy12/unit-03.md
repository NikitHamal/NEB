---
subject: Physics
grade: 12
unit: 3
title: Fluid statics
hours: 9
area: Mechanics
---

A fluid is anything that flows. Because a fluid at rest cannot support a
shearing force, its mechanics is written in terms of **pressure** rather than
force. This unit runs from fluids at rest (pressure, upthrust), through the
forces in a liquid **surface** (surface tension, capillarity), to fluids in
motion (viscosity, Poiseuille, Stokes, continuity, Bernoulli).

::: key Where the marks are
Four derivations recur in almost every paper: $P = h\rho g$, the capillary rise
$h = 2T\cos\theta/r\rho g$, terminal velocity from Stokes' law, and Bernoulli's
equation. Learn these four and the numericals become routine.
:::

## 3.1 Fluid statics: Pressure in a fluid; Buoyancy

**Pressure** is the normal force per unit area, $P = F/A$, in pascals
($1\ \text{Pa} = 1\ \text{N m}^{-2}$). It is a **scalar**: at a point in a fluid
at rest it is the same in every direction.

::: derivation Pressure due to a liquid column
Take a horizontal area $A$ at depth $h$ below the free surface of a liquid of
density $\rho$. The column standing on it has volume $Ah$, mass $\rho Ah$ and
weight $\rho Ahg$, all carried by that area:

$$ P = \frac{\rho Ahg}{A} = h\rho g $$
:::

Pressure therefore depends only on **depth**, density and $g$ — never on the
shape of the vessel. The **absolute** pressure is $P = P_0 + h\rho g$; $h\rho g$
alone is the **gauge** pressure. By **Pascal's law** pressure applied to an
enclosed fluid is transmitted undiminished, so a small force on a narrow piston
balances a large load on a wide one — the hydraulic press and brake.

```figure caption="Origin of upthrust. The bottom face lies deeper, so $P_2>P_1$ and the net vertical force $U=(P_2-P_1)A=\rho g V$ acts upwards."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(4.7,3.0))
ax.add_patch(Rectangle((-2.3, -3.1), 4.6, 3.1, facecolor=ACCENT, alpha=0.10,
                       edgecolor='none'))
ax.plot([-2.3, 2.3], [0, 0], color=ACCENT, lw=1.6)
ax.plot([-2.3, -2.3], [0, -3.1], color=INK, lw=1.4)
ax.plot([2.3, 2.3], [0, -3.1], color=INK, lw=1.4)
ax.plot([-2.3, 2.3], [-3.1, -3.1], color=INK, lw=1.4)
ax.add_patch(Rectangle((-0.6, -2.1), 1.2, 0.9, facecolor=ACCENT, alpha=0.40,
                       edgecolor=INK, lw=1.2))
ax.annotate('area $A$', (0, -1.65), color=INK, fontsize=9, ha='center', va='center')
for x, y0, y1, lab, col, ha in [(-1.55, 0, -1.2, '$h_1$', MUTED, 'right'),
                                (-1.95, 0, -2.1, '$h_2$', MUTED, 'right')]:
    ax.plot([x, x], [y0, y1], color=col, lw=0.9, ls=':')
    ax.annotate('', xy=(x, y1), xytext=(x, y0),
                arrowprops=dict(arrowstyle='<|-|>', color=col, lw=0.9, mutation_scale=8))
    ax.annotate(lab, (x-0.08, (y0+y1)/2), color=col, fontsize=9.5, ha=ha, va='center')
ax.plot([-1.95, 0.6], [-2.1, -2.1], color=MUTED, lw=0.7, ls=':')
ax.plot([-1.55, -0.6], [-1.2, -1.2], color=MUTED, lw=0.7, ls=':')
ax.annotate('', xy=(0, -1.32), xytext=(0, -0.62),
            arrowprops=dict(arrowstyle='-|>', color='#A8271F', lw=1.6, mutation_scale=12))
ax.annotate('$F_1=P_1A$', (0.08, -0.80), color='#A8271F', fontsize=9, ha='left')
ax.annotate('', xy=(0, -2.14), xytext=(0, -2.95),
            arrowprops=dict(arrowstyle='-|>', color='#0B6A62', lw=1.8, mutation_scale=13))
ax.annotate('$F_2=P_2A$', (0.10, -2.78), color='#0B6A62', fontsize=9, ha='left')
ax.set_xlim(-2.9, 3.1); ax.set_ylim(-3.6, 0.7)
ax.set_aspect('equal'); ax.axis('off')
```


::: derivation Archimedes' principle from pressure
A cylinder of cross-section $A$ is immersed with its top face at depth $h_1$ and
its bottom face at $h_2$. Sideways forces cancel in pairs; vertically
$F_1 = h_1\rho gA$ acts down and $F_2 = h_2\rho gA$ up. As $h_2 > h_1$ the
resultant — the **upthrust** — acts upwards:

$$ U = F_2 - F_1 = (h_2-h_1)A\rho g = V\rho g $$

Since $V\rho$ is the mass of liquid displaced, the upthrust equals the **weight
of fluid displaced**.
:::

A body floats when the upthrust equals its weight, so a body of density
$\rho_b$ and volume $V$ floating with volume $V_s$ submerged in liquid of
density $\rho_l$ has $V\rho_b g = V_s\rho_l g$, giving

$$ \frac{V_s}{V} = \frac{\rho_b}{\rho_l} $$

Ice ($917\ \text{kg m}^{-3}$) in sea water ($1025\ \text{kg m}^{-3}$) therefore
shows only about $11\%$ of itself above the surface.

::: example Worked example 3.1
**Problem.** (a) Find the absolute pressure $10\ \text{m}$ below the surface of
Phewa Lake. (b) A block weighs $4.9\ \text{N}$ in air and $3.92\ \text{N}$ in
water. Find its volume, density and relative density.
($P_0 = 1.013\times10^{5}\ \text{Pa}$, $\rho_w = 1000\ \text{kg m}^{-3}$,
$g = 9.8\ \text{m s}^{-2}$)

**Solution.**
(a) $P = P_0 + h\rho g = 1.013\times10^{5} + (10)(1000)(9.8) = 1.99\times10^{5}\ \text{Pa}$.

(b) Upthrust $U = 4.9 - 3.92 = 0.98\ \text{N} = V\rho_w g$, so

$$ V = \frac{0.98}{1000 \times 9.8} = 1.0\times10^{-4}\ \text{m}^{3} $$

Mass $= 4.9/9.8 = 0.5\ \text{kg}$, so
$\rho = 0.5/10^{-4} = 5000\ \text{kg m}^{-3}$ and the relative density is $5$.
:::

## 3.2 Surface tension: Theory of surface tension; Surface energy

A needle floats on water and rain gathers into spherical drops: a liquid surface
behaves like a stretched elastic membrane.

::: definition Surface tension
Surface tension is the force per unit length acting on an imaginary line drawn
on a liquid surface, perpendicular to the line and tangential to the surface:
$T = F/L$. Its unit is N m⁻¹ and its dimensions are $[MT^{-2}]$.
:::

**Theory.** Molecules attract one another (**cohesion**) within a *sphere of
influence* of radius about $10^{-9}\ \text{m}$. A molecule deep inside is pulled
equally in all directions, so the resultant on it is zero; one in the surface
layer has liquid only below it and feels a **net inward pull**. Work must be
done to bring a molecule up to the surface, so the liquid keeps its area as
**small as possible** — which is why free drops are spherical.

```figure caption="Molecular explanation of surface tension. Molecule $A$ inside the liquid is pulled equally in all directions; molecule $B$ in the surface has liquid only below it and feels a net inward force."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
fig, ax = plt.subplots(figsize=(4.8,2.8))
ax.add_patch(Rectangle((-2.6, -2.2), 5.2, 2.2, facecolor=ACCENT, alpha=0.10,
                       edgecolor='none'))
ax.plot([-2.6, 2.6], [0, 0], color=ACCENT, lw=1.8)
ax.annotate('free surface', (2.55, 0.12), color=ACCENT, fontsize=8.6, ha='right')
A = np.array([-1.3, -1.15]); B = np.array([1.1, 0.0])
for C, n, half in [(A, 12, False), (B, 12, True)]:
    ax.add_patch(Circle(C, 0.72, facecolor='none', edgecolor=MUTED, lw=0.8, ls='--'))
    for k in range(n):
        an = 2*np.pi*k/n
        if half and np.sin(an) > 0.05:
            continue
        d = np.array([np.cos(an), np.sin(an)])
        ax.annotate('', xy=C + 0.66*d, xytext=C,
                    arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=0.9,
                                    mutation_scale=7))
ax.add_patch(Circle(A, 0.13, facecolor=INK, edgecolor='none'))
ax.add_patch(Circle(B, 0.13, facecolor='#A8271F', edgecolor='none'))
ax.annotate('$A$', A, textcoords='offset points', xytext=(-46, 26), color=INK,
            fontsize=10, ha='center', va='center')
ax.annotate('$B$', B, textcoords='offset points', xytext=(-6, 9), color='#A8271F',
            fontsize=10)
ax.annotate('', xy=(B[0], B[1]-1.35), xytext=(B[0], B[1]-0.80),
            arrowprops=dict(arrowstyle='-|>', color='#A8271F', lw=1.8, mutation_scale=12))
ax.annotate('net inward\nforce', (B[0]+0.16, B[1]-1.20), color='#A8271F',
            fontsize=8.6, ha='left', va='center')
ax.set_xlim(-2.8, 2.8); ax.set_ylim(-2.45, 0.55)
ax.set_aspect('equal'); ax.axis('off')
```


**Surface energy.** A soap film on a frame of width $l$ pulls its light sliding
wire inwards with force $F = 2Tl$ (the $2$ because a film has **two** surfaces).
Pulling the wire out a distance $x$ does work

$$ W = 2Tl \times x = T\,(2lx) = T\,\Delta A $$

since $2lx$ is the increase in surface area, so $T = W/\Delta A$.

::: key Surface tension equals surface energy
Surface energy is the work done in increasing the area by unity (J m⁻²);
surface tension is force per unit length (N m⁻¹). As
$1\ \text{J m}^{-2} = 1\ \text{N m}^{-1}$, the two are numerically equal.
:::

The excess pressure inside a curved surface is $2T/r$ for a drop or an air
bubble in a liquid (one surface) and $4T/r$ for a soap bubble (two). Surface
tension falls as temperature rises and is lowered by detergents.

::: example Worked example 3.2
**Problem.** Find the work done in blowing a soap bubble of radius $3\ \text{cm}$
and the excess pressure inside it, given $T = 0.03\ \text{N m}^{-1}$.

**Solution.** A soap bubble has two surfaces, so the area created is

$$ \Delta A = 2 \times 4\pi r^{2} = 8\pi(0.03)^{2} = 2.26\times10^{-2}\ \text{m}^{2} $$
$$ W = T\,\Delta A = 0.03 \times 2.26\times10^{-2} = 6.79\times10^{-4}\ \text{J} $$

Excess pressure $= \dfrac{4T}{r} = \dfrac{4 \times 0.03}{0.03} = 4\ \text{Pa}$.
:::

## 3.3 Angle of contact, capillarity and its applications

::: definition Angle of contact
The angle of contact is the angle between the tangent to the liquid surface at
the point of contact and the solid surface, measured through the liquid.
:::

Whether it is acute or obtuse depends on the competition between **adhesion**
(liquid–solid attraction) and **cohesion** (liquid–liquid). The rise or fall of
a liquid in a tube of fine bore is called **capillarity**.

| | Water on glass | Mercury on glass |
|---|---|---|
| Stronger force | adhesion | cohesion |
| Meniscus | concave | convex |
| Angle of contact | acute (about $8^{\circ}$, taken as $0^{\circ}$) | obtuse (about $140^{\circ}$) |
| Behaviour | wets glass, **rises** | does not wet, is **depressed** |

```figure caption="Capillarity. Water ($\theta<90^\circ$) has a concave meniscus and rises; mercury ($\theta>90^\circ$) has a convex meniscus and is depressed."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(5.0,3.2))
w = 0.22
def setup(x0, h, concave, col, lab, ang):
    ax.add_patch(Rectangle((x0-1.5, -1.4), 3.0, 1.4, facecolor=col, alpha=0.20,
                           edgecolor='none'))
    ax.plot([x0-1.5, x0+1.5], [0, 0], color=col, lw=1.4)
    ax.plot([x0-1.5, x0-1.5], [0, -1.4], color=INK, lw=1.3)
    ax.plot([x0+1.5, x0+1.5], [0, -1.4], color=INK, lw=1.3)
    ax.plot([x0-1.5, x0+1.5], [-1.4, -1.4], color=INK, lw=1.3)
    ax.plot([x0-w, x0-w], [-1.0, 2.5], color=INK, lw=1.3)
    ax.plot([x0+w, x0+w], [-1.0, 2.5], color=INK, lw=1.3)
    xs = np.linspace(-w, w, 60)
    d = 0.16
    men = h - d*(1-(xs/w)**2) if concave else h + d*(1-(xs/w)**2)
    ax.fill_between(x0+xs, -1.0, men, color=col, alpha=0.40)
    ax.plot(x0+xs, men, color=col, lw=1.4)
    ax.annotate('', xy=(x0+w+0.55, h), xytext=(x0+w+0.55, 0),
                arrowprops=dict(arrowstyle='<|-|>', color='#A8271F', lw=1.0,
                                mutation_scale=9))
    ax.annotate('$h$', (x0+w+0.66, h/2), color='#A8271F', fontsize=10, va='center')
    ax.plot([x0+w, x0+w+0.62], [0, 0], color=MUTED, lw=0.7, ls=':')
    ax.plot([x0+w, x0+w+0.62], [h, h], color=MUTED, lw=0.7, ls=':')
    a = np.radians(ang)
    tipx = x0-w + 0.75*np.cos(a); tipy = h + 0.75*np.sin(a)
    ax.plot([x0-w, tipx], [h, tipy], color='#0B6A62', lw=1.3)
    ax.annotate(r'$\theta$', (x0-w+0.40*np.cos(a/2)-0.12, h+0.40*np.sin(a/2)+0.04),
                color='#0B6A62', fontsize=10)
    ax.annotate(lab, (x0, -1.85), color=INK, fontsize=9, ha='center', va='top')
setup(0.0, 1.55, True, ACCENT, 'water: $\\theta<90^\\circ$, rises', 20)
setup(4.2, -0.55, False, '#8a6d3b', 'mercury: $\\theta>90^\\circ$, falls', -55)
ax.set_xlim(-1.9, 6.3); ax.set_ylim(-2.6, 2.7)
ax.set_aspect('equal'); ax.axis('off')
```


::: derivation Height of liquid in a capillary tube
A tube of internal radius $r$ stands in a liquid of density $\rho$, surface
tension $T$ and angle of contact $\theta$. The liquid touches it along a circle
of length $2\pi r$, and the vertical component of the tension per unit length is
$T\cos\theta$, so the upward force is

$$ F = 2\pi r\,T\cos\theta $$

This supports the weight of the raised column of height $h$,
$W = (\pi r^{2}h)\rho g$. Equating $F = W$,

$$ 2\pi rT\cos\theta = \pi r^{2}h\rho g \qquad \Longrightarrow \qquad
h = \frac{2T\cos\theta}{r\rho g} $$
:::

So $h \propto 1/r$ — the narrower the tube, the higher the rise (**Jurin's
law**). If $\theta > 90^{\circ}$, $\cos\theta$ is negative and $h$ is a
depression, as with mercury.

Applications: oil rises up a lamp wick; sap reaches the leaves of a tree; ink
soaks into blotting paper; and farmers plough their fields to **break** the soil
capillaries, so water is not drawn up and lost by evaporation.

::: caution Internal radius, and the sign of $\cos\theta$
In $h = 2T\cos\theta/r\rho g$, $r$ is the **internal** radius. For water on
clean glass $\cos\theta = 1$, but for mercury $\cos 140^{\circ} = -0.766$: get
that sign wrong and a depression becomes a rise.
:::

::: example Worked example 3.3
**Problem.** Find the rise of water in a capillary tube of internal diameter
$0.4\ \text{mm}$. ($T = 0.072\ \text{N m}^{-1}$,
$\theta = 0^{\circ}$, $\rho = 1000\ \text{kg m}^{-3}$, $g = 9.8\ \text{m s}^{-2}$)

**Solution.** Here $r = 0.2\ \text{mm} = 2\times10^{-4}\ \text{m}$ and
$\cos 0^{\circ} = 1$, so

$$ h = \frac{2T\cos\theta}{r\rho g}
= \frac{2 \times 0.072 \times 1}{(2\times10^{-4})(1000)(9.8)}
= \frac{0.144}{1.96} = 0.0735\ \text{m} $$

The water rises $7.35\ \text{cm}$.
:::

## 3.4 Fluid Dynamics: Newton's formula for viscosity in a liquid; Coefficient of viscosity

In **streamline** (laminar) flow a liquid moves in layers that slide over one
another, each dragging on its neighbours; this internal friction is
**viscosity**. If layers a distance $dx$ apart differ in velocity by $dv$, then
$dv/dx$ is the **velocity gradient**, and Newton found the viscous force on a
contact area $A$ to be

$$ F = -\eta A\frac{dv}{dx} $$

the minus sign showing that it opposes the relative motion.

::: definition Coefficient of viscosity
The coefficient of viscosity is the tangential viscous force per unit area per
unit velocity gradient, $\eta = F/(A\,dv/dx)$. Its SI unit is N s m⁻² (Pa s),
its dimensions are $[ML^{-1}T^{-1}]$, and $1\ \text{Pa s} = 10\ \text{poise}$.
:::

```figure caption="Left: velocity gradient $dv/dx$ between layers of a liquid dragged by a moving plate. Right: the parabolic velocity profile of laminar flow in a tube, used in Poiseuille's formula."
import numpy as np, matplotlib.pyplot as plt
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(5.2,2.6))
# left: plates
ax1.plot([0, 3.2], [0, 0], color=INK, lw=1.8)
for xh in np.linspace(0.05, 3.0, 12):
    ax1.plot([xh, xh+0.16], [0, -0.22], color=MUTED, lw=0.8)
ax1.plot([0, 3.2], [1.8, 1.8], color=INK, lw=1.8)
for y in np.linspace(0.2, 1.8, 6):
    ax1.annotate('', xy=(0.45 + 1.45*y/1.8, y), xytext=(0.45, y),
                 arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.2,
                                 mutation_scale=9))
ax1.annotate('', xy=(2.85, 2.1), xytext=(1.55, 2.1),
             arrowprops=dict(arrowstyle='-|>', color='#A8271F', lw=1.6, mutation_scale=12))
ax1.annotate('$v$', (2.92, 2.1), color='#A8271F', fontsize=10, va='center')
ax1.annotate('fixed plate', (1.6, -0.45), color=MUTED, fontsize=8.4, ha='center', va='top')
ax1.annotate(r'$dv/dx$', (0.35, 1.05), color=ACCENT, fontsize=9.5, ha='right',
             va='center')
ax1.set_xlim(-0.95, 3.6); ax1.set_ylim(-1.0, 2.6)
ax1.set_aspect('equal'); ax1.axis('off')
# right: parabolic profile
R = 0.95
ax2.plot([0, 3.4], [R, R], color=INK, lw=1.8)
ax2.plot([0, 3.4], [-R, -R], color=INK, lw=1.8)
ax2.plot([0, 3.4], [0, 0], color=GRID, lw=0.9, ls='--')
for y in np.linspace(-R*0.92, R*0.92, 9):
    L = 1.7*(1 - (y/R)**2)
    ax2.annotate('', xy=(0.75 + L, y), xytext=(0.75, y),
                 arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.2,
                                 mutation_scale=9))
yy = np.linspace(-R, R, 100)
ax2.plot(0.75 + 1.7*(1-(yy/R)**2), yy, color='#A8271F', lw=1.4)
ax2.annotate('$R$', (0.35, R/2), color=MUTED, fontsize=9.5, ha='center')
ax2.annotate('', xy=(0.45, R), xytext=(0.45, 0),
             arrowprops=dict(arrowstyle='<|-|>', color=MUTED, lw=0.9, mutation_scale=8))
ax2.set_xlim(-0.2, 3.7); ax2.set_ylim(-1.75, 1.75)
ax2.set_aspect('equal'); ax2.axis('off')
```


Viscosity is to fluids what friction is to solids, except that the force depends
on **speed**. Heating makes a liquid **less** viscous (warm honey pours easily)
but a gas **more** viscous.

::: example Worked example 3.4
**Problem.** A plate of area $0.1\ \text{m}^{2}$ is dragged at
$0.5\ \text{m s}^{-1}$ over a $1\ \text{mm}$ layer of oil of viscosity
$0.8\ \text{Pa s}$ on a fixed table. What force is needed?

**Solution.** The velocity falls uniformly to zero across the layer, so
$dv/dx = 0.5/10^{-3} = 500\ \text{s}^{-1}$ and

$$ F = \eta A\frac{dv}{dx} = 0.8 \times 0.1 \times 500 = 40\ \text{N} $$
:::

## 3.5 Poiseuille's formula and its application

For steady laminar flow through a horizontal capillary of radius $r$ and length
$l$ under a pressure difference $P$, the volume flowing per second is

$$ Q = \frac{\pi P r^{4}}{8\eta l} $$

::: derivation Poiseuille's formula by the method of dimensions
Let $Q$ depend on the pressure gradient $P/l$, the radius $r$ and $\eta$:

$$ Q = K\left(\frac{P}{l}\right)^{a} r^{b}\,\eta^{c} $$

With $[Q] = [L^{3}T^{-1}]$, $[P/l] = [ML^{-2}T^{-2}]$, $[r] = [L]$ and
$[\eta] = [ML^{-1}T^{-1}]$,

$$ L^{3}T^{-1} = (ML^{-2}T^{-2})^{a}(L)^{b}(ML^{-1}T^{-1})^{c} $$

Comparing powers of $M$: $a + c = 0$; of $T$: $-2a - c = -1$; of $L$:
$-2a + b - c = 3$. These give $a = 1$, $c = -1$, $b = 4$:

$$ Q = K\frac{Pr^{4}}{\eta l}, \qquad K = \frac{\pi}{8} \text{ from the full theory.} $$
:::

::: key The fourth power of the radius
$Q \propto r^{4}$: halving the radius cuts the flow to **one sixteenth**, which
is why a slight narrowing of an artery makes the heart work so much harder.
:::

It is used to measure $\eta$, to study blood flow, and to fix the bore of
hypodermic needles and drip sets.

::: example Worked example 3.5
**Problem.** Water ($\eta = 1.0\times10^{-3}\ \text{Pa s}$) flows through a
horizontal tube of length $0.5\ \text{m}$ and radius $1\ \text{mm}$ under a
pressure difference of $1000\ \text{Pa}$. Find $Q$, and $Q$ if $r$ is halved.

**Solution.**

$$ Q = \frac{\pi P r^{4}}{8\eta l}
= \frac{\pi (1000)(10^{-3})^{4}}{8(1.0\times10^{-3})(0.5)}
= \frac{\pi \times 10^{-9}}{4\times10^{-3}} = 7.85\times10^{-7}\ \text{m}^{3}\text{s}^{-1} $$

i.e. $0.785\ \text{cm}^{3}\text{s}^{-1}$. Halving $r$ divides $Q$ by $16$,
giving $4.91\times10^{-8}\ \text{m}^{3}\text{s}^{-1}$.
:::

## 3.6 Stokes law and its applications

A small sphere of radius $r$ moving with velocity $v$ through a fluid of
viscosity $\eta$ meets a retarding force

$$ F = 6\pi\eta r v $$

This is **Stokes' law**, valid for slow, streamline motion; dimensional analysis
of $F \propto \eta^{a}r^{b}v^{c}$ gives $a = b = c = 1$.

::: derivation Terminal velocity
A sphere of radius $r$ and density $\rho$ falling through a liquid of density
$\sigma$ feels its weight down, and upthrust and drag up. The drag grows with
speed until the three balance and the sphere falls at a constant **terminal
velocity** $v_t$:

$$ \tfrac{4}{3}\pi r^{3}\rho g = \tfrac{4}{3}\pi r^{3}\sigma g + 6\pi\eta r v_t $$

$$ 6\pi\eta r v_t = \tfrac{4}{3}\pi r^{3}(\rho - \sigma)g
\qquad \Longrightarrow \qquad v_t = \frac{2r^{2}(\rho-\sigma)g}{9\eta} $$
:::

```figure caption="A sphere falling through a viscous liquid. When weight is balanced by upthrust plus drag the velocity becomes constant at the terminal value $v_t$."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(5.2,2.8),
                               gridspec_kw={'width_ratios':[1, 1.25]})
ax1.add_patch(Rectangle((-1.25, -2.6), 2.5, 3.8, facecolor=ACCENT, alpha=0.12,
                        edgecolor=INK, lw=1.2))
ax1.plot([-1.25, 1.25], [1.2, 1.2], color=ACCENT, lw=1.5)
C = np.array([0.0, -0.45])
ax1.add_patch(Circle(C, 0.30, facecolor=MUTED, edgecolor=INK, lw=1.1))
ax1.annotate('', xy=(C[0], C[1]-1.55), xytext=(C[0], C[1]-0.38),
             arrowprops=dict(arrowstyle='-|>', color='#A8271F', lw=1.7, mutation_scale=12))
ax1.annotate('$mg$', (C[0]+0.10, C[1]-1.15), color='#A8271F', fontsize=9, ha='left')
ax1.annotate('', xy=(C[0]-0.42, C[1]+1.45), xytext=(C[0]-0.42, C[1]+0.30),
             arrowprops=dict(arrowstyle='-|>', color='#0B6A62', lw=1.6, mutation_scale=12))
ax1.annotate('$U$', (C[0]-0.52, C[1]+1.05), color='#0B6A62', fontsize=9, ha='right')
ax1.annotate('', xy=(C[0]+0.42, C[1]+1.45), xytext=(C[0]+0.42, C[1]+0.30),
             arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.6, mutation_scale=12))
ax1.annotate(r'$6\pi\eta rv$', (C[0]+0.52, C[1]+1.05), color=ACCENT, fontsize=9, ha='left')
ax1.set_xlim(-1.9, 2.0); ax1.set_ylim(-2.9, 1.7)
ax1.set_aspect('equal'); ax1.axis('off')
t = np.linspace(0, 5, 300)
ax2.plot(t, 1 - np.exp(-1.35*t), color=ACCENT, lw=1.8)
ax2.axhline(1.0, color='#A8271F', lw=1.2, ls='--')
ax2.annotate('$v_t$', (4.6, 1.06), color='#A8271F', fontsize=10, ha='right')
ax2.set_xlabel('time  $t$'); ax2.set_ylabel('velocity  $v$')
ax2.set_xticks([]); ax2.set_yticks([])
ax2.set_ylim(0, 1.32); ax2.set_xlim(0, 5)
ax2.spines[['top','right']].set_visible(False)
```


Applications: **Millikan's oil-drop experiment** finds the drop radius and hence
the electronic charge; since $v_t \propto r^{2}$ tiny droplets float as cloud
while large drops fall fast; and $\eta$ is found by timing a ball-bearing falling through the liquid.

::: example Worked example 3.6
**Problem.** A steel ball of radius $1\ \text{mm}$ and density
$7800\ \text{kg m}^{-3}$ falls through oil of density $900\ \text{kg m}^{-3}$
and viscosity $1.0\ \text{Pa s}$. Find $v_t$.

**Solution.**

$$ v_t = \frac{2r^{2}(\rho-\sigma)g}{9\eta}
= \frac{2(10^{-3})^{2}(7800-900)(9.8)}{9 \times 1.0}
= 1.50\times10^{-2}\ \text{m s}^{-1} $$

i.e. about $1.5\ \text{cm s}^{-1}$.
:::

## 3.7 Equation of continuity and its applications

Take steady, incompressible flow through a tube whose cross-section changes from
$A_1$ to $A_2$. In time $\Delta t$ the liquid entering occupies a length
$v_1\Delta t$, so the mass entering is $\rho A_1v_1\Delta t$ and that leaving is
$\rho A_2v_2\Delta t$. No liquid is created or lost, so

$$ \rho A_1v_1 = \rho A_2 v_2 \qquad \Longrightarrow \qquad A_1v_1 = A_2v_2 = \text{constant} $$

This is the **equation of continuity** — the conservation of mass. Since
$v \propto 1/A$, **a fluid speeds up where the pipe narrows**: a thumb over a
hosepipe makes water shoot further, and a river runs fast through a gorge but
slow over a plain.

::: example Worked example 3.7
**Problem.** Water flows at $2\ \text{m s}^{-1}$ through a pipe of internal
diameter $6\ \text{cm}$ that narrows to $3\ \text{cm}$. Find the speed there and
the volume flow rate.

**Solution.** Since $A \propto d^{2}$,

$$ v_2 = v_1\left(\frac{d_1}{d_2}\right)^{2} = 2\left(\frac{6}{3}\right)^{2}
= 8\ \text{m s}^{-1} $$
$$ Q = A_1v_1 = \pi(0.03)^{2}(2) = 5.65\times10^{-3}\ \text{m}^{3}\text{s}^{-1}
= 5.65\ \text{litre s}^{-1} $$
:::

## 3.8 Bernoulli's equation and its applications

::: definition Bernoulli's principle
For the steady streamline flow of an ideal (non-viscous, incompressible) fluid,
the sum of pressure, kinetic and potential energy per unit volume is constant
along a streamline:

$$ P + \tfrac{1}{2}\rho v^{2} + \rho gh = \text{constant} $$
:::

::: derivation Bernoulli's equation from the work–energy theorem
Take a tube of flow with sections $A_1$ (height $h_1$, pressure $P_1$, speed
$v_1$) and $A_2$ (height $h_2$, pressure $P_2$, speed $v_2$). In time $\Delta t$
a mass $m = \rho V$ enters one end and an equal mass leaves the other, where
$V = A_1v_1\Delta t = A_2v_2\Delta t$. The entry pressure does work $P_1V$ and
work $P_2V$ is done against the exit pressure, so $W = (P_1-P_2)V$. By the
work–energy theorem this is the gain in kinetic plus potential energy:

$$ (P_1-P_2)V = \left(\tfrac{1}{2}mv_2^{2} - \tfrac{1}{2}mv_1^{2}\right)
+ (mgh_2 - mgh_1) $$

Putting $m = \rho V$ and dividing by $V$,

$$ P_1 + \tfrac{1}{2}\rho v_1^{2} + \rho gh_1
= P_2 + \tfrac{1}{2}\rho v_2^{2} + \rho gh_2 $$
:::

```figure caption="Venturi meter. By continuity the liquid speeds up in the throat; by Bernoulli's equation its pressure there falls, so the manometer column is shorter."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,2.9))
xs = np.array([0.0, 1.5, 2.3, 3.3, 4.1, 5.6])
ys = np.array([0.80, 0.80, 0.34, 0.34, 0.80, 0.80])
ax.plot(xs, ys, color=INK, lw=1.6)
ax.plot(xs, -ys, color=INK, lw=1.6)
xf = np.linspace(0, 5.6, 300)
up = np.interp(xf, xs, ys)
ax.fill_between(xf, -up, up, color=ACCENT, alpha=0.13)
for frac in (0.34, 0.68):
    ax.plot(xf, frac*up, color=ACCENT, lw=0.8, alpha=0.75)
    ax.plot(xf, -frac*up, color=ACCENT, lw=0.8, alpha=0.75)
ax.plot(xf, 0*xf, color=ACCENT, lw=0.8, alpha=0.75)
ax.annotate('', xy=(1.05, 0), xytext=(0.45, 0),
            arrowprops=dict(arrowstyle='-|>', color='#A8271F', lw=1.5, mutation_scale=11))
ax.annotate('$v_1$', (0.72, 0.13), color='#A8271F', fontsize=9.5, ha='center')
ax.annotate('', xy=(3.25, 0), xytext=(2.35, 0),
            arrowprops=dict(arrowstyle='-|>', color='#A8271F', lw=1.5, mutation_scale=11))
ax.annotate('$v_2$', (2.80, 0.13), color='#A8271F', fontsize=9.5, ha='center')
for x0, htop, lab in [(0.85, 2.30, '$P_1$'), (2.80, 1.45, '$P_2$')]:
    ax.plot([x0-0.11, x0-0.11], [np.interp(x0, xs, ys), 2.55], color=INK, lw=1.2)
    ax.plot([x0+0.11, x0+0.11], [np.interp(x0, xs, ys), 2.55], color=INK, lw=1.2)
    ax.fill_between([x0-0.11, x0+0.11], np.interp(x0, xs, ys), htop,
                    color=ACCENT, alpha=0.45)
    ax.plot([x0-0.11, x0+0.11], [htop, htop], color=ACCENT, lw=1.2)
    ax.annotate(lab, (x0+0.20, htop-0.22), color=INK, fontsize=9.5, ha='left')
ax.plot([0.74, 3.35], [2.30, 2.30], color=MUTED, lw=0.7, ls=':')
ax.annotate('', xy=(3.25, 1.45), xytext=(3.25, 2.30),
            arrowprops=dict(arrowstyle='<|-|>', color='#0B6A62', lw=1.0, mutation_scale=9))
ax.annotate('$h$', (3.36, 1.88), color='#0B6A62', fontsize=10, va='center')
ax.annotate('$A_1$', (0.35, -1.10), color=MUTED, fontsize=9.5, ha='center')
ax.annotate('$A_2$', (2.80, -0.72), color=MUTED, fontsize=9.5, ha='center')
ax.set_xlim(-0.4, 6.0); ax.set_ylim(-1.35, 2.85)
ax.set_aspect('equal'); ax.axis('off')
```


**Applications.**

1. **Venturi meter.** In a horizontal pipe $h_1 = h_2$, so
   $P_1 - P_2 = \frac{1}{2}\rho(v_2^{2}-v_1^{2})$; with $A_1v_1 = A_2v_2$ the
   measured pressure difference gives the rate of flow.
2. **Torricelli's theorem.** For a hole a depth $h$ below the free surface of an
   open tank the pressure is atmospheric at both points and the surface speed is
   negligible, so $\frac{1}{2}\rho v^{2} = \rho gh$, giving $v = \sqrt{2gh}$ —
   the speed of free fall through the same height.
3. **Aerofoil lift.** Air travels faster over the curved upper surface of a
   wing, so the pressure above is lower and there is a net upward force — the
   same effect lifts a tin roof off in a storm.
4. **Atomiser and Bunsen burner.** Fast air across the top of a tube lowers the
   pressure there, and atmospheric pressure drives the liquid up.

::: caution Bernoulli's equation has conditions
It holds only for **steady, streamline, non-viscous, incompressible** flow and
only **along one streamline**. Do not use it for turbulent flow, or for a real
viscous liquid in a long pipe where energy is lost as heat.
:::

## Chapter summary

- $P = h\rho g$ (gauge), $P = P_0 + h\rho g$ (absolute); pressure depends on
  depth only, and Pascal's law transmits it undiminished.
- Upthrust $U = V\rho g$ = weight of fluid displaced; a floating body has
  $V_s/V = \rho_b/\rho_l$.
- $T = F/L$ (N m⁻¹) equals the surface energy $W/\Delta A$ (J m⁻²). Excess
  pressure: $2T/r$ in a drop, $4T/r$ in a soap bubble.
- Capillary rise $h = 2T\cos\theta/r\rho g$, so $h \propto 1/r$.
- Viscosity $F = \eta A\,dv/dx$, $\eta$ in Pa s, $[ML^{-1}T^{-1}]$.
- Poiseuille $Q = \pi P r^{4}/8\eta l$ — the **fourth power** of the radius.
- Stokes $F = 6\pi\eta rv$, giving $v_t = 2r^{2}(\rho-\sigma)g/9\eta$.
- Continuity $A_1v_1 = A_2v_2$ (mass) and Bernoulli
  $P + \frac{1}{2}\rho v^{2} + \rho gh = \text{constant}$ (energy), giving
  $v = \sqrt{2gh}$ for efflux.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The SI unit of the coefficient of viscosity is <span class="marks">[1]</span>
   (a) poise (b) Pa s (c) N s⁻¹ (d) m² s⁻¹
2. A body floats in water with three-quarters of its volume submerged. Its
   relative density is <span class="marks">[1]</span>
   (a) $0.25$ (b) $0.50$ (c) $0.75$ (d) $1.33$
3. Water rises to a height $h$ in a capillary tube of radius $r$. In a tube of
   radius $r/2$ it rises to <span class="marks">[1]</span>
   (a) $h/2$ (b) $h$ (c) $2h$ (d) $4h$
4. In Poiseuille's formula $Q$ is proportional to <span class="marks">[1]</span>
   (a) $r$ (b) $r^{2}$ (c) $r^{3}$ (d) $r^{4}$
5. Bernoulli's equation expresses the conservation of <span class="marks">[1]</span>
   (a) mass (b) momentum (c) energy (d) angular momentum

::: note Answers to Group A
**1.** (b) — from $\eta = F/(A\,dv/dx)$, the unit is N s m⁻² = Pa s.
**2.** (c) — the fraction submerged equals the ratio of densities.
**3.** (c) — $h \propto 1/r$.
**4.** (d) — $Q = \pi Pr^{4}/8\eta l$.
**5.** (c) — it is the work–energy theorem per unit volume of fluid.
:::

**Group B — Short answer (5 marks each)**

1. Define surface tension and surface energy and show that they are numerically
   equal. <span class="marks">[5]</span>
2. A capillary tube of internal radius $0.5\ \text{mm}$ is dipped vertically in
   water of surface tension $0.072\ \text{N m}^{-1}$. Calculate the rise.
   ($\theta = 0^{\circ}$, $\rho = 1000\ \text{kg m}^{-3}$) <span class="marks">[5]</span>
3. State Stokes' law and derive the terminal velocity of a sphere in a viscous
   liquid. Hence find the terminal velocity of an air bubble of radius
   $1\ \text{mm}$ rising through a liquid of density $1200\ \text{kg m}^{-3}$
   and viscosity $0.5\ \text{Pa s}$. <span class="marks">[5]</span>
4. Water flows at $3\ \text{m s}^{-1}$ along a horizontal pipe of cross-section
   $10\ \text{cm}^{2}$, which narrows to $5\ \text{cm}^{2}$. Find the speed
   there and the pressure difference between the two sections. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Outline: $T = F/L$; surface energy $= W/\Delta A$. For a film on a frame
of width $l$ pulled out a distance $x$, $W = 2Tl\,x = T(2lx) = T\Delta A$, so
$1\ \text{N m}^{-1} = 1\ \text{J m}^{-2}$.

**2.** $h = \dfrac{2T\cos\theta}{r\rho g}
= \dfrac{2(0.072)}{(5\times10^{-4})(1000)(9.8)} = \dfrac{0.144}{4.9}
= 0.0294\ \text{m} = 2.94\ \text{cm}$.

**3.** For a rising bubble the upthrust exceeds the weight; taking the air
density as negligible,
$v_t = \dfrac{2r^{2}\sigma g}{9\eta}
= \dfrac{2(10^{-3})^{2}(1200)(9.8)}{9(0.5)} = 5.23\times10^{-3}\ \text{m s}^{-1}$,
about $5.2\ \text{mm s}^{-1}$ upwards.

**4.** $v_2 = A_1v_1/A_2 = (10 \times 3)/5 = 6\ \text{m s}^{-1}$; for a
horizontal pipe $P_1 - P_2 = \frac{1}{2}\rho(v_2^{2}-v_1^{2})
= \frac{1}{2}(1000)(36-9) = 1.35\times10^{4}\ \text{Pa}$.

:::

**Group C — Long answer (8 marks each)**

1. (a) Define angle of contact and explain why water wets glass but mercury does
   not. <span class="marks">[3]</span>
   (b) Derive an expression for the rise of a liquid in a capillary tube and
   calculate the rise of water in a tube of internal radius $0.1\ \text{mm}$.
   ($T = 0.072\ \text{N m}^{-1}$, $\theta = 0^{\circ}$,
   $\rho = 1000\ \text{kg m}^{-3}$) <span class="marks">[5]</span>
2. (a) State Bernoulli's principle and derive Bernoulli's equation for the
   streamline flow of an ideal liquid. <span class="marks">[5]</span>
   (b) A tank on the ground holds water to a depth of $3\ \text{m}$. A small hole
   is made in its side $1.2\ \text{m}$ below the surface. Find the speed of
   efflux and how far from the foot of the tank the jet strikes the ground. <span class="marks">[3]</span>

::: note Answers to Group C
**1.(b)** $h = \dfrac{2T\cos\theta}{r\rho g}
= \dfrac{2(0.072)}{(10^{-4})(1000)(9.8)} = \dfrac{0.144}{0.98}
= 0.147\ \text{m} = 14.7\ \text{cm}$.

**2.(b)** $v = \sqrt{2gh} = \sqrt{2(9.8)(1.2)} = 4.85\ \text{m s}^{-1}$. The
hole is $1.8\ \text{m}$ above the ground and the jet leaves horizontally, so
$t = \sqrt{2(1.8)/9.8} = 0.606\ \text{s}$ and $x = vt = 2.94\ \text{m}$.
:::
