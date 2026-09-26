---
subject: Physics
grade: 12
unit: 23
title: Quantization of energy
hours: 8
area: Modern Physics
---

Rutherford's nuclear atom had a fatal flaw: an orbiting electron is an
accelerating charge, so classical physics says it must radiate and spiral into
the nucleus in about $10^{-8}$ s. Atoms do not do this, and the light they emit
is not a continuous rainbow but a set of sharp lines. Bohr's answer was that
energy inside an atom is **quantized**. This unit follows that idea from the
hydrogen atom to X-rays and to the matter waves behind Bohr's rule.

::: key What the exam wants from this unit
The heaviest Modern Physics unit, and a reliable source of a Group C question.
Master five things: derive $r_n$ and $E_n$ for hydrogen; use
$1/\lambda = R(1/n_f^2 - 1/n_i^2)$; quote $\lambda = h/p = 12.27/\sqrt{V}$ Å;
draw the X-ray spectrum; apply $2d\sin\theta = n\lambda$.
:::

## 23.1 Bohr's theory of hydrogen atom

Bohr kept Rutherford's nucleus but added three postulates.

::: definition Bohr's postulates
1. **Stationary orbits.** An electron can revolve only in certain circular
   orbits in which it does **not** radiate energy. The centripetal force is
   supplied by the electrostatic attraction of the nucleus.
2. **Quantization of angular momentum.** The allowed orbits are those for which
   the angular momentum is an integral multiple of $h/2\pi$:
   $$ mvr = \frac{nh}{2\pi}, \qquad n = 1, 2, 3, \ldots $$
3. **Frequency condition.** Radiation is emitted or absorbed only when the
   electron jumps between two stationary orbits, and then
   $$ h\nu = E_i - E_f $$
:::

$n$ is the **principal quantum number**.

::: derivation Radius, speed and energy of the $n^{th}$ orbit
For a hydrogen atom (nuclear charge $+e$), the Coulomb attraction provides the
centripetal force:

$$ \frac{1}{4\pi\varepsilon_0}\frac{e^{2}}{r^{2}} = \frac{mv^{2}}{r}
\qquad \Rightarrow \qquad mv^{2}r = \frac{e^{2}}{4\pi\varepsilon_0} \quad (i) $$

From the second postulate, $v = nh/(2\pi m r)$. Substituting into $(i)$:

$$ m\left(\frac{nh}{2\pi m r}\right)^{2} r = \frac{e^{2}}{4\pi\varepsilon_0}
\qquad \Rightarrow \qquad \frac{n^{2}h^{2}}{4\pi^{2}mr} = \frac{e^{2}}{4\pi\varepsilon_0} $$

$$ \boxed{r_n = \frac{\varepsilon_0 h^{2}}{\pi m e^{2}}\,n^{2}} $$

Putting in the constants, $r_1 = 5.29\times10^{-11}\ \text{m} = 0.529$ Å (the
**Bohr radius**), and $r_n \propto n^{2}$.

Eliminating $r$ instead gives the orbital speed

$$ v_n = \frac{e^{2}}{2\varepsilon_0 n h} = \frac{c}{137\,n} $$

so $v_1 = 2.19\times10^{6}\ \text{m s}^{-1}$, about $1/137$ of the speed of light.

**Energy.** From $(i)$ the kinetic energy is
$K = \tfrac{1}{2}mv^{2} = e^{2}/(8\pi\varepsilon_0 r)$, and the electrostatic
potential energy is $U = -e^{2}/(4\pi\varepsilon_0 r)$. Hence

$$ E = K + U = \frac{e^{2}}{8\pi\varepsilon_0 r} - \frac{e^{2}}{4\pi\varepsilon_0 r}
= -\frac{e^{2}}{8\pi\varepsilon_0 r} $$

Substituting $r_n$:

$$ \boxed{E_n = -\frac{me^{4}}{8\varepsilon_0^{2}h^{2}n^{2}} = -\frac{13.6}{n^{2}}\ \text{eV}} $$
:::

Note $U = -2K$ and $E = -K$: the energy is negative, so the electron is
**bound**. $E = 0$ means a free, stationary electron.

::: caution Bohr's model is not general
It works for hydrogen and hydrogen-like ions (He⁺, Li²⁺, where
$E_n = -13.6\,Z^{2}/n^{2}$ eV and $r_n = 0.529\,n^{2}/Z$ Å), but fails for any
atom with two or more electrons. Do not apply it to helium or sodium.
:::

## 23.2 Spectral series; Excitation and ionization potentials

Combining the frequency condition with $E_n$ and $\nu = c/\lambda$:

$$ \frac{1}{\lambda} = \frac{me^{4}}{8\varepsilon_0^{2}h^{3}c}
\left(\frac{1}{n_f^{2}} - \frac{1}{n_i^{2}}\right)
= R\left(\frac{1}{n_f^{2}} - \frac{1}{n_i^{2}}\right) $$

where $R = 1.097\times10^{7}\ \text{m}^{-1}$ is the **Rydberg constant**. All
transitions ending on the same $n_f$ form one **spectral series**.

| Series | $n_f$ | $n_i$ | Region | Longest $\lambda$ | Series limit |
|---|---|---|---|---|---|
| Lyman | 1 | 2, 3, … | Ultraviolet | 121.6 nm | 91.2 nm |
| Balmer | 2 | 3, 4, … | Visible | 656.3 nm | 364.6 nm |
| Paschen | 3 | 4, 5, … | Infrared | 1875 nm | 820.4 nm |
| Brackett | 4 | 5, 6, … | Infrared | 4051 nm | 1458 nm |
| Pfund | 5 | 6, 7, … | Far infrared | 7460 nm | 2279 nm |

The **series limit** is the $n_i \to \infty$ line, $\lambda_{\min} = n_f^{2}/R$.

::: memory Order of the series
**L**yman, **B**almer, **P**aschen, **B**rackett, **P**fund — "**L**ittle
**B**oys **P**lay **B**etter **F**ootball" — ending on $n_f = 1,2,3,4,5$.
:::

**Excitation potential.** The p.d. through which an electron must be
accelerated so that, on colliding with an atom, it can lift that atom from the
ground state to the level $n$:

$$ V_{exc} = \frac{E_n - E_1}{e} $$

For hydrogen the first excitation potential is $(-3.4) - (-13.6) = 10.2$ V and
the second is $(-1.51)-(-13.6) = 12.09$ V.

**Ionization potential.** The potential needed to take the electron from
$n=1$ to $n=\infty$: for hydrogen $V_{ion} = 13.6$ V, so the **ionization
energy** is 13.6 eV.

::: example Worked example 23.1
**Problem.** Find (a) the radius and energy of the $n = 3$ orbit of hydrogen,
and (b) the wavelength of the photon emitted in the transition $n = 3 \to 2$.

**Solution.**

(a) $r_3 = 0.529 \times 3^{2} = 4.76$ Å $= 4.76\times10^{-10}$ m;
$E_3 = -13.6/9 = -1.51$ eV.

(b) $\Delta E = E_3 - E_2 = -1.51 - (-3.40) = 1.89\ \text{eV}$.

Using $\lambda = hc/\Delta E$ with $hc = 1240\ \text{eV nm}$,

$$ \lambda = \frac{1240}{1.89} = 656\ \text{nm} $$

This is the red $H_\alpha$ line of the Balmer series.
:::

## 23.3 Energy level; Emission and absorption spectra

Drawing the allowed energies as horizontal lines gives the **energy-level
diagram**. Since $E_n \propto -1/n^{2}$, the levels crowd together as $n$ grows
and converge on the ionization limit $E = 0$. Above it lies a continuum: a free
electron may have any energy.

```figure caption="Left: hydrogen levels drawn to scale in energy — note how they crowd towards the ionization limit. Right: the same levels drawn equally spaced (not to scale) so that the five named series can be shown. Each arrow is one emitted photon."
import numpy as np, matplotlib.pyplot as plt
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(5.1, 4.3),
                               gridspec_kw={'width_ratios': [1.0, 2.0]})

# ---- left: true energy scale ----
for n in range(1, 9):
    E = -13.6/n**2
    ax1.plot([0.1, 0.9], [E, E], color=INK, lw=1.3)
ax1.plot([0.1, 0.9], [0, 0], color=MUTED, lw=1.1, ls='--')
ax1.annotate('n = 1', (0.9, -13.6), xytext=(3, 2), textcoords='offset points', fontsize=8)
ax1.annotate('n = 2', (0.9, -3.4), xytext=(3, 2), textcoords='offset points', fontsize=8)
ax1.annotate('n = 3', (0.9, -1.51), xytext=(3, -1), textcoords='offset points', fontsize=8)
ax1.annotate('n → ∞', (0.9, 0), xytext=(3, 2), textcoords='offset points',
             fontsize=8, color=MUTED)
ax1.set_ylabel('energy  $E_n$  (eV)')
ax1.set_ylim(-14.6, 1.6); ax1.set_xlim(0, 1.7)
ax1.set_xticks([]); ax1.spines[['top', 'right', 'bottom']].set_visible(False)
ax1.set_yticks([-13.6, -10, -5, 0])

# ---- right: schematic, equally spaced ----
lab = {1: '-13.6', 2: '-3.40', 3: '-1.51', 4: '-0.85', 5: '-0.54', 6: '-0.38'}
for n in range(1, 7):
    ax2.plot([0.0, 4.75], [n, n], color=INK, lw=1.3)
    ax2.annotate(f'n = {n}   {lab[n]} eV', (-0.12, n), ha='right', va='center',
                 fontsize=7.4, color=MUTED)
ax2.plot([0.0, 4.75], [6.9, 6.9], color=MUTED, lw=1.1, ls='--')
ax2.annotate('n → ∞   0 eV', (-0.12, 6.9), ha='right', va='center',
             fontsize=7.4, color=MUTED)
ax2.annotate('(ionization)', (-0.12, 6.45), ha='right', va='center',
             fontsize=7.4, color=MUTED)

series = [('Lyman\n(UV)', 1, [2, 3, 4], 0.55, SERIES[4]),
          ('Balmer\n(visible)', 2, [3, 4, 5], 1.50, SERIES[1]),
          ('Paschen\n(IR)', 3, [4, 5, 6], 2.45, SERIES[3]),
          ('Brackett', 4, [5, 6], 3.35, SERIES[2]),
          ('Pfund', 5, [6], 4.10, SERIES[5])]
for name, nf, tops, x0, col in series:
    for k, ni in enumerate(tops):
        x = x0 + 0.24*k
        ax2.annotate('', xy=(x, nf), xytext=(x, ni),
                     arrowprops=dict(arrowstyle='-|>', color=col, lw=1.25,
                                     shrinkA=0, shrinkB=0, mutation_scale=9))
    ax2.annotate(name, (x0 + 0.12*(len(tops)-1), nf - 0.22), va='top',
                 ha='center', fontsize=7.4, color=col)
ax2.set_ylim(-0.95, 7.4); ax2.set_xlim(-2.05, 5.0)
ax2.axis('off')
fig.subplots_adjust(wspace=0.05)
```

**Emission spectrum.** An atom excited by heat, discharge or collision is
unstable and drops back within about $10^{-8}$ s, emitting a photon of energy
$E_i - E_f$. The result is a **bright-line spectrum**: coloured lines on a dark
background.

**Absorption spectrum.** White light passed through cool hydrogen gas loses
exactly those photons that can lift atoms to a higher level, giving a
**dark-line spectrum** at the same wavelengths as the emission lines.

| Feature | Emission spectrum | Absorption spectrum |
|---|---|---|
| Produced by | hot/excited gas | cool gas in front of a hot continuum source |
| Appearance | bright lines on dark ground | dark lines on bright ground |
| Transition | $n_i \to n_f$ (downward) | $n_f \to n_i$ (upward) |
| Lines observed | all series | mainly Lyman (from the ground state) |

The dark **Fraunhofer lines** in sunlight are an absorption spectrum produced by
the Sun's cooler outer gases, and they are how we know what stars are made of.

::: example Worked example 23.2
**Problem.** A hydrogen atom in its ground state is bombarded by an electron
accelerated through 12.5 V. To which level can the atom be excited, and what
wavelengths can it then emit?

**Solution.** The electron brings 12.5 eV. Energies needed from $n=1$ are
$E_2 - E_1 = 10.2$ eV, $E_3 - E_1 = 12.09$ eV, $E_4 - E_1 = 12.75$ eV. Since
$12.09 < 12.5 < 12.75$, the atom can reach **$n = 3$** but not $n = 4$.

From $n = 3$ three transitions are possible:

$3 \to 2$: $\Delta E = 1.89$ eV, $\lambda = 1240/1.89 = 656$ nm (Balmer)
$3 \to 1$: $\Delta E = 12.09$ eV, $\lambda = 1240/12.09 = 103$ nm (Lyman)
$2 \to 1$: $\Delta E = 10.2$ eV, $\lambda = 1240/10.2 = 122$ nm (Lyman)
:::

## 23.4 De Broglie Theory; Duality

Light behaves as a wave in diffraction and as photons in the photoelectric
effect. In 1924 de Broglie proposed that this **duality** is universal: every
moving particle has an associated wave of wavelength

$$ \lambda = \frac{h}{p} = \frac{h}{mv} $$

For a photon, $E = h\nu$ and $E = pc$ give $p = h/\lambda$; de Broglie read this
backwards for matter. For an electron accelerated from rest through a p.d. $V$,
$\tfrac12 mv^{2} = eV$, so $p = \sqrt{2meV}$ and

$$ \lambda = \frac{h}{\sqrt{2meV}} = \frac{12.27}{\sqrt{V}}\ \text{Å}
\qquad (V \text{ in volts}) $$

::: key Why ordinary objects show no wave behaviour
$h = 6.63\times10^{-34}$ J s is minute. A 60 kg student running at
$5\ \text{m s}^{-1}$ has $\lambda = 2.2\times10^{-36}$ m — smaller than any
possible obstacle, so no diffraction is observable. Wave behaviour appears only
when $\lambda$ is comparable to the aperture, i.e. for electrons and atoms.
:::

The **Davisson–Germer experiment** (1927) confirmed this: electrons
accelerated through 54 V and scattered from a nickel crystal gave a strong beam
at $50^{\circ}$, matching the predicted $12.27/\sqrt{54} = 1.67$ Å.

De Broglie's hypothesis also **explains Bohr's second postulate**: a stable
orbit is a standing wave that joins on to itself round the circumference,

$$ 2\pi r = n\lambda = \frac{nh}{mv} \qquad \Rightarrow \qquad mvr = \frac{nh}{2\pi} $$

which is exactly the quantization rule Bohr had to assume.

```figure caption="A Bohr orbit is a standing electron wave: the circumference must hold a whole number of de Broglie wavelengths, $2\pi r = n\lambda$. Left $n = 4$ (allowed), right a non-integral fit (the wave cancels itself, so the orbit is not allowed)."
import numpy as np, matplotlib.pyplot as plt
fig, axes = plt.subplots(1, 2, figsize=(5.0, 2.6))
for ax, n, ok in zip(axes, [4, 3.4], [True, False]):
    th = np.linspace(0, 2*np.pi, 900)
    R, a = 1.0, 0.16
    r = R + a*np.sin(n*th)
    ax.plot(R*np.cos(th), R*np.sin(th), color=MUTED, lw=0.9, ls=':')
    col = ACCENT if ok else SERIES[1]
    ax.plot(r*np.cos(th), r*np.sin(th), color=col, lw=1.7)
    ax.plot([0], [0], 'o', color=INK, ms=5)
    ax.annotate('nucleus', (0, 0), xytext=(0, -13), textcoords='offset points',
                ha='center', fontsize=7.6, color=MUTED)
    ax.set_title('n = 4  allowed' if ok else 'not a whole number — forbidden',
                 fontsize=8.6, color=col)
    ax.set_aspect('equal'); ax.set_xlim(-1.35, 1.35); ax.set_ylim(-1.35, 1.35)
    ax.axis('off')
```

::: example Worked example 23.3
**Problem.** Calculate the de Broglie wavelength of an electron accelerated
through 100 V. Take $h = 6.63\times10^{-34}$ J s, $m = 9.1\times10^{-31}$ kg,
$e = 1.6\times10^{-19}$ C.

**Solution.**

$$ p = \sqrt{2meV} = \sqrt{2(9.1\times10^{-31})(1.6\times10^{-19})(100)} $$

$$ p = \sqrt{2.912\times10^{-47}} = 5.40\times10^{-24}\ \text{kg m s}^{-1} $$

$$ \lambda = \frac{h}{p} = \frac{6.63\times10^{-34}}{5.40\times10^{-24}}
= 1.23\times10^{-10}\ \text{m} = 1.23\ \text{Å} $$

Check with the shortcut: $12.27/\sqrt{100} = 1.227$ Å. This is about the spacing
of atoms in a crystal, which is why electron diffraction works.
:::

## 23.5 Uncertainty principle

If an electron is a wave spread over a region, asking for its exact position is
meaningless. Heisenberg made this quantitative in 1927.

::: definition Heisenberg's uncertainty principle
It is impossible to measure simultaneously both the position and the momentum of
a particle with unlimited accuracy. If $\Delta x$ and $\Delta p$ are the
uncertainties in position and in the momentum component along the same
direction, then

$$ \Delta x \cdot \Delta p \ge \frac{h}{4\pi} $$

An equivalent statement for energy and time is
$\Delta E \cdot \Delta t \ge \dfrac{h}{4\pi}$.
:::

This is not a limitation of our instruments; it is a property of nature. Two
standard consequences:

- **Electrons cannot exist inside the nucleus.** Confining an electron to
  $\Delta x \approx 10^{-14}$ m needs $\Delta p \ge h/(4\pi\Delta x)$, an energy
  of about 20 MeV, whereas beta particles carry only a few MeV. The electron is
  *created* at the moment of decay, not stored.
- **Natural line width.** A state living for $\Delta t \approx 10^{-8}$ s has an
  energy blur $\Delta E \ge h/4\pi\Delta t$, so spectral "lines" are never
  infinitely sharp.

::: caution Uncertainty is not experimental error
$\Delta x$ and $\Delta p$ are not mistakes in reading a scale: even with perfect
apparatus the product cannot fall below $h/4\pi$. The principle links $x$ with
$p_x$ only — $\Delta x$ and $\Delta p_y$ are unrestricted.
:::

::: example Worked example 23.4
**Problem.** The position of an electron is measured to an accuracy of
$10^{-10}$ m. Find the minimum uncertainty in its velocity.

**Solution.**

$$ \Delta v \ge \frac{h}{4\pi m\,\Delta x}
= \frac{6.63\times10^{-34}}{4\pi(9.1\times10^{-31})(10^{-10})} $$

Denominator $= 4 \times 3.1416 \times 9.1\times10^{-31} \times 10^{-10}
= 1.144\times10^{-39}$.

$$ \Delta v \ge \frac{6.63\times10^{-34}}{1.144\times10^{-39}}
= 5.8\times10^{5}\ \text{m s}^{-1} $$

The uncertainty is about a quarter of the electron's own orbital speed in
hydrogen — so the idea of a definite "orbit" is not really tenable.
:::

## 23.6 X-rays: Nature and production; uses

X-rays were discovered by Röntgen in 1895. They are **electromagnetic waves** of
wavelength roughly $0.01$ Å to $100$ Å (0.001–10 nm), produced when fast
electrons are suddenly stopped by a heavy target — the reverse of the
photoelectric effect.

```figure caption="Coolidge X-ray tube. Electrons boiled off the hot filament are accelerated through 20–100 kV onto a tungsten target set in a copper anode; less than 1% of their energy becomes X-rays and the rest becomes heat."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, Polygon
fig, ax = plt.subplots(figsize=(5.0, 3.0))

ax.add_patch(FancyBboxPatch((0.6, 1.0), 7.2, 3.2, boxstyle='round,pad=0.25',
                            fc='none', ec=INK, lw=1.5))
ax.annotate('evacuated glass envelope', (2.4, 4.75), ha='center', fontsize=8, color=MUTED)

# filament (cathode)
th = np.linspace(0, 6*np.pi, 200)
ax.plot(1.35 + 0.12*np.sin(th), 2.3 + 0.9*th/(6*np.pi), color=SERIES[1], lw=1.6)
ax.add_patch(Polygon([[1.0, 2.1], [1.75, 2.1], [1.95, 3.5], [1.75, 3.35],
                      [1.0, 3.35]], closed=True, fc='none', ec=INK, lw=1.2))
ax.annotate('heated filament\n(cathode, −)', (1.55, 1.95), ha='center', va='top',
            fontsize=7.8, color=INK)

# anode with slanted target
ax.add_patch(Rectangle((6.3, 1.6), 0.75, 2.2, fc='#dfe7f1', ec=INK, lw=1.2))
ax.add_patch(Polygon([[6.3, 3.8], [6.3, 2.5], [5.55, 3.8]], closed=True,
                     fc=SERIES[3], ec=INK, lw=1.1))
ax.annotate('tungsten target on\ncopper anode (+)', xy=(6.05, 3.35), xytext=(6.9, 4.85),
            ha='center', fontsize=7.8, color=INK,
            arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.9))
for k in range(4):
    ax.plot([7.05, 7.55], [1.85 + 0.5*k, 1.85 + 0.5*k], color=MUTED, lw=1.4)
ax.annotate('cooling fins', (8.38, 2.6), rotation=90, va='center', ha='center',
            fontsize=7.4, color=MUTED)

# electron beam
ax.annotate('', xy=(5.95, 3.15), xytext=(2.1, 3.15),
            arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=2.0, mutation_scale=14))
ax.annotate('electron beam', (4.0, 3.3), ha='center', fontsize=8, color=ACCENT)

# X-rays out
for dx in (-1.15, -0.65, -0.15):
    ax.annotate('', xy=(5.95 + dx, 1.20), xytext=(5.95, 3.05),
                arrowprops=dict(arrowstyle='-|>', color=SERIES[2], lw=1.3,
                                mutation_scale=10))
ax.annotate('X-rays', (5.1, 1.00), ha='center', fontsize=8.4, color=SERIES[2])

# supplies
ax.plot([1.35, 1.35], [0.55, 1.15], color=INK, lw=1.1)
ax.plot([6.7, 6.7], [0.55, 1.35], color=INK, lw=1.1)
ax.plot([1.35, 6.7], [0.55, 0.55], color=INK, lw=1.1)
ax.plot([3.6, 3.6], [0.35, 0.75], color=INK, lw=1.6)
ax.plot([3.9, 3.9], [0.45, 0.65], color=INK, lw=1.6)
ax.annotate('high voltage  20–100 kV', (4.7, 0.30), ha='center', fontsize=7.8, color=INK)

ax.set_xlim(0.1, 9.0); ax.set_ylim(0.0, 5.35)
ax.axis('off')
```

**Two processes go on at the target, giving two parts to the spectrum.**

1. **Continuous (Bremsstrahlung) spectrum.** An electron decelerating in the
   field of a target nucleus radiates, and may lose any fraction of its energy,
   so all wavelengths above a limit appear. The limit comes from an electron
   that gives up *all* its energy in one collision:

   $$ eV = h\nu_{\max} = \frac{hc}{\lambda_{\min}}
   \qquad \Rightarrow \qquad
   \lambda_{\min} = \frac{hc}{eV} = \frac{1.24\times10^{-6}}{V}\ \text{m} $$

   This **Duane–Hunt limit** depends only on the accelerating voltage, not on
   the target material.

2. **Characteristic spectrum.** A fast electron knocks an electron out of the
   K shell of a target atom; an L-shell electron falling into the vacancy emits
   the sharp $K_\alpha$ line, an M-shell electron the $K_\beta$ line. These
   positions depend only on the **target element** (Moseley's law).

```figure caption="X-ray spectrum of a molybdenum target at two accelerating voltages. The continuous background cuts off sharply at $\lambda_{min} = hc/eV$, which moves left as $V$ rises, while the characteristic $K_\alpha$ and $K_\beta$ lines stay fixed."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0, 2.9))
lam = np.linspace(0.02, 0.13, 1400)   # nm

def spectrum(V_kV, scale):
    lmin = 1239.8 / (V_kV * 1000.0)    # nm, since hc = 1239.8 eV nm
    y = np.zeros_like(lam)
    m = lam > lmin
    y[m] = scale * (1.0/lam[m]**2) * (lam[m]/lmin - 1.0)
    return lmin, y

for V, col, ls in [(35, ACCENT, '-'), (25, SERIES[3], '--')]:
    lmin, y = spectrum(V, 1.0)
    y = y / 400.0
    if V == 35:
        for lc, amp, w in [(0.0709, 0.80, 0.0013), (0.0632, 0.42, 0.0012)]:
            y = y + amp*np.exp(-0.5*((lam - lc)/w)**2)
    ax.plot(lam, y, color=col, ls=ls, lw=1.6, label=f'{V} kV')
    ax.plot([lmin, lmin], [0, 0.62], color=col, lw=0.9, ls=':')
    ax.annotate(f'$\\lambda_{{min}}$ = {lmin*1000:.1f} pm', (lmin, 0.66), rotation=90,
                fontsize=7.2, color=col, ha='center', va='bottom')

ax.annotate('K$_\\alpha$', (0.0709, 1.34), ha='center', fontsize=9, color=INK)
ax.annotate('K$_\\beta$', (0.0632, 0.95), ha='center', fontsize=9, color=INK)
ax.annotate('continuous\n(Bremsstrahlung)', (0.102, 0.30), fontsize=7.8,
            color=MUTED, ha='center')
ax.set_xlabel('wavelength  λ  (nm)'); ax.set_ylabel('intensity (arb.)')
ax.set_xlim(0.02, 0.13); ax.set_ylim(0, 1.55)
ax.set_yticks([])
ax.spines[['top', 'right']].set_visible(False)
ax.grid(True, axis='x', alpha=0.4)
ax.legend(title='tube voltage', loc='upper right')
```

**Properties.** X-rays travel in straight lines at the speed of light, are
undeflected by electric and magnetic fields, penetrate matter, ionize gases,
affect photographic plates, cause fluorescence and are diffracted by crystals.

| Use | Basis |
|---|---|
| Medical radiography, CT scan | bone (high $Z$) absorbs more than soft tissue |
| Radiotherapy | hard X-rays destroy malignant cells |
| Airport and customs scanning | differential absorption reveals hidden metal |
| Detecting cracks in castings | voids transmit more |
| X-ray crystallography | $\lambda$ comparable to atomic spacing |

**Hard and soft X-rays.** A high tube voltage gives short wavelength and high
penetrating power ("hard" X-rays, used in radiotherapy); a low voltage gives
"soft", less penetrating X-rays used for imaging soft tissue.

## 23.7 X-rays diffraction; Bragg's law

An optical grating has lines about $10^{-6}$ m apart — far too coarse to
diffract X-rays of wavelength $10^{-10}$ m. Laue realised in 1912 that the
atomic planes of a crystal, spaced about $10^{-10}$ m apart, form a natural
three-dimensional grating.

```figure caption="Bragg reflection. B lies directly below P, a distance $d$ away. PA and PC are wavefronts, so the lower ray travels the extra path $AB + BC = 2d\sin\theta$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0, 3.0))
d = 1.0
th = np.radians(30.0)
s, c = np.sin(th), np.cos(th)
dirin = np.array([c, -s]); dirout = np.array([c, s])

for k in range(3):
    y = -k*d
    ax.plot([0.1, 7.4], [y, y], color=MUTED, lw=0.9, zorder=1)
    for x in np.arange(0.35, 7.4, 0.5):
        ax.plot([x], [y], 'o', color=INK, ms=4.0, zorder=2)

P = np.array([3.55, 0.0]); B = np.array([3.55, -d])
L = 2.9
for Q in (P, B):
    ax.annotate('', xy=Q, xytext=Q - L*dirin,
                arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.5,
                                shrinkA=0, shrinkB=0, mutation_scale=11), zorder=4)
    ax.annotate('', xy=Q + L*dirout, xytext=Q,
                arrowprops=dict(arrowstyle='-|>', color=SERIES[1], lw=1.5,
                                shrinkA=0, shrinkB=0, mutation_scale=11), zorder=4)

A = B - d*s*dirin
C = B + d*s*dirout
ax.plot([P[0], A[0]], [P[1], A[1]], color=INK, lw=1.1, ls='--', zorder=5)
ax.plot([P[0], C[0]], [P[1], C[1]], color=INK, lw=1.1, ls='--', zorder=5)
ax.plot([P[0], B[0]], [P[1], B[1]], color=SERIES[2], lw=1.2, zorder=5)
for pt, name, off in [(P, 'P', (-4, 7)), (A, 'A', (-12, 2)), (B, 'B', (-3, -13)),
                      (C, 'C', (7, -2))]:
    ax.plot([pt[0]], [pt[1]], 'o', color=SERIES[4], ms=4.6, zorder=6)
    ax.annotate(name, pt, xytext=off, textcoords='offset points',
                fontsize=9.5, color=SERIES[4], zorder=6)

ax.annotate('θ', (P[0]-0.80, P[1]+0.11), fontsize=10, color=INK)
ax.annotate('θ', (P[0]+0.62, P[1]+0.10), fontsize=10, color=INK)
ax.annotate('', xy=(0.85, 0.0), xytext=(0.85, -d),
            arrowprops=dict(arrowstyle='<|-|>', color=SERIES[2], lw=1.2,
                            mutation_scale=9))
ax.annotate('d', (0.68, -0.5), fontsize=10, color=SERIES[2], ha='right', va='center')
ax.annotate('AB = BC = d sin θ,   so  2d sin θ = nλ', (3.9, -2.55),
            ha='center', fontsize=8.8, color=INK)
ax.set_xlim(0.0, 7.7); ax.set_ylim(-2.9, 2.3)
ax.set_aspect('equal'); ax.axis('off')
```

::: derivation Bragg's law
Take two atomic planes a distance $d$ apart and a beam striking them at a
**glancing angle** $\theta$. With $B$ vertically below $P$, the lower ray travels
the extra distance $AB + BC$, where $PA$ and $PC$ are wavefronts. From the
right-angled triangles $PAB$ and $PCB$,

$$ AB = BC = d\sin\theta \qquad \Rightarrow \qquad
\text{path difference} = 2d\sin\theta $$

Constructive interference (a bright spot) requires the path difference to be a
whole number of wavelengths:

$$ \boxed{2d\sin\theta = n\lambda, \qquad n = 1, 2, 3, \ldots} $$
:::

::: caution $\theta$ is measured from the plane, not from the normal
In optics the angle of incidence is measured from the normal; in Bragg's law
$\theta$ is the **glancing angle**, measured from the plane itself. Using the
normal angle replaces $\sin\theta$ by $\cos\theta$ and is always wrong.
:::

Since $\sin\theta \le 1$, Bragg reflection needs $\lambda \le 2d$. The law is
used both ways: with $\lambda$ known it measures $d$ (X-ray crystallography,
which gave us the structure of DNA); with $d$ known it measures $\lambda$ (the
X-ray spectrometer).

::: example Worked example 23.5
**Problem.** A beam of X-rays of wavelength $1.54$ Å gives a first-order Bragg
reflection from a set of crystal planes at a glancing angle of $15.9^{\circ}$.
Find the spacing of the planes. What is the largest order that can be observed?

**Solution.** For $n = 1$,

$$ d = \frac{n\lambda}{2\sin\theta} = \frac{1 \times 1.54\times10^{-10}}
{2\sin 15.9^{\circ}} = \frac{1.54\times10^{-10}}{2 \times 0.2740} $$

$$ d = 2.81\times10^{-10}\ \text{m} = 2.81\ \text{Å} $$

Highest order: $\sin\theta \le 1$ needs $n \le 2d/\lambda =
2(2.81)/1.54 = 3.65$, so **$n = 3$** is the highest order observable.
:::

## Chapter summary

- Bohr: $mvr = nh/2\pi$; $r_n = \varepsilon_0h^{2}n^{2}/\pi me^{2} = 0.529\,n^{2}$ Å;
  $v_n = c/137n$; $E_n = -13.6/n^{2}$ eV (multiply by $Z^{2}$, divide $r_n$ by
  $Z$, for hydrogen-like ions).
- $h\nu = E_i - E_f$ gives $1/\lambda = R(1/n_f^{2} - 1/n_i^{2})$,
  $R = 1.097\times10^{7}$ m⁻¹. Series: Lyman (UV, $n_f=1$), Balmer (visible),
  Paschen, Brackett, Pfund (IR).
- Hydrogen: first excitation potential 10.2 V, ionization potential 13.6 V.
  Emission gives bright lines, absorption dark lines at the same wavelengths.
- De Broglie: $\lambda = h/p = 12.27/\sqrt{V}$ Å for an accelerated electron;
  $2\pi r = n\lambda$ reproduces Bohr's quantization.
- Uncertainty: $\Delta x\,\Delta p \ge h/4\pi$ and $\Delta E\,\Delta t \ge h/4\pi$.
- X-ray tube: continuous spectrum with $\lambda_{\min} = hc/eV$ (depends on $V$)
  plus characteristic $K_\alpha$, $K_\beta$ lines (depend on the target).
- Bragg: $2d\sin\theta = n\lambda$, $\theta$ measured from the atomic plane.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The radius of the $n^{\text{th}}$ Bohr orbit of hydrogen is proportional to <span class="marks">[1]</span>
   (a) $n$ (b) $n^{2}$ (c) $1/n$ (d) $1/n^{2}$
2. The Balmer series of hydrogen lies in the <span class="marks">[1]</span>
   (a) ultraviolet (b) visible (c) infrared (d) X-ray region
3. The minimum wavelength of the continuous X-ray spectrum depends on <span class="marks">[1]</span>
   (a) the target material (b) the filament current
   (c) the accelerating voltage (d) the gas pressure in the tube
4. The de Broglie wavelength of an electron accelerated through 400 V is about <span class="marks">[1]</span>
   (a) 0.61 Å (b) 1.23 Å (c) 2.45 Å (d) 12.27 Å
5. In Bragg's law $2d\sin\theta = n\lambda$, the angle $\theta$ is measured between the incident ray and the <span class="marks">[1]</span>
   (a) normal to the crystal plane (b) crystal plane
   (c) reflected ray (d) surface of the crystal only

::: note Answers to Group A
**1.** (b) — $r_n = (\varepsilon_0h^{2}/\pi me^{2})n^{2}$.
**2.** (b) — transitions to $n = 2$ give 656–410 nm, which is visible light.
**3.** (c) — $\lambda_{\min} = hc/eV$ contains only $V$; the characteristic lines depend on the target.
**4.** (a) — $12.27/\sqrt{400} = 12.27/20 = 0.61$ Å.
**5.** (b) — $\theta$ is the glancing angle, measured from the plane.
:::

**Group B — Short answer (5 marks each)**

1. State Bohr's postulates and hence derive an expression for the radius of the
   $n^{\text{th}}$ orbit of a hydrogen atom. <span class="marks">[5]</span>
2. Distinguish between emission and absorption spectra. Why do the dark lines of
   the solar absorption spectrum occur at exactly the wavelengths of the bright
   lines of a laboratory hydrogen lamp? <span class="marks">[5]</span>
3. Calculate the wavelength of the first line and of the series limit of the
   Lyman series. Take $R = 1.097\times10^{7}\ \text{m}^{-1}$. <span class="marks">[5]</span>
4. An X-ray tube operates at 40 kV. Find the minimum wavelength of the emitted
   X-rays. Explain why the spectrum also contains sharp lines whose wavelengths
   do not change when the voltage is raised. <span class="marks">[5]</span>

::: note Answers to Group B
**1.** Postulates as in §23.1. Equating Coulomb and centripetal force,
$e^{2}/4\pi\varepsilon_0r^{2} = mv^{2}/r$; putting $v = nh/2\pi mr$ gives
$r_n = \varepsilon_0h^{2}n^{2}/\pi me^{2} = 0.529\,n^{2}$ Å.

**2.** See the comparison table in §23.3. The same pair of levels is involved in
both cases — upward in absorption, downward in emission — and the energy gap
$E_i - E_f$ is a property of the atom, so $\lambda = hc/\Delta E$ is identical.

**3.** First line, $n_i = 2 \to n_f = 1$:
$1/\lambda = 1.097\times10^{7}(1 - 1/4) = 8.228\times10^{6}\ \text{m}^{-1}$, so
$\lambda = 1.216\times10^{-7}\ \text{m} = 121.6$ nm.
Series limit, $n_i = \infty$: $1/\lambda = 1.097\times10^{7}(1) $, so
$\lambda = 9.12\times10^{-8}\ \text{m} = 91.2$ nm. Both are ultraviolet.

**4.** $\lambda_{\min} = hc/eV = (6.63\times10^{-34})(3\times10^{8}) /
[(1.6\times10^{-19})(4\times10^{4})] = 3.11\times10^{-11}$ m $= 0.311$ Å.
The sharp lines are the characteristic spectrum, whose photon energies are fixed
by the **target's** own energy levels, not by the tube voltage.
:::

**Group C — Long answer (8 marks each)**

1. (a) Using Bohr's postulates, derive an expression for the total energy of the
   electron in the $n^{\text{th}}$ orbit of a hydrogen atom, and show that it equals
   $-13.6/n^{2}$ eV. <span class="marks">[5]</span>
   (b) Draw an energy-level diagram and mark the Lyman, Balmer and Paschen
   series. Calculate the ionization potential and the first excitation potential
   of hydrogen. <span class="marks">[3]</span>
2. (a) State de Broglie's hypothesis and show that it leads to Bohr's
   quantization of angular momentum. <span class="marks">[4]</span>
   (b) A beam of electrons is accelerated through 10 kV and falls on a crystal
   whose planes are $2.0$ Å apart. Find the de Broglie wavelength and the
   glancing angle for first-order Bragg reflection. <span class="marks">[4]</span>

::: note Answer to Group C question 2(b)
$\lambda = 12.27/\sqrt{10000} = 12.27/100 = 0.1227$ Å $= 1.227\times10^{-11}$ m.

For $n = 1$: $\sin\theta = \dfrac{n\lambda}{2d} =
\dfrac{1.227\times10^{-11}}{2 \times 2.0\times10^{-10}} = 0.03068$, so
$\theta = 1.76^{\circ}$ — a very small glancing angle, because the electron
wavelength is far shorter than the plane spacing.
:::
