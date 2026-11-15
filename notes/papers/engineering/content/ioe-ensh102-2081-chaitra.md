---
file: NEBians-IOE-Past-Paper-Engineering-Physics-ENSH102-2081-Chaitra.pdf
subject: Engineering Physics
level: BE · Year I / Part I
code: ENSH 102
year_bs: 2081 Chaitra
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
(a) Define calorific value. [[1]]
(b) Define double refraction. [[1]]
(c) Electric lines of forces never cross, why? [[1]]
(d) Write the physical significance of displacement current. [[1]]

@q 2
(a) If the ratio of mass to damping coefficient in a damped harmonic oscillator is 50 sec, find the time in which the energy of the system falls to $\dfrac{1}{e^4}$ of its initial value. [[2]]
(b) Compute the change in entropy when 10 g of ice at 0°C is converted into water at the same temperature. Given that the latent heat of fusion of ice is 80 cal/g. [[2]]
(c) Prove that ratio of electric and magnetic fields at a point in free space is equal to velocity of light in plane electromagnetic wave. [[2]]
(d) An electron is confined in an infinite potential well of width 0.1 nm. Calculate the ground state energy of the electron. [[2]]

@q 3
Write any two differences between bar pendulum and torsion pendulum on the basis of oscillation. Derive the time period of oscillation for torsional pendulum. [[2+2]]
@or
Define resonance. Derive the differential equation of forced harmonic motion and explain the resonance with mathematical explanation. [[4]]

@q 4
The volume of a room is 980 m³. The wall area of the room is 150 m², ceiling area 95 m² and floor area is 90 m². The average sound absorption coefficient for wall is 0.03, for ceiling is 0.80 and for the floor is 0.06. Calculate the average sound absorption coefficient and reverberation time for hall. [[4]]

@q 5
Derive Clapeyron latent heat equation $\dfrac{dP}{dT} = \dfrac{L}{T(V_2 - V_1)}$. Also explain the effect of increase in pressure on boiling point of water and melting point of solid. [[4]]
@or
Explain Einstein's quantum theory of the heat capacity of solids. Derive the expression for the heat capacity using this theory and discuss its agreement with experimental observations. [[4]]

@q 6
(a) Describe intensity distribution in single slit due to diffraction pattern. Hence find the intensity at first order maxima in terms of central maxima. [[4]]
(b) A parallel beam of sodium light of wavelength $5890\times10^{-8}$ cm is incident on a thin glass plate of refractive index 1.5 such that the angle of refraction in the plate is 60°. Calculate the smallest thickness of the plate which will make it appear dark by reflection. [[4]]
(c) Calculate the combined focal length of two thin lenses of focal length $f_1$ and $f_2$ separated by a finite distance $d$. Also find the position of two principal points. [[4]]
(d) Calculate the refractive indices of the core and cladding materials of a fiber from following data NA = 0.22 and fractional refractive index change $\Delta = 0.012$. [[4]]

@q 7
(a) Find the expression for the electric field intensity at a distance $z$ from center along the axis of positively charged circular disc of radius $R$. [[4]]
@or
What is electric quadrupole? Calculate electric potential at a point on the axis of the short quadrupole. [[4]]
(b) A parallel plate capacitor each of area 100 cm² has a potential difference of 500 V and capacitance of $100\times10^{-6}\ \mu$F. If a mica of dielectric constant 5.4 is inserted between plates, find the magnitude of (i) Electric field in mica (ii) Displacement vector and (iii) Polarization vector. [[4]]

@q 8
Derive an expression for the growth and decay of current in LR series circuit. Explain the meaning of inductive time constant. [[4]]

@q 9
Define Poynting vector and prove that $\vec S = \dfrac{1}{\mu}(\vec E\times\vec B)$. [[4]]

@q 10
Write the physical significance of wave function. Using the wave function derive an expression for the time dependent Schrödinger wave equation. [[4]]
<!-- SOLUTIONS -->

@s 1
**(a) Calorific value.** The calorific value of a fuel is the amount of heat energy released when a unit mass (or unit volume, for gases) of the fuel is burnt completely. Its units are J/kg (or kcal/kg, J/m³).

**(b) Double refraction.** When an unpolarised ray of light enters certain anisotropic crystals (calcite, quartz) it splits into **two** refracted rays: the **ordinary ray** ($o$), which obeys Snell's law, and the **extraordinary ray** ($e$), which does not. Both are plane polarised, with their vibrations at right angles to each other.

**(c)** The tangent to a line of force gives the direction of the electric field at that point. If two lines crossed, the field at the point of intersection would have two different directions at once. The electric field has a single, definite direction at every point, so the lines **cannot cross**.

**(d) Displacement current** $I_d = \varepsilon_0\,d\Phi_E/dt$.
- It extends Ampère's law, $\oint\vec B\cdot d\vec l = \mu_0(I + I_d)$, to regions where there is no conduction current (e.g. between the plates of a charging capacitor), so the total current is continuous.
- It shows that a **changing electric field produces a magnetic field**. Together with Faraday's law, this leads to self-propagating electromagnetic waves.

@s 2
**(a)** The energy of a damped oscillator decays as $E = E_0e^{-bt/m}$. We want $E = E_0e^{-4}$, so
$$\frac{bt}{m} = 4\ \Rightarrow\ t = 4\cdot\frac mb = 4\times50 = \boxed{200\ \text{s}}$$

**(b)** At the constant temperature $T = 273$ K, $Q = mL = 10\times80 = 800$ cal.
$$\Delta S = \frac QT = \frac{800}{273} = \boxed{2.93\ \text{cal/K}\ (\approx12.2\ \text{J/K})}$$

**(c)** Take a plane wave travelling along $+x$ with $\vec E = E_y\hat j$, $\vec B = B_z\hat k$, $E_y = E_0\sin(kx - \omega t)$. Faraday's law $\nabla\times\vec E = -\partial\vec B/\partial t$ reduces to
$$\frac{\partial E_y}{\partial x} = -\frac{\partial B_z}{\partial t}$$
Then $kE_0\cos(kx-\omega t) = -\dfrac{\partial B_z}{\partial t}$, and integrating gives $B_z = \dfrac k\omega E_0\sin(kx-\omega t)$ (the constant of integration is zero for a wave). Hence
$$B_0 = \frac{k}{\omega}E_0\ \Rightarrow\ \frac{E_0}{B_0} = \frac{\omega}{k} = c,\qquad \text{and}\qquad \frac EB = c\ \text{at every instant}$$
The wave equation gives $\omega/k = 1/\sqrt{\mu_0\varepsilon_0} = c$ in free space, so the ratio of the fields is the speed of light.

**(d)** For an infinite well of width $L$, $E_n = \dfrac{n^2h^2}{8mL^2}$. With $n = 1$, $L = 0.1$ nm $= 10^{-10}$ m:
$$E_1 = \frac{(6.626\times10^{-34})^2}{8\times9.11\times10^{-31}\times(10^{-10})^2} = 6.02\times10^{-18}\ \text{J}$$
$$\boxed{E_1 = \frac{6.02\times10^{-18}}{1.6\times10^{-19}}\approx37.6\ \text{eV}}$$

@s 3
**Two differences** (bar pendulum vs torsional pendulum):

| Basis | Bar pendulum | Torsion pendulum |
|---|---|---|
| Restoring torque | Due to **gravity**, $-mgl\sin\theta$ | Due to the **elastic twist** of the suspension wire, $-C\theta$ |
| Time period | Depends on $g$, $T = 2\pi\sqrt{(k^2+l^2)/gl}$ | Independent of $g$, $T = 2\pi\sqrt{I/C}$ |
| Plane of oscillation | Vertical plane, about a horizontal axis | Horizontal plane, about the vertical wire |

**Time period of a torsional pendulum.** A disc (or any body) of moment of inertia $I$ about the wire is suspended from a fixed support by a wire of length $l$ and radius $r$. If it is twisted through angle $\theta$, the wire exerts a restoring torque proportional to the twist:
$$\begin{gathered}\tau = -C\theta \\ C = \frac{\pi\eta r^4}{2l}\end{gathered}$$
where $C$ is the torque per unit twist (torsional constant) and $\eta$ is the rigidity modulus. By Newton's second law for rotation,
$$I\frac{d^2\theta}{dt^2} = -C\theta\ \Rightarrow\ \frac{d^2\theta}{dt^2} + \frac CI\theta = 0$$
This is simple harmonic motion with $\omega = \sqrt{C/I}$. Hence
$$\boxed{T = 2\pi\sqrt{\frac IC} = 2\pi\sqrt{\frac{2lI}{\pi\eta r^4}}}$$

**Or. Resonance** is the phenomenon in which a system driven by a periodic force of frequency close to its natural frequency oscillates with maximum amplitude.

**Differential equation.** A body of mass $m$ on a spring (constant $k$) with damping $-b\dot x$ is driven by $F_0\cos\alpha t$:
$$m\ddot x + b\dot x + kx = F_0\cos\alpha t\ \Rightarrow\ \ddot x + 2\gamma\dot x + \omega_0^2x = \frac{F_0}{m}\cos\alpha t$$
with $\gamma = b/2m$ and $\omega_0^2 = k/m$. The transient part dies out and the steady state is $x = A\cos(\alpha t - \varphi)$. Substituting,
$$\left\{(\omega_0^2 - \alpha^2)\cos\varphi + 2\gamma\alpha\sin\varphi - \frac{F_0}{mA}\right\}\cos\alpha t + \left\{(\omega_0^2 - \alpha^2)\sin\varphi - 2\gamma\alpha\cos\varphi\right\}\sin\alpha t = 0$$
Both brackets vanish. The second gives $\tan\varphi = \dfrac{2\gamma\alpha}{\omega_0^2 - \alpha^2}$ and then the first gives
$$A = \frac{F_0/m}{\sqrt{(\omega_0^2 - \alpha^2)^2 + 4\gamma^2\alpha^2}}$$
**Resonance.** The amplitude is maximum when the denominator is minimum: $\dfrac{d}{d\alpha}\left[(\omega_0^2-\alpha^2)^2 + 4\gamma^2\alpha^2\right] = 0$, i.e.
$$\begin{gathered}\boxed{\alpha_r = \sqrt{\omega_0^2 - 2\gamma^2}} \\ A_{\max} = \frac{F_0}{2m\gamma\sqrt{\omega_0^2 - \gamma^2}}\end{gathered}$$
For light damping $\alpha_r\approx\omega_0$ and $A_{\max}\approx F_0/b\omega_0$, which is large; the phase lag is $\varphi = 90^\circ$ at $\alpha = \omega_0$. If there were no damping ($\gamma\to0$), $A\to\infty$. Larger damping lowers and flattens the resonance peak, and moves it to a lower frequency.

@s 4
Total absorption $A = \sum\alpha_iS_i$:
$$\text{wall: }150\times0.03 = 4.5,\quad\text{ceiling: }95\times0.80 = 76.0,\quad\text{floor: }90\times0.06 = 5.4$$
$$\sum\alpha_iS_i = 4.5 + 76.0 + 5.4 = 85.9\ \text{m}^2\ \text{sabin}$$
Total surface area $S = 150 + 95 + 90 = 335$ m².
$$\bar\alpha = \frac{\sum\alpha_iS_i}{S} = \frac{85.9}{335} = \boxed{0.256}$$
By Sabine's formula,
$$T = \frac{0.161\,V}{\sum\alpha_iS_i} = \frac{0.161\times980}{85.9} = \boxed{1.84\ \text{s}}$$

@s 5
**Clapeyron's latent heat equation.** Consider 1 kg of a substance changing phase at temperature $T$ and saturation pressure $P$; $V_1$ and $V_2$ are the specific volumes of the initial and final phases and $L$ is the latent heat. Run a Carnot cycle between $T$ and $T - dT$, with pressures $P$ and $P - dP$.
1. Isothermal at $T$: the phase change absorbs heat $Q_1 = L$ while the volume goes from $V_1$ to $V_2$.
2. Adiabatic cooling to $T - dT$.
3. Isothermal at $T - dT$: the substance returns to the initial phase, rejecting heat $Q_2$.
4. Adiabatic heating back to $T$.

The area of the thin loop on the $P$–$V$ diagram is the work: $W = dP\,(V_2 - V_1)$. The Carnot efficiency is $\eta = \dfrac WL = \dfrac{dT}T$:
$$\frac{dP\,(V_2 - V_1)}{L} = \frac{dT}{T}\ \Rightarrow\ \boxed{\frac{dP}{dT} = \frac{L}{T(V_2 - V_1)}}$$
**Boiling point of water.** Here $V_2$ (steam) $\gg V_1$ (water) and $L>0$, so $dP/dT>0$: raising the pressure **raises** the boiling point (a pressure cooker cooks above 100°C).

**Melting point.** For a substance that expands on melting ($V_2>V_1$), $dP/dT>0$: pressure **raises** its melting point. Ice contracts on melting ($V_2<V_1$), so $dP/dT<0$ and pressure **lowers** its melting point by about 0.0075 K per atmosphere (regelation).

**Or. Einstein's quantum theory of specific heat.** *Assumptions.* Each atom of a solid is an independent three-dimensional harmonic oscillator, equivalent to three one-dimensional oscillators, all with the same frequency $\nu$. The energy of each is quantized, $E = nh\nu$ (Planck).

By Planck's law the average energy of a one-dimensional oscillator at temperature $T$ is
$$\bar E = \frac{h\nu}{e^{h\nu/kT} - 1}$$
For one mole ($N_A$ atoms, $3N_A$ oscillators), with $\theta_E = h\nu/k$ the Einstein temperature,
$$U = 3N_A\bar E = \frac{3N_Ak\theta_E}{e^{\theta_E/T} - 1} = \frac{3R\,\theta_E}{e^{\theta_E/T} - 1}$$
$$\boxed{C_V = \frac{dU}{dT} = 3R\left(\frac{\theta_E}{T}\right)^2\frac{e^{\theta_E/T}}{\left(e^{\theta_E/T} - 1\right)^2}}$$
**Discussion.**
- *High temperature* ($T\gg\theta_E$): $e^{x}\approx1 + x$, so $C_V\to3R\approx5.97$ cal mol⁻¹ K⁻¹, which is the **Dulong–Petit law** (agrees with experiment).
- *Low temperature* ($T\ll\theta_E$): $C_V\approx3R(\theta_E/T)^2e^{-\theta_E/T}\to0$ as $T\to0$. This explains why $C_V$ falls at low temperature, which classical theory could not, in agreement with the experimental trend.
- *Limitation*: the experimental curve falls as $T^3$ (not exponentially), because atoms vibrate with a spread of frequencies. Debye's theory corrects this.

```figure caption="Einstein heat capacity C_V / 3R against T/θ_E. It tends to the Dulong–Petit value 1 at high T and to 0 as T → 0."
import numpy as np, matplotlib.pyplot as plt
t=np.linspace(0.05,3,400); x=1/t
cv=x**2*np.exp(x)/(np.exp(x)-1)**2
fig,ax=plt.subplots(figsize=(4.8,2.5))
ax.plot(t,cv,color=ACCENT); ax.axhline(1,ls='--',color=MUTED,lw=0.9)
ax.text(2.0,1.04,"Dulong–Petit: 3R",fontsize=7.5,color=MUTED)
ax.set_xlabel("T / θ$_E$"); ax.set_ylabel("C$_V$ / 3R"); ax.set_ylim(0,1.15)
```

@s 6
**(a) Single-slit diffraction.** Let a plane wave of wavelength $\lambda$ fall normally on a slit of width $a$. Divide the slit into a large number of equal strips. In the direction $\theta$ the path difference between the two edges is $a\sin\theta$, a phase difference $2\alpha = \dfrac{2\pi}{\lambda}a\sin\theta$. Adding the strip contributions as a vector chain that bends into a circular arc of total length $A_0$ (the amplitude at $\theta = 0$) and subtends angle $2\alpha$, the resultant amplitude is the chord:
$$\begin{gathered}R = \frac{A_0\sin\alpha}{\alpha} \\ I = R^2 = I_0\left(\frac{\sin\alpha}{\alpha}\right)^2,\qquad \alpha = \frac{\pi a\sin\theta}{\lambda}\end{gathered}$$
- **Central maximum**: $\alpha\to0$, $\sin\alpha/\alpha\to1$, so $I = I_0$ (the principal maximum).
- **Minima**: $\sin\alpha = 0$ with $\alpha\ne0$, i.e. $\alpha = \pm n\pi$, so $a\sin\theta = n\lambda$.
- **Secondary maxima**: $\dfrac{dI}{d\alpha} = 0\Rightarrow\tan\alpha = \alpha$, with roots near $\alpha\approx\pm\tfrac32\pi,\pm\tfrac52\pi,\ldots$ (about midway between the minima).

For the first secondary maximum, $\alpha\approx\tfrac{3\pi}2$:
$$\frac{I_1}{I_0} = \left(\frac{\sin(3\pi/2)}{3\pi/2}\right)^2 = \frac{4}{9\pi^2} = 0.045\ \Rightarrow\ \boxed{I_1\approx4.5\%\ \text{of}\ I_0}$$
The next maxima are about $1.6\%$, $0.8\%$, … of $I_0$, so almost all the light falls in the central band, whose width is twice that of the secondary maxima.

```figure caption="Intensity distribution of the single-slit Fraunhofer pattern. The first secondary maximum is about 4.5% of the central one."
import numpy as np, matplotlib.pyplot as plt
a=np.linspace(-4*np.pi,4*np.pi,1200); I=np.sinc(a/np.pi)**2
fig,ax=plt.subplots(figsize=(5.2,2.5))
ax.plot(a/np.pi,I,color=ACCENT); ax.fill_between(a/np.pi,I,color="#eaf1ff")
ax.set_xticks(range(-4,5)); ax.set_xticklabels(["−4π","−3π","−2π","−π","0","π","2π","3π","4π"])
ax.annotate("I$_1$ ≈ 0.045 I$_0$",xy=(1.5,0.045),xytext=(2.1,0.45),arrowprops=dict(arrowstyle="->",color=INK),fontsize=8)
ax.set_xlabel("α = π a sinθ / λ"); ax.set_ylabel("I / I$_0$")
```

**(b)** For a thin film in air, the light reflected from the film is **dark** when
$$\begin{gathered}2\mu t\cos r = n\lambda \\ n = 0, 1, 2,\ldots\end{gathered}$$
(the extra $\lambda/2$ from reflection at the upper surface turns the usual bright condition into the dark one). The smallest non-zero thickness corresponds to $n = 1$:
$$t = \frac{\lambda}{2\mu\cos r} = \frac{5.89\times10^{-5}\ \text{cm}}{2\times1.5\times\cos60^\circ} = \frac{5.89\times10^{-5}}{1.5}$$
$$\boxed{t = 3.93\times10^{-5}\ \text{cm} = 0.393\ \mu\text{m}}$$

**(c) Combined focal length.** Let a ray parallel to the axis at height $h$ fall on lens $L_1$ ($f_1$), with $L_2$ ($f_2$) at distance $d$ behind it. After $L_1$ it converges with slope $-h/f_1$ and reaches $L_2$ at height $h_2 = h - dh/f_1 = h\left(1 - d/f_1\right)$. $L_2$ adds a further deviation $-h_2/f_2$, so the final slope is
$$-\frac{h}{f_1} - \frac{h(1 - d/f_1)}{f_2} = -h\left(\frac1{f_1} + \frac1{f_2} - \frac{d}{f_1f_2}\right) \equiv -\frac hF$$
$$\boxed{\frac1F = \frac1{f_1} + \frac1{f_2} - \frac{d}{f_1f_2}\ \Rightarrow\ F = \frac{f_1f_2}{f_1 + f_2 - d}}$$
**Principal points.** The emergent ray cuts the axis (the second focal point) at distance $v = h_2/(h/F) = F\left(1 - \dfrac d{f_1}\right)$ from $L_2$. The second principal point $H_2$ is where the extended incident ray meets the emergent ray, a distance $F$ before that focus, so its position relative to $L_2$ is
$$\boxed{\beta = v - F = -\frac{Fd}{f_1}}$$
that is, $H_2$ lies a distance $Fd/f_1$ **in front of** (to the left of) $L_2$. By the same argument for a ray travelling the other way, the first principal point $H_1$ lies a distance
$$\boxed{\alpha = +\frac{Fd}{f_2}}$$
**behind** (to the right of) $L_1$. For $d = 0$ both points coincide with the lenses and $1/F = 1/f_1 + 1/f_2$.

**(d)** Numerical aperture $\text{NA} = n_1\sqrt{2\Delta}$ (for $\Delta = (n_1 - n_2)/n_1\ll1$, $\text{NA} = \sqrt{n_1^2 - n_2^2}$).
$$n_1 = \frac{\text{NA}}{\sqrt{2\Delta}} = \frac{0.22}{\sqrt{0.024}} = \frac{0.22}{0.1549} = \boxed{1.42\ (\text{core})}$$
$$n_2 = n_1(1 - \Delta) = 1.420\times0.988 = \boxed{1.403\ (\text{cladding})}$$

@s 7
**(a) Field on the axis of a charged disc.** Let the surface charge density be $\sigma$. Divide the disc into thin rings of radius $x$ and width $dx$, with charge $dq = \sigma\,2\pi x\,dx$. The field of a ring on the axis at distance $z$ is $dE = \dfrac{1}{4\pi\varepsilon_0}\dfrac{z\,dq}{(x^2 + z^2)^{3/2}}$, along the axis. Integrating,
$$E = \frac{\sigma z}{2\varepsilon_0}\int_0^R\frac{x\,dx}{(x^2 + z^2)^{3/2}} = \frac{\sigma z}{2\varepsilon_0}\left[-\frac{1}{\sqrt{x^2 + z^2}}\right]_0^R$$
$$\boxed{E = \frac{\sigma}{2\varepsilon_0}\left[1 - \frac{z}{\sqrt{z^2 + R^2}}\right]}$$
directed away from the disc for $\sigma>0$. Limits: for $z\ll R$, $E\to\sigma/2\varepsilon_0$ (infinite sheet); for $z\gg R$, $E\to\dfrac{\sigma\pi R^2}{4\pi\varepsilon_0z^2}$, the field of a point charge $Q = \sigma\pi R^2$.

**Or. Electric quadrupole.** A quadrupole is a system of two equal and opposite dipoles placed end to end, so that the net charge and the net dipole moment are zero. The linear quadrupole has charges $+q$, $-2q$, $+q$ on a line, with spacing $a$.

**Potential on the axis.** For a point at distance $r$ from the central charge, on the axis:
$$V = \frac{q}{4\pi\varepsilon_0}\left[\frac1{r - a} - \frac2r + \frac1{r + a}\right] = \frac{q}{4\pi\varepsilon_0}\cdot\frac{2a^2}{r(r^2 - a^2)}$$
For a short quadrupole ($r\gg a$), $r^2 - a^2\approx r^2$:
$$\begin{gathered}\boxed{V = \frac{1}{4\pi\varepsilon_0}\frac{2qa^2}{r^3} = \frac{1}{4\pi\varepsilon_0}\frac{Q_q}{r^3}} \\ Q_q = 2qa^2\end{gathered}$$
So the potential of a quadrupole falls as $1/r^3$, compared with $1/r^2$ for a dipole and $1/r$ for a point charge.

**(b)** $C_0 = 100\times10^{-6}\ \mu\text{F} = 10^{-10}\ \text{F} = 100$ pF, $A = 100\ \text{cm}^2 = 10^{-2}\ \text{m}^2$, $V = 500$ V, $K = 5.4$. The capacitor is charged to 500 V and the mica slab is inserted with the charge unchanged, so the free charge density is
$$\sigma = \frac QA = \frac{C_0V}{A} = \frac{10^{-10}\times500}{10^{-2}} = 5\times10^{-6}\ \text{C/m}^2$$
- **(ii)** Displacement vector $D = \sigma = \boxed{5.0\times10^{-6}\ \text{C/m}^2}$ (it depends only on the free charge).
- **(i)** Field in mica $E = \dfrac{D}{K\varepsilon_0} = \dfrac{5\times10^{-6}}{5.4\times8.854\times10^{-12}} = \boxed{1.05\times10^5\ \text{V/m}}$.
- **(iii)** Polarisation $P = D - \varepsilon_0E = D\left(1 - \dfrac1K\right) = 5\times10^{-6}\times0.815 = \boxed{4.07\times10^{-6}\ \text{C/m}^2}$.

*Remark.* If the battery were kept connected (constant $V$), then $d = \varepsilon_0A/C_0 = 0.885$ mm, $E = V/d = 5.65\times10^5$ V/m, $D = K\varepsilon_0E = 2.70\times10^{-5}$ C/m² and $P = (K-1)\varepsilon_0E = 2.20\times10^{-5}$ C/m².

@s 8
An inductor $L$ and a resistor $R$ are in series with a battery of emf $V$ and a switch.

**Growth of current.** After the switch is closed, Kirchhoff's voltage law gives
$$V = L\frac{di}{dt} + iR\ \Rightarrow\ \frac{di}{V/R - i} = \frac RL\,dt$$
Integrating with $i = 0$ at $t = 0$: $-\ln\left(\dfrac VR - i\right)\Big|_0^i = \dfrac RLt$, so
$$\boxed{i = \frac VR\left(1 - e^{-Rt/L}\right) = i_0\left(1 - e^{-t/\tau}\right)}$$
where $i_0 = V/R$ is the final steady current and $\tau = L/R$.

**Decay of current.** When the battery is removed with the circuit kept closed through $R$ ($V = 0$) from the state $i = i_0$:
$$L\frac{di}{dt} + iR = 0\ \Rightarrow\ \frac{di}{i} = -\frac RL\,dt\ \Rightarrow\ \boxed{i = i_0\,e^{-Rt/L} = i_0e^{-t/\tau}}$$

**Inductive time constant** $\tau = L/R$ (unit: second). It is the time in which the growing current reaches $\left(1 - \tfrac1e\right) = 63.2\%$ of its final value, or the decaying current falls to $\tfrac1e = 36.8\%$ of its initial value. A large $L$ or a small $R$ gives slow growth and decay: the inductor opposes the change of current.

```figure caption="Growth and decay of current in an LR circuit; τ = L/R."
import numpy as np, matplotlib.pyplot as plt
t=np.linspace(0,5,300)
fig,ax=plt.subplots(figsize=(4.8,2.5))
ax.plot(t,1-np.exp(-t),color=ACCENT,label="growth  i = i$_0$(1 − e$^{-t/τ}$)")
ax.plot(t,np.exp(-t),color=SERIES[1],label="decay  i = i$_0$e$^{-t/τ}$")
ax.plot([1,1],[0,0.632],ls=':',color=MUTED); ax.axhline(0.632,ls=':',color=MUTED,lw=0.8); ax.axhline(0.368,ls=':',color=MUTED,lw=0.8)
ax.set_xlabel("t / τ"); ax.set_ylabel("i / i$_0$"); ax.legend(loc="center right",fontsize=7)
```

@s 9
The **Poynting vector** $\vec S$ is the rate of flow of electromagnetic energy per unit area, in the direction of propagation of the wave. Its unit is W/m².

**Proof.** Maxwell's equations in a medium give $\nabla\times\vec E = -\dfrac{\partial\vec B}{\partial t}$ and $\nabla\times\vec H = \vec J + \dfrac{\partial\vec D}{\partial t}$. Use the identity $\nabla\cdot(\vec E\times\vec H) = \vec H\cdot(\nabla\times\vec E) - \vec E\cdot(\nabla\times\vec H)$:
$$\nabla\cdot(\vec E\times\vec H) = -\vec H\cdot\frac{\partial\vec B}{\partial t} - \vec E\cdot\vec J - \vec E\cdot\frac{\partial\vec D}{\partial t}$$
For linear media, $\vec H\cdot\partial\vec B/\partial t + \vec E\cdot\partial\vec D/\partial t = \dfrac{\partial}{\partial t}\left(\tfrac12\vec B\cdot\vec H + \tfrac12\vec E\cdot\vec D\right) = \dfrac{\partial u}{\partial t}$, where $u$ is the energy density of the field. Hence
$$-\frac{\partial u}{\partial t} = \nabla\cdot(\vec E\times\vec H) + \vec E\cdot\vec J$$
This is the energy-conservation statement. The decrease of field energy per unit volume per second equals the outflow $\nabla\cdot\vec S$ plus the work $\vec E\cdot\vec J$ done on charges. So the energy flux is
$$\begin{gathered}\vec S = \vec E\times\vec H = \boxed{\frac{1}{\mu}\left(\vec E\times\vec B\right)} \\ (\vec B = \mu\vec H)\end{gathered}$$
In free space, $|\vec S| = \dfrac{EB}{\mu_0}$, perpendicular to both $\vec E$ and $\vec B$. Since $E = cB$, $S = \varepsilon_0cE^2$, and its time average is $\tfrac12\varepsilon_0cE_0^2$.

@s 10
**Physical significance of the wave function $\psi$.**
- $\psi(x, t)$ describes the quantum state of a particle. It is in general complex and is not directly measurable.
- $|\psi|^2 = \psi^*\psi$ is the **probability density**: $|\psi|^2dV$ is the probability of finding the particle in the volume $dV$.
- Normalisation: $\int|\psi|^2dV = 1$ over all space, since the particle is certainly somewhere.
- To be acceptable $\psi$ must be single-valued, finite and continuous, with a continuous first derivative.

**Time-dependent Schrödinger equation.** For a free particle moving along $x$ with momentum $p = \hbar k$ and energy $E = \hbar\omega$, the de Broglie wave is
$$\psi = Ae^{i(kx - \omega t)}$$
Differentiating,
$$\frac{\partial\psi}{\partial t} = -i\omega\psi\ \Rightarrow\ i\hbar\frac{\partial\psi}{\partial t} = \hbar\omega\psi = E\psi$$
$$\frac{\partial^2\psi}{\partial x^2} = -k^2\psi\ \Rightarrow\ -\hbar^2\frac{\partial^2\psi}{\partial x^2} = \hbar^2k^2\psi = p^2\psi$$
For a particle in a potential $V(x, t)$ the total energy is $E = \dfrac{p^2}{2m} + V$. Multiply by $\psi$ and use the two relations:
$$E\psi = \frac{p^2}{2m}\psi + V\psi$$
$$\boxed{i\hbar\frac{\partial\psi}{\partial t} = -\frac{\hbar^2}{2m}\frac{\partial^2\psi}{\partial x^2} + V\psi}$$
This is the **time-dependent Schrödinger equation**; in three dimensions $\partial^2/\partial x^2\to\nabla^2$, i.e. $i\hbar\,\partial\psi/\partial t = \hat H\psi$. For a time-independent $V$, putting $\psi = \phi(x)e^{-iEt/\hbar}$ gives the time-independent equation $-\dfrac{\hbar^2}{2m}\phi'' + V\phi = E\phi$.
