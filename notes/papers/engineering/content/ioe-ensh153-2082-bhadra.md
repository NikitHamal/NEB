---
file: NEBians-IOE-Past-Paper-Engineering-Chemistry-ENSH153-2082-Bhadra.pdf
subject: Engineering Chemistry
level: BE · Year I / Part II
code: ENSH 153
year_bs: 2082 Bhadra
cal: BS
year_ad: 2025
stream: BEL, BEI, BCT, BAM, BIE, BAS, BGE
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular (new course). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
What is a galvanic cell? Draw a diagram of a Daniel cell. Calculate the emf of the following cell at 25°C. [[1+1+3]]
$\text{Fe/Fe}^{2+}(0.6\ \text{M})//\text{Sn}^{2+}(0.2\ \text{M})/\text{Sn}$. Given: $E^\circ_{\text{Fe}^{2+}/\text{Fe}} = -0.44$ V and $E^\circ_{\text{Sn}^{2+}/\text{Sn}} = -0.14$ V.
@or
Write down the Butler-Volmer equation and its uses. Explain the charging and discharging process in lead acid battery with suitable chemical reactions. [[2+3]]

@q 2
Derive the Henderson's equation for basic buffer. If 3.0 milli mole of NaOH is added to 100 ml of a buffer which is 0.10 M in acetic acid and 0.1 M in sodium acetate, what will be the change in pH of solution? ($\text{p}K_a$ = 4.74). [[1+4]]

@q 3
Define photocatalysis and electrocatalysis. Explain the photocatalytic process of water splitting. [[1+1+3]]

@q 4
Write the principle of chromatography along with its applications. How is X-ray diffraction method useful in the analysis of crystalline structure? [[3+2]]
@or
Describe the principle of NMR spectroscopy. Draw and explain NMR spectrum of ethanol. [[3+2]]

@q 5
On the basis of VBT, explain the structure and hybridization involved in $[\text{Ni(CO)}_4]$. Write the IUPAC names of followings complexes. [[3+2]]
(i) $[\text{Cr(en)}_3]\text{Br}_3$ (ii) $[\text{Cr(H}_2\text{O)}_5\text{Cl}]\text{Cl}_2$ (iii) $\text{K}_3[\text{AlF}_6]$ (iv) $[\text{Cr(NH}_3)_4\text{SO}_4]\text{NO}_3$

@q 6
Explain crystal field splitting of d orbitals in tetrahedral complex. Also describe the color formation process in complexes with an example. [[3+2]]

@q 7
(a) What is green chemistry? Explain two principles of green chemistry with suitable examples. Discuss COD and its consequences with reference to water pollution. [[1+2+2]]
(b) Discuss the impacts of SOx and NOx on the environment and human health? How can we control emission containing SOx? [[3+2]]

@q 8
Define nanofibers and Mxene. Discuss physical vapor deposition (PVD) method for preparation of nanomaterials. [[2+3]]

@q 9
(a) Define fiber reinforced polymer. Write the preparation and use of polycarbonate and epoxy resin. [[1+2+2]]
(b) Differentiate between addition and condensation polymerization. Write the mechanism of anionic polymerization reaction with a suitable example. [[2+3]]
@or
Write short notes on: (i) Cellulose (ii) Polyphosphazine [[2×2.5]]

@q 10
(a) What is primary explosive? Write the preparation and uses of TNT. [[1+2]]
(b) Write the functions of lubricants. What are the requisite of paints? [[1+1]]
<!-- SOLUTIONS -->

@s 1
**Galvanic cell.** A galvanic (voltaic) cell is an electrochemical cell in which a **spontaneous redox reaction** produces electrical energy. Oxidation takes place at the anode (negative) and reduction at the cathode (positive); electrons flow through the external wire from anode to cathode, and ions move through the salt bridge.

**Daniell cell.** It consists of a zinc rod in $\text{ZnSO}_4$ solution (anode) and a copper rod in $\text{CuSO}_4$ solution (cathode) connected by a salt bridge ($\text{KCl}$ in agar) and an external wire:
$$\begin{gathered}\text{Zn(s)}\,|\,\text{ZnSO}_4(aq)\,\|\,\text{CuSO}_4(aq)\,|\,\text{Cu(s)} \\ E^\circ = 1.10\ \text{V}\end{gathered}$$
Anode: $\text{Zn}\to\text{Zn}^{2+} + 2e^-$; cathode: $\text{Cu}^{2+} + 2e^-\to\text{Cu}$.

```figure caption="Daniell cell: zinc anode in ZnSO4, copper cathode in CuSO4, salt bridge between the two beakers. Electrons flow from Zn to Cu through the wire."
import numpy as np, matplotlib.pyplot as plt, matplotlib.patches as mp
fig,ax=plt.subplots(figsize=(4.9,3.0))
for x0,col,lab in [(0.5,"#cfe3f7","ZnSO$_4$"),(3.5,"#c6e8e4","CuSO$_4$")]:
    ax.add_patch(mp.Rectangle((x0,0.2),2.0,1.7,fc="none",ec=INK,lw=1.4))
    ax.add_patch(mp.Rectangle((x0,0.2),2.0,1.2,fc=col,ec="none"))
    ax.text(x0+1.0,0.45,lab,ha="center",fontsize=8)
ax.add_patch(mp.Rectangle((1.0,0.5),0.35,1.9,fc="#9aa3ad",ec=INK)); ax.text(1.17,2.55,"Zn (anode, $-$)",ha="center",fontsize=7.5)
ax.add_patch(mp.Rectangle((4.65,0.5),0.35,1.9,fc="#c77b4a",ec=INK)); ax.text(4.82,2.55,"Cu (cathode, +)",ha="center",fontsize=7.5)
ax.plot([1.17,1.17,4.82,4.82],[2.4,3.0,3.0,2.4],color=INK,lw=1.3)
ax.annotate("",xy=(3.4,3.0),xytext=(2.6,3.0),arrowprops=dict(arrowstyle="->",color=SERIES[1],lw=1.4)); ax.text(3.0,3.12,"e$^-$",ha="center",color=SERIES[1],fontsize=8)
ax.plot([1.9,1.9,4.1,4.1],[1.2,2.0,2.0,1.2],color=SERIES[3],lw=7,solid_capstyle="butt",alpha=0.55); ax.text(3.0,1.75,"salt bridge",ha="center",fontsize=7.5,color=INK)
ax.set_xlim(0,6.2); ax.set_ylim(0,3.4); ax.axis("off")
```

**EMF of the cell.** The cell is $\text{Fe}\,|\,\text{Fe}^{2+}(0.6\ \text{M})\,\|\,\text{Sn}^{2+}(0.2\ \text{M})\,|\,\text{Sn}$. Fe has the lower reduction potential, so it is the anode, and Sn the cathode:
$$\begin{gathered}\text{Fe} + \text{Sn}^{2+}\to\text{Fe}^{2+} + \text{Sn} \\ n = 2\end{gathered}$$
$$E^\circ_{cell} = E^\circ_{cathode} - E^\circ_{anode} = -0.14 - (-0.44) = 0.30\ \text{V}$$
$$E_{cell} = E^\circ - \frac{0.0591}{2}\log\frac{[\text{Fe}^{2+}]}{[\text{Sn}^{2+}]} = 0.30 - 0.02955\log\frac{0.6}{0.2} = 0.30 - 0.02955\log3$$
$$\boxed{E_{cell} = 0.30 - 0.02955(0.4771) = 0.286\ \text{V}}$$

**Or. Butler–Volmer equation.** It gives the current density $j$ of an electrode reaction as a function of the overpotential $\eta$ (activation control):
$$\boxed{j = j_0\left[\exp\left(\frac{\alpha_aF\eta}{RT}\right) - \exp\left(-\frac{\alpha_cF\eta}{RT}\right)\right]}$$
$j_0$ is the exchange current density, $\alpha_a,\alpha_c$ the anodic and cathodic transfer coefficients ($\alpha_a + \alpha_c = 1$), $F$ Faraday's constant. For small $\eta$ it is linear, $j = j_0F\eta/RT$; for large $|\eta|$ it reduces to the Tafel equation $\eta = a + b\log j$.
*Uses:* kinetics of electrode reactions ($j_0$, $\alpha$), design of batteries, fuel cells and electrolysers, corrosion-rate estimation, comparing electrocatalysts, and electroplating.

**Lead–acid battery.** Anode (negative plate): spongy Pb; cathode (positive plate): $\text{PbO}_2$; electrolyte: about 37% $\text{H}_2\text{SO}_4$ ($\rho\approx1.28$ g/cm³); a cell gives about 2 V (a 12 V battery has 6 cells).

*Discharging (as a galvanic cell):*
$$\begin{gathered}\text{Anode: Pb + SO}_4^{2-}\to\text{PbSO}_4 + 2e^- \\ \text{Cathode: PbO}_2 + 4\text{H}^+ + \text{SO}_4^{2-} + 2e^-\to\text{PbSO}_4 + 2\text{H}_2\text{O} \\ \text{Overall: Pb + PbO}_2 + 2\text{H}_2\text{SO}_4\to2\text{PbSO}_4 + 2\text{H}_2\text{O}\end{gathered}$$
$\text{H}_2\text{SO}_4$ is consumed, so the acid density falls (a check of charge state).

*Charging (as an electrolytic cell, an external source forces the reverse reaction):*
$$2\text{PbSO}_4 + 2\text{H}_2\text{O}\to\text{Pb} + \text{PbO}_2 + 2\text{H}_2\text{SO}_4$$
The $\text{PbSO}_4$ on both plates is converted back to Pb (cathode during charging) and $\text{PbO}_2$ (anode), and the acid is regenerated.

@s 2
**Henderson's equation for a basic buffer.** A basic buffer is a weak base B and its salt BH⁺A⁻ with a strong acid, for example $\text{NH}_4\text{OH} + \text{NH}_4\text{Cl}$. For the weak base
$$\begin{gathered}\text{B} + \text{H}_2\text{O}\rightleftharpoons\text{BH}^+ + \text{OH}^- \\ K_b = \frac{[\text{BH}^+][\text{OH}^-]}{[\text{B}]}\end{gathered}$$
$$[\text{OH}^-] = K_b\frac{[\text{B}]}{[\text{BH}^+]}$$
Take the negative logarithm of both sides:
$$-\log[\text{OH}^-] = -\log K_b - \log\frac{[\text{B}]}{[\text{BH}^+]}$$
$$\begin{gathered}\boxed{\text{pOH} = \text{p}K_b + \log\frac{[\text{salt}]}{[\text{base}]}} \\ \text{pH} = 14 - \text{pOH}\end{gathered}$$
Here $[\text{BH}^+]$ is taken as the salt concentration (the salt is completely ionised and the base ionises very little) and $[\text{B}]$ as the base concentration. (For an acidic buffer, $\text{pH} = \text{p}K_a + \log\dfrac{[\text{salt}]}{[\text{acid}]}$.)

**Numerical.** Buffer volume 100 mL: acetic acid $= 0.10\times100 = 10$ mmol, acetate $= 10$ mmol.
*Initial pH:* $\text{pH}_0 = 4.74 + \log\dfrac{10}{10} = 4.74$.
*After adding 3.0 mmol NaOH:* $\text{CH}_3\text{COOH} + \text{OH}^-\to\text{CH}_3\text{COO}^- + \text{H}_2\text{O}$
$$\begin{gathered}\text{acid} = 10 - 3 = 7\ \text{mmol} \\ \text{acetate} = 10 + 3 = 13\ \text{mmol}\end{gathered}$$
$$\text{pH} = 4.74 + \log\frac{13}{7} = 4.74 + 0.269 = 5.009\approx5.01$$
$$\boxed{\Delta\text{pH} = 5.01 - 4.74 = +0.27}$$
The pH increases by only 0.27 units. (The same amount of NaOH in 100 mL of pure water would raise the pH from 7 to 12.5, a change of 5.5.)

@s 3
**Photocatalysis.** The acceleration of a chemical reaction by a catalyst (a semiconductor such as $\text{TiO}_2$, ZnO, CdS, $\text{g-C}_3\text{N}_4$) that is activated by absorbing **light** (UV or visible) of energy greater than its band gap, and which is not consumed.
**Electrocatalysis.** The increase of the rate of an electrode (electrochemical) reaction by a catalyst on the electrode surface, which lowers the overpotential (e.g. Pt for the hydrogen evolution reaction, $\text{IrO}_2$/$\text{RuO}_2$ for oxygen evolution, Pt in fuel cells).

**Photocatalytic water splitting** (with $\text{TiO}_2$, $E_g = 3.2$ eV):
1. **Light absorption:** a photon with $h\nu\ge E_g$ excites an electron from the valence band (VB) to the conduction band (CB), leaving a hole:
$$\text{TiO}_2 + h\nu\to e^-_{CB} + h^+_{VB}$$
2. **Charge separation and migration** of $e^-$ and $h^+$ to the surface (some recombine).
3. **Surface redox reactions:** the holes oxidise water (the VB edge must lie below the $\text{O}_2/\text{H}_2\text{O}$ level, +1.23 V), and the electrons reduce protons (the CB edge must lie above the $\text{H}^+/\text{H}_2$ level, 0 V):
$$\begin{gathered}\text{Oxidation (VB): }2\text{H}_2\text{O} + 4h^+\to\text{O}_2 + 4\text{H}^+ \\ \text{Reduction (CB): }4\text{H}^+ + 4e^-\to2\text{H}_2 \\ \text{Overall: }2\text{H}_2\text{O}\xrightarrow{h\nu,\ \text{catalyst}}2\text{H}_2 + \text{O}_2\quad(\Delta G = +237\ \text{kJ/mol per H}_2\text{O})\end{gathered}$$
A co-catalyst (Pt, $\text{RuO}_2$) is often loaded to improve charge separation. The band gap must be at least 1.23 eV (practically 1.8–2.0 eV) and straddle both redox levels. Sacrificial agents (methanol) and visible-light photocatalysts (doped $\text{TiO}_2$, CdS) improve the efficiency. The process gives clean hydrogen fuel from sunlight and water.

@s 4
**Principle of chromatography.** The components of a mixture are separated because they distribute differently between a **stationary phase** and a **mobile phase** that flows over it. A component with a larger affinity for the stationary phase (adsorption or partition) moves slowly, and one with a larger affinity for the mobile phase moves faster, so the components emerge or spread at different positions. The distribution is measured by the retention factor $R_f$ or the retention time. Types: adsorption (column, TLC), partition (paper), ion exchange, gel permeation (size exclusion), and gas or liquid chromatography (GC, HPLC).

*Applications:* separation and purification of mixtures; testing the purity of drugs and chemicals; qualitative and quantitative analysis of amino acids, sugars, vitamins, dyes, pesticide residues in food and water; forensic analysis (drugs, poisons); monitoring of reactions; analysis of air and water pollutants; isolating natural products.

**X-ray diffraction (XRD).** X-rays have a wavelength ($\sim0.1$–$0.2$ nm) comparable to interatomic distances, so a crystal acts as a three-dimensional diffraction grating. A monochromatic beam reflected from successive lattice planes of spacing $d$ gives constructive interference only when the path difference $2d\sin\theta$ is a whole number of wavelengths (**Bragg's law**):
$$\boxed{2d\sin\theta = n\lambda}$$
*Use:* by measuring the angles $2\theta$ of the diffracted peaks (powder method, diffractometer) one finds the interplanar spacings $d$, which gives:
- the **crystal structure** (cubic, hexagonal, etc.), lattice parameters and unit cell dimensions;
- the **identification of crystalline phases** and compounds by comparing the pattern with the database (the pattern is a fingerprint);
- the **crystallite size** from peak broadening (Scherrer formula, $D = \dfrac{0.9\lambda}{\beta\cos\theta}$), strain and degree of crystallinity (sharp peaks for crystalline, a broad halo for amorphous);
- the positions of atoms in a unit cell from single-crystal diffraction (bond lengths and angles, e.g. NaCl, diamond, DNA, proteins).

**Or. NMR spectroscopy: principle.** Nuclei with an odd mass number or odd atomic number (¹H, ¹³C) have a spin $I$ and a magnetic moment. In an external magnetic field $B_0$ they take $2I + 1$ orientations (for ¹H, $I = \tfrac12$: parallel, lower energy, and antiparallel, higher energy) with energy gap $\Delta E = \dfrac{\gamma h}{2\pi}B_0$. Radiation of radio-frequency $\nu = \dfrac{\gamma B_0}{2\pi}$ causes a spin flip (**resonance**). The actual field at a nucleus is reduced by the shielding of the surrounding electrons, so protons in different chemical environments resonate at different frequencies: this **chemical shift**, $\delta = \dfrac{\nu_{sample} - \nu_{TMS}}{\nu_{spectrometer}}\times10^6$ ppm, relative to tetramethylsilane (TMS, $\delta = 0$). The number of signals gives the number of types of H; the **area** (integral) gives the number of H in each type; and **spin–spin splitting** ($n + 1$ rule) gives the number of neighbouring H.

**NMR spectrum of ethanol, $\text{CH}_3\text{CH}_2\text{OH}$** (high resolution): three kinds of protons, three signals:

| Protons | $\delta$ (ppm) | Area | Splitting |
|---|---|---|---|
| $\text{CH}_3$ | ~1.2 | 3 | triplet (2 neighbouring H on CH₂) |
| $\text{CH}_2$ | ~3.7 | 2 | quartet (3 H on CH₃); (further split by OH if exchange is slow) |
| $\text{OH}$ | ~2–5 (variable) | 1 | singlet (broad; rapid proton exchange removes the coupling) |
The area ratio is 3 : 2 : 1. The CH₂ is the most deshielded because it is attached to the electronegative O.

```figure caption="Schematic 1H NMR spectrum of ethanol: CH3 triplet near 1.2 ppm, OH singlet, CH2 quartet near 3.7 ppm (areas 3 : 1 : 2 in order of shift)."
import numpy as np, matplotlib.pyplot as plt
d=np.linspace(0,5,4000)
def L(x,c,w=0.012): return w**2/((x-c)**2+w**2)
y=np.zeros_like(d)
for c,a in [(1.12,1),(1.2,2),(1.28,1)]: y+=0.75*a*L(d,c)
y+=0.9*L(d,2.6,0.07)
for c,a in [(3.55,1),(3.63,3),(3.71,3),(3.79,1)]: y+=0.3*a*L(d,c)*0+0.33*a*L(d,c)
y+=0.04*L(d,0,0.02)
fig,ax=plt.subplots(figsize=(4.8,2.3))
ax.plot(d,y,color=INK,lw=1.1); ax.invert_xaxis(); ax.set_yticks([])
ax.set_xlabel("chemical shift  $\\delta$ (ppm)")
ax.text(1.2,2.0,"CH$_3$ (3H)\ntriplet",ha="center",fontsize=7.5,color=ACCENT)
ax.text(2.6,1.0,"OH (1H)",ha="center",fontsize=7.5,color=SERIES[1])
ax.text(3.67,1.3,"CH$_2$ (2H)\nquartet",ha="center",fontsize=7.5,color=SERIES[2])
ax.text(0.0,0.2,"TMS",ha="center",fontsize=7,color=MUTED); ax.set_ylim(0,2.7)
for s in ["left","right","top"]: ax.spines[s].set_visible(False)
```

@s 5
**$[\text{Ni(CO)}_4]$ by VBT.** Ni in the zero oxidation state: $\text{Ni}(0)$, $3d^84s^2$. CO is a strong-field ligand: it forces the two $4s$ electrons to move into the $3d$ orbitals (and pair), giving the configuration $3d^{10}$:
$$\text{Ni}(0)\ 3d^8\,4s^2\ \xrightarrow{\text{CO}}\ 3d^{10}\,4s^0$$
All five $3d$ orbitals are now filled, and the vacant $4s$ and three $4p$ orbitals hybridise to $sp^3$ and accept four lone pairs from the four CO ligands:
$$[\text{Ni(CO)}_4]:\ [\uparrow\downarrow][\uparrow\downarrow][\uparrow\downarrow][\uparrow\downarrow][\uparrow\downarrow]\ \ \underbrace{[\text{CO}][\text{CO}][\text{CO}][\text{CO}]}_{sp^3}$$
- Hybridisation: $sp^3$; **geometry: tetrahedral** (bond angle $109.5^\circ$).
- No unpaired electrons, so the complex is **diamagnetic**. The CO also back-donates $d\to\pi^*$ electrons, which stabilises the complex; it is an inner-shell ($3d$) complete, outer-orbital ($4s4p$) bonded complex.

**IUPAC names.**

| Complex | Name | Oxidation state |
|---|---|---|
| (i) $[\text{Cr(en)}_3]\text{Br}_3$ | tris(ethane-1,2-diamine)chromium(III) bromide | $x + 0 = +3$ |
| (ii) $[\text{Cr(H}_2\text{O)}_5\text{Cl}]\text{Cl}_2$ | pentaaquachloridochromium(III) chloride | $x + 0 - 1 = +2$, $x = +3$ |
| (iii) $\text{K}_3[\text{AlF}_6]$ | potassium hexafluoridoaluminate(III) | $x - 6 = -3$, $x = +3$ |
| (iv) $[\text{Cr(NH}_3)_4\text{SO}_4]\text{NO}_3$ | tetraamminesulfatochromium(III) nitrate | $x + 0 - 2 = +1$, $x = +3$ |

@s 6
**Crystal field splitting in a tetrahedral complex.** In a tetrahedral field, the four ligands approach along the alternate corners of a cube, and the metal is at the centre. The ligands lie **between** the axes, so they approach the $t_2$ orbitals ($d_{xy}$, $d_{yz}$, $d_{xz}$, whose lobes point towards the cube edges' mid-points, closer to the ligands) more closely than the $e$ orbitals ($d_{x^2-y^2}$, $d_{z^2}$, which point along the axes through the cube-face centres). So the order is the **reverse** of the octahedral case:
$$\begin{gathered}E(t_2) = +0.4\Delta_t \\ E(e) = -0.6\Delta_t\end{gathered}$$
with the barycentre unchanged. The splitting is small: $\Delta_t = \dfrac49\Delta_o\approx0.44\Delta_o$ (for the same metal, ligand and distance), because there are only four ligands and none points directly at the orbitals. Hence $\Delta_t$ is always smaller than the pairing energy, and **tetrahedral complexes are always high-spin** (e.g. $[\text{NiCl}_4]^{2-}$, $[\text{CoCl}_4]^{2-}$, $[\text{FeCl}_4]^-$). The $g$ subscript is absent because the tetrahedron has no centre of inversion.

```figure caption="Splitting of d orbitals in a tetrahedral field (the inverse of the octahedral pattern): e lowered by 0.6 Delta_t, t2 raised by 0.4 Delta_t."
import numpy as np, matplotlib.pyplot as plt
fig,ax=plt.subplots(figsize=(4.4,2.7))
ax.hlines(0,0.0,1.0,color=INK,lw=1.4); ax.text(0.5,0.08,"free ion",ha="center",fontsize=7.5,color=MUTED)
for i in range(3): ax.hlines(0.4,2.7+i*1.1,3.7+i*1.1,color=INK,lw=1.8)
ax.text(6.1,0.4,"$t_2$  (+0.4 $\\Delta_t$)",fontsize=8,va="center")
for i in range(2): ax.hlines(-0.6,3.25+i*1.1,4.25+i*1.1,color=INK,lw=1.8)
ax.text(6.1,-0.6,"$e$  (-0.6 $\\Delta_t$)",fontsize=8,va="center")
ax.hlines(0,1.0,2.7,color=GRID,lw=0.9,ls="--")
ax.annotate("",xy=(4.1,0.4),xytext=(4.1,-0.6),arrowprops=dict(arrowstyle="<->",color=SERIES[1],lw=1.3)); ax.text(4.25,-0.1,"$\\Delta_t$",color=SERIES[1],fontsize=9)
ax.set_xlim(-0.2,8.8); ax.set_ylim(-0.9,0.8); ax.axis("off")
```

**Colour formation in complexes.** Transition-metal complexes with partly filled $d$ orbitals are coloured because of **d–d transitions**. Absorption of visible light of energy equal to the splitting $\Delta$ promotes an electron from a lower to a higher $d$ level (e.g. $t_{2g}\to e_g$ in octahedral complexes):
$$\Delta E = h\nu = \frac{hc}{\lambda}$$
The complex absorbs that part of white light and the colour seen is the **complementary colour** of the light absorbed (transmitted or reflected). The colour depends on the metal, its oxidation state, and the ligand strength (a larger $\Delta$ means absorption at a shorter wavelength).
*Example:* $[\text{Ti(H}_2\text{O)}_6]^{3+}$ ($3d^1$) absorbs green-yellow light (~500 nm, $\Delta_o\approx20{,}300\ \text{cm}^{-1}$), the $t_{2g}^1\to e_g^1$ transition, and appears **violet/purple**. $[\text{Cu(H}_2\text{O)}_4]^{2+}$ is pale blue and $[\text{Cu(NH}_3)_4]^{2+}$ a deep blue (stronger ligand, larger $\Delta$). Complexes with $d^0$ ($\text{Sc}^{3+}$, $\text{Zn}^{2+}$ ($d^{10}$)) have no d–d transition and are colourless.

@s 7
**(a) Green chemistry.** Green chemistry is the design of chemical products and processes that **reduce or eliminate the use and generation of hazardous substances** at the source (Anastas and Warner, 12 principles).

*Two principles with examples:*
1. **Prevention of waste:** it is better to prevent waste than to treat or clean it afterwards. *Example:* the Pfizer sertraline process and the BHC ibuprofen synthesis (3 steps instead of 6, with high atom economy) generates much less waste.
2. **Atom economy:** design syntheses so that most of the atoms of the reactants end up in the product, $\text{atom economy} = \dfrac{M(\text{desired product})}{\sum M(\text{reactants})}\times100$. *Example:* the Diels–Alder addition and hydrogenation have 100% atom economy; the Wittig reaction has a low one. 
(Other principles: safer solvents, e.g. water or supercritical $\text{CO}_2$ for dry cleaning instead of perchloroethylene; use of renewable feedstocks; catalysis rather than stoichiometric reagents; energy efficiency.)

**COD and its consequences.** Chemical oxygen demand is the amount of oxygen (mg O₂/L) required to oxidise all oxidisable organic (and some inorganic) matter in a water sample with a strong oxidant, usually boiling acidified $\text{K}_2\text{Cr}_2\text{O}_7$ (with $\text{Ag}_2\text{SO}_4$ catalyst), determined by back-titrating the remaining dichromate against ferrous ammonium sulfate. It measures the total organic pollution (including non-biodegradable matter) and COD $\ge$ BOD.
*Consequences:* a high COD means that a large amount of oxygen would be consumed; if released into rivers or lakes, it **depletes dissolved oxygen**, kills fish and aquatic life, leads to anaerobic conditions (bad odour, $\text{H}_2\text{S}$, $\text{CH}_4$), eutrophication, makes water unsuitable for drinking, and often indicates toxic organic pollutants. Industrial effluent limits COD to about 250 mg/L.

**(b) Impacts of SOx and NOx.** Sources: burning coal and oil (power plants, brick kilns, vehicles, smelters) forms $\text{SO}_2$ and $\text{SO}_3$; high-temperature combustion in engines forms NO and $\text{NO}_2$ ($\text{N}_2 + \text{O}_2\to2\text{NO}$).
*Environment:*
- **Acid rain:** $\text{SO}_2 + \text{H}_2\text{O}\to\text{H}_2\text{SO}_3$, $2\text{SO}_2 + \text{O}_2\to2\text{SO}_3$, $\text{SO}_3 + \text{H}_2\text{O}\to\text{H}_2\text{SO}_4$; $4\text{NO}_2 + \text{O}_2 + 2\text{H}_2\text{O}\to4\text{HNO}_3$. It acidifies lakes and soil, kills fish and forest, and corrodes buildings, marble and metals (the Taj Mahal).
- $\text{NO}_x$ + VOC + sunlight give **photochemical smog** and ground-level ozone; $\text{NO}_x$ cause nutrient overload (eutrophication); nitrous oxide $\text{N}_2\text{O}$ is a greenhouse gas; sulfate aerosols reduce visibility.
*Human health:* irritation of the eyes, nose and throat; asthma, bronchitis, emphysema and reduced lung function, especially in children and the old; $\text{NO}_2$ lowers resistance to respiratory infections; at high concentration pulmonary oedema and heart disease.

*Control of SOx emission:*
1. Use **low-sulfur fuel**, natural gas, or desulfurise coal (washing) and oil (hydrodesulfurisation).
2. **Flue gas desulfurisation (FGD):** wet scrubbing with a slurry of lime or limestone, $\text{SO}_2 + \text{CaCO}_3 + \tfrac12\text{O}_2 + 2\text{H}_2\text{O}\to\text{CaSO}_4\cdot2\text{H}_2\text{O} + \text{CO}_2$ (gypsum by-product, 90–95% removal); dry or semi-dry sorbent injection; $\text{SO}_2$ absorption in $\text{Na}_2\text{SO}_3$ or ammonia.
3. Fluidised-bed combustion with limestone, taller stacks, and a switch to renewable energy.
(Control of $\text{NO}_x$: low-$\text{NO}_x$ burners, catalytic converters in vehicles, selective catalytic reduction with $\text{NH}_3$.)

@s 8
**Nanofibres.** Fibres with a diameter in the nanometre range (1–100 nm, up to a few hundred nm) and a length thousands of times larger (an aspect ratio > 100). They are made from polymers, carbon or ceramics by electrospinning, template synthesis or CVD, and have a large surface-area-to-volume ratio, high porosity and good mechanical strength. Examples: polymer (PAN, PVA) nanofibres, carbon nanofibres, $\text{TiO}_2$ nanofibres; used in filters, tissue-engineering scaffolds, wound dressing, sensors and batteries.

**MXene.** A family of two-dimensional transition-metal carbides, nitrides and carbonitrides of the formula $\text{M}_{n+1}\text{X}_n\text{T}_x$ (M = early transition metal, e.g. Ti, V, Nb, Mo; X = C or N; $T_x$ = surface terminations –OH, –O, –F). They are made by selectively etching the A layer (Al) from a layered MAX phase ($\text{Ti}_3\text{AlC}_2$) with HF (or LiF/HCl), giving $\text{Ti}_3\text{C}_2\text{T}_x$. MXenes combine metallic conductivity with a hydrophilic surface, and are used in supercapacitors and batteries, EMI shielding, sensors, water purification and catalysis.

**Physical vapour deposition (PVD).** In PVD a solid material is converted to vapour by a **physical process** (heating or ion bombardment) in a high vacuum ($10^{-3}$–$10^{-6}$ Pa), and the vapour **condenses on a cooler substrate** to form a nanostructured thin film or nanoparticles. No chemical reaction is involved (unlike CVD).

*Steps:* (1) vaporisation of the target; (2) transport of the atoms through the vacuum (or a low-pressure inert gas); (3) condensation, nucleation and growth of the film on the substrate.

*Main methods:*
- **Thermal (vacuum) evaporation:** the source is heated by a resistance heater, an electron beam or a laser until it evaporates (e.g. Al, Au films).
- **Sputtering:** energetic $\text{Ar}^+$ ions in a plasma bombard a target and knock atoms out (DC, RF, magnetron sputtering), suitable for high melting point materials and alloys.
- **Pulsed laser deposition** and **cathodic arc deposition**.
In inert-gas condensation, the vapour condenses in cold He gas to give nanoparticles.

*Advantages:* clean and pure films, good adhesion, a wide range of materials, controlled thickness. *Limitations:* a high vacuum and a high-cost apparatus, line-of-sight deposition (poor coverage of complex shapes), and slow rates. *Uses:* hard coatings (TiN on tools), optical and mirror coatings, microelectronics and solar cells.

@s 9
**(a) Fibre reinforced polymer (FRP).** A composite material in which strong **fibres** (glass, carbon, aramid) are embedded in a polymer **matrix** (epoxy, polyester, vinyl ester). The fibres carry the load and the matrix binds them, transfers stress and protects them. FRPs have a high strength-to-weight ratio, corrosion resistance and fatigue life (examples: GFRP, CFRP). They are used in aircraft, wind-turbine blades, boats, sports equipment, bridges, and the strengthening of concrete structures.

**Polycarbonate (PC).** *Preparation:* condensation (step) polymerisation of **bisphenol-A** with **phosgene** ($\text{COCl}_2$) in the presence of a base (interfacial method) or by trans-esterification with diphenyl carbonate (melt process), with the loss of HCl (or phenol):
$$n\,\text{HO–C}_6\text{H}_4\text{–C(CH}_3)_2\text{–C}_6\text{H}_4\text{–OH} + n\,\text{COCl}_2\xrightarrow{\text{NaOH}}[\text{–O–C}_6\text{H}_4\text{–C(CH}_3)_2\text{–C}_6\text{H}_4\text{–O–CO–}]_n + 2n\,\text{HCl}$$
*Uses:* transparent, high-impact-resistant material for bullet-proof glazing, safety helmets and goggles, CDs/DVDs, electrical housings, lenses, greenhouse sheets, baby bottles (BPA-free substitutes) and car parts.

**Epoxy resin.** *Preparation:* condensation of **epichlorohydrin** with **bisphenol-A** in the presence of NaOH (which removes the HCl) gives a low-molar-mass diglycidyl ether of bisphenol-A (DGEBA) with epoxide end-groups:
$$\text{2 ClCH}_2\text{CH(O)CH}_2 + \text{HO–Ar–OH}\xrightarrow{\text{NaOH}}\text{CH}_2\text{(O)CH–CH}_2\text{–O–Ar–O–CH}_2\text{–CH(O)CH}_2 + 2\text{HCl}$$
The liquid resin is **cured (cross-linked)** by a hardener such as a polyamine (triethylenetetramine) or an acid anhydride, which opens the epoxide rings and forms a rigid three-dimensional network (a thermoset). *Uses:* strong adhesives (Araldite), surface coatings and paints, matrix of FRP, electrical encapsulation, flooring, and printed circuit boards.

**(b) Addition vs condensation polymerisation.**

| Addition polymerisation | Condensation polymerisation |
|---|---|
| Unsaturated monomers (C=C) add to each other | Bifunctional monomers react with the loss of a small molecule ($\text{H}_2\text{O}$, HCl, $\text{NH}_3$) |
| No by-product; $M_{polymer} = n\,M_{monomer}$ | By-product eliminated; $M_{polymer}<n\,M_{monomer}$ |
| Chain-growth: initiation, propagation, termination | Step-growth: any two molecules (monomer, dimer, oligomer) can react |
| High molar mass formed at once | Molar mass rises slowly with conversion |
| e.g. polyethylene, PVC, polystyrene | e.g. nylon-6,6, PET, Bakelite |

**Anionic polymerisation.** A chain-growth addition polymerisation started by a nucleophile (carbanion), applicable to monomers with electron-withdrawing groups that stabilise the carbanion (styrene, acrylonitrile, methyl methacrylate, butadiene). *Example:* polymerisation of **styrene** with *n*-butyllithium ($\text{n-BuLi}$) in THF or a hydrocarbon solvent.
1. **Initiation:** the butyl carbanion adds to the monomer:
$$\text{Bu}^-\text{Li}^+ + \text{CH}_2{=}\text{CHPh}\to\text{Bu–CH}_2\text{–C}^-\text{HPh}\ \text{Li}^+$$
2. **Propagation:** the benzylic carbanion (stabilised by the phenyl ring) attacks further monomer:
$$\text{Bu–(CH}_2\text{CHPh)}_n\text{–CH}_2\text{–C}^-\text{HPh} + \text{CH}_2{=}\text{CHPh}\to\text{Bu–(CH}_2\text{CHPh)}_{n+1}\text{–CH}_2\text{–C}^-\text{HPh}$$
3. **Termination:** there is no spontaneous termination; the chains remain "living" while monomer is present (each initiator gives one chain, so the molar mass is monomer/initiator and the distribution is narrow, $\text{PDI}\approx1$). Termination only on deliberate addition of a proton donor ($\text{H}_2\text{O}$, alcohol, $\text{CO}_2$): $\text{...C}^-\text{HPh} + \text{H}_2\text{O}\to\text{...CH}_2\text{Ph} + \text{OH}^-$. Living polymers allow the preparation of block copolymers (SBS rubber).

**Or. (i) Cellulose.** The most abundant natural polysaccharide, $(\text{C}_6\text{H}_{10}\text{O}_5)_n$, a linear polymer of $\beta$-D-glucose units joined by $\beta$-(1→4) glycosidic bonds (n = 3000–10 000). The chains form strong inter- and intra-chain hydrogen bonds into microfibrils, so it is insoluble in water and gives plant cell walls their strength; it is the main component of cotton (~90%) and wood (~50%). Humans cannot digest it. *Uses:* paper and board, textiles (cotton, rayon from viscose), cellulose acetate and nitrate (films, explosives, celluloid), carboxymethyl cellulose (thickener), and biofuel.

**(ii) Polyphosphazene.** An inorganic backbone polymer of alternating phosphorus and nitrogen atoms with two organic or organometallic side groups on each P: $[\text{–N=PR}_2\text{–}]_n$. *Preparation:* ring-opening polymerisation of hexachlorocyclotriphosphazene $(\text{NPCl}_2)_3$ at 250°C gives poly(dichlorophosphazene) $[\text{NPCl}_2]_n$, whose Cl atoms are replaced by nucleophiles (alkoxides, amines): $[\text{NPCl}_2]_n + 2n\,\text{NaOR}\to[\text{NP(OR)}_2]_n + 2n\,\text{NaCl}$. The backbone is very flexible (low glass-transition temperature) and the polymer is flame-resistant, and can be hydrolytically stable or biodegradable depending on R. *Uses:* fuel-line seals and O-rings (fluorophosphazene elastomers), fire-resistant materials, biomedical polymers (drug delivery, tissue engineering) and solid polymer electrolytes.

@s 10
**(a) Primary explosive.** A primary explosive is a very sensitive explosive that detonates on a small input of heat, friction, spark or impact, and is used to start (initiate) the explosion of less sensitive secondary explosives. Examples: lead azide $\text{Pb(N}_3)_2$, mercury fulminate $\text{Hg(ONC)}_2$, lead styphnate. (They are used in detonators.)

**TNT (2,4,6-trinitrotoluene).** *Preparation:* stepwise nitration of toluene with a mixture of conc. $\text{HNO}_3$ and conc. $\text{H}_2\text{SO}_4$ at gradually increasing temperature (30°C for mono-, 60°C for di-, and 100–115°C for trinitro; the sulfuric acid absorbs the water formed and generates the nitronium ion $\text{NO}_2^+$):
$$\text{C}_6\text{H}_5\text{CH}_3\xrightarrow{\text{HNO}_3/\text{H}_2\text{SO}_4,\ 30^\circ\text{C}}\text{O}_2\text{N–C}_6\text{H}_4\text{CH}_3\xrightarrow{60^\circ\text{C}}(\text{O}_2\text{N})_2\text{C}_6\text{H}_3\text{CH}_3\xrightarrow{100\text{–}115^\circ\text{C}}(\text{O}_2\text{N})_3\text{C}_6\text{H}_2\text{CH}_3$$
The product is washed with water and sodium sulfite and crystallised from alcohol. It is a pale yellow solid, melting point 81°C.
*Decomposition:* $2\,\text{C}_7\text{H}_5\text{N}_3\text{O}_6\to7\,\text{CO} + 7\,\text{C} + 5\,\text{H}_2\text{O} + 3\,\text{N}_2$ (oxygen-deficient, so black smoke).
*Uses:* a secondary (high) explosive in shells, bombs and grenades, military and demolition work, and in mining and quarrying (alone or in amatol with ammonium nitrate, torpex). It is insensitive to shock, and safe to handle and cast, and is the standard measure of explosive energy (1 ton TNT = 4.184 GJ).

**(b) Functions of lubricants.**
1. **Reduce friction and wear** between moving surfaces by forming a film that separates them.
2. **Cool the machine** by carrying heat away from the bearing and engine parts.
3. **Seal** the gap between piston and cylinder (preventing gas leakage).
4. **Prevent corrosion** (rusting) of the metal surfaces.
5. **Clean** the surfaces (carry away dirt and wear particles), reduce noise and vibration, and save power.

**Requisites of a good paint.**
- **Good covering power (opacity)** and a uniform, smooth coating, from a suitable pigment (e.g. $\text{TiO}_2$) and a proper viscosity for easy application.
- **Good adhesion** to the surface, and flexibility without cracking or peeling.
- **Drying quickly** to a hard, durable, tough film, with a suitable vehicle (drying oil such as linseed oil) and thinner.
- **Resistant** to weather, water, sunlight, heat, chemicals and abrasion, and **protective** against corrosion.
- **Non-toxic**, low in VOC, **colour-fast** (no fading or chalking), cheap, and with an attractive finish.
