---
subject: Physics
grade: CEE
unit: 15
title: Magnetic Field and Magnetic Properties of Materials
hours: 3
area: Current Electricity and Magnetism
---

This chapter is the magnetic half of Current Electricity and Magnetism, an area that
carries **9 of the 50 Physics questions** (official MEC weightage). We estimate that
**3** of them come from here. The questions are short and formula-shaped: a field at a
point near a wire or on the axis of a coil, the radius of a charged particle's circle,
a torque on a coil, a Hall voltage, or one fact about domains and hysteresis. Most lost
marks come from two habits — using the centre-of-coil formula on the axis, and
forgetting that parallel currents **attract**.

::: key What the paper asks from this chapter
- $B=\mu_0I/2\pi r$ near a long straight wire; $B=\mu_0NI/2R$ at the centre of a coil;
  $B=\mu_0NIR^2/2(R^2+x^2)^{3/2}$ on its axis; $B=\mu_0nI$ inside a long solenoid and
  $B/2$ at its ends.
- Parallel currents attract, antiparallel currents repel; $F/L=\mu_0I_1I_2/2\pi d$.
- $F=qvB\sin\theta$ is always perpendicular to $\vec v$, so it does no work; $r=mv/qB$;
  $T=2\pi m/qB$ is independent of speed; a component of $\vec v$ along $\vec B$ turns the
  circle into a helix.
- $F=BIL\sin\theta$; $\tau=NIAB\sin\theta=MB\sin\theta$; the moving-coil galvanometer
  and why its field is radial.
- Hall voltage $V_H=BI/net$; its **sign** gives the sign of the charge carriers.
- $\mu_r=1+\chi$; dia-, para- and ferromagnetism; domains; Curie's law and the Curie
  point.
- Hysteresis: retentivity, coercivity, and loop area $=$ energy lost per cycle per unit
  volume. Soft iron for cores, steel for permanent magnets.
:::

## 15.1 Magnetic field of a straight conductor, a circular coil and a long solenoid

### 15.1.1 The magnetic field and its field lines

A **magnetic field** is a region in which a moving charge or a current-carrying
conductor experiences a force. It is a vector $\vec B$, called the **magnetic flux
density** (or simply the magnetic field), measured in **tesla** (T):
1 T $=$ 1 N A⁻¹ m⁻¹ $=$ 1 Wb m⁻². For scale, the Earth's field is about
$5\times10^{-5}$ T, a strong laboratory electromagnet about 1 T.

Magnetic field lines:

- are **closed loops** — they have no start and no end, because there are no magnetic
  monopoles;
- never cross (the field has one direction at each point);
- are drawn closer together where the field is stronger;
- run from the north pole to the south pole **outside** a magnet, and from south to
  north **inside** it.

The direction of $\vec B$ at any point is the direction in which the north pole of a
small compass needle points there.

**Right-hand grip rule for a wire.** Grasp the wire with the right hand, thumb along
the current; the curled fingers give the direction of the field circles. Reversing the
current reverses the field.

### 15.1.2 The long straight wire

For a long straight wire carrying current $I$, the field at perpendicular distance $r$
from the wire has magnitude

$$ B=\frac{\mu_0 I}{2\pi r} $$

where $\mu_0=4\pi\times10^{-7}\ \text{T m A}^{-1}$ is the **permeability of free
space**. The field lines are concentric circles around the wire, in the plane
perpendicular to it.

The formula follows from Ampère's circuital law, $\oint \vec B\cdot d\vec l=\mu_0I$:
take a circular path of radius $r$ round the wire. By symmetry $B$ is the same all
along it and parallel to $d\vec l$, so $B(2\pi r)=\mu_0I$.

Two proportionalities carry most of the marks: $B\propto I$ and $B\propto 1/r$. Double
the current and the field doubles; double the distance and it halves.

::: caution The field of a wire is not the field of a point charge
The $1/r$ fall-off is not the $1/r^2$ of Coulomb's law. A wire is an extended source,
and the contributions of its elements add to a $1/r$ field. Using $1/r^2$ is the single
commonest error in this section.
:::

**Force between two parallel wires.** Wire 1 makes a field $B_1=\mu_0I_1/2\pi d$ at
wire 2. The force on a length $L$ of wire 2 is $F=B_1I_2L$, so

$$ \frac{F}{L}=\frac{\mu_0I_1I_2}{2\pi d} $$

The direction is the surprise: currents in the **same** direction **attract**;
currents in opposite directions **repel**. This is the opposite of the rule for
electric charges, and it is a favourite distractor.

Why? Take two parallel wires with current in the same direction. The field of wire 1
at wire 2 points perpendicular to both the wire and the line joining them; the force
$\vec F=I_2\vec L\times\vec B_1$ then points towards wire 1. Reverse either current and
the force reverses.

::: example Worked example 15.1 — a wire and a pair of wires
**Problem.** Two long parallel wires 20 cm apart carry 5 A and 8 A in the same
direction. (a) Find the field produced by the 5 A wire at the position of the other.
(b) Find the force per metre between them.

**Solution.** (a) $B=\dfrac{\mu_0I}{2\pi r}=\dfrac{(4\pi\times10^{-7})(5)}{2\pi(0.20)}
=5.0\times10^{-6}\ \text{T}$.

(b) $\dfrac{F}{L}=BI_2=(5.0\times10^{-6})(8)=4.0\times10^{-5}\ \text{N m}^{-1}$,
attractive because the currents are in the same direction.
:::

### 15.1.3 The circular coil

At the **centre** of a circular coil of $N$ turns, radius $R$, carrying current $I$,

$$ B=\frac{\mu_0NI}{2R} $$

Each element $d\vec l$ of the coil is at the same distance $R$ from the centre and its
field there points along the axis, so the contributions simply add: the field of one
turn is $\mu_0I/2R$, and $N$ turns give $N$ times as much.

On the **axis**, at distance $x$ from the centre,

$$ B=\frac{\mu_0NIR^2}{2(R^2+x^2)^{3/2}} $$

Setting $x=0$ recovers the centre value. Two limits are worth memorising:

| Position on the axis | Field | As a fraction of the centre field |
|---|---|---|
| $x=0$ (centre) | $\mu_0NI/2R$ | 1 |
| $x=R$ | $\mu_0NI/(4\sqrt{2}\,R)$ | $1/(2\sqrt{2})=0.354$ |
| $x\gg R$ | $\mu_0NIR^2/2x^3$ | falls as $1/x^3$ |

Far from the coil the field falls as $1/x^3$, like a magnetic dipole, not as $1/x^2$.

```figure caption="How the field on the axis of a circular coil falls with distance. At one radius from the centre it is already down to 35 % of the centre value; far away it falls as $1/x^3$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.7,2.8))
x = np.linspace(0, 4, 500)
B = 1.0/(1 + x**2)**1.5
ax.plot(x, B, color=ACCENT, lw=2.0)
ax.plot([1],[1/2**1.5],'o', color=INK, ms=4.5, zorder=5)
ax.plot([1,1],[0,1/2**1.5], color=MUTED, lw=0.8, ls=(0,(2,2)))
ax.plot([0,1],[1/2**1.5,1/2**1.5], color=MUTED, lw=0.8, ls=(0,(2,2)))
ax.annotate('x = R:  B = 0.354 B₀', xy=(1.05,0.34), xytext=(1.55,0.62), fontsize=8.6,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.8))
ax.text(2.55,0.17,'far away:  B ∝ 1/x³', fontsize=8.6, color=INK)
ax.set_xlabel('distance from centre  x / R')
ax.set_ylabel('B / B₀')
ax.set_xlim(0,4); ax.set_ylim(0,1.05)
ax.set_xticks([0,1,2,3,4])
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=0.5)
```

::: caution Centre formula on the axis is wrong
$B=\mu_0NI/2R$ holds **only at the centre**. On the axis use the full
$(R^2+x^2)^{3/2}$ form. At $x=R$ the field is not $B/2$ (that is the solenoid's end
value) but $B/(2\sqrt{2})\approx0.35B$.
:::

::: example Worked example 15.2 — centre and axis
**Problem.** A coil of 100 turns and radius 10 cm carries 2 A. Find the field at its
centre and at a point on its axis 20 cm from the centre.

**Solution.** Centre: $B_0=\dfrac{(4\pi\times10^{-7})(100)(2)}{2(0.10)}
=1.26\times10^{-3}\ \text{T}$.

Axis: $R^2+x^2=0.01+0.04=0.05\ \text{m}^2$, so
$B=\dfrac{(4\pi\times10^{-7})(100)(2)(0.01)}{2(0.05)^{3/2}}
=\dfrac{2.51\times10^{-6}}{0.0224}=1.1\times10^{-4}\ \text{T}$.

The field has dropped by a factor of about 11 in only two radii — the $1/x^3$ fall is
steep.
:::

### 15.1.4 The long solenoid

A **solenoid** is a long coil wound on a cylinder. If it has $N$ turns over length
$L$, the number of turns per unit length is $n=N/L$. Inside a long solenoid, well away
from the ends,

$$ B=\mu_0nI=\mu_0\frac{NI}{L} $$

The field inside is **uniform** — parallel straight lines of equal spacing — and the
field outside is practically **zero**. At the two ends, on the axis, the field is
**half** the interior value.

Apply Ampère's law to a rectangular loop with one side inside the solenoid parallel to
the axis and one side far outside, where $B\approx0$: the only contribution is from the
inside side, of length $\ell$, so $B\ell=\mu_0(n\ell)I$.

Note the difference from the coil: for a solenoid $B$ depends on the **turns per unit
length** $n$, not on the radius, and it does not fall off along the inside.

```figure caption="Field lines of a long straight wire (left) and of a long solenoid (right). The wire's lines are concentric circles; the solenoid's are parallel straight lines inside and almost absent outside."
import numpy as np, matplotlib.pyplot as plt
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(5.0,2.6))
for a in (ax1, ax2):
    a.set_aspect('equal'); a.axis('off')
# --- straight wire
th = np.linspace(0, 2*np.pi, 300)
for r in (0.60, 1.00, 1.40):
    ax1.plot(r*np.cos(th), r*np.sin(th), color=ACCENT, lw=1.2)
ax1.plot(0, 0, 'o', color=INK, ms=9)
ax1.plot(0, 0, 'o', color='white', ms=3.2)
ax1.annotate('', xy=(0.34,1.36), xytext=(-0.34,1.36),
             arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.2, mutation_scale=9))
ax1.annotate('', xy=(-1.38,0.30), xytext=(-1.38,-0.32),
             arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.2, mutation_scale=9))
ax1.text(0.40,1.50,'B', fontsize=9.5, color=ACCENT)
ax1.text(-1.62,-1.52,'⊙ = current out of page', fontsize=8.2, color=INK)
ax1.set_xlim(-1.75,1.75); ax1.set_ylim(-1.68,1.68)
# --- solenoid
ax2.plot([-1.45,1.45],[0.40,0.40], color=INK, lw=1.4)
ax2.plot([-1.45,1.45],[-0.40,-0.40], color=INK, lw=1.4)
ax2.add_patch(matplotlib.patches.Ellipse((-1.45,0), 0.26, 0.80,
              facecolor='white', edgecolor=INK, lw=1.2, zorder=4))
ax2.add_patch(matplotlib.patches.Ellipse((1.45,0), 0.26, 0.80,
              facecolor='white', edgecolor=INK, lw=1.2, zorder=4))
for x in np.linspace(-1.30, 1.20, 10):
    ax2.plot([x, x+0.14],[0.66,0.40], color=INK, lw=1.1)
    ax2.plot([x, x+0.14],[-0.66,-0.40], color=INK, lw=1.1)
for y in (-0.18, 0.0, 0.18):
    ax2.annotate('', xy=(1.18,y), xytext=(-1.18,y),
                 arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.2, mutation_scale=9))
ax2.text(0.0,0.86,'B = μ₀nI', fontsize=9.4, color=ACCENT, ha='center')
ax2.text(0.0,-0.90,'n = N / L', fontsize=8.6, color=INK, ha='center')
ax2.set_xlim(-1.85,1.85); ax2.set_ylim(-1.15,1.15)
```

| Source | Formula | Where it holds | Direction |
|---|---|---|---|
| Long straight wire | $B=\mu_0I/2\pi r$ | distance $r\ll$ length | circles round the wire |
| Circular coil, centre | $B=\mu_0NI/2R$ | at the centre only | along the axis |
| Circular coil, axis | $B=\mu_0NIR^2/2(R^2+x^2)^{3/2}$ | any point on the axis | along the axis |
| Long solenoid | $B=\mu_0nI$ | inside, away from the ends | along the axis |
| Solenoid end | $B=\mu_0nI/2$ | on the axis at the end | along the axis |

::: example Worked example 15.3 — a solenoid
**Problem.** A solenoid 40 cm long has 800 turns and carries 3 A. Find the field at its
centre and at one end on the axis.

**Solution.** $n=N/L=800/0.40=2000\ \text{m}^{-1}$.

$B=\mu_0nI=(4\pi\times10^{-7})(2000)(3)=7.5\times10^{-3}\ \text{T}$ at the centre, and
$3.8\times10^{-3}\ \text{T}$ at the end.
:::

::: tip Fast proportionality work
Write each formula once and then compare ratios. Wire: $B\propto I/r$. Coil centre:
$B\propto NI/R$. Solenoid: $B\propto NI/L$. In an MCQ with two setups, the constants
$\mu_0$ and $\pi$ cancel, and the answer is a ratio of two or three numbers.
:::

## 15.2 Force on a moving charge and on a current-carrying conductor; torque on a coil; Hall effect

### 15.2.1 Force on a moving charge

A charge $q$ moving with velocity $\vec v$ in a magnetic field $\vec B$ experiences

```photo id="phy12/galvanometer" caption="A moving-coil galvanometer from the early 20th century: the coil hangs between the poles of the permanent magnet and turns a pointer over a scale." width="60"
```


$$ \vec F=q\,\vec v\times\vec B \qquad\text{so}\qquad F=qvB\sin\theta $$

where $\theta$ is the angle between $\vec v$ and $\vec B$. The direction is given by
the right-hand rule for a positive charge (fingers from $\vec v$ to $\vec B$, thumb
gives $\vec F$); for an electron the force is opposite.

| Angle $\theta$ | Force |
|---|---|
| $0^{\circ}$ or $180^{\circ}$ (along the field) | zero |
| $90^{\circ}$ (across the field) | maximum, $qvB$ |
| any $\theta$ | $qvB\sin\theta$ |

Because $\vec F$ is perpendicular to $\vec v$ at every instant, the magnetic force does
**no work**: $W=\int\vec F\cdot d\vec s=0$. The speed and the kinetic energy of the
charge stay constant; only the direction of motion changes. This is why a magnetic
field can bend a beam of electrons into a circle without speeding it up.

::: caution The force is not along the field
A common error is to draw $\vec F$ along $\vec B$. It is perpendicular to **both**
$\vec v$ and $\vec B$. And a charge at rest, or moving exactly along the field,
feels no magnetic force at all.
:::

### 15.2.2 Circular and helical paths

If $\vec v$ is perpendicular to a uniform $\vec B$, the force is always perpendicular to
$\vec v$ and has constant magnitude $qvB$: the path is a circle. The magnetic force
supplies the centripetal force:

$$ qvB=\frac{mv^2}{r} \qquad\Longrightarrow\qquad r=\frac{mv}{qB}=\frac{p}{qB} $$

The **period** follows from $T=2\pi r/v$:

$$ T=\frac{2\pi m}{qB} \qquad\text{and}\qquad f=\frac{qB}{2\pi m} $$

The period does **not** contain $v$ or $r$. A faster particle travels a larger circle
in the same time. This is the principle of the cyclotron, and it is the most examined
single fact in this section.

If the velocity has a component $v_\parallel$ along $\vec B$ as well as $v_\perp$
across it, the two motions add: a circle in the plane perpendicular to $\vec B$, plus
constant motion along $\vec B$. The path is a **helix** (a corkscrew). Only the
perpendicular component bends:

$$ r=\frac{mv_\perp}{qB}=\frac{mv\sin\theta}{qB}, \qquad
   \text{pitch}=v_\parallel T=\frac{2\pi mv\cos\theta}{qB} $$

```figure caption="The helical path of a charge whose velocity has a component along the field. The circle comes from $v_\perp$; the steady drift along $B$ comes from $v_\parallel$; one turn advances the path by the pitch."
import numpy as np, matplotlib.pyplot as plt
fig, (ax, ax2) = plt.subplots(1, 2, figsize=(5.0,2.6),
                              gridspec_kw=dict(width_ratios=[1.55,1.0]))
for a in (ax, ax2):
    a.axis('off')
# --- left: the helix
R, w, d, turns = 0.50, 0.38, 0.60, 4
ts = np.linspace(0, 2*np.pi, 220)
xs, ys = [], []
for k in range(turns):
    xs.append(d*k + w*np.sin(ts))
    ys.append(R*np.cos(ts))
x = np.concatenate(xs); y = np.concatenate(ys)
ax.plot(x, y, color=ACCENT, lw=1.6)
ax.annotate('', xy=(x.max()+0.30, 0), xytext=(-0.28, 0),
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=0.9, mutation_scale=9,
                            linestyle=(0,(4,3))))
ax.text(x.max()+0.36, 0.09, 'B', fontsize=10, color=INK)
ax.annotate('', xy=(d, -0.90), xytext=(0, -0.90),
            arrowprops=dict(arrowstyle='<->', color=MUTED, lw=0.9, mutation_scale=8))
ax.text(d/2, -1.20, 'pitch', fontsize=9, color=MUTED, ha='center')
ax.set_xlim(-0.45, x.max()+0.72); ax.set_ylim(-1.38, 0.92)
# --- right: the velocity triangle
ax2.annotate('', xy=(1.55, 0), xytext=(-0.15, 0),
             arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=0.9, mutation_scale=9,
                             linestyle=(0,(4,3))))
ax2.text(1.62, 0.06, 'B', fontsize=10, color=INK)
ax2.annotate('', xy=(1.10, 0.72), xytext=(0, 0),
             arrowprops=dict(arrowstyle='-|>', color=SERIES[1], lw=1.6, mutation_scale=11))
ax2.text(1.12, 0.76, 'v', fontsize=10, color=SERIES[1])
ax2.annotate('', xy=(1.10, 0), xytext=(0, 0),
             arrowprops=dict(arrowstyle='-|>', color=SERIES[2], lw=1.4, mutation_scale=10))
ax2.text(0.50, -0.26, 'v cos θ', fontsize=8.8, color=SERIES[2])
ax2.annotate('', xy=(1.10, 0.72), xytext=(1.10, 0),
             arrowprops=dict(arrowstyle='-|>', color=SERIES[0], lw=1.4, mutation_scale=10))
ax2.text(1.17, 0.34, 'v sin θ', fontsize=8.8, color=SERIES[0])
ax2.add_patch(matplotlib.patches.Arc((0,0), 0.80, 0.80, theta1=0, theta2=33,
                                     color=INK, lw=0.9))
ax2.text(0.44, 0.10, 'θ', fontsize=9.5, color=INK)
ax2.plot([1.02,1.02,1.10],[0.08,0.08,0.08], color=INK, lw=0.8)
ax2.plot([1.02,1.02],[0,0.08], color=INK, lw=0.8)
ax2.set_xlim(-0.30, 1.90); ax2.set_ylim(-0.42, 1.02); ax2.set_aspect('equal')
```

::: example Worked example 15.4 — a proton in a field
**Problem.** A proton ($m=1.67\times10^{-27}$ kg, $q=1.6\times10^{-19}$ C) moves at
$1.0\times10^{6}$ m s⁻¹ perpendicular to a field of 0.50 T. Find the radius and the
period of its path.

**Solution.** $r=\dfrac{mv}{qB}=\dfrac{(1.67\times10^{-27})(10^{6})}{(1.6\times10^{-19})(0.50)}
=2.1\times10^{-2}\ \text{m}$.

$T=\dfrac{2\pi m}{qB}=\dfrac{2\pi(1.67\times10^{-27})}{8.0\times10^{-20}}
=1.3\times10^{-7}\ \text{s}$.

Check: $2\pi r/T=2\pi(0.021)/(1.3\times10^{-7})\approx10^{6}$ m s⁻¹ ✓.
:::

### 15.2.3 Force on a current-carrying conductor

A wire of length $L$ carrying current $I$ in a field $\vec B$ feels

$$ \vec F=I\,\vec L\times\vec B, \qquad F=BIL\sin\theta $$

where $\vec L$ points along the current. The force is greatest when the wire is
**perpendicular** to the field and zero when it is parallel.

The formula is just $F=qvB$ applied to all the drifting charges: if there are $n$ per
unit volume, each with drift speed $v_d$, the number in length $L$ is $nAL$ and the
total force is $(nAL)(ev_dB\sin\theta)=BIL\sin\theta$, using $I=nAev_d$.

::: example Worked example 15.5 — force on a wire
**Problem.** A straight wire 0.50 m long carries 4.0 A at 30° to a uniform field of
0.30 T. Find the force on it.

**Solution.** $F=BIL\sin\theta=(0.30)(4.0)(0.50)\sin30^{\circ}=0.30\ \text{N}$.

The component of the wire along the field ($L\cos30^{\circ}$) contributes nothing;
only the perpendicular component matters.
:::

### 15.2.4 Torque on a coil and the moving-coil galvanometer

A rectangular coil of $N$ turns, area $A$, carrying current $I$ in a uniform field
$\vec B$ behaves as a magnetic dipole of moment

$$ M=NIA \qquad (\text{unit A m}^2) $$

The two sides perpendicular to the field carry current in opposite directions and feel
equal and opposite forces, which form a **couple**. If $\theta$ is the angle between
$\vec B$ and the **normal** to the coil,

$$ \tau=NIAB\sin\theta=MB\sin\theta $$

::: derivation Torque on a current-carrying coil
**Setting up.** A rectangular coil of sides $a$ and $b$, so $A=ab$, with $N$ turns,
carrying current $I$. The field $\vec B$ lies in the plane of the page; the normal to
the coil makes an angle $\theta$ with $\vec B$.

**Step 1 — which sides feel a force.** The two sides of length $a$ are perpendicular to
$\vec B$, so each feels $F=BIa$ per turn. The two sides of length $b$ are parallel to
$\vec B$, so they feel no force.

**Step 2 — the forces form a couple.** The two $BIa$ forces are equal, opposite and
not in the same line. Their perpendicular separation is $b\sin\theta$.

**Step 3 — multiply force by separation.**
$$ \tau=(BIa)(b\sin\theta)=BIA\sin\theta $$

**Step 4 — allow for $N$ turns.** Each turn carries the same current, so the torques
add:
$$ \tau=NIAB\sin\theta $$

**Result.** $\tau=NIAB\sin\theta=MB\sin\theta$, where $M=NIA$.

**What it means.** The torque is maximum when the **plane** of the coil is parallel to
$\vec B$ (normal perpendicular to $\vec B$, $\theta=90^{\circ}$) and zero when the plane
is perpendicular to $\vec B$. A coil in a uniform field therefore rotates until its
normal lies along the field — the position a compass needle takes.
:::

::: caution Angle of the coil
$NIAB\sin\theta$ uses $\theta$ between $\vec B$ and the **normal**. "The plane of the
coil is parallel to the field" means $\theta=90^{\circ}$ and the torque is **maximum**.
Students who use the angle to the plane get every such question backwards.
:::

**The moving-coil galvanometer.** A small coil is suspended between the poles of a
permanent magnet shaped so that the field is **radial**: at every coil position the
plane of the coil is parallel to the field. Then $\sin\theta=1$ always, and

$$ \tau=NIAB $$

independent of the coil's angle. A hairspring provides a restoring torque
$\tau=k\phi$, where $\phi$ is the deflection. At equilibrium,

$$ NIAB=k\phi \qquad\Longrightarrow\qquad \phi=\frac{NAB}{k}I $$

so the deflection is **directly proportional to the current** and the scale is linear.

| Quantity | Expression | Meaning |
|---|---|---|
| Current sensitivity | $NAB/k$ | deflection per unit current (rad A⁻¹) |
| Voltage sensitivity | $NAB/(kG)$ | deflection per unit voltage, $G$ = coil resistance |
| Full-scale current | $I_g=k\phi_{max}/NAB$ | the current that gives the largest reading |

The galvanometer is the parent instrument of the ammeter and the voltmeter (Chapter
14): a shunt in parallel makes an ammeter, a multiplier in series makes a voltmeter.

### 15.2.5 The Hall effect

Send a current $I$ along a thin conducting strip of thickness $t$, with a magnetic
field $B$ perpendicular to the face of the strip. The charge carriers are pushed to one
side by the magnetic force. Charge collects there until the transverse electric field
$E_H$ is strong enough to cancel the magnetic force. A **Hall voltage** $V_H$ then
appears across the width of the strip.

::: derivation Hall voltage
**Setting up.** A strip of thickness $t$ and width $d$, current $I$ along its length,
field $B$ perpendicular to its face. Carriers of charge $q$ and drift speed $v_d$.

**Step 1 — balance of forces at equilibrium.** The magnetic force $qv_dB$ sideways is
balanced by the electric force $qE_H$ from the piled-up charge:
$$ qE_H=qv_dB \qquad\Longrightarrow\qquad E_H=v_dB $$

**Step 2 — convert field to voltage.** The field is uniform across the width $d$, so
$$ V_H=E_Hd=v_dBd $$

**Step 3 — express $v_d$ through the current.** The current crosses the area $dt$, so
$I=nq\,v_d\,dt$ and $v_d=\dfrac{I}{nqdt}$.

**Step 4 — substitute.**
$$ V_H=\frac{I}{nqdt}Bd=\frac{BI}{nqt} $$

**Result.** $V_H=\dfrac{BI}{net}$ for electrons ($q=e$).

**What it means.** The width $d$ cancels: a thinner strip gives a larger Hall voltage,
which is why Hall probes are made as thin films. A larger carrier density $n$ gives a
smaller voltage, so the effect is strong in semiconductors and weak in metals.
:::

**The sign of the Hall voltage.** Reverse the reasoning and it becomes a test:

- If the carriers are **negative** (electrons), they drift opposite to the conventional
  current, and the magnetic force pushes them to one side, making that side negative.
- If the carriers are **positive** (holes), they drift along the current, and the same
  magnetic force pushes them to the *same* side, making that side **positive**.

The two cases give opposite polarity. So the sign of $V_H$ tells you the sign of the
charge carriers — the experiment that proved that current in a metal is carried by
negative electrons.

The **Hall coefficient** is

$$ R_H=\frac{1}{nq}=\frac{V_Ht}{BI} $$

Its magnitude gives the carrier density and its sign gives the carrier type. In a
semiconductor, $R_H$ is negative for an n-type and positive for a p-type sample.

| Use of the Hall effect | What it relies on |
|---|---|
| Identifying the carrier sign | polarity of $V_H$ |
| Measuring carrier density | $n=BI/(eV_Ht)$ |
| Hall probe magnetometer | $V_H\propto B$ at fixed current |
| Multiplying (analogue computers) | $V_H\propto IB$ |

::: caution Hall voltage and thickness
$V_H=BI/net$: the voltage is **inversely** proportional to the thickness $t$ and does
**not** depend on the width. Doubling the thickness halves the Hall voltage. A
distractor that offers "doubles" is testing exactly this.
:::

::: example Worked example 15.6 — a Hall probe
**Problem.** A copper strip 0.10 mm thick carries 10 A in a field of 1.5 T
perpendicular to its face. Taking $n=8.5\times10^{28}$ m⁻³, find the Hall voltage.

**Solution.**
$V_H=\dfrac{BI}{net}=\dfrac{(1.5)(10)}{(8.5\times10^{28})(1.6\times10^{-19})(1.0\times10^{-4})}
=\dfrac{15}{1.36\times10^{6}}=1.1\times10^{-5}\ \text{V}$.

That is only 11 μV — measurable, but a reminder of why the effect is more useful in
semiconductors, where $n$ is a thousand times smaller and $V_H$ a thousand times
larger.
:::

## 15.3 Dia-, para- and ferromagnetism: domains, relative permeability, susceptibility and hysteresis

### 15.3.1 Magnetisation, permeability and susceptibility

When a material is placed in a magnetic field, its atomic currents give it a
**magnetisation** $\vec M$ — the magnetic moment per unit volume (A m⁻¹). The applied
field is described by $\vec H=nI$ (A m⁻¹), and the field inside the material is

$$ B=\mu_0(H+M)=\mu_0\mu_rH $$

| Quantity | Symbol | Definition | Unit |
|---|---|---|---|
| Relative permeability | $\mu_r$ | $B/(\mu_0H)=\mu/\mu_0$ | none |
| Susceptibility | $\chi$ | $M/H$ | none |
| Relation | | $\mu_r=1+\chi$ | |

So a material with $\chi=599$ has $\mu_r=600$ and multiplies the field of a solenoid
600 times. Since $\mu_r=1+\chi$, a small negative $\chi$ gives $\mu_r$ just below 1.

### 15.3.2 The three classes of magnetic material

| Property | Diamagnetic | Paramagnetic | Ferromagnetic |
|---|---|---|---|
| Atomic dipoles | none; induced only | permanent, randomly oriented | permanent, in domains |
| $\chi$ | small **negative**, about $-10^{-5}$ | small positive, $10^{-5}$–$10^{-3}$ | large positive, $10^{2}$–$10^{5}$ |
| $\mu_r$ | slightly less than 1 | slightly more than 1 | much greater than 1 |
| Temperature | independent of $T$ | $\chi=C/T$ (Curie's law) | $\chi=C/(T-T_C)$ above $T_C$ |
| In a non-uniform field | weakly **repelled** from the strong region | weakly attracted to the strong region | strongly attracted |
| Examples | Bi, Cu, Ag, Au, water, N₂, CO₂ | Al, Na, Pt, O₂, CuCl₂ | Fe, Co, Ni, Gd, alnico |

**Diamagnetism** arises in every material but is usually masked. The applied field
changes the orbital motion of the electrons so that a small moment is induced
**opposite** to the field — the atomic version of Lenz's law. There are no permanent
dipoles, so thermal agitation has nothing to randomise and $\chi$ hardly depends on
temperature. A superconductor is a perfect diamagnet, with $\chi=-1$ and
$\mu_r=0$: it expels the field completely (the Meissner effect).

**Paramagnetism** comes from atoms with a permanent magnetic moment. In zero field the
moments point in all directions and cancel. A field aligns them partially, but thermal
motion opposes the alignment, so the effect is weak and increases as the material is
cooled: **Curie's law**, $\chi=C/T$.

**Ferromagnetism** is different in kind, not degree. The moments are not independent:
they lock together in large regions called **domains**, so a modest field can produce a
very large magnetisation. $\chi$ can reach $10^{5}$.

### 15.3.3 Domain theory

A ferromagnetic solid is divided into **domains** — regions of microscopic size (order
$10^{-5}$ m, containing many thousands of atoms) in each of which the atomic moments
are already perfectly aligned. The domains point along a few easy directions of the
crystal.

- In an **unmagnetised** sample the domains point in random directions, so their
  moments cancel and the net magnetisation is zero.
- In an increasing field, domains whose moment is close to the field **grow** at the
  expense of the others (the domain walls move), and then the moments **rotate** into
  the field direction.
- At **saturation** the whole sample is one domain pointing along the field, and a
  further increase of $H$ produces almost no increase in $B$.

The **Curie point** $T_C$ is the temperature above which thermal agitation destroys the
domain alignment. The material then becomes paramagnetic, with
$\chi=C/(T-T_C)$. Typical values: iron 770 °C, cobalt 1115 °C, nickel 358 °C. Heating a
steel magnet above its Curie point and cooling it in zero field leaves it unmagnetised
— the standard way to demagnetise a magnet.

::: caution Domains are not molecules
A domain is a region of a crystal in which the moments are aligned; it is not a
particle and it does not move through the material as a whole. Magnetisation proceeds
by the **growth** of favourably oriented domains and by **rotation** of the moments,
not by domains physically travelling.
:::

### 15.3.4 Hysteresis

Plot $B$ inside a ferromagnetic material against the applied field $H$ as $H$ is taken
round a cycle. The curve does not retrace itself: it forms a **hysteresis loop**.

| Feature of the loop | Meaning |
|---|---|
| Saturation | the flat top, where all domains are aligned |
| **Retentivity** (remanence) $B_r$ | the $B$ left when $H$ is reduced to zero — how strong a permanent magnet the material makes |
| **Coercivity** $H_c$ | the reverse field needed to bring $B$ back to zero — how hard the material is to demagnetise |
| Area of the loop | energy dissipated as heat per cycle **per unit volume** (J m⁻³) |

The area matters in machines. In a transformer core the material is taken round the
loop 50 times a second, so the hysteresis power loss is

$$ P_{hyst}=(\text{area of loop})\times(\text{volume of core})\times(\text{frequency}) $$

```figure caption="Hysteresis loops. Soft iron has a tall, narrow loop — small retentivity and coercivity, little area, little loss per cycle. Steel has a wide loop — large retentivity and coercivity, so it stays magnetised, but it wastes energy in a core."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.9,3.0))
H = np.linspace(-700, 700, 600)
def loop(Bs, Hc, a):
    up = Bs*np.tanh((H - Hc)/a)
    dn = Bs*np.tanh((H + Hc)/a)
    return up, dn
Bs1, Hc1, a1 = 1.55, 25.0, 110.0
Bs2, Hc2, a2 = 1.15, 230.0, 420.0
up1, dn1 = loop(Bs1, Hc1, a1)
up2, dn2 = loop(Bs2, Hc2, a2)
ax.plot(np.r_[H, H[::-1], H[0]], np.r_[dn1, up1[::-1], dn1[0]], color=ACCENT, lw=1.9,
        label='soft iron (narrow loop)')
ax.plot(np.r_[H, H[::-1], H[0]], np.r_[dn2, up2[::-1], dn2[0]], color='#A8271F', lw=1.9,
        label='steel (wide loop)')
ax.axhline(0, color=INK, lw=0.8)
ax.axvline(0, color=INK, lw=0.8)
Br2 = Bs2*np.tanh(Hc2/a2)
ax.plot([0],[Br2],'o', color='#A8271F', ms=4, zorder=6)
ax.plot([-Hc2],[0],'o', color='#A8271F', ms=4, zorder=6)
ax.annotate('Bᵣ', xy=(5, Br2), xytext=(90, 0.30), fontsize=9.5, color='#A8271F',
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.8))
ax.annotate('−Hc', xy=(-Hc2, 0), xytext=(-620, -0.34), fontsize=9.5, color='#A8271F',
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.8))
ax.set_xlabel('applied field  H  (A m⁻¹)')
ax.set_ylabel('flux density  B  (T)')
ax.set_xlim(-700,700); ax.set_ylim(-1.55,1.70)
ax.set_xticks([-600,-300,0,300,600])
ax.set_yticks([-1,0,1])
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=0.4)
ax.legend(loc='lower right', fontsize=8.2, frameon=False)
```

**Soft iron versus steel.** The choice of material is decided by the loop:

| | Soft iron | Steel |
|---|---|---|
| Loop | narrow, steep | wide |
| Retentivity $B_r$ | small | large |
| Coercivity $H_c$ | small | large |
| Permeability $\mu_r$ | very high | moderate |
| Hysteresis loss | small | large |
| Best use | transformer cores, electromagnets, relays, generator armatures | permanent magnets, loudspeakers, magnetic chucks, memory devices |

A transformer core is magnetised and demagnetised 100 times a second (twice per cycle).
Any area inside its loop is energy turned into heat, so the core must be **soft**: easy
to magnetise, easy to demagnetise, narrow loop. A permanent magnet must **keep** its
magnetisation after the field is removed and must resist demagnetising fields, so it
must be **hard**: large retentivity and large coercivity — steel, and in practice
alnico or ferrite.

::: caution "Strong magnet" is not the same as "good core"
Soft iron makes a *strong temporary* magnet and a poor permanent magnet; steel makes a
*weaker but lasting* magnet. Exam questions often ask which is used where, and the
answer follows from the loop, not from which material is "more magnetic".
:::

::: example Worked example 15.7 — reading a loop
**Problem.** A ferromagnetic sample has $\mu_r=600$ at a field $H=200$ A m⁻¹. Find
$B$, $M$ and $\chi$.

**Solution.** $\chi=\mu_r-1=599$.

$B=\mu_0\mu_rH=(4\pi\times10^{-7})(600)(200)=1.51\times10^{-1}\ \text{T}$.

$M=\chi H=599(200)=1.20\times10^{5}\ \text{A m}^{-1}$.

Check: $\mu_0(H+M)=4\pi\times10^{-7}(200+1.2\times10^{5})=0.151$ T ✓ — the
magnetisation, not the applied field, supplies almost all of $B$.
:::

```photogrid label="15.1" cols="2" ratio="1.2" caption="Field falls as 1 / r^3. (a) Filaments of iron line up along the field of a bar magnet; lines crowd at the poles where the field is strongest. (b) On the axis of a short magnet B = (mu0 / 4 pi) 2m / r^3. For an assumed magnetic moment m = 1.0 A m^2 the field is 0.20 mT at 10 cm, 5 times the Earth's horizontal field of 40 microtesla (assumed), and falls eight-fold when r doubles. The magnet's field equals the Earth's at r = 17.1 cm, beyond which a compass ignores it."
@ photo id="ceephy/filings" cap="Iron filings show the field lines of a bar magnet, crowded near the poles"
fit 1.2
focus 0.5 0.5
@ svg cap="Axial field of a bar magnet against the Earth's field"
mu = 4e-7 * math.pi; m = 1.0; BE = 40e-6
B = lambda r: mu / (4 * math.pi) * 2 * m / r ** 3
req = (mu / (4 * math.pi) * 2 * m / BE) ** (1 / 3)
assert abs(B(0.1) - 2e-4) < 1e-9 and abs(B(0.2) * 8 - B(0.1)) < 1e-12 and abs(req - 0.171) < 0.001
facts = dict(b10="%.2f" % (B(0.1) * 1e3), mult="%.0f" % (B(0.1) / BE), req="%.1f" % (req * 100))
f = Fig(300, 236)
f.text(150, 14, "log B against r on the magnet axis", size=10.5, color=NAVY, bold=True)
lg = lambda r_cm: math.log10(B(r_cm / 100))
X = lambda r: 44 + (r - 5) * 9; Y = lambda l: 54 + (-2.7 - l) * 36
f.line(X(5), Y(-5.3), 280, Y(-5.3), color=SLATE, sw=1.4); f.line(X(5), Y(-5.3), X(5), 34, color=SOFT, sw=1.2)
pts = [(X(r), Y(lg(r))) for r in range(5, 31)]
for (a, b), (c, d) in zip(pts, pts[1:]): f.line(a, b, c, d, color=NAVY, sw=2.6)
ye = Y(math.log10(BE)); f.line(X(5), ye, 280, ye, color=AMBER, sw=1.4, dash=True)
f.text(278, ye - 8, "Earth 40 uT", size=10.5, color=AMBER, bold=True, anchor="end")
f.line(X(req * 100), ye, X(req * 100), Y(-5.3), color=TEAL, sw=1.2, dash=True); f.circle(X(req * 100), ye, 4, fill=TEAL, stroke=TEAL)
for r in (10, 20, 30): f.text(X(r), Y(-5.3) + 13, "%d" % r, size=10.5, color=SLATE)
f.text(150, 192, "B = %.2f mT at 10 cm (%.0f x Earth)" % (B(0.1) * 1e3, B(0.1) / BE), size=10.5, color=NAVY, bold=True)
f.text(150, 210, "equal to Earth at r = %.1f cm" % (req * 100), size=10.5, color=TEAL, bold=True)
f.text(150, 228, "r in cm; m = 1.0 A m^2 assumed", size=10.5, color=SLATE)
```

```photogrid label="15.2" cols="2" ratio="1.2" caption="Why the motor needs a commutator. (a) The split-ring commutator and carbon brushes reverse the current in the coil every half turn. (b) The cell computes the torque on a coil of 100 turns, area 12 cm2, carrying 2 A in a field of 0.2 T: the maximum, when the plane of the coil is parallel to the field, is 48 mN m, and it falls as sin(a) to zero when the plane is perpendicular. Because the commutator keeps the torque in one direction, the mean torque is 2 / pi of the maximum, 30.6 mN m, and at 3000 rpm the motor delivers about 9.6 W of mechanical power. Without the commutator the coil would only swing back and forth."
@ photo id="ceephy3/motor" cap="The commutator and brushes of a DC motor"
fit 1.2
focus 0.5 0.5
@ svg cap="Torque on a current-carrying coil"
import math
N, B, I = 100, 0.2, 2.0
A = 0.04 * 0.03
tmax = N * B * I * A
rows = [("%d deg" % a, tmax * math.sin(math.radians(a)) * 1000) for a in (90, 60, 30, 0)]
mean = tmax * 2 / math.pi
P = mean * 2 * math.pi * 3000 / 60
assert round(tmax, 3) == 0.048 and round(P, 1) == 9.6
f = Fig(300, 236)
f.text(150, 12, "Torque tau = N B I A sin(a), mN m", size=10.5, color=NAVY, bold=True)
hbars(f, rows, vmax=50, fmt="%.1f", x0=56, y0=30, bw=170, gap=30,
      colors=[(ROSE, RED), (SAND, AMBER), (MINT, TEAL), (BLUE, NAVY)])
f.text(150, 158, "a = angle between the coil plane and the field", size=10, color=SLATE, bold=True)
f.text(150, 178, "N = 100, B = 0.2 T, I = 2 A, A = 12 cm2", size=10.5, color=NAVY, bold=True)
f.text(150, 198, "mean torque (commutated) = %.1f mN m" % (mean * 1000), size=10.5, color=NAVY, bold=True)
f.text(150, 216, "power at 3000 rpm = %.1f W" % P, size=10.5, color=NAVY, bold=True)
facts = dict(t=tmax * 1000, m=mean * 1000, P=P)
```

## Formula and fact sheet

| Topic | Formula or fact |
|---|---|
| Permeability of free space | $\mu_0=4\pi\times10^{-7}\ \text{T m A}^{-1}$ |
| Straight wire | $B=\mu_0I/2\pi r$, circles round the wire, right-hand grip rule |
| Parallel wires | $F/L=\mu_0I_1I_2/2\pi d$; same direction attract, opposite repel |
| Coil, centre | $B=\mu_0NI/2R$ |
| Coil, axis | $B=\mu_0NIR^2/2(R^2+x^2)^{3/2}$; at $x=R$, $B=0.354B_0$; far away $B\propto1/x^3$ |
| Solenoid | $B=\mu_0nI=\mu_0NI/L$ inside; $B/2$ at the ends; $B\approx0$ outside |
| Magnetic force on a charge | $F=qvB\sin\theta$; perpendicular to $\vec v$; does no work |
| Circular path | $r=mv/qB=p/qB$; $T=2\pi m/qB$; $f=qB/2\pi m$ |
| Helix | $r=mv\sin\theta/qB$; pitch $=2\pi mv\cos\theta/qB$ |
| Force on a wire | $F=BIL\sin\theta$ |
| Coil torque | $\tau=NIAB\sin\theta=MB\sin\theta$; $M=NIA$ |
| Galvanometer | radial field gives $\tau=NIAB$; $\phi=(NAB/k)I$ |
| Hall voltage | $V_H=BI/net$; $R_H=1/nq=V_Ht/BI$ |
| Magnetic properties | $\mu_r=\mu/\mu_0=1+\chi$; $\chi=M/H$ |
| Diamagnetic | $\chi\approx-10^{-5}$, $\mu_r<1$, repelled, $T$-independent (Bi, Cu, water) |
| Paramagnetic | $\chi\approx10^{-5}$–$10^{-3}$, $\mu_r>1$, attracted, $\chi=C/T$ (Al, O₂) |
| Ferromagnetic | domains, $\chi\gg1$, Curie point, $\chi=C/(T-T_C)$ above $T_C$ (Fe, Co, Ni) |
| Curie points | Fe 770 °C, Co 1115 °C, Ni 358 °C |
| Hysteresis | $B_r$ retentivity, $H_c$ coercivity; loop area = energy per cycle per unit volume |
| Core versus magnet | soft iron: narrow loop, transformer cores; steel: wide loop, permanent magnets |

## Chapter summary

- A long straight wire gives $B=\mu_0I/2\pi r$, with circular field lines; two parallel
  wires with currents in the **same** direction attract, with
  $F/L=\mu_0I_1I_2/2\pi d$.
- At the centre of a coil $B=\mu_0NI/2R$; on the axis
  $B=\mu_0NIR^2/2(R^2+x^2)^{3/2}$, which is $0.354$ of the centre value at $x=R$ and
  falls as $1/x^3$ far away.
- Inside a long solenoid $B=\mu_0nI$ is uniform, outside it is nearly zero, and at the
  ends it is half the interior value.
- The magnetic force $F=qvB\sin\theta$ is perpendicular to $\vec v$ and does no work, so
  speed and kinetic energy stay constant; $r=mv/qB$ and $T=2\pi m/qB$, independent of
  speed. A velocity component along $\vec B$ turns the circle into a helix of pitch
  $v_\parallel T$.
- A wire feels $F=BIL\sin\theta$; a coil feels $\tau=NIAB\sin\theta$, maximum when its
  plane is parallel to the field. A radial field makes a galvanometer's deflection
  proportional to current.
- The Hall voltage $V_H=BI/net$ is inversely proportional to thickness, independent of
  width, and its polarity reveals whether the carriers are positive or negative.
- $\mu_r=1+\chi$. Diamagnets have a tiny negative $\chi$ and are repelled; paramagnets
  a tiny positive $\chi$ obeying $\chi=C/T$ and are attracted; ferromagnets have domains
  and a very large $\chi$ below the Curie point.
- The hysteresis loop gives retentivity (residual $B$), coercivity (field to erase $B$)
  and, through its area, the energy lost per cycle. Soft iron's narrow loop suits
  transformer cores; steel's wide loop suits permanent magnets.

## Practice questions

**Set A — Recall (28 questions)**

1. The SI unit of magnetic flux density is
   (a) weber (b) tesla (c) henry (d) newton per ampere
2. The magnetic field at a perpendicular distance r from a long straight wire carrying current I is
   (a) $\mu_0I/2\pi r$ (b) $\mu_0I/2r$ (c) $\mu_0I/4\pi r^2$ (d) $\mu_0I/2\pi r^2$
3. The field at the centre of a circular coil of N turns, radius R, carrying current I is
   (a) $\mu_0NI/R$ (b) $\mu_0NI/4R$ (c) $\mu_0NI/2\pi R$ (d) $\mu_0NI/2R$
4. Inside a long solenoid with n turns per metre carrying current I, the field is
   (a) $\mu_0NI$ (b) $\mu_0nI/2$ (c) $\mu_0nI$ (d) $\mu_0I/2\pi n$
5. The permeability of free space is
   (a) $4\pi\times10^{-7}\ \text{T m A}^{-1}$ (b) $4\pi\times10^{-7}\ \text{T m}^2\text{A}^{-1}$ (c) $8.85\times10^{-12}\ \text{F m}^{-1}$ (d) $9\times10^{9}\ \text{N m}^2\text{C}^{-2}$
6. The magnetic force on a moving charge is zero when the angle between its velocity and the field is
   (a) 90° (b) 45° (c) 0° (d) 60°
7. A charged particle moves in a circle of radius r in a uniform field B. Its radius is
   (a) $qB/mv$ (b) $mv/qB$ (c) $mv^2/qB$ (d) $qvB/m$
8. The force per unit length between two long parallel wires carrying currents $I_1$ and $I_2$ at separation d is
   (a) $\mu_0I_1I_2/2\pi d$ (b) $\mu_0I_1I_2/4\pi d$ (c) $\mu_0I_1I_2/2\pi d^2$ (d) $\mu_0(I_1+I_2)/2\pi d$
9. Two long parallel wires carry currents in the same direction. They
   (a) repel each other (b) exert no force (c) rotate about each other (d) attract each other
10. The torque on a coil in a magnetic field is maximum when the plane of the coil is
   (a) perpendicular to the field (b) parallel to the field (c) at 45° to the field (d) at 60° to the field
11. The deflection of a moving-coil galvanometer is proportional to the current because
   (a) the radial field keeps the torque proportional to the current (b) the coil has a large moment of inertia (c) the field is very strong (d) the coil turns at constant speed
12. The Hall voltage across a strip of thickness t carrying current I in field B is
   (a) $net/IB$ (b) $IBt/ne$ (c) $IB/net$ (d) $neIB/t$
13. The sign of the Hall voltage tells us
   (a) the magnitude of the current (b) the sign of the charge carriers (c) the resistance of the material (d) the field strength only
14. A material whose relative permeability is slightly less than 1 is
   (a) paramagnetic (b) ferromagnetic (c) non-magnetic (d) diamagnetic
15. The susceptibility of a ferromagnetic material is
   (a) small and negative (b) small and positive (c) very large and positive (d) exactly zero
16. The relation between relative permeability and susceptibility is
   (a) $\mu_r=1+\chi$ (b) $\mu_r=1-\chi$ (c) $\mu_r=\chi$ (d) $\mu_r=\chi-1$
17. Curie's law for a paramagnetic material states that its susceptibility is
   (a) proportional to T (b) inversely proportional to T (c) independent of T (d) proportional to T²
18. Above the Curie point, a ferromagnetic material becomes
   (a) diamagnetic (b) superconducting (c) an insulator (d) paramagnetic
19. The area of a hysteresis loop represents
   (a) the retentivity (b) the coercivity (c) the energy lost per cycle per unit volume (d) the saturation magnetisation
20. Soft iron is preferred for transformer cores because it has
   (a) high retentivity and high coercivity (b) a narrow loop and high permeability (c) a large hysteresis loss (d) low permeability
21. Steel is preferred for permanent magnets because it has
   (a) low retentivity (b) low coercivity (c) a narrow hysteresis loop (d) high retentivity and high coercivity
22. The field on the axis of a circular coil at distance x from the centre varies as
   (a) $1/(R^2+x^2)^{3/2}$ (b) $1/(R^2+x^2)$ (c) $1/(R^2+x^2)^{1/2}$ (d) $(R^2+x^2)^{3/2}$
23. At the end of a long solenoid, the field on the axis is
   (a) equal to the field at the centre (b) half the field at the centre (c) twice the field at the centre (d) zero
24. The magnetic force on a current-carrying conductor is greatest when the conductor is
   (a) parallel to the field (b) at 45° to the field (c) perpendicular to the field (d) at 60° to the field
25. The magnetic moment of a coil of N turns, area A and current I is
   (a) NIA (b) NI/A (c) NIA² (d) IA/N
26. When a ferromagnetic material is heated above its Curie temperature, its domains
   (a) grow larger (b) become perfectly aligned (c) reverse permanently (d) are destroyed and it becomes paramagnetic
27. Which of the following is diamagnetic?
   (a) iron (b) aluminium (c) bismuth (d) nickel
28. The magnetic field lines inside a long solenoid are
   (a) concentric circles (b) parallel straight lines (c) radial (d) curved outwards

::: note Answers and explanations — Set A
**1.** (b) — 1 T = 1 N A⁻¹ m⁻¹ = 1 Wb m⁻². The weber is the unit of flux, the henry of inductance.
**2.** (a) — Ampère's law round a circle of radius r gives $B(2\pi r)=\mu_0I$, so $B=\mu_0I/2\pi r$; the $1/r^2$ forms belong to point charges.
**3.** (d) — each turn contributes $\mu_0I/2R$ at the centre and N turns add, giving $\mu_0NI/2R$.
**4.** (c) — $B=\mu_0nI$ with n the turns per metre; $N$ alone is not enough without the length.
**5.** (a) — $\mu_0=4\pi\times10^{-7}$ T m A⁻¹. (c) is $\varepsilon_0$ and (d) is $1/4\pi\varepsilon_0$.
**6.** (c) — $F=qvB\sin\theta$ vanishes when $\theta=0^{\circ}$ (or 180°), i.e. when the velocity is along the field.
**7.** (b) — $qvB=mv^2/r$ gives $r=mv/qB$. Option (a) is the reciprocal and (c) is dimensionally wrong.
**8.** (a) — $B_1=\mu_0I_1/2\pi d$ at the second wire, and $F/L=B_1I_2$.
**9.** (d) — parallel currents attract. It is the opposite of the rule for like charges, which repel.
**10.** (b) — the torque is $NIAB\sin\theta$ with $\theta$ measured from the **normal**; the plane parallel to the field means the normal is perpendicular, so $\sin\theta=1$.
**11.** (a) — the radial field keeps $\sin\theta=1$, so $\tau=NIAB$ whatever the coil's angle, and the spring gives $\phi\propto I$.
**12.** (c) — balancing $qE_H=qv_dB$ and using $I=ne v_d t d$ gives $V_H=BI/net$; the width cancels.
**13.** (b) — electrons and holes are deflected to the same side but have opposite charge, so the polarity of $V_H$ reverses.
**14.** (d) — diamagnets have a small negative $\chi$, so $\mu_r=1+\chi$ is just below 1.
**15.** (c) — domain alignment gives $\chi$ of order $10^{2}$–$10^{5}$, positive.
**16.** (a) — $B=\mu_0(H+M)$ and $M=\chi H$ give $B=\mu_0(1+\chi)H$, so $\mu_r=1+\chi$.
**17.** (b) — thermal agitation opposes alignment, so $\chi=C/T$: cooling a paramagnet strengthens its response.
**18.** (d) — above $T_C$ the domains break up and the material behaves as a paramagnet with $\chi=C/(T-T_C)$.
**19.** (c) — the area is the work done per unit volume per cycle, dissipated as heat.
**20.** (b) — a narrow loop means little hysteresis loss each cycle, and high permeability means a strong flux for a small current.
**21.** (d) — a large retentivity keeps the magnetism after magnetisation and a large coercivity resists demagnetisation.
**22.** (a) — $B=\mu_0NIR^2/2(R^2+x^2)^{3/2}$; the numerator is constant on the axis, so $B\propto(R^2+x^2)^{-3/2}$.
**23.** (b) — half the interior value: the field lines spread out at the end.
**24.** (c) — $F=BIL\sin\theta$ is maximum at $\theta=90^{\circ}$.
**25.** (a) — $M=NIA$, in A m².
**26.** (d) — thermal energy overcomes the domain alignment; the material becomes paramagnetic.
**27.** (c) — bismuth is the standard diamagnetic example; iron and nickel are ferromagnetic and aluminium paramagnetic.
**28.** (b) — inside a long solenoid the field is uniform, with parallel straight lines.
:::

**Set B — Understanding (17 questions)**

1. Two long parallel wires carry currents in opposite directions. The force between them is
   (a) attractive, proportional to 1/d (b) attractive, proportional to 1/d² (c) repulsive, proportional to 1/d (d) repulsive, proportional to 1/d²
2. A charged particle enters a uniform field with its velocity perpendicular to the field. Which pair stays constant?
   (a) speed and kinetic energy (b) velocity and momentum (c) speed and momentum (d) kinetic energy and velocity
3. The period of circular motion of a charge in a uniform magnetic field is independent of
   (a) the charge (b) the mass (c) the field (d) the speed
4. A proton and an alpha particle enter the same field with the same speed, perpendicular to it. The ratio of their radii $r_p:r_\alpha$ is
   (a) 1 : 4 (b) 1 : 2 (c) 2 : 1 (d) 1 : 1
5. A long straight vertical wire carries current upward. At a point due south of the wire, the field points
   (a) upward (b) downward (c) east (d) west
6. The current in a circular coil is doubled and its radius is halved. The field at its centre becomes
   (a) 4 times (b) 2 times (c) unchanged (d) half
7. A charged particle moves with its velocity parallel to a uniform magnetic field. Its path is
   (a) a circle (b) a parabola (c) a helix (d) a straight line
8. An electron moves at 30° to a uniform field and follows a helix. The pitch of the helix is
   (a) $2\pi mv/qB$ (b) $2\pi mv\cos30^{\circ}/qB$ (c) $2\pi mv\sin30^{\circ}/qB$ (d) $mv\cos30^{\circ}/qB$
9. A diamagnetic substance is placed in a strong non-uniform field. It moves
   (a) from the stronger to the weaker part (b) from the weaker to the stronger part (c) not at all (d) along the field lines only
10. A paramagnetic substance is placed in a magnetic field. Its atomic dipoles
   (a) are unaffected (b) align opposite to the field (c) align along the field but are randomised by thermal motion (d) lock permanently along the field
11. A material has relative permeability 1.0002. It is
   (a) diamagnetic (b) paramagnetic (c) ferromagnetic (d) non-magnetic
12. As the temperature rises above the Curie point, the susceptibility of a ferromagnet
   (a) stays constant (b) rises without limit (c) becomes large and negative (d) falls, following a Curie–Weiss law
13. The field at the centre of a circular coil is $B$. At a point on its axis at distance equal to the radius, the field is
   (a) $B/2$ (b) $B/4$ (c) $B/(2\sqrt{2})$ (d) $B/\sqrt{2}$
14. Two solenoids of the same length have turns in the ratio 1 : 2 and carry the same current. The ratio of their interior fields is
   (a) 1 : 2 (b) 2 : 1 (c) 1 : 4 (d) 1 : 1
15. A soft iron core inside a solenoid increases the field because
   (a) it carries an extra current (b) its domains align and add a large magnetisation (c) it reduces the current (d) it makes the field non-uniform
16. Hysteresis loss in a transformer core is reduced by
   (a) increasing the frequency (b) increasing the flux density (c) using steel (d) using a soft magnetic material with a narrow loop
17. The Hall voltage in a strip is zero when
   (a) the current is perpendicular to the field (b) the current is parallel to the field (c) the material is a metal (d) the field is strong

::: note Answers and explanations — Set B
**1.** (c) — antiparallel currents repel, and the force per unit length falls as $1/d$, not $1/d^2$.
**2.** (a) — the magnetic force is always perpendicular to the velocity, so it does no work; the speed and kinetic energy are constant while the direction, and hence the velocity and momentum, change.
**3.** (d) — $T=2\pi m/qB$ contains only mass, charge and field. A faster particle simply moves on a larger circle.
**4.** (b) — $r=mv/qB$, so $r\propto m/q$; the alpha particle has $4m$ and $2e$, giving twice the radius.
**5.** (c) — with the current upward, the field circles anticlockwise seen from above. At a point due south of the wire the tangent points east.
**6.** (a) — $B\propto I/R$: doubling I doubles B and halving R doubles it again, so 4 times.
**7.** (d) — $\sin\theta=0$, so there is no magnetic force and the particle continues in a straight line at constant speed.
**8.** (b) — the pitch is $v_\parallel T$ with $v_\parallel=v\cos30^{\circ}$ and $T=2\pi m/qB$; the $\sin$ form gives the radius instead.
**9.** (a) — a diamagnet is repelled, so it drifts towards the weaker part of the field.
**10.** (c) — the moments have a preferred direction along the field, but thermal agitation prevents complete alignment, which is why the effect is weak and temperature-dependent.
**11.** (b) — $\chi=\mu_r-1=2\times10^{-4}$, a small positive value: paramagnetic. A diamagnet would be just below 1.
**12.** (d) — above $T_C$ the domains are gone and $\chi=C/(T-T_C)$ decreases as T rises.
**13.** (c) — put $x=R$: $B=B_0/(1+1)^{3/2}=B_0/(2\sqrt{2})=0.354B_0$. $B/2$ is the solenoid-end value, not this one.
**14.** (a) — $B=\mu_0NI/L$ with the same L, so $B\propto N$: 1 : 2.
**15.** (b) — the iron becomes magnetised; its aligned domains add $\mu_0M$ to $\mu_0H$, multiplying the field by $\mu_r$.
**16.** (d) — the loss per cycle is the loop area, so a narrow loop in a soft material is what matters; frequency and flux density make it worse, and steel's loop is wide.
**17.** (b) — the magnetic force $qvB\sin\theta$ is zero when the drift velocity (along the current) is parallel to the field, so no charge is pushed sideways.
:::

**Set C — Application (11 questions)**

1. A long straight wire carries 10 A. The field at a point 5 cm from the wire is
   (a) $2\times10^{-5}$ T (b) $4\times10^{-5}$ T (c) $4\times10^{-7}$ T (d) $8\times10^{-5}$ T
2. A circular coil of 50 turns and radius 10 cm carries 2 A. The field at its centre is
   (a) $6.3\times10^{-5}$ T (b) $1.3\times10^{-3}$ T (c) $6.3\times10^{-4}$ T (d) $3.1\times10^{-4}$ T
3. A solenoid 0.50 m long has 500 turns and carries 2 A. The field inside it is
   (a) $2.5\times10^{-3}$ T (b) $5.0\times10^{-3}$ T (c) $2.5\times10^{-4}$ T (d) $1.3\times10^{-3}$ T
4. An electron ($m=9.1\times10^{-31}$ kg) moves at $2\times10^{6}$ m s⁻¹ perpendicular to a field of 0.5 T. The radius of its path is
   (a) $4.6\times10^{-5}$ m (b) $1.1\times10^{-5}$ m (c) $2.3\times10^{-4}$ m (d) $2.3\times10^{-5}$ m
5. A wire 0.20 m long carrying 5 A lies perpendicular to a field of 0.40 T. The force on it is
   (a) 0.20 N (b) 0.40 N (c) 4.0 N (d) 0.04 N
6. A coil of 100 turns and area $2\times10^{-3}$ m² carries 0.5 A. Its plane is parallel to a field of 0.20 T. The torque on it is
   (a) 0.20 N m (b) $2\times10^{-3}$ N m (c) $2\times10^{-2}$ N m (d) $2\times10^{-4}$ N m
7. A silver strip 0.10 mm thick carries 2 A in a field of 1.5 T. Taking $n=5.9\times10^{28}$ m⁻³, the Hall voltage is
   (a) $3.2\times10^{-6}$ V (b) $3.2\times10^{-5}$ V (c) $6.4\times10^{-6}$ V (d) $1.6\times10^{-6}$ V
8. A magnetic material has susceptibility 599. Its relative permeability is
   (a) 599 (b) 0.998 (c) 60 (d) 600
9. A solenoid with an air core has a field of $2.0\times10^{-3}$ T. With a core of relative permeability 500, the field becomes
   (a) $4.0\times10^{-6}$ T (b) $2.0\times10^{-3}$ T (c) 1.0 T (d) 0.50 T
10. Two long parallel wires 10 cm apart carry 5 A and 10 A in the same direction. The force per metre between them is
   (a) $5\times10^{-5}$ N m⁻¹ (b) $1\times10^{-4}$ N m⁻¹ (c) $2\times10^{-4}$ N m⁻¹ (d) $1\times10^{-5}$ N m⁻¹
11. A proton moves in a circle of radius 0.10 m in a field of 0.20 T. Its speed is
   (a) $1.9\times10^{6}$ m s⁻¹ (b) $3.8\times10^{6}$ m s⁻¹ (c) $9.6\times10^{5}$ m s⁻¹ (d) $1.9\times10^{5}$ m s⁻¹

::: note Answers and explanations — Set C
**1.** (b) — $B=\dfrac{\mu_0I}{2\pi r}=\dfrac{(4\pi\times10^{-7})(10)}{2\pi(0.05)}=4.0\times10^{-5}$ T. Option (a) forgets the factor 2 in the denominator.
**2.** (c) — $B=\dfrac{\mu_0NI}{2R}=\dfrac{(4\pi\times10^{-7})(50)(2)}{2(0.10)}=6.3\times10^{-4}$ T. Option (d) halves it again by using R instead of 2R.
**3.** (a) — $n=N/L=500/0.50=1000$ m⁻¹, so $B=\mu_0nI=(4\pi\times10^{-7})(1000)(2)=2.5\times10^{-3}$ T. Option (b) uses 500 m⁻¹ without dividing by the length.
**4.** (d) — $r=\dfrac{mv}{qB}=\dfrac{(9.1\times10^{-31})(2\times10^{6})}{(1.6\times10^{-19})(0.5)}=2.3\times10^{-5}$ m.
**5.** (b) — $F=BIL=(0.40)(5)(0.20)=0.40$ N, since $\sin90^{\circ}=1$.
**6.** (c) — the plane is parallel to the field, so $\theta=90^{\circ}$ and $\tau=NIAB=(100)(0.5)(2\times10^{-3})(0.20)=2\times10^{-2}$ N m. Option (b) forgets a factor of 10.
**7.** (a) — $V_H=\dfrac{BI}{net}=\dfrac{(1.5)(2)}{(5.9\times10^{28})(1.6\times10^{-19})(10^{-4})}=3.2\times10^{-6}$ V.
**8.** (d) — $\mu_r=1+\chi=1+599=600$. Option (a) confuses $\chi$ with $\mu_r$.
**9.** (c) — $B'=\mu_rB=500(2.0\times10^{-3})=1.0$ T; the core multiplies the field, it does not divide it.
**10.** (b) — $\dfrac{F}{L}=\dfrac{\mu_0I_1I_2}{2\pi d}=\dfrac{(4\pi\times10^{-7})(50)}{2\pi(0.10)}=1.0\times10^{-4}$ N m⁻¹, attractive.
**11.** (a) — $v=\dfrac{qBr}{m}=\dfrac{(1.6\times10^{-19})(0.20)(0.10)}{1.67\times10^{-27}}=1.9\times10^{6}$ m s⁻¹. Option (b) doubles it by using the diameter.
:::
