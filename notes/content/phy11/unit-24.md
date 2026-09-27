---
subject: Physics
grade: 11
unit: 24
title: Nuclear physics
hours: 6
area: Modern Physics
---

Almost the whole mass of an atom sits in a nucleus about $10^{5}$ times smaller
than the atom itself. This unit is about that tiny object: how it was discovered,
how we describe it, and why rearranging its nucleons releases a million times
more energy per kilogram than burning coal. The single equation behind all of it
is Einstein's $E = mc^{2}$ — in nuclear physics, mass and energy are two ways of
writing the same thing.

::: key What the examiner asks from this unit
Two things appear every year: a numerical on mass defect, binding energy or
energy released in fission/fusion (always via $1\ \text{u} = 931.5\ \text{MeV}$),
and a question on the binding-energy-per-nucleon curve. Learn the curve, its
peak at $A \approx 56$, and what its two slopes mean.
:::

## 24.1 Nucleus: Discovery of nucleus

In 1911 the accepted picture was J. J. Thomson's "plum pudding" atom: positive
charge spread uniformly through the whole atom with electrons embedded in it. If
that were true, a fast alpha particle fired at a thin foil would pass through
almost undeflected, because the spread-out charge could never exert a large force.

Geiger and Marsden, working under Rutherford, fired alpha particles
(helium nuclei, energy about $5\ \text{MeV}$) from a radium source at a gold foil
only $\approx 10^{-7}\ \text{m}$ thick, and counted the flashes they produced on a
movable zinc-sulphide screen.

| Observation | Conclusion |
|---|---|
| Most alpha particles passed through with no deflection | the atom is mostly **empty space** |
| A small fraction were deflected through large angles | there is a concentrated, **positively charged** core that repels them |
| About 1 in 8000 was turned back through more than $90^{\circ}$ | that core is very **massive** and very **small** |

Rutherford's conclusion (1911) was the **nuclear model**: all the positive charge
and nearly all the mass of the atom are concentrated in a nucleus of radius about
$10^{-14}\ \text{m}$, while the electrons move around it at a distance of about
$10^{-10}\ \text{m}$. In his own words, the result was "as incredible as if you
fired a 15-inch shell at a piece of tissue paper and it came back and hit you."

```figure caption="Rutherford scattering. The deflection depends on the impact parameter $b$: only an alpha particle aimed almost straight at the nucleus is turned through a large angle, while distant ones pass practically undeviated."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle
fig, ax = plt.subplots(figsize=(5.0,3.4))

d, RMAX = 0.55, 7.0          # d = head-on distance of closest approach

def path(theta_deg, side):
    """Exact repulsive-Coulomb hyperbola deflected through theta_deg."""
    td = np.radians(theta_deg)
    b  = (d/2.0)/np.tan(td/2.0)
    e  = np.hypot(1.0, 2*b/d)
    p  = 2*b*b/d
    tm = np.arccos(1.0/e)
    lim = np.arccos(min((p/RMAX + 1.0)/e, 1.0))
    t = np.linspace(-lim, lim, 700)
    r = p/(e*np.cos(t) - 1.0)
    x, y = r*np.cos(t), r*np.sin(t)
    phi = tm - np.pi
    X = x*np.cos(phi) - y*np.sin(phi)
    Y = -(x*np.sin(phi) + y*np.cos(phi))
    return X, side*Y, b

RAYS = [(15, 1, ACCENT, (1.00, -0.10)), (30, 1, ACCENT, (0.70, 0.45)),
        (60, 1, ACCENT, (0.55, 0.55)), (120, -1, '#d9534f', (-0.55, -0.55)),
        (165, -1, '#d9534f', (-0.45, -0.60))]
btop = None
for th, s, c, off in RAYS:
    x, y, b = path(th, s)
    if th == 15: btop = b
    ax.plot(x, y, color=c, lw=1.4, zorder=3)
    ax.annotate('', xy=(x[34], y[34]), xytext=(x[0], y[0]),
                arrowprops=dict(arrowstyle='-|>', color=c, lw=1.2, mutation_scale=9), zorder=3)
    ax.annotate('', xy=(x[-1], y[-1]), xytext=(x[-40], y[-40]),
                arrowprops=dict(arrowstyle='-|>', color=c, lw=1.2, mutation_scale=9), zorder=3)
    ax.annotate(f'${th}^{{\\circ}}$', (x[-1]+off[0], y[-1]+off[1]),
                ha='center', va='center', fontsize=8.4, color=c, zorder=5)

ax.add_patch(Circle((0,0), 0.24, fc='#b8860b', ec=INK, lw=1.0, zorder=6))
ax.annotate('nucleus $+Ze$', (0.55,-0.68), ha='left', va='center',
            fontsize=8.8, color=INK, zorder=6)
ax.plot([-7.2, 9.4], [0,0], color=MUTED, lw=0.7, ls=':', zorder=1)
ax.plot([-7.2, -1.4], [btop, btop], color=MUTED, lw=0.7, ls=':', zorder=2)
ax.annotate('', xy=(-6.1,0.0), xytext=(-6.1,btop),
            arrowprops=dict(arrowstyle='<|-|>', color=INK, lw=1.0, mutation_scale=8), zorder=4)
ax.annotate('$b$', (-6.32, btop/2), ha='right', va='center', fontsize=9.5, color=INK)
ax.annotate('incident\nalpha beam', (-7.1, 4.6), ha='left', va='center',
            fontsize=8.8, color=MUTED)

ax.plot([1.1, 2.1], [-6.05,-6.05], color=ACCENT, lw=1.7, zorder=5)
ax.annotate('small deflection — almost all of them', (2.4,-6.05),
            ha='left', va='center', fontsize=8.4, color=ACCENT)
ax.plot([1.1, 2.1], [-7.25,-7.25], color='#d9534f', lw=1.7, zorder=5)
ax.annotate('scattered beyond $90^{\\circ}$ — about 1 in 8000', (2.4,-7.25),
            ha='left', va='center', fontsize=8.4, color='#d9534f')

ax.set_xlim(-7.3, 11.6); ax.set_ylim(-8.1, 7.1)
ax.set_aspect('equal'); ax.axis('off')
```

How big is the nucleus? An alpha particle fired straight at it never touches
it: the electrostatic repulsion stops it first. The point where it stops gives an
upper limit on the nuclear radius.

::: derivation Distance of closest approach
An alpha particle of kinetic energy $E$ is fired **head-on** at a nucleus of
atomic number $Z$. The alpha particle carries charge $+2e$, the nucleus carries
$+Ze$, so the two repel. As the alpha particle comes closer it slows down, and
at the closest point it has stopped completely for an instant. Call that
separation $r_0$.

**Step 1 — the energy far away.** At a large distance the potential energy of
the two charges is zero, so all the energy of the alpha particle is kinetic:

$$ E_{\text{far}} = E $$

**Step 2 — the energy at the closest point.** Here the speed is zero, so the
kinetic energy is zero. All the energy is now electrostatic potential energy of
two charges $2e$ and $Ze$ a distance $r_0$ apart:

$$ E_{\text{near}} = \frac{1}{4\pi\varepsilon_0}\cdot\frac{(2e)(Ze)}{r_0}
= \frac{1}{4\pi\varepsilon_0}\cdot\frac{2Ze^{2}}{r_0} $$

**Step 3 — energy is conserved,** so the two expressions are equal:

$$ E = \frac{1}{4\pi\varepsilon_0}\cdot\frac{2Ze^{2}}{r_0} $$

**Step 4 — multiply both sides by $r_0$:**

$$ E\,r_0 = \frac{2Ze^{2}}{4\pi\varepsilon_0} $$

**Step 5 — divide both sides by $E$** to make $r_0$ the subject:

$$ r_0 = \frac{2Ze^{2}}{4\pi\varepsilon_0 E} $$
:::

$r_0$ is the **distance of closest approach**. Because the alpha particle is
turned back before touching, the true nuclear radius must be smaller than $r_0$
— so this calculation puts an upper limit on the size of the nucleus.
Later work completed the picture: Rutherford identified the **proton**
in 1919, and Chadwick discovered the neutral **neutron** in 1932. Protons and
neutrons together are called **nucleons**, and they are held together by the
short-range, strongly attractive **nuclear force**, which acts only over about
$10^{-15}\ \text{m}$ but is far stronger than the electrostatic repulsion between
protons at that range.

## 24.2 Nuclear density, Mass number, Atomic number

::: definition Atomic number and mass number
The **atomic number** $Z$ is the number of protons in the nucleus (and so the
number of electrons in the neutral atom). The **mass number** $A$ is the total
number of nucleons, protons plus neutrons. The number of neutrons is
$N = A - Z$.
:::

A nuclide is written with the mass number as a left superscript and the atomic
number as a left subscript, for example ²³⁵₉₂U — uranium with $Z = 92$,
$A = 235$, hence $N = 143$ neutrons.

Experiments in which fast electrons are scattered from nuclei show that the
nuclear radius depends only on the number of nucleons:

$$ R = R_0 A^{1/3}, \qquad R_0 = 1.2\times10^{-15}\ \text{m} = 1.2\ \text{fm} $$

::: derivation Why nuclear density is the same for every nucleus
The volume of a nucleus is

$$ V = \frac{4}{3}\pi R^{3} = \frac{4}{3}\pi R_0^{3}A $$

so the volume is directly proportional to $A$. The mass of the nucleus is
approximately $A m_n$, where $m_n \approx 1.67\times10^{-27}\ \text{kg}$ is the
mass of one nucleon. Hence

$$ \rho = \frac{Am_n}{\frac{4}{3}\pi R_0^{3}A} = \frac{3m_n}{4\pi R_0^{3}} $$

$A$ cancels: **nuclear density is independent of the mass number**, the same for
hydrogen and for uranium. Numerically $\rho \approx 2.3\times10^{17}\ \text{kg m}^{-3}$,
about $10^{14}$ times the density of water. This constancy tells us that nucleons
are packed like marbles in a bag — the nuclear force saturates, each nucleon
binding only to its nearest neighbours.
:::

::: example Worked example 24.1
**Problem.** Find the radius and the density of a nucleus with mass number
$A = 125$. Take $R_0 = 1.2\ \text{fm}$ and the mass of a nucleon as
$1.67\times10^{-27}\ \text{kg}$.

**Solution.** Since $125^{1/3} = 5$,

$$ R = R_0A^{1/3} = 1.2\times10^{-15}\times5 = 6.0\times10^{-15}\ \text{m} $$

Volume:

$$ V = \frac{4}{3}\pi R^{3} = \frac{4}{3}\pi(6.0\times10^{-15})^{3}
= 9.05\times10^{-43}\ \text{m}^{3} $$

Mass $= 125\times1.67\times10^{-27} = 2.09\times10^{-25}\ \text{kg}$. Hence

$$ \rho = \frac{2.09\times10^{-25}}{9.05\times10^{-43}} = 2.3\times10^{17}\ \text{kg m}^{-3} $$
:::

## 24.3 Atomic mass, Isotopes

Nuclear masses are far too small for the kilogram, so we use the **unified atomic
mass unit** (u), also called the amu.

::: definition Atomic mass unit
One atomic mass unit is exactly one-twelfth of the mass of one neutral atom of
carbon-12:
$$ 1\ \text{u} = 1.6605\times10^{-27}\ \text{kg} $$
:::

| Particle | Mass (u) | Mass (kg) | Charge |
|---|---|---|---|
| Proton | $1.007276$ | $1.6726\times10^{-27}$ | $+e$ |
| Neutron | $1.008665$ | $1.6749\times10^{-27}$ | $0$ |
| Electron | $0.000549$ | $9.109\times10^{-31}$ | $-e$ |
| ¹H atom | $1.007825$ | — | neutral |

The **atomic mass** of an element is the mass of one of its atoms in u. It is
close to, but never exactly equal to, the mass number $A$ — partly because
protons and neutrons are not exactly $1\ \text{u}$, and mainly because some mass
is "missing" as binding energy (§24.5).

::: definition Isotopes
Isotopes are atoms of the same element that have the **same atomic number $Z$ but
different mass numbers $A$** — that is, the same number of protons but different
numbers of neutrons. They are chemically identical but physically different.
:::

| Term | Same | Examples |
|---|---|---|
| Isotopes | $Z$ | ¹H, ²H, ³H; ³⁵Cl, ³⁷Cl; ²³⁵U, ²³⁸U |
| Isobars | $A$ | ⁴⁰Ar, ⁴⁰K, ⁴⁰Ca |
| Isotones | $N = A - Z$ | ³⁶S, ³⁷Cl, ³⁸Ar (each $N = 20$) |

The atomic mass quoted in a data book is the **weighted average** over the
naturally occurring isotopes, which is why chlorine is listed as $35.45$ and not
as a whole number.

::: example Worked example 24.2
**Problem.** Natural chlorine is $75.77\ \%$ ³⁵Cl (atomic mass $34.96885\ \text{u}$)
and $24.23\ \%$ ³⁷Cl (atomic mass $36.96590\ \text{u}$). Find its average atomic
mass.

**Solution.**

$$ \bar{M} = \frac{75.77\times34.96885 + 24.23\times36.96590}{100} $$

The two products are $2649.59$ and $895.68$, so

$$ \bar{M} = \frac{3545.27}{100} = 35.45\ \text{u} $$
:::

## 24.4 Einstein's mass-energy relation

Einstein's special theory of relativity (1905) showed that mass and energy are
equivalent: a body of mass $m$ possesses a rest energy

$$ E = mc^{2} $$

with $c = 3.0\times10^{8}\ \text{m s}^{-1}$. If a system loses mass $\Delta m$, it
releases energy $\Delta E = \Delta m\,c^{2}$. Because $c^{2}$ is enormous, a tiny
mass change gives a huge energy: this is why nuclear reactions are millions of
times more energetic than chemical ones, in which the mass change is far too
small to detect.

### Where $E = mc^{2}$ comes from

Relativity says that mass is not a fixed property of a body. A body whose mass
is $m_0$ when it is at rest — its **rest mass** — behaves, when it moves at
speed $v$, as though its mass were

$$ m = \frac{m_0}{\sqrt{1 - v^{2}/c^{2}}} $$

At everyday speeds $v/c$ is so small that $m$ and $m_0$ agree to many decimal
places, which is why nobody noticed for two hundred years. As $v$ approaches
$c$ the square root approaches zero and $m$ grows without limit. The mass-energy
relation follows from this one formula together with the ordinary work-energy
theorem.

::: derivation Einstein's mass-energy relation $E = mc^{2}$
**Step 1 — work done becomes kinetic energy.** A force $F$ acting through a
small distance $dx$ does work $F\,dx$, and all of that work goes into the
kinetic energy of the body:

$$ dE_k = F\,dx $$

**Step 2 — write the force as a rate of change of momentum.** Newton's second
law in its general form is $F = \frac{d(mv)}{dt}$, so

$$ dE_k = \frac{d(mv)}{dt}\,dx $$

**Step 3 — rearrange the differentials.** $dx$ and $dt$ are just numbers, so we
may group them as $dx/dt$, which is the speed $v$:

$$ dE_k = d(mv)\cdot\frac{dx}{dt} = v\,d(mv) $$

**Step 4 — expand the product $d(mv)$.** Both $m$ and $v$ are changing now, so
the product rule gives $d(mv) = m\,dv + v\,dm$:

$$ dE_k = v(m\,dv + v\,dm) = mv\,dv + v^{2}dm \qquad (1) $$

**Step 5 — go back to the mass formula and clear the square root.** Squaring
$m = m_0/\sqrt{1-v^{2}/c^{2}}$ gives

$$ m^{2}\left(1 - \frac{v^{2}}{c^{2}}\right) = m_0^{2} $$

**Step 6 — multiply every term by $c^{2}$** so there are no fractions left:

$$ m^{2}c^{2} - m^{2}v^{2} = m_0^{2}c^{2} $$

**Step 7 — differentiate both sides.** The right-hand side is a constant, so
its differential is zero. Differentiating $m^{2}c^{2}$ gives $2mc^{2}dm$, and
differentiating $m^{2}v^{2}$ by the product rule gives
$2mv^{2}dm + 2m^{2}v\,dv$. Hence

$$ 2mc^{2}dm - 2mv^{2}dm - 2m^{2}v\,dv = 0 $$

**Step 8 — divide every term by $2m$:**

$$ c^{2}dm - v^{2}dm - mv\,dv = 0 $$

**Step 9 — move the last two terms across:**

$$ c^{2}dm = mv\,dv + v^{2}dm \qquad (2) $$

**Step 10 — compare (1) and (2).** Their right-hand sides are word for word the
same, so their left-hand sides must be equal:

$$ dE_k = c^{2}dm $$

**Step 11 — add up all the small bits.** Integrate from rest, where the mass is
$m_0$ and the kinetic energy is zero, up to speed $v$, where the mass is $m$ and
the kinetic energy is $E_k$:

$$ \int_{0}^{E_k} dE_k = c^{2}\int_{m_0}^{m} dm $$

$$ E_k = c^{2}(m - m_0) = (m - m_0)c^{2} $$

**Step 12 — read what this says.** Giving the body kinetic energy $E_k$ has
increased its mass by exactly $E_k/c^{2}$. Energy *has* mass. Turning the
statement round, the body already owned a hidden **rest energy** $m_0c^{2}$
before it ever moved, and its total energy is

$$ E = E_k + m_0c^{2} = (m - m_0)c^{2} + m_0c^{2} = mc^{2} $$
:::

::: key The conversion every nuclear numerical needs
$$ 1\ \text{u} = 931.5\ \text{MeV}/c^{2} $$
So a mass defect expressed in u is turned into energy simply by multiplying by
$931.5$ to get MeV. Also $1\ \text{eV} = 1.6\times10^{-19}\ \text{J}$ and
$1\ \text{MeV} = 1.6\times10^{-13}\ \text{J}$.
:::

::: example Worked example 24.3
**Problem.** (a) Show that $1\ \text{u}$ is equivalent to about
$931\ \text{MeV}$. (b) How much energy would be released if $1.0\ \text{g}$ of
matter were completely converted into energy?

**Solution.**

(a) $E = mc^{2} = (1.6605\times10^{-27})(2.998\times10^{8})^{2}
= 1.4924\times10^{-10}\ \text{J}$. Converting to MeV,

$$ E = \frac{1.4924\times10^{-10}}{1.602\times10^{-13}} = 931.5\ \text{MeV} $$

(b) $E = mc^{2} = (1.0\times10^{-3})(3.0\times10^{8})^{2} = 9.0\times10^{13}\ \text{J}$.

For comparison, burning $1\ \text{g}$ of coal gives about $3\times10^{4}\ \text{J}$
— roughly three billion times less.
:::

## 24.5 Mass defect, packing fraction, BE per nucleon

Measure the mass of a helium nucleus and compare it with the masses of the two
protons and two neutrons it contains: the nucleus is **lighter**. The missing
mass is called the **mass defect**.

::: definition Mass defect and binding energy
The **mass defect** is the difference between the total mass of the free nucleons
and the actual mass of the nucleus:
$$ \Delta m = [Zm_p + (A-Z)m_n] - M $$
The **binding energy** is the energy equivalent of the mass defect,
$B = \Delta m\,c^{2}$. It is the energy that must be supplied to break the nucleus
completely into free nucleons — and the energy released when they come together.
:::

::: caution Use atomic masses consistently
If you use the mass of the ¹H **atom** ($1.007825\ \text{u}$) instead of the
proton, you must also use the **atomic** mass of the nuclide, not the nuclear
mass. The $Z$ electron masses then cancel out. Mixing the two conventions is the
commonest source of wrong binding energies in exams.
:::

The **packing fraction** measures the mass defect per nucleon in a scaled form:

$$ f = \frac{M - A}{A} $$

where $M$ is the atomic mass in u and $A$ the mass number; it is usually quoted
after multiplying by $10^{4}$. A **negative** packing fraction means the nuclide
is lighter than $A$ units and so is stable; nuclides near $A \approx 56$ have the
most negative values. For ¹⁶O, $M = 15.9949\ \text{u}$, so
$f = (15.9949-16)/16 = -3.2\times10^{-4}$.

The real measure of stability, however, is the **binding energy per nucleon**,
$B/A$. Plotting it against $A$ gives the most important graph in nuclear physics.

```figure caption="Binding energy per nucleon against mass number. The peak is at $A \approx 56$ (iron), about $8.8$ MeV per nucleon."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,3.0))
A = np.array([2,3,4,6,7,9,12,14,16,20,23,27,32,40,56,62,84,107,120,140,184,208,235,238])
B = np.array([1.112,2.827,7.074,5.332,5.606,6.463,7.680,7.476,7.976,8.032,8.111,
              8.332,8.493,8.551,8.790,8.795,8.717,8.554,8.504,8.376,7.950,7.867,
              7.591,7.570])
ax.plot(A, B, color=ACCENT, lw=1.7, zorder=3)
ax.plot(A, B, 'o', color=ACCENT, ms=3.2, zorder=4)
ax.axhline(8.8, color=MUTED, lw=0.9, ls=':')

for a, b, lab, off in [(2,1.112,'$^{2}$H',(6,-4)),
                       (56,8.790,'$^{56}$Fe',(2,7)), (235,7.591,'$^{235}$U',(-4,-14))]:
    ax.annotate(lab, (a,b), textcoords='offset points', xytext=off,
                fontsize=9.0, color=INK)
ax.annotate('$^{4}$He', (4,7.074), textcoords='offset points', xytext=(30,-13),
            fontsize=9.0, color=INK,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.8))

ax.annotate('', xy=(46,4.6), xytext=(10,4.6),
            arrowprops=dict(arrowstyle='-|>', color='#2e8b57', lw=1.4, mutation_scale=10))
ax.annotate('fusion', (28,4.05), ha='center', va='top', color='#2e8b57', fontsize=9.0)
ax.annotate('', xy=(110,4.6), xytext=(215,4.6),
            arrowprops=dict(arrowstyle='-|>', color='#d9534f', lw=1.4, mutation_scale=10))
ax.annotate('fission', (163,4.05), ha='center', va='top', color='#d9534f', fontsize=9.0)

ax.set_xlabel('mass number  $A$')
ax.set_ylabel('$B/A$  (MeV per nucleon)')
ax.set_xlim(0,250); ax.set_ylim(0,10)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=.5)
```

Read the curve carefully — four facts are examined again and again:

1. $B/A$ rises steeply for light nuclei, with sharp peaks at ⁴He, ¹²C and ¹⁶O
   (nuclei built of whole alpha particles are unusually stable).
2. It is nearly flat at about $8.5$ to $8.8\ \text{MeV}$ for $30 < A < 120$; the
   maximum, $8.79\ \text{MeV}$, is at ⁵⁶Fe. These nuclei are the most stable.
3. It falls slowly for heavy nuclei (to $7.6\ \text{MeV}$ for ²³⁵U) because the
   long-range electrostatic repulsion between many protons grows faster than the
   short-range nuclear attraction.
4. Therefore energy is released **either** by joining very light nuclei
   (**fusion**) **or** by splitting very heavy ones (**fission**) — both move the
   products towards the peak, so the total binding energy increases.

::: example Worked example 24.4
**Problem.** Calculate the mass defect, the binding energy, and the binding energy
per nucleon of the helium nucleus ⁴He. Given: mass of ¹H atom
$= 1.007825\ \text{u}$, mass of neutron $= 1.008665\ \text{u}$, atomic mass of ⁴He
$= 4.002603\ \text{u}$.

**Solution.** Helium has $Z = 2$, $A = 4$, so $N = 2$.

$$ \Delta m = 2(1.007825) + 2(1.008665) - 4.002603 $$

$$ \Delta m = 2.015650 + 2.017330 - 4.002603 = 0.030377\ \text{u} $$

Binding energy:

$$ B = 0.030377\times931.5 = 28.3\ \text{MeV} $$

Binding energy per nucleon:

$$ \frac{B}{A} = \frac{28.3}{4} = 7.07\ \text{MeV per nucleon} $$

This is well above its neighbours on the curve, which is why the alpha particle
is so stable and is emitted as a unit in radioactive decay.
:::

## 24.6 Creation and annihilation

Because mass and energy are interchangeable, energy can turn into matter and
matter back into energy — but only in particle–antiparticle pairs, so that charge
is conserved.

**Pair production (creation).** A high-energy photon passing close to a heavy
nucleus can vanish, creating an electron and a positron:

γ → e⁻ + e⁺

The photon must supply at least the rest energy of both particles. Each has rest
energy $m_ec^{2} = 0.511\ \text{MeV}$, so the **threshold energy** is

$$ E_{min} = 2m_ec^{2} = 1.02\ \text{MeV} $$

Any extra photon energy appears as kinetic energy of the pair. The nearby nucleus
is essential: it recoils and takes up momentum, because a lone photon cannot
produce a pair and conserve energy and momentum at the same time.

**Annihilation.** The reverse process: when a positron meets an electron, both
disappear and their entire mass becomes radiation. Two photons are produced,
travelling in opposite directions,

e⁻ + e⁺ → γ + γ

each of energy $0.511\ \text{MeV}$ when the particles were nearly at rest. Two
photons are needed, not one, so that the total momentum stays zero. This process
is the basis of the **PET scan** used in hospitals.

```figure caption="Creation (pair production) needs a photon of at least $1.02$ MeV and a nearby nucleus; annihilation turns an electron-positron pair into two $0.511$ MeV photons moving oppositely."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle
fig, axes = plt.subplots(1, 2, figsize=(5.2,2.7))

def photon(ax, p0, p1, color, amp=0.11, n=7.0):
    p0 = np.array(p0,float); p1 = np.array(p1,float)
    d = p1-p0; L = np.hypot(*d); u = d/L; nv = np.array([-u[1],u[0]])
    t = np.linspace(0, L, 300)
    pts = p0 + np.outer(t,u) + np.outer(amp*np.sin(2*np.pi*n*t/L), nv)
    ax.plot(pts[:,0], pts[:,1], color=color, lw=1.5, zorder=3)
    ax.annotate('', xy=tuple(p1), xytext=tuple(p1-0.12*u),
                arrowprops=dict(arrowstyle='-|>', color=color, lw=1.4, mutation_scale=10), zorder=3)

def particle(ax, p0, p1, color, lab, off):
    ax.annotate('', xy=tuple(p1), xytext=tuple(p0),
                arrowprops=dict(arrowstyle='-|>', color=color, lw=1.6, mutation_scale=11), zorder=3)
    if lab:
        ax.annotate(lab, (p1[0]+off[0], p1[1]+off[1]), ha='center', va='center',
                    fontsize=9.2, color=color)

# --- pair production ---
ax = axes[0]
photon(ax, (0.10,1.15), (1.28,1.15), '#b8860b')
ax.annotate('$\\gamma$   ≥ 1.02 MeV', (0.10,1.62), ha='left', va='center',
            fontsize=8.6, color='#b8860b')
ax.add_patch(Circle((1.48,1.15), 0.15, fc=MUTED, ec=INK, lw=0.9, zorder=4))
ax.annotate('nucleus', (1.48,0.86), ha='center', va='top', fontsize=8.4, color=INK)
particle(ax, (1.63,1.26), (2.58,2.02), SERIES[0], '$e^{-}$', (0.24,0.10))
particle(ax, (1.63,1.04), (2.58,0.28), SERIES[1], '$e^{+}$', (0.24,-0.10))
ax.set_title('creation  (pair production)', fontsize=9.2)
ax.set_xlim(0.0,3.15); ax.set_ylim(0.05,2.35); ax.axis('off')

# --- annihilation ---
ax = axes[1]
particle(ax, (0.15,1.15), (1.30,1.15), SERIES[0], '', (0,0))
ax.annotate('$e^{-}$', (0.60,1.40), ha='center', fontsize=9.2, color=SERIES[0])
particle(ax, (2.85,1.15), (1.70,1.15), SERIES[1], '', (0,0))
ax.annotate('$e^{+}$', (2.42,1.40), ha='center', fontsize=9.2, color=SERIES[1])
ax.plot([1.50],[1.15],'*', color=INK, ms=11, zorder=5)
photon(ax, (1.50,1.03), (1.50,0.18), '#b8860b')
photon(ax, (1.50,1.27), (1.50,2.12), '#b8860b')
ax.annotate('$\\gamma$   0.511 MeV', (1.80,1.92), ha='left', va='center',
            fontsize=8.6, color='#b8860b')
ax.annotate('$\\gamma$   0.511 MeV', (1.80,0.38), ha='left', va='center',
            fontsize=8.6, color='#b8860b')
ax.set_title('annihilation', fontsize=9.2)
ax.set_xlim(0.0,3.6); ax.set_ylim(0.05,2.35); ax.axis('off')
```

## 24.7 Nuclear fission and fusion; energy released

::: definition Nuclear fission
Nuclear fission is the splitting of a heavy nucleus into two nuclei of comparable
size, together with two or three neutrons and a large release of energy, when it
absorbs a slow (thermal) neutron.
:::

A typical fission of uranium-235 is

²³⁵U + ¹n → ¹⁴¹Ba + ⁹²Kr + 3 ¹n + 200 MeV

The $200\ \text{MeV}$ is not a fact to be memorised — it can be read straight off
the binding-energy-per-nucleon curve.

::: derivation Where the 200 MeV of a fission comes from
**Step 1 — count the nucleons.** The ²³⁵U nucleus absorbs one neutron, so the
nucleus that actually splits has $A = 235 + 1 = 236$ nucleons. Nucleons are
neither created nor destroyed, so the products between them also hold $236$
nucleons.

**Step 2 — total binding energy before the split.** From the curve, uranium sits
at about $7.6\ \text{MeV}$ per nucleon. Total binding energy is
(binding energy per nucleon) $\times$ (number of nucleons):

$$ B_{\text{before}} = 236 \times 7.6 = 1794\ \text{MeV} $$

**Step 3 — total binding energy after the split.** The fragments have mass
numbers near $141$ and $92$, which lie close to the top of the curve at about
$8.5\ \text{MeV}$ per nucleon. Counting the same $236$ nucleons,

$$ B_{\text{after}} = 236 \times 8.5 = 2006\ \text{MeV} $$

**Step 4 — subtract.** The products are held together *more tightly* than the
uranium was. Binding energy that the system did not have before must have been
supplied from somewhere — it comes out of the rest mass, and appears as the
energy released:

$$ Q = B_{\text{after}} - B_{\text{before}} = 2006 - 1794 = 212\ \text{MeV} $$

which is the familiar "about $200\ \text{MeV}$ per fission". The same sum is
quicker per nucleon: each of the $236$ nucleons gains
$8.5 - 7.6 = 0.9\ \text{MeV}$, and $236 \times 0.9 \approx 212\ \text{MeV}$.
:::

About $80\ \%$ of that energy appears immediately as kinetic energy of the two
fragments, which is why the fuel gets hot; the rest is carried by the neutrons,
by prompt gamma rays, and by the radiation from the fragments as they later
decay.

### Chain reaction and critical mass

Each fission releases two or three neutrons, and each of those can split another
nucleus, which releases more neutrons still.

::: definition Chain reaction, multiplication factor and critical mass
A **chain reaction** is a self-sustaining series of fissions in which neutrons
produced by one fission go on to cause further fissions. Its state is measured
by the **neutron multiplication factor** $k$:

$$ k = \frac{\text{number of fissions in one generation}}
{\text{number of fissions in the generation before}} $$

- $k < 1$ — **subcritical**: each generation is smaller and the reaction dies out.
- $k = 1$ — **critical**: the rate is steady. This is how a power reactor is run.
- $k > 1$ — **supercritical**: the rate grows generation after generation. This
  is an atomic bomb.

The **critical mass** is the smallest mass of fissile material for which $k$ can
reach $1$. Below it too many neutrons leak out through the surface before they
meet a nucleus. The reason is geometric: volume grows as $r^{3}$ but surface
area only as $r^{2}$, so a bigger lump loses a smaller *fraction* of its
neutrons. For pure ²³⁵U as a bare sphere the critical mass is about
$52\ \text{kg}$, and much less if a neutron reflector surrounds it.
:::

```figure caption="A chain reaction. Each fission of a ²³⁵U nucleus releases about $200$ MeV and two or three neutrons, which can trigger further fissions."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle
fig, ax = plt.subplots(figsize=(5.0,3.0))

def nucleus(x, y, r=0.20):
    ax.add_patch(Circle((x,y), r, fc='#dfe8f3', ec=ACCENT, lw=1.3, zorder=4))
    ax.annotate('U', (x,y), ha='center', va='center', fontsize=8.4, color=INK, zorder=5)

def neutron(p0, p1, color=INK, lw=1.3):
    ax.annotate('', xy=tuple(p1), xytext=tuple(p0),
                arrowprops=dict(arrowstyle='-|>', color=color, lw=lw, mutation_scale=9), zorder=3)

def frag(x, y, lab, dy):
    ax.add_patch(Circle((x,y), 0.12, fc='#f3d9d8', ec='#d9534f', lw=1.0, zorder=4))
    ax.annotate(lab, (x, y+dy), ha='center', va='center', fontsize=7.8, color='#d9534f')

neutron((0.02,1.40),(0.68,1.40), color='#2e8b57', lw=1.6)
ax.annotate('slow\nneutron', (0.35,1.90), ha='center', va='center', fontsize=8.0, color='#2e8b57')
nucleus(0.95, 1.40)
frag(1.40, 2.16, 'Ba', 0.28); frag(1.40, 0.64, 'Kr', -0.28)
neutron((1.12,1.54),(1.30,1.98), color='#d9534f', lw=1.0)
neutron((1.12,1.26),(1.30,0.82), color='#d9534f', lw=1.0)

targets = [(2.80,2.45),(2.80,1.40),(2.80,0.35)]
for tx,ty in targets:
    neutron((1.18,1.40),(tx-0.26,ty), color='#2e8b57')
    nucleus(tx, ty)
    for dy in (0.40,0.0,-0.40):
        neutron((tx+0.24,ty),(tx+0.82,ty+dy), color='#2e8b57', lw=1.0)

ax.annotate('each fission:\n$+\\ 200$ MeV', (4.42,1.40), ha='center', va='center',
            fontsize=8.8, color=INK)
ax.annotate('1st generation', (0.95,-0.12), ha='center', va='center', fontsize=8.4, color=MUTED)
ax.annotate('2nd generation', (2.80,-0.55), ha='center', va='center', fontsize=8.4, color=MUTED)
ax.set_xlim(-0.05,5.45); ax.set_ylim(-0.78,2.95); ax.axis('off')
```

### Parts of a nuclear reactor

A reactor is simply a chain reaction held permanently at $k = 1$ with its heat
taken away and used.

| Part | Material | Function |
|---|---|---|
| Fuel rods | uranium enriched to 2–3 % ²³⁵U | supply the nuclei that fission |
| Moderator | graphite, heavy water (D₂O) or ordinary water | slows the fast neutrons (about 2 MeV) down to thermal speeds (about 0.025 eV), which ²³⁵U captures far more readily |
| Control rods | boron or cadmium | absorb surplus neutrons; pushed in to slow the chain, drawn out to speed it up, holding $k$ at exactly 1 |
| Coolant | water, CO₂ or liquid sodium | carries heat from the core to the heat exchanger |
| Heat exchanger | — | boils water to steam, which drives a turbine and generator |
| Shielding | thick concrete and lead | absorbs escaping neutrons and gamma rays and protects the operators |

::: caution The moderator and the control rods do opposite jobs
Both are "extra" materials in the core, so students mix them up. The
**moderator slows neutrons down** so that more fissions happen; the **control
rods absorb neutrons** so that fewer happen. Removing the moderator stops a
thermal reactor just as surely as pushing the control rods all the way in.
:::

```figure caption="Schematic of a thermal nuclear reactor. Control rods are raised or lowered to hold the multiplication factor at $k = 1$; the coolant carries the heat of the fission fragments away to the heat exchanger."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(5.2,3.2))

# --- biological shield, core, rods ----------------------------------------
ax.add_patch(Rectangle((0.0,0.40), 3.20, 4.40, fc='#eef0f3', ec=MUTED, lw=2.6, zorder=1))
ax.add_patch(Rectangle((0.45,0.90), 2.30, 3.20, fc='#dfe8f3', ec=ACCENT, lw=1.2, zorder=2))
for x in (0.75, 1.35, 1.95, 2.55):
    ax.add_patch(Rectangle((x-0.07,1.10), 0.14, 2.80, fc='#b8860b', ec='none', zorder=3))
for x in (1.05, 1.65, 2.25):
    ax.add_patch(Rectangle((x-0.08,2.50), 0.16, 3.05, fc='#d9534f', ec='none', zorder=4))

lab = dict(fontsize=8.3, color=INK,
           arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.8))
ax.annotate('control rods\n(boron or cadmium)', xy=(2.25,5.45), xytext=(3.55,6.10),
            ha='left', va='center', **lab)
ax.annotate('fuel rods\n(enriched $^{235}$U)', xy=(0.75,3.20), xytext=(-0.45,3.70),
            ha='right', va='center', **lab)
ax.annotate('moderator\n(graphite or D$_2$O)', xy=(0.85,1.35), xytext=(-0.45,1.50),
            ha='right', va='center', **lab)
ax.annotate('concrete shield', xy=(1.10,0.40), xytext=(1.10,-0.05),
            ha='center', va='top', **lab)

# --- coolant loop ----------------------------------------------------------
hot, cold = '#d9534f', ACCENT
ax.plot([2.75,4.05,4.05],[4.30,4.30,3.32], color=hot, lw=2.2, zorder=2,
        solid_joinstyle='round')
ax.annotate('', xy=(4.05,3.12), xytext=(4.05,3.36),
            arrowprops=dict(arrowstyle='-|>', color=hot, lw=2.0, mutation_scale=11))
ax.plot([4.05,4.05,2.75],[1.35,0.72,0.72], color=cold, lw=2.2, zorder=2,
        solid_joinstyle='round')
ax.annotate('', xy=(2.58,0.72), xytext=(2.86,0.72),
            arrowprops=dict(arrowstyle='-|>', color=cold, lw=2.0, mutation_scale=11))
ax.annotate('hot coolant out', (4.25,4.35), ha='left', va='center',
            fontsize=8.2, color=hot)
ax.annotate('coolant back in', (4.25,0.62), ha='left', va='center',
            fontsize=8.2, color=cold)

# --- heat exchanger, turbine, generator ------------------------------------
ax.add_patch(Rectangle((3.55,1.35), 1.90, 1.75, fc='none', ec=INK, lw=1.2, zorder=3))
ax.annotate('heat\nexchanger', (4.50,2.22), ha='center', va='center',
            fontsize=8.3, color=INK, zorder=4)
ax.annotate('', xy=(6.52,2.22), xytext=(5.48,2.22),
            arrowprops=dict(arrowstyle='-|>', color=MUTED, lw=1.6, mutation_scale=12))
ax.annotate('steam', (6.00,3.28), ha='center', va='bottom', fontsize=8.2, color=MUTED)
ax.add_patch(Rectangle((6.55,1.35), 1.95, 1.75, fc='none', ec=INK, lw=1.2, zorder=3))
ax.annotate('turbine and\ngenerator', (7.52,2.22), ha='center', va='center',
            fontsize=8.3, color=INK, zorder=4)
ax.annotate('', xy=(9.30,2.22), xytext=(8.53,2.22),
            arrowprops=dict(arrowstyle='-|>', color='#2e8b57', lw=1.6, mutation_scale=12))
ax.annotate('electricity', (9.45,2.22), ha='left', va='center',
            fontsize=8.2, color='#2e8b57')

ax.set_xlim(-2.55, 10.95); ax.set_ylim(-0.70, 6.55)
ax.set_aspect('equal'); ax.axis('off')
```

In a bomb the chain is deliberately left uncontrolled: two subcritical pieces of
almost pure ²³⁵U or ²³⁹Pu are slammed together to exceed the critical mass, and
$k$ jumps far above $1$.

::: definition Nuclear fusion
Nuclear fusion is the joining of two very light nuclei into a single heavier
nucleus, with a release of energy. It requires extremely high temperature
($\approx 10^{8}\ \text{K}$) so that the nuclei approach fast enough to overcome
their electrostatic repulsion; hence it is called a **thermonuclear** reaction.
:::

The reaction used in fusion research is deuterium–tritium:

²H + ³H → ⁴He + ¹n + 17.6 MeV

In the Sun, four hydrogen nuclei are effectively converted into one helium
nucleus through the proton–proton cycle, releasing $26.7\ \text{MeV}$ and
consuming about $6\times10^{11}\ \text{kg}$ of hydrogen every second.

| | Fission | Fusion |
|---|---|---|
| Process | heavy nucleus splits | light nuclei join |
| Trigger | absorption of a slow neutron | very high temperature and pressure |
| Energy per event | $\approx 200\ \text{MeV}$ | $\approx 17.6\ \text{MeV}$ (D–T) |
| Energy per nucleon | $\approx 0.85\ \text{MeV}$ | $\approx 3.5\ \text{MeV}$ |
| Products | radioactive fragments | mostly non-radioactive |
| Controlled use | nuclear power reactors | not yet commercially achieved |

::: example Worked example 24.5
**Problem.** (a) Calculate the energy released in the fusion reaction
²H + ³H → ⁴He + ¹n, given the masses ²H $= 2.014102\ \text{u}$,
³H $= 3.016049\ \text{u}$, ⁴He $= 4.002603\ \text{u}$, ¹n $= 1.008665\ \text{u}$.
(b) If each fission of ²³⁵U releases $200\ \text{MeV}$, how much energy is
obtainable from $1.0\ \text{kg}$ of ²³⁵U? ($N_A = 6.022\times10^{23}\ \text{mol}^{-1}$.)

**Solution.**

(a) Total mass before $= 2.014102 + 3.016049 = 5.030151\ \text{u}$.
Total mass after $= 4.002603 + 1.008665 = 5.011268\ \text{u}$.

$$ \Delta m = 5.030151 - 5.011268 = 0.018883\ \text{u} $$

$$ Q = 0.018883\times931.5 = 17.6\ \text{MeV} $$

(b) Number of nuclei in $1.0\ \text{kg} = 1000\ \text{g}$:

$$ N = \frac{1000}{235}\times6.022\times10^{23} = 2.56\times10^{24} $$

$$ E = 2.56\times10^{24}\times200\ \text{MeV} = 5.13\times10^{26}\ \text{MeV} $$

$$ E = 5.13\times10^{26}\times1.6\times10^{-13} = 8.2\times10^{13}\ \text{J} $$

That single kilogram would run a $100\ \text{MW}$ power station for
$8.2\times10^{13}/10^{8} = 8.2\times10^{5}\ \text{s}$, about $9.5$ days.
:::

## Chapter summary

- Rutherford's alpha-scattering experiment showed the atom is mostly empty with a
  tiny, massive, positively charged nucleus of radius about $10^{-14}\ \text{m}$.
- $Z$ = number of protons, $A$ = number of nucleons, $N = A - Z$;
  $R = R_0A^{1/3}$ with $R_0 = 1.2\ \text{fm}$, so nuclear density is constant at
  about $2.3\times10^{17}\ \text{kg m}^{-3}$.
- $1\ \text{u} = 1.6605\times10^{-27}\ \text{kg} = 931.5\ \text{MeV}$. Isotopes
  have the same $Z$ and different $A$.
- Mass varies with speed, $m = m_0/\sqrt{1-v^{2}/c^{2}}$; from this and
  $dE_k = v\,d(mv)$ follows $E_k = (m-m_0)c^{2}$ and hence $E = mc^{2}$. A mass
  defect in u times $931.5$ gives the energy in MeV.
- Mass defect $\Delta m = [Zm_p + (A-Z)m_n] - M$; binding energy $B = \Delta mc^2$;
  packing fraction $f = (M-A)/A$.
- The $B/A$ curve peaks at about $8.8\ \text{MeV}$ near $A = 56$; light nuclei
  release energy by fusion, heavy nuclei by fission.
- Pair production needs $E \ge 1.02\ \text{MeV}$ and a nearby nucleus;
  annihilation of e⁻ and e⁺ gives two $0.511\ \text{MeV}$ photons.
- Fission of ²³⁵U releases about $200\ \text{MeV}$ (read off the $B/A$ curve as
  $236\times(8.5-7.6)$) and 2–3 neutrons, which sustain a chain reaction above
  the critical mass ($\approx 52\ \text{kg}$ for bare ²³⁵U). A reactor holds the
  multiplication factor at $k = 1$ using a moderator to slow neutrons and
  control rods to absorb them.
- D–T fusion releases $17.6\ \text{MeV}$ but needs about $10^{8}\ \text{K}$.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. Rutherford's alpha-scattering experiment established that <span class="marks">[1]</span>
   (a) the electron is negatively charged (b) the nucleus is small, massive and positive
   (c) the atom is a uniform sphere of charge (d) neutrons exist in the nucleus
2. The density of a nucleus <span class="marks">[1]</span>
   (a) increases with $A$ (b) decreases with $A$ (c) is independent of $A$ (d) is equal to that of water
3. The energy equivalent of $1\ \text{u}$ is about <span class="marks">[1]</span>
   (a) $0.511\ \text{MeV}$ (b) $1.02\ \text{MeV}$ (c) $931.5\ \text{MeV}$ (d) $200\ \text{MeV}$
4. The binding energy per nucleon is maximum for nuclei with mass number near <span class="marks">[1]</span>
   (a) $4$ (b) $56$ (c) $120$ (d) $235$
5. The minimum photon energy needed for pair production is <span class="marks">[1]</span>
   (a) $0.255\ \text{MeV}$ (b) $0.511\ \text{MeV}$ (c) $1.02\ \text{MeV}$ (d) $1.44\ \text{MeV}$
6. Two nuclides with the same mass number but different atomic numbers are called <span class="marks">[1]</span>
   (a) isotopes (b) isobars (c) isotones (d) isomers
7. The moderator in a nuclear reactor is used to <span class="marks">[1]</span>
   (a) absorb surplus neutrons (b) slow down fast neutrons (c) cool the core (d) shield the operators
8. A chain reaction is just self-sustaining when the multiplication factor is <span class="marks">[1]</span>
   (a) $k < 1$ (b) $k = 0$ (c) $k = 1$ (d) $k > 1$

::: note Answers to Group A
**1.** (b) — large-angle scattering can only come from a concentrated positive charge.
**2.** (c) — mass $\propto A$ and volume $\propto A$, so $A$ cancels.
**3.** (c) — $(1.6605\times10^{-27})c^{2} = 1.49\times10^{-10}\ \text{J} = 931.5\ \text{MeV}$.
**4.** (b) — the peak of the $B/A$ curve is ⁵⁶Fe at $8.79\ \text{MeV}$.
**5.** (c) — twice the electron rest energy, $2\times0.511\ \text{MeV}$.
**6.** (b) — same $A$ means isobars, e.g. ⁴⁰Ar and ⁴⁰Ca.
**7.** (b) — slow (thermal) neutrons are captured by ²³⁵U far more readily; the
control rods, not the moderator, do the absorbing.
**8.** (c) — $k = 1$ means each generation is the same size as the one before.
:::

**Group B — Short answer (5 marks each)**

1. Describe Rutherford's alpha-particle scattering experiment. State three
   observations and the conclusion drawn from each. <span class="marks">[5]</span>
2. Show that the density of a nucleus is independent of its mass number, and
   calculate its value. Take $R_0 = 1.2\ \text{fm}$ and
   $m_n = 1.67\times10^{-27}\ \text{kg}$. <span class="marks">[5]</span>
3. Define mass defect and binding energy. Calculate the binding energy per
   nucleon of ⁷Li, given atomic masses ⁷Li $= 7.016004\ \text{u}$,
   ¹H $= 1.007825\ \text{u}$, ¹n $= 1.008665\ \text{u}$. <span class="marks">[5]</span>
4. An alpha particle of energy $5.0\ \text{MeV}$ is fired head-on at a gold
   nucleus ($Z = 79$). Find its distance of closest approach.
   Take $1/4\pi\varepsilon_0 = 9\times10^{9}\ \text{N m}^{2}\ \text{C}^{-2}$. <span class="marks">[5]</span>
5. What is meant by creation and annihilation of matter? Why does pair production
   need a minimum energy of $1.02\ \text{MeV}$, and why must it occur near a
   nucleus? <span class="marks">[5]</span>
6. Sketch the graph of binding energy per nucleon against mass number and use it
   to explain why both fission and fusion release energy. <span class="marks">[5]</span>
7. Starting from the relativistic variation of mass with speed, derive Einstein's
   mass-energy relation $E = mc^{2}$. <span class="marks">[5]</span>
8. With the help of a labelled diagram, describe the main parts of a nuclear
   reactor and state the function of each. <span class="marks">[5]</span>

::: note Answers to Group B
**2.** $\rho = 3m_n/4\pi R_0^{3}$; numerically
$3(1.67\times10^{-27})/[4\pi(1.2\times10^{-15})^{3}] = 5.01\times10^{-27}/7.24\times10^{-45}
= 2.3\times10^{17}\ \text{kg m}^{-3}$.

**3.** $\Delta m = 3(1.007825) + 4(1.008665) - 7.016004
= 3.023475 + 4.034660 - 7.016004 = 0.042131\ \text{u}$.
$B = 0.042131\times931.5 = 39.2\ \text{MeV}$, so
$B/A = 39.2/7 = 5.6\ \text{MeV per nucleon}$.

**4.** $E = 5.0\ \text{MeV} = 5.0\times1.6\times10^{-13} = 8.0\times10^{-13}\ \text{J}$.

$$ r_0 = \frac{1}{4\pi\varepsilon_0}\cdot\frac{2Ze^{2}}{E}
= \frac{9\times10^{9}\times2\times79\times(1.6\times10^{-19})^{2}}{8.0\times10^{-13}} $$

The numerator is $9\times10^{9}\times158\times2.56\times10^{-38} = 3.64\times10^{-26}$,
so $r_0 = 4.6\times10^{-14}\ \text{m}$.

**1., 5., 6.** are bookwork: see §24.1, §24.6 and §24.5. For 6, marks are given
for the labelled axes, the peak at $A \approx 56$ with $B/A \approx 8.8\ \text{MeV}$,
and the statement that both processes move the products towards the peak, so
binding energy increases and energy is released.

**7.** See the derivation in §24.4. One mark each for: $dE_k = v\,d(mv)$;
expanding it to $mv\,dv + v^{2}dm$; differentiating $m^{2}c^{2} - m^{2}v^{2}
= m_0^{2}c^{2}$ to reach $c^{2}dm = mv\,dv + v^{2}dm$; integrating
$dE_k = c^{2}dm$ to get $E_k = (m - m_0)c^{2}$; and concluding $E = mc^{2}$.

**8.** See §24.7. Marks for the labelled diagram plus fuel rods, moderator,
control rods, coolant and shielding with one correct function each.
:::

**Group C — Long answer (8 marks each)**

1. (a) Define mass defect, binding energy and binding energy per nucleon. <span class="marks">[3]</span>
   (b) Draw the binding-energy-per-nucleon curve and describe its main features. <span class="marks">[2]</span>
   (c) Calculate the energy released in the reaction ²H + ³H → ⁴He + ¹n, given
   ²H $= 2.014102\ \text{u}$, ³H $= 3.016049\ \text{u}$, ⁴He $= 4.002603\ \text{u}$
   and ¹n $= 1.008665\ \text{u}$. <span class="marks">[3]</span>
2. (a) What is nuclear fission? Explain chain reaction and critical mass, and
   state the function of a moderator and of control rods in a reactor. <span class="marks">[4]</span>
   (b) Each fission of ²³⁵U releases $200\ \text{MeV}$. Calculate the energy
   released by the complete fission of $0.50\ \text{kg}$ of ²³⁵U, and the mass
   that disappears in the process. <span class="marks">[4]</span>

::: note Answers to Group C
**1.(c)** $\Delta m = (2.014102+3.016049) - (4.002603+1.008665)
= 5.030151 - 5.011268 = 0.018883\ \text{u}$, so
$Q = 0.018883\times931.5 = 17.6\ \text{MeV}$.

**2.(b)** $N = (500/235)\times6.022\times10^{23} = 1.28\times10^{24}$ nuclei.
$E = 1.28\times10^{24}\times200\times1.6\times10^{-13} = 4.1\times10^{13}\ \text{J}$.
The mass lost follows from $E = \Delta mc^{2}$:
$\Delta m = 4.1\times10^{13}/(9\times10^{16}) = 4.6\times10^{-4}\ \text{kg}$,
i.e. about $0.46\ \text{g}$ — less than one part in a thousand of the fuel.

**1.(a), 1.(b), 2.(a)** are bookwork: see §24.5 and §24.7.
:::
