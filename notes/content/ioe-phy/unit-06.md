---
subject: Physics
grade: IOE
unit: 6
title: Modern Physics
hours: 2
area: Physics
---

Modern physics carries about **2 questions** (our estimate), but the syllabus is long: electrons, the photoelectric effect, Bohr, de Broglie, X-rays, semiconductors and gates, radioactivity and nuclear energy, plus a list of "recent trends" (particle physics, the universe, seismology, telecommunication, environment, new materials). The numerical questions repeat a few formulae; the recent-trends items are definitions you can score by reading once.

::: key What the paper asks from this chapter
- $e/m=1.76\times10^{11}$ C kg⁻¹; Millikan: charge is quantised, $e=1.6\times10^{-19}$ C.
- Photon $E=hf=\frac{1240\ \text{eV nm}}{\lambda}$; Einstein $K_{max}=hf-\phi$; $eV_s=K_{max}$.
- Bohr: $E_n=-\frac{13.6}{n^2}$ eV; $\frac{1}{\lambda}=R\big(\frac{1}{n_1^2}-\frac{1}{n_2^2}\big)$; Lyman, Balmer, Paschen.
- de Broglie $\lambda=\frac{h}{p}$, $\lambda\approx\frac{1.227}{\sqrt{V}}$ nm for electrons; uncertainty $\Delta x\,\Delta p\ge\frac{\hbar}{2}$; Bragg $2d\sin\theta=n\lambda$.
- Semiconductors: p-n junction, rectifier, Zener, transistor ($\beta=\frac{\alpha}{1-\alpha}$), logic gates.
- Nuclear: $N=N_0e^{-\lambda t}$, $T_{1/2}=\frac{0.693}{\lambda}$, $E=\Delta m\,c^2$ (1 u = 931.5 MeV), fission, fusion, carbon dating.
:::

## 6.1 Electrons

**Cathode rays** (a discharge tube at low pressure) are streams of electrons: deflected by electric and magnetic fields, negatively charged, travel in straight lines, produce X-rays on striking a target. **J.J. Thomson:** with crossed fields the speed is $v=\frac{E}{B}$; the deflection with only $B$ gives the **specific charge** $\frac{e}{m}=1.76\times10^{11}$ C kg⁻¹. **Millikan's oil-drop:** drops balanced between plates, $qE=mg$; every charge is an integral multiple of $e=1.6\times10^{-19}$ C (charge is quantised). Electron mass $9.1\times10^{-31}$ kg. An electron accelerated through $V$ volts gains $eV$ joules ($1\ \text{eV}=1.6\times10^{-19}$ J) and speed $\sqrt{\frac{2eV}{m}}$.

## 6.2 Photons and quantization of energy

**Photoelectric effect.** Light of frequency above the threshold $f_0$ ejects electrons instantly; $K_{max}$ depends on frequency, not intensity; the photo-current depends on intensity.
$$K_{max}=hf-\phi=h(f-f_0),\qquad eV_s=K_{max},\qquad \phi=hf_0.$$
$h=6.63\times10^{-34}$ J s; photon energy $E=\frac{hc}{\lambda}=\frac{1240}{\lambda(\text{nm})}$ eV; photon momentum $\frac{h}{\lambda}$. The wave theory cannot explain the instantaneous emission or the threshold. A 100 W sodium lamp (589 nm) emits about $3\times10^{20}$ photons per second.

**Bohr's theory (hydrogen):** angular momentum $mvr=\frac{nh}{2\pi}$; $E_n=-\dfrac{13.6}{n^2}$ eV; $r_n=0.53n^2$ Å; $v_n=\frac{2.2\times10^6}{n}$ m s⁻¹. Emission when an electron falls: $h f=E_{n_2}-E_{n_1}$, $\frac{1}{\lambda}=R\Big(\frac{1}{n_1^2}-\frac{1}{n_2^2}\Big)$, $R=1.097\times10^7$ m⁻¹.

| Series | Final level $n_1$ | Region |
|---|---|---|
| Lyman | 1 | ultraviolet |
| Balmer | 2 | visible (H$\alpha$ 656 nm for 3→2) |
| Paschen | 3 | infrared |
| Brackett, Pfund | 4, 5 | far infrared |

Ionisation energy of hydrogen is 13.6 eV; the first excitation energy 10.2 eV.

**de Broglie:** $\lambda=\frac{h}{p}=\frac{h}{mv}$; electron through $V$ volts: $\lambda=\frac{1.227}{\sqrt{V}}$ nm ($V=150$ V gives 0.1 nm). **Heisenberg uncertainty:** $\Delta x\Delta p\ge\frac{\hbar}{2}=\frac{h}{4\pi}$. **X-rays:** produced when fast electrons strike a metal target; the continuous spectrum has a minimum wavelength $\lambda_{min}=\frac{hc}{eV}$; the characteristic lines depend on the target (Moseley). **Bragg's law:** $2d\sin\theta=n\lambda$. X-rays are not deflected by fields, penetrate matter, are used in medicine and crystallography. **Laser:** stimulated emission, population inversion, optical cavity; light is coherent, monochromatic, directional and intense (surgery, cutting, communication, barcode readers).

## 6.3 Solids and semiconductor devices

Band theory: conductors (bands overlap), insulators (gap $>3$ eV), semiconductors (gap about 1 eV: Si 1.1, Ge 0.7). **Intrinsic** semiconductors have equal electron and hole numbers; their resistance falls with temperature. **Extrinsic:** n-type (donor, pentavalent: P, As, Sb; electrons majority), p-type (acceptor, trivalent: B, Al, In; holes majority); $n_en_h=n_i^2$.

**p-n junction:** diffusion creates a depletion layer and a barrier potential (0.3 V Ge, 0.7 V Si). *Forward bias* (p to +): the layer narrows and current flows; *reverse bias*: the layer widens, a tiny leakage current flows. **Rectification:** half-wave (one diode, ripple frequency = input), full-wave (two diodes or a bridge, ripple $2f$); a capacitor smooths the output. **Zener diode:** in reverse breakdown it holds a constant voltage (a regulator); LED and photodiode are other junction devices.

**Transistor** (npn / pnp; emitter, base, collector): $I_E=I_B+I_C$; $\alpha=\frac{I_C}{I_E}$, $\beta=\frac{I_C}{I_B}$, $\beta=\frac{\alpha}{1-\alpha}$ ($\alpha=0.98$: $\beta=49$); amplifier in common-emitter mode (phase reversal $180^\circ$), switch in cut-off and saturation. **Logic gates:**

| Gate | Output | Note |
|---|---|---|
| AND | 1 only if both inputs 1 | |
| OR | 1 if any input 1 | |
| NOT | inverts | |
| NAND, NOR | negations of AND, OR | **universal gates** |
| XOR | 1 if inputs differ | |

De Morgan: $\overline{A\cdot B}=\bar A+\bar B$, $\overline{A+B}=\bar A\cdot\bar B$.

## 6.4 Radioactivity and nuclear reaction

**Nucleus:** $A=Z+N$; radius $R=R_0A^{1/3}$, $R_0=1.2$ fm; so density is constant, about $2.3\times10^{17}$ kg m⁻³, independent of $A$. **Isotopes** share $Z$; isobars share $A$; isotones share $N$. Atomic mass unit: 1 u $=1.66\times10^{-27}$ kg $=931.5$ MeV$/c^2$.

**Mass–energy:** $E=mc^2$; **mass defect** $\Delta m=Zm_p+Nm_n-m_{nucleus}$; **binding energy** $=\Delta m\times931.5$ MeV; BE per nucleon peaks near $^{56}$Fe (8.8 MeV), so fission of heavy and fusion of light nuclei both release energy. Conversion of 1 g of matter gives $9\times10^{13}$ J.

**Decay law:** $N=N_0e^{-\lambda t}=N_0\big(\frac{1}{2}\big)^{t/T_{1/2}}$; $T_{1/2}=\frac{\ln2}{\lambda}=\frac{0.693}{\lambda}$; mean life $\tau=\frac{1}{\lambda}=1.44T_{1/2}$; activity $A=\lambda N$ (becquerel = 1 decay s⁻¹; curie $=3.7\times10^{10}$ Bq). After $n$ half-lives $\big(\frac{1}{2}\big)^n$ remains. $\alpha$ decay: $Z-2$, $A-4$; $\beta^-$: $Z+1$, an antineutrino emitted; $\gamma$: no change in $Z,A$.

**Carbon dating:** living matter has a constant $^{14}$C/$^{12}$C ratio; after death $^{14}$C ($T_{1/2}=5730$ y) decays; a sample with 25 % of the original is 11 460 years old. **Fission:** $^{235}$U + n → fragments + 2–3 neutrons + about 200 MeV, a chain reaction controlled by moderator (graphite, heavy water) and control rods (Cd, B). **Fusion:** light nuclei combine at about $10^7$ K (Sun: proton–proton cycle). **Health hazards:** ionising radiation damages DNA; dose in sievert; shielding, distance and time reduce exposure; radioactive waste handling.

## 6.5 Recent trends in physics

- **Particle physics:** every particle has an antiparticle (positron–electron annihilation $\to2\gamma$). **Quarks** (up, down, strange, charm, top, bottom; fractional charge $\pm\frac{1}{3},\pm\frac{2}{3}$) build hadrons: **baryons** (three quarks: proton uud, neutron udd) and **mesons** (quark–antiquark, e.g. pion). **Leptons** (electron, muon, tau and their neutrinos) are fundamental. The **Higgs boson** (found at the LHC, CERN, 2012; mass about 125 GeV) is the quantum of the field that gives mass.
- **Universe:** Big Bang about 13.8 billion years ago; **Hubble's law** $v=H_0d$ (galaxies recede; expansion); the cosmic microwave background; **dark matter** (galaxy rotation curves) and dark energy; **gravitational waves** (ripples of space-time from merging black holes, first detected by LIGO in 2015); **black hole**: escape speed exceeds $c$, event horizon $r_s=\frac{2GM}{c^2}$.
- **Seismology:** P-waves (longitudinal, fastest, through solids and liquids), S-waves (transverse, solids only); surface (L) waves cause the greatest damage; the Richter / magnitude scale is logarithmic.
- **Telecommunication:** radio (AM, FM, modulation), TV, mobile (cells), **GPS** (24+ satellites, timing signals; relativistic corrections), **remote sensing** (satellite imaging of land, forests, floods).
- **Environment:** energy crisis, greenhouse effect and global warming, ozone layer depletion by CFCs (UV-B), pollution.
- **New materials:** **nanotechnology** (1–100 nm; properties change with size), **superconductors** (zero resistance below $T_c$, Meissner effect — expel magnetic field; used in MRI and maglev), distinguished from a **perfect conductor** (which does not expel fields).

```photogrid label="6.1" cols="2" ratio="1.2" caption="Counting random decays. (a) A Geiger-Muller counter: each click is one ionising particle entering the tube, and the clicks come at random even though their average rate is steady. (b) A seeded simulation of 2,000 identical nuclei with half-life 10 min, each nucleus decaying independently with probability $1 - 2^{-1/10}$ every minute. The dots follow $N = N_0 (1/2)^{t/T}$ closely but not exactly; the first time the count falls to half is close to the true half-life, and the activity is $\\lambda N$ with $\\lambda = \\ln 2 / T$."
@ photo id="ioephy/geiger" cap="A Geiger-Muller counter"
fit 1.2
focus 0.5 0.5
@ svg cap="2,000 nuclei, T = 10 min: simulation vs formula"
import random, math
rnd = random.Random(2081)
N0, T = 2000, 10.0; p = 1 - 2 ** (-1 / T)
N = N0; sim = [N]
for m in range(40):
    N -= sum(1 for _ in range(N) if rnd.random() < p); sim.append(N)
half = next(m for m, n in enumerate(sim) if n <= N0 / 2)
lam = math.log(2) / T
assert abs(half - 10) <= 1 and abs(sim[20] - N0 / 4) < 60
f = Fig(300, 236)
X = lambda t: 40 + t * 6.2; Y = lambda n: 170 - n * 0.075
f.line(40, 170, 290, 170, color=SLATE, sw=1.2); f.line(40, 170, 40, 14, color=SLATE, sw=1.2)
pts = [(X(t), Y(N0 * 0.5 ** (t / T))) for t in range(0, 41)]
for a, b in zip(pts, pts[1:]): f.line(a[0], a[1], b[0], b[1], color=TEAL, sw=1.8)
for t, n in enumerate(sim):
    if t % 2 == 0: f.circle(X(t), Y(n), 2.8, fill=RED, stroke=RED)
for t in (0, 10, 20, 30, 40): f.text(X(t), 184, str(t), size=10.5, color=SLATE)
for n in (0, 1000, 2000): f.text(34, Y(n) + 4, format(n, ","), size=10.5, color=SLATE, anchor="end")
f.text(165, 200, "time in minutes", size=10.5, color=SLATE)
f.text(150, 218, "count halves at %d min (T = 10); N(20) = %d (expect 500)" % (half, sim[20]), size=10.5, color=NAVY, bold=True)
f.text(150, 232, "start activity = λ N0 = %d per min" % round(lam * N0), size=10.5, color=TEAL, bold=True)
```

```photogrid label="6.2" cols="2" ratio="1.2" caption="Photon energy sets the colour. (a) A 5 mm LED with its tiny chip on the anvil of the lead frame: when an electron falls across the band gap of the semiconductor, one photon leaves with energy equal to the gap. (b) $E = hc/\\lambda = 1239.8$ eV nm$/\\lambda$ for three typical LED colours, computed here. Blue needs the widest gap, so a blue LED needs a higher forward voltage than a red one; the energy of one blue photon is only about $4\\times10^{-19}$ J, which is why one LED emits billions every nanosecond."
@ photo id="ioephy/led" cap="A 5 mm LED: the chip sits in the reflector cup"
fit 1.2
focus 0.5 0.5
@ svg cap="Photon energy for three LED colours"
hc = 1239.84; e = 1.602e-19
leds = [("red 630 nm", 630, "#dc2626", "#fecaca"), ("green 525 nm", 525, "#16a34a", "#bbf7d0"), ("blue 465 nm", 465, "#2563eb", "#bfdbfe")]
E = [hc / w for _, w, _, _ in leds]
assert abs(E[0] - 1.97) < 0.01 and abs(E[2] - 2.67) < 0.01
f = Fig(300, 236)
f.text(150, 14, "E = hc / λ", size=10.5, color=NAVY, bold=True)
for i, ((n, w, c, bg), en) in enumerate(zip(leds, E)):
    y = 34 + i * 46; wd = 200 * en / 2.8
    f.text(8, y, n, size=10.5, color=c, bold=True, anchor="start")
    f.box(8, y + 6, wd, 20, "", fill=bg, stroke=c, r=3, sw=1)
    f.text(wd + 14, y + 16, "%.2f eV" % en, size=10.5, color=c, bold=True, anchor="start", vmid=True)
f.text(150, 186, "1 blue photon = %.2fe-19 J" % (E[2] * e * 1e19), size=10.5, color=NAVY, bold=True)
f.text(150, 206, "band gap about equals photon energy", size=10.5, color=SLATE)
f.text(150, 226, "ratio blue : red = %.2f (shorter wave, more energy)" % (E[2] / E[0]), size=10.5, color=TEAL, bold=True)
```

## Formula and fact sheet

| Topic | Result |
|---|---|
| $e/m$ | $1.76\times10^{11}$ C kg⁻¹ |
| photon | $E=hf=1240/\lambda_{nm}$ eV |
| photoelectric | $K_{max}=hf-\phi$ |
| Bohr | $E_n=-13.6/n^2$ eV |
| de Broglie | $\lambda=h/p$; $1.227/\sqrt{V}$ nm |
| Bragg | $2d\sin\theta=n\lambda$ |
| $\beta$ | $\alpha/(1-\alpha)$ |
| decay | $N=N_02^{-t/T}$; $T=0.693/\lambda$ |
| energy | 1 u $=931.5$ MeV |

## Chapter summary

- Photons carry $hf$; only frequency above threshold ejects electrons.
- Bohr energies scale as $1/n^2$; series are named by the final level.
- Wave–particle duality: $\lambda=h/p$; the uncertainty principle limits $x$ and $p$.
- Forward bias narrows the depletion layer; NAND and NOR are universal.
- $N=N_0(\tfrac{1}{2})^{n}$ after $n$ half-lives; binding energy peaks near iron.
- Know the recent-trends vocabulary: quark, boson, Hubble, LIGO, P/S waves, nano, superconductor.

## Practice questions

**Set A — Recall (10 questions)**

1. The specific charge of the electron is
   (a) $1.76\times10^{11}$ C kg⁻¹ (b) $9.1\times10^{-31}$ C kg⁻¹ (c) $1.6\times10^{-19}$ C kg⁻¹ (d) $1.76\times10^{-11}$ C kg⁻¹
2. The energy of a photon of wavelength 620 nm is
   (a) 1 eV (b) 2 eV (c) 4 eV (d) 0.5 eV
3. Photons of energy 5 eV fall on a metal of work function 2 eV. The stopping potential is
   (a) 2 V (b) 5 V (c) 3 V (d) 7 V
4. The energy of the hydrogen atom in the $n=2$ level is
   (a) $-13.6$ eV (b) $-6.8$ eV (c) $-1.51$ eV (d) $-3.4$ eV
5. The Balmer series of hydrogen lies in the
   (a) visible region (b) ultraviolet (c) infrared (d) X-ray region
6. The de Broglie wavelength of an electron accelerated through 150 V is about
   (a) 1 nm (b) 0.1 nm (c) 0.01 nm (d) 10 nm
7. After three half-lives the fraction of a radioactive sample that remains is
   (a) $1/3$ (b) $1/6$ (c) $1/8$ (d) $1/9$
8. An energy equivalent to 1 atomic mass unit is
   (a) 9.3 MeV (b) 93 MeV (c) 9315 MeV (d) 931.5 MeV
9. In forward bias the depletion region of a p-n junction
   (a) narrows (b) widens (c) is unchanged (d) is permanent
10. Which gate is known as a universal gate?
    (a) AND (b) OR (c) NAND (d) XOR

::: note Answers and explanations — Set A
**1.** (a) — $e/m=1.76\times10^{11}$ C kg⁻¹.
**2.** (b) — $\frac{1240}{620}=2$ eV.
**3.** (c) — $K_{max}=5-2=3$ eV, so $V_s=3$ V.
**4.** (d) — $-\frac{13.6}{4}$.
**5.** (a) — Balmer lines end at $n=2$ and are visible; Lyman is UV.
**6.** (b) — $\frac{1.227}{\sqrt{150}}=0.1$ nm.
**7.** (c) — $(\frac{1}{2})^3$.
**8.** (d) — standard.
**9.** (a) — the applied field opposes the barrier.
**10.** (c) — NAND (and NOR) can make every other gate.
:::

**Set B — Understanding (6 questions)**

1. A metal has threshold wavelength 500 nm. Light of wavelength 400 nm falls on it. The maximum kinetic energy of the photoelectrons is nearly
   (a) 0.62 eV (b) 1.24 eV (c) 3.1 eV (d) 2.48 eV
2. The wavelength of the H$\alpha$ line (the $n=3\to2$ transition) of hydrogen is nearly
   (a) 486 nm (b) 656 nm (c) 434 nm (d) 122 nm
3. A sample of 80 g of a radioactive element has a half-life of 10 days. After 30 days the mass remaining is
   (a) 40 g (b) 20 g (c) 10 g (d) 5 g
4. A wood sample has 25 % of the $^{14}$C of a living sample ($T_{1/2}=5730$ y). Its age is about
   (a) 5730 y (b) 2865 y (c) 17190 y (d) 11460 y
5. X-rays reflect from planes spaced 0.2 nm at a glancing angle of $30^\circ$ in first order. The wavelength is
   (a) 0.2 nm (b) 0.1 nm (c) 0.4 nm (d) 0.346 nm
6. The energy released by the complete conversion of 1 g of matter is
   (a) $9\times10^{16}$ J (b) $9\times10^{13}$ J (c) $9\times10^{10}$ J (d) $3\times10^{8}$ J

::: note Answers and explanations — Set B
**1.** (a) — $\frac{1240}{400}-\frac{1240}{500}=3.10-2.48=0.62$ eV.
**2.** (b) — $\Delta E=13.6(\frac{1}{4}-\frac{1}{9})=1.89$ eV; $\lambda=\frac{1240}{1.89}=656$ nm.
**3.** (c) — three half-lives: $80\to40\to20\to10$.
**4.** (d) — 25 % is two half-lives, $2\times5730$.
**5.** (a) — $\lambda=2d\sin\theta=2\times0.2\times0.5$.
**6.** (b) — $10^{-3}\times(3\times10^8)^2$.
:::

**Set C — Application (4 questions)**

1. A 100 W lamp emits light of wavelength 589 nm, all of its power. The number of photons per second is about
   (a) $3\times10^{20}$ (b) $3\times10^{18}$ (c) $3\times10^{22}$ (d) $3\times10^{19}$
2. A nucleus has a mass defect of 0.03 u. Its binding energy is nearly
   (a) 2.8 MeV (b) 28 MeV (c) 280 MeV (d) 0.28 MeV
3. A transistor has $\alpha=0.98$. Its current gain $\beta$ is
   (a) 98 (b) 4.9 (c) 49 (d) 0.02
4. An electron is localised to within 1 Å. The minimum uncertainty in its momentum ($\hbar=1.05\times10^{-34}$ J s) is about
   (a) $5.3\times10^{-24}$ (b) $6.6\times10^{-24}$ (c) $1.1\times10^{-34}$ (d) $5.3\times10^{-25}$ kg m s⁻¹

::: note Answers and explanations — Set C
**1.** (a) — $E=\frac{hc}{\lambda}=3.38\times10^{-19}$ J; $N=\frac{100}{3.38\times10^{-19}}$.
**2.** (b) — $0.03\times931.5=27.9$ MeV.
**3.** (c) — $\beta=\frac{0.98}{0.02}=49$.
**4.** (d) — $\Delta p\ge\frac{\hbar}{2\Delta x}=\frac{1.05\times10^{-34}}{2\times10^{-10}}=5.3\times10^{-25}$.
:::
