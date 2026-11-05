---
subject: Chemistry
grade: CEE
unit: 2
title: Atomic Structure
hours: 2
area: Physical Chemistry
---

Atomic structure carries about **two questions** in the paper (our estimate from the MEC
topic list). They are among the most predictable in Physical Chemistry: a Bohr-model
number (radius, speed or energy, almost always as a ratio in n and Z), a hydrogen-spectrum
question (series, wavelength, number of lines), a de Broglie or uncertainty calculation,
or a quantum-number rule (which set is allowed, how many nodes, the configuration of
Cr, Cu or a transition-metal ion). Learn the proportionalities and most questions take
under a minute.

::: key What the paper asks from this chapter
- Rutherford's α-scattering conclusions, and why the model fails (stability, line spectra).
- Bohr: $mvr = nh/2\pi$; $r \propto n^2/Z$ (0.529 Å), $v \propto Z/n$ (2.18 × 10⁶ m s⁻¹), $E \propto -Z^2/n^2$ (−13.6 eV); KE = −E, PE = 2E.
- Hydrogen spectrum: $1/\lambda = R_H Z^2 (1/n_1^2 - 1/n_2^2)$; the five series and their regions; number of lines $n(n-1)/2$.
- de Broglie $\lambda = h/mv = h/p$; Heisenberg $\Delta x \cdot \Delta p \geq h/4\pi$.
- The four quantum numbers and their allowed values; radial nodes $n - l - 1$, angular nodes $l$.
- Aufbau ($n + l$ rule), Pauli and Hund; the Cr and Cu exceptions; ions lose 4s electrons before 3d; counting unpaired electrons.
:::

## 2.1 Rutherford's and Bohr's atomic models; the spectrum of hydrogen

### Rutherford's nuclear model (1911)

Rutherford (with Geiger and Marsden) fired a beam of α-particles (He²⁺ nuclei) at a very
thin gold foil and counted the flashes they made on a zinc sulphide screen placed all
around it.

| Observation | Conclusion |
|---|---|
| Most α-particles passed straight through | Most of the atom is **empty space** |
| A few were deflected through large angles | The positive charge is concentrated in a tiny region — the **nucleus** — that repels the α-particles |
| A very small fraction bounced straight back | The nucleus is extremely small and holds almost all the **mass** |

**The model:** a tiny, dense, positive nucleus (radius about 10⁻¹⁵ m) with electrons
revolving round it in circular paths like planets (atom radius about 10⁻¹⁰ m — about
10⁵ times larger). Electrostatic attraction supplies the centripetal force.

**Why it failed.** (1) *Stability:* by classical electromagnetic theory an accelerating
(revolving) charge radiates energy, so the electron should spiral into the nucleus in a
fraction of a microsecond — atoms would collapse. (2) *Spectra:* a spiralling electron
would give a continuous spectrum, but atoms give **line** spectra. (3) It says nothing
about how the electrons are arranged.

### Bohr's model (1913)

1. Electrons revolve only in certain permitted circular orbits — **stationary states** —
   in which they do **not** radiate energy.
2. Only those orbits are allowed in which the angular momentum is a whole-number multiple
   of $h/2\pi$: $mvr = nh/2\pi$, $n = 1, 2, 3, \ldots$
3. Energy is emitted or absorbed only when an electron jumps between orbits, as one photon:
   $\Delta E = E_2 - E_1 = h\nu$.

For a one-electron species with nuclear charge Z (H, He⁺, Li²⁺, Be³⁺) these give:

| Quantity | Formula | Hydrogen, n = 1 | Varies as |
|---|---|---|---|
| Radius | $r_n = 0.529\,n^2/Z$ Å | 0.529 Å (Bohr radius) | $n^2/Z$ |
| Speed | $v_n = 2.18\times10^{6}\,Z/n$ m s⁻¹ | 2.18 × 10⁶ m s⁻¹ | $Z/n$ |
| Total energy | $E_n = -13.6\,Z^2/n^2$ eV | −13.6 eV = −2.18 × 10⁻¹⁸ J | $Z^2/n^2$ |
| Kinetic energy | $KE = -E_n$ | +13.6 eV | $Z^2/n^2$ |
| Potential energy | $PE = 2E_n$ | −27.2 eV | $Z^2/n^2$ |
| Angular momentum | $nh/2\pi$ | $h/2\pi$ | $n$ |
| Time for one revolution | $2\pi r/v$ | 1.5 × 10⁻¹⁶ s | $n^3/Z^2$ |

Hydrogen levels: E₁ = −13.6, E₂ = −3.40, E₃ = −1.51, E₄ = −0.85, E∞ = 0 eV. The energy
is negative because the electron is bound; zero means a free electron at rest at
infinity. As n increases the energy rises (becomes less negative) and the **gaps between
levels shrink**. Ionisation energy from the ground state is 13.6 Z² eV: H 13.6 eV
(1312 kJ mol⁻¹), He⁺ 54.4 eV, Li²⁺ 122.4 eV.

::: example Comparing orbits with ratios
**Problem.** Compare the radius, speed and energy of the electron in the n = 2 orbit of
He⁺ with those in the n = 1 orbit of hydrogen.

**Solution.** He⁺: Z = 2, n = 2. Radius ∝ n²/Z = 4/2 = 2, so r = 2 × 0.529 = **1.058 Å**
(twice hydrogen's). Speed ∝ Z/n = 1, so it is **the same**, 2.18 × 10⁶ m s⁻¹. Energy ∝
Z²/n² = 4/4 = 1, so it is **the same**, −13.6 eV. No formula beyond the ratios is needed.
:::

| Defect of Bohr's model | What it could not explain |
|---|---|
| Many-electron atoms | Works only for one-electron species; fails even for He |
| Fine structure | Each line, at high resolution, is a group of close lines |
| Zeeman and Stark effects | Splitting of lines in magnetic and electric fields |
| Dual nature and uncertainty | Treats the electron as a particle on a definite path, which de Broglie and Heisenberg forbid |
| Molecules | Cannot explain chemical bonding or molecular shapes |

### The spectrum of hydrogen

Light comes in packets (photons) of energy $E = h\nu = hc/\lambda$ (Planck). The
**wavenumber** $\bar{\nu} = 1/\lambda$ is the number of waves per unit length. A useful
shortcut: **E (eV) = 1240/λ (nm)**.

When hydrogen at low pressure is excited in a discharge tube, its light, passed through a
prism, gives sharp bright lines on a dark background: an **emission line spectrum**. Light
passed through cool hydrogen shows dark lines at the same wavelengths: an **absorption
spectrum**. Hot solids give continuous spectra, atoms give line spectra and molecules give
band spectra. Every hydrogen line fits the Rydberg equation, which Bohr's model derives:

$$ \bar{\nu} = \frac{1}{\lambda} = R_H Z^2\left(\frac{1}{n_1^2} - \frac{1}{n_2^2}\right), \qquad n_2 > n_1 $$

with $R_H = 1.097\times10^{7}$ m⁻¹ (109 678 cm⁻¹); Z = 1 for hydrogen.

| Series | n₁ | n₂ | Region | First (longest) line | Series limit (shortest) |
|---|---|---|---|---|---|
| Lyman | 1 | 2, 3, 4 … | ultraviolet | ≈ 122 nm | 91.2 nm |
| Balmer | 2 | 3, 4, 5 … | visible | 656 nm (Hα, red) | 365 nm |
| Paschen | 3 | 4, 5, 6 … | near infrared | 1875 nm | 820 nm |
| Brackett | 4 | 5, 6, 7 … | infrared | 4051 nm | 1458 nm |
| Pfund | 5 | 6, 7, 8 … | far infrared | 7458 nm | 2279 nm |

The four visible Balmer lines are Hα 656 nm (red), Hβ 486 nm (blue-green), Hγ 434 nm
(blue-violet) and Hδ 410 nm (violet). Within a series the lines crowd together towards
the series limit ($n_2 = \infty$).

```figure caption="Energy levels of the hydrogen atom, drawn to scale, $E_n = -13.6/n^2$ eV. Each series ends on one lower level. The levels n = 4, 5, 6 … crowd together just below n = ∞, which is why every series converges to a limit; the Brackett and Pfund jumps (ending on n = 4 and 5) are too short to draw at this scale."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(5.0,3.4))
E = lambda n: -13.6/n**2
for n in range(1, 8):
    ax.hlines(E(n), 0.0, 1.0, color=INK, lw=1.05)
ax.hlines(0, 0.0, 1.0, color=MUTED, lw=1.0, ls='--')
for n, lab in [(1, 'n = 1   −13.6 eV'), (2, 'n = 2   −3.40 eV'), (3, 'n = 3   −1.51 eV')]:
    ax.text(1.02, E(n), lab, va='center', fontsize=8.4, color=INK)
ax.text(1.02, 0.25, 'n = ∞   0 eV', va='center', fontsize=8.4, color=MUTED)
groups = [(1, [2, 3, 4, 5], SERIES[4], 'Lyman\n(UV)', 0.05),
          (2, [3, 4, 5, 6], SERIES[1], 'Balmer\n(visible)', 0.33),
          (3, [4, 5, 6], SERIES[2], 'Paschen\n(infrared)', 0.66)]
for nf, nis, c, lab, x0 in groups:
    for j, ni in enumerate(nis):
        x = x0 + j*0.055
        ax.annotate('', xy=(x, E(nf)), xytext=(x, E(ni)),
                    arrowprops=dict(arrowstyle='-|>', color=c, lw=1.3, mutation_scale=8))
    xm = x0 + (len(nis)-1)*0.055/2
    if nf == 1:
        ax.text(xm, E(1)-0.6, lab, ha='center', va='top', fontsize=8.2, color=c)
    else:
        ax.text(xm, -6.2, lab, ha='center', va='center', fontsize=8.2, color=c)
        ax.plot([xm, xm], [-5.3, E(nf)-0.15], color=c, lw=0.6, ls=':')
ax.set_xlim(-0.03, 1.38); ax.set_ylim(-17.2, 1.0)
ax.set_xticks([]); ax.set_yticks([])
ax.set_ylabel('energy (eV)')
ax.spines[['top','right','bottom']].set_visible(False)
```

**How many lines?** When electrons in a *sample* of atoms fall from level n₂ to level n₁
by every possible route, the number of distinct lines is $\Delta n(\Delta n + 1)/2$ with
$\Delta n = n_2 - n_1$; from level n to the ground state this is $n(n-1)/2$. A *single*
atom can give at most $n_2 - n_1$ lines on one trip down.

::: example A Balmer wavelength two ways
**Problem.** Find the wavelength of the line emitted in the jump n = 4 → n = 2 in
hydrogen.

**Solution.** Rydberg: $1/\lambda = 1.097\times10^{7}(1/4 - 1/16) = 1.097\times10^{7}\times0.1875 = 2.06\times10^{6}$ m⁻¹,
so λ = 4.86 × 10⁻⁷ m = **486 nm** (Hβ, blue-green). Energy route: ΔE = 3.40 − 0.85 =
2.55 eV, and λ = 1240/2.55 = 486 nm.
:::

::: example Counting spectral lines
**Problem.** Electrons in a sample of hydrogen atoms are excited to n = 6. How many lines
can appear in the emission spectrum, and how many of them belong to the Balmer series?

**Solution.** All lines: 6 × 5/2 = **15**. Balmer lines end on n = 2 and can start from
n = 3, 4, 5 or 6: **4 lines**.
:::

::: caution The traps in spectrum questions
- The **first** line of a series is its **longest** wavelength (smallest energy gap,
  $n_2 = n_1 + 1$); the series limit ($n_2 = \infty$) is its shortest.
- For He⁺ or Li²⁺ multiply the wavenumber by Z² — not by Z.
- Wavelength is inversely proportional to $(1/n_1^2 - 1/n_2^2)$: a ratio of wavelengths
  is the *inverse* ratio of these brackets. First Lyman : first Balmer = (5/36) : (3/4) =
  5 : 27.
:::

## 2.2 de Broglie's equation and Heisenberg's uncertainty principle

### de Broglie's wave–particle duality (1924)

Light behaves both as a wave (diffraction) and as particles (photoelectric effect).
de Broglie proposed that **every moving particle** also has a wave associated with it:

$$ \lambda = \frac{h}{mv} = \frac{h}{p} = \frac{h}{\sqrt{2m\,KE}} $$

For an electron accelerated from rest through a potential difference of V volts,
KE = eV, so λ ≈ 12.27/√V Å. Because λ ∝ 1/m, the wave is noticeable only for
microscopic particles. Davisson and Germer (1927) confirmed it by diffracting electrons
from a nickel crystal; the electron microscope uses the same idea.

**Bohr's rule from waves.** A stable orbit must hold a whole number of electron waves:
$2\pi r = n\lambda = nh/mv$, which rearranges to $mvr = nh/2\pi$ — Bohr's postulate.

::: example Electron against cricket ball
**Problem.** Find the de Broglie wavelength of (i) a 0.15 kg cricket ball bowled at
40 m s⁻¹, (ii) an electron moving at 2.18 × 10⁶ m s⁻¹ (m = 9.1 × 10⁻³¹ kg,
h = 6.63 × 10⁻³⁴ J s).

**Solution.** (i) λ = 6.63 × 10⁻³⁴/(0.15 × 40) = **1.1 × 10⁻³⁴ m** — hopelessly small to
detect. (ii) λ = 6.63 × 10⁻³⁴/(9.1 × 10⁻³¹ × 2.18 × 10⁶) = **3.3 × 10⁻¹⁰ m**, about the
size of an atom — in fact equal to the circumference of the first Bohr orbit,
2π × 0.529 Å = 3.3 Å.
:::

### Heisenberg's uncertainty principle (1927)

::: definition Uncertainty principle
It is impossible to determine simultaneously, with complete accuracy, both the position
and the momentum (or velocity) of a microscopic particle such as an electron:
$\Delta x \cdot \Delta p \geq h/4\pi$, that is $\Delta x \cdot \Delta v \geq h/4\pi m$.
:::

The more exactly the position is fixed, the less exactly the momentum is known (and
vice versa); if $\Delta x = 0$ then $\Delta p$ would be infinite. A similar relation holds
for energy and time, $\Delta E \cdot \Delta t \geq h/4\pi$. The uncertainty is not a fault of
instruments — observing an electron needs a photon, which disturbs it. **Consequence:** a
definite orbit (exact radius and exact speed together) has no meaning, so we speak only
of the **probability** of finding an electron, i.e. of orbitals.

::: example Uncertainty for an electron and a bullet
**Problem.** Find the minimum uncertainty in velocity of (i) an electron confined within
1.0 nm, (ii) a 10 g bullet whose position is known to within 1 μm.
(m_e = 9.1 × 10⁻³¹ kg, h = 6.63 × 10⁻³⁴ J s)

**Solution.** Δv = h/(4π m Δx).
(i) 6.63 × 10⁻³⁴/(4π × 9.1 × 10⁻³¹ × 1.0 × 10⁻⁹) = **5.8 × 10⁴ m s⁻¹** — large.
(ii) 6.63 × 10⁻³⁴/(4π × 0.010 × 1.0 × 10⁻⁶) = **5.3 × 10⁻²⁷ m s⁻¹** — utterly negligible.
:::

::: caution Where the factor goes wrong
The bound is $h/4\pi$, not $h$ and not $h/2\pi$ — setters put all three values among the
options. And the principle is about *simultaneous* measurement: position alone, or
momentum alone, can be measured as precisely as you like.
:::

## 2.3 Orbitals and quantum numbers; Aufbau, Pauli and Hund; electronic configuration

### Orbit and orbital

| Orbit (Bohr) | Orbital (quantum mechanics) |
|---|---|
| a definite circular path round the nucleus | a three-dimensional region where the probability of finding the electron is maximum |
| two-dimensional, fixed radius | three-dimensional, with a shape (s, p, d, f) |
| violates the uncertainty principle | consistent with it |
| holds up to 2n² electrons | holds at most 2 electrons |

### The four quantum numbers

| Quantum number | Symbol | Allowed values | Tells us |
|---|---|---|---|
| Principal | n | 1, 2, 3, … (K, L, M, N …) | shell; size and main energy |
| Azimuthal (angular momentum) | l | 0 to (n − 1); 0 = s, 1 = p, 2 = d, 3 = f | subshell and **shape** |
| Magnetic | m (mₗ) | −l … 0 … +l, i.e. 2l + 1 values | **orientation** in space |
| Spin | s (mₛ) | +½ or −½ | direction of spin |

| Counting rule | Formula | Examples |
|---|---|---|
| Subshells in shell n | n | n = 3: 3s, 3p, 3d |
| Orbitals in a subshell | 2l + 1 | s 1, p 3, d 5, f 7 |
| Electrons in a subshell | 2(2l + 1) | s 2, p 6, d 10, f 14 |
| Orbitals in shell n | n² | n = 3: 9 |
| Electrons in shell n | 2n² | n = 3: 18 |
| Radial (spherical) nodes | n − l − 1 | 3s: 2; 3p: 1; 3d: 0; 4d: 1 |
| Angular nodes (nodal planes) | l | s 0, p 1, d 2 |
| Total nodes | n − 1 | 4f: 3 |
| Orbital angular momentum | √(l(l + 1)) · h/2π | s: 0; p: √2 · h/2π |

Subshells that do not exist — **1p**, **2d** and **3f** — are favourite distractors:
l must always be less than n.

```figure caption="Shapes of orbitals (cross-sections of the boundary surfaces). Colours show the two signs of the wave function. An s orbital is spherical; a p orbital is a dumbbell with one nodal plane; d orbitals have two nodal surfaces — four lobes for d$_{xy}$, and for d$_{z^2}$ a dumbbell along z with a ring round its waist."
import numpy as np, matplotlib.pyplot as plt
fig, axs = plt.subplots(1, 4, figsize=(5.2, 2.4))
phi = np.linspace(0, 2*np.pi, 1441)
POS, NEG = SERIES[0], SERIES[1]
def draw(ax, f, scale=1.0):
    r = np.abs(f)*scale
    x, y = r*np.cos(phi), r*np.sin(phi)
    sgn = np.sign(f)
    start = 0
    for i in range(1, len(phi)+1):
        if i == len(phi) or sgn[i] != sgn[start]:
            if sgn[start] != 0 and i - start > 2:
                xs = np.concatenate([[0], x[start:i], [0]])
                ys = np.concatenate([[0], y[start:i], [0]])
                c = POS if sgn[start] > 0 else NEG
                ax.fill(xs, ys, color=c, alpha=0.30, lw=0)
                ax.plot(x[start:i], y[start:i], color=c, lw=1.1)
            start = i
def frame(ax, title, hx, vy):
    ax.set_xlim(-1.3, 1.3); ax.set_ylim(-1.3, 1.45)
    ax.set_aspect('equal'); ax.axis('off')
    ax.plot([-1.15, 1.15], [0, 0], color=MUTED, lw=0.6)
    ax.plot([0, 0], [-1.15, 1.15], color=MUTED, lw=0.6)
    ax.text(1.17, -0.04, hx, fontsize=8, color=MUTED, va='top')
    ax.text(0.06, 1.13, vy, fontsize=8, color=MUTED, va='bottom')
    ax.set_title(title, fontsize=9.6, color=INK, pad=2)
frame(axs[0], '1s', 'x', 'y')
axs[0].fill(0.8*np.cos(phi), 0.8*np.sin(phi), color=POS, alpha=0.30, lw=0)
axs[0].plot(0.8*np.cos(phi), 0.8*np.sin(phi), color=POS, lw=1.1)
frame(axs[1], '2p$_x$', 'x', 'y')
draw(axs[1], np.cos(phi), 1.0)
frame(axs[2], '3d$_{xy}$', 'x', 'y')
draw(axs[2], np.sin(2*phi), 1.0)
frame(axs[3], '3d$_{z^2}$', 'x', 'z')
th = np.pi/2 - phi
draw(axs[3], (3*np.cos(th)**2 - 1)/2, 1.0)
```

### Filling the orbitals: three rules

::: definition Aufbau, Pauli and Hund
**Aufbau principle.** In the ground state electrons occupy orbitals in order of increasing
energy. The order follows the **(n + l) rule**: the lower n + l fills first; if two
subshells have equal n + l, the one with lower n fills first.
**Pauli's exclusion principle.** No two electrons in an atom can have the same set of all
four quantum numbers — so an orbital holds at most two electrons, with opposite spins.
**Hund's rule of maximum multiplicity.** Electrons do not pair in degenerate orbitals (for
example the three 2p) until each has one electron; the single electrons have parallel
spins.
:::

```figure caption="The diagonal rule for the Aufbau order. Follow each arrow from its tail to its head, taking the arrows from the top: 1s 2s 2p 3s 3p 4s 3d 4p 5s 4d 5p 6s 4f 5d 6p 7s 5f 6d 7p. Every subshell on one arrow has the same value of n + l."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.4, 3.6))
rows = {1: 1, 2: 2, 3: 3, 4: 4, 5: 4, 6: 3, 7: 2}
letters = 'spdf'
for n, cnt in rows.items():
    for l in range(cnt):
        ax.text(l, -n, f'{n}{letters[l]}', ha='center', va='center', fontsize=10, color=INK,
                zorder=4, bbox=dict(fc='white', ec='none', pad=1.2))
for k in range(1, 9):
    mem = [(n, k-n) for n in range(1, 8) if 0 <= k-n < rows[n]]
    if not mem:
        continue
    top = min(mem, key=lambda t: t[0]); bot = max(mem, key=lambda t: t[0])
    x0, y0 = top[1] + 0.32, -top[0] + 0.32
    x1, y1 = bot[1] - 0.32, -bot[0] - 0.32
    ax.annotate('', xy=(x1, y1), xytext=(x0, y0), zorder=2,
                arrowprops=dict(arrowstyle='-|>', color=ACCENT, lw=1.1, mutation_scale=9, alpha=0.8))
    ax.text(top[1] + 0.40, -top[0] + 0.40, f'{k}', fontsize=8, color=SERIES[1], ha='left', va='bottom')
ax.text(3.3, -0.35, 'n + l', fontsize=8.4, color=SERIES[1], ha='left', va='bottom')
ax.set_xlim(-0.8, 4.0); ax.set_ylim(-7.9, 0.3)
ax.axis('off')
```

### Electronic configurations, exceptions and ions

| Species | Configuration | Unpaired e⁻ |
|---|---|---|
| N (7) | 1s² 2s² 2p³ | 3 |
| O (8) | 1s² 2s² 2p⁴ | 2 |
| K (19) | [Ar] 4s¹ | 1 |
| Sc (21) | [Ar] 3d¹ 4s² | 1 |
| **Cr (24)** | **[Ar] 3d⁵ 4s¹** (not 3d⁴ 4s²) | 6 |
| Mn (25) | [Ar] 3d⁵ 4s² | 5 |
| Fe (26) | [Ar] 3d⁶ 4s² | 4 |
| **Cu (29)** | **[Ar] 3d¹⁰ 4s¹** (not 3d⁹ 4s²) | 1 |
| Zn (30) | [Ar] 3d¹⁰ 4s² | 0 |
| Fe²⁺ / Fe³⁺ | [Ar] 3d⁶ / [Ar] 3d⁵ | 4 / 5 |
| Cu⁺ / Cu²⁺ | [Ar] 3d¹⁰ / [Ar] 3d⁹ | 0 / 1 |
| Mn²⁺ / Cr³⁺ / Zn²⁺ | [Ar] 3d⁵ / [Ar] 3d³ / [Ar] 3d¹⁰ | 5 / 3 / 0 |

- **Exceptions:** Cr and Cu (also Mo 4d⁵ 5s¹, Ag 4d¹⁰ 5s¹, Au 5d¹⁰ 6s¹) take one
  4s (ns) electron into the d subshell because **half-filled (d⁵) and completely filled
  (d¹⁰) subshells are extra stable** (symmetry and greater exchange energy).
- **Ions:** electrons are removed first from the shell of highest n — **4s before 3d**,
  although 4s filled first. Fe²⁺ is [Ar] 3d⁶, not [Ar] 3d⁴ 4s². Fe³⁺ (d⁵) is more stable
  than Fe²⁺ (d⁶), which is why iron(II) salts are slowly oxidised in air.
- A species with unpaired electrons is **paramagnetic** (attracted by a magnet); with all
  electrons paired it is **diamagnetic**. Spin-only magnetic moment
  $\mu = \sqrt{n(n+2)}$ BM for n unpaired electrons: Fe³⁺ (5) 5.92 BM, Cu²⁺ (1) 1.73 BM.

::: example Configurations of iron and its ions
**Problem.** Write the configurations of Fe (Z = 26), Fe²⁺ and Fe³⁺ and give the number
of unpaired electrons in each.

**Solution.** Fe: [Ar] 3d⁶ 4s². In the five 3d orbitals Hund's rule puts one electron in
each and pairs the sixth: **4 unpaired**. Fe²⁺: remove the two 4s electrons → [Ar] 3d⁶,
**4 unpaired**. Fe³⁺: remove one more from 3d → [Ar] 3d⁵, **5 unpaired** (one in each d
orbital).
:::

::: memory Quantum-number checks in five seconds
"l below n, m within ±l, s only ±½." A set fails if l ≥ n (2, 2, …), if |m| > l
(2, 1, −2, …) or if s is anything but ±½. Nodes: radial **n − l − 1**, angular **l**,
total **n − 1**.
:::

```photogrid label="2.1" cols="2" ratio="1.2" caption="Lines, not a continuum. (a) A spectroscope shows the sharp lines of an excited gas. (b) For hydrogen 1/lambda = R (1/2^2 - 1/n^2) with R = 1.0968 x 10^7 per metre gives the visible Balmer lines at 656.5 nm (n = 3, red), 486.3 nm (n = 4, blue-green), 434.2 nm (n = 5) and 410.3 nm (n = 6, violet), photon energies 1.89, 2.55, 2.86 and 3.02 eV. The lines crowd towards the series limit at 364.7 nm (n = infinity), where the electron is just freed from level 2."
@ photo id="phy12/spectroscope" cap="A laboratory spectroscope splits light from a discharge tube into lines"
fit 1.2
focus 0.5 0.5
@ svg cap="Balmer lines of hydrogen from the Rydberg formula"
def rgb(l):
    if l < 440: r, g, b = (440 - l) / 40, 0, 1
    elif l < 490: r, g, b = 0, (l - 440) / 50, 1
    elif l < 510: r, g, b = 0, 1, (510 - l) / 20
    elif l < 580: r, g, b = (l - 510) / 70, 1, 0
    elif l < 645: r, g, b = 1, (645 - l) / 65, 0
    else: r, g, b = 1, 0, 0
    return "#%02x%02x%02x" % tuple(int(255 * c) for c in (r, g, b))
R = 1.0968e7; hc = 1239.84
lam = lambda n: 1e9 / (R * (0.25 - 1 / n ** 2))
L = {n: lam(n) for n in (3, 4, 5, 6)}; lim = 1e9 / (R * 0.25)
assert abs(L[3] - 656.5) < 0.3 and abs(L[4] - 486.3) < 0.3 and abs(L[6] - 410.3) < 0.3 and abs(lim - 364.8) < 0.3
facts = dict(l3="%.1f" % L[3], l4="%.1f" % L[4], l5="%.1f" % L[5], l6="%.1f" % L[6], e3="%.2f" % (hc / L[3]), e4="%.2f" % (hc / L[4]), e5="%.2f" % (hc / L[5]), e6="%.2f" % (hc / L[6]), lim="%.1f" % lim)
f = Fig(300, 236)
f.text(150, 14, "Balmer series, n to 2", size=10.5, color=NAVY, bold=True)
X = lambda l: 20 + (l - 360) / 340 * 260
f.box(20, 34, 260, 70, fill="#0f172a", stroke="#0f172a", r=2)
for n, l in L.items():
    f.line(X(l), 34, X(l), 104, color=rgb(l) if l < 640 else "#ef4444", sw=3)
    f.text(X(l), 118, "%d" % n, size=10.5, color=NAVY, bold=True)
f.line(X(lim), 34, X(lim), 104, color="#94a3b8", sw=1.2, dash=True)
f.text(X(lim) + 3, 130, "limit", size=10.5, color=SLATE, anchor="start")
for l in (400, 500, 600, 700): f.text(X(l), 146, "%d" % l, size=10.5, color=SLATE)
f.text(150, 164, "wavelength in nm", size=10.5, color=SLATE)
f.text(150, 184, "n=3: %.1f nm, %.2f eV" % (L[3], hc / L[3]), size=10.5, color=RED, bold=True)
f.text(150, 202, "n=6: %.1f nm, %.2f eV" % (L[6], hc / L[6]), size=10.5, color="#6d28d9", bold=True)
f.text(150, 220, "series limit %.1f nm" % lim, size=10.5, color=NAVY, bold=True)
```

```photogrid label="2.2" cols="2" ratio="1.2" caption="Seeing atoms needs a short wavelength. (a) A transmission electron microscope accelerates electrons through tens of kilovolts and focuses them with magnetic lenses. (b) The cell applies de Broglie's relation, wavelength = h / p, with the relativistic correction for fast electrons: an electron accelerated through 100 V has a wavelength of 0.1226 nm, close to a bond length, while at 100 kV it is only 3.70 pm and at 200 kV 2.51 pm. Green light has a wavelength of 550 nm, about 219304 times longer than a 200 kV electron wave, so electrons resolve details that light cannot. The wave nature of matter is not a theory on paper but the working principle of an instrument."
@ photo id="ceechem2/tem" cap="A transmission electron microscope"
fit 1.2
focus 0.5 0.5
@ svg cap="de Broglie wavelength of accelerated electrons"
import math
h, m, e, c = 6.62607e-34, 9.10938e-31, 1.602177e-19, 2.99792458e8
def lam(V):
    return h / math.sqrt(2 * m * e * V * (1 + e * V / (2 * m * c * c)))
rows = [(v, lam(v) * 1e12) for v in (100, 1000, 100000, 200000)]
assert round(rows[0][1] / 1000, 4) == 0.1226 and round(rows[2][1], 2) == 3.70 and round(rows[3][1], 2) == 2.51
f = Fig(300, 236)
f.text(150, 12, "Electron wavelength, picometres", size=10.5, color=NAVY, bold=True)
import math as _m
hbars(f, [("%s V" % format(v, ","), _m.log10(p)) for v, p in rows], vmax=_m.log10(rows[0][1]), fmt="%.2f", x0=76, bw=130)
for i, (v, p) in enumerate(rows):
    f.text(292, 42 + i * 32, "%.2f pm" % p, size=9.5, color=SLATE, bold=True, anchor="end", vmid=True)
f.text(150, 178, "bar length = log10 of wavelength (pm)", size=10, color=SLATE, bold=True)
f.text(150, 200, "green light: 550 nm = 550,000 pm", size=10.5, color=NAVY, bold=True)
f.text(150, 218, "200 kV electron is %d times shorter" % round(550000 / rows[3][1]), size=10.5, color=SLATE, bold=True)
facts = dict(l100=rows[0][1] / 1000, k100=rows[2][1], k200=rows[3][1], ratio=round(550000 / rows[3][1]))
```

## Formula and fact sheet

| Quantity | Formula / value |
|---|---|
| Bohr radius | $r_n = 0.529\,n^2/Z$ Å |
| Bohr speed | $v_n = 2.18\times10^{6}\,Z/n$ m s⁻¹ |
| Bohr energy | $E_n = -13.6\,Z^2/n^2$ eV $= -2.18\times10^{-18}\,Z^2/n^2$ J $= -1312\,Z^2/n^2$ kJ mol⁻¹ |
| KE and PE | KE = −E; PE = 2E; PE/KE = −2 |
| Angular momentum | $mvr = nh/2\pi$ |
| Photon | $E = h\nu = hc/\lambda$; E (eV) = 1240/λ (nm); 1 eV = 1.6 × 10⁻¹⁹ J |
| Rydberg | $1/\lambda = R_H Z^2 (1/n_1^2 - 1/n_2^2)$, $R_H = 1.097\times10^{7}$ m⁻¹ |
| Number of lines | $\Delta n(\Delta n + 1)/2$; to ground state $n(n-1)/2$ |
| de Broglie | $\lambda = h/mv = h/p = h/\sqrt{2m\,KE}$; electron through V volts: 12.27/√V Å |
| Heisenberg | $\Delta x\cdot\Delta p \geq h/4\pi$; $\Delta x\cdot\Delta v \geq h/4\pi m$ |
| Orbitals and electrons | subshell 2l + 1 and 2(2l + 1); shell n² and 2n² |
| Nodes | radial n − l − 1; angular l; total n − 1 |
| Spin-only moment | $\mu = \sqrt{n(n+2)}$ BM |

Ionisation energies: H 13.6 eV, He⁺ 54.4 eV, Li²⁺ 122.4 eV. Series: Lyman (n₁ = 1, UV),
Balmer (2, visible), Paschen (3, IR), Brackett (4, IR), Pfund (5, far IR). Aufbau order:
1s 2s 2p 3s 3p 4s 3d 4p 5s 4d 5p 6s 4f 5d 6p 7s 5f 6d 7p. Exceptions: Cr 3d⁵ 4s¹,
Cu 3d¹⁰ 4s¹.

## Chapter summary

- Rutherford: most of the atom is empty; positive charge and mass sit in a nucleus about 10⁻¹⁵ m across. The model fails on stability and on line spectra.
- Bohr: stationary orbits with $mvr = nh/2\pi$; photons only on jumps, $\Delta E = h\nu$. For one-electron species $r \propto n^2/Z$, $v \propto Z/n$, $E = -13.6\,Z^2/n^2$ eV.
- Hydrogen lines obey $1/\lambda = R_H(1/n_1^2 - 1/n_2^2)$: Lyman (UV), Balmer (visible), Paschen, Brackett, Pfund (IR). A sample falling from level n gives $n(n-1)/2$ lines.
- de Broglie: $\lambda = h/mv$; significant only for tiny masses; $2\pi r = n\lambda$ gives Bohr's rule.
- Heisenberg: $\Delta x\cdot\Delta p \geq h/4\pi$, so orbits give way to orbitals (probability regions).
- Quantum numbers n, l (0 to n − 1), m (−l to +l), s (±½); radial nodes n − l − 1, angular nodes l.
- Aufbau by (n + l), Pauli (two electrons per orbital, opposite spins), Hund (no pairing until each degenerate orbital has one). Cr 3d⁵ 4s¹ and Cu 3d¹⁰ 4s¹; ions lose 4s before 3d.

## Practice questions

**Set A — Recall (20 questions)**

1. Rutherford's α-particle scattering experiment showed that
   (a) electrons revolve in fixed circular orbits (b) atoms are indivisible (c) the positive charge and most of the mass sit in a tiny nucleus (d) electrons behave as waves
2. Most α-particles passed through the gold foil without deflection. This showed that
   (a) most of the atom is empty space (b) the nucleus is positively charged (c) α-particles carry a positive charge (d) gold atoms are very heavy
3. Rutherford's nuclear model could NOT explain
   (a) the large-angle scattering of α-particles (b) the existence of a small, dense nucleus (c) why most α-particles pass straight through (d) the stability of the atom and its line spectrum
4. According to Bohr, the angular momentum of an electron in the nth orbit is
   (a) $nh/\pi$ (b) $nh/2\pi$ (c) $h/2\pi n$ (d) $n^2h/2\pi$
5. The energy of the electron in the ground state of the hydrogen atom is
   (a) −13.6 eV (b) +13.6 eV (c) −3.4 eV (d) 0 eV
6. The radius of the first Bohr orbit of hydrogen is about
   (a) 0.529 nm (b) 1.058 Å (c) 0.529 Å (d) 2.116 Å
7. The Balmer series of the hydrogen spectrum lies mainly in the
   (a) ultraviolet region (b) infrared region (c) microwave region (d) visible region
8. The lines of the Lyman series are produced by electron transitions ending at
   (a) n = 2 (b) n = 1 (c) n = 3 (d) n = ∞
9. de Broglie's equation for a particle of mass m moving with speed v is
   (a) λ = mv/h (b) λ = h/mv (c) λ = hv/m (d) λ = hm/v
10. Heisenberg's uncertainty principle is written as
   (a) Δx · Δp = 0 (b) Δx · Δp ≤ h/4π (c) Δx · Δp ≥ h/4π (d) Δx/Δp ≥ h/4π
11. The uncertainty principle is of practical importance only for
   (a) microscopic particles such as electrons (b) heavy bodies such as a cricket ball (c) bodies at rest (d) charged bodies of any size
12. The maximum number of electrons in a shell of principal quantum number n is
   (a) n² (b) 2n (c) 2l + 1 (d) 2n²
13. For l = 2, the number of allowed values of the magnetic quantum number is
   (a) 2 (b) 3 (c) 5 (d) 7
14. The shape of an orbital is decided by the
   (a) principal quantum number (b) azimuthal quantum number (c) magnetic quantum number (d) spin quantum number
15. "No two electrons in an atom can have the same set of all four quantum numbers." This is
   (a) Hund's rule (b) the Aufbau principle (c) Heisenberg's principle (d) Pauli's exclusion principle
16. Hund's rule of maximum multiplicity states that
   (a) electrons pair in degenerate orbitals only after each has one (b) electrons fill orbitals in order of increasing energy (c) an orbital holds at most two electrons (d) electrons of opposite spin attract each other
17. The shape of a p orbital is
   (a) spherical (b) dumbbell (c) cloverleaf (d) ring-shaped
18. The ground-state electronic configuration of chromium (Z = 24) is
   (a) [Ar] 3d⁴ 4s² (b) [Ar] 3d⁶ (c) [Ar] 3d³ 4s² 4p¹ (d) [Ar] 3d⁵ 4s¹
19. By the Aufbau principle, the subshell filled immediately after 4s is
   (a) 4p (b) 4d (c) 3d (d) 5s
20. The total number of orbitals in the shell with n = 3 is
   (a) 9 (b) 3 (c) 6 (d) 18

::: note Answers and explanations — Set A
**1.** (c) — Large-angle deflections and rebounds need a small, massive, positive centre: the nucleus. Fixed orbits (a) are Bohr's idea; wave behaviour (d) is de Broglie's.
**2.** (a) — An undeflected particle met nothing on its way, so most of the atom is empty space. Option (b) follows from the deflected particles, not the undeflected ones.
**3.** (d) — A revolving electron should radiate, spiral into the nucleus and give a continuous spectrum; the model explains (a), (b) and (c).
**4.** (b) — Bohr's quantum condition mvr = nh/2π. The other forms are distortions of it.
**5.** (a) — E₁ = −13.6 eV; the negative sign shows a bound electron. −3.4 eV is the n = 2 level.
**6.** (c) — r₁ = 0.529 Å = 0.0529 nm. (a) has the right digits but the wrong unit; 2.116 Å is n = 2.
**7.** (d) — n₁ = 2: its first four lines (656, 486, 434, 410 nm) are visible. Lyman is ultraviolet; Paschen, Brackett and Pfund are infrared.
**8.** (b) — Lyman lines end on n = 1, Balmer on 2, Paschen on 3.
**9.** (b) — λ = h/mv = h/p: wavelength is inversely proportional to momentum.
**10.** (c) — The product of the uncertainties can never be smaller than h/4π.
**11.** (a) — For an electron the uncertainty is comparable to atomic sizes and speeds; for heavy bodies it is immeasurably small.
**12.** (d) — 2n² (2, 8, 18, 32). n² is the number of orbitals; 2l + 1 counts orbitals in one subshell.
**13.** (c) — m runs from −2 to +2: −2, −1, 0, +1, +2, five values (five d orbitals).
**14.** (b) — l fixes the shape (s, p, d, f); n fixes size and energy, m the orientation, s the spin.
**15.** (d) — Pauli's principle; it limits an orbital to two electrons of opposite spin.
**16.** (a) — Degenerate orbitals are first singly occupied with parallel spins; (b) is Aufbau and (c) follows from Pauli.
**17.** (b) — Two lobes on opposite sides of a nodal plane; s is spherical and most d orbitals are cloverleaf-shaped.
**18.** (d) — The half-filled 3d⁵ subshell is extra stable, so one 4s electron moves into 3d.
**19.** (c) — 4s has n + l = 4; 3d, 4p and 5s all have 5, and among them 3d has the lowest n.
**20.** (a) — n² = 9 orbitals (one 3s, three 3p, five 3d). 18 is the number of electrons.
:::

**Set B — Understanding (14 questions)**

1. The radii of the first three Bohr orbits of hydrogen are in the ratio
   (a) 1 : 2 : 3 (b) 1 : 4 : 9 (c) 1 : 8 : 27 (d) 1 : 1/2 : 1/3
2. As n increases, the energy gap between successive Bohr orbits of hydrogen
   (a) increases (b) remains constant (c) first increases, then decreases (d) decreases
3. In Bohr's model the speed of the electron is proportional to
   (a) Z/n (b) n/Z (c) n² (d) Z²/n²
4. The total energy of an electron in a hydrogen orbit is −3.4 eV. Its kinetic and potential energies are respectively
   (a) −3.4 eV and +6.8 eV (b) +6.8 eV and −3.4 eV (c) +3.4 eV and −6.8 eV (d) +3.4 eV and −3.4 eV
5. An electron and a proton have the same de Broglie wavelength. They must have the same
   (a) speed (b) kinetic energy (c) momentum (d) total energy
6. Which set of quantum numbers (n, l, m, s) is NOT allowed?
   (a) 2, 2, 1, +½ (b) 2, 1, 0, +½ (c) 3, 2, −2, −½ (d) 4, 0, 0, −½
7. An electron with n = 3 and l = 1 is in a
   (a) 3s orbital (b) 3d orbital (c) 4p orbital (d) 3p orbital
8. The number of unpaired electrons in Fe³⁺ (Z = 26) is
   (a) 3 (b) 5 (c) 4 (d) 6
9. The electronic configuration of Cu²⁺ (Z = 29) is
   (a) [Ar] 3d⁹ (b) [Ar] 3d⁸ 4s¹ (c) [Ar] 3d¹⁰ (d) [Ar] 3d⁷ 4s²
10. In a many-electron atom, which of these subshells has the highest energy?
   (a) 4s (b) 3d (c) 4p (d) 5s
11. The number of radial nodes in a 4d orbital is
   (a) 0 (b) 2 (c) 1 (d) 3
12. Writing nitrogen as 1s² 2s² 2pₓ² 2pᵧ¹, with 2p_z empty, violates
   (a) the Aufbau principle (b) Hund's rule (c) Pauli's exclusion principle (d) the (n + l) rule
13. Bohr's idea of a fixed circular orbit is rejected today mainly because
   (a) it fixes position and momentum together, which uncertainty forbids (b) electrons have no mass (c) the nucleus is not positively charged (d) hydrogen gives a continuous spectrum
14. Bohr's quantum condition follows from de Broglie's idea if the circumference of an allowed orbit equals
   (a) λ/n (b) nλ/2 (c) 2nλ (d) nλ

::: note Answers and explanations — Set B
**1.** (b) — r ∝ n², so 1² : 2² : 3² = 1 : 4 : 9.
**2.** (d) — E ∝ −1/n², so the levels crowd together: 1→2 is 10.2 eV but 2→3 only 1.89 eV and 3→4 0.66 eV.
**3.** (a) — v = 2.18 × 10⁶ Z/n m s⁻¹: faster for a larger nuclear charge, slower in outer orbits. n²/Z is the radius dependence.
**4.** (c) — KE = −E = +3.4 eV and PE = 2E = −6.8 eV; check KE + PE = −3.4 eV.
**5.** (c) — λ = h/p, so equal wavelengths mean equal momenta. With different masses their speeds and kinetic energies (p²/2m) differ.
**6.** (a) — For n = 2, l can only be 0 or 1. The other sets obey l < n, |m| ≤ l and s = ±½.
**7.** (d) — n = 3 is the third shell and l = 1 is a p subshell: 3p.
**8.** (b) — Fe³⁺ = [Ar] 3d⁵: one electron in each of the five d orbitals.
**9.** (a) — Cu is [Ar] 3d¹⁰ 4s¹; remove the 4s electron, then one 3d electron: [Ar] 3d⁹.
**10.** (d) — n + l: 4s = 4, 3d = 5, 4p = 5, 5s = 5. For equal n + l the higher n has the higher energy, so 5s.
**11.** (c) — Radial nodes = n − l − 1 = 4 − 2 − 1 = 1. The 4d orbital also has 2 angular nodes, 3 nodes in all.
**12.** (b) — The 2p orbitals are degenerate; pairing in 2pₓ while 2p_z is empty breaks Hund's rule. No orbital holds more than two electrons, so Pauli is obeyed.
**13.** (a) — An orbit means an exact radius and an exact speed at the same time, which Heisenberg's principle rules out.
**14.** (d) — 2πr = nλ = nh/mv rearranges to mvr = nh/2π.
:::

**Set C — Application (11 questions)**

1. The wavelength of the line emitted when the electron of a hydrogen atom falls from n = 3 to n = 2 is (R_H = 1.097 × 10⁷ m⁻¹)
   (a) 656 nm (b) 486 nm (c) 122 nm (d) 1875 nm
2. The ratio of the wavelength of the first line of the Lyman series to that of the first line of the Balmer series is
   (a) 27 : 5 (b) 3 : 4 (c) 5 : 27 (d) 4 : 9
3. The energy needed to remove the electron from He⁺ in its ground state is
   (a) 13.6 eV (b) 54.4 eV (c) 27.2 eV (d) 122.4 eV
4. The de Broglie wavelength of an electron moving at 1.0 × 10⁶ m s⁻¹ is (m = 9.1 × 10⁻³¹ kg, h = 6.63 × 10⁻³⁴ J s)
   (a) 7.3 × 10⁻¹² m (b) 1.4 × 10⁻⁹ m (c) 7.3 × 10⁻⁸ m (d) 7.3 × 10⁻¹⁰ m
5. The position of an electron is known to within 1.0 × 10⁻¹⁰ m. The minimum uncertainty in its velocity is (m = 9.1 × 10⁻³¹ kg, h = 6.63 × 10⁻³⁴ J s)
   (a) 7.3 × 10⁶ m s⁻¹ (b) 1.2 × 10⁶ m s⁻¹ (c) 5.8 × 10⁵ m s⁻¹ (d) 5.8 × 10³ m s⁻¹
6. The radius of the second Bohr orbit of He⁺ is (radius of the first orbit of hydrogen = 0.529 Å)
   (a) 1.058 Å (b) 0.529 Å (c) 2.116 Å (d) 0.265 Å
7. Electrons in a sample of hydrogen atoms fall from n = 5 to n = 2 by all possible routes. The number of different spectral lines is
   (a) 3 (b) 6 (c) 10 (d) 4
8. The number of electrons with l = 2 in an atom of iron (Z = 26) is
   (a) 2 (b) 8 (c) 12 (d) 6
9. The wavelength of the series limit of the Balmer series of hydrogen is (R_H = 1.097 × 10⁷ m⁻¹)
   (a) 91.2 nm (b) 656 nm (c) 365 nm (d) 820 nm
10. The energy of a photon of wavelength 663 nm is (h = 6.63 × 10⁻³⁴ J s, c = 3.0 × 10⁸ m s⁻¹)
   (a) 3.0 × 10⁻¹⁸ J (b) 3.0 × 10⁻¹⁹ J (c) 1.5 × 10⁻¹⁹ J (d) 3.0 × 10⁻²⁸ J
11. The ratio of the energy of the electron in the second orbit of hydrogen to that in the third orbit of Li²⁺ is
   (a) 1 : 4 (b) 4 : 1 (c) 1 : 9 (d) 9 : 4

::: note Answers and explanations — Set C
**1.** (a) — 1/λ = R(1/4 − 1/9) = 5R/36, so λ = 36/(5 × 1.097 × 10⁷) = 6.56 × 10⁻⁷ m = 656 nm (Hα). 486 nm is 4 → 2; 122 nm is 2 → 1; 1875 nm is 4 → 3.
**2.** (c) — λ ∝ 1/(1/n₁² − 1/n₂²): Lyman (2 → 1) bracket 3/4, Balmer (3 → 2) bracket 5/36; λ_L : λ_B = (5/36) : (3/4) = 5 : 27.
**3.** (b) — IE = 13.6 Z² = 13.6 × 4 = 54.4 eV. Option (c) multiplies by Z instead of Z²; (d) is Li²⁺ (Z = 3).
**4.** (d) — λ = h/mv = 6.63 × 10⁻³⁴/(9.1 × 10⁻³¹ × 1.0 × 10⁶) = 7.3 × 10⁻¹⁰ m (about 7 Å).
**5.** (c) — Δv = h/(4πmΔx) = 6.63 × 10⁻³⁴/(4π × 9.1 × 10⁻³¹ × 10⁻¹⁰) = 5.8 × 10⁵ m s⁻¹. (a) omits 4π; (b) uses h/2π.
**6.** (a) — r = 0.529 × n²/Z = 0.529 × 4/2 = 1.058 Å. (c) forgets Z (hydrogen's n = 2); (d) is He⁺ n = 1.
**7.** (b) — Δn = 3, lines = Δn(Δn + 1)/2 = 3 × 4/2 = 6 (5→4, 5→3, 5→2, 4→3, 4→2, 3→2). A single atom gives at most 3; 10 lines would need a fall to n = 1.
**8.** (d) — Fe: 1s² 2s² 2p⁶ 3s² 3p⁶ 3d⁶ 4s². l = 2 means d electrons: 6. Option (c) counts the p electrons (l = 1).
**9.** (c) — For n₂ = ∞, 1/λ = R/4, so λ = 4/R = 3.65 × 10⁻⁷ m ≈ 365 nm. 91.2 nm is the Lyman limit and 820 nm the Paschen limit.
**10.** (b) — E = hc/λ = 6.63 × 10⁻³⁴ × 3.0 × 10⁸/(663 × 10⁻⁹) = 3.0 × 10⁻¹⁹ J (≈ 1.9 eV). Option (d) forgets to convert nm to m.
**11.** (a) — E ∝ Z²/n²: hydrogen n = 2 gives 1/4; Li²⁺ n = 3 gives 9/9 = 1. Ratio 1/4 : 1 = 1 : 4 (−3.4 eV against −13.6 eV).
:::
