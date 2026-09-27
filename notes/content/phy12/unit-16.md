---
subject: Physics
grade: 12
unit: 16
title: Magnetic field
hours: 9
area: Electricity and Magnetism
---

Before 1820 electricity and magnetism were two separate sciences. Then Oersted
noticed a compass needle twitch beside a current-carrying wire, and within ten
years Biot, Savart and Ampère had turned that twitch into a complete theory: a
moving charge makes a magnetic field, and a magnetic field pushes a moving
charge. This unit is the longest in the electricity section because every motor,
loudspeaker, galvanometer and Hall sensor you will ever meet is an application of
those two sentences.

::: key How this unit is examined
Two derivations appear again and again in Group C: the field of a long straight
conductor (Biot–Savart **or** Ampère) and the torque on a rectangular coil
leading to the moving-coil galvanometer. Group B favours $r = mv/qB$, the
solenoid, and the force between parallel wires with the definition of the ampere.
Learn the direction rules until they are automatic — half the marks lost in this
unit are lost on a wrong direction, not a wrong number.
:::

## 16.1 Magnetic field lines and magnetic flux; Oersted's experiment

A **magnetic field** is the region around a magnet or a current in which a
magnetic force can be detected. It is a vector field $\vec{B}$, called the
**magnetic flux density**, and its SI unit is the **tesla** (T), where
$1\ \text{T} = 1\ \text{N A}^{-1}\text{m}^{-1} = 1\ \text{Wb m}^{-2}$.

A **magnetic field line** is a line drawn so that its tangent at every point
gives the direction of $\vec{B}$ there. Their properties:

- They run from N to S **outside** a magnet and from S to N **inside** it, so
  every line is a **closed loop** — unlike electric field lines, which begin and
  end on charges.
- The number of lines per unit area crossing a surface at right angles measures
  the strength of $\vec{B}$: crowded lines mean a strong field.
- **Two field lines never intersect.** If they did, the field would have two
  directions at one point, which is impossible.
- Lines are in tension along their length and repel sideways — which is why
  unlike poles attract and like poles repel.

::: definition Magnetic flux
The magnetic flux through a surface of area $A$ placed in a uniform field
$\vec{B}$ is the product of the area and the component of $\vec{B}$ normal to it:

$$ \Phi = \vec{B}\cdot\vec{A} = BA\cos\theta $$

where $\theta$ is the angle between $\vec{B}$ and the normal to the surface. The
SI unit is the **weber** (Wb); $1\ \text{Wb} = 1\ \text{T m}^{2}$. Flux is a
**scalar**.
:::

Because every field line is a closed loop, every line that enters a closed
surface must leave it again. Hence **Gauss's law for magnetism**:

$$ \oint \vec{B}\cdot d\vec{A} = 0 $$

The net magnetic flux through any closed surface is zero: isolated magnetic
poles (monopoles) do not exist.

### Oersted's experiment

```figure caption="Left: Oersted's experiment — with the current flowing south to north in a wire above the needle, the N-pole deflects west. Right: the field of a long straight wire is a set of concentric circles; the dashed circle of radius $r$ is the Amperian loop of §16.7."

import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle
fig, axs = plt.subplots(1, 2, figsize=(5.2,2.9))

# ---- (a) Oersted -------------------------------------------------------
ax = axs[0]
ax.add_patch(Circle((0,0), 1.00, fc='white', ec=MUTED, lw=1.2, zorder=2))
for lab, p in [('N',(0,1.30)), ('S',(0,-1.30)), ('E',(1.30,0)), ('W',(-1.30,0))]:
    ax.annotate(lab, p, ha='center', va='center', fontsize=8.6, color=MUTED)
th = np.radians(133.0)
ax.annotate('', xy=(0.88*np.cos(th), 0.88*np.sin(th)),
            xytext=(-0.88*np.cos(th), -0.88*np.sin(th)),
            arrowprops=dict(arrowstyle='-|>', color='#A8271F', lw=2.4, mutation_scale=13))
ax.annotate('', xy=(0.62*np.cos(th), 0.62*np.sin(th)), xytext=(0, 0.62),
            arrowprops=dict(arrowstyle='-|>', color='#A8271F', lw=1.0,
                            connectionstyle='arc3,rad=0.35', mutation_scale=9))
ax.plot([0,0],[-2.05,2.05], color=ACCENT, lw=2.6, zorder=4)
ax.annotate('', xy=(0,1.84), xytext=(0,1.18),
            arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=2.2, mutation_scale=13))
ax.annotate('$I$', (0.20,1.66), color=ACCENT, fontsize=9.6)
ax.annotate('wire above\nthe needle', (1.62,1.55), ha='center', fontsize=8.0, color=ACCENT)
ax.annotate('deflected\nN-pole', (-1.55,1.25), ha='center', fontsize=8.0, color='#A8271F')
ax.annotate('at rest the needle lies N' + u'–' + 'S', (0,-2.20),
            ha='center', fontsize=8.0, color=MUTED)
ax.set_title('(a) Oersted 1820 ' + u'—' + ' plan view', fontsize=8.6)
ax.set_xlim(-2.7,2.7); ax.set_ylim(-2.6,2.5); ax.set_aspect('equal'); ax.axis('off')

# ---- (b) field of a straight wire -------------------------------------
ax = axs[1]
ax.add_patch(Circle((0,0), 0.16, fc='white', ec=INK, lw=1.4, zorder=5))
ax.plot([0],[0],'o', color=INK, ms=3.2, zorder=6)
ax.annotate('$I$ out of page', (0.26,0.30), fontsize=8.4, color=INK,
            bbox=dict(fc='white', ec='none', pad=1.5), zorder=7)
for R in (0.62, 1.10, 1.58, 2.06):
    dash = (R == 1.58)
    col = ACCENT if dash else MUTED
    ax.add_patch(Circle((0,0), R, fc='none', ec=col, lw=(1.4 if dash else 1.0),
                        ls=((0,(4,3)) if dash else '-'), zorder=2))
    a0 = np.radians(58)
    ax.annotate('', xy=(R*np.cos(a0+0.13), R*np.sin(a0+0.13)),
                xytext=(R*np.cos(a0), R*np.sin(a0)),
                arrowprops=dict(arrowstyle='-|>', color=col, lw=1.2, mutation_scale=10))
ar = np.radians(215)
ax.annotate('', xy=(1.58*np.cos(ar), 1.58*np.sin(ar)), xytext=(0,0),
            arrowprops=dict(arrowstyle='-|>', color='#A8271F', lw=1.2, mutation_scale=10))
ax.annotate('$r$', (-0.78,-0.44), color='#A8271F', fontsize=9.6)
ax.annotate('Amperian loop', (0.0,2.24), ha='center', fontsize=8.2, color=ACCENT)
ax.annotate(r'$B = \dfrac{\mu_0 I}{2\pi r}$', (0.0,-2.36), ha='center', fontsize=9.6)
ax.set_title('(b) field of a long straight wire', fontsize=8.6)
ax.set_xlim(-2.7,2.7); ax.set_ylim(-2.6,2.5); ax.set_aspect('equal'); ax.axis('off')
fig.tight_layout()
```
Hans Christian Oersted placed a straight wire **above** a pivoted compass needle
and parallel to it, i.e. along the magnetic north–south line. He found:

1. with no current, the needle rested along N–S;
2. with a current, the needle turned through a large angle and settled almost
   perpendicular to the wire;
3. reversing the current reversed the deflection;
4. the deflection increased with the current and decreased as the wire was moved
   further away.

**Conclusion: an electric current produces a magnetic field around it.**

::: memory SNOW and the right-hand grip rule
**SNOW** — current **S**outh to **N**orth in a wire **O**ver the needle sends the
N-pole **W**est.

**Right-hand grip rule** — grip the wire with the right hand, thumb along the
conventional current; the curled fingers give the direction of $\vec{B}$. This is
the rule to use for every straight-wire problem.
:::

## 16.2 Force on moving charge; Force on a conductor

A charge $q$ moving with velocity $\vec{v}$ in a field $\vec{B}$ experiences

$$ \vec{F} = q\,\vec{v}\times\vec{B}, \qquad F = qvB\sin\theta $$

where $\theta$ is the angle between $\vec{v}$ and $\vec{B}$.

```figure caption="Left: $\vec{F} = q\vec{v}\times\vec{B}$ is perpendicular to the plane of $\vec{v}$ and $\vec{B}$. Right: a positive charge projected at right angles to a uniform field moves in a circle of radius $r = mv/qB$."

import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle, Arc
fig, axs = plt.subplots(1, 2, figsize=(5.2,2.8))

ax = axs[0]
ax.annotate('', xy=(2.05,0), xytext=(0,0),
            arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=2.0, mutation_scale=13))
ax.annotate(r'$\vec{v}$', (2.14,-0.02), fontsize=10.5, color=ACCENT, va='center')
a = np.radians(52)
ax.annotate('', xy=(2.05*np.cos(a), 2.05*np.sin(a)), xytext=(0,0),
            arrowprops=dict(arrowstyle='-|>', color='#0B6A62', lw=2.0, mutation_scale=13))
ax.annotate(r'$\vec{B}$', (2.05*np.cos(a)+0.10, 2.05*np.sin(a)+0.10),
            fontsize=10.5, color='#0B6A62')
ax.add_patch(Arc((0,0), 1.5, 1.5, theta1=0, theta2=52, color=MUTED, lw=1.0))
ax.annotate(r'$\theta$', (0.92,0.30), fontsize=10, color=MUTED)
ax.add_patch(Circle((0,0), 0.22, fc='white', ec='#A8271F', lw=1.6, zorder=5))
ax.plot([0],[0],'o', color='#A8271F', ms=3.6, zorder=6)
ax.annotate(r'$\vec{F}$ out of the page' + '\n' + r'(for $+q$)', (-0.26,-0.75),
            ha='center', fontsize=8.4, color='#A8271F')
ax.annotate(r'$F = qvB\sin\theta$', (1.05,-1.55), ha='center', fontsize=9.6)
ax.set_title(r'(a) direction of $q\vec{v}\times\vec{B}$', fontsize=8.6)
ax.set_xlim(-1.5,2.9); ax.set_ylim(-2.0,2.4); ax.set_aspect('equal'); ax.axis('off')

ax = axs[1]
for x in np.linspace(-1.85,1.85,5):
    for y in np.linspace(-1.85,1.85,5):
        ax.plot([x],[y], marker='x', color=GRID, ms=5, mew=1.3, zorder=1)
R = 1.25
t = np.linspace(0, 2*np.pi, 300)
ax.plot(R*np.cos(t), R*np.sin(t), color=ACCENT, lw=1.8, ls=(0,(5,3)), zorder=3)
P = np.array([R*np.cos(np.radians(40)), R*np.sin(np.radians(40))])
ax.plot([P[0]],[P[1]],'o', color='#A8271F', ms=7, zorder=5)
ax.annotate('$+q$', P+np.array([0.12,0.14]), fontsize=9.0, color='#A8271F')
tan = np.array([-np.sin(np.radians(40)), np.cos(np.radians(40))])
ax.annotate('', xy=P+0.95*tan, xytext=P,
            arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.8, mutation_scale=12))
ax.annotate(r'$\vec{v}$', P+1.02*tan+np.array([0.06,0.10]), fontsize=10, color=ACCENT)
ax.annotate('', xy=(0,0), xytext=P,
            arrowprops=dict(arrowstyle='-|>', color='#A8271F', lw=1.6, mutation_scale=12))
ax.annotate(r'$\vec{F}$', (0.80,0.10), fontsize=10, color='#A8271F')
ax.plot([0,-R*np.cos(np.radians(20))],[0,R*np.sin(np.radians(140))],
        color=MUTED, lw=0.9, ls=':')
ax.annotate('$r$', (-0.76,0.62), fontsize=9.6, color=MUTED)
ax.annotate(r'$\vec{B}$ into the page', (0,-2.30), ha='center', fontsize=8.6, color=MUTED)
ax.set_title('(b) circular path', fontsize=8.6)
ax.set_xlim(-2.3,2.3); ax.set_ylim(-2.6,2.4); ax.set_aspect('equal'); ax.axis('off')
fig.tight_layout()
```
::: definition The tesla
The magnetic flux density is $1\ \text{tesla}$ if a charge of $1\ \text{coulomb}$
moving at $1\ \text{m s}^{-1}$ **at right angles** to the field experiences a
force of $1\ \text{newton}$.
:::

Three consequences follow straight from $F = qvB\sin\theta$:

- If $\vec{v}$ is **parallel** or antiparallel to $\vec{B}$ ($\theta = 0$ or
  $180^{\circ}$) the force is **zero** — the particle goes straight on.
- The force is greatest when $\vec{v} \perp \vec{B}$, and then $F = qvB$.
- $\vec{F}$ is always perpendicular to $\vec{v}$, so the magnetic force **does no
  work**. It can change the direction of motion but never the speed or the
  kinetic energy.

**Direction.** Use **Fleming's left-hand rule** for the force on a positive
charge (or a current): stretch the first three fingers of the *left* hand
mutually perpendicular — **Fore**finger = **Field**, **Cen**tre finger =
**Cur**rent, **Thu**mb = **Thrust**. For a negative charge, reverse the answer.

::: derivation Circular motion of a charge in a uniform field
If a charge enters at right angles to a uniform field, the force $qvB$ stays
perpendicular to $\vec{v}$ and constant in magnitude, so it acts as a centripetal
force and the path is a circle:

$$ qvB = \frac{mv^{2}}{r} \;\Longrightarrow\; \boxed{r = \frac{mv}{qB} = \frac{p}{qB}} $$

The period is the circumference divided by the speed:

$$ T = \frac{2\pi r}{v} = \frac{2\pi m}{qB}, \qquad
f = \frac{qB}{2\pi m} $$

Notice that $T$ and $f$ do **not** contain $v$: fast particles simply travel
round bigger circles in the same time. This is the principle of the cyclotron.
If the velocity has a component along $\vec{B}$ as well, that component is
unaffected and the path becomes a **helix** of pitch $p = v\cos\theta \cdot T$.
:::

::: example Worked example 16.1
**Problem.** A proton ($m = 1.67\times10^{-27}\ \text{kg}$,
$q = 1.6\times10^{-19}\ \text{C}$) enters a uniform magnetic field of
$0.50\ \text{T}$ at right angles with a speed of $2.0\times10^{6}\ \text{m s}^{-1}$.
Find the radius of its path, the period and the frequency of revolution.

**Solution.**
$$ r = \frac{mv}{qB} = \frac{(1.67\times10^{-27})(2.0\times10^{6})}
{(1.6\times10^{-19})(0.50)} = \frac{3.34\times10^{-21}}{8.0\times10^{-20}}
= 4.18\times10^{-2}\ \text{m} = 4.18\ \text{cm} $$

$$ T = \frac{2\pi m}{qB} = \frac{2\pi(1.67\times10^{-27})}{8.0\times10^{-20}}
= \frac{1.049\times10^{-26}}{8.0\times10^{-20}} = 1.31\times10^{-7}\ \text{s} $$

$$ f = \frac{1}{T} = 7.62\times10^{6}\ \text{Hz} = 7.62\ \text{MHz} $$
:::

### Force on a current-carrying conductor

A current is a stream of moving charges, so a wire in a magnetic field feels a
force.

::: derivation $F = BIL\sin\theta$ from $F = qvB\sin\theta$
Take a straight conductor of length $L$ and cross-sectional area $A$ containing
$n$ free electrons per unit volume, each of charge $q$, drifting with speed
$v_d$ at an angle $\theta$ to $\vec{B}$.

Force on **one** carrier: $f = q v_d B \sin\theta$.

Number of carriers in the length $L$: $N = nAL$.

Total force:
$$ F = (nAL)(qv_dB\sin\theta) = (nAqv_d)\,LB\sin\theta $$

But the current is $I = nAqv_d$, so

$$ \boxed{F = BIL\sin\theta}, \qquad \vec{F} = I\,\vec{L}\times\vec{B} $$

The force is maximum ($BIL$) when the conductor is perpendicular to the field and
zero when it lies along the field.
:::

```figure caption="Left: a conductor at angle $\theta$ to the field feels $F = BIL\sin\theta$, here directed into the page. Right: parallel currents in the same direction attract, with $F/L = \mu_0I_1I_2/2\pi d$."

import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle, Arc
fig, axs = plt.subplots(1, 2, figsize=(5.2,2.8))

ax = axs[0]
for y in np.linspace(-1.5,1.5,5):
    ax.annotate('', xy=(2.25,y), xytext=(-2.25,y),
                arrowprops=dict(arrowstyle='-|>', color=GRID, lw=1.3, mutation_scale=10))
ax.annotate(r'$\vec{B}$', (2.34,1.5), fontsize=10, color=MUTED, va='center')
th = np.radians(55); L = 1.55
P0 = np.array([-L*np.cos(th), -L*np.sin(th)]); P1 = -P0
ax.plot([P0[0],P1[0]],[P0[1],P1[1]], color=INK, lw=3.0,
        solid_capstyle='round', zorder=4)
ax.annotate('', xy=P1*0.62, xytext=P1*0.12,
            arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=2.0, mutation_scale=13))
ax.annotate('$I$', P1*0.52+np.array([0.24,-0.06]), fontsize=10, color=ACCENT)
ax.add_patch(Arc((0,0), 1.4, 1.4, theta1=0, theta2=55, color=MUTED, lw=1.0))
ax.annotate(r'$\theta$', (0.80,0.24), fontsize=10, color=MUTED)
C = P0*0.58
ax.add_patch(Circle(C, 0.20, fc='white', ec='#A8271F', lw=1.6, zorder=6))
ax.plot([C[0]],[C[1]], marker='x', color='#A8271F', ms=7, mew=1.8, zorder=7)
ax.annotate(r'$\vec{F}$ into page', (-1.55,-1.85), ha='center',
            fontsize=8.4, color='#A8271F')
ax.annotate('$L$', P1*0.85+np.array([-0.26,0.22]), fontsize=9.6, color=INK)
ax.set_title(r'(a) force on a conductor', fontsize=8.6)
ax.set_xlim(-2.7,2.9); ax.set_ylim(-2.3,2.2); ax.set_aspect('equal'); ax.axis('off')

ax = axs[1]
for x, lab in [(-0.85,'$I_1$'), (0.85,'$I_2$')]:
    ax.plot([x,x],[-1.9,1.9], color=INK, lw=2.4, zorder=3)
    ax.annotate('', xy=(x,1.55), xytext=(x,0.75),
                arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=2.0, mutation_scale=13))
    ax.annotate(lab, (x+0.14,1.62), fontsize=9.6, color=ACCENT)
ax.plot([0.85],[0.0], marker='x', color='#0B6A62', ms=8, mew=2.0, zorder=5)
ax.annotate('$B_1$ into page', (1.02,-0.06), fontsize=8.2, color='#0B6A62', va='center')
ax.annotate('', xy=(-0.30,-0.72), xytext=(-0.85,-0.72),
            arrowprops=dict(arrowstyle='-|>', color='#A8271F', lw=1.8, mutation_scale=12))
ax.annotate('', xy=(0.30,-0.72), xytext=(0.85,-0.72),
            arrowprops=dict(arrowstyle='-|>', color='#A8271F', lw=1.8, mutation_scale=12))
ax.annotate('$F$', (-0.58,-1.02), ha='center', fontsize=9.4, color='#A8271F')
ax.annotate('$F$', (0.58,-1.02), ha='center', fontsize=9.4, color='#A8271F')
ax.annotate('', xy=(0.85,-1.72), xytext=(-0.85,-1.72),
            arrowprops=dict(arrowstyle='<|-|>', color=MUTED, lw=1.1, mutation_scale=9))
ax.annotate('$d$', (0,-1.60), ha='center', fontsize=9.6, color=MUTED)
ax.set_title('(b) two parallel currents', fontsize=8.6)
ax.set_xlim(-2.3,2.5); ax.set_ylim(-2.3,2.2); ax.set_aspect('equal'); ax.axis('off')
fig.tight_layout()
```
::: example Worked example 16.2
**Problem.** A straight wire of length $20\ \text{cm}$ carries a current of
$5.0\ \text{A}$ and is placed in a uniform field of $0.40\ \text{T}$ so that it
makes $30^{\circ}$ with the field. Find the force on it, and the force if the
wire is turned perpendicular to the field.

**Solution.**
$$ F = BIL\sin\theta = (0.40)(5.0)(0.20)\sin 30^{\circ}
= (0.40)(5.0)(0.20)(0.50) = 0.20\ \text{N} $$

Turned perpendicular, $\sin\theta = 1$:
$$ F_{max} = BIL = (0.40)(5.0)(0.20) = 0.40\ \text{N} $$
:::

## 16.3 Force and Torque on rectangular coil; Moving coil galvanometer

Consider a rectangular coil of $N$ turns, length $l$ and breadth $b$, carrying a
current $I$ in a uniform field $\vec{B}$ parallel to the plane of the coil.

::: derivation Torque on a rectangular coil
The two sides of length $b$ lie **along** the field, so the forces on them are
zero or are equal, opposite and along the same line — they produce no turning
effect.

Each side of length $l$ is **perpendicular** to $\vec{B}$, so it carries a force

$$ F = NBIl $$

The two forces are equal and opposite but act along **different** lines: they
form a **couple**. If $\alpha$ is the angle between the plane of the coil and
$\vec{B}$, the perpendicular distance between the two lines of action is
$b\cos\alpha$, so

$$ \tau = F \times b\cos\alpha = NBIl\,b\cos\alpha = NBIA\cos\alpha $$

with $A = lb$ the area of the coil. Writing $\theta = 90^{\circ}-\alpha$ for the
angle between the **normal** to the coil and $\vec{B}$,

$$ \boxed{\tau = NBIA\sin\theta} $$

Defining the **magnetic dipole moment** of the coil as $m = NIA$ (unit
$\text{A m}^{2}$), this is simply $\tau = mB\sin\theta$.
:::

- $\tau$ is **maximum** $= NBIA$ when the plane of the coil contains $\vec{B}$
  ($\alpha = 0$, $\theta = 90^{\circ}$).
- $\tau$ is **zero** when the plane is perpendicular to $\vec{B}$
  ($\theta = 0$) — the coil is then in stable equilibrium.
- The result is independent of the *shape* of the coil: any plane coil of area
  $A$ gives $\tau = NBIA\sin\theta$.

```figure caption="Left: plan view of a coil whose plane makes angle $\alpha$ with $\vec{B}$; the two forces $NBIl$ form a couple of arm $b\cos\alpha$. Right: cross-section of a moving-coil galvanometer — the concave poles and the soft-iron core make the field radial."

import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle, Arc, Rectangle, Wedge
fig, axs = plt.subplots(1, 2, figsize=(5.2,3.0))

ax = axs[0]
for y in np.linspace(-1.2,1.2,5):
    ax.annotate('', xy=(2.05,y), xytext=(-2.05,y),
                arrowprops=dict(arrowstyle='-|>', color=GRID, lw=1.3, mutation_scale=10))
ax.annotate(r'$\vec{B}$', (2.14,1.2), fontsize=10, color=MUTED, va='center')
al = np.radians(35); h = 1.25
P = np.array([h*np.cos(al), h*np.sin(al)]); Q = -P
ax.plot([Q[0],P[0]],[Q[1],P[1]], color=INK, lw=2.4, zorder=4)
ax.add_patch(Circle(P, 0.17, fc='white', ec=INK, lw=1.4, zorder=5))
ax.plot([P[0]],[P[1]],'o', color=INK, ms=3.0, zorder=6)
ax.plot([Q[0]],[Q[1]], marker='x', color=INK, ms=8, mew=2.0, zorder=6)
ax.annotate('', xy=(P[0],P[1]+0.95), xytext=(P[0],P[1]+0.22),
            arrowprops=dict(arrowstyle='-|>', color='#A8271F', lw=1.8, mutation_scale=12))
ax.annotate('', xy=(Q[0],Q[1]-0.95), xytext=(Q[0],Q[1]-0.22),
            arrowprops=dict(arrowstyle='-|>', color='#A8271F', lw=1.8, mutation_scale=12))
ax.annotate('$NBIl$', (P[0]+0.16,P[1]+0.82), fontsize=8.8, color='#A8271F')
ax.annotate('$NBIl$', (Q[0]-0.16,Q[1]-0.92), ha='right', fontsize=8.8, color='#A8271F')
ax.plot([P[0],P[0]],[P[1],-2.10], color=MUTED, lw=0.9, ls=':')
ax.plot([Q[0],Q[0]],[Q[1],-2.10], color=MUTED, lw=0.9, ls=':')
ax.annotate('', xy=(P[0],-1.98), xytext=(Q[0],-1.98),
            arrowprops=dict(arrowstyle='<|-|>', color='#0B6A62', lw=1.1, mutation_scale=9))
ax.annotate(r'$b\cos\alpha$', (0,-2.46), ha='center', fontsize=9.0, color='#0B6A62')
ax.add_patch(Arc((0,0), 1.35, 1.35, theta1=0, theta2=35, color=MUTED, lw=1.0))
ax.annotate(r'$\alpha$', (0.80,0.16), fontsize=10, color=MUTED)
ax.set_title('(a) couple on a coil (plan view)', fontsize=8.6)
ax.set_xlim(-2.5,2.6); ax.set_ylim(-2.85,2.3); ax.set_aspect('equal'); ax.axis('off')

ax = axs[1]
ax.add_patch(Wedge((0,0), 2.35, 105, 255, width=0.85, fc='#dbe8f6',
                   ec=MUTED, lw=1.1, zorder=1))
ax.add_patch(Wedge((0,0), 2.35, -75, 75, width=0.85, fc='#f6d9d4',
                   ec=MUTED, lw=1.1, zorder=1))
ax.annotate('N', (-1.92,0), ha='center', va='center', fontsize=11,
            color=ACCENT, weight='bold')
ax.annotate('S', (1.92,0), ha='center', va='center', fontsize=11,
            color='#A8271F', weight='bold')
ax.add_patch(Circle((0,0), 0.78, fc='#e3e6ec', ec=INK, lw=1.2, zorder=3))
ax.annotate('soft iron\ncore', (0,0), ha='center', va='center',
            fontsize=7.6, color=INK, zorder=4)
for a_deg in (102, 130, 230, 258):
    a = np.radians(a_deg)
    ax.annotate('', xy=(0.86*np.cos(a), 0.86*np.sin(a)),
                xytext=(1.44*np.cos(a), 1.44*np.sin(a)),
                arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.1, mutation_scale=9))
for a_deg in (-78, -52, 52, 78):
    a = np.radians(a_deg)
    ax.annotate('', xy=(1.44*np.cos(a), 1.44*np.sin(a)),
                xytext=(0.86*np.cos(a), 0.86*np.sin(a)),
                arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.1, mutation_scale=9))
for a_deg, mk in ((180, 'o'), (0, 'x')):
    a = np.radians(a_deg); c = np.array([1.13*np.cos(a), 1.13*np.sin(a)])
    ax.add_patch(Rectangle((c[0]-0.17, c[1]-0.30), 0.34, 0.60, fc='white',
                           ec=INK, lw=1.3, zorder=5))
    if mk == 'o':
        ax.plot([c[0]],[c[1]],'o', color=INK, ms=4, zorder=6)
    else:
        ax.plot([c[0]],[c[1]], marker='x', color=INK, ms=7, mew=1.8, zorder=6)
ax.annotate('coil', (-1.13,0.56), ha='center', fontsize=8.0, color=INK)
ax.annotate('coil', (1.13,0.56), ha='center', fontsize=8.0, color=INK)
ax.annotate('radial field: plane of the coil\nis always parallel to $B$',
            (0,-2.60), ha='center', fontsize=8.0, color=MUTED)
ax.set_title('(b) moving-coil galvanometer', fontsize=8.6)
ax.set_xlim(-2.6,2.6); ax.set_ylim(-3.05,2.3); ax.set_aspect('equal'); ax.axis('off')
fig.tight_layout()
```
### Moving coil galvanometer

**Construction.** A rectangular coil of many turns of fine insulated copper wire
is wound on a light non-magnetic aluminium frame. It hangs by a thin
**phosphor-bronze suspension strip** between the **concave** pole pieces of a
strong permanent horseshoe magnet, with a cylindrical **soft-iron core** fixed
inside it (not touching). The suspension strip carries the current in and
provides the restoring couple; a fine spring below takes the current out. A small
mirror on the strip and a lamp-and-scale arrangement read the deflection.

**Why the field must be radial.** The concave pole faces plus the soft-iron core
make the field in the gap point everywhere along a radius of the cylinder. So
however far the coil turns, its plane always stays **parallel** to $\vec{B}$,
i.e. $\theta = 90^{\circ}$ and $\sin\theta = 1$ always.

::: derivation Why the galvanometer scale is linear
With a radial field the deflecting couple is $NBIA$ whatever the deflection. At
equilibrium it is balanced by the restoring couple $c\varphi$ of the suspension,
where $c$ is the torsional constant (couple per unit twist):

$$ NBIA = c\varphi \;\Longrightarrow\;
\boxed{\varphi = \left(\frac{NBA}{c}\right)I} $$

Since $N$, $B$, $A$ and $c$ are all constants, $\varphi \propto I$: the scale is
**uniform**. Without a radial field we would get $\varphi \propto I\sin\theta$
and a badly cramped scale.
:::

| Quantity | Definition | Expression |
|---|---|---|
| Current sensitivity | deflection per unit current | $\varphi/I = NBA/c$ |
| Voltage sensitivity | deflection per unit p.d. | $\varphi/V = NBA/cG$ |

To make a galvanometer more sensitive: increase $N$, $A$ and $B$, and decrease
$c$ (hence phosphor bronze, which has a very small torsional constant). The
soft-iron core does double duty — it makes the field radial *and* concentrates
the flux, increasing $B$.

::: caution High current sensitivity does not mean high voltage sensitivity
Doubling the number of turns $N$ doubles $NBA/c$, but it also roughly doubles the
coil resistance $G$, so the voltage sensitivity $NBA/cG$ hardly changes. An
instrument can be very sensitive to current and poor at detecting small p.d.s.
:::

::: example Worked example 16.3
**Problem.** A rectangular coil of $100$ turns and dimensions
$5.0\ \text{cm} \times 4.0\ \text{cm}$ carries a current of $2.0\ \text{A}$ in a
uniform field of $0.20\ \text{T}$. Find the torque when (a) the plane of the coil
is parallel to the field and (b) the plane makes $60^{\circ}$ with the field.

**Solution.** Area $A = 0.050 \times 0.040 = 2.0\times10^{-3}\ \text{m}^{2}$.

(a) Plane parallel to $\vec{B}$ means $\alpha = 0$, so $\cos\alpha = 1$:
$$ \tau = NBIA = (100)(0.20)(2.0)(2.0\times10^{-3}) = 0.080\ \text{N m} $$

(b) $\alpha = 60^{\circ}$, so $\cos 60^{\circ} = 0.50$:
$$ \tau = NBIA\cos\alpha = 0.080 \times 0.50 = 0.040\ \text{N m} $$
:::

## 16.4 Hall effect

::: definition Hall effect
When a current-carrying conductor is placed in a magnetic field perpendicular to
the current, a potential difference is set up across the conductor in the
direction perpendicular to **both** the current and the field. This transverse
p.d. is the **Hall voltage** $V_H$.
:::

::: derivation The Hall voltage
Let a slab of thickness $t$ (measured along $\vec{B}$) and width $w$ carry a
current $I$ of carriers of charge $q$, number density $n$ and drift speed $v_d$,
with $\vec{B}$ perpendicular to $I$.

**Step 1.** Each carrier feels a magnetic force $qv_dB$ pushing it sideways, so
charge piles up on one face and the opposite charge is left on the other.

**Step 2.** The separated charge sets up a transverse **Hall field** $E_H$.
Equilibrium is reached when the electric force balances the magnetic force:

$$ qE_H = qv_dB \;\Longrightarrow\; E_H = v_dB $$

**Step 3.** The Hall voltage across the width $w$ is

$$ V_H = E_H w = v_d B w $$

**Step 4.** From $I = nqv_dA = nqv_d(wt)$ we get $v_d = I/(nqwt)$, so

$$ \boxed{V_H = \frac{IB}{nqt}} $$

The **Hall coefficient** is defined as $R_H = 1/nq$, giving $V_H = R_H IB/t$.
:::

```figure caption="Left: the Biot–Savart geometry — the element $Id\vec{l}$, the distance $r$ to $P$ and the angle $\theta$ between them. Right: Hall effect — positive carriers are pushed to the upper face, making it positive; $t$ is measured along $\vec{B}$."

import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle, Arc, Polygon
fig, axs = plt.subplots(1, 2, figsize=(5.2,2.8))

ax = axs[0]
s = np.linspace(-1.35, 1.35, 200)
ax.plot(s, -0.9 + 0.42*s**2, color=INK, lw=2.2, zorder=3)
x0 = 0.25; y0 = -0.9 + 0.42*x0**2
tg = np.array([1.0, 0.84*x0]); tg = tg/np.hypot(*tg)
E0 = np.array([x0,y0]) - 0.20*tg; E1 = np.array([x0,y0]) + 0.20*tg
ax.plot([E0[0],E1[0]],[E0[1],E1[1]], color='#A8271F', lw=5.0,
        solid_capstyle='butt', zorder=5)
ax.annotate(r'$I\,d\vec{l}$', (x0-0.06, y0-0.46), ha='center',
            fontsize=9.6, color='#A8271F')
ax.annotate('', xy=(-0.62,-0.74), xytext=(-1.08,-0.41),
            arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.4, mutation_scale=11))
ax.annotate('$I$', (-1.22,-0.30), fontsize=9.6, color=INK)
P = np.array([1.35, 1.25])
ax.annotate('', xy=P, xytext=(x0,y0),
            arrowprops=dict(arrowstyle='-|>', color='#0B6A62', lw=1.5, mutation_scale=11))
ax.annotate('$r$', (0.58,0.38), fontsize=10, color='#0B6A62')
ax.plot([P[0]],[P[1]],'o', color=INK, ms=5, zorder=5)
ax.annotate('$P$', P+np.array([0.12,0.10]), fontsize=10, color=INK)
ax.plot([x0-0.30*tg[0], x0+1.35*tg[0]],[y0-0.30*tg[1], y0+1.35*tg[1]],
        color=MUTED, lw=0.9, ls=':')
ang_t = np.degrees(np.arctan2(tg[1], tg[0]))
ang_r = np.degrees(np.arctan2(P[1]-y0, P[0]-x0))
ax.add_patch(Arc((x0,y0), 1.90, 1.90, theta1=ang_t, theta2=ang_r,
                 color=MUTED, lw=1.0))
am = np.radians(0.5*(ang_t+ang_r))
ax.annotate(r'$\theta$', (x0+1.18*np.cos(am), y0+1.18*np.sin(am)),
            fontsize=10, color=MUTED)
ax.annotate(r'$dB = \dfrac{\mu_0}{4\pi}\dfrac{I\,dl\sin\theta}{r^2}$',
            (0.25,-2.00), ha='center', fontsize=9.4)
ax.set_title('(a) Biot' + u'–' + 'Savart law', fontsize=8.6)
ax.set_xlim(-1.7,2.3); ax.set_ylim(-2.45,1.9); ax.set_aspect('equal'); ax.axis('off')

ax = axs[1]
dx, dy = 0.62, 0.44
F = [(-1.6,-0.75), (1.6,-0.75), (1.6,0.75), (-1.6,0.75)]
ax.add_patch(Polygon([(F[3][0],F[3][1]), (F[2][0],F[2][1]),
                      (F[2][0]+dx,F[2][1]+dy), (F[3][0]+dx,F[3][1]+dy)],
                     closed=True, fc='#eef1f6', ec=MUTED, lw=1.0, zorder=1))
ax.add_patch(Polygon([(F[1][0],F[1][1]), (F[2][0],F[2][1]),
                      (F[2][0]+dx,F[2][1]+dy), (F[1][0]+dx,F[1][1]+dy)],
                     closed=True, fc='#e3e6ec', ec=MUTED, lw=1.0, zorder=1))
ax.add_patch(Polygon(F, closed=True, fc='white', ec=INK, lw=1.4, zorder=2))
for x in (-0.95, -0.35, 0.85):
    ax.plot([x],[-0.28], marker='x', color='#0B6A62', ms=7, mew=1.6, zorder=3)
ax.annotate(r'$\vec{B}$ into the slab', (1.35,1.45), ha='center',
            fontsize=8.2, color='#0B6A62')
ax.annotate('', xy=(1.95,0.10), xytext=(-1.40,0.10),
            arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.8, mutation_scale=12))
ax.annotate('$I$', (-1.34,0.24), fontsize=9.6, color=ACCENT)
for x in (-1.15, -0.35, 0.45, 1.15):
    ax.annotate('+', (x,0.50), ha='center', va='center', fontsize=11, color='#A8271F')
    ax.annotate(u'−', (x,-0.58), ha='center', va='center', fontsize=11, color=ACCENT)
ax.annotate('', xy=(0.15,-0.40), xytext=(0.15,0.36),
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.2, mutation_scale=10))
ax.annotate('$E_H$', (0.26,-0.06), fontsize=9.0, color=MUTED,
            bbox=dict(fc='white', ec='none', pad=1.0))
ax.annotate('', xy=(-1.85,0.75), xytext=(-1.85,-0.75),
            arrowprops=dict(arrowstyle='<|-|>', color=INK, lw=1.0, mutation_scale=8))
ax.annotate('$w$', (-2.00,0.0), ha='right', va='center', fontsize=9.4)
ax.annotate('', xy=(1.6+dx,-0.75+dy), xytext=(1.6,-0.75),
            arrowprops=dict(arrowstyle='<|-|>', color=INK, lw=1.0, mutation_scale=8))
ax.annotate('$t$', (2.10,-0.62), fontsize=9.4)
ax.annotate(r'$V_H = \dfrac{IB}{nqt}$', (0.0,-1.80), ha='center', fontsize=9.4)
ax.set_title('(b) Hall effect', fontsize=8.6)
ax.set_xlim(-2.9,2.9); ax.set_ylim(-2.35,1.9); ax.set_aspect('equal'); ax.axis('off')
fig.tight_layout()
```
**Uses of the Hall effect.**

- The **sign** of $V_H$ gives the **sign of the charge carriers** — this is how
  we know that conduction in an n-type semiconductor is by electrons and in a
  p-type by holes.
- From $R_H = 1/nq$ we get the **carrier concentration** $n$, and hence the drift
  velocity.
- A calibrated slab is a **Hall probe**, the standard instrument for measuring
  magnetic flux density.
- Hall sensors count the revolutions of motors and wheels and detect whether a
  phone's flip cover is closed.

::: example Worked example 16.4
**Problem.** A copper strip of thickness $0.50\ \text{mm}$ carries a current of
$10\ \text{A}$ in a magnetic field of $1.2\ \text{T}$ applied perpendicular to
its face. If copper has $n = 8.5\times10^{28}\ \text{m}^{-3}$ free electrons,
find the Hall voltage and the Hall coefficient.

**Solution.**
$$ nq = (8.5\times10^{28})(1.6\times10^{-19}) = 1.36\times10^{10}\ \text{C m}^{-3} $$

$$ V_H = \frac{IB}{nqt} = \frac{(10)(1.2)}
{(1.36\times10^{10})(0.50\times10^{-3})} = \frac{12}{6.8\times10^{6}}
= 1.76\times10^{-6}\ \text{V} = 1.76\ \mu\text{V} $$

$$ R_H = \frac{1}{nq} = \frac{1}{1.36\times10^{10}}
= 7.35\times10^{-11}\ \text{m}^{3}\text{C}^{-1} $$

The Hall voltage in a metal is tiny because $n$ is enormous. In a semiconductor
$n$ is about $10^{16}$ times smaller, so $V_H$ is millions of times larger —
which is why Hall probes are made of semiconductors.
:::

## 16.5 Magnetic field of a moving charge

A single charge $q$ moving with velocity $\vec{v}$ sets up a magnetic field at a
point $P$ whose position vector from the charge is $\vec{r}$:

$$ B = \frac{\mu_0}{4\pi}\,\frac{qv\sin\theta}{r^{2}}, \qquad
\vec{B} = \frac{\mu_0}{4\pi}\,\frac{q\,\vec{v}\times\hat{r}}{r^{2}} $$

where $\theta$ is the angle between $\vec{v}$ and $\vec{r}$, and

$$ \mu_0 = 4\pi\times10^{-7}\ \text{T m A}^{-1}, \qquad
\frac{\mu_0}{4\pi} = 10^{-7}\ \text{T m A}^{-1} $$

is the **permeability of free space**. Points to note:

- $B = 0$ along the line of motion ($\theta = 0$ or $180^{\circ}$) and is
  greatest in the plane through the charge perpendicular to $\vec{v}$.
- $\vec{B}$ is perpendicular to both $\vec{v}$ and $\vec{r}$; the lines are
  circles centred on the line of motion — the right-hand grip rule again.
- A stationary charge ($v = 0$) produces **no** magnetic field, only an electric
  one.

For example, an electron moving at $2.0\times10^{7}\ \text{m s}^{-1}$ produces,
at a point $1.0\ \text{nm}$ away at right angles to its motion,

$$ B = 10^{-7}\times\frac{(1.6\times10^{-19})(2.0\times10^{7})}
{(1.0\times10^{-9})^{2}} = \frac{3.2\times10^{-19}}{1.0\times10^{-18}}
= 0.32\ \text{T} $$

— an enormous field, which is why atomic-scale magnetism is so strong.

Adding up the fields of all the carriers in a short length $dl$ of wire, with
$I = nAqv_d$, converts this formula into the Biot–Savart law of the next section:
$q\vec{v} \rightarrow I\,d\vec{l}$.

## 16.6 Biot and Savart law and application to circular coil, long straight conductor, long solenoid

::: definition Biot–Savart law
The magnetic flux density $dB$ at a point $P$ due to a small element of length
$dl$ of a conductor carrying current $I$ is

$$ dB = \frac{\mu_0}{4\pi}\,\frac{I\,dl\sin\theta}{r^{2}} $$

where $r$ is the distance of $P$ from the element and $\theta$ is the angle
between the element and the line joining it to $P$. The direction of $d\vec{B}$
is that of $d\vec{l}\times\hat{r}$, i.e. perpendicular to the plane containing
the element and $P$.
:::

So $dB \propto I$, $dB \propto dl$, $dB \propto \sin\theta$ and
$dB \propto 1/r^{2}$. The total field is found by integrating over the whole
conductor.

### (a) Long straight conductor

Let $P$ be at perpendicular distance $a$ from a straight wire. Taking an element
at distance $l$ from the foot of the perpendicular and measuring the angle
$\phi$ from that perpendicular, integration gives the standard result

$$ B = \frac{\mu_0 I}{4\pi a}\left(\sin\phi_1 + \sin\phi_2\right) $$

where $\phi_1$ and $\phi_2$ are the angles subtended at $P$ by the two ends. For
an **infinitely long** wire $\phi_1 = \phi_2 = 90^{\circ}$, so

$$ \boxed{B = \frac{\mu_0 I}{2\pi a}} $$

and for a semi-infinite wire ending at the foot of the perpendicular,
$B = \mu_0 I/4\pi a$.

### (b) Circular coil — field at the centre

::: derivation Field at the centre of a circular coil
Take a circular coil of radius $a$ carrying current $I$. Every element $dl$ of
the coil is perpendicular to the radius drawn to the centre, so
$\theta = 90^{\circ}$ and $\sin\theta = 1$, and every element is the same
distance $a$ from the centre. Also, every element contributes $d\vec{B}$ in the
**same** direction — along the axis — so the magnitudes simply add:

$$ B = \oint dB = \frac{\mu_0}{4\pi}\frac{I}{a^{2}}\oint dl
= \frac{\mu_0}{4\pi}\frac{I}{a^{2}}(2\pi a) $$

$$ \boxed{B = \frac{\mu_0 I}{2a}} \qquad\text{and for } N \text{ turns } \;
B = \frac{\mu_0 N I}{2a} $$

At a point on the **axis** at distance $x$ from the centre the same integration
gives

$$ B = \frac{\mu_0 N I a^{2}}{2\left(a^{2}+x^{2}\right)^{3/2}} $$

which reduces to $\mu_0NI/2a$ at the centre ($x = 0$) and falls off as
$1/x^{3}$ far away.
:::

### (c) Long solenoid

For a solenoid with $n$ turns per unit length, integrating the on-axis coil
formula over all the turns gives, at an axial point,

$$ B = \tfrac{1}{2}\mu_0 n I\left(\sin\alpha_1 + \sin\alpha_2\right) $$

where $\alpha_1$ and $\alpha_2$ are the semi-angles subtended by the two ends.
Two limits matter:

| Position | Angles | Field |
|---|---|---|
| Middle of a very long solenoid | $\alpha_1 = \alpha_2 = 90^{\circ}$ | $B = \mu_0 n I$ |
| At one **end** of a long solenoid | $\alpha_1 = 0$, $\alpha_2 = 90^{\circ}$ | $B = \frac{1}{2}\mu_0 n I$ |

```figure caption="Field lines computed from the currents themselves. Left: a circular coil seen edge-on, the field through the centre is $\mu_0I/2a$. Right: a solenoid — the field inside is uniform and the rectangle $abcd$ is the Amperian loop of §16.7."

import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle
fig, axs = plt.subplots(1, 2, figsize=(5.2,2.9))
BOX = dict(fc='white', ec='none', pad=1.2)

def mark(ax, x, y, s, R=0.13):
    ax.add_patch(Circle((x,y), R, fc='white', ec=INK, lw=1.2, zorder=8))
    if s > 0:
        ax.plot([x],[y],'o', color=INK, ms=2.8, zorder=9)
    else:
        ax.plot([x],[y], marker='x', color=INK, ms=5, mew=1.5, zorder=9)

def arrow(ax, p, d, col=ACCENT, lw=1.2):
    d = np.asarray(d, float); d = d/np.hypot(*d)
    ax.annotate('', xy=(p[0]+0.06*d[0], p[1]+0.06*d[1]), xytext=(p[0], p[1]),
                arrowprops=dict(arrowstyle='-|>', color=col, lw=lw, mutation_scale=11),
                zorder=7)

# ---- (a) circular coil seen edge-on -------------------------------------
# the field lines of two antiparallel line currents are circles centred on the axis
ax = axs[0]
t = np.linspace(0, 2*np.pi, 400)
for m, adeg in ((1.18,-90), (1.55,-112), (2.4,-132), (4.0,-148)):
    R = np.sqrt(m*m - 1.0)
    for sgn in (1, -1):
        yc = sgn*m
        ax.plot(R*np.cos(t), yc + R*np.sin(t), color=ACCENT, lw=1.0, zorder=3)
        k = np.radians(adeg if sgn > 0 else -adeg)
        p = (R*np.cos(k), yc + R*np.sin(k))
        # out of page at the top: anticlockwise; into the page below: clockwise
        d = (-np.sin(k), np.cos(k)) if sgn > 0 else (np.sin(k), -np.cos(k))
        arrow(ax, p, d)
ax.plot([-2.55, 2.55], [0, 0], color=ACCENT, lw=1.0, zorder=3)
arrow(ax, (-2.10, 0), (1, 0)); arrow(ax, (2.10, 0), (1, 0))
mark(ax, 0.0, 1.0, +1); mark(ax, 0.0, -1.0, -1)
ax.annotate('', xy=(1.55,0), xytext=(0.32,0),
            arrowprops=dict(arrowstyle='-|>', color='#A8271F', lw=1.8, mutation_scale=12))
ax.annotate('axis', (1.05,0.14), ha='center', fontsize=8.4, color='#A8271F', bbox=BOX)
ax.annotate('coil seen\nedge-on,\nradius $a$', xy=(0.16,1.08), xytext=(1.45,1.62),
            fontsize=8.0, color=INK, ha='center', va='center', bbox=BOX, zorder=10,
            arrowprops=dict(arrowstyle='->', color=INK, lw=0.9))
ax.set_title('(a) circular coil, seen edge-on', fontsize=8.6)
ax.set_xlim(-2.6,2.6); ax.set_ylim(-2.3,2.3); ax.set_aspect('equal'); ax.axis('off')

# ---- (b) solenoid --------------------------------------------------------
ax = axs[1]
xs = np.linspace(-1.70, 1.70, 7)
for xi in xs:
    mark(ax, xi, 0.66, +1, R=0.105)
    mark(ax, xi, -0.66, -1, R=0.105)
for yin, yout, a, xin in ((0.36, 1.18, 2.30, -0.60), (0.18, 1.75, 2.75, 0.10),
                          (0.05, 2.35, 3.15, 0.75)):
    yc = 0.5*(yin + yout); b = 0.5*(yout - yin)
    for sgn in (1, -1):
        ax.plot(a*np.cos(t), sgn*(yc + b*np.sin(t)), color=ACCENT, lw=1.0, zorder=3)
        arrow(ax, (0.30, sgn*yout), (-1, 0))
    arrow(ax, (xin, yin), (1, 0))
ax.plot([-3.0, 3.0], [0, 0], color=ACCENT, lw=1.0, zorder=3)
arrow(ax, (-2.35, 0), (1, 0)); arrow(ax, (2.35, 0), (1, 0))
arrow(ax, (-0.45, 0), (1, 0))
ax.plot([-1.05,0.95,0.95,-1.05,-1.05], [-0.30,-0.30,1.10,1.10,-0.30],
        color='#A8271F', lw=1.4, ls=(0,(4,2.5)), zorder=10)
for px, py, lab, off in [(-1.05,-0.30,'$a$',(-12,-1)), (0.95,-0.30,'$b$',(12,-1)),
                         (0.95,1.10,'$c$',(12,2)), (-1.05,1.10,'$d$',(-12,2))]:
    ax.annotate(lab, (px,py), textcoords='offset points', xytext=off,
                fontsize=9.4, color='#A8271F', ha='center', va='center',
                bbox=BOX, zorder=11)
ax.annotate('', xy=(0.95,-1.30), xytext=(-1.05,-1.30),
            arrowprops=dict(arrowstyle='<|-|>', color='#A8271F', lw=1.0, mutation_scale=8))
ax.annotate('$L$', (-0.05,-1.30), ha='center', va='center', fontsize=9.4,
            color='#A8271F', bbox=BOX, zorder=11)
ax.set_title('(b) solenoid', fontsize=8.6)
ax.set_xlim(-3.3,3.3); ax.set_ylim(-2.9,2.9); ax.set_aspect('equal'); ax.axis('off')
fig.tight_layout()
```
::: example Worked example 16.5
**Problem.** (a) A circular coil of $50$ turns and radius $10\ \text{cm}$ carries
a current of $2.0\ \text{A}$. Find the flux density at its centre.
(b) A long straight wire carries $10\ \text{A}$. Find the flux density at a point
$5.0\ \text{cm}$ from it.

**Solution.**

(a) $$ B = \frac{\mu_0 NI}{2a} = \frac{(4\pi\times10^{-7})(50)(2.0)}{2(0.10)}
= \frac{1.2566\times10^{-4}}{0.20} = 6.28\times10^{-4}\ \text{T} $$

(b) $$ B = \frac{\mu_0 I}{2\pi a} = \frac{(2\times10^{-7})(10)}{0.050}
= \frac{2.0\times10^{-6}}{0.050} = 4.0\times10^{-5}\ \text{T} $$

(Using $\mu_0/2\pi = 2\times10^{-7}$ saves a line of arithmetic every time.)
:::

::: caution $2\pi a$ or $2a$?
$B = \mu_0 I/2\pi a$ is the field of a **straight** wire at distance $a$;
$B = \mu_0 I/2a$ is the field at the **centre of a circular coil** of radius $a$.
They differ by a factor of $\pi$. Check which geometry the question describes
before you write the formula.
:::

## 16.7 Ampere's law and applications to long straight conductor, straight solenoid, toroidal solenoid

::: definition Ampère's circuital law
The line integral of $\vec{B}$ around any **closed** path (an *Amperian loop*)
equals $\mu_0$ times the **net current** threading that path:

$$ \oint \vec{B}\cdot d\vec{l} = \mu_0 I_{enc} $$

Currents are counted positive if they are related to the sense of travel round
the loop by the right-hand rule.
:::

Ampère's law is to magnetism what Gauss's law is to electrostatics: always true,
but only *useful* where the symmetry lets you take $B$ outside the integral.

### (a) Long straight conductor

Choose a circle of radius $r$ centred on the wire, in the plane perpendicular to
it. By symmetry $B$ has the same magnitude everywhere on it and is everywhere
tangential, so $\vec{B}\cdot d\vec{l} = B\,dl$:

$$ \oint \vec{B}\cdot d\vec{l} = B\oint dl = B(2\pi r) = \mu_0 I
\;\Longrightarrow\; \boxed{B = \frac{\mu_0 I}{2\pi r}} $$

in two lines, where Biot–Savart needed an integration. **Inside** a solid
cylindrical conductor of radius $R$ carrying a uniform current, the loop of
radius $r < R$ encloses only the fraction $I r^{2}/R^{2}$, giving

$$ B = \frac{\mu_0 I r}{2\pi R^{2}} \qquad (r < R) $$

so $B$ rises linearly from zero on the axis to $\mu_0I/2\pi R$ at the surface,
then falls as $1/r$ outside.

### (b) Straight solenoid

::: derivation $B = \mu_0 n I$ inside a long solenoid
Take the rectangular Amperian loop $abcd$ of figure 5(b), with side $ab = L$ lying
along the axis inside the solenoid and side $cd$ well outside it. Split the
integral into four parts:

- along $ab$ (inside, $\vec{B}$ parallel to $d\vec{l}$): contributes $BL$;
- along $bc$ and $da$: $\vec{B}$ is perpendicular to $d\vec{l}$ where the path
  is inside, and $B \approx 0$ outside, so each contributes **zero**;
- along $cd$ (outside a long solenoid, where $B \approx 0$): contributes
  **zero**.

So $\oint \vec{B}\cdot d\vec{l} = BL$. The number of turns threading the loop is
$nL$, each carrying $I$, so $I_{enc} = nLI$ and

$$ BL = \mu_0 n L I \;\Longrightarrow\; \boxed{B = \mu_0 n I} $$

The result contains neither $L$ nor the position of the loop inside the
solenoid: **the field inside a long solenoid is uniform** and depends only on the
turns per unit length and the current.
:::

### (c) Toroidal solenoid

A toroid is a solenoid bent into a ring of $N$ turns. Take a circular Amperian
loop of radius $r$ running along the middle of the core. By symmetry $B$ is
constant and tangential along it, and the loop is threaded by all $N$ turns:

$$ B(2\pi r) = \mu_0 N I \;\Longrightarrow\;
\boxed{B = \frac{\mu_0 N I}{2\pi r}} $$

Writing $n = N/2\pi r$ for the turns per unit length along the core recovers
$B = \mu_0 n I$. For a loop drawn **inside the hole** or **outside the toroid**,
the enclosed current is zero, so $B = 0$ there: a toroid confines its field
completely inside the windings — which is why transformer and inductor cores are
toroidal.

::: example Worked example 16.6
**Problem.** A solenoid $50\ \text{cm}$ long has $500$ turns and carries
$3.0\ \text{A}$. Find the flux density (a) at its centre and (b) at one end.
(c) The same wire is wound into a toroid of mean radius $15\ \text{cm}$ with
$500$ turns and the same current; find the flux density along the mean circle.

**Solution.** Turns per unit length $n = 500/0.50 = 1000\ \text{m}^{-1}$.

(a) $$ B = \mu_0 nI = (4\pi\times10^{-7})(1000)(3.0) = 3.77\times10^{-3}\ \text{T} $$

(b) At the end the field is half that value:
$B = 1.88\times10^{-3}\ \text{T}$.

(c) $$ B = \frac{\mu_0 NI}{2\pi r} = \frac{(2\times10^{-7})(500)(3.0)}{0.15}
= \frac{3.0\times10^{-4}}{0.15} = 2.0\times10^{-3}\ \text{T} $$
:::

## 16.8 Force between two parallel conductors carrying current; definition of ampere

Two long parallel wires a distance $d$ apart carry currents $I_1$ and $I_2$.

::: derivation Force per unit length between parallel currents
Wire 1 produces at the position of wire 2 a field

$$ B_1 = \frac{\mu_0 I_1}{2\pi d} $$

which is perpendicular to wire 2. A length $L$ of wire 2 therefore feels

$$ F = B_1 I_2 L = \frac{\mu_0 I_1 I_2 L}{2\pi d}
\;\Longrightarrow\; \boxed{\frac{F}{L} = \frac{\mu_0 I_1 I_2}{2\pi d}} $$

By Newton's third law wire 1 feels an equal and opposite force. Applying
Fleming's left-hand rule shows that

- **currents in the same direction attract**, and
- **currents in opposite directions repel**
:::

::: memory Like currents attract — the opposite of charges
Two *like charges* repel, but two *like currents* attract. Students mix these up
constantly. Remember it as: parallel wires pull together, anti-parallel wires
push apart.
:::

::: definition The ampere
One **ampere** is that steady current which, when maintained in each of two
infinitely long straight parallel conductors of negligible circular
cross-section placed $1\ \text{metre}$ apart in vacuum, produces a force of
$2\times10^{-7}\ \text{newton}$ per metre of length between them.
:::

Check it: with $I_1 = I_2 = 1\ \text{A}$ and $d = 1\ \text{m}$,

$$ \frac{F}{L} = \frac{(4\pi\times10^{-7})(1)(1)}{2\pi(1)}
= 2\times10^{-7}\ \text{N m}^{-1} $$

> **A modern footnote.** Since 20 May 2019 the ampere has been defined instead by
> fixing the elementary charge at $e = 1.602176634\times10^{-19}\ \text{C}$, so
> that $1\ \text{A}$ is the current corresponding to $1/e$ elementary charges per
> second. As a result $\mu_0$ is now a *measured* quantity, though it still
> equals $4\pi\times10^{-7}\ \text{T m A}^{-1}$ to within a few parts in $10^{10}$.
> NEB papers still ask for the force-based definition above.

::: example Worked example 16.7
**Problem.** Two long parallel wires $10\ \text{cm}$ apart carry currents of
$5.0\ \text{A}$ and $10\ \text{A}$ in the same direction. Find the force per
metre between them, and the total force on a $2.0\ \text{m}$ length. State
whether it is attractive or repulsive. Where on the line joining them is the
resultant field zero?

**Solution.**
$$ \frac{F}{L} = \frac{\mu_0 I_1 I_2}{2\pi d}
= \frac{(2\times10^{-7})(5.0)(10)}{0.10}
= \frac{1.0\times10^{-5}}{0.10} = 1.0\times10^{-4}\ \text{N m}^{-1} $$

On $2.0\ \text{m}$: $F = 2.0\times10^{-4}\ \text{N}$, **attractive**, because the
currents are in the same direction.

Between the wires the two fields oppose. At a distance $x$ from the $5\ \text{A}$
wire,
$$ \frac{\mu_0(5.0)}{2\pi x} = \frac{\mu_0(10)}{2\pi(0.10-x)}
\;\Rightarrow\; 5(0.10-x) = 10x \;\Rightarrow\; 0.50 = 15x $$
so $x = 0.0333\ \text{m} = 3.33\ \text{cm}$ from the $5\ \text{A}$ wire.
:::

## Chapter summary

- Magnetic flux $\Phi = BA\cos\theta$ (weber); field lines are closed loops, so
  $\oint\vec{B}\cdot d\vec{A} = 0$ — there are no magnetic monopoles.
- Oersted: a current produces a magnetic field. Direction by the right-hand grip
  rule (or SNOW).
- Force on a moving charge $\vec{F} = q\vec{v}\times\vec{B}$, $F = qvB\sin\theta$;
  it does no work. Perpendicular entry gives a circle with $r = mv/qB$,
  $T = 2\pi m/qB$, independent of speed.
- Force on a conductor $F = BIL\sin\theta$; direction by Fleming's left-hand rule.
- Torque on a coil $\tau = NBIA\sin\theta = NBIA\cos\alpha$, with dipole moment
  $m = NIA$. A radial field makes $\sin\theta = 1$, so a moving-coil galvanometer
  has $\varphi = (NBA/c)I$ and a uniform scale.
- Hall effect: $V_H = IB/nqt$ with $R_H = 1/nq$; it gives the sign and the
  concentration of the carriers.
- Biot–Savart: $dB = (\mu_0/4\pi)(I\,dl\sin\theta/r^{2})$. Results:
  straight wire $\mu_0I/2\pi a$; centre of a coil $\mu_0NI/2a$; on the axis
  $\mu_0NIa^{2}/2(a^{2}+x^{2})^{3/2}$; long solenoid $\mu_0nI$ (half that at an
  end).
- Ampère: $\oint\vec{B}\cdot d\vec{l} = \mu_0I_{enc}$, which gives the straight
  wire, the solenoid ($\mu_0nI$) and the toroid ($\mu_0NI/2\pi r$, zero outside)
  in a few lines each.
- Parallel wires: $F/L = \mu_0I_1I_2/2\pi d$; like currents attract. This force
  defines the ampere as $2\times10^{-7}\ \text{N m}^{-1}$ for $1\ \text{A}$ at
  $1\ \text{m}$.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The SI unit of magnetic flux is <span class="marks">[1]</span>
   (a) tesla (b) weber (c) henry (d) ampere-metre
2. A charged particle moves parallel to a uniform magnetic field. The magnetic force on it is <span class="marks">[1]</span>
   (a) $qvB$ (b) zero (c) $qvB\sin 45^{\circ}$ (d) maximum
3. A charged particle enters a uniform magnetic field at right angles to it. Its path is <span class="marks">[1]</span>
   (a) a straight line (b) a parabola (c) a circle (d) a helix
4. The magnetic flux density at the centre of a circular coil of $N$ turns and radius $a$ carrying a current $I$ is <span class="marks">[1]</span>
   (a) $\mu_0NI/2\pi a$ (b) $\mu_0NI/2a$ (c) $\mu_0NI/4\pi a$ (d) $\mu_0NIa$
5. Two long parallel wires carry currents in the same direction. They <span class="marks">[1]</span>
   (a) attract each other (b) repel each other (c) exert no force (d) rotate about each other
6. The magnetic flux density inside a very long solenoid of $n$ turns per metre carrying current $I$ is <span class="marks">[1]</span>
   (a) $\mu_0nI/2$ (b) $\mu_0nI$ (c) $\mu_0nI/2\pi$ (d) zero
7. The field of a moving-coil galvanometer is made radial so that <span class="marks">[1]</span>
   (a) the coil does not rotate (b) the deflection is proportional to the current
   (c) the coil resistance is reduced (d) the torque is zero
8. The Hall voltage of a slab of thickness $t$ is proportional to <span class="marks">[1]</span>
   (a) $t$ (b) $1/t$ (c) $t^{2}$ (d) $\sqrt{t}$

::: note Answers to Group A
**1.** (b) — $\Phi = BA\cos\theta$, measured in weber $=$ T m².
**2.** (b) — $\sin 0^{\circ} = 0$, so $F = qvB\sin\theta = 0$.
**3.** (c) — the force stays perpendicular to $v$ and constant, so it is centripetal.
**4.** (b) — $B = \mu_0NI/2a$; the $2\pi$ form belongs to a straight wire.
**5.** (a) — like currents attract.
**6.** (b) — Ampère's law on a rectangular loop gives $B = \mu_0nI$.
**7.** (b) — with $\sin\theta = 1$ always, $\varphi = (NBA/c)I$, a uniform scale.
**8.** (b) — $V_H = IB/nqt$.
:::

**Group B — Short answer (5 marks each)**

1. Define magnetic flux and state its SI unit. Describe Oersted's experiment and
   state the conclusion drawn from it. <span class="marks">[5]</span>
2. Starting from the force on a single moving charge, derive the expression
   $F = BIL\sin\theta$ for the force on a current-carrying conductor in a
   magnetic field. <span class="marks">[5]</span>
3. An electron ($m = 9.1\times10^{-31}\ \text{kg}$, $e = 1.6\times10^{-19}\ \text{C}$)
   moves at $3.0\times10^{7}\ \text{m s}^{-1}$ at right angles to a magnetic field
   of $0.20\ \text{T}$. Find the radius of its path and its period of
   revolution. <span class="marks">[5]</span>
4. State the Biot–Savart law and use it to find the magnetic flux density at the
   centre of a circular coil of $N$ turns and radius $a$ carrying current
   $I$. <span class="marks">[5]</span>
5. Explain the Hall effect and show that $V_H = IB/nqt$. A metal strip of
   thickness $1.0\ \text{mm}$ with $n = 5.0\times10^{28}\ \text{m}^{-3}$ carries
   $20\ \text{A}$ in a field of $1.5\ \text{T}$; find the Hall
   voltage. <span class="marks">[5]</span>
6. Two long parallel wires $20\ \text{cm}$ apart carry currents of $10\ \text{A}$
   and $15\ \text{A}$ in **opposite** directions. Find the force per metre between
   them and state its nature. Hence define the ampere. <span class="marks">[5]</span>

::: note Answers to Group B
**3.** $$ r = \frac{mv}{eB} = \frac{(9.1\times10^{-31})(3.0\times10^{7})}
{(1.6\times10^{-19})(0.20)} = \frac{2.73\times10^{-23}}{3.2\times10^{-20}}
= 8.53\times10^{-4}\ \text{m} = 0.853\ \text{mm} $$
$$ T = \frac{2\pi m}{eB} = \frac{2\pi(9.1\times10^{-31})}{3.2\times10^{-20}}
= 1.79\times10^{-10}\ \text{s} $$

**5.** Derivation as in §16.4. Numerically,
$nq = (5.0\times10^{28})(1.6\times10^{-19}) = 8.0\times10^{9}$, so
$$ V_H = \frac{IB}{nqt} = \frac{(20)(1.5)}{(8.0\times10^{9})(1.0\times10^{-3})}
= \frac{30}{8.0\times10^{6}} = 3.75\times10^{-6}\ \text{V} = 3.75\ \mu\text{V} $$

**6.** $$ \frac{F}{L} = \frac{\mu_0I_1I_2}{2\pi d}
= \frac{(2\times10^{-7})(10)(15)}{0.20} = \frac{3.0\times10^{-5}}{0.20}
= 1.5\times10^{-4}\ \text{N m}^{-1} $$
The currents are opposite, so the force is **repulsive**. Definition of the
ampere: see §16.8.
:::

**Group C — Long answer (8 marks each)**

1. (a) State the Biot–Savart law and use it to derive the magnetic flux density
   at a perpendicular distance $a$ from a long straight conductor carrying a
   current $I$. <span class="marks">[5]</span>
   (b) A long straight wire carries $20\ \text{A}$. Find the flux density
   $10\ \text{cm}$ from it. A circular coil of $100$ turns and radius
   $10\ \text{cm}$ carries $2.0\ \text{A}$; find the flux density at its
   centre. <span class="marks">[3]</span>
2. (a) Derive an expression for the torque on a rectangular coil carrying a
   current in a uniform magnetic field. Explain, with a diagram, why the field of
   a moving-coil galvanometer is made radial and show that its scale is
   uniform. <span class="marks">[5]</span>
   (b) A galvanometer coil of $200$ turns and area $2.0\times10^{-4}\ \text{m}^{2}$
   hangs in a radial field of $0.20\ \text{T}$. The torsional constant of the
   suspension is $1.0\times10^{-6}\ \text{N m}$ per degree. Find the deflection
   produced by $5.0\ \text{mA}$ and the current
   sensitivity. <span class="marks">[3]</span>
3. (a) State Ampère's circuital law and apply it to find the magnetic flux
   density inside a long straight solenoid and inside a toroidal
   solenoid. <span class="marks">[5]</span>
   (b) A toroid of mean radius $15\ \text{cm}$ has $500$ turns and carries
   $3.0\ \text{A}$. Find the flux density along its mean circle and the flux
   density outside the toroid. <span class="marks">[3]</span>

::: note Answers to Group C
**1.** (b) Straight wire:
$$ B = \frac{\mu_0 I}{2\pi a} = \frac{(2\times10^{-7})(20)}{0.10}
= 4.0\times10^{-5}\ \text{T} $$
Circular coil:
$$ B = \frac{\mu_0 NI}{2a} = \frac{(4\pi\times10^{-7})(100)(2.0)}{2(0.10)}
= \frac{2.513\times10^{-4}}{0.20} = 1.26\times10^{-3}\ \text{T} $$

**2.** (b) $$ \tau = NBIA = (200)(0.20)(5.0\times10^{-3})(2.0\times10^{-4})
= 4.0\times10^{-5}\ \text{N m} $$
$$ \varphi = \frac{\tau}{c} = \frac{4.0\times10^{-5}}{1.0\times10^{-6}}
= 40\ \text{degrees} $$
Current sensitivity $= \dfrac{NBA}{c}
= \dfrac{(200)(0.20)(2.0\times10^{-4})}{1.0\times10^{-6}}
= 8.0\times10^{3}$ degrees per ampere, i.e. $8$ degrees per milliampere.

**3.** (b) $$ B = \frac{\mu_0 NI}{2\pi r} = \frac{(2\times10^{-7})(500)(3.0)}{0.15}
= \frac{3.0\times10^{-4}}{0.15} = 2.0\times10^{-3}\ \text{T} $$
Outside the toroid (and in the central hole) the Amperian loop encloses no net
current, so $B = 0$.
:::
