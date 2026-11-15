---
file: NEBians-IOE-Past-Paper-Engineering-Physics-ENSH152-2083-Baishakh.pdf
subject: Engineering Physics
level: BE · Year I / Part II
code: ENSH 152
year_bs: 2083 Baishakh
cal: BS
year_ad: 2026
stream: BCE, BME, BAG, BCH
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Back paper (new course). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
(a) Why thermal resistance is important in building science? [[1]]
(b) Write the name of retardation plate which produces circularly polarized light. [[1]]
(c) Mention the importance of supercapacitor. [[1]]
(d) Write the equation for rise of current in an LR circuit and sketch the graph. [[1]]

@q 2
(a) Show that the vibrating motion of a particle given by $y = Re^{i\omega t}$ is simple harmonic. [[2]]
(b) If the Einstein's temperature of a solid is 100°C, calculate the Einstein's frequency. [[2]]
(c) Convert Maxwell equation $\nabla\times\vec E = -\dfrac{\partial\vec B}{\partial t}$ into integral form. [[2]]
(d) Derive the relation between phase velocity and group velocity. [[2]]

@q 3
Derive the differential equation of forced oscillation and show that the maximum amplitude at resonance varies inversely with damping coefficient. [[4]]
@or
Show that the point of suspension and the point of oscillation are interchangeable in bar pendulum. [[4]]

@q 4
A room has dimensions of 6 m × 4 m × 5 m. Find (i) average distance travelled by the sound for two successive reflections and (ii) number of reflections made per second by the sound wave from the walls of the room. Given velocity of sound in air is 350 m s⁻¹. [[4]]

@q 5
What is Pyrheliometer? How can you measure solar constant using Pyrheliometer? [[4]]
@or
State Stefan's-Boltzmann law of radiation and prove it using the first law of thermodynamics and Maxwell's thermodynamics relation. [[4]]

@q 6
(a) Explain with necessary theory to obtain the radius of $n^{th}$ bright ring and $n^{th}$ dark ring in Newton's ring due to reflected system. [[4]]
(b) A diffraction grating with 400 lines per millimeter is illuminated normally by monochromatic light of wavelength 6000 Å. Calculate (i) the angle at which the first-order maxima occur (ii) the maximum number of diffraction maxima that can be observed. [[4]]
(c) Derive the expressions for acceptance angle and numerical aperture of an optical fiber. [[4]]
(d) The focal length of an achromatic combination of two lenses in contact is 120 cm. If the dispersive powers of the materials of the two lenses are 0.02 and 0.03, calculate the focal lengths of the two individual lenses. [[4]]

@q 7
(a) Define electric quadruple and quadruple moment. Derive the expression for electric potential on the axis of linear quadruple. [[4]]
@or
Find the electric field intensity at a distance $z$ above the center of a flat circular disk of radius $a$, which carries a uniform surface charge density $\sigma$. [[4]]
(b) If $a$ and $b$ are internal and external radii of a cylindrical capacitor then show that the half of the energy lies within $r = \sqrt{ab}$. [[4]]

@q 8
Derive an expression for energy stored by an inductor. Show that the energy density in magnetic field is directly proportional to the square of magnetic field. [[4]]

@q 9
State and prove charge conservation theorem. [[4]]

@q 10
Calculate the energy difference between ground state and first excited state for an electron in one dimensional infinite potential well of width 1 Å. Mass of electron ($m_e$) = $9.1\times10^{-31}$ kg and Planck's constant ($h$) = $6.62\times10^{-34}$ J s, 1 eV = $1.6\times10^{-19}$ J. [[4]]
<!-- SOLUTIONS -->

@s 1
**(a) Thermal resistance in building science.** Thermal resistance $R = \dfrac{L}{kA}$ (or $R = L/k$ per unit area, the "R-value") measures how strongly a layer of material opposes the flow of heat. For a wall made of several layers the resistances add, $R_{tot} = \sum L_i/k_i$, and the heat flow is $Q = \Delta T/R_{tot}$ (equivalently $U = 1/R_{tot}$).
It matters because it lets a designer choose walls, roofs and glazing so that **heat loss in winter and heat gain in summer are small**: lower energy for heating/cooling, a comfortable indoor temperature, and no surface condensation or mould.

**(b)** The **quarter-wave plate**. When plane polarised light falls on it with its vibration at $45^\circ$ to the optic axis, the $o$- and $e$-components have equal amplitude and a phase difference $\pi/2$ (path difference $\lambda/4$), so the emergent light is **circularly polarised**.

**(c) Importance of a supercapacitor.** A supercapacitor (electrochemical double-layer capacitor) has a capacitance of hundreds to thousands of farad. It sits between an ordinary capacitor and a battery:
- very high **power density** and charge/discharge in seconds,
- very long life ($10^5$–$10^6$ cycles) and wide temperature range,
- used for regenerative braking, power back-up and memory retention, smoothing of solar/wind power, and starting of engines.

**(d) Growth of current in an LR circuit.** With a battery of emf $E$ switched on at $t=0$:
$$\begin{gathered}\boxed{i = \frac{E}{R}\left(1 - e^{-Rt/L}\right) = I_0\left(1 - e^{-t/\tau}\right)} \\ I_0 = \frac ER,\qquad \tau = \frac LR\end{gathered}$$
The current starts from zero, reaches $63.2\%$ of $I_0$ after one time constant $\tau$ and approaches $I_0$ exponentially.

```figure caption="Rise of current in an LR circuit. After one time constant tau = L/R the current is 63.2% of its final value I0."
import numpy as np, matplotlib.pyplot as plt
t=np.linspace(0,5,300); i=1-np.exp(-t)
fig,ax=plt.subplots(figsize=(4.6,2.6))
ax.plot(t,i,color=ACCENT,lw=1.8)
ax.axhline(1,ls='--',color=MUTED,lw=0.9); ax.axhline(0.632,ls=':',color=MUTED,lw=0.9)
ax.plot([1,1],[0,0.632],ls=':',color=MUTED,lw=0.9); ax.plot([1],[0.632],'o',color=SERIES[1],ms=4)
ax.text(3.3,1.03,"$I_0$ = E / R",fontsize=8,color=MUTED); ax.text(1.1,0.55,"0.632 $I_0$ at t = $\\tau$",fontsize=8,color=MUTED)
ax.set_xlabel("t / $\\tau$"); ax.set_ylabel("i / $I_0$"); ax.set_ylim(0,1.15); ax.set_xlim(0,5)
```

@s 2
**(a)** $y = Re^{i\omega t}$. Differentiate twice with respect to $t$:
$$\begin{gathered}\frac{dy}{dt} = i\omega Re^{i\omega t} = i\omega y \\ \frac{d^2y}{dt^2} = (i\omega)^2y = -\omega^2y\end{gathered}$$
$$\Rightarrow\ \frac{d^2y}{dt^2} + \omega^2y = 0$$
This is the differential equation of simple harmonic motion: acceleration is proportional to the displacement and opposite to it. Therefore the motion (the real part $R\cos\omega t$, or the imaginary part $R\sin\omega t$) is **simple harmonic** with angular frequency $\omega$ and period $T = 2\pi/\omega$.

**(b) Einstein's frequency.** Einstein's characteristic temperature is $\theta_E = \dfrac{h\nu_E}{k_B}$, so
$$\nu_E = \frac{k_B\theta_E}{h} = \frac{(1.38\times10^{-23})(373)}{6.62\times10^{-34}} = \boxed{7.8\times10^{12}\ \text{Hz}}$$
($\theta_E = 100^\circ\text{C} = 373$ K). If $\theta_E$ were read as 100 K, the frequency would be $2.1\times10^{12}$ Hz.

**(c) Integral form of Faraday's law.** Integrate over an open surface $S$ bounded by the closed loop $C$ and apply Stokes' theorem $\int_S(\nabla\times\vec E)\cdot d\vec S = \oint_C\vec E\cdot d\vec l$:
$$\int_S(\nabla\times\vec E)\cdot d\vec S = -\int_S\frac{\partial\vec B}{\partial t}\cdot d\vec S$$
$$\boxed{\oint_C\vec E\cdot d\vec l = -\frac{d}{dt}\int_S\vec B\cdot d\vec S = -\frac{d\Phi_B}{dt}}$$
The induced emf round a closed path equals the negative rate of change of magnetic flux through it.

**(d) Phase velocity and group velocity.** Phase velocity $v_p = \omega/k$ and group velocity $v_g = d\omega/dk$, where $k = 2\pi/\lambda$. Since $\omega = kv_p$,
$$v_g = \frac{d(kv_p)}{dk} = v_p + k\frac{dv_p}{dk}$$
Using $k = 2\pi/\lambda$, $dk = -\dfrac{2\pi}{\lambda^2}d\lambda$, so $k\dfrac{dv_p}{dk} = -\lambda\dfrac{dv_p}{d\lambda}$:
$$\boxed{v_g = v_p - \lambda\frac{dv_p}{d\lambda}}$$
In a non-dispersive medium $dv_p/d\lambda = 0$ and $v_g = v_p$. In normal dispersion $dv_p/d\lambda>0$, so $v_g<v_p$.

@s 3
**Differential equation of forced oscillation.** A body of mass $m$ is acted on by a restoring force $-kx$, a damping force $-b\dot x$ ($b$ is the damping coefficient) and a periodic driving force $F_0\cos\alpha t$. Newton's second law:
$$m\ddot x + b\dot x + kx = F_0\cos\alpha t$$
$$\begin{gathered}\Rightarrow\ \boxed{\ddot x + 2\gamma\dot x + \omega_0^2x = \frac{F_0}{m}\cos\alpha t} \\ \gamma = \frac{b}{2m},\ \ \omega_0^2 = \frac km\end{gathered}$$

**Steady state.** After the transient dies out, the body oscillates at the driving frequency, $x = A\cos(\alpha t - \varphi)$. Substitute and compare coefficients of $\cos\alpha t$ and $\sin\alpha t$:
$$\begin{gathered}(\omega_0^2 - \alpha^2)A\cos\varphi + 2\gamma\alpha A\sin\varphi = \frac{F_0}{m} \\ (\omega_0^2 - \alpha^2)\sin\varphi = 2\gamma\alpha\cos\varphi\end{gathered}$$
so $\tan\varphi = \dfrac{2\gamma\alpha}{\omega_0^2 - \alpha^2}$ and
$$A = \frac{F_0/m}{\sqrt{(\omega_0^2 - \alpha^2)^2 + 4\gamma^2\alpha^2}}$$

**Resonance.** $A$ is largest when $D = (\omega_0^2 - \alpha^2)^2 + 4\gamma^2\alpha^2$ is smallest:
$$\frac{dD}{d\alpha} = -4\alpha(\omega_0^2 - \alpha^2) + 8\gamma^2\alpha = 0\ \Rightarrow\ \alpha_r^2 = \omega_0^2 - 2\gamma^2$$
Putting this back, $D_{\min} = 4\gamma^2(\omega_0^2 - \gamma^2)$, hence
$$\boxed{A_{\max} = \frac{F_0}{2m\gamma\sqrt{\omega_0^2 - \gamma^2}} = \frac{F_0}{b\sqrt{\omega_0^2 - b^2/4m^2}}}$$
Since $F_0$, $m$ and $\omega_0$ are fixed, $A_{\max}\propto\dfrac{1}{\gamma}\propto\dfrac1b$. For light damping $\alpha_r\approx\omega_0$ and $A_{\max}\approx\dfrac{F_0}{b\omega_0}$: **the resonance amplitude varies inversely with the damping coefficient**; with no damping it would become infinite.

```figure caption="Amplitude against driving frequency for three damping coefficients. The peak height varies inversely with damping and shifts slightly below omega0."
import numpy as np, matplotlib.pyplot as plt
w=np.linspace(0,2,500); w0=1
fig,ax=plt.subplots(figsize=(4.8,2.7))
for g,c in zip([0.05,0.1,0.25],SERIES):
    A=1/np.sqrt((w0**2-w**2)**2+4*g**2*w**2)
    ax.plot(w,A,color=c,label="$\\gamma$ = %.2f"%g)
ax.set_xlabel("driving frequency $\\alpha$ / $\\omega_0$"); ax.set_ylabel("amplitude (arb.)"); ax.legend(); ax.set_ylim(0,11)
```

**Or. Bar pendulum: suspension point and oscillation point are interchangeable.** For a bar (physical) pendulum of mass $M$ and radius of gyration $k$ about the centre of gravity $G$, suspended at $S$ at distance $l_1$ from $G$:
$$\begin{gathered}T = 2\pi\sqrt{\frac{I_S}{Mgl_1}} = 2\pi\sqrt{\frac{k^2 + l_1^2}{gl_1}} = 2\pi\sqrt{\frac{L}{g}} \\ L = l_1 + \frac{k^2}{l_1}\end{gathered}$$
$L$ is the length of the equivalent simple pendulum. Mark the point $O$ on the line $SG$ produced, at distance $L$ from $S$. It is the **centre of oscillation**, and its distance from $G$ is
$$l_2 = L - l_1 = \frac{k^2}{l_1}\ \Rightarrow\ l_1l_2 = k^2$$
Now suspend the bar at $O$. The distance of the new suspension point from $G$ is $l_2$, so the equivalent length is
$$L' = l_2 + \frac{k^2}{l_2} = \frac{k^2}{l_1} + l_1 = L$$
Hence $T' = 2\pi\sqrt{L'/g} = T$. The time period is the same when the bar is hung from $S$ or from $O$: the points of suspension and oscillation are **interchangeable** (the principle of Kater's reversible pendulum, which gives $g = 4\pi^2L/T^2$).

@s 4
Volume $V = 6\times4\times5 = 120\ \text{m}^3$. Total surface area
$$S = 2(6\times4 + 4\times5 + 6\times5) = 2(24 + 20 + 30) = 148\ \text{m}^2$$
**(i)** The mean free path of sound in a room (average distance between two successive reflections) is
$$\bar d = \frac{4V}{S} = \frac{4\times120}{148} = \boxed{3.24\ \text{m}}$$
**(ii)** Number of reflections per second
$$n = \frac{v}{\bar d} = \frac{350}{3.24} = \boxed{\approx108\ \text{reflections per second}}$$

@s 5
**Pyrheliometer.** A pyrheliometer is an instrument that measures the intensity of direct solar radiation falling normally on a surface, in W m⁻² (or cal cm⁻² min⁻¹). Its detector is a blackened receiver which absorbs the beam coming through a narrow tube that is pointed at the Sun.

**Ångström's electrical compensation pyrheliometer.** Two identical thin blackened manganin strips $A_1$ and $A_2$, each of area $A$, carry thermocouple junctions and are mounted behind a collimating tube.
1. $A_1$ is exposed to the Sun while $A_2$ is shaded. The heated strip becomes warmer, and the thermocouple (galvanometer) shows a deflection.
2. A current $I$ is sent through the shaded strip (resistance $R_s$) and adjusted until the galvanometer reads zero, so both strips are at equal temperature.
3. Heat absorbed from the Sun per second equals the electrical heating:
$$aSA = I^2R_s\ \Rightarrow\ \boxed{S = \frac{I^2R_s}{aA}}$$
where $a$ is the absorptivity of the blackened strip and $S$ the intensity at the ground.

**Solar constant.** The reading $S_z$ is taken after the beam has passed through the atmosphere. By the Bouguer–Langley law, for the Sun at zenith angle $z$ (air mass $m = \sec z$),
$$S_z = S_0e^{-\kappa\sec z}\ \Rightarrow\ \ln S_z = \ln S_0 - \kappa\sec z$$
Readings are taken at several times of a clear day. A graph of $\ln S_z$ against $\sec z$ is a straight line; extrapolated to $\sec z = 0$ (no atmosphere) the intercept gives $\ln S_0$, i.e. the **solar constant**
$$S_0\approx1.36\ \text{kW m}^{-2}\ (\approx1.95\ \text{cal cm}^{-2}\text{min}^{-1})$$
(Abbot's silver-disc pyrheliometer measures $S = \dfrac{mc\,\Delta\theta}{aAt}$ from the temperature rise $\Delta\theta$ of a blackened silver disc of mass $m$, specific heat $c$, exposed for time $t$.)

**Or. Stefan–Boltzmann law.** The total energy radiated per second per unit area of a black body is proportional to the fourth power of its absolute temperature:
$$\begin{gathered}E = \sigma T^4 \\ \sigma = 5.67\times10^{-8}\ \text{W m}^{-2}\text{K}^{-4}\end{gathered}$$

**Proof (Boltzmann).** Take black-body radiation in a cavity of volume $V$ at temperature $T$. Let $u$ be the energy density (a function of $T$ only), so $U = uV$. Maxwell's electromagnetic theory gives the radiation pressure $P = \dfrac u3$.

*Maxwell's relation.* From the first and second laws, $dU = TdS - PdV$. Taking $S(T,V)$:
$$dU = T\left(\frac{\partial S}{\partial T}\right)_VdT + \left[T\left(\frac{\partial S}{\partial V}\right)_T - P\right]dV$$
and using the Maxwell relation $\left(\dfrac{\partial S}{\partial V}\right)_T = \left(\dfrac{\partial P}{\partial T}\right)_V$ we get the thermodynamic equation of state
$$\left(\frac{\partial U}{\partial V}\right)_T = T\left(\frac{\partial P}{\partial T}\right)_V - P$$
For radiation, $\left(\dfrac{\partial U}{\partial V}\right)_T = u$ and $\left(\dfrac{\partial P}{\partial T}\right)_V = \dfrac13\dfrac{du}{dT}$. Therefore
$$u = \frac T3\frac{du}{dT} - \frac u3\ \Rightarrow\ 4u = T\frac{du}{dT}\ \Rightarrow\ \frac{du}{u} = 4\frac{dT}{T}$$
Integrating, $\ln u = 4\ln T + \text{const}$, i.e.
$$\boxed{u = aT^4}$$
The energy emitted per second per unit area of the black body is $E = \dfrac{c}{4}u = \dfrac{ac}{4}T^4 = \sigma T^4$, which is the **Stefan–Boltzmann law** (the constant $a = 4\sigma/c$ cannot come from thermodynamics alone; Planck's law supplies it).

@s 6
**(a) Newton's rings by reflected light.** A plano-convex lens of radius of curvature $R$ rests on a flat glass plate. The air film between them has thickness $t$ at distance $r$ from the point of contact. From the geometry of the circle, $r^2 = 2Rt - t^2\approx2Rt$ (since $t\ll R$):
$$t = \frac{r^2}{2R}$$
For normal incidence in air ($\mu = 1$, $\cos\theta = 1$) the effective path difference between the ray reflected from the top and bottom surfaces of the film is $2t$, plus a half wavelength $\lambda/2$ because the ray reflected from the glass plate (denser medium) suffers a phase change of $\pi$:
$$\Delta = 2t + \frac\lambda2$$

*Bright rings* (constructive, $\Delta = n\lambda$):
$$2t + \frac\lambda2 = n\lambda\ \Rightarrow\ \frac{r^2}{R} = \frac{(2n-1)\lambda}{2}$$
$$\begin{gathered}\boxed{r_n = \sqrt{\frac{(2n-1)\lambda R}{2}},\qquad D_n = \sqrt{2(2n-1)\lambda R}} \\ n = 1, 2, 3,\ldots\end{gathered}$$
*Dark rings* (destructive, $\Delta = (2n+1)\dfrac\lambda2$):
$$2t = n\lambda\ \Rightarrow\ \frac{r^2}{R} = n\lambda$$
$$\begin{gathered}\boxed{r_n = \sqrt{n\lambda R},\qquad D_n = 2\sqrt{n\lambda R}} \\ n = 0, 1, 2,\ldots\end{gathered}$$
The centre ($t = 0$, $n=0$) is dark. The diameters of the dark rings are proportional to $\sqrt n$, the square roots of the natural numbers, so the rings crowd together as $n$ increases. Bright-ring radii are proportional to $\sqrt{2n-1}$, the square roots of the odd numbers.

**(b) Diffraction grating.** $N = 400$ lines/mm, so the grating element is
$$\begin{gathered}d = \frac{1}{400}\ \text{mm} = 2.5\times10^{-6}\ \text{m} \\ \lambda = 6000\ \text{Å} = 6.0\times10^{-7}\ \text{m}\end{gathered}$$
**(i)** $d\sin\theta = n\lambda$ with $n = 1$:
$$\sin\theta_1 = \frac{\lambda}{d} = \frac{6.0\times10^{-7}}{2.5\times10^{-6}} = 0.24\ \Rightarrow\ \boxed{\theta_1 = 13.9^\circ}$$
**(ii)** The largest possible order has $\sin\theta\le1$:
$$n_{\max}\le\frac d\lambda = \frac{2.5\times10^{-6}}{6.0\times10^{-7}} = 4.17\ \Rightarrow\ \boxed{n_{\max} = 4}$$
Four orders can be seen on each side of the central maximum, so the total number of maxima is $2\times4 + 1 = \boxed{9}$.

**(c) Acceptance angle and numerical aperture.** An optical fibre has a core of refractive index $n_1$ and a cladding of smaller index $n_2$; the outside medium (air) has $n_0 = 1$. A ray enters the end face at angle of incidence $\theta_0$ and refracts at angle $\theta_r$. It then meets the core–cladding interface at angle of incidence $\varphi = 90^\circ - \theta_r$.

*Snell's law at the entry face:* $n_0\sin\theta_0 = n_1\sin\theta_r$.

*Limiting case:* the ray just undergoes total internal reflection when $\varphi$ equals the critical angle $\varphi_c$, where $\sin\varphi_c = n_2/n_1$. Then
$$\sin\theta_r = \cos\varphi_c = \sqrt{1 - \frac{n_2^2}{n_1^2}} = \frac{\sqrt{n_1^2 - n_2^2}}{n_1}$$
so the maximum angle at the entry face is
$$\boxed{\theta_{0,\max} = \sin^{-1}\left(\frac{\sqrt{n_1^2 - n_2^2}}{n_0}\right)}$$
This is the **acceptance angle**: all rays entering within a cone of half angle $\theta_{0,\max}$ are guided. The **numerical aperture** is the sine of this angle (for $n_0 = 1$):
$$\begin{gathered}\boxed{\text{NA} = \sin\theta_{0,\max} = \sqrt{n_1^2 - n_2^2} = n_1\sqrt{2\Delta}} \\ \Delta = \frac{n_1 - n_2}{n_1}\end{gathered}$$

**(d) Achromatic doublet.** Two thin lenses in contact are achromatic when
$$\frac{\omega_1}{f_1} + \frac{\omega_2}{f_2} = 0\ \Rightarrow\ f_2 = -\frac{\omega_2}{\omega_1}f_1 = -\frac{0.03}{0.02}f_1 = -1.5f_1$$
and the combined focal length is $\dfrac1F = \dfrac1{f_1} + \dfrac1{f_2}$:
$$\frac1{120} = \frac1{f_1} - \frac1{1.5f_1} = \frac{1}{3f_1}\ \Rightarrow\ f_1 = 40\ \text{cm}$$
$$\boxed{f_1 = +40\ \text{cm (convex)},\qquad f_2 = -60\ \text{cm (concave)}}$$
Check: $\dfrac1{40} - \dfrac1{60} = \dfrac1{120}$ ✓ and $\dfrac{0.02}{40} - \dfrac{0.03}{60} = 0$ ✓.

@s 7
**(a) Electric quadrupole.** A linear electric quadrupole is a system of three collinear charges $+q$, $-2q$, $+q$ with spacing $d$ (the middle charge is at the centre). Equivalently, it is two equal and opposite dipoles placed end to end. Its net charge and net dipole moment are zero. The **quadrupole moment** is
$$Q = \sum q_iz_i^2 = q d^2 + 0 + qd^2 = 2qd^2$$

**Potential on the axis.** Take a point $P$ on the axis at distance $r$ from the centre ($r>d$). The distances of $P$ from the charges are $r - d$, $r$ and $r + d$.
$$V = \frac{1}{4\pi\varepsilon_0}\left[\frac{q}{r-d} - \frac{2q}{r} + \frac{q}{r+d}\right] = \frac{q}{4\pi\varepsilon_0}\left[\frac{2r}{r^2 - d^2} - \frac2r\right]$$
$$= \frac{q}{4\pi\varepsilon_0}\cdot\frac{2d^2}{r(r^2 - d^2)}$$
For a short quadrupole ($r\gg d$), $r^2 - d^2\approx r^2$:
$$\boxed{V = \frac{2qd^2}{4\pi\varepsilon_0r^3} = \frac{Q}{4\pi\varepsilon_0r^3}}$$
The quadrupole potential falls as $1/r^3$ (monopole $1/r$, dipole $1/r^2$) and the field, $E = -dV/dr = \dfrac{3Q}{4\pi\varepsilon_0r^4}$, falls as $1/r^4$.

**Or. Field on the axis of a uniformly charged disc.** Take a ring of radius $x$ and width $dx$ on the disc. Its charge is $dq = \sigma\,2\pi x\,dx$. At a point on the axis at height $z$, the components perpendicular to the axis cancel, and only the axial component survives:
$$dE = \frac{1}{4\pi\varepsilon_0}\frac{dq}{x^2 + z^2}\cos\theta = \frac{1}{4\pi\varepsilon_0}\frac{\sigma2\pi x\,dx\ z}{(x^2 + z^2)^{3/2}}$$
$$E = \frac{\sigma z}{2\varepsilon_0}\int_0^a\frac{x\,dx}{(x^2 + z^2)^{3/2}} = \frac{\sigma z}{2\varepsilon_0}\left[-\frac{1}{\sqrt{x^2 + z^2}}\right]_0^a$$
$$\boxed{E = \frac{\sigma}{2\varepsilon_0}\left(1 - \frac{z}{\sqrt{z^2 + a^2}}\right)}$$
directed along the axis away from the disc if $\sigma>0$. *Limits:* for $a\to\infty$ (infinite sheet) $E\to\sigma/2\varepsilon_0$; for $z\gg a$, $E\approx\dfrac{\sigma\pi a^2}{4\pi\varepsilon_0z^2} = \dfrac{q}{4\pi\varepsilon_0z^2}$, the field of a point charge.

**(b) Energy in a cylindrical capacitor.** Let the inner radius be $a$, the outer radius $b$, length $L$, and charge $\pm q$. By Gauss' law, the field between the cylinders is
$$\begin{gathered}E = \frac{q}{2\pi\varepsilon_0Lr} \\ (a<r<b)\end{gathered}$$
The energy density is $u = \dfrac12\varepsilon_0E^2$. The energy in a thin shell of radius $r$ and thickness $dr$ (volume $2\pi rL\,dr$) is
$$dU = \frac12\varepsilon_0\left(\frac{q}{2\pi\varepsilon_0Lr}\right)^2 2\pi rL\,dr = \frac{q^2}{4\pi\varepsilon_0L}\frac{dr}{r}$$
The energy stored between $a$ and a radius $r$ is
$$\begin{gathered}U(r) = \frac{q^2}{4\pi\varepsilon_0L}\ln\frac ra \\ U_{\text{total}} = \frac{q^2}{4\pi\varepsilon_0L}\ln\frac ba\end{gathered}$$
For half the energy to lie within $r$:
$$\ln\frac ra = \frac12\ln\frac ba = \ln\sqrt{\frac ba}\ \Rightarrow\ r = a\sqrt{\frac ba}\ \Rightarrow\ \boxed{r = \sqrt{ab}}$$
Thus half of the energy lies within $r = \sqrt{ab}$, the geometric mean of the radii.

@s 8
**Energy stored in an inductor.** An inductor of inductance $L$ carries a current $i$ which is increasing, so a back emf $\mathcal E = -L\dfrac{di}{dt}$ opposes it. The source must do work against this emf. The power supplied is
$$P = \frac{dW}{dt} = -\mathcal E\,i = Li\frac{di}{dt}$$
The work done in raising the current from 0 to $I$ is
$$W = \int_0^ILi\,di = \frac12LI^2$$
This work is stored in the magnetic field:
$$\boxed{U_B = \frac12LI^2}$$

**Energy density.** Take a long solenoid of length $l$, cross-section $A$ and $n$ turns per unit length. Its inductance and field are
$$\begin{gathered}L = \mu_0n^2Al \\ B = \mu_0nI\ \Rightarrow\ I = \frac{B}{\mu_0n}\end{gathered}$$
$$U_B = \frac12\mu_0n^2Al\cdot\frac{B^2}{\mu_0^2n^2} = \frac{B^2}{2\mu_0}Al$$
The field fills the volume $Al$, so the energy per unit volume is
$$\boxed{u_B = \frac{U_B}{Al} = \frac{B^2}{2\mu_0}}\ \propto B^2$$
That is, the magnetic energy density is directly proportional to the square of the magnetic field. (In a medium of permeability $\mu$ this is $B^2/2\mu = \tfrac12\vec B\cdot\vec H$.)

@s 9
**Statement.** The net electric charge of an isolated system is conserved: charge can neither be created nor destroyed. Locally, the charge leaving a region per second equals the decrease of the charge inside it. This is expressed by the **equation of continuity**
$$\nabla\cdot\vec J + \frac{\partial\rho}{\partial t} = 0$$
where $\vec J$ is the current density and $\rho$ the volume charge density.

**Proof from Maxwell's equations.** Take Ampère–Maxwell's law
$$\nabla\times\vec H = \vec J + \frac{\partial\vec D}{\partial t}$$
and take the divergence of both sides. The divergence of a curl is zero:
$$0 = \nabla\cdot\vec J + \frac{\partial}{\partial t}(\nabla\cdot\vec D)$$
By Gauss' law $\nabla\cdot\vec D = \rho$, therefore
$$\boxed{\nabla\cdot\vec J + \frac{\partial\rho}{\partial t} = 0}$$
**Integral form.** Integrate over a volume $V$ bounded by the closed surface $S$ and use the divergence theorem:
$$\oint_S\vec J\cdot d\vec S = -\frac{d}{dt}\int_V\rho\,dV = -\frac{dq}{dt}$$
The net current flowing out through $S$ equals the rate of decrease of charge inside. For an isolated system no current crosses $S$, so $dq/dt = 0$ and the total charge is **constant**. (Without Maxwell's displacement current term, $\nabla\cdot(\nabla\times\vec H)$ would force $\nabla\cdot\vec J = 0$ and contradict charging capacitors; the displacement current restores charge conservation.)

@s 10
For an electron in a one-dimensional infinite well of width $L$ ($V = 0$ for $0<x<L$, infinite outside), the time-independent Schrödinger equation gives
$$\begin{gathered}\psi_n = \sqrt{\frac2L}\sin\frac{n\pi x}{L} \\ E_n = \frac{n^2h^2}{8mL^2}\end{gathered}$$
The ground state ($n = 1$) and first excited state ($n = 2$):
$$E_1 = \frac{h^2}{8mL^2} = \frac{(6.62\times10^{-34})^2}{8(9.1\times10^{-31})(10^{-10})^2} = 6.02\times10^{-18}\ \text{J} = 37.6\ \text{eV}$$
$$E_2 = 4E_1 = 2.41\times10^{-17}\ \text{J} = 150.5\ \text{eV}$$
$$\Delta E = E_2 - E_1 = 3E_1 = \boxed{1.81\times10^{-17}\ \text{J}\approx113\ \text{eV}}$$
($L = 1\ \text{Å} = 10^{-10}$ m.)
