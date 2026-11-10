---
file: NEBians-IOE-Past-Paper-Electrical-Engineering-Material-ENEE203-2081-Chaitra.pdf
subject: Electrical Engineering Material
level: BE · Year II / Part I
code: ENEE 203
year_bs: 2081 Chaitra
cal: BS
year_ad: 2025
stream: BEL
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular examination (new course, 2080 batch), BE Electrical Engineering (BEL), Year II / Part I. Full marks 60, pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

Constants: $m_e = 9.1\times10^{-31}$ kg; $h = 6.624\times10^{-34}$ J s; $n_i = 1.45\times10^{10}\ \text{cm}^{-3}$ for Si; $\mu_n = 1350\ \text{cm}^2\text{V}^{-1}\text{s}^{-1}$ (300 K); $\mu_h = 450\ \text{cm}^2\text{V}^{-1}\text{s}^{-1}$ (300 K); 1 eV $= 1.6\times10^{-19}$ J; $k = 1.38\times10^{-23}$ J/K; $N_A = 6.022\times10^{23}$/mol; permittivity of silicon $\varepsilon = \varepsilon_r\varepsilon_0 = 11.9\times8.85\times10^{-12}$ F/m; velocity of light $= 3\times10^{8}$ m/s; mass of photon $= 1.673\times10^{-27}$ kg.

@q 1
(a) With necessary mathematical expression, explain the nature of wave function in different regions in case of quantum leak. [[5]]

(b) An electron is confined to an infinite potential well of size 8.5 nm. Calculate the ground state energy of the electron and radian frequency. How this electron can be put to the fourth energy level? [[3]]

@q 2
(a) Using image charge method, derive an expression of emission current density for Schottky effect. [[6]]

(b) Find the temperature at which the probability of occupation of the energy state 0.75 eV above the Fermi energy is 30%. [[4]]

@q 3
(a) Derive the Clausius-Mossotti equation showing the relation between electronic polarizability and relative permittivity. [[4]]

(b) A glass dielectric has dielectric constant 2.6 and loss tangent $7\times10^{-5}$ at 1 MHz. Calculate the loss of power per unit volume if the signal applied to the glass has peak amplitude of 0.71 V/m. [[2]]

(c) Show that the dielectric loss per unit volume is a function of frequency of the applied field and the loss tangent. [[4]]

@q 4
(a) Classify the magnetic materials based on magnetization and explain each of them briefly. [[5]]

(b) Explain demagnetization of magnetic materials with the help of magnetic domain formation. Suggest which type of magnetic material is used for storing digital information and why? [[5]]

@q 5
(a) What is Meissner effect? Explain in brief about type-I and type-II superconductor. [[6]]

(b) Explain how donor dopants contribute electrons in conduction band in n-type extrinsic semiconductor. Also prove that $\sigma = ne\mu_e$ where symbols have their usual meanings. [[4]]

@q 6
(a) The density of states related effective masses of electrons and holes in silicon are approximately $1.08\,m_e$ and $0.56\,m_e$ respectively. The electron and hole drift mobilities at room temperature are 1350 and 450 cm$^2$V$^{-1}$s$^{-1}$ respectively. Calculate intrinsic concentration and intrinsic resistivity of silicon. The energy band gap for silicon is 1.1 eV. [[4]]

(b) An n-type semiconductor doped with $10^{16}\ \text{cm}^{-3}$ phosphorus atoms has been doped with $10^{17}\ \text{cm}^{-3}$ boron atoms. Calculate the electron and hole concentrations in the semiconductor. [[3]]

(c) Derive the expression for built-in potential in p-n junction. [[5]]

<!-- SOLUTIONS -->

@s 1
**(a) Quantum leak (quantum-mechanical tunnelling).** A particle of energy $E$ meets a potential barrier of height $V_0 > E$ and width $L$. Classically it is always reflected; in quantum mechanics its wave function does not vanish inside the barrier, so there is a finite probability of finding the particle on the other side. This "leak" through the barrier is called tunnelling. Take $V = 0$ for $x < 0$ and $x > L$, and $V = V_0$ for $0 < x < L$. The time-independent Schrödinger equation $-\dfrac{\hbar^2}{2m}\psi'' + V\psi = E\psi$ gives:

| Region | Equation | Wave function |
|---|---|---|
| I ($x < 0$), $V = 0$ | $\psi'' + k^2\psi = 0$, $k = \sqrt{2mE}/\hbar$ | $\psi_I = Ae^{ikx} + Be^{-ikx}$ (incident + reflected plane waves) |
| II ($0 < x < L$), $V = V_0 > E$ | $\psi'' - \alpha^2\psi = 0$, $\alpha = \sqrt{2m(V_0 - E)}/\hbar$ | $\psi_{II} = Ce^{-\alpha x} + De^{\alpha x}$ (real exponentials: **non-oscillating, decaying**) |
| III ($x > L$), $V = 0$ | same as region I | $\psi_{III} = Fe^{ikx}$ (only a transmitted wave, no wave coming back) |

The constants follow from the continuity of $\psi$ and $d\psi/dx$ at $x = 0$ and $x = L$. In the barrier the probability density decays as $|\psi|^2 \propto e^{-2\alpha x}$, and in region III the wave has the same wavelength as in region I but a much smaller amplitude. The **transmission coefficient** ($T = |F|^2/|A|^2$) is, for $\alpha L \gg 1$,

$$T \approx 16\frac{E}{V_0}\left(1 - \frac{E}{V_0}\right)e^{-2\alpha L}$$

so tunnelling decreases exponentially with the barrier width and with $\sqrt{m(V_0 - E)}$; it matters only for light particles (electrons) and thin barriers (nm). Applications: tunnel diode, scanning tunnelling microscope, Josephson junction, flash memory, field emission, alpha decay.

```figure caption="Question 1(a): wave function in the three regions of a rectangular barrier: oscillating in region I (incident + reflected), decaying exponentially inside the barrier, and a transmitted wave of smaller amplitude in region III."
fig,ax=plt.subplots(figsize=(5.8,2.6))
x1=np.linspace(-3,0,200); x2=np.linspace(0,1.5,100); x3=np.linspace(1.5,4.5,200)
ax.add_patch(Rectangle((0,0),1.5,1.6,fc="#f1efe6",ec=MUTED,lw=1)); ax.text(0.75,1.4,"V$_0$",ha="center",fontsize=9)
ax.plot(x1,0.35+0.55*np.cos(6*x1)*0.9+0.3*np.cos(6*x1+1.2)*0.2,color=ACCENT,lw=1.7)
y2=0.9*np.exp(-1.6*x2); ax.plot(x2,0.35+y2,color=SERIES[1],lw=1.7)
ax.plot(x3,0.35+0.18*np.cos(6*(x3-1.5)+0.0)*np.exp(-1.6*1.5)/np.exp(-1.6*1.5),color=SERIES[2],lw=1.7)
ax.axhline(0.35,color=GRID,lw=0.7)
for t,x in (("region I",-1.5),("region II",0.75),("region III",3.0)): ax.text(x,1.95,t,ha="center",fontsize=8.5)
ax.text(-1.5,-0.55,"$Ae^{ikx}+Be^{-ikx}$",ha="center",fontsize=8.5); ax.text(0.75,-0.55,"$Ce^{-\\alpha x}+De^{\\alpha x}$",ha="center",fontsize=8.5); ax.text(3.0,-0.55,"$Fe^{ikx}$",ha="center",fontsize=8.5)
ax.set_xlim(-3.2,4.6); ax.set_ylim(-0.8,2.2); ax.axis("off")
```

**(b) Electron in an infinite well.** $L = 8.5$ nm. The energy levels are $E_n = \dfrac{n^2h^2}{8mL^2}$.

$$E_1 = \frac{(6.624\times10^{-34})^2}{8\times9.1\times10^{-31}\times(8.5\times10^{-9})^2} = \frac{4.388\times10^{-67}}{5.260\times10^{-46}} = 8.34\times10^{-22}\ \text{J} = \mathbf{5.21\ meV}$$

*Radian frequency* of the ground state: $\omega_1 = E_1/\hbar$, with $\hbar = h/2\pi = 1.054\times10^{-34}$ J s:

$$\omega_1 = \frac{8.34\times10^{-22}}{1.054\times10^{-34}} = \mathbf{7.91\times10^{12}\ rad/s}\quad(f_1 = 1.26\times10^{12}\ \text{Hz})$$

*To raise the electron to the fourth level* ($n = 4$, $E_4 = 16E_1 = 1.334\times10^{-20}$ J), it must absorb the energy

$$\Delta E = E_4 - E_1 = 15E_1 = 1.251\times10^{-20}\ \text{J} = 0.0782\ \text{eV}$$

for example by absorbing a **photon** of frequency $\nu = \Delta E/h = 1.89\times10^{13}$ Hz, i.e. $\lambda = c/\nu = 15.9\ \mu\text{m}$ (far infrared), or by thermal or electrical excitation (a collision with energy of at least 0.078 eV).

@s 2
**(a) Schottky effect (image-charge method).** When an electron leaves a metal surface (work function $\phi_0$) it induces a positive charge on the metal; the attraction can be calculated as if an **image charge $+e$** were located at the same distance on the other side of the surface ($-x$). The electron at a distance $x$ outside is attracted by the image at distance $2x$:

$$F = -\frac{e^2}{4\pi\varepsilon_0(2x)^2} = -\frac{e^2}{16\pi\varepsilon_0x^2}$$

The potential energy due to the image force (work done to bring the electron from infinity to $x$) is

$$U_{im}(x) = -\int_x^{\infty}\!\!\!\frac{e^2}{16\pi\varepsilon_0x'^2}dx' = -\frac{e^2}{16\pi\varepsilon_0x}$$

An accelerating field $\mathcal{E}$ applied at the surface gives the electron an additional term $-e\mathcal{E}x$. Measured from the Fermi level, the total potential energy barrier is

$$U(x) = \phi_0 - \frac{e^2}{16\pi\varepsilon_0x} - e\mathcal{E}x$$

*The barrier has a maximum* where $dU/dx = 0$:

$$\frac{e^2}{16\pi\varepsilon_0x_m^2} = e\mathcal{E} \;\Rightarrow\; x_m = \sqrt{\frac{e}{16\pi\varepsilon_0\mathcal{E}}}$$

$$U_{max} = \phi_0 - \frac{e^2}{16\pi\varepsilon_0x_m} - e\mathcal{E}x_m = \phi_0 - 2e\mathcal{E}x_m = \phi_0 - e\sqrt{\frac{e\mathcal{E}}{4\pi\varepsilon_0}}$$

So the effective work function is **lowered** by $\Delta\phi = e\sqrt{e\mathcal{E}/4\pi\varepsilon_0}$ (Schottky lowering; for $\mathcal{E} = 10^{7}$ V/m, $\Delta\phi = 0.38$ eV). Thermionic emission follows Richardson's law with the effective work function, $J = AT^2e^{-\phi_{eff}/kT}$:

$$\boxed{J = AT^2\exp\left[-\frac{\phi_0 - e\sqrt{e\mathcal{E}/4\pi\varepsilon_0}}{kT}\right] = AT^2e^{-\phi_0/kT}\exp\left[\frac{e}{kT}\sqrt{\frac{e\mathcal{E}}{4\pi\varepsilon_0}}\right]}$$

with $A = 4\pi mek^2/h^3 = 1.2\times10^{6}$ A m$^{-2}$K$^{-2}$. The emission current thus rises with the field because the barrier becomes lower and thinner (the Schottky effect).

```figure caption="Question 2(a): Schottky effect. The image-force potential (dashed) added to the applied-field term (dotted) lowers and rounds the surface barrier from phi_0 to phi_0 - delta-phi at x_m."
fig,ax=plt.subplots(figsize=(5.4,2.9))
x=np.linspace(0.05,6,400); phi0=3.0; Uim=-0.9/x; Uf=-0.35*x; U=phi0+Uim+Uf
ax.plot(x,np.full_like(x,phi0),color=MUTED,lw=1.2,label="no field: $\\phi_0$"); ax.plot(x,phi0+Uim,color=SERIES[2],lw=1.2,ls="--",label="image force only")
ax.plot(x,phi0+Uf,color=SERIES[3],lw=1.2,ls=":",label="applied field only"); ax.plot(x,U,color=ACCENT,lw=2.2,label="total barrier")
i=np.argmax(U); ax.plot([x[i]],[U[i]],"o",color=SERIES[1]); ax.annotate("$x_m$, $\\phi_0-\\Delta\\phi$",xy=(x[i],U[i]),xytext=(x[i]+0.8,U[i]+0.5),fontsize=8.5,arrowprops=dict(arrowstyle="->",color=MUTED))
ax.axhline(0,color=INK,lw=0.8); ax.text(5.0,0.12,"Fermi level",fontsize=8); ax.set_ylim(-1.2,4.2); ax.set_xlim(0,6); ax.set_xlabel("distance x from the metal surface",fontsize=8.5); ax.set_ylabel("energy",fontsize=8.5); ax.legend(fontsize=7.2,loc="lower left"); ax.set_xticks([]); ax.set_yticks([])
```

**(b) Temperature for 30 % occupation.** $f(E) = \dfrac{1}{1 + e^{(E-E_F)/kT}} = 0.30$ at $E - E_F = 0.75$ eV:

$$e^{(E-E_F)/kT} = \frac{1}{0.30} - 1 = \frac{7}{3} \;\Rightarrow\; \frac{E - E_F}{kT} = \ln\frac{7}{3} = 0.8473$$

$$\begin{gathered}kT = \frac{0.75}{0.8473} = 0.8852\ \text{eV} \\ T = \frac{0.8852\times1.6\times10^{-19}}{1.38\times10^{-23}} = \mathbf{1.03\times10^{4}\ K\ (\approx 10\,260\ K)}\end{gathered}$$

(a very high temperature, as expected for a level well above $E_F$ to be 30 % occupied).

@s 3
**(a) Clausius-Mossotti equation (electronic polarizability).** A dielectric of $N$ atoms per unit volume, each with electronic polarizability $\alpha_e$ (dipole moment $p = \alpha_eE_{loc}$), has the polarisation

$$P = N\alpha_eE_{loc}$$

The field acting on an atom is the **Lorentz local field** (for a cubic or isotropic medium) $E_{loc} = E + \dfrac{P}{3\varepsilon_0}$. By the definition of the susceptibility, $P = \varepsilon_0(\varepsilon_r - 1)E$. Therefore

$$\varepsilon_0(\varepsilon_r - 1)E = N\alpha_e\left[E + \frac{\varepsilon_0(\varepsilon_r - 1)E}{3\varepsilon_0}\right] = N\alpha_eE\,\frac{\varepsilon_r + 2}{3}$$

$$\boxed{\frac{\varepsilon_r - 1}{\varepsilon_r + 2} = \frac{N\alpha_e}{3\varepsilon_0}}$$

This is the Clausius-Mossotti equation; it relates the macroscopic $\varepsilon_r$ to the microscopic $\alpha_e$ and is valid for non-polar dielectrics (gases, many solids, and, with $\alpha_e$ replaced by $\alpha_e + \alpha_i + \alpha_o$, polarizability in general). For optical frequencies $\varepsilon_r = n^2$ gives the Lorenz-Lorentz relation.

**(b) Dielectric loss in the glass.** $\varepsilon_r = 2.6$, $\tan\delta = 7\times10^{-5}$, $f = 1$ MHz, peak field $E_0 = 0.71$ V/m. The average power loss per unit volume is

$$P = \tfrac12\,\omega\,\varepsilon_0\varepsilon_r\tan\delta\,E_0^2 = \tfrac12\,(2\pi\times10^{6})(8.854\times10^{-12})(2.6)(7\times10^{-5})(0.71)^2$$

$$P = \mathbf{2.55\times10^{-9}\ W/m^3}\quad(\approx 2.6\ \text{nW/m}^3)$$

**(c) Dielectric loss as a function of frequency and loss tangent.** A real dielectric has a complex permittivity $\varepsilon = \varepsilon' - j\varepsilon''$, with $\varepsilon' = \varepsilon_0\varepsilon_r$ and $\varepsilon''$ the loss factor ($\tan\delta = \varepsilon''/\varepsilon'$). For the field $E = E_0e^{j\omega t}$ the current density is the sum of the conduction and displacement currents,

$$J = j\omega D = j\omega(\varepsilon' - j\varepsilon'')E = \omega\varepsilon''E + j\omega\varepsilon'E$$

The first term is in phase with $E$ (it gives the loss); the second leads $E$ by $90^\circ$ (the lossless charging current). The angle $\delta$ between the total current and the quadrature charging current is the loss angle. The average power dissipated per unit volume is

$$P = \tfrac12\mathrm{Re}(J\cdot E^*) = \tfrac12\,\omega\varepsilon''E_0^2 = \tfrac12\,\omega\,\varepsilon'\tan\delta\,E_0^2$$

$$\boxed{P = \tfrac12\,\omega\,\varepsilon_0\varepsilon_r\tan\delta\,E_0^2 = \pi f\,\varepsilon_0\varepsilon_r\tan\delta\,E_0^2 = 2\pi f\,\varepsilon_0\varepsilon_r\tan\delta\,E_{rms}^2}$$

Hence the loss per unit volume is **proportional to the frequency $f$** and to the loss tangent $\tan\delta$ (times the factor $\varepsilon_r$ and the square of the field). It is why low-loss dielectrics (small $\varepsilon_r\tan\delta$) are used in high-frequency insulation and capacitors; $\tan\delta$ itself changes with frequency, with peaks near the relaxation frequencies of orientational and ionic polarisation.

@s 4
**(a) Classification of magnetic materials.** By the response to a magnetic field (susceptibility $\chi = M/H$) and the arrangement of the atomic moments:

| Type | Behaviour of atomic moments | Susceptibility | Temperature dependence | Examples |
|---|---|---|---|---|
| **Diamagnetic** | No permanent moments; the field induces moments opposing it (Lenz's law) | Small, negative ($-10^{-5}$) | Independent of $T$ | Cu, Ag, Au, Bi, Zn, water, Si, superconductors ($\chi = -1$) |
| **Paramagnetic** | Permanent moments, randomly oriented; aligned weakly by the field against thermal agitation | Small, positive ($10^{-5}$ to $10^{-3}$) | Curie law $\chi = C/T$ | Al, Pt, Mn, O$_2$, Na |
| **Ferromagnetic** | Parallel alignment of neighbouring moments in domains by exchange interaction ($J > 0$) | Very large, positive; non-linear; hysteresis | Curie-Weiss $\chi = C/(T - T_C)$ above $T_C$ | Fe, Co, Ni, Gd |
| **Anti-ferromagnetic** | Neighbouring moments antiparallel and equal; net moment zero | Small, positive | Maximum at the Néel temperature $T_N$ | MnO, FeO, NiO, Cr |
| **Ferrimagnetic (ferrites)** | Antiparallel but **unequal** sublattice moments, so a net moment remains | Large, positive; hysteresis | Curie temperature | Fe$_3$O$_4$ (magnetite), MnFe$_2$O$_4$, NiZn ferrites, garnets |

**(b) Demagnetisation and domains.** When a ferromagnetic body is magnetised, its free poles at the ends produce a field inside the body directed opposite to the magnetisation, the **demagnetising field**

$$H_d = -N_dM$$

($N_d$ is the demagnetising factor, which depends on the shape: $1/3$ for a sphere, about 1 for a thin plate normal to the field, nearly 0 for a long rod along its axis). The magnetostatic energy $\tfrac12\mu_0N_dM^2$ stored in this field is the reason that a **single domain is unstable**: the body breaks up into **domains** with antiparallel magnetisation (two domains halve the energy, four domains quarter it) and finally **closure domains** at the ends, which carry the flux inside the material and eliminate the external field (zero demagnetising energy) at the price of the domain wall energy. The domain structure so formed (the equilibrium state) is the **demagnetised** state of the specimen, with no net moment.

*Demagnetising a magnet* means to bring the domains back into random orientation: (i) heat it above the Curie temperature, (ii) apply an alternating field of slowly decreasing amplitude (the state travels along ever smaller hysteresis loops to the origin), or (iii) apply a reverse field equal to the coercive field $H_c$; (iv) mechanical shock or vibration also helps. Hard magnets are demagnetised in storage by stray opposing fields and by their shape (a short bar has a big $N_d$, so keepers are used).

**Material for storing digital information.** A **hard magnetic material with a rectangular (square) hysteresis loop**: high remanence $B_r \approx B_s$, moderate-to-high coercivity $H_c$, a sharp switching at $H_c$ and high electrical resistivity: *ferrites* (for core memories: Mg-Mn ferrite, with the squareness ratio $B_r/B_s > 0.9$), and for tapes and disks, thin films and particles of $\gamma$-Fe$_2$O$_3$, CrO$_2$, Co-Cr-Pt alloys.

*Why:* the two stable remanent states $+B_r$ and $-B_r$ represent the bits 1 and 0, and stay without power. The squareness gives a definite state and the sharp switching at $H_c$ allows the bits to be written or read with a small current pulse and without disturbing nearby bits (half-select); a high $H_c$ prevents erasing by stray fields; a small loop area (narrow $H_c$) keeps the write energy low; and high resistivity (ferrites) avoids eddy current losses and gives fast switching.

```figure caption="Question 4(b): hysteresis loops: a square loop of a memory (storage) material, with two stable states +B_r and -B_r representing the bits 1 and 0, versus the narrow loop of a soft magnetic material."
fig,ax=plt.subplots(figsize=(4.8,2.8))
H=np.linspace(-3,3,400); sq_up=np.tanh(12*(H-0.8)); sq_dn=np.tanh(12*(H+0.8))
ax.plot(H,sq_up,color=ACCENT,lw=2); ax.plot(H,sq_dn,color=ACCENT,lw=2,label="square loop (storage)")
ax.plot(H,np.tanh(2.5*(H-0.15)),color=SERIES[2],lw=1.4); ax.plot(H,np.tanh(2.5*(H+0.15)),color=SERIES[2],lw=1.4,label="soft material")
ax.axhline(0,color=MUTED,lw=0.7); ax.axvline(0,color=MUTED,lw=0.7); ax.text(0.1,0.88,"+B$_r$ (bit 1)",fontsize=8); ax.text(0.1,-0.97,"$-$B$_r$ (bit 0)",fontsize=8); ax.text(0.85,-0.2,"H$_c$",fontsize=8)
ax.set_xlabel("H",fontsize=8.5); ax.set_ylabel("B",fontsize=8.5); ax.legend(fontsize=7.5,loc="lower right"); ax.set_xticks([]); ax.set_yticks([])
```

@s 5
**(a) Meissner effect.** A superconductor in the superconducting state ($T < T_c$ and $H < H_c$) is a **perfect diamagnet**: it expels the magnetic flux from its interior, $B = \mu_0(H + M) = 0$, so $M = -H$ and $\chi = -1$. The effect is the same whether the field is applied after cooling (as for a perfect conductor) or the specimen is cooled in a constant field (the flux is *expelled*, which a perfect conductor would not do). It is caused by surface (screening) currents that flow in a layer of thickness of the **London penetration depth** $\lambda_L$ (10 to 100 nm) and cancel the interior field. The effect shows that superconductivity is a true thermodynamic state, and it explains **magnetic levitation** (a magnet floats over a superconductor). If the field exceeds the critical field $H_c(T) = H_c(0)\left[1 - (T/T_c)^2\right]$, the superconductivity is destroyed.

**Type-I superconductors** (soft): pure elements such as Pb, Hg, Sn, Al, Zn. They show a **complete** Meissner effect up to a single critical field $H_c$ (low: 0.01 to 0.1 T); at $H_c$ the transition to the normal state is **sharp** (a first-order transition with latent heat). They cannot carry large currents or be used for strong magnets.

**Type-II superconductors** (hard): alloys and compounds (NbTi, Nb$_3$Sn, V$_3$Ga) and the high-$T_c$ ceramics (YBa$_2$Cu$_3$O$_7$). They have **two critical fields**: for $H < H_{c1}$ the Meissner state is complete; for $H_{c1} < H < H_{c2}$ the flux penetrates in the form of quantised **vortices** (flux lines, each carrying $\Phi_0 = h/2e = 2.07\times10^{-15}$ Wb) surrounded by normal cores, and the material is in the **mixed (vortex) state**, still superconducting (zero resistance); for $H > H_{c2}$ (up to 10 to 100 T) it turns normal. The transition is gradual, and the large $H_{c2}$ and critical current (with pinned vortices) make them useful for high-field magnets (MRI, NMR, accelerators, fusion).

```figure caption="Question 5(a): magnetisation curves. Type I: the Meissner state up to H_c and then an abrupt transition. Type II: Meissner state up to H_c1, mixed (vortex) state between H_c1 and H_c2, normal state above H_c2."
fig,(a1,a2)=plt.subplots(1,2,figsize=(6.0,2.3))
H=np.linspace(0,2,200); a1.plot(H,np.where(H<1,H,0),color=ACCENT,lw=2); a1.set_xticks([1]); a1.set_xticklabels(["H$_c$"]); a1.set_yticks([]); a1.set_title("type I",fontsize=9); a1.set_xlabel("H",fontsize=8.5); a1.set_ylabel("$-M$",fontsize=8.5)
H=np.linspace(0,3,300); M=np.where(H<0.7,H,np.where(H<2.4,0.7*((2.4-H)/1.7)**1.3,0)); a2.plot(H,M,color=SERIES[1],lw=2); a2.set_xticks([0.7,2.4]); a2.set_xticklabels(["H$_{c1}$","H$_{c2}$"]); a2.set_yticks([]); a2.set_title("type II",fontsize=9); a2.set_xlabel("H",fontsize=8.5); a2.text(1.2,0.5,"mixed state",fontsize=8)
```

**(b) Donors in an n-type semiconductor.** *Donors* are **pentavalent** atoms (P, As, Sb) added to pure silicon. Each substitutes a Si atom; four of its five valence electrons complete the covalent bonds with the four neighbours, while the **fifth electron is loosely bound** to the donor ion (hydrogen-like orbit with a radius enlarged and its energy reduced by $\varepsilon_r = 11.9$ and $m^*$: binding energy about 0.045 eV for P in Si). In the energy band diagram the donor creates a localised level $E_D$ just **below the conduction band** edge, $E_c - E_D \approx 0.045$ eV. At room temperature ($kT = 0.026$ eV) practically all donors are ionised: the fifth electron is excited into the conduction band, leaving behind an immobile positive donor ion; no hole is created in the valence band. So $n \approx N_D \gg n_i$ (electrons are the **majority** carriers; holes are minority carriers $p = n_i^2/N_D$) and the Fermi level moves up towards $E_c$.

```figure caption="Question 5(b): energy-band picture of an n-type semiconductor: the donor level E_D lies just below the conduction band; thermal energy lifts the loosely bound fifth electron into the conduction band."
fig,ax=plt.subplots(figsize=(4.6,2.6))
ax.fill_between([0,4],2.5,3.2,color="#dce9f8"); ax.fill_between([0,4],-0.7,0,color="#f6dcdc")
ax.text(2,2.8,"conduction band (E$_c$)",ha="center",fontsize=8); ax.text(2,-0.4,"valence band (E$_v$)",ha="center",fontsize=8)
ax.plot([1.2,2.8],[2.15,2.15],color=SERIES[1],lw=2,ls="--"); ax.text(2.9,2.1,"donor level E$_D$ (0.045 eV)",fontsize=7.5)
ax.plot([0.3,3.7],[2.35,2.35],color=SERIES[2],lw=1,ls=":"); ax.text(0.3,2.42,"E$_F$",fontsize=7.5,color=SERIES[2])
ax.annotate("",xy=(2.0,2.55),xytext=(2.0,2.15),arrowprops=dict(arrowstyle="-|>",color=INK)); ax.text(0.2,1.4,"electrons freed into E$_c$\nby thermal energy",fontsize=7.5)
ax.set_xlim(0,5.6); ax.set_ylim(-0.7,3.3); ax.axis("off")
```

*Proof of $\sigma = ne\mu_e$.* In the field $\mathcal{E}$ the conduction electrons (charge $-e$, concentration $n$) drift with the velocity $v_d = -\mu_e\mathcal{E}$ ($\mu_e$ the electron mobility). The current density is

$$J = n(-e)v_d = ne\mu_e\mathcal{E}$$

and with Ohm's law $J = \sigma\mathcal{E}$,

$$\boxed{\sigma = ne\mu_e}$$

(the hole contribution $pe\mu_h$ is negligible since $p \ll n$; in general $\sigma = e(n\mu_e + p\mu_h)$).

@s 6
**(a) Intrinsic concentration and resistivity of silicon at $T = 300$ K.** With the density-of-states effective masses $m_e^* = 1.08\,m_e$ and $m_h^* = 0.56\,m_e$:

$$\begin{gathered}N_c = 2\left(\frac{2\pi m_e^*kT}{h^2}\right)^{3/2} = 2.81\times10^{25}\ \text{m}^{-3} \\ N_v = 2\left(\frac{2\pi m_h^*kT}{h^2}\right)^{3/2} = 1.05\times10^{25}\ \text{m}^{-3}\end{gathered}$$

$$n_i = \sqrt{N_cN_v}\,\exp\left(-\frac{E_g}{2kT}\right) = \sqrt{2.81\times10^{25}\times1.05\times10^{25}}\;\exp\left(-\frac{1.1\times1.6\times10^{-19}}{2\times1.38\times10^{-23}\times300}\right)$$

$$n_i = (1.718\times10^{25})\times e^{-21.256} = \mathbf{1.01\times10^{16}\ m^{-3}} = 1.01\times10^{10}\ \text{cm}^{-3}$$

*Intrinsic conductivity and resistivity* ($\mu_n = 1350$ and $\mu_p = 450\ \text{cm}^2/\text{V s} = 0.135$ and $0.045\ \text{m}^2/\text{V s}$):

$$\sigma_i = en_i(\mu_n + \mu_p) = 1.6\times10^{-19}\times1.01\times10^{16}\times(0.135 + 0.045) = 2.91\times10^{-4}\ \text{S/m}$$

$$\rho_i = \frac{1}{\sigma_i} = \mathbf{3.44\times10^{3}\ \Omega\,m} = 3.44\times10^{5}\ \Omega\,\text{cm}$$

(the textbook value $n_i = 1.45\times10^{10}$ cm$^{-3}$ gives 2.4 $\times10^5$ Ω cm; the difference is due to the approximate effective masses and the 1.1 eV gap, since $n_i$ depends exponentially on $E_g$).

**(b) Compensated semiconductor.** $N_D = 10^{16}\ \text{cm}^{-3}$ (phosphorus), $N_A = 10^{17}\ \text{cm}^{-3}$ (boron); acceptors exceed donors, so the material becomes **p-type**. Charge neutrality, $p + N_D^+ = n + N_A^-$, with $p \gg n$:

$$p = N_A - N_D = 10^{17} - 10^{16} = \mathbf{9\times10^{16}\ cm^{-3}}$$

$$n = \frac{n_i^2}{p} = \frac{(1.45\times10^{10})^2}{9\times10^{16}} = \mathbf{2.34\times10^{3}\ cm^{-3}}$$

(holes are the majority carriers; the electrons are a minority, $n \ll p$.)

**(c) Built-in potential of a p-n junction.** When p- and n-type materials are joined, the holes diffuse from the p-side to the n-side and the electrons the other way, leaving behind the fixed ionised acceptors ($N_A^-$) and donors ($N_D^+$) and forming a **depletion region** with an electric field. In equilibrium the diffusion and drift currents cancel for each carrier, the Fermi level is constant through the junction, and the energy bands bend by $eV_0$: $V_0$ is the built-in (contact) potential.

*Derivation.* For electrons the net current is zero:

$$J_n = en\mu_n\mathcal{E} + eD_n\frac{dn}{dx} = 0 \;\Rightarrow\; \mathcal{E} = -\frac{D_n}{\mu_n}\frac{1}{n}\frac{dn}{dx}$$

With the Einstein relation $D_n/\mu_n = kT/e$ and $\mathcal{E} = -dV/dx$:

$$\frac{dV}{dx} = \frac{kT}{e}\frac{1}{n}\frac{dn}{dx} \;\Rightarrow\; \int_{p\text{-side}}^{n\text{-side}}dV = \frac{kT}{e}\int_{n_{p0}}^{n_{n0}}\frac{dn}{n}$$

$$V_0 = \frac{kT}{e}\ln\frac{n_{n0}}{n_{p0}}$$

On the n-side, far from the junction, $n_{n0} = N_D$; on the p-side the minority-electron density is $n_{p0} = n_i^2/N_A$. Therefore

$$\boxed{V_0 = \frac{kT}{e}\ln\frac{N_AN_D}{n_i^2}}$$

The same result follows from the holes ($V_0 = (kT/e)\ln(p_{p0}/p_{n0})$) or from the difference of the Fermi levels, $eV_0 = E_{Fn} - E_{Fp}$ before contact. *Example:* $N_A = 10^{17}$, $N_D = 10^{16}$ cm$^{-3}$ and $n_i = 1.45\times10^{10}$ cm$^{-3}$ at 300 K give $V_0 = 0.02588\times\ln(4.75\times10^{12}) = 0.755$ V. $V_0$ increases with doping and falls with temperature (about $-2$ mV/K); it cannot be measured with a voltmeter, but it sets the forward turn-on voltage (about 0.7 V for Si).

```figure caption="Question 6(c): energy-band diagram of a p-n junction in equilibrium: the Fermi level is flat and the bands bend by the built-in potential eV_0."
fig,ax=plt.subplots(figsize=(5.4,2.7))
x=np.linspace(-3,3,300); s=1/(1+np.exp(-3*x)); Ec=2.2-1.0*s*1.0+0.0; Ec=2.6-1.2*s; Ev=Ec-1.1
ax.plot(x,Ec,color=ACCENT,lw=2); ax.plot(x,Ev,color=SERIES[1],lw=2); ax.axhline(1.55,color=SERIES[2],lw=1.2,ls="--")
ax.text(-2.9,Ec[0]+0.12,"E$_c$",fontsize=8.5); ax.text(-2.9,Ev[0]-0.3,"E$_v$",fontsize=8.5); ax.text(2.6,1.62,"E$_F$",fontsize=8.5,color=SERIES[2])
ax.annotate("",xy=(0.0,1.48),xytext=(0.0,0.0+1.9-0.3),arrowprops=dict(arrowstyle="<->",color=MUTED)); ax.text(0.15,1.72,"eV$_0$",fontsize=9)
ax.text(-2.2,0.35,"p-type",fontsize=9); ax.text(1.6,0.35,"n-type",fontsize=9); ax.text(-0.45,3.0,"depletion region",fontsize=8,color=MUTED)
ax.axvspan(-0.8,0.8,color="#eeeeee",alpha=0.6,zorder=0); ax.set_xlim(-3,3); ax.set_ylim(-0.2,3.3); ax.axis("off")
```
