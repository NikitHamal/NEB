---
file: NEBians-IOE-Past-Paper-Electrical-Engineering-Material-ENEE203-2082-Kartik.pdf
subject: Electrical Engineering Material
level: BE · Year II / Part I
code: ENEE 203
year_bs: 2082 Kartik
cal: BS
year_ad: 2025
stream: BEL
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Back paper (new course), BE Electrical Engineering (BEL), Year II / Part I. Full marks 60, pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

Constants: $m_e = 9.1\times10^{-31}$ kg; $h = 6.624\times10^{-34}$ J s; $n_i = 1.45\times10^{10}\ \text{cm}^{-3}$ for Si; $\mu_n = 1350\ \text{cm}^2\text{V}^{-1}\text{s}^{-1}$ (300 K); $\mu_h = 450\ \text{cm}^2\text{V}^{-1}\text{s}^{-1}$ (300 K); 1 eV $= 1.6\times10^{-19}$ J; $k = 1.38\times10^{-23}$ J/K; $N_A = 6.022\times10^{23}$/mol; permittivity of silicon $\varepsilon = \varepsilon_0\varepsilon_r = 11.9\times8.85\times10^{-12}$ F/m; velocity of light $= 3\times10^{8}$ m/s; mass of photon $= 1.673\times10^{-27}$ kg.

@q 1
(a) Explain the concept of effective mass in crystal with necessary mathematical expression and diagrams. [[5]]

(b) In the photoelectric experiment, green light, with a wavelength of 522 nm is the longest wavelength radiation that can cause photoemission of electron from a clean sodium surface. Calculate the work function of sodium. If ultraviolet radiation with a wavelength of 250 nm is incident to the sodium surface, what will be the kinetic energy of the photo-emitted electrons? [[3]]

@q 2
(a) Explain the formation of H$_2$ molecule using molecular orbital bonding theory and draw the necessary diagrams. [[6]]

(b) For a given Fermi energy level $E_F$, show that the probability of emptying energy level $kT$ below $E_F$ is equal to probability of occupying level $kT$ above $E_F$. [[4]]

@q 3
(a) Define local field in relation to polarization. Derive the Clausius-Mossotti Equation for ionic polarization, relating polarizability with the permittivity. [[4]]

(b) Explain how? If the spacing between parallel plates of a capacitor is less, the dielectric breakdown will occur soon. [[2]]

(c) What do you mean by piezo-electric materials? Explain piezoelectric effect in terms of polarization. [[4]]

@q 4
(a) Distinguish between ferromagnetic and anti-ferromagnetic materials with suitable examples of each. Explain magnetostriction with neat diagram. [[5]]

(b) Explain the domain theory of magnetism in detail. [[5]]

@q 5
(a) How does Meissner effect help to differentiate superconductor as type-I and type-II? Explain in brief. Explain critical current in superconductor with necessary mathematical expression and diagram. [[6]]

(b) Explain how acceptor dopants contribute holes in valence band in p-type extrinsic semiconductor. Also prove that $\sigma = pe\mu_h$ where symbols have their usual meanings. [[4]]

@q 6
(a) Calculate the resistance of pure silicon cubic crystal of 1 cm$^3$ at room temperature. What will be the resistance of the cube when it is doped with 1 arsenic in $10^9$ silicon atoms and 1 boron atom per billion silicon atoms? Atomic concentration of silicon is $5\times10^{22}\ \text{cm}^{-3}$, $n_i = 1.45\times10^{10}\ \text{cm}^{-3}$. [[4]]

(b) Calculate the diffusion coefficient of electrons at 300 K in n-type silicon semiconductor with $10^{15}$ arsenic atoms per cm$^3$. ($\mu = 1300\ \text{cm}^2\text{V}^{-1}\text{s}^{-1}$) [[3]]

(c) Explain the diffusion process in semiconductor and derive the Einstein relation for diffusion process. [[5]]

<!-- SOLUTIONS -->

@s 1
**(a) Effective mass.** An electron in a crystal moves in the periodic potential of the lattice, so it does not obey $E = \hbar^2k^2/2m_e$ with the free-electron mass. Its energy depends on the wave vector, $E(k)$, and near a band edge it can still be described as a *free particle with a modified mass*, the **effective mass** $m^*$.

For a free electron $E = \hbar^2k^2/2m$ gives $d^2E/dk^2 = \hbar^2/m$. By analogy, for a crystal electron

$$\boxed{m^* = \frac{\hbar^2}{d^2E/dk^2}}$$

*Derivation.* The group velocity of the wave packet is $v_g = \dfrac{1}{\hbar}\dfrac{dE}{dk}$. Under an electric field $\mathcal{E}$ the force is $F = -e\mathcal{E} = \hbar\,dk/dt$, so the acceleration is

$$a = \frac{dv_g}{dt} = \frac{1}{\hbar}\frac{d^2E}{dk\,dt} = \frac{1}{\hbar}\frac{d^2E}{dk^2}\frac{dk}{dt} = \frac{1}{\hbar^2}\frac{d^2E}{dk^2}F$$

Comparing with Newton's law $F = m^*a$ gives the expression above.

*Meaning.* $m^*$ is inversely proportional to the curvature of the $E$-$k$ curve: at the bottom of the conduction band the curvature is positive, so $m^* > 0$ (a sharply curved, narrow-band curve means a light electron; a flat, wide-band curve a heavy one). At the top of the valence band the curvature is negative so $m^* < 0$, which is why a missing electron behaves as a **hole** of positive effective mass $m_h^* = -m^*$ and charge $+e$. In silicon $m_e^* \approx 1.08\,m_e$ and $m_h^* \approx 0.56\,m_e$; in GaAs $m_e^* \approx 0.067\,m_e$. $m^*$ includes the effect of the lattice forces, so that the electron can be treated as free.

```figure caption="Question 1(a): E-k diagram of a semiconductor. Near the conduction band minimum (E_c) the curvature is positive and m* > 0; near the valence band maximum (E_v) the curvature is negative and the missing electron behaves as a hole. The smaller the curvature, the heavier the carrier."
fig,ax=plt.subplots(figsize=(5.6,3.0))
k=np.linspace(-1,1,300); ax.plot(k,1.5+1.6*k**2,color=ACCENT,lw=2.2,label="conduction band: $m^*>0$ (d$^2$E/dk$^2$ > 0)")
ax.plot(k,-1.2*k**2,color=SERIES[1],lw=2.2,label="valence band: $m^*<0$ (d$^2$E/dk$^2$ < 0)")
ax.plot(k,1.5+0.5*k**2,color=ACCENT,lw=1.2,ls="--",label="flatter band: larger $m^*$")
ax.axhline(1.5,color=GRID,lw=0.8); ax.axhline(0,color=GRID,lw=0.8); ax.text(0.62,0.7,"E$_g$",fontsize=9); ax.annotate("",xy=(0.55,1.5),xytext=(0.55,0),arrowprops=dict(arrowstyle="<->",color=MUTED))
ax.set_xlabel("wave vector k",fontsize=8.5); ax.set_ylabel("energy E",fontsize=8.5); ax.legend(fontsize=7.3,loc="upper center"); ax.set_xticks([]); ax.set_yticks([]); ax.set_ylim(-1.5,4.6)
```

**(b) Work function of sodium.** The longest wavelength that causes emission is the threshold wavelength $\lambda_0 = 522$ nm, at which the photon energy equals the work function:

$$\phi = \frac{hc}{\lambda_0} = \frac{6.624\times10^{-34}\times3\times10^{8}}{522\times10^{-9}} = 3.807\times10^{-19}\ \text{J} = \mathbf{2.38\ eV}$$

For $\lambda = 250$ nm:

$$E_{ph} = \frac{hc}{\lambda} = \frac{1.9872\times10^{-25}}{250\times10^{-9}} = 7.949\times10^{-19}\ \text{J} = 4.968\ \text{eV}$$

$$KE_{max} = E_{ph} - \phi = 4.968 - 2.379 = \mathbf{2.59\ eV} = 4.14\times10^{-19}\ \text{J}$$

(the speed of the fastest photoelectron is $\sqrt{2KE/m_e} = 0.95\times10^{6}$ m/s).

@s 2
**(a) Formation of H$_2$ by molecular orbital theory.** In the MO theory the atomic orbitals of the combining atoms overlap to form molecular orbitals (MOs) spread over the whole molecule (LCAO: linear combination of atomic orbitals). The number of MOs equals the number of AOs.

Two hydrogen atoms each have one 1s electron ($\psi_A$, $\psi_B$). They combine in two ways:

$$\begin{gathered}\psi_{\sigma} = \frac{1}{\sqrt2}\left(\psi_A + \psi_B\right) \quad(\text{bonding, in-phase}) \\ \psi_{\sigma^*} = \frac{1}{\sqrt2}\left(\psi_A - \psi_B\right) \quad(\text{antibonding, out-of-phase})\end{gathered}$$

- The **bonding MO** $\sigma_{1s}$: constructive overlap, electron density is concentrated *between* the nuclei, so the energy is **lower** than that of the atomic orbitals (stable).
- The **antibonding MO** $\sigma^*_{1s}$: destructive overlap with a node between the nuclei, **higher** energy.

*Filling.* The two electrons (Aufbau, Pauli, Hund) occupy the lower MO with opposite spins: $(\sigma_{1s})^2$. 

$$\text{Bond order} = \frac{N_b - N_a}{2} = \frac{2 - 0}{2} = 1$$

so H$_2$ is stable with a single bond (bond length 74 pm, bond energy 436 kJ/mol), and it is diamagnetic (no unpaired electron). The same scheme shows why He$_2$ does not exist (bond order $(2-2)/2 = 0$), and H$_2^+$ (bond order 0.5) exists weakly.

```figure caption="Question 2(a): molecular-orbital energy-level diagram of H2: the two 1s atomic orbitals form a bonding sigma(1s) and an antibonding sigma*(1s) orbital; the two electrons fill the bonding orbital (bond order 1)."
fig,ax=plt.subplots(figsize=(5.4,3.1))
for x0,l in ((0,"H (1s)"),(4,"H (1s)")):
    ax.plot([x0,x0+1.2],[2,2],color=INK,lw=2); ax.text(x0+0.6,1.6,l,ha="center",fontsize=8.5)
ax.plot([0.6+0.0,0.6+0.0],[2,2],lw=0)
ax.text(0.15,2.17,"$\\uparrow$",fontsize=14); ax.text(4.15,2.17,"$\\downarrow$",fontsize=14)
ax.plot([2,3.2],[0.6,0.6],color=ACCENT,lw=2.4); ax.plot([2,3.2],[3.4,3.4],color=SERIES[1],lw=2.4)
ax.text(2.45,0.78,"$\\uparrow\\downarrow$",fontsize=14,color=ACCENT); ax.text(3.35,0.5,"$\\sigma_{1s}$ bonding",fontsize=8.5,color=ACCENT); ax.text(3.35,3.3,"$\\sigma^*_{1s}$ antibonding",fontsize=8.5,color=SERIES[1])
for a,b,y in ((1.2,2.0,0.6),(1.2,2.0,3.4),(4.0,3.2,0.6),(4.0,3.2,3.4)):
    ax.plot([a,b],[2,y],color=MUTED,lw=0.9,ls="--")
ax.set_xlim(-0.2,6.4); ax.set_ylim(0,4.1); ax.set_ylabel("energy",fontsize=8.5); ax.set_xticks([]); ax.set_yticks([])
for s in ("top","right","bottom"): ax.spines[s].set_visible(False)
```

**(b) Symmetry of the Fermi function.** The Fermi-Dirac probability of occupation is $f(E) = \dfrac{1}{1 + e^{(E-E_F)/kT}}$.

*Probability that a level $kT$ above $E_F$ is occupied:*

$$f(E_F + kT) = \frac{1}{1 + e^{1}} = \frac{1}{1 + e} = 0.269$$

*Probability that a level $kT$ below $E_F$ is empty* $= 1 - f(E_F - kT)$:

$$\begin{gathered}f(E_F - kT) = \frac{1}{1 + e^{-1}} \\ 1 - f(E_F - kT) = \frac{e^{-1}}{1 + e^{-1}} = \frac{1}{e + 1} = 0.269\end{gathered}$$

Hence $1 - f(E_F - kT) = f(E_F + kT)$: **proved.** In general $1 - f(E_F - \Delta) = f(E_F + \Delta)$, so the probability of finding a hole $\Delta$ below $E_F$ equals the probability of an electron $\Delta$ above it, which is why $E_F$ lies at the middle of the gap in an intrinsic semiconductor (symmetry of $f$ about $E_F$).

@s 3
**(a) Local field and Clausius-Mossotti equation.** The **local (internal) field** $E_{loc}$ is the *actual field acting on an atom or ion* inside the dielectric: it is the applied (Maxwell) field $E$ plus the field from all the other polarised dipoles. It differs from $E$, and the polarisation of a dipole is $\mu = \alpha E_{loc}$ ($\alpha$ the polarizability).

*Lorentz local field.* Consider a spherical cavity round the atom: $E_{loc} = E + E_1 + E_2 + E_3$, where $E_1 = P/\varepsilon_0$... more simply $E_1$ (depolarising field of the outer surface) $+ E_2$ (Lorentz cavity field $= P/3\varepsilon_0$) $+ E_3$ (the field of the dipoles inside the cavity, $= 0$ for a cubic or isotropic lattice). Combining $E_1$ with the applied field into the Maxwell field $E$:

$$E_{loc} = E + \frac{P}{3\varepsilon_0}$$

*Derivation.* With $N$ atoms (or ion pairs) per unit volume,

$$\begin{gathered}P = N\alpha E_{loc} = N\alpha\left(E + \frac{P}{3\varepsilon_0}\right) \\ P = \varepsilon_0(\varepsilon_r - 1)E\end{gathered}$$

Eliminating $E$:

$$\varepsilon_0(\varepsilon_r - 1)E = N\alpha E + \frac{N\alpha}{3\varepsilon_0}\varepsilon_0(\varepsilon_r - 1)E \;\Rightarrow\; (\varepsilon_r - 1)\left(1 - \frac{N\alpha}{3\varepsilon_0}\right) = \frac{N\alpha}{\varepsilon_0}$$

$$\boxed{\frac{\varepsilon_r - 1}{\varepsilon_r + 2} = \frac{N\alpha}{3\varepsilon_0}}$$

This is the Clausius-Mossotti equation. For an **ionic** crystal $\alpha$ is the sum of the electronic and the ionic polarizabilities, $\alpha = \alpha_e + \alpha_i$ (orientational term absent). The ionic polarizability follows from the relative displacement $x$ of the positive and negative ions, with restoring force $K x$ and natural frequency $\omega_0$:

$$qE_{loc} = Kx = \mu_r\omega_0^2x,\quad \mu_r = \frac{m_+m_-}{m_+ + m_-}\;\Rightarrow\; \alpha_i = \frac{qx}{E_{loc}} = \frac{q^2}{\mu_r\omega_0^2}$$

so that $\dfrac{\varepsilon_r - 1}{\varepsilon_r + 2} = \dfrac{N}{3\varepsilon_0}\left(\alpha_e + \dfrac{q^2}{\mu_r\omega_0^2}\right)$.

**(b) Spacing and breakdown.** For a potential difference $V$ across the plates spaced by $d$, the field in the dielectric is $E = V/d$. Dielectric breakdown happens when the field exceeds the **dielectric strength** $E_{bd}$ of the material (the field at which electrons are accelerated and ionise atoms, an avalanche). Thus the breakdown voltage is $V_{bd} = E_{bd}\,d$. If $d$ is small, the same applied voltage gives a larger field $E = V/d$, which reaches $E_{bd}$ at a **lower voltage**; hence the breakdown occurs sooner. (Example: air with $E_{bd} = 3$ MV/m breaks down at 3 kV for $d = 1$ mm but at 300 V for $d = 0.1$ mm.)

**(c) Piezoelectric materials.** A piezoelectric material generates a **polarisation (surface charge) when mechanical stress is applied** (the direct effect) and, conversely, is **strained when an electric field is applied** (converse effect). Examples: quartz, Rochelle salt, barium titanate, lead zirconate titanate (PZT), PVDF, ZnO.

*In terms of polarisation.* A piezoelectric crystal has **no centre of symmetry**. Without stress, the centres of positive and negative charge of every unit cell coincide (net dipole moment zero, as in quartz with its three-fold arrangement of SiO$_2$ units). A stress deforms the lattice and the ions are displaced relatively, so the charge centres no longer coincide: each cell gets a dipole moment and a net **polarisation** $P$ appears along a polar axis, with equal and opposite bound charges on opposite faces. For small stress

$$\begin{gathered}P = d\,\sigma\quad(\text{C/m}^2) \\ \text{with } d\ \text{the piezoelectric coefficient (C/N)}\end{gathered}$$

The polarisation reverses when compression changes to tension; the converse effect gives the strain $S = d\,\mathcal{E}$, so an alternating field makes the crystal vibrate (resonance at the natural frequency). *Uses:* quartz crystal oscillators and filters, microphones and pick-ups, ultrasound transducers, sonar, igniters (lighters), strain/force/accelerometer sensors, actuators and energy harvesting.

@s 4
**(a) Ferromagnetic versus anti-ferromagnetic materials.**

| Property | Ferromagnetic | Anti-ferromagnetic |
|---|---|---|
| Atomic moments | Neighbouring spins aligned **parallel** (exchange integral $J > 0$) | Neighbouring spins aligned **antiparallel** and equal ($J < 0$), two interpenetrating sublattices |
| Net magnetisation | Large spontaneous magnetisation in domains | **Zero** (moments cancel) |
| Susceptibility | Very large, positive ($10^2$ to $10^5$) | Small, positive |
| Critical temperature | Curie temperature $T_C$ ; above it paramagnetic ($\chi = C/(T - T_C)$) | Néel temperature $T_N$ ; above it paramagnetic ($\chi = C/(T + \theta)$), $\chi$ has a maximum at $T_N$ |
| Hysteresis | Yes | No |
| Examples | Fe ($T_C$ = 1043 K), Co, Ni, Gd | MnO ($T_N$ = 122 K), FeO, NiO, Cr, MnF$_2$ |

**Magnetostriction.** When a ferromagnetic material is magnetised, its **dimensions change** (it elongates or shortens in the direction of magnetisation) although its volume stays about constant. The strain $\lambda = \Delta l/l$ (saturation value $10^{-5}$ to $10^{-4}$: nickel is negative ($-35\times10^{-6}$), iron is positive at low field) arises because the magnetic domains rotate and the crystal lattice is distorted by the coupling between spin and lattice (spin-orbit). Conversely, stress changes the magnetisation (Villari effect). Magnetostriction explains the hum of transformers (twice the line frequency). *Uses:* ultrasonic generators (nickel, Terfenol-D), sonar, delay lines, precision actuators and torque sensors.

```figure caption="Question 4(a): magnetostriction. In the demagnetised state the domains point in random directions; on magnetising along the horizontal axis they rotate or grow, the lattice distorts, and the rod lengthens by delta-l (positive magnetostriction)."
fig,(a1,a2)=plt.subplots(1,2,figsize=(6.2,2.1))
def rod(ax,L,title,arrows):
    ax.add_patch(Rectangle((0,0),L,1.0,fc="#eaf1fb",ec=ACCENT,lw=1.6))
    for (x,y,dx,dy) in arrows: ax.annotate("",xy=(x+dx,y+dy),xytext=(x,y),arrowprops=dict(arrowstyle="-|>",color=SERIES[1],lw=1.6))
    ax.set_title(title,fontsize=8.5); ax.set_xlim(-0.3,5.3); ax.set_ylim(-0.6,1.5); ax.set_aspect("equal"); ax.axis("off")
rod(a1,4.0,"unmagnetised: random domains",[(0.8,0.5,0.0,0.3),(1.8,0.5,0.25,0.0),(2.8,0.5,0.0,-0.3),(3.3,0.5,-0.25,0.0)])
rod(a2,4.5,"magnetised: aligned, elongated by $\\Delta l$",[(0.7,0.5,0.6,0.0),(1.9,0.5,0.6,0.0),(3.1,0.5,0.6,0.0)])
a2.annotate("",xy=(4.5,-0.3),xytext=(4.0,-0.3),arrowprops=dict(arrowstyle="<->",color=MUTED)); a2.text(4.25,-0.55,"$\\Delta l$",fontsize=8.5,ha="center")
```

**(b) Domain theory of magnetism (Weiss).** In 1907 Weiss proposed that a ferromagnetic crystal, even when unmagnetised, is divided into small regions of about $10^{-6}$ to $10^{-3}$ cm in size, the **domains**, each of which is **spontaneously magnetised to saturation** because the exchange interaction (a quantum effect, between neighbouring electron spins) aligns the atomic moments, below $T_C$. The direction of magnetisation is different in different domains so that the net magnetisation of the specimen is zero.

*Why domains form:* the total energy of the specimen is minimised. A single domain would have a large external field (magnetostatic energy $\sim\frac12\int B\cdot H\,dV$); splitting into many antiparallel domains, and finally closure domains with the flux fully contained, reduces it. The splitting stops when the energy needed to create a **domain (Bloch) wall** (a transition region about 100 nm where the spins rotate gradually from one direction to the other, with the exchange and anisotropy energy as cost) equals the gain.

Energies involved: exchange energy (aligns spins), magnetostatic energy, **magnetocrystalline anisotropy** energy (easy axes, e.g. $\langle100\rangle$ in iron), **magnetostrictive** energy, domain-wall energy.

*Magnetisation process (B-H curve).* (1) At low field (weak): **domain-wall motion**, reversible, domains with the favourable direction grow at the cost of the others. (2) At medium field: irreversible wall motion (Barkhausen jumps) which gives the steep part and the hysteresis. (3) At high field: **domain rotation** to the field direction, up to saturation $M_s$ (a single domain). When the field is removed, wall motion is impeded by impurities and defects, so a **remanence** $B_r$ stays, and the coercive field $H_c$ is needed to remove it, giving the hysteresis loop (the area of the loop is the energy loss per cycle per unit volume). Above the Curie temperature the thermal energy destroys the alignment and the material is paramagnetic. The theory explains why a piece of iron is not a magnet by itself, saturation, hysteresis, and the difference of soft (easy wall motion, small loop: transformer cores) from hard (pinned walls, wide loop: permanent magnets) materials.

```figure caption="Question 4(b): (left) domain arrangements that reduce the magnetostatic energy: single domain, two domains and closure domains; (right) magnetisation curve with its three stages and the hysteresis loop (B_r remanence, H_c coercivity)."
fig,(a1,a2,a3,a4)=plt.subplots(1,4,figsize=(6.6,1.9),gridspec_kw={"width_ratios":[1,1,1,1.7]})
def sq(ax,t,pat):
    ax.add_patch(Rectangle((0,0),2,2,fc="white",ec=INK,lw=1.4)); ax.set_title(t,fontsize=7.5)
    for (x,y,dx,dy) in pat: ax.annotate("",xy=(x+dx,y+dy),xytext=(x,y),arrowprops=dict(arrowstyle="-|>",color=SERIES[1],lw=1.4))
    ax.set_xlim(-0.2,2.2); ax.set_ylim(-0.2,2.2); ax.set_aspect("equal"); ax.axis("off")
sq(a1,"single domain\n(large field)",[(0.4,1.0,1.2,0)])
a2.plot([1,1],[0,2],color=MUTED,lw=1.2); sq(a2,"two domains",[(0.4,1.4,1.2,0),(1.6,0.6,-1.2,0)])
sq(a3,"closure domains",[(0.3,1.5,1.4,0),(1.7,0.5,-1.4,0),(0.3,0.5,0,0.9),(1.7,1.5,0,-0.9)])
H=np.linspace(-3,3,300); up=np.tanh(2*(H-0.6)); dn=np.tanh(2*(H+0.6))
a4.plot(H,up,color=ACCENT,lw=1.6); a4.plot(H,dn,color=ACCENT,lw=1.6); a4.plot(np.linspace(0,3,100),np.tanh(2*(np.linspace(0,3,100)+0.0))*0.8,color=SERIES[2],lw=1,ls="--")
a4.axhline(0,color=MUTED,lw=0.7); a4.axvline(0,color=MUTED,lw=0.7); a4.text(0.1,0.7,"B$_r$",fontsize=8); a4.text(0.65,-0.18,"H$_c$",fontsize=8); a4.text(1.2,0.25,"virgin curve",fontsize=7,color=SERIES[2])
a4.set_xlabel("H",fontsize=8); a4.set_ylabel("B",fontsize=8); a4.set_xticks([]); a4.set_yticks([])
```

@s 5
**(a) Meissner effect and the two types of superconductor.** When a superconductor is cooled below its critical temperature $T_c$ in a magnetic field, it **expels the magnetic flux** from its interior ($B = 0$, perfect diamagnetism, $\chi = -1$), independently of whether the field was applied before or after cooling. This is the Meissner effect: it proves that a superconductor is not just a perfect conductor (for which $B$ would stay frozen at its value). Surface screening currents flow within the **London penetration depth** $\lambda_L \approx 10$ to $100$ nm and cancel the interior field.

The way the Meissner state breaks down when the field is raised differentiates the two types:

| | Type I (soft) | Type II (hard) |
|---|---|---|
| $M$-$H$ behaviour | Complete Meissner effect up to one critical field $H_c$, then an **abrupt** transition to the normal state | Complete Meissner effect only up to the **lower critical field $H_{c1}$**; between $H_{c1}$ and $H_{c2}$ the flux partly penetrates (**vortex / mixed state**); above the **upper critical field $H_{c2}$** the material is normal |
| Critical fields | Low ($H_c \lesssim 0.1$ T) | $H_{c2}$ very high (10 to 100 T) |
| Examples | Pure metals: Al, Pb, Hg, Sn, Zn | Alloys and compounds: Nb$_3$Sn, NbTi, YBCO, high-$T_c$ ceramics |
| Uses | Little (low fields) | Magnets (MRI, accelerators), cables |

The critical field varies with temperature as $H_c(T) = H_c(0)\left[1 - (T/T_c)^2\right]$.

```figure caption="Question 5(a): magnetisation M versus applied field H. Type I: perfect diamagnetism up to H_c, then an abrupt loss of superconductivity. Type II: complete expulsion up to H_c1, a mixed (vortex) state up to H_c2, then the normal state."
fig,(a1,a2)=plt.subplots(1,2,figsize=(6.2,2.4))
H=np.linspace(0,2,200); a1.plot(H,np.where(H<1,-H,0),color=ACCENT,lw=2); a1.axvline(1,color=GRID,ls=":"); a1.set_xticks([1]); a1.set_xticklabels(["H$_c$"]); a1.set_yticks([]); a1.set_title("type I",fontsize=9); a1.set_xlabel("H",fontsize=8.5); a1.set_ylabel("$-M$",fontsize=8.5)
H=np.linspace(0,3,300); M=np.where(H<0.7,H,np.where(H<2.4,0.7*((2.4-H)/(2.4-0.7))**1.3,0)); a2.plot(H,M,color=SERIES[1],lw=2); a2.axvline(0.7,color=GRID,ls=":"); a2.axvline(2.4,color=GRID,ls=":"); a2.set_xticks([0.7,2.4]); a2.set_xticklabels(["H$_{c1}$","H$_{c2}$"]); a2.set_yticks([]); a2.set_title("type II",fontsize=9); a2.set_xlabel("H",fontsize=8.5); a2.text(1.1,0.55,"vortex\nstate",fontsize=8)
```

**Critical current.** A superconductor can carry current without resistance only up to a **critical current** $I_c$ (critical current density $J_c$). Above it, the magnetic field of the current itself exceeds the critical field, and superconductivity is destroyed (**Silsbee's rule**). For a long straight wire of radius $r$ the field at the surface is $H = I/2\pi r$, so setting $H = H_c$:

$$\boxed{I_c = 2\pi r\,H_c(T) = 2\pi r\,H_c(0)\left[1 - \frac{T^2}{T_c^2}\right]}$$

and $J_c = I_c/\pi r^2 = 2H_c/r$. $I_c$ is zero at $T = T_c$ and maximum at $T = 0$; the same applies for an applied field, as the sum of the self-field and applied field must not exceed $H_c$. Thus the superconducting state exists only below the critical *surface* in the $(T, H, J)$ space. For type II wires $J_c$ is limited by the pinning of the vortices (flux flow gives resistance), and it falls with the field.

```figure caption="Question 5(a): critical current of a superconducting wire falls parabolically with temperature (Silsbee's rule I_c = 2 pi r H_c(T)); the superconducting state exists inside the curve."
fig,ax=plt.subplots(figsize=(4.4,2.4))
T=np.linspace(0,1,100); ax.plot(T,1-T**2,color=ACCENT,lw=2); ax.fill_between(T,0,1-T**2,color=ACCENT,alpha=0.12)
ax.text(0.3,0.35,"superconducting",fontsize=9); ax.text(0.75,0.8,"normal",fontsize=9)
ax.set_xticks([0,1]); ax.set_xticklabels(["0","T$_c$"]); ax.set_yticks([1]); ax.set_yticklabels(["I$_c$(0)"]); ax.set_xlabel("temperature",fontsize=8.5); ax.set_ylabel("critical current",fontsize=8.5)
```

**(b) Acceptor doping and conductivity of a p-type semiconductor.** *Acceptors* are **trivalent** atoms (B, Al, Ga, In) added to pure silicon. Each such atom replaces a silicon atom but has only three valence electrons, so one of its four covalent bonds is **incomplete**. A valence electron from a neighbouring Si-Si bond needs only a very small energy (0.045 eV for B in Si, much less than $E_g = 1.1$ eV) to fill this bond, which leaves a vacant electron state, a **hole**, in the valence band. In the band picture, the acceptor creates a localised energy level $E_A$ just above the valence band edge $E_v$ ($E_A - E_v \approx 0.045$ eV); at room temperature the thermal energy $kT = 0.026$ eV ionises practically all acceptors: electrons jump from the valence band to $E_A$ (the acceptor becomes a negative immobile ion), and **mobile holes** are left in the valence band. Hence $p \approx N_A \gg n_i$, the holes are the **majority** carriers, electrons the minority carriers ($n = n_i^2/N_A$), and the Fermi level moves down towards $E_v$.

```figure caption="Question 5(b): energy-band picture of a p-type semiconductor: acceptor level E_A just above the valence band; thermal energy lifts valence electrons into E_A, leaving holes in the valence band."
fig,ax=plt.subplots(figsize=(4.6,2.6))
ax.fill_between([0,4],2.5,3.2,color="#dce9f8"); ax.fill_between([0,4],-0.7,0,color="#f6dcdc")
ax.text(2,2.8,"conduction band (E$_c$)",ha="center",fontsize=8); ax.text(2,-0.4,"valence band (E$_v$)",ha="center",fontsize=8)
ax.plot([1.2,2.8],[0.35,0.35],color=SERIES[1],lw=2,ls="--"); ax.text(2.9,0.3,"acceptor level E$_A$ (0.045 eV)",fontsize=7.5)
ax.plot([0.3,3.7],[0.15,0.15],color=SERIES[2],lw=1,ls=":"); ax.text(3.0,0.55,"E$_F$",fontsize=7.5,color=SERIES[2])
ax.annotate("",xy=(2.0,0.35),xytext=(2.0,0.0),arrowprops=dict(arrowstyle="-|>",color=INK)); ax.text(1.0,-0.05,"holes $\\oplus$ left in E$_v$",fontsize=7.5)
ax.set_xlim(0,5.6); ax.set_ylim(-0.7,3.3); ax.axis("off")
```

*Proof of $\sigma = pe\mu_h$.* In an electric field $\mathcal{E}$, holes (charge $+e$, concentration $p$) acquire the drift velocity $v_d = \mu_h\mathcal{E}$, where $\mu_h$ is the hole mobility. The current density is the charge crossing unit area per second:

$$J = p\,e\,v_d = pe\mu_h\mathcal{E}$$

Ohm's law in point form is $J = \sigma\mathcal{E}$, so

$$\boxed{\sigma = pe\mu_h}$$

(for a p-type semiconductor $p \gg n$ so the electron term $ne\mu_e$ is negligible; in general $\sigma = e(n\mu_e + p\mu_h)$). The resistivity is $\rho = 1/pe\mu_h$.

@s 6
**(a) Resistance of the silicon cube** (1 cm$^3$, i.e. $l = 1$ cm, $A = 1\ \text{cm}^2$).

*Pure (intrinsic) silicon:* $n = p = n_i = 1.45\times10^{10}\ \text{cm}^{-3}$:

$$\sigma_i = en_i(\mu_n + \mu_h) = 1.6\times10^{-19}\times1.45\times10^{10}\times(1350 + 450) = 4.176\times10^{-6}\ \text{S/cm}$$

$$\begin{gathered}\rho_i = 2.395\times10^{5}\ \Omega\,\text{cm} \\ R = \rho\frac{l}{A} = 2.395\times10^{5}\times\frac{1}{1} = \mathbf{2.39\times10^{5}\ \Omega}\end{gathered}$$

*Doped with 1 As atom in $10^9$ Si atoms and 1 B atom per $10^9$ Si atoms:*

$$\begin{gathered}N_D = \frac{5\times10^{22}}{10^{9}} = 5\times10^{13}\ \text{cm}^{-3} \\ N_A = \frac{5\times10^{22}}{10^{9}} = 5\times10^{13}\ \text{cm}^{-3}\end{gathered}$$

The arsenic donors and the boron acceptors are **equal in number**, so they **compensate each other**: each electron donated by As is captured by a B acceptor, so the net doping $N_D - N_A = 0$. The charge neutrality $n + N_A = p + N_D$ with $np = n_i^2$ gives $n = p = n_i$. The cube therefore has again the same carrier concentrations as pure silicon and

$$\boxed{R \approx 2.4\times10^{5}\ \Omega\ \text{(unchanged)}}$$

(apart from a small reduction of the mobility by ionised impurity scattering, which is ignored here). *For comparison*, with arsenic alone ($N_D = 5\times10^{13}$): $n = 5\times10^{13}$, $p = n_i^2/n = 4.2\times10^{6}$ cm$^{-3}$, $\sigma = 1.6\times10^{-19}\times5\times10^{13}\times1350 = 1.08\times10^{-2}$ S/cm and $R = 92.6\ \Omega$: a factor $2.6\times10^{3}$ lower; it is the compensation by boron that restores the intrinsic resistance.

**(b) Diffusion coefficient of electrons.** From Einstein's relation $D_n = \mu_n\dfrac{kT}{e}$ (the doping level does not enter once $\mu$ is given):

$$\frac{kT}{e} = \frac{1.38\times10^{-23}\times300}{1.6\times10^{-19}} = 0.02588\ \text{V}$$

$$D_n = 1300\times0.02588 = \mathbf{33.6\ cm^2/s} = 3.36\times10^{-3}\ \text{m}^2/\text{s}$$

**(c) Diffusion in a semiconductor and the Einstein relation.** *Diffusion* is the movement of carriers from a region of high concentration to one of low concentration, caused by their random thermal motion and the concentration gradient (not by any field). The diffusion current density for electrons and holes (Fick's law, one dimension) is

$$\begin{gathered}J_n = eD_n\frac{dn}{dx} \\ J_p = -eD_p\frac{dp}{dx}\end{gathered}$$

*(the current for electrons has the same direction as the concentration gradient because the charge is negative; $D$ in cm$^2$/s)*. Diffusion and drift are the two current mechanisms; a p-n junction has a diffusion current of majority carriers which is balanced by the drift of the minority carriers in equilibrium.

*Einstein relation.* Take a non-uniform semiconductor in thermal equilibrium (no net current). Let the doping, hence the electron concentration $n(x)$, decrease with $x$. Electrons diffuse towards larger $x$; this separates charge and builds an internal field $\mathcal{E}(x)$ which gives a drift current opposing the diffusion. At equilibrium, $J_n = 0$:

$$J_n = en\mu_n\mathcal{E} + eD_n\frac{dn}{dx} = 0 \quad\Rightarrow\quad \mathcal{E} = -\frac{D_n}{\mu_n}\frac{1}{n}\frac{dn}{dx}$$

With $\mathcal{E} = -dV/dx$, the electrostatic potential energy of an electron is $-eV$, and the Boltzmann distribution gives $n = n_0\exp(eV/kT)$, so

$$\frac{1}{n}\frac{dn}{dx} = \frac{e}{kT}\frac{dV}{dx} = -\frac{e}{kT}\mathcal{E}$$

Substituting:

$$\mathcal{E} = -\frac{D_n}{\mu_n}\left(-\frac{e}{kT}\mathcal{E}\right) \;\Rightarrow\; 1 = \frac{D_n}{\mu_n}\frac{e}{kT}$$

$$\boxed{\frac{D_n}{\mu_n} = \frac{D_p}{\mu_p} = \frac{kT}{e} = V_T}$$

The ratio of the diffusion coefficient to the mobility is the thermal voltage $V_T = kT/e$ (25.9 mV at 300 K); the same holds for holes. It links the two transport coefficients, so the mobility can give $D$, as in part (b).
