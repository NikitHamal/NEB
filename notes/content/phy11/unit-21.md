---
subject: Physics
grade: 11
unit: 21
title: Potential, potential difference and potential energy
hours: 4
area: Electricity and Magnetism
---

The electric field tells you the force on a charge. This unit tells you the
**energy**. Because the electrostatic force is conservative — the work it does
between two points does not depend on the path taken — we can attach a single
number, the potential, to every point in space. Potential is a scalar, so it
adds by ordinary arithmetic, which makes it far easier to handle than the field
vector. Almost every practical device, from a torch cell to a cathode-ray tube,
is described in volts rather than in newtons per coulomb.

::: key Scalar, not vector
The one advantage you must exploit: potentials from several charges add as
**signed numbers**, with no angles and no components. If a question can be done
with $V$ instead of $\vec{E}$, do it with $V$.
:::

## 21.1 Potential difference, Potential due to a point charge, potential energy, electron volt

Move a charge $q$ slowly from point $A$ to point $B$ in an electric field. The
external work needed, $W_{AB}$, is the same for every path (this is what
"conservative" means). Divide it by the charge and the result depends only on
the two points:

::: definition Potential difference
The potential difference between two points is the work done per unit positive
charge in carrying it from one point to the other without acceleration:
$$ V_B - V_A = \frac{W_{AB}}{q} $$
Its SI unit is the **volt**: $1\ \text{V} = 1\ \text{J C}^{-1}$.
:::

Taking $A$ at infinity, where we agree the potential is zero, gives the
**absolute potential** at a point: the work done per unit positive charge in
bringing it from infinity to that point.

### Potential due to a point charge

::: derivation Potential at a point due to a point charge, $V = \dfrac{kQ}{r}$
We start from Coulomb's law for the force on a test charge, and we reach a
formula for the potential at a point a distance $r$ from an isolated charge $Q$.

**Setting up.** A charge $Q$ is fixed at the point $O$. The point $P$ lies a
distance $r$ from $O$. We bring a small positive test charge $q_0$ from infinity
(where we agree the potential is zero) up to $P$, moving it so slowly that it
never picks up any kinetic energy. By definition, the potential at $P$ is the
work the outside agent must do, per unit charge.

**Step 1 — Coulomb's law gives the force at every point on the way.** When the
test charge is at a distance $x$ from $O$, the field of $Q$ pushes it outward
with a force

$$ F = \frac{kQq_0}{x^{2}} $$

This force is *not* constant. It grows as $x$ gets smaller, so we cannot use
"work = force $\times$ distance". We must add up the work in tiny steps, which
means an integral.

**Step 2 — write the work done by the field over one tiny step.** Measure $x$
outward from $O$. The force acts along the direction of increasing $x$, so for a
small displacement $dx$ the work done by the field is

$$ dW_{field} = F\,dx = \frac{kQq_0}{x^{2}}\,dx $$

Over a step this small the force does not change, so here "work = force
$\times$ distance" is safe.

**Step 3 — add up all the tiny steps from infinity down to $P$.** The charge
travels from $x = \infty$ to $x = r$, and those become the limits of the
integral:

$$ W_{field} = \int_{\infty}^{r}\frac{kQq_0}{x^{2}}\,dx $$

**Step 4 — take the constants outside.** The quantities $k$, $Q$ and $q_0$ do
not change while the charge moves, so only $1/x^{2}$ stays inside:

$$ W_{field} = kQq_0\int_{\infty}^{r}\frac{dx}{x^{2}} $$

**Step 5 — carry out the integration.** The integral of $x^{-2}$ is $-x^{-1}$:

$$ W_{field} = kQq_0\left[-\frac{1}{x}\right]_{\infty}^{r} $$

**Step 6 — substitute the limits: value at the top limit minus value at the
bottom limit.**

$$ W_{field} = kQq_0\left[\left(-\frac{1}{r}\right)
- \left(-\frac{1}{\infty}\right)\right] $$

**Step 7 — the infinity term is zero.** One divided by a very large number is
as good as zero, and this is exactly why infinity is a convenient place to call
"zero potential":

$$ W_{field} = -\frac{kQq_0}{r} $$

The minus sign is correct and physical. Two positive charges repel, so the field
pushes backwards during the inward journey and does negative work.

**Step 8 — find the work done by the outside agent.** The agent pushes with a
force equal and opposite to the field's force at every instant, which is what
keeps the charge from speeding up. Equal and opposite force along the same path
means equal and opposite work:

$$ W_{ext} = -W_{field} = +\frac{kQq_0}{r} $$

**Step 9 — use the definition of potential: work per unit charge.**

$$ V = \frac{W_{ext}}{q_0} = \frac{kQq_0}{q_0\,r} $$

**Step 10 — cancel $q_0$ from top and bottom.**

$$ V = \frac{kQ}{r} = \frac{1}{4\pi\varepsilon_0}\frac{Q}{r} $$

**Result.** The absolute potential a distance $r$ from a point charge $Q$ is
$V = kQ/r$, where $k = 1/4\pi\varepsilon_0 = 9\times10^{9}\ \text{N m}^{2}
\text{ C}^{-2}$.

**What it means.** The test charge $q_0$ has cancelled out, so $V$ belongs to
the source charge $Q$ and the point $P$ alone — it describes the space around
$Q$ whether or not anything is placed there. The potential is a scalar, so it
carries the sign of $Q$ and nothing else: positive around a positive charge,
negative around a negative one.

**Conditions used.** The charge $Q$ is a point charge (or a uniformly charged
sphere, seen from outside) at rest in vacuum or air; the potential is taken as
zero at infinity; and the test charge is moved slowly, so no kinetic energy is
gained or lost.
:::

::: tip The examiner is looking for
1. A statement of the definition being used: $V = W_{ext}/q_0$, with zero
   potential at infinity.
2. Coulomb's law written for a general distance $x$, with a clear reason for
   integrating (the force varies).
3. The integral with the correct limits $\infty$ to $r$.
4. The integration and substitution of limits, including $1/\infty = 0$.
5. The step from $W_{field}$ to $W_{ext}$ (opposite sign), and the cancellation
   of $q_0$ giving $V = kQ/r$.
:::

Note carefully: $V \propto 1/r$ while $E \propto 1/r^{2}$. The potential is
**positive** near a positive charge and **negative** near a negative charge, and
it carries that sign into every sum. For several charges,

$$ V = \frac{1}{4\pi\varepsilon_0}\left(\frac{q_1}{r_1} + \frac{q_2}{r_2}
+ \frac{q_3}{r_3} + \cdots\right) $$

which is an ordinary algebraic sum — no resolution into components.

```figure caption="For a point charge, $V \propto 1/r$ falls off more slowly than $E \propto 1/r^2$. Both are taken as zero at infinity."
import numpy as np, matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 2, figsize=(5.1, 2.5))
r = np.linspace(0.35, 3.0, 300)
axes[0].plot(r, 1.0/r, color=ACCENT, lw=2.0)
axes[0].set_ylabel('potential  $V$')
axes[0].set_title(r'$V = kQ/r$', fontsize=9.5, color=INK)
axes[1].plot(r, 1.0/r**2, color='#d9534f', lw=2.0)
axes[1].set_ylabel('field  $E$')
axes[1].set_title(r'$E = kQ/r^{2}$', fontsize=9.5, color=INK)
for ax in axes:
    ax.set_xlabel('distance  $r$')
    ax.set_xlim(0, 3.0); ax.set_ylim(0, None)
    ax.set_xticks([]); ax.set_yticks([])
    ax.spines[['top', 'right']].set_visible(False)
    ax.grid(True, alpha=.45)
fig.tight_layout()
```

### Electric potential energy

The **potential energy** of a charge $q$ at a point where the potential is $V$
is simply $U = qV$ — the work stored in putting it there. For two point charges
a distance $r$ apart,

$$ U = \frac{1}{4\pi\varepsilon_0}\frac{q_1q_2}{r} $$

This is positive for like charges (you had to push them together, energy is
stored) and negative for unlike charges (the field did the work for you, so you
must supply energy to separate them). For a system of three charges, add the
energy of each **pair**:

$$ U = k\left(\frac{q_1q_2}{r_{12}} + \frac{q_2q_3}{r_{23}} + \frac{q_1q_3}{r_{13}}\right) $$

| | Potential $V$ | Potential energy $U$ |
|---|---|---|
| Belongs to | a point in space | a charge, or a system of charges |
| Defining relation | $V = W/q$ | $U = qV$ |
| SI unit | volt (J C⁻¹) | joule |
| Point charge | $kQ/r$ | $kq_1q_2/r$ (a pair) |
| Type | scalar | scalar |

### Potential of a charged conducting sphere

A conducting sphere of radius $R$ carrying charge $Q$ behaves outside itself
exactly like a point charge, so for $r \geq R$ the potential is $V = kQ/r$.
Inside the metal the field is zero, so by $E = -dV/dr$ the potential cannot
change: the whole sphere, surface and interior alike, sits at the single value

$$ V_{inside} = V_{surface} = \frac{kQ}{R} $$

Two useful consequences follow. First, for a given charge a **small** sphere
reaches a much higher potential than a large one, which is why charge sprayed
onto a small conductor leaks away readily. Second, if two charged spheres are
joined by a wire, charge flows until their potentials — not their charges — are
equal. The smaller sphere ends with less charge but a larger surface density,
and therefore a stronger surface field. This is the physics behind the pointed
lightning conductors on the tall temples and towers of the Kathmandu valley:
the sharp tip has a very small radius of curvature, so the field there becomes
large enough to ionise the air and quietly discharge the cloud.

### The electron volt

Charges on the atomic scale are tiny, so the joule is a clumsy unit.

::: definition Electron volt
One electron volt is the kinetic energy gained by an electron accelerated
through a potential difference of one volt:
$$ 1\ \text{eV} = 1.6\times10^{-19}\ \text{C}\times1\ \text{V}
= 1.6\times10^{-19}\ \text{J} $$
:::

It is a unit of **energy**, not of potential. Useful multiples: 1 keV = 10³ eV,
1 MeV = 10⁶ eV. You will meet it again in nuclear physics.

::: caution Potential is not potential energy
"The potential at $P$ is 100 J" is meaningless. Potential is measured in volts,
potential energy in joules, and they are linked by $U = qV$. Likewise the
electron volt is an energy, so never write "a p.d. of 5 eV".
:::

::: example Worked example 21.1
**Problem.** Three charges of $+2\ \mu\text{C}$ each are placed at the corners of
an equilateral triangle of side $10\ \text{cm}$. Find (a) the potential at the
centroid and (b) the potential energy of the system.

**Solution.**

(a) The centroid is $r = a/\sqrt{3} = 0.10/1.732 = 0.0577\ \text{m}$ from each
charge. Potentials add algebraically:

$$ V = 3\times\frac{kq}{r} = 3\times\frac{9\times10^{9}\times2\times10^{-6}}{0.0577}
= 9.35\times10^{5}\ \text{V} $$

(b) There are three identical pairs, each a distance $a = 0.10\ \text{m}$ apart:

$$ U = 3\times\frac{kq^{2}}{a}
= 3\times\frac{9\times10^{9}\times(2\times10^{-6})^{2}}{0.10} = 3\times0.36 = 1.08\ \text{J} $$
:::

::: example Worked example 21.2
**Problem.** Charges $+4\ \mu\text{C}$ and $-4\ \mu\text{C}$ are fixed at
$A(0,0)$ and $B(0.4\ \text{m}, 0)$. Find (a) the potential at $P(0, 0.3\ \text{m})$
and (b) the work needed to bring a charge of $+2\ \mu\text{C}$ from infinity to $P$.

**Solution.**

(a) $AP = 0.3\ \text{m}$ and $BP = \sqrt{0.4^{2}+0.3^{2}} = 0.5\ \text{m}$, so

$$ V = k q\left(\frac{1}{0.3} - \frac{1}{0.5}\right)
= 9\times10^{9}\times4\times10^{-6}\times(3.333 - 2.000) = 4.8\times10^{4}\ \text{V} $$

(b) $W = qV = 2\times10^{-6}\times4.8\times10^{4} = 9.6\times10^{-2}\ \text{J}
= 0.096\ \text{J}$.
:::

::: example Worked example 21.3
**Problem.** An electron starting from rest is accelerated through a potential
difference of $400\ \text{V}$. Find its kinetic energy in eV and in joules, and
its final speed. Take $m_e = 9.1\times10^{-31}\ \text{kg}$.

**Solution.** The work done on the electron is $W = eV$, so its kinetic energy
is $400\ \text{eV}$, that is

$$ KE = 400\times1.6\times10^{-19} = 6.4\times10^{-17}\ \text{J} $$

Then from $KE = \tfrac{1}{2}m_ev^{2}$,

$$ v = \sqrt{\frac{2\times6.4\times10^{-17}}{9.1\times10^{-31}}}
= \sqrt{1.41\times10^{14}} = 1.19\times10^{7}\ \text{m s}^{-1} $$
:::

## 21.2 Equipotential lines and surfaces

::: definition Equipotential surface
An equipotential surface is a surface on which the electric potential has the
same value at every point. Its intersection with the plane of a diagram is an
equipotential line.
:::

Their properties follow directly from $W = q(V_A - V_B)$:

- **No work is done** in moving a charge between two points of the same
  equipotential surface, because $V_A - V_B = 0$. This is true for *any* path on
  the surface.
- Equipotential surfaces are **always perpendicular to field lines**. If $\vec{E}$
  had a component along the surface, moving a charge along the surface would do
  work, contradicting the previous point.
- Two equipotential surfaces **never intersect**, since a point cannot have two
  potentials at once.
- Where the surfaces are **closely spaced the field is strong**, because the same
  drop in $V$ occurs over a shorter distance.
- The **surface of any charged conductor in equilibrium is an equipotential**, and
  so is its whole interior volume, since $E = 0$ inside.

The first two properties are the ones examiners ask you to *prove*, so here they
are in full.

::: derivation No work is done in moving a charge over an equipotential surface
We start from the definition of potential difference and reach two results: the
work is zero for any path on the surface, and the field must meet the surface at
a right angle.

**Setting up.** Let $A$ and $B$ be any two points lying on the same equipotential
surface, with potentials $V_A$ and $V_B$. A charge $q$ is carried from $A$ to $B$
along any path that stays on the surface.

**Step 1 — write the work in terms of potential difference.** Potential
difference is defined as work done per unit charge, so the work done against the
field in taking $q$ from $A$ to $B$ is

$$ W = q\,(V_B - V_A) $$

**Step 2 — use the definition of an equipotential surface.** Every point of the
surface has the same potential, and $A$ and $B$ are both on it, so

$$ V_A = V_B $$

**Step 3 — substitute this into the expression for the work.**

$$ W = q\,(V_A - V_A) $$

**Step 4 — the bracket is zero, so the work is zero.**

$$ W = q \times 0 = 0 $$

Nothing in Steps 1 to 4 mentioned the shape of the path, so the answer is zero
for *every* path on the surface, long or short, straight or curved.

**Step 5 — now write the same work the other way, using force and
displacement.** The field exerts a force $qE$ on the charge. If the charge is
moved a distance $s$ along the surface and the angle between $\vec{E}$ and that
displacement is $\theta$, then

$$ W = qEs\cos\theta $$

**Step 6 — set this equal to zero, the answer from Step 4.**

$$ qEs\cos\theta = 0 $$

**Step 7 — decide which factor is the zero one.** We have a real charge
($q \neq 0$), a real field ($E \neq 0$) and a real displacement ($s \neq 0$), so
the only factor left that can vanish is the cosine:

$$ \cos\theta = 0 $$

**Step 8 — solve for the angle.**

$$ \theta = 90^{\circ} $$

**Result.** No work is done in moving a charge between any two points of an
equipotential surface, $W = 0$; and the electric field is everywhere
perpendicular to the equipotential surface.

**What it means.** Moving along an equipotential is like walking around a hill
at a fixed height — you neither climb nor descend, so gravity takes and gives
nothing. The field, like gravity on the hillside, points straight "downhill",
at right angles to the contour.

**Conditions used.** The charges producing the field are at rest (an
electrostatic field), and the charge $q$ is moved slowly, so no kinetic energy
is gained. In Step 7 the field must be non-zero; where $E = 0$, as inside a
conductor, the angle is simply undefined and the work is zero anyway.
:::

The shape follows the source: concentric spheres around a point charge, parallel
planes in the uniform field between charged plates, and coaxial cylinders around
a long charged wire.

```figure caption="Equipotentials (dashed) and field lines (solid) around a positive point charge. Equal steps of $20\ \text{V}$ lie further and further apart because $V \propto 1/r$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.4, 3.2))
for th in np.arange(22.5, 360, 45):
    a = np.radians(th)
    ax.annotate('', xy=(3.25*np.cos(a), 3.25*np.sin(a)),
                xytext=(0.30*np.cos(a), 0.30*np.sin(a)),
                arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=0.95,
                                shrinkA=0, shrinkB=0, mutation_scale=8), zorder=2)
for rad, lab in [(1.0, '60 V'), (1.5, '40 V'), (2.0, '30 V'), (3.0, '20 V')]:
    ax.add_patch(plt.Circle((0, 0), rad, fill=False, ec='#d9534f', lw=1.3,
                            ls=(0, (4, 2.5)), zorder=3))
    ax.text(0, rad + 0.18, lab, color='#d9534f', fontsize=8.2, zorder=4,
            ha='center', va='center',
            bbox=dict(facecolor='white', edgecolor='none', pad=1.2))
ax.add_patch(plt.Circle((0, 0), 0.22, color='#d9534f', zorder=5))
ax.text(0, 0, '+', color='white', ha='center', va='center', fontsize=11, zorder=6)
ax.set_xlim(-3.5, 3.5); ax.set_ylim(-3.5, 3.5)
ax.set_aspect('equal'); ax.axis('off')
```

```figure caption="Uniform field between parallel plates. The equipotentials are flat planes parallel to the plates, and $E = V/d$ is the same everywhere between them."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8, 2.6))
d = 2.4
ax.plot([0, 0], [-1.0, 1.0], color='#d9534f', lw=3.4, solid_capstyle='butt')
ax.plot([d, d], [-1.0, 1.0], color=ACCENT, lw=3.4, solid_capstyle='butt')
for y in (-0.75, -0.25, 0.25, 0.75):
    ax.annotate('', xy=(d - 0.10, y), xytext=(0.10, y),
                arrowprops=dict(arrowstyle='-|>', color='#2e8b57', lw=1.2,
                                shrinkA=0, shrinkB=0, mutation_scale=10))
for x, lab in [(0.6, '150 V'), (1.2, '100 V'), (1.8, '50 V')]:
    ax.plot([x, x], [-1.0, 1.0], color=MUTED, lw=1.0, ls=(0, (3, 2.5)))
    ax.text(x, 1.10, lab, color=MUTED, fontsize=8.0, ha='center',
            va='bottom', rotation=90)
ax.text(-0.10, -1.22, '$+200$ V', color='#d9534f', fontsize=9, ha='center')
ax.text(d + 0.10, -1.22, '$0$ V', color=ACCENT, fontsize=9, ha='center')
ax.annotate('', xy=(d, -1.55), xytext=(0, -1.55),
            arrowprops=dict(arrowstyle='<->', color=INK, lw=0.9,
                            shrinkA=0, shrinkB=0, mutation_scale=8))
ax.text(d/2, -1.50, '$d$', color=INK, fontsize=10, ha='center')
ax.text(d/2, 0.0, r'$\vec{E}$', color='#2e8b57', fontsize=10, ha='center',
        va='center', bbox=dict(facecolor='white', edgecolor='none', pad=1.0))
ax.set_xlim(-0.75, d + 0.75); ax.set_ylim(-1.95, 2.25)
ax.set_aspect('equal'); ax.axis('off')
```

```figure caption="Equipotential contours of a dipole. The line midway between the charges is the $V = 0$ equipotential, on which no work is done."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0, 2.8))
n = 400
X, Y = np.meshgrid(np.linspace(-2.4, 2.4, n), np.linspace(-1.35, 1.35, n))
r1 = np.sqrt((X + 0.75)**2 + Y**2 + 0.004)
r2 = np.sqrt((X - 0.75)**2 + Y**2 + 0.004)
V = 1.0/r1 - 1.0/r2
lv = [-2.4, -1.2, -0.6, -0.25, 0.0, 0.25, 0.6, 1.2, 2.4]
cs = ax.contour(X, Y, V, levels=lv, colors=['#d9534f'], linewidths=1.0,
                linestyles='dashed')
ax.axvline(0, color=INK, lw=1.2)
ax.add_patch(plt.Circle((-0.75, 0), 0.13, color='#d9534f', zorder=5))
ax.add_patch(plt.Circle((0.75, 0), 0.13, color=ACCENT, zorder=5))
ax.text(-0.75, 0, '+', color='white', ha='center', va='center', fontsize=10, zorder=6)
ax.text(0.75, 0, '-', color='white', ha='center', va='center', fontsize=12, zorder=6)
ax.text(0.06, 1.12, '$V=0$', color=INK, fontsize=9)
ax.set_xlim(-2.4, 2.4); ax.set_ylim(-1.35, 1.35)
ax.set_aspect('equal'); ax.axis('off')
```

## 21.3 Potential gradient

The rate at which potential changes with distance is the **potential gradient**.
It is directly related to the field.

::: derivation Field is minus the potential gradient, and hence $E = V/d$
We start from the definition of potential difference as work per unit charge and
reach a relation that connects the field at a point to how fast the potential is
changing there. We then apply it to the uniform field between two plates.

**Setting up.** Take two nearby points $A$ and $B$ on a field line, a small
distance $dx$ apart, with $B$ further along the direction of $\vec{E}$. Let the
potential be $V$ at $A$ and $V + dV$ at $B$. A positive charge $q$ is moved from
$A$ to $B$. Because $dx$ is small, the field is effectively constant over the
journey.

**Step 1 — write the force the field exerts on the charge.** From the definition
of electric field strength, force = charge $\times$ field:

$$ F = qE $$

**Step 2 — work out the work done by the field over this small step.** The force
and the displacement point the same way, so work = force $\times$ distance:

$$ dW_{field} = qE\,dx $$

**Step 3 — write the same work again, this time from the definition of
potential difference.** Work done by the field = charge $\times$ (potential at
the start $-$ potential at the end):

$$ dW_{field} = q\left[V - (V + dV)\right] $$

**Step 4 — simplify the bracket.** The $V$ and $+V$ cancel and only $-dV$
survives:

$$ dW_{field} = -q\,dV $$

**Step 5 — the two expressions describe the same work, so set them equal.**

$$ qE\,dx = -q\,dV $$

**Step 6 — cancel $q$ from both sides.** It is a real, non-zero charge, so this
is allowed — and it shows the result does not depend on what we moved:

$$ E\,dx = -dV $$

**Step 7 — divide both sides by $dx$.**

$$ E = -\frac{dV}{dx} $$

This is the general result. The rest applies it to parallel plates.

**Step 8 — say what "uniform field" means for this equation.** Between two large
parallel plates the field $E$ has the same value everywhere, so $dV/dx$ is a
constant. A constant rate of change means the potential falls **linearly** with
distance, and the small changes $dV$ and $dx$ may be replaced by the total
changes measured across the whole gap:

$$ E = -\frac{\Delta V}{\Delta x} $$

**Step 9 — put in the values for the gap.** Let the plates be a distance $d$
apart, the positive plate at potential $V$ and the earthed plate at $0$. Going
across the gap in the direction of the field, the potential changes from $V$ to
$0$, so $\Delta V = 0 - V = -V$ and $\Delta x = d$:

$$ E = -\frac{(-V)}{d} $$

**Step 10 — cancel the two minus signs.**

$$ E = \frac{V}{d} $$

**Result.** The field at a point equals minus the potential gradient there,
$E = -dV/dx$; and for the uniform field between parallel plates a distance $d$
apart with potential difference $V$, the magnitude is $E = V/d$.

**What it means.** The minus sign says $\vec{E}$ points the way $V$ *decreases*
fastest, so a positive charge released from rest always slides "downhill" in
potential. It also explains the unit: $\text{V m}^{-1}$ and $\text{N C}^{-1}$
are the same thing. Closely packed equipotentials mean a steep gradient, and
therefore a strong field.

**Conditions used.** Static charges; $dx$ small enough that $E$ is constant over
it; and for $E = V/d$ the field must be uniform, which means large plates and a
small separation so that the edge effects can be ignored.
:::

::: tip The examiner is looking for
1. The two independent expressions for the same work: $dW = qE\,dx$ from force
   $\times$ distance, and $dW = -q\,dV$ from the definition of potential
   difference.
2. Equating them and cancelling $q$.
3. The final form $E = -dV/dx$, **with the minus sign** and a sentence saying
   what it means.
4. For the $V/d$ part: a clear statement that the field is uniform, so the
   gradient is constant and $dV/dx$ becomes $-V/d$.
:::

For the **uniform** field between two parallel plates a distance $d$ apart held
at a potential difference $V$,

$$ E = \frac{V}{d} $$

is the working formula for every parallel-plate and cathode-ray-tube
problem. For a point charge you can check the general relation directly:
$V = kQ/r$ gives $-dV/dr = kQ/r^{2} = E$, as it must.

The same relation run backwards recovers the potential from the field: since
$dV = -E\,dx$, the **change in potential between two points is minus the area
under the $E$–$x$ graph** between them. For a charged conducting sphere, for
instance, $E = 0$ inside contributes no area, so $V$ stays flat at $kQ/R$ right
up to the surface and only then begins to fall.

| Arrangement | Shape of equipotential surfaces | Field |
|---|---|---|
| Isolated point charge | concentric spheres | radial, $kQ/r^{2}$ |
| Long charged wire | coaxial cylinders | radial, $\lambda/2\pi\varepsilon_0 r$ |
| Parallel charged plates | parallel planes | uniform, $V/d$ |
| Any charged conductor | its own surface, and every interior point | zero inside |

::: tip Reading a graph of $V$ against $r$
$E$ is minus the **slope** of the $V$–$r$ graph. Where the graph is flat
(inside a charged hollow conductor, where $V$ is constant) the field is zero;
where the graph is steep, the field is large.
:::

::: example Worked example 21.4
**Problem.** Two parallel plates $2\ \text{cm}$ apart are connected to a
$200\ \text{V}$ supply. Find (a) the field between them, (b) the force on a
charge of $5\ \text{nC}$ placed between them, and (c) the work done in moving
that charge from one plate to the other.

**Solution.**

(a) $E = \dfrac{V}{d} = \dfrac{200}{0.02} = 1.0\times10^{4}\ \text{V m}^{-1}$.

(b) $F = qE = 5\times10^{-9}\times1.0\times10^{4} = 5\times10^{-5}\ \text{N}$.

(c) $W = qV = 5\times10^{-9}\times200 = 1.0\times10^{-6}\ \text{J}$.

Check: $W = Fd = 5\times10^{-5}\times0.02 = 1.0\times10^{-6}\ \text{J}$. The two
routes agree, as they must in a uniform field.
:::

## Chapter summary

- Potential difference $V_B - V_A = W_{AB}/q$, in volts (J C⁻¹); absolute
  potential takes $V = 0$ at infinity.
- Point charge: $V = kQ/r$ — a **scalar** that carries the sign of the charge, so
  potentials add algebraically.
- Potential energy: $U = qV$; for a pair of charges $U = kq_1q_2/r$; for a system
  add over all pairs.
- $1\ \text{eV} = 1.6\times10^{-19}\ \text{J}$ — a unit of energy, not of
  potential.
- An equipotential surface has constant $V$: no work is done moving a charge on
  it, and it is everywhere perpendicular to the field lines.
- Conductors in equilibrium are equipotential volumes; field lines meet their
  surfaces at right angles.
- $E = -dV/dx$: the field is the negative potential gradient, measured in
  V m⁻¹ = N C⁻¹. For parallel plates, $E = V/d$.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The SI unit of electric potential is <span class="marks">[1]</span>
   (a) J C (b) J C⁻¹ (c) N C⁻¹ (d) C V⁻¹
2. The work done in moving a charge between two points of an equipotential
   surface is <span class="marks">[1]</span>
   (a) $qV$ (b) infinite (c) zero (d) $q/V$
3. One electron volt is equal to <span class="marks">[1]</span>
   (a) $1.6\times10^{-19}\ \text{J}$ (b) $1.6\times10^{-19}\ \text{V}$
   (c) $9\times10^{9}\ \text{J}$ (d) $1\ \text{J}$
4. The electric field and the potential gradient are related by <span class="marks">[1]</span>
   (a) $E = dV/dx$ (b) $E = -dV/dx$ (c) $V = -dE/dx$ (d) $E = -V x$
5. At the midpoint of the line joining two equal and opposite charges, the
   potential and the field are respectively <span class="marks">[1]</span>
   (a) zero and zero (b) zero and non-zero (c) non-zero and zero (d) both non-zero

::: note Answers to Group A
**1.** (b) — $V = W/q$, so joule per coulomb.
**2.** (c) — $V_A - V_B = 0$, hence $W = q(V_A - V_B) = 0$.
**3.** (a) — $1\ \text{eV} = e\times1\ \text{V}$.
**4.** (b) — the field points down the potential gradient.
**5.** (b) — the two potentials cancel, but the two fields point the same way and add.
:::

**Group B — Short answer (5 marks each)**

1. Define electric potential and potential difference. Derive an expression for
   the potential at a distance $r$ from a point charge $Q$. <span class="marks">[5]</span>
2. What is an equipotential surface? State four of its properties and show that
   it must be perpendicular to the electric field. <span class="marks">[5]</span>
3. Establish the relation $E = -dV/dx$ between electric field and potential
   gradient, and hence show that $E = V/d$ for a parallel-plate arrangement. <span class="marks">[5]</span>
4. Calculate the work done in moving a charge of $2\ \mu\text{C}$ from a point
   $10\ \text{cm}$ away from a charge of $+3\ \mu\text{C}$ to a point
   $5\ \text{cm}$ away from it. <span class="marks">[5]</span>
5. An electron initially at rest is accelerated through a potential difference of
   $1000\ \text{V}$. Find its final kinetic energy in joules and its speed. <span class="marks">[5]</span>

::: note Answers to Group B
**4.** $V_1 = \dfrac{9\times10^{9}\times3\times10^{-6}}{0.10} = 2.7\times10^{5}\ \text{V}$
and $V_2 = \dfrac{9\times10^{9}\times3\times10^{-6}}{0.05} = 5.4\times10^{5}\ \text{V}$.
The work done by the external agent is
$W = q(V_2 - V_1) = 2\times10^{-6}\times2.7\times10^{5} = 0.54\ \text{J}$.

**5.** $KE = eV = 1.6\times10^{-19}\times1000 = 1.6\times10^{-16}\ \text{J}$
(that is $1\ \text{keV}$). Then
$v = \sqrt{2\times1.6\times10^{-16}/9.1\times10^{-31}} = \sqrt{3.52\times10^{14}}
= 1.88\times10^{7}\ \text{m s}^{-1}$.
:::

**Group C — Long answer (8 marks each)**

1. (a) Define absolute electric potential and derive $V = kQ/r$ for a point
   charge. <span class="marks">[4]</span>
   (b) Define an equipotential surface, prove that no work is done in moving a
   charge over it, and deduce the relation $E = -dV/dr$. <span class="marks">[4]</span>
2. Two point charges $+5\ \mu\text{C}$ and $-3\ \mu\text{C}$ are placed
   $0.4\ \text{m}$ apart in air. Calculate (a) the potential at the midpoint of
   the line joining them, (b) the potential energy of the system, and (c) the
   work required to bring a charge of $+2\ \mu\text{C}$ from infinity to that
   midpoint. <span class="marks">[8]</span>

::: note Answer to Group C question 2
Each charge is $0.2\ \text{m}$ from the midpoint.

(a) $V = 9\times10^{9}\left(\dfrac{5\times10^{-6}}{0.2} - \dfrac{3\times10^{-6}}{0.2}\right)
= 9\times10^{9}\times1\times10^{-5} = 9\times10^{4}\ \text{V}$.

(b) $U = \dfrac{9\times10^{9}\times5\times10^{-6}\times(-3\times10^{-6})}{0.4}
= -0.3375\ \text{J}$. It is negative because the charges attract, so external
work would be needed to pull them apart.

(c) $W = qV = 2\times10^{-6}\times9\times10^{4} = 0.18\ \text{J}$.
:::
