---
subject: Physics
grade: 12
unit: 18
title: Electromagnetic Induction
hours: 6
area: Electricity and Magnetism
---

In 1831 Michael Faraday showed that a *changing* magnetic field drives a current.
That discovery is why power generated at Kulekhani can be stepped up to 220 kV,
carried across the country and stepped back down for your house. Two laws run the
whole unit: Faraday's, which gives *how big* the induced e.m.f. is, and Lenz's,
which gives *which way* it drives current.

::: key How this unit is examined
Group C asks for one of three derivations: motional e.m.f. $e = Blv$, the
generator equation $e = NBA\omega\sin\omega t$, or the transformer turns-ratio
with its losses. Group B likes solenoid self-inductance, $U = \frac{1}{2}LI^{2}$
and numericals on $e = -N\,d\Phi/dt$. Never drop the minus sign — it *is* Lenz's
law.
:::

## 18.1 Faraday's laws; Induced electric fields

Move a magnet towards a coil joined to a galvanometer and the needle deflects.
Stop the magnet and the needle returns to zero even though the magnet is still
there. Move it away and the needle deflects the *other* way. What matters is not
the flux but the **rate of change** of flux.

```figure caption="Faraday's experiment. Only while the flux linked with the coil is changing does the galvanometer deflect; a faster movement gives a bigger deflection."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Ellipse
fig, ax = plt.subplots(figsize=(5.0,2.9))
ax.add_patch(Rectangle((-1.95,-0.34), 0.80, 0.68, facecolor='#6a8fb5',
                       alpha=0.85, edgecolor=INK, lw=1.0))
ax.add_patch(Rectangle((-1.15,-0.34), 0.80, 0.68, facecolor='#d9534f',
                       alpha=0.85, edgecolor=INK, lw=1.0))
ax.annotate('S', (-1.55,0), color='white', fontsize=10.5, ha='center', va='center')
ax.annotate('N', (-0.75,0), color='white', fontsize=10.5, ha='center', va='center')
ax.annotate('', xy=(-0.20,1.06), xytext=(-1.25,1.06),
            arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.7, mutation_scale=14))
ax.annotate('magnet moved in', (-0.72,1.26), ha='center', color=INK, fontsize=8.8)
for k in range(5):
    ax.add_patch(Ellipse((0.18+0.27*k, 0.0), 0.22, 1.60, facecolor='none',
                         edgecolor='#b8860b', lw=1.7))
ax.annotate('coil of N turns', (1.18,-1.12), ha='center', color='#b8860b', fontsize=8.8)
ax.plot([0.18,0.18,2.95],[0.80,1.80,1.80], color=INK, lw=1.1)
ax.plot([2.95,2.95],[1.80,0.44], color=INK, lw=1.1)
ax.plot([0.18,0.18,2.95],[-0.80,-1.80,-1.80], color=INK, lw=1.1)
ax.plot([2.95,2.95],[-1.80,-0.44], color=INK, lw=1.1)
ax.add_patch(Circle((2.95,0), 0.44, facecolor='none', edgecolor=INK, lw=1.3))
ax.annotate('', xy=(3.17,0.28), xytext=(2.95,-0.14),
            arrowprops=dict(arrowstyle='-|>', color='#d9534f', lw=1.5, mutation_scale=10))
ax.plot([2.95],[-0.17],'o',color=INK,ms=3.2)
ax.annotate('G', (2.44,0.10), ha='right', color=INK, fontsize=10.5)
ax.set_xlim(-2.55, 3.85); ax.set_ylim(-2.10, 1.95)
ax.set_aspect('equal'); ax.axis('off')
```
::: definition Faraday's laws of electromagnetic induction
**First law.** Whenever the magnetic flux linked with a circuit changes, an
e.m.f. is induced in it; the e.m.f. lasts only as long as the change lasts.

**Second law.** The magnitude of the induced e.m.f. is directly proportional to
the rate of change of flux linkage:

$$ e = -N\frac{d\Phi}{dt} = -\frac{d(N\Phi)}{dt} $$

The product $N\Phi$ is called the **flux linkage**, measured in weber-turns.
:::

Since $\Phi = BA\cos\theta$, the linkage changes if $B$ changes, if $A$ changes,
or if the coil turns. All three are used in real machines.

If the circuit has total resistance $R$, the induced current is $I = e/R$ and the
**charge** that flows in a change is independent of how fast the change happens:

$$ q = \int I\,dt = \int \frac{N}{R}\frac{d\Phi}{dt}dt = \frac{N\,\Delta\Phi}{R} $$

**Induced electric fields.** A stationary coil in a changing field has charges
that are not moving, so no magnetic force acts on them. Something else must push
them — a changing magnetic field creates an **electric field** in the space
around it, even where there is no wire:

$$ \oint \vec{E}\cdot d\vec{l} = -\frac{d\Phi}{dt} $$

This induced field is **non-conservative**: its line integral round a closed loop
is not zero, so no potential can be defined for it.

::: example Worked example 18.1
**Problem.** A coil of $200$ turns and area $300\ \text{cm}^{2}$ is placed with
its plane perpendicular to a magnetic field. The field increases uniformly from
$0.20\ \text{T}$ to $0.60\ \text{T}$ in $0.40\ \text{s}$. The coil has a
resistance of $12\ \Omega$. Find (a) the induced e.m.f., (b) the induced current
and (c) the charge that circulates.

**Solution.** $A = 300\ \text{cm}^{2} = 3.0\times10^{-2}\ \text{m}^{2}$ and
$\theta = 0$, so $\Phi = BA$.

(a) $$ |e| = NA\frac{dB}{dt} = 200 \times 3.0\times10^{-2}\times\frac{0.60-0.20}{0.40} = 200\times0.03\times1.0 = 6.0\ \text{V} $$

(b) $$ I = \frac{|e|}{R} = \frac{6.0}{12} = 0.50\ \text{A} $$

(c) $$ q = \frac{N\,\Delta\Phi}{R} = \frac{200\times(3.0\times10^{-2}\times0.40)}{12} = \frac{2.4}{12} = 0.20\ \text{C} $$
:::

## 18.2 Lenz's law; Motional electromotive force

::: definition Lenz's law
The induced current always flows in such a direction that it **opposes the change
in flux that produced it**.
:::

In the figure below, the N-pole of a magnet approaches a coil. The flux through
the coil towards the right is increasing, so the induced current flows so as to
make the near face of the coil a **north pole**, which repels the approaching
magnet. Pull the magnet away and the current reverses, the near face becomes a
**south pole**, and the coil tries to hold the magnet back.

```figure caption="Lenz's law. An approaching N-pole induces an anticlockwise current (seen from the magnet) that makes the near face a north pole, and the coil repels the magnet."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Ellipse
fig, ax = plt.subplots(figsize=(5.0,2.8))
ax.add_patch(Rectangle((-1.70,-0.30), 0.68, 0.60, facecolor='#6a8fb5',
                       alpha=0.85, edgecolor=INK, lw=1.0))
ax.add_patch(Rectangle((-1.02,-0.30), 0.68, 0.60, facecolor='#d9534f',
                       alpha=0.85, edgecolor=INK, lw=1.0))
ax.annotate('S', (-1.36,0), color='white', fontsize=10, ha='center', va='center')
ax.annotate('N', (-0.68,0), color='white', fontsize=10, ha='center', va='center')
ax.annotate('', xy=(0.12,0.72), xytext=(-0.72,0.72),
            arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.6, mutation_scale=13))
ax.annotate('$v$', (-0.30,0.86), ha='center', color=INK, fontsize=10)
for k in range(4):
    ax.add_patch(Ellipse((0.60+0.32*k, 0.0), 0.24, 1.70, facecolor='none',
                         edgecolor='#b8860b', lw=1.8))
ax.annotate('N', (0.60, 1.06), ha='center', color='#0B6A62', fontsize=10.5)
ax.annotate('S', (1.56, 1.06), ha='center', color='#0B6A62', fontsize=10.5)
ax.annotate('induced poles of the coil', (1.08, 1.34), ha='center',
            color='#0B6A62', fontsize=8.4)
s = np.linspace(-1.05, 1.05, 60)
ax.plot(0.60+0.12*np.sin(s), 0.85*np.cos(s), color='#d9534f', lw=1.7)
ax.annotate('', xy=(0.60+0.12*np.sin(-1.22), 0.85*np.cos(-1.22)),
            xytext=(0.60+0.12*np.sin(-1.05), 0.85*np.cos(-1.05)),
            arrowprops=dict(arrowstyle='-|>', color='#d9534f', lw=1.7, mutation_scale=13))
ax.annotate('induced current', (2.55,-0.55), color='#d9534f', fontsize=8.8)
ax.annotate('', xy=(0.74,-0.42), xytext=(2.50,-0.50),
            arrowprops=dict(arrowstyle='-', color='#d9534f', lw=0.8))
ax.annotate('', xy=(-1.95,0.0), xytext=(-1.75,0.0),
            arrowprops=dict(arrowstyle='-|>', color='#0B6A62', lw=1.6, mutation_scale=13))
ax.annotate('force on magnet\n(repulsion)', (-2.05,-0.05), ha='right', va='center',
            color='#0B6A62', fontsize=8.6)
ax.set_xlim(-3.55, 4.10); ax.set_ylim(-1.30, 1.65)
ax.set_aspect('equal'); ax.axis('off')
```
Lenz's law is **conservation of energy in disguise**. If the induced current
helped the magnet, the magnet would accelerate by itself while the coil also got
hot — energy from nothing. Because the coil pushes back, the work you do moving
the magnet reappears as electrical energy. That is what the minus sign in
$e = -N\,d\Phi/dt$ says.

### Motional e.m.f.

```figure caption="A rod of length $l$ sliding at speed $v$ on rails in a field $B$ into the page. The flux enclosed grows, so an e.m.f. $Blv$ drives a current, and the field then opposes the motion with a force $BIl$."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(4.8,2.8))
BB = dict(facecolor='white', edgecolor='none', pad=1.2)
for xx in np.arange(0.50, 4.30, 0.46):
    for yy in np.arange(0.32, 1.75, 0.39):
        ax.plot([xx],[yy], marker='x', color=MUTED, ms=4.0, mew=0.9)
ax.annotate('×  B into the page', (4.35,2.25), color=MUTED, fontsize=8.8, ha='right')
ax.plot([0.15,4.35],[0.10,0.10], color=INK, lw=1.6)
ax.plot([0.15,4.35],[1.90,1.90], color=INK, lw=1.6)
ax.plot([0.15,0.15],[0.10,0.72], color=INK, lw=1.6)
ax.plot([0.15,0.15],[1.28,1.90], color=INK, lw=1.6)
ax.add_patch(Rectangle((-0.04,0.72), 0.38, 0.56, facecolor='white',
                       edgecolor=INK, lw=1.3, zorder=4))
ax.annotate('R', (-0.16,1.00), ha='right', va='center', color=INK, fontsize=9.5)
ax.plot([2.55,2.55],[0.10,1.90], color='#d9534f', lw=3.2, solid_capstyle='butt', zorder=5)
ax.annotate('', xy=(3.40,1.02), xytext=(2.74,1.02),
            arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.6, mutation_scale=13))
ax.annotate('$v$', (3.07,1.20), ha='center', va='bottom', color=INK, fontsize=10, bbox=BB)
ax.annotate('', xy=(2.55,1.68), xytext=(2.55,0.32),
            arrowprops=dict(arrowstyle='-|>', color='#0B6A62', lw=1.5, mutation_scale=12))
ax.annotate('$I$', (2.72,1.62), ha='left', va='center', color='#0B6A62', fontsize=10, bbox=BB)
ax.annotate('', xy=(1.86,1.02), xytext=(2.42,1.02),
            arrowprops=dict(arrowstyle='-|>', color='#0B6A62', lw=1.5, mutation_scale=12))
ax.annotate('$F = BIl$', (2.14,1.20), ha='center', va='bottom', color='#0B6A62',
            fontsize=9, bbox=BB)
ax.annotate('', xy=(2.48,0.52), xytext=(0.22,0.52),
            arrowprops=dict(arrowstyle='<->', color=ACCENT, lw=0.9, mutation_scale=8))
ax.annotate('$x$', (1.35,0.52), ha='center', va='center', color=ACCENT, fontsize=9.5, bbox=BB)
ax.annotate('$l$', (2.70,0.24), ha='left', va='center', color='#d9534f', fontsize=10, bbox=BB)
ax.set_xlim(-0.55, 4.75); ax.set_ylim(-0.20, 2.55)
ax.set_aspect('equal'); ax.axis('off')
```
::: derivation Motional e.m.f. $e = Blv$
A conducting rod of length $l$ slides with speed $v$ on frictionless rails in a
uniform field $B$ perpendicular to the plane of the rails. After time $t$ the
enclosed area is $A = lx$, so the flux is $\Phi = Blx$. Then

$$ e = -\frac{d\Phi}{dt} = -Bl\frac{dx}{dt} = -Blv $$

so the magnitude of the e.m.f. is $\boxed{e = Blv}$.

**By the force on the charges.** A free charge in the rod moves at speed $v$, so
it feels a force $qvB$ along the rod. Charge separates until the electric field
balances it, $qE = qvB$, giving $E = vB$ and $e = El = Blv$ — the same answer.

**Energy check.** The induced current is $I = Blv/R$, and the field exerts a
retarding force $F = BIl = B^{2}l^{2}v/R$ on the rod. The mechanical power needed
to keep it moving is

$$ P = Fv = \frac{B^{2}l^{2}v^{2}}{R} = I^{2}R $$

which is exactly the electrical power dissipated. No energy is created.
:::

If the rod moves at an angle $\theta$ to the field, only the perpendicular
component counts and $e = Blv\sin\theta$.

::: example Worked example 18.2
**Problem.** A rod of length $0.50\ \text{m}$ slides on rails at
$4.0\ \text{m s}^{-1}$ in a uniform field of $0.80\ \text{T}$ perpendicular to
the plane of the rails. The circuit resistance is $2.0\ \Omega$. Find the e.m.f.,
the current, the force needed to keep the rod moving uniformly, and the power
supplied. Verify that the power supplied equals the heat produced.

**Solution.**

$$ e = Blv = 0.80\times0.50\times4.0 = 1.6\ \text{V} $$
$$ I = \frac{e}{R} = \frac{1.6}{2.0} = 0.80\ \text{A} $$
$$ F = BIl = 0.80\times0.80\times0.50 = 0.32\ \text{N} $$
$$ P = Fv = 0.32\times4.0 = 1.28\ \text{W} $$

Heat produced: $I^{2}R = (0.80)^{2}\times2.0 = 1.28\ \text{W}$. The two agree, as
Lenz's law requires.
:::

::: caution The minus sign is not decoration
$e = -N\,d\Phi/dt$. The sign carries the whole physical content of Lenz's law, so
state the signed form first and take magnitudes only afterwards.
:::

## 18.3 A.C. generators; Eddy currents

An **a.c. generator (dynamo)** converts mechanical energy into electrical energy
by rotating a coil in a magnetic field. Its parts are an **armature** (a coil of
$N$ turns wound on a soft-iron core), a **field magnet**, two **slip rings** and
two carbon **brushes**.

::: derivation The generator equation
Let the coil of $N$ turns and area $A$ rotate with constant angular velocity
$\omega$ in a uniform field $B$. If the normal to the coil makes angle
$\theta = \omega t$ with $\vec{B}$, the flux linked is

$$ \Phi = BA\cos\omega t $$

By Faraday's law,

$$ e = -N\frac{d\Phi}{dt} = -NBA\frac{d}{dt}(\cos\omega t) = NBA\omega\sin\omega t $$

So $e = e_0\sin\omega t$ with **peak e.m.f.** $e_0 = NBA\omega = 2\pi f NBA$.
:::

The e.m.f. is maximum when the coil's plane is **parallel** to the field (lines
are cut fastest) and zero when it is **perpendicular**, even though the flux is
then greatest. A split-ring commutator in place of the slip rings gives a d.c.
generator.

```figure caption="Output of an a.c. generator, $e = NBA\omega\sin\omega t$. The e.m.f. is zero when the flux is maximum and maximum when the flux is zero."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,2.6))
t = np.linspace(0, 2, 500)
ax.plot(t, np.sin(2*np.pi*t), color=ACCENT, lw=2.0, label=r'e.m.f.  $e = e_0\sin\omega t$')
ax.plot(t, np.cos(2*np.pi*t), color=MUTED, lw=1.3, ls=(0,(4,2)),
        label=r'flux  $\Phi = \Phi_0\cos\omega t$')
ax.axhline(0, color=INK, lw=0.9)
for xv in [0.0, 0.25, 0.5, 0.75, 1.0]:
    ax.axvline(xv, color=GRID, lw=0.8)
ax.annotate('coil plane normal to B\n(flux max, e = 0)', (0.02,-1.75), color=MUTED,
            fontsize=8.0, ha='left')
ax.annotate('coil plane along B\n(flux 0, e max)', (0.25,1.22), color=ACCENT,
            fontsize=8.0, ha='center')
ax.set_xlabel('time in periods  $t/T$'); ax.set_ylabel('normalised value')
ax.set_xlim(0,2); ax.set_ylim(-2.0,2.0)
ax.set_yticks([-1,0,1])
ax.spines[['top','right']].set_visible(False)
ax.legend(loc='upper right', fontsize=8.0)
```

### Eddy currents

When a **solid** block of metal sits in a changing magnetic field, the induced
e.m.f. drives swirling closed loops of current through the metal. These are
**eddy currents**. The resistance of a solid block is tiny, so the currents are
large, the $I^2R$ heating is wasteful, and by Lenz's law they oppose the motion
that produced them.

| Eddy currents as a nuisance | Eddy currents put to work |
|---|---|
| Heat and energy loss in transformer and motor cores | Induction furnace for melting metals |
| Damping and heating in dynamo armatures | Induction cooker / induction heating |
| Reduced efficiency of chokes | Electromagnetic braking in trains and treadmills |
| — | Dead-beat galvanometers and speedometers |
| — | Induction-type energy meters |

They are reduced by **laminating** the core: varnished silicon-steel sheets
stacked with their planes parallel to the flux. This breaks the large eddy loops
into many small high-resistance ones, so the loss falls sharply.

## 18.4 Self-inductance and mutual inductance

**Self-inductance.** A changing current in a coil changes its own flux, which
induces an e.m.f. in the *same* coil opposing the change — a **back e.m.f.** For a
coil with no ferromagnetic core, the flux linkage is proportional to the current:

$$ N\Phi = LI \qquad\text{and}\qquad e = -N\frac{d\Phi}{dt} = -L\frac{dI}{dt} $$

::: definition Self-inductance and the henry
The **self-inductance** $L$ of a coil is the flux linkage per unit current,
$L = N\Phi/I$; equivalently it is the back e.m.f. per unit rate of change of
current. Its SI unit is the **henry (H)**: a coil has a self-inductance of one
henry if a current changing at $1\ \text{A s}^{-1}$ induces a back e.m.f. of
$1\ \text{V}$. Thus $1\ \text{H} = 1\ \text{Wb A}^{-1} = 1\ \text{V s A}^{-1}$.
:::

::: derivation Self-inductance of a long solenoid
For a solenoid of length $l$, cross-sectional area $A$ and $N$ turns carrying a
current $I$, the interior field is $B = \mu_0 nI$ with $n = N/l$. The flux through
one turn is $\Phi = BA = \mu_0 nIA$, so the flux linkage is

$$ N\Phi = \mu_0 n^{2}lAI \qquad\Longrightarrow\qquad L = \mu_0 n^{2}Al = \frac{\mu_0N^{2}A}{l} $$

With a core of relative permeability $\mu_r$ this becomes $L = \mu_0\mu_r N^{2}A/l$.
:::

Notice $L$ depends only on the **geometry** of the coil and the core material —
never on the current.

**Mutual inductance.** If a changing current $I_1$ in coil 1 links flux through a
nearby coil 2, an e.m.f. appears in coil 2:

$$ N_2\Phi_2 = MI_1, \qquad e_2 = -M\frac{dI_1}{dt} $$

$M$ is the **mutual inductance**, also measured in henry. For two coaxial
solenoids of the same length $l$ and area $A$,

$$ M = \frac{\mu_0 N_1N_2A}{l} $$

It is reciprocal ($M_{12} = M_{21}$) and related to the self-inductances by

$$ M = k\sqrt{L_1L_2} $$

where the **coefficient of coupling** $k$ lies between 0 and 1; $k \to 1$ for
coils wound on a common closed iron core, as in a transformer.

## 18.5 Energy stored in an inductor

::: derivation $U = \frac{1}{2}LI^{2}$
While the current in an inductor is growing, the source must work against the
back e.m.f. $e = -L\,dI/dt$. In time $dt$ the work done is

$$ dW = -eI\,dt = LI\frac{dI}{dt}dt = LI\,dI $$

Integrating from zero current to the final current $I$,

$$ W = \int_0^{I} LI\,dI = \tfrac{1}{2}LI^{2} $$

This work is not dissipated — it is stored in the magnetic field, and it comes
back when the current is switched off:

$$ U = \tfrac{1}{2}LI^{2} $$

**Energy density.** For a solenoid, $L = \mu_0n^{2}Al$ and $B = \mu_0nI$, so
$I = B/\mu_0 n$ and

$$ U = \tfrac{1}{2}\mu_0n^{2}Al\cdot\frac{B^{2}}{\mu_0^{2}n^{2}} = \frac{B^{2}}{2\mu_0}(Al) $$

Since $Al$ is the volume, the energy stored per unit volume of the field is

$$ u = \frac{B^{2}}{2\mu_0} $$
:::

::: example Worked example 18.3
**Problem.** An air-cored solenoid is $50\ \text{cm}$ long, has a cross-sectional
area of $4.0\ \text{cm}^{2}$ and $1000$ turns. Find (a) its self-inductance,
(b) the energy stored when it carries $2.0\ \text{A}$, and (c) the average
induced e.m.f. if this current is switched off in $10\ \text{ms}$.

**Solution.** $l = 0.50\ \text{m}$, $A = 4.0\times10^{-4}\ \text{m}^{2}$, $N = 1000$.

(a) $$ L = \frac{\mu_0N^{2}A}{l} = \frac{(4\pi\times10^{-7})(1000)^{2}(4.0\times10^{-4})}{0.50} = 1.01\times10^{-3}\ \text{H} $$

so $L \approx 1.0\ \text{mH}$.

(b) $$ U = \tfrac{1}{2}LI^{2} = \tfrac{1}{2}(1.01\times10^{-3})(2.0)^{2} = 2.0\times10^{-3}\ \text{J} = 2.0\ \text{mJ} $$

(c) $$ |e| = L\,\frac{\Delta I}{\Delta t} = (1.01\times10^{-3})\times\frac{2.0}{10\times10^{-3}} = 0.20\ \text{V} $$
:::

## 18.6 Transformer

A **transformer** changes an alternating voltage to another value at the same
frequency, by **mutual induction**. A primary of $N_p$ turns and a secondary of
$N_s$ turns share a laminated soft-iron core, so nearly all the primary's flux
also threads the secondary.

```figure caption="A step-down transformer. Both coils share the same flux $\Phi$ in the laminated soft-iron core, so $E_s/E_p = N_s/N_p$."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(4.8,2.9))
ax.add_patch(Rectangle((0.0,0.0), 3.4, 2.1, facecolor='none', edgecolor=INK, lw=1.4))
ax.add_patch(Rectangle((0.62,0.42), 2.16, 1.26, facecolor='none', edgecolor=INK, lw=1.4))
for xv in np.arange(0.08, 3.40, 0.15):
    ax.plot([xv,xv],[0.03,0.39], color=GRID, lw=0.7)
    ax.plot([xv,xv],[1.71,2.07], color=GRID, lw=0.7)
th = np.linspace(0, 7*2*np.pi, 500)
ax.plot(0.31+0.20*np.sin(th), 0.28+th/(7*2*np.pi)*1.55, color='#b8860b', lw=1.5)
th2 = np.linspace(0, 3*2*np.pi, 300)
ax.plot(3.09+0.20*np.sin(th2), 0.55+th2/(3*2*np.pi)*1.00, color='#0B6A62', lw=1.5)
ax.annotate('primary,  $N_p$ turns', (0.31,-0.34), ha='center', color='#b8860b', fontsize=8.6)
ax.annotate('secondary,  $N_s$ turns', (3.09,-0.34), ha='center', color='#0B6A62', fontsize=8.6)
ax.annotate('laminated soft-iron core', (1.70,2.62), ha='center', color=INK, fontsize=8.8)
ax.annotate('', xy=(1.95,1.89), xytext=(1.30,1.89),
            arrowprops=dict(arrowstyle='-|>', color='#d9534f', lw=1.4, mutation_scale=12))
ax.annotate('flux Φ', (1.62,2.18), ha='center', color='#d9534f', fontsize=8.8)
ax.plot([0.11,-0.60],[0.28,0.28], color='#b8860b', lw=1.2)
ax.plot([0.11,-0.60],[1.83,1.83], color='#b8860b', lw=1.2)
ax.annotate('$E_p$', (-0.70,1.05), ha='right', va='center', color='#b8860b', fontsize=10.5)
ax.plot([3.29,4.00],[0.55,0.55], color='#0B6A62', lw=1.2)
ax.plot([3.29,4.00],[1.55,1.55], color='#0B6A62', lw=1.2)
ax.annotate('$E_s$', (4.10,1.05), ha='left', va='center', color='#0B6A62', fontsize=10.5)
ax.set_xlim(-1.35, 4.75); ax.set_ylim(-0.80, 2.90)
ax.set_aspect('equal'); ax.axis('off')
```
::: derivation The turns-ratio relation
Let $\Phi$ be the flux through each turn of the core at time $t$. The same
$d\Phi/dt$ acts on both coils, so

$$ E_p = -N_p\frac{d\Phi}{dt}, \qquad E_s = -N_s\frac{d\Phi}{dt} $$

Dividing,

$$ \frac{E_s}{E_p} = \frac{N_s}{N_p} = k $$

where $k$ is the **turns ratio**. If $k > 1$ the transformer steps **up**; if
$k < 1$ it steps **down**.

For an ideal (100% efficient) transformer, input power equals output power:

$$ E_pI_p = E_sI_s \qquad\Longrightarrow\qquad \frac{I_s}{I_p} = \frac{N_p}{N_s} = \frac{1}{k} $$

So voltage is stepped up only at the cost of current, and vice versa.
:::

| Energy loss | Cause | Minimised by |
|---|---|---|
| Copper loss | $I^{2}R$ heating in the windings | thick, low-resistance copper wire |
| Eddy-current loss | induced currents in the core | laminated, varnished core sheets |
| Hysteresis loss | repeated remagnetisation of the core | soft core with a narrow loop (silicon steel) |
| Flux leakage | flux that misses the secondary | interleaved windings on a closed core |
| Humming (magnetostriction) | core vibrating at $2f$ | tight clamping of laminations |

Efficiency is $\eta = P_{\text{out}}/P_{\text{in}}$, typically 96–99%. High-voltage
transmission pays because the same power at ten times the voltage needs one-tenth
the current and so wastes one-hundredth the $I^{2}R$ heat in the line.

::: example Worked example 18.4
**Problem.** A step-down transformer at a substation in Hetauda converts
$11\ \text{kV}$ to $220\ \text{V}$. The primary has $5000$ turns, and the
secondary supplies $20\ \text{A}$. Find (a) the number of secondary turns,
(b) the output power, and (c) the primary current if the efficiency is $80\%$.

**Solution.**

(a) $$ N_s = N_p\frac{E_s}{E_p} = 5000\times\frac{220}{11000} = 100\ \text{turns} $$

(b) $$ P_{\text{out}} = E_sI_s = 220\times20 = 4400\ \text{W} = 4.4\ \text{kW} $$

(c) $$ P_{\text{in}} = \frac{P_{\text{out}}}{\eta} = \frac{4400}{0.80} = 5500\ \text{W} $$
$$ I_p = \frac{P_{\text{in}}}{E_p} = \frac{5500}{11000} = 0.50\ \text{A} $$

The $1100\ \text{W}$ difference is lost as heat in the copper and the core.
:::

## Chapter summary

- Faraday: an e.m.f. appears whenever flux linkage changes, $e = -N\,d\Phi/dt$;
  the charge circulated is $q = N\Delta\Phi/R$, independent of the time taken.
- A changing $\vec{B}$ produces a non-conservative induced electric field,
  $\oint\vec{E}\cdot d\vec{l} = -d\Phi/dt$.
- Lenz: the induced current opposes the change producing it — a statement of
  energy conservation, carried by the minus sign.
- Motional e.m.f. $e = Blv$ (or $Blv\sin\theta$); the retarding force is
  $B^{2}l^{2}v/R$ and $Fv = I^{2}R$.
- A.C. generator: $\Phi = BA\cos\omega t$ gives $e = NBA\omega\sin\omega t$ with
  peak value $e_0 = NBA\omega$.
- Eddy currents are reduced by laminating cores; they are used in induction
  furnaces, induction cookers and electromagnetic brakes.
- $L = N\Phi/I$, $e = -L\,dI/dt$, solenoid $L = \mu_0\mu_rN^{2}A/l$;
  $M = k\sqrt{L_1L_2}$ and $e_2 = -M\,dI_1/dt$. Unit: henry.
- Energy stored $U = \frac{1}{2}LI^{2}$; energy density $u = B^{2}/2\mu_0$.
- Transformer: $E_s/E_p = N_s/N_p$ and, if ideal, $I_s/I_p = N_p/N_s$. Losses are
  copper, eddy-current, hysteresis, leakage and humming.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. Lenz's law is a direct consequence of the conservation of <span class="marks">[1]</span>
   (a) charge (b) momentum (c) energy (d) magnetic flux
2. The SI unit of self-inductance, the henry, is equivalent to <span class="marks">[1]</span>
   (a) Wb A⁻¹ (b) Wb A (c) A Wb⁻¹ (d) V A⁻¹
3. Eddy currents in a transformer core are reduced by <span class="marks">[1]</span>
   (a) using thicker wire (b) laminating the core (c) using a steel core (d) increasing the frequency
4. In a step-up transformer, compared with the primary the secondary has <span class="marks">[1]</span>
   (a) more turns and larger current (b) more turns and smaller current
   (c) fewer turns and larger current (d) fewer turns and smaller current
5. A coil of self-inductance $L$ carries a current $I$. The energy stored is <span class="marks">[1]</span>
   (a) $LI^{2}$ (b) $\frac{1}{2}LI^{2}$ (c) $\frac{1}{2}L^{2}I$ (d) $LI$

::: note Answers to Group A
**1.** (c) — if the induced current aided the change, energy would be created from nothing.
**2.** (a) — from $L = N\Phi/I$, henry = weber per ampere.
**3.** (b) — laminations break the large eddy loops into small high-resistance ones.
**4.** (b) — $E_s/E_p = N_s/N_p$ and $E_pI_p = E_sI_s$, so a higher voltage means a lower current.
**5.** (b) — from $W = \int LI\,dI$.
:::

**Group B — Short answer (5 marks each)**

1. State Faraday's laws of electromagnetic induction and define magnetic flux
   linkage. Show that the charge induced in a circuit is independent of the time
   in which the flux change occurs. <span class="marks">[5]</span>
2. Derive an expression for the motional e.m.f. induced in a rod of length $l$
   moving with velocity $v$ perpendicular to a uniform field $B$, and show that
   the mechanical power supplied equals the heat produced. <span class="marks">[5]</span>
3. A coil of $100$ turns and area $0.050\ \text{m}^{2}$ lies with its plane
   perpendicular to a uniform field of $0.20\ \text{T}$. It is turned through
   $180^{\circ}$ in $0.10\ \text{s}$. Calculate the average induced e.m.f. <span class="marks">[5]</span>
4. Define self-inductance and derive an expression for the self-inductance of a
   long air-cored solenoid. <span class="marks">[5]</span>
5. What are eddy currents? Give two useful applications and two ways in which
   they are a nuisance, and state how they are minimised. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Outline: state both laws, define flux linkage $N\Phi$ (weber-turns).
For the charge, $I = e/R = (N/R)(d\Phi/dt)$, so
$q = \int I\,dt = N\Delta\Phi/R$ — it contains no $t$, so a slow change gives a
small current for a long time and a fast change a large current for a short time,
with the same total charge.

**3.** Initially $\Phi_1 = BA\cos0^{\circ} = 0.20\times0.050 = 0.010\ \text{Wb}$;
after turning, $\Phi_2 = BA\cos180^{\circ} = -0.010\ \text{Wb}$. So
$\Delta\Phi = -0.020\ \text{Wb}$ and

$$ |e| = N\frac{|\Delta\Phi|}{\Delta t} = 100\times\frac{0.020}{0.10} = 20\ \text{V} $$

**5.** Outline: circulating induced currents set up in the body of a conductor in
a changing field. Useful: induction furnace, induction cooker, electromagnetic
braking, dead-beat galvanometer. Nuisance: heating and loss in transformer cores
and motor armatures. Minimised by laminating the core with varnished
silicon-steel sheets parallel to the flux.
:::

**Group C — Long answer (8 marks each)**

1. (a) State Lenz's law and describe an experiment to verify it. Show that it
   follows from the principle of conservation of energy. <span class="marks">[4]</span>
   (b) Describe the construction of an a.c. generator and derive an expression
   for the instantaneous e.m.f. it produces. <span class="marks">[4]</span>
2. (a) Explain the principle and working of a transformer and derive the relation
   between the voltages and the numbers of turns. List its energy losses and how
   each is reduced. <span class="marks">[4]</span>
   (b) A transformer steps $240\ \text{V}$ down to $12\ \text{V}$. The primary has
   $1200$ turns, and the secondary delivers $5.0\ \text{A}$ to a lamp. Assuming
   the transformer is 90% efficient, find the number of secondary turns, the
   output power and the primary current. <span class="marks">[4]</span>

::: note Answers to Group C
**1.** Outline. (a) State the law; use the magnet-and-coil experiment of §18.2 —
pushing the N-pole in makes the near face a north pole (repulsion), withdrawing
it makes that face a south pole (attraction). Energy argument: an aiding current
would accelerate the magnet *and* heat the coil, creating energy from nothing.
(b) Armature, field magnet, slip rings, brushes; $\Phi = BA\cos\omega t$ gives
$e = NBA\omega\sin\omega t$, peak $e_0 = NBA\omega$.

**2.** (b) $N_s = N_p(E_s/E_p) = 1200\times(12/240) = 60$ turns.

$$ P_{\text{out}} = 12\times5.0 = 60\ \text{W} $$
$$ P_{\text{in}} = \frac{60}{0.90} = 66.7\ \text{W} $$
$$ I_p = \frac{66.7}{240} = 0.28\ \text{A} $$
:::
