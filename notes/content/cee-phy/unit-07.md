---
subject: Physics
grade: CEE
unit: 7
title: Elasticity
hours: 1
area: Mechanics
---

Elasticity explains why a steel bridge bends under a truck and springs back, why a
rubber band stretches so much more than a steel wire of the same size, and why a
glass window cracks while a copper pipe dents. Of the **10 Mechanics questions**
(official weightage), we estimate about **1** comes from this chapter. It is a
formula chapter with a small number of ideas: stress over strain, the three moduli,
Poisson's ratio, and the energy stored in a stretched wire. Most marks are lost on
two things — mixing up which modulus belongs to which deformation, and forgetting
that a wire's extension depends on length and on the *square* of the diameter.

::: key What the paper asks from this chapter
- Stress $=F/A$ (Pa) and strain (no unit); Hooke's law: stress $\propto$ strain up to the proportional limit.
- $Y=\frac{F/A}{\Delta L/L}=\frac{FL}{A\,\Delta L}$; extension $\Delta L=\frac{FL}{AY}$, so $\Delta L \propto L/d^2$.
- $K=-\frac{\Delta P}{\Delta V/V}$ (all states of matter); $G=\frac{F/A}{\theta}$ (solids only).
- Poisson's ratio $\sigma=-\frac{\Delta d/d}{\Delta L/L}$, dimensionless, 0 to 0.5 for ordinary materials.
- Elastic energy $U=\frac{1}{2}F\Delta L=\frac{1}{2}kx^2$; energy density $u=\frac{1}{2}\times\text{stress}\times\text{strain}$.
- Young's modulus is a property of the **material**, not of the wire's length or thickness.
:::

## 7.1 Stress, strain and Hooke's law

### Deforming force, elasticity and plasticity

A **deforming force** changes the shape or size of a body. The body's own
intermolecular forces oppose the change and try to restore the original shape; this
is the **restoring force**.

::: definition Elasticity
**Elasticity** is the property of a body by which it regains its original shape and
size when the deforming force is removed. **Plasticity** is the property by which it
does **not** — the deformation remains.
:::

- A **perfectly elastic** body returns exactly to its original shape (quartz, and
  steel within its elastic limit, come close).
- A **perfectly plastic** body keeps the new shape (putty, mud, lead beyond its
  elastic limit).
- No real material is perfectly either; the difference is how large the elastic
  range is.

A note on language: physicists call **steel more elastic than rubber**, even though
rubber stretches much more. Elasticity is measured by the modulus — for the same
stress, the material that strains less is the more elastic one. Rubber is
*stretchier*, not more elastic.

### Stress and its kinds

::: definition Stress
**Stress** is the internal restoring force set up per unit area of cross-section:
$\sigma=F/A$. SI unit: N m⁻², called the **pascal** (Pa). Dimensions
$[ML^{-1}T^{-2}]$.
:::

Stress is **not** pressure, although the units are the same. Pressure acts on a
surface from outside and is always compressive; stress is set up *inside* the
material and can be tensile, compressive or tangential.

| Type of stress | Force direction | Example | Modulus that pairs with it |
|---|---|---|---|
| Tensile | perpendicular, pulling apart | a wire hanging a load | Young's modulus $Y$ |
| Compressive | perpendicular, pushing together | a pillar carrying a roof | Young's modulus $Y$ |
| Shear (tangential) | parallel to the surface | a book pushed sideways on a table; a rivet | modulus of rigidity $G$ |
| Volumetric (hydraulic) | perpendicular, from all sides | a ball sunk deep in water | bulk modulus $K$ |

### Strain

::: definition Strain
**Strain** is the fractional change in dimension produced by the stress. It has
**no unit** and no dimensions.
:::

| Type of strain | Definition | Written as |
|---|---|---|
| Longitudinal (tensile) | change in length / original length | $\Delta L/L$ |
| Volumetric | change in volume / original volume | $\Delta V/V$ |
| Shear | displacement of one face / distance between faces | $\Delta x/L=\tan\theta\approx\theta$ |

For small angles $\tan\theta\approx\theta$ in radians, so shear strain is numerically
the **angle of shear** in radians. Being a ratio of two lengths, strain is
dimensionless — a point the paper tests often.

### Hooke's law

::: definition Hooke's law
Within the **elastic limit**, the stress produced in a body is directly proportional
to the strain:
$\text{stress}\propto\text{strain}$, or $\text{stress}=E\times\text{strain}$,
where $E$ is the modulus of elasticity of the material.
:::

For a spring or a wire, the same law is written in terms of force and extension:

$$ F = k\,\Delta L $$

where $k$ is the **force constant** (spring constant), N m⁻¹. For a wire,
$k=YA/L$ — a short, thick wire is stiff, a long, thin one is soft.

The constant of proportionality between stress and strain is the **modulus of
elasticity**. Its value is large for a stiff material (steel) and small for a soft
one (rubber). Because strain has no unit, the modulus has the same unit as stress,
the pascal.

::: caution Stress is not pressure, and strain is not a length
Stress is force per unit area **inside** the material; strain is a **ratio**. A
strain of $10^{-3}$ means the wire grew by 0.1 % — not by 1 mm, unless you multiply
by the original length. Options that give strain a unit (m, m m⁻¹, rad) are always
wrong; only shear strain can be *quoted* in radians, and even then it is
dimensionless.
:::

### The stress–strain curve

Stretch a wire slowly, recording stress against strain. The shape of the graph is
the material's signature.

| Point on the graph | What happens |
|---|---|
| O to A — straight line | stress $\propto$ strain; Hooke's law holds; the slope is the modulus |
| A — **proportional limit** | the straight line ends; proportionality stops, elasticity may not |
| B — **elastic limit** (yield point) | beyond this the wire does not return to its original length |
| B to C — plastic region | large strain for little extra stress; the material flows |
| C — **ultimate tensile strength** | the greatest stress the material can bear |
| C to D — necking | the wire thins locally and stress falls |
| D — **breaking point** | the wire snaps |

The curve above is for a **ductile** metal. A **brittle** material such as glass or
cast iron has almost no plastic region: the line stays straight nearly to the
breaking point, so a glass rod gives no warning before it snaps. An **elastomer**
behaves differently again — it stretches a long way at low stress and then stiffens
as the polymer chains line up.

```figure caption="A typical stress–strain curve for a ductile metal. The straight part OA gives the modulus; beyond the elastic limit B the material deforms permanently, reaches its greatest stress at C, and breaks at D."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,2.9))
e1 = np.linspace(0, 0.004, 40); s1 = 250*e1
e2 = np.linspace(0.004, 0.030, 200); s2 = 1.0 + 0.55*(1 - np.exp(-(e2-0.004)/0.007))
e3 = np.linspace(0.030, 0.040, 60); s3 = 1.55 - 0.45*(e3-0.030)/0.010
ax.plot(e1, s1, color=ACCENT, lw=2.0)
ax.plot(e2, s2, color=ACCENT, lw=2.0)
ax.plot(e3, s3, color=ACCENT, lw=2.0)
for ex, sy, lab, dx, dy in [(0.004,1.00,'A',0.0012,-0.10), (0.008,1.24,'B',0.0012,0.06),
                            (0.030,1.55,'C',-0.0018,0.07), (0.040,1.10,'D',0.0014,0.02)]:
    ax.plot([ex],[sy],'o',color='#A8271F',ms=4,zorder=5)
    ax.text(ex+dx, sy+dy, lab, fontsize=9, color='#A8271F')
ax.annotate('slope = Young modulus', xy=(0.0016,0.40), xytext=(0.0055,0.28), fontsize=8,
            color=MUTED, arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.7))
ax.text(0.0245, 1.16, 'A  proportional limit\nB  elastic limit\nC  ultimate strength\nD  breaking point',
        fontsize=7.8, color=INK, va='top', linespacing=1.45)
ax.set_xlabel('strain  ε  (not to scale)'); ax.set_ylabel('stress  σ')
ax.set_xlim(0,0.045); ax.set_ylim(0,1.75)
ax.set_xticks([]); ax.set_yticks([])
ax.spines[['top','right']].set_visible(False)
```

### Ductile, brittle and elastomeric materials

| Behaviour | Description | Examples |
|---|---|---|
| Ductile | long plastic region; can be drawn into wires | copper, mild steel, aluminium |
| Brittle | breaks soon after the elastic limit, almost no plastic region | glass, cast iron, concrete, chalk |
| Elastomer | stretches enormously, is not Hookean, and does not retrace its curve | rubber, silicone |

Rubber's curve does not come back along the same path: the unloading curve lies
**below** the loading curve, and the area between them is energy converted to heat.
This is **elastic hysteresis**; it is why a rubber ball bounces lower each time and
why car tyres warm up.

### Elastic fatigue and elastic after-effect

A material that is loaded and unloaded many times becomes weaker: its elastic limit
falls, and it may break under a load it once carried easily. This is **elastic
fatigue** — the reason a piece of wire snaps after being bent to and fro at the same
place, and the reason a bridge is never designed to work near its breaking stress.

Some materials also do not recover instantly when the load is removed; the strain
lags behind the stress. This slow recovery is the **elastic after-effect**
(anelasticity), shown clearly by glass and lead.

### What changes the modulus

| Change | Effect on elasticity |
|---|---|
| Rise in temperature | elasticity usually **decreases** (metals soften); rubber is the exception and stiffens on heating |
| Adding an impurity | usually increases the modulus — carbon in steel makes it stiffer |
| Annealing (slow cooling) | softens the metal, lowers the modulus, increases ductility |
| Hammering and cold working | hardens the metal and raises the elastic limit, but makes it more brittle |

### Factor of safety

No structure is designed to work at its breaking stress. Engineers divide the
breaking stress by a number — the **factor of safety**:

$$ \text{factor of safety} = \frac{\text{breaking stress}}{\text{working stress}} $$

For bridges, lifts and pressure vessels it is typically 5 to 10. A steel cable whose
breaking stress is $1.0\times10^9$ Pa, used at a working stress of
$1.0\times10^8$ Pa, has a factor of safety of 10. A factor below 1 would mean the
working stress already exceeds the breaking stress, so the part would fail as soon
as it carried its design load.

::: tip Two conversions decide most numericals
$1\ \text{mm} = 10^{-3}$ m, $1\ \text{mm}^2 = 10^{-6}$ m², $1\ \text{cm}^2 = 10^{-4}$ m².
A diameter of 2 mm is a radius of $1\times10^{-3}$ m, so the area is
$\pi(10^{-3})^2 = 3.1\times10^{-6}$ m². Nearly every wrong option in this chapter
comes from using the diameter as the radius, or mm² as m².
:::

## 7.2 Young's modulus, bulk modulus and modulus of rigidity; Poisson's ratio

### Young's modulus

For a wire of original length $L$, area $A$, stretched by $\Delta L$ under a force
$F$, the tensile stress is $F/A$ and the longitudinal strain is $\Delta L/L$. Their
ratio is **Young's modulus**:

$$ Y = \frac{F/A}{\Delta L/L} = \frac{FL}{A\,\Delta L} $$

Rearranged, the extension is

$$ \Delta L = \frac{FL}{AY} = \frac{4FL}{\pi d^2 Y} $$

so for the same material and load,

$$ \Delta L \propto \frac{L}{d^2} $$

- double the length → double the extension;
- double the diameter → **one quarter** of the extension;
- double both → **half** the extension.

Young's modulus is a property of the **material** (and of its temperature), not of
the particular wire. A long thin wire and a short thick one cut from the same steel
have the same $Y$; only their extensions differ.

| Material | $Y$ (10¹⁰ Pa) |
|---|---|
| Steel | 20 |
| Copper | 11 |
| Brass | 9.1 |
| Aluminium | 7.0 |
| Glass | 6.5 |
| Bone | 1.5 |
| Rubber | 0.01–0.1 |

::: caution Y does not depend on the size of the wire
A question may say "a wire of twice the length and half the diameter is made of the
same material — what happens to Young's modulus?" The answer is **nothing**. $Y$ is
fixed by the material. What changes is the extension, and it changes by
$(2)/(1/2)^2 = 8$ times.
:::

### A wire hanging under its own weight

A vertical wire of length $L$, area $A$ and density $\rho$ stretches under its own
weight. At a distance $x$ above the free end the tension is the weight of the wire
below that point, $\rho A g x$. A slice of thickness $dx$ therefore extends by

$$ d(\Delta L) = \frac{\rho A g x\,dx}{AY} $$

Integrating from $x=0$ to $x=L$:

$$ \Delta L = \frac{\rho g L^2}{2Y} = \frac{MgL}{2AY} $$

where $M=\rho AL$ is the mass of the wire. This is **half** the extension the same
wire would have if its whole weight hung from its end, because the tension grows
from zero at the bottom to $Mg$ at the top.

### Bulk modulus and compressibility

When a body is subjected to a uniform pressure change $\Delta P$ from all sides, its
volume changes by $\Delta V$. The **bulk modulus** is

$$ K = -\frac{\Delta P}{\Delta V/V} = -V\frac{dP}{dV} $$

The minus sign keeps $K$ positive: an increase in pressure **decreases** the volume,
so $\Delta V$ is negative. $K$ applies to **solids, liquids and gases** — it is the
one modulus every state of matter has.

The reciprocal of the bulk modulus is the **compressibility**:

$$ \text{compressibility} = \frac{1}{K} = -\frac{1}{V}\frac{dV}{dP} $$

A large $K$ means a stiff, hard-to-compress material: steel $K\approx1.6\times10^{11}$
Pa, water $2.2\times10^9$ Pa, air about $1.0\times10^5$ Pa. Water's bulk modulus is
large, which is why a depth of 100 m changes its volume by less than 0.05 %.

::: caution The bulk modulus of a gas depends on the process
For a gas, $K$ is not a single number:
- **isothermal** change (temperature held constant): $K=P$;
- **adiabatic** change (no heat exchanged): $K=\gamma P$, where $\gamma=C_P/C_V$.

For air $\gamma=1.4$, so the adiabatic value is 1.4 times the isothermal one. Sound
waves compress the air so quickly that no heat has time to flow, so the speed of
sound uses $v=\sqrt{\gamma P/\rho}$, not $\sqrt{P/\rho}$. If a question says
"isothermal", use $P$; if it says "adiabatic" or "sound", use $\gamma P$.
:::

### Modulus of rigidity (shear modulus)

A **shear** deformation changes the shape but not the volume: one face of a solid is
displaced sideways relative to the opposite face, which is held fixed.

$$ G = \frac{\text{shear stress}}{\text{shear strain}} = \frac{F/A}{\theta} $$

where $\theta$ is the angle of shear in radians. The unit is the pascal. $G$ is also
called the **shear modulus** or modulus of rigidity.

Only **solids** have rigidity. A liquid or a gas cannot sustain a permanent shear
stress — it flows — so $G=0$ for liquids and gases. Steel has
$G\approx8\times10^{10}$ Pa, about 40 % of its Young's modulus.

::: memory Which modulus?
Stretch a rod — **Young**. Squash a volume — **Bulk**. Slide a face — **Rigidity**.
Shrink a waist — **Poisson**.
:::

::: tip Ratio questions in one line
For the same material and the same load,
$\Delta L_2/\Delta L_1 = (L_2/L_1)(d_1/d_2)^2$. Write that ratio down before touching
any numbers: most of these questions need no arithmetic beyond a square.
:::

::: example Worked example 7.1 — shear of a rivet
**Problem.** A rivet of cross-section 2.0 cm² and thickness 8.0 mm is sheared
sideways by a force of 4000 N, and the sheared face is displaced by 0.020 mm. Find
the shear stress, the shear strain and the modulus of rigidity.

**Solution.** $A = 2.0\ \text{cm}^2 = 2.0\times10^{-4}$ m².

Shear stress $= F/A = 4000/2.0\times10^{-4} = 2.0\times10^7$ Pa.

Shear strain $= \Delta x/L = 0.020/8.0 = 2.5\times10^{-3}$ rad.

$$ G = \frac{2.0\times10^7}{2.5\times10^{-3}} = 8.0\times10^9\ \text{Pa} $$

The two displacements are in the same unit (mm), so the strain is a pure ratio — no
conversion is needed for it.
:::

### Poisson's ratio

When a wire is stretched, it gets longer **and thinner**. The lateral contraction is
a real strain, and its ratio to the longitudinal strain is **Poisson's ratio**:

$$ \sigma = -\frac{\text{lateral strain}}{\text{longitudinal strain}} = -\frac{\Delta d/d}{\Delta L/L} $$

The minus sign makes $\sigma$ positive for ordinary materials, because $\Delta d$ and
$\Delta L$ have opposite signs. $\sigma$ is **dimensionless**.

| Value of $\sigma$ | Meaning | Example |
|---|---|---|
| 0 | no lateral contraction at all | cork |
| 0.2–0.4 | typical metals | steel 0.28–0.30, copper 0.33 |
| 0.5 | volume stays constant while stretching | rubber |

The theoretical range is $-1$ to $0.5$; ordinary materials lie between 0 and 0.5.
Cork's near-zero value is why it is used for bottle stoppers — it can be pushed into
a neck without swelling sideways.

```figure caption="The three basic deformations and the strain each produces. Tensile and compressive strains are measured along the force; shear strain is the angle θ; volumetric strain is the fractional change in volume."
import numpy as np, matplotlib.pyplot as plt
fig, axs = plt.subplots(1, 3, figsize=(5.0, 2.5))
for ax in axs:
    ax.set_xlim(-1.15, 1.15); ax.set_ylim(-1.20, 1.10)
    ax.axis('off'); ax.set_aspect('equal')
# (a) tensile
ax = axs[0]
ax.add_patch(plt.Rectangle((-0.30,-0.20), 0.60, 0.40, fc='none', ec=MUTED, ls='--', lw=1.0))
ax.add_patch(plt.Rectangle((-0.42,-0.16), 0.84, 0.32, fc=ACCENT, alpha=0.15, ec=ACCENT, lw=1.4))
ax.annotate('', xy=(-0.72,0), xytext=(-0.44,0), arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.2, mutation_scale=9))
ax.annotate('', xy=(0.72,0), xytext=(0.44,0), arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.2, mutation_scale=9))
ax.text(0, 0.82, 'tensile', fontsize=8.6, ha='center', color=INK)
ax.text(0, -0.80, 'strain  ΔL/L', fontsize=8.0, ha='center', color=ACCENT)
# (b) shear
ax = axs[1]
ax.add_patch(plt.Rectangle((-0.36,-0.30), 0.72, 0.60, fc='none', ec=MUTED, ls='--', lw=1.0))
ax.add_patch(plt.Polygon([[-0.36,-0.30],[0.36,-0.30],[0.58,0.30],[-0.14,0.30]],
                         closed=True, fc=ACCENT, alpha=0.15, ec=ACCENT, lw=1.4))
ax.annotate('', xy=(0.56,0.46), xytext=(-0.16,0.46),
            arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.2, mutation_scale=9))
ax.text(0.20, 0.50, 'F', fontsize=8.0, ha='center', va='bottom', color=INK)
ax.add_patch(matplotlib.patches.Arc((-0.36,-0.30), 0.56, 0.56, angle=0,
                                    theta1=70, theta2=90, color=MUTED, lw=0.9))
ax.text(-0.25, 0.04, 'θ', fontsize=8.0, color=MUTED)
for xx in np.linspace(-0.36,0.36,7):
    ax.plot([xx,xx-0.06],[-0.30,-0.38], color=MUTED, lw=0.8)
ax.text(0.02, 0.82, 'shear', fontsize=8.6, ha='center', color=INK)
ax.text(0, -0.80, 'strain  θ', fontsize=8.0, ha='center', color=ACCENT)
# (c) volumetric
ax = axs[2]
ax.add_patch(plt.Circle((0,0), 0.46, fc='none', ec=MUTED, ls='--', lw=1.0))
ax.add_patch(plt.Circle((0,0), 0.34, fc=ACCENT, alpha=0.15, ec=ACCENT, lw=1.4))
for ang in [45, 135, 225, 315]:
    a = np.radians(ang)
    ax.annotate('', xy=(0.36*np.cos(a),0.36*np.sin(a)), xytext=(0.60*np.cos(a),0.60*np.sin(a)),
                arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.1, mutation_scale=8))
ax.text(0, 0.82, 'volumetric', fontsize=8.6, ha='center', color=INK)
ax.text(0, -0.80, 'strain  ΔV/V', fontsize=8.0, ha='center', color=ACCENT)
fig.subplots_adjust(wspace=0.05, bottom=0.02, top=0.98)
```

```figure caption="Poisson's ratio. The wire is stretched along its length (ΔL) and contracts across its diameter (Δd); σ = −(Δd/d)/(ΔL/L). The dashed outline is the original wire."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,2.6))
ax.axis('off'); ax.set_xlim(-0.9, 5.6); ax.set_ylim(-1.1, 1.7)
ax.add_patch(plt.Rectangle((0,0.00), 4.0, 1.30, fc='none', ec=MUTED, ls='--', lw=1.1))
ax.add_patch(plt.Rectangle((0,0.20), 4.5, 0.90, fc=ACCENT, alpha=0.13, ec=ACCENT, lw=1.5))
ax.annotate('', xy=(0,-0.30), xytext=(4.0,-0.30), arrowprops=dict(arrowstyle='<|-|>', color=MUTED, lw=0.9, mutation_scale=8))
ax.text(2.0, -0.55, 'original length  L', fontsize=8.2, ha='center', color=MUTED)
ax.annotate('', xy=(4.0,-0.30), xytext=(4.5,-0.30), arrowprops=dict(arrowstyle='<|-|>', color='#A8271F', lw=0.9, mutation_scale=7))
ax.text(4.72, -0.30, 'ΔL', fontsize=8.2, ha='left', va='center', color='#A8271F')
ax.annotate('', xy=(-0.30,0.00), xytext=(-0.30,1.30), arrowprops=dict(arrowstyle='<|-|>', color=MUTED, lw=0.9, mutation_scale=8))
ax.text(-0.45, 0.65, 'd', fontsize=8.2, ha='right', va='center', color=MUTED)
ax.plot([4.55,5.00],[1.30,1.30], color=MUTED, lw=0.7, ls=':')
ax.plot([4.55,5.00],[1.10,1.10], color=MUTED, lw=0.7, ls=':')
ax.annotate('', xy=(4.92,1.10), xytext=(4.92,1.30), arrowprops=dict(arrowstyle='<|-|>', color='#A8271F', lw=1.0, mutation_scale=7))
ax.text(5.04, 1.20, 'Δd', fontsize=8.2, ha='left', va='center', color='#A8271F')
ax.text(2.1, 1.60, 'stretched wire is longer and thinner', fontsize=8.2, ha='center', color=INK)
```

### Relations between the moduli

For an isotropic material (the same in all directions) the three moduli are not
independent:

$$ Y = 2G(1+\sigma), \qquad Y = 3K(1-2\sigma) $$

These let a question give two and ask for the third. They also explain the limits on
$\sigma$: if $\sigma$ were 0.5, $Y=3K(1-1)=0$ and the material would be infinitely
compressible; if $\sigma$ were $-1$, $Y=0$. Real materials sit safely inside.

| Modulus | Symbol | Formula | Resistance to | Applies to | Steel |
|---|---|---|---|---|---|
| Young's | $Y$ | $\frac{F/A}{\Delta L/L}$ | change of length | solids | $2.0\times10^{11}$ Pa |
| Bulk | $K$ | $-\frac{\Delta P}{\Delta V/V}$ | change of volume | solids, liquids, gases | $1.6\times10^{11}$ Pa |
| Rigidity | $G$ | $\frac{F/A}{\theta}$ | change of shape | solids only | $8.0\times10^{10}$ Pa |

::: example Worked example 7.2 — Young's modulus from a stretch
**Problem.** A steel wire 2.0 m long and of cross-section 1.0 mm² extends by 1.0 mm
under a load of 100 N. Find the stress, the strain and Young's modulus.

**Solution.** $A = 1.0\ \text{mm}^2 = 1.0\times10^{-6}$ m².

Stress $= F/A = 100/1.0\times10^{-6} = 1.0\times10^8$ Pa.

Strain $= \Delta L/L = 1.0\times10^{-3}/2.0 = 5.0\times10^{-4}$.

$Y = \text{stress}/\text{strain} = 1.0\times10^8/5.0\times10^{-4} = 2.0\times10^{11}$ Pa,
the standard value for steel.
:::

::: example Worked example 7.3 — the L/d² ratio
**Problem.** Two wires are made of the same material. Wire 2 is twice as long as wire
1 and has half its diameter. The same load is hung on each. Find the ratio
$\Delta L_2/\Delta L_1$.

**Solution.** $\Delta L = 4FL/(\pi d^2Y)$, and $F$, $Y$ and $\pi$ are the same, so

$$ \frac{\Delta L_2}{\Delta L_1} = \frac{L_2}{L_1}\left(\frac{d_1}{d_2}\right)^2 = 2\times2^2 = 8 $$

Wire 2 stretches eight times as much. The diameter matters twice over because the
area depends on $d^2$.
:::

::: example Worked example 7.4 — bulk modulus of water
**Problem.** A sphere of water of volume 1.0 litre is taken 100 m below the surface
of a lake. Taking $\rho = 1000$ kg m⁻³, $g = 9.8$ m s⁻² and
$K = 2.2\times10^9$ Pa, find the fractional change in its volume.

**Solution.** $\Delta P = \rho g h = (1000)(9.8)(100) = 9.8\times10^5$ Pa.

$$ \frac{\Delta V}{V} = \frac{\Delta P}{K} = \frac{9.8\times10^5}{2.2\times10^9} = 4.5\times10^{-4} $$

The volume falls by 0.045 %, about 0.45 cm³ in a litre. Water is hard to compress —
that is why the bulk modulus is large.
:::

::: example Worked example 7.5 — Poisson's ratio
**Problem.** A wire 1.5 m long and 2.0 mm in diameter stretches by 1.5 mm when
loaded. Its diameter decreases by $6.0\times10^{-4}$ mm. Find Poisson's ratio.

**Solution.** Longitudinal strain $= 1.5\times10^{-3}/1.5 = 1.0\times10^{-3}$.

Lateral strain $= 6.0\times10^{-4}/2.0 = 3.0\times10^{-4}$.

$$ \sigma = \frac{3.0\times10^{-4}}{1.0\times10^{-3}} = 0.30 $$

The value is typical of steel. Note that both strains are dimensionless, so the
ratio is a pure number.
:::

## 7.3 Elastic potential energy and energy density

### Work done in stretching

To stretch a spring or a wire, an external force must do work against the restoring
force. Because the force grows from zero to $F=kx$ as the extension grows, the work
is the **area under the force–extension graph** — a triangle:

$$ W = \int_0^{x} kx'\,dx' = \frac{1}{2}kx^2 $$

Using $F=kx$, this is also

$$ U = \frac{1}{2}Fx = \frac{1}{2}k x^2 $$

This energy is stored in the stretched body as **elastic potential energy** and is
returned when the force is removed (for a perfectly elastic body).

For a wire of length $L$, area $A$, Young's modulus $Y$, with extension $\Delta L$:

$$ k = \frac{YA}{L} \quad\Longrightarrow\quad U = \frac{1}{2}\frac{YA}{L}(\Delta L)^2 $$

```figure caption="Force against extension for a Hookean spring. The work done in stretching it — and so the energy stored — is the shaded area, ½Fx. For a non-Hookean material the energy is still the area under the curve."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,2.8))
x = np.linspace(0, 0.05, 100); F = 200*x
ax.fill_between(x*100, 0, F, color=ACCENT, alpha=0.16, lw=0)
ax.plot(x*100, F, color=ACCENT, lw=2.0)
ax.plot([5],[10],'o',color='#A8271F',ms=4.5,zorder=5)
ax.annotate('F = kx', xy=(3.4,6.8), xytext=(1.6,8.6), fontsize=8.5, color=ACCENT,
            arrowprops=dict(arrowstyle='-', color=ACCENT, lw=0.7))
ax.text(2.15, 3.35, 'area = ½Fx\n= energy stored', fontsize=8.3, color=INK, va='top')
ax.annotate('(5 cm, 10 N)', xy=(5,10), xytext=(2.4,10.4), fontsize=8.0, color=MUTED,
            ha='left', va='center', arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6))
ax.set_xlabel('extension  x  (cm)'); ax.set_ylabel('force  F  (N)')
ax.set_xlim(0,5.6); ax.set_ylim(0,11.6)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.4)
```

### Energy density

The **energy density** is the elastic energy stored per unit volume:

$$ u = \frac{U}{AL} = \frac{1}{2}\frac{F}{A}\cdot\frac{\Delta L}{L} = \frac{1}{2}\,\sigma\,\varepsilon $$

$$ u = \frac{1}{2}Y\varepsilon^2 = \frac{\sigma^2}{2Y} $$

Multiplying by the volume gives the total energy:
$U=uAL=\frac{1}{2}\sigma\varepsilon AL$. A wire twice as long stores twice the energy
at the same stress, because it has twice the volume.

The unit is J m⁻³, which is the same as Pa. This is the quantity a materials engineer
compares when choosing a spring material: a good spring stores a lot of energy per
kilogram without exceeding its elastic limit.

This is why a bow, a catapult and a vehicle suspension are built from materials with
a high elastic limit as well as a high modulus — they must store a large energy per
unit volume and still return it. Rubber stores more energy per unit mass than steel,
which is why a rubber catapult works at all, even though steel has the larger $Y$.

::: caution Half, not one
The energy is $\frac{1}{2}F\Delta L$, not $F\Delta L$. The force is **not** constant
while the wire stretches: it rises from 0 to $F$. Using the final force for the whole
distance overcounts by a factor of 2 — the most common wrong option in this topic.
:::

::: example Worked example 7.6 — energy in a stretched wire
**Problem.** For the wire of Worked example 7.2 (load 100 N, extension 1.0 mm,
length 2.0 m, area 1.0 mm²), find the energy stored and the energy density.

**Solution.** $U = \frac{1}{2}F\Delta L = \frac{1}{2}(100)(1.0\times10^{-3}) = 0.050$ J.

Volume $= AL = (1.0\times10^{-6})(2.0) = 2.0\times10^{-6}$ m³.

$$ u = \frac{0.050}{2.0\times10^{-6}} = 2.5\times10^4\ \text{J m}^{-3} $$

Check with $\frac{1}{2}\sigma\varepsilon$:
$\frac{1}{2}(1.0\times10^8)(5.0\times10^{-4}) = 2.5\times10^4$ J m⁻³ — the same,
as it must be.
:::

```photogrid label="7.1" cols="2" ratio="1.2" caption="Stress, strain and a safety factor. (a) Each hanger of a suspension bridge is a long steel rope that stretches a little under load. (b) For an assumed hanger 50 m long and 4.0 cm in diameter carrying 200 kN with Young modulus 2.0 x 10^11 Pa, the stress is F / A = 159 MPa, the strain is stress / Y = 0.80 x 10^-3 and the extension is 39.8 mm, so the rope stores 1/2 F dL = 3,979 J. Taking 250 MPa as yield and 400 MPa as breaking stress (typical mild steel, assumed), the margins are 1.57 to yield and 2.51 to breaking."
@ photo id="ceephy/bridge" cap="Cables of a suspension bridge are steel wires working in tension"
fit 1.2
focus 0.5 0.5
@ svg cap="Working stress against yield and breaking stress"
Y_ = 200e9; L = 50.0; d = 0.04; F = 200e3; A = math.pi * (d / 2) ** 2
sig = F / A; eps = sig / Y_; dL = eps * L; E = 0.5 * F * dL
yld, brk = 250e6, 400e6
assert abs(sig / 1e6 - 159.15) < 0.05 and abs(dL * 1000 - 39.79) < 0.05 and abs(E - 3979) < 2
facts = dict(sig="%.0f" % (sig / 1e6), eps="%.2f" % (eps * 1000), dL="%.1f" % (dL * 1000), E="{:,.0f}".format(E), ym="%.2f" % (yld / sig), sf="%.2f" % (brk / sig))
f = Fig(300, 236)
f.text(150, 14, "Stress in one hanger, MPa", size=10.5, color=NAVY, bold=True)
rows = (("working stress (F / A)", sig, TEAL, BLUE), ("yield stress (assumed)", yld, AMBER, SAND), ("breaking stress (assumed)", brk, RED, ROSE))
for i, (lab, v, col, fl) in enumerate(rows):
    y = 34 + i * 46
    f.text(14, y + 4, lab, size=10.5, color=SLATE, anchor="start")
    w = v / 1e6 * 0.4
    f.box(14, y + 12, w, 16, fill=fl, stroke=col, r=2, sw=1.6)
    f.text(14 + w + 5, y + 20, "%.0f" % (v / 1e6), size=10.5, color=col, bold=True, anchor="start", vmid=True)
f.text(150, 186, "strain = %.2f x 10^-3 (dimensionless)" % (eps * 1000), size=10.5, color=NAVY, bold=True)
f.text(150, 204, "extension %.1f mm; energy %.0f J" % (dL * 1000, E), size=10.5, color=NAVY, bold=True)
f.text(150, 222, "margin to yield %.2f, to break %.2f" % (yld / sig, brk / sig), size=10.5, color=NAVY, bold=True)
```

## Formula and fact sheet

| Topic | Formula or fact |
|---|---|
| Stress | $\sigma = F/A$; Pa = N m⁻²; $[ML^{-1}T^{-2}]$ |
| Strain | $\Delta L/L$, $\Delta V/V$, $\theta$; dimensionless |
| Hooke's law | stress $\propto$ strain up to the proportional limit; $F=kx$ |
| Young's modulus | $Y=\frac{FL}{A\Delta L}$; unit Pa; material property only |
| Extension | $\Delta L=\frac{4FL}{\pi d^2Y}$, so $\Delta L\propto L/d^2$ |
| Bulk modulus | $K=-\frac{\Delta P}{\Delta V/V}$; all states; compressibility $=1/K$ |
| Gas bulk modulus | isothermal $K=P$; adiabatic $K=\gamma P$ |
| Rigidity | $G=\frac{F/A}{\theta}$; solids only; zero for liquids and gases |
| Poisson's ratio | $\sigma=-\frac{\Delta d/d}{\Delta L/L}$; dimensionless; 0 to 0.5 |
| Moduli relations | $Y=2G(1+\sigma)$; $Y=3K(1-2\sigma)$ |
| Elastic energy | $U=\frac{1}{2}kx^2=\frac{1}{2}F\Delta L=\frac{YA(\Delta L)^2}{2L}$ |
| Energy density | $u=\frac{1}{2}\sigma\varepsilon=\frac{1}{2}Y\varepsilon^2=\frac{\sigma^2}{2Y}$; J m⁻³ |
| Stress–strain points | proportional limit, elastic limit, ultimate strength, breaking point |
| Typical values | steel $Y=2\times10^{11}$ Pa, $G=8\times10^{10}$ Pa, $K=1.6\times10^{11}$ Pa; water $K=2.2\times10^{9}$ Pa |

## Chapter summary

- Elasticity is the recovery of shape after a deforming force is removed; beyond the
  elastic limit the deformation is plastic and permanent.
- Stress is force per unit area inside the material (Pa); strain is a fractional
  change of length, volume or angle and has no unit.
- Hooke's law — stress proportional to strain — holds only up to the proportional
  limit; the constant is the modulus of elasticity.
- $Y=\frac{FL}{A\Delta L}$ applies to stretching and compressing solids. It depends on
  the material, not on the wire's dimensions; the extension itself obeys
  $\Delta L\propto L/d^2$.
- $K=-\frac{\Delta P}{\Delta V/V}$ applies to every state of matter; for a gas it is
  $P$ isothermally and $\gamma P$ adiabatically.
- $G=\frac{F/A}{\theta}$ applies to solids only; liquids and gases have no rigidity.
- Poisson's ratio $\sigma=-\frac{\Delta d/d}{\Delta L/L}$ is dimensionless, 0 for
  cork, about 0.3 for steel and 0.5 for rubber.
- The three moduli are linked: $Y=2G(1+\sigma)$ and $Y=3K(1-2\sigma)$.
- A stretched wire stores $\frac{1}{2}F\Delta L=\frac{1}{2}kx^2$; per unit volume the
  energy density is $\frac{1}{2}\sigma\varepsilon=\frac{\sigma^2}{2Y}$.

## Practice questions

**Set A — Recall (20 questions)**

1. The SI unit of stress is
   (a) N m (b) J m⁻² (c) N m⁻² (d) N m²
2. The strain produced when a force acts parallel to the surface of a body is called
   (a) shear strain (b) longitudinal strain (c) volumetric strain (d) tensile strain
3. Hooke's law is obeyed up to the
   (a) proportional limit (b) yield point (c) breaking point (d) ultimate strength
4. Young's modulus is defined as
   (a) stress × strain (b) strain ÷ stress (c) stress ÷ strain (d) force × extension
5. The dimensional formula of Young's modulus is
   (a) [MLT⁻²] (b) [ML²T⁻²] (c) dimensionless (d) [ML⁻¹T⁻²]
6. Which of the following has no modulus of rigidity?
   (a) steel (b) water (c) copper (d) glass
7. The bulk modulus is defined as
   (a) $\frac{\Delta V/V}{\Delta P}$ (b) $\Delta P\times\frac{\Delta V}{V}$ (c) $-\frac{\Delta P}{\Delta V/V}$ (d) $-\frac{\Delta V}{V\Delta P}$
8. Compressibility is the reciprocal of
   (a) Young's modulus (b) modulus of rigidity (c) Poisson's ratio (d) bulk modulus
9. Poisson's ratio is the ratio of
   (a) lateral strain to longitudinal strain (b) longitudinal strain to lateral strain (c) stress to strain (d) change in volume to original volume
10. Poisson's ratio is
   (a) measured in m (b) measured in Pa (c) dimensionless (d) measured in m²
11. The SI unit of energy density is
   (a) J (b) J m⁻³ (c) N m⁻¹ (d) Pa m²
12. The elastic potential energy stored in a stretched wire is
   (a) ½FΔL (b) FΔL (c) 2FΔL (d) F/ΔL
13. The slope of the linear part of a stress–strain graph gives
   (a) the elastic limit (b) the modulus of elasticity (c) the breaking stress (d) the strain energy
14. The ratio of shear stress to shear strain is called
   (a) Young's modulus (b) bulk modulus (c) modulus of rigidity (d) Poisson's ratio
15. A body that regains its original shape completely when the deforming force is removed is
   (a) plastic (b) brittle (c) ductile (d) perfectly elastic
16. For the same stress, a steel wire stretches less than a rubber band because steel has
   (a) a smaller Young's modulus (b) a larger Young's modulus (c) a larger Poisson's ratio (d) a smaller density
17. Young's modulus has the same dimensions as
   (a) force (b) energy (c) pressure (d) momentum
18. In F = kx for a spring, k is called the
   (a) stress (b) strain (c) modulus (d) force constant
19. Bulk modulus applies to
   (a) solids only (b) liquids only (c) gases only (d) solids, liquids and gases
20. The modulus of rigidity of a liquid is
   (a) zero (b) infinite (c) equal to its bulk modulus (d) equal to its Young's modulus

::: note Answers and explanations — Set A
**1.** (c) — stress is force per unit area, N m⁻² = Pa. N m is a torque, and J m⁻² equals N m⁻¹, which is surface tension, not stress.
**2.** (a) — a force along the surface produces shear, measured by the angle θ through which a face is displaced. Tensile and longitudinal strains come from forces perpendicular to the surface.
**3.** (a) — the straight part of the stress–strain graph ends at the proportional limit; the elastic limit is slightly beyond it.
**4.** (c) — $Y=\frac{\text{stress}}{\text{strain}}$. Multiplying them would give energy per volume.
**5.** (d) — stress and strain have the same dimensions as pressure: $[ML^{-1}T^{-2}]$.
**6.** (b) — a liquid cannot sustain a shear stress; it flows, so $G=0$. Glass is a solid and has rigidity.
**7.** (c) — the minus sign keeps $K$ positive when pressure rises and volume falls.
**8.** (d) — compressibility $=1/K$; a large bulk modulus means low compressibility.
**9.** (a) — lateral strain over longitudinal strain, with a minus sign in the definition to make it positive.
**10.** (c) — it is a ratio of two strains, so it is a pure number.
**11.** (b) — energy per unit volume, J m⁻³, which equals Pa.
**12.** (a) — the force rises linearly from zero, so the work is the area of a triangle, $\frac{1}{2}F\Delta L$.
**13.** (b) — slope $=\frac{\text{stress}}{\text{strain}}=Y$ (or the relevant modulus).
**14.** (c) — shear stress over shear strain is the modulus of rigidity, $G$.
**15.** (d) — that is the definition of perfect elasticity. A ductile body deforms permanently; a brittle one breaks.
**16.** (b) — the same stress gives strain $=\text{stress}/Y$; a larger $Y$ means a smaller strain. Steel is "more elastic" in this technical sense.
**17.** (c) — $Y$ is stress per unit strain, and strain is dimensionless, so $Y$ has the dimensions of stress, the same as pressure.
**18.** (d) — $k$ is the force constant or spring constant, in N m⁻¹.
**19.** (d) — every state of matter resists a change of volume, so $K$ is defined for solids, liquids and gases.
**20.** (a) — a liquid flows under shear, so it offers no elastic resistance to shape change: $G=0$.
:::

**Set B — Understanding (13 questions)**

1. A wire extends by 1 mm under a load of 50 N. Within the elastic limit, the extension under 150 N is
   (a) 1.5 mm (b) 3 mm (c) 6 mm (d) 9 mm
2. Two wires of the same material and length have radii r and 2r. Under the same load, the ratio of their extensions (thin : thick) is
   (a) 4 : 1 (b) 1 : 4 (c) 2 : 1 (d) 1 : 2
3. A wire of length L and diameter d is replaced by one of length 2L and diameter 2d, of the same material, under the same load. Its extension becomes
   (a) double (b) the same (c) half (d) one quarter
4. Young's modulus of a wire depends on
   (a) its length (b) its diameter (c) the applied load (d) the material only
5. Steel is said to be more elastic than rubber because
   (a) steel is stronger (b) steel returns to shape and rubber does not (c) for the same stress steel produces less strain (d) steel has a smaller Young's modulus
6. The area under a force–extension graph gives
   (a) energy stored (b) stress (c) strain (d) Young's modulus
7. A material that can be drawn into long wires without breaking is
   (a) brittle (b) ductile (c) perfectly elastic (d) an elastomer
8. Glass breaks with almost no plastic deformation, so it is
   (a) ductile (b) malleable (c) brittle (d) elastic
9. A wire stretched beyond its elastic limit
   (a) returns to its original length (b) breaks at once (c) becomes perfectly elastic (d) is permanently deformed
10. For a material whose volume does not change when it is stretched, Poisson's ratio is
   (a) 0.5 (b) 0 (c) 0.25 (d) 1
11. Cork has a Poisson's ratio close to zero, which is why it
   (a) is very strong (b) does not bulge sideways when compressed (c) is a good conductor (d) has a large Young's modulus
12. The bulk modulus of a gas in an adiabatic change is
   (a) P (b) γP (c) P/γ (d) zero
13. If the load on a wire is doubled, within the elastic limit, the energy stored becomes
   (a) double (b) half (c) four times (d) unchanged

::: note Answers and explanations — Set B
**1.** (b) — Hooke's law gives extension proportional to load: $3\times1 = 3$ mm.
**2.** (a) — $\Delta L\propto1/r^2$, so the thin wire extends $(2r/r)^2 = 4$ times as much.
**3.** (c) — $\Delta L\propto L/d^2$: the length doubles but $d^2$ becomes four times, so the net factor is $2/4 = 1/2$.
**4.** (d) — $Y$ is a material constant (temperature aside). Length, diameter and load change the extension, not the modulus.
**5.** (c) — elasticity here means a small strain for a given stress, which is exactly a large $Y$. Strength (breaking stress) is a different property.
**6.** (a) — work $=\int F\,dx$ is the area; that work is stored as elastic energy.
**7.** (b) — ductility is the ability to undergo large plastic deformation in tension.
**8.** (c) — brittleness is fracture with little or no plastic flow.
**9.** (d) — the deformation is no longer recoverable, so a permanent set remains.
**10.** (a) — zero volume change means the lateral contraction exactly compensates the stretching, which occurs at $\sigma=0.5$.
**11.** (b) — a near-zero Poisson's ratio means almost no lateral expansion, so a cork stays the same width when pushed into the neck.
**12.** (b) — $K=\gamma P$ adiabatically and $K=P$ isothermally. Sound uses the adiabatic value.
**13.** (c) — $U=\frac{1}{2}kx^2$ and $x\propto F$, so doubling $F$ quadruples $U$.
:::

**Set C — Application (10 questions)**

1. A steel wire 2.0 m long and of cross-section 1.0 mm² extends by 1.0 mm under a load of 100 N. Young's modulus of the steel is
   (a) 2 × 10¹⁰ Pa (b) 2 × 10¹¹ Pa (c) 2 × 10⁹ Pa (d) 5 × 10¹⁰ Pa
2. The elastic energy stored in that wire is
   (a) 0.05 J (b) 0.10 J (c) 0.50 J (d) 5.0 J
3. Two wires of the same material have the same length but diameters d and d/2. Under the same load, the ratio of their extensions (thin : thick) is
   (a) 2 (b) 4 (c) 8 (d) 16
4. A wire of length L and radius r extends by x under a load F. Another wire of the same material, length 2L and radius 2r, under the same load extends by
   (a) x/4 (b) x (c) 2x (d) x/2
5. A sphere of water of volume 1 litre is taken 100 m deep in a lake (ρ = 1000 kg m⁻³, g = 9.8 m s⁻², K = 2.2 × 10⁹ Pa). The fractional change in volume is
   (a) 4.5 × 10⁻⁶ (b) 2.2 × 10⁻⁴ (c) 4.5 × 10⁻² (d) 4.5 × 10⁻⁴
6. A wire has a stress of 1.0 × 10⁸ Pa and a strain of 5.0 × 10⁻⁴. The energy density is
   (a) 2.5 × 10⁴ J m⁻³ (b) 5.0 × 10⁴ J m⁻³ (c) 2.5 × 10⁵ J m⁻³ (d) 1.0 × 10⁴ J m⁻³
7. A wire 1.5 m long and 2.0 mm in diameter stretches by 1.5 mm, while its diameter shrinks by 6.0 × 10⁻⁴ mm. Poisson's ratio is
   (a) 0.15 (b) 0.30 (c) 0.60 (d) 3.0
8. A steel rod 1.0 m long and of cross-section 1.0 cm² is compressed by 0.01 mm (Y = 2 × 10¹¹ Pa). The force required is
   (a) 20 N (b) 2000 N (c) 200 N (d) 2 × 10⁵ N
9. A spring of force constant 200 N m⁻¹ is stretched by 5.0 cm. The energy stored is
   (a) 0.025 J (b) 2.5 J (c) 0.25 J (d) 5.0 J
10. A wire breaks under a stress of 1.0 × 10⁹ Pa. The greatest load it can carry if its cross-section is 0.50 mm² is
   (a) 500 N (b) 50 N (c) 1000 N (d) 5 N

::: note Answers and explanations — Set C
**1.** (b) — $Y=\frac{FL}{A\Delta L} = \frac{(100)(2.0)}{(1.0\times10^{-6})(1.0\times10^{-3})} = 2\times10^{11}$ Pa.
**2.** (a) — $U=\frac{1}{2}F\Delta L = \frac{1}{2}(100)(1.0\times10^{-3}) = 0.05$ J. Option (b) forgets the ½.
**3.** (b) — the thin wire has area $\pi(d/2)^2 = A/4$, so for the same load its extension is 4 times larger: thin : thick $= 4:1$.
**4.** (d) — $\Delta L\propto L/r^2$; doubling both multiplies by $2/4 = 1/2$.
**5.** (d) — $\Delta P=\rho gh = 9.8\times10^5$ Pa; $\Delta V/V = \Delta P/K = 9.8\times10^5/2.2\times10^9 = 4.5\times10^{-4}$.
**6.** (a) — $u=\frac{1}{2}\sigma\varepsilon = \frac{1}{2}(1.0\times10^8)(5.0\times10^{-4}) = 2.5\times10^4$ J m⁻³.
**7.** (b) — lateral strain $=6.0\times10^{-4}/2.0 = 3.0\times10^{-4}$; longitudinal $=1.5\times10^{-3}/1.5 = 1.0\times10^{-3}$; $\sigma=0.30$.
**8.** (c) — $F=\frac{YA\Delta L}{L} = \frac{(2\times10^{11})(1.0\times10^{-4})(1.0\times10^{-5})}{1.0} = 200$ N.
**9.** (c) — $U=\frac{1}{2}kx^2 = \frac{1}{2}(200)(0.05)^2 = 0.25$ J. Option (d) 5.0 J comes from using $\frac{1}{2}kx$ and never squaring the extension.
**10.** (a) — $F=\text{stress}\times A = (1.0\times10^9)(0.50\times10^{-6}) = 500$ N.
:::
