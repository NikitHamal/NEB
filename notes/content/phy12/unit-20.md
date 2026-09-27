---
subject: Physics
grade: 12
unit: 20
title: Electrons
hours: 4
area: Modern Physics
---

The electron was discovered twice over. In 1897 J. J. Thomson measured the
**ratio** of its charge to its mass and showed that the same particle comes out
of every cathode, whatever the gas or the metal. In 1909 R. A. Millikan measured
the **charge itself** and found that it never comes in fractions. Put the two
numbers together and the mass of the electron drops out. This unit is those two
experiments, plus the piece of mechanics they both rest on: how a beam of
electrons moves when an electric or a magnetic field pushes it sideways.

::: key What the examiner wants
Two set-piece experiments — Millikan and Thomson — each a full Group C answer:
labelled diagram, theory, working formula, result. Between them sits a small
formula bank, $v=\sqrt{2eV_a/m}$, $y = eEL^{2}/2mv^{2}$, $r = mv/eB$ and
$v = E/B$, which carries almost every Group B numerical in this unit.
:::

## 20.1 Millikan's oil drop experiment

Millikan's question was simple: is electric charge continuous, like the volume of
water in a jug, or does it come in indivisible lumps? He answered it by weighing
single charged oil drops against an electric field.

```figure caption="Millikan's oil-drop apparatus (left) and the force balance on one drop (right): with the field off the drop falls at terminal velocity; with the field on it can be held stationary."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
fig = plt.figure(figsize=(5.1,3.3))
gs = fig.add_gridspec(1, 2, width_ratios=[2.3, 1.0], wspace=0.04)
ax = fig.add_subplot(gs[0]); bx = fig.add_subplot(gs[1])

ax.add_patch(Rectangle((1.0,0.7),8.2,6.0, fill=False, ec=MUTED, lw=1.2))
ax.add_patch(Rectangle((2.1,4.55),2.5,0.20, color=INK))
ax.add_patch(Rectangle((5.5,4.55),2.5,0.20, color=INK))
ax.add_patch(Rectangle((2.1,2.15),5.9,0.20, color=INK))
ax.annotate('pin-hole', (5.05,4.70), xytext=(30,14), textcoords='offset points',
            fontsize=7.6, color=MUTED,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.8))
# atomiser and spray
ax.add_patch(Rectangle((3.9,7.15),1.5,0.75, fill=False, ec=INK, lw=1.1))
ax.annotate('atomiser', (3.85,7.5), xytext=(-52,-2), textcoords='offset points',
            fontsize=8.0, color=INK)
ax.annotate('', xy=(5.05,4.95), xytext=(4.9,7.1),
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.1, mutation_scale=11))
ax.text(3.15,6.15,'oil spray', fontsize=7.6, color=MUTED)
# drop
ax.add_patch(Circle((5.05,3.55),0.13, color='#d9534f', zorder=5))
ax.annotate('charged drop', (5.20,3.50), xytext=(30,-24), textcoords='offset points',
            fontsize=8.0, color='#d9534f',
            arrowprops=dict(arrowstyle='-|>', color='#d9534f', lw=1.0, mutation_scale=9))
# plate separation
ax.annotate('', xy=(2.45,4.55), xytext=(2.45,2.35),
            arrowprops=dict(arrowstyle='<|-|>', color=INK, lw=1.0, mutation_scale=8))
ax.text(2.62,3.30,'$d$', fontsize=9.5, color=INK)
# battery / wiring
ax.plot([2.1,0.35,0.35],[4.65,4.65,3.95], color=INK, lw=1.1)
ax.plot([2.1,0.35,0.35],[2.25,2.25,2.95], color=INK, lw=1.1)
for yy,h in [(3.95,0.30),(3.72,0.16),(3.50,0.30),(3.27,0.16)]:
    ax.plot([0.35-h,0.35+h],[yy,yy], color=INK, lw=1.2)
ax.plot([0.35,0.35],[3.27,2.95], color=INK, lw=1.1)
ax.text(-0.35,3.52,'$V$', fontsize=9.5, color=INK)
ax.text(2.2,4.92,'+', fontsize=12, color=INK)
ax.text(2.2,1.70,'–', fontsize=12, color=INK)
# X-rays
ax.annotate('', xy=(4.55,2.85), xytext=(1.15,2.85),
            arrowprops=dict(arrowstyle='-|>', color='#2e8b57', lw=1.2, mutation_scale=10))
ax.text(1.20,2.48,'X-rays', fontsize=7.8, color='#2e8b57')
# microscope
ax.plot([9.2,10.6],[3.55,3.95], color=INK, lw=1.2)
ax.plot([9.2,10.6],[3.55,3.15], color=INK, lw=1.2)
ax.plot([10.6,10.6],[3.15,3.95], color=INK, lw=1.2)
ax.plot([5.3,9.2],[3.55,3.55], color=MUTED, lw=0.8, ls=(0,(4,3)))
ax.text(9.45,4.25,'microscope', fontsize=7.8, color=INK, ha='center')
ax.set_xlim(-0.9,11.2); ax.set_ylim(0.2,8.3); ax.axis('off')

# force panel
def drop(y0, lab):
    bx.add_patch(Circle((1.0,y0),0.17, color='#d9534f'))
    bx.text(1.0,y0-1.05,lab, fontsize=7.8, color=INK, ha='center')
def arrow(x,y0,y1,c,lab,dx):
    bx.annotate('', xy=(x,y1), xytext=(x,y0),
                arrowprops=dict(arrowstyle='-|>', color=c, lw=1.4, mutation_scale=10))
    bx.text(x+dx,(y0+y1)/2,lab, fontsize=8.0, color=c, va='center')
drop(3.55,'field off:  falls at $v_1$')
arrow(1.0,3.35,2.55,INK,'$mg$',0.12)
arrow(0.72,3.75,4.55,'#1d6fb8','$U$',-0.62)
arrow(1.28,3.75,4.55,'#2e8b57','$6\pi\eta r v_1$',0.10)
drop(1.05,'field on:  at rest')
arrow(1.0,0.85,0.05,INK,'$mg$',0.12)
arrow(0.72,1.25,2.05,'#1d6fb8','$U$',-0.62)
arrow(1.28,1.25,2.05,'#b8860b','$qE$',0.10)
bx.set_xlim(-0.7,2.6); bx.set_ylim(-0.35,5.1); bx.axis('off')
```
Fine drops of low-volatility oil are sprayed from an **atomiser** into the space
between two horizontal metal plates a distance $d$ apart. Friction in the nozzle
leaves each drop with a small charge; a beam of X-rays can add or remove further
electrons. A drop is watched through a travelling microscope against an
illuminated scale.

::: derivation The charge on a drop
**Stage 1 — field off.** The drop falls and quickly reaches a constant
(terminal) velocity $v_1$, when weight is balanced by upthrust plus the viscous
drag given by Stokes' law:

$$ \frac{4}{3}\pi r^{3}\rho g = \frac{4}{3}\pi r^{3}\sigma g + 6\pi\eta r v_1 $$

where $\rho$ is the density of the oil, $\sigma$ that of air and $\eta$ the
viscosity of air. Rearranging gives the radius of the drop:

$$ r = \sqrt{\frac{9\eta v_1}{2(\rho-\sigma)g}} $$

**Stage 2 — field on.** The pd $V$ is adjusted until the drop hangs
**stationary**. Now the drag is zero, and the upward electric force balances the
apparent weight:

$$ qE = \frac{q V}{d} = \frac{4}{3}\pi r^{3}(\rho-\sigma)g = 6\pi\eta r v_1 $$

$$ q = \frac{6\pi\eta r v_1 d}{V} = \frac{18\pi d}{V}\sqrt{\frac{\eta^{3}v_1^{3}}{2(\rho-\sigma)g}} $$

Every quantity on the right is measurable, so $q$ is measurable.
:::

In practice a drop is rarely balanced exactly. Millikan more often let it rise
with a steady velocity $v_2$ against the field. The drag then acts downwards and

$$ qE = \frac{4}{3}\pi r^{3}(\rho-\sigma)g + 6\pi\eta r v_2
= 6\pi\eta r (v_1+v_2) \;\Longrightarrow\; q = \frac{6\pi\eta r (v_1+v_2)d}{V} $$

Timing the same drop up and down many times, and using X-rays to change its
charge in between, he could watch $q$ jump in steps — and the steps were always
the same size.

Millikan repeated this for thousands of drops. The charges were never random:
every one was a whole-number multiple of the same small quantity.

$$ q = ne, \qquad n = 1,2,3,\dots, \qquad e = 1.60\times10^{-19}\ \text{C} $$

```figure caption="Charges measured on successive drops. Every value falls on a line $q = ne$ with $e = 1.6\\times10^{-19}$ C; no drop ever carries a fraction of $e$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.4,2.6))
n = np.array([3,5,4,7,6,4,8,5,3,6,9,7,2,6])
rng = np.random.default_rng(4)
q = 1.6*n + rng.normal(0,0.035,n.size)
for k in range(1,11):
    ax.axhline(1.6*k, color=GRID, lw=0.8, zorder=1)
ax.plot(np.arange(1,n.size+1), q, 'o', color='#d9534f', ms=5, zorder=3)
ax.set_xlabel('drop number')
ax.set_ylabel('measured charge  $q$')
ax.set_yticks([1.6*k for k in range(1,11)])
ax.set_yticklabels(['$e$','$2e$','$3e$','$4e$','$5e$','$6e$','$7e$','$8e$','$9e$','$10e$'])
ax.set_xlim(0.3, n.size+0.7); ax.set_ylim(0, 16.5)
ax.spines[['top','right']].set_visible(False)
```
::: key Quantisation of charge
Electric charge is not continuous. It exists only in integral multiples of the
elementary charge $e = 1.6\times10^{-19}\ \text{C}$. Millikan's experiment is the
direct experimental proof, and it also gives the value of $e$.
:::

::: caution Weight is not $mg$ here
The drop floats in air, so you must use the **apparent** weight
$\frac{4}{3}\pi r^{3}(\rho-\sigma)g$, not $\frac{4}{3}\pi r^{3}\rho g$. Students
also forget that the viscous force vanishes when the drop is *stationary* —
Stokes' drag depends on speed, and the speed is zero.
:::

::: example Worked example 20.1
**Problem.** In a Millikan apparatus the plates are $1.0\ \text{cm}$ apart. An oil
drop of mass $4.9\times10^{-15}\ \text{kg}$ is held stationary when the pd across
the plates is $1000\ \text{V}$. Find the charge on the drop and the number of
electrons it carries. (Neglect upthrust; $g = 9.8\ \text{m s}^{-2}$.)

**Solution.** The field between the plates is

$$ E = \frac{V}{d} = \frac{1000}{1.0\times10^{-2}} = 1.0\times10^{5}\ \text{V m}^{-1} $$

For equilibrium, $qE = mg$, so

$$ q = \frac{mg}{E} = \frac{4.9\times10^{-15}\times 9.8}{1.0\times10^{5}}
= \frac{4.802\times10^{-14}}{1.0\times10^{5}} = 4.8\times10^{-19}\ \text{C} $$

Number of electronic charges:

$$ n = \frac{q}{e} = \frac{4.8\times10^{-19}}{1.6\times10^{-19}} = 3 $$

The drop carries **3 excess electrons**.
:::

## 20.2 Motion of electron beam in electric and magnetic fields

An electron released from rest at a cathode and accelerated through a pd $V_a$
gains kinetic energy equal to the work done on it:

$$ eV_a = \frac{1}{2}mv^{2} \;\Longrightarrow\; v = \sqrt{\frac{2eV_a}{m}} $$

The speed depends on $\sqrt{V_a}$, not on $V_a$ — doubling the accelerating
voltage multiplies the speed by only $\sqrt{2}$.

### Transverse electric field

The beam now enters, at right angles, the field between two plates of length $L$
and separation $d$ held at pd $V_d$. Inside, $E = V_d/d$ and the electron has a
constant sideways acceleration $a = eE/m$, while its forward speed $v$ is
unchanged. This is exactly projectile motion: uniform velocity along the beam,
uniform acceleration across it, so the path is a **parabola**.

$$ x = vt, \qquad y = \frac{1}{2}\frac{eE}{m}t^{2} = \frac{eE}{2mv^{2}}x^{2} $$

At the far edge of the plates $x = L$, so the deflection there is

$$ y = \frac{eEL^{2}}{2mv^{2}} = \frac{eV_dL^{2}}{2mdv^{2}} = \frac{V_dL^{2}}{4V_ad} $$

using $v^{2} = 2eV_a/m$. Notice that $e$ and $m$ have cancelled: the deflection of
a cathode-ray spot depends only on the two voltages and the geometry. Beyond the
plates there is no field, so the electron travels in a straight line along the
tangent, making an angle $\theta$ with the axis where
$\tan\theta = eEL/mv^{2} = 2y/L$.

### Transverse magnetic field

A magnetic field $B$ perpendicular to the velocity exerts a force $F = evB$ that
is always perpendicular to the velocity. It therefore changes the direction but
never the speed: the path is a **circular arc** of radius $r$ given by

$$ evB = \frac{mv^{2}}{r} \;\Longrightarrow\; r = \frac{mv}{eB},
\qquad T = \frac{2\pi m}{eB} $$

The period $T$ is independent of the speed — the principle of the cyclotron.

```figure caption="An electron beam in a transverse electric field follows a parabola (left); in a transverse magnetic field it follows a circular arc of radius $r = mv/eB$ (right)."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, (ax, bx) = plt.subplots(1, 2, figsize=(5.1,2.5))

ax.add_patch(Rectangle((0.0,0.62),2.4,0.10, color=INK))
ax.add_patch(Rectangle((0.0,-0.72),2.4,0.10, color=INK))
ax.text(1.15,0.82,'+', fontsize=12, color=INK, ha='center')
ax.text(1.15,-1.08,'–', fontsize=12, color=INK, ha='center')
x1 = np.linspace(0,2.4,120); y1 = 0.088*x1**2
ax.plot([-1.0,0],[0,0], color='#d9534f', lw=1.8)
ax.plot(x1, y1, color='#d9534f', lw=1.8)
x2 = np.linspace(2.4,4.0,2)
ax.plot(x2, 0.088*2.4**2 + 2*0.088*2.4*(x2-2.4), color='#d9534f', lw=1.8, ls=(0,(5,2)))
ax.annotate('', xy=(-0.25,0), xytext=(-0.85,0),
            arrowprops=dict(arrowstyle='-|>', color='#d9534f', lw=1.6, mutation_scale=11))
ax.text(-1.0,0.18,'$v$', fontsize=9.5, color='#d9534f')
ax.annotate('', xy=(2.4,0.507), xytext=(2.4,0.0),
            arrowprops=dict(arrowstyle='<|-|>', color=MUTED, lw=0.9, mutation_scale=7))
ax.text(2.52,0.20,'$y$', fontsize=9.5, color=MUTED)
ax.plot([0,4.0],[0,0], color=MUTED, lw=0.7, ls=':')
ax.annotate('', xy=(2.4,-0.95), xytext=(0.0,-0.95),
            arrowprops=dict(arrowstyle='<|-|>', color=MUTED, lw=0.9, mutation_scale=7))
ax.text(1.2,-1.42,'$L$', fontsize=9.5, color=MUTED, ha='center')
ax.text(1.0,1.36,'electric field: parabola', fontsize=8.4, color=INK, ha='center')
ax.set_xlim(-1.4,4.2); ax.set_ylim(-1.85,1.75); ax.axis('off')

for i in np.linspace(0.3,3.3,6):
    for j in [-1.15,-0.62,0.32,0.85]:
        bx.plot([i],[j], marker='x', color='#1d6fb8', ms=3.4, mew=0.9)
R = 1.45
th = np.linspace(np.pi/2, 0.36, 160)
bx.plot([-1.0,0.0],[0,0], color='#d9534f', lw=1.8)
bx.plot(R*np.cos(th), -R + R*np.sin(th), color='#d9534f', lw=1.8)
bx.annotate('', xy=(-0.25,0), xytext=(-0.85,0),
            arrowprops=dict(arrowstyle='-|>', color='#d9534f', lw=1.6, mutation_scale=11))
bx.plot([0],[-R], marker='o', color=MUTED, ms=3.5)
bx.plot([0,0],[0,-R], color=MUTED, lw=0.9, ls=(0,(4,3)))
bx.plot([0,R*np.cos(0.36)],[-R,-R+R*np.sin(0.36)], color=MUTED, lw=0.9, ls=(0,(4,3)))
bx.text(0.20,-0.78,'$r$', fontsize=9.5, color=MUTED)
bx.text(1.2,1.36,'magnetic field: circle', fontsize=8.4, color=INK, ha='center')
bx.text(2.3,-1.58,'$B$ into page', fontsize=8.2, color='#1d6fb8', ha='center')
bx.set_xlim(-1.4,4.2); bx.set_ylim(-1.85,1.75); bx.axis('off')
```
### Crossed fields — the velocity selector

Apply $E$ and $B$ at right angles to each other and to the beam, so that the
electric force $eE$ and the magnetic force $evB$ act in opposite directions. Only
electrons of one particular speed pass straight through:

$$ eE = evB \;\Longrightarrow\; v = \frac{E}{B} $$

Faster electrons are bent by the magnetic force, slower ones by the electric
force. This "null method" is the heart of Thomson's experiment, and it is
accurate because setting a deflection to *zero* is much easier than measuring it.

These three results are the working parts of every electron-beam instrument.
The cathode-ray oscilloscope uses one pair of plates for the horizontal sweep and
another for the vertical signal, so the spot traces the waveform directly.
Television picture tubes and electron microscopes steer the beam magnetically,
because a magnetic deflection needs no high voltage inside the tube. The mass
spectrometer puts a velocity selector in front of a magnetic analyser, so that
$r = mv/qB$ then sorts ions purely by mass.

| Field | Force | Work done | Path | Speed |
|---|---|---|---|---|
| Electric $E$ | $eE$, along the field line | non-zero | parabola | changes |
| Magnetic $B$ | $evB$, perpendicular to $v$ | zero | circle | constant |

::: example Worked example 20.2
**Problem.** An electron is accelerated through $2000\ \text{V}$ and then enters
midway between two parallel plates $5.0\ \text{cm}$ long and $2.0\ \text{cm}$
apart, with $200\ \text{V}$ across them. Find (a) the speed of the electron,
(b) its deflection as it leaves the plates.
($e = 1.6\times10^{-19}\ \text{C}$, $m = 9.1\times10^{-31}\ \text{kg}$.)

**Solution.**

(a) From $eV_a = \frac{1}{2}mv^{2}$,

$$ v = \sqrt{\frac{2eV_a}{m}} = \sqrt{\frac{2\times1.6\times10^{-19}\times2000}{9.1\times10^{-31}}}
= \sqrt{7.03\times10^{14}} = 2.65\times10^{7}\ \text{m s}^{-1} $$

(b) Using the deflection formula,

$$ y = \frac{V_dL^{2}}{4V_ad} = \frac{200\times(5.0\times10^{-2})^{2}}{4\times2000\times2.0\times10^{-2}}
= \frac{200\times2.5\times10^{-3}}{160} = 3.1\times10^{-3}\ \text{m} $$

so the beam is deflected about $3.1\ \text{mm}$ — comfortably less than the
$1.0\ \text{cm}$ half-gap, so the electron does get out.
:::

## 20.3 Thomson's experiment to determine specific charge of electrons

The **specific charge** of a particle is the ratio $e/m$ — charge per unit mass.
Thomson measured it for cathode rays and found a value about $1800$ times larger
than that for the lightest known ion, the hydrogen ion. Either the charge was
enormous or the mass was tiny; the constancy of the result for every cathode
material showed it was a new, very light particle common to all matter.

```figure caption="Thomson's apparatus. The beam is accelerated, collimated, then passed through crossed electric and magnetic fields; the spot position is read on the fluorescent screen."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(5.1,2.7))
ax.plot([0.4,8.4,9.6,9.6,8.4,0.4,0.4],[1.32,1.32,2.25,-2.25,-1.32,-1.32,1.32],
        color=MUTED, lw=1.3)
ax.add_patch(Rectangle((0.55,-0.55),0.16,1.1, color=INK))
ax.text(0.62,-1.05,'C', fontsize=9, color=INK, ha='center')
ax.text(0.62,1.58,'cathode', fontsize=7.6, color=MUTED, ha='center')
for xp,lab in [(1.7,'A'),(2.8,'S')]:
    ax.add_patch(Rectangle((xp,0.16),0.14,0.95, color=INK))
    ax.add_patch(Rectangle((xp,-1.11),0.14,0.95, color=INK))
    ax.text(xp+0.07,-1.45,lab, fontsize=9, color=INK, ha='center')
ax.text(1.77,1.58,'anode', fontsize=7.6, color=MUTED, ha='center')
ax.text(2.87,1.58,'slit', fontsize=7.6, color=MUTED, ha='center')
ax.add_patch(Rectangle((4.3,0.52),2.0,0.13, color=INK))
ax.add_patch(Rectangle((4.3,-0.65),2.0,0.13, color=INK))
ax.text(5.3,0.78,'P  (+)', fontsize=8.2, color=INK, ha='center')
ax.text(5.3,-1.02,"P'  (–)", fontsize=8.2, color=INK, ha='center')
for i in np.linspace(4.45,6.15,6):
    for j in [-0.32,0.32]:
        ax.plot([i],[j], marker='x', color='#1d6fb8', ms=3.2, mew=0.9)
ax.text(5.3,1.72,'crossed  $E$  and  $B$', fontsize=8.2, color='#1d6fb8', ha='center')
ax.plot([0.75,9.55],[0,0], color='#d9534f', lw=1.8)
ax.plot([6.3,9.55],[0,0.95], color='#d9534f', lw=1.2, ls=(0,(5,2)))
ax.plot([6.3,9.55],[0,-0.95], color='#d9534f', lw=1.2, ls=(0,(3,2)))
ax.text(7.6,0.72,'$E$ only', fontsize=7.6, color='#d9534f', ha='center')
ax.text(7.6,-0.95,'$B$ only', fontsize=7.6, color='#d9534f', ha='center')
ax.plot([9.55,9.55],[-2.2,2.2], color='#2e8b57', lw=2.4)
ax.text(10.05,0,'screen', fontsize=8.2, color='#2e8b57', ha='center', rotation=90,
        va='center')
ax.annotate('', xy=(9.5,0.95), xytext=(9.5,0.0),
            arrowprops=dict(arrowstyle='<|-|>', color=INK, lw=0.9, mutation_scale=7))
ax.text(9.35,0.5,'$y$', fontsize=9.5, color=INK, ha='right')
ax.set_xlim(0.0,10.9); ax.set_ylim(-2.6,2.2); ax.axis('off')
```
**Method.** The tube is evacuated. Electrons boiled off the cathode C are
accelerated by the anode A, collimated by the slit S, and strike a fluorescent
screen, where they make a bright spot. Between the plates P and P' both an
electric field $E$ (from the plate pd) and a magnetic field $B$ (from coils
outside the tube, perpendicular to $E$) can be applied.

::: derivation Getting $e/m$ from two measurements
**Step 1 — find the speed.** Switch on both fields and adjust $B$ until the spot
returns to its undeflected position. The two forces are then equal and opposite:

$$ eE = evB \;\Longrightarrow\; v = \frac{E}{B} $$

**Step 2 — find the radius.** Switch the electric field off, leaving $B$ alone.
The magnetic force now provides the centripetal force and the beam bends into a
circle of radius $r$:

$$ evB = \frac{mv^{2}}{r} \;\Longrightarrow\; \frac{e}{m} = \frac{v}{Br} $$

**Combining the two,**

$$ \frac{e}{m} = \frac{E}{B^{2}r} $$

The radius is obtained from the measured deflection $y$ of the spot and the
geometry of the tube; for a short field region of length $L$, $r \approx L^{2}/2y$.

*Alternative route.* If instead the electric deflection $y$ is measured with the
magnetic field off, then $y = eEL^{2}/2mv^{2}$, and substituting $v = E/B$ from
Step 1 gives $e/m = 2yE/B^{2}L^{2}$.
:::

| Quantity | Modern accepted value |
|---|---|
| Specific charge of electron, $e/m$ | $1.76\times10^{11}\ \text{C kg}^{-1}$ |
| Electronic charge, $e$ (Millikan) | $1.60\times10^{-19}\ \text{C}$ |
| Mass of electron, $m = e \div (e/m)$ | $9.11\times10^{-31}\ \text{kg}$ |
| $e/m$ for the hydrogen ion | $9.58\times10^{7}\ \text{C kg}^{-1}$ |

The last two rows are the punchline: the electron's specific charge is $1837$
times that of the hydrogen ion, so the electron is about $1837$ times lighter
than the lightest atom.

::: example Worked example 20.3
**Problem.** In a Thomson-type tube the deflecting plates are $1.0\ \text{cm}$
apart with $300\ \text{V}$ across them. A magnetic field of
$1.0\times10^{-3}\ \text{T}$ leaves the beam undeflected. When the electric field
is switched off the beam bends into a circle of radius $17.0\ \text{cm}$. Find the
speed of the electrons, their specific charge, and hence the electron mass.

**Solution.** The electric field is

$$ E = \frac{V}{d} = \frac{300}{1.0\times10^{-2}} = 3.0\times10^{4}\ \text{V m}^{-1} $$

From the null condition,

$$ v = \frac{E}{B} = \frac{3.0\times10^{4}}{1.0\times10^{-3}} = 3.0\times10^{7}\ \text{m s}^{-1} $$

From the circular path,

$$ \frac{e}{m} = \frac{v}{Br} = \frac{3.0\times10^{7}}{1.0\times10^{-3}\times0.170}
= 1.76\times10^{11}\ \text{C kg}^{-1} $$

Taking $e = 1.6\times10^{-19}\ \text{C}$ from Millikan,

$$ m = \frac{e}{(e/m)} = \frac{1.6\times10^{-19}}{1.76\times10^{11}}
= 9.1\times10^{-31}\ \text{kg} $$
:::

::: tip Which formula, which experiment
Millikan gives $e$; Thomson gives $e/m$. Neither gives $m$ on its own. If a
question asks for the mass of the electron, it is asking you to combine the two.
:::

## Chapter summary

- Millikan balanced the apparent weight of a charged oil drop against an electric
  force: $q = mgd/V$ for a stationary drop, or
  $q = 6\pi\eta r v_1 d/V$ with $r = \sqrt{9\eta v_1/2(\rho-\sigma)g}$.
- Every measured charge is an integral multiple of
  $e = 1.60\times10^{-19}\ \text{C}$: charge is quantised.
- An electron accelerated through $V_a$ has speed $v = \sqrt{2eV_a/m}$.
- In a transverse electric field the path is a parabola with deflection
  $y = eEL^{2}/2mv^{2} = V_dL^{2}/4V_ad$ at the edge of the plates.
- In a transverse magnetic field the path is a circle, $r = mv/eB$, period
  $T = 2\pi m/eB$; the magnetic force does no work, so the speed is unchanged.
- Crossed fields select one speed: $v = E/B$.
- Thomson's tube gives $e/m = E/B^{2}r = 2yE/B^{2}L^{2}$; the accepted value is
  $1.76\times10^{11}\ \text{C kg}^{-1}$, which with Millikan's $e$ gives
  $m = 9.11\times10^{-31}\ \text{kg}$.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. Millikan's oil-drop experiment established that <span class="marks">[1]</span>
   (a) electrons have mass (b) charge is quantised (c) $e/m$ is constant (d) oil is an insulator
2. An electron accelerated from rest through a pd $V$ acquires a speed proportional to <span class="marks">[1]</span>
   (a) $V$ (b) $\sqrt{V}$ (c) $V^{2}$ (d) $1/V$
3. A charged particle enters a uniform magnetic field at right angles to it. Its path is <span class="marks">[1]</span>
   (a) a straight line (b) a parabola (c) a circle (d) a helix
4. In crossed electric and magnetic fields, the particles that pass undeflected have speed <span class="marks">[1]</span>
   (a) $EB$ (b) $E/B$ (c) $B/E$ (d) $E^{2}/B$
5. The specific charge of an electron is about <span class="marks">[1]</span>
   (a) $1.6\times10^{-19}\ \text{C kg}^{-1}$ (b) $9.1\times10^{-31}\ \text{C kg}^{-1}$
   (c) $1.76\times10^{11}\ \text{C kg}^{-1}$ (d) $9.58\times10^{7}\ \text{C kg}^{-1}$

::: note Answers to Group A
**1.** (b) — every drop charge came out as an integral multiple of $e$.
**2.** (b) — $eV = \frac12 mv^2$ gives $v \propto \sqrt{V}$.
**3.** (c) — the force $evB$ stays perpendicular to $v$, so the speed is constant and the path closes into a circle.
**4.** (b) — setting $eE = evB$ gives $v = E/B$.
**5.** (c) — $1.76\times10^{11}\ \text{C kg}^{-1}$; (d) is the value for the hydrogen ion.
:::

**Group B — Short answer (5 marks each)**

1. Describe Millikan's oil-drop experiment with a labelled diagram and derive an
   expression for the charge on a stationary drop. <span class="marks">[5]</span>
2. An oil drop of mass $1.96\times10^{-15}\ \text{kg}$ carrying two excess
   electrons is held stationary between horizontal plates $5.0\ \text{mm}$ apart.
   Find the pd applied across the plates. <span class="marks">[5]</span>
3. Show that the path of an electron entering a uniform transverse electric field
   is a parabola, and obtain the deflection at the end of the plates. <span class="marks">[5]</span>
4. An electron is accelerated through $500\ \text{V}$ and then enters a magnetic
   field of $2.0\times10^{-3}\ \text{T}$ at right angles. Find its speed and the
   radius of its circular path. <span class="marks">[5]</span>
5. Distinguish between the effects of an electric field and a magnetic field on a
   moving electron. <span class="marks">[5]</span>

::: note Answers to Group B
**2.** $q = 2e = 3.2\times10^{-19}\ \text{C}$ and
$mg = 1.96\times10^{-15}\times9.8 = 1.92\times10^{-14}\ \text{N}$. For equilibrium
$qV/d = mg$, so
$V = mgd/q = (1.92\times10^{-14}\times5.0\times10^{-3})/(3.2\times10^{-19}) = 300\ \text{V}$.

**4.** $v = \sqrt{2eV_a/m} = \sqrt{2\times1.6\times10^{-19}\times500/9.1\times10^{-31}}
= \sqrt{1.76\times10^{14}} = 1.33\times10^{7}\ \text{m s}^{-1}$. Then
$r = mv/eB = (9.1\times10^{-31}\times1.33\times10^{7})/(1.6\times10^{-19}\times2.0\times10^{-3})
= 1.21\times10^{-23}/3.2\times10^{-22} = 3.8\times10^{-2}\ \text{m} = 3.8\ \text{cm}$.

**5.** Outline: the electric force $eE$ is along the field and does work, so the
speed changes and the path is a parabola; the magnetic force $evB$ is
perpendicular to $v$, does no work, so the speed is constant and the path is a
circular arc. A magnetic field acts only on a *moving* charge; an electric field
acts on a charge at rest as well.
:::

**Group C — Long answer (8 marks each)**

1. (a) Draw a labelled diagram of Thomson's apparatus for measuring the specific
   charge of the electron. <span class="marks">[3]</span>
   (b) Explain the crossed-field (null) method and derive $e/m = E/B^{2}r$. Show
   how the mass of the electron follows when Millikan's value of $e$ is used. <span class="marks">[5]</span>
2. An electron accelerated through $1000\ \text{V}$ enters midway between two
   plates $4.0\ \text{cm}$ long and $1.0\ \text{cm}$ apart, with a pd of
   $100\ \text{V}$ between them. Find (a) the speed of the electron, (b) its
   deflection on leaving the plates, (c) the angle its path then makes with the
   axis, and (d) the magnetic flux density that would bring the beam back to the
   axis. <span class="marks">[8]</span>

::: note Answer to Group C question 2
(a) $v = \sqrt{2eV_a/m} = \sqrt{2\times1.6\times10^{-19}\times1000/9.1\times10^{-31}}
= \sqrt{3.52\times10^{14}} = 1.88\times10^{7}\ \text{m s}^{-1}$.

(b) $y = \dfrac{V_dL^{2}}{4V_ad} = \dfrac{100\times(4.0\times10^{-2})^{2}}{4\times1000\times1.0\times10^{-2}}
= \dfrac{0.16}{40} = 4.0\times10^{-3}\ \text{m} = 4.0\ \text{mm}$.

(c) $\tan\theta = 2y/L = (2\times4.0\times10^{-3})/(4.0\times10^{-2}) = 0.20$, so
$\theta = 11.3^{\circ}$.

(d) For no deflection, $eE = evB$ with $E = V_d/d = 100/0.010 = 1.0\times10^{4}\ \text{V m}^{-1}$:
$B = E/v = 1.0\times10^{4}/1.88\times10^{7} = 5.3\times10^{-4}\ \text{T}$.
:::
