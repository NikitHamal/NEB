---
subject: Physics
grade: 12
unit: 17
title: Magnetic properties of materials
hours: 5
area: Electricity and Magnetism
---

Unit 16 treated magnetic fields in empty space. Real coils, however, are wound on
iron, and the iron changes everything: the same current produces a field a
thousand times stronger, and the material remembers what you did to it. This unit
introduces the two field vectors $\vec{B}$ and $\vec{H}$, the numbers that link
them (permeability and susceptibility), the loop that describes magnetic memory
(hysteresis), and the three-way classification of all matter as diamagnetic,
paramagnetic or ferromagnetic.

::: key What the examiner wants here
Three items dominate: the derivation $\mu_r = 1 + \chi_m$, a labelled hysteresis
loop with retentivity and coercivity defined, and the soft-iron-versus-steel
comparison table. Numericals are almost always "find $H$, then $B$, then $M$" for
a solenoid or ring with a core. Keep $B$ (tesla) and $H$ (ampere per metre)
strictly apart — mixing their units is the single commonest error in this unit.
:::

## 17.1 Magnetic field lines and magnetic flux

A **magnetic field line** is a curve whose tangent at every point gives the
direction of the magnetic flux density $\vec{B}$ at that point. Because there are
no magnetic monopoles, every field line closes on itself: outside a magnet it
runs N to S, inside the magnet it continues S to N.

::: definition Magnetic flux
The magnetic flux through a surface of area $A$ in a uniform field is

$$ \Phi = \vec{B}\cdot\vec{A} = BA\cos\theta $$

where $\theta$ is the angle between $\vec{B}$ and the normal to the surface. Flux
is a **scalar**; its SI unit is the **weber** (Wb), and $1\ \text{Wb} = 1\ \text{T m}^{2}$.
:::

Rearranged, $B = \Phi/A$ for a surface held perpendicular to the field, which is
why $B$ is called the **magnetic flux density** — flux per unit area. Since every
line entering a closed surface must leave it,

$$ \oint \vec{B}\cdot d\vec{A} = 0 $$

This is **Gauss's law for magnetism**, and it holds inside matter as well as in
vacuum. Its practical consequence is that flux is *continuous*: if a magnetic
circuit narrows, the flux stays the same and $B$ rises.

Magnetic materials are studied with a **toroidal ring** (a Rowland ring) because
in a toroid the flux is trapped entirely inside the core, with no leakage and no
end effects. The whole of the winding's magnetising action is then felt by the
specimen.

```figure caption="Rowland ring: $N$ turns wound on a toroidal specimen of mean radius $r$. The flux $\Phi$ is confined to the core, and the magnetising field is $H = NI/2\pi r$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.4,3.2))
th = np.linspace(0, 2*np.pi, 500)
r1, r2 = 1.00, 1.42
ax.fill(np.concatenate([r2*np.cos(th), r1*np.cos(th[::-1])]),
        np.concatenate([r2*np.sin(th), r1*np.sin(th[::-1])]),
        color=ACCENT, alpha=0.13, lw=0)
ax.plot(r1*np.cos(th), r1*np.sin(th), color=INK, lw=1.2)
ax.plot(r2*np.cos(th), r2*np.sin(th), color=INK, lw=1.2)
for a in np.arange(0, 2*np.pi, np.pi/15):
    ca, sa = np.cos(a), np.sin(a)
    ax.plot([(r1-0.13)*ca, (r2+0.13)*ca], [(r1-0.13)*sa, (r2+0.13)*sa],
            color='#b8860b', lw=1.1, solid_capstyle='round')
rm = 0.5*(r1+r2)
ax.plot(rm*np.cos(th), rm*np.sin(th), color='#d9534f', lw=1.0, ls=(0,(4,3)))
for a in [0.6, 2.2, 3.9, 5.5]:
    ax.annotate('', xy=(rm*np.cos(a+0.14), rm*np.sin(a+0.14)),
                xytext=(rm*np.cos(a), rm*np.sin(a)),
                arrowprops=dict(arrowstyle='-|>', color='#d9534f', lw=1.5,
                                mutation_scale=12))
ax.annotate('flux Φ confined\nto the core', xy=(rm*np.cos(1.15), rm*np.sin(1.15)),
            textcoords='offset points', xytext=(26,20), color='#d9534f', fontsize=8.6,
            arrowprops=dict(arrowstyle='-', color='#d9534f', lw=0.8))
ax.annotate('N turns of wire', xy=(-(r2+0.10)*0.72, (r2+0.10)*0.72),
            textcoords='offset points', xytext=(-34,20), color='#b8860b', fontsize=8.6,
            ha='center', arrowprops=dict(arrowstyle='-', color='#b8860b', lw=0.8))
ax.annotate('', xy=(rm*np.cos(-1.35), rm*np.sin(-1.35)), xytext=(0,0),
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.1, mutation_scale=11))
ax.annotate('mean radius  r', (0.0, 0.34), ha='center', color=MUTED, fontsize=8.6)
ax.annotate('current  I', xy=(-(r2+0.13)*0.80, -(r2+0.13)*0.60),
            textcoords='offset points', xytext=(-40,-14), color=INK, fontsize=8.6,
            ha='center', arrowprops=dict(arrowstyle='-', color=INK, lw=0.8))
ax.set_xlim(-2.6, 2.6); ax.set_ylim(-2.05, 2.15)
ax.set_aspect('equal'); ax.axis('off')
```
::: example Worked example 17.1
**Problem.** A closed iron ring of cross-sectional area $4\ \text{cm}^{2}$ and
mean circumference $0.50\ \text{m}$ carries a flux of $6\times10^{-4}\ \text{Wb}$.
The relative permeability of the iron is $1200$. Find (a) the flux density in the
core and (b) the ampere-turns needed on the winding.

**Solution.**

(a) $A = 4\times10^{-4}\ \text{m}^{2}$, so

$$ B = \frac{\Phi}{A} = \frac{6\times10^{-4}}{4\times10^{-4}} = 1.5\ \text{T} $$

(b) Inside the core $B = \mu_0\mu_r H$, hence

$$ H = \frac{B}{\mu_0\mu_r} = \frac{1.5}{(4\pi\times10^{-7})(1200)} = \frac{1.5}{1.508\times10^{-3}} = 995\ \text{A m}^{-1} $$

For a ring, $H = NI/l$ with $l = 0.50\ \text{m}$, so

$$ NI = Hl = 995 \times 0.50 \approx 5.0\times10^{2}\ \text{ampere-turns} $$
:::

## 17.2 Flux density in magnetic material; Relative permeability; Susceptibility

When a specimen is placed inside a current-carrying solenoid, two separate causes
produce the field inside it:

1. the **free current** in the winding, described by the **magnetising field**
   $\vec{H}$, and
2. the **atomic currents** inside the specimen itself, described by the
   **intensity of magnetisation** $\vec{M}$.

::: definition Magnetising field and magnetisation
The **magnetising field** $H$ of a long solenoid or ring is the ampere-turns per
metre of its winding, $H = nI = NI/l$. The **intensity of magnetisation** $M$ is
the net magnetic dipole moment per unit volume of the specimen, $M = m/V$. Both
are measured in **ampere per metre (A m⁻¹)**, and both are independent of the
material's response.
:::

The resultant flux density inside the specimen is the sum of the two
contributions:

$$ B = \mu_0\left(H + M\right) $$

::: derivation The relation $\mu_r = 1 + \chi_m$
For a material that responds linearly, the magnetisation produced is proportional
to the magnetising field. The constant of proportionality is the **magnetic
susceptibility**:

$$ \chi_m = \frac{M}{H} $$

Since $M$ and $H$ have the same unit, $\chi_m$ is a **pure number**. Substituting
$M = \chi_m H$,

$$ B = \mu_0(H + \chi_m H) = \mu_0(1+\chi_m)H $$

The **absolute permeability** of the medium is defined by $\mu = B/H$, and the
**relative permeability** by $\mu_r = \mu/\mu_0$. Comparing,

$$ \mu = \mu_0(1+\chi_m) \;\Longrightarrow\; \boxed{\mu_r = 1 + \chi_m} $$
:::

| Quantity | Symbol | Defining relation | SI unit |
|---|---|---|---|
| Magnetic flux | $\Phi$ | $BA\cos\theta$ | weber (Wb) |
| Flux density | $B$ | $\Phi/A$ | tesla (T) |
| Magnetising field | $H$ | $NI/l$ | A m⁻¹ |
| Magnetisation | $M$ | $m/V$ | A m⁻¹ |
| Susceptibility | $\chi_m$ | $M/H$ | none |
| Permeability | $\mu$ | $B/H$ | T m A⁻¹ (= H m⁻¹) |
| Relative permeability | $\mu_r$ | $\mu/\mu_0$ | none |

Here $\mu_0 = 4\pi\times10^{-7}\ \text{T m A}^{-1}$ is the permeability of free
space; for vacuum $\chi_m = 0$ and $\mu_r = 1$ exactly.

::: caution $B$ and $H$ are not the same thing
$H$ is fixed by the current you pass through the winding; $B$ is what the material
gives you back. Changing the core changes $B$ but not $H$. Writing "$H = 1.5\ \text{T}$"
or "$B = 2000\ \text{A m}^{-1}$" costs marks even if the arithmetic is right.
:::

::: example Worked example 17.2
**Problem.** A solenoid $50\ \text{cm}$ long has $500$ turns and carries
$2.0\ \text{A}$. An iron rod fills the solenoid, and the flux density measured
inside is $1.6\ \text{T}$. Calculate $H$, $\mu$, $\mu_r$, $M$ and $\chi_m$.

**Solution.** Turns per metre: $n = 500/0.50 = 1000\ \text{m}^{-1}$.

$$ H = nI = 1000 \times 2.0 = 2.0\times10^{3}\ \text{A m}^{-1} $$
$$ \mu = \frac{B}{H} = \frac{1.6}{2.0\times10^{3}} = 8.0\times10^{-4}\ \text{T m A}^{-1} $$
$$ \mu_r = \frac{\mu}{\mu_0} = \frac{8.0\times10^{-4}}{4\pi\times10^{-7}} = 637 $$

From $B = \mu_0(H+M)$,

$$ M = \frac{B}{\mu_0} - H = \frac{1.6}{1.257\times10^{-6}} - 2000 = 1.273\times10^{6} - 2\times10^{3} = 1.27\times10^{6}\ \text{A m}^{-1} $$

$$ \chi_m = \frac{M}{H} = \frac{1.27\times10^{6}}{2.0\times10^{3}} = 636 $$

As a check, $\mu_r = 1 + \chi_m = 637$, which agrees.
:::

## 17.3 Hysteresis

Take an unmagnetised ferromagnetic ring and raise $H$ from zero. $B$ climbs along
the **initial magnetisation curve** $Oa$ and then flattens: all the domains are
aligned and the specimen has reached **saturation**. Now reduce $H$ back to zero.
$B$ does *not* retrace the curve — it falls along $ab$ and stops at a non-zero
value $B_r$. The specimen has become a magnet on its own.

::: definition Hysteresis, retentivity and coercivity
**Hysteresis** is the lagging of the flux density $B$ behind the magnetising
field $H$ when a ferromagnetic specimen is taken through a cycle of
magnetisation.

**Retentivity** (remanence) $B_r$ is the flux density that remains in the
specimen when the magnetising field is reduced to zero.

**Coercivity** $H_c$ is the reverse magnetising field needed to reduce the
retained flux density to zero.
:::

Continuing to reverse $H$ drives the specimen to saturation the other way, and
bringing $H$ forward again closes the curve. The closed figure $abcdefa$ is the
**hysteresis loop**.

```figure caption="A complete hysteresis loop. $Oa$ is the initial magnetisation curve, $Ob = B_r$ is the retentivity and $Oc = H_c$ the coercivity."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6,3.3))
Bs, Hc, a, Hm = 1.5, 1.0, 1.2, 4.0
H = np.linspace(-Hm, Hm, 400)
up   = Bs*np.tanh((H - Hc)/a)
down = Bs*np.tanh((H + Hc)/a)
Hi = np.linspace(0, Hm, 200)
ax.plot(Hi, Bs*np.tanh(Hi/a), color=MUTED, lw=1.4, ls=(0,(4,2)))
ax.plot(H, down, color=ACCENT, lw=1.9)
ax.plot(H, up,   color=ACCENT, lw=1.9)
Br = Bs*np.tanh(Hc/a)
ax.axhline(0, color=INK, lw=0.9); ax.axvline(0, color=INK, lw=0.9)
ax.plot([0,-Hc,0,Hc],[Br,0,-Br,0],'o',color='#d9534f',ms=4.5,zorder=5)
ax.annotate('a  (saturation)', (Hm, Bs*np.tanh((Hm+Hc)/a)),
            textcoords='offset points', xytext=(-74,8), color=INK, fontsize=9)
ax.annotate('b', (0,Br), textcoords='offset points', xytext=(7,3), color='#d9534f', fontsize=9.5)
ax.annotate('$B_r$', (0,Br), textcoords='offset points', xytext=(-26,-5), color='#d9534f', fontsize=9.5)
ax.annotate('c', (-Hc,0), textcoords='offset points', xytext=(-3,9), color='#d9534f', fontsize=9.5)
ax.annotate('$H_c$', (-Hc,0), textcoords='offset points', xytext=(-32,-16), color='#d9534f', fontsize=9.5)
ax.annotate('d', (-Hm, -Bs*np.tanh((Hm+Hc)/a)), textcoords='offset points',
            xytext=(10,6), color=INK, fontsize=9.5)
ax.annotate('e', (0,-Br), textcoords='offset points', xytext=(-14,-5), color='#d9534f', fontsize=9.5)
ax.annotate('f', (Hc,0), textcoords='offset points', xytext=(3,-15), color='#d9534f', fontsize=9.5)
ax.annotate('initial curve', (1.15, Bs*np.tanh(1.15/a)), textcoords='offset points',
            xytext=(12,-20), color=MUTED, fontsize=9,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.8))
ax.annotate('', xy=(-0.9, Bs*np.tanh((-0.9+Hc)/a)), xytext=(-0.4, Bs*np.tanh((-0.4+Hc)/a)),
            arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.4, mutation_scale=12))
ax.annotate('', xy=(0.9, Bs*np.tanh((0.9-Hc)/a)), xytext=(0.4, Bs*np.tanh((0.4-Hc)/a)),
            arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.4, mutation_scale=12))
ax.set_xlabel('magnetising field  $H$  (A m$^{-1}$)')
ax.set_ylabel('flux density  $B$  (T)')
ax.set_xlim(-5.0,5.0); ax.set_ylim(-2.1,2.1)
ax.set_xticks([]); ax.set_yticks([])
ax.spines[['top','right','bottom','left']].set_visible(False)
```
### Energy lost per cycle

::: derivation The loop area is the energy dissipated per unit volume per cycle
Take a ring of mean length $l$, cross-section $A$ and $N$ turns. When the flux
changes, a back e.m.f. $e = N\,d\Phi/dt$ opposes the source, so in time $dt$ the
source does work

$$ dW = eI\,dt = NI\,d\Phi = NI\,A\,dB $$

But $H = NI/l$, so $NI = Hl$ and

$$ dW = H\,l\,A\,dB = (Al)\,H\,dB $$

Since $Al$ is the volume $V$ of the specimen, the work done per unit volume in
one complete cycle is

$$ \frac{W}{V} = \oint H\,dB = \text{area enclosed by the } B\text{–}H \text{ loop} $$

The unit of this area is $(\text{A m}^{-1})(\text{T}) = \text{J m}^{-3}$. Because
the loop is traversed once per cycle and the work is not recovered, it appears as
heat. For a core of volume $V$ driven at frequency $f$,

$$ P_{\text{hyst}} = (\text{loop area}) \times V \times f $$
:::

### Soft and hard magnetic materials

```figure caption="Loops for a soft magnetic material (narrow, small area) and a hard one (broad, large $B_r$ and $H_c$). Loop area is the energy wasted as heat per cubic metre per cycle."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,3.0))
H = np.linspace(-4, 4, 500)
def loop(Bs, Hc, a):
    return Bs*np.tanh((H+Hc)/a), Bs*np.tanh((H-Hc)/a)
d1,u1 = loop(1.55, 0.25, 0.30)
d2,u2 = loop(1.05, 2.10, 0.95)
ax.fill(np.concatenate([H, H[::-1]]), np.concatenate([d1, u1[::-1]]),
        color=ACCENT, alpha=0.20, lw=0)
ax.plot(H, d1, color=ACCENT, lw=1.9, label='soft: silicon steel, low $H_c$')
ax.plot(H, u1, color=ACCENT, lw=1.9)
ax.plot(H, d2, color='#d9534f', lw=1.9, label='hard: carbon steel, high $H_c$')
ax.plot(H, u2, color='#d9534f', lw=1.9)
ax.axhline(0, color=INK, lw=0.9); ax.axvline(0, color=INK, lw=0.9)
ax.plot([-0.25, -2.10], [0,0], ' ')
ax.annotate('', xy=(-2.10,0.06), xytext=(0,0.06),
            arrowprops=dict(arrowstyle='<->', color='#d9534f', lw=1.0, mutation_scale=9))
ax.annotate('$H_c$ (hard)', (-1.05,0.06), textcoords='offset points', xytext=(0,10),
            color='#d9534f', fontsize=8.4, ha='center')
ax.set_xlabel('$H$  (A m$^{-1}$)'); ax.set_ylabel('$B$  (T)')
ax.set_xlim(-4.6,4.6); ax.set_ylim(-2.0,2.95)
ax.set_xticks([]); ax.set_yticks([])
ax.spines[['top','right','bottom','left']].set_visible(False)
ax.legend(loc='upper left', fontsize=8.2)
```
| Property | Soft magnetic material | Hard magnetic material |
|---|---|---|
| Loop shape | narrow, tall, small area | broad, large area |
| Retentivity $B_r$ | high | high |
| Coercivity $H_c$ | **very low** | **very high** |
| Susceptibility, $\mu_r$ | very large | moderate |
| Energy loss per cycle | small | large |
| Magnetisation | easily magnetised and demagnetised | hard to demagnetise |
| Examples | soft iron, silicon steel, mu-metal, ferrites | carbon steel, cobalt steel, alnico, ferrite magnets |
| Used for | transformer and motor cores, electromagnets, relays | permanent magnets, loudspeakers, compass needles, magnetic latches |

::: tip Choosing a core in one line
Anything that is magnetised and demagnetised many times a second wants a **small
loop area**, so use a soft material. Anything that must *stay* magnetised wants a
**large coercivity**, so use a hard material.
:::

::: example Worked example 17.3
**Problem.** The hysteresis loop of a transformer core material encloses an area
equivalent to $250\ \text{J m}^{-3}$ per cycle. The core has volume
$1200\ \text{cm}^{3}$ and the transformer runs at $50\ \text{Hz}$. Find the
energy lost per cycle and the hysteresis power loss.

**Solution.** $V = 1200\ \text{cm}^{3} = 1200\times10^{-6} = 1.2\times10^{-3}\ \text{m}^{3}$.

Energy per cycle:

$$ W = 250 \times 1.2\times10^{-3} = 0.30\ \text{J} $$

Power lost (50 cycles each second):

$$ P = Wf = 0.30 \times 50 = 15\ \text{W} $$

Low-loss silicon steel is used precisely to keep this figure small.
:::

## 17.4 Dia-, para- and ferro-magnetic materials

Every electron in an atom is both orbiting and spinning, and each motion is a
tiny current loop with a magnetic moment. How those moments add up decides the
class of the material.

**Diamagnetic materials.** The atomic moments cancel exactly, so the atom has
**no permanent** magnetic moment. An applied field changes the electron orbits
slightly (Lenz's law at atomic scale) and induces a moment *opposing* the field.
Hence $M$ is antiparallel to $H$, $\chi_m$ is small and **negative**
(about $-10^{-5}$), and $\mu_r$ is slightly less than 1. Field lines are pushed
out of the specimen, and a rod suspended in a non-uniform field moves from strong
to weak field and sets **perpendicular** to it. Examples: bismuth, copper, water,
gold, mercury, nitrogen, sodium chloride. Superconductors are perfect diamagnets
with $\chi_m = -1$.

**Paramagnetic materials.** The atoms *do* have permanent moments, but thermal
agitation keeps them randomly oriented. An applied field aligns them slightly, so
$M$ is parallel to $H$ with $\chi_m$ small and **positive** (about $10^{-5}$ to
$10^{-3}$) and $\mu_r$ slightly greater than 1. A rod moves from weak to strong
field and sets **parallel** to it. Alignment is destroyed by heat, so
susceptibility obeys **Curie's law**:

$$ \chi_m = \frac{C}{T} $$

where $C$ is the Curie constant. Examples: aluminium, platinum, manganese,
chromium, oxygen, copper sulphate solution.

**Ferromagnetic materials.** Neighbouring atomic moments lock parallel to each
other over regions called **domains**, each containing about $10^{17}$–$10^{21}$
atoms. In an unmagnetised sample the domains point in random directions and
cancel. A field makes favourably oriented domains **grow** at the expense of the
others and finally rotates them all into line — which is why $M$ saturates.
$\chi_m$ is large and positive (10² to 10⁵), $\mu_r$ runs into thousands, field
lines crowd strongly into the specimen, and the material shows hysteresis.
Examples: iron, cobalt, nickel, gadolinium and alloys such as alnico.

Above a critical temperature, the **Curie temperature** $T_C$, thermal energy
destroys the domain alignment and a ferromagnet becomes an ordinary paramagnet
obeying the **Curie–Weiss law**:

$$ \chi_m = \frac{C}{T - T_C} \qquad (T > T_C) $$

For iron $T_C = 1043\ \text{K}$ ($770\ ^{\circ}\text{C}$), for cobalt
$1394\ \text{K}$ and for nickel $631\ \text{K}$.

```figure caption="Field lines near a specimen. They are expelled by a diamagnetic, drawn in slightly by a paramagnetic and concentrated strongly by a ferromagnetic material."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
fig, axes = plt.subplots(1, 3, figsize=(5.1,2.4))
cfg = [('Diamagnetic\n$\\chi<0,\\ \\mu_r<1$',  0.21, 1),
       ('Paramagnetic\n$\\chi>0$ small, $\\mu_r>1$', -0.08, 3),
       ('Ferromagnetic\n$\\chi$ huge, $\\mu_r$ huge', -0.22, 8)]
x = np.linspace(-1.9, 1.9, 300)
for ax, (lab, k, nin) in zip(axes, cfg):
    for y0 in [0.62, 0.92, 1.24, -0.62, -0.92, -1.24]:
        s = np.sign(y0)
        y = y0 + s*k*np.exp(-(x/0.85)**2)
        ax.plot(x, y, color=MUTED, lw=0.85)
    ax.annotate('', xy=(1.88, 1.24), xytext=(1.30, 1.24),
                arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=0.9, mutation_scale=9))
    ax.add_patch(Ellipse((0,0), 1.7, 0.98, facecolor=ACCENT, alpha=0.16,
                         edgecolor=INK, lw=1.1))
    ys = [0.0] if nin == 1 else np.linspace(-0.34, 0.34, nin)
    for yy in ys:
        w = 0.82*np.sqrt(max(1 - (yy/0.49)**2, 0.02))
        ax.plot([-w, w], [yy, yy], color='#d9534f', lw=1.0)
    ax.set_title(lab, fontsize=8.0, color=INK, pad=5)
    ax.set_xlim(-2.0, 2.0); ax.set_ylim(-1.6, 1.6)
    ax.set_aspect('equal'); ax.axis('off')
fig.subplots_adjust(wspace=0.05)
```
| Property | Diamagnetic | Paramagnetic | Ferromagnetic |
|---|---|---|---|
| Atomic moment | zero | permanent, random | permanent, aligned in domains |
| $\chi_m$ | small, negative ($\approx -10^{-5}$) | small, positive ($10^{-5}$–$10^{-3}$) | large, positive ($10^{2}$–$10^{5}$) |
| $\mu_r$ | slightly $< 1$ | slightly $> 1$ | $\gg 1$ (10²–10⁵) |
| $M$ vs $H$ | linear, negative slope | linear, small positive slope | non-linear, saturates |
| Field lines | expelled | slightly concentrated | strongly concentrated |
| In non-uniform field | moves to weaker field | moves to stronger field | moves strongly to stronger field |
| Effect of temperature | almost none | $\chi_m = C/T$ | ferromagnetic below $T_C$, paramagnetic above |
| Hysteresis | no | no | yes |
| Examples | Bi, Cu, Au, H₂O, N₂ | Al, Pt, Mn, O₂, CuSO₄ | Fe, Co, Ni, Gd, alnico |

```figure caption="Plotting $1/\chi_m$ against temperature straightens both laws: a paramagnet gives a line through the origin, a ferromagnet above $T_C$ a line cutting the axis at $T_C$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6,2.8))
T = np.linspace(0, 1500, 300)
ax.plot(T, T/380.0, color=ACCENT, lw=1.9, label=r'paramagnet:  $1/\chi = T/C$')
Tc = 620.0
Tf = np.linspace(Tc, 1500, 200)
ax.plot(Tf, (Tf-Tc)/380.0, color='#d9534f', lw=1.9,
        label=r'ferromagnet:  $1/\chi = (T-T_C)/C$')
ax.plot([Tc],[0],'o',color='#d9534f',ms=5)
ax.annotate('$T_C$', (Tc,0), textcoords='offset points', xytext=(6,7),
            color='#d9534f', fontsize=9.5)
ax.axvspan(0, Tc, color='#d9534f', alpha=0.07, lw=0)
ax.annotate('ferromagnetic\n(domains ordered)', (Tc*0.5, 3.1), ha='center',
            color=MUTED, fontsize=8.2)
ax.set_xlabel('temperature  $T$  (K)'); ax.set_ylabel(r'$1/\chi_m$')
ax.set_xlim(0,1500); ax.set_ylim(0,5.4)
ax.set_yticks([])
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=0.5)
ax.legend(loc='upper left', fontsize=8.2)
```
::: example Worked example 17.4
**Problem.** A paramagnetic salt has susceptibility $2.4\times10^{-4}$ at
$300\ \text{K}$. (a) Find its susceptibility at $200\ \text{K}$. (b) At
$200\ \text{K}$ the salt is placed in a magnetising field of
$1.6\times10^{4}\ \text{A m}^{-1}$. Find its magnetisation and the flux density
inside it.

**Solution.**

(a) Curie's law gives $\chi_m T = C$, a constant, so $\chi_1T_1 = \chi_2T_2$:

$$ \chi_2 = \chi_1\frac{T_1}{T_2} = 2.4\times10^{-4}\times\frac{300}{200} = 3.6\times10^{-4} $$

(b) $M = \chi_m H = 3.6\times10^{-4}\times 1.6\times10^{4} = 5.76\ \text{A m}^{-1}$.

$$ B = \mu_0(H+M) = 4\pi\times10^{-7}\,(1.6\times10^{4} + 5.76) = 1.257\times10^{-6}\times 16006 $$
$$ B = 2.01\times10^{-2}\ \text{T} $$

The magnetisation contributes only $0.04\%$ of the total — a paramagnet barely
changes the field, unlike the iron of Worked example 17.2.
:::

::: caution "Higher permeability means stronger magnet"
No. Permeability measures how easily a material *carries* flux when a field is
applied. Soft iron has an enormous $\mu_r$ but makes a hopeless permanent magnet,
because its coercivity is tiny and it loses its magnetism as soon as the current
is switched off.
:::

## Chapter summary

- Magnetic flux $\Phi = BA\cos\theta$ (weber); $B = \Phi/A$ is the flux density
  (tesla); $\oint\vec{B}\cdot d\vec{A} = 0$ since field lines are closed loops.
- The magnetising field is $H = NI/l$ (A m⁻¹); magnetisation is $M = m/V$
  (A m⁻¹); inside matter $B = \mu_0(H+M)$.
- $\chi_m = M/H$, $\mu = B/H$, $\mu_r = \mu/\mu_0$ and $\mu_r = 1 + \chi_m$. Both
  $\chi_m$ and $\mu_r$ are dimensionless.
- Hysteresis is the lag of $B$ behind $H$. Retentivity $B_r$ is the flux density
  left when $H = 0$; coercivity $H_c$ is the reverse field that makes $B = 0$.
- Energy dissipated per unit volume per cycle equals the loop area,
  $\oint H\,dB$ (J m⁻³); the hysteresis power loss is (area) $\times V \times f$.
- Soft materials (small $H_c$, narrow loop) are for transformer cores and
  electromagnets; hard materials (large $H_c$, broad loop) are for permanent
  magnets.
- Diamagnetics: $\chi_m$ small negative, $\mu_r < 1$, repelled. Paramagnetics:
  $\chi_m$ small positive, $\mu_r > 1$, $\chi_m = C/T$. Ferromagnetics: domains,
  $\chi_m \gg 1$, saturation and hysteresis, and $\chi_m = C/(T - T_C)$ above the
  Curie temperature.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The SI unit of magnetic susceptibility is <span class="marks">[1]</span>
   (a) tesla (b) A m⁻¹ (c) weber (d) it has no unit
2. For a paramagnetic substance <span class="marks">[1]</span>
   (a) $\chi_m < 0,\ \mu_r < 1$ (b) $\chi_m > 0,\ \mu_r > 1$ (c) $\chi_m \gg 1$ (d) $\mu_r = 1$
3. The area of a B–H hysteresis loop represents <span class="marks">[1]</span>
   (a) retentivity (b) coercivity (c) energy lost per unit volume per cycle (d) permeability
4. Soft iron rather than steel is used for a transformer core because it has <span class="marks">[1]</span>
   (a) high coercivity (b) low coercivity and small loop area (c) low permeability (d) high density
5. Above its Curie temperature, iron becomes <span class="marks">[1]</span>
   (a) diamagnetic (b) paramagnetic (c) non-magnetic (d) more strongly ferromagnetic

::: note Answers to Group A
**1.** (d) — $\chi_m = M/H$, and $M$ and $H$ share the unit A m⁻¹, so the ratio is a pure number.
**2.** (b) — the moments align weakly with the field, so $M$ is positive and $\mu_r = 1+\chi_m > 1$.
**3.** (c) — the loop area is $\oint H\,dB$, whose unit is J m⁻³.
**4.** (b) — the core is remagnetised 100 times a second, so the loop area (energy wasted) must be small.
**5.** (b) — thermal agitation destroys domain alignment, leaving randomly oriented permanent moments.
:::

**Group B — Short answer (5 marks each)**

1. Define magnetic flux and magnetic flux density, and state their SI units.
   Distinguish clearly between $\vec{B}$ and $\vec{H}$. <span class="marks">[5]</span>
2. Define magnetic susceptibility and relative permeability, and derive the
   relation $\mu_r = 1 + \chi_m$. <span class="marks">[5]</span>
3. A solenoid with $400$ turns per metre carries a current of $3.0\ \text{A}$ and
   is filled with an iron core of relative permeability $800$. Calculate $H$, $B$,
   $M$ and $\chi_m$. <span class="marks">[5]</span>
4. Explain, with reference to the hysteresis loop, why soft iron is used in
   electromagnets while steel is used for permanent magnets. <span class="marks">[5]</span>
5. State Curie's law. A paramagnetic sample has $\chi_m = 3.6\times10^{-4}$ at
   $200\ \text{K}$. Find its susceptibility at $300\ \text{K}$. <span class="marks">[5]</span>

::: note Answers to Group B
**3.** $H = nI = 400\times3.0 = 1.2\times10^{3}\ \text{A m}^{-1}$.
$B = \mu_0\mu_rH = (4\pi\times10^{-7})(800)(1200) = 1.21\ \text{T}$.
$\chi_m = \mu_r - 1 = 799$.
$M = \chi_mH = 799\times1200 = 9.59\times10^{5}\ \text{A m}^{-1}$.

**4.** Outline: an electromagnet must switch on and off, so it needs a **small
coercivity** (demagnetises the instant the current stops) and a **small loop
area** (little heat wasted per cycle) — soft iron. A permanent magnet must keep
its magnetism against stray fields and knocks, so it needs a **large coercivity**
and large retentivity — steel. Sketch the narrow and broad loops side by side.

**5.** Curie's law: for a paramagnetic material $\chi_m = C/T$, i.e. the
susceptibility is inversely proportional to the absolute temperature.
$\chi_2 = \chi_1T_1/T_2 = 3.6\times10^{-4}\times200/300 = 2.4\times10^{-4}$.
:::

**Group C — Long answer (8 marks each)**

1. (a) What is hysteresis? Draw a complete hysteresis loop for a ferromagnetic
   material and define retentivity and coercivity on it. <span class="marks">[4]</span>
   (b) Show that the energy dissipated per unit volume per cycle equals the area
   of the loop. A core of volume $0.010\ \text{m}^{3}$ whose loop area is
   $300\ \text{J m}^{-3}$ is used at $50\ \text{Hz}$; find the power lost as
   heat. <span class="marks">[4]</span>
2. Compare diamagnetic, paramagnetic and ferromagnetic materials with respect to
   susceptibility, relative permeability, behaviour of field lines, behaviour in
   a non-uniform field and effect of temperature, giving two examples of each.
   Hence explain what happens to a ferromagnetic material as it is heated through
   its Curie temperature. <span class="marks">[8]</span>

::: note Answers to Group C
**1.** (a) Hysteresis is the lagging of $B$ behind $H$ over a magnetising cycle;
$B_r$ (retentivity) is the intercept on the $B$-axis, $H_c$ (coercivity) the
intercept on the $H$-axis. See the labelled loop in §17.3.

(b) For a ring of volume $V = Al$ and $N$ turns, the source does work
$dW = eI\,dt = NI\,d\Phi = NI A\,dB = (Al)H\,dB$, so
$W/V = \oint H\,dB$ = loop area. Numerically, energy per cycle
$= 300\times0.010 = 3.0\ \text{J}$, and

$$ P = Wf = 3.0\times50 = 150\ \text{W} $$

**2.** Outline: reproduce the comparison table of §17.4 with two examples each
(Bi and Cu; Al and Pt; Fe and Ni). For the Curie point: below $T_C$ the exchange
interaction holds neighbouring atomic moments parallel inside domains, giving
huge $\chi_m$, saturation and hysteresis. As $T$ rises, thermal energy disrupts
this order; at $T = T_C$ the domain structure collapses completely. Above $T_C$
the atoms keep their individual moments but point randomly, so the material is
paramagnetic with $\chi_m = C/(T-T_C)$, a value smaller by several orders of
magnitude. For iron $T_C = 1043\ \text{K}$; a red-hot iron nail is not attracted
by a magnet.
:::
