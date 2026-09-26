---
subject: Physics
grade: 12
unit: 21
title: Photons
hours: 3
area: Modern Physics
---

Interference and diffraction proved that light is a wave. Then, in 1887, Hertz
noticed that ultraviolet light makes a spark jump more easily — light was
knocking electrons out of metal. Nothing about that emission fitted wave theory.
Einstein's answer in 1905 was to say that light is delivered in indivisible
packets of energy called **photons**, and that a single photon, not a whole wave,
ejects a single electron. This unit is that argument and the experiment that
settles it.

::: key The one equation
$$ hf = \phi_0 + K_{max} $$
Everything in this unit — threshold frequency, stopping potential, the straight
line whose slope measures Planck's constant — is this equation read in a
different way. Learn it first, then learn what each symbol is measured by.
:::

## 21.1 Quantum nature of radiation

Classical physics treats a light beam as a continuous wave whose energy spreads
smoothly over the wavefront. Planck (1900), trying to explain the spectrum of a
hot body, was forced to assume the opposite: that an oscillator of frequency $f$
can only gain or lose energy in whole lumps of size $hf$. Einstein went further
and said the lumps are real, and travel through space as particles of light.

::: definition Photon
A photon is a quantum of electromagnetic radiation: a packet carrying energy
$E = hf = hc/\lambda$ that is emitted, travels and is absorbed as a single
indivisible unit. Here $h = 6.63\times10^{-34}\ \text{J s}$ is Planck's constant.
:::

Properties of a photon, as the NEB expects them listed:

- Energy $E = hf = hc/\lambda$; momentum $p = E/c = h/\lambda$.
- Rest mass **zero**; it travels at $c = 3\times10^{8}\ \text{m s}^{-1}$ in vacuum
  and cannot exist at rest. Its effective mass is $E/c^{2} = hf/c^{2}$.
- Electrically neutral, so unaffected by electric and magnetic fields.
- Energy does not change with the brightness of the beam; **intensity** means the
  *number* of photons crossing unit area per second, not the size of each one.
- In a collision with an electron, total energy and total momentum are conserved.

A useful shortcut: since $hc = 1.99\times10^{-25}\ \text{J m}$, the photon energy
in electron-volts is

$$ E\ (\text{eV}) \approx \frac{1242}{\lambda\ (\text{nm})} \approx \frac{1240}{\lambda\ (\text{nm})} $$

so visible light (400–700 nm) carries roughly 1.8–3.1 eV per photon — the right
size to move an outer electron, which is exactly why chemistry and vision work
with visible light.

::: example Worked example 21.1
**Problem.** A sodium street lamp radiates $40\ \text{W}$ of light of wavelength
$589\ \text{nm}$. Find the energy of one photon in joules and in eV, and the
number of photons emitted per second.

**Solution.** The photon energy is

$$ E = \frac{hc}{\lambda} = \frac{6.63\times10^{-34}\times3.0\times10^{8}}{589\times10^{-9}}
= \frac{1.989\times10^{-25}}{5.89\times10^{-7}} = 3.38\times10^{-19}\ \text{J} $$

$$ E = \frac{3.38\times10^{-19}}{1.6\times10^{-19}} = 2.11\ \text{eV} $$

The number emitted per second is the power divided by the energy per photon:

$$ n = \frac{P}{E} = \frac{40}{3.38\times10^{-19}} = 1.18\times10^{20}\ \text{s}^{-1} $$

More than $10^{20}$ photons a second — which is why a lamp looks continuous and
the graininess of light never shows up in everyday life.
:::

### The photoelectric effect

When light of high enough frequency falls on a clean metal surface, electrons
(called **photoelectrons**) are emitted at once. The apparatus is a photocell: an
evacuated tube with a large emitting cathode C and a small collecting anode A,
connected to a variable pd that can be reversed.

```figure caption="Apparatus for studying photoelectric emission. Monochromatic light of frequency $f$ falls on the cathode C; the potential of the anode A can be made positive or negative and the current read on the microammeter."
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
fig, ax = plt.subplots(figsize=(4.8,3.0))
ax.add_patch(Rectangle((1.4,1.6),4.6,3.0, fill=False, ec=MUTED, lw=1.3))
ax.plot([1.85,1.85],[2.1,4.1], color=INK, lw=3.0)
ax.text(1.62,1.72,'C', fontsize=9.5, color=INK, ha='center')
ax.plot([5.30,5.30],[2.75,3.45], color=INK, lw=3.0)
ax.text(5.05,1.72,'A', fontsize=9.5, color=INK, ha='center')
ax.text(3.7,4.80,'evacuated tube', fontsize=7.8, color=MUTED, ha='center')
for y0 in [2.45,3.10,3.75]:
    ax.annotate('', xy=(1.80,y0), xytext=(0.30,y0+0.55),
                arrowprops=dict(arrowstyle='-|>', color='#b8860b', lw=1.5, mutation_scale=10))
ax.text(0.20,4.58,'light, $f$', fontsize=8.6, color='#b8860b')
for y0 in [2.55,3.10,3.65]:
    ax.annotate('', xy=(5.24,3.10), xytext=(2.05,y0),
                arrowprops=dict(arrowstyle='-|>', color='#d9534f', lw=1.1, mutation_scale=8))
ax.text(3.4,2.22,'photoelectrons', fontsize=7.8, color='#d9534f', ha='center')
# cathode lead down to the supply
ax.plot([1.85,1.85],[2.1,0.32], color=INK, lw=1.2)
ax.plot([1.85,3.10],[0.32,0.32], color=INK, lw=1.2)
# variable, reversible supply (rheostat box)
ax.add_patch(Rectangle((3.10,0.08),1.75,0.48, fill=False, ec=INK, lw=1.2))
ax.annotate('', xy=(4.92,0.66), xytext=(3.05,-0.02),
            arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.0, mutation_scale=9))
ax.plot([4.85,6.55],[0.32,0.32], color=INK, lw=1.2)
ax.text(3.98,-0.52,'variable, reversible pd  $V$', fontsize=8.0, color=INK, ha='center')
# up the right-hand side through the microammeter to the anode
ax.plot([6.55,6.55],[0.32,5.10], color=INK, lw=1.2)
ax.add_patch(Circle((6.55,5.45),0.33, fill=False, ec=INK, lw=1.2))
ax.text(6.55,5.45,'$\mu$A', fontsize=8.0, color=INK, ha='center', va='center')
ax.plot([6.55,6.55],[5.78,6.35], color=INK, lw=1.2)
ax.plot([6.55,5.55],[6.35,6.35], color=INK, lw=1.2)
ax.plot([5.55,5.55],[6.35,3.10], color=INK, lw=1.2)
ax.plot([5.55,5.30],[3.10,3.10], color=INK, lw=1.2)
ax.set_xlim(0.0,7.3); ax.set_ylim(-0.85,6.9); ax.axis('off')
```
Four experimental facts come out, and not one of them is what a wave theory
predicts.

| Observation | Wave theory predicts | What actually happens |
|---|---|---|
| Effect of frequency | any frequency works if you wait | below a **threshold frequency** $f_0$ there is no emission at all, however bright |
| Effect of intensity | brighter light gives faster electrons | brighter light gives **more** electrons, each with the same maximum energy |
| Maximum kinetic energy | depends on intensity | depends **only** on frequency, increasing linearly with $f$ |
| Time lag | seconds to hours for a dim source | emission within $10^{-9}\ \text{s}$, however dim |

::: caution "Brighter means more energetic" is wrong
Doubling the intensity doubles the *number* of photons, so it doubles the
saturation current — but each photon still carries $hf$, so the maximum kinetic
energy and the stopping potential do not change at all.
:::

## 21.2 Einstein's photoelectric equation; Stopping potential

Einstein's picture: one photon is absorbed by one electron, all or nothing. Part
of the energy $hf$ is spent freeing the electron from the metal; the rest appears
as kinetic energy.

::: definition Work function
The **work function** $\phi_0$ of a metal is the minimum energy needed to remove
an electron from its surface. An electron emitted from the surface itself loses
only $\phi_0$ and so carries away the maximum kinetic energy; electrons from
deeper down lose more and come out slower.
:::

$$ hf = \phi_0 + K_{max} \;\Longrightarrow\;
K_{max} = \frac{1}{2}mv_{max}^{2} = hf - \phi_0 $$

Writing $\phi_0 = hf_0$, where $f_0$ is the **threshold frequency**,

$$ K_{max} = h(f - f_0), \qquad
f_0 = \frac{\phi_0}{h}, \qquad \lambda_0 = \frac{hc}{\phi_0} $$

::: key How the equation explains all four facts
1. If $f < f_0$ then $hf < \phi_0$: no electron can escape, whatever the
   intensity. **Threshold frequency explained.**
2. Intensity = number of photons per second, so it fixes the number of
   photoelectrons (the saturation current) and nothing else.
3. $K_{max} = hf - \phi_0$ is a straight line in $f$ with slope $h$ —
   independent of intensity.
4. Absorption is a single one-photon event, so there is no waiting time.
:::

**Stopping potential.** To measure $K_{max}$, make the anode *negative* with
respect to the cathode. Electrons are then decelerated, and slower ones turn back
before arriving. Make the reverse pd large enough and even the fastest electron
is stopped: the current falls to zero. That value $V_0$ is the **stopping
potential**, and

$$ eV_0 = K_{max} = hf - \phi_0 \;\Longrightarrow\;
V_0 = \frac{h}{e}f - \frac{\phi_0}{e} $$

```figure caption="Photocurrent against anode voltage. (a) At fixed frequency, raising the intensity raises the saturation current but leaves $V_0$ unchanged. (b) At fixed intensity, raising the frequency increases $V_0$ but not the saturation current."
import numpy as np, matplotlib.pyplot as plt
fig, (ax, bx) = plt.subplots(1, 2, figsize=(5.1,2.6), sharey=True)
V = np.linspace(-2.6, 6.0, 600)
def curve(V0, sat):
    y = sat*(1 - np.exp(-(V + V0)/0.9))
    return np.where(V > -V0, np.clip(y, 0, None), 0.0)
for sat, c, lab in [(1.00,SERIES[0],'$3I$'), (0.66,SERIES[1],'$2I$'), (0.33,SERIES[2],'$I$')]:
    ax.plot(V, curve(1.2, sat), color=c, lw=1.7, label=lab)
ax.axvline(-1.2, color=MUTED, lw=0.9, ls=(0,(4,3)))
ax.text(-1.32, 0.52, '$-V_0$', fontsize=9, color=MUTED, ha='right')
ax.set_title('(a)  fixed $f$, varying intensity', fontsize=8.6)
ax.legend(loc='center right', fontsize=8.0, title='intensity', title_fontsize=8.0)
for V0, c, lab in [(0.5,SERIES[0],'$f_1$'), (1.4,SERIES[3],'$f_2$'), (2.3,SERIES[4],'$f_3$')]:
    bx.plot(V, curve(V0, 0.80), color=c, lw=1.7, label=lab)
    bx.axvline(-V0, color=c, lw=0.8, ls=(0,(3,3)))
bx.set_title('(b)  fixed intensity, varying $f$', fontsize=8.6)
bx.legend(loc='center right', fontsize=8.0, title='$f_3 > f_2 > f_1$', title_fontsize=8.0)
for a in (ax, bx):
    a.axhline(0, color=INK, lw=0.9); a.axvline(0, color=INK, lw=0.9)
    a.set_xlabel('anode voltage  $V$')
    a.set_xlim(-2.9, 6.0); a.set_ylim(-0.08, 1.18)
    a.set_xticks([]); a.set_yticks([])
    a.spines[['top','right','left','bottom']].set_visible(False)
ax.set_ylabel('photocurrent')
```
Two features of these graphs are examined constantly. The current does **not**
fall to zero at $V = 0$: some electrons leave the cathode with enough energy to
reach the anode unaided. And the current levels off at a **saturation** value when
the anode voltage is high enough to collect every emitted electron.

::: example Worked example 21.2
**Problem.** Light of wavelength $400\ \text{nm}$ falls on a metal of work
function $2.0\ \text{eV}$. Find (a) the photon energy, (b) the maximum kinetic
energy of the photoelectrons, (c) the stopping potential, (d) the maximum speed
of the electrons, and (e) the threshold wavelength of the metal.

**Solution.**

(a) $E = \dfrac{hc}{\lambda} = \dfrac{6.63\times10^{-34}\times3.0\times10^{8}}{4.0\times10^{-7}}
= 4.97\times10^{-19}\ \text{J} = 3.11\ \text{eV}$.

(b) $K_{max} = hf - \phi_0 = 3.11 - 2.0 = 1.11\ \text{eV}
= 1.11\times1.6\times10^{-19} = 1.78\times10^{-19}\ \text{J}$.

(c) $V_0 = K_{max}/e = 1.11\ \text{V}$ (the number of eV read as volts).

(d) From $K_{max} = \frac{1}{2}mv_{max}^{2}$,

$$ v_{max} = \sqrt{\frac{2K_{max}}{m}} = \sqrt{\frac{2\times1.78\times10^{-19}}{9.1\times10^{-31}}}
= \sqrt{3.91\times10^{11}} = 6.25\times10^{5}\ \text{m s}^{-1} $$

(e) $\lambda_0 = \dfrac{hc}{\phi_0} = \dfrac{1.989\times10^{-25}}{2.0\times1.6\times10^{-19}}
= 6.2\times10^{-7}\ \text{m} = 620\ \text{nm}$ — in the orange, so red light would
not work on this metal at all.
:::

## 21.3 Measurement of Planck's constant

The relation $V_0 = (h/e)f - \phi_0/e$ is the equation of a **straight line** in
$f$. Millikan measured it point by point in 1916 — ironically, trying to disprove
Einstein — and got a value of $h$ agreeing with Planck's to better than 1%.

**Procedure.** Monochromatic light of known frequency $f$ is obtained from a
mercury lamp with a set of filters or a monochromator. For each frequency the
reverse pd is increased until the microammeter reads zero, giving $V_0$. The
points $(f, V_0)$ are plotted.

```figure caption="Stopping potential against frequency for two metals. Both lines have the same slope $h/e$; the intercepts give the work functions and threshold frequencies."
import numpy as np, matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(4.8,2.9))
h_e = 4.136e-15
f = np.linspace(0, 1.45e15, 200)
for phi, c, lab in [(2.14, SERIES[0], 'caesium,  $\phi_0 = 2.14$ eV'),
                    (4.65, SERIES[1], 'copper,  $\phi_0 = 4.65$ eV')]:
    f0 = phi/h_e
    ax.plot(f[f >= f0]/1e15, h_e*f[f >= f0] - phi, color=c, lw=1.9, label=lab)
    ax.plot(f[f < f0]/1e15, h_e*f[f < f0] - phi, color=c, lw=1.0, ls=(0,(4,3)))
    ax.plot([f0/1e15],[0], 'o', color=c, ms=5)
ax.axhline(0, color=INK, lw=0.9)
ax.annotate('slope $= h/e$', (0.85, h_e*0.85e15-2.14), xytext=(-72,-6),
            textcoords='offset points', fontsize=8.6, color=INK,
            arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.0, mutation_scale=9))
ax.annotate('$f_0$', (0.517, 0), xytext=(-4,-20), textcoords='offset points',
            fontsize=9, color=SERIES[0])
ax.annotate('intercept $= -\phi_0/e$', (0, -2.14), xytext=(16,-16),
            textcoords='offset points', fontsize=8.4, color=SERIES[0],
            arrowprops=dict(arrowstyle='-|>', color=SERIES[0], lw=1.0, mutation_scale=9))
ax.set_xlabel('frequency  $f$  ($10^{15}$ Hz)')
ax.set_ylabel('stopping potential  $V_0$  (V)')
ax.set_xlim(0, 1.45); ax.set_ylim(-5.2, 2.0)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=0.5)
ax.legend(loc='lower right', fontsize=8.0)
```
Reading the graph:

| Feature of the graph | What it gives |
|---|---|
| Slope | $h/e$, hence $h = e \times \text{slope}$ |
| Intercept on the $V_0$ axis | $-\phi_0/e$, hence the work function |
| Intercept on the $f$ axis | the threshold frequency $f_0$ |
| Lines for different metals | **parallel** — the slope $h/e$ is a universal constant |

That last row is the deep result. The slope does not depend on the metal, on the
intensity or on the apparatus. Planck's constant is a property of nature, not of
the experiment.

If only two readings are available, the graph reduces to two equations:

$$ eV_1 = hf_1 - \phi_0, \qquad eV_2 = hf_2 - \phi_0
\;\Longrightarrow\; h = \frac{e(V_1 - V_2)}{f_1 - f_2} $$

| Metal | $\phi_0$ (eV) | $\lambda_0$ (nm) |
|---|---|---|
| Caesium | 2.14 | 580 |
| Potassium | 2.30 | 540 |
| Sodium | 2.75 | 452 |
| Copper | 4.65 | 267 |
| Platinum | 5.65 | 220 |

Caesium works with ordinary yellow light, which is why photocells and older TV
camera tubes used caesium-coated cathodes; copper and platinum need ultraviolet.

::: example Worked example 21.3
**Problem.** In a photoelectric experiment the stopping potential is
$1.85\ \text{V}$ for light of wavelength $300\ \text{nm}$ and $0.82\ \text{V}$ for
$400\ \text{nm}$. Find Planck's constant and the work function of the cathode.

**Solution.** The frequencies are

$$ f_1 = \frac{c}{\lambda_1} = \frac{3.0\times10^{8}}{300\times10^{-9}} = 1.0\times10^{15}\ \text{Hz},
\qquad f_2 = \frac{3.0\times10^{8}}{400\times10^{-9}} = 7.5\times10^{14}\ \text{Hz} $$

Subtracting the two photoelectric equations removes $\phi_0$:

$$ h = \frac{e(V_1-V_2)}{f_1-f_2}
= \frac{1.6\times10^{-19}\,(1.85-0.82)}{1.0\times10^{15}-7.5\times10^{14}}
= \frac{1.648\times10^{-19}}{2.5\times10^{14}} = 6.59\times10^{-34}\ \text{J s} $$

within 1% of the accepted $6.63\times10^{-34}\ \text{J s}$. The work function
follows from either reading:

$$ \phi_0 = hf_1 - eV_1 = 6.59\times10^{-19} - 2.96\times10^{-19}
= 3.63\times10^{-19}\ \text{J} = 2.27\ \text{eV} $$
:::

::: tip Keep the units in one family
Work in electron-volts when the data is in eV and volts — then $K_{max}$ in eV is
numerically the stopping potential in volts, and you need no conversions at all.
Convert to joules only at the last step, when a speed is asked for.
:::

## Chapter summary

- Radiation is emitted and absorbed in quanta: a photon has $E = hf = hc/\lambda$,
  $p = h/\lambda$, zero rest mass, and travels at $c$.
- Intensity fixes the *number* of photons per second; frequency fixes the energy
  of each one.
- Photoelectric emission occurs only above a threshold frequency $f_0$, is
  instantaneous, gives a current proportional to intensity, and gives a maximum
  kinetic energy proportional to $(f-f_0)$.
- Einstein's equation: $hf = \phi_0 + K_{max}$, with $\phi_0 = hf_0 = hc/\lambda_0$.
- Stopping potential: $eV_0 = K_{max}$, so $V_0 = (h/e)f - \phi_0/e$; $V_0$ is
  independent of intensity.
- A graph of $V_0$ against $f$ is a straight line of slope $h/e$, intercept
  $-\phi_0/e$ and $f$-intercept $f_0$; the slope is the same for every metal,
  giving $h = 6.63\times10^{-34}\ \text{J s}$.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. The momentum of a photon of wavelength $\lambda$ is <span class="marks">[1]</span>
   (a) $h\lambda$ (b) $h/\lambda$ (c) $hc/\lambda$ (d) $\lambda/h$
2. The stopping potential in a photoelectric experiment depends on <span class="marks">[1]</span>
   (a) the intensity only (b) the frequency only (c) the distance of the source (d) the area of the cathode
3. The slope of a stopping potential versus frequency graph equals <span class="marks">[1]</span>
   (a) $h$ (b) $h/e$ (c) $e/h$ (d) $\phi_0$
4. If the intensity of the incident light is doubled at constant frequency, the
   saturation current <span class="marks">[1]</span>
   (a) halves (b) is unchanged (c) doubles (d) becomes zero
5. The rest mass of a photon is <span class="marks">[1]</span>
   (a) $9.1\times10^{-31}\ \text{kg}$ (b) $1.67\times10^{-27}\ \text{kg}$ (c) $hf/c^{2}$ (d) zero

::: note Answers to Group A
**1.** (b) — $p = E/c = hf/c = h/\lambda$.
**2.** (b) — $eV_0 = hf - \phi_0$ contains no intensity term.
**3.** (b) — $V_0 = (h/e)f - \phi_0/e$, so the slope is $h/e$.
**4.** (c) — twice as many photons eject twice as many electrons.
**5.** (d) — a photon has zero rest mass; $hf/c^{2}$ is its *effective* mass.
:::

**Group B — Short answer (5 marks each)**

1. State Einstein's photoelectric equation and use it to explain the existence of
   a threshold frequency and the failure of intensity to change the maximum
   kinetic energy. <span class="marks">[5]</span>
2. Light of wavelength $3000\ \text{Å}$ falls on a metal whose threshold
   wavelength is $5000\ \text{Å}$. Find the work function and the stopping
   potential. <span class="marks">[5]</span>
3. Explain, with sketches, how the photocurrent varies with the anode voltage for
   (i) two different intensities at the same frequency and (ii) two different
   frequencies at the same intensity. <span class="marks">[5]</span>
4. Ultraviolet light of wavelength $300\ \text{nm}$ falls on a sodium surface of
   work function $2.28\ \text{eV}$. Calculate the maximum kinetic energy of the
   photoelectrons in eV, the stopping potential, and the threshold frequency of
   sodium. <span class="marks">[5]</span>
5. Give three observations of the photoelectric effect that the wave theory of
   light cannot explain, and say what the photon theory says about each. <span class="marks">[5]</span>

::: note Answers to Group B
**2.** $\phi_0 = hc/\lambda_0 = 1.989\times10^{-25}/(5.0\times10^{-7})
= 3.98\times10^{-19}\ \text{J} = 2.49\ \text{eV}$. Photon energy
$= 1.989\times10^{-25}/(3.0\times10^{-7}) = 6.63\times10^{-19}\ \text{J} = 4.14\ \text{eV}$.
So $K_{max} = 4.14 - 2.49 = 1.65\ \text{eV}$ and $V_0 = 1.65\ \text{V}$.

**4.** Photon energy $= 1.989\times10^{-25}/(3.0\times10^{-7}) = 6.63\times10^{-19}\ \text{J}
= 4.14\ \text{eV}$. $K_{max} = 4.14 - 2.28 = 1.86\ \text{eV}$, so $V_0 = 1.86\ \text{V}$.
Threshold frequency $f_0 = \phi_0/h = (2.28\times1.6\times10^{-19})/(6.63\times10^{-34})
= 5.50\times10^{14}\ \text{Hz}$ (that is $\lambda_0 = 545\ \text{nm}$).
:::

**Group C — Long answer (8 marks each)**

1. (a) Describe, with a labelled diagram, an experiment to study the photoelectric
   effect, and define stopping potential. <span class="marks">[4]</span>
   (b) Derive Einstein's photoelectric equation and explain how a graph of
   stopping potential against frequency is used to measure Planck's constant and
   the work function. <span class="marks">[4]</span>
2. A photocell has a caesium cathode of work function $2.14\ \text{eV}$ and is
   illuminated with light of wavelength $400\ \text{nm}$.
   Find (a) the energy of each photon in eV, (b) the maximum kinetic energy of
   the photoelectrons, (c) the stopping potential, (d) the maximum speed of the
   electrons, and (e) the longest wavelength that would still cause emission.
   State what happens to answers (c) and (e) if the intensity is doubled. <span class="marks">[8]</span>

::: note Answer to Group C question 2
(a) $E = hc/\lambda = 1.989\times10^{-25}/(4.0\times10^{-7}) = 4.97\times10^{-19}\ \text{J}
= 3.11\ \text{eV}$.

(b) $K_{max} = 3.11 - 2.14 = 0.97\ \text{eV} = 0.97\times1.6\times10^{-19}
= 1.55\times10^{-19}\ \text{J}$.

(c) $V_0 = 0.97\ \text{V}$.

(d) $v_{max} = \sqrt{2K_{max}/m} = \sqrt{2\times1.55\times10^{-19}/9.1\times10^{-31}}
= \sqrt{3.41\times10^{11}} = 5.8\times10^{5}\ \text{m s}^{-1}$.

(e) $\lambda_0 = hc/\phi_0 = 1.989\times10^{-25}/(2.14\times1.6\times10^{-19})
= 5.8\times10^{-7}\ \text{m} = 580\ \text{nm}$.

Doubling the intensity changes **neither** (c) nor (e): it only doubles the number
of photoelectrons, and hence the saturation current.
:::
