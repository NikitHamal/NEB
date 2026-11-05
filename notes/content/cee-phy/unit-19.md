---
subject: Physics
grade: CEE
unit: 19
title: Atomic Physics and X-rays
hours: 2
area: Modern Physics
---

Modern Physics carries **12 of the 50 Physics questions** (official MEC weightage),
and we estimate about **2** come from this chapter. They are almost always one
Bohr-model calculation — an orbit radius, an energy, a wavelength or a series
name — and one X-ray fact, usually the Duane–Hunt limit $\lambda_{min} = hc/eV$ or
Bragg's law. Both halves reward a small number of remembered results, and both
punish the two standard confusions: putting the Lyman series in the visible, and
calling the $K_\alpha$ line the shortest wavelength in the X-ray spectrum.

::: key What the paper asks from this chapter
- Bohr's three postulates, and the quantisation condition $mvr = nh/2\pi$.
- The hydrogen results: $r_n \propto n^2$, $v_n \propto 1/n$, $E_n = -13.6/n^2$ eV.
- The five named series, the level each ends on, and the region each lies in.
- Ionisation energy 13.6 eV; first excitation 10.2 eV; the Rydberg formula.
- de Broglie's relation $\lambda = h/p$ and the uncertainty principle, as statements with one consequence.
- X-ray production, the continuous and characteristic spectra, $\lambda_{min} = hc/eV$.
- Bragg's law $2d\sin\theta = n\lambda$ and Moseley's law qualitatively.
:::

## 19.1 Bohr's theory of the hydrogen atom: energy levels and spectral series

### Why the Rutherford atom had to be replaced

Rutherford's experiment (1911) put a tiny positive nucleus at the centre of the
atom, with electrons outside it. That picture has a fatal flaw in classical
physics. An electron moving in a circle is accelerating, and an accelerating
charge radiates energy. So the electron should lose energy continuously, spiral
into the nucleus in about $10^{-11}$ s, and the light it emitted should form a
**continuous** spectrum that changes as the orbit shrinks.

```photo id="phy12/spectroscope" caption="An old brass prism spectroscope: the collimator (with slit) on the right sends a parallel beam to the prism on the central table, and the telescope on the left views the spectrum." width="70"
```


Neither happens. Atoms are stable, and a hydrogen discharge emits a spectrum of
**sharp lines** — a few fixed wavelengths, not a smear. Niels Bohr (1913) kept
the nuclear model and added three postulates that remove both contradictions.

::: definition Bohr's postulates
1. **Stationary states.** An electron can revolve round the nucleus only in
   certain allowed orbits, and while it is in one of them it does **not** radiate,
   even though it is accelerating.
2. **Quantisation of angular momentum.** The allowed orbits are those for which
   the angular momentum is a whole-number multiple of $h/2\pi$:
   $mvr = nh/2\pi$, $n = 1, 2, 3, \dots$
3. **Quantum jumps.** Radiation is emitted or absorbed only when the electron
   moves between two allowed orbits, and one photon carries the whole energy
   difference: $hf = E_2 - E_1$.
:::

The integer $n$ is the **principal quantum number**. The orbit with $n = 1$ is the
**ground state**; $n = 2, 3, \dots$ are **excited states**.

### The radius, speed and energy

The electron of charge $-e$ moves in a circle of radius $r$ round a nucleus of
charge $+e$. The Coulomb attraction supplies the centripetal force.

::: derivation The Bohr radius and the hydrogen energy levels
**Setting up.** Let $m$ be the electron mass, $v$ its speed, $r$ the orbit
radius, and $k = 1/4\pi\varepsilon_0$. Two equations hold: force balance and
angular-momentum quantisation.

**Step 1 — force balance.** The Coulomb force is the centripetal force:
$$ \frac{mv^2}{r} = \frac{ke^2}{r^2} \quad\Longrightarrow\quad mv^2 = \frac{ke^2}{r} $$

**Step 2 — quantisation.** From $mvr = nh/2\pi$, the speed is
$v = nh/(2\pi mr)$.

**Step 3 — substitute.** Squaring the speed and putting it into Step 1:
$$ \frac{m n^2h^2}{4\pi^2m^2r^2} = \frac{ke^2}{r}
\quad\Longrightarrow\quad r_n = \frac{n^2h^2}{4\pi^2 m k e^2} $$

**Step 4 — put in the numbers.** With $h = 6.63\times10^{-34}$ J s,
$m = 9.11\times10^{-31}$ kg, $e = 1.6\times10^{-19}$ C and
$k = 9\times10^9$ N m² C⁻², the bracket is $0.529\times10^{-10}$ m. So
$$ r_n = 0.529\,n^2 \ \text{Å} = a_0n^2 $$
where $a_0 = 0.529$ Å is the **Bohr radius**.

**Step 5 — the speed.** Putting $r_n$ back into $v = nh/(2\pi mr)$ gives
$$ v_n = \frac{e^2}{2\varepsilon_0nh} = \frac{2.19\times10^6}{n}\ \text{m s}^{-1} $$

**Step 6 — the energy.** Kinetic energy $K = \frac{1}{2}mv^2 = ke^2/2r$;
potential energy $U = -ke^2/r$. So $U = -2K$ and
$$ E_n = K + U = -\frac{ke^2}{2r_n} = -\frac{13.6}{n^2}\ \text{eV} $$

**Result.** $r_n \propto n^2$, $v_n \propto 1/n$, $E_n \propto -1/n^2$, with
$E_1 = -13.6$ eV.

**What it means.** The negative sign means the electron is **bound**: 13.6 eV must
be supplied to remove it from the ground state. The energy levels crowd together
as $n$ grows and reach zero at $n = \infty$, where the electron is free.
:::

| Quantity in state $n$ | Depends on $n$ as | Ground-state value |
|---|---|---|
| Radius $r_n$ | $n^2$ | 0.529 Å |
| Speed $v_n$ | $1/n$ | $2.19\times10^6$ m s⁻¹ |
| Kinetic energy $K_n$ | $1/n^2$ | 13.6 eV |
| Potential energy $U_n$ | $-1/n^2$ | −27.2 eV |
| Total energy $E_n$ | $-1/n^2$ | −13.6 eV |
| Angular momentum $L_n$ | $n$ | $h/2\pi$ |
| Time period $T_n$ | $n^3$ | $1.5\times10^{-16}$ s |

Note the useful pair $U = 2E$ and $K = -E$: the potential energy is twice the
total energy, and the kinetic energy is minus the total energy. In the ground
state $K = 13.6$ eV, $U = -27.2$ eV, $E = -13.6$ eV.

::: caution The two energies students mix up
**Ionisation energy** is the energy to take the electron from its present level to
$n = \infty$: 13.6 eV from the ground state, but only 3.4 eV from $n = 2$.
**Excitation energy** is the energy to lift it to the *next* level: 10.2 eV from
$n = 1$ to $n = 2$, and 12.09 eV from $n = 1$ to $n = 3$. An electron in the
ground state cannot absorb a photon of 12 eV — photons are absorbed whole, and
12 eV matches no gap. It can absorb 10.2 eV, 12.09 eV, 12.75 eV, … exactly.
:::

### The spectral series

A downward jump from level $n_2$ to a lower level $n_1$ emits a photon of energy
$13.6(1/n_1^2 - 1/n_2^2)$ eV. In wavelength form this is the **Rydberg formula**:

$$ \frac{1}{\lambda} = R\left(\frac{1}{n_1^2} - \frac{1}{n_2^2}\right),
\qquad R = 1.097\times10^7\ \text{m}^{-1} $$

with $n_2 > n_1$. Each fixed $n_1$ gives a **series**; within a series $n_2$ runs
from $n_1 + 1$ upward, and the lines crowd together towards the **series limit**
at $n_2 = \infty$, where $\lambda_{limit} = 1/(R/n_1^2)$.

| Series | Ends on $n_1$ | Region | First line $\lambda$ | Series limit |
|---|---|---|---|---|
| Lyman | 1 | ultraviolet | 121.6 nm (Ly-α) | 91.2 nm |
| Balmer | 2 | visible (and near UV) | 656.3 nm (Hα, red) | 364.6 nm |
| Paschen | 3 | infrared | 1875 nm | 820 nm |
| Brackett | 4 | infrared | 4050 nm | 1458 nm |
| Pfund | 5 | infrared | 7460 nm | 2279 nm |

The visible hydrogen lines all belong to the **Balmer** series: Hα (656 nm, red),
Hβ (486 nm, blue-green), Hγ (434 nm, violet) and Hδ (410 nm, violet). The series
limit of Balmer, 364.6 nm, is the shortest wavelength the series can reach.

```figure caption="Energy levels of hydrogen, $E_n = -13.6/n^2$ eV, on a compressed vertical scale. Every downward arrow is an emitted photon: Lyman arrows end on $n=1$, Balmer arrows on $n=2$, Paschen on $n=3$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.9,3.4))
E = {1:-13.6, 2:-3.40, 3:-1.51, 4:-0.85, 5:0.0}
POS = {1: 0.0, 2: 1.05, 3: 1.62, 4: 2.00, 5: 2.75}
for n, e in E.items():
    y = POS[n]
    ax.plot([0.10, 0.86], [y, y], color=INK, lw=1.3)
    lab = r'$\infty$' if n == 5 else str(n)
    ax.text(0.075, y, 'n = ' + lab, ha='right', va='center', fontsize=8.6, color=INK)
    ax.text(0.875, y, ('0' if n == 5 else f'{e:.2f}') + ' eV',
            ha='left', va='center', fontsize=8.0, color=MUTED)
def arrow(x, n1, n2, col):
    ax.annotate('', xy=(x, POS[n1] + 0.05), xytext=(x, POS[n2] - 0.05),
                arrowprops=dict(arrowstyle='-|>', color=col, lw=1.6,
                                mutation_scale=10))
arrow(0.18, 1, 2, SERIES[0]); arrow(0.25, 1, 3, SERIES[0])
arrow(0.47, 2, 3, SERIES[2]); arrow(0.54, 2, 4, SERIES[2])
arrow(0.76, 3, 4, SERIES[3])
ax.plot([0.10, 0.14], [-0.30, -0.30], color=SERIES[0], lw=2.2)
ax.text(0.155, -0.30, 'Lyman (UV)', fontsize=8.2, va='center', color=SERIES[0])
ax.plot([0.40, 0.44], [-0.30, -0.30], color=SERIES[2], lw=2.2)
ax.text(0.455, -0.30, 'Balmer (visible)', fontsize=8.2, va='center', color=SERIES[2])
ax.plot([0.70, 0.74], [-0.30, -0.30], color=SERIES[3], lw=2.2)
ax.text(0.755, -0.30, 'Paschen (IR)', fontsize=8.2, va='center', color=SERIES[3])
ax.set_xlim(0.0, 1.0); ax.set_ylim(-0.45, 2.90)
ax.axis('off')
```

::: memory The series in order
**L**yman **B**almer **P**aschen **B**rackett **P**fund — “**L**ittle **B**oys
**P**lay **B**asketball **P**erfectly”. The ending level is the position in the
list: Lyman 1, Balmer 2, Paschen 3, Brackett 4, Pfund 5.
:::

**Number of lines.** An electron falling from level $n$ can take any downward
jump, and each pair of levels gives one line. The number of possible lines is
$$ N = \frac{n(n-1)}{2} $$
so a gas of atoms in the $n = 4$ state can emit 6 different wavelengths.

::: example Worked example 19.1 — the red line of hydrogen
**Problem.** Find the energy and wavelength of the photon emitted when a hydrogen
atom drops from $n = 3$ to $n = 2$.

**Solution.** $E = 13.6(1/2^2 - 1/3^2) = 13.6(1/4 - 1/9) = 1.89$ eV.
Using $1240\ \text{eV nm} = hc$:
$\lambda = 1240/1.89 = 656$ nm — the red Hα line, in the visible.
:::

::: example Worked example 19.2 — ionising an excited atom
**Problem.** A hydrogen atom is in the $n = 2$ state. What is the longest
wavelength that can ionise it?

**Solution.** Ionisation from $n = 2$ needs $0 - (-3.4) = 3.4$ eV. The longest
wavelength corresponds to exactly this energy:
$\lambda = 1240/3.4 = 365$ nm — the Balmer limit, in the near ultraviolet.
Any photon of 365 nm or shorter will do; a longer one cannot.
:::

### Successes and limits of the Bohr model

Bohr's model gets the hydrogen spectrum exactly right, explains why atoms are
stable, predicts the correct ionisation energy, and gives the right size for the
atom. It fails for everything with more than one electron (helium onward), cannot
explain the **relative brightness** of spectral lines, says nothing about **fine
structure** or the splitting of lines in a magnetic field (the Zeeman effect), and
assumes sharp circular orbits that quantum mechanics does not allow. It is a
half-way house: correct energies, wrong picture.

## 19.2 de Broglie waves and the uncertainty principle

### Matter waves

In 1924 Louis de Broglie proposed that if light waves can behave as particles
(photons, Chapter 18), then particles should behave as waves. A particle of
momentum $p = mv$ has a **de Broglie wavelength**

$$ \lambda = \frac{h}{p} = \frac{h}{mv} $$

For a particle of kinetic energy $K$ (non-relativistic), $p = \sqrt{2mK}$, so
$$ \lambda = \frac{h}{\sqrt{2mK}} $$

For an electron accelerated from rest through a potential difference $V$,
$K = eV$ and
$$ \lambda = \frac{h}{\sqrt{2meV}} \approx \sqrt{\frac{150}{V}}\ \text{Å} $$
with $V$ in volts. At 100 V the wavelength is 1.23 Å — about the spacing of atoms
in a crystal, which is why electrons diffract from crystals.

| Object | Speed | de Broglie wavelength |
|---|---|---|
| Electron, 100 V | $5.9\times10^6$ m s⁻¹ | 1.23 Å |
| Electron, 10 kV | $5.9\times10^7$ m s⁻¹ | 0.123 Å |
| Proton, same 100 V | $1.4\times10^5$ m s⁻¹ | $2.9\times10^{-12}$ m |
| Cricket ball, 0.16 kg | 30 m s⁻¹ | $1.4\times10^{-34}$ m |

The last line is the important one. A cricket ball has a wavelength $10^{20}$ times
smaller than a nucleus, so no experiment can detect its wave nature. **Wave
behaviour matters only when $\lambda$ is comparable to the size of the obstacles
or openings in the experiment** — for electrons in crystals, for neutrons in
diffraction experiments, for atoms in interferometers.

The first evidence came from **Davisson and Germer** (1927): a beam of electrons
reflected from a nickel crystal produced a diffraction pattern with maxima at
angles given by Bragg's law, exactly as waves would. Electron microscopes are the
practical application: a 100 kV electron has $\lambda \approx 0.004$ nm, thousands
of times shorter than visible light, so the resolution is thousands of times
better.

**Bohr's orbits explained.** A de Broglie wave going round an orbit must fit a
whole number of wavelengths, otherwise it cancels itself:
$2\pi r = n\lambda = nh/mv$. Rearranged, $mvr = nh/2\pi$ — Bohr's quantisation
condition is just the condition for a **standing wave** round the nucleus.

::: example Worked example 19.3 — electron wavelength
**Problem.** Find the de Broglie wavelength of an electron accelerated through
100 V.

**Solution.** $K = eV = 1.6\times10^{-17}$ J.
$p = \sqrt{2mK} = \sqrt{2(9.11\times10^{-31})(1.6\times10^{-17})}
= 5.4\times10^{-24}$ kg m s⁻¹.
$\lambda = h/p = 6.63\times10^{-34}/5.4\times10^{-24} = 1.2\times10^{-10}$ m
= 1.2 Å. (The shortcut $\sqrt{150/100} = 1.22$ Å gives the same.)
:::

### Heisenberg's uncertainty principle

A wave does not have a sharp position, so a particle described by a matter wave
cannot have both a sharp position and a sharp momentum. Heisenberg (1927) made
this precise:

::: definition Uncertainty principle
$$ \Delta x\,\Delta p \ge \frac{h}{4\pi} = \frac{\hbar}{2} $$
The product of the uncertainties in position and momentum of a particle can never
be smaller than $h/4\pi$. There is a companion relation between energy and time,
$$ \Delta E\,\Delta t \ge \frac{h}{4\pi} $$
:::

Here $\hbar = h/2\pi = 1.055\times10^{-34}$ J s. The principle is not a statement
about clumsy instruments; it is a property of nature. Measuring the position
precisely (small $\Delta x$) forces a large spread of momentum, and vice versa.

**An order-of-magnitude consequence.** Confine an electron to a region the size of
an atom, $\Delta x \approx 10^{-10}$ m. Then
$$ \Delta p \ge \frac{1.055\times10^{-34}}{2\times10^{-10}}
= 5.3\times10^{-25}\ \text{kg m s}^{-1},
\qquad \Delta v \ge \frac{\Delta p}{m_e} \approx 6\times10^5\ \text{m s}^{-1} $$
That is the same order as the electron's orbital speed. So an electron in an atom
cannot be pictured as a particle moving along a definite path; only a
**probability cloud** has meaning. Confine the same electron to a nucleus
($\Delta x \approx 10^{-14}$ m) and the minimum speed becomes
$6\times10^9$ m s⁻¹ — greater than the speed of light. **Electrons cannot exist
inside nuclei**; the electrons emitted in beta decay are created at the moment of
decay.

::: caution What the principle does and does not say
It does **not** say that a particle has a definite position and momentum that we
simply do not know. It says the pair has no simultaneous definite values. It also
does not stop us measuring one of them exactly — only both at once. And $\Delta E
\Delta t \ge \hbar/2$ explains the **natural width** of spectral lines: a state
that lives only $10^{-8}$ s has an energy uncertain by about $10^{-7}$ eV.
:::

## 19.3 X-rays: production, properties and uses; Bragg's law

### The Coolidge tube

X-rays are produced when fast electrons strike a heavy metal target. In a modern
**Coolidge tube**:

- a **tungsten filament** (cathode) is heated by a small current and emits
  electrons by **thermionic emission**;
- a high voltage (typically 20–150 kV) accelerates these electrons towards the
  **anode**, a heavy metal such as tungsten or molybdenum;
- the tube is evacuated, so the electrons travel without colliding with gas;
- more than 99 % of the electron energy becomes **heat** in the anode, which is
  therefore cooled (often a rotating anode spreads the heat).

The **tube current** (filament heating) controls the *number* of electrons, hence
the *intensity* of the X-rays. The **tube voltage** controls the *energy* of each
electron, hence the *penetrating power* (hardness) and the shortest wavelength.

### The two spectra

An X-ray tube emits a **superposition** of two distinct spectra.

**1. Continuous spectrum (bremsstrahlung).** An electron passing close to a
nucleus is decelerated and radiates the lost energy as a photon. The energy lost
can be anything from zero up to the whole kinetic energy $eV$, so the spectrum is
continuous. The most energetic photon occurs when the electron loses *all* its
energy in one collision:

$$ \lambda_{min} = \frac{hc}{eV} $$

This is the **Duane–Hunt limit**. It depends only on the tube voltage, not on the
target metal.

**2. Characteristic spectrum.** If the bombarding electron knocks out an inner
(K-shell) electron, an electron from a higher shell falls down and emits a photon
of fixed energy. These are the sharp **K-series** lines: $K_\alpha$ (from L to K)
and $K_\beta$ (from M to K). Their wavelengths are a fingerprint of the target
element and do **not** change when the tube voltage changes (as long as the
voltage is high enough to remove a K electron at all).

```figure caption="X-ray spectrum of a molybdenum target at two tube voltages. The continuous background is bremsstrahlung and cuts off at $\lambda_{min} = hc/eV$, which moves left as the voltage rises. The $K_\alpha$ and $K_\beta$ peaks stay at the same wavelengths: they are properties of molybdenum."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.9,3.0))
lam = np.linspace(0.02, 0.14, 2000)
def cont(l, lmin, amp):
    x = np.clip(l/lmin - 1, 0, None)
    return amp * x**1.2 * np.exp(-x/0.55)
def peak(l, c, w, h):
    return h*np.exp(-((l-c)/w)**2)
for lmin, amp, col, lab in [(0.0496, 1.05, MUTED, '25 kV'),
                            (0.0354, 1.45, ACCENT, '35 kV')]:
    y = cont(lam, lmin, amp) + peak(lam, 0.0630, 0.0008, 0.26) + peak(lam, 0.0710, 0.0009, 0.42)
    ax.plot(lam, y, color=col, lw=1.8, label=lab)
    ax.plot([lmin, lmin], [0, 1.50 if lmin < 0.04 else 1.22], color=col, lw=0.9, ls=':')
ax.text(0.0365, 1.53, r'$\lambda_{min}=0.035$ nm', fontsize=8.0, color=ACCENT)
ax.text(0.0505, 1.25, r'$\lambda_{min}=0.050$ nm', fontsize=8.0, color=MUTED)
ax.text(0.0585, 0.60, r'$K_\beta$', fontsize=8.8, color=INK, ha='right', va='bottom')
ax.text(0.0735, 0.72, r'$K_\alpha$', fontsize=8.8, color=INK, ha='left', va='bottom')
ax.set_xlabel('wavelength  $\\lambda$  (nm)'); ax.set_ylabel('intensity')
ax.set_xlim(0.02, 0.14); ax.set_ylim(0, 1.72)
ax.set_yticks([])
ax.spines[['top','right']].set_visible(False)
ax.legend(loc='upper right', fontsize=8.2)
ax.grid(True, axis='x', alpha=.5)
```

::: caution The $K_\alpha$ trap
The $K_\alpha$ line is **not** the shortest wavelength in the spectrum. The
continuous cut-off $\lambda_{min}$ is always shorter, because it comes from an
electron losing *all* its energy at once, while $K_\alpha$ comes from a
transition with a fixed, smaller energy. In the figure the cut-off is at 0.035 nm
and $K_\alpha$ at 0.071 nm.
:::

### Properties of X-rays

| Property | Consequence |
|---|---|
| Electromagnetic waves, wavelength about 0.01–10 nm | travel at $c$, obey reflection, refraction, diffraction, polarisation |
| No charge | **not deflected** by electric or magnetic fields (unlike cathode rays) |
| High photon energy | ionise gases, blacken photographic film, cause fluorescence |
| Penetrate matter | absorbed more by dense, high-$Z$ material (bone, lead) than by flesh |
| Produced by electron bombardment | originate in the electron cloud, not the nucleus |
| Harmful to living tissue | ionisation damages DNA; shielding and dose limits needed |

**Soft X-rays** have long wavelength and low penetrating power; **hard X-rays**
have short wavelength and high penetrating power. Raising the tube voltage makes
the beam harder.

### Uses

- **Diagnosis:** radiographs of bone and teeth, mammography, CT scans, angiography.
  Absorption depends on density and atomic number, so bone ($Z$ high) shows white
  against soft tissue.
- **Therapy:** high-energy X-rays destroy cancer cells; the beam is aimed from
  several directions so the tumour receives a high dose and healthy tissue less.
- **Industry:** checking welds and castings for internal cracks, scanning luggage.
- **Science:** X-ray crystallography (Bragg), identifying elements by their
  characteristic lines (Moseley), X-ray fluorescence analysis.

### Bragg's law

Crystals have layers of atoms separated by a distance $d$ comparable to the X-ray
wavelength. X-rays scattered from successive layers interfere. The ray from the
second layer travels an extra distance $2d\sin\theta$, where $\theta$ is measured
**from the planes**, not from the normal.

::: definition Bragg's law
$$ 2d\sin\theta = n\lambda $$
where $d$ is the spacing between the reflecting planes, $\theta$ the glancing
angle between the ray and the plane, and $n = 1, 2, 3, \dots$ the order of
reflection.
:::

```figure caption="Bragg reflection from two neighbouring planes. The lower ray travels an extra distance $d\sin\theta$ on the way in and the same on the way out, so the path difference is $2d\sin\theta$."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,3.0))
for y in (0.35, 0.55):
    ax.plot([0.06, 0.94], [y, y], color=INK, lw=1.3)
    for x in np.arange(0.10, 0.95, 0.07):
        ax.plot(x, y, 'o', ms=2.6, color=INK)
A = (0.40, 0.55); B = (0.40, 0.35); D = (0.313, 0.40)
ax.annotate('', xy=A, xytext=(0.10, 0.723),
            arrowprops=dict(arrowstyle='-|>', color=SERIES[0], lw=1.5, mutation_scale=9))
ax.annotate('', xy=(0.70, 0.723), xytext=(0.405, 0.553),
            arrowprops=dict(arrowstyle='-|>', color=SERIES[0], lw=1.5, mutation_scale=9))
ax.annotate('', xy=B, xytext=(0.10, 0.523),
            arrowprops=dict(arrowstyle='-|>', color=SERIES[1], lw=1.5, mutation_scale=9))
ax.annotate('', xy=(0.70, 0.523), xytext=(0.405, 0.353),
            arrowprops=dict(arrowstyle='-|>', color=SERIES[1], lw=1.5, mutation_scale=9))
ax.plot([D[0], B[0]], [D[1], B[1]], color='#8c2f28', lw=2.8, solid_capstyle='round')
ax.plot([A[0], B[0]], [A[1], B[1]], color=MUTED, lw=0.9, ls=':')
ax.annotate('', xy=(0.40, 0.535), xytext=(0.40, 0.365),
            arrowprops=dict(arrowstyle='<|-|>', color=MUTED, lw=0.8, mutation_scale=7))
ax.text(0.415, 0.45, r'$d$', fontsize=9.4, color=MUTED, va='center')
ax.add_patch(matplotlib.patches.Arc(B, 0.20, 0.20, theta1=150, theta2=180,
                                    color=INK, lw=0.9))
ax.text(0.283, 0.362, r'$\theta$', fontsize=9.2, color=INK, ha='right', va='bottom')
ax.text(0.365, 0.575, r'$A$', fontsize=8.8, color=INK, ha='right')
ax.text(0.365, 0.325, r'$B$', fontsize=8.8, color=INK, ha='right')
ax.text(0.335, 0.408, r'$d\sin\theta$', fontsize=8.4, color='#8c2f28',
        ha='center', va='bottom')
ax.text(0.115, 0.760, 'incident', fontsize=8.2, color=INK, ha='left')
ax.text(0.700, 0.760, 'reflected', fontsize=8.2, color=INK, ha='left')
ax.set_xlim(0, 0.98); ax.set_ylim(0.24, 0.82)
ax.axis('off')
```

::: example Worked example 19.4 — a crystal spacing
**Problem.** X-rays of wavelength 0.154 nm are reflected from a crystal whose
plane spacing is 0.282 nm. Find the glancing angle for the first-order maximum.

**Solution.** $n = 1$: $\sin\theta = \lambda/(2d) = 0.154/(2\times0.282) = 0.273$.
$\theta = \sin^{-1}(0.273) = 15.8^{\circ}$.
:::

::: example Worked example 19.5 — the Duane–Hunt limit
**Problem.** An X-ray tube runs at 40 kV. Find the shortest wavelength emitted,
and state what happens to it if the voltage is doubled.

**Solution.** $\lambda_{min} = hc/eV = 1240\ \text{eV nm}/(4.0\times10^4\ \text{eV})
= 0.031$ nm. Doubling the voltage doubles $eV$, so $\lambda_{min}$ **halves** to
0.0155 nm. The target metal does not enter the calculation.
:::

### Moseley's law

Moseley (1913) measured the $K_\alpha$ frequencies of many elements and found
$$ \sqrt{f} = a(Z - b) $$
where $Z$ is the atomic number, $a$ is a constant and $b \approx 1$ for the K
series. The frequency of the characteristic line therefore rises steadily with
atomic number — the line is a fingerprint of the element. This is how Moseley
established that **atomic number, not atomic mass, is the real ordering number of
the elements**, and it is the basis of X-ray fluorescence identification. You are
not expected to use the equation numerically, only to know that $\sqrt{f}$ is
linear in $Z$ and that the line is characteristic of the element.

```photogrid label="19.1" cols="2" ratio="1.2" caption="Short-wavelength limit and characteristic lines. (a) Roentgen's plate shows bones and a ring because X-rays are absorbed more by dense matter. (b) Electrons accelerated through V can give one photon at most eV, so the continuous spectrum stops at lambda_min = hc / eV: 0.0413 nm at 30 kV and 0.0620 nm at 20 kV. The curves use Kramers' shape (lambda / lambda_min - 1) / lambda^2. The K-alpha line of copper from Moseley's law, E = 13.6 (3/4) (Z - 1)^2 eV with Z = 29, is 8.00 keV at 0.155 nm, independent of tube voltage."
@ photo id="ceephy/xray" cap="One of the first X-ray photographs, a hand with a ring, made by Roentgen in 1895"
fit 1.2
focus 0.5 0.5
@ svg cap="Continuous X-ray spectrum and the copper K-alpha line"
hc = 1239.84
lmin = lambda kV: hc / (kV * 1e3) 
l30, l20 = lmin(30), lmin(20)
Ek = 13.6 * 0.75 * (29 - 1) ** 2; lk = hc / Ek
assert abs(l30 - 0.04133) < 1e-4 and abs(l20 - 0.0620) < 1e-4 and abs(lk - 0.155) < 1e-3
I = lambda l, lm: (l / lm - 1) / l ** 2 if l > lm else 0.0
Imax = I(2 * l30, l30)
facts = dict(l30="%.4f" % l30, l20="%.4f" % l20, ek="%.2f" % (Ek / 1000), lk="%.3f" % lk)
f = Fig(300, 244)
f.text(150, 14, "intensity against wavelength (nm)", size=10.5, color=NAVY, bold=True)
X = lambda l: 30 + l * 1250; Y = lambda i: 150 - i / Imax * 105
f.line(X(0), Y(0), 285, Y(0), color=SLATE, sw=1.4); f.line(X(0), Y(0), X(0), 34, color=SOFT, sw=1.2)
for lm, col in ((l30, NAVY), (l20, TEAL)):
    pts = [(X(k / 1000), Y(I(k / 1000, lm))) for k in range(int(lm * 1000) + 1, 205, 3)]
    for (a, b), (c, d) in zip(pts, pts[1:]): f.line(a, b, c, d, color=col, sw=2.4)
f.line(X(lk), Y(0), X(lk), Y(0.25 * Imax), color=RED, sw=2.4)
f.text(X(lk) + 5, Y(0.25 * Imax) + 6, "Cu K-a", size=10.5, color=RED, bold=True, anchor="start")
f.text(X(0.1), Y(Imax) - 8, "30 kV", size=10.5, color=NAVY, bold=True)
f.text(X(0.1), Y(I(0.1, l20)) + 16, "20 kV", size=10.5, color=TEAL, bold=True)
for q in (0, 0.05, 0.1, 0.15, 0.2): f.text(X(q), Y(0) + 13, "%g" % q, size=10.5, color=SLATE)
f.text(150, 184, "lambda_min = %.4f nm (30 kV)" % l30, size=10.5, color=NAVY, bold=True)
f.text(150, 202, "lambda_min = %.4f nm (20 kV)" % l20, size=10.5, color=TEAL, bold=True)
f.text(150, 220, "Cu K-alpha %.2f keV = %.3f nm" % (Ek / 1000, lk), size=10.5, color=RED, bold=True)
```

```photogrid label="19.2" cols="2" ratio="1.2" caption="Counting reflections from crystal planes. (a) An X-ray diffractometer rotates a crystal and a detector to find the angles at which the X-rays reflect strongly. (b) Bragg's law, 2 d sin(theta) = n lambda, is applied to the (100) planes of rock salt, spaced 282 pm apart, with copper K-alpha X-rays of wavelength 154 pm. The first-order reflection appears at 15.8 degrees, the second at 33.1 degrees and the third at 55.0 degrees; a fourth is impossible, since it would need a sine larger than 1. Only 3 orders are therefore seen, and with the shorter wavelength of molybdenum radiation 7 orders appear. Measuring these angles gives the spacing d of the planes in an unknown crystal."
@ photo id="ceephy3/xrd" cap="An X-ray diffractometer"
fit 1.2
focus 0.5 0.5
@ svg cap="Bragg reflection from a sodium chloride crystal"
import math
d, lam = 282.0, 154.0
rows = []
for n in (1, 2, 3):
    rows.append(("n = %d" % n, math.degrees(math.asin(n * lam / (2 * d)))))
assert round(rows[0][1], 1) == 15.8 and round(rows[1][1], 1) == 33.1 and round(rows[2][1], 1) == 55.0
nmax = int(2 * d / lam)
nmo = int(2 * d / 71.0)
f = Fig(300, 236)
f.text(150, 12, "Bragg angle, degrees, 2 d sin(t) = n lambda", size=10.5, color=NAVY, bold=True)
hbars(f, rows, vmax=60, fmt="%.1f", x0=52, y0=30, bw=170, gap=30,
      colors=[(BLUE, NAVY), (MINT, TEAL), (SAND, AMBER)])
f.text(150, 130, "NaCl planes d = 282 pm, Cu K-alpha 154 pm", size=10, color=SLATE, bold=True)
f.text(150, 152, "n = 4 would need sin(t) = %.2f (> 1)" % (4 * lam / (2 * d)), size=10.5, color=RED, bold=True)
f.text(150, 176, "highest order: n = 2d / lambda = %.2f" % (2 * d / lam), size=10.5, color=NAVY, bold=True)
f.text(150, 194, "so %d orders are seen with Cu light" % nmax, size=10.5, color=NAVY, bold=True)
f.text(150, 214, "Mo K-alpha (71 pm) gives %d orders" % nmo, size=10, color=SLATE, bold=True)
facts = dict(a1=rows[0][1], a2=rows[1][1], a3=rows[2][1], nmax=nmax, nmo=nmo)
```

## Formula and fact sheet

| Quantity | Formula or value |
|---|---|
| Angular momentum | $mvr = nh/2\pi$, $n = 1, 2, 3, \dots$ |
| Bohr radius | $r_n = 0.529\,n^2$ Å; $a_0 = 0.529$ Å |
| Speed | $v_n = 2.19\times10^6/n$ m s⁻¹ $= c/(137n)$ |
| Energy | $E_n = -13.6/n^2$ eV $= -2.18\times10^{-18}/n^2$ J |
| Energy relations | $K = -E$, $U = 2E$, $U = -2K$ |
| Ionisation energy | 13.6 eV from $n=1$; $13.6/n^2$ eV from level $n$ |
| Excitation | 10.2 eV (1→2), 12.09 eV (1→3), 12.75 eV (1→4) |
| Rydberg | $1/\lambda = R(1/n_1^2 - 1/n_2^2)$, $R = 1.097\times10^7$ m⁻¹ |
| Photon energy shortcut | $E = 1240/\lambda$ with $E$ in eV, $\lambda$ in nm |
| Lines from level $n$ | $n(n-1)/2$ |
| Series | Lyman 1 (UV), Balmer 2 (visible), Paschen 3, Brackett 4, Pfund 5 (IR) |
| Balmer lines | Hα 656 nm, Hβ 486 nm, Hγ 434 nm, Hδ 410 nm; limit 365 nm |
| Lyman limit | 91.2 nm |
| de Broglie | $\lambda = h/p = h/mv = h/\sqrt{2mK}$ |
| Electron through $V$ | $\lambda \approx \sqrt{150/V}$ Å |
| Uncertainty | $\Delta x\Delta p \ge h/4\pi$; $\Delta E\Delta t \ge h/4\pi$ |
| X-ray cut-off | $\lambda_{min} = hc/eV = 1240/V$ nm with $V$ in volts |
| Bragg | $2d\sin\theta = n\lambda$ ($\theta$ from the planes) |
| Moseley | $\sqrt{f} = a(Z - b)$, $b \approx 1$ for K series |
| X-ray range | about 0.01–10 nm; $c$; undeflected by fields |

## Chapter summary

- Bohr kept the nuclear atom and added stationary states, $mvr = nh/2\pi$, and
  photon emission on a jump, $hf = E_2 - E_1$.
- For hydrogen $r_n = 0.529n^2$ Å, $v_n = 2.19\times10^6/n$ m s⁻¹ and
  $E_n = -13.6/n^2$ eV; the ground state is bound by 13.6 eV.
- A downward jump $n_2 \to n_1$ emits
  $1/\lambda = R(1/n_1^2 - 1/n_2^2)$; each $n_1$ names a series.
- Lyman ends on $n = 1$ and is ultraviolet; Balmer ends on $n = 2$ and is the only
  visible series; Paschen, Brackett and Pfund are infrared.
- The number of lines from level $n$ is $n(n-1)/2$; lines crowd to a series limit.
- de Broglie: $\lambda = h/p$; an electron at 100 V has $\lambda \approx 1.2$ Å,
  small enough to diffract from crystals, which is the evidence for matter waves.
- $\Delta x\Delta p \ge h/4\pi$: confinement increases momentum spread, which is
  why electrons cannot live in nuclei and why atomic orbits are not sharp paths.
- X-rays come from a Coolidge tube: thermionic electrons accelerated onto a heavy
  target; over 99 % of the energy becomes heat.
- The continuous spectrum is bremsstrahlung and cuts off at
  $\lambda_{min} = hc/eV$; the characteristic lines are inner-shell transitions and
  do not move with voltage. $K_\alpha$ is never the shortest wavelength.
- Bragg's law $2d\sin\theta = n\lambda$ measures crystal spacings; Moseley's
  $\sqrt{f} = a(Z-b)$ makes the characteristic line an element fingerprint.

## Practice questions

**Set A — Recall (23 questions)**

1. Bohr's quantisation condition for the allowed orbits of the hydrogen atom is
   (a) $mvr = nh$ (b) $mvr = nh/2\pi$ (c) $mvr = n\hbar/2$ (d) $mvr^2 = nh/2\pi$
2. The radius of the $n$th Bohr orbit of hydrogen is proportional to
   (a) $n$ (b) $1/n$ (c) $n^2$ (d) $1/n^2$
3. The energy of the hydrogen atom in the state with principal quantum number $n$ is
   (a) $-13.6/n^2$ eV (b) $-13.6n^2$ eV (c) $-13.6/n$ eV (d) $13.6/n^2$ eV
4. The ionisation energy of a hydrogen atom in its ground state is
   (a) 3.4 eV (b) 10.2 eV (c) 27.2 eV (d) 13.6 eV
5. The first excitation energy of hydrogen is
   (a) 3.4 eV (b) 10.2 eV (c) 12.09 eV (d) 13.6 eV
6. The Lyman series of hydrogen lies in the
   (a) visible region (b) infrared region (c) ultraviolet region (d) microwave region
7. The Balmer series of hydrogen ends on the level
   (a) $n = 2$ (b) $n = 1$ (c) $n = 3$ (d) $n = 4$
8. The series of hydrogen that ends on $n = 3$ is the
   (a) Lyman series (b) Balmer series (c) Paschen series (d) Brackett series
9. The series limit of the Balmer series is about
   (a) 91.2 nm (b) 121.6 nm (c) 656 nm (d) 365 nm
10. The value of the Rydberg constant is about
   (a) $1.097\times10^7$ m⁻¹ (b) $1.097\times10^5$ m⁻¹ (c) $6.63\times10^{-34}$ m⁻¹ (d) $3.29\times10^{15}$ m⁻¹
11. The angular momentum of the electron in the ground state of hydrogen is
   (a) zero (b) $h/2\pi$ (c) $h$ (d) $2h/\pi$
12. The de Broglie wavelength of a particle of mass $m$ and speed $v$ is
   (a) $hv$ (b) $mv/h$ (c) $h/(mv^2)$ (d) $h/mv$
13. For an electron accelerated through a potential difference $V$, the de Broglie wavelength is proportional to
   (a) $V$ (b) $1/V$ (c) $1/\sqrt{V}$ (d) $\sqrt{V}$
14. The uncertainty principle states that
   (a) position and momentum can both be measured exactly (b) $\Delta x\Delta p \ge h/4\pi$ (c) energy is always uncertain (d) $\Delta x\Delta p \le h/4\pi$
15. In a Coolidge X-ray tube, electrons are produced by
   (a) thermionic emission (b) photoelectric emission (c) field emission (d) secondary emission
16. The continuous X-ray spectrum is produced by
   (a) transitions between inner shells (b) the nucleus breaking up (c) ionisation of the target atoms (d) deceleration of electrons in the target
17. Characteristic X-rays are produced when
   (a) electrons are decelerated by nuclei (b) outer electrons are removed (c) an inner-shell vacancy is filled (d) the target is heated
18. The shortest wavelength in an X-ray spectrum depends on
   (a) the tube voltage only (b) the target material only (c) both voltage and target (d) the filament current
19. X-rays are not deflected by an electric or magnetic field because they
   (a) travel at the speed of light (b) are uncharged (c) have very short wavelength (d) have high energy
20. Bragg's law for X-ray diffraction is
   (a) $d\sin\theta = n\lambda$ (b) $2d\cos\theta = n\lambda$ (c) $d\cos\theta = n\lambda$ (d) $2d\sin\theta = n\lambda$
21. Moseley's law relates the frequency of a characteristic X-ray line to
   (a) the atomic mass (b) the tube voltage (c) the atomic number (d) the tube current
22. The penetrating power of an X-ray beam is increased by
   (a) increasing the filament current (b) increasing the tube voltage (c) using a thicker target (d) cooling the anode
23. The energy of a photon of wavelength 620 nm is about
   (a) 2.0 eV (b) 1.0 eV (c) 3.1 eV (d) 4.0 eV

::: note Answers and explanations — Set A
**1.** (b) — the allowed angular momenta are $h/2\pi$, $2h/2\pi$, … so $mvr = nh/2\pi$. Option (a) misses the $2\pi$.
**2.** (c) — $r_n = 0.529n^2$ Å, so the radius grows as the square of the quantum number.
**3.** (a) — $E_n = -13.6/n^2$ eV; the negative sign shows the electron is bound.
**4.** (d) — removing the electron from $n=1$ to $n=\infty$ takes $0-(-13.6) = 13.6$ eV.
**5.** (b) — the gap from $n=1$ to $n=2$ is $13.6(1-1/4) = 10.2$ eV. The 3.4 eV in (a) is the ionisation energy from $n=2$.
**6.** (c) — every Lyman line ends on $n=1$, and the largest gaps give the shortest wavelengths, in the ultraviolet.
**7.** (a) — Balmer lines are jumps from higher levels down to $n=2$; that is why the visible hydrogen lines are Balmer lines.
**8.** (c) — Paschen lines end on $n=3$ and lie in the infrared.
**9.** (d) — the limit is the jump $\infty \to 2$: $1240/3.4 = 365$ nm. The 656 nm in (c) is Hα, the first line, not the limit.
**10.** (a) — $R = 1.097\times10^7$ m⁻¹; (d) is $cR$, a frequency.
**11.** (b) — $n=1$ gives $L = h/2\pi$, not zero.
**12.** (d) — $\lambda = h/p = h/mv$; (b) is the inverse, which would have units of m⁻¹ s.
**13.** (c) — $K = eV$ and $\lambda = h/\sqrt{2mK}$, so $\lambda \propto 1/\sqrt{V}$.
**14.** (b) — the product of the two uncertainties cannot be less than $h/4\pi$.
**15.** (a) — the tungsten filament is heated and electrons boil off it (thermionic emission).
**16.** (d) — bremsstrahlung: electrons lose any fraction of their energy on passing near a nucleus.
**17.** (c) — an inner-shell electron is knocked out, a higher electron falls in, and the fixed energy gap gives a sharp line.
**18.** (a) — $\lambda_{min} = hc/eV$ contains only the voltage; the target sets the characteristic lines.
**19.** (b) — X-rays are photons, with no charge, so the Lorentz force on them is zero.
**20.** (d) — the extra path is $2d\sin\theta$, measured from the planes.
**21.** (c) — $\sqrt{f} = a(Z-b)$; the line frequency tracks atomic number.
**22.** (b) — a higher voltage gives each electron more energy, so shorter wavelengths and a harder beam. Filament current changes intensity, not hardness.
**23.** (a) — $E = 1240/620 = 2.0$ eV.
:::

**Set B — Understanding (14 questions)**

1. According to classical electromagnetism, the electron in Rutherford's atom should
   (a) stay in a fixed orbit forever (b) move in a straight line (c) radiate continuously and spiral into the nucleus (d) emit only certain fixed wavelengths
2. In the Balmer series, which transition emits the longest wavelength?
   (a) $3 \to 2$ (b) $4 \to 2$ (c) $5 \to 2$ (d) $\infty \to 2$
3. The ratio of the energy of the $n=2$ state to that of the $n=1$ state of hydrogen is
   (a) $1/2$ (b) $2$ (c) $4$ (d) $1/4$
4. When the principal quantum number of a hydrogen atom is doubled, its radius and speed become
   (a) $2r$, $2v$ (b) $4r$, $v/2$ (c) $2r$, $v/2$ (d) $4r$, $2v$
5. A hydrogen atom is in the $n=4$ state. The number of different wavelengths it can emit while returning to the ground state is
   (a) 3 (b) 4 (c) 6 (d) 10
6. A hydrogen atom in the ground state absorbs a photon of energy 10.2 eV. The atom
   (a) moves to $n=2$ (b) is ionised (c) moves to $n=3$ (d) is unchanged
7. A hydrogen atom in the ground state is offered a photon of energy 11.0 eV. The atom
   (a) is ionised, and the electron leaves with 11.0 eV (b) moves to $n=2$ (c) is ionised, and the electron leaves with 0.6 eV (d) is unchanged
8. An electron and a proton have the same speed. The de Broglie wavelength of the electron is
   (a) shorter than that of the proton (b) longer than that of the proton (c) equal to that of the proton (d) zero
9. The uncertainty principle implies that an electron cannot be confined inside a nucleus because
   (a) the nucleus is positively charged (b) the electron would be attracted to the protons (c) the momentum uncertainty would demand a speed above $c$ (d) a nucleus is too small to contain any particle
10. If the voltage across an X-ray tube is doubled, the cut-off wavelength
   (a) halves (b) doubles (c) stays the same (d) becomes four times
11. Compared with the $K_\alpha$ line, the $K_\beta$ line has
   (a) a longer wavelength and lower energy (b) the same wavelength (c) a longer wavelength but higher energy (d) a shorter wavelength and higher energy
12. The filament current of an X-ray tube is increased while the voltage is kept fixed. The result is
   (a) a shorter $\lambda_{min}$ (b) a longer $\lambda_{min}$ (c) more intense X-rays at the same wavelengths (d) a change in the characteristic wavelengths
13. In Bragg reflection, if the glancing angle is increased from the first-order to the second-order maximum, then $\sin\theta$ becomes
   (a) half as large (b) twice as large (c) the same (d) four times as large
14. The target of an X-ray tube is made of a heavy metal because a heavy target
   (a) gives a higher X-ray yield (b) produces a higher voltage (c) is easier to cool (d) emits only characteristic lines

::: note Answers and explanations — Set B
**1.** (c) — an accelerating charge radiates; the electron would lose energy and spiral in within about $10^{-11}$ s, so atoms could not exist.
**2.** (a) — the smallest energy gap in a series gives the longest wavelength. $3\to2$ is the smallest gap in Balmer; $\infty\to2$ gives the series limit, the shortest wavelength.
**3.** (d) — $E_2 = -13.6/4 = -3.4$ eV and $E_1 = -13.6$ eV, so $E_2/E_1 = 1/4$. Both are negative; the ratio is not 4.
**4.** (b) — $r \propto n^2$ so the radius is four times; $v \propto 1/n$ so the speed is halved.
**5.** (c) — $n(n-1)/2 = 4\times3/2 = 6$: the jumps 4→1, 4→2, 4→3, 3→1, 3→2, 2→1.
**6.** (a) — 10.2 eV is exactly $E_2 - E_1$, so the atom is excited to $n=2$ and the photon is absorbed completely.
**7.** (d) — a photon is absorbed only if its energy equals a gap exactly. 11.0 eV is above the 10.2 eV gap but below 13.6 eV and matches no gap, so it passes by and the atom is unchanged.
**8.** (b) — $\lambda = h/mv$; at the same speed the lighter electron has the longer wavelength.
**9.** (c) — confining an electron to $10^{-14}$ m forces $\Delta v \sim 6\times10^9$ m s⁻¹, greater than $c$, which is impossible.
**10.** (a) — $\lambda_{min} = hc/eV$, so doubling $V$ halves $\lambda_{min}$.
**11.** (d) — $K_\beta$ falls from the M shell, a bigger energy gap than from L, so its photon has more energy and a shorter wavelength.
**12.** (c) — filament current sets the number of electrons, hence intensity; the wavelengths (including $\lambda_{min}$) are set by the voltage and the target.
**13.** (b) — $2d\sin\theta = n\lambda$ with fixed $d$ and $\lambda$ gives $\sin\theta \propto n$, so it doubles.
**14.** (a) — a high-$Z$ target stops the electrons in a short distance and converts a larger fraction of their energy into X-rays, so the yield is higher.
:::

**Set C — Application (9 questions)**

1. The wavelength of the photon emitted in the transition $n=3 \to n=2$ of hydrogen is about
   (a) 122 nm (b) 486 nm (c) 656 nm (d) 820 nm
2. The energy needed to excite a hydrogen atom from $n=2$ to $n=3$ is about
   (a) 1.9 eV (b) 3.4 eV (c) 10.2 eV (d) 13.6 eV
3. The radius of the $n=2$ orbit of hydrogen is
   (a) 0.53 Å (b) 1.06 Å (c) 4.24 Å (d) 2.12 Å
4. The speed of the electron in the $n=2$ orbit of hydrogen is about
   (a) $2.2\times10^6$ m s⁻¹ (b) $1.1\times10^6$ m s⁻¹ (c) $4.4\times10^6$ m s⁻¹ (d) $5.5\times10^5$ m s⁻¹
5. An X-ray tube operates at 30 kV. The shortest wavelength it emits is about
   (a) 0.041 nm (b) 0.41 nm (c) 0.0041 nm (d) 4.1 nm
6. X-rays of wavelength 0.10 nm are diffracted by crystal planes of spacing 0.20 nm. The first-order glancing angle is
   (a) 30° (b) 45° (c) 60° (d) 14.5°
7. The de Broglie wavelength of an electron accelerated through 400 V is about
   (a) 1.2 Å (b) 0.61 Å (c) 2.4 Å (d) 4.9 Å
8. The ionisation energy of a hydrogen atom in the $n=2$ state is
   (a) 6.8 eV (b) 10.2 eV (c) 3.4 eV (d) 13.6 eV
9. A photon of wavelength 0.10 nm strikes a stationary electron. The momentum of the photon is
   (a) $6.6\times10^{-25}$ kg m s⁻¹ (b) $6.6\times10^{-24}$ kg m s⁻¹ (c) $2.0\times10^{-24}$ kg m s⁻¹ (d) $3.3\times10^{-24}$ kg m s⁻¹

::: note Answers and explanations — Set C
**1.** (c) — $E = 13.6(1/4-1/9) = 1.89$ eV; $\lambda = 1240/1.89 = 656$ nm (Hα). 122 nm is Lyman-α and 486 nm is Hβ ($4\to2$).
**2.** (a) — $13.6(1/4-1/9) = 1.89$ eV. This equals the photon energy of the $3\to2$ line, as it must.
**3.** (d) — $r_2 = 0.529\times2^2 = 2.12$ Å.
**4.** (b) — $v_2 = 2.19\times10^6/2 = 1.1\times10^6$ m s⁻¹.
**5.** (a) — $\lambda_{min} = 1240/30000 = 0.0413$ nm.
**6.** (d) — $\sin\theta = 0.10/(2\times0.20) = 0.25$, so $\theta = 14.5^{\circ}$. The glancing angle is measured from the planes, not from the normal.
**7.** (b) — $\lambda = \sqrt{150/400} = \sqrt{0.375} = 0.61$ Å.
**8.** (c) — from $n=2$ the electron needs $0-(-3.4) = 3.4$ eV; 13.6 eV is from the ground state.
**9.** (b) — $p = h/\lambda = 6.63\times10^{-34}/1.0\times10^{-10} = 6.6\times10^{-24}$ kg m s⁻¹.
:::
