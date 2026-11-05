---
subject: Physics
grade: CEE
unit: 17
title: Electrostatics and Capacitors
hours: 4
area: Electrostatics and Capacitors
---

Electrostatics is the physics of charge at rest: how charge is transferred from one
body to another, how it pushes and pulls other charge, and what it does to the space
around it. The area carries **4 of the 50 Physics questions** (official MEC
weightage), and this one chapter supplies all four — the heaviest single chapter in
the paper. The marks divide almost evenly between Coulomb's law and fields, potential
and Gauss's law, and capacitors, so none of the three can be left out.

::: key What the paper asks from this chapter
- Quantisation $q = ne$; charging by friction, conduction and induction; what a gold-leaf electroscope shows.
- Coulomb's law in vacuum and in a medium, and the net force on one charge due to several others.
- The zero-field point on a line of two charges, and the charge that holds a three-charge system in equilibrium.
- Field of a point charge and of a charged conducting sphere (zero inside); the rules field lines obey.
- Potential $V = kq/r$, potential energy $U = qV = kq_1q_2/r$, and $E = -dV/dr$.
- The three Gauss results: sphere $kQ/r^2$, line $\lambda/(2\pi\varepsilon_0r)$, sheet $\sigma/(2\varepsilon_0)$.
- $C = Q/V$; $C = \varepsilon_0A/d$ and $K\varepsilon_0A/d$; series and parallel; $U = \frac12CV^2$; $u = \frac12\varepsilon_0E^2$.
- The dielectric table: battery connected against battery removed.
:::

## 17.1 Electric charge, electrostatic induction and Coulomb's law

### Charge and its four properties

There are two kinds of electric charge. **Like charges repel, unlike charges
attract.** A body is charged when it gains or loses electrons; protons do not move
from one body to another in ordinary charging.

```photo id="phy11/electroscope" caption="A gold-leaf electroscope: the brass disc on top, the rod, and the leaves hanging inside the glass case." width="45"
```


1. **Quantisation.** Every charge is a whole-number multiple of the elementary
   charge: $q = ne$, with $e = 1.6\times10^{-19}$ C. So one coulomb is the charge of
   $1/1.6\times10^{-19} = 6.25\times10^{18}$ electrons. An electron carries $-e$, a
   proton $+e$.
2. **Conservation.** Charge is neither created nor destroyed. When a glass rod is
   rubbed with silk, the rod loses electrons and becomes positive; the silk gains
   exactly the same number and becomes negative. The total charge stays zero.
3. **Additivity.** Total charge is the algebraic sum of the individual charges — it
   is a scalar, although we speak of "positive" and "negative" charge.
4. **Invariance.** Charge on a body does not change with its speed.

A **conductor** (metals, graphite, salt solution) has free electrons that move
through it easily. An **insulator** (glass, rubber, dry wood, plastic) holds its
electrons tightly; charge placed on it stays where it was put.

### Three ways to charge a body

| Method | What is done | Charge acquired |
|---|---|---|
| Friction | two different insulators are rubbed together | equal and opposite charges on the two |
| Conduction | the body is touched with a charged conductor | same sign as the charging body |
| Induction | a charged body is held near, the body is earthed, then separated | opposite sign to the inducing charge |

**Induction** is the one the paper tests. Bring a positively charged rod near an
uncharged metal sphere (no contact). Electrons in the metal are attracted towards the
rod, so the near side becomes negative and the far side is left positive. The sphere
as a whole is still neutral. If it is now earthed — even by a finger — electrons flow
from the earth to neutralise the far side. Break the earth connection first, then
remove the rod: the sphere is left with a net **negative** charge, opposite to the
rod.

::: caution Earthing order matters
If you remove the rod before removing the earth connection, the separated charge
simply flows back and the sphere ends up neutral. The sequence is: rod near → earth →
remove earth → remove rod.
:::

### The gold-leaf electroscope

A metal rod carries a brass disc (or cap) at the top and two thin gold leaves at the
bottom, all inside a glass case. The case is earthed (often by a metal coating) so
that outside charges cannot interfere.

- **Charged by conduction:** touch the cap with a charged rod. Charge spreads over
  the cap, rod and leaves; both leaves get the *same* sign and repel, so they
  diverge. The electroscope now has the same sign as the rod.
- **Charged by induction:** hold a charged rod near the cap without touching. The cap
  gets the opposite charge and the leaves the same charge as the rod, so the leaves
  diverge. Touch the cap briefly (earth it): the leaves collapse. Remove the finger,
  then the rod: the leaves diverge again, now carrying the *opposite* charge to the
  rod.
- **Testing the sign of an unknown charge:** first charge the electroscope with a
  known sign. Bring the unknown body near the cap. If the divergence *increases*, the
  body has the same sign; if it *decreases*, the opposite sign.
- **Testing whether a body is charged:** bring it near an uncharged electroscope. Any
  divergence means it is charged.

The divergence measures neither the charge nor the potential exactly — it is a
detector, not a meter.

### Coulomb's law

The force between two point charges at rest in vacuum is proportional to the product
of the charges and inversely proportional to the square of the distance between them:

$$ F = \frac{1}{4\pi\varepsilon_0}\frac{q_1q_2}{r^2} $$

where $q_1, q_2$ are in coulomb, $r$ in metre, $F$ in newton, and
$\varepsilon_0 = 8.85\times10^{-12}$ C² N⁻¹ m⁻² is the permittivity of free space. The
constant $k = 1/(4\pi\varepsilon_0) = 9\times10^{9}$ N m² C⁻².

In vector form, the force on $q_1$ due to $q_2$ is
$\vec F_{12} = k\,q_1q_2\,\hat r_{12}/r^2$, where $\hat r_{12}$ points from $q_2$ to
$q_1$. A positive product gives a force along $\hat r_{12}$ (repulsion); a negative
product reverses it (attraction).

**In a medium** of dielectric constant (relative permittivity) $K$, the force is
reduced:

$$ F_{\text{medium}} = \frac{F_{\text{vacuum}}}{K} = \frac{1}{4\pi\varepsilon_0K}\frac{q_1q_2}{r^2} $$

For water $K \approx 80$, so two charges attract or repel 80 times more weakly in
water than in air.

The law holds for **point charges**, for charges at rest, and for distances large
compared with the size of the bodies. For spheres, $r$ is measured between centres.

**Superposition.** The force between two charges is not changed by the presence of a
third. The net force on a charge is the vector sum of the forces due to each of the
others, taken one at a time.

| Feature | Electrostatic force | Gravitational force |
|---|---|---|
| Acts between | charges | masses |
| Direction | attract or repel | always attract |
| Formula | $kq_1q_2/r^2$ | $Gm_1m_2/r^2$ |
| Relative strength (two protons) | about $10^{36}$ times stronger | weakest force |
| Effect of medium | reduced by $K$ | unchanged |
| Shielding | can be shielded | cannot be shielded |

### Three charges in a line

Two fixed charges $q_1$ and $q_2$ a distance $L$ apart create a point where the net
field is zero — the **null point**. Its position follows from equating the two field
magnitudes.

- If $q_1$ and $q_2$ have the **same sign**, the null point lies **between** them,
  nearer the smaller charge, at distance $x$ from $q_1$ given by
  $x = L/(1+\sqrt{q_2/q_1})$.
- If they have **opposite signs**, the null point lies **outside** the pair, on the
  side of the smaller charge.

For the whole three-charge system to be in equilibrium, the third charge must be
opposite in sign to the other two, and its magnitude is fixed by the condition that
the net force on *every* charge is zero.

::: example Worked example 17.1 — the null point and a balanced system
**Problem.** Charges $+4\ \mu\text{C}$ and $+1\ \mu\text{C}$ are fixed 30 cm apart in
air. (a) Where on the line can a third charge be placed so that the force on it is
zero? (b) What charge there would keep all three charges in equilibrium?

**Solution.** (a) The point is between them, nearer the $1\ \mu\text{C}$ charge. Let
$x$ be its distance from the $4\ \mu\text{C}$ charge:
$$ \frac{4}{x^2} = \frac{1}{(0.30-x)^2} \Rightarrow \frac{2}{x} = \frac{1}{0.30-x} \Rightarrow x = 0.20\ \text{m} $$
So the point is 20 cm from the $4\ \mu\text{C}$ charge and 10 cm from the
$1\ \mu\text{C}$ charge.

(b) The third charge $q$ must be negative. For the $1\ \mu\text{C}$ charge to be in
equilibrium, the pull from $q$ at 10 cm must balance the push from the
$4\ \mu\text{C}$ charge at 30 cm:
$$ \frac{k(4)(1)}{(0.30)^2} = \frac{k|q|(1)}{(0.10)^2} \Rightarrow |q| = \frac{4}{9}\ \mu\text{C} \approx 0.44\ \mu\text{C} $$
So $q = -0.44\ \mu\text{C}$. (Check the $4\ \mu\text{C}$ charge: the forces are
$k(4)(1)/0.30^2$ and $k(4)(4/9)/0.20^2$, both equal to $44.4k$.)
:::

### Charges at the corners of a triangle

Three equal charges $q$ at the corners of an equilateral triangle of side $a$: the
force on any one charge is the vector sum of two forces of magnitude $kq^2/a^2$ at
60°, so

$$ F = 2\frac{kq^2}{a^2}\cos30^{\circ} = \sqrt{3}\,\frac{kq^2}{a^2} $$

directed away from the centre of the triangle. To hold the system in equilibrium, a
charge $q' = -q/\sqrt{3}$ is placed at the centre. For a square with equal charges at
the corners, the field at the centre is zero by symmetry, but the potential there is
not.

## 17.2 Electric field, potential and Gauss's law

### Electric field

The **electric field** at a point is the force per unit positive charge placed there:

$$ \vec E = \frac{\vec F}{q_0}, \qquad E = \frac{F}{q_0} $$

It is a vector, pointing the way a positive test charge would be pushed. The unit is
N C⁻¹, which is the same as V m⁻¹. For a point charge,

$$ E = \frac{1}{4\pi\varepsilon_0}\frac{q}{r^2} = \frac{kq}{r^2} $$

directed radially outward for positive $q$ and inward for negative $q$. Fields from
several charges add as vectors.

Between two parallel plates with potential difference $V$ a distance $d$ apart, the
field is uniform: $E = V/d$, directed from the positive plate to the negative one.

```figure caption="Field lines. (a) A positive charge: lines leave it. (b) A negative charge: lines end on it. (c) An electric dipole: lines leave the positive charge and end on the negative one; the density shows where the field is strong."
import numpy as np, matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 3, figsize=(5.1, 2.25))
for ax in axes:
    ax.set_aspect('equal'); ax.axis('off')
    ax.set_xlim(-1.3, 1.3); ax.set_ylim(-1.15, 1.15)

def charge(ax, x, y, s, col):
    ax.plot(x, y, 'o', color=col, ms=11, zorder=6)
    ax.text(x, y, s, color='white', ha='center', va='center', fontsize=9.5, zorder=7)

for th in np.linspace(0, 2*np.pi, 10)[:-1]:
    axes[0].annotate('', xy=(1.10*np.cos(th), 1.10*np.sin(th)),
                     xytext=(0.26*np.cos(th), 0.26*np.sin(th)),
                     arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.0, mutation_scale=7))
charge(axes[0], 0, 0, '+', '#B23A2E')
axes[0].text(-1.20, 1.16, '(a)  +Q', ha='left', va='bottom', fontsize=8.5, color=MUTED)

for th in np.linspace(0, 2*np.pi, 10)[:-1]:
    axes[1].annotate('', xy=(0.26*np.cos(th), 0.26*np.sin(th)),
                     xytext=(1.10*np.cos(th), 1.10*np.sin(th)),
                     arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.0, mutation_scale=7))
charge(axes[1], 0, 0, '−', '#2A5C8A')
axes[1].text(-1.20, 1.16, '(b)  −Q', ha='left', va='bottom', fontsize=8.5, color=MUTED)

p1 = np.array([-0.42, 0.0]); p2 = np.array([0.42, 0.0])
def field(P):
    E = np.zeros(2)
    for q, c in ((1.0, p1), (-1.0, p2)):
        d = P - c; r = np.linalg.norm(d)
        E += q * d / r**3
    return E
def trace(P0, h=0.008, n=6000):
    pts = [P0.copy()]; P = P0.copy()
    for _ in range(n):
        k1 = field(P); k1 /= np.linalg.norm(k1)
        k2 = field(P + 0.5*h*k1); k2 /= np.linalg.norm(k2)
        P = P + h*k2
        pts.append(P.copy())
        if np.linalg.norm(P - p2) < 0.04 or np.max(np.abs(P)) > 1.45:
            break
    return np.array(pts)
ax = axes[2]
for th in np.linspace(0, 2*np.pi, 12, endpoint=False):
    start = p1 + 0.10*np.array([np.cos(th), np.sin(th)])
    pts = trace(start)
    if len(pts) < 8:
        continue
    ax.plot(pts[:, 0], pts[:, 1], color=ACCENT, lw=0.95, zorder=3)
    i = int(0.55*len(pts))
    ax.annotate('', xy=pts[i+1], xytext=pts[i-1],
                arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=0.9, mutation_scale=7))
charge(ax, *p1, '+', '#B23A2E')
charge(ax, *p2, '−', '#2A5C8A')
ax.text(-1.20, 1.16, '(c)  dipole', ha='left', va='bottom', fontsize=8.5, color=MUTED)
```

**Rules for field lines.**

- They start on positive charge and end on negative charge (or go to infinity).
- They never cross: at a crossing point the field would have two directions.
- Their density (lines per unit area perpendicular to them) is proportional to the
  field strength.
- They leave and enter a conductor **perpendicular** to its surface.
- There are no field lines inside a conductor in electrostatic equilibrium.
- They behave like stretched elastic strings: they pull charges together along their
  length and push them apart sideways.

### A charged conducting sphere

For a conducting sphere of radius $R$ carrying charge $Q$:

| Region | Electric field | Potential |
|---|---|---|
| inside, $r < R$ | $0$ | $kQ/R$ (constant) |
| at the surface, $r = R$ | $kQ/R^2$ | $kQ/R$ |
| outside, $r > R$ | $kQ/r^2$ | $kQ/r$ |

All the charge sits on the **outer surface**, and outside the sphere the field is
exactly that of a point charge $Q$ at the centre. This is why the sphere behaves like
a point charge from outside.

```figure caption="A charged conducting sphere of radius $R$. Left: the field is zero everywhere inside and falls as $1/r^2$ outside, jumping at the surface. Right: the potential is constant inside and falls as $1/r$ outside — it does not jump."
import numpy as np, matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 2, figsize=(5.0, 2.55))
R = 1.0
r = np.linspace(0, 3.0, 900)
E = np.where(r < R, 0.0, np.where(r > 0, 1.0/np.maximum(r, 1e-9)**2, 0))
V = np.where(r <= R, 1.0, np.where(r > 0, 1.0/np.maximum(r, 1e-9), 0))
axes[0].plot(r, E, color=ACCENT, lw=2.0)
axes[0].plot([R, R], [0, 1], color=MUTED, lw=0.8, ls=(0, (3, 2)))
axes[0].plot(R, 1, 'o', mfc='white', mec=ACCENT, ms=5.0, zorder=5)
axes[0].text(0.10, 0.10, 'E = 0', fontsize=8.6, color=INK)
axes[0].text(1.62, 0.62, 'E = kQ/r²', fontsize=8.6, color=ACCENT)
axes[0].set_ylabel('electric field  E')
axes[0].set_title('field', fontsize=9, color=INK)
axes[1].plot(r, V, color=SERIES[1], lw=2.0)
axes[1].plot([R, R], [0, 1], color=MUTED, lw=0.8, ls=(0, (3, 2)))
axes[1].text(0.10, 0.72, 'V = kQ/R', fontsize=8.6, color=SERIES[1])
axes[1].text(1.55, 0.38, 'V = kQ/r', fontsize=8.6, color=SERIES[1])
axes[1].set_ylabel('potential  V')
axes[1].set_title('potential', fontsize=9, color=INK)
for ax in axes:
    ax.set_xlim(0, 3.0); ax.set_ylim(-0.06, 1.18)
    ax.set_xticks([0, 1, 2, 3]); ax.set_xticklabels(['0', 'R', '2R', '3R'])
    ax.set_yticks([])
    ax.set_xlabel('distance  r  from centre')
    ax.spines[['top', 'right']].set_visible(False)
    ax.grid(True, alpha=.35)
```

**A hollow conductor and its outer field.** If a charge $q$ is placed inside a hollow
conductor, an induced charge $-q$ appears on the inner surface and $+q$ on the outer
surface. The field inside the metal is zero, so the outside world feels only the $+q$
on the outer surface, as if it sat at the centre. Conversely, a closed metal box with
no charge inside has $E = 0$ in its cavity: it shields its contents from outside
fields — a **Faraday cage**.

::: caution E = 0 does not mean V = 0
Inside a charged conducting sphere the field is zero, but the potential is
$kQ/R$ — the same as at the surface, not zero. Field is the *slope* of potential;
zero slope does not mean zero height.
:::

### Electric potential and potential energy

The **electric potential** at a point is the work done by an external agent in
bringing a unit positive charge from infinity to that point, without acceleration:

$$ V = \frac{W_{\text{ext}}}{q_0}, \qquad V = \frac{kq}{r} $$

The unit is the volt: 1 V = 1 J C⁻¹. Potential is a **scalar**, so potentials add
algebraically — much easier than adding fields. The zero is taken at infinity.

The **potential energy** of a charge $q$ at potential $V$ is $U = qV$. For a pair of
point charges,

$$ U = \frac{kq_1q_2}{r} $$

| Situation | Sign of $U$ | Who does the work |
|---|---|---|
| two like charges brought together | positive | the external agent does positive work |
| two unlike charges brought together | negative | the field does positive work |
| positive charge moved along $\vec E$ | falls | the field does positive work |
| positive charge moved against $\vec E$ | rises | the external agent does positive work |

The field and the potential are linked by

$$ E = -\frac{dV}{dr} $$

The minus sign says that the field points **downhill** in potential. For a uniform
field, $E = V/d$. Moving a charge through a potential difference $\Delta V$ changes
its energy by $q\Delta V$; this is the working principle of every accelerator,
battery and cathode-ray tube.

For a **system of several charges**, the potential energy is the sum over every pair:

$$ U = k\left(\frac{q_1q_2}{r_{12}} + \frac{q_1q_3}{r_{13}} + \frac{q_2q_3}{r_{23}} + \cdots\right) $$

Four equal charges $q$ at the corners of a square of side $a$ therefore have
$U = 4kq^2/a + 2kq^2/(\sqrt{2}a)$: four side pairs and two diagonal pairs.

An **equipotential surface** is a surface on which $V$ is constant. No work is done
moving a charge along it, so equipotentials are always perpendicular to field lines.
The surface of any conductor is an equipotential.

::: example Worked example 17.2 — field and potential of a sphere
**Problem.** A conducting sphere of radius 10 cm carries $1\ \mu\text{C}$. Find the
field and the potential at (a) 5 cm and (b) 20 cm from the centre.

**Solution.** (a) 5 cm is inside the sphere, so $E = 0$. The potential is the surface
value, $V = kQ/R = 9\times10^9\times10^{-6}/0.10 = 9\times10^4$ V.
(b) $E = kQ/r^2 = 9\times10^9\times10^{-6}/(0.20)^2 = 2.25\times10^5$ N C⁻¹, and
$V = kQ/r = 9\times10^9\times10^{-6}/0.20 = 4.5\times10^4$ V.
:::

### Gauss's law

The **electric flux** through a surface is $\phi = \int \vec E\cdot d\vec A$ — the
field times the area perpendicular to it. Gauss's law states:

$$ \oint \vec E\cdot d\vec A = \frac{q_{\text{enclosed}}}{\varepsilon_0} $$

The flux through any **closed** surface equals the net charge inside it divided by
$\varepsilon_0$. The field $\vec E$ in the integral is the total field from all
charges, but charges *outside* the surface contribute zero net flux: every line that
enters must also leave.

Three results must be known cold. Each comes from choosing a surface on which the
field is constant and perpendicular.

| Charge distribution | Gaussian surface | Result |
|---|---|---|
| point charge, or outside a sphere $Q$ | sphere of radius $r$ | $E = \dfrac{Q}{4\pi\varepsilon_0r^2}$ |
| long line charge, $\lambda$ per metre | cylinder of radius $r$, length $l$ | $E = \dfrac{\lambda}{2\pi\varepsilon_0r}$ |
| infinite sheet, $\sigma$ per m² | pillbox through the sheet | $E = \dfrac{\sigma}{2\varepsilon_0}$ |
| two opposite plates, each $\sigma$ | pillbox through one plate | $E = \dfrac{\sigma}{\varepsilon_0}$ between them |

For the sphere: $E(4\pi r^2) = Q/\varepsilon_0$. For the line:
$E(2\pi rl) = \lambda l/\varepsilon_0$. For the sheet, the flux leaves both faces of
the pillbox: $E(2A) = \sigma A/\varepsilon_0$. In each case the area of the Gaussian
surface cancels, which is why the answer depends only on the charge density.

```figure caption="The three Gaussian surfaces the paper asks about: a sphere around a point charge or charged sphere, a cylinder around a line charge, and a pillbox through an infinite sheet."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
fig, axes = plt.subplots(1, 3, figsize=(5.1, 2.25))
for ax in axes:
    ax.set_aspect('equal'); ax.axis('off')
    ax.set_xlim(-1.25, 1.25); ax.set_ylim(-1.15, 1.15)

ax = axes[0]
ax.add_patch(Circle((0, 0), 0.62, fill=False, ec=MUTED, lw=1.1, ls=(0, (3, 2))))
ax.plot(0, 0, 'o', color='#B23A2E', ms=8, zorder=5)
ax.text(0, 0, '+', color='white', ha='center', va='center', fontsize=8, zorder=6)
for th in np.linspace(0, 2*np.pi, 8, endpoint=False):
    ax.annotate('', xy=(0.98*np.cos(th), 0.98*np.sin(th)),
                xytext=(0.66*np.cos(th), 0.66*np.sin(th)),
                arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.0, mutation_scale=7))
ax.annotate('', xy=(0.62*np.cos(0.9), 0.62*np.sin(0.9)), xytext=(0, 0),
            arrowprops=dict(arrowstyle='-', color=INK, lw=0.8))
ax.text(0.26, 0.30, 'r', fontsize=9.5, color=INK, bbox=dict(fc='white', ec='none', pad=1.0))
ax.text(0, -1.08, 'Gaussian sphere', ha='center', fontsize=8.3, color=MUTED)

ax = axes[1]
ax.plot([0, 0], [-0.85, 0.85], color='#B23A2E', lw=2.4)
ax.add_patch(Rectangle((-0.48, -0.62), 0.96, 1.24, fill=False, ec=MUTED, lw=1.1, ls=(0, (3, 2))))
for y in (-0.45, 0, 0.45):
    for s in (-1, 1):
        ax.annotate('', xy=(s*0.95, y), xytext=(s*0.10, y),
                    arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=0.95, mutation_scale=7))
ax.text(-0.42, 0.92, 'λ per metre', fontsize=8.0, color=INK)
ax.text(0.55, -0.78, 'cylinder', fontsize=8.3, color=MUTED)
ax.text(0, -1.08, 'line charge', ha='center', fontsize=8.3, color=MUTED)

ax = axes[2]
ax.add_patch(Rectangle((-0.95, -0.07), 1.9, 0.14, facecolor='#B23A2E', alpha=0.55, ec='none'))
ax.add_patch(Rectangle((-0.40, -0.42), 0.80, 0.84, fill=False, ec=MUTED, lw=1.1, ls=(0, (3, 2))))
for x in (-0.22, 0.0, 0.22):
    ax.annotate('', xy=(x, 0.95), xytext=(x, 0.12),
                arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=0.95, mutation_scale=7))
    ax.annotate('', xy=(x, -0.95), xytext=(x, -0.12),
                arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=0.95, mutation_scale=7))
ax.text(0, 1.02, 'E', ha='center', fontsize=8.5, color=ACCENT)
ax.text(0, -1.08, 'infinite sheet,  σ', ha='center', fontsize=8.3, color=MUTED)
```

::: caution Flux is about what is inside
The flux through a closed surface depends only on the net charge **enclosed**. Move
the charge around inside and the flux does not change. A charge outside gives zero
net flux even though the field at the surface is not zero. Through one face of a cube
with a charge at its centre, the flux is $q/6\varepsilon_0$ by symmetry.
:::

## 17.3 Capacitors

### Capacitance

A **capacitor** is a pair of conductors separated by an insulator. When a potential
difference $V$ is applied, the plates carry charges $+Q$ and $-Q$. The **capacitance**
is the charge on the positive plate per unit potential difference:

$$ C = \frac{Q}{V} $$

The unit is the **farad**, 1 F = 1 C V⁻¹. One farad is enormous; practical capacitors
are marked in microfarads (1 µF = 10⁻⁶ F) or picofarads (1 pF = 10⁻¹² F).

### The parallel-plate capacitor

For plates of area $A$ separated by a distance $d$ in vacuum (or air), the field
between them is $E = \sigma/\varepsilon_0 = Q/(\varepsilon_0A)$ and the potential
difference is $V = Ed = Qd/(\varepsilon_0A)$. Hence

$$ C_0 = \frac{\varepsilon_0A}{d} $$

::: derivation Capacitance of a parallel-plate capacitor
**Setting up.** Two parallel plates of area $A$, separation $d$, carrying $+Q$ and
$-Q$. The field between them is uniform and the plates are equipotentials.

**Step 1 — the field from one plate.** A single sheet of charge density $\sigma$
gives $E = \sigma/2\varepsilon_0$ on each side. Two opposite plates add their fields
between them and cancel them outside: $E = \sigma/\varepsilon_0$.

**Step 2 — write $\sigma$ in terms of $Q$.** $\sigma = Q/A$, so $E = Q/(\varepsilon_0A)$.

**Step 3 — integrate the field.** The potential difference between two points a
distance $d$ apart along a uniform field is $V = Ed = Qd/(\varepsilon_0A)$.

**Step 4 — divide.** $C = Q/V = \varepsilon_0A/d$.

**Result.** $C = \varepsilon_0A/d$: capacitance grows with plate area and shrinks as
the plates are separated. **Condition:** the plates are large compared with their
separation, so edge effects can be ignored.
:::

So $C \propto A$ and $C \propto 1/d$. Doubling the separation halves the capacitance;
doubling the area doubles it. Note that $C$ does **not** depend on $Q$ or $V$: it is a
property of the geometry (and the dielectric).

### Dielectrics

A **dielectric** is an insulating material placed between the plates. Its molecules
polarise — in a polar material they already carry a dipole moment and line up; in a
non-polar one the applied field separates the charge. Either way the face of the slab
next to the positive plate becomes negative and the far face positive, and this
induced field opposes the applied one. The net field inside is weaker, so the same
charge needs a smaller potential difference, and the capacitance rises:

$$ C = \frac{K\varepsilon_0A}{d} = KC_0 $$

where $K$ is the **dielectric constant** (relative permittivity), $K = C/C_0$.

| Material | $K$ |
|---|---|
| vacuum | 1 (exactly) |
| air | 1.0006 ≈ 1 |
| paper | 3.7 |
| mica | 6 |
| glass | 5–10 |
| water | 80 |
| barium titanate | about 1200 |

If a slab of thickness $t$ (less than $d$) is inserted, the two regions act like
capacitors in series:

$$ C = \frac{\varepsilon_0A}{d - t + t/K} $$

### Combinations

| | Series | Parallel |
|---|---|---|
| Connection | end to end | side by side |
| Same for each | charge $Q$ | potential difference $V$ |
| Total | $\dfrac{1}{C} = \dfrac{1}{C_1} + \dfrac{1}{C_2} + \cdots$ | $C = C_1 + C_2 + \cdots$ |
| Two capacitors | $C = \dfrac{C_1C_2}{C_1 + C_2}$ | $C = C_1 + C_2$ |
| Result | smaller than the smallest | larger than the largest |

In series the smallest capacitor takes the largest share of the voltage
($V \propto 1/C$). In parallel each capacitor takes the share of charge it can hold
($Q \propto C$).

```photogrid label="17.2" cols="2" ratio="1.2" caption="Series and parallel combinations. (a) Real capacitors carry both a capacitance and a voltage rating. (b) For 10, 20 and 40 microfarad on 12 V, in series 1/C = 1/10 + 1/20 + 1/40 gives 5.71 microfarad and one common charge of 68.6 microcoulomb, so the voltage divides inversely as capacitance: 6.86, 3.43 and 1.71 V, adding to 12 V. In parallel the voltage is 12 V on each, C = 70 microfarad, and the charges 120, 240 and 480 microcoulomb add up to 840. The parallel bank stores 5.04 mJ, 12.2 times the 0.411 mJ of the series chain."
@ photo id="ceephy/capacitors" cap="Electrolytic capacitors of different capacitance and voltage rating"
fit 1.2
focus 0.5 0.5
@ svg cap="12 V shared by 10, 20 and 40 microfarad capacitors"
C = (10e-6, 20e-6, 40e-6); V = 12.0
cs = 1 / sum(1 / c for c in C); cp = sum(C); q = cs * V
vs = [q / c for c in C]; qs = [c * V for c in C]
assert abs(sum(vs) - V) < 1e-9 and abs(sum(qs) - cp * V) < 1e-12 and abs(cs * 1e6 - 5.714) < 1e-3
es, ep = 0.5 * cs * V ** 2, 0.5 * cp * V ** 2
facts = dict(cs="%.2f" % (cs * 1e6), q="%.1f" % (q * 1e6), v1="%.2f" % vs[0], v2="%.2f" % vs[1], v3="%.2f" % vs[2], cp="%.0f" % (cp * 1e6), q1="%.0f" % (qs[0] * 1e6), q2="%.0f" % (qs[1] * 1e6), q3="%.0f" % (qs[2] * 1e6), qt="%.0f" % (sum(qs) * 1e6), ep="%.2f" % (ep * 1e3), es="%.3f" % (es * 1e3), rat="%.1f" % (ep / es))
f = Fig(300, 236)
f.text(150, 14, "Series: voltage divides, 12 V in all", size=10.5, color=NAVY, bold=True)
x = 20
for i, (v, c, col, fl) in enumerate(zip(vs, (10, 20, 40), (RED, AMBER, TEAL), (ROSE, SAND, MINT))):
    w = v * 20; f.box(x, 30, w, 30, label="%.1f" % v, fill=fl, stroke=col, size=10.5, bold=True, r=2)
    f.text(x + w / 2, 74, "%d uF" % c, size=10.5, color=col, bold=True); x += w
f.text(150, 98, "V = Q / C, same Q = %.1f uC" % (q * 1e6), size=10.5, color=SLATE)
f.text(150, 124, "Parallel: charge adds, 840 uC in all", size=10.5, color=NAVY, bold=True)
x = 20
for i, (qq, c, col, fl) in enumerate(zip(qs, (10, 20, 40), (RED, AMBER, TEAL), (ROSE, SAND, MINT))):
    w = qq / sum(qs) * 240; f.box(x, 140, w, 30, label="%.0f" % (qq * 1e6), fill=fl, stroke=col, size=10.5, bold=True, r=2)
    f.text(x + w / 2, 184, "%d uF" % c, size=10.5, color=col, bold=True); x += w
f.text(150, 206, "series %.2f uF; parallel %.0f uF" % (cs * 1e6, cp * 1e6), size=10.5, color=NAVY, bold=True)
f.text(150, 224, "energy %.3f mJ against %.2f mJ" % (es * 1e3, ep * 1e3), size=10.5, color=NAVY, bold=True)
```

### Energy stored

Charging a capacitor means pushing charge against the growing potential. The work
done, and the energy stored, is

$$ U = \frac{1}{2}QV = \frac{1}{2}CV^2 = \frac{Q^2}{2C} $$

The energy is stored in the **field** between the plates, not in the metal. For a
parallel-plate capacitor, divide by the volume $Ad$:

$$ u = \frac{U}{Ad} = \frac{1}{2}\varepsilon_0E^2 $$

This is the **energy density** of an electric field, in J m⁻³. With a dielectric it
becomes $\frac12K\varepsilon_0E^2$.

The two plates attract each other with a force

$$ F = \frac{Q^2}{2\varepsilon_0A} = \frac12\varepsilon_0AE^2 $$

At constant charge this force does not depend on the separation. To pull the plates
apart you must do work $F\,\Delta d$, and that work is exactly the rise in stored
energy — which is why $U\propto d$ when $Q$ is fixed.

### Effect of a dielectric: battery connected or removed

This table is the single most examined idea in the chapter. Decide first whether the
battery is still connected.

| Quantity | Battery connected ($V$ fixed) | Battery removed ($Q$ fixed) |
|---|---|---|
| Capacitance $C$ | becomes $KC$ | becomes $KC$ |
| Charge $Q$ | becomes $KQ$ | unchanged |
| Potential difference $V$ | unchanged | falls to $V/K$ |
| Field $E = V/d$ | unchanged | falls to $E/K$ |
| Energy $U$ | becomes $KU$ | falls to $U/K$ |
| Who supplies the energy | the battery | the field (it pulls the slab in) |

With the battery connected, inserting the slab draws extra charge $Q(K-1)$ from the
battery. The battery does work $VQ(K-1)$, while the stored energy rises by only half
that amount; the rest is dissipated as heat (or appears as mechanical work if the slab
is free to move).

With the battery removed, the charge cannot change. The field pulls the slab in and
does mechanical work; the stored energy falls by exactly that amount.

```figure caption="A parallel-plate capacitor. (a) With vacuum between the plates the field is uniform, $E_0 = V/d$. (b) A dielectric slab of constant $K$, with the battery disconnected so the charge stays the same: the field inside the slab falls to $E_0/K$ and the potential difference falls with it."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, axes = plt.subplots(1, 2, figsize=(5.0, 2.6))
for ax in axes:
    ax.axis('off'); ax.set_xlim(-0.15, 3.15); ax.set_ylim(-0.50, 2.45)

for ax, slab in zip(axes, (False, True)):
    ax.plot([0.45, 0.45], [0.15, 2.05], color='#B23A2E', lw=4.0, solid_capstyle='butt')
    ax.plot([2.45, 2.45], [0.15, 2.05], color='#2A5C8A', lw=4.0, solid_capstyle='butt')
    ax.text(0.45, 2.14, '+Q', fontsize=9, color='#B23A2E', ha='center')
    ax.text(2.45, 2.14, '−Q', fontsize=9, color='#2A5C8A', ha='center')
    for y in (0.55, 1.10, 1.65):
        if slab:
            ax.annotate('', xy=(1.15, y), xytext=(0.52, y),
                        arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.3, mutation_scale=8))
            ax.annotate('', xy=(1.72, y), xytext=(1.19, y),
                        arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=0.6, mutation_scale=5.5))
            ax.annotate('', xy=(2.38, y), xytext=(1.78, y),
                        arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.3, mutation_scale=8))
        else:
            ax.annotate('', xy=(2.38, y), xytext=(0.52, y),
                        arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.3, mutation_scale=8))

axes[0].annotate('', xy=(2.45, -0.18), xytext=(0.45, -0.18),
                 arrowprops=dict(arrowstyle='<->', color=MUTED, lw=1.0, mutation_scale=8))
axes[0].text(1.45, -0.44, 'd', fontsize=9.5, color=MUTED, ha='center')
axes[0].text(1.45, 2.36, '(a)  vacuum', fontsize=8.6, color=INK, ha='center')
axes[1].add_patch(Rectangle((1.15, 0.15), 0.60, 1.90, facecolor=SERIES[2], alpha=0.28, ec=SERIES[2], lw=0.8))
axes[1].text(1.45, -0.30, 'dielectric,  K', fontsize=8.4, color=INK, ha='center')
axes[1].text(1.45, 2.36, '(b)  with dielectric', fontsize=8.6, color=INK, ha='center')
```

::: caution The 1/d trap
At constant charge, pulling the plates apart **increases** the potential difference
and the stored energy: $C$ falls as $1/d$, so $V = Q/C$ rises as $d$, and
$U = Q^2/2C$ rises as $d$. The work you do against the attraction of the plates is
stored in the field. Students often say $V$ falls because "the capacitor is
weaker" — it is the charge that would fall if a battery were connected, not the
potential difference of an isolated capacitor.
:::

::: caution Connected or disconnected?
The dielectric table flips depending on the battery. Connected: $V$ stays, $Q$
rises, $U$ rises. Disconnected: $Q$ stays, $V$ falls, $U$ falls. Write "V fixed" or
"Q fixed" at the top of your rough work before touching a formula.
:::

### Sharing charge between capacitors

When a charged capacitor $C_1$ at $V_1$ is connected to an uncharged (or differently
charged) capacitor $C_2$, charge flows until both have the same potential:

$$ V = \frac{C_1V_1 + C_2V_2}{C_1 + C_2}, \qquad Q_{\text{total}} = Q_1 + Q_2 $$

The total charge is conserved, but the total energy is **not**: some is lost as heat
in the connecting wire and as electromagnetic radiation. The loss is

$$ \Delta U = \frac{C_1C_2}{2(C_1+C_2)}(V_1 - V_2)^2 $$

For two equal capacitors, one charged and one empty, exactly half the initial energy
is lost, whatever the voltage.

::: example Worked example 17.3 — a capacitor with and without a dielectric
**Problem.** A parallel-plate capacitor has plates of area $0.02\ \text{m}^2$
separated by 1 mm of air. (a) Find its capacitance. (b) A slab of dielectric constant
5 fills the gap and the capacitor is connected to 100 V. Find the charge and the
stored energy. (c) The battery is then removed and the slab is pulled out. Find the
new potential difference.

**Solution.** (a)
$C_0 = \varepsilon_0A/d = 8.85\times10^{-12}\times0.02/10^{-3} = 1.77\times10^{-10}$
F $= 177$ pF.

(b) With the dielectric, $C = KC_0 = 5\times177 = 885$ pF. Then
$Q = CV = 885\times10^{-12}\times100 = 8.85\times10^{-8}$ C $= 88.5$ nC, and
$U = \frac12CV^2 = \frac12\times885\times10^{-12}\times10^4 = 4.43\times10^{-6}$ J.

(c) The battery is removed, so $Q$ stays $88.5$ nC. Without the slab,
$C = 177$ pF, so $V = Q/C = 8.85\times10^{-8}/1.77\times10^{-10} = 500$ V. Removing
the dielectric at constant charge raises the voltage five times — the same factor $K$.
:::

::: example Worked example 17.4 — sharing charge
**Problem.** A $2\ \mu\text{F}$ capacitor charged to 100 V is connected to an
uncharged $3\ \mu\text{F}$ capacitor. Find the common potential and the energy lost.

**Solution.** Total charge $= 2\times10^{-6}\times100 = 200\ \mu\text{C}$; total
capacitance $= 5\ \mu\text{F}$. So
$V = 200\ \mu\text{C}/5\ \mu\text{F} = 40$ V.

Initial energy $= \frac12(2\times10^{-6})(100)^2 = 0.010$ J. Final energy
$= \frac12(5\times10^{-6})(40)^2 = 0.004$ J. Loss $= 0.006$ J $= 6$ mJ, which is
60 % of the initial energy.
:::

```photogrid label="17.1" cols="2" ratio="1.2" caption="Energy stored in charged conductors. (a) A thundercloud and the ground behave like a huge capacitor that discharges as lightning. (b) The energy U = 1/2 Q V, drawn on a log scale, is 0.312 J in a 1,000 microfarad, 25 V electrolytic capacitor, 5.45 J in a camera flash (100 microfarad, 330 V), 400 J in a defibrillator (32 microfarad, 5 kV) and about 7.5 x 10^8 J for a flash that moves 15 C through 100 MV (illustrative), roughly 208 kWh. Each step in the chart is a factor of ten in energy."
@ photo id="ceephy/eiffel" cap="An early photograph of lightning striking the Eiffel Tower, a discharge of a natural capacitor"
fit 1.2
focus 0.5 0.5
@ svg cap="Energy stored, U = 1/2 Q V, on a log scale"
U = lambda C, V: 0.5 * C * V ** 2
u1, u2, u3 = U(1000e-6, 25), U(100e-6, 330), U(32e-6, 5000); u4 = 0.5 * 15 * 1e8
assert abs(u1 - 0.3125) < 1e-9 and abs(u2 - 5.445) < 1e-9 and abs(u3 - 400) < 1e-9 and abs(u4 / 3.6e6 - 208.3) < 0.1
facts = dict(u1="%.3f" % u1, u2="%.2f" % u2, u3="%.0f" % u3, u4="7.5 x 10^8", kwh="%.0f" % (u4 / 3.6e6))
f = Fig(300, 236)
f.text(150, 14, "U = 1/2 Q V (joules, log scale)", size=10.5, color=NAVY, bold=True)
rows = (("1000 uF at 25 V", u1, TEAL, MINT), ("flash 100 uF at 330 V", u2, TEAL, MINT), ("defibrillator 32 uF at 5 kV", u3, AMBER, SAND), ("lightning 15 C, 100 MV", u4, RED, ROSE))
for i, (lab, v, col, fl) in enumerate(rows):
    y = 28 + i * 40
    f.text(14, y + 4, lab, size=10.5, color=SLATE, anchor="start")
    w = (math.log10(v) + 1) * 20
    f.box(14, y + 10, w, 14, fill=fl, stroke=col, r=2, sw=1.6)
    f.text(14 + w + 5, y + 17, "%.4g J" % v if v < 1000 else "7.5e8 J", size=10.5, color=col, bold=True, anchor="start", vmid=True)
f.text(150, 200, "bar length = log10(U) + 1 decades", size=10.5, color=SLATE)
f.text(150, 218, "lightning = %.0f kWh (illustrative)" % (u4 / 3.6e6), size=10.5, color=NAVY, bold=True)
```

```photogrid label="17.3" cols="2" ratio="1.2" caption="Energy stored in the field. (a) Electrolytic capacitors have a large capacitance for their size and are marked with their capacitance and maximum voltage. (b) The cell uses U = 1/2 C V2 for a 330 microfarad capacitor of the type used in a camera flash. At 100 V it stores only 1.65 J, but at 300 V it stores 14.85 J (a charge of 0.099 C) and at 400 V 26.4 J, since the energy grows as the square of the voltage. Released in one millisecond, 14.85 J is a peak power of 14.8 kW, which is how a small battery can produce a bright flash. The same energy could lift a 1 kg mass by 1.52 m."
@ photo id="ceephy3/capacitor" cap="Electrolytic capacitors"
fit 1.2
focus 0.5 0.5
@ svg cap="Energy stored in a camera-flash capacitor"
C = 330e-6
rows = [("%d V" % v, 0.5 * C * v ** 2) for v in (100, 200, 300, 400)]
assert round(rows[2][1], 2) == 14.85 and round(rows[3][1], 1) == 26.4
Q = C * 300
P = rows[2][1] / 1e-3 / 1000
h = rows[2][1] / (1 * 9.8)
f = Fig(300, 236)
f.text(150, 12, "Energy U = 1/2 C V^2 of a 330 microfarad capacitor, J", size=10, color=NAVY, bold=True)
hbars(f, rows, vmax=28, fmt="%.2f", x0=52, y0=30, bw=170, gap=30)
f.text(150, 158, "doubling V quadruples U", size=10, color=SLATE, bold=True)
f.text(150, 178, "at 300 V: Q = C V = %.3f C" % Q, size=10.5, color=NAVY, bold=True)
f.text(150, 198, "released in 1 ms: peak power %.1f kW" % P, size=10.5, color=NAVY, bold=True)
f.text(150, 216, "equal to lifting 1 kg by %.2f m" % h, size=10, color=SLATE, bold=True)
facts = dict(u=rows[2][1], u4=rows[3][1], u1=rows[0][1], P=P, Q=Q, h=h)
```

## Formula and fact sheet

| Item | Formula or fact |
|---|---|
| Quantisation | $q = ne$, $e = 1.6\times10^{-19}$ C; 1 C $= 6.25\times10^{18}$ electrons |
| Coulomb's law | $F = kq_1q_2/r^2$, $k = 9\times10^9$ N m² C⁻² |
| In a medium | $F = F_0/K$ |
| Field of a point charge | $E = kq/r^2$, N C⁻¹ = V m⁻¹ |
| Uniform field | $E = V/d$ |
| Force on a charge | $F = qE$ |
| Potential | $V = kq/r$, J C⁻¹ = V; scalar |
| Potential energy | $U = qV = kq_1q_2/r$ |
| Field and potential | $E = -dV/dr$ |
| Conducting sphere | $E = 0$ inside; $E = kQ/r^2$ outside; $V = kQ/R$ inside |
| Gauss's law | $\oint \vec E\cdot d\vec A = q_{\text{enc}}/\varepsilon_0$ |
| Line charge | $E = \lambda/(2\pi\varepsilon_0r)$ |
| Sheet of charge | $E = \sigma/(2\varepsilon_0)$ |
| Two plates | $E = \sigma/\varepsilon_0$ between them |
| Capacitance | $C = Q/V$; 1 F $= 1$ C V⁻¹ |
| Parallel plate | $C = \varepsilon_0A/d$; with dielectric $C = K\varepsilon_0A/d$ |
| Partly filled gap | $C = \varepsilon_0A/(d - t + t/K)$ |
| Series | $1/C = \Sigma 1/C_i$; same $Q$ |
| Parallel | $C = \Sigma C_i$; same $V$ |
| Energy | $U = \frac12QV = \frac12CV^2 = Q^2/2C$ |
| Energy density | $u = \frac12\varepsilon_0E^2$; $\frac12K\varepsilon_0E^2$ in a dielectric |
| Isolated sphere | $C = 4\pi\varepsilon_0R$ |
| Sharing | $V = (C_1V_1+C_2V_2)/(C_1+C_2)$ |
| Energy lost in sharing | $\Delta U = C_1C_2(V_1-V_2)^2/[2(C_1+C_2)]$ |
| Constant $Q$, plates apart | $C\propto1/d$, $V\propto d$, $U\propto d$ |
| Constant $V$, plates apart | $C\propto1/d$, $Q\propto1/d$, $U\propto1/d$ |
| Null point, like charges | between them, nearer the smaller, $x = L/(1+\sqrt{q_2/q_1})$ |
| Triangle of three equal charges | $F = \sqrt{3}\,kq^2/a^2$ on each; centre charge $-q/\sqrt{3}$ |
| Dielectric constants | air 1, paper 3.7, mica 6, glass 5–10, water 80 |

## Chapter summary

- Charge is quantised ($q = ne$), conserved, and additive as a scalar. One coulomb is
  $6.25\times10^{18}$ electronic charges.
- Charging by conduction gives the same sign as the charging body; charging by
  induction gives the opposite sign, provided the earth is removed before the rod.
- Coulomb's law: $F = kq_1q_2/r^2$ in vacuum, divided by $K$ in a medium. Forces
  superpose as vectors, so the net force is found one charge at a time.
- The null point of two like charges lies between them, nearer the smaller; for
  equilibrium of three charges the third is opposite in sign and fixed in magnitude.
- Field lines leave positive charge, end on negative charge, never cross, and are
  perpendicular to conductors. $E = 0$ inside a conductor, but $V$ is constant there,
  not zero.
- $V = kq/r$ is a scalar; $U = qV$; $E = -dV/dr$ points downhill in potential.
- Gauss's law gives the three standard fields: $kQ/r^2$ for a sphere,
  $\lambda/(2\pi\varepsilon_0r)$ for a line, $\sigma/(2\varepsilon_0)$ for a sheet.
- $C = Q/V = \varepsilon_0A/d$, multiplied by $K$ with a dielectric; series adds
  reciprocals, parallel adds directly.
- $U = \frac12CV^2 = Q^2/2C$ and $u = \frac12\varepsilon_0E^2$. At constant charge,
  separating the plates raises $V$ and $U$; at constant voltage, inserting a
  dielectric raises $Q$ and $U$ by $K$.
- Charge sharing conserves charge but not energy: the loss is
  $C_1C_2(V_1-V_2)^2/[2(C_1+C_2)]$.

## Practice questions

**Set A — Recall (30 questions)**

1. One coulomb is the charge on
   (a) $1.6\times10^{-19}$ electrons (b) $6.25\times10^{-18}$ electrons (c) $6.25\times10^{18}$ electrons (d) $1.6\times10^{19}$ electrons
2. The force between two point charges in a medium of dielectric constant $K$, at the same separation, is
   (a) $K$ times the vacuum force (b) $1/K$ times the vacuum force (c) $K^2$ times the vacuum force (d) the same as in vacuum
3. The value of $1/(4\pi\varepsilon_0)$ is
   (a) $9\times10^{9}$ N m² C⁻² (b) $8.85\times10^{-12}$ N m² C⁻² (c) $9\times10^{9}$ N C⁻² (d) $1.6\times10^{-19}$ N m² C⁻²
4. The electric field at a point is the
   (a) force on any charge placed there (b) work done in bringing a unit charge there (c) charge per unit area there (d) force per unit positive charge there
5. The unit of electric field strength may be written as
   (a) N C (b) N C⁻¹ or V m⁻¹ (c) J C⁻¹ (d) C m⁻²
6. Inside a charged conductor in electrostatic equilibrium, the electric field is
   (a) zero (b) maximum (c) equal to the surface field (d) directed outward
7. Electric potential is a
   (a) vector along the field (b) vector against the field (c) scalar (d) tensor
8. The work done in moving a charge along an equipotential surface is
   (a) $qV$ (b) maximum (c) infinite (d) zero
9. The electric flux through a closed surface enclosing a charge $q$ is
   (a) $q\varepsilon_0$ (b) $q/\varepsilon_0$ (c) zero (d) $q/4\pi\varepsilon_0$
10. The field due to an infinite plane sheet of charge density $\sigma$ is
   (a) $\sigma/\varepsilon_0$ (b) $2\sigma/\varepsilon_0$ (c) $\sigma/2\varepsilon_0$ (d) $\sigma r/\varepsilon_0$
11. The field at distance $r$ from a long line charge of density $\lambda$ is proportional to
   (a) $1/r$ (b) $1/r^2$ (c) $r$ (d) $r^2$
12. Outside a charged conducting sphere of radius $R$, the field at distance $r>R$ is
   (a) $kQ/R^2$ (b) zero (c) $kQr/R^3$ (d) $kQ/r^2$
13. Capacitance is defined as
   (a) energy stored per unit charge (b) charge stored per unit potential difference (c) potential difference per unit charge (d) charge per unit area
14. The farad is equal to
   (a) 1 C V (b) 1 V C⁻¹ (c) 1 C V⁻¹ (d) 1 J C⁻¹
15. The capacitance of a parallel-plate capacitor is directly proportional to
   (a) the plate area (b) the plate separation (c) the potential difference (d) the charge stored
16. Capacitors in series all carry the same
   (a) potential difference (b) energy (c) capacitance (d) charge
17. Capacitors in parallel all have the same
   (a) charge (b) energy (c) potential difference (d) capacitance
18. The energy stored in a capacitor $C$ at potential difference $V$ is
   (a) $CV$ (b) $\frac12CV^2$ (c) $CV^2$ (d) $\frac12C^2V$
19. The energy density in a field $E$ in vacuum is
   (a) $\frac12\varepsilon_0E^2$ (b) $\varepsilon_0E^2$ (c) $\frac12\varepsilon_0E$ (d) $\frac12E^2/\varepsilon_0$
20. The dielectric constant of a medium is the ratio of
   (a) charge to potential (b) field to potential (c) $\varepsilon_0$ to the medium's permittivity (d) the capacitance with the dielectric to that without it
21. Charge is said to be quantised because it
   (a) is always positive (b) occurs only in whole multiples of $e$ (c) is conserved (d) can be transferred
22. In charging by induction, the conductor acquires a charge
   (a) opposite in sign to the inducing charge (b) of the same sign as the inducing charge (c) that is always positive (d) that is always zero
23. The leaves of a gold-leaf electroscope diverge because
   (a) the leaves are magnetised (b) air pushes them apart (c) they carry like charges and repel (d) the glass case is charged
24. Electric field lines
   (a) can cross at a neutral point (b) start on negative charges (c) are always straight (d) never cross one another
25. The electric potential at infinity is taken as
   (a) zero (b) infinite (c) $kQ/R$ (d) negative
26. The potential at distance $r$ from a point charge $q$ is
   (a) $kq/r^2$ (b) $kqr$ (c) $kq/r$ (d) $kq/r^3$
27. The relation between field and potential is
   (a) $E = dV/dr$ (b) $E = -dV/dr$ (c) $E = Vr$ (d) $E = -V/r^2$
28. The capacitance of an isolated conducting sphere of radius $R$ is
   (a) $4\pi\varepsilon_0R^2$ (b) $\varepsilon_0R$ (c) $4\pi\varepsilon_0/R$ (d) $4\pi\varepsilon_0R$
29. Three capacitors of $3\ \mu\text{F}$ each are joined in series. The equivalent capacitance is
   (a) $9\ \mu\text{F}$ (b) $3\ \mu\text{F}$ (c) $1\ \mu\text{F}$ (d) $0.33\ \mu\text{F}$
30. The charge on each plate of a $2\ \mu\text{F}$ capacitor charged to 100 V is
   (a) $200\ \mu\text{C}$ (b) $50\ \mu\text{C}$ (c) $2\ \mu\text{C}$ (d) $0.02$ C

::: note Answers and explanations — Set A
**1.** (c) — $n = Q/e = 1/1.6\times10^{-19} = 6.25\times10^{18}$. Option (a) is the magnitude of the charge on one electron.
**2.** (b) — the medium's polarisation weakens the force: $F = F_0/K$. $K$ for air is about 1, for water about 80.
**3.** (a) — $k = 9\times10^9$ N m² C⁻². Option (b) is $\varepsilon_0$ itself, not $1/4\pi\varepsilon_0$.
**4.** (d) — field is force per unit *positive* charge; a negative charge feels force opposite to $\vec E$.
**5.** (b) — N C⁻¹ and V m⁻¹ are the same unit, since V = J C⁻¹ = N m C⁻¹.
**6.** (a) — free electrons rearrange until the internal field is zero; the charge sits on the surface.
**7.** (c) — potential is a scalar; only the field is a vector.
**8.** (d) — no potential difference means no work, by $W = q\Delta V$.
**9.** (b) — Gauss's law: flux $= q_{\text{enc}}/\varepsilon_0$.
**10.** (c) — one sheet gives $\sigma/2\varepsilon_0$; the $\sigma/\varepsilon_0$ answer is for the field *between two* opposite plates.
**11.** (a) — $E = \lambda/(2\pi\varepsilon_0r)$; the $1/r^2$ law belongs to a point charge.
**12.** (d) — outside, the sphere acts as a point charge at its centre.
**13.** (b) — $C = Q/V$, charge per volt.
**14.** (c) — 1 F = 1 C V⁻¹.
**15.** (a) — $C = \varepsilon_0A/d$: up with area, down with separation.
**16.** (d) — the same charge passes through each capacitor in series; the voltages divide.
**17.** (c) — parallel branches share the same potential difference; the charges divide.
**18.** (b) — $U = \frac12CV^2$. Option (a) is the charge, not the energy.
**19.** (a) — $u = \frac12\varepsilon_0E^2$, in J m⁻³.
**20.** (d) — $K = C/C_0 = \varepsilon/\varepsilon_0$.
**21.** (b) — charge comes in packets of $e$; no fraction of $e$ has ever been observed free.
**22.** (a) — induction leaves the opposite charge; the inducing charge is never transferred.
**23.** (c) — both leaves receive the same sign and repel; the divergence angle grows with charge.
**24.** (d) — two directions at one point is impossible; lines also start on positive charge.
**25.** (a) — the zero of potential is at infinity, by convention.
**26.** (c) — $V = kq/r$; the $1/r^2$ form is the field.
**27.** (b) — the field points downhill in potential; the minus sign carries that meaning.
**28.** (d) — $C = 4\pi\varepsilon_0R$; a sphere of radius 9 km has $C\approx1\ \mu\text{F}$.
**29.** (c) — $1/C = 1/3+1/3+1/3 = 1$, so $C = 1\ \mu\text{F}$.
**30.** (a) — $Q = CV = 2\times10^{-6}\times100 = 2\times10^{-4}$ C $= 200\ \mu\text{C}$.
:::

**Set B — Understanding (18 questions)**

1. Two point charges are a distance $d$ apart. If the distance is doubled, the force becomes
   (a) $4F$ (b) $F/4$ (c) $F/2$ (d) $2F$
2. Two charges are held at a fixed distance. If each charge is doubled, the force
   (a) is unchanged (b) doubles (c) halves (d) becomes four times as large
3. Two equal positive charges $+q$ are $2a$ apart. At the midpoint
   (a) $E = 0$ and $V = 2kq/a$ (b) $E = 0$ and $V = 0$ (c) $E = 2kq/a^2$ and $V = 0$ (d) $E = kq/a^2$ and $V = 2kq/a$
4. Two equal and opposite charges $+q$ and $-q$ are $2a$ apart. At the midpoint
   (a) $E = 0$ and $V = 0$ (b) $E = 2kq/a^2$ and $V = 2kq/a$ (c) $E = 2kq/a^2$ and $V = 0$ (d) $E = 0$ and $V = 2kq/a$
5. A charge inside a closed surface is moved from one point to another inside it. The total flux through the surface
   (a) changes (b) stays the same (c) becomes zero (d) depends on the shape of the surface
6. A charge is placed just outside a closed surface. The net flux through the surface is
   (a) $q/\varepsilon_0$ (b) $q/2\varepsilon_0$ (c) infinite (d) zero
7. A capacitor is charged and then disconnected from the battery. Its plates are pulled apart. The charge, potential difference and stored energy respectively
   (a) stay the same, increase, increase (b) decrease, increase, increase (c) stay the same, decrease, decrease (d) stay the same, increase, decrease
8. A capacitor connected to a battery has a dielectric inserted between its plates. Which is correct?
   (a) $Q$ same, $V$ increases (b) $Q$ decreases, $V$ same (c) $Q$ increases, $V$ same (d) $Q$ same, $U$ decreases
9. A charged capacitor is disconnected, then a dielectric is inserted. The potential difference across it
   (a) increases $K$ times (b) stays the same (c) becomes zero (d) falls to $V/K$
10. Two capacitors of $2\ \mu\text{F}$ and $4\ \mu\text{F}$ are in series across 12 V. The charge on each is
   (a) $8\ \mu\text{C}$ (b) $16\ \mu\text{C}$ (c) $4\ \mu\text{C}$ (d) $48\ \mu\text{C}$
11. Two capacitors of $2\ \mu\text{F}$ and $4\ \mu\text{F}$ are in parallel across 12 V. Their charges are
   (a) $16\ \mu\text{C}$ each (b) $8\ \mu\text{C}$ and $16\ \mu\text{C}$ (c) $24\ \mu\text{C}$ and $48\ \mu\text{C}$ (d) $12\ \mu\text{C}$ and $24\ \mu\text{C}$
12. A $2\ \mu\text{F}$ capacitor charged to 100 V is connected to an uncharged $2\ \mu\text{F}$ capacitor. The common potential is
   (a) 50 V (b) 100 V (c) 25 V (d) zero
13. A $2\ \mu\text{F}$ capacitor at 100 V shares its charge with an identical uncharged capacitor. The fraction of the initial energy lost is
   (a) none (b) 25 % (c) 75 % (d) 50 %
14. The field inside a hollow charged conducting sphere is zero. The potential inside is
   (a) zero (b) constant and equal to the surface value (c) increasing outward (d) decreasing outward
15. An electron enters a uniform electric field moving along the field. Its path is
   (a) circular (b) parabolic (c) a straight line with changing speed (d) a straight line with constant speed
16. A positive charge is moved from a point at 10 V to a point at 20 V. The work done by the external agent is
   (a) positive (b) negative (c) zero (d) infinite
17. The electric field just outside a charged conductor is
   (a) zero (b) parallel to the surface (c) perpendicular to the surface (d) at 45° to the surface
18. Capacitors $C$ and $2C$ are joined in series. The larger charge is on
   (a) neither; both have the same charge (b) $C$ (c) $2C$ (d) it depends on the applied voltage

::: note Answers and explanations — Set B
**1.** (b) — $F\propto1/d^2$; doubling $d$ gives one quarter.
**2.** (d) — $F\propto q_1q_2$; doubling both multiplies the force by 4.
**3.** (a) — the two fields cancel at the midpoint, but the two potentials add: $kq/a+kq/a$.
**4.** (c) — both fields point from $+$ to $-$, so they add to $2kq/a^2$; the potentials cancel because they have opposite signs.
**5.** (b) — flux depends only on the enclosed charge, not on where it sits.
**6.** (d) — every line that enters the surface also leaves it; the net enclosed charge is zero.
**7.** (a) — isolated means $Q$ fixed; $C\propto1/d$ falls, so $V = Q/C$ and $U = Q^2/2C$ both rise.
**8.** (c) — the battery holds $V$ fixed; $C$ rises to $KC$, so $Q = CV$ rises.
**9.** (d) — $Q$ is fixed and $C$ rises $K$ times, so $V = Q/C$ falls to $V/K$.
**10.** (b) — $C = (2\times4)/6 = 1.33\ \mu\text{F}$, so $Q = 1.33\times12 = 16\ \mu\text{C}$ on each.
**11.** (c) — parallel means the same 12 V: $2\times12 = 24\ \mu\text{C}$ and $4\times12 = 48\ \mu\text{C}$.
**12.** (a) — equal capacitors share the charge equally, so the voltage halves.
**13.** (d) — half the energy is lost for any two equal capacitors; the loss is $C(V_1-V_2)^2/4$.
**14.** (b) — $E = 0$ inside means $V$ does not change with position; it keeps the surface value.
**15.** (c) — the force is along the velocity, so there is no sideways deflection; the electron speeds up or slows down.
**16.** (a) — the charge moves to a higher potential, so the agent must do positive work, $q(20-10)$.
**17.** (c) — any tangential component would move surface charge, so the field must be normal to the surface.
**18.** (a) — series capacitors carry the same charge, whatever their capacitances.
:::

**Set C — Application (14 questions)**

1. Three charges of $1\ \mu\text{C}$ each sit at the corners of an equilateral triangle of side 10 cm. The net force on one charge is about
   (a) 0.90 N (b) 2.70 N (c) 1.56 N (d) 0.78 N
2. Charges of $2\ \mu\text{C}$ and $3\ \mu\text{C}$ are 30 cm apart in air. The force between them is
   (a) 0.60 N (b) 0.18 N (c) 1.80 N (d) 6.0 N
3. The electric field 30 cm from a $2\ \mu\text{C}$ point charge is
   (a) $6\times10^4$ N C⁻¹ (b) $6\times10^5$ N C⁻¹ (c) $2\times10^4$ N C⁻¹ (d) $2\times10^5$ N C⁻¹
4. A charge of $2\ \mu\text{C}$ is moved from a point at 50 V to a point at 150 V. The work done by the external agent is
   (a) $1\times10^{-4}$ J (b) $2\times10^{-4}$ J (c) $2\times10^{-6}$ J (d) $3\times10^{-4}$ J
5. A cube encloses a charge of $1\ \mu\text{C}$ at its centre. The flux through one face is about
   (a) $1.9\times10^4$ N m² C⁻¹ (b) $1.1\times10^5$ N m² C⁻¹ (c) $6.8\times10^5$ N m² C⁻¹ (d) $1.1\times10^4$ N m² C⁻¹
6. A conducting sphere of radius 10 cm carries $1\ \mu\text{C}$. The field 5 cm from its centre is
   (a) zero (b) $9\times10^5$ N C⁻¹ (c) $2.3\times10^5$ N C⁻¹ (d) $1.8\times10^6$ N C⁻¹
7. A conducting sphere of radius 10 cm carries $1\ \mu\text{C}$. The potential at its centre is
   (a) zero (b) $4.5\times10^4$ V (c) $9\times10^5$ V (d) $9\times10^4$ V
8. A parallel-plate capacitor has plates of area $0.02\ \text{m}^2$ separated by 1 mm of air. Its capacitance is about
   (a) 17.7 pF (b) 177 pF (c) 885 pF (d) 88.5 pF
9. A parallel-plate capacitor of 177 pF in air is filled with a dielectric of constant 5 and connected to 100 V. The charge on its plates is
   (a) 88.5 nC (b) 17.7 nC (c) 8.85 nC (d) 177 nC
10. A $2\ \mu\text{F}$ capacitor is charged to 100 V and disconnected. The plates are then pulled apart until their separation is doubled. The new potential difference is
   (a) 200 V (b) 100 V (c) 50 V (d) 400 V
11. A $2\ \mu\text{F}$ capacitor charged to 100 V is connected to an uncharged $3\ \mu\text{F}$ capacitor. The common potential is
   (a) 60 V (b) 50 V (c) 20 V (d) 40 V
12. A $2\ \mu\text{F}$ capacitor charged to 100 V is connected to an uncharged $3\ \mu\text{F}$ capacitor. The energy lost in the wire is
   (a) 10 mJ (b) 6 mJ (c) 4 mJ (d) 2 mJ
13. The energy density of a field of $10^6$ V m⁻¹ in vacuum is about
   (a) 8.85 J m⁻³ (b) 4.43 J m⁻³ (c) 2.21 J m⁻³ (d) $4.43\times10^{-3}$ J m⁻³
14. The energy stored in a $2\ \mu\text{F}$ capacitor charged to 100 V is
   (a) 0.01 J (b) 0.2 J (c) 0.02 J (d) 1 J

::: note Answers and explanations — Set C
**1.** (c) — two forces of $kq^2/a^2 = 0.90$ N at 60° give $2(0.90)\cos30^{\circ} = 1.56$ N. Option (a) is one force alone; (d) is one force multiplied by $\cos30^{\circ}$.
**2.** (a) — $F = 9\times10^9\times2\times10^{-6}\times3\times10^{-6}/(0.30)^2 = 0.60$ N.
**3.** (d) — $E = kq/r^2 = 9\times10^9\times2\times10^{-6}/0.09 = 2\times10^5$ N C⁻¹. Option (a) is the potential, not the field.
**4.** (b) — $W = q\Delta V = 2\times10^{-6}\times100 = 2\times10^{-4}$ J.
**5.** (a) — total flux $= q/\varepsilon_0 = 1.13\times10^5$; one of six faces gets $1.9\times10^4$.
**6.** (a) — 5 cm is inside the conductor, where $E$ is always zero.
**7.** (d) — inside, $V$ is constant at the surface value $kQ/R = 9\times10^4$ V.
**8.** (b) — $C = 8.85\times10^{-12}\times0.02/10^{-3} = 1.77\times10^{-10}$ F $= 177$ pF.
**9.** (a) — $C = 5\times177 = 885$ pF, so $Q = CV = 885\times10^{-12}\times100 = 8.85\times10^{-8}$ C.
**10.** (a) — $Q$ fixed, $C$ halves, so $V = Q/C$ doubles to 200 V.
**11.** (d) — $V = (2\times100+0)/5 = 40$ V.
**12.** (b) — initial $0.010$ J, final $\frac12(5\times10^{-6})(40)^2 = 0.004$ J; loss $0.006$ J.
**13.** (b) — $u = \frac12\varepsilon_0E^2 = \frac12\times8.85\times10^{-12}\times10^{12} = 4.43$ J m⁻³.
**14.** (a) — $U = \frac12CV^2 = \frac12\times2\times10^{-6}\times10^4 = 0.01$ J.
:::
