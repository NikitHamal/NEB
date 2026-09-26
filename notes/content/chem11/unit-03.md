---
subject: Chemistry
grade: 11
unit: 3
title: Atomic Structure
hours: 8
area: General and Physical Chemistry
---

This unit follows one long argument. Rutherford showed the atom has a tiny
positive nucleus but could not say where the electrons are. Bohr placed them in
fixed orbits and successfully predicted the hydrogen spectrum — then failed for
every other atom. De Broglie and Heisenberg showed why: an electron is not a
particle on a track, and the best we can state is a **probability**. What
survives is the quantum mechanical model, four quantum numbers and the three
filling rules you will use in every later unit.

::: key What you must be able to do
Write the electronic configuration of any atom or ion up to $Z = 30$ without
hesitating; quote Bohr's postulates and the three filling rules; and handle the
four standard numericals — Bohr radius and energy, the Rydberg equation,
$\lambda = h/mv$, and $\Delta x\,\Delta p \geq h/4\pi$.
:::

## 3.1 Rutherford's atomic model and its limitations

In 1909 Geiger and Marsden, working under Rutherford, fired a narrow beam of
α-particles (He²⁺, mass 4 u, charge +2) at a gold foil about 0.00004 cm thick and
recorded the flashes on a movable zinc sulphide screen. Rutherford explained
their results in 1911.

| Observation | Conclusion |
|---|---|
| Most α-particles passed straight through | The atom is mostly empty space |
| A small fraction were deflected by small angles | There is a concentrated positive charge that repels them |
| Roughly 1 in 8,000 was turned through more than 90° | All the positive charge and almost all the mass is packed into a very small **nucleus** |

```figure caption="Rutherford scattering: computed hyperbolic paths of α-particles past a nucleus. Only the paths above the beam axis are drawn — the pattern is symmetrical below it. The angle at the left of each path is its deflection. The closer a particle aims at the nucleus, the larger the deflection; a head-on particle is thrown straight back through $180^\circ$."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle
fig, ax = plt.subplots(figsize=(5.0,2.6))
d = 0.26                              # head-on distance of closest approach
def path(b):
    Th = 2*np.arctan(d/(2*b)); e = 1/np.sin(Th/2); a = d/2
    tm = np.arccos(1/e)*0.99999
    t  = np.linspace(tm, -tm, 1200)
    r  = a*(e**2-1)/(e*np.cos(t)-1)
    al = np.pi/2 + Th/2
    x, y = r*np.cos(al+t), r*np.sin(al+t)
    m = (x > -4.4) & (x < 4.5) & (y < 2.6)
    return x[m], y[m], np.degrees(Th)
ax.plot([-4.4, 4.5], [0,0], color=GRID, lw=0.9, ls=(0,(4,3)))
for b, c in [(1.70, MUTED), (1.10, MUTED), (0.62, SERIES[0]), (0.28, SERIES[0])]:
    x, y, Th = path(b)
    ax.plot(x, y, color=c, lw=1.4)
    ax.annotate('', xy=(x[-1], y[-1]), xytext=(x[-8], y[-8]),
                arrowprops=dict(arrowstyle='-|>', color=c, lw=1.4, mutation_scale=9))
    ax.text(-4.55, b, f'{Th:.0f}°', fontsize=7.8, color=c, ha='right', va='center')
ax.plot([-4.4,-0.26], [0.055,0.055], color=SERIES[1], lw=1.4)
ax.plot([-0.26,-4.4], [-0.055,-0.055], color=SERIES[1], lw=1.4)
ax.annotate('', xy=(-4.35,-0.055), xytext=(-3.85,-0.055),
            arrowprops=dict(arrowstyle='-|>', color=SERIES[1], lw=1.4, mutation_scale=9))
ax.text(-4.55, -0.055, '180°', fontsize=7.8, color=SERIES[1], ha='right', va='center')
ax.add_patch(Circle((0,0), 0.10, color=SERIES[1], zorder=6))
ax.annotate('nucleus: +Ze, tiny and dense', xy=(0.10,-0.06), xytext=(0.85,-1.20),
            fontsize=8.4, color=INK,
            arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.0, mutation_scale=9))
ax.text(-4.4, 2.85, 'incoming beam of α-particles   →', fontsize=8.8, color=INK)
ax.set_xlim(-5.0, 4.7); ax.set_ylim(-1.7, 3.05)
ax.set_aspect('equal'); ax.axis('off')
```

**The model.** The atom has a small, dense, positively charged nucleus containing
practically the whole mass; electrons revolve around it at relatively large
distances, and the centripetal force is supplied by electrostatic attraction. The
nuclear radius is of the order of 10⁻¹⁵ m against an atomic radius of 10⁻¹⁰ m —
the nucleus is about 10⁵ times smaller than the atom.

**Limitations.**

1. **It predicts an unstable atom.** By Maxwell's electromagnetic theory a charged
   body moving in a circle is accelerating, so it must radiate energy
   continuously. The electron would spiral into the nucleus in about 10⁻⁸ s. Matter
   would not exist.
2. **It predicts the wrong spectrum.** A continuously spiralling electron would
   emit a *continuous* spectrum, whereas atoms give sharp **line** spectra.
3. **It says nothing about the arrangement of electrons** — no shells, no energies,
   so it cannot explain chemical behaviour or valency.

## 3.2 Postulates of Bohr's atomic model and its application

Niels Bohr (1913) kept the nuclear atom and added quantisation.

1. Electrons revolve round the nucleus only in certain permitted circular paths
   called **stationary states** or energy levels, in which they do **not** radiate
   energy.
2. Only those orbits are allowed for which the angular momentum is an integral
   multiple of $h/2\pi$:
   $$ mvr = \frac{nh}{2\pi}, \qquad n = 1, 2, 3, \ldots $$
3. Energy is emitted or absorbed **only** when an electron jumps from one
   stationary state to another, in a packet of size
   $$ \Delta E = E_2 - E_1 = h\nu $$
4. The electrostatic attraction between nucleus and electron provides the
   centripetal force needed for the circular motion.

::: derivation Radius and energy of the nth Bohr orbit
For a one-electron species of nuclear charge $+Ze$, balancing the Coulomb force
against the centripetal force,

$$ \frac{kZe^{2}}{r^{2}} = \frac{mv^{2}}{r} \qquad \text{so} \qquad mv^{2} = \frac{kZe^{2}}{r} $$

with $k = 1/4\pi\varepsilon_0$. From the quantisation condition $v = nh/2\pi mr$;
substituting and solving for $r$,

$$ r_n = \frac{n^{2}h^{2}}{4\pi^{2}mkZe^{2}} = 0.529\,\frac{n^{2}}{Z}\ \text{Å} $$

The total energy is kinetic plus potential,
$E = \frac{1}{2}mv^{2} - kZe^{2}/r = -\frac{1}{2}kZe^{2}/r$. Putting in $r_n$,

$$ E_n = -\frac{2\pi^{2}mk^{2}Z^{2}e^{4}}{n^{2}h^{2}} = -13.6\,\frac{Z^{2}}{n^{2}}\ \text{eV} = -2.18\times10^{-18}\,\frac{Z^{2}}{n^{2}}\ \text{J} $$
:::

The energy is negative because the electron is **bound**; zero energy corresponds
to a free electron at infinity. The orbital speed works out as
$v_n = 2.188\times10^{6}\,(Z/n)\ \text{m s}^{-1}$.

::: example Worked example 3.1
**Problem.** Calculate the radius and the energy of the third Bohr orbit of the
hydrogen atom. How much energy is needed to remove the electron completely from
the ground state?

**Solution.** For hydrogen $Z = 1$.

$$ r_3 = 0.529\times\frac{3^{2}}{1} = 0.529\times9 = 4.761\ \text{Å} = 4.761\times10^{-10}\ \text{m} $$

$$ E_3 = -\frac{13.6}{3^{2}} = -1.51\ \text{eV} $$

Ionisation from the ground state means $n = 1 \rightarrow n = \infty$:

$$ \Delta E = E_\infty - E_1 = 0 - (-13.6) = 13.6\ \text{eV} = 2.18\times10^{-18}\ \text{J} $$

Per mole this is $2.18\times10^{-18}\times6.022\times10^{23} = 1.31\times10^{6}\ \text{J} = 1312\ \text{kJ mol}^{-1}$.
:::

## 3.3 Spectrum of hydrogen atom

When hydrogen gas at low pressure is excited in a discharge tube and the light is
passed through a prism, the result is not a continuous rainbow but a set of sharp
coloured **lines** on a dark background — an emission line spectrum. The
wavenumber of every line fits one empirical equation:

$$ \bar{\nu} = \frac{1}{\lambda} = R_H\left(\frac{1}{n_1^{2}} - \frac{1}{n_2^{2}}\right), \qquad n_2 > n_1 $$

where $R_H = 1.097\times10^{7}\ \text{m}^{-1}$ is the Rydberg constant. Bohr's
model **derives** this equation: putting $\Delta E = h c/\lambda$ with
$E_n = -13.6/n^2$ eV reproduces $R_H$ to three figures. That was its triumph.

| Series | $n_1$ | $n_2$ | Region |
|---|---|---|---|
| Lyman | 1 | 2, 3, 4 … | Ultraviolet |
| Balmer | 2 | 3, 4, 5 … | Visible |
| Paschen | 3 | 4, 5, 6 … | Infrared |
| Brackett | 4 | 5, 6, 7 … | Infrared |
| Pfund | 5 | 6, 7, 8 … | Far infrared |

```figure caption="Energy levels of the hydrogen atom and the origin of the spectral series. Because $E_n \propto -1/n^2$, the levels for $n = 4, 5, 6 \ldots$ crowd together and converge on $n = \infty$, which is why every series ends in a series limit."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,3.3))
for n in range(1,8):
    ax.hlines(-13.6/n**2, 0.06, 0.92, color=INK, lw=1.15)
ax.hlines(0, 0.06, 0.92, color=MUTED, lw=1.0, ls='--')
for n in (1,2,3):
    e = -13.6/n**2
    ax.text(0.94, e, f'n = {n}', va='center', fontsize=8.6, color=INK)
    ax.text(0.04, e, f'{e:.2f} eV', va='center', ha='right', fontsize=8.0, color=MUTED)
ax.text(0.94, 0, 'n = ∞', va='center', fontsize=8.6, color=MUTED)
ax.text(0.04, 0, '0.00 eV', va='center', ha='right', fontsize=8.0, color=MUTED)
series = [(1,[2,3,4],SERIES[4],'Lyman\n(ultraviolet)',0.13),
          (2,[3,4,5],SERIES[1],'Balmer\n(visible)',0.46),
          (3,[4,5,6],SERIES[2],'Paschen\n(infrared)',0.74)]
for nf,nis,c,lab,x0 in series:
    for j,ni in enumerate(nis):
        x = x0 + j*0.05
        ax.annotate('', xy=(x,-13.6/nf**2), xytext=(x,-13.6/ni**2),
                    arrowprops=dict(arrowstyle='-|>', color=c, lw=1.25, mutation_scale=8))
    ax.text(x0+0.05, -16.2, lab, fontsize=8.1, color=c, ha='center', va='top')
ax.text(0.51, -4.3, '656, 486, 434 nm', fontsize=7.8, color=SERIES[1], ha='center')
ax.set_ylabel('energy  $E_n = -13.6/n^2$  (eV)')
ax.set_xlim(-0.34,1.12); ax.set_ylim(-19.2, 1.4)
ax.set_xticks([]); ax.set_yticks([])
ax.spines[['top','right','bottom','left']].set_visible(False)
```

::: example Worked example 3.2
**Problem.** Calculate the wavelength of the radiation emitted when the electron
in a hydrogen atom falls from $n = 4$ to $n = 2$. To which series does it belong
and what colour is it? ($R_H = 1.097\times10^{7}\ \text{m}^{-1}$)

**Solution.**

$$ \frac{1}{\lambda} = R_H\left(\frac{1}{2^{2}} - \frac{1}{4^{2}}\right) = 1.097\times10^{7}\left(0.25 - 0.0625\right) $$

$$ \frac{1}{\lambda} = 1.097\times10^{7}\times0.1875 = 2.057\times10^{6}\ \text{m}^{-1} $$

$$ \lambda = 4.86\times10^{-7}\ \text{m} = 486\ \text{nm} $$

Since $n_1 = 2$ it is the second line of the **Balmer** series (Hβ), in the
blue-green part of the visible spectrum.
:::

## 3.4 Defects of Bohr's theory

| Defect | What Bohr could not explain |
|---|---|
| Multi-electron atoms | The theory works only for one-electron species (H, He⁺, Li²⁺); it fails even for helium |
| Fine structure | Under a high-resolution spectroscope each line is really several closely spaced lines |
| Zeeman effect | Splitting of spectral lines in a magnetic field |
| Stark effect | Splitting of spectral lines in an electric field |
| Wave nature | It treats the electron purely as a particle, ignoring de Broglie's wave character |
| Uncertainty principle | Fixing both the radius of an orbit and the momentum in it is forbidden by Heisenberg |
| Shape of orbits | It assumes circular orbits only; Sommerfeld had to add elliptical ones |
| Bonding | It cannot explain the shapes of molecules or how chemical bonds form |

::: caution Two defects worth memorising together
The two *fundamental* objections are the wave nature of the electron and the
uncertainty principle: they do not merely say Bohr got details wrong, they say the
idea of a definite orbit is meaningless. Quote these two first; the rest are
experimental failures.
:::

## 3.5 Elementary idea of the quantum mechanical model: de Broglie's wave equation

Light behaves as a wave (diffraction) and as a particle (photoelectric effect).
In 1924 Louis de Broglie proposed that **all** matter has this dual character.

::: derivation The de Broglie relation
For a photon, Planck's relation gives $E = h\nu = hc/\lambda$ and Einstein's
mass–energy relation gives $E = mc^{2}$. Equating them,

$$ mc^{2} = \frac{hc}{\lambda} \qquad \Longrightarrow \qquad \lambda = \frac{h}{mc} $$

Replacing the speed of light by the speed $v$ of any material particle,

$$ \lambda = \frac{h}{mv} = \frac{h}{p} $$
:::

The wavelength is inversely proportional to mass, which is why the effect is
invisible for everyday objects: a 100 g ball thrown at 10 m s⁻¹ has
$\lambda \approx 6.6\times10^{-34}$ m, far too small to detect. For an electron it
is about 10⁻¹⁰ m — the size of an atom — and Davisson and Germer confirmed it in
1927 by diffracting electrons from a nickel crystal.

::: example Worked example 3.3
**Problem.** The electron in the first Bohr orbit of hydrogen moves with speed
$2.19\times10^{6}\ \text{m s}^{-1}$. Calculate its de Broglie wavelength and
compare it with the circumference of that orbit ($r_1 = 0.529$ Å).
($h = 6.626\times10^{-34}$ J s, $m_e = 9.11\times10^{-31}$ kg)

**Solution.**

$$ \lambda = \frac{h}{mv} = \frac{6.626\times10^{-34}}{9.11\times10^{-31}\times2.19\times10^{6}} = \frac{6.626\times10^{-34}}{1.995\times10^{-24}} $$

$$ \lambda = 3.32\times10^{-10}\ \text{m} = 3.32\ \text{Å} $$

The circumference of the first orbit is

$$ 2\pi r_1 = 2\pi\times0.529\times10^{-10} = 3.32\times10^{-10}\ \text{m} $$

They are equal. The first Bohr orbit holds exactly **one** de Broglie wavelength,
so the electron wave joins up on itself and forms a standing wave. Generalising,
$2\pi r = n\lambda = nh/mv$, which rearranges to Bohr's second postulate
$mvr = nh/2\pi$.
:::

## 3.6 Heisenberg's Uncertainty Principle

::: definition Uncertainty principle
It is impossible to determine simultaneously and with complete accuracy both the
position and the momentum of a microscopic particle. If $\Delta x$ is the
uncertainty in position and $\Delta p$ that in momentum,

$$ \Delta x \cdot \Delta p \geq \frac{h}{4\pi}, \qquad \text{i.e.} \qquad \Delta x \cdot m\Delta v \geq \frac{h}{4\pi} $$
:::

The same limit applies to energy and time, $\Delta E\cdot\Delta t \geq h/4\pi$.
The principle is not a limitation of our instruments: any measurement of an
electron requires a photon, and the photon inevitably disturbs it.

::: example Worked example 3.4
**Problem.** The position of an electron is measured to an accuracy of
$10^{-11}$ m. Calculate the minimum uncertainty in its velocity and comment.

**Solution.**

$$ \Delta v = \frac{h}{4\pi m\,\Delta x} = \frac{6.626\times10^{-34}}{4\times3.1416\times9.11\times10^{-31}\times10^{-11}} $$

$$ \Delta v = \frac{6.626\times10^{-34}}{1.145\times10^{-40}} = 5.79\times10^{6}\ \text{m s}^{-1} $$

This uncertainty is larger than the electron's own speed in the first Bohr orbit
($2.19\times10^{6}$ m s⁻¹). Once we pin the electron down to a tenth of an
ångström we have no idea how fast it is going, so a definite "orbit" cannot exist.
:::

## 3.7 Concept of probability

Because a path cannot be defined, Erwin Schrödinger (1926) replaced it with a
**wave function** $\psi$, obtained by solving his wave equation for the electron.
The wave function itself has no physical meaning, but Max Born showed that
$\psi^{2}$ at any point gives the **probability density** — the chance of finding
the electron in unit volume at that point.

::: definition Orbital
An orbital is the three-dimensional region around the nucleus where the
probability of finding an electron is maximum (conventionally the region that
encloses about 90 % of the total probability).
:::

An orbital is therefore a *charge cloud*, not a track. Solving the Schrödinger
equation automatically produces three quantum numbers $n$, $l$ and $m$; the fourth,
$s$, comes from experiment.

## 3.8 Quantum numbers

| Quantum number | Symbol | Allowed values | Tells us |
|---|---|---|---|
| Principal | $n$ | 1, 2, 3, … | Shell (K, L, M, N); size and main energy of the orbital |
| Azimuthal / angular momentum | $l$ | 0 to $(n-1)$ | Subshell (s, p, d, f) and the **shape** of the orbital |
| Magnetic | $m$ | $-l$ to $+l$, including 0 | Orientation of the orbital in space |
| Spin | $s$ | $+\tfrac{1}{2}$ or $-\tfrac{1}{2}$ | Direction of spin of the electron |

| $l$ | Subshell | Values of $m$ | Orbitals | Maximum electrons |
|---|---|---|---|---|
| 0 | s | 0 | 1 | 2 |
| 1 | p | −1, 0, +1 | 3 | 6 |
| 2 | d | −2 … +2 | 5 | 10 |
| 3 | f | −3 … +3 | 7 | 14 |

For a shell of principal quantum number $n$ there are $n^{2}$ orbitals and at most
$2n^{2}$ electrons. Angular momentum of the electron in an orbital is
$\sqrt{l(l+1)}\,(h/2\pi)$.

::: memory Reading a subshell label
In "4d⁷": the 4 is $n$, the letter d means $l = 2$, and the superscript 7 is the
number of electrons. So those electrons are in the fourth shell, in a
five-orbital d subshell that can hold ten.
:::

## 3.9 Orbitals and shape of s and p orbitals

```figure caption="Boundary-surface pictures of the s and p orbitals. The two colours are the two signs (phases) of the wave function $\psi$, which matters when orbitals overlap to form bonds in Unit 5."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse
fig, axs = plt.subplots(1, 4, figsize=(5.2,2.3))
titles = ['1s', '2p$_x$', '2p$_y$', '2p$_z$']
for ax, t in zip(axs, titles):
    ax.set_xlim(-1.45,1.45); ax.set_ylim(-1.35,1.45)
    ax.set_aspect('equal'); ax.axis('off')
    ax.plot([-1.1,1.1],[0,0], color=GRID, lw=0.8)
    ax.plot([0,0],[-1.1,1.1], color=GRID, lw=0.8)
    ax.plot([-0.72,0.72],[-0.52,0.52], color=GRID, lw=0.8)
    ax.set_title(t, fontsize=9.6, color=INK, pad=3)
    ax.text(1.15,-0.18,'x',fontsize=7.6,color=MUTED)
    ax.text(0.74,0.52,'y',fontsize=7.6,color=MUTED)
    ax.text(0.07,1.12,'z',fontsize=7.6,color=MUTED)
axs[0].add_patch(Circle((0,0), 0.70, fc=ACCENT, alpha=0.28, ec=ACCENT, lw=1.1))
def dumb(ax, dx, dy, w, h, ang):
    ax.add_patch(Ellipse(( dx, dy), w, h, angle=ang, fc=SERIES[0], alpha=0.33, ec=SERIES[0], lw=1.1))
    ax.add_patch(Ellipse((-dx,-dy), w, h, angle=ang, fc=SERIES[1], alpha=0.33, ec=SERIES[1], lw=1.1))
dumb(axs[1], 0.50, 0.00, 0.95, 0.58, 0)
dumb(axs[2], 0.40, 0.29, 0.95, 0.58, 36)
dumb(axs[3], 0.00, 0.50, 0.58, 0.95, 0)
for ax in axs:
    ax.plot([0],[0],'o',color=INK,ms=3.2)
```

| | s orbital | p orbital |
|---|---|---|
| Value of $l$ | 0 | 1 |
| Shape | Spherical | Dumb-bell |
| Number per shell | 1 | 3 (p_x, p_y, p_z) |
| Orientation | Non-directional | Directional, along the three axes, mutually perpendicular |
| Nodal planes through the nucleus | 0 | 1 |
| Present from shell | $n = 1$ | $n = 2$ |

The three p orbitals of a given shell are **degenerate** — equal in energy — in an
isolated atom. A 1s orbital is smaller than a 2s orbital, and a 2s orbital has one
spherical node inside it, but both are spheres.

## 3.10 Aufbau Principle, Pauli's exclusion principle and Hund's rule

::: definition The three filling rules
**Aufbau principle.** In the ground state, electrons occupy the available orbitals
in order of increasing energy: the lowest-energy orbital is filled first.

**Pauli's exclusion principle.** No two electrons in an atom can have the same
values of all four quantum numbers. Hence an orbital holds at most two electrons,
and they must have opposite spins.

**Hund's rule of maximum multiplicity.** Pairing of electrons in the orbitals of a
given subshell does not begin until each orbital of that subshell has one
electron, and these unpaired electrons have parallel spins.
:::

The order of energies follows the **(n + l) rule**: the subshell with the lower
value of $(n+l)$ fills first, and if two subshells have the same $(n+l)$, the one
with the lower $n$ fills first. For 4s, $n+l = 4+0 = 4$; for 3d, $n+l = 3+2 = 5$;
so 4s fills before 3d.

```figure caption="The diagonal rule. Each arrow follows a diagonal of constant $(n+l)$; reading the arrows from the top gives the filling order 1s 2s 2p 3s 3p 4s 3d 4p 5s 4d 5p 6s 4f 5d 6p 7s."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.6,3.3))
sub = {0:'s',1:'p',2:'d',3:'f'}
skip = {(5,3),(6,2),(6,3),(7,1),(7,2),(7,3)}
cells = {}
for n in range(1,8):
    for l in range(0, min(n,4)):
        if (n,l) in skip: continue
        cells[(n,l)] = f'{n}{sub[l]}'
for (n,l),lab in cells.items():
    ax.text(l*1.05, -n, lab, fontsize=10, color=INK, ha='center', va='center',
            zorder=5, bbox=dict(fc='white', ec='none', pad=1.4))
for k in sorted({n+l for (n,l) in cells}):
    grp = sorted([(n,l) for (n,l) in cells if n+l == k])
    (n1,l1) = grp[0]; (n2,l2) = grp[-1]
    ax.annotate('', xy=(l2*1.05-0.34, -n2-0.34), xytext=(l1*1.05+0.34, -n1+0.34),
                arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.15, mutation_scale=9),
                zorder=2)
ax.set_xlim(-0.85, 3.85); ax.set_ylim(-7.8, -0.25)
ax.axis('off')
```

::: caution 4s fills first but empties first
4s is filled before 3d, yet when a transition metal forms a cation the **4s**
electrons are removed first, because once 3d is occupied the 3d level drops below
4s. So Fe is [Ar]3d⁶4s² but Fe²⁺ is [Ar]3d⁶ — not [Ar]3d⁴4s².
:::

## 3.11 Electronic configurations of atoms and ions (up to atomic number 30)

| $Z$ | Element | Configuration | $Z$ | Element | Configuration |
|---|---|---|---|---|---|
| 1 | H | 1s¹ | 16 | S | [Ne]3s²3p⁴ |
| 2 | He | 1s² | 17 | Cl | [Ne]3s²3p⁵ |
| 3 | Li | [He]2s¹ | 18 | Ar | [Ne]3s²3p⁶ |
| 4 | Be | [He]2s² | 19 | K | [Ar]4s¹ |
| 5 | B | [He]2s²2p¹ | 20 | Ca | [Ar]4s² |
| 6 | C | [He]2s²2p² | 21 | Sc | [Ar]3d¹4s² |
| 7 | N | [He]2s²2p³ | 22 | Ti | [Ar]3d²4s² |
| 8 | O | [He]2s²2p⁴ | 23 | V | [Ar]3d³4s² |
| 9 | F | [He]2s²2p⁵ | 24 | Cr | [Ar]3d⁵4s¹ |
| 10 | Ne | [He]2s²2p⁶ | 25 | Mn | [Ar]3d⁵4s² |
| 11 | Na | [Ne]3s¹ | 26 | Fe | [Ar]3d⁶4s² |
| 12 | Mg | [Ne]3s² | 27 | Co | [Ar]3d⁷4s² |
| 13 | Al | [Ne]3s²3p¹ | 28 | Ni | [Ar]3d⁸4s² |
| 14 | Si | [Ne]3s²3p² | 29 | Cu | [Ar]3d¹⁰4s¹ |
| 15 | P | [Ne]3s²3p³ | 30 | Zn | [Ar]3d¹⁰4s² |

**The two anomalies.** Chromium is [Ar]3d⁵4s¹ and copper is [Ar]3d¹⁰4s¹, not
3d⁴4s² and 3d⁹4s². A **half-filled** (d⁵) or **completely filled** (d¹⁰) subshell
is extra stable, because such an arrangement is symmetrical and gives the maximum
exchange energy between electrons of parallel spin.

**Ions.** For an anion, add electrons in the usual Aufbau order; for a cation,
remove electrons from the shell of **highest $n$** first.

| Ion | Derived from | Configuration |
|---|---|---|
| Na⁺ | Na [Ne]3s¹ | 1s²2s²2p⁶ = [Ne] |
| Cl⁻ | Cl [Ne]3s²3p⁵ | [Ne]3s²3p⁶ = [Ar] |
| O²⁻ | O [He]2s²2p⁴ | 1s²2s²2p⁶ = [Ne] |
| Fe²⁺ | Fe [Ar]3d⁶4s² | [Ar]3d⁶ |
| Fe³⁺ | Fe [Ar]3d⁶4s² | [Ar]3d⁵ (half-filled, hence the stability of Fe³⁺) |
| Cu²⁺ | Cu [Ar]3d¹⁰4s¹ | [Ar]3d⁹ |
| Zn²⁺ | Zn [Ar]3d¹⁰4s² | [Ar]3d¹⁰ |

::: example Worked example 3.5
**Problem.** (a) Write the electronic configuration of the element with $Z = 24$
and explain why it is not [Ar]3d⁴4s². (b) How many unpaired electrons does Fe³⁺
contain? (c) Give the four quantum numbers of the last electron of chlorine
($Z = 17$).

**Solution.**

(a) Chromium: **[Ar]3d⁵4s¹**. Moving one 4s electron into 3d makes both subshells
exactly half-filled (3d⁵ and 4s¹), a symmetrical arrangement of lower energy than
3d⁴4s².

(b) Fe ($Z = 26$) is [Ar]3d⁶4s². Removing the two 4s electrons and one 3d electron
gives Fe³⁺ = [Ar]3d⁵. By Hund's rule the five 3d electrons occupy the five
orbitals singly, so Fe³⁺ has **5 unpaired electrons**.

(c) Cl is 1s²2s²2p⁶3s²3p⁵. The last electron enters the 3p subshell, so
$n = 3$, $l = 1$. With five electrons the three p orbitals hold 2, 2 and 1, so the
last one pairs up in the first orbital: $m = -1$ and $s = -\tfrac{1}{2}$.
:::

## Chapter summary

- Rutherford's α-scattering proved the nuclear atom but predicted an unstable atom
  and a continuous spectrum, and said nothing about electron arrangement.
- Bohr quantised angular momentum, $mvr = nh/2\pi$, giving
  $r_n = 0.529\,n^2/Z$ Å and $E_n = -13.6\,Z^2/n^2$ eV, and radiation only on
  transitions, $\Delta E = h\nu$.
- Hydrogen line spectrum: $1/\lambda = R_H(1/n_1^{2} - 1/n_2^{2})$ with
  $R_H = 1.097\times10^{7}\ \text{m}^{-1}$; Lyman (UV, $n_1=1$), Balmer (visible,
  $n_1=2$), Paschen, Brackett, Pfund (IR).
- Bohr fails for many-electron atoms, fine structure, Zeeman and Stark effects,
  and contradicts both wave–particle duality and the uncertainty principle.
- De Broglie: $\lambda = h/mv$. A Bohr orbit is a standing wave, $2\pi r = n\lambda$.
- Heisenberg: $\Delta x\cdot\Delta p \geq h/4\pi$, so orbits give way to
  probability; $\psi^{2}$ is the probability density and an orbital is the 90 %
  probability region.
- Quantum numbers: $n$ (shell, size), $l = 0$ to $n-1$ (shape), $m = -l$ to $+l$
  (orientation), $s = \pm\tfrac{1}{2}$ (spin); a shell holds $n^{2}$ orbitals and
  $2n^{2}$ electrons.
- s orbitals are spherical, p orbitals are dumb-bell shaped with one nodal plane
  and three orientations.
- Fill by the Aufbau $(n+l)$ rule, two per orbital with opposite spins (Pauli),
  singly first with parallel spins (Hund). Cr and Cu are anomalous; cations lose
  their 4s electrons before their 3d electrons.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The Balmer series of the hydrogen spectrum lies in the <span class="marks">[1]</span>
   (a) ultraviolet region (b) visible region (c) infrared region (d) X-ray region
2. The maximum number of electrons in a shell with principal quantum number $n$ is <span class="marks">[1]</span>
   (a) $n^{2}$ (b) $2n^{2}$ (c) $2n$ (d) $n+1$
3. The electronic configuration of Cr ($Z = 24$) is <span class="marks">[1]</span>
   (a) [Ar]3d⁴4s² (b) [Ar]3d⁵4s¹ (c) [Ar]3d⁶ (d) [Ar]3d³4s²
4. The number of unpaired electrons in Fe³⁺ is <span class="marks">[1]</span>
   (a) 3 (b) 4 (c) 5 (d) 6
5. Which pair of quantum numbers is **not** allowed? <span class="marks">[1]</span>
   (a) $n = 3,\ l = 2$ (b) $n = 2,\ l = 1$ (c) $n = 2,\ l = 2$ (d) $n = 4,\ l = 0$

::: note Answers to Group A
**1.** (b) — Balmer transitions end at $n = 2$ and fall at 656–410 nm.
**2.** (b) — $n^{2}$ orbitals, each holding 2 electrons.
**3.** (b) — a half-filled 3d⁵ with 4s¹ is more stable than 3d⁴4s².
**4.** (c) — Fe³⁺ is [Ar]3d⁵, and by Hund's rule all five are unpaired.
**5.** (c) — $l$ can only run from 0 to $n-1$, so $l = 2$ is impossible for $n = 2$.
:::

**Group B — Short answer (5 marks each)**

1. Describe Rutherford's α-scattering experiment and state the conclusions drawn
   from it. Give two limitations of his model. <span class="marks">[5]</span>
2. State the postulates of Bohr's atomic theory and mention any three defects of
   the theory. <span class="marks">[5]</span>
3. Calculate the radius and energy of the second Bohr orbit of the hydrogen atom,
   and the wavelength of the first line of the Lyman series.
   ($R_H = 1.097\times10^{7}\ \text{m}^{-1}$) <span class="marks">[5]</span>
4. State Heisenberg's uncertainty principle. Calculate the uncertainty in the
   position of an electron whose velocity is known to within
   $1.0\times10^{5}\ \text{m s}^{-1}$. <span class="marks">[5]</span>
5. Define the four quantum numbers and write the electronic configurations of
   Sc ($Z = 21$), Cu ($Z = 29$) and Zn²⁺. <span class="marks">[5]</span>

::: note Answers to Group B
**3.** $r_2 = 0.529\times2^{2} = 2.116\ \text{Å} = 2.116\times10^{-10}$ m and
$E_2 = -13.6/4 = -3.40$ eV.
First Lyman line is $n = 2 \rightarrow n = 1$:
$1/\lambda = 1.097\times10^{7}(1 - 1/4) = 8.23\times10^{6}\ \text{m}^{-1}$,
so $\lambda = 1.215\times10^{-7}\ \text{m} = 121.5$ nm (ultraviolet).

**4.** $\Delta x = h/(4\pi m \Delta v)
= 6.626\times10^{-34}/(4\times3.1416\times9.11\times10^{-31}\times1.0\times10^{5})
= 6.626\times10^{-34}/(1.145\times10^{-24}) = 5.79\times10^{-10}$ m,
i.e. about 5.8 Å — several atomic diameters.

**5.** Sc: [Ar]3d¹4s². Cu: [Ar]3d¹⁰4s¹ (filled 3d is extra stable).
Zn²⁺: Zn is [Ar]3d¹⁰4s², so removing the two 4s electrons gives [Ar]3d¹⁰.
:::

**Group C — Long answer (8 marks each)**

1. (a) State Bohr's postulates and derive expressions for the radius and the energy
   of the $n^{\text{th}}$ orbit of a hydrogen-like atom. <span class="marks">[5]</span>
   (b) Using these, show how the Rydberg equation for the hydrogen spectrum
   follows, and name the series obtained for $n_1 = 1, 2$ and $3$. <span class="marks">[3]</span>
2. (a) State the Aufbau principle, Pauli's exclusion principle and Hund's rule. <span class="marks">[3]</span>
   (b) Write the ground-state electronic configurations of ₂₄Cr, ₂₆Fe, ₂₉Cu and
   ₃₀Zn, explaining the two anomalies. <span class="marks">[3]</span>
   (c) Calculate the de Broglie wavelength of an electron moving with a velocity of
   $1.0\times10^{7}\ \text{m s}^{-1}$. <span class="marks">[2]</span>

::: note Answer outline for Group C
**1 (b).** For a jump from $n_2$ to $n_1$, $\Delta E = 13.6(1/n_1^{2} - 1/n_2^{2})$ eV.
Since $\Delta E = hc/\lambda$,
$1/\lambda = (13.6\times1.602\times10^{-19})/(hc)\times(1/n_1^{2} - 1/n_2^{2})$,
and the constant evaluates to $1.097\times10^{7}\ \text{m}^{-1} = R_H$.
$n_1 = 1$ gives the Lyman series (UV), $n_1 = 2$ the Balmer series (visible) and
$n_1 = 3$ the Paschen series (IR).

**2 (b).** Cr [Ar]3d⁵4s¹, Fe [Ar]3d⁶4s², Cu [Ar]3d¹⁰4s¹, Zn [Ar]3d¹⁰4s².
Cr and Cu promote one 4s electron to 3d because a half-filled (d⁵) or completely
filled (d¹⁰) subshell is symmetrical and of lower energy.

**2 (c).** $\lambda = h/mv
= 6.626\times10^{-34}/(9.11\times10^{-31}\times1.0\times10^{7})
= 6.626\times10^{-34}/(9.11\times10^{-24}) = 7.27\times10^{-11}$ m
$= 0.727$ Å.
:::
